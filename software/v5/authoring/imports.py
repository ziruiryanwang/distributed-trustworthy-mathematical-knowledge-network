"""Operation-local verified import selection; never deserialize an acceptance.

The owner process and ReceiptVerifier installation are trusted. This is not a
hostile-Python sandbox. Canonical data returned by this adapter remains data;
the guest and final receiver independently verify the resulting contribution.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import time

from admission.verifier import ReceiptVerifier, VerifiedModule
from modules import codec as C
from modules.model import ConditionalEnvironment, ImportClaim
from modules.receipt.witness import decode_journal, make_input


@dataclass(frozen=True)
class _Record:
    handle: VerifiedModule
    receipt: bytes
    summary: bytes
    journal: bytes


class ImportSession:
    """A single-owner bounded session; no persistence of verification authority.

    A module selects one exact receipt/journal for this operation. Other proofs
    of the same module cannot silently replace its rank or parent assumption.
    close() revokes this session only; the separately owned verifier stays open.
    """
    def __init__(self, verifier, *, max_modules=8, max_calls=4096,
                 receipt_bytes=64*1024**2, data_bytes=16*1024**2, wall_seconds=3600):
        C.require(type(verifier) is ReceiptVerifier, "IMPORT_OWNER_VERIFIER_REQUIRED")
        for value, cap in ((max_modules, 8), (max_calls, 65536),
                           (receipt_bytes, 1024**3), (data_bytes, 16*1024**2),
                           (wall_seconds, 86400)):
            C.require(0 < C.uint(value, cap), "IMPORT_SESSION_LIMIT")
        self._verifier = verifier
        self._profile = verifier.report()["profile_id"]
        C.digest_string(self._profile)
        self._deadline = time.monotonic()+wall_seconds
        self._closed = False
        self._max_modules, self._max_calls = max_modules, max_calls
        self._receipt_cap, self._data_cap = receipt_bytes, data_bytes
        self._calls = self._receipt_bytes = self._data_bytes = 0
        self._records: dict[str, _Record] = {}
        self._cache: dict[tuple[str, bytes, str], str] = {}
        self._groups: dict[tuple[str, int], bytes] = {}
        self._bodies: dict[tuple[str, int, str], bytes] = {}

    def _active(self):
        C.require(not self._closed and time.monotonic() < self._deadline,
                  "IMPORT_SESSION_CLOSED_OR_EXPIRED")

    def _begin(self):
        self._active()
        C.require(self._calls < self._max_calls, "IMPORT_SESSION_CALL_BUDGET")
        self._calls += 1  # Failed and deduplicated calls still consume a request.

    def _describe(self, module):
        self._active()
        C.digest_string(module)
        C.require(module in self._records, "IMPORT_UNSELECTED_MODULE")
        record = self._records[module]
        live = self._verifier.describe(record.handle)
        C.require(live["profile_id"] == self._profile and live["module"] == module
                  and C.canonical(live["summary"]) == record.summary
                  and live["journal"] == record.journal
                  and live["receipt_sha256"] == hashlib.sha256(record.receipt).hexdigest(),
                  "IMPORT_LIVE_HANDLE_BINDING")
        parsed = decode_journal(record.journal)
        C.require(parsed["module"] == module and C.canonical(parsed["summary"]) == record.summary,
                  "IMPORT_EXACT_JOURNAL_SUMMARY")
        self._active()
        return parsed

    def _register(self, handle, receipt):
        C.require(type(receipt) is bytes and 0 < len(receipt) <= 64*1024**2,
                  "IMPORT_RECEIPT_BOUND")
        live = self._verifier.describe(handle)
        summary = C.canonical(live["summary"])
        digest = hashlib.sha256(receipt).hexdigest()
        C.require(live["profile_id"] == self._profile and live["receipt_sha256"] == digest,
                  "IMPORT_RECEIPT_HANDLE_MISMATCH")
        parsed = decode_journal(live["journal"])
        module = parsed["module"]
        C.require(module == live["module"] and C.canonical(parsed["summary"]) == summary,
                  "IMPORT_JOURNAL_BINDING")
        previous = self._records.get(module)
        if previous is not None:
            self._describe(module)
            C.require(previous.receipt == receipt and previous.summary == summary
                      and previous.journal == live["journal"], "IMPORT_PARENT_SELECTION_CONFLICT")
        else:
            C.require(len(self._records) < self._max_modules
                      and self._receipt_bytes+len(receipt) <= self._receipt_cap,
                      "IMPORT_RECEIPT_STORAGE_BUDGET")
            self._active()
            self._records[module] = _Record(handle, receipt, summary, live["journal"])
            self._receipt_bytes += len(receipt)
        self._cache[self._profile, summary, digest] = module
        return module

    def use_handle(self, handle, receipt):
        """Adopt a handle minted by THIS live verifier, with exact receipt bytes."""
        self._begin()
        return self._register(handle, receipt)

    def receive(self, receipt, expected_summary, operation_directory, **limits):
        """Verify a new exact parent once, or reuse its still-live exact handle.

        A cache hit does not create operation_directory. A different receipt of
        an already selected ModuleID refuses before another verifier operation.
        """
        self._begin()
        C.require(type(receipt) is bytes and 0 < len(receipt) <= 64*1024**2,
                  "IMPORT_RECEIPT_BOUND")
        module = C.summary_id(expected_summary)
        summary = C.canonical(expected_summary)
        key = self._profile, summary, hashlib.sha256(receipt).hexdigest()
        if key in self._cache:
            self._describe(module)
            C.require(self._records[module].receipt == receipt, "IMPORT_EXACT_CACHED_RECEIPT")
            return module
        C.require(module not in self._records, "IMPORT_PARENT_SELECTION_CONFLICT")
        C.require(len(self._records) < self._max_modules
                  and self._receipt_bytes+len(receipt) <= self._receipt_cap,
                  "IMPORT_RECEIPT_STORAGE_BUDGET")
        remaining = int(self._deadline-time.monotonic())
        C.require(remaining >= 1, "IMPORT_SESSION_DEADLINE")
        requested_wall = limits.pop("wall_seconds", 60)
        C.require(type(requested_wall) is int and 1 <= requested_wall <= 600,
                  "IMPORT_PER_CALL_WALL")
        handle = self._verifier.receive(receipt, C.parse_json(summary), operation_directory,
            wall_seconds=min(requested_wall, remaining), **limits)
        self._active()
        return self._register(handle, receipt)

    def open_group(self, module, opening):
        self._begin()
        self._describe(module)
        group = self._verifier.open_group(self._records[module].handle, opening)
        raw = C.canonical(opening)
        key = module, opening["index"]
        previous = self._groups.get(key)
        C.require(previous is None or previous == raw, "IMPORT_OPENING_MUTATION")
        if previous is None:
            C.require(len(self._groups) < C.DEFAULT_LIMITS.max_groups
                      and self._data_bytes+len(raw) <= self._data_cap,
                      "IMPORT_OPENING_STORAGE_BUDGET")
            self._active()
            self._groups[key] = raw
            self._data_bytes += len(raw)
        return group

    def supply_body(self, module, universes, expression):
        self._begin()
        self._describe(module)
        digest = C.body_id(expression, universes)
        allowed = False
        for (owner, _), raw in self._groups.items():
            if owner != module:
                continue
            for descriptor in C.parse_json(raw)["group"]["declarations"]:
                if descriptor["universes"] != universes:
                    continue
                if descriptor["kind"] in ("definition", "opaque"):
                    allowed |= descriptor["value_hash"] == digest
                elif descriptor["kind"] == "recursor":
                    allowed |= any(rule["value_hash"] == digest for rule in descriptor["meta"]["rules"])
        C.require(allowed, "IMPORT_BODY_NOT_COMMITTED_BY_SELECTED_GROUP")
        raw = C.canonical(expression)
        key = module, universes, digest
        previous = self._bodies.get(key)
        C.require(previous is None or previous == raw, "IMPORT_BODY_MUTATION")
        if previous is None:
            C.require(self._data_bytes+len(raw) <= self._data_cap, "IMPORT_BODY_STORAGE_BUDGET")
            self._active()
            self._bodies[key] = raw
            self._data_bytes += len(raw)
        return digest

    def selected_data(self):
        """Copied frontend data, NOT a transferable verification token."""
        self._begin()
        records = []
        for module, record in sorted(self._records.items()):
            parsed = self._describe(module)
            openings = [C.parse_json(raw) for (owner, _), raw in sorted(self._groups.items())
                        if owner == module]
            for opening in openings:
                self._verifier.open_group(record.handle, opening)
            bodies = [{"universes": arity, "digest": digest, "expression": C.parse_json(raw)}
                      for (owner, arity, digest), raw in sorted(self._bodies.items()) if owner == module]
            records.append({"module": module, "journal": record.journal,
                            "receipt": record.receipt, "summary": parsed["summary"],
                            "openings": openings, "bodies": bodies})
        self._active()
        return records

    def make_request(self, local_environment, foundation_rows, image):
        """Construct an untrusted prover input and exact real parent witnesses.

        Caller-created imported claims are refused; only freshly revalidated
        session selections create import roles. This does not prove the child.
        """
        self._begin()
        C.require(type(local_environment) is ConditionalEnvironment
                  and not local_environment.claims
                  and all(owner == local_environment.module for owner, _ in local_environment.groups),
                  "IMPORT_LOCAL_ONLY_ENVIRONMENT_REQUIRED")
        # Copy local values into a private environment; never mutate the caller.
        env = ConditionalEnvironment(local_environment.spec)
        for (arity, _), raw in local_environment.bodies.items():
            env.supply_body(C.parse_json(raw), arity)
        for address, digest in local_environment.local_proofs.items():
            descriptor = local_environment.declarations[address].descriptor
            env.supply_local_value(address.name, C.parse_json(local_environment.bodies[descriptor["universes"], digest]))
        parents, receipts = [], []
        for item in self.selected_data():
            C.require(item["openings"], "IMPORT_SELECTED_PARENT_WITHOUT_GROUP")
            parsed = decode_journal(item["journal"])
            env.add_claim(ImportClaim(module=item["module"], foundation=parsed["foundation"],
                policy=parsed["policy"], group_root=parsed["group_root"], group_count=parsed["group_count"],
                rank=parsed["rank"], journal_hash=hashlib.sha256(item["journal"]).hexdigest(),
                receipt_hash=hashlib.sha256(item["receipt"]).hexdigest()))
            for opening in item["openings"]:
                env.add_import_opening(item["module"], opening)
            for body in item["bodies"]:
                env.supply_body(body["expression"], body["universes"])
            parents.append({"journal": item["journal"], "openings": item["openings"]})
            receipts.append({"module": item["module"], "journal": item["journal"], "receipt": item["receipt"]})
        request = make_input(env, foundation_rows, image, parents)
        for module in self._records:
            self._describe(module)
        self._active()
        return {"status": "UNTRUSTED_PROVER_REQUEST_NOT_CHILD_ADMISSION",
                "input": request, "parent_receipts": receipts}

    def close(self):
        self._closed = True
        self._records.clear()
        self._cache.clear()
        self._groups.clear()
        self._bodies.clear()

"""One finite ordinary client for mixed extensions or exact certified targets.

New closed custody profile; frozen mixed/atomic clients remain unchanged. Only
actual I/A/mixed issuers grant authority. Structural custody and publication do
not. This is trusted-owner Windows software, not a hostile-source sandbox.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
import os
from pathlib import Path
import secrets
import sqlite3
import sys
import time

from admission.verifier import ReceiptVerifier
from aggregate_claims.aggregate_admission import AggregateReceiptVerifier
from aggregate_claims import bindings as B
from custody.module_store import ModuleStore, permitted_hashes
from discovery import formal_features as F
from discovery.discovery_store import Store, ordinary
from discovery.module_export_adapter import ModuleExportAdapter
from evidence_network.packet import inspect_evidence, parse_terminal, pack_terminal
from evidence_network.custody import PacketStore, public_profile, profile_id
from evidence_network.transport import EvidenceAcquisition
from mixed_claims.authoring_atomic import MixedOwnerPreparation
from mixed_claims.packet import Envelope
from mixed_claims.receiver import MixedDeltaVerifier
from modules import codec as C
from transport.receipt_client import AcquisitionBudget
from transport import acquisition_resilience as AR
from transport.acquisition_resilience import try_body as _try_body
from . import workspace_mixed as M
from .workspace_atomic import (
    OperationGrant, LiveWarrant, Candidate, PartialPublicationError,
    _sha, _copy, _under, _action, _async_action)

MIB = 1024**2
SCHEMA = "DMKN_V5_CLIENT_EVIDENCE_WORKSPACE_V1"
REPORT_SCHEMA = "DMKN_V5_CLIENT_EVIDENCE_REPORT_V1"


class Workspace(M.Workspace):
    """Fresh concrete two-form store; no old-workspace migration or proxy store."""
    @classmethod
    def open(cls, root, config, create=False):
        F.need(os.name == "nt", "CLIENT_WINDOWS_OWNER_REQUIRED")
        F.fields(config, ("schema", "wire_profile", "module_limits", "packet_limits", "index_limits",
            "packet_envelope", "terminal_receipt_bytes", "max_operations", "max_report_bytes", "ledger_pages"))
        F.need(config["schema"] == SCHEMA, "CLIENT_EVIDENCE_WORKSPACE_SCHEMA")
        profile_id(config["wire_profile"])
        F.uint(config["terminal_receipt_bytes"], 1, 8*MIB)
        F.uint(config["max_operations"], 1, 4096); F.uint(config["max_report_bytes"], 1024, MIB)
        F.uint(config["ledger_pages"], 256, 65536)
        envelope = Envelope(**config["packet_envelope"]); envelope.validate()
        self = cls.__new__(cls)
        self.root = ordinary(root, fresh=create)
        self.config, self._config_raw = _copy(config), C.canonical(config)
        self._envelope = envelope
        self._closed, self._client, self._poisoned = False, None, False
        self._grants, self._lock, self.db = {}, None, None
        self.modules = self.packets = self.index = None
        if create: self.root.mkdir()
        try:
            import msvcrt
            lock = self.root/"owner.lock"
            if lock.exists(): ordinary(lock, directory=False)
            self._lock = lock.open("a+b")
            if lock.stat().st_size == 0:
                self._lock.write(b"\0"); self._lock.flush(); os.fsync(self._lock.fileno())
            self._lock.seek(0); msvcrt.locking(self._lock.fileno(), msvcrt.LK_NBLCK, 1)
            ledger = ordinary(self.root/"workspace.sqlite", fresh=create, directory=False)
            self.db = sqlite3.connect(ledger, timeout=1, isolation_level=None)
            self.db.execute("PRAGMA journal_mode=DELETE"); self.db.execute("PRAGMA synchronous=FULL")
            self.db.execute("PRAGMA temp_store=MEMORY"); self.db.execute("PRAGMA mmap_size=0")
            F.need(self.db.execute("PRAGMA max_page_count="+str(config["ledger_pages"])).fetchone()[0]
                   == config["ledger_pages"], "CLIENT_LEDGER_CAP")
            if create:
                self.db.executescript("""
                    BEGIN IMMEDIATE;
                    CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), config BLOB NOT NULL);
                    CREATE TABLE operations(id TEXT PRIMARY KEY, grant BLOB NOT NULL,
                        status TEXT NOT NULL, report BLOB) WITHOUT ROWID;
                    CREATE TABLE publications(id TEXT PRIMARY KEY, operation TEXT NOT NULL,
                        intent BLOB NOT NULL, outcome BLOB NOT NULL) WITHOUT ROWID;
                    COMMIT;
                """)
                self.db.execute("INSERT INTO meta VALUES(1,?)", (self._config_raw,))
                (self.root/"operations").mkdir()
            held = self.db.execute("SELECT config FROM meta WHERE id=1").fetchone()
            F.need(held is not None and bytes(held[0]) == self._config_raw, "CLIENT_WORKSPACE_CONFIG")
            ordinary(self.root/"operations", directory=True)
            self.adapter = ModuleExportAdapter(C, B.FOUNDATION, B.POLICY)
            self.modules = ModuleStore(self.root/"modules", C, B.FOUNDATION, B.POLICY,
                                       config["module_limits"], create=create)
            self.packets = PacketStore(self.root/"packets", config["wire_profile"], config["packet_limits"],
                envelope=envelope, terminal_receipt_bytes=config["terminal_receipt_bytes"], create=create)
            self.index = Store(self.root/"index", self.adapter, config["index_limits"], create=create)
            self.db.execute("UPDATE operations SET status='INTERRUPTED_WITH_UNCERTAIN_TAIL' "
                            "WHERE status IN ('GRANTED','OPEN','FAILED_PENDING_CLOSE')")
            return self
        except BaseException:
            self._release(); raise

    def operation(self, grant, *, aggregate_owner, delta_owner, receipt_owner=None,
                  preparation_owner=None, foundation_bytes, foundation_sha256):
        """Transfer exact owners on SUCCESS only; caller cleans failed construction."""
        self._active(); self._grant_active(grant)
        F.need(not self._poisoned and self._client is None, "CLIENT_OPERATION_ACTIVE_OR_UNCERTAIN")
        F.need(type(grant) is OperationGrant and grant in self._grants
               and grant._workspace is self and not grant._used, "CLIENT_EXACT_UNUSED_GRANT")
        client = CommonsClient(self, grant, receipt_owner, aggregate_owner, delta_owner,
                               preparation_owner, foundation_bytes, foundation_sha256)
        self._record(grant.identifier, "OPEN")
        grant._used = True; self._client = client
        return client

    def status(self):
        return {**super().status(), "schema": SCHEMA}


class CommonsClient(M.CommonsClient):
    """Concrete two-form specialization; same original I/A/delta owner lifetime."""
    def __init__(self, workspace, grant, receipt, aggregate, delta, preparation, foundation, foundation_sha):
        # Frozen predecessor's exact owner/suballocation contract, specialized
        # only at its lexical custody/profile and required source-origin seams.
        F.need(type(aggregate) is AggregateReceiptVerifier and type(delta) is MixedDeltaVerifier
               and (receipt is None or type(receipt) is ReceiptVerifier), "CLIENT_MIXED_EXACT_REAL_OWNERS")
        F.need(preparation is None or type(preparation) is MixedOwnerPreparation,
               "CLIENT_EXACT_PREPARATION_OWNER")
        image = workspace.config["wire_profile"]["aggregate_image"]
        F.need(type(workspace.packets) is PacketStore
               and profile_id(workspace.config["wire_profile"]) == workspace.packets.profile_id
               and workspace.packets.profile == public_profile(image), "CLIENT_EVIDENCE_CUSTODY_PROFILE")
        F.need(len(delta._owners) == 2 and delta._owners[0] is receipt and delta._owners[1] is aggregate
               and delta._aggregate_image == aggregate._image == image
               and (aggregate._foundation, aggregate._policy) == (B.FOUNDATION, B.POLICY)
               and (delta._image, delta._foundation, delta._policy)
                   == (B.RELATION_IMAGE, B.FOUNDATION, B.POLICY), "CLIENT_SHARED_MIXED_ORIGIN")
        if receipt is not None:
            F.need((receipt._image, receipt._foundation, receipt._policy)
                   == (B.RELATION_IMAGE, B.FOUNDATION, B.POLICY), "CLIENT_SHARED_I_ORIGIN")
            receipt._check_install()
            F.need(receipt.report()["attempts"] == receipt.report()["live_handles"] == 0,
                   "CLIENT_PRISTINE_I_ISSUER")
        aggregate._check_live(); delta._check()
        ar, dr = aggregate.report(), delta.report()
        F.need(all(ar[key] == 0 for key in ("attempts", "submitted_receipt_bytes", "reserved_cpu_seconds",
            "member_calls", "submitted_member_bytes", "live_aggregates", "live_members",
            "reserved_output_bytes", "reserved_output_entries"))
            and dr["attempts"] == dr["live_handles"] == 0, "CLIENT_PRISTINE_MIXED_ISSUERS")
        F.need(all(owner._deadline <= grant.deadline for owner in (receipt, aggregate, delta)
                   if owner is not None), "CLIENT_ORIGINAL_OWNER_DEADLINE")
        F.need(delta._started >= grant.started and aggregate._controller_started >= grant._cpu
               and asdict(delta._envelope) == asdict(workspace._envelope), "CLIENT_DELTA_STARTED_OR_ENVELOPE")
        _under(delta._output, grant.directory)
        caps = grant._limits; acquisition = caps["acquisition"]
        F.need(all(owner._caps[2] <= acquisition["worker_cpu_seconds"]
                   and owner._caps[1] <= acquisition["verification_input_bytes"]
                   for owner in (receipt, aggregate, delta) if owner is not None)
               and delta._caps[0] <= acquisition["verify_attempts"]
               and delta._caps[3] <= caps["controller_cpu_seconds"]
               and delta._caps[5] <= caps["output_bytes"] and delta._caps[6] <= caps["output_entries"],
               "CLIENT_OWNER_SUBALLOCATION")
        F.need(aggregate._member_caps[0] <= caps["imports"]["max_calls"]
               and aggregate._member_caps[1] <= caps["imports"]["max_members"]
               and aggregate._member_caps[2] <= caps["input_bytes"]
               and aggregate._controller_cpu_cap <= caps["controller_cpu_seconds"]
               and aggregate._output_caps[0] <= caps["output_bytes"]
               and aggregate._output_caps[1] <= caps["output_entries"], "CLIENT_AGGREGATE_SUBALLOCATION")
        preparation_cpu = 0
        if preparation is not None:
            preparation._check()
            F.need(preparation.report()["calls"] == 0 and preparation._started >= grant.started
                   and preparation._deadline <= grant.deadline
                   and preparation._allowance["controller_cpu_seconds"] <= caps["controller_cpu_seconds"],
                   "CLIENT_PRISTINE_PREPARATION_DEADLINE")
            _under(preparation._output, grant.directory)
            preparation_cpu = preparation._allowance["worker_cpu_seconds"]
        F.need(preparation_cpu+acquisition["worker_cpu_seconds"] <= caps["worker_cpu_seconds"],
               "CLIENT_DISJOINT_AUTHOR_ADMISSION_SUBALLOCATION")
        F.need(type(foundation) is bytes and 0 < len(foundation) <= 16*MIB
               and _sha(foundation) == foundation_sha, "CLIENT_FOUNDATION_PIN")
        F.need(len(foundation) <= caps["input_bytes"], "CLIENT_FOUNDATION_INPUT_LIMIT")
        self.workspace, self.grant = workspace, grant
        self.receipt, self.aggregate, self.delta, self.preparation = receipt, aggregate, delta, preparation
        self._origin_owners = receipt, aggregate, delta, preparation
        self._aggregate_image = image
        self._profiles = None if receipt is None else receipt.report()["profile_id"], ar["profile_id"], dr["profile_id"]
        root = Path(__file__).resolve().parents[1]
        names = ("client", "client.workspace_atomic", "client.workspace_mixed", "client.workspace_evidence",
            "mixed_network", "mixed_network.custody", "mixed_network.transport",
            "evidence_network", "evidence_network.packet", "evidence_network.custody", "evidence_network.transport")
        self._required_origins = {name: root/(name.replace(".", "/")+
            ("/__init__.py" if "." not in name else ".py")) for name in names}
        pins = {path: pin for owner in (receipt, aggregate, delta) if owner is not None
                for path, pin in owner._pins.items()}
        F.need(set(self._required_origins.values()) <= set(pins), "CLIENT_EVIDENCE_REQUIRED_SOURCE_PINS")
        self._source_pins = {path: deepcopy(pins[path]) for path in self._required_origins.values()}
        self._origin_stores = workspace.modules, workspace.packets, workspace.index
        self._foundation, self._foundation_sha = foundation, foundation_sha
        self._state, self._busy, self._closed = "OPEN", False, False
        self._cleanup_uncertain = False
        self._calls, self._input_bytes = 0, len(foundation)
        self._warrants, self._receipt_cache, self._packet_cache, self._aggregate_cache = {}, {}, {}, {}
        self._candidates, self._context, self._selection_view, self._session = {}, None, None, None
        self._channel = self._handoff = self._search = self._acquisition = None
        self._query_used = False
        self._budget = AcquisitionBudget(grant.deadline, acquisition)
        self._failures, self._publications = [], []
        self._counts = {key: 0 for key in ("admission_submissions", "same_live_hits", "author_calls",
            "store_calls", "publication_attempts", "new_import_sessions")}
        self._active(); self._census()

    def _active(self):
        super()._active()
        stores = self.workspace.modules, self.workspace.packets, self.workspace.index
        F.need(all(a is b for a, b in zip(stores, self._origin_stores)), "CLIENT_EVIDENCE_STORE_CHANGED")
        F.need(type(self.workspace.packets) is PacketStore
               and self.workspace.packets.profile == public_profile(self._aggregate_image)
               and self.workspace.packets.profile_id == profile_id(self.workspace.config["wire_profile"])
               and asdict(self.workspace.packets.envelope) == asdict(self.workspace._envelope)
               and self.workspace.packets.terminal_receipt_bytes == self.workspace.config["terminal_receipt_bytes"],
               "CLIENT_EVIDENCE_STORE_PROFILE_CHANGED")
        F.need(M is sys.modules["client.workspace_mixed"]
               and inspect_evidence is sys.modules["evidence_network.packet"].inspect_evidence
               and parse_terminal is sys.modules["evidence_network.packet"].parse_terminal
               and pack_terminal is sys.modules["evidence_network.packet"].pack_terminal
               and PacketStore is sys.modules["evidence_network.custody"].PacketStore
               and EvidenceAcquisition is sys.modules["evidence_network.transport"].EvidenceAcquisition,
               "CLIENT_EVIDENCE_IMPORTED_SYMBOL_CHANGED")
        if self._acquisition is not None:
            F.need(type(self._acquisition) is EvidenceAcquisition
                   and self._acquisition.budget is self._budget and self._acquisition.verifier is None
                   and self._acquisition.modules is self.workspace.modules
                   and self._acquisition.packets is self.workspace.packets
                   and self._acquisition.profile == self.workspace.config["wire_profile"],
                   "CLIENT_EVIDENCE_ACQUISITION_ORIGIN")
            self._acquisition._active()

    def _inspect(self, raw):
        return inspect_evidence(raw, self.workspace._envelope, aggregate_image=self._aggregate_image,
            terminal_receipt_bytes=self.workspace.config["terminal_receipt_bytes"])

    def _expected(self, exact, expected):
        if expected is not None:
            F.need(type(expected) is bytes and len(expected) == 184, "CLIENT_EXPECTED_EXACT_J_BYTES")
            B.member_journal(expected)
            F.need(exact == expected, "CLIENT_EXPECTED_EXACT_J_MISMATCH")

    def _admit_evidence(self, raw, summary, expected, native_cpu, receipt_cpu, wall, memory):
        for value in (native_cpu, receipt_cpu, wall): F.uint(value, 1, 600)
        F.uint(memory, 64, 4096)
        kind, target, exact, unused = self._inspect(raw)
        F.need(target == summary, "CLIENT_EVIDENCE_TARGET_SUMMARY")
        self._expected(exact, expected)
        if kind == "mixed":
            token = super()._admit_packet(raw, summary, native_cpu, receipt_cpu, wall, memory)
        else:
            F.need(kind == "terminal", "CLIENT_EVIDENCE_KIND")
            receipt, header, journal, index, siblings, unused = parse_terminal(raw, self.workspace._envelope,
                aggregate_image=self._aggregate_image,
                terminal_receipt_bytes=self.workspace.config["terminal_receipt_bytes"])
            token = M.CommonsClient.admit_aggregate_member.__wrapped__(self,
                receipt, header, journal, index, list(siblings), cpu_seconds=receipt_cpu,
                wall_seconds=wall, memory_mib=memory)
        unused_kind, unused_handle, unused_raw, live = self._warrant(token)
        F.need(live["journal"] == exact and live["summary"] == summary, "CLIENT_EVIDENCE_LIVE_TARGET")
        self._expected(live["journal"], expected)
        # This cache is only a same-live acquisition locator. On a terminal
        # hit, admission still rebinds/charges exact membership via the A core.
        self._packet_cache[(_sha(raw), len(raw), C.canonical(summary))] = token
        return token

    @_action
    def admit_local(self, module, packet_sha256, packet_bytes, *, expected_exact_journal=None,
                    native_cpu_seconds=30, receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024):
        raw = self._store(self.workspace.packets.get, packet_sha256, packet_bytes); self._charge(raw)
        summary, unused = self.workspace.packets.inspect(module, raw)
        return self._admit_evidence(raw, summary, expected_exact_journal, native_cpu_seconds,
                                    receipt_cpu_seconds, wall_seconds, memory_mib)

    @_async_action
    async def resolve(self, provider, record):
        F.need(self._search is not None, "CLIENT_SEARCH_NOT_READY")
        self._charge(C.canonical(record))
        if self._acquisition is None:
            self._acquisition = EvidenceAcquisition.from_search(self._handoff,
                public_profile(self._aggregate_image), self.workspace.modules, self.workspace.packets,
                verifier=None)
        resolved = await self._acquisition.export(provider, record)
        candidate = Candidate()
        self._candidates[candidate] = provider, _copy({**resolved, "candidate_origin": "ORIGINATING_INDEX_SEARCH"})
        return candidate

    def _selected_supplier(self, supplier):
        """Select only an existing original contact; never create or renew one."""
        F.need(type(supplier) is str and self._acquisition is not None
               and self._search is not None
               and supplier in self._acquisition.endpoints
               and supplier in self._search._adopted_endpoints,
               "CLIENT_SUPPLIER_NOT_AUTHORIZED")
        contact = self._acquisition.endpoints[supplier]
        F.need(contact is self._acquisition.structural.endpoints.get(supplier)
               and contact._budget is self._budget
               and contact._endpoint == self._search._adopted_endpoints[supplier]
               and self._search.endpoints[supplier] == contact._endpoint
               and contact._policy is self._search._policy
               and contact._expires == min(self.grant.deadline, self._search._expiries[supplier]),
               "CLIENT_SUPPLIER_ORIGINAL_CONTACT")
        return supplier

    @_action
    def check_supplier(self, supplier):
        """No-I/O live-contact check for explicit choices, including cache hits.

        This costs a facade call/input bytes, not a network attempt. It returns
        inert data, creates no token and does not establish who supplied cached
        bytes. A later actual request still reserves and checks at predial.
        """
        selected = self._selected_supplier(supplier)
        self._charge(C.canonical({"supplier": selected}))
        self._acquisition.endpoints[selected].validate()
        return {"status": "AUTHORIZED_LIVE_CONTACT", "supplier": selected,
                "mathematical_acceptance": False}

    @_async_action
    async def resolve_declaration(self, origin_candidate, module, relative_name, *, max_bytes,
                                  supplier=None):
        provider, unused = self._candidate(origin_candidate)
        selection = {}
        if supplier is not None:
            provider = self._selected_supplier(supplier)
            selection["supplier"] = provider
        self._charge(C.canonical({"module": module, "relative_name": relative_name,
                                 "max_bytes": max_bytes, **selection}))
        resolved = await self._acquisition.declaration(provider, module, relative_name, max_bytes)
        self._charge(C.canonical(resolved["opening"]))
        candidate = Candidate()
        # New exact-name data from Q get a new Q candidate. The origin token,
        # its recorded P supplier and all its mathematical bytes stay unchanged.
        self._candidates[candidate] = provider, _copy({**resolved, "candidate_origin": "EXACT_NAME_NOT_INDEX_SEARCH"})
        return candidate

    @_async_action
    async def acquire_body(self, candidate, digest, *, max_bytes, supplier=None):
        provider, resolved = self._candidate(candidate)
        selection = {}
        if supplier is not None:
            provider = self._selected_supplier(supplier)
            selection["supplier"] = provider
        self._charge(C.canonical({"digest": digest, "max_bytes": max_bytes, **selection}))
        # A held authentic descriptor fixes the demanded body. Q need not
        # supply a redundant declaration opening merely to serve these bytes.
        result = await self._acquisition.body(provider, resolved, digest, max_bytes)
        self._charge(C.canonical(result["body"]))
        return result

    def _body_attempt_sources(self):
        """Adopt only already-selected source pins, never hash arbitrary code."""
        F.need(AR is sys.modules["transport.acquisition_resilience"]
               and _try_body is AR.try_body, "CLIENT_BODY_ATTEMPT_SYMBOL_CHANGED")
        root = Path(AR.__file__).resolve().parents[1]
        names = ("transport.acquisition_resilience", "transport.search_resilience",
                 "transport.http_provider", "transport.clients", "transport.receipt_client",
                 "transport.located_receipts", "client.direct_contacts",
                 "custody.module_store", "discovery.formal_features")
        for name in names:
            path = root/(name.replace(".", "/")+".py")
            pins = [owner._pins[path] for owner in (self.receipt, self.aggregate, self.delta)
                    if owner is not None and path in owner._pins]
            F.need(pins and all(pin == pins[0] for pin in pins),
                   "CLIENT_BODY_ATTEMPT_REQUIRED_SOURCE_PIN:"+name)
            self._required_origins[name] = path
            self._source_pins[path] = deepcopy(pins[0])
        self._active()

    @_async_action
    async def try_acquire_body(self, candidate, digest, *, max_bytes, supplier=None,
                               attempt_timeout_ms=5000):
        """One explicit body attempt; a settled refusal preserves live work."""
        # Import the direct contact guard before checking its source origin.
        from . import direct_contacts
        self._body_attempt_sources()
        provider, resolved = self._candidate(candidate)
        provider = self._selected_supplier(provider if supplier is None else supplier)
        self._charge(C.canonical({"digest": digest, "max_bytes": max_bytes,
            "supplier": provider, "attempt_timeout_ms": attempt_timeout_ms}))
        result = await _try_body(self._acquisition, provider, resolved, digest,
                                max_bytes, attempt_timeout_ms=attempt_timeout_ms)
        self._body_attempt_sources()
        if result["status"] == "UNAVAILABLE_AT_SELECTED_SUPPLIER":
            # This local result came from the selected transport path before
            # body validation/commit; do not classify caught public exceptions.
            return result
        F.need(result["status"] == "BODY_VALIDATED", "CLIENT_BODY_ATTEMPT_RESULT")
        loc, body = resolved["locator"], result["body"]
        # No recoverable catch encloses commit, readback, byte charge or final
        # liveness. These retain the ordinary facade's fail-stop semantics.
        self.workspace.modules.put_body(loc["module_id"], loc["relative_name"], body,
                                        before_commit=self._acquisition._active)
        held = self.workspace.modules.get_body(loc["module_id"], loc["relative_name"],
                                               body["universes"], digest)
        F.need(held == body, "RECEIPT_BODY_COMMIT_READBACK")
        self._acquisition._active()
        self._charge(C.canonical(body))
        return {**result, "status": "BODY_CUSTODIED"}

    @_async_action
    async def acquire(self, candidate, entry, *, bodies=(), expected_exact_journal=None,
                      native_cpu_seconds=30, receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024):
        provider, resolved = self._candidate(candidate); loc = resolved["locator"]
        for value in (native_cpu_seconds, receipt_cpu_seconds, wall_seconds): F.uint(value, 1, 600)
        F.uint(memory_mib, 64, 4096)
        if expected_exact_journal is not None:
            F.need(type(expected_exact_journal) is bytes and len(expected_exact_journal) == 184,
                   "CLIENT_EXPECTED_EXACT_J_BYTES")
            B.member_journal(expected_exact_journal)
        F.fields(entry, ("packet_sha256", "packet_bytes"))
        F.need((provider, loc["module_id"], entry["packet_sha256"], entry["packet_bytes"])
               in self._acquisition._offers, "CLIENT_UNOFFERED_PACKET")
        F.need(type(bodies) in (list, tuple) and len(bodies) <= 16384, "CLIENT_BODY_REQUESTS")
        for item in bodies:
            F.fields(item, ("digest", "max_bytes"))
            result = await self._acquisition.body(provider, resolved, item["digest"], item["max_bytes"])
            self._charge(C.canonical(result["body"]))
        key = entry["packet_sha256"], entry["packet_bytes"], C.canonical(resolved["opening"]["summary"])
        if key in self._packet_cache:
            self._warrant(self._packet_cache[key])
        else:
            await self._acquisition.packet(provider, loc["module_id"], entry)
        demands = [x["digest"] for x in bodies]
        self._acquisition.custody_ready(resolved, entry, demands)
        raw = self._store(self.workspace.packets.get, entry["packet_sha256"], entry["packet_bytes"])
        self._charge(raw)
        token = self._admit_evidence(raw, resolved["opening"]["summary"], expected_exact_journal,
            native_cpu_seconds, receipt_cpu_seconds, min(wall_seconds, self.grant.remaining_seconds()), memory_mib)
        kind, handle, unused, live = self._warrant(token)
        owner = self.aggregate if kind == "A-member" else self.delta
        F.need(kind in ("A-member", "mixed"), "CLIENT_EVIDENCE_WARRANT_KIND")
        owner.open_group(handle, resolved["opening"])
        self._acquisition.custody_ready(resolved, entry, demands)
        unused_kind, unused_handle, unused_raw, final = self._warrant(token)
        F.need(final["journal"] == live["journal"], "CLIENT_EVIDENCE_FINAL_TARGET")
        self._expected(final["journal"], expected_exact_journal)
        return token

    @_action
    def export_evidence(self, warrant):
        kind, unused_handle, raw, live = self._warrant(warrant)
        F.need(kind in ("mixed", "A-member"), "CLIENT_NO_A_FROM_I_WARRANT")
        if kind == "A-member":
            raw = pack_terminal(live["aggregate_header"], live["journal"], live["member_index"],
                live["siblings"], raw, aggregate_image=self._aggregate_image, envelope=self.workspace._envelope,
                terminal_receipt_bytes=self.workspace.config["terminal_receipt_bytes"])
        unused_kind, unused_summary, exact, unused_census = self._inspect(raw)
        F.need(exact == live["journal"], "CLIENT_EXPORTED_EXACT_TARGET")
        self._charge(raw); self._warrant(warrant)
        return raw

    @_action
    def retain_semantics(self, openings, bodies):
        F.need(type(openings) is list and type(bodies) is list
               and len(openings) <= 4096 and len(bodies) <= 8192, "CLIENT_SEMANTIC_RETENTION_LISTS")
        raw = C.canonical({"openings": openings, "bodies": bodies}); self._charge(raw)
        F.need(len(raw) <= self.grant._limits["imports"]["data_bytes"], "CLIENT_SEMANTIC_RETENTION_DATA")
        groups, values = 0, 0
        for item in openings:
            F.fields(item, ("module", "opening")); module, opening = item["module"], item["opening"]
            group = C.verify_group_opening(module, opening)
            self._store(self.workspace.modules.put_group, module, opening, before_commit=self._active)
            for declaration in group["declarations"]:
                held, unused = self._store(self.workspace.modules.get_group, module, declaration["name"], opening["index"])
                F.need(held == opening, "CLIENT_RETAINED_GROUP_READBACK")
            groups += 1
        for response in bodies:
            F.fields(response, ("schema", "module_id", "relative_name", "universes", "body_hash", "expression"))
            module, name = response["module_id"], response["relative_name"]
            self._store(self.workspace.modules.put_body, module, name, response, before_commit=self._active)
            held = self._store(self.workspace.modules.get_body, module, name,
                               response["universes"], response["body_hash"])
            F.need(held == response, "CLIENT_RETAINED_BODY_READBACK"); values += 1
        return {"status": "STRUCTURAL_SEMANTICS_DURABLY_READ_BACK", "groups": groups, "bodies": values,
                "cross_database_atomic": False, "all_future_bodies_covered": False, "mathematical_acceptance": False}

    def _body_present(self, module, universes, digest):
        # Point lookup only; caller routes it through _store for the same
        # activity and store-call accounting as public custody operations.
        return self.workspace.modules.db.execute(
            "SELECT 1 FROM bodies WHERE module=? AND universes=? AND hash=?",
            (module, universes, digest)).fetchone() is not None

    def _publish(self, raw, export_names, retention_policy, reconciles=None):
        kind, summary, exact, census = self._inspect(raw)
        if kind == "mixed": return super()._publish(raw, export_names, retention_policy, reconciles)
        F.need(kind == "terminal", "CLIENT_EVIDENCE_KIND")
        self._charge(raw)
        F.need(retention_policy == {"mode": "quota-bounded-local-custody"}, "CLIENT_RETENTION_POLICY")
        F.need(type(export_names) is list and len(export_names) <= 16384, "CLIENT_EXPORT_NAMES")
        self._charge(C.canonical(export_names)); module = C.summary_id(summary)
        keys = [C.name_key(name) for name in export_names]
        F.need(len(keys) == len(set(keys)), "CLIENT_DUPLICATE_EXPORT")
        # All selected groups are already durable before intent. No detached
        # semantic arrays are silently lost on restart/reconcile.
        groups = {}
        for name in export_names:
            opening, unused = self._store(self.workspace.modules.get_group, module, name)
            F.need(opening["summary"] == summary, "CLIENT_TERMINAL_SELECTED_SUMMARY")
            groups[opening["index"]] = C.canonical(opening)
        identifier = secrets.token_hex(32)
        intent = {"module": module, "packet_sha256": _sha(raw), "packet_bytes": len(raw),
            "export_names": export_names, "retention_policy": retention_policy, "reconciles": reconciles}
        outcome = {"phase": "INTENT", "groups": 0, "bodies": 0, "indexed": 0,
                   "missing_bodies": 0, "mathematical_acceptance": False}
        def save():
            data = C.canonical(outcome)
            F.need(len(data) <= self.workspace.config["max_report_bytes"], "CLIENT_PUBLICATION_REPORT_LIMIT")
            self.workspace.db.execute("UPDATE publications SET outcome=? WHERE id=?", (data, identifier))
        intent_raw = C.canonical(intent)
        F.need(len(intent_raw) <= self.workspace.config["max_report_bytes"], "CLIENT_PUBLICATION_INTENT_LIMIT")
        self.workspace.db.execute("INSERT INTO publications VALUES(?,?,?,?)",
            (identifier, self.grant.identifier, intent_raw, C.canonical(outcome)))
        self._counts["publication_attempts"] += 1; self._publications.append(identifier)
        try:
            self._store(self.workspace.packets.put, module, raw, before_commit=self._active)
            F.need(self._store(self.workspace.packets.get, intent["packet_sha256"], len(raw)) == raw,
                   "CLIENT_PUBLICATION_PACKET_READBACK")
            outcome["phase"] = "PACKET_READ_BACK"; save()
            for index, encoded in sorted(groups.items()):
                opening = C.parse_json(encoded)
                for declaration in opening["group"]["declarations"]:
                    held, unused = self._store(self.workspace.modules.get_group, module, declaration["name"], index)
                    F.need(held == opening, "CLIENT_PUBLICATION_GROUP_READBACK")
                    for digest in sorted(permitted_hashes(declaration)):
                        # Distinguish absent body from any corrupt/invalid body;
                        # do not turn an arbitrary read failure into availability.
                        present = self._store(self._body_present, module, declaration["universes"], digest)
                        if not present:
                            outcome["missing_bodies"] += 1; continue
                        self._store(self.workspace.modules.get_body, module, declaration["name"],
                                    declaration["universes"], digest)
                        outcome["bodies"] += 1
                outcome["groups"] += 1
            outcome["phase"] = "SELECTED_SEMANTICS_READ_BACK"; save()
            for name in export_names:
                opening, unused = self._store(self.workspace.modules.get_group, module, name)
                F.need(opening["summary"] == summary, "CLIENT_TERMINAL_INDEX_SUMMARY")
                export = self.workspace.adapter.encode_opening(module, name, opening)
                self._store(self.workspace.index.admit, export, expected_id=C.export_id(module, name))
                outcome["indexed"] += 1; save()
            outcome.update(phase="LOCALLY_PUBLISHED", cross_database_atomic=False,
                remote_placement_confirmed=False, all_future_bodies_covered=False,
                packet_census=census, snapshot_id=self.workspace.index.status()["latest"])
            self._active(); save()
            return {"publication_id": identifier, "intent": intent, **deepcopy(outcome)}
        except Exception as error:
            outcome.update(status="PARTIAL_PUBLICATION", failure=type(error).__name__+":"+str(error)[:500])
            try: save()
            except BaseException: pass
            raise PartialPublicationError(identifier, outcome) from error

    def report(self):
        return {**super().report(), "schema": REPORT_SCHEMA,
                "evidence_forms": ["mixed", "terminal"],
                "terminal_receipt_bytes": self.workspace.config["terminal_receipt_bytes"]}

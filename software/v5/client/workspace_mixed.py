"""Concrete A-capable commons client over unchanged mixed admission machinery.

A is required; I is optional. The trusted caller reserves one finite grant before
constructing exact owners inside its enclosing Job. Saved data is not authority.
This module never constructs issuers, produces proofs or migrates I-only stores.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
import os
from pathlib import Path
import sqlite3
import sys
import time

from admission.verifier import ReceiptVerifier
from aggregate_claims.aggregate_admission import AggregateReceiptVerifier
from aggregate_claims import bindings as B
from custody.module_store import ModuleStore
from discovery import formal_features as F
from discovery.discovery_store import Store, ordinary
from discovery.module_export_adapter import ModuleExportAdapter
from mixed_claims.authoring_atomic import MixedOwnerPreparation
from mixed_claims.imports_atomic import MixedImportSession
from mixed_claims.packet import Envelope, parse_packet
from mixed_claims.receiver import MixedDeltaVerifier
from mixed_network.custody import PacketStore, public_profile, profile_id
from mixed_network.transport import MixedAcquisition, MixedLocatedHandoff
from modules import codec as C
from transport.receipt_client import AcquisitionBudget
from . import workspace_atomic as A
from .workspace_atomic import (
    OperationGrant, LiveWarrant, AuthorContext, Candidate, PartialPublicationError,
    LIMITS, IMPORT_LIMITS, _sha, _copy, _under, _action, _async_action)

MIB = 1024**2
SCHEMA = "DMKN_V5_CLIENT_MIXED_WORKSPACE_V1"
REPORT_SCHEMA = "DMKN_V5_CLIENT_MIXED_REPORT_V1"


def _encoded_fact(fact):
    """Known inert comparison fields only; original issuer bytes stay untouched."""
    result = dict(fact)
    for key in ("journal", "header", "aggregate_header"):
        if key in result: result[key] = list(result[key])
    if "siblings" in result: result["siblings"] = [list(part) for part in result["siblings"]]
    return _copy(result)


class Workspace(A.Workspace):
    """New schema and exact mixed custody; no in-place I-only migration."""
    @classmethod
    def open(cls, root, config, create=False):
        F.need(os.name == "nt", "CLIENT_WINDOWS_OWNER_REQUIRED")
        F.fields(config, ("schema", "wire_profile", "module_limits", "packet_limits", "index_limits",
                          "packet_envelope", "max_operations", "max_report_bytes", "ledger_pages"))
        F.need(config["schema"] == SCHEMA, "CLIENT_MIXED_WORKSPACE_SCHEMA")
        profile_id(config["wire_profile"])
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
                                       envelope=envelope, create=create)
            self.index = Store(self.root/"index", self.adapter, config["index_limits"], create=create)
            self.db.execute("UPDATE operations SET status='INTERRUPTED_WITH_UNCERTAIN_TAIL' "
                            "WHERE status IN ('GRANTED','OPEN','FAILED_PENDING_CLOSE')")
            return self
        except BaseException:
            self._release(); raise

    def operation(self, grant, *, aggregate_owner, delta_owner, receipt_owner=None,
                  preparation_owner=None, foundation_bytes, foundation_sha256):
        """Transfer exact owners on SUCCESS only; caller cleans construction failure."""
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


class CommonsClient(A.CommonsClient):
    """Closed A-only or I+A configuration, not a verifier/plugin registry."""
    def __init__(self, workspace, grant, receipt, aggregate, delta, preparation, foundation, foundation_sha):
        F.need(type(aggregate) is AggregateReceiptVerifier and type(delta) is MixedDeltaVerifier
               and (receipt is None or type(receipt) is ReceiptVerifier), "CLIENT_MIXED_EXACT_REAL_OWNERS")
        F.need(preparation is None or type(preparation) is MixedOwnerPreparation,
               "CLIENT_EXACT_PREPARATION_OWNER")
        image = workspace.config["wire_profile"]["aggregate_image"]
        F.need(type(workspace.packets) is PacketStore
               and profile_id(workspace.config["wire_profile"]) == workspace.packets.profile_id
               and workspace.packets.profile == public_profile(image), "CLIENT_MIXED_CUSTODY_PROFILE")
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
        names = ("client", "client.workspace_atomic", "client.workspace_mixed",
                 "mixed_network", "mixed_network.custody", "mixed_network.transport")
        self._required_origins = {name: root/(name.replace(".", "/")+
            ("/__init__.py" if "." not in name else ".py")) for name in names}
        pins = {path: pin for owner in (receipt, aggregate, delta) if owner is not None
                for path, pin in owner._pins.items()}
        F.need(set(self._required_origins.values()) <= set(pins), "CLIENT_MIXED_REQUIRED_SOURCE_PINS")
        self._source_pins = {path: deepcopy(pins[path]) for path in self._required_origins.values()}
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
        self.workspace._active(); self.workspace._grant_active(self.grant)
        F.need(not self._closed and self._state == "OPEN" and time.monotonic() < self.grant.deadline,
               "CLIENT_CLOSED_FAILED_OR_EXPIRED")
        F.need(time.process_time()-self.grant._cpu <= self.grant._limits["controller_cpu_seconds"],
               "CLIENT_CONTROLLER_CPU_LIMIT")
        owners = self.receipt, self.aggregate, self.delta, self.preparation
        F.need(all(owner is original for owner, original in zip(owners, self._origin_owners))
               and len(self.delta._owners) == 2 and self.delta._owners[0] is self.receipt
               and self.delta._owners[1] is self.aggregate
               and self.delta._aggregate_image == self.aggregate._image == self._aggregate_image
               == self.workspace.config["wire_profile"]["aggregate_image"], "CLIENT_MIXED_ORIGIN_CHANGED")
        for owner, expected in zip(owners[:3], self._profiles):
            F.need((None if owner is None else owner.report()["profile_id"]) == expected,
                   "CLIENT_ISSUER_PROFILE_CHANGED")
            if owner is not None: owner._active()
        for name, path in self._required_origins.items():
            loaded = sys.modules.get(name)
            F.need(loaded is not None and type(getattr(loaded, "__file__", None)) is str
                   and Path(loaded.__file__).resolve() == path, "CLIENT_MIXED_LOADED_SOURCE_ORIGIN")
            held = [owner._pins[path] for owner in owners[:3] if owner is not None and path in owner._pins]
            F.need(held and all(pin == self._source_pins[path] for pin in held), "CLIENT_MIXED_SOURCE_PIN_CHANGED")
        F.need(A is sys.modules["client.workspace_atomic"]
               and MixedLocatedHandoff is A.FrontierLocatedHandoff,
               "CLIENT_MIXED_INHERITED_SOURCE_OR_HANDOFF_CHANGED")
        self._budget.active()

    def _fail(self, error):
        self._state = "FAILED"; self._failures.append(type(error).__name__+":"+str(error)[:1000])
        self._warrants.clear(); self._receipt_cache.clear(); self._packet_cache.clear(); self._aggregate_cache.clear()
        self._candidates.clear(); self._context = self._selection_view = None
        self._budget.closed = True
        # Attribute substitution must not strand a transferred original issuer,
        # or authorize cleanup of the untransferred replacement.
        for owner in (self._session, *reversed(self._origin_owners)):
            if owner is not None:
                try: owner.close()
                except BaseException as cleanup:
                    self._cleanup_uncertain = True; self.workspace._poisoned = True
                    self._failures.append("cleanup:"+type(cleanup).__name__)
        try: self.workspace._record(self.grant.identifier, "FAILED_PENDING_CLOSE", self.report())
        except BaseException: self._failures.append("failure_report_not_persisted")

    def _live_fact(self, kind, handle):
        if kind == "I":
            F.need(self.receipt is not None, "CLIENT_I_OWNER_NOT_SELECTED")
            return self.receipt.describe(handle)
        if kind == "A-member": return self.aggregate.describe_member(handle)
        F.need(kind == "mixed", "CLIENT_WARRANT_KIND")
        return self.delta.describe(handle)

    def _issue(self, kind, handle, raw):
        live = self._live_fact(kind, handle)
        self._bind_fact(kind, raw, live)
        token = LiveWarrant(); self._warrants[token] = kind, handle, raw, _encoded_fact(live)
        return token

    def _bind_fact(self, kind, raw, live):
        F.need(_sha(raw) == live["packet_sha256" if kind == "mixed" else "receipt_sha256"],
               "CLIENT_EVIDENCE_CHANGED")
        slot = {"I": 0, "A-member": 1, "mixed": 2}[kind]
        F.need(live["profile_id"] == self._profiles[slot], "CLIENT_WARRANT_PROFILE")
        if kind == "A-member":
            F.need(live["aggregate_image"] == self._aggregate_image and live["receipt_bytes"] == len(raw),
                   "CLIENT_AGGREGATE_MEMBER_BINDING")

    def _warrant(self, token):
        F.need(type(token) is LiveWarrant and token in self._warrants, "CLIENT_FOREIGN_WARRANT")
        kind, handle, raw, expected = self._warrants[token]
        live = self._live_fact(kind, handle)
        F.need(_encoded_fact(live) == expected, "CLIENT_EXACT_WARRANT_CHANGED")
        self._bind_fact(kind, raw, live)
        return kind, handle, raw, live

    @_action
    def describe(self, token):
        kind, handle, unused_raw, live = self._warrant(token)
        members = self.delta.members(handle) if kind == "mixed" else [live]
        return {"kind": kind, "live": live, "members": members,
                "authority": "SAME_CLIENT_LIVE_REFERENCE_NOT_TRANSFERABLE_REPORT"}

    @_action
    def admit_receipt(self, receipt, expected_summary, *, cpu_seconds=30, wall_seconds=60, memory_mib=1024):
        F.need(self.receipt is not None, "CLIENT_I_OWNER_NOT_SELECTED")
        return A.CommonsClient.admit_receipt.__wrapped__(self, receipt, expected_summary,
            cpu_seconds=cpu_seconds, wall_seconds=wall_seconds, memory_mib=memory_mib)

    def _aggregate_fact(self, handle, receipt, header):
        live = self.aggregate.describe_aggregate(handle)
        F.need(live["header"] == header and live["receipt_sha256"] == _sha(receipt)
               and live["receipt_bytes"] == len(receipt) and live["profile_id"] == self._profiles[1],
               "CLIENT_EXACT_AGGREGATE_RECEIPT")
        return _encoded_fact(live)

    @_action
    def admit_aggregate_member(self, receipt_bytes, expected_header, exact_journal, index, siblings,
                               *, cpu_seconds=30, wall_seconds=60, memory_mib=1024):
        F.need(type(receipt_bytes) is bytes and 0 < len(receipt_bytes) <= 64*MIB
               and type(expected_header) is bytes and len(expected_header) == B.HEADER_BYTES
               and type(exact_journal) is bytes and len(exact_journal) == 184
               and type(siblings) is list and len(siblings) <= B.MAX_SIBLINGS
               and all(type(part) is bytes and len(part) == 32 for part in siblings),
               "CLIENT_AGGREGATE_MEMBER_INPUT")
        self._charge(receipt_bytes); self._charge(expected_header); self._charge(exact_journal)
        for part in siblings: self._charge(part)
        F.uint(index, 0, B.MAX_MEMBERS-1); self._charge(C.canonical(index))
        F.uint(cpu_seconds, 1, 600); F.uint(wall_seconds, 1, 600); F.uint(memory_mib, 64, 4096)
        B.bind_member(expected_header, exact_journal, index, siblings, adopted_image=self._aggregate_image)
        key = (self._aggregate_image, self._profiles[1], _sha(receipt_bytes), len(receipt_bytes), expected_header)
        if key in self._aggregate_cache:
            handle, expected = self._aggregate_cache[key]
            F.need(self._aggregate_fact(handle, receipt_bytes, expected_header) == expected,
                   "CLIENT_AGGREGATE_CACHE_CHANGED")
            self._counts["same_live_hits"] += 1
        else:
            self._budget.verification(len(receipt_bytes), cpu_seconds)
            self._counts["admission_submissions"] += 1
            output = self.grant.directory/("aggregate-"+str(self._counts["admission_submissions"]))
            handle = self.aggregate.receive(receipt_bytes, expected_header, output,
                cpu_seconds=cpu_seconds, wall_seconds=min(wall_seconds, self.grant.remaining_seconds()),
                memory_mib=memory_mib)
            self._aggregate_cache[key] = handle, self._aggregate_fact(handle, receipt_bytes, expected_header)
        # Membership remains exact and charged even on a receipt-cache hit.
        member = self.aggregate.select_member(handle, exact_journal, index, siblings)
        return self._issue("A-member", member, receipt_bytes)

    def _admit_packet(self, raw, summary, native_cpu_seconds, receipt_cpu_seconds, wall_seconds, memory_mib):
        key = (_sha(raw), len(raw), C.canonical(summary))
        if key in self._packet_cache:
            token = self._packet_cache[key]; self._warrant(token)
            self._counts["same_live_hits"] += 1; return token
        unused, unused2, witnesses, census = parse_packet(raw, self.workspace._envelope,
                                                         aggregate_image=self._aggregate_image)
        F.need(witnesses[-1][2] == summary, "CLIENT_PACKET_TARGET_SUMMARY")
        reserved = census["claims"]*receipt_cpu_seconds+census["deltas"]*native_cpu_seconds
        self._budget.verification(len(raw), reserved); self._counts["admission_submissions"] += 1
        handle = self.delta.receive(raw, summary, native_cpu_seconds=native_cpu_seconds,
            receipt_cpu_seconds=receipt_cpu_seconds, wall_seconds=min(wall_seconds, self.grant.remaining_seconds()),
            memory_mib=memory_mib)
        token = self._issue("mixed", handle, raw); self._packet_cache[key] = token
        return token

    @_async_action
    async def resolve(self, provider, record):
        F.need(self._search is not None, "CLIENT_SEARCH_NOT_READY")
        self._charge(C.canonical(record))
        if self._acquisition is None:
            self._acquisition = MixedAcquisition.from_search(self._handoff,
                public_profile(self._aggregate_image), self.workspace.modules, self.workspace.packets,
                verifier=self.delta)
        resolved = await self._acquisition.export(provider, record)
        candidate = Candidate(); self._candidates[candidate] = provider, _copy(resolved)
        return candidate

    def _context_data(self, warrants, selected, openings, bodies):
        F.need(type(warrants) is list and type(selected) is list and type(openings) is list
               and type(bodies) is list, "CLIENT_CONTEXT_LISTS")
        F.need(all(type(exact) is bytes for exact in selected), "CLIENT_CONTEXT_EXACT_J_BYTES")
        batch = C.canonical({"selected": [list(exact) for exact in selected], "openings": openings, "bodies": bodies})
        self._charge(batch)
        for row in warrants:
            F.fields(row, ("warrant", "resolutions"))
            kind, handle, raw, unused = self._warrant(row["warrant"]); self._charge(raw)
            if row["resolutions"] is not None:
                self._charge(C.canonical([[list(exact), choice] for exact, choice in row["resolutions"].items()]))
            if kind == "I": self._session.use_legacy_handle(handle, raw, resolutions=row["resolutions"])
            elif kind == "A-member": self._session.use_aggregate_member(handle, raw, resolutions=row["resolutions"])
            else: self._session.use_delta_handle(handle, resolutions=row["resolutions"])
        ready, view = self._session.materialize(batch, self._foundation, self._foundation_sha)
        context = AuthorContext(); self._context = context, ready["selection_binding"]
        self._selection_view = view
        return {"context": context, "status": ready["status"], "demands": ready.get("demands", []),
                "cost": ready["cost"], "mathematical_acceptance": False}

    @_action
    def import_context(self, warrants, selected, openings, bodies):
        F.need(self._session is None, "CLIENT_IMPORT_SESSION_ALREADY_CREATED")
        self._session = MixedImportSession(legacy_verifier=self.receipt, aggregate_verifier=self.aggregate,
            delta_verifier=self.delta, **self.grant._limits["imports"], wall_seconds=self.grant.remaining_seconds())
        self._counts["new_import_sessions"] += 1
        return self._context_data(warrants, selected, openings, bodies)

    def _semantic_plan(self, raw):
        unused, unused2, witnesses, census = parse_packet(raw, self.workspace._envelope,
                                                         aggregate_image=self._aggregate_image)
        groups, values = {}, {}
        def group(module, opening):
            C.verify_group_opening(module, opening); key = module, opening["index"]
            encoded = C.canonical(opening)
            F.need(key not in groups or groups[key] == encoded, "CLIENT_SEMANTIC_GROUP_CONFLICT")
            groups[key] = encoded
        for witness_raw, unused_parents, unused_summary, unused_rank in witnesses:
            witness = C.parse_json(witness_raw); spec = witness["local_spec"]; module = C.module_id(spec)
            for index in range(len(spec["groups"])): group(module, C.group_opening(spec, index))
            for parent in witness["parents"]:
                owner = B.member_journal(bytes(parent["journal"]))["module"]
                for opening in parent["openings"]: group(owner, opening)
            for body in witness["bodies"]:
                key = body["universes"], body["digest"]; encoded = C.canonical(body["expression"])
                F.need(C.body_id(body["expression"], body["universes"]) == body["digest"]
                       and (key not in values or values[key] == encoded), "CLIENT_SEMANTIC_BODY_CONFLICT")
                values[key] = encoded
        return witnesses[-1][2], groups, values, census

    @_action
    def semantic_material(self, token):
        F.need(type(token) is LiveWarrant and token in self._warrants, "CLIENT_FOREIGN_WARRANT")
        if self._warrants[token][0] == "A-member":
            unused_kind, unused_handle, unused_raw, live = self._warrant(token)
            return {"status": "NEED_CALLER_OR_PROVIDER_SEMANTICS", "module": live["module"],
                    "openings": [], "bodies": [], "mathematical_acceptance": False}
        return A.CommonsClient.semantic_material.__wrapped__(self, token)

    def report(self):
        receipt, aggregate, delta, preparation = self._origin_owners
        return {"schema": REPORT_SCHEMA, "operation_id": self.grant.identifier,
            "status": self._state, "closed": self._closed, "wire_profile_id": self.workspace.packets.profile_id,
            "aggregate_image": self._aggregate_image, "owner_profiles": list(self._profiles),
            "grant": self.grant.limits, "calls": self._calls, "submitted_input_bytes": self._input_bytes,
            "counts": dict(self._counts),
            "input_byte_scope": "SUBMITTED_OR_RELOADED_EVIDENCE_FOUNDATION_SOURCE_QUERY_CONTEXT_AND_SELECTIONS;"
                                "DIRECT_A_RECEIPT_HEADER_JOURNAL_INDEX_PATH_INCLUDED;REPEATS_CHARGED;"
                                "NOT_PHYSICAL_TRANSFER_BYTES;OTHER_CONTROL_METADATA_EXCLUDED",
            "observed_controller_cpu_since_grant": time.process_time()-self.grant._cpu,
            "wall_since_grant": time.monotonic()-self.grant.started, "acquisition": self._budget.report(),
            "receipt": None if receipt is None else receipt.report(),
            "aggregate": aggregate.report(), "mixed": delta.report(),
            "preparation": None if preparation is None else preparation.report(),
            "search": None if self._search is None else self._search.report(),
            "location": None if self._handoff is None else self._handoff.location.report(),
            "transport": None if self._acquisition is None else self._acquisition.report(),
            "publications": list(self._publications), "failures": list(self._failures),
            "cleanup_uncertain": self._cleanup_uncertain,
            "cost_scope": "CONTROLLER_INCLUSIVE_SINCE_GRANT;NESTED_WORKERS_NOT_ADDITIVE_TOTAL",
            "unknowns": ["enclosing_Job_total_supplied_by_caller", "failed_worker_cost_may_be_unknown",
                         "final_report_and_exit_tail", "provider_costs", "DHT_wire_bytes"],
            "hard_containment": "TRUSTED_CALLER_ACTUAL_ENCLOSING_JOB_REQUIRED", "mathematical_acceptance": False}

    async def close(self):
        if self._closed: return self.report()
        F.need(not self._busy, "CLIENT_CANCEL_AND_AWAIT_ACTIVE_CALL_BEFORE_CLOSE")
        errors = []; self._budget.closed = True
        if self._acquisition is not None:
            try: self._acquisition.close()
            except BaseException as error: errors.append(type(error).__name__+":"+str(error)[:300])
        # The mixed verifier does not own its independent I/A issuers. Close
        # every transferred owner even if acquisition cleanup already failed.
        for owner in (self._session, *reversed(self._origin_owners)):
            if owner is not None:
                try: owner.close()
                except BaseException as error: errors.append(type(error).__name__+":"+str(error)[:300])
        if self._channel is not None:
            try: await self._channel.close()
            except BaseException as error: errors.append(type(error).__name__+":"+str(error)[:300])
        self._warrants.clear(); self._candidates.clear(); self._context = self._selection_view = None
        self._receipt_cache.clear(); self._packet_cache.clear(); self._aggregate_cache.clear()
        if errors: self._failures.extend(errors); self._cleanup_uncertain = True
        if self._cleanup_uncertain: self._state = "CLEANUP_INCOMPLETE"
        elif self._state == "OPEN": self._state = "CLOSED"
        self._closed = True
        try:
            report = self.report(); self.workspace._record(self.grant.identifier, self._state, report)
            return report
        except BaseException:
            self._failures.append("final_report_not_persisted"); self._state = "CLOSED_REPORT_UNCERTAIN"
            self.workspace._poisoned = True
            raise
        finally:
            if self._cleanup_uncertain: self.workspace._poisoned = True
            self.workspace._client = None; self.workspace._grants.pop(self.grant, None)

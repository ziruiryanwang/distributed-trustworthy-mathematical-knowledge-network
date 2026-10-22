"""One finite ordinary client for mixed extensions or exact certified targets.

New closed custody profile; frozen mixed/atomic clients remain unchanged. Only
actual I/A/mixed issuers grant authority. Structural custody and publication do
not. This is trusted-owner Windows software, not a hostile-source sandbox.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
from functools import wraps
import os
from pathlib import Path
import secrets
import sqlite3
from placement import storage_profile as SP, storage_paths as SF
import sys
import time

from admission.verifier import ReceiptVerifier
from aggregate_claims.aggregate_admission import AggregateReceiptVerifier
from aggregate_claims import bindings as B
from custody.module_store import ModuleStore, permitted_hashes
from discovery import formal_features as F
from discovery.discovery_store import Store, ordinary
from discovery.module_export_adapter import (
    ModuleExportAdapter, validate_pair_profile, validate_type_pattern_profile,
    validate_fingerprint_profile)
from evidence_network.packet import (
    inspect_evidence, parse_terminal, pack_terminal, parse_terminal_i, pack_terminal_i)
from evidence_network.custody import PacketStore, public_profile, profile_id, PROFILE_SCHEMA_V2
from evidence_network.transport import EvidenceAcquisition
from mixed_claims.authoring_atomic import MixedOwnerPreparation
from mixed_claims.imports_atomic import MixedImportSession
from mixed_claims.packet import Envelope
from mixed_claims.receiver import MixedDeltaVerifier
from modules import codec as C
from transport.receipt_client import AcquisitionBudget
from transport import acquisition_resilience as AR
from transport.acquisition_resilience import try_body as _try_body
from transport.acquisition_resilience import try_body_from as _try_body_from
from transport import declaration_resilience as DR
from transport.declaration_resilience import try_declaration as _try_declaration
from . import workspace_mixed as M
from . import body_custody as BC
from .body_custody import reserve as _reserve_body_location, _BodyPool
from .workspace_atomic import (
    OperationGrant, LiveWarrant, AuthorContext, Candidate, PartialPublicationError,
    _sha, _copy, _under, _action, _async_action)

MIB = 1024**2
SCHEMA = "DMKN_V5_CLIENT_EVIDENCE_WORKSPACE_V1"
CONJUNCTION_SCHEMA = "DMKN_V5_CLIENT_EVIDENCE_CONJUNCTION_WORKSPACE_V1"
TYPE_PATTERN_SCHEMA = "DMKN_V5_CLIENT_EVIDENCE_TYPE_PATTERN_WORKSPACE_V1"
CONCLUSION_FINGERPRINT_SCHEMA = "DMKN_V5_CLIENT_EVIDENCE_CONCLUSION_FINGERPRINT_WORKSPACE_V1"
REPORT_SCHEMA = "DMKN_V5_CLIENT_EVIDENCE_REPORT_V1"


def _terminal_final(self):
    """Do not expose a trial result until post-census authority checks finish."""
    self._active(); self._census(); self._active()
    # Active/census checks can perform blocking I/O. These last observations
    # are nonblocking and retain every original deadline, never a fresh one.
    now = time.monotonic()
    F.need(now < self.grant.deadline and all(owner is None or now < owner._deadline
               for owner in self._origin_owners), "CLIENT_TERMINAL_TRIAL_DEADLINE")
    F.need(time.process_time()-self.grant._cpu <= self.grant._limits["controller_cpu_seconds"],
           "CLIENT_CONTROLLER_CPU_LIMIT")


def _terminal_action(method):
    @wraps(method)
    def call(self, *args, **kwargs):
        self._enter()
        try:
            result = method(self, *args, **kwargs)
            _terminal_final(self)
            return result
        except BaseException as error:
            self._fail(error); raise
        finally: self._busy = False
    return call


def _async_terminal_action(method):
    @wraps(method)
    async def call(self, *args, **kwargs):
        self._enter()
        try:
            result = await method(self, *args, **kwargs)
            _terminal_final(self)
            return result
        except BaseException as error:
            self._fail(error); raise
        finally: self._busy = False
    return call


class Workspace(M.Workspace):
    """Fresh profile-selected store; no old-workspace migration or proxy store."""
    @classmethod
    def open(cls, root, config, create=False):
        F.need(os.name == "nt", "CLIENT_WINDOWS_OWNER_REQUIRED")
        F.need(type(config) is dict, "CLIENT_EVIDENCE_WORKSPACE_CONFIG")
        fields = ("schema", "wire_profile", "module_limits", "packet_limits", "index_limits",
            "packet_envelope", "terminal_receipt_bytes", "max_operations", "max_report_bytes", "ledger_pages")
        if config.get("schema") == CONCLUSION_FINGERPRINT_SCHEMA:
            F.fields(config, (*fields, "discovery_profile"))
            # Explicit positional profile, isolated from both predecessor modes.
            # Validate before filesystem mutation; immutable config binds reopen.
            discovery_profile = validate_fingerprint_profile(config["discovery_profile"])
        elif config.get("schema") == TYPE_PATTERN_SCHEMA:
            F.fields(config, (*fields, "discovery_profile"))
            # A fixed pattern-only profile is distinct from the old pair mode.
            # Refuse crossed or malformed profiles before any filesystem mutation.
            discovery_profile = validate_type_pattern_profile(config["discovery_profile"])
        elif config.get("schema") == CONJUNCTION_SCHEMA:
            F.fields(config, (*fields, "discovery_profile"))
            # Validate before creating a directory, lock, ledger or index. The
            # explicit profile is persisted with the immutable whole config.
            discovery_profile = validate_pair_profile(config["discovery_profile"])
        else:
            F.fields(config, fields)
            F.need(config["schema"] == SCHEMA, "CLIENT_EVIDENCE_WORKSPACE_SCHEMA")
            discovery_profile = None
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
            SF.preopen_lock(lock, create=create)
            self._lock = lock.open("a+b")
            if lock.stat().st_size == 0:
                self._lock.write(b"\0"); self._lock.flush(); os.fsync(self._lock.fileno())
            self._lock.seek(0); msvcrt.locking(self._lock.fileno(), msvcrt.LK_NBLCK, 1)
            ledger = ordinary(self.root/"workspace.sqlite", fresh=create, directory=False)
            SF.preopen_database(ledger, max_pages=config["ledger_pages"], create=create)
            self.db = sqlite3.connect(ledger, timeout=1, isolation_level=None)
            SP.configure_connection(self.db, max_pages=config["ledger_pages"])
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
            self.adapter = ModuleExportAdapter(C, B.FOUNDATION, B.POLICY,
                                               discovery_profile=discovery_profile)
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
        return {**super().status(), "schema": self.config["schema"]}


class CommonsClient(M.CommonsClient):
    """Closed evidence specialization; same original I/A/delta owner lifetime."""
    def __init__(self, workspace, grant, receipt, aggregate, delta, preparation, foundation, foundation_sha):
        # Frozen predecessor's exact owner/suballocation contract, specialized
        # only at its lexical custody/profile and required source-origin seams.
        F.need(type(aggregate) is AggregateReceiptVerifier and type(delta) is MixedDeltaVerifier
               and (receipt is None or type(receipt) is ReceiptVerifier), "CLIENT_MIXED_EXACT_REAL_OWNERS")
        F.need(preparation is None or type(preparation) is MixedOwnerPreparation,
               "CLIENT_EXACT_PREPARATION_OWNER")
        image = workspace.config["wire_profile"]["aggregate_image"]
        selected_profile = profile_id(workspace.config["wire_profile"])
        F.need(type(workspace.packets) is PacketStore
               and selected_profile == workspace.packets.profile_id
               and workspace.packets.profile == workspace.config["wire_profile"],
               "CLIENT_EVIDENCE_CUSTODY_PROFILE")
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
        self._wire_profile_id = selected_profile
        self._profiles = None if receipt is None else receipt.report()["profile_id"], ar["profile_id"], dr["profile_id"]
        root = Path(__file__).resolve().parents[1]
        names = ("client", "client.workspace_atomic", "client.workspace_mixed", "client.workspace_evidence",
            "mixed_network", "mixed_network.custody", "mixed_network.transport",
            "evidence_network", "evidence_network.packet", "evidence_network.custody", "evidence_network.transport",
            "mixed_claims.interface_projection")
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
        self._definition_mode = self._origin_definition_mode = "eager"
        self._channel = self._handoff = self._search = self._acquisition = None
        self._query_used = False
        self._body_pool = self._origin_body_pool = None
        self._budget = AcquisitionBudget(grant.deadline, acquisition)
        self._failures, self._publications = [], []
        self._counts = {key: 0 for key in ("admission_submissions", "same_live_hits", "author_calls",
            "store_calls", "publication_attempts", "new_import_sessions")}
        self._active(); self._census()

    def _active(self):
        super()._active()
        F.need(self._body_pool is self._origin_body_pool
               and (self._body_pool is None or type(self._body_pool) is _BodyPool),
               "CLIENT_BODY_POOL_ORIGIN_CHANGED")
        F.need(self._definition_mode == self._origin_definition_mode,
               "CLIENT_DEFINITION_MODE_CHANGED")
        stores = self.workspace.modules, self.workspace.packets, self.workspace.index
        F.need(all(a is b for a, b in zip(stores, self._origin_stores)), "CLIENT_EVIDENCE_STORE_CHANGED")
        F.need(type(self.workspace.packets) is PacketStore
               and self.workspace.packets.profile == self.workspace.config["wire_profile"]
               and self.workspace.packets.profile_id == self._wire_profile_id
               == profile_id(self.workspace.config["wire_profile"])
               and asdict(self.workspace.packets.envelope) == asdict(self.workspace._envelope)
               and self.workspace.packets.terminal_receipt_bytes == self.workspace.config["terminal_receipt_bytes"],
               "CLIENT_EVIDENCE_STORE_PROFILE_CHANGED")
        F.need(M is sys.modules["client.workspace_mixed"]
               and inspect_evidence is sys.modules["evidence_network.packet"].inspect_evidence
               and parse_terminal is sys.modules["evidence_network.packet"].parse_terminal
               and pack_terminal is sys.modules["evidence_network.packet"].pack_terminal
               and parse_terminal_i is sys.modules["evidence_network.packet"].parse_terminal_i
               and pack_terminal_i is sys.modules["evidence_network.packet"].pack_terminal_i
               and PROFILE_SCHEMA_V2 == sys.modules["evidence_network.custody"].PROFILE_SCHEMA_V2
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

    def _fail(self, error):
        # Revoke original capabilities even if a public attribute was replaced.
        try:
            if self._origin_body_pool is not None: self._origin_body_pool.close()
        except BaseException as cleanup:
            self._failures.append("body_cleanup:"+type(cleanup).__name__)
        super()._fail(error)

    async def close(self):
        F.need(not self._busy, "CLIENT_CANCEL_AND_AWAIT_ACTIVE_CALL_BEFORE_CLOSE")
        if not self._closed and self._origin_body_pool is not None:
            try: self._origin_body_pool.close()
            except BaseException as cleanup:
                self._failures.append("body_cleanup:"+type(cleanup).__name__)
                self._cleanup_uncertain = True
                self.workspace._poisoned = True
        return await super().close()

    def _body_location_sources(self):
        # Bind only sources selected by the original mathematical owners.
        from . import semantic_reader, located_queries
        self._body_attempt_sources()
        F.need(BC is sys.modules["client.body_custody"]
               and _reserve_body_location is BC.reserve and _BodyPool is BC._BodyPool
               and _try_body_from is AR.try_body_from, "CLIENT_BODY_LOCATION_SYMBOL_CHANGED")
        root = Path(__file__).resolve().parents[1]
        for name in ("client.body_custody", "client.semantic_reader", "client.located_queries"):
            path = root/(name.replace(".", "/")+".py")
            pins = [owner._pins[path] for owner in (self.receipt, self.aggregate, self.delta)
                    if owner is not None and path in owner._pins]
            F.need(pins and all(pin == pins[0] for pin in pins),
                   "CLIENT_BODY_LOCATION_REQUIRED_SOURCE_PIN:"+name)
            self._required_origins[name] = path
            self._source_pins[path] = deepcopy(pins[0])
        self._active()

    @_action
    def reserve_body_location(self, limits):
        """Prepay optional exact-body location before the first located query."""
        self._body_location_sources()
        self._charge(C.canonical(limits))
        pool = _reserve_body_location(self, limits)
        self._body_pool = self._origin_body_pool = pool
        return pool.report()

    @_async_action
    async def _locate_body(self, reader, demand, *, event_cap, peer_cap,
                           descriptor_requests, max_age_ms=10000):
        self._body_location_sources()
        F.need(self._body_pool is not None, "CLIENT_BODY_LOCATION_NOT_RESERVED")
        self._charge(C.canonical({"demand": demand, "event_cap": event_cap,
            "peer_cap": peer_cap, "descriptor_requests": descriptor_requests,
            "max_age_ms": max_age_ms}))
        result = await self._body_pool.locate(reader, demand, event_cap=event_cap,
            peer_cap=peer_cap, descriptor_requests=descriptor_requests, max_age_ms=max_age_ms)
        self._body_location_sources()
        return result

    @_async_action
    async def _try_acquire_body_from(self, reader, demand, capability, *, max_bytes,
                                      attempt_timeout_ms=5000):
        """Consume one exact demand capability; custody failures stay fatal."""
        self._body_location_sources()
        F.need(self._body_pool is not None, "CLIENT_BODY_LOCATION_NOT_RESERVED")
        F.uint(max_bytes, 1, 16*MIB, "CLIENT_BODY_ATTEMPT_BYTES")
        F.uint(attempt_timeout_ms, 1, 60000, "CLIENT_BODY_ATTEMPT_TIMEOUT")
        self._charge(C.canonical({"demand": demand, "max_bytes": max_bytes,
                                  "attempt_timeout_ms": attempt_timeout_ms}))
        attempt = self._body_pool.begin_attempt(reader, demand, capability)
        try:
            result = await _try_body_from(attempt, max_bytes,
                                          attempt_timeout_ms=attempt_timeout_ms)
            self._body_location_sources()
            if result["status"] == "UNAVAILABLE_AT_SELECTED_SUPPLIER":
                return {**result, "route_key": attempt.route_key, "demand": _copy(demand)}
            F.need(result["status"] == "BODY_VALIDATED", "CLIENT_BODY_ATTEMPT_RESULT")
            loc, body = attempt.resolved["locator"], result["body"]
            # Outside every recoverable transport catch: partial custody cannot
            # be presented as an ordinary miss or a retryable token.
            self.workspace.modules.put_body(loc["module_id"], loc["relative_name"], body,
                                            before_commit=self._acquisition._active)
            held = self.workspace.modules.get_body(loc["module_id"], loc["relative_name"],
                                                   body["universes"], attempt.digest)
            F.need(held == body, "RECEIPT_BODY_COMMIT_READBACK")
            self._acquisition._active()
            self._charge(C.canonical(body))
            return {**result, "status": "BODY_CUSTODIED"}
        finally:
            attempt.finish()

    def _context_data(self, warrants, selected, openings, bodies):
        """Continue using the original explicit interface policy and grant."""
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
        ready, view = self._session.materialize(batch, self._foundation, self._foundation_sha,
                                               definition_mode=self._definition_mode)
        context = AuthorContext(); self._context = context, ready["selection_binding"]
        self._selection_view = view
        return {"context": context, "status": ready["status"], "demands": ready.get("demands", []),
                "cost": ready["cost"], "mathematical_acceptance": False}

    @_action
    def import_context(self, warrants, selected, openings, bodies, *, definition_mode="eager"):
        """Fix eager/interface-only before one live import session is created.

        Inherited extend_context retains this choice; it never silently changes
        modes, retries authoring, or renews any owner or resource allowance.
        """
        F.need(self._session is None, "CLIENT_IMPORT_SESSION_ALREADY_CREATED")
        F.need(type(definition_mode) is str and definition_mode in ("eager", "interface-only"),
               "CLIENT_DEFINITION_MODE")
        self._definition_mode = self._origin_definition_mode = definition_mode
        self._session = MixedImportSession(legacy_verifier=self.receipt, aggregate_verifier=self.aggregate,
            delta_verifier=self.delta, **self.grant._limits["imports"], wall_seconds=self.grant.remaining_seconds())
        self._counts["new_import_sessions"] += 1
        return self._context_data(warrants, selected, openings, bodies)

    def _inspect(self, raw):
        return inspect_evidence(raw, self.workspace._envelope, aggregate_image=self._aggregate_image,
            terminal_receipt_bytes=self.workspace.config["terminal_receipt_bytes"],
            terminal_i=self.workspace.config["wire_profile"]["schema"] == PROFILE_SCHEMA_V2)

    def _expected(self, exact, expected):
        if expected is not None:
            F.need(type(expected) is bytes and len(expected) == 184, "CLIENT_EXPECTED_EXACT_J_BYTES")
            B.member_journal(expected)
            F.need(exact == expected, "CLIENT_EXPECTED_EXACT_J_MISMATCH")

    def _admit_i(self, receipt, expected_summary, cpu, wall, memory, *, trial=False):
        # Same positive cache/accounting path for ordinary and opt-in admission.
        # None can arrive only from the original issuer's clean-refusal branch.
        F.need(self.receipt is not None, "CLIENT_I_OWNER_NOT_SELECTED")
        self._charge(receipt); self._charge(C.canonical(expected_summary))
        key = (_sha(receipt), len(receipt), C.canonical(expected_summary))
        if key in self._receipt_cache:
            token = self._receipt_cache[key]; self._warrant(token)
            self._counts["same_live_hits"] += 1; return token
        self._budget.verification(len(receipt), cpu)
        self._counts["admission_submissions"] += 1
        output = self.grant.directory/("receipt-"+str(self._counts["admission_submissions"]))
        receive = self.receipt.try_receive if trial else self.receipt.receive
        handle = receive(receipt, expected_summary, output, cpu_seconds=cpu,
            wall_seconds=min(wall, self.grant.remaining_seconds()), memory_mib=memory)
        if trial and handle is None:
            return None
        token = self._issue("I", handle, receipt); self._receipt_cache[key] = token
        return token

    @_action
    def admit_receipt(self, receipt, expected_summary, *, cpu_seconds=30, wall_seconds=60, memory_mib=1024):
        return self._admit_i(receipt, expected_summary, cpu_seconds, wall_seconds, memory_mib)

    def _admit_a_member(self, receipt_bytes, expected_header, exact_journal, index, siblings,
                        cpu, wall, memory, *, trial=False):
        F.need(type(receipt_bytes) is bytes and 0 < len(receipt_bytes) <= 64*MIB
               and type(expected_header) is bytes and len(expected_header) == B.HEADER_BYTES
               and type(exact_journal) is bytes and len(exact_journal) == 184
               and type(siblings) is list and len(siblings) <= B.MAX_SIBLINGS
               and all(type(part) is bytes and len(part) == 32 for part in siblings),
               "CLIENT_AGGREGATE_MEMBER_INPUT")
        self._charge(receipt_bytes); self._charge(expected_header); self._charge(exact_journal)
        for part in siblings: self._charge(part)
        F.uint(index, 0, B.MAX_MEMBERS-1); self._charge(C.canonical(index))
        F.uint(cpu, 1, 600); F.uint(wall, 1, 600); F.uint(memory, 64, 4096)
        # Membership is checked before any issuer call, including a trial.
        B.bind_member(expected_header, exact_journal, index, siblings, adopted_image=self._aggregate_image)
        key = (self._aggregate_image, self._profiles[1], _sha(receipt_bytes), len(receipt_bytes), expected_header)
        if key in self._aggregate_cache:
            handle, expected = self._aggregate_cache[key]
            F.need(self._aggregate_fact(handle, receipt_bytes, expected_header) == expected,
                   "CLIENT_AGGREGATE_CACHE_CHANGED")
            self._counts["same_live_hits"] += 1
        else:
            self._budget.verification(len(receipt_bytes), cpu)
            self._counts["admission_submissions"] += 1
            output = self.grant.directory/("aggregate-"+str(self._counts["admission_submissions"]))
            receive = self.aggregate.try_receive if trial else self.aggregate.receive
            handle = receive(receipt_bytes, expected_header, output, cpu_seconds=cpu,
                wall_seconds=min(wall, self.grant.remaining_seconds()), memory_mib=memory)
            if trial and handle is None:
                return None
            self._aggregate_cache[key] = handle, self._aggregate_fact(handle, receipt_bytes, expected_header)
        # No recoverable catch encloses member selection or warrant issuance.
        member = self.aggregate.select_member(handle, exact_journal, index, siblings)
        return self._issue("A-member", member, receipt_bytes)

    @_action
    def admit_aggregate_member(self, receipt_bytes, expected_header, exact_journal, index, siblings,
                               *, cpu_seconds=30, wall_seconds=60, memory_mib=1024):
        return self._admit_a_member(receipt_bytes, expected_header, exact_journal, index, siblings,
                                    cpu_seconds, wall_seconds, memory_mib)

    @staticmethod
    def _terminal_trial_result(status, kind, raw, summary, token=None):
        result = {"status": status, "evidence_kind": kind, "module": C.summary_id(summary),
                  "packet_sha256": _sha(raw), "packet_bytes": len(raw),
                  "authority": "LOCAL_ATTEMPT_OUTCOME_NOT_TRANSFERABLE_PROOF"}
        if status == "ADMITTED":
            F.need(token is not None, "CLIENT_TRIAL_MISSING_WARRANT")
            result["warrant"] = token
        else:
            F.need(status in ("NOT_ADMITTED", "UNSUPPORTED_TRIAL_FORM") and token is None,
                   "CLIENT_TRIAL_OUTCOME")
        return result

    def _admit_evidence(self, raw, summary, expected, native_cpu, receipt_cpu, wall, memory,
                        *, terminal_trial=False):
        for value in (native_cpu, receipt_cpu, wall): F.uint(value, 1, 600)
        F.uint(memory, 64, 4096)
        kind, target, exact, unused = self._inspect(raw)
        F.need(target == summary, "CLIENT_EVIDENCE_TARGET_SUMMARY")
        self._expected(exact, expected)
        if kind == "mixed":
            if terminal_trial:
                return self._terminal_trial_result("UNSUPPORTED_TRIAL_FORM", kind, raw, summary)
            token = super()._admit_packet(raw, summary, native_cpu, receipt_cpu, wall, memory)
        elif kind == "terminal-i":
            receipt, journal, unused_member = parse_terminal_i(raw, self.workspace._envelope,
                aggregate_image=self._aggregate_image,
                terminal_receipt_bytes=self.workspace.config["terminal_receipt_bytes"],
                terminal_i=self.workspace.config["wire_profile"]["schema"] == PROFILE_SCHEMA_V2)
            token = self._admit_i(receipt, summary, receipt_cpu, wall, memory, trial=terminal_trial)
        else:
            F.need(kind == "terminal", "CLIENT_EVIDENCE_KIND")
            receipt, header, journal, index, siblings, unused = parse_terminal(raw, self.workspace._envelope,
                aggregate_image=self._aggregate_image,
                terminal_receipt_bytes=self.workspace.config["terminal_receipt_bytes"])
            token = self._admit_a_member(receipt, header, journal, index, list(siblings),
                                        receipt_cpu, wall, memory, trial=terminal_trial)
        if terminal_trial and token is None:
            # No authority/cache insertion, staging/import mutation or retry.
            return self._terminal_trial_result("NOT_ADMITTED", kind, raw, summary)
        live_kind, unused_handle, live_raw, live = self._warrant(token)
        if kind == "terminal-i":
            F.need(live_kind == "I" and live_raw == receipt
                   and live["profile_id"] == self._profiles[0]
                   and live["receipt_sha256"] == _sha(receipt), "CLIENT_TERMINAL_I_LIVE_RECEIPT")
        # This equality is unconditional, including I receipt-cache hits and
        # callers with no separate expected J. ModuleID/summary do not bind rank.
        F.need(live["journal"] == exact and live["summary"] == summary, "CLIENT_EVIDENCE_LIVE_TARGET")
        self._expected(live["journal"], expected)
        # This cache is only a same-live acquisition locator. On a terminal
        # hit, A rebinds membership and I revalidates its exact live receipt/J.
        self._packet_cache[(_sha(raw), len(raw), C.canonical(summary))] = token
        if terminal_trial:
            return self._terminal_trial_result("ADMITTED", kind, raw, summary, token)
        return token

    @_action
    def admit_local(self, module, packet_sha256, packet_bytes, *, expected_exact_journal=None,
                    native_cpu_seconds=30, receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024):
        raw = self._store(self.workspace.packets.get, packet_sha256, packet_bytes); self._charge(raw)
        summary, unused = self.workspace.packets.inspect(module, raw)
        return self._admit_evidence(raw, summary, expected_exact_journal, native_cpu_seconds,
                                    receipt_cpu_seconds, wall_seconds, memory_mib)

    @_terminal_action
    def try_admit_terminal_local(self, module, packet_sha256, packet_bytes, *, expected_exact_journal=None,
                                 receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024):
        """One terminal trial from exact custody; no staging, import or retry.

        NOT_ADMITTED is a settled verifier nonacceptance, not invalid mathematics.
        Existing live contexts/selections are neither replaced nor rolled back.
        """
        raw = self._store(self.workspace.packets.get, packet_sha256, packet_bytes); self._charge(raw)
        summary, unused = self.workspace.packets.inspect(module, raw)
        return self._admit_evidence(raw, summary, expected_exact_journal, 30,
            receipt_cpu_seconds, wall_seconds, memory_mib, terminal_trial=True)

    @_async_action
    async def resolve(self, provider, record):
        F.need(self._search is not None, "CLIENT_SEARCH_NOT_READY")
        self._charge(C.canonical(record))
        if self._acquisition is None:
            self._acquisition = EvidenceAcquisition.from_search(self._handoff,
                self.workspace.config["wire_profile"], self.workspace.modules, self.workspace.packets,
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

    def _declaration_attempt_sources(self):
        """Extend the existing attempt source guard with the selected group route."""
        self._body_attempt_sources()
        F.need(DR is sys.modules["transport.declaration_resilience"]
               and _try_declaration is DR.try_declaration,
               "CLIENT_DECLARATION_ATTEMPT_SYMBOL_CHANGED")
        root = Path(DR.__file__).resolve().parents[1]
        name = "transport.declaration_resilience"
        path = root/"transport/declaration_resilience.py"
        pins = [owner._pins[path] for owner in (self.receipt, self.aggregate, self.delta)
                if owner is not None and path in owner._pins]
        F.need(pins and all(pin == pins[0] for pin in pins),
               "CLIENT_DECLARATION_ATTEMPT_REQUIRED_SOURCE_PIN")
        self._required_origins[name] = path
        self._source_pins[path] = deepcopy(pins[0])
        self._active()

    @_async_action
    async def try_resolve_declaration(self, origin_candidate, module, relative_name, *, max_bytes,
                                      supplier=None, attempt_timeout_ms=5000):
        """One exact-name attempt; only settled supplier absence preserves work."""
        from . import direct_contacts
        self._declaration_attempt_sources()
        provider, unused = self._candidate(origin_candidate)
        provider = self._selected_supplier(provider if supplier is None else supplier)
        self._charge(C.canonical({"module": module, "relative_name": relative_name,
            "max_bytes": max_bytes, "supplier": provider, "attempt_timeout_ms": attempt_timeout_ms}))
        result = await _try_declaration(self._acquisition, provider, module, relative_name,
                                       max_bytes, attempt_timeout_ms=attempt_timeout_ms)
        self._declaration_attempt_sources()
        if result["status"] == "UNAVAILABLE_AT_SELECTED_SUPPLIER":
            return result
        F.need(result["status"] == "DECLARATION_VALIDATED", "CLIENT_DECLARATION_ATTEMPT_RESULT")
        resolved = result["resolved"]
        loc = resolved["locator"]
        # Commit/readback and final checks have no recoverable exception path.
        self.workspace.modules.put_group(loc["module_id"], resolved["opening"],
                                         before_commit=self._acquisition._active)
        opening, descriptor = self.workspace.modules.get_group(
            loc["module_id"], loc["relative_name"], loc["group_index"])
        F.need(opening == resolved["opening"] and descriptor == resolved["descriptor"],
               "EVIDENCE_DECLARATION_COMMIT_READBACK")
        self._acquisition._active()
        self._charge(C.canonical(opening))
        candidate = Candidate()
        self._candidates[candidate] = provider, _copy({**resolved,
            "candidate_origin": "EXACT_NAME_NOT_INDEX_SEARCH",
            "next_gate": "ACTUAL_PUBLIC_CLIENT_EVIDENCE_ADMISSION_BEFORE_MATHEMATICAL_USE"})
        return {"status": "DECLARATION_CUSTODIED", "candidate": candidate,
                "mathematical_acceptance": False}

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
        from . import direct_contacts, located_queries
        F.need(AR is sys.modules["transport.acquisition_resilience"]
               and _try_body is AR.try_body, "CLIENT_BODY_ATTEMPT_SYMBOL_CHANGED")
        root = Path(AR.__file__).resolve().parents[1]
        names = ("transport.acquisition_resilience", "transport.search_resilience",
                 "transport.http_provider", "transport.clients", "transport.receipt_client",
                 "transport.located_receipts", "client.direct_contacts", "client.located_queries",
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
        """Acquire offered evidence through the ordinary live admission gate."""
        return await self._acquire_packet(candidate, entry, bodies=bodies,
            expected_exact_journal=expected_exact_journal, native_cpu_seconds=native_cpu_seconds,
            receipt_cpu_seconds=receipt_cpu_seconds, wall_seconds=wall_seconds, memory_mib=memory_mib,
            offered=True)

    @_async_action
    async def acquire_exact(self, candidate, entry, *, bodies=(), expected_exact_journal=None,
                            native_cpu_seconds=30, receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024):
        """Acquire a known digest and size through that same admission gate."""
        return await self._acquire_packet(candidate, entry, bodies=bodies,
            expected_exact_journal=expected_exact_journal, native_cpu_seconds=native_cpu_seconds,
            receipt_cpu_seconds=receipt_cpu_seconds, wall_seconds=wall_seconds, memory_mib=memory_mib,
            offered=False)

    @_async_terminal_action
    async def try_acquire_terminal(self, candidate, entry, *, expected_exact_journal=None,
                                    receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024):
        """One offered terminal trial; safe refusal is data, unsafe failure fatal."""
        return await self._acquire_packet(candidate, entry, bodies=(),
            expected_exact_journal=expected_exact_journal, native_cpu_seconds=30,
            receipt_cpu_seconds=receipt_cpu_seconds, wall_seconds=wall_seconds, memory_mib=memory_mib,
            offered=True, terminal_trial=True)

    @_async_terminal_action
    async def try_acquire_terminal_exact(self, candidate, entry, *, expected_exact_journal=None,
                                          receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024):
        """One known-identity terminal trial, without offer membership or bodies."""
        return await self._acquire_packet(candidate, entry, bodies=(),
            expected_exact_journal=expected_exact_journal, native_cpu_seconds=30,
            receipt_cpu_seconds=receipt_cpu_seconds, wall_seconds=wall_seconds, memory_mib=memory_mib,
            offered=False, terminal_trial=True)

    async def _acquire_packet(self, candidate, entry, *, bodies, expected_exact_journal,
                              native_cpu_seconds, receipt_cpu_seconds, wall_seconds, memory_mib, offered,
                              terminal_trial=False):
        provider, resolved = self._candidate(candidate); loc = resolved["locator"]
        for value in (native_cpu_seconds, receipt_cpu_seconds, wall_seconds): F.uint(value, 1, 600)
        F.uint(memory_mib, 64, 4096)
        if expected_exact_journal is not None:
            F.need(type(expected_exact_journal) is bytes and len(expected_exact_journal) == 184,
                   "CLIENT_EXPECTED_EXACT_J_BYTES")
            B.member_journal(expected_exact_journal)
        F.fields(entry, ("packet_sha256", "packet_bytes"))
        F.hexid(entry["packet_sha256"]); F.uint(entry["packet_bytes"], 1, 32*MIB)
        entry = dict(entry)
        if offered:
            F.need((provider, loc["module_id"], entry["packet_sha256"], entry["packet_bytes"])
                   in self._acquisition._offers, "CLIENT_UNOFFERED_PACKET")
        F.need(type(bodies) in (list, tuple) and len(bodies) <= 16384, "CLIENT_BODY_REQUESTS")
        F.need(not terminal_trial or not bodies, "CLIENT_TERMINAL_TRIAL_NO_BODY_REQUESTS")
        # Snapshot every body selection before the first transfer, not lazily
        # during the loop: the caller may otherwise mutate later requests.
        selected_bodies = []
        for item in bodies:
            F.fields(item, ("digest", "max_bytes"))
            F.hexid(item["digest"])
            F.need(type(item["max_bytes"]) is int, "CLIENT_BODY_MAX_BYTES")
            selected_bodies.append(dict(item))
        bodies = tuple(selected_bodies)
        for item in bodies:
            result = await self._acquisition.body(provider, resolved, item["digest"], item["max_bytes"])
            self._charge(C.canonical(result["body"]))
        key = entry["packet_sha256"], entry["packet_bytes"], C.canonical(resolved["opening"]["summary"])
        if key in self._packet_cache:
            self._warrant(self._packet_cache[key])
        else:
            transfer = self._acquisition.packet if offered else self._acquisition.packet_exact
            await transfer(provider, loc["module_id"], entry)
        demands = [x["digest"] for x in bodies]
        self._acquisition.custody_ready(resolved, entry, demands)
        raw = self._store(self.workspace.packets.get, entry["packet_sha256"], entry["packet_bytes"])
        self._charge(raw)
        result = self._admit_evidence(raw, resolved["opening"]["summary"], expected_exact_journal,
            native_cpu_seconds, receipt_cpu_seconds, min(wall_seconds, self.grant.remaining_seconds()), memory_mib,
            terminal_trial=terminal_trial)
        if terminal_trial:
            if result["status"] != "ADMITTED":
                F.need(result["status"] in ("NOT_ADMITTED", "UNSUPPORTED_TRIAL_FORM"), "CLIENT_TRIAL_OUTCOME")
                # Local custody/liveness failure remains fatal even after a
                # settled verifier refusal; no commit error is an ordinary miss.
                self._acquisition.custody_ready(resolved, entry, demands)
                return result
            token = result["warrant"]
        else:
            token = result
        kind, handle, unused, live = self._warrant(token)
        F.need(kind in ("I", "A-member", "mixed"), "CLIENT_EVIDENCE_WARRANT_KIND")
        owner = self.receipt if kind == "I" else self.aggregate if kind == "A-member" else self.delta
        owner.open_group(handle, resolved["opening"])
        self._acquisition.custody_ready(resolved, entry, demands)
        unused_kind, unused_handle, unused_raw, final = self._warrant(token)
        F.need(final["journal"] == live["journal"], "CLIENT_EVIDENCE_FINAL_TARGET")
        self._expected(final["journal"], expected_exact_journal)
        if terminal_trial:
            return result
        return token

    @_action
    def export_evidence(self, warrant):
        kind, unused_handle, raw, live = self._warrant(warrant)
        F.need(kind in ("I", "mixed", "A-member"), "CLIENT_EVIDENCE_WARRANT_KIND")
        if kind == "A-member":
            raw = pack_terminal(live["aggregate_header"], live["journal"], live["member_index"],
                live["siblings"], raw, aggregate_image=self._aggregate_image, envelope=self.workspace._envelope,
                terminal_receipt_bytes=self.workspace.config["terminal_receipt_bytes"])
        elif kind == "I":
            raw = pack_terminal_i(live["journal"], raw, aggregate_image=self._aggregate_image,
                envelope=self.workspace._envelope,
                terminal_receipt_bytes=self.workspace.config["terminal_receipt_bytes"],
                terminal_i=self.workspace.config["wire_profile"]["schema"] == PROFILE_SCHEMA_V2)
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
        F.need(kind in ("terminal", "terminal-i"), "CLIENT_EVIDENCE_KIND")
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
        result = {**super().report(), "schema": REPORT_SCHEMA,
                "evidence_forms": ["mixed", "terminal"] + (["terminal-i"]
                    if self.workspace.config["wire_profile"]["schema"] == PROFILE_SCHEMA_V2 else []),
                "terminal_receipt_bytes": self.workspace.config["terminal_receipt_bytes"]}
        if self._origin_body_pool is not None:
            result["body_location"] = self._origin_body_pool.report()
        return result

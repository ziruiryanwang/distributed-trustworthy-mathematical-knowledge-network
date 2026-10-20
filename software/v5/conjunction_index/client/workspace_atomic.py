"""Persistent untrusted custody plus one finite, concrete I-only owner session.

This is a trusted-owner Windows library, not a sandbox or an autonomous agent.
Reserve the grant before constructing owners inside the caller's enclosing Job.
Only successful operation construction transfers those exact owners. Saved data
and reports never recreate authority. All public work is serialized.
"""
from __future__ import annotations

import asyncio
from copy import deepcopy
from dataclasses import asdict
from functools import wraps
import hashlib
import json
import math
import os
from pathlib import Path
import secrets
import sqlite3
import time

from admission.verifier import ReceiptVerifier
from aggregate_claims import bindings as B
from custody.module_store import ModuleStore, BODY_SCHEMA, permitted_hashes
from discovery import formal_features as F
from discovery.discovery_store import Store, ordinary
from discovery.module_export_adapter import ModuleExportAdapter
from frontier_network.custody import PacketStore, public_profile, profile_id
from frontier_network.transport import FrontierAcquisition, FrontierLocatedHandoff
from location.controller_services import ServiceLocationProcess
from location.protocol import OwnerEgressPolicy
from location.observed_route import route
from location.available_descriptor import descriptor
from mixed_claims.authoring_atomic import MixedSourceOperation, MixedOwnerPreparation
from mixed_claims.imports_atomic import MixedImportSession
from mixed_claims.packet import Envelope, parse_packet
from mixed_claims.receiver import MixedDeltaVerifier
from modules import codec as C
from transport.receipt_client import AcquisitionBudget, LIMITS as ACQUISITION_LIMITS

MIB = 1024**2
SCHEMA = "DMKN_V5_CLIENT_WORKSPACE_V1"
GRANT_SCHEMA = "DMKN_V5_CLIENT_GRANT_V1"
LIMITS = {"wall_seconds": (1, 3600), "controller_cpu_seconds": (1, 3600),
          "calls": (1, 4096), "input_bytes": (1, 512*MIB),
          "worker_cpu_seconds": (1, 86400), "output_bytes": (128*MIB, 2*1024*MIB),
          "output_entries": (32, 8192)}
IMPORT_LIMITS = {"max_sources": (1, 128), "max_members": (1, 1024),
                 "max_receipts": (1, 128), "max_calls": (1, 65536),
                 "submitted_bytes": (1, 256*MIB), "data_bytes": (1, 16*MIB)}


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _limits(value, bounds):
    F.fields(value, bounds)
    for key, pair in bounds.items(): F.uint(value[key], *pair, "CLIENT_LIMIT:"+key)


def _copy(value):
    return C.parse_json(C.canonical(value))


def _operational_bytes(value):
    """Operational telemetry permits finite floats; mathematical decoding does not."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def _operational_value(raw):
    value = json.loads(raw)
    F.need(_operational_bytes(value) == raw, "CLIENT_OPERATIONAL_RECORD_CANONICAL")
    return value


def _grant_bytes(grant):
    return _operational_bytes({"schema": GRANT_SCHEMA, "id": grant._id, "limits": grant._limits,
        "started_monotonic": grant._started, "deadline_monotonic": grant._deadline,
        "controller_started_process_time": grant._cpu, "directory": str(grant._directory),
        "authority": "HISTORICAL_GRANT_DATA_NOT_RESTARTABLE_AUTHORITY"})


def _under(path, root):
    path = Path(path)
    F.need(path.is_absolute() and path != root and path.is_relative_to(root), "CLIENT_OUTPUT_SCOPE")
    return path


def _action(method):
    @wraps(method)
    def call(self, *args, **kwargs):
        self._enter()
        try:
            result = method(self, *args, **kwargs)
            self._active(); self._census()
            return result
        except BaseException as error:
            self._fail(error); raise
        finally: self._busy = False
    return call


def _async_action(method):
    @wraps(method)
    async def call(self, *args, **kwargs):
        self._enter()
        try:
            result = await method(self, *args, **kwargs)
            self._active(); self._census()
            return result
        except BaseException as error:
            self._fail(error); raise
        finally: self._busy = False
    return call


class OperationGrant:
    """Opaque workspace-issued grant; persisted fields are not reissuable tokens."""
    __slots__ = ("_workspace", "_id", "_limits", "_started", "_cpu", "_deadline", "_directory", "_used")

    @property
    def identifier(self): return self._id
    @property
    def limits(self): return deepcopy(self._limits)
    @property
    def started(self): return self._started
    @property
    def deadline(self): return self._deadline
    @property
    def directory(self): return self._directory

    def remaining_seconds(self):
        value = math.floor(self._deadline-time.monotonic())
        F.need(value >= 1, "CLIENT_GRANT_EXPIRED")
        return value


class LiveWarrant:
    """Same-client reference to an actual issuer handle, never transferable proof."""
    __slots__ = ()


class AuthorContext:
    """Same-client reference to one live mixed import selection, not a JSON context."""
    __slots__ = ()


class Candidate:
    """Same-query reference to an actually resolved formal export."""
    __slots__ = ()


class PartialPublicationError(RuntimeError):
    """Recoverable audit locator; no rollback, mathematical or availability claim."""
    def __init__(self, publication_id, outcome):
        self.publication_id, self.outcome = publication_id, deepcopy(outcome)
        super().__init__("PARTIAL_PUBLICATION:"+publication_id+":"+outcome["phase"])


class Workspace:
    """One process owns the workspace lock; stores and reports contain no authority."""
    @classmethod
    def open(cls, root, config, create=False):
        F.need(os.name == "nt", "CLIENT_WINDOWS_OWNER_REQUIRED")
        F.fields(config, ("schema", "wire_profile", "module_limits", "packet_limits", "index_limits",
                          "packet_envelope", "max_operations", "max_report_bytes", "ledger_pages"))
        F.need(config["schema"] == SCHEMA, "CLIENT_WORKSPACE_SCHEMA")
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
            self.packets = PacketStore(self.root/"packets", public_profile(), config["packet_limits"],
                                       envelope=envelope, create=create)
            self.index = Store(self.root/"index", self.adapter, config["index_limits"], create=create)
            # The OS lock rules out another live owner. No prior monotonic grant resumes.
            self.db.execute("UPDATE operations SET status='INTERRUPTED_WITH_UNCERTAIN_TAIL' "
                            "WHERE status IN ('GRANTED','OPEN','FAILED_PENDING_CLOSE')")
            return self
        except BaseException:
            self._release(); raise

    def _active(self):
        F.need(not self._closed and C.canonical(self.config) == self._config_raw,
               "CLIENT_WORKSPACE_CLOSED_OR_CHANGED")

    def _record(self, identifier, status, report=None):
        raw = None if report is None else _operational_bytes(report)
        F.need(raw is None or len(raw) <= self.config["max_report_bytes"], "CLIENT_REPORT_LIMIT")
        self.db.execute("UPDATE operations SET status=?,report=COALESCE(?,report) WHERE id=?",
                        (status, raw, identifier))

    def reserve(self, limits, *, outer_deadline=None):
        """Explicit new grant, BEFORE runtime-owner construction; never called by a retry."""
        self._active()
        F.need(not self._poisoned and self._client is None and not self._grants,
               "CLIENT_OPERATION_RESERVED_OR_CLEANUP_UNCERTAIN")
        F.fields(limits, (*LIMITS, "acquisition", "imports"))
        _limits({key: limits[key] for key in LIMITS}, LIMITS)
        _limits(limits["acquisition"], ACQUISITION_LIMITS); _limits(limits["imports"], IMPORT_LIMITS)
        F.need(limits["acquisition"]["worker_cpu_seconds"] <= limits["worker_cpu_seconds"],
               "CLIENT_ADMISSION_SUBALLOCATION")
        count = self.db.execute("SELECT count(*) FROM operations").fetchone()[0]
        F.need(count < self.config["max_operations"], "CLIENT_OPERATION_STORAGE_LIMIT")
        grant = OperationGrant()
        grant._workspace, grant._id, grant._limits = self, secrets.token_hex(32), _copy(limits)
        grant._started, grant._cpu = time.monotonic(), time.process_time()
        grant._deadline = grant._started+limits["wall_seconds"]
        if outer_deadline is not None:
            F.need(type(outer_deadline) in (int, float) and math.isfinite(outer_deadline)
                   and outer_deadline > grant._started, "CLIENT_OUTER_DEADLINE")
            grant._deadline = min(grant._deadline, outer_deadline)
        grant._directory = ordinary(self.root/"operations"/grant._id, fresh=True)
        grant._used = False
        raw = _grant_bytes(grant)
        self.db.execute("INSERT INTO operations VALUES(?,?,'GRANTED',NULL)", (grant._id, raw))
        try: grant._directory.mkdir()
        except BaseException:
            self._record(grant.identifier, "FAILED_GRANT_ISSUANCE"); raise
        self._grants[grant] = raw
        return grant

    def _grant_active(self, grant):
        F.need(type(grant) is OperationGrant and grant in self._grants and grant._workspace is self
               and _grant_bytes(grant) == self._grants[grant]
               and time.monotonic() < grant.deadline, "CLIENT_GRANT_CHANGED_OR_EXPIRED")

    def operation(self, grant, *, receipt_owner, delta_owner, preparation_owner=None,
                  foundation_bytes, foundation_sha256):
        """Transfer exact owners on SUCCESS only; caller cleans up construction failure."""
        self._active(); self._grant_active(grant)
        F.need(not self._poisoned and self._client is None, "CLIENT_OPERATION_ACTIVE_OR_UNCERTAIN")
        F.need(type(grant) is OperationGrant and grant in self._grants
               and grant._workspace is self and not grant._used, "CLIENT_EXACT_UNUSED_GRANT")
        client = CommonsClient(self, grant, receipt_owner, delta_owner, preparation_owner,
                               foundation_bytes, foundation_sha256)
        self._record(grant.identifier, "OPEN")
        grant._used = True; self._client = client
        return client

    def status(self):
        self._active()
        counts = dict(self.db.execute("SELECT status,count(*) FROM operations GROUP BY status"))
        return {"schema": SCHEMA, "wire_profile_id": self.packets.profile_id,
                "operations": counts, "modules": self.modules.status(), "packets": self.packets.status(),
                "index": self.index.status(), "active_client": self._client is not None,
                "mathematical_acceptance": False}

    def history(self, kind, *, after=None, limit=16):
        """Bounded audit identifiers, in lexical ID order; not a live-corpus snapshot."""
        self._active(); F.need(kind in ("operations", "publications"), "CLIENT_HISTORY_KIND")
        F.uint(limit, 1, 64)
        if after is not None: F.hexid(after)
        rows = self.db.execute("SELECT id FROM "+kind+" WHERE id>? ORDER BY id LIMIT ?",
                               ("" if after is None else after, limit+1)).fetchall()
        selected = [row[0] for row in rows[:limit]]
        return {"kind": kind, "identifiers": selected,
                "next_cursor": selected[-1] if len(rows) > limit else None,
                "ordering": "LEXICAL_IDS_NOT_A_SNAPSHOT_OF_CONCURRENT_NEW_RECORDS",
                "mathematical_acceptance": False}

    def read_record(self, kind, identifier, *, max_bytes=1048576):
        """Read bounded untrusted audit data; never restore grants, contexts or handles."""
        self._active(); F.hexid(identifier); F.uint(max_bytes, 1024, 2*MIB)
        F.need(kind in ("operations", "publications"), "CLIENT_HISTORY_KIND")
        json_columns = ("grant", "report") if kind == "operations" else ("intent", "outcome")
        columns = (("status",) if kind == "operations" else ("operation",))+json_columns
        lengths = self.db.execute("SELECT "+",".join("COALESCE(length(CAST("+x+" AS BLOB)),0)" for x in columns)
                                  +" FROM "+kind+" WHERE id=?", (identifier,)).fetchone()
        F.need(lengths is not None and sum(lengths) <= max_bytes, "CLIENT_AUDIT_MISSING_OR_BYTE_CAP")
        row = self.db.execute("SELECT "+",".join(columns)+" FROM "+kind+" WHERE id=?", (identifier,)).fetchone()
        F.need(row is not None and sum(0 if x is None else len(x.encode("utf-8") if type(x) is str else x)
                                     for x in row) <= max_bytes,
               "CLIENT_AUDIT_READ_BOUND")
        result = {name: (None if raw is None else _operational_value(bytes(raw)))
                  if name in json_columns else raw for name, raw in zip(columns, row)}
        return {"identifier": identifier, "kind": kind, **result,
                "authority": "UNTRUSTED_HISTORICAL_RECORD_ONLY", "mathematical_acceptance": False}

    def _release(self):
        for store in (self.index, self.packets, self.modules):
            if store is not None: store.close()
        if self.db is not None: self.db.close(); self.db = None
        if self._lock is not None: self._lock.close(); self._lock = None
        self._closed = True

    def close(self):
        if self._closed: return
        F.need(self._client is None, "CLIENT_CLOSE_ACTIVE_OPERATION_FIRST")
        for grant in self._grants:
            self._record(grant.identifier, "UNTRANSFERRED_GRANT_CLOSED")
        self._grants.clear(); self._release()


class CommonsClient:
    """One finite caller-serialized lifecycle. No owner factories or JSON authority."""
    def __init__(self, workspace, grant, receipt, delta, preparation, foundation, foundation_sha):
        F.need(type(receipt) is ReceiptVerifier and type(delta) is MixedDeltaVerifier,
               "CLIENT_EXACT_REAL_OWNERS")
        F.need(preparation is None or type(preparation) is MixedOwnerPreparation,
               "CLIENT_EXACT_PREPARATION_OWNER")
        F.need(delta._owners == (receipt, None) and delta._aggregate_image is None
               and (receipt._image, receipt._foundation, receipt._policy)
               == (B.RELATION_IMAGE, B.FOUNDATION, B.POLICY), "CLIENT_SHARED_I_ORIGIN")
        receipt._check_install(); delta._check()
        F.need(receipt.report()["attempts"] == delta.report()["attempts"] == 0
               and receipt.report()["live_handles"] == delta.report()["live_handles"] == 0,
               "CLIENT_PRISTINE_ISSUERS")
        F.need(receipt._deadline <= grant.deadline and delta._deadline <= grant.deadline,
               "CLIENT_ORIGINAL_OWNER_DEADLINE")
        F.need(delta._started >= grant.started and asdict(delta._envelope) == asdict(workspace._envelope),
               "CLIENT_DELTA_STARTED_OR_ENVELOPE")
        _under(delta._output, grant.directory)
        caps = grant._limits; acquisition = caps["acquisition"]
        F.need(receipt._caps[2] <= acquisition["worker_cpu_seconds"]
               and delta._caps[2] <= acquisition["worker_cpu_seconds"]
               and delta._caps[3] <= caps["controller_cpu_seconds"], "CLIENT_OWNER_SUBALLOCATION")
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
        self.receipt, self.delta, self.preparation = receipt, delta, preparation
        self._profiles = (receipt.report()["profile_id"], delta.report()["profile_id"])
        self._foundation, self._foundation_sha = foundation, foundation_sha
        self._state, self._busy, self._closed = "OPEN", False, False
        self._calls, self._input_bytes = 0, len(foundation)
        self._warrants, self._receipt_cache, self._packet_cache = {}, {}, {}
        self._candidates, self._context = {}, None
        self._selection_view = None
        self._session = None
        self._channel = self._handoff = self._search = self._acquisition = None
        self._query_used = False
        self._budget = AcquisitionBudget(grant.deadline, acquisition)
        self._failures, self._publications = [], []
        self._counts = {key: 0 for key in ("admission_submissions", "same_live_hits", "author_calls",
            "store_calls", "publication_attempts", "new_import_sessions")}
        self._active(); self._census()

    def _active(self):
        self.workspace._active()
        self.workspace._grant_active(self.grant)
        F.need(not self._closed and self._state == "OPEN" and time.monotonic() < self.grant.deadline,
               "CLIENT_CLOSED_FAILED_OR_EXPIRED")
        F.need(time.process_time()-self.grant._cpu <= self.grant._limits["controller_cpu_seconds"],
               "CLIENT_CONTROLLER_CPU_LIMIT")
        F.need(self.receipt.report()["profile_id"] == self._profiles[0]
               and self.delta.report()["profile_id"] == self._profiles[1]
               and self.delta._owners == (self.receipt, None), "CLIENT_ISSUER_PROFILE_CHANGED")
        self.receipt._active(); self.delta._active(); self._budget.active()

    def _census(self):
        size = entries = 0
        for parent, dirs, files in os.walk(self.grant.directory, followlinks=False):
            for name in dirs+files:
                path = ordinary(Path(parent)/name, directory=name in dirs)
                entries += 1
                if name in files: size += path.stat().st_size
                F.need(size <= self.grant._limits["output_bytes"]
                       and entries <= self.grant._limits["output_entries"], "CLIENT_OUTPUT_CENSUS_LIMIT")
        return {"bytes": size, "entries": entries, "hard_disk_limit": False}

    def _enter(self):
        F.need(not self._busy, "CLIENT_SERIALIZED_CALLS_REQUIRED")
        try:
            self._active()
            F.need(self._calls < self.grant._limits["calls"], "CLIENT_CALL_LIMIT")
        except BaseException as error:
            if not self._closed and self._state == "OPEN": self._fail(error)
            raise
        self._calls += 1; self._busy = True

    def _charge(self, raw):
        F.need(type(raw) is bytes, "CLIENT_EXACT_INPUT_BYTES")
        self._input_bytes += len(raw)
        F.need(self._input_bytes <= self.grant._limits["input_bytes"], "CLIENT_INPUT_LIMIT")

    def _store(self, method, *args, **kwargs):
        self._active(); self._counts["store_calls"] += 1
        F.need(self._counts["store_calls"] <= self.grant._limits["imports"]["max_calls"],
               "CLIENT_STORE_CALL_LIMIT")
        result = method(*args, **kwargs); self._active(); return result

    def _fail(self, error):
        self._state = "FAILED"
        self._failures.append(type(error).__name__+":"+str(error)[:1000])
        self._warrants.clear(); self._receipt_cache.clear(); self._packet_cache.clear(); self._context = None
        for owner in (self._session, self.preparation, self.delta, self.receipt):
            if owner is not None:
                try: owner.close()
                except BaseException as cleanup: self._failures.append("cleanup:"+type(cleanup).__name__)
        try: self.workspace._record(self.grant.identifier, "FAILED_PENDING_CLOSE", self.report())
        except BaseException: self._failures.append("failure_report_not_persisted")

    def _issue(self, kind, handle, raw):
        live = self.receipt.describe(handle) if kind == "I" else self.delta.describe(handle)
        token = LiveWarrant()
        self._warrants[token] = (kind, handle, raw, _copy({**live, "journal": list(live["journal"])}))
        return token

    def _warrant(self, token):
        F.need(type(token) is LiveWarrant and token in self._warrants, "CLIENT_FOREIGN_WARRANT")
        kind, handle, raw, expected = self._warrants[token]
        live = self.receipt.describe(handle) if kind == "I" else self.delta.describe(handle)
        F.need(_copy({**live, "journal": list(live["journal"])}) == expected,
               "CLIENT_EXACT_WARRANT_CHANGED")
        F.need(_sha(raw) == (live["receipt_sha256"] if kind == "I" else live["packet_sha256"]),
               "CLIENT_EVIDENCE_CHANGED")
        return kind, handle, raw, live

    @_action
    def describe(self, token):
        kind, handle, raw, live = self._warrant(token)
        members = [live] if kind == "I" else self.delta.members(handle)
        return {"kind": kind, "live": live, "members": members,
                "authority": "SAME_CLIENT_LIVE_REFERENCE_NOT_TRANSFERABLE_REPORT"}

    @_action
    def admit_receipt(self, receipt, expected_summary, *, cpu_seconds=30, wall_seconds=60, memory_mib=1024):
        self._charge(receipt); self._charge(C.canonical(expected_summary))
        key = (_sha(receipt), len(receipt), C.canonical(expected_summary))
        if key in self._receipt_cache:
            token = self._receipt_cache[key]; self._warrant(token)
            self._counts["same_live_hits"] += 1; return token
        self._budget.verification(len(receipt), cpu_seconds)
        self._counts["admission_submissions"] += 1
        output = self.grant.directory/("receipt-"+str(self._counts["admission_submissions"]))
        handle = self.receipt.receive(receipt, expected_summary, output, cpu_seconds=cpu_seconds,
            wall_seconds=min(wall_seconds, self.grant.remaining_seconds()), memory_mib=memory_mib)
        token = self._issue("I", handle, receipt); self._receipt_cache[key] = token
        return token

    def _admit_packet(self, raw, summary, native_cpu_seconds, receipt_cpu_seconds, wall_seconds, memory_mib):
        key = (_sha(raw), len(raw), C.canonical(summary))
        if key in self._packet_cache:
            token = self._packet_cache[key]; self._warrant(token)
            self._counts["same_live_hits"] += 1; return token
        unused, unused2, witnesses, census = parse_packet(raw, self.workspace._envelope, aggregate_image=None)
        F.need(witnesses[-1][2] == summary, "CLIENT_PACKET_TARGET_SUMMARY")
        reserved = census["claims"]*receipt_cpu_seconds+census["deltas"]*native_cpu_seconds
        self._budget.verification(len(raw), reserved); self._counts["admission_submissions"] += 1
        handle = self.delta.receive(raw, summary, native_cpu_seconds=native_cpu_seconds,
            receipt_cpu_seconds=receipt_cpu_seconds, wall_seconds=min(wall_seconds, self.grant.remaining_seconds()),
            memory_mib=memory_mib)
        token = self._issue("mixed", handle, raw); self._packet_cache[key] = token
        return token

    @_action
    def admit_local(self, module, packet_sha256, packet_bytes, *, native_cpu_seconds=30,
                    receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024):
        raw = self._store(self.workspace.packets.get, packet_sha256, packet_bytes); self._charge(raw)
        summary, unused = self.workspace.packets.inspect(module, raw)
        return self._admit_packet(raw, summary, native_cpu_seconds, receipt_cpu_seconds, wall_seconds, memory_mib)

    @_async_action
    async def find(self, channel, specs, policy, location_limits, search_limits, *, routes,
                   descriptor_bytes=4096, descriptor_age_ms=60000):
        """One prospective remote query; returns contacts, not chosen mathematics."""
        F.need(not self._query_used and type(channel) is ServiceLocationProcess
               and type(policy) is OwnerEgressPolicy, "CLIENT_ONE_EXACT_REMOTE_QUERY")
        F.need(channel.deadline == self.grant.deadline
               and self.workspace.root.is_relative_to(channel.adoption.workspace),
               "CLIENT_LOCATION_WORKSPACE_DEADLINE")
        _under(channel.evidence, self.grant.directory); _under(channel.state, self.grant.directory)
        features = self.workspace.adapter.compile_query(specs)
        self._charge(C.canonical(specs))
        F.need(type(routes) is list and 1 <= len(routes) <= location_limits["route_operations"],
               "CLIENT_EXPLICIT_ROUTE_PLAN")
        for item in routes:
            F.fields(item, ("features", "stripe", "event_cap", "peer_cap", "descriptors"))
            chosen = F.validate_features(item["features"], 8)
            F.need(set(chosen) <= set(features), "CLIENT_ROUTE_NOT_QUERY_SUBSET")
            F.uint(item["stripe"], 0, 255)
            F.uint(item["event_cap"], 1, location_limits["routing_events"])
            F.uint(item["peer_cap"], 1, location_limits["routing_peer_slots"])
            F.uint(item["descriptors"], 0, 64)
        F.need(sum(x["event_cap"] for x in routes) <= location_limits["routing_events"]
               and sum(x["peer_cap"] for x in routes) <= location_limits["routing_peer_slots"]
               and sum(x["descriptors"] for x in routes) <= location_limits["descriptor_requests"],
               "CLIENT_ROUTE_SUBALLOCATION")
        handoff = FrontierLocatedHandoff(channel, self.workspace.adapter, features, policy, self._budget,
                                         location_limits, search_limits)
        self._query_used = True; self._channel, self._handoff = channel, handoff
        ready = await channel.start(); self._active()
        attempted, contacts, outcomes = set(), set(), []
        for plan in routes:
            located = await route(handoff.location, plan["features"], plan["stripe"],
                                  event_cap=plan["event_cap"], peer_cap=plan["peer_cap"])
            rows = []
            for peer in [peer for peer in located["peers"] if peer not in attempted][:plan["descriptors"]]:
                attempted.add(peer)
                answer = await descriptor(handoff.location, peer, located["route_key"],
                    max_bytes=descriptor_bytes, max_age_ms=descriptor_age_ms)
                rows.append(answer)
                if answer["status"] == "ADOPTED_ADVISORY_CONTACTS": contacts.update(answer["contacts"])
            outcomes.append({"route": located, "descriptors": rows}); self._active()
        if contacts: self._search = handoff.begin_search()
        return {"status": "QUERY_CONTACTS_READY" if contacts else "NO_CONTACTS_IN_SELECTED_ROUTE_PLAN",
                "contacts": sorted(contacts), "ready": ready, "routes": outcomes,
                "global_complete": False, "mathematical_acceptance": False}

    @_async_action
    async def search_offer(self, provider, max_bytes=1048576, *, max_expanded_bytes=1048576, max_age_ms=60000):
        F.need(self._search is not None, "CLIENT_SEARCH_NOT_READY")
        return await self._search.offer(provider, max_bytes, max_expanded_bytes=max_expanded_bytes,
                                        max_age_ms=max_age_ms)

    @_async_action
    async def search_page(self, provider, snapshot_id, partition, start, limits, *, candidates_only=True):
        F.need(self._search is not None and type(candidates_only) is bool, "CLIENT_SEARCH_NOT_READY")
        method = self._search.candidates if candidates_only else self._search.page
        return await method(provider, snapshot_id, partition, start, limits)

    @_async_action
    async def resolve(self, provider, record):
        F.need(self._search is not None, "CLIENT_SEARCH_NOT_READY")
        self._charge(C.canonical(record))
        if self._acquisition is None:
            self._acquisition = FrontierAcquisition.from_search(self._handoff, public_profile(),
                self.workspace.modules, self.workspace.packets, verifier=self.delta)
        resolved = await self._acquisition.export(provider, record)
        candidate = Candidate(); self._candidates[candidate] = provider, _copy(resolved)
        return candidate

    def _candidate(self, candidate):
        F.need(type(candidate) is Candidate and candidate in self._candidates, "CLIENT_FOREIGN_CANDIDATE")
        return self._candidates[candidate]

    @_action
    def describe_candidate(self, candidate):
        provider, resolved = self._candidate(candidate)
        return {"provider": provider, **deepcopy(resolved)}

    @_async_action
    async def packet_offers(self, candidate, *, max_offers=4, max_bytes=4096):
        provider, resolved = self._candidate(candidate)
        return await self._acquisition.offers(provider, resolved["locator"]["module_id"],
                                              max_offers=max_offers, max_bytes=max_bytes)

    @_async_action
    async def acquire(self, candidate, entry, *, bodies=(), native_cpu_seconds=30,
                      receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024):
        provider, resolved = self._candidate(candidate); loc = resolved["locator"]
        F.need(type(bodies) in (list, tuple) and len(bodies) <= 16384, "CLIENT_BODY_REQUESTS")
        for item in bodies:
            F.fields(item, ("digest", "max_bytes"))
            result = await self._acquisition.body(provider, resolved, item["digest"], item["max_bytes"])
            self._charge(C.canonical(result["body"]))
        summary = resolved["opening"]["summary"]
        key = (entry["packet_sha256"], entry["packet_bytes"], C.canonical(summary))
        F.need((provider, loc["module_id"], entry["packet_sha256"], entry["packet_bytes"])
               in self._acquisition._offers, "CLIENT_UNOFFERED_PACKET")
        if key in self._packet_cache:
            token = self._packet_cache[key]; unused_kind, handle, unused_raw, unused_live = self._warrant(token)
            self._acquisition.custody_ready(resolved, entry, [x["digest"] for x in bodies])
            self.delta.open_group(handle, resolved["opening"]); self.delta.describe(handle)
            self._counts["same_live_hits"] += 1; return token
        await self._acquisition.packet(provider, loc["module_id"], entry)
        self._counts["admission_submissions"] += 1
        result = self._acquisition.admit(resolved, entry, demanded_bodies=[x["digest"] for x in bodies],
            native_cpu_seconds=native_cpu_seconds, receipt_cpu_seconds=receipt_cpu_seconds,
            wall_seconds=min(wall_seconds, self.grant.remaining_seconds()), memory_mib=memory_mib)
        raw = self._store(self.workspace.packets.get, entry["packet_sha256"], entry["packet_bytes"])
        self._charge(raw)
        token = self._issue("mixed", result["handle"], raw); self._packet_cache[key] = token
        return token

    def _context_data(self, warrants, selected, openings, bodies):
        F.need(type(warrants) is list and type(selected) is list and type(openings) is list
               and type(bodies) is list, "CLIENT_CONTEXT_LISTS")
        F.need(all(type(exact) is bytes for exact in selected), "CLIENT_CONTEXT_EXACT_J_BYTES")
        batch = C.canonical({"selected": [list(exact) for exact in selected],
                             "openings": openings, "bodies": bodies})
        self._charge(batch)
        for row in warrants:
            F.fields(row, ("warrant", "resolutions"))
            kind, handle, raw, unused = self._warrant(row["warrant"])
            self._charge(raw)
            if row["resolutions"] is not None:
                self._charge(C.canonical([[list(exact), choice] for exact, choice in row["resolutions"].items()]))
            if kind == "I": self._session.use_legacy_handle(handle, raw, resolutions=row["resolutions"])
            else: self._session.use_delta_handle(handle, resolutions=row["resolutions"])
        ready, view = self._session.materialize(batch, self._foundation, self._foundation_sha)
        context = AuthorContext(); self._context = context, ready["selection_binding"]
        self._selection_view = view
        return {"context": context, "status": ready["status"], "demands": ready.get("demands", []),
                "cost": ready["cost"], "mathematical_acceptance": False}

    @_action
    def import_context(self, warrants, selected, openings, bodies):
        F.need(self._session is None, "CLIENT_IMPORT_SESSION_ALREADY_CREATED")
        self._session = MixedImportSession(legacy_verifier=self.receipt, delta_verifier=self.delta,
            **self.grant._limits["imports"], wall_seconds=self.grant.remaining_seconds())
        self._counts["new_import_sessions"] += 1
        return self._context_data(warrants, selected, openings, bodies)

    def _live_context(self, context):
        F.need(type(context) is AuthorContext and self._context is not None and self._context[0] is context,
               "CLIENT_FOREIGN_OR_SUPERSEDED_CONTEXT")
        if self._selection_view is None:
            self._session.require_selection(self._context[1])
        else:
            self._session.require_view(self._selection_view)

    @_action
    def extend_context(self, context, *, warrants, selected, openings, bodies):
        self._live_context(context)
        F.need(self._selection_view is None, "CLIENT_READY_CONTEXT_SEALED")
        return self._context_data(warrants, selected, openings, bodies)

    @_action
    def author(self, context, source, roots, *, cpu_seconds, wall_seconds, memory_mib=2048):
        self._live_context(context); F.need(self.preparation is not None, "CLIENT_AUTHOR_OWNER_NOT_SELECTED")
        F.need(type(source) is str, "CLIENT_SOURCE_TEXT"); self._charge(source.encode("utf-8"))
        self._charge(C.canonical(roots))
        operation = MixedSourceOperation(self._session, self._foundation, self._foundation_sha,
                                         source, roots, envelope=self.workspace._envelope,
                                         view=self._selection_view)
        try:
            self._counts["author_calls"] += 1
            return self.preparation.author(operation, "author-"+str(self._counts["author_calls"]),
                cpu_seconds=cpu_seconds, wall_seconds=min(wall_seconds, self.grant.remaining_seconds()),
                memory_mib=memory_mib)
        finally: operation.close()

    def _semantic_plan(self, raw):
        unused, unused2, witnesses, census = parse_packet(raw, self.workspace._envelope, aggregate_image=None)
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
        """Expose available formal data from the actual admitted packet, never new authority."""
        kind, unused_handle, raw, live = self._warrant(token)
        if kind == "I":
            return {"status": "NEED_CALLER_OR_PROVIDER_SEMANTICS", "module": live["module"],
                    "openings": [], "bodies": [], "mathematical_acceptance": False}
        self._charge(raw)
        unused_summary, groups, values, census = self._semantic_plan(raw)
        openings, bodies, missing, seen = [], [], [], set()
        data_bytes = 0
        def reserve_data(size):
            nonlocal data_bytes
            data_bytes += size
            F.need(data_bytes <= self.grant._limits["imports"]["data_bytes"],
                   "CLIENT_SEMANTIC_MATERIAL_DATA_LIMIT")
        for (module, unused_index), encoded in sorted(groups.items()):
            reserve_data(len(encoded)+len(C.canonical({"module": module, "opening": None})))
            opening = C.parse_json(encoded); openings.append({"module": module, "opening": opening})
            for declaration in opening["group"]["declarations"]:
                for digest in sorted(permitted_hashes(declaration)):
                    key = declaration["universes"], digest
                    address = module, *key
                    if address in seen: continue
                    seen.add(address)
                    if key in values:
                        reserve_data(len(values[key])+len(C.canonical({"module": module,
                            "universes": key[0], "expression": None})))
                        bodies.append({"module": module, "universes": key[0],
                                       "expression": C.parse_json(values[key])})
                    else:
                        demand = {"module": module, "name": declaration["name"],
                                  "universes": key[0], "body_hash": digest}
                        reserve_data(len(C.canonical(demand))); missing.append(demand)
        return {"status": "AVAILABLE_PACKET_SEMANTICS", "openings": openings, "bodies": bodies,
                "unavailable_committed_bodies": missing, "census": census,
                "material_rows_bytes_upper_bound": data_bytes,
                "all_future_bodies_covered": False, "mathematical_acceptance": False}

    def _publish(self, raw, export_names, retention_policy, reconciles=None):
        self._charge(raw)
        F.need(retention_policy == {"mode": "quota-bounded-local-custody"}, "CLIENT_RETENTION_POLICY")
        F.need(type(export_names) is list and len(export_names) <= 16384, "CLIENT_EXPORT_NAMES")
        self._charge(C.canonical(export_names))
        summary, groups, values, census = self._semantic_plan(raw); module = C.summary_id(summary)
        keys = [C.name_key(name) for name in export_names]
        F.need(len(keys) == len(set(keys)), "CLIENT_DUPLICATE_EXPORT")
        available = {C.name_key(d["name"]) for (owner, unused), encoded in groups.items() if owner == module
                     for d in C.parse_json(encoded)["group"]["declarations"]}
        F.need(set(keys) <= available, "CLIENT_EXPORT_NOT_TARGET_DECLARATION")
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
        self._counts["publication_attempts"] += 1
        self._publications.append(identifier)
        try:
            self._store(self.workspace.packets.put, module, raw, before_commit=self._active)
            F.need(self._store(self.workspace.packets.get, intent["packet_sha256"], len(raw)) == raw,
                   "CLIENT_PUBLICATION_PACKET_READBACK")
            outcome["phase"] = "PACKET_READ_BACK"; save()
            for (owner, index), encoded in sorted(groups.items()):
                opening = C.parse_json(encoded)
                self._store(self.workspace.modules.put_group, owner, opening, before_commit=self._active)
                for declaration in opening["group"]["declarations"]:
                    held, unused = self._store(self.workspace.modules.get_group, owner, declaration["name"], index)
                    F.need(held == opening, "CLIENT_PUBLICATION_GROUP_READBACK")
                    for digest in sorted(permitted_hashes(declaration)):
                        key = declaration["universes"], digest
                        if key not in values: outcome["missing_bodies"] += 1; continue
                        response = {"schema": BODY_SCHEMA, "module_id": owner,
                            "relative_name": declaration["name"], "universes": key[0], "body_hash": digest,
                            "expression": C.parse_json(values[key])}
                        self._store(self.workspace.modules.put_body, owner, declaration["name"], response,
                                    before_commit=self._active)
                        F.need(self._store(self.workspace.modules.get_body, owner, declaration["name"], *key)
                               == response, "CLIENT_PUBLICATION_BODY_READBACK")
                        outcome["bodies"] += 1
                outcome["groups"] += 1
            outcome["phase"] = "SELECTED_SEMANTICS_READ_BACK"; save()
            for name in export_names:
                opening, unused = self._store(self.workspace.modules.get_group, module, name)
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

    @_action
    def publish(self, packet, export_names, *, retention_policy):
        return self._publish(packet, export_names, retention_policy)

    @_action
    def reconcile(self, publication_id):
        F.hexid(publication_id)
        row = self.workspace.db.execute("SELECT operation,intent FROM publications WHERE id=?",
                                         (publication_id,)).fetchone()
        F.need(row is not None and row[0] != self.grant.identifier, "CLIENT_RECONCILE_PRIOR_OPERATION_REQUIRED")
        intent = C.parse_json(bytes(row[1]))
        raw = self._store(self.workspace.packets.get, intent["packet_sha256"], intent["packet_bytes"])
        return self._publish(raw, intent["export_names"], intent["retention_policy"], reconciles=publication_id)

    def report(self):
        return {"schema": "DMKN_V5_CLIENT_REPORT_V1", "operation_id": self.grant.identifier,
            "status": self._state, "closed": self._closed, "wire_profile_id": self.workspace.packets.profile_id,
            "owner_profiles": list(self._profiles), "grant": self.grant.limits,
            "calls": self._calls, "submitted_input_bytes": self._input_bytes, "counts": dict(self._counts),
            "input_byte_scope": "SUBMITTED_OR_RELOADED_EVIDENCE_FOUNDATION_SOURCE_QUERY_RECORDS_AND_CONTEXT_DATA;"
                                "FORMAL_ROOT_AND_EXPORT_SELECTIONS_INCLUDED;"
                                "REPEATS_CHARGED_NOT_PHYSICAL_TRANSFER_BYTES;CONTROL_METADATA_EXCLUDED",
            "observed_controller_cpu_since_grant": time.process_time()-self.grant._cpu,
            "wall_since_grant": time.monotonic()-self.grant.started,
            "acquisition": self._budget.report(), "receipt": self.receipt.report(), "mixed": self.delta.report(),
            "preparation": None if self.preparation is None else self.preparation.report(),
            "search": None if self._search is None else self._search.report(),
            "location": None if self._handoff is None else self._handoff.location.report(),
            "transport": None if self._acquisition is None else self._acquisition.report(),
            "publications": list(self._publications), "failures": list(self._failures),
            "cost_scope": "CONTROLLER_INCLUSIVE_SINCE_GRANT;NESTED_WORKERS_NOT_ADDITIVE_TOTAL",
            "unknowns": ["enclosing_Job_total_supplied_by_caller", "failed_worker_cost_may_be_unknown",
                         "final_report_and_exit_tail", "provider_costs", "DHT_wire_bytes"],
            "hard_containment": "TRUSTED_CALLER_ACTUAL_ENCLOSING_JOB_REQUIRED",
            "mathematical_acceptance": False}

    async def close(self):
        if self._closed: return self.report()
        F.need(not self._busy, "CLIENT_CANCEL_AND_AWAIT_ACTIVE_CALL_BEFORE_CLOSE")
        errors = []
        for owner in (self._session, self.preparation):
            if owner is not None:
                try: owner.close()
                except BaseException as error: errors.append(type(error).__name__+":"+str(error)[:300])
        if self._acquisition is not None:
            try: self._acquisition.close()
            except BaseException as error: errors.append(type(error).__name__+":"+str(error)[:300])
        else:
            self._budget.closed = True
            try: self.delta.close()
            except BaseException as error: errors.append(type(error).__name__+":"+str(error)[:300])
        try: self.receipt.close()
        except BaseException as error: errors.append(type(error).__name__+":"+str(error)[:300])
        if self._channel is not None:
            try: await self._channel.close()
            except BaseException as error: errors.append(type(error).__name__+":"+str(error)[:300])
        self._warrants.clear(); self._candidates.clear(); self._context = None
        self._selection_view = None
        self._receipt_cache.clear(); self._packet_cache.clear()
        if errors: self._failures.extend(errors); self._state = "CLEANUP_INCOMPLETE"
        elif self._state == "OPEN": self._state = "CLOSED"
        self._closed = True
        try:
            report = self.report()
            self.workspace._record(self.grant.identifier, self._state, report)
            return report
        except BaseException:
            self._failures.append("final_report_not_persisted")
            self._state = "CLOSED_REPORT_UNCERTAIN"
            self.workspace._poisoned = True
            raise
        finally:
            if errors: self.workspace._poisoned = True
            self.workspace._client = None; self.workspace._grants.pop(self.grant, None)

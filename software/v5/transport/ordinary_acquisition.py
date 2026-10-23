"""Bounded ordinary preview/evidence acquisition and inert byte custody.

Two explicit byte fetches plus exact export lookup; no automatic ancestry,
retries, source/native loading,
certificates or mathematical adoption. Caller supplies one absolute parent
deadline and serialized owner calls. Existing HTTP exchange owns Endpoint/TLS
and connection closure; its extra <=1s best-effort cleanup needs a separate outer
allowance. Soft checks here do not replace hard process/resource containment.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import math
import os
from pathlib import Path
import sqlite3
import time

from discovery import formal_features as F
from discovery.discovery_store import ordinary
from . import http_provider as H
from .clients import configured


PREVIEW_ROUTE = H.ORDINARY_PREVIEW_ROUTE
EVIDENCE_ROUTE = H.ORDINARY_EVIDENCE_ROUTE
LOCATOR_ROUTE = H.ORDINARY_LOCATOR_ROUTE
PREVIEW_REQUEST = "DMKN_ORDINARY_PREVIEW_REQUEST_V1"
EVIDENCE_REQUEST = "DMKN_ORDINARY_EVIDENCE_REQUEST_V1"
LOCATOR_REQUEST = "DMKN_ORDINARY_LOCATOR_REQUEST_V1"
PREVIEW_MAX, EVIDENCE_MAX = H.ROUTES[PREVIEW_ROUTE], H.ROUTES[EVIDENCE_ROUTE]
LOCATOR_MAX = H.ROUTES[LOCATOR_ROUTE]
STORE_SCHEMA = "DMKN_ORDINARY_INERT_CUSTODY_V1"
STORE_LIMITS = {"objects": (1, 1000000), "exports": (1, 16000000), "logical_bytes": (1024, 2**40),
                "db_pages": (256, 268435456)}


def request_limit(route, request):
    """Exact wire shape and body cap; no URI, native path or remote code field."""
    if route == PREVIEW_ROUTE:
        F.fields(request, ("schema", "object_sha256", "object_bytes"))
        F.need(request["schema"] == PREVIEW_REQUEST, "ORDINARY_PREVIEW_REQUEST_SCHEMA")
        F.hexid(request["object_sha256"])
        return F.uint(request["object_bytes"], 1, PREVIEW_MAX, "ORDINARY_PREVIEW_BYTES")
    if route == LOCATOR_ROUTE:
        F.fields(request, ("schema", "semantic_id", "export_id", "max_bytes"))
        F.need(request["schema"] == LOCATOR_REQUEST, "ORDINARY_LOCATOR_REQUEST_SCHEMA")
        F.hexid(request["semantic_id"]); F.hexid(request["export_id"])
        return F.uint(request["max_bytes"], 1, LOCATOR_MAX, "ORDINARY_LOCATOR_BYTES")
    F.need(route == EVIDENCE_ROUTE, "ORDINARY_ACQUISITION_ROUTE")
    F.fields(request, ("schema", "semantic_id", "unit_id", "max_bytes"))
    F.need(request["schema"] == EVIDENCE_REQUEST, "ORDINARY_EVIDENCE_REQUEST_SCHEMA")
    F.hexid(request["semantic_id"]); F.hexid(request["unit_id"])
    return F.uint(request["max_bytes"], 1, EVIDENCE_MAX, "ORDINARY_EVIDENCE_BYTES")


def _check(callback):
    if callback is not None:
        callback()


class OrdinaryStore:
    """One owner-local durable byte store, not a catalog of accepted judgments.

    No module/receipt schema is reused. Exact bounded canonical objects are
    stored with exact export locators in SQLite with DELETE/FULL and finite physical/logical
    quotas. Protected owner/OS paths, serialized calls and no external database
    mutation are premises. Reopen requires the same S/limits, not a new warrant.
    """
    def __init__(self, root, semantic_id, limits, *, create=False):
        F.need(type(create) is bool, "ORDINARY_CUSTODY_CREATE")
        F.fields(limits, STORE_LIMITS)
        for key, bounds in STORE_LIMITS.items():
            F.uint(limits[key], *bounds, "ORDINARY_CUSTODY_LIMIT:"+key)
        self.semantic_id, self.limits = F.hexid(semantic_id), dict(limits)
        self.root, self.db = ordinary(root, fresh=create), None
        if create:
            self.root.mkdir()
        path = ordinary(self.root / "ordinary.sqlite", fresh=create, directory=False)
        maximum = self.limits["db_pages"]*4096
        if not create:
            F.need(path.stat().st_nlink == 1 and path.stat().st_size <= maximum,
                   "ORDINARY_CUSTODY_DATABASE_BOUND")
        for suffix in ("-wal", "-shm"):
            F.need(not os.path.lexists(str(path)+suffix), "ORDINARY_CUSTODY_SIDECAR")
        journal = Path(str(path)+"-journal")
        if os.path.lexists(journal):
            F.need(not create, "ORDINARY_CUSTODY_FRESH_JOURNAL")
            ordinary(journal, directory=False)
            F.need(journal.stat().st_nlink == 1 and journal.stat().st_size <= 2*maximum+1048576,
                   "ORDINARY_CUSTODY_JOURNAL_BOUND")
        cfg = F.compact({"schema": STORE_SCHEMA, "semantic_id": self.semantic_id, "limits": self.limits})
        try:
            self.db = sqlite3.connect(path, timeout=1, isolation_level=None)
            for pragma in ("trusted_schema=OFF", "journal_mode=DELETE", "synchronous=FULL",
                           "temp_store=MEMORY", "mmap_size=0", "cache_size=-2048"):
                self.db.execute("PRAGMA "+pragma)
            F.need(self.db.execute("PRAGMA page_size").fetchone()[0] == 4096,
                   "ORDINARY_CUSTODY_PAGE_SIZE")
            F.need(self.db.execute("PRAGMA max_page_count="+str(self.limits["db_pages"])).fetchone()[0]
                   == self.limits["db_pages"], "ORDINARY_CUSTODY_DATABASE_CAP")
            if create:
                self.db.executescript("""
                    BEGIN IMMEDIATE;
                    CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), cfg BLOB NOT NULL,
                        objects INTEGER NOT NULL, exports INTEGER NOT NULL, logical_bytes INTEGER NOT NULL);
                    CREATE TABLE objects(kind TEXT NOT NULL, identity TEXT NOT NULL,
                        raw_sha256 TEXT NOT NULL, raw BLOB NOT NULL,
                        PRIMARY KEY(kind,identity)) WITHOUT ROWID;
                    CREATE TABLE exports(export_id TEXT PRIMARY KEY, unit_id TEXT NOT NULL,
                        locator BLOB NOT NULL) WITHOUT ROWID;
                    COMMIT;
                """)
                self.db.execute("INSERT INTO meta VALUES(1,?,0,0,0)", (cfg,))
            row = self.db.execute("SELECT cfg FROM meta WHERE id=1").fetchone()
            F.need(row is not None and bytes(row[0]) == cfg, "ORDINARY_CUSTODY_CONFIG")
            self.status()
        except BaseException:
            self.close()
            raise

    def close(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    def _active(self):
        F.need(self.db is not None, "ORDINARY_CUSTODY_CLOSED")

    def status(self):
        self._active()
        row = self.db.execute("SELECT objects,exports,logical_bytes FROM meta WHERE id=1").fetchone()
        F.need(row is not None, "ORDINARY_CUSTODY_META")
        counts = dict(zip(("objects", "exports", "logical_bytes"), row))
        for key, value in counts.items():
            F.uint(value, 0, self.limits[key], "ORDINARY_CUSTODY_STORED_QUOTA")
        return {"semantic_id": self.semantic_id, "counts": counts, "mathematical_acceptance": False}

    def _validate(self, kind, raw):
        F.need(type(raw) is bytes, "ORDINARY_CUSTODY_RAW_BYTES")
        if kind == "preview":
            import portable_preview as P
            F.uint(len(raw), 1, PREVIEW_MAX, "ORDINARY_PREVIEW_BYTES")
            parsed = P.read_preview(raw)
            identity = hashlib.sha256(raw).hexdigest()
        else:
            import portable_evidence as E
            F.need(kind == "evidence", "ORDINARY_CUSTODY_KIND")
            F.uint(len(raw), 1, EVIDENCE_MAX, "ORDINARY_EVIDENCE_BYTES")
            parsed = E.read_evidence(raw)
            identity = parsed.unit_id
        F.need(parsed.document["semantic_id"] == self.semantic_id, "ORDINARY_CUSTODY_SEMANTICS")
        return identity, hashlib.sha256(raw).hexdigest(), parsed

    def _export_locators(self, parsed, check_budget):
        """Project every actual output, or refuse the whole inert put; no omissions."""
        import portable_preview as P
        import portable_evidence as E
        result = []
        for output in parsed.document["unit"][2]:
            _check(check_budget)
            locator = P.read_locator({"schema": P.LOCATOR_SCHEMA, "semantic_id": self.semantic_id,
                                      "unit_id": parsed.unit_id, "export_name": output[0]})
            raw = F.compact(locator)
            F.uint(len(raw), 1, LOCATOR_MAX, "ORDINARY_LOCATOR_BYTES")
            identity = E.export_id(self.semantic_id, parsed.unit_id, locator["export_name"])
            result.append((identity, raw))
        return result

    def _put(self, kind, raw, before_commit):
        self._active(); _check(before_commit)
        identity, digest, parsed = self._validate(kind, raw)
        locators = self._export_locators(parsed, before_commit) if kind == "evidence" else []
        _check(before_commit)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            old = self.db.execute("SELECT length(raw),raw_sha256 FROM objects WHERE kind=? AND identity=?",
                                  (kind, identity)).fetchone()
            if old is not None:
                F.need(old == (len(raw), digest), "ORDINARY_CUSTODY_CONFLICT")
                held = self.db.execute("SELECT raw FROM objects WHERE kind=? AND identity=?",
                                       (kind, identity)).fetchone()
                F.need(held is not None and bytes(held[0]) == raw, "ORDINARY_CUSTODY_CONFLICT")
                for export, locator_raw in locators:
                    _check(before_commit)
                    held = self.db.execute("SELECT unit_id,locator FROM exports WHERE export_id=?", (export,)).fetchone()
                    F.need(held == (identity, locator_raw), "ORDINARY_CUSTODY_EXPORT_BINDING")
            else:
                counts = self.status()["counts"]
                charge = len(raw)+len(kind)+128+sum(128+len(value) for _, value in locators)
                F.need(counts["objects"]+1 <= self.limits["objects"] and
                       counts["exports"]+len(locators) <= self.limits["exports"] and
                       counts["logical_bytes"]+charge <= self.limits["logical_bytes"], "ORDINARY_CUSTODY_QUOTA")
                self.db.execute("INSERT INTO objects VALUES(?,?,?,?)", (kind, identity, digest, raw))
                for export, locator_raw in locators:
                    _check(before_commit)
                    self.db.execute("INSERT INTO exports VALUES(?,?,?)", (export, identity, locator_raw))
                self.db.execute("UPDATE meta SET objects=objects+1,exports=exports+?,logical_bytes=logical_bytes+? WHERE id=1",
                                (len(locators), charge))
            _check(before_commit)
            self.db.execute("COMMIT")
        except BaseException:
            if self.db.in_transaction:
                self.db.execute("ROLLBACK")
            raise
        return {"new": old is None, "semantic_id": self.semantic_id, "identity": identity,
                "raw_sha256": digest, "raw_bytes": len(raw), "mathematical_acceptance": False}

    def put_preview(self, raw, *, before_commit=None):
        return self._put("preview", raw, before_commit)

    def put_evidence(self, raw, *, before_commit=None):
        return self._put("evidence", raw, before_commit)

    def _get(self, kind, identity, maximum, check_budget):
        self._active(); F.hexid(identity); _check(check_budget)
        row = self.db.execute("SELECT length(raw),raw_sha256 FROM objects WHERE kind=? AND identity=?",
                              (kind, identity)).fetchone()
        F.need(row is not None, "ORDINARY_OBJECT_UNAVAILABLE")
        F.uint(row[0], 1, maximum, "ORDINARY_CUSTODY_OBJECT_BOUND")
        # Length is checked before materializing the bounded SQLite BLOB.
        held = self.db.execute("SELECT raw FROM objects WHERE kind=? AND identity=?",
                               (kind, identity)).fetchone()
        F.need(held is not None, "ORDINARY_OBJECT_UNAVAILABLE")
        raw = bytes(held[0])
        digest = hashlib.sha256(raw).hexdigest()
        if kind == "preview":
            content_id = digest
        else:
            import portable_evidence as E
            F.need(kind == "evidence", "ORDINARY_CUSTODY_KIND")
            hashed = hashlib.sha256(E.EVIDENCE_DOMAIN.encode("ascii")+b"\0")
            hashed.update(raw)
            content_id = hashed.hexdigest()
        # The owner validated syntax/S once at put. Under the protected database
        # premise, cold serving needs exact raw/content hashing, not repeated DAG
        # census. Every receiving client still parses its selected remote unit.
        F.need(len(raw) == row[0] and digest == row[1] and content_id == identity,
               "ORDINARY_CUSTODY_EXACT_BINDING")
        _check(check_budget)
        return raw

    def get_preview(self, digest, count, *, check_budget=None):
        F.hexid(digest); F.uint(count, 1, PREVIEW_MAX, "ORDINARY_PREVIEW_BYTES")
        raw = self._get("preview", digest, count, check_budget)
        F.need(len(raw) == count, "ORDINARY_PREVIEW_EXACT_SIZE")
        return raw

    def get_evidence(self, semantic_id, unit_id, max_bytes, *, check_budget=None):
        F.need(F.hexid(semantic_id) == self.semantic_id, "ORDINARY_CUSTODY_SEMANTICS")
        F.uint(max_bytes, 1, EVIDENCE_MAX, "ORDINARY_EVIDENCE_BYTES")
        return self._get("evidence", F.hexid(unit_id), max_bytes, check_budget)

    def get_locator(self, semantic_id, export_id, max_bytes, *, check_budget=None):
        """Exact export lookup, not original-name/semantic search or acceptance."""
        import portable_preview as P
        import ordinary_evidence as E
        import ordinary_semantics as S
        self._active(); _check(check_budget)
        F.need(F.hexid(semantic_id) == self.semantic_id, "ORDINARY_CUSTODY_SEMANTICS")
        F.hexid(export_id); F.uint(max_bytes, 1, LOCATOR_MAX, "ORDINARY_LOCATOR_BYTES")
        row = self.db.execute("SELECT unit_id,length(locator) FROM exports WHERE export_id=?", (export_id,)).fetchone()
        F.need(row is not None, "ORDINARY_EXPORT_LOCALLY_UNAVAILABLE")
        F.uint(row[1], 1, max_bytes, "ORDINARY_LOCATOR_BYTES")
        held = self.db.execute("SELECT locator FROM exports WHERE export_id=?", (export_id,)).fetchone()
        F.need(held is not None, "ORDINARY_EXPORT_LOCALLY_UNAVAILABLE")
        raw = bytes(held[0])
        F.need(len(raw) == row[1], "ORDINARY_CUSTODY_EXPORT_BINDING")
        locator = P.read_locator(E.strict_json(raw, P.DEFAULT_LIMITS.codec))
        F.need(locator["semantic_id"] == semantic_id and locator["unit_id"] == row[0] and
               S.export_id(semantic_id, row[0], locator["export_name"]) == export_id,
               "ORDINARY_CUSTODY_EXPORT_BINDING")
        retained = self.db.execute("SELECT length(raw) FROM objects WHERE kind='evidence' AND identity=?",
                                   (row[0],)).fetchone()
        F.need(retained is not None, "ORDINARY_OBJECT_UNAVAILABLE")
        F.uint(retained[0], 1, EVIDENCE_MAX, "ORDINARY_CUSTODY_OBJECT_BOUND")
        _check(check_budget)
        return raw


def serve(store, route, request, *, check_budget=None):
    """Optional Provider role. No remote writes or mathematical authority."""
    F.need(type(store) is OrdinaryStore, "ORDINARY_CUSTODY_ROLE")
    request_limit(route, request); _check(check_budget)
    if route == PREVIEW_ROUTE:
        return store.get_preview(request["object_sha256"], request["object_bytes"], check_budget=check_budget)
    if route == LOCATOR_ROUTE:
        return store.get_locator(request["semantic_id"], request["export_id"], request["max_bytes"],
                                 check_budget=check_budget)
    return store.get_evidence(request["semantic_id"], request["unit_id"], request["max_bytes"],
                              check_budget=check_budget)


class OrdinaryBudget:
    """One nonrenewing owner budget shared by both fetch kinds, lookups and providers.

    Search/location suballocations may be prepaid before any fetch. Reply-byte
    budget excludes request/header overhead, which report() bounds separately.
    Every begun attempt consumes a request; failures charge its full reply cap.
    """
    def __init__(self, *, deadline, requests, reply_bytes):
        F.need(type(deadline) in (int, float) and math.isfinite(deadline) and
               time.monotonic() < deadline <= time.monotonic()+3600, "ORDINARY_PARENT_DEADLINE")
        F.uint(requests, 1, 8192, "ORDINARY_ACQUISITION_REQUESTS")
        F.uint(reply_bytes, 1, 1024**3, "ORDINARY_ACQUISITION_BYTES")
        self.deadline, self.request_cap, self.byte_cap = deadline, requests, reply_bytes
        self.requests = self.reply_bytes = self.sequence = 0
        self.pending, self.closed, self.external = None, False, []

    def active(self):
        F.need(not self.closed and time.monotonic() < self.deadline, "ORDINARY_BUDGET_CLOSED_OR_EXPIRED")

    def charge_external(self, label, requests, reply_bytes):
        """Prepay bounded search/location work; caller enforces that subbudget."""
        self.active()
        F.need(self.pending is None and self.sequence == 0, "ORDINARY_PREALLOCATION_PHASE")
        F.need(type(label) is str and 0 < len(label) <= 64 and len(self.external) < 8 and
               label not in [row["label"] for row in self.external], "ORDINARY_EXTERNAL_LABEL")
        F.uint(requests, 0, self.request_cap); F.uint(reply_bytes, 0, self.byte_cap)
        F.need(self.requests+requests <= self.request_cap and self.reply_bytes+reply_bytes <= self.byte_cap,
               "ORDINARY_AGGREGATE_BUDGET")
        self.requests += requests; self.reply_bytes += reply_bytes
        self.external.append({"label": label, "requests": requests, "reply_bytes": reply_bytes})

    def begin(self, maximum):
        self.active(); F.uint(maximum, 1, EVIDENCE_MAX, "ORDINARY_ACQUISITION_OBJECT_BOUND")
        F.need(self.pending is None and self.requests < self.request_cap and
               self.reply_bytes+maximum <= self.byte_cap, "ORDINARY_AGGREGATE_BUDGET")
        self.requests += 1; self.sequence += 1
        self.pending = (self.sequence, maximum)
        return self.sequence

    def settle(self, ticket, count=None):
        F.need(self.pending is not None and ticket == self.pending[0], "ORDINARY_PRIVATE_TICKET")
        maximum = self.pending[1]
        if count is None:
            count = maximum
        F.uint(count, 0, maximum, "ORDINARY_SETTLEMENT_BYTES")
        self.reply_bytes += count; self.pending = None

    def remaining_ms(self):
        self.active()
        remaining = int((self.deadline-time.monotonic())*1000)
        F.need(remaining > 0, "ORDINARY_BUDGET_CLOSED_OR_EXPIRED")
        return min(60000, remaining)

    def close(self):
        F.need(self.pending is None, "ORDINARY_REQUEST_PENDING")
        self.closed = True

    def report(self):
        return {"requests": self.requests, "charged_reply_bytes": self.reply_bytes,
                "reserved_reply_bytes": 0 if self.pending is None else self.pending[1],
                "pending_requests": int(self.pending is not None), "external_prepaid": deepcopy(self.external),
                "remaining_ms": max(0, int((self.deadline-time.monotonic())*1000)),
                "closed": self.closed, "mathematical_acceptance": False}


class OrdinaryAcquisition:
    """Explicit typed reads into optional inert custody, not native admission."""
    def __init__(self, adapter, endpoints, budget, *, local_custody=None):
        from discovery.ordinary_export_adapter import OrdinaryExportAdapter
        F.need(type(adapter) is OrdinaryExportAdapter and type(budget) is OrdinaryBudget,
               "ORDINARY_ACQUISITION_OWNER_TYPES")
        budget.active()
        F.need(local_custody is None or (type(local_custody) is OrdinaryStore and
               local_custody.semantic_id == adapter.semantic_id), "ORDINARY_ACQUISITION_CUSTODY")
        self.adapter, self.budget, self.endpoints = adapter, budget, configured(endpoints)
        self.local_custody = local_custody
        self.http = {"completed_responses": 0, "failed_attempts": 0, "actual_request_bytes": 0,
                     "actual_reply_bytes": 0, "actual_header_bytes": 0,
                     "request_body_upper_bound": 0, "header_upper_bound": 0}

    async def _fetch(self, provider, route, request, validate, retain):
        F.need(provider in self.endpoints, "ENDPOINT_NOT_CONFIGURED")
        maximum = request_limit(route, request)
        ticket = self.budget.begin(maximum)
        self.http["request_body_upper_bound"] += H.REQUEST_MAX
        self.http["header_upper_bound"] += 2*H.HEADER_MAX
        charged = None
        try:
            response = await H.exchange(self.endpoints[provider], route, request, maximum, self.budget.remaining_ms())
            self.http["completed_responses"] += 1
            for source, target in (("request_bytes", "actual_request_bytes"),
                                   ("reply_bytes", "actual_reply_bytes"), ("header_bytes", "actual_header_bytes")):
                self.http[target] += response[source]
            F.need(response["status"] == 200, "ORDINARY_ACQUISITION_HTTP_STATUS")
            self.budget.active()
            raw = response["raw"]
            result = validate(raw)
            self.budget.active()
            if retain is not None:
                retain(raw, before_commit=self.budget.active)
            self.budget.active()
            charged = len(raw)
            return {**result, "raw": raw, "mathematical_acceptance": False}
        except BaseException:
            self.http["failed_attempts"] += 1
            raise
        finally:
            self.budget.settle(ticket, charged)

    async def preview(self, provider, record):
        """Fetch by advertised hash/size; recompute the entire exact record."""
        selected = deepcopy(record)
        F.validate_record(selected, self.adapter.namespace)
        F.need(selected["schema"] == F.ORDINARY_EXPORT_RECORD_SCHEMA, "ORDINARY_ACQUISITION_RECORD")
        request = {"schema": PREVIEW_REQUEST, "object_sha256": selected["object_sha256"],
                   "object_bytes": selected["object_bytes"]}
        def validate(raw):
            F.need(len(raw) == selected["object_bytes"] and hashlib.sha256(raw).hexdigest() ==
                   selected["object_sha256"], "ORDINARY_PREVIEW_EXACT_BYTES")
            return self.adapter.resolve(selected, raw)
        retain = None if self.local_custody is None else self.local_custody.put_preview
        return await self._fetch(provider, PREVIEW_ROUTE, request, validate, retain)

    async def locator(self, provider, semantic_id, export_id, max_bytes=LOCATOR_MAX, *, expected_name=None):
        """Find a claimed UnitID/name for one known ExportID; fetch nothing else."""
        import ordinary_evidence as E
        import portable_preview as P
        import ordinary_semantics as S
        F.need(F.hexid(semantic_id) == self.adapter.semantic_id, "ORDINARY_ACQUISITION_SEMANTICS")
        expected_key = None if expected_name is None else E.name_key(expected_name, P.DEFAULT_LIMITS.codec)
        request = {"schema": LOCATOR_REQUEST, "semantic_id": semantic_id,
                   "export_id": F.hexid(export_id), "max_bytes": max_bytes}
        def validate(raw):
            locator = P.read_locator(E.strict_json(raw, P.DEFAULT_LIMITS.codec))
            F.need(locator["semantic_id"] == semantic_id and
                   S.export_id(semantic_id, locator["unit_id"], locator["export_name"]) == export_id,
                   "ORDINARY_LOCATOR_EXACT_EXPORT")
            F.need(expected_key is None or E.name_key(locator["export_name"]) == expected_key,
                   "ORDINARY_LOCATOR_EXPECTED_NAME")
            return {"export_id": export_id, "locator": locator,
                    "assurance": "EXACT_EXPORT_LOCATOR_NOT_OUTPUT_CENSUS_OR_MATHEMATICAL_ACCEPTANCE"}
        return await self._fetch(provider, LOCATOR_ROUTE, request, validate, None)

    async def evidence(self, provider, semantic_id, unit_id, max_bytes, *,
                       expected_export_id=None, expected_export_name=None):
        """Fetch one exact unit; no dependencies are fetched or warranted."""
        import portable_evidence as E
        import ordinary_evidence as OE
        F.need(F.hexid(semantic_id) == self.adapter.semantic_id, "ORDINARY_ACQUISITION_SEMANTICS")
        F.need((expected_export_id is None) == (expected_export_name is None), "ORDINARY_EXPECTED_EXPORT_PAIR")
        export_name_key = None
        if expected_export_id is not None:
            F.hexid(expected_export_id)
            export_name_key = OE.name_key(expected_export_name)
            F.need(E.export_id(semantic_id, unit_id, OE.strict_json(export_name_key)) == expected_export_id,
                   "ORDINARY_EXPECTED_EXPORT_LOCATOR")
        request = {"schema": EVIDENCE_REQUEST, "semantic_id": semantic_id,
                   "unit_id": F.hexid(unit_id), "max_bytes": max_bytes}
        def validate(raw):
            exact = E.read_evidence(raw)
            F.need(exact.document["semantic_id"] == semantic_id and exact.unit_id == unit_id,
                   "ORDINARY_EVIDENCE_EXACT_ID")
            if export_name_key is not None:
                F.need(any(OE.name_key(row[0]) == export_name_key for row in exact.document["unit"][2]),
                       "ORDINARY_EVIDENCE_EXPORT_OMISSION")
            return {"semantic_id": semantic_id, "unit_id": unit_id,
                    "raw_sha256": hashlib.sha256(raw).hexdigest(), "raw_bytes": len(raw),
                    "assurance": "EXACT_PORTABLE_INERT_EVIDENCE_NOT_MATHEMATICAL_ACCEPTANCE"}
        retain = None if self.local_custody is None else self.local_custody.put_evidence
        return await self._fetch(provider, EVIDENCE_ROUTE, request, validate, retain)

    def report(self):
        return {"budget": self.budget.report(), "http": dict(self.http), "mathematical_acceptance": False}

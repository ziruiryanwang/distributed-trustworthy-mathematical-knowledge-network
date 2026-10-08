"""Bounded positive-only candidates, separate from authenticated scan coverage.

The owner must serialize Store access and lend its otherwise unused SQLite
progress handler for this call. No write/schema/commitment change occurs. The
handler is removed and busy_timeout restored in finally. Fixed three connection
control PRAGMAs are outside the data-query VM allowance. Hard process/memory
containment is still required; monotonic deadlines are cooperative, not real-time.

Data SQL reserves100 VM instructions before each statement and each next callback
block. This deliberately overcharges partial blocks; it is an upper allowance,
not an exact instruction count. SQLite/proof counters sent by a remote provider
are claims, not independently authenticated work. Positive proof membership is
authenticated; continuation and termination never prove a skipped interval.
"""
from copy import deepcopy
import sqlite3
import time

from . import authenticated_index as A
from . import discovery_query as Q
from . import formal_features as F

LIMITS = {"scanned": (1, 4096), "matches": (1, 8), "bytes": (2048, 1048576),
          "timeout_ms": (1, 1000), "record_probes": (1, 65536),
          "node_reads": (1, 100000), "hash_calls": (1, 2000000),
          "sql_vm_steps": (100, 10000000)}
TERMINATIONS = ("anchor_boundary", "scanned_exhausted", "matches_exhausted", "bytes_exhausted",
                "time_exhausted", "record_probes_exhausted", "node_reads_exhausted",
                "hash_calls_exhausted", "sql_vm_steps_exhausted")
CHARGES = ("scanned", "record_probes", "node_reads", "hash_calls", "sql_vm_steps",
           "record_loads", "proofs")
CLAIM = "POSITIVE_MATCHES_ONLY_NO_VERIFIED_SCAN_COVERAGE"


def validate_request(request, namespace=None):
    F.fields(request, ("schema", "namespace", "snapshot_id", "features", "partition", "anchor", "start", "limits"))
    F.need(request["schema"] == "DMKN_FORMAL_CANDIDATE_REQUEST_V1", "CANDIDATE_REQUEST_SCHEMA")
    F.hexid(request["namespace"]); F.hexid(request["snapshot_id"]); F.hexid(request["anchor"])
    F.need(namespace is None or request["namespace"] == namespace, "CANDIDATE_NAMESPACE")
    F.validate_features(request["features"], 8)
    F.need(request["anchor"] in request["features"], "CANDIDATE_ANCHOR_FEATURE")
    F.uint(request["partition"], 0, 255, "CANDIDATE_PARTITION")
    F.uint(request["start"], 0, A.MAX_VECTOR, "CANDIDATE_START")
    F.fields(request["limits"], LIMITS)
    for key, (low, high) in LIMITS.items(): F.uint(request["limits"][key], low, high, "CANDIDATE_LIMIT:"+key)
    F.need(len(F.compact(request)) <= 16384, "CANDIDATE_REQUEST_BYTES")
    return request


def cursor(request, query, position):
    return {"schema": "DMKN_FORMAL_CANDIDATE_CURSOR_V1", "snapshot_id": request["snapshot_id"],
            "query_id": query, "partition": request["partition"], "anchor": request["anchor"],
            "next": position, "assurance": "ADVISORY_POSITION_NOT_VERIFIED_COVERAGE"}


class _Stop(Exception):
    pass


class _ReadIO:
    def __init__(self, db, limits, clock):
        self.db, self.limits, self.clock = db, limits, clock
        self.until = clock() + limits["timeout_ms"]/1000
        self.used = {k: 0 for k in CHARGES}
        self.interrupted, self.cache, self.cache_bytes = None, {}, 0

    def live(self):
        if self.clock() >= self.until: raise _Stop("time_exhausted")

    def charge(self, key, amount=1):
        self.live()
        if self.used[key] + amount > self.limits[key]: raise _Stop(key+"_exhausted")
        self.used[key] += amount

    def hash_step(self): self.charge("hash_calls")

    def progress(self):
        try:
            self.charge("sql_vm_steps", 100)
            return 0
        except _Stop as error:
            self.interrupted = str(error)
            return 1

    def one(self, sql, args=(), *, probe=False):
        if probe: self.charge("record_probes")
        self.charge("sql_vm_steps", 100)
        self.interrupted = None
        statement = None
        try:
            statement = self.db.execute(sql, args)
            result = statement.fetchone()
            self.live()
            return result
        except sqlite3.OperationalError:
            if self.interrupted is not None: raise _Stop(self.interrupted) from None
            raise
        finally:
            if statement is not None: statement.close()

    def get_node(self, key):
        self.charge("node_reads"); F.hexid(key)
        if key in self.cache: return deepcopy(self.cache[key])
        row = self.one("SELECT encoded FROM cas_nodes WHERE hash=?", (key,))
        F.need(row is not None, "CANDIDATE_CAS_NODE_MISSING")
        raw = bytes(row[0]); node = F.strict(raw, 4096)
        F.need(A.node_hash(node) == key, "CANDIDATE_CAS_NODE_HASH")
        if len(self.cache) < 512 and self.cache_bytes+len(raw) <= 2097152:
            self.cache[key] = deepcopy(node); self.cache_bytes += len(raw)
        return node


def _finalize(result, request, used):
    result["next_cursor"] = None if result["anchor_count"] == result["next"] else cursor(
        request, result["query_id"], result["next"])
    result["charged"] = dict(used)
    return result


def _wire_upper(result, request):
    """Reserve worst scalar/counter widths, including a non-null cursor."""
    largest = {key: request["limits"].get(key, request["limits"]["scanned"]) for key in CHARGES}
    value = {**result, "next": A.MAX_VECTOR, "anchor_count": A.MAX_VECTOR,
             "next_cursor": cursor(request, result["query_id"], A.MAX_VECTOR),
             "termination": max(TERMINATIONS, key=len), "charged": largest}
    return len(F.compact(value))


def page(store, request, *, clock=None):
    """Return bounded proved hits; caller owns serialized Store/progress handler.

    Exact ordinal driver + secondary membership probes use existing B-trees.
    Only surviving IDs load records/build proofs. Old-cut ceilings apply to all
    feature probes, and admitted_seq also gates the full object read. A returned
    anchor proof authenticates the whole record and therefore its claimed feature
    conjunction, not correctness of feature extraction or non-anchor indexes.
    """
    validate_request(request, store.namespace)
    limits, io = request["limits"], _ReadIO(store.db, request["limits"], clock or time.monotonic)
    # One fixed bounded query-identity hash is counted before any database I/O.
    io.hash_step(); query = Q.query_id(request["namespace"], request["features"])
    result = {"schema": "DMKN_FORMAL_CANDIDATE_PAGE_V1", "namespace": request["namespace"],
              "snapshot_id": request["snapshot_id"], "query_id": query,
              "partition": request["partition"], "anchor": request["anchor"], "start": request["start"],
              "next": request["start"], "anchor_count": None, "hits": [], "next_cursor": None,
              "termination": "anchor_boundary", "charged": {}, "coverage": CLAIM,
              "global_complete": False, "mathematical_acceptance": False}
    F.need(_wire_upper(result, request) <= limits["bytes"], "CANDIDATE_PAGE_TOO_SMALL")
    saved_busy = store.db.execute("PRAGMA busy_timeout").fetchone()[0]
    store.db.execute("PRAGMA busy_timeout=0")
    store.db.set_progress_handler(io.progress, 100)
    try:
        with A.hash_meter(io.hash_step):
            try:
                stored = io.one("SELECT descriptor FROM snapshots WHERE snapshot_id=?", (request["snapshot_id"],))
                F.need(stored is not None, "SNAPSHOT_NOT_RETAINED")
                snapshot = F.strict(bytes(stored[0]), 4096)
                A.validate_snapshot(snapshot, store.namespace)
                F.need(A.snapshot_id(snapshot) == request["snapshot_id"], "CANDIDATE_SNAPSHOT_HASH")
                descriptors = {}
                for feature in request["features"]:
                    root, _ = A.map_get(io, store.namespace, snapshot["feature_map_root"], feature)
                    descriptors[feature] = A.empty_descriptor(store.namespace, feature, request["partition"]) if root is None else (
                        A.partition_get(io, store.namespace, feature, root, request["partition"])[0])
                anchor = min(descriptors, key=lambda f: (descriptors[f]["count"], f))
                part = descriptors[anchor]
                F.need(anchor == request["anchor"], "CANDIDATE_PLANNED_ANCHOR")
                F.uint(request["start"], 0, part["count"], "CANDIDATE_START")
                result["anchor_count"] = part["count"]
                ctx = A.context(store.namespace, anchor, request["partition"])
                while result["next"] < part["count"]:
                    if len(result["hits"]) == limits["matches"]:
                        result["termination"] = "matches_exhausted"; break
                    io.charge("scanned")
                    position = result["next"]
                    row = io.one("SELECT object_id FROM postings WHERE feature_id=? AND partition=? AND ordinal=?",
                                 (anchor, request["partition"], position), probe=True)
                    F.need(row is not None, "CANDIDATE_ANCHOR_POSTING_MISSING")
                    object_id = F.hexid(row[0]); matches = True
                    for feature in request["features"]:
                        if feature == anchor: continue
                        probe = io.one("SELECT ordinal FROM postings WHERE feature_id=? AND partition=? AND object_id=?",
                                       (feature, request["partition"], object_id), probe=True)
                        # The database contains later appends too; current membership
                        # alone must not qualify an object for this selected old cut.
                        if probe is None or not 0 <= probe[0] < descriptors[feature]["count"]:
                            matches = False; break
                    if not matches:
                        io.live(); result["next"] = position+1; continue
                    io.used["record_loads"] += 1
                    stored = io.one("SELECT record_id,record FROM objects WHERE object_id=? AND admitted_seq<=?",
                                    (object_id, snapshot["local_cut"]), probe=True)
                    F.need(stored is not None, "CANDIDATE_OBJECT_NOT_IN_CUT")
                    record = F.validate_record(F.strict(bytes(stored[1]), F.MAX_RECORD), store.namespace)
                    io.hash_step(); rid = F.record_id(record)
                    F.need(rid == stored[0] and record["object_id"] == object_id
                           and int(object_id[:2], 16) == request["partition"]
                           and set(request["features"]) <= set(record["features"]), "CANDIDATE_RECORD_BINDING")
                    io.used["proofs"] += 1
                    committed, siblings = A.vector_get(io, ctx, part["count"], part["tree_root"], position)
                    F.need(committed == rid, "CANDIDATE_ANCHOR_RECORD_BINDING")
                    proposed = {**result, "next": position+1,
                                "hits": [*result["hits"], {"ordinal": position, "record": record, "siblings": siblings}]}
                    if _wire_upper(proposed, request) > limits["bytes"]:
                        result["termination"] = "bytes_exhausted"; break
                    io.live(); result = proposed
                io.live()
            except _Stop as stopped:
                result["termination"] = str(stopped)
    finally:
        store.db.set_progress_handler(None, 0)
        store.db.execute("PRAGMA busy_timeout="+str(saved_busy))
    _finalize(result, request, io.used)
    F.need(len(F.compact(result)) <= limits["bytes"], "CANDIDATE_PAGE_TOO_SMALL")
    return result


def verify_page(summary, request, response, *, check_budget=None):
    """Verify positive record membership only, using a locally verified summary.

    The transport/session must charge raw bytes before parsing; this function
    neither owns network budgets nor creates Coverage. Remote resource counters,
    next cursor and termination remain advisory even when every hit verifies.
    """
    def guard():
        if check_budget is not None: check_budget()
    guard(); validate_request(request, summary["namespace"])
    F.need(request["snapshot_id"] == summary["snapshot_id"] and request["features"] == summary["features"],
           "CANDIDATE_SUMMARY_BINDING")
    plan = Q.plan_partitions(summary)[request["partition"]]
    F.need(request["anchor"] == plan["anchor"], "CANDIDATE_PLANNED_ANCHOR")
    F.uint(request["start"], 0, plan["anchor_count"], "CANDIDATE_START")
    F.fields(response, ("schema", "namespace", "snapshot_id", "query_id", "partition", "anchor", "start", "next",
                        "anchor_count", "hits", "next_cursor", "termination", "charged", "coverage",
                        "global_complete", "mathematical_acceptance"))
    F.need(response["schema"] == "DMKN_FORMAL_CANDIDATE_PAGE_V1", "CANDIDATE_PAGE_SCHEMA")
    for key in ("namespace", "snapshot_id", "partition", "anchor", "start"):
        F.need(type(response[key]) is type(request[key]) and response[key] == request[key], "CANDIDATE_REQUEST_BINDING:"+key)
    query = Q.query_id(summary["namespace"], summary["features"])
    F.need(response["query_id"] == query and response["coverage"] == CLAIM
           and response["global_complete"] is False and response["mathematical_acceptance"] is False,
           "CANDIDATE_ASSURANCE")
    limits = request["limits"]
    F.need(len(F.compact(response)) <= limits["bytes"], "CANDIDATE_BYTE_CAP")
    F.need(type(response["hits"]) is list and len(response["hits"]) <= limits["matches"], "CANDIDATE_HIT_COUNT")
    F.uint(response["next"], request["start"], plan["anchor_count"], "CANDIDATE_NEXT")
    F.need(response["termination"] in TERMINATIONS, "CANDIDATE_TERMINATION")
    if response["anchor_count"] is None:
        F.need(not response["hits"] and response["next"] == request["start"]
               and response["termination"] in ("time_exhausted", "node_reads_exhausted", "hash_calls_exhausted",
                                                "sql_vm_steps_exhausted"), "CANDIDATE_UNPLANNED_REFUSAL")
    else:
        F.need(type(response["anchor_count"]) is int and response["anchor_count"] == plan["anchor_count"],
               "CANDIDATE_ANCHOR_COUNT")
    F.need(response["termination"] != "anchor_boundary" or response["next"] == plan["anchor_count"],
           "CANDIDATE_ADVISORY_BOUNDARY")
    expected_cursor = None if response["anchor_count"] == response["next"] else cursor(request, query, response["next"])
    F.need(response["next_cursor"] == expected_cursor, "CANDIDATE_CURSOR_BINDING")
    F.fields(response["charged"], CHARGES)
    for key in CHARGES:
        F.uint(response["charged"][key], 0, limits.get(key, limits["scanned"]), "CANDIDATE_REPORTED_CHARGE:"+key)
    F.need(len(response["hits"]) <= response["charged"]["proofs"] <= response["charged"]["record_loads"]
           <= response["charged"]["scanned"], "CANDIDATE_REPORTED_WORK_SHAPE")
    F.need(response["next"]-request["start"] <= response["charged"]["scanned"]
           and response["charged"]["sql_vm_steps"] % 100 == 0, "CANDIDATE_REPORTED_SCAN_BOUND")
    p, anchor, seen, prior, hits = request["partition"], request["anchor"], set(), request["start"]-1, []
    parts = summary["partitions"][anchor]
    part = A.empty_descriptor(summary["namespace"], anchor, p) if parts is None else parts[p]
    ctx = A.context(summary["namespace"], anchor, p)
    for row in response["hits"]:
        guard(); F.fields(row, ("ordinal", "record", "siblings"))
        ordinal = F.uint(row["ordinal"], request["start"], response["next"]-1, "CANDIDATE_HIT_ORDINAL")
        F.need(ordinal > prior, "CANDIDATE_HIT_ORDER"); prior = ordinal
        record = F.validate_record(row["record"], summary["namespace"])
        F.need(set(request["features"]) <= set(record["features"])
               and int(record["object_id"][:2], 16) == p, "CANDIDATE_POSITIVE_FEATURE_RANGE")
        F.need(record["object_id"] not in seen, "CANDIDATE_DUPLICATE_OBJECT"); seen.add(record["object_id"])
        A.verify_vector(ctx, part["count"], part["tree_root"], ordinal, F.record_id(record), row["siblings"])
        hits.append(deepcopy(record))
    guard()
    return {"snapshot_id": summary["snapshot_id"], "namespace": summary["namespace"], "query_id": query,
            "features": list(summary["features"]), "matches": hits,
            "advisory_next": deepcopy(response["next_cursor"]), "provider_termination": response["termination"],
            "provider_work_claims": deepcopy(response["charged"]),
            "assurance": "VERIFIED_POSITIVE_COMMITTED_RECORDS_ONLY", "verified_scan_coverage": False,
            "global_complete": False, "mathematical_acceptance": False}

"""Client verification and coverage, never mathematical acceptance.

verify_page expects an unmodified result of verify_summary from the caller's
trusted local process. Network dictionaries are not verified summaries merely
because they happen to have the same shape. Coverage keeps its own deep copy.
"""
from __future__ import annotations

from copy import deepcopy
from . import authenticated_index as A
from .formal_features import (compact, digest, fields, hexid, need, record_id,
                              uint, validate_features, validate_record)

PAGE_LIMITS = {"examined": (1, 32), "matches": (1, 8), "bytes": (1024, 1048576),
               "timeout_ms": (1, 1000), "node_reads": (1, 100000)}
TERMINATIONS = {"anchor_exhausted", "examined_exhausted", "matches_exhausted",
                "bytes_exhausted", "time_exhausted", "work_exhausted", "page_continuation"}


def query_id(namespace, features):
    validate_features(features, 8)
    return digest("DMKN-FORMAL-CONJUNCTION-V1", {"namespace": hexid(namespace), "features": features})


def validate_request(request, namespace=None):
    fields(request, ("schema", "namespace", "snapshot_id", "features", "partition", "anchor", "start", "limits"))
    need(request["schema"] == "DMKN_FORMAL_QUERY_REQUEST_V1", "QUERY_REQUEST_SCHEMA")
    hexid(request["namespace"]); hexid(request["snapshot_id"]); hexid(request["anchor"])
    need(namespace is None or request["namespace"] == namespace, "QUERY_NAMESPACE")
    validate_features(request["features"], 8)
    need(request["anchor"] in request["features"], "QUERY_ANCHOR_FEATURE")
    uint(request["partition"], 0, 255, "QUERY_PARTITION")
    uint(request["start"], 0, A.MAX_VECTOR, "QUERY_START")
    fields(request["limits"], PAGE_LIMITS)
    for key, (low, high) in PAGE_LIMITS.items(): uint(request["limits"][key], low, high, "QUERY_LIMIT:"+key)
    need(len(compact(request)) <= 16384, "QUERY_REQUEST_BYTES")
    return request


def cursor(request, next_position):
    return {"schema": "DMKN_FORMAL_QUERY_CURSOR_V1", "snapshot_id": request["snapshot_id"],
            "query_id": query_id(request["namespace"], request["features"]),
            "partition": request["partition"], "anchor": request["anchor"], "next": next_position}


def verify_summary(expected_snapshot_id, namespace, features, response):
    hexid(expected_snapshot_id); hexid(namespace); validate_features(features, 8)
    fields(response, ("schema", "namespace", "snapshot_id", "snapshot", "features", "rows",
                      "coverage", "mathematical_acceptance"))
    need(response["schema"] == "DMKN_FORMAL_QUERY_SUMMARY_V1" and response["namespace"] == namespace
         and response["snapshot_id"] == expected_snapshot_id and response["features"] == features,
         "SUMMARY_REQUEST_BINDING")
    need(response["coverage"] == "COMMITTED_METADATA_NOT_SOURCE_CORPUS"
         and response["mathematical_acceptance"] is False, "SUMMARY_ASSURANCE")
    A.validate_snapshot(response["snapshot"], namespace)
    need(A.snapshot_id(response["snapshot"]) == expected_snapshot_id, "SUMMARY_SNAPSHOT_ID")
    need(type(response["rows"]) is list and len(response["rows"]) == len(features), "SUMMARY_ROWS")
    need(len(compact(response)) <= 1048576, "SUMMARY_BYTE_CAP")
    partitions = {}
    for feature, row in zip(features, response["rows"]):
        fields(row, ("feature_id", "partitions", "siblings"))
        need(row["feature_id"] == feature, "SUMMARY_FEATURE_ORDER")
        selected_root = None if row["partitions"] is None else A.feature_root(namespace, feature, row["partitions"])
        A.verify_map(namespace, response["snapshot"]["feature_map_root"], feature, selected_root, row["siblings"])
        partitions[feature] = deepcopy(row["partitions"])
    return {"snapshot_id": expected_snapshot_id, "namespace": namespace, "descriptor": deepcopy(response["snapshot"]),
            "features": list(features), "partitions": partitions}


def plan_partitions(summary):
    result = []
    for p in range(256):
        count, anchor = min((0 if summary["partitions"][f] is None else summary["partitions"][f][p]["count"], f)
                            for f in summary["features"])
        result.append({"partition": p, "anchor": anchor, "anchor_count": count, "committed_empty": count == 0})
    return result


def verify_page(summary, request, response):
    validate_request(request, summary["namespace"])
    need(request["snapshot_id"] == summary["snapshot_id"] and request["features"] == summary["features"], "PAGE_SUMMARY_BINDING")
    selected = plan_partitions(summary)[request["partition"]]
    need(request["anchor"] == selected["anchor"], "PAGE_PLANNED_ANCHOR")
    uint(request["start"], 0, selected["anchor_count"], "PAGE_START")
    fields(response, ("schema", "namespace", "snapshot_id", "query_id", "partition", "anchor", "start", "next",
                      "anchor_count", "examined", "match_ordinals", "next_cursor", "termination", "charged",
                      "coverage", "mathematical_acceptance"))
    need(response["schema"] == "DMKN_FORMAL_QUERY_PAGE_V1", "PAGE_SCHEMA")
    for key in ("namespace", "snapshot_id", "partition", "anchor", "start"):
        need(type(response[key]) is type(request[key]) and response[key] == request[key], "PAGE_REQUEST_BINDING:"+key)
    expected_query = query_id(summary["namespace"], summary["features"])
    need(response["query_id"] == expected_query and response["anchor_count"] == selected["anchor_count"]
         and type(response["anchor_count"]) is int, "PAGE_COUNT_BINDING")
    need(response["coverage"] == "COMMITTED_ANCHOR_INTERVAL_ONLY" and response["mathematical_acceptance"] is False,
         "PAGE_ASSURANCE")
    limits = request["limits"]
    need(type(response["examined"]) is list and len(response["examined"]) <= limits["examined"], "PAGE_EXAMINED_BOUND")
    uint(response["next"], request["start"], selected["anchor_count"], "PAGE_NEXT")
    need(response["next"] == request["start"] + len(response["examined"]), "PAGE_CONSECUTIVE_INTERVAL")
    need(type(response["match_ordinals"]) is list and len(response["match_ordinals"]) <= limits["matches"], "PAGE_MATCH_BOUND")
    need(response["termination"] in TERMINATIONS, "PAGE_TERMINATION")
    need((response["next"] == selected["anchor_count"]) == (response["termination"] == "anchor_exhausted"), "PAGE_TERMINAL_POSITION")
    expected_cursor = None if response["next"] == selected["anchor_count"] else cursor(request, response["next"])
    need(response["next_cursor"] == expected_cursor, "PAGE_CURSOR_BINDING")
    fields(response["charged"], ("node_reads", "examined"))
    uint(response["charged"]["node_reads"], 0, limits["node_reads"], "PAGE_CHARGED_READS")
    need(type(response["charged"]["examined"]) is int
         and response["charged"]["examined"] == len(response["examined"]), "PAGE_CHARGED_EXAMINED")
    need(len(compact(response)) <= limits["bytes"], "PAGE_BYTE_CAP")
    p, anchor = request["partition"], request["anchor"]
    descriptor = summary["partitions"][anchor]
    part = A.empty_descriptor(summary["namespace"], anchor, p) if descriptor is None else descriptor[p]
    wanted = set(summary["features"]); matches, ordinals, seen = [], [], set()
    ctx = A.context(summary["namespace"], anchor, p)
    for offset, row in enumerate(response["examined"]):
        fields(row, ("ordinal", "record", "siblings"))
        index = request["start"] + offset
        need(type(row["ordinal"]) is int and row["ordinal"] == index, "PAGE_ORDINAL_OMISSION")
        record = validate_record(row["record"], summary["namespace"])
        need(anchor in record["features"] and int(record["object_id"][:2], 16) == p, "PAGE_POSTING_FEATURE_RANGE")
        need(record["object_id"] not in seen, "PAGE_DUPLICATE_OBJECT"); seen.add(record["object_id"])
        A.verify_vector(ctx, part["count"], part["tree_root"], index, record_id(record), row["siblings"])
        if wanted <= set(record["features"]): matches.append(deepcopy(record)); ordinals.append(index)
    need(response["match_ordinals"] == ordinals and all(type(i) is int for i in response["match_ordinals"]), "PAGE_FILTER_RESULT")
    return {"snapshot_id": summary["snapshot_id"], "namespace": summary["namespace"], "query_id": expected_query,
            "features": list(summary["features"]), "partition": p, "anchor": anchor, "start": request["start"],
            "next": response["next"], "anchor_count": part["count"], "matches": matches,
            "termination": response["termination"], "assurance": "VERIFIED_COMMITTED_INTERVAL",
            "mathematical_acceptance": False}


class Coverage:
    def __init__(self, summary):
        self.summary = deepcopy(summary)
        self.plans = plan_partitions(self.summary)
        self.intervals = {p: [] for p in range(256)}
        self.observed = {}

    def accept(self, request, response, *, before_commit=None):
        verified = verify_page(self.summary, request, response)
        updates = {}
        for row in response["examined"]:
            key, position = row["record"]["object_id"], (verified["partition"], row["ordinal"])
            binding = (position, record_id(row["record"]))
            need(key not in self.observed or self.observed[key] == binding, "CROSS_PAGE_OBJECT_CONSISTENCY")
            updates[key] = binding
        p = verified["partition"]
        intervals = sorted([*self.intervals[p], (verified["start"], verified["next"])])
        merged = []
        for start, stop in intervals:
            if start == stop: continue
            if merged and start <= merged[-1][1]: merged[-1] = (merged[-1][0], max(stop, merged[-1][1]))
            else: merged.append((start, stop))
        if before_commit is not None: before_commit()
        self.observed.update(updates); self.intervals[p] = merged
        return verified

    def report(self):
        rows = []
        for plan in self.plans:
            p, count = plan["partition"], plan["anchor_count"]
            complete = count == 0 or self.intervals[p] == [(0, count)]
            rows.append({"partition": p, "anchor": plan["anchor"], "anchor_count": count,
                         "intervals": [list(pair) for pair in self.intervals[p]], "complete_committed_anchor": complete})
        done = all(row["complete_committed_anchor"] for row in rows)
        return {"snapshot_id": self.summary["snapshot_id"], "query_id": query_id(self.summary["namespace"], self.summary["features"]),
                "partitions": rows, "complete_committed_anchor_domain": done,
                "conditional_complete_if_correctly_built": done, "global_complete": False,
                "mathematical_acceptance": False, "build_assurance": "NOT_PROVIDED"}

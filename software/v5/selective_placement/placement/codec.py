"""Closed placement data and conservative reservations, never live authority."""
from copy import deepcopy
import hashlib

from discovery import formal_features as F
from discovery.module_export_adapter import validate_spec
from discovery.conclusion_fingerprint import FINGERPRINT_TAG
from location.protocol import route_key
from modules import codec as C

MIB = 1024**2
REQUEST_MAX, OUTCOME_MAX = 16384, 65536
CONFIG_SCHEMA = "DMKN_V5_LOCAL_PLACEMENT_GENERATION_V1"
REQUEST_SCHEMA = "DMKN_V5_LOCAL_PLACEMENT_REQUEST_V1"
RESOURCES = ("placements", "requests", "reply_bytes", "wire_overhead_bytes",
             "structural_bytes", "storage_bytes", "index_calls", "recovery_passes", "new_cells")
# Selected index: at most 260 map, 9 partition and 22 vector writes per
# feature, each <=4096 encoded bytes; one record and one small snapshot.
# This bounds additional *logical* bytes, not filesystem pages or free space.
INDEX_LOGICAL_INCREMENT = F.MAX_FEATURES*(260+9+22)*4096+F.MAX_RECORD+4096
FLAGS = {"mathematical_acceptance": False, "global_complete": False,
         "cross_database_atomic": False, "all_future_bodies_covered": False}


def digest(raw): return hashlib.sha256(raw).hexdigest()


def limits(value):
    F.fields(value, RESOURCES)
    for name in RESOURCES:
        F.uint(value[name], 0, 2**50, "PLACEMENT_LIMIT:"+name)
    return deepcopy(value)


def config(value):
    F.fields(value, ("schema", "service_epoch", "generation", "namespace", "wire_profile_id",
                     "admission_close_ms", "retention_not_after_ms", "max_grants", "max_requests",
                     "max_cells", "max_runs", "ledger_pages", "limits"))
    F.need(value["schema"] == CONFIG_SCHEMA, "PLACEMENT_CONFIG_SCHEMA")
    for name in ("service_epoch", "generation", "namespace", "wire_profile_id"): F.hexid(value[name])
    for name in ("admission_close_ms", "retention_not_after_ms"):
        F.uint(value[name], 1, 2**53-1, "PLACEMENT_ABSOLUTE_TIME")
    F.need(value["admission_close_ms"] <= value["retention_not_after_ms"], "PLACEMENT_HORIZON_ORDER")
    for name in ("max_grants", "max_requests", "max_cells", "max_runs"):
        F.uint(value[name], 1, 4096, "PLACEMENT_CONFIG_CAP:"+name)
    F.uint(value["ledger_pages"], 256, 65536, "PLACEMENT_LEDGER_PAGES")
    limits(value["limits"])
    return deepcopy(value)


def manifest(raw, selected):
    F.need(type(raw) is bytes and 0 < len(raw) <= REQUEST_MAX, "PLACEMENT_REQUEST_BYTES")
    value = F.strict(raw, REQUEST_MAX)
    F.need(F.compact(value) == raw, "PLACEMENT_REQUEST_CANONICAL")
    F.fields(value, ("schema", "generation", "namespace", "wire_profile_id", "module_id",
        "relative_name", "export_id", "fingerprint", "cell", "export_object_sha256",
        "export_object_bytes", "opening_max_bytes", "packet_sha256", "packet_bytes",
        "bodies", "retention_end_ms"))
    F.need(value["schema"] == REQUEST_SCHEMA, "PLACEMENT_REQUEST_SCHEMA")
    for name in ("generation", "namespace", "wire_profile_id"):
        F.need(value[name] == selected[name], "PLACEMENT_REQUEST_DOMAIN:"+name)
    for name in ("module_id", "export_id", "cell", "export_object_sha256", "packet_sha256"):
        F.hexid(value[name])
    C.validate_name(value["relative_name"])
    F.need(C.export_id(value["module_id"], value["relative_name"]) == value["export_id"],
           "PLACEMENT_EXPORT_ADDRESS")
    spec = validate_spec(value["fingerprint"])
    F.need(spec["tag"] == FINGERPRINT_TAG, "PLACEMENT_FINGERPRINT_REQUIRED")
    for name, ceiling in (("export_object_bytes",16*MIB),("opening_max_bytes",16*MIB),
                          ("packet_bytes",32*MIB)):
        F.uint(value[name], 1, ceiling, "PLACEMENT_OBJECT_BOUND:"+name)
    F.uint(value["retention_end_ms"], 1, selected["retention_not_after_ms"], "PLACEMENT_RETENTION")
    rows = value["bodies"]
    F.need(type(rows) is list and len(rows) <= 8, "PLACEMENT_BODY_COUNT")
    keys = []
    for row in rows:
        F.fields(row, ("body_hash", "max_bytes")); keys.append(F.hexid(row["body_hash"]))
        F.uint(row["max_bytes"], 1, 16*MIB, "PLACEMENT_BODY_BYTES")
    F.need(keys == sorted(set(keys)), "PLACEMENT_BODY_ORDER")
    return value


def request_id(raw, grant_id, generation):
    return F.digest("DMKN-V5-PLACEMENT-REQUEST-V1", {
        "manifest_sha256": digest(raw), "manifest_bytes": len(raw),
        "grant_id": F.hexid(grant_id), "generation": F.hexid(generation)})


def cell(adapter, fingerprint):
    features = adapter.compile_query([fingerprint])
    F.need(len(features) == 1, "PLACEMENT_SINGLE_FINGERPRINT")
    return route_key(adapter.namespace, features, 0), features[0]


def quote(value, *, new_cell, index_logical_cap):
    """Finite upper suballocation; not a measurement or promise of free space.

    Counters are cumulative funded authorization, not physical reservations.
    Actual immutable logical/page caps still govern writes. Known-new storage
    is reported separately; duplicate content is not claimed as a fresh copy.
    No unused funding reservation is refunded.
    """
    count = 3+len(value["bodies"])
    payload = value["opening_max_bytes"]+value["packet_bytes"]+sum(x["max_bytes"] for x in value["bodies"])
    return {"placements": 1, "requests": count, "reply_bytes": payload+4096,
        "wire_overhead_bytes": count*32768,
        "structural_bytes": 32*(payload+value["export_object_bytes"]+REQUEST_MAX),
        "storage_bytes": 3*value["export_object_bytes"]+value["packet_bytes"]
                         +sum(x["max_bytes"] for x in value["bodies"])
                         +min(index_logical_cap,INDEX_LOGICAL_INCREMENT)+2*OUTCOME_MAX,
        "index_calls": 2, "recovery_passes": 1, "new_cells": int(new_cell)}


def checked_export(adapter, value, opening):
    raw = adapter.encode_opening(value["module_id"], value["relative_name"], opening)
    F.need(len(raw) == value["export_object_bytes"] and digest(raw) == value["export_object_sha256"],
           "PLACEMENT_EXACT_EXPORT_OBJECT")
    described = adapter.describe(raw, expected_id=value["export_id"])
    actual = [spec for spec in described["specs"] if spec["tag"] == FINGERPRINT_TAG]
    F.need(actual == [value["fingerprint"]], "PLACEMENT_DERIVED_FINGERPRINT")
    key, feature = cell(adapter, actual[0])
    F.need(key == value["cell"], "PLACEMENT_DERIVED_CELL")
    return raw, described, feature

"""Canonical sparse SUMMARY_V1 transport encoding, NOT authentication.

decode_summary returns an ordinary reconstructed dictionary. The caller MUST
pass it to discovery_query.verify_summary with independently selected bindings
before treating any metadata interval as authenticated. Mathematical acceptance
and source-corpus completeness never follow from this codec or summary proofs.

Receive/charge the actual raw wire bytes before decoding. Expanded canonical
bytes are separately bounded, not falsely charged as network traffic. Counts
bound allocation to8 rows,2048 partition descriptors and2048 sibling hashes;
Python object/container overhead is additional to the encoded-byte ceilings.
"""
from copy import deepcopy

from . import authenticated_index as A
from . import formal_features as F

SCHEMA = "DMKN_FORMAL_QUERY_SUMMARY_COMPACT_V1"
EXPANDED_SCHEMA = "DMKN_FORMAL_QUERY_SUMMARY_V1"
MAX_BYTES = 1048576
HEADER = ("schema", "namespace", "snapshot_id", "snapshot", "features", "rows",
          "coverage", "mathematical_acceptance")
_SIBLING_LIST_BYTES = 2 + 256*66 + 255
_DESCRIPTOR_ZERO_BYTES = len(F.compact({"partition": 0, "count": 0, "tree_root": "0"*64}))
_EMPTY_PARTITION_LIST_BYTES = 2 + 255 + 256*(_DESCRIPTOR_ZERO_BYTES-1) + sum(len(str(p)) for p in range(256))
_ROW_SKELETON_BYTES = len(F.compact({"feature_id": "0"*64, "partitions": None, "siblings": []}))


def _limits(wire, expanded):
    F.uint(wire, 1, MAX_BYTES, "SUMMARY_WIRE_CAP")
    F.uint(expanded, 1, MAX_BYTES, "SUMMARY_EXPANDED_CAP")


def _check(callback):
    if callback is not None: callback()


def _header(value, schema, expected_snapshot_id, namespace, features):
    F.hexid(expected_snapshot_id); F.hexid(namespace); F.validate_features(features, 8)
    F.fields(value, HEADER)
    F.need(value["schema"] == schema and value["namespace"] == namespace
           and value["snapshot_id"] == expected_snapshot_id and value["features"] == features,
           "SUMMARY_WIRE_REQUEST_BINDING")
    F.need(value["coverage"] == "COMMITTED_METADATA_NOT_SOURCE_CORPUS"
           and value["mathematical_acceptance"] is False, "SUMMARY_WIRE_ASSURANCE")
    A.validate_snapshot(value["snapshot"], namespace)
    F.need(A.snapshot_id(value["snapshot"]) == expected_snapshot_id, "SUMMARY_WIRE_SNAPSHOT_BINDING")
    F.need(type(value["rows"]) is list and len(value["rows"]) == len(features), "SUMMARY_WIRE_ROWS")


def _sparse_rows(value, namespace, features, check_budget):
    """Validate all sparse counts/indices BEFORE allocating expanded arrays."""
    defaults = A.map_empty(namespace)
    for feature, row in zip(features, value["rows"]):
        _check(check_budget)
        F.fields(row, ("feature_id", "presence", "partitions", "siblings"))
        F.need(row["feature_id"] == feature, "SUMMARY_WIRE_FEATURE_ORDER")
        F.need(row["presence"] in ("present", "absent"), "SUMMARY_WIRE_PRESENCE")
        F.need(type(row["partitions"]) is list and len(row["partitions"]) <= 256, "SUMMARY_WIRE_PARTITION_COUNT")
        F.need(row["presence"] == "present" or not row["partitions"], "SUMMARY_WIRE_ABSENT_PARTITIONS")
        previous = -1
        for desc in row["partitions"]:
            F.fields(desc, ("partition", "count", "tree_root"))
            p = F.uint(desc["partition"], 0, 255, "SUMMARY_WIRE_PARTITION")
            F.need(p > previous, "SUMMARY_WIRE_PARTITION_ORDER"); previous = p
            F.uint(desc["count"], 1, A.MAX_VECTOR, "SUMMARY_WIRE_NONEMPTY_PARTITION")
            F.hexid(desc["tree_root"])
        F.need(type(row["siblings"]) is list and len(row["siblings"]) <= 256, "SUMMARY_WIRE_SIBLING_COUNT")
        previous = -1
        for entry in row["siblings"]:
            F.need(type(entry) is list and len(entry) == 2, "SUMMARY_WIRE_SIBLING_ENTRY")
            depth = F.uint(entry[0], 0, 255, "SUMMARY_WIRE_DEPTH")
            F.need(depth > previous, "SUMMARY_WIRE_SIBLING_ORDER"); previous = depth
            F.hexid(entry[1])
            F.need(entry[1] != defaults[depth+1], "SUMMARY_WIRE_EXPLICIT_DEFAULT")


def _expanded_bytes(value):
    """Exact canonical byte size using integer/string widths, before expansion."""
    header = {**value, "schema": EXPANDED_SCHEMA, "rows": []}
    total = len(F.compact(header)) + len(value["rows"])-1
    for row in value["rows"]:
        partitions = 4  # JSON null, not an empty/present partition vector.
        if row["presence"] == "present":
            partitions = _EMPTY_PARTITION_LIST_BYTES + sum(len(str(d["count"]))-1 for d in row["partitions"])
        total += _ROW_SKELETON_BYTES - 4 - 2 + partitions + _SIBLING_LIST_BYTES
    return total


def decode_summary(raw, expected_snapshot_id, namespace, features, *,
                   max_wire_bytes=MAX_BYTES, max_expanded_bytes=MAX_BYTES, check_budget=None):
    """Bounded structural reconstruction only; call Q.verify_summary afterwards.

    check_budget is an optional owner-local deadline/resource guard. It runs
    before parsing, for every sparse/expanded row and before returning. There is
    no persistent verified cache and no authorization imported from raw bytes.
    """
    _limits(max_wire_bytes, max_expanded_bytes); _check(check_budget)
    value = F.strict(raw, max_wire_bytes)
    _header(value, SCHEMA, expected_snapshot_id, namespace, features)
    _sparse_rows(value, namespace, features, check_budget)
    predicted = _expanded_bytes(value)
    F.need(predicted <= max_expanded_bytes, "SUMMARY_EXPANSION_BYTES")
    defaults, rows = A.map_empty(namespace), []
    for row in value["rows"]:
        _check(check_budget)
        partitions = None
        if row["presence"] == "present":
            supplied = {d["partition"]: d for d in row["partitions"]}
            partitions = [deepcopy(supplied[p]) if p in supplied else A.empty_descriptor(namespace, row["feature_id"], p)
                          for p in range(256)]
        siblings = list(defaults[1:])
        for depth, digest in row["siblings"]: siblings[depth] = digest
        rows.append({"feature_id": row["feature_id"], "partitions": partitions, "siblings": siblings})
    result = {**value, "schema": EXPANDED_SCHEMA, "rows": rows}
    F.need(len(F.compact(result)) == predicted, "SUMMARY_EXPANSION_SIZE_ACCOUNTING")
    _check(check_budget)
    return result


def encode_summary(value, expected_snapshot_id, namespace, features, *,
                   max_wire_bytes=MAX_BYTES, max_expanded_bytes=MAX_BYTES, check_budget=None):
    """Lossless structural compression; neither this nor decode verifies proofs."""
    _limits(max_wire_bytes, max_expanded_bytes); _check(check_budget)
    _header(value, EXPANDED_SCHEMA, expected_snapshot_id, namespace, features)
    defaults, rows = A.map_empty(namespace), []
    for feature, row in zip(features, value["rows"]):
        _check(check_budget)
        F.fields(row, ("feature_id", "partitions", "siblings"))
        F.need(row["feature_id"] == feature, "SUMMARY_WIRE_FEATURE_ORDER")
        parts, sparse = row["partitions"], []
        if parts is not None:
            F.need(type(parts) is list and len(parts) == 256, "SUMMARY_EXPANDED_PARTITION_COUNT")
            for p, desc in enumerate(parts):
                F.fields(desc, ("partition", "count", "tree_root"))
                F.need(type(desc["partition"]) is int and desc["partition"] == p, "SUMMARY_EXPANDED_PARTITION_ORDER")
                F.uint(desc["count"], 0, A.MAX_VECTOR, "SUMMARY_EXPANDED_PARTITION_COUNT")
                F.hexid(desc["tree_root"])
                if desc["count"] == 0:
                    F.need(desc == A.empty_descriptor(namespace, feature, p), "SUMMARY_EXPANDED_DEFAULT_BINDING")
                else: sparse.append(deepcopy(desc))
        F.need(type(row["siblings"]) is list and len(row["siblings"]) == 256, "SUMMARY_EXPANDED_SIBLING_COUNT")
        siblings = []
        for depth, sibling in enumerate(row["siblings"]):
            F.hexid(sibling)
            if sibling != defaults[depth+1]: siblings.append([depth, sibling])
        rows.append({"feature_id": feature, "presence": "absent" if parts is None else "present",
                     "partitions": sparse, "siblings": siblings})
    compact = {**{k: deepcopy(v) for k, v in value.items() if k != "rows"}, "schema": SCHEMA, "rows": rows}
    # Original tree/arrays have fixed counts and scalar widths before encoding.
    F.need(len(F.compact(value)) <= max_expanded_bytes, "SUMMARY_EXPANSION_BYTES")
    raw = F.compact(compact)
    F.need(len(raw) <= max_wire_bytes, "SUMMARY_WIRE_BYTES")
    _check(check_budget)
    return raw

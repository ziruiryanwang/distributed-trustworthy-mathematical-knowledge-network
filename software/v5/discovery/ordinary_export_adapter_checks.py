"""Four focused portable-discovery controls; root selects execution separately.

Uses the actual fresh Store/Query/Candidate code, not a replacement index. All
preview fixtures are synthetic, unproved metadata. No Lean, catalog, migration,
network or certificate work. The caller supplies a fresh absolute --store-root
under its operation directory; the resulting index is retained, not deleted.
"""
from pathlib import Path
import argparse
import builtins
from copy import deepcopy
import hashlib
import json
import sys

sys.dont_write_bytecode = True
V5 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(V5))
from discovery import formal_features as F
from discovery import authenticated_index as A
from discovery import discovery_query as Q
from discovery import candidate_query as C
from discovery import ordinary_export_adapter as O
from discovery.discovery_store import Store


STORE_LIMITS = dict(max_objects=16, max_postings=4096, max_features=4096,
                    max_snapshots=32, max_logical_bytes=16777216, max_db_pages=8192)
PAGE_LIMITS = dict(examined=32, matches=8, bytes=65536, timeout_ms=1000,
                   node_reads=100000)
CANDIDATE_LIMITS = dict(scanned=32, matches=8, bytes=65536, timeout_ms=1000,
                        record_probes=256, node_reads=100000, hash_calls=2000000,
                        sql_vm_steps=1000000)


def ensure(ok, code):
    if not ok:
        raise AssertionError(code)


def refuses(marker, action):
    try:
        action()
    except ValueError as exc:
        ensure(marker in str(exc), "WRONG_REFUSAL:" + str(exc))
    else:
        raise AssertionError("MISSING_REFUSAL:" + marker)


def report(label):
    print("PORTABLE_DISCOVERY_CHECK " + label + " PASS", flush=True)


def key(label):
    return hashlib.sha256(label.encode("ascii")).hexdigest()


def name(label):
    return [[0, {"$bytes": list(label.encode("ascii"))}]]


def independent_json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def legacy_control():
    """Fixed old schemas/domains, with ordinary imports forbidden throughout."""
    helpers = {"ordinary_evidence", "ordinary_preview", "ordinary_semantics",
               "portable_evidence", "portable_preview"}
    ensure(not helpers.intersection(sys.modules), "ORDINARY_HELPERS_EAGERLY_IMPORTED")
    original_import = builtins.__import__

    def blocked(module, *args, **kwargs):
        ensure(module.split(".")[0] not in helpers, "OLD_PATH_IMPORTS_ORDINARY_HELPER")
        return original_import(module, *args, **kwargs)

    first = {"schema": "DMKN_FORMAL_FEATURE_RECORD_V1", "namespace": "1" * 64,
             "kind": "named-definition-v1", "object_id": "2" * 64,
             "object_sha256": "3" * 64, "object_bytes": 7, "features": ["4" * 64]}
    second = {**first, "schema": "DMKN_FORMAL_FEATURE_RECORD_V2", "kind": "module-export-v1",
              "locator": {"schema": "DMKN_MODULE_EXPORT_LOCATOR_V1", "module_id": "5" * 64,
                          "group_index": 0, "relative_name": [["s", "Fixture"]],
                          "descriptor_id": "6" * 64}}
    try:
        builtins.__import__ = blocked
        ensure(F.SCHEMA == "DMKN_DECLARED_TYPE_FEATURES_V1" and
               F.EXPORT_SCHEMA == "DMKN_MODULE_EXPORT_FEATURES_V1", "LEGACY_FEATURE_SCHEMAS")
        for record, domain in (
                (first, b"DMKN-FORMAL-FEATURE-RECORD-V1\0"),
                (second, b"DMKN-FORMAL-FEATURE-RECORD-V2\0")):
            expected_bytes = independent_json(record)
            ensure(F.validate_record(deepcopy(record)) == record and
                   F.compact(record) == expected_bytes and
                   F.record_id(record) == hashlib.sha256(domain + expected_bytes).hexdigest(),
                   "LEGACY_VALID_RECORD_BYTES_OR_DOMAIN")
        for feature_schema in ("DMKN_DECLARED_TYPE_FEATURES_V1", "DMKN_MODULE_EXPORT_FEATURES_V1"):
            snapshot = {"schema": "DMKN_FORMAL_INDEX_SNAPSHOT_V1", "namespace": "1" * 64,
                        "feature_schema": feature_schema, "partition_bits": 8,
                        "feature_map_root": "7" * 64, "local_cut": 0,
                        "previous_snapshot": None,
                        "coverage_claim": "PROVIDER_SELECTED_FEATURE_RECORDS_NOT_GLOBAL_CORPUS"}
            expected_bytes = independent_json(snapshot)
            ensure(A.validate_snapshot(deepcopy(snapshot)) == snapshot and
                   F.compact(snapshot) == expected_bytes and A.snapshot_id(snapshot) ==
                   hashlib.sha256(b"DMKN-FORMAL-INDEX-SNAPSHOT-V1\0" + expected_bytes).hexdigest(),
                   "LEGACY_SNAPSHOT_BYTES_OR_DOMAIN")
        ensure(not helpers.intersection(sys.modules), "OLD_PATH_LOADED_ORDINARY_HELPER")
    finally:
        builtins.__import__ = original_import
    report("legacy_valid_bytes_domains_and_lazy_imports")


def preview(E, semantic, label, nodes, bindings, *, kind=2):
    bindings = sorted(deepcopy(bindings), key=lambda row: E.name_key(row[0]))
    return E.canonical_json({"schema": "DMKN_ORDINARY_LEAN_TYPE_PREVIEW_V2",
        "semantic_id": semantic, "unit_id": key("unit:" + label),
        "export_name": name(label), "header": [kind, [], [E.EXPR_FORMAT, [], nodes, len(nodes)-1]],
        "type_bindings": bindings})


def two_symbol_preview(E, semantic, label, a, b, *, kind=2):
    nodes = [[2, a[0], []], [2, b[0], []], [3, 0, 1], [5, [], 0, 0, 2]]
    return preview(E, semantic, label, nodes, [a, b], kind=kind)


def integration_control(store, adapter, E, semantic):
    known = [name("KnownType"), key("symbol:KnownType")]
    operation = [name("KnownOperation"), key("symbol:KnownOperation")]
    unrelated = [name("OtherOperation"), key("symbol:OtherOperation")]
    # Select the query solely from already-known symbols, before constructing
    # the unfamiliar result's fixture or reading any returned object identity.
    features = O.compile_query(adapter.namespace, [
        {"tag": "declaration-kind", "value": "theorem"},
        *({"tag": "type-symbol", "symbol": {"kind": "portable-symbol", "symbol_id": row[1]}}
          for row in (known, operation))])
    raws = [two_symbol_preview(E, semantic, "UnfamiliarMethod", known, operation),
            two_symbol_preview(E, semantic, "DifferentSubject", known, unrelated),
            two_symbol_preview(E, semantic, "DefinitionNotTheorem", known, operation, kind=1)]
    records, acquisition = [], {}
    for raw in raws:
        admitted = store.admit(raw)
        ensure(admitted["new"] and admitted["mathematical_acceptance"] is False,
               "FRESH_METADATA_ADMISSION")
        record = admitted["record"]
        records.append(record)
        acquisition[record["object_id"]] = raw
    sid = store.status()["latest"]
    wire_summary = store.summary(sid, features)
    summary = Q.verify_summary(sid, adapter.namespace, features, wire_summary)
    ensure(summary["descriptor"]["feature_schema"] == F.ORDINARY_EXPORT_SCHEMA,
           "PORTABLE_SNAPSHOT_SCHEMA")
    matches, candidate_matches = [], []
    plans = Q.plan_partitions(summary)
    ensure(len(plans) == 256, "ACTUAL_PARTITION_PLANNING")
    for plan in plans:
        if plan["committed_empty"]:
            continue
        # The partition and anchor come only from the authenticated summary,
        # never from the expected result's ID or fixture-record selection.
        request = {"schema": "DMKN_FORMAL_QUERY_REQUEST_V1", "namespace": adapter.namespace,
                   "snapshot_id": sid, "features": features, "partition": plan["partition"],
                   "anchor": plan["anchor"], "start": 0, "limits": dict(PAGE_LIMITS)}
        response = store.page(request)
        verified = Q.verify_page(summary, request, response)
        ensure(verified["termination"] == "anchor_exhausted" and
               verified["mathematical_acceptance"] is False, "FINITE_QUERY_NOT_EXHAUSTED")
        matches.extend(verified["matches"])
        candidate_request = {**request, "schema": "DMKN_FORMAL_CANDIDATE_REQUEST_V1",
                             "limits": dict(CANDIDATE_LIMITS)}
        candidate_response = C.page(store, candidate_request)
        candidates = C.verify_page(summary, candidate_request, candidate_response)
        ensure(candidates["verified_scan_coverage"] is False and
               candidates["mathematical_acceptance"] is False,
               "CANDIDATE_COVERAGE_OR_ACCEPTANCE_ESCALATION")
        candidate_matches.extend(candidates["matches"])
    ensure(matches == [records[0]] and candidate_matches == matches, "UNKNOWN_ID_QUERY_RESULT")
    resolved = adapter.resolve(matches[0], acquisition[matches[0]["object_id"]])
    ensure(resolved["locator"]["export_name"] == name("UnfamiliarMethod") and
           resolved["mathematical_acceptance"] is False and resolved["assurance"] ==
           "EXACT_PREVIEW_RECORD_BOUND_NOT_EVIDENCE_OR_MATHEMATICAL_ACCEPTANCE",
           "RESOLUTION_AUTHORITY_BOUNDARY")
    report("actual_store_unknown_id_query_and_positive_candidate")
    return raws[0], records[0]


def binding_control(store, adapter, E, S, raw, record):
    cases = [
        ("semantic", "ORDINARY_RECORD_NAMESPACE"),
        ("unit", "ORDINARY_RECORD_EXPORT_BINDING"),
        ("name", "ORDINARY_RECORD_EXPORT_BINDING"),
        ("namespace", "RECORD_NAMESPACE"),
        ("object", "ORDINARY_RECORD_EXPORT_BINDING"),
        ("hash", "ORDINARY_PREVIEW_RECORD_BINDING"),
        ("size", "ORDINARY_PREVIEW_RECORD_BINDING"),
        ("features", "ORDINARY_PREVIEW_RECORD_BINDING"),
        ("kind", "ORDINARY_RECORD_KIND")]
    for change, marker in cases:
        bad = deepcopy(record)
        if change == "semantic": bad["locator"]["semantic_id"] = key("other-semantic")
        elif change == "unit": bad["locator"]["unit_id"] = key("other-unit")
        elif change == "name": bad["locator"]["export_name"] = name("OtherExport")
        elif change == "namespace": bad["namespace"] = key("other-namespace")
        elif change == "object": bad["object_id"] = key("other-object")
        elif change == "hash": bad["object_sha256"] = key("other-preview")
        elif change == "size": bad["object_bytes"] += 1
        elif change == "features": bad["features"] = sorted({*bad["features"], key("invented-feature")})
        else: bad["kind"] = "other-kind"
        refuses(marker, lambda bad=bad: adapter.resolve(bad, raw))
    refuses("ORDINARY_EXPORT_ID_BINDING", lambda: adapter.extract(raw, expected_id=key("wrong-id")))
    saved_snapshot = store.snapshot()
    same = store.admit(raw)
    ensure(not same["new"] and same["snapshot_id"] == A.snapshot_id(saved_snapshot),
           "DUPLICATE_METADATA_NOT_IDEMPOTENT")
    changed_doc = E.strict_json(raw)
    changed_doc["header"][0] = 1
    changed_raw = E.canonical_json(changed_doc)
    refuses("ORDINARY_PREVIEW_RECORD_BINDING", lambda: adapter.resolve(record, changed_raw))
    refuses("OBJECT_RECORD_CONFLICT", lambda: store.admit(changed_raw))
    ensure(store.snapshot() == saved_snapshot, "CONFLICT_CHANGED_SNAPSHOT")
    other = key("unsupported-semantic")
    unsupported = deepcopy(record)
    unsupported["locator"]["semantic_id"] = other
    unsupported["namespace"] = O.namespace_for(other)
    unsupported["object_id"] = S.export_id(other, unsupported["locator"]["unit_id"],
                                           unsupported["locator"]["export_name"])
    ensure(F.validate_record(unsupported) == unsupported, "GENERIC_METADATA_ADOPTS_SEMANTICS")
    refuses("ORDINARY_SEMANTICS_NOT_SELECTED", lambda: O.OrdinaryExportAdapter(other))
    report("v3_binding_idempotence_conflict_and_unsupported_semantics")


def dag_control(adapter, E, semantic):
    a, b = [name("SharedHead"), key("SharedHead")], [name("SharedArgument"), key("SharedArgument")]
    nodes = [[2, a[0], []], [2, b[0], []]]
    shared = 0
    for _ in range(20):
        nodes.append([3, shared, 1])
        shared = len(nodes)-1
    body = shared
    for _ in range(12):
        nodes.append([5, [], 0, shared, body])
        body = len(nodes)-1
    described = adapter.describe(preview(E, semantic, "SharedSpine", nodes, [a, b]))
    expected_head = {"tag": "const", "symbol": {"kind": "portable-symbol", "symbol_id": a[1]}}
    ensure(described["type_nodes"] == len(nodes) and
           described["work"] == len(nodes)+2+2*12+3 and
           {"tag": "result-head", "head": expected_head} in described["specs"] and
           {"tag": "binder-domain-head", "head": expected_head} in described["specs"],
           "SHARED_SPINE_FEATURE_OR_LINEAR_WORK")
    projected = adapter.describe(preview(E, semantic, "Projection", [
        [2, a[0], []], [8, b[0], 0, 0]], [a, b]))
    ensure({"tag": "result-head", "head": {"tag": "proj", "symbol": {
        "kind": "portable-symbol", "symbol_id": b[1]}}} in projected["specs"], "PROJECTION_HEAD_BINDING")
    for tag, expected in ((7, "nat-literal"), (9, "string-literal")):
        literal = adapter.describe(preview(E, semantic, "Literal"+str(tag),
                                           [[tag, {"$bytes": [65]}]], []))
        ensure({"tag": "result-head", "head": {"tag": expected}} in literal["specs"] and
               not any(spec["tag"] == "type-symbol" for spec in literal["specs"]),
               "LITERAL_HEAD_OR_INVENTED_DEPENDENCY")

    def crowded(count):
        bindings = [[name("Type"+str(i)), key("Type"+str(i))] for i in range(count)]
        graph = [[2, row[0], []] for row in bindings]
        tail = 0
        for index in range(1, count):
            graph.append([3, tail, index])
            tail = len(graph)-1
        graph.append([5, [], 0, 0, tail])
        return preview(E, semantic, "Crowded"+str(count), graph, bindings)

    ensure(len(adapter.extract(crowded(124))["features"]) == 128, "FEATURE_BOUNDARY_128")
    refuses("ORDINARY_FEATURE_PROFILE_EXHAUSTED", lambda: adapter.extract(crowded(125)))
    report("shared_dag_exact_heads_literals_and_feature_boundary")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-root", required=True)
    args = parser.parse_args()
    legacy_control()
    # The old-path isolation control must execute before these lazy helpers load.
    sys.path.insert(0, str(V5 / "ordinary_lean"))
    import ordinary_evidence as E
    import ordinary_semantics as S
    semantic = S.semantic_id()
    adapter = O.OrdinaryExportAdapter(semantic)
    store = Store(Path(args.store_root), adapter, STORE_LIMITS, create=True)
    try:
        raw, record = integration_control(store, adapter, E, semantic)
        binding_control(store, adapter, E, S, raw, record)
        dag_control(adapter, E, semantic)
    finally:
        store.close()
    print("PORTABLE_DISCOVERY_ALL_PASS groups=4 mathematical_acceptance=false", flush=True)


if __name__ == "__main__":
    main()

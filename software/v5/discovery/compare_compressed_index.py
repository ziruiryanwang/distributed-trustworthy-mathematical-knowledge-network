"""One fresh18-export index vs immutable network01 database, never a network run.

All pins/inputs are explicit. Retained evidence opens mode=ro&immutable=1 only.
Root selects finite execution and freezes sources before running this harness.
"""
from pathlib import Path
import argparse
import hashlib
import sqlite3
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C
from discovery import formal_features as F
from discovery import authenticated_index as A
from discovery import discovery_query as Q
from discovery.discovery_store import Store
from discovery.module_export_adapter import ModuleExportAdapter, compile_query


def pinned(path, expected, maximum):
    path = Path(path); F.need(path.is_absolute(), "ABSOLUTE_INPUT")
    F.hexid(expected); F.need(0 < path.stat().st_size <= maximum, "INPUT_BOUND")
    raw = path.read_bytes()
    F.need(len(raw) <= maximum and hashlib.sha256(raw).hexdigest() == expected, "INPUT_PIN")
    return path, raw


class LegacyReadOnly:
    def __init__(self, path):
        self.db = sqlite3.connect(path.as_uri()+"?mode=ro&immutable=1", uri=True)
        self.reads = 0

    def close(self): self.db.close()

    def get_node(self, identifier):
        F.need(self.reads < 500000, "REFERENCE_READ_CAP"); self.reads += 1
        row = self.db.execute("SELECT encoded FROM cas_nodes WHERE hash=?", (identifier,)).fetchone()
        F.need(row is not None, "REFERENCE_NODE_MISSING")
        node = F.strict(bytes(row[0]), 4096)
        F.need(A.node_hash(node) == identifier, "REFERENCE_NODE_HASH")
        return node

    def record(self, identifier):
        row = self.db.execute("SELECT record FROM objects WHERE record_id=?", (identifier,)).fetchone()
        F.need(row is not None, "REFERENCE_RECORD_MISSING")
        record = F.strict(bytes(row[0]), F.MAX_RECORD)
        F.need(F.record_id(record) == identifier, "REFERENCE_RECORD_HASH")
        return record

    def map_get(self, namespace, root, feature):
        # Explicit old expanded algorithm, independent of new compressed walk.
        key, current, siblings = int(feature, 16), root, []
        empty = A.map_empty(namespace)
        for depth in range(256):
            if current == empty[depth]: left = right = empty[depth+1]
            else:
                node = self.get_node(current)
                F.need(node["kind"] == "map-node" and node["depth"] == depth, "REFERENCE_MAP_DEPTH")
                left, right = node["left"], node["right"]
            bit = (key >> (255-depth)) & 1
            siblings.append(left if bit else right); current = right if bit else left
        if current == empty[256]: return None, siblings
        leaf = self.get_node(current)
        F.need(leaf["kind"] == "map-leaf" and leaf["feature_id"] == feature, "REFERENCE_MAP_KEY")
        return leaf["feature_root"], siblings

    def summary(self, sid, descriptor, features):
        ns, rows = descriptor["namespace"], []
        for feature in features:
            root, proof = self.map_get(ns, descriptor["feature_map_root"], feature)
            parts = None if root is None else [A.partition_get(self, ns, feature, root, p)[0] for p in range(256)]
            rows.append({"feature_id": feature, "partitions": parts, "siblings": proof})
        return {"schema": "DMKN_FORMAL_QUERY_SUMMARY_V1", "namespace": ns, "snapshot_id": sid,
                "snapshot": descriptor, "features": features, "rows": rows,
                "coverage": "COMMITTED_METADATA_NOT_SOURCE_CORPUS", "mathematical_acceptance": False}


def compare_page(old, store, summary, request):
    page = store.page(request); Q.verify_page(summary, request, page)
    p, anchor, ns = request["partition"], request["anchor"], request["namespace"]
    parts = summary["partitions"][anchor]
    part = A.empty_descriptor(ns, anchor, p) if parts is None else parts[p]
    F.need(part["count"] <= 8, "FIXED_COMPARATOR_VECTOR_BOUND")
    rows, matches = [], []
    for index in range(part["count"]):
        rid, proof = A.vector_get(old, A.context(ns, anchor, p), part["count"], part["tree_root"], index)
        record = old.record(rid)
        rows.append({"ordinal": index, "record": record, "siblings": proof})
        if set(request["features"]) <= set(record["features"]): matches.append(index)
    expected = {"schema": "DMKN_FORMAL_QUERY_PAGE_V1", "namespace": ns,
        "snapshot_id": request["snapshot_id"], "query_id": Q.query_id(ns, request["features"]),
        "partition": p, "anchor": anchor, "start": 0, "next": part["count"],
        "anchor_count": part["count"], "examined": rows, "match_ordinals": matches,
        "next_cursor": None, "termination": "anchor_exhausted",
        "coverage": "COMMITTED_ANCHOR_INTERVAL_ONLY", "mathematical_acceptance": False}
    F.need(F.compact({k:v for k,v in page.items() if k != "charged"}) == F.compact(expected),
           "EXACT_PAGE_PROOF_AND_RESULT_COMPATIBILITY")
    return {"partition": p, "examined": len(rows), "matches": len(matches),
            "proof_payload_sha256": hashlib.sha256(F.compact(expected)).hexdigest(),
            "new_charged": page["charged"]}


def run(args, evidence, report):
    old_path, old_raw = pinned(args.legacy_db, args.legacy_db_sha256, 64*1024**2)
    old_bytes = len(old_raw); del old_raw
    F.need(len(args.bundle) == len(args.bundle_sha256) == 5, "EXACT_FIVE_BUNDLES")
    bundles = []
    for path, digest in zip(args.bundle, args.bundle_sha256):
        _, raw = pinned(path, digest, 16*1024**2); bundle = C.parse_json(raw)
        F.need(bundle["schema"] == "DMKN_V5_OWNER_WORKLOAD_BUNDLE_V1"
               and bundle["mathematical_admission"] is False
               and bundle["certificate_verification"] == "NOT_PERFORMED", "RETAINED_BUNDLE_PROFILE")
        F.need(C.module_id(bundle["spec"]) == bundle["module"], "RETAINED_MODULE_BINDING")
        F.need(len(bundle["openings"]) == len(bundle["spec"]["groups"]), "RETAINED_GROUP_COUNT")
        for index, opening in enumerate(bundle["openings"]):
            F.need(opening["index"] == index and C.verify_group_opening(bundle["module"], opening)
                   == bundle["spec"]["groups"][index], "RETAINED_GROUP_BINDING")
        bundles.append(bundle)
    foundation, policy = bundles[0]["spec"]["foundation"], bundles[0]["spec"]["policy"]
    F.need(all(b["spec"]["foundation"] == foundation and b["spec"]["policy"] == policy for b in bundles), "ONE_NAMESPACE")
    adapter = ModuleExportAdapter(C, foundation, policy)
    old, store = LegacyReadOnly(old_path), None
    try:
        meta = old.db.execute("SELECT cfg,objects,postings,features,snapshots FROM meta WHERE id=1").fetchone()
        cfg = F.strict(bytes(meta[0]), 16384)
        F.need(cfg["schema"] == "DMKN_DISCOVERY_STORE_V1" and cfg["namespace"] == adapter.namespace,
               "EXACT_LEGACY_STORE_PROFILE")
        F.need(tuple(meta[1:]) == (18, 362, 67, 19), "EXACT_RETAINED_NETWORK01_COUNTS")
        old_cuts = {}
        for sid, raw in old.db.execute("SELECT snapshot_id,descriptor FROM snapshots"):
            desc = F.strict(bytes(raw), 4096); F.need(A.snapshot_id(desc) == sid, "OLD_SNAPSHOT_HASH")
            F.need(desc["local_cut"] not in old_cuts, "OLD_DUPLICATE_CUT")
            old_cuts[desc["local_cut"]] = (sid, desc)
        F.need(sorted(old_cuts) == list(range(19)), "EXACT_NINETEEN_OLD_CUTS")
        records = list(old.db.execute("SELECT object_id,record_id,record,admitted_seq FROM objects ORDER BY admitted_seq"))
        F.need(len(records) == 18, "EXACT_RECORD_COUNT")
        # Only this build interval is called new index-build CPU; comparison,
        # input pinning and output reporting are reported separately/outerly.
        build_wall, build_cpu = time.monotonic(), time.process_time()
        store = Store(evidence/"compressed-index", adapter, cfg["limits"], create=True)
        new_cuts, charges, sequence = [(store.status()["latest"], store.snapshot())], [], 0
        for bundle in bundles:
            for opening in bundle["openings"]:
                for descriptor in opening["group"]["declarations"]:
                    raw = adapter.encode_opening(bundle["module"], descriptor["name"], opening)
                    result = store.admit(raw); charges.append(result["charged"]); sequence += 1
                    F.need(sequence <= 18, "BUILD_EXPORT_CAP")
                    expected = records[sequence-1]
                    F.need(result["record"]["object_id"] == expected[0]
                           and result["record_id"] == expected[1]
                           and F.compact(result["record"]) == bytes(expected[2])
                           and sequence == expected[3], "EXACT_RETAINED_EXPORT_ORDER_AND_RECORD")
                    new_cuts.append((result["snapshot_id"], store.snapshot()))
        F.need(sequence == 18, "EXACT_BUILD_EXPORT_COUNT")
        report["build"] = {"process_cpu_seconds": time.process_time()-build_cpu,
                           "wall_seconds": time.monotonic()-build_wall,
                           "admission_charges": charges, "status": store.status()}
        F.need(new_cuts == [old_cuts[i] for i in range(19)], "ALL_NINETEEN_SNAPSHOTS_EXACT")
        report["snapshot_ids"] = [row[0] for row in new_cuts]
        compare_wall, compare_cpu = time.monotonic(), time.process_time()
        proofs = 0
        final_features = [row[0] for row in old.db.execute("SELECT feature_id FROM feature_heads ORDER BY feature_id")]
        absent = hashlib.sha256(b"DMKN-COMPRESSION-ABSENT-FEATURE").hexdigest()
        F.need(absent not in final_features, "COMPARATOR_ABSENT_FEATURE")
        store._budget(60, 500000)
        with A.hash_meter(store._hash_step):
            for cut, (_, desc) in enumerate(new_cuts):
                wanted = [absent] if cut == 0 else [absent, *F.strict(bytes(records[cut-1][2]), F.MAX_RECORD)["features"]]
                if cut == 18: wanted = sorted(set([*wanted, *final_features]))
                for feature in wanted:
                    actual = A.map_get(store, adapter.namespace, desc["feature_map_root"], feature)
                    expected = old.map_get(adapter.namespace, desc["feature_map_root"], feature)
                    F.need(actual == expected, "EXACT_EXPANDED_MAP_PROOF")
                    A.verify_map(adapter.namespace, desc["feature_map_root"], feature, *actual); proofs += 1
        features = compile_query(adapter.namespace, [
            {"tag": "declaration-kind", "value": "theorem"},
            {"tag": "result-head", "head": {"tag": "const", "symbol": {"kind": "foundation-name",
             "name_hash": C.hash_value("foundation-symbol", [["s", "Eq"]])}}}])
        sid, descriptor = new_cuts[-1]
        actual_summary = store.summary(sid, features)
        reference_summary = old.summary(sid, descriptor, features)
        F.need(F.compact(actual_summary) == F.compact(reference_summary), "EXACT_SUMMARY_BYTES")
        summary = Q.verify_summary(sid, adapter.namespace, features, actual_summary)
        plans = Q.plan_partitions(summary)
        selected = [p for p in plans if p["anchor_count"]]
        F.need(len(selected) == 5, "FIVE_RETAINED_MATCH_PARTITIONS")
        selected.append(next(p for p in plans if not p["anchor_count"]))
        pages = []
        for plan in selected:
            request = {"schema": "DMKN_FORMAL_QUERY_REQUEST_V1", "namespace": adapter.namespace,
                       "snapshot_id": sid, "features": features, "partition": plan["partition"],
                       "anchor": plan["anchor"], "start": 0, "limits": dict(examined=16, matches=8,
                       bytes=262144, timeout_ms=1000, node_reads=100000)}
            pages.append(compare_page(old, store, summary, request))
        report["compatibility"] = {"snapshot_count": 19, "exact_expanded_map_proofs": proofs,
            "summary_bytes": len(F.compact(actual_summary)),
            "summary_sha256": hashlib.sha256(F.compact(actual_summary)).hexdigest(), "pages": pages,
            "legacy_node_reads": old.reads, "process_cpu_seconds": time.process_time()-compare_cpu,
            "wall_seconds": time.monotonic()-compare_wall}
        census = {}
        for encoded, in store.db.execute("SELECT encoded FROM cas_nodes"):
            node = F.strict(bytes(encoded), 4096); slot = census.setdefault(node["kind"], {"nodes": 0, "encoded_bytes": 0})
            slot["nodes"] += 1; slot["encoded_bytes"] += len(encoded)
        report["new_cas_census"] = census
        store.close(); store = None
        new_bytes = (evidence/"compressed-index"/"discovery.sqlite").stat().st_size
        report["storage"] = {"old_sqlite_bytes": old_bytes, "new_sqlite_bytes": new_bytes,
                             "reduction_fraction": 1-new_bytes/old_bytes, "required_reduction_fraction": 0.9}
        F.need(new_bytes*10 <= old_bytes, "PROSPECTIVE_NINETY_PERCENT_STORAGE_GATE")
        # Reopen new state and resolve an old cut; no migration of old evidence.
        store = Store(evidence/"compressed-index", adapter, cfg["limits"])
        F.need(store.snapshot(new_cuts[1][0]) == new_cuts[1][1], "RESTART_OLD_CUT")
        _, old_after = pinned(old_path, args.legacy_db_sha256, 64*1024**2)
        F.need(len(old_after) == old_bytes, "LEGACY_BYTES_UNCHANGED")
        report["status"] = "PASS"
    finally:
        if store is not None: store.close()
        old.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy-db", required=True); parser.add_argument("--legacy-db-sha256", required=True)
    parser.add_argument("--bundle", action="append", required=True)
    parser.add_argument("--bundle-sha256", action="append", required=True)
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args(); evidence = Path(args.evidence)
    F.need(evidence.is_absolute() and not evidence.exists(), "FRESH_ABSOLUTE_EVIDENCE")
    evidence.mkdir(parents=True)
    report = {"schema": "DMKN_COMPRESSED_INDEX_COMPARISON_V1", "status": "FAIL",
              "mathematical_acceptance": False, "network_operations": 0,
              "baseline_cpu_comparison": "UNAVAILABLE_OLD_BUILD_NOT_SEPARATELY_TIMED",
              "hash_telemetry_scope": "AUTHENTICATED_INDEX_SHA_CALLS_NOT_ALL_ADAPTER_OR_RECORD_HASHES"}
    started, cpu = time.monotonic(), time.process_time()
    try: run(args, evidence, report)
    except BaseException as error:
        report["error"] = {"type": type(error).__name__, "message": str(error)[:1000]}
    report.update(process_cpu_seconds=time.process_time()-cpu, wall_seconds=time.monotonic()-started)
    with (evidence/"RESULT.json").open("xb") as stream: stream.write(F.compact(report))
    print(F.compact({"status": report["status"], "storage": report.get("storage"), "error": report.get("error")}).decode("utf-8"))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())

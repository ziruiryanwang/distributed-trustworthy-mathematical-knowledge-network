"""Changed-boundary structural export tests; synthetic specs are NOT proofs."""
from pathlib import Path
import argparse
from copy import deepcopy
import hashlib
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C
from discovery import formal_features as F
from discovery import authenticated_index as A
from discovery import module_export_adapter as E
from discovery import discovery_store as S
from discovery import discovery_query as Q

EVIDENCE = None


def digest(text): return hashlib.sha256(text.encode("ascii")).hexdigest()
def name(text): return [["s", text]]
def const(text): return ["const", ["foundation", name(text)], []]


def specification():
    # These are metadata/AST fixtures, deliberately not claimed inhabited.
    return {"schema": C.SPEC_SCHEMA, "foundation": digest("fixture-foundation"),
            "policy": digest("fixture-policy"), "groups": [
                {"kind": "ordinary", "declarations": [{"name": name(label), "kind": "theorem",
                 "universes": 0, "type": typ, "value_hash": None, "meta": {}}]}
                for label, typ in [("onlyAlpha", const("Alpha")), ("onlyBeta", const("Beta")),
                                   ("both", ["app", const("Alpha"), const("Beta")])]]}


class ExportAdapterContracts(unittest.TestCase):
    def setUp(self):
        self.spec = specification()
        self.module = C.module_id(self.spec)
        self.adapter = E.ModuleExportAdapter(C, self.spec["foundation"], self.spec["policy"])
        self.raws = [self.adapter.encode_opening(self.module, group["declarations"][0]["name"],
                     C.group_opening(self.spec, i)) for i, group in enumerate(self.spec["groups"])]

    def test_per_export_features_do_not_union_unrelated_declarations(self):
        records = [self.adapter.extract(raw) for raw in self.raws]
        features = E.compile_query(self.adapter.namespace, [
            {"tag": "type-symbol", "symbol": {"kind": "foundation-name",
             "name_hash": C.hash_value("foundation-symbol", name(symbol))}} for symbol in ("Alpha", "Beta")])
        self.assertEqual([set(features) <= set(row["features"]) for row in records], [False, False, True])
        self.assertEqual(len({row["object_id"] for row in records}), 3)
        self.assertTrue(all(row["locator"]["module_id"] == self.module for row in records))

    def test_locator_exact_export_descriptor_and_resolution(self):
        record = self.adapter.extract(self.raws[1])
        expected = C.export_id(self.module, name("onlyBeta"))
        self.assertEqual(record["object_id"], expected)
        self.assertNotEqual(expected, self.module)
        self.assertEqual(record["locator"], {"schema": "DMKN_MODULE_EXPORT_LOCATOR_V1",
            "module_id": self.module, "group_index": 1, "relative_name": name("onlyBeta"),
            "descriptor_id": C.hash_value("declaration-descriptor", self.spec["groups"][1]["declarations"][0])})
        resolved = self.adapter.resolve(record, self.raws[1])
        self.assertFalse(resolved["mathematical_acceptance"])
        self.assertEqual(resolved["locator"]["module_id"], self.module)
        self.assertEqual(resolved["assurance"], "AUTHENTICATED_EXPORT_DESCRIPTOR")
        with self.assertRaises(ValueError): self.adapter.extract(self.raws[1], self.module)

    def test_wrapper_locator_and_opening_mutations_refuse(self):
        original = C.parse_json(self.raws[0])
        variants = []
        for field, replacement in (("module_id", digest("other-module")), ("relative_name", name("onlyBeta"))):
            item = deepcopy(original); item[field] = replacement; variants.append(item)
        item = deepcopy(original); item["opening"]["index"] = 1; variants.append(item)
        item = deepcopy(original); item["opening"]["group"]["declarations"][0]["type"] = const("Beta"); variants.append(item)
        for variant in variants:
            with self.assertRaises(ValueError): self.adapter.extract(C.canonical(variant))
        record = self.adapter.extract(self.raws[0])
        for field, replacement in (("module_id", digest("wrong")), ("group_index", 1),
                                   ("relative_name", name("wrong")), ("descriptor_id", digest("wrong"))):
            altered = deepcopy(record); altered["locator"][field] = replacement
            with self.assertRaises(ValueError): self.adapter.resolve(altered, self.raws[0])
        altered = deepcopy(record); altered["features"] = [digest("forged-feature")]
        with self.assertRaises(ValueError): self.adapter.resolve(altered, self.raws[0])

    def test_namespace_shared_across_modules_but_binds_policy(self):
        changed = deepcopy(self.spec)
        changed["groups"][0]["declarations"][0]["name"] = name("renamed")
        another = C.module_id(changed)
        self.assertNotEqual(self.module, another)
        raw = self.adapter.encode_opening(another, name("renamed"), C.group_opening(changed, 0))
        self.assertEqual(self.adapter.extract(raw)["namespace"], self.adapter.namespace)
        other_policy = E.ModuleExportAdapter(C, self.spec["foundation"], digest("different-policy"))
        self.assertNotEqual(self.adapter.namespace, other_policy.namespace)
        with self.assertRaises(ValueError): other_policy.extract(self.raws[0])

    def test_actual_store_accepts_versioned_export_records_and_pages(self):
        limits = dict(max_objects=8, max_postings=1024, max_features=1024,
                      max_snapshots=9, max_logical_bytes=33554432, max_db_pages=16384)
        store = S.Store(EVIDENCE / "export-store", self.adapter, limits, create=True)
        try:
            admitted = [store.admit(raw) for raw in self.raws]
            sid = admitted[-1]["snapshot_id"]
            self.assertEqual(store.snapshot()["feature_schema"], F.EXPORT_SCHEMA)
            feature = E.feature_id(self.adapter.namespace, {"tag": "declaration-kind", "value": "theorem"})
            summary = Q.verify_summary(sid, self.adapter.namespace, [feature], store.summary(sid, [feature]))
            found = []
            for plan in Q.plan_partitions(summary):
                if not plan["anchor_count"]: continue
                req = {"schema": "DMKN_FORMAL_QUERY_REQUEST_V1", "namespace": self.adapter.namespace,
                       "snapshot_id": sid, "features": [feature], "partition": plan["partition"],
                       "anchor": feature, "start": 0, "limits": dict(examined=8, matches=8,
                       bytes=1048576, timeout_ms=1000, node_reads=100000)}
                page = Q.verify_page(summary, req, store.page(req))
                found.extend(page["matches"])
            self.assertEqual({row["object_id"] for row in found}, {row["record"]["object_id"] for row in admitted})
            self.assertTrue(all(row["schema"] == F.EXPORT_RECORD_SCHEMA for row in found))
        finally: store.close()

    def test_v1_record_and_snapshot_hash_domains_unchanged(self):
        record = {"schema": F.RECORD_SCHEMA, "namespace": digest("v1-ns"), "kind": "synthetic-v1",
                  "object_id": digest("v1-id"), "object_sha256": digest("v1-bytes"),
                  "object_bytes": 8, "features": [digest("v1-feature")]}
        expected = hashlib.sha256(b"DMKN-FORMAL-FEATURE-RECORD-V1\0" + F.compact(record)).hexdigest()
        self.assertEqual(F.record_id(record), expected)
        descriptor = {"schema": "DMKN_FORMAL_INDEX_SNAPSHOT_V1", "namespace": record["namespace"],
                      "feature_schema": F.SCHEMA, "partition_bits": 8, "feature_map_root": digest("v1-root"),
                      "local_cut": 0, "previous_snapshot": None,
                      "coverage_claim": "PROVIDER_SELECTED_FEATURE_RECORDS_NOT_GLOBAL_CORPUS"}
        expected_snapshot = hashlib.sha256(b"DMKN-FORMAL-INDEX-SNAPSHOT-V1\0" + F.compact(descriptor)).hexdigest()
        self.assertEqual(A.snapshot_id(descriptor), expected_snapshot)


def main():
    global EVIDENCE
    parser = argparse.ArgumentParser(); parser.add_argument("--evidence", required=True)
    EVIDENCE = Path(parser.parse_args().evidence)
    if not EVIDENCE.is_absolute() or EVIDENCE.exists(): raise ValueError("FRESH_ABSOLUTE_TEST_EVIDENCE")
    EVIDENCE.mkdir(parents=True)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExportAdapterContracts)
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

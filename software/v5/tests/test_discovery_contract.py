"""Independent black-box metadata tests; synthetic rows are NOT mathematics.

The real-object adapter controls use immutable v4 fixtures, without rerunning
their mathematical checks. Pass a fresh --evidence directory for retained DBs.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import formal_features as F
from discovery import authenticated_index as A
from discovery import discovery_store as S
from discovery import discovery_query as Q

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
EVIDENCE = None
LIMITS = dict(max_objects=64, max_postings=8192, max_features=4096,
              max_snapshots=128, max_logical_bytes=67108864, max_db_pages=32768)
NS = hashlib.sha256(b"V5 independent synthetic metadata test namespace").hexdigest()
COMMON, RARE, OTHER, ABSENT = [hashlib.sha256(x).hexdigest()
                              for x in (b"common", b"rare", b"other", b"absent")]


class SyntheticAdapter:
    """Explicitly synthetic metadata only, including controllable hash buckets."""
    namespace = NS

    def extract(self, raw, expected_id=None):
        value = json.loads(raw)
        digest = hashlib.sha256(raw).hexdigest()
        identifier = f'{value["partition"]:02x}' + digest[2:]
        if expected_id is not None and expected_id != identifier:
            raise ValueError("SYNTHETIC_ID")
        return {"schema": F.RECORD_SCHEMA, "namespace": NS, "kind": "synthetic-test-only",
                "object_id": identifier, "object_sha256": digest, "object_bytes": len(raw),
                "features": sorted(value["features"])}


def raw(i, partition=7):
    features = [COMMON]
    if i in (1, 4, 7, 10):
        features.append(RARE)
    if i in (0, 1, 2, 3, 4, 5, 6, 8, 9):
        features.append(OTHER)
    return F.compact({"partition": partition, "features": sorted(features), "payload": i})


def request(summary, partition, *, start=0, examined=2, matches=1, byte_limit=1048576):
    plan = Q.plan_partitions(summary)[partition]
    return {"schema": "DMKN_FORMAL_QUERY_REQUEST_V1", "namespace": summary["namespace"],
            "snapshot_id": summary["snapshot_id"], "features": summary["features"],
            "partition": partition, "anchor": plan["anchor"], "start": start,
            "limits": {"examined": examined, "matches": matches, "bytes": byte_limit,
                       "timeout_ms": 1000, "node_reads": 100000}}


class DiscoveryContracts(unittest.TestCase):
    def setUp(self):
        self.root = EVIDENCE / self._testMethodName
        self.root.mkdir()
        self.stores = []
        self.adapter = SyntheticAdapter()
        self.store = self.open("primary")
        self.raws = [raw(i) for i in range(12)] + [raw(90, 99)]
        for value in self.raws:
            self.snapshot = self.store.admit(value)["snapshot_id"]

    def open(self, name, limits=None):
        store = S.Store(self.root / name, self.adapter, limits or LIMITS, create=True)
        self.stores.append(store)
        return store

    def tearDown(self):
        for store in reversed(self.stores):
            store.close()

    def summary(self, features, snapshot=None, store=None):
        selected = snapshot or self.snapshot
        features = sorted(features)
        response = (store or self.store).summary(selected, features)
        return Q.verify_summary(selected, NS, features, response)

    def drain(self, store, summary, partition):
        start, out, pages, covered = 0, [], [], Q.Coverage(summary)
        count = Q.plan_partitions(summary)[partition]["anchor_count"]
        while start < count:
            self.assertLess(len(pages), 32, "finite test loop")
            req = request(summary, partition, start=start)
            response = store.page(req)
            verified = Q.verify_page(summary, req, response)
            self.assertFalse(verified["mathematical_acceptance"])
            self.assertEqual(verified["assurance"], "VERIFIED_COMMITTED_INTERVAL")
            self.assertGreater(verified["next"], start)
            out.extend(row["object_id"] for row in verified["matches"])
            covered.accept(req, response)
            pages.append((req, response))
            start = verified["next"]
        return out, covered.report(), pages

    def test_rarest_anchor_exact_filter_and_partial_coverage(self):
        summary = self.summary([COMMON, RARE, OTHER])
        plan = Q.plan_partitions(summary)
        self.assertEqual(plan[7]["anchor"], RARE)
        self.assertEqual(plan[7]["anchor_count"], 4)
        found, report, pages = self.drain(self.store, summary, 7)
        expected = [self.adapter.extract(raw(i))["object_id"] for i in (1, 4)]
        self.assertEqual(found, expected)
        self.assertTrue(report["partitions"][7]["complete_committed_anchor"])
        self.assertFalse(report["global_complete"])
        self.assertFalse(report["mathematical_acceptance"])
        self.assertEqual(report["build_assurance"], "NOT_PROVIDED")
        self.assertGreaterEqual(len(pages), 2)

    def test_last_page_does_not_authenticate_earlier_pages(self):
        summary = self.summary([COMMON])
        req = request(summary, 7, start=11)
        coverage = Q.Coverage(summary)
        coverage.accept(req, self.store.page(req))
        report = coverage.report()
        self.assertFalse(report["partitions"][7]["complete_committed_anchor"])
        self.assertFalse(report["complete_committed_anchor_domain"])

    def test_portable_continuation_and_old_snapshot_after_admission(self):
        replica = self.open("replica")
        for value in self.raws:
            replica_id = replica.admit(value)["snapshot_id"]
        self.assertEqual(replica_id, self.snapshot)
        summary = self.summary([COMMON])
        req = request(summary, 7)
        first = Q.verify_page(summary, req, self.store.page(req))
        newer = self.store.admit(raw(98))["snapshot_id"]
        self.assertNotEqual(newer, self.snapshot)
        continuation = request(summary, 7, start=first["next"])
        continued = Q.verify_page(summary, continuation, replica.page(continuation))
        self.assertEqual(continued["start"], first["next"])
        old_results, _, _ = self.drain(self.store, summary, 7)
        new_results, _, _ = self.drain(self.store, self.summary([COMMON], newer), 7)
        self.assertEqual(len(old_results), 12)
        self.assertEqual(len(new_results), 13)

    def test_omission_false_filter_wrong_context_and_root_refuse(self):
        summary = self.summary([COMMON, RARE, OTHER])
        req = request(summary, 7, examined=4, matches=8)
        response = self.store.page(req)
        Q.verify_page(summary, req, response)
        variants = []
        missing = copy.deepcopy(response)
        missing["examined"].pop(0)
        variants.append(missing)
        filtering = copy.deepcopy(response)
        filtering["match_ordinals"] = []
        variants.append(filtering)
        wrong_context = copy.deepcopy(response)
        wrong_context["partition"] = 8
        variants.append(wrong_context)
        wrong_root = copy.deepcopy(response)
        wrong_root["snapshot_id"] = "f" * 64
        variants.append(wrong_root)
        for value in variants:
            with self.subTest(tamper=len(F.compact(value))):
                with self.assertRaises(ValueError):
                    Q.verify_page(summary, req, value)

    def test_summary_tamper_and_byte_budget(self):
        features = [COMMON]
        response = self.store.summary(self.snapshot, features)
        damaged = copy.deepcopy(response)
        damaged["snapshot_id"] = "0" * 64
        with self.assertRaises(ValueError):
            Q.verify_summary(self.snapshot, NS, features, damaged)
        with self.assertRaises(ValueError):
            self.store.summary(self.snapshot, features, max_bytes=1024)

    def test_duplicate_and_quota_failure_are_atomic(self):
        small = self.open("small", {**LIMITS, "max_objects": 1})
        first = small.admit(raw(0))
        duplicate = small.admit(raw(0))
        self.assertEqual(first["snapshot_id"], duplicate["snapshot_id"])
        self.assertFalse(duplicate["new"])
        with self.assertRaises(ValueError):
            small.admit(raw(1))
        summary = self.summary([COMMON], first["snapshot_id"], small)
        self.assertEqual(Q.plan_partitions(summary)[7]["anchor_count"], 1)

    def test_authenticated_absence_is_not_global_absence(self):
        summary = self.summary([ABSENT])
        plans = Q.plan_partitions(summary)
        self.assertTrue(all(p["committed_empty"] for p in plans))
        report = Q.Coverage(summary).report()
        self.assertTrue(report["complete_committed_anchor_domain"])
        self.assertFalse(report["global_complete"])
        self.assertEqual(report["build_assurance"], "NOT_PROVIDED")


class ActualAdapterContracts(unittest.TestCase):
    """New feature extraction over frozen inputs; no old proof suite rerun."""

    @classmethod
    def setUpClass(cls):
        base = ROOT / "product-local/v4-library-commons-02/commons-v4"
        def load(name, relative, expected):
            path = base / relative
            contents = path.read_bytes()
            if hashlib.sha256(contents).hexdigest() != expected:
                raise ValueError("FROZEN_ADAPTER_INPUT_PIN")
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            exec(compile(contents, str(path), "exec"), module.__dict__)
            return module
        cls.library = load("_v5_fixture_library", "library/library_codec.py",
            "9480ce938123c910ecbecddb55ba18d1e748505acc0202dd8fc7dcef56f46a36")
        cls.codec = load("_v5_fixture_codec", "receiver/cert_capsule.py",
            "b534e60eb02667050d895f272a567560cfbacd76010565834716c474cb76d967")
        registry_raw = (base / "receiver/assets/registry.json").read_bytes()
        if hashlib.sha256(registry_raw).hexdigest() != "63bb37cc7b51bb77dcbae152a0cba1b82ae7925d6ca0822327d3470adb5729e1":
            raise ValueError("FROZEN_REGISTRY_PIN")
        cls.adapter = F.NamedModuleAdapter(cls.library, cls.codec, json.loads(registry_raw))
        cls.parent = "af026e83f6f01326e947ab436c6f4041997a40332bb71c6be154ff7c0df24036"
        cls.child = "4f3bbca156bd548591b9d22abae15990a79f26ae4951a391accc991415225ced"
        fixture = ROOT / "experiments/named-library-01/fixtures01/modules"
        cls.value = (fixture / (cls.child + ".json")).read_bytes()
        if hashlib.sha256(cls.value).hexdigest() != "c76dc024e13731c843281f9fe32876469cd6c5cdabb7592cf6e2fb114ace1c91":
            raise ValueError("FROZEN_FIXTURE_PIN")

    def test_real_declared_type_excludes_value_only_import_symbols(self):
        described = self.adapter.describe(self.value, self.child)
        self.assertFalse(described["mathematical_acceptance"])
        specs = described["specs"]
        graph = self.codec.Graph()
        for row in json.loads(self.value)["graph"]:
            graph.push(row)
        # This fixture's declared type is (A : Sort u) -> (A -> A -> A)
        # -> Nat -> A -> A. Its body, but NOT type, refers to the imported iterator.
        expected_nat = {"tag": "type-symbol", "symbol": {
            "kind": "foundation-name", "name_hash": graph.hashes["name"][9]}}
        self.assertEqual([x for x in specs if x["tag"] == "type-symbol"], [expected_nat])
        self.assertEqual([x for x in specs if x["tag"] == "direct-import"],
                         [{"tag": "direct-import", "module_id": self.parent}])
        self.assertIn({"tag": "result-head", "head": {"tag": "bvar"}}, specs)
        query = F.compile_query(self.adapter.namespace, [expected_nat,
                 {"tag": "direct-import", "module_id": self.parent}])
        self.assertTrue(set(query) <= set(described["record"]["features"]))

    def test_real_canonical_mutation_cannot_keep_original_id(self):
        changed = json.loads(self.value)
        changed["graph"][1]["str"]["str"] = "AnotherDisplayName"
        with self.assertRaises(ValueError):
            self.adapter.extract(F.compact(changed), self.child)


def main():
    global EVIDENCE
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args()
    EVIDENCE = Path(args.evidence)
    if not EVIDENCE.is_absolute() or EVIDENCE.exists():
        raise ValueError("FRESH_ABSOLUTE_TEST_EVIDENCE")
    EVIDENCE.mkdir(parents=True)
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

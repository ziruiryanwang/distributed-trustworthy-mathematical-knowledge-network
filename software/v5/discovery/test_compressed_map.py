"""Focused V2 physical-map contracts. Root selects execution; no networking."""
from pathlib import Path
import argparse
from copy import deepcopy
import hashlib
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import authenticated_index as A
from discovery import formal_features as F
from discovery import discovery_store as S
from discovery import discovery_query as Q

EVIDENCE = None


def key(text): return hashlib.sha256(text.encode("ascii")).hexdigest()


def reference_hash(domain, *parts):
    return hashlib.sha256(("DMKN-DISCOVERY-"+domain+"-V1").encode("ascii")
                          + b"\0" + b"".join(parts)).hexdigest()


class ExpandedReference:
    """Independent old expanded-map algorithm: no new map/run routines."""
    def __init__(self, namespace):
        self.namespace, self.nodes = namespace, {}
        self.empty = [None]*257
        self.empty[256] = reference_hash("MAP-EMPTY-LEAF", bytes.fromhex(namespace))
        for d in range(255, -1, -1):
            self.empty[d] = self.branch_hash(d, self.empty[d+1], self.empty[d+1])

    @staticmethod
    def branch_hash(depth, left, right):
        return reference_hash("MAP-NODE", depth.to_bytes(2, "big"), bytes.fromhex(left), bytes.fromhex(right))

    def get(self, root, feature):
        current, siblings, selected = root, [], int(feature, 16)
        for d in range(256):
            if current == self.empty[d]: left = right = self.empty[d+1]
            else:
                depth, left, right = self.nodes[current]
                if depth != d: raise ValueError("REFERENCE_DEPTH")
            bit = (selected >> (255-d)) & 1
            siblings.append(left if bit else right); current = right if bit else left
        if current == self.empty[256]: return None, siblings
        actual_key, value = self.nodes[current]
        if actual_key != feature: raise ValueError("REFERENCE_KEY")
        return value, siblings

    def set(self, root, feature, value):
        _, siblings = self.get(root, feature)
        current = reference_hash("MAP-LEAF", bytes.fromhex(feature), bytes.fromhex(value))
        self.nodes[current] = (feature, value)
        for d in range(255, -1, -1):
            left, right = (siblings[d], current) if (int(feature, 16) >> (255-d)) & 1 else (current, siblings[d])
            current = self.branch_hash(d, left, right); self.nodes[current] = (d, left, right)
        return current


class Memory:
    def __init__(self): self.nodes = {}
    def get_node(self, identifier): return deepcopy(self.nodes[identifier])
    def put_node(self, node):
        identifier = A.node_hash(node)
        if identifier in self.nodes and self.nodes[identifier] != node: raise ValueError("CAS_CONFLICT")
        self.nodes[identifier] = deepcopy(node)
        return identifier


def reachable(io, root):
    seen, todo = set(), [root]
    while todo:
        current = todo.pop()
        if current in seen: continue
        seen.add(current); node = io.nodes[current]
        if node["kind"] == "map-node": todo.extend([node["left"], node["right"]])
        elif node["kind"] == "map-run": todo.append(node["child"])
    return len(seen)


class CompressedMapContracts(unittest.TestCase):
    def test_independent_roots_proofs_old_cuts_long_prefixes_and_bound(self):
        ns = key("compression-independent"); io = Memory(); ref = ExpandedReference(ns)
        root, expected = A.map_empty(ns)[0], ref.empty[0]
        keys = [f"{v:064x}" for v in (0, 1, 2, 1 << 255, 1 << 128, (1 << 128)+1, (1 << 256)-1)]
        absent = f"{17:064x}"
        cuts, present = [(root, {})], {}
        for index, feature in enumerate([*keys, keys[0], keys[4], keys[-1]]):
            value = key("value-"+str(index)); present[feature] = value
            root = A.map_set(io, ns, root, feature, value); expected = ref.set(expected, feature, value)
            self.assertEqual(root, expected)
            self.assertLessEqual(reachable(io, root), 4*len(present)-2)
            for selected in [*keys, absent]:
                actual = A.map_get(io, ns, root, selected)
                self.assertEqual(actual, ref.get(expected, selected))
                A.verify_map(ns, root, selected, *actual)
            cuts.append((root, dict(present)))
        for old_root, old_values in cuts:
            for selected in [*keys, absent]:
                actual = A.map_get(io, ns, old_root, selected)
                self.assertEqual(actual[0], old_values.get(selected))
                A.verify_map(ns, old_root, selected, *actual)
        # A no-op replacement preserves both root and canonical physical bytes.
        self.assertEqual(root, A.map_set(io, ns, root, keys[-1], present[keys[-1]]))

    def test_invalid_run_fields_and_physical_noncanonicality_refuse(self):
        ns, feature = key("run-shape"), "00"*32
        leaf = {"kind": "map-leaf", "feature_id": feature, "feature_root": key("value")}
        template = {"kind": "map-run", "namespace": ns, "depth": 0, "end_depth": 256,
                    "path": feature, "child": A.node_hash(leaf)}
        for field, value in (("depth", -1), ("depth", True), ("end_depth", 0),
                             ("end_depth", 257), ("path", "X"*64),
                             ("child", A.map_empty(ns)[256]), ("namespace", "bad")):
            invalid = {**template, field: value}
            with self.subTest(field=field, value=value), self.assertRaises(ValueError): A.node_hash(invalid)
        with self.assertRaisesRegex(ValueError, "MAP_RUN_PATH_MASK"):
            A.node_hash({**template, "depth": 1, "path": "80"+"00"*31})
        io = Memory(); child = io.put_node(leaf)
        inner = io.put_node({**template, "depth": 128, "child": child})
        outer = io.put_node({**template, "end_depth": 128, "child": inner})
        with self.assertRaisesRegex(ValueError, "MAP_ENDPOINT_BRANCH"):
            A.map_get(io, ns, outer, feature)
        valid_io = Memory(); child = valid_io.put_node(leaf)
        valid = valid_io.put_node({**template, "child": child})
        with self.assertRaisesRegex(ValueError, "MAP_RUN_CONTEXT"):
            A.map_get(valid_io, key("wrong-ns"), valid, feature)
        valid_io.nodes[valid]["child"] = key("corrupt-child")
        with self.assertRaisesRegex(ValueError, "AUTHENTICATED_NODE_BINDING"):
            A.map_get(valid_io, ns, valid, feature)


NS, FEATURE = key("sqlite-compression"), key("sqlite-feature")


class Adapter:
    namespace = NS
    def extract(self, raw, expected_id=None):
        digest = hashlib.sha256(raw).hexdigest()
        return {"schema": F.RECORD_SCHEMA, "namespace": NS, "kind": "compression-fixture",
                "object_id": "07"+digest[2:], "object_sha256": digest,
                "object_bytes": len(raw), "features": [FEATURE]}


LIMITS = dict(max_objects=8, max_postings=8, max_features=8,
              max_snapshots=9, max_logical_bytes=4194304, max_db_pages=4096)


class FaultStore(S.Store):
    expire_on_seal = False
    exhaust_hashes = False
    def _budget(self, *args, **kwargs):
        super()._budget(*args, **kwargs)
        if self.exhaust_hashes: self.hash_cap = 0
    def _seal(self):
        result = super()._seal()
        if self.expire_on_seal: self.until = float("-inf")
        return result


class CompressedStoreContracts(unittest.TestCase):
    def test_smaller_read_prelude_and_hash_accounting(self):
        store = S.Store(EVIDENCE/"read-budget", Adapter(), LIMITS, create=True)
        try:
            for i in range(4): result = store.admit(F.compact({"fixture": i}))
            self.assertGreater(result["charged"]["index_hash_steps"], 0)
            sid = result["snapshot_id"]
            summary = Q.verify_summary(sid, NS, [FEATURE], store.summary(sid, [FEATURE]))
            request = {"schema": "DMKN_FORMAL_QUERY_REQUEST_V1", "namespace": NS,
                       "snapshot_id": sid, "features": [FEATURE], "partition": 7,
                       "anchor": FEATURE, "start": 0, "limits": dict(examined=32, matches=8,
                       bytes=1048576, timeout_ms=1000, node_reads=15)}
            #3 map accesses (run, checked endpoint, traversed leaf) +9 partition.
            #One width4 membership adds3, with cap checked before increment.
            page = store.page(request); verified = Q.verify_page(summary, request, page)
            self.assertEqual((verified["next"], verified["termination"]), (1, "work_exhausted"))
            self.assertEqual(page["charged"], {"node_reads": 15, "examined": 1})
            request["limits"]["node_reads"] = 12
            page = store.page(request); verified = Q.verify_page(summary, request, page)
            self.assertEqual((verified["next"], verified["termination"]), (0, "work_exhausted"))
            self.assertEqual(page["charged"], {"node_reads": 12, "examined": 0})
            request["limits"]["node_reads"] = 11
            with self.assertRaisesRegex(ValueError, "NODE_READ_CAP"): store.page(request)
        finally: store.close()

    def test_deadline_hash_cap_and_quota_rollback_then_restart(self):
        root = EVIDENCE/"rollback"; store = FaultStore(root, Adapter(), LIMITS, create=True)
        try:
            old = store.status(); old_nodes = store.db.execute("SELECT count(*) FROM cas_nodes").fetchone()[0]
            store.expire_on_seal = True
            with self.assertRaisesRegex(ValueError, "DISCOVERY_TIME_EXHAUSTED"): store.admit(b"expiry")
            self.assertEqual(store.status(), old)
            self.assertEqual(store.db.execute("SELECT count(*) FROM cas_nodes").fetchone()[0], old_nodes)
            self.assertEqual(store._node_cache, {})
            store.expire_on_seal = False; store.exhaust_hashes = True
            with self.assertRaisesRegex(ValueError, "INDEX_HASH_CAP"): store.admit(b"hash-cap")
            self.assertEqual(store.status(), old)
            self.assertEqual(store.work["index_hash_steps"], 0)
            store.exhaust_hashes = False; accepted = store.admit(b"accepted")
        finally: store.close()
        store = S.Store(root, Adapter(), LIMITS)
        try:
            self.assertEqual(store.status()["latest"], accepted["snapshot_id"])
            self.assertFalse(store.admit(b"accepted")["new"])
            summary = store.summary(accepted["snapshot_id"], [FEATURE])
            Q.verify_summary(accepted["snapshot_id"], NS, [FEATURE], summary)
        finally: store.close()
        tiny = S.Store(EVIDENCE/"quota", Adapter(), {**LIMITS, "max_logical_bytes": 1024}, create=True)
        try:
            old = tiny.status()
            with self.assertRaisesRegex(ValueError, "LOGICAL_BYTE_CAP"): tiny.admit(b"too-large")
            self.assertEqual(tiny.status(), old)
            self.assertEqual(tiny.db.execute("SELECT count(*) FROM cas_nodes").fetchone()[0], 0)
        finally: tiny.close()

    def test_cache_is_not_mutable_authority_and_cas_conflict_remains(self):
        store = S.Store(EVIDENCE/"conflict", Adapter(), LIMITS, create=True)
        try:
            accepted = store.admit(b"one")
            root = store.snapshot(accepted["snapshot_id"])["feature_map_root"]
            node = store.get_node(root); self.assertEqual(node["kind"], "map-run")
            saved = deepcopy(node); node["child"] = key("caller-mutation")
            self.assertEqual(store.get_node(root), saved)
            # A different valid physical encoding shares the logical hash. It
            # must not be silently accepted as an exact-byte CAS duplicate.
            values = A._run_values(saved); bit = (int(saved["path"], 16) >> 255) & 1
            alternate = {"kind": "map-node", "depth": 0,
                         "left": A.map_empty(NS)[1] if bit else values[1],
                         "right": values[1] if bit else A.map_empty(NS)[1]}
            self.assertEqual(A.node_hash(alternate), root)
            store.db.execute("BEGIN IMMEDIATE")
            try:
                store.db.execute("UPDATE cas_nodes SET encoded=? WHERE hash=?", (F.compact(alternate), root))
                with self.assertRaisesRegex(ValueError, "CAS_CONFLICT"): store.put_node(saved)
            finally: store.db.execute("ROLLBACK")
            store._budget(5, 1000, 1000)
            with self.assertRaisesRegex(ValueError, "MAP_UNCOMPRESSED_UNARY"): store.put_node(alternate)
        finally: store.close()

    def test_new_disk_profile_is_explicit_and_run_corruption_refuses(self):
        root = EVIDENCE/"profile"; store = S.Store(root, Adapter(), LIMITS, create=True)
        try:
            accepted = store.admit(b"one")
            cfg = F.strict(bytes(store.db.execute("SELECT cfg FROM meta WHERE id=1").fetchone()[0]), 16384)
            self.assertEqual((cfg["schema"], cfg["map_encoding"]), (S.STORE_SCHEMA, S.MAP_ENCODING))
            maproot = store.snapshot()["feature_map_root"]; node = store.get_node(maproot)
            node["path"] = f"{int(node['path'],16)^1:064x}"
            store.db.execute("UPDATE cas_nodes SET encoded=? WHERE hash=?", (F.compact(node), maproot))
            with self.assertRaisesRegex(ValueError, "CAS_NODE_HASH"):
                store.summary(accepted["snapshot_id"], [FEATURE])
        finally: store.close()


def main():
    global EVIDENCE
    parser = argparse.ArgumentParser(); parser.add_argument("--evidence", required=True)
    EVIDENCE = Path(parser.parse_args().evidence)
    if not EVIDENCE.is_absolute() or EVIDENCE.exists(): raise ValueError("FRESH_ABSOLUTE_TEST_EVIDENCE")
    EVIDENCE.mkdir(parents=True)
    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(cls)
                               for cls in (CompressedMapContracts, CompressedStoreContracts)])
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

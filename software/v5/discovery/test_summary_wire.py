"""Focused sparse-wire tests using independently built expanded map proofs.

Synthetic metadata authenticates a chosen index, not mathematical theorems.
Root selects execution; no Store, network, verifier worker or filesystem writes.
"""
from copy import deepcopy
import hashlib
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import formal_features as F
from discovery import authenticated_index as A
from discovery import discovery_query as Q
from discovery import summary_wire as W


def key(text): return hashlib.sha256(text.encode("ascii")).hexdigest()


def H(domain, *parts):
    return hashlib.sha256(("DMKN-DISCOVERY-"+domain+"-V1").encode("ascii") + b"\0" + b"".join(parts)).hexdigest()


def expanded_map(namespace, bindings):
    """Old full-path map construction; does not use map-run or wire helpers."""
    empty, nodes = [None]*257, {}
    empty[256] = H("MAP-EMPTY-LEAF", bytes.fromhex(namespace))
    def branch(depth, left, right):
        return H("MAP-NODE", depth.to_bytes(2, "big"), bytes.fromhex(left), bytes.fromhex(right))
    for d in range(255, -1, -1): empty[d] = branch(d, empty[d+1], empty[d+1])
    def get(root, feature):
        current, siblings = root, []
        for d in range(256):
            left, right = (empty[d+1], empty[d+1]) if current == empty[d] else nodes[current]
            bit = (int(feature,16) >> (255-d)) & 1
            siblings.append(left if bit else right); current = right if bit else left
        return (None if current == empty[256] else nodes[current][1]), siblings
    root = empty[0]
    for feature, selected in sorted(bindings.items()):
        _, proof = get(root, feature)
        current = H("MAP-LEAF", bytes.fromhex(feature), bytes.fromhex(selected)); nodes[current] = (feature, selected)
        for d in range(255, -1, -1):
            left, right = (proof[d], current) if (int(feature,16) >> (255-d)) & 1 else (current, proof[d])
            current = branch(d, left, right); nodes[current] = (left, right)
        root = current
    return root, get, empty


def fixture():
    ns = key("summary-wire-namespace")
    filled, empty, absent = (key(label) for label in ("filled-feature", "empty-feature", "absent-feature"))
    features = sorted([filled, empty, absent])
    partitions = {feature: [A.empty_descriptor(ns, feature, p) for p in range(256)] for feature in (filled, empty)}
    partitions[filled][0] = {"partition": 0, "count": 1, "tree_root": key("first-vector")}
    partitions[filled][255] = {"partition": 255, "count": A.MAX_VECTOR, "tree_root": key("last-vector")}
    root, get, defaults = expanded_map(ns, {f: A.feature_root(ns, f, rows) for f, rows in partitions.items()})
    desc = {"schema": "DMKN_FORMAL_INDEX_SNAPSHOT_V1", "namespace": ns, "feature_schema": F.SCHEMA,
            "partition_bits": 8, "feature_map_root": root, "local_cut": 2, "previous_snapshot": None,
            "coverage_claim": "PROVIDER_SELECTED_FEATURE_RECORDS_NOT_GLOBAL_CORPUS"}
    sid = A.snapshot_id(desc)
    summary = {"schema": "DMKN_FORMAL_QUERY_SUMMARY_V1", "namespace": ns, "snapshot_id": sid,
               "snapshot": desc, "features": features, "rows": [{"feature_id": f,
               "partitions": partitions.get(f), "siblings": get(root, f)[1]} for f in features],
               "coverage": "COMMITTED_METADATA_NOT_SOURCE_CORPUS", "mathematical_acceptance": False}
    # Separate straightforward spelling of the selected compact format.
    compact = {**deepcopy(summary), "schema": "DMKN_FORMAL_QUERY_SUMMARY_COMPACT_V1",
               "rows": [{"feature_id": row["feature_id"], "presence": "absent" if row["partitions"] is None else "present",
               "partitions": [] if row["partitions"] is None else [deepcopy(d) for d in row["partitions"] if d["count"]],
               "siblings": [[d, h] for d, h in enumerate(row["siblings"]) if h != defaults[d+1]]}
               for row in summary["rows"]]}
    return ns, sid, features, summary, compact, (filled, empty, absent), defaults


class SummaryWireContracts(unittest.TestCase):
    def setUp(self):
        self.ns, self.sid, self.features, self.expanded, self.sparse, self.names, self.defaults = fixture()
        self.raw = F.compact(self.sparse)

    def decode(self, value, **kwargs):
        return W.decode_summary(F.compact(value), self.sid, self.ns, self.features, **kwargs)

    def test_exact_roundtrip_independent_encoding_and_existing_verifier(self):
        encoded = W.encode_summary(self.expanded, self.sid, self.ns, self.features)
        self.assertEqual(encoded, self.raw)
        decoded = W.decode_summary(encoded, self.sid, self.ns, self.features)
        self.assertEqual(F.compact(decoded), F.compact(self.expanded))
        self.assertEqual(Q.verify_summary(self.sid, self.ns, self.features, decoded),
                         Q.verify_summary(self.sid, self.ns, self.features, self.expanded))
        self.assertLess(len(encoded), len(F.compact(self.expanded))//5)
        self.assertEqual(W.encode_summary(decoded, self.sid, self.ns, self.features), encoded)

    def test_sparse_ranges_order_duplicates_and_defaults_are_rejected(self):
        filled = self.features.index(self.names[0]); variants = []
        def variant():
            value = deepcopy(self.sparse); variants.append(value); return value["rows"][filled]
        variant()["partitions"].append(deepcopy(self.sparse["rows"][filled]["partitions"][0]))
        variant()["partitions"].reverse()
        for field, values in (("partition", (-1, 256, True)), ("count", (0, -1, True, A.MAX_VECTOR+1)),
                              ("tree_root", ("bad",))):
            for value in values: variant()["partitions"][0][field] = value
        variant()["siblings"] = [[0, key("x")], [0, key("y")]]
        variant()["siblings"] = [[255, key("x")], [0, key("y")]]
        variant()["siblings"] = [[0, self.defaults[1]]]
        for depth in (-1, 256, True): variant()["siblings"] = [[depth, key("x")]]
        variant()["siblings"] = [[0, "bad"]]
        variant()["siblings"] = [[0, key("x"), "extra"]]
        variant()["siblings"] = [[0, key("x")]]*257
        variant()["partitions"] = [self.sparse["rows"][filled]["partitions"][0]]*257
        variant()["unexpected"] = 1
        for index, value in enumerate(variants):
            with self.subTest(mutation=index), self.assertRaises(ValueError): self.decode(value)

    def test_absent_and_empty_present_distinct_and_decoding_is_not_authentication(self):
        filled, empty, absent = [self.features.index(n) for n in self.names]
        self.assertEqual(self.sparse["rows"][empty]["partitions"], [])
        self.assertEqual(self.sparse["rows"][absent]["partitions"], [])
        self.assertNotEqual(self.sparse["rows"][empty]["presence"], self.sparse["rows"][absent]["presence"])
        self.assertIsNone(self.decode(self.sparse)["rows"][absent]["partitions"])
        self.assertEqual(len(self.decode(self.sparse)["rows"][empty]["partitions"]), 256)
        variants = []
        value = deepcopy(self.sparse); value["rows"][filled]["partitions"].pop(); variants.append(value)
        value = deepcopy(self.sparse); value["rows"][filled]["siblings"].pop(); variants.append(value)
        value = deepcopy(self.sparse); value["rows"][empty]["presence"] = "absent"; variants.append(value)
        value = deepcopy(self.sparse); value["rows"][filled]["partitions"][0]["count"] = 2; variants.append(value)
        for index, value in enumerate(variants):
            decoded = self.decode(value)  # Structurally valid, NOT authenticated.
            with self.subTest(mutation=index), self.assertRaises(ValueError):
                Q.verify_summary(self.sid, self.ns, self.features, decoded)
        value = deepcopy(self.sparse); value["rows"][filled]["presence"] = "absent"
        with self.assertRaisesRegex(ValueError, "SUMMARY_WIRE_ABSENT_PARTITIONS"): self.decode(value)

    def test_snapshot_query_namespace_and_assurance_bindings(self):
        variants = []
        for field, value in (("schema", W.EXPANDED_SCHEMA), ("namespace", key("other")),
                             ("snapshot_id", key("other")), ("features", list(reversed(self.features))),
                             ("coverage", "GLOBAL_COMPLETE"), ("mathematical_acceptance", True)):
            variants.append({**deepcopy(self.sparse), field: value})
        changed = deepcopy(self.sparse); changed["snapshot"]["local_cut"] += 1; variants.append(changed)
        changed = deepcopy(self.sparse); changed["rows"].reverse(); variants.append(changed)
        changed = deepcopy(self.sparse); changed["rows"][0]["presence"] = "unknown"; variants.append(changed)
        changed = deepcopy(self.sparse); changed["rows"].append(changed["rows"][0]); variants.append(changed)
        for index, value in enumerate(variants):
            with self.subTest(mutation=index), self.assertRaises(ValueError): self.decode(value)
        with self.assertRaises(ValueError): W.decode_summary(self.raw, key("wrong-pin"), self.ns, self.features)
        with self.assertRaises(ValueError): W.decode_summary(self.raw, self.sid, key("wrong-ns"), self.features)

    def test_exact_byte_limits_preallocation_guard_and_detached_results(self):
        expanded_bytes = len(F.compact(self.expanded))
        decoded = self.decode(self.sparse, max_wire_bytes=len(self.raw), max_expanded_bytes=expanded_bytes)
        self.assertEqual(decoded, self.expanded)
        with patch.object(A, "empty_descriptor", side_effect=AssertionError("EXPANSION_MUST_NOT_START")):
            with self.assertRaisesRegex(ValueError, "SUMMARY_EXPANSION_BYTES"):
                self.decode(self.sparse, max_expanded_bytes=expanded_bytes-1)
        with self.assertRaises(ValueError): self.decode(self.sparse, max_wire_bytes=len(self.raw)-1)
        for limits in ({"max_wire_bytes": True}, {"max_expanded_bytes": 0}, {"max_expanded_bytes": W.MAX_BYTES+1}):
            with self.assertRaises(ValueError): self.decode(self.sparse, **limits)
        def refuse(): raise ValueError("OWNER_BUDGET_EXHAUSTED")
        with self.assertRaisesRegex(ValueError, "OWNER_BUDGET_EXHAUSTED"):
            self.decode(self.sparse, check_budget=refuse)
        decoded["snapshot"]["local_cut"] = 77
        self.assertEqual(self.decode(self.sparse), self.expanded)
        self.assertEqual(W.encode_summary(self.expanded, self.sid, self.ns, self.features), self.raw)

    def test_noncanonical_json_duplicate_keys_and_nested_payload_refuse(self):
        samples = [self.raw+b"\n", b'{"schema":1,"schema":2}', b"["*33+b"0"+b"]"*33,
                   b'{"schema":1.0}', self.raw.replace(b'"local_cut":2', b'"local_cut":2.0')]
        for index, raw in enumerate(samples):
            with self.subTest(mutation=index), self.assertRaises(ValueError):
                W.decode_summary(raw, self.sid, self.ns, self.features)

    def test_expanded_encoder_rejects_malformed_arrays_and_false_empty_values(self):
        filled = self.features.index(self.names[0]); variants = []
        value = deepcopy(self.expanded); value["rows"][filled]["partitions"].pop(); variants.append(value)
        value = deepcopy(self.expanded); value["rows"][filled]["partitions"][1]["tree_root"] = key("wrong-empty"); variants.append(value)
        value = deepcopy(self.expanded); value["rows"][filled]["partitions"][0]["partition"] = True; variants.append(value)
        value = deepcopy(self.expanded); value["rows"][filled]["siblings"].pop(); variants.append(value)
        value = deepcopy(self.expanded); value["rows"][filled]["siblings"][0] = "bad"; variants.append(value)
        for index, value in enumerate(variants):
            with self.subTest(mutation=index), self.assertRaises(ValueError):
                W.encode_summary(value, self.sid, self.ns, self.features)
        with self.assertRaisesRegex(ValueError, "SUMMARY_WIRE_BYTES"):
            W.encode_summary(self.expanded, self.sid, self.ns, self.features, max_wire_bytes=len(self.raw)-1)


if __name__ == "__main__": unittest.main(verbosity=2)

"""Changed pair-index boundaries, with structural/inert fixtures only.

No mathematical authority, proof, native verification or network is created.
Real SQLite Store/query and workspace persistence are exercised. The hot-list
fixture has explicitly synthetic IDs and types, not accepted mathematics.
"""
import asyncio
from copy import deepcopy
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import socket
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE / "portable_runtime"), str(SOURCE)]


def overlay(name, relative):
    parent = importlib.import_module(name.rsplit(".", 1)[0])
    spec = importlib.util.spec_from_file_location(name, SOURCE / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    setattr(parent, name.rsplit(".", 1)[1], module)
    return module


F = overlay("discovery.formal_features", "conjunction_index/discovery/formal_features.py")
A = overlay("discovery.authenticated_index", "conjunction_index/discovery/authenticated_index.py")
S = overlay("discovery.discovery_store", "conjunction_index/discovery/discovery_store.py")
Legacy = overlay("discovery._legacy_export_adapter", "discovery/module_export_adapter.py")
E = overlay("discovery.module_export_adapter", "conjunction_index/discovery/module_export_adapter.py")
overlay("admission.pin_phase", "runtime_efficient/admission/pin_phase.py")
overlay("admission.trust", "trust_withdrawal/admission/trust.py")
overlay("admission.verifier", "trust_withdrawal/admission/verifier.py")
overlay("aggregate_claims.aggregate_admission", "trust_withdrawal/aggregate_claims/aggregate_admission.py")
overlay("mixed_claims.receiver", "runtime_efficient/mixed_claims/receiver.py")
overlay("mixed_claims.imports_atomic", "interface_views/imports_atomic.py")
overlay("mixed_claims.interface_projection", "interface_views/projection.py")
overlay("mixed_claims.authoring_atomic", "interface_views/authoring_atomic.py")
overlay("transport.semantic_staging", "interface_views/semantic_staging.py")
WA = overlay("client.workspace_atomic", "conjunction_index/client/workspace_atomic.py")
WE = overlay("client.workspace_evidence", "conjunction_index/client/workspace_evidence.py")
overlay("client.workspace_staged", "interface_views/workspace_staged.py")
WV = importlib.import_module("client.workspace_validated")
D = overlay("client.direct_contacts", "conjunction_index/client/direct_contacts.py")
from aggregate_claims import bindings as B
from discovery import discovery_query as Q, candidate_query as CQ
from evidence_network.custody import public_profile
from modules import codec as C

OUTPUT = None
OBSERVED = {}
INDEX_LIMITS = dict(max_objects=64, max_postings=2048, max_features=1024,
    max_snapshots=65, max_logical_bytes=33554432, max_db_pages=16384)
CANDIDATE_LIMITS = dict(scanned=64, matches=8, bytes=65536, timeout_ms=1000,
    record_probes=512, node_reads=100000, hash_calls=2000000, sql_vm_steps=1000000)


def digest(value): return hashlib.sha256(value.encode("ascii")).hexdigest()
def name(value): return [["s", value]]
def const(value): return ["const", ["foundation", name(value)], []]
def atom(value):
    return {"tag": "type-symbol", "symbol": {"kind": "foundation-name",
        "name_hash": C.hash_value("foundation-symbol", name(value))}}


def profile(*pairs):
    rows = [sorted([deepcopy(a), deepcopy(b)], key=F.compact) for a, b in pairs]
    return {"schema": E.PAIR_PROFILE_SCHEMA, "pairs": sorted(rows, key=F.compact)}


def adapter(selected=None):
    return E.ModuleExportAdapter(C, B.FOUNDATION, B.POLICY, discovery_profile=selected)


def export_raw(adopted, label, symbols):
    typ = const(symbols[0] if symbols else "Neither")
    for symbol in symbols[1:]: typ = ["app", typ, const(symbol)]
    spec = {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
        "groups": [{"kind": "ordinary", "declarations": [{"name": name(label),
            "kind": "theorem", "universes": 0, "type": typ, "value_hash": None, "meta": {}}]}]}
    module = C.module_id(spec)
    return adopted.encode_opening(module, name(label), C.group_opening(spec, 0))


class SyntheticPostingAdapter:
    """Deterministic stress records only; IDs are not real ExportIDs/proofs."""
    def __init__(self, selected):
        self.actual = adapter(selected)
        self.namespace, self.feature_schema = self.actual.namespace, self.actual.feature_schema
        self.pair = selected["pairs"][0]
        self.atomic = {E.feature_id(self.namespace, a) for a in self.pair}
        self.compound = E.pair_feature_id(self.namespace, self.pair)

    def extract(self, raw, expected_id=None):
        value = F.strict(raw, 4096)
        F.fields(value, ("label", "atoms"))
        keys = {E.feature_id(self.namespace, atom(symbol)) for symbol in value["atoms"]}
        # A unique formal type key avoids equal-type deduplication as explanation.
        keys.add(E.feature_id(self.namespace, {"tag": "declared-type-key", "value": digest(value["label"])}))
        if self.atomic <= keys: keys.add(self.compound)
        identifier = "07"+digest(value["label"])[2:]
        if expected_id is not None: F.need(expected_id == identifier, "SYNTHETIC_ID")
        return {"schema": F.RECORD_SCHEMA, "namespace": self.namespace,
            "kind": "structural-synthetic-pair-control", "object_id": identifier,
            "object_sha256": hashlib.sha256(raw).hexdigest(), "object_bytes": len(raw),
            "features": sorted(keys)}


class StopAfterCompile(ValueError): pass


class PairControls(unittest.TestCase):
    def setUp(self): self.serial = 0

    def fresh(self, label):
        self.serial += 1
        return OUTPUT/(self._testMethodName+"-"+str(self.serial)+"-"+label)

    def store(self, adopted, **limits):
        value = S.Store(self.fresh("store"), adopted, {**INDEX_LIMITS, **limits}, create=True)
        self.addCleanup(value.close)
        return value

    def query(self, store, sid, features):
        summary = Q.verify_summary(sid, store.namespace, features, store.summary(sid, features))
        hits, scanned = [], 0
        for plan in Q.plan_partitions(summary):
            if not plan["anchor_count"]: continue
            req = {"schema": "DMKN_FORMAL_CANDIDATE_REQUEST_V1", "namespace": store.namespace,
                "snapshot_id": sid, "features": features, "partition": plan["partition"],
                "anchor": plan["anchor"], "start": 0, "limits": dict(CANDIDATE_LIMITS)}
            response = CQ.page(store, req)
            checked = CQ.verify_page(summary, req, response)
            self.assertEqual(response["termination"], "anchor_boundary")
            self.assertFalse(checked["verified_scan_coverage"])
            self.assertFalse(checked["mathematical_acceptance"])
            scanned += response["charged"]["scanned"]
            hits.extend(row["object_id"] for row in checked["matches"])
        return sorted(hits), scanned

    def test_legacy_identity_and_record_bytes_unchanged(self):
        old = Legacy.ModuleExportAdapter(C, B.FOUNDATION, B.POLICY)
        new = adapter()
        raw = export_raw(old, "legacy", ["Alpha", "Beta"])
        self.assertEqual(new.namespace, old.namespace)
        self.assertEqual(F.compact(new.describe(raw)), F.compact(old.describe(raw)))
        specs = [atom("Alpha"), atom("Beta")]
        self.assertEqual(new.compile_query(specs), Legacy.compile_query(old.namespace, specs))
        self.assertEqual(new.feature_schema, F.EXPORT_SCHEMA)

    def test_pair_iff_and_first_pair_preserves_overlapping_queries(self):
        selected = profile((atom("Alpha"), atom("Beta")), (atom("Beta"), atom("Gamma")))
        adopted = adapter(selected)
        for bits in range(8):
            symbols = [value for i, value in enumerate(("Alpha", "Beta", "Gamma")) if bits & (1<<i)]
            record = adopted.extract(export_raw(adopted, "subset"+str(bits), symbols))
            for pair in selected["pairs"]:
                atoms = {E.feature_id(adopted.namespace, a) for a in pair}
                self.assertEqual(E.pair_feature_id(adopted.namespace, pair) in record["features"],
                                 atoms <= set(record["features"]))
            for wanted in (("Alpha", "Beta"), ("Alpha", "Beta", "Gamma"), ("Beta", "Gamma"), ("Alpha", "Gamma")):
                specs = [atom(a) for a in wanted]
                atomic = set(E.compile_query(adopted.namespace, specs))
                compiled = adopted.compile_query(specs)
                expected = set(atomic)
                for pair in selected["pairs"]:
                    keys = {E.feature_id(adopted.namespace, a) for a in pair}
                    if keys <= atomic:
                        expected.difference_update(keys)
                        expected.add(E.pair_feature_id(adopted.namespace, pair))
                        break
                self.assertEqual(compiled, sorted(expected))
                self.assertEqual(set(compiled) <= set(record["features"]), atomic <= set(record["features"]))
                self.assertLessEqual(len(compiled), len(atomic))
        OBSERVED["all_eight_atom_subsets_first_pair_equivalent"] = True

    def test_profile_shape_copy_namespace_and_mutation_refusal(self):
        selected = profile((atom("Alpha"), atom("Beta")))
        adopted = adapter(selected)
        namespace = adopted.namespace
        selected["pairs"][0][0] = atom("Changed")
        self.assertEqual(adopted.namespace, namespace)
        self.assertEqual(len(adopted.compile_query([atom("Alpha"), atom("Beta")])), 1)
        self.assertNotEqual(namespace, adapter(profile((atom("Alpha"), atom("Gamma")))).namespace)
        invalid = [
            {"schema": E.PAIR_PROFILE_SCHEMA, "pairs": []},
            {"schema": E.PAIR_PROFILE_SCHEMA, "pairs": [[atom("Alpha"), atom("Alpha")]]},
            {"schema": E.PAIR_PROFILE_SCHEMA, "pairs": [list(reversed(profile((atom("Alpha"), atom("Beta")))["pairs"][0]))]},
            {"schema": E.PAIR_PROFILE_SCHEMA, "pairs": profile((atom("Alpha"), atom("Beta")))["pairs"]*2},
            {"schema": "wrong", "pairs": profile((atom("Alpha"), atom("Beta")))["pairs"]},
            profile(*[(atom("Alpha"), atom("X"+str(i))) for i in range(9)]),
        ]
        for item in invalid:
            with self.assertRaisesRegex(ValueError, "EXPORT_PAIR_"): adapter(item)
        nested = {"tag": "atomic-pair", "atoms": [atom("Alpha"), atom("Beta")]}
        with self.assertRaisesRegex(ValueError, "EXPORT_FEATURE_TAG"):
            adapter(profile((nested, atom("Gamma"))))
        with self.assertRaisesRegex(ValueError, "EXPORT_FEATURE_TAG"):
            adopted.compile_query([nested])
        adopted._profile_raw = b"changed"
        with self.assertRaisesRegex(ValueError, "EXPORT_PAIR_PROFILE_CHANGED"):
            adopted.compile_query([atom("Alpha")])

    def test_wrong_profile_and_forged_compound_refuse_at_resolution(self):
        adopted = adapter(profile((atom("Alpha"), atom("Beta"))))
        raw = export_raw(adopted, "one-atom", ["Alpha"])
        record = adopted.extract(raw)
        forged = deepcopy(record)
        forged["features"] = sorted([*record["features"], adopted.compile_query([atom("Alpha"), atom("Beta")])[0]])
        with self.assertRaisesRegex(ValueError, "EXPORT_RECORD_BINDING"):
            adopted.resolve(forged, raw)
        other = adapter(profile((atom("Alpha"), atom("Gamma"))))
        with self.assertRaisesRegex(ValueError, "RECORD_NAMESPACE"):
            other.resolve(record, raw)
        self.assertFalse(adopted.resolve(record, raw)["mathematical_acceptance"])

    def test_feature_record_and_posting_caps_refuse_without_truncation(self):
        old = adapter()
        raw = export_raw(old, "feature-cap", ["Alpha", *["X"+str(i) for i in range(120)]])
        self.assertEqual(len(old.extract(raw)["features"]), 128)
        adopted = adapter(profile((atom("Alpha"), atom("X0"))))
        with self.assertRaisesRegex(ValueError, "EXPORT_FEATURE_PROFILE_EXHAUSTED"):
            adopted.extract(raw)
        huge = old.extract(export_raw(old, "record-cap", ["Alpha"]))
        huge["locator"]["relative_name"] = [["s", "x"*1024] for _ in range(20)]
        with self.assertRaisesRegex(ValueError, "RECORD_BYTES"):
            F.validate_record(huge)
        raw2 = export_raw(adopted, "posting-cap", ["Alpha", "X0"])
        needed = len(adopted.extract(raw2)["features"])
        store = self.store(adopted, max_postings=needed-1)
        before = store.status()
        with self.assertRaisesRegex(ValueError, "POSTING_CAP"): store.admit(raw2)
        self.assertEqual(store.status(), before)
        OBSERVED["cap_refusal_no_rows_silently_dropped"] = True

    def test_real_export_store_roundtrip_and_profile_reopen(self):
        adopted = adapter(profile((atom("Alpha"), atom("Beta"))))
        store = self.store(adopted)
        raw = export_raw(adopted, "structural-export", ["Alpha", "Beta"])
        admitted = store.admit(raw)
        features = adopted.compile_query([atom("Alpha"), atom("Beta")])
        self.assertEqual(self.query(store, admitted["snapshot_id"], features),
                         ([admitted["record"]["object_id"]], 1))
        self.assertEqual(store.snapshot()["feature_schema"], F.EXPORT_PAIR_SCHEMA)
        root = store.root
        store.close()
        reopened = S.Store(root, adapter(profile((atom("Alpha"), atom("Beta")))), INDEX_LIMITS)
        self.addCleanup(reopened.close)
        self.assertEqual(reopened.snapshot()["namespace"], adopted.namespace)
        with self.assertRaisesRegex(ValueError, "STORE_CONFIG"):
            S.Store(root, adapter(profile((atom("Alpha"), atom("Gamma")))), INDEX_LIMITS)

    def test_synthetic_same_corpus_hot_postings_old_cut_and_storage_cost(self):
        selected = profile((atom("Alpha"), atom("Beta")))
        synthetic = SyntheticPostingAdapter(selected)
        store = self.store(synthetic)
        def add(label, atoms): return store.admit(F.compact({"label": label, "atoms": atoms}))
        for i in range(4): add("a"+str(i), ["Alpha"])
        hit = add("both", ["Alpha", "Beta"])
        for i in range(4): add("b"+str(i), ["Beta"])
        sid = store.snapshot()
        snapshot_id = A.snapshot_id(sid)
        original_status = store.status()
        atomic = E.compile_query(synthetic.namespace, [atom("Alpha"), atom("Beta")])
        contracted = synthetic.actual.compile_query([atom("Alpha"), atom("Beta")])
        before_atomic = self.query(store, snapshot_id, atomic)
        before_pair = self.query(store, snapshot_id, contracted)
        self.assertEqual(before_atomic, ([hit["record"]["object_id"]], 5))
        self.assertEqual(before_pair, ([hit["record"]["object_id"]], 1))
        self.assertEqual(original_status["objects"], 9)
        self.assertEqual(original_status["postings"], 20)  #19 atomic/type +1 pair
        for i in range(3):
            add("later-a"+str(i), ["Alpha"])
            add("later-b"+str(i), ["Beta"])
        current_id = A.snapshot_id(store.snapshot())
        self.assertEqual(self.query(store, current_id, atomic), ([hit["record"]["object_id"]], 8))
        self.assertEqual(self.query(store, current_id, contracted), before_pair)
        late = add("late-both", ["Alpha", "Beta"])
        self.assertEqual(self.query(store, snapshot_id, atomic), before_atomic)
        self.assertEqual(self.query(store, snapshot_id, contracted), before_pair)
        last_id = A.snapshot_id(store.snapshot())
        expected_ids = sorted([hit["record"]["object_id"], late["record"]["object_id"]])
        self.assertEqual(self.query(store, last_id, contracted), (expected_ids, 2))
        final_status = store.status()
        self.assertEqual(final_status["objects"], 16)
        self.assertEqual(final_status["postings"], 36)  #34 atomic/type +2 pair
        OBSERVED["hot_postings"] = {"scope": "STRUCTURALLY_SYNTHETIC_NOT_MATHEMATICS",
            "initial_same_corpus": 9, "initial_atomic_scan": 5, "initial_pair_scan": 1,
            "unrelated_growth_corpus": 15, "grown_atomic_scan": 8, "grown_pair_scan": 1,
            "final_corpus": 16, "same_ids": expected_ids, "rejected_records": 0,
            "initial_postings": original_status["postings"], "final_postings": final_status["postings"],
            "initial_logical_bytes": original_status["logical"], "final_logical_bytes": final_status["logical"],
            "additional_pair_postings": 2, "old_cut_unchanged": True}

    def workspace_config(self):
        return {"schema": WE.CONJUNCTION_SCHEMA, "discovery_profile": profile((atom("Alpha"), atom("Beta"))),
            "wire_profile": public_profile("99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60"),
            "module_limits": dict(modules=32, groups=128, declarations=512, bodies=256,
                logical_bytes=33554432, db_pages=16384),
            "packet_limits": dict(packets=4, packet_bytes=16777216, offers=8, offers_per_module=2,
                logical_bytes=67108864, db_pages=32768),
            "index_limits": dict(INDEX_LIMITS), "packet_envelope": {}, "terminal_receipt_bytes": 8388608,
            "max_operations": 2, "max_report_bytes": 1048576, "ledger_pages": 1024}

    def test_ordinary_workspace_persists_profile_and_legacy_stays_separate(self):
        config = self.workspace_config()
        root = self.fresh("workspace")
        workspace = WV.Workspace.open(root, config, create=True)
        self.addCleanup(workspace.close)
        namespace = workspace.adapter.namespace
        self.assertEqual(workspace.adapter.compile_query([atom("Alpha"), atom("Beta")]),
                         adapter(config["discovery_profile"]).compile_query([atom("Alpha"), atom("Beta")]))
        self.assertEqual(workspace.status()["schema"], WE.CONJUNCTION_SCHEMA)
        workspace.close()
        reopened = WV.Workspace.open(root, deepcopy(config))
        self.addCleanup(reopened.close)
        self.assertEqual(reopened.adapter.namespace, namespace)
        reopened.close()
        changed = deepcopy(config)
        changed["discovery_profile"] = profile((atom("Alpha"), atom("Gamma")))
        with self.assertRaisesRegex(ValueError, "CLIENT_WORKSPACE_CONFIG"):
            WV.Workspace.open(root, changed)
        malformed = deepcopy(config)
        malformed["discovery_profile"]["pairs"] = []
        fresh = self.fresh("invalid-before-write")
        with self.assertRaisesRegex(ValueError, "EXPORT_PAIR_PROFILE_COUNT"):
            WV.Workspace.open(fresh, malformed, create=True)
        self.assertFalse(fresh.exists())
        legacy = deepcopy(config)
        del legacy["discovery_profile"]
        legacy["schema"] = WE.SCHEMA
        old = WV.Workspace.open(self.fresh("legacy-workspace"), legacy, create=True)
        self.addCleanup(old.close)
        self.assertEqual(old.adapter.namespace, adapter().namespace)
        self.assertEqual(len(old.adapter.compile_query([atom("Alpha"), atom("Beta")])), 2)
        OBSERVED["ordinary_workspace_profile_reopen_and_legacy"] = True

    def test_both_ordinary_query_callers_forward_to_adopted_compiler(self):
        adopted = adapter(profile((atom("Alpha"), atom("Beta"))))
        specs, observed = [atom("Alpha"), atom("Beta")], []
        compiler = adopted.compile_query
        def stop(specifications):
            observed.append(compiler(specifications))
            raise StopAfterCompile("INERT_STOP_AFTER_ACTUAL_PROFILE_COMPILER")
        adopted.compile_query = stop
        client = WV.CommonsClient.__new__(WV.CommonsClient)
        client._query_used = False
        client._channel = client._handoff = client._search = client._acquisition = None
        client.workspace = SimpleNamespace(adapter=adopted, root=OUTPUT)
        client.grant = SimpleNamespace(deadline=1, directory=OUTPUT)
        policy = D.OwnerEgressPolicy({"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test",
            "public_ports": [], "test_endpoints": [{"host": "127.0.0.1", "port": 49991}]})
        # Exact-class inert client, real policy and changed function bodies only.
        # Bypass unchanged action wrappers; sentinel forbids downstream sessions/I/O.
        with self.assertRaisesRegex(StopAfterCompile, "INERT_STOP_AFTER_ACTUAL_PROFILE_COMPILER"):
            D.bind.__wrapped__(client, {"inert": {"host": "127.0.0.1", "port": 49991,
                "tls": False, "server_name": None}}, specs, policy, {})
        channel = WA.ServiceLocationProcess.__new__(WA.ServiceLocationProcess)
        channel.deadline, channel.adoption = 1, SimpleNamespace(workspace=OUTPUT.parent)
        channel.evidence, channel.state = OUTPUT/"no-launch-evidence", OUTPUT/"no-launch-state"
        with self.assertRaisesRegex(StopAfterCompile, "INERT_STOP_AFTER_ACTUAL_PROFILE_COMPILER"):
            asyncio.run(WA.CommonsClient.find.__wrapped__(client, channel, specs, policy, {}, {}, routes=[]))
        expected = compiler(specs)
        self.assertEqual(len(expected), 1)
        self.assertEqual(observed, [expected, expected])
        OBSERVED["both_real_query_bodies_use_profile_compiler"] = True


SELECTED = (
    "test_legacy_identity_and_record_bytes_unchanged",
    "test_pair_iff_and_first_pair_preserves_overlapping_queries",
    "test_profile_shape_copy_namespace_and_mutation_refusal",
    "test_wrong_profile_and_forged_compound_refuse_at_resolution",
    "test_feature_record_and_posting_caps_refuse_without_truncation",
    "test_real_export_store_roundtrip_and_profile_reopen",
    "test_synthetic_same_corpus_hot_postings_old_cut_and_storage_cost",
    "test_ordinary_workspace_persists_profile_and_legacy_stays_separate",
    "test_both_ordinary_query_callers_forward_to_adopted_compiler",
)


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output": raise ValueError("OUTPUT_REQUIRED")
    output = Path(sys.argv[2])
    if not output.is_dir() or output.resolve() != output: raise ValueError("CANONICAL_OUTPUT_REQUIRED")
    OUTPUT = output/"pair-fixtures"
    OUTPUT.mkdir()
    suite = unittest.TestSuite(PairControls(name) for name in SELECTED)
    # Real asyncio's Windows loop can create local loopback wakeup sockets; only
    # outbound connect/create_connection is prohibited, not loop construction.
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "create_subprocess_exec", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "create_subprocess_shell", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(socket, "create_connection", side_effect=AssertionError("NETWORK_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "selected": list(SELECTED), "observed": OBSERVED,
        "scope": "STRUCTURAL_PAIR_INDEX_AND_INERT_ORDINARY_CLIENT_WIRING",
        "mathematical_acceptance": False, "proof_calls": 0, "native_calls": 0,
        "network_operations": 0, "timing_speedup_claim": False}
    with (output/"controls-result.json").open("x", encoding="utf-8") as target:
        json.dump(report, target, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

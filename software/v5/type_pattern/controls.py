"""Whole-type variant discovery controls; all example mathematics is unproved.

Real content-addressed structural openings and ordinary SQLite/query/workspace
paths are used. No native checking, authority object, certificate or network.
"""
from copy import deepcopy
import importlib
import importlib.util
import json
from pathlib import Path
import socket
import subprocess
import sys
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


F = overlay("discovery.formal_features", "type_pattern/discovery/formal_features.py")
T = overlay("discovery.type_pattern", "type_pattern/discovery/type_pattern.py")
A = overlay("discovery.authenticated_index", "type_pattern/discovery/authenticated_index.py")
S = overlay("discovery.discovery_store", "type_pattern/discovery/discovery_store.py")
Old = overlay("discovery._conjunction_predecessor", "conjunction_index/discovery/module_export_adapter.py")
E = overlay("discovery.module_export_adapter", "type_pattern/discovery/module_export_adapter.py")
from discovery import discovery_query as Q, candidate_query as CQ
overlay("admission.pin_phase", "runtime_efficient/admission/pin_phase.py")
overlay("admission.trust", "trust_withdrawal/admission/trust.py")
overlay("admission.verifier", "trust_withdrawal/admission/verifier.py")
overlay("aggregate_claims.aggregate_admission", "trust_withdrawal/aggregate_claims/aggregate_admission.py")
overlay("mixed_claims.receiver", "runtime_efficient/mixed_claims/receiver.py")
overlay("mixed_claims.imports_atomic", "interface_views/imports_atomic.py")
overlay("mixed_claims.interface_projection", "interface_views/projection.py")
overlay("mixed_claims.authoring_atomic", "interface_views/authoring_atomic.py")
overlay("transport.semantic_staging", "interface_views/semantic_staging.py")
overlay("client.workspace_atomic", "conjunction_index/client/workspace_atomic.py")
WE = overlay("client.workspace_evidence", "type_pattern/client/workspace_evidence.py")
overlay("client.workspace_staged", "interface_views/workspace_staged.py")
WV = importlib.import_module("client.workspace_validated")
from aggregate_claims import bindings as B
from evidence_network.custody import public_profile
from modules import codec as C

OUTPUT = None
OBSERVED = {}
OWNER, OTHER = "11" * 32, "22" * 32  # Local template labels, never candidate ModuleIDs.
INDEX_LIMITS = dict(max_objects=64, max_postings=2048, max_features=1024,
    max_snapshots=65, max_logical_bytes=33554432, max_db_pages=16384)
CANDIDATE_LIMITS = dict(scanned=64, matches=8, bytes=65536, timeout_ms=1000,
    record_probes=512, node_reads=100000, hash_calls=2000000, sql_vm_steps=1000000)


def name(*parts): return [["s", part] for part in parts]
def local(label): return ["const", ["local", name(label)], []]
def foundation(label): return ["const", ["foundation", name(label)], []]
def app(f, x): return ["app", f, x]
def profile(): return {"schema": E.PATTERN_PROFILE_SCHEMA}
def adapter(selected=None): return E.ModuleExportAdapter(C, B.FOUNDATION, B.POLICY, discovery_profile=selected)
def key(expr, owner=OWNER, universes=0): return T.pattern_spec(C, owner, universes, expr)
def atom(label): return {"tag": "type-symbol", "symbol": {"kind": "foundation-name",
    "name_hash": C.hash_value("foundation-symbol", name(label))}}
def pair_profile():
    return {"schema": E.PAIR_PROFILE_SCHEMA,
        "pairs": [sorted([atom("Alpha"), atom("Beta")], key=F.compact)]}


def law(carrier="LocalCarrier", operation="LocalOperation", *, idempotent=False):
    typ, fn, x = local(carrier), local(operation), ["bvar", 0]
    eq = ["const", ["foundation", name("Eq")], [["succ", ["zero"]]]]
    body = app(app(app(eq, typ), app(fn, app(fn, x))), app(fn, x) if idempotent else x)
    return ["forall", "default", typ, body]


def export_raw(adopted, label, typ, universes=0):
    # These are structural symbolic theorem declarations, not accepted proofs.
    spec = {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
        "groups": [{"kind": "ordinary", "declarations": [{"name": name(label),
            "kind": "theorem", "universes": universes, "type": typ, "value_hash": None, "meta": {}}]}]}
    module = C.module_id(spec)
    return adopted.encode_opening(module, name(label), C.group_opening(spec, 0))


class PatternControls(unittest.TestCase):
    def setUp(self): self.serial = 0
    def fresh(self, label):
        self.serial += 1
        return OUTPUT / (self._testMethodName + "-" + str(self.serial) + "-" + label)
    def store(self, adopted, **limits):
        result = S.Store(self.fresh("store"), adopted, {**INDEX_LIMITS, **limits}, create=True)
        self.addCleanup(result.close)
        return result
    def query(self, store, sid, features):
        summary = Q.verify_summary(sid, store.namespace, features, store.summary(sid, features))
        hits, scanned = [], 0
        for plan in Q.plan_partitions(summary):
            if not plan["anchor_count"]: continue
            request = {"schema": "DMKN_FORMAL_CANDIDATE_REQUEST_V1", "namespace": store.namespace,
                "snapshot_id": sid, "features": features, "partition": plan["partition"],
                "anchor": plan["anchor"], "start": 0, "limits": dict(CANDIDATE_LIMITS)}
            response = CQ.page(store, request)
            checked = CQ.verify_page(summary, request, response)
            self.assertEqual(response["termination"], "anchor_boundary")
            self.assertFalse(checked["verified_scan_coverage"])
            self.assertFalse(checked["mathematical_acceptance"])
            scanned += response["charged"]["scanned"]
            hits.extend(row["object_id"] for row in checked["matches"])
        return sorted(hits), scanned

    def test_cross_owner_renaming_and_local_external_alias(self):
        self.assertEqual(key(law()), key(law("RemoteCarrier", "RemoteOperation"), OTHER))
        original = app(local("x"), local("x"))
        alias = app(local("x"), ["const", ["external", OWNER, name("x")], []])
        distinct = app(local("x"), ["const", ["external", OTHER, name("x")], []])
        self.assertEqual(key(original), key(alias))
        self.assertNotEqual(key(original), key(distinct))
        self.assertEqual(key(distinct), key(app(local("a"), local("b"))))
        OBSERVED["unknown_owner_invariance_and_exact_alias_coalescing"] = True

    def test_repeated_symbols_and_const_projection_share_one_table(self):
        self.assertNotEqual(key(app(local("f"), local("f"))), key(app(local("f"), local("g"))))
        shared = ["proj", ["local", name("Structure")], 0, local("Structure")]
        unshared = ["proj", ["local", name("Structure")], 0, local("Value")]
        alias = ["proj", ["external", OWNER, name("Structure")], 0, local("Structure")]
        self.assertEqual(key(shared), key(alias))
        self.assertNotEqual(key(shared), key(unshared))
        self.assertNotEqual(key(shared), key(["proj", ["local", name("Structure")], 1, local("Structure")]))

    def test_tree_binder_bound_variable_universe_and_foundation_retained(self):
        self.assertNotEqual(key(law()), key(law(idempotent=True)))
        changed = law(); changed[1] = "implicit"
        self.assertNotEqual(key(law()), key(changed))
        left = ["forall", "default", local("T"), ["forall", "default", local("T"), ["bvar", 0]]]
        right = deepcopy(left); right[3][3] = ["bvar", 1]
        self.assertNotEqual(key(left), key(right))
        self.assertNotEqual(key(local("a")), key(local("a"), universes=1))
        self.assertNotEqual(key(["sort", ["param", 0]], universes=2),
                            key(["sort", ["param", 1]], universes=2))
        self.assertNotEqual(key(["sort", ["max", ["param", 0], ["param", 1]]], universes=2),
                            key(["sort", ["max", ["param", 1], ["param", 0]]], universes=2))
        self.assertNotEqual(key(foundation("Eq")), key(foundation("OtherEq")))
        self.assertNotEqual(key(foundation("Eq")), key(local("Eq")))
        OBSERVED["whole_tree_position_and_fixed_foundation_distinctions"] = True

    def test_preflight_bounds_before_whole_serialization(self):
        cycle = ["app", local("f")]; cycle.append(cycle)
        shared = local("x" * 1024)
        for _ in range(20): shared = ["app", shared, shared]
        short_shared = local("x")
        for _ in range(20): short_shared = ["app", short_shared, short_shared]
        malformed = [cycle, shared, ["bvar", False], ["bvar", 0],
            ["bvar", 2**32], ["const", ["local", name("x" * 1025)], []],
            ["const", ["local", name("\ud800")], []], ["sort", ["param", 0]],
            ["bad-tag"], ["sort", None], ["app"] * 257]
        for index, expr in enumerate(malformed):
            with self.subTest(index=index):
                with self.assertRaises(ValueError): key(expr)
        with self.assertRaisesRegex(ValueError, "EXPORT_TYPE_PATTERN_PREFLIGHT_WORK"):
            key(short_shared)
        # An exception proves the preflight happens before codec's whole encoding.
        with patch.object(C, "validate_expr", side_effect=AssertionError("SERIALIZED_TOO_EARLY")):
            with self.assertRaises(ValueError): key(cycle)
            with self.assertRaises(ValueError): key(shared)
            with self.assertRaisesRegex(ValueError, "EXPORT_TYPE_PATTERN_PREFLIGHT_WORK"):
                key(short_shared)
        with self.assertRaises(ValueError): key(local("x"), owner="not-an-owner")
        with self.assertRaises(ValueError): key(local("x"), universes=True)
        OBSERVED["cyclic_and_exponentially_shared_inputs_preflight_refuse"] = True

    def test_legacy_none_and_pair_bytes_are_identical(self):
        for selected in (None, pair_profile()):
            with self.subTest(selected=selected):
                old = Old.ModuleExportAdapter(C, B.FOUNDATION, B.POLICY, discovery_profile=selected)
                new = adapter(selected)
                raw = export_raw(old, "legacy", app(foundation("Alpha"), foundation("Beta")))
                self.assertEqual(new.namespace, old.namespace)
                self.assertEqual(new.feature_schema, old.feature_schema)
                self.assertEqual(F.compact(new.describe(raw)), F.compact(old.describe(raw)))
                self.assertEqual(new.compile_query([atom("Alpha"), atom("Beta")]),
                                 old.compile_query([atom("Alpha"), atom("Beta")]))
        OBSERVED["both_existing_profiles_namespace_record_byte_identity"] = True

    def test_profile_guards_and_forged_pattern_record(self):
        template = key(law())
        for selected in (None, pair_profile()):
            with self.assertRaises(ValueError): adapter(selected).compile_query([template])
        bad_pair = {"schema": E.PAIR_PROFILE_SCHEMA,
            "pairs": [sorted([template, atom("Eq")], key=F.compact)]}
        with self.assertRaises(ValueError): adapter(bad_pair)
        for value in ({"schema": E.PATTERN_PROFILE_SCHEMA, "extra": True}, {"schema": "bad"}):
            with self.assertRaises(ValueError): adapter(value)
        selected = profile(); adopted = adapter(selected); before = adopted.namespace
        selected["schema"] = "mutated"
        self.assertEqual(adopted.namespace, before)
        self.assertNotEqual(before, adapter().namespace)
        self.assertNotEqual(before, adapter(pair_profile()).namespace)
        other_foundation = E.ModuleExportAdapter(C, "33" * 32, B.POLICY, discovery_profile=profile())
        self.assertNotEqual(before, other_foundation.namespace)
        raw = export_raw(adopted, "involution", law("RemoteT", "RemoteF"))
        record = adopted.extract(raw)
        forged = deepcopy(record)
        true_key = adopted.compile_query([template])[0]
        false_key = adopted.compile_query([key(law(idempotent=True))])[0]
        forged["features"] = sorted((set(forged["features"]) - {true_key}) | {false_key})
        with self.assertRaisesRegex(ValueError, "EXPORT_RECORD_BINDING"): adopted.resolve(forged, raw)
        with self.assertRaisesRegex(ValueError, "RECORD_NAMESPACE"): adapter().resolve(record, raw)
        adopted._pattern_enabled = False
        with self.assertRaisesRegex(ValueError, "PROFILE_CHANGED"): adopted.compile_query([template])

    def test_feature_and_posting_caps_refuse_not_truncate(self):
        typ = foundation("Alpha")
        for i in range(120): typ = app(typ, foundation("X" + str(i)))
        raw = export_raw(adapter(), "feature-cap", typ)
        self.assertEqual(len(adapter().extract(raw)["features"]), 128)
        with self.assertRaisesRegex(ValueError, "FEATURE_PROFILE_EXHAUSTED"): adapter(profile()).extract(raw)
        adopted = adapter(profile())
        raw = export_raw(adopted, "posting-cap", law())
        needed = len(adopted.extract(raw)["features"])
        store = self.store(adopted, max_postings=needed - 1)
        before = store.status()
        with self.assertRaisesRegex(ValueError, "POSTING_CAP"): store.admit(raw)
        self.assertEqual(store.status(), before)

    def test_real_unknown_id_discriminator_store_query_resolve(self):
        # Construct query FIRST, using only caller-owned template labels, never
        # any candidate module ID, declaration name, descriptor or type bytes.
        query_spec = key(law("QueryT", "QueryF"))
        adopted = adapter(profile())
        query_features = adopted.compile_query([query_spec])
        first = export_raw(adopted, "UnfamiliarInvolution", law("HiddenT", "HiddenF"))
        second = export_raw(adopted, "UnfamiliarIdempotence", law("HiddenT", "HiddenF", idempotent=True))
        old = Old.ModuleExportAdapter(C, B.FOUNDATION, B.POLICY)
        def independent_specs(raw):
            return sorted([F.compact(s) for s in old.describe(raw)["specs"] if
                s["tag"] in ("type-edge", "declaration-kind", "object-kind") or
                (s["tag"] == "result-head" and s["head"].get("symbol", {}).get("kind") == "foundation-name")])
        self.assertEqual(independent_specs(first), independent_specs(second))
        store = self.store(adopted)
        first_result, second_result = store.admit(first), store.admit(second)
        sid = second_result["snapshot_id"]
        broad = adopted.compile_query([{"tag": "declaration-kind", "value": "theorem"}])
        broad_hits = self.query(store, sid, broad)
        exact_hits = self.query(store, sid, query_features)
        expected = first_result["record"]["object_id"]
        self.assertEqual(exact_hits, ([expected], 1))
        self.assertEqual(broad_hits[1], 2)
        self.assertEqual(len(broad_hits[0]), 2)
        self.assertFalse(adopted.resolve(first_result["record"], first)["mathematical_acceptance"])
        self.assertEqual(store.snapshot()["feature_schema"], F.EXPORT_TYPE_PATTERN_SCHEMA)
        root = store.root; store.close()
        reopened = S.Store(root, adapter(profile()), INDEX_LIMITS)
        self.addCleanup(reopened.close)
        self.assertEqual(self.query(reopened, sid, query_features), exact_hits)
        with self.assertRaisesRegex(ValueError, "STORE_CONFIG"): S.Store(root, adapter(), INDEX_LIMITS)
        OBSERVED["bounded_unknown_id_discriminator"] = {"corpus_objects": 2,
            "broad_scan": 2, "pattern_scan": 1, "matching_content_id": expected,
            "source_types_unproved": True, "global_selectivity_claim": False,
            "query_uses_candidate_identity": False}

    def test_public_workspace_profile_persist_and_pre_mutation_denial(self):
        config = {"schema": WE.TYPE_PATTERN_SCHEMA, "discovery_profile": profile(),
            "wire_profile": public_profile("99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60"),
            "module_limits": dict(modules=32, groups=128, declarations=512, bodies=256,
                logical_bytes=33554432, db_pages=16384),
            "packet_limits": dict(packets=4, packet_bytes=16777216, offers=8, offers_per_module=2,
                logical_bytes=67108864, db_pages=32768),
            "index_limits": dict(INDEX_LIMITS), "packet_envelope": {}, "terminal_receipt_bytes": 8388608,
            "max_operations": 2, "max_report_bytes": 1048576, "ledger_pages": 1024}
        root = self.fresh("workspace")
        workspace = WV.Workspace.open(root, config, create=True)
        self.addCleanup(workspace.close)
        self.assertEqual(workspace.status()["schema"], WE.TYPE_PATTERN_SCHEMA)
        self.assertEqual(workspace.adapter.namespace, adapter(profile()).namespace)
        workspace.close()
        reopened = WV.Workspace.open(root, deepcopy(config))
        self.addCleanup(reopened.close)
        self.assertEqual(reopened.adapter.namespace, adapter(profile()).namespace)
        reopened.close()
        wrong = deepcopy(config); wrong["schema"] = WE.CONJUNCTION_SCHEMA
        with self.assertRaises(ValueError): WV.Workspace.open(root, wrong)
        for changed in ({"schema": "bad"}, pair_profile(), {**profile(), "extra": True}):
            bad = deepcopy(config); bad["discovery_profile"] = changed
            path = self.fresh("must-not-exist")
            with self.assertRaises(ValueError): WV.Workspace.open(path, bad, create=True)
            self.assertFalse(path.exists())
        OBSERVED["ordinary_workspace_persist_reopen_and_pre_mutation_refusal"] = True


SELECTED = ("test_cross_owner_renaming_and_local_external_alias",
    "test_repeated_symbols_and_const_projection_share_one_table",
    "test_tree_binder_bound_variable_universe_and_foundation_retained",
    "test_preflight_bounds_before_whole_serialization",
    "test_legacy_none_and_pair_bytes_are_identical",
    "test_profile_guards_and_forged_pattern_record",
    "test_feature_and_posting_caps_refuse_not_truncate",
    "test_real_unknown_id_discriminator_store_query_resolve",
    "test_public_workspace_profile_persist_and_pre_mutation_denial")


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output": raise ValueError("OUTPUT_REQUIRED")
    output = Path(sys.argv[2])
    if not output.is_dir() or output.resolve() != output: raise ValueError("CANONICAL_OUTPUT_REQUIRED")
    OUTPUT = output / "pattern-fixtures"
    OUTPUT.mkdir()
    suite = unittest.TestSuite(PatternControls(item) for item in SELECTED)
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(socket, "socket", side_effect=AssertionError("NETWORK_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "selected": list(SELECTED), "observed": OBSERVED,
        "scope": "BOUNDED_VARIANT_QUERY_AND_REAL_STRUCTURAL_INDEX_NOT_MATHEMATICS",
        "mathematical_acceptance": False, "proof_calls": 0, "native_calls": 0,
        "network_operations": 0, "global_selectivity_claim": False, "growth_advantage_claim": False}
    with (output / "controls-result.json").open("x", encoding="utf-8") as target:
        json.dump(report, target, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

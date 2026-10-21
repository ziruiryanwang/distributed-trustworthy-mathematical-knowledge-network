"""Eight structural conclusion-filter controls; no proved mathematics or peers."""
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


F = overlay("discovery.formal_features", "instantiation_discovery/discovery/formal_features.py")
T = overlay("discovery.type_pattern", "type_pattern/discovery/type_pattern.py")
K = overlay("discovery.conclusion_fingerprint", "instantiation_discovery/discovery/conclusion_fingerprint.py")
A = overlay("discovery.authenticated_index", "instantiation_discovery/discovery/authenticated_index.py")
S = overlay("discovery.discovery_store", "instantiation_discovery/discovery/discovery_store.py")
Old = overlay("discovery._pattern_predecessor", "type_pattern/discovery/module_export_adapter.py")
E = overlay("discovery.module_export_adapter", "instantiation_discovery/discovery/module_export_adapter.py")
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
overlay("evidence_network.transport", "iterative_queries/evidence_network/transport.py")
overlay("client.workspace_atomic", "conjunction_index/client/workspace_atomic.py")
WE = overlay("client.workspace_evidence", "instantiation_discovery/client/workspace_evidence.py")
overlay("client.workspace_staged", "interface_views/workspace_staged.py")
WV = overlay("client.workspace_validated", "iterative_queries/client/workspace_validated.py")
from aggregate_claims import bindings as B
from evidence_network.custody import public_profile
from modules import codec as C

OUTPUT = None
OBSERVED = {}
OWNER, OTHER = "11" * 32, "22" * 32
INDEX_LIMITS = dict(max_objects=64, max_postings=2048, max_features=1024,
    max_snapshots=65, max_logical_bytes=33554432, max_db_pages=16384)
PAGE_LIMITS = dict(scanned=64, matches=8, bytes=65536, timeout_ms=1000,
    record_probes=512, node_reads=100000, hash_calls=2000000, sql_vm_steps=1000000)


def name(label): return [["s", label]]
def const(label): return ["const", ["foundation", name(label)], []]
def local(label): return ["const", ["local", name(label)], []]
def var(index): return ["bvar", index]
def app(fn, arg): return ["app", fn, arg]
def pi(domain, body): return ["forall", "default", domain, body]
def lam(domain, body): return ["lam", "default", domain, body]
def profile(*paths):
    return {"schema": K.FINGERPRINT_PROFILE_SCHEMA,
            "paths": sorted([list(p) for p in paths], key=F.compact)}
def adapter(selected=None):
    return E.ModuleExportAdapter(C, B.FOUNDATION, B.POLICY, discovery_profile=selected)
def key(expr, selected, owner=OWNER, universes=0):
    return K.conclusion_spec(C, owner, universes, expr, selected)
def queries(expr, selected, *, context=0, owner=OWNER, universes=0):
    return K.goal_queries(C, owner, universes, expr, selected, context_binders=context)
def expected(selected, tokens):
    # Independent tiny-token oracle: never calls the implementation's observer.
    pid = C.hash_value("conclusion-fingerprint-profile-v1", selected)
    return {"tag": "conclusion-fingerprint", "profile_id": pid,
            "value": C.hash_value("conclusion-fingerprint-v1", {"profile_id": pid, "tokens": tokens})}
def symbol(label):
    return {"kind": "foundation-name", "name_hash": C.hash_value("foundation-symbol", name(label))}
def atom(label): return {"tag": "type-symbol", "symbol": symbol(label)}
def pair_profile():
    return {"schema": E.PAIR_PROFILE_SCHEMA,
            "pairs": [sorted([atom("Alpha"), atom("Beta")], key=F.compact)]}
def law(*, idempotent=False):
    x, fn = var(0), const("f")
    return pi(const("T"), app(app(app(const("Eq"), const("T")), app(fn, app(fn, x))),
                             app(fn, x) if idempotent else x))
def export_raw(adopted, label, typ):
    spec = {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
        "groups": [{"kind": "ordinary", "declarations": [{"name": name(label),
            "kind": "theorem", "universes": 0, "type": typ, "value_hash": None, "meta": {}}]}]}
    module = C.module_id(spec)
    return adopted.encode_opening(module, name(label), C.group_opening(spec, 0))


class FingerprintControls(unittest.TestCase):
    def setUp(self): self.serial = 0
    def fresh(self, label):
        self.serial += 1
        return OUTPUT / (self._testMethodName + "-" + str(self.serial) + "-" + label)
    def store(self, adopted):
        store = S.Store(self.fresh("store"), adopted, INDEX_LIMITS, create=True)
        self.addCleanup(store.close)
        return store
    def page(self, store, sid, features):
        summary = Q.verify_summary(sid, store.namespace, features, store.summary(sid, features))
        hits, scanned = [], 0
        for plan in Q.plan_partitions(summary):
            if not plan["anchor_count"]: continue
            request = {"schema": "DMKN_FORMAL_CANDIDATE_REQUEST_V1", "namespace": store.namespace,
                "snapshot_id": sid, "features": features, "partition": plan["partition"],
                "anchor": plan["anchor"], "start": 0, "limits": dict(PAGE_LIMITS)}
            response = CQ.page(store, request)
            checked = CQ.verify_page(summary, request, response)
            self.assertEqual(response["termination"], "anchor_boundary")
            self.assertFalse(checked["verified_scan_coverage"])
            self.assertFalse(checked["mathematical_acceptance"])
            hits.extend(row["object_id"] for row in checked["matches"])
            scanned += response["charged"]["scanned"]
        return sorted(hits), scanned

    def test_profile_bounds_fresh_copy_and_singleton_or(self):
        selected = profile([], ["arg"], ["fn"])
        copied = K.validate_fingerprint_profile(selected)
        copied["paths"][0].append("body")
        self.assertNotEqual(copied, selected)
        before = deepcopy(selected)
        goal = app(const("f"), const("a"))
        result = queries(goal, selected)
        self.assertEqual(len(result), 8)
        self.assertTrue(all(len(row) == 1 and row[0]["tag"] == K.FINGERPRINT_TAG for row in result))
        self.assertEqual([F.compact(row[0]) for row in result], sorted({F.compact(row[0]) for row in result}))
        self.assertEqual(selected, before)
        self.assertEqual(result, K.goal_queries(C, OWNER, 0, goal, selected))
        malformed = [{"schema": K.FINGERPRINT_PROFILE_SCHEMA, "paths": []},
            profile([], ["arg"], ["fn"], ["body"]), profile(["arg"]*13),
            profile(["bad"]), {**profile([]), "extra": 0},
            {"schema": K.FINGERPRINT_PROFILE_SCHEMA, "paths": [[], []]},
            {"schema": K.FINGERPRINT_PROFILE_SCHEMA, "paths": [["fn"], ["arg"]]}]
        for value in malformed:
            with self.subTest(profile=value):
                with self.assertRaises(ValueError): K.validate_fingerprint_profile(value)
        with patch.object(K, "_compact", side_effect=AssertionError("ENCODED_TOO_EARLY")):
            with self.assertRaises(ValueError): K.validate_fingerprint_profile(profile(["arg"]*13))
        OBSERVED["maximum_eight_separately_funded_singleton_queries"] = True

    def test_explicit_raw_substitution_pairs(self):
        # Source and instance are written independently, not by production substitution.
        cases = [
            (const("a"), const("a"), 0, profile([], ["arg"])),  # k=0
            (pi(const("T"), var(0)), app(const("f"), const("a")), 0,
             profile([], ["arg"], ["fn", "arg"])),
            (pi(const("T"), lam(const("T"), app(var(1), var(0)))),
             lam(const("T"), app(const("f"), var(0))), 0,
             profile(["body", "fn"], ["body", "arg"], ["domain"])),
            (pi(const("T"), ["let", const("T"), var(0), app(var(1), var(0))]),
             ["let", const("T"), const("a"), app(const("a"), var(0))], 0,
             profile(["value"], ["body", "fn"], ["body", "arg"])),
            (pi(["sort", ["zero"]], pi(var(0), app(const("P"), var(0)))),
             app(const("P"), const("a")), 0, profile(["arg"], ["fn"])),
            (pi(const("T"), lam(const("T"), app(var(1), var(0)))),
             pi(const("T"), lam(const("T"), app(var(1), var(0)))), 1,
             profile(["body", "fn"], ["body", "arg"], ["domain"])),
        ]
        for source, goal, context, selected in cases:
            with self.subTest(source=source, context=context):
                self.assertIn([key(source, selected)], queries(goal, selected, context=context))
        OBSERVED["independently_constructed_raw_substitution_pairs"] = len(cases)

    def test_context_scope_exact_strip_and_rigid_absence(self):
        root = profile([])
        wrapper = pi(const("T"), var(0))
        self.assertEqual(queries(wrapper, root, context=1), [[expected(root, [["star"]])]])
        self.assertIn([expected(root, [["node", "forall"]])], queries(wrapper, root))
        # One binder belongs to Gamma; the next still belongs to the goal.
        nested = pi(const("T"), pi(const("T"), app(var(1), var(0))))
        selected = profile(["body", "arg"], ["body", "fn"])
        self.assertEqual(set(F.compact(row[0]) for row in queries(nested, selected, context=1)),
            {F.compact(expected(selected, [["local", 0], ["star"]])),
             F.compact(expected(selected, [["star"], ["star"]]))})
        below = profile(["arg"])
        self.assertIn([expected(below, [["absent"]])], queries(wrapper, below, context=1))
        self.assertIn([key(const("rigid"), below)], queries(wrapper, below, context=1))
        # Dependent context A:Sort, a:A; lambda body refers to Gamma's a.
        dependent = pi(["sort", ["zero"]], pi(var(0), lam(var(1), var(1))))
        self.assertEqual(queries(dependent, profile(["body"]), context=2),
                         [[expected(profile(["body"]), [["star"]])]])
        self.assertEqual(key(pi(const("T"), lam(const("T"), var(0))), profile(["body"])),
                         expected(profile(["body"]), [["local", 0]]))
        OBSERVED["full_dependent_context_and_internal_binder_distinction"] = True

    def test_rigid_symbols_universe_omission_and_no_reduction(self):
        root = profile([])
        external = ["const", ["external", OWNER, name("x")], []]
        self.assertEqual(key(local("x"), root), key(external, root, owner=OTHER))
        self.assertNotEqual(key(local("x"), root), key(local("x"), root, owner=OTHER))
        self.assertNotEqual(key(const("x"), root), key(local("x"), root))
        instantiated = ["const", ["foundation", name("x")], [["param", 0]]]
        self.assertEqual(key(const("x"), root), key(instantiated, root, universes=1))
        self.assertEqual(key(["sort", ["zero"]], root), key(["sort", ["param", 0]], root, universes=1))
        # beta-equivalent syntax is deliberately not normalized.
        beta = app(lam(const("T"), var(0)), const("a"))
        self.assertNotIn([key(beta, root)], queries(const("a"), root))
        below = profile(["arg", "body"])
        self.assertEqual(key(pi(const("T"), var(0)), below), expected(below, [["star"]]))
        self.assertEqual(key(const("a"), below), expected(below, [["absent"]]))

    def test_preflight_and_invalid_context_refusal(self):
        selected = profile([])
        cycle = ["app", const("f")]; cycle.append(cycle)
        for expr in (cycle, const("x"*1025), ["bvar", False], ["app"]*257):
            with patch.object(C, "validate_expr", side_effect=AssertionError("ENCODED_TOO_EARLY")):
                with self.assertRaises(ValueError): key(expr, selected)
                with self.assertRaises(ValueError): queries(expr, selected)
        for n in (True, -1, C.DEFAULT_LIMITS.max_depth+1):
            with patch.object(C, "validate_expr", side_effect=AssertionError("ENCODED_TOO_EARLY")):
                with self.assertRaises(ValueError): queries(const("a"), selected, context=n)
        for expr, n in ((var(0), 0), (const("a"), 1),
                        (pi(var(0), const("a")), 1),
                        (pi(const("T"), var(1)), 1),
                        (pi(const("T"), var(0)), 2)):
            with self.subTest(expr=expr, context=n):
                with self.assertRaises(ValueError): queries(expr, selected, context=n)
        with self.assertRaises(ValueError): key(const("a"), selected, owner="bad")
        with self.assertRaises(ValueError): key(const("a"), selected, universes=True)

    def test_adapter_isolation_legacy_bytes_caps_and_work(self):
        selected = profile(["arg"]); adopted = adapter(selected)
        spec = key(law(), selected)
        for old_profile in (None, pair_profile(), {"schema": T.PATTERN_PROFILE_SCHEMA}):
            previous = Old.ModuleExportAdapter(C, B.FOUNDATION, B.POLICY, discovery_profile=old_profile)
            new = adapter(old_profile)
            raw = export_raw(previous, "Legacy", app(const("Alpha"), const("Beta")))
            self.assertEqual(new.namespace, previous.namespace)
            self.assertEqual(F.compact(new.describe(raw)), F.compact(previous.describe(raw)))
            with self.assertRaises(ValueError): new.compile_query([spec])
        with self.assertRaises(ValueError): adopted.compile_query([T.pattern_spec(C, OWNER, 0, law())])
        with self.assertRaises(ValueError): adopted.compile_query([{**spec, "profile_id": "aa"*32}])
        with self.assertRaises(ValueError): adapter({"schema": E.PAIR_PROFILE_SCHEMA,
            "pairs": [sorted([spec, atom("Eq")], key=F.compact)]})
        original_namespace = adopted.namespace
        selected["paths"][0].append("body")
        self.assertEqual(adopted.namespace, original_namespace)
        self.assertNotEqual(adopted.namespace, adapter(selected).namespace)
        raw = export_raw(adopted, "General", law())
        described = adopted.describe(raw)
        fingerprint_specs = [s for s in described["specs"] if s["tag"] == K.FINGERPRINT_TAG]
        self.assertEqual(fingerprint_specs, [key(law(), profile(["arg"]), owner=described["record"]["locator"]["module_id"])])
        old_work = adapter().describe(raw)["work"]
        derived, extra_work = K._derive_conclusion(C, described["record"]["locator"]["module_id"], 0, law(), profile(["arg"]))
        self.assertEqual(described["work"], old_work + extra_work)
        self.assertEqual(derived, fingerprint_specs[0])
        forged = deepcopy(described["record"])
        real_key = adopted.compile_query([spec])[0]
        false_key = adopted.compile_query([key(law(idempotent=True), profile(["arg"]))])[0]
        forged["features"] = sorted((set(forged["features"])-{real_key})|{false_key})
        with self.assertRaisesRegex(ValueError, "EXPORT_RECORD_BINDING"): adopted.resolve(forged, raw)
        typ = const("Alpha")
        for i in range(120): typ = app(typ, const("X"+str(i)))
        cap_raw = export_raw(adapter(), "Cap", typ)
        self.assertEqual(len(adapter().extract(cap_raw)["features"]), 128)
        with self.assertRaisesRegex(ValueError, "FEATURE_PROFILE_EXHAUSTED"):
            adapter(profile(["arg"])).extract(cap_raw)
        adopted._fingerprint_enabled = False
        with self.assertRaisesRegex(ValueError, "PROFILE_CHANGED"): adopted.compile_query([spec])
        OBSERVED["legacy_null_pair_pattern_preserved_and_new_posting_mandatory"] = True

    def test_generated_or_real_index_two_to_one_and_reopen(self):
        selected = profile(["arg"])
        # Construct alternatives before candidate names, descriptors or identities.
        goal = app(app(app(const("Eq"), const("T")), app(const("f"), app(const("f"), const("a")))), const("a"))
        alternatives = queries(goal, selected)
        adopted = adapter(selected)
        compiled = [adopted.compile_query(row) for row in alternatives]
        first = export_raw(adopted, "UnfamiliarGeneralLaw", law())
        second = export_raw(adopted, "UnfamiliarDifferentLaw", law(idempotent=True))
        store = self.store(adopted)
        first_result = store.admit(first); second_result = store.admit(second)
        sid = second_result["snapshot_id"]
        broad = self.page(store, sid, adopted.compile_query([{"tag": "declaration-kind", "value": "theorem"}]))
        results = [self.page(store, sid, features) for features in compiled]
        expected_id = first_result["record"]["object_id"]
        self.assertEqual(sorted({hit for hits, _ in results for hit in hits}), [expected_id])
        self.assertEqual(sum(scanned for _, scanned in results), 1)
        self.assertEqual((len(broad[0]), broad[1]), (2, 2))
        self.assertFalse(adopted.resolve(first_result["record"], first)["mathematical_acceptance"])
        self.assertEqual(store.snapshot()["feature_schema"], F.EXPORT_CONCLUSION_FINGERPRINT_SCHEMA)
        root = store.root; store.close()
        reopened = S.Store(root, adapter(selected), INDEX_LIMITS); self.addCleanup(reopened.close)
        self.assertEqual([self.page(reopened, sid, features) for features in compiled], results)
        with self.assertRaisesRegex(ValueError, "STORE_CONFIG"):
            S.Store(root, adapter(profile([])), INDEX_LIMITS)
        OBSERVED["concrete_discriminator"] = {"objects": 2, "broad_scan": 2,
            "generated_or_scan": 1, "alternatives": len(alternatives),
            "query_uses_candidate_identity": False, "mathematical_acceptance": False}

    def test_public_workspace_persist_and_premutation_refusal(self):
        selected = profile(["arg"])
        config = {"schema": WE.CONCLUSION_FINGERPRINT_SCHEMA, "discovery_profile": selected,
            "wire_profile": public_profile("99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60"),
            "module_limits": dict(modules=32, groups=128, declarations=512, bodies=256,
                logical_bytes=33554432, db_pages=16384),
            "packet_limits": dict(packets=4, packet_bytes=16777216, offers=8, offers_per_module=2,
                logical_bytes=67108864, db_pages=32768),
            "index_limits": dict(INDEX_LIMITS), "packet_envelope": {}, "terminal_receipt_bytes": 8388608,
            "max_operations": 2, "max_report_bytes": 1048576, "ledger_pages": 1024}
        root = self.fresh("workspace")
        workspace = WV.Workspace.open(root, config, create=True); self.addCleanup(workspace.close)
        self.assertEqual(workspace.status()["schema"], WE.CONCLUSION_FINGERPRINT_SCHEMA)
        self.assertEqual(workspace.adapter.namespace, adapter(selected).namespace)
        workspace.close()
        reopened = WV.Workspace.open(root, deepcopy(config)); self.addCleanup(reopened.close)
        self.assertEqual(reopened.adapter.namespace, adapter(selected).namespace)
        reopened.close()
        changed = deepcopy(config); changed["discovery_profile"] = profile([])
        with self.assertRaisesRegex(ValueError, "WORKSPACE_CONFIG"): WV.Workspace.open(root, changed)
        bad_configs = []
        for invalid in (pair_profile(), {"schema": T.PATTERN_PROFILE_SCHEMA}, {**selected, "extra": True}):
            bad = deepcopy(config); bad["discovery_profile"] = invalid; bad_configs.append(bad)
        for schema in (WE.SCHEMA, WE.CONJUNCTION_SCHEMA, WE.TYPE_PATTERN_SCHEMA):
            bad = deepcopy(config); bad["schema"] = schema; bad_configs.append(bad)
        for bad in bad_configs:
            path = self.fresh("must-not-exist")
            with self.assertRaises(ValueError): WV.Workspace.open(path, bad, create=True)
            self.assertFalse(path.exists())
        OBSERVED["persisted_profile_namespace_and_precreation_refusal"] = True


SELECTED = ("test_profile_bounds_fresh_copy_and_singleton_or",
    "test_explicit_raw_substitution_pairs", "test_context_scope_exact_strip_and_rigid_absence",
    "test_rigid_symbols_universe_omission_and_no_reduction", "test_preflight_and_invalid_context_refusal",
    "test_adapter_isolation_legacy_bytes_caps_and_work", "test_generated_or_real_index_two_to_one_and_reopen",
    "test_public_workspace_persist_and_premutation_refusal")


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output": raise ValueError("OUTPUT_REQUIRED")
    output = Path(sys.argv[2])
    if not output.is_dir() or output.resolve() != output: raise ValueError("CANONICAL_OUTPUT_REQUIRED")
    OUTPUT = output / "fingerprint-fixtures"; OUTPUT.mkdir()
    suite = unittest.TestSuite(FingerprintControls(item) for item in SELECTED)
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(socket, "socket", side_effect=AssertionError("NETWORK_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "selected": list(SELECTED), "observed": OBSERVED,
        "scope": "STRUCTURAL_RAW_INSTANTIATION_FILTER_AND_REAL_INDEX_NOT_MATHEMATICS",
        "mathematical_acceptance": False, "proof_calls": 0, "native_calls": 0,
        "network_operations": 0, "global_selectivity_claim": False, "growth_advantage_claim": False}
    with (output / "controls-result.json").open("x", encoding="utf-8") as target:
        json.dump(report, target, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

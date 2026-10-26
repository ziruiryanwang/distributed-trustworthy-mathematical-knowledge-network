"""Prospective native-free correlation controls; root alone selects execution.

Actual frozen parsers, adapter, SQLite store and positive-proof verifier are used.
Synthetic type previews are unproved metadata, never mathematical acceptance.
No sockets, native subprocesses, package loader or retained owner state is used.
"""
from __future__ import annotations

import time
START, CPU = time.monotonic(), time.process_time()
import argparse
from contextlib import ExitStack
from copy import deepcopy
from dataclasses import replace
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import sqlite3
import ssl
import subprocess
import sys
from types import ModuleType
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024 ** 2
INSTALL = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
OLD_ADAPTER_PATH = "software/v5/ordinary_formal_query/discovery/ordinary_export_adapter.py"
OLD_ADAPTER_SHA = "3ddbed2156a393b08543a5da88c89b5c5b9c2b4f65689c46fbd7623cec38db0a"
THEORY_PATH = "experiments/v5-local-checks/concept-theory-b-export-01/bundle/units/0be846200d7809eaa68cf06cf23ef362052d4d3f4a5db4892c7f369691393e83.json"
THEORY_SHA = "f47ae493eb89d7c052f62b039d9f929195b9e02f72aa38acaa597e4195774556"
EXPR = "DMKN_LEAN_ORIGINAL_EXPR_V1"
MODULES = {
    "ordinary_evidence": "installation/py/ordinary_evidence.py",
    "ordinary_semantics": "installation/py/ordinary_semantics.py",
    "portable_evidence": "installation/py/portable_evidence.py",
    "ordinary_preview": "authoring/py/ordinary_preview.py",
    "portable_preview": "authoring/py/portable_preview.py",
    "formal_query": "authoring/py/formal_query.py",
    "discovery.formal_features": "support/discovery/formal_features.py",
    "discovery.authenticated_index": "support/discovery/authenticated_index.py",
    "discovery.ordinary_export_adapter": None,
    "discovery._prior_adapter": "@prior",
    "discovery.pair_access": "support/discovery/pair_access.py",
    "discovery.discovery_store": "support/discovery/discovery_store.py",
    "discovery.discovery_query": "support/discovery/discovery_query.py",
    "discovery.candidate_query": "support/discovery/candidate_query.py",
}
KNOWN = {
    "Eq": "80b9689fa00451ea0cb456c6e822415c8ca66d4d0cd6a47c890c84371a59d6d5",
    "List": "630c153b900f07dd0bbc113fb8f1d9147eeddac2cc18476773d66cf79f28d54b",
    "RepairTheory.Repair": "ccf36ceef222dbd19a914c058d9659a273159ee5a72416390fe307879f47a751",
    "RepairTheory.run": "06d5b5d82174b561b6ab58aa138341e53dae8d229430768c54cf756c30c5308f",
}


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 60 and time.process_time()-CPU < 35,
         "CORRELATION_CONTROL_ORIGINAL_ENVELOPE")


def raw(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def name(label):
    return [[0, {"$bytes": list(part.encode("utf-8"))}] for part in label.split(".")]


def identity(label):
    return hashlib.sha256(("UNPROVED-CORRELATION-FIXTURE:"+label).encode()).hexdigest()


def local(path, *, fresh=False):
    need(path.is_absolute() and ".." not in path.parts and path.is_relative_to(ROOT),
         "CORRELATION_CONTROL_LOCAL_PATH")
    checked = path.parent if fresh else path
    for parent in (checked, *checked.parents):
        st = parent.lstat()
        need(not parent.is_symlink() and not getattr(st, "st_file_attributes", 0) & 0x400,
             "CORRELATION_CONTROL_REDIRECT")
    need(checked.resolve(strict=True) == checked, "CORRELATION_CONTROL_CANONICAL_PATH")
    if fresh:
        need(not os.path.lexists(path), "CORRELATION_CONTROL_FRESH_PATH")
    return path


def read(path, digest=None):
    check(); local(path)
    with path.open("rb") as stream:
        value = stream.read(2*MIB+1)
    need(0 < len(value) <= 2*MIB, "CORRELATION_CONTROL_READ_BOUND")
    if digest is not None:
        need(hashlib.sha256(value).hexdigest() == digest, "CORRELATION_CONTROL_INPUT_PIN")
    return value


def save(path, value):
    content = raw(value)
    need(len(content) <= 2*MIB, "CORRELATION_CONTROL_OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(content+b"\n")


def forbidden(*args, **kwargs):
    raise AssertionError("CORRELATION_CONTROL_FORBIDDEN_EXTERNAL_OPERATION")


# Declarative tiny fixture trees, not a key/equality/filter implementation.
def c(label, levels=()): return ("c", label, list(levels))
def v(index): return ("v", index)
def app(fn, *args):
    for arg in args: fn = ("app", fn, arg)
    return fn
def pi(label, domain, body): return ("pi", label, domain, body)


def packet(tree, levels):
    nodes, shared = [], {}
    def emit(term):
        tag = term[0]
        if tag == "shared":
            # An explicit fixture-only backreference, not structural keying.
            # Each selected shared label is used in one binder context.
            if term[1] not in shared:
                shared[term[1]] = emit(term[2])
            return shared[term[1]]
        if tag == "c": node = [2, name(term[1]), term[2]]
        elif tag == "v": node = [0, term[1]]
        elif tag == "sort": node = [1, term[1]]
        elif tag == "app": node = [3, emit(term[1]), emit(term[2])]
        elif tag in ("pi", "lam"):
            node = [5 if tag == "pi" else 4, name(term[1]), 0, emit(term[2]), emit(term[3])]
        else: raise AssertionError("FIXTURE_TERM_TAG")
        nodes.append(node)
        return len(nodes)-1
    root = emit(tree)
    return [EXPR, deepcopy(levels), nodes, root]


def schedule_goal(*, same=False, left=None, right=None):
    # Locally chosen before reading any candidate: forall alpha rs ss x,
    # run rs x = run ss x. No foreign premise vocabulary or target ID.
    left = v(2) if left is None else left
    right = (v(2) if same else v(1)) if right is None else right
    run = c("RepairTheory.run", [0])
    conclusion = app(c("Eq", [1]), v(3), app(run, v(3), left, v(0)),
                     app(run, v(3), right, v(0)))
    seq = lambda depth: app(c("List", [0]), app(c("RepairTheory.Repair", [0]), v(depth)))
    return pi("alpha", ("sort", 1), pi("rs", seq(0), pi("ss", seq(1),
           pi("x", v(2), conclusion))))


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("source-root", "package", "profile-sha256", "adapter-sha256", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "CORRELATION_CONTROL_CONTEXT")
    source_root, package, output = (Path(value) for value in
                                  (args.source_root, args.package, args.output))
    local(source_root); local(package); local(output, fresh=True)
    need(output.is_relative_to(ROOT/"experiments/v5-local-checks"), "CORRELATION_CONTROL_OUTPUT_SCOPE")
    profile_raw = read(package/"PROFILE.json", args.profile_sha256)
    installation_raw = read(package/"installation/INSTALLATION.json", INSTALL)
    profile, installation = json.loads(profile_raw), json.loads(installation_raw)
    need(profile["installation_manifest_sha256"] == INSTALL, "CORRELATION_CONTROL_INSTALL_BINDING")
    selected = {}
    for module, relative in MODULES.items():
        if relative is None:
            path, expected = source_root/"software/v5/ordinary_correlation_search/ordinary_export_adapter.py", args.adapter_sha256
            data = read(path, expected)
            need(read(package/"support/discovery/ordinary_export_adapter.py", args.adapter_sha256) == data,
                 "CORRELATION_CONTROL_ASSEMBLED_ADAPTER")
        elif relative == "@prior":
            path = ROOT/OLD_ADAPTER_PATH
            data = read(path, OLD_ADAPTER_SHA)
        else:
            path = package/relative
            pins = installation["files"][relative.removeprefix("installation/")] if relative.startswith("installation/") else profile["files"][relative]
            data = read(path, pins["sha256"])
            need(len(data) == pins["bytes"], "CORRELATION_CONTROL_INPUT_LENGTH")
        selected[module] = (path, data)
    theory_raw = read(ROOT/THEORY_PATH, THEORY_SHA)
    need(len(theory_raw) == 13776, "CORRELATION_CONTROL_THEORY_LENGTH")
    need(not any(key in sys.modules for key in (*MODULES, "discovery")), "CORRELATION_CONTROL_CLEAN_IMPORT_MAP")
    output.mkdir()
    cases, fixtures, modules = [], {}, {}
    status, failure = "FAIL", None

    def case(label, fn):
        check(); detail = fn()
        cases.append({"case": label, "status": "PASS", "detail": detail})
        need(len(cases) <= 24, "CORRELATION_CONTROL_CASE_CAP")

    def refusal(fn, expected=None):
        try: fn()
        except ValueError as exc:
            need(expected is None or str(exc) == expected, "CORRELATION_CONTROL_WRONG_REFUSAL:"+str(exc))
            return str(exc)
        raise AssertionError("CORRELATION_CONTROL_MISSING_REFUSAL")

    def remember(label, data):
        need(len(data) < 128*1024, "CORRELATION_CONTROL_FIXTURE_BOUND")
        fixtures[label] = {"raw_utf8": data.decode("utf-8"), "sha256": hashlib.sha256(data).hexdigest()}
        need(len(raw(fixtures)) <= MIB, "CORRELATION_CONTROL_FIXTURE_TOTAL")
        return data

    original_connect = sqlite3.connect
    def fresh_connect(database, *positional, **kw):
        path = Path(database)
        need(path.is_absolute() and path.is_relative_to(output/"index"), "CORRELATION_CONTROL_DATABASE_SCOPE")
        return original_connect(database, *positional, **kw)

    try:
        with ExitStack() as stack:
            for target in ("socket.socket", "socket.create_connection", "subprocess.Popen", "os.system", "os.startfile"):
                stack.enter_context(patch(target, forbidden))
            stack.enter_context(patch("sqlite3.connect", fresh_connect))
            pkg = ModuleType("discovery"); pkg.__path__ = []
            sys.modules["discovery"] = pkg
            for module, (path, data) in selected.items():
                spec = importlib.util.spec_from_file_location(module, path)
                value = importlib.util.module_from_spec(spec)
                sys.modules[module] = value
                modules[module] = value
                exec(compile(data, str(path), "exec"), value.__dict__)
                if module.startswith("discovery."): setattr(pkg, module.split(".")[-1], value)
            Q, PP, S = (modules[k] for k in ("formal_query", "portable_preview", "ordinary_semantics"))
            A, Old, F, DS, DQ, CQ = (modules["discovery."+k] for k in
                ("ordinary_export_adapter", "_prior_adapter", "formal_features", "discovery_store", "discovery_query", "candidate_query"))
            semantic = S.semantic_id(); adapter = A.OrdinaryExportAdapter(semantic)
            params, levels = [name("u")], [[4, 0], [1, 0]]

            def query(label, tree, *, up=params, lv=levels, extra=None):
                dag = packet(tree, lv)
                # Fixture name census only; real parser checks its exactness/scope.
                names = {raw(node[1]): node[1] for node in dag[2] if node[0] == 2}
                known = {raw(name(key)): value for key, value in {**KNOWN, **(extra or {})}.items()}
                rows = [[names[key], known.get(key, identity(key.hex()))] for key in sorted(names)]
                native = raw([Q.NATIVE_SCHEMA, up, dag])
                qr = Q.bind_native_type(native, raw(rows), semantic_id=semantic)
                if label == "independent_schedule_goal":
                    # Exact canonical bytes, without save()'s report newline.
                    for filename, data in (("query-native.json", native), ("query-bindings.json", raw(rows))):
                        need(len(data) <= MIB, "PUBLIC_QUERY_FIXTURE_BOUND")
                        with (output/filename).open("xb") as stream: stream.write(data)
                return remember(label, qr)

            def preview(label, qr, *, kind=2):
                doc, _ = Q.read_query(qr)
                return remember(label, raw({"schema": PP.SCHEMA, "semantic_id": semantic,
                    "unit_id": identity(label), "export_name": name(label),
                    "header": [kind, doc["universe_params"], doc["type"]],
                    "type_bindings": doc["type_bindings"]}))

            def values(pr):
                return {spec["value"] for spec in adapter.describe(pr)["specs"] if spec["tag"] == "conclusion-correlation"}

            # Independently constructed local query precedes parsing the retained theorem.
            qr = query("independent_schedule_goal", schedule_goal())
            separate = A.correlation_query_spec(qr, context_binders=4)
            need(separate["value"] == "separate", "INDEPENDENT_GOAL_PARTITION")
            export_name = name("RepairTheory.ClosureBridge.same_constraints_same_run")
            real = remember("retained_theory_preview", PP.preview_from_evidence(theory_raw, export_name))
            real_doc = json.loads(real)
            need(real_doc["header"][2][3] == 60 and real_doc["header"][2][2][48] == [3, 44, 25], "RETAINED_TYPE_GEOMETRY")
            mutated = deepcopy(real_doc)
            mutated["unit_id"], mutated["export_name"] = identity("unproved-reflexive"), name("UnprovedReflexive")
            mutated["header"][2][2][48][2] = 28  # only RHS schedule ss -> rs
            # Original node25 is still reached through premise domains, so this
            # one-edge change preserves the preview's no-orphan DAG contract.
            need(mutated["header"][2][2][26] == [3, 21, 25] and
                 mutated["header"][2][2][33] == [3, 32, 25], "DECOY_PARAMETER_STILL_REACHABLE")
            reflexive = remember("mechanical_unproved_reflexive_preview", raw(mutated))

            def source_discriminator():
                real_info, decoy_info = adapter.describe(real), adapter.describe(reflexive)
                def atomic(info): return sorted(raw(s) for s in info["specs"] if s["tag"] not in ("conclusion-correlation", "declared-type-key"))
                need(atomic(real_info) == atomic(decoy_info), "SAME_NONEXACT_FEATURES")
                need(values(real) == {"equal", "separate"} and values(reflexive) == {"equal"}, "SOURCE_CORRELATION_DISCRIMINATOR")
                need(Q.query_spec(qr) not in real_info["specs"], "WHOLE_TYPE_SHORTCUT_NOT_AVAILABLE")
                key = A.compile_query(adapter.namespace, [separate])[0]
                need(key in real_info["record"]["features"] and key not in decoy_info["record"]["features"], "ONE_KEY_DISCRIMINATION")
                need(not real_info["mathematical_acceptance"] and not adapter.resolve(real_info["record"], real)["mathematical_acceptance"], "NOT_MATH")
                return {"target": real_info["record"]["object_id"], "decoy": decoy_info["record"]["object_id"], "query_feature": key}
            case("retained_type_independent_goal_and_same_feature_nonmatch", source_discriminator)

            def duplicate_equal():
                equal_raw = query("duplicate_equal_subterms", schedule_goal(same=True))
                doc, _ = Q.read_query(equal_raw); ns = doc["type"][2]; root = doc["type"][3]
                for _ in range(4): root = ns[root][4]
                left = ns[ns[ns[root][2]][1]][2]
                right = ns[ns[ns[ns[root][1]][2]][1]][2]
                need(left != right and ns[left] == ns[right] == [0, 2], "DUPLICATE_NODE_FIXTURE")
                spec = A.correlation_query_spec(equal_raw, context_binders=4)
                need(spec["value"] == "equal" and spec in adapter.describe(real)["specs"], "DISTINCT_PARAMS_MAY_HAVE_EQUAL_INSTANCES")
                need(A.correlation_query_spec(qr, context_binders=0)["value"] == "separate", "UNSTRIPPED_GOAL_NOT_ALL_FORALLS")
                return {"distinct_equal_node_indices": [left, right], "value": spec["value"]}
            case("equal_substitution_and_duplicate_dag_nodes", duplicate_equal)

            def compound_sharing():
                child = app(c("J"), v(2))
                shared_child = ("shared", "compound-child", child)
                value = query("differently_shared_compound_endpoints", schedule_goal(
                    left=app(c("K"), shared_child, shared_child),
                    right=app(c("K"), child, child)))
                doc, _ = Q.read_query(value); ns = doc["type"][2]; root = doc["type"][3]
                for _ in range(4): root = ns[root][4]
                right = ns[ns[ns[root][2]][1]][2]
                left = ns[ns[ns[ns[root][1]][2]][1]][2]
                left_children = [ns[ns[left][1]][2], ns[left][2]]
                right_children = [ns[ns[right][1]][2], ns[right][2]]
                need(left_children[0] == left_children[1] and
                     right_children[0] != right_children[1], "COMPOUND_SHARING_FIXTURE")
                need(A.correlation_query_spec(value, context_binders=4)["value"] == "equal",
                     "INTERNAL_SHARING_MUST_NOT_CHANGE_KEY")
                return {"shared_child_indices": left_children,
                        "duplicate_child_indices": right_children, "value": "equal"}
            case("equal_compound_endpoints_with_different_internal_sharing", compound_sharing)

            def absent_and_early():
                missing = query("missing_paths", ("sort", 0), up=[], lv=[[0]])
                early_tree = pi("A", ("sort", 1), pi("f", pi("a", v(0), v(1)), pi("x", v(1),
                    app(c("Eq", [1]), v(2), app(v(1), v(0)), app(v(1), v(0)))) ))
                early = query("early_parameters", early_tree)
                for label, value, count in (("missing", missing, 0), ("early", early, 3)):
                    need(A.correlation_query_spec(value, context_binders=count)["value"] == "separate", "MISSING_NOT_EQUAL")
                    need(values(preview(label+"_source", value)) == {"equal", "separate"}, "EARLY_NOT_REQUIRED_EQUALITY")
                return {"missing": "separate", "early": "separate"}
            case("missing_endpoints_and_early_parameter_are_unconstrained", absent_and_early)

            def structural_fields():
                same_label = query("alpha_endpoint_labels", schedule_goal(
                    left=("lam", "left", v(3), v(0)), right=("lam", "right", v(3), v(0))))
                need(A.correlation_query_spec(same_label, context_binders=4)["value"] == "equal", "ALPHA_LABEL_QUOTIENT")
                univ = query("universe_endpoint_difference", schedule_goal(left=c("K", [0]), right=c("K", [2])),
                             up=[name("u"), name("v")], lv=[[4, 0], [1, 0], [4, 1]])
                need(A.correlation_query_spec(univ, context_binders=4)["value"] == "separate", "UNIVERSE_INSTANCE_NOT_ERASED")
                rigids = query("different_rigid_endpoints", schedule_goal(left=c("K"), right=c("J")))
                need(A.correlation_query_spec(rigids, context_binders=4)["value"] == "separate", "RIGID_SYMBOL_NOT_ERASED")
                return {"alpha_labels": "equal", "universe_instances": "separate", "rigid_symbols": "separate"}
            case("exact_quotient_at_complete_endpoint_subterms", structural_fields)

            def strict_inputs():
                outcomes = [refusal(lambda n=n: A.correlation_query_spec(qr, context_binders=n), "ORDINARY_CORRELATION_CONTEXT_COUNT") for n in (True, -1, 1.0, Q.DEFAULT_LIMITS.codec.max_dag_depth+1)]
                outcomes.append(refusal(lambda: A.correlation_query_spec(qr, context_binders=5), "ORDINARY_CORRELATION_CONTEXT_TELESCOPE"))
                bad = json.loads(qr); bad["type"][2][0] = [0, 999]
                outcomes.append(refusal(lambda: A.correlation_query_spec(raw(bad), context_binders=4)))
                # Tiny bound must refuse, never silently classify an incomplete key.
                outcomes.append(refusal(lambda: A.correlation_query_spec(qr, context_binders=4, limits=replace(Q.DEFAULT_LIMITS, max_type_nodes=1))))
                for changed, expected in (({**separate, "profile_id": "0"*64}, "ORDINARY_CORRELATION_PROFILE"),
                    ({**separate, "value": True}, "ORDINARY_CORRELATION_VALUE"),
                    ({**separate, "value": "unknown"}, "ORDINARY_CORRELATION_VALUE"),
                    ({**separate, "extra": 0}, "EXACT_FIELDS")):
                    outcomes.append(refusal(lambda changed=changed: A.validate_spec(changed), expected))
                return outcomes
            case("scope_context_budget_and_exact_spec_refusals", strict_inputs)

            def cap_and_kinds():
                def many(count, kind):
                    tree = c("C000")
                    for i in range(1, count): tree = app(tree, c("C"+str(i).zfill(3)))
                    q = query("cap_query_"+str(count)+"_"+str(kind), tree, up=[], lv=[])
                    return preview("cap_preview_"+str(count)+"_"+str(kind), q, kind=kind)
                full = adapter.describe(many(122, 2))
                need(len(full["record"]["features"]) == 128, "EXACT_128_FEATURE_CAP")
                reason = refusal(lambda: adapter.describe(many(123, 2)), "ORDINARY_FEATURE_PROFILE_EXHAUSTED")
                definition = many(123, 1)
                need(values(definition) == set() and len(adapter.describe(definition)["record"]["features"]) == 127, "THEOREM_ONLY_KEYS")
                return {"full_features": 128, "overflow": reason, "definition_features": 127}
            case("whole_feature_set_fits_or_refuses_and_theorem_only", cap_and_kinds)

            def namespaces_and_resolution():
                old_namespace = Old.namespace_for(semantic)
                need(adapter.namespace != old_namespace, "NEW_NAMESPACE_REQUIRED")
                record = adapter.extract(real)
                changed = deepcopy(record); changed["namespace"] = old_namespace
                old_refusal = refusal(lambda: A.validate_record_locator(changed), "ORDINARY_RECORD_NAMESPACE")
                key = A.compile_query(adapter.namespace, [separate])[0]
                changed = deepcopy(record); changed["features"].remove(key)
                missing = refusal(lambda: adapter.resolve(changed, real), "ORDINARY_PREVIEW_RECORD_BINDING")
                need(Q.query_spec(qr)["tag"] == "declared-type-key" and Q.type_key(qr) == Q.query_spec(qr)["value"], "EXACT_MODE_UNCHANGED")
                return {"old_namespace": old_namespace, "new_namespace": adapter.namespace, "refusals": [old_refusal, missing]}
            case("fresh_namespace_exact_mode_and_complete_record_binding", namespaces_and_resolution)

            def actual_store():
                limits = dict(max_objects=4, max_postings=128, max_features=128, max_snapshots=5,
                              max_logical_bytes=4*MIB, max_db_pages=1024)
                store = DS.Store(output/"index", adapter, limits, create=True)
                try:
                    admitted = [store.admit(value) for value in (reflexive, real)]
                    need(all(not item["mathematical_acceptance"] for item in admitted), "STORE_NOT_MATH")
                    snapshot = admitted[-1]["snapshot_id"]
                    base_specs = [{"tag": "declaration-kind", "value": "theorem"}, {"tag": "type-symbol", "symbol": {"kind": "portable-symbol", "symbol_id": KNOWN["RepairTheory.run"]}}]
                    results = []
                    for specs in (base_specs, [*base_specs, separate]):
                        features = A.compile_query(adapter.namespace, specs)
                        summary = DQ.verify_summary(snapshot, adapter.namespace, features, store.summary(snapshot, features))
                        hits, scanned, pages = [], 0, 0
                        for plan in DQ.plan_partitions(summary):
                            if plan["committed_empty"]: continue
                            need(pages < 2, "TWO_OBJECT_PARTITION_BOUND")
                            request = dict(schema="DMKN_FORMAL_CANDIDATE_REQUEST_V1", namespace=adapter.namespace,
                                snapshot_id=snapshot, features=features, partition=plan["partition"], anchor=plan["anchor"], start=0,
                                limits=dict(scanned=4, matches=4, bytes=262144, timeout_ms=1000,
                                            record_probes=256, node_reads=100000, hash_calls=2000000, sql_vm_steps=1000000))
                            reply = CQ.page(store, request)
                            verified = CQ.verify_page(summary, request, reply, check_budget=check)
                            need(not verified["mathematical_acceptance"] and not verified["global_complete"] and not verified["verified_scan_coverage"], "POSITIVE_PROOFS_NOT_GLOBAL_OR_MATH")
                            hits.extend(item["object_id"] for item in verified["matches"])
                            scanned += reply["charged"]["scanned"]; pages += 1
                        results.append({"hits": sorted(hits), "scanned": scanned, "pages": pages})
                    need(results[0]["hits"] == sorted(item["record"]["object_id"] for item in admitted), "BROAD_HITS")
                    need(results[1]["hits"] == [admitted[1]["record"]["object_id"]], "CORRELATED_HIT_ONLY")
                    need(results[0]["scanned"] == 2 and results[1]["scanned"] == 1, "ACTUAL_METADATA_SCAN_DISCRIMINATOR")
                    return {"broad": results[0], "refined": results[1], "claim": "SYNTACTIC_METADATA_ONLY_NOT_GROWTH"}
                finally: store.close()
            case("actual_store_summary_candidate_and_positive_proofs", actual_store)
            for path, data in selected.values():
                need(read(path) == data, "CORRELATION_CONTROL_SOURCE_CHANGED")
            need(read(ROOT/THEORY_PATH, THEORY_SHA) == theory_raw and read(package/"PROFILE.json", args.profile_sha256) == profile_raw and read(package/"installation/INSTALLATION.json", INSTALL) == installation_raw, "CORRELATION_CONTROL_FINAL_INPUTS")
            status = "PASS"
    except BaseException as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)[:2000]}
        raise
    finally:
        save(output/"FIXTURES.json", fixtures)
        save(output/"RESULT.json", {"status": status, "failure": failure, "groups": cases,
            "wall_seconds": time.monotonic()-START, "own_cpu_seconds": time.process_time()-CPU,
            "source_map": {key: {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()} for key, (path, data) in selected.items()},
            "theory_evidence_sha256": THEORY_SHA, "mathematical_acceptance": False,
            "query_fixture": {"native": "query-native.json", "bindings": "query-bindings.json", "context_count": 4},
            "scope": "NATIVE_FREE_CORRELATION_AND_TEMPORARY_METADATA_INDEX_NOT_FULL_V5"})


if __name__ == "__main__":
    main()

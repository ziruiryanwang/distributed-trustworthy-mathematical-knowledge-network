"""Finite query/preview/adapter metadata controls; never mathematical acceptance.

Synthetic names and SymbolIDs below are unproved search inputs, not a basis,
theorem, checked declaration or evidence. Actual pinned helper modules do every
syntax/key/feature operation. No replacement key engine, Store or native call.
Execution requires a later root selection and an externally supervised process.
"""
from __future__ import annotations

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
import subprocess
import sys
import time
from types import ModuleType
from unittest.mock import patch

START, CPU = time.monotonic(), time.process_time()
ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
PINS = {
    "ordinary_evidence": "fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6",
    "ordinary_semantics": "ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915",
    "ordinary_preview": "0fd9bb516fbb53d9d4264271853904e35810286fc92d5670d15d7a9d3c26b0d6",
    "portable_evidence": "f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8",
    "portable_preview": "b78dd54340b7b55e4359769d6784f7f225ba304457ce880ce2760717e865550d",
    "formal_query": "7901236768784a399f9ae5c56b374d040bce56536b0a47a6ee85093440cabcee",
    "_query_controls_discovery.formal_features":
        "f1f53ee40ce32126085f7f776c47d9d0ab2c5b7c679d40f018f6bff70f6430e5",
    "_query_controls_discovery.ordinary_export_adapter":
        "3ddbed2156a393b08543a5da88c89b5c5b9c2b4f65689c46fbd7623cec38db0a",
}
EXPR = "DMKN_LEAN_ORIGINAL_EXPR_V1"
NATIVE = "DMKN_ORDINARY_LEAN_QUERY_TYPE_AST_V1"


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic() - START < 35 and time.process_time() - CPU < 20,
         "QUERY_CONTROLS_ORIGINAL_ALLOWANCE")


def forbidden(*_, **__):
    raise AssertionError("QUERY_CONTROLS_FORBIDDEN_EXTERNAL_CALL")


def raw(value):
    # Independent fixture encoder, not the product's canonicalization helper.
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def name(label):
    return [[0, {"$bytes": list(label.encode("ascii"))}]]


def identity(label):
    # Explicitly fabricated test metadata, never a warranted SymbolID.
    return hashlib.sha256(("UNPROVED-QUERY-CONTROL:" + label).encode("ascii")).hexdigest()


def packet(levels, expressions):
    return [EXPR, levels, expressions, len(expressions) - 1]


def bindings(*labels):
    return sorted([[name(label), identity(label)] for label in labels], key=lambda row: raw(row[0]))


def source_bytes(path, digest):
    need(path.is_absolute() and ".." not in path.parts and
         path.resolve(strict=True).is_relative_to(ROOT), "QUERY_CONTROLS_LOCAL_SOURCE")
    with path.open("rb") as stream:
        value = stream.read(MIB + 1)
    need(0 < len(value) <= MIB and hashlib.sha256(value).hexdigest() == digest,
         "QUERY_CONTROLS_SOURCE_PIN")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for option in ("helpers", "query", "formal-features", "adapter", "output"):
        parser.add_argument("--" + option, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "QUERY_CONTROLS_CONTEXT")
    output = Path(args.output)
    need(output.is_absolute() and ".." not in output.parts and
         output.resolve().is_relative_to(ROOT / "experiments/v5-local-checks") and
         not os.path.lexists(output) and output.parent.is_dir(), "QUERY_CONTROLS_FRESH_OUTPUT")
    paths = {key: Path(args.helpers) / (key + ".py") for key in list(PINS)[:5]}
    paths.update({"formal_query": Path(args.query),
        "_query_controls_discovery.formal_features": Path(args.formal_features),
        "_query_controls_discovery.ordinary_export_adapter": Path(args.adapter)})
    # Verify the whole exact source closure before executing any product source.
    selected = {key: source_bytes(paths[key], digest) for key, digest in PINS.items()}
    need(not any(key in sys.modules for key in PINS), "QUERY_CONTROLS_CLEAN_MODULES")
    output.mkdir()
    cases, fixtures = [], {}

    def remember(label, value):
        need(label not in fixtures and len(value) <= 65536, "QUERY_CONTROLS_FIXTURE_BOUND")
        fixtures[label] = {"raw_utf8": value.decode("utf-8"),
                           "sha256": hashlib.sha256(value).hexdigest()}
        need(len(raw(fixtures)) <= 256 * 1024, "QUERY_CONTROLS_TOTAL_FIXTURE_BOUND")
        return value

    def positive(label, call):
        check()
        detail = call()
        cases.append({"case": label, "outcome": "PASS", "detail": detail})
        need(len(cases) <= 64, "QUERY_CONTROLS_CASE_BOUND")

    def negative(label, expected, call):
        check()
        try:
            call()
        except ValueError as error:
            need(str(error) == expected, "QUERY_CONTROLS_WRONG_REFUSAL:" + label + ":" + str(error))
        else:
            raise AssertionError("QUERY_CONTROLS_MISSING_REFUSAL:" + label)
        cases.append({"case": label, "outcome": "EXPECTED_REFUSAL", "reason": expected})
        need(len(cases) <= 64, "QUERY_CONTROLS_CASE_BOUND")

    with ExitStack() as stack:
        for target in ("subprocess.Popen", "socket.socket", "socket.create_connection",
                       "sqlite3.connect", "os.system", "os.startfile"):
            stack.enter_context(patch(target, forbidden))
        package = ModuleType("_query_controls_discovery")
        package.__path__ = []
        stack.enter_context(patch.dict(sys.modules, {package.__name__: package}))
        modules = {}
        for key, value in selected.items():
            check()
            spec = importlib.util.spec_from_file_location(key, paths[key])
            module = importlib.util.module_from_spec(spec)
            sys.modules[key] = module  # Dataclass annotations and relative imports need this.
            modules[key] = module
            exec(compile(value, str(paths[key]), "exec"), module.__dict__)
            if key.startswith(package.__name__ + "."):
                setattr(package, key.rsplit(".", 1)[1], module)
        Q, P, PP = (modules[key] for key in ("formal_query", "ordinary_preview", "portable_preview"))
        S = modules["ordinary_semantics"]
        A = modules["_query_controls_discovery.ordinary_export_adapter"]
        F = modules["_query_controls_discovery.formal_features"]
        semantic = S.semantic_id()

        def native(params, expr):
            return raw([NATIVE, params, expr])

        def query(label, params, expr, rows):
            nr = remember(label + ":native", native(params, expr))
            br = remember(label + ":bindings", raw(rows))
            return remember(label + ":query", Q.bind_native_type(nr, br, semantic_id=semantic))

        # Author the query before the candidate preview, with no preview-derived header.
        params = [name("u"), name("v")]
        base = packet([[4, 0], [4, 1]], [
            [2, name("A"), [0]], [2, name("B"), [1]], [2, name("R"), []],
            [0, 1], [0, 0], [3, 2, 3], [3, 5, 4],
            [5, name("y"), 0, 1, 6], [5, name("x"), 0, 0, 7]])
        rows = bindings("A", "B", "R")
        qr = query("base", params, base, rows)
        base_key = Q.type_key(qr)
        positive("independent-reference-name-census", lambda: need(
            Q.reference_names(native(params, base)) == [row[0] for row in rows], "REFERENCE_CENSUS"))

        # Independently written candidate: different traversal and inert labels.
        advertised = {"schema": "DMKN_ORDINARY_LEAN_TYPE_PREVIEW_V2", "semantic_id": semantic,
            "unit_id": identity("unproved-candidate-unit"), "export_name": name("UnprovedCandidate"),
            "header": [2, [name("alpha"), name("beta")], packet([[4, 0], [4, 1]], [
                [0, 0], [2, name("R"), []], [0, 1], [3, 1, 2], [3, 3, 0],
                [2, name("B"), [1]], [5, name("right"), 0, 5, 4],
                [2, name("A"), [0]], [5, name("left"), 0, 7, 6]])],
            "type_bindings": bindings("R", "B", "A")}
        pr = remember("independent-candidate-preview", raw(advertised))

        def agreement():
            found = Q.preview_key(pr)
            need(found == {"key": base_key, "key_node_visits": 11}, "INDEPENDENT_KEY_AGREEMENT")
            need(Q.query_spec(qr) == {"tag": "declared-type-key", "value": base_key}, "QUERY_SPEC")
            need(PP.read_preview(pr).mathematical_acceptance is False, "PREVIEW_NOT_AUTHORITY")
            return found
        positive("independently-authored-query-preview-agreement", agreement)
        adapter = A.OrdinaryExportAdapter(semantic)

        def adapter_agreement():
            described = adapter.describe(pr)
            spec = Q.query_spec(qr)
            feature = A.compile_query(adapter.namespace, [spec])
            need(len(feature) == 1 and feature[0] in described["record"]["features"] and
                 spec in described["specs"], "QUERY_ADAPTER_FEATURE_AGREEMENT")
            expected_namespace = hashlib.sha256(b"DMKN-ORDINARY-DISCOVERY-NAMESPACE-V1\0" + raw({
                "semantic_id": semantic, "preview_schema": "DMKN_ORDINARY_LEAN_TYPE_PREVIEW_V2",
                "evidence_schema": "DMKN_LEAN_ORDINARY_EVIDENCE_V2",
                "unit_format": "DMKN_LEAN_ORDINARY_UNIT_V1", "expression_format": EXPR,
                "normalization": "original-type-dag-no-conversion",
                "feature_schema": "DMKN_ORDINARY_LEAN_EXPORT_FEATURES_V1",
                "feature_revision": "kind-symbol-memoized-spine-head-exact-type-v2",
                "type_key_profile": Q.PROFILE_ID, "partition_bits": 8})).hexdigest()
            need(adapter.namespace == expected_namespace, "NEW_QUERY_NAMESPACE")
            F.validate_record(described["record"], expected_namespace)
            resolved = adapter.resolve(described["record"], pr)
            need(described["mathematical_acceptance"] is False and
                 resolved["mathematical_acceptance"] is False and
                 resolved["next_gate"] == "ACQUIRE_EXACT_PORTABLE_ORDINARY_EVIDENCE",
                 "ADAPTER_NOT_AUTHORITY")
            return {"namespace": expected_namespace, "feature": feature[0],
                    "candidate_authority": "UNPROVED_METADATA_ONLY"}
        positive("actual-adapter-feature-namespace-and-resolution", adapter_agreement)

        def compare(label, p1, e1, b1, p2, e2, b2, equal):
            def run():
                left = Q.type_key(query(label + ":left", p1, e1, b1))
                right = Q.type_key(query(label + ":right", p2, e2, b2))
                need((left == right) is equal, "STRUCTURAL_KEY_RELATION:" + label)
                if not equal:
                    need(A.compile_query(adapter.namespace, [{"tag": "declared-type-key", "value": left}]) !=
                         A.compile_query(adapter.namespace, [{"tag": "declared-type-key", "value": right}]),
                         "STRUCTURAL_FEATURE_NONMATCH:" + label)
                return {"left_key": left, "right_key": right, "expected_equal": equal}
            positive(label, run)

        changed = deepcopy(base)
        changed[2][7][1], changed[2][8][1] = name("renamedY"), name("renamedX")
        compare("forall-binder-alpha", params, base, rows, params, changed, rows, True)
        compare("universe-label-alpha", params, base, rows, [name("v"), name("u")], base, rows, True)
        numbered = packet([[4, 0], [4, 1]], [[0, 0], [2, name("R"), []], [0, 1],
            [3, 1, 2], [3, 3, 0], [2, name("B"), [1]], [5, name("y"), 0, 5, 4],
            [2, name("A"), [0]], [5, name("x"), 0, 7, 6]])
        compare("expression-numbering", params, base, rows, params, numbered, rows, True)
        shared = packet([], [[2, name("R"), []], [2, name("A"), []], [3, 0, 1], [3, 2, 2]])
        expanded = packet([], [[2, name("R"), []], [2, name("A"), []], [3, 0, 1],
            [2, name("R"), []], [2, name("A"), []], [3, 3, 4], [3, 2, 5]])
        compare("expression-sharing", [], shared, bindings("A", "R"),
                [], expanded, bindings("A", "R"), True)
        compare("universe-sharing-numbering", [name("u")],
                packet([[4, 0], [1, 0], [2, 1, 1]], [[1, 2]]), [], [name("u")],
                packet([[4, 0], [1, 0], [4, 0], [1, 2], [2, 1, 3]], [[1, 4]]), [], True)
        lam = packet([], [[2, name("A"), []], [0, 0], [4, name("x"), 0, 0, 1]])
        renamed = deepcopy(lam)
        renamed[2][2][1] = name("renamed")
        compare("lambda-binder-alpha", [], lam, bindings("A"), [], renamed, bindings("A"), True)
        let = packet([], [[2, name("A"), []], [7, {"$bytes": [1]}], [0, 0],
                          [6, name("x"), 0, 1, 2, 0]])
        renamed = deepcopy(let)
        renamed[2][3][1] = name("renamed")
        compare("let-binder-alpha", [], let, bindings("A"), [], renamed, bindings("A"), True)

        for label in ("universe-positions", "binder-annotation", "binder-order"):
            changed = deepcopy(base)
            if label == "universe-positions":
                changed[1] = [[4, 1], [4, 0]]
            elif label == "binder-annotation":
                changed[2][8][2] = 1
            else:
                changed[2][7][3], changed[2][8][3] = 0, 1
            compare(label, params, base, rows, params, changed, rows, False)
        compare("universe-arity", params, base, rows, params + [name("unused")], base, rows, False)
        altered = deepcopy(rows)
        next(row for row in altered if row[0] == name("A"))[1] = identity("different-A")
        compare("exact-SymbolID", params, base, rows, params, base, altered, False)
        compare("universe-instance-order", params, packet([[4, 0], [4, 1]], [[2, name("A"), [0, 1]]]),
                bindings("A"), params, packet([[4, 0], [4, 1]], [[2, name("A"), [1, 0]]]), bindings("A"), False)
        changed = deepcopy(lam)
        changed[2][2][2] = 1
        compare("lambda-annotation", [], lam, bindings("A"), [], changed, bindings("A"), False)
        changed = deepcopy(let)
        changed[2][3][5] = 1
        compare("let-nondependent-flag", [], let, bindings("A"), [], changed, bindings("A"), False)
        proj = packet([], [[2, name("R"), []], [8, name("A"), 0, 0]])
        changed = deepcopy(proj)
        changed[2][1][2] = 1
        compare("projection-field", [], proj, bindings("A", "R"), [], changed, bindings("A", "R"), False)
        altered = bindings("A", "R")
        next(row for row in altered if row[0] == name("A"))[1] = identity("different-structure")
        compare("projection-SymbolID", [], proj, bindings("A", "R"), [], proj, altered, False)
        for tag, label in ((7, "nat-literal"), (9, "string-literal")):
            compare(label, [], packet([], [[tag, {"$bytes": [65]}]]), [],
                    [], packet([], [[tag, {"$bytes": [66]}]]), [], False)

        for label, invalid in (("missing", rows[:-1]), ("extra", sorted(rows + bindings("Z"), key=lambda r: raw(r[0]))),
                               ("duplicate", [rows[0], *rows]), ("order", list(reversed(rows)))):
            br = remember("invalid-bindings:" + label, raw(invalid))
            negative("bind-" + label, "FORMAL_QUERY_BINDING_CENSUS_OR_ORDER",
                     lambda br=br: Q.bind_native_type(native(params, base), br, semantic_id=semantic))
            doc = json.loads(qr)
            doc["type_bindings"] = invalid
            bad_query = remember("invalid-query-bindings:" + label, raw(doc))
            negative("read-query-" + label, "FORMAL_QUERY_BINDING_CENSUS_OR_ORDER",
                     lambda bad_query=bad_query: Q.type_key(bad_query))

        for label, expr, reason in (
                ("open", packet([], [[0, 0]]), "EXPR_OPEN_ROOT"),
                ("orphan-expression", packet([], [[7, {"$bytes": [1]}], [7, {"$bytes": [2]}]]),
                 "PREVIEW_ORPHAN_TYPE_NODE"),
                ("orphan-universe", packet([[0]], [[7, {"$bytes": [1]}]]), "PREVIEW_ORPHAN_TYPE_NODE")):
            nr = remember("invalid-native:" + label, native([], expr))
            negative("native-" + label, reason, lambda nr=nr: Q.read_native_type(nr))
            doc = json.loads(qr)
            doc.update(universe_params=[], type=expr, type_bindings=[])
            bad_query = remember("invalid-query:" + label, raw(doc))
            negative("query-" + label, reason, lambda bad_query=bad_query: Q.type_key(bad_query))
        negative("strict-node-limit", "PREVIEW_TYPE_NODE_BOUND",
                 lambda: Q.type_key(qr, replace(P.DEFAULT_LIMITS, max_type_nodes=10)))
        negative("strict-byte-limit", "JSON_BYTE_BOUND", lambda: Q.read_native_type(native(params, base),
                 replace(P.DEFAULT_LIMITS, codec=replace(P.DEFAULT_LIMITS.codec, max_bytes=32))))
        negative("limit-expansion", "FORMAL_QUERY_LIMITS_NOT_STRICTER",
                 lambda: Q.type_key(qr, replace(P.DEFAULT_LIMITS, max_type_nodes=P.DEFAULT_LIMITS.max_type_nodes + 1)))
        doc = json.loads(qr)
        doc["key_profile"] = identity("wrong-profile")
        bad_profile = remember("invalid-query-profile", raw(doc))
        negative("query-profile-binding", "FORMAL_QUERY_SCHEMA_OR_PROFILE", lambda: Q.type_key(bad_profile))
        bad_preview = deepcopy(advertised)
        bad_preview["type_bindings"] = rows[:-1]
        bad_preview_raw = remember("invalid-preview-bindings", raw(bad_preview))
        negative("preview-binding-census", "PREVIEW_TYPE_BINDING_CENSUS_OR_ORDER",
                 lambda: Q.preview_key(bad_preview_raw))
        negative("adapter-exact-export-binding", "ORDINARY_EXPORT_ID_BINDING",
                 lambda: adapter.describe(pr, identity("wrong-export")))
        need(len(cases) == 42, "QUERY_CONTROLS_EXACT_CASE_COUNT")
        # Recheck actual selected bytes, not only the initially retained dictionary.
        for key, digest in PINS.items():
            source_bytes(paths[key], digest)
    check()
    fixture_raw = raw(fixtures)
    with (output / "FIXTURES.json").open("xb") as stream:
        stream.write(fixture_raw)
    result = {"status": "PASS_SELECTED_FORMAL_QUERY_CONTROLS", "cases": cases,
        "source_pins": {key: {"path": str(paths[key]), "sha256": digest} for key, digest in PINS.items()},
        "fixtures_sha256": hashlib.sha256(fixture_raw).hexdigest(),
        "wall_seconds": time.monotonic() - START, "controller_cpu_seconds": time.process_time() - CPU,
        "scope": "PURE_QUERY_PREVIEW_ADAPTER_METADATA_NOT_NATIVE_OR_MATHEMATICAL_ACCEPTANCE",
        "mathematical_acceptance": False}
    with (output / "REPORT.json").open("xb") as stream:
        stream.write(raw(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

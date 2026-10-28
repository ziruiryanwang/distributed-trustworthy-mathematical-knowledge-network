"""Focused ordinary-DAG pattern controls; execute only by root selection.

Real pinned codecs and fixed inventory, synthetic unproved type advertisements.
No owner, Lean, theorem, database, network, old SDK fixture or product mutation.
An outer finite supervisor remains required; internal allowances cooperate.
"""
from __future__ import annotations

import argparse
from collections import Counter
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
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
START, CPU = time.monotonic(), time.process_time()
MIB = 1024 ** 2
INVENTORY = "c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0"
PINS = {
    "ordinary_evidence": "fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6",
    "ordinary_semantics": "ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915",
    "ordinary_preview": "0fd9bb516fbb53d9d4264271853904e35810286fc92d5670d15d7a9d3c26b0d6",
    "portable_evidence": "f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8",
    "portable_preview": "b78dd54340b7b55e4359769d6784f7f225ba304457ce880ce2760717e865550d",
    "formal_query": "7901236768784a399f9ae5c56b374d040bce56536b0a47a6ee85093440cabcee",
}
EXPR = "DMKN_LEAN_ORIGINAL_EXPR_V1"
NATIVE = "DMKN_ORDINARY_LEAN_QUERY_TYPE_AST_V1"
PREVIEW = "DMKN_ORDINARY_LEAN_TYPE_PREVIEW_V2"


def need(ok, code):
    if not ok:
        raise AssertionError("PATTERN_CONTROL_" + code)


def check():
    need(time.monotonic() - START < 45 and time.process_time() - CPU < 25,
         "ALLOWANCE")


def forbidden(*args, **kwargs):
    raise AssertionError("PATTERN_CONTROL_FORBIDDEN_EXTERNAL_OR_UNPINNED_PARSE")


def raw(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(value):
    return hashlib.sha256(value).hexdigest()


def name(*parts):
    return [[1, part] if type(part) is int else
            [0, {"$bytes": list(part.encode("utf-8"))}] for part in parts]


def symbol(label):
    return sha(("UNPROVED-PATTERN-CONTROL:" + label).encode("utf-8"))


def literal(value):
    return {"$bytes": list(value)}


def refuses(call, expected):
    check()
    try:
        call()
    except ValueError as error:
        need(str(error) == expected, "WRONG_REFUSAL:" + str(error))
        return expected
    raise AssertionError("PATTERN_CONTROL_MISSING_REFUSAL:" + expected)


def controls(T, E, S, P, PP, Q, inventory, candidate_raw):
    anchors = T.prepare_inventory(inventory)
    need(len(anchors.by_name) == 581 and len(anchors.by_symbol) == 581,
         "REAL_FIXED_INVENTORY_CENSUS")
    need(T.PROFILE_ID != Q.PROFILE_ID and T.PATTERN_TAG == "declared-type-pattern",
         "SEPARATE_PATTERN_PROFILE_NOT_RELABELLED_EXACT_KEY")
    cases, inputs = [], {}
    a, b = name("PatternControl", "Alpha"), name("PatternControl", "Beta")
    x, y = name("Unfamiliar", "Action"), name("Unfamiliar", "Carrier")
    sa, sb, sx, sy = [symbol(label) for label in ("a", "b", "x", "y")]
    for n in (a, b, x, y):
        need(raw(n) not in anchors.by_name, "SYNTHETIC_NONBASIS_NAME")
    basis_keys = sorted(anchors.by_name)[:2]
    ba, bb = [json.loads(key) for key in basis_keys]
    bsa, bsb = [anchors.by_name[key] for key in basis_keys]
    need(bsa == S.basis_symbol_id(S.semantic_id(), S.foundation_id(), ba) and
         bsb == S.basis_symbol_id(S.semantic_id(), S.foundation_id(), bb),
         "EXACT_BASIS_IDS")

    def remember(value):
        need(type(value) is bytes and len(value) <= 65536, "SMALL_SYNTHETIC_INPUT")
        inputs.setdefault(sha(value), value.decode("utf-8"))
        need(len(raw(inputs)) <= MIB, "TOTAL_SYNTHETIC_INPUT_BOUND")
        return value

    def make(nodes, *, levels=(), params=(), bindings=(), kind=2,
             semantic=None, export=None):
        packet = [EXPR, list(levels), nodes, len(nodes) - 1]
        native = remember(raw([NATIVE, list(params), packet]))
        # Fixtures supply every name/identity explicitly. Sorting is only the
        # existing preview wire order, never a replacement pattern derivation.
        rows = sorted(deepcopy(list(bindings)), key=lambda row: raw(row[0]))
        preview = remember(raw(dict(schema=PREVIEW,
            semantic_id=S.semantic_id() if semantic is None else semantic,
            unit_id=symbol("unit"), export_name=export or name("PatternControlExport"),
            header=[kind, list(params), packet], type_bindings=rows)))
        return native, preview

    def result(call):
        check()
        value = call()
        need(set(value) == {"key", "spec", "profile_id", "semantic_id", "counters",
                            "work", "mathematical_acceptance"} and
             value["spec"] == {"tag": "declared-type-pattern", "value": value["key"]} and
             value["profile_id"] == T.PROFILE_ID and
             value["semantic_id"] == S.semantic_id() and
             value["mathematical_acceptance"] is False and
             type(value["work"]) is int and value["work"] > 0,
             "RESULT_SCOPE_AND_SPEC")
        E._hex(value["key"])
        return value

    def pair(fixture, selected=anchors):
        n, p = fixture
        left = result(lambda: T.native_pattern(n, selected))
        right = result(lambda: T.preview_pattern(p, selected))
        need(left["key"] == right["key"], "COHERENT_NATIVE_PREVIEW_KEY")
        need(left["counters"]["input_bytes"] == len(n) and
             right["counters"]["input_bytes"] == len(p), "ACTUAL_INPUT_BYTES")
        return left, right

    def group(label, detail):
        cases.append(dict(case=label, outcome="PASS", detail=detail))
        check()

    base = make([[2, a, []], [2, b, []], [3, 0, 1], [3, 2, 0]],
                bindings=((a, sa), (b, sb)))
    first = pair(base, inventory)
    prepared = pair(base)
    for original, cached in zip(first, prepared):
        need(original["key"] == cached["key"] and
             original["counters"]["inventory_bytes_hashed"] == len(inventory) and
             cached["counters"]["inventory_bytes_hashed"] == 0,
             "SAME_RAW_INPUT_SEPARATE_PREPARED_ANCHORS")
    group("raw-native-preview-correspondence-and-separate-prepared-inventory",
          dict(key=first[0]["key"], inventory_bytes=len(inventory)))

    renamed = make([[2, x, []], [2, y, []], [3, 0, 1], [3, 2, 0]],
                   bindings=((x, sx), (y, sy)), kind=1, export=name("OtherExport"))
    repeated = make([[2, a, []], [2, b, []], [3, 0, 1], [3, 2, 1]],
                    bindings=((a, sa), (b, sb)))
    need(pair(renamed)[0]["key"] == first[0]["key"] and
         pair(repeated)[0]["key"] != first[0]["key"], "BIJECTION_NOT_REPETITION_ERASURE")
    alias = make([[2, a, []], [2, b, []], [3, 0, 1], [3, 2, 0]],
                 bindings=((a, sa), (b, sa)))
    same = make([[2, a, []], [3, 0, 0], [3, 1, 0]], bindings=((a, sa),))
    alias_result = result(lambda: T.preview_pattern(alias[1], anchors))
    need(alias_result["key"] == pair(same)[0]["key"] and
         alias_result["key"] != first[0]["key"] and
         alias_result["counters"]["abstract_symbols"] == 1,
         "PREVIEW_ALIAS_BY_PORTABLE_ID")
    group("bijective-vocabulary-renames-repetition-and-portable-aliases",
          dict(renamed_key=first[0]["key"], alias_key=alias_result["key"]))

    anchor_a = make([[2, ba, []]], bindings=((ba, bsa),))
    anchor_b = make([[2, bb, []]], bindings=((bb, bsb),))
    ka, kb = pair(anchor_a)[0], pair(anchor_b)[0]
    need(ka["key"] != kb["key"] and ka["counters"]["anchored_symbols"] == 1 and
         ka["counters"]["abstract_symbols"] == 0, "DISTINCT_BASIS_FIXED")
    forged = make([[2, x, []]], bindings=((x, bsa),))
    refuses(lambda: T.preview_pattern(forged[1], anchors), "PATTERN_BASIS_NAME_MISMATCH")
    counterfeit = make([[2, ba, []]], bindings=((ba, sa),))
    local = make([[2, a, []]], bindings=((a, sa),))
    counterfeit_result = result(lambda: T.preview_pattern(counterfeit[1], anchors))
    need(counterfeit_result["key"] == pair(local)[0]["key"] and
         counterfeit_result["key"] != ka["key"] and
         counterfeit_result["counters"]["anchored_symbols"] == 0,
         "BASIS_SPELLING_ALONE_IS_NOT_PORTABLE_ANCHOR")
    group("exact-basis-preservation-forged-id-refusal-and-counterfeit-spelling",
          dict(basis_names=[ba, bb], basis_ids=[bsa, bsb],
               expected_refusal="PATTERN_BASIS_NAME_MISMATCH"))

    projection = make([[2, a, []], [8, a, 0, 0]], bindings=((a, sa),))
    projection_renamed = make([[2, x, []], [8, x, 0, 0]], bindings=((x, sx),))
    projection_split = make([[2, a, []], [8, b, 0, 0]], bindings=((a, sa), (b, sb)))
    projection_field = make([[2, a, []], [8, a, 1, 0]], bindings=((a, sa),))
    pk = pair(projection)[0]["key"]
    need(pair(projection_renamed)[0]["key"] == pk and
         pair(projection_split)[0]["key"] != pk and
         pair(projection_field)[0]["key"] != pk, "CONST_PROJ_ONE_IDENTITY_MAP_AND_FIELD")
    group("constant-projection-identity-sharing-and-field-preservation", dict(key=pk))

    params = [name("u"), name("v")]
    levels = [[4, 0], [4, 1], [2, 0, 1], [1, 2]]
    binder_nodes = [[2, a, [3]], [0, 0], [4, name("x"), 0, 0, 1],
                    [5, name("y"), 0, 0, 2]]
    binder = make(binder_nodes, levels=levels, params=params, bindings=((a, sa),))
    bk = pair(binder)[0]["key"]
    labeled = deepcopy(binder_nodes)
    labeled[2][1], labeled[3][1] = name("freshBinder"), []
    need(pair(make(labeled, levels=levels, params=[name("i"), name("j")],
                   bindings=((a, sa),)))[0]["key"] == bk, "ERASE_ONLY_BINDER_PARAMETER_LABELS")
    for index, field, value in ((2, 2, 1), (2, 0, 5), (1, 1, 1)):
        changed = deepcopy(binder_nodes)
        changed[index][field] = value
        need(pair(make(changed, levels=levels, params=params,
                       bindings=((a, sa),)))[0]["key"] != bk,
             "BINDER_FLAG_TAG_OR_DEBRUIJN_PRESERVED")
    group("binder-label-erasure-with-flags-tags-and-debruijn-preserved", dict(key=bk))

    changed_levels = deepcopy(levels)
    changed_levels[0][1], changed_levels[1][1] = 1, 0
    need(pair(make(binder_nodes, levels=changed_levels, params=params,
                   bindings=((a, sa),)))[0]["key"] != bk, "PARAMETER_INDEX_PRESERVED")
    changed_levels = deepcopy(levels)
    changed_levels[2][0] = 3
    need(pair(make(binder_nodes, levels=changed_levels, params=params,
                   bindings=((a, sa),)))[0]["key"] != bk, "LEVEL_OPERATOR_PRESERVED")
    need(pair(make(binder_nodes, levels=levels, params=params + [name("unused")],
                   bindings=((a, sa),)))[0]["key"] != bk, "UNIVERSE_ARITY_PRESERVED")
    instances = make([[2, a, [0, 1]]], levels=[[4, 0], [4, 1]],
                     params=params, bindings=((a, sa),))
    reversed_instances = make([[2, a, [1, 0]]], levels=[[4, 0], [4, 1]],
                              params=params, bindings=((a, sa),))
    need(pair(instances)[0]["key"] != pair(reversed_instances)[0]["key"],
         "ORDERED_LEVEL_INSTANCES")
    group("universe-arity-position-operators-and-ordered-instances", dict(key=bk))

    let_nodes = [[2, a, []], [7, literal(b"\x07")], [0, 0],
                 [6, name("value"), 0, 1, 2, 0]]
    lk = pair(make(let_nodes, bindings=((a, sa),)))[0]["key"]
    label_changed = deepcopy(let_nodes)
    label_changed[-1][1] = name("renamedValue")
    need(pair(make(label_changed, bindings=((a, sa),)))[0]["key"] == lk, "LET_LABEL_ERASED")
    for index, value in ((5, 1),):
        changed = deepcopy(let_nodes)
        changed[-1][index] = value
        need(pair(make(changed, bindings=((a, sa),)))[0]["key"] != lk, "LET_NONDEP_PRESERVED")
    natural = pair(make([[7, literal(b"\x07")]]))[0]["key"]
    for node in ([7, literal(b"\x08")], [9, literal(b"7")]):
        need(pair(make([node]))[0]["key"] != natural, "LITERAL_VALUE_AND_KIND")
    need(pair(make([[9, literal("left".encode())]]))[0]["key"] !=
         pair(make([[9, literal("right".encode())]]))[0]["key"], "STRING_VALUE_PRESERVED")
    group("let-flags-and-natural-string-literal-values", dict(let_key=lk, natural_key=natural))

    shared = make([[2, a, []], [2, b, []], [3, 0, 1], [3, 2, 2]],
                  bindings=((a, sa), (b, sb)))
    duplicated = make([[2, a, []], [2, b, []], [3, 0, 1], [2, a, []],
                       [2, b, []], [3, 3, 4], [3, 2, 5]], bindings=((a, sa), (b, sb)))
    reordered = make([[2, b, []], [2, a, []], [3, 1, 0], [3, 2, 2]],
                     bindings=((a, sa), (b, sb)))
    sk = pair(shared)[0]["key"]
    need(pair(duplicated)[0]["key"] == sk and pair(reordered)[0]["key"] == sk,
         "SHARING_AND_TOPOLOGICAL_NUMBERING_INVARIANT")
    shared_level = make([[1, 1], [3, 0, 0]], levels=[[0], [1, 0]])
    duplicate_level = make([[1, 1], [1, 3], [3, 0, 1]],
                           levels=[[0], [1, 0], [0], [1, 2]])
    need(pair(shared_level)[0]["key"] == pair(duplicate_level)[0]["key"],
         "LEVEL_AND_EXPRESSION_SHARING_INVARIANT")
    group("differently-shared-and-numbered-expression-level-dags", dict(key=sk))

    # Observe actual line visits and actual hash calls through public raw APIs.
    # This does not trust the candidate's reported counters alone, replace its
    # algorithm, or construct the exponentially expanded expression tree.
    source_lines = candidate_raw.decode("utf-8").splitlines()
    def line_of(fragment):
        found = [i + 1 for i, line in enumerate(source_lines) if line.strip() == fragment]
        need(len(found) == 1, "TRACE_SOURCE_MARKER")
        return found[0]
    pop_line = line_of("index = todo.pop()")
    visit_line = line_of('counters["preorder_nodes"] += 1')
    measured = []
    for depth in (32, 256):
        vertices = depth + 1
        nodes = [[2, a, []]] + [[3, i - 1, i - 1] for i in range(1, depth + 1)]
        fixture = make(nodes, bindings=((a, sa),))
        for entry, value in ((T.native_pattern, fixture[0]), (T.preview_pattern, fixture[1])):
            observed, hashes = Counter(), Counter()
            original_digest = T._digest
            def digest(domain, value):
                hashes[domain] += 1
                need(sum(hashes.values()) <= vertices + 1, "OBSERVED_HASH_BOUND")
                return original_digest(domain, value)
            def trace(frame, event, arg):
                if frame.f_code is not T._derive.__code__:
                    return None
                if event == "line":
                    if frame.f_lineno == pop_line:
                        observed["pops"] += 1
                    elif frame.f_lineno == visit_line:
                        observed["visits"] += 1
                    need(observed["pops"] <= 2 * depth + 1 and
                         observed["visits"] <= vertices, "OBSERVED_TRAVERSAL_BOUND")
                return trace
            need(sys.gettrace() is None, "NO_PREEXISTING_TRACE")
            try:
                with patch.object(T, "_digest", side_effect=digest):
                    sys.settrace(trace)
                    value_result = result(lambda: entry(value, anchors))
            finally:
                sys.settrace(None)
            need(observed == {"pops": 2 * depth + 1, "visits": vertices} and
                 hashes == {"DMKN-ORDINARY-TYPE-PATTERN-NODE-V1": vertices,
                            "DMKN-ORDINARY-TYPE-PATTERN-KEY-V1": 1},
                 "ACTUAL_LINEAR_VISITS_AND_HASHES")
            c = value_result["counters"]
            need(c["preorder_nodes"] == vertices and c["expression_edges"] == 2 * depth and
                 c["node_hashes"] == vertices and c["symbol_occurrences"] == 1 and
                 c["max_pending_nodes"] <= vertices + 1 and
                 value_result["work"] == 4 * depth + 3,
                 "REPORTED_STRUCTURAL_COUNTS_MATCH_OBSERVATION")
            measured.append(dict(api=entry.__name__, depth=depth, vertices=vertices,
                unfolded_tree_nodes=str(2 ** (depth + 1) - 1),
                actual_visits=observed["visits"], actual_pops=observed["pops"],
                actual_hashes=dict(hashes), result=value_result))
    group("small-exponential-shared-dag-has-measured-linear-traversal", measured)

    refusals = []
    for fixture, reason in (
        ((b"{", b"{"), "JSON_UNTERMINATED"),
        (make([[3, 0, 0]]), "BACKWARD_INDEX"),
        (make([[0, 0]]), "EXPR_OPEN_ROOT"),
        (make([[2, a, []], [2, b, []]], bindings=((a, sa), (b, sb))), "PREVIEW_ORPHAN_TYPE_NODE"),
        (make([[7, literal(b"")]], levels=[[0]]), "PREVIEW_ORPHAN_TYPE_NODE"),
    ):
        for entry, value in ((T.native_pattern, fixture[0]), (T.preview_pattern, fixture[1])):
            refusals.append(dict(api=entry.__name__, reason=refuses(
                lambda: entry(value, anchors), reason)))
    bad = json.loads(base[1])
    bad["type_bindings"] = []
    bad_raw = remember(raw(bad))
    refusals.append(dict(api="preview_pattern", reason=refuses(
        lambda: T.preview_pattern(bad_raw, anchors), "PREVIEW_TYPE_BINDING_CENSUS_OR_ORDER")))
    bad = json.loads(base[1]); bad["semantic_id"] = symbol("unsupported-semantics")
    bad_raw = remember(raw(bad))
    refusals.append(dict(api="preview_pattern", reason=refuses(
        lambda: T.preview_pattern(bad_raw, anchors), "PATTERN_SEMANTICS_NOT_SELECTED")))
    group("public-raw-api-malformed-open-orphan-census-and-semantics-refusals", refusals)

    refusals = []
    for entry, value in ((T.native_pattern, base[0]), (T.preview_pattern, base[1])):
        byte_limits = replace(T.DEFAULT_LIMITS,
            codec=replace(T.DEFAULT_LIMITS.codec, max_bytes=len(value) - 1))
        node_limits = replace(T.DEFAULT_LIMITS, max_type_nodes=1)
        expanded_limits = replace(T.DEFAULT_LIMITS,
                                  max_type_nodes=T.DEFAULT_LIMITS.max_type_nodes + 1)
        for limits, reason in ((byte_limits, "JSON_BYTE_BOUND"),
                               (node_limits, "PREVIEW_TYPE_NODE_BOUND"),
                               (expanded_limits, "FORMAL_QUERY_LIMITS_NOT_STRICTER")):
            refusals.append(dict(api=entry.__name__, reason=refuses(
                lambda: entry(value, anchors, limits), reason)))
    parsed_native, parsed_preview = Q.read_native_type(base[0]), PP.read_preview(base[1])
    refuses(lambda: T.native_pattern(parsed_native, anchors), "JSON_BYTE_BOUND")
    refuses(lambda: T.preview_pattern(parsed_preview, anchors), "JSON_BYTE_BOUND")
    group("narrowed-input-node-caps-no-expanded-limits-and-no-parsed-token-authority", refusals)

    # Invalid bytes must fail the fixed-inventory pin BEFORE any JSON parser.
    with patch.object(T.json, "loads", side_effect=forbidden):
        refuses(lambda: T.prepare_inventory(b"{"), "PATTERN_FIXED_INVENTORY")
        refuses(lambda: T.prepare_inventory(inventory + b"\n"), "PATTERN_FIXED_INVENTORY")
        refuses(lambda: T.prepare_inventory(b"x" * (MIB + 1)), "PATTERN_INVENTORY_BYTES")
        for entry, value in ((T.native_pattern, base[0]), (T.preview_pattern, base[1])):
            refuses(lambda: entry(value, b"{"), "PATTERN_FIXED_INVENTORY")
            refuses(lambda: entry(value, {}), "PATTERN_PREPARED_INVENTORY")
    group("fixed-inventory-pin-before-parser-and-no-peer-prepared-token",
          dict(inventory_sha256=sha(inventory), expected_refusals=7))
    return cases, inputs


def selected_bytes(path, expected, maximum=MIB):
    path = Path(path)
    need(path.is_absolute() and ".." not in path.parts and
         path.resolve(strict=True).is_relative_to(ROOT), "CANONICAL_SELECTED_SOURCE")
    with path.open("rb") as stream:
        value = stream.read(maximum + 1)
    need(0 < len(value) <= maximum and sha(value) == expected, "SELECTED_SOURCE_PIN")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for option in ("helpers", "query", "candidate", "candidate-sha256", "inventory",
                   "self-sha256", "output"):
        parser.add_argument("--" + option, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "ISOLATED_CANONICAL_PYTHON")
    output = Path(args.output)
    need(output.is_absolute() and ".." not in output.parts and output.parent.is_dir() and
         output.resolve().is_relative_to(ROOT / "experiments/v5-local-checks") and
         not os.path.lexists(output), "FRESH_OUTPUT")
    paths = {key: Path(args.helpers) / (key + ".py") for key in list(PINS)[:5]}
    paths.update(formal_query=Path(args.query), _pattern_control_candidate=Path(args.candidate))
    pins = dict(PINS, _pattern_control_candidate=args.candidate_sha256)
    captured = {key: selected_bytes(paths[key], expected) for key, expected in pins.items()}
    inventory = selected_bytes(Path(args.inventory), INVENTORY)
    selected_bytes(Path(__file__), args.self_sha256)
    need(not any(key in sys.modules for key in paths), "CLEAN_SELECTED_MODULES")
    loaded = {}
    with ExitStack() as stack:
        for target in ("subprocess.Popen", "socket.socket", "socket.create_connection",
                       "sqlite3.connect", "os.system", "os.startfile"):
            stack.enter_context(patch(target, forbidden))
        for key, code in captured.items():
            spec = importlib.util.spec_from_file_location(key, paths[key])
            module = importlib.util.module_from_spec(spec)
            sys.modules[key] = module
            exec(compile(code, str(paths[key]), "exec", dont_inherit=True), module.__dict__)
            loaded[key] = module
        output.mkdir()
        cases, inputs = controls(loaded["_pattern_control_candidate"],
            loaded["ordinary_evidence"], loaded["ordinary_semantics"],
            loaded["ordinary_preview"], loaded["portable_preview"], loaded["formal_query"],
            inventory, captured["_pattern_control_candidate"])
    for key, expected in pins.items():
        selected_bytes(paths[key], expected)
    selected_bytes(Path(args.inventory), INVENTORY)
    selected_bytes(Path(__file__), args.self_sha256)
    check()
    inputs_raw = raw(inputs)
    outcome = dict(status="PASS_ORDINARY_DAG_PATTERN_CONTROLS", groups=len(cases), cases=cases,
        source_pins={str(paths[key]): expected for key, expected in pins.items()},
        controls_sha256=args.self_sha256, inventory_sha256=INVENTORY,
        input_fixture_count=len(inputs), inputs_sha256=sha(inputs_raw),
        mathematical_acceptance=False,
        scope="SYNTHETIC_RAW_DAGS_REAL_CODECS_FIXED_INVENTORY_NO_OWNER_OR_LEAN",
        wall_seconds=time.monotonic() - START, cpu_seconds=time.process_time() - CPU)
    with (output / "INPUTS.json").open("xb") as stream:
        stream.write(inputs_raw)
    result_raw = raw(outcome)
    need(len(result_raw) <= MIB, "RESULT_BOUND")
    with (output / "RESULT.json").open("xb") as stream:
        stream.write(result_raw)
    print(result_raw.decode("utf-8"), flush=True)


if __name__ == "__main__":
    main()

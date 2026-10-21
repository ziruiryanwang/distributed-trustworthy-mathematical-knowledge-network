"""Bounded source-lowering contracts; synthetic structure is NOT checked math."""
from copy import deepcopy
from dataclasses import replace
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
sys.path.insert(0, str(SOURCE))
from modules import codec as C, source_rows as Legacy

parent = importlib.import_module("modules")
spec = importlib.util.spec_from_file_location("modules.source_rows", SOURCE / "nat_literals/source_rows.py")
S = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = S
spec.loader.exec_module(S)
parent.source_rows = S

F, P = "11" * 32, "22" * 32
OBSERVED = {}


def name(*parts): return [["s", part] for part in parts]
NAT, ZERO, SUCC, REC, ROOT = (name("Nat"), name("Nat", "zero"),
    name("Nat", "succ"), name("Nat", "rec"), name("sample"))
LOCAL = [NAT, ZERO, SUCC, REC, ROOT]
OFNAT = name("OfNat", "ofNat")


def const(n): return ["const", ["local", deepcopy(n)], []]
def unary(k):
    value = const(ZERO)
    for _ in range(k): value = ["app", const(SUCC), value]
    return value


def fixture(value="2", body=5):
    # Nat's type/constructors are exact. Recursor type/rules are inert structural
    # placeholders, deliberately NOT offered as mathematical correctness evidence.
    return [{"meta": {"synthetic_source_test_only": True}},
        {"in": 1, "str": {"pre": 0, "str": "Nat"}},
        {"in": 2, "str": {"pre": 1, "str": "zero"}},
        {"in": 3, "str": {"pre": 1, "str": "succ"}},
        {"in": 4, "str": {"pre": 1, "str": "rec"}},
        {"in": 5, "str": {"pre": 0, "str": "sample"}},
        {"in": 6, "str": {"pre": 0, "str": "u"}},
        {"in": 7, "str": {"pre": 0, "str": "OfNat"}},
        {"in": 8, "str": {"pre": 7, "str": "ofNat"}},
        {"il": 1, "succ": 0}, {"il": 2, "param": 6},
        {"ie": 0, "sort": 1}, {"ie": 1, "const": {"name": 1, "us": []}},
        {"ie": 2, "const": {"name": 2, "us": []}},
        {"ie": 3, "const": {"name": 3, "us": []}},
        {"ie": 4, "forallE": {"name": 0, "type": 1, "body": 1, "binderInfo": "default"}},
        {"ie": 5, "natVal": value}, {"ie": 6, "const": {"name": 8, "us": []}},
        {"ie": 7, "app": {"fn": 6, "arg": 5}},
        {"ie": 8, "app": {"fn": 5, "arg": 5}},
        {"inductive": {
            "types": [{"name": 1, "levelParams": [], "type": 0, "all": [1], "ctors": [2, 3],
                "numParams": 0, "numIndices": 0, "numNested": 0,
                "isRec": True, "isReflexive": False, "isUnsafe": False}],
            "ctors": [{"name": 2, "levelParams": [], "type": 1, "induct": 1,
                "cidx": 0, "numParams": 0, "numFields": 0, "isUnsafe": False},
                {"name": 3, "levelParams": [], "type": 4, "induct": 1,
                "cidx": 1, "numParams": 0, "numFields": 1, "isUnsafe": False}],
            "recs": [{"name": 4, "levelParams": [6], "type": 0, "all": [1],
                "numParams": 0, "numIndices": 0, "numMotives": 1, "numMinors": 2,
                "k": False, "isUnsafe": False,
                "rules": [{"ctor": 2, "nfields": 0, "rhs": 2},
                          {"ctor": 3, "nfields": 1, "rhs": 3}]}]}},
        {"def": {"name": 5, "levelParams": [], "type": 1, "value": body,
            "hints": {"regular": 1}, "safety": "safe", "all": [5]}}]


def reader(rows=None, **kwargs):
    return S.SourceRows(rows if rows is not None else fixture(), deepcopy(LOCAL), [], **kwargs)


def decode(rows, **kwargs):
    return S.decode_source(rows, deepcopy(LOCAL), [], F, P, **kwargs)


class LiteralControls(unittest.TestCase):
    def test_zero_one_two_exact_constructors_and_decode(self):
        for k in (0, 1, 2):
            with self.subTest(k=k):
                rows = fixture(str(k))
                self.assertEqual(reader(rows).expression(5, ()), unary(k))
                env = decode(rows)
                declaration = env.spec["groups"][-1]["declarations"][0]
                self.assertEqual(declaration["value_hash"], C.body_id(unary(k), 0))
                self.assertIn("NO_MATHEMATICAL_ADMISSION", env.status)
        OBSERVED["exact_0_1_2_and_actual_structural_decode"] = True

    def test_unconverted_forms_and_ofnat_application_preserved(self):
        rows = fixture(body=7)
        expected = ["app", ["const", ["foundation", OFNAT], []], unary(2)]
        source = S.SourceRows(rows, deepcopy(LOCAL), [OFNAT])
        self.assertEqual(source.expression(7, ()), expected)
        env = S.decode_source(rows, deepcopy(LOCAL), [OFNAT], F, P)
        self.assertEqual(env.spec["groups"][-1]["declarations"][0]["value_hash"], C.body_id(expected, 0))
        # No literal is visited when the root body is an existing zero constructor.
        rows = fixture(body=2)
        left = Legacy.decode_source(rows, deepcopy(LOCAL), [], F, P)
        right = decode(rows)
        self.assertEqual(left.spec, right.spec)
        self.assertEqual(left.bodies, right.bodies)
        OBSERVED["nonliteral_identity_and_ofnat_not_rewritten"] = True

    def test_census_only_reader_remains_nonconverting(self):
        rows = fixture()
        rows[-2]["inductive"]["recs"] = []
        census = S.SourceRows(rows, [], [])
        self.assertEqual(census.name(1), NAT)
        self.assertEqual(len(census.declarations), 2)
        with self.assertRaises(C.StructureError): census.expression(5, ())

    def test_literal_spelling_and_unsupported_tags_refuse(self):
        for value in ("", "00", "01", "-1", "+1", "1.0", " 2", "2 ", "2\n", "\u0662", 2, True, None):
            with self.subTest(value=repr(value)):
                with self.assertRaises(C.StructureError): reader(fixture(value)).expression(5, ())
        for tag, value in (("strVal", "2"), ("mysteryLiteral", "2")):
            rows = fixture()
            at = next(i for i, row in enumerate(rows) if row.get("ie") == 5)
            rows[at] = {"ie": 5, tag: value}
            with self.assertRaises(C.StructureError): reader(rows).expression(5, ())
        rows = fixture("9" * 100000)
        with self.assertRaises(C.StructureError): reader(rows).expression(5, ())
        OBSERVED["huge_decimal_is_controlled_refusal"] = True

    def test_exact_nat_role_and_structured_name_required(self):
        for replacement in ("NotNat", "Nat.zero"):
            rows = fixture()
            rows[1]["str"]["str"] = replacement
            with self.assertRaises(C.StructureError): reader(rows).expression(5, ())
        for missing in range(4):
            with self.subTest(missing=missing):
                locals_ = [n for i, n in enumerate(LOCAL) if i != missing]
                with self.assertRaises(C.StructureError):
                    S.SourceRows(fixture(), locals_, [LOCAL[missing]]).expression(5, ())
        external = [{"source_name": NAT, "module": "33" * 32, "relative_name": NAT}]
        with self.assertRaises(C.StructureError):
            S.SourceRows(fixture(), LOCAL[1:], [], external).expression(5, ())
        rows = fixture()
        rows.append(deepcopy(rows[-2]))
        with self.assertRaises(C.StructureError): reader(rows).expression(5, ())

    def test_exact_nat_shape_and_complete_recursor_required(self):
        def mutate(path, value):
            rows = fixture()
            target = rows[-2]["inductive"]
            for part in path[:-1]: target = target[part]
            target[path[-1]] = value
            return rows
        changes = [(("types", 0, "type"), 1), (("types", 0, "levelParams"), [6]),
            (("types", 0, "numParams"), 1), (("types", 0, "numIndices"), 1),
            (("types", 0, "numNested"), 1), (("types", 0, "ctors"), [3, 2]),
            (("types", 0, "numParams"), False), (("types", 0, "isRec"), False),
            (("types", 0, "isReflexive"), True),
            (("ctors", 0, "type"), 4), (("ctors", 1, "type"), 1),
            (("ctors", 1, "numFields"), 0), (("ctors", 1, "cidx"), 0),
            (("ctors", 1, "induct"), 5), (("ctors", 1, "isUnsafe"), True),
            (("recs",), []), (("recs", 0, "name"), 5),
            (("recs", 0, "numMinors"), 1), (("recs", 0, "all"), [5]),
            (("recs", 0, "k"), True),
            (("recs", 0, "rules"), [{"ctor": 2, "nfields": 0, "rhs": 2}]),
            (("recs", 0, "rules", 1, "ctor"), 2),
            (("recs", 0, "rules", 1, "nfields"), 0)]
        for path, value in changes:
            with self.subTest(path=path):
                with self.assertRaises(C.StructureError): reader(mutate(path, value)).expression(5, ())
        rows = fixture()
        rows[-2]["inductive"]["recs"].append(deepcopy(rows[-2]["inductive"]["recs"][0]))
        with self.assertRaises(C.StructureError): reader(rows).expression(5, ())
        OBSERVED["exact_group_and_recursor_census_refusals"] = len(changes) + 1

    def test_lowering_reaches_types_bodies_and_recursor_rules(self):
        rows = fixture()
        rows[-1]["def"]["type"] = 5  # Structural fixture, intentionally not a valid type.
        rows[-2]["inductive"]["recs"][0]["rules"][0]["rhs"] = 5
        env = decode(rows)
        self.assertEqual(env.spec["groups"][-1]["declarations"][0]["type"], unary(2))
        rec = env.spec["groups"][0]["declarations"][-1]
        self.assertEqual(rec["type"], ["sort", ["succ", ["zero"]]])
        self.assertEqual(rec["meta"]["rules"][0]["value_hash"], C.body_id(unary(2), 1))
        self.assertEqual(rec["meta"]["rules"][1]["value_hash"], C.body_id(const(SUCC), 1))
        self.assertIn("NO_MATHEMATICAL_ADMISSION", env.status)
        OBSERVED["homomorphic_paths_and_complete_rule_retention"] = True

    def test_depth_and_work_limits_charge_expanded_occurrences(self):
        # Literal 2 has 8 codec visits and depth3 rooted at0. Tests are local
        # SourceRows expression bounds, not claims about whole-spec validator caps.
        with self.assertRaises(C.StructureError):
            reader(limits=replace(C.DEFAULT_LIMITS, max_depth=2)).expression(5, ())
        with self.assertRaises(C.StructureError):
            reader().expression(5, (), C.DEFAULT_LIMITS.max_depth - 2)
        source = reader()
        before = source.work
        self.assertEqual(source.expression(5, ()), unary(2))
        self.assertGreaterEqual(source.work - before, 8)
        after = source.work
        source.expression(5, ())
        self.assertGreaterEqual(source.work - after, 8)
        source = reader(limits=replace(C.DEFAULT_LIMITS, max_nodes=16))
        with self.assertRaises(C.StructureError): source.expression(8, ())
        OBSERVED["repeated_dag_literals_are_not_free"] = True

    def test_generated_bytes_refuse_with_small_compact_input(self):
        rows = fixture("100")
        input_bytes = len(C.canonical(rows))
        expanded_bytes = len(C.canonical(unary(100)))
        self.assertGreater(expanded_bytes, input_bytes + 64)
        limits = replace(C.DEFAULT_LIMITS, max_bytes=input_bytes + 64)
        with self.assertRaises(C.StructureError): reader(rows, limits=limits).expression(5, ())
        OBSERVED["compact_input_cannot_bypass_generated_byte_cap"] = {
            "input_bytes": input_bytes, "expanded_subtree_bytes": expanded_bytes,
            "selected_byte_limit": limits.max_bytes}
        # The imported address can be far longer than its short source alias.
        # Two occurrences must use actual emitted-reference sizes in the reserve.
        rows = fixture()
        rows[-2:-2] = [{"ie": 9, "app": {"fn": 6, "arg": 6}},
                      {"ie": 10, "app": {"fn": 5, "arg": 9}}]
        relative = name(*("R" * 1024 for _ in range(16)))
        external = [{"source_name": OFNAT, "module": "33" * 32, "relative_name": relative}]
        ref = ["const", ["external", "33" * 32, relative], []]
        actual_bytes = len(C.canonical(["app", unary(2), ["app", ref, ref]]))
        limits = replace(C.DEFAULT_LIMITS, max_bytes=20000)
        self.assertLess(len(C.canonical(rows)), limits.max_bytes)
        self.assertGreater(actual_bytes, limits.max_bytes)
        with self.assertRaises(C.StructureError):
            S.SourceRows(rows, deepcopy(LOCAL), [], external, limits).expression(10, ())
        OBSERVED["external_relative_name_is_in_preallocation_bound"] = actual_bytes


SELECTED = ("test_zero_one_two_exact_constructors_and_decode",
    "test_unconverted_forms_and_ofnat_application_preserved",
    "test_census_only_reader_remains_nonconverting",
    "test_literal_spelling_and_unsupported_tags_refuse",
    "test_exact_nat_role_and_structured_name_required",
    "test_exact_nat_shape_and_complete_recursor_required",
    "test_lowering_reaches_types_bodies_and_recursor_rules",
    "test_depth_and_work_limits_charge_expanded_occurrences",
    "test_generated_bytes_refuse_with_small_compact_input")


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--output": raise ValueError("OUTPUT_REQUIRED")
    output = Path(sys.argv[2])
    if not output.is_dir() or output.resolve() != output: raise ValueError("CANONICAL_OUTPUT_REQUIRED")
    suite = unittest.TestSuite(LiteralControls(item) for item in SELECTED)
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(socket, "socket", side_effect=AssertionError("NETWORK_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "selected": list(SELECTED), "observed": OBSERVED,
        "scope": "BOUNDED_SYNTHETIC_SOURCE_LOWERING_STRUCTURE_ONLY",
        "mathematical_acceptance": False, "proof_calls": 0, "native_calls": 0,
        "network_operations": 0, "growth_advantage_claim": False}
    with (output / "controls-result.json").open("x", encoding="utf-8") as target:
        json.dump(report, target, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

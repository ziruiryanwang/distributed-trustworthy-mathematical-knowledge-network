"""Producer-decoder controls. These fixtures are NOT mathematical evidence.

No native checker, proof, certificate, network or file mutation is performed.
Root owns selection and execution of an exact source snapshot.
"""
from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C, source_rows as S

F, P = "11" * 32, "22" * 32


def name(label):
    return [["s", label]]


def ordinary_rows(universe="u"):
    # A valid polymorphic identity's syntax; this test does not check it.
    return [{"meta": {"synthetic_source_test_only": True}},
            {"in": 1, "str": {"pre": 0, "str": "identity"}},
            {"in": 2, "str": {"pre": 0, "str": universe}},
            {"il": 1, "param": 2},
            {"ie": 0, "sort": 1}, {"ie": 1, "bvar": 0}, {"ie": 2, "bvar": 1},
            {"ie": 3, "forallE": {"name": 0, "type": 1, "body": 2, "binderInfo": "default"}},
            {"ie": 4, "forallE": {"name": 0, "type": 0, "body": 3, "binderInfo": "default"}},
            {"ie": 5, "lam": {"name": 0, "type": 1, "body": 1, "binderInfo": "default"}},
            {"ie": 6, "lam": {"name": 0, "type": 0, "body": 5, "binderInfo": "default"}},
            {"def": {"name": 1, "levelParams": [2], "type": 4, "value": 6,
                     "hints": {"regular": 1}, "safety": "safe", "all": [1]}}]


def group_rows():
    # Deliberately only a structural group, never offered as a checked recursor.
    return [{"meta": {"synthetic_source_test_only": True}},
            {"in": 1, "str": {"pre": 0, "str": "Tree"}},
            {"in": 2, "str": {"pre": 1, "str": "leaf"}},
            {"in": 3, "str": {"pre": 1, "str": "rec"}},
            {"il": 1, "succ": 0}, {"ie": 0, "sort": 1},
            {"ie": 1, "const": {"name": 1, "us": []}},
            {"ie": 2, "const": {"name": 2, "us": []}},
            {"inductive": {
                "types": [{"name": 1, "levelParams": [], "type": 0, "all": [1], "ctors": [2],
                           "numParams": 0, "numIndices": 0, "numNested": 0,
                           "isRec": False, "isReflexive": False, "isUnsafe": False}],
                "ctors": [{"name": 2, "levelParams": [], "type": 1, "induct": 1,
                           "cidx": 0, "numParams": 0, "numFields": 0, "isUnsafe": False}],
                "recs": [{"name": 3, "levelParams": [], "type": 0, "all": [1],
                          "numParams": 0, "numIndices": 0, "numMotives": 1, "numMinors": 1,
                          "k": False, "isUnsafe": False,
                          "rules": [{"ctor": 2, "nfields": 0, "rhs": 2}]}]}}]


class SourceRowsTests(unittest.TestCase):
    def decode(self, rows, local=None, foundation=None, **kwargs):
        return S.decode_source(rows, local or [name("identity")], foundation or [], F, P, **kwargs)

    def test_positional_universe_and_binder_alpha(self):
        left = self.decode(ordinary_rows("u"))
        right = self.decode(ordinary_rows("renamedUniverse"))
        self.assertEqual(left.module, right.module)
        self.assertEqual(left.spec, right.spec)
        self.assertFalse(left.new_local_obligations()[0]["mathematical_admission"])
        self.assertEqual(left.spec["groups"][0]["declarations"][0]["type"][2],
                         ["sort", ["param", 0]])

    def test_exact_partition_and_census(self):
        with self.assertRaisesRegex(C.StructureError, "ROLE_OVERLAP"):
            self.decode(ordinary_rows(), foundation=[name("identity")])
        with self.assertRaisesRegex(C.StructureError, "CENSUS_MISMATCH"):
            self.decode(ordinary_rows(), local=[name("identity"), name("absent")])
        rows = ordinary_rows()
        rows.append(copy.deepcopy(rows[-1]))
        with self.assertRaisesRegex(C.StructureError, "DUPLICATE_DECLARATION"):
            self.decode(rows)

    def test_unknown_reference_not_inferred_foundation(self):
        rows = ordinary_rows()
        rows.insert(3, {"in": 3, "str": {"pre": 0, "str": "other"}})
        rows.insert(-1, {"ie": 7, "const": {"name": 3, "us": []}})
        rows[-1]["def"]["value"] = 7
        with self.assertRaisesRegex(C.StructureError, "UNMAPPED_REFERENCE"):
            self.decode(rows)
        env = self.decode(rows, foundation=[name("other")])
        body = next(C.parse_json(value) for value in env.bodies.values())
        self.assertEqual(body, ["const", ["foundation", name("other")], []])
        external = [{"source_name": name("other"), "module": "33" * 32,
                     "relative_name": [["s", "Distinct"], ["n", 7]]}]
        env = self.decode(rows, external_names=external)
        body = next(C.parse_json(value) for value in env.bodies.values())
        self.assertEqual(body[1], ["external", "33" * 32, external[0]["relative_name"]])

    def test_unsupported_literal_and_unsafe_refuse(self):
        rows = ordinary_rows()
        rows.insert(-1, {"ie": 7, "natVal": "0"})
        rows[-1]["def"]["value"] = 7
        with self.assertRaisesRegex(C.StructureError, "UNSUPPORTED_EXPRESSION"):
            self.decode(rows)
        rows = ordinary_rows()
        rows[-1]["def"]["safety"] = "unsafe"
        with self.assertRaisesRegex(C.StructureError, "UNSAFE_DEFINITION"):
            self.decode(rows)

    def test_expansion_budget_counts_shared_occurrences(self):
        rows = ordinary_rows()
        declaration = rows.pop()
        for index in range(7, 22):
            rows.append({"ie": index, "app": {"fn": index - 1, "arg": index - 1}})
        declaration["def"]["value"] = 21
        rows.append(declaration)
        with self.assertRaisesRegex(C.StructureError, "EXPANSION_LIMIT"):
            self.decode(rows, limits=replace(C.DEFAULT_LIMITS, max_nodes=80))

    def test_structured_names_and_complete_group(self):
        locals_ = [name("Tree"), name("Tree") + name("leaf"), name("Tree") + name("rec")]
        env = self.decode(group_rows(), local=locals_)
        self.assertEqual(len(env.spec["groups"][0]["declarations"]), 3)
        self.assertEqual(len(env.bodies), 1)
        self.assertNotEqual(C.name_key(locals_[1]), C.name_key(name("Tree.leaf")))
        with self.assertRaisesRegex(C.StructureError, "PARTIAL_LOCAL_GROUP"):
            self.decode(group_rows(), local=locals_[:1], foundation=locals_[1:])

    def test_rule_fields_and_local_axiom_refuse(self):
        rows = group_rows()
        rows[-1]["inductive"]["recs"][0]["rules"][0]["ignored"] = True
        locals_ = [name("Tree"), name("Tree") + name("leaf"), name("Tree") + name("rec")]
        with self.assertRaisesRegex(C.StructureError, "EXACT_RECORD_FIELDS"):
            self.decode(rows, local=locals_)
        rows = ordinary_rows()
        rows[-1] = {"axiom": {"name": 1, "levelParams": [2], "type": 4, "isUnsafe": False}}
        with self.assertRaisesRegex(C.StructureError, "LOCAL_AXIOM"):
            self.decode(rows)


if __name__ == "__main__":
    unittest.main()

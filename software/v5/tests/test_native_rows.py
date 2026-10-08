"""Independent adapter controls. Synthetic rows/claims do not prove mathematics.

These tests do not run a checker, verify receipts, or grant admission. Root
selects execution of immutable snapshots; no import-side runtime or file writes.
"""
from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C, model as M, native_rows as N

FOUNDATION = [{"meta": {"synthetic_adapter_test_only": True}}]
F, P = "11" * 32, "22" * 32
S0, S1 = ["sort", ["zero"]], ["sort", ["succ", ["zero"]]]


def name(label):
    return [["s", label]]


def ordinary(label, kind="definition", body=S0, hint="abbrev"):
    return {"kind": "ordinary", "declarations": [{
        "name": name(label), "kind": kind, "universes": 0, "type": copy.deepcopy(S1),
        "value_hash": None if kind == "theorem" else C.body_id(body, 0),
        "meta": {"hint": hint, "safety": "safe"} if kind == "definition"
        else {"safety": "safe"} if kind == "opaque" else {}}]}


def spec(*groups):
    return {"schema": C.SPEC_SCHEMA, "foundation": F, "policy": P,
            "groups": list(groups)}


def environment():
    env = M.ConditionalEnvironment(spec(ordinary("Local")))
    env.supply_local_value(name("Local"), S0)
    return env


def import_groups(env, parent, indices=None):
    summary, identity = C.summarize(parent), C.module_id(parent)
    env.add_claim(M.ImportClaim(identity, F, P, summary["group_root"],
        summary["group_count"], 0, "33" * 32, "44" * 32))
    for i in range(len(parent["groups"])) if indices is None else indices:
        env.add_import_opening(identity, C.group_opening(parent, i))
    return identity


def graph(rows):
    names, expressions, levels = {0: []}, {}, {0: ["zero"]}
    for row in rows:
        if "in" in row:
            item = row.get("str", row.get("num"))
            suffix = ["s", item["str"]] if "str" in row else ["n", item["i"]]
            names[row["in"]] = names[item["pre"]] + [suffix]
        if "ie" in row:
            expressions[row["ie"]] = {k: v for k, v in row.items() if k != "ie"}
        if "il" in row:
            levels[row["il"]] = {k: v for k, v in row.items() if k != "il"}
    return names, expressions, levels


class NativeRowsContracts(unittest.TestCase):
    def test_missing_definition_keeps_kind_and_hint_opaque_stays_distinct(self):
        env = environment()
        parent = spec(ordinary("D", body=S1, hint="opaque"), ordinary("O", "opaque", body=S1))
        owner = import_groups(env, parent)
        result = N.emit_conditional(env, FOUNDATION)
        rows, names = result["rows"], graph(result["rows"])[0]
        definition = next(r["moduleImportDef"] for r in rows if "moduleImportDef" in r)
        opaque = next(r["moduleImportOpaque"] for r in rows if "moduleImportOpaque" in r)
        self.assertEqual(definition["hints"], "opaque")
        self.assertNotIn("hints", opaque)
        self.assertEqual(definition["bodyHash"], list(bytes.fromhex(C.body_id(S1, 0))))
        self.assertEqual(names[definition["name"]], C.relocated_name(owner, name("D")))
        self.assertFalse(result["mathematical_admission"])
        self.assertEqual(result["certificate_verification"], "NOT_PERFORMED")
        self.assertEqual(len(result["unverified_module_premises"]), 2)

    def test_imported_theorem_has_no_proof_body_and_local_still_requires_one(self):
        env = environment()
        import_groups(env, spec(ordinary("Imported", "theorem")))
        # A supplied but irrelevant proof witness must not enter a theorem header.
        hidden = ["const", ["foundation", name("UnexposedProofHistory")], []]
        env.supply_body(hidden, 0)
        result = N.emit_conditional(env, FOUNDATION)
        headers = [r["moduleImportTheorem"] for r in result["rows"] if "moduleImportTheorem" in r]
        self.assertEqual(len(headers), 1)
        self.assertEqual(set(headers[0]), {"name", "levelParams", "type"})
        self.assertNotIn(name("UnexposedProofHistory"), graph(result["rows"])[0].values())
        local = M.ConditionalEnvironment(spec(ordinary("New", "theorem")))
        with self.assertRaisesRegex(C.StructureError, "LOCAL_PROOF_MISSING"):
            N.emit_conditional(local, FOUNDATION)
        local.supply_local_value(name("New"), hidden)
        emitted = N.emit_conditional(local, FOUNDATION)
        self.assertEqual(sum("thm" in r for r in emitted["rows"]), 1)
        self.assertFalse(emitted["mathematical_admission"])

    def test_identical_relative_bodies_relocate_under_defining_modules(self):
        body = ["const", ["local", name("Target")], []]
        p1 = spec(ordinary("Target"), ordinary("Use", body=body))
        p2 = spec(ordinary("Target"), ordinary("Use", body=body), ordinary("Different"))
        env = environment()
        owners = [import_groups(env, parent, [1]) for parent in (p1, p2)]
        self.assertNotEqual(*owners)
        env.supply_body(body, 0)
        rows = N.emit_conditional(env, FOUNDATION)["rows"]
        names, expressions, _ = graph(rows)
        bindings = {}
        for row in rows:
            if "def" in row and names[row["def"]["name"]][-1] == ["s", "Use"]:
                definition = row["def"]
                bindings[tuple(tuple(x) for x in names[definition["name"]])] = names[
                    expressions[definition["value"]]["const"]["name"]]
        self.assertEqual(len(bindings), 2)
        for owner in owners:
            self.assertEqual(bindings[tuple(tuple(x) for x in C.relocated_name(owner, name("Use")))],
                             C.relocated_name(owner, name("Target")))

    def test_all_import_rows_precede_new_locals_regardless_opening_order(self):
        env = environment()
        parent = spec(ordinary("First", body=S1), ordinary("Second", body=S1))
        import_groups(env, parent, [1, 0])
        rows = N.emit_conditional(env, FOUNDATION)["rows"]
        declarations = [next(iter(r)) for r in rows if len(r) == 1 and "meta" not in r]
        self.assertEqual(declarations, ["moduleImportDef", "moduleImportDef", "def"])

    def test_missing_new_definition_is_exact_body_demand(self):
        env = M.ConditionalEnvironment(spec(ordinary("New")))
        with self.assertRaises(M.DemandRequired) as caught:
            N.emit_conditional(env, FOUNDATION)
        need = caught.exception.demand
        self.assertEqual((need.kind, need.address.module, need.address.name, need.body_hash),
                         ("NeedBody", env.module, name("New"), C.body_id(S0, 0)))

    def test_whole_inductive_row_preserves_owner_and_rule_body(self):
        ind, ctor, rec = name("I"), [["s", "I"], ["s", "mk"]], [["s", "I"], ["s", "rec"]]
        group = {"kind": "inductive", "declarations": [
            {"name": ind, "kind": "inductive", "universes": 0, "type": S1,
             "value_hash": None, "meta": {"all": [ind], "constructors": [ctor],
                "num_params": 0, "num_indices": 0, "num_nested": 0,
                "is_recursive": False, "is_reflexive": False}},
            {"name": ctor, "kind": "constructor", "universes": 0,
             "type": ["const", ["local", ind], []], "value_hash": None,
             "meta": {"inductive": ind, "constructor_index": 0, "num_params": 0, "num_fields": 0}},
            {"name": rec, "kind": "recursor", "universes": 0, "type": S1,
             "value_hash": None, "meta": {"all": [ind], "num_params": 0,
                "num_indices": 0, "num_motives": 0, "num_minors": 0, "is_k": False,
                "rules": [{"constructor": ctor, "num_fields": 0,
                           "value_hash": C.body_id(["const", ["local", ctor], []], 0)}]}}]}
        env = environment()
        owner = import_groups(env, spec(group))
        with self.assertRaises(M.DemandRequired):
            N.emit_conditional(env, FOUNDATION)
        env.supply_body(["const", ["local", ctor], []], 0)
        result = N.emit_conditional(env, FOUNDATION)
        blocks = [row["inductive"] for row in result["rows"] if "inductive" in row]
        self.assertEqual(len(blocks), 1)
        block = blocks[0]
        self.assertEqual([len(block[k]) for k in ("types", "ctors", "recs")], [1, 1, 1])
        names, expressions, _ = graph(result["rows"])
        rule = block["recs"][0]["rules"][0]
        self.assertEqual(names[rule["ctor"]], C.relocated_name(owner, ctor))
        self.assertEqual(expressions[rule["rhs"]]["const"]["name"], rule["ctor"])
        self.assertEqual(len(result["unverified_module_premises"][0]["native_name_indices"]), 3)
        self.assertFalse(result["mathematical_admission"])

    def test_absolute_names_allow_exact_three_component_prefix(self):
        emitter = N.NativeRows(FOUNDATION)
        relative = [["s", "part" + str(i)] for i in range(64)]
        index = emitter.relative_name("ab" * 32, relative)
        self.assertEqual(len(graph(emitter.rows)[0][index]), 67)
        self.assertEqual(emitter.relative_name("ab" * 32, relative), index)
        with self.assertRaises(C.StructureError):
            emitter.relative_name("ab" * 32, relative + [["s", "overflow"]])

    def test_aggregate_canonical_byte_accounting_is_exact_and_atomic(self):
        row = {"in": 1, "str": {"pre": 0, "str": "x"}}
        required = len(C.canonical([*FOUNDATION, row]))
        fit = N.NativeRows(FOUNDATION, replace(C.DEFAULT_LIMITS, max_bytes=required))
        fit._append(row)
        self.assertEqual(fit.canonical_bytes, required)
        self.assertEqual(fit.canonical_bytes, len(C.canonical(fit.rows)))
        fail = N.NativeRows(FOUNDATION, replace(C.DEFAULT_LIMITS, max_bytes=required-1))
        before = copy.deepcopy((fail.rows, fail.canonical_bytes))
        with self.assertRaisesRegex(C.StructureError, "CANONICAL_BYTE_LIMIT"):
            fail._append(row)
        self.assertEqual((fail.rows, fail.canonical_bytes), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)

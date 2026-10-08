"""Independent finite tests of structural module bookkeeping, NOT mathematics.

Root selects and launches immutable snapshots; merely importing this file does
not run a checker, build a guest, verify a receipt, or create proof authority.
The fake ImportClaim digests below are intentionally unresolved premises.
"""
from __future__ import annotations

import copy
from dataclasses import asdict, replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec, model


F, P = "11" * 32, "22" * 32
SORT0 = ["sort", ["zero"]]
SORT1 = ["sort", ["succ", ["zero"]]]


def name(text):
    return [["s", text]]


def ordinary(text, kind="definition", value=SORT0):
    meta = ({"hint": {"regular": 0}, "safety": "safe"}
            if kind == "definition" else {"safety": "safe"} if kind == "opaque" else {})
    return {"kind": "ordinary", "declarations": [{
        "name": name(text), "kind": kind, "universes": 0,
        "type": copy.deepcopy(SORT1),
        "value_hash": None if kind == "theorem" else codec.body_id(value, 0),
        "meta": meta}]}


def spec(*groups, foundation=F, policy=P):
    return {"schema": codec.SPEC_SCHEMA, "foundation": foundation,
            "policy": policy, "groups": list(groups)}


def claim(parent, rank=0, journal="33" * 32, receipt="44" * 32):
    summary = codec.summarize(parent)
    return model.ImportClaim(codec.module_id(parent), summary["foundation"],
                             summary["policy"], summary["group_root"],
                             summary["group_count"], rank, journal, receipt)


def group_charge(group):
    return len(codec.canonical(group)) + sum(len(codec.canonical(d))
                                             for d in group["declarations"])


def state(env):
    """State plus counters: quota failure must not silently spend either."""
    return copy.deepcopy((env.claims, env.groups, env.declarations, env.bodies,
                          env.local_proofs, env._header_bytes, env._body_bytes))


def inductive_group():
    """Syntactically whole group; NOT asserted a native valid recursor."""
    ind, ctor, rec = name("I"), [["s", "I"], ["s", "mk"]], [["s", "I"], ["s", "rec"]]
    ds = [
        {"name": ind, "kind": "inductive", "universes": 0, "type": SORT1,
         "value_hash": None, "meta": {"all": [ind], "constructors": [ctor],
             "num_params": 0, "num_indices": 0, "num_nested": 0,
             "is_recursive": False, "is_reflexive": False}},
        {"name": ctor, "kind": "constructor", "universes": 0,
         "type": ["const", ["local", ind], []], "value_hash": None,
         "meta": {"inductive": ind, "constructor_index": 0,
                  "num_params": 0, "num_fields": 0}},
        {"name": rec, "kind": "recursor", "universes": 0, "type": SORT1,
         "value_hash": None, "meta": {"all": [ind], "num_params": 0,
             "num_indices": 0, "num_motives": 0, "num_minors": 0,
             "is_k": False, "rules": [{"constructor": ctor, "num_fields": 0,
                                        "value_hash": codec.body_id(SORT0, 0)}]}}]
    return {"kind": "inductive", "declarations": copy.deepcopy(ds)}


class ModuleStructuralControls(unittest.TestCase):
    def test_decode_rejects_duplicate_float_and_boolean_integer(self):
        for raw in (b'{"x":1,"x":2}', b'{"x":1.0}', b'{"x":NaN}'):
            with self.subTest(raw=raw), self.assertRaises(codec.StructureError):
                codec.parse_json(raw)
        wrong = ordinary("D")
        wrong["declarations"][0]["universes"] = True
        with self.assertRaises(codec.StructureError):
            codec.validate_group(wrong)

    def test_expression_scope_and_work_limits(self):
        for expression, universes in ((["bvar", 0], 0),
                                     (["sort", ["param", 0]], 0),
                                     (["const", ["external", "not-a-hash", name("D")], []], 0)):
            with self.subTest(expression=expression), self.assertRaises(codec.StructureError):
                codec.validate_expr(expression, universes)
        codec.validate_expr(["forall", "default", SORT0, ["bvar", 0]], 0)
        with self.assertRaisesRegex(codec.StructureError, "STRUCTURE_WORK_LIMIT"):
            codec.validate_expr(SORT1, 0, replace(codec.DEFAULT_LIMITS, max_nodes=1))

    def test_unique_structured_names_and_export_addresses(self):
        dotted, hierarchical = [["s", "I.rec"]], [["s", "I"], ["s", "rec"]]
        self.assertNotEqual(codec.name_key(dotted), codec.name_key(hierarchical))
        module = codec.module_id(spec(ordinary("D")))
        self.assertNotEqual(codec.export_id(module, dotted), codec.export_id(module, hierarchical))
        self.assertNotEqual(codec.export_id(module, name("D")), codec.export_id("55" * 32, name("D")))
        with self.assertRaisesRegex(codec.StructureError, "DUPLICATE_MODULE_DECLARATION"):
            codec.validate_spec(spec(ordinary("D"), ordinary("D", "theorem")))
        axiom = ordinary("A", "theorem")
        axiom["declarations"][0]["kind"] = "axiom"
        with self.assertRaisesRegex(codec.StructureError, "DECLARATION_KIND"):
            codec.validate_group(axiom)

    def test_openings_at_odd_and_power_of_two_boundaries(self):
        for count in (1, 2, 3, 4, 5):
            parent = spec(*(ordinary("D" + str(i)) for i in range(count)))
            identity = codec.module_id(parent)
            for i, group in enumerate(parent["groups"]):
                with self.subTest(count=count, index=i):
                    self.assertEqual(codec.verify_group_opening(identity, codec.group_opening(parent, i)), group)

    def test_opening_mutations_refuse(self):
        parent = spec(ordinary("A"), ordinary("B"), ordinary("C"))
        identity, opening = codec.module_id(parent), codec.group_opening(parent, 2)
        changes = []
        for field, value in (("index", 0), ("index", True)):
            wrong = copy.deepcopy(opening); wrong[field] = value; changes.append(wrong)
        wrong = copy.deepcopy(opening); wrong["siblings"][0] = "00" * 32; changes.append(wrong)
        wrong = copy.deepcopy(opening); wrong["siblings"].append("00" * 32); changes.append(wrong)
        wrong = copy.deepcopy(opening); wrong["siblings"].pop(); changes.append(wrong)
        wrong = copy.deepcopy(opening); wrong["summary"]["group_count"] = 4; changes.append(wrong)
        wrong = copy.deepcopy(opening); wrong["group"]["declarations"][0]["meta"]["hint"] = "abbrev"; changes.append(wrong)
        for i, wrong in enumerate(changes):
            with self.subTest(mutation=i), self.assertRaises(codec.StructureError):
                codec.verify_group_opening(identity, wrong)
        with self.assertRaises(codec.StructureError):
            codec.verify_group_opening("00" * 32, opening)

    def test_local_visibility_never_becomes_fetchable_import(self):
        env = model.ConditionalEnvironment(spec(ordinary("A"), ordinary("B")))
        a, b = model.Address.of(env.module, name("A")), model.Address.of(env.module, name("B"))
        self.assertEqual(env.lookup(a, 1).role, "LOCAL_MUST_CHECK")
        for address, cutoff in ((a, 0), (b, 0), (b, 1)):
            with self.subTest(address=address, cutoff=cutoff), self.assertRaises(model.NotVisible):
                env.lookup(address, cutoff)
        with self.assertRaisesRegex(codec.StructureError, "UNDECLARED_LOCAL_REFERENCE"):
            env.lookup(model.Address.of(env.module, name("Missing")), 2)
        with self.assertRaisesRegex(codec.StructureError, "MUTUAL_VISIBILITY_SCOPE"):
            env.lookup(a, 0, checking_inductive_group=0)
        with self.assertRaisesRegex(codec.StructureError, "IMPORT_CURRENT_LOCAL_MODULE"):
            env.add_claim(claim(env.spec))

    def test_import_declaration_then_body_demands_retain_kind(self):
        parent = spec(ordinary("P"))
        c = claim(parent)
        env = model.ConditionalEnvironment(spec(ordinary("L")))
        address = model.Address.of(c.module, name("P"))
        with self.assertRaises(model.DemandRequired) as missing:
            env.lookup(address, 0)
        self.assertEqual(missing.exception.demand, model.Need("NeedDeclaration", address))
        opening = codec.group_opening(parent, 0)
        with self.assertRaisesRegex(codec.StructureError, "MISSING_UNVERIFIED_IMPORT_PREMISE"):
            env.add_import_opening(c.module, opening)
        env.add_claim(c); env.add_import_opening(c.module, opening)
        d = env.lookup(address, 0).descriptor
        self.assertEqual(d["kind"], "definition")
        self.assertEqual(d["meta"]["hint"], {"regular": 0})
        with self.assertRaises(model.DemandRequired) as missing:
            env.demand_definition_body(address, 0)
        self.assertEqual(missing.exception.demand, model.Need("NeedBody", address, d["value_hash"]))
        env.supply_body(SORT1, 0)  # An unrelated body must not satisfy the demand.
        with self.assertRaises(model.DemandRequired):
            env.demand_definition_body(address, 0)
        env.supply_body(SORT0, 0)
        self.assertEqual(env.demand_definition_body(address, 0), SORT0)
        before = state(env)
        env.add_claim(c); env.add_import_opening(c.module, opening); env.supply_body(SORT0, 0)
        self.assertEqual(state(env), before)

    def test_opaque_is_not_a_missing_transparent_definition(self):
        parent = spec(ordinary("O", "opaque"))
        c = claim(parent); env = model.ConditionalEnvironment(spec(ordinary("L")))
        env.add_claim(c); env.add_import_opening(c.module, codec.group_opening(parent, 0))
        address = model.Address.of(c.module, name("O"))
        self.assertEqual(env.lookup(address, 0).descriptor["kind"], "opaque")
        with self.assertRaisesRegex(codec.StructureError, "DELTA_REQUIRES_DEFINITION_KIND"):
            env.demand_definition_body(address, 0)

    def test_same_relative_body_is_interpreted_under_defining_module(self):
        expression = ["const", ["local", name("x")], []]
        left, right = spec(ordinary("L", value=expression)), spec(ordinary("R", value=expression))
        left_id, right_id = codec.module_id(left), codec.module_id(right)
        self.assertNotEqual(left_id, right_id)
        self.assertEqual(left["groups"][0]["declarations"][0]["value_hash"],
                         right["groups"][0]["declarations"][0]["value_hash"])
        left_expr = codec.relocate_expr(expression, left_id, 0)
        right_expr = codec.relocate_expr(expression, right_id, 0)
        self.assertNotEqual(left_expr, right_expr)
        self.assertEqual(left_expr[1], ["absolute", codec.relocated_name(left_id, name("x"))])
        external = ["const", ["external", right_id, name("x")], []]
        self.assertEqual(codec.relocate_expr(external, left_id, 0)[1], right_expr[1])

    def test_alternative_receipts_are_invocation_choices_not_module_identity(self):
        parent = spec(ordinary("P")); c = claim(parent)
        alternative = replace(c, rank=3, journal_hash="66" * 32, receipt_hash="77" * 32)
        local = spec(ordinary("L")); first = model.ConditionalEnvironment(local)
        first.add_claim(c); before = state(first)
        with self.assertRaisesRegex(codec.StructureError, "CLAIM_MUTATION"):
            first.add_claim(alternative)
        self.assertEqual(state(first), before)
        second = model.ConditionalEnvironment(local); second.add_claim(alternative)
        self.assertEqual(first.claims[c.module].module, second.claims[c.module].module)
        self.assertNotEqual(first.conditional_premises()["suggested_rank"],
                            second.conditional_premises()["suggested_rank"])
        self.assertFalse(second.conditional_premises()["mathematical_admission"])

    def test_policy_mismatch_and_rank_overflow_refuse_without_admission(self):
        env = model.ConditionalEnvironment(spec(ordinary("L")))
        for parent in (spec(ordinary("P"), foundation="88" * 32),
                       spec(ordinary("P"), policy="99" * 32)):
            before = state(env)
            with self.assertRaisesRegex(codec.StructureError, "IMPORT_FOUNDATION_POLICY"):
                env.add_claim(claim(parent))
            self.assertEqual(state(env), before)
        env.add_claim(claim(spec(ordinary("P")), rank=2**64 - 1))
        with self.assertRaisesRegex(codec.StructureError, "BOUNDED_UNSIGNED_INTEGER"):
            env.conditional_premises()

    def test_aggregate_imported_headers_quota_is_atomic(self):
        local = spec(ordinary("L"))
        parents = [spec(ordinary("P" + str(i))) for i in range(2)]
        claims = [claim(parent) for parent in parents]
        base = len(codec.canonical(local)) + group_charge(local["groups"][0])
        total = base + sum(len(codec.canonical(asdict(c))) for c in claims)
        total += sum(group_charge(parent["groups"][0]) for parent in parents)
        bound = total - 1  # Every single object fits; their aggregate does not.
        limits = replace(codec.DEFAULT_LIMITS, max_bytes=bound)
        env = model.ConditionalEnvironment(local, limits)
        for c in claims: env.add_claim(c)
        openings = [codec.group_opening(parent, 0) for parent in parents]
        self.assertTrue(all(len(codec.canonical(op)) < bound for op in openings))
        env.add_import_opening(claims[0].module, openings[0]); before = state(env)
        with self.assertRaisesRegex(codec.StructureError, "WITNESS_TOTAL_CANONICAL_BYTE_LIMIT"):
            env.add_import_opening(claims[1].module, openings[1])
        self.assertEqual(state(env), before)
        self.assertNotIn((claims[1].module, 0), env.groups)

    def test_aggregate_body_and_claim_quotas_are_atomic(self):
        local = spec(ordinary("L"))
        base = len(codec.canonical(local)) + group_charge(local["groups"][0])
        env = model.ConditionalEnvironment(local, replace(codec.DEFAULT_LIMITS,
            max_bytes=base + len(codec.canonical(SORT0)) - 1))
        before = state(env)
        with self.assertRaisesRegex(codec.StructureError, "WITNESS_TOTAL_CANONICAL_BYTE_LIMIT"):
            env.supply_local_value(name("L"), SORT0)
        self.assertEqual(state(env), before)
        c = claim(spec(ordinary("P")))
        env = model.ConditionalEnvironment(local, replace(codec.DEFAULT_LIMITS,
            max_bytes=base + len(codec.canonical(asdict(c))) - 1))
        before = state(env)
        with self.assertRaisesRegex(codec.StructureError, "WITNESS_TOTAL_CANONICAL_BYTE_LIMIT"):
            env.add_claim(c)
        self.assertEqual(state(env), before)

    def test_new_values_cannot_be_reclassified_or_omitted(self):
        local = spec(ordinary("D"), ordinary("T", "theorem"))
        env = model.ConditionalEnvironment(local)
        with self.assertRaisesRegex(codec.StructureError, "NEW_LOCAL_VALUE_MUST_BE_PRESENT"):
            env.new_local_obligations()
        before = state(env)
        with self.assertRaisesRegex(codec.StructureError, "LOCAL_VALUE_COMMITMENT"):
            env.supply_local_value(name("D"), SORT1)
        self.assertEqual(state(env), before)
        env.supply_local_value(name("D"), SORT0)
        with self.assertRaisesRegex(codec.StructureError, "NEW_LOCAL_VALUE_MUST_BE_PRESENT"):
            env.new_local_obligations()
        env.supply_local_value(name("T"), SORT0)  # Deliberately NOT a checked proof.
        obligations = env.new_local_obligations()
        self.assertEqual(len(obligations), 2)
        self.assertTrue(all(x["role"] == "LOCAL_MUST_CHECK" and not x["mathematical_admission"]
                            for x in obligations))
        report = env.conditional_premises()
        self.assertEqual(report["certificate_verification"], "NOT_PERFORMED")
        self.assertFalse(report["mathematical_admission"])
        before = state(env)
        with self.assertRaisesRegex(codec.StructureError, "LOCAL_PROOF_MUTATION"):
            env.supply_local_value(name("T"), SORT1)
        self.assertEqual(state(env), before)

    def test_inductive_groups_whole_and_visibility_atomic(self):
        group = inductive_group(); codec.validate_group(group)
        for missing in (0, 1, 2):
            wrong = copy.deepcopy(group); del wrong["declarations"][missing]
            with self.subTest(missing=missing), self.assertRaises(codec.StructureError):
                codec.validate_group(wrong)
        wrong = copy.deepcopy(group)
        wrong["declarations"][1]["meta"]["constructor_index"] = 1
        with self.assertRaisesRegex(codec.StructureError, "CONSTRUCTOR_OWNERSHIP"):
            codec.validate_group(wrong)
        env = model.ConditionalEnvironment(spec(group))
        address = model.Address.of(env.module, name("I"))
        with self.assertRaises(model.NotVisible): env.lookup(address, 0)
        self.assertEqual(env.lookup(address, 0, checking_inductive_group=0).role, "LOCAL_MUST_CHECK")
        with self.assertRaisesRegex(codec.StructureError, "NEW_LOCAL_RECURSOR_RULE_MUST_BE_PRESENT"):
            env.new_local_obligations()
        env.supply_body(SORT0, 0)
        self.assertFalse(env.new_local_obligations()[0]["mathematical_admission"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

"""Pure combined-batch controls; no Lean, catalog, filesystem mutation or warrant.

Root selects execution separately. These synthetic dependency graphs exercise
only successor_envelopes; importing the controller never invokes its main.
"""
from pathlib import Path
import copy
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_evidence as E
import run_successor_admission as R

R.E = E


def name(text):
    return [[0, {"$bytes": list(part.encode("utf-8"))}] for part in text.split(".")]


def unit(own, dependency):
    own_name = name(own)
    type_dag = [E.EXPR_FORMAT, [], [[2, name("Nat"), []]], 0]
    body_dag = [E.EXPR_FORMAT, [], [[2, name(dependency), []]], 0]
    return [E.UNIT_FORMAT,
            [0, own_name, [], type_dag, body_dag, [2, 1], [own_name]],
            [[own_name, 1, [], type_dag, [body_dag, [2, 1], [own_name]]]]]


def recount(bundle):
    bundle["stats"] = {
        "source_records_enumerated": len(bundle["units"]),
        "selected_units": len(bundle["units"]),
        "dependency_edges": 0,
        "scan_nodes": 0,
        "unit_json_bytes": sum(len(E.canonical_json(x)) for x in bundle["units"]),
        "boundary_imports": len(bundle["boundary_imports"]),
    }
    if "unresolved_imports" in bundle:
        bundle["stats"]["unresolved_imports"] = len(bundle["unresolved_imports"])
    if bundle["schema"] == "DMKN_ORDINARY_MISSING_IMPORT_BUNDLE_V1":
        bundle["stats"]["lookup_count"] = 4


def bundle(schema, targets, imports, units, unresolved=None):
    result = {
        "schema": schema, "assurance": "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE",
        "profile_id": R.PROFILE, "context_id": R.PARENT, "basis_id": R.BASIS,
        "targets": [name(x) for x in targets], "boundary_imports": imports,
        "units": units,
    }
    if unresolved is not None:
        result["unresolved_imports"] = [name(x) for x in unresolved]
    recount(result)
    return result


class CombinedAdmissionChecks(unittest.TestCase):
    def setUp(self):
        self.target = name("Consumer.target")
        self.nat, self.accepted = "a" * 64, "b" * 64
        self.prepared = {E.name_key(name("Nat")): self.nat}
        self.parent = {**self.prepared, E.name_key(name("K.accepted")): self.accepted}
        self.candidate = bundle("DMKN_ORDINARY_CANDIDATE_BUNDLE_V1", ["Consumer.target"],
            [[name("Nat"), self.nat]], [unit("Consumer.target", "Missing.lemma")],
            ["Missing.lemma"])
        self.supplement = bundle("DMKN_ORDINARY_MISSING_IMPORT_BUNDLE_V1", ["Missing.lemma"],
            [[name("Nat"), self.nat], [name("K.accepted"), self.accepted]],
            [unit("Support.helper", "K.accepted"), unit("Missing.lemma", "Support.helper")])

    def planned(self, *, with_supplement=True):
        # Assert nonmutation even for refusal after partially yielding evidence.
        before = copy.deepcopy((self.candidate, self.supplement, self.prepared, self.parent))
        try:
            return list(R.successor_envelopes(self.candidate, self.prepared, self.parent,
                self.target, self.supplement if with_supplement else None))
        finally:
            self.assertEqual((self.candidate, self.supplement, self.prepared, self.parent), before)

    def refuses(self, marker, *, with_supplement=True):
        with self.assertRaisesRegex(ValueError, marker):
            self.planned(with_supplement=with_supplement)

    def test_order_exact_units_and_provisional_ids(self):
        results = self.planned()
        self.assertEqual([lane for _, _, lane in results], ["supplement", "supplement", "candidate"])
        self.assertEqual([raw for _, raw, _ in results],
            [E.canonical_json(x) for x in self.supplement["units"] + self.candidate["units"]])
        helper_id = E.export_id(R.PROFILE, results[0][0].unit_id, name("Support.helper"))
        lemma_id = E.export_id(R.PROFILE, results[1][0].unit_id, name("Missing.lemma"))
        self.assertIn([name("Support.helper"), helper_id], results[1][0].document["imports"])
        self.assertIn([name("Missing.lemma"), lemma_id], results[2][0].document["imports"])
        # A supplemental K import legitimately does not appear in preparation.
        self.assertNotIn(E.name_key(name("K.accepted")), self.prepared)
        self.assertIn([name("K.accepted"), self.accepted], results[0][0].document["imports"])

    def test_missing_without_supplement_refuses(self):
        self.refuses("UNACCEPTED_CANDIDATE_IMPORTS count=1", with_supplement=False)

    def test_no_missing_still_works_and_rejects_unneeded_supplement(self):
        self.candidate["units"] = [unit("Consumer.target", "K.accepted")]
        self.candidate["unresolved_imports"] = [name("K.accepted")]
        recount(self.candidate)
        self.assertEqual(len(self.planned(with_supplement=False)), 1)
        self.refuses("SUPPLEMENT_NOT_NEEDED")

    def test_legacy_exact_claim_route_unchanged(self):
        self.prepared[E.name_key(name("K.accepted"))] = self.accepted
        self.candidate = bundle("DMKN_ORDINARY_SUCCESSOR_BUNDLE_V1", ["Consumer.target"],
            [[name("Nat"), self.nat], [name("K.accepted"), self.accepted]],
            [unit("Consumer.target", "K.accepted")])
        self.assertEqual(len(self.planned(with_supplement=False)), 1)
        self.refuses("SUPPLEMENT_NOT_NEEDED")

    def test_missing_target_set_must_be_exact_and_unique(self):
        for targets in ([], [name("Other.lemma")], [name("Missing.lemma")] * 2,
                        [name("Missing.lemma"), name("Other.lemma")]):
            with self.subTest(targets=targets):
                self.supplement["targets"] = targets
                self.refuses("SUPPLEMENT_EXACT_MISSING_TARGETS")

    def test_supplement_parent_ids_must_match(self):
        self.supplement["boundary_imports"][1][1] = "c" * 64
        self.refuses("SUPPLEMENT_PARENT_IDENTITY")

    def test_original_claim_still_requires_prepared_and_parent(self):
        for mapping in (self.prepared, self.parent):
            with self.subTest(mapping="prepared" if mapping is self.prepared else "parent"):
                key = E.name_key(name("Nat"))
                mapping[key] = "c" * 64
                self.refuses("SUCCESSOR_BOUNDARY_IDENTITY")
                mapping[key] = self.nat

    def test_forward_supplement_or_future_candidate_reference_refuses(self):
        original = copy.deepcopy(self.supplement["units"])
        for units in (list(reversed(original)),
                      [unit("Support.helper", "Consumer.target"), original[1]]):
            with self.subTest(units=units):
                self.supplement["units"] = units
                recount(self.supplement)
                self.refuses("UNBOUND_SUPPLEMENT_REFERENCE")

    def test_parent_and_cross_lane_output_collisions_refuse(self):
        original = copy.deepcopy(self.supplement["units"])
        for units in ([unit("K.accepted", "Nat")] + original,
                      original + [unit("Consumer.target", "Missing.lemma")]):
            with self.subTest(units=units):
                self.supplement["units"] = units
                recount(self.supplement)
                self.refuses("SUCCESSOR_EXISTING_OR_DUPLICATE_NAME")

    def test_missing_target_must_actually_be_exported(self):
        self.supplement["units"] = self.supplement["units"][:1]
        recount(self.supplement)
        self.refuses("SUPPLEMENT_MISSING_TARGET_OUTPUT")

    def test_undeclared_extra_supplement_output_is_not_candidate_import(self):
        self.candidate["units"] = [unit("Consumer.target", "Support.helper")]
        recount(self.candidate)
        self.refuses("UNBOUND_SUCCESSOR_REFERENCE")

    def test_each_lane_bytes_checked_even_after_yield(self):
        for selected, marker in ((self.supplement, "SUPPLEMENT_UNIT_BYTES"),
                                 (self.candidate, "SUCCESSOR_TARGET_OR_BYTES")):
            with self.subTest(marker=marker):
                selected["stats"]["unit_json_bytes"] += 1
                self.refuses(marker)
                selected["stats"]["unit_json_bytes"] -= 1

    def test_combined_count_is_not_two_independent_allowances(self):
        self.candidate["units"] *= 1023
        recount(self.candidate)
        self.refuses("COMBINED_UNIT_COUNT_BOUND")

    def test_final_target_must_come_from_original_candidate(self):
        self.supplement["units"].append(unit("Consumer.target", "Missing.lemma"))
        self.candidate["units"] = [unit("Consumer.other", "Missing.lemma")]
        recount(self.supplement)
        recount(self.candidate)
        self.refuses("SUCCESSOR_TARGET_OR_BYTES")

    def test_supplement_semantic_context_and_assurance_are_bound(self):
        for field in ("profile_id", "context_id", "basis_id", "assurance"):
            with self.subTest(field=field):
                original = self.supplement[field]
                self.supplement[field] = "d" * 64
                self.refuses("EXACT_SUPPLEMENT_BUNDLE")
                self.supplement[field] = original

    def test_supplement_lookup_count_is_bounded(self):
        self.supplement["stats"]["lookup_count"] = 65537
        self.refuses("SUPPLEMENT_STATISTICS_CENSUS")


if __name__ == "__main__":
    unittest.main(verbosity=2)

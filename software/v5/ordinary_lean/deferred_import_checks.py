"""Pure deferred-name binding controls; no Lean, catalog, files or acceptance.

Root must select execution separately. These synthetic maps are not warrants.
Only the narrow controller resolver is called; main/admission is never invoked.
"""
from pathlib import Path
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_evidence as E
import run_successor_admission as R

R.E = E


def name(text):
    return [[0, {"$bytes": list(part.encode("utf-8"))}] for part in text.split(".")]


def packet(claimed=(), unresolved=(), *, candidate=True):
    result = {
        "schema": "DMKN_ORDINARY_CANDIDATE_BUNDLE_V1" if candidate
        else "DMKN_ORDINARY_SUCCESSOR_BUNDLE_V1",
        "boundary_imports": [list(row) for row in claimed],
    }
    if candidate:
        result["unresolved_imports"] = list(unresolved)
    return result


class DeferredBindingChecks(unittest.TestCase):
    def setUp(self):
        self.a, self.b, self.c = map(name, ("Fixture.a", "Fixture.b", "Fixture.c"))
        self.ka, self.kb, self.kc = map(E.name_key, (self.a, self.b, self.c))
        self.ia, self.ib, self.ic = "a" * 64, "b" * 64, "c" * 64
        self.prepared = {self.ka: self.ia}
        self.parent = {self.ka: self.ia, self.kb: self.ib, self.kc: self.ic}

    def resolve(self, bundle):
        before_prepared, before_parent = dict(self.prepared), dict(self.parent)
        try:
            return R.resolve_candidate_imports(bundle, self.prepared, self.parent)
        finally:
            self.assertEqual(self.prepared, before_prepared)
            self.assertEqual(self.parent, before_parent)

    def test_legacy_route_selects_only_claimed_exact_ids(self):
        result = self.resolve(packet([(self.a, self.ia)], candidate=False))
        self.assertEqual(result, ({self.ka: self.ia}, 1, 0))

    def test_candidate_resolves_reached_names_only(self):
        result = self.resolve(packet([(self.a, self.ia)], [self.b]))
        self.assertEqual(result, ({self.ka: self.ia, self.kb: self.ib}, 1, 1))
        self.assertNotIn(self.kc, result[0])

    def test_unclaimed_only_does_not_need_prepared_membership(self):
        self.assertEqual(self.resolve(packet(unresolved=[self.b])),
                         ({self.kb: self.ib}, 0, 1))

    def test_wrong_claimed_id_refuses(self):
        with self.assertRaisesRegex(ValueError, "SUCCESSOR_BOUNDARY_IDENTITY"):
            self.resolve(packet([(self.a, self.ib)]))

    def test_claimed_id_absent_from_prepared_refuses(self):
        with self.assertRaisesRegex(ValueError, "SUCCESSOR_BOUNDARY_IDENTITY"):
            self.resolve(packet([(self.b, self.ib)]))

    def test_claimed_parent_disagreement_refuses(self):
        self.parent[self.ka] = self.ic
        with self.assertRaisesRegex(ValueError, "SUCCESSOR_BOUNDARY_IDENTITY"):
            self.resolve(packet([(self.a, self.ia)]))

    def test_duplicate_claimed_refuses(self):
        with self.assertRaisesRegex(ValueError, "SUCCESSOR_BOUNDARY_IDENTITY"):
            self.resolve(packet([(self.a, self.ia), (self.a, self.ia)]))

    def test_duplicate_unresolved_refuses(self):
        with self.assertRaisesRegex(ValueError, "SUCCESSOR_DUPLICATE_OR_PREPARED_UNCLAIMED_IMPORT"):
            self.resolve(packet(unresolved=[self.b, self.b]))

    def test_mixed_claimed_unresolved_refuses(self):
        with self.assertRaisesRegex(ValueError, "SUCCESSOR_DUPLICATE_OR_PREPARED_UNCLAIMED_IMPORT"):
            self.resolve(packet([(self.a, self.ia)], [self.a]))

    def test_prepared_name_cannot_drop_its_claimed_id(self):
        with self.assertRaisesRegex(ValueError, "SUCCESSOR_DUPLICATE_OR_PREPARED_UNCLAIMED_IMPORT"):
            self.resolve(packet(unresolved=[self.a]))

    def test_all_missing_names_reported_together(self):
        left, right = name("Missing.left"), name("Missing.right")
        with self.assertRaises(ValueError) as raised:
            self.resolve(packet(unresolved=[left, self.b, right]))
        message = str(raised.exception)
        self.assertIn("UNACCEPTED_CANDIDATE_IMPORTS count=2", message)
        prefixes = json.loads(message.partition(" encoded_name_prefixes=")[2])
        self.assertEqual(prefixes, [E.name_key(left).decode(), E.name_key(right).decode()])

    def test_aggregate_bound_precedes_large_iteration(self):
        with self.assertRaisesRegex(ValueError, "SUCCESSOR_AGGREGATE_BOUNDARY_BOUND"):
            self.resolve(packet([(self.a, self.ia)], [self.b] * 65536))

    def test_missing_diagnostic_has_byte_bound(self):
        # A legal long encoded name must not defeat the supervisor's log cap.
        huge = name("x" * 10000)
        with self.assertRaises(ValueError) as raised:
            self.resolve(packet(unresolved=[huge]))
        message = str(raised.exception)
        self.assertIn("UNACCEPTED_CANDIDATE_IMPORTS count=1", message)
        self.assertLessEqual(len(message.encode("utf-8")), 9000)


if __name__ == "__main__":
    unittest.main(verbosity=2)

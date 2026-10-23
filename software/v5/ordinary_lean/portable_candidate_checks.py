"""Finite candidate/V2 identity controls; synthetic syntax, not mathematics."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as PE
import portable_candidate as B
import semantic_identity_checks as F


class CandidateChecks(unittest.TestCase):
    def setUp(self):
        self.s, self.f, self.root = S.semantic_id(), S.foundation_id(), "a"*64
        self.nat = F.name("Nat")
        self.nat_id = S.basis_symbol_id(self.s, self.f, self.nat)
        self.parent = {E.name_key(self.nat): self.nat_id}
        self.prepared = dict(self.parent)
        self.lookups = []

    def unit(self, text, refs=()):
        result = E.strict_json(F.evidence(self.s))["unit"]
        name = F.name(text)
        result[1][1] = name
        result[1][6] = [name]
        result[2][0][0] = name
        result[2][0][4][2] = [name]
        if refs:
            nodes = [[2, F.name(ref), []] for ref in refs]
            root = 0
            for index in range(1, len(refs)):
                nodes.append([3, root, index])
                root = len(nodes)-1
            value = [E.EXPR_FORMAT, [], nodes, root]
            result[1][4] = value
            result[2][0][4][0] = value
        return result

    def bundle(self, units=None, unresolved=()):
        units = [self.unit("First"), self.unit("Second", ("First",))] if units is None else units
        return {"schema": B.SCHEMA, "assurance": B.ASSURANCE, "semantic_id": self.s,
            "foundation_id": self.f, "context_root": self.root,
            "targets": [units[-1][2][0][0]], "boundary_imports": [[self.nat, self.nat_id]],
            "unresolved_imports": [F.name(x) for x in unresolved], "units": units,
            "stats": {"source_records_enumerated": 0, "selected_units": len(units),
                "dependency_edges": 0, "scan_nodes": 0,
                "unit_json_bytes": sum(len(E.canonical_json(unit)) for unit in units),
                "boundary_imports": 1, "unresolved_imports": len(unresolved)}}

    def bind(self, doc, **changes):
        def lookup(name):
            self.lookups.append(E.name_key(name))
            return self.parent.get(E.name_key(name))
        args = dict(semantic_id=self.s, foundation_id=self.f, context_root=self.root,
                    expected_targets=doc["targets"], prepared_bindings=self.prepared,
                    warranted_symbol=lookup)
        args.update(changes)
        return B.bind_candidate(E.canonical_json(doc), **args)

    def test_exact_new_chain_and_no_global_map_scan(self):
        doc = self.bundle()
        out = self.bind(doc)
        self.assertEqual(out.status, "READY")
        self.assertFalse(out.mathematical_acceptance)
        first, second = map(PE.read_evidence, out.raw_units)
        self.assertEqual(first.document["unit"], doc["units"][0])
        self.assertEqual(second.document["unit"], doc["units"][1])
        self.assertEqual(dict((E.name_key(n), s) for n, s in second.document["imports"])[E.name_key(F.name("First"))],
                         S.export_id(self.s, first.unit_id, F.name("First")))
        self.assertEqual(len(self.lookups), len(set(self.lookups)))
        self.assertEqual(set(self.lookups), {E.name_key(self.nat), E.name_key(F.name("First")),
                                            E.name_key(F.name("Second"))})

    def test_full_missing_frontier_has_no_evidence(self):
        doc = self.bundle([self.unit("First", ("MissingA", "MissingB"))], ("MissingA", "MissingB"))
        out = self.bind(doc)
        self.assertEqual(out.status, "NEEDS_LOCAL_INTERPRETATIONS")
        self.assertEqual(out.missing_names, tuple(sorted(E.name_key(F.name(x)) for x in ("MissingA", "MissingB"))))
        self.assertEqual(out.raw_units, ())

    def test_explicit_unclaimed_local_interpretation(self):
        doc = self.bundle([self.unit("First", ("Accepted",))], ("Accepted",))
        self.parent[E.name_key(F.name("Accepted"))] = "b"*64
        out = self.bind(doc)
        self.assertEqual(out.status, "READY")
        imports = PE.read_evidence(out.raw_units[0]).document["imports"]
        self.assertIn([F.name("Accepted"), "b"*64], imports)

    def test_claimed_identity_is_never_substituted(self):
        doc = self.bundle()
        doc["boundary_imports"][0][1] = "b"*64
        with self.assertRaisesRegex(ValueError, "CANDIDATE_CLAIMED_IDENTITY"):
            self.bind(doc)

    def test_claimed_parent_disagreement(self):
        self.parent[E.name_key(self.nat)] = "b"*64
        with self.assertRaisesRegex(ValueError, "CANDIDATE_CLAIMED_IDENTITY"):
            self.bind(self.bundle())

    def test_prepared_name_cannot_become_unclaimed(self):
        doc = self.bundle()
        doc["boundary_imports"] = []
        doc["unresolved_imports"] = [self.nat]
        doc["stats"]["boundary_imports"], doc["stats"]["unresolved_imports"] = 0, 1
        with self.assertRaisesRegex(ValueError, "CANDIDATE_DUPLICATE_OR_PREPARED_UNCLAIMED"):
            self.bind(doc)

    def test_duplicate_and_existing_outputs_refuse(self):
        for existing in (False, True):
            doc = self.bundle([self.unit("First"), self.unit("First")]) if not existing else self.bundle()
            if existing:
                self.parent[E.name_key(F.name("First"))] = "c"*64
            with self.subTest(existing=existing), self.assertRaisesRegex(ValueError, "CANDIDATE_EXISTING_OR_DUPLICATE_OUTPUT"):
                self.bind(doc)

    def test_forward_reference_refuses_before_native(self):
        doc = self.bundle([self.unit("Second", ("First",)), self.unit("First")])
        with self.assertRaisesRegex(ValueError, "CANDIDATE_UNBOUND_OR_FORWARD_REFERENCE"):
            self.bind(doc)

    def test_context_schema_and_targets_are_exact(self):
        for field, value, marker in (("context_root", "b"*64, "CANDIDATE_BUNDLE_CONTEXT"),
                                     ("semantic_id", "b"*64, "CANDIDATE_BUNDLE_CONTEXT"),
                                     ("foundation_id", "b"*64, "CANDIDATE_BUNDLE_CONTEXT"),
                                     ("schema", "DMKN_ORDINARY_CANDIDATE_BUNDLE_V1", "CANDIDATE_BUNDLE_CONTEXT")):
            doc = self.bundle(); doc[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, marker):
                self.bind(doc)
        with self.assertRaisesRegex(ValueError, "CANDIDATE_EXACT_TARGETS"):
            self.bind(self.bundle(), expected_targets=[F.name("NotRequested")])

    def test_claimed_counts_and_budget_fail_closed(self):
        doc = self.bundle(); doc["stats"]["unit_json_bytes"] += 1
        with self.assertRaisesRegex(ValueError, "CANDIDATE_UNIT_BYTES_OR_TARGET"):
            self.bind(doc)
        with self.assertRaisesRegex(ValueError, "CANDIDATE_AGGREGATE_UNIT_BOUND"):
            self.bind(self.bundle(), limits=B.Limits(max_total_nodes=1))
        def exhausted():
            raise ValueError("CALLER_PARENT_DEADLINE")
        with self.assertRaisesRegex(ValueError, "CALLER_PARENT_DEADLINE"):
            self.bind(self.bundle(), check_budget=exhausted)
        self.assertEqual(self.lookups.count(E.name_key(self.nat)), 2)

    def test_native_writer_order_allowed_but_duplicate_keys_refuse(self):
        import json
        doc = self.bundle()
        raw = json.dumps(doc, indent=1).encode()
        result = B.bind_candidate(raw, semantic_id=self.s, foundation_id=self.f, context_root=self.root,
            expected_targets=doc["targets"], prepared_bindings=self.prepared,
            warranted_symbol=lambda n: self.parent.get(E.name_key(n)))
        self.assertEqual(result.status, "READY")
        with self.assertRaisesRegex(ValueError, "CANDIDATE_WRITER_DUPLICATE_KEY"):
            B._writer_json(b'{"x":1,"x":2}', 100)
        for raw in (b'{"x":true}', b'{"x":-1}', b'{"x":1e2}', b'{"x":18446744073709551616}'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                B._writer_json(raw, 100)


if __name__ == "__main__":
    unittest.main()

"""One changed-boundary closure control; root selects any execution separately.

The exact pinned foundation inventory is used without replay. Synthetic inert
unit syntax and callback maps are NOT Lean mathematics or protected warrants.
No catalog, native execution, network or output writes occur in this control.
"""
from pathlib import Path
import hashlib
import json
import sys
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as PE
import portable_owner_request as R
import semantic_identity_checks as F

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
INVENTORY = ROOT / "software/assets/foundation/seed-inventory-json.json"


class SelectedClosureCheck(unittest.TestCase):
    def test_missing_theorem_omits_proof_ancestry_but_definition_keeps_body(self):
        with INVENTORY.open("rb") as stream:
            inventory_raw = stream.read(1024**2 + 1)
        self.assertLessEqual(len(inventory_raw), 1024**2)
        self.assertEqual(hashlib.sha256(inventory_raw).hexdigest(), S.INVENTORY)
        # Like prepare(), parse only after matching the exact owner-selected pin;
        # the retained Lean inventory need not use Python's canonical JSON order.
        inventory = json.loads(inventory_raw)
        semantic, foundation = S.semantic_id(), S.foundation_id()
        basis = {E.name_key(row[0]): S.basis_symbol_id(semantic, foundation, row[0])
                 for row in inventory}
        nat, truth, dep = F.name("Nat"), F.name("True"), F.name("ProofOnlyDependency")
        self.assertIn(E.name_key(nat), basis)
        self.assertIn(E.name_key(truth), basis)

        # A complete synthetic leaf provides an actual portable ExportID rather
        # than an arbitrary stand-in. Its declared type is not a proof claim.
        leaf = E.strict_json(F.evidence(semantic))
        leaf["unit"][1][1] = dep
        leaf["unit"][1][6] = [dep]
        leaf["unit"][2][0][0] = dep
        leaf["unit"][2][0][4][2] = [dep]
        leaf_raw = E.canonical_json(leaf)
        leaf_parsed = PE.read_evidence(leaf_raw)
        dep_id = S.export_id(semantic, leaf_parsed.unit_id, dep)
        type_dag = [E.EXPR_FORMAT, [], [[2, truth, []], [5, [], 0, 0, 0]], 1]
        body_dag = [E.EXPR_FORMAT, [], [[2, dep, []]], 0]

        for theorem in (True, False):
            with self.subTest(theorem=theorem):
                own = F.name("MissingTheorem" if theorem else "MissingDefinition")
                if theorem:
                    unit = [E.UNIT_FORMAT, [1, own, [], type_dag, body_dag, [own]],
                            [[own, 2, [], type_dag, [body_dag, [own]]]]]
                else:
                    unit = [E.UNIT_FORMAT, [0, own, [], type_dag, body_dag, [2, 1], [own]],
                            [[own, 1, [], type_dag, [body_dag, [2, 1], [own]]]]]
                imports = [[truth, basis[E.name_key(truth)]], [dep, dep_id]]
                imports.sort(key=lambda row: E.name_key(row[0]))
                raw = E.canonical_json({"schema": PE.SCHEMA, "semantic_id": semantic,
                                        "imports": imports, "unit": unit})
                parsed = PE.read_evidence(raw)
                own_id = S.export_id(semantic, parsed.unit_id, own)
                parent = {**basis, E.name_key(dep): dep_id, E.name_key(own): own_id}
                evidence = {E.name_key(dep): leaf_raw, E.name_key(own): raw}
                fetched, looked_up = [], []

                def warranted(name):
                    key = E.name_key(name)
                    looked_up.append(key)
                    return parent.get(key)

                def fetch(name, symbol):
                    key = E.name_key(name)
                    self.assertEqual(parent[key], symbol)
                    fetched.append(key)
                    return evidence[key]

                result = R.prepare(semantic_id=semantic, foundation_id=foundation,
                    context_root="a"*64, inventory_raw=inventory_raw, targets=[[own, own_id]],
                    warranted_symbol=warranted, fetch_evidence=fetch, owner_absent=lambda _: True)
                self.assertIn(E.name_key(dep), looked_up)  # Full claimed ID still checked.
                self.assertEqual(fetched, [E.name_key(own)] if theorem else
                                 [E.name_key(own), E.name_key(dep)])
                self.assertEqual(result.evidence_ids, (parsed.unit_id,) if theorem else
                                 (leaf_parsed.unit_id, parsed.unit_id))
                self.assertEqual(result.acquired_bytes, len(raw) if theorem else len(raw)+len(leaf_raw))
                packet = E.strict_json(result.groups[-1])
                self.assertEqual(packet[0], R.GROUP_FORMAT)
                self.assertEqual(packet[2], [] if theorem else [unit])
                self.assertEqual(packet[1][0][1], 0 if theorem else 1)
                self.assertEqual(packet[1][0][2], own_id)
                if theorem:
                    self.assertEqual(packet[1][0][3], [[], type_dag])


if __name__ == "__main__":
    unittest.main()

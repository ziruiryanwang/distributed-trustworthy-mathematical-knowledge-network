"""Pure selection controls: synthetic claims are NOT proofs or acceptance.

One identity comparison reads retained real input bytes. No native, guest,
cryptographic verifier, network, producer, or filesystem mutation is invoked.
"""
from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE))
from modules import codec as C
from admission.bindings import journal
from aggregate_claims import bindings as B, input as I
from aggregate_claims.prepare_mixed import prepare_mixed_seal
from delta_claims.claims import expected_journal
from mixed_claims import packet as P

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
CHECKS = PROJECT/"experiments/v5-local-checks"
IMAGE = "a5"*32
REAL_IMAGE = "99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60"
HELD = (
    ("selected-frontier-layout-01/evidence/wire.bin", 113849,
     "898660ddeea92cefccbf793e35b1ee49ef4867c9daec24b5344f37a1ed375500"),
    ("selected-frontier-layout-01/evidence/header.bin", 192,
     "49dd845edaec83f5b0cba5af38653f768e51ed95a4bb6ea7824c10bdd1c3169e"),
    ("module-base-production-01/finish-0/receipt.bin", 223594,
     "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"),
)


def held_bytes():
    result = []
    for relative, size, expected in HELD:
        path = CHECKS/relative
        with path.open("rb") as stream:
            raw = stream.read(size+1)
        assert len(raw) == size and hashlib.sha256(raw).hexdigest() == expected
        result.append(raw)
    return result


def spec(name):
    return {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
        "groups": [{"kind": "ordinary", "declarations": [{"kind": "theorem",
        "name": [["s", name]], "universes": 0, "type": ["sort", ["zero"]],
        "value_hash": None, "meta": {}}]}]}


def exact(name, rank=0):
    return expected_journal(C.summarize(spec(name)), rank, B.RELATION_IMAGE)


def witness(name, rank, parents):
    return {"schema": "DMKN_CERTIFIED_MODULES_V2",
        "image": journal(exact(name, rank))["image"], "rank": rank,
        "local_spec": spec(name), "rows": [], "bodies": [],
        "parents": [{"journal": list(parent), "openings": []} for parent in parents]}


def header(members, height):
    members = sorted(members)
    return (B.MAGIC+B.VERSION.to_bytes(4, "little")
        +bytes.fromhex(IMAGE+B.RELATION_IMAGE+B.FOUNDATION+B.POLICY)
        +B.commitment(members)+len(members).to_bytes(4, "little")
        +max(journal(j)["rank"] for j in members).to_bytes(8, "little")
        +height.to_bytes(8, "little"))


def claim(tag, statement, receipt=b"SYNTHETIC-NOT-A-RECEIPT"):
    return {"tag": tag, "statement": list(statement), "receipt_hex": receipt.hex()}


def frontier(index, j, member=0, siblings=()):
    return {"claim_index": index, "journal": list(j), "member_index": member,
            "siblings": [list(s) for s in siblings]}


def branch(height=7):
    a, b = exact("A"), exact("B")
    value = {"schema": P.SCHEMA, "claims": [claim(1, header([a], height)), claim(0, b)],
        "frontiers": [frontier(0, a), frontier(1, b)],
        "deltas": [witness("L", 1, [b]), witness("R", 1, [a]),
                   witness("T", 2, [exact("L", 1), exact("R", 1)])]}
    return value


class PreparationControls(unittest.TestCase):
    def prepare(self, value, target, *, envelope=None):
        return prepare_mixed_seal(C.canonical(value), target, adopted_image=IMAGE,
                                  envelope=envelope or P.Envelope())

    def test_exact_full_target_matches_existing_encoder(self):
        value = branch(); raw = C.canonical(value); target = exact("T", 2)
        claims, frontiers, witnesses, unused = P.parse_packet(raw, P.Envelope(), aggregate_image=IMAGE)
        plan = self.prepare(value, target)
        direct = I.encode(adopted_image=IMAGE, claims=[(t, s) for t, s, r in claims],
            frontiers=[(c, j, i, list(p)) for c, j, i, p in frontiers],
            witnesses=[w[0] for w in witnesses], targets=[target])
        self.assertEqual(plan.wire, direct)
        self.assertEqual(plan.selected_delta_indices, (0, 1, 2))
        self.assertEqual(plan.target_journal, target)
        self.assertEqual(plan.members, tuple(sorted([exact("A"), exact("B"),
            exact("L", 1), exact("R", 1), target])))
        B.bind_member(plan.expected_header, target, plan.target_index,
                      list(plan.target_siblings), adopted_image=IMAGE)

    def test_prune_remap_without_changing_witness_or_selected_height(self):
        value = branch(2**64-1); raw = C.canonical(value)
        parsed = P.parse_packet(raw, P.Envelope(), aggregate_image=IMAGE)
        plan = self.prepare(value, exact("L", 1))
        self.assertEqual(plan.selected_claim_indices, (1,))
        self.assertEqual(plan.selected_frontier_indices, (1,))
        self.assertEqual(plan.selected_delta_indices, (0,))
        self.assertEqual(plan.parents[0].statement, exact("B"))
        self.assertEqual(plan.wire, I.encode(adopted_image=IMAGE,
            claims=[(0, exact("B"))], frontiers=[(0, exact("B"), 0, [])],
            witnesses=[parsed[2][0][0]], targets=[exact("L", 1)]))
        self.assertEqual(plan.witnesses[0].sha256, hashlib.sha256(parsed[2][0][0]).hexdigest())
        self.assertEqual(B.decode_header(plan.expected_header, adopted_image=IMAGE)["seal_height"], 1)
        with self.assertRaises((P.DeltaError, C.StructureError)):
            self.prepare(value, exact("R", 1))

    def test_shared_A_claim_and_I_order_are_preserved(self):
        members = sorted([exact("A0"), exact("A1")]); base = exact("I")
        claims = [claim(1, header(members, 4), b"ONE-SYNTHETIC-A"), claim(0, base, b"SYNTHETIC-I")]
        value = {"schema": P.SCHEMA, "claims": claims,
            "frontiers": [frontier(0, j, i, B.opening(members, i)) for i, j in enumerate(members)]
                         +[frontier(1, base)], "deltas": [witness("All", 1, members+[base])]}
        plan = self.prepare(value, exact("All", 1))
        self.assertEqual(tuple(p.tag for p in plan.parents), (1, 0))
        self.assertEqual(tuple(p.receipt for p in plan.parents), (b"ONE-SYNTHETIC-A", b"SYNTHETIC-I"))
        self.assertEqual((plan.census.claims, plan.census.frontiers, plan.census.deltas), (2, 3, 1))
        self.assertEqual(plan.census.receipt_bytes, len(b"ONE-SYNTHETIC-A")+len(b"SYNTHETIC-I"))
        self.assertEqual(B.decode_header(plan.expected_header, adopted_image=IMAGE)["seal_height"], 5)

    def test_exact_target_not_module_alias_or_certified_frontier(self):
        value = branch()
        for target in (exact("absent"), exact("L", 2), exact("A")):
            with self.subTest(target=target.hex()):
                with self.assertRaises((P.DeltaError, C.StructureError)):
                    self.prepare(value, target)
        value["deltas"] = []
        with self.assertRaises((P.DeltaError, C.StructureError)):
            self.prepare(value, exact("A"))

    def test_invalid_omitted_descendant_is_not_salvaged(self):
        for change in (lambda v: v["deltas"][2].update(rank=3),
                       lambda v: v["deltas"][2]["parents"][0].update(journal=list(exact("absent"))),
                       lambda v: v["frontiers"][0].update(member_index=1),
                       lambda v: v["claims"][0]["statement"].__setitem__(12, 0)):
            value = branch(); change(value)
            with self.assertRaises((P.DeltaError, C.StructureError)):
                self.prepare(value, exact("L", 1))

    def test_resource_and_wire_overhead_bounds(self):
        value = branch(); target = exact("T", 2)
        for limits in (replace(P.Envelope(), packet_bytes=1),
                       replace(P.Envelope(), receipt_bytes=1),
                       replace(P.Envelope(), deltas=1), replace(P.Envelope(), edges=1)):
            with self.assertRaises((P.DeltaError, C.StructureError)):
                self.prepare(value, target, envelope=limits)
        size = len(self.prepare(value, target).wire)
        with patch.object(I, "MAX_BYTES", size):
            self.assertEqual(len(self.prepare(value, target).wire), size)
        with patch.object(I, "MAX_BYTES", size-1):
            with self.assertRaises((P.DeltaError, C.StructureError)):
                self.prepare(value, target)

    def test_plan_is_frozen_and_carries_no_authority(self):
        value = branch(); before = deepcopy(value)
        plan = self.prepare(value, exact("T", 2))
        self.assertEqual(value, before)
        self.assertEqual(plan.status, "UNTRUSTED_MIXED_SEAL_PREPARATION")
        self.assertIs(plan.mathematical_admission, False)
        self.assertIs(type(plan.parents), tuple)
        self.assertIs(type(plan.members), tuple)
        self.assertIs(type(plan.target_siblings), tuple)
        for obj, name, replacement in ((plan, "wire", b"changed"),
                (plan.parents[0], "receipt", b"changed"), (plan.census, "claims", 100)):
            with self.assertRaises(FrozenInstanceError): setattr(obj, name, replacement)
        self.assertTrue(all(p.receipt.startswith(b"SYNTHETIC") for p in plan.parents))

    def test_retained_real_FIRST_wire_header_and_witness_identity(self):
        wire, expected, receipt = held_bytes()
        base, target, first = wire[61:245], wire[441:625], wire[629:]
        self.assertEqual(hashlib.sha256(first).hexdigest(),
            "88b71b8282afc99297bf6564d22616fce6211eed9a9e18afa1cb42a41d1206e1")
        value = {"schema": P.SCHEMA, "claims": [claim(0, base, receipt)],
            "frontiers": [frontier(0, base)], "deltas": [C.parse_json(first)]}
        plan = prepare_mixed_seal(C.canonical(value), target, adopted_image=REAL_IMAGE,
                                  envelope=P.Envelope())
        self.assertEqual(plan.wire, wire)
        self.assertEqual(plan.expected_header, expected)
        self.assertEqual(plan.parents[0].receipt, receipt)
        self.assertEqual(plan.witnesses[0].bytes, len(first))
        self.assertEqual(held_bytes(), [wire, expected, receipt])


if __name__ == "__main__":
    assert Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
    held_bytes()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PreparationControls)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    held_bytes()
    imports = []
    for name, module in sorted(sys.modules.items()):
        location = getattr(module, "__file__", None)
        if location and Path(location).is_relative_to(SOURCE):
            raw = Path(location).read_bytes()
            imports.append({"name": name, "path": str(Path(location)), "bytes": len(raw),
                            "sha256": hashlib.sha256(raw).hexdigest()})
    print(json.dumps({"status": "PASS" if result.wasSuccessful() else "FAIL",
        "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "scope": "PURE_PREPARATION_SYNTHETIC_AND_RETAINED_BYTE_IDENTITY_NO_PROOF", "imports": imports}), flush=True)
    raise SystemExit(0 if result.wasSuccessful() else 1)

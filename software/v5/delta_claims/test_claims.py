"""UNRUN SYNTHETIC BOOKKEEPING CONTROLS; zero mathematical authority.

Empty rows and fabricated receipts below are NOT valid Lean/cryptographic proofs.
The exact-class object.__new__ + patched-method harness deliberately bypasses
the real verifier in tests only. No production injection seam is introduced.
These tests cannot establish native checking, receipt verification or acceptance.
"""
from copy import deepcopy
import hashlib
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from admission.bindings import journal
from admission.verifier import VerifiedModule
from modules import codec as C
from delta.packet import SCHEMA, DeltaError, Envelope, parse_packet
from delta.receiver import VerifiedDelta as FrozenVerifiedDelta
from delta_claims.claims import bind_members, expected_journal
from delta_claims.imports import DeltaImportSession
from delta_claims.receiver import DeltaVerifier, VerifiedDelta

IMAGE, FOUNDATION, POLICY, PROFILE = "12"*32, "34"*32, "56"*32, "78"*32


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def spec(name):
    return {"schema": C.SPEC_SCHEMA, "foundation": FOUNDATION, "policy": POLICY,
        "groups": [{"kind": "ordinary", "declarations": [{"kind": "theorem",
            "name": [["s", name]], "universes": 0, "type": ["sort", ["zero"]],
            "value_hash": None, "meta": {}}]}]}


def claim(module_spec, rank):
    return expected_journal(C.summarize(module_spec), rank, IMAGE)


def witness(module_spec, rank, parents=()):
    return {"schema": "DMKN_CERTIFIED_MODULES_V2", "image": journal(claim(module_spec,rank))["image"],
        "rank": rank, "local_spec": deepcopy(module_spec), "rows": [], "bodies": [],
        "parents": [{"journal": list(exact), "openings": [C.group_opening(parent_spec,0)]}
                    for exact,parent_spec in parents]}


def packet_parts(frontier_pairs, deltas):
    """Supply fake receipt bytes paired with exact J; there is no verification."""
    raw = C.canonical({"schema": SCHEMA,
        "frontiers": [{"receipt_hex": receipt.hex(), "summary": journal(exact)["summary"]}
                      for exact,receipt in frontier_pairs], "deltas": deltas})
    digest = sha(raw)
    facts = []
    for exact,receipt in frontier_pairs:
        facts.append((exact,"receipt-frontier",receipt))
    for delta in deltas:
        facts.append((claim(delta["local_spec"],delta["rank"]),"native-delta",C.canonical(delta)))
    members = [{"module": journal(exact)["module"], "summary": journal(exact)["summary"],
        "journal": exact, "profile_id": PROFILE, "packet_sha256": digest,
        "proof_form": form, "evidence_sha256": sha(payload)} for exact,form,payload in facts]
    return raw,members


def mixed():
    """Honest graph SHAPE only: M0 and M1 differ in rank, not semantics."""
    values = {name: spec(name) for name in ("H","M","C1","C2","T")}
    exact = {"H0":claim(values["H"],0), "M0":claim(values["M"],0),
        "M1":claim(values["M"],1), "C1":claim(values["C1"],1),
        "C2":claim(values["C2"],2), "T":claim(values["T"],3)}
    deltas = [witness(values["M"],1,[(exact["H0"],values["H"])]),
        witness(values["C1"],1,[(exact["M0"],values["M"])]),
        witness(values["C2"],2,[(exact["M1"],values["M"])]),
        witness(values["T"],3,[(exact["C1"],values["C1"]),(exact["C2"],values["C2"])])]
    frontiers = [(exact["H0"],b"NOT-A-RECEIPT-H"),(exact["M0"],b"NOT-A-RECEIPT-M")]
    raw,members = packet_parts(frontiers,deltas)
    return values,exact,frontiers,deltas,raw,members


def alternate_target():
    """Same target J/rank, another COMPLETE synthetic derivation, no edge union."""
    values,exact,frontiers,deltas,_,_ = mixed()
    other = witness(values["T"],3,[(exact["C2"],values["C2"])])
    return packet_parts(frontiers[:1],[deltas[0],deltas[2],other])


class SyntheticOwner:
    """TEST ONLY: deliberately fake exact-class object, never production authority."""
    def __init__(self):
        self.owner = object.__new__(DeltaVerifier)
        self.owner._deadline = time.monotonic()+3600
        self.owner._image = IMAGE
        self.owner._foundation, self.owner._policy = FOUNDATION,POLICY
        self.owner._envelope = Envelope()
        self.packets = {}
        # No constructor/runtime/checker/proof. These instance patches are test-only.
        self.owner._active = lambda: None
        self.owner.report = lambda: {"profile_id":PROFILE}
        self.owner.describe = self.describe
        self.owner.members = lambda handle: deepcopy(self.packets[handle][1])
        self.owner.export_packet = lambda handle: self.packets[handle][0]

    def register(self, raw, members):
        handle = VerifiedDelta(); self.packets[handle] = raw,deepcopy(members)
        return handle

    def describe(self, handle):
        raw,members = self.packets[handle]
        return {**deepcopy(members[-1]), "packet_sha256":sha(raw)}


class ExactWarrantControls(unittest.TestCase):
    def bind(self,raw,members):
        return bind_members(raw,members,envelope=Envelope(),image=IMAGE,
                            profile=PROFILE,packet_digest=sha(raw))

    def loaded(self, **limits):
        values,exact,frontiers,deltas,raw,members = mixed()
        fake = SyntheticOwner(); handle = fake.register(raw,members)
        session = DeltaImportSession(fake.owner,**limits)
        session.use_handle(handle)
        return session,fake,handle,values,exact,frontiers,deltas,raw,members

    def test_exact_journal_variants_preserve_semantic_identity(self):
        values,exact,_,_,_,_ = mixed()
        self.assertNotEqual(exact["M0"],exact["M1"])
        self.assertEqual(journal(exact["M0"])["module"],journal(exact["M1"])["module"])
        self.assertEqual(journal(exact["M1"])["summary"],C.summarize(values["M"]))

    def test_synthetic_binding_retains_two_exact_warrants_and_old_parents(self):
        _,exact,_,_,raw,members = mixed()
        nodes = self.bind(raw,members)
        self.assertEqual(len(nodes),6)
        self.assertEqual(nodes[exact["C1"]][3],(exact["M0"],))
        self.assertEqual(nodes[exact["C2"]][3],(exact["M1"],))
        self.assertEqual(nodes[exact["M1"]][3],(exact["H0"],))

    def test_another_same_module_variant_does_not_fill_missing_exact_ancestor(self):
        _,_,frontiers,deltas,_,_ = mixed()
        raw,members = packet_parts(frontiers[:1],deltas)
        with self.assertRaisesRegex(DeltaError,"COMPLETE_EXACT_ANCESTRY"):
            self.bind(raw,members)

    def test_binding_rejects_wrong_payload_digest_or_omitted_fact(self):
        _,_,_,_,raw,members = mixed()
        changed = deepcopy(members); changed[-1]["evidence_sha256"] = "00"*32
        for facts in (changed,members[:-1]):
            with self.assertRaises(DeltaError): self.bind(raw,facts)

    def test_same_summary_frontiers_bind_by_exact_evidence_not_first_rank(self):
        _,exact,_,deltas,_,_ = mixed()
        frontiers = [(exact["M1"],b"FAKE-RANK-ONE"),(exact["M0"],b"FAKE-RANK-ZERO")]
        raw,members = packet_parts(frontiers,deltas[1:])
        nodes = self.bind(raw,members)
        self.assertEqual(nodes[exact["M1"]][2],b"FAKE-RANK-ONE")
        self.assertEqual(nodes[exact["M0"]][2],b"FAKE-RANK-ZERO")

    def test_receiver_member_lookup_is_exact_and_not_module_first(self):
        _,exact,_,_,raw,members = mixed(); fake = SyntheticOwner()
        handle = fake.register(raw,members); module = journal(exact["M0"])["module"]
        self.assertEqual(len(fake.owner.variants(handle,module)),2)
        self.assertEqual(fake.owner.describe_member(handle,exact["M1"])["journal"],exact["M1"])
        with self.assertRaises(C.StructureError): fake.owner.describe_member(handle,module)
        with self.assertRaises(DeltaError): fake.owner.describe_member(handle,claim(spec("M"),8))

    def test_fresh_authority_classes_not_old_receipt_or_old_delta(self):
        self.assertIsNot(VerifiedDelta,FrozenVerifiedDelta)
        self.assertFalse(issubclass(VerifiedDelta,VerifiedModule))
        with self.assertRaises(DeltaError): DeltaImportSession(object())
        session,*_ = self.loaded()
        with self.assertRaises(DeltaError): session.use_handle(FrozenVerifiedDelta())

    def test_explicit_selection_required_even_for_single_candidate(self):
        session,_,_,values,exact,*_ = self.loaded()
        module = journal(exact["H0"])["module"]
        with self.assertRaises(DeltaError) as failure:
            session.open_group(module,C.group_opening(values["H"],0))
        self.assertEqual(failure.exception.status,"NEEDS_SELECTION")
        session.select_warrant(exact["H0"])
        session.open_group(module,C.group_opening(values["H"],0))

    def test_explicit_choice_is_immutable_and_unestablished_rank_refuses(self):
        session,_,_,values,exact,*_ = self.loaded()
        module = session.select_warrant(exact["M1"])
        self.assertEqual(session.select_warrant(exact["M1"]),module)
        with self.assertRaises(DeltaError) as failure: session.select_warrant(exact["M0"])
        self.assertEqual(failure.exception.status,"SELECTION_CONFLICT")
        with self.assertRaises(DeltaError): session.select_warrant(claim(values["M"],9))
        self.assertEqual(session._selected[module],exact["M1"])

    def test_semantic_opening_stored_once_but_warrants_count_separately(self):
        session,_,_,values,exact,*_ = self.loaded()
        module = session.select_warrant(exact["M1"]); opening = C.group_opening(values["M"],0)
        session.open_group(module,opening); first = session._data_bytes
        session.open_group(module,opening)
        self.assertEqual(session._data_bytes,first)
        selected = session.selected_data()
        self.assertEqual(len(selected),1); self.assertEqual(selected[0]["journal"],exact["M1"])
        count = session.census()
        self.assertEqual((count["retained_warrants"],count["unique_semantic_modules"],count["semantic_openings"]),(6,5,1))
        self.assertTrue(count["counts_are_not_useful_growth"])

    def test_duplicate_handle_submission_charges_before_deduplication(self):
        session,_,handle,_,_,_,_,raw,_ = self.loaded()
        before = session.census(); session.use_handle(handle); after = session.census()
        self.assertEqual(after["submitted_packet_bytes"],before["submitted_packet_bytes"]+len(raw))
        self.assertEqual(after["calls"],before["calls"]+1)
        self.assertEqual(after["retained_warrants"],before["retained_warrants"])

    def test_warrant_capacity_does_not_collapse_same_semantics(self):
        _,_,_,_,raw,members = mixed(); fake = SyntheticOwner()
        session = DeltaImportSession(fake.owner,max_members=5)
        with self.assertRaisesRegex(DeltaError,"WARRANT_STORAGE"):
            session.use_handle(fake.register(raw,members))
        self.assertEqual(session._nodes,{})
        self.assertEqual(session._handles,{})
        self.assertEqual(session.census()["submitted_packet_bytes"],len(raw))

    def test_rejected_submission_keeps_cost_without_partial_state_merge(self):
        values,_,_,_,raw,members = mixed(); fake = SyntheticOwner()
        handle = fake.register(raw,members)
        session = DeltaImportSession(fake.owner,packet_bytes=len(raw))
        session.use_handle(handle); before = dict(session._nodes)
        with self.assertRaisesRegex(DeltaError,"SUBMITTED_PACKET_ALLOWANCE"):
            session.use_handle(handle)
        self.assertEqual(session._nodes,before)
        self.assertEqual(session.census()["submitted_packet_bytes"],2*len(raw))
        self.assertEqual(session.census()["calls"],2)

    def test_conflicting_same_j_representation_atomic_refusal(self):
        session,fake,_,_,_,frontiers,deltas,raw,_ = self.loaded()
        before = (deepcopy(session._nodes),deepcopy(session._summaries),dict(session._handles))
        changed = deepcopy(deltas); changed[-1]["rows"] = [None] # Still not a proof.
        altered,facts = packet_parts(frontiers,changed)
        handle = fake.register(altered,facts)
        with self.assertRaises(DeltaError) as failure: session.use_handle(handle)
        self.assertEqual(failure.exception.status,"REPRESENTATION_CONFLICT")
        self.assertEqual((session._nodes,session._summaries,session._handles),before)
        self.assertEqual(session.census()["submitted_packet_bytes"],len(raw)+len(altered))

    def test_explicit_existing_choice_preserves_complete_original_record(self):
        session,fake,_,_,exact,*_ = self.loaded()
        raw,members = alternate_target(); handle = fake.register(raw,members)
        original = session._nodes[exact["T"]]
        session.use_handle(handle,resolutions={exact["T"]:"existing"})
        self.assertEqual(session._nodes[exact["T"]],original)
        self.assertEqual(session._representation_revision,0)
        # A previously stored packet still needs directives when it conflicts.
        with self.assertRaises(DeltaError): session.use_handle(handle)
        self.assertEqual(session._nodes[exact["T"]],original)

    def test_explicit_incoming_choice_selects_one_record_and_prunes_other_branch(self):
        session,fake,_,values,exact,*_ = self.loaded()
        raw,members = alternate_target()
        session.use_handle(fake.register(raw,members),resolutions={exact["T"]:"incoming"})
        self.assertEqual(session._nodes[exact["T"]][3],(exact["C2"],))
        self.assertEqual(session._representation_revision,1)
        self.assertIn(exact["C1"],session._nodes) # Stored, but not emitted if unused.
        module = session.select_warrant(exact["T"])
        session.open_group(module,C.group_opening(values["T"],0)); _,binding = session.selection()
        child = witness(spec("New"),4,[(exact["T"],values["T"])])
        onward,_ = session.onward_packet(child,binding,Envelope())
        frontiers,deltas,_ = parse_packet(onward,Envelope())
        returned = {expected_journal(item[2],item[3],IMAGE):item for item in deltas}
        self.assertNotIn(exact["C1"],returned)
        self.assertEqual(returned[exact["T"]][1],(exact["C2"],))
        self.assertEqual(returned[exact["C2"]][1],(exact["M1"],))
        self.assertEqual(len(frontiers),1)
        self.assertEqual(C.parse_json(frontiers[0][1]),journal(exact["H0"])["summary"])

    def test_missing_extra_malformed_and_arbitrary_payload_choices_are_atomic(self):
        session,fake,_,_,exact,*_ = self.loaded()
        raw,members = alternate_target(); handle = fake.register(raw,members)
        before = (deepcopy(session._nodes),deepcopy(session._summaries),dict(session._handles),
                  session._representation_revision)
        choices = ({}, {exact["T"]:"incoming",exact["M0"]:"existing"},
            {exact["T"]:"unverified"}, {exact["T"]:session._nodes[exact["T"]]},
            {"module-only":"incoming"}, [(exact["T"],"incoming")])
        for directives in choices:
            with self.assertRaises(DeltaError): session.use_handle(handle,resolutions=directives)
            self.assertEqual((session._nodes,session._summaries,session._handles,
                              session._representation_revision),before)

    def test_no_unused_choice_even_on_identical_repeated_packet(self):
        session,_,handle,_,exact,*_ = self.loaded()
        with self.assertRaisesRegex(DeltaError,"MISSING_OR_UNUSED"):
            session.use_handle(handle,resolutions={exact["T"]:"existing"})

    def test_ancestor_representation_change_invalidates_and_cannot_revive_selection(self):
        session,fake,original,values,exact,frontiers,deltas,_,_ = self.loaded()
        descendant_spec = spec("Descendant")
        descendant = witness(descendant_spec,4,[(exact["T"],values["T"])])
        descendant_raw,descendant_members = packet_parts(frontiers,deltas+[descendant])
        session.use_handle(fake.register(descendant_raw,descendant_members))
        raw,members = alternate_target(); alternate = fake.register(raw,members)
        session.use_handle(alternate,resolutions={exact["T"]:"existing"})
        # T is only an ancestor of the selected descendant, not a direct import.
        module = session.select_warrant(claim(descendant_spec,4))
        session.open_group(module,C.group_opening(descendant_spec,0)); _,binding = session.selection()
        before = deepcopy(session._nodes); packets_before = set(session._handles)
        session.use_handle(alternate,resolutions={exact["T"]:"incoming"})
        with self.assertRaisesRegex(DeltaError,"SELECTION_CHANGED"): session.require_selection(binding)
        session.use_handle(original,resolutions={exact["T"]:"incoming"})
        self.assertEqual(session._nodes,before)
        self.assertEqual(set(session._handles),packets_before)
        with self.assertRaisesRegex(DeltaError,"SELECTION_CHANGED"): session.require_selection(binding)
        self.assertEqual(session._representation_revision,2)

    def test_final_liveness_failure_does_not_commit_choice_or_new_handle(self):
        session,fake,_,_,exact,*_ = self.loaded()
        raw,members = alternate_target(); handle = fake.register(raw,members)
        before = (deepcopy(session._nodes),deepcopy(session._summaries),dict(session._handles),
                  session._representation_revision)
        actual_members = fake.owner.members; calls = 0
        def fail_final(incoming):
            nonlocal calls
            if incoming is handle:
                calls += 1
                if calls == 2: raise DeltaError("TEST_ONLY","FAKE_FINAL_LIVENESS_FAILURE")
            return actual_members(incoming)
        with patch.object(fake.owner,"members",fail_final):
            with self.assertRaisesRegex(DeltaError,"FAKE_FINAL_LIVENESS_FAILURE"):
                session.use_handle(handle,resolutions={exact["T"]:"incoming"})
        self.assertEqual((session._nodes,session._summaries,session._handles,
                          session._representation_revision),before)

    def test_fresh_acquisition_invalidates_prepared_selection(self):
        session,fake,*_ = self.loaded()
        _,binding = session.selection()
        raw,members = packet_parts([], [witness(spec("Unrelated"),0)])
        session.use_handle(fake.register(raw,members))
        with self.assertRaisesRegex(DeltaError,"SELECTION_CHANGED"):
            session.require_selection(binding)

    def test_live_inventory_change_invalidates_session(self):
        session,fake,handle,*_ = self.loaded()
        fake.packets[handle][1][0]["evidence_sha256"] = "00"*32
        with self.assertRaisesRegex(DeltaError,"INVENTORY_CHANGED"): session.selection()

    def test_onward_packet_preserves_exact_ancestor_witnesses_and_mixed_variants(self):
        session,_,_,values,exact,_,deltas,_,_ = self.loaded()
        module = session.select_warrant(exact["T"])
        session.open_group(module,C.group_opening(values["T"],0))
        _,binding = session.selection()
        child = witness(spec("New"),4,[(exact["T"],values["T"])])
        raw,_ = session.onward_packet(child,binding,Envelope())
        _,returned,_ = parse_packet(raw,Envelope())
        self.assertEqual(set(item[0] for item in returned[:-1]),set(C.canonical(item) for item in deltas))
        by_module = {C.summary_id(item[2]):item for item in returned}
        self.assertEqual(by_module[C.module_id(values["C1"])][1],(exact["M0"],))
        self.assertEqual(by_module[C.module_id(values["C2"])][1],(exact["M1"],))
        self.assertEqual(returned[-1][1],(exact["T"],))

    def test_onward_wrong_selected_parent_rank_and_same_module_refuse(self):
        session,_,_,values,exact,*_ = self.loaded()
        module = session.select_warrant(exact["M1"])
        session.open_group(module,C.group_opening(values["M"],0)); _,binding = session.selection()
        wrong_parent = witness(spec("New"),1,[(exact["M0"],values["M"])])
        wrong_rank = witness(spec("New"),1,[(exact["M1"],values["M"])])
        same_module = witness(values["M"],2,[(exact["M1"],values["M"])])
        for item in (wrong_parent,wrong_rank,same_module):
            with self.assertRaises(DeltaError): session.onward_packet(item,binding,Envelope())

    def test_duplicate_direct_semantic_parents_stay_forbidden(self):
        session,_,_,values,exact,*_ = self.loaded()
        opening = C.group_opening(values["M"],0)
        items = [{"journal":exact[key],"openings":[opening]} for key in ("M0","M1")]
        bad = witness(spec("New"),2,[(exact["M0"],values["M"]),(exact["M1"],values["M"])])
        # Test-only impossible session selection checks the final defensive rule.
        with patch.object(session,"require_selection",lambda binding:None), \
             patch.object(session,"selection",lambda:(items,"synthetic-binding")):
            with self.assertRaisesRegex(DeltaError,"SINGLE_WITNESS_DIRECT_MODULE_CONSTRAINT"):
                session.onward_packet(bad,"synthetic-binding",Envelope())


if __name__ == "__main__":
    unittest.main(verbosity=2)

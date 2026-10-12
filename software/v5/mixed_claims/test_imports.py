"""UNRUN synthetic mixed import/cut/authoring controls, not crypto or Lean tests.

Reuse frozen deliberately fake control fixtures. Native/checker/receipt/file
operations never execute; authoring foundation decoding is explicitly mocked.
"""
from copy import deepcopy
from dataclasses import FrozenInstanceError
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from modules import codec as C
from admission.bindings import journal
from admission.verifier import ReceiptVerifier
from aggregate_claims import bindings as B
from aggregate_claims.aggregate_admission import VerifiedAggregate, AggregateReceiptVerifier
from aggregate_claims.aggregate_admission_controls import fake_owner,FAKE_IMAGE
from mixed_claims.test_receiver import fake_receiver,packet_value,witness
from mixed_claims.imports import MixedImportSession
from mixed_claims import authoring as A
from mixed_claims import packet as P
from mixed_claims import receiver as R


def fake_source_pins(owner):
    """TEST ONLY: fake size/hash map; owners' real installation checks are mocked."""
    names = ("mixed_claims","mixed_claims.packet","mixed_claims.receiver","mixed_claims.imports",
        "admission","admission.verifier","admission.bindings","aggregate_claims",
        "aggregate_claims.aggregate_admission","aggregate_claims.admission_binding","aggregate_claims.bindings",
        "modules","modules.codec","delta","delta.packet","delta.receiver",
        "delta_claims","delta_claims.receiver","delta_claims.claims","production","production.producer")
    owner._pins = {ROOT/(name.replace(".","/")+("/__init__.py" if "." not in name else ".py")):
                   {"sha256":"00"*32,"bytes":1} for name in names}
    if type(owner) is AggregateReceiptVerifier: owner._member_caps = 65536,4096,64*P.MIB


def direct_session():
    aggregate,batch,header,pairs,paths = fake_owner(); fake_source_pins(aggregate)
    receipt = b"NOT-A-RECEIPT"; aggregate._handles[batch] = header,R._sha(receipt),len(receipt)
    session = MixedImportSession(aggregate_verifier=aggregate)
    members = [aggregate.select_member(batch,pair[0],index,paths[index]) for index,pair in enumerate(pairs)]
    return session,aggregate,batch,receipt,pairs,members


def accepted_delta_session():
    verifier,aggregate,supervisor = fake_receiver(); fake_source_pins(verifier); fake_source_pins(aggregate)
    value = packet_value(); raw = C.canonical(value); child_spec = value["deltas"][-1]["local_spec"]
    with patch.object(Path,"mkdir",return_value=None): handle = verifier.receive(raw,C.summarize(child_spec))
    session = MixedImportSession(aggregate_verifier=aggregate,delta_verifier=verifier)
    exact = session.use_delta_handle(handle); module = session.select_warrant(exact)
    session.open_group(module,C.group_opening(child_spec,0))
    return session,aggregate,verifier,handle,exact,child_spec,supervisor


def fabricated_seal(aggregate,journals,receipt,header=None):
    """TEST ONLY append fabricated authority; ZERO certificate production."""
    journals = sorted(journals)
    if header is None:
        header = (B.MAGIC+B.VERSION.to_bytes(4,"little")+bytes.fromhex(FAKE_IMAGE+B.RELATION_IMAGE+B.FOUNDATION+B.POLICY)
            +B.commitment(journals)+len(journals).to_bytes(4,"little")
            +max(journal(exact)["rank"] for exact in journals).to_bytes(8,"little")+(2).to_bytes(8,"little"))
    batch = VerifiedAggregate(); aggregate._handles[batch] = header,R._sha(receipt),len(receipt)
    return batch,[aggregate.select_member(batch,exact,index,B.opening(journals,index)) for index,exact in enumerate(journals)]


def new_witness(session,name="grandchild"):
    items,binding = session.selection(); exacts = [item["journal"] for item in items]
    rank = max((journal(exact)["rank"] for exact in exacts),default=-1)+1
    value = witness(name,rank,exacts)
    value["parents"] = [{"journal":list(item["journal"]),"openings":item["openings"]} for item in items]
    return value,binding


def fake_foundation(raw,pin,view):
    assert not isinstance(view._verifier,(ReceiptVerifier,AggregateReceiptVerifier,R.MixedDeltaVerifier))
    assert (view._verifier._foundation,view._verifier._policy) == (B.FOUNDATION,B.POLICY)
    return {"groups":[],"bodies":[],"values":[],"names":[]},0


class MixedImportControls(unittest.TestCase):
    def test_pure_A_import_and_context_need_no_I_or_native_owner(self):
        session,aggregate,batch,receipt,pairs,members = direct_session()
        exact = session.use_aggregate_member(members[0],receipt)
        module = session.select_warrant(exact); opened = session.open_group(module,C.group_opening(pairs[0][1],0))
        self.assertEqual(opened,pairs[0][1]["groups"][0]); self.assertIsNone(session._owners[0]); self.assertIsNone(session._owners[2])
        with patch.object(A,"_decode_foundation",fake_foundation):
            operation = A.MixedSourceOperation(session,b"TEST-ONLY-FOUNDATION","00"*32,"theorem next : True := by trivial",[[["s","next"]]])
            result = operation.prepare()
        self.assertFalse(result["mathematical_acceptance"])
        self.assertEqual(operation._origin_basis.image,B.RELATION_IMAGE)
        with self.assertRaises(FrozenInstanceError): operation._origin_basis.image = FAKE_IMAGE

    def test_shared_A_receipt_stored_once_but_each_submission_charged(self):
        session,aggregate,batch,receipt,pairs,members = direct_session()
        session.use_aggregate_member(members[0],receipt); session.use_aggregate_member(members[1],receipt)
        session.use_aggregate_member(members[0],receipt)
        report = session.census()
        self.assertEqual(report["retained_receipts"],1); self.assertEqual(report["retained_receipt_bytes"],len(receipt))
        self.assertEqual(report["submitted_bytes"],3*len(receipt)); self.assertEqual(report["retained_warrants"],2)

    def test_copied_fact_foreign_handle_and_changed_receipt_are_not_authority(self):
        session,aggregate,batch,receipt,pairs,members = direct_session()
        other,other_aggregate,other_batch,other_receipt,other_pairs,other_members = direct_session()
        for handle,raw in ((aggregate.describe_member(members[0]),receipt),(other_members[0],receipt),(members[0],b"CHANGED")):
            with self.assertRaises((P.DeltaError,C.StructureError)): session.use_aggregate_member(handle,raw)
        self.assertEqual(session._nodes,{})

    def test_same_exact_J_seal_cut_removes_ancestry_without_changing_descendant(self):
        session,aggregate,verifier,handle,exact,child_spec,supervisor = accepted_delta_session()
        value,binding = new_witness(session); before,unused = session.onward_packet(value,binding,P.Envelope())
        receipt = b"FAKE-NEW-SEAL"; batch,members = fabricated_seal(aggregate,[exact],receipt)
        session.use_aggregate_member(members[0],receipt,resolutions={exact:"incoming"})
        same_value,after_binding = new_witness(session); after,census = session.onward_packet(same_value,after_binding,P.Envelope())
        self.assertEqual(C.canonical(value),C.canonical(same_value))
        before_value,after_value = C.parse_json(before),C.parse_json(after)
        self.assertEqual((len(before_value["deltas"]),len(after_value["deltas"])),(2,1))
        self.assertEqual(after_value["deltas"][-1],before_value["deltas"][-1])
        self.assertEqual((len(before_value["frontiers"]),len(after_value["frontiers"])),(2,1))
        self.assertEqual(bytes(after_value["frontiers"][0]["journal"]),exact)
        self.assertEqual(session._representation_revision,1)
        self.assertEqual(len(supervisor.claim_calls),1) # No extra mocked receive during cut/import.

    def test_missing_or_extra_resolution_is_atomic_with_charges_retained(self):
        session,aggregate,verifier,handle,exact,child_spec,supervisor = accepted_delta_session()
        receipt = b"FAKE-CUT"; batch,members = fabricated_seal(aggregate,[exact],receipt)
        previous = dict(session._nodes); revision = session._representation_revision; charged = session._submitted_bytes
        for choices in (None,{exact:"incoming",b"x"*184:"existing"}):
            with self.assertRaisesRegex(P.DeltaError,"MISSING_OR_UNUSED_RESOLUTIONS"):
                session.use_aggregate_member(members[0],receipt,resolutions=choices)
            self.assertEqual(session._nodes,previous); self.assertEqual(session._representation_revision,revision)
        self.assertEqual(session._submitted_bytes,charged+2*len(receipt))

    def test_ancestry_change_and_reversal_leave_original_source_operation_stale(self):
        session,aggregate,verifier,handle,exact,child_spec,supervisor = accepted_delta_session()
        with patch.object(A,"_decode_foundation",fake_foundation):
            operation = A.MixedSourceOperation(session,b"TEST-FOUNDATION","00"*32,"theorem later : True := by trivial",[[["s","later"]]])
        original = operation._binding
        receipt = b"FAKE-CUT"; batch,members = fabricated_seal(aggregate,[exact],receipt)
        session.use_aggregate_member(members[0],receipt,resolutions={exact:"incoming"})
        with self.assertRaisesRegex(P.DeltaError,"SELECTION_CHANGED"): operation.prepare()
        session.use_delta_handle(handle,resolutions={exact:"incoming"})
        self.assertEqual(session._representation_revision,2)
        with self.assertRaisesRegex(P.DeltaError,"SELECTION_CHANGED"): session.require_selection(original)
        with self.assertRaisesRegex(P.DeltaError,"SELECTION_CHANGED"): operation.prepare()

    def test_same_claim_different_receipts_refuse_until_explicit_whole_J_resolution(self):
        session,aggregate,batch,receipt,pairs,members = direct_session()
        header = aggregate._handles[batch][0]; alternate = b"ANOTHER-FAKE-RECEIPT"
        other_batch,other_members = fabricated_seal(aggregate,[pair[0] for pair in pairs],alternate,header)
        for index,(member,raw) in enumerate(((members[0],receipt),(other_members[1],alternate))):
            exact = session.use_aggregate_member(member,raw); module = session.select_warrant(exact)
            session.open_group(module,C.group_opening(pairs[index][1],0))
        value,binding = new_witness(session)
        with self.assertRaisesRegex(P.DeltaError,"CLAIM_RECEIPT_REPRESENTATION_CONFLICT"):
            session.onward_packet(value,binding,P.Envelope())
        exact = pairs[1][0]
        session.use_aggregate_member(members[1],receipt,resolutions={exact:"incoming"})
        value,binding = new_witness(session); raw,census = session.onward_packet(value,binding,P.Envelope())
        self.assertEqual(len(C.parse_json(raw)["claims"]),1)

    def test_owner_close_revokes_session_and_copied_data_cannot_revive_it(self):
        session,aggregate,batch,receipt,pairs,members = direct_session()
        exact = session.use_aggregate_member(members[0],receipt); copied = dict(session._nodes)
        aggregate.close()
        with self.assertRaises((P.DeltaError,C.StructureError)): session.selection()
        self.assertTrue(session._closed); self.assertEqual(session._nodes,{})
        session._nodes.update(copied)
        with self.assertRaises(P.DeltaError): session.selection()

    def test_final_authority_recheck_failure_cannot_partially_commit(self):
        session,aggregate,batch,receipt,pairs,members = direct_session(); original = session._snapshot; calls = [0]
        def final(kind,handle,raw):
            calls[0] += 1
            if calls[0] == 2: raise C.StructureError("TEST_ONLY_FINAL_SOURCE_FAILURE")
            return original(kind,handle,raw)
        with patch.object(session,"_snapshot",final):
            with self.assertRaisesRegex(C.StructureError,"FINAL_SOURCE_FAILURE"):
                session.use_aggregate_member(members[0],receipt)
        self.assertTrue(session._closed); self.assertEqual(session._nodes,{})
        self.assertEqual(session._sources,{}); self.assertEqual(session._receipts,{})
        self.assertEqual(session._submitted_bytes,len(receipt))

    def test_A_only_session_requires_eager_source_pins_not_native_executable(self):
        aggregate,batch,header,pairs,paths = fake_owner(); fake_source_pins(aggregate)
        aggregate._pins.pop(ROOT/"delta/receiver.py")
        with self.assertRaisesRegex(P.DeltaError,"REQUIRED_SOURCE_PINS"):
            MixedImportSession(aggregate_verifier=aggregate)


if __name__ == "__main__": unittest.main(verbosity=2)

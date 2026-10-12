"""UNRUN synthetic mixed adapter controls. ZERO native/crypto/file operations.

In-memory fake supervisors and fabricated exact-class owners intentionally
bypass real verification. Empty witness rows are NOT mathematical proofs.
The frozen aggregate control fixture is reused as TEST DATA, never authority.
"""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from modules import codec as C
from admission.bindings import journal
from admission.verifier import ReceiptVerifier, VerifiedModule
from aggregate_claims import bindings as B
from aggregate_claims.aggregate_admission_controls import fake_owner,fixture,FAKE_IMAGE
from aggregate_claims.aggregate_admission import VerifiedAggregate
from delta_claims.claims import expected_journal
from delta_claims.receiver import VerifiedDelta
from mixed_claims import packet as P
from mixed_claims import receiver as R


def spec(name):
    return {"schema":C.SPEC_SCHEMA,"foundation":B.FOUNDATION,"policy":B.POLICY,
        "groups":[{"kind":"ordinary","declarations":[{"kind":"theorem","name":[["s",name]],
            "universes":0,"type":["sort",["zero"]],"value_hash":None,"meta":{}}]}]}


def witness(name,rank,parents):
    module = spec(name)
    return {"schema":"DMKN_CERTIFIED_MODULES_V2",
        "image":journal(expected_journal(C.summarize(module),rank,B.RELATION_IMAGE))["image"],
        "rank":rank,"local_spec":module,"rows":[],"bodies":[],
        "parents":[{"journal":list(exact),"openings":[]} for exact in parents]}


def packet_value():
    header,pairs,paths = fixture()
    return {"schema":P.SCHEMA,"claims":[{"tag":1,"statement":list(header),
        "receipt_hex":b"NOT-A-RECEIPT".hex()}],
        "frontiers":[{"claim_index":0,"journal":list(pair[0]),"member_index":index,
            "siblings":[list(s) for s in paths[index]]} for index,pair in enumerate(pairs)],
        "deltas":[witness("child",1,[pair[0] for pair in pairs])]}


def fake_receiver(mode="ok"):
    """TEST ONLY: no constructor, installation, process or genuine receipt."""
    aggregate,batch,header,pairs,paths = fake_owner()
    receipt = b"NOT-A-RECEIPT"
    aggregate._handles[batch] = header,R._sha(receipt),len(receipt)
    aggregate._install = ROOT/"TEST-ONLY-NONEXISTENT-INSTALL"
    owner = object.__new__(R.MixedDeltaVerifier)
    owner._owners = owner._origins = None,aggregate
    owner._profiles = None,aggregate._profile_id
    owner._image,owner._foundation,owner._policy = B.RELATION_IMAGE,B.FOUNDATION,B.POLICY
    owner._aggregate_image = FAKE_IMAGE
    owner._donor = aggregate
    owner._envelope = P.Envelope()
    owner._deadline,owner._cpu_started = time.monotonic()+120,time.process_time()
    owner._caps = 8,128*P.MIB,3600,600,3600,512*P.MIB,4096
    owner._closed = owner._busy = False
    owner._used,owner._observed_worker,owner._handles,owner._cache = [0,0,0],0.0,{},{}
    owner._profile_id = owner._origin_profile = "aa"*32
    owner._output = ROOT/"TEST-ONLY-NONEXISTENT-MIXED-OUTPUT"
    owner._native = aggregate._install/"NO-SUCH-NATIVE.exe"
    owner._check = lambda deadline=None:owner._active(deadline) # Explicit fake installation checks.

    def process():
        return {"status":"COMMAND_EXITED_ZERO_AND_CLOSED","child_exit_code":0,
            "direct_child_reaped":True,"job_closed":True,"cleanup_errors":[],
            "termination_requested":False,"wall_seconds_through_cleanup":0.5,
            "final_job":{"cpu_seconds":0.25,"active_processes":0,"terminated_processes":0}}

    class FakeSupervisor:
        def __init__(self): self.files,self.claim_calls,self.native_calls = {},[],[]
        def bounded_read(self,path,cap):
            raw = self.files[path]; assert len(raw) <= cap; return raw
        def limits_checked(self,value): return dict(value)
        def supervise(self,argv,cwd,prefix,limits,job):
            self.native_calls.append((list(argv),cwd,prefix,dict(limits),job))
            path = Path(argv[-1]); raw = self.files[path]; value = C.parse_json(raw)
            exact = expected_journal(C.summarize(value["local_spec"]),value["rank"],B.RELATION_IMAGE)
            self.files[prefix/"stdout.txt"] = C.canonical({"schema":"DMKN_NATIVE_DELTA_CONCLUSION_V1",
                "status":"CHECKED_CONDITIONAL_RELATION_NOT_ADMISSION","input_sha256":R._sha(raw),
                "input_bytes":len(raw),"journal":list(exact),
                "parents":[parent["journal"] for parent in value["parents"]],"mathematical_admission":False})
            if mode == "changed_input": self.files[path] = b"ALTERED"
            if mode == "wrong_native_statement":
                value = C.parse_json(self.files[prefix/"stdout.txt"]); value["journal"][-1] ^= 1
                self.files[prefix/"stdout.txt"] = C.canonical(value)
            if mode == "expired_after_native": aggregate._deadline = time.monotonic()-1
            report = process()
            if mode == "unclean": report["final_job"]["active_processes"] = 1
            return report

    supervisor = FakeSupervisor()
    owner._A = aggregate._supervisor = supervisor
    owner._Job = aggregate._job = object()
    def write(path,raw):
        assert path not in supervisor.files
        supervisor.files[path] = raw
        if mode == "expired_after_evidence" and path.name == "RESULT.json":
            aggregate._deadline = time.monotonic()-1
    owner._write = write
    owner._census = lambda reserve=0,entries=0:None # Deliberately no actual filesystem census.
    def receive(received,expected,operation,**limits):
        assert received == receipt and expected == header
        supervisor.claim_calls.append((received,expected,operation,limits))
        supervisor.files[operation/"process.json"] = C.canonical(process())
        return batch
    aggregate.receive = receive
    return owner,aggregate,supervisor


class MixedControls(unittest.TestCase):
    def parse(self,value,limits=None):
        return P.parse_packet(C.canonical(value),limits or P.Envelope(),aggregate_image=FAKE_IMAGE)

    def test_two_members_share_one_exact_A_claim(self):
        claims,frontiers,witnesses,census = self.parse(packet_value())
        self.assertEqual((len(claims),len(frontiers),len(witnesses)),(1,2,1))
        self.assertEqual(census["warrants"],3)
        self.assertEqual(claims[0][0],1)
        self.assertNotEqual(frontiers[0][1],frontiers[1][1])

    def test_old_wire_and_tag_impersonation_refuse(self):
        for change in (lambda value:value.update(schema="DMKN_NATIVE_DELTA_PACKET_V1"),
                       lambda value:value["claims"][0].update(tag=0),
                       lambda value:value["claims"][0].update(tag=True)):
            value = packet_value(); change(value)
            with self.assertRaises((P.DeltaError,C.StructureError)): self.parse(value)

    def test_duplicate_claim_even_different_receipt_refuses(self):
        value = packet_value(); other = deepcopy(value["claims"][0]); other["receipt_hex"] = b"DIFFERENT".hex()
        value["claims"].append(other)
        with self.assertRaisesRegex(P.DeltaError,"DUPLICATE_EXACT_CLAIM"): self.parse(value)

    def test_wrong_path_and_index_refuse(self):
        for change in (lambda value:value["frontiers"][0].update(member_index=1),
                       lambda value:value["frontiers"][0].update(siblings=[[0]*32]),
                       lambda value:value["frontiers"][0].update(journal=value["frontiers"][1]["journal"])):
            value = packet_value(); change(value)
            with self.assertRaises((P.DeltaError,C.StructureError)): self.parse(value)

    def test_graph_refusals_before_any_verifier(self):
        for change in (lambda value:value["deltas"][0].update(rank=2),
                       lambda value:value["deltas"][0].update(parents=value["deltas"][0]["parents"][:1]),
                       lambda value:value["deltas"][0]["parents"][0].update(journal=[0]*184),
                       lambda value:value["deltas"][0].update(image=[0]*8)):
            value = packet_value(); change(value)
            with self.assertRaises((P.DeltaError,C.StructureError)): self.parse(value)

    def test_caps_and_unused_claim_refuse(self):
        with self.assertRaises(P.DeltaError): self.parse(packet_value(),replace(P.Envelope(),packet_bytes=1))
        with self.assertRaises(P.DeltaError): self.parse(packet_value(),replace(P.Envelope(),frontiers=1))
        value = packet_value()
        value["claims"].append({"tag":0,"statement":value["frontiers"][0]["journal"],"receipt_hex":"ab"})
        with self.assertRaisesRegex(P.DeltaError,"UNUSED_CLAIM"): self.parse(value)

    def test_distinct_exact_ranks_of_one_semantic_module_coexist(self):
        value = packet_value(); base = spec("same")
        exact = [expected_journal(C.summarize(base),rank,B.RELATION_IMAGE) for rank in (0,1)]
        value["claims"] = [{"tag":0,"statement":list(raw),"receipt_hex":bytes([index+1]).hex()}
                            for index,raw in enumerate(exact)]
        value["frontiers"] = [{"claim_index":index,"journal":list(raw),"member_index":0,"siblings":[]}
                               for index,raw in enumerate(exact)]
        left,right = witness("L",1,[exact[0]]),witness("R",2,[exact[1]])
        children = [expected_journal(C.summarize(child["local_spec"]),child["rank"],B.RELATION_IMAGE)
                    for child in (left,right)]
        value["deltas"] = [left,right,witness("T",3,children)]
        claims,frontiers,witnesses,census = self.parse(value)
        self.assertEqual(census["warrants"],5)
        self.assertNotEqual(frontiers[0][1],frontiers[1][1])
        self.assertEqual(journal(frontiers[0][1])["module"],journal(frontiers[1][1])["module"])

    def test_I_live_binding_requires_rank_not_only_summary(self):
        owner = object.__new__(R.MixedDeltaVerifier); owner._active = lambda deadline=None:None
        legacy = object.__new__(ReceiptVerifier); owner._owners,owner._profiles = (legacy,None),("bb"*32,None)
        summary = C.summarize(spec("rank"))
        expected = expected_journal(summary,0,B.RELATION_IMAGE)
        wrong = expected_journal(summary,1,B.RELATION_IMAGE)
        legacy.describe = lambda handle:{"profile_id":"bb"*32,"receipt_sha256":"cc"*32,
            "summary":summary,"journal":wrong}
        with self.assertRaisesRegex(P.DeltaError,"EXACT_I_JOURNAL"):
            owner._claim_live(0,VerifiedModule(),"cc"*32,1,expected)

    def test_mocked_A_only_receiver_checks_native_I_and_verifies_claim_once(self):
        owner,aggregate,supervisor = fake_receiver()
        value = packet_value(); raw = C.canonical(value); summary = C.summarize(value["deltas"][-1]["local_spec"])
        with patch.object(Path,"mkdir",return_value=None):
            handle = owner.receive(raw,summary)
        self.assertIs(type(handle),R.VerifiedMixedDelta)
        self.assertFalse(isinstance(handle,(VerifiedModule,VerifiedAggregate,VerifiedDelta)))
        self.assertEqual(len(supervisor.claim_calls),1); self.assertEqual(len(supervisor.native_calls),1)
        self.assertEqual(supervisor.native_calls[0][0][1:3],["check",B.RELATION_IMAGE])
        self.assertNotEqual(supervisor.native_calls[0][0][2],FAKE_IMAGE)
        self.assertEqual(len(owner.members(handle)),3)
        self.assertEqual(owner.export_packet(handle),raw)
        self.assertEqual(owner._used,[1,len(raw),60])
        self.assertIsNone(owner._owners[0])

    def test_mocked_claim_cache_still_charges_each_packet_and_CPU_reservation(self):
        owner,aggregate,supervisor = fake_receiver(); value = packet_value()
        raw = C.canonical(value); summary = C.summarize(value["deltas"][-1]["local_spec"])
        with patch.object(Path,"mkdir",return_value=None):
            first = owner.receive(raw,summary); second = owner.receive(raw,summary)
        self.assertEqual(len(supervisor.claim_calls),1); self.assertEqual(len(supervisor.native_calls),2)
        self.assertEqual(owner._used,[2,2*len(raw),120])
        self.assertIsNot(first,second)

    def test_mocked_bad_graph_refuses_without_workers(self):
        owner,aggregate,supervisor = fake_receiver(); value = packet_value(); value["deltas"][0]["rank"] = 2
        with self.assertRaisesRegex(P.DeltaError,"EXACT_RANK"):
            owner.receive(C.canonical(value),C.summarize(value["deltas"][0]["local_spec"]))
        self.assertEqual(supervisor.claim_calls,[]); self.assertEqual(supervisor.native_calls,[])
        self.assertTrue(owner._closed)

    def test_mocked_native_and_final_origin_failures_cannot_mint(self):
        for mode in ("changed_input","wrong_native_statement","unclean","expired_after_native","expired_after_evidence"):
            with self.subTest(mode=mode):
                owner,aggregate,supervisor = fake_receiver(mode); value = packet_value(); raw = C.canonical(value)
                with patch.object(Path,"mkdir",return_value=None):
                    with self.assertRaises((P.DeltaError,C.StructureError)):
                        owner.receive(raw,C.summarize(value["deltas"][0]["local_spec"]))
                self.assertTrue(owner._closed); self.assertEqual(owner._handles,{})
                self.assertEqual(owner._cache,{}); self.assertFalse(owner._busy)
                self.assertEqual(owner._used,[1,len(raw),60])
                self.assertEqual(len(supervisor.claim_calls),1); self.assertEqual(len(supervisor.native_calls),1)


if __name__ == "__main__": unittest.main(verbosity=2)

"""Synthetic scheduler/accounting controls. NO real host, proof or admission.

All synthetic artifacts are retained below the root-selected fresh --output.
Fixture Producer construction deliberately bypasses runtime adoption so a fake
supervisor cannot be confused with qualification of the real host adapter.
"""
from copy import deepcopy
import argparse
from pathlib import Path
import struct
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from production import producer as P

OUTPUT = None


def fake_checkpoint(key, binding):
    kind, index = key.split(":"); payload = b"SYNTHETIC_NOT_A_CRYPTOGRAPHIC_PROOF"
    return (struct.pack("<I",5)+bytes.fromhex(binding)+struct.pack("<Q",len(kind))+kind.encode()
        +struct.pack("<IQ",int(index),len(payload))+payload)


class FakeSupervisor:
    def __init__(self):
        self.calls=[]; self.mode=None; self.clock=None

    def absolute(self,path,*,directory=False,fresh=False):
        p=Path(path); P.require(p.is_absolute() and p.resolve()==p,"FAKE_ABSOLUTE")
        P.require(not p.exists() if fresh else (p.is_dir() if directory else p.is_file()),"FAKE_EXISTENCE")
        return p

    def overlap(self,a,b): return a.is_relative_to(b) or b.is_relative_to(a)
    def bounded_read(self,path,limit):
        raw=Path(path).read_bytes(); P.require(0<len(raw)<=limit,"FAKE_READ_BOUND"); return raw
    def save_new(self,path,value):
        with Path(path).open("xb") as stream: stream.write(P.encoded(value))
        if self.mode=="finalization" and Path(path).name=="RESULT.json" and value.get("schema")=="DMKN_V5_PRODUCER_ATTEMPT_V1":
            self.clock[0]=1000

    def supervise(self,argv,cwd,evidence,limits,job):
        self.calls.append((list(argv),dict(limits)))
        if self.mode=="raise": raise RuntimeError("synthetic supervisor interruption")
        kind,index=argv[7],int(argv[8]); artifact=Path(argv[9]); binding="06"*32
        raw=b"SYNTHETIC_NOT_A_RECEIPT" if kind=="finish" else fake_checkpoint(P.stage_key(kind,index),binding)
        artifact.write_bytes(raw); evidence.mkdir()
        if kind=="finish":
            line=("REAL_SUCCINCT_CHECKPOINT_FINISHED image_id="+"01"*32+
                " rank=0 groups=1 receipt_bytes="+str(len(raw))+" parents=0 segments=2 binding="+binding)
        else:
            line=("REAL_PROOF_CHECKPOINT_NOT_APPLICATION_CERTIFICATE kind="+kind+" index="+str(index)+
                " checkpoint_bytes="+str(len(raw))+" segments=2 assumptions=0 binding="+binding)
        (evidence/"stdout.txt").write_text(line+"\n",encoding="ascii")
        (evidence/"stderr.txt").write_bytes(b"")
        if self.mode=="mutation":
            request=artifact.parent.parent/"request.json"; request.write_bytes(request.read_bytes()+b" ")
        if self.mode=="timeout": self.clock[0]=1000
        if self.mode=="failure":
            status,code="COMMAND_FAILED",1
        else:
            status,code="COMMAND_EXITED_ZERO_AND_CLOSED",0
        return {"status":status,"child_exit_code":code,"direct_child_reaped":True,
            "job_closed":True,"cleanup_errors":[],"termination_requested":False,
            "final_job":{"cpu_seconds":100 if self.mode=="overshoot" else 1,
                "active_processes":0,"terminated_processes":0}}


def fixture(name):
    root=OUTPUT/name; root.mkdir(); install=root/"install"; install.mkdir()
    def saved(name,raw):
        p=install/name; p.write_bytes(raw); return P.file_pin(p)
    journal=b"DMKNM002"+struct.pack("<I",2)+b"".join(bytes([i])*32 for i in range(1,6))+struct.pack("<IQ",1,0)
    host=saved("host.exe",b"SYNTHETIC_NOT_AN_EXECUTABLE")
    session={"image":saved("image.bin",b"image"),"frame":saved("frame.bin",b"frame"),
        "expected":saved("journal.bin",journal),"capsule":saved("capsule.bin",struct.pack("<I",3)+b"not_a_capsule"),
        "parents":[],"binding":"06"*32,"cycles":1<<25,"po2":18,"segments":2,"assumptions":0}
    owner=P.Producer.__new__(P.Producer)
    owner.profile={"host":host,"image_id":"01"*32,"foundation":"02"*32,"policy":"03"*32}
    owner._profile_raw=P.encoded(owner.profile); owner._pins={host["path"]:host}; owner._install=install
    owner._A=FakeSupervisor(); owner._Job=object; owner._closed=False; owner._busy=False
    owner._attempt_open=False; owner._history={}; owner._last_call_failure=None
    request={"schema":"DMKN_V5_PRODUCER_REQUEST_V1","allowance_id":"07"*32,"session":session,
        "checkpoints":[],"output_directory":str(root/"attempt-1"),"stage_limit":392,
        "budget":{"worker_cpu_seconds":20,"controller_cpu_seconds":60,"wall_seconds":60,
            "output_bytes":96*P.MIB,"output_entries":128,
            "stages":{k:{"cpu_seconds":4,"wall_seconds":20} for k in P.KINDS}},
        "prior_attempts":[],"carried_external_costs":{"worker_cpu_seconds":10,
            "controller_cpu_seconds":1,"wall_seconds":2,"scope":"SYNTHETIC_COSTS_ONLY"}}
    return owner,request,root


class ProducerControls(unittest.TestCase):
    def test_graph_and_joined_frontier(self):
        nodes=P.graph(1,2)
        self.assertEqual(nodes[-1],("finish:0",("segment:0","resolve:1")))
        self.assertEqual(dict(nodes)["resolve:0"],("lift:0",))
        available={"segment:0","segment:1","lift:0","lift:1","join:1"}
        plan=P.missing_plan(110,0,available)
        self.assertEqual(len(plan),325); self.assertEqual(plan[0][0],"segment:2")
        self.assertEqual(plan[-1][0],"finish:0")
        self.assertEqual(len(plan[-1][1]),111)
        self.assertEqual(P.missing_plan(2,0,{"segment:0","segment:1","join:1"}),
            [("finish:0",("segment:0","segment:1","join:1"))])
        for args in ((0,0),(129,0),(1,9),(True,0)):
            with self.assertRaises(ValueError): P.graph(*args)
        with self.assertRaises(ValueError): P.missing_plan(2,0,{"segment:7"})

    def test_checkpoint_envelope_is_not_crypto(self):
        raw=fake_checkpoint("segment:1","06"*32)
        P.checkpoint_header(raw[:64],len(raw),"06"*32,"segment:1")
        for binding,key,size in (("05"*32,"segment:1",len(raw)),("06"*32,"lift:1",len(raw)),("06"*32,"segment:1",len(raw)+1)):
            with self.assertRaises(ValueError): P.checkpoint_header(raw[:64],size,binding,key)

    def test_complete_synthetic_dispatch_and_no_admission(self):
        owner,request,root=fixture("complete")
        result=owner.run(request)
        self.assertEqual(result["status"],"PASS_FINISHED_RECEIPT_ARTIFACT")
        self.assertFalse(result["mathematical_admission"])
        self.assertEqual(result["worker_cpu_charge_this_attempt"],6)
        self.assertEqual([x[0][7:9] for x in owner._A.calls],
            [["segment","0"],["lift","0"],["segment","1"],["lift","1"],["join","1"],["finish","0"]])
        finish=owner._A.calls[-1][0]
        self.assertEqual(len(finish[12:]),3)
        self.assertEqual(len(result["control_documents"]),2)

    def test_resume_and_live_lineage_no_reset(self):
        owner,request,root=fixture("resume"); request["stage_limit"]=1
        first=owner.run(request)
        missing=deepcopy(request); missing["output_directory"]=str(root/"omitted")
        with self.assertRaisesRegex(ValueError,"LIVE_ALLOWANCE_HISTORY_MISSING"): owner.run(missing)
        self.assertIsNotNone(owner.report()["last_call_failure"])
        second=deepcopy(request); second["output_directory"]=str(root/"attempt-2")
        second["prior_attempts"]=[P.file_pin(root/"attempt-1"/"RESULT.json")]
        second["checkpoints"]=first["retained_checkpoints"]; second["stage_limit"]=2
        result=owner.run(second)
        self.assertEqual([x[0][7:9] for x in owner._A.calls],[["segment","0"],["lift","0"],["segment","1"]])
        self.assertEqual(result["prior_allowance_worker_charge"],1)
        self.assertEqual(result["worker_cpu_charge_this_attempt"],2)

    def test_failures_stop_and_unknown_closes(self):
        for mode in ("failure","overshoot","raise"):
            owner,request,root=fixture(mode); owner._A.mode=mode
            result=owner.run(request)
            self.assertEqual(result["status"],"FAIL"); self.assertEqual(len(owner._A.calls),1)
            self.assertFalse(result["application_receipt_created"])
            self.assertEqual(result["worker_cpu_charge_this_attempt"],100 if mode=="overshoot" else 4 if mode=="raise" else 1)
            if mode=="raise":
                self.assertFalse(result["closure_accounting_known"])
                self.assertTrue(owner.report()["closed"])

    def test_saved_request_mutation_refuses(self):
        owner,request,root=fixture("mutation"); owner._A.mode="mutation"
        result=owner.run(request)
        self.assertEqual(result["status"],"FAIL"); self.assertFalse(result["final_binding_validated"])
        self.assertEqual(len(owner._A.calls),1)

    def test_deadline_and_finalization_refuse(self):
        for mode in ("timeout","finalization"):
            owner,request,root=fixture(mode); clock=[0.0]; owner._A.mode=mode; owner._A.clock=clock
            with patch.object(P.time,"monotonic",side_effect=lambda:clock[0]):
                with self.assertRaisesRegex(ValueError,"FINALIZATION_FAILED"): owner.run(request)
            self.assertTrue((root/"attempt-1"/"FINALIZATION-FAILED.json").is_file())
            self.assertTrue(owner.report()["closed"])

    def test_pin_conflict_and_output_overlap_preflight(self):
        owner,request,root=fixture("preflight")
        pins={request["session"]["image"]["path"]:request["session"]["image"]}
        changed=deepcopy(request["session"]["image"]); changed["sha256"]="09"*32
        with self.assertRaisesRegex(ValueError,"CONFLICTING_ROLE_PIN"): owner._add_pin(pins,changed)
        request["output_directory"]=str(owner._install/"overlap")
        with self.assertRaisesRegex(ValueError,"OUTPUT_OVERLAP"): owner.run(request)
        self.assertEqual(owner._A.calls,[])
        self.assertFalse(owner.report()["last_call_failure"]["attempt_directory_created"])


def main():
    global OUTPUT
    parser=argparse.ArgumentParser(); parser.add_argument("--output",required=True); args=parser.parse_args()
    OUTPUT=Path(args.output)
    P.require(OUTPUT.is_absolute() and OUTPUT.resolve()==OUTPUT and not OUTPUT.exists(),"FRESH_TEST_OUTPUT")
    OUTPUT.mkdir()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ProducerControls)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    summary={"schema":"DMKN_V5_SYNTHETIC_PRODUCER_CONTROLS_V1","tests":result.testsRun,
        "failures":len(result.failures),"errors":len(result.errors),"host_calls":0,
        "guest_executions":0,"cryptographic_proofs":0,"mathematical_admission":False}
    with (OUTPUT/"CONTROL-RESULT.json").open("xb") as stream: stream.write(P.encoded(summary))
    return 0 if result.wasSuccessful() else 1


if __name__=="__main__":
    raise SystemExit(main())

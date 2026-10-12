"""UNRUN structural/refusal controls. No native execution or positive authority.

Synthetic journals/replies below are explicitly nonproofs. Successful pure
binding tests must never be described as mathematical admission.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from modules import codec as C
from delta.packet import Envelope, DeltaError, parse_packet, bind_native, require_closure
from delta.receiver import DeltaVerifier, VerifiedDelta
from admission.verifier import VerifiedModule
from production.producer import parse as parse_local_report


def sample():
    image, foundation, policy = "12"*32, "34"*32, "56"*32
    spec = {"schema":C.SPEC_SCHEMA,"foundation":foundation,"policy":policy,"groups":[
        {"kind":"ordinary","declarations":[{"kind":"theorem","name":[["s","test"]],
        "universes":0,"type":["sort",["zero"]],"value_hash":None,"meta":{}}]}]}
    summary = C.summarize(spec)
    raw = (b"DMKNM002"+(2).to_bytes(4,"little")+bytes.fromhex(image+foundation+policy
           +C.summary_id(summary)+summary["group_root"])+(1).to_bytes(4,"little")+(0).to_bytes(8,"little"))
    witness = {"schema":"DMKN_CERTIFIED_MODULES_V2",
        "image":[int.from_bytes(bytes.fromhex(image)[i:i+4],"little") for i in range(0,32,4)],
        "rank":0,"local_spec":spec,"rows":[],"parents":[],"bodies":[]}
    return image,foundation,policy,summary,raw,witness


class PacketControls(unittest.TestCase):
    def test_structural_parse_is_not_native_validation(self):
        *_, witness = sample()
        raw = C.canonical({"schema":"DMKN_NATIVE_DELTA_PACKET_V1","frontiers":[],"deltas":[witness]})
        frontiers,deltas,cost = parse_packet(raw,Envelope())
        self.assertEqual(frontiers,[]); self.assertEqual(len(deltas),1)
        self.assertEqual(cost["rows"],0)  # Native relation would reject this synthetic empty foundation.

    def test_aggregate_node_and_byte_limits(self):
        *_, witness = sample()
        raw = C.canonical({"schema":"DMKN_NATIVE_DELTA_PACKET_V1","frontiers":[],"deltas":[witness,witness]})
        for envelope in (replace(Envelope(),deltas=1),replace(Envelope(),packet_bytes=len(raw)-1),
                         replace(Envelope(),nodes=3)):
            with self.assertRaises(DeltaError) as error: parse_packet(raw,envelope)
            self.assertEqual(error.exception.status,"NEEDS_SEAL")

    def test_full_edge_and_row_totals(self):
        *_, parent, witness = sample()
        witness["parents"] = [{"journal":list(parent),"openings":[]}]
        witness["rows"] = [None]
        raw = C.canonical({"schema":"DMKN_NATIVE_DELTA_PACKET_V1","frontiers":[],"deltas":[witness,witness]})
        for envelope in (replace(Envelope(),edges=1),replace(Envelope(),rows=1)):
            with self.assertRaises(DeltaError) as error: parse_packet(raw,envelope)
            self.assertEqual(error.exception.status,"NEEDS_SEAL")

    def test_bad_hex_and_duplicate_record_keys(self):
        _,_,_,summary,_,witness = sample()
        for bad in ("aa ","AA","a",""):
            raw = C.canonical({"schema":"DMKN_NATIVE_DELTA_PACKET_V1",
                "frontiers":[{"receipt_hex":bad,"summary":summary}],"deltas":[witness]})
            with self.assertRaises(DeltaError): parse_packet(raw,Envelope())
        with self.assertRaises(C.StructureError): parse_packet(b'{"schema":1,"schema":2}',Envelope())

    def test_exact_native_binding_and_changes(self):
        image,foundation,policy,summary,raw,witness = sample()
        encoded = C.canonical(witness)
        reply = {"schema":"DMKN_NATIVE_DELTA_CONCLUSION_V1",
            "status":"CHECKED_CONDITIONAL_RELATION_NOT_ADMISSION",
            "input_sha256":hashlib.sha256(encoded).hexdigest(),"input_bytes":len(encoded),
            "journal":list(raw),"parents":[],"mathematical_admission":False}
        self.assertEqual(bind_native(C.canonical(reply),encoded,(),summary,0,image,foundation,policy),(raw,()))
        for key,value in (("mathematical_admission",True),("input_sha256","00"*32),
                          ("parents",[list(raw)]),("input_bytes",True)):
            changed = {**reply,key:value}
            with self.assertRaises((DeltaError,C.StructureError)):
                bind_native(C.canonical(changed),encoded,(),summary,0,image,foundation,policy)
        for bad_image,bad_rank in (("00"*32,0),(image,1)):
            with self.assertRaises(DeltaError):
                bind_native(C.canonical(reply),encoded,(),summary,bad_rank,bad_image,foundation,policy)

    def test_exact_journal_not_only_module(self):
        image,foundation,policy,summary,raw,witness = sample()
        other_rank = raw[:-8]+(1).to_bytes(8,"little")
        encoded = C.canonical(witness)
        reply = {"schema":"DMKN_NATIVE_DELTA_CONCLUSION_V1",
            "status":"CHECKED_CONDITIONAL_RELATION_NOT_ADMISSION",
            "input_sha256":hashlib.sha256(encoded).hexdigest(),"input_bytes":len(encoded),
            "journal":list(raw),"parents":[list(other_rank)],"mathematical_admission":False}
        with self.assertRaises(DeltaError):
            bind_native(C.canonical(reply),encoded,(raw,),summary,0,image,foundation,policy)

    def test_complete_closure_and_missing_material(self):
        require_closure(b"child",{b"base":(),b"child":(b"base",)})
        with self.assertRaises(DeltaError):
            require_closure(b"child",{b"base":(),b"child":(b"base",),b"extra":()})
        with self.assertRaises(DeltaError) as error:
            require_closure(b"child",{b"child":(b"base",)})
        self.assertEqual(error.exception.status,"MISSING_MATERIAL")

    def test_distinct_authority_and_no_duck_verifier(self):
        self.assertIsNot(type(VerifiedDelta()),VerifiedModule)
        self.assertFalse(issubclass(VerifiedDelta,VerifiedModule))
        with self.assertRaises(DeltaError):
            DeltaVerifier(object(),native_executable="unused",runtime_pins={},output_directory="unused")

    def test_clean_report_requires_closure_and_actual_limits(self):
        report = {"status":"COMMAND_EXITED_ZERO_AND_CLOSED","child_exit_code":0,
            "direct_child_reaped":True,"job_closed":True,"cleanup_errors":[],
            "termination_requested":False,"final_job":{"active_processes":0,
            "terminated_processes":0,"cpu_seconds":1},"wall_seconds_through_cleanup":2}
        self.assertEqual(DeltaVerifier._clean(report,3,3),1)
        fractional = {**report,"final_job":{**report["final_job"],"cpu_seconds":1.25},
                      "wall_seconds_through_cleanup":2.5}
        encoded = json.dumps(fractional).encode()
        self.assertEqual(DeltaVerifier._clean(parse_local_report(encoded),3,3),1.25)
        with self.assertRaises(C.StructureError): C.parse_json(encoded)
        for changed in ({**report,"job_closed":False},{**report,"wall_seconds_through_cleanup":4},
                        {**report,"final_job":{**report["final_job"],"cpu_seconds":4}}):
            with self.assertRaises(DeltaError): DeltaVerifier._clean(changed,3,3)
        with self.assertRaises(DeltaError) as error:
            DeltaVerifier._clean({**report,"child_exit_code":2},3,3)
        self.assertEqual(error.exception.status,"INVALID_OR_UNBOUND")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--output",required=True)
    args = parser.parse_args(); output = Path(args.output)
    output.mkdir(parents=True,exist_ok=False)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PacketControls))
    value = {"status":"PASS_STRUCTURAL_ONLY" if result.wasSuccessful() else "FAIL",
             "tests":result.testsRun,"failures":len(result.failures),"errors":len(result.errors),
             "native_calls":0,"receipt_verifications":0,"positive_authority_created":False}
    with (output/"RESULT.json").open("x",encoding="utf-8") as stream: json.dump(value,stream,sort_keys=True)
    raise SystemExit(0 if result.wasSuccessful() else 1)

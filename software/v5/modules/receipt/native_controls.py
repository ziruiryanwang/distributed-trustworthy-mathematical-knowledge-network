"""Finite cross-language wrapper controls; no Lean/prover/network campaign.

Root selects and runs a frozen snapshot under its supervisor. Native diagnostics
can validate hashes/relations but never turn synthetic journals into receipts.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from modules import codec as C


def synthetic_journal(spec, rank=0):
    summary = C.summarize(spec)
    return (b"DMKNM001" + struct.pack("<I8I",1,*([0]*8))
            + bytes.fromhex(spec["foundation"]) + bytes.fromhex(spec["policy"])
            + bytes.fromhex(C.module_id(spec)) + bytes.fromhex(summary["group_root"])
            + struct.pack("<IQ",summary["group_count"],rank) + bytes.fromhex("44"*32))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--binary",required=True);parser.add_argument("--sha256",required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    binary,out=Path(args.binary),Path(args.output)
    C.require(binary.is_absolute() and out.is_absolute() and not out.exists(),"EXPLICIT_FRESH_PATHS")
    C.require(hashlib.sha256(binary.read_bytes()).hexdigest()==args.sha256,"NATIVE_BINARY_PIN")
    out.mkdir()
    calls=[]

    expected_status={"profile":"PROFILE_DESCRIPTION_ONLY", "hash":"HASHES_COMPUTED",
                     "journal":"JOURNAL_STRUCTURE_ONLY", "openings":"OPENING_HASH_BINDINGS_ONLY"}

    def invoke(label,action,value=None,raw=None,refuses=False,reason_contains=None):
        argv=[str(binary),action]
        if value is not None or raw is not None:
            path=out/(label+".input.json")
            path.write_bytes(raw if raw is not None else C.canonical(value))
            argv.append(str(path))
        result=subprocess.run(argv,capture_output=True,timeout=20,check=False)
        (out/(label+".stdout")).write_bytes(result.stdout)
        (out/(label+".stderr")).write_bytes(result.stderr)
        answer=json.loads(result.stdout)
        C.require(answer.get("mathematical_admission") is False,"NO_MATHEMATICAL_ADMISSION")
        C.require((result.returncode==2 and answer["status"]=="REFUSED") if refuses else
                  (result.returncode==0 and answer["status"]==expected_status[action]),"EXPECTED_NATIVE_RESULT")
        if reason_contains is not None:
            C.require(refuses and reason_contains in answer.get("reason",""),"EXPECTED_REFUSAL_REASON")
        calls.append({"label":label,"exit_code":result.returncode,"status":answer["status"]})
        return answer

    profile=invoke("profile","profile")
    C.require(profile["policy"]==C.hash_value("semantic-policy",profile["semantic_descriptor"]),"POLICY_CROSS_LANGUAGE_HASH")
    C.require("certificate_verification" not in profile["semantic_descriptor"]
              and "image" not in profile["semantic_descriptor"],"SEMANTIC_POLICY_SEPARATE_FROM_RECEIVER")
    values=[None,True,False,0,2**64-1,"quote\" slash/ newline\n tab\t 中文 𝒫\u2028",["s",1],
            {"z":[],"a":{"𝒫":2,"中文":1,"a":0}},profile["semantic_descriptor"]]
    cases=[{"domain":"cross-language-control","value":value} for value in values]
    answer=invoke("canonical-hashes","hash",cases)
    C.require(answer["hashes"]==[C.hash_value(item["domain"],item["value"]) for item in cases],"HASH_PARITY")
    invoke("duplicate-key","hash",raw=b'[{"domain":"x","value":{"a":1,"a":2}}]',refuses=True,
           reason_contains="duplicate key")
    invoke("negative-number","hash",raw=b'[{"domain":"x","value":-1}]',refuses=True,
           reason_contains="negative integer forbidden")
    invoke("float-number","hash",raw=b'[{"domain":"x","value":1.0}]',refuses=True,
           reason_contains="noninteger number forbidden")
    body=["sort",["zero"]]
    groups=[{"kind":"ordinary","declarations":[{"name":[["s","d"],["n",index]],"kind":"definition",
             "universes":0,"type":["sort",["succ",["zero"]]],"value_hash":C.body_id(body,0),
             "meta":{"hint":"abbrev","safety":"safe"}}]} for index in range(3)]
    spec={"schema":C.SPEC_SCHEMA,"foundation":profile["foundation"],"policy":profile["policy"],"groups":groups}
    journal=synthetic_journal(spec)
    answer=invoke("journal-roundtrip","journal",list(journal))
    C.require(bytes(answer["roundtrip"])==journal and answer["summary"]==C.summarize(spec),"JOURNAL_PARITY")
    openings=[C.group_opening(spec,index) for index in range(3)]
    answer=invoke("merkle-openings","openings",{"journal":list(journal),"openings":openings})
    C.require(answer["indices"]==[0,1,2],"ODD_WIDTH_OPENING_PARITY")
    bad=copy.deepcopy(openings[2]);bad["siblings"][0]="00"*32
    invoke("wrong-odd-padding","openings",{"journal":list(journal),"openings":[bad]},refuses=True)
    bad=bytearray(journal);bad[108]^=1
    invoke("wrong-module-journal","journal",list(bad),refuses=True)
    invoke("old-profile-journal","journal",list(b"DMKNJ004"+journal[8:]),refuses=True)
    report={"status":"PASS_WRAPPER_CROSS_LANGUAGE_ONLY","calls":calls,"profile":profile,
            "mathematical_admission":False,"certificate_verification_performed":False}
    (out/"RESULT.json").write_bytes(C.canonical(report));print(json.dumps(report))


if __name__=="__main__":main()

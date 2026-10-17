"""One retained-mathematics aggregate capability attempt; no proof or admission.

Run only inside the separately selected bounded outer Job. Rebind the new image
slot, not the member mathematics. The host independently checks the whole wire,
actual image, expected header and genuine receipt before one guest execution.
This is not an optimization or speedup comparison and authorizes no retry.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C
from aggregate_claims import bindings as B

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT/"experiments/v5-local-checks"
HOST = HERE/"aggregate-host-build-01/aggregate_host.exe"
HOST_SHA = "b1605995c957e06b7c4529d28dfc2a49e496cefae7629b3fdddfc4a1bfb6f6d1"
WIRE = HERE/"aggregate-claims-controls-02/evidence/actual-two-delta.bin"
WIRE_SHA = "7e21d092206b08a9a71231045b8152df4179ee6575cdc5e3afc704ef03c0be58"
REFERENCE = HERE/"aggregate-claims-controls-02/evidence/actual-two-delta/stdout.txt"
REFERENCE_SHA = "01d7c9cc45a16f520980e80672f90c0a97a69e31e344f748910df5abb24ffd0b"
RECEIPT = HERE/"module-base-production-01/finish-0/receipt.bin"
RECEIPT_SHA = "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"
SYNTHETIC_A = bytes.fromhex("07000000"*8)
MIB = 1024**2


def read_pin(path, digest, maximum):
    C.require(path.is_absolute() and path.resolve(strict=True) == path
              and path.is_file(), "EXACT_ORDINARY_INPUT")
    size = path.stat().st_size
    C.require(0 < size <= maximum, "INPUT_BOUND")
    with path.open("rb") as stream: raw = stream.read(maximum+1)
    C.require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest,
              "INPUT_PIN:"+str(path))
    return raw


def pin(path, maximum):
    C.require(path.is_absolute() and path.resolve(strict=True) == path and path.is_file(),
              "EXACT_OUTPUT")
    size = path.stat().st_size
    C.require(0 < size <= maximum, "OUTPUT_BOUND")
    with path.open("rb") as stream: digest = hashlib.file_digest(stream,"sha256").hexdigest()
    C.require(path.stat().st_size == size, "OUTPUT_CHANGED")
    return {"path":str(path),"bytes":size,"sha256":digest}


def save(path, raw):
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def main():
    started = time.monotonic()
    C.require(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated
        and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize
        and len(sys.argv) == 3, "CANONICAL_ISOLATED_SELECTED_SCREEN")
    config_path,config_sha = Path(sys.argv[1]),sys.argv[2]
    C.digest_string(config_sha)
    raw_config = read_pin(config_path,config_sha,MIB)
    config = C.parse_json(raw_config)
    C.fields(config,{"schema","image_result","image_result_sha256","aggregate_image","output"})
    C.require(config["schema"] == "DMKN_AGGREGATE_COST_SCREEN_V1", "SCREEN_SCHEMA")
    image_result = Path(config["image_result"])
    C.require(image_result.is_relative_to(HERE) and image_result.name == "RESULT.json",
              "SELECTED_ASSEMBLY_RESULT")
    assembly = C.parse_json(read_pin(image_result,config["image_result_sha256"],MIB))
    image_id = config["aggregate_image"]
    B._adopted_image(image_id)
    C.require(assembly["status"] == "PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY"
        and assembly["image_id"] == image_id and assembly["assembler_calls"] == 1
        and assembly["guest_executions"] == assembly["proof_calls"] == 0
        and assembly["mathematical_admission"] is False,"ADOPTED_IMAGE_ASSEMBLY_ONLY")
    image = Path(assembly["image"]["path"])
    C.require(image.is_relative_to(HERE), "LOCAL_SELECTED_IMAGE")
    bindings = ((HOST,HOST_SHA,128*MIB),(WIRE,WIRE_SHA,MIB),
        (REFERENCE,REFERENCE_SHA,MIB),(RECEIPT,RECEIPT_SHA,MIB),
        (image_result,config["image_result_sha256"],MIB),
        (image,assembly["image"]["sha256"],64*MIB),(config_path,config_sha,MIB))

    def rebind():
        for path,digest,maximum in bindings: read_pin(path,digest,maximum)
        C.require(image.stat().st_size == assembly["image"]["bytes"],"IMAGE_BYTES")

    rebind()
    old_wire = read_pin(WIRE,WIRE_SHA,MIB)
    prior = C.parse_json(read_pin(REFERENCE,REFERENCE_SHA,MIB))
    C.require(prior["status"] == "CHECKED_CONDITIONAL_AGGREGATE_NOT_ADMISSION"
        and prior["mathematical_admission"] is False and len(prior["assumptions"]) == 1
        and prior["input_sha256"] == WIRE_SHA and prior["input_bytes"] == len(old_wire)
        and prior["edges"] == 3 and len(prior["members"]) == 3,"RETAINED_TWO_DELTA_CONCLUSION")
    old_header = bytes(prior["header"])
    B.decode_header(old_header,adopted_image=SYNTHETIC_A.hex())
    C.require(len(old_wire) == 215540 and old_wire[:12] == b"DMKNAI02\x02\x00\x00\x00"
        and old_wire[12:44] == old_header[12:44] == SYNTHETIC_A,"EXACT_REBIND_SLOT")
    actual_image = bytes.fromhex(image_id)
    wire = old_wire[:12]+actual_image+old_wire[44:]
    header = old_header[:12]+actual_image+old_header[44:]
    decoded = B.decode_header(header,adopted_image=image_id)
    C.require(decoded["member_count"] == 3 and decoded["maximum_member_rank"] == 2
        and decoded["seal_height"] == 1,"EXACT_EXPECTED_HEADER")
    for member in prior["members"]:
        B.bind_member(header,bytes(member["journal"]),member["index"],
            [bytes(x) for x in member["siblings"]],adopted_image=image_id)
    output = Path(config["output"])
    C.require(output.is_absolute() and output.resolve() == output and output.parent.is_dir()
        and output.is_relative_to(HERE) and not output.exists(),"FRESH_SCREEN_OUTPUT")
    output.mkdir()
    wire_path,header_path = output/"wire.bin",output/"header.bin"
    capsule,diagnostic = output/"aggregate.snapshot",output/"diagnostic.json"
    save(wire_path,wire); save(header_path,header)
    save(output/"configuration.json",raw_config)
    argv = [str(HOST),"snapshot",image_id,str(image),str(wire_path),str(header_path),
        str(2**26),"19","stats",str(capsule),str(diagnostic),"1",str(RECEIPT)]
    save(output/"COMMAND.json",C.canonical({"argv":argv,"timeout_seconds":120,
        "authority":"ONE_GUEST_CAPABILITY_SCREEN_NO_PROOF_OR_ADMISSION"}))
    report = {"schema":"DMKN_AGGREGATE_COST_SCREEN_RESULT_V1","status":"FAIL",
        "proof_calls":0,"mathematical_admission":False,"host_calls":0,
        "aggregate_image":image_id,"cycles":2**26,"segment_po2":19,"diagnostic_mode":"stats",
        "configuration_sha256":config_sha,"scope":"ONE_MEMO_IMAGE_CAPABILITY_ATTEMPT_NOT_OPTIMIZATION_OR_SPEEDUP"}
    try:
        rebind()
        environment = {k:v for k,v in os.environ.items() if not k.upper().startswith("RISC0_")}
        report["host_calls"] = 1
        with (output/"stdout.txt").open("xb") as stdout, (output/"stderr.txt").open("xb") as stderr:
            process = subprocess.run(argv,cwd=ROOT,env=environment,stdin=subprocess.DEVNULL,
                stdout=stdout,stderr=stderr,timeout=120,check=False,
                creationflags=subprocess.CREATE_NO_WINDOW)
        report["exit_code"] = process.returncode
        C.require((output/"stdout.txt").stat().st_size <= MIB
            and (output/"stderr.txt").stat().st_size <= MIB,"HOST_LOG_BOUND")
        if diagnostic.exists():
            report["diagnostic"] = pin(diagnostic,8*MIB)
        C.require(process.returncode == 0,"ACTUAL_AGGREGATE_EXECUTION_FAILED")
        result = C.parse_json((output/"stdout.txt").read_bytes())
        C.require(result["status"] == "UNTRUSTED_AGGREGATE_EXECUTION_CAPSULE_RETAINED"
            and result["aggregate_image"] == image_id and bytes(result["header"]) == header
            and result["capsule_path"] == str(capsule) and result["guest_execute_calls"] == 1
            and result["proof_calls"] == 0 and result["mathematical_admission"] is False
            and result["assumptions"] == 1 and 1 <= result["segments"] <= 128,"EXACT_ACTUAL_CAPSULE_RESULT")
        observed = pin(capsule,64*MIB)
        C.require(observed["bytes"] == result["capsule_bytes"]
            and observed["sha256"] == result["capsule_sha256"]
            and "diagnostic" in report,"CAPSULE_EXACT_BINDING")
        report.update(status="PASS_ONE_AGGREGATE_EXECUTION_CAPSULE_ONLY",capsule=observed,
            actual_result=result)
    except BaseException as error:
        report["error"] = type(error).__name__+": "+str(error)[:2000]
    try:
        rebind()
        C.require(wire_path.read_bytes() == wire and header_path.read_bytes() == header,"PREPARED_INPUT_CHANGED")
        entries,size = 0,0
        for parent,dirs,names in os.walk(output,followlinks=False):
            for name in dirs+names:
                path = Path(parent)/name; entries += 1
                C.require(not path.is_symlink() and not path.is_junction(),"ORDINARY_OUTPUT_TREE")
                if name in names: size += path.stat().st_size
                C.require(entries <= 160 and size <= 144*MIB,"FINAL_OUTPUT_CENSUS")
        report["output_census_before_result"] = {"entries":entries,"bytes":size}
    except BaseException as error:
        report.update(status="FAIL_FINAL_BINDING",final_error=type(error).__name__+": "+str(error)[:2000])
    report["wall_seconds_before_final_report"] = time.monotonic()-started
    save(output/"RESULT.json",C.canonical(report))
    print(json.dumps(report),flush=True)
    return 0 if report["status"] == "PASS_ONE_AGGREGATE_EXECUTION_CAPSULE_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())

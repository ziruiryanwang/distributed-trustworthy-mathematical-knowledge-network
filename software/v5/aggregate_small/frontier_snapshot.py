"""One selected BASE+FIRST layout; unchanged target/checker, no proof authority.

The old two-delta input remains immutable. This adapter selects the dependency
closure needed by FIRST, not its already retained SECOND descendant. A new H,
wire and capsule/session are required. Run only under a fresh bounded selection.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

# Import the exact sibling helper without executing aggregate_small/__init__.py
# (which imports the producer). Both files and all imported sources are pinned
# by the enclosing selected launcher. This is not a dynamic plugin interface.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import capability_snapshot02 as S
from aggregate_claims.input import encode

C, B = S.C, S.B
ROOT, HERE, MIB = S.ROOT, S.HERE, S.MIB
read_pin, pin, save, adopt_host = S.read_pin, S.pin, S.save, S.adopt_host
BASE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
FIRST = "4adbc049e4d1e29ec045d64c7dba9e27bdd506dfa6c7fb707f022be40439e742"
SECOND = "52c564f87f31082468557df6eed0a04bc7adf9d28d9614fe6cf173f5633088bf"
JOURNAL_PINS = (
    (BASE, 0, "22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682"),
    (FIRST, 1, "07734789fd165d5c29667a2925c09b882d346db97a511c75644f2cb4b8ccd0da"),
    (SECOND, 2, "6317ca94965267295974ce571adc4ca3c7515a9efed819896592b75d73c14541"),
)
FIRST_WITNESS_SHA = "88b71b8282afc99297bf6564d22616fce6211eed9a9e18afa1cb42a41d1206e1"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def derive(old_wire, reference, image_id):
    """Exact selected-byte preparation, never execution or mathematical checking."""
    prior = C.parse_json(reference)
    C.require(prior["schema"] == "DMKN_NATIVE_AGGREGATE_CONCLUSION_V1"
        and prior["status"] == "CHECKED_CONDITIONAL_AGGREGATE_NOT_ADMISSION"
        and prior["mathematical_admission"] is False and len(prior["assumptions"]) == 1
        and prior["input_sha256"] == S.WIRE_SHA and prior["input_bytes"] == len(old_wire)
        and prior["wire_bytes"] == len(old_wire) and prior["edges"] == 3
        and len(prior["members"]) == 3, "RETAINED_TWO_DELTA_CONCLUSION")
    C.require(len(old_wire) == 215540 and digest(old_wire) == S.WIRE_SHA
        and old_wire[:12] == b"DMKNAI02\x02\x00\x00\x00"
        and old_wire[12:44] == S.SYNTHETIC_A
        and [int.from_bytes(old_wire[i:i+4], "little") for i in (44,48,52,56)] == [1,1,2,1],
        "EXACT_RETAINED_WIRE_COUNTS")
    old_header = bytes(prior["header"])
    old_statement = B.decode_header(old_header, adopted_image=S.SYNTHETIC_A.hex())
    C.require(old_statement["member_count"] == 3 and old_statement["maximum_member_rank"] == 2
        and old_statement["seal_height"] == 1, "EXACT_RETAINED_HEADER")
    journals = []
    for index, (row, expected) in enumerate(zip(prior["members"], JOURNAL_PINS)):
        raw = bytes(row["journal"])
        member = B.member_journal(raw)
        C.require(len(raw) == 184 and row["index"] == index
            and (member["module"], member["rank"], digest(raw)) == expected,
            "EXACT_RETAINED_MEMBER_JOURNAL")
        B.bind_member(old_header, raw, index, [bytes(x) for x in row["siblings"]],
                      adopted_image=S.SYNTHETIC_A.hex())
        journals.append(raw)
    base, first, second = journals
    C.require(bytes(prior["assumptions"][0]["journal"]) == base
        and old_wire[60:61] == b"\x00" and old_wire[61:245] == base
        and old_wire[245:249] == bytes(4) and old_wire[249:433] == base
        and old_wire[433:441] == bytes(8) and old_wire[441:625] == second,
        "EXACT_RETAINED_CLAIM_FRONTIER_TARGET")
    first_length = int.from_bytes(old_wire[625:629], "little")
    second_offset = 629+first_length
    C.require(first_length == 113220 and second_offset == 113849
        and int.from_bytes(old_wire[second_offset:second_offset+4], "little") == 101687
        and second_offset+4+101687 == len(old_wire), "EXACT_TWO_FRAME_EXTENTS_AND_EOF")
    first_witness = old_wire[629:second_offset]
    second_witness = old_wire[second_offset+4:]
    C.require(digest(first_witness) == FIRST_WITNESS_SHA, "EXACT_UNCHANGED_FIRST_WITNESS")
    witness = C.parse_json(first_witness)
    C.require(witness["rank"] == 1 and len(witness["parents"]) == 1
        and bytes(witness["parents"][0]["journal"]) == base and len(witness["rows"]) == 1355
        and C.summary_id(C.summarize(witness["local_spec"])) == FIRST,
        "EXACT_FIRST_DEPENDENCY_CLOSURE")
    common = {"claims": [(0,base)], "frontiers": [(0,base,0,[])]}
    C.require(encode(adopted_image=S.SYNTHETIC_A.hex(), **common,
        witnesses=[first_witness,second_witness], targets=[second]) == old_wire,
        "EXACT_ORIGINAL_FRAME_RECONSTRUCTION")
    wire = encode(adopted_image=image_id, **common, witnesses=[first_witness], targets=[first])
    C.require(len(wire) == 113849 and wire[629:] == first_witness,
        "EXACT_FIRST_ONLY_WIRE")
    selected = [base,first]
    header = (B.MAGIC+B.VERSION.to_bytes(4,"little")+bytes.fromhex(image_id)
        +old_header[44:140]+B.commitment(selected)+(2).to_bytes(4,"little")
        +(1).to_bytes(8,"little")+(1).to_bytes(8,"little"))
    statement = B.decode_header(header, adopted_image=image_id)
    C.require(statement["member_count"] == 2 and statement["maximum_member_rank"] == 1
        and statement["seal_height"] == 1, "EXACT_SELECTED_HEADER")
    member_rows = []
    for index, raw in enumerate(selected):
        siblings = B.opening(selected,index)
        B.bind_member(header,raw,index,siblings,adopted_image=image_id)
        member_rows.append({"index":index,"journal":list(raw),
                            "siblings":[list(x) for x in siblings]})
    old_actual = old_header[:12]+bytes.fromhex(image_id)+old_header[44:]
    derivation = {"schema":"DMKN_FIRST_FRONTIER_SELECTION_DERIVATION_V1",
        "authority":"INERT_EXACT_INPUT_SELECTION_NOT_PROOF_OR_ADMISSION",
        "old_wire":{"bytes":len(old_wire),"sha256":digest(old_wire)},
        "old_synthetic_header":list(old_header),"previous_actual_header":list(old_actual),
        "selected_header":list(header),"selected_wire":{"bytes":len(wire),"sha256":digest(wire)},
        "selected_target":list(first),"omitted_descendant":list(second),
        "preserved_first_witness":{"bytes":len(first_witness),"sha256":digest(first_witness)},
        "omitted_second_witness":{"bytes":len(second_witness),"sha256":digest(second_witness)},
        "members":member_rows,"unchanged_parent_journal":list(base),
        "unchanged_parent_receipt_sha256":S.RECEIPT_SHA,
        "reason":"FIRST depends on BASE; SECOND is a descendant and remains downstream authoring work.",
        "completes_old_three_member_workload":False,"claims_positive_growth":False}
    return wire,header,C.canonical(derivation)


def main():
    started = time.monotonic()
    C.require(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated
        and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize
        and len(sys.argv) == 3, "CANONICAL_ISOLATED_SELECTED_SCREEN")
    config_path,config_sha = Path(sys.argv[1]),sys.argv[2]
    C.digest_string(config_sha)
    raw_config = read_pin(config_path,config_sha,MIB)
    config = C.parse_json(raw_config)
    C.fields(config,{"schema","image_result","image_result_sha256","aggregate_image","output","host_build"})
    C.require(config["schema"] == "DMKN_SMALL_AGGREGATE_COST_SCREEN_V1", "SCREEN_SCHEMA")
    host,host_pin,build_pins = adopt_host(config["host_build"])
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
    bindings = ((host,host_pin["sha256"],8*MIB),(S.WIRE,S.WIRE_SHA,MIB),
        (S.REFERENCE,S.REFERENCE_SHA,MIB),(S.RECEIPT,S.RECEIPT_SHA,MIB),
        (image_result,config["image_result_sha256"],MIB),
        (image,assembly["image"]["sha256"],64*MIB),(config_path,config_sha,MIB))

    def rebind():
        for path,sha,maximum in bindings: read_pin(path,sha,maximum)
        for item in build_pins.values(): S.read_record(item)
        C.require(pin(host,8*MIB) == host_pin, "SNAPSHOT_HOST_REBIND")
        for item in build_pins.values():
            C.require(not (Path(item["path"]).parent/"FINALIZATION-FAILED.json").exists(),
                      "BUILD_FINALIZATION_OVERRIDE")
        C.require(image.stat().st_size == assembly["image"]["bytes"],"IMAGE_BYTES")

    rebind()
    wire,header,derivation = derive(read_pin(S.WIRE,S.WIRE_SHA,MIB),
                                   read_pin(S.REFERENCE,S.REFERENCE_SHA,MIB),image_id)
    output = Path(config["output"])
    C.require(output.is_absolute() and output.resolve() == output and output.parent.is_dir()
        and output.is_relative_to(HERE) and not output.exists(),"FRESH_SCREEN_OUTPUT")
    output.mkdir()
    wire_path,header_path = output/"wire.bin",output/"header.bin"
    capsule,diagnostic = output/"aggregate.snapshot",output/"diagnostic.json"
    derivation_path = output/"selection-derivation.json"
    save(wire_path,wire); save(header_path,header); save(derivation_path,derivation)
    save(output/"configuration.json",raw_config)
    argv = [str(host),"snapshot",image_id,str(image),str(wire_path),str(header_path),
        str(2**26),"18","stats",str(capsule),str(diagnostic),"1",str(S.RECEIPT)]
    save(output/"COMMAND.json",C.canonical({"argv":argv,"timeout_seconds":120,
        "authority":"ONE_GUEST_CAPABILITY_SCREEN_NO_PROOF_OR_ADMISSION"}))
    report = {"schema":"DMKN_SMALL_AGGREGATE_COST_SCREEN_RESULT_V1","status":"FAIL",
        "proof_calls":0,"mathematical_admission":False,"host_calls":0,
        "aggregate_image":image_id,"cycles":2**26,"segment_po2":18,"diagnostic_mode":"stats",
        "host_build":config["host_build"],"configuration_sha256":config_sha,
        "scope":"ONE_FIRST_FRONTIER_CAPABILITY_ATTEMPT_NOT_OLD_THREE_MEMBER_COMPLETION_OR_SPEEDUP"}
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
        if diagnostic.exists(): report["diagnostic"] = pin(diagnostic,8*MIB)
        C.require(process.returncode == 0,"ACTUAL_AGGREGATE_EXECUTION_FAILED")
        result = C.parse_json((output/"stdout.txt").read_bytes())
        C.require(result["schema"] == "DMKN_SMALL_AGGREGATE_SNAPSHOT_RESULT_V1"
            and result["status"] == "UNTRUSTED_AGGREGATE_EXECUTION_CAPSULE_RETAINED"
            and result["aggregate_image"] == image_id and bytes(result["header"]) == header
            and result["capsule_path"] == str(capsule) and result["guest_execute_calls"] == 1
            and result["proof_calls"] == 0 and result["mathematical_admission"] is False
            and result["assumptions"] == 1 and 1 <= result["segments"] <= 256,"EXACT_ACTUAL_CAPSULE_RESULT")
        observed = pin(capsule,96*MIB)
        C.require(observed["bytes"] == result["capsule_bytes"]
            and observed["sha256"] == result["capsule_sha256"] and "diagnostic" in report,
            "CAPSULE_EXACT_BINDING")
        report.update(status="PASS_ONE_AGGREGATE_EXECUTION_CAPSULE_ONLY",capsule=observed,
                      actual_result=result)
    except BaseException as error:
        report["error"] = type(error).__name__+": "+str(error)[:2000]
    try:
        rebind()
        C.require(wire_path.read_bytes() == wire and header_path.read_bytes() == header
            and derivation_path.read_bytes() == derivation,"PREPARED_INPUT_CHANGED")
        entries,size = 0,0
        for parent,dirs,names in os.walk(output,followlinks=False):
            for name in dirs+names:
                path = Path(parent)/name; entries += 1
                C.require(not path.is_symlink() and not path.is_junction(),"ORDINARY_OUTPUT_TREE")
                if name in names: size += path.stat().st_size
                C.require(entries+1 <= 288 and size+MIB <= 208*MIB,"FINAL_OUTPUT_CENSUS")
        report["output_census_before_result"] = {"entries":entries,"bytes":size}
    except BaseException as error:
        report.update(status="FAIL_FINAL_BINDING",final_error=type(error).__name__+": "+str(error)[:2000])
    report["wall_seconds_before_final_report"] = time.monotonic()-started
    final_raw = C.canonical(report)
    C.require(len(final_raw) <= MIB, "FINAL_REPORT_RESERVE")
    save(output/"RESULT.json",final_raw)
    print(json.dumps(report),flush=True)
    return 0 if report["status"] == "PASS_ONE_AGGREGATE_EXECUTION_CAPSULE_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())

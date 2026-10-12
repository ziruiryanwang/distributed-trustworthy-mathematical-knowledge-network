"""Selected native controls and cross-language vectors, NEVER A-receipt authority.

Four remaining workers: one corrected syntax group, retained mathematics with
v2 framing, wrong exact target and invalid proof. Prior 15 Python and 15 Rust
successes are carried as retained evidence, not rerun. No proof, receipt or guest.
"""
from pathlib import Path
import hashlib
import importlib.util
import math
import os
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from aggregate_claims import bindings as B
from aggregate_claims.input import encode, from_legacy_packet
from aggregate_claims.binding_controls import run as binding_checks
from delta.packet import parse_packet
from modules import codec as C
from production.producer import (MIB, encoded, parse, fields, require, pin_fields, file_pin)

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
BASE = ROOT/"product-local/v4-library-commons-02/commons-v4"
MANIFEST_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
PACKET_SHA = "54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1"
TARGET = "52c564f87f31082468557df6eed0a04bc7adf9d28d9614fe6cf173f5633088bf"
SYNTHETIC_A = "07000000"*8
SCHEMA = "DMKN_V5_AGGREGATE_CLAIMS_REMAINING_CONTROLS_V1"
PRIOR = ROOT/"experiments/v5-local-checks/aggregate-claims-controls-01/evidence/RESULT.json"
PRIOR_SHA = "3ca0555fc9c9f6f71061457051768f949d3bf4f114e57f65f1127ab3e3f5f651"
REFERENCE = ROOT/"experiments/v5-local-checks/aggregate-native-controls-02/evidence/cross-language-vectors.json"
REFERENCE_SHA = "877f8d8b92d9b54c28ac7ab18949c22e302880d8a0dcec9781620a0a71347364"


def sha(raw): return hashlib.sha256(raw).hexdigest()


def read_pin(pin, maximum=128*MIB):
    path = pin_fields(pin, maximum)
    require(path.resolve() == path and file_pin(path) == pin, "CONTROL_PIN")
    with path.open("rb") as stream: raw = stream.read(maximum+1)
    require(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"], "CONTROL_READ_PIN")
    return raw


def save(path, value):
    raw = encoded(value); require(len(raw) <= 4*MIB, "CONTROL_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def json_census(values):
    count, depth = 0, 0
    pending = [(value,0) for value in values]
    while pending:
        value, level = pending.pop(); count += 1; depth = max(depth,level)
        if type(value) is dict: pending.extend((v,level+1) for v in value.values())
        elif type(value) is list: pending.extend((v,level+1) for v in value)
    return count, depth


def run(config_path, config_sha):
    started, cpu_started = time.monotonic(), time.process_time()
    require(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
        and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
        "CONTROL_ISOLATED_OWNER")
    path = Path(config_path); C.digest_string(config_sha)
    require(path.is_absolute() and path.resolve() == path and path.is_relative_to(ROOT/"experiments")
        and 0 < path.stat().st_size <= MIB, "CONTROL_CONFIGURATION_PATH")
    raw_config = path.read_bytes(); require(sha(raw_config) == config_sha, "CONTROL_CONFIGURATION_PIN")
    config = parse(raw_config)
    fields(config, ("schema","packet","native","tests","runtime_pins","output_directory"))
    require(config["schema"] == SCHEMA, "CONTROL_SCHEMA")
    packet_raw = read_pin(config["packet"], 16*MIB)
    require(len(packet_raw) == 662480 and sha(packet_raw) == PACKET_SHA, "CONTROL_RETAINED_TWO_DELTA_FIXTURE")
    read_pin(config["native"]); read_pin(config["tests"])
    require(0 < REFERENCE.stat().st_size <= MIB, "REFERENCE_BOUND")
    reference_raw = REFERENCE.read_bytes(); require(sha(reference_raw) == REFERENCE_SHA, "EXACT_RETAINED_REFERENCE")
    reference = C.parse_json(reference_raw)
    require(0 < PRIOR.stat().st_size <= MIB, "PRIOR_EVIDENCE_BOUND")
    prior_raw = PRIOR.read_bytes(); require(sha(prior_raw) == PRIOR_SHA, "PRIOR_EVIDENCE_PIN")
    prior = parse(prior_raw)
    require(prior["status"] == "FAIL" and len(prior["commands"]) == 1
        and prior["commands"][0]["child_exit_code"] == 101
        and prior["checks"][0]["status"] == "PASS" and len(prior["checks"][0]["checks"]) == 15,
        "PRIOR_FAILED_OPERATION_RETAINED_NOT_RELABELED")
    target_matches = [bytes(row["journal"]) for row in reference["members"]
                      if B.member_journal(bytes(row["journal"]))["module"] == TARGET]
    require(len(target_matches) == 1 and B.member_journal(target_matches[0])["rank"] == 2,
            "EXACT_RETAINED_TARGET_WARRANT")
    target_journal = target_matches[0]
    require(type(config["runtime_pins"]) is list and 1 <= len(config["runtime_pins"]) <= 128,
        "CONTROL_RUNTIME_LIST")
    runtime = {}
    for pin in config["runtime_pins"]:
        runtime_path = pin_fields(pin)
        require(str(runtime_path) not in runtime, "CONTROL_UNIQUE_RUNTIME")
        read_pin(pin); runtime[str(runtime_path)] = pin
    for required in (Path(__file__).resolve(),Path(sys.executable).resolve(),
        Path(sys.executable).resolve().parent/"python314.dll",Path(config["native"]["path"]),Path(config["tests"]["path"])):
        require(str(required) in runtime and file_pin(required) == runtime[str(required)], "CONTROL_REQUIRED_RUNTIME")
    # Source module paths actually loaded by this isolated control must be pinned.
    for name in ("aggregate_claims", "aggregate_claims.bindings", "aggregate_claims.input",
                 "aggregate_claims.binding_controls", "aggregate_claims.admission_binding",
                 "admission", "admission.bindings", "admission.verifier", "delta", "delta.packet",
                 "delta.receiver", "modules", "modules.codec", "production", "production.producer"):
        actual = Path(sys.modules[name].__file__).resolve()
        require(str(actual) in runtime and file_pin(actual) == runtime[str(actual)], "CONTROL_LOADED_SOURCE_PIN:"+name)
    manifest = BASE/"RELEASE-MANIFEST.json"
    manifest_raw = manifest.read_bytes(); require(sha(manifest_raw) == MANIFEST_SHA, "CONTROL_SUPERVISOR_MANIFEST")
    manifest_files = parse(manifest_raw)["files"]
    loaded = {}

    def load(name, relative):
        source = BASE/relative; raw = source.read_bytes()
        require({"bytes":len(raw),"sha256":sha(raw)} == manifest_files[relative], "CONTROL_SUPERVISOR_SOURCE")
        require(name not in sys.modules, "CONTROL_MODULE_COLLISION")
        spec = importlib.util.spec_from_file_location(name,source)
        module = importlib.util.module_from_spec(spec); sys.modules[name] = module
        exec(compile(raw,str(source),"exec"),module.__dict__)
        loaded[source] = raw
        return module

    A = load("_aggregate_native_supervisor","operator/commons.py")
    load("domains","receiver/helpers/domains.py")
    J = load("_aggregate_native_job","receiver/helpers/run_stage.py")
    packet = C.parse_json(packet_raw)
    first, second = packet["deltas"]
    require(len(packet["frontiers"]) == 1 and len(first["parents"]) == 1
        and len(second["parents"]) == 2 and first["rank"] == 1 and second["rank"] == 2
        and C.summary_id(C.summarize(second["local_spec"])) == TARGET, "CONTROL_ACTUAL_GRAPH")
    base_journal = bytes(first["parents"][0]["journal"])
    wire, pending_claims, packet_census = from_legacy_packet(packet_raw,[base_journal],
        adopted_image=SYNTHETIC_A,targets=[target_journal])
    require(len(pending_claims) == 1 and pending_claims[0][1] == base_journal
        and sha(pending_claims[0][0]) == "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47",
        "CONTROL_EXACT_PENDING_LEGACY_MATERIAL_NOT_VERIFICATION")
    output = Path(config["output_directory"])
    require(output.is_absolute() and output.resolve() == output and output.parent.is_dir()
        and output.is_relative_to(ROOT/"experiments/v5-local-checks") and not output.exists(), "CONTROL_FRESH_OUTPUT")
    protected = [path,manifest.parent,Path(__file__).resolve().parents[1],Path(config["packet"]["path"])]
    protected.extend(Path(name) for name in runtime)
    require(all(not output.is_relative_to(p) and not p.is_relative_to(output) for p in protected), "CONTROL_OUTPUT_OVERLAP")
    output.mkdir(); save(output/"configuration.json",config)
    result = {"schema":SCHEMA,"status":"FAIL","configuration_sha256":config_sha,
        "synthetic_A":SYNTHETIC_A,"mathematical_admission":False,"proof_calls":0,"guest_calls":0,
        "receipt_calls":0,"author_calls":0,"network_calls":0,"commands":[],"checks":[],
        "authority":"LOCAL_NATIVE_CONDITIONAL_EVIDENCE_NOT_AGGREGATE_RECEIPT"}
    deadline = started+600

    def remaining():
        left = math.floor(deadline-time.monotonic())
        require(left > 0 and time.process_time()-cpu_started <= 60, "CONTROL_TOTAL_ENVELOPE")
        return left

    def output_census():
        count = size = 0
        for path in output.rglob("*"):
            count += 1
            require(count <= 128 and not path.is_symlink(), "CONTROL_OUTPUT_ENTRY_BOUND")
            if path.is_file(): size += path.stat().st_size
            require(size <= 64*MIB, "CONTROL_OUTPUT_BYTE_BOUND")
        return {"bytes":size,"entries":count}

    def call(name, argv, expected_code):
        require(len(result["commands"]) < 4, "CONTROL_FOUR_WORKERS_MAX")
        limits = {"cpu_seconds":30,"wall_seconds":min(60,remaining()),"memory_mib":3072,
            "active_processes":2,"stdout_bytes":MIB,"stderr_bytes":MIB}
        process = A.supervise(argv,ROOT,output/name,limits,J.Job)
        result["commands"].append(process); save(output/(name+"-process.json"),process)
        output_census(); remaining()
        require(process["child_exit_code"] == expected_code and process["direct_child_reaped"] is True
            and process["job_closed"] is True and process["cleanup_errors"] == []
            and process["termination_requested"] is False and process["final_job"]["active_processes"] == 0
            and process["final_job"]["terminated_processes"] == 0
            and process["final_job"]["cpu_seconds"] <= 30
            and process["wall_seconds_through_cleanup"] <= limits["wall_seconds"]
            and all(process["observed_logs"][k] <= limits[k] for k in ("stdout_bytes","stderr_bytes")),
            "CONTROL_CLEAN_EXPECTED_EXIT:"+name)
        require(process["status"] == ("COMMAND_EXITED_ZERO_AND_CLOSED" if expected_code == 0 else "COMMAND_FAILED"),
            "CONTROL_PROCESS_STATUS:"+name)
        return (output/name/"stdout.txt").read_bytes()

    generated_inputs = {}

    def native(name, raw, expected_reason=None):
        request = output/(name+".bin")
        with request.open("xb") as stream: stream.write(raw)
        generated_inputs[request] = raw
        raw_reply = call(name,[config["native"]["path"],"check",str(request)],0 if expected_reason is None else 2)
        reply = C.parse_json(raw_reply,C.Limits(max_bytes=MIB))
        if expected_reason is not None:
            C.fields(reply,{"status","reason","mathematical_admission"})
            require(reply == {"status":"REFUSED","reason":expected_reason,"mathematical_admission":False},
                "CONTROL_EXACT_REFUSAL:"+name)
            result["checks"].append({"name":name,"input_sha256":sha(raw),"reason":expected_reason})
        return reply

    try:
        result["carried_evidence"] = {"prior_result_sha256":PRIOR_SHA,"prior_status":"FAIL",
            "inert_python_groups_retained":15,"rust_groups_retained":15,"prior_tests_rerun":0}
        tests = call("unit-controls",[config["tests"]["path"],"--test-threads=1"],0).decode("utf-8")
        require("test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out;" in tests
            and "test corrected_named_positional_extraction_then_schema_refusals ... ok" in tests,
            "CONTROL_ONE_CORRECTED_GROUP_ONLY")
        result["checks"].append({"name":"one_corrected_syntax_differential_group","status":"PASS"})
        reply = native("actual-two-delta",wire)
        C.fields(reply,{"schema","status","mathematical_admission","input_sha256","input_bytes","wire_bytes",
            "header","assumptions","members","edges","census"})
        require(reply["schema"] == "DMKN_NATIVE_AGGREGATE_CONCLUSION_V1"
            and reply["status"] == "CHECKED_CONDITIONAL_AGGREGATE_NOT_ADMISSION"
            and reply["mathematical_admission"] is False and reply["input_sha256"] == sha(wire)
            and reply["input_bytes"] == reply["wire_bytes"] == len(wire) and reply["edges"] == 3,
            "CONTROL_NATIVE_BOUND_CONCLUSION")
        claims = [{"image":B.member_journal(base_journal)["image"],"journal":list(base_journal)}]
        require(reply["assumptions"] == claims, "CONTROL_EXACT_PENDING_CLAIM")
        require(type(reply["members"]) is list and len(reply["members"]) == 3, "CONTROL_THREE_MEMBERS")
        members = [bytes(row["journal"]) for row in reply["members"]]
        expected = {B.member_journal(base_journal)["module"]:(B.member_journal(base_journal)["summary"],0)}
        expected.update({C.summary_id(C.summarize(v["local_spec"])):(C.summarize(v["local_spec"]),v["rank"])
            for v in (first,second)})
        require(len(expected) == 3, "CONTROL_UNIQUE_EXPECTED_MODULES")
        for raw in members:
            j = B.member_journal(raw); require((j["summary"],j["rank"]) == expected[j["module"]], "CONTROL_ACTUAL_MEMBER")
        require(base_journal in members and all(bytes(p["journal"]) in members for p in second["parents"]),
            "CONTROL_EXACT_IMPORTED_JOURNALS")
        require(set(members) == {bytes(row["journal"]) for row in reference["members"]}
            and reply["census"] == reference["census"] and reply["assumptions"] == reference["assumptions"]
            and reply["edges"] == reference["edges"], "UNCHANGED_RETAINED_MATHEMATICS_AND_CENSUS")
        header = bytes(reply["header"])
        expected_header = (B.MAGIC+B.VERSION.to_bytes(4,"little")+bytes.fromhex(SYNTHETIC_A)
            +bytes.fromhex(B.RELATION_IMAGE)+bytes.fromhex(B.FOUNDATION)+bytes.fromhex(B.POLICY)
            +B.commitment(members)+(3).to_bytes(4,"little")+(2).to_bytes(8,"little")+(1).to_bytes(8,"little"))
        require(header == expected_header, "CONTROL_INDEPENDENT_PYTHON_HEADER_ROOT")
        for index,row in enumerate(reply["members"]):
            C.fields(row,{"index","journal","siblings"})
            siblings = [bytes(value) for value in row["siblings"]]
            require(row["index"] == index and siblings == B.opening(members,index), "CONTROL_CROSS_LANGUAGE_PATH")
            B.bind_member(header,members[index],index,siblings,adopted_image=SYNTHETIC_A)
        nodes, depth = json_census([first,second])
        require(reply["census"] == {"rows":packet_census["rows"],"bodies":packet_census["bodies"],
            "openings":packet_census["openings"],"parent_edges":3,"nodes":nodes,"maximum_depth":depth},
            "CONTROL_INDEPENDENT_JSON_CENSUS")
        save(output/"cross-language-vectors.json",reply)
        result["checks"].append({"name":"actual_conditional_two_delta_and_all_python_vectors","status":"PASS"})
        common = {"adopted_image":SYNTHETIC_A,"claims":[(0,base_journal)],
            "frontiers":[(0,base_journal,0,[])],"targets":[target_journal]}
        wrong_target = target_journal[:176]+(3).to_bytes(8,"little")
        native("wrong-exact-target",encode(**dict(common, targets=[wrong_target]),
            witnesses=[C.canonical(first),C.canonical(second)]),
            "aggregate target must be an exact newly checked delta warrant")
        changed = C.parse_json(C.canonical(first))
        require(changed["rows"][-1]["thm"]["value"] == 1200 and changed["rows"][-1]["thm"]["type"] == 770,
            "CONTROL_EXACT_INVALID_PROOF_CHANGE")
        changed["rows"][-1]["thm"]["value"] = 770
        native("invalid-proof",encode(**common,witnesses=[C.canonical(changed),C.canonical(second)]),
            "CHECKER_PANIC_OR_UNRESOLVED_DEMAND")
        require(len(result["commands"]) == 4, "CONTROL_COMPLETE_WORKER_COUNT")
        result["status"] = "PASS_REMAINING_EXACT_WARRANT_NATIVE_BOUNDARIES"
    except BaseException as error:
        result["error"] = {"type":type(error).__name__,"message":str(error)[:4000]}
    finally:
        try:
            remaining(); require(path.read_bytes() == raw_config, "CONTROL_CONFIGURATION_CHANGED")
            require(read_pin(config["packet"],16*MIB) == packet_raw, "CONTROL_PACKET_CHANGED")
            for pin in runtime.values(): read_pin(pin)
            require(REFERENCE.read_bytes() == reference_raw, "RETAINED_REFERENCE_CHANGED")
            require(PRIOR.read_bytes() == prior_raw, "PRIOR_EVIDENCE_CHANGED")
            for source,raw in generated_inputs.items(): require(source.read_bytes() == raw, "GENERATED_INPUT_CHANGED")
            require((output/"configuration.json").read_bytes() == encoded(config), "SAVED_CONFIGURATION_CHANGED")
            require(manifest.read_bytes() == manifest_raw, "CONTROL_MANIFEST_CHANGED")
            for source,raw in loaded.items(): require(source.read_bytes() == raw, "CONTROL_SUPERVISOR_CHANGED")
            result["output_census_before_result"] = output_census()
        except BaseException as error: result.update(status="FAIL_FINAL_BINDING",final_error=str(error)[:3000])
        result.update(owner_cpu_seconds=time.process_time()-cpu_started,wall_seconds=time.monotonic()-started,
            accounting="FOUR_WORKERS_AT_MOST_120CPU_RESERVED;OWNER_CPU_DISJOINT;OUTER_JOB_INCLUSIVE_DO_NOT_ADD_TWICE")
        save(output/"RESULT.json",result)
        try:
            remaining(); output_census()
        except BaseException as error:
            result.update(status="FAIL_FINALIZATION",finalization_error=str(error)[:3000])
            save(output/"FINALIZATION-FAILED.json",{"status":"FAIL_FINALIZATION",
                "overrides_result":True,"result_sha256":sha((output/"RESULT.json").read_bytes()),
                "error":str(error)[:3000]})
    return result


if __name__ == "__main__":
    require(len(sys.argv) == 3,"CONFIG_AND_SHA_REQUIRED")
    result = run(sys.argv[1],sys.argv[2])
    print(encoded({key:result.get(key) for key in ("status","error")}).decode(),end="")
    raise SystemExit(0 if result["status"].startswith("PASS_") else 1)

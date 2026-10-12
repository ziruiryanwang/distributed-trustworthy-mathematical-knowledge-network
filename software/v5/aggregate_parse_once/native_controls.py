"""Five new unit cases and two new native calls against frozen expected bytes.

No old binary/suite, Lean authoring, receipt verification, guest, proof or network.
Only stdlib and the exact retained supervisor are loaded; no v5 eager imports.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = ROOT/"software/v5/aggregate_parse_once"
BASE = ROOT/"product-local/v4-library-commons-02/commons-v4"
MANIFEST_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
FIXTURE_ROOT = ROOT/"experiments/v5-local-checks/aggregate-native-controls-02/evidence"
FIXTURES = {
    "actual-two-delta.bin":"cec1e5fc3e211bd367a9171c2a398e2a1218e627f96d28848d60c9366746c808",
    "cross-language-vectors.json":"877f8d8b92d9b54c28ac7ab18949c22e302880d8a0dcec9781620a0a71347364",
    "invalid-proof.bin":"112bf21c3d0ad44bbf6af9263ba5371810a9f284c2861f7db866e739f75417bc",
    "invalid-proof/stdout.txt":"42d71010ea316cdbce83b22f2ce5ef77ced0dda6a980802091de6bb15134205d",
}
MIB = 1024**2
SCHEMA = "DMKN_V5_AGGREGATE_PARSE_ONCE_CONTROLS_V1"


def need(value, reason):
    if not value: raise ValueError(reason)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def parse(raw):
    def pairs(values):
        result = {}
        for key,value in values:
            need(key not in result,"DUPLICATE_JSON_KEY"); result[key] = value
        return result
    def constant(_): raise ValueError("NONFINITE_JSON_NUMBER")
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=constant)


def encode(value): return (json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def save(path, value):
    raw = encode(value); need(len(raw) <= 4*MIB,"REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def pin_path(pin):
    need(type(pin) is dict and set(pin) == {"path","bytes","sha256"}
        and type(pin["path"]) is str and type(pin["bytes"]) is int
        and 0 <= pin["bytes"] <= 128*MIB and type(pin["sha256"]) is str
        and re.fullmatch(r"[0-9a-f]{64}",pin["sha256"]),"PIN_FIELDS")
    path = Path(pin["path"])
    need(path.is_absolute() and path.resolve() == path,"CANONICAL_PIN_PATH")
    return path


def read_pin(pin):
    path = pin_path(pin)
    need(path.stat().st_size == pin["bytes"],"PIN_SIZE:"+str(path))
    with path.open("rb") as stream: raw = stream.read(pin["bytes"]+1)
    need(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"],"PIN_BYTES:"+str(path))
    return raw


def run(config_path, config_sha):
    started,cpu_started = time.monotonic(),time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT
        and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
        and not sys.flags.optimize,"ISOLATED_CANONICAL_OWNER")
    path = Path(config_path)
    need(type(config_sha) is str and re.fullmatch(r"[0-9a-f]{64}",config_sha)
        and path.is_absolute() and path.resolve() == path and path.is_relative_to(ROOT/"experiments")
        and 0 < path.stat().st_size <= MIB,"EXACT_CONFIGURATION_PATH")
    raw_config = path.read_bytes(); need(sha(raw_config) == config_sha,"CONFIGURATION_PIN")
    config = parse(raw_config)
    need(type(config) is dict and set(config) == {"schema","native","tests","runtime_pins","output_directory"}
        and config["schema"] == SCHEMA,"CONFIGURATION_FIELDS")
    read_pin(config["native"]); read_pin(config["tests"])
    need(type(config["runtime_pins"]) is list and 1 <= len(config["runtime_pins"]) <= 128,"RUNTIME_LIST")
    runtime = {}
    for pin in config["runtime_pins"]:
        actual = pin_path(pin); key = os.path.normcase(str(actual))
        need(key not in runtime,"UNIQUE_RUNTIME"); read_pin(pin); runtime[key] = pin
    for required in (Path(__file__).resolve(),Path(sys.executable).resolve(),
        Path(sys.executable).resolve().parent/"python314.dll",pin_path(config["native"]),pin_path(config["tests"])):
        key = os.path.normcase(str(required)); need(key in runtime,"REQUIRED_RUNTIME:"+str(required))
        read_pin(runtime[key])
    for field in ("native","tests"):
        need(config[field] == runtime[os.path.normcase(str(pin_path(config[field])))],"CONSISTENT_BINARY_PIN")
    fixture_bytes = {}
    for relative,digest in FIXTURES.items():
        source = FIXTURE_ROOT/relative
        need(0 < source.stat().st_size <= 16*MIB,"FIXTURE_SIZE")
        with source.open("rb") as stream: raw = stream.read(16*MIB+1)
        need(0 < len(raw) <= 16*MIB and sha(raw) == digest,"FIXTURE_PIN:"+relative)
        fixture_bytes[relative] = raw
    expected_positive = parse(fixture_bytes["cross-language-vectors.json"])
    need(expected_positive["status"] == "CHECKED_CONDITIONAL_AGGREGATE_NOT_ADMISSION"
        and expected_positive["mathematical_admission"] is False
        and expected_positive["input_sha256"] == FIXTURES["actual-two-delta.bin"],"EXACT_CONDITIONAL_REFERENCE")
    need(parse(fixture_bytes["invalid-proof/stdout.txt"]) == {"status":"REFUSED",
        "reason":"CHECKER_PANIC_OR_UNRESOLVED_DEMAND","mathematical_admission":False},"EXACT_NEGATIVE_REFERENCE")
    manifest = BASE/"RELEASE-MANIFEST.json"
    manifest_raw = manifest.read_bytes(); need(sha(manifest_raw) == MANIFEST_SHA,"SUPERVISOR_MANIFEST")
    manifest_files = parse(manifest_raw)["files"]; loaded = {}

    def load(name, relative):
        source = BASE/relative; raw = source.read_bytes()
        need({"bytes":len(raw),"sha256":sha(raw)} == manifest_files[relative],"SUPERVISOR_SOURCE")
        need(name not in sys.modules,"MODULE_COLLISION")
        spec = importlib.util.spec_from_file_location(name,source)
        module = importlib.util.module_from_spec(spec); sys.modules[name] = module
        exec(compile(raw,str(source),"exec"),module.__dict__); loaded[source] = raw
        return module

    A = load("_parse_once_native_supervisor","operator/commons.py")
    load("domains","receiver/helpers/domains.py")
    J = load("_parse_once_native_job","receiver/helpers/run_stage.py")
    output = Path(config["output_directory"])
    need(output.is_absolute() and output.resolve() == output and output.parent.is_dir()
        and output.is_relative_to(ROOT/"experiments/v5-local-checks") and not output.exists(),"FRESH_OUTPUT")
    protected = [path,BASE,SOURCE,FIXTURE_ROOT,*[pin_path(pin) for pin in runtime.values()]]
    need(all(not output.is_relative_to(p) and not p.is_relative_to(output) for p in protected),"OUTPUT_OVERLAP")
    output.mkdir(); save(output/"configuration.json",config)
    result = {"schema":SCHEMA,"status":"FAIL","configuration_sha256":config_sha,
        "mathematical_admission":False,"guest_calls":0,"proof_calls":0,"receipt_calls":0,
        "author_calls":0,"network_calls":0,"old_binary_calls":0,"commands":[],"checks":[],
        "fixture_pins":FIXTURES,"authority":"REPRESENTATION_DIFFERENTIAL_NOT_AGGREGATE_RECEIPT"}
    deadline = started+600
    generated_inputs = {}

    def remaining():
        left = math.floor(deadline-time.monotonic())
        need(left > 0 and time.process_time()-cpu_started <= 60,"TOTAL_ENVELOPE")
        return left

    def output_census():
        count = size = 0
        for entry in output.rglob("*"):
            count += 1
            need(count <= 128 and not entry.is_symlink(),"OUTPUT_ENTRY_BOUND")
            if entry.is_file(): size += entry.stat().st_size
            need(size <= 64*MIB,"OUTPUT_BYTE_BOUND")
        return {"bytes":size,"entries":count}

    def call(name, argv, expected_code):
        need(len(result["commands"]) < 3,"THREE_WORKERS_MAX")
        limits = {"cpu_seconds":30,"wall_seconds":min(60,remaining()),"memory_mib":3072,
            "active_processes":2,"stdout_bytes":MIB,"stderr_bytes":MIB}
        process = A.supervise(argv,ROOT,output/name,limits,J.Job)
        result["commands"].append(process); save(output/(name+"-process.json"),process)
        output_census(); remaining()
        need(process["child_exit_code"] == expected_code and process["direct_child_reaped"] is True
            and process["job_closed"] is True and process["cleanup_errors"] == []
            and process["termination_requested"] is False and process["final_job"]["active_processes"] == 0
            and process["final_job"]["terminated_processes"] == 0 and process["final_job"]["cpu_seconds"] <= 30
            and process["wall_seconds_through_cleanup"] <= limits["wall_seconds"]
            and all(process["observed_logs"][k] <= limits[k] for k in ("stdout_bytes","stderr_bytes")),
            "CLEAN_EXPECTED_EXIT:"+name)
        need(process["status"] == ("COMMAND_EXITED_ZERO_AND_CLOSED" if expected_code == 0 else "COMMAND_FAILED"),
            "PROCESS_STATUS:"+name)
        return (output/name/"stdout.txt").read_bytes()

    try:
        tests = call("changed-unit-controls",[config["tests"]["path"],"parse_once_controls::","--test-threads=1"],0).decode("utf-8")
        need("test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 9 filtered out;" in tests,
            "FIVE_NEW_GROUPS_AND_NO_OLD_GROUPS")
        expected_cases = ("named_positional_and_noncanonical_spellings_return_exact_value",
            "strict_parse_refusals_preserve_unmodified_initial_census",
            "shape_and_depth_failures_preserve_partial_census_state",
            "cumulative_caps_overflow_and_success_then_refusal_match",
            "public_value_entry_preserves_early_relation_refusals_and_census")
        for case in expected_cases:
            need("test parse_once_controls::"+case+" ... ok" in tests,"EXACT_NEW_UNIT_CASE:"+case)
        result["checks"].append({"name":"five_new_changed_boundary_units","status":"PASS"})
        for name,input_name,expected_name,exit_code in (
            ("actual-two-delta","actual-two-delta.bin","cross-language-vectors.json",0),
            ("invalid-proof","invalid-proof.bin","invalid-proof/stdout.txt",2)):
            raw = fixture_bytes[input_name]; request = output/(name+".bin")
            with request.open("xb") as stream: stream.write(raw)
            generated_inputs[request] = raw
            reply = call(name,[config["native"]["path"],"check",str(request)],exit_code)
            need(request.read_bytes() == raw,"GENERATED_INPUT_CHANGED:"+name)
            need(reply == fixture_bytes[expected_name],"EXACT_RETAINED_REPLY_BYTES:"+name)
            result["checks"].append({"name":name,"status":"PASS","input_sha256":sha(raw),
                "output_sha256":sha(reply),"matches_frozen_reference":True})
        need(len(result["commands"]) == 3,"EXACT_WORKER_COUNT")
        result["status"] = "PASS_PARSE_ONCE_NATIVE_DIFFERENTIAL"
    except BaseException as error: result["error"] = {"type":type(error).__name__,"message":str(error)[:4000]}
    finally:
        try:
            remaining(); need(path.read_bytes() == raw_config,"CONFIGURATION_CHANGED")
            for pin in runtime.values(): read_pin(pin)
            for relative,raw in fixture_bytes.items(): need((FIXTURE_ROOT/relative).read_bytes() == raw,"FIXTURE_CHANGED")
            for source,raw in generated_inputs.items(): need(source.read_bytes() == raw,"GENERATED_INPUT_CHANGED")
            need(manifest.read_bytes() == manifest_raw,"MANIFEST_CHANGED")
            for source,raw in loaded.items(): need(source.read_bytes() == raw,"SUPERVISOR_CHANGED")
            need((output/"configuration.json").read_bytes() == encode(config),"SAVED_CONFIG_CHANGED")
            result["output_census_before_result"] = output_census()
        except BaseException as error: result.update(status="FAIL_FINAL_BINDING",final_error=str(error)[:3000])
        result.update(owner_cpu_seconds=time.process_time()-cpu_started,wall_seconds=time.monotonic()-started,
            accounting="THREE_WORKERS_AT_MOST_90CPU_RESERVED;OWNER_CPU_DISJOINT;OUTER_JOB_INCLUSIVE_DO_NOT_ADD_TWICE")
        save(output/"RESULT.json",result)
        try: remaining(); output_census()
        except BaseException as error:
            result.update(status="FAIL_FINALIZATION",finalization_error=str(error)[:3000])
            save(output/"FINALIZATION-FAILED.json",{"status":"FAIL_FINALIZATION","overrides_result":True,
                "result_sha256":sha((output/"RESULT.json").read_bytes()),"error":str(error)[:3000]})
    return result


if __name__ == "__main__":
    need(len(sys.argv) == 3,"CONFIG_AND_SHA_REQUIRED")
    result = run(sys.argv[1],sys.argv[2]); print(encode({key:result.get(key) for key in ("status","error")}).decode(),end="")
    raise SystemExit(0 if result["status"] == "PASS_PARSE_ONCE_NATIVE_DIFFERENTIAL" else 1)

"""Ten selected finish-only native manifest refusals; no guest or prover call.

Inputs are the completed BASE+FIRST po18 layout, not a synthetic capsule. The
finish branch cannot construct the prover even on unexpected parser acceptance.
Every failed control stops this finite operation; no retries or cap relaxation.
"""
from pathlib import Path
import importlib.util
import os
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from production import producer as P

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT/"experiments/v5-local-checks"
MIB = P.MIB
SCHEMA = "DMKN_SMALL_NATIVE_MANIFEST_CONTROLS_V1"
A_IMAGE = "99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60"
HOST_SHA = "8f8e444ddd9029906fee60a073a701bdd34c8b095d54f81f2554bfe1e91ad8ee"
CAPSULE_SHA = "6e41621e2595c252328eaf5f34862c6d6f913caecb68117406bcd616a61b44a5"
SESSION_BINDING = "9c87448ba08ae98273ac6fc1df8a41a22716db8be686ce473eb5fba874a1475d"
CAPSULE_BINDING = "e56cb33f432a4c5bbdb0624eb2a072db48562e26c77fc20cefd0da8831585a2b"
INPUT_NAMES = ("host","image","wire","expected","capsule","parent",
               "layout_result","layout_outer","layout_command")
SUPERVISOR_SOURCES = (("_small_manifest_supervisor","operator/commons.py"),
    ("domains","receiver/helpers/domains.py"),("_small_manifest_job","receiver/helpers/run_stage.py"))
ORACLES = (
    ("M1",("exact dependency manifest bytes/hash",)),
    ("M2",("duplicate field `schema`",)),
    ("M3",("invalid type: sequence","a JSON object with exact named fields")),
    ("M4",("invalid type: boolean `true`","expected u64")),
    ("M5",("manifest exact schema/session/capsule/stage",)),
    ("M6",("exact ordered dependency keys",)),
    ("M7",("exact dependency file bytes/hash",)),
    ("M8",("exact dependency count",)),
    ("M9",("dependency row bound",)),
    ("M10",("aggregate checkpoint magic/version",)),
)


def read_pin(pin, maximum=128*MIB):
    path = P.pin_fields(pin,maximum)
    P.require(path.resolve(strict=True) == path and P.file_pin(path) == pin, "EXACT_CONTROL_INPUT_PIN")
    with path.open("rb") as stream: raw = stream.read(maximum+1)
    P.require(len(raw) == pin["bytes"] and P.hash_bytes(raw) == pin["sha256"], "EXACT_CONTROL_INPUT_READ")
    return raw


def save(path, raw):
    P.require(type(raw) is bytes and len(raw) <= MIB, "CONTROL_FILE_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def flipped(value):
    P.digest(value)
    return ("0" if value[0] != "0" else "1")+value[1:]


def manifests(base):
    """Each malformed record is isolated; normal extents/hashes are recomputed."""
    ordinary = P.encoded(base)
    cases = []
    for name,_ in ORACLES:
        value = P.parse(ordinary)
        if name == "M3":
            item = value["dependencies"][0]["file"]
            value["dependencies"][0]["file"] = [item["path"],item["bytes"],item["sha256"]]
        elif name == "M4": value["dependencies"][0]["file"]["bytes"] = True
        elif name == "M5": value["capsule_binding"] = flipped(value["capsule_binding"])
        elif name == "M6": value["dependencies"].reverse()
        elif name == "M7":
            item = value["dependencies"][0]["file"]
            item["sha256"] = flipped(item["sha256"])
        elif name in ("M8","M9"):
            value["dependencies"] = [{"key":"lift:0","file":dict(base["dependencies"][0]["file"])}
                                     for _ in range(257 if name == "M8" else 258)]
        raw = P.encoded(value)
        if name == "M2":
            raw = b'{"schema":"DMKN_AGGREGATE_DEPENDENCIES_V1",'+raw[1:]
        P.require(0 < len(raw) <= 256*1024, "MANIFEST_FIXTURE_BYTE_BOUND")
        actual_sha = P.hash_bytes(raw)
        cases.append((name,raw,flipped(actual_sha) if name == "M1" else actual_sha))
    return cases


def main():
    started,cpu_started = time.monotonic(),time.process_time()
    P.require(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
        and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize
        and len(sys.argv) == 3,"CANONICAL_ISOLATED_CONTROL_OWNER")
    config_path = Path(sys.argv[1]); P.digest(sys.argv[2])
    P.require(config_path.is_relative_to(HERE),"LOCAL_SELECTED_CONFIGURATION")
    configuration_pin = {"path":str(config_path),"bytes":config_path.stat().st_size,"sha256":sys.argv[2]}
    raw_config = read_pin(configuration_pin,MIB)
    config = P.parse(raw_config)
    P.fields(config,("schema","inputs","supervisor_manifest","runtime_pins",
                     "case_limits","total_limits","output_directory"))
    P.require(config["schema"] == SCHEMA,"CONTROL_CONFIGURATION_SCHEMA")
    inputs = config["inputs"]; P.fields(inputs,INPUT_NAMES)
    held = {}

    def add(pin, maximum=128*MIB):
        path = P.pin_fields(pin,maximum)
        P.require(str(path) not in held or held[str(path)] == pin,"CONFLICTING_CONTROL_PIN")
        P.require(path.resolve(strict=True) == path and P.file_pin(path) == pin,"CONTROL_SELECTED_FILE")
        held[str(path)] = dict(pin)
        return path

    add(configuration_pin,MIB)
    for name,item in inputs.items(): add(item)
    P.require(inputs["host"]["bytes"] == 68036608 and inputs["host"]["sha256"] == HOST_SHA
        and inputs["capsule"]["bytes"] == 32965324 and inputs["capsule"]["sha256"] == CAPSULE_SHA,
        "ACTUAL_ADOPTED_HOST_AND_COMPLETE_CAPSULE")
    manifest_path = add(config["supervisor_manifest"],8*MIB)
    release = P.parse(read_pin(config["supervisor_manifest"],8*MIB))
    P.require(type(release.get("files")) is dict,"SUPERVISOR_RELEASE_MAP")
    runtime = config["runtime_pins"]
    P.require(type(runtime) is list and 1 <= len(runtime) <= 128,"FINITE_CONTROL_RUNTIME")
    runtime_paths = set()
    for item in runtime:
        path = add(item)
        P.require(str(path) not in runtime_paths,"UNIQUE_RUNTIME_PIN")
        runtime_paths.add(str(path))
    for source in (Path(__file__).resolve(),Path(P.__file__).resolve(),
                   Path(sys.modules["production"].__file__).resolve(),
                   Path(sys.executable).resolve(),Path(sys.executable).resolve().parent/"python314.dll",
                   Path(inputs["host"]["path"])):
        P.require(str(source) in runtime_paths,"ACTUAL_LOADED_RUNTIME_PIN:"+str(source))
    loaded = {}
    for name,relative in SUPERVISOR_SOURCES:
        item = release["files"].get(relative); P.fields(item,("bytes","sha256"))
        source = manifest_path.parent/relative
        source_pin = {"path":str(source),**item}
        add(source_pin,4*MIB)
        P.require(str(source) in runtime_paths and name not in sys.modules,"SUPERVISOR_SOURCE_OR_COLLISION")
        raw = read_pin(source_pin,4*MIB)
        spec = importlib.util.spec_from_file_location(name,source)
        module = importlib.util.module_from_spec(spec); sys.modules[name] = module
        exec(compile(raw,str(source),"exec"),module.__dict__)
        loaded[name] = module
    supervisor,job = loaded["_small_manifest_supervisor"],loaded["_small_manifest_job"].Job
    for path in held: supervisor.absolute(path)
    P.require(sum(item["bytes"] for item in held.values()) <= 256*MIB,"TOTAL_PINNED_INPUT_ENVELOPE")
    limits = supervisor.limits_checked(config["case_limits"])
    ceilings = {"cpu_seconds":15,"wall_seconds":20,"memory_mib":1024,"active_processes":1,
                "stdout_bytes":64*1024,"stderr_bytes":64*1024}
    P.require(all(limits[name] <= maximum for name,maximum in ceilings.items()),"NATIVE_CASE_CEILINGS")
    total = config["total_limits"]
    total_ceilings = {"worker_cpu_seconds":150,"controller_cpu_seconds":30,"wall_seconds":240,
                      "output_bytes":16*MIB,"output_entries":128}
    P.fields(total,total_ceilings)
    for name,maximum in total_ceilings.items(): P.uint(total[name],maximum,1)
    P.require(total["output_bytes"] >= 3*MIB and total["output_entries"] >= 80,"REPORT_AND_CASE_RESERVES")

    layout = P.parse(read_pin(inputs["layout_result"],MIB))
    outer = P.parse(read_pin(inputs["layout_outer"],MIB))
    command = P.parse(read_pin(inputs["layout_command"],MIB))
    P.require(layout["schema"] == "DMKN_SMALL_AGGREGATE_COST_SCREEN_RESULT_V1"
        and layout["status"] == "PASS_ONE_AGGREGATE_EXECUTION_CAPSULE_ONLY"
        and layout["exit_code"] == 0 and layout["capsule"] == inputs["capsule"]
        and layout["cycles"] == 2**26 and layout["segment_po2"] == 18
        and layout["host_calls"] == 1 and layout["proof_calls"] == 0
        and layout["mathematical_admission"] is False and P.clean(outer["result"]),
        "ADOPTED_CLEAN_COMPLETE_LAYOUT")
    actual = layout["actual_result"]
    expected = read_pin(inputs["expected"],192)
    P.require(actual["aggregate_image"] == A_IMAGE and bytes(actual["header"]) == expected
        and actual["segments"] == 167 and actual["assumptions"] == 1
        and actual["session_binding"] == SESSION_BINDING and actual["capsule_binding"] == CAPSULE_BINDING
        and actual["capsule_path"] == inputs["capsule"]["path"]
        and actual["capsule_sha256"] == CAPSULE_SHA and actual["capsule_bytes"] == 32965324
        and actual["guest_execute_calls"] == 1 and actual["proof_calls"] == 0,
        "ACTUAL_SELECTED_167_ONE_PARENT_BINDING")
    P.require(expected[:12] == b"DMKNA002\x02\0\0\0" and len(expected) == 192
        and expected[12:44].hex() == A_IMAGE and int.from_bytes(expected[172:176],"little") == 2
        and int.from_bytes(expected[176:184],"little") == 1
        and int.from_bytes(expected[184:192],"little") == 1,"SELECTED_TWO_MEMBER_H")
    argv = command["argv"]
    P.require(type(argv) is list and len(argv) == 13
        and argv[1:8] == ["snapshot",A_IMAGE,inputs["image"]["path"],inputs["wire"]["path"],
                         inputs["expected"]["path"],str(2**26),"18"]
        and argv[8] == "stats" and argv[9] == inputs["capsule"]["path"]
        and argv[11:] == ["1",inputs["parent"]["path"]],"ACTUAL_LAYOUT_INPUT_ORDER")

    output = supervisor.absolute(config["output_directory"],fresh=True)
    P.require(output.is_relative_to(HERE) and output.parent.is_dir()
        and all(not supervisor.overlap(output,Path(path)) for path in held),"FRESH_NONOVERLAPPING_CONTROL_OUTPUT")
    output.mkdir()
    save(output/"configuration.json",raw_config)
    generated = {}

    def generated_file(path,raw):
        save(path,raw); item = P.file_pin(path); generated[str(path)] = item
        return item

    invalid = generated_file(output/"invalid-checkpoint.bin",bytes(72))
    P.require(len(invalid["path"].encode("utf-16-le"))//2 <= 512,"NATIVE_FIXTURE_PATH_BOUND")
    base = {"schema":"DMKN_AGGREGATE_DEPENDENCIES_V1","session_binding":SESSION_BINDING,
        "capsule_binding":CAPSULE_BINDING,"stage":"finish:0",
        "dependencies":[{"key":"segment:"+str(i),"file":dict(invalid)} for i in range(167)]
                       +[{"key":"resolve:0","file":dict(invalid)}]}
    cases = []
    for (name,raw,supplied_sha),(_,oracle) in zip(manifests(base),ORACLES):
        fixture = generated_file(output/(name+"-manifest.json"),raw)
        artifact = output/(name+"-artifact.bin")
        cases.append((name,fixture,supplied_sha,artifact,oracle))
    result = {"schema":SCHEMA,"status":"FAIL","configuration_sha256":sys.argv[2],
        "authority":"NATIVE_MANIFEST_REFUSALS_NOT_APPLICATION_RECEIPT_OR_MATHEMATICAL_ADMISSION",
        "host_calls":0,"guest_calls":0,"proof_calls":0,"mathematical_admission":False,
        "proof_call_count_basis":"FINISH_ONLY_SOURCE_CONTROL_FLOW_NOT_RUNTIME_INSTRUMENTATION",
        "segments":167,"assumptions":1,"session_binding":SESSION_BINDING,
        "capsule_binding":CAPSULE_BINDING,"checks":[],"commands":[],
        "known_worker_cpu_seconds":0,"closure_accounting_known":True,
        "accounting":"SUM_OF_DISJOINT_CHILD_JOBS;CONTROLLER_SEPARATE;ENCLOSING_OWNER_INCLUDES_EXIT_TAILS"}

    def rebind():
        for table in (held,generated):
            for path,item in table.items():
                supervisor.absolute(path)
                P.require(P.file_pin(Path(path)) == item,"CONTROL_INPUT_MUTATION:"+path)
        for name in ("layout_result","layout_outer"):
            P.require(not (Path(inputs[name]["path"]).parent/"FINALIZATION-FAILED.json").exists(),
                      "LAYOUT_FINALIZATION_OVERRIDE")

    def envelope(dispatch=False):
        P.require(time.process_time()-cpu_started <= total["controller_cpu_seconds"]
            and time.monotonic()-started <= total["wall_seconds"],"CONTROL_TOTAL_TIME_ENVELOPE")
        if dispatch:
            P.require(result["host_calls"] < 10
                and result["known_worker_cpu_seconds"]+limits["cpu_seconds"] <= total["worker_cpu_seconds"]
                and time.monotonic()-started+limits["wall_seconds"]+5 <= total["wall_seconds"],
                "RESERVED_NEXT_CASE_AND_FINALIZATION")
        count = size = 0
        for parent,dirs,names in os.walk(output,followlinks=False):
            for name in dirs+names:
                path = Path(parent)/name; count += 1
                supervisor.absolute(path,directory=name in dirs)
                if name in names: size += path.stat().st_size
                P.require(count+2 <= total["output_entries"] and size+2*MIB <= total["output_bytes"],
                          "CONTROL_OUTPUT_AND_FINALIZATION_RESERVES")
        return {"bytes":size,"entries":count}

    try:
        for name,fixture,supplied_sha,artifact,oracle in cases:
            rebind(); envelope(dispatch=True)
            supervisor.absolute(artifact,fresh=True)
            argv = [inputs["host"]["path"],"stage-manifest",A_IMAGE,inputs["image"]["path"],
                inputs["wire"]["path"],inputs["expected"]["path"],str(2**26),"18","finish","0",
                str(artifact),"1",inputs["parent"]["path"],inputs["capsule"]["path"],
                fixture["path"],str(fixture["bytes"]),supplied_sha]
            P.require(len(argv) == 17 and argv[8:10] == ["finish","0"],"FINISH_ONLY_NO_PROVER_BRANCH")
            result["host_calls"] += 1
            process = supervisor.supervise(argv,ROOT,output/name,limits,job)
            result["commands"].append({"case":name,"process":process})
            save(output/(name+"-process.json"),P.encoded(process))
            final = process.get("final_job")
            if type(final) is dict:
                P.number(final["cpu_seconds"])
                result["known_worker_cpu_seconds"] += final["cpu_seconds"]
            else:
                result["closure_accounting_known"] = False
            known = P.closure_known(process)
            result["closure_accounting_known"] = result["closure_accounting_known"] and known
            P.require(known and process["status"] == "COMMAND_FAILED"
                and type(process["child_exit_code"]) is int and 0 < process["child_exit_code"] < 256
                and process["termination_requested"] is False and final["terminated_processes"] == 0
                and final["cpu_seconds"] <= limits["cpu_seconds"]
                and process["wall_seconds_through_cleanup"] <= limits["wall_seconds"]
                and all(process["observed_logs"][key] <= limits[key] for key in ("stdout_bytes","stderr_bytes")),
                "ORDINARY_REFUSAL_AND_CLEAN_JOB:"+name)
            stdout = (output/name/"stdout.txt").read_bytes()
            stderr = (output/name/"stderr.txt").read_bytes()
            P.require(len(stdout) <= limits["stdout_bytes"] and len(stderr) <= limits["stderr_bytes"],
                      "REBOUND_LOG_EXTENTS")
            text = stderr.decode("utf-8",errors="strict")
            P.require(not artifact.exists() and not artifact.is_symlink() and stdout == b""
                and "phase=crypto" not in text and "phase=written" not in text
                and "REAL_AGGREGATE_" not in text
                and all(token in text for token in oracle),"EXACT_NATIVE_REFUSAL_ORACLE:"+name)
            P.require(name != "M8" or "dependency row bound" not in text,"M8_DECODED_257_NOT_ROW_REFUSAL")
            P.require(result["known_worker_cpu_seconds"] <= total["worker_cpu_seconds"],"CONTROL_TOTAL_WORKER_CPU")
            result["checks"].append({"case":name,"status":"PASS","required_diagnostics":list(oracle),
                "manifest":fixture,"supplied_manifest_sha256":supplied_sha,"artifact_absent":True})
            rebind(); envelope()
        P.require(len(result["checks"]) == result["host_calls"] == 10,"TEN_DISTINCT_NATIVE_CONTROLS")
        result["status"] = "PASS_TEN_FINISH_ONLY_NATIVE_MANIFEST_REFUSALS"
    except BaseException as error:
        result["error"] = type(error).__name__+": "+str(error)[:2000]
    try:
        rebind()
        P.require(all(not artifact.exists() and not artifact.is_symlink()
                      for _,_,_,artifact,_ in cases),"NO_NATIVE_OUTPUT_ARTIFACTS")
        result["output_census_before_result"] = envelope()
    except BaseException as error:
        result.update(status="FAIL_FINAL_BINDING",final_error=type(error).__name__+": "+str(error)[:2000])
    result["controller_cpu_seconds_before_report"] = time.process_time()-cpu_started
    result["wall_seconds_before_report"] = time.monotonic()-started
    raw = P.encoded(result)
    P.require(len(raw) <= MIB,"FINAL_CONTROL_REPORT_BOUND")
    save(output/"RESULT.json",raw)
    print(raw.decode("utf-8"),end="",flush=True)
    return 0 if result["status"] == "PASS_TEN_FINISH_ONLY_NATIVE_MANIFEST_REFUSALS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

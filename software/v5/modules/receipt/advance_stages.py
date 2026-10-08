"""Owner-selected four-stage prefix over one retained module capsule.

No execution, retry, final receipt, admission, backend rebuild or implicit next
stage. Fresh selections may reuse a pinned completed prefix; crypto authority
remains the unchanged host's real checkpoint verification, never saved JSON.
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
HERE = ROOT / "experiments/v5-local-checks"
BASE = ROOT / "product-local/v4-library-commons-02/commons-v4"
MANIFEST_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
OWNED = {"software/v5/modules/receipt/advance_stages.py"}
SEQUENCE = (("lift", 0), ("segment", 1), ("lift", 1), ("join", 1))
AGGREGATE = {"worker_cpu_seconds": 2250, "controller_cpu_seconds": 60,
             "wall_seconds": 660, "output_bytes": 384*1024**2, "output_entries": 128}
COMMON = {"memory_mib": 4096, "active_processes": 2,
          "stdout_bytes": 1024**2, "stderr_bytes": 1024**2}
INPUT_LIMITS = {"host": 128*1024**2, "host_result": 2*1024**2,
    "image": 64*1024**2, "frame": 16*1024**2+4, "expected": 184,
    "capsule": 64*1024**2, "snapshot_result": 2*1024**2,
    "snapshot_outer_result": 2*1024**2, "python": 128*1024**2,
    "python_dll": 128*1024**2, "segment0": 64*1024**2, "segment0_result": 2*1024**2}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(name, relative, files):
    path = BASE / relative
    raw = path.read_bytes()
    need({"sha256": sha(raw), "bytes": len(raw)} == files[relative], "SUPERVISOR_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def clean(process):
    return (process["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED"
        and process["child_exit_code"] == 0 and process["direct_child_reaped"] is True
        and process["job_closed"] is True and not process["cleanup_errors"]
        and process["termination_requested"] is False
        and process["final_job"]["active_processes"] == 0
        and process["final_job"]["terminated_processes"] == 0)


def main():
    started, controller_started = time.monotonic(), time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize
         and Path(__file__).resolve() == ROOT / "software/v5/modules/receipt/advance_stages.py"
         and len(sys.argv) == 3, "CANONICAL_ISOLATED_OWNER_INVOCATION")
    manifest_path = BASE / "RELEASE-MANIFEST.json"
    manifest_raw = manifest_path.read_bytes()
    need(sha(manifest_raw) == MANIFEST_SHA, "FROZEN_SUPERVISOR_MANIFEST")
    files = json.loads(manifest_raw)["files"]
    A = load("_v5_prefix_supervisor", "operator/commons.py", files)
    load("domains", "receiver/helpers/domains.py", files)
    J = load("_v5_prefix_job", "receiver/helpers/run_stage.py", files)
    selection_path = A.absolute(sys.argv[1])
    need(selection_path.parent == HERE and re.fullmatch(r"[0-9a-f]{64}", sys.argv[2]),
         "EXACT_LOCAL_SELECTION")
    selection_raw = A.bounded_read(selection_path, 1024**2)
    need(sha(selection_raw) == sys.argv[2], "SELECTION_PIN")
    selected = A.strict(selection_raw)
    need(type(selected) is dict and set(selected) == {
        "schema", "name", "sources", "inputs", "image_id", "limits", "completed"}
        and selected["schema"] == "DMKN_V5_RETAINED_PREFIX_V1"
        and re.fullmatch(r"module-base-prefix[0-9]{2}", selected["name"])
        and selected["limits"] == AGGREGATE, "EXACT_FOUR_STAGE_SCOPE")
    need(type(selected["sources"]) is dict and set(selected["sources"]) == OWNED,
         "EXACT_SOURCE_SCOPE")
    sources = {}
    for relative, digest in selected["sources"].items():
        raw = A.bounded_read(ROOT / relative, 2*1024**2)
        need(sha(raw) == digest, "SELECTED_SOURCE_PIN")
        sources[relative] = raw

    all_pins = []
    def input_pin(pin, maximum):
        need(type(pin) is dict and set(pin) == {"path", "bytes", "sha256"}
             and type(pin["bytes"]) is int and 0 < pin["bytes"] <= maximum
             and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]), "INPUT_PIN_FORMAT")
        path = A.absolute(pin["path"])
        need(path.is_relative_to(ROOT), "CANONICAL_INPUT_SCOPE")
        all_pins.append((path, pin))
        return path

    need(type(selected["inputs"]) is dict and set(selected["inputs"]) == set(INPUT_LIMITS),
         "EXACT_INPUT_CENSUS")
    paths = {role: input_pin(pin, INPUT_LIMITS[role]) for role, pin in selected["inputs"].items()}
    need(paths["python"] == BASE / "receiver/runtime/python/python.exe"
         and paths["python_dll"] == paths["python"].parent / "python314.dll"
         and Path(sys.executable).resolve() == paths["python"], "ADOPTED_PYTHON")
    completed = selected["completed"]
    need(type(completed) is list and len(completed) < len(SEQUENCE), "MISSING_SUFFIX_REQUIRED")
    resumes = []
    for position, item in enumerate(completed):
        need(type(item) is dict and set(item) == {"kind", "index", "checkpoint", "report",
             "invocation", "allow_failed_invocation"} and type(item["allow_failed_invocation"]) is bool
             and (item["kind"], item["index"]) == SEQUENCE[position], "CONTIGUOUS_COMPLETED_PREFIX")
        checkpoint = input_pin(item["checkpoint"], 64*1024**2)
        report_path = input_pin(item["report"], 1024**2)
        invocation = input_pin(item["invocation"], 1024**2)
        need(checkpoint.parent == report_path.parent and report_path.name == "RESULT.json"
             and invocation == report_path.parent.parent / "RESULT.json"
             and not (invocation.parent / "FINALIZATION-FAILED.json").exists()
             and not (report_path.parent / "FINALIZATION-FAILED.json").exists(), "RESUME_RESULT_LOCATION")
        resumes.append((item, checkpoint, report_path, invocation))
    unique_pins = {}
    for path, pin in all_pins:
        need(path not in unique_pins or unique_pins[path] == pin, "CONFLICTING_INPUT_PIN")
        unique_pins[path] = pin
    need(len(set(paths.values())) == len(paths)
         and sum(pin["bytes"] for _, pin in all_pins) <= 512*1024**2, "BOUNDED_INPUTS")
    all_pins = list(unique_pins.items())

    def deadline():
        need(time.monotonic()-started <= AGGREGATE["wall_seconds"]
             and time.process_time()-controller_started <= AGGREGATE["controller_cpu_seconds"],
             "WHOLE_OPERATION_LIMIT")

    def rebind():
        deadline()
        need(A.bounded_read(selection_path, 1024**2) == selection_raw
             and A.bounded_read(manifest_path, 8*1024**2) == manifest_raw, "SELECTION_OR_MANIFEST_CHANGED")
        for relative, raw in sources.items():
            need(A.bounded_read(ROOT / relative, 2*1024**2) == raw, "SOURCE_CHANGED")
        for relative in ("operator/commons.py", "receiver/helpers/domains.py", "receiver/helpers/run_stage.py"):
            need(A.pin(BASE / relative) == files[relative], "SUPERVISOR_CHANGED")
        for path, expected in all_pins:
            deadline()
            need(A.pin(path) == {key: expected[key] for key in ("sha256", "bytes")}, "INPUT_CHANGED:"+str(path))
        deadline()

    rebind()
    host = json.loads(A.bounded_read(paths["host_result"], 2*1024**2))
    need(host["status"] == "PASS_MODULE_HOST_COMPILE_ONLY" and host["job"]["active_processes"] == 0
         and host["executable"] == selected["inputs"]["host"], "ACTUAL_ADOPTED_HOST")
    snap = json.loads(A.bounded_read(paths["snapshot_result"], 2*1024**2))
    outer = json.loads(A.bounded_read(paths["snapshot_outer_result"], 2*1024**2))
    need(outer["result"]["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED"
         and outer["result"]["final_job"]["active_processes"] == 0
         and outer["result"]["job_closed"] is True, "CLEAN_SNAPSHOT_WRAPPER")
    need(snap["schema"] == "DMKN_MODULE_SNAPSHOT_SCREEN_V2"
         and snap["status"] == "PASS_REAL_GUEST_SNAPSHOT_ONLY"
         and snap["journal_profile"] == 2 and snap["cycles_cap"] == 2**25
         and snap["segment_po2"] == 18 and snap["guest_execute_calls"] == 1
         and snap["proof_calls"] == 0 and snap["mathematical_admission"] is False
         and snap["metrics"]["assumptions"] == 0 and snap["metrics"]["segments"] == 110,
         "EXACT_SUCCESSFUL_BASE_CAPSULE")
    need(snap["image_id"] == selected["image_id"]
         and re.fullmatch(r"[0-9a-f]{64}", selected["image_id"])
         and all(snap["capsule"][key] == selected["inputs"]["capsule"][key]
                 for key in ("path", "bytes", "sha256"))
         and snap["input_frame_sha256"] == selected["inputs"]["frame"]["sha256"]
         and snap["expected_journal_sha256"] == selected["inputs"]["expected"]["sha256"],
         "EXACT_SNAPSHOT_BINDINGS")
    expected = A.bounded_read(paths["expected"], 184)
    need(len(expected) == 184 and expected[:12] == b"DMKNM002\x02\0\0\0"
         and expected[12:44].hex() == selected["image_id"]
         and expected[108:140].hex() == snap["module_id"]
         and int.from_bytes(expected[176:184], "little") == 0, "PROFILE2_BASE_JOURNAL")
    binding = snap["capsule"]["binding"]
    identity = {role: selected["inputs"][role] for role in ("host", "image", "frame", "expected", "capsule")}
    zero = json.loads(A.bounded_read(paths["segment0_result"], 2*1024**2))
    need(zero["status"] == "PASS_ONE_RETAINED_SEGMENT_NOT_FULL_PROOF" and clean(zero["process"])
         and zero["checkpoint"] == {**selected["inputs"]["segment0"], "binding": binding,
             "schema": 5, "kind": "segment", "index": 0}
         and not (paths["segment0_result"].parent / "FINALIZATION-FAILED.json").exists(),
         "EXACT_RETAINED_SEGMENT0")
    cache = {("segment", 0): paths["segment0"]}
    for item, checkpoint, report_path, invocation in resumes:
        prior = json.loads(A.bounded_read(report_path, 1024**2))
        prior_outer = json.loads(A.bounded_read(invocation, 1024**2))
        need(prior_outer["schema"] == "DMKN_V5_PREFIX_RESULT_V1"
             and prior_outer["input_identity"] == identity
             and prior_outer["final_binding_validated"] is True
             and prior_outer["status"] in ("PASS_SELECTED_PREFIX_NOT_FULL_PROOF", "FAIL")
             and item["allow_failed_invocation"] == (prior_outer["status"] == "FAIL")
             and item["report"] in prior_outer["stages"], "EXPLICIT_PRIOR_INVOCATION_DISPOSITION")
        need(prior["schema"] == "DMKN_V5_PREFIX_STAGE_V1"
             and prior["status"] == "PASS_RETAINED_CHECKPOINT_ONLY" and clean(prior["process"])
             and prior["input_identity"] == identity
             and prior["checkpoint"] == {**item["checkpoint"], "binding": binding, "schema": 5,
                 "kind": item["kind"], "index": item["index"]}, "BOUND_COMPLETED_PREFIX")
        cache[(item["kind"], item["index"])] = checkpoint

    out = A.absolute(HERE / selected["name"], directory=True, fresh=True)
    out.mkdir()
    with (out / "selection.json").open("xb") as stream:
        stream.write(selection_raw); stream.flush(); os.fsync(stream.fileno())
    for relative, raw in sources.items():
        target = out / "sources" / Path(relative).name
        target.parent.mkdir(exist_ok=True)
        with target.open("xb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())

    def census():
        need(A.bounded_read(out / "selection.json", 1024**2) == selection_raw,
             "SAVED_SELECTION_CHANGED")
        for relative, raw in sources.items():
            need(A.bounded_read(out / "sources" / Path(relative).name, 2*1024**2) == raw,
                 "SAVED_SOURCE_CHANGED")
        size, count = 0, 0
        for directory, dirs, names in os.walk(out, followlinks=False):
            for name in dirs + names:
                deadline()
                path = Path(directory) / name
                A.absolute(path, directory=name in dirs)
                count += 1
                need(count <= AGGREGATE["output_entries"], "OUTPUT_ENTRY_LIMIT")
                if name in names:
                    size += path.stat().st_size
                need(size <= AGGREGATE["output_bytes"], "OUTPUT_BYTE_LIMIT")
        return {"bytes": size, "entries": count}

    report = {"schema": "DMKN_V5_PREFIX_RESULT_V1", "status": "FAIL",
        "selection_sha256": sha(selection_raw), "input_identity": identity,
        "planned_stages": [list(x) for x in SEQUENCE[len(completed):]],
        "completed_input_stages": completed, "stages": [], "worker_cpu_seconds": 0,
        "worker_accounting_complete": True, "guest_execute_calls": 0, "proof_stage_calls": 0,
        "application_receipt_created": False, "mathematical_admission": False,
        "authority": "LOCAL_PREFIX_CHECKPOINTS_NOT_APPLICATION_CERTIFICATE"}
    try:
        for kind, index in SEQUENCE[len(completed):]:
            rebind(); census()
            for key, checkpoint in cache.items():
                with checkpoint.open("rb") as stream:
                    need(stream.read(4) == (5).to_bytes(4, "little"), "CHECKPOINT_SCHEMA5")
            deps = [] if kind == "segment" else ([cache[("segment", index)]] if kind == "lift"
                                                  else [cache[("lift", 0)], cache[("lift", 1)]])
            stage_dir = out / (kind+"-"+str(index))
            stage_dir.mkdir()
            artifact = stage_dir / (kind+"-"+str(index)+".checkpoint")
            limits = {**COMMON, "cpu_seconds": 1500 if kind == "segment" else 250,
                      "wall_seconds": 300 if kind == "segment" else 120}
            limits["wall_seconds"] = min(limits["wall_seconds"],
                math.floor(AGGREGATE["wall_seconds"]-(time.monotonic()-started)))
            need(limits["wall_seconds"] > 0 and report["worker_cpu_seconds"]+limits["cpu_seconds"]
                 <= AGGREGATE["worker_cpu_seconds"], "REMAINING_PREFIX_RESERVATION")
            argv = [str(paths["host"]), "stage", str(paths["image"]), str(paths["frame"]),
                str(paths["expected"]), str(2**25), "18", kind, str(index), str(artifact),
                "0", str(paths["capsule"]), *map(str, deps)]
            stage = {"schema": "DMKN_V5_PREFIX_STAGE_V1", "status": "FAIL", "kind": kind,
                "index": index, "input_identity": identity, "selection_sha256": sha(selection_raw)}
            report["proof_stage_calls"] += 1
            try:
                process = A.supervise(argv, BASE, stage_dir / "command", limits, J.Job)
            except BaseException as error:
                process = {"status": "SUPERVISOR_RAISED_UNCERTAIN", "final_job": None}
                stage["supervisor_error"] = type(error).__name__+": "+str(error)[:2000]
            stage["process"] = process
            final = process.get("final_job")
            charge = final["cpu_seconds"] if final is not None else limits["cpu_seconds"]
            report["worker_cpu_seconds"] += charge
            report["worker_accounting_complete"] &= final is not None
            stage["worker_cpu_seconds_or_reserved"] = charge
            try:
                need(report["worker_cpu_seconds"] <= AGGREGATE["worker_cpu_seconds"], "AGGREGATE_WORKER_CPU_LIMIT")
                need(clean(process), "PROOF_STAGE_NOT_CLEAN")
                stdout = A.bounded_read(stage_dir / "command/stdout.txt", COMMON["stdout_bytes"]).decode("ascii").strip()
                match = re.fullmatch(r"REAL_PROOF_CHECKPOINT_NOT_APPLICATION_CERTIFICATE kind="+kind+
                    r" index="+str(index)+r" checkpoint_bytes=([0-9]+) segments=110 assumptions=0 binding=([0-9a-f]{64})", stdout)
                need(match is not None and match[2] == binding, "SAME_CAPSULE_STAGE_MARKER")
                artifact_pin = A.pin(artifact)
                need(0 < artifact_pin["bytes"] <= 64*1024**2 and artifact_pin["bytes"] == int(match[1]), "CHECKPOINT_BOUND")
                rebind(); census(); deadline()
                stage.update(status="PASS_RETAINED_CHECKPOINT_ONLY", checkpoint={"path": str(artifact),
                    **artifact_pin, "binding": binding, "schema": 5, "kind": kind, "index": index})
            except BaseException as error:
                stage.update(status="FAIL", error=type(error).__name__+": "+str(error)[:2000])
            A.save_new(stage_dir / "RESULT.json", stage)
            report["stages"].append({"path": str(stage_dir / "RESULT.json"), **A.pin(stage_dir / "RESULT.json")})
            try:
                deadline(); census()
            except BaseException:
                A.save_new(stage_dir / "FINALIZATION-FAILED.json", {"status": "STAGE_FINALIZATION_LIMIT"})
                raise
            need(stage["status"] == "PASS_RETAINED_CHECKPOINT_ONLY", "FIRST_STAGE_FAILURE_STOPS_PREFIX")
            cache[(kind, index)] = artifact
            all_pins.append((artifact, {"path": str(artifact), **artifact_pin}))
        rebind(); deadline()
        need(report["worker_cpu_seconds"] <= AGGREGATE["worker_cpu_seconds"], "FINAL_AGGREGATE_WORKER_CPU_LIMIT")
        report.update(status="PASS_SELECTED_PREFIX_NOT_FULL_PROOF", output_census_before_result=census())
    except BaseException as error:
        report.update(status="FAIL", error=type(error).__name__+": "+str(error)[:2000])
    report["final_binding_validated"] = False
    try:
        rebind()
        report["final_binding_validated"] = True
    except BaseException as error:
        report.update(status="FAIL", final_binding_error=type(error).__name__+": "+str(error)[:2000])
    report.update(controller_cpu_seconds=time.process_time()-controller_started,
        wall_seconds=time.monotonic()-started,
        accounting="THIS_INVOCATION_WORKER_JOB_PLUS_CONTROLLER;SUPERVISION_NESTED;PRIOR_WORK_RETAINED_NOT_RECHARGED")
    A.save_new(out / "RESULT.json", report)
    try:
        deadline(); census()
    except BaseException:
        A.save_new(out / "FINALIZATION-FAILED.json", {"status": "PREFIX_FINALIZATION_LIMIT"})
        print("FAIL_FINALIZATION_LIMIT", flush=True)
        return 1
    print(json.dumps(report), flush=True)
    return 0 if report["status"] == "PASS_SELECTED_PREFIX_NOT_FULL_PROOF" else 1


if __name__ == "__main__":
    raise SystemExit(main())

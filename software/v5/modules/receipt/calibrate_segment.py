"""Exactly one selected segment-0 proof from a retained successful v5 capsule.

No guest execution, retry, next stage, receipt admission or cap override. Uses
the unchanged adopted owner supervisor directly; Run-V5-Check stays unchanged.
The selection is a local owner instruction, never untrusted network data.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import re
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
BASE = ROOT / "product-local/v4-library-commons-02/commons-v4"
MANIFEST_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
OWNED = {"software/v5/modules/receipt/calibrate_segment.py",
         "software/v5/modules/receipt/SEGMENT-CALIBRATION-PLAN.md"}
LIMITS = {"cpu_seconds": 1500, "wall_seconds": 300, "memory_mib": 4096,
          "active_processes": 2, "stdout_bytes": 1048576, "stderr_bytes": 1048576}
INPUT_LIMITS = {"host": 128*1024**2, "host_result": 2*1024**2,
    "image": 64*1024**2, "frame": 16*1024**2+4, "expected": 184,
    "capsule": 64*1024**2, "snapshot_result": 2*1024**2,
    "snapshot_outer_result": 2*1024**2, "python": 128*1024**2,
    "python_dll": 128*1024**2}


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


def main():
    started, controller_started = time.monotonic(), time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize
         and Path(__file__).resolve() == ROOT / "software/v5/modules/receipt/calibrate_segment.py"
         and len(sys.argv) == 3, "CANONICAL_ISOLATED_OWNER_INVOCATION")
    manifest_path = BASE / "RELEASE-MANIFEST.json"
    manifest_raw = manifest_path.read_bytes()
    need(sha(manifest_raw) == MANIFEST_SHA, "FROZEN_SUPERVISOR_MANIFEST")
    files = json.loads(manifest_raw)["files"]
    A = load("_v5_segment_supervisor", "operator/commons.py", files)
    load("domains", "receiver/helpers/domains.py", files)
    J = load("_v5_segment_job", "receiver/helpers/run_stage.py", files)
    selection_path = A.absolute(sys.argv[1])
    need(selection_path.parent == HERE and re.fullmatch(r"[0-9a-f]{64}", sys.argv[2]),
         "EXACT_LOCAL_SELECTION")
    selection_raw = A.bounded_read(selection_path, 1024**2)
    need(sha(selection_raw) == sys.argv[2], "SELECTION_PIN")
    selected = A.strict(selection_raw)
    need(type(selected) is dict and set(selected) == {
        "schema", "name", "sources", "inputs", "image_id", "limits"}
        and selected["schema"] == "DMKN_V5_RETAINED_SEGMENT0_V1"
        and selected["name"] == "module-base-segment0-01"
        and selected["limits"] == LIMITS, "EXACT_SINGLE_STAGE_SCOPE")
    A.limits_checked(selected["limits"])
    need(type(selected["sources"]) is dict and set(selected["sources"]) == OWNED,
         "EXACT_SOURCE_SCOPE")
    source_bytes = {}
    for relative, digest in selected["sources"].items():
        raw = A.bounded_read(ROOT / relative, 2*1024**2)
        need(sha(raw) == digest, "SELECTED_SOURCE_PIN")
        source_bytes[relative] = raw
    need(type(selected["inputs"]) is dict and set(selected["inputs"]) == set(INPUT_LIMITS),
         "EXACT_INPUT_CENSUS")
    paths = {}
    for role, pin in selected["inputs"].items():
        need(type(pin) is dict and set(pin) == {"path", "bytes", "sha256"}
             and type(pin["bytes"]) is int and 0 < pin["bytes"] <= INPUT_LIMITS[role]
             and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]), "INPUT_PIN_FORMAT")
        paths[role] = A.absolute(pin["path"])
        need(paths[role].is_relative_to(ROOT), "CANONICAL_INPUT_SCOPE")
    need(len(set(paths.values())) == len(paths)
         and sum(pin["bytes"] for pin in selected["inputs"].values()) <= 256*1024**2,
         "DISTINCT_BOUNDED_INPUTS")
    need(paths["python"] == BASE / "receiver/runtime/python/python.exe"
         and paths["python_dll"] == paths["python"].parent / "python314.dll"
         and Path(sys.executable).resolve() == paths["python"], "ADOPTED_PYTHON")

    def deadline():
        need(time.monotonic()-started <= LIMITS["wall_seconds"]
             and time.process_time()-controller_started <= 60, "WHOLE_OPERATION_LIMIT")

    def rebind():
        deadline()
        need(A.bounded_read(selection_path, 1024**2) == selection_raw
             and A.bounded_read(manifest_path, 8*1024**2) == manifest_raw,
             "SELECTION_OR_MANIFEST_CHANGED")
        for relative, raw in source_bytes.items():
            need(A.bounded_read(ROOT / relative, 2*1024**2) == raw, "SOURCE_CHANGED")
        for relative in ("operator/commons.py", "receiver/helpers/domains.py", "receiver/helpers/run_stage.py"):
            need(A.pin(BASE / relative) == files[relative], "SUPERVISOR_CHANGED")
        for role, path in paths.items():
            deadline()
            expected = selected["inputs"][role]
            need(A.pin(path) == {key: expected[key] for key in ("sha256", "bytes")},
                 "INPUT_CHANGED:" + role)
        deadline()

    rebind()
    host = json.loads(A.bounded_read(paths["host_result"], 2*1024**2))
    need(host["status"] == "PASS_MODULE_HOST_COMPILE_ONLY" and host["job"]["active_processes"] == 0
         and host["executable"] == selected["inputs"]["host"], "ACTUAL_ADOPTED_HOST")
    snap = json.loads(A.bounded_read(paths["snapshot_result"], 2*1024**2))
    outer = json.loads(A.bounded_read(paths["snapshot_outer_result"], 2*1024**2))
    need(outer["result"]["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED"
         and outer["result"]["final_job"]["active_processes"] == 0
         and outer["result"]["job_closed"] is True, "ACTUAL_CLEAN_SNAPSHOT_WRAPPER")
    need(snap["schema"] == "DMKN_MODULE_SNAPSHOT_SCREEN_V2"
         and snap["status"] == "PASS_REAL_GUEST_SNAPSHOT_ONLY"
         and snap["journal_profile"] == 2 and snap["cycles_cap"] == 2**25
         and snap["segment_po2"] == 18 and snap["guest_execute_calls"] == 1
         and snap["proof_calls"] == 0 and snap["mathematical_admission"] is False
         and snap["metrics"]["assumptions"] == 0
         and 1 <= snap["metrics"]["segments"] <= 128, "SUCCESSFUL_RETAINED_BASE_CAPSULE")
    need(snap["image_id"] == selected["image_id"]
         and re.fullmatch(r"[0-9a-f]{64}", selected["image_id"])
         and all(snap["capsule"][key] == selected["inputs"]["capsule"][key]
                 for key in ("path", "bytes", "sha256"))
         and snap["input_frame_sha256"] == selected["inputs"]["frame"]["sha256"]
         and snap["expected_journal_sha256"] == selected["inputs"]["expected"]["sha256"],
         "EXACT_SNAPSHOT_ARTIFACT_BINDINGS")
    expected = A.bounded_read(paths["expected"], 184)
    need(len(expected) == 184 and expected[:12] == b"DMKNM002\x02\0\0\0"
         and expected[12:44].hex() == selected["image_id"]
         and expected[108:140].hex() == snap["module_id"]
         and int.from_bytes(expected[176:184], "little") == 0, "EXACT_PROFILE2_BASE_JOURNAL")
    with paths["capsule"].open("rb") as stream:
        need(stream.read(4) == (3).to_bytes(4, "little"), "CAPSULE_SCHEMA3")
    out = A.absolute(HERE / selected["name"], directory=True, fresh=True)
    out.mkdir()
    with (out / "selection.json").open("xb") as stream:
        stream.write(selection_raw)
    for relative, raw in source_bytes.items():
        target = out / "sources" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(raw)
    artifact = out / "segment-0.checkpoint"
    argv = [str(paths["host"]), "stage", str(paths["image"]), str(paths["frame"]),
        str(paths["expected"]), str(2**25), "18", "segment", "0", str(artifact),
        "0", str(paths["capsule"])]
    report = {"schema": "DMKN_V5_RETAINED_SEGMENT0_RESULT_V1", "status": "FAIL",
        "selection_sha256": sha(selection_raw), "guest_execute_calls": 0,
        "proof_stage_calls": 0, "application_receipt_created": False,
        "mathematical_admission": False, "authority": "LOCAL_STAGE_COST_NOT_APPLICATION_CERTIFICATE"}
    try:
        deadline()
        report["proof_stage_calls"] = 1
        result = A.supervise(argv, BASE, out / "command", LIMITS, J.Job, started=started)
        report["process"] = result
        A.save_new(out / "process.json", result)
        need(result["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED"
             and result["child_exit_code"] == 0 and result["direct_child_reaped"] is True
             and result["job_closed"] is True and not result["cleanup_errors"]
             and result["termination_requested"] is False
             and result["final_job"]["active_processes"] == 0
             and result["final_job"]["terminated_processes"] == 0, "PROOF_STAGE_NOT_CLEAN")
        record = A.bounded_read(out / "command/stdout.txt", LIMITS["stdout_bytes"]).decode("ascii").strip()
        match = re.fullmatch(r"REAL_PROOF_CHECKPOINT_NOT_APPLICATION_CERTIFICATE kind=segment index=0 "
            r"checkpoint_bytes=([0-9]+) segments=([0-9]+) assumptions=0 binding=([0-9a-f]{64})", record)
        need(match is not None and int(match[2]) == snap["metrics"]["segments"]
             and match[3] == snap["capsule"]["binding"], "EXACT_SAME_CAPSULE_SEGMENT_RECORD")
        artifact_pin = A.pin(artifact)
        need(0 < artifact_pin["bytes"] <= 64*1024**2 and artifact_pin["bytes"] == int(match[1]),
             "CHECKPOINT_BYTE_BINDING")
        with artifact.open("rb") as stream:
            need(stream.read(4) == (5).to_bytes(4, "little"), "CHECKPOINT_SCHEMA5")
        rebind()
        for relative, raw in source_bytes.items():
            need(A.bounded_read(out / "sources" / relative, 2*1024**2) == raw, "SNAPSHOT_SOURCE_CHANGED")
        need(A.bounded_read(out / "selection.json", 1024**2) == selection_raw, "SNAPSHOT_SELECTION_CHANGED")
        deadline()
        report.update(status="PASS_ONE_RETAINED_SEGMENT_NOT_FULL_PROOF", checkpoint={
            "path": str(artifact), **artifact_pin, "binding": match[3], "schema": 5,
            "kind": "segment", "index": 0}, segments=snap["metrics"]["segments"],
            scope="ONE_ACTUAL_STAGE_NOT_A_BOUND_FOR_ALL_REMAINING_STAGES")
    except BaseException as error:
        report.update(status="FAIL", error=type(error).__name__ + ": " + str(error)[:2000])
    if report["status"] != "PASS_ONE_RETAINED_SEGMENT_NOT_FULL_PROOF":
        # Preserve failed-stage evidence too; failure never gains authority if
        # its final pins or operation deadline cannot be confirmed.
        try:
            rebind()
        except BaseException as error:
            report["final_binding_error"] = type(error).__name__ + ": " + str(error)[:2000]
    report.update(controller_cpu_seconds=time.process_time()-controller_started,
                  wall_seconds=time.monotonic()-started,
                  accounting="PROCESS_WORKER_JOB_PLUS_THIS_CONTROLLER;SUPERVISION_CPU_IS_NESTED")
    A.save_new(out / "RESULT.json", report)
    # A blocking final report write cannot turn an expired operation into success.
    try:
        deadline()
    except BaseException:
        A.save_new(out / "FINALIZATION-FAILED.json", {"status": "WHOLE_OPERATION_LIMIT_AFTER_REPORT"})
        print("FAIL_FINALIZATION_LIMIT", flush=True)
        return 1
    print(json.dumps(report), flush=True)
    return 0 if report["status"] == "PASS_ONE_RETAINED_SEGMENT_NOT_FULL_PROOF" else 1


if __name__ == "__main__":
    raise SystemExit(main())

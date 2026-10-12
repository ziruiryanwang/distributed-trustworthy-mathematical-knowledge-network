"""One real worker/native launch with the unchanged two-active-process cap.

The native request deliberately supplies the wrong schema. A schema-specific
refusal and clean whole-Job closure establish launch compatibility, not math.
Run only through the separately pinned owner Run-V5-Check selection.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
BASE = ROOT / "product-local/v4-library-commons-02/commons-v4"
MANIFEST_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
NATIVE = ROOT / "experiments/v5-local-checks/author-lean-link-01/link/AuthorLean.exe"
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
DLLS = ("libInit_shared.dll", "libleanshared.dll", "libleanshared_1.dll",
        "libleanshared_2.dll", "libc++.dll")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pin(path):
    path = path.resolve()
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": digest}


def load(name, relative, files):
    path = BASE / relative
    raw = path.read_bytes()
    require({"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)} == files[relative],
            "SUPERVISOR_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def main():
    started = time.monotonic()
    require(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
            and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
            "CANONICAL_ISOLATED_INVOCATION")
    require(len(sys.argv) == 2, "FRESH_EVIDENCE_PATH_REQUIRED")
    evidence = Path(sys.argv[1])
    require(evidence.is_absolute() and evidence.resolve() == evidence
            and evidence.parent.is_dir() and not evidence.exists()
            and evidence.is_relative_to(ROOT / "experiments/v5-local-checks"), "FRESH_EVIDENCE")
    selection = json.loads((evidence.parent / "selection.json").read_bytes())
    runtime = selection["runtime_pins"]
    manifest = (BASE / "RELEASE-MANIFEST.json").read_bytes()
    require(hashlib.sha256(manifest).hexdigest() == MANIFEST_SHA, "MANIFEST_PIN")
    files = json.loads(manifest)["files"]
    supervisor = load("_envelope_supervisor", "operator/commons.py", files)
    load("domains", "receiver/helpers/domains.py", files)
    jobs = load("_envelope_jobs", "receiver/helpers/run_stage.py", files)
    worker = Path(__file__).resolve().parents[1] / "authoring/worker.py"
    worker_pin = pin(worker)
    require(worker_pin["sha256"] == selection["sources"]["software/v5/authoring/worker.py"],
            "SNAPSHOT_WORKER_PIN")
    native_pin = pin(NATIVE)
    dll_pins = [pin(LEAN / "bin" / name) for name in DLLS]
    for item in [pin(Path(sys.executable)), native_pin, *dll_pins]:
        require(runtime[item["path"]] == item["sha256"], "SELECTED_RUNTIME_PIN")
    evidence.mkdir()
    request = evidence / "malformed-request.json"
    with request.open("xb") as stream:
        stream.write(b'{"schema":"DMKN_INTENTIONAL_WRONG_SCHEMA","mathematical_acceptance":false}')
        stream.flush(); os.fsync(stream.fileno())
    config = {"schema": "DMKN_OWNER_LEAN_WORKER_V1", "worker": worker_pin,
              "executable": native_pin, "lean_root": str(LEAN), "runtime_pins": dll_pins,
              "request": pin(request), "output_directory": str(evidence / "native-output"),
              "report_path": str(evidence / "worker-result.json"),
              "deadline_monotonic": started + 20}
    config_path = evidence / "worker-config.json"
    supervisor.save_new(config_path, config)
    config_pin = pin(config_path)
    limits = {"cpu_seconds": 10, "wall_seconds": 20, "memory_mib": 512,
              "active_processes": 2, "stdout_bytes": 1048576, "stderr_bytes": 1048576}
    process = supervisor.supervise([sys.executable, "-I", "-S", "-B", str(worker),
        "--config", str(config_path), "--config-sha256", config_pin["sha256"]],
        BASE, evidence / "process", limits, jobs.Job, started=started)
    supervisor.save_new(evidence / "process.json", process)
    worker_report = supervisor.strict(supervisor.bounded_read(evidence / "worker-result.json", 1048576))
    stderr = supervisor.bounded_read(evidence / "process/stderr.txt", 1048576).decode("utf-8")
    checks = {
        "expected_worker_refusal": process["status"] == "COMMAND_FAILED" and process["child_exit_code"] == 1,
        "same_call_worker_binding": worker_report["schema"] == "DMKN_OWNER_LEAN_WORKER_RESULT_V1"
            and worker_report["status"] == "FAIL"
            and worker_report["config_sha256"] == config_pin["sha256"]
            and worker_report["request_sha256"] == config["request"]["sha256"]
            and worker_report["executable_sha256"] == native_pin["sha256"]
            and worker_report["worker_sha256"] == worker_pin["sha256"]
            and not worker_report.get("cleanup_error"),
        "actual_native_parser_reached": "OWNER_AUTHORING_FAILED" in stderr and "AUTHOR_REQUEST_SCHEMA" in stderr,
        "native_reaped": worker_report["native_return_code"] == 1 and worker_report["direct_child_reaped"] is True,
        "no_timeout": worker_report["native_timed_out"] is False,
        "expected_worker_diagnostic": worker_report.get("error") == "WORKER_NATIVE_REFUSED",
        "no_promotion": worker_report["mathematical_acceptance"] is False and worker_report["export_sha256"] is None,
        "whole_job_closed": process["direct_child_reaped"] is True and process["job_closed"] is True
            and not process["termination_requested"] and not process["cleanup_errors"]
            and process["final_job"]["active_processes"] == 0
            and process["final_job"]["terminated_processes"] == 0,
        "inner_resource_limits": process["final_job"]["cpu_seconds"] <= limits["cpu_seconds"]
            and process["wall_seconds_through_cleanup"] <= limits["wall_seconds"]
            and process["final_job"]["peak_job_private_commit_bytes"] <= limits["memory_mib"] * 1048576,
        "input_unchanged": pin(request) == config["request"] and pin(config_path) == config_pin,
    }
    result = {"status": "PASS_REAL_WORKER_NATIVE_CAP2_LAUNCH_ONLY" if all(checks.values()) else "FAIL",
              "checks": checks, "process": process, "worker": worker_report,
              "mathematical_admission": False, "scope": "LAUNCH_ENVELOPE_NOT_POSITIVE_AUTHORING",
              "wall_before_report": time.monotonic() - started}
    supervisor.save_new(evidence / "RESULT.json", result)
    print(json.dumps({"status": result["status"], "checks": checks}), flush=True)
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())

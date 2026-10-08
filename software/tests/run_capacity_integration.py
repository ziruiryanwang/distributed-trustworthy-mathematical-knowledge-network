"""Pinned standalone metadata-engine unittest suites; no mathematical authority.

One exact allocation per launch. The selected suite checks four v3 integration boundaries,
with synthetic workloads and mocked supply, never native acceptance. New suites require explicit source review.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import time

SOURCE = Path(__file__).resolve().parents[1]
LIMITS = {"wall_seconds": 60, "cpu_seconds": 30, "memory_mib": 512,
          "active_processes": 8, "stdout_bytes": 65536,
          "stderr_bytes": 65536, "event_bytes": 65536}
RETAINED = {"bytes": 256 * 1048576, "files": 4096, "entries": 8192}
SUITES = {"test_capacity_integration.py": "v3 integration controls; synthetic dispatcher workloads; no native acceptance"}
REQUEST = b'{"op":"test-metadata-contracts"}\n'


def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def read(path, bound=1048576):
    with Path(path).open("rb") as stream:
        raw = stream.read(bound + 1)
    require(len(raw) <= bound, "INPUT_BOUND")
    return raw


def safe(path):
    path = Path(path)
    require(path.is_absolute(), "ABSOLUTE_PATH")
    for ancestor in (path, *path.parents):
        require(not ancestor.is_symlink() and not getattr(ancestor.lstat(), "st_file_attributes", 0) & 0x400,
                "REPARSE_POINT")
    return path.resolve(strict=True)


def pin(path):
    path = safe(path)
    require(path.is_file() and path.stat().st_size <= RETAINED["bytes"], "PIN_FILE_BOUND")
    digest, size = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while part := stream.read(1048576):
            size += len(part)
            require(size <= RETAINED["bytes"], "PIN_BYTE_BOUND")
            digest.update(part)
    require(size == path.stat().st_size, "PIN_SIZE_CHANGED")
    return {"path": str(path), "bytes": size, "sha256": digest.hexdigest()}


def save_raw(path, raw):
    require(len(raw) <= 2 * 1048576, "OUTPUT_RECORD_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def load(path):
    def pairs(items):
        value = {}
        for key, item in items:
            require(key not in value, "DUPLICATE_KEY")
            value[key] = item
        return value
    def bad(_):
        raise RuntimeError("NONFINITE_JSON")
    launch = json.loads(read(safe(path), 65536), object_pairs_hook=pairs, parse_constant=bad)
    require(type(launch) is dict and set(launch) == {"schema", "allocation", "suite", "tests", "pins", "limits", "retained"}
            and type(launch["schema"]) is int and launch["schema"] == 1
            and type(launch["allocation"]) is str and re.fullmatch(r"capacity-integration-[0-9]{2}", launch["allocation"])
            and type(launch["suite"]) is str and launch["suite"] in SUITES
            and type(launch["tests"]) is int and launch["tests"] == 4
            and encode(launch["limits"]) == encode(LIMITS)
            and encode(launch["retained"]) == encode(RETAINED), "EXACT_LAUNCH")
    return launch


def paths(launch):
    return [Path(sys.executable), Path(__file__).resolve(), SOURCE / "py/run_stage.py",
            SOURCE / "py/supervise.py", SOURCE / "py/domains.py",
            SOURCE / "py/capacity.py", SOURCE / "py/storage.py", SOURCE / "py/admin_worker.py",
            SOURCE / "py/node.py", SOURCE / "manage.py", SOURCE / "build.py",
            SOURCE / "tests" / launch["suite"]]


def worker(args):
    import unittest
    launch = load(args.config)
    require(encode([pin(path) for path in paths(launch)]) == encode(launch["pins"]), "WORKER_PINS")
    state = SOURCE.parent / "product-local" / launch["allocation"]
    require(args.state.resolve() == state and state.is_dir() and not any(state.iterdir())
            and read(args.request, 1024) == REQUEST, "FIXED_WORKER_BINDING")
    os.environ["DTMKN_TEST_ROOT"] = str(state)
    suite = unittest.defaultTestLoader.discover(str(SOURCE / "tests"), pattern=launch["suite"])
    module = sys.modules.get(Path(launch["suite"]).stem)
    require(module is not None and Path(module.__file__).resolve() == paths(launch)[-1].resolve(),
            "SUITE_MODULE_ORIGIN")
    require(suite.countTestCases() == launch["tests"], "DECLARED_SUITE_COUNT")
    observed = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    result = {"status": "PASS" if observed.wasSuccessful() and observed.testsRun == launch["tests"]
              and not observed.skipped else "FAIL", "tests": observed.testsRun,
              "failures": len(observed.failures), "errors": len(observed.errors),
              "skipped": len(observed.skipped), "scope": SUITES[launch["suite"]]}
    raw = encode(result)
    save_raw(args.event, encode({"request_sha256": hashlib.sha256(REQUEST).hexdigest(),
                               "response_sha256": hashlib.sha256(raw).hexdigest()}))
    sys.stdout.buffer.write(raw)


def quiescent(receipt):
    return bool(receipt and receipt.get("direct_child_reaped") is True
                and receipt.get("final_active_zero") is True and receipt.get("job_closed") is True
                and not receipt.get("cleanup_errors") and receipt.get("final_job", {}).get("active_processes") == 0)


def coordinator(args):
    started, cpu_started = time.monotonic(), time.process_time()
    launch = load(args.launch)
    selected = [pin(path) for path in paths(launch)]
    require(encode(selected) == encode(launch["pins"]), "EXACT_ORDERED_PINS")
    evidence = SOURCE / "qualification" / launch["allocation"]
    state = SOURCE.parent / "product-local" / launch["allocation"]
    for path in (evidence, state):
        safe(path.parent)
        require(not os.path.lexists(path), "FRESH_ALLOCATION_REQUIRED")
    evidence.mkdir()
    cases, snapshots = evidence / "cases", evidence / "sources"
    result = {"status": "FAILED", "scope": SUITES[launch["suite"]], "cpu_complete": False,
              "containment": "worker Windows Job; coordinator copying/census outside Job",
              "measurement_scope": "coordinator entry through final report preparation; interpreter startup and final write excluded"}
    response, receipt = None, None
    transport_attempted, supervisor_module = False, None
    try:
        state.mkdir()
        cases.mkdir()
        snapshots.mkdir()
        save_raw(evidence / "launch.json", read(args.launch, 65536))
        for path, expected in zip(paths(launch)[1:], selected[1:]):
            raw = read(path, 1048576)
            require(hashlib.sha256(raw).hexdigest() == expected["sha256"] and len(raw) == expected["bytes"],
                    "SOURCE_SNAPSHOT_BINDING")
            save_raw(snapshots / path.name, raw)
        sys.path.insert(0, str(SOURCE / "py"))
        import run_stage
        import supervise
        supervisor_module = supervise
        for module, path in ((run_stage, SOURCE / "py/run_stage.py"),
                             (supervise, SOURCE / "py/supervise.py"),
                             (run_stage.domain_module, SOURCE / "py/domains.py")):
            require(Path(module.__file__).resolve() == path.resolve(), "SUPERVISOR_MODULE_ORIGIN")
        transport = supervise.Transport(sys.executable, Path(__file__).resolve(), args.launch,
            state, cases, run_stage, dict(LIMITS, pins=[*selected, pin(args.launch)]))
        transport_attempted = True
        response = transport("suite", REQUEST)
    except BaseException as error:
        result["execution_error"] = type(error).__name__ + ":" + str(error)[:1024]
        if supervisor_module is not None and isinstance(error, supervisor_module.SupervisorFailure):
            receipt = error.record
    try:
        if receipt is None:
            receipt = json.loads(read(cases / "suite/supervisor.json"))
        result["job_cpu_seconds"] = receipt.get("final_job", {}).get("cpu_seconds")
        result["cleanup"] = {key: receipt.get(key) for key in
                             ("direct_child_reaped", "final_active_zero", "job_closed", "cleanup_errors")}
        observed_cpu = result["job_cpu_seconds"]
        result["cpu_complete"] = (quiescent(receipt) and type(observed_cpu) in (int, float)
                                  and math.isfinite(observed_cpu) and observed_cpu >= 0)
        save_raw(evidence / "supervisor-observation.json", encode(receipt))
        if response is not None:
            outcome = json.loads(response["stdout"])
            result["outcome"] = outcome
            require(response["returncode"] == 0 and outcome == {"status": "PASS", "tests": launch["tests"],
                "errors": 0, "failures": 0, "skipped": 0, "scope": SUITES[launch["suite"]]}
                and quiescent(receipt), "EXACT_SUITE_PASS")
            result["status"] = "PASS_PENDING_AUDIT"
    except BaseException as error:
        result["observation_error"] = type(error).__name__ + ":" + str(error)[:1024]
        result["status"] = "FAILED"
    try:
        require(not transport_attempted or quiescent(receipt), "CENSUS_REQUIRES_QUIESCENCE")
        pending, files, entries, total = [p for p in (state, evidence) if p.is_dir()], [], 0, 0
        while pending:
            for path in pending.pop().iterdir():
                entries += 1
                require(entries <= RETAINED["entries"], "ENTRY_LIMIT")
                path = safe(path)
                if path.is_dir():
                    pending.append(path)
                else:
                    total += path.stat().st_size
                    require(len(files) < RETAINED["files"] and total <= RETAINED["bytes"], "RETAINED_LIMIT")
                    files.append(pin(path))
        census = encode({"files": files, "entries": entries, "bytes": total,
                         "endpoint": "after quiescence, before census and result files"})
        require(total + len(census) + 65536 <= RETAINED["bytes"] and len(files) + 2 <= RETAINED["files"]
                and entries + 2 <= RETAINED["entries"], "FINAL_RETAINED_LIMIT")
        save_raw(evidence / "census.json", census)
        result.update(census=pin(evidence / "census.json"), retained_bytes_before_final=total,
                      retained_files_before_final=len(files))
    except BaseException as error:
        result["status"] = "FAILED"
        result["census_error"] = type(error).__name__ + ":" + str(error)[:1024]
    result["elapsed_seconds"] = time.monotonic() - started
    result["coordinator_cpu_seconds"] = time.process_time() - cpu_started
    raw = encode(result)
    require(len(raw) <= 65536, "FINAL_RESULT_BOUND")
    save_raw(evidence / "result.json", raw)
    sys.stdout.buffer.write(raw)
    return 0 if result["status"] == "PASS_PENDING_AUDIT" else 1


def main():
    require(os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_site and sys.flags.no_user_site, "WINDOWS_STARTUP_PROFILE")
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", type=Path)
    for name in ("config", "state", "request", "event"):
        parser.add_argument("--" + name, type=Path)
    args = parser.parse_args()
    if args.launch is not None:
        require(all(getattr(args, name) is None for name in ("config", "state", "request", "event")), "MODE")
        return coordinator(args)
    require(all(getattr(args, name) is not None for name in ("config", "state", "request", "event")), "MODE")
    worker(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

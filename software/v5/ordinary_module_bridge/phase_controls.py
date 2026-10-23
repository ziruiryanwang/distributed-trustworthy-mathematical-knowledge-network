"""Mocked subprocess controls for the new three-phase module commit gate.

No Lean, owner, catalog, database, network or actual child process is exercised.
The inert fixture's invented report is not a mathematical warrant. All scratch
files are fresh retained scenario files inside the selected output directory.
One original35wall/20CPU lifetime; an enclosing supervisor owns hard limits.
"""
import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
from contextlib import ExitStack
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import sqlite3
import stat
import subprocess
import sys
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
PHASES = ["build", "reread-private", "reread-exported"]


def need(condition, code):
    if not condition:
        raise AssertionError(code)


def check():
    need(time.monotonic() < START_WALL+35 and time.process_time()-START_CPU < 20,
         "PHASE_CONTROL_ORIGINAL_ALLOWANCE")


def forbidden(*_, **__):
    raise AssertionError("PHASE_CONTROL_FORBIDDEN_EXTERNAL_OPERATION")


def save(path, value):
    raw = value if type(value) is bytes else json.dumps(value, sort_keys=True,
        ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode("ascii")
    need(0 < len(raw) <= MIB, "PHASE_CONTROL_FIXTURE_BOUND")
    with path.open("xb") as handle:
        handle.write(raw)


def load_worker(path, expected):
    need(path.is_absolute() and path.is_relative_to(ROOT) and ".." not in path.parts,
         "PHASE_CONTROL_CANONICAL_SOURCE")
    for item in (*reversed(path.parents), path):
        metadata = item.lstat()
        need(not stat.S_ISLNK(metadata.st_mode) and
             not getattr(metadata, "st_file_attributes", 0) & 0x400,
             "PHASE_CONTROL_SOURCE_REDIRECT")
        need(stat.S_ISDIR(metadata.st_mode) if item != path else
             stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
             "PHASE_CONTROL_SOURCE_KIND")
    need(0 < path.stat().st_size <= MIB, "PHASE_CONTROL_SOURCE_BOUND")
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == expected, "PHASE_CONTROL_SOURCE_PIN")
    module_name = "_dmkn_phase_control_worker"
    need(module_name not in sys.modules, "PHASE_CONTROL_MODULE_FRESH")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def scenario(worker, output, label, *, fail_phase=None, mutation=None, existing=False):
    check()
    directory = output/label
    directory.mkdir()
    sysroot, helpers = directory/"inert-runtime", directory/"inert-helpers"
    (sysroot/"bin").mkdir(parents=True)
    (sysroot/"lib/lean").mkdir(parents=True)
    helpers.mkdir()
    lean, source = sysroot/"bin/lean.exe", directory/"inert-native.lean"
    inventory, request = directory/"inventory.json", directory/"request.json"
    artifact, report = directory/"DMKNBridge_mock.olean", directory/"native-report.json"
    pending = report.with_name(report.name+".pending")
    trace = report.with_name(report.name+".phases.jsonl")
    parts = (artifact, Path(str(artifact)+".server"), Path(str(artifact)+".private"),
             artifact.with_suffix(".ir.sig"), artifact.with_suffix(".ir"))
    for path, raw in ((lean, b"INERT-NOT-EXECUTABLE"), (source, b"-- INERT-NOT-RUN"),
                      (inventory, b"[]"), (request, b"{}")):
        save(path, raw)
    if existing:
        save(report, b"PREEXISTING-DO-NOT-TOUCH")
    calls, produced = [], {}

    def mock_call(argv, **kwargs):
        check()
        need(argv[:6] == [str(lean), "-DElab.async=false", "-R", str(source.parent),
                          "--run", str(source)], "PHASE_CONTROL_EXACT_NATIVE_COMMAND")
        phase = argv[6]
        need(len(calls) < len(PHASES) and phase == PHASES[len(calls)],
             "PHASE_CONTROL_PHASE_ORDER")
        need(kwargs["stdin"] == subprocess.DEVNULL and
             kwargs["creationflags"] == subprocess.CREATE_NO_WINDOW and
             kwargs["cwd"] == Path.cwd() and
             kwargs["env"]["LEAN_PATH"] == os.pathsep.join(map(str, (sysroot/"lib/lean", helpers))),
             "PHASE_CONTROL_CHILD_PROFILE")
        expected = ((sysroot, inventory, request, artifact, pending) if phase == "build" else
                    (sysroot, request, artifact, pending))
        need(argv[7:] == list(map(str, expected)), "PHASE_CONTROL_PHASE_ARGUMENTS")
        calls.append(phase)
        if phase == fail_phase:
            return 7
        if phase == "build":
            for index, path in enumerate(parts):
                save(path, ("artifact-part-"+str(index)).encode("ascii"))
            produced.update(schema=worker.PENDING_SCHEMA, assurance=worker.PENDING_ASSURANCE,
                semantic_id="a"*64, context_root="b"*64, foundation_id="c"*64,
                module_name=[], targets=[], unit_ids=[], names=[], inventories=[],
                units_checked=0, checking_passes=2, basis_rows=581,
                artifact_parts=[{"path": str(path), "bytes": path.stat().st_size} for path in parts])
            save(pending, produced)
        if phase == "reread-private" and mutation is not None:
            selected = {"source": source, "inventory": inventory, "request": request,
                        "pending": pending, **{"part"+str(i): p for i, p in enumerate(parts)}}[mutation]
            raw = selected.read_bytes()
            # Change content WITHOUT changing size: hash checking, not stat alone,
            # must detect this. Only this scenario's inert fresh file is modified.
            changed = bytes([raw[0] ^ 1])+raw[1:]
            with selected.open("r+b") as handle:
                handle.write(changed)
                handle.flush()
        return 0

    expected_error = ("MODULE_WORKER_FRESH_OUTPUTS" if existing else
        "MODULE_WORKER_INPUT_CHANGED" if mutation in ("source", "inventory", "request") else
        "MODULE_WORKER_PHASE_OUTPUT_CHANGED" if mutation is not None else None)
    argv = list(map(str, (lean, source, helpers, sysroot, inventory, request, artifact, report)))
    with patch.object(subprocess, "call", mock_call):
        try:
            code = worker.main(argv)
        except ValueError as error:
            need(expected_error is not None and str(error) == expected_error,
                 "PHASE_CONTROL_WRONG_REFUSAL:"+str(error))
            code = None
        else:
            need(expected_error is None, "PHASE_CONTROL_MISSING_REFUSAL")
            need(code == (7 if fail_phase else 0), "PHASE_CONTROL_RETURN_CODE")
    if existing:
        need(calls == [] and not trace.exists() and
             report.read_bytes() == b"PREEXISTING-DO-NOT-TOUCH", "PHASE_CONTROL_EXISTING_UNCHANGED")
    else:
        expected_calls = (PHASES[:PHASES.index(fail_phase)+1] if fail_phase else
                          PHASES[:2] if mutation is not None else PHASES)
        need(calls == expected_calls, "PHASE_CONTROL_NO_LATER_PHASE")
        rows = [json.loads(line) for line in trace.read_bytes().splitlines()]
        expected_rows = []
        for phase in calls:
            for event, value in (("STARTED", None), ("EXITED", 7 if phase == fail_phase else 0)):
                expected_rows.append({"schema": "DMKN_ORDINARY_MODULE_PHASE_TRACE_V1",
                    "phase": phase, "event": event, "exit_code": value})
        need(rows == expected_rows, "PHASE_CONTROL_EXACT_PHASE_TRACE")
        if fail_phase or mutation:
            need(not report.exists(), "PHASE_CONTROL_FAILURE_CANNOT_FINALIZE")
        else:
            result = json.loads(report.read_bytes())
            expected_report = dict(produced)
            expected_report.update(schema="DMKN_ORDINARY_MODULE_OUTPUT_V1",
                assurance="LOCAL_CHECKED_MODULE_CONTROLLER_BOUND_IDENTITIES")
            need(result == expected_report and json.loads(pending.read_bytes()) == produced,
                 "PHASE_CONTROL_FINAL_SCHEMA_AND_RETAINED_PENDING")
            need(all(path.read_bytes() == ("artifact-part-"+str(i)).encode("ascii")
                     for i, path in enumerate(parts)), "PHASE_CONTROL_SUCCESS_PARTS_UNCHANGED")
    check()
    return {"case": label, "status": "PASS", "mocked_phases": calls,
            "expected_error": expected_error, "expected_native_exit": 7 if fail_phase else None}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", required=True)
    parser.add_argument("--worker-sha256", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PHASE_CONTROL_RUNTIME")
    output = Path(args.output)
    need(output.is_absolute() and ".." not in output.parts and output.is_relative_to(ROOT) and
         output.is_dir(), "PHASE_CONTROL_OUTPUT")
    fixtures = output/"phase-fixtures"
    need(not os.path.lexists(fixtures) and not os.path.lexists(output/"RESULTS.json"),
         "PHASE_CONTROL_FRESH_RESULTS")
    fixtures.mkdir()
    worker_path = Path(args.worker)
    with ExitStack() as guards:
        for owner, attribute in ((subprocess, "Popen"), (subprocess, "call"), (os, "system"),
                (os, "startfile"), (socket, "socket"), (socket, "create_connection"), (sqlite3, "connect")):
            guards.enter_context(patch.object(owner, attribute, forbidden))
        worker = load_worker(worker_path, args.worker_sha256)
        rows = [scenario(worker, fixtures, "three-phase-success")]
        for phase in PHASES:
            rows.append(scenario(worker, fixtures, "failure-"+phase, fail_phase=phase))
        for name in ("source", "inventory", "request", "pending", *("part"+str(i) for i in range(5))):
            rows.append(scenario(worker, fixtures, "mutation-"+name, mutation=name))
        rows.append(scenario(worker, fixtures, "existing-final", existing=True))
        need(len(rows) == 14 and hashlib.sha256(worker_path.read_bytes()).hexdigest() == args.worker_sha256,
             "PHASE_CONTROL_FINAL_SOURCE_AND_CENSUS")
    check()
    save(output/"RESULTS.json", {"status": "PASS", "scope": "MOCKED_THREE_PHASE_COMMIT_GATE_ONLY",
        "worker_sha256": args.worker_sha256, "cases": rows, "case_count": len(rows),
        "actual_child_processes": 0, "native_calls": 0, "owner_openings": 0,
        "database_calls": 0, "network_calls": 0, "mathematical_acceptance": False,
        "wall_seconds": time.monotonic()-START_WALL, "process_cpu_seconds": time.process_time()-START_CPU})


if __name__ == "__main__":
    main()

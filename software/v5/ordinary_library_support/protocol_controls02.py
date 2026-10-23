"""Five real-process controls of the installed extraction IPC supervisor.

Only tiny isolated Python children run; no Lean, exporter, owner, database or
network operation is allowed. Protocol names/results are inert synthetic data.
One original parent allowance accounts every child; unknown accounting is last
and conservatively reserved, never reported as measured CPU or mathematics.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import json
import os
import sys


def need(condition, code):
    if not condition:
        raise AssertionError(code)


def formal_name(text):
    return [[0, {"$bytes": list(part.encode("utf-8"))}] for part in text.split(".")]


def protocol_child(mode):
    """Small nonmathematical peer, reached before any package/test imports."""
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CHILD_PYTHON")
    need(mode in ("success", "bad-sequence", "trailing-frame", "idle", "unassigned"),
         "CHILD_MODE")
    def send(value):
        raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("ascii")+b"\n"
        sys.stdout.buffer.write(raw); sys.stdout.buffer.flush()
    def idle():
        until = time.monotonic()+10
        while time.monotonic() < until:
            time.sleep(0.05)
        raise AssertionError("CHILD_NOT_STOPPED")
    sys.stderr.buffer.write(b"synthetic-protocol-child\n"); sys.stderr.buffer.flush()
    if mode == "bad-sequence":
        send({"schema": "DMKN_ORDINARY_PARENT_LOOKUP_V1", "seq": 1,
              "name": formal_name("Protocol.Known")})
        idle()
    need(mode != "unassigned", "UNASSIGNED_CHILD_MUST_NEVER_RUN")
    for sequence, (label, symbol) in enumerate((("Protocol.Known", "1"*64),
                                                ("Protocol.Absent", None))):
        name = formal_name(label)
        send({"schema": "DMKN_ORDINARY_PARENT_LOOKUP_V1", "seq": sequence, "name": name})
        raw = sys.stdin.buffer.readline(4097)
        need(0 < len(raw) <= 4096 and raw.endswith(b"\n"), "CHILD_REPLY_BOUND")
        reply = json.loads(raw)
        expected = {"schema": "DMKN_ORDINARY_PARENT_REPLY_V1", "seq": sequence,
                    "name": name, "status": "FOUND" if symbol else "ABSENT"}
        if symbol:
            expected["symbol_id"] = symbol
        need(reply == expected, "CHILD_EXACT_REPLY")
    if mode == "idle":
        idle()
    done = {"schema": "DMKN_ORDINARY_MISSING_IMPORT_DONE_V1", "lookups": 2,
            "units": 1, "output_bytes": 1}
    send(done)
    if mode == "trailing-frame":
        send({"schema": "DMKN_ORDINARY_PARENT_LOOKUP_V1", "seq": 2,
              "name": formal_name("Protocol.Trailing")})
        idle()
    need(sys.stdin.buffer.read(1) == b"", "CHILD_EXPECTED_STDIN_EOF")
    return 0


if len(sys.argv) == 3 and sys.argv[1] == "--protocol-child":
    raise SystemExit(protocol_child(sys.argv[2]))

import argparse
from contextlib import ExitStack
import hashlib
import importlib.util
import math
from pathlib import Path
import socket
import sqlite3
import stat
import subprocess
import threading
from unittest.mock import patch

MIB = 1024**2
PROFILE = "1801fee2c3e9e39cef35182478acc693c923fef32ebb47ae2d7099d9a7776d3e"


def forbidden(*_, **__):
    raise AssertionError("PROTOCOL_CONTROL_FORBIDDEN_OPERATION")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, maximum=2*MIB, *, empty=False):
    need(path.is_absolute() and ".." not in path.parts, "PROTOCOL_CONTROL_ABSOLUTE_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "PROTOCOL_CONTROL_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PROTOCOL_CONTROL_REGULAR")
    size = path.stat().st_size
    need((empty or size > 0) and size <= maximum, "PROTOCOL_CONTROL_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "PROTOCOL_CONTROL_FILE_CHANGED")
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=True,
                     allow_nan=False, separators=(",", ":")).encode("ascii")
    need(0 < len(raw) <= MIB, "PROTOCOL_CONTROL_OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)
    return sha(raw)


class Allowance:
    deadline = START_WALL+70

    def __init__(self):
        self.measured_cpu, self.reserved_cpu, self.charges = 0.0, 0.0, []

    def check(self):
        need(time.monotonic() < self.deadline and
             time.process_time()-START_CPU+self.measured_cpu+self.reserved_cpu < 30,
             "PROTOCOL_CONTROL_ORIGINAL_ALLOWANCE")

    def budget(self, A):
        self.check()
        need(self.deadline-time.monotonic() >= 30, "PROTOCOL_CONTROL_REMAINING_WALL")
        remaining = math.floor(30-(time.process_time()-START_CPU)-self.measured_cpu-self.reserved_cpu)-1
        need(remaining >= 2, "PROTOCOL_CONTROL_REMAINING_CPU")
        return A.OperationBudget(30, remaining, 128, active_processes=2, log_bytes=4096)

    def charge(self, budget, mode):
        need(budget.claimed and mode not in [row["mode"] for row in self.charges],
             "PROTOCOL_CONTROL_SINGLE_CHARGE")
        if math.isfinite(budget.worker_cpu) and budget.worker_cpu >= 0:
            self.measured_cpu += budget.worker_cpu
            row = {"mode": mode, "measured_cpu_seconds": budget.worker_cpu,
                   "conservative_reservation_seconds": 0, "accounting_complete": True}
        else:
            # Preserve the charge even if an unexpected scenario loses its
            # accounting; subsequent assertions then fail that scenario.
            self.reserved_cpu += budget.cpu_seconds
            row = {"mode": mode, "measured_cpu_seconds": None,
                   "conservative_reservation_seconds": budget.cpu_seconds, "accounting_complete": False,
                   "expected_injected_unknown": mode == "unassigned" and math.isinf(budget.worker_cpu)}
        self.charges.append(row)


def selected_package(args, allowance):
    root = Path(args.package)
    raw = read(root/"PROFILE.json")
    need(args.profile_sha256 == PROFILE and sha(raw) == PROFILE, "PROTOCOL_CONTROL_PROFILE_PIN")
    descriptor = json.loads(raw)
    path, module_name = root/"owner.py", "_protocol_controls_owner"
    source, pin = read(path), descriptor["files"]["owner.py"]
    need(len(source) == pin["bytes"] and sha(source) == pin["sha256"] and
         module_name not in sys.modules, "PROTOCOL_CONTROL_CODE_PIN")
    spec = importlib.util.spec_from_file_location(module_name, path)
    owner = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = owner
    exec(compile(source, str(path), "exec"), owner.__dict__)
    loader = owner.bootstrap(root, PROFILE, allowance.check)
    loaded = loader.load(root, PROFILE,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        allowance.deadline, check_parent=allowance.check)
    need(loaded.library_extraction.A is loaded.A and loaded.library_extraction.X.A is loaded.A,
         "PROTOCOL_CONTROL_SHARED_CORE")
    return loaded


def run_case(mode, loaded, output, allowance):
    A, X, real_job = loaded.A, loaded.library_extraction.X, loaded.installation._job_module.Job
    budget = allowance.budget(A)
    directory = output/mode; directory.mkdir()
    script = A.C.ordinary(Path(__file__).absolute())
    script_pin = sha(read(script))
    argv = [str(loaded.installation.path("python")), "-I", "-S", "-B", str(script),
            "--protocol-child", mode]
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
    env["PATH"] = str(loaded.installation.runtime_roots["python_runtime"])
    processes, jobs, lookup_keys = [], [], []
    original_threads = set(threading.enumerate())
    cancel_at = cancel_observed = None
    report = result = caught = None
    actual_popen = subprocess.Popen

    def selected_popen(command, **keywords):
        need(command == argv and len(processes) == 0 and keywords == {
             "cwd": directory, "env": env, "stdin": subprocess.PIPE,
             "stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "bufsize": 0,
             "creationflags": 0x4 | subprocess.CREATE_NO_WINDOW}, "PROTOCOL_CONTROL_EXACT_CHILD")
        child = actual_popen(command, **keywords)
        processes.append(child)
        return child

    class UnassignedJob:
        def __init__(self, job):
            self.job = job
        def attach_resume(self, process):
            need(process.poll() is None, "PROTOCOL_CONTROL_SUSPENDED_CHILD")
            raise RuntimeError("CONTROL_SYNTHETIC_PREATTACH_FAILURE")
        def stats(self):
            return self.job.stats()
        def kill(self):
            return self.job.kill()
        def close(self):
            return self.job.close()

    def selected_job(*positional, **keywords):
        need(not jobs, "PROTOCOL_CONTROL_SINGLE_JOB")
        job = real_job(*positional, **keywords)
        jobs.append(job)
        return UnassignedJob(job) if mode == "unassigned" else job

    known, absent = (A.E.name_key(formal_name(label)) for label in ("Protocol.Known", "Protocol.Absent"))
    def lookup(key):
        nonlocal cancel_at
        need(key in (known, absent) and key not in lookup_keys, "PROTOCOL_CONTROL_LOOKUP")
        lookup_keys.append(key)
        if mode == "idle" and key == absent:
            # The first round trip is already complete. Cancel after a short
            # quiet interval, not relative to OS launch/import scheduling.
            cancel_at = time.monotonic()+0.15
        return "1"*64 if key == known else None

    def check_parent():
        nonlocal cancel_observed
        allowance.check()
        if cancel_at is not None and time.monotonic() >= cancel_at:
            cancel_observed = time.monotonic()
            raise RuntimeError("CONTROL_IDLE_CANCELLED")

    started = time.monotonic()
    try:
        with patch.object(subprocess, "Popen", selected_popen):
            try:
                result = X.exchange(argv, env=env, cwd=directory, output=directory,
                    lookup=lookup, parse=A._writer_json, name_key=A.E.name_key, budget=budget,
                    parent_deadline=allowance.deadline, check_parent=check_parent, job_type=selected_job)
                report = result[3]
            except X.ExchangeError as error:
                caught, report = error, error.report
    finally:
        if budget.claimed:
            allowance.charge(budget, mode)
    finished = time.monotonic()
    need(type(report) is dict, "PROTOCOL_CONTROL_REPORT_REQUIRED")
    stored = read(directory/"EXTRACTION-SUPERVISION.json", MIB)
    need(json.loads(stored) == report, "PROTOCOL_CONTROL_RETAINED_REPORT")
    need(len(processes) == len(jobs) == 1 and processes[0].poll() is not None and
         report["direct_child_reaped"] and report["child_exit_code"] == processes[0].returncode and
         report["job_closed"] and jobs[0].handle is None and report["threads_joined"] and
         not report["cleanup_errors"] and not (set(threading.enumerate())-original_threads),
         "PROTOCOL_CONTROL_REAL_CLEANUP")
    need(all(stream.closed for stream in (processes[0].stdin, processes[0].stdout, processes[0].stderr)),
         "PROTOCOL_CONTROL_CLOSED_PIPES")
    need(report["final_job"]["active_processes"] == 0 and budget.claimed and
         sha(read(script)) == script_pin, "PROTOCOL_CONTROL_QUIESCENCE_AND_SOURCE")
    need(report["protocol_limits"] == {"frame_bytes": MIB, "combined_bytes": 32*MIB,
         "stdin_log_bytes": 4096, "lookups": 65536, "stdout_log_bytes": 4096,
         "stderr_log_bytes": 4096} and report["limits"]["stdout_bytes"] == 4096 and
         report["limits"]["stderr_bytes"] == 4096, "PROTOCOL_CONTROL_ACTUAL_STREAM_CAPS")
    for filename in ("protocol.stdout.jsonl", "protocol.stdin.jsonl", "native.stderr.txt"):
        if (directory/filename).exists():
            read(directory/filename, 4096, empty=True)
    need(report["claim"] == "OPERATIONAL_REPORT_NOT_MATHEMATICAL_ACCEPTANCE",
         "PROTOCOL_CONTROL_NO_MATH_CLAIM")
    if mode == "unassigned":
        need(caught is not None and report["error"] == "CONTROL_SYNTHETIC_PREATTACH_FAILURE" and
             report["status"] == "EXTRACTION_FAILED" and report["termination_requested"] and
             not report["job_attach_resume_completed"] and report["final_job"]["total_processes"] == 0 and
             report["native_cpu_seconds"] is None and not report["accounting_complete"] and
             math.isinf(budget.worker_cpu) and report["lookups"] == 0,
             "PROTOCOL_CONTROL_UNASSIGNED_UNKNOWN_NOT_ZERO")
    else:
        need(report["job_attach_resume_completed"] and 1 <= report["final_job"]["total_processes"] <= budget.active_processes and
             report["accounting_complete"] and math.isfinite(report["native_cpu_seconds"]) and
             report["native_cpu_seconds"] >= 0 and budget.worker_cpu == report["native_cpu_seconds"] ==
             report["final_job"]["cpu_seconds"], "PROTOCOL_CONTROL_MEASURED_JOB_CPU")
        if mode == "success":
            need(caught is None and report["status"] == "EXTRACTED_AND_CLOSED" and
                 report["child_exit_code"] == 0 and not report["termination_requested"] and
                 report["final_job"]["terminated_processes"] == 0 and lookup_keys == [known, absent] and
                 result[:2] == ({"schema": "DMKN_ORDINARY_MISSING_IMPORT_DONE_V1", "lookups": 2,
                     "units": 1, "output_bytes": 1}, {known: "1"*64, absent: None}),
                 "PROTOCOL_CONTROL_SUCCESS_PROTOCOL")
            stdout = read(directory/"protocol.stdout.jsonl", 4096)
            stdin = read(directory/"protocol.stdin.jsonl", 4096)
            need(len(stdout.splitlines()) == 3 and len(stdin.splitlines()) == 2 and
                 result[2] == report["protocol_bytes"] == len(stdout)+len(stdin) and
                 report["stdin_log_bytes"] == len(stdin), "PROTOCOL_CONTROL_EXACT_TRANSCRIPTS")
        else:
            expected = {"bad-sequence": "EXCHANGE_LOOKUP_BINDING",
                        "trailing-frame": "EXCHANGE_TRAILING_STDOUT_FRAME",
                        "idle": "CONTROL_IDLE_CANCELLED"}[mode]
            need(caught is not None and report["status"] == "EXTRACTION_FAILED" and
                 report["error"] == expected and report["termination_requested"],
                 "PROTOCOL_CONTROL_EXACT_FAILURE")
        if mode == "idle":
            need(cancel_at is not None and cancel_observed is not None and
                 0 <= cancel_observed-cancel_at <= finished-cancel_at < 1,
                 "PROTOCOL_CONTROL_SUBSECOND_IDLE_CANCELLATION")
    allowance.check()
    return {"mode": mode, "ok": True, "child_pid": processes[0].pid,
            "wall_seconds": finished-started, "report_sha256": sha(stored),
            "native_cpu_seconds": report["native_cpu_seconds"],
            "accounting_complete": report["accounting_complete"],
            "cancellation_seconds_through_cleanup": None if cancel_at is None else finished-cancel_at,
            "synthetic_preassignment_fault": mode == "unassigned"}


def main(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PROTOCOL_CONTROL_PYTHON")
    allowance, rows = Allowance(), []
    with ExitStack() as guards:
        guards.enter_context(patch.object(sqlite3, "connect", forbidden))
        guards.enter_context(patch.object(socket.socket, "connect", forbidden))
        guards.enter_context(patch.object(socket.socket, "connect_ex", forbidden))
        with patch.object(subprocess, "Popen", forbidden):
            loaded = selected_package(args, allowance)
        guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, "open", forbidden))
        guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, "preflight", forbidden))
        guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, "admit", forbidden))
        guards.enter_context(patch.object(loaded.peer_api.H, "exchange", forbidden))
        guards.enter_context(patch.object(loaded.peer_api.H.Provider, "start", forbidden))
        output = loaded.A.C.ordinary(Path(args.output), directory=True)
        for protected in (loaded.root, *loaded.installation.runtime_roots.values()):
            need(not output.is_relative_to(protected) and not protected.is_relative_to(output),
                 "PROTOCOL_CONTROL_OUTPUT_OVERLAP")
        for mode in ("success", "bad-sequence", "trailing-frame", "idle", "unassigned"):
            try:
                rows.append(run_case(mode, loaded, output, allowance))
            except BaseException as error:
                rows.append({"mode": mode, "ok": False, "error_type": type(error).__name__,
                             "error": str(error)[:2000]})
                break  # Preserve failure/cost; no retry or more children after a failed gate.
    report = {"ok": len(rows) == 5 and all(row["ok"] for row in rows), "scenarios": rows,
        "profile_sha256": PROFILE, "implementation_id": loaded.installation.implementation_id,
        "charges": allowance.charges, "known_measured_child_cpu_seconds": allowance.measured_cpu,
        "conservative_unknown_cpu_reservation_seconds": allowance.reserved_cpu,
        "wall_seconds": time.monotonic()-START_WALL,
        "controller_cpu_seconds": time.process_time()-START_CPU,
        "lean_exporter_operations": 0, "owner_opens": 0,
        "claim": "REAL_PYTHON_IPC_AND_JOB_CONTROLS_NOT_LEAN_EXTRACTION_OR_MATHEMATICAL_ACCEPTANCE"}
    save(output/"PROTOCOL-CONTROLS.json", report)
    print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+argument, required=True)
    raise SystemExit(main(parser.parse_args()))

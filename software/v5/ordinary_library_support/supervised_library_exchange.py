"""Bounded installed-library IPC under the selected existing Windows Job.

Owner-selected executable/environment/cwd and pinned job_type are premises.
This is process containment, not hostile-binary isolation or mathematical
acceptance. No catalog is opened here. The current owner supplies point lookup.
Caller charges its parent ledger once in finally using budget.worker_cpu.
Unknown final native CPU poisons that field with infinity and always refuses;
the retained report distinguishes unknown accounting from measured zero.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import queue
import subprocess
import threading
import time

import ordinary_admission as A

MIB = 1024**2
FRAME_BYTES = MIB
PROTOCOL_BYTES = 32*MIB
POLL_SECONDS = 0.05


class ExchangeError(RuntimeError):
    def __init__(self, report):
        self.report = report
        super().__init__("LIBRARY_EXCHANGE_FAILED:"+report.get("error", report["status"]))


def need(condition, code):
    if not condition:
        raise ValueError(code)


def exchange(argv, *, env, cwd, output, lookup, parse, name_key, budget,
             parent_deadline, check_parent, job_type):
    """Return (DONE, reached answers, protocol bytes, clean supervision report).

    Exact unused OperationBudget is claimed once. Its allowance reserves cleanup
    before launch; idle IPC polls still check wall/controller/total native CPU.
    Existing Job supplies suspended attach, native memory/user-CPU/process caps
    and kill-on-close. Parent Python checks remain cooperative. Fresh diagnostic
    files survive every outcome; no result grants authority to its supplement.
    """
    need(os.name == "nt" and type(budget) is A.OperationBudget and not budget.claimed
         and budget.worker_cpu == 0 and type(parent_deadline) in (int, float)
         and math.isfinite(parent_deadline) and budget.deadline <= parent_deadline
         and all(callable(f) for f in (lookup, parse, name_key, check_parent, job_type)),
         "EXCHANGE_CONFIGURATION")
    need(type(argv) is list and 1 <= len(argv) <= 16 and
         all(type(item) is str and 0 < len(item) <= 32768 and "\x00" not in item for item in argv)
         and sum(len(item)+3 for item in argv) <= 30000, "EXCHANGE_ARGV")
    need(type(env) is dict and len(env) <= 4096 and all(type(k) is str and type(v) is str
         and k and "=" not in k and "\x00" not in k+v for k, v in env.items())
         and sum(len(k)+len(v)+2 for k, v in env.items()) <= 131072, "EXCHANGE_ENVIRONMENT")
    cwd = A.C.ordinary(Path(cwd), directory=True)
    output = A.C.ordinary(Path(output), directory=True)
    A.C.ordinary(Path(argv[0]))
    names = ("protocol.stdout.jsonl", "protocol.stdin.jsonl", "native.stderr.txt", "EXTRACTION-SUPERVISION.json")
    for filename in names:
        A.C.ordinary(output/filename, fresh=True)

    started, controller_cpu_started = time.monotonic(), time.process_time()
    cleanup_deadline = min(parent_deadline, budget.deadline)
    report = {"schema": "DMKN_ORDINARY_LIBRARY_EXTRACTION_SUPERVISION_V1",
        "status": "EXTRACTION_FAILED", "argv": list(argv), "cwd": str(cwd),
        "claim": "OPERATIONAL_REPORT_NOT_MATHEMATICAL_ACCEPTANCE",
        "child_exit_code": None, "direct_child_reaped": False, "job_closed": False,
        "job_attach_resume_completed": False,
        "threads_joined": False, "termination_requested": False, "cleanup_errors": [],
        "last_observed_job": None, "final_job": None, "native_cpu_seconds": None,
        "accounting_complete": False, "limits": None,
        "protocol_limits": {"frame_bytes": FRAME_BYTES, "combined_bytes": PROTOCOL_BYTES,
                            "stdin_log_bytes": budget.log_bytes, "lookups": 65536},
        "containment": "EXISTING_JOB_USER_CPU_MEMORY_PROCESS_CAPS_SAMPLED_TOTAL_CPU_AND_WALL",
        "controller_scope": "COOPERATIVE_PARENT_CHECKS_NOT_HARD_CONTROLLER_MEMORY_LIMIT"}
    job = process = grant = None
    threads = []
    thread_faults = []
    stop = threading.Event()
    events, writes = queue.Queue(8), queue.Queue(1)
    answers, done, eof = {}, None, set()
    sequence = protocol_bytes = stdin_bytes = 0
    fault = None
    phase = "ALLOCATION"
    active_deadline = cleanup_deadline

    def sample():
        observed = job.stats()
        need(type(observed) is dict and type(observed.get("cpu_seconds")) in (int, float)
             and math.isfinite(observed["cpu_seconds"]) and observed["cpu_seconds"] >= 0
             and all(type(observed.get(key)) is int and observed[key] >= 0
                     for key in ("active_processes", "total_processes", "terminated_processes")),
             "EXCHANGE_JOB_ACCOUNTING")
        report["last_observed_job"] = observed
        return observed

    def check():
        check_parent()
        budget.check()
        need(time.monotonic() < active_deadline, "EXCHANGE_ORIGINAL_DEADLINE")
        if job is not None:
            observed = sample()
            need(observed["cpu_seconds"] <= grant["cpu_seconds"] and
                 time.process_time()-budget.cpu_started+observed["cpu_seconds"] < budget.cpu_seconds,
                 "EXCHANGE_ORIGINAL_TOTAL_CPU")

    def emit(event):
        while not stop.is_set():
            try:
                events.put(event, timeout=POLL_SECONDS)
                return
            except queue.Full:
                pass

    def thread_error(error):
        # Preserve failures even if cleanup has stopped queue publication.
        thread_faults.append(error)
        emit(("error", error))

    def reader():
        try:
            with (output/"protocol.stdout.jsonl").open("xb") as log:
                total = 0
                while not stop.is_set():
                    raw = process.stdout.readline(FRAME_BYTES+2)
                    if not raw:
                        break
                    total += len(raw)
                    need(total <= min(PROTOCOL_BYTES, grant["stdout_bytes"]) and raw.endswith(b"\n") and
                         1 < len(raw) <= FRAME_BYTES+1, "EXCHANGE_STDOUT_BOUND")
                    log.write(raw)
                    emit(("frame", raw))
            emit(("stdout_eof", None))
        except BaseException as error:
            thread_error(error)

    def stderr_reader():
        try:
            with (output/"native.stderr.txt").open("xb") as log:
                total, tail = 0, b""
                while not stop.is_set():
                    chunk = process.stderr.read(4096)
                    if not chunk:
                        break
                    total += len(chunk)
                    need(total <= min(MIB, grant["stderr_bytes"]), "EXCHANGE_STDERR_BOUND")
                    need(b"PANIC" not in (tail+chunk).upper(), "EXCHANGE_NATIVE_PANIC")
                    tail = chunk[-4:]
                    log.write(chunk)
            emit(("stderr_eof", None))
        except BaseException as error:
            thread_error(error)

    def writer():
        try:
            while not stop.is_set():
                try:
                    raw = writes.get(timeout=POLL_SECONDS)
                except queue.Empty:
                    continue
                if raw is None:
                    process.stdin.close()
                    return
                view = memoryview(raw)
                while view and not stop.is_set():
                    count = process.stdin.write(view)
                    need(count is not None and count > 0, "EXCHANGE_PIPE_WRITE")
                    view = view[count:]
                process.stdin.flush()
        except BaseException as error:
            thread_error(error)

    def enqueue(raw):
        while True:
            check()
            try:
                writes.put(raw, timeout=min(POLL_SECONDS, max(0, active_deadline-time.monotonic())))
                return
            except queue.Full:
                pass

    try:
        check_parent(); budget.check()
        grant = budget.allowance(parent_deadline)
        active_deadline = min(started+grant["wall_seconds"], cleanup_deadline)
        report["limits"] = dict(grant)
        report["protocol_limits"].update(stdout_log_bytes=min(PROTOCOL_BYTES, grant["stdout_bytes"]),
                                         stderr_log_bytes=min(MIB, grant["stderr_bytes"]))
        budget.claim()
        check()
        phase = "LAUNCH"
        job = job_type(grant["cpu_seconds"], grant["memory_mib"],
                       active_processes=grant["active_processes"])
        # No uncontained child may run before Job assignment. If assignment or
        # resume fails, finally also kills/reaps the direct suspended process.
        process = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0,
            creationflags=0x4 | subprocess.CREATE_NO_WINDOW)
        job.attach_resume(process)
        report["job_attach_resume_completed"] = True
        phase = "PROTOCOL"
        for target in (reader, stderr_reader, writer):
            thread = threading.Thread(target=target, daemon=True)
            threads.append(thread); thread.start()
        with (output/"protocol.stdin.jsonl").open("xb") as transcript:
            while len(eof) != 2:
                check()
                try:
                    kind, value = events.get(timeout=min(POLL_SECONDS, max(0, active_deadline-time.monotonic())))
                except queue.Empty:
                    continue
                if kind == "error":
                    raise value
                if kind in ("stdout_eof", "stderr_eof"):
                    need(kind not in eof and (kind != "stdout_eof" or done is not None),
                         "EXCHANGE_PREMATURE_OR_DUPLICATE_EOF")
                    eof.add(kind)
                    continue
                need(kind == "frame" and done is None, "EXCHANGE_TRAILING_STDOUT_FRAME")
                protocol_bytes += len(value)
                need(protocol_bytes <= PROTOCOL_BYTES, "EXCHANGE_PROTOCOL_BYTES")
                frame = parse(value[:-1], FRAME_BYTES)
                check()
                need(type(frame) is dict, "EXCHANGE_PROTOCOL_OBJECT")
                if frame.get("schema") == "DMKN_ORDINARY_MISSING_IMPORT_DONE_V1":
                    need(set(frame) == {"schema", "lookups", "units", "output_bytes"}
                         and type(frame["lookups"]) is int and frame["lookups"] == sequence
                         and type(frame["units"]) is int and 1 <= frame["units"] <= 1024
                         and type(frame["output_bytes"]) is int and 0 < frame["output_bytes"] <= 64*MIB,
                         "EXCHANGE_DONE_BINDING")
                    done = frame
                    enqueue(None)
                    continue
                need(set(frame) == {"schema", "seq", "name"}
                     and frame["schema"] == "DMKN_ORDINARY_PARENT_LOOKUP_V1"
                     and type(frame["seq"]) is int and frame["seq"] == sequence and sequence < 65536,
                     "EXCHANGE_LOOKUP_BINDING")
                key = name_key(frame["name"])
                need(type(key) is bytes and 0 < len(key) <= 65536 and key not in answers,
                     "EXCHANGE_DUPLICATE_OR_UNBOUNDED_LOOKUP")
                symbol = lookup(key)
                check()
                need(symbol is None or type(symbol) is str, "EXCHANGE_LOOKUP_RESULT")
                if symbol is not None:
                    A.C.hexid(symbol)
                answers[key] = symbol
                response = {"schema": "DMKN_ORDINARY_PARENT_REPLY_V1", "seq": sequence,
                    "name": frame["name"], "status": "FOUND" if symbol is not None else "ABSENT"}
                if symbol is not None:
                    response["symbol_id"] = symbol
                raw = json.dumps(response, separators=(",", ":"), ensure_ascii=True).encode("ascii")+b"\n"
                protocol_bytes += len(raw)
                stdin_bytes += len(raw)
                need(len(raw) <= FRAME_BYTES+1 and protocol_bytes <= PROTOCOL_BYTES,
                     "EXCHANGE_REPLY_BYTE_BOUND")
                need(stdin_bytes <= budget.log_bytes, "EXCHANGE_STDIN_LOG_BOUND")
                transcript.write(raw)
                enqueue(raw)
                sequence += 1
        phase = "EXIT"
        while process.poll() is None:
            check()
            try:
                process.wait(timeout=min(POLL_SECONDS, max(0, active_deadline-time.monotonic())))
            except subprocess.TimeoutExpired:
                pass
        need(process.returncode == 0, "EXCHANGE_NATIVE_EXIT_REQUIRED")
        # A child can close both pipes and leave a descendant. Permit only a
        # short natural settlement inside the active allowance, then refuse.
        settle = min(active_deadline, time.monotonic()+1)
        while True:
            check()
            observed = report["last_observed_job"]
            if observed["active_processes"] == 0:
                break
            need(time.monotonic() < settle, "EXCHANGE_ACTIVE_DESCENDANTS")
            time.sleep(min(POLL_SECONDS, max(0, settle-time.monotonic())))
        need(observed["terminated_processes"] == 0, "EXCHANGE_NATIVE_TERMINATION")
    except BaseException as error:
        fault = error
        report.update(phase=phase, error_type=type(error).__name__, error=str(error)[:2000])
    finally:
        # The remaining part of the original allowance is cleanup, not a reset.
        stop.set()
        if fault is not None:
            if job is not None:
                try:
                    job.kill(); report["termination_requested"] = True
                except BaseException as error:
                    report["cleanup_errors"].append("job.kill:"+type(error).__name__)
            if process is not None:
                try:
                    if process.poll() is None:
                        process.kill(); report["termination_requested"] = True
                except BaseException as error:
                    report["cleanup_errors"].append("direct.kill:"+type(error).__name__)
        if process is not None:
            try:
                process.wait(timeout=max(0, min(5, cleanup_deadline-time.monotonic())))
                report["child_exit_code"] = process.returncode
                report["direct_child_reaped"] = True
            except BaseException as error:
                report["cleanup_errors"].append("direct.wait:"+type(error).__name__)
        for thread in threads:
            try:
                thread.join(timeout=max(0, min(2, cleanup_deadline-time.monotonic())))
            except BaseException as error:
                report["cleanup_errors"].append("thread.join:"+type(error).__name__)
        report["threads_joined"] = all(not thread.is_alive() for thread in threads)
        if not report["threads_joined"]:
            report["cleanup_errors"].append("threads.alive")
        if thread_faults and fault is None:
            fault = thread_faults[0]
            report.update(phase="PIPE_THREAD", error_type=type(fault).__name__, error=str(fault)[:2000])
        # Reader/writer errors queued just after their peer EOF must not vanish.
        while True:
            try:
                kind, value = events.get_nowait()
            except queue.Empty:
                break
            if fault is None:
                fault = value if kind == "error" else ValueError("EXCHANGE_UNCONSUMED_EVENT:"+kind)
                report.update(phase="CLEANUP", error_type=type(fault).__name__, error=str(fault)[:2000])
        if process is not None:
            for label, stream in (("stdin", process.stdin), ("stdout", process.stdout), ("stderr", process.stderr)):
                try:
                    if stream is not None and not stream.closed:
                        stream.close()
                except BaseException as error:
                    report["cleanup_errors"].append(label+".close:"+type(error).__name__)
        if job is not None:
            try:
                while True:
                    observed = sample()
                    report["final_job"] = observed
                    if observed["active_processes"] == 0:
                        break
                    if time.monotonic() >= cleanup_deadline:
                        raise ValueError("EXCHANGE_CLEANUP_ACTIVE_DESCENDANTS")
                    # Cleanup after a late pipe fault also kills the whole Job.
                    job.kill(); report["termination_requested"] = True
                    time.sleep(min(POLL_SECONDS, max(0, cleanup_deadline-time.monotonic())))
            except BaseException as error:
                report["cleanup_errors"].append("job.quiesce:"+type(error).__name__)
            try:
                job.close(); report["job_closed"] = True
            except BaseException as error:
                report["cleanup_errors"].append("job.close:"+type(error).__name__)
        final = report["final_job"]
        # A fresh empty Job does not account a child whose assignment failed.
        # A live/unreaped child also makes a pre-close CPU sample incomplete.
        accounting = (final is not None and final["active_processes"] == 0
                      and final["total_processes"] >= 1 and report["direct_child_reaped"])
        if process is None:
            accounting, native_cpu = True, 0.0
        elif accounting:
            native_cpu = final["cpu_seconds"]
        else:
            native_cpu = None
        if budget.claimed:
            budget.worker_cpu += native_cpu if accounting else math.inf
        report["native_cpu_seconds"], report["accounting_complete"] = native_cpu, accounting
        report["protocol_bytes"], report["lookups"] = protocol_bytes, sequence
        report["stdin_log_bytes"] = stdin_bytes
        report["done"] = done
        report["wall_seconds_through_cleanup"] = time.monotonic()-started
        report["controller_cpu_seconds"] = time.process_time()-controller_cpu_started

    clean = fault is None and done is not None and eof == {"stdout_eof", "stderr_eof"}
    clean = clean and report["direct_child_reaped"] and report["child_exit_code"] == 0
    clean = clean and report["job_closed"] and report["threads_joined"] and not report["cleanup_errors"]
    clean = clean and report["accounting_complete"] and report["final_job"]["active_processes"] == 0
    clean = clean and report["final_job"]["terminated_processes"] == 0 and not report["termination_requested"]
    if clean:
        try:
            check_parent(); budget.check()
            need(time.monotonic() < cleanup_deadline and budget.worker_cpu <= grant["cpu_seconds"],
                 "EXCHANGE_FINAL_ALLOWANCE")
        except BaseException as error:
            clean, fault = False, error
            report.update(phase="FINAL_BUDGET", error_type=type(error).__name__, error=str(error)[:2000])
    report["status"] = "EXTRACTED_AND_CLOSED" if clean else "EXTRACTION_FAILED"
    if not clean and fault is None:
        fault = ValueError("EXCHANGE_CLEANUP_OR_ACCOUNTING_UNCERTAIN")
        report.update(phase="CLEANUP", error_type=type(fault).__name__, error=str(fault))
    try:
        raw = json.dumps(report, sort_keys=True, ensure_ascii=True, allow_nan=False).encode("ascii")
        need(len(raw) <= MIB, "EXCHANGE_REPORT_BOUND")
        A.P.PortableCatalog._write_fresh(output/"EXTRACTION-SUPERVISION.json", raw)
    except BaseException as error:
        report["status"] = "EXTRACTION_FAILED"
        report["report_write_error"] = type(error).__name__+":"+str(error)[:1000]
        raise ExchangeError(report) from error
    if not clean:
        raise ExchangeError(report) from fault
    return done, answers, protocol_bytes, report

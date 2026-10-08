"""Request-scoped owner-controlled stage runner; no global history census.

Not a peer-input API, a general sandbox, or mathematical acceptance authority.
All commands are supplied by the node operator as a recorded JSON plan.
Windows Job containment limits child lifetime, private commit and process count.
Polling CPU/time/output caps can overshoot; such attempts never pass the envelope.
"""

from __future__ import annotations

import argparse
import ctypes as C
from ctypes import wintypes as W
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

import domains as domain_module
from domains import Domains, PYTHON_FLAGS, require_python_profile

MAX_RECEIPT_BYTES = 1024 * 1024
MAX_STAGE_ENTRIES = 4096
UTC = lambda: datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for data in iter(lambda: f.read(1024 * 1024), b""):
            h.update(data)
    return h.hexdigest()


def size_tree(path: Path) -> int:
    if not path.is_dir():
        raise FileNotFoundError(f"census root missing: {path}")
    total = 0
    for number, p in enumerate(path.rglob("*"), 1):
        if number > MAX_STAGE_ENTRIES or not p.resolve().is_relative_to(path.resolve()):
            raise RuntimeError("SELECTED_STAGE_ENTRY_OR_PATH_LIMIT")
        try:
            if p.is_file():
                total += p.stat().st_size
        except FileNotFoundError:
            # A compiler may rename/remove a temporary output between discovery
            # and stat. It is absent at this observation; retained bytes are
            # counted at the next poll and the quiescent final census.
            continue
    return total


def selected_output_files(path: Path, stage_dir: Path) -> list[Path]:
    files = []
    for number, entry in enumerate(path.rglob("*"), 1):
        if number > MAX_STAGE_ENTRIES or not entry.resolve().is_relative_to(stage_dir):
            raise RuntimeError("SELECTED_OUTPUT_ENTRY_OR_PATH_LIMIT")
        if entry.is_file():
            files.append(entry)
    return sorted(files)


def record_file(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": digest(path)}


def save(path: Path, obj: dict) -> None:
    # The experiment deliberately retains unfinished/error records as well.
    raw = (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    if len(raw) > MAX_RECEIPT_BYTES:
        raise RuntimeError("RECEIPT_BYTE_LIMIT")
    with path.open("wb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def inside(path: Path, parent: Path) -> Path:
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(parent.resolve()):
        raise ValueError(f"path outside declared input domain: {path}")
    return resolved


def relative_destination(text: str, parent: Path) -> Path:
    rel = Path(text)
    if (rel.is_absolute() or rel.drive or rel.root or ".." in rel.parts or not rel.parts
            or any(":" in part or part.endswith((".", " "))
                   or os.path.isreserved(part) for part in rel.parts)):
        raise ValueError("invalid relative snapshot/output path")
    result = parent / rel
    if not result.resolve().is_relative_to(parent.resolve()):
        raise ValueError("relative path escapes its declared directory")
    return result


class BasicLimits(C.Structure):
    _fields_ = [("PerProcessUserTimeLimit", C.c_longlong), ("PerJobUserTimeLimit", C.c_longlong),
                ("LimitFlags", W.DWORD), ("MinimumWorkingSetSize", C.c_size_t),
                ("MaximumWorkingSetSize", C.c_size_t), ("ActiveProcessLimit", W.DWORD),
                ("Affinity", C.c_size_t), ("PriorityClass", W.DWORD), ("SchedulingClass", W.DWORD)]


class IOCounters(C.Structure):
    _fields_ = [(s, C.c_ulonglong) for s in ("ReadOperationCount", "WriteOperationCount",
                "OtherOperationCount", "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]


class ExtendedLimits(C.Structure):
    _fields_ = [("BasicLimitInformation", BasicLimits), ("IoInfo", IOCounters),
                ("ProcessMemoryLimit", C.c_size_t), ("JobMemoryLimit", C.c_size_t),
                ("PeakProcessMemoryUsed", C.c_size_t), ("PeakJobMemoryUsed", C.c_size_t)]


class Accounting(C.Structure):
    _fields_ = [("TotalUserTime", C.c_longlong), ("TotalKernelTime", C.c_longlong),
                ("ThisPeriodTotalUserTime", C.c_longlong), ("ThisPeriodTotalKernelTime", C.c_longlong),
                ("TotalPageFaultCount", W.DWORD), ("TotalProcesses", W.DWORD),
                ("ActiveProcesses", W.DWORD), ("TotalTerminatedProcesses", W.DWORD)]


class Job:
    def __init__(self, seconds: int, memory_mib: int, active_processes: int = 1):
        if os.name != "nt":
            raise RuntimeError("this experiment's resource backend requires Windows")
        if type(active_processes) is not int or not 1 <= active_processes <= 8:
            raise ValueError("invalid Job active-process bound")
        self.k = C.WinDLL("kernel32", use_last_error=True)
        self.n = C.WinDLL("ntdll", use_last_error=True)
        self.k.CreateJobObjectW.argtypes = [C.c_void_p, W.LPCWSTR]
        self.k.CreateJobObjectW.restype = W.HANDLE
        self.k.SetInformationJobObject.argtypes = [W.HANDLE, C.c_int, C.c_void_p, W.DWORD]
        self.k.SetInformationJobObject.restype = W.BOOL
        self.k.QueryInformationJobObject.argtypes = [W.HANDLE, C.c_int, C.c_void_p, W.DWORD, C.c_void_p]
        self.k.QueryInformationJobObject.restype = W.BOOL
        self.k.AssignProcessToJobObject.argtypes = [W.HANDLE, W.HANDLE]
        self.k.AssignProcessToJobObject.restype = W.BOOL
        self.k.TerminateJobObject.argtypes = [W.HANDLE, W.UINT]
        self.k.TerminateJobObject.restype = W.BOOL
        self.k.CloseHandle.argtypes = [W.HANDLE]
        self.k.CloseHandle.restype = W.BOOL
        self.n.NtResumeProcess.argtypes = [W.HANDLE]
        self.n.NtResumeProcess.restype = C.c_long
        self.handle = self.k.CreateJobObjectW(None, None)
        if not self.handle:
            raise C.WinError(C.get_last_error())
        limits = ExtendedLimits()
        # JOB_TIME | ACTIVE_PROCESS | JOB_MEMORY | KILL_ON_JOB_CLOSE.
        limits.BasicLimitInformation.LimitFlags = 0x4 | 0x8 | 0x200 | 0x2000
        limits.BasicLimitInformation.PerJobUserTimeLimit = seconds * 10_000_000
        limits.BasicLimitInformation.ActiveProcessLimit = active_processes
        limits.JobMemoryLimit = memory_mib * 1024 * 1024
        if not self.k.SetInformationJobObject(self.handle, 9, C.byref(limits), C.sizeof(limits)):
            err = C.WinError(C.get_last_error())
            self.close()
            raise err

    def attach_resume(self, p: subprocess.Popen) -> None:
        if not self.k.AssignProcessToJobObject(self.handle, W.HANDLE(int(p._handle))):
            raise C.WinError(C.get_last_error())
        if self.n.NtResumeProcess(W.HANDLE(int(p._handle))) != 0:
            raise RuntimeError("NtResumeProcess failed; process remains untrusted/unstarted")

    def stats(self) -> dict:
        a, m = Accounting(), ExtendedLimits()
        if not self.k.QueryInformationJobObject(self.handle, 1, C.byref(a), C.sizeof(a), None):
            raise C.WinError(C.get_last_error())
        if not self.k.QueryInformationJobObject(self.handle, 9, C.byref(m), C.sizeof(m), None):
            raise C.WinError(C.get_last_error())
        return {"user_cpu_seconds": a.TotalUserTime / 1e7,
                "kernel_cpu_seconds": a.TotalKernelTime / 1e7,
                "cpu_seconds": (a.TotalUserTime + a.TotalKernelTime) / 1e7,
                "active_processes": a.ActiveProcesses, "total_processes": a.TotalProcesses,
                "terminated_processes": a.TotalTerminatedProcesses,
                "peak_job_private_commit_bytes": m.PeakJobMemoryUsed}

    def kill(self) -> None:
        if not self.k.TerminateJobObject(self.handle, 1):
            raise C.WinError(C.get_last_error())

    def close(self) -> None:
        if getattr(self, "handle", None):
            if not self.k.CloseHandle(self.handle):
                # Retain the handle and surface uncertainty on failed release.
                raise C.WinError(C.get_last_error())
            self.handle = None


def execute(plan_path: Path, directory: Path, stage: str, expected_plan_sha256: str) -> int:
    started = time.monotonic()
    require_python_profile()
    if not stage or len(stage) > 64 or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for ch in stage):
        raise ValueError("STAGE_ID")
    if (type(expected_plan_sha256) is not str or len(expected_plan_sha256) != 64
            or any(ch not in "0123456789abcdefABCDEF" for ch in expected_plan_sha256)):
        raise ValueError("EXPECTED_PLAN_HASH")
    # Authenticate the owner-created plan and all path domains before any write.
    if not plan_path.is_absolute():
        raise ValueError("PLAN_ABSOLUTE_PATH_REQUIRED")
    plan_path = plan_path.resolve(strict=True)
    with plan_path.open("rb") as stream:
        plan_raw = stream.read(64 * 1024 * 1024 + 1)
    if (len(plan_raw) > 64 * 1024 * 1024
            or hashlib.sha256(plan_raw).hexdigest() != expected_plan_sha256.lower()):
        raise ValueError("REVIEWED_PLAN_HASH_MISMATCH")
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("DUPLICATE_PLAN_KEY")
            result[key] = value
        return result
    def nonfinite(_):
        raise ValueError("NONFINITE_PLAN")
    plan = json.loads(plan_raw, object_pairs_hook=pairs, parse_constant=nonfinite)
    domains = Domains.from_stage_plan(plan)
    if plan["domains"] != domains.as_dict():
        raise ValueError("NONCANONICAL_PLAN_DOMAINS")
    request_directory = domains.require_work(plan["request_directory"])
    stage_dir = domains.require_stage(directory, request_directory)
    if (str(stage_dir) != plan["stage_directory"] or stage != plan["stage"]
            or str(request_directory) != plan["request_directory"] or stage_dir.exists()):
        raise ValueError("NEW_BOUND_STAGE_REQUIRED")
    if plan_path == request_directory or not plan_path.is_relative_to(request_directory):
        raise ValueError("SELECTED_REQUEST_PLAN_DOMAIN")
    source_pin = plan["domains_source"]
    if type(source_pin) is not dict or set(source_pin) != {"path", "bytes", "sha256"}:
        raise ValueError("DOMAINS_PIN_FIELDS")
    source_path = domains.require_read(source_pin["path"])
    if (source_path != domains.install / "py" / "domains.py"
            or source_path != Path(domain_module.__file__).resolve()
            or type(source_pin["bytes"]) is not int or source_path.stat().st_size != source_pin["bytes"]
            or digest(source_path) != source_pin["sha256"].lower()):
        raise ValueError("DOMAINS_SOURCE_PIN")
    runner_path = domains.require_read(Path(__file__).resolve())
    if (runner_path != domains.install / "py" / "run_stage.py"
            or digest(runner_path) != plan["expected_runner_sha256"].lower()):
        raise ValueError("RUNNER_INSTALLED_SOURCE_PIN")
    LEAN = domains.require_lean(plan["lean"]["path"])
    RUNTIME = domains.lean_runtime
    if (set(plan["lean"]) != {"path", "bytes", "sha256"}
            or type(plan["lean"]["bytes"]) is not int
            or LEAN.stat().st_size != plan["lean"]["bytes"]
            or digest(LEAN) != plan["lean"]["sha256"].lower()):
        raise ValueError("LEAN_PIN")
    actual_python = record_file(Path(sys.executable).resolve(strict=True))
    if (set(plan["python"]) != {"path", "bytes", "sha256"}
            or Path(plan["python"]["path"]).resolve(strict=True) != Path(sys.executable).resolve(strict=True)
            or type(plan["python"]["bytes"]) is not int
            or plan["python"]["bytes"] != actual_python["bytes"]
            or plan["python"]["sha256"].lower() != actual_python["sha256"]):
        raise ValueError("PYTHON_PIN")
    seconds, memory_mib, LIMIT_BYTES = plan["seconds"], plan["memory_mib"], plan["bytes"]
    if type(seconds) is not int or not 1 <= seconds <= 300:
        raise ValueError("invalid stage seconds")
    if type(memory_mib) is not int or not 1 <= memory_mib <= 4096:
        raise ValueError("invalid private-commit limit")
    if type(LIMIT_BYTES) is not int or not 1 <= LIMIT_BYTES <= 512 * 1024 * 1024:
        raise ValueError("invalid selected stage byte allowance")
    inputs = plan.get("inputs")
    if type(inputs) is not list or not 1 <= len(inputs) <= 64:
        raise ValueError("STAGE_INPUT_COUNT")
    bound_domains = [item for item in inputs if item.get("as") == "domains.py"]
    if bound_domains != [{**source_pin, "as": "domains.py"}]:
        raise ValueError("STAGE_DOMAINS_SNAPSHOT_BINDING")
    job, process = None, None
    owns_stage = False
    quiescent = True
    lock = stage_dir / "ACTIVE.lock"
    record = {"started_utc": UTC(), "stage": stage, "steps": [],
              "status": "PREPARING", "authority": "COOPERATIVE_OWNER_LOCAL_NOT_PEER_SOURCE",
              "domains": domains.as_dict(), "request_directory": str(request_directory),
              "accounting_root": str(stage_dir), "retained_bytes_scope": "SELECTED_STAGE_ONLY"}
    record_path = stage_dir / "stage.json"
    try:
        stage_dir.mkdir(parents=True, exist_ok=False)
        owns_stage = True
        with lock.open("xb") as stream:
            stream.write(str(os.getpid()).encode("ascii"))
        save(record_path, record)
        with (stage_dir / "plan.json").open("xb") as stream:
            stream.write(plan_raw)
            stream.flush()
        shutil.copy2(runner_path, stage_dir / "run_stage.py")
        if digest(stage_dir / "plan.json") != expected_plan_sha256.lower():
            raise RuntimeError("REVIEWED_PLAN_SNAPSHOT_HASH_MISMATCH")
        if digest(stage_dir / "run_stage.py") != plan["expected_runner_sha256"].lower():
            raise RuntimeError("REVIEWED_RUNNER_SNAPSHOT_HASH_MISMATCH")
        record["expected_plan_sha256"] = expected_plan_sha256.lower()
        record["lean"] = record_file(LEAN)
        record["python"] = record_file(Path(sys.executable))
        record["runner"] = record_file(stage_dir / "run_stage.py")
        record["plan"] = record_file(stage_dir / "plan.json")
        record["inputs"] = []
        input_names = set()
        for item in inputs:
            src = domains.require_read(item["path"])
            if not src.is_file():
                raise ValueError("only explicitly listed input files may be snapshotted")
            rel = Path(item["as"])
            dst = relative_destination(item["as"], stage_dir / "input")
            name = str(rel).casefold()
            if name in input_names:
                raise ValueError("duplicate input snapshot name")
            input_names.add(name)
            if dst.exists():
                raise ValueError("input snapshot escapes its directory or overwrites an existing file")
            if size_tree(stage_dir) + src.stat().st_size > LIMIT_BYTES:
                raise RuntimeError("SELECTED_STAGE_STAGING_LIMIT_BEFORE_COPY")
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            row = record_file(dst)
            row["source"] = str(src)
            record["inputs"].append(row)
            if row["sha256"] != item["sha256"].lower() or row["bytes"] != item["bytes"]:
                raise RuntimeError(f"REVIEWED_INPUT_SNAPSHOT_MISMATCH: {item['as']}")
        (stage_dir / "out").mkdir()
        for directory in plan.get("output_directories", []):
            relative_destination(directory, stage_dir / "out").mkdir(parents=True, exist_ok=False)
        substitutions = {"$RUN": str(stage_dir), "$RUNTIME": str(RUNTIME)}

        def expand(text: str) -> str:
            for key, val in substitutions.items():
                text = text.replace(key, val)
            return text

        env = os.environ.copy()
        for key in ("LEAN_PATH", "LEAN_SRC_PATH", "LEAN_SYSROOT", "PYTHONPATH", "PYTHONHOME"):
            env.pop(key, None)
        env["LEAN_SYSROOT"] = str(RUNTIME)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        record["limits"] = {"stage_wall_seconds": seconds, "stage_aggregate_cpu_seconds": seconds,
                            "job_private_commit_mib": memory_mib, "job_active_processes": 1,
                            "selected_stage_staging_bytes": LIMIT_BYTES, "poll_seconds": 0.05}
        record["limitations"] = ["Runtime and owner tools remain trusted; not hostile-code filesystem/network isolation.",
                                 "Total CPU, wall and output polling may overshoot; overruns fail the envelope.",
                                 "One job permits only one active child process; attempted child spawning may fail.",
                                 "Inputs and actual commands are bound; zero exit is not native acceptance."]
        steps = plan.get("steps")
        if not isinstance(steps, list) or not 1 <= len(steps) <= 24:
            raise ValueError("stage requires 1..24 serial steps")
        job = Job(seconds, memory_mib)
        record["status"] = "RUNNING"
        save(record_path, record)
        for index, step in enumerate(steps):
            if time.monotonic() - started >= seconds or job.stats()["cpu_seconds"] >= seconds:
                raise RuntimeError("STAGE_BUDGET_EXHAUSTED_BEFORE_NEXT_CHILD")
            if step["kind"] not in ("lean", "python"):
                raise ValueError("only pinned Lean or current Python child allowed")
            if step["kind"] == "python" and step["argv"][:len(PYTHON_FLAGS)] != PYTHON_FLAGS:
                raise ValueError("PYTHON_CHILD_ISOLATED_STARTUP_REQUIRED")
            executable = LEAN if step["kind"] == "lean" else Path(sys.executable)
            command = [str(executable), *[expand(x) for x in step["argv"]]]
            if step["kind"] == "lean":
                command[1:1] = ["-j", "1", "-M", str(memory_mib)]
            child_env = env.copy()
            paths = [expand(x) for x in step.get("lean_path", [])]
            for p in paths:
                inside(Path(p), stage_dir)
            child_env["LEAN_PATH"] = os.pathsep.join(paths)
            workdir = Path(expand(step.get("cwd", "$RUN")))
            inside(workdir, stage_dir)
            outpath, errpath = stage_dir / f"{index:02d}.stdout.log", stage_dir / f"{index:02d}.stderr.log"
            row = {"index": index, "label": step.get("label", str(index)), "command": command,
                   "cwd": str(workdir), "lean_path": paths, "started_utc": UTC(), "status": "STARTING"}
            record["steps"].append(row)
            save(record_path, record)
            with outpath.open("wb") as out, errpath.open("wb") as err:
                # Create suspended, attach to the resource/lifetime job, then resume.
                process = subprocess.Popen(command, cwd=workdir, env=child_env, stdout=out, stderr=err,
                                           creationflags=0x4 | subprocess.CREATE_NO_WINDOW)
                row["pid"] = process.pid
                row["status"] = "SUSPENDED_PENDING_JOB_ASSIGNMENT"
                save(record_path, record)
                job.attach_resume(process)
                row["status"] = "RUNNING"
                save(record_path, record)
                reason = None
                while process.poll() is None:
                    stats = job.stats()
                    if time.monotonic() - started > seconds:
                        reason = "STAGE_WALL_LIMIT"
                    elif stats["cpu_seconds"] > seconds:
                        reason = "STAGE_CPU_LIMIT"
                    elif size_tree(stage_dir) > LIMIT_BYTES:
                        reason = "SELECTED_STAGE_STAGING_LIMIT"
                    if reason:
                        job.kill()
                        break
                    time.sleep(0.05)
                row["exit_code"] = process.wait(timeout=15)
                row["status"] = reason or "EXITED"
                row["finished_utc"] = UTC()
                # The process handle can signal before Job accounting observes
                # its removal. Wait for the job to settle before another child;
                # this wait consumes the same stage allowance, never a refill.
                row["job_at_process_exit"] = job.stats()
                settled = row["job_at_process_exit"]
                settle_started = time.monotonic()
                settle_deadline = min(started + seconds, settle_started + 5)
                while (settled["active_processes"] != 0
                       and time.monotonic() < settle_deadline
                       and settled["cpu_seconds"] <= seconds):
                    time.sleep(0.01)
                    settled = job.stats()
                row["postexit_quiescence_seconds"] = time.monotonic() - settle_started
                row["job"] = settled
            row["stdout"] = record_file(outpath)
            row["stderr"] = record_file(errpath)
            row["cumulative_stage_wall_seconds"] = time.monotonic() - started
            if row["cumulative_stage_wall_seconds"] > seconds:
                row["status"] = "STAGE_WALL_LIMIT"
            if row["job"]["cpu_seconds"] > seconds:
                row["status"] = "STAGE_CPU_LIMIT"
            if row["job"]["terminated_processes"] > 0:
                row["status"] = "JOB_LIMIT_TERMINATION"
            if size_tree(stage_dir) > LIMIT_BYTES:
                row["status"] = "SELECTED_STAGE_STAGING_LIMIT"
            if row["job"]["active_processes"] != 0:
                raise RuntimeError("child did not quiesce")
            save(record_path, record)
            process = None
            expected = step.get("expected_exit", 0)
            if row["status"] != "EXITED" or row["exit_code"] != expected:
                record["status"] = "STEP_FAILED"
                break
        else:
            record["status"] = "STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE"
        record["job"] = job.stats()
        record["outputs"] = [record_file(p) for p in selected_output_files(stage_dir / "out", stage_dir)]
        record["stage_wall_seconds"] = time.monotonic() - started
        record["selected_stage_staging_bytes"] = size_tree(stage_dir)
    except BaseException as exc:
        record["status"] = "HARNESS_OR_PREPARATION_ERROR"
        record["error"] = (type(exc).__name__ + ": " + str(exc))[:2048]
        record["error_traceback"] = traceback.format_exc()[-8192:]
    finally:
        try:
            if process is not None and process.poll() is None:
                try:
                    if job is not None:
                        job.kill()
                finally:
                    # Also handles a suspended child whose job assignment failed.
                    if process.poll() is None:
                        process.kill()
                    process.wait(timeout=15)
            if job is not None:
                deadline = time.monotonic() + 5
                while job.stats()["active_processes"] and time.monotonic() < deadline:
                    job.kill()
                    time.sleep(0.05)
                record["final_job"] = job.stats()
                quiescent = record["final_job"]["active_processes"] == 0
                job.close()
        except BaseException as exc:
            record["cleanup_error"] = (type(exc).__name__ + ": " + str(exc))[:2048]
            quiescent = False
        if not quiescent:
            record["status"] = "QUIESCENCE_UNCONFIRMED_LOCK_RETAINED"
        census_complete = False
        if owns_stage:
            try:
                record["selected_stage_bytes_at_execution_endpoint"] = size_tree(stage_dir)
                census_complete = True
            except BaseException as exc:
                record["status"] = "SELECTED_STAGE_ENDPOINT_CENSUS_FAILED"
                record["endpoint_census_error"] = (type(exc).__name__ + ": " + str(exc))[:2048]
        record["stage_wall_seconds"] = time.monotonic() - started
        record["execution_endpoint"] = {"children_quiescent": quiescent,
                                        "selected_output_census_complete": census_complete,
                                        "receipt_persistence": "separate final bookkeeping below"}
        final_cpu = record.get("final_job", {}).get("cpu_seconds")
        if owns_stage and "limits" in record:
            if record["stage_wall_seconds"] > record["limits"]["stage_wall_seconds"]:
                record["status"] = "STAGE_WALL_LIMIT"
            if final_cpu is not None and final_cpu > record["limits"]["stage_aggregate_cpu_seconds"]:
                record["status"] = "STAGE_CPU_LIMIT"
        if not quiescent:
            record["status"] = "QUIESCENCE_UNCONFIRMED_LOCK_RETAINED"
        record["finished_utc"] = UTC()
        if owns_stage:
            receipt_started = time.monotonic()
            save(record_path, record)
            try:
                if size_tree(stage_dir) > LIMIT_BYTES:
                    record["status"] = "SELECTED_STAGE_STAGING_LIMIT"
            except BaseException as exc:
                record["status"] = "SELECTED_STAGE_POSTWRITE_CENSUS_FAILED"
                record["postwrite_census_error"] = (type(exc).__name__ + ": " + str(exc))[:2048]
            record["receipt_persistence_and_postwrite_census_seconds"] = time.monotonic() - receipt_started
            if not quiescent:
                record["status"] = "QUIESCENCE_UNCONFIRMED_LOCK_RETAINED"
            save(record_path, record)
        if quiescent and lock.exists():
            lock.unlink()
    print(json.dumps({"record": str(record_path), "status": record["status"]}), flush=True)
    return 0 if record["status"] == "STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE" else 1


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--directory", type=Path, required=True)
    p.add_argument("--stage", required=True)
    p.add_argument("--expected-plan-sha256", required=True)
    p.add_argument("plan", type=Path)
    a = p.parse_args()
    return execute(a.plan, a.directory, a.stage, a.expected_plan_sha256)


if __name__ == "__main__":
    raise SystemExit(main())

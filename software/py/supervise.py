"""Bounded Windows public-CLI transport; no self-execution or native authority.

The coordinator owns launch clearance, immutable pins, phase orchestration and
fixture faults. This module owns only one public dispatcher process tree per
call. The supplied reviewed runner module provides Job; its nested-stage API
remains unchanged. Output and wall limits are polled, not hard filesystem caps.
The success wall endpoint includes bounded output parsing/hashing and Job close;
only final supervisor-receipt serialization/write is outside that observation.
"""
from __future__ import annotations

from contextlib import ExitStack
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

MIB = 1024 * 1024
SAFE_NAME = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")
RESERVED_NAMES = {"CON", "PRN", "AUX", "NUL", *("COM" + str(i) for i in range(1, 10)),
                  *("LPT" + str(i) for i in range(1, 10))}
DEFAULTS = {"wall_seconds": 450, "cpu_seconds": 450, "memory_mib": 6144,
            "active_processes": 8, "stdout_bytes": 2 * MIB, "stderr_bytes": 65536,
            "event_bytes": 65536, "request_bytes": 131072,
            "poll_seconds": 0.05, "settle_seconds": 15}


class SupervisorFailure(RuntimeError):
    def __init__(self, code, record):
        super().__init__(code)
        self.code, self.record = code, record


def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def bounded_read(path, bound):
    with Path(path).open("rb") as stream:
        raw = stream.read(bound + 1)
    require(len(raw) <= bound, "FILE_BYTE_LIMIT")
    return raw


def save_new(path, raw, bound=65536):
    require(type(raw) is bytes and len(raw) <= bound, "SUPERVISOR_RECORD_BYTE_LIMIT")
    with Path(path).open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "DUPLICATE_EVENT_KEY")
            result[key] = value
        return result

    def bad(_):
        raise RuntimeError("NONFINITE_EVENT_NUMBER")

    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=bad)


class Transport:
    """One-case supervisor, callable as transport(name, exact_request_bytes).

    limits may override DEFAULTS downward, add case_seconds:{name:seconds} wall
    overrides (each at most450 seconds), and must contain pins: a list of
    {path,bytes,sha256} records, at most16 files/64MiB total/16MiB each. Pins must
    include Python, node, config and the supplied runner module. Root may also
    bind storage/checking/test/supervisor sources here. No directory traversal is
    used for pinning, polling, or process cleanup. Paths and runner object are
    trusted coordinator inputs, not public request fields.

    The evidence root must already exist. Each case gets a new directory; no
    existing case, response or failure record is overwritten. Return requires
    measured final Job.active_processes==0 and a reaped direct child. Any failure
    preserves available evidence and raises SupervisorFailure, never acceptance.
    """
    def __init__(self, python, node, config, state, evidence_root, runner_module, limits):
        require(os.name == "nt", "WINDOWS_JOB_PROFILE_REQUIRED")
        require(type(limits) is dict and "pins" in limits and
                set(limits) <= set(DEFAULTS) | {"pins", "case_seconds"}, "SUPERVISOR_LIMIT_FIELDS")
        self.limits = dict(DEFAULTS, **{key: value for key, value in limits.items() if key in DEFAULTS})
        for key, ceiling in DEFAULTS.items():
            value = self.limits[key]
            if key in {"poll_seconds", "settle_seconds"}:
                require(type(value) in (int, float) and 0 < value <= ceiling, "SUPERVISOR_LIMIT:" + key)
            else:
                require(type(value) is int and 0 < value <= ceiling, "SUPERVISOR_LIMIT:" + key)
        require(self.limits["active_processes"] == 8, "OUTER_EIGHT_PROCESS_PROFILE")
        self.case_seconds = limits.get("case_seconds", {})
        require(type(self.case_seconds) is dict and len(self.case_seconds) <= 128, "CASE_WALL_OVERRIDES")
        for name, seconds in self.case_seconds.items():
            require(type(name) is str and SAFE_NAME.fullmatch(name) and
                    type(seconds) in (int, float) and 0 < seconds <= 450, "CASE_WALL_OVERRIDE")
        self.python, self.node, self.config = (Path(value).resolve(strict=True) for value in (python, node, config))
        self.state = Path(state).resolve()
        self.evidence_root = Path(evidence_root).resolve(strict=True)
        require(self.evidence_root.is_dir(), "EVIDENCE_ROOT_DIRECTORY")
        self.runner = runner_module
        self.runner_path = Path(runner_module.__file__).resolve(strict=True)
        require(callable(getattr(runner_module, "Job", None)), "REVIEWED_JOB_CLASS_REQUIRED")
        self.pins = limits["pins"]
        require(type(self.pins) is list and 4 <= len(self.pins) <= 16, "BOUND_PIN_COUNT")
        pin_paths, declared_bytes = set(), 0
        for pin in self.pins:
            require(type(pin) is dict and set(pin) == {"path", "bytes", "sha256"}, "BOUND_PIN_FIELDS")
            path = Path(pin["path"]).resolve(strict=True)
            require(path not in pin_paths, "DUPLICATE_BOUND_PIN")
            require(type(pin["bytes"]) is int and 0 < pin["bytes"] <= 16 * MIB, "BOUND_PIN_BYTES")
            require(type(pin["sha256"]) is str and re.fullmatch(r"[a-fA-F0-9]{64}", pin["sha256"]), "BOUND_PIN_SHA256")
            pin_paths.add(path)
            declared_bytes += pin["bytes"]
        require(declared_bytes <= 64 * MIB and
                {self.python, self.node, self.config, self.runner_path} <= pin_paths, "REQUIRED_BOUND_PINS")

    def verify_pins(self, record):
        record["bound_pin_count"], record["bound_pin_bytes"] = 0, 0
        record["pins"] = []
        for pin in self.pins:
            path = Path(pin["path"]).resolve(strict=True)
            with path.open("rb") as stream:
                raw = stream.read(pin["bytes"] + 1)
            actual = {"path": str(path), "bytes": len(raw), "sha256": digest(raw)}
            record["pins"].append(actual)
            record["bound_pin_count"] += 1
            record["bound_pin_bytes"] += len(raw)
            require(len(raw) == pin["bytes"] and actual["sha256"] == pin["sha256"].lower(), "BOUND_PIN_CHANGED")

    def lengths(self, directory):
        result = {}
        for name in ("stdout.txt", "stderr.txt", "event.json"):
            path = directory / name
            result[name] = path.stat().st_size if path.exists() else 0
        return result

    def output_within_bounds(self, directory):
        observed = self.lengths(directory)
        for name, field in (("stdout.txt", "stdout_bytes"), ("stderr.txt", "stderr_bytes"), ("event.json", "event_bytes")):
            require(observed[name] <= self.limits[field], "PUBLIC_OUTPUT_LIMIT:" + name)
        return observed

    def quiesce(self, job, process, record, *, terminate):
        """Bounded cleanup also covers assignment/resume failure while suspended."""
        errors = []
        if terminate and job is not None:
            try:
                job.kill()
                record["job_termination_requested"] = True
            except Exception as error:
                errors.append("job.kill:" + type(error).__name__)
        if process is not None:
            try:
                # This direct kill is required if assignment never succeeded;
                # killing an empty Job alone would leave a suspended child.
                if terminate and process.poll() is None:
                    process.kill()
                    record["direct_termination_requested"] = True
                process.wait(timeout=self.limits["settle_seconds"])
                record["returncode"] = process.returncode
                record["direct_child_reaped"] = True
            except Exception as error:
                errors.append("process.wait:" + type(error).__name__)
        if job is not None:
            deadline = time.monotonic() + self.limits["settle_seconds"]
            try:
                while True:
                    final = job.stats()
                    record["final_job"] = final
                    if final["active_processes"] == 0:
                        record["final_active_zero"] = True
                        break
                    if time.monotonic() >= deadline:
                        errors.append("job.active_processes:not_zero")
                        break
                    time.sleep(self.limits["poll_seconds"])
            except Exception as error:
                errors.append("job.stats:" + type(error).__name__)
        else:
            record["final_active_zero"] = process is None
        if errors:
            record.setdefault("cleanup_errors", []).extend(errors)
        return record["final_active_zero"] and (process is None or record["direct_child_reaped"])

    def record_outputs(self, directory, record):
        rows = {}
        for name, bound in (("request.json", self.limits["request_bytes"]), ("command.json", 65536),
                            ("stdout.txt", self.limits["stdout_bytes"]), ("stderr.txt", self.limits["stderr_bytes"]),
                            ("event.json", self.limits["event_bytes"])):
            path = directory / name
            if not path.exists():
                rows[name] = {"present": False}
                continue
            length = path.stat().st_size
            rows[name] = {"present": True, "bytes": length, "sha256": None}
            if length <= bound:
                rows[name]["sha256"] = digest(bounded_read(path, bound))
        record["files"] = rows

    def __call__(self, name, raw):
        require(type(name) is str and SAFE_NAME.fullmatch(name) and name.upper() not in RESERVED_NAMES, "CASE_NAME")
        require(type(raw) is bytes and 0 < len(raw) <= self.limits["request_bytes"], "REQUEST_BYTES")
        directory = self.evidence_root / name
        require(directory.resolve().is_relative_to(self.evidence_root), "CASE_PATH_DOMAIN")
        directory.mkdir(exist_ok=False)
        started = time.monotonic()
        wall_limit = self.case_seconds.get(name, self.limits["wall_seconds"])
        record = {"schema": 1, "name": name, "started_utc": datetime.now(timezone.utc).isoformat(),
                  "status": "PREPARING", "native_acceptance": False,
                  "limits": self.limits, "wall_limit_seconds": wall_limit, "request_sha256": digest(raw),
                  "job_created_before_process": False, "attach_resume_returned": False,
                  "job_termination_requested": False, "direct_termination_requested": False,
                  "direct_child_reaped": False, "final_active_zero": False,
                  "returncode": None, "polls": 0, "sampled_peak_active_processes": 0,
                  "sampled_peak_job_private_commit_bytes": 0,
                  "wall_endpoint": "after quiescence, output parsing/hashing and Job close; before final receipt serialization/write",
                  "scope": "one public dispatcher process tree; no hard transient filesystem quota or mathematical authority"}
        job, process, failure, result = None, None, None, None
        try:
            save_new(directory / "request.json", raw, self.limits["request_bytes"])
            self.verify_pins(record)
            command = [str(self.python), "-B", "-E", "-s", "-S", str(self.node), "--config", str(self.config),
                       "--state", str(self.state), "--request", str(directory / "request.json"),
                       "--event", str(directory / "event.json")]
            save_new(directory / "command.json", encoded({"argv": command, "cwd": str(self.node.parent),
                                                         "shell": False, "creationflags": 0x4 | subprocess.CREATE_NO_WINDOW,
                                                         "environment_override": {"PYTHONDONTWRITEBYTECODE": "1"}}))
            job = self.runner.Job(seconds=self.limits["cpu_seconds"], memory_mib=self.limits["memory_mib"],
                                  active_processes=self.limits["active_processes"])
            record["job_created_before_process"] = True
            record["initial_job"] = job.stats()
            require(record["initial_job"]["active_processes"] == 0, "NEW_JOB_NOT_EMPTY")
            child_environment = os.environ.copy()
            child_environment["PYTHONDONTWRITEBYTECODE"] = "1"
            child_environment.pop("PYTHONPATH", None)
            child_environment.pop("PYTHONHOME", None)
            with ExitStack() as streams:
                out = streams.enter_context((directory / "stdout.txt").open("xb"))
                err = streams.enter_context((directory / "stderr.txt").open("xb"))
                record["launch_seconds"] = time.monotonic() - started
                require(record["launch_seconds"] <= wall_limit, "PUBLIC_WALL_LIMIT_BEFORE_LAUNCH")
                process = subprocess.Popen(command, cwd=self.node.parent, env=child_environment,
                                           stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                           shell=False, close_fds=True,
                                           creationflags=0x4 | subprocess.CREATE_NO_WINDOW)
                record["pid"] = process.pid
                job.attach_resume(process)
                record["attach_resume_returned"] = True
                record["resumed_seconds"] = time.monotonic() - started
                while True:
                    stats = job.stats()
                    record["polls"] += 1
                    record["sampled_peak_active_processes"] = max(record["sampled_peak_active_processes"], stats["active_processes"])
                    record["sampled_peak_job_private_commit_bytes"] = max(record["sampled_peak_job_private_commit_bytes"], stats["peak_job_private_commit_bytes"])
                    require(time.monotonic() - started <= wall_limit, "PUBLIC_WALL_LIMIT")
                    require(stats["cpu_seconds"] <= self.limits["cpu_seconds"], "PUBLIC_CPU_LIMIT")
                    require(stats["peak_job_private_commit_bytes"] <= self.limits["memory_mib"] * MIB, "PUBLIC_JOB_MEMORY_LIMIT")
                    require(stats["active_processes"] <= self.limits["active_processes"], "PUBLIC_ACTIVE_PROCESS_LIMIT")
                    self.output_within_bounds(directory)
                    if process.poll() is not None:
                        record["direct_exit_seconds"] = time.monotonic() - started
                        break
                    time.sleep(self.limits["poll_seconds"])
                require(self.quiesce(job, process, record, terminate=False), "PUBLIC_DESCENDANTS_NOT_QUIESCENT")
                record["quiescent_seconds"] = time.monotonic() - started
            self.output_within_bounds(directory)
            final = record["final_job"]
            require(final["total_processes"] >= 1, "PUBLIC_JOB_NEVER_ASSIGNED")
            require(final["terminated_processes"] == 0, "PUBLIC_JOB_TERMINATED_PROCESSES")
            require(final["cpu_seconds"] <= self.limits["cpu_seconds"] and
                    final["peak_job_private_commit_bytes"] <= self.limits["memory_mib"] * MIB,
                    "PUBLIC_FINAL_JOB_LIMIT")
            require(time.monotonic() - started <= wall_limit, "PUBLIC_FINAL_WALL_LIMIT")
            stdout = bounded_read(directory / "stdout.txt", self.limits["stdout_bytes"])
            stderr = bounded_read(directory / "stderr.txt", self.limits["stderr_bytes"])
            event = strict_json(bounded_read(directory / "event.json", self.limits["event_bytes"]))
            require(type(event) is dict and event.get("request_sha256") == digest(raw) and
                    event.get("response_sha256") == digest(stdout), "PUBLIC_EVENT_IO_BINDING")
            result = {"stdout": stdout, "stderr": stderr, "returncode": process.returncode, "event": event}
            record["status"] = "TRANSPORT_COMPLETE" if process.returncode == 0 else "TRANSPORT_NONZERO_EXIT"
        except BaseException as error:
            failure = error
            record["status"] = "TRANSPORT_FAILED"
            record["failure"] = {"type": type(error).__name__, "detail": str(error)[:2048]}
            self.quiesce(job, process, record, terminate=True)
        finally:
            if job is not None:
                # Closing is a final kill-on-close backstop, never substituted
                # for the preceding active-zero query and child wait.
                try:
                    job.close()
                    record["job_closed"] = True
                except Exception as error:
                    record["job_closed"] = False
                    record.setdefault("cleanup_errors", []).append("job.close:" + type(error).__name__)
                    failure = failure or error
            try:
                self.record_outputs(directory, record)
            except Exception as error:
                record["output_record_error"] = type(error).__name__ + ":" + str(error)[:512]
                failure = failure or error
            record["wall_seconds"] = time.monotonic() - started
            record["finished_utc"] = datetime.now(timezone.utc).isoformat()
            if failure is None and record["wall_seconds"] > wall_limit:
                failure = RuntimeError("PUBLIC_BOOKKEEPING_WALL_LIMIT")
                record["failure"] = {"type": type(failure).__name__, "detail": str(failure)}
            if failure is not None:
                record["status"] = "TRANSPORT_FAILED"
            try:
                save_new(directory / "supervisor.json", encoded(record))
            except Exception as error:
                record["status"] = "TRANSPORT_FAILED"
                record["evidence_persistence_error"] = type(error).__name__ + ":" + str(error)[:512]
                failure = failure or error
        if failure is not None or not record["final_active_zero"] or not record["direct_child_reaped"]:
            raise SupervisorFailure("PUBLIC_TRANSPORT_FAILED:" + name, record) from failure
        return result

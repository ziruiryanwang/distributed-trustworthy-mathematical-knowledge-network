"""Private same-call clean nonacceptance checks; no proof or saved-report API.

The owning verifier supplies the actual in-memory supervisor result and captures
all expected arguments itself. Pins, trust, exact inputs and final deadlines are
separate mandatory caller checks. Passing these checks never grants a warrant.
"""
import math
import os
from pathlib import Path


REPORT_FIELDS = frozenset((
    "schema", "status", "authority", "argv", "cwd", "limits", "child_exit_code",
    "direct_child_reaped", "final_job", "last_observed_job", "job_closed",
    "cleanup_errors", "termination_requested", "cpu_scope", "limits_scope",
    "observed_logs", "service_orderly_stop_sent", "wrapper_supervision_cpu_seconds",
    "wall_seconds_through_cleanup"))
JOB_FIELDS = frozenset(("user_cpu_seconds", "kernel_cpu_seconds", "cpu_seconds",
    "active_processes", "total_processes", "terminated_processes", "peak_job_private_commit_bytes"))
LIMIT_FIELDS = frozenset(("cpu_seconds", "wall_seconds", "memory_mib",
    "active_processes", "stdout_bytes", "stderr_bytes"))


def _need(ok, code):
    if not ok:
        raise ValueError("CLEAN_REFUSAL_"+code)


def _integer(value, lower, upper, code):
    _need(type(value) is int and lower <= value <= upper, code)
    return value


def _number(value, upper, code):
    _need(type(value) in (int, float) and 0 <= value <= upper
          and math.isfinite(value), code)
    return value


def validate_report(report, *, argv, cwd, limits):
    """Reject every ambiguous/nonclean result; never mutate report or inputs."""
    _need(type(limits) is dict and set(limits) == LIMIT_FIELDS, "EXPECTED_LIMITS")
    for name, value in limits.items():
        _integer(value, 1, 2**63-1, "EXPECTED_LIMIT:"+name)
    _need(type(argv) is list and bool(argv) and all(type(x) is str for x in argv), "EXPECTED_ARGV")
    _need(type(report) is dict and set(report) == REPORT_FIELDS, "REPORT_FIELDS")
    _need(report["schema"] == "DMKN_V4_OWNER_COMMAND_REPORT_V1"
          and report["authority"] == "LOCAL_OPERATION_REPORT_NOT_MATHEMATICAL_ACCEPTANCE"
          and report["status"] == "COMMAND_FAILED", "REPORT_STATUS")
    _need(type(report["argv"]) is list and report["argv"] == argv
          and type(report["cwd"]) is str and report["cwd"] == str(cwd)
          and type(report["limits"]) is dict and report["limits"] == limits
          and all(type(value) is int for value in report["limits"].values()), "CALL_BINDING")
    _integer(report["child_exit_code"], 1, 1, "EXIT_CODE")
    _need(report["direct_child_reaped"] is True and report["job_closed"] is True
          and report["termination_requested"] is False
          and report["service_orderly_stop_sent"] is False
          and type(report["cleanup_errors"]) is list and report["cleanup_errors"] == [], "CLOSURE")
    _need(report["cpu_scope"] == "NATIVE_JOB_USER_TIME_LIMIT_AND_SAMPLED_JOB_USER_PLUS_KERNEL;WRAPPER_SEPARATE"
          and report["limits_scope"] == "WALL_TOTAL_CPU_AND_LOG_CAPS_SAMPLED_NOT_HARD_DISK_CAPS",
          "REPORT_SCOPE")
    final = report["final_job"]
    _need(type(final) is dict and set(final) == JOB_FIELDS, "FINAL_JOB")
    _need(type(report["last_observed_job"]) is dict and report["last_observed_job"] == final
          and all(type(report["last_observed_job"][key]) is type(value)
                  for key, value in final.items()),
          "FINAL_OBSERVATION")
    _integer(final["active_processes"], 0, 0, "ACTIVE_PROCESSES")
    _integer(final["terminated_processes"], 0, 0, "TERMINATED_PROCESSES")
    _integer(final["total_processes"], 1, 2**32-1, "TOTAL_PROCESSES")
    _integer(final["peak_job_private_commit_bytes"], 0, limits["memory_mib"]*1024**2, "MEMORY")
    user = _number(final["user_cpu_seconds"], limits["cpu_seconds"], "USER_CPU")
    kernel = _number(final["kernel_cpu_seconds"], limits["cpu_seconds"], "KERNEL_CPU")
    total = _number(final["cpu_seconds"], limits["cpu_seconds"], "TOTAL_CPU")
    _need(math.isclose(total, user+kernel, rel_tol=1e-12, abs_tol=1e-7), "CPU_SUM")
    _number(report["wrapper_supervision_cpu_seconds"], 60, "WRAPPER_CPU")
    _number(report["wall_seconds_through_cleanup"], limits["wall_seconds"], "WALL")
    logs = report["observed_logs"]
    _need(type(logs) is dict and set(logs) == {"stdout_bytes", "stderr_bytes"}, "LOG_FIELDS")
    for name in logs:
        _integer(logs[name], 0, limits[name], "LOG_BOUND:"+name)
    _need(logs["stdout_bytes"] == 0, "NONEMPTY_STDOUT")


def census(supervisor, directory, *, byte_cap, entry_cap, active):
    """Bound only this fresh attempt's ordinary outputs, with streaming traversal."""
    _integer(byte_cap, 1, 2**63-1, "OUTPUT_BYTE_CAP")
    _integer(entry_cap, 1, 2**31-1, "OUTPUT_ENTRY_CAP")
    active()
    root = supervisor.absolute(directory, directory=True)
    pending = [root]; count = size = 0
    while pending:
        active()
        with os.scandir(pending.pop()) as entries:
            for entry in entries:
                active(); count += 1
                _need(count <= entry_cap, "OUTPUT_ENTRIES")
                is_directory = entry.is_dir(follow_symlinks=False)
                path = supervisor.absolute(Path(entry.path), directory=is_directory)
                _need(path.is_relative_to(root), "OUTPUT_SCOPE")
                if is_directory:
                    pending.append(path)
                else:
                    size += path.stat().st_size
                    _need(size <= byte_cap, "OUTPUT_BYTES")
                active()
    active()


def validate_output(supervisor, directory, report, *, byte_cap, entry_cap, active):
    """Check real logs including empty stdout, then census the operation root."""
    active()
    root = supervisor.absolute(directory, directory=True)
    for name in ("stdout", "stderr"):
        active()
        path = supervisor.absolute(root/"command"/(name+".txt"))
        expected = report["observed_logs"][name+"_bytes"]
        cap = report["limits"][name+"_bytes"]
        _integer(expected, 0, cap, "ACTUAL_LOG_BOUND")
        _need(path.stat().st_size == expected, "ACTUAL_LOG_SIZE")
        with path.open("rb") as stream:
            raw = stream.read(cap+1)
        _need(len(raw) == expected and path.stat().st_size == expected, "ACTUAL_LOG_CHANGED")
        if name == "stdout":
            _need(raw == b"", "ACTUAL_NONEMPTY_STDOUT")
        active()
    census(supervisor, root, byte_cap=byte_cap, entry_cap=entry_cap, active=active)

"""Finite installed producer parent; no arbitrary owner code or automatic retry.

Only the exact release-owned entry is copied. Product modules stay at their
installed origins. Uses the existing Windows Job supervisor, not a new sandbox.
The distribution caller preserves its original STARTED_NS/STARTED_CPU clocks.
"""
from __future__ import annotations

import time
STARTED_NS, STARTED_CPU = time.monotonic_ns(), time.process_time()
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import sys

MIB = 1024**2
PUBLIC_ENTRY_REPORT_LIMIT = 64*1024
RELEASE_SCHEMA = "DMKN_V5_DIRECTORY_RELEASE_V4"
RESULT_SCHEMA = "DMKN_RELEASE_PRODUCER_LAUNCH_RESULT_V1"
BASE_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
CONTRACT = "sdk/v5/release_production/launch_contract.py"
ENTRY = "sdk/v5/release_production/operator.py"
SELF = "sdk/v5/release_production/launch.py"
HELPERS = {
    "_dmkn_release_producer_supervisor": "operator/commons.py",
    "domains": "receiver/helpers/domains.py",
    "_dmkn_release_producer_job": "receiver/helpers/run_stage.py",
}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def strict(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            need(key not in value, "PRODUCER_LAUNCH_DUPLICATE_KEY")
            value[key] = item
        return value
    def reject(unused):
        raise ValueError("PRODUCER_LAUNCH_NONFINITE_JSON")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=reject)


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":"
         and path != Path(path.anchor) and str(path.resolve(strict=not fresh)) == str(path),
         "PRODUCER_LAUNCH_CANONICAL_PATH")
    for part in path.parts[1:]:
        need(part not in (".", "..") and not part.endswith((".", " "))
             and not os.path.isreserved(part)
             and not any(ord(c) < 32 or c in ':*?"<>|' for c in part),
             "PRODUCER_LAUNCH_PATH_COMPONENT")
    for ancestor in path.parents:
        info = ancestor.lstat()
        need(stat.S_ISDIR(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "PRODUCER_LAUNCH_ORDINARY_PARENT")
    if fresh:
        need(not path.exists() and not path.is_symlink() and not path.is_junction(),
             "PRODUCER_LAUNCH_FRESH_PATH")
    else:
        info = path.lstat()
        need(not getattr(info, "st_file_attributes", 0) & 0x400
             and (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)),
             "PRODUCER_LAUNCH_ORDINARY_TARGET")
    return path


def digest(value):
    need(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value),
         "PRODUCER_LAUNCH_DIGEST")
    return value


def read(path, maximum):
    path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "PRODUCER_LAUNCH_READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "PRODUCER_LAUNCH_READ_CHANGED")
    return raw


def pin(path, maximum=128*MIB):
    path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "PRODUCER_LAUNCH_PIN_BOUND")
    with path.open("rb") as stream:
        value = hashlib.file_digest(stream, "sha256").hexdigest()
    need(path.stat().st_size == size, "PRODUCER_LAUNCH_PIN_CHANGED")
    return dict(path=str(path), bytes=size, sha256=value)


def checked(row, maximum=128*MIB):
    need(type(row) is dict and set(row) == {"path", "bytes", "sha256"}
         and type(row["path"]) is str and type(row["bytes"]) is int
         and 0 < row["bytes"] <= maximum, "PRODUCER_LAUNCH_PIN_FIELDS")
    digest(row["sha256"])
    need(pin(row["path"], maximum) == row, "PRODUCER_LAUNCH_EXACT_PIN")
    return Path(row["path"])


def payload(root, files, relative, maximum=128*MIB):
    row = files.get(relative)
    need(type(row) is dict and set(row) == {"bytes", "sha256"},
         "PRODUCER_LAUNCH_RELEASE_ROLE")
    selected = dict(path=str(root/relative), **row)
    checked(selected, maximum)
    return selected


def held_module(name, selected):
    need(name not in sys.modules, "PRODUCER_LAUNCH_PRELOADED_HELPER")
    path = checked(selected, 4*MIB)
    raw = read(path, 4*MIB)
    need(len(raw) == selected["bytes"] and hashlib.sha256(raw).hexdigest() == selected["sha256"],
         "PRODUCER_LAUNCH_HELD_SOURCE_CHANGED")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


def write_new(path, raw):
    ordinary(path, fresh=True)
    need(type(raw) is bytes and 0 < len(raw) <= 2*MIB, "PRODUCER_LAUNCH_WRITE_BOUND")
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "PRODUCER_LAUNCH_SHORT_WRITE")
        stream.flush()
        os.fsync(stream.fileno())
    observed = pin(path, 2*MIB)
    need(observed["bytes"] == len(raw) and observed["sha256"] == hashlib.sha256(raw).hexdigest(),
         "PRODUCER_LAUNCH_SAVED_BYTES")
    return observed


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()


def overlap(left, right):
    return left.is_relative_to(right) or right.is_relative_to(left)


def output_census(run, action_output, limits):
    need(type(limits) is dict and set(limits) == {"bytes", "entries"},
         "PRODUCER_LAUNCH_OUTPUT_LIMIT_FIELDS")
    for name, maximum in (("bytes", 1024*MIB), ("entries", 16384)):
        need(type(limits[name]) is int and 0 < limits[name] <= maximum,
             "PRODUCER_LAUNCH_OUTPUT_LIMIT")
    need(not overlap(run, action_output), "PRODUCER_LAUNCH_OUTPUT_ROOT_OVERLAP")
    entries = total = 0
    for root in (run, action_output):
        if not root.exists():
            need(not root.is_symlink() and not root.is_junction(), "PRODUCER_LAUNCH_OUTPUT_ALIAS")
            continue
        ordinary(root, directory=True)
        for parent, children, names in os.walk(root, followlinks=False):
            parent = ordinary(parent, directory=True)
            entries += len(children)+len(names)
            need(entries <= limits["entries"], "PRODUCER_LAUNCH_OUTPUT_ENTRIES")
            for child in children:
                ordinary(parent/child, directory=True)
            for name in names:
                total += ordinary(parent/name).stat().st_size
                need(total <= limits["bytes"], "PRODUCER_LAUNCH_OUTPUT_BYTES")
    return dict(entries=entries, bytes=total,
                scope="DISJOINT_OPERATION_AND_SELECTED_ACTION_OUTPUT_ROOTS")


def clean(result):
    return (type(result) is dict and result.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED"
            and type(result.get("child_exit_code")) is int and result["child_exit_code"] == 0
            and result.get("direct_child_reaped") is True and result.get("job_closed") is True
            and result.get("cleanup_errors") == [] and result.get("termination_requested") is False
            and type(result.get("final_job")) is dict
            and result["final_job"].get("active_processes") == 0
            and result["final_job"].get("terminated_processes") == 0)


def within(deadline, cpu_limit=60):
    need(time.monotonic_ns() < deadline and time.process_time()-STARTED_CPU <= cpu_limit,
         "PRODUCER_LAUNCH_ORIGINAL_ENVELOPE_EXCEEDED")


def main():
    need(len(sys.argv) == 3, "PRODUCER_LAUNCH_USAGE_PLAN_AND_SHA")
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "PRODUCER_LAUNCH_ISOLATED_WINDOWS")
    original_path, expected = ordinary(sys.argv[1]), digest(sys.argv[2])
    raw = read(original_path, MIB)
    need(hashlib.sha256(raw).hexdigest() == expected, "PRODUCER_LAUNCH_PLAN_PIN")
    preliminary = strict(raw)
    need(type(preliminary) is dict and type(preliminary.get("release")) is dict,
         "PRODUCER_LAUNCH_RELEASE_REQUIRED")
    release = preliminary["release"]
    need(set(release) == {"root", "manifest", "descriptor"}, "PRODUCER_LAUNCH_RELEASE_FIELDS")
    root = ordinary(release["root"], directory=True)
    checked(release["manifest"], 8*MIB)
    need(Path(release["manifest"]["path"]) == root/"V5-RELEASE.json",
         "PRODUCER_LAUNCH_RELEASE_MANIFEST_LOCATION")
    manifest_raw = read(root/"V5-RELEASE.json", 8*MIB)
    need(hashlib.sha256(manifest_raw).hexdigest() == release["manifest"]["sha256"],
         "PRODUCER_LAUNCH_RELEASE_CHANGED")
    manifest = strict(manifest_raw)
    need(type(manifest) is dict and manifest.get("schema") == RELEASE_SCHEMA
         and type(manifest.get("files")) is dict and 1 <= len(manifest["files"]) <= 20000,
         "PRODUCER_LAUNCH_RELEASE_CONTAINER")
    files = manifest["files"]
    need(Path(__file__).resolve() == root/SELF, "PRODUCER_LAUNCH_INSTALLED_ORIGIN")
    executable = root/"base/receiver/runtime/python/python.exe"
    need(Path(sys.executable).resolve() == executable, "PRODUCER_LAUNCH_INSTALLED_PYTHON")
    bootstrap_pins = [dict(release["manifest"])]
    for relative in (SELF, CONTRACT, ENTRY, "base/receiver/runtime/python/python.exe",
                     "base/receiver/runtime/python/python314.dll", "base/RELEASE-MANIFEST.json"):
        bootstrap_pins.append(payload(root, files, relative))
    need(bootstrap_pins[-1]["sha256"] == BASE_SHA, "PRODUCER_LAUNCH_FIXED_SUPERVISOR")
    contract_pin = next(row for row in bootstrap_pins if row["path"] == str(root/CONTRACT))
    C = held_module("_dmkn_release_producer_contract_parent", contract_pin)
    selection, original_pin = C.read_selection(original_path, expected)
    need(selection == preliminary, "PRODUCER_LAUNCH_PLAN_CHANGED_DURING_BOOTSTRAP")
    selected = C.validate_selection(selection, original_pin, fresh_run=True)
    need(Path(selected.root) == root, "PRODUCER_LAUNCH_SELECTED_ROOT")
    run, action_output = Path(selected.run), Path(selected.action_output)
    need(not overlap(run, original_path) and not overlap(action_output, original_path),
         "PRODUCER_LAUNCH_ORIGINAL_PLAN_OUTPUT_OVERLAP")
    base_files = strict(read(root/"base/RELEASE-MANIFEST.json", 8*MIB))["files"]
    modules = {}
    for name, relative in HELPERS.items():
        row = payload(root, files, "base/"+relative, 4*MIB)
        need({key: row[key] for key in ("bytes", "sha256")} == base_files.get(relative),
             "PRODUCER_LAUNCH_SUPERVISOR_ROLE_MAP")
        bootstrap_pins.append(row)
        modules[name] = held_module(name, row)
    A, J = modules["_dmkn_release_producer_supervisor"], modules["_dmkn_release_producer_job"]
    limits = A.limits_checked(selection["limits"])
    need(limits["cpu_seconds"] <= 86400 and limits["wall_seconds"] <= 3600
         and limits["memory_mib"] <= 4096, "PRODUCER_LAUNCH_FINITE_LIMITS")
    deadline = STARTED_NS+limits["wall_seconds"]*1_000_000_000
    within(deadline, 30)
    # Validate the output envelope before any run directory exists.
    output_census(run, action_output, selection["output_limits"])
    C.rebind_selection(selected)
    ordinary(run, directory=True, fresh=True)
    run.mkdir()
    result = worker_pin = copied_pin = observed_output = None
    status, final_error, bootstrap_cpu = "FAIL", None, None
    copied_entry_pin = None
    pending_pin = None
    try:
        # Result bytes are provisional while this marker exists. If any later
        # failure also prevents writing its diagnostic, the marker still blocks
        # adoption. The final unlink below is the completion commit boundary.
        pending_pin = write_new(run/"FINALIZATION-PENDING.json", encode(dict(
            schema="DMKN_RELEASE_PRODUCER_FINALIZATION_PENDING_V1",
            authority="RESULT_NOT_ADOPTABLE_UNTIL_MARKER_REMOVED")))
        copied_pin = write_new(run/"selection.json", raw)
        entry_raw = read(checked(selection["entry"], PUBLIC_ENTRY_REPORT_LIMIT), PUBLIC_ENTRY_REPORT_LIMIT)
        need(len(entry_raw) == selection["entry"]["bytes"]
             and hashlib.sha256(entry_raw).hexdigest() == selection["entry"]["sha256"],
             "PRODUCER_LAUNCH_ENTRY_COPY_CHANGED")
        copied_entry_pin = write_new(run/"entry.py", entry_raw)
        argv = C.command(selection, copied_pin)
        need(argv[:5] == [str(executable), "-I", "-S", "-B", str(run/"entry.py")],
             "PRODUCER_LAUNCH_FIXED_CHILD_PREFIX")
        within(deadline, 30)
        bootstrap_cpu = time.process_time()-STARTED_CPU
        result = A.supervise(argv, root, run/"command", limits, J.Job, started=STARTED_NS/1e9)
        need(clean(result), "PRODUCER_LAUNCH_CHILD_NOT_CLEANLY_COMPLETED")
        need(result["argv"] == argv and result["cwd"] == str(root) and result["limits"] == limits,
             "PRODUCER_LAUNCH_ACTUAL_INVOCATION")
        worker_pin = pin(run/"OWNER-RESULT.json", PUBLIC_ENTRY_REPORT_LIMIT)
        C.validate_worker_report(selection, copied_pin, worker_pin)
        if selection["action"] in ("request", "preflight"):
            need(not action_output.exists(), "PRODUCER_LAUNCH_NONDISPATCH_OUTPUT_CREATED")
        C.rebind_selection(selected)
        for row in (*bootstrap_pins, original_pin, copied_pin, copied_entry_pin, worker_pin):
            checked(row)
        need(read(original_path, MIB) == raw and read(run/"selection.json", MIB) == raw,
             "PRODUCER_LAUNCH_FINAL_SELECTION_CHANGED")
        observed_output = output_census(run, action_output, selection["output_limits"])
        within(deadline)
        status = "COMMAND_EXITED_ZERO_AND_CLOSED"
    except BaseException as error:
        final_error = type(error).__name__+": "+str(error)[:1800]
    report = dict(schema=RESULT_SCHEMA, status=status, selection=copied_pin,
        worker_report=worker_pin, result=result, final_error=final_error,
        observed_output=observed_output, bootstrap_cpu_seconds=bootstrap_cpu,
        wrapper_cpu_seconds=time.process_time()-STARTED_CPU,
        wall_seconds=(time.monotonic_ns()-STARTED_NS)/1e9,
        pre_clock_interpreter_startup="UNMEASURED_NOT_ZERO",
        bootstrap_containment="TRUSTED_FINITE_PARENT_NOT_CHILD_JOB;CPU_BEFORE_REPORT;FINALIZATION_BOUNDED;PENDING_UNLINK_COMMITS",
        authority="OPERATIONAL_CLOSURE_NOT_MATHEMATICAL_ACCEPTANCE")
    try:
        report_pin = write_new(run/"RESULT.json", encode(report))
        C.rebind_selection(selected)
        for row in (*bootstrap_pins, original_pin, report_pin):
            checked(row)
        if copied_pin is not None:
            checked(copied_pin)
        if copied_entry_pin is not None:
            checked(copied_entry_pin)
        if worker_pin is not None:
            checked(worker_pin)
        if status == "COMMAND_EXITED_ZERO_AND_CLOSED":
            C.validate_worker_report(selection, copied_pin, worker_pin)
        output_census(run, action_output, selection["output_limits"])
        within(deadline)
        need(not (run/"FINALIZATION-FAILED.json").exists(), "PRODUCER_LAUNCH_FINAL_OVERRIDE")
        if status == "COMMAND_EXITED_ZERO_AND_CLOSED":
            checked(pending_pin, 2*MIB)
            # Printed output is provisional too: consumers adopt the saved
            # result only when both failure and pending markers are absent.
            print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)
            within(deadline)
            (run/"FINALIZATION-PENDING.json").unlink()
            # No further failable validation/I/O after this commit. This is a
            # trusted local-filesystem operation, not a power-loss transaction.
            return 0
    except BaseException as error:
        status = "FAIL"
        marker = dict(status="PRODUCER_LAUNCH_FINALIZATION_FAILED", overrides_result=True,
                      error=type(error).__name__+": "+str(error)[:1800])
        try:
            write_new(run/"FINALIZATION-FAILED.json", encode(marker))
        except BaseException as marker_error:
            report["marker_error"] = type(marker_error).__name__+": "+str(marker_error)[:500]
        report.update(status="FAIL", final_error=marker["error"])
    print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

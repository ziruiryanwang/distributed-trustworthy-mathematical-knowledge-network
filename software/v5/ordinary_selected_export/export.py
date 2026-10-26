"""Bounded, fixed-action inert custody export; never mathematical acceptance.

The approved entrypoint/Python/OS and stable owner-controlled source paths are
premises. Only selected approved launcher/codec sources are loaded. No native
checker, owner-catalog or network operation runs, and the package is unchanged.
The private worker action alone does not establish supervised completion.
"""
from __future__ import annotations

import time
START, CPU_START = time.monotonic(), time.process_time()
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import stat
import subprocess
import sys
from types import SimpleNamespace

MIB = 1024**2
REQUEST_SCHEMA = "DMKN_SELECTED_INERT_EXPORT_REQUEST_V1"
RUN_SHA = "47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39"
INVENTORY_SHA = "c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0"
# Ordered imports: only these selected pure codecs enter the worker.
CODECS = (
    ("ordinary_evidence", "installation/py/ordinary_evidence.py", "fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6"),
    ("ordinary_semantics", "installation/py/ordinary_semantics.py", "ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915"),
    ("portable_evidence", "installation/py/portable_evidence.py", "f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8"),
    ("portable_candidate", "authoring/py/portable_candidate.py", "29ae111a362472b09b2b1ff16b567b352be793d76c2cd1b5421e0aee29219331"),
    ("baseline_bundle", "reference/baseline_bundle.py", "d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce"),
    ("ordinary_preview", "authoring/py/ordinary_preview.py", "0fd9bb516fbb53d9d4264271853904e35810286fc92d5670d15d7a9d3c26b0d6"),
    ("portable_preview", "authoring/py/portable_preview.py", "b78dd54340b7b55e4359769d6784f7f225ba304457ce880ce2760717e865550d"),
)
LIMITS = {"wall_seconds": 600, "cpu_seconds": 600, "memory_mib": 2048,
          "active_processes": 1, "stdout_bytes": MIB, "stderr_bytes": MIB}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def strict(raw, *, reports=False):
    def pairs(rows):
        result = {}
        for key, value in rows:
            need(key not in result, "EXPORT_DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    def reject(_):
        raise ValueError("EXPORT_JSON_NUMBER")
    def decimal(value):
        result = float(value)
        need(math.isfinite(result), "EXPORT_REPORT_NUMBER")
        return result
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=decimal if reports else reject, parse_constant=reject)


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("ascii")


def initial_read(path, maximum):
    """Minimal bounded source bootstrap before the pinned path helper loads."""
    need(path.is_absolute() and ".." not in path.parts, "EXPORT_BOOTSTRAP_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "EXPORT_BOOTSTRAP_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "EXPORT_BOOTSTRAP_KIND")
    size = path.stat().st_size
    need(0 < size <= maximum, "EXPORT_BOOTSTRAP_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "EXPORT_BOOTSTRAP_CHANGED")
    return raw


def load_source(name, path, raw):
    need(name not in sys.modules, "EXPORT_PRELOADED_MODULE:"+name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    return module


def setup(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "EXPORT_PYTHON_PROFILE")
    limits = {key: getattr(args, key) for key in LIMITS}
    need(all(type(value) is int and 1 <= value <= LIMITS[key]
             for key, value in limits.items()), "EXPORT_FINITE_LIMITS")
    need(limits["wall_seconds"] >= 5 and limits["cpu_seconds"] >= 1,
         "EXPORT_MINIMUM_ALLOWANCE")
    deadline = START+limits["wall_seconds"]
    if args.worker:
        need(args.deadline is not None and args.original_start is not None and
             args.original_start <= START and START < args.deadline <= deadline,
             "EXPORT_WORKER_ORIGINAL_ALLOWANCE")
        deadline = args.deadline
    else:
        need(args.deadline is None and args.original_start is None, "EXPORT_PRIVATE_WORKER_OPTIONS")
    def check():
        need(time.monotonic() < deadline and
             time.process_time()-CPU_START < limits["cpu_seconds"], "EXPORT_ALLOWANCE_EXHAUSTED")
    check()
    entry = Path(__file__).absolute()
    need(digest(initial_read(entry, 2*MIB)) == args.entry_sha256, "EXPORT_ENTRY_PIN")
    package = Path(args.package)
    run_path = package/"run.py"
    run_raw = initial_read(run_path, 2*MIB)
    need(digest(run_raw) == RUN_SHA, "EXPORT_SUPPORTED_LAUNCHER_SOURCE")
    R = load_source("_selected_export_launch_support", run_path, run_raw)
    package = R.ordinary(package, directory=True)
    python = R.ordinary(args.python_runtime, directory=True)
    R.hexid(args.entry_sha256); R.hexid(args.helper_sha256)
    bound = R.bind_support(package, args.profile_sha256, python, check)
    helper_path = R.ordinary(entry.parent/"selected_export.py")
    helper_raw = R.read(helper_path, 2*MIB, check)
    need(digest(helper_raw) == args.helper_sha256, "EXPORT_HELPER_PIN")
    request_path = R.ordinary(args.request)
    raw = R.read(request_path, MIB, check)
    need(digest(raw) == R.hexid(args.request_sha256), "EXPORT_REQUEST_PIN")
    request = strict(raw)
    need(type(request) is dict and set(request) == {
         "schema", "custody", "targets", "output", "custody_limits", "limits"} and
         request["schema"] == REQUEST_SCHEMA, "EXPORT_REQUEST_SCHEMA")
    need(type(request["custody"]) is str and type(request["output"]) is str,
         "EXPORT_REQUEST_PATHS")
    custody = R.ordinary(request["custody"], directory=True)
    output = R.ordinary(request["output"], directory=True, fresh=True)
    diagnostics = R.ordinary(args.diagnostics, directory=True, fresh=not args.worker)
    protected = [package, python, entry.parent, request_path, diagnostics]
    need(all(not R.overlap(output, path) and not R.overlap(custody, path)
             for path in protected), "EXPORT_STATE_OUTPUT_SUPPORT_OVERLAP")
    need(not R.overlap(output, custody), "EXPORT_CUSTODY_OUTPUT_OVERLAP")
    need(all(not R.overlap(diagnostics, path) for path in
             (package, python, entry.parent, request_path)), "EXPORT_DIAGNOSTIC_INPUT_OVERLAP")
    check()
    return SimpleNamespace(R=R, limits=limits, check=check, deadline=deadline,
        entry=entry, package=package, python=python, bound=bound,
        helper_path=helper_path, helper_raw=helper_raw, request_path=request_path,
        request_raw=raw, request=request, custody=custody, output=output,
        diagnostics=diagnostics, protected=protected)


def load_codecs(s):
    R, check = s.R, s.check
    profile_raw = R.read(s.package/"PROFILE.json", 2*MIB, check)
    installation_raw = R.read(s.package/"installation/INSTALLATION.json", 2*MIB, check)
    need(digest(profile_raw) == s.bound["profile_sha256"] and
         digest(installation_raw) == s.bound["installation_manifest_sha256"],
         "EXPORT_PACKAGE_METADATA_CHANGED")
    profile, installation = strict(profile_raw), strict(installation_raw)
    modules = {}
    for name, relative, expected in CODECS:
        pin = (installation["files"][relative.removeprefix("installation/")]
               if relative.startswith("installation/") else profile["files"][relative])
        need(pin.get("sha256") == expected, "EXPORT_CODEC_VERSION:"+name)
        raw = R.bound_file(s.package/relative, pin, check, source=True)
        modules[name] = load_source(name, s.package/relative, raw)
    inventory_path = s.package/"installation/foundation/inventory.json"
    inventory_pin = installation["files"]["foundation/inventory.json"]
    need(inventory_pin.get("sha256") == INVENTORY_SHA, "EXPORT_INVENTORY_VERSION")
    inventory = R.bound_file(inventory_path, inventory_pin, check, source=True)
    return SimpleNamespace(E=modules["ordinary_evidence"], S=modules["ordinary_semantics"],
        PE=modules["portable_evidence"], B=modules["baseline_bundle"],
        PP=modules["portable_preview"]), inventory


def save_new(path, value):
    raw = canonical(value)
    need(len(raw) <= MIB, "EXPORT_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    need(initial_read(path, MIB) == raw, "EXPORT_REPORT_READBACK")
    return {"bytes": len(raw), "sha256": digest(raw)}


def verify_output(s, expected):
    """Finite exact byte/census verification, never proof checking."""
    R, check = s.R, s.check
    need(type(expected) is dict and expected.get("schema") == "DMKN_ORDINARY_SELECTED_EXPORT_RESULT_V1"
         and expected.get("status") == "INERT_BUNDLE_EXPORTED" and
         expected.get("mathematical_acceptance") is False and
         expected.get("source_acceptance") == "UNASSERTED" and
         expected.get("custody") == str(s.custody) and expected.get("targets") == s.request["targets"],
         "EXPORT_RESULT_DISPOSITION")
    raw = R.read(s.output/"RESULT.json", MIB, check)
    need(strict(raw, reports=True) == expected, "EXPORT_EXACT_RESULT_BINDING")
    pin = expected.get("manifest")
    need(type(pin) is dict and set(pin) == {"path", "bytes", "sha256"} and
         pin["path"] == "manifest.json" and type(pin["bytes"]) is int and
         0 < pin["bytes"] <= 2*MIB, "EXPORT_MANIFEST_DESCRIPTOR")
    manifest_raw = R.read(s.output/"manifest.json", 2*MIB, check)
    need(len(manifest_raw) == pin["bytes"] and digest(manifest_raw) == R.hexid(pin["sha256"]),
         "EXPORT_MANIFEST_PIN")
    manifest = strict(manifest_raw)
    need(type(manifest) is dict and set(manifest) == {"schema", "semantic_id", "batches"} and
         manifest["schema"] == "DMKN_ORDINARY_BASELINE_BUNDLE_V1" and
         manifest["semantic_id"] == expected.get("semantic_id") and
         type(manifest["batches"]) is list and 1 <= len(manifest["batches"]) <= 64,
         "EXPORT_MANIFEST_LAYOUT")
    names, total = set(), 0
    for batch in manifest["batches"]:
        need(type(batch) is list and 1 <= len(batch) <= 1024, "EXPORT_MANIFEST_BATCH")
        for entry in batch:
            check()
            need(type(entry) is dict and set(entry) == {"unit_id", "raw_bytes", "raw_sha256"},
                 "EXPORT_MANIFEST_ENTRY")
            unit = R.hexid(entry["unit_id"])
            need(unit not in names and len(names) < 1024 and type(entry["raw_bytes"]) is int and
                 0 < entry["raw_bytes"] <= 8*MIB, "EXPORT_MANIFEST_UNIT_BOUND")
            names.add(unit); total += entry["raw_bytes"]
            need(total <= 64*MIB, "EXPORT_MANIFEST_TOTAL_BOUND")
            R.bound_file(s.output/"units"/(unit+".json"),
                {"bytes": entry["raw_bytes"], "sha256": entry["raw_sha256"]}, check)
    need(expected.get("counts", {}).get("units") == len(names) and
         expected["counts"].get("evidence_bytes") == total, "EXPORT_RESULT_COUNTS")
    for directory, wanted in ((s.output, {"units", "manifest.json", "RESULT.json"}),
                              (s.output/"units", {name+".json" for name in names})):
        R.ordinary(directory, directory=True)
        actual = set()
        with os.scandir(directory) as listing:
            for entry in listing:
                check(); actual.add(entry.name)
                need(len(actual) <= len(wanted), "EXPORT_OUTPUT_CENSUS_BOUND")
        need(actual == wanted, "EXPORT_OUTPUT_CENSUS")
    check()
    return {"result_sha256": digest(raw), "manifest_sha256": pin["sha256"],
            "units": len(names), "evidence_bytes": total}


def worker(args):
    s = None
    result = {"schema": "DMKN_SELECTED_EXPORT_WORKER_V1", "ok": False,
              "claim": "INERT_EXPORT_SOURCE_ACCEPTANCE_UNASSERTED",
              "supervised_completion": False}
    try:
        s = setup(args)
        api, inventory = load_codecs(s)
        helper = load_source("_selected_export_helper", s.helper_path, s.helper_raw)
        report = helper.export_selected(s.custody, s.request["targets"], s.output,
            api=api, inventory_raw=inventory, custody_limits=s.request["custody_limits"],
            limits=s.request["limits"], check_budget=s.check, protected_paths=s.protected)
        s.check()
        need(s.R.read(s.request_path, MIB, s.check) == s.request_raw, "EXPORT_REQUEST_CHANGED")
        report_raw = s.R.read(s.output/"RESULT.json", MIB, s.check)
        need(strict(report_raw, reports=True) == report, "EXPORT_WORKER_RESULT_READBACK")
        result.update(ok=True, result=report, request_sha256=args.request_sha256,
            profile_sha256=args.profile_sha256, entry_sha256=args.entry_sha256,
            helper_sha256=args.helper_sha256, result_sha256=digest(report_raw))
    except BaseException as error:
        result.update(error_type=type(error).__name__, error=str(error)[:2000],
                      retention="PARTIAL_OUTPUT_PRESERVED_NO_RETRY")
    result["worker_cpu_seconds"] = time.process_time()-CPU_START
    result["worker_wall_seconds"] = time.monotonic()-START
    if s is not None:
        try:
            save_new(s.diagnostics/"WORKER.json", result)
        except BaseException as error:
            result.update(ok=False, report_error=type(error).__name__+": "+str(error)[:1000])
    print(canonical(result).decode("ascii"), flush=True)
    return 0 if result["ok"] else 1


def parent(args):
    s, created = None, False
    result = {"schema": "DMKN_SELECTED_EXPORT_OPERATION_V1", "ok": False,
              "claim": "INERT_EXPORT_SOURCE_ACCEPTANCE_UNASSERTED",
              "status": "NO_WORKER_LAUNCHED", "mathematical_acceptance": False}
    try:
        s = setup(args)
        supervisor, job_class = s.R.load_supervision(s.bound)
        original_environment = supervisor.child_environment
        def environment(cwd):
            value = original_environment(cwd)
            value["PATH"] = os.pathsep.join(map(str, (s.python, s.python/"DLLs")))
            return value
        argv = [str(s.python/"python.exe"), "-I", "-S", "-B", str(s.entry),
            "--worker", "--deadline", repr(s.deadline), "--original-start", repr(START)]
        for key in ("package", "profile_sha256", "python_runtime", "entry_sha256",
                    "helper_sha256", "request", "request_sha256", "diagnostics", *LIMITS):
            argv.extend(("--"+key.replace("_", "-"), str(getattr(args, key))))
        need(len(subprocess.list2cmdline(argv).encode("utf-16-le"))//2 < 32760,
             "EXPORT_COMMAND_LINE_BOUND")
        s.check(); s.diagnostics.mkdir(); created = True
        save_new(s.diagnostics/"LAUNCH.json", {"argv": argv, "limits": s.limits,
            "request_sha256": args.request_sha256, "profile_sha256": args.profile_sha256,
            "entry_sha256": args.entry_sha256, "helper_sha256": args.helper_sha256})
        supervisor.child_environment = environment
        try:
            result["status"] = "WORKER_OUTCOME_PENDING"
            supervision = supervisor.supervise(argv, s.diagnostics, s.diagnostics/"child",
                                               s.limits, job_class, started=START)
        finally:
            supervisor.child_environment = original_environment
        save_new(s.diagnostics/"SUPERVISION.json", supervision)
        clean = (s.R.operational_result(supervision)["ok"] and
                 supervision.get("termination_requested") is False)
        need(clean, "EXPORT_WORKER_NOT_CLEANLY_COMPLETE")
        s.check()
        child_raw = s.R.read(s.diagnostics/"WORKER.json", MIB, s.check)
        child = strict(child_raw, reports=True)
        need(type(child) is dict and child.get("schema") == "DMKN_SELECTED_EXPORT_WORKER_V1" and
             child.get("ok") is True and child.get("supervised_completion") is False and
             all(child.get(key) == getattr(args, key) for key in
                 ("request_sha256", "profile_sha256", "entry_sha256", "helper_sha256")),
             "EXPORT_WORKER_REPORT_BINDING")
        need(s.R.read(s.request_path, MIB, s.check) == s.request_raw, "EXPORT_FINAL_REQUEST_CHANGED")
        verified = verify_output(s, child["result"])
        need(child.get("result_sha256") == verified["result_sha256"], "EXPORT_FINAL_OUTPUT_CHANGED")
        result.update(ok=True, status="INERT_EXPORT_COMPLETE", result=child["result"],
            worker_report_sha256=digest(child_raw),
            profile_sha256=args.profile_sha256, request_sha256=args.request_sha256,
            output_verified=verified,
            closure="EXIT_ZERO_REAPED_JOB_CLOSED_ZERO_ACTIVE_ZERO_TERMINATED_NO_CLEANUP_ERROR",
            supervisor_scope="ONE_WORKER_JOB;TRUSTED_WRAPPER_CPU_SEPARATE")
    except BaseException as error:
        result.update(ok=False, error_type=type(error).__name__, error=str(error)[:2000],
                      retention="PARTIAL_OUTPUT_PRESERVED_NO_RETRY")
    result["wrapper_cpu_seconds"] = time.process_time()-CPU_START
    result["wall_seconds"] = time.monotonic()-START
    if created:
        try:
            save_new(s.diagnostics/"RUN.json", result)
        except BaseException as error:
            result.update(ok=False, report_error=type(error).__name__+": "+str(error)[:1000])
    print(canonical(result).decode("ascii"), flush=True)
    return 0 if result["ok"] else 1


def arguments():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("package", "profile-sha256", "python-runtime", "entry-sha256",
                 "helper-sha256", "request", "request-sha256", "diagnostics"):
        parser.add_argument("--"+name, required=True)
    for key in LIMITS:
        parser.add_argument("--"+key.replace("_", "-"), required=True, type=int)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--deadline", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--original-start", type=float, help=argparse.SUPPRESS)
    return parser.parse_args()


if __name__ == "__main__":
    selected = arguments()
    raise SystemExit(worker(selected) if selected.worker else parent(selected))

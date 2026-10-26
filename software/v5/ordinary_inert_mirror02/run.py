"""Two finite source-only inert-mirror actions; no Lean or mathematical authority.

Approved code/Python/Windows and protected local paths are prerequisites. The
fixed manifest selects software, never peer input. Only the parent may promote
prepared data to READY after successful Job supervision and exact report checks.
"""
from __future__ import annotations

import time
START, CPU_START = time.monotonic(), time.process_time()
import argparse
import asyncio
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import stat
import subprocess
import sys
from types import ModuleType, SimpleNamespace

MIB = 1024**2
SOURCE_SHA = "1bc43d4c9896476443d0d6aab95015db7af32bc46a04cfb1624a5c40e638feb9"
CLOSURE = "EXIT_ZERO_REAPED_JOB_CLOSED_ZERO_ACTIVE_ZERO_TERMINATED_NO_CLEANUP_ERROR"
READY_FIELDS = {"schema", "status", "descriptor_sha256", "request_sha256",
    "source_manifest_sha256", "entry_sha256", "helper_sha256", "worker_report_sha256",
    "supervision_report_sha256", "closure", "mathematical_acceptance"}
CEILINGS = {"wall_seconds": 3600, "cpu_seconds": 600, "memory_mib": 2048,
            "active_processes": 1, "stdout_bytes": MIB, "stderr_bytes": MIB}
ORDER = (
    "ordinary_evidence", "ordinary_semantics", "portable_evidence", "portable_candidate",
    "ordinary_preview", "portable_preview", "formal_query", "baseline_bundle",
    "discovery.formal_features", "discovery.authenticated_index", "discovery.pair_access",
    "discovery.discovery_store", "discovery.discovery_query", "discovery.candidate_query",
    "discovery.summary_wire", "discovery.ordinary_export_adapter", "custody.module_store",
    "transport.http_provider", "transport.clients", "transport.ordinary_acquisition",
    "transport.authoring_offers", "transport.contact_directory")
ALIASES = {"E": "ordinary_evidence", "S": "ordinary_semantics", "PE": "portable_evidence",
    "B": "baseline_bundle", "PP": "portable_preview", "O": "transport.ordinary_acquisition",
    "DS": "discovery.discovery_store", "OA": "discovery.ordinary_export_adapter",
    "H": "transport.http_provider", "F": "discovery.formal_features",
    "C": "discovery.candidate_query", "Q": "discovery.discovery_query",
    "W": "discovery.summary_wire"}


def need(ok, code):
    if not ok:
        raise ValueError("INERT_MIRROR_" + code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def strict(raw, *, reports=False):
    def pairs(rows):
        value = {}
        for key, item in rows:
            need(key not in value, "DUPLICATE_JSON_KEY")
            value[key] = item
        return value
    def reject(_):
        raise ValueError("INERT_MIRROR_JSON_NUMBER")
    def decimal(value):
        result = float(value)
        need(math.isfinite(result), "REPORT_NUMBER")
        return result
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
        parse_float=decimal if reports else reject, parse_constant=reject)


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                      separators=(",", ":")).encode("ascii")


def initial_read(path, maximum):
    """Bounded bootstrap before the pinned ordinary-path helper is available."""
    path = Path(path)
    need(path.is_absolute() and ".." not in path.parts and path != Path(path.anchor),
         "BOOTSTRAP_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "BOOTSTRAP_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "BOOTSTRAP_KIND")
    size = path.stat().st_size
    need(0 < size <= maximum, "BOOTSTRAP_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    need(len(raw) == size and path.stat().st_size == size, "BOOTSTRAP_CHANGED")
    return raw


def load_source(name, path, raw):
    need(name not in sys.modules, "PRELOADED_MODULE:" + name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    if "." in name:
        parent, child = name.rsplit(".", 1)
        setattr(sys.modules[parent], child, module)
    return module


def source_inputs(source_root, check_budget):
    """Validate the fixed closure without executing any mathematical package."""
    need(callable(check_budget), "BUDGET_CALLBACK")
    check_budget()
    root = Path(source_root)
    manifest_raw = initial_read(Path(__file__).absolute().parent / "SOURCES.json", MIB)
    need(digest(manifest_raw) == SOURCE_SHA, "FIXED_SOURCE_MANIFEST")
    manifest = strict(manifest_raw)
    need(manifest["schema"] == "DMKN_INERT_MIRROR_SOURCES_V1" and
         set(manifest["files"]) == set(ORDER) | {"_launcher", "_inventory", "_supervisor", "domains", "_job"},
         "SOURCE_ROLE_SET")
    selected = manifest["files"]["_launcher"]
    path = root / selected["source"]
    raw = initial_read(path, 2*MIB)
    need(len(raw) == selected["bytes"] and digest(raw) == selected["sha256"], "LAUNCHER_PIN")
    R = load_source("_inert_mirror_launch", path, raw)
    root = R.ordinary(root, directory=True)
    ancestor = R.read(root / "INVESTIGATOR-SOURCE-MANIFEST.json", 2*MIB, check_budget)
    need(digest(ancestor) == manifest["source_manifest_sha256"], "INVESTIGATOR_SOURCE_SELECTION")
    raws, paths = {}, {}
    for name, pin in manifest["files"].items():
        check_budget()
        path = root / pin["source"]
        raws[name] = R.bound_file(path, {key: pin[key] for key in ("bytes", "sha256")},
                                 check_budget, source=True)
        paths[name] = path
    need(digest(raws["_launcher"]) == digest(raw), "LOADED_LAUNCHER_CHANGED")
    check_budget()
    return SimpleNamespace(root=root, R=R, manifest=manifest, paths=paths, raws=raws,
                           manifest_sha256=SOURCE_SHA)


def load_libraries(bound, check_budget):
    """Use exact names and no ambient package search paths for selected modules."""
    bases = ("discovery", "transport", "custody")
    need(not any(name in ORDER or any(name == base or name.startswith(base + ".")
             for base in bases) for name in sys.modules), "PRELOADED_SUPPORT")
    for name in bases:
        package = ModuleType(name)
        package.__package__, package.__path__ = name, []
        package.__spec__ = importlib.util.spec_from_loader(name, loader=None, is_package=True)
        package.__spec__.submodule_search_locations = []
        sys.modules[name] = package
    modules = {}
    for name in ORDER:
        check_budget()
        modules[name] = load_source(name, bound.paths[name], bound.raws[name])
    api = {key: modules[name] for key, name in ALIASES.items()}
    api["D"] = api["DS"]
    api["R"] = bound.R
    need(digest(bound.raws["_inventory"]) == api["S"].INVENTORY, "INVENTORY_SEMANTICS")
    check_budget()
    return SimpleNamespace(**{key: api[key] for key in ALIASES}, modules=modules, api=api,
        inventory_raw=bound.raws["_inventory"], manifest_sha256=SOURCE_SHA, R=bound.R)


def load_support(source_root, check_budget):
    """Public source-only loader; includes fixed-manifest and exact-file validation."""
    return load_libraries(source_inputs(source_root, check_budget), check_budget)


def setup(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and sys.maxsize > 2**32 and
         sys.byteorder == "little" and sys.version_info[:3] == (3, 14, 6), "PYTHON_PROFILE")
    limits = {key: getattr(args, key) for key in CEILINGS}
    need(all(type(value) is int and 1 <= value <= CEILINGS[key]
             for key, value in limits.items()), "FINITE_LIMITS")
    need(limits["wall_seconds"] >= 5, "MINIMUM_ALLOWANCE")
    deadline = START + limits["wall_seconds"]
    if args.worker:
        need(type(args.deadline) is float and math.isfinite(args.deadline) and
             type(args.original_start) is float and math.isfinite(args.original_start) and
             args.original_start <= START < args.deadline <= deadline, "ORIGINAL_ALLOWANCE")
        deadline = args.deadline
    else:
        need(args.deadline is None and args.original_start is None, "PRIVATE_WORKER_OPTIONS")
    def check():
        need(time.monotonic() < deadline and time.process_time() - CPU_START < limits["cpu_seconds"],
             "ALLOWANCE_EXHAUSTED")
    check()
    entry = Path(__file__).absolute()
    need(digest(initial_read(entry, 2*MIB)) == args.entry_sha256, "ENTRY_PIN")
    need(args.source_manifest_sha256 == SOURCE_SHA, "SOURCE_MANIFEST_SELECTION")
    bound = source_inputs(Path(args.source_root), check)
    R = bound.R
    for key in ("entry_sha256", "helper_sha256", "request_sha256"):
        R.hexid(getattr(args, key))
    python = R.ordinary(args.python_runtime, directory=True)
    need(R.ordinary(Path(sys.executable)) == python / "python.exe", "RUNNING_PYTHON")
    for relative, pin in bound.manifest["python"]["files"].items():
        R.bound_file(python / relative, pin, check)
    helper_path = R.ordinary(entry.parent / "mirror.py")
    helper_raw = R.read(helper_path, 2*MIB, check)
    need(digest(helper_raw) == args.helper_sha256, "HELPER_PIN")
    request_path = R.ordinary(args.request)
    request_raw = R.read(request_path, MIB, check)
    need(digest(request_raw) == args.request_sha256, "REQUEST_PIN")
    request = strict(request_raw)
    need(type(request) is dict, "REQUEST_OBJECT")
    diagnostics = R.ordinary(args.diagnostics, directory=True, fresh=not args.worker)
    protected = (bound.root, python, entry.parent, request_path)
    need(all(not R.overlap(diagnostics, path) for path in protected), "DIAGNOSTICS_OVERLAP")
    if args.operation == "prepare":
        required = {"schema", "bundle_directory", "manifest_sha256", "targets", "output_directory",
                    "share_all_bundle", "limits"}
        need(required <= set(request) <= required | {"custody_limits", "index_limits"} and
             request["schema"] == "DMKN_INERT_MIRROR_PREPARE_REQUEST_V1", "PREPARE_FIELDS")
        bundle = R.ordinary(request["bundle_directory"], directory=True)
        state = R.ordinary(request["output_directory"], directory=True, fresh=True)
        R.hexid(request["manifest_sha256"])
        need(request["share_all_bundle"] is True, "WHOLE_BUNDLE_DISCLOSURE")
        need(not R.overlap(state, bundle) and not R.overlap(diagnostics, bundle), "BUNDLE_OVERLAP")
    else:
        need(set(request) == {"schema", "prepared_directory", "descriptor_sha256", "ready_sha256", "config"}
             and request["schema"] == "DMKN_INERT_MIRROR_SERVE_REQUEST_V1", "SERVE_FIELDS")
        state = R.ordinary(request["prepared_directory"], directory=True)
        bundle = None
        R.hexid(request["descriptor_sha256"]); R.hexid(request["ready_sha256"])
    need(not R.overlap(state, diagnostics) and
         all(not R.overlap(state, path) for path in protected), "STATE_SUPPORT_OVERLAP")
    check()
    result = SimpleNamespace(R=R, bound=bound, check=check, deadline=deadline, limits=limits,
        entry=entry, python=python, helper_path=helper_path, helper_raw=helper_raw,
        request=request, request_path=request_path, request_raw=request_raw,
        diagnostics=diagnostics, state=state, bundle=bundle, protected=protected)
    if args.operation == "serve":
        verify_ready(result, args)
    return result


def verify_ready(s, args):
    descriptor = s.R.read(s.state / "DESCRIPTOR.json", 2*MIB, s.check)
    ready_raw = s.R.read(s.state / "READY.json", MIB, s.check)
    need(digest(descriptor) == s.request["descriptor_sha256"] and
         digest(ready_raw) == s.request["ready_sha256"], "PREPARED_SELECTION")
    ready = strict(ready_raw)
    need(type(ready) is dict and set(ready) == READY_FIELDS and
         ready["schema"] == "DMKN_INERT_MIRROR_READY_V1" and ready["status"] == "INERT_MIRROR_READY" and
         ready["mathematical_acceptance"] is False and ready["closure"] == CLOSURE and
         ready["descriptor_sha256"] == s.request["descriptor_sha256"], "PREPARED_READY")
    for key in ("descriptor_sha256", "request_sha256", "source_manifest_sha256", "entry_sha256",
                "helper_sha256", "worker_report_sha256", "supervision_report_sha256"):
        s.R.hexid(ready[key])
    need(ready["source_manifest_sha256"] == SOURCE_SHA and
         ready["entry_sha256"] == args.entry_sha256 and ready["helper_sha256"] == args.helper_sha256,
         "PREPARED_SUPPORT_CHANGED")
    return descriptor, ready_raw


def save_new(path, value):
    raw = canonical(value)
    need(0 < len(raw) <= MIB, "REPORT_BOUND")
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "REPORT_SHORT_WRITE")
        stream.flush(); os.fsync(stream.fileno())
    need(initial_read(path, MIB) == raw, "REPORT_READBACK")
    return digest(raw)


def worker(args):
    s = None
    report = {"schema": "DMKN_INERT_MIRROR_WORKER_V1", "ok": False,
        "operation": args.operation, "mathematical_acceptance": False,
        "supervised_completion": False}
    try:
        s = setup(args)
        loaded = load_libraries(s.bound, s.check)
        core = load_source("_inert_mirror_core", s.helper_path, s.helper_raw)
        if args.operation == "prepare":
            manifest_raw = s.R.read(s.bundle / "manifest.json", 2*MIB, s.check)
            options = {key: s.request[key] for key in ("custody_limits", "index_limits") if key in s.request}
            result = core.prepare(bundle_directory=s.bundle, manifest_raw=manifest_raw,
                manifest_sha256=s.request["manifest_sha256"], targets=s.request["targets"],
                inventory_raw=loaded.inventory_raw, output_directory=s.state, api=loaded.api,
                limits=s.request["limits"], check_budget=s.check,
                protected_paths=(*s.protected, s.diagnostics), share_all_bundle=True, **options)
        else:
            descriptor, ready_raw = verify_ready(s, args)
            def ready(value):
                s.check()
                save_new(s.diagnostics / "SERVICE-READY.json", value)
            result = asyncio.run(core.serve(prepared_directory=s.state,
                descriptor_raw=descriptor, descriptor_sha256=s.request["descriptor_sha256"],
                ready_raw=ready_raw, ready_sha256=s.request["ready_sha256"], config=s.request["config"],
                api=loaded.api, check_budget=s.check, deadline=s.deadline, ready=ready))
        s.check()
        need(s.R.read(s.request_path, MIB, s.check) == s.request_raw, "REQUEST_CHANGED")
        report.update(ok=True, result=result, request_sha256=args.request_sha256,
            source_manifest_sha256=SOURCE_SHA, entry_sha256=args.entry_sha256,
            helper_sha256=args.helper_sha256)
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:2000],
                      retention="PARTIAL_OUTPUT_RETAINED_NOT_READY_NO_RETRY")
        if hasattr(error, "report"):
            report["detail"] = error.report
    report["worker_cpu_seconds"] = time.process_time() - CPU_START
    report["worker_wall_seconds"] = time.monotonic() - START
    if s is not None:
        try:
            save_new(s.diagnostics / "WORKER.json", report)
        except BaseException as error:
            report.update(ok=False, report_error=type(error).__name__ + ": " + str(error)[:1000])
    print(canonical(report).decode("ascii"), flush=True)
    return 0 if report["ok"] else 1


def parent(args):
    s, created = None, False
    report = {"schema": "DMKN_INERT_MIRROR_OPERATION_V1", "ok": False,
        "operation": args.operation, "status": "NO_WORKER_LAUNCHED",
        "mathematical_acceptance": False}
    try:
        s = setup(args)
        selected = {role: (s.bound.paths[name], s.bound.raws[name]) for role, name in
                    (("supervisor", "_supervisor"), ("domains", "domains"), ("job", "_job"))}
        supervisor, Job = s.R.load_supervision({"support": selected})
        previous_environment = supervisor.child_environment
        def environment(cwd):
            value = previous_environment(cwd)
            value["PATH"] = os.pathsep.join(map(str, (s.python, s.python / "DLLs")))
            return value
        argv = [str(s.python / "python.exe"), "-I", "-S", "-B", str(s.entry), args.operation,
                "--worker", "--deadline", repr(s.deadline), "--original-start", repr(START)]
        for key in ("source_root", "source_manifest_sha256", "python_runtime", "entry_sha256",
                    "helper_sha256", "request", "request_sha256", "diagnostics", *CEILINGS):
            argv.extend(("--" + key.replace("_", "-"), str(getattr(args, key))))
        need(len(subprocess.list2cmdline(argv).encode("utf-16-le")) // 2 < 32760, "COMMAND_LINE_BOUND")
        s.check(); s.diagnostics.mkdir(); created = True
        save_new(s.diagnostics / "LAUNCH.json", {"argv": argv, "limits": s.limits,
            "request_sha256": args.request_sha256, "source_manifest_sha256": SOURCE_SHA})
        supervisor.child_environment = environment
        try:
            report["status"] = "WORKER_OUTCOME_PENDING"
            supervision = supervisor.supervise(argv, s.diagnostics, s.diagnostics / "child",
                                               s.limits, Job, started=START)
        finally:
            supervisor.child_environment = previous_environment
        supervision_sha = save_new(s.diagnostics / "SUPERVISION.json", supervision)
        need(s.R.operational_result(supervision)["ok"] and
             supervision.get("termination_requested") is False, "WORKER_NOT_CLEANLY_COMPLETE")
        s.check()
        raw = s.R.read(s.diagnostics / "WORKER.json", MIB, s.check)
        child = strict(raw, reports=True)
        need(type(child) is dict and child.get("schema") == "DMKN_INERT_MIRROR_WORKER_V1" and
             child.get("ok") is True and child.get("operation") == args.operation and
             child.get("mathematical_acceptance") is False and child.get("supervised_completion") is False and
             all(child.get(key) == getattr(args, key) for key in
                 ("request_sha256", "source_manifest_sha256", "entry_sha256", "helper_sha256")),
             "WORKER_REPORT_BINDING")
        need(s.R.read(s.request_path, MIB, s.check) == s.request_raw, "FINAL_REQUEST_CHANGED")
        result = child["result"]
        need(type(result) is dict and result.get("mathematical_acceptance") is False, "RESULT_ASSURANCE")
        report.update(result=result, worker_report_sha256=digest(raw), supervision_report_sha256=supervision_sha,
            request_sha256=args.request_sha256, source_manifest_sha256=SOURCE_SHA,
            closure=CLOSURE, supervisor_scope="ONE_WORKER_JOB;TRUSTED_WRAPPER_CPU_SEPARATE")
        if args.operation == "prepare":
            need(result.get("status") == "PREPARED_DATA_NOT_SUPERVISED_READY" and
                 result.get("descriptor_path") == str(s.state / "DESCRIPTOR.json"), "PREPARE_RESULT")
            descriptor_raw = s.R.read(s.state / "DESCRIPTOR.json", 2*MIB, s.check)
            need(digest(descriptor_raw) == s.R.hexid(result["descriptor_sha256"]), "PREPARE_DESCRIPTOR_PIN")
            descriptor = strict(descriptor_raw)
            need(type(descriptor) is dict and descriptor.get("schema") == "DMKN_INERT_MIRROR_DESCRIPTOR_V1"
                 and descriptor.get("status") == "PREPARED_DATA_NOT_SUPERVISED_READY" and
                 descriptor.get("mathematical_acceptance") is False, "PREPARE_DESCRIPTOR_ASSURANCE")
            ready = {"schema": "DMKN_INERT_MIRROR_READY_V1", "status": "INERT_MIRROR_READY",
                "descriptor_sha256": result["descriptor_sha256"], "request_sha256": args.request_sha256,
                "source_manifest_sha256": SOURCE_SHA, "entry_sha256": args.entry_sha256,
                "helper_sha256": args.helper_sha256, "worker_report_sha256": digest(raw),
                "supervision_report_sha256": supervision_sha, "closure": CLOSURE,
                "mathematical_acceptance": False}
            # All fallible reporting/checking precedes promotion. RUN alone is
            # explicitly not public completion; only the final READY seal is.
            report.update(status="PREPARED_ELIGIBLE_FOR_READY_COMMIT", ready_sha256=digest(canonical(ready)))
            report["wrapper_cpu_seconds"] = time.process_time() - CPU_START
            report["wall_seconds"] = time.monotonic() - START
            save_new(s.diagnostics / "RUN.json", report)
            pending = s.R.ordinary(s.state / "READY-PENDING.json", fresh=True)
            save_new(pending, ready)
            s.check()
            ready_path = s.R.ordinary(s.state / "READY.json", fresh=True)
            # Windows rename refuses an existing destination. Promotion is the
            # final state action: preseal reporting/readback can never expose
            # READY, and a retained READY-PENDING file is not service authority.
            os.rename(pending, ready_path)
            report.update(ok=True, status="INERT_MIRROR_PREPARE_COMPLETE", ready_path=str(ready_path))
        else:
            need(result.get("status") == "LEASE_FINISHED" and result.get("quiescent") is True and
                 result.get("cleanup_errors") == [], "SERVICE_NOT_CLEANLY_COMPLETE")
            verify_ready(s, args)
            report.update(ok=True, status="INERT_MIRROR_SERVE_COMPLETE")
            report["wrapper_cpu_seconds"] = time.process_time() - CPU_START
            report["wall_seconds"] = time.monotonic() - START
            s.check(); save_new(s.diagnostics / "RUN.json", report)
    except BaseException as error:
        report.update(ok=False, error_type=type(error).__name__, error=str(error)[:2000],
                      retention="PARTIAL_OUTPUT_RETAINED_NO_AUTOMATIC_RETRY")
        if created and not (s.diagnostics / "RUN.json").exists():
            try:
                save_new(s.diagnostics / "RUN.json", report)
            except BaseException as nested:
                report["report_error"] = type(nested).__name__ + ": " + str(nested)[:1000]
    print(canonical(report).decode("ascii"), flush=True)
    return 0 if report["ok"] else 1


def arguments():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("operation", choices=("prepare", "serve"))
    for name in ("source-root", "source-manifest-sha256", "python-runtime", "entry-sha256",
                 "helper-sha256", "request", "request-sha256", "diagnostics"):
        parser.add_argument("--" + name, required=True)
    for key in CEILINGS:
        parser.add_argument("--" + key.replace("_", "-"), type=int, required=True)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--deadline", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--original-start", type=float, help=argparse.SUPPRESS)
    return parser.parse_args()


if __name__ == "__main__":
    selected = arguments()
    raise SystemExit(worker(selected) if selected.worker else parent(selected))

"""One finite Windows/Python inert-host operation under the existing Job supervisor.

The external profile pin selects local software. Configurations and bundles never
select code. All mathematical bytes remain inert; consumers independently check.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
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
CEILINGS = {"wall_seconds": 3600, "cpu_seconds": 600, "memory_mib": 8192,
            "active_processes": 8, "stdout_bytes": 8*MIB, "stderr_bytes": 8*MIB}
CLOSURE = "EXIT_ZERO_REAPED_JOB_CLOSED_ZERO_ACTIVE_ZERO_TERMINATED_NO_CLEANUP_ERROR"


def need(condition, code):
    if not condition:
        raise ValueError("INERT_RUN_" + code)


def encode(value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":")).encode("ascii")
    need(0 < len(raw) <= 16*MIB, "REPORT_BOUND")
    return raw


class Allowance:
    """Shared original wall deadline; worker Job and trusted wrapper CPU differ.

    --cpu-seconds caps the worker's Job, not aggregate wrapper-plus-worker CPU.
    The wrapper separately checks min(60, cpu-seconds) cooperatively. Its measured
    CPU is reported separately and is not charged a second time as worker CPU.
    """
    def __init__(self, args):
        self.limits = {key: getattr(args, key) for key in CEILINGS}
        need(all(type(value) is int and 1 <= value <= CEILINGS[key]
                 for key, value in self.limits.items()), "EXPLICIT_FINITE_LIMITS")
        need(args.wall_seconds >= 35 and args.cpu_seconds >= 4, "MINIMUM_ALLOWANCE")
        self.deadline = START_WALL + args.wall_seconds
        self.original_start = START_WALL
        if args.worker:
            need(type(args.deadline) is float and math.isfinite(args.deadline) and
                 type(args.original_start) is float and math.isfinite(args.original_start) and
                 args.original_start <= START_WALL < args.deadline <= self.deadline and
                 args.deadline == args.original_start + args.wall_seconds, "ORIGINAL_ALLOWANCE")
            self.deadline, self.original_start = args.deadline, args.original_start
        else:
            need(args.deadline is None and args.original_start is None, "PRIVATE_WORKER_OPTIONS")
        self.cpu_seconds, self.memory_mib = args.cpu_seconds, args.memory_mib
        self.local_cpu_limit = args.cpu_seconds if args.worker else min(60, args.cpu_seconds)

    def check(self):
        need(time.monotonic() < self.deadline and
             time.process_time() - START_CPU < self.local_cpu_limit, "ORIGINAL_ALLOWANCE_EXHAUSTED")

    def remaining_cpu(self):
        self.check()
        return self.local_cpu_limit - (time.process_time() - START_CPU)

    def report(self):
        return {"wall_seconds": time.monotonic() - self.original_start,
                "controller_cpu_seconds": time.process_time() - START_CPU,
                "worker_cpu_seconds": 0,
                "controller_limits": "COOPERATIVE;PUBLIC_WORKER_SEPARATELY_JOB_SUPERVISED",
                "cpu_scope": "THIS_PROCESS_ONLY_NOT_AGGREGATE_WRAPPER_PLUS_WORKER",
                "local_cooperative_cpu_limit_seconds": self.local_cpu_limit}


def initial_read(path, check):
    """Bounded bootstrap before the selected ordinary-path helper is executed."""
    need(path.is_absolute() and ".." not in path.parts and path != Path(path.anchor),
         "BOOTSTRAP_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "BOOTSTRAP_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "BOOTSTRAP_KIND")
    check()
    size = path.stat().st_size
    need(0 < size <= 2*MIB, "BOOTSTRAP_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    check()
    need(len(raw) == size and path.stat().st_size == size, "BOOTSTRAP_CHANGED")
    return raw


def bootstrap(root, expected, check):
    need(type(expected) is str and len(expected) == 64 and
         all(c in "0123456789abcdef" for c in expected), "PROFILE_HASH")
    raw = initial_read(root / "SOURCES.json", check)
    need(hashlib.sha256(raw).hexdigest() == expected, "PROFILE_PIN")
    def pairs(rows):
        value = {}
        for key, item in rows:
            need(key not in value, "DUPLICATE_JSON_KEY")
            value[key] = item
        return value
    def reject(_):
        raise ValueError("INERT_RUN_JSON_NUMBER")
    manifest = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                          parse_float=reject, parse_constant=reject)
    need(type(manifest) is dict and type(manifest.get("files")) is dict, "PROFILE_OBJECT")
    selected = {}
    for name, filename in (("_entry", "run.py"), ("_support", "support.py")):
        pin = manifest["files"].get(name)
        need(type(pin) is dict and set(pin) == {"path", "source", "bytes", "sha256"} and
             pin["path"] == filename and type(pin["bytes"]) is int and
             0 < pin["bytes"] <= 2*MIB, "BOOTSTRAP_PIN")
        selected[name] = initial_read(root / filename, check)
        need(len(selected[name]) == pin["bytes"] and
             hashlib.sha256(selected[name]).hexdigest() == pin["sha256"], "BOOTSTRAP_SOURCE_PIN")
    name, path = "inert_host_support", root / "support.py"
    need(name not in sys.modules, "SUPPORT_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(selected["_support"], str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    return module, raw, selected


def setup(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON_PROFILE")
    need((args.operation in ("append", "serve")) == (args.host_sha256 is not None),
         "HOST_SEAL_PIN_MODE")
    allowance = Allowance(args)
    root = Path(__file__).absolute().parent
    R, manifest_raw, captured = bootstrap(root, args.profile_sha256, allowance.check)
    bound = R.bind(root, args.profile_sha256, args.python_runtime, allowance.check)
    need(bound.manifest_raw == manifest_raw and
         all(bound.raws[name] == raw for name, raw in captured.items()), "BOOTSTRAP_SELECTION_CHANGED")
    config_path = R.ordinary(args.config)
    config_raw = R.read(config_path, 2*MIB, allowance.check)
    need(R.digest(config_raw) == R.hexid(args.config_sha256), "CONFIG_PIN")
    config = R.strict(config_raw)
    need(type(config) is dict, "CONFIG_OBJECT")
    if args.host_sha256 is not None:
        R.hexid(args.host_sha256)
    host_root = R.ordinary(args.host_root, directory=True,
                           fresh=args.operation in ("init", "prepare"))
    output = R.ordinary(args.output, directory=True, fresh=True)
    diagnostics = R.ordinary(args.diagnostics, directory=True, fresh=not args.worker)
    R.separated([root, bound.python_root, host_root, output, diagnostics], "STATE_SUPPORT_LOG_OVERLAP")
    R.reject_dedicated(output)
    R.reject_dedicated(diagnostics)
    inputs = [config_path]
    if args.operation in ("prepare", "append"):
        need(type(config.get("bundle_directory")) is str and type(config.get("manifest")) is dict
             and type(config["manifest"].get("path")) is str, "BUNDLE_INPUT_PATHS")
        inputs.extend((R.ordinary(config["bundle_directory"], directory=True),
                       R.ordinary(config["manifest"]["path"])))
    elif args.operation == "serve" and config.get("tls") is not None:
        tls = config["tls"]
        need(type(tls) is dict and all(type(tls.get(k)) is str for k in ("cert_file", "key_file")),
             "TLS_INPUT_PATHS")
        inputs.extend(R.ordinary(tls[k]) for k in ("cert_file", "key_file"))
    for source in inputs:
        need(all(not R.overlap(source, target) for target in (host_root, output, diagnostics)),
             "INPUT_WRITABLE_OVERLAP")
    allowance.check()
    return SimpleNamespace(R=R, bound=bound, allowance=allowance, config_path=config_path,
        config_raw=config_raw, config=config, host_root=host_root, output=output,
        diagnostics=diagnostics, root=root)


def reverify(s):
    need(s.R.read(s.config_path, 2*MIB, s.allowance.check) == s.config_raw, "CONFIG_CHANGED")
    s.bound.verify(s.allowance.check)
    s.allowance.check()


def worker(args):
    s, created, result, phase = None, False, None, "SETUP"
    report = {"schema": "DMKN_INERT_HOST_WORKER_V1", "ok": False,
        "operation": args.operation, "mathematical_acceptance": False,
        "mathematical_owner_opened": False, "supervised_completion": False}
    try:
        s = setup(args)
        support = s.R.load_support(s.bound, s.allowance.check)
        core = s.R.load_source("_inert_host_core", s.bound.paths["_core"], s.bound.raws["_core"])
        def finalize():
            need(support.read(s.config_path, 2*MIB) == s.config_raw, "CONFIG_CHANGED")
            support.verify()
            s.allowance.check()
        finalize()
        s.output.mkdir()
        created = True
        phase = args.operation.upper()
        keywords = {"profile_sha256": args.profile_sha256, "finalize": finalize}
        if args.operation in ("append", "serve"):
            keywords["expected_host_sha256"] = args.host_sha256
        if args.operation == "serve":
            def ready(value):
                s.allowance.check()
                support.write_fresh(s.output / "READY.json", encode(value))
            keywords["ready"] = ready
        action = core.initialize if args.operation == "init" else getattr(core, args.operation)
        result = action(support, s.host_root, s.config, s.allowance, **keywords)
        finalize()
        report.update(ok=True, result=result, profile_sha256=args.profile_sha256,
            config_sha256=args.config_sha256, host_root=str(s.host_root),
            semantic_id=support.semantic_id, namespace=support.namespace)
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:2000], phase=phase,
            result=result, retention="PRESERVE_PARTIAL_HOST_AND_OUTPUT_NO_AUTOMATIC_RETRY")
        if hasattr(error, "report"):
            report["detail"] = error.report
    report["cost"] = s.allowance.report() if s is not None else {
        "wall_seconds": time.monotonic() - START_WALL,
        "controller_cpu_seconds": time.process_time() - START_CPU, "worker_cpu_seconds": 0}
    try:
        raw = encode(report)
        if created:
            s.R.write_fresh(s.output / "RESULT.json", raw, s.allowance.check)
    except BaseException as error:
        report.update(ok=False, final_report_error=type(error).__name__ + ": " + str(error)[:1000],
            retention="HOST_EFFECTS_PRESERVED_REPORT_NOT_CONFIRMED_NO_AUTOMATIC_RETRY")
        raw = encode(report)
    sys.stdout.buffer.write(raw + b"\n")
    sys.stdout.buffer.flush()
    return 0 if report["ok"] else 1


def parent(args):
    s, created, entered, supervisor = None, False, False, None
    report = {"schema": "DMKN_INERT_HOST_OPERATION_V1", "ok": False,
        "operation": args.operation, "status": "NO_WORKER_LAUNCHED",
        "mathematical_acceptance": False, "mathematical_owner_opened": False}
    try:
        s = setup(args)
        supervisor, Job = s.R.load_supervision(s.bound)
        need(supervisor.limits_checked(s.allowance.limits) == s.allowance.limits, "SUPERVISOR_LIMITS")
        original_environment = supervisor.child_environment
        def environment(cwd):
            value = original_environment(cwd)
            value["PATH"] = os.pathsep.join(map(str, (s.bound.python_root, s.bound.python_root / "DLLs")))
            return value
        argv = [str(s.bound.python_root / "python.exe"), "-I", "-S", "-B",
                str(s.root / "run.py"), args.operation, "--worker", "--deadline",
                repr(s.allowance.deadline), "--original-start", repr(START_WALL)]
        for key in ("profile_sha256", "python_runtime", "host_root", "config", "config_sha256",
                    "output", "diagnostics", *CEILINGS):
            argv.extend(("--" + key.replace("_", "-"), str(getattr(args, key))))
        if args.host_sha256 is not None:
            argv.extend(("--host-sha256", args.host_sha256))
        need(len(subprocess.list2cmdline(argv).encode("utf-16-le")) // 2 < 32760, "COMMAND_LINE_BOUND")
        reverify(s)
        s.diagnostics.mkdir()
        created = True
        supervisor.save_new(s.diagnostics / "LAUNCH.json", {"argv": argv,
            "limits": s.allowance.limits, "profile_sha256": args.profile_sha256,
            "config_sha256": args.config_sha256, "original_start": START_WALL,
            "deadline": s.allowance.deadline,
            "cpu_scope": "LIMITS_CPU_SECONDS_IS_WORKER_JOB_ONLY",
            "wrapper_cooperative_cpu_limit_seconds": s.allowance.local_cpu_limit})
        supervisor.child_environment = environment
        try:
            entered = True
            supervision = supervisor.supervise(argv, s.diagnostics, s.diagnostics / "child",
                s.allowance.limits, Job, started=START_WALL)
        finally:
            supervisor.child_environment = original_environment
        supervisor.save_new(s.diagnostics / "SUPERVISION.json", supervision)
        report["child_supervision_status"] = supervision.get("status")
        report["child_exit_code"] = supervision.get("child_exit_code")
        need(s.R.operational_result(supervision), "WORKER_NOT_CLEANLY_COMPLETE")
        raw = s.R.read(s.output / "RESULT.json", 16*MIB, s.allowance.check)
        child = s.R.strict(raw, reports=True)
        need(type(child) is dict and child.get("schema") == "DMKN_INERT_HOST_WORKER_V1" and
             child.get("ok") is True and child.get("operation") == args.operation and
             child.get("mathematical_acceptance") is False and
             child.get("mathematical_owner_opened") is False and
             child.get("supervised_completion") is False and
             child.get("host_root") == str(s.host_root) and
             child.get("profile_sha256") == args.profile_sha256 and
             child.get("config_sha256") == args.config_sha256, "WORKER_REPORT_BINDING")
        result = child.get("result")
        need(type(result) is dict and result.get("mathematical_acceptance") is False and
             result.get("cleanup_errors") == [] and result.get("host_lock_closure") == "CLOSED" and
             result.get("index_closure") == "CLOSED" and result.get("custody_closure") == "CLOSED",
             "HOST_RESULT_CLOSURE")
        reverify(s)
        report.update(ok=True, status="INERT_HOST_OPERATION_COMPLETE", result=result,
            profile_sha256=args.profile_sha256, config_sha256=args.config_sha256,
            worker_report_sha256=s.R.digest(raw), closure=CLOSURE,
            supervisor_scope="ONE_WORKER_WHOLE_JOB;TRUSTED_WRAPPER_CPU_SEPARATE",
            cpu_scope="LIMITS_CPU_SECONDS_IS_WORKER_JOB_ONLY;NO_AGGREGATE_HARD_CPU_CAP",
            wrapper_cooperative_cpu_limit_seconds=s.allowance.local_cpu_limit,
            limit_precision="PRIVATE_COMMIT_PROCESS_AND_LIFETIME_JOB_LIMITS;WALL_TOTAL_CPU_LOGS_SAMPLED")
    except BaseException as error:
        report.update(ok=False, status="OPERATION_OUTCOME_UNKNOWN" if entered else "NO_WORKER_LAUNCHED",
            error_type=type(error).__name__, error=str(error)[:2000],
            retention="PRESERVED_NOT_ROLLED_BACK;DO_NOT_DELETE_LOCKS_OR_RETRY_AUTOMATICALLY")
    report["wrapper_cpu_seconds"] = time.process_time() - START_CPU
    report["wall_seconds"] = time.monotonic() - START_WALL
    if created:
        try:
            supervisor.save_new(s.diagnostics / "RUN.json", report)
        except BaseException as error:
            report.update(ok=False, status="REPORT_WRITE_FAILED_OPERATION_OUTCOME_UNKNOWN",
                          report_error=type(error).__name__ + ": " + str(error)[:1000])
    print(encode(report).decode("ascii"), flush=True)
    return 0 if report["ok"] else 1


def arguments():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("operation", choices=("init", "append", "prepare", "serve"))
    for name in ("profile-sha256", "python-runtime", "host-root", "config", "config-sha256",
                 "output", "diagnostics"):
        parser.add_argument("--" + name, required=True)
    for name in CEILINGS:
        parser.add_argument("--" + name.replace("_", "-"), required=True, type=int)
    parser.add_argument("--host-sha256", help="Required for append/serve; incremental pin binds policy, not content.")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--deadline", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--original-start", type=float, help=argparse.SUPPRESS)
    flags = [value for value in sys.argv[1:] if value.startswith("--")]
    need(len(flags) == len(set(flags)) and all("=" not in value for value in flags), "EXACT_UNIQUE_OPTIONS")
    return parser.parse_args()


if __name__ == "__main__":
    selected = arguments()
    raise SystemExit(worker(selected) if selected.worker else parent(selected))

"""One bounded ordinary CLI operation, not a shell or a mathematical checker.

Run this approved package entry with its selected Python -I -S -B. The small
supervisor reads only local selection/code, never remote mathematical evidence.
It uses the shipped Windows Job supervision, without retry or grant renewal.
OS, Python, approved code and immutable cooperative owner storage are premises.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

MIB = 1024**2
ENTRIES = {"owner": "owner.py", "peer": "peer.py", "query": "query.py", "host": "host.py"}
OPERATIONS = {
    "owner": {"init", "status", "contribute", "complete", "extract-std",
              "extract-project", "export-module", "intake-baseline", "produce-baseline"},
    "peer": {"find", "directory-find", "directory-serve", "preview", "inspect", "authoring-offers", "receive", "publish", "serve"},
    "query": set(),
    "host": {"prepare", "serve"},
}
STATE_OPTIONS = {"catalog", "custody"}
COMMON_OPTIONS = STATE_OPTIONS | {"store-id", "custody-limits", "output"}
OPTIONS = {
    "owner": COMMON_OPTIONS | {"catalog-limits", "parent-root", "source", "acquired-targets",
        "module-targets", "module-anchor", "output-names", "project-authoring", "authoring-frontier-root",
        "project-authoring-sha256", "candidate", "candidate-sha256", "supplement",
        "supplement-sha256", "prepared-bindings", "prepared-bindings-sha256",
        "retained-contribution", "retained-request-sha256", "retained-candidate-sha256",
        "library-modules", "project-extraction", "project-extraction-sha256",
        "context-root", "after-root", "limit", "bundle-directory", "bundle-manifest",
        "bundle-manifest-sha256", "project-production", "project-production-sha256", "spool-mib"},
    "peer": COMMON_OPTIONS | {"config", "config-sha256"},
    "query": COMMON_OPTIONS | {"bindings", "native-type", "symbol-names", "context-root"},
    "host": {"host-root", "host-sha256", "config", "config-sha256", "output"},
}
PATH_OPTIONS = STATE_OPTIONS | {"custody-limits", "output", "catalog-limits", "source",
    "acquired-targets", "module-targets", "output-names", "project-authoring", "candidate",
    "supplement", "prepared-bindings", "retained-contribution", "library-modules",
    "project-extraction", "bundle-directory", "bundle-manifest", "project-production",
    "config", "bindings", "native-type", "symbol-names", "host-root"}
DIRECTORY_OPTIONS = STATE_OPTIONS | {"output", "retained-contribution", "bundle-directory", "host-root"}
SUPERVISOR_ROLES = {"supervisor": "supervisor/commons.py", "domains": "supervisor/domains.py",
                    "job": "supervisor/run_stage.py"}
PYTHON_ROLES = {"python": "python_runtime/python.exe", "python_dll": "python_runtime/python314.dll",
                "python_stable_dll": "python_runtime/python3.dll"}
CEILINGS = {"wall_seconds": 3600, "cpu_seconds": 200000, "memory_mib": 8192,
            "active_processes": 8, "stdout_bytes": 8*MIB, "stderr_bytes": 8*MIB}


def need(condition, code):
    if not condition:
        raise ValueError(code)


def hexid(value):
    need(type(value) is str and len(value) == 64 and
         all(c in "0123456789abcdef" for c in value), "RUN_SHA256")
    return value


def ordinary(value, *, directory=False, fresh=False):
    """Local nonredirected paths; fresh leaves require an existing ordinary parent."""
    path = Path(value)
    need(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":" and
         path != Path(path.anchor) and len(path.parts) <= 128 and len(str(path)) <= 32767,
         "RUN_ABSOLUTE_NONROOT_PATH")
    need(all(part not in (".", "..") and not part.endswith((".", " ")) and
         not os.path.isreserved(part) and not any(ord(c) < 32 or c in ':*?"<>|' for c in part)
         for part in path.parts[1:]), "RUN_PATH_COMPONENT")
    for ancestor in reversed(path.parents):
        info = ancestor.lstat()
        need(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode) and
             not getattr(info, "st_file_attributes", 0) & 0x400, "RUN_PATH_ANCESTRY")
    if fresh:
        need(not path.exists() and not path.is_symlink(), "RUN_FRESH_PATH")
    else:
        info = path.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "RUN_REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "RUN_PATH_KIND")
    need(path.resolve(strict=not fresh) == path, "RUN_CANONICAL_PATH")
    return path


def overlap(left, right):
    return left.is_relative_to(right) or right.is_relative_to(left)


def separated(paths, code):
    for position, left in enumerate(paths):
        for right in paths[position+1:]:
            need(not overlap(left, right), code)


def reject_dedicated(path):
    """Exclude marked host generations from ordinary mutable paths/logs.

    This is a cooperative supported-command boundary, not a same-user sandbox.
    Inspect the marker's existence; malformed markers must also deny access.
    """
    path = Path(path)
    for parent in (path, *path.parents):
        try:
            (parent/"DMKN-DEDICATED-HOST.json").lstat()
        except FileNotFoundError:
            continue
        raise ValueError("RUN_DEDICATED_HOST_PATH")


def read(path, maximum, check):
    ordinary(path)
    check()
    size = path.stat().st_size
    need(0 < size <= maximum, "RUN_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    check()
    need(len(raw) == size and path.stat().st_size == size, "RUN_FILE_CHANGED")
    return raw


def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "RUN_JSON_DUPLICATE")
            result[key] = value
        return result
    def reject(_):
        raise ValueError("RUN_JSON_NUMBER")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=reject, parse_constant=reject)


def bound_file(path, pin, check, *, source=False):
    need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
         type(pin["bytes"]) is int and 0 < pin["bytes"] <= (2 if source else 128)*MIB,
         "RUN_FILE_PIN")
    hexid(pin["sha256"])
    ordinary(path)
    need(path.stat().st_size == pin["bytes"], "RUN_PIN_SIZE")
    digest, size, chunks = hashlib.sha256(), 0, []
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            check(); size += len(block)
            need(size <= pin["bytes"], "RUN_PIN_GREW")
            digest.update(block)
            if source:
                chunks.append(block)
    check()
    need(size == pin["bytes"] and path.stat().st_size == size and
         digest.hexdigest() == pin["sha256"], "RUN_PIN_CHANGED")
    return b"".join(chunks) if source else None


def checked_limits(args):
    limits = {key: getattr(args, key) for key in CEILINGS}
    need(all(type(value) is int and 1 <= value <= CEILINGS[key]
             for key, value in limits.items()), "RUN_EXPLICIT_FINITE_LIMITS")
    need(limits["wall_seconds"] >= 35 and limits["cpu_seconds"] >= 4,
         "RUN_CHILD_MINIMUM_ALLOWANCE")
    need(args.tool not in ("query", "host") or limits["cpu_seconds"] <= 600, "RUN_QUERY_CPU_ALLOWANCE")
    return limits


def child_arguments(tool, tokens):
    """Exact fixed CLI grammar; no abbreviations, duplicates or allocation overrides."""
    need(tool in ENTRIES and type(tokens) is list and len(tokens) <= 128 and
         all(type(token) is str and 0 < len(token) <= 32767 and "\0" not in token for token in tokens),
         "RUN_CHILD_ARGUMENTS")
    tokens = list(tokens)
    if tokens[:1] == ["--"]:
        tokens.pop(0)
    result, options = [], {}
    if tool != "query":
        need(tokens and tokens[0] in OPERATIONS[tool], "RUN_FIXED_OPERATION")
        result.append(tokens.pop(0))
    while tokens:
        flag = tokens.pop(0)
        need(flag.startswith("--") and "=" not in flag, "RUN_EXACT_OPTION")
        key = flag[2:]
        need(key not in options, "RUN_DUPLICATE_OPTION")
        if tool == "owner" and key == "approve-local-project":
            options[key] = True
            result.append(flag)
            continue
        need(key in OPTIONS[tool] and tokens and not tokens[0].startswith("--"),
             "RUN_UNAPPROVED_OPTION_OR_MISSING_VALUE")
        value = tokens.pop(0)
        if key == "authoring-frontier-root":
            hexid(value)
        options[key] = value
        result.extend((flag, value))
    return result, options


def configured_state(tool, tail, options, check):
    """Only publish/serve's pinned local config names an indirect writable index."""
    if tool != "peer" or tail[0] not in {"publish", "serve"}:
        return ()
    need("config" in options and "config-sha256" in options, "RUN_PEER_CONFIG_REQUIRED")
    raw = read(Path(options["config"]), 2*MIB, check)
    need(hashlib.sha256(raw).hexdigest() == hexid(options["config-sha256"]), "RUN_PEER_CONFIG_PIN")
    doc = strict(raw)
    need(type(doc) is dict and type(doc.get("index")) is dict, "RUN_PEER_INDEX")
    selected = doc["index"]
    need(type(selected.get("path")) is str and type(selected.get("create")) is bool,
         "RUN_PEER_INDEX_PATH")
    return (ordinary(selected["path"], directory=True, fresh=selected["create"]),)


def separate_arguments(root, python_root, lean_root, diagnostics, options, extra_state=(), *, tool=None):
    protected = [root, python_root, lean_root]
    separated(protected, "RUN_SUPPORT_OVERLAP")
    ordinary(diagnostics, directory=True, fresh=True)
    selected = {}
    for key in PATH_OPTIONS & set(options):
        path = Path(options[key])
        fresh = key in STATE_OPTIONS | {"output", "host-root"} and not path.exists()
        selected[key] = ordinary(path, directory=key in DIRECTORY_OPTIONS, fresh=fresh)
        need(not overlap(diagnostics, selected[key]), "RUN_DIAGNOSTICS_ARGUMENT_OVERLAP")
    writable = [diagnostics, *extra_state] + [selected[key] for key in STATE_OPTIONS | {"output", "host-root"} if key in selected]
    separated(writable, "RUN_WRITABLE_OVERLAP")
    for target in writable:
        need(all(not overlap(target, support) for support in protected), "RUN_WRITABLE_SUPPORT_OVERLAP")
        if tool == "host" and target == selected.get("host-root"):
            # The dedicated controller validates its exact root, marker and OS
            # lock. The exemption cannot be selected by another public entry.
            continue
        reject_dedicated(target)
    for key, source in selected.items():
        if key not in STATE_OPTIONS | {"output", "host-root"}:
            need(all(not overlap(source, target) for target in writable), "RUN_INPUT_WRITABLE_OVERLAP")
    return selected


def bind_support(root, expected_profile, python_root, check):
    """Bind only launch/bootstrap support; child verifies its full package before use."""
    ordinary(root, directory=True)
    ordinary(python_root, directory=True)
    raw = read(root/"PROFILE.json", 2*MIB, check)
    need(hashlib.sha256(raw).hexdigest() == hexid(expected_profile), "RUN_PROFILE_PIN")
    doc = strict(raw)
    need(type(doc) is dict and set(doc) == {"schema", "installation_manifest_sha256",
         "helper_paths", "author_worker", "files"} and doc["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1",
         "RUN_PROFILE_FIELDS")
    files = doc["files"]
    need(type(files) is dict and 1 <= len(files) <= 512, "RUN_PROFILE_FILES")
    for name in ("run.py", "owner.py", "peer.py", "query.py", "profile.py", "host.py", "custodian.py"):
        need(name in files, "RUN_REQUIRED_ENTRY")
        bound_file(root/name, files[name], check, source=True)
    installed = ordinary(root/"installation", directory=True)
    manifest_raw = read(installed/"INSTALLATION.json", 2*MIB, check)
    manifest_sha = hexid(doc["installation_manifest_sha256"])
    need(hashlib.sha256(manifest_raw).hexdigest() == manifest_sha, "RUN_INSTALLATION_PIN")
    manifest = strict(manifest_raw)
    need(type(manifest) is dict and manifest.get("schema") == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1"
         and type(manifest.get("roles")) is dict and type(manifest.get("files")) is dict
         and 1 <= len(manifest["files"]) <= 512, "RUN_INSTALLATION_FIELDS")
    support = {}
    for role, logical in {**SUPERVISOR_ROLES, **PYTHON_ROLES}.items():
        need(manifest["roles"].get(role) == logical and logical in manifest["files"],
             "RUN_REQUIRED_ROLE:"+role)
        path = python_root/logical.split("/", 1)[1] if role in PYTHON_ROLES else installed/logical
        support[role] = (path, bound_file(path, manifest["files"][logical], check,
                                        source=role in SUPERVISOR_ROLES))
    need(ordinary(Path(sys.executable)) == python_root/"python.exe", "RUN_RUNNING_PYTHON")
    return {"profile_sha256": expected_profile, "installation_manifest_sha256": manifest_sha,
            "support": support}


def load_source(name, path, raw):
    need(name not in sys.modules, "RUN_PRELOADED_MODULE:"+name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    return module


def load_supervision(bound):
    support = bound["support"]
    supervisor = load_source("_dmkn_operation_supervisor", *support["supervisor"])
    load_source("domains", *support["domains"])
    job = load_source("_dmkn_operation_job", *support["job"])
    return supervisor, job.Job


def operational_result(report):
    clean = (report.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED" and
             report.get("child_exit_code") == 0 and report.get("direct_child_reaped") is True and
             report.get("job_closed") is True and report.get("cleanup_errors") == [] and
             type(report.get("final_job")) is dict and
             report["final_job"].get("active_processes") == 0 and
             report["final_job"].get("terminated_processes") == 0)
    return {"ok": clean, "status": "CLI_EXITED_ZERO" if clean else "OPERATION_INTERRUPTED_OR_UNSUCCESSFUL",
            "mathematical_disposition": "NOT_INTERPRETED",
            "state_disposition": "PRESERVED_NOT_ROLLED_BACK;INSPECT_CHILD_REPORT_AND_OWNER_RECOVERY"}


def run(args):
    supervisor, diagnostics, created, entered = None, None, False, False
    result = {"schema": "DMKN_ORDINARY_BOUNDED_OPERATION_V1", "ok": False,
              "status": "NO_CHILD_LAUNCHED", "mathematical_disposition": "NOT_INTERPRETED",
              "authority": "LOCAL_OPERATION_REPORT_NOT_MATHEMATICAL_ACCEPTANCE"}
    try:
        need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
             sys.dont_write_bytecode and not sys.flags.optimize, "RUN_PYTHON_PROFILE")
        limits = checked_limits(args)
        def check():
            need(time.monotonic()-START_WALL < limits["wall_seconds"] and
                 time.process_time()-START_CPU < min(60, limits["cpu_seconds"]), "RUN_BOOTSTRAP_ALLOWANCE")
        check()
        root = ordinary(Path(__file__).absolute().parent, directory=True)
        python_root = ordinary(args.python_runtime, directory=True)
        lean_root = ordinary(args.lean_runtime, directory=True)
        diagnostics = Path(args.diagnostics)
        tail, options = child_arguments(args.tool, args.child_args)
        bound = bind_support(root, args.profile_sha256, python_root, check)
        extra_state = configured_state(args.tool, tail, options, check)
        separate_arguments(root, python_root, lean_root, diagnostics, options, extra_state, tool=args.tool)
        supervisor, job_class = load_supervision(bound)
        need(supervisor.limits_checked(limits) == limits, "RUN_SUPERVISOR_LIMITS")
        # The preserved supervisor's historical receiver layout is not this
        # package layout. Retain its sanitization and change only PATH here.
        original_environment = supervisor.child_environment
        def environment(cwd):
            value = original_environment(cwd)
            value["PATH"] = os.pathsep.join(map(str, (python_root, python_root/"DLLs", lean_root/"bin")))
            return value
        argv = [str(python_root/"python.exe"), "-I", "-S", "-B", str(root/ENTRIES[args.tool]),
                *tail, "--profile-sha256", args.profile_sha256,
                "--python-runtime", str(python_root), "--lean-runtime", str(lean_root),
                "--wall-seconds", str(limits["wall_seconds"]), "--cpu-seconds", str(limits["cpu_seconds"]),
                "--memory-mib", str(limits["memory_mib"])]
        need(len(subprocess.list2cmdline(argv).encode("utf-16-le"))//2 < 32760, "RUN_COMMAND_LINE_BOUND")
        check()
        diagnostics.mkdir()
        created = True
        result.update({"tool": args.tool, "profile_sha256": args.profile_sha256,
            "installation_manifest_sha256": bound["installation_manifest_sha256"],
            "limits": limits, "diagnostics": str(diagnostics),
            "supervisor_scope": "CHILD_WHOLE_TREE_JOB;TRUSTED_WRAPPER_CPU_SEPARATE",
            "limit_precision": "PRIVATE_COMMIT_PROCESS_AND_LIFETIME_JOB_LIMITS;WALL_TOTAL_CPU_LOGS_SAMPLED",
            "child_environment": "SANITIZED_WITH_EXPLICIT_SELECTED_PYTHON_AND_LEAN_PATH"})
        supervisor.save_new(diagnostics/"LAUNCH.json", {**result, "argv": argv})
        supervisor.child_environment = environment
        try:
            entered = True
            report = supervisor.supervise(argv, diagnostics, diagnostics/"child", limits,
                                          job_class, started=START_WALL)
        finally:
            supervisor.child_environment = original_environment
        # Retain the unchanged detailed report; do not parse child evidence or
        # interpret exit status as acceptance, rejection, or atomic rollback.
        supervisor.save_new(diagnostics/"SUPERVISION.json", report)
        result.update(operational_result(report))
        result["child_supervision_status"] = report.get("status")
        result["child_exit_code"] = report.get("child_exit_code")
    except BaseException as error:
        result.update({"ok": False, "status": "OPERATION_OUTCOME_UNKNOWN" if entered else "NO_CHILD_LAUNCHED",
            "error_type": type(error).__name__, "error": str(error)[:2000],
            "state_disposition": "PRESERVED_NOT_ROLLED_BACK;DO_NOT_DELETE_LOCKS_OR_RETRY_AUTOMATICALLY"})
    result["wrapper_cpu_seconds_total"] = time.process_time()-START_CPU
    result["wall_seconds_through_report"] = time.monotonic()-START_WALL
    if created:
        try:
            supervisor.save_new(diagnostics/"RUN.json", result)
        except BaseException as error:
            result.update({"ok": False, "status": "REPORT_WRITE_FAILED_OPERATION_OUTCOME_UNKNOWN",
                           "report_error": type(error).__name__+": "+str(error)[:1000]})
    return result


def arguments():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("profile-sha256", "python-runtime", "lean-runtime", "diagnostics"):
        parser.add_argument("--"+name, required=True)
    for name in CEILINGS:
        parser.add_argument("--"+name.replace("_", "-"), required=True, type=int)
    parser.add_argument("tool", choices=tuple(ENTRIES))
    parser.add_argument("child_args", nargs=argparse.REMAINDER)
    return parser.parse_args()


def main():
    result = run(arguments())
    print(json.dumps(result, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

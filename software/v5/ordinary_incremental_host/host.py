"""Initialize, append to, prepare or serve dedicated inert mathematical custody.

This entry never opens a mathematical owner or invokes native checking. Hosted
bytes and search records remain candidates for each recipient's own acceptance.
Use the package launcher for hard whole-process containment.
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
import sys

MIB = 1024**2


def need(value, code):
    if not value:
        raise ValueError(code)


def bootstrap(root, expected, check):
    """Capture selected entry/owner bytes before executing the owner bootstrap."""
    need(type(expected) is str and len(expected) == 64 and
         all(c in "0123456789abcdef" for c in expected), "HOST_PROFILE_HASH")

    def read(path):
        need(path.is_absolute() and ".." not in path.parts, "HOST_BOOTSTRAP_PATH")
        for part in (*reversed(path.parents), path):
            info = part.lstat()
            need(not stat.S_ISLNK(info.st_mode) and not
                 getattr(info, "st_file_attributes", 0) & 0x400, "HOST_BOOTSTRAP_REDIRECT")
            need(stat.S_ISDIR(info.st_mode) if part != path else
                 stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "HOST_BOOTSTRAP_KIND")
        size = path.stat().st_size
        need(0 < size <= 2*MIB, "HOST_BOOTSTRAP_BOUND")
        check()
        with path.open("rb") as stream:
            raw = stream.read(2*MIB+1)
        need(len(raw) == size, "HOST_BOOTSTRAP_CHANGED")
        check()
        return raw

    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "HOST_BOOTSTRAP_DUPLICATE")
            result[key] = value
        return result

    raw = read(root/"PROFILE.json")
    need(hashlib.sha256(raw).hexdigest() == expected, "HOST_PROFILE_PIN")
    descriptor = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    need(type(descriptor) is dict and type(descriptor.get("files")) is dict,
         "HOST_BOOTSTRAP_DESCRIPTOR")
    selected = {}
    for filename in ("host.py", "owner.py"):
        pin = descriptor["files"].get(filename)
        need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
             type(pin["bytes"]) is int and 0 < pin["bytes"] <= 2*MIB, "HOST_BOOTSTRAP_PIN")
        selected[filename] = read(root/filename)
        need(len(selected[filename]) == pin["bytes"] and
             hashlib.sha256(selected[filename]).hexdigest() == pin["sha256"], "HOST_SOURCE_PIN")
    name, path = "_dmkn_host_owner_entry", root/"owner.py"
    need(name not in sys.modules, "HOST_BOOTSTRAP_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(selected["owner.py"], str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    module.START_WALL, module.START_CPU = START_WALL, START_CPU
    return module


def helper(loaded, root, check):
    name, filename = "_dmkn_dedicated_custodian", "custodian.py"
    need(name not in sys.modules, "HOST_HELPER_PRELOADED")
    pin = loaded.descriptor["files"][filename]
    path = loaded.A.C.ordinary(root/filename)
    check()
    raw = loaded.A.C.read_bounded(path, 2*MIB)
    need(len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"],
         "HOST_HELPER_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    check()
    return module


def disjoint(paths):
    for i, left in enumerate(paths):
        for right in paths[i+1:]:
            need(not left.is_relative_to(right) and not right.is_relative_to(left),
                 "HOST_OUTPUT_STATE_SUPPORT_OVERLAP")


def encode(value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":")).encode("ascii")
    need(len(raw) <= 16*MIB, "HOST_REPORT_BOUND")
    return raw


def run(args):
    loaded = allocation = output = result = None
    created, phase = False, "ARGUMENTS"
    try:
        need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
             sys.dont_write_bytecode and not sys.flags.optimize, "HOST_PYTHON_PROFILE")
        need(args.operation in ("init", "append", "prepare", "serve"), "HOST_OPERATION")
        need((args.operation in ("append", "serve")) == (args.host_sha256 is not None),
             "HOST_SEAL_PIN_MODE")
        need(type(args.wall_seconds) is int and 35 <= args.wall_seconds <= 3600 and
             type(args.cpu_seconds) is int and 4 <= args.cpu_seconds <= 600 and
             type(args.memory_mib) is int and 1 <= args.memory_mib <= 8192,
             "HOST_ORIGINAL_ALLOCATION")
        deadline = START_WALL+args.wall_seconds

        def boot_check():
            need(time.monotonic() < deadline and time.process_time()-START_CPU < args.cpu_seconds,
                 "HOST_ORIGINAL_ALLOCATION_EXHAUSTED")

        root = Path(__file__).absolute().parent
        base = bootstrap(root, args.profile_sha256, boot_check)
        allocation = base.Allowance(args)
        phase = "SUPPORT"
        loader = base.bootstrap(root, args.profile_sha256, allocation.check)
        loaded = loader.load(root, args.profile_sha256,
            {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
            allocation.deadline, check_parent=allocation.check)
        A = loaded.A
        phase = "CONFIGURATION"
        if args.host_sha256 is not None:
            A.C.hexid(args.host_sha256)
        config_path = A.C.ordinary(Path(args.config))
        A.C.hexid(args.config_sha256)
        config_raw = A.C.read_bounded(config_path, 2*MIB)
        need(hashlib.sha256(config_raw).hexdigest() == args.config_sha256, "HOST_CONFIG_PIN")
        config = loader.owner_json(config_raw, 2*MIB)
        need(type(config) is dict, "HOST_CONFIG_OBJECT")
        host_root = A.C.ordinary(Path(args.host_root), directory=True,
                                 fresh=args.operation in ("init", "prepare"))
        output = A.C.ordinary(Path(args.output), directory=True, fresh=True)
        # Host state is intentionally allowed only through this entry's explicit
        # argument. Logs/output/package/runtime must remain outside that state.
        disjoint([output, host_root, root, *loaded.installation.runtime_roots.values()])
        base.separated([output, root, *loaded.installation.runtime_roots.values()],
                       "HOST_LOG_SUPPORT_OVERLAP")
        need(not config_path.is_relative_to(output) and not config_path.is_relative_to(host_root),
             "HOST_CONFIG_STATE_OVERLAP")
        # Check input/output overlap before creating even the report directory.
        # The helper independently validates full schemas, budgets and state
        # separation before preparing a generation or opening it for service.
        inputs = []
        if args.operation in ("prepare", "append"):
            need(type(config.get("bundle_directory")) is str and
                 type(config.get("manifest")) is dict and
                 type(config["manifest"].get("path")) is str, "HOST_BUNDLE_INPUT_PATHS")
            inputs = [A.C.ordinary(Path(config["bundle_directory"]), directory=True),
                      A.C.ordinary(Path(config["manifest"]["path"]))]
        elif args.operation == "serve" and config.get("tls") is not None:
            tls = config["tls"]
            need(type(tls) is dict and all(type(tls.get(k)) is str for k in ("cert_file", "key_file")),
                 "HOST_TLS_INPUT_PATHS")
            inputs = [A.C.ordinary(Path(tls[k])) for k in ("cert_file", "key_file")]
        for path in inputs:
            need(not path.is_relative_to(output) and not output.is_relative_to(path),
                 "HOST_INPUT_OUTPUT_OVERLAP")
        api = helper(loaded, root, allocation.check)

        def finalize():
            need(A.C.read_bounded(config_path, 2*MIB) == config_raw, "HOST_CONFIG_CHANGED")
            loaded.profile.verify(allocation.check)
            allocation.check()

        allocation.check()
        output.mkdir(); created = True
        phase = args.operation.upper()
        if args.operation == "init":
            result = api.initialize(loaded, host_root, config, allocation,
                                    profile_sha256=args.profile_sha256, finalize=finalize)
        elif args.operation == "append":
            result = api.append(loaded, host_root, config, allocation,
                profile_sha256=args.profile_sha256, expected_host_sha256=args.host_sha256,
                finalize=finalize)
        elif args.operation == "prepare":
            result = api.prepare(loaded, host_root, config, allocation,
                                 profile_sha256=args.profile_sha256, finalize=finalize)
        else:
            def ready(value):
                allocation.check()
                A.P.PortableCatalog._write_fresh(output/"READY.json", encode(value))
            result = api.serve(loaded, host_root, config, allocation,
                profile_sha256=args.profile_sha256, expected_host_sha256=args.host_sha256,
                finalize=finalize, ready=ready)
        finalize()
        report = {"ok": True, "operation": "host-"+args.operation, "result": result,
            "profile_sha256": args.profile_sha256, "config_sha256": args.config_sha256,
            "host_root": str(host_root), "semantic_id": loaded.installation.semantic_id,
            "mathematical_acceptance": False, "mathematical_owner_opened": False}
    except BaseException as error:
        report = {"ok": False, "operation": "host-"+args.operation, "phase": phase,
            "error_type": type(error).__name__, "error": str(error)[:2000], "result": result,
            "mathematical_acceptance": False,
            "retention": "PRESERVE_PARTIAL_HOST_AND_OUTPUT_NO_AUTOMATIC_RETRY"}
        if hasattr(error, "report"):
            report["detail"] = error.report
    report["cost"] = allocation.report() if allocation is not None else {
        "wall_seconds": time.monotonic()-START_WALL,
        "controller_cpu_seconds": time.process_time()-START_CPU, "worker_cpu_seconds": 0}
    try:
        if allocation is not None:
            allocation.check()
        raw = encode(report)
        if created:
            loaded.A.P.PortableCatalog._write_fresh(output/"RESULT.json", raw)
    except BaseException as error:
        report.update(ok=False, final_report_error=type(error).__name__+": "+str(error)[:1000],
            retention="HOST_EFFECTS_PRESERVED_REPORT_NOT_CONFIRMED_NO_AUTOMATIC_RETRY")
        raw = encode(report)
    return report, raw


def arguments():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("operation", choices=("init", "append", "prepare", "serve"))
    for name in ("profile-sha256", "python-runtime", "lean-runtime", "host-root",
                 "config", "config-sha256", "output"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+name, required=True, type=int)
    parser.add_argument("--host-sha256", help="Exact HOST.json pin; required for append/serve. "
                        "An incremental descriptor pin identifies policy, not current content.")
    return parser.parse_args()


if __name__ == "__main__":
    report, raw = run(arguments())
    sys.stdout.buffer.write(raw+b"\n"); sys.stdout.buffer.flush()
    raise SystemExit(0 if report["ok"] else 1)

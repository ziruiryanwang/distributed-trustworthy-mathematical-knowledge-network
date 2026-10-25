"""Finite direct-contact peer commands over one selected ordinary package.

Peer replies remain inert. Only receive's actual ordinary native admission can
accept mathematics. Publish changes a local index; serve exposes all addressable
objects in the explicitly selected custody. No remote writes, daemon renewal,
automatic retry, source execution, initialization or library copying occurs.
Preview exposes an inert candidate type; inspect exposes one exact inert unit.
Like find both open no local owner/catalog/custody and reject all state arguments.
Their results are not mathematical acceptance, complete discovery, native imports
or verified applicability. Inspect does not follow the unit's dependencies.
Authoring-offers returns only advisory project locations; it never follows them,
approves execution or checks correspondence between project and mathematics.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
import asyncio
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import stat
import sys

MIB = 1024**2
MAX_REPORT_BYTES = 16*MIB


def need(condition, code):
    if not condition:
        raise ValueError(code)


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("find", "preview", "inspect", "authoring-offers", "receive", "publish", "serve"))
    for name in ("profile-sha256", "python-runtime", "lean-runtime", "config",
                 "config-sha256", "output"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+name, required=True, type=int)
    for name in ("catalog", "custody", "store-id", "custody-limits"):
        parser.add_argument("--"+name)
    return parser.parse_args()


def bootstrap_owner(root, expected, check):
    """Check this entry and old owner bytes before importing reusable helpers.

    Entrypoint/Python/OS integrity and immutable local owner storage remain
    premises. The externally selected hash is byte selection, not authentication.
    The unchanged owner bootstrap next checks the new exact profile loader.
    """
    need(type(expected) is str and len(expected) == 64 and
         all(c in "0123456789abcdef" for c in expected), "PEER_PROFILE_HASH")
    def read(path, maximum):
        need(path.is_absolute() and ".." not in path.parts, "PEER_BOOTSTRAP_PATH")
        for part in (*reversed(path.parents), path):
            info = part.lstat()
            need(not stat.S_ISLNK(info.st_mode) and not
                 (getattr(info, "st_file_attributes", 0) & 0x400), "PEER_BOOTSTRAP_REDIRECT")
            need(stat.S_ISDIR(info.st_mode) if part != path else
                 stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PEER_BOOTSTRAP_FILE")
        size = path.stat().st_size
        need(0 < size <= maximum, "PEER_BOOTSTRAP_BOUND")
        check()
        with path.open("rb") as stream:
            raw = stream.read(maximum+1)
        need(len(raw) == size, "PEER_BOOTSTRAP_CHANGED")
        return raw
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "PEER_BOOTSTRAP_DUPLICATE")
            result[key] = value
        return result
    raw = read(root/"PROFILE.json", 2*MIB)
    need(hashlib.sha256(raw).hexdigest() == expected, "PEER_PROFILE_PIN")
    doc = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    need(type(doc) is dict and type(doc.get("files")) is dict, "PEER_BOOTSTRAP_DESCRIPTOR")
    selected = {}
    for filename in ("peer.py", "owner.py"):
        pin = doc["files"].get(filename)
        need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
             type(pin["bytes"]) is int and 0 < pin["bytes"] <= 2*MIB, "PEER_BOOTSTRAP_PIN")
        selected[filename] = read(root/filename, 2*MIB)
        need(len(selected[filename]) == pin["bytes"] and
             hashlib.sha256(selected[filename]).hexdigest() == pin["sha256"],
             "PEER_BOOTSTRAP_SOURCE_CHANGED")
    name, path = "_dmkn_ordinary_owner_entry", root/"owner.py"
    need(name not in sys.modules, "PEER_BOOTSTRAP_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(selected["owner.py"], str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    # Reuse the exact owner Allowance implementation, including all subsequent
    # worker CPU charges, while accounting from THIS entry's original start.
    module.START_WALL, module.START_CPU = START_WALL, START_CPU
    return module


def encode_report(value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":")).encode("ascii")
    need(len(raw) <= MAX_REPORT_BYTES, "PEER_REPORT_BYTE_BOUND")
    return raw


def terminal_report(report, result, operation, check=None):
    """Bound terminal reporting without discarding already committed effects."""
    try:
        raw = encode_report(report)
        if check is not None:
            check()
    except BaseException as error:
        detail = report.get("detail")
        effects = detail if type(detail) is dict else result if type(result) is dict else {}
        accepted = effects.get("accepted")
        if accepted is None:
            accepted = effects.get("admission")
        if accepted is None and type(result) is dict:
            accepted = result.get("accepted")
            if accepted is None:
                accepted = result.get("admission")
        publications = effects.get("publications", [])
        # Publish has at most 64 targets. Preserve committed identities, not the
        # potentially large discovery records that caused report-size failure.
        compact_publications = [{key: item[key] for key in
            ("new", "record_id", "snapshot_id", "mathematical_acceptance") if key in item}
            for item in publications[:64] if type(item) is dict] if type(publications) is list else []
        report = {"ok": False, "operation": operation, "phase": "REPORT",
                  "error_type": type(error).__name__, "error": str(error)[:500],
                  "accepted": accepted, "publications": compact_publications,
                  "local_context": effects.get("local_context"), "cost": report["cost"],
                  "retention": "ACCEPTED_STATE_PRESERVED_REPORT_NOT_FULLY_SERIALIZED"}
        raw = encode_report(report)
    return report, raw


def run(args):
    owner = custody = allocation = loaded = output = None
    report, result, phase, config_raw = None, None, "BOOTSTRAP", None
    try:
        need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
             sys.dont_write_bytecode and not sys.flags.optimize, "PEER_PYTHON_PROFILE")
        need(type(args.wall_seconds) is int and 35 <= args.wall_seconds <= 3600 and
             type(args.cpu_seconds) is int and 4 <= args.cpu_seconds <= 200000 and
             type(args.memory_mib) is int and 1 <= args.memory_mib <= 8192,
             "PEER_ORIGINAL_ALLOCATION")
        deadline = START_WALL+args.wall_seconds
        def boot_check():
            need(time.monotonic() < deadline and time.process_time()-START_CPU < args.cpu_seconds,
                 "PEER_ORIGINAL_ALLOCATION_EXHAUSTED")
        root = Path(__file__).absolute().parent
        base = bootstrap_owner(root, args.profile_sha256, boot_check)
        allocation = base.Allowance(args)
        loader = base.bootstrap(root, args.profile_sha256, allocation.check)
        loaded = loader.load(root, args.profile_sha256,
            {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
            allocation.deadline, check_parent=allocation.check)
        A, O, api, installation = loaded.A, loaded.O, loaded.peer_api, loaded.installation
        need(api.A is A, "PEER_API_SHARED_CORE")
        phase = "CONFIGURATION"
        need(args.operation in ("find", "preview", "inspect", "authoring-offers", "receive", "publish", "serve"), "PEER_OPERATION")
        state_free = args.operation in ("find", "preview", "inspect", "authoring-offers")
        loader.hexid(args.config_sha256)
        config_path = A.C.ordinary(Path(args.config))
        config_raw = A.C.read_bounded(config_path, 2*MIB)
        need(hashlib.sha256(config_raw).hexdigest() == args.config_sha256, "PEER_CONFIG_PIN")
        config = loader.owner_json(config_raw, 2*MIB)
        need(type(config) is dict, "PEER_CONFIG_OBJECT")
        state_args = (args.catalog, args.custody, args.store_id, args.custody_limits)
        need(all(value is None for value in state_args) if state_free else
             all(value is not None for value in state_args), "PEER_OPERATION_STATE_ARGUMENTS")
        protected = [root, *installation.runtime_roots.values()]
        output = A.C.ordinary(Path(args.output), directory=True, fresh=True)
        state_paths, catalog_path, custody_path = [], None, None
        if not state_free:
            A.C.hexid(args.store_id)
            catalog_path = A.C.ordinary(Path(args.catalog), directory=True)
            custody_path = A.C.ordinary(Path(args.custody), directory=True)
            state_paths = [catalog_path, custody_path]
        if args.operation in ("publish", "serve"):
            selected = config.get("index")
            A.P.fields(selected, ("path", "limits", "create"), "PEER_INDEX_FIELDS")
            need(type(selected["path"]) is str and type(selected["create"]) is bool,
                 "PEER_INDEX_SELECTION")
            need(args.operation == "publish" or selected["create"] is False, "PEER_SERVE_EXISTING_INDEX")
            index_path = A.C.ordinary(Path(selected["path"]), directory=True, fresh=selected["create"])
            state_paths.append(index_path)
        if args.operation == "serve":
            need(config.get("share_all_custody") is True and config.get("exclusive") is True,
                 "PEER_EXPLICIT_SERVICE_SCOPE")
        base.separated([output, *state_paths, *protected], "PEER_OUTPUT_STATE_SUPPORT_OVERLAP")
        if not state_free:
            custody_limits = A._writer_json(A.C.read_bounded(Path(args.custody_limits), 65536), 65536)
            A.P.fields(custody_limits, O.STORE_LIMITS, "PEER_CUSTODY_LIMITS")
            for key, bounds in O.STORE_LIMITS.items():
                A.P.uint(custody_limits[key], *bounds, "PEER_CUSTODY_LIMIT:"+key)
            marker = A.E.strict_json(A.C.read_bounded(catalog_path/"ADOPTION.json", 65536),
                                    A.E.Limits(max_bytes=65536))
            A.P.fields(marker, ("schema", "store_id", "implementation", "limits"), "PEER_ADOPTION_FIELDS")
            need(marker["schema"] == A.P.SCHEMA and marker["store_id"] == args.store_id and
                 marker["implementation"] == installation.doc["implementation"], "PEER_ADOPTION_BINDING")
            catalog_limits = A.P.Limits(**marker["limits"])
        allocation.check()
        output.mkdir()
        if not state_free:
            phase = "OPEN_OWNER"
            custody = O.OrdinaryStore(custody_path, installation.semantic_id, custody_limits)
            # Serve holds the SAME ordinary catalog lock as old owner.py. This
            # serializes this owner's supported mutation/serving commands; it
            # does not lock unrelated catalogs or arbitrary lower-level callers.
            owner = A.OrdinaryAdmission.open(installation, catalog_path, args.store_id,
                                            custody, limits=catalog_limits)
        allocation.check()
        phase = args.operation.upper()
        if args.operation == "find":
            result = asyncio.run(api.find(loaded, config, allocation))
        elif args.operation == "preview":
            result = asyncio.run(api.preview(loaded, config, allocation))
        elif args.operation == "inspect":
            result = asyncio.run(api.inspect(loaded, config, allocation))
        elif args.operation == "authoring-offers":
            result = asyncio.run(api.authoring_offers(loaded, config, allocation))
        elif args.operation == "receive":
            result = asyncio.run(api.receive(loaded, owner, custody, config, allocation))
        elif args.operation == "publish":
            result = api.publish(loaded, owner, custody, config, allocation)
        elif args.operation == "serve":
            def ready(value):
                allocation.check()
                A.P.PortableCatalog._write_fresh(output/"READY.json", encode_report(value))
            result = asyncio.run(api.serve(loaded, custody, config, allocation, ready=ready))
        else:
            # Never route a new or malformed operation into service startup.
            raise ValueError("PEER_OPERATION")
        allocation.check()
        need(A.C.read_bounded(config_path, 2*MIB) == config_raw, "PEER_CONFIG_CHANGED")
        report = {"ok": True, "operation": args.operation, "result": result,
                  "profile_sha256": args.profile_sha256, "config_sha256": args.config_sha256,
                  "implementation_id": installation.implementation_id,
                  "semantic_id": installation.semantic_id,
                  "store_id": args.store_id, "catalog": args.catalog, "custody": args.custody,
                  "claim": "DIRECT_CONTACT_LOCAL_OPERABILITY_NOT_GLOBAL_COMPLETENESS_OR_FINAL_V5"}
    except BaseException as error:
        report = {"ok": False, "operation": args.operation, "phase": phase,
                  "error_type": type(error).__name__, "error": str(error)[:2000],
                  "result": result,
                  "retention": "ACCEPTED_STATE_AND_PARTIAL_OUTPUTS_PRESERVED_NO_RETRY"}
        if hasattr(error, "report"):
            report["detail"] = error.report
    finally:
        close_errors = []
        # Provider/index cleanup occurs inside API. The owner lock remains held
        # until that call returns or fails, including its cleanup path.
        for name, value in (("owner", owner), ("custody", custody)):
            if value is not None:
                try:
                    value.close()
                except BaseException as error:
                    close_errors.append({"component": name, "error_type": type(error).__name__,
                                         "error": str(error)[:500]})
        if close_errors:
            report["ok"] = False
            report["close_errors"] = close_errors
        if allocation is not None:
            try:
                allocation.check()
            except BaseException as error:
                report["ok"] = False
                report["final_budget_error"] = {"error_type": type(error).__name__, "error": str(error)[:500]}
        report["cost"] = allocation.report() if allocation is not None else {
            "wall_seconds": time.monotonic()-START_WALL,
            "controller_cpu_seconds": time.process_time()-START_CPU,
            "worker_cpu_seconds": 0,
            "controller_limits": "COOPERATIVE_REQUIRES_EXTERNAL_JOB"}
    report, raw = terminal_report(report, result, args.operation,
                                  allocation.check if allocation is not None else None)
    if output is not None and output.is_dir() and loaded is not None:
        try:
            loaded.A.P.PortableCatalog._write_fresh(output/"RESULT.json", raw)
        except BaseException as error:
            report["ok"] = False
            report["report_write_error"] = {"error_type": type(error).__name__, "error": str(error)[:500]}
            raw = encode_report(report)
    return report, raw


if __name__ == "__main__":
    result, raw_result = run(arguments())
    sys.stdout.buffer.write(raw_result+b"\n")
    sys.stdout.buffer.flush()
    raise SystemExit(0 if result["ok"] else 1)

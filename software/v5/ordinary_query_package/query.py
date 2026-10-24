"""Compile inert owner-local type metadata into the existing peer search spec.

This does not run Lean, prove a theorem, query a provider or open owner state.
Run the local Lean query command separately in an approved project. Supply only
already known portable symbol bindings; unknown bindings refuse. Package
approval, local runtime and immutable storage are the same premises as owner.py.
Process CPU/wall checks are cooperative; use an outer supervisor for hard bounds.
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


def need(condition, code):
    if not condition:
        raise ValueError(code)


def bootstrap_owner(root, expected, check):
    """Check this entry and old owner bytes before importing reusable helpers.

    Entrypoint/Python/OS integrity and immutable local owner storage remain
    premises. The externally selected hash is byte selection, not authentication.
    The unchanged owner bootstrap next checks the new exact profile loader.
    """
    need(type(expected) is str and len(expected) == 64 and
         all(c in "0123456789abcdef" for c in expected), "QUERY_PROFILE_HASH")
    def read(path, maximum):
        need(path.is_absolute() and ".." not in path.parts, "QUERY_BOOTSTRAP_PATH")
        for part in (*reversed(path.parents), path):
            info = part.lstat()
            need(not stat.S_ISLNK(info.st_mode) and not
                 (getattr(info, "st_file_attributes", 0) & 0x400), "QUERY_BOOTSTRAP_REDIRECT")
            need(stat.S_ISDIR(info.st_mode) if part != path else
                 stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "QUERY_BOOTSTRAP_FILE")
        size = path.stat().st_size
        need(0 < size <= maximum, "QUERY_BOOTSTRAP_BOUND")
        check()
        with path.open("rb") as stream:
            raw = stream.read(maximum+1)
        need(len(raw) == size, "QUERY_BOOTSTRAP_CHANGED")
        return raw
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "QUERY_BOOTSTRAP_DUPLICATE")
            result[key] = value
        return result
    raw = read(root/"PROFILE.json", 2*MIB)
    need(hashlib.sha256(raw).hexdigest() == expected, "QUERY_PROFILE_PIN")
    doc = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    need(type(doc) is dict and type(doc.get("files")) is dict, "QUERY_BOOTSTRAP_DESCRIPTOR")
    selected = {}
    for filename in ("query.py", "owner.py"):
        pin = doc["files"].get(filename)
        need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
             type(pin["bytes"]) is int and 0 < pin["bytes"] <= 2*MIB, "QUERY_BOOTSTRAP_PIN")
        selected[filename] = read(root/filename, 2*MIB)
        need(len(selected[filename]) == pin["bytes"] and
             hashlib.sha256(selected[filename]).hexdigest() == pin["sha256"],
             "QUERY_BOOTSTRAP_SOURCE_CHANGED")
    name, path = "_dmkn_ordinary_owner_entry", root/"owner.py"
    need(name not in sys.modules, "QUERY_BOOTSTRAP_PRELOADED")
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



def arguments():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("profile-sha256", "python-runtime", "lean-runtime",
                 "native-type", "bindings", "output"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+name, required=True, type=int)
    return parser.parse_args()


def run(args):
    allocation, created, output, result = None, False, None, None
    phase = "BOOTSTRAP"
    try:
        need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
             sys.dont_write_bytecode and not sys.flags.optimize, "QUERY_PYTHON_PROFILE")
        need(type(args.wall_seconds) is int and 35 <= args.wall_seconds <= 3600 and
             type(args.cpu_seconds) is int and 4 <= args.cpu_seconds <= 600,
             "QUERY_FINITE_ALLOWANCE")
        deadline = START_WALL+args.wall_seconds
        def check():
            need(time.monotonic() < deadline and
                 time.process_time()-START_CPU < args.cpu_seconds, "QUERY_ALLOWANCE")
        root = Path(__file__).absolute().parent
        base = bootstrap_owner(root, args.profile_sha256, check)
        allocation = base.Allowance(args)
        loader = base.bootstrap(root, args.profile_sha256, allocation.check)
        loaded = loader.load(root, args.profile_sha256,
            {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
            allocation.deadline, check_parent=allocation.check)
        A, Q = loaded.A, loaded.formal_query
        adapter = sys.modules["discovery.ordinary_export_adapter"]
        need(Q.E is A.E and Q.S is A.S and adapter.Q is Q, "QUERY_SHARED_HELPERS")
        phase = "INPUTS"
        native_path, bindings_path = (A.C.ordinary(Path(value))
                                     for value in (args.native_type, args.bindings))
        native_raw = A.C.read_bounded(native_path, MIB)
        bindings_raw = A.C.read_bounded(bindings_path, MIB)
        output = A.C.ordinary(Path(args.output), directory=True, fresh=True)
        base.separated([output, root, *loaded.installation.runtime_roots.values()],
                       "QUERY_OUTPUT_SUPPORT_OVERLAP")
        need(not native_path.is_relative_to(output) and not bindings_path.is_relative_to(output),
             "QUERY_INPUT_OUTPUT_OVERLAP")
        allocation.check()
        phase = "QUERY"
        query_raw = Q.bind_native_type(native_raw, bindings_raw,
                                      semantic_id=loaded.installation.semantic_id)
        spec = Q.query_spec(query_raw)
        namespace = adapter.namespace_for(loaded.installation.semantic_id)
        features = adapter.compile_query(namespace, [spec])
        # Recheck captured inputs and selected package before any output commit.
        need(A.C.read_bounded(native_path, MIB) == native_raw and
             A.C.read_bounded(bindings_path, MIB) == bindings_raw, "QUERY_INPUT_CHANGED")
        loaded.profile.verify(allocation.check)
        allocation.check()
        output.mkdir()
        created = True
        A.P.PortableCatalog._write_fresh(output/"QUERY.json", query_raw)
        A.P.PortableCatalog._write_fresh(output/"SPECS.json", A.E.canonical_json([spec]))
        result = {"ok": True, "operation": "prepare-query", "namespace": namespace,
            "specs": [spec], "features": features, "key_profile": Q.PROFILE_ID,
            "query_sha256": hashlib.sha256(query_raw).hexdigest(),
            "native_type_sha256": hashlib.sha256(native_raw).hexdigest(),
            "bindings_sha256": hashlib.sha256(bindings_raw).hexdigest(),
            "profile_sha256": args.profile_sha256, "mathematical_acceptance": False,
            "claim": "BOUNDED_EXACT_TYPE_SEARCH_INPUT_NOT_THEOREM_OR_GLOBAL_COVERAGE",
            "next": "Use specs in existing peer.py find with explicit contacts and budgets"}
        allocation.check()
    except BaseException as error:
        result = {"ok": False, "phase": phase, "error_type": type(error).__name__,
                  "error": str(error)[:2000], "mathematical_acceptance": False,
                  "retention": "PARTIAL_OUTPUT_RETAINED_NO_RETRY"}
    result["cost"] = allocation.report() if allocation is not None else {
        "wall_seconds": time.monotonic()-START_WALL,
        "controller_cpu_seconds": time.process_time()-START_CPU,
        "worker_cpu_seconds": 0, "controller_limits": "COOPERATIVE_REQUIRES_EXTERNAL_JOB"}
    raw = json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False,
                     separators=(",", ":")).encode("utf-8")
    if created:
        try:
            A.P.PortableCatalog._write_fresh(output/"RESULT.json", raw)
        except BaseException as error:
            result.update(ok=False, report_write_error=str(error)[:500])
            raw = json.dumps(result, sort_keys=True, allow_nan=False).encode("utf-8")
    return result, raw


if __name__ == "__main__":
    result, raw = run(arguments())
    sys.stdout.buffer.write(raw+b"\n")
    sys.stdout.buffer.flush()
    raise SystemExit(0 if result["ok"] else 1)

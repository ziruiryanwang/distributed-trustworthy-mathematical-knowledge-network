"""Owner-approved inert handoff from existing custody to an ordinary file bundle.

Use selected Python -I -S -B; a hard whole-operation supervisor is separate.
No native/cut catalog, Lean process, source project, network or acceptance call.
The entrypoint/runtime/OS and approved immutable support are trust premises.
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


def need(ok, code):
    if not ok:
        raise ValueError("RETURN_COMMAND_" + code)


def _read(path, maximum, check):
    need(path.is_absolute() and ".." not in path.parts and len(path.parts) <= 128 and
         len(str(path)) <= 32768, "ABSOLUTE_PATH")
    for item in (*reversed(path.parents), path):
        info = item.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             (getattr(info, "st_file_attributes", 0) & 0x400), "REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if item != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "SINGLE_FILE")
    size = path.stat().st_size
    need(0 < size <= maximum, "FILE_BOUND")
    check()
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    check()
    need(len(raw) == size, "READ_CHANGED")
    return raw


def _hex(value):
    need(type(value) is str and len(value) == 64 and
         all(char in "0123456789abcdef" for char in value), "HASH")
    return value


def _execute(name, path, raw):
    need(name not in sys.modules, "PRELOADED_MODULE")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    return module


def _owner(root, profile_hash, check):
    raw = _read(root / "PROFILE.json", 2*MIB, check)
    need(hashlib.sha256(raw).hexdigest() == _hex(profile_hash), "PROFILE_PIN")
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "DUPLICATE_PROFILE_KEY")
            result[key] = value
        return result
    doc = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    need(type(doc) is dict and type(doc.get("files")) is dict, "PROFILE_DESCRIPTOR")
    pin = doc["files"].get("owner.py")
    need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
         type(pin["bytes"]) is int and 0 < pin["bytes"] <= 2*MIB, "OWNER_PIN")
    source = _read(root / "owner.py", 2*MIB, check)
    need(len(source) == pin["bytes"] and
         hashlib.sha256(source).hexdigest() == _hex(pin["sha256"]), "OWNER_CHANGED")
    return _execute("_dmkn_custody_return_owner", root / "owner.py", source)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("package", "profile-sha256", "helper-sha256", "python-runtime", "lean-runtime",
                 "custody", "custody-limits", "custody-limits-sha256", "targets", "targets-sha256",
                 "output"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--policy", required=True, choices=("selected-units", "closed-basis"))
    parser.add_argument("--wall-seconds", required=True, type=int)
    parser.add_argument("--cpu-seconds", required=True, type=int)
    parser.add_argument("--approve-local-custody", action="store_true")
    parser.add_argument("--limits", help="Optional owner JSON with lowered baseline-bundle caps")
    parser.add_argument("--limits-sha256")
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_PYTHON")
    need(args.approve_local_custody and 1 <= args.wall_seconds <= 3600 and
         1 <= args.cpu_seconds <= 200000 and
         ((args.limits is None) == (args.limits_sha256 is None)), "ORIGINAL_ALLOCATION_OR_ARGUMENTS")
    deadline = START_WALL + args.wall_seconds
    def check():
        need(time.monotonic() < deadline and
             time.process_time() - START_CPU < args.cpu_seconds, "ORIGINAL_ALLOCATION_EXHAUSTED")
    check()
    root = Path(args.package)
    owner = _owner(root, args.profile_sha256, check)
    loader = owner.bootstrap(root, args.profile_sha256, check)
    loaded = loader.load(root, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        deadline, check_parent=check)
    A, O = loaded.A, loaded.O
    source_root = A.C.ordinary(Path(__file__).absolute().parent, directory=True)
    helper_path = source_root / "custody_return.py"
    source = _read(helper_path, 2*MIB, check)
    need(hashlib.sha256(source).hexdigest() == _hex(args.helper_sha256), "HELPER_PIN")
    helper = _execute("_dmkn_custody_return_helper", helper_path, source)

    def selected(path, expected, maximum):
        raw = _read(Path(path), maximum, check)
        need(hashlib.sha256(raw).hexdigest() == _hex(expected), "INPUT_PIN")
        return A._writer_json(raw, maximum)
    custody_limits = selected(args.custody_limits, args.custody_limits_sha256, 65536)
    A.P.fields(custody_limits, O.STORE_LIMITS, "RETURN_CUSTODY_LIMITS")
    for key, bounds in O.STORE_LIMITS.items():
        A.P.uint(custody_limits[key], *bounds, "RETURN_CUSTODY_LIMIT:" + key)
    export_ids = selected(args.targets, args.targets_sha256, MIB)
    limits = helper.Limits() if args.limits is None else helper.Limits(
        **selected(args.limits, args.limits_sha256, 65536))
    custody_root = A.C.ordinary(Path(args.custody), directory=True)
    output = A.C.ordinary(Path(args.output), directory=True, fresh=True)
    support = (loaded.root, source_root, *loaded.installation.runtime_roots.values())
    for protected in support:
        helper._separate(custody_root, protected)
        helper._separate(output, protected)
    helper._separate(output, custody_root)
    # Never implicitly recover a selected store. Owner-serialized access is a
    # premise: this does not acquire the separately held native/cut owner lock.
    for suffix in ("-journal", "-wal", "-shm"):
        need(not os.path.lexists(str(custody_root / "ordinary.sqlite") + suffix),
             "CUSTODY_SIDECAR_REQUIRES_OWNER_RECOVERY")
    check()
    custody = O.OrdinaryStore(custody_root, A.S.semantic_id(), custody_limits, create=False)
    try:
        result = helper.write_bundle(loaded, custody, export_ids, policy=args.policy,
                                     output=output, limits=limits, check=check)
    finally:
        custody.close()
    result["controller_limits"] = "COOPERATIVE_REQUIRES_OUTER_SUPERVISOR"
    result["custody_open"] = "READ_WRITE_HANDLE_PRAGMAS_NO_LOGICAL_WRITES"
    result["wall_seconds"] = time.monotonic() - START_WALL
    result["controller_cpu_seconds"] = time.process_time() - START_CPU
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(json.dumps({"status": "REFUSED", "mathematical_acceptance": False,
                          "error": (type(error).__name__ + ": " + str(error))[:2048]},
                         sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)

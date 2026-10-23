"""Select preparation or small-process IPC controls; do not execute the check."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_library_support/"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
MIB = 1024**2


def need(condition, code):
    if not condition:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("name", "package", "profile-sha256"):
        parser.add_argument("--"+name, required=True)
    parser.add_argument("--kind", required=True, choices=("preparation", "protocol"))
    parser.add_argument("--retained-directory")
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode, "LIBRARY_CHECK_SELECTION_CONTEXT")
    need(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", args.name) is not None and
         re.fullmatch(r"[0-9a-f]{64}", args.profile_sha256) is not None,
         "LIBRARY_CHECK_SELECTION_ID")
    destination = LOCAL/(args.name+".selection.json")
    need(not destination.exists() and not (LOCAL/args.name).exists(), "LIBRARY_CHECK_FRESH")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    with builder.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5",
         "LIBRARY_CHECK_PRESERVED_BUILDER")
    spec = importlib.util.spec_from_file_location("_library_check_path_helpers", builder)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(builder), "exec"), B.__dict__)
    package = B.ordinary(args.package, directory=True)
    need(package.is_relative_to(LOCAL), "LIBRARY_CHECK_SELECTED_LOCAL_PACKAGE")
    deadline = time.monotonic()+60
    def check():
        need(time.monotonic() < deadline, "LIBRARY_CHECK_SELECTION_DEADLINE")
    runtime = {}
    def pin(path, expected=None, maximum=128*MIB):
        actual = B.pin(path, check, maximum)
        need(expected is None or actual == expected, "LIBRARY_CHECK_INPUT_PIN")
        runtime[str(path)] = actual["sha256"]
        return actual
    def document(path, expected):
        selected = pin(path, maximum=2*MIB)
        need(selected["sha256"] == expected, "LIBRARY_CHECK_DESCRIPTOR_PIN")
        with path.open("rb") as stream:
            raw = stream.read(2*MIB+1)
        need(len(raw) == selected["bytes"] and hashlib.sha256(raw).hexdigest() == expected,
             "LIBRARY_CHECK_DESCRIPTOR_CHANGED")
        def pairs(items):
            result = {}
            for key, value in items:
                need(key not in result, "LIBRARY_CHECK_DUPLICATE_KEY")
                result[key] = value
            return result
        return json.loads(raw, object_pairs_hook=pairs)
    def relative(name):
        path = PurePosixPath(name)
        need(type(name) is str and path.parts and not path.is_absolute() and
             path.as_posix() == name and "\\" not in name and
             all(part not in (".", "..") and not any(c in ':*?"<>|' for c in part)
                 for part in path.parts), "LIBRARY_CHECK_RELATIVE_PATH")
        return path.parts
    profile = document(package/"PROFILE.json", args.profile_sha256)
    for name, expected in profile["files"].items():
        pin(package.joinpath(*relative(name)), expected)
    installation = document(package/"installation/INSTALLATION.json", profile["installation_manifest_sha256"])
    roots = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    for name, expected in installation["files"].items():
        parts = relative(name)
        path = roots[parts[0]].joinpath(*parts[1:]) if parts[0] in roots else package/"installation"/name
        pin(path, expected)
    runner = "preparation_controls.py" if args.kind == "preparation" else "protocol_controls02.py"
    need((args.retained_directory is not None) == (args.kind == "preparation"),
         "LIBRARY_CHECK_RETAINED_ARGUMENT")
    if args.kind == "preparation":
        retained = B.ordinary(args.retained_directory, directory=True)
        need(retained.is_relative_to(LOCAL), "LIBRARY_CHECK_LOCAL_RETAINED_INPUT")
        # The runner independently requires these exact already-retained
        # fixture identities. No owner or catalog is opened by this selector.
        for filename in ("REQUEST.json", "candidate.json", "targets.json",
                         "owner-request/header.json", "owner-request/group-00000.json",
                         "owner-request/group-00001.json"):
            pin(retained/filename, maximum=MIB)
    sources = {name: B.pin(ROOT/name, check, 2*MIB)["sha256"] for name in (
        "tools/Run-V5-Check.py", PREFIX+"select_protocol02.py", PREFIX+runner)}
    argv = [str(PYTHON/"python.exe"), "-I", "-S", "-B", "{snapshot}\\"+PREFIX.replace("/", "\\")+runner,
            "--package", str(package), "--profile-sha256", args.profile_sha256,
            "--output", "{output}"]
    argv.extend(["--python-runtime", str(PYTHON), "--lean-runtime", str(LEAN)])
    if args.kind == "preparation":
        argv.extend(["--retained-directory", str(retained)])
    limits = dict(wall_seconds=60 if args.kind == "preparation" else 90,
                  cpu_seconds=35 if args.kind == "preparation" else 40,
                  memory_mib=512, active_processes=2 if args.kind == "preparation" else 4,
                  stdout_bytes=MIB, stderr_bytes=MIB)
    need(len(runtime) <= 256, "LIBRARY_CHECK_PIN_COUNT")
    plan = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": args.name, "sources": sources,
            "runtime_pins": runtime, "argv": argv, "limits": limits}
    raw = json.dumps(plan, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":")).encode("ascii")
    B.fresh_bytes(destination, raw)
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}))


if __name__ == "__main__":
    main()

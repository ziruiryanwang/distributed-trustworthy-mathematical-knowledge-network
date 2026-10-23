"""Select one native-free closure check or existing-owner module check; no launch."""
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
PREFIX = "software/v5/ordinary_module_bridge/"
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
    parser.add_argument("--kind", choices=("closure", "native"), required=True)
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
    bridge_names = ("module_closure.py", "module_export.py", "module_worker.py", "OrdinaryModule.lean")
    runner = "closure_controls.py" if args.kind == "closure" else "native_check.py"
    source_names = ("tools/Run-V5-Check.py", PREFIX+"select_check.py", PREFIX+runner)
    source_names += tuple(PREFIX+name for name in (bridge_names if args.kind == "native" else bridge_names[:1]))
    source_pins = {name: B.pin(ROOT/name, check, 2*MIB) for name in source_names}
    sources = {name: value["sha256"] for name, value in source_pins.items()}
    argv = [str(PYTHON/"python.exe"), "-I", "-S", "-B",
            "{snapshot}/"+PREFIX+runner, "--package", str(package),
            "--profile-sha256", args.profile_sha256, "--output", "{output}"]
    if args.kind == "closure":
        for relative in (
            "ordinary-package-lifecycle-continuation-01/contribution/evidence/25ae588e95228a64196a576aa9c9dd78249c23b0c26189c5671a434b93afa1b3.json",
            "ordinary-package-lifecycle-continuation-01/contribution/evidence/c4639e6e5f70e259ea1611adba8e168aa74dbfb91f98e2512cd465f82705e61e.json",
            "ordinary-peer-reciprocal-02/B-contribution/evidence/d52aed3d1d0f94b8ee2236a7ee84435c983c9523dca0f100f4369c183c3d4e51.json"):
            pin(LOCAL/relative, maximum=MIB)
        argv += ["--python-runtime", str(PYTHON), "--lean-runtime", str(LEAN),
                 "--collector-sha256", sources[PREFIX+"module_closure.py"]]
        limits = dict(wall_seconds=60, cpu_seconds=35, memory_mib=512,
                      active_processes=2, stdout_bytes=MIB, stderr_bytes=MIB)
    else:
        old = LOCAL/"ordinary-peer-reciprocal-02"
        for filename in ("RECIPROCAL-RESULT.json", "B-custody-limits.json", "B-catalog/ADOPTION.json"):
            pin(old/filename, maximum=2*MIB)
        for operation in (
            "55cbddc0310a3d93ae4e2c555baa83e0ada1536b0290bf24f95b33d02f448bfe",
            "99303d20602ddd2932ed1fa693f5f29cf3ad91f4698f171e6192cec4d66241bb",
            "f156ac506d2a64dc89c344ead48a3f970834f1602d957a11b2de982a072693f2"):
            pin(old/"B-catalog/operations"/operation/"chunk.olean", maximum=32*MIB)
        bridge_path = LOCAL/(args.name+".bridge-pins.json")
        need(not bridge_path.exists(), "MODULE_CHECK_FRESH_BRIDGE_PINS")
        bridge = {name: source_pins[PREFIX+name] for name in bridge_names}
        raw_bridge = json.dumps(bridge, sort_keys=True, separators=(",", ":")).encode("ascii")
        B.fresh_bytes(bridge_path, raw_bridge)
        bridge_pin = pin(bridge_path, maximum=MIB)
        argv += ["--bridge-pins", str(bridge_path), "--bridge-pins-sha256", bridge_pin["sha256"]]
        limits = dict(wall_seconds=180, cpu_seconds=110, memory_mib=2048,
                      active_processes=8, stdout_bytes=MIB, stderr_bytes=MIB)
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

"""Write one finite file-only library-completion package assembly selection; never launch it."""
from pathlib import Path
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
PREFIX = "software/v5/ordinary_library_package/"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
MIB = 1024**2


def need(condition, code):
    if not condition:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True)
    parser.add_argument("--base-package", required=True)
    parser.add_argument("--base-profile-sha256", required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode, "LIBRARY_SELECTION_CANONICAL")
    need(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", args.name) is not None and
         re.fullmatch(r"[0-9a-f]{64}", args.base_profile_sha256) is not None,
         "LIBRARY_SELECTION_NAME_OR_PIN")
    target = LOCAL/(args.name+".selection.json")
    need(not target.exists() and not (LOCAL/args.name).exists(), "LIBRARY_SELECTION_FRESH")
    spec = importlib.util.spec_from_file_location("_library_selected_assembler", ROOT/PREFIX/"assemble.py")
    S = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(S)  # Definition-only selected source, not assemble().
    B = S.bootstrap(ROOT/S.BUILDER, "_library_selected_preserved_builder", S.BUILDER_SHA)
    base = B.ordinary(args.base_package, directory=True)
    need(base.is_relative_to(LOCAL), "LIBRARY_SELECTION_LOCAL_BASE")
    deadline = time.monotonic()+60

    def check():
        need(time.monotonic() < deadline, "LIBRARY_SELECTION_DEADLINE")

    def read_doc(path, expected):
        selected = B.pin(path, check, 2*MIB)
        need(selected["sha256"] == expected, "LIBRARY_SELECTION_DESCRIPTOR_PIN")
        with path.open("rb") as stream:
            raw = stream.read(2*MIB+1)
        need(len(raw) == selected["bytes"] and hashlib.sha256(raw).hexdigest() == expected,
             "LIBRARY_SELECTION_DESCRIPTOR_CHANGED")
        def pairs(items):
            result = {}
            for key, value in items:
                need(key not in result, "LIBRARY_SELECTION_DUPLICATE_KEY")
                result[key] = value
            return result
        return json.loads(raw, object_pairs_hook=pairs)

    profile = read_doc(base/"PROFILE.json", args.base_profile_sha256)
    installation = read_doc(base/"installation/INSTALLATION.json", profile["installation_manifest_sha256"])
    need(B.pin(base/"profile.py", check, 2*MIB)["sha256"] == S.BASE_LOADER_SHA,
         "LIBRARY_SELECTION_BASE_LOADER_VERSION")
    owner = S.bootstrap(base/"owner.py", "_library_selection_base_owner", S.BASE_OWNER_SHA)
    loader = owner.bootstrap(base, args.base_profile_sha256, check)
    # Reuse the pure relative-path rules without loading core or opening state.
    runtime = {str(base/"PROFILE.json"): args.base_profile_sha256,
               str(base/"installation/INSTALLATION.json"): profile["installation_manifest_sha256"]}
    for name, expected in profile["files"].items():
        path = base.joinpath(*loader.relative(name).parts)
        need(B.pin(path, check, 128*MIB) == expected, "LIBRARY_SELECTION_BASE_PAYLOAD")
        runtime[str(path)] = expected["sha256"]
    roots = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    for name, expected in installation["files"].items():
        parts = loader.relative(name).parts
        path = roots[parts[0]].joinpath(*parts[1:]) if parts[0] in roots else base/"installation"/name
        need(B.pin(path, check, 128*MIB) == expected, "LIBRARY_SELECTION_INSTALLED_PAYLOAD")
        runtime[str(path)] = expected["sha256"]
    names = {"tools/Run-V5-Check.py", PREFIX+"select_assembly.py", PREFIX+"assemble.py",
             S.BUILDER, *S.SOURCES.values()}
    sources = {name: B.pin(ROOT/name, check, 2*MIB)["sha256"] for name in sorted(names)}
    for name in (S.BUILDER, PREFIX+"assemble.py", *S.SOURCES.values()):
        runtime[str(ROOT/name)] = sources[name]
    need(len(runtime) <= 256, "LIBRARY_SELECTION_RUNTIME_CENSUS")
    plan = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": args.name,
        "sources": sources, "runtime_pins": runtime,
        "argv": [str(PYTHON/"python.exe"), "-I", "-S", "-B",
            r"{snapshot}\software\v5\ordinary_library_package\assemble.py",
            "--source-root", str(ROOT), "--base-package", str(base),
            "--base-profile-sha256", args.base_profile_sha256,
            "--python-runtime", str(PYTHON), "--lean-runtime", str(LEAN),
            "--output", r"{output}\package", "--wall-seconds", "60", "--cpu-seconds", "40"],
        "limits": {"wall_seconds": 90, "cpu_seconds": 50, "memory_mib": 512,
                   "active_processes": 2, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    raw = json.dumps(plan, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":")).encode("ascii")
    B.fresh_bytes(target, raw)
    print(json.dumps({"selection": str(target), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}))


if __name__ == "__main__":
    main()

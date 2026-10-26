"""Prepare one finite build selection from an already approved source extraction.

This does not launch the builder, copy another source tree or approve a release.
The owner supplies the adopted exact outer-manifest hash after the controls gate.
Only the pinned current bundle and its pinned file helper execute for verification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import types

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_current_release/"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
MIB = 1024**2
BUNDLE_SHA = "437cc3c083d62b2e792ace0d3243552d8c15d02fea6b827ec256dda83829f1bd"
BUILDER_SHA = "86612e8c76cf7281e942ea9e55705ba53de85d2c6efb45950561532997055d03"
RUNNER_SHA = "44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651"


def need(ok, code):
    if not ok:
        raise ValueError("CURRENT_BUILD_SELECTION_" + code)


def bundle_module():
    path = ROOT / PREFIX / "bundle.py"
    for ancestor in (*reversed(path.parents), path):
        info = ancestor.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "BUNDLE_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if ancestor != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == 14420,
             "BUNDLE_PATH")
    with path.open("rb") as stream:
        raw = stream.read(14421)
    need(len(raw) == 14420 and hashlib.sha256(raw).hexdigest() == BUNDLE_SHA, "BUNDLE_PIN")
    module = types.ModuleType("_current_release_build_selection_bundle")
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--name", required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize and
         Path(__file__).absolute() == ROOT / PREFIX / "select_build.py", "PROCESS")
    need(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", args.name) is not None and
         re.fullmatch(r"[0-9a-f]{64}", args.manifest_sha256) is not None, "ARGUMENTS")
    bundle = bundle_module()
    H = bundle.helper()
    check = H.guard()
    extraction = H.ordinary(args.source_root, directory=True)
    need(extraction.is_relative_to(ROOT / "experiments"), "LOCAL_ADOPTED_EXTRACTION")
    selection = H.ordinary(LOCAL / (args.name + ".selection.json"), fresh=True)
    output = H.ordinary(LOCAL / args.name, directory=True, fresh=True)
    need(not extraction.is_relative_to(output) and not output.is_relative_to(extraction),
         "OUTPUT_EXTRACTION_OVERLAP")
    verified = bundle.verify(extraction, args.manifest_sha256, check=check)
    need(verified["kind"] == "source" and len(verified["files"]) == 106,
         "SOURCE_DISTRIBUTION_REQUIRED")
    files = dict(verified["files"])
    files[bundle.MANIFEST] = verified["manifest"]
    need(len(files) == 107 and files[PREFIX + "bundle.py"]["sha256"] == BUNDLE_SHA and
         files[PREFIX + "build.py"]["sha256"] == BUILDER_SHA,
         "REVIEWED_BUILD_AND_BUNDLE")
    release, _ = bundle.selection(extraction, check)
    runtime_map = release["build"]["runtime_pins"]
    need(type(runtime_map) is dict and len(runtime_map) == 23, "RUNTIME_CENSUS")
    runtimes = {"python_runtime": H.ordinary(PYTHON, directory=True),
                "lean_runtime": H.ordinary(LEAN, directory=True)}
    need(Path(sys.executable).resolve() == PYTHON / "python.exe", "RUNNING_PYTHON")
    pins = {str(extraction / relative): pin for relative, pin in files.items()}

    def check_pin(path, expected):
        H.ordinary(path)
        bundle.checked_pin(expected, 512*MIB)
        need(path.stat().st_size == expected["bytes"], "INPUT_LENGTH")
        digest, size = hashlib.sha256(), 0
        with path.open("rb") as stream:
            while block := stream.read(MIB):
                check(); size += len(block)
                need(size <= expected["bytes"], "INPUT_GREW")
                digest.update(block)
        need(size == H.ordinary(path).stat().st_size == expected["bytes"] and
             digest.hexdigest() == expected["sha256"], "INPUT_PIN:" + str(path))

    for name, pin in runtime_map.items():
        H.relative(name)
        category, relative = name.split("/", 1)
        need(category in runtimes, "RUNTIME_ROOT")
        path = runtimes[category] / relative
        need(str(path) not in pins, "INPUT_OVERLAP")
        check_pin(path, pin)
        pins[str(path)] = pin
    need(len(pins) == 130 and len({p.casefold() for p in pins}) == 130, "ALL_INPUT_CENSUS")
    selected = ("tools/Run-V5-Check.py", PREFIX + "select_build.py",
                PREFIX + "BUILD-PLAN.md", PREFIX + "build.py", PREFIX + "bundle.py",
                PREFIX + "release.json", bundle.HELPER)
    sources = {name: H.pin(H.read(ROOT / name, check)) for name in selected}
    need(sources["tools/Run-V5-Check.py"]["sha256"] == RUNNER_SHA and
         all(sources[name] == files[name] for name in
             (PREFIX + "build.py", PREFIX + "bundle.py", PREFIX + "release.json", bundle.HELPER)),
         "REVIEWED_SOURCE_MATCHES_EXTRACTION")
    plan = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": args.name,
        "sources": {name: pin["sha256"] for name, pin in sources.items()},
        "runtime_pins": {name: pin["sha256"] for name, pin in pins.items()},
        "argv": [str(PYTHON / "python.exe"), "-I", "-S", "-B",
            r"{snapshot}\software\v5\ordinary_current_release\build.py",
            "--source-root", str(extraction), "--python-runtime", str(PYTHON),
            "--lean-runtime", str(LEAN), "--output", r"{output}\distribution",
            "--wall-seconds", "480", "--cpu-seconds", "360", "--memory-mib", "2048"],
        "limits": {"wall_seconds": 540, "cpu_seconds": 440, "memory_mib": 2304,
                   "active_processes": 8, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    bundle.check_tree(extraction, files, check)
    for name, pin in pins.items():
        check_pin(Path(name), pin)
    for name, pin in sources.items():
        need(H.pin(H.read(ROOT / name, check)) == pin, "SOURCE_CHANGED")
    raw = H.canonical(plan)
    need(len(raw) <= MIB, "SELECTION_BOUND")
    check()
    H.fresh_bytes(selection, raw)
    need(H.read(selection, check) == raw, "SELECTION_READBACK")
    print(json.dumps({"selection": str(selection), "sha256": H.sha(raw),
        "source_root": str(extraction), "manifest_sha256": args.manifest_sha256,
        "extraction_files": 107, "external_runtime_files": 23, "runtime_pins": 130,
        "source_snapshots": len(sources), "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()

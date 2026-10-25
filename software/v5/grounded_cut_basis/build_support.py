"""Build only the reviewed grounded-cut addition; root selects execution later.

Reuse the exact approved ordinary package and its existing supervisor. No base
rebuild, owner/catalog open, native mathematical request, retry or acceptance.
An outer Run-V5-Check Job must contain this controller and its entire child tree.
"""
from __future__ import annotations

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
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
PROFILE = "9c41b9a3fe36f7283af130ac6ef290e82c2a78c432980b2bea75ccdcf197a6d4"
MIB = 1024**2
SOURCES = {"GroundedCut.lean", "GroundedCutDriver.lean", "cut_worker.py",
           "cut_runtime.py", "cut_controller.py", "source_anchor.py",
           "cut_map.py", "cut_summary.py", "cut_catalog.py", "cut_bootstrap.py"}
OBJECTS = {"GroundedCut" + suffix for suffix in
           (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")}
REUSED_SOURCES = {
    "cut_map.py": "6d82a30944ce1a0190aff1bdf3e035b6ee9c8b7c1ae5f46708666907d74d077c",
    "cut_summary.py": "d13a04b1a4e97501bfd2af74cf88e317a613c31efc0dc5a084f26086f585f586",
    "cut_catalog.py": "f51e16b1b0fc08d35c1ce55cfc6f2cee2d9161624f30850c6ab5fdf0cdcee843",
}


def need(ok, code):
    if not ok:
        raise ValueError("CUT_BUILD_" + code)


def ordinary(path, *, directory=False, fresh=False):
    path = Path(path)
    need(path.is_absolute() and ".." not in path.parts and len(path.parts) <= 128 and
         len(str(path)) <= 32768, "ABSOLUTE_PATH")
    for item in (*reversed(path.parents), path):
        try:
            info = item.lstat()
        except FileNotFoundError:
            need(item == path and fresh, "MISSING_PATH")
            return path
        need(not stat.S_ISLNK(info.st_mode) and not
             (getattr(info, "st_file_attributes", 0) & 0x400), "REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if item != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PATH_KIND")
    return path


def read(path, maximum, check):
    check()
    path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    need(len(raw) == size, "FILE_CHANGED")
    check()
    return raw


def pin(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def load(name, path, raw):
    need(name not in sys.modules, "PRELOADED_MODULE")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def compile_worker(arguments):
    """Fixed native commands only, inside the original inherited supervised Job."""
    need(len(arguments) == 5, "WORKER_ARGUMENTS")
    addition, base = (ordinary(value, directory=True) for value in arguments[:2])
    deadline = float(arguments[2])
    own_sha, expected_profile = arguments[3:]
    need(math.isfinite(deadline) and 0 < deadline - time.monotonic() <= 600 and
         expected_profile == PROFILE, "WORKER_ORIGINAL_DEADLINE")
    def check():
        need(time.monotonic() < deadline, "WORKER_DEADLINE")
    need(pin(read(Path(__file__).absolute(), 2 * MIB, check))["sha256"] == own_sha,
         "WORKER_SOURCE_CHANGED")
    need(pin(read(base / "PROFILE.json", 2 * MIB, check))["sha256"] == PROFILE,
         "WORKER_BASE_CHANGED")
    objects = ordinary(addition / "lean-lib", directory=True)
    need(not any(objects.iterdir()), "WORKER_FRESH_OBJECTS")
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
    env["PATH"] = os.pathsep.join((str(PYTHON), str(LEAN / "bin")))
    env["LEAN_PATH"] = os.pathsep.join(map(str, (objects, base / "authoring/helpers",
                                                base / "installation/lean-lib")))
    commands = (
        ("conditional-helper-compile", [str(LEAN / "bin/lean.exe"), "-DElab.async=false",
            "-R", str(addition), "-o", str(objects / "GroundedCut.olean"),
            str(addition / "GroundedCut.lean")]),
        ("driver-typecheck-no-main", [str(LEAN / "bin/lean.exe"), "-DElab.async=false",
            "-R", str(addition), str(addition / "GroundedCutDriver.lean")]))
    for phase, argv in commands:
        check()
        code = subprocess.call(argv, cwd=addition, env=env, stdin=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        print(json.dumps({"phase": phase, "exit_code": code}), flush=True)
        need(code == 0, "NATIVE_COMMAND_FAILED:" + phase)
        check()
    return 0


def build(args):
    started, cpu_started, worker_cpu = time.monotonic(), time.process_time(), 0.0
    need(35 <= args.wall_seconds <= 600 and 4 <= args.cpu_seconds <= 600 and
         256 <= args.memory_mib <= 4096, "ORIGINAL_FINITE_ALLOCATION")
    deadline = started + args.wall_seconds
    def check():
        need(time.monotonic() < deadline and
             time.process_time() - cpu_started + worker_cpu < args.cpu_seconds,
             "ORIGINAL_ALLOWANCE")
    source = ordinary(args.source_root, directory=True)
    base = ordinary(args.base_package, directory=True)
    output = ordinary(args.output, directory=True, fresh=True)
    need(source.is_relative_to(ROOT / "experiments") and
         output.is_relative_to(ROOT / "experiments") and
         Path(__file__).absolute() == source / "build_support.py", "SELECTED_SNAPSHOT")
    paths = (source, base, output, ordinary(PYTHON, directory=True), ordinary(LEAN, directory=True))
    for index, left in enumerate(paths):
        for right in paths[index + 1:]:
            need(not left.is_relative_to(right) and not right.is_relative_to(left), "PATH_OVERLAP")
    profile_raw = read(base / "PROFILE.json", 2 * MIB, check)
    need(pin(profile_raw)["sha256"] == PROFILE, "BASE_PROFILE_PIN")
    # This exact externally pinned descriptor is trusted selection, not peer JSON.
    descriptor = json.loads(profile_raw)
    owner_raw = read(base / "owner.py", 2 * MIB, check)
    need(pin(owner_raw) == descriptor["files"]["owner.py"], "BASE_OWNER_PIN")
    owner = load("_dmkn_cut_build_owner", base / "owner.py", owner_raw)
    profile = owner.bootstrap(base, PROFILE, check)
    loaded = profile.load(base, PROFILE, {"python_runtime": PYTHON, "lean_runtime": LEAN},
                          deadline, check_parent=check)
    E, P = loaded.A.E, loaded.A.P
    need(loaded.descriptor == descriptor, "BASE_LOADED_DESCRIPTOR")
    own_raw = read(source / "build_support.py", 2 * MIB, check)
    own_pin = pin(own_raw)
    # Run-V5-Check preserves canonical relative source paths in its immutable
    # snapshot. Reuse the three old helpers from that snapshot's sibling only,
    # never from the live source directory or an existing used support build.
    source_paths = {name: (source.parent / "grounded_cut" / name
                          if name in REUSED_SOURCES else source / name)
                    for name in sorted(SOURCES)}
    selected = {name: read(path, 2 * MIB, check) for name, path in source_paths.items()}
    need(sum(map(len, selected.values())) <= 16 * MIB, "SOURCE_TOTAL_BOUND")
    source_pins = {name: pin(raw) for name, raw in selected.items()}
    need(all(source_pins[name]["sha256"] == digest
             for name, digest in REUSED_SOURCES.items()), "UNCHANGED_HELPER_PINS")
    output.mkdir()
    addition = output / "addition"
    addition.mkdir()
    (addition / "lean-lib").mkdir()
    for name, raw in selected.items():
        check()
        P.PortableCatalog._write_fresh(addition / name, raw)
        need(read(addition / name, 2 * MIB, check) == raw, "COPY_CHANGED")
    P.PortableCatalog._write_fresh(output / "SOURCE-PINS.json", E.canonical_json(
        {"builder": own_pin, "sources": source_pins, "base_profile_sha256": PROFILE}))
    supervisor, job = loaded.installation._supervisor, loaded.installation._job_module
    check()
    # Same cleanup/bookkeeping reserve as the approved OperationBudget.allowance.
    remaining_wall = math.floor(deadline - time.monotonic()) - 24
    remaining_cpu = math.floor(args.cpu_seconds - (time.process_time() - cpu_started) - worker_cpu) - 1
    need(remaining_wall >= 1 and remaining_cpu >= 1, "INSUFFICIENT_REMAINING_BUDGET")
    limits = supervisor.limits_checked({
        "wall_seconds": remaining_wall, "cpu_seconds": remaining_cpu,
        "memory_mib": args.memory_mib, "active_processes": 4,
        "stdout_bytes": MIB, "stderr_bytes": MIB})
    argv = [str(PYTHON / "python.exe"), "-I", "-S", "-B", str(source / "build_support.py"),
            "--compile-worker", str(addition), str(base), str(deadline), own_pin["sha256"], PROFILE]
    observation = supervisor.supervise(argv, output, output / "compile", limits, job.Job)
    supervisor.save_new(output / "compile-observation.json", observation)
    final = observation.get("final_job")
    measured = final.get("cpu_seconds") if type(final) is dict else None
    known_cpu = type(measured) in (int, float) and math.isfinite(measured) and measured >= 0
    if known_cpu:
        worker_cpu += measured
    need(loaded.A._clean_worker(observation), "NATIVE_BUILD_NOT_CLEAN")
    need(known_cpu, "WORKER_CPU_ACCOUNTING")
    check()
    files = dict(source_pins)
    compiled = set()
    for path in (addition / "lean-lib").iterdir():
        check()
        need(path.name in OBJECTS and path.name not in compiled, "COMPILED_CENSUS")
        files["lean-lib/" + path.name] = pin(read(path, 64 * MIB, check))
        compiled.add(path.name)
    need("GroundedCut.olean" in compiled and
         sum(item["bytes"] for item in files.values()) <= 512 * MIB, "COMPILED_SUPPORT_BOUND")
    actual = {path.name for path in addition.iterdir()}
    need(actual == SOURCES | {"lean-lib"}, "ADDITION_CENSUS")
    for name, raw in selected.items():
        need(read(source_paths[name], 2 * MIB, check) == raw and
             read(addition / name, 2 * MIB, check) == raw, "FINAL_SOURCE_CHANGED")
    need(read(source / "build_support.py", 2 * MIB, check) == own_raw and
         read(base / "PROFILE.json", 2 * MIB, check) == profile_raw, "FINAL_INPUT_CHANGED")
    # Last payload write inside addition. Presence alone is not build adoption.
    manifest = E.canonical_json({"schema": "DMKN_GROUNDED_CUT_BASIS_SUPPORT_V1",
                                "base_profile_sha256": PROFILE, "files": files})
    P.PortableCatalog._write_fresh(addition / "CUT-SUPPORT.json", manifest)
    manifest_sha = hashlib.sha256(manifest).hexdigest()
    bootstrap = load("cut_bootstrap", addition / "cut_bootstrap.py", selected["cut_bootstrap.py"])
    assembled = bootstrap.load(addition, manifest_sha, loaded, check=check)
    need(assembled.support.manifest_raw == manifest and assembled.support.base is loaded,
         "ASSEMBLED_LOADER_BINDING")
    check()
    result = {"schema": "DMKN_GROUNDED_CUT_BASIS_SUPPORT_BUILD_V1",
        "status": "SUPPORT_COMPILED_AND_LOADED_NOT_MATHEMATICAL_ACCEPTANCE",
        "base_profile_sha256": PROFILE, "manifest_sha256": manifest_sha,
        "support_id": assembled.support.support_id, "sources": source_pins,
        "compiled": {name: files[name] for name in files if name.startswith("lean-lib/")},
        "native_compilations": 1, "driver_typechecks_without_main": 1,
        "mathematical_requests": 0, "catalogs_opened": 0,
        "wall_seconds": time.monotonic() - started, "worker_cpu_seconds": worker_cpu,
        "controller_cpu_seconds": time.process_time() - cpu_started}
    supervisor.save_new(output / "BUILD-RESULT.json", result)
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON / "python.exe", "PINNED_PYTHON_PROCESS")
    if len(sys.argv) > 1 and sys.argv[1] == "--compile-worker":
        return compile_worker(sys.argv[2:])
    need(Path.cwd() == ROOT, "CANONICAL_WORKDIR")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("source-root", "base-package", "output"):
        parser.add_argument("--" + name, required=True)
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--" + name, required=True, type=int)
    return build(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())

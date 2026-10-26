"""Compile only the five affected receiver modules in a fresh eight-module tree.

Root selects execution separately through Run-V5-Check. No authoring rebuild,
fixture run, owner state, package assembly, retry or mathematical acceptance.
Used input snapshots and partial outputs remain intact on every failure.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
BASE = ROOT / "experiments/v5-local-checks/intake-progress-package01/distribution/package"
PROFILE = "b850b12a96667b9a31984fe86fc0330517db9b5172bd6e63982782c10ee3ae47"
INSTALLATION = "a7403d6b798a654f7e5c76a863304bf415ad6016c6634a35513e73657ab0f9eb"
HELPER = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
CHANGED = ("CheckedExtension", "LocalSnapshot", "OrdinaryWorkflowWorker")
REUSED = ("OriginalExpr", "OriginalDecl", "BootstrapSupport")
COMPILE = ("CheckedExtension", "LocalSnapshot", "OrdinaryExport", "BasisSnapshot", "OrdinaryWorkflowWorker")
MODULES = (*REUSED, *COMPILE)
COMPANIONS = (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError("KERNEL_BUILD_" + code)


def load(name, path):
    need(name not in sys.modules, "MODULE_ALREADY_LOADED")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def compile_worker(arguments):
    """Fixed sequential compiler calls inside one inherited, bounded Job."""
    need(len(arguments) == 3, "WORKER_ARGUMENTS")
    output, deadline_text, own_sha = arguments
    output = Path(output)
    deadline = float(deadline_text)
    need(math.isfinite(deadline) and 0 < deadline - time.monotonic() <= 300,
         "WORKER_ORIGINAL_DEADLINE")
    need(hashlib.sha256(Path(__file__).read_bytes()).hexdigest() == own_sha,
         "WORKER_SOURCE_CHANGED")
    need(output.name == "native" and output.parent.parent == ROOT / "experiments/v5-local-checks",
         "WORKER_OUTPUT_SCOPE")
    source, objects = output / "lean-src", output / "lean-lib"
    need({p.name for p in source.iterdir()} == {n + ".lean" for n in MODULES} and
         {p.name for p in objects.iterdir()} == {n + ".olean" for n in REUSED},
         "WORKER_INITIAL_CENSUS")
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
    env["PATH"] = os.pathsep.join((str(PYTHON), str(LEAN / "bin")))
    env["LEAN_PATH"] = str(objects)
    for module in COMPILE:
        need(time.monotonic() < deadline, "WORKER_DEADLINE")
        argv = [str(LEAN / "bin/lean.exe"), "-DElab.async=false", "-R", str(source),
                "-o", str(objects / (module + ".olean")), str(source / (module + ".lean"))]
        code = subprocess.call(argv, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        print(json.dumps({"module": module, "exit_code": code}), flush=True)
        need(code == 0, "COMPILE_FAILED:" + module)
        need(time.monotonic() < deadline, "WORKER_DEADLINE")
    return 0


def build(args):
    started, cpu_started, worker_cpu = time.monotonic(), time.process_time(), 0.0
    need(35 <= args.wall_seconds <= 300 and 4 <= args.cpu_seconds <= 240 and
         256 <= args.memory_mib <= 1536, "FINITE_ALLOCATION")
    deadline = started + args.wall_seconds

    def check():
        need(time.monotonic() < deadline and
             time.process_time() - cpu_started + worker_cpu < args.cpu_seconds, "ORIGINAL_ALLOWANCE")

    source = Path(args.source_root)
    need(source == Path(__file__).resolve().parent and
         source.is_relative_to(ROOT / "experiments/v5-local-checks") and
         source.parts[-4:] == ("sources", "software", "v5", "ordinary_kernel_admission"),
         "OWNER_SOURCE_SNAPSHOT")
    helper_path = source.parent / "ordinary_fair_search/assemble.py"
    need(hashlib.sha256(helper_path.read_bytes()).hexdigest() == HELPER, "FILE_HELPER_PIN")
    H = load("_kernel_build_files", helper_path)
    H.ordinary(source, directory=True)
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    need(output == source.parents[3] / "native", "OUTPUT_SCOPE")
    selected = {}

    def remember(path, expected=None, maximum=128*MIB):
        actual = H.pin(path, check, maximum)
        need(expected is None or actual == expected or
             isinstance(expected, str) and actual["sha256"] == expected, "INPUT_PIN:" + str(path))
        key = str(path)
        need(key not in selected or selected[key] == actual, "INPUT_OVERLAP")
        selected[key] = actual
        return actual

    own_pin = remember(source / "build.py")
    remember(helper_path, HELPER)
    descriptor, _ = H.read_json(BASE / "PROFILE.json", PROFILE, check)
    manifest, _ = H.read_json(BASE / "installation/INSTALLATION.json", INSTALLATION, check)
    remember(BASE / "PROFILE.json", PROFILE)
    remember(BASE / "installation/INSTALLATION.json", INSTALLATION)
    need(descriptor["installation_manifest_sha256"] == INSTALLATION, "BASE_BINDING")
    source_inputs = {}
    for module in MODULES:
        path = (source / (module + ".lean") if module in CHANGED else
                BASE / "installation/lean-src" / (module + ".lean"))
        expected = None if module in CHANGED else manifest["files"]["lean-src/" + module + ".lean"]
        source_inputs[module] = (path, remember(path, expected, 2*MIB))
    object_inputs = {module: (BASE / "installation/lean-lib" / (module + ".olean"),
        manifest["files"]["lean-lib/" + module + ".olean"]) for module in REUSED}
    for path, expected in object_inputs.values():
        remember(path, expected)
    runtime_roots = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    runtime_pins = {}
    for name, expected in manifest["files"].items():
        head, _, relative = name.partition("/")
        if head in runtime_roots:
            path = runtime_roots[head] / relative
            runtime_pins[str(path)] = remember(path, expected)
    need(len(runtime_pins) == 9, "NAMED_RUNTIME_CENSUS")
    supervisor_inputs = {}
    for name in ("commons.py", "domains.py", "run_stage.py"):
        path = BASE / "installation/supervisor" / name
        supervisor_inputs[name] = (path, remember(path, manifest["files"]["supervisor/" + name], 2*MIB))
    need(sum(pin["bytes"] for _, pin in source_inputs.values()) <= 2*MIB, "SOURCE_TOTAL")
    output.mkdir()
    for directory in ("lean-src", "lean-lib", "inputs"):
        (output / directory).mkdir()
    staged = {}

    def copy(path, target, expected):
        need(H.pin(path, check) == expected, "COPY_INPUT_CHANGED")
        with H.ordinary(path).open("rb") as incoming, H.ordinary(target, fresh=True).open("xb") as outgoing:
            count = 0
            while block := incoming.read(MIB):
                check(); count += len(block)
                need(count <= expected["bytes"], "COPY_GREW")
                outgoing.write(block)
            outgoing.flush(); os.fsync(outgoing.fileno())
        need(H.pin(target, check) == expected, "COPY_READBACK")
        staged[str(target)] = expected

    for module, (path, expected) in source_inputs.items():
        copy(path, output / "lean-src" / (module + ".lean"), expected)
    for module, (path, expected) in object_inputs.items():
        copy(path, output / "lean-lib" / (module + ".olean"), expected)
    for name, (path, expected) in supervisor_inputs.items():
        copy(path, output / "inputs" / name, expected)
    H.fresh_bytes(output / "INPUTS.json", H.canonical({"base_profile_sha256": PROFILE,
        "base_installation_sha256": INSTALLATION, "inputs": selected,
        "compile_order": list(COMPILE), "reused_objects": list(REUSED)}))
    supervisor = load("_kernel_build_supervisor", output / "inputs/commons.py")
    load("domains", output / "inputs/domains.py")
    job = load("_kernel_build_job", output / "inputs/run_stage.py")
    remaining_wall = math.floor(deadline - time.monotonic()) - 24
    remaining_cpu = math.floor(args.cpu_seconds - (time.process_time() - cpu_started)) - 1
    need(remaining_wall >= 1 and remaining_cpu >= 1, "REMAINING_ALLOWANCE")
    limits = supervisor.limits_checked({"wall_seconds": remaining_wall, "cpu_seconds": remaining_cpu,
        "memory_mib": args.memory_mib, "active_processes": 4, "stdout_bytes": MIB, "stderr_bytes": MIB})
    argv = [str(PYTHON / "python.exe"), "-I", "-S", "-B", str(source / "build.py"),
            "--compile-worker", str(output), str(deadline - 24), own_pin["sha256"]]
    observation = supervisor.supervise(argv, ROOT, output / "compile", limits, job.Job)
    supervisor.save_new(output / "SUPERVISION.json", observation)
    final = observation.get("final_job")
    measured = final.get("cpu_seconds") if type(final) is dict else None
    known_cpu = type(measured) in (int, float) and math.isfinite(measured) and measured >= 0
    if known_cpu:
        worker_cpu = measured
    need(observation.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED" and
         observation.get("child_exit_code") == 0 and observation.get("direct_child_reaped") is True and
         observation.get("job_closed") is True and observation.get("cleanup_errors") == [] and
         observation.get("termination_requested") is False and type(final) is dict and
         final.get("active_processes") == 0 and final.get("terminated_processes") == 0 and known_cpu,
         "COMPILER_NOT_CLEAN")
    need((output / "compile/stderr.txt").stat().st_size == 0, "NATIVE_DIAGNOSTICS")
    check()
    allowed = {n + s for n in COMPILE for s in COMPANIONS} | {n + ".olean" for n in REUSED}
    compiled = {}
    for path in (output / "lean-lib").iterdir():
        need(path.name in allowed and path.name not in compiled, "COMPILED_CENSUS")
        compiled[path.name] = H.pin(path, check, 64*MIB)
    need({n + ".olean" for n in MODULES} <= compiled.keys() and
         sum(pin["bytes"] for pin in compiled.values()) <= 128*MIB, "COMPILED_BOUND")
    H.census(output / "lean-src", {n + ".lean" for n in MODULES}, check)
    for path, expected in (*selected.items(), *staged.items()):
        need(H.pin(Path(path), check) == expected, "FINAL_INPUT_OR_COPY_CHANGED")
    module_map = {module: {"source": source_inputs[module][1],
        "object": compiled[module + ".olean"],
        "object_origin": "reused_exact" if module in REUSED else "compiled",
        "source_origin": str(source_inputs[module][0])} for module in MODULES}
    result = {"status": "COMPILED_NOT_TESTED_OR_ADOPTED", "base_profile_sha256": PROFILE,
        "base_installation_sha256": INSTALLATION, "modules": module_map, "compiled_files": compiled,
        "native_compilations": 5, "mathematical_requests": 0, "owner_states_opened": 0,
        "wall_seconds": time.monotonic() - started, "worker_cpu_seconds": worker_cpu,
        "controller_cpu_seconds": time.process_time() - cpu_started,
        "runtime_scope": "EXPLICIT_NAMED_SUPPORT_NOT_HERMETIC_TOOLCHAIN"}
    check()
    H.fresh_bytes(output / "BUILD.json", H.canonical(result))
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0


def main():
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON / "python.exe", "ISOLATED_CANONICAL_PROCESS")
    if len(sys.argv) > 1 and sys.argv[1] == "--compile-worker":
        return compile_worker(sys.argv[2:])
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("source-root", "output"):
        parser.add_argument("--" + name, required=True)
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--" + name, type=int, required=True)
    return build(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())

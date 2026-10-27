"""Compile four authoring helpers under one externally selected bounded Job.

Run only through Run-V5-Check. No owner, test, receiver rebuild or installation.
Compiler diagnostics and partial output are preserved; there is no retry.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
BASE = ROOT / "experiments/v5-local-checks/kernel-admission-package01/distribution/package"
PROFILE = "60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b"
INSTALLATION = "9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27"
HELPER = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
MODULES = ("OwnerConstruction", "PortableOwnerConstructCommand",
           "PortableConstructExportCommand", "PortableContributionExportCommand")
PARTS = (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")
UNCHANGED = {
    "PortableConstructExportCommand": "8251bc13836fde6620203752b9378bfafccefeef16587788221dec7ad7e95a8b",
    "PortableContributionExportCommand": "dc6988a6a237f482fed6f9055d8a248e430c8c99cb17c70a4a110774717e0182",
}
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError("FRONTIER_BUILD_" + code)


def main():
    started = time.monotonic()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON / "python.exe", "CANONICAL_PROCESS")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    need(source.is_relative_to(ROOT / "experiments/v5-local-checks") and
         source.parts[-4:] == ("sources", "software", "v5", "ordinary_demand_frontier"),
         "SOURCE_SNAPSHOT")
    helper = source.parent / "ordinary_fair_search/assemble.py"
    raw = helper.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == HELPER, "FILE_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_frontier_build_files", helper)
    H = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = H
    exec(compile(raw, str(helper), "exec", dont_inherit=True), H.__dict__)
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    need(output == source.parents[3] / "native", "OUTPUT_SCOPE")

    def check():
        # A second wall guard only. The enclosing Job accounts for all child CPU,
        # memory, process and stream limits, including interrupted compiler calls.
        need(time.monotonic() - started < 120, "WALL_GUARD")

    inputs = {}

    def remember(path, expected=None, maximum=128*MIB):
        actual = H.pin(path, check, maximum)
        need(expected is None or actual == expected or
             isinstance(expected, str) and actual["sha256"] == expected,
             "INPUT_PIN:" + str(path))
        key = str(path)
        need(key not in inputs or inputs[key] == actual, "INCONSISTENT_INPUT")
        inputs[key] = actual
        return actual

    remember(Path(__file__))
    remember(helper, HELPER)
    profile, _ = H.read_json(BASE / "PROFILE.json", PROFILE, check)
    installation, _ = H.read_json(BASE / "installation/INSTALLATION.json", INSTALLATION, check)
    remember(BASE / "PROFILE.json", PROFILE)
    remember(BASE / "installation/INSTALLATION.json", INSTALLATION)
    need(profile["installation_manifest_sha256"] == INSTALLATION, "BASE_BINDING")
    helper_pins = {name: pin for name, pin in profile["files"].items()
                   if name.startswith("authoring/helpers/")}
    need(len(helper_pins) == 70 and
         {"authoring/helpers/" + m + ext for m in MODULES for ext in PARTS} <= helper_pins.keys(),
         "BASE_HELPER_CENSUS")
    H.census(BASE / "authoring/helpers", {Path(name).name for name in helper_pins}, check)
    for name, expected in helper_pins.items():
        remember(BASE / name, expected)
    for name, expected in installation["files"].items():
        head, _, tail = name.partition("/")
        if head in ("python_runtime", "lean_runtime"):
            remember((PYTHON if head == "python_runtime" else LEAN) / tail, expected)
    source_pins = {m: remember(source / (m + ".lean"), UNCHANGED.get(m), 2*MIB)
                   for m in MODULES}
    need(sum(pin["bytes"] for pin in source_pins.values()) <= 2*MIB, "SOURCE_TOTAL")
    output.mkdir()
    src, objects = output / "lean-src", output / "lean-lib"
    src.mkdir(); objects.mkdir()
    for module, expected in source_pins.items():
        raw = (source / (module + ".lean")).read_bytes()
        need(len(raw) == expected["bytes"] and hashlib.sha256(raw).hexdigest() == expected["sha256"],
             "SOURCE_COPY_CHANGED")
        H.fresh_bytes(src / (module + ".lean"), raw)
    H.fresh_bytes(output / "INPUTS.json", H.canonical({"profile_sha256": PROFILE,
        "installation_sha256": INSTALLATION, "inputs": inputs,
        "source_pins": source_pins, "compile_order": list(MODULES)}))
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith(("LEAN", "PYTHON", "ELAN")) and k.upper() != "PATH"}
    env["PATH"] = os.pathsep.join((str(PYTHON), str(LEAN / "bin")))
    env["LEAN_PATH"] = os.pathsep.join((str(objects), str(BASE / "authoring/helpers"),
                                       str(LEAN / "lib/lean")))
    commands = []
    for index, module in enumerate(MODULES):
        check()
        argv = [str(LEAN / "bin/lean.exe"), "-DElab.async=false", "-R", str(src),
                "-o", str(objects / (module + ".olean")), str(src / (module + ".lean"))]
        command = {"module": module, "argv": argv, "cwd": str(ROOT)}
        H.fresh_bytes(output / f"{index:02d}-INTENT.json", H.canonical(command))
        print(json.dumps({"event": "COMPILING", "module": module}), flush=True)
        code = subprocess.call(argv, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        command["exit_code"] = code
        H.fresh_bytes(output / f"{index:02d}-RESULT.json", H.canonical(command))
        commands.append(command)
        need(code == 0, "COMPILER_FAILED:" + module)
        check()
    expected_outputs = {module + ext for module in MODULES for ext in PARTS}
    H.census(objects, expected_outputs, check)
    H.census(src, {module + ".lean" for module in MODULES}, check)
    outputs = {name: H.pin(objects / name, check, 64*MIB) for name in sorted(expected_outputs)}
    need(sum(pin["bytes"] for pin in outputs.values()) <= 128*MIB, "OUTPUT_TOTAL")
    for path, expected in inputs.items():
        need(H.pin(Path(path), check) == expected, "FINAL_INPUT_CHANGED")
    for module, expected in source_pins.items():
        need(H.pin(src / (module + ".lean"), check) == expected, "STAGED_SOURCE_CHANGED")
    report = {"status": "FOUR_AUTHORING_HELPERS_COMPILED_NOT_TESTED_OR_INSTALLED",
        "base_profile_sha256": PROFILE, "base_installation_sha256": INSTALLATION,
        "source_pins": source_pins, "compiled_files": outputs, "commands": commands,
        "wall_seconds": time.monotonic() - started, "native_compilations": 4,
        "owner_states_opened": 0, "receiver_compilations": 0,
        "cost_scope": "WHOLE_BUILD_CPU_IS_RECORDED_BY_ENCLOSING_JOB",
        "runtime_scope": "EXPLICIT_SUPPORT_NOT_HERMETIC_TOOLCHAIN"}
    H.fresh_bytes(output / "BUILD.json", H.canonical(report))
    print(json.dumps({"status": report["status"], "compiled_files": len(outputs),
                      "wall_seconds": report["wall_seconds"]}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

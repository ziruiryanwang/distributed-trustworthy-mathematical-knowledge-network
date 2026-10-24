"""Build four new baseline modules using ten exact preserved shared objects.

Only run under the separately selected Run-V5-Check enclosing Job. Its one
original allowance contains this process and every compiler/linker descendant.
No helper rebuild, candidate execution, library replay, owner/catalog operation,
package assembly, retry or mathematical acceptance occurs here. Named runtime
pins are not a hermetic toolchain census. Failure preserves all fresh output.
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
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_baseline/"
BUILDER = "software/v5/ordinary_package/build.py"
BUILDER_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
RUNNER = "tools/Run-V5-Check.py"
BUILD_BASE = LOCAL/"ordinary-current-source-build-01/distribution/_build"
SHARED = BUILD_BASE/"extractor-objects"
SHARED_MANIFEST = BUILD_BASE/"EXTRACTOR-OUTPUTS.json"
SHARED_MANIFEST_SHA = "f55d4c5b56fc299564b76d68c66d63d3090f439b44479b597b016113c4b53768"
RUNTIME_TEMPLATE = LOCAL/"ordinary-current-source-build-01.selection.json"
RUNTIME_TEMPLATE_SHA = "97a4c0d19aea620d067f9cf2a227706fd460654bf06b978cc201a2b7b2e8790b"
RUNTIMES = {"python_runtime": Path(r"D:\Python314"),
            "lean_runtime": ROOT/"software/runtime/lean-4.34.0-windows"}
SHARED_MODULES = ("OriginalExpr", "OriginalDecl", "CheckedExtension",
                  "BootstrapSupport", "OrdinaryExport")
NEW_MODULES = ("BaselineExporter", "BaselineArtifactCore", "BaselineArtifacts", "OrdinaryReferenceBase")
EXECUTABLES = ("BaselineExporter", "BaselineArtifacts", "OrdinaryReferenceBase")
LINK_MODULES = {"BaselineExporter": ("BaselineExporter",),
    "BaselineArtifacts": ("BaselineArtifactCore", "BaselineArtifacts"),
    "OrdinaryReferenceBase": ("BaselineArtifactCore", "OrdinaryReferenceBase")}
SOURCE_FILES = (PREFIX+"build_native.py", PREFIX+"select_native_build.py",
                *(PREFIX+name+".lean" for name in NEW_MODULES), BUILDER, RUNNER)
NAME = "ordinary-baseline-native-build-01"
OUTPUT = LOCAL/NAME/"build"
MIB = 1024**2
SOURCE_MAXIMUM, OBJECT_MAXIMUM = 2*MIB, 32*MIB
GENERATED_MAXIMUM, SPOOL_MAXIMUM = 256*MIB, 384*MIB


def need(ok, code):
    if not ok:
        raise ValueError(code)


def read(path, maximum):
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(0 < len(raw) <= maximum, "BASELINE_BUILD_READ_BOUND")
    return raw


def helper():
    path = ROOT/BUILDER
    raw = read(path, SOURCE_MAXIMUM)
    need(hashlib.sha256(raw).hexdigest() == BUILDER_SHA, "BASELINE_BUILD_BUILDER_PIN")
    spec = importlib.util.spec_from_file_location("_baseline_native_builder", path)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec"), B.__dict__)
    return B


def inspect_inputs(B, check):
    """Only the selected shared objects, named toolchain and current sources."""
    pins = {}

    def keep(path, expected=None, maximum=512*MIB):
        path = B.ordinary(path)
        pin = B.pin(path, check, maximum)
        need(expected is None or pin == expected, "BASELINE_BUILD_INPUT_PIN:"+str(path))
        need(path not in pins or pins[path] == pin, "BASELINE_BUILD_INPUT_CONFLICT")
        pins[path] = pin
        return pin

    def pinned_json(path, expected):
        pin = keep(path, maximum=2*MIB)
        need(pin["sha256"] == expected, "BASELINE_BUILD_MANIFEST_PIN")
        raw = read(path, 2*MIB)
        need({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()} == pin,
             "BASELINE_BUILD_MANIFEST_CHANGED")
        return json.loads(raw)

    manifest = pinned_json(SHARED_MANIFEST, SHARED_MANIFEST_SHA)
    shared = {}
    for name in SHARED_MODULES:
        for suffix in (".olean", ".o"):
            key = name+suffix
            shared[key] = keep(SHARED/key, manifest[key], maximum=128*MIB)
    need(len(shared) == 10, "BASELINE_BUILD_SHARED_CENSUS")
    template = pinned_json(RUNTIME_TEMPLATE, RUNTIME_TEMPLATE_SHA)
    runtime = {}
    for name, digest in template["runtime_pins"].items():
        path = Path(name)
        if any(path.is_relative_to(root) for root in RUNTIMES.values()):
            pin = keep(path)
            need(pin["sha256"] == digest, "BASELINE_BUILD_TOOLCHAIN_PIN")
            runtime[path] = pin
    required = {RUNTIMES["python_runtime"]/"python.exe",
                *(RUNTIMES["lean_runtime"]/"bin"/name for name in
                  ("lean.exe", "leanc.exe", "clang.exe", "ld.lld.exe"))}
    need(required <= set(runtime) and len(runtime) == 23, "BASELINE_BUILD_TOOLCHAIN_CENSUS")
    # These bytes are read when a future selector is explicitly invoked. No
    # mutable draft native hash is embedded in this source-only adapter.
    sources = {name: keep(ROOT/name, maximum=SOURCE_MAXIMUM) for name in SOURCE_FILES}
    need(sources[BUILDER]["sha256"] == BUILDER_SHA and len(pins) <= 64,
         "BASELINE_BUILD_SOURCE_SUPPORT_BOUND")
    return pins, shared, runtime, sources


def build(args):
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "BASELINE_BUILD_CONTEXT")
    need(Path(sys.executable).resolve() == RUNTIMES["python_runtime"]/"python.exe",
         "BASELINE_BUILD_SELECTED_PYTHON")
    started, cpu = time.monotonic(), time.process_time()
    deadline = started+210

    def check():
        need(time.monotonic() < deadline and time.process_time()-cpu < 150,
             "BASELINE_BUILD_ORIGINAL_ALLOWANCE")

    B = helper()
    output = B.ordinary(Path(args.output), directory=True, fresh=True)
    source_root = B.ordinary(Path(args.source_root), directory=True)
    need(output == OUTPUT, "BASELINE_BUILD_SELECTED_OUTPUT")
    for path in (SHARED, source_root, *(ROOT/name for name in SOURCE_FILES), *RUNTIMES.values()):
        need(not output.is_relative_to(path) and not path.is_relative_to(output),
             "BASELINE_BUILD_OUTPUT_OVERLAP")
    input_pins, shared, runtime_pins, sources = inspect_inputs(B, check)
    for name, expected in sources.items():
        need(B.pin(source_root/name, check, SOURCE_MAXIMUM) == expected, "BASELINE_BUILD_SNAPSHOT_PIN")
    need(Path(__file__).resolve() == source_root/PREFIX/"build_native.py" and
         B.pin(Path(__file__).resolve(), check, SOURCE_MAXIMUM) == sources[PREFIX+"build_native.py"],
         "BASELINE_BUILD_RUNNING_SOURCE")
    minimum_spool = (sum(pin["bytes"] for pin in shared.values())+
                     sum(sources[PREFIX+name+".lean"]["bytes"] for name in NEW_MODULES)+
                     GENERATED_MAXIMUM+6*MIB)
    need(minimum_spool <= SPOOL_MAXIMUM, "BASELINE_BUILD_SPOOL_RESERVATION")
    output.mkdir()
    stage_source, shared_copy, objects = output/"source", output/"shared", output/"objects"
    for path in (stage_source, shared_copy, objects):
        path.mkdir()
    completed, phase = [], "STAGING"
    metadata_pins, generated = {}, {}
    expected_objects = set()

    def save(path, value):
        check()
        raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=True, allow_nan=False).encode("ascii")
        need(0 < len(raw) <= 2*MIB, "BASELINE_BUILD_METADATA_BOUND")
        B.fresh_bytes(path, raw)
        pin = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        need(B.pin(path, check, 2*MIB) == pin, "BASELINE_BUILD_METADATA_READBACK")
        return pin

    def copy_exact(source, target, expected):
        check()
        B.ordinary(source); B.ordinary(target, fresh=True)
        count, digest = 0, hashlib.sha256()
        with source.open("rb") as incoming, target.open("xb") as outgoing:
            while block := incoming.read(MIB):
                check(); count += len(block)
                need(count <= expected["bytes"], "BASELINE_BUILD_COPY_GREW")
                digest.update(block); outgoing.write(block)
            outgoing.flush(); os.fsync(outgoing.fileno())
        need({"bytes": count, "sha256": digest.hexdigest()} == expected and
             B.pin(target, check, 128*MIB) == expected and
             B.pin(source, check, 128*MIB) == expected, "BASELINE_BUILD_COPY_PIN")

    def census(directory, expected, maximum, total_maximum):
        check()
        seen, total = set(), 0
        with os.scandir(directory) as listing:
            for item in listing:
                check()
                need(len(seen) < len(expected) and item.name in expected,
                     "BASELINE_BUILD_UNEXPECTED_OUTPUT:"+str(directory))
                path = B.ordinary(Path(item.path))
                size = path.stat().st_size
                need(0 < size <= maximum, "BASELINE_BUILD_OUTPUT_FILE_BOUND")
                seen.add(item.name); total += size
                need(total <= total_maximum, "BASELINE_BUILD_OUTPUT_TOTAL_BOUND")
        need(seen == set(expected), "BASELINE_BUILD_MISSING_OUTPUT")
        return total

    try:
        need(sum(pin["bytes"] for pin in shared.values()) <= 128*MIB,
             "BASELINE_BUILD_SHARED_TOTAL_BOUND")
        for name, expected in shared.items():
            copy_exact(SHARED/name, shared_copy/name, expected)
        for name in NEW_MODULES:
            relative = PREFIX+name+".lean"
            copy_exact(source_root/relative, stage_source/(name+".lean"), sources[relative])
        metadata_pins["INPUTS.json"] = save(output/"INPUTS.json", {
            "schema": "DMKN_ORDINARY_BASELINE_NATIVE_BUILD_INPUTS_V1",
            "files": {str(path): pin for path, pin in input_pins.items()},
            "source_snapshots": {name: {"path": str(source_root/name), **pin}
                                 for name, pin in sources.items()},
            "shared_manifest_sha256": SHARED_MANIFEST_SHA,
            "runtime_template_sha256": RUNTIME_TEMPLATE_SHA,
            "shared_objects": shared, "modules_to_compile": list(NEW_MODULES),
            "executables_to_link": list(EXECUTABLES),
            "minimum_spool_authorization_bytes": minimum_spool,
            "spool_maximum_bytes": SPOOL_MAXIMUM,
            "runtime_scope": "23_EXPLICIT_NAMED_PINS_NOT_HERMETIC_TOOLCHAIN"})
        runtime = RUNTIMES["lean_runtime"]
        env = {key: value for key, value in os.environ.items()
               if not key.upper().startswith(("LEAN", "PYTHON", "RUST", "CARGO", "RISC0", "NODE"))
               and key.upper() not in ("PATH", "VIRTUAL_ENV")}
        env["PATH"] = str(runtime/"bin")
        env["LEAN_PATH"] = os.pathsep.join((str(objects), str(shared_copy)))

        def run(label, argv, new_outputs):
            nonlocal phase
            check()
            phase = label
            need(sum(len(value)+3 for value in argv) <= 30000, "BASELINE_BUILD_COMMAND_BOUND")
            before = time.monotonic()
            # Every timeout uses the original controller deadline. Descendants
            # inherit the one enclosing Job; this is not a new supervision grant.
            result = subprocess.run(argv, cwd=output, env=env, stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW, timeout=max(0.001, deadline-before))
            row = {"phase": label, "argv": argv, "exit_code": result.returncode,
                   "wall_seconds": time.monotonic()-before}
            completed.append(row)
            print(json.dumps(row, sort_keys=True), flush=True)
            need(result.returncode == 0, "BASELINE_BUILD_COMMAND_FAILED:"+label)
            expected_objects.update(new_outputs)
            census(objects, expected_objects, OBJECT_MAXIMUM, GENERATED_MAXIMUM)
            check()

        for name in NEW_MODULES:
            run(name+"-codegen", [str(runtime/"bin/lean.exe"), "-DElab.async=false",
                "-R", str(stage_source), "-o", str(objects/(name+".olean")),
                "-c", str(objects/(name+".c")), str(stage_source/(name+".lean"))],
                (name+".olean", name+".c"))
            run(name+"-object", [str(runtime/"bin/leanc.exe"), "-c", "-O0",
                str(objects/(name+".c")), "-o", str(objects/(name+".o"))], (name+".o",))
        for name in EXECUTABLES:
            run(name+"-link", [str(runtime/"bin/leanc.exe"), "-leanshared",
                *(str(shared_copy/(shared_name+".o")) for shared_name in SHARED_MODULES),
                *(str(objects/(module+".o")) for module in LINK_MODULES[name]),
                "-o", str(objects/(name+".exe"))], (name+".exe",))
        need(len(completed) == 11 and len(expected_objects) == 15, "BASELINE_BUILD_EXACT_COMMAND_CENSUS")
        generated = {name: B.pin(objects/name, check, OBJECT_MAXIMUM) for name in sorted(expected_objects)}
        metadata_pins["NATIVE-OUTPUTS.json"] = save(output/"NATIVE-OUTPUTS.json", generated)
        phase = "FINAL_REHASH"
        for path, expected in input_pins.items():
            need(B.pin(path, check, 512*MIB) == expected, "BASELINE_BUILD_FINAL_ORIGINAL_INPUT")
        for name, expected in sources.items():
            need(B.pin(source_root/name, check, SOURCE_MAXIMUM) == expected, "BASELINE_BUILD_FINAL_SNAPSHOT")
        for name, expected in shared.items():
            need(B.pin(shared_copy/name, check, 128*MIB) == expected, "BASELINE_BUILD_FINAL_SHARED_COPY")
        for name in NEW_MODULES:
            need(B.pin(stage_source/(name+".lean"), check, SOURCE_MAXIMUM) == sources[PREFIX+name+".lean"],
                 "BASELINE_BUILD_FINAL_NATIVE_SOURCE")
        for name, expected in generated.items():
            need(B.pin(objects/name, check, OBJECT_MAXIMUM) == expected, "BASELINE_BUILD_FINAL_GENERATED")
        for name, expected in metadata_pins.items():
            need(B.pin(output/name, check, 2*MIB) == expected, "BASELINE_BUILD_FINAL_METADATA")
        source_bytes = census(stage_source, {name+".lean" for name in NEW_MODULES}, SOURCE_MAXIMUM, 8*MIB)
        shared_bytes = census(shared_copy, shared, 128*MIB, 128*MIB)
        generated_bytes = census(objects, generated, OBJECT_MAXIMUM, GENERATED_MAXIMUM)
        total = source_bytes+shared_bytes+generated_bytes+sum(pin["bytes"] for pin in metadata_pins.values())
        need(total+2*MIB <= SPOOL_MAXIMUM, "BASELINE_BUILD_FINAL_SPOOL_BOUND")
        need({path.name for path in output.iterdir()} ==
             {"source", "shared", "objects", "INPUTS.json", "NATIVE-OUTPUTS.json"},
             "BASELINE_BUILD_TOP_LEVEL_CENSUS")
        receipt = {"schema": "DMKN_ORDINARY_BASELINE_NATIVE_BUILD_V1",
            "status": "BUILT_CANDIDATES_NOT_INSTALLED_OR_ADOPTED", "mathematical_acceptance": False,
            "source_files": sources, "shared_manifest_sha256": SHARED_MANIFEST_SHA,
            "runtime_template_sha256": RUNTIME_TEMPLATE_SHA, "runtime_pin_count": len(runtime_pins),
            "shared_objects": shared, "generated_outputs": generated,
            "executable_links": {name+".exe": [*(key+".o" for key in SHARED_MODULES),
                *(key+".o" for key in LINK_MODULES[name])] for name in EXECUTABLES},
            "metadata": metadata_pins, "completed_commands": completed,
            "spool_bytes_before_build_receipt": total, "spool_maximum_bytes": SPOOL_MAXIMUM,
            "wall_seconds_before_build_receipt": time.monotonic()-started,
            "controller_cpu_seconds_before_build_receipt": time.process_time()-cpu,
            "inclusive_cpu_and_closure": "ONLY_ENCLOSING_JOB_RESULT",
            "bounds": "COOPERATIVE_FILE_CENSUS_NOT_HARD_DISK_QUOTA",
            "next_step": "SEPARATE_REVIEW_AND_SELECTION_NO_AUTOMATIC_EXECUTABLE_RUN"}
        phase = "BUILD_RECEIPT"
        save(output/"BUILD.json", receipt)
        check()
        return receipt
    except BaseException as error:
        try:
            # Best-effort diagnostic after failure does not claim child closure
            # or delete any partial compiler output. Only the outer Job does so.
            raw = json.dumps({"schema": "DMKN_ORDINARY_BASELINE_NATIVE_BUILD_FAILURE_V1",
                "phase": phase, "error_type": type(error).__name__, "error": str(error)[:2048],
                "completed_commands": completed, "wall_seconds": time.monotonic()-started,
                "controller_cpu_seconds": time.process_time()-cpu,
                "inclusive_cpu_and_closure": "ONLY_ENCLOSING_JOB_RESULT",
                "retention": "ALL_PARTIAL_FILES_PRESERVED_NO_RETRY",
                "build_receipt_may_exist": phase == "BUILD_RECEIPT",
                "mathematical_acceptance": False}, sort_keys=True, allow_nan=False).encode("ascii")
            need(len(raw) <= 2*MIB, "BASELINE_BUILD_FAILURE_BOUND")
            B.fresh_bytes(output/"BUILD-FAILURE.json", raw)
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output", required=True)
    result = build(parser.parse_args())
    print(json.dumps({"status": result["status"], "completed_commands": len(result["completed_commands"]),
                      "generated_outputs": len(result["generated_outputs"])}, sort_keys=True), flush=True)

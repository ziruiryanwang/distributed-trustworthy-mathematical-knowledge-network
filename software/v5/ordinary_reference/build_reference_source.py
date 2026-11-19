"""Two compile-only qualifications using retained exact helper artifacts.

No helper rebuild or recopy, code generation/linking, source authoring, native
main, library import, snapshot copy, owner mutation or mathematical acceptance.
ReferenceEnvironment is a no-main parser derivative; ReferenceSource imports it.
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
PREFIX = "software/v5/ordinary_reference/"
NAME = "ordinary-reference-source-build-01"
MODULES = ("ReferenceEnvironment", "ReferenceSource")
OLD = LOCAL/"ordinary-reference-module-build-01"
SUPPORT = OLD/"build/support"
BUILDER = "software/v5/ordinary_package/build.py"
BUILDER_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
SOURCE_FILES = (PREFIX+"build_reference_source.py", PREFIX+"select_reference_source_build.py",
                PREFIX+"ReferenceEnvironment.lean", PREFIX+"ReferenceSource.lean",
                PREFIX+"ReferenceModule.lean", PREFIX+"reference_author_worker.py",
                BUILDER, "tools/Run-V5-Check.py")
PROVENANCE = {
    "build/BUILD.json": "dd51cef62552b523f9e5b5bbade9cb978c8816d0361a8a4d28162d9193362a0c",
    "RESULT.json": "d7075a3ba48e82330075a593ca4f85615f39277fc959d345cf3df74471c16071",
    "selection.json": "18dc8fb7f82a9b6162aaa363fdf41aa686d2dbc5ffc0b5d5bf5bb10e0ab5fdff",
}
MIB = 1024**2
INNER_SPOOL = 64*MIB


def need(ok, code):
    if not ok:
        raise ValueError(code)


def read(path):
    with path.open("rb") as handle:
        raw = handle.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB, "REFERENCE_SOURCE_BUILD_READ_BOUND")
    return raw


def helper():
    path = ROOT/BUILDER
    raw = read(path)
    need(hashlib.sha256(raw).hexdigest() == BUILDER_SHA, "REFERENCE_SOURCE_BUILD_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_reference_source_builder", path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def inspect_inputs(B, check):
    pins, docs = {}, {}

    def keep(path, expected=None, maximum=512*MIB):
        value = B.pin(B.ordinary(path), check, maximum)
        need(expected is None or value == expected or value["sha256"] == expected,
             "REFERENCE_SOURCE_BUILD_PIN:"+str(path))
        need(str(path) not in pins or pins[str(path)] == value, "REFERENCE_SOURCE_BUILD_PIN_CONFLICT")
        pins[str(path)] = value
        return value

    for relative, digest in PROVENANCE.items():
        path = OLD/relative
        expected = keep(path, digest, 2*MIB)
        raw = read(path)
        need({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()} == expected,
             "REFERENCE_SOURCE_BUILD_METADATA_CHANGED")
        docs[relative] = json.loads(raw)
    result, selected, old = docs["RESULT.json"], docs["selection.json"], docs["build/BUILD.json"]
    event = result["result"]
    need(result["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1" and
         result["selection_sha256"] == PROVENANCE["selection.json"] and selected["name"] == OLD.name and
         event["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and event["child_exit_code"] == 0 and
         event["direct_child_reaped"] is True and event["job_closed"] is True and
         event["cleanup_errors"] == [] and event["termination_requested"] is False and
         event["final_job"]["active_processes"] == event["final_job"]["terminated_processes"] == 0,
         "REFERENCE_SOURCE_BUILD_PREDECESSOR_CLOSURE")
    need(old["schema"] == "DMKN_ORDINARY_REFERENCE_MODULE_BUILD_V1" and
         old["status"] == "COMPILED_CANDIDATE_NOT_INSTALLED_OR_EXECUTED" and
         len(old["completed_commands"]) == 1 and old["completed_commands"][0]["exit_code"] == 0 and
         set(old["metadata"]) == {"INPUTS.json", "NATIVE-OUTPUTS.json"},
         "REFERENCE_SOURCE_BUILD_PREDECESSOR_RECEIPT")
    for filename, expected in old["metadata"].items():
        keep(OLD/"build"/filename, expected, 2*MIB)
    need(json.loads(read(OLD/"build/NATIVE-OUTPUTS.json")) == old["generated_outputs"],
         "REFERENCE_SOURCE_BUILD_PREDECESSOR_OUTPUT_MAP")
    expected_names = {name+".olean" for name in
        ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport", "OrdinaryExport",
         "BaselineArtifactCore04")}
    expected_names.update("OwnerRebind"+suffix for suffix in
        (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir"))
    need(set(old["reused_support"]) == expected_names and
         {path.name for path in B.ordinary(SUPPORT, directory=True).iterdir()} == expected_names,
         "REFERENCE_SOURCE_BUILD_RETAINED_SUPPORT_CENSUS")
    reused = {}
    for filename in sorted(expected_names):
        value = old["reused_support"][filename]
        expected = {key: value[key] for key in ("bytes", "sha256")}
        path = SUPPORT/filename
        reused[filename] = {"path": str(path), **keep(path, expected, 32*MIB)}
    runtime = {}
    for filename, digest in selected["runtime_pins"].items():
        path = Path(filename)
        if path.is_relative_to(PYTHON) or path.is_relative_to(LEAN):
            runtime[filename] = keep(path, digest)
    need(len(runtime) == 23 and str(PYTHON/"python.exe") in runtime and
         str(LEAN/"bin/lean.exe") in runtime, "REFERENCE_SOURCE_BUILD_RUNTIME_CENSUS")
    sources = {relative: keep(ROOT/relative, maximum=2*MIB) for relative in SOURCE_FILES}
    need(sources[PREFIX+"ReferenceModule.lean"] == old["source_files"][PREFIX+"ReferenceModule.lean"] and
         sources[BUILDER]["sha256"] == BUILDER_SHA and len(pins) <= 64,
         "REFERENCE_SOURCE_BUILD_SOURCE_CENSUS")
    return pins, reused, runtime, sources


def main(args):
    started, cpu = time.monotonic(), time.process_time()
    deadline = started+135

    def check():
        need(time.monotonic() < deadline and time.process_time()-cpu < 75,
             "REFERENCE_SOURCE_BUILD_ORIGINAL_ALLOWANCE")

    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON/"python.exe", "REFERENCE_SOURCE_BUILD_CONTEXT")
    B = helper()
    source_root = B.ordinary(Path(args.source_root), directory=True)
    output = B.ordinary(Path(args.output), directory=True, fresh=True)
    need(output == LOCAL/NAME/"build" and Path(__file__).resolve() ==
         source_root/PREFIX/"build_reference_source.py", "REFERENCE_SOURCE_BUILD_LOCATION")
    inputs, reused, runtime, sources = inspect_inputs(B, check)
    for relative, expected in sources.items():
        need(B.pin(source_root/relative, check, 2*MIB) == expected, "REFERENCE_SOURCE_BUILD_SNAPSHOT")
    output.mkdir()
    stage, objects = output/"source", output/"objects"
    stage.mkdir(); objects.mkdir()
    completed, metadata, generated = [], {}, {}
    phase = "STAGING"

    def save(path, value):
        check()
        raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
        need(0 < len(raw) <= 2*MIB, "REFERENCE_SOURCE_BUILD_METADATA_BOUND")
        B.fresh_bytes(path, raw)
        expected = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        need(B.pin(path, check, 2*MIB) == expected, "REFERENCE_SOURCE_BUILD_READBACK")
        return expected

    def census(directory, expected, maximum):
        need({p.name for p in directory.iterdir()} == set(expected), "REFERENCE_SOURCE_BUILD_FILE_CENSUS")
        total = 0
        for filename, value in expected.items():
            need(B.pin(B.ordinary(directory/filename), check, maximum) == value,
                 "REFERENCE_SOURCE_BUILD_FINAL_FILE")
            total += value["bytes"]
        return total

    try:
        for name in MODULES:
            relative = PREFIX+name+".lean"
            raw = read(source_root/relative)
            need({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()} == sources[relative],
                 "REFERENCE_SOURCE_BUILD_STAGE_PIN")
            B.fresh_bytes(stage/(name+".lean"), raw)
        metadata["INPUTS.json"] = save(output/"INPUTS.json", {"inputs": inputs, "reused_support": reused,
            "source_snapshots": {relative: {"path": str(source_root/relative), **value}
                                 for relative, value in sources.items()},
            "support_provenance": PROVENANCE,
            "purpose": "TWO_COMPILE_COMMANDS_NO_NATIVE_MAIN_OR_LIBRARY_OPERATION"})
        env = {key: value for key, value in os.environ.items() if not key.upper().startswith(
            ("LEAN", "PYTHON", "RUST", "CARGO", "RISC0", "NODE")) and key.upper() not in ("PATH", "VIRTUAL_ENV")}
        env["PATH"] = str(LEAN/"bin")
        env["LEAN_PATH"] = os.pathsep.join((str(objects), str(SUPPORT)))
        for name in MODULES:
            argv = [str(LEAN/"bin/lean.exe"), "-DElab.async=false", "-R", str(stage),
                    "-o", str(objects/(name+".olean")), str(stage/(name+".lean"))]
            need(sum(len(value)+3 for value in argv) <= 30000, "REFERENCE_SOURCE_BUILD_ARGV_BOUND")
            phase = name+"-compile"
            check(); before = time.monotonic()
            result = subprocess.run(argv, cwd=output, env=env, stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW, timeout=max(0.001, deadline-before))
            completed.append({"phase": phase, "argv": argv, "exit_code": result.returncode,
                              "wall_seconds": time.monotonic()-before})
            print(json.dumps(completed[-1], sort_keys=True), flush=True)
            need(result.returncode == 0, "REFERENCE_SOURCE_BUILD_COMPILE_FAILED")
            generated[name+".olean"] = B.pin(B.ordinary(objects/(name+".olean")), check, 16*MIB)
        metadata["NATIVE-OUTPUTS.json"] = save(output/"NATIVE-OUTPUTS.json", generated)
        phase = "FINAL_REHASH"
        for filename, expected in inputs.items():
            need(B.pin(Path(filename), check, 512*MIB) == expected, "REFERENCE_SOURCE_BUILD_FINAL_INPUT")
        for relative, expected in sources.items():
            need(B.pin(source_root/relative, check, 2*MIB) == expected, "REFERENCE_SOURCE_BUILD_FINAL_SNAPSHOT")
        total = census(objects, generated, 16*MIB)
        total += census(stage, {name+".lean": sources[PREFIX+name+".lean"] for name in MODULES}, 2*MIB)
        # Reused support is not part of the fresh spool, but its census remains exact.
        census(SUPPORT, {name: {key: row[key] for key in ("bytes", "sha256")}
                         for name, row in reused.items()}, 32*MIB)
        for filename, expected in metadata.items():
            need(B.pin(output/filename, check, 2*MIB) == expected, "REFERENCE_SOURCE_BUILD_FINAL_METADATA")
            total += expected["bytes"]
        need(total+2*MIB <= INNER_SPOOL and {p.name for p in output.iterdir()} ==
             {"source", "objects", "INPUTS.json", "NATIVE-OUTPUTS.json"}, "REFERENCE_SOURCE_BUILD_FINAL_CENSUS")
        receipt = {"schema": "DMKN_ORDINARY_REFERENCE_SOURCE_BUILD_V1",
            "status": "COMPILED_CANDIDATES_NOT_INSTALLED_OR_EXECUTED", "mathematical_acceptance": False,
            "inputs": inputs, "source_files": sources, "reused_support": reused,
            "generated_outputs": generated, "metadata": metadata, "completed_commands": completed,
            "runtime_pin_count": len(runtime), "support_provenance": PROVENANCE,
            "fresh_inner_spool_maximum_bytes": INNER_SPOOL, "spool_before_receipt": total,
            "bounds": "COOPERATIVE_FILE_CENSUS_NOT_HARD_DISK_QUOTA",
            "wall_seconds": time.monotonic()-started, "controller_cpu_seconds": time.process_time()-cpu,
            "inclusive_cpu_and_closure": "ONLY_ENCLOSING_JOB_RESULT",
            "next_step": "SEPARATE_OWNER_INTEGRATION_SELECTION_NO_AUTOMATIC_EXECUTION"}
        phase = "BUILD_RECEIPT"
        save(output/"BUILD.json", receipt); check()
        print(json.dumps({"status": receipt["status"], "commands": len(completed)}), flush=True)
    except BaseException as error:
        try:
            B.fresh_bytes(output/"BUILD-FAILURE.json", json.dumps({"phase": phase,
                "error_type": type(error).__name__, "error": str(error)[:2048],
                "completed_commands": completed, "mathematical_acceptance": False,
                "retention": "PRESERVE_ALL_NO_RETRY", "wall_seconds": time.monotonic()-started,
                "controller_cpu_seconds": time.process_time()-cpu,
                "inclusive_cpu_and_closure": "ONLY_ENCLOSING_JOB_RESULT"}, sort_keys=True).encode("ascii"))
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output", required=True)
    main(parser.parse_args())

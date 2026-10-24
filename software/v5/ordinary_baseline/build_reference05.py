"""Build one selected reference matcher from retained core04 support; never run it.

Exactly three compiler/linker commands under the root-selected enclosing Job.
No artifact collection, library snapshot, owner operation or acceptance.
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
NAME = "ordinary-reference-native-build-05"
OLD = LOCAL/"ordinary-baseline-native-build-04"
MATCHER = "OrdinaryReferenceBase05"
CORE = "BaselineArtifactCore04"
SHARED = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport", "OrdinaryExport")
BUILDER = "software/v5/ordinary_package/build.py"
BUILDER_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
SOURCE_FILES = (PREFIX+"build_reference05.py", PREFIX+"select_reference05_build.py",
                PREFIX+MATCHER+".lean", BUILDER, "tools/Run-V5-Check.py")
PROVENANCE = {
    "build/BUILD.json": "5811c38b872b094c284579241d9c90d463432ac35dc96d0ae6008b5b7df76213",
    "RESULT.json": "f997200b7abb83d13a0682261858b576d9938031c0368292bc5b5ec2b17632ec",
    "selection.json": "0de88c987ff006d5f7a070996c3d01f7aa34cd7d6f880e180c3e51e47d213ac4",
}
MIB = 1024**2
INNER_SPOOL, GENERATED = 104*MIB, 64*MIB


def need(ok, code):
    if not ok:
        raise ValueError(code)


def read(path):
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB, "REFERENCE_MATCHER_BUILD_READ_BOUND")
    return raw


def helper():
    path = ROOT/BUILDER
    raw = read(path)
    need(hashlib.sha256(raw).hexdigest() == BUILDER_SHA, "REFERENCE_MATCHER_BUILD_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_reference_matcher_builder", path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def inspect_inputs(B, check):
    pins = {}

    def keep(path, expected=None, maximum=512*MIB):
        value = B.pin(B.ordinary(path), check, maximum)
        need(expected is None or value == expected or value["sha256"] == expected,
             "REFERENCE_MATCHER_BUILD_INPUT_PIN:"+str(path))
        need(str(path) not in pins or pins[str(path)] == value, "REFERENCE_MATCHER_BUILD_PIN_CONFLICT")
        pins[str(path)] = value
        return value

    previous = {}
    for relative, digest in PROVENANCE.items():
        path = OLD/relative
        expected = keep(path, digest, 2*MIB)
        raw = read(path)
        need({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()} == expected,
             "REFERENCE_MATCHER_BUILD_PROVENANCE_CHANGED")
        previous[relative] = json.loads(raw)
    build, result, selected = previous["build/BUILD.json"], previous["RESULT.json"], previous["selection.json"]
    event = result["result"]
    need(result["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1" and
         result["selection_sha256"] == PROVENANCE["selection.json"] and
         event["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and event["child_exit_code"] == 0 and
         event["direct_child_reaped"] is True and event["job_closed"] is True and
         event["cleanup_errors"] == [] and event["termination_requested"] is False and
         event["final_job"]["active_processes"] == event["final_job"]["terminated_processes"] == 0 and
         selected["name"] == OLD.name and build["status"] == "BUILT_CANDIDATES_NOT_INSTALLED_OR_ADOPTED" and
         len(build["completed_commands"]) == 9 and all(row["exit_code"] == 0 for row in build["completed_commands"]),
         "REFERENCE_MATCHER_BUILD_PREDECESSOR")
    for filename, expected in build["metadata"].items():
        need(filename in ("INPUTS.json", "NATIVE-OUTPUTS.json"), "REFERENCE_MATCHER_BUILD_METADATA")
        keep(OLD/"build"/filename, expected, 2*MIB)
    outputs = json.loads(read(OLD/"build/NATIVE-OUTPUTS.json"))
    need(outputs == build["all_candidate_outputs"], "REFERENCE_MATCHER_BUILD_OUTPUT_MAP")
    reused = {}
    for name in (*SHARED, CORE):
        for suffix in (".olean", ".o"):
            filename = name+suffix
            path = OLD/"build"/("objects" if name == CORE else "shared")/filename
            expected = outputs[filename] if name == CORE else build["shared_objects"][filename]
            reused[filename] = {"path": str(path), **keep(path, expected, 32*MIB)}
    core_source = PREFIX+CORE+".lean"
    core_pin = build["source_files"][core_source]
    need(selected["sources"][core_source] == core_pin["sha256"], "REFERENCE_MATCHER_BUILD_CORE_SOURCE")
    keep(ROOT/core_source, core_pin, 2*MIB)
    keep(OLD/"sources"/core_source, core_pin, 2*MIB)
    runtime = {}
    for filename, digest in selected["runtime_pins"].items():
        path = Path(filename)
        if path.is_relative_to(PYTHON) or path.is_relative_to(LEAN):
            runtime[filename] = keep(path, digest)
    required = {str(PYTHON/"python.exe"), *(str(LEAN/"bin"/name) for name in
                 ("lean.exe", "leanc.exe", "clang.exe", "ld.lld.exe"))}
    need(len(runtime) == 23 and required <= runtime.keys(), "REFERENCE_MATCHER_BUILD_RUNTIME_CENSUS")
    sources = {name: keep(ROOT/name, maximum=2*MIB) for name in SOURCE_FILES}
    need(sources[BUILDER]["sha256"] == BUILDER_SHA and len(reused) == 12 and len(pins) <= 64,
         "REFERENCE_MATCHER_BUILD_INPUT_CENSUS")
    return pins, reused, runtime, sources


def main(args):
    started, cpu = time.monotonic(), time.process_time()
    deadline = started+105

    def check():
        need(time.monotonic() < deadline and time.process_time()-cpu < 50,
             "REFERENCE_MATCHER_BUILD_ORIGINAL_ALLOWANCE")

    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON/"python.exe", "REFERENCE_MATCHER_BUILD_CONTEXT")
    B = helper()
    source_root = B.ordinary(Path(args.source_root), directory=True)
    output = B.ordinary(Path(args.output), directory=True, fresh=True)
    need(output == LOCAL/NAME/"build" and Path(__file__).resolve() ==
         source_root/PREFIX/"build_reference05.py", "REFERENCE_MATCHER_BUILD_LOCATION")
    inputs, reused, runtime, sources = inspect_inputs(B, check)
    for name, expected in sources.items():
        need(B.pin(source_root/name, check, 2*MIB) == expected, "REFERENCE_MATCHER_BUILD_SNAPSHOT")
    reservation = sum(row["bytes"] for row in reused.values())+GENERATED+2*MIB+6*MIB
    need(reservation <= INNER_SPOOL, "REFERENCE_MATCHER_BUILD_SPOOL_RESERVATION")
    output.mkdir()
    stage, support, objects = output/"source", output/"support", output/"objects"
    for path in (stage, support, objects):
        path.mkdir()
    completed, metadata, generated = [], {}, {}
    phase = "STAGING"

    def save(path, value):
        check()
        raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
        need(0 < len(raw) <= 2*MIB, "REFERENCE_MATCHER_BUILD_METADATA_BOUND")
        B.fresh_bytes(path, raw)
        expected = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        need(B.pin(path, check, 2*MIB) == expected, "REFERENCE_MATCHER_BUILD_METADATA_READBACK")
        return expected

    def copy_exact(source, destination, expected):
        check(); B.ordinary(source); B.ordinary(destination, fresh=True)
        count, digest = 0, hashlib.sha256()
        with source.open("rb") as incoming, destination.open("xb") as outgoing:
            while block := incoming.read(MIB):
                check(); count += len(block)
                need(count <= expected["bytes"], "REFERENCE_MATCHER_BUILD_COPY_GREW")
                digest.update(block); outgoing.write(block)
            outgoing.flush(); os.fsync(outgoing.fileno())
        need({"bytes": count, "sha256": digest.hexdigest()} == expected and
             B.pin(source, check, 32*MIB) == expected and B.pin(destination, check, 32*MIB) == expected,
             "REFERENCE_MATCHER_BUILD_COPY_PIN")

    def census(path, names, maximum, aggregate):
        total, seen = 0, set()
        for item in path.iterdir():
            check()
            need(item.name in names and item.name not in seen, "REFERENCE_MATCHER_BUILD_EXTRA_FILE")
            B.ordinary(item)
            size = item.stat().st_size
            need(0 < size <= maximum, "REFERENCE_MATCHER_BUILD_FILE_BOUND")
            total += size; seen.add(item.name)
            need(total <= aggregate, "REFERENCE_MATCHER_BUILD_TOTAL_BOUND")
        need(seen == set(names), "REFERENCE_MATCHER_BUILD_MISSING_FILE")
        return total

    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON", "RUST", "CARGO", "RISC0", "NODE"))
           and key.upper() not in ("PATH", "VIRTUAL_ENV")}
    env["PATH"], env["LEAN_PATH"] = str(LEAN/"bin"), str(support)
    expected_outputs = set()

    def run(label, argv, new_outputs):
        nonlocal phase
        check(); phase = label
        need(len(completed) < 3 and sum(len(value)+3 for value in argv) <= 30000,
             "REFERENCE_MATCHER_BUILD_COMMAND_BOUND")
        before = time.monotonic()
        result = subprocess.run(argv, cwd=output, env=env, stdin=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW, timeout=max(0.001, deadline-before))
        completed.append({"phase": label, "argv": argv, "exit_code": result.returncode,
                          "wall_seconds": time.monotonic()-before})
        print(json.dumps(completed[-1], sort_keys=True), flush=True)
        need(result.returncode == 0, "REFERENCE_MATCHER_BUILD_COMMAND_FAILED:"+label)
        expected_outputs.update(new_outputs)
        census(objects, expected_outputs, 16*MIB, GENERATED)

    try:
        for name, row in reused.items():
            copy_exact(Path(row["path"]), support/name, {key: row[key] for key in ("bytes", "sha256")})
        source_relative = PREFIX+MATCHER+".lean"
        copy_exact(source_root/source_relative, stage/(MATCHER+".lean"), sources[source_relative])
        metadata["INPUTS.json"] = save(output/"INPUTS.json", {"inputs": inputs,
            "source_snapshots": {name: {"path": str(source_root/name), **value} for name, value in sources.items()},
            "reused_support": reused, "prior_build_provenance": PROVENANCE,
            "purpose": "CONDITIONAL_REFERENCE_CORRESPONDENCE_NOT_ACCEPTANCE",
            "minimum_spool_reservation_bytes": reservation, "fresh_inner_spool_maximum_bytes": INNER_SPOOL})
        run("reference-codegen", [str(LEAN/"bin/lean.exe"), "-DElab.async=false", "-R", str(stage),
            "-o", str(objects/(MATCHER+".olean")), "-c", str(objects/(MATCHER+".c")),
            str(stage/(MATCHER+".lean"))], (MATCHER+".olean", MATCHER+".c"))
        run("reference-object", [str(LEAN/"bin/leanc.exe"), "-c", "-O0", str(objects/(MATCHER+".c")),
            "-o", str(objects/(MATCHER+".o"))], (MATCHER+".o",))
        run("reference-link", [str(LEAN/"bin/leanc.exe"), "-leanshared",
            *(str(support/(name+".o")) for name in (*SHARED, CORE)),
            str(objects/(MATCHER+".o")), "-o", str(objects/(MATCHER+".exe"))], (MATCHER+".exe",))
        need(len(completed) == 3 and len(expected_outputs) == 4, "REFERENCE_MATCHER_BUILD_EXACT_SCOPE")
        generated = {name: B.pin(objects/name, check, 16*MIB) for name in sorted(expected_outputs)}
        metadata["NATIVE-OUTPUTS.json"] = save(output/"NATIVE-OUTPUTS.json", generated)
        phase = "FINAL_REHASH"
        for path, expected in inputs.items():
            need(B.pin(Path(path), check, 512*MIB) == expected, "REFERENCE_MATCHER_BUILD_FINAL_INPUT")
        for name, expected in sources.items():
            need(B.pin(source_root/name, check, 2*MIB) == expected, "REFERENCE_MATCHER_BUILD_FINAL_SNAPSHOT")
        for name, row in reused.items():
            need(B.pin(support/name, check, 32*MIB) == {key: row[key] for key in ("bytes", "sha256")},
                 "REFERENCE_MATCHER_BUILD_FINAL_SUPPORT")
        need(B.pin(stage/(MATCHER+".lean"), check, 2*MIB) == sources[source_relative],
             "REFERENCE_MATCHER_BUILD_FINAL_SOURCE")
        for name, expected in generated.items():
            need(B.pin(objects/name, check, 16*MIB) == expected, "REFERENCE_MATCHER_BUILD_FINAL_GENERATED")
        for name, expected in metadata.items():
            need(B.pin(output/name, check, 2*MIB) == expected, "REFERENCE_MATCHER_BUILD_FINAL_METADATA")
        total = census(support, reused, 32*MIB, INNER_SPOOL)+census(objects, generated, 16*MIB, GENERATED)
        total += census(stage, {MATCHER+".lean"}, 2*MIB, 2*MIB)+sum(value["bytes"] for value in metadata.values())
        need(total+2*MIB <= INNER_SPOOL and {path.name for path in output.iterdir()} ==
             {"source", "support", "objects", "INPUTS.json", "NATIVE-OUTPUTS.json"},
             "REFERENCE_MATCHER_BUILD_FINAL_CENSUS")
        receipt = {"schema": "DMKN_ORDINARY_REFERENCE_NATIVE_BUILD_V1",
            "status": "BUILT_CANDIDATE_NOT_INSTALLED_OR_ADOPTED", "mathematical_acceptance": False,
            "purpose": "CONDITIONAL_REFERENCE_CORRESPONDENCE_NOT_ACCEPTANCE",
            "source": {"path": str(ROOT/source_relative), **sources[source_relative]},
            "executable": {"path": str(objects/(MATCHER+".exe")), **generated[MATCHER+".exe"]},
            "inputs": inputs, "source_files": sources, "reused_support": reused,
            "generated_outputs": generated, "metadata": metadata, "completed_commands": completed,
            "runtime_pin_count": len(runtime), "prior_build_provenance": PROVENANCE,
            "fresh_inner_spool_maximum_bytes": INNER_SPOOL, "spool_before_receipt": total,
            "bounds": "COOPERATIVE_FILE_CENSUS_NOT_HARD_DISK_QUOTA",
            "wall_seconds": time.monotonic()-started, "controller_cpu_seconds": time.process_time()-cpu,
            "inclusive_cpu_and_closure": "ONLY_ENCLOSING_JOB_RESULT",
            "next_step": "SEPARATE_CORRESPONDENCE_SELECTION_NO_AUTOMATIC_EXECUTION"}
        phase = "BUILD_RECEIPT"
        save(output/"BUILD.json", receipt); check()
        print(json.dumps({"status": receipt["status"], "purpose": receipt["purpose"]}), flush=True)
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

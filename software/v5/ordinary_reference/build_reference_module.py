"""One selected ReferenceModule .olean qualification command; never run main.

Reuse six exact legacy oleans and the five parts of modern OwnerRebind. No
helper codegen, linking, fixture compilation, snapshot, owner or registration.
The resulting .olean is compiler evidence, not an installed executable product.
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
BASE_PREFIX = "software/v5/ordinary_baseline/"
NAME = "ordinary-reference-module-build-01"
MODULE = "ReferenceModule"
CORE = "BaselineArtifactCore04"
SHARED = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport", "OrdinaryExport")
OLD = LOCAL/"ordinary-baseline-native-build-04"
PACKAGE_BUILD = LOCAL/"ordinary-current-source-build-01"
PACKAGE = PACKAGE_BUILD/"distribution/package"
BUILDER = "software/v5/ordinary_package/build.py"
BUILDER_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
OWNER_SOURCE = "software/v5/ordinary_lean/OwnerRebind.lean"
OWNER_SOURCE_SHA = "63ffaac12ae23d5e21ddbee7857e08f2a3f6d01a950b87a4128f27ae48594cc3"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
SOURCE_FILES = (PREFIX+"build_reference_module.py", PREFIX+"select_reference_module_build.py",
                PREFIX+MODULE+".lean", BUILDER, "tools/Run-V5-Check.py")
PROVENANCE = {
    "build/BUILD.json": "5811c38b872b094c284579241d9c90d463432ac35dc96d0ae6008b5b7df76213",
    "RESULT.json": "f997200b7abb83d13a0682261858b576d9938031c0368292bc5b5ec2b17632ec",
    "selection.json": "0de88c987ff006d5f7a070996c3d01f7aa34cd7d6f880e180c3e51e47d213ac4",
}
OWNER_PROVENANCE = {
    "RESULT.json": "0a3f1c599dc9cd49c1586a9f5622032aa8feeb15f405614e1055c95811d00a8b",
    "selection.json": "97a4c0d19aea620d067f9cf2a227706fd460654bf06b978cc201a2b7b2e8790b",
    "distribution/_build/BUILD-RESULT.json": "634820284798fbc1825c70c7b67f66c8ddf70a73783da51e7738dda40872fa02",
    "distribution/package/PROFILE.json": "3f3c0de037fd03907d661e428b6cc3592848ec8b66cc0e6fdbf579b0fb603026",
    "distribution/_build/SOURCES.json": "4a91efc4e7afbffa378ea2fef6066b73478f73c44070d01632c0e7de7bec0f63",
}
MIB = 1024**2
INNER_SPOOL = 104*MIB


def need(ok, code):
    if not ok:
        raise ValueError(code)


def read(path):
    with path.open("rb") as handle:
        raw = handle.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB, "REFERENCE_MODULE_BUILD_READ_BOUND")
    return raw


def helper():
    path = ROOT/BUILDER
    raw = read(path)
    need(hashlib.sha256(raw).hexdigest() == BUILDER_SHA, "REFERENCE_MODULE_BUILD_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_reference_module_builder", path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def clean_result(result, selection_sha):
    event = result["result"]
    need(result["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1" and
         result["selection_sha256"] == selection_sha and
         event["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and event["child_exit_code"] == 0 and
         event["direct_child_reaped"] is True and event["job_closed"] is True and
         event["cleanup_errors"] == [] and event["termination_requested"] is False and
         event["final_job"]["active_processes"] == event["final_job"]["terminated_processes"] == 0,
         "REFERENCE_MODULE_BUILD_PREDECESSOR_CLOSURE")


def inspect_inputs(B, check):
    pins = {}

    def keep(path, expected=None, maximum=512*MIB):
        value = B.pin(B.ordinary(path), check, maximum)
        need(expected is None or value == expected or value["sha256"] == expected,
             "REFERENCE_MODULE_BUILD_PIN:"+str(path))
        need(str(path) not in pins or pins[str(path)] == value, "REFERENCE_MODULE_BUILD_PIN_CONFLICT")
        pins[str(path)] = value
        return value

    def documents(root, identity):
        result = {}
        for relative, digest in identity.items():
            path = root/relative
            expected = keep(path, digest, 2*MIB)
            raw = read(path)
            need({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()} == expected,
                 "REFERENCE_MODULE_BUILD_METADATA_CHANGED")
            result[relative] = json.loads(raw)
        return result

    old = documents(OLD, PROVENANCE)
    clean_result(old["RESULT.json"], PROVENANCE["selection.json"])
    build, selected = old["build/BUILD.json"], old["selection.json"]
    need(selected["name"] == OLD.name and build["status"] == "BUILT_CANDIDATES_NOT_INSTALLED_OR_ADOPTED" and
         len(build["completed_commands"]) == 9 and all(r["exit_code"] == 0 for r in build["completed_commands"]),
         "REFERENCE_MODULE_BUILD_BASELINE_RECEIPT")
    for filename, expected in build["metadata"].items():
        need(filename in ("INPUTS.json", "NATIVE-OUTPUTS.json"), "REFERENCE_MODULE_BUILD_METADATA_ROLE")
        keep(OLD/"build"/filename, expected, 2*MIB)
    outputs = json.loads(read(OLD/"build/NATIVE-OUTPUTS.json"))
    need(outputs == build["all_candidate_outputs"], "REFERENCE_MODULE_BUILD_OUTPUT_MAP")
    reused = {}
    for name in (*SHARED, CORE):
        filename = name+".olean"
        path = OLD/"build"/("objects" if name == CORE else "shared")/filename
        expected = outputs[filename] if name == CORE else build["shared_objects"][filename]
        reused[filename] = {"path": str(path), **keep(path, expected, 32*MIB)}
    core_source = BASE_PREFIX+CORE+".lean"
    core_pin = build["source_files"][core_source]
    need(selected["sources"][core_source] == core_pin["sha256"], "REFERENCE_MODULE_BUILD_CORE_SOURCE")
    keep(ROOT/core_source, core_pin, 2*MIB)
    keep(OLD/"sources"/core_source, core_pin, 2*MIB)
    owner = documents(PACKAGE_BUILD, OWNER_PROVENANCE)
    clean_result(owner["RESULT.json"], OWNER_PROVENANCE["selection.json"])
    package_result = owner["distribution/_build/BUILD-RESULT.json"]
    profile = owner["distribution/package/PROFILE.json"]
    source_map = owner["distribution/_build/SOURCES.json"]
    need(owner["selection.json"]["name"] == PACKAGE_BUILD.name and
         package_result["status"] == "BUILT_NOT_ADOPTED" and
         package_result["profile_sha256"] == OWNER_PROVENANCE["distribution/package/PROFILE.json"] and
         package_result["installation_manifest_sha256"] == profile["installation_manifest_sha256"] and
         source_map["files"][OWNER_SOURCE]["sha256"] == OWNER_SOURCE_SHA,
         "REFERENCE_MODULE_BUILD_OWNER_PROVENANCE")
    keep(ROOT/OWNER_SOURCE, source_map["files"][OWNER_SOURCE], 2*MIB)
    for suffix in (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir"):
        filename = "OwnerRebind"+suffix
        path = PACKAGE/"authoring/helpers"/filename
        expected = profile["files"]["authoring/helpers/"+filename]
        reused[filename] = {"path": str(path), **keep(path, expected, 32*MIB)}
    runtime = {}
    for filename, digest in selected["runtime_pins"].items():
        path = Path(filename)
        if path.is_relative_to(PYTHON) or path.is_relative_to(LEAN):
            runtime[filename] = keep(path, digest)
    need(len(runtime) == 23 and str(PYTHON/"python.exe") in runtime and str(LEAN/"bin/lean.exe") in runtime,
         "REFERENCE_MODULE_BUILD_RUNTIME_CENSUS")
    sources = {name: keep(ROOT/name, maximum=2*MIB) for name in SOURCE_FILES}
    need(sources[BUILDER]["sha256"] == BUILDER_SHA and len(reused) == 11 and len(pins) <= 80,
         "REFERENCE_MODULE_BUILD_INPUT_CENSUS")
    return pins, reused, runtime, sources


def main(args):
    started, cpu = time.monotonic(), time.process_time()
    deadline = started+105

    def check():
        need(time.monotonic() < deadline and time.process_time()-cpu < 50,
             "REFERENCE_MODULE_BUILD_ORIGINAL_ALLOWANCE")

    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and Path(sys.executable).resolve() == PYTHON/"python.exe",
         "REFERENCE_MODULE_BUILD_CONTEXT")
    B = helper()
    source_root = B.ordinary(Path(args.source_root), directory=True)
    output = B.ordinary(Path(args.output), directory=True, fresh=True)
    need(output == LOCAL/NAME/"build" and Path(__file__).resolve() ==
         source_root/PREFIX/"build_reference_module.py", "REFERENCE_MODULE_BUILD_LOCATION")
    inputs, reused, runtime, sources = inspect_inputs(B, check)
    for name, expected in sources.items():
        need(B.pin(source_root/name, check, 2*MIB) == expected, "REFERENCE_MODULE_BUILD_SNAPSHOT")
    need(sum(row["bytes"] for row in reused.values())+16*MIB+8*MIB <= INNER_SPOOL,
         "REFERENCE_MODULE_BUILD_SPOOL_RESERVATION")
    output.mkdir()
    stage, support, objects = output/"source", output/"support", output/"objects"
    for path in (stage, support, objects):
        path.mkdir()
    completed, metadata = [], {}
    phase = "STAGING"

    def save(path, value):
        check()
        raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
        need(0 < len(raw) <= 2*MIB, "REFERENCE_MODULE_BUILD_METADATA_BOUND")
        B.fresh_bytes(path, raw)
        expected = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        need(B.pin(path, check, 2*MIB) == expected, "REFERENCE_MODULE_BUILD_READBACK")
        return expected

    def copy(source, destination, expected):
        B.ordinary(source); B.ordinary(destination, fresh=True)
        size, digest = 0, hashlib.sha256()
        with source.open("rb") as incoming, destination.open("xb") as outgoing:
            while block := incoming.read(MIB):
                check(); size += len(block)
                need(size <= expected["bytes"], "REFERENCE_MODULE_BUILD_COPY_BOUND")
                digest.update(block); outgoing.write(block)
            outgoing.flush(); os.fsync(outgoing.fileno())
        need({"bytes": size, "sha256": digest.hexdigest()} == expected and
             B.pin(source, check, 32*MIB) == expected and B.pin(destination, check, 32*MIB) == expected,
             "REFERENCE_MODULE_BUILD_COPY_PIN")

    def census(directory, expected, maximum):
        need({p.name for p in directory.iterdir()} == set(expected), "REFERENCE_MODULE_BUILD_FILE_CENSUS")
        total = 0
        for name, value in expected.items():
            need(B.pin(B.ordinary(directory/name), check, maximum) == value, "REFERENCE_MODULE_BUILD_FINAL_FILE")
            total += value["bytes"]
        return total

    try:
        for filename, row in reused.items():
            copy(Path(row["path"]), support/filename, {k: row[k] for k in ("bytes", "sha256")})
        source_relative = PREFIX+MODULE+".lean"
        copy(source_root/source_relative, stage/(MODULE+".lean"), sources[source_relative])
        metadata["INPUTS.json"] = save(output/"INPUTS.json", {"inputs": inputs, "reused_support": reused,
            "source_snapshots": {name: {"path": str(source_root/name), **value} for name, value in sources.items()},
            "baseline_provenance": PROVENANCE, "owner_provenance": OWNER_PROVENANCE,
            "purpose": "SOURCE_QUALIFICATION_ONLY_NO_REFERENCE_OR_DELTA_EXECUTION"})
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith(
            ("LEAN", "PYTHON", "RUST", "CARGO", "RISC0", "NODE")) and k.upper() not in ("PATH", "VIRTUAL_ENV")}
        env["PATH"], env["LEAN_PATH"] = str(LEAN/"bin"), str(support)
        argv = [str(LEAN/"bin/lean.exe"), "-DElab.async=false", "-R", str(stage),
                "-o", str(objects/(MODULE+".olean")), str(stage/(MODULE+".lean"))]
        need(sum(len(v)+3 for v in argv) <= 30000, "REFERENCE_MODULE_BUILD_ARGV_BOUND")
        phase = "reference-module-compile"
        check(); before = time.monotonic()
        result = subprocess.run(argv, cwd=output, env=env, stdin=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW, timeout=max(0.001, deadline-before))
        completed.append({"phase": phase, "argv": argv, "exit_code": result.returncode,
                          "wall_seconds": time.monotonic()-before})
        print(json.dumps(completed[-1], sort_keys=True), flush=True)
        need(result.returncode == 0, "REFERENCE_MODULE_BUILD_COMPILE_FAILED")
        generated = {MODULE+".olean": B.pin(B.ordinary(objects/(MODULE+".olean")), check, 16*MIB)}
        metadata["NATIVE-OUTPUTS.json"] = save(output/"NATIVE-OUTPUTS.json", generated)
        phase = "FINAL_REHASH"
        for filename, expected in inputs.items():
            need(B.pin(Path(filename), check, 512*MIB) == expected, "REFERENCE_MODULE_BUILD_FINAL_INPUT")
        for name, expected in sources.items():
            need(B.pin(source_root/name, check, 2*MIB) == expected, "REFERENCE_MODULE_BUILD_FINAL_SNAPSHOT")
        support_pins = {name: {k: row[k] for k in ("bytes", "sha256")} for name, row in reused.items()}
        total = census(support, support_pins, 32*MIB)+census(objects, generated, 16*MIB)
        total += census(stage, {MODULE+".lean": sources[source_relative]}, 2*MIB)
        for name, expected in metadata.items():
            need(B.pin(output/name, check, 2*MIB) == expected, "REFERENCE_MODULE_BUILD_FINAL_METADATA")
            total += expected["bytes"]
        need(total+2*MIB <= INNER_SPOOL and {p.name for p in output.iterdir()} ==
             {"source", "support", "objects", "INPUTS.json", "NATIVE-OUTPUTS.json"},
             "REFERENCE_MODULE_BUILD_FINAL_CENSUS")
        receipt = {"schema": "DMKN_ORDINARY_REFERENCE_MODULE_BUILD_V1",
            "status": "COMPILED_CANDIDATE_NOT_INSTALLED_OR_EXECUTED", "mathematical_acceptance": False,
            "source": {"path": str(ROOT/source_relative), **sources[source_relative]},
            "compiled_module": {"path": str(objects/(MODULE+".olean")), **generated[MODULE+".olean"]},
            "inputs": inputs, "source_files": sources, "reused_support": reused, "generated_outputs": generated,
            "metadata": metadata, "completed_commands": completed, "runtime_pin_count": len(runtime),
            "baseline_provenance": PROVENANCE, "owner_provenance": OWNER_PROVENANCE,
            "fresh_inner_spool_maximum_bytes": INNER_SPOOL, "spool_before_receipt": total,
            "bounds": "COOPERATIVE_FILE_CENSUS_NOT_HARD_DISK_QUOTA",
            "wall_seconds": time.monotonic()-started, "controller_cpu_seconds": time.process_time()-cpu,
            "inclusive_cpu_and_closure": "ONLY_ENCLOSING_JOB_RESULT",
            "next_step": "SEPARATE_OWNER_INTEGRATION_SELECTION_NO_AUTOMATIC_EXECUTION"}
        phase = "BUILD_RECEIPT"
        save(output/"BUILD.json", receipt); check()
        print(json.dumps({"status": receipt["status"], "commands": 1}), flush=True)
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

"""Compile only repaired Source02; retain failed01 and reuse its successful helper."""
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
PREFIX = "software/v5/ordinary_reference/"
NAME = "ordinary-reference-source-continuation-01"
OLD_NAME = "ordinary-reference-source-build-01"
BASE = "build_reference_source.py"
BASE_SHA = "7287ddd595c8ef54fad3e659923b26934283b80be6f00ad4a4b585c4927e0951"
FRESH = (PREFIX+"build_reference_source_continuation.py",
         PREFIX+"select_reference_source_continuation.py", PREFIX+"ReferenceSource02.lean")
PARTIAL_PROVENANCE = {
    "RESULT.json": "cbe0bdd69220a1793321b291b36b55cee73c9cee9722c50f75835eddd494750d",
    "selection.json": "aa6026c11c205472b8bc800c6af477c720da0f5a119f5dda362258d93af1c0fe",
    "build/BUILD-FAILURE.json": "4c51dd23ff0c59084591b4573d249ffcd5eaf5eed992b0aa58e47c44473a54ab",
    "build/INPUTS.json": "3e8de58e928004d3aa92bad124f430ccf4d437cd1b89e3cbbe15f561fa42ea69",
}
ENVIRONMENT_PIN = {"bytes": 2378696,
    "sha256": "a082feb7bfcf3b28199c4438baafc11e3e00b4ad37af07e3507473e1e452c698"}
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def base():
    path = ROOT/PREFIX/BASE
    with path.open("rb") as handle:
        raw = handle.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == BASE_SHA, "SOURCE_CONTINUATION_BASE_PIN")
    spec = importlib.util.spec_from_file_location("_source_continuation_base", path)
    H = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec"), H.__dict__)
    return H


def inspect_inputs(H, B, check):
    inputs, reused, runtime, sources = H.inspect_inputs(B, check)
    old, docs = H.LOCAL/OLD_NAME, {}

    def keep(path, expected, maximum=2*MIB):
        value = B.pin(B.ordinary(path), check, maximum)
        need(value == expected or value["sha256"] == expected, "SOURCE_CONTINUATION_INPUT_PIN")
        need(str(path) not in inputs or inputs[str(path)] == value, "SOURCE_CONTINUATION_PIN_CONFLICT")
        inputs[str(path)] = value
        return value

    for relative, digest in PARTIAL_PROVENANCE.items():
        pin = keep(old/relative, digest)
        raw = H.read(old/relative)
        need({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()} == pin,
             "SOURCE_CONTINUATION_METADATA_CHANGED")
        docs[relative] = json.loads(raw)
    result, selected = docs["RESULT.json"], docs["selection.json"]
    failure, initial = docs["build/BUILD-FAILURE.json"], docs["build/INPUTS.json"]
    event = result["result"]
    need(result["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1" and selected["name"] == OLD_NAME and
         result["selection_sha256"] == PARTIAL_PROVENANCE["selection.json"] and
         event["status"] == "COMMAND_FAILED" and event["child_exit_code"] == 1 and
         event["direct_child_reaped"] is True and event["job_closed"] is True and
         event["cleanup_errors"] == [] and event["termination_requested"] is False and
         event["final_job"]["active_processes"] == event["final_job"]["terminated_processes"] == 0 and
         failure["phase"] == "ReferenceSource-compile" and failure["error"] == "REFERENCE_SOURCE_BUILD_COMPILE_FAILED",
         "SOURCE_CONTINUATION_EXPECTED_FAILED_PREDECESSOR")
    commands = failure["completed_commands"]
    need(len(commands) == 2 and [(row["phase"], row["exit_code"]) for row in commands] ==
         [("ReferenceEnvironment-compile", 0), ("ReferenceSource-compile", 1)],
         "SOURCE_CONTINUATION_PARTIAL_COMMANDS")
    for row, module in zip(commands, ("ReferenceEnvironment", "ReferenceSource")):
        need(row["argv"] == [str(H.LEAN/"bin/lean.exe"), "-DElab.async=false", "-R", str(old/"build/source"),
             "-o", str(old/"build/objects"/(module+".olean")), str(old/"build/source"/(module+".lean"))],
             "SOURCE_CONTINUATION_PARTIAL_COMMAND_BINDING")
    need(initial["reused_support"] == reused and
         {p.name for p in B.ordinary(old/"build/objects", directory=True).iterdir()} == {"ReferenceEnvironment.olean"},
         "SOURCE_CONTINUATION_RETAINED_SUPPORT")
    for module in ("ReferenceEnvironment", "ReferenceSource"):
        relative = PREFIX+module+".lean"
        expected = sources[relative]
        need(selected["sources"][relative] == expected["sha256"] and
             initial["source_snapshots"][relative] == {"path": str(old/"sources"/relative), **expected},
             "SOURCE_CONTINUATION_PARTIAL_SOURCE")
        keep(old/"sources"/relative, expected)
        keep(old/"build/source"/(module+".lean"), expected)
    env_path = old/"build/objects/ReferenceEnvironment.olean"
    reused["ReferenceEnvironment.olean"] = {"path": str(env_path), **keep(env_path, ENVIRONMENT_PIN, 16*MIB)}
    for relative in FRESH:
        value = B.pin(B.ordinary(ROOT/relative), check, 2*MIB)
        inputs[str(ROOT/relative)], sources[relative] = value, value
    need(len(sources) == 11 and len(reused) == 12 and len(runtime) == 23 and len(inputs) <= 80,
         "SOURCE_CONTINUATION_CENSUS")
    return inputs, reused, runtime, sources


def main(args):
    started, cpu = time.monotonic(), time.process_time()
    deadline = started+75

    def check():
        need(time.monotonic() < deadline and time.process_time()-cpu < 45, "SOURCE_CONTINUATION_ALLOWANCE")

    H = base(); B = H.helper()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and Path(sys.executable).resolve() == H.PYTHON/"python.exe",
         "SOURCE_CONTINUATION_CONTEXT")
    source_root = B.ordinary(Path(args.source_root), directory=True)
    output = B.ordinary(Path(args.output), directory=True, fresh=True)
    need(output == H.LOCAL/NAME/"build" and Path(__file__).resolve() ==
         source_root/FRESH[0], "SOURCE_CONTINUATION_LOCATION")
    inputs, reused, runtime, sources = inspect_inputs(H, B, check)
    for relative, expected in sources.items():
        need(B.pin(source_root/relative, check, 2*MIB) == expected, "SOURCE_CONTINUATION_SNAPSHOT")
    output.mkdir(); (output/"source").mkdir(); (output/"objects").mkdir()
    completed, metadata = [], {}
    phase = "STAGING"

    def save(path, value):
        check()
        raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
        need(0 < len(raw) <= 2*MIB, "SOURCE_CONTINUATION_METADATA_BOUND")
        B.fresh_bytes(path, raw)
        pin = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        need(B.pin(path, check, 2*MIB) == pin, "SOURCE_CONTINUATION_READBACK")
        return pin

    try:
        source = output/"source/ReferenceSource02.lean"
        raw = H.read(source_root/FRESH[2])
        need({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()} == sources[FRESH[2]],
             "SOURCE_CONTINUATION_STAGE_PIN")
        B.fresh_bytes(source, raw)
        metadata["INPUTS.json"] = save(output/"INPUTS.json", {"inputs": inputs, "reused_support": reused,
            "source_files": sources, "partial_provenance": PARTIAL_PROVENANCE,
            "retained_environment": "EXPLICIT_PIN_FROM_SUCCESSFUL_FIRST_COMMAND_OF_FAILED_BUILD"})
        env = {key: value for key, value in os.environ.items() if not key.upper().startswith(
            ("LEAN", "PYTHON", "RUST", "CARGO", "RISC0", "NODE")) and key.upper() not in ("PATH", "VIRTUAL_ENV")}
        env["PATH"] = str(H.LEAN/"bin")
        env["LEAN_PATH"] = os.pathsep.join((str(H.LOCAL/OLD_NAME/"build/objects"), str(H.SUPPORT)))
        target = output/"objects/ReferenceSource02.olean"
        argv = [str(H.LEAN/"bin/lean.exe"), "-DElab.async=false", "-R", str(source.parent), "-o", str(target), str(source)]
        need(sum(len(value)+3 for value in argv) <= 30000, "SOURCE_CONTINUATION_ARGV_BOUND")
        phase = "ReferenceSource02-compile"; check(); before = time.monotonic()
        result = subprocess.run(argv, cwd=output, env=env, stdin=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW, timeout=max(0.001, deadline-before))
        completed.append({"phase": phase, "argv": argv, "exit_code": result.returncode,
                          "wall_seconds": time.monotonic()-before})
        print(json.dumps(completed[-1], sort_keys=True), flush=True)
        need(result.returncode == 0, "SOURCE_CONTINUATION_COMPILE_FAILED")
        generated = {target.name: B.pin(B.ordinary(target), check, 16*MIB)}
        metadata["NATIVE-OUTPUTS.json"] = save(output/"NATIVE-OUTPUTS.json", generated)
        phase = "FINAL_REHASH"
        for filename, expected in inputs.items():
            need(B.pin(Path(filename), check, 512*MIB) == expected, "SOURCE_CONTINUATION_FINAL_INPUT")
        for relative, expected in sources.items():
            need(B.pin(source_root/relative, check, 2*MIB) == expected, "SOURCE_CONTINUATION_FINAL_SNAPSHOT")
        need(B.pin(source, check, 2*MIB) == sources[FRESH[2]] and
             {p.name for p in source.parent.iterdir()} == {source.name} and
             {p.name for p in target.parent.iterdir()} == {target.name} and
             B.pin(target, check, 16*MIB) == generated[target.name] and
             {p.name for p in output.iterdir()} == {"source", "objects", "INPUTS.json", "NATIVE-OUTPUTS.json"},
             "SOURCE_CONTINUATION_FINAL_CENSUS")
        for filename, expected in metadata.items():
            need(B.pin(output/filename, check, 2*MIB) == expected, "SOURCE_CONTINUATION_FINAL_METADATA")
        total = sources[FRESH[2]]["bytes"]+generated[target.name]["bytes"]+sum(p["bytes"] for p in metadata.values())
        need(total+2*MIB <= 32*MIB, "SOURCE_CONTINUATION_SPOOL")
        receipt = {"schema": "DMKN_ORDINARY_REFERENCE_SOURCE_CONTINUATION_V1",
            "status": "COMPILED_SOURCE_CANDIDATE_REUSING_PARTIAL_ENVIRONMENT_NOT_EXECUTED",
            "mathematical_acceptance": False, "inputs": inputs, "source_files": sources,
            "reused_support": reused, "generated_outputs": generated, "metadata": metadata,
            "completed_commands": completed, "runtime_pin_count": len(runtime),
            "partial_provenance": PARTIAL_PROVENANCE, "support_provenance": H.PROVENANCE,
            "fresh_inner_spool_maximum_bytes": 32*MIB, "spool_before_receipt": total,
            "bounds": "COOPERATIVE_FILE_CENSUS_NOT_HARD_DISK_QUOTA",
            "wall_seconds": time.monotonic()-started, "controller_cpu_seconds": time.process_time()-cpu,
            "inclusive_cpu_and_closure": "ONLY_ENCLOSING_JOB_RESULT"}
        phase = "BUILD_RECEIPT"; save(output/"BUILD.json", receipt); check()
        print(json.dumps({"status": receipt["status"], "commands": 1}), flush=True)
    except BaseException as error:
        try:
            B.fresh_bytes(output/"BUILD-FAILURE.json", json.dumps({"phase": phase,
                "error_type": type(error).__name__, "error": str(error)[:2048], "completed_commands": completed,
                "mathematical_acceptance": False, "retention": "PRESERVE_ALL_NO_RETRY"}, sort_keys=True).encode("ascii"))
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output", required=True)
    main(parser.parse_args())

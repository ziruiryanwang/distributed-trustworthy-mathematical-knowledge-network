"""Bounded read-only adoption of one preserved compiled artifact, not a build.

Requires a separately selected outer Job and source snapshot. Reuses audited
compiler/SDK provenance; never scans target/cache/SDK trees or invokes tools.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import struct
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
PREFIX = HERE / "aggregate-guest-build-01"
COMPILE = HERE / "aggregate-guest-compile-01"
PASS = "PASS_REVALIDATED_AGGREGATE_GUEST_ARTIFACT_ONLY"
RECORDS = {
    "aggregate-guest-build-01/RESULT.json": "231c94114e625a59371fdb1208aa7ae2838c9c35c9b8877b80bead4e7ad7e0ac",
    "aggregate-guest-build-01/SOURCE-MAP.json": "52c5166f2d41b7922a8916182ebbcbdc40e0dba2833899602273159654d0084b",
    "aggregate-guest-build-01/selection.json": "011ac45c532756eba74a573f66a06e1a2f0e78ba1219aed2bdd6bef8a3d67f70",
    "aggregate-guest-build-01/commands/offline-aggregate-graph/stdout.txt": "2cc441345c1cf3cc16e9dd21cca1bf2130319dbfa1124ad3ddb1d6507f2f4609",
    "aggregate-guest-build-01-attempt.json": "afbe7c3b9e4ae4b69484a5e9bdbab8ab1c62ab5427f736b10af5f2e58f2eeb6a",
    "aggregate-guest-compile-01/RESULT.json": "81cce68d9b20f22b12d12d5d698084eb8eb101493de71c6e35cd6acb7b44f47a",
    "aggregate-guest-compile-01/FINALIZATION-FAILED.json": "d0d6d8980c492d43a8927825aa153271543fa18d960305db5bde1e51c323dd54",
    "aggregate-guest-compile-01/ARTIFACT.json": "dc3a4f79e1006bf45d8355829486ee0b2bb019bd4fd12cf45fb0aec37cfc5904",
    "aggregate-guest-compile-01/SOURCE-MAP.json": "75c710e3ee13f63cb6ef44da8656caa53c300bf649317d2b5669d8b9cde06ce0",
    "aggregate-guest-compile-01/GRAPH-COMPARISON.json": "a7f5ea2fe059e6a57a6aaad48e616986267afe2b7c8a8c60de3194e2b010d458",
    "aggregate-guest-compile-01/selection.json": "19fef22ed3323d963349d67c131cea7a7b1dea8de82321be9ef2c33ffe06b7cd",
    "aggregate-guest-compile-01-attempt.json": "5e0b848fbd32c7b3dd58962658d90c3fb76771a2a3d58229acb7f9a1e63251b0",
}


def need(value, reason):
    if not value:
        raise ValueError(reason)


def file_bytes(path, maximum=4 * 1024**2):
    need(path.is_absolute() and path.resolve(strict=True) == path and path.is_file(), "EXACT_FILE_PATH")
    size = path.stat().st_size
    need(0 <= size <= maximum, "BOUNDED_INPUT_FILE")
    raw = path.read_bytes()
    need(len(raw) == size and path.stat().st_size == size, "FILE_SIZE_CHANGED")
    return raw, {"bytes": size, "sha256": hashlib.sha256(raw).hexdigest()}


def save(path, value):
    raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    need(len(raw) <= 128 * 1024, "REPORT_SIZE_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def elf_headers(raw):
    need(len(raw) >= 52 and raw[:7] == b"\x7fELF\x01\x01\x01", "ELF32_LE_VERSION1")
    fields = struct.unpack_from("<HHIIIIIHHHHHH", raw, 16)
    kind, machine, version, entry, phoff, _, _, ehsize, phsize, phcount, _, _, _ = fields
    need((kind, machine, version, ehsize, phsize) == (2, 243, 1, 52, 32)
         and 1 <= phcount <= 256 and phoff + phcount * phsize <= len(raw), "EXECUTABLE_RV32_HEADERS")
    segments = []
    for index in range(phcount):
        kind, offset, address, _, filesz, memsz, flags, _ = struct.unpack_from("<IIIIIIII", raw, phoff + index * phsize)
        if kind == 1:
            need(filesz <= memsz and offset + filesz <= len(raw) and address + memsz <= 2**32,
                 "BOUNDED_LOAD_SEGMENT")
            segments.append({"address": address, "file_bytes": filesz, "memory_bytes": memsz, "flags": flags})
    need(segments and any(row["flags"] & 1 and row["address"] <= entry < row["address"] + row["memory_bytes"]
                          for row in segments), "ENTRY_IN_EXECUTABLE_SEGMENT")
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "entry": entry, "segments": segments}


def main():
    started, cpu = time.monotonic(), time.process_time()
    invoked = Path(__file__).resolve(strict=True)
    need(invoked.is_relative_to(HERE), "OWNER_JOB_SNAPSHOT_ROOT")
    parts = invoked.relative_to(HERE).parts
    need(len(parts) == 6 and parts[1:] == ("sources", "software", "v5", "aggregate_guest", "validate_artifact.py")
         and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", parts[0]) and os.name == "nt" and Path.cwd() == ROOT
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "EXACT_OUTER_JOB_SNAPSHOT_INVOCATION")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    operation = HERE / parts[0]
    need(output.is_absolute() and output.is_relative_to(operation) and output.resolve() == output
         and not output.exists(), "FRESH_OWNED_VALIDATION_OUTPUT")
    output.mkdir()
    report = {"schema": "DMKN_V5_AGGREGATE_ARTIFACT_VALIDATION_V1", "status": "FAIL_ARTIFACT_VALIDATION",
              "old_failure_preserved": True, "prior_budget_met": False, "new_compile_calls": 0,
              "new_graph_calls": 0, "image_assembly_calls": 0, "guest_executions": 0, "proof_calls": 0,
              "mathematical_admission": False}
    bound = {}

    def bind(path, expected, maximum=4 * 1024**2):
        need(time.monotonic() - started < 45 and time.process_time() - cpu < 24, "SMALL_VALIDATION_ENVELOPE")
        raw, pin = file_bytes(path, maximum)
        need(set(expected) <= {"path", "bytes", "sha256"}
             and all(pin[key] == expected[key] for key in ("bytes", "sha256") if key in expected), "EXACT_RETAINED_PIN")
        if "path" in expected:
            need(expected["path"] == str(path), "EXACT_RETAINED_LOCATION")
        bound[str(path)] = pin
        return raw

    code = 1
    try:
        records = {name: bind(HERE / name, {"sha256": digest}) for name, digest in RECORDS.items()}
        data = lambda name: json.loads(records[name])
        prefix = data("aggregate-guest-build-01/RESULT.json")
        built = data("aggregate-guest-compile-01/RESULT.json")
        override = data("aggregate-guest-compile-01/FINALIZATION-FAILED.json")
        need(override == {"status": "FAIL_FINALIZATION", "overrides_result_and_attempt": True,
              "result_sha256": RECORDS["aggregate-guest-compile-01/RESULT.json"], "error": "REMAINING_TOTAL_ENVELOPE"},
             "ORIGINAL_RESOURCE_FAILURE_MUST_REMAIN")
        need(built["status"] == "PASS_OPTIMIZED_EXACT_WARRANT_AGGREGATE_GUEST_COMPILE_ONLY"
             and built.get("error") is None and built.get("final_check_error") is None
             and built["controller_cpu_seconds"] == 149.640625 and built["controller_cpu_seconds"] > 134
             and built["job"]["active_processes"] == built["job"]["terminated_processes"] == 0
             and prefix["status"] == "FAIL" and prefix["job"]["active_processes"] == 0,
             "KNOWN_CLOSED_PREFIX_AND_RECORDED_BUDGET_FAILURE")
        need(built["guest_executions"] == built["proof_calls"] == built["image_assembly_calls"] == built["new_graph_calls"] == 0
             and len(built["commands"]) == 1 and len(prefix["commands"]) == 1, "NO_UNRECORDED_WORK")
        command = built["commands"][0]
        expected_argv = [str(ROOT / "experiments/scale-crypto-01/runs/run-01/rust/bin/cargo.exe"), "build", "--release",
            "--manifest-path", str(PREFIX / "project/software/v5/aggregate_guest/Cargo.toml"),
            "--bin", "dmkn-aggregate-claim-guest", "--target", "riscv32im-risc0-zkvm-elf",
            "-Z", "build-std=alloc,core,proc_macro,panic_abort,std", "-Z", "build-std-features=compiler-builtins-mem",
            "--locked", "--offline", "--message-format=json"]
        need(command["argv"] == expected_argv and command["label"] == "build-aggregate-guest"
             and command["cwd"] == str(PREFIX / "project/software/v5/aggregate_guest")
             and command["exit_code"] == 0 and command["cleanup_errors"] == []
             and command["job_after"]["active_processes"] == 0, "EXACT_SUCCESSFUL_CARGO_PREFIX")
        source_map = data("aggregate-guest-compile-01/SOURCE-MAP.json")
        prior_map = data("aggregate-guest-build-01/SOURCE-MAP.json")
        chosen = data("aggregate-guest-build-01/selection.json")
        project = PREFIX / "project"
        need(source_map["reused_project"] == str(project) and source_map["project"] == prior_map["project"]
             and len(chosen["sources"]) == 38 and len(source_map["project"]) == 39
             and set(source_map["project"]) == set(chosen["sources"]) | {"software/v5/aggregate_guest/Cargo.lock"}
             and all(source_map["project"][name] == pin for name, pin in chosen["sources"].items()),
             "EXACT_39_SOURCE_AND_LOCK_BINDINGS")
        need(sum(pin["bytes"] for pin in source_map["project"].values()) <= 16 * 1024**2, "TOTAL_SOURCE_BYTES")
        for relative, pin in source_map["project"].items():
            path = project / relative
            need(path.is_relative_to(project) and path.resolve(strict=True) == path, "SOURCE_ESCAPE")
            bind(path, pin, 2 * 1024**2)
        bind(Path(source_map["controller"]["path"]), source_map["controller"], 1024**2)
        graph = data("aggregate-guest-compile-01/GRAPH-COMPARISON.json")
        need(graph == built["graph_delta"] and graph["status"] == "EXACT_FOUR_LEXICAL_FIELDS_WITH_FULL_GRAPH_EQUALITY"
             and graph["units"] == 297 and len(graph["changes"]) == 4
             and graph["external_package_feature_profile_or_edge_changes"] == graph["new_graph_calls"] == 0,
             "ADOPTED_EXACT_GRAPH_COMPARISON")
        logs = command["logs"]
        need(len(logs) == 2 and [row["path"] for row in logs] ==
             [str(COMPILE / "commands/build-aggregate-guest" / name) for name in ("stdout.txt", "stderr.txt")],
             "EXACT_COMPILER_LOG_PATHS")
        stdout = bind(Path(logs[0]["path"]), logs[0])
        bind(Path(logs[1]["path"]), logs[1])
        rows = [json.loads(line) for line in stdout.decode("utf-8").splitlines()]
        need([row.get("success") for row in rows if row.get("reason") == "build-finished"] == [True],
             "ACTUAL_CARGO_BUILD_FINISHED")
        artifacts = [row for row in rows if row.get("reason") == "compiler-artifact"
                     and row.get("target", {}).get("name") == "dmkn-aggregate-claim-guest" and row.get("executable")]
        need(len(artifacts) == 1, "ONE_ACTUAL_GUEST_ARTIFACT")
        compiler = artifacts[0]
        artifact = data("aggregate-guest-compile-01/ARTIFACT.json")
        need(artifact == built["artifact"] and compiler["target"]["kind"] == ["bin"]
             and compiler["profile"]["test"] is False and compiler["profile"]["overflow_checks"] is True
             and Path(compiler["target"]["src_path"]).resolve(strict=True) == project / "software/v5/aggregate/main.rs"
             and compiler["executable"] == artifact["user_elf"]["path"] ==
                 str(COMPILE / "target/riscv32im-risc0-zkvm-elf/release/dmkn-aggregate-claim-guest")
             and artifact["link_map"]["path"] == str(COMPILE / "guest-link.map"), "EXACT_ELF_SOURCE_AND_MAP_LINEAGE")
        elf = bind(Path(artifact["user_elf"]["path"]), artifact["user_elf"])
        link_map = bind(Path(artifact["link_map"]["path"]), artifact["link_map"])
        need(elf_headers(elf) == artifact["elf_headers"], "ACTUAL_ELF_HEADERS_AGREE")
        symbols = link_map.decode("utf-8")
        need(re.search(r"\b_start\b", symbols) and re.search(r"\b__start\b", symbols), "RETAINED_STARTUP_SYMBOLS")
        for path, pin in list(bound.items()):
            need(file_bytes(Path(path))[1] == pin, "FINAL_SELECTED_INPUT_REBIND")
        need(time.monotonic() - started < 45 and time.process_time() - cpu < 24, "FINAL_SMALL_VALIDATION_ENVELOPE")
        report.update(status=PASS, artifact=artifact, source_files=39, bound_files=bound,
            prior_effective_status="FAIL_FINALIZATION", compiler_sdk_provenance="REUSED_PREVIOUSLY_AUDITED_COMPLETE_REBIND",
            compile_result={"path": str(COMPILE / "RESULT.json"), "sha256": RECORDS["aggregate-guest-compile-01/RESULT.json"]},
            preserved_failure={"path": str(COMPILE / "FINALIZATION-FAILED.json"),
                               "sha256": RECORDS["aggregate-guest-compile-01/FINALIZATION-FAILED.json"]},
            prior_recorded_costs={"worker_cpu_seconds": prefix["job"]["cpu_seconds"] + built["job"]["cpu_seconds"],
                "controller_cpu_seconds": prefix["controller_cpu_seconds"] + built["controller_cpu_seconds"],
                "wall_seconds": prefix["wall_seconds"] + built["wall_seconds"],
                "accounting": "ORIGINAL_FINAL_REPORT_EXIT_TAILS_EXCLUDED;NEW_VALIDATION_CHARGED_SEPARATELY"},
            authority="EXISTING_SOURCE_BOUND_ELF_ARTIFACT_ONLY_NOT_BUILD_BUDGET_PASS_OR_MATHEMATICAL_ADMISSION")
        code = 0
    except BaseException as error:
        report["error"] = type(error).__name__ + ": " + str(error)[:2000]
    finally:
        report.update(controller_cpu_seconds=time.process_time() - cpu, wall_seconds=time.monotonic() - started)
        save(output / "RESULT.json", report)
        if time.monotonic() - started >= 45 or time.process_time() - cpu >= 24:
            save(output / "FINALIZATION-FAILED.json", {"status": "FAIL_FINALIZATION", "overrides_result": True,
                 "result_sha256": file_bytes(output / "RESULT.json")[1]["sha256"], "error": "SMALL_VALIDATION_ENVELOPE"})
            code = 1
    print(json.dumps({"status": report["status"] if code == 0 else "FAIL_ARTIFACT_VALIDATION",
                      "output": str(output), "new_compile_calls": 0}))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

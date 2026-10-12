"""One owner-selected aggregate guest image assembly; no execution or proving.

Run only inside the root-selected bounded local-check Job. The existing pinned
assembler/kernel are reused; the existing aggregate ELF requires a separately
adopted artifact-validation record. Its original resource failure stays failed.
An image ID is not a certificate or mathematical admission.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
SNAPSHOT_SUFFIX = ("sources", "software", "v5", "aggregate_guest", "assemble.py")
DRIVER_HOME = ROOT / "experiments/general-checker-guest-02/driver-build-04"
DRIVER_RESULT_SHA = "d89626da253ade06a4482d6e7f4a7e9aac0f93d360a2eab2f1b39ba25cc8c43a"
KERNEL = ROOT / ("experiments/general-checker-guest-01/host-prepare-01/original/"
                "risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8/risc0/zkos/v1compat/elfs/v1compat.elf")
KERNEL_PIN = {"bytes": 58736,
              "sha256": "9dd8af014a24db3752b9beda71c837f553ff361fc1bca83cc79584bd38ac9de5"}
BUILD_PASS = "PASS_OPTIMIZED_EXACT_WARRANT_AGGREGATE_GUEST_COMPILE_ONLY"
PREFIX = HERE / "aggregate-guest-build-01"
PREFIX_RESULT_SHA = "231c94114e625a59371fdb1208aa7ae2838c9c35c9b8877b80bead4e7ad7e0ac"
PREFIX_GRAPH_SHA = "2cc441345c1cf3cc16e9dd21cca1bf2130319dbfa1124ad3ddb1d6507f2f4609"
PREFIX_ATTEMPT_SHA = "afbe7c3b9e4ae4b69484a5e9bdbab8ab1c62ab5427f736b10af5f2e58f2eeb6a"
COMPILE_RESULT_SHA = "81cce68d9b20f22b12d12d5d698084eb8eb101493de71c6e35cd6acb7b44f47a"
COMPILE_FAILURE_SHA = "d0d6d8980c492d43a8927825aa153271543fa18d960305db5bde1e51c323dd54"
FILE_LIMIT = 64 * 1024**2


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def pin(path, maximum=FILE_LIMIT):
    need(path.is_absolute() and path.resolve(strict=True) == path and path.is_file(), "EXACT_ABSOLUTE_FILE")
    size = path.stat().st_size
    need(0 < size <= maximum, "INPUT_SIZE_BOUND")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    need(path.stat().st_size == size, "INPUT_CHANGED_DURING_HASH")
    return {"bytes": size, "sha256": digest}


def save(path, value):
    with path.open("xb") as stream:
        stream.write((json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8"))


def main():
    invoked = Path(__file__).resolve(strict=True)
    need(invoked.is_relative_to(HERE), "OWNER_JOB_SOURCE_SNAPSHOT_ROOT")
    relative = invoked.relative_to(HERE).parts
    need(len(relative) == 6 and relative[1:] == SNAPSHOT_SUFFIX
         and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", relative[0]), "EXACT_OWNER_JOB_SOURCE_SNAPSHOT")
    need(os.name == "nt" and Path.cwd() == ROOT
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, "CANONICAL_ISOLATED_OWNER_INVOCATION")
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-validation", required=True)
    parser.add_argument("--artifact-validation-sha256", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    validation_result, output = Path(args.artifact_validation), Path(args.output)
    need(output.is_absolute() and output.is_relative_to(HERE)
         and output.resolve() == output and not output.exists(), "FRESH_LOCAL_ASSEMBLY_OUTPUT")
    need(validation_result.is_absolute() and validation_result.is_relative_to(HERE)
         and validation_result.name == "RESULT.json", "EXACT_ARTIFACT_VALIDATION_RESULT_PATH")
    validation_pin = pin(validation_result, 2 * 1024**2)
    need(validation_pin["sha256"] == args.artifact_validation_sha256
         and not (validation_result.parent / "FINALIZATION-FAILED.json").exists(), "ADOPTED_VALIDATION_PIN_AND_FINALIZATION")
    validation = json.loads(validation_result.read_bytes())
    need(validation["schema"] == "DMKN_V5_AGGREGATE_ARTIFACT_VALIDATION_V1"
         and validation["status"] == "PASS_REVALIDATED_AGGREGATE_GUEST_ARTIFACT_ONLY"
         and validation["old_failure_preserved"] is True and validation["prior_budget_met"] is False
         and validation["prior_effective_status"] == "FAIL_FINALIZATION"
         and validation["mathematical_admission"] is False
         and all(validation[name] == 0 for name in ("new_compile_calls", "new_graph_calls",
             "image_assembly_calls", "guest_executions", "proof_calls")), "EXPLICIT_ARTIFACT_ONLY_READOPTION")
    build_result = HERE / "aggregate-guest-compile-01/RESULT.json"
    result_pin = pin(build_result, 2 * 1024**2)
    need(result_pin["sha256"] == COMPILE_RESULT_SHA
         and validation["compile_result"] == {"path": str(build_result), "sha256": COMPILE_RESULT_SHA},
         "REVALIDATED_EXACT_COMPILER_PREFIX")
    built = json.loads(build_result.read_bytes())
    need(built["schema"] == "DMKN_V5_AGGREGATE_GUEST_COMPILE_RESULT_V1"
         and built["status"] == BUILD_PASS and built["job"]["active_processes"] == 0
         and built["guest_executions"] == built["proof_calls"] == built["image_assembly_calls"] == 0
         and built["network_fetch_commands"] == built["host_backend_builds"] == built["new_graph_calls"] == 0,
         "ACTUAL_CLOSED_COMPILER_PREFIX_NOT_OVERALL_BUDGET_PASS")
    need(len(built["commands"]) == 1
         and built["commands"][0]["label"] == "build-aggregate-guest"
         and all(row["exit_code"] == 0 and row["cleanup_errors"] == []
                 and row["job_after"]["active_processes"] == 0 for row in built["commands"]),
         "EXACT_ONE_CLOSED_COMPILE_COMMAND")
    prefix_result = PREFIX / "RESULT.json"
    prefix_graph = PREFIX / "commands/offline-aggregate-graph/stdout.txt"
    prefix_attempt = HERE / "aggregate-guest-build-01-attempt.json"
    need(built["predecessor_result"] == {"path": str(prefix_result), "sha256": PREFIX_RESULT_SHA}
         and built["predecessor_graph"] == {"path": str(prefix_graph), "sha256": PREFIX_GRAPH_SHA},
         "EXACT_RETAINED_GRAPH_LINEAGE")
    prefix_result_pin, prefix_graph_pin = pin(prefix_result, 2 * 1024**2), pin(prefix_graph, 2 * 1024**2)
    need(prefix_result_pin["sha256"] == PREFIX_RESULT_SHA and prefix_graph_pin["sha256"] == PREFIX_GRAPH_SHA
         and pin(prefix_attempt, 65536)["sha256"] == PREFIX_ATTEMPT_SHA
         and not (PREFIX / "FINALIZATION-FAILED.json").exists(), "UNCHANGED_GRAPH_PREFIX_RECORDS")
    prefix = json.loads(prefix_result.read_bytes())
    need(prefix["status"] == "FAIL" and prefix["error"] == "ValueError: UNSELECTED_FULL_AGGREGATE_GUEST_GRAPH_DELTA"
         and prefix["job"]["active_processes"] == 0 and len(prefix["commands"]) == 1
         and prefix["commands"][0]["label"] == "offline-aggregate-graph"
         and prefix["commands"][0]["exit_code"] == 0 and prefix["commands"][0]["cleanup_errors"] == []
         and prefix["commands"][0]["job_after"]["active_processes"] == 0,
         "FAILED_PREFIX_HAS_ONLY_CLOSED_SUCCESSFUL_GRAPH_NOT_A_BUILD_PASS")
    attempt = HERE / (build_result.parent.name + "-attempt.json")
    attempt_pin = pin(attempt, 65536)
    expected_attempt = {"status": BUILD_PASS, "result_sha256": result_pin["sha256"]}
    need(json.loads(attempt.read_bytes()) == expected_attempt, "TERMINAL_GUEST_BUILD_MARKER")
    failure_marker = build_result.parent / "FINALIZATION-FAILED.json"
    failure_pin = pin(failure_marker, 65536)
    need(failure_pin["sha256"] == COMPILE_FAILURE_SHA
         and validation["preserved_failure"] == {"path": str(failure_marker), "sha256": COMPILE_FAILURE_SHA}
         and json.loads(failure_marker.read_bytes()) == {"status": "FAIL_FINALIZATION",
             "overrides_result_and_attempt": True, "result_sha256": COMPILE_RESULT_SHA,
             "error": "REMAINING_TOTAL_ENVELOPE"}, "ORIGINAL_RESOURCE_FAILURE_MUST_REMAIN_EXPLICIT")
    need(validation["artifact"] == built["artifact"], "READOPTED_EXACT_ARTIFACT")
    user_pin = built["artifact"]["user_elf"]
    user = Path(user_pin["path"])
    need(user == build_result.parent / "target/riscv32im-risc0-zkvm-elf/release/dmkn-aggregate-claim-guest",
         "EXACT_NEW_AGGREGATE_GUEST_ELF")
    expected_user = {key: user_pin[key] for key in ("bytes", "sha256")}
    driver_result = DRIVER_HOME / "RESULT.json"
    need(pin(driver_result, 2 * 1024**2)["sha256"] == DRIVER_RESULT_SHA, "ADOPTED_ASSEMBLER_RESULT")
    driver = json.loads(driver_result.read_bytes())
    need(driver["status"] == "PASS_DRIVER_COMPILE_ONLY", "QUALIFIED_ASSEMBLER")
    executable = Path(driver["executable"]["path"])
    need(executable.parent == DRIVER_HOME, "EXACT_ASSEMBLER_HOME")
    executable_pin = {key: driver["executable"][key] for key in ("bytes", "sha256")}

    def rebind():
        need(pin(validation_result, 2 * 1024**2) == validation_pin
             and not (validation_result.parent / "FINALIZATION-FAILED.json").exists(), "ARTIFACT_READOPTION_CHANGED")
        need(pin(build_result, 2 * 1024**2) == result_pin and pin(user) == expected_user,
             "NEW_AGGREGATE_GUEST_ARTIFACT_CHANGED")
        need(pin(attempt, 65536) == attempt_pin and pin(failure_marker, 65536) == failure_pin,
             "PRESERVED_GUEST_FAILURE_STATE_CHANGED")
        need(pin(prefix_result, 2 * 1024**2) == prefix_result_pin
             and pin(prefix_graph, 2 * 1024**2) == prefix_graph_pin
             and pin(prefix_attempt, 65536)["sha256"] == PREFIX_ATTEMPT_SHA
             and not (PREFIX / "FINALIZATION-FAILED.json").exists(), "RETAINED_GRAPH_PREFIX_CHANGED")
        need(pin(driver_result, 2 * 1024**2)["sha256"] == DRIVER_RESULT_SHA
             and pin(executable, 128 * 1024**2) == executable_pin, "ASSEMBLER_CHANGED")
        need(pin(KERNEL) == KERNEL_PIN, "ADOPTED_KERNEL_CHANGED")

    rebind()
    output.mkdir()
    image = output / "aggregate_image.bin"
    command = [str(executable), "assemble", str(user), str(KERNEL), str(image)]
    save(output / "COMMAND.json", {"argv": command, "cwd": str(ROOT), "timeout_seconds": 60,
         "artifact_validation": {"path": str(validation_result), **validation_pin},
         "guest_build_result": {"path": str(build_result), **result_pin},
         "guest_build_attempt": {"path": str(attempt), **attempt_pin},
         "preserved_resource_failure": {"path": str(failure_marker), **failure_pin},
         "retained_failed_prefix": {"path": str(prefix_result), **prefix_result_pin},
         "retained_successful_graph": {"path": str(prefix_graph), **prefix_graph_pin},
         "user_elf": user_pin, "kernel": {"path": str(KERNEL), **KERNEL_PIN},
         "assembler": driver["executable"], "authority": "ASSEMBLY_ONLY_NOT_ADMISSION"})
    report = {"schema": "DMKN_V5_AGGREGATE_IMAGE_ASSEMBLY_RESULT_V1",
              "status": "FAIL_AGGREGATE_IMAGE_ASSEMBLY", "assembler_calls": 0,
              "guest_executions": 0, "proof_calls": 0, "mathematical_admission": False,
              "prior_resource_failure_preserved": True,
              "artifact_validation_sha256": validation_pin["sha256"]}
    code = 1
    try:
        report["assembler_calls"] = 1
        actual = subprocess.run(command, cwd=ROOT, stdin=subprocess.DEVNULL, capture_output=True,
                                timeout=60, check=False, creationflags=subprocess.CREATE_NO_WINDOW)
        (output / "stdout.txt").write_bytes(actual.stdout)
        (output / "stderr.txt").write_bytes(actual.stderr)
        report["exit_code"] = actual.returncode
        need(len(actual.stdout) <= 65536 and len(actual.stderr) <= 65536, "ASSEMBLER_OUTPUT_BOUND")
        need(actual.returncode == 0 and not actual.stderr, "ASSEMBLER_ZERO_WITHOUT_DIAGNOSTICS")
        match = re.fullmatch(r"COMBINED_IMAGE image_id=([0-9a-f]{64}) bytes=([0-9]+)\r?\n?",
                             actual.stdout.decode("ascii"))
        need(match is not None, "EXACT_ASSEMBLER_IMAGE_RECORD")
        image_pin = pin(image)
        need(int(match[2]) == image_pin["bytes"], "ACTUAL_IMAGE_BYTE_COUNT")
        rebind()
        report.update(status="PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY",
                      image={"path": str(image), **image_pin}, image_id=match[1],
                      image_id_origin="ACTUAL_PINNED_ASSEMBLER_NOT_FILE_SHA256")
        code = 0
    except BaseException as error:
        report["error"] = type(error).__name__ + ": " + str(error)[:2000]
    finally:
        save(output / "RESULT.json", report)
    print(json.dumps(report), flush=True)
    return code


if __name__ == "__main__":
    raise SystemExit(main())

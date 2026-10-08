"""One owner-selected new guest image assembly; no guest execution or proving.

Run only inside the root-selected bounded local-check Job. This adapter uses
the exact previously qualified assembler/kernel and a freshly successful v5
guest build result. A reported image ID is not mathematical admission.
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
DRIVER_HOME = ROOT / "experiments/general-checker-guest-02/driver-build-04"
DRIVER_RESULT_SHA = "d89626da253ade06a4482d6e7f4a7e9aac0f93d360a2eab2f1b39ba25cc8c43a"
KERNEL = ROOT / ("experiments/general-checker-guest-01/host-prepare-01/original/"
                "risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8/risc0/zkos/v1compat/elfs/v1compat.elf")
KERNEL_PIN = {"bytes": 58736,
              "sha256": "9dd8af014a24db3752b9beda71c837f553ff361fc1bca83cc79584bd38ac9de5"}
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
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "CANONICAL_ISOLATED_OWNER_INVOCATION")
    parser = argparse.ArgumentParser()
    parser.add_argument("--guest-result", required=True)
    parser.add_argument("--guest-result-sha256", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    build_result, output = Path(args.guest_result), Path(args.output)
    need(output.is_absolute() and output.is_relative_to(ROOT / "experiments/v5-local-checks")
         and output.resolve() == output and not output.exists(), "FRESH_LOCAL_ASSEMBLY_OUTPUT")
    need(build_result.is_relative_to(ROOT / "experiments/v5-local-checks")
         and build_result.name == "RESULT.json"
         and re.fullmatch(r"guest-build-[0-9]{2}", build_result.parent.name), "NEW_GUEST_BUILD_RESULT")
    result_pin = pin(build_result, 2 * 1024**2)
    need(result_pin["sha256"] == args.guest_result_sha256, "GUEST_RESULT_PIN")
    built = json.loads(build_result.read_bytes())
    need(built["status"] == "PASS_NEW_MODULE_GUEST_CROSS_BUILD_ONLY"
         and built["job"]["active_processes"] == 0
         and built["guest_executions"] == built["proof_calls"] == built["image_assembly_calls"] == 0,
         "ACTUAL_NEW_GUEST_BUILD_PASS_AND_CLOSED")
    user_pin = built["artifact"]["user_elf"]
    user = Path(user_pin["path"])
    need(user == build_result.parent / "target/riscv32im-risc0-zkvm-elf/release/dmkn-module-guest",
         "EXACT_NEW_MODULE_GUEST_ELF")
    expected_user = {key: user_pin[key] for key in ("bytes", "sha256")}
    driver_result = DRIVER_HOME / "RESULT.json"
    need(pin(driver_result, 2 * 1024**2)["sha256"] == DRIVER_RESULT_SHA, "ADOPTED_ASSEMBLER_RESULT")
    driver = json.loads(driver_result.read_bytes())
    need(driver["status"] == "PASS_DRIVER_COMPILE_ONLY", "QUALIFIED_ASSEMBLER")
    executable = Path(driver["executable"]["path"])
    need(executable.parent == DRIVER_HOME, "EXACT_ASSEMBLER_HOME")
    executable_pin = {key: driver["executable"][key] for key in ("bytes", "sha256")}

    def rebind():
        need(pin(build_result, 2 * 1024**2) == result_pin and pin(user) == expected_user,
             "NEW_GUEST_ARTIFACT_CHANGED")
        need(pin(driver_result, 2 * 1024**2)["sha256"] == DRIVER_RESULT_SHA
             and pin(executable, 128 * 1024**2) == executable_pin, "ASSEMBLER_CHANGED")
        need(pin(KERNEL) == KERNEL_PIN, "ADOPTED_KERNEL_CHANGED")

    rebind()
    output.mkdir()
    image = output / "module_image.bin"
    command = [str(executable), "assemble", str(user), str(KERNEL), str(image)]
    save(output / "COMMAND.json", {"argv": command, "cwd": str(ROOT), "timeout_seconds": 60,
         "guest_build_result": {"path": str(build_result), **result_pin},
         "user_elf": user_pin, "kernel": {"path": str(KERNEL), **KERNEL_PIN},
         "assembler": driver["executable"], "authority": "ASSEMBLY_ONLY_NOT_ADMISSION"})
    report = {"status": "FAIL_IMAGE_ASSEMBLY", "assembler_calls": 0, "guest_executions": 0,
              "proof_calls": 0, "mathematical_admission": False}
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
        report.update(status="PASS_NEW_MODULE_IMAGE_ASSEMBLY_ONLY",
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

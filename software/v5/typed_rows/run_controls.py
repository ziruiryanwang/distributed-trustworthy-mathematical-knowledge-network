"""One focused old/new representation comparison; no guest or proof production.

Run only inside a root-selected Run-V5-Check envelope. The selected native test
binary includes retained conditional module positives, not certificate creation
or mathematical admission. Inputs and outputs are never rewritten in place.
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
FIXTURES = {
    "DMKN_TYPED_PACKET": (
        "experiments/v5-local-checks/delta-reprepare-01/evidence/delta-packet.json",
        "54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1"),
    "DMKN_TYPED_AGGREGATE_INPUT": (
        "experiments/v5-local-checks/aggregate-claims-controls-02/evidence/actual-two-delta.bin",
        "7e21d092206b08a9a71231045b8152df4179ee6575cdc5e3afc704ef03c0be58"),
    "DMKN_TYPED_AGGREGATE_EXPECTED": (
        "experiments/v5-local-checks/aggregate-claims-controls-02/evidence/actual-two-delta/stdout.txt",
        "01d7c9cc45a16f520980e80672f90c0a97a69e31e344f748910df5abb24ffd0b"),
}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True)
    parser.add_argument("--binary-sha", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--expected-tests", type=int, required=True)
    args = parser.parse_args()
    need(1 <= args.expected_tests <= 32, "FINITE_EXPECTED_TEST_COUNT")
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, "CANONICAL_ISOLATED_CONTROLS")
    source = Path(__file__).resolve(strict=True)
    need(source.is_relative_to(ROOT / "experiments/v5-local-checks")
         and "sources" in source.parts, "SELECTED_SOURCE_SNAPSHOT")
    binary = Path(args.binary).resolve(strict=True)
    output = Path(args.output).resolve()
    need(binary.is_relative_to(ROOT / "experiments/v5-local-checks")
         and output.is_relative_to(ROOT / "experiments/v5-local-checks")
         and not output.exists(), "EXACT_LOCAL_FRESH_PATHS")
    need(digest(binary) == args.binary_sha, "SELECTED_TEST_BINARY")
    env = {key: os.environ[key] for key in ("SystemRoot", "WINDIR", "ComSpec")
           if key in os.environ}
    need("SystemRoot" in env, "WINDOWS_RUNTIME_ROOT")
    env.update({
        "PATH": str(Path(env["SystemRoot"]) / "System32"),
        "RUST_BACKTRACE": "0",
        # Match the retained native driver's checker-thread stack. This affects
        # only the selected test child, never the machine or future operations.
        "RUST_MIN_STACK": "16777216",
    })
    for key, (relative, sha256) in FIXTURES.items():
        path = ROOT / relative
        need(path.stat().st_size <= 1024**2 and digest(path) == sha256,
             "EXACT_RETAINED_FIXTURE:" + key)
        env[key] = str(path)
    output.mkdir()
    with (output / "stdout.txt").open("xb") as stdout, (
            output / "stderr.txt").open("xb") as stderr:
        # Outer Job owns the cumulative CPU/process limit and final containment.
        # This smaller wall timeout cannot renew the enclosing allowance.
        completed = subprocess.run([str(binary), "--test-threads=1"], cwd=ROOT,
                                   env=env, stdout=stdout, stderr=stderr,
                                   timeout=60, check=False)
    need(digest(binary) == args.binary_sha, "TEST_BINARY_CHANGED")
    for key, (relative, sha256) in FIXTURES.items():
        need(digest(ROOT / relative) == sha256, "FIXTURE_CHANGED:" + key)
    for name in ("stdout.txt", "stderr.txt"):
        need((output / name).stat().st_size <= 1024**2, "CONTROL_LOG_BOUND")
    stdout_text = (output / "stdout.txt").read_text(encoding="utf-8")
    passed = re.findall(r"^test ([A-Za-z0-9_:]+) \.\.\. ok$", stdout_text, re.MULTILINE)
    suite_ok = (
        completed.returncode == 0 and len(passed) == args.expected_tests
        and len(set(passed)) == args.expected_tests
        and (f"test result: ok. {args.expected_tests} passed; 0 failed; "
             "0 ignored; 0 measured; 0 filtered out;") in stdout_text
    )
    report = {
        "schema": "DMKN_TYPED_ROW_CONTROLS_V1",
        "exit_code": completed.returncode,
        "status": "PASS" if suite_ok else "FAIL",
        "passed_tests": passed,
        "test_binary_sha256": args.binary_sha,
        "fixtures": {key: {"path": relative, "sha256": sha256}
                     for key, (relative, sha256) in FIXTURES.items()},
        "authority": "CONDITIONAL_CHECKER_EQUIVALENCE_NOT_CERTIFICATE_OR_GROWTH",
        "guest_calls": 0, "proof_calls": 0,
    }
    with (output / "result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps(report), flush=True)
    return 0 if suite_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

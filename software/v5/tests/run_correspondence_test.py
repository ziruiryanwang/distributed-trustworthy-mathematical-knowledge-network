"""Run the selected standalone correspondence comparison under the outer Job.

No build, guest, kernel, proof, or network call. This adapter makes the immutable
native executable reachable from the shared snapshot-based local supervisor.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
BUILD = HERE / "correspondence-differential-build-01"
BINARY = BUILD / "correspondence_move_differential.exe"
BINARY_SHA = "342e86c233e483e9d59a5c8196c42fad30f355e3b731f7498f14f237f1e7faa4"
FIXTURES = {
    "base": "16963893ecd12a3a44181fd40c328ecb7c6f34551cfd957d30c972c3735b8358",
    "fusion": "217156a2168bab58a712f75ee2e4252b1ccca3ccb525907f19734c090c9d4dd4",
    "fold_map": "636caebafe8265ec30596214a79a66ee400591d044a06ae1303f464da2e30f1b",
    "fusion_map": "0318029911b271407551d76ce96ad4a12a0cd44068150a35d299c8229631fd10",
    "project_summary": "fb8eb0efbffa41cc9a98a2f12d42a5d308be3b8f6e59eff278348ebbc0fae8d8",
}


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def pin(path, maximum, expected):
    need(path.is_absolute() and path.resolve(strict=True) == path
         and path.is_file() and path.stat().st_size <= maximum, "INPUT_FILE_BOUND")
    with path.open("rb") as stream:
        need(hashlib.file_digest(stream, "sha256").hexdigest() == expected, "INPUT_FILE_PIN")


def main():
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize
         and len(sys.argv) == 2, "CANONICAL_ISOLATED_INVOCATION")
    output = Path(sys.argv[1])
    need(output == HERE / "correspondence-differential-run-01/evidence"
         and output.parent.is_dir() and not output.exists(), "FRESH_SELECTED_OUTPUT")
    fixtures = [HERE / "receipt-prepare-01/prepared" / label / "native.json"
                for label in FIXTURES]

    def pins():
        pin(BINARY, 2 * 1024**2, BINARY_SHA)
        for path, expected in zip(fixtures, FIXTURES.values()):
            pin(path, 2 * 1024**2, expected)

    pins()
    # Child inherits the containing Job. The outer supervisor supplies the
    # selected whole-tree CPU/wall/memory/log bounds and process cleanup.
    result = subprocess.run([str(BINARY), str(output), *map(str, fixtures)],
        cwd=ROOT, stdin=subprocess.DEVNULL, check=False,
        creationflags=subprocess.CREATE_NO_WINDOW)
    pins()
    need(result.returncode == 0, "DIFFERENTIAL_NONZERO")
    report_path = output / "RESULT.json"
    need(report_path.is_file() and report_path.stat().st_size <= 1024**2,
         "BOUNDED_ACTUAL_REPORT")
    report = json.loads(report_path.read_bytes())
    need(report["schema"] == "DMKN_CORRESPONDENCE_MOVE_DIFFERENTIAL_V1"
         and report["status"] == "PASS_OLD_NEW_STRUCTURAL_EQUIVALENCE_ONLY"
         and report["positive_cases"] == 5 and report["negative_cases"] == 6
         and len(report["results"]) == 11 and report["kernel_calls"] == 0
         and report["proof_calls"] == 0 and report["mathematical_admission"] is False,
         "EXACT_STRUCTURAL_TEST_CONCLUSION")
    print("PASS_SELECTED_ELEVEN_CASE_DIFFERENTIAL_NOT_GUEST_OR_SPEEDUP", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

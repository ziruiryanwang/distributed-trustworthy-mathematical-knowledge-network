"""Invoke the exact existential harness under the root's bounded outer Job."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
BINARY = HERE / "existential-differential-build-01/existential_differential.exe"
FIXTURES = {
    "receipt-prepare-01/prepared/base/receipt-input.json": "025d2ce3c42cf7eeab00d1e6626d22d59afe495c64232ad2687893eea278d4a8",
    "receipt-prepare-01/prepared/base/receipt-result.json": "51e2b590da76786a69f00dc70842f0ecf2e068199ef4a9a4211f294594a297b1",
    "receipt-prepare-01/prepared/fusion/receipt-input.json": "c24c7cc535a047ec548c58b6983149ec988c4550f64972492a127a05a25f0904",
    "receipt-prepare-01/prepared/fusion/receipt-result.json": "4b1d671c76dcdc374b1dcf15766b0f45f3d5c4e64d3b96ddc4aa4d3e3a86933f",
    "receipt-prepare-01/prepared/fold_map/receipt-input.json": "766034d47509df7ecda7f4293234a06da148377d137d751e4fa1fc224efdf8c8",
    "receipt-prepare-01/prepared/fold_map/receipt-result.json": "a5f44515eb73d6874c9a48fe6fac871f6d5cf33c88ad0d8d006357cf8bd5c868",
    "receipt-prepare-01/prepared/fusion_map/receipt-input.json": "a7e5e42ab9be25c464dcf426c9b538e9f7cce9d619b59d6d401f04b031716082",
    "receipt-prepare-01/prepared/fusion_map/receipt-result.json": "4237af1e925bcae2bb5240412e14e1a1a16ede01c51663f5ba69aa5960544bb6",
    "receipt-prepare-01/prepared/project_summary/receipt-input.json": "905a20c3095830dae32aaf36b27e9392caae3bc8c80ecb3152757b7ecdb2ff11",
    "receipt-prepare-01/prepared/project_summary/receipt-result.json": "925ac0553d528c2cc1461ba2e3b94678edd742ee4499ff06b5214845d8d6d65f",
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
         and len(sys.argv) == 3, "CANONICAL_ISOLATED_INVOCATION")
    output = Path(sys.argv[1])
    binary_sha = sys.argv[2]
    need(output == HERE / "existential-differential-run-01/evidence"
         and output.parent.is_dir() and not output.exists(), "FRESH_SELECTED_OUTPUT")
    need(re.fullmatch(r"[0-9a-f]{64}", binary_sha), "SELECTED_ACTUAL_BINARY_DIGEST")

    def pins():
        pin(BINARY, 128 * 1024**2, binary_sha)
        for name, expected in FIXTURES.items():
            pin(HERE / name, 2 * 1024**2, expected)

    pins()
    # The containing root supervisor supplies whole-tree CPU/wall/memory/log
    # bounds and cleanup. No shell and no separate unlimited child allocation.
    result = subprocess.run([str(BINARY), str(output)], cwd=ROOT,
        stdin=subprocess.DEVNULL, check=False, creationflags=subprocess.CREATE_NO_WINDOW)
    pins()
    need(result.returncode == 0, "EXISTENTIAL_DIFFERENTIAL_NONZERO")
    report_path = output / "RESULT.json"
    need(report_path.is_file() and report_path.stat().st_size <= 2 * 1024**2,
         "BOUNDED_ACTUAL_REPORT")
    report = json.loads(report_path.read_bytes())
    need(report["schema"] == "DMKN_EXISTENTIAL_PROFILE2_DIFFERENTIAL_V1"
         and report["status"] == "PASS_PROFILE2_CHANGED_BOUNDARIES_NOT_GUEST_PROOF_OR_SPEEDUP"
         and len(report["held_projected_cases"]) == 5 and report["relation_calls"] == 13
         and report["native_checker_reached_calls"] == 8 and len(report["relation_refusals"]) == 6
         and report["journal_layout_refusals"] == 9 and len(report["validation_controls"]) == 183
         and report["alternate_checked_proof_same_conclusion"] is True
         and report["value_and_byte_entry_agree_on_base"] is True
         and report["old_journal_projection_is_test_only"] is True
         and report["guest_executions"] == 0 and report["proof_calls"] == 0
         and report["certificate_verification_performed"] is False
         and report["mathematical_admission"] is False, "EXACT_EXISTENTIAL_TEST_CONCLUSION")
    print("PASS_SELECTED_EXISTENTIAL_DIFFERENTIAL_NOT_GUEST_OR_SPEEDUP", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

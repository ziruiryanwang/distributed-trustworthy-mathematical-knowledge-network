"""D17 array-payload continuation; preserve and reuse the audited failed prefix."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
BINARY = HERE / "structural-continuation-build-01/structural_continuation.exe"
PRIOR_SELECTION = HERE / "structural-frontend-run-01/selection.json"
PRIOR_SELECTION_SHA = "8987f8919d619be3d83100880b312e10f3f00d83073020bc50e3f7f0cf59d5b0"
PRIOR_RESULT = HERE / "structural-frontend-run-01/RESULT.json"
PRIOR_RESULT_SHA = "064a59718ccd3ed05a7b6c22f14dc025d4c1f5740ad5109d68f54a372bbcc33f"
PRIOR_STDERR = HERE / "structural-frontend-run-01/command/stderr.txt"
PRIOR_STDERR_SHA = "a9591b55d168d41fc98982e50b998b4e1d542dcfc707cb61014ee9e76045dc03"
FOUNDATION = HERE / "structural-frontend-run-01/evidence/reconstructed-foundation.json"
CANONICAL_SHA = "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"
FOUNDATION_ID = "d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481"


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
    need(output == HERE / "structural-continuation-run-01/evidence"
         and output.parent.is_dir() and not output.exists(), "FRESH_SELECTED_OUTPUT")
    need(re.fullmatch(r"[0-9a-f]{64}", binary_sha), "SELECTED_ACTUAL_BINARY_DIGEST")
    pin(PRIOR_SELECTION, 65536, PRIOR_SELECTION_SHA)
    prior = json.loads(PRIOR_SELECTION.read_bytes())
    need(prior["name"] == "structural-frontend-run-01"
         and len(prior["runtime_pins"]) == 40, "EXACT_PRIOR_RUNTIME_MAP")

    def pins():
        pin(BINARY, 128 * 1024**2, binary_sha)
        pin(PRIOR_SELECTION, 65536, PRIOR_SELECTION_SHA)
        pin(PRIOR_RESULT, 65536, PRIOR_RESULT_SHA)
        pin(PRIOR_STDERR, 16384, PRIOR_STDERR_SHA)
        pin(FOUNDATION, 23313, CANONICAL_SHA)
        # Rebind prior actual binary, exact harness/checker source snapshots,
        # five held inputs and runtime. None of their tests is invoked again.
        total = 0
        for name, digest in prior["runtime_pins"].items():
            path = Path(name)
            pin(path, 128 * 1024**2, digest)
            total += path.stat().st_size
        need(total <= 512 * 1024**2, "BOUNDED_PRIOR_RUNTIME_BYTES")

    pins()
    previous = json.loads(PRIOR_RESULT.read_bytes())
    need(previous["selection_sha256"] == PRIOR_SELECTION_SHA
         and previous["result"]["status"] == "COMMAND_FAILED"
         and previous["result"]["child_exit_code"] == 1
         and previous["result"]["job_closed"] is True
         and previous["result"]["final_job"]["active_processes"] == 0,
         "PRESERVE_PRIOR_ACTUAL_FAILURE")
    need(not (FOUNDATION.parent / "RESULT.json").exists(), "NO_PRIOR_FULL_PASS")
    diagnostic = PRIOR_STDERR.read_text(encoding="utf-8")
    need('changed row-decoding success boundary: Object {"const": Array [Number(0), Array []]' in diagnostic
         and "old=Ok(OwnedExportRow" in diagnostic
         and "invalid type: sequence, expected struct variant" in diagnostic,
         "EXACT_RETAINED_FAILURE_BOUNDARY")
    raw = FOUNDATION.read_bytes()
    need(len(raw) == 23313 and len(json.loads(raw)) == 413, "RETAINED_FOUNDATION_SIZE")
    domain = b"owner-workload-foundation-candidate"
    framed = b"DMKN-V5-MODULE\0" + len(domain).to_bytes(4, "big") + domain
    framed += len(raw).to_bytes(8, "big") + raw
    need(hashlib.sha256(framed).hexdigest() == FOUNDATION_ID, "RETAINED_COMPILED_FOUNDATION_ID")
    # Source/control-flow audit, not a prior overall PASS, establishes the five
    # held cases + 421 foundation controls + first three extras before this panic.
    try:
        result = subprocess.run([str(BINARY), str(output)], cwd=ROOT,
            stdin=subprocess.DEVNULL, check=False, creationflags=subprocess.CREATE_NO_WINDOW)
    finally:
        pins()
    need(result.returncode == 0, "STRUCTURAL_CONTINUATION_NONZERO")
    report_path = output / "RESULT.json"
    need(report_path.is_file() and report_path.stat().st_size <= 65536, "BOUNDED_ACTUAL_REPORT")
    report = json.loads(report_path.read_bytes())
    need(report["schema"] == "DMKN_STRUCTURAL_FRONTEND_CONTINUATION_V1"
         and report["status"] == "PASS_POSITIONAL_ARRAY_FALLBACK_AND_REMAINING_DECODER_CONTROLS"
         and report["prior_held_cases_reused"] == 5
         and report["prior_foundation_refusals_reused"] == 421
         and report["prior_extra_accepted_rows_reused"] == 3
         and report["remaining_accepted_rows"] == 9
         and report["array_payload_controls"] == 6
         and type(report["array_accepted_by_both"]) is int
         and 2 <= report["array_accepted_by_both"] <= 6
         and report["irregular_rows"] == 21
         and type(report["irregular_accepted_by_both"]) is int
         and 0 <= report["irregular_accepted_by_both"] <= 21
         and report["native_kernel_calls"] == 0 and report["guest_executions"] == 0
         and report["proof_calls"] == 0 and report["mathematical_admission"] is False
         and report["speedup_measured"] is False, "EXACT_CONTINUATION_CONCLUSION")
    conclusion = {"status": "PASS_RETAINED_PREFIX_AND_FOUNDATION_BINDING",
        "prior_result_sha256": PRIOR_RESULT_SHA, "prior_overall_status_remains": "COMMAND_FAILED",
        "canonical_bytes": len(raw), "canonical_sha256": CANONICAL_SHA,
        "foundation_id": FOUNDATION_ID, "prior_held_cases_reused": 5,
        "prior_foundation_refusals_reused": 421, "prior_extra_accepted_rows_reused": 3,
        "scope": "Reused audited executed prefix; no repeated kernel, VM, proof or speedup claim."}
    with (output / "retained-prefix-binding.json").open("xb") as stream:
        stream.write((json.dumps(conclusion, sort_keys=True, indent=2) + "\n").encode())
    pins()
    print("PASS_STRUCTURAL_CONTINUATION_WITH_PRIOR_FAILURE_PRESERVED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

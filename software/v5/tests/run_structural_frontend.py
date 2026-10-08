"""Exact D17 decoder/foundation differential under root's bounded outer Job."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
BINARY = HERE / "structural-frontend-build-02/structural_frontend.exe"
FIXTURE_DIR = HERE / "existential-differential-run-01/evidence"
FIXTURES = {
    "base": "ce554d4877e0b865690f565384381a188ce13166e960a55d39106159f46c067c",
    "fusion": "a91fd6f56a33cd441b6300e32e8d0d15f8f7dd8ab0fa9e18c0b57e567173e750",
    "fold_map": "0d79f84ed5e352dafff43bd589e250d81d63d9dab489ae55fd3ef1a9170bb97c",
    "fusion_map": "720103ad10f9f26ff50877d2a5be6b543a750bca32ab4af22e1f7b177b287155",
    "project_summary": "a1b9e297fadd6fb1c0e7ad8e4f46a560f80385f5940c4c9c09df2e5897738696",
}
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
    need(output == HERE / "structural-frontend-run-01/evidence"
         and output.parent.is_dir() and not output.exists(), "FRESH_SELECTED_OUTPUT")
    need(re.fullmatch(r"[0-9a-f]{64}", binary_sha), "SELECTED_ACTUAL_BINARY_DIGEST")

    def pins():
        pin(BINARY, 128 * 1024**2, binary_sha)
        for label, expected in FIXTURES.items():
            pin(FIXTURE_DIR / ("diagnostic-" + label + "-input.json"), 2 * 1024**2, expected)

    pins()
    expected_counts = [{"label": label, "row_decoding_pairs": len(json.loads(
        (FIXTURE_DIR / ("diagnostic-" + label + "-input.json")).read_bytes())["rows"])}
        for label in FIXTURES]
    # Whole-tree limits/closure come from the exact root-selected outer Job.
    # The executable only decodes; no native kernel, VM or proof calls occur.
    try:
        result = subprocess.run([str(BINARY), str(FIXTURE_DIR), str(output)], cwd=ROOT,
            stdin=subprocess.DEVNULL, check=False, creationflags=subprocess.CREATE_NO_WINDOW)
    finally:
        pins()
    need(result.returncode == 0, "STRUCTURAL_DIFFERENTIAL_NONZERO")
    report_path = output / "RESULT.json"
    need(report_path.is_file() and report_path.stat().st_size <= 2 * 1024**2,
         "BOUNDED_ACTUAL_REPORT")
    report = json.loads(report_path.read_bytes())
    need(report["schema"] == "DMKN_STRUCTURAL_FRONTEND_DIFFERENTIAL_V1"
         and report["status"] == "PASS_EXACT_FOUNDATION_AND_OWNED_ROW_EQUIVALENCE_ONLY"
         and report["held_cases"] == expected_counts
         and report["foundation_refusals"] == 421 and report["extra_accepted_rows"] == 12
         and report["irregular_rows"] == 21
         and type(report["irregular_accepted_by_both"]) is int
         and 0 <= report["irregular_accepted_by_both"] <= 21
         and report["foundation_reconstructed_bytes"] == 23313
         and report["native_kernel_calls"] == 0 and report["guest_executions"] == 0
         and report["proof_calls"] == 0 and report["mathematical_admission"] is False
         and report["speedup_measured"] is False, "EXACT_DIFFERENTIAL_CONCLUSION")
    reconstructed = output / "reconstructed-foundation.json"
    pin(reconstructed, 23313, CANONICAL_SHA)
    raw = reconstructed.read_bytes()
    need(len(raw) == 23313 and len(json.loads(raw)) == 413, "FOUNDATION_RECONSTRUCTION_SIZE")
    domain = b"owner-workload-foundation-candidate"
    framed = b"DMKN-V5-MODULE\0" + len(domain).to_bytes(4, "big") + domain
    framed += len(raw).to_bytes(8, "big") + raw
    need(hashlib.sha256(framed).hexdigest() == FOUNDATION_ID, "COMPILED_FOUNDATION_DOMAIN_ID")
    conclusion = {"status": "PASS_COMPILED_FOUNDATION_CANONICAL_AND_DOMAIN_BINDING",
        "canonical_bytes": len(raw), "canonical_sha256": CANONICAL_SHA,
        "foundation_id": FOUNDATION_ID, "held_row_counts": expected_counts,
        "scope": "Decoder/foundation only; no mathematical admission or measured speedup."}
    with (output / "foundation-binding.json").open("xb") as stream:
        stream.write((json.dumps(conclusion, sort_keys=True, indent=2) + "\n").encode())
    print("PASS_SELECTED_STRUCTURAL_FRONTEND_NOT_GUEST_OR_SPEEDUP", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

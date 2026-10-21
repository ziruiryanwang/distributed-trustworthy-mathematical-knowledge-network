"""One bounded RC0/native-W comparison; no guest, receipt or network calls.

Run only through an exact root-selected Run-V5-Check envelope. The supplied
base journal is retained genuine evidence, but this native harness does not
re-verify its receipt and grants no new receipt authority.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
EXPECTED_NAMES = (
    "first_exact_original_refinement", "second_exact_original_refinement",
    "second_uses_exact_first_conclusion", "wrong_semantic_image", "wrong_exact_rank",
    "extra_legacy_rows_field", "proof_count_mismatch", "loose_proof_bvar",
    "free_binder_domain", "unknown_binder_style", "out_of_scope_universe",
    "unsupported_public_successor_level", "unsupported_let", "wrong_composition_argument",
    "nonproposition_theorem_type", "extra_theorem_metadata", "self_reference_not_earlier_local",
    "changed_parent_group_path", "wrong_constant_universe_arity", "unavailable_foundation_constant",
    "imported_definition_is_not_a_sealed_theorem", "missing_import_type_reference_closure",
    "conditional_two_delta_target_closure", "conditional_same_image_member_continuation",
    "aggregate_wrong_parent_image", "aggregate_unestablished_exact_premise", "aggregate_exact_eof",
    "aggregate_old_magic", "frame_length_before_allocation", "duplicate_JSON_field",
    "exact_foundation_signature_projection", "binder_origin_comparison_is_root_only",
    "simultaneous_universe_substitution", "capture_safe_open_under_binder",
    "raw_imax_zero_comparison_is_root_only", "syntactic_beta_redex_refused",
    "source_counter_exact_boundary", "work_counter_exact_boundary",
    "aggregate_source_counter_is_shared", "aggregate_work_counter_is_shared",
)
# Exact ordered refusal subset of the reviewed 40-case contract; never derived
# from the report being evaluated. Private boundary checks are not refusals.
EXPECTED_REFUSALS = tuple(EXPECTED_NAMES[i] for i in (*range(3, 22), *range(24, 30), 35))
FIXTURES = {
    "journal": ("experiments/v5-local-checks/module-base-snapshot-03/evidence/base.expected-journal",
                184, "22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682"),
    "bundle": ("experiments/v5-local-checks/receipt-prepare-01/prepared/base/bundle.json",
               53769, "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926"),
    "foundation": ("product-local/v5-distribution-terminal-i-01/Mathematical Commons v5/assets/foundation/foundation.json",
                   23313, "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"),
}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_fixture(name):
    relative, size, expected = FIXTURES[name]
    path = ROOT / relative
    need(path.stat().st_size == size and digest(path) == expected, "EXACT_RETAINED_FIXTURE:" + name)
    raw = path.read_bytes()
    need(len(raw) == size and hashlib.sha256(raw).hexdigest() == expected, "FIXTURE_READ_CHANGED:" + name)
    return raw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True)
    parser.add_argument("--binary-sha", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--expected-tests", type=int, required=True)
    args = parser.parse_args()
    need(args.expected_tests == len(EXPECTED_NAMES) == 40, "EXACT_EXPECTED_TEST_COUNT")
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "CANONICAL_ISOLATED_CONTROLS")
    source = Path(__file__).resolve(strict=True)
    need(source.is_relative_to(ROOT / "experiments/v5-local-checks")
         and source.parents[3].name == "sources", "SELECTED_SOURCE_SNAPSHOT")
    binary = Path(args.binary).resolve(strict=True)
    output = Path(args.output).resolve()
    need(binary == ROOT / "experiments/v5-local-checks/restricted-composition-build-02/restricted_controls.exe"
         and output.is_relative_to(ROOT / "experiments/v5-local-checks") and not output.exists(),
         "EXACT_LOCAL_FRESH_PATHS")
    need(digest(binary) == args.binary_sha, "SELECTED_CONTROL_BINARY")
    code = source.parents[1]
    sys.path.insert(0, str(code))
    import modules
    from modules import codec, model, native_rows
    from modules import receipt
    from modules.receipt import witness
    from restricted_composition import fixtures
    for module, relative in ((modules, "modules/__init__.py"), (codec, "modules/codec.py"),
            (model, "modules/model.py"), (native_rows, "modules/native_rows.py"),
            (receipt, "modules/receipt/__init__.py"), (witness, "modules/receipt/witness.py"),
            (fixtures, "restricted_composition/fixtures.py")):
        need(Path(module.__file__).resolve(strict=True) == code / relative, "SELECTED_MODULE_ORIGIN:" + relative)
    bundle = codec.parse_json(read_fixture("bundle"))
    foundation = codec.parse_json(read_fixture("foundation"))
    journal = read_fixture("journal")
    need(len(foundation) == 413 and bundle["module"] == codec.module_id(bundle["spec"]), "EXACT_BASIS_SHAPE")
    opening = codec.group_opening(bundle["spec"], 10)
    need(opening == bundle["openings"][10], "EXACT_BINARY_CONGR_OPENING")
    fixture = fixtures.make_fixtures(journal, opening, foundation)
    encoded = codec.canonical(fixture)
    need(len(encoded) <= 4 * 1024**2, "FOUR_FIELD_FIXTURE_BOUND")
    output.mkdir()
    path = output / "fixture.json"
    with path.open("xb") as stream:
        stream.write(encoded)
    fixture_sha = hashlib.sha256(encoded).hexdigest()
    env = {key: os.environ[key] for key in ("SystemRoot", "WINDIR", "ComSpec") if key in os.environ}
    need("SystemRoot" in env, "WINDOWS_RUNTIME_ROOT")
    env.update(PATH=str(Path(env["SystemRoot"]) / "System32"), RUST_BACKTRACE="0")
    with (output / "stdout.txt").open("xb") as stdout, (output / "stderr.txt").open("xb") as stderr:
        # The outer Job owns cumulative resources and kills descendants on any
        # timeout; this timeout cannot renew that enclosing allocation.
        completed = subprocess.run([str(binary), str(path)], cwd=ROOT, env=env,
                                   stdout=stdout, stderr=stderr, timeout=60, check=False)
    need(digest(binary) == args.binary_sha and digest(path) == fixture_sha, "CONTROL_INPUT_CHANGED")
    for name in FIXTURES:
        read_fixture(name)
    for name in ("stdout.txt", "stderr.txt"):
        need((output / name).stat().st_size <= 1024**2, "CONTROL_LOG_BOUND")
    native = json.loads((output / "stdout.txt").read_bytes())
    executed = native.get("executed", [])
    names = [row.get("name") for row in executed if type(row) is dict] if type(executed) is list else []
    refusals = native.get("expected_refusals", [])
    ok = (completed.returncode == 0 and native.get("schema") == "DMKN_RC0_CONTROLS_V1"
          and native.get("status") == "PASS" and native.get("errors") == []
          and type(executed) is list and len(names) == len(executed)
          and all(type(name) is str for name in names)
          and len(names) == args.expected_tests and len(set(names)) == args.expected_tests
          and names == list(EXPECTED_NAMES)
          and native.get("executed_count") == args.expected_tests
          and all(row.get("status") == "PASS" for row in executed)
          and type(refusals) is list and all(type(name) is str and name in names for name in refusals)
          and len(set(refusals)) == len(refusals)
          and refusals == list(EXPECTED_REFUSALS) and len(refusals) == 26
          and native.get("crypto_produced") is False and native.get("global_growth_claim") is False
          and native.get("authority") == "NATIVE_CONDITIONAL_CONTROLS_NOT_RECEIPT_AUTHORITY")
    report = {"schema": "DMKN_RC_CONTROL_RUN_V1", "status": "PASS" if ok else "FAIL",
              "exit_code": completed.returncode, "test_binary_sha256": args.binary_sha,
              "fixture_sha256": fixture_sha, "fixture_bytes": len(encoded), "native": native,
              "fixtures": FIXTURES, "guest_calls": 0, "proof_calls": 0, "network_calls": 0,
              "authority": "CONDITIONAL_REFINEMENT_NOT_RECEIPT_OR_GROWTH"}
    with (output / "result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps(report), flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

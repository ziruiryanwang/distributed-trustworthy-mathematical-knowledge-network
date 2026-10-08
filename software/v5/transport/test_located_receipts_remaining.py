"""Only D19's three unfinished constructor refusals; no passed group rerun.

The predecessor FAIL is preserved. Its five passed groups and executed prefix
remain independently reviewed evidence, not recast as a complete suite PASS.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import formal_features as F
from transport import test_located_receipts as previous

EXPECTED_PREVIOUS = "0103c4a4912fbbcbaead9b5e137685f8bdbd61cf9d1c509c10bb3ca7c81cba20"
EXPECTED_STDERR = "e84c5ffd63cff359fcd3687c6607fe508067f482997edbab4fc86fe7837c626d"


class RemainingControls(previous.LocatedReceiptControls):
    async def test_three_remaining_constructor_refusals(self):
        # charge_external checks each finite preallocation against its entire
        # grant before its aggregate-sum check. Both exact failures are INTEGER_BOUND.
        for label, limits in (("undersized-request-grant", {**previous.ACQUISITION, "requests": 6}),
                              ("undersized-reply-grant", {**previous.ACQUISITION, "reply_bytes": previous.LOCATION["reply_bytes"]-1})):
            with self.subTest(label=label):
                with self.assertRaisesRegex(ValueError, "^INTEGER_BOUND$"):
                    self.workflow(acquisition_limits=limits)
        wrong = {**self.profile, "policy": previous.h("different-policy")}
        with self.assertRaisesRegex(ValueError, "^LOCATED_RECEIPT_INITIAL_NAMESPACE_PROFILE$"):
            self.workflow(wire_profile=wrong)
        self.start.assert_not_called(); self.dial.assert_not_called(); self.spawn.assert_not_called()
        self.assertEqual(self.workflows, []); self.unchanged_stores()


def pinned(path, expected):
    path = Path(path)
    F.need(path.is_absolute() and path.is_file() and path.stat().st_size <= 1048576, "PREVIOUS_EVIDENCE_BOUND")
    with path.open("rb") as stream: raw = stream.read(1048577)
    F.need(len(raw) <= 1048576 and hashlib.sha256(raw).hexdigest() == expected, "PREVIOUS_EVIDENCE_PIN")
    return raw


def main():
    parser = argparse.ArgumentParser()
    for arg in ("evidence", "previous-result", "previous-stderr"): parser.add_argument("--"+arg, required=True)
    args = parser.parse_args(); output = Path(args.evidence)
    F.need(output.is_absolute() and not output.exists(), "FRESH_ABSOLUTE_TEST_EVIDENCE")
    old = json.loads(pinned(args.previous_result, EXPECTED_PREVIOUS))
    stderr = pinned(args.previous_stderr, EXPECTED_STDERR).decode("utf-8")
    F.need(old["status"] == "FAIL" and old["tests_run"] == 6 and old["failures"] == 1
           and old["errors"] == old["skipped"] == 0 and old["mathematical_acceptance"] is False,
           "PREVIOUS_PARTIAL_RESULT")
    F.need(stderr.count(" ... ok") == 5 and '"RECEIPT_AGGREGATE_BUDGET" does not match "INTEGER_BOUND"' in stderr,
           "PREVIOUS_EXACT_FIXTURE_FAILURE")
    output.mkdir(parents=True); previous.EVIDENCE = output
    # Explicit one-case suite: default discovery would inherit/repeat six old
    # test_* methods from the fixture class, which is deliberately forbidden.
    suite = unittest.TestSuite([RemainingControls("test_three_remaining_constructor_refusals")])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"schema": "DMKN_LOCATED_RECEIPT_REMAINING_CONTROLS_V1", "status": "PASS" if result.wasSuccessful() else "FAIL",
        "tests_run": result.testsRun, "remaining_subcontrols": 3, "failures": len(result.failures), "errors": len(result.errors),
        "skipped": len(result.skipped), "adopted_prior_complete_groups": 5, "prior_complete_suite_status": "FAIL_PRESERVED",
        "previous_result_sha256": EXPECTED_PREVIOUS, "previous_stderr_sha256": EXPECTED_STDERR,
        "prior_executed_prefix": "ORIGINAL_DEADLINE_PREPAY_AND_DIFFERENT_DEADLINE_REFUSAL_NOT_RERUN",
        "product_source_changed": False, "mathematical_acceptance": False,
        "genuine_receipt_verification": "NOT_RUN", "actual_dht_or_noise": False,
        "transport_scope": "NO_PROVIDER_SOCKET_DIAL_OR_PROCESS_SPAWN_ALLOWED_BY_TRIPWIRES",
        "fixture_scope": "INHERITED_OWNER_CONSTRUCTORS_SQLITE_AND_MOCKED_READER_NO_ADOPTION"}
    with (output/"RESULT.json").open("xb") as stream: stream.write(F.compact(report))
    print(json.dumps({key: report[key] for key in ("status", "tests_run", "remaining_subcontrols", "failures", "errors")}))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

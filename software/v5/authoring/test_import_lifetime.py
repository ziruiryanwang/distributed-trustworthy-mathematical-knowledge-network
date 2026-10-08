"""Constructor/lifetime/foreign-token controls, never positive verification.

Exact-class fixtures bypass installation adoption and keep empty handle tables.
No receive(), cryptographic success, valid journal or positive module is mocked.
These controls prove only the selected local lifecycle/type refusal behavior.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from admission.verifier import ReceiptVerifier, VerifiedModule
from transport.receipt_client import DeadlineReceiptVerifier
from authoring.imports import ImportSession
from discovery import formal_features as F


def owner(kind=ReceiptVerifier, *, deadline=None, outer=None):
    # This is not an adopted real verifier. All handles remain absent; real
    # _active/report/close/describe methods are exercised, never minting methods.
    value = object.__new__(kind)
    value._deadline = time.monotonic()+60 if deadline is None else deadline
    value._closed = value._busy = False
    value._used = [0, 0, 0]; value._handles = {}
    value._profile_id = hashlib.sha256(b"UNADOPTED_LIFETIME_FIXTURE").hexdigest()
    if kind is DeadlineReceiptVerifier:
        value.outer_deadline = value._deadline if outer is None else outer
    return value


class ImportLifetimeControls(unittest.TestCase):
    def test_exact_owner_types_and_all_deadline_minima(self):
        now = time.monotonic()
        base = owner(deadline=now+10)
        session = ImportSession(base, wall_seconds=60)
        self.assertEqual(session._deadline, base._deadline)
        bounded = owner(DeadlineReceiptVerifier, deadline=now+20, outer=now+8)
        first = ImportSession(bounded, wall_seconds=60)
        self.assertEqual(first._deadline, bounded.outer_deadline)
        actual_earlier = owner(DeadlineReceiptVerifier, deadline=now+4, outer=now+10)
        second = ImportSession(actual_earlier, wall_seconds=60)
        self.assertEqual(second._deadline, actual_earlier._deadline)
        requested_earlier = ImportSession(owner(deadline=now+60), wall_seconds=1)
        self.assertLessEqual(requested_earlier._deadline, time.monotonic()+1)
        for selected in (session, first, second, requested_earlier):
            self.assertEqual(selected.selected_data(), [])
            self.assertEqual(selected._verifier._handles, {})
            self.assertEqual(selected._verifier._used, [0, 0, 0])

    def test_duck_and_arbitrary_subclasses_refuse(self):
        class OtherVerifier(ReceiptVerifier): pass
        class OtherBoundedVerifier(DeadlineReceiptVerifier): pass
        for value in ({"success": True}, object(), object.__new__(OtherVerifier), object.__new__(OtherBoundedVerifier)):
            with self.subTest(kind=type(value).__name__):
                with self.assertRaisesRegex(ValueError, "^IMPORT_OWNER_VERIFIER_REQUIRED$"):
                    ImportSession(value)

    def test_closed_or_expired_verifier_refuses_construction(self):
        closed = owner(); closed.close()
        with self.assertRaisesRegex(ValueError, "^ADMISSION_CLOSED_OR_EXPIRED$"): ImportSession(closed)
        with self.assertRaisesRegex(ValueError, "^ADMISSION_CLOSED_OR_EXPIRED$"):
            ImportSession(owner(deadline=time.monotonic()-1))
        with self.assertRaisesRegex(ValueError, "^RECEIPT_ORIGINAL_DEADLINE$"):
            ImportSession(owner(DeadlineReceiptVerifier, outer=time.monotonic()-1))

    def test_owner_close_revokes_even_empty_session_operations(self):
        for kind in (ReceiptVerifier, DeadlineReceiptVerifier):
            with self.subTest(kind=kind.__name__):
                verifier = owner(kind); session = ImportSession(verifier)
                self.assertEqual(session.selected_data(), [])
                used_calls = session._calls; verifier.close()
                with self.assertRaisesRegex(ValueError, "^ADMISSION_CLOSED_OR_EXPIRED$"): session.selected_data()
                # Liveness must refuse before inspecting deliberately absent
                # authoring inputs, even when no imported module was selected.
                with self.assertRaisesRegex(ValueError, "^ADMISSION_CLOSED_OR_EXPIRED$"):
                    session.make_request(None, None, None)
                self.assertEqual(session._calls, used_calls)
                self.assertEqual(verifier._handles, {}); self.assertEqual(verifier._used, [0, 0, 0])

    def test_session_and_verifier_deadline_remain_independently_live(self):
        verifier = owner(); session = ImportSession(verifier, wall_seconds=10)
        with patch("time.monotonic", return_value=session._deadline+1):
            with self.assertRaisesRegex(ValueError, "^IMPORT_SESSION_CLOSED_OR_EXPIRED$"): session.selected_data()
        # Owner-side invalidation after session construction: a later session
        # timestamp cannot extend the originating verifier's current lifetime.
        verifier._deadline = time.monotonic()-1
        with self.assertRaisesRegex(ValueError, "^ADMISSION_CLOSED_OR_EXPIRED$"): session.selected_data()
        bounded = owner(DeadlineReceiptVerifier); child = ImportSession(bounded, wall_seconds=10)
        bounded.outer_deadline = time.monotonic()-1
        with self.assertRaisesRegex(ValueError, "^RECEIPT_ORIGINAL_DEADLINE$"): child.selected_data()
        separate = owner(); independent = ImportSession(separate); independent.close()
        with self.assertRaisesRegex(ValueError, "^IMPORT_SESSION_CLOSED_OR_EXPIRED$"): independent.selected_data()
        separate._active(); self.assertFalse(separate._closed)

    def test_foreign_and_serialized_tokens_never_register(self):
        for kind in (ReceiptVerifier, DeadlineReceiptVerifier):
            verifier = owner(kind); session = ImportSession(verifier)
            # Public empty token construction is intentionally not sufficient.
            for token in (VerifiedModule(), {"verified": True, "module": "0"*64}, object()):
                with self.subTest(kind=kind.__name__, token=type(token).__name__):
                    with self.assertRaisesRegex(ValueError, "^ADMISSION_FOREIGN_OR_UNKNOWN_HANDLE$"):
                        session.use_handle(token, b"NOT_A_RECEIPT")
            self.assertEqual(session._records, {}); self.assertEqual(session._cache, {})
            self.assertEqual(verifier._handles, {}); self.assertEqual(verifier._used, [0, 0, 0])
            self.assertEqual(session._calls, 3)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--evidence", required=True)
    output = Path(parser.parse_args().evidence)
    F.need(output.is_absolute() and not output.exists(), "FRESH_ABSOLUTE_TEST_EVIDENCE")
    output.mkdir(parents=True)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ImportLifetimeControls))
    report = {"schema": "DMKN_IMPORT_LIFETIME_CONTROLS_V1", "status": "PASS" if result.wasSuccessful() else "FAIL",
        "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "verifier_origin": "UNADOPTED_EXACT_CLASS_LIFETIME_FIXTURES_EMPTY_HANDLE_TABLES",
        "positive_handles_registered": 0, "receive_calls_selected": 0, "mathematical_acceptance": False,
        "genuine_receipt_verification": "NOT_RUN", "source_scope": "IMPORT_TYPE_DEADLINE_LIVENESS_BRIDGE_ONLY"}
    with (output/"RESULT.json").open("xb") as stream: stream.write(F.compact(report))
    print(json.dumps({key: report[key] for key in ("status", "tests_run", "failures", "errors")}))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

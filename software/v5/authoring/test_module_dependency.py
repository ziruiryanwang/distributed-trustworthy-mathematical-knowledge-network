"""New-owner structural/refusal controls; no positive receipt/handle fabrication.

Reuse only the older test's setup/teardown/reply helpers, never its passing suite.
Real cryptographic admission and onward authoring are separate required evidence.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from authoring import test_dependency_acquisition as fixture
from authoring.module_dependency import ModuleDependencyAcquisition
from discovery import formal_features as F
from modules import codec as C


class NewOwnerControls(unittest.IsolatedAsyncioTestCase):
    reply = fixture.DependencyControls.reply
    asyncTearDown = fixture.DependencyControls.asyncTearDown

    async def asyncSetUp(self):
        await fixture.DependencyControls.asyncSetUp(self)
        self.workflow._receipts = self.receipts
        self.workflow.adapter = self.adapter
        self.workflow._profile = deepcopy(self.profile)
        self.new_owner = ModuleDependencyAcquisition(self.workflow, self.session)

    async def prepare(self):
        with self.reply():
            return await self.new_owner.prepare("held-contact", self.module, self.name, 4096)

    async def test_exact_unselected_owner_is_structural_only_and_copied(self):
        requested = deepcopy(self.name)
        def mutate(request):
            requested[0][1] = "changed_after_dispatch"
            self.assertEqual(request["relative_name"], self.name)
        with self.reply(effect=mutate), \
                patch.object(self.adapter, "describe", side_effect=AssertionError("NO_FEATURE_WORK")), \
                patch.object(self.adapter, "resolve", side_effect=AssertionError("NO_CANDIDATE_WORK")):
            result = await self.new_owner.prepare("held-contact", self.module, requested, 4096)
        self.assertEqual(result["locator"]["relative_name"], self.name)
        self.assertFalse(result["mathematical_acceptance"])
        self.assertFalse(result["discovery_candidate_promotion"])
        result["opening"]["group"]["declarations"][0]["name"][0][1] = "changed_return"
        self.assertEqual(self.modules.get_group(self.module, self.name)[0], self.opening)
        held = C.parse_json(self.new_owner._selected[self.module, C.name_key(self.name)])
        self.assertEqual(held["opening"], self.opening)
        self.assertEqual(self.budget.used["requests"], 1)
        self.assertEqual(self.new_owner.report()["retained_selections"], 1)

    async def test_wrong_address_and_corrupted_opening_consume_attempts(self):
        with self.reply():
            with self.assertRaisesRegex(ValueError, "^MODULE_DEPENDENCY_EXACT_ADDRESS$"):
                await self.new_owner.prepare("held-contact", self.module, [["s", "Absent"]], 4096)
        wrong = deepcopy(self.opening)
        wrong["group"]["declarations"][0]["type"] = ["sort", ["succ", ["zero"]]]
        with self.reply(wrong):
            with self.assertRaises(ValueError):
                await self.new_owner.prepare("held-contact", self.module, self.name, 4096)
        self.assertEqual(self.budget.used["requests"], 2)
        self.assertEqual(self.modules.status()["counts"]["groups"], 0)

    async def test_expired_contact_and_session_preserve_shared_costs(self):
        self.contact._expires = time.monotonic()-1
        with self.assertRaisesRegex(ValueError, "^LOCATED_CUSTODY_CONTACT_EXPIRED$"):
            await self.new_owner.prepare("held-contact", self.module, self.name, 4096)
        self.assertEqual(self.budget.used["reply_bytes"], 4096)
        self.contact._expires = self.deadline
        def expire(unused): self.session._deadline = time.monotonic()-1
        with self.reply(effect=expire):
            with self.assertRaisesRegex(ValueError, "^IMPORT_SESSION_CLOSED_OR_EXPIRED$"):
                await self.new_owner.prepare("held-contact", self.module, self.name, 4096)
        self.assertEqual(self.budget.used["requests"], 2)
        self.assertEqual(self.modules.status()["counts"]["groups"], 0)

    async def test_extra_owner_and_contact_identity_changes_refuse(self):
        self.workflow._receipts = object()
        with self.assertRaisesRegex(ValueError, "^MODULE_DEPENDENCY_OWNER_BINDING_CHANGED$"):
            self.new_owner.report()
        self.workflow._receipts = self.receipts
        old = self.acquisition.endpoints["held-contact"]
        self.acquisition.endpoints["held-contact"] = object()
        with self.assertRaisesRegex(ValueError, "^MODULE_DEPENDENCY_CONTACTS_CHANGED$"):
            self.new_owner.report()
        self.acquisition.endpoints["held-contact"] = old
        self.assertEqual(self.budget.used["requests"], 0)

    async def test_retention_and_session_capacity_refuse_before_admission(self):
        bounded = ModuleDependencyAcquisition(self.workflow, self.session, data_bytes=1)
        with self.reply():
            with self.assertRaisesRegex(ValueError, "^MODULE_DEPENDENCY_DATA_CAP$"):
                await bounded.prepare("held-contact", self.module, self.name, 4096)
        self.assertEqual(self.modules.status()["counts"]["groups"], 0)
        await self.prepare()
        self.session._max_modules = 0
        entry = {"receipt_sha256": fixture.digest("NOT_A_RECEIPT"), "receipt_bytes": 1}
        with patch.object(self.acquisition, "admit", side_effect=AssertionError("NO_EXPENSIVE_ADMIT")) as admitted:
            with self.assertRaisesRegex(ValueError, "^MODULE_DEPENDENCY_IMPORT_CAPACITY$"):
                self.new_owner.admit(self.module, self.name, entry, self.root/"never-created")
        admitted.assert_not_called()
        self.assertFalse((self.root/"never-created").exists())

    async def test_missing_receipt_cannot_select_or_launch_verifier(self):
        await self.prepare()
        entry = {"receipt_sha256": fixture.digest("ABSENT_RECEIPT"), "receipt_bytes": 1}
        with patch.object(self.verifier, "receive", side_effect=AssertionError("NO_RECEIPT_TO_VERIFY")) as received:
            with self.assertRaises(ValueError):
                self.new_owner.admit(self.module, self.name, entry, self.root/"never-created")
        received.assert_not_called()
        self.assertFalse(self.verifier._closed)
        self.assertEqual(self.budget.used["verify_attempts"], 0)
        self.assertEqual(self.modules.status()["counts"]["groups"], 1)
        self.assertFalse((self.root/"never-created").exists())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", required=True)
    evidence = Path(parser.parse_args().evidence)
    F.need(evidence.is_absolute() and not evidence.exists(), "FRESH_ABSOLUTE_TEST_EVIDENCE")
    evidence.mkdir(parents=True)
    fixture.EVIDENCE = evidence
    fixture.DETAILS.clear()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NewOwnerControls))
    report = {"schema": "DMKN_MODULE_DEPENDENCY_CONTROLS_V1",
              "status": "PASS" if result.wasSuccessful() else "FAIL", "tests_run": result.testsRun,
              "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
              "mathematical_acceptance": False, "genuine_receipt_verification": "NOT_RUN",
              "positive_handles_registered": 0, "provider_wire": "NO_DIAL_HTTP_FIXTURES_ONLY",
              "old_passing_suite_repeated": False, "details": fixture.DETAILS}
    with (evidence/"RESULT.json").open("xb") as stream: stream.write(F.compact(report))
    print(json.dumps({key: report[key] for key in ("status", "tests_run", "failures", "errors")}))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

"""D20 companion controls: conditional structural plumbing, NEVER admission.

No positive handle, receipt or journal is fabricated. Owner constructors use
empty-registry exact-class fixtures; selected-module/open-group prerequisites
are explicitly mocked ONLY in structural wiring controls. A genuine receipt
and actual live import remain an untested required endpoint.
"""
from pathlib import Path
import argparse
from copy import deepcopy
import hashlib
import json
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from authoring.acquisition import DependencyAcquisition
from authoring.imports import ImportSession
from authoring.test_import_lifetime import owner
from custody.module_store import ModuleStore
from custody.receipt_store import ReceiptStore, public_profile, profile_id
from discovery import formal_features as F
from discovery.module_export_adapter import ModuleExportAdapter
from location.protocol import OwnerEgressPolicy
from modules import codec as C
from transport.located_receipts import LocatedReceiptWorkflow, _ExpiringContact
from transport.receipt_client import AcquisitionBudget, ReceiptAcquisition, DeadlineReceiptVerifier

EVIDENCE = None
DETAILS = {}


def digest(label): return hashlib.sha256(label.encode("ascii")).hexdigest()


class DependencyControls(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.root = EVIDENCE/self._testMethodName; self.root.mkdir()
        self.name = [["s", "Dependency"]]
        structural_type = ["sort", ["zero"]]
        if self._testMethodName == "test_conditional_structural_success_copies_address_and_never_extracts_features":
            nodes = [["const", ["foundation", [["s", "UnadoptedSymbol"+str(i)]]], []] for i in range(140)]
            while len(nodes) > 1:
                nodes = [["app", nodes[i], nodes[i+1]] if i+1 < len(nodes) else nodes[i]
                         for i in range(0, len(nodes), 2)]
            structural_type = nodes[0]
        self.spec = {"schema": C.SPEC_SCHEMA, "foundation": digest("D20_NONPROOF_FOUNDATION"),
            "policy": digest("D20_NONPROOF_POLICY"), "groups": [{"kind": "ordinary", "declarations": [
                {"name": self.name, "kind": "theorem", "universes": 0,
                 "type": structural_type, "value_hash": None, "meta": {}}]}]}
        # Structurally valid descriptor; no mathematical validity is asserted.
        self.module = C.module_id(self.spec); self.opening = C.group_opening(self.spec, 0)
        self.summary = C.summarize(self.spec); self.deadline = time.monotonic()+40
        self.adapter = ModuleExportAdapter(C, self.spec["foundation"], self.spec["policy"])
        self.profile = public_profile(digest("D20_NONPROOF_IMAGE"), self.spec["foundation"], self.spec["policy"])
        self.verifier = owner(DeadlineReceiptVerifier, deadline=self.deadline, outer=self.deadline)
        self.verifier.wire_profile_id = profile_id(self.profile)
        self.session = ImportSession(self.verifier)
        self.modules = ModuleStore(self.root/"modules", C, self.spec["foundation"], self.spec["policy"],
            dict(modules=4, groups=8, declarations=16, bodies=8, logical_bytes=1048576, db_pages=256), create=True)
        self.receipts = ReceiptStore(self.root/"receipts", self.profile,
            dict(receipts=4, offers=8, offers_per_module=2, receipt_bytes=4096,
                 logical_bytes=65536, db_pages=256), create=True)
        self.budget = AcquisitionBudget(self.deadline, dict(requests=8, reply_bytes=65536,
            verify_attempts=1, verification_input_bytes=4096, worker_cpu_seconds=10))
        self.policy = OwnerEgressPolicy({"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test",
            "public_ports": [], "test_endpoints": [{"host": "127.0.0.1", "port": 43210}]})
        endpoint = self.policy.endpoint({"host": "127.0.0.1", "port": 43210,
                                        "tls": False, "server_name": None})
        self.contact = _ExpiringContact(endpoint, self.deadline, self.policy, self.budget)
        self.acquisition = ReceiptAcquisition(self.adapter, {"held-contact": self.contact}, self.profile,
            self.budget, self.modules, self.receipts, verifier=self.verifier)
        # Exact wrapper shape only, not a completed authenticated location run.
        self.workflow = object.__new__(LocatedReceiptWorkflow)
        self.workflow.deadline = self.deadline; self.workflow.budget = self.budget
        self.workflow._modules = self.modules; self.workflow._verifier = self.verifier
        self.workflow._acquisition = self.acquisition
        self.workflow.phase = "ACQUIRING"; self.workflow.closed = False
        self.workflow._search = SimpleNamespace(session=SimpleNamespace(seen_candidates={}))
        self.companion = DependencyAcquisition(self.workflow, self.session)
        self.dial = AsyncMock(side_effect=AssertionError("UNEXPECTED_PROVIDER_DIAL"))
        self.spawn = AsyncMock(side_effect=AssertionError("UNEXPECTED_PROCESS_SPAWN"))
        self.patches = [patch("asyncio.open_connection", self.dial),
                        patch("asyncio.create_subprocess_exec", self.spawn)]
        for item in self.patches: item.start()

    async def asyncTearDown(self):
        try:
            self.dial.assert_not_called(); self.spawn.assert_not_called()
            self.assertEqual(self.verifier._handles, {}); self.assertEqual(self.verifier._used, [0, 0, 0])
            self.assertEqual(self.session._records, {}); self.assertEqual(self.session._groups, {})
            self.assertEqual(self.workflow._search.session.seen_candidates, {})
            self.assertIsNone(self.budget.pending)
            DETAILS[self._testMethodName] = {"budget": self.budget.report(),
                "custody": self.modules.status(), "mocked_authority_is_not_admission": True}
        finally:
            for item in reversed(self.patches): item.stop()
            self.session.close(); self.verifier.close(); self.modules.close(); self.receipts.close()

    def selected(self):
        # Explicit conditional prerequisite, not an actual registered handle.
        return patch.object(self.session, "_describe", return_value={"summary": deepcopy(self.summary)})

    def reply(self, opening=None, effect=None):
        raw = C.canonical(self.opening if opening is None else opening)
        async def exchange(endpoint, route, request, maximum, timeout):
            endpoint.validate()
            self.assertEqual(route, "/v5/modules/group")
            self.assertEqual(request["module_id"], self.module)
            self.assertIsNone(request["group_index"])
            self.assertLessEqual(len(raw), maximum)
            if effect is not None: effect(request)
            return {"status": 200, "raw": raw, "request_bytes": len(F.compact(request)),
                    "reply_bytes": len(raw), "header_bytes": 0, "elapsed_ms": 0}
        return patch("transport.clients.exchange", side_effect=exchange)

    async def test_real_unselected_foreign_and_exact_owner_refusals(self):
        with self.assertRaisesRegex(ValueError, "^IMPORT_UNSELECTED_MODULE$"):
            await self.companion.declaration("held-contact", self.module, self.name, 4096)
        foreign = ImportSession(owner(DeadlineReceiptVerifier, deadline=self.deadline, outer=self.deadline))
        with self.assertRaisesRegex(ValueError, "^DEPENDENCY_SAME_LIVE_VERIFIER$"):
            DependencyAcquisition(self.workflow, foreign)
        with self.assertRaisesRegex(ValueError, "^DEPENDENCY_EXACT_OWNER_TYPES$"):
            DependencyAcquisition({"verified": True}, self.session)
        foreign.close()
        self.assertEqual(self.budget.used["requests"], 0)

    async def test_owner_identity_and_session_deadline_refuse_before_dispatch(self):
        self.workflow._modules = object()
        with self.assertRaisesRegex(ValueError, "^DEPENDENCY_OWNER_BINDING_CHANGED$"):
            self.companion._active()
        self.workflow._modules = self.modules
        self.workflow.deadline += 1
        with self.assertRaisesRegex(ValueError, "^DEPENDENCY_ORIGINAL_DEADLINE$"):
            self.companion._active()
        self.workflow.deadline = self.deadline
        self.session._deadline = time.monotonic()-1
        with self.assertRaisesRegex(ValueError, "^IMPORT_SESSION_CLOSED_OR_EXPIRED$"):
            await self.companion.declaration("held-contact", self.module, self.name, 4096)
        self.assertEqual(self.budget.used["requests"], 0)

    async def test_conditional_structural_success_copies_address_and_never_extracts_features(self):
        # Establish the exact changed discriminator: this synthetic structural
        # type exceeds discovery's feature cap, not the group codec's limits.
        raw_export = self.adapter.encode_opening(self.module, self.name, self.opening)
        with self.assertRaisesRegex(ValueError, "^EXPORT_FEATURE_PROFILE_EXHAUSTED$"):
            self.adapter.describe(raw_export)
        requested = deepcopy(self.name)
        def mutate(request):
            requested[0][1] = "MUTATED_AFTER_DISPATCH"
            self.assertEqual(request["relative_name"], self.name)
        def conditional_open(module, opening):
            held, descriptor = self.modules.get_group(module, self.name)
            self.assertEqual(held, opening); self.assertEqual(descriptor["name"], self.name)
            return C.verify_group_opening(module, opening)
        with self.selected(), self.reply(effect=mutate), \
                patch.object(self.session, "open_group", side_effect=conditional_open) as opened, \
                patch.object(self.adapter, "describe", side_effect=AssertionError("DISCOVERY_FEATURE_WORK")), \
                patch.object(self.adapter, "resolve", side_effect=AssertionError("DISCOVERY_RESOLVE_WORK")):
            result = await self.companion.declaration("held-contact", self.module, requested, 32768)
        opened.assert_called_once()
        self.assertEqual(result["locator"]["relative_name"], self.name)
        self.assertFalse(result["mathematical_acceptance"])
        self.assertFalse(result["discovery_candidate_promotion"])
        self.assertFalse(result["cross_component_atomic"])
        result["opening"]["group"]["declarations"][0]["name"][0][1] = "MUTATED_RETURN"
        self.assertEqual(self.modules.get_group(self.module, self.name)[0], self.opening)
        self.assertEqual(self.budget.used["requests"], 1)
        self.assertEqual(self.budget.used["reply_bytes"], len(C.canonical(self.opening)))

    async def test_conditional_wrong_address_and_corrupt_opening_remain_charged(self):
        with self.selected(), self.reply(), patch.object(self.session, "open_group") as opened:
            with self.assertRaisesRegex(ValueError, "^DEPENDENCY_EXACT_SELECTED_ADDRESS$"):
                await self.companion.declaration("held-contact", self.module, [["s", "Absent"]], 4096)
            opened.assert_not_called()
        corrupted = deepcopy(self.opening)
        corrupted["group"]["declarations"][0]["name"] = [["s", "Tampered"]]
        with self.selected(), self.reply(corrupted), patch.object(self.session, "open_group") as opened:
            with self.assertRaises(ValueError):
                await self.companion.declaration("held-contact", self.module, self.name, 4096)
            opened.assert_not_called()
        wrong_summary = deepcopy(self.summary); wrong_summary["group_count"] += 1
        with patch.object(self.session, "_describe", return_value={"summary": wrong_summary}), \
                self.reply(), patch.object(self.session, "open_group") as opened:
            with self.assertRaisesRegex(ValueError, "^DEPENDENCY_EXACT_SELECTED_SUMMARY$"):
                await self.companion.declaration("held-contact", self.module, self.name, 4096)
            opened.assert_not_called()
        self.assertEqual(self.budget.used["requests"], 3)
        self.assertEqual(self.modules.status()["counts"]["groups"], 0)

    async def test_ttl_predial_and_postreply_session_expiry_preserve_shared_charges(self):
        self.contact._expires = time.monotonic()-1
        with self.selected(), patch.object(self.session, "open_group") as opened:
            with self.assertRaisesRegex(ValueError, "^LOCATED_CUSTODY_CONTACT_EXPIRED$"):
                await self.companion.declaration("held-contact", self.module, self.name, 4096)
            opened.assert_not_called()
        self.assertEqual(self.budget.used["requests"], 1)
        self.assertEqual(self.budget.used["reply_bytes"], 4096)
        self.contact._expires = self.deadline
        def expire(unused): self.session._deadline = time.monotonic()-1
        with self.selected(), self.reply(effect=expire), patch.object(self.session, "open_group") as opened:
            with self.assertRaisesRegex(ValueError, "^IMPORT_SESSION_CLOSED_OR_EXPIRED$"):
                await self.companion.declaration("held-contact", self.module, self.name, 4096)
            opened.assert_not_called()
        self.assertEqual(self.budget.used["requests"], 2)
        self.assertEqual(self.budget.used["reply_bytes"], 4096+len(C.canonical(self.opening)))
        self.assertEqual(self.modules.status()["counts"]["groups"], 0)

    async def test_late_open_or_readback_refusal_leaves_only_structural_custody(self):
        with self.selected(), self.reply(), \
                patch.object(self.session, "open_group", side_effect=ValueError("CONDITIONAL_OPEN_REFUSED")):
            with self.assertRaisesRegex(ValueError, "^CONDITIONAL_OPEN_REFUSED$"):
                await self.companion.declaration("held-contact", self.module, self.name, 4096)
        self.assertEqual(self.modules.status()["counts"]["groups"], 1)
        held, descriptor = self.modules.get_group(self.module, self.name)
        wrong = deepcopy(descriptor); wrong["universes"] = 1
        with self.selected(), self.reply(), patch.object(self.modules, "get_group", return_value=(held, wrong)), \
                patch.object(self.session, "open_group") as opened:
            with self.assertRaisesRegex(ValueError, "^DEPENDENCY_GROUP_COMMIT_READBACK$"):
                await self.companion.declaration("held-contact", self.module, self.name, 4096)
            opened.assert_not_called()
        self.assertEqual(self.modules.get_group(self.module, self.name), (held, descriptor))
        self.assertEqual(self.budget.used["requests"], 2)


def main():
    global EVIDENCE
    parser = argparse.ArgumentParser(); parser.add_argument("--evidence", required=True)
    EVIDENCE = Path(parser.parse_args().evidence)
    F.need(EVIDENCE.is_absolute() and not EVIDENCE.exists(), "FRESH_ABSOLUTE_TEST_EVIDENCE")
    EVIDENCE.mkdir(parents=True)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(DependencyControls))
    report = {"schema": "DMKN_DEPENDENCY_ACQUISITION_CONTROLS_V1",
        "status": "PASS" if result.wasSuccessful() else "FAIL", "tests_run": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "mathematical_acceptance": False, "genuine_receipt_verification": "NOT_RUN",
        "positive_handles_registered": 0, "actual_authenticated_location": "NOT_RUN",
        "structural_success_prerequisites": "EXPLICITLY_MOCKED_SELECTED_SUMMARY_AND_OPEN_CALLBACK_NO_AUTHORITY",
        "provider_wire": "NO_PROVIDER_DIAL_HTTP_REPLY_FIXTURES_ONLY", "details": DETAILS}
    with (EVIDENCE/"RESULT.json").open("xb") as stream: stream.write(F.compact(report))
    print(json.dumps({key: report[key] for key in ("status", "tests_run", "failures", "errors")}))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

"""Focused D19 composition controls, NOT a real location or certificate run.

Real wrapper/store/HTTP preflight code; seeded owner-local contacts/candidates;
mocked reader start/close; dial and process tripwires. No DHT/Noise, socket, Node
or verifier process is permitted. Synthetic receipt bytes remain nonauthority.
"""
from pathlib import Path
import argparse
import json
import sys
import time
import unittest
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import formal_features as F
from discovery.module_export_adapter import ModuleExportAdapter
from custody.module_store import ModuleStore
from custody.receipt_store import ReceiptStore, public_profile, receipt_digest
from location import protocol as P
from location.controller import AdoptedLocationRuntime, SOURCE_NAMES
from location.controller_services import ServiceLocationProcess, ROLE_NAMES
from transport.located_receipts import LocatedReceiptWorkflow
from transport.test_receipt_contract import fixture, h, STORE_LIMITS, MODULE_LIMITS, OPAQUE, C

EVIDENCE = None
DETAILS = {}
SEARCH = dict(providers=1, snapshots=1, requests=3, pages=1, examined=8,
              candidates=4, bytes=16384, wall_ms=20000, inflight=1)
LOCATION = dict(wall_ms=30000, route_operations=2, routing_events=16,
                routing_peer_slots=4, descriptor_requests=2, contacts=1, reply_bytes=24576)
ACQUISITION = dict(requests=9, reply_bytes=65536, verify_attempts=1,
                   verification_input_bytes=4096, worker_cpu_seconds=30)


class LocatedReceiptControls(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.root = EVIDENCE/self._testMethodName; self.root.mkdir()
        self.spec, self.expression, self.digest = fixture()
        self.module = C.module_id(self.spec); self.name = [["s", "Example"]]
        self.adapter = ModuleExportAdapter(C, self.spec["foundation"], self.spec["policy"])
        self.record = self.adapter.extract(self.adapter.encode_opening(self.module, self.name, C.group_opening(self.spec, 0)))
        self.features = [self.record["features"][0]]
        self.profile = public_profile(h("synthetic-no-admission-image"), self.spec["foundation"], self.spec["policy"])
        self.entry = {"receipt_sha256": receipt_digest(OPAQUE), "receipt_bytes": len(OPAQUE)}
        self.modules = ModuleStore(self.root/"modules", C, self.spec["foundation"], self.spec["policy"], MODULE_LIMITS, create=True)
        self.receipts = ReceiptStore(self.root/"receipts", self.profile, STORE_LIMITS, create=True)
        self.policy_config = {"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test",
            "public_ports": [], "test_endpoints": [{"host": "127.0.0.1", "port": 43210}]}
        self.policy = P.OwnerEgressPolicy(self.policy_config)
        self.endpoint = self.policy.endpoint({"host": "127.0.0.1", "port": 43210, "tls": False, "server_name": None})
        self.deadline = time.monotonic()+60
        # Shape-only owner constructors. These deliberately unverified reference
        # hashes are never adopted or executed; the verify/start tripwires below
        # prohibit accidentally turning this fixture into a Node/runtime test.
        source = Path(__file__).resolve().parents[1]/"location"
        self.adoption = AdoptedLocationRuntime(source, {name: h("UNVERIFIED_FIXTURE:"+name) for name in SOURCE_NAMES})
        config = {"schema": "DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", "role": "reader",
                  "namespace": self.adapter.namespace, "egress": self.policy_config}
        self.channel = ServiceLocationProcess(self.adoption, {name: h("UNVERIFIED_FIXTURE:"+name) for name in ROLE_NAMES},
                                               config, self.root/"never-started-controller", deadline=self.deadline)
        self.dial = AsyncMock(side_effect=AssertionError("UNEXPECTED_SOCKET_DIAL"))
        self.spawn = AsyncMock(side_effect=AssertionError("UNEXPECTED_PROCESS_SPAWN"))
        self.start = AsyncMock(return_value={"role": "reader", "fixture": "NO_AUTHENTICATED_CHANNEL"})
        self.close = AsyncMock(return_value=None)
        self.patches = [patch("asyncio.open_connection", self.dial), patch("asyncio.create_subprocess_exec", self.spawn),
            patch.object(self.channel, "start", self.start), patch.object(self.channel, "close", self.close),
            patch.object(self.adoption, "verify", side_effect=AssertionError("UNEXPECTED_RUNTIME_ADOPTION"))]
        for pending in self.patches: pending.start()
        self.workflows = []

    async def asyncTearDown(self):
        try:
            for workflow in self.workflows:
                await workflow.close()
            self.dial.assert_not_called(); self.spawn.assert_not_called()
            self.assertIsNone(self.channel.process); self.assertIsNone(self.channel._spawn_task)
            self.assertFalse((self.root/"never-started-controller").exists())
        finally:
            for pending in reversed(self.patches): pending.stop()
            self.modules.close(); self.receipts.close()

    def workflow(self, **changes):
        args = dict(deadline=self.deadline, channel=self.channel, adapter=self.adapter, features=self.features,
                    policy=self.policy, location_limits=LOCATION, search_limits=SEARCH, acquisition_limits=ACQUISITION,
                    wire_profile=self.profile, module_custody=self.modules, receipt_custody=self.receipts)
        args.update(changes); result = LocatedReceiptWorkflow(**args)
        self.workflows.append(result); return result

    async def searchable(self):
        workflow = self.workflow(); await workflow.start()
        # Explicit nonauthentic fixture seeding: no route/descriptor success is
        # asserted. Public begin_search/acquisition still run their real checks.
        underlying = workflow.location._workflow
        self.contact = h("fixture-contact-not-authenticated")
        self.expires = time.monotonic()+10
        underlying._contacts[self.contact] = self.endpoint
        underlying._expiries[self.contact] = self.expires
        workflow.begin_search()
        workflow._search.session.seen_candidates[(self.record["object_id"], F.record_id(self.record))] = True
        return workflow

    def unchanged_stores(self):
        self.assertEqual(self.modules.status()["counts"], dict(modules=0, groups=0, declarations=0, bodies=0, logical_bytes=0))
        self.assertEqual(self.receipts.status()["counts"], dict(receipts=0, offers=0, logical_bytes=0))

    def charged_rejections(self, workflow):
        report = workflow.report(); budget = report["budget"]
        self.assertEqual(budget["used"]["requests"], 9)
        self.assertEqual(budget["used"]["reply_bytes"], LOCATION["reply_bytes"]+self.record["object_bytes"]+len(OPAQUE))
        self.assertEqual(budget["pending_requests"], 0); self.assertEqual(budget["reserved_reply_bytes"], 0)
        self.assertEqual(budget["used"]["verify_attempts"], 0)
        self.assertEqual(report["acquisition"]["structural_http"]["failures"], 1)
        self.assertEqual(report["acquisition"]["receipt_http"]["failed_requests"], 1)
        self.dial.assert_not_called(); self.dial.assert_not_awaited(); self.unchanged_stores()
        DETAILS[self._testMethodName] = report

    async def test_original_deadline_and_upfront_prepaid_grants(self):
        workflow = self.workflow()
        self.assertEqual(workflow.deadline, self.deadline); self.assertEqual(workflow.budget.deadline, self.deadline)
        self.assertLessEqual(workflow.location.deadline, self.deadline)
        report = workflow.report(); self.assertEqual(report["phase"], "CREATED")
        self.assertEqual(report["budget"]["used"]["requests"], 2+2+3)
        self.assertEqual(report["budget"]["used"]["reply_bytes"], LOCATION["reply_bytes"])
        self.assertEqual(report["location"]["workflow"]["search_reply_allocation"], SEARCH["bytes"])
        self.start.assert_not_called()
        with self.assertRaisesRegex(ValueError, "LOCATED_RECEIPT_FRESH_READER"):
            self.workflow(deadline=self.deadline-1)
        with self.assertRaisesRegex(ValueError, "RECEIPT_AGGREGATE_BUDGET"):
            self.workflow(acquisition_limits={**ACQUISITION, "requests": 6})
        with self.assertRaisesRegex(ValueError, "RECEIPT_AGGREGATE_BUDGET"):
            self.workflow(acquisition_limits={**ACQUISITION, "reply_bytes": LOCATION["reply_bytes"]-1})
        wrong = {**self.profile, "policy": h("different-policy")}
        with self.assertRaisesRegex(ValueError, "LOCATED_RECEIPT_INITIAL_NAMESPACE_PROFILE"):
            self.workflow(wire_profile=wrong)
        self.unchanged_stores(); DETAILS[self._testMethodName] = report

    async def test_exact_candidate_and_one_phase_transition(self):
        workflow = await self.searchable()
        self.assertLessEqual(workflow._search.session.deadline, self.deadline)
        workflow._search.session.pending[999] = {"fixture": "not-a-request"}
        try:
            with self.assertRaisesRegex(ValueError, "LOCATED_RECEIPT_PENDING_SEARCH"):
                workflow.begin_acquisition()
        finally: del workflow._search.session.pending[999]
        transitioned = workflow.begin_acquisition()
        self.assertEqual(transitioned["contacts"], [self.contact])
        self.assertIs(workflow._acquisition.budget, workflow.budget)
        before = dict(workflow.budget.used)
        with self.assertRaisesRegex(ValueError, "LOCATED_RECEIPT_PHASE:ACQUIRING"): workflow.begin_acquisition()
        with self.assertRaisesRegex(ValueError, "LOCATED_RECEIPT_PHASE:ACQUIRING"): workflow.begin_search()
        altered = {**self.record, "object_sha256": h("different-record-same-object")}
        with self.assertRaisesRegex(ValueError, "LOCATED_RECEIPT_CANDIDATE_NOT_RETURNED_BY_THIS_SEARCH"):
            await workflow.export(self.contact, altered)
        self.assertEqual(workflow.budget.used, before)
        # The exact record passes the candidate gate and reaches the independent
        # TTL guard. A false blanket refusal would produce the wrong exception.
        with patch("time.monotonic", return_value=self.expires+1):
            with self.assertRaisesRegex(ValueError, "LOCATED_CUSTODY_CONTACT_EXPIRED"):
                await workflow.export(self.contact, self.record)
        self.assertEqual(workflow.budget.used["requests"], 8)
        self.assertIsNone(workflow.budget.pending); self.unchanged_stores()
        DETAILS[self._testMethodName] = workflow.report()

    async def test_expiry_after_transition_refuses_both_dials_and_charges(self):
        workflow = await self.searchable(); workflow.begin_acquisition()
        advanced = self.expires+1
        self.assertLess(advanced, workflow.deadline)
        self.assertLess(advanced, workflow.location.deadline)
        with patch("time.monotonic", return_value=advanced):
            with self.assertRaisesRegex(ValueError, "LOCATED_CUSTODY_CONTACT_EXPIRED"):
                await workflow.export(self.contact, self.record)
            with self.assertRaisesRegex(ValueError, "LOCATED_CUSTODY_CONTACT_EXPIRED"):
                await workflow.receipt(self.contact, self.module, self.entry)
            with self.assertRaisesRegex(ValueError, "RECEIPT_AGGREGATE_BUDGET"):
                await workflow.receipt_offers(self.contact, self.module)
        self.charged_rejections(workflow)

    async def test_owner_egress_invalidation_after_transition_refuses_both(self):
        workflow = await self.searchable(); workflow.begin_acquisition()
        self.assertLess(time.monotonic(), self.expires)
        # Owner fixture mutation only; this is NOT a shipped policy-rotation API.
        # The already-created guard references the same owner policy object.
        self.policy._tests = frozenset()
        with self.assertRaisesRegex(ValueError, "LOCATION_TEST_ENDPOINT_NOT_ALLOWED"):
            await workflow.export(self.contact, self.record)
        with self.assertRaisesRegex(ValueError, "LOCATION_TEST_ENDPOINT_NOT_ALLOWED"):
            await workflow.receipt(self.contact, self.module, self.entry)
        self.charged_rejections(workflow)

    async def test_original_deadline_refuses_before_new_attempt(self):
        workflow = await self.searchable(); workflow.begin_acquisition()
        before = dict(workflow.budget.used)
        with patch("time.monotonic", return_value=workflow.deadline+1):
            with self.assertRaisesRegex(ValueError, "RECEIPT_WORKFLOW_CLOSED_OR_EXPIRED"):
                await workflow.export(self.contact, self.record)
            with self.assertRaisesRegex(ValueError, "RECEIPT_WORKFLOW_CLOSED_OR_EXPIRED"):
                await workflow.receipt(self.contact, self.module, self.entry)
        self.assertEqual(workflow.budget.used, before); self.assertIsNone(workflow.budget.pending)
        self.dial.assert_not_awaited(); self.unchanged_stores()

    async def test_close_revokes_work_and_does_not_own_durable_stores(self):
        workflow = await self.searchable(); workflow.begin_acquisition()
        await workflow.close(); await workflow.close()
        self.close.assert_awaited_once(); self.assertTrue(workflow.closed); self.assertTrue(workflow.budget.closed)
        self.assertEqual(workflow.phase, "CLOSED")
        with self.assertRaisesRegex(ValueError, "RECEIPT_WORKFLOW_CLOSED_OR_EXPIRED"):
            await workflow.receipt(self.contact, self.module, self.entry)
        self.unchanged_stores()


def main():
    global EVIDENCE
    parser = argparse.ArgumentParser(); parser.add_argument("--evidence", required=True)
    EVIDENCE = Path(parser.parse_args().evidence)
    if not EVIDENCE.is_absolute() or EVIDENCE.exists(): raise ValueError("FRESH_ABSOLUTE_TEST_EVIDENCE")
    EVIDENCE.mkdir(parents=True)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(LocatedReceiptControls))
    report = {"schema": "DMKN_LOCATED_RECEIPT_COMPOSITION_CONTROLS_V1", "status": "PASS" if result.wasSuccessful() else "FAIL",
        "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "details": DETAILS, "contact_and_candidate_origin": "SEEDED_UNAUTHENTICATED_OWNER_FIXTURES",
        "reader_lifecycle": "MOCKED_NO_RUNTIME_ADOPTION", "socket_and_process_policy": "TRIPWIRE_NO_CALL_ALLOWED",
        "policy_mutation": "TEST_FIXTURE_ONLY_NOT_SHIPPED_ROTATION_API", "mathematical_acceptance": False,
        "genuine_receipt_verification": "NOT_RUN", "actual_dht_or_noise": False}
    with (EVIDENCE/"RESULT.json").open("xb") as stream: stream.write(F.compact(report))
    print(json.dumps({key: report[key] for key in ("status", "tests_run", "failures", "errors", "mathematical_acceptance")}))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

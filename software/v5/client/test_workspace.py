"""Focused workspace/lifetime controls, with explicitly synthetic cache owners.

No constructor for a mathematical verifier is invoked; no Lean, receipt,
native checker, Node or proof operation runs. Cache controls call the undecorated
method against a test-only stub: they do not create valid mathematical authority.
"""
import argparse
import asyncio
from copy import deepcopy
import json
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

V5 = Path(__file__).resolve().parents[1]
if __name__ == "__main__": sys.path[:0] = [str(V5/"portable_runtime"), str(V5)]
from client.workspace import Workspace, CommonsClient, SCHEMA, LiveWarrant, PartialPublicationError
from frontier_network.custody import public_profile
from mixed_claims.packet import Envelope
from dataclasses import asdict

EVIDENCE = None


def configuration():
    return {"schema": SCHEMA, "wire_profile": public_profile(),
            "module_limits": dict(modules=4, groups=8, declarations=16, bodies=8,
                                  logical_bytes=1048576, db_pages=256),
            "packet_limits": dict(packets=4, offers=8, offers_per_module=2, packet_bytes=65536,
                                  logical_bytes=1048576, db_pages=256),
            "index_limits": dict(max_objects=8, max_postings=1024, max_features=128,
                                 max_snapshots=16, max_logical_bytes=4194304, max_db_pages=2048),
            "packet_envelope": asdict(Envelope()), "max_operations": 8,
            "max_report_bytes": 1048576, "ledger_pages": 256}


def grant_limits():
    return dict(wall_seconds=30, controller_cpu_seconds=30, calls=8, input_bytes=1048576,
                worker_cpu_seconds=120, output_bytes=128*1024**2, output_entries=64,
                acquisition=dict(requests=8, reply_bytes=1048576, verify_attempts=2,
                                 verification_input_bytes=65536, worker_cpu_seconds=60),
                imports=dict(max_sources=4, max_members=8, max_receipts=8, max_calls=32,
                             submitted_bytes=1048576, data_bytes=1048576))


class WorkspaceControls(unittest.TestCase):
    def setUp(self):
        self.root = EVIDENCE/self._testMethodName; self.root.mkdir()
        self.stores = []

    def tearDown(self):
        for value in reversed(self.stores): value.close()

    def open(self, *, create=True, config=None):
        value = Workspace.open(self.root/"workspace", config or configuration(), create=create)
        self.stores.append(value); return value

    def test_exact_configuration_and_single_owner_lock(self):
        workspace = self.open()
        with self.assertRaises((OSError, ValueError)): self.open(create=False)
        self.assertFalse(workspace.status()["mathematical_acceptance"])
        workspace.close()
        wrong = configuration(); wrong["max_operations"] += 1
        with self.assertRaisesRegex(ValueError, "WORKSPACE_CONFIG"):
            self.open(create=False, config=wrong)
        again = self.open(create=False)
        self.assertEqual(again.status()["operations"], {})

    def test_one_original_grant_and_no_config_alias(self):
        workspace = self.open(); limits = grant_limits(); before = time.monotonic()
        grant = workspace.reserve(limits)
        self.assertGreaterEqual(grant.started, before)
        self.assertEqual(grant.deadline, grant.started+30)
        limits["calls"] = 4096
        exposed = grant.limits; exposed["calls"] = 2048
        self.assertEqual(grant.limits["calls"], 8)
        self.assertTrue(grant.directory.is_relative_to(workspace.root))
        with self.assertRaisesRegex(ValueError, "OPERATION_RESERVED_OR_CLEANUP_UNCERTAIN"):
            workspace.reserve(grant_limits())
        self.assertEqual(workspace.status()["operations"], {"GRANTED": 1})

    def test_reopen_marks_incomplete_grant_not_restored_authority(self):
        workspace = self.open(); original = workspace.reserve(grant_limits())
        original_id = original.identifier
        workspace._release()  # TEST ONLY: emulate loss of owner before orderly grant closure.
        again = self.open(create=False)
        self.assertEqual(again.status()["operations"], {"INTERRUPTED_WITH_UNCERTAIN_TAIL": 1})
        with self.assertRaisesRegex(ValueError, "GRANT_CHANGED_OR_EXPIRED"):
            again.operation(original, receipt_owner=object(), delta_owner=object(),
                            foundation_bytes=b"synthetic", foundation_sha256="00"*32)
        fresh = again.reserve(grant_limits())
        self.assertNotEqual(fresh.identifier, original_id)
        self.assertFalse(again.status()["mathematical_acceptance"])

    def test_foreign_owners_refuse_without_transfer_or_attempt(self):
        workspace = self.open(); grant = workspace.reserve(grant_limits())
        with self.assertRaisesRegex(ValueError, "EXACT_REAL_OWNERS"):
            workspace.operation(grant, receipt_owner=object(), delta_owner=object(),
                                foundation_bytes=b"synthetic", foundation_sha256="00"*32)
        self.assertFalse(workspace.status()["active_client"])
        self.assertEqual(workspace.status()["operations"], {"GRANTED": 1})
        self.assertFalse(grant._used)

    def test_grant_mutation_cannot_renew_deadline(self):
        workspace = self.open(); deadline = time.monotonic()+10
        grant = workspace.reserve(grant_limits(), outer_deadline=deadline)
        self.assertEqual(grant.deadline, deadline)
        grant._deadline += 3600  # Deliberate corruption of private caller-visible state.
        with self.assertRaisesRegex(ValueError, "GRANT_CHANGED_OR_EXPIRED"):
            workspace.operation(grant, receipt_owner=object(), delta_owner=object(),
                                foundation_bytes=b"synthetic", foundation_sha256="00"*32)
        self.assertFalse(workspace.status()["active_client"])

    def test_history_roundtrips_operational_floats_without_authority(self):
        workspace = self.open(); grant = workspace.reserve(grant_limits())
        workspace._record(grant.identifier, "GRANTED", {"elapsed_seconds": 0.125})
        page = workspace.history("operations", limit=1)
        self.assertEqual(page["identifiers"], [grant.identifier])
        row = workspace.read_record("operations", grant.identifier)
        self.assertEqual(row["report"]["elapsed_seconds"], 0.125)
        self.assertEqual(row["grant"]["deadline_monotonic"], grant.deadline)
        self.assertFalse(row["mathematical_acceptance"])

    def structural_client(self, workspace, grant):
        # TEST ONLY: structural publication needs no mathematical handle here.
        client = CommonsClient.__new__(CommonsClient)
        client.workspace, client.grant = workspace, grant
        client._input_bytes = 0; client._publications = []
        client._counts = {"store_calls": 0, "publication_attempts": 0}
        client._active = lambda: workspace._grant_active(grant)
        return client

    def test_partial_publication_is_publicly_recoverable(self):
        from aggregate_claims import bindings as B
        from modules import codec as C
        spec = {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
                "groups": [{"kind": "ordinary", "declarations": [{"kind": "theorem",
                "name": [["s", "synthetic"]], "universes": 0, "type": ["sort", ["zero"]],
                "value_hash": None, "meta": {}}]}]}
        image = [int.from_bytes(bytes.fromhex(B.RELATION_IMAGE)[i:i+4], "little") for i in range(0,32,4)]
        raw = C.canonical({"schema": "DMKN_MIXED_DELTA_PACKET_V1", "claims": [], "frontiers": [],
            "deltas": [{"schema": "DMKN_CERTIFIED_MODULES_V2", "image": image, "rank": 0,
                        "local_spec": spec, "rows": [], "bodies": [], "parents": []}]})
        workspace = self.open(); grant = workspace.reserve(grant_limits())
        client = self.structural_client(workspace, grant)
        with patch.object(workspace.index, "admit", side_effect=ValueError("TEST_INDEX_INTERRUPTION")):
            with self.assertRaises(PartialPublicationError) as failure:
                client._publish(raw, [[["s", "synthetic"]]], {"mode": "quota-bounded-local-custody"})
        identifier = failure.exception.publication_id
        self.assertIn(identifier, workspace.history("publications")["identifiers"])
        row = workspace.read_record("publications", identifier)
        self.assertEqual(row["outcome"]["status"], "PARTIAL_PUBLICATION")
        before = workspace.packets.status(); workspace.close()
        again = self.open(create=False); fresh = again.reserve(grant_limits())
        repaired = self.structural_client(again, fresh)
        result = CommonsClient.reconcile.__wrapped__(repaired, identifier)
        self.assertEqual(result["phase"], "LOCALLY_PUBLISHED")
        self.assertEqual(result["intent"]["reconciles"], identifier)
        self.assertFalse(result["mathematical_acceptance"])
        self.assertEqual(again.packets.status(), before)

    def test_report_failure_still_releases_client_and_disallows_renewal(self):
        workspace = self.open(); grant = workspace.reserve(grant_limits())
        client = CommonsClient.__new__(CommonsClient)
        client.workspace, client.grant = workspace, grant
        client._closed = client._busy = False; client._state = "OPEN"
        client._session = client.preparation = client._acquisition = client._channel = None
        class StubOwner:
            def close(self): pass
        class StubBudget: closed = False
        client.delta = client.receipt = StubOwner(); client._budget = StubBudget()
        client._warrants, client._candidates, client._receipt_cache, client._packet_cache = {}, {}, {}, {}
        client._context = None; client._failures = []
        client.report = lambda: {"test_only": True}
        workspace._client = client
        with patch.object(workspace, "_record", side_effect=OSError("TEST_REPORT_FAILURE")):
            with self.assertRaisesRegex(OSError, "TEST_REPORT_FAILURE"): asyncio.run(client.close())
        self.assertIsNone(workspace._client)
        self.assertNotIn(grant, workspace._grants)
        self.assertTrue(workspace._poisoned)
        with self.assertRaisesRegex(ValueError, "CLEANUP_UNCERTAIN"): workspace.reserve(grant_limits())

    def test_same_live_cache_still_checks_issuer_and_never_receives_again(self):
        # Intentional stub, not a ReceiptVerifier or a generated proof.
        raw = b"TEST-ONLY-NOT-A-RECEIPT"; summary = {"synthetic": True}
        import hashlib
        digest = hashlib.sha256(raw).hexdigest()
        state = {"describes": 0, "receives": 0, "live": True}
        handle, token = object(), LiveWarrant()
        live = {"journal": b"test-journal", "receipt_sha256": digest, "profile_id": "11"*32}
        class StubIssuer:
            def describe(self, got):
                self_outer.assertIs(got, handle); state["describes"] += 1
                if not state["live"]: raise ValueError("TEST_ISSUER_REVOKED")
                return deepcopy(live)
            def receive(self, *args, **kwargs):
                state["receives"] += 1; raise AssertionError("unexpected full receive")
        self_outer = self
        client = CommonsClient.__new__(CommonsClient)
        client.receipt = StubIssuer(); client._input_bytes = 0
        class StubGrant: _limits = {"input_bytes": 1048576}
        client.grant = StubGrant()
        from modules import codec as C
        key = digest, len(raw), C.canonical(summary)
        client._receipt_cache = {key: token}
        client._warrants = {token: ("I", handle, raw, {**live, "journal": list(live["journal"])})}
        client._counts = {"same_live_hits": 0}
        result = CommonsClient.admit_receipt.__wrapped__(client, raw, summary)
        self.assertIs(result, token)
        self.assertEqual((state["describes"], state["receives"], client._counts["same_live_hits"]), (1,0,1))
        state["live"] = False
        with self.assertRaisesRegex(ValueError, "TEST_ISSUER_REVOKED"):
            CommonsClient.admit_receipt.__wrapped__(client, raw, summary)
        self.assertEqual(state["receives"], 0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True)
    EVIDENCE = Path(parser.parse_args().output); EVIDENCE.mkdir(parents=True, exist_ok=False)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(WorkspaceControls))
    report = {"status": "PASS_WORKSPACE_STRUCTURAL_CONTROLS" if result.wasSuccessful() else "FAIL",
              "tests": result.testsRun, "errors": len(result.errors), "failures": len(result.failures),
              "native_calls": 0, "receipt_verifications": 0, "mathematical_authority": False}
    with (EVIDENCE/"RESULT.json").open("x", encoding="utf-8") as stream: json.dump(report, stream, sort_keys=True)
    raise SystemExit(0 if result.wasSuccessful() else 1)

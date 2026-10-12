"""Synthetic changed-boundary controls, not mathematical admission evidence.

One local HTTP loopback, SQLite and fake receipt bytes. No DHT, guest, Lean,
native kernel, cryptographic verification or proving. Root selects execution.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from aggregate_claims import bindings as B
from custody.module_store import ModuleStore
from delta import custody as OLD
from discovery.discovery_store import Store
from discovery.module_export_adapter import ModuleExportAdapter
from mixed_claims.test_receiver import packet_value, FAKE_IMAGE
from mixed_claims.receiver import MixedDeltaVerifier
from mixed_network.custody import PacketStore, public_profile, profile_id, verify_offer, packet_digest
from mixed_network.transport import CompositeProvider, MixedAcquisition
from modules import codec as C
from transport.http_provider_receipts import Endpoint
from transport.receipt_client import AcquisitionBudget

EVIDENCE = None
PACKET_LIMITS = dict(packets=4, offers=8, offers_per_module=2, packet_bytes=65536,
                     logical_bytes=1048576, db_pages=256)
MODULE_LIMITS = dict(modules=4, groups=8, declarations=16, bodies=8,
                     logical_bytes=1048576, db_pages=256)
INDEX_LIMITS = dict(max_objects=8, max_postings=1024, max_features=128,
                    max_snapshots=16, max_logical_bytes=4194304, max_db_pages=2048)
BUDGET_LIMITS = dict(requests=5, reply_bytes=1048576, verify_attempts=2,
                     verification_input_bytes=65536, worker_cpu_seconds=60)


class NetworkControls(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.root = EVIDENCE/self._testMethodName; self.root.mkdir()
        self.value = packet_value(); self.raw = C.canonical(self.value)
        self.spec = self.value["deltas"][-1]["local_spec"]
        self.summary = C.summarize(self.spec); self.module = C.summary_id(self.summary)
        self.profile = public_profile(FAKE_IMAGE)
        self.entry = {"packet_sha256": packet_digest(self.raw), "packet_bytes": len(self.raw)}
        self.adapter = ModuleExportAdapter(C, B.FOUNDATION, B.POLICY)
        self.opening = C.group_opening(self.spec, 0)
        self.name = self.spec["groups"][0]["declarations"][0]["name"]
        self.export = self.adapter.encode_opening(self.module, self.name, self.opening)
        self.record = self.adapter.extract(self.export)
        self.stores, self.providers, self.clients = [], [], []

    async def asyncTearDown(self):
        for provider in reversed(self.providers): await provider.stop()
        for client in reversed(self.clients): client.close()
        for store in reversed(self.stores): store.close()

    def packets(self, name, *, create=True, limits=None):
        result = PacketStore(self.root/name, self.profile, limits or PACKET_LIMITS, create=create)
        self.stores.append(result); return result

    def modules(self, name):
        result = ModuleStore(self.root/name, C, B.FOUNDATION, B.POLICY, MODULE_LIMITS, create=True)
        self.stores.append(result); return result

    def request(self):
        return {"module_id": self.module, "wire_profile_id": profile_id(self.profile),
                "max_offers": 2, "max_bytes": 4096}

    def client(self, modules, packets, *, verifier=None, endpoints=None):
        budget = AcquisitionBudget(time.monotonic()+30, BUDGET_LIMITS)
        result = MixedAcquisition(self.adapter, endpoints or {"p": Endpoint("127.0.0.1", 1)},
            self.profile, budget, modules, packets, verifier=verifier)
        self.clients.append(result); return result

    async def test_profiles_and_offers_are_not_interchangeable(self):
        old = OLD.public_profile(B.RELATION_IMAGE, B.FOUNDATION, B.POLICY)
        with self.assertRaises(ValueError): profile_id(old)
        with self.assertRaises(ValueError): OLD.profile_id(self.profile)
        for field, wrong in (("aggregate_image", B.RELATION_IMAGE), ("relation_image", "00"*32),
                             ("proof_form", "bounded-native-delta-v1")):
            changed = {**self.profile, field: wrong}
            with self.assertRaises(ValueError): profile_id(changed)
        store = self.packets("p"); store.put(self.module, self.raw)
        offer = store.offer(self.request())
        self.assertEqual(verify_offer(offer, self.request())["packets"], [self.entry])
        with self.assertRaises(ValueError): OLD.verify_offer(offer, self.request())
        for field, wrong in (("mathematical_acceptance", True), ("global_complete", True),
                             ("packets", [self.entry, self.entry]), ("module_id", "00"*32),
                             ("schema", OLD.OFFER_SCHEMA), ("wire_profile_id", "00"*32)):
            with self.assertRaises(ValueError): verify_offer({**offer, field: wrong}, self.request())

    async def test_reopen_exact_custody_and_corruption_refusal(self):
        store = self.packets("p")
        self.assertTrue(store.put(self.module, self.raw)["new_packet"])
        self.assertFalse(store.put(self.module, self.raw)["new_offer"])
        target, census = store.inspect(self.module, self.raw)
        self.assertEqual(target, self.summary)
        self.assertEqual((census["claims"], census["frontiers"], census["deltas"]), (1, 2, 1))
        status = store.status(); self.assertFalse(status["mathematical_acceptance"]); store.close()
        store = self.packets("p", create=False); self.assertEqual(store.status(), status)
        self.assertEqual(store.get(self.entry["packet_sha256"], len(self.raw)), self.raw)
        store.db.execute("UPDATE packets SET blob=?", (b"x"*len(self.raw),))
        with self.assertRaisesRegex(ValueError, "CUSTODY_DIGEST"):
            store.get(self.entry["packet_sha256"], len(self.raw))

    async def test_transaction_and_mixed_structural_refusals(self):
        store = self.packets("p", limits={**PACKET_LIMITS, "offers_per_module": 1})
        empty = store.status()
        def expired(): raise ValueError("TEST_EXPIRED")
        with self.assertRaisesRegex(ValueError, "TEST_EXPIRED"):
            store.put(self.module, self.raw, before_commit=expired)
        self.assertEqual(store.status(), empty)
        with self.assertRaisesRegex(ValueError, "MIXED_CUSTODY_TARGET_BINDING"):
            store.put("00"*32, self.raw)
        for change in (lambda value: value.update(schema="DMKN_NATIVE_DELTA_PACKET_V1"),
                       lambda value: value["frontiers"][0].update(siblings=[[0]*32]),
                       lambda value: value["claims"][0]["statement"].__setitem__(12, 9)):
            value = deepcopy(self.value); change(value)
            with self.assertRaises(ValueError): store.put(self.module, C.canonical(value))
        self.assertEqual(store.status(), empty)
        store.put(self.module, self.raw); before = store.status()
        variant = deepcopy(self.value); variant["claims"][0]["receipt_hex"] = b"STILL-NOT-A-PROOF".hex()
        with self.assertRaisesRegex(ValueError, "CUSTODY_LOCAL_OFFERS"):
            store.put(self.module, C.canonical(variant))
        self.assertEqual(store.status(), before)

    async def test_loopback_acquisition_and_provider_loss(self):
        remote_packets, remote_modules = self.packets("remote-p"), self.modules("remote-m")
        remote_packets.put(self.module, self.raw); remote_modules.put_group(self.module, self.opening)
        index = Store(self.root/"index", self.adapter, INDEX_LIMITS, create=True)
        self.stores.append(index); index.admit(self.export)
        provider = CompositeProvider(index=index, custody=remote_modules, packets=remote_packets,
            max_requests=8, max_reply_bytes=64*1024**2, operation_ms=5000)
        self.providers.append(provider); endpoint = await provider.start()
        local_packets, local_modules = self.packets("local-p"), self.modules("local-m")
        client = self.client(local_modules, local_packets, endpoints={"replica": endpoint})
        client.budget.charge_external("test-prepaid-prior-phase", 2, 4096)
        resolved = await client.export("replica", self.record)
        self.assertIn("MIXED_RECEIVE", resolved["next_gate"])
        offer = await client.offers("replica", self.module); self.assertEqual(offer["packets"], [self.entry])
        retained = await client.packet("replica", self.module, self.entry)
        self.assertFalse(retained["mathematical_acceptance"])
        with self.assertRaisesRegex(ValueError, "MIXED_REAL_OWNER_VERIFIER_REQUIRED"):
            client.admit(resolved, self.entry)
        with self.assertRaisesRegex(ValueError, "RECEIPT_AGGREGATE_BUDGET"):
            await client.offers("replica", self.module)
        await provider.stop(); remote_packets.close(); remote_modules.close(); index.close()
        held = client.custody_ready(resolved, self.entry)
        self.assertFalse(held["mathematical_acceptance"])
        self.assertEqual(held["census"]["claims"], 1)
        self.assertEqual(provider.status()["requests"], 3)
        self.assertEqual(provider.status()["active"], 0)
        self.assertEqual(client.budget.report()["used"]["requests"], 5)
        self.assertEqual(client.budget.report()["pending_requests"], 0)
        self.assertEqual(client.budget.report()["used"]["reply_bytes"],
            4096+client.http["reply_bytes"]+client.structural.report()["charged_reply_bytes"])
        client.close(); local_packets.close(); local_modules.close()
        cold = self.packets("local-p", create=False)
        self.assertEqual(cold.get(self.entry["packet_sha256"], len(self.raw)), self.raw)

    async def test_no_duck_authority_no_unoffered_fetch_no_changed_owner(self):
        modules, packets = self.modules("m"), self.packets("p")
        with self.assertRaisesRegex(ValueError, "MIXED_ACQUISITION_REAL_OWNER_VERIFIER"):
            self.client(modules, packets, verifier=object())
        client = self.client(modules, packets)
        with self.assertRaisesRegex(ValueError, "PACKET_NOT_OFFERED"):
            await client.packet("p", self.module, self.entry)
        self.assertEqual(client.budget.report()["used"]["requests"], 0)
        with self.assertRaisesRegex(ValueError, "EXACT_PROSPECTIVE_HANDOFF"):
            MixedAcquisition.from_search(object(), self.profile, modules, packets)
        client.verifier = object()
        with self.assertRaisesRegex(ValueError, "ORIGIN_OR_CLOSED"): client._active()
        client.verifier = None  # Restore solely for test teardown, not authority.

    async def test_mocked_admission_reserves_claims_not_members(self):
        modules, packets = self.modules("m"), self.packets("p")
        modules.put_group(self.module, self.opening); packets.put(self.module, self.raw)
        # TEST ONLY: exact-class fake never returns a mathematical handle.
        owner = object.__new__(MixedDeltaVerifier)
        owner._image, owner._aggregate_image = B.RELATION_IMAGE, FAKE_IMAGE
        owner._foundation, owner._policy = B.FOUNDATION, B.POLICY
        owner._active = lambda: None; owner.close = lambda: None
        calls = []
        def refuse(raw, summary, **kwargs):
            calls.append((raw, summary, kwargs)); raise ValueError("TEST_ONLY_NO_RECEIPT")
        owner.receive = refuse
        client = self.client(modules, packets, verifier=owner)
        resolved = {"locator": {"module_id": self.module, "relative_name": self.name, "group_index": 0},
                    "opening": self.opening, "descriptor": self.spec["groups"][0]["declarations"][0]}
        with self.assertRaisesRegex(ValueError, "TEST_ONLY_NO_RECEIPT"):
            client.admit(resolved, self.entry)
        self.assertEqual(len(calls), 1)
        self.assertEqual(client.budget.report()["used"]["worker_cpu_seconds"], 60)
        self.assertEqual(client.budget.report()["used"]["verify_attempts"], 1)
        with self.assertRaisesRegex(ValueError, "RECEIPT_VERIFY_BUDGET"):
            client.admit(resolved, self.entry)
        self.assertEqual(len(calls), 1)

    async def test_mocked_owner_expiry_during_readback_refuses_final_promotion(self):
        modules, packets = self.modules("m"), self.packets("p")
        modules.put_group(self.module, self.opening); packets.put(self.module, self.raw)
        owner = object.__new__(MixedDeltaVerifier)
        owner._image, owner._aggregate_image = B.RELATION_IMAGE, FAKE_IMAGE
        owner._foundation, owner._policy = B.FOUNDATION, B.POLICY
        state = {"expired": False, "closed": False, "describe_calls": 0}
        owner._active = lambda: None
        owner.close = lambda: state.update(closed=True)
        owner.receive = lambda *args, **kwargs: object()  # TEST ONLY fake handle.
        owner.open_group = lambda *args: {"TEST_ONLY": True}
        def describe(handle):
            state["describe_calls"] += 1
            if state["expired"]: raise ValueError("TEST_EXPIRED_MATHEMATICAL_OWNER")
        owner.describe = describe
        client = self.client(modules, packets, verifier=owner)
        original = client.custody_ready
        calls = []
        def held(*args, **kwargs):
            result = original(*args, **kwargs); calls.append(result)
            if len(calls) == 2: state["expired"] = True
            return result
        client.custody_ready = held
        resolved = {"locator": {"module_id": self.module, "relative_name": self.name, "group_index": 0},
                    "opening": self.opening, "descriptor": self.spec["groups"][0]["declarations"][0]}
        with self.assertRaisesRegex(ValueError, "TEST_EXPIRED_MATHEMATICAL_OWNER"):
            client.admit(resolved, self.entry)
        self.assertEqual(len(calls), 2)
        self.assertEqual(state["describe_calls"], 1)
        self.assertTrue(state["closed"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True)
    args = parser.parse_args(); EVIDENCE = Path(args.output)
    EVIDENCE.mkdir(parents=True, exist_ok=False)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NetworkControls))
    report = {"status": "PASS_MIXED_STRUCTURAL_LOOPBACK_ONLY" if result.wasSuccessful() else "FAIL",
              "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
              "native_calls": 0, "receipt_verifications": 0, "positive_mathematical_authority": False}
    with (EVIDENCE/"RESULT.json").open("x", encoding="utf-8") as stream: json.dump(report, stream, sort_keys=True)
    raise SystemExit(0 if result.wasSuccessful() else 1)

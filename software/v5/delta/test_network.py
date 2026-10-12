"""UNRUN changed-boundary controls; synthetic packet rows are NOT proofs.

Root selects any actual launch under a finite Job. These controls use local
SQLite and one bounded loopback provider, never a native checker/prover/DHT.
"""
import argparse
import asyncio
from copy import deepcopy
import json
from pathlib import Path
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from modules import codec as C
from delta.test_packet import sample
from delta.packet import Envelope
from delta.custody import PacketStore, public_profile, profile_id, packet_digest, verify_offer
from delta.transport import CompositeProvider, DeltaAcquisition, DeltaLocatedHandoff, OFFER_ROUTE, PACKET_ROUTE, ROUTES
from custody.module_store import ModuleStore
from custody.receipt_store import profile_id as receipt_profile_id
from discovery.module_export_adapter import ModuleExportAdapter
from discovery.discovery_store import Store
from transport.receipt_client import AcquisitionBudget
from transport.http_provider_receipts import RECEIPT_ROUTE, RECEIPT_OFFER_ROUTE

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
        image, foundation, policy, self.summary, unused, self.witness = sample()
        self.profile = public_profile(image, foundation, policy)
        self.module = C.summary_id(self.summary)
        self.raw = C.canonical({"schema": "DMKN_NATIVE_DELTA_PACKET_V1", "frontiers": [],
                                "deltas": [self.witness]})
        self.entry = {"packet_sha256": packet_digest(self.raw), "packet_bytes": len(self.raw)}
        self.adapter = ModuleExportAdapter(C, foundation, policy)
        self.opening = C.group_opening(self.witness["local_spec"], 0)
        self.name = self.witness["local_spec"]["groups"][0]["declarations"][0]["name"]
        self.export = self.adapter.encode_opening(self.module, self.name, self.opening)
        self.record = self.adapter.extract(self.export)
        self.stores, self.providers, self.clients = [], [], []

    async def asyncTearDown(self):
        for provider in reversed(self.providers): await provider.stop()
        for client in reversed(self.clients): client.close()
        for store in reversed(self.stores): store.close()

    def packets(self, name, *, create=True, limits=None):
        value = PacketStore(self.root/name, self.profile, limits or PACKET_LIMITS, create=create)
        self.stores.append(value); return value

    def modules(self, name, *, create=True):
        value = ModuleStore(self.root/name, C, self.profile["foundation"], self.profile["policy"],
                            MODULE_LIMITS, create=create)
        self.stores.append(value); return value

    def request(self):
        return {"module_id": self.module, "wire_profile_id": profile_id(self.profile),
                "max_offers": 2, "max_bytes": 4096}

    async def test_distinct_wire_and_untrusted_offers(self):
        self.assertNotIn(RECEIPT_ROUTE, ROUTES); self.assertNotIn(RECEIPT_OFFER_ROUTE, ROUTES)
        self.assertIn(OFFER_ROUTE, ROUTES); self.assertIn(PACKET_ROUTE, ROUTES)
        with self.assertRaises(ValueError): receipt_profile_id(self.profile)
        altered = deepcopy(self.profile); altered["proof_form"] = "succinct-poseidon2"
        with self.assertRaises(ValueError): profile_id(altered)
        store = self.packets("p"); store.put(self.module, self.raw)
        offer = store.offer(self.request())
        self.assertEqual(offer["packets"], [self.entry]); self.assertFalse(offer["mathematical_acceptance"])
        self.assertFalse(offer["global_complete"])
        for field, value in (("mathematical_acceptance", True), ("module_id", "00"*32),
                             ("proof_form", "receipt"), ("packets", [self.entry, self.entry])):
            changed = {**offer, field: value}
            with self.assertRaises(ValueError): verify_offer(changed, self.request())

    async def test_reopen_exact_bytes_dedup_and_corruption(self):
        store = self.packets("p")
        self.assertTrue(store.put(self.module, self.raw)["new_packet"])
        self.assertFalse(store.put(self.module, self.raw)["new_offer"])
        original = store.status(); store.close()
        store = self.packets("p", create=False)
        self.assertEqual(store.status(), original)
        self.assertEqual(store.get(self.entry["packet_sha256"], len(self.raw)), self.raw)
        store.db.execute("UPDATE packets SET blob=? WHERE digest=?", (b"x"*len(self.raw), self.entry["packet_sha256"]))
        with self.assertRaisesRegex(ValueError, "DELTA_CUSTODY_DIGEST"):
            store.get(self.entry["packet_sha256"], len(self.raw))

    async def test_transaction_target_profile_and_quota_refusals(self):
        store = self.packets("p", limits={**PACKET_LIMITS, "offers_per_module": 1})
        empty = store.status()
        def expired(): raise ValueError("TEST_ORIGINAL_DEADLINE")
        with self.assertRaisesRegex(ValueError, "TEST_ORIGINAL_DEADLINE"):
            store.put(self.module, self.raw, before_commit=expired)
        self.assertEqual(store.status(), empty)
        self.assertEqual(store.offer(self.request())["packets"], [])
        with self.assertRaisesRegex(ValueError, "DELTA_CUSTODY_TARGET_BINDING"):
            store.put("00"*32, self.raw)
        wrong = deepcopy(self.witness); wrong["image"] = [0]*8
        bad = C.canonical({"schema": "DMKN_NATIVE_DELTA_PACKET_V1", "frontiers": [], "deltas": [wrong]})
        with self.assertRaisesRegex(ValueError, "DELTA_CUSTODY_IMAGE"): store.put(self.module, bad)
        store.put(self.module, self.raw); before = store.status()
        variant = deepcopy(self.witness); variant["rows"] = [None]
        changed = C.canonical({"schema": "DMKN_NATIVE_DELTA_PACKET_V1", "frontiers": [], "deltas": [variant]})
        with self.assertRaisesRegex(ValueError, "DELTA_CUSTODY_LOCAL_OFFERS"): store.put(self.module, changed)
        self.assertEqual(store.status(), before)

    async def test_actual_loopback_byte_acquisition_and_supplier_offline_readback(self):
        remote_packets, remote_modules = self.packets("remote-packets"), self.modules("remote-modules")
        remote_packets.put(self.module, self.raw); remote_modules.put_group(self.module, self.opening)
        index = Store(self.root/"remote-index", self.adapter, INDEX_LIMITS, create=True)
        self.stores.append(index); index.admit(self.export)
        provider = CompositeProvider(index=index, custody=remote_modules, packets=remote_packets,
                                     max_requests=8, max_reply_bytes=64*1024**2, operation_ms=5000)
        self.providers.append(provider); endpoint = await provider.start()
        budget = AcquisitionBudget(time.monotonic()+30, BUDGET_LIMITS)
        budget.charge_external("test-prepaid-prior-phase", 2, 4096)
        local_packets, local_modules = self.packets("local-packets"), self.modules("local-modules")
        client = DeltaAcquisition(self.adapter, {"replica": endpoint}, self.profile, budget,
                                  local_modules, local_packets)
        self.clients.append(client)
        resolved = await client.export("replica", self.record)
        self.assertEqual(resolved["next_gate"], "ACTUAL_COMPLETE_DELTA_RECEIVE_BEFORE_MATHEMATICAL_USE")
        offered = await client.offers("replica", self.module)
        self.assertEqual(offered["packets"], [self.entry])
        retained = await client.packet("replica", self.module, self.entry)
        self.assertFalse(retained["mathematical_acceptance"])
        with self.assertRaisesRegex(ValueError, "DELTA_REAL_OWNER_VERIFIER_REQUIRED"):
            client.admit(resolved, self.entry)
        with self.assertRaisesRegex(ValueError, "RECEIPT_AGGREGATE_BUDGET"):
            await client.offers("replica", self.module)
        await provider.stop(); remote_packets.close(); remote_modules.close(); index.close()
        held = client.custody_ready(resolved, self.entry)
        self.assertFalse(held["mathematical_acceptance"])
        self.assertFalse(held["cross_database_atomic"]); self.assertFalse(held["all_future_bodies_covered"])
        self.assertEqual(held["census"]["rows"], 0)  # Deliberately not valid mathematics.
        self.assertEqual(provider.status()["requests"], 3)
        self.assertEqual(provider.status()["active"], 0)
        self.assertEqual(provider.status()["reserved_reply_bytes"], 0)
        self.assertEqual(budget.report()["used"]["requests"], 5)
        self.assertEqual(budget.report()["pending_requests"], 0)
        self.assertEqual(budget.report()["used"]["reply_bytes"],
            4096+client.http["reply_bytes"]+client.structural.report()["charged_reply_bytes"])
        client.close(); local_packets.close(); local_modules.close()
        cold = self.packets("local-packets", create=False)
        self.assertEqual(cold.get(self.entry["packet_sha256"], len(self.raw)), self.raw)

    async def test_no_unoffered_download_or_duck_authority(self):
        from transport.http_provider_receipts import Endpoint
        modules, packets = self.modules("m"), self.packets("p")
        budget = AcquisitionBudget(time.monotonic()+30, BUDGET_LIMITS)
        with self.assertRaisesRegex(ValueError, "DELTA_ACQUISITION_REAL_OWNER_VERIFIER"):
            DeltaAcquisition(self.adapter, {"p": Endpoint("127.0.0.1", 1)}, self.profile, budget,
                             modules, packets, verifier=object())
        client = DeltaAcquisition(self.adapter, {"p": Endpoint("127.0.0.1", 1)}, self.profile,
                                  budget, modules, packets)
        self.clients.append(client)
        with self.assertRaisesRegex(ValueError, "DELTA_PACKET_NOT_OFFERED"):
            await client.packet("p", self.module, self.entry)
        self.assertEqual(budget.report()["used"]["requests"], 0)
        with self.assertRaisesRegex(ValueError, "DELTA_ACQUISITION_EXACT_PROSPECTIVE_HANDOFF"):
            DeltaAcquisition.from_search(object(), self.profile, modules, packets)
        with self.assertRaisesRegex(ValueError, "DELTA_HANDOFF_FRESH_READER"):
            DeltaLocatedHandoff(object(), self.adapter, [], object(), budget, {}, {})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True)
    args = parser.parse_args(); EVIDENCE = Path(args.output)
    EVIDENCE.mkdir(parents=True, exist_ok=False)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NetworkControls))
    report = {"status": "PASS_STRUCTURAL_AND_LOOPBACK_ONLY" if result.wasSuccessful() else "FAIL",
              "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
              "native_calls": 0, "receipt_verifications": 0, "positive_mathematical_authority": False}
    with (EVIDENCE/"RESULT.json").open("x", encoding="utf-8") as stream: json.dump(report, stream, sort_keys=True)
    raise SystemExit(0 if result.wasSuccessful() else 1)

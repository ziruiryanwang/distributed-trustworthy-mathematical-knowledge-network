"""Changed I-only profile boundaries; synthetic bytes are NOT valid proofs.

SQLite and a bounded local HTTP exchange only. No native/receipt/proving calls.
Root selects one finite execution; this is not another mixed-verifier campaign.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from aggregate_claims import bindings as B
from custody.module_store import ModuleStore
from delta.transport import DeltaLocatedHandoff
from delta_claims.claims import expected_journal
from discovery.discovery_store import Store
from discovery.module_export_adapter import ModuleExportAdapter
from frontier_network import custody as F
from frontier_network.transport import CompositeProvider, FrontierAcquisition, FrontierLocatedHandoff
from mixed_network import custody as M
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


def specimen():
    def spec(name):
        return {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
                "groups": [{"kind": "ordinary", "declarations": [{"kind": "theorem",
                "name": [["s", name]], "universes": 0, "type": ["sort", ["zero"]],
                "value_hash": None, "meta": {}}]}]}
    parent, child = spec("synthetic_parent"), spec("synthetic_child")
    exact = expected_journal(C.summarize(parent), 0, B.RELATION_IMAGE)
    image = [int.from_bytes(bytes.fromhex(B.RELATION_IMAGE)[i:i+4], "little") for i in range(0,32,4)]
    return {"schema": F.PACKET_SCHEMA,
            "claims": [{"tag": 0, "statement": list(exact), "receipt_hex": b"NOT-A-PROOF".hex()}],
            "frontiers": [{"claim_index": 0, "journal": list(exact), "member_index": 0, "siblings": []}],
            "deltas": [{"schema": "DMKN_CERTIFIED_MODULES_V2", "image": image, "rank": 1,
                        "local_spec": child, "rows": [], "bodies": [],
                        "parents": [{"journal": list(exact), "openings": []}]}]}


class ProfileControls(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.root = EVIDENCE/self._testMethodName; self.root.mkdir()
        self.value = specimen(); self.raw = C.canonical(self.value)
        self.spec = self.value["deltas"][0]["local_spec"]
        self.module = C.summary_id(C.summarize(self.spec))
        self.opening = C.group_opening(self.spec, 0)
        self.profile = F.public_profile()
        self.adapter = ModuleExportAdapter(C, B.FOUNDATION, B.POLICY)
        self.stores, self.clients, self.providers = [], [], []

    async def asyncTearDown(self):
        for provider in reversed(self.providers): await provider.stop()
        for client in reversed(self.clients): client.close()
        for store in reversed(self.stores): store.close()

    def packets(self, name, *, create=True, limits=None):
        store = F.PacketStore(self.root/name, self.profile, limits or PACKET_LIMITS, create=create)
        self.stores.append(store); return store

    def modules(self, name):
        store = ModuleStore(self.root/name, C, B.FOUNDATION, B.POLICY, MODULE_LIMITS, create=True)
        self.stores.append(store); return store

    def request(self):
        return dict(module_id=self.module, wire_profile_id=F.profile_id(self.profile), max_offers=2, max_bytes=4096)

    async def test_distinct_fixed_profile_and_offer(self):
        old = M.public_profile("11"*32)
        with self.assertRaises(ValueError): F.profile_id(old)
        with self.assertRaises(ValueError): M.profile_id(self.profile)
        for key, wrong in (("supported_claim_tags", [0,1]), ("aggregate_image", "11"*32),
                           ("foundation", "00"*32), ("policy", "00"*32)):
            with self.assertRaises(ValueError): F.profile_id({**self.profile, key: wrong})
        copy = F.public_profile(); copy["supported_claim_tags"].append(1)
        self.assertEqual(F.public_profile()["supported_claim_tags"], [0])
        store = self.packets("p"); store.put(self.module, self.raw)
        offer = store.offer(self.request()); F.verify_offer(offer, self.request())
        self.assertFalse(offer["mathematical_acceptance"])
        with self.assertRaises(ValueError): M.verify_offer(offer, self.request())
        for key, wrong in (("schema", M.OFFER_SCHEMA), ("proof_form", M.PROOF_FORM),
                           ("global_complete", True), ("mathematical_acceptance", True)):
            with self.assertRaises(ValueError): F.verify_offer({**offer, key: wrong}, self.request())

    async def test_A_refused_before_receipt_or_custody_mutation(self):
        store = self.packets("p"); before = store.status()
        wrong = deepcopy(self.value)
        # Exact-size but otherwise meaningless A header: refusal occurs before decoding it.
        wrong["claims"][0].update(tag=1, statement=[0]*B.HEADER_BYTES)
        with self.assertRaisesRegex(ValueError, "MIXED_AGGREGATE_OWNER_REQUIRED"):
            store.put(self.module, C.canonical(wrong))
        self.assertEqual(store.status(), before)
        self.assertTrue(store.put(self.module, self.raw)["new_packet"])
        target, census = store.inspect(self.module, self.raw)
        self.assertEqual(C.summary_id(target), self.module)
        self.assertEqual((census["claims"], census["frontiers"], census["deltas"]), (1,1,1))

    async def test_reopen_profile_config_and_mutation_refuse(self):
        store = self.packets("p"); store.put(self.module, self.raw)
        before = store.status(); store.close()
        with self.assertRaisesRegex(ValueError, "I_FRONTIER_CUSTODY_CONFIG"):
            self.packets("p", create=False, limits={**PACKET_LIMITS, "packets": 3})
        store = self.packets("p", create=False)
        self.assertEqual(store.status(), before)
        self.assertEqual(store.get(F.packet_digest(self.raw), len(self.raw)), self.raw)
        store.profile["aggregate_image"] = "11"*32
        with self.assertRaises(ValueError): store.inspect(self.module, self.raw)
        with self.assertRaises(ValueError): store.offer(self.request())

    async def test_exact_owner_and_same_handoff(self):
        self.assertIs(FrontierLocatedHandoff, DeltaLocatedHandoff)
        modules, packets = self.modules("m"), self.packets("p")
        budget = AcquisitionBudget(time.monotonic()+30, BUDGET_LIMITS)
        with self.assertRaisesRegex(ValueError, "REAL_OWNER_VERIFIER"):
            FrontierAcquisition(self.adapter, {"p": Endpoint("127.0.0.1",1)},
                self.profile, budget, modules, packets, verifier=object())
        with self.assertRaisesRegex(ValueError, "EXACT_PROSPECTIVE_HANDOFF"):
            FrontierAcquisition.from_search(object(), self.profile, modules, packets)
        self.assertEqual(budget.report()["used"]["verify_attempts"], 0)
        budget.closed = True  # Test-owned orphan: no client acquired this budget.

    async def test_new_profile_http_path_and_shared_grant(self):
        remote_p, remote_m = self.packets("rp"), self.modules("rm")
        remote_p.put(self.module, self.raw); remote_m.put_group(self.module, self.opening)
        name = self.spec["groups"][0]["declarations"][0]["name"]
        export = self.adapter.encode_opening(self.module, name, self.opening)
        record = self.adapter.extract(export)
        index = Store(self.root/"index", self.adapter, INDEX_LIMITS, create=True); self.stores.append(index)
        index.admit(export)
        provider = CompositeProvider(index=index, custody=remote_m, packets=remote_p,
            max_requests=4, max_reply_bytes=64*1024**2, operation_ms=5000)
        self.providers.append(provider); endpoint = await provider.start()
        local_p, local_m = self.packets("lp"), self.modules("lm")
        budget = AcquisitionBudget(time.monotonic()+30, BUDGET_LIMITS)
        budget.charge_external("prior-query", 2, 4096)
        client = FrontierAcquisition(self.adapter, {"peer": endpoint}, self.profile, budget, local_m, local_p)
        self.clients.append(client)
        resolved = await client.export("peer", record)
        entry = (await client.offers("peer", self.module))["packets"][0]
        await client.packet("peer", self.module, entry)
        self.assertEqual(client.report()["proof_form"], F.PROOF_FORM)
        self.assertIsNone(client.report()["aggregate_image"])
        self.assertEqual(client.budget.report()["used"]["requests"], 5)
        with self.assertRaisesRegex(ValueError, "RECEIPT_AGGREGATE_BUDGET"):
            await client.offers("peer", self.module)
        with self.assertRaisesRegex(ValueError, "REAL_OWNER_VERIFIER_REQUIRED"):
            client.admit(resolved, entry)
        self.assertFalse(client.custody_ready(resolved, entry)["mathematical_acceptance"])
        self.assertEqual(provider.status()["requests"], 3)
        self.assertEqual(client.budget.report()["used"]["verify_attempts"], 0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True)
    EVIDENCE = Path(parser.parse_args().output); EVIDENCE.mkdir(parents=True, exist_ok=False)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ProfileControls))
    report = {"status": "PASS_I_ONLY_PROFILE_CONTROLS" if result.wasSuccessful() else "FAIL",
              "tests": result.testsRun, "errors": len(result.errors), "failures": len(result.failures),
              "native_calls": 0, "receipt_verifications": 0, "mathematical_authority": False}
    with (EVIDENCE/"RESULT.json").open("x", encoding="utf-8") as stream: json.dump(report, stream, sort_keys=True)
    raise SystemExit(0 if result.wasSuccessful() else 1)

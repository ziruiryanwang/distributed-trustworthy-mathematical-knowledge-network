"""D18 changed-boundary controls: synthetic opaque bytes are NEVER proofs.

Run only in root's finite reviewed Job. No prover, admission executable, DHT or
old broad campaign is launched. Real loopback + durable SQLite are exercised.
"""
from pathlib import Path
import argparse
import asyncio
from copy import deepcopy
import hashlib
import json
import sys
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C
from discovery import formal_features as F
from discovery.module_export_adapter import ModuleExportAdapter
from custody.module_store import ModuleStore, BODY_SCHEMA
from custody.receipt_store import ReceiptStore, public_profile, profile_id, receipt_digest, verify_offer
from transport.http_provider_receipts import Provider, Endpoint, exchange, _header, RECEIPT_ROUTE, RECEIPT_OFFER_ROUTE
from transport.receipt_client import AcquisitionBudget, ReceiptAcquisition, DeadlineReceiptVerifier

EVIDENCE = None
REPORTS = {}
STORE_LIMITS = dict(receipts=8, offers=16, offers_per_module=4, receipt_bytes=4096,
                    logical_bytes=65536, db_pages=256)
MODULE_LIMITS = dict(modules=4, groups=8, declarations=16, bodies=8,
                     logical_bytes=1048576, db_pages=256)
BUDGET_LIMITS = dict(requests=16, reply_bytes=1048576, verify_attempts=2,
                     verification_input_bytes=8192, worker_cpu_seconds=60)
OPAQUE = b"NOT A RISC ZERO RECEIPT\x00\xff\xfe\x01"


def h(text): return hashlib.sha256(text.encode("ascii")).hexdigest()


def fixture():
    expression = ["sort", ["zero"]]
    digest = C.body_id(expression, 0)
    spec = {"schema": C.SPEC_SCHEMA, "foundation": h("receipt-fixture-foundation"),
            "policy": h("receipt-fixture-policy"), "groups": [{"kind": "ordinary", "declarations": [
                {"name": [["s", "Example"]], "kind": "definition", "universes": 0,
                 "type": ["sort", ["succ", ["zero"]]], "value_hash": digest,
                 "meta": {"hint": "abbrev", "safety": "safe"}}]}]}
    return spec, expression, digest


class ReceiptControls(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.root = EVIDENCE / self._testMethodName; self.root.mkdir()
        self.spec, self.expression, self.digest = fixture()
        self.module = C.module_id(self.spec); self.name = [["s", "Example"]]
        self.opening = C.group_opening(self.spec, 0)
        self.adapter = ModuleExportAdapter(C, self.spec["foundation"], self.spec["policy"])
        self.record = self.adapter.extract(self.adapter.encode_opening(self.module, self.name, self.opening))
        self.profile = public_profile(h("synthetic-no-admission-image"), self.spec["foundation"], self.spec["policy"])
        self.entry = {"receipt_sha256": receipt_digest(OPAQUE), "receipt_bytes": len(OPAQUE)}
        self.stores, self.providers, self.clients = [], [], []

    async def asyncTearDown(self):
        for provider in reversed(self.providers): await provider.stop()
        for client in reversed(self.clients): client.close()
        for store in reversed(self.stores): store.close()

    def receipts(self, name, *, create=True, limits=None):
        store = ReceiptStore(self.root/name, self.profile, limits or STORE_LIMITS, create=create)
        self.stores.append(store); return store

    def modules(self, name, *, create=True):
        store = ModuleStore(self.root/name, C, self.spec["foundation"], self.spec["policy"], MODULE_LIMITS, create=create)
        self.stores.append(store); return store

    def body_value(self):
        return {"schema": BODY_SCHEMA, "module_id": self.module, "relative_name": self.name,
                "universes": 0, "body_hash": self.digest, "expression": self.expression}

    def request(self):
        return {"module_id": self.module, "wire_profile_id": profile_id(self.profile), "max_offers": 4, "max_bytes": 4096}

    async def start(self, **kwargs):
        provider = Provider(**kwargs); self.providers.append(provider)
        return provider, await provider.start()

    def client(self, endpoint, *, receipts=None, modules=None, budget=None):
        client = ReceiptAcquisition(self.adapter, {"holder": endpoint}, self.profile,
            budget or AcquisitionBudget(time.monotonic()+20, BUDGET_LIMITS),
            modules or self.modules("local-modules"), receipts or self.receipts("local-receipts"))
        self.clients.append(client); return client

    async def test_store_reopen_coalescing_profile_and_corruption(self):
        store = self.receipts("source")
        first = store.put(self.module, OPAQUE)
        self.assertTrue(first["new_receipt"]); self.assertFalse(first["mathematical_acceptance"])
        self.assertFalse(store.put(self.module, OPAQUE)["new_offer"])
        self.assertTrue(store.put(h("other-module"), OPAQUE)["new_offer"])
        store.put(self.module, OPAQUE+b"different-certificate")
        self.assertEqual(store.status()["counts"]["receipts"], 2)
        self.assertEqual(store.status()["counts"]["offers"], 3)
        offered = store.offer(self.request())
        self.assertEqual(len(offered["receipts"]), 2)
        self.assertFalse(offered["global_complete"]); self.assertFalse(offered["mathematical_acceptance"])
        wrong = self.request(); wrong["wire_profile_id"] = h("wrong-profile")
        with self.assertRaisesRegex(ValueError, "RECEIPT_STORE_PROFILE"): store.offer(wrong)
        mutated = deepcopy(self.profile); mutated["encoding"]["max_bytes"] = float(mutated["encoding"]["max_bytes"])
        with self.assertRaisesRegex(ValueError, "RECEIPT_WIRE_PROFILE"): profile_id(mutated)
        store.close(); reopened = self.receipts("source", create=False)
        self.assertEqual(reopened.get(**{"digest": self.entry["receipt_sha256"], "size": len(OPAQUE)}), OPAQUE)
        self.assertEqual(reopened.offer(self.request()), offered)
        reopened.db.execute("UPDATE receipts SET blob=? WHERE digest=?", (b"x"*len(OPAQUE), self.entry["receipt_sha256"]))
        with self.assertRaisesRegex(ValueError, "RECEIPT_STORE_DIGEST"):
            reopened.get(self.entry["receipt_sha256"], len(OPAQUE))
        REPORTS[self._testMethodName] = {"cold_reopen_structural_only": True, "mathematical_acceptance": False}

    async def test_store_quota_and_deadline_are_atomic(self):
        store = self.receipts("source", limits={**STORE_LIMITS, "receipts": 1, "offers_per_module": 1})
        before = store.status()
        def expired(): raise ValueError("DEADLINE_BEFORE_COMMIT")
        with self.assertRaisesRegex(ValueError, "DEADLINE_BEFORE_COMMIT"):
            store.put(self.module, OPAQUE, before_commit=expired)
        self.assertEqual(store.status(), before)
        self.assertEqual(store.offer(self.request())["receipts"], [])
        store.put(self.module, OPAQUE); before = store.status()
        with self.assertRaisesRegex(ValueError, "RECEIPT_STORE_LOCAL_OFFERS"):
            store.put(self.module, b"another")
        with self.assertRaisesRegex(ValueError, "RECEIPT_STORE_QUOTA:receipts"):
            store.put(h("different-module"), b"another")
        with self.assertRaisesRegex(ValueError, "RECEIPT_STORE_OBJECT_CAP"):
            store.put(self.module, b"x"*4097)
        self.assertEqual(store.status(), before)
        self.assertEqual(store.get(self.entry["receipt_sha256"], len(OPAQUE)), OPAQUE)

    async def test_actual_binary_json_compatibility_and_supplier_offline_custody(self):
        source_receipts, source_modules = self.receipts("source-receipts"), self.modules("source-modules")
        source_receipts.put(self.module, OPAQUE); source_modules.put_group(self.module, self.opening)
        source_modules.put_body(self.module, self.name, self.body_value())
        provider, endpoint = await self.start(receipts=source_receipts, custody=source_modules)
        budget = AcquisitionBudget(time.monotonic()+20, {**BUDGET_LIMITS, "requests": 6})
        budget.charge_external("earlier-search-suballocation", 2, 4096)
        client = self.client(endpoint, budget=budget)
        resolved = await client.export("holder", self.record)
        offers = await client.offers("holder", self.module)
        self.assertEqual(offers["receipts"], [self.entry])
        retained = await client.receipt("holder", self.module, offers["receipts"][0])
        self.assertFalse(retained["mathematical_acceptance"])
        with self.assertRaisesRegex(ValueError, "CUSTODY_BODY_NOT_FOUND"):
            client.custody_ready(resolved, self.entry, [self.digest])
        await client.body("holder", resolved, self.digest, 4096)
        with self.assertRaisesRegex(ValueError, "RECEIPT_REAL_OWNER_VERIFIER_REQUIRED"):
            client.admit(resolved, self.entry, self.root/"forbidden-verifier-operation")
        self.assertFalse((self.root/"forbidden-verifier-operation").exists())
        with self.assertRaisesRegex(ValueError, "RECEIPT_AGGREGATE_BUDGET"):
            await client.offers("holder", self.module)
        self.assertEqual(provider.status()["requests"], 4)
        await provider.stop(); source_receipts.close(); source_modules.close()
        ready = client.custody_ready(resolved, self.entry, [self.digest])
        self.assertFalse(ready["mathematical_acceptance"])
        self.assertFalse(ready["cross_database_atomic"]); self.assertFalse(ready["all_future_bodies_covered"])
        report = client.report(); self.assertEqual(report["budget"]["used"]["requests"], 6)
        self.assertEqual(report["budget"]["pending_requests"], 0)
        self.assertEqual(report["budget"]["used"]["reply_bytes"],
            4096+report["receipt_http"]["reply_bytes"]+report["structural_http"]["charged_reply_bytes"])
        self.assertEqual(provider.status()["requests"], 4); self.assertEqual(provider.status()["active"], 0)
        self.assertEqual(provider.status()["reserved_reply_bytes"], 0)
        client.close(); client.modules.close(); client.receipts.close()
        cold_modules = self.modules("local-modules", create=False); cold_receipts = self.receipts("local-receipts", create=False)
        self.assertEqual(cold_modules.get_group(self.module, self.name)[0], self.opening)
        self.assertEqual(cold_modules.get_body(self.module, self.name, 0, self.digest), self.body_value())
        self.assertEqual(cold_receipts.get(self.entry["receipt_sha256"], len(OPAQUE)), OPAQUE)
        self.assertFalse(cold_receipts.status()["mathematical_acceptance"])
        REPORTS[self._testMethodName] = {"client": report, "provider": provider.status(),
            "cold_mathematical_reverification": "NOT_RUN_NO_GENUINE_RECEIPT", "mathematical_acceptance": False}

    async def test_separate_store_failure_remains_incomplete(self):
        source_receipts, source_modules = self.receipts("source-receipts"), self.modules("source-modules")
        source_receipts.put(self.module, OPAQUE); source_modules.put_group(self.module, self.opening)
        _, endpoint = await self.start(receipts=source_receipts, custody=source_modules)
        limited = self.receipts("limited", limits={**STORE_LIMITS, "receipt_bytes": 1})
        client = self.client(endpoint, receipts=limited)
        resolved = await client.export("holder", self.record)
        with self.assertRaisesRegex(ValueError, "RECEIPT_STORE_OBJECT_CAP"):
            await client.receipt("holder", self.module, self.entry)
        self.assertEqual(client.modules.status()["counts"]["groups"], 1)
        self.assertEqual(limited.status()["counts"]["receipts"], 0)
        with self.assertRaises(ValueError): client.custody_ready(resolved, self.entry)
        self.assertEqual(client.report()["budget"]["used"]["requests"], 2)
        self.assertEqual(client.report()["budget"]["pending_requests"], 0)

    async def test_binary_framing_digest_and_failure_charges(self):
        tasks = set(); variants = iter(("media", "size", "truncated", "trailing", "duplicate", "digest"))
        async def respond(reader, writer):
            task = asyncio.current_task(); tasks.add(task)
            try:
                header = await reader.readuntil(b"\r\n\r\n")
                length = int(next(x for x in header.decode().split("\r\n") if x.startswith("Content-Length:")).split(":")[1])
                await reader.readexactly(length); variant = next(variants)
                media = "application/json" if variant == "media" else "application/octet-stream"
                count = len(OPAQUE)+1 if variant == "size" else len(OPAQUE)
                head = _header("HTTP/1.1 200 OK", count, media=media)
                if variant == "duplicate": head = head[:-2]+b"Content-Length: "+str(count).encode()+b"\r\n\r\n"
                body = b"x"*len(OPAQUE) if variant == "digest" else OPAQUE
                if variant == "truncated": body = body[:-1]
                if variant == "trailing": body += b"x"
                writer.write(head+body); await writer.drain()
            finally:
                writer.close()
                try: await writer.wait_closed()
                finally: tasks.discard(task)
        server = await asyncio.start_server(respond, "127.0.0.1", 0)
        endpoint = Endpoint("127.0.0.1", server.sockets[0].getsockname()[1])
        client = self.client(endpoint)
        try:
            for variant in ("media", "size", "truncated", "trailing", "duplicate", "digest"):
                with self.subTest(variant=variant):
                    with self.assertRaises(Exception): await client.receipt("holder", self.module, self.entry)
            report = client.report()
            self.assertEqual(report["budget"]["used"]["requests"], 6)
            self.assertEqual(report["budget"]["used"]["reply_bytes"], 6*len(OPAQUE))
            self.assertEqual(report["budget"]["pending_requests"], 0)
            self.assertEqual(client.receipts.status()["counts"]["receipts"], 0)
            self.assertEqual(report["receipt_http"]["unknown_header_upper_bound"], 5*2*8192)
            self.assertEqual(report["receipt_http"]["unknown_request_body_upper_bound"], 5*16384)
            REPORTS[self._testMethodName] = report
        finally:
            server.close(); await server.wait_closed()
            pending = list(tasks)
            for task in pending: task.cancel()
            if pending: await asyncio.gather(*pending, return_exceptions=True)

    async def test_common_provider_quota_across_receipt_routes(self):
        store = self.receipts("source"); raw = b"x"*800; put = store.put(self.module, raw)
        provider, endpoint = await self.start(receipts=store, max_reply_bytes=1024, max_requests=3)
        request = {**self.request(), "max_bytes": 1024}
        response = await exchange(endpoint, RECEIPT_OFFER_ROUTE, request, 1024, 1000)
        self.assertGreater(len(response["raw"]), 224)
        entry = {"receipt_sha256": put["receipt_sha256"], "receipt_bytes": len(raw)}
        with self.assertRaises(Exception): await exchange(endpoint, RECEIPT_ROUTE, entry, len(raw), 1000)
        self.assertEqual(provider.status()["reply_bytes"], len(response["raw"]))
        self.assertEqual(provider.status()["requests"], 2)
        self.assertEqual(provider.status()["reserved_reply_bytes"], 0)
        self.assertEqual(provider.status()["failures"], 1)

    async def test_offer_binding_and_owner_configuration_refusals(self):
        store = self.receipts("source"); store.put(self.module, OPAQUE)
        offered = store.offer(self.request())
        for field, value in (("module_id", h("wrong-module")), ("wire_profile_id", h("wrong-profile")),
                             ("global_complete", True), ("mathematical_acceptance", True)):
            bad = deepcopy(offered); bad[field] = value
            with self.subTest(field=field):
                with self.assertRaises(ValueError): verify_offer(bad, self.request())
        bad = deepcopy(offered); bad["receipts"] *= 2
        with self.assertRaisesRegex(ValueError, "RECEIPT_OFFER_ORDER"): verify_offer(bad, self.request())
        _, endpoint = await self.start(receipts=store)
        local_m, local_r = self.modules("local-modules"), self.receipts("local-receipts")
        with self.assertRaisesRegex(ValueError, "RECEIPT_EXACT_OWNER_VERIFIER"):
            ReceiptAcquisition(self.adapter, {"holder": endpoint}, self.profile,
                AcquisitionBudget(time.monotonic()+20, BUDGET_LIMITS), local_m, local_r, verifier={"success": True})
        with self.assertRaisesRegex(ValueError, "RECEIPT_LOCAL_ADOPTION_PROFILE"):
            DeadlineReceiptVerifier(deadline=time.monotonic()+20, wire_profile=self.profile, image_id=h("wrong-image"))

    async def test_original_deadline_reservations_and_no_refund(self):
        with self.assertRaisesRegex(ValueError, "RECEIPT_ORIGINAL_DEADLINE"):
            AcquisitionBudget(time.monotonic()-1, BUDGET_LIMITS)
        budget = AcquisitionBudget(time.monotonic()+20, {**BUDGET_LIMITS, "requests": 2, "reply_bytes": 1024})
        budget.charge_external("search", 1, 512)
        ticket = budget.begin(512)
        with self.assertRaisesRegex(ValueError, "RECEIPT_AGGREGATE_BUDGET"): budget.begin(1)
        with self.assertRaisesRegex(ValueError, "RECEIPT_PRIVATE_TICKET"): budget.settle(ticket+1, 1)
        budget.settle(ticket)
        self.assertEqual(budget.used["reply_bytes"], 1024)
        with self.assertRaisesRegex(ValueError, "RECEIPT_AGGREGATE_BUDGET"): budget.begin(1)
        with self.assertRaisesRegex(ValueError, "RECEIPT_PREALLOCATION_PHASE"): budget.charge_external("renew", 0, 0)
        budget.verification(len(OPAQUE), 30); budget.verification(len(OPAQUE), 30)
        with self.assertRaisesRegex(ValueError, "RECEIPT_VERIFY_BUDGET"): budget.verification(len(OPAQUE), 1)
        self.assertEqual(budget.used["worker_cpu_seconds"], 60)
        # An expired private owner deadline fails even before the base verifier's
        # initialized state is available. No verifier executable is constructed.
        verifier = object.__new__(DeadlineReceiptVerifier); verifier.outer_deadline = time.monotonic()-1
        with self.assertRaisesRegex(ValueError, "RECEIPT_ORIGINAL_DEADLINE"): verifier._active()
        budget.closed = True
        with self.assertRaisesRegex(ValueError, "RECEIPT_WORKFLOW_CLOSED_OR_EXPIRED"): budget.active()


def main():
    global EVIDENCE
    parser = argparse.ArgumentParser(); parser.add_argument("--evidence", required=True)
    EVIDENCE = Path(parser.parse_args().evidence)
    if not EVIDENCE.is_absolute() or EVIDENCE.exists(): raise ValueError("FRESH_ABSOLUTE_TEST_EVIDENCE")
    EVIDENCE.mkdir(parents=True)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ReceiptControls)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"schema": "DMKN_RECEIPT_STRUCTURAL_CONTROLS_V1", "status": "PASS" if result.wasSuccessful() else "FAIL",
              "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
              "skipped": len(result.skipped), "details": REPORTS,
              "mathematical_acceptance": False, "genuine_receipt_verification": "NOT_RUN",
              "hosting": "SAME_HOST_LOOPBACK_ONLY"}
    with (EVIDENCE/"RESULT.json").open("xb") as stream: stream.write(F.compact(report))
    print(json.dumps({key: report[key] for key in ("status", "tests_run", "failures", "errors", "mathematical_acceptance")}))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

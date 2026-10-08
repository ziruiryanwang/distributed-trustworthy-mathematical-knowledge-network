"""Focused actual loopback/SQLite controls. Structural fixtures are not proofs."""
from pathlib import Path
import argparse
import asyncio
from copy import deepcopy
import hashlib
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C
from discovery import formal_features as F
from discovery.module_export_adapter import ModuleExportAdapter, feature_id
from discovery.discovery_store import Store
from discovery.search_session import SearchSession
from custody.module_store import ModuleStore, BODY_SCHEMA
from transport.http_provider import Provider, Endpoint, exchange, _header
from transport.clients import SearchClient, AcquisitionClient

EVIDENCE = None
INDEX_LIMITS = dict(max_objects=32, max_postings=4096, max_features=4096,
                    max_snapshots=33, max_logical_bytes=33554432, max_db_pages=16384)
CUSTODY_LIMITS = dict(modules=8, groups=32, declarations=64, bodies=32,
                      logical_bytes=16777216, db_pages=8192)
SESSION_LIMITS = dict(providers=2, snapshots=2, requests=16, pages=8, examined=32,
                     candidates=16, bytes=1048576, wall_ms=30000, inflight=2)
PAGE_LIMITS = dict(examined=2, matches=1, bytes=16384, timeout_ms=1000, node_reads=100000)


def h(text): return hashlib.sha256(text.encode("ascii")).hexdigest()


def fixture():
    expression = ["sort", ["zero"]]
    digest = C.body_id(expression, 0)
    spec = {"schema": C.SPEC_SCHEMA, "foundation": h("transport-foundation"),
            "policy": h("transport-policy"), "groups": [
                {"kind": "ordinary", "declarations": [{"name": [["s", name]], "kind": "definition",
                 "universes": 0, "type": ["sort", ["succ", ["zero"]]], "value_hash": digest,
                 "meta": {"hint": "abbrev", "safety": "safe"}}]} for name in ("First", "Second")]}
    return spec, expression, digest


class ProviderControls(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.root = EVIDENCE / self._testMethodName; self.root.mkdir()
        self.spec, self.expression, self.digest = fixture()
        self.module = C.module_id(self.spec)
        self.adapter = ModuleExportAdapter(C, self.spec["foundation"], self.spec["policy"])
        self.stores, self.providers = [], []

    async def asyncTearDown(self):
        for provider in reversed(self.providers): await provider.stop()
        for store in reversed(self.stores): store.close()

    def custody(self, name, *, create=True, limits=None):
        store = ModuleStore(self.root/name, C, self.spec["foundation"], self.spec["policy"],
                            limits or CUSTODY_LIMITS, create=create)
        self.stores.append(store); return store

    def body(self, name):
        return {"schema": BODY_SCHEMA, "module_id": self.module, "relative_name": [["s", name]],
                "universes": 0, "body_hash": self.digest, "expression": self.expression}

    def index(self, name):
        store = Store(self.root/name, self.adapter, INDEX_LIMITS, create=True)
        self.stores.append(store)
        for i, group in enumerate(self.spec["groups"]):
            store.admit(self.adapter.encode_opening(self.module, group["declarations"][0]["name"], C.group_opening(self.spec, i)))
        return store

    async def start(self, **kwargs):
        provider = Provider(**kwargs); self.providers.append(provider)
        endpoint = await provider.start(); return provider, endpoint

    async def test_provider_loss_continuation_and_custody_restart(self):
        index_a, index_b, custody = self.index("a"), self.index("b"), self.custody("custody")
        for i in range(2): custody.put_group(self.module, C.group_opening(self.spec, i))
        custody.put_body(self.module, [["s", "First"]], self.body("First"))
        provider_a, endpoint_a = await self.start(index=index_a)
        _, endpoint_b = await self.start(index=index_b)
        provider_c, endpoint_c = await self.start(custody=custody)
        sid = index_a.status()["latest"]
        self.assertEqual(sid, index_b.status()["latest"])
        feature = feature_id(self.adapter.namespace, {"tag": "declaration-kind", "value": "definition"})
        session = SearchSession(self.adapter.namespace, [feature], SESSION_LIMITS)
        client = SearchClient(session, {"a": endpoint_a, "b": endpoint_b})
        summary = await client.summary("a", sid, 65536)
        plan = next(p for p in summary["partitions"] if p["anchor_count"])
        first = await client.page("a", sid, plan["partition"], 0, PAGE_LIMITS)
        await provider_a.stop()
        with self.assertRaises(Exception): await client.page("a", sid, plan["partition"], 0, PAGE_LIMITS)
        repeated = await client.page("b", sid, plan["partition"], 0, PAGE_LIMITS)
        self.assertEqual(first["matches"], repeated["matches"])
        candidate = repeated["matches"][0]
        receiver = self.custody("receiver")
        acquisition = AcquisitionClient(self.adapter, {"c": endpoint_c}, requests=4, bytes=1048576,
                                        wall_ms=30000, local_custody=receiver)
        resolved = await acquisition.export("c", candidate)
        self.assertNotEqual(resolved["export_id"], self.module)
        await provider_c.stop(); custody.close()
        reopened = self.custody("custody", create=False)
        _, replacement = await self.start(custody=reopened)
        acquisition.endpoints["c"] = replacement
        body = await acquisition.body("c", resolved, self.digest, 65536)
        self.assertEqual(body["body"]["expression"], self.expression)
        self.assertFalse(body["mathematical_acceptance"])
        self.assertEqual(client.report()["session"]["pending_requests"], 0)
        self.assertEqual(client.report()["http"]["failed_requests"], 1)

    async def test_custody_commit_deadline_and_quota_fail_atomically(self):
        store = self.custody("custody", limits={**CUSTODY_LIMITS, "groups": 1})
        def expired(): raise ValueError("EXPIRED_BEFORE_COMMIT")
        with self.assertRaisesRegex(ValueError, "EXPIRED_BEFORE_COMMIT"):
            store.put_group(self.module, C.group_opening(self.spec, 0), before_commit=expired)
        self.assertEqual(store.status()["counts"]["groups"], 0)
        self.assertEqual(store.status()["counts"]["modules"], 0)
        store.put_group(self.module, C.group_opening(self.spec, 0))
        before = deepcopy(store.status())
        with self.assertRaises(ValueError): store.put_group(self.module, C.group_opening(self.spec, 1))
        self.assertEqual(store.status(), before)
        with self.assertRaisesRegex(ValueError, "EXPIRED_BEFORE_COMMIT"):
            store.put_body(self.module, [["s", "First"]], self.body("First"), before_commit=expired)
        self.assertEqual(store.status(), before)
        bad = self.body("First"); bad["expression"] = ["sort", ["succ", ["zero"]]]
        with self.assertRaises(ValueError): store.put_body(self.module, [["s", "First"]], bad)
        self.assertEqual(store.status(), before)

    async def test_readonly_routes_and_declared_request_overflow_close(self):
        store = self.custody("custody")
        provider, endpoint = await self.start(custody=store)
        with self.assertRaises(ValueError):
            await exchange(endpoint, "/v5/modules/write", {}, 1024, 1000)
        reader, writer = await asyncio.open_connection(endpoint.host, endpoint.port)
        writer.write(_header("POST /v5/modules/group HTTP/1.1", 16385, "127.0.0.1")); await writer.drain()
        try:
            self.assertEqual(await asyncio.wait_for(reader.read(1), 2), b"")
        finally: writer.close(); await writer.wait_closed()
        self.assertEqual(store.status()["counts"]["groups"], 0)
        self.assertEqual(provider.status()["failures"], 1)

    async def test_client_rejects_oversized_truncated_and_corrupt_responses(self):
        servers = []
        async def fake(reader, writer, variant):
            try:
                header = await reader.readuntil(b"\r\n\r\n")
                count = int(next(x for x in header.decode().split("\r\n") if x.startswith("Content-Length:")).split(":")[1])
                await reader.readexactly(count)
                if variant == "oversized": writer.write(_header("HTTP/1.1 200 OK", 2048))
                else: writer.write(_header("HTTP/1.1 200 OK", 20)+b"{}")
                await writer.drain()
            finally: writer.close(); await writer.wait_closed()
        try:
            for variant in ("oversized", "truncated"):
                async def serve(reader, writer, selected=variant): await fake(reader, writer, selected)
                server = await asyncio.start_server(serve, "127.0.0.1", 0); servers.append(server)
                endpoint = Endpoint("127.0.0.1", server.sockets[0].getsockname()[1])
                with self.assertRaises(Exception):
                    await exchange(endpoint, "/v5/modules/group", {}, 1024, 1000)
        finally:
            for server in servers: server.close(); await server.wait_closed()
        store = self.custody("custody")
        store.put_group(self.module, C.group_opening(self.spec, 0))
        store.put_body(self.module, [["s", "First"]], self.body("First"))
        store.db.execute("UPDATE bodies SET expression=?", (C.canonical(["sort", ["succ", ["zero"]]]),))
        with self.assertRaises(ValueError): store.get_body(self.module, [["s", "First"]], 0, self.digest)

    async def test_nonloopback_plaintext_endpoint_refuses(self):
        with self.assertRaises(ValueError): Endpoint("192.0.2.1", 443).validate()
        self.assertTrue(Endpoint("192.0.2.1", 443, tls=True).validate().tls)


def main():
    global EVIDENCE
    parser = argparse.ArgumentParser(); parser.add_argument("--evidence", required=True)
    EVIDENCE = Path(parser.parse_args().evidence)
    if not EVIDENCE.is_absolute() or EVIDENCE.exists(): raise ValueError("FRESH_ABSOLUTE_TEST_EVIDENCE")
    EVIDENCE.mkdir(parents=True)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ProviderControls)
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

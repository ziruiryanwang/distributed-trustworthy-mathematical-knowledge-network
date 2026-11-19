"""Changed-boundary controls: real index/session, in-memory async HTTP streams.

No mathematical checker, native build, socket, subprocess or retained state.
The old fixture supplies synthetic committed metadata, not mathematical truth.
Root separately selects a single finite run after independent source review.
"""
from __future__ import annotations

import argparse
import asyncio
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def modules(root):
    for name in ("discovery", "transport", "custody"):
        package = types.ModuleType(name)
        package.__path__ = [str(root / name)]
        sys.modules[name] = package
    # Bind the selected ordinary provider, not the older same-named source.
    provider = load("transport.http_provider", root / "ordinary_authoring_offers/http_provider.py")
    exchange = load("transport.fair_exchange", root / "ordinary_fair_search/fair_exchange.py")
    search = load("discovery.fair_search", root / "ordinary_fair_search/fair_search.py")
    from discovery import formal_features
    from discovery.search_session import SearchSession
    from discovery.test_candidate_query import Fixture, NS, FEATURES, LIMITS, Clock
    return provider, exchange, search, formal_features, SearchSession, Fixture, NS, FEATURES, LIMITS, Clock


class SelectedIndex:
    def __init__(self, store, sid):
        self.store, self.sid = store, sid
        self.namespace, self.db = store.namespace, store.db
    def snapshot(self): return self.store.snapshot(self.sid)
    def summary(self, *args): return self.store.summary(*args)
    def page(self, request): return self.store.page(request)


class MemoryWriter:
    def __init__(self, reader, provider, mode, calls, label):
        self.reader, self.provider, self.mode = reader, provider, mode
        self.calls, self.label = calls, label
        self.buffer, self.closed, self.waits, self.answered = bytearray(), False, 0, False
    def write(self, raw): self.buffer.extend(raw)
    def close(self): self.closed = True
    async def wait_closed(self):
        self.waits += 1
        if self.mode == "dirty": raise OSError("CONTROL_DIRTY_CLOSURE")
    async def drain(self):
        if self.mode == "cancel": raise asyncio.CancelledError("CONTROL_CANCEL")
        if self.answered or b"\r\n\r\n" not in self.buffer: return
        head, body = bytes(self.buffer).split(b"\r\n\r\n", 1)
        length = int(next(line.split(b":", 1)[1] for line in head.split(b"\r\n")
                          if line.lower().startswith(b"content-length:")))
        if len(body) < length: return
        self.answered = True
        route = head.split(b"\r\n", 1)[0].decode("ascii").split(" ")[1]
        self.calls.append((self.label, route))
        if self.mode == "stall" or (self.mode == "stall-page" and route == H.CANDIDATE_ROUTE):
            return
        value = self.provider.dispatch(route, F.strict(body, H.REQUEST_MAX))
        raw = value if type(value) is bytes else F.compact(value)
        if self.mode == "invalid-json":
            raw = b"not-json"
        if self.mode == "no-progress" and route == H.CANDIDATE_ROUTE:
            from discovery import candidate_query as C
            request = F.strict(body, H.REQUEST_MAX)
            answer = F.strict(raw, 1048576)
            answer.update(hits=[], next=request["start"], termination="time_exhausted",
                          charged={key: 0 for key in C.CHARGES},
                          next_cursor=C.cursor(request, answer["query_id"], request["start"]))
            raw = F.compact(answer)
        if self.mode == "invalid-proof" and route == H.CANDIDATE_ROUTE:
            answer = F.strict(raw, 1048576)
            answer["hits"][0]["siblings"][0] = "f" * 64
            raw = F.compact(answer)
        wire = H._header("HTTP/1.1 200 Control", len(raw)) + raw
        self.reader.feed_data(wire)
        self.reader.feed_eof()


class Dial:
    def __init__(self, provider, mode="normal"):
        self.provider, self.mode = provider, mode
        self.connections, self.calls, self.writers, self.options = [], [], [], []
    async def __call__(self, host, port, **kwargs):
        label = "a" if port == 20001 else "b"
        self.connections.append(label); self.options.append(kwargs)
        mode = self.mode if label == "a" else "normal"
        if mode == "refused": raise ConnectionRefusedError("CONTROL_REFUSED")
        if mode == "connect-timeout": await asyncio.Event().wait()
        if mode == "connect-reset": raise ConnectionResetError("CONTROL_CONNECT_RESET")
        if mode == "local": raise OSError("CONTROL_LOCAL_FAILURE")
        reader = asyncio.StreamReader(limit=H.HEADER_MAX)
        writer = MemoryWriter(reader, self.provider, mode, self.calls, label)
        self.writers.append(writer)
        return reader, writer


SESSION = dict(providers=4, snapshots=8, requests=24, pages=16, examined=512,
               candidates=128, bytes=4*1024**2, wall_ms=60000, inflight=1)
OFFER = dict(max_bytes=16384, max_expanded_bytes=1048576, max_age_ms=60000)


class FairControls(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls): cls.fixture = Fixture()
    @classmethod
    def tearDownClass(cls): cls.fixture.db.close()
    def setUp(self):
        self.store = self.fixture.store()
        self.addCleanup(self.store.close)
        self.provider = H.Provider(index=SelectedIndex(self.store, self.fixture.snapshots[0]))
        self.clock = Clock()

    def client(self, **limits):
        session = SearchSession(NS, FEATURES, {**SESSION, **limits}, clock=self.clock)
        return S.FairSearch(session, {"a": H.Endpoint("127.0.0.1", 20001),
                                      "b": H.Endpoint("127.0.0.1", 20002)})

    async def search(self, client, dial, *, page=None, attempt=50):
        original = (id(client.session), client.session.deadline, deepcopy(client.session.limits))
        with patch.object(X.asyncio, "open_connection", new=dial):
            value = await client.run(["a", "b"], dict(OFFER), dict(PAGE if page is None else page),
                attempt_timeout_ms=attempt, check_owner=lambda: None,
                recover_metadata_failure=lambda error: False)
        self.assertEqual((id(client.session), client.session.deadline, client.session.limits), original)
        self.assertEqual(client.session.pending, {})
        self.assertTrue(all(x == 0 for x in client.session.reserved.values()))
        self.assertFalse(value["global_complete"])
        self.assertFalse(value["verified_scan_coverage"])
        return value

    async def test_rounds_before_second_page(self):
        client, dial = self.client(), Dial(self.provider)
        value = await self.search(client, dial, page={**PAGE, "scanned": 5})
        self.assertEqual(dial.calls[:4], [("a", H.OFFER_ROUTE), ("b", H.OFFER_ROUTE),
            ("a", H.CANDIDATE_ROUTE), ("b", H.CANDIDATE_ROUTE)])
        self.assertGreaterEqual(len(dial.calls), 6)
        self.assertTrue(value["matches"])
        self.assertEqual(client.session.used["requests"], len(dial.connections))

    async def test_stalled_offer_preserves_later_hit_and_full_charge(self):
        client, dial = self.client(), Dial(self.provider, "stall")
        value = await self.search(client, dial)
        self.assertTrue(value["matches"])
        self.assertTrue(all(row["provider"] == "b" for row in value["matches"]))
        self.assertEqual(dial.connections.count("a"), 1)
        self.assertGreaterEqual(client.session.used["bytes"], OFFER["max_bytes"])
        self.assertTrue(dial.writers[0].closed)
        self.assertEqual(dial.writers[0].waits, 1)
        self.assertTrue(value["provider_errors"])

    async def test_stalled_page_keeps_scan_charge_and_later_hit(self):
        client, dial = self.client(), Dial(self.provider, "stall-page")
        value = await self.search(client, dial)
        self.assertTrue(value["matches"])
        self.assertEqual(dial.connections.count("a"), 2)
        self.assertEqual(client.session.used["examined"], 2*PAGE["scanned"])
        self.assertEqual(client.session.used["candidates"], PAGE["matches"]+1)
        self.assertEqual(client.session.last_verified, {})

    async def test_refused_connection_can_continue(self):
        client, dial = self.client(), Dial(self.provider, "refused")
        value = await self.search(client, dial)
        self.assertTrue(value["matches"])
        self.assertEqual(dial.connections.count("a"), 1)
        self.assertEqual(client.session.pending, {})

    async def fatal(self, mode, error=Exception):
        client, dial = self.client(), Dial(self.provider, mode)
        with self.assertRaises(error): await self.search(client, dial)
        self.assertEqual(dial.connections, ["a"])
        self.assertEqual(client.session.pending, {})
        self.assertTrue(all(x == 0 for x in client.session.reserved.values()))
        self.assertEqual(client.session.used["requests"], 1)
        self.assertEqual(client.session.used["bytes"], OFFER["max_bytes"])
        return client, dial

    async def test_dirty_close_is_fatal(self): await self.fatal("dirty")
    async def test_external_cancel_is_fatal(self): await self.fatal("cancel", asyncio.CancelledError)
    async def test_unreturned_connect_timeout_is_fatal(self): await self.fatal("connect-timeout")
    async def test_unreturned_connect_reset_is_fatal(self): await self.fatal("connect-reset")
    async def test_unknown_local_failure_is_fatal(self): await self.fatal("local")

    async def test_invalid_membership_never_becomes_a_hit(self):
        client, dial = self.client(), Dial(self.provider, "invalid-proof")
        with self.assertRaises(ValueError): await self.search(client, dial)
        self.assertEqual(client.result()["matches"], [])
        self.assertEqual(client.session.seen_candidates, {})
        self.assertEqual(client.session.pending, {})
        self.assertEqual(client.session.used["examined"], PAGE["scanned"])
        self.assertEqual(client.session.used["candidates"], PAGE["matches"])
        self.assertNotIn(("b", H.CANDIDATE_ROUTE), dial.calls)

    async def test_insufficient_cleanup_slice_dials_nobody(self):
        client, dial = self.client(), Dial(self.provider)
        self.clock.value = 59.9
        value = await self.search(client, dial)
        self.assertEqual(dial.connections, [])
        self.assertEqual(value["status"], "INCOMPLETE_SEARCH")
        self.assertIsNotNone(value["termination"])

    async def test_single_use_cannot_renew_grant(self):
        client, dial = self.client(), Dial(self.provider)
        await self.search(client, dial)
        used = deepcopy(client.session.used); count = len(dial.connections)
        with self.assertRaises(ValueError): await self.search(client, dial)
        self.assertEqual(client.session.used, used)
        self.assertEqual(len(dial.connections), count)

    async def test_request_cap_preserves_partial_offers(self):
        client, dial = self.client(requests=1), Dial(self.provider)
        value = await self.search(client, dial)
        self.assertEqual(value["termination"], "SESSION_BUDGET:requests")
        self.assertEqual(dial.connections, ["a"])
        self.assertEqual(len(value["offers"]), 1)
        self.assertEqual(client.session.used["requests"], 1)

    async def test_only_explicit_metadata_refusal_can_continue(self):
        client, dial = self.client(), Dial(self.provider, "invalid-json")
        with patch.object(X.asyncio, "open_connection", new=dial):
            value = await client.run(["a", "b"], dict(OFFER), dict(PAGE),
                attempt_timeout_ms=50, check_owner=lambda: None,
                recover_metadata_failure=lambda error: type(error) is json.JSONDecodeError)
        self.assertTrue(value["matches"])
        self.assertEqual(dial.connections.count("a"), 1)
        self.assertEqual(client.session.pending, {})
        self.assertTrue(value["provider_errors"])

    async def test_owner_grant_mutation_refuses_before_dial(self):
        client, dial = self.client(), Dial(self.provider)
        def altered_owner(): client.session.deadline += 1
        with patch.object(X.asyncio, "open_connection", new=dial), self.assertRaisesRegex(
                ValueError, "FAIR_OWNER_OR_GRANT_CHANGED"):
            await client.run(["a", "b"], dict(OFFER), dict(PAGE), attempt_timeout_ms=50,
                check_owner=altered_owner, recover_metadata_failure=lambda error: True)
        self.assertEqual(dial.connections, [])
        self.assertEqual(client.session.pending, {})

    async def test_nonprogress_cursor_does_not_suppress_other_provider(self):
        client, dial = self.client(), Dial(self.provider, "no-progress")
        value = await self.search(client, dial)
        self.assertTrue(value["matches"])
        self.assertTrue(all(row["provider"] == "b" for row in value["matches"]))
        self.assertEqual(dial.connections.count("a"), 2)
        self.assertEqual(client.session.last_verified, {})


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source, output = Path(args.source_root), Path(args.output)
    if not source.is_absolute() or not output.is_absolute() or output.exists():
        raise ValueError("CONTROL_ABSOLUTE_FRESH_OUTPUT")
    if not output.parent.is_dir(): raise ValueError("CONTROL_EXISTING_PARENT")
    global H, X, S, F, SearchSession, Fixture, NS, FEATURES, PAGE, Clock
    H, X, S, F, SearchSession, Fixture, NS, FEATURES, PAGE, Clock = modules(source)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(FairControls)
    output.mkdir()
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    report = dict(tests=result.testsRun, failures=len(result.failures),
                  errors=len(result.errors), skipped=len(result.skipped), passed=result.wasSuccessful(),
                  authority="SYNTHETIC_METADATA_REAL_SESSION_MEMORY_HTTP_NOT_MATHEMATICS_OR_TCP")
    with (output/"RESULT.json").open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, sort_keys=True)+"\n")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

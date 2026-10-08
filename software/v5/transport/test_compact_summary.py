"""Changed compact-route/session contracts; memory streams, not network evidence.

Reuse the already qualified wire fixture without rerunning its seven tests.
Root separately owns one retained-summary real-loopback comparison.
"""
import asyncio
from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import formal_features as F
from discovery import discovery_query as Q
from discovery import summary_wire as W
from discovery.search_session import SearchSession
from discovery.test_summary_wire import fixture
from transport import clients as C
from transport import http_provider as H


LIMITS = dict(providers=2, snapshots=2, requests=8, pages=8, examined=64,
              candidates=64, bytes=2097152, wall_ms=60000, inflight=2)


class IndexFixture:
    def __init__(self, namespace, sid, features, summary):
        self.namespace, self.sid, self.features, self.summary_value = namespace, sid, features, summary
        self.calls = []
    def summary(self, sid, features, max_bytes):
        self.calls.append(max_bytes)
        F.need(sid == self.sid and features == self.features, "FIXTURE_QUERY_BINDING")
        F.need(len(F.compact(self.summary_value)) <= max_bytes, "FIXTURE_EXPANDED_BYTE_CAP")
        return deepcopy(self.summary_value)


class MemoryWriter:
    def __init__(self): self.data, self.closed = bytearray(), False
    def write(self, data):
        F.need(len(self.data)+len(data) <= 2*1048576, "MEMORY_TRANSPORT_BOUND")
        self.data.extend(data)
    async def drain(self): pass
    def close(self): self.closed = True
    async def wait_closed(self): pass


async def memory_request(provider, route, request):
    body = F.compact(request)
    reader, writer = asyncio.StreamReader(limit=H.HEADER_MAX), MemoryWriter()
    reader.feed_data(H._header("POST "+route+" HTTP/1.1", len(body), "127.0.0.1:1")+body)
    reader.feed_eof()
    await provider._serve(reader, writer)
    F.need(writer.closed, "MEMORY_TRANSPORT_CLOSED")
    return bytes(writer.data)


class CompactSummaryContracts(unittest.TestCase):
    def setUp(self):
        self.ns, self.sid, self.features, self.expanded, self.sparse, self.names, _ = fixture()
        self.raw, self.expanded_raw = F.compact(self.sparse), F.compact(self.expanded)
        self.wire_cap, self.expanded_cap = max(1024, len(self.raw)), len(self.expanded_raw)

    def session(self, **kwargs): return SearchSession(self.ns, self.features, LIMITS, **kwargs)

    def request(self):
        return {"snapshot_id": self.sid, "features": self.features, "max_bytes": self.wire_cap,
                "max_expanded_bytes": self.expanded_cap}

    def test_client_selects_explicit_compact_route_and_charges_real_wire(self):
        index = IndexFixture(self.ns, self.sid, self.features, self.expanded)
        provider, session, calls = H.Provider(index=index), self.session(), []
        async def exchange(endpoint, route, request, maximum, timeout):
            calls.append((route, deepcopy(request), maximum))
            raw = provider.dispatch(route, request)
            self.assertIs(type(raw), bytes)
            self.assertLessEqual(len(raw), maximum)
            return {"status": 200, "raw": raw, "request_bytes": len(F.compact(request)),
                    "reply_bytes": len(raw), "header_bytes": 0}
        client = C.SearchClient(session, {"p": H.Endpoint("127.0.0.1", 1)})
        with patch.object(C, "exchange", new=exchange):
            result = asyncio.run(client.summary("p", self.sid, self.wire_cap,
                encoding="compact-v1", max_expanded_bytes=self.expanded_cap))
        self.assertEqual(result["status"], "VERIFIED_SUMMARY")
        self.assertEqual(calls, [(H.COMPACT_SUMMARY_ROUTE, self.request(), self.wire_cap)])
        self.assertEqual(index.calls, [self.expanded_cap])
        report = client.report()
        self.assertEqual(report["session"]["used"]["bytes"], len(self.raw))
        self.assertEqual(report["http"]["actual_reply_bytes"], len(self.raw))
        self.assertEqual(report["session"]["reserved"]["bytes"], 0)
        self.assertLess(report["session"]["used"]["bytes"], len(self.expanded_raw))
        self.assertEqual(session.summaries[self.sid], Q.verify_summary(self.sid, self.ns, self.features, self.expanded))

    def test_expanded_default_stays_compatible_and_no_format_fallback(self):
        index = IndexFixture(self.ns, self.sid, self.features, self.expanded)
        provider, calls, session = H.Provider(index=index), [], self.session()
        async def exchange(endpoint, route, request, maximum, timeout):
            calls.append((route, deepcopy(request)))
            raw = F.compact(provider.dispatch(route, request))
            return {"status": 200, "raw": raw, "request_bytes": len(F.compact(request)),
                    "reply_bytes": len(raw), "header_bytes": 0}
        client = C.SearchClient(session, {"p": H.Endpoint("127.0.0.1", 1)})
        with patch.object(C, "exchange", new=exchange): asyncio.run(client.summary("p", self.sid))
        self.assertEqual(calls, [("/v5/discovery/summary", {"snapshot_id": self.sid,
                                "features": self.features, "max_bytes": 1048576})])
        self.assertEqual(session.used["bytes"], len(self.expanded_raw))
        for encoding, unexpected in (("expanded-v1", self.raw), ("compact-v1", self.expanded_raw)):
            refused = self.session()
            ticket = refused.begin_summary("p", self.sid, 1048576, encoding=encoding)
            with self.subTest(encoding=encoding), self.assertRaises(ValueError): refused.accept(ticket["ticket"], unexpected)
            self.assertEqual(refused.used["bytes"], len(unexpected))
            self.assertEqual(refused.summaries, {}); self.assertEqual(refused.coverage, {})
            self.assertEqual(refused.used["requests"], 1)

    def test_private_ticket_pins_and_bad_proof_costs_survive_without_retry(self):
        session = self.session()
        ticket = session.begin_summary("p", self.sid, self.wire_cap, encoding="compact-v1",
                                       max_expanded_bytes=self.expanded_cap)
        number = ticket["ticket"]
        ticket["summary_encoding"] = "expanded-v1"; ticket["max_expanded_bytes"] = 1
        ticket["request"]["features"].clear()
        self.assertEqual(session.accept(number, self.raw)["status"], "VERIFIED_SUMMARY")
        failed = self.session(); broken = deepcopy(self.sparse)
        filled = self.features.index(self.names[0]); broken["rows"][filled]["siblings"].pop()
        raw = F.compact(broken)
        pending = failed.begin_summary("p", self.sid, self.wire_cap, encoding="compact-v1")
        with self.assertRaisesRegex(ValueError, "MAP_PROOF_ROOT"): failed.accept(pending["ticket"], raw)
        self.assertEqual(failed.used["bytes"], len(raw)); self.assertEqual(failed.coverage, {})
        self.assertEqual(failed.pending, {}); self.assertEqual(failed.reserved["bytes"], 0)
        with self.assertRaisesRegex(ValueError, "SESSION_TICKET_NOT_PENDING"):
            failed.accept(pending["ticket"], self.raw)
        self.assertEqual(failed.used["bytes"], len(raw)); self.assertEqual(failed.used["requests"], 1)

    def test_wire_and_expansion_caps_refuse_without_verified_state(self):
        for encoding, raw in (("compact-v1", self.raw), ("expanded-v1", self.expanded_raw)):
            session = self.session()
            ticket = session.begin_summary("p", self.sid, 1048576, encoding=encoding,
                                           max_expanded_bytes=self.expanded_cap-1)
            with self.subTest(encoding=encoding), self.assertRaises(ValueError): session.accept(ticket["ticket"], raw)
            self.assertEqual(session.used["bytes"], len(raw)); self.assertEqual(session.summaries, {})
            self.assertEqual(session.reserved["bytes"], 0)
        session = self.session(); before = session.report()
        for kwargs in ({"encoding": "automatic"}, {"max_expanded_bytes": True},
                       {"max_expanded_bytes": 1048577}, {"max_expanded_bytes": 1023}):
            with self.assertRaises(ValueError): session.begin_summary("p", self.sid, self.wire_cap, **kwargs)
        self.assertEqual(session.used, {k: before["used"][k] for k in session.used})
        self.assertEqual(session.pending, {})

    def test_deadline_during_decode_and_after_verify_preserves_no_coverage(self):
        class Clock:
            value = 0
            def __call__(self): return self.value
        for boundary in ("decode", "verify"):
            clock = Clock(); session = self.session(clock=clock)
            ticket = session.begin_summary("p", self.sid, self.wire_cap, encoding="compact-v1")
            if boundary == "decode":
                original = W.decode_summary
                def decode(*args, **kwargs):
                    guard = kwargs["check_budget"]; calls = 0
                    def deadline():
                        nonlocal calls
                        calls += 1
                        if calls == 2: clock.value = 1000
                        guard()
                    kwargs["check_budget"] = deadline
                    return original(*args, **kwargs)
                context = patch.object(W, "decode_summary", new=decode)
            else:
                original = Q.verify_summary
                def verify(*args, **kwargs):
                    result = original(*args, **kwargs); clock.value = 1000; return result
                context = patch.object(Q, "verify_summary", new=verify)
            with context, self.subTest(boundary=boundary), self.assertRaisesRegex(ValueError, "SESSION_DEADLINE_EXHAUSTED"):
                session.accept(ticket["ticket"], self.raw)
            self.assertEqual(session.used["bytes"], len(self.raw)); self.assertEqual(session.summaries, {})
            self.assertEqual(session.coverage, {}); self.assertEqual(session.reserved["bytes"], 0)

    def test_memory_stream_provider_reserves_wire_cap_not_expanded_cap(self):
        index = IndexFixture(self.ns, self.sid, self.features, self.expanded)
        provider = H.Provider(index=index, max_reply_bytes=self.wire_cap)
        first = asyncio.run(memory_request(provider, H.COMPACT_SUMMARY_ROUTE, self.request()))
        header, body = first.split(b"\r\n\r\n", 1)
        self.assertTrue(header.startswith(b"HTTP/1.1 200 OK")); self.assertEqual(body, self.raw)
        self.assertEqual(provider.status()["reply_bytes"], len(self.raw))
        second = asyncio.run(memory_request(provider, H.COMPACT_SUMMARY_ROUTE, self.request()))
        self.assertEqual(second, b"")
        self.assertEqual(index.calls, [self.expanded_cap])
        self.assertEqual(provider.status()["failures"], 1)
        self.assertEqual(provider.status()["reserved_reply_bytes"], 0)
        self.assertEqual(provider.status()["active"], 0)

    def test_provider_expansion_and_canonical_request_refusals(self):
        index = IndexFixture(self.ns, self.sid, self.features, self.expanded)
        provider = H.Provider(index=index)
        for field, value in (("max_bytes", 1023), ("max_bytes", 1048577),
                             ("max_expanded_bytes", True), ("max_expanded_bytes", 1048577)):
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                provider.dispatch(H.COMPACT_SUMMARY_ROUTE, {**self.request(), field: value})
        self.assertEqual(index.calls, [])
        with self.assertRaises(ValueError):
            provider.dispatch(H.COMPACT_SUMMARY_ROUTE, {**self.request(), "encoding": "guess"})
        with self.assertRaisesRegex(ValueError, "FIXTURE_EXPANDED_BYTE_CAP"):
            provider.dispatch(H.COMPACT_SUMMARY_ROUTE, {**self.request(), "max_expanded_bytes": self.expanded_cap-1})
        def refuse(): raise ValueError("OWNER_PROVIDER_DEADLINE")
        with self.assertRaisesRegex(ValueError, "OWNER_PROVIDER_DEADLINE"):
            provider.dispatch(H.COMPACT_SUMMARY_ROUTE, self.request(), check_budget=refuse)
        self.assertEqual(index.calls, [self.expanded_cap-1])


if __name__ == "__main__": unittest.main(verbosity=2)

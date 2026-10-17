"""Focused search-continuation controls; inert owners, one real loopback read.

Only the new suite runs. The imported index fixture supplies synthetic metadata,
not mathematics. Facade construction/liveness/census are inert, while its actual
async methods, entry/decorator and fail-stop cleanup remain active. No issuer,
Lean, proof, compiler, subprocess or external network operation is performed.
"""
import argparse
import asyncio
from copy import deepcopy
import errno
import hashlib
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE))
from client import workspace_resilient as W
from client.workspace_atomic import LiveWarrant
from discovery import formal_features as F
from discovery.search_session import SearchSession
from discovery.test_candidate_query import Fixture, Clock, NS, FEATURES, P, LIMITS as CANDIDATE_LIMITS
from location.protocol import OwnerEgressPolicy
from location.workflow import _LocatedSearchClient
from transport import http_provider as H, search_resilience as R

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SESSION_LIMITS = dict(providers=4, snapshots=8, requests=16, pages=8, examined=256,
                      candidates=64, bytes=2097152, wall_ms=60000, inflight=1)
PAGE_LIMITS = dict(examined=32, matches=8, bytes=65536, timeout_ms=1000, node_reads=100000)
OFFER_BYTES = 16384
SOCKET_EVIDENCE = []


class InertOwner:
    def __init__(self): self.closes = 0
    def close(self): self.closes += 1


class InertFacade(W.CommonsClient):
    """Only lifetime fixture; it does not issue or validate mathematical tokens."""
    def __init__(self, search):
        self._search = search
        self.grant = SimpleNamespace(identifier="SYNTHETIC-NOT-ISSUED-GRANT", _limits={"calls": 64})
        self.owner_records = []
        self.workspace = SimpleNamespace(_poisoned=False, _record=lambda *row: self.owner_records.append(row))
        self._origin_owners = (InertOwner(), InertOwner(), InertOwner(), None)
        self._session = None
        self._budget = SimpleNamespace(closed=False)
        self._state, self._busy, self._closed = "OPEN", False, False
        self._calls, self._cleanup_uncertain, self._failures = 0, False, []
        self.token, self.context = LiveWarrant(), object()
        self._warrants = {self.token: ("SYNTHETIC-NOT-AUTHORITY", object())}
        self._context, self._selection_view = self.context, self.context
        self._receipt_cache, self._packet_cache, self._aggregate_cache, self._candidates = {}, {}, {}, {}

    def _active(self):
        F.need(self._state == "OPEN" and not self._closed and not self._budget.closed,
               "SYNTHETIC_CLIENT_NOT_LIVE")
        F.need(all(o is None or o.closes == 0 for o in self._origin_owners), "SYNTHETIC_ORIGIN_CLOSED")

    def _census(self): return {"scope": "INERT_NO_WORKSPACE_CENSUS"}
    def report(self): return {"status": self._state, "authority": "SYNTHETIC_NOT_MATHEMATICS"}


class SelectedIndex:
    def __init__(self, store, sid):
        self.store, self.sid, self.namespace, self.db = store, sid, store.namespace, store.db
    def snapshot(self): return self.store.snapshot(self.sid)
    def summary(self, *args): return self.store.summary(*args)
    def page(self, request): return self.store.page(request)


def located(endpoints=None, **limits):
    endpoints = endpoints or {"bad": H.Endpoint("127.0.0.1", 20001), "good": H.Endpoint("127.0.0.1", 20002)}
    policy = OwnerEgressPolicy({"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test",
        "public_ports": [], "test_endpoints": [{"host": host, "port": port}
            for host, port in sorted({(e.host, e.port) for e in endpoints.values()})]})
    clock = Clock(); session = SearchSession(NS, FEATURES, {**SESSION_LIMITS, **limits}, clock=clock)
    return _LocatedSearchClient(session, endpoints, policy, {p: 50 for p in endpoints}, clock)


class InertWriter:
    def __init__(self, reader, provider, mode):
        self.reader, self.provider, self.mode = reader, provider, mode
        self.sent, self.responded, self.closed, self.waits = bytearray(), False, False, 0
    def write(self, raw): self.sent.extend(raw)
    def is_closing(self): return self.closed
    def close(self): self.closed = True
    async def wait_closed(self):
        self.waits += 1
        if self.mode == "dirty-close": raise OSError(errno.EIO, "SYNTHETIC_CLOSE_FAILURE")
    async def drain(self):
        if self.mode == "cancel-read": raise asyncio.CancelledError("SYNTHETIC_CANCEL_AFTER_CONNECT")
        if self.mode == "reset": raise ConnectionResetError(errno.ECONNRESET, "SYNTHETIC_PEER_RESET")
        if self.mode == "broken-pipe": raise BrokenPipeError(errno.EPIPE, "SYNTHETIC_PEER_PIPE")
        if self.responded or b"\r\n\r\n" not in self.sent: return
        head, body = bytes(self.sent).split(b"\r\n\r\n", 1)
        expected = int(next(line.split(b":", 1)[1] for line in head.split(b"\r\n")
                            if line.lower().startswith(b"content-length:")))
        if len(body) < expected: return
        self.responded = True
        if self.mode == "timeout": return
        if self.mode == "eof": wire = b"HTTP/1.1 200 OK\r\n"
        elif self.mode == "protocol": wire = b"HTTP/1.1 200 OK\r\nInvalid-Header\r\n\r\n"
        else:
            status = int(self.mode[5:]) if self.mode.startswith("http-") else 200
            if self.mode == "invalid-metadata": raw = b"not-json"
            elif status != 200: raw = b"{}"
            else:
                route = head.split(b"\r\n", 1)[0].decode("ascii").split(" ")[1]
                value = self.provider.dispatch(route, F.strict(body, H.REQUEST_MAX))
                raw = value if type(value) is bytes else F.compact(value)
            wire = H._header("HTTP/1.1 "+str(status)+" Synthetic", len(raw))+raw
        self.reader.feed_data(wire); self.reader.feed_eof()


class InertDial:
    def __init__(self, provider, bad_port=20001, mode="refused", on_connect=None):
        self.provider, self.bad_port, self.mode = provider, bad_port, mode
        self.on_connect = on_connect
        self.calls, self.writers = [], []
    async def __call__(self, host, port, **kwargs):
        self.calls.append((host, port))
        mode = self.mode if port == self.bad_port else "honest"
        if mode == "refused": raise ConnectionRefusedError(errno.ECONNREFUSED, "SYNTHETIC_PEER_REFUSED")
        if mode == "connect-reset": raise ConnectionResetError(errno.ECONNRESET, "SYNTHETIC_CONNECT_RESET")
        if mode == "connect-timeout": await asyncio.Event().wait()
        if mode == "local": raise OSError(errno.EMFILE, "SYNTHETIC_LOCAL_RESOURCE_ERROR")
        if mode == "memory": raise MemoryError("SYNTHETIC_LOCAL_ALLOCATION")
        if mode == "cancel": raise asyncio.CancelledError("SYNTHETIC_CALLER_CANCEL")
        reader = asyncio.StreamReader(limit=H.HEADER_MAX)
        writer = InertWriter(reader, self.provider, mode); self.writers.append(writer)
        if self.on_connect is not None: self.on_connect()
        return reader, writer


class SearchResilienceControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.fixture = Fixture()
    @classmethod
    def tearDownClass(cls): cls.fixture.db.close()
    def setUp(self):
        self.store = self.fixture.store(); self.addCleanup(self.store.close)
        self.sid = self.fixture.snapshots[0]
        self.provider = H.Provider(index=SelectedIndex(self.store, self.sid))

    def live(self, client, search, grant, deadline, mapping):
        self.assertIs(client._search, search); self.assertIs(client.grant, grant)
        self.assertEqual(search.session.deadline, deadline)
        self.assertEqual(search.session.limits, {**SESSION_LIMITS, **getattr(client, "test_limits", {})})
        self.assertEqual(client._warrants, mapping); self.assertIs(client._context, client.context)
        self.assertEqual(client._state, "OPEN"); self.assertFalse(client._budget.closed)
        self.assertTrue(all(o is None or o.closes == 0 for o in client._origin_owners))
        self.assertFalse(client._busy)

    def refusal(self, result, search, reason, *, operation="offer", amount=OFFER_BYTES):
        self.assertEqual(result["schema"], "DMKN_SEARCH_SETTLED_REFUSAL_V1")
        self.assertEqual((result["status"], result["reason"], result["operation"]),
                         ("REFUSED_PROVIDER_ATTEMPT", reason, operation))
        self.assertEqual(result["settlement"], "ABANDONED_CONSERVATIVELY_CHARGED")
        self.assertFalse(result["mathematical_acceptance"] or result["global_complete"])
        self.assertNotIn("matches", result); self.assertNotIn("coverage", result)
        self.assertEqual(search.session.pending, {})
        self.assertEqual(search.session.reserved, {"bytes": 0, "examined": 0, "candidates": 0})
        self.assertGreaterEqual(search.session.used["bytes"], amount)

    def failed(self, client):
        self.assertEqual(client._state, "FAILED"); self.assertEqual(client._warrants, {})
        self.assertIsNone(client._context); self.assertTrue(client._budget.closed)
        self.assertTrue(all(o is None or o.closes == 1 for o in client._origin_owners))
        self.assertFalse(client._busy)

    def test_dead_or_expired_contact_then_honest_same_session_and_live_mapping(self):
        for mode, reason in (("refused", "CONNECTION_REFUSED"), ("expired", "CONTACT_EXPIRED")):
            with self.subTest(mode=mode):
                search = located(); client = InertFacade(search)
                grant, deadline, mapping = client.grant, search.session.deadline, dict(client._warrants)
                dial = InertDial(self.provider)
                if mode == "expired": search._expiries["bad"] = 0
                async def exercise():
                    failed = await client.search_offer("bad", OFFER_BYTES)
                    self.refusal(failed, search, reason)
                    self.assertEqual(search.session.used["bytes"], OFFER_BYTES)
                    self.assertEqual(search.session.used["requests"], 1)
                    self.assertEqual(search.session.snapshot_slots, 1)
                    self.assertEqual(search.session.summaries, {})
                    self.live(client, search, grant, deadline, mapping)
                    return await client.search_offer("good", OFFER_BYTES)
                with patch.object(asyncio, "open_connection", dial): result = asyncio.run(exercise())
                self.assertEqual(result["status"], "OFFERED")
                self.assertEqual(search.session.used["requests"], 2)
                self.assertEqual(len(dial.calls), 1 if mode == "expired" else 2)
                self.live(client, search, grant, deadline, mapping)

    def test_receive_failures_settle_only_after_clean_close(self):
        cases = (("reset", "CONNECTION_RESET"), ("broken-pipe", "BROKEN_PIPE"),
            ("eof", "PEER_EOF"), ("protocol", "HTTP_PROTOCOL"),
            ("http-400", "HTTP_400"), ("http-404", "HTTP_404"), ("http-503", "HTTP_503"),
            ("timeout", "ATTEMPT_TIMEOUT"))
        for mode, reason in cases:
            with self.subTest(mode=mode):
                search = located(); client = InertFacade(search); dial = InertDial(self.provider, mode=mode)
                with patch.object(asyncio, "open_connection", dial):
                    result = asyncio.run(client.search_offer("bad", OFFER_BYTES, attempt_timeout_ms=10))
                self.refusal(result, search, reason)
                self.assertEqual(search.session.used["requests"], 1)
                self.assertEqual(search.session.used["bytes"], OFFER_BYTES)
                self.assertEqual(len(dial.calls), 1)
                self.assertTrue(all(w.closed and w.waits == 1 for w in dial.writers))
                self.assertEqual(client._state, "OPEN")

    def test_failed_candidate_and_interval_pages_charge_full_reservations_once(self):
        for candidates in (True, False):
            with self.subTest(candidates_only=candidates):
                search = located(); client = InertFacade(search); dial = InertDial(self.provider)
                limits = CANDIDATE_LIMITS if candidates else PAGE_LIMITS
                async def exercise():
                    offered = await client.search_offer("good", OFFER_BYTES)
                    before = search.session.report()
                    failed = await client.search_page("bad", offered["snapshot_id"], P, 0, limits,
                                                      candidates_only=candidates)
                    self.refusal(failed, search, "CONNECTION_REFUSED",
                                 operation="candidates" if candidates else "page", amount=limits["bytes"])
                    for key, amount in (("bytes", 65536), ("examined", 32), ("candidates", 8), ("pages", 1), ("requests", 1)):
                        self.assertEqual(search.session.used[key]-before["used"][key], amount)
                    self.assertEqual(search.session.report()["coverage"], before["coverage"])
                    self.assertEqual(search.session.seen_candidates, {})
                    return await client.search_page("good", offered["snapshot_id"], P, 0, limits,
                                                    candidates_only=candidates)
                with patch.object(asyncio, "open_connection", dial): result = asyncio.run(exercise())
                self.assertEqual(len(result["new_matches"]), 1)
                self.assertEqual(search.session.used["requests"], 3)
                self.assertEqual(search.session.used["examined"], 64 if candidates else 42)
                self.assertEqual(search.session.used["candidates"], 9)
                self.assertEqual(client._state, "OPEN")

    def test_exhausted_original_allowance_refuses_without_redial_or_renewal(self):
        search = located(requests=1); client = InertFacade(search); dial = InertDial(self.provider)
        deadline, grant = search.session.deadline, client.grant
        async def exercise():
            self.refusal(await client.search_offer("bad", OFFER_BYTES), search, "CONNECTION_REFUSED")
            with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:requests"):
                await client.search_offer("good", OFFER_BYTES)
        with patch.object(asyncio, "open_connection", dial): asyncio.run(exercise())
        self.assertEqual(len(dial.calls), 1); self.assertEqual(search.session.used["requests"], 1)
        self.assertEqual(search.session.deadline, deadline); self.assertIs(client.grant, grant)
        self.assertEqual(search.session.limits["requests"], 1); self.failed(client)

    def test_cleanup_cancellation_local_fault_and_bad_metadata_are_fatal(self):
        for mode, kind in (("dirty-close", R.SearchCleanupError), ("cancel", asyncio.CancelledError),
                           ("cancel-read", asyncio.CancelledError),
                           ("connect-reset", ConnectionResetError), ("connect-timeout", TimeoutError),
                           ("local", OSError), ("memory", MemoryError), ("invalid-metadata", ValueError)):
            with self.subTest(mode=mode):
                search = located(); client = InertFacade(search); dial = InertDial(self.provider, mode=mode)
                with patch.object(asyncio, "open_connection", dial):
                    with self.assertRaises(kind):
                        asyncio.run(client.search_offer("bad", OFFER_BYTES, attempt_timeout_ms=10))
                self.failed(client)
                self.assertEqual(search.session.summaries, {}); self.assertEqual(search.session.coverage, {})
                self.assertEqual(search.session.seen_candidates, {}); self.assertEqual(len(dial.calls), 1)
                self.assertTrue(all(w.closed for w in dial.writers))
                self.assertEqual(search.session.pending, {})
                self.assertEqual(search.session.used["bytes"], 8 if mode == "invalid-metadata" else OFFER_BYTES)

    def test_changed_endpoint_policy_and_deadline_are_fatal_before_dial(self):
        for mode in ("endpoint", "policy", "deadline", "invalid-timeout"):
            with self.subTest(mode=mode):
                search = located(); client = InertFacade(search); dial = InertDial(self.provider)
                if mode == "endpoint": search.endpoints["bad"] = search.endpoints["good"]
                elif mode == "policy": search._policy._tests = frozenset({("127.0.0.1", 20002)})
                elif mode == "deadline": search.session.clock.value = 61
                with patch.object(asyncio, "open_connection", dial):
                    with self.assertRaises(ValueError):
                        asyncio.run(client.search_offer("bad", OFFER_BYTES,
                            attempt_timeout_ms=0 if mode == "invalid-timeout" else 1000))
                self.failed(client); self.assertEqual(dial.calls, [])

    def test_inflight_deadline_budget_and_ticket_corruption_cannot_continue(self):
        for mode in ("deadline", "budget", "ticket"):
            with self.subTest(mode=mode):
                search = located(); client = InertFacade(search)
                def change():
                    if mode == "deadline": search.session.clock.value = 61
                    elif mode == "budget": search.session.limits["requests"] += 1
                    else: search.session.pending[search.session.sequence]["max_reply_bytes"] += 1
                dial = InertDial(self.provider, mode="http-503", on_connect=change)
                with patch.object(asyncio, "open_connection", dial):
                    with self.assertRaises(ValueError): asyncio.run(client.search_offer("bad", OFFER_BYTES))
                self.failed(client); self.assertEqual(len(dial.calls), 1)
                self.assertEqual(search.session.summaries, {})
                self.assertTrue(all(w.closed and w.waits == 1 for w in dial.writers))

    def test_actual_loopback_503_then_honest_offer_and_candidate(self):
        async def exercise():
            tasks, errors, counts = set(), [], {"unavailable": 0, "honest": 0}
            async def handle(reader, writer, unavailable):
                task = asyncio.current_task(); tasks.add(task)
                try:
                    async with asyncio.timeout(3):
                        first, unused, count, unused_bytes = await H._headers(reader)
                        raw = await H._body(reader, count)
                        route = first.split(" ")[1]
                        role = "unavailable" if unavailable else "honest"; counts[role] += 1
                        if unavailable: status, body = 503, b"{}"
                        else:
                            value = self.provider.dispatch(route, F.strict(raw, H.REQUEST_MAX))
                            status, body = 200, value if type(value) is bytes else F.compact(value)
                        writer.write(H._header("HTTP/1.1 "+str(status)+" Test", len(body))+body)
                        await writer.drain()
                except BaseException as error: errors.append(type(error).__name__+":"+str(error))
                finally:
                    writer.close()
                    try:
                        async with asyncio.timeout(1): await writer.wait_closed()
                    except BaseException as error: errors.append("close:"+type(error).__name__)
                    tasks.discard(task)
            bad = await asyncio.start_server(lambda r,w: handle(r,w,True), "127.0.0.1", 0, limit=H.HEADER_MAX)
            good = None
            try:
                good = await asyncio.start_server(lambda r,w: handle(r,w,False), "127.0.0.1", 0, limit=H.HEADER_MAX)
                endpoints = {"bad": H.Endpoint("127.0.0.1", bad.sockets[0].getsockname()[1]),
                             "good": H.Endpoint("127.0.0.1", good.sockets[0].getsockname()[1])}
                search = located(endpoints); client = InertFacade(search)
                grant, deadline, mapping = client.grant, search.session.deadline, dict(client._warrants)
                refused = await client.search_offer("bad", OFFER_BYTES, attempt_timeout_ms=2000)
                self.refusal(refused, search, "HTTP_503")
                offered = await client.search_offer("good", OFFER_BYTES, attempt_timeout_ms=2000)
                found = await client.search_page("good", offered["snapshot_id"], P, 0, CANDIDATE_LIMITS,
                                                 attempt_timeout_ms=2000)
                self.assertEqual(found["new_matches"], [self.fixture.hit])
                self.live(client, search, grant, deadline, mapping)
                self.assertEqual(search.session.used["requests"], 3)
                self.assertEqual(search.session.snapshot_slots, 2)
                self.assertEqual(search.session.used["bytes"], OFFER_BYTES+search.http["actual_reply_bytes"]-2)
            finally:
                bad.close()
                if good is not None: good.close()
                await bad.wait_closed()
                if good is not None: await good.wait_closed()
                if tasks:
                    async with asyncio.timeout(3): await asyncio.gather(*tuple(tasks))
            self.assertEqual(errors, []); self.assertEqual(tasks, set())
            self.assertEqual(counts, {"unavailable": 1, "honest": 2})
            SOCKET_EVIDENCE.append({"transport": "ACTUAL_IPV4_LOOPBACK_NO_TLS", "accepted_connections": 3,
                "provider_responses": counts, "handler_errors": errors, "all_servers_closed": True,
                "authority": "SYNTHETIC_INDEX_AND_OWNERS_NOT_MATHEMATICAL_ACCEPTANCE"})
        asyncio.run(exercise())


def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True)
    output = Path(parser.parse_args().output)
    F.need(Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
           and not sys.flags.optimize, "CANONICAL_ISOLATED_CONTROLS")
    F.need(output.is_absolute() and output.resolve() == output and output.is_relative_to(PROJECT/"experiments")
           and not output.exists() and output.parent.is_dir(), "FRESH_CONTROL_OUTPUT")
    output.mkdir()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SearchResilienceControls)
    F.need(suite.countTestCases() == 8, "EXACT_EIGHT_SEARCH_CONTROLS")
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_PROCESS_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    imports = []
    for name, module in sorted(sys.modules.items()):
        location = getattr(module, "__file__", None)
        if location and Path(location).is_relative_to(SOURCE): imports.append({"name": name, **pin(Path(location))})
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skips": len(result.skipped),
        "scope": "REAL_SEARCH_PROTOCOL_AND_FAILSTOP_WITH_INERT_FACADE_OWNERS",
        "authority": "SYNTHETIC_HANDLES_GRANT_INDEX_NOT_MATHEMATICS_OR_FULL_OWNER_CONSTRUCTION",
        "native_process_calls": 0, "proof_calls": 0, "external_network_calls": 0,
        "actual_socket_evidence": SOCKET_EVIDENCE, "imports": imports}
    with (output/"RESULT.json").open("xb") as stream: stream.write(F.compact(report))
    print(F.compact(report).decode(), flush=True)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

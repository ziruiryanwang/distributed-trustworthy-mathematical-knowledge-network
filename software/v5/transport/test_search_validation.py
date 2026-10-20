"""Only the new metadata-rejection boundary; synthetic metadata/inert owners.

Uses actual validated facade methods, decorators, stateful session and bounded
transport. No predecessor suite, native check, issuer, proof or compiler runs.
One small loopback case supplies malformed 200 then honest metadata.
"""
import argparse
import asyncio
from copy import deepcopy
import hashlib
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE))
from client import workspace_validated as W
from discovery import formal_features as F
from discovery.search_session import SearchSession
from transport import http_provider as H, search_resilience as R, search_validation as V
from transport import test_search_resilience as T

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOCKET_EVIDENCE = []


class InertFacade(W.CommonsClient):
    """Borrow fixture initialization, never its predecessor search methods."""
    _active = T.InertFacade._active
    _census = T.InertFacade._census
    report = T.InertFacade.report

    def __init__(self, search):
        T.InertFacade.__init__(self, search)
        self.stage_token = object()
        self._staged = {self.stage_token: (b"synthetic-data-not-authority", False)}
        self._staging_counts = dict(packets_staged=1, admission_transitions=0, previews=0)


class Mutator:
    def __init__(self, provider):
        self.provider, self.change = provider, None

    def dispatch(self, route, request):
        value = self.provider.dispatch(route, request)
        if self.change is None: return value
        change, self.change = self.change, None
        value = F.strict(value, 1048576) if type(value) is bytes else deepcopy(value)
        result = change(value)
        return result if result is not None else value


def metadata(session):
    # Test-only snapshot, never used by the production preflight.
    return deepcopy(dict(summaries=session.summaries,
        coverage={key: (value.report(), value.observed) for key, value in session.coverage.items()},
        hints=session.offer_hints, seen=session.seen_candidates, first=session.candidate_first,
        advisory=session.last_advisory, last=session.last_verified,
        duplicate=session.duplicate_candidates, conflicts=session.metadata_conflicts,
        attempted=session.attempted_snapshots))


class ValidationControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.fixture = T.Fixture()
    @classmethod
    def tearDownClass(cls): cls.fixture.db.close()

    def setUp(self):
        self.store = self.fixture.store(); self.addCleanup(self.store.close)
        self.sid = self.fixture.snapshots[0]
        self.provider = H.Provider(index=T.SelectedIndex(self.store, self.sid))
        self.mutator = Mutator(self.provider)
        self.dial = T.InertDial(self.mutator, mode="honest")

    def live(self, client, search, grant, deadline, tokens, staged):
        self.assertIs(client._search, search); self.assertIs(client.grant, grant)
        self.assertEqual(search.session.deadline, deadline)
        self.assertEqual(client._warrants, tokens); self.assertEqual(client._staged, staged)
        self.assertIs(client._context, client.context)
        self.assertEqual(client._state, "OPEN"); self.assertFalse(client._budget.closed)
        self.assertTrue(all(owner is None or owner.closes == 0 for owner in client._origin_owners))
        self.assertFalse(client._busy)

    def refusal(self, result, search, before, operation, byte_cap, examined=0, candidates=0):
        self.assertEqual(result["schema"], V.SCHEMA)
        self.assertEqual((result["status"], result["operation"], result["reason"]),
                         ("REFUSED_PROVIDER_ATTEMPT", operation, "INVALID_METADATA"))
        self.assertEqual(result["settlement"], "ABANDONED_CONSERVATIVELY_CHARGED")
        self.assertFalse(result["mathematical_acceptance"] or result["global_complete"])
        self.assertFalse(set(result) & {"matches", "new_matches", "coverage", "summary"})
        self.assertEqual(search.session.pending, {})
        self.assertEqual(search.session.reserved, dict(examined=0, candidates=0, bytes=0))
        for key, amount in (("bytes", byte_cap), ("examined", examined), ("candidates", candidates),
                            ("requests", 1), ("pages", int(operation != "offer"))):
            self.assertEqual(search.session.used[key]-before[key], amount, key)

    def failed(self, client):
        self.assertEqual(client._state, "FAILED")
        self.assertEqual(client._warrants, {}); self.assertEqual(client._staged, {})
        self.assertIsNone(client._context); self.assertTrue(client._budget.closed)
        self.assertTrue(all(owner is None or owner.closes == 1 for owner in client._origin_owners))
        self.assertFalse(client._busy)

    def test_malformed_and_bad_summary_then_honest_preserve_same_owner(self):
        def bad_summary(value):
            value["summary"]["snapshot"]["local_cut"] += 1
        for change in (lambda _: b"not-json", lambda _: b"\xff", bad_summary):
            with self.subTest(change=change):
                search = T.located(); client = InertFacade(search)
                grant, deadline = client.grant, search.session.deadline
                tokens, staged = dict(client._warrants), dict(client._staged)
                before, original = dict(search.session.used), metadata(search.session)
                self.mutator.change = change
                async def exercise():
                    refused = await client.search_offer("bad", T.OFFER_BYTES)
                    self.refusal(refused, search, before, "offer", T.OFFER_BYTES)
                    self.assertEqual(metadata(search.session), original)
                    self.live(client, search, grant, deadline, tokens, staged)
                    return await client.search_offer("good", T.OFFER_BYTES)
                with patch.object(asyncio, "open_connection", self.dial):
                    offered = asyncio.run(exercise())
                self.assertEqual(offered["status"], "OFFERED")
                self.assertEqual(search.session.used["requests"], 2)
                self.assertEqual(search.session.snapshot_slots, 2)
                self.live(client, search, grant, deadline, tokens, staged)

    def test_bad_positive_and_interval_proofs_then_honest_no_partial_metadata(self):
        for candidates in (True, False):
            with self.subTest(candidates=candidates):
                search = T.located(); client = InertFacade(search)
                limits = T.CANDIDATE_LIMITS if candidates else T.PAGE_LIMITS
                def damage(value):
                    rows = value["hits"] if candidates else value["examined"]
                    rows[-1]["siblings"][0] = "0"*64
                async def exercise():
                    await client.search_offer("good", T.OFFER_BYTES)
                    original, before = metadata(search.session), dict(search.session.used)
                    scan = search.session.candidate_scan_charges
                    self.mutator.change = damage
                    refused = await client.search_page("bad", self.sid, T.P, 0, limits,
                                                       candidates_only=candidates)
                    self.refusal(refused, search, before,
                        "candidates" if candidates else "page", limits["bytes"], 32, 8)
                    self.assertEqual(metadata(search.session), original)
                    self.assertEqual(search.session.candidate_scan_charges-scan, 32 if candidates else 0)
                    self.assertEqual(client._state, "OPEN"); self.assertIn(client.stage_token, client._staged)
                    return await client.search_page("good", self.sid, T.P, 0, limits,
                                                    candidates_only=candidates)
                with patch.object(asyncio, "open_connection", self.dial): found = asyncio.run(exercise())
                self.assertEqual(found["new_matches"], [self.fixture.hit])
                self.assertEqual(search.session.used["candidates"], 9)
                self.assertEqual(search.session.used["requests"], 3)

    def test_cross_page_conflict_is_read_only_rejection(self):
        search = T.located(); client = InertFacade(search)
        async def exercise():
            await client.search_offer("good", T.OFFER_BYTES)
            # Synthetic prior authenticated observation: exercise exactly the
            # state-dependent check absent from the pure page verifier.
            hit = self.fixture.hit
            search.session.coverage[self.sid].observed[hit["object_id"]] = (
                (T.P, 999), F.record_id(hit))
            original, before = metadata(search.session), dict(search.session.used)
            refused = await client.search_page("bad", self.sid, T.P, 0, T.PAGE_LIMITS,
                                               candidates_only=False)
            self.refusal(refused, search, before, "page", T.PAGE_LIMITS["bytes"], 32, 8)
            self.assertIn("CROSS_PAGE_OBJECT_CONSISTENCY", refused["validation_error"])
            self.assertEqual(metadata(search.session), original)
            self.assertEqual(client._state, "OPEN")
        with patch.object(asyncio, "open_connection", self.dial): asyncio.run(exercise())

    def test_original_request_budget_exhausts_without_second_dial(self):
        search = T.located(requests=1); client = InertFacade(search)
        self.mutator.change = lambda _: b"not-json"
        async def exercise():
            refused = await client.search_offer("bad", T.OFFER_BYTES)
            self.assertEqual(refused["reason"], "INVALID_METADATA")
            with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:requests"):
                await client.search_offer("good", T.OFFER_BYTES)
        with patch.object(asyncio, "open_connection", self.dial): asyncio.run(exercise())
        self.assertEqual(len(self.dial.calls), 1)
        self.assertEqual(search.session.used["bytes"], T.OFFER_BYTES)
        self.assertEqual(search.session.used["requests"], 1)
        self.failed(client)

    def test_decode_callback_expiry_escapes_metadata_classification(self):
        class ExpiringClock(T.Clock):
            def __init__(self):
                super().__init__(); self.armed, self.calls = False, 0
            def __call__(self):
                if self.armed:
                    self.calls += 1
                    if self.calls >= 3: self.value = 61
                return self.value
        clock = ExpiringClock()
        session = SearchSession(T.NS, T.FEATURES, T.SESSION_LIMITS, clock=clock)
        ticket = session.begin_offer("synthetic", T.OFFER_BYTES)
        raw = self.provider.dispatch(H.OFFER_ROUTE, ticket["request"])
        raw = raw if type(raw) is bytes else F.compact(raw)
        original = metadata(session); clock.armed = True
        with self.assertRaisesRegex(ValueError, "SESSION_DEADLINE_EXHAUSTED"):
            V._preflight(session, ticket, raw)
        self.assertGreaterEqual(clock.calls, 3)  # Second guard, inside decode.
        self.assertEqual(metadata(session), original)
        self.assertIn(ticket["ticket"], session.pending)
        self.assertEqual(session.state, "DEADLINE_EXHAUSTED")

    def test_local_binding_and_late_commit_errors_still_fail_stop(self):
        for mode in ("coverage", "late"):
            with self.subTest(mode=mode):
                search = T.located(); client = InertFacade(search)
                async def exercise():
                    await client.search_offer("good", T.OFFER_BYTES)
                    if mode == "coverage":
                        search.session.coverage[self.sid].summary["namespace"] = "0"*64
                        with self.assertRaisesRegex(ValueError, "SEARCH_COVERAGE_SUMMARY_BINDING"):
                            await client.search_page("good", self.sid, T.P, 0, T.PAGE_LIMITS,
                                                     candidates_only=False)
                    else:
                        original_accept = search.session.accept
                        def late(ticket, raw):
                            original_accept(ticket, raw)
                            raise RuntimeError("SYNTHETIC_LATE_COMMIT_FAILURE")
                        with patch.object(search.session, "accept", late):
                            with self.assertRaisesRegex(RuntimeError, "SYNTHETIC_LATE_COMMIT_FAILURE"):
                                await client.search_page("good", self.sid, T.P, 0, T.CANDIDATE_LIMITS)
                        self.assertEqual(len(search.session.seen_candidates), 1)
                    self.assertEqual(search.session.pending, {})
                with patch.object(asyncio, "open_connection", self.dial): asyncio.run(exercise())
                self.failed(client)

    def test_cleanup_cancel_and_local_allocation_are_not_metadata_refusals(self):
        for mode, expected in (("dirty-close", R.SearchCleanupError),
                               ("cancel", asyncio.CancelledError), ("memory", MemoryError)):
            with self.subTest(mode=mode):
                search = T.located(); client = InertFacade(search)
                dial = T.InertDial(self.provider, mode=mode)
                with patch.object(asyncio, "open_connection", dial):
                    with self.assertRaises(expected): asyncio.run(client.search_offer("bad", T.OFFER_BYTES))
                self.failed(client); self.assertEqual(search.session.pending, {})
                self.assertEqual(search.session.used["bytes"], T.OFFER_BYTES)

    def test_actual_loopback_invalid_200_then_honest_same_live_operation(self):
        async def exercise():
            tasks, errors, counts = set(), [], dict(bad=0, good=0)
            async def handle(reader, writer, invalid):
                task = asyncio.current_task(); tasks.add(task)
                try:
                    async with asyncio.timeout(3):
                        first, unused, count, unused_bytes = await H._headers(reader)
                        raw = await H._body(reader, count)
                        role = "bad" if invalid else "good"; counts[role] += 1
                        if invalid: body = b"not-json"
                        else:
                            value = self.provider.dispatch(first.split(" ")[1], F.strict(raw, H.REQUEST_MAX))
                            body = value if type(value) is bytes else F.compact(value)
                        writer.write(H._header("HTTP/1.1 200 Test", len(body))+body)
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
                search = T.located({"bad": H.Endpoint("127.0.0.1", bad.sockets[0].getsockname()[1]),
                                    "good": H.Endpoint("127.0.0.1", good.sockets[0].getsockname()[1])})
                client = InertFacade(search)
                grant, deadline = client.grant, search.session.deadline
                tokens, staged = dict(client._warrants), dict(client._staged)
                before = dict(search.session.used)
                refused = await client.search_offer("bad", T.OFFER_BYTES, attempt_timeout_ms=2000)
                self.refusal(refused, search, before, "offer", T.OFFER_BYTES)
                offered = await client.search_offer("good", T.OFFER_BYTES, attempt_timeout_ms=2000)
                self.assertEqual(offered["status"], "OFFERED")
                self.live(client, search, grant, deadline, tokens, staged)
                self.assertEqual(search.session.used["requests"], 2)
                self.assertEqual(search.session.used["bytes"],
                                 T.OFFER_BYTES+search.http["actual_reply_bytes"]-8)
            finally:
                bad.close()
                if good is not None: good.close()
                await bad.wait_closed()
                if good is not None: await good.wait_closed()
                if tasks:
                    async with asyncio.timeout(3): await asyncio.gather(*tuple(tasks))
            self.assertEqual(errors, []); self.assertEqual(tasks, set())
            self.assertEqual(counts, dict(bad=1, good=1))
            SOCKET_EVIDENCE.append(dict(transport="ACTUAL_IPV4_LOOPBACK_NO_TLS",
                accepted_connections=2, responses=counts, errors=errors, all_servers_closed=True,
                authority="SYNTHETIC_METADATA_AND_INERT_OWNERS_NOT_MATHEMATICS"))
        asyncio.run(exercise())


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True)
    output = Path(parser.parse_args().output)
    F.need(Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
           and sys.dont_write_bytecode and not sys.flags.optimize, "CANONICAL_ISOLATED_CONTROLS")
    F.need(output.is_absolute() and output.resolve() == output
           and output.is_relative_to(PROJECT/"experiments") and not output.exists()
           and output.parent.is_dir(), "FRESH_CONTROL_OUTPUT")
    output.mkdir()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ValidationControls)
    F.need(suite.countTestCases() == 8, "EXACT_EIGHT_VALIDATION_CONTROLS")
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_PROCESS_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    imports = []
    for name, module in sorted(sys.modules.items()):
        location = getattr(module, "__file__", None)
        if location and Path(location).is_relative_to(SOURCE): imports.append(dict(name=name, **pin(Path(location))))
    report = dict(status="PASS" if result.wasSuccessful() else "FAIL", tests=result.testsRun,
        failures=len(result.failures), errors=len(result.errors), skips=len(result.skipped),
        scope="VALIDATED_FACADE_SEARCH_METHODS_WITH_INERT_CONSTRUCTION_AND_OWNERS",
        authority="SYNTHETIC_METADATA_NOT_MATHEMATICS_OR_FULL_OWNER_CONSTRUCTION",
        native_process_calls=0, proof_calls=0, external_network_calls=0,
        actual_socket_evidence=SOCKET_EVIDENCE, imports=imports)
    with (output/"RESULT.json").open("xb") as stream: stream.write(F.compact(report))
    print(F.compact(report).decode(), flush=True)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())

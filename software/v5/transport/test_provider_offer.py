"""Focused offer-entry/accounting controls, not remote or mathematical evidence.

Reuse existing authenticated in-memory fixture; do not rerun its old controls.
The root owns actual retained-index/public-reuse integration and all launches.
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
from discovery.search_session import SearchSession
from discovery.test_search_session import Fixture, Clock, NS, FEATURE, PAGE_LIMITS
from transport import clients as C
from transport import http_provider as H
from transport.test_compact_summary import memory_request

LIMITS = dict(providers=2, snapshots=2, requests=8, pages=8, examined=64,
              candidates=64, bytes=1048576, wall_ms=60000, inflight=2)
WIRE, EXPANDED = 8192, 65536


class Index:
    def __init__(self, fixture):
        self.fixture, self.namespace, self.calls = fixture, NS, []
    def snapshot(self):
        self.calls.append("snapshot")
        return deepcopy(self.fixture.snapshot)
    def summary(self, sid, features, maximum):
        self.calls.append((sid, list(features), maximum))
        F.need(sid == self.fixture.sid and features == [FEATURE], "FIXTURE_QUERY_BINDING")
        F.need(len(F.compact(self.fixture.summary)) <= maximum, "SUMMARY_BYTES_EXHAUSTED")
        return deepcopy(self.fixture.summary)
    def page(self, request): return self.fixture.page(request)


class ProviderOfferContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.fixture = Fixture()

    def session(self, **overrides):
        return SearchSession(NS, [FEATURE], {**LIMITS, **overrides}, clock=Clock())

    def request(self, **overrides):
        return {"namespace": NS, "features": [FEATURE], "max_bytes": WIRE,
                "max_expanded_bytes": EXPANDED, **overrides}

    def provider(self): return H.Provider(index=Index(self.fixture))

    def raw(self): return self.provider().dispatch(H.OFFER_ROUTE, self.request())

    def adopt(self, session, provider="p", **kwargs):
        ticket = session.begin_offer(provider, WIRE, max_expanded_bytes=EXPANDED, **kwargs)
        return session.accept(ticket["ticket"], self.raw())

    def test_unknown_sid_offer_page_and_pinned_summary_share_one_workflow(self):
        provider, session, calls = self.provider(), self.session(), []
        async def exchange(endpoint, route, request, maximum, timeout):
            calls.append((route, deepcopy(request)))
            value = provider.dispatch(route, request)
            raw = value if type(value) is bytes else F.compact(value)
            self.assertLessEqual(len(raw), maximum)
            return {"status": 200, "raw": raw, "request_bytes": len(F.compact(request)),
                    "reply_bytes": len(raw), "header_bytes": 0}
        client = C.SearchClient(session, {"p": H.Endpoint("127.0.0.1", 1)})
        with patch.object(C, "exchange", new=exchange):
            offered = asyncio.run(client.offer("p", WIRE, max_expanded_bytes=EXPANDED))
            sid = offered["snapshot_id"]
            page = asyncio.run(client.page("p", sid, 7, 0, PAGE_LIMITS))
            explicit = asyncio.run(client.summary("p", sid, EXPANDED))
        self.assertEqual(calls[0], (H.OFFER_ROUTE, self.request()))
        self.assertNotIn("snapshot_id", calls[0][1])
        self.assertEqual(offered["status"], "OFFERED"); self.assertEqual(sid, self.fixture.sid)
        self.assertFalse(offered["global_complete"]); self.assertFalse(offered["mathematical_acceptance"])
        self.assertEqual(page["status"], "VERIFIED_PAGE"); self.assertEqual(explicit["status"], "VERIFIED_SUMMARY")
        report = client.report()
        self.assertEqual(report["session"]["used"]["requests"], 3)
        self.assertEqual(report["session"]["used"]["bytes"], report["http"]["actual_reply_bytes"])
        self.assertEqual(report["session"]["snapshot_budget"],
                         {"charged_attempt_slots": 1, "known_snapshot_ids": 1, "limit": 2})
        self.assertEqual(report["session"]["coverage"][sid]["partitions"][7]["intervals"], [[0, 1]])

    def test_typed_no_offer_and_refusal_are_not_absence_or_free_attempts(self):
        cases = [(H.Provider(custody=object()), self.request(), "NO_OFFER", "ROLE_NOT_SERVED"),
                 (self.provider(), self.request(namespace="f"*64), "NO_OFFER", "NAMESPACE_NOT_SERVED"),
                 (self.provider(), self.request(max_expanded_bytes=1024), "REFUSED", "SUMMARY_RESOURCE_BOUND"),
                 (self.provider(), self.request(max_bytes=1024), "REFUSED", "SUMMARY_RESOURCE_BOUND")]
        for provider, request, status, reason in cases:
            session = SearchSession(request["namespace"], request["features"], {**LIMITS, "snapshots": 1})
            ticket = session.begin_offer("p", request["max_bytes"], max_expanded_bytes=request["max_expanded_bytes"])
            raw = provider.dispatch(H.OFFER_ROUTE, request)
            with self.subTest(status=status, reason=reason):
                result = session.accept(ticket["ticket"], raw)
                self.assertEqual((result["status"], result["reason"]), (status, reason))
                self.assertFalse(result["global_complete"]); self.assertEqual(session.coverage, {})
                self.assertEqual(session.used["bytes"], len(raw)); self.assertEqual(session.used["requests"], 1)
                self.assertEqual(session.report()["snapshot_budget"]["known_snapshot_ids"], 0)
                with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:snapshots"): session.begin_offer("p", WIRE)
        # Largest legal no-offer envelope still fits the smallest wire limit.
        features = sorted([F.digest("offer-fixture", i) for i in range(8)])
        raw = H.Provider(custody=object()).dispatch(H.OFFER_ROUTE, self.request(features=features, max_bytes=1024))
        self.assertLessEqual(len(raw), 1024)

    def test_private_ticket_and_query_provider_bindings_reject_bad_envelopes(self):
        session = self.session(); ticket = session.begin_offer("approved-p", WIRE, max_expanded_bytes=EXPANDED)
        ident = ticket["ticket"]
        ticket["provider"] = "other"; ticket["features"].clear(); ticket["request"]["features"].clear()
        ticket["namespace"] = "f"*64; ticket["offer_until"] = -1; ticket["max_expanded_bytes"] = 1
        self.assertEqual(session.accept(ident, self.raw())["provider"], "approved-p")
        good = F.strict(self.raw(), WIRE)
        mutations = []
        for field, value in (("namespace", "f"*64), ("features", []), ("global_complete", True),
                             ("mathematical_acceptance", True), ("reason", "LATEST_GLOBAL"),
                             ("remote_expiry", 999999), ("status", "REFUSED")):
            broken = deepcopy(good); broken[field] = value; mutations.append(broken)
        broken = deepcopy(good); broken["summary"]["snapshot_id"] = "f"*64; mutations.append(broken)
        broken = deepcopy(good); broken["summary"]["rows"][0]["partitions"][0]["count"] += 1; mutations.append(broken)
        for broken in mutations:
            failed = self.session(); pending = failed.begin_offer("p", WIRE, max_expanded_bytes=EXPANDED)
            raw = F.compact(broken)
            with self.assertRaises(ValueError): failed.accept(pending["ticket"], raw)
            self.assertEqual(failed.summaries, {}); self.assertEqual(failed.coverage, {})
            self.assertEqual(failed.used["bytes"], len(raw)); self.assertEqual(failed.snapshot_slots, 1)
            self.assertEqual(failed.pending, {}); self.assertEqual(failed.offer_hints, {})
        changed = self.session(); pending = changed.begin_offer("p", WIRE)
        changed.features = ["f"*64]
        with self.assertRaisesRegex(ValueError, "SESSION_QUERY_CHANGED"): changed.accept(pending["ticket"], self.raw())
        self.assertEqual(changed.coverage, {}); self.assertEqual(changed.used["requests"], 1)

    def test_concurrent_and_duplicate_offers_charge_slots_before_sid_is_known(self):
        session = self.session(snapshots=2)
        first = session.begin_offer("a", WIRE); second = session.begin_offer("b", WIRE)
        self.assertEqual(session.snapshot_slots, 2); self.assertEqual(session.attempted_snapshots, set())
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:inflight"): session.begin_offer("a", WIRE)
        session.accept(first["ticket"], self.raw())
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:snapshots"): session.begin_offer("a", WIRE)
        session.accept(second["ticket"], self.raw())
        report = session.report()
        self.assertEqual(report["snapshot_budget"], {"charged_attempt_slots": 2, "known_snapshot_ids": 1, "limit": 2})
        self.assertEqual(report["used"]["snapshots"], 1)
        page = session.begin_page("b", self.fixture.sid, 7, 0, PAGE_LIMITS)
        session.accept(page["ticket"], F.compact(self.fixture.page(page["request"])))
        self.assertEqual(session.snapshot_slots, 2)
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:snapshots"):
            session.begin_summary("a", "f"*64, WIRE)

    def test_failures_abandonment_and_offer_page_budgets_cannot_reset(self):
        session = self.session(bytes=2*WIRE); calls = []
        async def fail(endpoint, route, request, maximum, timeout):
            calls.append(route); raise ValueError("TRANSPORT_FAILED")
        client = C.SearchClient(session, {"p": H.Endpoint("127.0.0.1", 1)})
        with patch.object(C, "exchange", new=fail):
            with self.assertRaisesRegex(ValueError, "TRANSPORT_FAILED"): asyncio.run(client.offer("p", WIRE))
        pending = session.begin_offer("p", WIRE); session.abandon(pending["ticket"])
        self.assertEqual(calls, [H.OFFER_ROUTE]); self.assertEqual(session.used["bytes"], 2*WIRE)
        self.assertEqual(session.snapshot_slots, 2); self.assertEqual(session.reserved["bytes"], 0)
        with self.assertRaises(ValueError): session.begin_offer("p", WIRE)
        exhausted = self.session(requests=1); self.adopt(exhausted)
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:requests"):
            exhausted.begin_page("p", self.fixture.sid, 7, 0, PAGE_LIMITS)
        limited = self.session(providers=1); pending = limited.begin_offer("p", WIRE)
        limited.abandon(pending["ticket"])
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:providers"): limited.begin_offer("q", WIRE)
        unconfigured = self.session(); client = C.SearchClient(unconfigured, {"p": H.Endpoint("127.0.0.1", 1)})
        with self.assertRaisesRegex(ValueError, "ENDPOINT_NOT_CONFIGURED"): asyncio.run(client.offer("referral", WIRE))
        self.assertEqual(unconfigured.used["requests"], 0)

    def test_owner_clock_limits_offer_adoption_not_immutable_snapshot_validity(self):
        for boundary in ("arrival", "post-verification"):
            session = self.session(); ticket = session.begin_offer("p", WIRE, max_age_ms=100)
            original = Q.verify_summary
            def expire(*args, **kwargs):
                result = original(*args, **kwargs); session.clock.value = .1; return result
            if boundary == "arrival": session.clock.value = .1
            with patch.object(Q, "verify_summary", side_effect=expire), self.subTest(boundary=boundary):
                with self.assertRaisesRegex(ValueError, "SESSION_OFFER_EXPIRED"): session.accept(ticket["ticket"], self.raw())
            self.assertEqual(session.coverage, {}); self.assertEqual(session.snapshot_slots, 1)
            self.assertEqual(session.used["bytes"], len(self.raw()))
        session = self.session(); self.adopt(session, max_age_ms=100)
        session.clock.value = .2
        self.assertFalse(session.report()["offer_hints"][0]["fresh"])
        page = session.begin_page("p", self.fixture.sid, 7, 0, PAGE_LIMITS)
        self.assertEqual(session.accept(page["ticket"], F.compact(self.fixture.page(page["request"])))
                         ["status"], "VERIFIED_PAGE")
        # A session deadline still gates all later operations, including offers.
        late = self.session(wall_ms=100); ticket = late.begin_offer("p", WIRE, max_age_ms=1000)
        late.clock.value = .1
        with self.assertRaisesRegex(ValueError, "SESSION_DEADLINE_EXHAUSTED"): late.accept(ticket["ticket"], self.raw())
        self.assertEqual(late.coverage, {})

    def test_total_envelope_bytes_expansion_caps_and_no_format_downgrade(self):
        provider = self.provider(); raw = provider.dispatch(H.OFFER_ROUTE, self.request())
        cap = len(raw); self.assertGreater(cap, 1024)
        self.assertEqual(provider.dispatch(H.OFFER_ROUTE, self.request(max_bytes=cap)), raw)
        smaller = F.strict(provider.dispatch(H.OFFER_ROUTE, self.request(max_bytes=cap-1)), cap-1)
        self.assertEqual(smaller["status"], "REFUSED")
        session = self.session(); ticket = session.begin_offer("p", cap-1)
        with self.assertRaisesRegex(ValueError, "SESSION_TRANSPORT_BYTE_VIOLATION"): session.accept(ticket["ticket"], raw)
        self.assertEqual(session.used["bytes"], cap); self.assertEqual(session.coverage, {})
        session = self.session(); ticket = session.begin_offer("p", WIRE, max_expanded_bytes=1024)
        with self.assertRaisesRegex(ValueError, "SUMMARY_EXPANSION_BYTES"): session.accept(ticket["ticket"], raw)
        self.assertEqual(session.coverage, {})
        session = self.session(); ticket = session.begin_offer("p", EXPANDED)
        with self.assertRaises(ValueError): session.accept(ticket["ticket"], F.compact(self.fixture.summary))
        self.assertEqual(session.coverage, {})
        for change in ({"max_age_ms": True}, {"max_age_ms": 0}, {"max_expanded_bytes": 1048577}):
            session = self.session()
            with self.assertRaises(ValueError): session.begin_offer("p", WIRE, **change)
            self.assertEqual(session.used["requests"], 0)

    def test_memory_stream_offer_reserves_total_wire_not_expansion(self):
        raw = self.raw(); cap = len(raw)
        provider = H.Provider(index=Index(self.fixture), max_reply_bytes=cap)
        request = self.request(max_bytes=cap)
        first = asyncio.run(memory_request(provider, H.OFFER_ROUTE, request))
        head, body = first.split(b"\r\n\r\n", 1)
        self.assertTrue(head.startswith(b"HTTP/1.1 200 OK")); self.assertEqual(body, raw)
        second = asyncio.run(memory_request(provider, H.OFFER_ROUTE, request))
        self.assertEqual(second, b""); self.assertEqual(provider.status()["reply_bytes"], cap)
        self.assertEqual(provider.status()["failures"], 1); self.assertEqual(provider.status()["active"], 0)
        self.assertEqual(provider.status()["reserved_reply_bytes"], 0)
        self.assertEqual(provider.index.calls, ["snapshot", (self.fixture.sid, [FEATURE], EXPANDED)])

    def test_provider_malformed_requests_and_unexpected_failures_are_not_typed_absence(self):
        provider = self.provider()
        for field, value in (("max_bytes", True), ("max_bytes", 1023), ("max_bytes", 1048577),
                             ("features", []), ("namespace", "bad"), ("snapshot_id", self.fixture.sid),
                             ("max_expanded_bytes", 1023)):
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                provider.dispatch(H.OFFER_ROUTE, self.request(**{field: value}))
        self.assertEqual(provider.index.calls, [])
        with patch.object(provider.index, "snapshot", side_effect=ValueError("CORRUPT_INDEX")):
            with self.assertRaisesRegex(ValueError, "CORRUPT_INDEX"): provider.dispatch(H.OFFER_ROUTE, self.request())
        def refuse(): raise ValueError("PROVIDER_OPERATION_DEADLINE")
        with self.assertRaisesRegex(ValueError, "PROVIDER_OPERATION_DEADLINE"):
            provider.dispatch(H.OFFER_ROUTE, self.request(), check_budget=refuse)


if __name__ == "__main__": unittest.main(verbosity=2)

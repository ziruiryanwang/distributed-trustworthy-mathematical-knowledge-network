"""Focused public candidate accounting controls, not actual network evidence.

Uses the qualified repaired synthetic SQLite fixture and memory HTTP streams.
Does not rerun the isolated candidate algorithm suite. Root owns all launches.
"""
import asyncio
from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import authenticated_index as A
from discovery import candidate_query as K
from discovery import discovery_query as Q
from discovery import formal_features as F
from discovery.search_session import SearchSession
from discovery.test_candidate_query import Fixture, Memory, Clock, NS, FEATURES, P, LIMITS as QUERY_LIMITS
from transport import clients as C
from transport import http_provider as H
from transport.test_compact_summary import memory_request

SESSION_LIMITS = dict(providers=3, snapshots=2, requests=16, pages=8, examined=256,
                      candidates=64, bytes=2097152, wall_ms=60000, inflight=2)
PAGE_LIMITS = dict(examined=32, matches=8, bytes=65536, timeout_ms=1000, node_reads=100000)


class SelectedIndex:
    """Provider-owned retained cut; client receives its ID only through offer."""
    def __init__(self, store, sid): self.store, self.sid, self.namespace, self.db = store, sid, store.namespace, store.db
    def snapshot(self): return self.store.snapshot(self.sid)
    def summary(self, *args): return self.store.summary(*args)
    def page(self, request): return self.store.page(request)


class CandidateSessionContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.fixture = Fixture()
    @classmethod
    def tearDownClass(cls): cls.fixture.db.close()
    def setUp(self):
        self.store = self.fixture.store(); self.addCleanup(self.store.close)
        self.sid = self.fixture.snapshots[0]
        self.summary = self.store.summary(self.sid, FEATURES)
        self.summary_raw = F.compact(self.summary)

    def session(self, **limits): return SearchSession(NS, FEATURES, {**SESSION_LIMITS, **limits}, clock=Clock())

    def adopt(self, session):
        pending = session.begin_summary("p", self.sid, 262144)
        return session.accept(pending["ticket"], self.summary_raw)

    def ticket(self, session, provider="p", **limits):
        return session.begin_candidates(provider, self.sid, P, 0, {**QUERY_LIMITS, **limits})

    def raw(self, ticket): return F.compact(K.page(self.store, ticket["request"]))

    def test_client_offer_candidates_and_page_share_budgets_and_dedup_not_coverage(self):
        session, calls = self.session(), []
        provider = H.Provider(index=SelectedIndex(self.store, self.sid))
        async def exchange(endpoint, route, request, maximum, timeout):
            calls.append((route, deepcopy(request)))
            value = provider.dispatch(route, request)
            raw = value if type(value) is bytes else F.compact(value)
            self.assertLessEqual(len(raw), maximum)
            return {"status": 200, "raw": raw, "request_bytes": len(F.compact(request)),
                    "reply_bytes": len(raw), "header_bytes": 0}
        client = C.SearchClient(session, {"p": H.Endpoint("127.0.0.1", 1), "q": H.Endpoint("127.0.0.1", 2)})
        with patch.object(C, "exchange", new=exchange):
            offered = asyncio.run(client.offer("p", 16384))
            baseline = session.report()["coverage"]
            first = asyncio.run(client.candidates("p", offered["snapshot_id"], P, 0, QUERY_LIMITS))
            self.assertEqual(session.report()["coverage"], baseline)
            self.assertEqual(session.last_verified, {})
            page = asyncio.run(client.page("p", offered["snapshot_id"], P, 0, PAGE_LIMITS))
            again = asyncio.run(client.candidates("q", offered["snapshot_id"], P, 0, QUERY_LIMITS))
        self.assertNotIn("snapshot_id", calls[0][1]); self.assertEqual(calls[1][0], H.CANDIDATE_ROUTE)
        self.assertEqual(first["status"], "VERIFIED_CANDIDATES"); self.assertEqual(len(first["new_matches"]), 1)
        self.assertFalse(first["verified_scan_coverage"]); self.assertEqual(len(first["matches"]), 1)
        self.assertEqual(page["new_matches"], []); self.assertEqual(page["duplicate_matches"], 1)
        self.assertEqual(again["new_matches"], []); self.assertEqual(again["duplicate_matches"], 1)
        report = client.report()
        self.assertEqual(report["session"]["used"]["examined"], 32+10+32)
        self.assertEqual(report["session"]["used"]["candidates"], 3)
        self.assertEqual(report["session"]["used"]["pages"], 3)
        self.assertEqual(report["session"]["used"]["requests"], 4)
        self.assertEqual(report["session"]["snapshot_budget"]["charged_attempt_slots"], 1)
        self.assertEqual(report["session"]["candidate_search"], {"charged_scan_allowances": 64,
            "unique_verified_records": 1, "duplicate_verified_hits": 2,
            "alternative_metadata_claims": 0, "duplicates_still_charged": True})
        self.assertEqual(report["session"]["coverage"][self.sid]["partitions"][P]["intervals"], [[0, 10]])
        self.assertEqual(report["session"]["used"]["bytes"], report["http"]["actual_reply_bytes"])
        report["session"]["last_advisory"].clear()
        self.assertIn(self.sid, session.last_advisory)

    def test_zero_work_claim_never_refunds_reserved_scan_allowance(self):
        session = self.session(examined=32); self.adopt(session)
        ticket = self.ticket(session); response = F.strict(self.raw(ticket), QUERY_LIMITS["bytes"])
        response.update(hits=[], next=0, termination="time_exhausted",
                        charged={key: 0 for key in K.CHARGES},
                        next_cursor=K.cursor(ticket["request"], response["query_id"], 0))
        result = session.accept(ticket["ticket"], F.compact(response))
        self.assertEqual(result["status"], "VERIFIED_CANDIDATES"); self.assertEqual(result["matches"], [])
        self.assertEqual(session.used["examined"], 32); self.assertEqual(session.used["candidates"], 0)
        self.assertEqual(session.report()["coverage"][self.sid]["partitions"][P]["intervals"], [])
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:examined"): self.ticket(session)

    def test_invalid_raw_proof_or_assurance_charges_full_allowances_without_adoption(self):
        for bad in ("json", "proof", "assurance"):
            session = self.session(); self.adopt(session); before = session.report()
            ticket = self.ticket(session); response = F.strict(self.raw(ticket), QUERY_LIMITS["bytes"])
            if bad == "proof": response["hits"][0]["siblings"][0] = "f"*64
            if bad == "assurance": response["global_complete"] = True
            raw = b"not JSON" if bad == "json" else F.compact(response)
            with self.subTest(bad=bad), self.assertRaises(ValueError): session.accept(ticket["ticket"], raw)
            self.assertEqual(session.used["examined"], 32); self.assertEqual(session.used["candidates"], 8)
            self.assertEqual(session.used["bytes"], before["used"]["bytes"]+len(raw))
            self.assertEqual(session.report()["coverage"], before["coverage"])
            self.assertEqual(session.last_advisory, {}); self.assertEqual(session.seen_candidates, {})
            self.assertEqual(session.reserved, {"bytes": 0, "examined": 0, "candidates": 0})

    def test_private_ticket_and_post_verify_deadline_preserve_bindings_and_state(self):
        session = self.session(); self.adopt(session); ticket = self.ticket(session); raw = self.raw(ticket)
        ident = ticket["ticket"]
        ticket["request"]["start"] = 9; ticket["request"]["limits"]["scanned"] = 1
        ticket["features"].clear(); ticket["max_reply_bytes"] = 1; ticket["provider"] = "other"
        result = session.accept(ident, raw)
        self.assertEqual(result["status"], "VERIFIED_CANDIDATES"); self.assertEqual(session.used["examined"], 32)
        self.assertEqual(session.last_advisory[self.sid][P]["provider"], "p")
        late = self.session(); self.adopt(late); ticket = self.ticket(late); before = late.report()
        raw, original = self.raw(ticket), K.verify_page
        def expire(*args, **kwargs):
            value = original(*args, **kwargs); late.clock.value = 100; return value
        with patch.object(K, "verify_page", side_effect=expire):
            with self.assertRaisesRegex(ValueError, "SESSION_DEADLINE_EXHAUSTED"): late.accept(ticket["ticket"], raw)
        self.assertEqual(late.used["examined"], 32); self.assertEqual(late.used["candidates"], 8)
        self.assertEqual(late.report()["coverage"], before["coverage"])
        self.assertEqual(late.last_advisory, {}); self.assertEqual(late.seen_candidates, {})

    def test_unknown_transport_and_http_error_are_charged_once_without_retry(self):
        for failure in ("transport", "http"):
            session = self.session(); self.adopt(session); before = dict(session.used); calls = []
            async def exchange(endpoint, route, request, maximum, timeout):
                calls.append(route)
                if failure == "transport": raise ValueError("TRANSPORT_FAILED")
                return {"status": 503, "raw": b"{}", "request_bytes": len(F.compact(request)),
                        "reply_bytes": 2, "header_bytes": 0}
            client = C.SearchClient(session, {"p": H.Endpoint("127.0.0.1", 1)})
            with patch.object(C, "exchange", new=exchange), self.assertRaises(ValueError):
                asyncio.run(client.candidates("p", self.sid, P, 0, QUERY_LIMITS))
            self.assertEqual(calls, [H.CANDIDATE_ROUTE]); self.assertEqual(session.used["examined"], 32)
            self.assertEqual(session.used["candidates"], 8)
            self.assertEqual(session.used["bytes"], before["bytes"]+QUERY_LIMITS["bytes"])
            self.assertEqual(session.pending, {}); self.assertEqual(session.last_advisory, {})
            with self.assertRaisesRegex(ValueError, "SESSION_TICKET_NOT_PENDING"): session.abandon(session.sequence)
            self.assertEqual(session.used["examined"], 32)

    def test_concurrent_and_cross_api_limits_prevent_free_allowance_reset(self):
        session = self.session(examined=64); self.adopt(session)
        first, second = self.ticket(session), self.ticket(session)
        self.assertEqual(session.reserved["examined"], 64)
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:inflight"): self.ticket(session)
        session.accept(first["ticket"], self.raw(first))
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:examined"): self.ticket(session)
        session.accept(second["ticket"], self.raw(second))
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:examined"):
            session.begin_page("p", self.sid, P, 0, PAGE_LIMITS)
        limited = self.session(pages=1); self.adopt(limited); pending = self.ticket(limited); limited.abandon(pending["ticket"])
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:pages"):
            limited.begin_page("p", self.sid, P, 0, PAGE_LIMITS)
        byte_limited = self.session(bytes=len(self.summary_raw)+QUERY_LIMITS["bytes"])
        # Use the precise known summary bound so its reservation itself fits.
        pending = byte_limited.begin_summary("p", self.sid, len(self.summary_raw))
        byte_limited.accept(pending["ticket"], self.summary_raw)
        pending = self.ticket(byte_limited)
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:bytes"): self.ticket(byte_limited)
        byte_limited.abandon(pending["ticket"])
        self.assertEqual(byte_limited.used["bytes"], byte_limited.limits["bytes"])
        hit_limited = self.session(candidates=8); self.adopt(hit_limited)
        pending = self.ticket(hit_limited); hit_limited.accept(pending["ticket"], self.raw(pending))
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:candidates"): self.ticket(hit_limited)

    def conflicting_summary(self):
        changed, io, rows, root = deepcopy(self.fixture.hit), Memory(), [], A.map_empty(NS)[0]
        changed["object_sha256"] = "f"*64
        for feature in FEATURES:
            parts = [A.empty_descriptor(NS, feature, p) for p in range(256)]
            ctx = A.context(NS, feature, P)
            tree = A.append_vector(io, ctx, 0, A.vector_empty(ctx), F.record_id(changed))
            parts[P] = dict(partition=P, count=1, tree_root=tree)
            root = A.map_set(io, NS, root, feature, A.feature_root(NS, feature, parts))
            rows.append({"feature_id": feature, "partitions": parts})
        descriptor = {**self.summary["snapshot"], "feature_map_root": root, "local_cut": 1, "previous_snapshot": None}
        sid = A.snapshot_id(descriptor)
        for row in rows: row["siblings"] = A.map_get(io, NS, root, row["feature_id"])[1]
        return changed, {**self.summary, "snapshot_id": sid, "snapshot": descriptor, "rows": rows}

    def test_poison_first_provider_cannot_suppress_later_honest_candidate(self):
        session = self.session()
        changed, summary = self.conflicting_summary(); sid = summary["snapshot_id"]
        pending = session.begin_summary("q", sid, 262144)
        session.accept(pending["ticket"], F.compact(summary))
        pending = session.begin_candidates("q", sid, P, 0, QUERY_LIMITS)
        query = Q.query_id(NS, FEATURES)
        response = {"schema": "DMKN_FORMAL_CANDIDATE_PAGE_V1", "namespace": NS, "snapshot_id": sid,
                    "query_id": query, "partition": P, "anchor": FEATURES[0], "start": 0, "next": 1,
                    "anchor_count": 1, "hits": [{"ordinal": 0, "record": changed, "siblings": []}],
                    "next_cursor": None, "termination": "anchor_boundary",
                    "charged": dict(scanned=1, record_probes=3, node_reads=1, hash_calls=1,
                                    sql_vm_steps=100, record_loads=1, proofs=1), "coverage": K.CLAIM,
                    "global_complete": False, "mathematical_acceptance": False}
        poison = session.accept(pending["ticket"], F.compact(response))
        self.assertEqual(poison["new_matches"], [changed]); self.assertEqual(poison["metadata_conflicts"], [])
        self.adopt(session)
        pending = self.ticket(session); honest = session.accept(pending["ticket"], self.raw(pending))
        self.assertEqual(honest["new_matches"], [self.fixture.hit])
        self.assertEqual(honest["duplicate_matches"], 0); self.assertEqual(len(honest["metadata_conflicts"]), 1)
        self.assertEqual(honest["metadata_conflicts"][0]["object_id"], changed["object_id"])
        self.assertEqual(len(session.seen_candidates), 2)
        self.assertEqual(session.used["examined"], 64); self.assertEqual(session.used["candidates"], 2)
        self.assertEqual(session.report()["coverage"][sid]["partitions"][P]["intervals"], [])
        self.assertEqual(session.report()["coverage"][self.sid]["partitions"][P]["intervals"], [])
        pending = session.begin_page("p", self.sid, P, 0, PAGE_LIMITS)
        ordinary = self.store.page(pending["request"])
        duplicate = session.accept(pending["ticket"], F.compact(ordinary))
        self.assertEqual(duplicate["new_matches"], []); self.assertEqual(duplicate["duplicate_matches"], 1)
        self.assertEqual(session.used["candidates"], 3)
        self.assertEqual(session.report()["coverage"][self.sid]["partitions"][P]["intervals"], [[0, 10]])

    def test_provider_memory_http_uses_wire_reservation_and_owner_time_ceiling(self):
        session = self.session(); self.adopt(session); ticket = self.ticket(session)
        provider = H.Provider(index=self.store, max_reply_bytes=QUERY_LIMITS["bytes"])
        with patch.object(K, "page", wraps=K.page) as calls:
            first = asyncio.run(memory_request(provider, H.CANDIDATE_ROUTE, ticket["request"]))
            second = asyncio.run(memory_request(provider, H.CANDIDATE_ROUTE, ticket["request"]))
        head, raw = first.split(b"\r\n\r\n", 1)
        self.assertTrue(head.startswith(b"HTTP/1.1 200 OK")); self.assertEqual(second, b"")
        self.assertEqual(calls.call_count, 1); self.assertEqual(provider.status()["failures"], 1)
        self.assertEqual(provider.status()["reserved_reply_bytes"], 0)
        self.assertEqual(session.accept(ticket["ticket"], raw)["status"], "VERIFIED_CANDIDATES")
        constrained = H.Provider(index=self.store, operation_ms=20)
        original = deepcopy(ticket["request"])
        with patch.object(K, "page", return_value={"stub": True}) as selected:
            constrained.dispatch(H.CANDIDATE_ROUTE, original)
        self.assertEqual(selected.call_args.args[1]["limits"]["timeout_ms"], 20)
        self.assertEqual(original["limits"]["timeout_ms"], QUERY_LIMITS["timeout_ms"])

    def test_unverified_snapshot_unconfigured_contact_and_bad_request_refuse_before_dispatch(self):
        session = self.session()
        with self.assertRaisesRegex(ValueError, "SESSION_VERIFIED_SUMMARY_REQUIRED"): self.ticket(session)
        self.assertEqual(session.used["requests"], 0)
        self.adopt(session); before = session.used["requests"]
        client = C.SearchClient(session, {"p": H.Endpoint("127.0.0.1", 1)})
        with self.assertRaisesRegex(ValueError, "ENDPOINT_NOT_CONFIGURED"):
            asyncio.run(client.candidates("referral", self.sid, P, 0, QUERY_LIMITS))
        self.assertEqual(session.used["requests"], before)
        provider = H.Provider(index=self.store); ticket = self.ticket(session)
        with patch.object(K, "page") as calls:
            for change in ({"schema": "DMKN_FORMAL_QUERY_REQUEST_V1"}, {"namespace": "f"*64}):
                with self.assertRaises(ValueError): provider.dispatch(H.CANDIDATE_ROUTE, {**ticket["request"], **change})
            self.assertEqual(calls.call_count, 0)
        def expired(): raise ValueError("OWNER_PROVIDER_DEADLINE")
        with self.assertRaisesRegex(ValueError, "OWNER_PROVIDER_DEADLINE"):
            provider.dispatch(H.CANDIDATE_ROUTE, ticket["request"], check_budget=expired)


if __name__ == "__main__": unittest.main(verbosity=2)

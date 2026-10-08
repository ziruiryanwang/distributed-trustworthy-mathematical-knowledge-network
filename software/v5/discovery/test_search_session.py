"""Bounded session controls using synthetic authenticated metadata, no network."""
from pathlib import Path
from copy import deepcopy
import hashlib
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import formal_features as F
from discovery import authenticated_index as A
from discovery import discovery_query as Q
from discovery import search_session as S


def key(text): return hashlib.sha256(text.encode("ascii")).hexdigest()
NS, FEATURE = key("session-ns"), key("session-feature")
LIMITS = dict(providers=2, snapshots=2, requests=16, pages=10, examined=32,
              candidates=16, bytes=262144, wall_ms=1000, inflight=2)
PAGE_LIMITS = dict(examined=2, matches=1, bytes=16384, timeout_ms=1000, node_reads=100000)


class Clock:
    def __init__(self): self.value = 0
    def __call__(self): return self.value


class Memory:
    def __init__(self): self.nodes = {}
    def put_node(self, node):
        digest = A.node_hash(node); self.nodes[digest] = deepcopy(node); return digest
    def get_node(self, digest): return deepcopy(self.nodes[digest])


class Fixture:
    def __init__(self):
        self.io, self.ctx = Memory(), A.context(NS, FEATURE, 7)
        self.records = [{"schema": F.RECORD_SCHEMA, "namespace": NS, "kind": "synthetic-session",
                         "object_id": "07" + key("object"+str(i))[2:], "object_sha256": key("raw"+str(i)),
                         "object_bytes": 1, "features": [FEATURE]} for i in range(3)]
        self.root = A.vector_empty(self.ctx)
        for i, row in enumerate(self.records):
            self.root = A.append_vector(self.io, self.ctx, i, self.root, F.record_id(row))
        descriptors = [A.empty_descriptor(NS, FEATURE, p) for p in range(256)]
        descriptors[7] = {"partition": 7, "count": 3, "tree_root": self.root}
        feature_root = A.feature_root(NS, FEATURE, descriptors)
        map_root = A.map_set(self.io, NS, A.map_empty(NS)[0], FEATURE, feature_root)
        self.snapshot = {"schema": "DMKN_FORMAL_INDEX_SNAPSHOT_V1", "namespace": NS,
                         "feature_schema": F.SCHEMA, "partition_bits": 8, "feature_map_root": map_root,
                         "local_cut": 3, "previous_snapshot": None,
                         "coverage_claim": "PROVIDER_SELECTED_FEATURE_RECORDS_NOT_GLOBAL_CORPUS"}
        self.sid = A.snapshot_id(self.snapshot)
        _, siblings = A.map_get(self.io, NS, map_root, FEATURE)
        self.summary = {"schema": "DMKN_FORMAL_QUERY_SUMMARY_V1", "namespace": NS,
                        "snapshot_id": self.sid, "snapshot": self.snapshot, "features": [FEATURE],
                        "rows": [{"feature_id": FEATURE, "partitions": descriptors, "siblings": siblings}],
                        "coverage": "COMMITTED_METADATA_NOT_SOURCE_CORPUS", "mathematical_acceptance": False}

    def page(self, request):
        start = request["start"]
        _, siblings = A.vector_get(self.io, self.ctx, 3, self.root, start)
        return {"schema": "DMKN_FORMAL_QUERY_PAGE_V1", "namespace": NS, "snapshot_id": self.sid,
                "query_id": Q.query_id(NS, [FEATURE]), "partition": 7, "anchor": FEATURE,
                "start": start, "next": start+1, "anchor_count": 3,
                "examined": [{"ordinal": start, "record": deepcopy(self.records[start]), "siblings": siblings}],
                "match_ordinals": [start], "next_cursor": None if start == 2 else Q.cursor(request, start+1),
                "termination": "anchor_exhausted" if start == 2 else "matches_exhausted",
                "charged": {"node_reads": 3, "examined": 1},
                "coverage": "COMMITTED_ANCHOR_INTERVAL_ONLY", "mathematical_acceptance": False}


class SessionContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.fixture = Fixture()

    def session(self, **overrides):
        return S.SearchSession(NS, [FEATURE], {**LIMITS, **overrides}, clock=Clock())

    def adopt(self, session):
        ticket = session.begin_summary("provider-a", self.fixture.sid, 65536)
        return session.accept(ticket["ticket"], F.compact(self.fixture.summary))

    def test_portable_pages_preserve_private_coverage_and_cursors(self):
        session = self.session()
        self.adopt(session)
        first = session.begin_page("provider-a", self.fixture.sid, 7, 0, PAGE_LIMITS)
        page = session.accept(first["ticket"], F.compact(self.fixture.page(first["request"])))
        self.assertEqual(page["next"], 1)
        second = session.begin_page("provider-b", self.fixture.sid, 7, 1, PAGE_LIMITS)
        session.accept(second["ticket"], F.compact(self.fixture.page(second["request"])))
        report = session.report()
        self.assertEqual(report["used"]["providers"], 2)
        self.assertEqual(report["used"]["examined"], 2)
        self.assertEqual(report["used"]["candidates"], 2)
        self.assertEqual(report["coverage"][self.fixture.sid]["partitions"][7]["intervals"], [[0, 2]])
        self.assertEqual(report["last_verified"][self.fixture.sid][7]["next"], 2)
        self.assertFalse(report["global_complete"])
        # Caller mutation cannot reset the session's private state.
        report["coverage"].clear()
        self.assertIn(self.fixture.sid, session.report()["coverage"])

    def test_invalid_raw_bytes_are_charged_without_adoption(self):
        session = self.session()
        ticket = session.begin_summary("provider-a", self.fixture.sid, 65536)
        with self.assertRaises(ValueError): session.accept(ticket["ticket"], b"not canonical JSON")
        report = session.report()
        self.assertEqual(report["used"]["bytes"], len(b"not canonical JSON"))
        self.assertEqual(report["pending_requests"], 0)
        self.assertEqual(report["coverage"], {})
        self.assertEqual(report["used"]["requests"], 1)

    def test_invalid_page_retains_last_verified_cursor_and_charges(self):
        session = self.session(); self.adopt(session)
        first = session.begin_page("provider-a", self.fixture.sid, 7, 0, PAGE_LIMITS)
        session.accept(first["ticket"], F.compact(self.fixture.page(first["request"])))
        before = session.report()
        next_ticket = session.begin_page("provider-a", self.fixture.sid, 7, 1, PAGE_LIMITS)
        damaged = self.fixture.page(next_ticket["request"])
        damaged["examined"][0]["record"]["object_sha256"] = key("forged")
        raw = F.compact(damaged)
        with self.assertRaises(ValueError): session.accept(next_ticket["ticket"], raw)
        after = session.report()
        self.assertEqual(after["last_verified"], before["last_verified"])
        self.assertEqual(after["coverage"], before["coverage"])
        self.assertEqual(after["used"]["bytes"], before["used"]["bytes"] + len(raw))
        self.assertEqual(after["used"]["examined"], 3)  # 1 verified +2 reserved failed

    def test_reservations_and_abandonment_cannot_reuse_budget(self):
        session = self.session(bytes=65536)
        first = session.begin_summary("provider-a", self.fixture.sid, 65536)
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:bytes"):
            session.begin_summary("provider-a", self.fixture.sid, 1024)
        session.abandon(first["ticket"])
        self.assertEqual(session.report()["used"]["bytes"], 65536)
        with self.assertRaises(ValueError): session.begin_summary("provider-a", self.fixture.sid, 1024)
        with self.assertRaises(ValueError): session.abandon(first["ticket"])

    def test_provider_and_page_ceilings_are_workflow_wide(self):
        session = self.session(providers=1, pages=1)
        self.adopt(session)
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:providers"):
            session.begin_summary("provider-b", self.fixture.sid, 1024)
        first = session.begin_page("provider-a", self.fixture.sid, 7, 0, PAGE_LIMITS)
        session.abandon(first["ticket"])
        with self.assertRaisesRegex(ValueError, "SESSION_BUDGET:pages"):
            session.begin_page("provider-a", self.fixture.sid, 7, 0, PAGE_LIMITS)

    def test_deadline_after_verification_does_not_adopt_page(self):
        session = self.session(); self.adopt(session)
        ticket = session.begin_page("provider-a", self.fixture.sid, 7, 0, PAGE_LIMITS)
        original = Q.verify_page
        def expire(*args, **kwargs):
            verified = original(*args, **kwargs)
            session.clock.value = 2
            return verified
        with patch.object(Q, "verify_page", side_effect=expire):
            with self.assertRaisesRegex(ValueError, "SESSION_DEADLINE_EXHAUSTED"):
                session.accept(ticket["ticket"], F.compact(self.fixture.page(ticket["request"])))
        report = session.report()
        self.assertEqual(report["last_verified"], {})
        self.assertEqual(report["coverage"][self.fixture.sid]["partitions"][7]["intervals"], [])
        self.assertGreater(report["used"]["bytes"], 0)
        with self.assertRaises(ValueError): session.begin_summary("provider-a", self.fixture.sid, 1024)

    def test_oversized_transport_reply_poisoned_and_fully_charged(self):
        session = self.session()
        ticket = session.begin_summary("provider-a", self.fixture.sid, 1024)
        with self.assertRaisesRegex(ValueError, "SESSION_TRANSPORT_BYTE_VIOLATION"):
            session.accept(ticket["ticket"], b"x" * 1025)
        self.assertEqual(session.report()["used"]["bytes"], 1025)
        self.assertEqual(session.report()["status"], "TRANSPORT_BYTE_VIOLATION")
        with self.assertRaises(ValueError): session.begin_summary("provider-a", self.fixture.sid, 1024)


if __name__ == "__main__": unittest.main(verbosity=2)

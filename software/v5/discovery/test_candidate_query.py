"""Candidate-only boundary controls using real SQLite and synthetic commitments.

No mathematical, network, huge-corpus or speedup evidence. Root owns launches.
The fixture builds the same logical tables/indexes and lends an in-memory Store
to both actual query algorithms; it does not exercise Store filesystem startup.
"""
from copy import deepcopy
from pathlib import Path
import sqlite3
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import authenticated_index as A
from discovery import formal_features as F
from discovery import discovery_query as Q
from discovery import candidate_query as C
from discovery.discovery_store import Store

def key(value): return F.digest("candidate-fixture", value)
NS = key("namespace")
FEATURES = sorted((key("a"), key("b")))
P = 7
LIMITS = dict(scanned=32, matches=8, bytes=65536, timeout_ms=1000,
              record_probes=256, node_reads=100000, hash_calls=2000000, sql_vm_steps=1000000)


class Clock:
    def __init__(self): self.value = 0
    def __call__(self): return self.value


class Memory:
    def __init__(self): self.nodes = {}
    def put_node(self, node):
        digest = A.node_hash(node); self.nodes[digest] = deepcopy(node); return digest
    def get_node(self, key): return deepcopy(self.nodes[key])


class Fixture:
    def __init__(self):
        self.db, self.io, self.seq, self.parts = sqlite3.connect(":memory:"), Memory(), 0, {}
        self.snapshots, self.summaries, self.records = [], [], []
        self.db.executescript("""
            CREATE TABLE objects(object_id TEXT PRIMARY KEY,record_id TEXT NOT NULL UNIQUE,
              record BLOB NOT NULL,admitted_seq INTEGER NOT NULL) WITHOUT ROWID;
            CREATE TABLE postings(feature_id TEXT NOT NULL,partition INTEGER NOT NULL,
              ordinal INTEGER NOT NULL,object_id TEXT NOT NULL,
              PRIMARY KEY(feature_id,partition,ordinal),UNIQUE(feature_id,partition,object_id)) WITHOUT ROWID;
            CREATE TABLE cas_nodes(hash TEXT PRIMARY KEY,encoded BLOB NOT NULL) WITHOUT ROWID;
            CREATE TABLE snapshots(snapshot_id TEXT PRIMARY KEY,descriptor BLOB NOT NULL) WITHOUT ROWID;
        """)
        for i in range(9): self.add("a-only-"+str(i), [FEATURES[0]])
        # Extra committed features make the positive record large enough to
        # exercise the smallest whole-envelope byte allowance deterministically.
        self.hit = self.add("old-hit", sorted([*FEATURES, *(key("extra"+str(i)) for i in range(10))]))
        for i in range(19): self.add("b-only-"+str(i), [FEATURES[1]])
        self.seal()
        self.late = self.add("later-hit", FEATURES)
        self.seal(); self.db.commit()

    def add(self, name, features):
        self.seq += 1
        record = {"schema": F.RECORD_SCHEMA, "namespace": NS, "kind": "synthetic-candidate",
                  "object_id": "07"+key(name)[2:], "object_sha256": key("bytes-"+name),
                  "object_bytes": 1, "features": list(features)}
        rid = F.record_id(record)
        self.db.execute("INSERT INTO objects VALUES(?,?,?,?)", (record["object_id"], rid, F.compact(record), self.seq))
        for f in features:
            if f not in self.parts: self.parts[f] = [A.empty_descriptor(NS, f, p) for p in range(256)]
            old = self.parts[f][P]
            tree = A.append_vector(self.io, A.context(NS, f, P), old["count"], old["tree_root"], rid)
            self.db.execute("INSERT INTO postings VALUES(?,?,?,?)", (f, P, old["count"], record["object_id"]))
            self.parts[f][P] = dict(partition=P, count=old["count"]+1, tree_root=tree)
        self.records.append(record)
        return record

    def seal(self):
        root = A.map_empty(NS)[0]
        for f, parts in sorted(self.parts.items()):
            # feature_root computes only a hash. Like actual Store.admit, the
            # fixture must materialize each nonempty partition path in CAS.
            partition_root = A.partition_empty()[8]
            for descriptor in parts:
                if descriptor["count"]:
                    partition_root = A.partition_set(self.io, NS, f, partition_root, descriptor)
            F.need(partition_root == A.feature_root(NS, f, parts), "FIXTURE_PARTITION_ROOT_BINDING")
            root = A.map_set(self.io, NS, root, f, partition_root)
        snapshot = {"schema": "DMKN_FORMAL_INDEX_SNAPSHOT_V1", "namespace": NS,
                    "feature_schema": F.SCHEMA, "partition_bits": 8, "feature_map_root": root,
                    "local_cut": self.seq, "previous_snapshot": self.snapshots[-1] if self.snapshots else None,
                    "coverage_claim": "PROVIDER_SELECTED_FEATURE_RECORDS_NOT_GLOBAL_CORPUS"}
        sid = A.snapshot_id(snapshot)
        self.db.execute("INSERT INTO snapshots VALUES(?,?)", (sid, F.compact(snapshot)))
        for digest, node in self.io.nodes.items():
            self.db.execute("INSERT OR IGNORE INTO cas_nodes VALUES(?,?)", (digest, F.compact(node)))
        summary = {"schema": "DMKN_FORMAL_QUERY_SUMMARY_V1", "namespace": NS, "snapshot_id": sid,
                   "snapshot": snapshot, "features": FEATURES,
                   "rows": [{"feature_id": f, "partitions": deepcopy(self.parts[f]),
                             "siblings": A.map_get(self.io, NS, root, f)[1]} for f in FEATURES],
                   "coverage": "COMMITTED_METADATA_NOT_SOURCE_CORPUS", "mathematical_acceptance": False}
        self.snapshots.append(sid); self.summaries.append(Q.verify_summary(sid, NS, FEATURES, summary))

    def store(self):
        store = Store.__new__(Store)
        store.namespace, store.feature_schema, store.db = NS, F.SCHEMA, sqlite3.connect(":memory:")
        self.db.backup(store.db)
        return store


class CandidateContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.fixture = Fixture()
    @classmethod
    def tearDownClass(cls): cls.fixture.db.close()
    def setUp(self):
        self.store = self.fixture.store(); self.addCleanup(self.store.close)

    def request(self, *, cut=0, start=0, **limits):
        return {"schema": "DMKN_FORMAL_CANDIDATE_REQUEST_V1", "namespace": NS,
                "snapshot_id": self.fixture.snapshots[cut], "features": list(FEATURES),
                "partition": P, "anchor": FEATURES[0], "start": start, "limits": {**LIMITS, **limits}}

    def verify(self, request, response, cut=0): return C.verify_page(self.fixture.summaries[cut], request, response)

    def test_only_survivors_load_records_and_build_proofs_compared_with_exhaustive_page(self):
        request = self.request(); statements = []
        self.store.db.set_trace_callback(statements.append)
        response = C.page(self.store, request); self.store.db.set_trace_callback(None)
        result = self.verify(request, response)
        self.assertEqual([r["object_id"] for r in result["matches"]], [self.fixture.hit["object_id"]])
        self.assertEqual(response["charged"]["scanned"], 10)
        self.assertEqual(response["charged"]["record_loads"], 1); self.assertEqual(response["charged"]["proofs"], 1)
        loads = [s for s in statements if s.startswith("SELECT record_id,record FROM objects")]
        self.assertEqual(len(loads), 1)
        self.assertFalse(result["verified_scan_coverage"]); self.assertFalse(result["mathematical_acceptance"])
        self.assertEqual(response["termination"], "anchor_boundary")
        old_request = {**request, "schema": "DMKN_FORMAL_QUERY_REQUEST_V1",
                       "limits": dict(examined=32, matches=8, bytes=65536, timeout_ms=1000, node_reads=100000)}
        with patch.object(self.store, "_record", wraps=self.store._record) as record_loads:
            exhaustive = self.store.page(old_request)
        verified = Q.verify_page(self.fixture.summaries[0], old_request, exhaustive)
        self.assertEqual(verified["matches"], result["matches"])
        self.assertEqual(record_loads.call_count, 10)
        self.assertLess(len(F.compact(response)), len(F.compact(exhaustive)))
        coverage = Q.Coverage(self.fixture.summaries[0]); before = coverage.report()
        with self.assertRaises(ValueError): coverage.accept(request, response)
        self.assertEqual(coverage.report(), before)

    def test_old_snapshot_cutoffs_reject_later_feature_posting_before_record_load(self):
        old = self.request(); response = C.page(self.store, old)
        self.assertEqual(response["anchor_count"], 10)
        self.assertEqual([row["record"]["object_id"] for row in response["hits"]], [self.fixture.hit["object_id"]])
        new = self.request(cut=1); current = C.page(self.store, new)
        self.assertEqual([r["object_id"] for r in self.verify(new, current, 1)["matches"]],
                         [self.fixture.hit["object_id"], self.fixture.late["object_id"]])
        # Poison the old hit's secondary posting ordinal to the later position.
        # A current-membership-only implementation would still load/return it.
        self.store.db.execute("DELETE FROM postings WHERE feature_id=? AND object_id=?", (FEATURES[1], self.fixture.late["object_id"]))
        self.store.db.execute("UPDATE postings SET ordinal=20 WHERE feature_id=? AND object_id=?",
                              (FEATURES[1], self.fixture.hit["object_id"]))
        refused = C.page(self.store, old); self.verify(old, refused)
        self.assertEqual(refused["hits"], []); self.assertEqual(refused["charged"]["record_loads"], 0)
        self.assertEqual(refused["charged"]["proofs"], 0)

    def test_scan_probe_match_and_byte_terminations_leave_advisory_positions(self):
        for limits, reason, position in (({"scanned": 3}, "scanned_exhausted", 3),
                                          ({"record_probes": 5}, "record_probes_exhausted", 2),
                                          ({"bytes": 2048}, "bytes_exhausted", 9)):
            request = self.request(**limits); response = C.page(self.store, request)
            with self.subTest(reason=reason):
                self.verify(request, response)
                self.assertEqual((response["termination"], response["next"]), (reason, position))
                self.assertEqual(response["hits"], [])
                self.assertEqual(response["next_cursor"]["assurance"], "ADVISORY_POSITION_NOT_VERIFIED_COVERAGE")
        request = self.request(cut=1, matches=1); response = C.page(self.store, request)
        self.verify(request, response, 1)
        self.assertEqual((response["termination"], response["next"]), ("matches_exhausted", 10))
        continuation = self.request(cut=1, start=response["next"])
        remaining = C.page(self.store, continuation)
        self.assertEqual([r["object_id"] for r in self.verify(continuation, remaining, 1)["matches"]],
                         [self.fixture.late["object_id"]])

    def test_setup_read_hash_vm_refusals_preserve_shape_and_connection_settings(self):
        self.store.db.execute("PRAGMA busy_timeout=73")
        for limits, reason in (({"node_reads": 1}, "node_reads_exhausted"),
                               ({"hash_calls": 1}, "hash_calls_exhausted"),
                               ({"sql_vm_steps": 100}, "sql_vm_steps_exhausted")):
            request = self.request(**limits); response = C.page(self.store, request)
            with self.subTest(reason=reason):
                self.verify(request, response)
                self.assertEqual(response["termination"], reason)
                self.assertEqual(response["hits"], []); self.assertEqual(response["next"], 0)
                self.assertIsNone(response["anchor_count"])
                self.assertEqual(self.store.db.execute("PRAGMA busy_timeout").fetchone()[0], 73)
        # Exercise the actual callback abort, not only pre-statement allowance.
        io = C._ReadIO(self.store.db, {**LIMITS, "sql_vm_steps": 200}, Clock())
        self.store.db.set_progress_handler(io.progress, 100)
        try:
            with self.assertRaisesRegex(C._Stop, "sql_vm_steps_exhausted"):
                io.one("WITH RECURSIVE r(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM r WHERE n<1000) SELECT sum(n) FROM r")
            self.assertEqual(io.interrupted, "sql_vm_steps_exhausted")
            self.assertEqual(io.used["sql_vm_steps"], 200)
        finally: self.store.db.set_progress_handler(None, 0)

    def test_partial_proof_or_deadline_never_skips_the_unfinished_positive(self):
        for how in ("node", "deadline"):
            clock = Clock(); request = self.request(); original = A.vector_get
            def interrupt(*args, **kwargs):
                if how == "node": raise C._Stop("node_reads_exhausted")
                result = original(*args, **kwargs); clock.value = 2; return result
            with patch.object(A, "vector_get", side_effect=interrupt): response = C.page(self.store, request, clock=clock)
            self.verify(request, response)
            self.assertEqual(response["next"], 9); self.assertEqual(response["hits"], [])
            self.assertEqual(response["next_cursor"]["next"], 9)
            self.assertEqual(response["charged"]["record_loads"], 1); self.assertEqual(response["charged"]["proofs"], 1)
            self.assertEqual(response["termination"], "node_reads_exhausted" if how == "node" else "time_exhausted")

    def test_corrupted_membership_missing_features_bindings_and_false_coverage_refuse(self):
        request = self.request(); good = C.page(self.store, request)
        changed = []
        for field, value in (("coverage", "COMPLETE"), ("global_complete", True), ("mathematical_acceptance", True),
                             ("snapshot_id", "f"*64), ("next", 0), ("anchor_count", 999)):
            bad = deepcopy(good); bad[field] = value; changed.append(bad)
        for action in ("hash", "proof", "features", "duplicate", "ordinal"):
            bad = deepcopy(good); hit = bad["hits"][0]
            if action == "hash": hit["record"]["object_sha256"] = "f"*64
            elif action == "proof": hit["siblings"][0] = "f"*64
            elif action == "features": hit["record"]["features"].remove(FEATURES[1])
            elif action == "duplicate": bad["hits"].append(deepcopy(hit))
            else: hit["ordinal"] = 0
            changed.append(bad)
        for bad in changed:
            with self.assertRaises(ValueError): self.verify(request, bad)
        def expired(): raise ValueError("OWNER_VERIFY_DEADLINE")
        with self.assertRaisesRegex(ValueError, "OWNER_VERIFY_DEADLINE"):
            C.verify_page(self.fixture.summaries[0], request, good, check_budget=expired)

    def test_corrupt_full_record_fails_and_restores_db_controls(self):
        self.store.db.execute("PRAGMA busy_timeout=57")
        damaged = {**self.fixture.hit, "object_sha256": "f"*64}
        self.store.db.execute("UPDATE objects SET record=? WHERE object_id=?",
                              (F.compact(damaged), self.fixture.hit["object_id"]))
        with self.assertRaisesRegex(ValueError, "CANDIDATE_RECORD_BINDING"): C.page(self.store, self.request())
        self.assertEqual(self.store.db.execute("PRAGMA busy_timeout").fetchone()[0], 57)
        self.assertEqual(self.store.db.execute("SELECT count(*) FROM objects").fetchone()[0], 30)

    def test_committed_empty_cut_still_makes_no_global_absence_claim(self):
        missing = key("never-present")
        old = self.fixture.summaries[0]; descriptor = old["descriptor"]
        absent, siblings = A.map_get(self.fixture.io, NS, descriptor["feature_map_root"], missing)
        self.assertIsNone(absent)
        raw_summary = {"schema": "DMKN_FORMAL_QUERY_SUMMARY_V1", "namespace": NS,
                       "snapshot_id": old["snapshot_id"], "snapshot": descriptor, "features": [missing],
                       "rows": [{"feature_id": missing, "partitions": None, "siblings": siblings}],
                       "coverage": "COMMITTED_METADATA_NOT_SOURCE_CORPUS", "mathematical_acceptance": False}
        summary = Q.verify_summary(old["snapshot_id"], NS, [missing], raw_summary)
        request = {**self.request(), "features": [missing], "anchor": missing}
        response = C.page(self.store, request); result = C.verify_page(summary, request, response)
        self.assertEqual(response["termination"], "anchor_boundary")
        self.assertEqual(response["charged"]["scanned"], 0); self.assertEqual(response["hits"], [])
        self.assertFalse(result["global_complete"]); self.assertFalse(result["verified_scan_coverage"])

    def test_request_schemas_and_malformed_bounds_refuse_before_sql(self):
        statements = []; self.store.db.set_trace_callback(statements.append)
        for key, value in (("scanned", 0), ("matches", True), ("sql_vm_steps", 99), ("bytes", 2047),
                           ("hash_calls", 2000001), ("record_probes", 65537)):
            with self.assertRaises(ValueError): C.page(self.store, self.request(**{key: value}))
        request = self.request(); request["schema"] = "DMKN_FORMAL_QUERY_REQUEST_V1"
        with self.assertRaises(ValueError): C.page(self.store, request)
        request = self.request(); request["namespace"] = "f"*64
        with self.assertRaises(ValueError): C.page(self.store, request)
        self.store.db.set_trace_callback(None); self.assertEqual(statements, [])


if __name__ == "__main__": unittest.main(verbosity=2)

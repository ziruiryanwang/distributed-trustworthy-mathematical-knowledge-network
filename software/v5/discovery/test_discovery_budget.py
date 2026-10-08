"""Focused author-supplied actual Store budget boundary; root selects execution."""
from pathlib import Path
import argparse
import hashlib
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import formal_features as F
from discovery import discovery_store as S
from discovery import discovery_query as Q

EVIDENCE = None
NS = hashlib.sha256(b"synthetic-budget-namespace").hexdigest()
FEATURE = hashlib.sha256(b"synthetic-budget-feature").hexdigest()


class Adapter:
    namespace = NS

    def extract(self, raw, expected_id=None):
        digest = hashlib.sha256(raw).hexdigest()
        return {"schema": F.RECORD_SCHEMA, "namespace": NS, "kind": "synthetic-budget-only",
                "object_id": "07" + digest[2:], "object_sha256": digest,
                "object_bytes": len(raw), "features": [FEATURE]}


class BudgetBoundary(unittest.TestCase):
    def test_real_sqlite_work_exhaustion_keeps_verifiable_interval(self):
        limits = dict(max_objects=8, max_postings=8, max_features=8,
                      max_snapshots=9, max_logical_bytes=4194304, max_db_pages=4096)
        store = S.Store(EVIDENCE / "store", Adapter(), limits, create=True)
        try:
            for i in range(4):
                sid = store.admit(F.compact({"synthetic": i}))["snapshot_id"]
            summary = Q.verify_summary(sid, NS, [FEATURE], store.summary(sid, [FEATURE]))
            request = {"schema": "DMKN_FORMAL_QUERY_REQUEST_V1", "namespace": NS,
                       "snapshot_id": sid, "features": [FEATURE], "partition": 7,
                       "anchor": FEATURE, "start": 0,
                       "limits": dict(examined=32, matches=8, bytes=1048576,
                                      timeout_ms=1000, node_reads=269)}
            # Prelude =256 map nodes +1 map leaf +8 partition nodes +1 leaf.
            # Width4 membership =2 vector nodes +1 vector leaf. Thus269 allows
            # exactly one authenticated record; the next attempted read refuses
            # before increment, and the partial reply remains client-verifiable.
            response = store.page(request)
            verified = Q.verify_page(summary, request, response)
            self.assertEqual(verified["next"], 1)
            self.assertEqual(verified["termination"], "work_exhausted")
            self.assertEqual(response["charged"], {"node_reads": 269, "examined": 1})
            self.assertEqual(len(verified["matches"]), 1)
            request["limits"]["node_reads"] = 266
            response = store.page(request)
            verified = Q.verify_page(summary, request, response)
            self.assertEqual(verified["next"], 0)
            self.assertEqual(verified["termination"], "work_exhausted")
            self.assertEqual(response["charged"], {"node_reads": 266, "examined": 0})
            request["limits"]["node_reads"] = 265
            with self.assertRaisesRegex(ValueError, "NODE_READ_CAP"):
                store.page(request)
        finally:
            store.close()


def main():
    global EVIDENCE
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args()
    EVIDENCE = Path(args.evidence)
    if not EVIDENCE.is_absolute() or EVIDENCE.exists():
        raise ValueError("FRESH_ABSOLUTE_TEST_EVIDENCE")
    EVIDENCE.mkdir(parents=True)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BudgetBoundary)
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

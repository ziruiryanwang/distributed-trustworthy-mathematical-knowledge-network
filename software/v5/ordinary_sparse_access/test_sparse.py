"""Prospective native-free sparse access controls; root selects execution.

One coherent pinned package; actual fresh Store admission, summaries, positive
proofs and sessions. Generic forced-partition records and an ordinary preview
are deliberately unproved metadata. No sockets, native work, public API campaign,
retained operational state, or mathematical/growth acceptance claim.
"""
from __future__ import annotations

import time
START, CPU = time.monotonic(), time.process_time()
import argparse
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import sqlite3
import ssl  # Load the socket subclass before installing the no-socket guard.
import subprocess
import sys
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
DEADLINE = START + 90
CASES = []
BASE_LIMITS = dict(max_objects=64, max_postings=2048, max_features=128,
                   max_snapshots=65, max_logical_bytes=8*MIB, max_db_pages=2048)
PAGE_LIMITS = dict(scanned=16, matches=8, bytes=65536, timeout_ms=1000,
                   record_probes=256, node_reads=100000, hash_calls=2000000,
                   sql_vm_steps=1000000)
ATOM_A, ATOM_B, ATOM_C, ATOM_D = (str(i)*64 for i in range(1, 5))
PARTITION = 7


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic() < DEADLINE and time.process_time()-CPU < 60,
         "SPARSE_CONTROL_ORIGINAL_ENVELOPE")


def raw(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def identity(label):
    return hashlib.sha256(("UNPROVED-SPARSE-CONTROL:"+label).encode("ascii")).hexdigest()


def passed(label, **detail):
    check()
    need(len(CASES) < 48, "SPARSE_CONTROL_GROUP_CAP")
    CASES.append(dict(case=label, status="PASS", **detail))


def refuses(call, *, database=False, expected=None):
    check()
    try:
        call()
    except (ValueError, sqlite3.DatabaseError) as error:
        need(database or isinstance(error, ValueError), "SPARSE_CONTROL_UNEXPECTED_DB_ERROR")
        if expected is not None:
            need(str(error) == expected, "SPARSE_CONTROL_WRONG_REFUSAL:"+str(error))
        return str(error)
    raise AssertionError("SPARSE_CONTROL_MISSING_REFUSAL")


def forbidden(*args, **kwargs):
    raise AssertionError("SPARSE_CONTROL_FORBIDDEN_EXTERNAL_OPERATION")


def read(path, maximum=2*MIB):
    check()
    size = path.stat().st_size
    need(0 < size <= maximum, "SPARSE_CONTROL_READ_BOUND")
    with path.open("rb") as stream:
        value = stream.read(maximum+1)
    need(len(value) == size, "SPARSE_CONTROL_READ_CHANGED")
    return value


def save(path, value):
    content = raw(value)
    need(len(content) <= 2*MIB, "SPARSE_CONTROL_OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(content+b"\n")


def load_package(args):
    package = Path(args.package)
    need(package.is_absolute() and package.resolve(strict=True) == package,
         "SPARSE_CONTROL_PACKAGE_PATH")
    profile_raw = read(package/"PROFILE.json")
    need(hashlib.sha256(profile_raw).hexdigest() == args.profile_sha256,
         "SPARSE_CONTROL_PROFILE_PIN")
    descriptor = json.loads(profile_raw)
    source = read(package/"profile.py")
    pin = descriptor["files"]["profile.py"]
    need(len(source) == pin["bytes"] and hashlib.sha256(source).hexdigest() == pin["sha256"],
         "SPARSE_CONTROL_LOADER_PIN")
    spec = importlib.util.spec_from_file_location("_sparse_control_profile", package/"profile.py")
    loader = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = loader
    exec(compile(source, str(package/"profile.py"), "exec"), loader.__dict__)
    return loader.load(package, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        DEADLINE, check_parent=check)


class Clock:
    def __init__(self): self.value = 0.0
    def __call__(self): return self.value


class SyntheticAdapter:
    """Declared fake metadata authority, not a substitute ordinary adapter."""
    def __init__(self, features):
        self.F = features
        self.namespace, self.feature_schema = identity("generic-namespace"), features.SCHEMA

    def extract(self, value, expected_id=None):
        doc = self.F.strict(value, 16384)
        self.F.fields(doc, ("label", "features"))
        digest = hashlib.sha256(value).hexdigest()
        record = dict(schema=self.F.RECORD_SCHEMA, namespace=self.namespace,
            kind="synthetic-sparse-control", object_id="07"+identity(doc["label"])[2:],
            object_sha256=digest, object_bytes=len(value), features=doc["features"])
        self.F.validate_record(record, self.namespace)
        if expected_id is not None:
            self.F.need(record["object_id"] == expected_id, "SYNTHETIC_EXPECTED_ID")
        return record


def synthetic(label, features):
    return raw(dict(label=label, features=sorted(features)))


def config(pairs=None, *, rows=256, logical=MIB):
    pairs = [[ATOM_A, ATOM_B], [ATOM_A, ATOM_C]] if pairs is None else pairs
    return dict(pairs=deepcopy(pairs), limits=dict(max_rows=rows, max_logical_bytes=logical))


def logical_state(store):
    """Tiny fixture-only logical fingerprint, never a product query or repair."""
    tables = [row[0] for row in store.db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()]
    expected = {"meta", "objects", "postings", "cas_nodes", "feature_heads", "snapshots"}
    if store.access_pairs is not None:
        expected |= {"access_rows", "access_meta"}
    need(set(tables) == expected, "SPARSE_CONTROL_UNEXPECTED_TABLE")
    result = {}
    for table in tables:
        # Names are compared with the fixed allowlist before interpolation.
        rows = store.db.execute('SELECT * FROM "'+table+'"').fetchall()
        encoded = sorted(raw([{"hex": item.hex()} if isinstance(item, bytes) else item
                              for item in row]) for row in rows)
        digest = hashlib.sha256()
        for item in encoded:
            digest.update(len(item).to_bytes(8, "big")); digest.update(item)
        result[table] = dict(rows=len(rows), sha256=digest.hexdigest())
    return result


class Suite:
    def __init__(self, loaded, output):
        self.api, self.output = loaded.peer_api, output
        self.C, self.F, self.DS = self.api.CQ, self.api.F, self.api.DS
        self.Q, self.PA = self.C.Q, self.DS.PA
        self.adapter = SyntheticAdapter(self.F)
        self.stores, self.fixtures = [], {}

    def close(self):
        errors = []
        for store in reversed(self.stores):
            try: store.close()
            except BaseException as error: errors.append(type(error).__name__+":"+str(error))
        need(not errors, "SPARSE_CONTROL_STORE_CLEANUP:"+repr(errors))

    def store(self, label, *, adapter=None, access=None, create=True):
        check()
        store = self.DS.Store(self.output/label, adapter or self.adapter,
            deepcopy(BASE_LIMITS), create=create, access_pairs=deepcopy(access))
        self.stores.append(store)
        return store

    def admit(self, store, value):
        check()
        digest = hashlib.sha256(value).hexdigest()
        self.fixtures[digest] = value.decode("ascii")
        result = store.admit(value)
        need(result["mathematical_acceptance"] is False, "SPARSE_CONTROL_ADMIT_NOT_MATH")
        return result

    def query(self, store, sid, features, *, sparse=True, start=0, partition=PARTITION, **limits):
        features = sorted(features)
        wire = store.summary(sid, features)
        summary = self.Q.verify_summary(sid, store.namespace, features, wire)
        plan = self.Q.plan_partitions(summary)[partition]
        req = dict(schema="DMKN_FORMAL_CANDIDATE_REQUEST_V2" if sparse else
            "DMKN_FORMAL_CANDIDATE_REQUEST_V1", namespace=store.namespace,
            snapshot_id=sid, features=features, partition=partition,
            anchor=plan["anchor"], start=start, limits={**PAGE_LIMITS, **limits})
        return summary, req

    def page(self, store, summary, req, *, sparse=True, clock=None):
        check()
        reply = self.C.page(store, req, sparse=sparse, clock=clock)
        verified = self.C.verify_page(summary, req, reply, sparse=sparse, check_budget=check)
        need(verified["verified_scan_coverage"] is False and
             verified["global_complete"] is False and verified["mathematical_acceptance"] is False,
             "SPARSE_CONTROL_POSITIVE_NOT_AUTHORITY")
        need(len(self.F.compact(reply)) <= req["limits"]["bytes"], "SPARSE_CONTROL_ENVELOPE_BOUND")
        return reply, verified

    def run(self):
        plain = self.store("plain")
        pair = self.store("pair", access=config())
        first = [synthetic("A0", [ATOM_A, ATOM_C]), synthetic("A1", [ATOM_A, ATOM_C]),
                 synthetic("B0", [ATOM_B, ATOM_C]), synthetic("B1", [ATOM_B, ATOM_C]),
                 synthetic("AB0", [ATOM_A, ATOM_B])]
        admissions = []
        for value in first:
            p, s = self.admit(plain, value), self.admit(pair, value)
            for key in ("record", "record_id", "snapshot_id"):
                need(p[key] == s[key], "SPARSE_CONTROL_ATOMIC_IDENTITY:"+key)
            need(plain.snapshot() == pair.snapshot(), "SPARSE_CONTROL_SNAPSHOT_IDENTITY")
            admissions.append(s)
        sid = admissions[-1]["snapshot_id"]
        summary, req = self.query(pair, sid, [ATOM_A, ATOM_B], scanned=1, matches=1)
        need(plain.summary(sid, [ATOM_A, ATOM_B]) == pair.summary(sid, [ATOM_A, ATOM_B]),
             "SPARSE_CONTROL_SUMMARY_IDENTITY")
        pair_meta = pair.db.execute("SELECT completed_seq,oriented_rows FROM access_meta WHERE id=1").fetchone()
        need(pair_meta == (5, 6), "SPARSE_CONTROL_BOTH_ORIENTATIONS")
        rows = pair.db.execute("SELECT anchor,companion,partition,anchor_ordinal,companion_ordinal,object_id,admitted_seq FROM access_rows").fetchall()
        expected_bytes = len(self.F.compact(config())) + sum(len(self.F.compact(row)) for row in rows)
        actual_bytes = pair.db.execute("SELECT logical_bytes FROM access_meta WHERE id=1").fetchone()[0]
        need(actual_bytes == expected_bytes and pair.status()["logical"]-plain.status()["logical"] == expected_bytes,
             "SPARSE_CONTROL_ACCESS_BYTES_SINGLE_GLOBAL_CHARGE")
        before = logical_state(pair)
        duplicate = self.admit(pair, first[-1])
        need(duplicate["new"] is False and logical_state(pair) == before,
             "SPARSE_CONTROL_DUPLICATE_NOOP")
        passed("real-store-common-prefix-identities-and-duplicate-noop")

        pair.close(); pair = self.store("pair", access=config(), create=False)
        need(logical_state(pair) == before, "SPARSE_CONTROL_REOPEN_STATE")
        pair.close()
        for changed in (None, config(rows=255), config([[ATOM_A, ATOM_B]])):
            refuses(lambda changed=changed: self.store("pair", access=changed, create=False))
        pair = self.store("pair", access=config(), create=False)
        plain.close()
        refuses(lambda: self.store("plain", access=config(), create=False))
        plain = self.store("plain", create=False)
        bad_configs = [config([[ATOM_B, ATOM_A]]), config([[ATOM_A, ATOM_A]]),
            config([[ATOM_A, ATOM_B], [ATOM_A, ATOM_B]]), config(rows=True),
            config(logical=1023), config([]),
            config([[f"{i:064x}", f"{i+1:064x}"] for i in range(1, 10)])]
        for bad in bad_configs:
            refuses(lambda bad=bad: self.PA.validate_config(bad))
        original = config(); detached = self.PA.validate_config(original)
        original["limits"]["max_rows"] = 1; original["pairs"].clear()
        need(detached == config(), "SPARSE_CONTROL_CONFIG_DETACHED")
        alias_config = config(rows=1)
        alias = self.store("persisted-alias", access=alias_config)
        persisted = self.F.strict(bytes(alias.db.execute("SELECT cfg FROM meta WHERE id=1").fetchone()[0]), 16384)
        persisted["access_pairs"]["limits"]["max_rows"] = True
        alias.db.execute("UPDATE meta SET cfg=? WHERE id=1", (self.F.compact(persisted),))
        refuses(lambda: self.PA.open_config(alias, alias_config), expected="ACCESS_LIMIT:max_rows")
        alias.close()
        refuses(lambda: self.store("persisted-alias", access=alias_config, create=False),
                expected="ACCESS_LIMIT:max_rows")
        passed("exact-reopen-no-migration-and-strict-detached-config")

        s1, r1 = self.query(plain, sid, [ATOM_A, ATOM_B], sparse=False, scanned=2, matches=1)
        miss, _ = self.page(plain, s1, r1, sparse=False)
        need(miss["hits"] == [] and miss["charged"]["scanned"] == 2,
             "SPARSE_CONTROL_V1_TWO_MISSES")
        s3, r3 = self.query(plain, sid, [ATOM_A, ATOM_B], sparse=False, scanned=3, matches=1)
        full, _ = self.page(plain, s3, r3, sparse=False)
        statements = []
        pair.db.set_trace_callback(statements.append)
        try:
            with patch.object(self.PA, "next_row", wraps=self.PA.next_row) as seeks:
                sparse, verified = self.page(pair, summary, req)
            need(seeks.call_count == 1, "SPARSE_CONTROL_ONE_ACTUAL_DRIVER_SEEK")
        finally: pair.db.set_trace_callback(None)
        need(sparse["hits"] == full["hits"] and len(sparse["hits"]) == 1 and
             sparse["hits"][0]["ordinal"] == 2 and sparse["next"] == 3,
             "SPARSE_CONTROL_SAME_ORIGINAL_PROOF")
        need((full["charged"]["scanned"], sparse["charged"]["scanned"],
              sparse["charged"]["record_loads"], sparse["charged"]["proofs"]) == (3, 1, 1, 1),
             "SPARSE_CONTROL_THREE_VERSUS_ONE")
        need(sparse["access_used"] == dict(kind="pair", companion=ATOM_B),
             "SPARSE_CONTROL_PAIR_PLAN")
        access_sql = [sql for sql in statements if sql.lstrip().upper().startswith("SELECT") and
                      "FROM ACCESS_ROWS" in sql.upper() and "LIMIT 0" not in sql.upper()]
        need(len(access_sql) == 1, "SPARSE_CONTROL_ONLY_ONE_ACCESS_SELECT")
        plan = pair.db.execute("EXPLAIN QUERY PLAN "+access_sql[0]).fetchall()
        detail = " ".join(str(row[-1]).upper() for row in plan)
        need("SEARCH ACCESS_ROWS" in detail and "TEMP B-TREE" not in detail and
             "ANCHOR_ORDINAL" in access_sql[0].upper() and "LIMIT 1" in access_sql[0].upper(),
             "SPARSE_CONTROL_INDEXED_BOUNDED_DRIVER")
        passed("one-versus-three-same-proof-actual-indexed-seek", atomic=full["charged"],
               sparse=sparse["charged"], original_ordinal=2, query_plan=detail)

        for value in (synthetic("A-later", [ATOM_A]), synthetic("AB1", [ATOM_A, ATOM_B])):
            p, s = self.admit(plain, value), self.admit(pair, value)
            need((p["record_id"], p["snapshot_id"]) == (s["record_id"], s["snapshot_id"]),
                 "SPARSE_CONTROL_LATER_IDENTITY")
        sid2 = s["snapshot_id"]
        current_summary, current_req = self.query(pair, sid2, [ATOM_A, ATOM_B])
        current, _ = self.page(pair, current_summary, current_req)
        need(current_req["anchor"] == ATOM_B and current["access_used"] ==
             dict(kind="pair", companion=ATOM_A) and [r["ordinal"] for r in current["hits"]] == [2, 3],
             "SPARSE_CONTROL_OPPOSITE_ANCHOR")
        old, _ = self.page(pair, summary, req)
        need(old["hits"] == sparse["hits"], "SPARSE_CONTROL_OLD_CUT")
        extra_summary, extra_req = self.query(pair, sid, [ATOM_A, ATOM_B, ATOM_C], scanned=1)
        extra, _ = self.page(pair, extra_summary, extra_req)
        need(extra_req["anchor"] == ATOM_A and extra["hits"] == [] and
             extra["charged"]["scanned"] == 1 and extra["charged"]["proofs"] == 0,
             "SPARSE_CONTROL_EXTRA_CONJUNCT_REJECTION")
        passed("old-cut-opposite-anchor-and-all-query-conjuncts")

        for target, features, start in ((plain, [ATOM_A, ATOM_B], 0),
                (pair, [ATOM_B, ATOM_C], 0), (pair, [ATOM_A, ATOM_B, ATOM_D], 0)):
            fs, fr = self.query(target, sid, features, start=start, scanned=2)
            before = logical_state(target)
            fallback, _ = self.page(target, fs, fr)
            need(fallback["access_used"] == dict(kind="atomic") and logical_state(target) == before,
                 "SPARSE_CONTROL_SAME_REQUEST_ATOMIC_FALLBACK")
        empty_summary, empty_req = self.query(pair, sid, [ATOM_A, ATOM_C], start=2, scanned=1)
        empty, _ = self.page(pair, empty_summary, empty_req)
        need(empty["hits"] == [] and empty["next"] == 3 and empty["charged"]["scanned"] == 1 and
             empty["charged"]["record_probes"] >= 1,
             "SPARSE_CONTROL_EMPTY_SEEK_CHARGED")
        passed("disabled-ineligible-and-third-anchor-fallback-empty-seek")

        self.corruption(pair, summary, req)
        self.tampering(pair, summary, req, sparse, current_summary, current_req, current)
        self.meters(pair, summary, req)
        self.transactions()
        self.ordinary()
        self.sessions(pair, sid, summary, req, empty_summary, empty_req)
        return dict(old_snapshot=sid, new_snapshot=sid2,
            fixture_authority="UNPROVED_GENERIC_AND_ORDINARY_METADATA",
            fixture_count=len(self.fixtures), native_calls=0, socket_calls=0)

    def corruption(self, store, summary, req):
        before = logical_state(store)
        mutations = [
            ("watermark", "UPDATE access_meta SET completed_seq=0 WHERE id=1", ()),
            ("old-companion", "UPDATE access_rows SET companion_ordinal=999 WHERE anchor=? AND companion=? AND anchor_ordinal=2",
             (ATOM_A, ATOM_B)),
            ("old-sequence", "UPDATE access_rows SET admitted_seq=999 WHERE anchor=? AND companion=? AND anchor_ordinal=2",
             (ATOM_A, ATOM_B)),
            ("missing-table", "DROP TABLE access_rows", ())]
        reasons = {}
        for label, sql, params in mutations:
            store.db.execute("BEGIN IMMEDIATE")
            try:
                store.db.execute(sql, params)
                reasons[label] = refuses(lambda: self.C.page(store, req, sparse=True), database=True)
            finally:
                if store.db.in_transaction: store.db.execute("ROLLBACK")
            need(logical_state(store) == before, "SPARSE_CONTROL_FAULT_RESTORED")
        good, _ = self.page(store, summary, req)
        need(len(good["hits"]) == 1, "SPARSE_CONTROL_AFTER_CORRUPTION")
        passed("enabled-corruption-refuses-not-fallback", reasons=reasons)

    def tampering(self, store, summary, req, good, current_summary, current_req, current):
        edits = []
        for key, value in (("global_complete", True), ("mathematical_acceptance", True),
                ("coverage", "COMPLETE"), ("namespace", "e"*64), ("snapshot_id", "e"*64),
                ("partition", 8), ("anchor", ATOM_B), ("next", 0), ("anchor_count", 99),
                ("schema", "DMKN_FORMAL_CANDIDATE_PAGE_V1"), ("access_used", None),
                ("access_used", dict(kind="pair", companion=ATOM_A)),
                ("access_used", dict(kind="pair", companion=ATOM_D)),
                ("access_used", dict(kind="atomic", extra=True))):
            bad = deepcopy(good); bad[key] = value; edits.append(bad)
        for kind in ("ordinal", "proof", "hash", "feature", "object", "counter"):
            bad = deepcopy(good); hit = bad["hits"][0]
            if kind == "ordinal": hit["ordinal"] = 0
            elif kind == "proof": hit["siblings"][0] = "e"*64
            elif kind == "hash": hit["record"]["object_sha256"] = "e"*64
            elif kind == "feature": hit["record"]["features"].remove(ATOM_B)
            elif kind == "object": hit["record"]["object_id"] = "08"+"e"*62
            else: bad["charged"]["scanned"] = 0
            edits.append(bad)
        for bad in edits:
            refuses(lambda bad=bad: self.C.verify_page(summary, req, bad, sparse=True))
        for kind in ("duplicate", "order"):
            bad = deepcopy(current)
            bad["hits"] = [bad["hits"][0], deepcopy(bad["hits"][0])] if kind == "duplicate" else list(reversed(bad["hits"]))
            refuses(lambda bad=bad: self.C.verify_page(current_summary, current_req, bad, sparse=True))
        cursor_summary, cursor_req = self.query(store, req["snapshot_id"],
                                                [ATOM_A, ATOM_C], scanned=1, matches=1)
        partial, _ = self.page(store, cursor_summary, cursor_req)
        need(partial["next_cursor"] is not None and partial["next_cursor"]["next"] == 1,
             "SPARSE_CONTROL_NONTERMINAL_ONE_CURSOR")
        alias = deepcopy(partial); alias["next_cursor"]["next"] = True
        refuses(lambda: self.C.verify_page(cursor_summary, cursor_req, alias, sparse=True),
                expected="CANDIDATE_CURSOR_NEXT")
        for mode in (1, None, "sparse-v2"):
            refuses(lambda mode=mode: self.C.validate_request(req, sparse=mode))
            refuses(lambda mode=mode: self.C.page(store, req, sparse=mode))
            refuses(lambda mode=mode: self.C.verify_page(summary, req, good, sparse=mode))
        # Use a genuinely V1-shaped envelope: refusal must not merely be schema mismatch.
        old_req, old_reply = deepcopy(req), deepcopy(good)
        old_req["schema"] = "DMKN_FORMAL_CANDIDATE_REQUEST_V1"
        old_reply["schema"] = "DMKN_FORMAL_CANDIDATE_PAGE_V1"
        del old_reply["access_used"]
        if old_reply["next_cursor"] is not None:
            old_reply["next_cursor"]["schema"] = "DMKN_FORMAL_CANDIDATE_CURSOR_V1"
        refuses(lambda: self.C.verify_page(summary, old_req, old_reply),
                expected="CANDIDATE_REPORTED_SCAN_BOUND")
        passed("positive-proof-binding-mode-shape-and-v1-distance-tampering", mutated_replies=len(edits)+2)

    def meters(self, store, summary, req):
        before = logical_state(store)
        store.db.execute("PRAGMA busy_timeout=73")
        for key, limit in (("sql_vm_steps", 100), ("node_reads", 1),
                           ("hash_calls", 1), ("record_probes", 1)):
            limited = deepcopy(req); limited["limits"][key] = limit
            reply, _ = self.page(store, summary, limited, clock=Clock())
            need(reply["termination"] == key+"_exhausted" and reply["hits"] == [] and
                 reply["next"] <= 2 and reply["charged"][key] <= limit,
                 "SPARSE_CONTROL_METER:"+key)
            if reply["anchor_count"] is None:
                need(reply["access_used"] is None, "SPARSE_CONTROL_UNPLANNED_ACCESS_NULL")
            need(store.db.execute("PRAGMA busy_timeout").fetchone()[0] == 73,
                 "SPARSE_CONTROL_BUSY_RESTORED")
        for kind in ("node", "deadline"):
            clock = Clock(); original = self.C.A.vector_get
            def stop(*args, **kwargs):
                if kind == "node": raise self.C._Stop("node_reads_exhausted")
                value = original(*args, **kwargs); clock.value = 2.0; return value
            with patch.object(self.C.A, "vector_get", side_effect=stop):
                interrupted, _ = self.page(store, summary, req, clock=clock)
            need(interrupted["hits"] == [] and interrupted["next"] <= 2 and
                 interrupted["termination"] == ("node_reads_exhausted" if kind == "node" else "time_exhausted"),
                 "SPARSE_CONTROL_UNFINISHED_NOT_SKIPPED")
            continuation = deepcopy(req); continuation["start"] = interrupted["next"]
            completed, _ = self.page(store, summary, continuation)
            need(len(completed["hits"]) == 1, "SPARSE_CONTROL_UNFINISHED_RESUMES")
        # A recursive SELECT after return would hit an incorrectly retained exhausted callback.
        need(store.db.execute("WITH RECURSIVE r(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM r WHERE n<200) SELECT sum(n) FROM r").fetchone()[0] == 20100,
             "SPARSE_CONTROL_PROGRESS_REMOVED")
        need(logical_state(store) == before, "SPARSE_CONTROL_READ_ONLY_LIMITS")
        passed("sparse-meters-interruption-continuation-and-connection-cleanup")

        large = self.store("large-envelope", access=config([[ATOM_A, ATOM_B]]))
        extra = [f"{i:064x}" for i in range(100, 132)]
        admission = self.admit(large, synthetic("large-preview-metadata", [ATOM_A, ATOM_B, *extra]))
        need(len(self.F.compact(admission["record"])) > 2048, "SPARSE_CONTROL_BYTE_FIXTURE_LARGE_ENOUGH")
        ls, lr = self.query(large, admission["snapshot_id"], [ATOM_A, ATOM_B], scanned=1, bytes=2048)
        small, _ = self.page(large, ls, lr)
        need(small["termination"] == "bytes_exhausted" and small["hits"] == [] and small["next"] == 0,
             "SPARSE_CONTROL_BYTE_CAP_NO_ADVANCE")
        lr["limits"]["bytes"] = 65536
        accepted, _ = self.page(large, ls, lr)
        need(len(accepted["hits"]) == 1, "SPARSE_CONTROL_BYTE_RESUME")
        passed("whole-v2-envelope-byte-cap-preserves-pending-candidate")

    def transactions(self):
        target = self.store("transaction", access=config([[ATOM_A, ATOM_B]]))
        self.admit(target, synthetic("tx-before", [ATOM_A]))
        before = logical_state(target)
        target.db.execute("""CREATE TEMP TRIGGER fail_second BEFORE INSERT ON access_rows
            WHEN (SELECT count(*) FROM access_rows WHERE object_id=NEW.object_id)>=1
            BEGIN SELECT RAISE(ABORT,'SPARSE_CONTROL_SECOND_ORIENTATION'); END""")
        reason = refuses(lambda: self.admit(target, synthetic("tx-pending", [ATOM_A, ATOM_B])), database=True,
                          expected="SPARSE_CONTROL_SECOND_ORIENTATION")
        need(not target.db.in_transaction and logical_state(target) == before and
             target.work["access_inserts"] >= 2, "SPARSE_CONTROL_TRANSACTION_ROLLBACK")
        target.db.execute("DROP TRIGGER fail_second")
        target.close(); target = self.store("transaction", access=config([[ATOM_A, ATOM_B]]), create=False)
        need(logical_state(target) == before, "SPARSE_CONTROL_ROLLBACK_REOPEN")
        success = self.admit(target, synthetic("tx-next-valid", [ATOM_A, ATOM_B]))
        need(success["new"] is True and target.db.execute(
            "SELECT completed_seq,oriented_rows FROM access_meta WHERE id=1").fetchone() == (2, 2),
             "SPARSE_CONTROL_VALID_AFTER_ROLLBACK")
        passed("actual-second-orientation-sql-abort-all-tables-rollback", reason=reason)

        row_store = self.store("row-quota", access=config([[ATOM_A, ATOM_B]], rows=2))
        value = synthetic("row-first", [ATOM_A, ATOM_B])
        self.admit(row_store, value); before = logical_state(row_store)
        row_reason = refuses(lambda: self.admit(row_store, synthetic("row-over", [ATOM_A, ATOM_B])),
                             expected="ACCESS_ROW_CAP")
        need(logical_state(row_store) == before and not row_store.db.in_transaction,
             "SPARSE_CONTROL_ROW_QUOTA_ROLLBACK")
        need(self.admit(row_store, value)["new"] is False and logical_state(row_store) == before,
             "SPARSE_CONTROL_DUPLICATE_AT_CAP")
        # Small legal byte cap; at most six tiny objects suffice to cross it.
        byte_store = self.store("byte-quota", access=config([[ATOM_A, ATOM_B]], logical=1024))
        byte_reason = None
        for i in range(6):
            before = logical_state(byte_store)
            try: self.admit(byte_store, synthetic("byte-"+str(i), [ATOM_A, ATOM_B]))
            except ValueError as error:
                byte_reason = str(error)
                need(logical_state(byte_store) == before and not byte_store.db.in_transaction,
                     "SPARSE_CONTROL_BYTE_QUOTA_ROLLBACK")
                break
        need(byte_reason == "ACCESS_LOGICAL_BYTE_CAP", "SPARSE_CONTROL_BYTE_QUOTA_NOT_REACHED")
        many = self.store("multiple-pairs", access=config())
        result = self.admit(many, synthetic("ABC", [ATOM_A, ATOM_B, ATOM_C]))
        row = many.db.execute("SELECT completed_seq,oriented_rows,logical_bytes FROM access_meta WHERE id=1").fetchone()
        need(row[0:2] == (1, 4) and result["charged"]["access_checks"] == 2 and
             result["charged"]["access_inserts"] == 4 and
             result["charged"]["access_logical_bytes"] > 0,
             "SPARSE_CONTROL_MULTIPLE_PAIR_ACCOUNTING")
        need(many.db.execute("PRAGMA max_page_count").fetchone()[0] == BASE_LIMITS["max_db_pages"],
             "SPARSE_CONTROL_SHARED_PHYSICAL_CAP")
        passed("independent-pair-quotas-duplicate-cap-and-multiple-pair-cost",
               row_refusal=row_reason, byte_refusal=byte_reason, multi_pair=result["charged"])

    def ordinary(self):
        adapter = self.api.OrdinaryExportAdapter(self.api.A.S.semantic_id())
        def name(value): return [[0, {"$bytes": list(value.encode("ascii"))}]]
        bindings = sorted([[name(label), identity("ordinary-symbol-"+label)] for label in ("A", "R")],
                          key=lambda item: raw(item[0]))
        expr = [self.api.A.E.EXPR_FORMAT, [], [[2, name("R"), []], [2, name("A"), []], [3, 0, 1]], 2]
        preview = raw(dict(schema=self.api.PP.SCHEMA, semantic_id=adapter.semantic_id,
            unit_id=identity("ordinary-unproved-unit"), export_name=name("UnprovedSparseClaim"),
            header=[2, [], expr], type_bindings=bindings))
        described = adapter.describe(preview)
        features = self.api.compile_query(adapter.namespace, [dict(tag="type-symbol",
            symbol=dict(kind="portable-symbol", symbol_id=binding[1])) for binding in bindings])
        need(set(features) <= set(described["record"]["features"]) and
             described["mathematical_acceptance"] is False, "SPARSE_CONTROL_ORDINARY_TYPE_SYMBOLS")
        access = config([features])
        plain, pair = self.store("ordinary-plain", adapter=adapter), self.store("ordinary-pair", adapter=adapter, access=access)
        ordinary_results = [self.admit(store, preview) for store in (plain, pair)]
        p, s = ordinary_results
        for key in ("record", "record_id", "snapshot_id"):
            need(p[key] == s[key], "SPARSE_CONTROL_ORDINARY_IDENTITY:"+key)
        need(p["record"] == described["record"] and p["record"]["schema"] == self.F.ORDINARY_EXPORT_RECORD_SCHEMA,
             "SPARSE_CONTROL_REAL_V3_RECORD")
        partition = int(p["record"]["object_id"][:2], 16)
        positives = []
        for store, sparse in ((plain, False), (pair, True)):
            summary, req = self.query(store, p["snapshot_id"], features, sparse=sparse,
                                      partition=partition, scanned=1)
            reply, verified = self.page(store, summary, req, sparse=sparse)
            need(verified["matches"] == [p["record"]], "SPARSE_CONTROL_ORDINARY_RETRIEVAL")
            positives.append(reply["hits"])
        need(positives[0] == positives[1], "SPARSE_CONTROL_ORDINARY_PROOF_UNCHANGED")
        resolved = adapter.resolve(p["record"], preview)
        need(resolved["mathematical_acceptance"] is False and
             resolved["next_gate"] == "ACQUIRE_EXACT_PORTABLE_ORDINARY_EVIDENCE",
             "SPARSE_CONTROL_ORDINARY_NOT_ACCEPTANCE")
        passed("actual-ordinary-preview-adapter-store-query-identity", namespace=adapter.namespace,
               export_id=p["record"]["object_id"], record_id=p["record_id"], partition=partition)

    def sessions(self, store, sid, summary, req, empty_summary, empty_req):
        def session(features):
            clock = Clock()
            limits = dict(providers=1, snapshots=1, requests=8, pages=4, examined=2,
                          candidates=16, bytes=4*MIB, wall_ms=60000, inflight=1)
            s = self.api.SearchSession(store.namespace, features, limits, clock=clock)
            ticket = s.begin_summary("provider", sid)
            accepted = s.accept(ticket["ticket"], self.F.compact(store.summary(sid, features)))
            need(accepted["status"] == "VERIFIED_SUMMARY", "SPARSE_CONTROL_SESSION_REAL_SUMMARY")
            return s
        for mode, outcome in (("sparse-v2", "success"), ("sparse-v2", "malformed"),
                ("sparse-v2", "proof"), ("sparse-v2", "wrong-version"),
                ("sparse-v2", "abandon"), ("atomic-v1", "wrong-version")):
            s = session(req["features"])
            before_coverage = s.coverage[sid].report()
            ticket = s.begin_candidates("provider", sid, PARTITION, 0,
                                        deepcopy(req["limits"]), mode=mode)
            need(ticket["operation"] == "candidates" and s.reserved["examined"] == 1,
                 "SPARSE_CONTROL_SESSION_ORIGINAL_RESERVATION")
            response = self.C.page(store, ticket["request"], sparse=(mode == "sparse-v2"))
            if outcome == "abandon":
                s.abandon(ticket["ticket"])
            else:
                if outcome == "proof": response["hits"][0]["siblings"][0] = "e"*64
                if outcome == "wrong-version":
                    other = deepcopy(ticket["request"])
                    other_sparse = mode != "sparse-v2"
                    other["schema"] = "DMKN_FORMAL_CANDIDATE_REQUEST_V2" if other_sparse else "DMKN_FORMAL_CANDIDATE_REQUEST_V1"
                    response = self.C.page(store, other, sparse=other_sparse)
                payload = b"{}" if outcome == "malformed" else self.F.compact(response)
                if outcome == "success":
                    result = s.accept(ticket["ticket"], payload)
                    need(len(result["matches"]) == 1, "SPARSE_CONTROL_SESSION_SUCCESS")
                else:
                    refuses(lambda: s.accept(ticket["ticket"], payload))
            need(not s.pending and not any(s.reserved.values()) and s.used["examined"] == 1 and
                 s.candidate_scan_charges == 1 and s.coverage[sid].report() == before_coverage,
                 "SPARSE_CONTROL_SETTLED_ONCE_NO_COVERAGE")
            need(len(s.seen_candidates) == (1 if outcome == "success" else 0),
                 "SPARSE_CONTROL_SESSION_NO_PARTIAL_ACCEPT")
            used = deepcopy(s.used)
            refuses(lambda: s.abandon(ticket["ticket"]))
            need(s.used == used, "SPARSE_CONTROL_NO_DOUBLE_SETTLEMENT")
            too_large = {**req["limits"], "scanned": 2}
            refuses(lambda: s.begin_candidates("provider", sid, PARTITION, 0, too_large, mode=mode))
            need(s.used == used and not s.pending, "SPARSE_CONTROL_NO_RENEWED_ALLOWANCE")
        # A lying zero-work report for a no-hit page still consumes the full grant.
        s = session(empty_req["features"])
        ticket = s.begin_candidates("provider", sid, PARTITION, 2, deepcopy(empty_req["limits"]), mode="sparse-v2")
        response = self.C.page(store, ticket["request"], sparse=True)
        response["charged"] = {key: 0 for key in response["charged"]}
        s.accept(ticket["ticket"], self.F.compact(response))
        need(s.used["examined"] == 1 and s.candidate_scan_charges == 1,
             "SPARSE_CONTROL_PROVIDER_ZERO_NO_REFUND")
        default = session(req["features"])
        ticket = default.begin_candidates("provider", sid, PARTITION, 0, deepcopy(req["limits"]))
        need(ticket["request"]["schema"] == "DMKN_FORMAL_CANDIDATE_REQUEST_V1",
             "SPARSE_CONTROL_DEFAULT_V1")
        default.abandon(ticket["ticket"])
        passed("held-schema-default-v1-settlement-failure-and-no-counter-refunds")


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "SPARSE_CONTROL_ISOLATED_PROCESS")
    need(output.is_absolute() and output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         output.parent.is_dir() and output.parent.resolve(strict=True) == output.parent and
         not os.path.lexists(output), "SPARSE_CONTROL_FRESH_OUTPUT")
    for selected in (args.package, args.python_runtime, args.lean_runtime):
        path = Path(selected)
        need(path.is_absolute() and not output.is_relative_to(path) and not path.is_relative_to(output),
             "SPARSE_CONTROL_PROTECTED_OUTPUT")
    output.mkdir()
    report = dict(passed=False, cases=CASES, profile_sha256=args.profile_sha256,
        authority="NATIVE_FREE_REAL_STORE_QUERY_SESSION_UNPROVED_METADATA_NOT_MATHEMATICS_OR_NETWORK")
    suite = None
    try:
        with ExitStack() as guard:
            for name in ("subprocess.Popen", "socket.socket", "socket.create_connection", "os.system", "os.startfile"):
                guard.enter_context(patch(name, forbidden))
            loaded = load_package(args)
            suite = Suite(loaded, output)
            report["detail"] = suite.run()
            save(output/"FIXTURES.json", suite.fixtures)
            suite.close(); suite = None
        report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:1000])
    finally:
        if suite is not None:
            if not (output/"FIXTURES.json").exists():
                try: save(output/"FIXTURES.json", suite.fixtures)
                except BaseException as error:
                    report["fixture_save_error"] = type(error).__name__+":"+str(error)[:1000]
            try: suite.close()
            except BaseException as error:
                report["cleanup_error"] = type(error).__name__+":"+str(error)[:1000]
                report["passed"] = False
    report.update(wall_seconds=time.monotonic()-START, harness_cpu_seconds=time.process_time()-CPU,
                  completed_groups=len(CASES))
    save(output/"RESULT.json", report)
    print(raw(report).decode("ascii"))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

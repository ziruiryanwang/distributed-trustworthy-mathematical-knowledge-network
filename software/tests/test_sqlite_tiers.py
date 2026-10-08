"""Synthetic SQLite page-tier falsification controls; no product imports.

Root owns a separately supervised execution. All fixtures and observations are
retained under an explicit fresh DTMKN_TEST_ROOT outside the installation.
This file does not implement ControlStore, native acceptance or renewal.
"""
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
import sys
import unittest

MIB = 1048576
PAGE = 4096
BASE, ORDINARY, TERMINAL, ADMISSION = 8192, 6144, 7168, 4096
RETAINED_BYTES = 256 * MIB
MAX_LARGE_WRITES, MAX_ATTEMPTED_PAYLOAD = 64, 96 * MIB
INSTALL = Path(__file__).absolute().parents[1]
SCHEMA = """
CREATE TABLE state (
 id INTEGER PRIMARY KEY CHECK(id=1),
 used_requests INTEGER NOT NULL CHECK(typeof(used_requests)='integer' AND used_requests>=0),
 used_stages INTEGER NOT NULL CHECK(typeof(used_stages)='integer' AND used_stages>=0),
 used_bytes INTEGER NOT NULL CHECK(typeof(used_bytes)='integer' AND used_bytes>=0),
 auth_requests INTEGER NOT NULL CHECK(typeof(auth_requests)='integer' AND auth_requests BETWEEN 1 AND 4096),
 auth_stages INTEGER NOT NULL CHECK(typeof(auth_stages)='integer' AND auth_stages BETWEEN 1 AND 256),
 auth_bytes INTEGER NOT NULL CHECK(typeof(auth_bytes)='integer' AND auth_bytes BETWEEN 0 AND 68719476736),
 cap INTEGER NOT NULL CHECK(typeof(cap)='integer' AND cap IN (8192,16384,32768,65536)),
 grants INTEGER NOT NULL CHECK(typeof(grants)='integer' AND grants BETWEEN 0 AND 64),
 active TEXT,
 CHECK(used_requests<=auth_requests AND used_stages<=auth_stages AND used_bytes<=auth_bytes)
);
CREATE TABLE requests (
 id TEXT PRIMARY KEY, raw BLOB NOT NULL CHECK(typeof(raw)='blob' AND length(raw)<=4096),
 phase TEXT NOT NULL CHECK(phase IN ('pending','terminal')),
 response BLOB CHECK((phase='pending' AND response IS NULL) OR
   (phase='terminal' AND typeof(response)='blob' AND length(response)<=1048576))
);
CREATE TABLE filler (id INTEGER PRIMARY KEY, payload BLOB NOT NULL
 CHECK(typeof(payload)='blob' AND length(payload)<=2097152));
CREATE TABLE visible (
 id TEXT PRIMARY KEY, sort_key TEXT NOT NULL,
 kind TEXT NOT NULL CHECK(kind='synthetic-unpromoted'),
 payload BLOB NOT NULL CHECK(typeof(payload)='blob' AND length(payload)<=2097152)
);
CREATE UNIQUE INDEX visible_sort ON visible(sort_key);
CREATE TABLE owner_grants (
 id TEXT PRIMARY KEY, seq INTEGER UNIQUE NOT NULL
 CHECK(typeof(seq)='integer' AND seq BETWEEN 1 AND 64),
 raw BLOB NOT NULL CHECK(typeof(raw)='blob' AND length(raw)<=4096),
 response BLOB NOT NULL CHECK(typeof(response)='blob' AND length(response)<=4096)
);
"""


def require(value, code):
    if not value:
        raise RuntimeError(code)


def checked(path):
    path = Path(path)
    require(path.is_absolute(), "ABSOLUTE_FIXTURE_ROOT")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        require(not stat.S_ISLNK(info.st_mode)
                and not getattr(info, "st_file_attributes", 0) & 0x400, "FIXTURE_REPARSE_POINT")
    return path.resolve(strict=True)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def save(path, value):
    raw = encode(value)
    require(len(raw) <= MIB, "OBSERVATION_BYTE_LIMIT")
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(MIB), b""):
            h.update(chunk)
    return h.hexdigest()


def response_bytes(size):
    prefix = b'{"synthetic":true,"status":"REFUSED","padding":"'
    suffix = b'"}\n'
    require(size >= len(prefix) + len(suffix), "SYNTHETIC_RESPONSE_SIZE")
    return prefix + b"x" * (size - len(prefix) - len(suffix)) + suffix


def compact(value):
    if type(value) is bytes:
        return {"bytes": len(value), "sha256": hashlib.sha256(value).hexdigest()}
    return value


class SQLiteTierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        require(sys.dont_write_bytecode and sys.flags.ignore_environment
                and sys.flags.no_user_site and sys.flags.no_site, "PYTHON_B_E_s_S_REQUIRED")
        require(sqlite3.sqlite_version == "3.50.4", "EXACT_SQLITE_3_50_4_REQUIRED")
        parent = os.environ.get("DTMKN_TEST_ROOT")
        require(type(parent) is str and parent, "EXPLICIT_TEST_ROOT_REQUIRED")
        parent = checked(parent)
        require(parent.is_dir() and not parent.is_relative_to(INSTALL)
                and not INSTALL.is_relative_to(parent), "TEST_ROOT_MUST_NOT_OVERLAP_INSTALL")
        cls.suite_root = parent / "sqlite-tiers"
        cls.suite_root.mkdir(exist_ok=False)
        cls.large_writes, cls.attempted_payload = 0, 0
        save(cls.suite_root / "scope.json", {"schema": 1, "synthetic_storage_only": True,
            "native_acceptance": False, "renewal_qualification": False,
            "sqlite_version": sqlite3.sqlite_version, "methods": 5,
            "max_large_write_attempts": MAX_LARGE_WRITES,
            "max_attempted_large_payload_bytes": MAX_ATTEMPTED_PAYLOAD,
            "retained_byte_bound": RETAINED_BYTES,
            "peak_scope": "sampled page/journal/retained observations, not hard transient quotas"})

    def setUp(self):
        self.root = self.suite_root / self._testMethodName
        self.root.mkdir(exist_ok=False)
        self.path = self.root / "synthetic.sqlite3"
        self.connections, self.observations = [], []
        self.vm_steps = 0
        self.peak_pages = self.peak_journal = self.peak_retained = 0
        self.notes = {}

    def retained(self):
        total, count, pending = 0, 0, [self.suite_root]
        while pending:
            for path in pending.pop().iterdir():
                count += 1
                require(count <= 128, "RETAINED_ENTRY_BOUND")
                path = checked(path)
                if path.is_dir():
                    pending.append(path)
                else:
                    require(path.is_file(), "RETAINED_REGULAR_FILE")
                    total += path.stat().st_size
                    require(total <= RETAINED_BYTES, "RETAINED_256_MIB_BOUND")
        self.peak_retained = max(self.peak_retained, total)
        return total

    def journal_sample(self):
        path = Path(str(self.path) + "-journal")
        size = path.stat().st_size if path.exists() else 0
        self.peak_journal = max(self.peak_journal, size)
        return size

    def progress(self):
        self.vm_steps += 100
        self.journal_sample()
        return 1 if self.vm_steps > 500000 else 0

    def connect(self, readonly=False):
        db = sqlite3.connect(self.path.as_uri() + ("?mode=ro" if readonly else "?mode=rw"),
                             uri=True, isolation_level=None, timeout=0)
        self.connections.append(db)
        db.set_progress_handler(self.progress, 100)
        db.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 3 * MIB)
        if readonly:
            db.execute("PRAGMA query_only=ON")
        else:
            db.execute("PRAGMA synchronous=FULL")
            db.execute("PRAGMA temp_store=MEMORY")
        return db

    def fresh(self, pending=False):
        # Exclusive file creation precedes mode=rw; an existing fixture is never reused.
        with self.path.open("xb"):
            pass
        db = self.connect()
        db.execute("PRAGMA page_size=4096")
        self.assertEqual(db.execute("PRAGMA journal_mode=DELETE").fetchone()[0], "delete")
        self.assertEqual(db.execute("PRAGMA synchronous").fetchone()[0], 2)
        self.assertEqual(db.execute("PRAGMA temp_store").fetchone()[0], 2)
        self.assertEqual(db.execute("PRAGMA max_page_count=8192").fetchone()[0], BASE)
        db.executescript("BEGIN IMMEDIATE;" + SCHEMA + "COMMIT;")
        db.execute("BEGIN IMMEDIATE")
        db.execute("INSERT INTO state VALUES(1,?,0,?,128,16,4294967296,8192,0,?)",
                   (2 if pending else 1, (2 if pending else 1) * 8 * MIB,
                    "pending" if pending else None))
        db.execute("INSERT INTO requests VALUES('old',?,'terminal',?)",
                   (b"synthetic-old-request", response_bytes(128)))
        if pending:
            db.execute("INSERT INTO requests VALUES('pending',?,'pending',NULL)",
                       (b"synthetic-pending-request",))
        db.execute("COMMIT")
        self.assertEqual(db.execute("PRAGMA page_size").fetchone()[0], PAGE)
        self.observe(db, "fresh")
        return db

    def observe(self, db, label):
        require(len(self.observations) < 256, "OBSERVATION_COUNT_BOUND")
        pages = db.execute("PRAGMA page_count").fetchone()[0]
        self.peak_pages = max(self.peak_pages, pages)
        self.observations.append({"label": label, "pages": pages,
            "freelist": db.execute("PRAGMA freelist_count").fetchone()[0],
            "connection_cap": db.execute("PRAGMA max_page_count").fetchone()[0],
            "in_transaction": db.in_transaction, "journal_bytes": self.journal_sample(),
            "database_bytes": self.path.stat().st_size, "suite_retained_bytes": self.retained()})

    def large_write(self, db, sql, parameters, size):
        require(65536 <= size <= 2 * MIB, "LARGE_PAYLOAD_PROFILE")
        type(self).large_writes += 1
        type(self).attempted_payload += size
        require(self.large_writes <= MAX_LARGE_WRITES
                and self.attempted_payload <= MAX_ATTEMPTED_PAYLOAD, "LARGE_WRITE_ALLOCATION")
        return db.execute(sql, parameters)

    def fill(self, db, sizes):
        self.assertEqual(db.execute("PRAGMA max_page_count=6144").fetchone()[0], ORDINARY)
        for index, size in enumerate(sizes):
            db.execute("BEGIN IMMEDIATE")
            self.large_write(db, "INSERT INTO filler(payload) VALUES(zeroblob(?))", (size,), size)
            self.observe(db, "filler-" + str(index) + "-uncommitted")
            db.execute("COMMIT")
        self.observe(db, "filler-committed")

    def logical(self, db):
        result = {}
        for table, order in (("state", "id"), ("requests", "id"), ("filler", "id"),
                             ("visible", "id"), ("owner_grants", "seq")):
            rows = []
            for row in db.execute("SELECT * FROM " + table + " ORDER BY " + order):
                require(len(rows) < 128, "SYNTHETIC_ROW_BOUND")
                rows.append([compact(value) for value in row])
            result[table] = rows
        return result

    def grants64(self, db):
        self.assertIsNone(db.execute("SELECT active FROM state").fetchone()[0])
        self.assertEqual(db.execute("PRAGMA max_page_count=8192").fetchone()[0], BASE)
        db.execute("BEGIN IMMEDIATE")
        db.executemany("INSERT INTO owner_grants VALUES(?,?,?,?)",
                       [("grant-" + str(i), i, b"G" * 4096, b"R" * 4096) for i in range(1, 65)])
        db.execute("UPDATE state SET grants=64")
        self.observe(db, "64-grants-uncommitted")
        db.execute("COMMIT")
        self.assertEqual(db.execute("SELECT count(*),sum(length(raw)+length(response)) FROM owner_grants").fetchone(),
                         (64, 64 * 8192))

    def status_without_changes(self, writable):
        writable.close()
        self.connections.remove(writable)
        for suffix in ("-journal", "-wal", "-shm"):
            path = Path(str(self.path) + suffix)
            self.assertTrue(not path.exists() or path.stat().st_size == 0, "NONEMPTY_SIDECAR")
        before = {path.name: (path.stat().st_size, digest(path)) for path in self.root.iterdir() if path.is_file()}
        db = self.connect(readonly=True)
        self.assertEqual(db.execute("PRAGMA query_only").fetchone()[0], 1)
        status = {"state": db.execute("SELECT * FROM state WHERE id=1").fetchone(),
                  "pages": db.execute("PRAGMA page_count").fetchone()[0],
                  "freelist": db.execute("PRAGMA freelist_count").fetchone()[0],
                  "requests": db.execute("SELECT count(*) FROM requests").fetchone()[0],
                  "grants": db.execute("SELECT count(*) FROM owner_grants").fetchone()[0]}
        with self.assertRaises(sqlite3.OperationalError) as error:
            db.execute("UPDATE state SET active=NULL")
        self.assertEqual(error.exception.sqlite_errorcode & 255, sqlite3.SQLITE_READONLY)
        db.close()
        self.connections.remove(db)
        after = {path.name: (path.stat().st_size, digest(path)) for path in self.root.iterdir() if path.is_file()}
        self.assertEqual(before, after, "QUERY_ONLY_STATUS_CHANGED_FILES")
        self.notes["readonly_status"] = status
        self.notes["status_files_before"] = before
        self.notes["status_files_after"] = after

    def test_admin_highwater_cannot_lower_cap_and_replay_remains_readable(self):
        db = self.fresh(pending=True)
        self.fill(db, [2 * MIB] * 11 + [MIB])
        large_response = response_bytes(MIB - 64)
        self.assertEqual(db.execute("PRAGMA max_page_count=7168").fetchone()[0], TERMINAL)
        db.execute("BEGIN IMMEDIATE")
        self.large_write(db, "UPDATE requests SET phase='terminal',response=? WHERE id='pending'",
                         (large_response,), len(large_response))
        db.execute("UPDATE state SET active=NULL")
        self.observe(db, "terminal-response-uncommitted")
        db.execute("COMMIT")
        self.grants64(db)
        pages = db.execute("PRAGMA page_count").fetchone()[0]
        self.assertGreater(pages, ORDINARY)
        self.assertLessEqual(pages, BASE)
        attempted = db.execute("PRAGMA max_page_count=6144").fetchone()[0]
        self.assertEqual(attempted, pages, "SQLITE_CANNOT_LOWER_BELOW_ALLOCATED_PAGES")
        self.observe(db, "lowering-returned-current-pages")
        db.close()
        self.connections.remove(db)
        db = self.connect()
        durable = db.execute("SELECT cap FROM state").fetchone()[0]
        self.assertEqual(durable, BASE)
        self.assertEqual(db.execute("PRAGMA max_page_count=" + str(durable)).fetchone()[0], BASE)
        replay_before = self.logical(db)
        self.assertTrue(db.execute("SELECT response FROM requests WHERE id='pending' AND raw=?",
                                   (b"synthetic-pending-request",)).fetchone()[0] == large_response)
        self.assertEqual(db.execute("SELECT response FROM owner_grants WHERE id='grant-64' AND raw=?",
                                    (b"G" * 4096,)).fetchone()[0], b"R" * 4096)
        self.assertEqual(replay_before, self.logical(db))
        self.notes["cap_lowering"] = {"requested": ORDINARY, "returned": attempted, "actual_pages": pages}
        self.status_without_changes(db)

    def test_real_full_rolls_back_visibility_then_small_terminal_only_refusal(self):
        db = self.fresh(pending=True)
        self.fill(db, [2 * MIB] * 11)
        before = self.logical(db)
        db.execute("BEGIN IMMEDIATE")
        db.execute("INSERT INTO visible VALUES('uncommitted','first','synthetic-unpromoted',X'00')")
        large_response = response_bytes(MIB - 64)
        self.large_write(db, "UPDATE requests SET phase='terminal',response=? WHERE id='pending'",
                         (large_response,), len(large_response))
        db.execute("UPDATE state SET active=NULL")
        self.observe(db, "visibility-prefix-uncommitted")
        with self.assertRaises(sqlite3.OperationalError) as error:
            self.large_write(db, "INSERT INTO visible VALUES('too-large','second','synthetic-unpromoted',zeroblob(?))",
                             (2 * MIB - 64,), 2 * MIB - 64)
        code = error.exception.sqlite_errorcode
        self.assertEqual(code & 255, sqlite3.SQLITE_FULL, "REQUIRE_REAL_SQLITE_FULL")
        self.notes["full"] = {"sqlite_errorcode": code, "sqlite_errorname": error.exception.sqlite_errorname,
                              "in_transaction_immediately_after_error": db.in_transaction}
        self.journal_sample()
        db.rollback()  # Safe whether SQLite already rolled the whole transaction back or not.
        self.assertFalse(db.in_transaction)
        self.assertEqual(before, self.logical(db), "COMMITTED_PENDING_PREFIX_CHANGED")
        self.assertEqual(db.execute("SELECT active FROM state").fetchone()[0], "pending")
        self.assertEqual(db.execute("SELECT phase,response FROM requests WHERE id='pending'").fetchone(),
                         ("pending", None))
        self.observe(db, "full-rollback-observed")
        small = encode({"synthetic": True, "status": "REFUSED", "code": "METADATA_SPACE"})
        self.assertLessEqual(len(small), 4096)
        self.assertEqual(db.execute("PRAGMA max_page_count=7168").fetchone()[0], TERMINAL)
        db.execute("BEGIN IMMEDIATE")
        db.execute("UPDATE requests SET phase='terminal',response=? WHERE id='pending'", (small,))
        db.execute("UPDATE state SET active=NULL")
        self.observe(db, "small-terminal-uncommitted")
        db.execute("COMMIT")
        expected = json.loads(json.dumps(before))
        expected["state"][0][-1] = None
        for row in expected["requests"]:
            if row[0] == "pending":
                row[2], row[3] = "terminal", compact(small)
        self.assertEqual(self.logical(db), expected, "TERMINAL_ONLY_DELTA_OR_CONSUMPTION_CHANGED")
        self.assertEqual(db.execute("SELECT count(*) FROM visible").fetchone()[0], 0)
        self.notes["small_terminal_response_bytes"] = len(small)

    def test_cap_only_expansion_restores_admission_margin_without_refund(self):
        db = self.fresh()
        self.fill(db, [2 * MIB] * 9)
        pages = db.execute("PRAGMA page_count").fetchone()[0]
        self.assertGreater(pages, ADMISSION)
        before = self.logical(db)
        self.assertFalse(pages <= before["state"][0][7] - 4096)
        self.assertEqual(before, self.logical(db), "HEADROOM_REFUSAL_MUST_BE_READ_ONLY")
        self.assertEqual(db.execute("PRAGMA max_page_count=16384").fetchone()[0], 16384)
        db.execute("BEGIN IMMEDIATE")
        db.execute("UPDATE state SET cap=16384")
        db.execute("ROLLBACK")
        self.assertEqual(db.execute("SELECT cap FROM state").fetchone()[0], BASE)
        self.assertEqual(before, self.logical(db), "PRAGMA_EXPANSION_IS_NOT_DURABLE_AUTHORIZATION")
        self.assertEqual(db.execute("PRAGMA max_page_count=8192").fetchone()[0], BASE)
        self.assertEqual(db.execute("PRAGMA max_page_count=16384").fetchone()[0], 16384)
        db.execute("BEGIN IMMEDIATE")
        db.execute("INSERT INTO owner_grants VALUES('cap-only',1,?,?)",
                   (b"synthetic-cap-only-32-to-64-MiB", b"synthetic-no-refund-no-mathematical-acceptance"))
        db.execute("UPDATE state SET cap=16384,grants=1")
        self.observe(db, "cap-only-uncommitted")
        db.execute("COMMIT")
        after = self.logical(db)
        expected_state = before["state"][0][:]
        expected_state[7], expected_state[8] = 16384, 1
        self.assertEqual(after["state"], [expected_state], "CAP_GRANT_CHANGED_OTHER_STATE")
        for table in ("requests", "filler", "visible"):
            self.assertEqual(before[table], after[table])
        self.assertLessEqual(db.execute("PRAGMA page_count").fetchone()[0], 16384 - 4096)
        self.assertEqual(db.execute("PRAGMA max_page_count=14336").fetchone()[0], 14336)
        db.execute("BEGIN IMMEDIATE")
        db.execute("INSERT INTO requests VALUES('new',?,'pending',NULL)", (b"synthetic-new-reservation",))
        db.execute("UPDATE state SET used_requests=used_requests+1,used_bytes=used_bytes+8388608,active='new'")
        db.execute("COMMIT")
        final = db.execute("SELECT used_requests,used_stages,used_bytes,active FROM state").fetchone()
        self.assertEqual(final, (2, 0, 16 * MIB, "new"))
        self.notes["admission_margin"] = {"old_pages": ADMISSION, "actual_pages_before": pages,
                                          "expanded_pages": 12288}

    def test_near_limit_blobs_index_split_and_64_bounded_grants(self):
        db = self.fresh()
        index_page = db.execute("SELECT rootpage FROM sqlite_schema WHERE name='visible_sort'").fetchone()[0]
        def page_kind():
            with self.path.open("rb") as stream:
                stream.seek((index_page - 1) * PAGE)
                return stream.read(1)[0]
        self.assertEqual(page_kind(), 0x0A, "FRESH_INDEX_LEAF_PAGE")
        db.execute("BEGIN IMMEDIATE")
        self.large_write(db, "INSERT INTO visible VALUES('large','large','synthetic-unpromoted',zeroblob(?))",
                         (2 * MIB - 64,), 2 * MIB - 64)
        db.executemany("INSERT INTO visible VALUES(?,?,'synthetic-unpromoted',?)",
                       [("small-" + str(i), str(i).zfill(4) + "k" * 764, b"synthetic" * 8) for i in range(64)])
        large_response = response_bytes(MIB - 64)
        self.large_write(db, "UPDATE requests SET response=? WHERE id='old'", (large_response,), len(large_response))
        self.observe(db, "near-limits-and-index-uncommitted")
        db.execute("COMMIT")
        self.assertEqual(page_kind(), 0x02, "OBSERVED_INDEX_INTERIOR_AFTER_SPLIT")
        self.grants64(db)
        self.assertEqual(db.execute("SELECT length(payload) FROM visible WHERE id='large'").fetchone()[0], 2 * MIB - 64)
        self.assertEqual(db.execute("SELECT length(response) FROM requests WHERE id='old'").fetchone()[0], MIB - 64)
        self.assertEqual(db.execute("SELECT count(*) FROM visible").fetchone()[0], 65)
        self.assertEqual(db.execute("PRAGMA integrity_check(1)").fetchone()[0], "ok")
        self.notes["index"] = {"name": "visible_sort", "root_page": index_page,
                               "before_page_kind": 10, "after_page_kind": 2,
                               "small_indexed_rows": 64, "large_record_rows": 1}
        self.notes["grant_rows"] = {"rows": 64, "exact_blob_bytes": 64 * 8192}

    def test_sql_persisted_type_range_and_used_authorized_invariants(self):
        db = self.fresh(pending=True)
        before = self.logical(db)
        invalid = [("used_requests", -1), ("used_requests", 129), ("used_requests", 1.5),
                   ("used_requests", "not-an-integer"), ("used_stages", 17),
                   ("used_bytes", 4294967297), ("auth_requests", 4097),
                   ("auth_stages", 257), ("auth_bytes", 68719476737),
                   ("cap", 6144), ("grants", 65)]
        for column, value in invalid:
            with self.subTest(column=column, value=value):
                db.execute("BEGIN IMMEDIATE")
                with self.assertRaises(sqlite3.IntegrityError):
                    db.execute("UPDATE state SET " + column + "=?", (value,))
                db.rollback()
                self.assertEqual(before, self.logical(db))
        with self.assertRaises(sqlite3.IntegrityError):
            db.execute("UPDATE state SET used_requests=9223372036854775807+1")
        self.assertEqual(before, self.logical(db))
        # SQL integer affinity cannot distinguish original Python booleans or
        # numeric strings from integers. This is a parser obligation, not a pass.
        db.execute("BEGIN IMMEDIATE")
        db.execute("UPDATE state SET used_requests=?", (True,))
        boolean = db.execute("SELECT used_requests,typeof(used_requests) FROM state").fetchone()
        db.execute("UPDATE state SET used_requests=?", ("2",))
        numeric_string = db.execute("SELECT used_requests,typeof(used_requests) FROM state").fetchone()
        db.rollback()
        self.assertEqual(boolean, (1, "integer"))
        self.assertEqual(numeric_string, (2, "integer"))
        self.assertEqual(before, self.logical(db))
        self.notes["input_type_limitation"] = {"python_boolean_persisted_as": boolean,
                                               "numeric_string_persisted_as": numeric_string}

    def tearDown(self):
        errors = []
        for db in self.connections:
            try:
                if db.in_transaction:
                    db.rollback()
                db.close()
            except BaseException as error:
                errors.append(type(error).__name__ + ":" + str(error)[:256])
        self.journal_sample()
        retained = self.retained()
        report = {"test": self.id(), "synthetic_only": True, "notes": self.notes,
                  "observations": self.observations, "sampled_peak_pages": self.peak_pages,
                  "sampled_peak_journal_bytes": self.peak_journal,
                  "sampled_peak_suite_retained_bytes": self.peak_retained,
                  "retained_bytes_before_this_report": retained, "sql_vm_steps_at_callbacks": self.vm_steps,
                  "suite_large_write_attempts_so_far": self.large_writes,
                  "suite_attempted_payload_bytes_so_far": self.attempted_payload,
                  "close_errors": errors,
                  "failure_authority": "unittest result; observations are retained on failed assertions too"}
        save(self.root / "observations.json", report)
        self.retained()
        self.assertFalse(errors, "SQLITE_CLOSE_FAILURE")


if __name__ == "__main__":
    unittest.main(verbosity=2)

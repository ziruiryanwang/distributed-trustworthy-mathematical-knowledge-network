"""Private protected-event storage, NOT a mathematical admission API.

Only the actual trusted controller may commit after authenticating bootstrap or
the clean grounded-cut worker event. Saved PASS text and supplied summaries are
not authority. Owner/OS integrity, live source support and no rollback are premises.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
import hashlib
import os
from pathlib import Path
import sqlite3
import ordinary_evidence as E
import portable_catalog as P
import cut_map as M
import source_anchor as A
SCHEMA = "DMKN_GROUNDED_CUT_CATALOG_V1"
ROOT_SCHEMA = "DMKN_GROUNDED_CUT_ROOT_V1"
SUMMARY_DOMAIN = b"DMKN-GROUNDED-CUT-SUMMARY-V1\0"
ROOT_DOMAIN = b"DMKN-GROUNDED-CUT-ROOT-V1\0"
ROOT_FIELDS = {"schema", "store_id", "support_id", "epoch", "source_binding_sha256",
               "kind", "parent", "map_root", "request_id", "unit_id",
               "frontier_summary", "result_summary", "event_summary"}

class CatalogError(ValueError):
    pass
class CommitDisposition(CatalogError):
    """Terminal outcome; never retry automatically, including UNKNOWN."""
    def __init__(self, root_id, disposition):
        self.root_id, self.disposition = root_id, disposition
        super().__init__("CUT_COMMIT_" + disposition + ":" + root_id)


def need(ok, code):
    if not ok:
        raise CatalogError("CUT_CATALOG_" + code)

@dataclass(frozen=True)
class Limits:
    max_db_pages: int = 262144
    max_roots: int = 1000000
    max_summaries: int = 4000000
    max_summary_bytes: int = 8 * 1024**2
    max_total_summary_bytes: int = 1024**3
    max_root_bytes: int = 16384
    max_total_root_bytes: int = 256 * 1024**2
    max_nodes: int = 16000000
    max_total_node_bytes: int = 1024**3
    map_limits: M.Limits = M.DEFAULT_LIMITS

    def __post_init__(self):
        need(type(self.map_limits) is M.Limits, "MAP_LIMITS")
        for key, value in vars(self).items():
            if key != "map_limits":
                need(type(value) is int and 1 <= value <= (1 << 63) - 1, "LIMITS")
        need(self.max_db_pages <= 1048576 and self.max_summary_bytes <= 64 * 1024**2
             and self.max_root_bytes <= 65536, "HARD_LIMITS")


def _operation(method):
    @wraps(method)
    def call(self, *args, **kwargs):
        try:
            self._live()
            need(self._db.in_transaction and self._allowance is not None, "BEGIN_REQUIRED")
            return method(self, *args, **kwargs)
        except BaseException:
            self._abort()
            raise
    return call

class CutCatalog:
    @classmethod
    def open(cls, directory, *, store_id, support_id, epoch, source_binding_raw,
             check, create=False, limits=Limits()):
        need(os.name == "nt" and callable(check), "WINDOWS_LIVE_GUARD_REQUIRED")
        need(type(create) is bool and type(limits) is Limits, "CONFIGURATION")
        check()
        A.parse_binding(source_binding_raw)
        self = cls.__new__(cls)
        self._closed = self._denied = False
        self._db = self._lock = self._allowance = None
        self._check, self._limits = check, limits
        self._identity = dict(store_id=P.hexid(store_id), support_id=P.hexid(support_id),
                              epoch=P.hexid(epoch),
                              source_binding_sha256=hashlib.sha256(source_binding_raw).hexdigest())
        self._caps = (limits.max_roots, limits.max_summaries, limits.max_total_summary_bytes,
                      limits.max_nodes, limits.max_total_node_bytes, limits.max_total_root_bytes)
        config = {key: value for key, value in vars(limits).items() if key != "map_limits"}
        config["map_limits"] = vars(limits.map_limits)
        self._marker = E.canonical_json(dict(schema=SCHEMA, **self._identity,
                                source_binding_hex=source_binding_raw.hex(), limits=config))
        self._root = P.ordinary(directory, directory=True, fresh=create)
        self._base, self._state, self._bootstrap = (0,) * 6, "BOOTSTRAPPING", ""
        self._pending, self._maps = [0] * 6, set()
        try:
            if create:
                self._root.mkdir()
                P.PortableCatalog._write_fresh(self._root / "ADOPTION.json", self._marker)
                P.PortableCatalog._write_fresh(self._root / "owner.lock", b"\0")
            need(P.read_bounded(self._root / "ADOPTION.json", len(self._marker)) == self._marker,
                 "ADOPTION_CHANGED")
            need(P.read_bounded(self._root / "owner.lock", 1) == b"\0", "LOCK_FILE")
            import msvcrt
            self._lock = P.ordinary(self._root / "owner.lock").open("r+b")
            msvcrt.locking(self._lock.fileno(), msvcrt.LK_NBLCK, 1)
            database = P.ordinary(self._root / "catalog.sqlite", fresh=create)
            for suffix in ("-wal", "-shm", "-journal"):
                need(not os.path.lexists(str(database) + suffix), "RECOVERY_REQUIRED")
            if not create:
                need(0 < database.stat().st_size <= limits.max_db_pages * 4096, "DB_BOUND")
            self._db = sqlite3.connect(database, isolation_level=None, timeout=1)
            for pragma in ("trusted_schema=OFF", "foreign_keys=ON", "journal_mode=DELETE",
                           "synchronous=FULL", "temp_store=MEMORY", "mmap_size=0"):
                self._db.execute("PRAGMA " + pragma)
            need(self._db.execute("PRAGMA page_size").fetchone() == (4096,), "PAGE_SIZE")
            need(self._db.execute("PRAGMA max_page_count=" + str(limits.max_db_pages)).fetchone()
                 == (limits.max_db_pages,), "PAGE_BOUND")
            if create:
                self._db.execute("BEGIN IMMEDIATE")
                self._db.execute("""CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1),
                    marker BLOB NOT NULL,state TEXT NOT NULL,bootstrap TEXT NOT NULL,
                    roots INTEGER NOT NULL,summaries INTEGER NOT NULL,summary_bytes INTEGER NOT NULL,
                    nodes INTEGER NOT NULL,node_bytes INTEGER NOT NULL,root_bytes INTEGER NOT NULL)""")
                for table in ("roots", "summaries"):
                    self._db.execute("CREATE TABLE " + table +
                                     "(id TEXT PRIMARY KEY,raw BLOB NOT NULL) WITHOUT ROWID")
                M.create_schema(self._db, M.Allowance(0, 1, 0, 0))
                self._db.execute("INSERT INTO meta VALUES(1,?,'BOOTSTRAPPING','',0,0,0,0,0,0)",
                                 (self._marker,))
                self._db.execute("COMMIT")
            row = self._meta()
            self._state, self._bootstrap, *counts = row
            self._base = tuple(counts)
            need(create or (self._state == "ACTIVE" and self._base[0] > 0), "INCOMPLETE_BOOTSTRAP")
            self._live()
            return self
        except BaseException:
            self.close()
            raise

    def _meta(self):
        row = self._db.execute("""SELECT CASE WHEN typeof(marker)='blob' AND length(marker)=?
            THEN marker END,CASE WHEN typeof(state)='text' AND length(state)<=13 THEN state END,
            CASE WHEN typeof(bootstrap)='text' AND length(bootstrap)<=64 THEN bootstrap END,
            CASE WHEN typeof(roots)='integer' THEN roots END,
            CASE WHEN typeof(summaries)='integer' THEN summaries END,
            CASE WHEN typeof(summary_bytes)='integer' THEN summary_bytes END,
            CASE WHEN typeof(nodes)='integer' THEN nodes END,
            CASE WHEN typeof(node_bytes)='integer' THEN node_bytes END,
            CASE WHEN typeof(root_bytes)='integer' THEN root_bytes END
            FROM meta WHERE id=1""", (len(self._marker),)).fetchone()
        need(row is not None and row[0] == self._marker, "META_IDENTITY")
        need(row[1] in ("BOOTSTRAPPING", "ACTIVE") and
             ((row[1] == "BOOTSTRAPPING" and row[2] == "") or
              (row[1] == "ACTIVE" and P.hexid(row[2]) == row[2])), "META_STATE")
        need(all(type(n) is int and 0 <= n <= cap for n, cap in zip(row[3:], self._caps)),
             "META_COUNTERS")
        return row[1:]

    def _live(self):
        need(not self._closed and not self._denied, "CLOSED_OR_WITHDRAWN")
        try:
            self._check()  # Original allowance AND the held SourceAnchor.check.
            need(not os.path.lexists(self._root / "WITHDRAWN"), "WITHDRAWN")
            need(P.read_bounded(self._root / "ADOPTION.json", len(self._marker)) == self._marker,
                 "ADOPTION_CHANGED")
            db = P.ordinary(self._root / "catalog.sqlite")
            need(db.stat().st_size <= self._limits.max_db_pages * 4096, "DB_BOUND")
            for suffix in ("-wal", "-shm"):
                need(not os.path.lexists(str(db) + suffix), "SIDECAR")
            journal = Path(str(db) + "-journal")
            if os.path.lexists(journal):
                need(P.ordinary(journal).stat().st_size <=
                     2 * self._limits.max_db_pages * 4096 + 1024**2, "JOURNAL_BOUND")
            need(self._meta() == (self._state, self._bootstrap, *self._base), "META_CHANGED")
        except BaseException:
            self._denied = True
            raise

    def _begin(self, allowance):
        try:
            self._live()
            need(not self._db.in_transaction and type(allowance) is M.Allowance, "TRANSACTION_STATE")
            self._db.execute("BEGIN IMMEDIATE")
            self._allowance, self._pending, self._maps = allowance, [0] * 6, set()
            if self._state == "BOOTSTRAPPING":
                self._maps.add(M.EMPTY_ROOT)
        except BaseException:
            self._abort()
            raise

    def _reserve(self, index, amount):
        need(self._base[index] + self._pending[index] + amount <= self._caps[index], "QUOTA")
        self._pending[index] += amount

    def _read(self, table, identifier, cap, domain, optional=False):
        P.hexid(identifier)
        a = self._allowance
        a._charge("reads", 1)
        available = a.max_read_bytes - a.read_bytes
        row = self._db.execute("SELECT typeof(raw),length(raw),CASE WHEN typeof(raw)='blob' "
            "AND length(raw)<=? THEN raw ELSE NULL END FROM " + table + " WHERE id=?",
            (min(cap, available), identifier)).fetchone()
        if row is None:
            need(optional, "MISSING_" + table.upper())
            return None
        kind, size, raw = row
        need(kind == "blob" and type(size) is int and 0 < size <= cap and
             size <= available and type(raw) is bytes and len(raw) == size, "BLOB_BOUND")
        a._charge("read_bytes", size)
        need(hashlib.sha256(domain + raw).hexdigest() == identifier, "CONTENT_HASH")
        return raw

    def _put(self, table, identifier, raw):
        self._allowance._charge("writes", 1)
        self._allowance._charge("write_bytes", len(raw))
        self._db.execute("INSERT INTO " + table + " VALUES(?,?)", (identifier, raw))

    @_operation
    def put_summary(self, raw):
        need(type(raw) is bytes and 0 < len(raw) <= self._limits.max_summary_bytes, "SUMMARY_BOUND")
        identifier = hashlib.sha256(SUMMARY_DOMAIN + raw).hexdigest()
        old = self._read("summaries", identifier, self._limits.max_summary_bytes, SUMMARY_DOMAIN, True)
        if old is None:
            self._reserve(1, 1)
            self._reserve(2, len(raw))
            self._put("summaries", identifier, raw)
        else:
            need(old == raw, "SUMMARY_COLLISION")
        return identifier

    @_operation
    def read_summary(self, identifier):
        return self._read("summaries", identifier, self._limits.max_summary_bytes, SUMMARY_DOMAIN)

    def _record(self, record):
        need(type(record) is dict and set(record) == ROOT_FIELDS and
             record["schema"] == ROOT_SCHEMA and
             all(record[key] == value for key, value in self._identity.items()), "ROOT_IDENTITY")
        for key in ("map_root", "request_id", "frontier_summary", "result_summary", "event_summary"):
            P.hexid(record[key])
        need(record["kind"] in ("native-bootstrap", "theorem-cut"), "ROOT_KIND")
        if record["kind"] == "native-bootstrap":
            need(record["parent"] == record["unit_id"] == "", "BOOTSTRAP_PARENT")
        else:
            P.hexid(record["parent"])
            P.hexid(record["unit_id"])
        raw = E.canonical_json(record)
        need(len(raw) <= self._limits.max_root_bytes, "ROOT_BOUND")
        return raw

    @_operation
    def root(self, identifier):
        raw = self._read("roots", identifier, self._limits.max_root_bytes, ROOT_DOMAIN)
        record = E.strict_json(raw, E.Limits(max_bytes=self._limits.max_root_bytes))
        need(self._record(record) == raw, "ROOT_ENCODING")
        self._maps.add(record["map_root"])
        return record

    @_operation
    def lookup(self, root_id, encoded_name):
        return M.lookup(self._db, self.root(root_id)["map_root"], encoded_name,
                        self._allowance, limits=self._limits.map_limits)

    @_operation
    def _insert(self, map_root, encoded_name, value):
        need(map_root in self._maps, "UNROOTED_MAP")
        a = self._allowance
        writes, size = a.writes, a.write_bytes
        result = M.insert(self._db, map_root, encoded_name, value, a, limits=self._limits.map_limits)
        self._reserve(3, a.writes - writes)
        self._reserve(4, a.write_bytes - size)
        self._maps.add(result)
        return result

    def _commit_root(self, record):
        """PRIVATE: actual protected controller has established mathematical event."""
        try:
            self._live()
            need(self._db.in_transaction and self._allowance is not None, "BEGIN_REQUIRED")
            raw = self._record(record)
            identifier = hashlib.sha256(ROOT_DOMAIN + raw).hexdigest()
            if self._state == "BOOTSTRAPPING":
                need(record["kind"] == "native-bootstrap" and self._base[0] == 0, "BOOTSTRAP_ONLY")
                bootstrap = identifier
            else:
                need(record["kind"] == "theorem-cut", "EXTENSION_ONLY")
                self.root(record["parent"])
                bootstrap = self._bootstrap
            need(record["map_root"] in self._maps, "UNROOTED_MAP")
            for key in ("frontier_summary", "result_summary", "event_summary"):
                self.read_summary(record[key])
            need(self._read("roots", identifier, self._limits.max_root_bytes, ROOT_DOMAIN, True)
                 is None, "ROOT_ALREADY_COMMITTED")
            self._reserve(0, 1)
            self._reserve(5, len(raw))
            self._put("roots", identifier, raw)
            counts = tuple(a + b for a, b in zip(self._base, self._pending))
            self._live()  # Last live source/withdrawal/budget check before authority changes.
            self._db.execute("UPDATE meta SET state='ACTIVE',bootstrap=?,roots=?,summaries=?,"
                "summary_bytes=?,nodes=?,node_bytes=?,root_bytes=? WHERE id=1", (bootstrap, *counts))
        except BaseException:
            self._abort()
            raise
        try:
            self._db.execute("COMMIT")
        except BaseException as error:
            disposition = "UNKNOWN"
            try:
                if self._db.in_transaction:
                    self._db.execute("ROLLBACK")
                    disposition = "NOT_COMMITTED"
                else:
                    row = self._db.execute("SELECT raw FROM roots WHERE id=? AND length(raw)=?",
                                           (identifier, len(raw))).fetchone()
                    disposition = "COMMITTED" if row == (raw,) else "UNKNOWN"
            except BaseException:
                pass
            try:
                self.close()
            except BaseException:
                pass
            raise CommitDisposition(identifier, disposition) from error
        self._state, self._bootstrap, self._base = "ACTIVE", bootstrap, counts
        self._allowance, self._pending, self._maps = None, [0] * 6, set()
        return identifier

    def _abort(self):
        if self._db is not None and not self._closed and self._db.in_transaction:
            try:
                self._db.execute("ROLLBACK")
            except BaseException:
                self.close()
                raise
        self._allowance, self._pending, self._maps = None, [0] * 6, set()

    def close(self):
        if self._closed:
            return
        self._closed = True
        try:
            if self._db is not None:
                self._db.close()
        finally:
            if self._lock is not None:
                self._lock.close()

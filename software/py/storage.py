"""V3 operation-local control store; integrated development, not qualified.

Trusted owner filesystem; one OS writer lock. Indexed immutable records and
sequence cuts are local bookkeeping, never mathematical acceptance authority.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import msvcrt
from pathlib import Path
import sqlite3

from capacity import initial_authorization, parse_grant, physical_supply

MIB = 1024 * 1024
MAX_REQUESTS, MAX_STAGES, MAX_RESERVED = 4096, 256, 64 * 1024 * MIB
METADATA_PAGES = (8192, 16384, 32768, 65536)


class Refusal(Exception):
    def __init__(self, code, detail=""):
        super().__init__(detail or code)
        self.code, self.detail = code, detail


class RenewalUncertain(Refusal):
    def __init__(self, detail=""):
        super().__init__("RENEWAL_OUTCOME_UNKNOWN", detail)


def require(value, code, detail=""):
    if not value:
        raise Refusal(code, detail)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def decode(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "INVALID_JSON", "duplicate key")
            result[key] = value
        return result
    def bad(_):
        raise Refusal("INVALID_JSON", "noninteger number")
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                          parse_float=bad, parse_constant=bad)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as error:
        raise Refusal("INVALID_JSON", type(error).__name__) from None


def read(path, limit):
    with Path(path).open("rb") as stream:
        raw = stream.read(limit + 1)
    require(len(raw) <= limit, "INPUT_LIMIT")
    return raw


@contextmanager
def owner_lock(root, *, create=True):
    """OS-released lock, not evidence that native descendants are quiescent."""
    root = Path(root)
    require(type(create) is bool, "LOCK_CREATE_FLAG")
    if create:
        root.mkdir(parents=True, exist_ok=True)
        stream = (root / "owner.lock").open("a+b")
        stream.seek(0, 2)
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
    else:
        require(root.is_dir() and (root / "owner.lock").is_file(), "EXISTING_OWNER_LOCK_REQUIRED")
        stream = (root / "owner.lock").open("r+b")
    stream.seek(0)
    locked = False
    try:
        try:
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            locked = True
        except OSError:
            raise Refusal("BUSY") from None
        if not create:
            # A competing Windows byte-range lock may itself forbid reading.
            # Validate bytes only after acquiring, so contention remains BUSY.
            stream.seek(0)
            require(stream.read(2) == b"0", "OWNER_LOCK_BYTES")
        yield
    finally:
        try:
            if locked:
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        finally:
            stream.close()


SCHEMA = (
    "CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1),config TEXT NOT NULL,"
    "initialized INTEGER NOT NULL CHECK(typeof(initialized)='integer' AND initialized IN (0,1)),"
    "requests INTEGER NOT NULL CHECK(typeof(requests)='integer' AND requests BETWEEN 0 AND 4096),"
    "stages INTEGER NOT NULL CHECK(typeof(stages)='integer' AND stages BETWEEN 0 AND 256),"
    "charged INTEGER NOT NULL CHECK(typeof(charged)='integer' AND charged BETWEEN 0 AND 68719476736),active TEXT)",
    "CREATE TABLE requests(key TEXT PRIMARY KEY,client TEXT NOT NULL,request_id TEXT NOT NULL,"
    "raw BLOB NOT NULL CHECK(typeof(raw)='blob' AND length(raw)<=131072),"
    "phase TEXT NOT NULL CHECK(phase IN ('pending','terminal')),response BLOB,"
    "CHECK((phase='pending' AND response IS NULL) OR (phase='terminal' AND typeof(response)='blob' AND length(response)<=1048576)),"
    "UNIQUE(client,request_id)) WITHOUT ROWID",
    "CREATE TABLE records(handle TEXT PRIMARY KEY,kind TEXT NOT NULL,client TEXT NOT NULL,"
    "raw BLOB NOT NULL CHECK(typeof(raw)='blob' AND length(raw)<=2097152)) WITHOUT ROWID",
    "CREATE TABLE heads(client TEXT PRIMARY KEY,context TEXT NOT NULL) WITHOUT ROWID",
    "CREATE TABLE providers(provider TEXT PRIMARY KEY,cut INTEGER NOT NULL CHECK(typeof(cut)='integer' AND cut BETWEEN 0 AND 8192),snapshot TEXT NOT NULL) WITHOUT ROWID",
    "CREATE TABLE snapshots(handle TEXT PRIMARY KEY,provider TEXT NOT NULL,cut INTEGER NOT NULL CHECK(typeof(cut)='integer' AND cut BETWEEN 0 AND 8192),raw BLOB NOT NULL CHECK(typeof(raw)='blob' AND length(raw)<=2048)) WITHOUT ROWID",
    "CREATE TABLE entries(provider TEXT NOT NULL,seq INTEGER NOT NULL CHECK(typeof(seq)='integer' AND seq BETWEEN 1 AND 8192),descriptor_key TEXT NOT NULL,raw BLOB NOT NULL CHECK(typeof(raw)='blob' AND length(raw)<=32768),PRIMARY KEY(provider,seq),UNIQUE(provider,descriptor_key)) WITHOUT ROWID",
    "CREATE TABLE stages(id INTEGER PRIMARY KEY CHECK(id BETWEEN 0 AND 255),request TEXT NOT NULL,"
    "purpose TEXT NOT NULL CHECK(purpose IN ('bootstrap','admit','submit')),directory TEXT NOT NULL,"
    "grant_bytes INTEGER NOT NULL CHECK(typeof(grant_bytes)='integer' AND grant_bytes BETWEEN 1 AND 536870912))",
    "CREATE TABLE authorization(id INTEGER PRIMARY KEY CHECK(id=1),config TEXT NOT NULL,"
    "requests INTEGER NOT NULL CHECK(typeof(requests)='integer' AND requests BETWEEN 1 AND 4096),"
    "stages INTEGER NOT NULL CHECK(typeof(stages)='integer' AND stages BETWEEN 1 AND 256),"
    "reserved_bytes INTEGER NOT NULL CHECK(typeof(reserved_bytes)='integer' AND reserved_bytes BETWEEN 0 AND 68719476736),"
    "metadata_pages INTEGER NOT NULL CHECK(typeof(metadata_pages)='integer' AND metadata_pages IN (8192,16384,32768,65536)),"
    "grants INTEGER NOT NULL CHECK(typeof(grants)='integer' AND grants BETWEEN 0 AND 64))",
    "CREATE TABLE owner_grants(grant_id TEXT PRIMARY KEY,sequence INTEGER UNIQUE NOT NULL "
    "CHECK(typeof(sequence)='integer' AND sequence BETWEEN 1 AND 64),"
    "raw BLOB NOT NULL CHECK(typeof(raw)='blob' AND length(raw) BETWEEN 1 AND 4096),"
    "response BLOB NOT NULL CHECK(typeof(response)='blob' AND length(response) BETWEEN 1 AND 4096)) WITHOUT ROWID",
)

class ControlStore:
    def __init__(self, root, config_id, limits, event, *, create=False, readonly=False, scratch=None):
        self.root, self.config_id, self.limits, self.event = Path(root), config_id, limits, event
        self.scratch, self.readonly = scratch, readonly
        self.db_path = self.root / "control.sqlite3"
        self._uncertain, self._tier = False, None
        require(type(create) is bool and type(readonly) is bool and not (create and readonly), "STORE_OPEN_FLAGS")
        require(type(config_id) is str and len(config_id) == 64
                and all(c in "0123456789abcdef" for c in config_id), "CONFIG_ID")
        require(sqlite3.sqlite_version == "3.50.4", "SQLITE_VERSION")
        for suffix in ("-journal", "-wal", "-shm"):
            path = Path(str(self.db_path) + suffix)
            require(not path.exists() or path.stat().st_size == 0, "UNEXPECTED_SQLITE_AUXILIARY")
        fresh = not self.db_path.exists()
        require(not fresh or (create and not readonly), "NOT_INITIALIZED")
        initial = initial_authorization(limits) if fresh else None
        if fresh:
            self.event["initial_physical_supply"] = physical_supply(
                self.root, scratch, initial["reserved_bytes"], initial["metadata_pages"])
        self.db = sqlite3.connect(self.db_path.absolute().as_uri()
                                  + ("?mode=ro" if readonly else "?mode=rwc" if fresh else "?mode=rw"),
                                  uri=True, timeout=0, isolation_level=None)
        self.event["sql_opened"] = True
        self.db.row_factory = sqlite3.Row
        self.db.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 3 * MIB)
        self.db.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 16384)
        self.db.set_progress_handler(self._progress, 1)
        try:
            # Reject old/unsupported stores before any writable setup pragma.
            version = self.scalar("version", "PRAGMA user_version")
            require(type(version) is int and version == (0 if fresh else 3), "SQLITE_SCHEMA_VERSION")
            if readonly:
                self.exec("query_only", "PRAGMA query_only=ON")
                require(self.scalar("query_only_read", "PRAGMA query_only") == 1, "SQLITE_READ_ONLY")
            require(self.scalar("journal", "PRAGMA journal_mode") == "delete", "SQLITE_PROFILE")
            if fresh:
                self.exec("page_size", "PRAGMA page_size=4096")
                self.exec("vacuum_none", "PRAGMA auto_vacuum=NONE")
            require(self.scalar("pagesize", "PRAGMA page_size") == 4096, "SQLITE_PROFILE")
            require(self.scalar("vacuum", "PRAGMA auto_vacuum") == 0, "SQLITE_PROFILE")
            if not readonly:
                self.exec("sync", "PRAGMA synchronous=FULL")
                require(self.scalar("sync_read", "PRAGMA synchronous") == 2, "SQLITE_PROFILE")
            # Connection-only bounds also apply to status; neither pragma
            # configures persistent database state or enables a write.
            self.exec("temp", "PRAGMA temp_store=MEMORY")
            self.exec("mmap", "PRAGMA mmap_size=0")
            if fresh:
                with self._transaction(initial["metadata_pages"], "initial"):
                    for i, statement in enumerate(SCHEMA):
                        self.exec("schema_" + str(i), statement)
                    self.exec("meta_create", "INSERT INTO meta VALUES(1,?,0,0,0,0,NULL)", (config_id,))
                    self.exec("authorization_create", "INSERT INTO authorization VALUES(1,?,?,?,?,?,0)",
                              (config_id, initial["requests"], initial["stages"],
                               initial["reserved_bytes"], initial["metadata_pages"]))
                    self.exec("schema_version", "PRAGMA user_version=3")
            state = self.authorization_state()
            pages = self.page_count()
            self.event["metadata_pages_consistent"] = pages <= state["metadata_pages"]
            if not readonly:
                # Historical request/grant replay is reachable above ordinary tier.
                self._ceiling(state["metadata_pages"])
        except BaseException:
            self.db.close()
            raise

    def _progress(self):
        self.event["sql_vm_steps"] += 1
        return int(self.event["sql_vm_steps"] >= 100000)

    def exec(self, name, statement, values=()):
        return self.db.execute(statement, values)

    def rows(self, name, statement, values=(), maximum=1):
        cursor = self.exec(name, statement, values)
        rows = cursor.fetchmany(maximum + 1)
        require(len(rows) <= maximum, "SQL_ROW_BOUND", name)
        counts = self.event["sql_rows"]
        counts[name] = counts.get(name, 0) + len(rows)
        return rows

    def scalar(self, name, statement, values=()):
        rows = self.rows(name, statement, values)
        require(len(rows) == 1, "MISSING_SQL_SINGLETON", name)
        return rows[0][0]

    @staticmethod
    def integer(value, low, high, code="CORRUPT_CAPACITY"):
        require(type(value) is int and low <= value <= high, code)
        return value

    def meta(self):
        rows = self.rows("meta", "SELECT * FROM meta WHERE id=1")
        require(len(rows) == 1, "MISSING_META")
        value = rows[0]
        require(value["config"] == self.config_id, "CONFIG_CHANGED")
        self.integer(value["initialized"], 0, 1)
        for key, maximum in (("requests", MAX_REQUESTS), ("stages", MAX_STAGES), ("charged", MAX_RESERVED)):
            self.integer(value[key], 0, maximum)
        active = value["active"]
        require(active is None or (type(active) is str and len(active) == 64
                and all(c in "0123456789abcdef" for c in active)), "CORRUPT_ACTIVE")
        return value

    def authorization_state(self):
        meta = self.meta()
        rows = self.rows("authorization", "SELECT * FROM authorization WHERE id=1")
        require(len(rows) == 1 and rows[0]["config"] == self.config_id, "AUTHORIZATION_BINDING")
        value = rows[0]
        authorized = {}
        for key, minimum, maximum in (("requests", 1, MAX_REQUESTS), ("stages", 1, MAX_STAGES),
                                      ("reserved_bytes", 0, MAX_RESERVED)):
            authorized[key] = self.integer(value[key], minimum, maximum)
        pages, grants = value["metadata_pages"], value["grants"]
        require(type(pages) is int and pages in METADATA_PAGES, "CORRUPT_METADATA_CAP")
        self.integer(grants, 0, 64)
        used = {"requests": meta["requests"], "stages": meta["stages"], "reserved_bytes": meta["charged"]}
        require(all(used[key] <= authorized[key] for key in used), "USED_EXCEEDS_AUTHORIZATION")
        return {"used": used, "authorized": authorized, "metadata_pages": pages, "grants": grants,
                "initialized": meta["initialized"], "active": meta["active"]}

    def page_count(self):
        return self.integer(self.scalar("pages", "PRAGMA page_count"), 0, 2147483647, "SQLITE_PAGE_COUNT")

    def _writable(self):
        require(not self.readonly, "READ_ONLY_CONTROL")
        require(not self._uncertain, "TRANSACTION_OUTCOME_UNKNOWN")

    def _ceiling(self, pages):
        self._writable()
        self.integer(pages, 1, 65536, "SQLITE_TIER")
        require(self.page_count() <= pages, "METADATA_CAP_INCONSISTENT")
        require(self.scalar("cap", "PRAGMA max_page_count=" + str(pages)) == pages, "SQLITE_CAP")

    @contextmanager
    def _transaction(self, pages, tier):
        self._writable()
        require(not self.db.in_transaction and self._tier is None, "TRANSACTION_ALREADY_ACTIVE")
        self._ceiling(pages)
        self.exec("begin", "BEGIN IMMEDIATE")
        self._tier = tier
        commit_attempted = False
        try:
            yield
            commit_attempted = True
            self.exec("commit", "COMMIT")
        except BaseException as error:
            rollback_error = None
            try:
                self.db.rollback()
                require(not self.db.in_transaction, "ROLLBACK_NOT_COMPLETE")
            except BaseException as failure:
                rollback_error = failure
            # A failed COMMIT may already be durable. Even a returned rollback
            # cannot prove otherwise, so no terminalization follows in this store.
            if commit_attempted or rollback_error is not None:
                self._uncertain = True
                self.event["transaction_outcome_unknown"] = True
                if tier == "administrative":
                    self.event["renewal_state_outcome"] = "UNKNOWN_REPLAY_REQUIRED"
                    raise RenewalUncertain(type(error).__name__) from error
                raise Refusal("TRANSACTION_OUTCOME_UNKNOWN", type(error).__name__) from error
            self.event["transaction_rollback_confirmed"] = True
            if (tier == "ordinary" and isinstance(error, sqlite3.Error)
                    and getattr(error, "sqlite_errorcode", None) == sqlite3.SQLITE_FULL):
                raise Refusal("METADATA_SPACE") from error
            raise
        finally:
            self._tier = None

    @contextmanager
    def transaction(self):
        state = self.authorization_state()
        with self._transaction(state["metadata_pages"] - 2048, "ordinary"):
            yield

    def close(self):
        self.db.close()

    def prior(self, client, request_id, raw):
        rows = self.rows("request", "SELECT raw,phase,response FROM requests WHERE client=? AND request_id=?",
                         (client, request_id))
        if not rows:
            return None
        require(bytes(rows[0]["raw"]) == raw, "REQUEST_ID_CONFLICT")
        require(rows[0]["phase"] == "terminal", "PENDING_EXECUTION")
        require(type(rows[0]["response"]) is bytes and 0 < len(rows[0]["response"]) <= MIB, "TERMINAL_RESPONSE_BINDING")
        return rows[0]["response"]

    def reserve(self, client, request_id, raw, *, grant=None):
        self._writable()
        if grant is None:
            grant = self.limits["request_bytes"]
        require(type(grant) is int and grant > 0 and grant in {
            self.limits["request_bytes"], self.limits.get("peer_request_bytes"),
            self.limits.get("expose_request_bytes")}, "REQUEST_GRANT")
        state = self.authorization_state()
        require(state["active"] is None, "PENDING_EXECUTION")
        requests = state["used"]["requests"] + 1
        charged = state["used"]["reserved_bytes"] + grant
        require(requests <= state["authorized"]["requests"], "REQUEST_QUOTA")
        require(charged <= state["authorized"]["reserved_bytes"], "STAGING_QUOTA")
        require(self.page_count() <= state["metadata_pages"] - 4096, "METADATA_HEADROOM")
        self.event["admission_physical_supply"] = physical_supply(
            self.root, self.scratch, state["authorized"]["reserved_bytes"] - state["used"]["reserved_bytes"],
            state["metadata_pages"])
        key = digest(encode([client, request_id]))
        with self.transaction():
            require(encode(self.authorization_state()) == encode(state), "AUTHORIZATION_CHANGED")
            self.exec("request_insert", "INSERT INTO requests VALUES(?,?,?,?,?,NULL)",
                      (key, client, request_id, raw, "pending"))
            origin = self.event.get("origin_directory")
            if origin is not None:
                require(type(origin) is str and len(origin) <= 32767 and Path(origin).is_absolute(),
                        "REQUEST_ORIGIN_DIRECTORY")
                self.put_record("attempt", "owner", {"request": key, "call_directory": origin})
            self.exec("request_charge", "UPDATE meta SET requests=?,charged=?,active=? WHERE id=1",
                      (requests, charged, key))
        self.event["reserved_request_bytes"] = grant
        return key

    def _pending(self, key):
        require(self.meta()["active"] == key, "PENDING_BINDING")
        rows = self.rows("pending", "SELECT phase,response FROM requests WHERE key=?", (key,))
        require(len(rows) == 1 and rows[0]["phase"] == "pending" and rows[0]["response"] is None, "PENDING_BINDING")

    def terminal(self, key, response):
        self._writable()
        require(self.db.in_transaction and self._tier in {"ordinary", "terminal"}, "TERMINAL_TRANSACTION")
        self._pending(key)
        require(type(response) is bytes and 0 < len(response) <= MIB, "RESPONSE_LIMIT")
        cursor = self.exec("terminal", "UPDATE requests SET phase='terminal',response=? WHERE key=? AND phase='pending'",
                           (response, key))
        require(cursor.rowcount == 1, "PENDING_BINDING")
        self.exec("inactive", "UPDATE meta SET active=NULL WHERE id=1")

    def terminal_refusal(self, key, reply):
        self._writable()
        require(not self.db.in_transaction, "ROLLBACK_NOT_COMPLETE")
        require(type(reply) is bytes and 0 < len(reply) <= MIB, "RESPONSE_LIMIT")
        value = decode(reply)
        require(type(value) is dict and value.get("status") == "REFUSED"
                and type(value.get("code")) is str and 0 < len(value["code"]) <= 128
                and "accepted" not in value
                and ("mathematicalAcceptance" not in value or value["mathematicalAcceptance"] is False),
                "TERMINAL_REFUSAL_ONLY")
        if value["code"] == "METADATA_SPACE":
            require(len(reply) <= 4096, "METADATA_REFUSAL_BOUND")
        state = self.authorization_state()
        self._pending(key)
        with self._transaction(state["metadata_pages"] - 1024, "terminal"):
            require(encode(self.authorization_state()) == encode(state), "AUTHORIZATION_CHANGED")
            self._pending(key)
            self.terminal(key, reply)
        self.event["terminal_only_completion"] = True

    def stage(self, key, purpose):
        require(purpose in {"bootstrap", "admit", "submit"}, "STAGE_PURPOSE")
        with self.transaction():
            state = self.authorization_state()
            self._pending(key)
            require(state["used"]["stages"] < state["authorized"]["stages"], "STAGE_QUOTA")
            grant = self.integer(self.limits["stage_bytes"], MIB, 512 * MIB, "STAGE_GRANT")
            charged = state["used"]["reserved_bytes"] + grant
            require(charged <= state["authorized"]["reserved_bytes"], "STAGING_QUOTA")
            number = state["used"]["stages"]
            directory = self.root / "work" / key / ("stage-%04d" % number)
            self.exec("stage_insert", "INSERT INTO stages VALUES(?,?,?,?,?)", (number, key, purpose, str(directory), grant))
            self.exec("stage_charge", "UPDATE meta SET stages=?,charged=? WHERE id=1", (number + 1, charged))
        self.event["stages_allocated"] += 1
        return {"id": number, "directory": str(directory), "seconds": self.limits["native_seconds"],
                "memory_mib": self.limits["native_memory_mib"], "bytes": grant}

    def _grant_prior(self, raw, parsed):
        rows = self.rows("grant", "SELECT sequence,raw,response FROM owner_grants WHERE grant_id=?",
                         (parsed["grant_id"],))
        if not rows:
            return None
        row = rows[0]
        self.integer(row["sequence"], 1, 64, "GRANT_RECORD_BINDING")
        require(type(row["raw"]) is bytes and row["raw"] == raw, "GRANT_ID_CONFLICT")
        require(type(row["response"]) is bytes and 0 < len(row["response"]) <= 4096, "GRANT_RECORD_BINDING")
        return row["response"]

    def _grant_proposal(self, state, parsed):
        require(state["initialized"] == 1, "NOT_INITIALIZED")
        require(state["active"] is None, "PENDING_EXECUTION")
        require(state["grants"] < 64, "GRANT_QUOTA")
        after = {}
        for key, maximum in (("requests", MAX_REQUESTS), ("stages", MAX_STAGES), ("reserved_bytes", MAX_RESERVED)):
            after[key] = self.integer(state["authorized"][key] + parsed["add"][key], 0, maximum,
                                      "AUTHORIZATION_LIMIT:" + key)
        pages = state["metadata_pages"] if parsed["metadata_pages"] is None else parsed["metadata_pages"]
        require(pages >= state["metadata_pages"], "METADATA_CAP_DECREASE")
        require(any(parsed["add"].values()) or pages > state["metadata_pages"], "GRANT_NO_INCREASE")
        return after, pages

    def renew(self, raw, parsed_grant):
        self._writable()
        parsed = parse_grant(raw, self.config_id)
        require(encode(parsed) == encode(parsed_grant), "PARSED_GRANT_BINDING")
        self.event["renewal_historical"] = False
        self.event["renewal_state_outcome"] = "UNCHANGED_BY_RENEWAL"
        prior = self._grant_prior(raw, parsed)
        if prior is not None:
            self.event["renewal_historical"] = True
            self.event["renewal_state_outcome"] = "ORIGINAL_GRANT_RESPONSE_REPLAYED"
            return prior
        state = self.authorization_state()
        after, pages = self._grant_proposal(state, parsed)
        self.event["renewal_physical_supply"] = physical_supply(
            self.root, self.scratch, after["reserved_bytes"] - state["used"]["reserved_bytes"], pages)
        response = encode({"status": "OK", "grant_id": parsed["grant_id"], "sequence": state["grants"] + 1,
            "config": self.config_id, "authorized_before": state["authorized"], "authorized_after": after,
            "metadata_cap_before": {"pages": state["metadata_pages"], "bytes": state["metadata_pages"] * 4096},
            "metadata_cap_after": {"pages": pages, "bytes": pages * 4096}, "used_at_commit": state["used"],
            "mathematicalAcceptance": False, "refund": False,
            "grant_recorded": True, "state_outcome": "RENEWAL_COMMITTED"})
        require(len(response) <= 4096, "GRANT_RESPONSE_BOUND")
        with self._transaction(pages, "administrative"):
            require(self._grant_prior(raw, parsed) is None, "GRANT_CHANGED")
            current = self.authorization_state()
            require(encode(current) == encode(state), "AUTHORIZATION_CHANGED")
            repeated_after, repeated_pages = self._grant_proposal(current, parsed)
            require(encode(repeated_after) == encode(after) and repeated_pages == pages, "GRANT_PROPOSAL_CHANGED")
            self.exec("grant_insert", "INSERT INTO owner_grants VALUES(?,?,?,?)",
                      (parsed["grant_id"], state["grants"] + 1, raw, response))
            self.exec("grant_authorize",
                      "UPDATE authorization SET requests=?,stages=?,reserved_bytes=?,metadata_pages=?,grants=? WHERE id=1",
                      (after["requests"], after["stages"], after["reserved_bytes"], pages, state["grants"] + 1))
            require(dict(self.meta()) == dict(config=self.config_id, id=1, initialized=state["initialized"],
                    requests=state["used"]["requests"], stages=state["used"]["stages"],
                    charged=state["used"]["reserved_bytes"], active=state["active"]), "RENEWAL_CHANGED_USAGE")
        self.event["renewal_state_outcome"] = "RENEWAL_COMMITTED"
        return response

    def put_record(self, kind, client, data):
        raw = encode({"config": self.config_id, "kind": kind, "client": client, "data": data})
        require(len(raw) <= 2 * MIB, "RECORD_LIMIT")
        handle = kind + ":" + digest(raw)
        self.exec("record_insert", "INSERT OR IGNORE INTO records VALUES(?,?,?,?)", (handle, kind, client, raw))
        return handle

    def record(self, handle, kind, client):
        require(type(handle) is str and len(handle) <= 96 and handle.startswith(kind + ":"), "HANDLE_KIND")
        rows = self.rows("record", "SELECT kind,client,raw FROM records WHERE handle=?", (handle,))
        require(rows, "UNKNOWN_HANDLE")
        row = rows[0]
        require(row["client"] == client, "WRONG_CLIENT_HANDLE")
        raw = bytes(row["raw"])
        require(row["kind"] == kind and handle == kind + ":" + digest(raw), "RECORD_BINDING")
        value = decode(raw)
        require(value["config"] == self.config_id and value["client"] == client and value["kind"] == kind, "RECORD_BINDING")
        return value["data"]

    def head(self, client):
        rows = self.rows("head", "SELECT context FROM heads WHERE client=?", (client,))
        require(rows, "UNKNOWN_CLIENT")
        return rows[0][0]

    def set_head(self, client, context):
        self.exec("head_set", "INSERT INTO heads VALUES(?,?) ON CONFLICT(client) DO UPDATE SET context=excluded.context", (client, context))

    def snapshot(self, provider, cut):
        raw = encode({"config": self.config_id, "provider": provider, "cut": cut, "order": "append-sequence-v1"})
        handle = "snapshot:" + digest(raw)
        self.exec("snapshot_insert", "INSERT OR IGNORE INTO snapshots VALUES(?,?,?,?)", (handle, provider, cut, raw))
        self.exec("provider_set", "INSERT INTO providers VALUES(?,?,?) ON CONFLICT(provider) DO UPDATE SET cut=excluded.cut,snapshot=excluded.snapshot", (provider, cut, handle))
        return handle

    def current(self, provider):
        rows = self.rows("provider", "SELECT cut,snapshot FROM providers WHERE provider=?", (provider,))
        require(rows, "UNKNOWN_PROVIDER")
        return rows[0]

    def cut(self, handle):
        require(type(handle) is str and len(handle) <= 96, "SNAPSHOT_HANDLE")
        rows = self.rows("snapshot", "SELECT provider,cut,raw FROM snapshots WHERE handle=?", (handle,))
        require(rows, "UNKNOWN_SNAPSHOT")
        row = rows[0]
        raw = bytes(row["raw"])
        require(handle == "snapshot:" + digest(raw), "SNAPSHOT_BINDING")
        value = decode(raw)
        require(value["config"] == self.config_id and value["provider"] == row["provider"] and value["cut"] == row["cut"], "SNAPSHOT_BINDING")
        return value

    def entry(self, provider, sequence):
        rows = self.rows("entry", "SELECT raw FROM entries WHERE provider=? AND seq=?", (provider, sequence))
        require(rows, "UNKNOWN_ENTRY")
        return decode(bytes(rows[0][0]))

    def descriptor(self, provider, descriptor_id):
        """One indexed exact lookup; caller separately validates selected bytes."""
        key = digest(encode(descriptor_id))
        rows = self.rows("descriptor_lookup", "SELECT seq,raw FROM entries WHERE provider=? AND descriptor_key=?",
                         (provider, key))
        if not rows:
            return None
        offer = decode(bytes(rows[0]["raw"]))
        require(encode(offer["descriptor_id"]) == encode(descriptor_id), "DESCRIPTOR_BINDING")
        return rows[0]["seq"], offer

    def publication_data(self, provider, sequence, descriptor_id):
        require(provider == "P1" and type(sequence) is int and sequence > 0, "PUBLICATION_ENTRY")
        return {"provider": provider, "sequence": sequence, "descriptor_id": descriptor_id}

    def mark_published(self, provider, sequence, descriptor_id):
        """Called only inside the checked local publish visibility transaction."""
        data = self.publication_data(provider, sequence, descriptor_id)
        return self.put_record("publication", "owner", data)

    def require_published(self, provider, sequence, descriptor_id):
        data = self.publication_data(provider, sequence, descriptor_id)
        raw = encode({"config": self.config_id, "kind": "publication", "client": "owner", "data": data})
        handle = "publication:" + digest(raw)
        rows = self.rows("publication", "SELECT handle FROM records WHERE handle=?", (handle,))
        require(rows, "NOT_LOCALLY_PUBLISHED")
        require(encode(self.record(handle, "publication", "owner")) == encode(data), "PUBLICATION_BINDING")
        return handle

    def append(self, provider, offer):
        key = digest(encode(offer["descriptor_id"]))
        present = self.rows("descriptor", "SELECT seq,raw FROM entries WHERE provider=? AND descriptor_key=?", (provider, key))
        if present:
            require(decode(bytes(present[0]["raw"])) == offer, "DESCRIPTOR_CONFLICT")
            return self.current(provider)["snapshot"], present[0]["seq"], True
        sequence = self.current(provider)["cut"] + 1
        require(sequence <= self.limits["entries"], "ENTRY_QUOTA")
        raw = encode(offer)
        require(len(raw) <= 32768, "ENTRY_LIMIT")
        self.exec("entry_insert", "INSERT INTO entries VALUES(?,?,?,?)", (provider, sequence, key, raw))
        return self.snapshot(provider, sequence), sequence, False

    def page(self, provider, first, cut, limit):
        rows = self.rows("range", "SELECT seq,raw FROM entries WHERE provider=? AND seq>=? AND seq<=? ORDER BY seq LIMIT ?",
                         (provider, first, cut, limit), maximum=limit)
        self.event["fetched_sequences"].extend(row["seq"] for row in rows)
        return [(row["seq"], decode(bytes(row["raw"]))) for row in rows]

"""Finite durable reservations under one already locked exact Workspace."""
from copy import deepcopy
import secrets
import sqlite3

from client.workspace_evidence import Workspace, CONCLUSION_FINGERPRINT_SCHEMA
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from modules import codec as C
from . import codec as P

PHASES = frozenset(("RESERVED", "PULLING", "CUSTODIED", "INDEXED", "RECEIPT_COMMITTED",
                    "INCOMPLETE", "RECONCILING", "RECOVERY_INCOMPLETE"))


class PlacementLedger:
    """No token/row is live execution authority; the controller supplies guards."""
    @classmethod
    def open(cls, workspace, config, *, create=False):
        F.need(type(workspace) is Workspace, "PLACEMENT_EXACT_WORKSPACE")
        workspace._active()
        F.need(workspace.config["schema"] == CONCLUSION_FINGERPRINT_SCHEMA,
               "PLACEMENT_FINGERPRINT_WORKSPACE")
        cfg = P.config(config)
        F.need((cfg["namespace"], cfg["wire_profile_id"]) ==
               (workspace.adapter.namespace, workspace.packets.profile_id), "PLACEMENT_WORKSPACE_DOMAIN")
        self = cls.__new__(cls)
        previous = getattr(workspace,"_placement_ledger",None)
        F.need(previous is None or previous.closed,"PLACEMENT_LEDGER_ALREADY_OPEN")
        self.workspace, self._workspace = workspace, workspace
        self.config, self._config_raw = cfg, F.compact(cfg)
        self._roles = workspace.adapter, workspace.modules, workspace.packets, workspace.index, workspace._lock
        self.db, self.closed, self.runtime_id = None, False, None
        path = ordinary(workspace.root/"placement.sqlite", fresh=create, directory=False)
        self._path = path
        self.db = sqlite3.connect(path, timeout=1, isolation_level=None)
        workspace._placement_ledger = self
        try:
            self.db.execute("PRAGMA journal_mode=DELETE"); self.db.execute("PRAGMA synchronous=FULL")
            self.db.execute("PRAGMA foreign_keys=ON"); self.db.execute("PRAGMA temp_store=MEMORY")
            self.db.execute("PRAGMA mmap_size=0"); self.db.execute("PRAGMA cache_size=-1024")
            F.need(self.db.execute("PRAGMA max_page_count="+str(cfg["ledger_pages"])).fetchone()[0]
                   == cfg["ledger_pages"], "PLACEMENT_LEDGER_PAGE_CAP")
            if create:
                self.db.executescript("""
                    BEGIN IMMEDIATE;
                    CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), config BLOB NOT NULL,
                        state TEXT NOT NULL, runs INTEGER NOT NULL, used BLOB NOT NULL);
                    CREATE TABLE grants(id TEXT PRIMARY KEY, runtime TEXT NOT NULL, policy BLOB NOT NULL,
                        used BLOB NOT NULL) WITHOUT ROWID;
                    CREATE TABLE requests(id TEXT PRIMARY KEY, grant_id TEXT NOT NULL, manifest BLOB NOT NULL,
                        reservation BLOB NOT NULL, phase TEXT NOT NULL, recovery_used INTEGER NOT NULL,
                        outcome BLOB, FOREIGN KEY(grant_id) REFERENCES grants(id)) WITHOUT ROWID;
                    CREATE TABLE cells(id TEXT PRIMARY KEY, phase TEXT NOT NULL) WITHOUT ROWID;
                    COMMIT;
                """)
                self.db.execute("INSERT INTO meta VALUES(1,?,'OPEN',0,?)",
                                (self._config_raw, F.compact({key: 0 for key in P.RESOURCES})))
            row = self.db.execute("SELECT config FROM meta WHERE id=1").fetchone()
            F.need(row is not None and bytes(row[0]) == self._config_raw, "PLACEMENT_LEDGER_CONFIG")
            self.active()
            return self
        except BaseException:
            self.close(); raise

    def active(self):
        w = self._workspace
        F.need(not self.closed and self.db is not None and self.workspace is w,
               "PLACEMENT_LEDGER_CLOSED_OR_OWNER")
        w._active()
        F.need(w._lock is not None and not w._lock.closed and getattr(w,"_placement_ledger",None) is self
               and all(actual is original for actual,original in
                       zip((w.adapter,w.modules,w.packets,w.index,w._lock),self._roles))
               and w._client is None and not w._grants,
               "PLACEMENT_WORKSPACE_LOCK_OR_COMPETING_OPERATION")
        F.need(F.compact(self.config) == self._config_raw, "PLACEMENT_CONFIG_CHANGED")
        row = self.db.execute("SELECT config FROM meta WHERE id=1").fetchone()
        F.need(row is not None and bytes(row[0]) == self._config_raw, "PLACEMENT_DURABLE_CONFIG_CHANGED")

    def _transaction(self, function, guard):
        self.active(); guard()
        self.db.execute("BEGIN IMMEDIATE")
        try:
            result = function()
            guard(); self.db.execute("COMMIT")
            return result
        except BaseException:
            if self.db.in_transaction: self.db.execute("ROLLBACK")
            raise

    def start_run(self, identifier, guard):
        F.hexid(identifier)
        F.need(self.runtime_id is None, "PLACEMENT_RUNTIME_ALREADY_ISSUED")
        def commit():
            row = self.db.execute("SELECT runs FROM meta WHERE id=1").fetchone()
            F.need(row[0] < self.config["max_runs"], "PLACEMENT_RUNTIME_CAP")
            self.db.execute("UPDATE meta SET runs=runs+1 WHERE id=1")
        self._transaction(commit, guard)
        self.runtime_id = identifier

    def issue(self, policy, guard):
        self.active(); F.need(self.runtime_id is not None, "PLACEMENT_NO_RUNTIME")
        token = secrets.token_hex(32); identifier = P.digest(token.encode("ascii"))
        raw = F.compact(policy)
        F.need(len(raw) <= P.REQUEST_MAX, "PLACEMENT_GRANT_BYTES")
        def commit():
            F.need(self.db.execute("SELECT state FROM meta WHERE id=1").fetchone()[0] == "OPEN",
                   "PLACEMENT_GENERATION_SEALED")
            F.need(self.db.execute("SELECT count(*) FROM grants").fetchone()[0] < self.config["max_grants"],
                   "PLACEMENT_GRANT_CAP")
            self.db.execute("INSERT INTO grants VALUES(?,?,?,?)", (identifier,self.runtime_id,raw,
                F.compact({key:0 for key in P.RESOURCES})))
        self._transaction(commit,guard)
        return token,identifier

    def authenticate(self, token):
        self.active()
        F.need(type(token) is str and len(token) == 64
               and all(char in "0123456789abcdef" for char in token), "PLACEMENT_TOKEN_SHAPE")
        identifier = P.digest(token.encode("ascii"))
        row = self.db.execute("SELECT runtime,policy,used FROM grants WHERE id=?",(identifier,)).fetchone()
        F.need(row is not None, "PLACEMENT_UNKNOWN_TOKEN")
        policy = F.strict(bytes(row[1]), P.REQUEST_MAX)
        return identifier,row[0],policy,P.limits(F.strict(bytes(row[2]), P.REQUEST_MAX))

    def request(self, identifier, grant_id=None):
        self.active(); F.hexid(identifier)
        row = self.db.execute("SELECT grant_id,manifest,reservation,phase,recovery_used,outcome "
                              "FROM requests WHERE id=?",(identifier,)).fetchone()
        F.need(row is not None, "PLACEMENT_REQUEST_NOT_FOUND")
        F.need(grant_id is None or row[0] == grant_id, "PLACEMENT_STATUS_GRANT")
        return {"request_id":identifier,"grant_id":row[0],"manifest":bytes(row[1]),
            "reservation":P.limits(F.strict(bytes(row[2]),P.REQUEST_MAX)),"phase":row[3],
            "recovery_used":bool(row[4]),
            "outcome":None if row[5] is None else F.strict(bytes(row[5]),P.OUTCOME_MAX)}

    @staticmethod
    def public(row):
        return {"request_id":row["request_id"],"phase":row["phase"],
                "reservation":deepcopy(row["reservation"]),"recovery_used":row["recovery_used"],
                "outcome":deepcopy(row["outcome"]),"observation_only":True,**P.FLAGS}

    def reserve(self, auth, raw, value, now_ms, index_logical_cap, guard):
        identifier,runtime,policy,unused = auth
        rid = P.request_id(raw,identifier,self.config["generation"])
        # Exact request duplicates are status-only, even after restart/expiry.
        found = self.db.execute("SELECT manifest FROM requests WHERE id=?",(rid,)).fetchone()
        if found is not None:
            F.need(bytes(found[0]) == raw,"PLACEMENT_REQUEST_ID_CONFLICT")
            return self.request(rid,identifier),False
        F.need(runtime == self.runtime_id and now_ms < policy["write_until_ms"],
               "PLACEMENT_TOKEN_STATUS_ONLY")
        F.need(now_ms < self.config["admission_close_ms"]
               and now_ms < value["retention_end_ms"] <= policy["retention_until_ms"],
               "PLACEMENT_ADMISSION_OR_RETENTION_WINDOW")
        def commit():
            state,used_raw = self.db.execute("SELECT state,used FROM meta WHERE id=1").fetchone()
            F.need(state == "OPEN","PLACEMENT_GENERATION_SEALED")
            F.need(self.db.execute("SELECT count(*) FROM requests").fetchone()[0] < self.config["max_requests"],
                   "PLACEMENT_REQUEST_CAP")
            new_cell = self.db.execute("SELECT 1 FROM cells WHERE id=?",(value["cell"],)).fetchone() is None
            if new_cell:
                F.need(self.db.execute("SELECT count(*) FROM cells").fetchone()[0] < self.config["max_cells"],
                       "PLACEMENT_CELL_CAP")
            reservation = P.quote(value,new_cell=new_cell,index_logical_cap=index_logical_cap)
            used = P.limits(F.strict(bytes(used_raw),P.REQUEST_MAX))
            grant_used = P.limits(F.strict(bytes(self.db.execute("SELECT used FROM grants WHERE id=?",
                                         (identifier,)).fetchone()[0]),P.REQUEST_MAX))
            for key,amount in reservation.items():
                F.need(used[key]+amount <= self.config["limits"][key]
                       and grant_used[key]+amount <= policy["limits"][key],"PLACEMENT_RESERVED_CAP:"+key)
                used[key] += amount; grant_used[key] += amount
            self.db.execute("UPDATE meta SET used=? WHERE id=1",(F.compact(used),))
            self.db.execute("UPDATE grants SET used=? WHERE id=?",(F.compact(grant_used),identifier))
            if new_cell: self.db.execute("INSERT INTO cells VALUES(?,'RESERVED')",(value["cell"],))
            self.db.execute("INSERT INTO requests VALUES(?,?,?,?,'RESERVED',0,NULL)",
                            (rid,identifier,raw,F.compact(reservation)))
        self._transaction(commit,guard)
        return self.request(rid,identifier),True

    def phase(self, identifier, phase, guard, outcome=None):
        F.need(phase in PHASES,"PLACEMENT_PHASE")
        raw = None if outcome is None else F.compact(outcome)
        F.need(raw is None or len(raw) <= P.OUTCOME_MAX,"PLACEMENT_OUTCOME_BYTES")
        def commit():
            row = self.request(identifier)
            F.need(row["phase"] != "RECEIPT_COMMITTED","PLACEMENT_ALREADY_COMPLETE")
            self.db.execute("UPDATE requests SET phase=?,outcome=COALESCE(?,outcome) WHERE id=?",
                            (phase,raw,identifier))
        self._transaction(commit,guard)

    def recovery(self, identifier, guard):
        def commit():
            row = self.request(identifier)
            F.need(row["phase"] != "RECEIPT_COMMITTED" and not row["recovery_used"]
                   and row["reservation"]["recovery_passes"] == 1,"PLACEMENT_RECOVERY_EXHAUSTED")
            self.db.execute("UPDATE requests SET recovery_used=1,phase='RECONCILING' WHERE id=?",(identifier,))
        self._transaction(commit,guard)
        return self.request(identifier)

    def finish(self, identifier, outcome, guard):
        raw = F.compact(outcome); F.need(len(raw) <= P.OUTCOME_MAX,"PLACEMENT_OUTCOME_BYTES")
        def commit():
            row = self.request(identifier)
            F.need(row["phase"] == "INDEXED","PLACEMENT_FINISH_PHASE")
            value = P.manifest(row["manifest"],self.config)
            self.db.execute("UPDATE cells SET phase='INTENT_ONLY' WHERE id=?",(value["cell"],))
            self.db.execute("UPDATE requests SET phase='RECEIPT_COMMITTED',outcome=? WHERE id=?",(raw,identifier))
        self._transaction(commit,guard)

    def seal(self, guard):
        self._transaction(lambda:self.db.execute("UPDATE meta SET state='SEALED_SERVING' WHERE id=1"),guard)

    def close(self):
        self.closed = True
        if self.db is not None: self.db.close(); self.db = None
        if getattr(self._workspace,"_placement_ledger",None) is self:
            self._workspace._placement_ledger = None

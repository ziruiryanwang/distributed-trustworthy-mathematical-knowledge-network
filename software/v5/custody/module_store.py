"""Durable, bounded structural custody of module groups and demanded bodies.

No certificates, proof acceptance, source execution, or remote write authority.
Body permissions derive from exact stored descriptors; owner qualifies locals.
"""
from __future__ import annotations

from copy import deepcopy
import sqlite3

from discovery import formal_features as F
from discovery.discovery_store import ordinary

BODY_SCHEMA = "DMKN_MODULE_BODY_V1"
LIMITS = {"modules": (1, 100000), "groups": (1, 1000000), "declarations": (1, 1000000),
          "bodies": (1, 1000000), "logical_bytes": (1024, 2**40), "db_pages": (256, 268435456)}


def permitted_hashes(descriptor):
    if descriptor["kind"] in ("definition", "opaque"): return {descriptor["value_hash"]}
    if descriptor["kind"] == "recursor": return {r["value_hash"] for r in descriptor["meta"]["rules"]}
    return set()


def validate_body(codec, module, name, descriptor, response, expected_hash):
    F.fields(response, ("schema", "module_id", "relative_name", "universes", "body_hash", "expression"))
    F.hexid(module); codec.validate_name(name); F.hexid(expected_hash)
    F.need(response["schema"] == BODY_SCHEMA and response["module_id"] == module
           and codec.name_key(response["relative_name"]) == codec.name_key(name), "BODY_ADDRESS")
    F.need(expected_hash in permitted_hashes(descriptor), "BODY_NOT_COMMITTED_BY_DESCRIPTOR")
    F.need(type(response["universes"]) is int and response["universes"] == descriptor["universes"]
           and response["body_hash"] == expected_hash, "BODY_DESCRIPTOR_BINDING")
    F.need(codec.body_id(response["expression"], response["universes"]) == expected_hash, "BODY_HASH_BINDING")
    return response


class ModuleStore:
    def __init__(self, root, codec, foundation, policy, limits, *, create=False):
        F.fields(limits, LIMITS)
        for k, (lo, hi) in LIMITS.items(): F.uint(limits[k], lo, hi, "CUSTODY_LIMIT:"+k)
        self.codec, self.foundation, self.policy = codec, F.hexid(foundation), F.hexid(policy)
        self.limits, self.db = dict(limits), None
        self.root = ordinary(root, fresh=create)
        if create: self.root.mkdir()
        path = ordinary(self.root / "modules.sqlite", fresh=create, directory=False)
        cfg = {"schema": "DMKN_MODULE_CUSTODY_V1", "foundation": foundation, "policy": policy, "limits": limits}
        self.db = sqlite3.connect(path, timeout=1, isolation_level=None)
        try:
            self.db.execute("PRAGMA journal_mode=DELETE")
            self.db.execute("PRAGMA synchronous=FULL")
            self.db.execute("PRAGMA foreign_keys=ON")
            self.db.execute("PRAGMA temp_store=MEMORY")
            self.db.execute("PRAGMA mmap_size=0")
            self.db.execute("PRAGMA cache_size=-2048")
            F.need(self.db.execute("PRAGMA max_page_count="+str(limits["db_pages"])).fetchone()[0]
                   == limits["db_pages"], "CUSTODY_DATABASE_CAP")
            if create:
                self.db.executescript("""
                    BEGIN IMMEDIATE;
                    CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), cfg BLOB NOT NULL,
                        modules INTEGER NOT NULL, groups INTEGER NOT NULL, declarations INTEGER NOT NULL,
                        bodies INTEGER NOT NULL, logical_bytes INTEGER NOT NULL);
                    CREATE TABLE modules(module TEXT PRIMARY KEY, summary BLOB NOT NULL) WITHOUT ROWID;
                    CREATE TABLE groups(module TEXT NOT NULL, idx INTEGER NOT NULL, opening BLOB NOT NULL,
                        PRIMARY KEY(module,idx), FOREIGN KEY(module) REFERENCES modules(module)) WITHOUT ROWID;
                    CREATE TABLE names(module TEXT NOT NULL, name BLOB NOT NULL, idx INTEGER NOT NULL,
                        PRIMARY KEY(module,name), FOREIGN KEY(module,idx) REFERENCES groups(module,idx)) WITHOUT ROWID;
                    CREATE TABLE bodies(module TEXT NOT NULL, universes INTEGER NOT NULL, hash TEXT NOT NULL,
                        expression BLOB NOT NULL, PRIMARY KEY(module,universes,hash),
                        FOREIGN KEY(module) REFERENCES modules(module)) WITHOUT ROWID;
                    COMMIT;
                """)
                self.db.execute("INSERT INTO meta VALUES(1,?,0,0,0,0,0)", (F.compact(cfg),))
            row = self.db.execute("SELECT cfg FROM meta WHERE id=1").fetchone()
            F.need(row is not None and F.strict(bytes(row[0]), 16384) == cfg, "CUSTODY_CONFIG")
            self.status()
        except BaseException:
            self.close(); raise

    def close(self):
        if self.db is not None: self.db.close(); self.db = None

    def status(self):
        row = self.db.execute("SELECT modules,groups,declarations,bodies,logical_bytes FROM meta WHERE id=1").fetchone()
        F.need(row is not None, "CUSTODY_META")
        counts = dict(zip(("modules", "groups", "declarations", "bodies", "logical_bytes"), row))
        for k, value in counts.items(): F.uint(value, 0, self.limits[k], "CUSTODY_STORED_QUOTA")
        return {"counts": counts, "foundation": self.foundation, "policy": self.policy,
                "mathematical_acceptance": False}

    def _charge(self, **amounts):
        counts = self.status()["counts"]
        for k, value in amounts.items():
            F.need(k in counts and type(value) is int and value >= 0
                   and counts[k]+value <= self.limits[k], "CUSTODY_QUOTA:"+k)
        for k, value in amounts.items(): self.db.execute("UPDATE meta SET "+k+"="+k+"+? WHERE id=1", (value,))

    def put_group(self, module, opening, *, before_commit=None):
        c = self.codec
        group = c.verify_group_opening(module, opening)
        summary = opening["summary"]
        F.need(summary["foundation"] == self.foundation and summary["policy"] == self.policy, "CUSTODY_NAMESPACE")
        raw, summary_raw = c.canonical(opening), c.canonical(summary)
        idx = opening["index"]
        self.db.execute("BEGIN IMMEDIATE")
        try:
            previous = self.db.execute("SELECT opening FROM groups WHERE module=? AND idx=?", (module, idx)).fetchone()
            if previous is not None:
                F.need(bytes(previous[0]) == raw, "CUSTODY_GROUP_CONFLICT")
                if before_commit is not None: before_commit()
                self.db.execute("COMMIT"); return {"new": False, "mathematical_acceptance": False}
            old = self.db.execute("SELECT summary FROM modules WHERE module=?", (module,)).fetchone()
            if old is None:
                self._charge(modules=1, logical_bytes=len(summary_raw))
                self.db.execute("INSERT INTO modules VALUES(?,?)", (module, summary_raw))
            else: F.need(bytes(old[0]) == summary_raw, "CUSTODY_SUMMARY_CONFLICT")
            names = [c.name_key(d["name"]) for d in group["declarations"]]
            self._charge(groups=1, declarations=len(names), logical_bytes=len(raw)+sum(map(len, names)))
            self.db.execute("INSERT INTO groups VALUES(?,?,?)", (module, idx, raw))
            for name in names: self.db.execute("INSERT INTO names VALUES(?,?,?)", (module, name, idx))
            if before_commit is not None: before_commit()
            self.db.execute("COMMIT")
            return {"new": True, "mathematical_acceptance": False}
        except BaseException:
            if self.db.in_transaction: self.db.execute("ROLLBACK")
            raise

    def get_group(self, module, name, group_index=None):
        c = self.codec; F.hexid(module); key = c.name_key(name)
        row = self.db.execute("SELECT idx FROM names WHERE module=? AND name=?", (module, key)).fetchone()
        F.need(row is not None, "CUSTODY_DECLARATION_NOT_FOUND")
        if group_index is not None:
            F.uint(group_index, 0, 4095, "CUSTODY_GROUP_INDEX")
            F.need(row[0] == group_index, "CUSTODY_GROUP_LOCATOR")
        data = self.db.execute("SELECT opening FROM groups WHERE module=? AND idx=?", (module, row[0])).fetchone()
        F.need(data is not None, "CUSTODY_GROUP_MISSING")
        opening = c.parse_json(bytes(data[0])); F.need(c.canonical(opening) == bytes(data[0]), "CUSTODY_GROUP_CANONICAL")
        group = c.verify_group_opening(module, opening)
        selected = [d for d in group["declarations"] if c.name_key(d["name"]) == key]
        F.need(len(selected) == 1 and opening["index"] == row[0], "CUSTODY_NAME_BINDING")
        return opening, selected[0]

    def put_body(self, module, name, response, *, before_commit=None):
        _, descriptor = self.get_group(module, name)
        expected = response.get("body_hash") if type(response) is dict else None
        validate_body(self.codec, module, name, descriptor, response, expected)
        raw = self.codec.canonical(response["expression"])
        key = module, descriptor["universes"], expected
        self.db.execute("BEGIN IMMEDIATE")
        try:
            old = self.db.execute("SELECT expression FROM bodies WHERE module=? AND universes=? AND hash=?", key).fetchone()
            if old is not None: F.need(bytes(old[0]) == raw, "CUSTODY_BODY_CONFLICT")
            else:
                self._charge(bodies=1, logical_bytes=len(raw))
                self.db.execute("INSERT INTO bodies VALUES(?,?,?,?)", (*key, raw))
            if before_commit is not None: before_commit()
            self.db.execute("COMMIT")
            return {"new": old is None, "mathematical_acceptance": False}
        except BaseException:
            if self.db.in_transaction: self.db.execute("ROLLBACK")
            raise

    def get_body(self, module, name, universes, body_hash):
        _, descriptor = self.get_group(module, name)
        F.uint(universes, 0, 256, "CUSTODY_UNIVERSES"); F.hexid(body_hash)
        F.need(universes == descriptor["universes"] and body_hash in permitted_hashes(descriptor), "CUSTODY_BODY_PERMISSION")
        row = self.db.execute("SELECT expression FROM bodies WHERE module=? AND universes=? AND hash=?",
                              (module, universes, body_hash)).fetchone()
        F.need(row is not None, "CUSTODY_BODY_NOT_FOUND")
        expression = self.codec.parse_json(bytes(row[0]))
        F.need(self.codec.canonical(expression) == bytes(row[0]), "CUSTODY_BODY_CANONICAL")
        result = {"schema": BODY_SCHEMA, "module_id": module, "relative_name": deepcopy(name),
                  "universes": universes, "body_hash": body_hash, "expression": expression}
        return validate_body(self.codec, module, name, descriptor, result, body_hash)

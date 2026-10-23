"""Atomic incremental, metadata-only index. Caller adopts the object adapter.

No mathematical acceptance, networking, source execution or implicit custody.
Old snapshot trees remain immutable. Quota refusal replaces unimplemented GC.
"""
from __future__ import annotations

import os
from copy import deepcopy
from functools import wraps
from pathlib import Path
import sqlite3
import stat
import time

from . import authenticated_index as A
from .formal_features import (SCHEMA, EXPORT_SCHEMA, ORDINARY_EXPORT_SCHEMA, MAX_RECORD, compact, fields, hexid, need,
                              record_id, strict, uint, validate_features, validate_record)

LIMITS = {"max_objects": (1, 1000000), "max_postings": (1, 128000000),
          "max_features": (1, 1048576), "max_snapshots": (1, 1000001),
          "max_logical_bytes": (1024, 2**40), "max_db_pages": (256, 268435456)}
STORE_SCHEMA = "DMKN_DISCOVERY_STORE_V2"
MAP_ENCODING = "MAXIMAL_SPARSE_MAP_RUNS_V1"


def _hash_counted(method):
    @wraps(method)
    def invoke(self, *args, **kwargs):
        with A.hash_meter(self._hash_step):
            return method(self, *args, **kwargs)
    return invoke


def ordinary(path, fresh=False, directory=True):
    path = Path(path)
    need(path.is_absolute() and path != Path(path.anchor), "ABSOLUTE_NONROOT_PATH")
    for part in path.parts[1:]:
        need(part not in (".", "..") and not part.endswith((".", " "))
             and not any(ord(c) < 32 or c in ':*?"<>|' for c in part)
             and not (os.name == "nt" and os.path.isreserved(part)), "ORDINARY_PATH")
    start = path.parent if fresh else path
    for part in (start, *start.parents):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "REPARSE_PATH")
    need(start.resolve(strict=True) == start, "CANONICAL_PATH")
    if fresh: need(not os.path.lexists(path) and start.is_dir(), "FRESH_PATH")
    else: need(path.is_dir() if directory else path.is_file(), "PATH_KIND")
    return path


class Store:
    @_hash_counted
    def __init__(self, root, adapter, limits, create=False):
        fields(limits, LIMITS)
        for key, (low, high) in LIMITS.items(): uint(limits[key], low, high, "STORE_LIMIT:"+key)
        self.namespace, self.adapter = hexid(adapter.namespace), adapter
        self.feature_schema = getattr(adapter, "feature_schema", SCHEMA)
        need(self.feature_schema in (SCHEMA, EXPORT_SCHEMA, ORDINARY_EXPORT_SCHEMA), "ADAPTER_FEATURE_SCHEMA")
        self.limits, self.db = dict(limits), None
        self.root = ordinary(root, fresh=create)
        self._budget(30, 500000, 500000)
        if create: self.root.mkdir()
        path = ordinary(self.root / "discovery.sqlite", fresh=create, directory=False)
        self.db = sqlite3.connect(path, timeout=1, isolation_level=None)
        try:
            self.db.execute("PRAGMA journal_mode=DELETE")
            self.db.execute("PRAGMA synchronous=FULL")
            self.db.execute("PRAGMA foreign_keys=ON")
            self.db.execute("PRAGMA temp_store=MEMORY")
            self.db.execute("PRAGMA mmap_size=0")
            self.db.execute("PRAGMA cache_size=-2048")
            cfg = {"schema": STORE_SCHEMA, "map_encoding": MAP_ENCODING,
                   "namespace": self.namespace, "limits": limits}
            if self.feature_schema != SCHEMA: cfg["feature_schema"] = self.feature_schema
            if create:
                need(self.db.execute("PRAGMA max_page_count="+str(limits["max_db_pages"])).fetchone()[0]
                     == limits["max_db_pages"], "DATABASE_CAP")
                self.db.executescript("""
                    BEGIN IMMEDIATE;
                    CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), cfg BLOB NOT NULL,
                        seq INTEGER NOT NULL, maproot TEXT NOT NULL, latest TEXT,
                        objects INTEGER NOT NULL, postings INTEGER NOT NULL, features INTEGER NOT NULL,
                        snapshots INTEGER NOT NULL, logical INTEGER NOT NULL);
                    CREATE TABLE objects(object_id TEXT PRIMARY KEY, record_id TEXT NOT NULL UNIQUE,
                        record BLOB NOT NULL, admitted_seq INTEGER NOT NULL) WITHOUT ROWID;
                    CREATE TABLE postings(feature_id TEXT NOT NULL, partition INTEGER NOT NULL,
                        ordinal INTEGER NOT NULL, object_id TEXT NOT NULL,
                        PRIMARY KEY(feature_id,partition,ordinal), UNIQUE(feature_id,partition,object_id),
                        FOREIGN KEY(object_id) REFERENCES objects(object_id)) WITHOUT ROWID;
                    CREATE TABLE cas_nodes(hash TEXT PRIMARY KEY, encoded BLOB NOT NULL) WITHOUT ROWID;
                    CREATE TABLE feature_heads(feature_id TEXT PRIMARY KEY, feature_root TEXT NOT NULL) WITHOUT ROWID;
                    CREATE TABLE snapshots(snapshot_id TEXT PRIMARY KEY, descriptor BLOB NOT NULL) WITHOUT ROWID;
                    COMMIT;
                """)
                self.db.execute("BEGIN IMMEDIATE")
                try:
                    self.db.execute("INSERT INTO meta VALUES(1,?,0,?,NULL,0,0,0,0,0)",
                                    (compact(cfg), A.map_empty(self.namespace)[0]))
                    self._seal()
                    self.db.execute("COMMIT")
                except BaseException:
                    if self.db.in_transaction: self.db.execute("ROLLBACK")
                    raise
            row = self.db.execute("SELECT cfg FROM meta WHERE id=1").fetchone()
            need(row is not None and strict(bytes(row[0]), 16384) == cfg, "STORE_CONFIG")
            need(self.db.execute("PRAGMA max_page_count="+str(limits["max_db_pages"])).fetchone()[0]
                 == limits["max_db_pages"], "DATABASE_CAP")
            self.status()
        except BaseException:
            self.close(); raise

    def close(self):
        if self.db is not None: self.db.close(); self.db = None

    def _budget(self, seconds, reads, writes=0):
        self.until = time.monotonic() + seconds
        self.read_cap, self.write_cap = reads, writes
        self.hash_cap = 2000000
        self.work = {"node_reads": 0, "node_writes": 0, "new_nodes": 0,
                     "index_hash_steps": 0, "node_selects": 0, "node_cache_hits": 0}
        # Operation-only cache, bounded by both encoded bytes and entry count.
        # Returns are copied so callers cannot mutate later cached evidence.
        self._node_cache, self._cache_bytes = {}, 0

    def _guard(self): need(time.monotonic() < self.until, "DISCOVERY_TIME_EXHAUSTED")

    def _hash_step(self):
        self._guard(); need(self.work["index_hash_steps"] < self.hash_cap, "INDEX_HASH_CAP")
        self.work["index_hash_steps"] += 1

    def _cache(self, key, content, node):
        if key not in self._node_cache and len(self._node_cache) < 512 and self._cache_bytes + len(content) <= 2097152:
            self._node_cache[key] = (content, deepcopy(node)); self._cache_bytes += len(content)

    def _meta(self):
        row = self.db.execute("SELECT seq,maproot,latest,objects,postings,features,snapshots,logical FROM meta WHERE id=1").fetchone()
        need(row is not None, "STORE_META")
        return dict(zip(("seq", "maproot", "latest", "objects", "postings", "features", "snapshots", "logical"), row))

    def status(self):
        value = self._meta()
        for key in ("objects", "postings", "features", "snapshots"):
            uint(value[key], 0, self.limits["max_"+key], "STORED_QUOTA")
        uint(value["logical"], 0, self.limits["max_logical_bytes"], "STORED_LOGICAL_QUOTA")
        hexid(value["maproot"]); hexid(value["latest"])
        return {**value, "namespace": self.namespace, "limits": dict(self.limits),
                "storage_schema": STORE_SCHEMA, "map_encoding": MAP_ENCODING, "mathematical_acceptance": False}

    def _charge(self, amount):
        uint(amount, 0, 1048576, "LOGICAL_CHARGE")
        need(self._meta()["logical"] + amount <= self.limits["max_logical_bytes"], "LOGICAL_BYTE_CAP")
        self.db.execute("UPDATE meta SET logical=logical+? WHERE id=1", (amount,))

    def put_node(self, node):
        self._guard(); need(self.work["node_writes"] < self.write_cap, "NODE_WRITE_CAP")
        self.work["node_writes"] += 1
        key = A.node_hash(node); content = compact(node)
        A.validate_map_storage(self, self.namespace, node)
        need(len(content) <= 4096, "CAS_NODE_BYTES")
        self.work["node_selects"] += 1
        old = self.db.execute("SELECT encoded FROM cas_nodes WHERE hash=?", (key,)).fetchone()
        if old is not None:
            need(bytes(old[0]) == content, "CAS_CONFLICT"); return key
        self._charge(len(content))
        self.db.execute("INSERT INTO cas_nodes VALUES(?,?)", (key, content))
        self.work["new_nodes"] += 1
        self._cache(key, content, node)
        return key

    def get_node(self, key):
        self._guard(); need(self.work["node_reads"] < self.read_cap, "NODE_READ_CAP")
        self.work["node_reads"] += 1
        hexid(key)
        if key in self._node_cache:
            self.work["node_cache_hits"] += 1
            return deepcopy(self._node_cache[key][1])
        self.work["node_selects"] += 1
        row = self.db.execute("SELECT encoded FROM cas_nodes WHERE hash=?", (hexid(key),)).fetchone()
        need(row is not None, "CAS_NODE_MISSING")
        node = strict(bytes(row[0]), 4096)
        need(A.node_hash(node) == key, "CAS_NODE_HASH")
        self._cache(key, bytes(row[0]), node)
        return node

    def _seal(self):
        meta = self._meta()
        need(meta["snapshots"] < self.limits["max_snapshots"], "SNAPSHOT_CAP")
        desc = {"schema": "DMKN_FORMAL_INDEX_SNAPSHOT_V1", "namespace": self.namespace,
                "feature_schema": self.feature_schema, "partition_bits": 8, "feature_map_root": meta["maproot"],
                "local_cut": meta["seq"], "previous_snapshot": meta["latest"],
                "coverage_claim": "PROVIDER_SELECTED_FEATURE_RECORDS_NOT_GLOBAL_CORPUS"}
        key, content = A.snapshot_id(desc), compact(desc)
        self._charge(len(content))
        self.db.execute("INSERT INTO snapshots VALUES(?,?)", (key, content))
        self.db.execute("UPDATE meta SET latest=?,snapshots=snapshots+1 WHERE id=1", (key,))
        return key

    def snapshot(self, snapshot_id=None):
        selected = self._meta()["latest"] if snapshot_id is None else hexid(snapshot_id)
        row = self.db.execute("SELECT descriptor FROM snapshots WHERE snapshot_id=?", (selected,)).fetchone()
        need(row is not None, "SNAPSHOT_NOT_RETAINED")
        desc = strict(bytes(row[0]), 4096)
        A.validate_snapshot(desc, self.namespace)
        need(desc["feature_schema"] == self.feature_schema, "SNAPSHOT_FEATURE_SCHEMA")
        need(A.snapshot_id(desc) == selected, "SNAPSHOT_HASH")
        return desc

    @_hash_counted
    def admit(self, raw, expected_id=None):
        self._budget(30, 500000, 500000)
        record = validate_record(self.adapter.extract(raw, expected_id=expected_id), self.namespace)
        need(type(raw) is bytes and record["object_bytes"] == len(raw), "ADAPTER_BYTE_BINDING")
        import hashlib
        need(record["object_sha256"] == hashlib.sha256(raw).hexdigest(), "ADAPTER_HASH_BINDING")
        if expected_id is not None: need(record["object_id"] == hexid(expected_id), "ADAPTER_ID_BINDING")
        rid, content = record_id(record), compact(record)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            old = self.db.execute("SELECT record_id,record FROM objects WHERE object_id=?", (record["object_id"],)).fetchone()
            if old is not None:
                need(old[0] == rid and bytes(old[1]) == content, "OBJECT_RECORD_CONFLICT")
                result = {"new": False, "record": record, "record_id": rid,
                          "snapshot_id": self._meta()["latest"], "mathematical_acceptance": False}
                self._guard(); self.db.execute("COMMIT"); return {**result, "charged": dict(self.work)}
            meta = self._meta()
            need(meta["objects"] < self.limits["max_objects"], "OBJECT_CAP")
            need(meta["postings"] + len(record["features"]) <= self.limits["max_postings"], "POSTING_CAP")
            self._charge(len(content))
            self.db.execute("INSERT INTO objects VALUES(?,?,?,?)", (record["object_id"], rid, content, meta["seq"]+1))
            root = meta["maproot"]; partition = int(record["object_id"][:2], 16)
            for feature in record["features"]:
                self._guard()
                def update(old_root):
                    if old_root is None:
                        need(self._meta()["features"] < self.limits["max_features"], "FEATURE_CAP")
                        old_root = A.partition_empty()[8]
                        self.db.execute("INSERT INTO feature_heads VALUES(?,?)", (feature, old_root))
                        self.db.execute("UPDATE meta SET features=features+1 WHERE id=1")
                    desc, _ = A.partition_get(self, self.namespace, feature, old_root, partition)
                    ctx = A.context(self.namespace, feature, partition)
                    updated = A.append_vector(self, ctx, desc["count"], desc["tree_root"], rid)
                    self.db.execute("INSERT INTO postings VALUES(?,?,?,?)", (feature, partition, desc["count"], record["object_id"]))
                    new_desc = {"partition": partition, "count": desc["count"]+1, "tree_root": updated}
                    new_root = A.partition_set(self, self.namespace, feature, old_root, new_desc)
                    self.db.execute("UPDATE feature_heads SET feature_root=? WHERE feature_id=?", (new_root, feature))
                    return new_root
                root = A.map_update(self, self.namespace, root, feature, update)
            self.db.execute("UPDATE meta SET seq=seq+1,maproot=?,objects=objects+1,postings=postings+? WHERE id=1",
                            (root, len(record["features"])))
            selected = self._seal(); self._guard()
            self.db.execute("COMMIT")
            return {"new": True, "record": record, "record_id": rid, "snapshot_id": selected,
                    "charged": dict(self.work), "mathematical_acceptance": False}
        except BaseException:
            if self.db.in_transaction: self.db.execute("ROLLBACK")
            self._node_cache.clear(); self._cache_bytes = 0
            raise

    @_hash_counted
    def summary(self, snapshot_id, feature_ids, max_bytes=1048576):
        validate_features(feature_ids, 8); uint(max_bytes, 1024, 1048576, "SUMMARY_BYTE_CAP")
        self._budget(5, 30000)
        desc = self.snapshot(snapshot_id); rows = []
        for feature in feature_ids:
            root, proof = A.map_get(self, self.namespace, desc["feature_map_root"], feature)
            partitions = None if root is None else [A.partition_get(self, self.namespace, feature, root, p)[0] for p in range(256)]
            rows.append({"feature_id": feature, "partitions": partitions, "siblings": proof})
        result = {"schema": "DMKN_FORMAL_QUERY_SUMMARY_V1", "namespace": self.namespace,
                  "snapshot_id": snapshot_id, "snapshot": desc, "features": feature_ids, "rows": rows,
                  "coverage": "COMMITTED_METADATA_NOT_SOURCE_CORPUS", "mathematical_acceptance": False}
        self._guard(); need(len(compact(result)) <= max_bytes, "SUMMARY_BYTES_EXHAUSTED")
        return result

    def _record(self, rid):
        row = self.db.execute("SELECT record FROM objects WHERE record_id=?", (rid,)).fetchone()
        need(row is not None, "RECORD_MISSING")
        value = validate_record(strict(bytes(row[0]), MAX_RECORD), self.namespace)
        need(record_id(value) == rid, "RECORD_HASH")
        return value

    @_hash_counted
    def page(self, request):
        from .discovery_query import validate_request, query_id, cursor
        validate_request(request, self.namespace)
        limits = request["limits"]
        self._budget(limits["timeout_ms"]/1000, limits["node_reads"])
        desc = self.snapshot(request["snapshot_id"]); choices = []
        for feature in request["features"]:
            root, _ = A.map_get(self, self.namespace, desc["feature_map_root"], feature)
            part = A.empty_descriptor(self.namespace, feature, request["partition"]) if root is None else A.partition_get(
                self, self.namespace, feature, root, request["partition"])[0]
            choices.append((part["count"], feature, part))
        count, anchor, part = min(choices, key=lambda row: (row[0], row[1]))
        need(request["anchor"] == anchor, "QUERY_ANCHOR")
        uint(request["start"], 0, count, "QUERY_START")
        result = {"schema": "DMKN_FORMAL_QUERY_PAGE_V1", "namespace": self.namespace,
                  "snapshot_id": request["snapshot_id"], "query_id": query_id(self.namespace, request["features"]),
                  "partition": request["partition"], "anchor": anchor, "start": request["start"],
                  "next": request["start"], "anchor_count": count, "examined": [], "match_ordinals": [],
                  "next_cursor": None, "termination": "anchor_exhausted", "charged": {},
                  "coverage": "COMMITTED_ANCHOR_INTERVAL_ONLY", "mathematical_acceptance": False}
        wanted = set(request["features"]); ctx = A.context(self.namespace, anchor, request["partition"])
        def finalize(value, reason):
            value["termination"] = reason
            value["next_cursor"] = None if value["next"] == count else cursor(request, value["next"])
            value["charged"] = {"node_reads": self.work["node_reads"], "examined": len(value["examined"])}
            return value
        while result["next"] < count:
            if len(result["examined"]) >= limits["examined"]: finalize(result, "examined_exhausted"); break
            if len(result["match_ordinals"]) >= limits["matches"]: finalize(result, "matches_exhausted"); break
            try:
                self._guard(); index = result["next"]
                rid, proof = A.vector_get(self, ctx, count, part["tree_root"], index)
                record = self._record(rid)
                need(anchor in record["features"] and int(record["object_id"][:2],16) == request["partition"], "POSTING_RECORD_BINDING")
                matches = wanted <= set(record["features"])
                row = {"ordinal": index, "record": record, "siblings": proof}
                proposed = {**result, "next": index+1, "examined": [*result["examined"], row],
                            "match_ordinals": [*result["match_ordinals"], *([index] if matches else [])]}
                finalize(proposed, "anchor_exhausted" if index+1 == count else "page_continuation")
                if len(compact(proposed)) > limits["bytes"]:
                    need(result["examined"], "PAGE_TOO_SMALL")
                    finalize(result, "bytes_exhausted"); break
                self._guard(); result = proposed
            except ValueError as error:
                if str(error) not in ("DISCOVERY_TIME_EXHAUSTED", "NODE_READ_CAP", "INDEX_HASH_CAP"): raise
                finalize(result, "time_exhausted" if str(error) == "DISCOVERY_TIME_EXHAUSTED" else "work_exhausted"); break
        finalize(result, result["termination"])
        need(len(compact(result)) <= limits["bytes"], "PAGE_TOO_SMALL")
        return result

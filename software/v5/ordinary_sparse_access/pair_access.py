"""Optional owner-selected physical pair index; never discovery authority.

Auxiliary rows share the Store transaction and database. No migration, repair,
backfill, independent commit or remote configuration is performed here. Readiness
checks validate bounded metadata, not completeness of unvisited cache rows.
"""
from copy import deepcopy

from . import authenticated_index as A
from . import formal_features as F

STORE_SCHEMA = "DMKN_DISCOVERY_STORE_V3"
LIMITS = {"max_rows": (1, 16000000), "max_logical_bytes": (1024, 2**40)}


def validate_config(value):
    F.fields(value, ("pairs", "limits"))
    pairs = value["pairs"]
    F.need(type(pairs) is list and 1 <= len(pairs) <= 8, "ACCESS_PAIR_COUNT")
    ordered = []
    for pair in pairs:
        F.need(type(pair) is list and len(pair) == 2, "ACCESS_PAIR_SHAPE")
        left, right = map(F.hexid, pair)
        F.need(left < right, "ACCESS_PAIR_ORDER")
        ordered.append((left, right))
    F.need(ordered == sorted(set(ordered)), "ACCESS_PAIRS_ORDER")
    F.fields(value["limits"], LIMITS)
    for key, (low, high) in LIMITS.items():
        F.uint(value["limits"][key], low, high, "ACCESS_LIMIT:"+key)
    F.need(len(F.compact(value)) <= 4096, "ACCESS_CONFIG_BYTES")
    return deepcopy(value)


def _one(store, sql, args=()):
    store._guard()
    statement = store.db.execute(sql, args)
    try:
        row = statement.fetchone()
        store._guard()
        return row
    finally:
        statement.close()


def _state(store, config, one, guard):
    guard()
    config = validate_config(config)
    base = one("SELECT cfg,seq FROM meta WHERE id=1")
    F.need(base is not None, "ACCESS_BASE_META")
    persisted = F.strict(bytes(base[0]), 16384)
    F.need(type(persisted) is dict and persisted.get("schema") == STORE_SCHEMA and
           persisted.get("namespace") == store.namespace, "ACCESS_CONFIG_BINDING")
    # JSON true compares equal to integer one in Python mappings. Validate the
    # stored config independently before exact equality with the owner config.
    stored_config = validate_config(persisted.get("access_pairs"))
    F.need(stored_config == config, "ACCESS_CONFIG_BINDING")
    seq = F.uint(base[1], 0, store.limits["max_objects"], "ACCESS_BASE_SEQUENCE")
    row = one("SELECT completed_seq,oriented_rows,logical_bytes FROM access_meta WHERE id=1")
    F.need(row is not None, "ACCESS_META_MISSING")
    completed = F.uint(row[0], 0, store.limits["max_objects"], "ACCESS_SEQUENCE")
    rows = F.uint(row[1], 0, config["limits"]["max_rows"], "ACCESS_STORED_ROWS")
    logical = F.uint(row[2], len(F.compact(config)),
                     config["limits"]["max_logical_bytes"], "ACCESS_STORED_BYTES")
    F.need(completed == seq, "ACCESS_NOT_READY")
    F.need(rows % 2 == 0 and rows <= 2*len(config["pairs"])*seq, "ACCESS_STORED_ROW_SHAPE")
    # Resolve the expected table/columns without visiting any cache rows. A
    # dropped table is corruption even when this query has no eligible pair.
    one("SELECT anchor,companion,partition,anchor_ordinal,companion_ordinal,object_id,admitted_seq FROM access_rows LIMIT 0")
    guard()
    return dict(completed_seq=completed, oriented_rows=rows, logical_bytes=logical)


def create(store, config):
    config = validate_config(config)
    F.need(store.db.in_transaction and store._meta()["seq"] == 0 and
           store._meta()["objects"] == 0, "ACCESS_FRESH_TRANSACTION")
    store._guard()
    # execute(), not executescript(): no implicit commit of the caller's txn.
    store.db.execute("""CREATE TABLE access_rows(
        anchor TEXT NOT NULL, companion TEXT NOT NULL,
        partition INTEGER NOT NULL CHECK(partition BETWEEN 0 AND 255),
        anchor_ordinal INTEGER NOT NULL CHECK(anchor_ordinal BETWEEN 0 AND 1048575),
        companion_ordinal INTEGER NOT NULL CHECK(companion_ordinal BETWEEN 0 AND 1048575),
        object_id TEXT NOT NULL,
        admitted_seq INTEGER NOT NULL CHECK(admitted_seq BETWEEN 1 AND 1000000),
        PRIMARY KEY(anchor,companion,partition,anchor_ordinal),
        FOREIGN KEY(object_id) REFERENCES objects(object_id),
        CHECK(anchor<>companion)) WITHOUT ROWID""")
    store._guard()
    store.db.execute("""CREATE TABLE access_meta(
        id INTEGER PRIMARY KEY CHECK(id=1),
        completed_seq INTEGER NOT NULL CHECK(completed_seq BETWEEN 0 AND 1000000),
        oriented_rows INTEGER NOT NULL CHECK(oriented_rows BETWEEN 0 AND 16000000),
        logical_bytes INTEGER NOT NULL CHECK(logical_bytes>=0))""")
    amount = len(F.compact(config))
    F.need(amount <= config["limits"]["max_logical_bytes"], "ACCESS_LOGICAL_BYTE_CAP")
    store.work["access_logical_bytes"] += amount
    store._charge(amount)
    store.db.execute("INSERT INTO access_meta VALUES(1,0,0,?)", (amount,))
    store._guard()


def open_config(store, config):
    return _state(store, config, lambda sql, args=(): _one(store, sql, args), store._guard)


def append(store, record, ordinals, admitted_seq):
    """Append both orientations; caller owns atomic base/access commit."""
    F.need(store.db.in_transaction and store.access_pairs is not None, "ACCESS_APPEND_TRANSACTION")
    config = validate_config(store.access_pairs)
    state = open_config(store, config)
    F.uint(admitted_seq, 1, store.limits["max_objects"], "ACCESS_NEW_SEQUENCE")
    F.need(admitted_seq == state["completed_seq"]+1, "ACCESS_SEQUENCE_STEP")
    features = F.validate_features(record["features"], F.MAX_FEATURES)
    F.need(type(ordinals) is dict and set(ordinals) == set(features), "ACCESS_ORDINAL_KEYS")
    for ordinal in ordinals.values():
        F.uint(ordinal, 0, A.MAX_VECTOR-1, "ACCESS_ORDINAL")
    object_id = F.hexid(record["object_id"])
    partition = int(object_id[:2], 16)
    actual = _one(store, "SELECT admitted_seq FROM objects WHERE object_id=?", (object_id,))
    F.need(actual == (admitted_seq,), "ACCESS_NEW_OBJECT_BINDING")
    rows, logical = state["oriented_rows"], state["logical_bytes"]
    wanted = set(features)
    for left, right in config["pairs"]:
        store._guard()
        store.work["access_checks"] += 1
        if left not in wanted or right not in wanted:
            continue
        for anchor, companion in ((left, right), (right, left)):
            store._guard()
            row = (anchor, companion, partition, ordinals[anchor],
                   ordinals[companion], object_id, admitted_seq)
            amount = len(F.compact(row))
            F.need(rows < config["limits"]["max_rows"], "ACCESS_ROW_CAP")
            F.need(logical+amount <= config["limits"]["max_logical_bytes"], "ACCESS_LOGICAL_BYTE_CAP")
            # Attempt charges survive later SQL/quota/commit rollback in memory.
            store.work["access_inserts"] += 1
            store.work["access_logical_bytes"] += amount
            store._charge(amount)
            store.db.execute("INSERT INTO access_rows VALUES(?,?,?,?,?,?,?)", row)
            rows += 1; logical += amount
    store._guard()
    store.db.execute("UPDATE access_meta SET completed_seq=?,oriented_rows=?,logical_bytes=? WHERE id=1",
                     (admitted_seq, rows, logical))
    store._guard()


def plan(store, features, anchor, io):
    """Meter readiness, then choose a configured original-anchor pair only."""
    io.live()
    F.validate_features(features, 8); F.hexid(anchor)
    F.need(anchor in features, "ACCESS_QUERY_ANCHOR")
    if store.access_pairs is None:
        return None
    config = validate_config(store.access_pairs)
    _state(store, config, io.one, io.live)
    wanted, eligible = set(features), []
    for left, right in config["pairs"]:
        if anchor == left and right in wanted: eligible.append(right)
        elif anchor == right and left in wanted: eligible.append(left)
    io.live()
    return min(eligible) if eligible else None


def next_row(store, anchor, companion, partition, start, stop, io):
    """One metered bounded key-range seek; caller charges scanned beforehand."""
    io.live()
    F.hexid(anchor); F.hexid(companion)
    F.need(anchor != companion and store.access_pairs is not None and
           sorted((anchor, companion)) in store.access_pairs["pairs"], "ACCESS_SELECTED_PAIR")
    F.uint(partition, 0, 255, "ACCESS_PARTITION")
    F.uint(start, 0, A.MAX_VECTOR, "ACCESS_START")
    F.uint(stop, start, A.MAX_VECTOR, "ACCESS_STOP")
    return io.one("""SELECT anchor_ordinal,companion_ordinal,object_id,admitted_seq
        FROM access_rows WHERE anchor=? AND companion=? AND partition=?
          AND anchor_ordinal>=? AND anchor_ordinal<?
        ORDER BY anchor_ordinal LIMIT 1""",
        (anchor, companion, partition, start, stop), probe=True)

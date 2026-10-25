"""Bounded immutable exact-key map; no mathematical or root authority.

The caller owns the SQLite transaction, protected schema and root eligibility.
Keys are previously validated canonical encoded-name bytes, never dotted names.
This module neither opens databases nor commits, rolls back or traverses events.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import sqlite3


_DOMAIN = b"DMKN-GROUNDED-CUT-MAP-V1\0"
_HARD_BYTES = 1024 * 1024
_HEX = frozenset("0123456789abcdef")
_U64 = (1 << 64) - 1
EMPTY_ROOT = hashlib.sha256(_DOMAIN + b"\x00").hexdigest()


class MapError(ValueError):
    """Storage/allowance refusal, never a mathematical validity verdict."""


def _need(condition, code):
    if not condition:
        raise MapError(code)


@dataclass(frozen=True)
class Limits:
    max_key_bytes: int = 16 * 1024
    max_value_bytes: int = 4 * 1024

    def __post_init__(self):
        for value in (self.max_key_bytes, self.max_value_bytes):
            _need(type(value) is int and 1 <= value <= _HARD_BYTES,
                  "CUT_MAP_LIMIT_CONFIGURATION")

    @property
    def max_node_bytes(self):
        return max(99, 9 + self.max_key_bytes + self.max_value_bytes)


DEFAULT_LIMITS = Limits()


@dataclass
class Allowance:
    """Finite caller-chosen logical I/O limits; no automatic replenishment.

    Counters charge issued statements and transferred payload bytes, not SQLite
    physical-page work, CPU or wall time. Enclosing supervision remains required.
    """
    max_reads: int
    max_writes: int
    max_read_bytes: int
    max_write_bytes: int
    reads: int = field(default=0, init=False)
    writes: int = field(default=0, init=False)
    read_bytes: int = field(default=0, init=False)
    write_bytes: int = field(default=0, init=False)

    def __post_init__(self):
        for value in (self.max_reads, self.max_writes,
                      self.max_read_bytes, self.max_write_bytes):
            _need(type(value) is int and 0 <= value <= _U64,
                  "CUT_MAP_ALLOWANCE_CONFIGURATION")

    def _charge(self, counter, amount):
        used, maximum = getattr(self, counter), getattr(self, "max_" + counter)
        _need(type(used) is int and type(maximum) is int and
              0 <= used <= maximum <= _U64 and 0 <= amount <= maximum - used,
              "CUT_MAP_ALLOWANCE_" + counter.upper())
        setattr(self, counter, used + amount)


def _transaction(conn, allowance):
    _need(isinstance(conn, sqlite3.Connection) and conn.in_transaction,
          "CUT_MAP_CALLER_TRANSACTION_REQUIRED")
    _need(type(allowance) is Allowance, "CUT_MAP_ALLOWANCE_CONFIGURATION")


def create_schema(conn, allowance):
    """Create once inside caller BEGIN; an existing table is an explicit error."""
    _transaction(conn, allowance)
    allowance._charge("writes", 1)
    conn.execute("""CREATE TABLE grounded_cut_nodes (
        node_id TEXT PRIMARY KEY COLLATE BINARY NOT NULL
            CHECK(typeof(node_id) = 'text' AND length(node_id) = 64),
        payload BLOB NOT NULL
            CHECK(typeof(payload) = 'blob' AND length(payload) BETWEEN 1 AND 2097161)
    ) WITHOUT ROWID""")


def _root(value):
    _need(type(value) is str and len(value) == 64 and set(value) <= _HEX,
          "CUT_MAP_ROOT_ENCODING")
    return value


def _bytes(value, maximum, code):
    _need(type(value) is bytes and 1 <= len(value) <= maximum, code)
    return value


def _mask(bits):
    return ((1 << bits) - 1) << (256 - bits)


def _digest(raw):
    return hashlib.sha256(_DOMAIN + raw).hexdigest()


def _read_raw(conn, identifier, allowance, limits, *, optional=False):
    """One exact primary-key read, with no oversized payload materialization."""
    allowance._charge("reads", 1)
    available = allowance.max_read_bytes - allowance.read_bytes
    _need(type(available) is int and available >= 0,
          "CUT_MAP_ALLOWANCE_READ_BYTES")
    cap = min(limits.max_node_bytes, available)
    row = conn.execute("""SELECT typeof(payload), length(payload),
        CASE WHEN typeof(payload) = 'blob' AND length(payload) <= ?
             THEN payload ELSE NULL END
        FROM grounded_cut_nodes WHERE node_id = ?""", (cap, identifier)).fetchone()
    if row is None:
        _need(optional, "CUT_MAP_MISSING_NODE")
        return None
    kind, size, raw = row
    _need(kind == "blob" and type(size) is int and
          1 <= size <= limits.max_node_bytes, "CUT_MAP_NODE_BYTE_BOUND")
    _need(size <= available, "CUT_MAP_ALLOWANCE_READ_BYTES")
    _need(type(raw) is bytes and len(raw) == size, "CUT_MAP_NODE_STORAGE")
    allowance._charge("read_bytes", size)
    _need(_digest(raw) == identifier, "CUT_MAP_NODE_HASH")
    return raw


def _decode(raw, limits):
    # Fixed binary encodings have no alternate field orders or integer forms.
    if raw[0] == 1:
        _need(len(raw) >= 9, "CUT_MAP_LEAF_ENCODING")
        key_size = int.from_bytes(raw[1:5], "big")
        _need(1 <= key_size <= limits.max_key_bytes and
              len(raw) >= 9 + key_size, "CUT_MAP_KEY_BYTE_BOUND")
        key = raw[5:5 + key_size]
        value_size = int.from_bytes(raw[5 + key_size:9 + key_size], "big")
        _need(1 <= value_size <= limits.max_value_bytes and
              len(raw) == 9 + key_size + value_size, "CUT_MAP_VALUE_BYTE_BOUND")
        return ("leaf", 256, int.from_bytes(hashlib.sha256(key).digest(), "big"),
                key, raw[9 + key_size:])
    _need(raw[0] == 2 and len(raw) == 99, "CUT_MAP_BRANCH_ENCODING")
    depth = int.from_bytes(raw[1:3], "big")
    prefix = int.from_bytes(raw[3:35], "big")
    left, right = raw[35:67].hex(), raw[67:99].hex()
    _need(depth < 256 and prefix & _mask(depth) == prefix,
          "CUT_MAP_BRANCH_PREFIX")
    _need(left != right and EMPTY_ROOT not in (left, right),
          "CUT_MAP_BRANCH_CHILDREN")
    return ("branch", depth, prefix, left, right)


def _read_node(conn, identifier, allowance, limits, prefix, bits):
    node = _decode(_read_raw(conn, identifier, allowance, limits), limits)
    _need(node[1] >= bits and node[2] & _mask(bits) == prefix,
          "CUT_MAP_CHILD_LINK")
    return node


def _put(conn, raw, allowance, limits):
    _need(0 < len(raw) <= limits.max_node_bytes, "CUT_MAP_NODE_BYTE_BOUND")
    identifier = _digest(raw)
    _need(identifier != EMPTY_ROOT, "CUT_MAP_RESERVED_HASH_COLLISION")
    previous = _read_raw(conn, identifier, allowance, limits, optional=True)
    if previous is not None:
        _need(previous == raw, "CUT_MAP_NODE_HASH_COLLISION")
        return identifier
    allowance._charge("write_bytes", len(raw))
    allowance._charge("writes", 1)
    conn.execute("INSERT INTO grounded_cut_nodes(node_id, payload) VALUES (?, ?)",
                 (identifier, raw))
    return identifier


def _leaf(key, value):
    return (b"\x01" + len(key).to_bytes(4, "big") + key +
            len(value).to_bytes(4, "big") + value)


def _branch(depth, prefix, left, right):
    return (b"\x02" + depth.to_bytes(2, "big") + prefix.to_bytes(32, "big") +
            bytes.fromhex(left) + bytes.fromhex(right))


def _start(conn, root, key, allowance, limits):
    _transaction(conn, allowance)
    _need(type(limits) is Limits, "CUT_MAP_LIMIT_CONFIGURATION")
    _root(root)
    _bytes(key, limits.max_key_bytes, "CUT_MAP_KEY_BYTE_BOUND")
    return int.from_bytes(hashlib.sha256(key).digest(), "big")


def lookup(conn, root, encoded_name, allowance, *, limits=DEFAULT_LIMITS):
    """Return exact opaque value or None; absence is only under this supplied root."""
    key_hash = _start(conn, root, encoded_name, allowance, limits)
    current, prefix, bits = root, 0, 0
    while current != EMPTY_ROOT:
        node = _read_node(conn, current, allowance, limits, prefix, bits)
        kind, depth, path, left, right = node
        if kind == "leaf":
            if path != key_hash:
                return None
            _need(left == encoded_name, "CUT_MAP_KEY_HASH_COLLISION")
            return right
        if key_hash & _mask(depth) != path:
            return None
        bit = (key_hash >> (255 - depth)) & 1
        current = right if bit else left
        prefix, bits = path | bit << (255 - depth), depth + 1
    return None


def insert(conn, root, encoded_name, value, allowance, *, limits=DEFAULT_LIMITS):
    """Path-copy insert, preserving root; exact duplicate is idempotent.

    A differing existing value refuses. Partial new nodes after any failure are
    uncommitted: the controller must roll back its event transaction, not adopt
    a partially returned root. This function never commits or rolls back.
    """
    key_hash = _start(conn, root, encoded_name, allowance, limits)
    _bytes(value, limits.max_value_bytes, "CUT_MAP_VALUE_BYTE_BOUND")

    def visit(current, prefix, bits):
        if current == EMPTY_ROOT:
            return _put(conn, _leaf(encoded_name, value), allowance, limits)
        node = _read_node(conn, current, allowance, limits, prefix, bits)
        kind, depth, path, left, right = node
        mismatch = (key_hash ^ path) & _mask(depth)
        if mismatch:
            split = 256 - mismatch.bit_length()
            _need(bits <= split < depth, "CUT_MAP_SPLIT_LINK")
            added = _put(conn, _leaf(encoded_name, value), allowance, limits)
            bit = (key_hash >> (255 - split)) & 1
            return _put(conn, _branch(split, key_hash & _mask(split),
                                     current if bit else added,
                                     added if bit else current), allowance, limits)
        if kind == "leaf":
            _need(left == encoded_name, "CUT_MAP_KEY_HASH_COLLISION")
            _need(right == value, "CUT_MAP_KEY_ALREADY_BOUND")
            return current
        bit = (key_hash >> (255 - depth)) & 1
        old_child = right if bit else left
        changed = visit(old_child, path | bit << (255 - depth), depth + 1)
        if changed == old_child:
            return current
        return _put(conn, _branch(depth, path, left if bit else changed,
                                 changed if bit else right), allowance, limits)

    return visit(root, 0, 0)

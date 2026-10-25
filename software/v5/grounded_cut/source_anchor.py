"""Conservative LOCAL source-support guard for a future grounded-cut catalog.

SOURCE ONLY, not a deployable admission API. Capture is a paid one-time operation
on a genuinely locked eligible native catalog. A protected destination must bind
the returned bytes to its own accepted bootstrap event. Downloaded anchor bytes
and matching files alone grant no authority. Reopen reads only fixed identity /
withdrawal state; it never restores snapshots, scans operations, or recovers them.

An operational source quarantine deliberately invalidates use here, even when
an earlier theorem might remain true. This first lane performs no support transfer.
Protected OS/storage, approved code and no whole-state rollback remain premises.
"""
from __future__ import annotations

import os
from pathlib import Path
import sqlite3

import ordinary_evidence as E
import ordinary_semantics as S
import portable_catalog as P


SCHEMA = "DMKN_GROUNDED_CUT_NATIVE_SUPPORT_ANCHOR_V1"
MAX_BINDING = 128 * 1024
MAX_MARKER = 32 * 1024
MAX_ACTIVATION = 8 * 1024
FIELDS = {"schema", "directory", "marker_hex", "activation_hex", "store_id",
          "semantic_id", "foundation_id", "implementation_id", "selected_root",
          "retained_support", "max_db_bytes"}


def need(ok, code):
    if not ok:
        raise ValueError("GROUNDED_SOURCE_" + code)


def _raw_hex(value, maximum):
    need(type(value) is str and 0 < len(value) <= 2 * maximum and
         len(value) % 2 == 0 and all(c in "0123456789abcdef" for c in value),
         "ENCODED_IDENTITY")
    return bytes.fromhex(value)


def parse_binding(raw):
    """Validate inert binding syntax; does not establish its derivation event."""
    doc = E.strict_json(raw, E.Limits(max_bytes=MAX_BINDING))
    need(type(doc) is dict and set(doc) == FIELDS and doc["schema"] == SCHEMA,
         "BINDING_FIELDS")
    need(type(doc["directory"]) is str and 0 < len(doc["directory"]) <= 32768,
         "DIRECTORY_SHAPE")
    for key in ("store_id", "semantic_id", "foundation_id", "implementation_id",
                "selected_root"):
        P.hexid(doc[key])
    need(doc["semantic_id"] == S.semantic_id() and
         doc["foundation_id"] == S.foundation_id(), "FOUNDATION")
    support = doc["retained_support"]
    need(type(support) is list and 1 <= len(support) <= 128 and
         support == sorted(set(support)), "SUPPORT_SET")
    for identity in support:
        P.hexid(identity)
    need(type(doc["max_db_bytes"]) is int and
         4096 <= doc["max_db_bytes"] <= 4096 * 1048576, "DATABASE_LIMIT")
    marker = _raw_hex(doc["marker_hex"], MAX_MARKER)
    activation = _raw_hex(doc["activation_hex"], MAX_ACTIVATION)
    marker_doc = E.strict_json(marker, E.Limits(max_bytes=MAX_MARKER))
    activation_doc = E.strict_json(activation, E.Limits(max_bytes=MAX_ACTIVATION))
    need(type(marker_doc) is dict and set(marker_doc) ==
         {"schema", "store_id", "implementation", "limits"} and
         marker_doc["schema"] == P.SCHEMA and
         marker_doc["store_id"] == doc["store_id"], "MARKER_IDENTITY")
    implementation_raw = E.canonical_json(marker_doc["implementation"])
    implementation = S.read_implementation(implementation_raw)
    need(S.implementation_id(implementation_raw) == doc["implementation_id"] and
         implementation["semantic_id"] == doc["semantic_id"] and
         sorted({implementation[key] for key in P.SUPPORT_FIELDS}) == support,
         "IMPLEMENTATION_SUPPORT")
    need(type(marker_doc["limits"]) is dict and
         type(marker_doc["limits"].get("max_db_pages")) is int and
         marker_doc["limits"]["max_db_pages"] * 4096 == doc["max_db_bytes"],
         "MARKER_LIMIT")
    expected_activation = {"schema": P.ACTIVATION_SCHEMA,
        "semantic_id": doc["semantic_id"], "foundation_id": doc["foundation_id"],
        "implementation_id": doc["implementation_id"], "store_id": doc["store_id"],
        "state": "ACTIVE", "origin": "native-bootstrap",
        "basis_root": S.local_root_id(implementation_raw, doc["store_id"], "basis", "",
            P.basis_request_id(doc["semantic_id"], doc["foundation_id"]))}
    need(activation_doc == expected_activation, "NATIVE_BOOTSTRAP_ONLY")
    return doc, marker, activation


def capture(native, selected_root, *, check):
    """Paid migration seam. Caller continues holding native's actual owner lock.

    Returns (canonical binding bytes, validated full context). The context's full
    proof associations must still be used to derive exact summaries; this function
    itself creates no destination, short theorem interface, or accepted event.
    """
    need(type(native) is P.PortableCatalog and callable(check), "LIVE_NATIVE_TYPE")
    check()
    state = native._active()
    need(state["origin"] == "native-bootstrap" and native._lock is not None and
         not native._lock.closed, "LIVE_NATIVE_BOOTSTRAP_REQUIRED")
    context = native.context(P.hexid(selected_root))
    check()
    need(context["local_root"] == selected_root and
         context["implementation_id"] == native.implementation_id,
         "SELECTED_CONTEXT")
    raw = E.canonical_json({"schema": SCHEMA, "directory": str(native._root),
        "marker_hex": native._marker.hex(),
        "activation_hex": native._activation_raw.hex(),
        "store_id": native._store_id, "semantic_id": native.semantic_id,
        "foundation_id": native.foundation_id,
        "implementation_id": native.implementation_id, "selected_root": selected_root,
        "retained_support": context["retained_support"],
        "max_db_bytes": native._limits.max_db_pages * 4096})
    parse_binding(raw)
    native._active()
    check()
    return raw, context


class SourceAnchor:
    """Read-only support guard; caller already authenticated the binding's origin.

    Hold the guard throughout a cut operation. No other native owner can hold the
    same source lock concurrently. After closing, a future guard reacquires it.
    Source relocation/deletion/quarantine deliberately refuses this narrow lane.
    """

    @classmethod
    def open(cls, protected_binding_raw, *, check):
        need(os.name == "nt" and callable(check), "WINDOWS_OWNER_GUARD")
        check()
        doc, marker, activation = parse_binding(protected_binding_raw)
        self = cls.__new__(cls)
        self._closed, self._denied = False, False
        self._lock = self._db = None
        self._doc, self._marker, self._activation = doc, marker, activation
        self._check = check
        self._root = P.ordinary(doc["directory"], directory=True)
        try:
            lock_path = P.ordinary(self._root / "owner.lock")
            need(P.read_bounded(lock_path, 1) == b"\0", "LOCK_FILE")
            import msvcrt
            self._lock = lock_path.open("r+b")
            msvcrt.locking(self._lock.fileno(), msvcrt.LK_NBLCK, 1)
            database = P.ordinary(self._root / "catalog.sqlite")
            need(0 < database.stat().st_size <= doc["max_db_bytes"], "DATABASE_BOUND")
            # Refuse rather than trigger hidden recovery or mutate the source.
            for suffix in ("-wal", "-shm", "-journal"):
                need(not os.path.lexists(str(database) + suffix), "SOURCE_NEEDS_RECOVERY")
            self._db = sqlite3.connect(database.as_uri() + "?mode=ro",
                                      uri=True, isolation_level=None, timeout=1)
            for pragma in ("trusted_schema=OFF", "query_only=ON", "mmap_size=0"):
                self._db.execute("PRAGMA " + pragma)
            self.check()
            return self
        except BaseException:
            self.close()
            raise

    def check(self):
        """Fixed identity/withdrawal check, with no selected-root/history traversal."""
        need(not self._closed and not self._denied, "CLOSED_OR_WITHDRAWN")
        try:
            self._check()
            need(not os.path.lexists(self._root / "WITHDRAWN"), "WITHDRAWN")
            need(P.read_bounded(self._root / "ADOPTION.json", MAX_MARKER) == self._marker,
                 "ADOPTION_CHANGED")
            # Bind lengths before reading identity blobs. This is one primary-key
            # row, not count(*), integrity_check, context(), or operation recovery.
            sizes = self._db.execute(
                "SELECT length(marker),length(activation) FROM meta WHERE id=1").fetchone()
            need(sizes == (len(self._marker), len(self._activation)), "META_SIZE")
            row = self._db.execute("SELECT marker,activation FROM meta WHERE id=1").fetchone()
            need(row == (self._marker, self._activation), "META_IDENTITY_CHANGED")
            self._check()
        except BaseException:
            self._denied = True
            raise

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

    def __enter__(self):
        self.check()
        return self

    def __exit__(self, *_):
        self.close()

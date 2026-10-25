"""Protected LOCAL native support and fixed-basis snapshot binding.

SOURCE ONLY. Capture authenticates a committed fixed-basis operation while the
genuine native owner lock is held. A destination must bind the returned bytes
to its actual derivation event. Matching files or downloaded descriptors confer
no authority. Reopen keeps the predecessor's fixed identity/withdrawal cadence;
it never reconstructs the selected application lineage or scans operations.

Each actual worker event must call basis_snapshot once before unsafe loading and
hold this guard throughout use. Exact artifact hashing authenticates one fixed
snapshot, not peer mathematics. Protected OS/storage, approved native serializer/
loader correspondence, immutable files and no whole-state rollback are premises.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import os
from pathlib import Path
import sqlite3

import ordinary_evidence as E
import ordinary_semantics as S
import portable_catalog as P


SCHEMA = "DMKN_GROUNDED_CUT_NATIVE_SUPPORT_ANCHOR_V2"
MAX_BINDING = 128 * 1024
MAX_MARKER = 32 * 1024
MAX_ACTIVATION = 8 * 1024
MAX_BASIS_BYTES = 1024 * 1024 * 1024
MAX_PATH_BYTES = 32768
HASH_CHUNK = 1024 * 1024
FIELDS = {"schema", "directory", "marker_hex", "activation_hex", "store_id",
          "semantic_id", "foundation_id", "implementation_id", "selected_root",
          "retained_support", "max_db_bytes", "basis"}
BASIS_FIELDS = {"basis_root", "parent_root", "request_hash", "operation_id",
                "record_sha256", "module_name", "parent_module", "relative_path",
                "artifact_path", "artifact_bytes", "artifact_sha256", "names_count",
                "seed_sha256", "inventory_sha256"}


def need(ok, code):
    if not ok:
        raise ValueError("GROUNDED_SOURCE_" + code)


def _raw_hex(value, maximum):
    need(type(value) is str and 0 < len(value) <= 2 * maximum and
         len(value) % 2 == 0 and all(c in "0123456789abcdef" for c in value),
         "ENCODED_IDENTITY")
    return bytes.fromhex(value)


def _basis_binding(doc, marker_doc, activation_doc):
    """Validate descriptor syntax/relations, not its protected capture origin."""
    basis = doc["basis"]
    need(type(basis) is dict and set(basis) == BASIS_FIELDS, "BASIS_FIELDS")
    for key in ("basis_root", "request_hash", "operation_id", "record_sha256",
                "artifact_sha256", "seed_sha256", "inventory_sha256"):
        P.hexid(basis[key])
    need(basis["basis_root"] == activation_doc["basis_root"] and
         basis["parent_root"] == "" and basis["parent_module"] == [] and
         basis["request_hash"] == P.basis_request_id(doc["semantic_id"], doc["foundation_id"]),
         "BASIS_ORIGIN_BINDING")
    need(basis["module_name"] == P.L.module_name(basis["basis_root"]) and
         type(basis["names_count"]) is int and basis["names_count"] == 581 and
         basis["seed_sha256"] == S.SEED and basis["inventory_sha256"] == S.INVENTORY,
         "BASIS_FIXED_PROFILE")
    relative = "operations/" + basis["operation_id"] + "/chunk.olean"
    expected = str(Path(doc["directory"]).joinpath(*relative.split("/")))
    need(basis["relative_path"] == relative and
         type(basis["artifact_path"]) is str and basis["artifact_path"] == expected and
         0 < len(expected.encode("utf-8")) <= MAX_PATH_BYTES,
         "BASIS_ARTIFACT_PATH")
    maximum = marker_doc["limits"].get("max_artifact_bytes")
    need(type(maximum) is int and 0 < maximum <= (1 << 40) and
         type(basis["artifact_bytes"]) is int and
         0 < basis["artifact_bytes"] <= min(maximum, MAX_BASIS_BYTES),
         "BASIS_ARTIFACT_BOUND")


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
    _basis_binding(doc, marker_doc, activation_doc)
    return doc, marker, activation


def capture(native, selected_root, *, check):
    """Paid derivation under the actual native lock; returns (binding, context).

    Explicitly authenticate the committed basis row/operation, not a caller path
    or an extension snapshot. The full selected context still supplies the proof
    associations used by the caller's separately authenticated cut derivation.
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
    basis_root = P.hexid(state["basis_root"])
    basis_raw, basis_row = native._root_row(basis_root)
    need(basis_row.get("kind") == "basis" and basis_row.get("origin") == "native-check" and
         basis_row.get("parent_root") == "" and basis_row.get("input_unit_ids") == [] and
         basis_row.get("request_hash") == P.basis_request_id(native.semantic_id, native.foundation_id),
         "COMMITTED_NATIVE_BASIS_REQUIRED")
    # This checks the real COMMITTED operation/root/size, exact record origin,
    # implementation, generated path and artifact binding under the held lock.
    artifact = native._validate_record(basis_raw, basis_row, None, {})
    check()
    snapshot = basis_row["snapshot"]
    need(snapshot["parent_module"] == [] and snapshot["writer_origin"] == "native-check" and
         context["basis_root"] == basis_root and
         context["basis_module"] == snapshot["module_name"] and
         len(basis_row["bindings"]) == 581, "BASIS_CONTEXT_IDENTITY")
    expected_first = {"module_name": snapshot["module_name"], "path": str(artifact),
        "parent_module": [], "artifact_bytes": snapshot["artifact_bytes"], "names_count": 581}
    need(context["modules"] and context["modules"][0] == expected_first,
         "BASIS_CONTEXT_FIRST_MODULE")
    basis = {"basis_root": basis_root, "parent_root": "",
        "request_hash": basis_row["request_hash"],
        "operation_id": basis_row["provenance"]["operation_id"],
        "record_sha256": hashlib.sha256(basis_raw).hexdigest(),
        "module_name": deepcopy(snapshot["module_name"]), "parent_module": [],
        "relative_path": snapshot["relative_path"], "artifact_path": str(artifact),
        "artifact_bytes": snapshot["artifact_bytes"],
        "artifact_sha256": snapshot["artifact_sha256"], "names_count": 581,
        "seed_sha256": S.SEED, "inventory_sha256": S.INVENTORY}
    raw = E.canonical_json({"schema": SCHEMA, "directory": str(native._root),
        "marker_hex": native._marker.hex(),
        "activation_hex": native._activation_raw.hex(),
        "store_id": native._store_id, "semantic_id": native.semantic_id,
        "foundation_id": native.foundation_id,
        "implementation_id": native.implementation_id, "selected_root": selected_root,
        "retained_support": context["retained_support"],
        "max_db_bytes": native._limits.max_db_pages * 4096, "basis": basis})
    parse_binding(raw)
    native._active()
    need(native._lock is not None and not native._lock.closed, "NATIVE_LOCK_LOST")
    check()
    return raw, context


class SourceAnchor:
    """Read-only support guard with an internally derived fixed-basis capability.

    Caller authenticates the binding's accepted derivation. Hold this guard and
    its genuine source lock throughout the worker event. Source relocation,
    deletion or quarantine refuses; no state/support transfer is implemented.
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
        """Unchanged identity/withdrawal cadence; no history traversal or hashing."""
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

    def basis_snapshot(self):
        """Authenticate once per worker event; return its exact three-field input.

        The caller charges artifact_bytes and keeps this guard/files immutable
        through native use. No artifact cache survives this invocation. The Lean
        worker independently hardcodes one module, no parent and exactly581 names;
        it still checks restored fixed inventory, not just this file descriptor.
        """
        self.check()
        try:
            need(self._lock is not None and not self._lock.closed, "NATIVE_LOCK_LOST")
            basis = self._doc["basis"]
            path = P.ordinary(self._root.joinpath(*basis["relative_path"].split("/")))
            need(str(path) == basis["artifact_path"], "BASIS_ARTIFACT_PATH")
            size = basis["artifact_bytes"]
            need(path.stat().st_size == size, "BASIS_ARTIFACT_SIZE")
            digest = hashlib.sha256()
            consumed = 0
            with path.open("rb") as stream:
                need(os.fstat(stream.fileno()).st_size == size, "BASIS_ARTIFACT_SIZE")
                while consumed < size:
                    self._check()
                    chunk = stream.read(min(HASH_CHUNK, size - consumed))
                    need(bool(chunk), "BASIS_ARTIFACT_TRUNCATED")
                    consumed += len(chunk)
                    digest.update(chunk)
                self._check()
                need(stream.read(1) == b"" and os.fstat(stream.fileno()).st_size == size,
                     "BASIS_ARTIFACT_CHANGED")
            need(consumed == size and digest.hexdigest() == basis["artifact_sha256"],
                 "BASIS_ARTIFACT_DIGEST")
            need(P.ordinary(path).stat().st_size == size, "BASIS_ARTIFACT_CHANGED")
            self.check()
            return {"module_name": deepcopy(basis["module_name"]),
                    "path": str(path), "artifact_bytes": size}
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

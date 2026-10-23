"""Owner-local V2 catalog; portable IDs do not make snapshots portable warrants.

This is conditional trusted-controller storage, not peer admission. Only an
actual clean pinned worker event permits _commit_checked. Only a separately
reviewed live legacy importer, holding an eligible source's owner lock and
establishing the adopted correspondence, permits _activate_import. Neither
method interprets a saved PASS/compatible flag as authority. This file contains
no worker, legacy-source reader, translation, copying or migration algorithm.

Uses the existing V1 ordinary-path, bounded-read and Windows-lock/DELETE/FULL
patterns without inheriting V1 admission methods. Owner/OS immutability and no
whole-store rollback remain premises. Serialized owner calls only. Native
artifacts remain local acceleration state and never network mathematical evidence.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import math
import os
from pathlib import Path
import platform
import secrets
import sqlite3
import struct
import time

import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as PE
import local_catalog as L

Limits = L.Limits
CatalogError = L.CatalogError
need, hexid, ordinary, read_bounded = L.need, L.hexid, L.ordinary, L.read_bounded
SCHEMA = "DMKN_ORDINARY_LOCAL_CATALOG_V2"
ROOT_SCHEMA = "DMKN_ORDINARY_LOCAL_ROOT_V2"
ACTIVATION_SCHEMA = "DMKN_ORDINARY_LOCAL_ACTIVATION_V2"
IMPORT_SCHEMA = "DMKN_ORDINARY_LOCAL_IMPORT_V2"
SUPPORT_FIELDS = ("kernel_support", "adapter_support", "basis_receiver_support",
                  "controller_support", "snapshot_support")
SOURCE_SUPPORT_FIELDS = ("kernel_support", "adapter_support", "basis_receiver_support")


def fields(value, keys, code):
    need(type(value) is dict and set(value) == set(keys), code)


def uint(value, low, high, code):
    need(type(value) is int and low <= value <= high, code)
    return value


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def basis_request_id(semantic, foundation):
    return L.digest("DMKN-ORDINARY-FIXED-BASIS-REQUEST-V2",
                    [hexid(semantic), hexid(foundation), S.SEED, S.INVENTORY])


def batch_id(identities):
    return L.digest("DMKN-ORDINARY-BATCH-V2", identities)


def _check_parent_deadline(parent_deadline):
    """Optional caller-owned absolute clock; never replenish it during parsing."""
    if parent_deadline is not None:
        need(type(parent_deadline) in (int, float) and math.isfinite(parent_deadline) and
             time.monotonic() < parent_deadline, "CATALOG_PARENT_DEADLINE")


def legacy_root_id(semantic, foundation, store, import_id, source_root, parent):
    if parent:
        hexid(parent)
    else:
        need(parent == "", "PORTABLE_LEGACY_PARENT")
    return L.digest("DMKN-ORDINARY-LEGACY-ROOT-V2", [hexid(semantic),
        hexid(foundation), hexid(store), hexid(import_id), hexid(source_root), parent])


def _supports(values):
    need(type(values) is list and 1 <= len(values) <= 128, "PORTABLE_SUPPORT_BOUND")
    for value in values:
        hexid(value)
    need(values == sorted(set(values)), "PORTABLE_SUPPORT_ORDER")
    return values


class _Grant:
    __slots__ = ("identifier", "directory", "deadline", "root", "parent", "kind",
                 "request_hash", "bindings_raw", "names_count", "input_unit_ids",
                 "module_name_raw", "parent_module_raw", "parent_plan_raw")


class _ImportGrant:
    __slots__ = ("identifier", "directory", "deadline", "output_bytes")


class PortableCatalog:
    """One operational authority, with separately authenticated snapshot origins."""

    @classmethod
    def open(cls, directory, implementation_raw, store_id, *, create=False, limits=Limits()):
        """Open ACTIVE only. IMPORTING never recovers into an accepted context."""
        return cls._open(directory, implementation_raw, store_id, create=create,
                         limits=limits, importing=None)

    @classmethod
    def _create_importing(cls, directory, implementation_raw, store_id, *,
                          limits=Limits(), seconds=120, output_bytes=1024*1024*1024,
                          parent_deadline=None):
        """PRIVATE fresh-destination seam; grants no source eligibility.

        The importer must use a deadline no later than its nonrenewing parent
        allocation. A failed/closed destination is retained quarantine; this API
        deliberately cannot reopen or resume it. No worker grants are available.
        """
        uint(seconds, 1, 3600, "PORTABLE_IMPORT_DEADLINE")
        need(type(limits) is Limits, "PORTABLE_LIMIT_CONFIGURATION")
        uint(output_bytes, 1, limits.max_total_artifact_bytes, "PORTABLE_IMPORT_OUTPUT_BOUND")
        identifier = secrets.token_hex(32)
        deadline = time.monotonic() + seconds
        if parent_deadline is not None:
            need(type(parent_deadline) in (int, float) and math.isfinite(parent_deadline),
                 "PORTABLE_IMPORT_PARENT_DEADLINE")
            deadline = min(deadline, parent_deadline)
        self = cls._open(directory, implementation_raw, store_id, create=True,
                         limits=limits, importing=identifier)
        try:
            grant = _ImportGrant()
            grant.identifier, grant.deadline, grant.output_bytes = identifier, deadline, output_bytes
            grant.directory = self._root / "imports" / identifier
            grant.directory.mkdir()
            self._import_grant = grant
            self._import_binding = tuple(getattr(grant, key) for key in _ImportGrant.__slots__)
            self._import_active(grant)
            return self, grant
        except BaseException:
            self.close()
            raise

    @classmethod
    def _open(cls, directory, implementation_raw, store_id, *, create, limits, importing):
        need(os.name == "nt", "CATALOG_WINDOWS_LOCK_REQUIRED")
        need(type(create) is bool and type(limits) is Limits and type(implementation_raw) is bytes,
             "PORTABLE_CATALOG_CONFIGURATION")
        implementation = S.read_implementation(implementation_raw)
        architecture = {"amd64": "x86_64", "x86_64": "x86_64", "arm64": "aarch64",
                        "aarch64": "aarch64"}.get(platform.machine().lower())
        need(implementation["platform"] == {"os": "windows", "architecture": architecture,
             "word_bits": struct.calcsize("P")*8, "byte_order": "little"}, "PORTABLE_LOCAL_PLATFORM")
        need(importing is None or create, "PORTABLE_IMPORT_FRESH_ONLY")
        self = cls.__new__(cls)
        self._limits, self._implementation_raw = limits, implementation_raw
        self.semantic_id, self.foundation_id = implementation["semantic_id"], S.foundation_id()
        self.implementation_id = S.implementation_id(implementation_raw)
        self._store_id = hexid(store_id)
        self._current_support = sorted({implementation[key] for key in SUPPORT_FIELDS})
        self._basis_request = basis_request_id(self.semantic_id, self.foundation_id)
        self._native_basis_root = S.local_root_id(implementation_raw, store_id, "basis", "", self._basis_request)
        self._basis_root = ""
        self._root = ordinary(directory, directory=True, fresh=create)
        self._marker = E.canonical_json({"schema": SCHEMA, "store_id": store_id,
                                        "implementation": implementation, "limits": vars(limits)})
        self._closed, self._denied = False, False
        self._lock, self._db = None, None
        self._grant = self._grant_binding = self._import_grant = self._import_binding = None
        self._activation_raw = None
        self._verified_artifacts = set()
        if create:
            self._root.mkdir()
        try:
            marker = self._root / "ADOPTION.json"
            if create:
                self._write_fresh(marker, self._marker)
                (self._root / "operations").mkdir()
                (self._root / "imports").mkdir()
                self._write_fresh(self._root / "owner.lock", b"\0")
            need(read_bounded(marker, len(self._marker)) == self._marker, "CATALOG_ADOPTION")
            self._live()
            ordinary(self._root / "operations", directory=True)
            ordinary(self._root / "imports", directory=True)
            need(read_bounded(self._root / "owner.lock", 1) == b"\0", "CATALOG_LOCK_FILE")
            import msvcrt
            self._lock = (self._root / "owner.lock").open("r+b")
            msvcrt.locking(self._lock.fileno(), msvcrt.LK_NBLCK, 1)
            database = ordinary(self._root / "catalog.sqlite", fresh=create)
            maximum = limits.max_db_pages * 4096
            if not create:
                need(database.stat().st_size <= maximum, "CATALOG_DATABASE_BOUND")
            for suffix in ("-wal", "-shm"):
                need(not os.path.lexists(str(database) + suffix), "CATALOG_DATABASE_SIDECAR")
            journal = Path(str(database) + "-journal")
            if os.path.lexists(journal):
                need(not create, "CATALOG_FRESH_JOURNAL")
                ordinary(journal)
                need(journal.stat().st_size <= 2*maximum+1024*1024, "CATALOG_JOURNAL_BOUND")
            self._db = sqlite3.connect(database, isolation_level=None, timeout=1)
            for pragma in ("trusted_schema=OFF", "foreign_keys=ON", "journal_mode=DELETE",
                           "synchronous=FULL", "temp_store=MEMORY", "mmap_size=0"):
                self._db.execute("PRAGMA " + pragma)
            need(self._db.execute("PRAGMA page_size").fetchone()[0] == 4096, "CATALOG_PAGE_SIZE")
            need(self._db.execute("PRAGMA max_page_count="+str(limits.max_db_pages)).fetchone()[0]
                 == limits.max_db_pages, "CATALOG_PAGE_BOUND")
            if create:
                activation = self._identity_activation()
                if importing is None:
                    activation.update(state="ACTIVE", origin="native-bootstrap",
                                      basis_root=self._native_basis_root)
                else:
                    activation.update(state="IMPORTING", import_id=hexid(importing))
                self._db.executescript("""
                    BEGIN IMMEDIATE;
                    CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), marker BLOB NOT NULL,
                        activation BLOB NOT NULL);
                    CREATE TABLE roots(id TEXT PRIMARY KEY, parent TEXT REFERENCES roots(id),
                        record BLOB NOT NULL) WITHOUT ROWID;
                    CREATE TABLE operations(id TEXT PRIMARY KEY, root TEXT NOT NULL,
                        state TEXT NOT NULL, reserved_bytes INTEGER NOT NULL) WITHOUT ROWID;
                    CREATE TABLE imports(id TEXT PRIMARY KEY, record BLOB NOT NULL,
                        reserved_bytes INTEGER NOT NULL) WITHOUT ROWID;
                    COMMIT;
                """)
                self._db.execute("INSERT INTO meta VALUES(1,?,?)", (self._marker, E.canonical_json(activation)))
            row = self._db.execute("SELECT marker,activation FROM meta WHERE id=1").fetchone()
            need(row is not None and row[0] == self._marker, "CATALOG_DATABASE_LINEAGE")
            self._activation_raw = bytes(row[1])
            activation = self._validate_activation(self._activation_raw)
            if importing is not None:
                need(activation["state"] == "IMPORTING" and activation["import_id"] == importing,
                     "PORTABLE_IMPORT_ACTIVATION")
                return self
            need(activation["state"] == "ACTIVE", "PORTABLE_CATALOG_IMPORTING")
            self._basis_root = activation["basis_root"]
            # No deadline or actual-event authority survives process reopening.
            self._db.execute("UPDATE operations SET state='INTERRUPTED' WHERE state='RESERVED'")
            if activation["origin"] == "legacy-import":
                self.context(activation["selected_root"])
            self._active()
            return self
        except BaseException:
            self.close()
            raise

    @staticmethod
    def _write_fresh(path, raw):
        ordinary(path, fresh=True)
        with path.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())

    @property
    def basis_root(self):
        self._active()
        return self._basis_root

    def _identity_activation(self):
        return {"schema": ACTIVATION_SCHEMA, "semantic_id": self.semantic_id,
                "foundation_id": self.foundation_id, "implementation_id": self.implementation_id,
                "store_id": self._store_id}

    def _parse(self, raw):
        need(type(raw) is bytes and 0 < len(raw) <= self._limits.max_manifest_bytes,
             "CATALOG_MANIFEST_BOUND")
        return E.strict_json(raw, E.Limits(max_bytes=self._limits.max_manifest_bytes))

    def _validate_activation(self, raw):
        doc = self._parse(raw)
        base = self._identity_activation()
        need(type(doc) is dict and all(doc.get(key) == value for key, value in base.items()),
             "PORTABLE_ACTIVATION_IDENTITY")
        if doc.get("state") == "IMPORTING":
            fields(doc, (*base, "state", "import_id"), "PORTABLE_ACTIVATION_FIELDS")
            hexid(doc["import_id"])
        elif doc.get("state") == "ACTIVE" and doc.get("origin") == "native-bootstrap":
            fields(doc, (*base, "state", "origin", "basis_root"), "PORTABLE_ACTIVATION_FIELDS")
            need(doc["basis_root"] == self._native_basis_root, "PORTABLE_ACTIVATION_BASIS")
        else:
            fields(doc, (*base, "state", "origin", "basis_root", "selected_root", "import_id",
                         "import_record_sha256"), "PORTABLE_ACTIVATION_FIELDS")
            need(doc["state"] == "ACTIVE" and doc["origin"] == "legacy-import", "PORTABLE_ACTIVATION_STATE")
            for key in ("basis_root", "selected_root", "import_id", "import_record_sha256"):
                hexid(doc[key])
        return doc

    def _live(self):
        need(not self._closed, "CATALOG_CLOSED")
        if os.path.lexists(self._root / "WITHDRAWN"):
            self._denied = True
        need(not self._denied, "CATALOG_WITHDRAWN")

    def _state(self):
        self._live()
        need(self._db.execute("SELECT marker,activation FROM meta WHERE id=1").fetchone()
             == (self._marker, self._activation_raw), "PORTABLE_ACTIVATION_CHANGED")
        return self._validate_activation(self._activation_raw)

    def _active(self):
        state = self._state()
        need(state["state"] == "ACTIVE", "PORTABLE_CATALOG_IMPORTING")
        return state

    def _root_row(self, root):
        hexid(root)
        row = self._db.execute("SELECT length(record) FROM roots WHERE id=?", (root,)).fetchone()
        need(row is not None, "CATALOG_UNCOMMITTED_ROOT")
        uint(row[0], 1, self._limits.max_manifest_bytes, "CATALOG_MANIFEST_BOUND")
        stored = self._db.execute("SELECT parent,record FROM roots WHERE id=?", (root,)).fetchone()
        raw = bytes(stored[1])
        need(len(raw) == row[0], "CATALOG_RECORD_CHANGED")
        record = self._parse(raw)
        need(type(record) is dict and record.get("local_root") == root and
             record.get("parent_root") == (stored[0] or ""), "PORTABLE_RECORD_SQL_BINDING")
        return raw, record

    def _artifact(self, relative, size, expected, *, maximum=None):
        # All callers supply a path already equated to a catalog-generated form.
        path = self._root.joinpath(*relative.split("/"))
        uint(size, 1, maximum or self._limits.max_artifact_bytes, "CATALOG_ARTIFACT_SIZE")
        hexid(expected)
        key = (relative, size, expected)
        if key not in self._verified_artifacts:
            ordinary(path)
            need(path.stat().st_size == size, "CATALOG_ARTIFACT_SIZE")
            with path.open("rb") as stream:
                actual = hashlib.file_digest(stream, "sha256").hexdigest()
            need(actual == expected, "CATALOG_ARTIFACT_DIGEST")
            self._verified_artifacts.add(key)
        return path

    def _import_record(self, activation):
        if activation["origin"] == "native-bootstrap":
            need(self._db.execute("SELECT count(*) FROM imports").fetchone()[0] == 0,
                 "PORTABLE_UNEXPECTED_IMPORT")
            return None
        need(self._db.execute("SELECT count(*) FROM imports").fetchone()[0] == 1,
             "PORTABLE_SINGLE_IMPORT_LINEAGE")
        row = self._db.execute("SELECT length(record),reserved_bytes FROM imports WHERE id=?",
                               (activation["import_id"],)).fetchone()
        need(row is not None, "PORTABLE_IMPORT_RECORD_MISSING")
        uint(row[0], 1, self._limits.max_manifest_bytes, "CATALOG_MANIFEST_BOUND")
        uint(row[1], 1, self._limits.max_total_artifact_bytes, "PORTABLE_IMPORT_CHARGE")
        raw = bytes(self._db.execute("SELECT record FROM imports WHERE id=?",
                                    (activation["import_id"],)).fetchone()[0])
        need(len(raw) == row[0] and sha(raw) == activation["import_record_sha256"],
             "PORTABLE_IMPORT_RECORD_BINDING")
        doc = self._validate_import(raw)
        need(doc["import_id"] == activation["import_id"] and
             doc["roots"][0][0] == activation["basis_root"] and
             doc["roots"][-1][0] == activation["selected_root"], "PORTABLE_IMPORT_ACTIVATION_ROOTS")
        return doc

    def _validate_import(self, raw):
        doc = self._parse(raw)
        fields(doc, ("schema", "import_id", "semantic_id", "foundation_id", "implementation_id",
            "store_id", "source_store_id", "source_profile", "source_selected_root",
            "source_manifest_sha256", "correspondence_sha256", "translation_support",
            "source_check_support", "retained_support", "roots", "audit"), "PORTABLE_IMPORT_FIELDS")
        need(doc["schema"] == IMPORT_SCHEMA and doc["semantic_id"] == self.semantic_id and
             doc["foundation_id"] == self.foundation_id and doc["implementation_id"] == self.implementation_id
             and doc["store_id"] == self._store_id, "PORTABLE_IMPORT_IDENTITY")
        for key in ("import_id", "source_store_id", "source_selected_root", "source_manifest_sha256",
                    "correspondence_sha256", "translation_support"):
            hexid(doc[key])
        L.profile_bytes(doc["source_profile"])
        _supports(doc["source_check_support"])
        need({doc["source_profile"][key] for key in SOURCE_SUPPORT_FIELDS}
             <= set(doc["source_check_support"]), "PORTABLE_SOURCE_SUPPORT_OMISSION")
        need(_supports(doc["retained_support"]) == sorted(set(self._current_support +
             doc["source_check_support"] + [doc["translation_support"]])), "PORTABLE_RETAINED_SUPPORT")
        need(type(doc["roots"]) is list and 1 <= len(doc["roots"]) <= self._limits.max_roots,
             "PORTABLE_IMPORT_ROOT_BOUND")
        for row in doc["roots"]:
            need(type(row) is list and len(row) == 2, "PORTABLE_IMPORT_ROOT_ROW")
            hexid(row[0]); hexid(row[1])
        need(len({row[0] for row in doc["roots"]}) == len(doc["roots"]), "PORTABLE_IMPORT_DUPLICATE_ROOT")
        audit = doc["audit"]
        fields(audit, ("relative_path", "artifact_bytes", "artifact_sha256"), "PORTABLE_IMPORT_AUDIT_FIELDS")
        need(audit["relative_path"] == "imports/"+doc["import_id"]+"/audit.json", "PORTABLE_IMPORT_AUDIT_PATH")
        self._artifact(audit["relative_path"], audit["artifact_bytes"], audit["artifact_sha256"],
                       maximum=self._limits.max_manifest_bytes)
        correspondence = self._root / "imports" / doc["import_id"] / "correspondence.json"
        need(sha(read_bounded(correspondence, self._limits.max_manifest_bytes)) == doc["correspondence_sha256"],
             "PORTABLE_CORRESPONDENCE_BINDING")
        return doc

    def _validate_record(self, raw, row, import_doc, import_roots):
        fields(row, ("schema", "local_root", "parent_root", "kind", "semantic_id", "foundation_id",
            "input_unit_ids", "request_hash", "bindings", "snapshot", "origin", "provenance"),
            "PORTABLE_ROOT_FIELDS")
        need(row["schema"] == ROOT_SCHEMA and row["semantic_id"] == self.semantic_id and
             row["foundation_id"] == self.foundation_id, "PORTABLE_ROOT_IDENTITY")
        hexid(row["local_root"]); hexid(row["request_hash"])
        need(row["kind"] in ("basis", "extension"), "PORTABLE_ROOT_KIND")
        if row["kind"] == "basis":
            need(row["parent_root"] == "" and row["input_unit_ids"] == [] and
                 row["request_hash"] == self._basis_request, "PORTABLE_BASIS_REQUEST")
        else:
            hexid(row["parent_root"])
            ids = row["input_unit_ids"]
            need(type(ids) is list and 1 <= len(ids) <= self._limits.max_batch_units,
                 "PORTABLE_ROOT_INPUT_BOUND")
            for identity in ids:
                hexid(identity)
            need(len(set(ids)) == len(ids) and batch_id(ids) == row["request_hash"], "PORTABLE_ROOT_INPUT_BINDING")
        bindings = row["bindings"]
        need(type(bindings) is list and 1 <= len(bindings) <= self._limits.max_names, "CATALOG_BINDING_BOUND")
        seen = set()
        for binding in bindings:
            need(type(binding) is list and len(binding) == 2, "PORTABLE_BINDING_ROW")
            key = E.name_key(binding[0]); hexid(binding[1])
            need(key not in seen, "PORTABLE_DUPLICATE_BINDING")
            seen.add(key)
        if row["kind"] == "basis":
            need(len(bindings) == 581 and all(symbol == S.basis_symbol_id(self.semantic_id,
                 self.foundation_id, name) for name, symbol in bindings), "PORTABLE_BASIS_BINDINGS")
        snapshot, origin = row["snapshot"], row["provenance"]
        fields(snapshot, ("module_name", "parent_module", "relative_path", "artifact_bytes",
                          "artifact_sha256", "writer_origin"), "PORTABLE_SNAPSHOT_FIELDS")
        E.name_key(snapshot["module_name"])
        if snapshot["parent_module"] != []:
            E.name_key(snapshot["parent_module"])
        if row["origin"] == "native-check":
            fields(origin, ("implementation_id", "operation_id"), "PORTABLE_NATIVE_ORIGIN_FIELDS")
            need(origin["implementation_id"] == self.implementation_id, "PORTABLE_NATIVE_IMPLEMENTATION")
            hexid(origin["operation_id"])
            need(row["local_root"] == S.local_root_id(self._implementation_raw, self._store_id,
                 row["kind"], row["parent_root"], row["request_hash"]), "PORTABLE_NATIVE_ROOT")
            need(snapshot["module_name"] == L.module_name(row["local_root"]) and
                 snapshot["relative_path"] == "operations/"+origin["operation_id"]+"/chunk.olean" and
                 snapshot["writer_origin"] == "native-check", "PORTABLE_NATIVE_SNAPSHOT")
            operation = self._db.execute("SELECT root,state,reserved_bytes FROM operations WHERE id=?",
                                         (origin["operation_id"],)).fetchone()
            need(operation == (row["local_root"], "COMMITTED", snapshot["artifact_bytes"]),
                 "PORTABLE_NATIVE_OPERATION_BINDING")
        else:
            fields(origin, ("import_id", "ordinal", "source_store_id", "source_profile_id", "source_root",
                "source_parent_root", "source_record_sha256", "source_operation_id", "source_check_support",
                "translation_support"), "PORTABLE_LEGACY_ORIGIN_FIELDS")
            need(row["origin"] == "legacy-translation" and import_doc is not None and
                 origin["import_id"] == import_doc["import_id"] and
                 import_roots.get(row["local_root"]) == sha(raw), "PORTABLE_LEGACY_IMPORT_BINDING")
            ordinal = uint(origin["ordinal"], 0, len(import_doc["roots"])-1, "PORTABLE_IMPORT_ORDINAL")
            need(import_doc["roots"][ordinal][0] == row["local_root"], "PORTABLE_IMPORT_ROOT_ORDER")
            profile_id = L.digest("ordinary-native-profile-v1", import_doc["source_profile"])
            need(origin["source_store_id"] == import_doc["source_store_id"] and
                 origin["source_profile_id"] == profile_id and
                 origin["source_check_support"] == import_doc["source_check_support"] and
                 origin["translation_support"] == import_doc["translation_support"], "PORTABLE_LEGACY_ORIGIN")
            for key in ("source_root", "source_record_sha256", "source_operation_id"):
                hexid(origin[key])
            if origin["source_parent_root"] != "": hexid(origin["source_parent_root"])
            need(row["local_root"] == legacy_root_id(self.semantic_id, self.foundation_id, self._store_id,
                 origin["import_id"], origin["source_root"], row["parent_root"]), "PORTABLE_LEGACY_ROOT")
            prefix = "imports/"+origin["import_id"]+"/"+str(ordinal)+"/"
            need(snapshot["relative_path"] == prefix+"chunk.olean" and snapshot["writer_origin"] == "retained-v1-check"
                 and snapshot["module_name"] == L.module_name(origin["source_root"]) and
                 snapshot["parent_module"] == (L.module_name(origin["source_parent_root"])
                                                if origin["source_parent_root"] else []), "PORTABLE_LEGACY_SNAPSHOT")
            original_raw = read_bounded(self._root.joinpath(*prefix.split("/")) / "source-record.json",
                                         self._limits.max_manifest_bytes)
            need(sha(original_raw) == origin["source_record_sha256"], "PORTABLE_SOURCE_RECORD_DIGEST")
            original = self._parse(original_raw)
            fields(original, ("root", "profile_id", "kind", "parent", "operation", "request_hash",
                              "artifact_bytes", "artifact_sha256", "bindings"), "PORTABLE_SOURCE_RECORD_FIELDS")
            need(original["root"] == origin["source_root"] and original["parent"] == origin["source_parent_root"]
                 and original["profile_id"] == profile_id and original["operation"] == origin["source_operation_id"]
                 and original["kind"] == row["kind"] and original["artifact_bytes"] == snapshot["artifact_bytes"]
                 and original["artifact_sha256"] == snapshot["artifact_sha256"], "PORTABLE_SOURCE_RECORD_ORIGIN")
            source_basis = L.digest("ordinary-basis-root-v1", [profile_id, L.SEED, L.INVENTORY])
            hexid(original["request_hash"])
            if row["kind"] == "basis":
                need(original["request_hash"] == L.digest("ordinary-fixed-basis-request-v1", [L.SEED, L.INVENTORY]),
                     "PORTABLE_SOURCE_BASIS_REQUEST")
            expected_source_root = source_basis if row["kind"] == "basis" else L.digest(
                "ordinary-extension-root-v1", [profile_id, original["parent"], original["request_hash"]])
            need(original["root"] == expected_source_root, "PORTABLE_SOURCE_ROOT_FORMULA")
            need(type(original["bindings"]) is list and len(original["bindings"]) == len(bindings),
                 "PORTABLE_SOURCE_BINDING_COUNT")
            for before, after in zip(original["bindings"], bindings):
                need(type(before) is list and len(before) == 2 and E.name_key(before[0]) == E.name_key(after[0]),
                     "PORTABLE_SOURCE_BINDING_NAMES")
                hexid(before[1])
                if row["kind"] == "basis":
                    need(before[1] == E.basis_symbol_id(profile_id, source_basis, before[0]),
                         "PORTABLE_SOURCE_BASIS_BINDING")
        return self._artifact(snapshot["relative_path"], snapshot["artifact_bytes"], snapshot["artifact_sha256"])

    def _context_rows(self, rows, basis_root, import_doc):
        bindings, plan, total, previous, previous_source, imported_count = {}, [], 0, "", "", 0
        import_roots = {} if import_doc is None else dict(import_doc["roots"])
        for position, (raw, row) in enumerate(rows):
            need(row.get("parent_root") == previous and row.get("kind") == ("basis" if position == 0 else "extension"),
                 "PORTABLE_CONTEXT_CHAIN")
            if position == 0:
                need(row.get("local_root") == basis_root, "CATALOG_BASIS_REQUIRED")
            path = self._validate_record(raw, row, import_doc, import_roots)
            snapshot = row["snapshot"]
            expected_parent = [] if not plan else plan[-1]["module_name"]
            need(snapshot["parent_module"] == expected_parent, "PORTABLE_PARENT_MODULE_BINDING")
            if row["origin"] == "legacy-translation":
                need(imported_count == position and row["provenance"]["ordinal"] == position and
                     row["provenance"]["source_parent_root"] == previous_source,
                     "PORTABLE_LEGACY_PREFIX_CHAIN")
                previous_source = row["provenance"]["source_root"]
                imported_count += 1
            total += snapshot["artifact_bytes"]
            need(total <= self._limits.max_total_artifact_bytes, "CATALOG_SELECTED_BYTE_BOUND")
            for name, symbol in row["bindings"]:
                key = E.name_key(name)
                need(key not in bindings, "CATALOG_SHADOWED_BINDING")
                bindings[key] = symbol
            need(len(bindings) <= self._limits.max_names, "CATALOG_CONTEXT_NAME_BOUND")
            plan.append({"module_name": deepcopy(snapshot["module_name"]), "path": str(path),
                         "parent_module": deepcopy(snapshot["parent_module"]),
                         "artifact_bytes": snapshot["artifact_bytes"], "names_count": len(row["bindings"])})
            previous = row["local_root"]
        need(plan, "CATALOG_BASIS_REQUIRED")
        if import_doc is not None and imported_count == len(import_doc["roots"]):
            need(previous_source == import_doc["source_selected_root"], "PORTABLE_SOURCE_SELECTED_ROOT")
        return {"local_root": previous, "semantic_id": self.semantic_id, "foundation_id": self.foundation_id,
                "implementation_id": self.implementation_id, "basis_root": basis_root,
                "basis_module": deepcopy(plan[0]["module_name"]), "root_module": deepcopy(plan[-1]["module_name"]),
                "bindings": bindings, "modules": plan,
                "retained_support": list(self._current_support if import_doc is None else import_doc["retained_support"])}

    def context(self, local_root):
        """Internal checked-lineage plan, never a transferable warrant.

        Verify retained snapshot bytes once per owner process. A fresh native
        worker still loads the selected context; no constant-cost cold import is
        claimed. Original imported module names are returned without rewriting.
        """
        activation = self._active()
        import_doc = self._import_record(activation)
        reverse, seen, current = [], set(), hexid(local_root)
        while current:
            need(current not in seen and len(seen) < self._limits.max_roots, "CATALOG_CHAIN_BOUND")
            seen.add(current)
            raw, row = self._root_row(current)
            reverse.append((raw, row))
            current = row.get("parent_root")
            need(type(current) is str, "PORTABLE_PARENT_ROOT")
        result = self._context_rows(list(reversed(reverse)), self._basis_root, import_doc)
        self._active()
        return result

    def _reserve(self, kind, parent, request_hash, bindings, identities, parent_plan, *, seconds, output_bytes,
                 parent_deadline=None):
        self._active()
        need(self._grant is None, "CATALOG_OPERATION_ACTIVE")
        uint(seconds, 1, 3600, "CATALOG_DEADLINE")
        uint(output_bytes, 1, self._limits.max_artifact_bytes, "CATALOG_OUTPUT_RESERVATION")
        need(self._db.execute("SELECT count(*) FROM roots").fetchone()[0] < self._limits.max_roots, "CATALOG_ROOT_LIMIT")
        count, reserved = self._db.execute("SELECT count(*),COALESCE(sum(reserved_bytes),0) FROM operations").fetchone()
        imported = self._db.execute("SELECT COALESCE(sum(reserved_bytes),0) FROM imports").fetchone()[0]
        need(count < self._limits.max_operations and reserved+imported+output_bytes <= self._limits.max_total_artifact_bytes,
             "CATALOG_OPERATION_OR_STORAGE_LIMIT")
        raw = E.canonical_json(bindings)
        need(0 < len(bindings) <= self._limits.max_names and len(raw) <= self._limits.max_manifest_bytes//2,
             "CATALOG_BINDING_BOUND")
        root = S.local_root_id(self._implementation_raw, self._store_id, kind, parent, request_hash)
        need(self._db.execute("SELECT 1 FROM roots WHERE id=?", (root,)).fetchone() is None, "CATALOG_ALREADY_COMMITTED")
        grant = _Grant()
        grant.identifier, grant.root, grant.parent, grant.kind = secrets.token_hex(32), root, parent, kind
        grant.request_hash, grant.bindings_raw, grant.names_count = request_hash, raw, len(bindings)
        grant.input_unit_ids = tuple(identities)
        grant.module_name_raw = E.canonical_json(L.module_name(root))
        grant.parent_module_raw = E.canonical_json(parent_plan[-1]["module_name"] if parent_plan else [])
        grant.parent_plan_raw = E.canonical_json(parent_plan)
        need(len(grant.parent_plan_raw) <= self._limits.max_manifest_bytes, "PORTABLE_PARENT_PLAN_BOUND")
        _check_parent_deadline(parent_deadline)
        grant.deadline = time.monotonic()+seconds
        if parent_deadline is not None:
            grant.deadline = min(grant.deadline, parent_deadline)
        grant.directory = self._root / "operations" / grant.identifier
        self._db.execute("INSERT INTO operations VALUES(?,?,'RESERVED',?)", (grant.identifier, root, output_bytes))
        grant.directory.mkdir()
        self._grant = grant
        self._grant_binding = tuple(getattr(grant, key) for key in _Grant.__slots__)
        return grant

    def reserve_basis(self, fixed_names, *, seconds=120, output_bytes=32*1024*1024, parent_deadline=None):
        """Reserve the actual pinned basis worker, not a metadata-only basis."""
        self._active()
        _check_parent_deadline(parent_deadline)
        need(type(fixed_names) in (list, tuple) and len(fixed_names) == 581, "CATALOG_FIXED_BASIS_CENSUS")
        need(self._db.execute("SELECT count(*) FROM roots").fetchone()[0] == 0 and
             self._basis_root == self._native_basis_root, "CATALOG_BASIS_ALREADY_PRESENT")
        rows = sorted((E.name_key(name), name) for name in fixed_names)
        need(len({key for key, _ in rows}) == 581, "CATALOG_FIXED_BASIS_CENSUS")
        bindings = [[name, S.basis_symbol_id(self.semantic_id, self.foundation_id, name)] for _, name in rows]
        return self._reserve("basis", "", self._basis_request, bindings, [], [], seconds=seconds,
                             output_bytes=output_bytes, parent_deadline=parent_deadline)

    def reserve_extension(self, parent_root, raw_v2_units, *, seconds=120, output_bytes=64*1024*1024,
                          parent_deadline=None):
        self._active()
        _check_parent_deadline(parent_deadline)
        need(type(raw_v2_units) in (list, tuple) and 1 <= len(raw_v2_units) <= self._limits.max_batch_units,
             "CATALOG_BATCH_COUNT")
        need(all(type(raw) is bytes for raw in raw_v2_units) and sum(map(len, raw_v2_units)) <= self._limits.max_batch_bytes,
             "CATALOG_BATCH_BYTES")
        context = self.context(parent_root)
        bindings, introduced, identities = dict(context["bindings"]), [], []
        for raw in raw_v2_units:
            _check_parent_deadline(parent_deadline)
            evidence = PE.read_evidence(raw)
            doc = evidence.document
            need(doc["semantic_id"] == self.semantic_id, "PORTABLE_EVIDENCE_SEMANTICS")
            for name, symbol in doc["imports"]:
                need(bindings.get(E.name_key(name)) == symbol, "CATALOG_DEPENDENCY_BINDING")
            for row in doc["unit"][2]:
                name, key = row[0], E.name_key(row[0])
                need(key not in bindings, "CATALOG_OVERWRITE")
                symbol = S.export_id(self.semantic_id, evidence.unit_id, name)
                bindings[key] = symbol
                introduced.append([name, symbol])
            need(len(bindings) <= self._limits.max_names, "CATALOG_CONTEXT_NAME_BOUND")
            identities.append(evidence.unit_id)
        return self._reserve("extension", parent_root, batch_id(identities), introduced, identities,
                             context["modules"], seconds=seconds, output_bytes=output_bytes,
                             parent_deadline=parent_deadline)

    def _grant_active(self, grant):
        self._active()
        need(type(grant) is _Grant and grant is self._grant and
             tuple(getattr(grant, key) for key in _Grant.__slots__) == self._grant_binding,
             "CATALOG_LIVE_GRANT_REQUIRED")
        need(time.monotonic() < grant.deadline, "CATALOG_GRANT_EXPIRED")
        row = self._db.execute("SELECT root,state FROM operations WHERE id=?", (grant.identifier,)).fetchone()
        need(row == (grant.root, "RESERVED"), "PORTABLE_GRANT_OPERATION_BINDING")

    def _commit_checked(self, grant):
        """PRIVATE: call only immediately after the exact clean worker event.

        Controller binds actual I/support, parent_plan_raw, parent_module_raw,
        module_name_raw, ordered V2 IDs/raw units and output/name census to this
        live grant and supervises resource bounds/closure. A report file alone
        cannot supply that event. Storage tests with inert files prove no math.
        """
        self._grant_active(grant)
        entries = 0
        with os.scandir(grant.directory) as listing:
            for entry in listing:
                entries += 1
                need(entries == 1 and entry.name == "chunk.olean", "CATALOG_OUTPUT_CENSUS")
        need(entries == 1, "CATALOG_OUTPUT_CENSUS")
        path = ordinary(grant.directory / "chunk.olean")
        size = path.stat().st_size
        reserved = self._db.execute("SELECT reserved_bytes FROM operations WHERE id=?", (grant.identifier,)).fetchone()[0]
        uint(size, 1, reserved, "CATALOG_RESULT_OUTPUT_BOUND")
        with path.open("r+b") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
            stream.flush(); os.fsync(stream.fileno())
        record = E.canonical_json({"schema": ROOT_SCHEMA, "local_root": grant.root, "parent_root": grant.parent,
            "kind": grant.kind, "semantic_id": self.semantic_id, "foundation_id": self.foundation_id,
            "input_unit_ids": list(grant.input_unit_ids), "request_hash": grant.request_hash,
            "bindings": self._parse(grant.bindings_raw),
            "snapshot": {"module_name": self._parse(grant.module_name_raw),
                "parent_module": self._parse(grant.parent_module_raw),
                "relative_path": "operations/"+grant.identifier+"/chunk.olean", "artifact_bytes": size,
                "artifact_sha256": actual, "writer_origin": "native-check"},
            "origin": "native-check", "provenance": {"implementation_id": self.implementation_id,
                                                       "operation_id": grant.identifier}})
        need(len(record) <= self._limits.max_manifest_bytes, "CATALOG_MANIFEST_BOUND")
        self._grant_active(grant)
        self._db.execute("BEGIN IMMEDIATE")
        try:
            self._db.execute("INSERT INTO roots VALUES(?,?,?)", (grant.root, grant.parent or None, record))
            self._db.execute("UPDATE operations SET state='COMMITTED',reserved_bytes=? WHERE id=?", (size, grant.identifier))
            self._active()
            need(time.monotonic() < grant.deadline, "CATALOG_GRANT_EXPIRED")
            self._db.execute("COMMIT")
        except BaseException as error:
            self._uncertain(error)
        self._grant = self._grant_binding = None
        return grant.root

    def _import_active(self, grant):
        state = self._state()
        need(state["state"] == "IMPORTING" and type(grant) is _ImportGrant and grant is self._import_grant
             and tuple(getattr(grant, key) for key in _ImportGrant.__slots__) == self._import_binding
             and state["import_id"] == grant.identifier, "PORTABLE_LIVE_IMPORT_REQUIRED")
        need(time.monotonic() < grant.deadline, "PORTABLE_IMPORT_EXPIRED")

    def _flush_import_tree(self, grant):
        """Bounded ordinary-file census/flush; no parsing or native loading."""
        todo, entries, total = [grant.directory], 0, 0
        while todo:
            directory = ordinary(todo.pop(), directory=True)
            with os.scandir(directory) as listing:
                for entry in listing:
                    self._import_active(grant)
                    entries += 1
                    need(entries <= self._limits.max_names, "PORTABLE_IMPORT_FILE_COUNT")
                    path = Path(entry.path)
                    if entry.is_dir(follow_symlinks=False):
                        ordinary(path, directory=True)
                        todo.append(path)
                    else:
                        ordinary(path)
                        size = path.stat().st_size
                        total += size
                        need(total <= grant.output_bytes, "PORTABLE_IMPORT_OUTPUT_BOUND")
                        with path.open("r+b") as stream:
                            stream.flush(); os.fsync(stream.fileno())
                        need(path.stat().st_size == size, "PORTABLE_IMPORT_FILE_CHANGED")
        need(total > 0, "PORTABLE_IMPORT_EMPTY")
        return total

    def _activate_import(self, grant, ordered_root_records_raw, import_record_raw, *, source_recheck):
        """PRIVATE storage seam, NOT an implementation of legacy migration.

        Precondition: actual eligible locked V1 chain, full source/support and
        interpretation correspondence, exact evidence translation/census, copied
        immutable artifacts and full audit were established by the live importer.
        The source must remain locked/eligible/unchanged through this call. This
        method cannot infer those facts from the manifest or correspondence file.
        It validates destination bindings and atomically activates once; it never
        opens the old catalog, translates proof identities or copies a snapshot.
        source_recheck is the trusted importer's bounded raising assertion over
        its still-held source lock/eligibility; no peer supplies this callback.
        It is called before the transaction and immediately before activation.
        """
        self._import_active(grant)
        need(callable(source_recheck), "PORTABLE_SOURCE_RECHECK_REQUIRED")
        need(type(ordered_root_records_raw) in (list, tuple) and
             1 <= len(ordered_root_records_raw) <= self._limits.max_roots, "PORTABLE_IMPORT_ROOT_BOUND")
        need(all(type(raw) is bytes for raw in ordered_root_records_raw) and
             sum(map(len, ordered_root_records_raw)) <= self._limits.max_batch_bytes, "PORTABLE_IMPORT_RECORD_BYTES")
        doc = self._validate_import(import_record_raw)
        need(doc["import_id"] == grant.identifier, "PORTABLE_IMPORT_GRANT_ID")
        rows = [(raw, self._parse(raw)) for raw in ordered_root_records_raw]
        need(all(type(row) is dict for _, row in rows), "PORTABLE_IMPORT_ROOT_SHAPE")
        need([[row.get("local_root"), sha(raw)] for raw, row in rows] == doc["roots"], "PORTABLE_IMPORT_ROOT_MANIFEST")
        basis_root, selected_root = doc["roots"][0][0], doc["roots"][-1][0]
        for _, row in rows:
            need(row.get("origin") == "legacy-translation", "PORTABLE_IMPORT_NATIVE_LAUNDERING")
        self._context_rows(rows, basis_root, doc)
        charged = self._flush_import_tree(grant)
        # Recheck mutable eligibility/activation immediately before promotion.
        source_recheck()
        self._import_active(grant)
        need(self._db.execute("SELECT count(*) FROM roots").fetchone()[0] == 0 and
             self._db.execute("SELECT count(*) FROM operations").fetchone()[0] == 0 and
             self._db.execute("SELECT count(*) FROM imports").fetchone()[0] == 0, "PORTABLE_IMPORT_DESTINATION_NOT_EMPTY")
        activation = {**self._identity_activation(), "state": "ACTIVE", "origin": "legacy-import",
                      "basis_root": basis_root, "selected_root": selected_root, "import_id": grant.identifier,
                      "import_record_sha256": sha(import_record_raw)}
        activation_raw = E.canonical_json(activation)
        self._db.execute("BEGIN IMMEDIATE")
        try:
            self._db.execute("INSERT INTO imports VALUES(?,?,?)", (grant.identifier, import_record_raw, charged))
            for raw, row in rows:
                self._db.execute("INSERT INTO roots VALUES(?,?,?)", (row["local_root"], row["parent_root"] or None, raw))
            source_recheck()
            self._import_active(grant)
            self._db.execute("UPDATE meta SET activation=? WHERE id=1", (activation_raw,))
            self._live()
            need(time.monotonic() < grant.deadline, "PORTABLE_IMPORT_EXPIRED")
            self._db.execute("COMMIT")
        except BaseException as error:
            self._uncertain(error)
        self._activation_raw, self._basis_root = activation_raw, basis_root
        self._import_grant = self._import_binding = None
        return selected_root

    def _uncertain(self, error):
        try:
            if self._db.in_transaction:
                self._db.execute("ROLLBACK")
        finally:
            self.close()
        raise CatalogError("CATALOG_TRANSACTION_UNCERTAIN_REOPEN_REQUIRED") from error

    def abandon(self, grant):
        """Only after outer worker cleanup; preserve and charge staging bytes."""
        need(grant is self._grant and grant is not None, "CATALOG_LIVE_GRANT_REQUIRED")
        self._db.execute("UPDATE operations SET state='FAILED_RETAINED' WHERE id=?", (grant.identifier,))
        self._grant = self._grant_binding = None

    def close(self):
        # Outer controller/importer settles its own worker/source lock. This
        # object never kills a worker and never manufactures resumable authority.
        self._grant = self._grant_binding = self._import_grant = self._import_binding = None
        if self._db is not None:
            self._db.close(); self._db = None
        if self._lock is not None:
            self._lock.close(); self._lock = None
        self._closed = True

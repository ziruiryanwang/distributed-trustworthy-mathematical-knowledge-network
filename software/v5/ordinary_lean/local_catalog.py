"""Internal owner-controlled checked-library catalog, not peer admission.

Only the selected trusted controller may call _commit_checked, immediately
after the actual pinned native worker has checked the reserved request, written
its exact delta, and exited with clean supervision. No JSON success flag, peer
file, hash, or constructor supplies that precondition. This module deliberately
does not implement a network endpoint or execute Lean.

Reuses existing workspace_atomic and storage_paths design: one OS owner lock,
fresh non-resumable grants, SQLite DELETE/FULL, ordinary nonaliased paths, and
sticky withdrawal. Owner/OS immutability and no whole-store rollback are trust
premises. Local artifacts are acceleration state, NEVER portable math evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import secrets
import sqlite3
import stat
import time

import ordinary_evidence as E

SCHEMA = "DMKN_ORDINARY_LOCAL_CATALOG_V1"
PROFILE = "DMKN_ORDINARY_NATIVE_PROFILE_V1"
SEED = "a0acdc706f5e42dca21950c14db2307a18955c63ff953019aaff413d0a976001"
INVENTORY = "c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0"


class CatalogError(ValueError):
    pass


def need(ok, code):
    if not ok:
        raise CatalogError(code)


def digest(domain, value):
    return hashlib.sha256(domain.encode("ascii") + b"\0" + E.canonical_json(value)).hexdigest()


def hexid(value):
    need(type(value) is str and len(value) == 64 and
         all(ch in "0123456789abcdef" for ch in value), "CATALOG_HEX_ID")
    return value


def profile_bytes(profile):
    """Validate a selected identity, not the truth of its support assertions."""
    need(type(profile) is dict and set(profile) == {
        "schema", "kernel_support", "adapter_support", "basis_receiver_support",
        "basis_seed", "basis_inventory", "expression_format", "declaration_format",
        "axiom_policy", "snapshot_format"}, "NATIVE_PROFILE_FIELDS")
    need(profile["schema"] == PROFILE and profile["basis_seed"] == SEED and
         profile["basis_inventory"] == INVENTORY and
         profile["expression_format"] == E.EXPR_FORMAT and
         profile["declaration_format"] == E.UNIT_FORMAT and
         profile["axiom_policy"] == "FIXED_BASIS_NO_NEW_AXIOM_UNSAFE_SORRY" and
         profile["snapshot_format"] == "LEAN_4_34_MODULEDATA_NO_EXTENSIONS_NO_IR",
         "NATIVE_PROFILE_POLICY")
    for field in ("kernel_support", "adapter_support", "basis_receiver_support"):
        hexid(profile[field])
    return E.canonical_json(profile)


def module_name(root):
    hexid(root)
    return [[0, {"$bytes": list(b"DMKNLocal")}],
            [0, {"$bytes": list(("r" + root).encode("ascii"))}]]


@dataclass(frozen=True)
class Limits:
    max_roots: int = 4096
    max_operations: int = 8192
    max_names: int = 1048576
    max_manifest_bytes: int = 16 * 1024 * 1024
    max_artifact_bytes: int = 1024 * 1024 * 1024
    max_total_artifact_bytes: int = 4 * 1024 * 1024 * 1024
    max_db_pages: int = 32768
    max_batch_bytes: int = 64 * 1024 * 1024
    max_batch_units: int = 1024

    def __post_init__(self):
        need(all(type(x) is int and 1 <= x <= (1 << 40)
                 for x in vars(self).values()), "CATALOG_LIMITS")
        need(self.max_db_pages <= 1048576 and self.max_roots <= 65536,
             "CATALOG_LIMITS_TOO_LARGE")


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and ".." not in path.parts and
         len(path.parts) <= 128 and len(str(path)) <= 32768, "CATALOG_ABSOLUTE_PATH")
    for item in (*reversed(path.parents), path):
        try:
            info = item.lstat()
        except FileNotFoundError:
            need(item == path and fresh, "CATALOG_MISSING_PATH")
            return path
        need(not stat.S_ISLNK(info.st_mode) and not
             (getattr(info, "st_file_attributes", 0) & 0x400), "CATALOG_REDIRECTED_PATH")
        if item != path or directory:
            need(stat.S_ISDIR(info.st_mode), "CATALOG_DIRECTORY_REQUIRED")
        else:
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "CATALOG_SINGLE_FILE")
    need(not fresh, "CATALOG_FRESH_REQUIRED")
    return path


def read_bounded(path, maximum):
    path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "CATALOG_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    need(len(raw) == size, "CATALOG_FILE_CHANGED")
    return raw


class _Grant:
    """Only entries retained by this exact live catalog are active grants."""
    __slots__ = ("identifier", "directory", "deadline", "root", "parent", "kind",
                 "request_hash", "bindings_raw", "names_count")


class LocalCatalog:
    """Trusted owner API; serialized calls only. No peer may call its internals."""
    @classmethod
    def open(cls, directory, profile, store_id, *, create=False, limits=Limits()):
        need(os.name == "nt", "CATALOG_WINDOWS_LOCK_REQUIRED")
        need(type(create) is bool and type(limits) is Limits, "CATALOG_CONFIGURATION")
        selected = profile_bytes(profile)
        self = cls.__new__(cls)
        self._limits, self._profile_raw = limits, selected
        self.profile_id = digest("ordinary-native-profile-v1", profile)
        self.basis_id = digest("ordinary-basis-root-v1", [self.profile_id, SEED, INVENTORY])
        self._root = ordinary(directory, directory=True, fresh=create)
        self._marker = E.canonical_json({"schema": SCHEMA, "store_id": hexid(store_id),
            "profile": profile, "limits": vars(limits)})
        self._closed, self._denied, self._grant = False, False, None
        self._lock, self._db = None, None
        self._verified_artifacts = set()
        self._grant_binding = None
        if create:
            self._root.mkdir()
        try:
            marker = self._root / "ADOPTION.json"
            if create:
                with marker.open("xb") as stream:
                    stream.write(self._marker); stream.flush(); os.fsync(stream.fileno())
                (self._root / "operations").mkdir()
                with (self._root / "owner.lock").open("xb") as stream:
                    stream.write(b"\0"); stream.flush(); os.fsync(stream.fileno())
            need(read_bounded(marker, len(self._marker)) == self._marker, "CATALOG_ADOPTION")
            self._active()
            ordinary(self._root / "operations", directory=True)
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
                need(journal.stat().st_size <= 2 * maximum + 1024 * 1024,
                     "CATALOG_JOURNAL_BOUND")
            self._db = sqlite3.connect(database, isolation_level=None, timeout=1)
            self._db.execute("PRAGMA trusted_schema=OFF")
            self._db.execute("PRAGMA foreign_keys=ON")
            self._db.execute("PRAGMA journal_mode=DELETE")
            self._db.execute("PRAGMA synchronous=FULL")
            self._db.execute("PRAGMA temp_store=MEMORY")
            self._db.execute("PRAGMA mmap_size=0")
            need(self._db.execute("PRAGMA page_size").fetchone()[0] == 4096, "CATALOG_PAGE_SIZE")
            need(self._db.execute("PRAGMA max_page_count=" + str(limits.max_db_pages)).fetchone()[0]
                 == limits.max_db_pages, "CATALOG_PAGE_BOUND")
            if create:
                self._db.executescript("""
                    BEGIN IMMEDIATE;
                    CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), marker BLOB NOT NULL);
                    CREATE TABLE roots(id TEXT PRIMARY KEY, parent TEXT REFERENCES roots(id),
                        record BLOB NOT NULL) WITHOUT ROWID;
                    CREATE TABLE operations(id TEXT PRIMARY KEY, root TEXT NOT NULL,
                        state TEXT NOT NULL, reserved_bytes INTEGER NOT NULL) WITHOUT ROWID;
                    COMMIT;
                """)
                self._db.execute("INSERT INTO meta VALUES(1,?)", (self._marker,))
            need(self._db.execute("SELECT marker FROM meta WHERE id=1").fetchone()
                 == (self._marker,), "CATALOG_DATABASE_LINEAGE")
            # Monotonic deadlines and in-process worker authority never resume.
            self._db.execute("UPDATE operations SET state='INTERRUPTED' WHERE state='RESERVED'")
            return self
        except BaseException:
            self.close()
            raise

    def _active(self):
        need(not self._closed, "CATALOG_CLOSED")
        if os.path.lexists(self._root / "WITHDRAWN"):
            self._denied = True
        need(not self._denied, "CATALOG_WITHDRAWN")

    def _record(self, root):
        self._active(); hexid(root)
        row = self._db.execute("SELECT length(record) FROM roots WHERE id=?", (root,)).fetchone()
        need(row is not None, "CATALOG_UNCOMMITTED_ROOT")
        need(0 < row[0] <= self._limits.max_manifest_bytes, "CATALOG_MANIFEST_BOUND")
        raw = self._db.execute("SELECT record FROM roots WHERE id=?", (root,)).fetchone()[0]
        need(len(raw) == row[0], "CATALOG_RECORD_CHANGED")
        return E.strict_json(raw, E.Limits(max_bytes=self._limits.max_manifest_bytes))

    def context(self, root):
        """Authenticate the selected chain once per owner process, NOT peer files.

        Returned data are internal controller inputs, not unforgeable authority.
        A fresh worker still deserializes the chain; this is not constant-cost
        cold onboarding. Warm workers retain their actual checked environment.
        """
        self._active()
        reverse, seen, current, total = [], set(), root, 0
        while current:
            need(current not in seen and len(seen) < self._limits.max_roots, "CATALOG_CHAIN_BOUND")
            seen.add(current)
            row = self._record(current)
            need(row["root"] == current and row["profile_id"] == self.profile_id,
                 "CATALOG_RECORD_BINDING")
            reverse.append(row); current = row["parent"]
        chain = list(reversed(reverse))
        need(chain and chain[0]["root"] == self.basis_id and chain[0]["kind"] == "basis",
             "CATALOG_BASIS_REQUIRED")
        bindings, plan = {}, []
        for row in chain:
            path = self._root / "operations" / row["operation"] / "chunk.olean"
            key = (str(path), row["artifact_sha256"], row["artifact_bytes"])
            if key not in self._verified_artifacts:
                ordinary(path)
                need(path.stat().st_size == row["artifact_bytes"] and
                     0 < row["artifact_bytes"] <= self._limits.max_artifact_bytes,
                     "CATALOG_ARTIFACT_SIZE")
                with path.open("rb") as stream:
                    actual = hashlib.file_digest(stream, "sha256").hexdigest()
                need(actual == row["artifact_sha256"], "CATALOG_ARTIFACT_DIGEST")
                self._verified_artifacts.add(key)
            total += row["artifact_bytes"]
            need(total <= self._limits.max_total_artifact_bytes, "CATALOG_SELECTED_BYTE_BOUND")
            for name, symbol in row["bindings"]:
                name_bytes = E.name_key(name)
                need(name_bytes not in bindings, "CATALOG_SHADOWED_BINDING")
                bindings[name_bytes] = hexid(symbol)
            need(len(bindings) <= self._limits.max_names, "CATALOG_CONTEXT_NAME_BOUND")
            plan.append({"module_name": module_name(row["root"]), "path": str(path),
                "parent_module": module_name(row["parent"]) if row["parent"] else [],
                "artifact_bytes": row["artifact_bytes"], "names_count": len(row["bindings"])})
        self._active()
        return {"root": root, "profile_id": self.profile_id, "bindings": bindings, "modules": plan}

    def _reserve(self, kind, parent, request_hash, bindings, *, seconds, output_bytes):
        self._active()
        need(self._grant is None, "CATALOG_OPERATION_ACTIVE")
        need(type(seconds) is int and 1 <= seconds <= 3600, "CATALOG_DEADLINE")
        need(type(output_bytes) is int and 1 <= output_bytes <= self._limits.max_artifact_bytes,
             "CATALOG_OUTPUT_RESERVATION")
        need(self._db.execute("SELECT count(*) FROM roots").fetchone()[0] < self._limits.max_roots,
             "CATALOG_ROOT_LIMIT")
        count, reserved = self._db.execute("SELECT count(*),COALESCE(sum(reserved_bytes),0) "
                                         "FROM operations").fetchone()
        # Failed or interrupted staging is retained and remains charged at its
        # reservation. No optimistic free space or unselected GC is assumed.
        need(count < self._limits.max_operations and
             reserved + output_bytes <= self._limits.max_total_artifact_bytes,
             "CATALOG_OPERATION_OR_STORAGE_LIMIT")
        raw = E.canonical_json(bindings)
        need(0 < len(bindings) <= self._limits.max_names and
             len(raw) <= self._limits.max_manifest_bytes // 2, "CATALOG_BINDING_BOUND")
        root = (self.basis_id if kind == "basis" else
                digest("ordinary-extension-root-v1", [self.profile_id, parent, request_hash]))
        need(self._db.execute("SELECT 1 FROM roots WHERE id=?", (root,)).fetchone() is None,
             "CATALOG_ALREADY_COMMITTED")
        grant = _Grant()
        grant.identifier = secrets.token_hex(32)
        grant.root, grant.parent, grant.kind = root, parent, kind
        grant.request_hash, grant.bindings_raw, grant.names_count = request_hash, raw, len(bindings)
        grant.deadline = time.monotonic() + seconds
        grant.directory = self._root / "operations" / grant.identifier
        self._db.execute("INSERT INTO operations VALUES(?,?,'RESERVED',?)",
                         (grant.identifier, root, output_bytes))
        grant.directory.mkdir()
        self._grant = grant
        self._grant_binding = tuple(getattr(grant, field) for field in _Grant.__slots__)
        return grant

    def reserve_basis(self, fixed_names, *, seconds=120, output_bytes=32 * 1024 * 1024):
        """Reserve pinned-bootstrap work; names supplied by trusted fixed inventory.

        This does not check or admit the basis. The later worker must reconstruct
        it from empty through the pinned receiveSeed, not import arbitrary Init.
        """
        need(self._db.execute("SELECT count(*) FROM roots").fetchone()[0] == 0,
             "CATALOG_BASIS_ALREADY_PRESENT")
        rows = sorted([(E.name_key(name), name) for name in fixed_names])
        need(len(rows) == 581 and len({key for key, _ in rows}) == 581, "CATALOG_FIXED_BASIS_CENSUS")
        bindings = [[name, E.basis_symbol_id(self.profile_id, self.basis_id, name)] for _, name in rows]
        return self._reserve("basis", "", digest("ordinary-fixed-basis-request-v1", [SEED, INVENTORY]),
                             bindings, seconds=seconds, output_bytes=output_bytes)

    def reserve_extension(self, parent, raw_units, *, seconds=120, output_bytes=64 * 1024 * 1024):
        """Bind a bounded inert batch to accepted exact dependency identities.

        Reservation is not mathematical acceptance. Never pass Evidence.document
        mutated after parsing: this method reparses the exact immutable bytes.
        """
        self._active()
        need(type(raw_units) in (list, tuple) and 1 <= len(raw_units) <= self._limits.max_batch_units,
             "CATALOG_BATCH_COUNT")
        need(all(type(raw) is bytes for raw in raw_units) and
             sum(map(len, raw_units)) <= self._limits.max_batch_bytes, "CATALOG_BATCH_BYTES")
        context = self.context(parent)
        bindings, introduced, identities = dict(context["bindings"]), [], []
        for raw in raw_units:
            evidence = E.read_evidence(raw)
            doc = evidence.document
            need(doc["profile_id"] == self.profile_id, "CATALOG_EVIDENCE_PROFILE")
            for name, symbol in doc["imports"]:
                need(bindings.get(E.name_key(name)) == symbol, "CATALOG_DEPENDENCY_BINDING")
            for row in doc["unit"][2]:
                name = row[0]; key = E.name_key(name)
                need(key not in bindings, "CATALOG_OVERWRITE")
                symbol = E.export_id(self.profile_id, evidence.unit_id, name)
                bindings[key] = symbol; introduced.append([name, symbol])
            need(len(bindings) <= self._limits.max_names, "CATALOG_CONTEXT_NAME_BOUND")
            identities.append(evidence.unit_id)
        return self._reserve("extension", parent, digest("ordinary-batch-v1", identities),
                             introduced, seconds=seconds, output_bytes=output_bytes)

    def _grant_active(self, grant):
        self._active()
        need(type(grant) is _Grant and grant is self._grant and
             tuple(getattr(grant, field) for field in _Grant.__slots__) == self._grant_binding,
             "CATALOG_LIVE_GRANT_REQUIRED")
        need(time.monotonic() < grant.deadline, "CATALOG_GRANT_EXPIRED")

    def _commit_checked(self, grant):
        """PRIVATE integration seam: only actual clean native checking authorizes.

        The controller must bind worker profile/parent/request/module/output to
        this exact reservation and enforce total CPU/memory/output/closure. This
        helper does not inspect a PASS report or make a peer file trustworthy.
        Tests of this helper with inert dummy files are storage tests ONLY.
        """
        self._grant_active(grant)
        # This private directory is ONLY the artifact destination. Request,
        # logs and supervision reports have separately accounted owner paths.
        entries = 0
        with os.scandir(grant.directory) as listing:
            for entry in listing:
                entries += 1
                need(entries == 1 and entry.name == "chunk.olean", "CATALOG_OUTPUT_CENSUS")
        need(entries == 1, "CATALOG_OUTPUT_CENSUS")
        path = ordinary(grant.directory / "chunk.olean")
        size = path.stat().st_size
        reserved = self._db.execute("SELECT reserved_bytes FROM operations WHERE id=?",
                                    (grant.identifier,)).fetchone()[0]
        need(0 < size <= reserved, "CATALOG_RESULT_OUTPUT_BOUND")
        with path.open("r+b") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
            stream.flush(); os.fsync(stream.fileno())
        bindings = E.strict_json(grant.bindings_raw,
                                E.Limits(max_bytes=self._limits.max_manifest_bytes))
        record = E.canonical_json({"root": grant.root, "profile_id": self.profile_id,
            "kind": grant.kind, "parent": grant.parent, "operation": grant.identifier,
            "request_hash": grant.request_hash, "artifact_bytes": size,
            "artifact_sha256": actual, "bindings": bindings})
        need(len(record) <= self._limits.max_manifest_bytes, "CATALOG_MANIFEST_BOUND")
        self._grant_active(grant)
        self._db.execute("BEGIN IMMEDIATE")
        try:
            self._db.execute("INSERT INTO roots VALUES(?,?,?)", (grant.root, grant.parent or None, record))
            self._db.execute("UPDATE operations SET state='COMMITTED',reserved_bytes=? WHERE id=?",
                             (size, grant.identifier))
            self._db.execute("COMMIT")
        except BaseException as error:
            # A COMMIT exception need not prove that nothing committed. Never
            # leave a retryable in-memory grant after an uncertain transaction.
            # Reopen and resolve this exact root; no automatic worker replay.
            try:
                if self._db.in_transaction:
                    self._db.execute("ROLLBACK")
            finally:
                self.close()
            raise CatalogError("CATALOG_TRANSACTION_UNCERTAIN_REOPEN_REQUIRED") from error
        self._grant = self._grant_binding = None
        return grant.root

    def abandon(self, grant):
        """Called only after worker cleanup; preserve and charge uncommitted bytes."""
        need(grant is self._grant and grant is not None, "CATALOG_LIVE_GRANT_REQUIRED")
        self._db.execute("UPDATE operations SET state='FAILED_RETAINED' WHERE id=?", (grant.identifier,))
        self._grant = self._grant_binding = None

    def close(self):
        # Does not kill a worker: the outer controller must settle its own Job.
        if self._db is not None:
            self._db.close(); self._db = None
        if self._lock is not None:
            self._lock.close(); self._lock = None
        self._closed = True

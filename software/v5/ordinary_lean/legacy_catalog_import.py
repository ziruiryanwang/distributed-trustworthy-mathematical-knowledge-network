"""One selected owner-local V1 chain, translated once without native replay.

PRIVATE trusted-controller API, never peer admission. The caller must already
have adopted the actual original checking lineage and its concrete same-runtime
correspondence to S. File pins, a saved PASS, this manifest, and an argument file
do not establish those premises. The initial source is deliberately restricted
to the selected local successor catalog. No arbitrary foreign store is eligible.

Read-only SQLite plus the existing owner lock preserve V1, including failures.
Unchanged raw units are translated through the established name pairing; native
snapshot bytes retain their original module names. A fresh destination remains
IMPORTING until the catalog's one private transaction. Any failure retains it;
there is no retry, recovery, deserialization, compilation or mathematical check.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import sqlite3
import time

import ordinary_evidence as E
import ordinary_semantics as S
import local_catalog as C
import legacy_identity_translation as T
import portable_catalog as P

SOURCE_SCHEMA = "DMKN_ORDINARY_ELIGIBLE_LOCAL_SOURCE_V1"
CORRESPONDENCE_SCHEMA = "DMKN_ORDINARY_SAME_RUNTIME_CORRESPONDENCE_V1"
AUDIT_SCHEMA = "DMKN_ORDINARY_LEGACY_TRANSLATION_AUDIT_V1"
ELIGIBLE_SOURCE = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network") / (
    "experiments/v5-local-checks/ordinary-successor-admission-01/successor-admission/catalog")
ORIGINAL_PROFILE = ELIGIBLE_SOURCE.parents[2] / "ordinary-native-admission-01/native-admission/PROFILE.json"
MIB = 1024 * 1024
need, fields, uint, sha = C.need, P.fields, P.uint, P.sha


@dataclass(frozen=True)
class ImportLimits:
    max_roots: int = 32
    max_names: int = 65536
    max_units: int = 4096
    max_files: int = 8192
    max_file_bytes: int = 128 * MIB
    max_input_bytes: int = 512 * MIB
    max_output_bytes: int = 512 * MIB
    max_manifest_bytes: int = 16 * MIB
    max_nodes: int = 16 * 1024 * 1024

    def __post_init__(self):
        need(all(type(x) is int and 1 <= x <= (1 << 32) - 1
                 for x in vars(self).values()), "IMPORT_LIMITS")
        need(self.max_roots <= 4096 and self.max_files <= 65536 and
             self.max_names <= 1048576 and self.max_units <= 65536,
             "IMPORT_LIMITS_TOO_LARGE")


class _Files:
    """Unique selected-input accounting and chunked deadline-checked I/O."""
    def __init__(self, limits, deadline):
        self.limits, self.deadline = limits, deadline
        self.pins, self.input_bytes, self.output_bytes, self.output_files = {}, 0, 0, 0

    def live(self):
        need(time.monotonic() < self.deadline, "IMPORT_DEADLINE")

    def pin(self, pin):
        fields(pin, ("path", "bytes", "sha256"), "IMPORT_FILE_PIN_FIELDS")
        need(type(pin["path"]) is str, "IMPORT_FILE_PATH")
        path = C.ordinary(pin["path"])
        need(str(path) == pin["path"], "IMPORT_NORMALIZED_FILE_PATH")
        uint(pin["bytes"], 0, self.limits.max_file_bytes, "IMPORT_FILE_BOUND")
        C.hexid(pin["sha256"])
        if path in self.pins:
            need(self.pins[path] == pin, "IMPORT_CONFLICTING_PIN")
        else:
            self.input_bytes += pin["bytes"]
            self.pins[path] = dict(pin)
            need(len(self.pins) <= self.limits.max_files and
                 self.input_bytes <= self.limits.max_input_bytes, "IMPORT_INPUT_BOUND")
        self.live()
        return path

    def chunks(self, pin):
        path = self.pin(pin)
        need(path.stat().st_size == pin["bytes"], "IMPORT_FILE_SIZE")
        actual, count = hashlib.sha256(), 0
        with path.open("rb") as stream:
            while raw := stream.read(MIB):
                self.live()
                count += len(raw)
                need(count <= pin["bytes"], "IMPORT_FILE_GREW")
                actual.update(raw)
                yield raw
        need(count == pin["bytes"] and path.stat().st_size == count and
             actual.hexdigest() == pin["sha256"], "IMPORT_FILE_PIN")
        self.live()

    def read(self, pin, maximum):
        need(pin["bytes"] <= maximum, "IMPORT_READ_BOUND")
        return b"".join(self.chunks(pin))

    def verify(self, pin):
        for _ in self.chunks(pin):
            pass

    def _output(self, path, chunks):
        self.live()
        C.ordinary(path, fresh=True)
        self.output_files += 1
        need(self.output_files <= self.limits.max_files, "IMPORT_OUTPUT_FILE_BOUND")
        with path.open("xb") as stream:
            for raw in chunks:
                self.live()
                self.output_bytes += len(raw)
                need(self.output_bytes <= self.limits.max_output_bytes, "IMPORT_OUTPUT_BYTE_BOUND")
                stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        self.live()

    def write(self, path, raw):
        need(type(raw) is bytes and 0 < len(raw) <= self.limits.max_file_bytes,
             "IMPORT_OUTPUT_FILE_BYTES")
        self._output(path, (raw,))

    def copy(self, pin, path):
        self._output(path, self.chunks(pin))
        # Destination readback is distinct from the source-copy digest.
        expected = {**pin, "path": str(path)}
        need(path.stat().st_size == expected["bytes"], "IMPORT_COPY_SIZE")
        actual = hashlib.sha256()
        with path.open("rb") as stream:
            while raw := stream.read(MIB):
                self.live()
                actual.update(raw)
        need(actual.hexdigest() == expected["sha256"], "IMPORT_COPY_DIGEST")


class LegacyReadOnly:
    """Locked exact local source. Never calls V1 LocalCatalog.open or recovery."""
    @classmethod
    def open(cls, directory, expected_source_manifest_raw, *, parent_deadline,
             limits=ImportLimits()):
        need(os.name == "nt" and type(limits) is ImportLimits, "IMPORT_WINDOWS_CONFIGURATION")
        need(type(parent_deadline) in (float, int) and math.isfinite(parent_deadline) and
             0 < parent_deadline - time.monotonic() <= 3600, "IMPORT_PARENT_DEADLINE")
        self = cls.__new__(cls)
        self._db, self._lock, self._closed, self._denied = None, None, False, False
        self._root = C.ordinary(directory, directory=True)
        need(self._root == ELIGIBLE_SOURCE, "IMPORT_NOT_SELECTED_OWNER_LOCAL_SOURCE")
        self.files = _Files(limits, parent_deadline)
        self.manifest_raw = expected_source_manifest_raw
        self.manifest = E.strict_json(expected_source_manifest_raw,
            E.Limits(max_bytes=limits.max_manifest_bytes))
        m = self.manifest
        fields(m, ("schema", "source_directory", "store_id", "profile_id", "basis_id", "selected_root",
            "marker", "database", "fixed_seed", "fixed_inventory", "check_support", "roots"),
            "IMPORT_SOURCE_MANIFEST_FIELDS")
        need(m["schema"] == SOURCE_SCHEMA and m["source_directory"] == str(self._root),
             "IMPORT_SOURCE_SELECTION")
        for key in ("store_id", "profile_id", "basis_id", "selected_root"):
            C.hexid(m[key])
        need(type(m["roots"]) is list and 1 <= len(m["roots"]) <= limits.max_roots and
             type(m["check_support"]) is list and 1 <= len(m["check_support"]) <= 128,
             "IMPORT_SOURCE_MANIFEST_BOUNDS")
        need(m["marker"]["path"] == str(self._root / "ADOPTION.json") and
             m["database"]["path"] == str(self._root / "catalog.sqlite"), "IMPORT_SOURCE_FILES")
        try:
            self._eligible()
            lock_path = C.ordinary(self._root / "owner.lock")
            need(C.read_bounded(lock_path, 1) == b"\0", "IMPORT_OWNER_LOCK_BYTE")
            import msvcrt
            self._lock = lock_path.open("r+b")
            msvcrt.locking(self._lock.fileno(), msvcrt.LK_NBLCK, 1)
            self._eligible()
            self.marker_raw = self.files.read(m["marker"], limits.max_manifest_bytes)
            marker = self._parse(self.marker_raw)
            fields(marker, ("schema", "store_id", "profile", "limits"), "IMPORT_MARKER_FIELDS")
            need(marker["schema"] == C.SCHEMA and marker["store_id"] == m["store_id"], "IMPORT_MARKER_LINEAGE")
            C.profile_bytes(marker["profile"])
            self.profile = marker["profile"]
            self.source_limits = C.Limits(**marker["limits"])
            need(C.digest("ordinary-native-profile-v1", self.profile) == m["profile_id"] and
                 C.digest("ordinary-basis-root-v1", [m["profile_id"], C.SEED, C.INVENTORY]) == m["basis_id"],
                 "IMPORT_ORIGINAL_PROFILE_BASIS")
            need(m["database"]["bytes"] <= self.source_limits.max_db_pages * 4096, "IMPORT_DATABASE_BOUND")
            self.files.verify(m["database"])
            self._db = sqlite3.connect((self._root / "catalog.sqlite").as_uri() + "?mode=ro",
                                      uri=True, isolation_level=None, timeout=0)
            for pragma in ("query_only=ON", "trusted_schema=OFF", "temp_store=MEMORY", "mmap_size=0"):
                self._db.execute("PRAGMA " + pragma)
            self._db.set_progress_handler(lambda: int(time.monotonic() >= self.files.deadline), 1000)
            need(self._db.execute("PRAGMA page_size").fetchone() == (4096,), "IMPORT_DATABASE_PAGE_SIZE")
            need(self._db.execute("SELECT marker FROM meta WHERE id=1").fetchone() == (self.marker_raw,),
                 "IMPORT_DATABASE_LINEAGE")
            self.records = self._records()
            self._source_tree()
            for pin in m["check_support"]:
                self.files.verify(pin)
            self._eligible()
            return self
        except BaseException:
            self.close()
            raise

    def _parse(self, raw):
        return E.strict_json(raw, E.Limits(max_bytes=self.files.limits.max_manifest_bytes))

    def _eligible(self):
        self.files.live()
        need(not self._closed, "IMPORT_SOURCE_CLOSED")
        if os.path.lexists(self._root / "WITHDRAWN"):
            self._denied = True
        need(not self._denied, "IMPORT_SOURCE_WITHDRAWN")
        for suffix in ("-journal", "-wal", "-shm"):
            need(not os.path.lexists(str(self._root / "catalog.sqlite") + suffix), "IMPORT_SOURCE_SIDECAR")

    def _records(self):
        m, limits = self.manifest, self.files.limits
        count = self._db.execute("SELECT count(*) FROM roots").fetchone()[0]
        need(count == len(m["roots"]) <= self.source_limits.max_roots, "IMPORT_EXACT_ROOT_CHAIN")
        count = self._db.execute("SELECT count(*) FROM operations").fetchone()[0]
        need(count <= min(self.source_limits.max_operations, limits.max_files), "IMPORT_OPERATION_BOUND")
        operations = self._db.execute("SELECT id,root,state,reserved_bytes FROM operations").fetchall()
        self.operations = {}
        for op, root, state, reserved in operations:
            C.hexid(op); C.hexid(root)
            need(state in ("COMMITTED", "FAILED_RETAINED", "INTERRUPTED"), "IMPORT_ACTIVE_OR_UNKNOWN_OPERATION")
            uint(reserved, 1, self.source_limits.max_artifact_bytes, "IMPORT_OPERATION_RESERVATION")
            self.operations[op] = (root, state, reserved)
        need(sum(row[2] for row in self.operations.values()) <= self.source_limits.max_total_artifact_bytes,
             "IMPORT_ORIGINAL_STORAGE_BOUND")
        records, previous, evidence_paths, total_units, total_names, artifact_bytes = [], "", set(), 0, 0, 0
        seen, record_bytes = set(), 0
        for ordinal, selected in enumerate(m["roots"]):
            self._eligible()
            fields(selected, ("root", "record_sha256", "check_lineage", "evidence"), "IMPORT_ROOT_SELECTION_FIELDS")
            root = C.hexid(selected["root"])
            C.hexid(selected["record_sha256"])
            need(root not in seen, "IMPORT_ROOT_CYCLE")
            seen.add(root)
            need(type(selected["check_lineage"]) is list and 1 <= len(selected["check_lineage"]) <= 128 and
                 type(selected["evidence"]) is list, "IMPORT_ROOT_MANIFEST_LISTS")
            for pin in selected["check_lineage"]:
                self.files.verify(pin)
            length = self._db.execute("SELECT length(record) FROM roots WHERE id=?", (root,)).fetchone()
            need(length is not None and 0 < length[0] <= limits.max_manifest_bytes, "IMPORT_RECORD_BOUND")
            record_bytes += length[0]
            need(record_bytes <= limits.max_manifest_bytes, "IMPORT_TOTAL_RECORD_BYTES")
            sql_parent, raw = self._db.execute("SELECT parent,record FROM roots WHERE id=?", (root,)).fetchone()
            need(type(raw) is bytes and len(raw) == length[0] and sha(raw) == selected["record_sha256"],
                 "IMPORT_RECORD_PIN")
            row = self._parse(raw)
            fields(row, ("root", "profile_id", "kind", "parent", "operation", "request_hash", "artifact_bytes",
                         "artifact_sha256", "bindings"), "IMPORT_RECORD_FIELDS")
            need(row["root"] == root and row["parent"] == previous and (sql_parent or "") == previous and
                 row["profile_id"] == m["profile_id"] and row["kind"] == ("basis" if ordinal == 0 else "extension"),
                 "IMPORT_RECORD_CHAIN")
            C.hexid(row["operation"]); C.hexid(row["request_hash"]); C.hexid(row["artifact_sha256"])
            uint(row["artifact_bytes"], 1, self.source_limits.max_artifact_bytes, "IMPORT_ARTIFACT_BOUND")
            need(self.operations.get(row["operation"]) == (root, "COMMITTED", row["artifact_bytes"]),
                 "IMPORT_COMMITTED_OPERATION")
            expected = m["basis_id"] if ordinal == 0 else C.digest(
                "ordinary-extension-root-v1", [m["profile_id"], previous, row["request_hash"]])
            need(root == expected, "IMPORT_ROOT_FORMULA")
            if ordinal == 0:
                need(selected["evidence"] == [] and row["request_hash"] == C.digest(
                    "ordinary-fixed-basis-request-v1", [C.SEED, C.INVENTORY]), "IMPORT_BASIS_REQUEST")
            else:
                need(1 <= len(selected["evidence"]) <= self.source_limits.max_batch_units,
                     "IMPORT_BATCH_UNIT_BOUND")
            batch_bytes = 0
            for pin in selected["evidence"]:
                path = self.files.pin(pin)
                need(path not in evidence_paths, "IMPORT_DUPLICATE_EVIDENCE")
                evidence_paths.add(path)
                batch_bytes += pin["bytes"]
            total_units += len(selected["evidence"])
            need(batch_bytes <= self.source_limits.max_batch_bytes and total_units <= limits.max_units,
                 "IMPORT_EVIDENCE_BOUND")
            need(type(row["bindings"]) is list and 1 <= len(row["bindings"]) <= limits.max_names,
                 "IMPORT_BINDING_BOUND")
            total_names += len(row["bindings"])
            artifact_bytes += row["artifact_bytes"]
            need(total_names <= limits.max_names and artifact_bytes <= self.source_limits.max_total_artifact_bytes,
                 "IMPORT_CHAIN_BOUND")
            artifact = {"path": str(self._root / "operations" / row["operation"] / "chunk.olean"),
                        "bytes": row["artifact_bytes"], "sha256": row["artifact_sha256"]}
            self.files.verify(artifact)
            records.append((raw, row, artifact))
            previous = root
        need(previous == m["selected_root"] and
             {op for op, (_, state, _) in self.operations.items() if state == "COMMITTED"} ==
             {row["operation"] for _, row, _ in records}, "IMPORT_SELECTED_FINAL_ROOT")
        return records

    def _source_tree(self):
        # Failed operation directories/files remain untouched and nonauthoritative.
        allowed_dirs = {"operations", *("operations/" + op for op in self.operations)}
        allowed_files = {"ADOPTION.json", "catalog.sqlite", "owner.lock",
                         *("operations/" + op + "/chunk.olean" for op in self.operations)}
        pending, entries = [self._root], 0
        while pending:
            directory = C.ordinary(pending.pop(), directory=True)
            with os.scandir(directory) as listing:
                for entry in listing:
                    self._eligible()
                    entries += 1
                    need(entries <= self.files.limits.max_files, "IMPORT_SOURCE_TREE_BOUND")
                    path = Path(entry.path)
                    relative = path.relative_to(self._root).as_posix()
                    if entry.is_dir(follow_symlinks=False):
                        need(relative in allowed_dirs, "IMPORT_UNSELECTED_SOURCE_DIRECTORY")
                        C.ordinary(path, directory=True)
                        pending.append(path)
                    else:
                        need(relative in allowed_files, "IMPORT_UNSELECTED_SOURCE_FILE")
                        C.ordinary(path)
                        need(path.stat().st_size <= self.files.limits.max_file_bytes, "IMPORT_SOURCE_FILE_BOUND")

    def assert_unchanged(self):
        self._eligible()
        self._lock.seek(0)
        need(self._lock.read(2) == b"\0", "IMPORT_LOCK_CHANGED")
        for pin in tuple(self.files.pins.values()):
            self.files.verify(pin)
        self._eligible()

    def close(self):
        if self._db is not None:
            self._db.close(); self._db = None
        if self._lock is not None:
            self._lock.close(); self._lock = None
        self._closed = True


def _correspondence(source, implementation_raw, raw):
    """Check exact selected identities, not truth of the caller's adoption."""
    implementation = S.read_implementation(implementation_raw)
    doc = source._parse(raw)
    fields(doc, ("schema", "source_profile_id", "semantic_id", "foundation_id", "implementation_id",
        "kernel_support", "adapter_support", "basis_receiver_support", "snapshot_support", "snapshot_format",
        "platform", "seed_sha256", "inventory_sha256", "expression_contract_sha256",
        "declaration_contract_sha256", "adopted_argument"), "IMPORT_CORRESPONDENCE_FIELDS")
    expected = {"schema": CORRESPONDENCE_SCHEMA, "source_profile_id": source.manifest["profile_id"],
        "semantic_id": S.semantic_id(), "foundation_id": S.foundation_id(),
        "implementation_id": S.implementation_id(implementation_raw), "seed_sha256": S.SEED,
        "inventory_sha256": S.INVENTORY, "expression_contract_sha256": S.EXPRESSION_CONTRACT,
        "declaration_contract_sha256": S.DECLARATION_CONTRACT,
        "platform": {"os": "windows", "architecture": "x86_64", "word_bits": 64, "byte_order": "little"}}
    need(all(doc[key] == value for key, value in expected.items()) and
         doc["platform"] == implementation["platform"], "IMPORT_CORRESPONDENCE_INTERPRETATION")
    for key in P.SOURCE_SUPPORT_FIELDS:
        need(doc[key] == source.profile[key] == implementation[key], "IMPORT_CHANGED_NATIVE_SUPPORT")
    profiles = [pin for pin in source.manifest["check_support"] if pin["path"] == str(ORIGINAL_PROFILE)]
    need(len(profiles) == 1, "IMPORT_ORIGINAL_SUPPORT_PROFILE_REQUIRED")
    original = source._parse(source.files.read(profiles[0], 2 * MIB))
    fields(original, ("profile", "support", "scope"), "IMPORT_ORIGINAL_SUPPORT_FIELDS")
    need(original["profile"] == source.profile and original["scope"] ==
         "EXPLICIT_NATIVE_PINS_NOT_HERMETIC_TOOLCHAIN_OR_SECURITY_SANDBOX", "IMPORT_ORIGINAL_SUPPORT_PROFILE")
    support = original["support"]
    fields(support, ("kernel", "adapter", "basis_receiver"), "IMPORT_ORIGINAL_SUPPORT_MAPS")
    for name, domain in (("kernel", "ordinary-kernel-support-v1"),
                         ("adapter", "ordinary-adapter-support-v1"),
                         ("basis_receiver", "ordinary-basis-receiver-support-v1")):
        need(C.digest(domain, support[name]) == source.profile[name + "_support"],
             "IMPORT_ORIGINAL_SUPPORT_DIGEST")
    fields(support["kernel"], ("version", "files", "scope"), "IMPORT_KERNEL_SUPPORT_FIELDS")
    need(support["kernel"]["version"] == "Lean 4.34.0" and support["kernel"]["scope"] ==
         "EXPLICIT_NAMED_BINARIES_NOT_HERMETIC_TOOLCHAIN", "IMPORT_KERNEL_SUPPORT_SCOPE")
    for section in ("adapter", "basis_receiver"):
        fields(support[section], ("source", "compiled"), "IMPORT_ADAPTER_SUPPORT_FIELDS")
    # Each claimed support leaf must resolve to a selected actual file already
    # byte-verified above, including the large native DLLs. Map hashes alone do
    # not substitute for those files or for the caller's adopted conformance.
    leaves = [support["kernel"]["files"], *(support[section][kind]
        for section in ("adapter", "basis_receiver") for kind in ("source", "compiled"))]
    selected_files = {(Path(pin["path"]).name, pin["bytes"], pin["sha256"])
                      for pin in source.manifest["check_support"]}
    for mapping in leaves:
        need(type(mapping) is dict and 1 <= len(mapping) <= 128, "IMPORT_SUPPORT_LEAF_BOUND")
        for name, pin in mapping.items():
            fields(pin, ("bytes", "sha256"), "IMPORT_SUPPORT_LEAF_FIELDS")
            need(type(name) is str and Path(name).name == name and
                 (name, pin["bytes"], pin["sha256"]) in selected_files, "IMPORT_SUPPORT_FILE_NOT_SELECTED")
    snapshot = {kind: {name + suffix: support["adapter"][kind][name + suffix]
        for name in ("BasisSnapshot", "LocalSnapshot")}
        for kind, suffix in (("source", ".lean"), ("compiled", ".olean"))}
    need(doc["snapshot_support"] == implementation["snapshot_support"] ==
         C.digest("ordinary-snapshot-support-v1", snapshot) and
         doc["snapshot_format"] == source.profile["snapshot_format"] == implementation["snapshot_format"],
         "IMPORT_SNAPSHOT_CORRESPONDENCE")
    source.files.verify(doc["adopted_argument"])
    return implementation, doc


def import_legacy(source_directory, expected_source_manifest_raw, fresh_destination,
                  implementation_raw, destination_store_id, correspondence_raw, *,
                  parent_deadline, limits=ImportLimits(), catalog_limits=C.Limits()):
    """Bounded once-only local cutover; return identities, never a portable warrant.

    The source manifest/correspondence are canonical bytes selected by the trusted
    owner controller, not files supplied by a peer. Their exact field contracts
    are checked above. The caller is responsible for the adopted actual checking
    and support-to-S argument. This function checks its concrete byte/identity
    premises and preserves that provenance without claiming a new kernel event.
    """
    source = LegacyReadOnly.open(source_directory, expected_source_manifest_raw,
                                parent_deadline=parent_deadline, limits=limits)
    destination = None
    try:
        implementation, correspondence = _correspondence(source, implementation_raw, correspondence_raw)
        files, manifest = source.files, source.manifest
        fresh_destination = C.ordinary(fresh_destination, directory=True, fresh=True)
        need(not fresh_destination.is_relative_to(source._root), "IMPORT_DESTINATION_INSIDE_SOURCE")
        need(type(catalog_limits) is C.Limits and len(source.records) <= catalog_limits.max_roots and
             limits.max_output_bytes <= catalog_limits.max_total_artifact_bytes,
             "IMPORT_DESTINATION_LIMITS")
        seed_raw = files.read(manifest["fixed_seed"], MIB)
        inventory_raw = files.read(manifest["fixed_inventory"], MIB)
        need(sha(seed_raw) == C.SEED == S.SEED and sha(inventory_raw) == C.INVENTORY == S.INVENTORY,
             "IMPORT_EXACT_FIXED_FOUNDATION")
        # Only these exact authenticated installed bytes use their Lean writer's
        # JSON spelling. They are not peer input and need not be Python canonical.
        seed, inventory = json.loads(seed_raw), json.loads(inventory_raw)
        need(type(seed) is list and len(seed) == 3 and type(seed[1]) is list and len(seed[1]) == 456 and
             type(seed[2]) is list and len(seed[2]) == 581 and type(inventory) is list and len(inventory) == 581,
             "IMPORT_FIXED_FOUNDATION_CENSUS")
        fixed_names = seed[2]
        need([row[0] for row in inventory] == fixed_names, "IMPORT_FIXED_INVENTORY_NAMES")
        legacy, portable = T.basis_pairs(manifest["profile_id"], manifest["basis_id"], fixed_names)
        legacy_basis = [[E.strict_json(key), symbol] for key, symbol in sorted(legacy.items())]
        portable_basis = [[E.strict_json(key), symbol] for key, symbol in sorted(portable.items())]
        need(source.records[0][1]["bindings"] == legacy_basis, "IMPORT_COMPLETE_ORIGINAL_BASIS")
        seconds = min(3600, math.floor(parent_deadline - time.monotonic()))
        need(seconds >= 1, "IMPORT_DEADLINE")
        destination, grant = P.PortableCatalog._create_importing(fresh_destination, implementation_raw,
            destination_store_id, limits=catalog_limits, seconds=seconds,
            output_bytes=limits.max_output_bytes, parent_deadline=parent_deadline)
        support = sorted({*(source.profile[key] for key in P.SOURCE_SUPPORT_FIELDS),
            *(pin["sha256"] for pin in manifest["check_support"]),
            *(pin["sha256"] for selected in manifest["roots"] for pin in selected["check_lineage"])})
        need(len(support) <= 128, "IMPORT_RETAINED_SUPPORT_BOUND")
        translation_support = implementation["controller_support"]
        records_raw, audit_roots, previous, total_nodes = [], [], "", 0
        summary_bytes = len(expected_source_manifest_raw) + len(E.canonical_json([legacy_basis, portable_basis]))
        new_record_bytes = 0
        for ordinal, (original_raw, original, artifact) in enumerate(source.records):
            files.live()
            directory = grant.directory / str(ordinal)
            C.ordinary(directory, directory=True, fresh=True).mkdir()
            files.write(directory / "source-record.json", original_raw)
            old_ids, new_ids, old_outputs, new_outputs, translations = [], [], [], [], []
            if ordinal == 0:
                new_outputs = portable_basis
            else:
                (directory / "evidence").mkdir()
                for index, pin in enumerate(manifest["roots"][ordinal]["evidence"]):
                    files.live()
                    raw = files.read(pin, E.DEFAULT_LIMITS.max_bytes)
                    translated = T.translate_unit(raw, manifest["profile_id"], legacy, portable)
                    total_nodes += translated.nodes
                    need(total_nodes <= limits.max_nodes, "IMPORT_TOTAL_NODE_BOUND")
                    old_rows = E.strict_json(translated.legacy_outputs_raw)
                    new_rows = E.strict_json(translated.portable_outputs_raw)
                    for old_row, new_row in zip(old_rows, new_rows):
                        need(old_row[0] == new_row[0], "IMPORT_TRANSLATED_OUTPUT_NAMES")
                        key = E.name_key(old_row[0])
                        legacy[key], portable[key] = old_row[1], new_row[1]
                    need(len(legacy) == len(portable) <= min(limits.max_names, catalog_limits.max_names),
                         "IMPORT_TOTAL_NAME_BOUND")
                    old_ids.append(translated.legacy_unit_id)
                    new_ids.append(translated.portable_unit_id)
                    old_outputs.extend(old_rows); new_outputs.extend(new_rows)
                    evidence_path = directory / "evidence" / (str(index) + ".json")
                    files.write(evidence_path, translated.raw)
                    entry = {"legacy_unit_id": translated.legacy_unit_id,
                        "portable_unit_id": translated.portable_unit_id,
                        "legacy_evidence_sha256": translated.legacy_evidence_sha256,
                        "unchanged_unit_sha256": translated.unchanged_unit_sha256,
                        "legacy_outputs": old_rows, "portable_outputs": new_rows,
                        "portable_evidence": {"relative_path": evidence_path.relative_to(destination._root).as_posix(),
                            "artifact_bytes": len(translated.raw), "artifact_sha256": sha(translated.raw)}}
                    summary_bytes += len(E.canonical_json(entry))
                    need(summary_bytes <= min(limits.max_manifest_bytes, catalog_limits.max_manifest_bytes),
                         "IMPORT_TRANSLATION_SUMMARY_BOUND")
                    translations.append(entry)
                    del raw, translated
                need(old_outputs == original["bindings"] and
                     C.digest("ordinary-batch-v1", old_ids) == original["request_hash"],
                     "IMPORT_COMPLETE_ORIGINAL_BATCH")
            local_root = P.legacy_root_id(destination.semantic_id, destination.foundation_id,
                destination_store_id, grant.identifier, original["root"], previous)
            files.copy(artifact, directory / "chunk.olean")
            row = {"schema": P.ROOT_SCHEMA, "local_root": local_root, "parent_root": previous,
                "kind": original["kind"], "semantic_id": destination.semantic_id,
                "foundation_id": destination.foundation_id, "input_unit_ids": new_ids,
                "request_hash": P.batch_id(new_ids) if ordinal else P.basis_request_id(
                    destination.semantic_id, destination.foundation_id), "bindings": new_outputs,
                "snapshot": {"module_name": C.module_name(original["root"]),
                    "parent_module": C.module_name(original["parent"]) if original["parent"] else [],
                    "relative_path": (directory / "chunk.olean").relative_to(destination._root).as_posix(),
                    "artifact_bytes": original["artifact_bytes"], "artifact_sha256": original["artifact_sha256"],
                    "writer_origin": "retained-v1-check"}, "origin": "legacy-translation",
                "provenance": {"import_id": grant.identifier, "ordinal": ordinal,
                    "source_store_id": manifest["store_id"], "source_profile_id": manifest["profile_id"],
                    "source_root": original["root"], "source_parent_root": original["parent"],
                    "source_record_sha256": sha(original_raw), "source_operation_id": original["operation"],
                    "source_check_support": support, "translation_support": translation_support}}
            encoded = E.canonical_json(row)
            need(len(encoded) <= min(limits.max_manifest_bytes, catalog_limits.max_manifest_bytes),
                 "IMPORT_NEW_RECORD_BOUND")
            new_record_bytes += len(encoded)
            need(new_record_bytes <= catalog_limits.max_batch_bytes, "IMPORT_NEW_RECORDS_BOUND")
            records_raw.append(encoded)
            audit_roots.append({"source_root": original["root"], "local_root": local_root,
                "source_record_sha256": sha(original_raw), "translated_record_sha256": sha(encoded),
                "legacy_unit_ids": old_ids, "portable_unit_ids": new_ids, "translations": translations})
            previous = local_root
        audit_raw = E.canonical_json({"schema": AUDIT_SCHEMA, "source_manifest": manifest,
            "correspondence_sha256": sha(correspondence_raw), "translation_support": translation_support,
            "basis_pairs": [[old, new] for old, new in zip(legacy_basis, portable_basis)],
            "roots": audit_roots, "total_names": len(portable), "total_nodes": total_nodes})
        need(len(audit_raw) <= min(limits.max_manifest_bytes, catalog_limits.max_manifest_bytes),
             "IMPORT_AUDIT_BOUND")
        files.write(grant.directory / "audit.json", audit_raw)
        files.write(grant.directory / "correspondence.json", correspondence_raw)
        imported = {"schema": P.IMPORT_SCHEMA, "import_id": grant.identifier,
            "semantic_id": destination.semantic_id, "foundation_id": destination.foundation_id,
            "implementation_id": destination.implementation_id, "store_id": destination_store_id,
            "source_store_id": manifest["store_id"], "source_profile": source.profile,
            "source_selected_root": manifest["selected_root"], "source_manifest_sha256": sha(expected_source_manifest_raw),
            "correspondence_sha256": sha(correspondence_raw), "translation_support": translation_support,
            "source_check_support": support, "retained_support": sorted(set(support + [translation_support] +
                [implementation[key] for key in P.SUPPORT_FIELDS])),
            "roots": [[root["local_root"], sha(raw)] for root, raw in zip(audit_roots, records_raw)],
            "audit": {"relative_path": "imports/" + grant.identifier + "/audit.json",
                "artifact_bytes": len(audit_raw), "artifact_sha256": sha(audit_raw)}}
        selected = destination._activate_import(grant, records_raw, E.canonical_json(imported),
                                                source_recheck=source.assert_unchanged)
        return {"local_root": selected, "basis_root": imported["roots"][0][0],
                "semantic_id": destination.semantic_id, "foundation_id": destination.foundation_id,
                "implementation_id": destination.implementation_id, "import_id": grant.identifier,
                "source_root": manifest["selected_root"], "names": len(portable),
                "roots": len(records_raw), "output_bytes": files.output_bytes}
    finally:
        if destination is not None:
            destination.close()
        source.close()

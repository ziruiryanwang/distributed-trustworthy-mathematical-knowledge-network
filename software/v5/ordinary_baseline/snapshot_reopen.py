"""Revalidate retained original-library bytes, without accepting mathematics.

The caller authenticates the manifest identity through its current protected
realization and holds that owner's lock. A caller-supplied hash or this inert
return value alone is not a warrant. No original project path is opened, no
binary is imported and no proof history is decoded. The same validation is
usable before/after live correspondence and when loading a protected reference.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path

import ordinary_admission as A
import baseline_snapshot as S


MIB = 1024**2


@dataclass(frozen=True)
class SnapshotView:
    directory: Path
    manifest_raw: bytes
    manifest_sha256: str
    replay_raw: bytes
    source_report_raw: bytes
    # Exact ordered roots and file pins; immutable bytes avoid nested aliases.
    root_imports_raw: bytes
    module_keys: tuple[bytes, ...]
    part_pins: tuple[tuple[Path, int, str], ...]
    artifact_bytes: int


def _read(path, maximum, check):
    check()
    raw = A.C.read_bounded(path, maximum)
    A.need(0 < len(raw) <= maximum, "REFERENCE_SNAPSHOT_EMPTY_FILE")
    check()
    return raw


def _census(directory, files, directories, check):
    """Exact finite retained tree; refuse links and unselected extra entries."""
    pending, seen_files, seen_dirs = [directory], set(), {directory}
    while pending:
        current = A.C.ordinary(pending.pop(), directory=True)
        # Iterate rather than materialize an unbounded foreign directory.
        for path in current.iterdir():
            check()
            if path.is_dir():
                A.need(path in directories and path not in seen_dirs,
                       "REFERENCE_SNAPSHOT_DIRECTORY_CENSUS")
                A.C.ordinary(path, directory=True)
                seen_dirs.add(path)
                pending.append(path)
            else:
                A.need(path in files and path not in seen_files,
                       "REFERENCE_SNAPSHOT_FILE_CENSUS")
                A.C.ordinary(path)
                seen_files.add(path)
    A.need(seen_files == files and seen_dirs == directories,
           "REFERENCE_SNAPSHOT_MISSING_ENTRY")


def read_snapshot(directory, manifest_sha256, installation_manifest_sha256, *, check_budget):
    """Check one exact immutable snapshot, never register or reconstruct it.

    Hashing costs O(selected artifact bytes); parsing costs O(module metadata).
    There is no mathematical proof replay here. The selected installation and
    protected store, not this function, establish the authority of the inputs.
    """
    A.need(S.A is A and callable(check_budget), "REFERENCE_SNAPSHOT_CONFIGURATION")
    check = check_budget
    check()
    A.C.hexid(manifest_sha256)
    A.C.hexid(installation_manifest_sha256)
    directory = A.C.ordinary(Path(directory), directory=True)
    manifest_raw = _read(directory/"prepared-manifest.json", S.MAX_MANIFEST, check)
    A.need(A.sha(manifest_raw) == manifest_sha256, "REFERENCE_SNAPSHOT_MANIFEST_PIN")
    manifest = A.E.strict_json(manifest_raw, A.E.Limits(max_bytes=S.MAX_MANIFEST))
    S._fields(manifest, ("schema", "status", "mathematical_acceptance",
        "installation_manifest_sha256", "project_selection_sha256", "source_report_sha256",
        "replay_request_sha256", "roots", "modules", "artifact_bytes", "module_count",
        "part_count"), "REFERENCE_SNAPSHOT_MANIFEST_FIELDS")
    A.need(manifest["schema"] == S.SNAPSHOT_SCHEMA and
           manifest["status"] == "PREPARED_NOT_REPLAYED_OR_REGISTERED" and
           type(manifest["mathematical_acceptance"]) is int and
           manifest["mathematical_acceptance"] == 0 and
           manifest["installation_manifest_sha256"] == installation_manifest_sha256,
           "REFERENCE_SNAPSHOT_MANIFEST_BINDING")
    for role in ("project_selection_sha256", "source_report_sha256", "replay_request_sha256"):
        A.C.hexid(manifest[role])
    replay_raw = _read(directory/"replay-request.json", S.MAX_REQUEST, check)
    source_raw = _read(directory/"source-report.json", S.MAX_REPORT, check)
    A.need(A.sha(replay_raw) == manifest["replay_request_sha256"] and
           A.sha(source_raw) == manifest["source_report_sha256"],
           "REFERENCE_SNAPSHOT_METADATA_PIN")
    replay = A.E.strict_json(replay_raw, A.E.Limits(max_bytes=S.MAX_REQUEST))
    S._fields(replay, ("schema", "mode", "modules", "artifacts"),
              "REFERENCE_SNAPSHOT_REPLAY_FIELDS")
    A.need(replay["schema"] == S.REQUEST_SCHEMA and replay["mode"] == "replay",
           "REFERENCE_SNAPSHOT_REPLAY_SCHEMA")
    roots = A.E._array(manifest["roots"], maximum=16)
    root_keys = [S._import(row) for row in roots]
    A.need(bool(roots) and len(set(root_keys)) == len(roots) and
           all(row["import_all"] == 0 and row["is_exported"] == 1 and row["is_meta"] == 0
               for row in roots) and replay["modules"] == [row["module"] for row in roots],
           "REFERENCE_SNAPSHOT_ROOTS")
    rows = A.E._array(manifest["modules"], maximum=S.MAX_MODULES)
    artifacts = A.E._array(replay["artifacts"], len(rows))
    A.need(bool(rows), "REFERENCE_SNAPSHOT_EMPTY_MODULES")
    source = A._writer_json(source_raw, S.MAX_REPORT)
    S._fields(source, ("schema", "assurance", "mode", "roots", "modules", "module_count",
        "part_count", "direct_import_edges", "artifact_bytes"), "REFERENCE_SNAPSHOT_SOURCE_FIELDS")
    A.need(source["schema"] == S.REPORT_SCHEMA and source["mode"] == "collect" and
           source["assurance"] == "INERT_ARTIFACT_CLOSURE_NOT_MATHEMATICAL_ACCEPTANCE" and
           source["roots"] == roots, "REFERENCE_SNAPSHOT_SOURCE_BINDING")
    original_rows = A.E._array(source["modules"], len(rows))
    originals = {}
    for row in original_rows:
        check()
        S._fields(row, ("module", "is_module", "imports", "effective", "parts", "part_bytes"),
                  "REFERENCE_SNAPSHOT_SOURCE_MODULE_FIELDS")
        key, _ = S._module(row["module"])
        A.need(key not in originals and type(row["is_module"]) is int and row["is_module"] == 1,
               "REFERENCE_SNAPSHOT_SOURCE_MODULE")
        # Original paths are provenance data, never reopened after registration.
        for path in S._matrix(row["parts"]):
            A.need(type(path) is str, "REFERENCE_SNAPSHOT_SOURCE_PATH_TYPE")
        originals[key] = row
    files = {directory/name for name in ("prepared-manifest.json", "replay-request.json", "source-report.json")}
    directories = {directory, directory/"modules"}
    pins, modules, edge_count, total = [], {}, 0, 0
    for row, artifact in zip(rows, artifacts):
        check()
        S._fields(row, ("module", "imports", "effective", "parts", "pins"),
                  "REFERENCE_SNAPSHOT_MODULE_FIELDS")
        S._fields(artifact, ("module", "parts"), "REFERENCE_SNAPSHOT_ARTIFACT_FIELDS")
        key, _ = S._module(row["module"])
        A.need(key not in modules and key in originals and
               artifact == {"module": row["module"], "parts": row["parts"]},
               "REFERENCE_SNAPSHOT_REPLAY_MODULE")
        original = originals[key]
        A.need(row["imports"] == original["imports"] and row["effective"] == original["effective"],
               "REFERENCE_SNAPSHOT_SOURCE_MODULE_BINDING")
        effective = row["effective"]
        S._fields(effective, ("import_all", "is_exported", "is_meta", "has_data", "ir_phases"),
                  "REFERENCE_SNAPSHOT_EFFECTIVE_FIELDS")
        for flag in ("import_all", "is_exported", "is_meta", "has_data"):
            S._uint(effective[flag], 0, 1, "REFERENCE_SNAPSHOT_EFFECTIVE_FLAG")
        A.need(effective["import_all"] == effective["has_data"] == 1 and
               effective["ir_phases"] in ("runtime", "comptime", "all"),
               "REFERENCE_SNAPSHOT_PRIVATE_DATA")
        imports = A.E._array(row["imports"], maximum=S.MAX_EDGES)
        edge_count += len(imports)
        A.need(edge_count <= S.MAX_EDGES, "REFERENCE_SNAPSHOT_EDGE_BOUND")
        modules[key] = {S._import(item) for item in imports}
        part_dir = directory/"modules"/A.sha(key)
        directories.add(part_dir)
        for path_text, pin, size, suffix in zip(S._matrix(row["parts"]), S._matrix(row["pins"]),
                S._matrix(original["part_bytes"]), S.SUFFIXES):
            path = part_dir/("module"+suffix)
            S._fields(pin, ("bytes", "sha256"), "REFERENCE_SNAPSHOT_PART_PIN_FIELDS")
            S._uint(pin["bytes"], 1, S.MAX_PART, "REFERENCE_SNAPSHOT_PART_BOUND")
            S._uint(size, 1, S.MAX_PART, "REFERENCE_SNAPSHOT_SOURCE_PART_BOUND")
            A.C.hexid(pin["sha256"])
            A.need(path_text == str(path) and pin["bytes"] == size and path not in files,
                   "REFERENCE_SNAPSHOT_EXACT_PART_PATH")
            total += size
            A.need(total <= S.MAX_ARTIFACTS, "REFERENCE_SNAPSHOT_ARTIFACT_BOUND")
            files.add(path)
            pins.append((path, size, pin["sha256"]))
    A.need(modules.keys() == originals.keys(), "REFERENCE_SNAPSHOT_SOURCE_CENSUS")
    for document in (manifest, source):
        for field, expected, ceiling in (("module_count", len(rows), S.MAX_MODULES),
                ("part_count", len(pins), 5*S.MAX_MODULES), ("artifact_bytes", total, S.MAX_ARTIFACTS)):
            S._uint(document[field], 1, ceiling, "REFERENCE_SNAPSHOT_CENSUS_TYPE")
            A.need(document[field] == expected, "REFERENCE_SNAPSHOT_CENSUS")
    S._uint(source["direct_import_edges"], 0, S.MAX_EDGES, "REFERENCE_SNAPSHOT_EDGE_CENSUS_TYPE")
    A.need(source["direct_import_edges"] == edge_count, "REFERENCE_SNAPSHOT_EDGE_CENSUS")
    users, degree = {key: set() for key in modules}, {}
    for key, dependencies in modules.items():
        check()
        A.need(dependencies <= modules.keys(), "REFERENCE_SNAPSHOT_MISSING_DEPENDENCY")
        degree[key] = len(dependencies)
        for dependency in dependencies:
            users[dependency].add(key)
    ready, visited = deque(key for key, value in degree.items() if value == 0), 0
    while ready:
        check()
        key = ready.popleft()
        visited += 1
        for user in users[key]:
            degree[user] -= 1
            if degree[user] == 0:
                ready.append(user)
    A.need(visited == len(modules), "REFERENCE_SNAPSHOT_IMPORT_CYCLE")
    pending, reached = list(root_keys), set()
    while pending:
        check()
        key = pending.pop()
        A.need(key in modules, "REFERENCE_SNAPSHOT_ROOT_MISSING")
        if key not in reached:
            reached.add(key)
            pending.extend(modules[key]-reached)
    A.need(reached == modules.keys(), "REFERENCE_SNAPSHOT_UNUSED_MODULE")
    _census(directory, files, directories, check)
    for path, size, digest in pins:
        A.need(S._hash_exact(path, size, check) == digest, "REFERENCE_SNAPSHOT_PART_CHANGED")
    # Fail closed on metadata changes observed during validation. Protected-store
    # immutability and no hostile local administrator are still premises.
    for name, raw, maximum in (("prepared-manifest.json", manifest_raw, S.MAX_MANIFEST),
            ("replay-request.json", replay_raw, S.MAX_REQUEST),
            ("source-report.json", source_raw, S.MAX_REPORT)):
        A.need(_read(directory/name, maximum, check) == raw, "REFERENCE_SNAPSHOT_METADATA_CHANGED")
    _census(directory, files, directories, check)
    check()
    return SnapshotView(directory, manifest_raw, manifest_sha256, replay_raw, source_raw,
        A.E.canonical_json(roots), tuple(modules), tuple(pins), total)

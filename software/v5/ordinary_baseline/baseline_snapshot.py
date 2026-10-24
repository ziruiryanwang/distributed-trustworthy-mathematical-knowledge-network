"""Prepare exact local artifact bytes for later replay and correspondence.

No import, native execution, owner/catalog access or reference registration.
The input is an inert locator report for an explicitly approved local library.
Copied bytes remain untrusted mathematics until the separate live correspondence
operation matches independently warranted declarations. A manifest is not a
replayable acceptance token. Caller owns partial output and the enclosing budget.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re

import ordinary_admission as A
import library_extraction as X

MIB = 1024**2
REPORT_SCHEMA = "DMKN_ORDINARY_BASELINE_ARTIFACT_REPORT_V1"
REQUEST_SCHEMA = "DMKN_ORDINARY_BASELINE_ARTIFACT_REQUEST_V1"
SNAPSHOT_SCHEMA = "DMKN_ORDINARY_PREPARED_BASELINE_SNAPSHOT_V1"
SUFFIXES = (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir")
MAX_MODULES, MAX_EDGES = 4096, 65536
MAX_PART, MAX_ARTIFACTS = 64*MIB, 512*MIB
MAX_REPORT, MAX_REQUEST, MAX_MANIFEST = 16*MIB, 16*MIB, 32*MIB
METADATA_RESERVATION = MAX_REPORT+MAX_REQUEST+MAX_MANIFEST


@dataclass(frozen=True)
class PreparedSnapshot:
    """Inert convenience result, not a protected reference or mathematical root."""
    directory: Path
    manifest_raw: bytes
    manifest_sha256: str
    replay_request_raw: bytes
    artifact_bytes: int
    total_bytes: int


def _fields(value, names, code):
    A.need(type(value) is dict and set(value) == set(names), code)


def _uint(value, low, high, code):
    A.need(type(value) is int and low <= value <= high, code)
    return value


def _module(name):
    # Exactly the approved-project spelling rule, applied to every transitive
    # module rather than just the <=16 root modules.
    selected = X.selected_modules([name], installed_std=False)
    key = A.E.name_key(selected[0])
    return key, tuple(bytes(part[1]["$bytes"]).decode("ascii") for part in selected[0])


def _matrix(value):
    rows = A.E._array(value, 2)
    return tuple(A.E._array(rows[0], 3)+A.E._array(rows[1], 2))


def _as_matrix(values):
    return [list(values[:3]), list(values[3:])]


def _drive_path(raw):
    # Validate the spelling before Path can erase dot components or reinterpret
    # drive/UNC/device namespaces. Native reports must have stripped only their
    # own extended-drive lookup prefix.
    A.need(os.name == "nt" and type(raw) is str and 0 < len(raw.encode("utf-8")) <= 32768
           and re.match(r"^[A-Za-z]:[\\/]", raw) is not None
           and all(ord(c) >= 32 for c in raw) and ";" not in raw,
           "BASELINE_SNAPSHOT_PATH_SPELLING")
    parts = [part for part in re.split(r"[\\/]", raw[3:]) if part]
    A.need(len(parts)+1 <= 128 and all(part not in (".", "..") for part in parts),
           "BASELINE_SNAPSHOT_PATH_COMPONENTS")
    return Path(raw)


def _import(row):
    _fields(row, ("module", "import_all", "is_exported", "is_meta"),
            "BASELINE_SNAPSHOT_IMPORT_FIELDS")
    key, _ = _module(row["module"])
    for name in ("import_all", "is_exported", "is_meta"):
        _uint(row[name], 0, 1, "BASELINE_SNAPSHOT_IMPORT_FLAG")
    return key


def _first_resolved(parts, roots, check):
    """Match Lean.Util.Path.findWithExt's first package-prefix resolution."""
    for root in roots:
        check()
        prefix = root/parts[0]
        prefix_file = prefix.with_suffix(".olean")
        if prefix.is_dir() or prefix_file.exists():
            if prefix.is_dir():
                A.C.ordinary(prefix, directory=True)
            else:
                A.C.ordinary(prefix_file)
            base = root.joinpath(*parts).with_suffix(".olean")
            # Lean chooses the first root with A/ or A.olean, not the first
            # complete A/B.olean file. A missing later component must refuse;
            # it may not silently choose a later shadowed package.
            return A.C.ordinary(base)
    A.need(False, "BASELINE_SNAPSHOT_UNRESOLVED_MODULE")


def validate_collected_report(raw, expected_sha256, *, project, roots, check):
    """Validate locators and graph, not the declarations inside their files."""
    A.need(callable(check) and type(raw) is bytes and 0 < len(raw) <= MAX_REPORT,
           "BASELINE_SNAPSHOT_REPORT_BOUND")
    A.C.hexid(expected_sha256)
    check()
    A.need(A.sha(raw) == expected_sha256, "BASELINE_SNAPSHOT_REPORT_PIN")
    # Selected native output need not use the peer codec's canonical key order.
    # Preserve its exact raw hash while retaining duplicate/token/depth bounds.
    report = A._writer_json(raw, MAX_REPORT)
    _fields(report, ("schema", "assurance", "mode", "roots", "modules", "module_count",
                    "part_count", "direct_import_edges", "artifact_bytes"),
            "BASELINE_SNAPSHOT_REPORT_FIELDS")
    A.need(report["schema"] == REPORT_SCHEMA and report["mode"] == "collect" and
           report["assurance"] == "INERT_ARTIFACT_CLOSURE_NOT_MATHEMATICAL_ACCEPTANCE",
           "BASELINE_SNAPSHOT_REPORT_KIND")
    # Root imports are the selected collector's unchanged default Import flags.
    expected_roots = [{"module": name, "import_all": 0, "is_exported": 1, "is_meta": 0}
                      for name in project["modules"]]
    A.need(report["roots"] == expected_roots, "BASELINE_SNAPSHOT_ROOT_SELECTION")
    root_keys = [_import(row) for row in report["roots"]]
    rows = A.E._array(report["modules"], maximum=MAX_MODULES)
    A.need(bool(rows), "BASELINE_SNAPSHOT_EMPTY_MODULES")
    modules, all_paths, total, edges = {}, set(), 0, 0
    for row in rows:
        check()
        _fields(row, ("module", "is_module", "imports", "effective", "parts", "part_bytes"),
                "BASELINE_SNAPSHOT_MODULE_FIELDS")
        key, components = _module(row["module"])
        A.need(key not in modules, "BASELINE_SNAPSHOT_DUPLICATE_MODULE")
        _uint(row["is_module"], 1, 1, "BASELINE_SNAPSHOT_MODERN_MODULE")
        effective = row["effective"]
        _fields(effective, ("import_all", "is_exported", "is_meta", "has_data", "ir_phases"),
                "BASELINE_SNAPSHOT_EFFECTIVE_FIELDS")
        for flag in ("import_all", "is_exported", "is_meta", "has_data"):
            _uint(effective[flag], 0, 1, "BASELINE_SNAPSHOT_EFFECTIVE_FLAG")
        A.need(effective["import_all"] == effective["has_data"] == 1 and
               effective["ir_phases"] in ("runtime", "comptime", "all"),
               "BASELINE_SNAPSHOT_PRIVATE_DATA_REQUIRED")
        imports = A.E._array(row["imports"], maximum=MAX_EDGES)
        edges += len(imports)
        A.need(edges <= MAX_EDGES, "BASELINE_SNAPSHOT_EDGE_BOUND")
        dependencies = set()
        for entry in imports:
            check()
            dependencies.add(_import(entry))
        base = _first_resolved(components, roots, check)
        expected_parts = tuple(base.with_suffix(suffix) for suffix in SUFFIXES)
        paths = tuple(_drive_path(path) for path in _matrix(row["parts"]))
        A.need(paths == expected_parts, "BASELINE_SNAPSHOT_APPROVED_RESOLUTION")
        sizes = _matrix(row["part_bytes"])
        for path, size in zip(paths, sizes):
            check()
            _uint(size, 1, MAX_PART, "BASELINE_SNAPSHOT_PART_BOUND")
            A.need(path not in all_paths, "BASELINE_SNAPSHOT_PATH_ALIAS")
            path = A.C.ordinary(path)
            A.need(path.stat().st_size == size, "BASELINE_SNAPSHOT_SOURCE_SIZE")
            all_paths.add(path)
            total += size
            A.need(total <= MAX_ARTIFACTS, "BASELINE_SNAPSHOT_ARTIFACT_BOUND")
        modules[key] = {"row": row, "paths": paths, "sizes": sizes, "dependencies": dependencies}
    for field, actual, ceiling in (("module_count", len(modules), MAX_MODULES),
            ("part_count", len(all_paths), 5*MAX_MODULES),
            ("direct_import_edges", edges, MAX_EDGES), ("artifact_bytes", total, MAX_ARTIFACTS)):
        _uint(report[field], 0, ceiling, "BASELINE_SNAPSHOT_CENSUS_TYPE")
        A.need(report[field] == actual, "BASELINE_SNAPSHOT_CENSUS_MISMATCH")
    # Exact closure and acyclicity are inexpensive metadata obligations. Neither
    # proves the binary importer actually sees this graph; live replay must agree.
    users = {key: set() for key in modules}
    degree = {}
    for key, item in modules.items():
        check()
        A.need(item["dependencies"] <= modules.keys(), "BASELINE_SNAPSHOT_MISSING_DEPENDENCY")
        degree[key] = len(item["dependencies"])
        for dependency in item["dependencies"]:
            users[dependency].add(key)
    pending = deque(key for key, count in degree.items() if count == 0)
    ordered = []
    while pending:
        check()
        key = pending.popleft()
        ordered.append(key)
        for user in sorted(users[key]):
            degree[user] -= 1
            if degree[user] == 0:
                pending.append(user)
    A.need(len(ordered) == len(modules), "BASELINE_SNAPSHOT_IMPORT_CYCLE")
    reached, pending = set(), list(root_keys)
    while pending:
        check()
        key = pending.pop()
        A.need(key in modules, "BASELINE_SNAPSHOT_ROOT_MISSING")
        if key not in reached:
            reached.add(key)
            pending.extend(modules[key]["dependencies"]-reached)
    A.need(reached == modules.keys(), "BASELINE_SNAPSHOT_UNUSED_MODULE")
    return report, tuple(modules[key] for key in ordered), total


def _hash_exact(path, size, check):
    A.C.ordinary(path)
    A.need(path.stat().st_size == size, "BASELINE_SNAPSHOT_PIN_SIZE")
    count, digest = 0, hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(min(MIB, size+1-count)):
            check()
            count += len(chunk)
            A.need(count <= size, "BASELINE_SNAPSHOT_INPUT_GREW")
            digest.update(chunk)
    check()
    A.need(count == size and path.stat().st_size == size, "BASELINE_SNAPSHOT_INPUT_CHANGED")
    return digest.hexdigest()


def _copy_exact(source, destination, size, check):
    expected = _hash_exact(source, size, check)
    destination = A.C.ordinary(destination, fresh=True)
    count, digest = 0, hashlib.sha256()
    with source.open("rb") as incoming, destination.open("xb") as outgoing:
        while chunk := incoming.read(min(MIB, size+1-count)):
            check()
            count += len(chunk)
            A.need(count <= size, "BASELINE_SNAPSHOT_COPY_GREW")
            outgoing.write(chunk)
            digest.update(chunk)
        outgoing.flush()
        os.fsync(outgoing.fileno())
    A.need(count == size and digest.hexdigest() == expected and
           _hash_exact(source, size, check) == expected and
           _hash_exact(destination, size, check) == expected,
           "BASELINE_SNAPSHOT_COPY_CHANGED")
    return {"bytes": size, "sha256": expected}


def _write(path, raw, maximum, check):
    check()
    A.need(type(raw) is bytes and 0 < len(raw) <= maximum, "BASELINE_SNAPSHOT_METADATA_BOUND")
    path = A.C.ordinary(path, fresh=True)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    check()
    A.need(A.C.read_bounded(path, maximum) == raw, "BASELINE_SNAPSHOT_METADATA_CHANGED")


def prepare_snapshot(installation, *, project_selection_raw, project_selection_sha256,
                     report_raw, report_sha256, output_directory, spool_bytes, check_budget):
    """Copy fresh approved inputs once; retain all outputs on any exception.

    The check callback charges the original enclosing allocation. It must cover
    this controller and all prior/future phases, not renew a native allowance.
    Spool reservation is a cooperative bound on selected output, not a hard disk
    quota or protection against a hostile local writer. Even a returned result
    remains pending exact replay/private-public correspondence and registration.
    """
    A.need(type(installation) is A.NativeInstallation and X.A is A and callable(check_budget),
           "BASELINE_SNAPSHOT_CONFIGURATION")
    check = check_budget
    check()
    project, project_roots = X.selected_project(project_selection_raw, project_selection_sha256, check)
    runtime = A.C.ordinary(installation.runtime_roots["lean_runtime"], directory=True)
    roots = (A.C.ordinary(runtime/"lib/lean", directory=True), *project_roots)
    report, entries, artifact_bytes = validate_collected_report(report_raw, report_sha256,
        project=project, roots=roots, check=check)
    _uint(spool_bytes, 1, MAX_ARTIFACTS+METADATA_RESERVATION, "BASELINE_SNAPSHOT_SPOOL_ALLOWANCE")
    A.need(spool_bytes >= artifact_bytes+METADATA_RESERVATION, "BASELINE_SNAPSHOT_SPOOL_RESERVATION")
    output = A.C.ordinary(Path(output_directory), directory=True, fresh=True)
    package = A.C.ordinary(Path(__file__).absolute().parent.parent, directory=True)
    for root in (package, installation.root, *installation.runtime_roots.values(), *project_roots):
        root = A.C.ordinary(root, directory=True)
        A.need(not output.is_relative_to(root) and not root.is_relative_to(output),
               "BASELINE_SNAPSHOT_OUTPUT_OVERLAP")
    check()
    output.mkdir()
    modules_directory = output/"modules"
    modules_directory.mkdir()
    copied, replay = [], []
    for item in entries:
        check()
        row = item["row"]
        key, _ = _module(row["module"])
        stem = A.sha(key)
        directory = A.C.ordinary(modules_directory/stem, directory=True, fresh=True)
        directory.mkdir()
        paths, pins = [], []
        for suffix, source, size in zip(SUFFIXES, item["paths"], item["sizes"]):
            destination = directory/("module"+suffix)
            pin = _copy_exact(source, destination, size, check)
            paths.append(str(destination))
            pins.append(pin)
        replay.append({"module": row["module"], "parts": _as_matrix(paths)})
        copied.append({"module": row["module"], "imports": row["imports"],
            "effective": row["effective"], "parts": _as_matrix(paths), "pins": _as_matrix(pins)})
    replay_raw = A.E.canonical_json({"schema": REQUEST_SCHEMA, "mode": "replay",
        "modules": project["modules"], "artifacts": replay})
    manifest_raw = A.E.canonical_json({"schema": SNAPSHOT_SCHEMA,
        "status": "PREPARED_NOT_REPLAYED_OR_REGISTERED", "mathematical_acceptance": 0,
        "installation_manifest_sha256": installation.manifest_sha256,
        "project_selection_sha256": project_selection_sha256,
        "source_report_sha256": report_sha256,
        "replay_request_sha256": A.sha(replay_raw), "roots": report["roots"], "modules": copied,
        "artifact_bytes": artifact_bytes, "module_count": len(copied), "part_count": 5*len(copied)})
    # All three metadata bounds are checked before creating any metadata file.
    A.need(len(replay_raw) <= MAX_REQUEST and len(manifest_raw) <= MAX_MANIFEST,
           "BASELINE_SNAPSHOT_FINAL_METADATA_BOUND")
    total = artifact_bytes+len(report_raw)+len(replay_raw)+len(manifest_raw)
    A.need(total <= spool_bytes, "BASELINE_SNAPSHOT_FINAL_SPOOL_BOUND")
    _write(output/"source-report.json", report_raw, MAX_REPORT, check)
    _write(output/"replay-request.json", replay_raw, MAX_REQUEST, check)
    # A prepared-manifest write is the last required file, never registration.
    # A late exception may leave it present; no saved label establishes success.
    _write(output/"prepared-manifest.json", manifest_raw, MAX_MANIFEST, check)
    check()
    return PreparedSnapshot(output, manifest_raw, A.sha(manifest_raw), replay_raw, artifact_bytes, total)

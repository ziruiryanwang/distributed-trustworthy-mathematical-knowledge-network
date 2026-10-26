"""Bounded exact custody-to-baseline copy, never source or receiver acceptance.

The approved caller authenticates pure codecs, inventory and local paths, and
supplies one original budget plus outer containment. No native, owner, network,
project or peer code is loaded here. Protected supported SQLite files are inputs.
"""
from collections import deque
import hashlib
import heapq
import json
import os
from pathlib import Path
import sqlite3
import stat
import time

MIB = 1024**2
CEILINGS = {"units": 1024, "bytes": 64*MIB, "nodes": 2097152, "names": 65536,
            "edges": 262144, "locator_reads": 65536, "locator_bytes": 64*MIB,
            "output_bytes": 68*MIB}
CUSTODY_BOUNDS = {"objects": (1, 1000000), "exports": (1, 16000000),
                  "logical_bytes": (1024, 2**40), "db_pages": (256, 268435456)}
STORE_SCHEMA = "DMKN_ORDINARY_INERT_CUSTODY_V1"
RESULT_SCHEMA = "DMKN_ORDINARY_SELECTED_EXPORT_RESULT_V1"


def need(condition, code):
    if not condition:
        raise ValueError("SELECTED_EXPORT_"+code)


def ordinary(value, *, directory=True, fresh=False):
    path = Path(value)
    need(path.is_absolute() and path != Path(path.anchor), "ABSOLUTE_NONROOT_PATH")
    for part in path.parts[1:]:
        need(part not in (".", "..") and not part.endswith((".", " ")) and
             not any(ord(c) < 32 or c in ':*?"<>|' for c in part) and
             not (os.name == "nt" and os.path.isreserved(part)), "ORDINARY_PATH")
    start = path.parent if fresh else path
    for item in (start, *start.parents):
        info = item.lstat()
        need(not stat.S_ISLNK(info.st_mode) and
             not getattr(info, "st_file_attributes", 0) & 0x400, "REPARSE_PATH")
    need(start.resolve(strict=True) == start, "CANONICAL_PATH")
    if fresh:
        need(not os.path.lexists(path) and start.is_dir(), "FRESH_PATH")
    else:
        need(path.is_dir() if directory else path.is_file(), "PATH_KIND")
    return path


def validate_limits(custody_limits, limits):
    need(type(limits) is dict and set(limits) == set(CEILINGS), "LIMIT_FIELDS")
    for name, ceiling in CEILINGS.items():
        need(type(limits[name]) is int and 0 < limits[name] <= ceiling, "LIMIT:"+name)
    need(type(custody_limits) is dict and set(custody_limits) == set(CUSTODY_BOUNDS),
         "CUSTODY_LIMIT_FIELDS")
    for name, (low, high) in CUSTODY_BOUNDS.items():
        need(type(custody_limits[name]) is int and low <= custody_limits[name] <= high,
             "CUSTODY_LIMIT:"+name)


class ReadCustody:
    """One finite SQLite read snapshot; no owner/catalog and no recovery writes."""
    def __init__(self, root, semantic, custody_limits, api, limits, counts, check):
        self.db = None
        self.root, self.semantic = root, semantic
        self.api, self.limits, self.counts, self.check = api, limits, counts, check
        path = ordinary(root/"ordinary.sqlite", directory=False)
        size = path.stat()
        need(size.st_nlink == 1 and 0 < size.st_size <= custody_limits["db_pages"]*4096,
             "DATABASE_BOUND")
        for suffix in ("-wal", "-shm", "-journal"):
            need(not os.path.lexists(str(path)+suffix), "SOURCE_NEEDS_RECOVERY")
        check()
        try:
            self.db = sqlite3.connect(path.as_uri()+"?mode=ro", uri=True,
                                      isolation_level=None, timeout=1)
            def progress():
                try:
                    check()
                    return 0
                except BaseException:
                    return 1
            self.db.set_progress_handler(progress, 1000)
            for pragma in ("query_only=ON", "trusted_schema=OFF", "mmap_size=0",
                           "temp_store=MEMORY", "cache_size=-2048"):
                self.db.execute("PRAGMA "+pragma)
            need(self.one("PRAGMA journal_mode") == ("delete",), "JOURNAL_MODE")
            need(self.one("PRAGMA page_size") == (4096,), "PAGE_SIZE")
            self.db.execute("BEGIN")
            cfg = api.E.canonical_json({"schema": STORE_SCHEMA, "semantic_id": semantic,
                                       "limits": custody_limits})
            need(self.one("SELECT length(cfg) FROM meta WHERE id=1") == (len(cfg),),
                 "CONFIG_SIZE")
            need(self.one("SELECT cfg FROM meta WHERE id=1") == (cfg,), "CONFIG")
            row = self.one("SELECT objects,exports,logical_bytes FROM meta WHERE id=1")
            need(row is not None and all(type(value) is int and 0 <= value <= custody_limits[key]
                 for key, value in zip(("objects", "exports", "logical_bytes"), row)), "STORE_COUNTS")
            check()
        except BaseException:
            self.close()
            raise

    def one(self, sql, args=()):
        self.check()
        value = self.db.execute(sql, args).fetchone()
        self.check()
        return value

    def locator(self, name, identity):
        self.counts["locator_reads"] += 1
        need(self.counts["locator_reads"] <= self.limits["locator_reads"], "LOCATOR_READ_BOUND")
        row = self.one("SELECT length(unit_id),length(locator) FROM exports WHERE export_id=?",
                       (identity,))
        remaining = min(MIB, self.limits["locator_bytes"]-self.counts["locator_bytes"])
        need(row is not None and row[0] == 64 and type(row[1]) is int and
             0 < row[1] <= remaining, "LOCATOR_UNAVAILABLE_OR_BOUND")
        held = self.one("SELECT unit_id,locator FROM exports WHERE export_id=?", (identity,))
        need(held is not None and type(held[1]) is bytes and len(held[1]) == row[1], "LOCATOR_BYTES")
        self.counts["locator_bytes"] += len(held[1])
        value = self.api.PP.read_locator(self.api.E.strict_json(held[1]))
        need(value["semantic_id"] == self.semantic and value["unit_id"] == held[0] and
             self.api.E.name_key(value["export_name"]) == self.api.E.name_key(name) and
             self.api.S.export_id(self.semantic, held[0], name) == identity, "LOCATOR_BINDING")
        return held[0]

    def evidence(self, unit):
        remaining = min(8*MIB, self.limits["bytes"]-self.counts["evidence_bytes"])
        row = self.one("SELECT length(raw),length(raw_sha256) FROM objects WHERE kind='evidence' AND identity=?",
                       (unit,))
        need(row is not None and type(row[0]) is int and 0 < row[0] <= remaining and row[1] == 64,
             "EVIDENCE_UNAVAILABLE_OR_BOUND")
        held = self.one("SELECT raw,raw_sha256 FROM objects WHERE kind='evidence' AND identity=?", (unit,))
        need(held is not None and type(held[0]) is bytes and len(held[0]) == row[0] and
             hashlib.sha256(held[0]).hexdigest() == held[1], "EVIDENCE_RAW_BINDING")
        self.counts["evidence_bytes"] += len(held[0])
        parsed = self.api.PE.read_evidence(held[0])
        need(parsed.unit_id == unit and parsed.document["semantic_id"] == self.semantic,
             "EVIDENCE_IDENTITY")
        self.check()
        return parsed

    def close(self):
        if self.db is not None:
            try:
                if self.db.in_transaction:
                    self.db.rollback()
            finally:
                self.db.close()
                self.db = None


def export_selected(custody_root, targets, output_directory, *, api, inventory_raw,
                    custody_limits, limits, check_budget, protected_paths=()):
    """Copy the exact basis-closed union; mathematical/source acceptance unasserted."""
    started, cpu_started = time.monotonic(), time.process_time()
    need(callable(check_budget), "BUDGET")
    check_budget()
    validate_limits(custody_limits, limits)
    E, S, PE, B, PP = api.E, api.S, api.PE, api.B, api.PP
    need(S.E is E and PE.E is E and PE.S is S and B.E is E and B.PE is PE and
         B.S is S and PP.E is E and PP.PE is PE, "SHARED_CODECS")
    semantic = S.semantic_id()
    root = ordinary(custody_root)
    output = ordinary(output_directory, fresh=True)
    for path in (root, *map(Path, protected_paths)):
        need(path.is_absolute() and not output.is_relative_to(path) and
             not path.is_relative_to(output), "OUTPUT_OVERLAP")
    need(type(inventory_raw) is bytes and 0 < len(inventory_raw) <= MIB and
         hashlib.sha256(inventory_raw).hexdigest() == S.INVENTORY, "INVENTORY_PIN")
    inventory = B.C._writer_json(inventory_raw, MIB)
    need(type(inventory) is list and len(inventory) == 581, "BASIS_CENSUS")
    basis = {}
    for row in inventory:
        check_budget()
        E._array(row, 5)
        key = E.name_key(row[0])
        need(key not in basis, "BASIS_DUPLICATE")
        basis[key] = S.basis_symbol_id(semantic, S.foundation_id(), row[0])
    need(type(targets) is list and 1 <= len(targets) <= 64, "TARGET_COUNT")
    target_raw = E.canonical_json(targets)
    need(len(target_raw) <= 65536, "TARGET_BYTES")
    targets = E.strict_json(target_raw, E.Limits(max_bytes=65536))
    expected_units, scheduled, queue, outputs, units = {}, {}, deque(), {}, {}
    counts = dict(units=0, evidence_bytes=0, nodes=0, names=0, edges=0,
                  locator_reads=0, locator_bytes=0)

    def schedule(name, identity):
        check_budget()
        key = E.name_key(name)
        E._hex(identity)
        if key in basis:
            need(basis[key] == identity, "BASIS_IMPORT_MISMATCH")
            return
        need(key not in scheduled or scheduled[key] == identity, "IMPORT_ID_CONFLICT")
        if key not in scheduled:
            need(len(scheduled) < limits["names"], "SCHEDULE_BOUND")
            scheduled[key] = identity
            queue.append((key, identity))

    for target in targets:
        need(type(target) is dict and set(target) == {"name", "unit_id", "export_id"}, "TARGET_FIELDS")
        key = E.name_key(target["name"])
        E._hex(target["unit_id"]); E._hex(target["export_id"])
        need(key not in basis and key not in expected_units, "TARGET_DUPLICATE_OR_BASIS")
        need(S.export_id(semantic, target["unit_id"], target["name"]) == target["export_id"], "TARGET_IDENTITY")
        expected_units[key] = target["unit_id"]
        schedule(target["name"], target["export_id"])
    store = ReadCustody(root, semantic, custody_limits, api, limits, counts, check_budget)
    try:
        while queue:
            check_budget()
            key, identity = queue.popleft()
            if key in outputs:
                need(outputs[key][0] == identity and
                     (key not in expected_units or outputs[key][1] == expected_units[key]), "KNOWN_OUTPUT_MISMATCH")
                continue
            need(len(units) < limits["units"], "UNIT_BOUND")
            name = E.strict_json(key)
            unit = store.locator(name, identity)
            need(key not in expected_units or unit == expected_units[key], "TARGET_UNIT_MISMATCH")
            need(unit not in units, "LOCATOR_OUTPUT_OMISSION")
            parsed = store.evidence(unit)
            rows, imports = parsed.document["unit"][2], parsed.document["imports"]
            counts["units"] += 1; counts["nodes"] += parsed.census.total_nodes
            counts["names"] += len(rows); counts["edges"] += len(imports)
            need(all(counts[field] <= limits[field] for field in ("units", "nodes", "names", "edges")), "CLOSURE_CENSUS")
            for row in rows:
                check_budget()
                own_key = E.name_key(row[0])
                own_id = S.export_id(semantic, unit, row[0])
                need(own_key not in basis and own_key not in outputs, "OUTPUT_NAME_CONFLICT")
                need(own_key not in scheduled or scheduled[own_key] == own_id, "OUTPUT_ID_CONFLICT")
                need(own_key not in expected_units or expected_units[own_key] == unit, "TARGET_UNIT_MISMATCH")
                outputs[own_key] = (own_id, unit)
            need(key in outputs and outputs[key] == (identity, unit), "ACTUAL_TARGET_OMISSION")
            units[unit] = (parsed.raw, imports)
            for import_name, import_id in imports:
                schedule(import_name, import_id)
    finally:
        store.close()
    deps, users = {}, {unit: [] for unit in units}
    for unit, (_, imports) in units.items():
        check_budget()
        dependencies = set()
        for name, identity in imports:
            check_budget()
            key = E.name_key(name)
            if key in basis:
                need(basis[key] == identity, "BASIS_IMPORT_MISMATCH")
            else:
                need(key in outputs and outputs[key][0] == identity, "UNCLOSED_IMPORT")
                dependencies.add(outputs[key][1])
        deps[unit] = dependencies
        for dependency in dependencies:
            users[dependency].append(unit)
    ready = [unit for unit in units if not deps[unit]]
    heapq.heapify(ready)
    ordered = []
    while ready:
        check_budget()
        unit = heapq.heappop(ready)
        ordered.append(units[unit][0])
        for user in users[unit]:
            deps[user].remove(unit)
            if not deps[user]: heapq.heappush(ready, user)
    need(len(ordered) == len(units), "CYCLIC_CLOSURE")
    bundle_limits = B.Limits(max_units=limits["units"], max_bytes=limits["bytes"],
        max_nodes=limits["nodes"], max_names=limits["names"], max_edges=limits["edges"])
    batches = B.split_units(ordered, limits=bundle_limits, check_budget=check_budget)
    manifest = B.make_manifest(batches, limits=bundle_limits, check_budget=check_budget)
    check_budget()
    output.mkdir(); (output/"units").mkdir()
    written = 0

    def save(path, raw):
        nonlocal written
        check_budget()
        need(written+len(raw) <= limits["output_bytes"], "OUTPUT_BYTE_BOUND")
        ordinary(path, directory=False, fresh=True)
        with path.open("xb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        written += len(raw)
        with path.open("rb") as stream:
            need(stream.read(len(raw)+1) == raw, "OUTPUT_READBACK")
        check_budget()

    for entries, raws in zip(manifest.batches, batches):
        for entry, raw in zip(entries, raws):
            save(output/entry.relative_path, raw)
    save(output/"manifest.json", manifest.raw)
    result = {"schema": RESULT_SCHEMA, "status": "INERT_BUNDLE_EXPORTED",
        "custody": str(root), "semantic_id": semantic, "targets": targets, "counts": counts,
        "manifest": {"path": "manifest.json", "bytes": len(manifest.raw), "sha256": manifest.sha256},
        "mathematical_acceptance": False, "source_acceptance": "UNASSERTED",
        "wall_seconds": time.monotonic()-started, "cpu_seconds": time.process_time()-cpu_started}
    result_raw = json.dumps(result, sort_keys=True, ensure_ascii=True, allow_nan=False,
                            separators=(",", ":")).encode("ascii")
    need(len(result_raw) <= MIB, "RESULT_BOUND")
    save(output/"RESULT.json", result_raw)
    check_budget()
    return result

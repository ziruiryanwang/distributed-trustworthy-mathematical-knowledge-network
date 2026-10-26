"""Finite inert bundle preparation and serving; never mathematical authority.

The approved supervised entrypoint supplies pinned pure modules, one original
budget and protected local paths. No peer input selects code. Prepared stores
are exclusive and immutable-by-policy, not hostile-local-process sandboxes.
"""
from __future__ import annotations

import asyncio
from copy import deepcopy
import hashlib
import heapq
import ipaddress
import os
from pathlib import Path
import stat
import time
import uuid

MIB = 1024**2
CEILINGS = {"units": 1024, "bytes": 64*MIB, "nodes": 2097152,
            "names": 65536, "edges": 262144, "targets": 64,
            "preview_bytes": 16*MIB, "metadata_bytes": 16*MIB,
            "output_bytes": 512*MIB, "index_hash_steps": 32000000}
CUSTODY_LIMITS = {"objects": 1088, "exports": 65536,
                  "logical_bytes": 160*MIB, "db_pages": 32768}
INDEX_LIMITS = {"max_objects": 64, "max_postings": 8192,
               "max_features": 8192, "max_snapshots": 65,
               "max_logical_bytes": 64*MIB, "max_db_pages": 8192}
DESCRIPTOR_SCHEMA = "DMKN_INERT_MIRROR_DESCRIPTOR_V1"
READY_SCHEMA = "DMKN_INERT_MIRROR_READY_V1"
RESULT_SCHEMA = "DMKN_INERT_MIRROR_RESULT_V1"
PREPARED = "PREPARED_DATA_NOT_SUPERVISED_READY"
READY_CLOSURE = "EXIT_ZERO_REAPED_JOB_CLOSED_ZERO_ACTIVE_ZERO_TERMINATED_NO_CLEANUP_ERROR"
SYNTACTIC = "SYNTACTIC_IMPORTS_CLOSED_AGAINST_PINNED_BASIS_NOT_MATHEMATICAL_ACCEPTANCE"
INDEX_CALL_HASH_CAP = 2000000  # Exact selected Store._budget per-operation ceiling.
READY_FIELDS = {"schema", "status", "descriptor_sha256", "request_sha256",
                "source_manifest_sha256", "entry_sha256", "helper_sha256",
                "worker_report_sha256", "supervision_report_sha256", "closure",
                "mathematical_acceptance"}


def need(condition, code):
    if not condition:
        raise ValueError("INERT_MIRROR_"+code)


class MirrorError(RuntimeError):
    def __init__(self, report):
        self.report = report
        super().__init__(report["error"])


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


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


def _read(path, maximum, check):
    check()
    path = ordinary(path, directory=False)
    info = path.stat()
    need(info.st_nlink == 1 and 0 < info.st_size <= maximum, "FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == info.st_size and len(raw) <= maximum, "FILE_CHANGED_OR_BOUND")
    check()
    return raw


def _save(path, raw):
    ordinary(path, directory=False, fresh=True)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    with path.open("rb") as stream:
        need(stream.read(len(raw)+1) == raw, "FILE_READBACK")


def _fields(value, expected, code):
    need(type(value) is dict and set(value) == set(expected), code)


def validate_limits(limits, custody_limits=None, index_limits=None):
    _fields(limits, CEILINGS, "LIMIT_FIELDS")
    for key, maximum in CEILINGS.items():
        need(type(limits[key]) is int and 0 < limits[key] <= maximum, "LIMIT:"+key)
    custody = dict(CUSTODY_LIMITS if custody_limits is None else custody_limits)
    index = dict(INDEX_LIMITS if index_limits is None else index_limits)
    for selected, defaults, label in ((custody, CUSTODY_LIMITS, "CUSTODY"),
                                      (index, INDEX_LIMITS, "INDEX")):
        _fields(selected, defaults, label+"_LIMIT_FIELDS")
        for key, maximum in defaults.items():
            minimum = 256 if key in ("db_pages", "max_db_pages") else (
                1024 if key in ("logical_bytes", "max_logical_bytes") else 1)
            need(type(selected[key]) is int and minimum <= selected[key] <= maximum,
                 label+"_LIMIT:"+key)
    # Existing DELETE journals may occupy up to 2*database capacity + 1 MiB.
    # Reserve both databases, both journals and bounded local descriptor/seal.
    physical_reservation = 3*4096*(custody["db_pages"]+index["max_db_pages"])+4*MIB
    need(physical_reservation <= limits["output_bytes"], "PHYSICAL_OUTPUT_RESERVATION")
    return custody, index


def _api(api):
    need(type(api) is dict and all(key in api for key in
         ("B", "E", "S", "PE", "PP", "O", "D", "OA", "H")), "API")
    E, S, PE, B, PP = (api[key] for key in ("E", "S", "PE", "B", "PP"))
    need(S.E is E and PE.E is E and PE.S is S and B.E is E and B.PE is PE and
         B.S is S and PP.E is E and PP.PE is PE, "SHARED_CODECS")
    return E, S, PE, B, PP


def _basis(E, S, B, inventory_raw, check):
    need(type(inventory_raw) is bytes and 0 < len(inventory_raw) <= MIB and
         _sha(inventory_raw) == S.INVENTORY, "INVENTORY_PIN")
    inventory = B.C._writer_json(inventory_raw, MIB)
    need(type(inventory) is list and len(inventory) == 581, "BASIS_CENSUS")
    basis, semantic = {}, S.semantic_id()
    for row in inventory:
        check()
        E._array(row, 5)
        key = E.name_key(row[0])
        need(key not in basis, "BASIS_DUPLICATE")
        basis[key] = S.basis_symbol_id(semantic, S.foundation_id(), row[0])
    return basis


def _targets(E, S, semantic, targets, maximum):
    need(type(targets) is list and 1 <= len(targets) <= maximum, "TARGET_COUNT")
    raw = E.canonical_json(targets)
    need(len(raw) <= 65536, "TARGET_BYTES")
    selected, seen = E.strict_json(raw), set()
    for target in selected:
        _fields(target, ("name", "unit_id", "export_id"), "TARGET_FIELDS")
        key = E.name_key(target["name"])
        E._hex(target["unit_id"]); E._hex(target["export_id"])
        need(key not in seen, "TARGET_DUPLICATE")
        seen.add(key)
        need(S.export_id(semantic, target["unit_id"], target["name"]) == target["export_id"],
             "TARGET_IDENTITY")
    return selected


def _closed_bundle(root, manifest_raw, manifest_sha256, targets, inventory_raw,
                   api, limits, check):
    E, S, PE, B, _ = _api(api)
    basis = _basis(E, S, B, inventory_raw, check)
    blimits = B.Limits(max_units=limits["units"], max_bytes=limits["bytes"],
        max_nodes=limits["nodes"], max_names=limits["names"], max_edges=limits["edges"],
        max_binding_bytes=limits["metadata_bytes"])
    manifest = B.read_manifest(manifest_raw, manifest_sha256, limits=blimits,
                               check_budget=check)
    selected = _targets(E, S, manifest.semantic_id, targets, limits["targets"])
    totals = dict(units=0, bytes=0, nodes=0, names=0, edges=0,
                  metadata_bytes=0, binding_bytes=2, preview_bytes=0, index_hash_steps=0,
                  index_hash_authorized_upper_bound=0)
    units, imports, outputs = {}, {}, {}
    for entries in manifest.batches:
        check()
        raws = tuple(_read(root/entry.relative_path, entry.raw_bytes, check) for entry in entries)
        census = B.validate_batch(entries, raws, limits=blimits, check_budget=check)
        previous_names = totals["names"]
        for key in ("units", "bytes", "nodes", "names", "edges"):
            totals[key] += getattr(census, key)
            need(totals[key] <= limits[key], "AGGREGATE_"+key.upper())
        totals["binding_bytes"] += census.binding_bytes-2+int(bool(previous_names and census.names))
        need(totals["binding_bytes"] <= limits["metadata_bytes"], "AGGREGATE_BINDING_BYTES")
        for raw in raws:
            check()
            item = PE.read_evidence(raw)
            need(item.unit_id not in units, "DUPLICATE_UNIT")
            units[item.unit_id] = raw
            imports[item.unit_id] = item.document["imports"]
            for name, identity in item.document["imports"]:
                totals["metadata_bytes"] += len(E.canonical_json([name, identity]))
                need(totals["metadata_bytes"] <= limits["metadata_bytes"], "METADATA_BOUND")
            for row in item.document["unit"][2]:
                check()
                key = E.name_key(row[0])
                identity = S.export_id(manifest.semantic_id, item.unit_id, row[0])
                need(key not in basis, "BASIS_OUTPUT_COLLISION")
                need(key not in outputs, "OUTPUT_NAME_CONFLICT")
                totals["metadata_bytes"] += len(E.canonical_json([row[0], identity, item.unit_id]))
                need(totals["metadata_bytes"] <= limits["metadata_bytes"], "METADATA_BOUND")
                outputs[key] = (identity, item.unit_id)
    need(totals["units"] == manifest.unit_count and totals["bytes"] == manifest.evidence_bytes,
         "MANIFEST_CENSUS")
    deps, users = {}, {unit: [] for unit in units}
    for unit, rows in imports.items():
        dependencies = set()
        for name, identity in rows:
            check()
            key = E.name_key(name)
            if key in basis:
                need(basis[key] == identity, "BASIS_IMPORT_MISMATCH")
            else:
                need(key in outputs, "UNCLOSED_IMPORT")
                need(outputs[key][0] == identity, "IMPORT_ID_MISMATCH")
                dependencies.add(outputs[key][1])
        deps[unit] = dependencies
        for dependency in dependencies:
            users[dependency].append(unit)
    available = [unit for unit in units if not deps[unit]]
    heapq.heapify(available)
    ordered = []
    while available:
        check()
        unit = heapq.heappop(available)
        ordered.append(unit)
        for user in users[unit]:
            deps[user].remove(unit)
            if not deps[user]:
                heapq.heappush(available, user)
    need(len(ordered) == len(units), "CYCLIC_IMPORTS")
    for target in selected:
        check()
        need(outputs.get(E.name_key(target["name"])) == (target["export_id"], target["unit_id"]),
             "TARGET_NOT_ACTUAL_OUTPUT")
    return manifest, selected, units, ordered, totals


class _Lock:
    """Exclusive local operation marker; crash/uncertain cleanup leaves it held."""
    def __init__(self, root):
        self.path = ordinary(root/"ACTIVE.lock", directory=False, fresh=True)
        self.raw = uuid.uuid4().hex.encode("ascii")
        _save(self.path, self.raw)
        self.held = True

    def release(self):
        need(self.held and _read(self.path, 32, lambda: None) == self.raw, "LOCK_CHANGED")
        self.path.unlink()
        self.held = False


def _close(stores, report):
    closed = True
    for store in stores:
        if store is not None:
            try:
                store.close()
                need(store.db is None, "STORE_CLOSE_UNCERTAIN")
            except BaseException as error:
                closed = False
                report["cleanup_errors"].append(type(error).__name__+":"+str(error))
    report["stores_closed"] = closed
    return closed


def _finish(report, error, started, cpu_started):
    report.update(wall_seconds=time.monotonic()-started,
                  controller_cpu_seconds=time.process_time()-cpu_started)
    if error is not None or report["cleanup_errors"]:
        report.update(status="REFUSED_OR_INCOMPLETE", error=(type(error).__name__+":"+str(error)
            if error is not None else "INERT_MIRROR_CLEANUP_UNCERTAIN"))
        raise MirrorError(report) from error
    return report


def prepare(*, bundle_directory, manifest_raw, manifest_sha256, targets, inventory_raw,
            output_directory, api, limits, check_budget, protected_paths=(),
            share_all_bundle=False, custody_limits=None, index_limits=None):
    """Prepare exact syntactically closed data; no public READY seal is written."""
    started, cpu_started = time.monotonic(), time.process_time()
    report = dict(schema=RESULT_SCHEMA, action="prepare", mathematical_acceptance=False,
                  cleanup_errors=[], stores_closed=True,
                  index_hash_accounting="OBSERVED_COUNTERS_PARTIAL_ON_EXCEPTION_AUTHORIZED_UPPER_BOUND_RETAINED")
    custody = index = lock = None
    error = None
    try:
        need(callable(check_budget), "BUDGET")
        check_budget()
        need(share_all_bundle is True, "EXPLICIT_WHOLE_BUNDLE_DISCLOSURE")
        E, S, _, _, PP = _api(api)
        climits, ilimits = validate_limits(limits, custody_limits, index_limits)
        root = ordinary(bundle_directory)
        output = ordinary(output_directory, fresh=True)
        for path in (root, *map(Path, protected_paths)):
            need(path.is_absolute() and not output.is_relative_to(path) and
                 not path.is_relative_to(output), "OUTPUT_OVERLAP")
        need(_read(root/"manifest.json", 2*MIB, check_budget) == manifest_raw,
             "MANIFEST_FILE_BINDING")
        manifest, selected, units, ordered, counts = _closed_bundle(root, manifest_raw,
            manifest_sha256, targets, inventory_raw, api, limits, check_budget)
        report["counts"] = counts
        check_budget()
        output.mkdir()
        lock = _Lock(output)
        custody = api["O"].OrdinaryStore(output/"custody", S.semantic_id(), climits, create=True)
        adapter = api["OA"].OrdinaryExportAdapter(S.semantic_id())
        need(INDEX_CALL_HASH_CAP <= limits["index_hash_steps"], "INDEX_AGGREGATE_RESERVATION")
        counts["index_hash_authorized_upper_bound"] = INDEX_CALL_HASH_CAP
        index = api["D"].Store(output/"index", adapter, ilimits, create=True)
        need(index.db.execute("PRAGMA page_size").fetchone() == (4096,), "INDEX_PAGE_SIZE")
        counts["index_hash_steps"] = index.work["index_hash_steps"]
        for unit in ordered:
            check_budget()
            custody.put_evidence(units[unit], before_commit=check_budget)
        for target in selected:
            check_budget()
            raw = custody.get_evidence(S.semantic_id(), target["unit_id"], 8*MIB,
                                       check_budget=check_budget)
            preview = PP.preview_from_evidence(raw, target["name"])
            PP.resolve(preview, raw)
            need(PP.read_preview(preview).export_id == target["export_id"], "PREVIEW_TARGET")
            counts["preview_bytes"] += len(preview)
            need(counts["preview_bytes"] <= limits["preview_bytes"], "PREVIEW_AGGREGATE_BOUND")
            custody.put_preview(preview, before_commit=check_budget)
            # Reserve one complete existing bounded index operation before it
            # starts; do not rely on a post-operation refusal to authorize work.
            need(counts["index_hash_steps"]+INDEX_CALL_HASH_CAP <= limits["index_hash_steps"],
                 "INDEX_AGGREGATE_RESERVATION")
            counts["index_hash_authorized_upper_bound"] = counts["index_hash_steps"]+INDEX_CALL_HASH_CAP
            try:
                index.admit(preview, expected_id=target["export_id"])
            finally:
                # The selected admit resets its counter before its first work;
                # retain observable work even when that operation refuses.
                counts["index_hash_steps"] += index.work["index_hash_steps"]
            need(counts["index_hash_steps"] <= limits["index_hash_steps"], "INDEX_AGGREGATE_WORK")
            check_budget()
        custody_status, index_status = custody.status(), index.status()
        snapshot_id = index_status["latest"]
        snapshot = index.snapshot(snapshot_id)
        descriptor = dict(schema=DESCRIPTOR_SCHEMA, status=PREPARED,
            prepared_directory=str(output), semantic_id=S.semantic_id(),
            foundation_inventory_sha256=_sha(inventory_raw), manifest_sha256=manifest.sha256,
            targets=selected, namespace=adapter.namespace, snapshot_id=snapshot_id,
            snapshot=snapshot, limits=dict(limits), custody_limits=climits, index_limits=ilimits,
            custody_status=custody_status, index_status=index_status, counts=counts,
            closure=SYNTACTIC, mathematical_acceptance=False)
        raw_descriptor = E.canonical_json(descriptor)
        need(len(raw_descriptor) <= MIB, "DESCRIPTOR_BOUND")
        report["counts"] = counts
    except BaseException as caught:
        error = caught
    finally:
        closed = _close((index, custody), report)
        if lock is not None and closed:
            try:
                lock.release()
            except BaseException as caught:
                report["cleanup_errors"].append(type(caught).__name__+":"+str(caught))
    if error is None and not report["cleanup_errors"]:
        try:
            check_budget()
            _save(output/"DESCRIPTOR.json", raw_descriptor)
            report.update(status=PREPARED, descriptor_path=str(output/"DESCRIPTOR.json"),
                          descriptor_sha256=_sha(raw_descriptor))
            check_budget()
        except BaseException as caught:
            error = caught
    return _finish(report, error, started, cpu_started)


def _database(root, filename, pages, check):
    path = ordinary(root/filename, directory=False)
    info = path.stat()
    need(info.st_nlink == 1 and 0 < info.st_size <= pages*4096, "DATABASE_BOUND")
    for suffix in ("-journal", "-wal", "-shm"):
        need(not os.path.lexists(str(path)+suffix), "PREPARED_STATE_NEEDS_RECOVERY")
    check()


def _ready(E, F, root, descriptor_sha256, ready_raw, ready_sha256, check):
    E._hex(ready_sha256)
    need(type(ready_raw) is bytes and 0 < len(ready_raw) <= MIB and
         _sha(ready_raw) == ready_sha256 and
         _read(root/"READY.json", MIB, check) == ready_raw, "READY_EXACT_BINDING")
    seal = F.strict(ready_raw, MIB)
    _fields(seal, READY_FIELDS, "READY_FIELDS")
    need(seal["schema"] == READY_SCHEMA and seal["status"] == "INERT_MIRROR_READY" and
         seal["descriptor_sha256"] == descriptor_sha256 and
         seal["closure"] == READY_CLOSURE and seal["mathematical_acceptance"] is False,
         "SUPERVISED_PREPARATION_REQUIRED")
    for key in READY_FIELDS:
        if key.endswith("sha256"):
            E._hex(seal[key])
    return seal


async def serve(*, prepared_directory, descriptor_raw, descriptor_sha256,
                ready_raw, ready_sha256, config, api, check_budget, deadline, ready=None):
    """Serve a locally protected, parent-sealed preparation for one finite lease.

    The public entry additionally pins the seal's approved code selection. The
    seal is local workflow authority, never a transferable mathematical warrant.
    """
    started, cpu_started = time.monotonic(), time.process_time()
    report = dict(schema=RESULT_SCHEMA, action="serve", mathematical_acceptance=False,
                  cleanup_errors=[], stores_closed=True, quiescent=False, ready=None)
    custody = index = provider = lock = lease_timer = None
    error = None
    cleanup_until = deadline
    try:
        need(callable(check_budget) and (ready is None or callable(ready)), "CALLBACK")
        need(type(deadline) in (int, float) and time.monotonic() < deadline, "DEADLINE")
        check_budget()
        E, S, _, _, _ = _api(api)
        root = ordinary(prepared_directory)
        E._hex(descriptor_sha256)
        need(type(descriptor_raw) is bytes and 0 < len(descriptor_raw) <= MIB and
             _sha(descriptor_raw) == descriptor_sha256 and
             _read(root/"DESCRIPTOR.json", MIB, check_budget) == descriptor_raw,
             "DESCRIPTOR_EXACT_BINDING")
        descriptor = api["O"].F.strict(descriptor_raw, MIB)
        _fields(descriptor, ("schema", "status", "prepared_directory", "semantic_id",
            "foundation_inventory_sha256", "manifest_sha256", "targets", "namespace",
            "snapshot_id", "snapshot", "limits", "custody_limits", "index_limits",
            "custody_status", "index_status", "counts", "closure", "mathematical_acceptance"),
            "DESCRIPTOR_FIELDS")
        need(descriptor["schema"] == DESCRIPTOR_SCHEMA and descriptor["status"] == PREPARED and
             descriptor["prepared_directory"] == str(root) and
             descriptor["semantic_id"] == S.semantic_id() and
             descriptor["foundation_inventory_sha256"] == S.INVENTORY and
             descriptor["closure"] == SYNTACTIC and descriptor["mathematical_acceptance"] is False,
             "DESCRIPTOR_PROFILE")
        _ready(E, api["O"].F, root, descriptor_sha256, ready_raw, ready_sha256, check_budget)
        climits, ilimits = validate_limits(descriptor["limits"], descriptor["custody_limits"],
                                           descriptor["index_limits"])
        _targets(E, S, S.semantic_id(), descriptor["targets"], descriptor["limits"]["targets"])
        _fields(config, ("host", "port", "tls", "lease_seconds", "cleanup_seconds", "limits",
                         "share_all_custody", "exclusive"), "SERVE_CONFIG_FIELDS")
        need(config["share_all_custody"] is True and config["exclusive"] is True,
             "EXPLICIT_CUSTODY_EXCLUSIVE_DISCLOSURE")
        need(type(config["host"]) is str and len(config["host"]) <= 64, "HOST")
        address = ipaddress.ip_address(config["host"])
        need(not address.is_unspecified and not address.is_multicast, "HOST_POLICY")
        for key, low, high in (("port", 0, 65535), ("lease_seconds", 1, 3600),
                               ("cleanup_seconds", 10, 60)):
            need(type(config[key]) is int and low <= config[key] <= high, "SERVE_LIMIT:"+key)
        _fields(config["limits"], ("max_connections", "max_requests", "max_reply_bytes",
                                  "operation_ms"), "PROVIDER_LIMIT_FIELDS")
        tls = None
        if config["tls"] is not None:
            value = config["tls"]
            _fields(value, ("cert_file", "cert_sha256", "key_file", "key_sha256"), "TLS_FIELDS")
            for label in ("cert", "key"):
                E._hex(value[label+"_sha256"])
                need(_sha(_read(Path(value[label+"_file"]), MIB, check_budget)) == value[label+"_sha256"],
                     "TLS_PIN")
            tls = api["H"].server_tls(value["cert_file"], value["key_file"])
            for label in ("cert", "key"):
                need(_sha(_read(Path(value[label+"_file"]), MIB, check_budget)) == value[label+"_sha256"],
                     "TLS_CHANGED")
        need(address.is_loopback or tls is not None, "REMOTE_TLS_REQUIRED")
        lock = _Lock(root)
        _database(root/"custody", "ordinary.sqlite", climits["db_pages"], check_budget)
        _database(root/"index", "discovery.sqlite", ilimits["max_db_pages"], check_budget)
        custody = api["O"].OrdinaryStore(root/"custody", S.semantic_id(), climits)
        adapter = api["OA"].OrdinaryExportAdapter(S.semantic_id())
        need(adapter.namespace == descriptor["namespace"], "NAMESPACE_BINDING")
        index = api["D"].Store(root/"index", adapter, ilimits)
        need(index.db.execute("PRAGMA page_size").fetchone() == (4096,), "INDEX_PAGE_SIZE")
        need(custody.status() == descriptor["custody_status"] and
             index.status() == descriptor["index_status"] and
             index.status()["latest"] == descriptor["snapshot_id"] and
             index.snapshot(descriptor["snapshot_id"]) == descriptor["snapshot"],
             "PREPARED_STATE_BINDING")
        for store in (index, custody):
            store.db.execute("PRAGMA query_only=ON")
        check_budget()
        lease_until = time.monotonic()+config["lease_seconds"]
        need(lease_until+config["cleanup_seconds"] < deadline, "LEASE_ORIGINAL_ALLOWANCE")
        cleanup_until = min(deadline, lease_until+config["cleanup_seconds"])
        provider = api["H"].Provider(index=index, ordinary=custody, **config["limits"])
        lease_timer = asyncio.timeout_at(lease_until)
        async with lease_timer:
            endpoint = await provider.start(config["host"], config["port"], tls_context=tls)
            check_budget()
            report["ready"] = dict(status="READY", host=endpoint.host, port=endpoint.port,
                tls=endpoint.tls, lease_seconds=config["lease_seconds"], shared_custody=str(custody.root),
                index=str(index.root), snapshot_id=descriptor["snapshot_id"],
                namespace=descriptor["namespace"], mathematical_acceptance=False)
            if ready is not None:
                ready(deepcopy(report["ready"]))
            while time.monotonic() < lease_until:
                check_budget()
                await asyncio.sleep(min(0.1, max(0, lease_until-time.monotonic())))
        report["status"] = "LEASE_FINISHED"
    except TimeoutError as caught:
        if lease_timer is not None and lease_timer.expired() and report["ready"] is not None:
            report["status"] = "LEASE_FINISHED"
        else:
            error = caught
    except BaseException as caught:
        error = caught
    finally:
        provider_closed = provider is None
        if provider is not None:
            try:
                async with asyncio.timeout_at(cleanup_until):
                    await provider.stop()
                status = provider.status()
                report["provider"] = status
                provider_closed = (provider.server is None and not provider.tasks and
                    status["active"] == 0 and status["reserved_reply_bytes"] == 0 and
                    status["cleanup_pending"] == 0 and status["cleanup_failures"] == 0)
                need(provider_closed, "PROVIDER_CLEANUP_UNCERTAIN")
            except BaseException as caught:
                report["cleanup_errors"].append(type(caught).__name__+":"+str(caught))
        report["quiescent"] = provider_closed
        stores_closed = _close((index, custody), report)
        if lock is not None and provider_closed and stores_closed:
            try:
                lock.release()
            except BaseException as caught:
                report["cleanup_errors"].append(type(caught).__name__+":"+str(caught))
    if error is None and not report["cleanup_errors"]:
        try:
            check_budget()
        except BaseException as caught:
            error = caught
    return _finish(report, error, started, cpu_started)

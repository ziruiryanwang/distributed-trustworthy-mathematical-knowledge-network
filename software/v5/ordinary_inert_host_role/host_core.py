"""Static and incremental custody/index hosting with authentic inert-role support.

No owner catalog, native worker, grounding, new storage schema or network protocol.
The protected package/OS and serialized supported-command assumptions remain.
"""
from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
import asyncio
import hashlib
import ipaddress
from pathlib import Path
import sys
import time

import inert_host_support as IS

MIB = 1024**2
MARKER = "DMKN-DEDICATED-HOST.json"
MARKER_SCHEMA = "DMKN_DEDICATED_HOST_V1"
PREPARE_SCHEMA = "DMKN_DEDICATED_HOST_PREPARE_V1"
SERVE_SCHEMA = "DMKN_DEDICATED_HOST_SERVE_V1"
SEAL_SCHEMA = "DMKN_DEDICATED_HOST_SEAL_V1"
INIT_SCHEMA = "DMKN_INCREMENTAL_HOST_INIT_V1"
APPEND_SCHEMA = "DMKN_INCREMENTAL_HOST_APPEND_V1"
DESCRIPTOR_SCHEMA = "DMKN_INCREMENTAL_HOST_DESCRIPTOR_V1"
ASSURANCE = "INERT_HOST_NOT_MATHEMATICAL_ACCEPTANCE"
SEAL_FIELDS = ("schema", "profile_sha256", "semantic_id", "namespace", "manifest_sha256",
               "targets", "custody_limits", "index_limits", "custody_counts",
               "index_snapshot_id", "index_objects", "assurance", "mathematical_acceptance")
DESCRIPTOR_FIELDS = ("schema", "profile_sha256", "semantic_id", "namespace",
                     "custody_limits", "index_limits", "partial_publication",
                     "assurance", "mathematical_acceptance")
INCREMENTAL_IDENTITY = "STABLE_INCREMENTAL_CONFIGURATION_NOT_CONTENT_IDENTITY"


class HostFailure(RuntimeError):
    def __init__(self, report):
        self.report = report
        super().__init__(report["error"])


def need(condition, code):
    if not condition:
        raise ValueError("HOST_"+code)


def _error(error):
    return (type(error).__name__+": "+str(error))[:2048]


def _failure(report, error):
    report.update(status="FAILED", error=_error(error), mathematical_acceptance=False)
    return HostFailure(report)


def _separate(left, right):
    need(not left.is_relative_to(right) and not right.is_relative_to(left), "PATH_OVERLAP")


def _modules(support, allowance, profile_sha256, finalize):
    need(IS is sys.modules.get("inert_host_support") and
         type(support) is IS.InertHostSupport and callable(finalize) and
         callable(allowance.check), "SELECTED_INERT_SUPPORT")
    support.hexid(profile_sha256)
    need(profile_sha256 == support.profile_sha256, "SUPPORT_PROFILE_BINDING")
    api = support.api
    selected = {"E": "ordinary_evidence", "S": "ordinary_semantics",
        "PE": "portable_evidence", "B": "baseline_bundle", "PP": "portable_preview",
        "O": "transport.ordinary_acquisition", "DS": "discovery.discovery_store",
        "OA": "discovery.ordinary_export_adapter", "H": "transport.http_provider",
        "F": "discovery.formal_features"}
    need(all(api[key] is support.modules[name] is sys.modules.get(name)
             for key, name in selected.items()), "SELECTED_MODULE_IDENTITIES")
    E, S, PE, B = (api[key] for key in ("E", "S", "PE", "B"))
    need(S.E is E and B.E is E and B.S is S and B.PE is PE and PE.E is E and PE.S is S and
         api["PP"].E is E and api["PP"].PE is PE and
         support.semantic_id == S.semantic_id() and
         support.namespace == api["OA"].OrdinaryExportAdapter(support.semantic_id).namespace,
         "SELECTED_CODECS_AND_SEMANTICS")
    allowance.check()
    return api["O"], api, B


def _config(api, value):
    need(type(value) is dict, "CONFIGURATION")
    raw = api["F"].compact(value)
    need(0 < len(raw) <= 2*MIB, "CONFIGURATION_BYTES")
    return api["F"].strict(raw, 2*MIB)


def _targets(support, api, values):
    need(type(values) is list and 1 <= len(values) <= 64, "TARGET_COUNT")
    seen, result = set(), []
    for row in values:
        support.fields(row, ("name", "export_id", "unit_id"), "HOST_TARGET_FIELDS")
        api["E"].name_key(row["name"])
        eid, uid = support.hexid(row["export_id"]), support.hexid(row["unit_id"])
        need(eid not in seen and api["S"].export_id(api["S"].semantic_id(), uid, row["name"]) == eid,
             "TARGET_IDENTITY_OR_DUPLICATE")
        seen.add(eid); result.append(deepcopy(row))
    return result


def _checked_limits(support, value, bounds, code):
    support.fields(value, bounds, code)
    for key, interval in bounds.items():
        support.uint(value[key], *interval, code+":"+key)
    return dict(value)


def _limits(support, api, O, custody, index):
    _checked_limits(support, custody, O.STORE_LIMITS, "HOST_CUSTODY_LIMITS")
    _checked_limits(support, index, api["DS"].LIMITS, "HOST_INDEX_LIMITS")


def _root(support, value, *, fresh):
    root = support.ordinary(Path(value), directory=True, fresh=fresh)
    need(root != Path(root.anchor), "ROOT_DIRECTORY")
    for protected in (support.root, support.python_runtime_root):
        _separate(root, protected)
    if fresh:
        for ancestor in root.parents:
            for filename in (MARKER, "ADOPTION.json", "ordinary.sqlite", "discovery.sqlite"):
                try:
                    (ancestor/filename).lstat()
                except FileNotFoundError:
                    continue
                need(False, "NESTED_EXISTING_STATE")
    return root


def _marker(support, api, root):
    expected = api["E"].canonical_json({"schema": MARKER_SCHEMA})
    need(support.read(root/MARKER, len(expected)) == expected, "PERMANENT_MARKER")


@contextmanager
def _locked(support, api, root, report, *, create):
    # Marker creation precedes any store; both host preparation and serving use
    # this one permanent lock inode. Never recreate it to bypass contention.
    stream = None
    try:
        if create:
            root.mkdir(); report["host_created"] = True
            support.write_fresh(root/MARKER,
                                api["E"].canonical_json({"schema": MARKER_SCHEMA}))
            support.write_fresh(root/"host.lock", b"\0")
        lock_path = support.ordinary(root/"host.lock")
        need(support.read(lock_path, 1) == b"\0", "LOCK_FILE")
        import msvcrt
        stream = lock_path.open("r+b")
        msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        report["host_lock_closure"] = "OPEN"
        _marker(support, api, root)
        yield
    finally:
        if stream is not None:
            try:
                stream.close()
                report["host_lock_closure"] = "CLOSED"
            except BaseException as error:
                report["host_lock_closure"] = "UNCERTAIN"
                report["cleanup_errors"].append(_error(error))
                raise


def _close(index, custody, report):
    first = None
    for label, handle in (("index", index), ("custody", custody)):
        if handle is not None:
            try:
                handle.close()
                need(handle.db is None, "STORE_CLOSE_NOT_COMPLETE")
                report[label+"_closure"] = "CLOSED"
            except BaseException as error:
                report[label+"_closure"] = "UNCERTAIN"
                report["cleanup_errors"].append(_error(error))
                first = first or error
    return first


def _index_config(root, limits, *, create):
    return {"path": str(root/"index"), "limits": deepcopy(limits), "create": create}


def _read_batch(support, B, directory, entries, limits, check):
    """Preserve baseline_intake's inert bounded-read/validate boundary only."""
    raw_units = []
    for entry in entries:
        check()
        path = support.ordinary(directory/entry.relative_path)
        raw_units.append(support.read(path, entry.raw_bytes))
    raws = tuple(raw_units)
    census = B.validate_batch(entries, raws, limits=limits, check_budget=check)
    return raws, census


def _index(support, custody, config, check):
    """Construct the actual selected index without an owner/install facade."""
    api = support.api
    fields = ("path", "limits", "create")
    support.fields(config, (*fields, "access_pairs") if type(config) is dict and
                   "access_pairs" in config else fields, "HOST_INDEX_FIELDS")
    need(type(config["create"]) is bool and type(config["path"]) is str,
         "INDEX_CONFIGURATION")
    _checked_limits(support, config["limits"], api["DS"].LIMITS, "HOST_INDEX_LIMITS")
    need(type(custody) is api["O"].OrdinaryStore and
         custody.semantic_id == support.semantic_id, "CUSTODY_BINDING")
    custody._active()
    root = support.ordinary(Path(config["path"]), directory=True, fresh=config["create"])
    for protected in (support.root, support.python_runtime_root, custody.root):
        _separate(root, protected)
    check()
    return api["DS"].Store(root, api["OA"].OrdinaryExportAdapter(support.semantic_id),
        config["limits"], create=config["create"], access_pairs=config.get("access_pairs"))


def _pin(support, path, digest, check):
    check(); support.hexid(digest)
    need(type(path) is str, "PIN_PATH")
    selected = support.ordinary(Path(path))
    raw = support.read(selected, MIB)
    need(hashlib.sha256(raw).hexdigest() == digest, "FILE_PIN")
    check()
    return selected, digest


async def _service(support, custody, config, allowance, *, ready=None):
    """Existing finite provider composition, restricted to this inert host role.

    The caller holds the permanent host lock and closes custody after this
    coroutine and asyncio.run's drain have completed. Only index/provider handles
    are owned here. A failed cleanup never obtains a fresh time allowance.
    """
    allowance.check()
    api = support.api
    config = _config(api, config)
    report = {"operation": "serve", "status": "STARTED", "mathematical_acceptance": False,
        "controller_limits": "COOPERATIVE_REQUIRES_EXTERNAL_JOB", "cleanup_errors": [],
        "provider": None, "ready": None, "quiescent": False}
    index = provider = lease_timer = None
    error = None
    cleanup_until = allowance.deadline
    try:
        support.fields(config, ("index", "host", "port", "tls", "lease_seconds",
            "cleanup_seconds", "limits", "share_all_custody", "exclusive"), "HOST_SERVICE_FIELDS")
        need(type(custody) is api["O"].OrdinaryStore and
             custody.semantic_id == support.semantic_id, "CUSTODY_BINDING")
        custody._active()
        need(config["share_all_custody"] is True and config["exclusive"] is True,
             "EXPLICIT_FULL_CUSTODY_EXCLUSIVE_SCOPE")
        need(ready is None or callable(ready), "READY_CALLBACK")
        support.uint(config["lease_seconds"], 1, 3600, "HOST_SERVICE_LEASE")
        support.uint(config["cleanup_seconds"], 10, 60, "HOST_SERVICE_CLEANUP_RESERVE")
        support.uint(config["port"], 0, 65535, "HOST_SERVICE_PORT")
        need(type(config["host"]) is str and len(config["host"]) <= 64, "SERVICE_HOST")
        address = ipaddress.ip_address(config["host"])
        need(not address.is_unspecified and not address.is_multicast, "SERVICE_ADDRESS")
        limits = _checked_limits(support, config["limits"], {
            "max_connections": (1, 8), "max_requests": (1, 1000000),
            "max_reply_bytes": (1024, 2**40), "operation_ms": (1, 60000)}, "HOST_PROVIDER_LIMITS")
        support.fields(config["index"], ("path", "limits", "create"), "HOST_SERVICE_INDEX_FIELDS")
        need(config["index"]["create"] is False, "SERVICE_EXISTING_INDEX")
        tls, pins = None, []
        if config["tls"] is not None:
            selected = config["tls"]
            support.fields(selected, ("cert_file", "cert_sha256", "key_file", "key_sha256"),
                           "HOST_SERVER_TLS_FIELDS")
            pins = [_pin(support, selected["cert_file"], selected["cert_sha256"], allowance.check),
                    _pin(support, selected["key_file"], selected["key_sha256"], allowance.check)]
            tls = api["H"].server_tls(str(pins[0][0]), str(pins[1][0]))
            for path, digest in pins:
                _pin(support, str(path), digest, allowance.check)
        need(address.is_loopback or tls is not None, "REMOTE_TLS_REQUIRED")
        index = _index(support, custody, config["index"], allowance.check)
        allowance.check()
        lease_until = time.monotonic()+config["lease_seconds"]
        need(lease_until+config["cleanup_seconds"] < allowance.deadline, "LEASE_ORIGINAL_ALLOWANCE")
        cleanup_until = min(allowance.deadline, lease_until+config["cleanup_seconds"])
        provider = api["H"].Provider(index=index, ordinary=custody, **limits)
        lease_timer = asyncio.timeout_at(lease_until)
        async with lease_timer:
            endpoint = await provider.start(config["host"], config["port"], tls_context=tls)
            allowance.check()
            report["ready"] = {"status": "READY", "host": endpoint.host, "port": endpoint.port,
                "tls": endpoint.tls, "lease_seconds": config["lease_seconds"],
                "shared_custody": str(custody.root), "index": str(index.root),
                "mathematical_acceptance": False, "controller_limits": report["controller_limits"]}
            if ready is not None:
                ready(deepcopy(report["ready"]))
            while time.monotonic() < lease_until:
                allowance.check()
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
        if provider is not None:
            try:
                async with asyncio.timeout_at(cleanup_until):
                    await provider.stop()
                report["quiescent"] = (provider.server is None and not provider.tasks and
                                        provider.reserved_reply_bytes == 0)
                need(report["quiescent"], "SERVICE_CLEANUP_UNCERTAIN")
            except BaseException as caught:
                report["cleanup_errors"].append(_error(caught)); error = error or caught
                # Preserve the current provider composition's fallback drain,
                # within the same original cleanup deadline and held host lock.
                if provider.server is not None:
                    try: provider.server.close()
                    except BaseException as other:
                        report["cleanup_errors"].append(_error(other))
                tasks = list(provider.tasks)
                for task in tasks: task.cancel()
                if tasks:
                    try:
                        async with asyncio.timeout_at(cleanup_until):
                            await asyncio.gather(*tasks, return_exceptions=True)
                    except BaseException as other:
                        report["cleanup_errors"].append(_error(other))
            report["provider"] = provider.status()
        if index is not None:
            try:
                index.close()
                need(index.db is None, "SERVICE_INDEX_CLOSE_UNCERTAIN")
            except BaseException as caught:
                report["cleanup_errors"].append(_error(caught)); error = error or caught
    try: allowance.check()
    except BaseException as caught: error = error or caught
    if error is not None:
        raise _failure(report, error) from error
    return report


def _report(operation, root, profile):
    return {"operation": operation, "status": "STARTED", "host_root": str(root),
            "profile_sha256": profile, "assurance": ASSURANCE, "mathematical_acceptance": False,
            "host_created": False, "host_lock_closure": "NOT_OPENED",
            "index_closure": "NOT_OPENED", "custody_closure": "NOT_OPENED",
            "cleanup_errors": [], "seal_attempted": False, "sealed": False}


def prepare(support, host_root, config, allowance, *, profile_sha256, finalize):
    """Create and seal one fresh inert generation; failed roots are never reused."""
    O, api, B = _modules(support, allowance, profile_sha256, finalize)
    config = _config(api, config)
    fields = ("schema", "bundle_directory", "manifest", "targets", "custody_limits",
              "index_limits", "share_all_bundle")
    support.fields(config, (*fields, "bundle_limits") if "bundle_limits" in config else fields,
               "HOST_PREPARE_FIELDS")
    need(config["schema"] == PREPARE_SCHEMA and config["share_all_bundle"] is True,
         "PREPARE_SCHEMA_OR_DISCLOSURE")
    _limits(support, api, O, config["custody_limits"], config["index_limits"])
    lowered = config.get("bundle_limits", {})
    need(type(lowered) is dict and set(lowered) <= set(vars(B.DEFAULT_LIMITS)), "BUNDLE_LIMIT_FIELDS")
    limits = B.Limits(**lowered)
    targets = _targets(support, api, config["targets"])
    need(len(targets) <= limits.max_targets, "TARGET_LIMIT")
    root = _root(support, host_root, fresh=True)
    bundle = support.ordinary(Path(config["bundle_directory"]), directory=True)
    support.fields(config["manifest"], ("path", "sha256"), "HOST_MANIFEST_FIELDS")
    manifest_path = support.ordinary(Path(config["manifest"]["path"]))
    _separate(root, bundle); _separate(root, manifest_path)
    manifest_raw = support.read(manifest_path, limits.max_manifest_bytes)
    manifest = B.read_manifest(manifest_raw, config["manifest"]["sha256"],
                               limits=limits, check_budget=allowance.check)
    unit_ids = {entry.unit_id for batch in manifest.batches for entry in batch}
    need(all(target["unit_id"] in unit_ids for target in targets), "TARGET_UNIT_NOT_IN_BUNDLE")
    selected = {}
    for target in targets:
        selected.setdefault(target["unit_id"], []).append(target)
    report = _report("prepare", root, profile_sha256)
    report.update(phase="CREATE_HOST", manifest_sha256=manifest.sha256, publications=[])
    try:
        allowance.check()
        with _locked(support, api, root, report, create=True):
            index = custody = None
            error = None
            try:
                report["phase"] = "PREPARE_STORES"
                report["custody_closure"] = "NOT_CONFIRMED"
                custody = O.OrdinaryStore(root/"custody", manifest.semantic_id,
                                          config["custody_limits"], create=True)
                report["custody_closure"] = "OPEN"
                report["index_closure"] = "NOT_CONFIRMED"
                index = _index(support, custody,
                    _index_config(root, config["index_limits"], create=True), allowance.check)
                report["index_closure"] = "OPEN"
                total = B._empty_census()
                for entries in manifest.batches:
                    allowance.check()
                    raws, census = _read_batch(support, B, bundle, entries, limits, allowance.check)
                    total = B._add(total, census); B._total_bound(total, limits)
                    for entry, raw in zip(entries, raws):
                        allowance.check()
                        stored = custody.put_evidence(raw, before_commit=allowance.check)
                        need(stored["identity"] == entry.unit_id and stored["raw_sha256"] == entry.raw_sha256
                             and stored["raw_bytes"] == entry.raw_bytes, "CUSTODY_PUT_BINDING")
                        need(custody.get_evidence(manifest.semantic_id, entry.unit_id, entry.raw_bytes,
                                                 check_budget=allowance.check) == raw, "EVIDENCE_READBACK")
                        for target in selected.get(entry.unit_id, ()):
                            allowance.check()
                            preview = api["PP"].preview_from_evidence(raw, target["name"])
                            api["PP"].resolve(preview, raw)
                            parsed = api["PP"].read_preview(preview)
                            need(parsed.export_id == target["export_id"] and
                                 parsed.document["unit_id"] == target["unit_id"], "TARGET_PREVIEW_BINDING")
                            held = custody.put_preview(preview, before_commit=allowance.check)
                            need(custody.get_preview(held["identity"], len(preview),
                                                     check_budget=allowance.check) == preview, "PREVIEW_READBACK")
                            locator_raw = custody.get_locator(manifest.semantic_id, target["export_id"],
                                                             O.LOCATOR_MAX, check_budget=allowance.check)
                            locator = api["PP"].read_locator(api["E"].strict_json(locator_raw))
                            need(locator == {"schema": api["PP"].LOCATOR_SCHEMA, "semantic_id": manifest.semantic_id,
                                 "unit_id": target["unit_id"], "export_name": target["name"]}, "LOCATOR_READBACK")
                            publication = index.admit(preview, expected_id=target["export_id"])
                            need(index._record(publication["record_id"]) == publication["record"], "INDEX_READBACK")
                            report["publications"].append({"export_id": target["export_id"],
                                "record_id": publication["record_id"], "preview_sha256": held["identity"]})
                    del raws
                need(total.units == manifest.unit_count and total.bytes == manifest.evidence_bytes and
                     len(report["publications"]) == len(targets), "COMPLETE_CENSUS")
                state = index.status(); counts = custody.status()["counts"]
                need(state["objects"] == len(targets), "INDEX_OBJECT_CENSUS")
                need(api["DS"].A.snapshot_id(index.snapshot()) == state["latest"], "INDEX_SNAPSHOT_READBACK")
                seal = {"schema": SEAL_SCHEMA, "profile_sha256": profile_sha256,
                    "semantic_id": manifest.semantic_id, "namespace": index.namespace,
                    "manifest_sha256": manifest.sha256, "targets": targets,
                    "custody_limits": config["custody_limits"], "index_limits": config["index_limits"],
                    "custody_counts": counts, "index_snapshot_id": state["latest"],
                    "index_objects": state["objects"], "assurance": ASSURANCE, "mathematical_acceptance": False}
                report["census"] = vars(total)
            except BaseException as caught:
                error = caught
            finally:
                closing = _close(index, custody, report)
                error = error or closing
            if error is not None:
                raise error
            report["phase"] = "SEAL"
            need(support.read(manifest_path, limits.max_manifest_bytes) == manifest_raw,
                 "MANIFEST_CHANGED")
            _marker(support, api, root); finalize(); allowance.check()
            seal_raw = api["E"].canonical_json(seal)
            need(len(seal_raw) <= 2*MIB, "SEAL_BYTES")
            report["host_sha256"] = hashlib.sha256(seal_raw).hexdigest()
            pending, final = root/".HOST.pending", root/"HOST.json"
            support.write_fresh(pending, seal_raw)
            support.ordinary(final, fresh=True)
            allowance.check(); report["seal_attempted"] = True
            pending.rename(final)
            report["sealed"] = True
        allowance.check()
        report.update(status="PREPARED_INERT_HOST", phase="CLOSED", host_file=str(root/"HOST.json"))
        return report
    except BaseException as error:
        raise _failure(report, error) from error


def _current_content(api, index, custody):
    """Read current bounded metadata and one snapshot, never the stored corpus."""
    state = index.status()
    need(api["DS"].A.snapshot_id(index.snapshot()) == state["latest"], "INDEX_SNAPSHOT_READBACK")
    return {"custody_counts": custody.status()["counts"],
            "index_snapshot_id": state["latest"], "index_objects": state["objects"]}


def initialize(support, host_root, config, allowance, *, profile_sha256, finalize):
    """Create empty stores and then install one immutable operating descriptor."""
    O, api, _ = _modules(support, allowance, profile_sha256, finalize)
    config = _config(api, config)
    support.fields(config, ("schema", "custody_limits", "index_limits", "partial_publication"),
               "HOST_INIT_FIELDS")
    need(config["schema"] == INIT_SCHEMA and config["partial_publication"] is True,
         "INIT_SCHEMA_OR_PARTIAL_PUBLICATION")
    _limits(support, api, O, config["custody_limits"], config["index_limits"])
    root = _root(support, host_root, fresh=True)
    semantic = api["S"].semantic_id()
    report = _report("init", root, profile_sha256)
    report.update(phase="CREATE_HOST", host_identity_kind=INCREMENTAL_IDENTITY,
                  partial_publication=True, descriptor_attempted=False, initialized=False)
    try:
        finalize(); allowance.check()
        with _locked(support, api, root, report, create=True):
            index = custody = None
            error = None
            try:
                report["phase"] = "INITIALIZE_STORES"
                report["custody_closure"] = "NOT_CONFIRMED"
                custody = O.OrdinaryStore(root/"custody", semantic, config["custody_limits"], create=True)
                report["custody_closure"] = "OPEN"
                report["index_closure"] = "NOT_CONFIRMED"
                index = _index(support, custody,
                    _index_config(root, config["index_limits"], create=True), allowance.check)
                report["index_closure"] = "OPEN"
                current = _current_content(api, index, custody)
                state = index.status()
                need(current["custody_counts"] == {"objects": 0, "exports": 0, "logical_bytes": 0}
                     and all(state[key] == 0 for key in ("seq", "objects", "postings", "features"))
                     and state["snapshots"] == 1, "INITIAL_STORES_NOT_EMPTY")
                descriptor = {"schema": DESCRIPTOR_SCHEMA, "profile_sha256": profile_sha256,
                    "semantic_id": semantic, "namespace": index.namespace,
                    "custody_limits": config["custody_limits"], "index_limits": config["index_limits"],
                    "partial_publication": True, "assurance": ASSURANCE, "mathematical_acceptance": False}
                report["current_content"] = current
            except BaseException as caught:
                error = caught
            finally:
                closing = _close(index, custody, report)
                error = error or closing
            if error is not None:
                raise error
            report["phase"] = "INSTALL_DESCRIPTOR"
            _marker(support, api, root); finalize(); allowance.check()
            raw = api["E"].canonical_json(descriptor)
            need(len(raw) <= 2*MIB, "DESCRIPTOR_BYTES")
            report["host_sha256"] = hashlib.sha256(raw).hexdigest()
            pending, final = root/".HOST.pending", root/"HOST.json"
            support.write_fresh(pending, raw)
            support.ordinary(final, fresh=True)
            allowance.check(); report["descriptor_attempted"] = True
            pending.rename(final)
            report["initialized"] = True
        allowance.check()
        report.update(status="INITIALIZED_INCREMENTAL_INERT_HOST", phase="CLOSED",
                      host_file=str(root/"HOST.json"))
        return report
    except BaseException as error:
        raise _failure(report, error) from error


def append(support, host_root, config, allowance, *, profile_sha256,
           expected_host_sha256, finalize):
    """Append one approved bounded batch; every committed prefix may be served."""
    O, api, B = _modules(support, allowance, profile_sha256, finalize)
    config = _config(api, config)
    fields = ("schema", "bundle_directory", "manifest", "targets", "share_all_bundle",
              "allow_partial_publication")
    support.fields(config, (*fields, "bundle_limits") if "bundle_limits" in config else fields,
               "HOST_APPEND_FIELDS")
    need(config["schema"] == APPEND_SCHEMA and config["share_all_bundle"] is True and
         config["allow_partial_publication"] is True, "APPEND_SCHEMA_OR_DISCLOSURE")
    lowered = config.get("bundle_limits", {})
    need(type(lowered) is dict and set(lowered) <= set(vars(B.DEFAULT_LIMITS)), "BUNDLE_LIMIT_FIELDS")
    limits = B.Limits(**lowered)
    targets = _targets(support, api, config["targets"])
    need(len(targets) <= limits.max_targets, "TARGET_LIMIT")
    root = _root(support, host_root, fresh=False)
    bundle = support.ordinary(Path(config["bundle_directory"]), directory=True)
    support.fields(config["manifest"], ("path", "sha256"), "HOST_MANIFEST_FIELDS")
    manifest_path = support.ordinary(Path(config["manifest"]["path"]))
    _separate(root, bundle); _separate(root, manifest_path)
    manifest_raw = support.read(manifest_path, limits.max_manifest_bytes)
    manifest = B.read_manifest(manifest_raw, config["manifest"]["sha256"],
                               limits=limits, check_budget=allowance.check)
    unit_ids = {entry.unit_id for batch in manifest.batches for entry in batch}
    need(all(target["unit_id"] in unit_ids for target in targets), "TARGET_UNIT_NOT_IN_BUNDLE")
    selected = {}
    for target in targets:
        selected.setdefault(target["unit_id"], []).append(target)
    report = _report("append", root, profile_sha256)
    report.update(phase="OPEN_HOST", host_sha256=expected_host_sha256,
                  host_identity_kind=INCREMENTAL_IDENTITY, partial_publication=True,
                  manifest_sha256=manifest.sha256, evidence=[], previews=[], publications=[],
                  batch_complete=False,
                  durable_progress="COMMITS_MAY_EXCEED_REPORTED_PROGRESS_ON_FAILURE")
    try:
        with _locked(support, api, root, report, create=False):
            descriptor = _read_seal(support, O, api, root, profile_sha256, expected_host_sha256)
            need(descriptor["schema"] == DESCRIPTOR_SCHEMA, "APPEND_REQUIRES_INCREMENTAL_HOST")
            need(manifest.semantic_id == descriptor["semantic_id"], "APPEND_SEMANTICS")
            index = custody = None
            error = None
            try:
                report["custody_closure"] = "NOT_CONFIRMED"
                custody = O.OrdinaryStore(root/"custody", manifest.semantic_id,
                                          descriptor["custody_limits"], create=False)
                report["custody_closure"] = "OPEN"
                report["index_closure"] = "NOT_CONFIRMED"
                index = _index(support, custody,
                    _index_config(root, descriptor["index_limits"], create=False), allowance.check)
                report["index_closure"] = "OPEN"
                report["before_content"] = _current_content(api, index, custody)
                _marker(support, api, root); finalize(); allowance.check()
                report["phase"] = "APPEND_ITEMS"
                total = B._empty_census()
                for entries in manifest.batches:
                    allowance.check()
                    raws, census = _read_batch(support, B, bundle, entries, limits, allowance.check)
                    total = B._add(total, census); B._total_bound(total, limits)
                    for entry, raw in zip(entries, raws):
                        allowance.check()
                        stored = custody.put_evidence(raw, before_commit=allowance.check)
                        report["evidence"].append(deepcopy(stored))
                        need(stored["identity"] == entry.unit_id and stored["raw_sha256"] == entry.raw_sha256
                             and stored["raw_bytes"] == entry.raw_bytes, "CUSTODY_PUT_BINDING")
                        need(custody.get_evidence(manifest.semantic_id, entry.unit_id, entry.raw_bytes,
                                                 check_budget=allowance.check) == raw, "EVIDENCE_READBACK")
                        for target in selected.get(entry.unit_id, ()):
                            allowance.check()
                            preview = api["PP"].preview_from_evidence(raw, target["name"])
                            api["PP"].resolve(preview, raw)
                            parsed = api["PP"].read_preview(preview)
                            need(parsed.export_id == target["export_id"] and
                                 parsed.document["unit_id"] == target["unit_id"], "TARGET_PREVIEW_BINDING")
                            held = custody.put_preview(preview, before_commit=allowance.check)
                            report["previews"].append(deepcopy(held))
                            need(custody.get_preview(held["identity"], len(preview),
                                                     check_budget=allowance.check) == preview, "PREVIEW_READBACK")
                            locator_raw = custody.get_locator(manifest.semantic_id, target["export_id"],
                                                             O.LOCATOR_MAX, check_budget=allowance.check)
                            locator = api["PP"].read_locator(api["E"].strict_json(locator_raw))
                            need(locator == {"schema": api["PP"].LOCATOR_SCHEMA, "semantic_id": manifest.semantic_id,
                                 "unit_id": target["unit_id"], "export_name": target["name"]}, "LOCATOR_READBACK")
                            publication = index.admit(preview, expected_id=target["export_id"])
                            report["publications"].append({"export_id": target["export_id"],
                                "record_id": publication["record_id"], "preview_sha256": held["identity"],
                                "new": publication["new"], "snapshot_id": publication["snapshot_id"]})
                            need(index._record(publication["record_id"]) == publication["record"], "INDEX_READBACK")
                    del raws
                need(total.units == manifest.unit_count and total.bytes == manifest.evidence_bytes and
                     len(report["publications"]) == len(targets), "COMPLETE_CENSUS")
                report["census"] = vars(total)
                report["current_content"] = _current_content(api, index, custody)
            except BaseException as caught:
                error = caught
            finally:
                closing = _close(index, custody, report)
                error = error or closing
            if error is not None:
                raise error
            report["phase"] = "FINALIZE"
            need(support.read(manifest_path, limits.max_manifest_bytes) == manifest_raw,
                 "MANIFEST_CHANGED")
            need(_read_seal(support, O, api, root, profile_sha256, expected_host_sha256) == descriptor,
                 "DESCRIPTOR_CHANGED")
            _marker(support, api, root); finalize(); allowance.check()
        allowance.check()
        report.update(status="APPENDED_INERT_HOST", phase="CLOSED", batch_complete=True,
                      durable_progress="COMPLETE_SELECTED_BATCH")
        return report
    except BaseException as error:
        raise _failure(report, error) from error


def _read_seal(support, O, api, root, profile_sha256, expected_host_sha256):
    raw = support.read(root/"HOST.json", 2*MIB)
    need(hashlib.sha256(raw).hexdigest() == support.hexid(expected_host_sha256), "SEAL_PIN")
    seal = api["F"].strict(raw, 2*MIB)
    if type(seal) is dict and seal.get("schema") == DESCRIPTOR_SCHEMA:
        support.fields(seal, DESCRIPTOR_FIELDS, "HOST_DESCRIPTOR_FIELDS")
        need(api["E"].canonical_json(seal) == raw and seal["profile_sha256"] == profile_sha256 and
             seal["semantic_id"] == api["S"].semantic_id() and seal["partial_publication"] is True and
             seal["assurance"] == ASSURANCE and seal["mathematical_acceptance"] is False,
             "DESCRIPTOR_IDENTITY")
        need(seal["namespace"] == api["OA"].OrdinaryExportAdapter(seal["semantic_id"]).namespace,
             "DESCRIPTOR_NAMESPACE")
        _limits(support, api, O, seal["custody_limits"], seal["index_limits"])
        return seal
    support.fields(seal, SEAL_FIELDS, "HOST_SEAL_FIELDS")
    need(api["E"].canonical_json(seal) == raw and seal["schema"] == SEAL_SCHEMA and
         seal["profile_sha256"] == profile_sha256 and seal["semantic_id"] == api["S"].semantic_id() and
         seal["assurance"] == ASSURANCE and seal["mathematical_acceptance"] is False, "SEAL_IDENTITY")
    need(seal["namespace"] == api["OA"].OrdinaryExportAdapter(seal["semantic_id"]).namespace, "SEAL_NAMESPACE")
    support.hexid(seal["manifest_sha256"]); support.hexid(seal["index_snapshot_id"])
    _limits(support, api, O, seal["custody_limits"], seal["index_limits"])
    targets = _targets(support, api, seal["targets"])
    support.uint(seal["index_objects"], 1, 64, "HOST_INDEX_OBJECT_COUNT")
    need(seal["index_objects"] == len(targets), "SEAL_TARGET_CENSUS")
    support.fields(seal["custody_counts"], ("objects", "exports", "logical_bytes"), "HOST_CUSTODY_COUNTS")
    for key, value in seal["custody_counts"].items():
        support.uint(value, 0, seal["custody_limits"][key], "HOST_CUSTODY_COUNT:"+key)
    return seal


def serve(support, host_root, config, allowance, *, profile_sha256,
          expected_host_sha256, finalize, ready=None):
    """Serve static or current incremental content under the same permanent lock."""
    O, api, _ = _modules(support, allowance, profile_sha256, finalize)
    config = _config(api, config)
    support.fields(config, ("schema", "host", "port", "tls", "lease_seconds", "cleanup_seconds",
                       "limits", "share_all_custody", "exclusive"), "HOST_SERVE_FIELDS")
    need(config["schema"] == SERVE_SCHEMA and config["share_all_custody"] is True and
         config["exclusive"] is True and (ready is None or callable(ready)), "SERVE_SCHEMA_OR_DISCLOSURE")
    root = _root(support, host_root, fresh=False)
    support.hexid(expected_host_sha256)
    if config["tls"] is not None:
        support.fields(config["tls"], ("cert_file", "cert_sha256", "key_file", "key_sha256"),
                    "HOST_TLS_FIELDS")
        for field in ("cert_file", "key_file"):
            _separate(root, support.ordinary(Path(config["tls"][field])))
    report = _report("serve", root, profile_sha256)
    report.update(phase="OPEN_HOST", host_sha256=expected_host_sha256)
    try:
        with _locked(support, api, root, report, create=False):
            seal = _read_seal(support, O, api, root, profile_sha256, expected_host_sha256)
            incremental = seal["schema"] == DESCRIPTOR_SCHEMA
            if incremental:
                report.update(host_identity_kind=INCREMENTAL_IDENTITY, partial_publication=True,
                              prior_append_completion="NOT_ASSERTED_BY_SERVICE")
            custody = index = None
            error = None
            try:
                allowance.check()
                report["custody_closure"] = "NOT_CONFIRMED"
                custody = O.OrdinaryStore(root/"custody", seal["semantic_id"], seal["custody_limits"], create=False)
                report["custody_closure"] = "OPEN"
                if not incremental:
                    need(custody.status()["counts"] == seal["custody_counts"], "SEALED_CUSTODY_CHANGED")
                index_config = _index_config(root, seal["index_limits"], create=False)
                report["index_closure"] = "NOT_CONFIRMED"
                index = _index(support, custody, index_config, allowance.check)
                report["index_closure"] = "OPEN"
                state = index.status()
                if incremental:
                    report["current_content"] = _current_content(api, index, custody)
                else:
                    need(state["latest"] == seal["index_snapshot_id"] and
                         state["objects"] == seal["index_objects"], "SEALED_INDEX_CHANGED")
                closing = _close(index, None, report)
                if closing is not None:
                    raise closing
                index = None
                report["preflight_index_closure"] = report["index_closure"]
                service_config = {key: value for key, value in config.items() if key != "schema"}
                service_config["index"] = index_config
                _marker(support, api, root); finalize(); allowance.check()
                report["phase"] = "SERVE"
                report["index_closure"] = "NOT_CONFIRMED"
                def listening(value):
                    value = deepcopy(value)
                    if incremental:
                        value.update(host_identity_kind=INCREMENTAL_IDENTITY,
                                     current_content=deepcopy(report["current_content"]),
                                     prior_append_completion="NOT_ASSERTED_BY_SERVICE")
                    report["ready"] = deepcopy(value)
                    if ready is not None:
                        ready({**deepcopy(value), "host_root": str(root), "host_sha256": expected_host_sha256,
                               "assurance": ASSURANCE})
                # Runner shutdown cancels/drains any remaining provider tasks
                # before control can leave this held host lock. A stuck shutdown
                # remains under the caller's original outer Job allowance.
                report["service"] = asyncio.run(
                    _service(support, custody, service_config, allowance, ready=listening))
                report["index_closure"] = "CLOSED"
            except BaseException as caught:
                error = caught
                if isinstance(getattr(caught, "report", None), dict):
                    report["service"] = caught.report
            finally:
                closing = _close(index, custody, report)
                error = error or closing
            try:
                finalize(); allowance.check()
            except BaseException as caught:
                report["finalize_error"] = _error(caught)
                error = error or caught
            if error is not None:
                raise error
        allowance.check()
        report.update(status=report["service"]["status"], phase="CLOSED")
        return report
    except BaseException as error:
        raise _failure(report, error) from error

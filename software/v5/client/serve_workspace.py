"""Finite read-only HTTP entry for an existing, exclusively owned workspace.

Run as a trusted owner through client.boot, never as an uncontained daemon.
Read-only describes remote routes: opening/querying can write local metadata.
Serving data does not verify it or issue mathematical authority.
"""
import asyncio
from copy import deepcopy
import hashlib
from importlib import import_module
import ipaddress
import json
import math
from pathlib import Path
import time

from discovery.discovery_store import ordinary
from transport.http_provider import server_tls

SCHEMA = "DMKN_V5_WORKSPACE_SERVICE_V1"
MIB = 1024**2
MODES = {
    "atomic": ("client.workspace_atomic", "frontier_network.transport"),
    "mixed": ("client.workspace_mixed", "mixed_network.transport"),
    "evidence": ("client.workspace_evidence", "evidence_network.transport"),
    "staged": ("client.workspace_staged", "evidence_network.transport"),
    "validated": ("client.workspace_validated", "evidence_network.transport"),
}
LIMITS = {"max_connections": (1, 8), "max_requests": (1, 1000000),
          "max_reply_bytes": (1024, 2**40), "operation_ms": (1, 60000)}


def _need(ok, reason):
    if not ok:
        raise ValueError(reason)


def _fields(value, expected):
    _need(type(value) is dict and set(value) == set(expected), "SERVICE_FIELDS")


def _types(mode):
    """Closed local selection; no profile fallback, migration, or remote code."""
    _need(type(mode) is str and mode in MODES, "SERVICE_MODE")
    workspace, provider = MODES[mode]
    return import_module(workspace).Workspace, import_module(provider).CompositeProvider


def _save(path, value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                     allow_nan=False).encode("utf-8")
    _need(len(raw) <= MIB, "SERVICE_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def _error(error):
    return {"type": type(error).__name__, "message": str(error)[:500]}


def _tls_pin(row):
    _fields(row, {"path", "bytes", "sha256"})
    _need(type(row["path"]) is str and type(row["bytes"]) is int
          and 0 < row["bytes"] <= MIB and type(row["sha256"]) is str
          and len(row["sha256"]) == 64
          and all(ch in "0123456789abcdef" for ch in row["sha256"]), "SERVICE_TLS_PIN")
    path = ordinary(row["path"], directory=False)
    _need(path.stat().st_size == row["bytes"], "SERVICE_TLS_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(row["bytes"]+1)
    _need(len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"],
          "SERVICE_TLS_CHANGED")
    return path


def _parameters(context):
    params = deepcopy(dict(context.parameters))
    _fields(params, {"schema", "mode", "workspace_path", "workspace_config",
                     "bind", "tls", "service_limits"})
    _need(params["schema"] == SCHEMA, "SERVICE_SCHEMA")
    _need(type(params["mode"]) is str and params["mode"] in MODES, "SERVICE_MODE")
    _need(type(params["workspace_config"]) is dict, "SERVICE_WORKSPACE_CONFIG")
    bind, limits = params["bind"], params["service_limits"]
    _fields(bind, {"host", "port"})
    _need(type(bind["host"]) is str and len(bind["host"]) <= 64, "SERVICE_BIND_HOST")
    address = ipaddress.ip_address(bind["host"])
    _need(not address.is_unspecified and not address.is_multicast
          and (address.is_loopback or params["tls"] is not None), "SERVICE_BIND_POLICY")
    _need(type(bind["port"]) is int and 0 <= bind["port"] <= 65535, "SERVICE_BIND_PORT")
    _fields(limits, {*LIMITS, "lifetime_seconds"})
    for name, (low, high) in LIMITS.items():
        _need(type(limits[name]) is int and low <= limits[name] <= high, "SERVICE_LIMIT:"+name)
    lifetime = limits["lifetime_seconds"]
    _need(type(lifetime) in (int, float) and math.isfinite(lifetime)
          and 0 < lifetime <= 3600, "SERVICE_LIFETIME")
    _need(type(context.deadline) in (int, float) and math.isfinite(context.deadline),
          "SERVICE_OUTER_DEADLINE")
    # Let one in-flight synchronous dispatch finish, then drain/report. The
    # enclosing Job remains the hard bound if dispatch or OS cleanup misbehaves.
    reserve = limits["operation_ms"]/1000 + 5
    _need(time.monotonic() < context.deadline-reserve, "SERVICE_NO_CLEANUP_MARGIN")
    _need(type(params["workspace_path"]) is str, "SERVICE_WORKSPACE_PATH")
    workspace = ordinary(params["workspace_path"])
    run = ordinary(context.run)
    work = ordinary(context.location_workspace)
    _need(work != run and work.is_relative_to(run), "SERVICE_OUTPUT_SCOPE")
    roots = (context.installation, run, context.sources_v5,
             context.sources_portable, context.sources_owner)
    for value in roots:
        root = ordinary(value)
        _need(not workspace.is_relative_to(root) and not root.is_relative_to(workspace),
              "SERVICE_WORKSPACE_DISJOINT")
    outputs = tuple(ordinary(work/name, fresh=True, directory=False)
                    for name in ("service-ready.json", "service-result.json"))
    tls = None
    if params["tls"] is not None:
        _fields(params["tls"], {"certificate", "private_key"})
        certificate = _tls_pin(params["tls"]["certificate"])
        key = _tls_pin(params["tls"]["private_key"])
        tls = server_tls(certificate, key)
    return params, workspace, outputs, tls, reserve


def _close_workspace(workspace, errors):
    """Attempt remaining closes even if the predecessor's sequential close fails."""
    try:
        workspace.close()
    except BaseException as error:
        errors.append({"component": "workspace", **_error(error)})
        # No grants or mathematical clients are created by this entry. A failed
        # close is still a failed service, even when these fallback closes work.
        for name in ("index", "packets", "modules", "db", "_lock"):
            component = getattr(workspace, name, None)
            if component is None:
                continue
            try:
                component.close()
            except BaseException as tail:
                errors.append({"component": name, **_error(tail)})
        return False
    return bool(workspace._closed and workspace.db is None and workspace._lock is None
                and all(store is None or store.db is None
                        for store in (workspace.index, workspace.packets, workspace.modules)))


async def serve(context):
    """Serve once, publish READY while live, then return/save a terminal report.

    Invalid parameters raise before opening data. Runtime/cleanup errors return
    FAILED; cancellation attempts cleanup and then propagates cancellation.
    """
    params, path, (ready_path, result_path), tls, reserve = _parameters(context)
    Workspace, Provider = _types(params["mode"])
    started = time.monotonic()
    deadline = min(started+params["service_limits"]["lifetime_seconds"],
                   context.deadline-reserve)
    workspace = provider = None
    cancelled = None
    report = {"schema": "DMKN_V5_WORKSPACE_SERVICE_RESULT_V1", "status": "FAILED",
        "error": None, "cleanup": {"http_closed": False, "workspace_closed": False, "errors": []},
        "endpoint": None, "namespace": None, "wire_profile": None, "counters": None,
        "started": started, "deadline": deadline, "outer_deadline": context.deadline,
        "cleanup_reserve_seconds": reserve, "mode": params["mode"],
        "workspace_path": str(path), "service_limits": params["service_limits"],
        "authority": "OPERATIONAL_SERVICE_DATA_NOT_MATHEMATICAL_AUTHORITY",
        "mathematical_acceptance": False}
    try:
        workspace = Workspace.open(path, params["workspace_config"], create=False)
        _need(time.monotonic() < deadline, "SERVICE_STARTUP_DEADLINE")
        provider = Provider(index=workspace.index, custody=workspace.modules,
                            packets=workspace.packets,
                            **{name: params["service_limits"][name] for name in LIMITS})
        report["namespace"] = workspace.index.namespace
        report["wire_profile"] = workspace.packets.profile_id
        async with asyncio.timeout_at(deadline):
            endpoint = await provider.start(**params["bind"], tls_context=tls)
        report["endpoint"] = {name: getattr(endpoint, name)
                              for name in ("host", "port", "tls", "server_name")}
        _need(time.monotonic() < deadline, "SERVICE_STARTUP_DEADLINE")
        _save(ready_path, {"schema": "DMKN_V5_WORKSPACE_SERVICE_READY_V1",
            "endpoint": report["endpoint"], "namespace": report["namespace"],
            "wire_profile": report["wire_profile"], "deadline": deadline,
            "outer_deadline": context.deadline, "mode": params["mode"],
            "authority": report["authority"], "mathematical_acceptance": False})
        await asyncio.sleep(max(0, deadline-time.monotonic()))
        report["status"] = "PASS"
    except BaseException as error:
        report["error"] = _error(error)
        if isinstance(error, asyncio.CancelledError):
            cancelled = error
    finally:
        errors = report["cleanup"]["errors"]
        if provider is not None:
            try:
                remaining = min(5, context.deadline-time.monotonic())
                _need(remaining > 0, "SERVICE_CLEANUP_DEADLINE")
                async with asyncio.timeout(remaining):
                    await provider.stop()
                report["cleanup"]["http_closed"] = (provider.server is None
                    and not provider.tasks and provider.reserved_reply_bytes == 0)
                _need(report["cleanup"]["http_closed"], "SERVICE_HTTP_CLEANUP_UNCERTAIN")
            except BaseException as error:
                errors.append({"component": "http", **_error(error)})
                # A stop failure must not skip listener close or cancellation
                # of live handlers. These best-effort actions never clear the
                # cleanup error or manufacture a clean-success report.
                if provider.server is not None:
                    try:
                        provider.server.close()
                    except BaseException as tail:
                        errors.append({"component": "http_listener", **_error(tail)})
                tasks = tuple(provider.tasks)
                for task in tasks:
                    task.cancel()
                remaining = min(1, context.deadline-time.monotonic())
                if tasks and remaining > 0:
                    try:
                        async with asyncio.timeout(remaining):
                            await asyncio.gather(*tasks, return_exceptions=True)
                    except BaseException as tail:
                        errors.append({"component": "http_handlers", **_error(tail)})
            try:
                report["counters"] = provider.status()
            except BaseException as error:
                errors.append({"component": "http_status", **_error(error)})
        else:
            report["cleanup"]["http_closed"] = True
        if workspace is not None:
            report["cleanup"]["workspace_closed"] = _close_workspace(workspace, errors)
            if not report["cleanup"]["workspace_closed"] and not errors:
                errors.append({"component": "workspace", "type": "CleanupUncertain",
                               "message": "SERVICE_WORKSPACE_CLEANUP_UNCERTAIN"})
        else:
            # open() owns its internal partial construction cleanup. There is
            # no returned object to reclaim if that operation itself raises.
            report["cleanup"]["workspace_closed"] = False
        if errors or not all(report["cleanup"][name]
                             for name in ("http_closed", "workspace_closed")):
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        if report["finished"] >= context.deadline:
            report["status"] = "FAILED"
            errors.append({"component": "deadline", "type": "DeadlineExceeded",
                           "message": "SERVICE_ORIGINAL_DEADLINE_EXHAUSTED"})
        _save(result_path, report)
    if cancelled is not None:
        raise cancelled
    return report


def main(context):
    return 0 if asyncio.run(serve(context))["status"] == "PASS" else 1

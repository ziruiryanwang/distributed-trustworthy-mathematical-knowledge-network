"""Bounded ordinary-peer coordination over the unchanged acceptance APIs.

The selected package loader must verify this module and its import closure first.
Callers own the loaded package, original allowance and serialized owner/custody
handles. Peer data is inert. Owner-controlled immutable files/OS and exclusive
store use are premises; cooperative controller checks require an external Job
for hard CPU/memory/wall containment. No daemon, retry or remote source execution.
"""
from __future__ import annotations

import asyncio
from copy import deepcopy
import hashlib
import ipaddress
import math
from pathlib import Path
import re
import time

import ordinary_admission as A
import portable_preview as PP
from discovery import candidate_query as CQ
from discovery import discovery_store as DS
from discovery import formal_features as F
from discovery.ordinary_export_adapter import OrdinaryExportAdapter, compile_query
from discovery.search_session import SearchSession, LIMITS as SEARCH_LIMITS
from transport import http_provider as H
from transport import ordinary_acquisition as O
from transport.clients import SearchClient

MIB = 1024**2
CONTROLLER_LIMITS = "COOPERATIVE_REQUIRES_EXTERNAL_JOB"
RECEIVE_LIMITS = {"requests": (1, 8192), "reply_bytes": (1, 1024*MIB),
                  "units": (1, 1024), "unit_bytes": (1, O.EVIDENCE_MAX),
                  "total_bytes": (1, 64*MIB), "missing": (1, 4096),
                  "preflights": (1, 1025), "locator_bytes": (1, O.LOCATOR_MAX)}
PROVIDER_LIMITS = {"max_connections": (1, 8), "max_requests": (1, 1000000),
                   "max_reply_bytes": (1024, 2**40), "operation_ms": (1, 60000)}


class PeerFailure(ValueError):
    """Failure with retained partial outcomes, never rollback of acceptance."""
    def __init__(self, report):
        self.report = report
        super().__init__(report["error"]["code"])


def _error(error):
    message = str(error)
    code = message if len(message) <= 160 and re.fullmatch(r"[A-Z0-9_:.+-]+", message) else "PEER_OPERATION_FAILED"
    return {"type": type(error).__name__, "code": code}


def _fields(value, keys, code):
    A.need(type(value) is dict and set(value) == set(keys), code)


def _limits(value, bounds, code):
    _fields(value, bounds, code)
    for key, interval in bounds.items():
        F.uint(value[key], *interval, code+":"+key)
    return dict(value)


def _begin(loaded, config, allowance, operation):
    allowance.check()
    A.need(loaded.A is A and loaded.O is O and type(loaded.installation) is A.NativeInstallation,
           "PEER_SELECTED_MODULE_IDENTITY")
    A.need(type(config) is dict and len(F.compact(config)) <= 2*MIB, "PEER_CONFIG_BOUND")
    return deepcopy(config), {"operation": operation, "status": "STARTED",
        "mathematical_acceptance": False, "controller_limits": CONTROLLER_LIMITS,
        "cleanup_errors": []}


def _state(loaded, owner, custody):
    A.need(type(custody) is O.OrdinaryStore and custody.semantic_id == loaded.installation.semantic_id,
           "PEER_CUSTODY_BINDING")
    custody._active()
    if owner is not None:
        A.need(type(owner) is A.OrdinaryAdmission and owner.installation is loaded.installation
               and owner.evidence_store is custody, "PEER_OWNER_BINDING")


def _pin(path, digest, check):
    check(); F.hexid(digest)
    A.need(type(path) is str, "PEER_PIN_PATH")
    selected = A.C.ordinary(Path(path))
    raw = A.C.read_bounded(selected, MIB)
    A.need(hashlib.sha256(raw).hexdigest() == digest, "PEER_FILE_PIN")
    check()
    return selected, digest


def _repin(pins, check):
    for path, digest in pins:
        _pin(str(path), digest, check)


def _contacts(config, check):
    """CA files stay immutable under the same owner/OS premise as package code.

    Verify pins before/after each operation; remote peers cannot choose a path,
    referral, trust store or server name. Null CA explicitly selects system CAs.
    """
    A.need(type(config) is dict and 1 <= len(config) <= 64, "PEER_CONTACTS_BOUND")
    endpoints, pins = {}, []
    for label, row in config.items():
        A.need(type(label) is str and 1 <= len(label.encode("utf-8")) <= 128
               and all(ord(c) >= 32 for c in label), "PEER_CONTACT_LABEL")
        _fields(row, ("host", "port", "tls", "server_name", "ca_file", "ca_sha256"), "PEER_CONTACT_FIELDS")
        A.need((row["ca_file"] is None) == (row["ca_sha256"] is None), "PEER_CA_PIN_PAIR")
        endpoint = H.Endpoint(row["host"], row["port"], row["tls"], row["server_name"], row["ca_file"])
        endpoint.validate()
        if row["ca_file"] is not None:
            pins.append(_pin(row["ca_file"], row["ca_sha256"], check))
        endpoints[label] = endpoint
    return endpoints, pins


def _network(allowance, requests, reply_bytes, existing, deadline):
    allowance.check()
    until = min(allowance.deadline-3, deadline)
    if existing is None:
        return O.OrdinaryBudget(deadline=until, requests=requests, reply_bytes=reply_bytes), True
    A.need(type(existing) is O.OrdinaryBudget and existing.pending is None,
           "PEER_SHARED_NETWORK_BUDGET")
    existing.active()
    A.need(existing.request_cap >= requests and existing.byte_cap >= reply_bytes,
           "PEER_SHARED_NETWORK_CAPS")
    existing.deadline = min(existing.deadline, until)  # Narrow only; never renew.
    existing.active()
    return existing, False


def _failure(report, error):
    report.update(status="FAILED", error=_error(error))
    return PeerFailure(report)


async def find(loaded, config, allowance, *, network_budget=None):
    """Unknown-ID positive search. Results remain incomplete inert metadata.

    Composed callers supply one OrdinaryBudget created before find; the entire
    search suballocation is prepaid before any I/O and never refunded. Separate
    CLI calls are separate explicit owner grants, not automatic continuation.
    """
    config, report = _begin(loaded, config, allowance, "find")
    report.update(matches=[], offers=[], termination=None, global_complete=False,
                  verified_scan_coverage=False, search=None, network=None)
    ledger = client = None
    own_ledger = False
    error = None
    try:
        _fields(config, ("contacts", "providers", "specs", "limits", "offer", "page"), "PEER_FIND_FIELDS")
        endpoints, pins = _contacts(config["contacts"], allowance.check)
        providers = config["providers"]
        A.need(type(providers) is list and 1 <= len(providers) <= 64
               and all(type(p) is str and p in endpoints for p in providers)
               and len(set(providers)) == len(providers), "PEER_FIND_PROVIDERS")
        limits = _limits(config["limits"], SEARCH_LIMITS, "PEER_SEARCH_LIMITS")
        # Bound retained CLI results independently of the provider's counters.
        A.need(limits["candidates"] <= 256 and limits["requests"] <= 512
               and limits["bytes"] <= 32*MIB, "PEER_SEARCH_RESULT_PROFILE")
        offer = _limits(config["offer"], {"max_bytes": (1024, MIB),
            "max_expanded_bytes": (1024, MIB), "max_age_ms": (1, 3600000)}, "PEER_OFFER_LIMITS")
        page = _limits(config["page"], CQ.LIMITS, "PEER_CANDIDATE_LIMITS")
        adapter = OrdinaryExportAdapter(loaded.installation.semantic_id)
        features = compile_query(adapter.namespace, config["specs"])
        ledger, own_ledger = _network(allowance, limits["requests"], limits["bytes"],
                                      network_budget, allowance.deadline-3)
        ledger.charge_external("peer-find", limits["requests"], limits["bytes"])
        limits["wall_ms"] = min(limits["wall_ms"], math.floor((ledger.deadline-time.monotonic())*1000))
        F.uint(limits["wall_ms"], 1, 3600000, "PEER_SEARCH_REMAINING_TIME")
        client = SearchClient(SearchSession(adapter.namespace, features, limits), endpoints)
        report["namespace"], report["features"] = adapter.namespace, features
        async with asyncio.timeout_at(ledger.deadline):
            for provider in providers:
                allowance.check(); _repin(pins, allowance.check)
                found = await client.offer(provider, **offer)
                allowance.check(); _repin(pins, allowance.check)
                report["offers"].append({key: found[key] for key in
                    ("status", "snapshot_id", "reason") if key in found} | {"provider": provider})
                if found["status"] != "OFFERED":
                    continue
                for partition in found["partitions"]:
                    start = 0
                    while start < partition["anchor_count"]:
                        allowance.check(); _repin(pins, allowance.check)
                        result = await client.candidates(provider, found["snapshot_id"],
                            partition["partition"], start, page)
                        allowance.check(); _repin(pins, allowance.check)
                        report["matches"].extend({"provider": provider,
                            "snapshot_id": found["snapshot_id"], "record": row}
                            for row in result["new_matches"])
                        next_cursor = result["advisory_next"]
                        if next_cursor is None or next_cursor["next"] <= start:
                            break  # Advisory stop only, never absence or coverage.
                        start = next_cursor["next"]
        report["termination"] = "SELECTED_CONTACTS_FINISHED_NO_COMPLETENESS_CLAIM"
        report["status"] = "INCOMPLETE_SEARCH"
    except BaseException as caught:
        if isinstance(caught, ValueError) and str(caught).startswith("SESSION_BUDGET:"):
            report.update(status="INCOMPLETE_SEARCH", termination=str(caught))
        else:
            error = caught
    finally:
        if client is not None:
            report["search"] = client.report()
            report["http_overhead_upper_bounds"] = {
                "request_body_bytes": client.session.used["requests"]*H.REQUEST_MAX,
                "header_bytes": client.session.used["requests"]*2*H.HEADER_MAX}
        if ledger is not None:
            if own_ledger:
                try: ledger.close()
                except BaseException as caught:
                    report["cleanup_errors"].append(_error(caught)); error = error or caught
            report["network"] = ledger.report()
    try: allowance.check()
    except BaseException as caught: error = error or caught
    if error is not None:
        raise _failure(report, error) from error
    return report


async def receive(loaded, owner, custody, config, allowance, *, network_budget=None):
    """Acquire an explicitly selected target/closure, then independently admit.

    Snapshot/record data selects bytes, not a warrant. No proof/native artifact
    supplied by a peer enters the local acceptance context without owner.admit.
    """
    config, report = _begin(loaded, config, allowance, "receive")
    report.update(admission=None, acquisition=None, frontier=[], unit_ids=[], network=None)
    operation = ledger = client = None
    own_ledger = False
    error = None
    try:
        _fields(config, ("contacts", "selection", "parent_root", "limits"), "PEER_RECEIVE_FIELDS")
        _state(loaded, owner, custody)
        parent = F.hexid(config["parent_root"])
        limits = _limits(config["limits"], RECEIVE_LIMITS, "PEER_RECEIVE_LIMITS")
        A.need(limits["unit_bytes"] <= limits["total_bytes"], "PEER_CLOSURE_BYTE_LIMITS")
        if network_budget is not None:
            # These two receive fields describe the ORIGINAL aggregate grant,
            # including prepaid discovery, not a replenished receive allowance.
            A.need(type(network_budget) is O.OrdinaryBudget and
                   limits["requests"] == network_budget.request_cap and
                   limits["reply_bytes"] == network_budget.byte_cap, "PEER_RECEIVE_SHARED_GRANT")
        endpoints, pins = _contacts(config["contacts"], allowance.check)
        selection = config["selection"]
        _fields(selection, ("provider", "snapshot_id", "record"), "PEER_SELECTION_FIELDS")
        provider = selection["provider"]
        A.need(type(provider) is str and provider in endpoints, "PEER_SELECTED_CONTACT")
        F.hexid(selection["snapshot_id"])  # Retained provenance, never authority.
        adapter = OrdinaryExportAdapter(loaded.installation.semantic_id)
        record = F.validate_record(selection["record"], adapter.namespace)
        A.need(record["schema"] == F.ORDINARY_EXPORT_RECORD_SCHEMA, "PEER_ORDINARY_RECORD")
        operation = allowance.operation(A)  # Before any preview/evidence fetch.
        ledger, own_ledger = _network(allowance, limits["requests"], limits["reply_bytes"],
                                      network_budget, operation.deadline)
        operation.deadline = min(operation.deadline, ledger.deadline)
        def live():
            allowance.check(); operation.check(); ledger.active(); _repin(pins, allowance.check)
        owner.catalog.context(parent); live()  # Refuse wrong parent before I/O.
        client = O.OrdinaryAcquisition(adapter, endpoints, ledger, local_custody=custody)
        units, requested = {}, set()
        preflight_limits = A.PreflightLimits(max_units=limits["units"], max_bytes=limits["total_bytes"])
        def retain(raw, identity):
            live()
            A.need(identity not in units or units[identity] == raw, "PEER_UNIT_COLLISION")
            if identity not in units:
                A.need(len(units) < limits["units"] and
                       sum(map(len, units.values()))+len(raw) <= limits["total_bytes"], "PEER_FINITE_CLOSURE")
                units[identity] = raw
                report["unit_ids"] = sorted(units)
        async with asyncio.timeout_at(operation.deadline):
            live()
            preview = await client.preview(provider, record)
            live()
            locator = record["locator"]
            selected = await client.evidence(provider, loaded.installation.semantic_id,
                locator["unit_id"], limits["unit_bytes"], expected_export_id=record["object_id"],
                expected_export_name=locator["export_name"])
            live(); PP.resolve(preview["raw"], selected["raw"])
            retain(selected["raw"], locator["unit_id"])
            plan = None
            for _ in range(limits["preflights"]):
                live()
                plan = owner.preflight(parent, list(units.values()), limits=preflight_limits, budget=operation)
                live()
                A.need(len(plan.missing) <= limits["missing"], "PEER_MISSING_FRONTIER_BOUND")
                report["frontier"].append({"status": plan.status, "missing_count": len(plan.missing),
                                            "units": len(units)})
                if plan.status == "READY":
                    break
                before = len(units)
                for name_raw, identity in plan.missing:
                    live()
                    pair = (name_raw, identity)
                    A.need(pair not in requested and len(requested) < limits["missing"],
                           "PEER_NO_PROGRESS_OR_MISSING_CAP")
                    requested.add(pair)
                    name = A.E.strict_json(name_raw)
                    located = await client.locator(provider, loaded.installation.semantic_id, identity,
                        limits["locator_bytes"], expected_name=name)
                    live(); uid = located["locator"]["unit_id"]
                    if uid not in units:
                        A.need(len(units) < limits["units"], "PEER_CLOSURE_UNIT_CAP")
                        remaining = limits["total_bytes"]-sum(map(len, units.values()))
                        A.need(remaining > 0, "PEER_CLOSURE_BYTE_CAP")
                        fetched = await client.evidence(provider, loaded.installation.semantic_id, uid,
                            min(limits["unit_bytes"], remaining), expected_export_id=identity,
                            expected_export_name=name)
                        live(); retain(fetched["raw"], uid)
                    else:
                        parsed = A.PE.read_evidence(units[uid])
                        A.need(any(A.E.name_key(row[0]) == name_raw for row in parsed.document["unit"][2]),
                               "PEER_EXISTING_UNIT_EXPORT_OMISSION")
                A.need(len(units) > before, "PEER_CLOSURE_NO_PROGRESS")
            A.need(plan is not None and plan.status == "READY", "PEER_PREFLIGHT_CAP")
        live()
        accepted = owner.admit(parent, plan, operation)
        # Set this before any checking/reporting/cleanup that could subsequently fail.
        report["admission"] = accepted
        A.need(accepted["status"] in ("CHECKED", "REUSED"), "PEER_ADMISSION_STATUS")
        report["mathematical_acceptance"] = accepted["status"] == "CHECKED"
        report["acceptance_facet"] = "NEW_LOCAL_NATIVE_ACCEPTANCE" if accepted["status"] == "CHECKED" else "EXISTING_LOCAL_ACCEPTANCE_NO_NEW_CHECK"
        report["local_acceptance_available"] = True
        report["status"] = "CHECKED" if accepted["status"] == "CHECKED" else "REUSED_LOCAL_ACCEPTANCE"
        report["target"] = {"name": locator["export_name"], "unit_id": locator["unit_id"],
                            "export_id": record["object_id"]}
        live()
    except BaseException as caught:
        error = caught
    finally:
        if operation is not None:
            try: allowance.account(operation.worker_cpu)
            except BaseException as caught:
                report["cleanup_errors"].append(_error(caught)); error = error or caught
        if ledger is not None:
            if own_ledger:
                try: ledger.close()
                except BaseException as caught:
                    report["cleanup_errors"].append(_error(caught)); error = error or caught
            report["network"] = ledger.report()
        if client is not None:
            report["acquisition"] = client.report()
    try: allowance.check()
    except BaseException as caught: error = error or caught
    if error is not None:
        raise _failure(report, error) from error
    return report


def _index(loaded, owner, custody, config, check):
    _fields(config, ("path", "limits", "create"), "PEER_INDEX_FIELDS")
    A.need(type(config["create"]) is bool and type(config["path"]) is str, "PEER_INDEX_CONFIGURATION")
    _limits(config["limits"], DS.LIMITS, "PEER_INDEX_LIMITS")
    root = A.C.ordinary(Path(config["path"]), directory=True, fresh=config["create"])
    protected = [loaded.root, *loaded.installation.runtime_roots.values(), custody.root]
    if owner is not None: protected.append(owner.directory)
    for path in protected:
        A.need(not root.is_relative_to(path) and not path.is_relative_to(root), "PEER_INDEX_STORAGE_OVERLAP")
    check()
    return DS.Store(root, OrdinaryExportAdapter(loaded.installation.semantic_id),
                    config["limits"], create=config["create"])


def publish(loaded, owner, custody, config, allowance):
    """Index selected local accepted outputs; indexing itself is not admission.

    Multiple targets are separately committed, not one atomic batch. Retain each
    successful publication immediately so later refusal/cleanup cannot erase it.
    """
    config, report = _begin(loaded, config, allowance, "publish")
    report.update(publications=[], local_context=None)
    index = None
    error = None
    try:
        _fields(config, ("index", "context_root", "targets", "max_unit_bytes", "max_total_bytes"),
                "PEER_PUBLISH_FIELDS")
        _state(loaded, owner, custody)
        context_root = F.hexid(config["context_root"])
        F.uint(config["max_unit_bytes"], 1, O.EVIDENCE_MAX, "PEER_PUBLISH_UNIT_BYTES")
        F.uint(config["max_total_bytes"], 1, 64*MIB, "PEER_PUBLISH_TOTAL_BYTES")
        targets = config["targets"]
        A.need(type(targets) is list and 1 <= len(targets) <= 64, "PEER_PUBLISH_TARGETS")
        context = owner.catalog.context(context_root); allowance.check()
        report["local_context"] = context_root
        prepared, seen, total = [], set(), 0
        for target in targets:
            allowance.check()
            _fields(target, ("name", "export_id", "unit_id"), "PEER_TARGET_FIELDS")
            key = A.E.name_key(target["name"])
            uid, eid = F.hexid(target["unit_id"]), F.hexid(target["export_id"])
            A.need(key not in seen, "PEER_DUPLICATE_TARGET")
            seen.add(key)
            A.need(context["bindings"].get(key) == eid and
                   A.S.export_id(loaded.installation.semantic_id, uid, target["name"]) == eid,
                   "PEER_LOCAL_TARGET_BINDING")
            remaining = config["max_total_bytes"]-total
            A.need(remaining > 0, "PEER_PUBLISH_TOTAL_BYTES")
            raw = custody.get_evidence(loaded.installation.semantic_id, uid,
                min(config["max_unit_bytes"], remaining), check_budget=allowance.check)
            total += len(raw)
            preview = PP.preview_from_evidence(raw, target["name"])
            PP.resolve(preview, raw)
            A.need(PP.read_preview(preview).export_id == eid, "PEER_PUBLISH_PREVIEW_BINDING")
            prepared.append((eid, preview))
        allowance.check()
        index = _index(loaded, owner, custody, config["index"], allowance.check)
        allowance.check()
        for eid, preview in prepared:
            allowance.check()
            custody.put_preview(preview, before_commit=allowance.check)
            # admit is a bounded synchronous metadata operation, not a new grant.
            result = index.admit(preview, expected_id=eid)
            report["publications"].append(result)
            allowance.check()
        report.update(status="INDEXED_LOCAL_TARGETS", evidence_bytes_read=total)
    except BaseException as caught:
        error = caught
    finally:
        if index is not None:
            try: index.close()
            except BaseException as caught:
                report["cleanup_errors"].append(_error(caught)); error = error or caught
    try: allowance.check()
    except BaseException as caught: error = error or caught
    if error is not None:
        raise _failure(report, error) from error
    return report


async def serve(loaded, custody, config, allowance, *, ready=None):
    """Finite, exclusive read-only serving of the ENTIRE selected custody store.

    No per-object ACL is implied. Caller must exclude concurrent users/writers
    for both stores and run an outer Job if hard controller limits are required.
    The shipped CLI holds the associated OrdinaryAdmission owner lock throughout
    serving/cleanup. API-only inert rehosting must supply its own serialization.
    Caller closes custody even on PeerFailure; this function attempts all owned
    provider/index cleanup. Readiness means listening, never math acceptance.
    """
    config, report = _begin(loaded, config, allowance, "serve")
    report.update(provider=None, ready=None, quiescent=False)
    index = provider = None
    lease_timer = None
    error = None
    cleanup_until = allowance.deadline
    try:
        _fields(config, ("index", "host", "port", "tls", "lease_seconds", "cleanup_seconds",
                        "limits", "share_all_custody", "exclusive"), "PEER_SERVE_FIELDS")
        _state(loaded, None, custody)
        A.need(config["share_all_custody"] is True and config["exclusive"] is True,
               "PEER_EXPLICIT_FULL_CUSTODY_EXCLUSIVE_SCOPE")
        A.need(ready is None or callable(ready), "PEER_READY_CALLBACK")
        F.uint(config["lease_seconds"], 1, 3600, "PEER_SERVICE_LEASE")
        F.uint(config["cleanup_seconds"], 10, 60, "PEER_SERVICE_CLEANUP_RESERVE")
        F.uint(config["port"], 0, 65535, "PEER_SERVICE_PORT")
        A.need(type(config["host"]) is str and len(config["host"]) <= 64, "PEER_SERVICE_HOST")
        address = ipaddress.ip_address(config["host"])
        A.need(not address.is_unspecified and not address.is_multicast, "PEER_SERVICE_ADDRESS")
        limits = _limits(config["limits"], PROVIDER_LIMITS, "PEER_PROVIDER_LIMITS")
        _fields(config["index"], ("path", "limits", "create"), "PEER_INDEX_FIELDS")
        A.need(config["index"]["create"] is False, "PEER_SERVICE_EXISTING_INDEX")
        tls, pins = None, []
        if config["tls"] is not None:
            selected = config["tls"]
            _fields(selected, ("cert_file", "cert_sha256", "key_file", "key_sha256"), "PEER_SERVER_TLS_FIELDS")
            pins = [_pin(selected["cert_file"], selected["cert_sha256"], allowance.check),
                    _pin(selected["key_file"], selected["key_sha256"], allowance.check)]
            tls = H.server_tls(str(pins[0][0]), str(pins[1][0]))
            _repin(pins, allowance.check)
        A.need(address.is_loopback or tls is not None, "PEER_REMOTE_TLS_REQUIRED")
        index = _index(loaded, None, custody, config["index"], allowance.check)
        allowance.check()
        lease_until = time.monotonic()+config["lease_seconds"]
        A.need(lease_until+config["cleanup_seconds"] < allowance.deadline, "PEER_LEASE_ORIGINAL_ALLOWANCE")
        cleanup_until = min(allowance.deadline, lease_until+config["cleanup_seconds"])
        provider = H.Provider(index=index, ordinary=custody, **limits)
        lease_timer = asyncio.timeout_at(lease_until)
        async with lease_timer:
            endpoint = await provider.start(config["host"], config["port"], tls_context=tls)
            allowance.check()
            report["ready"] = {"status": "READY", "host": endpoint.host, "port": endpoint.port,
                "tls": endpoint.tls, "lease_seconds": config["lease_seconds"],
                "shared_custody": str(custody.root), "index": str(index.root),
                "mathematical_acceptance": False, "controller_limits": CONTROLLER_LIMITS}
            if ready is not None: ready(deepcopy(report["ready"]))
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
                report["quiescent"] = provider.server is None and not provider.tasks and provider.reserved_reply_bytes == 0
                A.need(report["quiescent"], "PEER_SERVICE_CLEANUP_UNCERTAIN")
            except BaseException as caught:
                report["cleanup_errors"].append(_error(caught)); error = error or caught
                # stop() may fail before reaching task cancellation. Still
                # attempt every cleanup phase within the SAME original reserve.
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
            try: index.close()
            except BaseException as caught:
                report["cleanup_errors"].append(_error(caught)); error = error or caught
    try: allowance.check()
    except BaseException as caught: error = error or caught
    if error is not None:
        raise _failure(report, error) from error
    return report

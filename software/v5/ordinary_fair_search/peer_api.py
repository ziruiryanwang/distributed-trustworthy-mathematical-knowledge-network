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
import json
import math
from pathlib import Path
import re
import ssl
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
from transport import authoring_offers as AO
from discovery.fair_search import FairSearch

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


def _provider_error(error):
    """Exact remote-failure allowlist, not a generic malformed-input recovery."""
    if type(error) in (ConnectionRefusedError, ConnectionResetError,
            ConnectionAbortedError, BrokenPipeError, TimeoutError,
            asyncio.IncompleteReadError, asyncio.LimitOverrunError,
            ssl.SSLCertVerificationError, json.JSONDecodeError, UnicodeDecodeError):
        return True
    return type(error) is ValueError and str(error) in {
        "REMOTE_HTTP_ERROR_CONSERVATIVELY_CHARGED",
        "HTTP_HEADER_BYTES", "HTTP_HEADER_LINES", "HTTP_HEADER_SHAPE", "HTTP_HEADER_NAME",
        "HTTP_HEADER_DUPLICATE_OR_CONTROL", "HTTP_UNSUPPORTED_HEADER", "HTTP_CONTENT_LENGTH",
        "HTTP_MESSAGE_PROFILE", "HTTP_STATUS", "HTTP_RESPONSE_BOUND", "HTTP_TRAILING_RESPONSE",
        "JSON_BYTE_LIMIT", "JSON_DEPTH_LIMIT", "JSON_DUPLICATE_KEY", "JSON_NONINTEGER",
        "NONCANONICAL_JSON", "SESSION_OFFER_QUERY_BINDING", "SESSION_OFFER_ASSURANCE",
        "SESSION_OFFER_STATUS", "SESSION_OFFER_NO_SUMMARY", "SESSION_OFFER_SUMMARY",
        "SESSION_OFFER_EXPIRED", "CANDIDATE_PAGE_SCHEMA", "CANDIDATE_ASSURANCE",
        "CANDIDATE_CURSOR_BINDING"}


async def find(loaded, config, allowance, *, network_budget=None):
    """Unknown-ID positive search. Results remain incomplete inert metadata.

    Composed callers supply one OrdinaryBudget created before find; the entire
    search suballocation is prepaid before any I/O and never refunded. Separate
    CLI calls are separate explicit owner grants, not automatic continuation.
    Offers and candidate pages use serial fair rounds with a five-second attempt
    ceiling, further divided from the original residual session time. Recoverable
    refusals require settled transport cleanup. No retry or new grant is created;
    local synchronous work and inadequate aggregate grants still limit progress.
    """
    config, report = _begin(loaded, config, allowance, "find")
    report.update(matches=[], offers=[], provider_errors=[], termination=None, global_complete=False,
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
        client = FairSearch(SearchSession(adapter.namespace, features, limits), endpoints)
        report["namespace"], report["features"] = adapter.namespace, features
        def live():
            allowance.check(); ledger.active(); _repin(pins, allowance.check)
        async with asyncio.timeout_at(ledger.deadline):
            report.update(await client.run(providers, offer, page,
                attempt_timeout_ms=5000, check_owner=live,
                recover_metadata_failure=_provider_error))
    except BaseException as caught:
        if isinstance(caught, ValueError) and str(caught).startswith("SESSION_BUDGET:"):
            report.update(status="INCOMPLETE_SEARCH", termination=str(caught))
        else:
            error = caught
    finally:
        if client is not None:
            partial = client.result()
            for key in ("matches", "offers", "provider_errors"):
                report[key] = partial[key]
            if report["termination"] is None:
                report["termination"] = partial["termination"]
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
    """Acquire a target under an explicit dependency policy, then admit if ready.

    Snapshot/record data selects bytes, not a warrant. No proof/native artifact
    supplied by a peer enters the local acceptance context without owner.admit.
    selected-unit-only refuses missing premises before requesting ancestors;
    bounded-closure explicitly permits the existing finite recursive acquisition.
    Nonacceptance still completes accounting, cleanup and the final budget check.
    """
    config, report = _begin(loaded, config, allowance, "receive")
    report.update(admission=None, acquisition=None, frontier=[], unit_ids=[], network=None,
                  dependency_policy=None, target=None, local_acceptance_available=False)
    operation = ledger = client = None
    own_ledger = False
    error = None
    try:
        _fields(config, ("contacts", "selection", "parent_root", "limits", "dependency_policy"),
                "PEER_RECEIVE_FIELDS")
        policy = config["dependency_policy"]
        A.need(type(policy) is str and policy in ("selected-unit-only", "bounded-closure"),
               "PEER_RECEIVE_DEPENDENCY_POLICY")
        report["dependency_policy"] = policy
        _state(loaded, owner, custody)
        parent = F.hexid(config["parent_root"])
        report["parent_root"] = parent
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
            report["target"] = {"name": locator["export_name"], "unit_id": locator["unit_id"],
                                "export_id": record["object_id"]}
            retain(selected["raw"], locator["unit_id"])
            plan = None
            needs_grounded = False
            for _ in range(limits["preflights"]):
                live()
                plan = owner.preflight(parent, list(units.values()), limits=preflight_limits, budget=operation)
                live()
                A.need(len(plan.missing) <= limits["missing"], "PEER_MISSING_FRONTIER_BOUND")
                report["frontier"].append({"status": plan.status, "missing_count": len(plan.missing),
                                            "units": len(units)})
                if plan.status == "READY":
                    break
                if policy == "selected-unit-only":
                    A.need(plan.status == "NEEDS" and bool(plan.missing), "PEER_PREFLIGHT_STATUS")
                    needs_grounded = True
                    report.update(status="NEED_GROUNDED_PREMISES",
                        acceptance_facet="NO_LOCAL_ACCEPTANCE_MISSING_PREMISES",
                        grounded_premises_needed=[
                            {"name": A.E.strict_json(name_raw), "export_id": identity}
                            for name_raw, identity in plan.missing])
                    break  # No ancestor locator/evidence request and no admission.
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
            if not needs_grounded:
                A.need(plan is not None and plan.status == "READY", "PEER_PREFLIGHT_CAP")
        live()
        if not needs_grounded:
            accepted = owner.admit(parent, plan, operation)
            # Set this before any checking/reporting/cleanup that could subsequently fail.
            report["admission"] = accepted
            A.need(accepted["status"] in ("CHECKED", "REUSED"), "PEER_ADMISSION_STATUS")
            report["mathematical_acceptance"] = accepted["status"] == "CHECKED"
            report["acceptance_facet"] = "NEW_LOCAL_NATIVE_ACCEPTANCE" if accepted["status"] == "CHECKED" else "EXISTING_LOCAL_ACCEPTANCE_NO_NEW_CHECK"
            report["local_acceptance_available"] = True
            report["status"] = "CHECKED" if accepted["status"] == "CHECKED" else "REUSED_LOCAL_ACCEPTANCE"
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
        serve_fields = ("index", "host", "port", "tls", "lease_seconds", "cleanup_seconds",
                        "limits", "share_all_custody", "exclusive")
        _fields(config, (*serve_fields, "authoring_offers") if "authoring_offers" in config
                else serve_fields, "PEER_SERVE_FIELDS")
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
        authoring_map = None
        offer_selection = config.get("authoring_offers")
        if offer_selection is not None:
            _fields(offer_selection, ("path", "sha256"), "PEER_AUTHORING_MAP_FIELDS")
            A.need(type(offer_selection["path"]) is str, "PEER_AUTHORING_MAP_PATH")
            expected = F.hexid(offer_selection["sha256"])
            selected_path = A.C.ordinary(Path(offer_selection["path"]))
            allowance.check()
            raw_map = A.C.read_bounded(selected_path, AO.MAP_MAX)
            A.need(hashlib.sha256(raw_map).hexdigest() == expected, "PEER_AUTHORING_MAP_PIN")
            # Serve the selected immutable in-memory snapshot, not a live file.
            authoring_map = AO.OfferMap.from_bytes(raw_map, check_budget=allowance.check)
            report["authoring_map_sha256"] = expected
            allowance.check()
        index = _index(loaded, None, custody, config["index"], allowance.check)
        allowance.check()
        lease_until = time.monotonic()+config["lease_seconds"]
        A.need(lease_until+config["cleanup_seconds"] < allowance.deadline, "PEER_LEASE_ORIGINAL_ALLOWANCE")
        cleanup_until = min(allowance.deadline, lease_until+config["cleanup_seconds"])
        provider = H.Provider(index=index, ordinary=custody, authoring_offers=authoring_map, **limits)
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


async def authoring_offers(loaded, config, allowance, *, network_budget=None):
    """One bounded lookup of project hints, without following or approving them."""
    config, report = _begin(loaded, config, allowance, "authoring-offers")
    report.update(selection=None, reply=None, reply_sha256=None, reply_bytes=None,
                  acquisition=None, network=None, source_availability_verified=False,
                  project_correspondence_verified=False, execution_approved=False)
    ledger = client = None
    own_ledger = False
    error = None
    try:
        _fields(config, ("contacts", "selection", "limits"), "PEER_AUTHORING_OFFERS_FIELDS")
        endpoints, pins = _contacts(config["contacts"], allowance.check)
        limits = _limits(config["limits"], {"requests": (1, 1),
            "reply_bytes": (1, AO.REPLY_MAX), "max_offers": (1, AO.MAX_OFFERS)},
            "PEER_AUTHORING_OFFERS_LIMITS")
        selection = config["selection"]
        _fields(selection, ("provider", "export_id"), "PEER_AUTHORING_OFFERS_SELECTION")
        provider = selection["provider"]
        A.need(type(provider) is str and provider in endpoints, "PEER_SELECTED_CONTACT")
        eid = F.hexid(selection["export_id"])
        adapter = OrdinaryExportAdapter(loaded.installation.semantic_id)
        request = {"schema": AO.REQUEST_SCHEMA, "semantic_id": adapter.semantic_id,
                   "export_id": eid, "max_bytes": limits["reply_bytes"],
                   "max_offers": limits["max_offers"]}
        AO.request_limit(request)
        report["selection"] = deepcopy(selection)
        ledger, own_ledger = _network(allowance, 1, limits["reply_bytes"],
            network_budget, allowance.deadline-3)

        def live():
            allowance.check(); ledger.active(); _repin(pins, allowance.check)

        client = O.OrdinaryAcquisition(adapter, endpoints, ledger, local_custody=None)
        async with asyncio.timeout_at(ledger.deadline):
            live()
            fetched = await client.authoring_offers(provider, adapter.semantic_id, eid,
                limits["reply_bytes"], max_offers=limits["max_offers"])
            live()
        raw = fetched["raw"]
        reply = AO.read_reply(raw, request)
        report.update(status="UNVERIFIED_AUTHORING_ASSOCIATIONS", reply=deepcopy(reply),
            reply_sha256=hashlib.sha256(raw).hexdigest(), reply_bytes=len(raw),
            assurance="PROJECT_HINTS_ONLY_NOT_SOURCE_OR_EXECUTION_OR_MATHEMATICAL_AUTHORITY")
        live()
    except BaseException as caught:
        error = caught
    finally:
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


async def inspect(loaded, config, allowance, *, network_budget=None):
    """Read ONE named concept's exact inert unit, without ancestry or admission.

    The selection may come from a preview's type_bindings. The locator binds
    its name/ExportID to a UnitID; evidence then binds that exact unit and its
    output census. The entire declaration group is returned as parsed inert
    data, not executable Lean code or warranted laws. Dependencies remain
    unchecked. No owner/custody is opened and no automatic traversal occurs.

    Exactly two sequential reads share one nonrenewing ledger. Composed callers
    supply their existing ledger; exhaustion refuses before any I/O. Each failed
    begun attempt retains its full reservation. HTTP exchange owns connection
    cleanup; the original allowance retains the same three-second reserve used
    by preview. Hard containment still requires an external process envelope.
    """
    config, report = _begin(loaded, config, allowance, "inspect")
    report.update(selection=None, semantic_id=loaded.installation.semantic_id,
                  locator=None, locator_sha256=None, locator_bytes=None,
                  evidence=None, evidence_sha256=None, evidence_bytes=None,
                  unit_id=None, acquisition=None, network=None,
                  dependencies_checked=False, native_usable=False)
    ledger = client = None
    own_ledger = False
    error = None
    try:
        _fields(config, ("contacts", "selection", "limits"), "PEER_INSPECT_FIELDS")
        endpoints, pins = _contacts(config["contacts"], allowance.check)
        limits = _limits(config["limits"], {
            "requests": (2, 2), "reply_bytes": (1, O.LOCATOR_MAX+O.EVIDENCE_MAX),
            "locator_bytes": (1, O.LOCATOR_MAX), "unit_bytes": (1, O.EVIDENCE_MAX)},
            "PEER_INSPECT_LIMITS")
        maximum = limits["locator_bytes"]+limits["unit_bytes"]
        A.need(maximum <= limits["reply_bytes"], "PEER_INSPECT_REPLY_CAP")
        selection = config["selection"]
        _fields(selection, ("provider", "name", "export_id"), "PEER_INSPECT_SELECTION_FIELDS")
        provider = selection["provider"]
        A.need(type(provider) is str and provider in endpoints, "PEER_SELECTED_CONTACT")
        export_id = F.hexid(selection["export_id"])
        A.E.name_key(selection["name"])  # Validate encoded Lean name before I/O.
        adapter = OrdinaryExportAdapter(loaded.installation.semantic_id)
        report["selection"] = deepcopy(selection)
        ledger, own_ledger = _network(allowance, limits["requests"],
            limits["reply_bytes"], network_budget, allowance.deadline-3)
        A.need(ledger.requests+2 <= ledger.request_cap and
               ledger.reply_bytes+maximum <= ledger.byte_cap,
               "PEER_INSPECT_REMAINING_BUDGET")

        def live():
            allowance.check()
            ledger.active()
            _repin(pins, allowance.check)

        client = O.OrdinaryAcquisition(adapter, endpoints, ledger, local_custody=None)
        async with asyncio.timeout_at(ledger.deadline):
            live()
            located = await client.locator(provider, adapter.semantic_id, export_id,
                limits["locator_bytes"], expected_name=selection["name"])
            live()
            locator = located["locator"]
            report.update(locator=deepcopy(locator),
                locator_sha256=hashlib.sha256(located["raw"]).hexdigest(),
                locator_bytes=len(located["raw"]))
            fetched = await client.evidence(provider, adapter.semantic_id,
                locator["unit_id"], limits["unit_bytes"], expected_export_id=export_id,
                expected_export_name=selection["name"])
            live()
        raw = fetched["raw"]
        # Reparse exact acquired bytes for JSON output; never serialize raw
        # Python bytes or turn a helper's mutable result into an authority token.
        parsed = A.PE.read_evidence(raw)
        report.update(status="INSPECTION_BOUND_NOT_ACCEPTED",
            evidence=deepcopy(parsed.document), unit_id=parsed.unit_id,
            evidence_sha256=hashlib.sha256(raw).hexdigest(), evidence_bytes=len(raw),
            assurance="EXACT_INERT_UNIT_AND_EXPORT_BOUND_NOT_DEPENDENCY_OR_MATHEMATICAL_ACCEPTANCE")
        live()
    except BaseException as caught:
        error = caught
    finally:
        if ledger is not None:
            if own_ledger:
                try:
                    ledger.close()
                except BaseException as caught:
                    report["cleanup_errors"].append(_error(caught))
                    error = error or caught
            report["network"] = ledger.report()
        if client is not None:
            report["acquisition"] = client.report()
    try:
        allowance.check()
    except BaseException as caught:
        error = error or caught
    if error is not None:
        raise _failure(report, error) from error
    return report


async def preview(loaded, config, allowance, *, network_budget=None):
    """Inspect ONE exact advertised type without opening owner/custody state.

    This reuses the ordinary preview fetch/record rederivation, not evidence
    acquisition or mathematical admission. Snapshot identity is retained only:
    this operation does not reverify a search membership proof. Caller-selected
    data stays inert, including names and the complete returned type DAG.

    A standalone call owns a one-request ledger. A composed caller supplies its
    existing ledger; only one additional fetch is allowed and the deadline can
    only narrow. No retry/referral, source execution, locator or evidence call.
    A later explicit receive still fetches its own preview and charges that cost.
    """
    config, report = _begin(loaded, config, allowance, "preview")
    report.update(selection=None, preview=None, preview_sha256=None,
                  preview_bytes=None, namespace=None, acquisition=None,
                  network=None, evidence_bound=False,
                  snapshot_membership_reverified=False)
    ledger = client = None
    own_ledger = False
    error = None
    try:
        _fields(config, ("contacts", "selection", "limits"), "PEER_PREVIEW_FIELDS")
        endpoints, pins = _contacts(config["contacts"], allowance.check)
        limits = _limits(config["limits"], {
            "requests": (1, 1), "reply_bytes": (1, O.PREVIEW_MAX)},
            "PEER_PREVIEW_LIMITS")
        selection = config["selection"]
        _fields(selection, ("provider", "snapshot_id", "record"),
                "PEER_SELECTION_FIELDS")
        provider = selection["provider"]
        A.need(type(provider) is str and provider in endpoints,
               "PEER_SELECTED_CONTACT")
        F.hexid(selection["snapshot_id"])  # Retained label, not membership proof.
        adapter = OrdinaryExportAdapter(loaded.installation.semantic_id)
        record = F.validate_record(selection["record"], adapter.namespace)
        A.need(record["schema"] == F.ORDINARY_EXPORT_RECORD_SCHEMA,
               "PEER_ORDINARY_RECORD")
        A.need(record["object_bytes"] <= limits["reply_bytes"],
               "PEER_PREVIEW_REPLY_CAP")
        report["selection"] = deepcopy(selection)
        report["namespace"] = adapter.namespace
        ledger, own_ledger = _network(allowance, limits["requests"],
            limits["reply_bytes"], network_budget, allowance.deadline-3)

        def live():
            allowance.check()
            ledger.active()
            _repin(pins, allowance.check)

        # No OrdinaryStore/owner is constructed: the preview remains in this
        # bounded report, not in trusted state or automatic local custody.
        client = O.OrdinaryAcquisition(adapter, endpoints, ledger,
                                       local_custody=None)
        async with asyncio.timeout_at(ledger.deadline):
            live()
            fetched = await client.preview(provider, record)
            live()
        raw = fetched["raw"]
        # The fetch already checked exact bytes and recomputed the entire
        # advertised record. Reparse raw bytes at this output boundary; a mutable
        # helper result/header is not an authority token.
        parsed = PP.read_preview(raw, adapter.limits)
        report.update(
            status="PREVIEW_BOUND_NOT_ACCEPTED",
            preview=deepcopy(parsed.document),
            preview_sha256=hashlib.sha256(raw).hexdigest(),
            preview_bytes=len(raw),
            assurance="EXACT_PREVIEW_RECORD_BOUND_NOT_EVIDENCE_OR_MATHEMATICAL_ACCEPTANCE")
        live()
    except BaseException as caught:
        error = caught
    finally:
        if ledger is not None:
            if own_ledger:
                try:
                    ledger.close()
                except BaseException as caught:
                    report["cleanup_errors"].append(_error(caught))
                    error = error or caught
            report["network"] = ledger.report()
        if client is not None:
            report["acquisition"] = client.report()
    try:
        allowance.check()
    except BaseException as caught:
        error = error or caught
    if error is not None:
        raise _failure(report, error) from error
    return report

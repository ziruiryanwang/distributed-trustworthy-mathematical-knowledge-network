"""Focused native-free multi-source controls; source only until root selects a run.

Real portable codecs, inert custody, acquisition and budget; explicit admission
and unused search doubles. The retained false theorem is NEVER Lean-checked.
"""
from __future__ import annotations

import argparse
import asyncio
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import ssl
import sys
import time
from types import ModuleType, SimpleNamespace as NS
from unittest.mock import patch

START, CPU = time.monotonic(), time.process_time()
MIB = 1024**2
REQUEST_SHA = "6f2f5aa5849fabbd88c141a05735ae44ac1b6b49dcee790cad9d11b86d494801"
MANIFEST_SHA = "799bb3c86af8b0af8aa11c1f38cac4d1c6ec8d642858122ab3c92683864f6416"
STORE_LIMITS = dict(objects=32, exports=64, logical_bytes=MIB, db_pages=256)
POLICY = dict(acquisition_sources=["A", "B"], attempt_timeout_ms=3000,
              finalization_reserve_ms=2000)


def need(ok, code):
    if not ok:
        raise AssertionError("MULTI_SOURCE_TEST_" + code)


def check():
    need(time.monotonic()-START < 90 and time.process_time()-CPU < 30, "ORIGINAL_ALLOWANCE")


def forbidden(*args, **kwargs):
    raise AssertionError("MULTI_SOURCE_TEST_UNSELECTED_EXECUTION")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, maximum=2*MIB, expected=None):
    check()
    need(path.is_file() and 0 < path.stat().st_size <= maximum, "INPUT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) <= maximum and (expected is None or sha(raw) == expected), "INPUT_PIN")
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
    need(len(raw) <= 2*MIB, "REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def load(name, path, *, replace=False):
    need(replace or name not in sys.modules, "PRELOADED_MODULE")
    raw = read(path)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    if "." in name:
        parent, child = name.rsplit(".", 1)
        setattr(sys.modules[parent], child, module)
    return module


def refusal(action, kind, text=None):
    try:
        action()
    except BaseException as error:
        need(isinstance(error, kind) and (text is None or text in str(error)),
             "UNEXPECTED_REFUSAL:" + type(error).__name__ + ":" + str(error))
        return error
    raise AssertionError("MULTI_SOURCE_TEST_REFUSAL_MISSING")


async def async_refusal(action, kind, text=None):
    try:
        await action()
    except BaseException as error:
        need(isinstance(error, kind) and (text is None or text in str(error)),
             "UNEXPECTED_ASYNC_REFUSAL:" + type(error).__name__ + ":" + str(error))
        return error
    raise AssertionError("MULTI_SOURCE_TEST_ASYNC_REFUSAL_MISSING")


def support(here, source_root):
    loader = load("_multi_source_pure_loader", here.parent/"ordinary_inert_mirror02/run.py")
    with ExitStack() as guards:
        for name in ("subprocess.Popen", "os.system", "socket.socket", "socket.create_connection"):
            guards.enter_context(patch(name, forbidden))
        s = loader.load_support(source_root, check)
        # Replace the only changed transport payloads after fixed pure selection.
        s.H = load("transport.http_provider", here/"http_provider.py", replace=True)
        s.O = load("transport.ordinary_acquisition", here/"ordinary_acquisition.py", replace=True)
        # No production admission module is imported. These type identities are
        # explicit control doubles, not a bypass within production software.
        A = ModuleType("ordinary_admission")
        A.need, A.E, A.PE = s.F.need, s.E, s.PE
        A.NativeInstallation = type("AuthorityDoubleInstallation", (), {})
        A.OrdinaryAdmission = type("AuthorityDoubleAdmission", (), {})
        A.PreflightLimits = NS
        sys.modules[A.__name__] = A
        for name, attributes in {
            "discovery.search_session": dict(SearchSession=forbidden, LIMITS={}),
            "transport.fair_exchange": {},
            "discovery.fair_search": dict(FairSearch=forbidden),
        }.items():
            need(name not in sys.modules, "UNEXPECTED_SEARCH_IMPORT")
            stub = ModuleType(name)
            stub.__dict__.update(attributes)
            sys.modules[name] = stub
            parent, child = name.rsplit(".", 1)
            setattr(sys.modules[parent], child, stub)
        api = load("_multi_source_peer", here/"peer_api.py")
    need(api.H is s.H and api.O is s.O and s.O.H is s.H and api.A is A,
         "SELECTED_MODULE_IDENTITIES")
    need(not any(name in sys.modules for name in
        ("portable_admission", "baseline_intake", "profile", "ordinary_contribution")), "NO_NATIVE_IMPORT")
    s.A, s.api = A, api
    return s


def fixture(s, root):
    request = json.loads(read(root/"prepare-request.json", expected=REQUEST_SHA))
    bundle = root/"bundle"
    manifest = s.B.read_manifest(read(bundle/"manifest.json", expected=MANIFEST_SHA),
                                 MANIFEST_SHA, check_budget=check)
    need(manifest.unit_count == 4 and manifest.evidence_bytes == 5149, "RETAINED_FIXTURE_SCOPE")
    units, exports, inputs = {}, {}, []
    for batch in manifest.batches:
        for entry in batch:
            path = bundle/entry.relative_path
            raw = read(path, entry.raw_bytes, entry.raw_sha256)
            need(len(raw) == entry.raw_bytes, "EXACT_FIXTURE_LENGTH")
            units[entry.unit_id] = raw
            parsed = s.PE.read_evidence(raw)
            need(parsed.unit_id == entry.unit_id, "EXACT_FIXTURE_UNIT")
            for row in parsed.document["unit"][2]:
                eid = s.S.export_id(s.S.semantic_id(), entry.unit_id, row[0])
                exports[eid] = dict(name=row[0], export_id=eid, unit_id=entry.unit_id)
            inputs.append((path, entry.raw_bytes, entry.raw_sha256))
    target = request["targets"][0]
    need(exports[target["export_id"]] == target, "RETAINED_TARGET")
    preview = s.PP.preview_from_evidence(units[target["unit_id"]], target["name"])
    adapter = s.OA.OrdinaryExportAdapter(s.S.semantic_id())
    record = adapter.extract(preview, target["export_id"])
    # Follow only the retained fixture's exact imports to identify its two
    # metadata dependencies. This does not establish proof validity.
    def local_imports(uid):
        return [exports[eid] for _, eid in s.PE.read_evidence(units[uid]).document["imports"]
                if eid in exports]
    second, = local_imports(target["unit_id"])
    first, = local_imports(second["unit_id"])
    need(local_imports(first["unit_id"]) == [], "EXACT_RETAINED_THREE_UNIT_CHAIN")
    return NS(root=root, units=units, exports=exports, target=target, second=second,
              first=first, preview=preview, record=record, adapter=adapter, inputs=inputs)


def endpoints(s):
    return {label: s.H.Endpoint("127.0.0.1", 41000+i)
            for i, label in enumerate(("origin", "A", "B"))}


def response(s, raw, request, status=200):
    return dict(status=status, raw=raw, request_bytes=len(s.F.compact(request)),
                reply_bytes=len(raw), header_bytes=128, elapsed_ms=0)


class FixtureTransport:
    """Explicit transport double; selected source/route bytes remain real."""
    def __init__(self, s, f, mode):
        self.s, self.f, self.mode, self.calls = s, f, mode, []
        self.labels = {ep.port: label for label, ep in endpoints(s).items()}

    async def __call__(self, endpoint, route, request, cap, timeout, **kwargs):
        check()
        s, f = self.s, self.f
        label = self.labels[endpoint.port]
        self.calls.append(dict(provider=label, route=route, request=deepcopy(request), cap=cap,
                               timeout_ms=timeout, kwargs=kwargs))
        need(s.O.request_limit(route, request) == cap and 0 < timeout <= 60000, "EXCHANGE_REQUEST_BOUND")
        if self.mode == "default":
            need(label == "origin" and kwargs == {}, "DEFAULT_EXCHANGE_COMPATIBILITY")
        else:
            need(label in ("A", "B") and kwargs == {"classify_unavailable": True}
                 and timeout <= POLICY["attempt_timeout_ms"], "EXPLICIT_SOURCE_ONLY")
        if route == s.O.PREVIEW_ROUTE:
            raw, holder = f.preview, "B"
        elif route == s.O.LOCATOR_ROUTE:
            target = f.exports[request["export_id"]]
            raw = s.F.compact(dict(schema=s.PP.LOCATOR_SCHEMA, semantic_id=s.S.semantic_id(),
                                  unit_id=target["unit_id"], export_name=target["name"]))
            holder = "A" if target == f.second else "B"
        else:
            need(route == s.O.EVIDENCE_ROUTE, "ONLY_SELECTED_ACQUISITION_ROUTES")
            raw = f.units[request["unit_id"]]
            holder = "A" if request["unit_id"] == f.second["unit_id"] else "B"
        if self.mode == "no-preview" and route == s.O.PREVIEW_ROUTE:
            return response(s, b"", request, 404)
        if self.mode != "default" and label != holder:
            return response(s, b"", request, 503 if route == s.O.EVIDENCE_ROUTE else 404)
        return response(s, raw, request)


def authority(s, f, custody, *, grounded=False):
    """Metadata-only preflight and REUSED admission double, NEVER Lean checking."""
    installation = s.A.NativeInstallation()
    installation.semantic_id = s.S.semantic_id()
    loaded = NS(A=s.A, O=s.O, installation=installation)
    owner = s.A.OrdinaryAdmission()
    owner.installation, owner.evidence_store = installation, custody
    owner.calls, owner.plans = [], []
    parent = "1"*64
    def context(identity):
        need(identity == parent, "ORIGINAL_PARENT")
        owner.calls.append("context")
    owner.catalog = NS(context=context)
    def preflight(identity, raws, *, limits, budget):
        need(identity == parent and len(raws) <= limits.max_units and
             sum(map(len, raws)) <= limits.max_bytes, "DOUBLE_PREFLIGHT_INPUT")
        budget.check()
        parsed = [s.PE.read_evidence(raw) for raw in raws]
        have = {s.S.export_id(s.S.semantic_id(), p.unit_id, row[0])
                for p in parsed for row in p.document["unit"][2]}
        missing = sorted({(s.E.name_key(name), eid) for p in parsed
                          for name, eid in p.document["imports"]
                          if eid in f.exports and eid not in have}) if not grounded else []
        plan = NS(status="NEEDS" if missing else "READY", missing=tuple(missing))
        owner.plans.append(plan)
        owner.calls.append("preflight:"+plan.status)
        return plan
    def admit(identity, plan, budget):
        need(identity == parent and plan is owner.plans[-1] and plan.status == "READY", "ADMIT_ONLY_READY")
        budget.check(); owner.calls.append("admit-double")
        return dict(status="REUSED", authority="EXPLICIT_TEST_DOUBLE_NOT_LOCAL_ACCEPTANCE")
    owner.preflight, owner.admit = preflight, admit
    return loaded, owner, parent


class Allowance:
    def __init__(self):
        self.deadline, self.accounts, self.operations = min(START+85, time.monotonic()+30), [], []
    def check(self):
        check(); need(time.monotonic() < self.deadline, "ALLOWANCE_DEADLINE")
    def operation(self, selected):
        self.check()
        op = NS(deadline=self.deadline-3, worker_cpu=0)
        op.check = lambda: (self.check(), need(time.monotonic() < op.deadline, "OPERATION_DEADLINE"))
        self.operations.append(op)
        return op
    def account(self, value):
        need(value == 0, "NO_NATIVE_CPU")
        self.accounts.append(value)


def config(s, f, parent, *, opt=True, policy="bounded-closure", requests=32, reply_bytes=MIB):
    contacts = {label: dict(host=ep.host, port=ep.port, tls=False, server_name=None,
                           ca_file=None, ca_sha256=None) for label, ep in endpoints(s).items()}
    value = dict(contacts=contacts, selection=dict(provider="origin", snapshot_id="2"*64,
        record=deepcopy(f.record)), parent_root=parent, dependency_policy=policy,
        limits=dict(requests=requests, reply_bytes=reply_bytes, units=4, unit_bytes=4096,
                    total_bytes=16384, missing=4, preflights=4, locator_bytes=1024))
    if opt:
        value.update(deepcopy(POLICY))
    return value


async def receive_case(s, f, output, name, *, mode="disjoint", opt=True,
                       policy="bounded-closure", grounded=False, expect=None):
    store = s.O.OrdinaryStore(output/name, s.S.semantic_id(), STORE_LIMITS, create=True)
    loaded, owner, parent = authority(s, f, store, grounded=grounded)
    allowance = Allowance()
    ledger = s.O.OrdinaryBudget(deadline=allowance.deadline-3, requests=32, reply_bytes=MIB)
    ledger.charge_external("retained-discovery-test-double", 1, 64)
    original_deadline = ledger.deadline
    transport = FixtureTransport(s, f, mode)
    cfg = config(s, f, parent, opt=opt, policy=policy)
    original_config = deepcopy(cfg)
    try:
        with patch.object(s.H, "exchange", transport):
            if expect is None:
                report = await s.api.receive(loaded, owner, store, cfg, allowance, network_budget=ledger)
            else:
                error = await async_refusal(lambda: s.api.receive(loaded, owner, store, cfg, allowance,
                    network_budget=ledger), s.api.PeerFailure, expect)
                report = error.report
        need(cfg == original_config and ledger.deadline <= original_deadline and not ledger.closed
             and ledger.pending is None and allowance.accounts == [0]
             and len(allowance.operations) == 1, "ORIGINAL_STATE_GRANT_AND_ACCOUNTING")
        need(ledger.requests == len(transport.calls)+1 and ledger.external ==
             [dict(label="retained-discovery-test-double", requests=1, reply_bytes=64)], "SHARED_LEDGER")
        need(report["mathematical_acceptance"] is False, "NO_TEST_MATHEMATICAL_CLAIM")
        value = dict(report=report, calls=transport.calls, owner_calls=owner.calls,
                     actual_native_calls=0, authority="EXPLICIT_METADATA_AND_ADMISSION_DOUBLES")
        save(output/(name+".json"), value)
        return value
    finally:
        store.close()
        if ledger.pending is None:
            ledger.close()


def policy_controls(s):
    api, eps = s.api, endpoints(s)
    need(api._receive_source_policy({}, eps) is None, "DEFAULT_POLICY_ABSENT")
    good = api._receive_source_policy(POLICY, eps)
    need(good == POLICY and good["acquisition_sources"] is not POLICY["acquisition_sources"], "EXACT_ORDER_COPY")
    variants = [dict(acquisition_sources=["A"]), {**POLICY, "acquisition_sources": []},
        {**POLICY, "acquisition_sources": ["A", "A"]},
        {**POLICY, "acquisition_sources": ["unapproved"]},
        {**POLICY, "acquisition_sources": ["A"]*9},
        {**POLICY, "acquisition_sources": ("A", "B")},
        {**POLICY, "attempt_timeout_ms": True}, {**POLICY, "attempt_timeout_ms": 0},
        {**POLICY, "finalization_reserve_ms": 60001}, {**POLICY, "finalization_reserve_ms": 1.5}]
    for bad in variants:
        refusal(lambda bad=bad: api._receive_source_policy(bad, eps), ValueError)
    for deadline, remaining, cap, now, expected in (
        (20, 2, 30000, 10, 4000), (20, 2, 1500, 10, 1500),
        (20, 1, 30000, 10, 9000), (20, 8, 60000, 10, 250)):
        need(api._source_timeout_ms(deadline, remaining, cap, now=now) == expected, "TIME_DIVISION")
    for values in ((12, 2, 1000, 10), (10, 1, 1000, 10), (20, 0, 1000, 10),
                   (20, 1, True, 10), (float("inf"), 1, 1000, 10)):
        refusal(lambda v=values: api._source_timeout_ms(v[0], v[1], v[2], now=v[3]), ValueError)
    router = api._ReceiveSources(None, "origin", POLICY, 30, check)
    need(router.deadline == 28 and set(router.report["by_provider"]) == {"A", "B"}, "RESERVE_ONCE")
    return dict(invalid_policies=len(variants), arithmetic_cases=9, default_unchanged=True)


async def acquisition_controls(s, f, output):
    """Real one-ticket acquisition and source router; no owner/native action."""
    outcomes = []
    expected_errors = {
        "http400": (ValueError, "ORDINARY_ACQUISITION_HTTP_STATUS"),
        "wrong-preview": (ValueError, "ORDINARY_PREVIEW_EXACT_BYTES"),
        "wrong-evidence": (ValueError, "ORDINARY_EVIDENCE_EXACT_ID"),
        "wrong-locator": (ValueError, "ORDINARY_LOCATOR_EXACT_EXPORT"),
        "tls": (ssl.SSLCertVerificationError, "TEST_TLS"),
        "bare-timeout": (TimeoutError, "TEST_UNOWNED_TIMEOUT"),
        "os-error": (OSError, "TEST_LOCAL_OS"),
        "cancel": (asyncio.CancelledError, "TEST_CANCEL"),
        "retention": (sqlite3.OperationalError, "TEST_RETENTION_FAILURE"),
        "settlement": (ValueError, "TEST_SETTLEMENT_FAILURE"),
        "budget": (ValueError, "ORDINARY_AGGREGATE_BUDGET"),
        "live-after-failure": (ValueError, "TEST_OWNER_OR_CA_RECHECK_FAILED"),
    }
    for fault in ("http400", "wrong-preview", "wrong-evidence", "wrong-locator", "tls", "bare-timeout",
                  "os-error", "cancel", "retention", "settlement", "budget", "live-after-failure"):
        check()
        store = s.O.OrdinaryStore(output/("terminal-"+fault), s.S.semantic_id(), STORE_LIMITS, create=True)
        maximum = len(f.preview)
        ledger = s.O.OrdinaryBudget(deadline=time.monotonic()+20, requests=8,
                                   reply_bytes=maximum if fault == "budget" else MIB)
        client = s.O.OrdinaryAcquisition(f.adapter, endpoints(s), ledger, local_custody=store)
        calls, live_calls = [], []
        def live():
            check(); ledger.active(); live_calls.append(1)
            if fault == "live-after-failure" and len(live_calls) == 2:
                raise ValueError("TEST_OWNER_OR_CA_RECHECK_FAILED")
        router = s.api._ReceiveSources(client, "origin", POLICY, ledger.deadline, live)
        async def exchange(ep, route, request, cap, timeout, **kwargs):
            calls.append(ep.port)
            need(ep.port == endpoints(s)["A"].port, "TERMINAL_MUST_NOT_FALLBACK")
            if fault == "tls": raise ssl.SSLCertVerificationError("TEST_TLS")
            if fault == "bare-timeout": raise TimeoutError("TEST_UNOWNED_TIMEOUT")
            if fault == "os-error": raise OSError("TEST_LOCAL_OS")
            if fault == "cancel": raise asyncio.CancelledError("TEST_CANCEL")
            if fault in ("settlement", "budget", "live-after-failure"):
                raise s.H.TransportUnavailable("CONNECTION_REFUSED")
            if fault == "http400": return response(s, b"", request, 400)
            if fault == "wrong-evidence": return response(s, f.units[f.second["unit_id"]], request)
            if fault == "wrong-locator":
                return response(s, s.F.compact(dict(schema=s.PP.LOCATOR_SCHEMA, semantic_id=s.S.semantic_id(),
                    unit_id=f.first["unit_id"], export_name=f.first["name"])), request)
            return response(s, f.preview+b" " if fault == "wrong-preview" else f.preview, request)
        async def action():
            if fault == "wrong-evidence":
                return await router.fetch(client.evidence, s.S.semantic_id(), f.target["unit_id"], 4096)
            if fault == "wrong-locator":
                return await router.fetch(client.locator, s.S.semantic_id(), f.second["export_id"], 1024,
                                          expected_name=f.second["name"])
            return await router.fetch(client.preview, f.record)
        try:
            with ExitStack() as guards:
                guards.enter_context(patch.object(s.H, "exchange", exchange))
                if fault == "retention":
                    guards.enter_context(patch.object(store, "put_preview",
                        side_effect=sqlite3.OperationalError("TEST_RETENTION_FAILURE")))
                if fault == "settlement":
                    guards.enter_context(patch.object(ledger, "settle", side_effect=ValueError("TEST_SETTLEMENT_FAILURE")))
                error = await async_refusal(action, *expected_errors[fault])
            need(not isinstance(error, s.O.AcquisitionUnavailable) and len(calls) == 1,
                 "TERMINAL_PROPAGATION")
            if fault == "cancel": need(isinstance(error, asyncio.CancelledError), "CANCELLATION_UNCHANGED")
            if fault == "settlement":
                need(str(error) == "TEST_SETTLEMENT_FAILURE" and ledger.pending is not None
                     and ledger.reply_bytes == 0, "SETTLEMENT_UNCERTAINTY_NOT_RECOVERY")
                # The failed reservation is retained in the report, not refunded
                # or fabricated into a successful settlement by this test.
            else:
                need(ledger.pending is None and ledger.requests == 1 and ledger.reply_bytes ==
                     (4096 if fault == "wrong-evidence" else 1024 if fault == "wrong-locator" else maximum),
                     "FAILED_FULL_CAP_CHARGE")
            if fault == "budget":
                need(str(error) == "ORDINARY_AGGREGATE_BUDGET" and
                     router.report["by_provider"]["B"]["calls"] == 1, "NO_FRESH_GRANT")
            outcomes.append(dict(fault=fault, exception=type(error).__name__, error=str(error),
                acquisition=client.report(), sources=router.report, actual_exchange_calls=len(calls)))
        finally:
            store.close()
            if ledger.pending is None: ledger.close()
    # Legacy no-keyword API refuses unavailable status; it never silently retries.
    ledger = s.O.OrdinaryBudget(deadline=time.monotonic()+20, requests=4, reply_bytes=MIB)
    client = s.O.OrdinaryAcquisition(f.adapter, endpoints(s), ledger)
    legacy_calls = []
    async def legacy(ep, route, request, cap, timeout):
        legacy_calls.append(1)
        return response(s, b"", request, 404)
    with patch.object(s.H, "exchange", legacy):
        await async_refusal(lambda: client.preview("origin", f.record), ValueError,
                            "ORDINARY_ACQUISITION_HTTP_STATUS")
    need(len(legacy_calls) == 1 and ledger.reply_bytes == len(f.preview), "DEFAULT_UNAVAILABLE_NOT_RECOVERED")
    ledger.close()
    return dict(terminal_cases=outcomes, legacy_404_nonretry=True)


async def transport_controls(s):
    """Three real loopback requests; all additional error injections are explicit."""
    H = s.H
    tasks, errors, requests = set(), [], []
    release = asyncio.Event()
    async def handler(reader, writer):
        task = asyncio.current_task(); tasks.add(task)
        try:
            head = await reader.readuntil(b"\r\n\r\n")
            count = int(next(line.split(b":", 1)[1] for line in head.split(b"\r\n")
                             if line.startswith(b"Content-Length:")))
            await reader.readexactly(count)
            requests.append("received")
            if len(requests) < 3:
                writer.write(H._header("HTTP/1.1 200 OK", 4)+b"{}")
                await writer.drain()
            else:
                await release.wait()
        except BaseException as error:
            errors.append(type(error).__name__)
        finally:
            writer.close()
            try: await writer.wait_closed()
            except Exception as error: errors.append(type(error).__name__)
            tasks.discard(task)
    server = await asyncio.start_server(handler, "127.0.0.1", 0)
    endpoint = H.Endpoint("127.0.0.1", server.sockets[0].getsockname()[1])
    route = H.ORDINARY_PREVIEW_ROUTE
    try:
        await async_refusal(lambda: H.exchange(endpoint, route, {}, 32, 1000), asyncio.IncompleteReadError)
        eof = await async_refusal(lambda: H.exchange(endpoint, route, {}, 32, 1000,
            classify_unavailable=True), H.TransportUnavailable)
        need(eof.reason == "INCOMPLETE_READ", "ACTUAL_EOF_CLASSIFICATION")
        timed = await async_refusal(lambda: H.exchange(endpoint, route, {}, 32, 200,
            classify_unavailable=True), H.TransportUnavailable)
        need(timed.reason == "ATTEMPT_TIMEOUT", "OWN_TIMEOUT_CLASSIFICATION")
    finally:
        release.set(); server.close(); await server.wait_closed()
        if tasks:
            await asyncio.wait_for(asyncio.gather(*tuple(tasks)), 2)
    need(len(requests) == 3 and not tasks and not errors, "ACTUAL_LOOPBACK_CLEANUP")
    injected = []
    for error, expected in ((ConnectionRefusedError(), "CONNECTION_REFUSED"),
        (ConnectionResetError(), "CONNECTION_RESET"), (ConnectionAbortedError(), "CONNECTION_ABORTED"),
        (BrokenPipeError(), "BROKEN_PIPE"), (ssl.SSLError("TEST_TLS"), None),
        (TimeoutError("TEST_BARE_TIMEOUT"), None), (OSError("TEST_OS"), None),
        (asyncio.CancelledError("TEST_CANCEL"), None)):
        async def failed_connect(*args, selected=error, **kwargs): raise selected
        with patch.object(H.asyncio, "open_connection", failed_connect):
            caught = await async_refusal(lambda: H.exchange(endpoint, route, {}, 32, 1000,
                classify_unavailable=True), H.TransportUnavailable if expected else type(error))
        if expected: need(caught.reason == expected, "NETWORK_REASON_ENUM")
        else: need(caught is error, "NONAVAILABILITY_IDENTITY")
        injected.append(dict(error=type(error).__name__, classification=expected))
    with patch.object(H.asyncio, "open_connection", forbidden):
        await async_refusal(lambda: H.exchange(H.Endpoint("192.0.2.1", 443), route, {}, 32, 1000,
            classify_unavailable=True), ValueError, "REMOTE_TLS_REQUIRED")
        with patch.object(H.ssl, "create_default_context", side_effect=FileNotFoundError("TEST_CA_SETUP")):
            await async_refusal(lambda: H.exchange(H.Endpoint("127.0.0.1", 443, True), route,
                {}, 32, 1000, classify_unavailable=True), FileNotFoundError, "TEST_CA_SETUP")
    return dict(actual_loopback_requests=3, actual_eof_and_timeout=True, clean=True,
                injected_connection_cases=injected, endpoint_and_ca_setup_terminal=True)


async def run(s, f, output):
    groups = []
    save(output/"policy.json", policy_controls(s)); groups.append("policy_validation_and_time_division")
    default = await receive_case(s, f, output, "default", mode="default", opt=False, grounded=True)
    need(len(default["calls"]) == 2 and "source_acquisition" not in default["report"] and
         default["owner_calls"].count("admit-double") == 1, "DEFAULT_RECEIVE_REPORT_AND_ADMISSION")
    groups.append("default_receive_compatibility")
    multi = await receive_case(s, f, output, "disjoint")
    expected_order = ["A", "B", "A", "B", "A", "A", "A", "B", "A", "B"]
    need([row["provider"] for row in multi["calls"]] == expected_order and
         multi["owner_calls"] == ["context", "preflight:NEEDS", "preflight:NEEDS",
                                  "preflight:READY", "admit-double"], "DISJOINT_ORDER_AND_ONE_FINAL_ADMIT")
    wanted_units = sorted(t["unit_id"] for t in (f.target, f.second, f.first))
    need(multi["report"]["unit_ids"] == wanted_units, "EXACT_SELECTED_CLOSURE")
    sources = multi["report"]["source_acquisition"]
    need(sources["discovery_provider"] == "origin" and sources["fetches"] == 6 and
         sources["by_provider"]["A"] == dict(calls=6, successes=2, unavailable=4, last_reason="HTTP_503") and
         sources["by_provider"]["B"] == dict(calls=4, successes=4, unavailable=0, last_reason=None),
         "BOUNDED_PER_PROVIDER_REPORT")
    failed_caps = len(f.preview)+4096+1024+4096
    successful_bytes = len(f.preview)+sum(len(f.units[uid]) for uid in wanted_units)
    successful_bytes += sum(len(s.F.compact(dict(schema=s.PP.LOCATOR_SCHEMA,
        semantic_id=s.S.semantic_id(), unit_id=t["unit_id"], export_name=t["name"])))
        for t in (f.second, f.first))
    need(multi["report"]["network"]["charged_reply_bytes"] == 64+failed_caps+successful_bytes,
         "FULL_FAILED_CAP_PLUS_SUCCESSFUL_ACTUAL_ACCOUNTING")
    groups.append("disjoint_exact_suppliers_shared_grant_and_ready_only_admission_double")
    selected = await receive_case(s, f, output, "selected-only", policy="selected-unit-only")
    need(selected["report"]["status"] == "NEED_GROUNDED_PREMISES" and
         selected["owner_calls"].count("admit-double") == 0 and len(selected["calls"]) == 4 and
         all(row["route"] != s.O.LOCATOR_ROUTE and row["request"].get("unit_id", f.target["unit_id"])
             == f.target["unit_id"] for row in selected["calls"]), "ZERO_ANCESTOR_REQUESTS")
    missing = await receive_case(s, f, output, "missing-preview", mode="no-preview",
                                 expect="PEER_ACQUISITION_SOURCES_EXHAUSTED")
    need(len(missing["calls"]) == 2 and missing["owner_calls"] == ["context"] and
         all(row["route"] == s.O.PREVIEW_ROUTE for row in missing["calls"]), "NO_INVENTED_PREVIEW")
    groups.append("selected_only_zero_ancestors_and_evidence_only_holder_refusal")
    save(output/"terminal.json", await acquisition_controls(s, f, output))
    groups.append("terminal_failures_and_conservative_nonrenewing_accounting")
    save(output/"transport.json", await transport_controls(s))
    groups.append("real_loopback_and_narrow_transport_classification")
    return groups


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("source-root", "fixture-root", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON_PROFILE")
    here, output, root = Path(__file__).absolute().parent, Path(args.output), Path(args.fixture_root)
    need(output.is_absolute() and not output.exists() and output.parent.is_dir(), "FRESH_OUTPUT")
    need(root.is_absolute() and root.is_dir() and not output.is_relative_to(root)
         and not root.is_relative_to(output), "RETAINED_INPUT_SEPARATION")
    s = support(here, Path(args.source_root))
    f = fixture(s, root)
    output.mkdir()
    save(output/"INPUTS.json", dict(request_sha256=REQUEST_SHA, manifest_sha256=MANIFEST_SHA,
        units=4, evidence_bytes=5149, source_files={name: sha(read(here/name)) for name in
        ("http_provider.py", "ordinary_acquisition.py", "peer_api.py", "test_multi_source.py")},
        mathematical_authority="EXPLICIT_DOUBLES_NOT_LEAN", new_fixture_construction=False))
    try:
        with patch("subprocess.Popen", forbidden), patch("os.system", forbidden):
            groups = asyncio.run(run(s, f, output))
        read(root/"prepare-request.json", expected=REQUEST_SHA)
        read(root/"bundle/manifest.json", expected=MANIFEST_SHA)
        for path, maximum, expected in f.inputs: read(path, maximum, expected)
        check()
        result = dict(status="PASS", groups=groups, group_count=len(groups), mathematical_acceptance=False,
            native_calls=0, actual_loopback_requests=3, wall_seconds=time.monotonic()-START,
            test_process_cpu_seconds=time.process_time()-CPU,
            scope="MULTI_SOURCE_CONTROL_WITH_EXPLICIT_AUTHORITY_DOUBLES_NOT_MATHEMATICAL_QUALIFICATION")
        save(output/"TEST-RESULT.json", result)
        print(json.dumps(result), flush=True)
        return 0
    except BaseException as error:
        save(output/"FAILURE.json", dict(status="FAILED", exception=type(error).__name__, error=str(error),
            mathematical_acceptance=False, wall_seconds=time.monotonic()-START,
            test_process_cpu_seconds=time.process_time()-CPU))
        raise


if __name__ == "__main__":
    raise SystemExit(main())

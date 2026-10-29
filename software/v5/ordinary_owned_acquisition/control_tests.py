"""Focused typed-acquisition controls; not executable until root selects a run.

Load the selected assembled package, use real codecs/ledger/source scheduler,
script transport responses and one post-TLS setup expiry boundary. No application
socket, database, owner, native process or mathematical acceptance. Retention is
an explicitly inert method spy on an uninitialized OrdinaryStore instance.
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
import socket
import ssl
import sys
import time
from types import SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
START, CPU = time.monotonic(), time.process_time()
MIB = 1024**2
PINS = {
    "support/transport/ordinary_acquisition.py": "677b6a6acd17de5ad60dbdd5700aac3014fc7a571876757b39382f8642f6d37e",
    "support/transport/fair_exchange.py": "a04c4577a4fd6b3f68a48a869397d5ee35ec5075f7e5c1c496f5bb31fb06fc9a",
}
FIXTURE = ROOT/"experiments/v5-local-checks/contribution-bundle-controls01/checks/bundle-completion/units"
UNIT = "f1c20bb5d6ef8d37227b0db40e0479d22ef3849f34c71d7a41880497316b1aa0"
UNIT_SHA = "53c957070a250ac49c9ec46d2fdb091d0967143852546238c4d21d08f7f1506e"
OTHER = "25ae588e95228a64196a576aa9c9dd78249c23b0c26189c5671a434b93afa1b3"
OTHER_SHA = "c7266a3047afcf59059b7884853b4d6b9be4244509f260e78dd072973f9704aa"
CASES, FORBIDDEN = [], []


def need(ok, code):
    if not ok:
        raise AssertionError("OWNED_ACQUISITION_CONTROL_"+code)


def check():
    need(time.monotonic()-START < 120 and time.process_time()-CPU < 60, "ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, pin=None, maximum=2*MIB):
    check()
    need(path.is_absolute() and path.is_file() and not path.is_symlink(), "INPUT")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(0 < len(raw) <= maximum and (pin is None or sha(raw) == pin), "INPUT_PIN")
    return raw


def forbidden(*args, **kwargs):
    if len(FORBIDDEN) < 16:
        FORBIDDEN.append("FORBIDDEN_EXTERNAL_EFFECT")
    raise AssertionError("OWNED_ACQUISITION_FORBIDDEN_EXTERNAL_EFFECT")


def save(path, value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":")).encode("ascii")
    need(len(raw) <= 2*MIB, "REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def load(args):
    package = Path(args.package)
    need(package.is_absolute() and package.resolve(strict=True) == package, "PACKAGE")
    profile_raw = read(package/"PROFILE.json", args.profile_sha256)
    profile = json.loads(profile_raw)
    for relative, digest in PINS.items():
        raw = read(package/relative, digest)
        need(profile["files"][relative] == dict(bytes=len(raw), sha256=digest), "SUCCESSOR_PIN")
    source = read(package/"profile.py")
    need(profile["files"]["profile.py"] == dict(bytes=len(source), sha256=sha(source)), "LOADER_PIN")
    spec = importlib.util.spec_from_file_location("_owned_acquisition_profile", package/"profile.py")
    need(spec.name not in sys.modules, "PRELOADED_LOADER")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    exec(compile(source, str(package/"profile.py"), "exec"), module.__dict__)
    loaded = module.load(package, args.profile_sha256,
        dict(python_runtime=args.python_runtime, lean_runtime=args.lean_runtime),
        START+120, check_parent=check)
    p, O = loaded.peer_api, loaded.O
    need(p.O is O and p.X.H is O.H and p.H is O.H, "SHARED_MODULE_IDENTITIES")
    return loaded


def fixture(loaded):
    p = loaded.peer_api
    raw = read(FIXTURE/(UNIT+".json"), UNIT_SHA, 4997)
    other = read(FIXTURE/(OTHER+".json"), OTHER_SHA, 2133)
    exact = loaded.A.PE.read_evidence(raw)
    need(exact.unit_id == UNIT and len(raw) == 4997, "FIXTURE_UNIT")
    name = exact.document["unit"][2][0][0]
    semantic = loaded.installation.semantic_id
    identity = loaded.A.S.export_id(semantic, UNIT, name)
    need(identity == "d0c7be50520d2b91b72e43308b8f1ec75022b32c37fe9561381f4aef879fff1a", "FIXTURE_EXPORT")
    preview = p.PP.preview_from_evidence(raw, name)
    adapter = p.OrdinaryExportAdapter(semantic)
    record = adapter.extract(preview, identity)
    offers = p.AO.OfferMap.from_bytes(p.F.compact(dict(schema=p.AO.MAP_SCHEMA, entries=[])))
    return NS(raw=raw, other=other, name=name, semantic=semantic, identity=identity,
              preview=preview, locator=p.F.compact(record["locator"]), record=record,
              adapter=adapter, offers=offers)


def budget(O, *, deadline=None):
    return O.OrdinaryBudget(deadline=time.monotonic()+60 if deadline is None else deadline,
                            requests=32, reply_bytes=MIB)


def client(loaded, f, ledger, *, retention=None, tls=False):
    O, H = loaded.O, loaded.peer_api.H
    endpoints = {label: H.Endpoint("127.0.0.1", 43101+i, tls,
                                  "math.example" if tls else None)
                 for i, label in enumerate(("A", "B"))}
    return O.OrdinaryAcquisition(f.adapter, endpoints, ledger, local_custody=retention)


def spec(kind, c, f):
    O = sys.modules["transport.ordinary_acquisition"]
    if kind == "preview":
        return NS(method=c.preview, args=(f.record,), kwargs={}, route=O.PREVIEW_ROUTE, maximum=len(f.preview))
    if kind == "locator":
        return NS(method=c.locator, args=(f.semantic, f.identity, 4096),
                  kwargs=dict(expected_name=f.name), route=O.LOCATOR_ROUTE, maximum=4096)
    if kind == "evidence":
        return NS(method=c.evidence, args=(f.semantic, UNIT, 8192),
                  kwargs=dict(expected_export_id=f.identity, expected_export_name=f.name),
                  route=O.EVIDENCE_ROUTE, maximum=8192)
    need(kind == "offers", "KIND")
    return NS(method=c.authoring_offers, args=(f.semantic, f.identity, 4096),
              kwargs=dict(max_offers=1), route=O.AUTHORING_OFFERS_ROUTE, maximum=4096)


async def direct(item, *, retry=False, timeout=5000):
    kwargs = dict(item.kwargs)
    if item.route != sys.modules["transport.ordinary_acquisition"].AUTHORING_OFFERS_ROUTE:
        kwargs.update(unavailable_errors=retry, attempt_timeout_ms=timeout)
    return await item.method("A", *item.args, **kwargs)


def body(loaded, f, route, request):
    O = loaded.O
    if route == O.PREVIEW_ROUTE: return f.preview
    if route == O.LOCATOR_ROUTE: return f.locator
    if route == O.EVIDENCE_ROUTE: return f.raw
    need(route == O.AUTHORING_OFFERS_ROUTE, "REPLY_ROUTE")
    return f.offers.reply(request)


def response(loaded, raw, request, status=200):
    return dict(status=status, raw=raw, request_bytes=len(loaded.peer_api.F.compact(request)),
                reply_bytes=len(raw), header_bytes=128, elapsed_ms=0)


def scheduler(loaded, c, ledger):
    def live():
        check(); ledger.active()
    return loaded.peer_api._ReceiveSources(c, "A", dict(acquisition_sources=["A", "B"],
        attempt_timeout_ms=1000, finalization_reserve_ms=1000), ledger.deadline, live)


async def caught(action):
    try:
        await action()
    except BaseException as error:
        return error
    raise AssertionError("OWNED_ACQUISITION_EXPECTED_FAILURE")


def finished(ledger):
    need(ledger.pending is None, "NO_PENDING_TICKET")
    ledger.close()


async def controls(loaded, f):
    O, X, H, p = loaded.O, loaded.peer_api.X, loaded.peer_api.H, loaded.peer_api
    kinds = ("preview", "locator", "evidence", "offers")
    with patch.object(H, "exchange", forbidden):
        ledger = budget(O)
        ledger.charge_external("already-reserved-search", 1, 128)
        original_deadline = ledger.deadline
        retained, calls, sizes = [], [], []
        store = O.OrdinaryStore.__new__(O.OrdinaryStore)
        store.semantic_id = f.semantic
        def retain(kind):
            def keep(raw, *, before_commit):
                before_commit(); retained.append((kind, raw))
            return keep
        store.put_preview, store.put_evidence = retain("preview"), retain("evidence")
        c = client(loaded, f, ledger, retention=store)
        async def success(endpoint, route, request, maximum, timeout_ms, *, absolute_deadline):
            need(time.monotonic() < absolute_deadline <= original_deadline and 1 <= timeout_ms <= 60000,
                 "ORIGINAL_ABSOLUTE_HORIZON")
            raw = body(loaded, f, route, request)
            need(len(raw) <= maximum, "VALID_REPLY_CAP")
            calls.append(route); sizes.append(len(raw))
            return response(loaded, raw, request)
        with patch.object(X, "exchange", success):
            for kind in kinds:
                result = await direct(spec(kind, c, f))
                need(result["mathematical_acceptance"] is False, "NO_ACCEPTANCE")
        need(calls == [spec(k, c, f).route for k in kinds] and ledger.requests == 5 and
             ledger.reply_bytes == 128+sum(sizes) and ledger.deadline == original_deadline and
             retained == [("preview", f.preview), ("evidence", f.raw)] and
             c.http["completed_responses"] == 4 and c.http["failed_attempts"] == 0,
             "FOUR_TYPED_READS_EXACT_RETAINED_AND_SHARED_GRANT")
        finished(ledger)
        CASES.append(dict(case="four-typed-successes-real-codecs-retention-spies-original-ledger", status="PASS"))

        for reason in ("ATTEMPT_TIMEOUT", "CONNECTION_REFUSED", "CONNECTION_RESET", "BROKEN_PIPE", "PEER_EOF", "HTTP_404", "HTTP_503"):
            ledger = budget(O); ledger.charge_external("prepaid-location", 1, 64)
            c = client(loaded, f, ledger); item = spec("locator", c, f)
            sources, calls = scheduler(loaded, c, ledger), []
            async def fallback(endpoint, route, request, maximum, timeout_ms, *, absolute_deadline):
                calls.append(endpoint.port)
                need(absolute_deadline <= ledger.deadline, "FALLBACK_HORIZON")
                if len(calls) == 1:
                    if reason.startswith("HTTP_"):
                        return response(loaded, b"{}", request, int(reason[5:]))
                    return X.SettledRefusal(reason)
                need(ledger.pending is not None and ledger.requests == 3 and ledger.reply_bytes == 64+item.maximum,
                     "FAILURE_FULLY_SETTLED_BEFORE_SECOND_DIAL")
                return response(loaded, f.locator, request)
            with patch.object(X, "exchange", fallback):
                result = await sources.fetch(item.method, *item.args, **item.kwargs)
            expected = "INCOMPLETE_READ" if reason == "PEER_EOF" else reason
            need(calls == [43101, 43102] and result["locator"]["unit_id"] == UNIT and
                 ledger.requests == 3 and ledger.reply_bytes == 64+item.maximum+len(f.locator) and
                 sources.report["by_provider"]["A"]["last_reason"] == expected and
                 c.http["failed_attempts"] == 1, "ONLY_SETTLED_FALLBACK")
            finished(ledger)
        CASES.append(dict(case="five-settled-reasons-and-two-http-unavailable-outcomes-share-ledger", status="PASS"))

        factories = (
            ("protocol", lambda: X.SettledRefusal("HTTP_PROTOCOL"), ValueError),
            ("unknown-reason", lambda: X.SettledRefusal("UNKNOWN"), ValueError),
            ("unsettled", lambda: X.UnsettledTransportError("SCRIPTED_UNCERTAIN_CLOSE"), X.UnsettledTransportError),
            ("tls", lambda: ssl.SSLError("SCRIPTED_TLS_FAILURE"), ssl.SSLError),
            ("cancelled", lambda: asyncio.CancelledError(), asyncio.CancelledError),
            ("unknown-local", lambda: RuntimeError("SCRIPTED_LOCAL_FAILURE"), RuntimeError),
            ("aborted", lambda: ConnectionAbortedError("SCRIPTED_ABORT"), ConnectionAbortedError),
        )
        for label, factory, expected in factories:
            ledger = budget(O); c = client(loaded, f, ledger); item = spec("locator", c, f)
            sources, calls = scheduler(loaded, c, ledger), []
            async def terminal(endpoint, *args, **kwargs):
                calls.append(endpoint.port); outcome = factory()
                if isinstance(outcome, BaseException): raise outcome
                return outcome
            with patch.object(X, "exchange", terminal):
                error = await caught(lambda: sources.fetch(item.method, *item.args, **item.kwargs))
            need(type(error) is expected and not isinstance(error, O.AcquisitionUnavailable) and
                 calls == [43101] and ledger.requests == 1 and ledger.reply_bytes == item.maximum and
                 c.http["failed_attempts"] == 1, "TERMINAL_NO_FALLBACK:"+label)
            finished(ledger)
        CASES.append(dict(case="protocol-unsettled-tls-cancellation-unknown-failures-terminal", status="PASS"))

        for kind in kinds:
            ledger = budget(O); c = client(loaded, f, ledger); item = spec(kind, c, f); calls = []
            async def default_refusal(endpoint, *args, **kwargs):
                calls.append(endpoint.port); return X.SettledRefusal("CONNECTION_REFUSED")
            with patch.object(X, "exchange", default_refusal):
                error = await caught(lambda: direct(item))
            need(type(error) is ValueError and "ORDINARY_ACQUISITION_TRANSPORT_CONNECTION_REFUSED" in str(error)
                 and calls == [43101] and ledger.requests == 1 and ledger.reply_bytes == item.maximum,
                 "DEFAULT_NO_RETRY:"+kind)
            finished(ledger)
        CASES.append(dict(case="all-four-default-reads-including-authoring-stay-no-retry", status="PASS"))

        for kind in kinds:
            ledger = budget(O); c = client(loaded, f, ledger); item = spec(kind, c, f); calls = []
            async def invalid(endpoint, route, request, *args, **kwargs):
                calls.append(endpoint.port)
                if kind == "evidence": raw = f.other
                elif kind == "locator":
                    row = deepcopy(f.record["locator"]); row["unit_id"] = OTHER; raw = p.F.compact(row)
                elif kind == "offers":
                    row = json.loads(body(loaded, f, route, request)); row["export_id"] = "0"*64; raw = p.F.compact(row)
                else: raw = b"{}"
                return response(loaded, raw, request)
            with patch.object(X, "exchange", invalid):
                if kind == "offers": error = await caught(lambda: direct(item))
                else:
                    sources = scheduler(loaded, c, ledger)
                    error = await caught(lambda: sources.fetch(item.method, *item.args, **item.kwargs))
            need(isinstance(error, ValueError) and not isinstance(error, O.AcquisitionUnavailable) and
                 calls == [43101] and ledger.requests == 1 and ledger.reply_bytes == item.maximum,
                 "REAL_VALIDATOR_TERMINAL:"+kind)
            finished(ledger)
        CASES.append(dict(case="real-preview-locator-evidence-and-authoring-binding-refusals", status="PASS"))

        ledger = budget(O); events = []
        store = O.OrdinaryStore.__new__(O.OrdinaryStore); store.semantic_id = f.semantic
        def fail_retain(raw, *, before_commit):
            before_commit(); events.append(raw); raise RuntimeError("SCRIPTED_RETAIN_FAILURE")
        store.put_evidence = fail_retain
        c = client(loaded, f, ledger, retention=store); item = spec("evidence", c, f)
        sources, calls = scheduler(loaded, c, ledger), []
        async def retained_response(endpoint, route, request, *args, **kwargs):
            calls.append(endpoint.port); return response(loaded, f.raw, request)
        with patch.object(X, "exchange", retained_response):
            error = await caught(lambda: sources.fetch(item.method, *item.args, **item.kwargs))
        need(type(error) is RuntimeError and str(error) == "SCRIPTED_RETAIN_FAILURE" and
             calls == [43101] and events == [f.raw] and ledger.reply_bytes == item.maximum and
             c.http["failed_attempts"] == 1, "RETENTION_FAILURE_FULL_CHARGE")
        finished(ledger)
        CASES.append(dict(case="retention-liveness-hook-and-terminal-full-cap-failure", status="PASS"))

        # Real successor exchange reaches its post-TLS guard for every new route.
        # Its socket engine is unchanged and already separately qualified.
        for kind, attempt_cap in [(kind, None) for kind in kinds]+[("locator", 100)]:
            start = time.monotonic(); now = [start]; setup, allocations = [], []
            clock = NS(monotonic=lambda: now[0])
            fake_socket = NS(**vars(socket))
            def allocate(*args, **kwargs):
                allocations.append(True); raise AssertionError("MUST_NOT_ALLOCATE_AFTER_EXPIRY")
            fake_socket.socket = allocate
            horizon = start + (1 if attempt_cap is None else .1)
            def context(*, cafile):
                setup.append(cafile); now[0] = horizon+.001
                return NS(minimum_version=None)
            fake_ssl = NS(create_default_context=context, TLSVersion=ssl.TLSVersion)
            with patch.object(O, "time", clock), patch.object(X, "time", clock), \
                 patch.object(X, "ssl", fake_ssl), patch.object(X, "socket", fake_socket):
                ledger = budget(O, deadline=start+(1 if attempt_cap is None else 10))
                c = client(loaded, f, ledger, tls=True); item = spec(kind, c, f)
                original = ledger.deadline
                error = await caught(lambda: direct(item, retry=True, timeout=attempt_cap))
                need(type(error) is ValueError and str(error) == "FAIR_LOCAL_ATTEMPT_SETUP_EXHAUSTED" and
                     setup == [None] and not allocations and ledger.deadline == original and
                     ledger.requests == 1 and ledger.reply_bytes == item.maximum,
                     "POST_SETUP_EXPIRY_NO_DIAL:"+kind)
                finished(ledger)
        # An expired grant cannot escape as retryable even with a settled outcome.
        now = [time.monotonic()]; clock = NS(monotonic=lambda: now[0])
        with patch.object(O, "time", clock):
            ledger = budget(O, deadline=now[0]+5); c = client(loaded, f, ledger)
            item = spec("locator", c, f); calls = []
            async def expired(endpoint, *args, **kwargs):
                calls.append(endpoint.port); now[0] = ledger.deadline+.001
                return X.SettledRefusal("CONNECTION_REFUSED")
            with patch.object(X, "exchange", expired):
                error = await caught(lambda: direct(item, retry=True))
            need(type(error) is ValueError and "ORDINARY_BUDGET_CLOSED_OR_EXPIRED" in str(error) and
                 calls == [43101] and ledger.requests == 1 and ledger.reply_bytes == item.maximum,
                 "EXPIRED_GRANT_STILL_CHARGED_NOT_RETRYABLE")
            finished(ledger)
        CASES.append(dict(case="four-routes-short-attempt-and-returned-expiry-preserve-original-grant", status="PASS"))


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTEXT")
    output = Path(args.output)
    need(output.is_absolute() and output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         output.parent.resolve(strict=True) == output.parent and not os.path.lexists(output), "FRESH_OUTPUT")
    output.mkdir()
    report = dict(passed=False, profile_sha256=args.profile_sha256, source_pins=PINS,
                  scope="SCRIPTED_TYPED_ACQUISITION_NOT_NATIVE_OR_ACTUAL_NETWORK", cases=CASES)
    loop_errors = []
    try:
        with ExitStack() as guards:
            for target in ("sqlite3.connect", "subprocess.Popen", "os.system", "socket.create_connection"):
                guards.enter_context(patch(target, forbidden))
            loaded = load(args); f = fixture(loaded)
            guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, "open", forbidden))
            loop = asyncio.new_event_loop()
            loop.set_exception_handler(lambda _loop, context: loop_errors.append(str(context)[:1000]))
            try:
                with ExitStack() as network_guards:
                    for target in ("socket.socket.connect", "socket.socket.connect_ex", "socket.socket.bind",
                                   "socket.socket.listen", "asyncio.open_connection"):
                        network_guards.enter_context(patch(target, forbidden))
                    loop.run_until_complete(controls(loaded, f))
                    loop.run_until_complete(asyncio.sleep(0))
                    need(not asyncio.all_tasks(loop), "NO_PENDING_TASKS")
            finally:
                loop.close()
            need(not loop_errors and not FORBIDDEN, "NO_EXTERNAL_OR_UNHANDLED_EFFECT")
            loaded.profile.verify(check)
            read(FIXTURE/(UNIT+".json"), UNIT_SHA, 4997)
            read(FIXTURE/(OTHER+".json"), OTHER_SHA, 2133)
            need(len(CASES) == 7, "ALL_GROUPS")
            report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:1000])
    report.update(completed_groups=len(CASES), forbidden_calls=FORBIDDEN,
                  unhandled_loop_exceptions=loop_errors, native_calls=0, owner_calls=0,
                  database_calls=0, application_network_calls=0,
                  wall_seconds=time.monotonic()-START, harness_cpu_seconds=time.process_time()-CPU)
    save(output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

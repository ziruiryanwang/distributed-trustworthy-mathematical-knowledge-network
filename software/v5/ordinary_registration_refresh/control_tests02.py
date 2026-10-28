"""Repaired changed-seam harness; root separately selects execution.

Real selected API, contact parser and budgets; scripted exchange/service/clock
and in-memory HTTP writers. No sockets, mathematical owner, database or Lean.
This does not repeat the old parser, transport or theorem campaigns.
Original control_tests.py and its non-clean run stay preserved. This successor
retains socket.socket's type and fails on unhandled event-loop callbacks.
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
import sqlite3
import subprocess
import sys
import time
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
START, CPU = time.monotonic(), time.process_time()
MIB = 1024**2
CASES = []


def need(ok, code):
    if not ok:
        raise AssertionError("REFRESH_CONTROL_" + code)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU < 20, "ALLOWANCE")


def passed(name):
    check()
    CASES.append(dict(case=name, status="PASS"))


def read(path, maximum=2*MIB):
    check()
    need(path.is_absolute() and path.is_file() and not path.is_symlink(), "INPUT")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(0 < len(raw) <= maximum, "INPUT_SIZE")
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":")).encode("ascii")
    need(len(raw) <= 2*MIB, "REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def load(args):
    package = Path(args.package)
    need(package.is_absolute() and package.resolve(strict=True) == package, "PACKAGE")
    raw = read(package/"PROFILE.json")
    need(hashlib.sha256(raw).hexdigest() == args.profile_sha256, "PROFILE_PIN")
    profile = json.loads(raw)
    source = read(package/"profile.py")
    need(profile["files"]["profile.py"] ==
         dict(bytes=len(source), sha256=hashlib.sha256(source).hexdigest()), "LOADER_PIN")
    spec = importlib.util.spec_from_file_location("_refresh_control_profile", package/"profile.py")
    module = importlib.util.module_from_spec(spec)
    need(spec.name not in sys.modules, "PRELOADED_LOADER")
    sys.modules[spec.name] = module
    exec(compile(source, str(package/"profile.py"), "exec"), module.__dict__)
    return module.load(package, args.profile_sha256,
        dict(python_runtime=args.python_runtime, lean_runtime=args.lean_runtime),
        START+45, check_parent=check)


def endpoint(port):
    return dict(host="127.0.0.1", port=port, tls=False, server_name=None)


def config(feeds=1):
    rows = [endpoint(41010), endpoint(41011)]
    names = ["feed"+str(i) for i in range(feeds)]
    return dict(
        contacts={name: dict(endpoint(40100+i), ca_file=None, ca_sha256=None)
                  for i, name in enumerate(names)},
        slots=[dict(feed=name, specs=[dict(tag="declaration-kind", value="theorem")],
                    max_contacts=2, max_bytes=4096) for name in names],
        endpoint_scopes={name: dict(tls_names=[], endpoints=deepcopy(rows)) for name in names},
        egress=dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
                    test_endpoints=[dict(host=r["host"], port=r["port"]) for r in rows]),
        refresh=dict(requests=feeds, reply_bytes=4096*feeds, attempt_timeout_ms=5000,
                     max_age_ms=20000, min_service_ms=1000),
        service=dict(host="127.0.0.1", port=0, tls=None, lease_seconds=10, cleanup_seconds=10,
                     limits=dict(max_connections=2, max_requests=8,
                                 max_reply_bytes=65536, operation_ms=1000)))


async def refresh_controls(loaded):
    api = loaded.peer_api
    C, F, X = api.CD, api.F, api.X
    all_nonces = []

    async def exercise(conf, script, *, expected_error=None, shared=None):
        clock = [time.monotonic()]
        initial = clock[0]
        allowance = SimpleNamespace(deadline=initial+60, check=check)
        exchanges, services, ready = [], [], []
        budget = None
        if shared is not None:
            budget = api.O.OrdinaryBudget(deadline=initial+30, requests=shared["requests"],
                                          reply_bytes=shared["reply_bytes"])
            budget.charge_external(shared["label"], 1, 1)
            original_budget_deadline = budget.deadline

        async def exchange(ep, route, request, cap, timeout_ms, *, absolute_deadline):
            need(ep.port in {r["port"] for r in conf["contacts"].values()}, "NO_LEARNED_DIAL")
            need(route == api.H.CONTACT_DIRECTORY_ROUTE, "ONLY_CONTACT_REQUEST")
            need(len(exchanges) < len(script), "UNEXPECTED_RETRY")
            item = script[len(exchanges)]
            exchanges.append((ep.port, deepcopy(request)))
            all_nonces.append(request["nonce"])
            elapsed = item.get("elapsed", 0)
            need(elapsed*1000 <= timeout_ms and clock[0]+elapsed <= absolute_deadline,
                 "SCRIPT_WITHIN_TRANSPORT_DEADLINE")
            clock[0] += elapsed
            if item.get("unavailable"):
                return X.SettledRefusal("CONNECTION_REFUSED")
            reply = C._envelope(request, deepcopy(item.get("rows", [])), item.get("truncated", False))
            if item.get("invalid"):
                reply["nonce"] = "0"*64 if request["nonce"] != "0"*64 else "1"*64
            raw = F.compact(reply)
            need(len(raw) <= cap, "SCRIPT_REPLY_BOUND")
            return dict(status=item.get("status", 200), raw=raw, reply_bytes=len(raw),
                        request_bytes=len(F.compact(request)), header_bytes=100)

        async def serve(_loaded, service, _allowance, *, ready=None, contact_deadline=None,
                        minimum_service_ms=0):
            need(_loaded is loaded and _allowance is allowance, "SAME_CONTEXT")
            need(clock[0]+minimum_service_ms/1000 <= contact_deadline, "LIVE_SERVICE_HANDOFF")
            services.append(dict(config=deepcopy(service), cutoff=contact_deadline,
                                 minimum_ms=minimum_service_ms))
            value = dict(status="READY", mathematical_acceptance=False)
            if ready is not None:
                ready(value)
            return dict(status="LEASE_FINISHED", quiescent=True, cleanup_errors=[])

        original = deepcopy(conf)
        with patch.object(api, "time", SimpleNamespace(monotonic=lambda: clock[0])), \
             patch.object(X, "exchange", new=exchange), patch.object(api, "directory_serve", new=serve):
            try:
                result = await api.directory_refresh_serve(loaded, conf, allowance,
                    ready=ready.append, network_budget=budget)
            except api.PeerFailure as caught:
                need(expected_error is not None and caught.report["error"]["code"] == expected_error,
                     "EXPECTED_POLICY_FAILURE")
                need(exchanges == [] and services == [] and ready == [], "REFUSE_BEFORE_IO")
                result = caught.report
            else:
                need(expected_error is None, "EXPECTED_REFUSAL")
                need(result["network"]["closed"] == (budget is None) and result["quiescent"] and
                     result["cleanup_errors"] == [], "CLOSED_REFRESH")
        if budget is not None:
            need(not budget.closed and budget.pending is None and
                 budget.deadline <= original_budget_deadline, "SHARED_OWNERSHIP_NO_RENEWAL")
            budget.close()
        need(conf == original and not result["mathematical_acceptance"], "NO_MUTATION_OR_ACCEPTANCE")
        return result, exchanges, services, ready

    invalids = []
    q = config(2); q["slots"][0]["max_contacts"] = 9; q["slots"][1]["max_contacts"] = 8
    invalids.append((q, "REFRESH_ROUTE_QUOTA_SUM"))
    q = config(); q["slots"].append(deepcopy(q["slots"][0]))
    invalids.append((q, "REFRESH_DUPLICATE_SLOT"))
    q = config(2); q["refresh"]["reply_bytes"] = 4096
    invalids.append((q, "REFRESH_COMPLETE_PLAN_ALLOCATION"))
    q = config(); q["endpoint_scopes"]["unexpected"] = deepcopy(q["endpoint_scopes"]["feed0"])
    invalids.append((q, "REFRESH_SCOPE_FEEDS"))
    for q, code in invalids:
        await exercise(q, [], expected_error=code)
    passed("policy-slot-quota-and-full-plan-refuse-before-io")

    shared = dict(requests=8, reply_bytes=32768, label="earlier-work")
    report, _, _, _ = await exercise(config(), [dict(rows=[])], shared=shared)
    need(not report["network"]["closed"] and report["network"]["requests"] == 2 and
         report["network"]["charged_reply_bytes"] == 4097 and
         len(report["network"]["external_prepaid"]) == 2, "SHARED_CHARGES_PRESERVED")
    await exercise(config(), [], expected_error="ORDINARY_AGGREGATE_BUDGET",
                   shared=dict(shared, requests=1))
    await exercise(config(), [], expected_error="ORDINARY_EXTERNAL_LABEL",
                   shared=dict(shared, label="directory-refresh-serve"))
    passed("shared-ledger-preserves-prior-charges-owner-lifetime-and-deadline")

    base = config()
    first, _, a, _ = await exercise(base, [dict(rows=[endpoint(41010)])])
    second, _, b, _ = await exercise(base, [dict(rows=[endpoint(41011)])])
    empty, _, c, _ = await exercise(base, [dict(rows=[])])
    need(first["refresh_complete"] and second["refresh_complete"] and
         a[0]["config"]["entries"][0]["endpoints"] == [endpoint(41010)] and
         b[0]["config"]["entries"][0]["endpoints"] == [endpoint(41011)] and
         empty["status"] == "REFRESHED_EMPTY" and empty["lookups"][0]["status"] == "EMPTY_SOURCE"
         and empty["refresh_complete"] and c == [], "REPLACEMENT_WITHDRAWAL_NO_CACHE")
    need(len(set(all_nonces)) == len(all_nonces), "FRESH_NONCES")
    passed("fresh-replacement-empty-withdrawal-no-cached-fallback")

    for item, status in ((dict(truncated=True), "EMPTY_TRUNCATED_SOURCE"),
                         (dict(invalid=True), "INVALID_DIRECTORY_METADATA"),
                         (dict(unavailable=True), "SETTLED_UNAVAILABLE"),
                         (dict(status=503), "HTTP_REFUSAL")):
        report, calls, served, _ = await exercise(base, [item])
        need(report["status"] == "INCOMPLETE_REFRESH_EMPTY" and not report["refresh_complete"] and
             report["lookups"][0]["status"] == status and len(calls) == 1 and served == [],
             "EMPTY_FAILURE_DISTINCTIONS")
        need(report["refresh"]["charged_reply_bytes"] == 4096, "NO_REFUND_ON_FAILURE")
    passed("empty-truncated-malformed-http-unavailable-distinct-no-listener")

    two = config(2)
    report, _, served, ready = await exercise(two,
        [dict(rows=[endpoint(41010)], truncated=True), dict(unavailable=True)])
    need(report["status"] == "INCOMPLETE_REFRESH_SERVICE_FINISHED" and
         not ready[0]["refresh_complete"] and report["contact_count"] == 1 and len(served) == 1,
         "PARTIAL_UNION_DISCLOSURE")
    report, _, served, _ = await exercise(two,
        [dict(rows=[endpoint(41010)]), dict(rows=[endpoint(41010)])])
    need(report["refresh_complete"] and report["contact_count"] == 1 and
         len(served[0]["config"]["entries"][0]["endpoints"]) == 1, "DEDUP_ROUTE_UNION")
    report, _, served, _ = await exercise(two, [dict(rows=[endpoint(41010)]), dict(rows=[])])
    need(report["refresh_complete"] and report["contact_count"] == 1, "ONE_SOURCE_CANNOT_WITHDRAW_OTHER")
    passed("partial-union-dedup-and-source-local-withdrawal")

    restricted = config(); restricted["endpoint_scopes"]["feed0"]["endpoints"] = [endpoint(41010)]
    report, _, served, _ = await exercise(restricted, [dict(rows=[endpoint(41011)])])
    slot = report["lookups"][0]
    need(slot["status"] == "ADVISORY_CONTACTS" and slot["rejected"] == 1 and
         slot["adopted"] == 0 and not report["refresh_complete"] and served == [], "REJECTION_NOT_WITHDRAWAL")
    passed("scope-rejection-is-not-valid-empty-withdrawal")

    aged = config(2); aged["refresh"].update(max_age_ms=10000, min_service_ms=4000)
    report, _, served, _ = await exercise(aged,
        [dict(rows=[endpoint(41010)], elapsed=3), dict(rows=[endpoint(41011)], elapsed=3.5)])
    need(report["lookups"][0]["status"] == "INSUFFICIENT_REMAINING_HORIZON" and
         not report["lookups"][0]["included"] and report["lookups"][1]["included"] and
         served[0]["config"]["entries"][0]["endpoints"] == [endpoint(41011)] and
         not report["refresh_complete"], "ASSEMBLY_RECHECKS_EARLIER_SLOTS")
    impossible = config(); impossible["refresh"].update(max_age_ms=1000, min_service_ms=1000)
    report, calls, served, _ = await exercise(impossible, [])
    need(report["lookups"][0]["status"] == "NO_LEGAL_ATTEMPT_SLICE" and calls == [] and
         served == [] and report["status"] == "INCOMPLETE_REFRESH_EMPTY", "NO_USELESS_DIAL")
    passed("assembly-omits-aged-slots-and-no-legal-slice-does-not-dial")


class Writer:
    def __init__(self, clock, advances=()):
        self.clock, self.advances = clock, list(advances)
        self.writes, self.drains = [], 0

    def write(self, raw):
        need(sum(map(len, self.writes))+len(raw) <= 256*1024, "WRITER_BOUND")
        self.writes.append(bytes(raw))

    async def drain(self):
        if self.drains < len(self.advances):
            self.clock[0] += self.advances[self.drains]
        self.drains += 1

    def close(self):
        pass


async def cutoff_controls(loaded):
    api = loaded.peer_api
    H, C, F = api.H, api.CD, api.F
    adapter = api.OrdinaryExportAdapter(loaded.installation.semantic_id)
    features = api.compile_query(adapter.namespace, [dict(tag="declaration-kind", value="theorem")])
    directory = C.ContactMap.from_bytes(F.compact(dict(schema=C.MAP_SCHEMA, namespace=adapter.namespace,
        entries=[dict(features=features, endpoints=[endpoint(41010)])])))
    request = dict(schema=C.REQUEST_SCHEMA, namespace=adapter.namespace, features=features,
                   nonce="7"*64, max_contacts=1, max_bytes=4096)
    expected = C.reply(directory, request)
    clock = [time.monotonic()]

    def refused(call, code):
        try:
            call()
        except ValueError as error:
            need(str(error) == code, "REFUSAL_CODE")
        else:
            raise AssertionError("REFRESH_CONTROL_EXPECTED_REFUSAL")

    def reader():
        raw = F.compact(request)
        data = H._header("POST "+C.ROUTE+" HTTP/1.1", len(raw), "127.0.0.1")+raw
        value = asyncio.StreamReader(); value.feed_data(data); value.feed_eof()
        return value

    with patch.object(H, "time", SimpleNamespace(monotonic=lambda: clock[0])):
        for value in (True, "100", float("nan"), float("inf")):
            refused(lambda v=value: H.Provider(contact_directory=directory, contact_deadline=v),
                    "CONTACT_DIRECTORY_DEADLINE")
        initial = clock[0]
        provider = H.Provider(contact_directory=directory, contact_deadline=initial+1)
        need(provider.dispatch(C.ROUTE, request) == expected, "DIRECT_LIVE")
        def caller_stop():
            raise ValueError("CALLER_STOP")
        refused(lambda: provider.dispatch(C.ROUTE, request, check_budget=caller_stop), "CALLER_STOP")
        clock[0] = initial+1
        refused(lambda: provider.dispatch(C.ROUTE, request), "CONTACT_DIRECTORY_EXPIRED")
        offer = dict(namespace=adapter.namespace, features=features, max_bytes=1024, max_expanded_bytes=1024)
        need(provider.dispatch(H.OFFER_ROUTE, offer) ==
             H.Provider(contact_directory=directory).dispatch(H.OFFER_ROUTE, offer), "NONCONTACT_UNCHANGED")
        clock[0] = initial
        def late_reply(*args, **kwargs):
            clock[0] = initial+1
            return expected
        with patch.object(C, "reply", new=late_reply):
            refused(lambda: provider.dispatch(C.ROUTE, request), "CONTACT_DIRECTORY_EXPIRED")
        passed("finite-deadline-direct-composition-expiry-noncontact-and-postreply")

        clock[0] = initial
        provider = H.Provider(contact_directory=directory, contact_deadline=initial+0.5, operation_ms=1000)
        writer = Writer(clock, [0.6])
        await provider._serve(reader(), writer)
        need(len(writer.writes) == 1 and writer.writes[0].startswith(b"HTTP/1.1 200 OK") and
             provider.reserved_reply_bytes == 0 and provider.reply_bytes == len(expected) and
             provider.failures == 1, "HEADER_DRAIN_NO_BODY_CONSERVATIVE_CHARGE")

        clock[0] = initial
        provider = H.Provider(contact_directory=directory, contact_deadline=initial+0.5, operation_ms=1000)
        incoming = reader()
        old_header = H._header
        def delayed_header(*args, **kwargs):
            result = old_header(*args, **kwargs); clock[0] = initial+0.6
            return result
        writer = Writer(clock)
        with patch.object(H, "_header", new=delayed_header):
            await provider._serve(incoming, writer)
        need(writer.writes == [] and provider.reserved_reply_bytes == 0 and
             provider.reply_bytes == len(expected) and provider.failures == 1, "PRE_ENQUEUE_GUARD")
        passed("http-preheader-and-postdrain-cutoff-preserve-charges")

        clock[0] = initial
        writer = Writer(clock, [0.6])
        def budget():
            if clock[0] >= initial+0.5:
                raise ValueError("TEST_CUTOFF")
        try:
            await H._write(writer, b"x"*(H.CHUNK+7), check_budget=budget)
        except ValueError as error:
            need(str(error) == "TEST_CUTOFF", "CHUNK_REFUSAL")
        else:
            raise AssertionError("REFRESH_CONTROL_EXPECTED_CHUNK_CUTOFF")
        need(list(map(len, writer.writes)) == [H.CHUNK], "NO_SECOND_ENQUEUE")
        passed("writer-rechecks-after-drain-before-next-chunk")

        # Default path intentionally retains predecessor behavior. No cutoff is
        # inferred merely because this provider happens to serve contacts.
        clock[0] = initial
        provider = H.Provider(contact_directory=directory, operation_ms=1000)
        writer = Writer(clock, [2])
        await provider._serve(reader(), writer)
        need(len(writer.writes) == 2 and writer.writes[1] == expected and provider.failures == 0 and
             provider.reserved_reply_bytes == 0, "DEFAULT_NO_NEW_WRITE_DEADLINE")
        passed("default-none-retains-ordinary-contact-bytes-and-write-path")

    # Test only the new start-to-READY boundary with a no-socket Provider double.
    conf = config()["service"]
    conf = dict(conf, lease_seconds=1, entries=[dict(specs=[dict(tag="declaration-kind", value="theorem")],
                                   endpoints=[endpoint(41010)])])
    start = time.monotonic(); clock = [start]; seen = []; ready = []
    class SlowProvider:
        def __init__(self, **kwargs):
            seen.append(kwargs); self.server = None; self.tasks = set(); self.reserved_reply_bytes = 0
        async def start(self, *args, **kwargs):
            clock[0] += 1.5
            return SimpleNamespace(host="127.0.0.1", port=41000, tls=False)
        async def stop(self):
            self.server = None
        def status(self):
            return dict(accepting=False, reserved_reply_bytes=0)
    with patch.object(api, "time", SimpleNamespace(monotonic=lambda: clock[0])), \
         patch.object(H, "Provider", new=SlowProvider):
        try:
            await api.directory_serve(loaded, conf, SimpleNamespace(deadline=start+60, check=check),
                ready=ready.append, contact_deadline=start+20, minimum_service_ms=1000)
        except api.PeerFailure as caught:
            need(caught.report["error"]["code"] == "REFRESH_START_TOO_LATE" and
                 caught.report["ready"] is None and caught.report["quiescent"], "LATE_START_FAILURE")
        else:
            raise AssertionError("REFRESH_CONTROL_EXPECTED_LATE_START")
    need(ready == [] and seen[0]["contact_deadline"] == start+1, "NO_LATE_READY_CLIPPED_PROVIDER")
    passed("late-provider-start-refuses-ready-and-cleans-up")


def forbidden(*args, **kwargs):
    raise AssertionError("REFRESH_CONTROL_FORBIDDEN_EXTERNAL_EFFECT")


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
    report = dict(passed=False, cases=CASES, profile_sha256=args.profile_sha256,
        scope="SCRIPTED_CHANGED_SEAMS_NOT_NETWORK_OR_MATHEMATICS")
    loop_audit = dict(count=0, contexts=[])
    try:
        loaded = load(args)
        # Event-loop setup can allocate an internal wakeup socket. Create it
        # before denying application connection/listener methods. Keep the
        # socket.socket class intact: Windows Proactor uses it in isinstance.
        loop = asyncio.new_event_loop()
        def loop_exception(_loop, context):
            loop_audit["count"] += 1
            if len(loop_audit["contexts"]) < 16:
                error = context.get("exception")
                loop_audit["contexts"].append(dict(
                    message=str(context.get("message", ""))[:500],
                    error_type=type(error).__name__ if error is not None else None,
                    error=str(error)[:500] if error is not None else None))
        loop.set_exception_handler(loop_exception)
        try:
            with ExitStack() as stack:
                for name in ("socket.socket.connect", "socket.socket.connect_ex",
                             "socket.socket.bind", "socket.socket.listen", "socket.create_connection",
                             "sqlite3.connect", "subprocess.Popen", "asyncio.open_connection"):
                    stack.enter_context(patch(name, forbidden))
                loop.run_until_complete(refresh_controls(loaded))
                loop.run_until_complete(cutoff_controls(loaded))
                # Drain already-scheduled callbacks before accepting the run;
                # this is harness settlement, not an additional test group.
                loop.run_until_complete(asyncio.sleep(0))
        finally:
            loop.close()
        need(loop_audit["count"] == 0, "UNHANDLED_LOOP_EXCEPTION")
        report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:1000])
    report.update(completed_groups=len(CASES), wall_seconds=time.monotonic()-START,
                  harness_cpu_seconds=time.process_time()-CPU,
                  unhandled_loop_exceptions=loop_audit["count"],
                  loop_exception_contexts=loop_audit["contexts"])
    save(output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Focused ownership controls; source-only until root selects one bounded run.

Real selected exchange/timeout context, scripted raw sockets and stream handoff.
No application sockets, HTTP/parser campaign, owner, database, subprocess or Lean.
"""
from __future__ import annotations

import argparse
import asyncio
from contextlib import ExitStack
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
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
        raise AssertionError("CONNECT_CONTROL_"+code)


def check():
    need(time.monotonic()-START < 30 and time.process_time()-CPU < 15, "ALLOWANCE")


def read(path):
    check()
    need(path.is_absolute() and path.is_file() and not path.is_symlink(), "INPUT")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB, "INPUT_BOUND")
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
    spec = importlib.util.spec_from_file_location("_connect_control_profile", package/"profile.py")
    module = importlib.util.module_from_spec(spec)
    need(spec.name not in sys.modules, "PRELOADED_LOADER")
    sys.modules[spec.name] = module
    exec(compile(source, str(package/"profile.py"), "exec"), module.__dict__)
    return module.load(package, args.profile_sha256,
        dict(python_runtime=args.python_runtime, lean_runtime=args.lean_runtime),
        START+30, check_parent=check)


class RawSocket:
    def __init__(self, events, mode, args, kwargs):
        self.events, self.mode, self.args, self.kwargs = events, mode, args, kwargs
        self.fd, self.closes, self.nonblocking = 71, 0, False

    def setblocking(self, value):
        self.events.append("setblocking")
        need(value is False, "NONBLOCKING_ONLY")
        if self.mode == "setblocking-error":
            raise ValueError("LOCAL_SETBLOCKING")
        self.nonblocking = True

    def close(self):
        self.events.append("raw-close")
        self.closes += 1
        if self.mode != "close-still-live":
            self.fd = -1
        if self.mode == "close-error":
            raise OSError("LOCAL_CLOSE_FAILURE")

    def fileno(self):
        self.events.append("raw-fileno")
        return self.fd


class Writer:
    def __init__(self, raw, events, mode):
        self.raw, self.events, self.mode = raw, events, mode
        self.closed, self.waited = False, False

    def close(self):
        self.events.append("writer-close")
        self.closed = True
        self.raw.fd = -1  # Scripted stream owner, not helper raw-close.

    async def wait_closed(self):
        self.events.append("writer-wait")
        self.waited = True
        if self.mode == "writer-close-error":
            raise OSError("LOCAL_WRITER_CLOSE_FAILURE")


async def controls(loaded):
    X = loaded.peer_api.X
    H = X.H
    loop = asyncio.get_running_loop()
    original_timeout_at = asyncio.timeout_at

    async def exercise(*, connect="ok", handoff="ok", raw_mode="ok",
                       response="ok", host="127.0.0.1", tls=False,
                       cancel_at=None, short=False, scope_error=False,
                       expire_after_connect=False):
        events, sockets, connects, streams, deadlines, contexts, scopes = [], [], [], [], [], [], []
        entered = asyncio.Event()
        writer_rows = []
        clock_offset = [0]
        endpoint = H.Endpoint(host, 43001, tls, "math.example" if tls else None,
                              "selected-ca.pem" if tls else None)
        original_deadline = time.monotonic()+(.02 if short else 2)

        def construct(*args, **kwargs):
            events.append("allocate")
            if raw_mode == "constructor-error":
                raise OSError("LOCAL_SOCKET_ALLOCATION")
            row = RawSocket(events, raw_mode, args, kwargs)
            sockets.append(row)
            return row

        def scope_lookup(name):
            scopes.append(name)
            if scope_error:
                raise OSError("LOCAL_SCOPE_LOOKUP")
            return 7

        fake_socket = SimpleNamespace(**vars(socket))
        fake_socket.socket = construct
        fake_socket.if_nametoindex = scope_lookup

        async def dial(raw, address):
            events.append("connect")
            connects.append((raw, address))
            need(raw in sockets and raw.nonblocking, "OWN_NONBLOCKING_SOCKET")
            if cancel_at == "connect":
                entered.set()
                await asyncio.Future()
            if connect in ("stall", "timeout-plus-external"):
                try:
                    await asyncio.Future()
                except asyncio.CancelledError:
                    if connect == "timeout-plus-external":
                        asyncio.current_task().cancel("EXTERNAL_DURING_TIMEOUT")
                    raise
                finally:
                    events.append("connect-unwound")
            if isinstance(connect, BaseException):
                raise connect
            if expire_after_connect:
                clock_offset[0] = 5

        async def stream(*args, **kwargs):
            events.append("handoff")
            streams.append((args, dict(kwargs)))
            need(not args and kwargs.get("sock") is sockets[0] and
                 "host" not in kwargs and "port" not in kwargs, "ONLY_CONNECTED_SOCKET")
            need(len(connects) == 1, "NO_EXTRA_CONNECT")
            if cancel_at == "handoff":
                entered.set()
                await asyncio.Future()
            if handoff == "stall":
                await asyncio.Future()
            if isinstance(handoff, BaseException):
                raise handoff
            writer = Writer(sockets[0], events, raw_mode)
            writer_rows.append(writer)
            return object(), writer

        async def respond(reader, writer, head, raw, maximum):
            events.append("response")
            need(writer in writer_rows and maximum == 4096, "SELECTED_RESPONSE")
            if isinstance(response, BaseException):
                raise response
            return dict(status=200, raw=b"{}", request_bytes=len(raw), reply_bytes=2, header_bytes=1)

        def context(*, cafile):
            row = SimpleNamespace(cafile=cafile, minimum_version=None)
            contexts.append(row)
            return row

        def timer(when):
            deadlines.append(when)
            return original_timeout_at(when)

        result, error = None, None
        with patch.object(X, "socket", fake_socket), patch.object(loop, "sock_connect", dial), \
             patch.object(X.asyncio, "open_connection", stream), patch.object(X, "_response", respond), \
             patch.object(X.ssl, "create_default_context", context), \
             patch.object(X.asyncio, "timeout_at", timer), \
             patch.object(X, "time", SimpleNamespace(monotonic=lambda: time.monotonic()+clock_offset[0])):
            task = asyncio.create_task(X.exchange(endpoint, H.CONTACT_DIRECTORY_ROUTE,
                dict(control="ownership"), 4096, 1000, absolute_deadline=original_deadline))
            try:
                if cancel_at is not None:
                    async with original_timeout_at(time.monotonic()+1):
                        await entered.wait()
                    task.cancel("EXTERNAL_CONTROL_CANCEL")
                try:
                    result = await task
                except BaseException as caught:
                    error = caught
            finally:
                if not task.done():
                    task.cancel("HARNESS_ABORT")
                    try:
                        await task
                    except BaseException:
                        pass
        check()
        need(all(when <= original_deadline for when in deadlines), "NO_DEADLINE_RENEWAL")
        return SimpleNamespace(result=result, error=error, sockets=sockets, connects=connects,
            streams=streams, events=events, deadlines=deadlines, contexts=contexts,
            scopes=scopes, writers=writer_rows, deadline=original_deadline)

    def raw_settled(row, reason):
        need(row.error is None and type(row.result) is X.SettledRefusal and
             row.result.reason == reason, "KNOWN_SETTLED_REASON")
        need(len(row.sockets) == len(row.connects) == 1 and not row.streams and
             row.sockets[0].closes == 1 and row.sockets[0].fd == -1, "CLOSE_BEFORE_SETTLED")
        need("raw-fileno" in row.events and row.events.index("raw-close") <
             row.events.index("raw-fileno"), "CONFIRMED_RAW_CLOSE")

    def fatal(row):
        need(row.result is None and row.error is not None, "TERMINAL_FAILURE")

    def passed(name):
        CASES.append(dict(case=name, status="PASS"))

    for host, family, address in (("127.0.0.1", socket.AF_INET, ("127.0.0.1", 43001)),
                                  ("::1", socket.AF_INET6, ("::1", 43001, 0, 0))):
        row = await exercise(host=host)
        need(row.error is None and type(row.result) is dict and row.result["status"] == 200,
             "SUCCESS_RESPONSE")
        raw = row.sockets[0]
        supplied_family = raw.kwargs.get("family", raw.args[0] if raw.args else None)
        need(supplied_family == family and row.connects[0][1] == address, "NUMERIC_FAMILY_ADDRESS")
        need(len(row.sockets) == len(row.connects) == len(row.streams) == 1 and raw.closes == 0,
             "ONE_SOCKET_SINGLE_TRANSFER")
        need(row.writers[0].closed and row.writers[0].waited and raw.fd == -1, "STREAM_OWNER_CLOSED")
    passed("one-owned-numeric-socket-and-stream-transfer-ipv4-ipv6")

    for error, reason in ((ConnectionRefusedError(), "CONNECTION_REFUSED"),
                          (ConnectionResetError(), "CONNECTION_RESET"),
                          (TimeoutError(), "ATTEMPT_TIMEOUT")):
        raw_settled(await exercise(connect=error), reason)
    passed("known-pretransfer-errors-close-before-settled-return")

    row = await exercise(connect="stall", short=True)
    raw_settled(row, "ATTEMPT_TIMEOUT")
    need("connect-unwound" in row.events and row.deadlines == [row.deadline], "OWN_TIMEOUT_ORIGINAL_DEADLINE")
    raw_settled(await exercise(expire_after_connect=True), "ATTEMPT_TIMEOUT")
    passed("own-timeout-unwinds-and-closes-without-deadline-renewal")

    row = await exercise(cancel_at="connect")
    fatal(row)
    need(type(row.error) is asyncio.CancelledError and row.error.args == ("EXTERNAL_CONTROL_CANCEL",)
         and row.sockets[0].closes == 1 and row.sockets[0].fd == -1 and not row.streams,
         "EXTERNAL_CANCEL_PROPAGATES_AFTER_CLOSE")
    row = await exercise(connect="timeout-plus-external", short=True)
    fatal(row)
    need(type(row.error) is asyncio.CancelledError and row.sockets[0].closes == 1 and
         row.sockets[0].fd == -1 and not row.streams, "ADDITIONAL_CANCEL_NOT_SWALLOWED_BY_TIMEOUT")
    row = await exercise(cancel_at="connect", raw_mode="close-error")
    fatal(row)
    need(type(row.error) is asyncio.CancelledError and type(row.error.__cause__) is
         X.UnsettledTransportError, "CANCEL_AND_FAILED_CLEANUP_BOTH_RETAINED")
    passed("external-cancellation-is-not-a-settled-timeout")

    for mode in ("close-error", "close-still-live"):
        row = await exercise(connect=ConnectionResetError(), raw_mode=mode)
        fatal(row)
        need(type(row.error) is X.UnsettledTransportError and not row.streams, "FAILED_CLOSE_TERMINAL")
    passed("close-error-or-live-descriptor-never-settles")

    error = OSError("LOCAL_UNKNOWN")
    row = await exercise(connect=error)
    fatal(row)
    need(row.error is error and row.sockets[0].closes == 1 and row.sockets[0].fd == -1,
         "UNKNOWN_ERROR_PRESERVED")
    for mode in ("constructor-error", "setblocking-error"):
        row = await exercise(raw_mode=mode)
        fatal(row)
        need(not row.connects and not row.streams, "LOCAL_SETUP_NO_DIAL")
        need(not row.sockets or (row.sockets[0].closes == 1 and row.sockets[0].fd == -1),
             "SETUP_OWNED_SOCKET_CLEANED")
    passed("unknown-and-local-setup-errors-propagate-with-owned-cleanup")

    for error in (ConnectionRefusedError(), ConnectionResetError(), TimeoutError(),
                  X.ssl.SSLError("TLS_CONTROL"), OSError("LOCAL_HANDOFF")):
        row = await exercise(handoff=error)
        fatal(row)
        need(len(row.streams) == 1 and row.sockets[0].closes == 0, "NO_RECLAIM_AFTER_TRANSFER")
    row = await exercise(handoff="stall", short=True)
    fatal(row)
    need(type(row.error) is X.UnsettledTransportError and row.sockets[0].closes == 0,
         "POSTTRANSFER_TIMEOUT_TERMINAL")
    passed("all-no-writer-posttransfer-failures-remain-terminal")

    row = await exercise(cancel_at="handoff")
    fatal(row)
    need(type(row.error) is asyncio.CancelledError and row.error.args == ("EXTERNAL_CONTROL_CANCEL",)
         and row.sockets[0].closes == 0, "POSTTRANSFER_CANCEL_PRESERVED")
    passed("external-cancellation-after-handoff-remains-terminal")

    row = await exercise(tls=True)
    need(row.error is None and len(row.contexts) == 1, "TLS_SUCCESS")
    options = row.streams[0][1]
    need(options["ssl"] is row.contexts[0] and options["server_hostname"] == "math.example" and
         options["ssl_shutdown_timeout"] == X.CLOSE_SECONDS and
         0 < options["ssl_handshake_timeout"] <= 1 and options["limit"] == H.HEADER_MAX and
         row.contexts[0].cafile == "selected-ca.pem" and
         row.contexts[0].minimum_version is X.ssl.TLSVersion.TLSv1_2, "UNCHANGED_TLS_POLICY")
    passed("tls-context-name-and-remaining-handshake-budget-preserved")

    row = await exercise(response=ConnectionResetError())
    need(row.error is None and type(row.result) is X.SettledRefusal and
         row.result.reason == "CONNECTION_RESET" and row.writers[0].closed and row.writers[0].waited,
         "WRITER_SETTLEMENT_RETAINED")
    row = await exercise(raw_mode="writer-close-error")
    fatal(row)
    need(type(row.error) is X.UnsettledTransportError, "WRITER_CLOSE_FAILURE_RETAINED")
    passed("existing-returned-writer-settlement-boundary-retained")

    for host, expected_scope, expected_lookups in (("fe80::1%3", 3, []),
                                                ("fe80::1%control0", 7, ["control0"])):
        row = await exercise(host=host, tls=True)
        need(row.error is None and row.connects[0][1] == ("fe80::1", 43001, 0, expected_scope)
             and row.scopes == expected_lookups, "IPV6_SCOPE_PRESERVED")
    row = await exercise(host="fe80::1%control0", tls=True, scope_error=True)
    fatal(row)
    need(not row.sockets and not row.connects and not row.streams, "SCOPE_FAILURE_BEFORE_ALLOCATION")
    passed("ipv6-zone-preserved-and-invalid-local-scope-does-not-dial")


def forbidden(*args, **kwargs):
    raise AssertionError("CONNECT_CONTROL_FORBIDDEN_EXTERNAL_EFFECT")


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
                  scope="SCRIPTED_OWNERSHIP_NOT_NETWORK_OR_MATHEMATICS")
    loop_audit = dict(count=0, contexts=[])
    try:
        loaded = load(args)
        loop = asyncio.new_event_loop()
        def loop_exception(_loop, context):
            loop_audit["count"] += 1
            if len(loop_audit["contexts"]) < 16:
                error = context.get("exception")
                loop_audit["contexts"].append(dict(message=str(context.get("message", ""))[:500],
                    error_type=type(error).__name__ if error is not None else None,
                    error=str(error)[:500] if error is not None else None))
        loop.set_exception_handler(loop_exception)
        try:
            with ExitStack() as stack:
                for name in ("socket.socket.connect", "socket.socket.connect_ex",
                             "socket.socket.bind", "socket.socket.listen", "socket.create_connection",
                             "sqlite3.connect", "subprocess.Popen", "asyncio.open_connection"):
                    stack.enter_context(patch(name, forbidden))
                loop.run_until_complete(controls(loaded))
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

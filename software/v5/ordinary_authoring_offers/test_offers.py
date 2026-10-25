"""Focused advisory-offer controls, selected by root before execution.

Real codec, map, provider dispatch and acquisition; synthetic inert repository
hints, mocked exchange and CLI bootstrap. No server, repository, native process
or knowledge store is opened. This is not installed/actual-network qualification.
"""
from pathlib import Path
import argparse
import asyncio
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
import socket
import sqlite3
import subprocess
import sys
import time
from types import SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PROFILE = "a8d10b6ba7048f90ae4bf2411b7662090199934380fd24b042b62ff5ceb40960"
EXPORT = "2bf543aad2166307a1fccd72250b93cb9b7ec0d7df942b1e20beb5f700c7f886"
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU < 25,
         "OFFERS_CONTROL_ORIGINAL_ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def module(name, path, expected=None):
    raw = path.read_bytes()
    need(0 < len(raw) <= 2*MIB and (expected is None or sha(raw) == expected),
         "OFFERS_CONTROL_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    exec(compile(raw, str(path), "exec"), result.__dict__)
    if "." in name:
        parent, attr = name.rsplit(".", 1)
        setattr(sys.modules[parent], attr, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "OFFERS_CONTROL_PROCESS")
    package, output = Path(args.package), Path(args.output)
    need(output.is_absolute() and output.resolve().is_relative_to(ROOT/"experiments/v5-local-checks")
         and output.parent.is_dir() and not os.path.lexists(output), "OFFERS_CONTROL_OUTPUT")
    profile_raw = (package/"PROFILE.json").read_bytes()
    need(sha(profile_raw) == PROFILE, "OFFERS_CONTROL_PROFILE")
    descriptor = json.loads(profile_raw)
    base = module("_offers_control_owner", package/"owner.py", descriptor["files"]["owner.py"]["sha256"])
    loader = base.bootstrap(package, PROFILE, check)
    loaded = loader.load(package, PROFILE,
        {"python_runtime": Path(r"D:\Python314"),
         "lean_runtime": ROOT/"software/runtime/lean-4.34.0-windows"}, START+45, check_parent=check)
    source = Path(__file__).resolve().parent
    old_h, old_o = loaded.peer_api.H, loaded.O
    AO = module("transport.authoring_offers", source/"authoring_offers.py")
    H = module("transport.http_provider", source/"http_provider.py")
    O = module("transport.ordinary_acquisition", source/"ordinary_acquisition.py")
    api = module("_offers_control_api", source/"peer_api.py")
    entry = module("_offers_control_entry", source/"peer.py")
    loaded.O, loaded.peer_api = O, api
    need(api.O is O and api.H is H and api.AO is AO and O.H is H and api.A is loaded.A,
         "OFFERS_CONTROL_SHARED_MODULES")
    raw = api.F.compact
    sid = loaded.installation.semantic_id
    encoded_name = lambda *parts: [[0, {"$bytes": list(part.encode())}] for part in parts]
    offer = {"repository": "https://example.invalid/math.git", "object_format": "sha1",
        "commit": "1"*40, "project_dir": "", "module": encoded_name("TheoryB"),
        "export_name": encoded_name("RepairTheory", "ClosureBridge", "OrderData"),
        "toolchain": "leanprover/lean4:v4.34.0"}
    second = dict(offer, commit="2"*40)
    document = {"schema": AO.MAP_SCHEMA, "entries": [
        {"semantic_id": sid, "export_id": EXPORT, "offers": [offer, second]}]}
    request = {"schema": AO.REQUEST_SCHEMA, "semantic_id": sid, "export_id": EXPORT,
               "max_offers": 8, "max_bytes": AO.REPLY_MAX}
    calls, forbidden_calls, cases = [], [], []

    def forbidden(*_, **__):
        forbidden_calls.append("FORBIDDEN")
        raise AssertionError("OFFERS_CONTROL_FORBIDDEN_STATE_EXECUTION_OR_NETWORK")

    def refusal(label, call, exact=None):
        try:
            call()
        except ValueError as error:
            if exact is not None:
                need(str(error) == exact, "OFFERS_CONTROL_WRONG_REFUSAL:"+label+":"+str(error))
            cases.append({"case": label, "status": "REFUSED", "error": str(error)})
            return
        raise AssertionError("OFFERS_CONTROL_EXPECTED_REFUSAL:"+label)

    def no_authority(reply):
        need(reply["status"] == "UNVERIFIED_AUTHORING_ASSOCIATIONS" and
             reply["mathematical_acceptance"] is False and reply["execution_approved"] is False and
             reply["global_complete"] is False and reply["source_availability"] == "NOT_CHECKED" and
             reply["correspondence"] == "NOT_CHECKED", "OFFERS_CONTROL_AUTHORITY")

    index = AO.OfferMap.from_bytes(raw(document), check_budget=check)
    full = AO.read_reply(index.reply(request, check_budget=check), request)
    need(full["offers"] == [offer, second] and full["truncated"] is False,
         "OFFERS_CONTROL_EXACT_SYNTHETIC_HINTS")
    no_authority(full)
    # Parsed map output cannot mutate the retained encoded rows.
    full["offers"][0]["repository"] = "https://changed.invalid/repo"
    need(AO.read_reply(index.reply(request), request)["offers"][0] == offer,
         "OFFERS_CONTROL_IMMUTABLE_SNAPSHOT")
    count_request = dict(request, max_offers=1)
    limited = AO.read_reply(index.reply(count_request), count_request)
    need(limited["offers"] == [offer] and limited["truncated"], "OFFERS_CONTROL_COUNT_PREFIX")
    absent_request = dict(request, export_id="f"*64)
    empty = AO.read_reply(index.reply(absent_request), absent_request)
    no_authority(empty)
    need(not empty["offers"] and empty["truncated"] is False, "OFFERS_CONTROL_LOCAL_ABSENCE_ONLY")
    byte_request = dict(request, max_bytes=len(raw(dict(empty, export_id=EXPORT, truncated=True)))+1)
    tiny = AO.read_reply(index.reply(byte_request), byte_request)
    need(tiny["offers"] == [] and tiny["truncated"], "OFFERS_CONTROL_BYTE_PREFIX")
    cases.append({"case": "canonical-map-exact-empty-truncation-and-defensive-output", "status": "PASS"})
    refusal("envelope-does-not-fit", lambda: index.reply(dict(request, max_bytes=1)))
    for label, key, value in (
        ("http-repository", "repository", "http://example.invalid/math.git"),
        ("credentialed-repository", "repository", "https://user:secret@example.invalid/math.git"),
        ("query-repository", "repository", "https://example.invalid/math.git?token=x"),
        ("fragment-repository", "repository", "https://example.invalid/math.git#main"),
        ("relative-parent", "project_dir", "../escape"),
        ("absolute-project", "project_dir", "/escape"),
        ("backslash-project", "project_dir", "a\\b"),
        ("branch-not-commit", "commit", "main"),
        ("bad-object-format", "object_format", "sha512"),
        ("oversized-toolchain", "toolchain", "x"*4096),
        ("invalid-module-name", "module", [True]),
    ):
        malformed = deepcopy(document); malformed["entries"][0]["offers"][0][key] = value
        refusal(label, lambda d=malformed: AO.OfferMap.from_bytes(raw(d)))
    duplicate = deepcopy(document); duplicate["entries"].append(deepcopy(duplicate["entries"][0]))
    refusal("duplicate-map-key", lambda: AO.OfferMap.from_bytes(raw(duplicate)))
    duplicate = deepcopy(document); duplicate["entries"][0]["offers"] = [offer, offer]
    refusal("duplicate-offer", lambda: AO.OfferMap.from_bytes(raw(duplicate)))
    oversized = deepcopy(document); oversized["entries"][0]["offers"] = [dict(offer, commit=str(i)*40) for i in range(9)]
    refusal("ninth-offer", lambda: AO.OfferMap.from_bytes(raw(oversized)))
    refusal("raw-map-byte-cap", lambda: AO.OfferMap.from_bytes(b" "*(AO.MAP_MAX+1)))
    refusal("noncanonical-map", lambda: AO.OfferMap.from_bytes(raw(document)+b"\n"))
    bad_reply = AO.read_reply(index.reply(request), request); bad_reply["semantic_id"] = "0"*64
    refusal("wrong-reply-key", lambda: AO.read_reply(raw(bad_reply), request))
    bad_reply = AO.read_reply(index.reply(request), request); bad_reply["execution_approved"] = True
    refusal("execution-claim-refused", lambda: AO.read_reply(raw(bad_reply), request))
    refusal("boolean-count", lambda: AO.request_limit(dict(request, max_offers=True)))
    provider = H.Provider(authoring_offers=index)
    absent_provider = H.Provider(index=object())
    refusal("role-absent", lambda: absent_provider.dispatch(AO.ROUTE, request), "ROLE_NOT_SERVED")
    inert_store = object.__new__(O.OrdinaryStore)
    refusal("offers-not-custody", lambda: O.serve(inert_store, AO.ROUTE, request), "AUTHORING_OFFERS_NOT_CUSTODY")
    need(H.AUTHORING_OFFERS_ROUTE == AO.ROUTE == O.AUTHORING_OFFERS_ROUTE and
         H.ROUTES[AO.ROUTE] == AO.REPLY_MAX and AO.ROUTE not in H.ORDINARY_ROUTES,
         "OFFERS_CONTROL_ROUTE_ROLE_SEPARATION")
    mode = "good"

    async def exchange(endpoint, route, value, maximum, milliseconds):
        calls.append({"route": route, "request": deepcopy(value), "maximum": maximum})
        need(route == AO.ROUTE and milliseconds > 0, "OFFERS_CONTROL_ONE_ROUTE")
        if mode == "reset":
            raise ConnectionResetError()
        if mode == "cancel":
            raise asyncio.CancelledError()
        data = provider.dispatch(route, value, check_budget=check)
        if mode == "wrong-key":
            changed = json.loads(data); changed["export_id"] = "0"*64; data = raw(changed)
        if mode == "tamper":
            data = data[:-1]+b"!"
        need(len(data) <= maximum, "OFFERS_CONTROL_TRANSPORT_CAP")
        return {"status": 503 if mode == "http-error" else 200, "raw": data,
                "request_bytes": len(raw(value)), "reply_bytes": len(data), "header_bytes": 80}

    allowance = NS(deadline=START+45, check=check, operation=forbidden, account=forbidden)
    config = {"contacts": {"fixture": {"host": "127.0.0.1", "port": 12345, "tls": False,
        "server_name": None, "ca_file": None, "ca_sha256": None}},
        "selection": {"provider": "fixture", "export_id": EXPORT},
        "limits": {"requests": 1, "reply_bytes": AO.REPLY_MAX, "max_offers": 8}}

    async def exercise(label, selected=None, ledger=None, fails=False, count=1):
        before = len(calls); supplied = deepcopy(config if selected is None else selected)
        original = deepcopy(supplied)
        try:
            result = await api.authoring_offers(loaded, supplied, allowance, network_budget=ledger)
            need(not fails, "OFFERS_CONTROL_EXPECTED_API_REFUSAL:"+label)
        except api.PeerFailure as error:
            need(fails, "OFFERS_CONTROL_UNEXPECTED_API_REFUSAL:"+str(error.report))
            result = error.report
        need(supplied == original and len(calls)-before == count, "OFFERS_CONTROL_IO_OR_MUTATION:"+label)
        need(result["mathematical_acceptance"] is False and result["execution_approved"] is False and
             result["source_availability_verified"] is False and result["project_correspondence_verified"] is False,
             "OFFERS_CONTROL_API_AUTHORITY")
        if not fails:
            no_authority(result["reply"])
            need(result["reply"]["offers"] == [offer, second], "OFFERS_CONTROL_API_CONTENT")
        if result["network"] is not None:
            need(result["network"]["pending_requests"] == 0, "OFFERS_CONTROL_SETTLED_TICKET")
        need(json.loads(raw(result)) == result, "OFFERS_CONTROL_JSON_OUTPUT")
        cases.append({"case": label, "status": result["status"], "network": result["network"]})
        return result

    async def api_cases():
        nonlocal mode
        class MemoryWriter:
            def __init__(self):
                self.parts, self.closed = [], False
            def write(self, data):
                self.parts.append(bytes(data))
            async def drain(self):
                pass
            def close(self):
                self.closed = True
            async def wait_closed(self):
                pass

        async def handle(label, cap, succeeds):
            # Exercise the changed wire reservation/byte-output branch without
            # binding a server or opening a socket. This is not actual HTTP I/O.
            selected = H.Provider(authoring_offers=index, max_reply_bytes=cap)
            reader, writer = asyncio.StreamReader(), MemoryWriter()
            body = raw(request)
            reader.feed_data(H._header("POST "+AO.ROUTE+" HTTP/1.1", len(body),
                                       "127.0.0.1:12345")+body)
            reader.feed_eof()
            await selected._serve(reader, writer)
            status = selected.status()
            need(writer.closed and not status["reserved_reply_bytes"] and not status["active"],
                 "OFFERS_CONTROL_HANDLER_CLOSED")
            if succeeds:
                header, delivered = b"".join(writer.parts).split(b"\r\n\r\n", 1)
                need(header.startswith(b"HTTP/1.1 200 OK") and delivered == index.reply(request)
                     and status["reply_bytes"] == len(delivered) and status["failures"] == 0,
                     "OFFERS_CONTROL_HANDLER_EXACT_BYTES")
            else:
                need(not writer.parts and status["failures"] == 1 and status["reply_bytes"] == 0,
                     "OFFERS_CONTROL_HANDLER_CAP_REFUSAL")
            cases.append({"case": label, "status": "PASS", "provider": status})

        await handle("memory-handler-byte-output", AO.REPLY_MAX, True)
        await handle("memory-handler-quota-before-dispatch", 1024, False)
        result = await exercise("one-exact-advisory-lookup")
        need(result["network"]["closed"] and result["network"]["requests"] == 1 and
             result["network"]["charged_reply_bytes"] == result["reply_bytes"], "OFFERS_CONTROL_OWNED_LEDGER")
        for mode in ("reset", "cancel", "wrong-key", "tamper", "http-error"):
            result = await exercise(mode, fails=True)
            need(result["network"]["closed"] and result["network"]["charged_reply_bytes"] == AO.REPLY_MAX,
                 "OFFERS_CONTROL_FAILED_RESERVATION")
        mode = "good"
        ledger = O.OrdinaryBudget(deadline=START+44, requests=2, reply_bytes=AO.REPLY_MAX+100)
        ledger.charge_external("earlier-search", 1, 100)
        deadline = ledger.deadline
        await exercise("shared-ledger-no-renewal", ledger=ledger)
        need(not ledger.closed and ledger.requests == 2 and ledger.deadline <= deadline,
             "OFFERS_CONTROL_SHARED_OWNERSHIP")
        await exercise("spent-ledger-before-io", ledger=ledger, fails=True, count=0); ledger.close()
        for label, change in (("extra-field", lambda c: c.update(custody="forbidden")),
                ("two-requests", lambda c: c["limits"].update(requests=2)),
                ("oversized-reply", lambda c: c["limits"].update(reply_bytes=AO.REPLY_MAX+1))):
            bad = deepcopy(config); change(bad)
            await exercise(label, selected=bad, fails=True, count=0)

    output.mkdir()
    with ExitStack() as stack:
        for obj, key in ((sqlite3, "connect"), (subprocess, "Popen"), (socket, "create_connection"),
                (asyncio, "open_connection"), (loaded.A.OrdinaryAdmission, "open"),
                (O.OrdinaryStore, "__init__"), (old_o.OrdinaryStore, "__init__"),
                (H.Provider, "start"), (old_h.Provider, "start"),
                (sys.modules["transport.clients"], "exchange")):
            stack.enter_context(patch.object(obj, key, forbidden))
        stack.enter_context(patch.object(H, "exchange", exchange))
        asyncio.run(api_cases())
        stack.enter_context(patch.object(entry, "bootstrap_owner", lambda *a: base))
        facade_loader = NS(hexid=loader.hexid, owner_json=loader.owner_json, load=lambda *a, **kw: loaded)
        stack.enter_context(patch.object(base, "bootstrap", lambda *a: facade_loader))
        config_path = output/"config.json"
        with config_path.open("xb") as stream:
            stream.write(raw(config))
        cli = NS(operation="authoring-offers", profile_sha256=PROFILE, python_runtime=r"D:\Python314",
            lean_runtime=str(ROOT/"software/runtime/lean-4.34.0-windows"), config=str(config_path),
            config_sha256=sha(raw(config)), output=str(output/"facade"), wall_seconds=55,
            cpu_seconds=30, memory_mib=512, catalog=None, custody=None, store_id=None, custody_limits=None)
        result, encoded = entry.run(cli)
        need(result["ok"] and json.loads(encoded) == result and
             result["result"]["reply"]["offers"] == [offer, second], "OFFERS_CONTROL_FACADE")
        cases.append({"case": "state-free-facade", "status": "PASS"})
        for field in ("catalog", "custody", "store_id", "custody_limits"):
            bad = deepcopy(cli); setattr(bad, field, "forbidden"); bad.output = str(output/("reject-"+field))
            before = len(calls); result, _ = entry.run(bad)
            need(not result["ok"] and result["error"] == "PEER_OPERATION_STATE_ARGUMENTS" and
                 len(calls) == before and not Path(bad.output).exists(), "OFFERS_CONTROL_STATE_REFUSAL")
            cases.append({"case": "state-refused-"+field, "status": "PASS"})
        need(not forbidden_calls, "OFFERS_CONTROL_NO_FORBIDDEN_CALLS")
    check()
    result = {"status": "PASS_ADVISORY_OFFERS_REAL_CODEC_MOCKED_EXCHANGE", "case_count": len(cases),
        "cases": cases, "exchange_calls": calls, "forbidden_calls": forbidden_calls,
        "profile_sha256": PROFILE, "repository": "SYNTHETIC_NOT_ACCESSED_OR_AVAILABLE",
        "transport": "MOCKED_EXCHANGE_REAL_PROVIDER_DISPATCH", "facade": "MOCKED_BOOTSTRAP",
        "mathematical_acceptance": False, "execution_approved": False,
        "wall_seconds": time.monotonic()-START, "controller_cpu_seconds": time.process_time()-CPU}
    with (output/"RESULT.json").open("xb") as stream:
        stream.write(raw(result))
    print(json.dumps({"status": result["status"], "case_count": len(cases)}), flush=True)


if __name__ == "__main__":
    main()

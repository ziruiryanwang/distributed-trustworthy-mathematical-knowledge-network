"""Six isolated controls for one explicitly selected ordinary-peer package.

Loads the exact package once; never opens an owner/custody/index, invokes native
checking, binds a provider, fetches a peer or copies package/state. Narrow mocks
replace only state binding and I/O dispatch at the documented control boundaries.
Root must select this source and its outer finite process envelope before use.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
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
import stat
import subprocess
import sys
from unittest.mock import patch

MIB = 1024**2


def need(value, code):
    if not value:
        raise AssertionError(code)


class Allowance:
    deadline = START_WALL+50

    def check(self):
        need(time.monotonic() < self.deadline and time.process_time()-START_CPU < 30,
             "CONTROL_ORIGINAL_ALLOWANCE")

    def operation(self, _):
        raise AssertionError("CONTROL_UNEXPECTED_NATIVE_ALLOCATION")

    def account(self, _):
        raise AssertionError("CONTROL_UNEXPECTED_NATIVE_CHARGE")


def forbidden(*_, **__):
    raise AssertionError("CONTROL_FORBIDDEN_STATE_NATIVE_OR_NETWORK")


def read(path, maximum=2*MIB):
    need(path.is_absolute() and ".." not in path.parts, "CONTROL_ABSOLUTE_PATH")
    for item in (*reversed(path.parents), path):
        info = item.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             (getattr(info, "st_file_attributes", 0) & 0x400), "CONTROL_REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if item != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "CONTROL_REGULAR_FILE")
    need(0 < path.stat().st_size <= maximum, "CONTROL_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == path.stat().st_size and len(raw) <= maximum, "CONTROL_FILE_CHANGED")
    return raw


def selected_package(args, allowance):
    root = Path(args.package)
    raw = read(root/"PROFILE.json")
    need(hashlib.sha256(raw).hexdigest() == args.profile_sha256, "CONTROL_PROFILE_PIN")
    descriptor = json.loads(raw)
    entry = read(root/"peer.py")
    pin = descriptor["files"]["peer.py"]
    need(len(entry) == pin["bytes"] and hashlib.sha256(entry).hexdigest() == pin["sha256"],
         "CONTROL_PEER_ENTRY_PIN")
    name = "_dmkn_peer_controls_entry"
    need(name not in sys.modules, "CONTROL_PRELOADED_ENTRY")
    spec = importlib.util.spec_from_file_location(name, root/"peer.py")
    peer = importlib.util.module_from_spec(spec)
    sys.modules[name] = peer
    exec(compile(entry, str(root/"peer.py"), "exec"), peer.__dict__)
    base = peer.bootstrap_owner(root, args.profile_sha256, allowance.check)
    loader = base.bootstrap(root, args.profile_sha256, allowance.check)
    loaded = loader.load(root, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        allowance.deadline, check_parent=allowance.check)
    need(loaded.peer_api.A is loaded.A and loaded.peer_api.O is loaded.O,
         "CONTROL_SHARED_CORE_IDENTITY")
    return peer, loader, loaded


def refuses(code, call):
    try:
        call()
    except ValueError as error:
        need(str(error) == code, "CONTROL_WRONG_REFUSAL:"+str(error))
        return error
    raise AssertionError("CONTROL_EXPECTED_REFUSAL:"+code)


def peer_refuses(api, code, coroutine):
    error = refuses(code, lambda: asyncio.run(coroutine))
    need(type(error) is api.PeerFailure and error.report["status"] == "FAILED"
         and error.report["error"]["code"] == code, "CONTROL_PARTIAL_FAILURE_REPORT")
    return error.report


def contact(**changes):
    return {"p": {"host": "127.0.0.1", "port": 41001, "tls": False,
                  "server_name": None, "ca_file": None, "ca_sha256": None, **changes}}


def minima(bounds):
    return {key: interval[0] for key, interval in bounds.items()}


def controls(peer, loader, loaded, allowance):
    api = loaded.peer_api

    def json_contract():
        need(loader.owner_json(b' { "ok": true, "ca": null, "seconds": 10 }\n') ==
             {"ok": True, "ca": None, "seconds": 10}, "CONTROL_NORMAL_OWNER_JSON")
        refuses("OWNER_PROFILE_JSON_DUPLICATE", lambda: loader.owner_json(b'{"x":1,"x":2}'))
        for raw in (b'{"x":1.5}', b'{"x":NaN}', b'{"x":Infinity}'):
            refuses("OWNER_PROFILE_JSON_NUMBER", lambda raw=raw: loader.owner_json(raw))

    def contact_policy():
        endpoints, pins = api._contacts(contact(), allowance.check)
        need(endpoints["p"].tls is False and pins == [], "CONTROL_LOOPBACK_CONTACT")
        refuses("REMOTE_TLS_REQUIRED", lambda: api._contacts(contact(host="192.0.2.1"), allowance.check))
        refuses("PEER_CA_PIN_PAIR", lambda: api._contacts(contact(tls=True,
            ca_file=str(loaded.root/"peer.py")), allowance.check))
        refuses("PEER_FILE_PIN", lambda: api._contacts(contact(tls=True,
            ca_file=str(loaded.root/"peer.py"), ca_sha256="0"*64), allowance.check))
        # File selection only: this is deliberately NOT a TLS certificate/handshake test.
        digest = loaded.descriptor["files"]["peer.py"]["sha256"]
        endpoints, pins = api._contacts(contact(tls=True, ca_file=str(loaded.root/"peer.py"),
            ca_sha256=digest), allowance.check)
        need(endpoints["p"].tls and len(pins) == 1, "CONTROL_CA_EXACT_FILE_SELECTION")
        endpoints, pins = api._contacts(contact(host="192.0.2.1", tls=True), allowance.check)
        need(endpoints["p"].ca_file is None and not pins, "CONTROL_EXPLICIT_SYSTEM_CA")

    def receive_config(**changes):
        limits = minima(api.RECEIVE_LIMITS)
        return {"contacts": contact(), "selection": {"provider": "p", "snapshot_id": "1"*64,
                "record": {}}, "parent_root": "2"*64, "limits": limits, **changes}

    def malformed_boundaries():
        limits = minima(api.RECEIVE_LIMITS)
        refuses("PEER_RECEIVE_LIMITS", lambda: api._limits({}, api.RECEIVE_LIMITS, "PEER_RECEIVE_LIMITS"))
        for bad in (0, True, api.RECEIVE_LIMITS["requests"][1]+1):
            changed = dict(limits, requests=bad)
            refuses("PEER_RECEIVE_LIMITS:requests", lambda: api._limits(
                changed, api.RECEIVE_LIMITS, "PEER_RECEIVE_LIMITS"))
        peer_refuses(api, "PEER_RECEIVE_FIELDS", api.receive(loaded, None, None, {}, allowance))
        # Only owner binding is replaced; validation still uses the real loaded
        # semantic profile and rejects before operation allocation or acquisition.
        with patch.object(api, "_state", lambda *_: None):
            report = peer_refuses(api, "RECORD_SCHEMA", api.receive(
                loaded, None, None, receive_config(), allowance))
        need(report["admission"] is None and report["network"] is None,
             "CONTROL_MALFORMED_RECORD_NO_ACCEPTANCE_OR_NETWORK")

    def shared_search_grant():
        limits = minima(api.SEARCH_LIMITS)
        limits.update(requests=2, bytes=4096, wall_ms=10000)
        config = {"contacts": contact(), "providers": ["p"],
            "specs": [{"tag": "declaration-kind", "value": "theorem"}],
            "limits": limits, "offer": {"max_bytes": 1024, "max_expanded_bytes": 1024,
            "max_age_ms": 1000}, "page": minima(api.CQ.LIMITS)}
        ledger = loaded.O.OrdinaryBudget(deadline=allowance.deadline-5, requests=3, reply_bytes=8192)
        original_deadline = ledger.deadline
        calls = []
        async def stop_at_offer(client, provider, **_):
            need(ledger.requests == 2 and ledger.reply_bytes == 4096,
                 "CONTROL_SEARCH_NOT_PREPAID")
            calls.append(provider)
            raise ValueError("CONTROL_OFFER_STOP")
        try:
            with patch.object(api.SearchClient, "offer", stop_at_offer):
                report = peer_refuses(api, "CONTROL_OFFER_STOP",
                    api.find(loaded, config, allowance, network_budget=ledger))
            need(calls == ["p"] and report["network"]["requests"] == 2 and not ledger.closed,
                 "CONTROL_SEARCH_FAILURE_RETAINED_PREPAY")
            reused, owns = api._network(allowance, 3, 8192, ledger, original_deadline+1)
            need(reused is ledger and not owns and ledger.deadline <= original_deadline and
                 ledger.requests == 2 and ledger.reply_bytes == 4096, "CONTROL_NO_GRANT_RENEWAL")
            with patch.object(api, "_state", lambda *_: None):
                wrong = receive_config()
                wrong["limits"].update(requests=1, reply_bytes=4096)
                peer_refuses(api, "PEER_RECEIVE_SHARED_GRANT", api.receive(
                    loaded, None, None, wrong, allowance, network_budget=ledger))
                exact = receive_config()
                exact["limits"].update(requests=3, reply_bytes=8192)
                peer_refuses(api, "RECORD_SCHEMA", api.receive(
                    loaded, None, None, exact, allowance, network_budget=ledger))
            ticket = ledger.begin(4096)
            ledger.settle(ticket)  # A failed dispatch consumes its full reserved cap.
            refuses("ORDINARY_AGGREGATE_BUDGET", lambda: ledger.begin(1))
            need(ledger.requests == 3 and ledger.reply_bytes == 8192,
                 "CONTROL_SHARED_GRANT_CONSUMPTION")
        finally:
            ledger.close()

    def partial_effect_reporting():
        accepted = {"status": "CHECKED", "local_root": "3"*64, "units_checked": 1,
                    "retained_unit_ids": ["4"*64]}
        def exhausted():
            raise ValueError("OWNER_ORIGINAL_ALLOCATION_EXHAUSTED")
        failure = api._failure({"admission": accepted}, ValueError("CONTROL_AFTER_ADMISSION"))
        original = {"ok": False, "phase": "RECEIVE", "detail": failure.report, "cost": {}}
        reported, raw = peer.terminal_report(original, None, "receive", exhausted)
        need(reported["phase"] == "REPORT" and reported["accepted"] == accepted and
             json.loads(raw)["accepted"]["local_root"] == accepted["local_root"],
             "CONTROL_PARTIAL_ADMISSION_LOST")
        reused = dict(accepted, status="REUSED", units_checked=0)
        reported, _ = peer.terminal_report({"ok": True, "result": {"admission": reused},
            "cost": {}}, {"admission": reused}, "receive", exhausted)
        need(reported["accepted"] == reused, "CONTROL_LOCAL_REUSE_LOST")
        publication = {"new": True, "record_id": "5"*64, "snapshot_id": "6"*64,
                       "mathematical_acceptance": False, "record": {"large": "x"*4096}}
        with patch.object(peer, "MAX_REPORT_BYTES", 2048):
            reported, raw = peer.terminal_report({"ok": False, "cost": {}, "detail":
                {"publications": [publication], "local_context": "7"*64}}, None, "publish")
        need(len(raw) <= 2048 and reported["publications"][0]["record_id"] == "5"*64 and
             "record" not in reported["publications"][0] and reported["local_context"] == "7"*64,
             "CONTROL_PARTIAL_PUBLICATION_LOST")

    def service_scope():
        config = {"index": {"path": str(loaded.root), "limits": minima(api.DS.LIMITS), "create": False},
            "host": "127.0.0.1", "port": 0, "tls": None, "lease_seconds": 1, "cleanup_seconds": 10,
            "limits": minima(api.PROVIDER_LIMITS), "share_all_custody": True, "exclusive": True}
        with patch.object(api, "_state", lambda *_: None):
            for field in ("share_all_custody", "exclusive"):
                bad = dict(config, **{field: False})
                peer_refuses(api, "PEER_EXPLICIT_FULL_CUSTODY_EXCLUSIVE_SCOPE",
                    api.serve(loaded, None, bad, allowance))
            peer_refuses(api, "PEER_SERVICE_LEASE", api.serve(
                loaded, None, dict(config, lease_seconds=1.5), allowance))
            peer_refuses(api, "PEER_SERVICE_CLEANUP_RESERVE", api.serve(
                loaded, None, dict(config, cleanup_seconds=9), allowance))
            bad = deepcopy(config); bad["index"]["create"] = True
            peer_refuses(api, "PEER_SERVICE_EXISTING_INDEX", api.serve(loaded, None, bad, allowance))
            peer_refuses(api, "PEER_REMOTE_TLS_REQUIRED", api.serve(
                loaded, None, dict(config, host="192.0.2.1"), allowance))

    return [("owner-json", json_contract), ("explicit-contact-policy", contact_policy),
            ("malformed-peer-boundaries", malformed_boundaries),
            ("shared-find-receive-grant", shared_search_grant),
            ("partial-effects-reporting", partial_effect_reporting),
            ("service-scope", service_scope)]


def main(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTROL_PYTHON_PROFILE")
    allowance = Allowance()
    peer, loader, loaded = selected_package(args, allowance)
    output = loaded.A.C.ordinary(Path(args.output), directory=True)
    for protected in (loaded.root, *loaded.installation.runtime_roots.values()):
        need(not output.is_relative_to(protected) and not protected.is_relative_to(output),
             "CONTROL_OUTPUT_OVERLAP")
    rows = []
    # Guards prevent the test seam from accidentally reaching real external work.
    # asyncio's own local event-loop wakeup socket is not a peer connection.
    with ExitStack() as guards:
        guards.enter_context(patch.object(sqlite3, "connect", forbidden))
        guards.enter_context(patch.object(subprocess, "Popen", forbidden))
        guards.enter_context(patch.object(loaded.peer_api.H, "exchange", forbidden))
        guards.enter_context(patch.object(sys.modules["transport.clients"], "exchange", forbidden))
        guards.enter_context(patch.object(loaded.peer_api.H.Provider, "start", forbidden))
        for name, control in controls(peer, loader, loaded, allowance):
            allowance.check()
            try:
                control(); allowance.check()
                rows.append({"group": name, "ok": True})
            except BaseException as error:
                rows.append({"group": name, "ok": False, "error_type": type(error).__name__,
                             "error": str(error)[:1000]})
    report = {"ok": len(rows) == 6 and all(row["ok"] for row in rows), "groups": rows,
        "profile_sha256": args.profile_sha256, "implementation_id": loaded.installation.implementation_id,
        "semantic_id": loaded.installation.semantic_id, "wall_seconds": time.monotonic()-START_WALL,
        "controller_cpu_seconds": time.process_time()-START_CPU, "native_operations": 0,
        "claim": "MOCKED_BOUNDARY_CONTROLS_NOT_NETWORK_NATIVE_OR_WHOLE_V5_QUALIFICATION"}
    raw = json.dumps(report, sort_keys=True, allow_nan=False, separators=(",", ":")).encode("utf-8")
    with (output/"CONTROLS.json").open("xb") as stream:
        stream.write(raw+b"\n")
    sys.stdout.buffer.write(raw+b"\n"); sys.stdout.buffer.flush()
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    raise SystemExit(main(parser.parse_args()))

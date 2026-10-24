"""Focused preview controls: real record validation, explicitly inert transport.

Load the already selected package without opening any state. Only the new API
and facade come from the runner's immutable source snapshot. Network exchange is
a test double; database/native/evidence/locator calls are forbidden. Facade
bootstrap is an explicit double after the real one-time package load. This is
not actual HTTP, independently hosted operation or mathematical acceptance.
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
import sqlite3
import subprocess
import sys
import time
from types import SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PROFILE = "aab7e2460c0879d0fbb2b570470984efe2a66c4a932f5725ce563a1df7c2530f"
PREVIEW_SHA = "362292c8237bd4cf0f9127ed5575723f188b51efa7ab0a784ac0bf1c1489193c"
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU < 25,
         "PREVIEW_CONTROLS_ORIGINAL_ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def raw(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def module(name, path, expected=None):
    data = path.read_bytes()
    need(len(data) <= 2*MIB and (expected is None or sha(data) == expected),
         "PREVIEW_CONTROL_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    exec(compile(data, str(path), "exec"), value.__dict__)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "preview", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "PREVIEW_CONTROL_PROCESS")
    package, output = Path(args.package), Path(args.output)
    need(output.is_absolute() and output.resolve().is_relative_to(ROOT/"experiments/v5-local-checks")
         and output.parent.is_dir() and not os.path.lexists(output), "PREVIEW_CONTROL_OUTPUT")
    profile_raw = (package/"PROFILE.json").read_bytes()
    need(sha(profile_raw) == PROFILE, "PREVIEW_CONTROL_PROFILE")
    profile = json.loads(profile_raw)
    base = module("_preview_control_owner", package/"owner.py", profile["files"]["owner.py"]["sha256"])
    loader = base.bootstrap(package, PROFILE, check)
    loaded = loader.load(package, PROFILE,
        {"python_runtime": Path(r"D:\Python314"),
         "lean_runtime": ROOT/"software/runtime/lean-4.34.0-windows"}, START+45, check_parent=check)
    source = Path(__file__).resolve().parent
    api = module("_preview_control_api", source/"peer_api.py")
    entry = module("_preview_control_entry", source/"peer.py")
    need(api.A is loaded.A and api.O is loaded.O, "PREVIEW_CONTROL_SHARED_HELPERS")
    loaded.peer_api = api
    preview_raw = Path(args.preview).read_bytes()
    need(sha(preview_raw) == PREVIEW_SHA, "PREVIEW_CONTROL_FIXTURE")
    adapter = api.OrdinaryExportAdapter(loaded.installation.semantic_id)
    record = adapter.extract(preview_raw)
    selection = {"provider": "fixture", "snapshot_id": "1"*64, "record": record}
    config = {"contacts": {"fixture": {"host": "127.0.0.1", "port": 12345,
        "tls": False, "server_name": None, "ca_file": None, "ca_sha256": None}},
        "selection": selection, "limits": {"requests": 1, "reply_bytes": len(preview_raw)}}
    calls, forbidden_calls, cases = [], [], []
    exchange_mode = "good"
    expected_object_sha = record["object_sha256"]

    def forbidden(*_, **__):
        forbidden_calls.append("FORBIDDEN")
        raise AssertionError("PREVIEW_CONTROL_FORBIDDEN_SIDE_EFFECT")

    async def exchange(endpoint, route, request, maximum, milliseconds):
        calls.append({"route": route, "request": deepcopy(request), "maximum": maximum})
        need(route == api.O.PREVIEW_ROUTE and maximum == len(preview_raw) and
             request == {"schema": api.O.PREVIEW_REQUEST,
                         "object_sha256": expected_object_sha, "object_bytes": len(preview_raw)} and milliseconds > 0,
             "PREVIEW_CONTROL_ONLY_EXACT_PREVIEW_ROUTE")
        if exchange_mode == "cancel":
            raise asyncio.CancelledError()
        data = preview_raw if exchange_mode not in ("tamper", "malformed") else preview_raw[:-1]+b"!"
        return {"status": 503 if exchange_mode == "http-failure" else 200,
                "raw": data, "request_bytes": 40, "reply_bytes": len(data), "header_bytes": 80}

    allowance = NS(deadline=START+45, check=check, operation=forbidden, account=forbidden)

    async def exercise(label, selected=None, *, ledger=None, failure=None, count=1):
        before = len(calls)
        original = deepcopy(config if selected is None else selected)
        supplied = deepcopy(original)
        outcome = None
        try:
            outcome = await api.preview(loaded, supplied, allowance, network_budget=ledger)
            need(failure is None, "PREVIEW_CONTROL_EXPECTED_FAILURE:"+label)
        except api.PeerFailure as error:
            need(failure is not None, "PREVIEW_CONTROL_UNEXPECTED_FAILURE:"+str(error.report))
            outcome = error.report
            if failure != "any":
                need(outcome["error"]["code"] == failure, "PREVIEW_CONTROL_FAILURE_CODE:"+label)
        need(supplied == original and len(calls)-before == count, "PREVIEW_CONTROL_INPUT_OR_IO:"+label)
        need(outcome["mathematical_acceptance"] is False and
             outcome["evidence_bound"] is False and outcome["snapshot_membership_reverified"] is False,
             "PREVIEW_CONTROL_NO_AUTHORITY:"+label)
        if failure is None:
            need(outcome["status"] == "PREVIEW_BOUND_NOT_ACCEPTED" and
                 outcome["selection"] == original["selection"] and outcome["preview_sha256"] == PREVIEW_SHA and
                 outcome["preview_bytes"] == len(preview_raw) and
                 raw(outcome["preview"]) == preview_raw, "PREVIEW_CONTROL_EXACT_OUTPUT:"+label)
        cases.append({"case": label, "outcome": outcome, "requests": len(calls)-before})
        return outcome

    async def api_cases():
        nonlocal exchange_mode, expected_object_sha
        good = await exercise("complete-type-bound-without-proof")
        need(good["network"]["closed"] is True and good["network"]["requests"] == 1 and
             good["network"]["charged_reply_bytes"] == len(preview_raw), "PREVIEW_CONTROL_OWNED_ACCOUNTING")
        for mode in ("tamper", "http-failure", "cancel"):
            exchange_mode = mode
            outcome = await exercise(mode, failure="any")
            need(outcome["network"]["closed"] is True and outcome["network"]["pending_requests"] == 0 and
                 outcome["network"]["charged_reply_bytes"] == len(preview_raw), "PREVIEW_CONTROL_FAILURE_CHARGED")
        exchange_mode = "good"
        unverified_snapshot = deepcopy(config)
        unverified_snapshot["selection"]["snapshot_id"] = "2"*64
        await exercise("snapshot-label-not-membership-proof", unverified_snapshot)
        malformed = deepcopy(config)
        expected_object_sha = sha(preview_raw[:-1]+b"!")
        malformed["selection"]["record"]["object_sha256"] = expected_object_sha
        exchange_mode = "malformed"
        await exercise("matching-hash-malformed-preview", malformed, failure="any")
        expected_object_sha = record["object_sha256"]
        exchange_mode = "good"
        corrupt = deepcopy(config)
        corrupt["selection"]["record"]["features"] = ["0"*64]
        await exercise("record-feature-mismatch", corrupt, failure="ORDINARY_PREVIEW_RECORD_BINDING")
        for label, change in (
            ("insufficient-preview-cap", lambda c: c["limits"].update(reply_bytes=len(preview_raw)-1)),
            ("more-than-one-request", lambda c: c["limits"].update(requests=2)),
            ("unselected-provider", lambda c: c["selection"].update(provider="absent")),
            ("invalid-snapshot", lambda c: c["selection"].update(snapshot_id="not-an-id")),
        ):
            changed = deepcopy(config); change(changed)
            await exercise(label, changed, failure="any", count=0)
        ledger = api.O.OrdinaryBudget(deadline=START+44, requests=3, reply_bytes=len(preview_raw)*3)
        ledger.charge_external("earlier-search", 1, len(preview_raw))
        before_deadline = ledger.deadline
        await exercise("shared-budget-not-closed-or-renewed", ledger=ledger)
        need(not ledger.closed and ledger.requests == 2 and ledger.reply_bytes == len(preview_raw)*2
             and ledger.deadline <= before_deadline and ledger.external[0]["label"] == "earlier-search",
             "PREVIEW_CONTROL_SHARED_CHARGES")
        await exercise("shared-final-request", ledger=ledger)
        await exercise("shared-exhausted-no-new-grant", ledger=ledger,
                       failure="ORDINARY_AGGREGATE_BUDGET", count=0)
        need(ledger.requests == 3 and not ledger.closed and ledger.pending is None,
             "PREVIEW_CONTROL_EXHAUSTED_PRESERVED")
        ledger.close()

    output.mkdir()
    with ExitStack() as stack:
        for obj, name in ((sqlite3, "connect"), (subprocess, "Popen"),
                          (loaded.A.OrdinaryAdmission, "open"), (api.O.OrdinaryStore, "__init__"),
                          (api.O.OrdinaryAcquisition, "evidence"), (api.O.OrdinaryAcquisition, "locator")):
            stack.enter_context(patch.object(obj, name, forbidden))
        stack.enter_context(patch.object(api.H, "exchange", exchange))
        asyncio.run(api_cases())
        # Explicit facade-bootstrap double: the real package was loaded once above.
        stack.enter_context(patch.object(entry, "bootstrap_owner", lambda *a: base))
        facade_loader = NS(hexid=loader.hexid, owner_json=loader.owner_json,
                           load=lambda *a, **kw: loaded)
        stack.enter_context(patch.object(base, "bootstrap", lambda *a: facade_loader))
        config_path = output/"config.json"
        with config_path.open("xb") as stream:
            stream.write(raw(config))
        cli = NS(operation="preview", profile_sha256=PROFILE, python_runtime=r"D:\Python314",
            lean_runtime=str(ROOT/"software/runtime/lean-4.34.0-windows"),
            config=str(config_path), config_sha256=sha(raw(config)), output=str(output/"facade"),
            wall_seconds=55, cpu_seconds=30, memory_mib=512,
            catalog=None, custody=None, store_id=None, custody_limits=None)
        result, encoded = entry.run(cli)
        need(result["ok"] and json.loads(encoded) == result and
             result["result"]["preview_sha256"] == PREVIEW_SHA,
             "PREVIEW_CONTROL_FACADE_DISPATCH")
        cases.append({"case": "inert-facade-dispatch-no-owner", "outcome": result})
        for field in ("catalog", "custody", "store_id", "custody_limits"):
            rejected = deepcopy(cli); setattr(rejected, field, "forbidden-state")
            rejected.output = str(output/("reject-"+field))
            before = len(calls)
            result, _ = entry.run(rejected)
            need(not result["ok"] and result["error"] == "PEER_OPERATION_STATE_ARGUMENTS" and
                 len(calls) == before and not Path(rejected.output).exists(), "PREVIEW_CONTROL_STATE_REJECTED")
            cases.append({"case": "state-argument-"+field, "outcome": result})
        need(not forbidden_calls, "PREVIEW_CONTROL_NO_FORBIDDEN_SIDE_EFFECTS")
    check()
    report = {"status": "PASS_REAL_PREVIEW_VALIDATION_INERT_TRANSPORT", "cases": cases,
        "case_count": len(cases), "exchange_calls": calls, "forbidden_calls": forbidden_calls,
        "profile_sha256": PROFILE, "preview_sha256": PREVIEW_SHA,
        "mathematical_acceptance": False, "network": "INERT_EXCHANGE_NOT_ACTUAL_HTTP",
        "wall_seconds": time.monotonic()-START, "controller_cpu_seconds": time.process_time()-CPU}
    with (output/"RESULT.json").open("xb") as stream:
        stream.write(raw(report))
    print(json.dumps({"status": report["status"], "case_count": len(cases)}), flush=True)


if __name__ == "__main__":
    main()

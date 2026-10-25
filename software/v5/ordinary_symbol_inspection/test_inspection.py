"""Focused inspector controls; real acquisition/codec, inert transport only.

Load the frozen native-src01 package once without opening owner state or running
native code. Overlay only the selected fresh API/CLI from the runner snapshot.
The final facade bootstrap is explicitly doubled; this is not installed-CLI or
actual-HTTP qualification. Root alone selects execution under Run-V5-Check.py.
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
PROFILE = "fc45893cef624978f0ab5212d0e1e172ff7c71f821124daa8751727bf7123ef6"
EVIDENCE_SHA = "08e2651ea1ebcf724a241d96036cfeeefc9d048d9ed79f88cf99c91a03f3c80f"
UNIT_ID = "3da789d6da6c0a12fadfdc74f08e7cced7146a97454eababae91ec9266242dd8"
EXPORT_ID = "2bf543aad2166307a1fccd72250b93cb9b7ec0d7df942b1e20beb5f700c7f886"
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU < 25,
         "INSPECTION_CONTROL_ORIGINAL_ALLOWANCE")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def raw(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def module(name, path, expected=None):
    data = path.read_bytes()
    need(len(data) <= 2*MIB and (expected is None or sha(data) == expected),
         "INSPECTION_CONTROL_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    exec(compile(data, str(path), "exec"), value.__dict__)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "evidence", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "INSPECTION_CONTROL_PROCESS")
    package, output = Path(args.package), Path(args.output)
    need(output.is_absolute() and output.resolve().is_relative_to(ROOT/"experiments/v5-local-checks")
         and output.parent.is_dir() and not os.path.lexists(output), "INSPECTION_CONTROL_OUTPUT")
    profile_raw = (package/"PROFILE.json").read_bytes()
    need(sha(profile_raw) == PROFILE, "INSPECTION_CONTROL_PROFILE")
    profile = json.loads(profile_raw)
    base = module("_inspection_control_owner", package/"owner.py", profile["files"]["owner.py"]["sha256"])
    loader = base.bootstrap(package, PROFILE, check)
    loaded = loader.load(package, PROFILE,
        {"python_runtime": Path(r"D:\Python314"),
         "lean_runtime": ROOT/"software/runtime/lean-4.34.0-windows"}, START+45, check_parent=check)
    source = Path(__file__).resolve().parent
    api = module("_inspection_control_api", source/"peer_api.py")
    entry = module("_inspection_control_entry", source/"peer.py")
    need(api.A is loaded.A and api.O is loaded.O, "INSPECTION_CONTROL_SHARED_HELPERS")
    loaded.peer_api = api
    evidence_raw = Path(args.evidence).read_bytes()
    need(sha(evidence_raw) == EVIDENCE_SHA, "INSPECTION_CONTROL_FIXTURE")
    parsed = api.A.PE.read_evidence(evidence_raw)
    need(parsed.unit_id == UNIT_ID and parsed.document["imports"], "INSPECTION_CONTROL_NONEMPTY_ANCESTRY")
    name = [[0, {"$bytes": list(part.encode())}] for part in
            ("RepairTheory", "ClosureBridge", "OrderData")]
    selection = {"provider": "fixture", "name": name, "export_id": EXPORT_ID}
    config = {"contacts": {"fixture": {"host": "127.0.0.1", "port": 12345,
        "tls": False, "server_name": None, "ca_file": None, "ca_sha256": None}},
        "selection": selection,
        "limits": {"requests": 2, "reply_bytes": 17408, "locator_bytes": 1024, "unit_bytes": 16384}}
    need(api.A.PE.export_id(loaded.installation.semantic_id, UNIT_ID, name) == EXPORT_ID,
         "INSPECTION_CONTROL_REAL_EXPORT")
    calls, forbidden_calls, cases = [], [], []
    exchange_mode, locator_name, locator_uid = "good", name, UNIT_ID

    def forbidden(*_, **__):
        forbidden_calls.append("FORBIDDEN")
        raise AssertionError("INSPECTION_CONTROL_FORBIDDEN_SIDE_EFFECT")

    async def exchange(endpoint, route, request, maximum, milliseconds):
        calls.append({"route": route, "request": deepcopy(request), "maximum": maximum})
        need(route in (api.O.LOCATOR_ROUTE, api.O.EVIDENCE_ROUTE) and milliseconds > 0,
             "INSPECTION_CONTROL_ONLY_SELECTED_ROUTES")
        if route == api.O.LOCATOR_ROUTE:
            data = raw({"schema": api.PP.LOCATOR_SCHEMA, "semantic_id": loaded.installation.semantic_id,
                        "unit_id": locator_uid, "export_name": locator_name})
        else:
            need(request["unit_id"] == locator_uid, "INSPECTION_CONTROL_LOCATOR_UNIT")
            if exchange_mode == "cancel":
                raise asyncio.CancelledError()
            if exchange_mode == "transport-failure":
                raise ConnectionResetError()
            data = evidence_raw if exchange_mode != "tamper" else evidence_raw[:-1]+b"!"
        need(len(data) <= maximum, "INSPECTION_CONTROL_TRANSPORT_CAP")
        return {"status": 503 if exchange_mode == "http-failure" else 200,
                "raw": data, "request_bytes": len(raw(request)), "reply_bytes": len(data), "header_bytes": 80}

    allowance = NS(deadline=START+45, check=check, operation=forbidden, account=forbidden)

    async def exercise(label, selected=None, *, ledger=None, failure=None, count=2):
        before = len(calls)
        original = deepcopy(config if selected is None else selected)
        supplied = deepcopy(original)
        try:
            result = await api.inspect(loaded, supplied, allowance, network_budget=ledger)
            need(failure is None, "INSPECTION_CONTROL_EXPECTED_FAILURE:"+label)
        except api.PeerFailure as error:
            need(failure is not None, "INSPECTION_CONTROL_UNEXPECTED_FAILURE:"+str(error.report))
            result = error.report
            if failure != "any":
                need(result["error"]["code"] == failure, "INSPECTION_CONTROL_WRONG_REFUSAL:"+label)
        need(supplied == original and len(calls)-before == count, "INSPECTION_CONTROL_INPUT_OR_IO:"+label)
        need(result["mathematical_acceptance"] is False and result["dependencies_checked"] is False
             and result["native_usable"] is False, "INSPECTION_CONTROL_NO_AUTHORITY:"+label)
        if failure is None:
            need(result["status"] == "INSPECTION_BOUND_NOT_ACCEPTED" and result["unit_id"] == UNIT_ID and
                 result["evidence_sha256"] == EVIDENCE_SHA and result["evidence_bytes"] == len(evidence_raw)
                 and result["evidence"] == parsed.document, "INSPECTION_CONTROL_EXACT_CONTENT:"+label)
        need(json.loads(raw(result)) == result, "INSPECTION_CONTROL_SERIALIZABLE")
        if result["network"] is not None:
            need(result["network"]["pending_requests"] == 0, "INSPECTION_CONTROL_TICKET_SETTLED")
        cases.append({"case": label, "status": result["status"], "requests": len(calls)-before,
                      "error": result.get("error"), "network": result["network"]})
        return result

    async def api_cases():
        nonlocal exchange_mode, locator_name, locator_uid
        good = await exercise("inspect-real-structure-with-imports-without-recursion")
        locator_bytes = good["locator_bytes"]
        need(good["network"]["closed"] and good["network"]["requests"] == 2 and
             good["network"]["charged_reply_bytes"] == locator_bytes+len(evidence_raw),
             "INSPECTION_CONTROL_OWNED_ACCOUNTING")
        for mode in ("tamper", "transport-failure", "cancel"):
            exchange_mode = mode
            result = await exercise(mode, failure="any")
            need(result["network"]["closed"] and result["network"]["charged_reply_bytes"] ==
                 locator_bytes+16384, "INSPECTION_CONTROL_FAILURE_CONSERVATIVELY_CHARGED")
        exchange_mode = "http-failure"
        result = await exercise("locator-http-failure", failure="ORDINARY_ACQUISITION_HTTP_STATUS", count=1)
        need(result["network"]["charged_reply_bytes"] == 1024, "INSPECTION_CONTROL_LOCATOR_FAILURE_CHARGE")
        exchange_mode = "good"
        wrong = deepcopy(config); wrong["selection"]["export_id"] = "0"*64
        await exercise("wrong-export-id", wrong, failure="ORDINARY_LOCATOR_EXACT_EXPORT", count=1)
        wrong = deepcopy(config); wrong["selection"]["name"] = [[0, {"$bytes": [120]}]]
        await exercise("wrong-export-name", wrong, failure="ORDINARY_LOCATOR_EXPECTED_NAME", count=1)
        locator_name = [[0, {"$bytes": [120]}]]
        wrong["selection"]["export_id"] = api.A.PE.export_id(loaded.installation.semantic_id, UNIT_ID, locator_name)
        await exercise("locator-claims-absent-output", wrong, failure="ORDINARY_EVIDENCE_EXPORT_OMISSION")
        locator_name, locator_uid = name, "0"*64
        wrong = deepcopy(config)
        wrong["selection"]["export_id"] = api.A.PE.export_id(loaded.installation.semantic_id, locator_uid, name)
        await exercise("wrong-evidence-unit", wrong, failure="ORDINARY_EVIDENCE_EXACT_ID")
        locator_uid = UNIT_ID
        for label, change in (
            ("third-request-refused", lambda c: c["limits"].update(requests=3)),
            ("insufficient-total-cap", lambda c: c["limits"].update(reply_bytes=17407)),
            ("boolean-cap", lambda c: c["limits"].update(locator_bytes=True)),
            ("unselected-provider", lambda c: c["selection"].update(provider="absent")),
            ("extra-config-field", lambda c: c.update(custody="forbidden")),
        ):
            wrong = deepcopy(config); change(wrong)
            await exercise(label, wrong, failure="any", count=0)
        ledger = api.O.OrdinaryBudget(deadline=START+44, requests=3, reply_bytes=20000)
        ledger.charge_external("earlier-search", 1, 100)
        deadline = ledger.deadline
        await exercise("shared-budget-no-renewal", ledger=ledger)
        need(not ledger.closed and ledger.requests == 3 and ledger.reply_bytes == 100+locator_bytes+len(evidence_raw)
             and ledger.deadline <= deadline, "INSPECTION_CONTROL_SHARED_ACCOUNTING")
        await exercise("spent-shared-budget-refused-before-io", ledger=ledger, failure="any", count=0)
        ledger.close()
        ledger = api.O.OrdinaryBudget(deadline=START+44, requests=4, reply_bytes=20000)
        ledger.charge_external("earlier-search", 1, 3000)
        await exercise("shared-byte-reservation-refused-before-io", ledger=ledger, failure="any", count=0)
        ledger.close()
        ledger = api.O.OrdinaryBudget(deadline=START+44, requests=2, reply_bytes=20000)
        ledger.deadline = time.monotonic()-1
        await exercise("expired-shared-budget-refused", ledger=ledger, failure="any", count=0)
        ledger.close()

    output.mkdir()
    with ExitStack() as stack:
        for obj, key in ((sqlite3, "connect"), (subprocess, "Popen"),
                         (loaded.A.OrdinaryAdmission, "open"), (api.O.OrdinaryStore, "__init__"),
                         (api.O.OrdinaryAcquisition, "preview"), (api.H.Provider, "start")):
            stack.enter_context(patch.object(obj, key, forbidden))
        stack.enter_context(patch.object(sys.modules["transport.clients"], "exchange", forbidden))
        stack.enter_context(patch.object(api.H, "exchange", exchange))
        asyncio.run(api_cases())
        stack.enter_context(patch.object(entry, "bootstrap_owner", lambda *a: base))
        facade_loader = NS(hexid=loader.hexid, owner_json=loader.owner_json, load=lambda *a, **kw: loaded)
        stack.enter_context(patch.object(base, "bootstrap", lambda *a: facade_loader))
        config_path = output/"config.json"
        with config_path.open("xb") as stream:
            stream.write(raw(config))
        cli = NS(operation="inspect", profile_sha256=PROFILE, python_runtime=r"D:\Python314",
            lean_runtime=str(ROOT/"software/runtime/lean-4.34.0-windows"),
            config=str(config_path), config_sha256=sha(raw(config)), output=str(output/"facade"),
            wall_seconds=55, cpu_seconds=30, memory_mib=512,
            catalog=None, custody=None, store_id=None, custody_limits=None)
        result, encoded = entry.run(cli)
        need(result["ok"] and json.loads(encoded) == result and
             result["result"]["evidence_sha256"] == EVIDENCE_SHA, "INSPECTION_CONTROL_FACADE_DISPATCH")
        cases.append({"case": "state-free-facade-dispatch", "status": "PASS"})
        for field in ("catalog", "custody", "store_id", "custody_limits"):
            rejected = deepcopy(cli); setattr(rejected, field, "forbidden-state")
            rejected.output = str(output/("reject-"+field))
            before = len(calls)
            result, _ = entry.run(rejected)
            need(not result["ok"] and result["error"] == "PEER_OPERATION_STATE_ARGUMENTS" and
                 len(calls) == before and not Path(rejected.output).exists(), "INSPECTION_CONTROL_STATE_REJECTION")
            cases.append({"case": "state-rejected-"+field, "status": "PASS"})
        need(not forbidden_calls, "INSPECTION_CONTROL_NO_FORBIDDEN_CALLS")
    check()
    report = {"status": "PASS_INSPECTION_REAL_CODEC_INERT_TRANSPORT", "cases": cases,
        "case_count": len(cases), "exchange_calls": calls, "forbidden_calls": forbidden_calls,
        "profile_sha256": PROFILE, "evidence_sha256": EVIDENCE_SHA,
        "mathematical_acceptance": False, "network": "MOCKED_EXCHANGE_NOT_ACTUAL_HTTP",
        "facade": "MOCKED_BOOTSTRAP_NOT_INSTALLED_PACKAGE",
        "wall_seconds": time.monotonic()-START, "controller_cpu_seconds": time.process_time()-CPU}
    with (output/"RESULT.json").open("xb") as stream:
        stream.write(raw(report))
    print(json.dumps({"status": report["status"], "case_count": len(cases)}), flush=True)


if __name__ == "__main__":
    main()

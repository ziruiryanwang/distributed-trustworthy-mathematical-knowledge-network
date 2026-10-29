"""Fresh retained-data fallback accepting either selected settled unavailable outcome.

Source only until root selects execution. This calls the packaged typed API,
not full public receive or mathematical admission. One finite ten-second service;
no Lean, owner, old database, mock, forced kill, retry or renewed allowance.
"""
from __future__ import annotations

import time
START, CPU = time.monotonic(), time.process_time()
import argparse
import asyncio
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import socket
import sys
from types import ModuleType, SimpleNamespace as NS

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PACKAGE = ROOT/"experiments/v5-local-checks/owned-acquisition-assembly01/distribution/package"
PROFILE = "85d45c928523c2b96f127ec8c15b2e2664f8428f0c1ef2415470a5b30737d3c8"
INSTALLATION = "9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27"
FIXTURE = ROOT/"experiments/v5-local-checks/ordinary-project-extraction-public-01/project/completion"
FIXTURE_PIN = "d031230312290008c5b09bb0587615d9a02310b4cfdc014ccbee2b491477d298"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
EXPORT = "d0c7be50520d2b91b72e43308b8f1ec75022b32c37fe9561381f4aef879fff1a"
UNIT = "f1c20bb5d6ef8d37227b0db40e0479d22ef3849f34c71d7a41880497316b1aa0"
MIB, DEADLINE = 1024**2, START+35
PACKAGES = ("discovery", "custody", "transport")
FORBIDDEN = ("ordinary_admission", "portable_catalog", "local_catalog", "ordinary_contribution",
             "baseline_intake", "peer_api", "owner", "profile")
# Fixed pure closure, captured and hash-verified before the first product import.
SOURCES = (
    ("ordinary_evidence", "installation/py/ordinary_evidence.py"),
    ("ordinary_semantics", "installation/py/ordinary_semantics.py"),
    ("portable_evidence", "installation/py/portable_evidence.py"),
    ("ordinary_preview", "authoring/py/ordinary_preview.py"),
    ("portable_preview", "authoring/py/portable_preview.py"),
    ("formal_query", "authoring/py/formal_query.py"),
    ("discovery.formal_features", "support/discovery/formal_features.py"),
    ("discovery.authenticated_index", "support/discovery/authenticated_index.py"),
    ("discovery.pair_access", "support/discovery/pair_access.py"),
    ("discovery.discovery_store", "support/discovery/discovery_store.py"),
    ("discovery.summary_wire", "support/discovery/summary_wire.py"),
    ("discovery.ordinary_export_adapter", "support/discovery/ordinary_export_adapter.py"),
    ("custody.module_store", "support/custody/module_store.py"),
    ("transport.http_provider", "support/transport/http_provider.py"),
    ("transport.clients", "support/transport/clients.py"),
    ("transport.fair_exchange", "support/transport/fair_exchange.py"),
    ("transport.ordinary_acquisition", "support/transport/ordinary_acquisition.py"))


def need(value, code):
    if not value:
        raise AssertionError("OWNED_PUBLIC_"+code)


def check():
    need(time.monotonic() < DEADLINE and time.process_time()-CPU < 20, "ORIGINAL_ENVELOPE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ordinary(path, *, directory=False):
    need(path.is_absolute() and path.resolve(strict=True) == path, "CANONICAL_PATH")
    for part in (path, *path.parents):
        need(not part.is_symlink() and not part.is_junction(), "REDIRECTED_PATH")
    need(path.is_dir() if directory else path.is_file(), "PATH_KIND")
    return path


def read(path, maximum=2*MIB, expected=None):
    check(); ordinary(path)
    need(0 < path.stat().st_size <= maximum, "READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(0 < len(raw) <= maximum and (expected is None or sha(raw) == expected), "READ_PIN")
    return raw


def write(path, raw):
    need(type(raw) is bytes and 0 < len(raw) <= 2*MIB, "OUTPUT_BOUND")
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "SHORT_WRITE")
        stream.flush(); os.fsync(stream.fileno())


def save(path, value):
    write(path, json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                          separators=(",", ":")).encode("ascii"))


def errors(error):
    result, seen = [], set()
    while error is not None and len(result) < 6 and id(error) not in seen:
        seen.add(id(error)); result.append(dict(type=type(error).__name__, message=str(error)[:500]))
        error = error.__cause__ if error.__cause__ is not None else error.__context__
    return result


def load_package(args, report):
    package = ordinary(Path(args.package), directory=True)
    need(package == PACKAGE and args.profile_sha256 == PROFILE, "SELECTED_PACKAGE")
    profile_raw = read(package/"PROFILE.json", expected=PROFILE)
    profile = json.loads(profile_raw)
    need(profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
         profile["installation_manifest_sha256"] == INSTALLATION, "PROFILE_BINDING")
    installed_raw = read(package/"installation/INSTALLATION.json", expected=INSTALLATION)
    installed = json.loads(installed_raw)
    need(installed["implementation"]["semantic_id"] == SEMANTIC, "SEMANTICS")
    pins = [(package/"PROFILE.json", len(profile_raw), PROFILE),
            (package/"installation/INSTALLATION.json", len(installed_raw), INSTALLATION)]
    for name in ("python.exe", "python3.dll", "python314.dll"):
        pin = installed["files"]["python_runtime/"+name]
        path = Path(sys.executable).parent/name
        raw = read(path, 16*MIB, pin["sha256"])
        need(len(raw) == pin["bytes"], "PYTHON_SUPPORT_BYTES")
        pins.append((path, len(raw), pin["sha256"]))
    captured = []
    for name, relative in SOURCES:
        pin = (installed["files"][relative.removeprefix("installation/")]
               if relative.startswith("installation/") else profile["files"][relative])
        raw = read(package/relative, expected=pin["sha256"])
        need(len(raw) == pin["bytes"], "SOURCE_BYTES")
        captured.append((name, package/relative, raw)); pins.append((package/relative, len(raw), sha(raw)))
    need(not any(name in sys.modules for name, _ in SOURCES) and
         not any(name == base or name.startswith(base+".") for name in sys.modules for base in PACKAGES),
         "PRELOADED_PRODUCT")
    for name in PACKAGES:
        module = ModuleType(name); module.__package__ = name; module.__path__ = []
        module.__spec__ = importlib.machinery.ModuleSpec(name, loader=None, is_package=True)
        module.__spec__.submodule_search_locations = []
        sys.modules[name] = module
    modules = {}
    for name, path, raw in captured:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec); sys.modules[name] = module
        exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
        if "." in name:
            parent, child = name.rsplit(".", 1); setattr(sys.modules[parent], child, module)
        modules[name] = module
    need(not any(name in sys.modules for name in FORBIDDEN), "OWNER_NATIVE_IMPORT")
    report["source_closure"] = [{"name": name, "path": str(path.relative_to(package)),
                                  "bytes": len(raw), "sha256": sha(raw)} for name, path, raw in captured]
    return NS(package=package, pins=pins, modules=modules,
        E=modules["ordinary_evidence"], PE=modules["portable_evidence"], PP=modules["portable_preview"],
        F=modules["discovery.formal_features"], OA=modules["discovery.ordinary_export_adapter"],
        H=modules["transport.http_provider"], O=modules["transport.ordinary_acquisition"])


def fixture(s, report):
    result_raw = read(FIXTURE/"RESULT.json", expected=FIXTURE_PIN)
    result = json.loads(result_raw)
    need(result["semantic_id"] == SEMANTIC and len(result["targets"]) == len(result["previews"]) == 1,
         "RETAINED_RESULT")
    target, preview = result["targets"][0], result["previews"][0]
    need(target["export_id"] == EXPORT and target["unit_id"] == UNIT and
         preview["export_id"] == EXPORT and preview["unit_id"] == UNIT and
         preview["name"] == target["name"], "RETAINED_TARGET")
    unit = next(row for row in result["units"] if row["unit_id"] == UNIT)
    need(preview["file"] == str(FIXTURE/"previews"/(EXPORT+".json")) and
         unit["file"] == str(FIXTURE/"evidence"/(UNIT+".json")), "RETAINED_PATHS")
    p = read(Path(preview["file"]), expected=preview["sha256"])
    u = read(Path(unit["file"]), expected=unit["sha256"])
    need(len(p) == preview["bytes"] == 1351 and len(u) == unit["bytes"] == 4997, "RETAINED_BYTES")
    s.PP.resolve(p, u)
    adapter = s.OA.OrdinaryExportAdapter(SEMANTIC)
    record = adapter.describe(p, EXPORT)["record"]
    locator = {"schema": s.PP.LOCATOR_SCHEMA, "semantic_id": SEMANTIC,
               "unit_id": UNIT, "export_name": target["name"]}
    locator_raw = s.F.compact(s.PP.read_locator(locator))
    s.pins.extend(((FIXTURE/"RESULT.json", len(result_raw), FIXTURE_PIN),
                   (Path(preview["file"]), len(p), preview["sha256"]),
                   (Path(unit["file"]), len(u), unit["sha256"])))
    report["fixture"] = dict(result_sha256=FIXTURE_PIN, target=target,
        preview_sha256=sha(p), evidence_sha256=sha(u), locator_sha256=sha(locator_raw),
        locator_origin="UNCHANGED_CANONICAL_LOCATOR_DERIVED_FROM_RETAINED_EXACT_IDENTITIES")
    return NS(target=target, preview=p, evidence=u, locator=locator, locator_raw=locator_raw,
              adapter=adapter, record=record)


async def scenario(s, f, output, report):
    O, H = s.O, s.H
    store = provider = reservation = lease = client = budget = None
    lease_until = None
    report.update(attempts=[], cleanup_errors=[], service_lease_seconds=10,
                  native_calls=0, owner_opened=False, forced_termination=False)
    try:
        store = O.OrdinaryStore(output/"custody", SEMANTIC,
            dict(objects=4, exports=16, logical_bytes=MIB, db_pages=256), create=True)
        store.put_evidence(f.evidence, before_commit=check); store.put_preview(f.preview, before_commit=check)
        need(store.get_locator(SEMANTIC, EXPORT, len(f.locator_raw), check_budget=check) == f.locator_raw,
             "STORED_LOCATOR_BYTES")
        report["custody"] = store.status()
        reservation = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        reservation.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        reservation.bind(("127.0.0.1", 0))  # Deliberately never listen; keep port reserved.
        # Windows may wait for the attempt deadline instead of refusing immediately.
        # Either selected unavailable outcome must come through owned, settled cleanup.
        unavailable = H.Endpoint("127.0.0.1", reservation.getsockname()[1])
        provider = H.Provider(ordinary=store, max_connections=1, max_requests=3,
            max_reply_bytes=MIB, operation_ms=1500)
        live = await provider.start("127.0.0.1", 0)
        need(live.port != unavailable.port, "DISTINCT_ENDPOINTS")
        lease_until = time.monotonic()+10
        report["service_started_seconds"] = lease_until-10-START

        async def finite_service():
            await asyncio.sleep(max(0, lease_until-time.monotonic()))
            await provider.stop()
            report["service_closed_seconds"] = time.monotonic()-START
            report["service_termination"] = "NATURAL_ORIGINAL_LEASE"
        lease = asyncio.create_task(finite_service())
        request_cap = 4
        byte_cap = 2*len(f.preview)+len(f.locator_raw)+len(f.evidence)
        original_deadline = min(lease_until-2, DEADLINE-5)
        budget = O.OrdinaryBudget(deadline=original_deadline, requests=request_cap, reply_bytes=byte_cap)
        client = O.OrdinaryAcquisition(f.adapter, {"unavailable": unavailable, "live": live}, budget)
        report["grant"] = dict(deadline_seconds=original_deadline-START, requests=request_cap,
            reply_bytes=byte_cap, attempt_timeout_ms=1500, ledger_instances=1)
        report["endpoints"] = {"unavailable": dict(host=unavailable.host, port=unavailable.port),
                               "live": dict(host=live.host, port=live.port),
                               "policy": "EXPLICIT_CONFIGURED_LOOPBACK_ONLY"}

        async def attempt(label, action, expected=None):
            check(); need(client.budget is budget and budget.deadline == original_deadline, "SAME_LEDGER")
            row = dict(label=label, status="STARTED", before=client.report())
            report["attempts"].append(row)
            try:
                value = await action()
                need(expected is None, "UNAVAILABLE_SUCCEEDED")
                row.update(status="EXACT_TYPED_RESPONSE", bytes=len(value["raw"]), sha256=sha(value["raw"]))
                return value
            except O.AcquisitionUnavailable as error:
                row.update(status="SETTLED_UNAVAILABLE", reason=error.reason)
                need(expected is not None and error.reason in expected and error.provider == "unavailable" and
                     error.route == O.PREVIEW_ROUTE, "EXPECTED_SETTLED_REFUSAL")
                return None
            except BaseException as error:
                row.update(status="FAILED", errors=errors(error)); raise
            finally:
                row["after"] = client.report()
                need(client.budget is budget and budget.deadline == original_deadline, "UNCHANGED_DEADLINE")

        await attempt("unavailable-preview", lambda: client.preview("unavailable", f.record,
            attempt_timeout_ms=1500, unavailable_errors=True),
            expected=("CONNECTION_REFUSED", "ATTEMPT_TIMEOUT"))
        # This assertion precedes issuance of the live-provider fallback.
        need(budget.requests == budget.sequence == 1 and budget.reply_bytes == len(f.preview) and
             budget.pending is None and client.http["failed_attempts"] == 1, "FAILED_ATTEMPT_ALREADY_CHARGED")
        report["failed_charge_observed_before_fallback"] = True
        preview = await attempt("live-preview", lambda: client.preview("live", f.record, attempt_timeout_ms=1500))
        need(preview["raw"] == f.preview and preview["mathematical_acceptance"] is False, "PREVIEW_IDENTITY")
        locator = await attempt("live-locator", lambda: client.locator("live", SEMANTIC, EXPORT,
            len(f.locator_raw), expected_name=f.target["name"], attempt_timeout_ms=1500))
        need(locator["raw"] == f.locator_raw and locator["locator"] == f.locator and
             locator["export_id"] == EXPORT and locator["mathematical_acceptance"] is False, "LOCATOR_IDENTITY")
        evidence = await attempt("live-evidence", lambda: client.evidence("live", SEMANTIC,
            locator["locator"]["unit_id"], len(f.evidence), expected_export_id=EXPORT,
            expected_export_name=f.target["name"], attempt_timeout_ms=1500))
        need(evidence["raw"] == f.evidence and evidence["unit_id"] == UNIT and
             evidence["semantic_id"] == SEMANTIC and evidence["mathematical_acceptance"] is False,
             "EVIDENCE_IDENTITY")
        need(budget.requests == budget.sequence == request_cap and budget.reply_bytes == byte_cap and
             budget.pending is None and budget.external == [] and client.http["completed_responses"] == 3 and
             client.http["failed_attempts"] == 1 and client.http["actual_reply_bytes"] ==
             len(f.preview)+len(f.locator_raw)+len(f.evidence), "AGGREGATE_ACCOUNTING")
        budget.close(); report["acquisition"] = client.report()
        for name, raw in (("ACQUIRED-PREVIEW.json", preview["raw"]),
                          ("ACQUIRED-LOCATOR.json", locator["raw"]), ("ACQUIRED-EVIDENCE.json", evidence["raw"])):
            write(output/name, raw)
    finally:
        if client is not None:
            report["final_acquisition"] = client.report()
        if lease is not None:
            try:
                async with asyncio.timeout_at(min(DEADLINE-2, lease_until+3)):
                    await asyncio.shield(lease)
            except BaseException as error:
                report["cleanup_errors"].append(errors(error))
        elif provider is not None:
            try:
                await provider.stop()
            except BaseException as error:
                report["cleanup_errors"].append(errors(error))
        if reservation is not None:
            reservation.close(); report["unavailable_reservation_closed"] = reservation.fileno() == -1
        if provider is not None:
            report["provider"] = provider.status()
            report["quiescent"] = (provider.server is None and not provider.tasks and
                                    not provider._connections and provider.reserved_reply_bytes == 0)
        if store is not None:
            store.close(); report["custody_closed"] = store.db is None
    need(report["cleanup_errors"] == [] and report.get("quiescent") is True and
         report.get("custody_closed") is True and report.get("unavailable_reservation_closed") is True and
         report.get("service_termination") == "NATURAL_ORIGINAL_LEASE", "CLEAN_CLOSURE")
    need(report["provider"]["requests"] == report["provider"]["accepted_attempts"] == 3 and
         report["provider"]["failures"] == report["provider"]["cleanup_failures"] == 0, "PROVIDER_CENSUS")


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("package", "profile-sha256", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize and sys.version_info[:3] == (3, 14, 6), "PYTHON_PROFILE")
    output = Path(args.output)
    ordinary(output.parent, directory=True)
    need(output.is_absolute() and output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         not output.exists() and output.name not in (".", "..") and
         not output.is_relative_to(PACKAGE) and not PACKAGE.is_relative_to(output), "FRESH_OUTPUT")
    output.mkdir()
    report = dict(status="STARTED", package=str(PACKAGE), profile_sha256=PROFILE,
        installation_manifest_sha256=INSTALLATION, mathematical_acceptance=False,
        scope="PACKAGED_TYPED_API_FIXED_PROVIDER_FALLBACK_NOT_PUBLIC_RECEIVE_OR_NATIVE_ADMISSION")
    try:
        s = load_package(args, report); f = fixture(s, report)
        asyncio.run(scenario(s, f, output, report))
        for path, length, digest in s.pins:
            need(len(read(path, 16*MIB, digest)) == length, "FINAL_INPUT_BINDING")
        need(all(sys.modules[name] is module for name, module in s.modules.items()) and
             not any(name in sys.modules for name in FORBIDDEN), "FINAL_PURE_CLOSURE")
        check(); report["status"] = "PASS"
    except BaseException as error:
        report.update(status="FAIL", errors=errors(error))
    report.update(wall_seconds=time.monotonic()-START, known_process_cpu_seconds=time.process_time()-CPU)
    save(output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")), flush=True)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

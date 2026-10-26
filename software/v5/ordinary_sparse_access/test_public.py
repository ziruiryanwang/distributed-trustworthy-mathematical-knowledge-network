"""Two bounded real public sparse finds plus narrow configuration forwarding.

One real pair-enabled ordinary metadata index, current HTTP positive, exact old
provider missing-route refusal, and a declared in-process directory capture.
No accepted mathematical state, Lean process, proof campaign or timing claim.
This source needs root's separate exact package/finite execution selection.
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
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
DEADLINE = START_WALL + 80
LEGACY = ROOT/"experiments/v5-local-checks/contact-federation-assembly01/assembled/package/support/transport/http_provider.py"
LEGACY_SHA256 = "250543498b83deb4a0893bd159ef6b890fcdd3744be4ca562079368a7f110954"
INDEX_LIMITS = dict(max_objects=1, max_postings=64, max_features=64,
                    max_snapshots=2, max_logical_bytes=2*MIB, max_db_pages=256)
PAGE = dict(scanned=8, matches=4, bytes=65536, timeout_ms=1000,
            record_probes=64, node_reads=100000, hash_calls=2000000, sql_vm_steps=1000000)


def need(ok, code):
    if not ok:
        raise ValueError(code)


def check():
    need(time.monotonic() < DEADLINE and time.process_time()-START_CPU < 45,
         "SPARSE_PUBLIC_ORIGINAL_ENVELOPE")


def read(path, maximum=2*MIB):
    check()
    size = path.stat().st_size
    need(0 < size <= maximum, "SPARSE_PUBLIC_READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size, "SPARSE_PUBLIC_READ_CHANGED")
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(raw) <= 2*MIB, "SPARSE_PUBLIC_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw+b"\n")


def load_package(args):
    root = Path(args.package)
    need(root.is_absolute() and root.resolve(strict=True) == root, "SPARSE_PUBLIC_PACKAGE_PATH")
    raw = read(root/"PROFILE.json")
    need(hashlib.sha256(raw).hexdigest() == args.profile_sha256, "SPARSE_PUBLIC_PROFILE_PIN")
    pin = json.loads(raw)["files"]["profile.py"]
    source = read(root/"profile.py")
    need(len(source) == pin["bytes"] and hashlib.sha256(source).hexdigest() == pin["sha256"],
         "SPARSE_PUBLIC_LOADER_PIN")
    spec = importlib.util.spec_from_file_location("_sparse_public_profile", root/"profile.py")
    loader = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = loader
    exec(compile(source, str(root/"profile.py"), "exec"), loader.__dict__)
    return loader.load(root, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        DEADLINE, check_parent=check)


def load_legacy(current):
    raw = read(LEGACY)
    need(hashlib.sha256(raw).hexdigest() == LEGACY_SHA256, "SPARSE_PUBLIC_LEGACY_PIN")
    name = "transport._sparse_public_legacy_provider"
    need(name not in sys.modules, "SPARSE_PUBLIC_LEGACY_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, LEGACY)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(LEGACY), "exec"), module.__dict__)
    need(current.SPARSE_CANDIDATE_ROUTE not in module.ROUTES and
         current.OFFER_ROUTE == module.OFFER_ROUTE and current.CANDIDATE_ROUTE in module.ROUTES,
         "SPARSE_PUBLIC_ACTUAL_LEGACY_ROUTES")
    return module


def search_fields():
    return dict(limits=dict(providers=1, snapshots=2, requests=4, pages=2,
        examined=16, candidates=8, bytes=MIB, wall_ms=15000, inflight=1),
        offer=dict(max_bytes=65536, max_expanded_bytes=MIB, max_age_ms=15000),
        page=deepcopy(PAGE), candidate_mode="sparse-v2")


def contact(endpoint):
    return dict(host=endpoint.host, port=endpoint.port, tls=endpoint.tls,
                server_name=endpoint.server_name, ca_file=None, ca_sha256=None)


def command(args, output, label, config):
    path = output/(label+"-config.json")
    save(path, config)
    digest = hashlib.sha256(read(path)).hexdigest()
    argv = [str(Path(args.python_runtime)/"python.exe"), "-I", "-S", "-B",
        str(Path(args.package)/"run.py"), "--profile-sha256", args.profile_sha256,
        "--python-runtime", args.python_runtime, "--lean-runtime", args.lean_runtime,
        "--diagnostics", str(output/(label+"-launcher")), "--wall-seconds", "35",
        "--cpu-seconds", "20", "--memory-mib", "512", "--active-processes", "3",
        "--stdout-bytes", str(MIB), "--stderr-bytes", str(MIB), "peer", "--", "find",
        "--config", str(path), "--config-sha256", digest,
        "--output", str(output/(label+"-public"))]
    need(not any(value in argv for value in ("--catalog", "--custody", "--store-id", "--custody-limits")),
         "SPARSE_PUBLIC_UNEXPECTED_STATE_ARGUMENT")
    save(output/(label+"-COMMAND.json"), dict(argv=argv, cwd=str(ROOT), attempts=1))
    return argv, digest


def public_result(args, output, label, digest, semantic):
    launch = json.loads(read(output/(label+"-launcher")/"RUN.json"))
    supervision = json.loads(read(output/(label+"-launcher")/"SUPERVISION.json"))
    public = json.loads(read(output/(label+"-public")/"RESULT.json"))
    need(launch["ok"] is True and launch["profile_sha256"] == args.profile_sha256 and
         supervision["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and
         supervision["direct_child_reaped"] is True and supervision["job_closed"] is True and
         supervision["cleanup_errors"] == [] and supervision["final_job"]["active_processes"] == 0,
         "SPARSE_PUBLIC_JOB_NOT_CLOSED")
    need(public["ok"] is True and public["operation"] == "find" and
         public["semantic_id"] == semantic and public["config_sha256"] == digest and
         public["profile_sha256"] == args.profile_sha256 and public["catalog"] is None and
         public["custody"] is None and public["store_id"] is None and
         public["cost"]["worker_cpu_seconds"] == 0,
         "SPARSE_PUBLIC_RESULT_BINDING_OR_NATIVE_WORK")
    return dict(result=public, supervision=supervision, launcher=launch)


async def directory_forwarding(loaded, specs, features, report):
    """Only composition: declared exchange/find doubles; no directory campaign."""
    api, calls = loaded.peer_api, []
    seed = api.H.Endpoint("127.0.0.1", 40001)
    hint = dict(host="127.0.0.1", port=40002, tls=False, server_name=None)
    adapter = api.OrdinaryExportAdapter(loaded.installation.semantic_id)
    mapping = api.CD.ContactMap.from_bytes(api.F.compact(dict(schema=api.CD.MAP_SCHEMA,
        namespace=adapter.namespace, entries=[dict(features=features, endpoints=[hint])])),
        check_budget=check)
    config = dict(contacts={"seed": contact(seed)}, directories=["seed"],
        specs=deepcopy(specs), routes=[deepcopy(specs)], search=search_fields(),
        directory=dict(requests=1, reply_bytes=api.CD.REPLY_MAX, max_contacts=1,
            max_bytes=api.CD.REPLY_MAX, max_age_ms=20000, attempt_timeout_ms=3000),
        egress=dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
            test_endpoints=[dict(host=hint["host"], port=hint["port"])]))
    allowance = SimpleNamespace(deadline=DEADLINE, check=check)
    ledger = api.O.OrdinaryBudget(deadline=DEADLINE-3, requests=5,
                                  reply_bytes=MIB+api.CD.REPLY_MAX)
    original_deadline = ledger.deadline

    async def exchange_double(endpoint, route, request, cap, timeout, *, absolute_deadline):
        check()
        need(endpoint == seed and route == api.H.CONTACT_DIRECTORY_ROUTE and
             cap == api.CD.REPLY_MAX and absolute_deadline <= original_deadline,
             "SPARSE_PUBLIC_DIRECTORY_CAPTURE_INPUT")
        raw = mapping.reply(request, check_budget=check)
        calls.append("contact-exchange-double")
        return dict(status=200, raw=raw, reply_bytes=len(raw),
                    request_bytes=len(api.F.compact(request)), header_bytes=0)

    async def find_double(selected, forwarded, checked_allowance, *, network_budget):
        check(); checked_allowance.check()
        need(selected is loaded and network_budget is ledger and ledger.deadline <= original_deadline and
             forwarded["candidate_mode"] == "sparse-v2" and forwarded["specs"] == specs and
             forwarded["page"] == PAGE and forwarded["limits"] == config["search"]["limits"] and
             len(forwarded["contacts"]) == 1 and
             next(iter(forwarded["contacts"].values())) == {**hint, "ca_file": None, "ca_sha256": None},
             "SPARSE_PUBLIC_NESTED_MODE_OR_GRANT_NOT_FORWARDED")
        need(ledger.external == [dict(label="directory-find", requests=1, reply_bytes=api.CD.REPLY_MAX)],
             "SPARSE_PUBLIC_CAPTURE_BEFORE_SEARCH_CHARGE")
        calls.append("find-capture-double")
        return dict(matches=[], authority="CAPTURE_ONLY_NO_SEARCH_OR_MATHEMATICS")

    def no_dial(*args, **kwargs):
        raise AssertionError("SPARSE_PUBLIC_DIRECTORY_CAPTURE_MUST_NOT_DIAL")

    try:
        with patch.object(api.X, "exchange", new=exchange_double), \
                patch.object(api, "find", new=find_double), \
                patch.object(asyncio, "open_connection", new=no_dial):
            result = await api.directory_find(loaded, config, allowance, network_budget=ledger)
        need(calls == ["contact-exchange-double", "find-capture-double"] and
             result["candidate_mode"] == "sparse-v2" and result["cleanup_errors"] == [] and
             result["directory"]["requests"] == 1 and not ledger.closed and ledger.pending is None,
             "SPARSE_PUBLIC_DIRECTORY_CAPTURE_RESULT")
        report["directory_forwarding"] = dict(scope="DOUBLED_CONTACT_AND_FIND_COMPOSITION_ONLY",
            calls=calls, result=result)
    finally:
        ledger.close()
        report["directory_forwarding_ledger"] = ledger.report()


async def scenario(args, output, loaded, report):
    api, H = loaded.peer_api, loaded.peer_api.H
    legacy = load_legacy(H)
    adapter = api.OrdinaryExportAdapter(loaded.installation.semantic_id)
    def name(value): return [[0, {"$bytes": list(value.encode("ascii"))}]]
    bindings = sorted([[name(label), hashlib.sha256(("sparse-public-symbol-"+label).encode("ascii")).hexdigest()]
        for label in ("A", "R")], key=lambda row: api.F.compact(row[0]))
    specs = [dict(tag="type-symbol", symbol=dict(kind="portable-symbol", symbol_id=row[1])) for row in bindings]
    features = api.compile_query(adapter.namespace, specs)
    expr = [api.A.E.EXPR_FORMAT, [], [[2, name("R"), []], [2, name("A"), []], [3, 0, 1]], 2]
    raw = api.F.compact(dict(schema=api.PP.SCHEMA, semantic_id=loaded.installation.semantic_id,
        unit_id=hashlib.sha256(b"sparse-public-unproved-unit").hexdigest(),
        export_name=name("UnprovedPublicSparseClaim"), header=[2, [], expr], type_bindings=bindings))
    described = adapter.describe(raw)
    expected = described["record"]
    need(len(features) == 2 and set(features) <= set(expected["features"]) and
         expected["schema"] == api.F.ORDINARY_EXPORT_RECORD_SCHEMA and
         described["mathematical_acceptance"] is False, "SPARSE_PUBLIC_SYNTHETIC_ORDINARY_METADATA")
    with (output/"SYNTHETIC-PREVIEW.json").open("xb") as stream:
        stream.write(raw)
    save(output/"EXPECTED-RECORD.json", expected)
    access = dict(pairs=[features], limits=dict(max_rows=2, max_logical_bytes=4096))
    index_config = dict(path=str(output/"fresh-index"), create=True,
                        limits=deepcopy(INDEX_LIMITS), access_pairs=deepcopy(access))
    save(output/"INDEX-CONFIG.json", index_config)
    # _index consumes only .root for separation. This object is NOT a store or
    # acceptance authority; no publish/serve/_state gate is bypassed or claimed.
    custody_path_only = SimpleNamespace(root=output/"unused-custody-separation-path")
    index = None
    providers, children, pins = {}, {}, {}
    connections, tasks, writers, dispatches, legacy_lines, cleanup_errors = [], [], [], [], [], []
    original_headers = legacy._headers

    async def observed_legacy_headers(reader):
        value = await original_headers(reader)
        need(len(legacy_lines) < 2, "SPARSE_PUBLIC_LEGACY_REQUEST_BOUND")
        legacy_lines.append(value[0])
        return value

    def observed_provider(base, label):
        class Observed(base):
            def dispatch(self, route, request, *, check_budget=None):
                value = super().dispatch(route, request, check_budget=check_budget)
                need(len(dispatches) < 3, "SPARSE_PUBLIC_DISPATCH_BOUND")
                row = dict(provider=label, route=route, request=deepcopy(request))
                if route == H.SPARSE_CANDIDATE_ROUTE:
                    row["page"] = deepcopy(value)
                dispatches.append(row)
                return value

            async def _serve(self, reader, writer):
                row = dict(provider=label, closed=False)
                connections.append(row); tasks.append(asyncio.current_task()); writers.append(writer)
                try:
                    need(len(connections) <= 4, "SPARSE_PUBLIC_CONNECTION_BOUND")
                    await super()._serve(reader, writer)
                except BaseException as error:
                    row.update(error_type=type(error).__name__, error=str(error)[:300])
                finally:
                    try:
                        writer.close()
                        async with asyncio.timeout(max(0.001, min(2, DEADLINE-time.monotonic()))):
                            await writer.wait_closed()
                        row["closed"] = True
                    except BaseException as error:
                        row.update(close_error_type=type(error).__name__, close_error=str(error)[:300])
        return Observed

    try:
        index = api._index(loaded, None, custody_path_only, index_config, check)
        admitted = index.admit(raw, expected_id=expected["object_id"])
        need(admitted["record"] == expected and index.access_pairs == access and
             index.status()["objects"] == 1, "SPARSE_PUBLIC_REAL_INDEX_ADMISSION")
        index.close()
        need(index.db is None, "SPARSE_PUBLIC_CREATE_HANDLE_NOT_CLOSED")
        index = api._index(loaded, None, custody_path_only, {**index_config, "create": False}, check)
        need(index.access_pairs == access and index.status()["objects"] == 1,
             "SPARSE_PUBLIC_EXACT_INDEX_REOPEN")
        report["index_forwarding"] = dict(scope="REAL_INDEX_CREATE_AND_REOPEN_PATH_ONLY_CUSTODY_DOUBLE",
            access_pairs=access, admitted=admitted)
        await directory_forwarding(loaded, specs, features, report)
        with patch.object(legacy, "_headers", new=observed_legacy_headers), ExitStack() as files:
            for label, implementation in (("sparse", H), ("legacy", legacy)):
                provider = observed_provider(implementation.Provider, label)(index=index,
                    max_connections=2, max_requests=2, max_reply_bytes=MIB, operation_ms=5000)
                providers[label] = provider
                endpoint = await provider.start("127.0.0.1", 0)
                config = dict(contacts={label: contact(endpoint)}, providers=[label],
                              specs=deepcopy(specs), **search_fields())
                argv, pins[label] = command(args, output, label, config)
                need(DEADLINE-time.monotonic() >= 43, "SPARSE_PUBLIC_NO_ROOM_FOR_ORIGINAL_CHILD")
                stdout = files.enter_context((output/(label+"-stdout.txt")).open("xb"))
                stderr = files.enter_context((output/(label+"-stderr.txt")).open("xb"))
                children[label] = await asyncio.create_subprocess_exec(*argv, cwd=ROOT,
                    stdout=stdout, stderr=stderr, stdin=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW)
            async with asyncio.timeout_at(DEADLINE-8):
                exits = await asyncio.gather(*(child.wait() for child in children.values()))
            need(exits == [0, 0], "SPARSE_PUBLIC_LAUNCHER_FAILURE")
        for label in ("sparse", "legacy"):
            for suffix in ("stdout", "stderr"):
                need((output/(label+"-"+suffix+".txt")).stat().st_size <= MIB,
                     "SPARSE_PUBLIC_CHILD_LOG_BOUND")
            selected = public_result(args, output, label, pins[label], loaded.installation.semantic_id)
            report[label] = selected
            result = selected["result"]["result"]
            need(result["candidate_mode"] == "sparse-v2" and result["status"] == "INCOMPLETE_SEARCH" and
                 result["global_complete"] is False and result["verified_scan_coverage"] is False and
                 result["mathematical_acceptance"] is False and result["cleanup_errors"] == [],
                 "SPARSE_PUBLIC_NO_COMPLETENESS_OR_MATHEMATICS")
            session = result["search"]["session"]
            need(session["used"]["requests"] == 2 and session["used"]["pages"] == 1 and
                 session["used"]["examined"] == PAGE["scanned"] and session["pending_requests"] == 0 and
                 all(value == 0 for value in session["reserved"].values()) and
                 session["candidate_search"]["charged_scan_allowances"] == PAGE["scanned"] and
                 session["last_verified"] == {}, "SPARSE_PUBLIC_FULL_SCAN_CHARGE_AND_SETTLEMENT")
            budget = result["network"]
            need(budget["closed"] is True and budget["pending_requests"] == 0 and budget["requests"] == 4 and
                 budget["charged_reply_bytes"] == MIB and
                 budget["external_prepaid"] == [dict(label="peer-find", requests=4, reply_bytes=MIB)],
                 "SPARSE_PUBLIC_SINGLE_ORIGINAL_GRANT")
            if label == "sparse":
                need(result["matches"] == [dict(provider=label, snapshot_id=admitted["snapshot_id"], record=expected)] and
                     result["provider_errors"] == [] and session["candidate_search"]["unique_verified_records"] == 1 and
                     result["search"]["http"]["failed_requests"] == 0,
                     "SPARSE_PUBLIC_EXACT_VERIFIED_POSITIVE")
            else:
                errors = result["provider_errors"]
                need(result["matches"] == [] and session["candidate_search"]["unique_verified_records"] == 0 and
                     len(errors) == 1 and errors[0]["provider"] == label and errors[0]["phase"] == "candidates" and
                     errors[0]["error"]["type"] == "SettledRefusal" and
                     errors[0]["error"]["code"] in ("PEER_EOF", "CONNECTION_RESET", "BROKEN_PIPE") and
                     session["used"]["candidates"] == PAGE["matches"] and
                     session["used"]["bytes"] >= PAGE["bytes"] and
                     result["search"]["http"]["failed_requests"] == 1 and
                     result["termination"] == "SELECTED_CONTACTS_FINISHED_WITH_PROVIDER_ERRORS_NO_COMPLETENESS_CLAIM",
                     "SPARSE_PUBLIC_CHARGED_LEGACY_UNSUPPORTED_NO_RETRY")
        pages = [row for row in dispatches if row["route"] == H.SPARSE_CANDIDATE_ROUTE]
        need(len(pages) == 1 and pages[0]["provider"] == "sparse" and
             pages[0]["request"]["schema"] == "DMKN_FORMAL_CANDIDATE_REQUEST_V2" and
             pages[0]["page"]["schema"] == "DMKN_FORMAL_CANDIDATE_PAGE_V2" and
             pages[0]["page"]["access_used"]["kind"] == "pair" and
             pages[0]["page"]["access_used"]["companion"] in features and
             pages[0]["page"]["hits"][0]["record"] == expected,
             "SPARSE_PUBLIC_ACTUAL_PAIR_ROUTE")
        need(legacy_lines == ["POST "+H.OFFER_ROUTE+" HTTP/1.1",
                              "POST "+H.SPARSE_CANDIDATE_ROUTE+" HTTP/1.1"] and
             [row["route"] for row in dispatches if row["provider"] == "legacy"] == [H.OFFER_ROUTE],
             "SPARSE_PUBLIC_ACTUAL_OLD_MISSING_ROUTE_NO_ATOMIC_RETRY")
        report["assertions_passed"] = True
    finally:
        for label, child in children.items():
            if child.returncode is None:
                try:
                    child.kill()
                    async with asyncio.timeout(max(0.001, min(3, DEADLINE-time.monotonic()))):
                        await child.wait()
                except BaseException as error:
                    cleanup_errors.append(label+":"+type(error).__name__)
        report["children_reaped"] = {name: child.returncode is not None for name, child in children.items()}
        report["providers"] = {}
        for label, provider in providers.items():
            try:
                async with asyncio.timeout(max(0.001, min(2, DEADLINE-time.monotonic()))):
                    await provider.stop()
            except BaseException as error:
                cleanup_errors.append(label+"-provider:"+type(error).__name__)
            report["providers"][label] = dict(status=provider.status(), listener_closed=provider.server is None)
        for writer in writers:
            writer.close()
        live = [task for task in tasks if not task.done()]
        for task in live:
            task.cancel()
        if live:
            try:
                async with asyncio.timeout(max(0.001, min(2, DEADLINE-time.monotonic()))):
                    await asyncio.gather(*live, return_exceptions=True)
            except BaseException as error:
                cleanup_errors.append("observers:"+type(error).__name__)
        report.update(connections=connections, handlers_finished=all(task.done() for task in tasks),
                      dispatches=dispatches, legacy_request_lines=legacy_lines)
        if index is not None:
            try: index.close()
            except BaseException as error: cleanup_errors.append("index:"+type(error).__name__)
            report["index_closed"] = index.db is None
        report["cleanup_errors"] = cleanup_errors
    need(not cleanup_errors and report["children_reaped"] == {"sparse": True, "legacy": True} and
         report["handlers_finished"] and report.get("index_closed") is True and len(connections) == 4 and
         all(row["closed"] and "error_type" not in row and "close_error_type" not in row for row in connections),
         "SPARSE_PUBLIC_CLEANUP_UNCERTAIN")
    for label, value in report["providers"].items():
        status = value["status"]
        need(value["listener_closed"] and status["requests"] == 2 and status["active"] == 0 and
             status["reserved_reply_bytes"] == 0 and status["refused"] == 0 and
             status["failures"] == int(label == "legacy"), "SPARSE_PUBLIC_PROVIDER_SETTLEMENT")
    check()


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for option in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+option, required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "SPARSE_PUBLIC_INVOCATION")
    need(output.is_absolute() and output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         not output.exists() and output.parent.is_dir() and output.parent.resolve(strict=True) == output.parent,
         "SPARSE_PUBLIC_FRESH_OUTPUT")
    protected = [Path(args.package), Path(args.python_runtime), Path(args.lean_runtime), LEGACY.parent]
    need(all(path.is_absolute() and not output.is_relative_to(path) and not path.is_relative_to(output)
             for path in protected), "SPARSE_PUBLIC_OUTPUT_SUPPORT_OVERLAP")
    output.mkdir()
    report = dict(passed=False, assertions_passed=False, profile_sha256=args.profile_sha256,
        legacy_provider_sha256=LEGACY_SHA256,
        authority="TWO_REAL_PUBLIC_FINDS_LOOPBACK_SYNTHETIC_METADATA_NOT_MATHEMATICS_OR_TLS",
        forwarding_boundary="DIRECTORY_CAPTURE_DOUBLES_AND_CUSTODY_PATH_ONLY_DOUBLE_DECLARED")
    try:
        loaded = load_package(args)
        report["semantic_id"] = loaded.installation.semantic_id
        asyncio.run(scenario(args, output, loaded, report))
        report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:1000])
    report.update(wall_seconds=time.monotonic()-START_WALL, harness_cpu_seconds=time.process_time()-START_CPU)
    save(output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

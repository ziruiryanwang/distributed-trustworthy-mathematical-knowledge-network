"""One prospective real-package/public-find loopback smoke; root owns launch.

No native invocation, existing mathematical state, external network or mocks.
A stalls an offer; B serves one synthetic inert V3 record through the installed
provider. A separate real public launcher avoids preloaded-module pollution.
All outputs are retained. A pass is integration evidence, not mathematics.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
import asyncio
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
DEADLINE = START_WALL + 80
MIB = 1024**2


def need(condition, code):
    if not condition:
        raise ValueError(code)


def check():
    need(time.monotonic() < DEADLINE and time.process_time()-START_CPU < 45,
         "SMOKE_ORIGINAL_ENVELOPE_EXHAUSTED")


def read(path, maximum=2*MIB):
    check()
    size = path.stat().st_size
    need(0 < size <= maximum, "SMOKE_READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size, "SMOKE_READ_CHANGED")
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(raw) <= 2*MIB, "SMOKE_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw+b"\n")


def load_package(args):
    """Bind the loader before executing it; then use its unchanged full checks."""
    root = Path(args.package)
    need(root.is_absolute() and root.resolve(strict=True) == root, "SMOKE_PACKAGE_PATH")
    raw = read(root/"PROFILE.json")
    need(hashlib.sha256(raw).hexdigest() == args.profile_sha256, "SMOKE_PROFILE_PIN")
    descriptor = json.loads(raw)
    pin = descriptor["files"]["profile.py"]
    loader_raw = read(root/"profile.py")
    need(len(loader_raw) == pin["bytes"] and
         hashlib.sha256(loader_raw).hexdigest() == pin["sha256"], "SMOKE_LOADER_PIN")
    spec = importlib.util.spec_from_file_location("_fair_smoke_profile", root/"profile.py")
    loader = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = loader
    exec(compile(loader_raw, str(root/"profile.py"), "exec"), loader.__dict__)
    loaded = loader.load(root, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        DEADLINE, check_parent=check)
    return loader, loaded


class Connections:
    """Observe original handlers; never replace protocol replies or validation."""
    def __init__(self):
        self.rows, self.tasks, self.writers = [], [], []

    async def observe(self, role, reader, writer, handler):
        row = dict(role=role, entered=time.monotonic()-START_WALL, closed=False)
        self.rows.append(row)
        self.tasks.append(asyncio.current_task())
        self.writers.append(writer)
        try:
            need(len(self.rows) <= 8, "SMOKE_CONNECTION_CENSUS")
            await handler(reader, writer, row)
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
            row["finished"] = time.monotonic()-START_WALL

    async def close(self):
        for writer in self.writers:
            writer.close()
        live = [task for task in self.tasks if not task.done()]
        for task in live:
            task.cancel()
        if live:
            async with asyncio.timeout(max(0.001, min(3, DEADLINE-time.monotonic()))):
                await asyncio.gather(*live, return_exceptions=True)
        need(all(task.done() for task in self.tasks), "SMOKE_HANDLER_STILL_LIVE")


async def scenario(args, output, loaded, report):
    from discovery import discovery_store as DS
    from discovery import formal_features as F
    from discovery.ordinary_export_adapter import OrdinaryExportAdapter, compile_query
    from transport import http_provider as H
    import portable_preview as P

    adapter = OrdinaryExportAdapter(loaded.installation.semantic_id)
    name = [[0, {"$bytes": list(b"FairSearchSyntheticClaim")}]]
    # Deliberately only a well-formed claim: no evidence unit or proof is created.
    raw = F.compact(dict(schema=P.SCHEMA, semantic_id=loaded.installation.semantic_id,
        unit_id=hashlib.sha256(b"fair-smoke-no-mathematical-evidence").hexdigest(),
        export_name=name, header=[2, [], [loaded.A.E.EXPR_FORMAT, [[0]], [[1, 0]], 0]],
        type_bindings=[]))
    specs = [{"tag": "declaration-kind", "value": "theorem"},
             {"tag": "result-head", "head": {"tag": "sort"}}]
    features = compile_query(adapter.namespace, specs)
    expected = adapter.extract(raw)
    need(expected["schema"] == F.ORDINARY_EXPORT_RECORD_SCHEMA == "DMKN_FORMAL_FEATURE_RECORD_V3" and
         set(features) <= set(expected["features"]), "SMOKE_ORDINARY_V3_RECORD")
    with (output/"SYNTHETIC-PREVIEW.json").open("xb") as stream:
        stream.write(raw)
    save(output/"EXPECTED-RECORD.json", expected)
    connections = Connections()
    index = provider = stalled_server = process = None
    cleanup_errors = []

    class ObservedProvider(H.Provider):
        async def _serve(self, reader, writer):
            async def original(r, w, row):
                await super(ObservedProvider, self)._serve(r, w)
            await connections.observe("b", reader, writer, original)

    async def stalled(reader, writer):
        async def wait_for_client(r, w, row):
            async with asyncio.timeout(max(0.001, min(15, DEADLINE-time.monotonic()))):
                first, headers, count, _ = await H._headers(r)
                need(first == "POST "+H.OFFER_ROUTE+" HTTP/1.1" and "host" in headers,
                     "SMOKE_A_EXACT_OFFER_ROUTE")
                need(0 < count <= H.REQUEST_MAX, "SMOKE_A_REQUEST_BOUND")
                request = F.strict(await H._body(r, count), H.REQUEST_MAX)
                H._offer_request(request)
                need(request["namespace"] == adapter.namespace and request["features"] == features,
                     "SMOKE_A_QUERY_BINDING")
                row["offer_received"] = True
                need(await r.read(1) == b"", "SMOKE_A_UNEXPECTED_EXTRA_BYTES")
                row["client_eof_observed"] = True
        await connections.observe("a", reader, writer, wait_for_client)

    try:
        check()
        index = DS.Store(output/"fresh-index", adapter,
            dict(max_objects=1, max_postings=64, max_features=64, max_snapshots=2,
                 max_logical_bytes=2*MIB, max_db_pages=256), create=True)
        admitted = index.admit(raw, expected_id=expected["object_id"])
        need(admitted["record"] == expected and index.status()["objects"] == 1,
             "SMOKE_EXACT_SINGLE_RECORD_INDEX")
        report["snapshot_id"] = admitted["snapshot_id"]
        provider = ObservedProvider(index=index, max_connections=2, max_requests=4,
                                    max_reply_bytes=MIB, operation_ms=5000)
        endpoint_b = await provider.start("127.0.0.1", 0)
        stalled_server = await asyncio.start_server(stalled, "127.0.0.1", 0,
                                                    limit=H.HEADER_MAX, backlog=2)
        endpoint_a = H.Endpoint("127.0.0.1", stalled_server.sockets[0].getsockname()[1])
        contacts = {label: dict(host=ep.host, port=ep.port, tls=False, server_name=None,
                               ca_file=None, ca_sha256=None)
                    for label, ep in (("a", endpoint_a), ("b", endpoint_b))}
        limits = dict(providers=2, snapshots=4, requests=8, pages=4, examined=32,
                      candidates=8, bytes=MIB, wall_ms=25000, inflight=1)
        config = dict(contacts=contacts, providers=["a", "b"], specs=specs, limits=limits,
            offer=dict(max_bytes=65536, max_expanded_bytes=MIB, max_age_ms=25000),
            page=dict(scanned=8, matches=4, bytes=65536, timeout_ms=1000,
                      record_probes=64, node_reads=100000, hash_calls=2000000, sql_vm_steps=1000000))
        save(output/"find.json", config)
        config_sha = hashlib.sha256(read(output/"find.json")).hexdigest()
        # This fixed single call fits the original harness allowance or refuses.
        check()
        need(DEADLINE-time.monotonic() >= 66, "SMOKE_NO_ROOM_FOR_FIXED_PUBLIC_CALL")
        argv = [str(Path(args.python_runtime)/"python.exe"), "-I", "-S", "-B",
            str(Path(args.package)/"run.py"), "--profile-sha256", args.profile_sha256,
            "--python-runtime", args.python_runtime, "--lean-runtime", args.lean_runtime,
            "--diagnostics", str(output/"launcher"), "--wall-seconds", "60",
            "--cpu-seconds", "30", "--memory-mib", "768", "--active-processes", "4",
            "--stdout-bytes", str(MIB), "--stderr-bytes", str(MIB), "peer", "--", "find",
            "--config", str(output/"find.json"), "--config-sha256", config_sha,
            "--output", str(output/"public-find")]
        save(output/"PUBLIC-COMMAND.json", dict(argv=argv, cwd=str(ROOT), attempts=1))
        with (output/"launcher-stdout.txt").open("xb") as stdout, \
                (output/"launcher-stderr.txt").open("xb") as stderr:
            process = await asyncio.create_subprocess_exec(*argv, cwd=ROOT,
                stdout=stdout, stderr=stderr, stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW)
            async with asyncio.timeout_at(DEADLINE-5):
                returncode = await process.wait()
        report["launcher_exit_code"] = returncode
        need(returncode == 0, "SMOKE_PUBLIC_LAUNCHER_FAILED")
        launch = json.loads(read(output/"launcher"/"RUN.json"))
        supervision = json.loads(read(output/"launcher"/"SUPERVISION.json"))
        public = json.loads(read(output/"public-find"/"RESULT.json"))
        need(launch["ok"] is True and launch["profile_sha256"] == args.profile_sha256 and
             supervision["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and
             supervision["direct_child_reaped"] is True and supervision["job_closed"] is True and
             supervision["cleanup_errors"] == [] and supervision["final_job"]["active_processes"] == 0,
             "SMOKE_PUBLIC_JOB_NOT_CLOSED")
        need(public["ok"] is True and public["semantic_id"] == loaded.installation.semantic_id and
             public["config_sha256"] == config_sha and public["profile_sha256"] == args.profile_sha256,
             "SMOKE_PUBLIC_RESULT_BINDING")
        result = public["result"]
        need(result["status"] == "INCOMPLETE_SEARCH" and result["global_complete"] is False and
             result["verified_scan_coverage"] is False and result["mathematical_acceptance"] is False,
             "SMOKE_INCOMPLETE_NOT_ACCEPTED")
        need(result["matches"] == [dict(provider="b", snapshot_id=admitted["snapshot_id"], record=expected)],
             "SMOKE_EXACT_LATER_PROVIDER_MATCH")
        need(result["provider_errors"] == [dict(provider="a", phase="offer",
             error=dict(type="SettledRefusal", code="ATTEMPT_TIMEOUT"))], "SMOKE_EXACT_STALLED_REFUSAL")
        session = result["search"]["session"]
        need(session["used"]["requests"] == 3 and session["used"]["pages"] == 1 and
             session["used"]["bytes"] >= config["offer"]["max_bytes"] and
             session["pending_requests"] == 0 and all(v == 0 for v in session["reserved"].values()),
             "SMOKE_CONSERVATIVE_SETTLED_SESSION")
        network = result["network"]
        need(network["closed"] is True and network["pending_requests"] == 0 and
             network["external_prepaid"] == [dict(label="peer-find", requests=8, reply_bytes=MIB)] and
             network["requests"] == 8 and network["charged_reply_bytes"] == MIB,
             "SMOKE_SINGLE_PREPAID_GRANT")
        report.update(public_result=public, public_supervision=supervision, assertions_passed=True)
    finally:
        if process is not None and process.returncode is None:
            try:
                process.kill()
                async with asyncio.timeout(max(0.001, min(3, DEADLINE-time.monotonic()))):
                    await process.wait()
            except BaseException as error:
                cleanup_errors.append("launcher:"+type(error).__name__)
        report["launcher_reaped"] = process is None or process.returncode is not None
        if stalled_server is not None:
            try:
                stalled_server.close()
                async with asyncio.timeout(max(0.001, min(2, DEADLINE-time.monotonic()))):
                    await stalled_server.wait_closed()
            except BaseException as error:
                cleanup_errors.append("stalled_listener:"+type(error).__name__)
        report["stalled_listener_closed"] = stalled_server is None or not stalled_server.is_serving()
        if provider is not None:
            try:
                async with asyncio.timeout(max(0.001, min(3, DEADLINE-time.monotonic()))):
                    await provider.stop()
            except BaseException as error:
                cleanup_errors.append("provider:"+type(error).__name__)
            report["provider"] = provider.status()
            report["provider_listener_closed"] = provider.server is None
        try:
            await connections.close()
        except BaseException as error:
            cleanup_errors.append("connection_observers:"+type(error).__name__)
        report["connections"] = connections.rows
        report["handlers_finished"] = all(task.done() for task in connections.tasks)
        if index is not None:
            try:
                index.close()
            except BaseException as error:
                cleanup_errors.append("index:"+type(error).__name__)
            report["index_closed"] = index.db is None
        report["cleanup_errors"] = cleanup_errors
    need(not cleanup_errors and report["launcher_reaped"] and report["stalled_listener_closed"] and
         report.get("provider_listener_closed") is True and report["handlers_finished"] and
         report.get("index_closed") is True, "SMOKE_CLEANUP_UNCERTAIN")
    rows_a = [row for row in connections.rows if row["role"] == "a"]
    rows_b = [row for row in connections.rows if row["role"] == "b"]
    need(len(rows_a) == 1 and len(rows_b) == 2 and
         rows_a[0].get("offer_received") is True and rows_a[0].get("client_eof_observed") is True and
         all(row["closed"] and "error_type" not in row and "close_error_type" not in row
             for row in connections.rows), "SMOKE_OBSERVED_CONNECTION_CLOSURE")
    need(report["provider"]["requests"] == 2 and report["provider"]["failures"] == 0 and
         report["provider"]["active"] == 0 and report["provider"]["reserved_reply_bytes"] == 0,
         "SMOKE_PROVIDER_SETTLED")
    check()


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for option in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+option, required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "SMOKE_ISOLATED_CANONICAL_INVOCATION")
    need(output.is_absolute() and output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         not output.exists() and output.parent.is_dir() and
         output.parent.resolve(strict=True) == output.parent, "SMOKE_FRESH_ABSOLUTE_OUTPUT")
    protected = [Path(args.package), Path(args.python_runtime), Path(args.lean_runtime)]
    need(all(path.is_absolute() and not output.is_relative_to(path) and not path.is_relative_to(output)
             for path in protected), "SMOKE_OUTPUT_SUPPORT_OVERLAP")
    output.mkdir()
    report = dict(passed=False, assertions_passed=False, profile_sha256=args.profile_sha256,
                  authority="REAL_LOOPBACK_PUBLIC_FIND_SYNTHETIC_METADATA_NOT_MATHEMATICS_OR_TLS")
    try:
        _, loaded = load_package(args)
        report["semantic_id"] = loaded.installation.semantic_id
        asyncio.run(scenario(args, output, loaded, report))
        report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:1000])
    report.update(wall_seconds=time.monotonic()-START_WALL,
                  harness_cpu_seconds=time.process_time()-START_CPU)
    save(output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

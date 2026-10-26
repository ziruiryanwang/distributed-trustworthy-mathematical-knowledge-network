"""One selected public directory-serve -> directory-find loopback integration.

The parent hosts one actual provider with synthetic inert V3 metadata. A separate
public CLI serves the directory; a second public CLI learns the provider through
HTTP using only that directory as a contact. No native/math check, real knowledge
state, external network, mock, retry or automatic grant renewal. Root owns launch.
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
MIB = 1024**2
DEADLINE = START_WALL + 80


def need(ok, code):
    if not ok:
        raise ValueError(code)


def check():
    need(time.monotonic() < DEADLINE and time.process_time()-START_CPU < 45,
         "DIRECTORY_PUBLIC_ORIGINAL_ENVELOPE")


def read(path, maximum=2*MIB):
    check()
    size = path.stat().st_size
    need(0 < size <= maximum, "DIRECTORY_PUBLIC_READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size, "DIRECTORY_PUBLIC_READ_CHANGED")
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(raw) <= 2*MIB, "DIRECTORY_PUBLIC_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw+b"\n")


def load_package(args):
    root = Path(args.package)
    need(root.is_absolute() and root.resolve(strict=True) == root, "DIRECTORY_PUBLIC_PACKAGE_PATH")
    raw = read(root/"PROFILE.json")
    need(hashlib.sha256(raw).hexdigest() == args.profile_sha256, "DIRECTORY_PUBLIC_PROFILE_PIN")
    descriptor = json.loads(raw)
    pin = descriptor["files"]["profile.py"]
    source = read(root/"profile.py")
    need(len(source) == pin["bytes"] and hashlib.sha256(source).hexdigest() == pin["sha256"],
         "DIRECTORY_PUBLIC_LOADER_PIN")
    spec = importlib.util.spec_from_file_location("_directory_public_profile", root/"profile.py")
    loader = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = loader
    exec(compile(source, str(root/"profile.py"), "exec"), loader.__dict__)
    return loader.load(root, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        DEADLINE, check_parent=check)


def command(args, output, operation, config, wall_seconds):
    path = output/(operation+".json")
    save(path, config)
    digest = hashlib.sha256(read(path)).hexdigest()
    argv = [str(Path(args.python_runtime)/"python.exe"), "-I", "-S", "-B",
        str(Path(args.package)/"run.py"), "--profile-sha256", args.profile_sha256,
        "--python-runtime", args.python_runtime, "--lean-runtime", args.lean_runtime,
        "--diagnostics", str(output/(operation+"-launcher")), "--wall-seconds", str(wall_seconds),
        "--cpu-seconds", "25", "--memory-mib", "512", "--active-processes", "3",
        "--stdout-bytes", str(MIB), "--stderr-bytes", str(MIB), "peer", "--", operation,
        "--config", str(path), "--config-sha256", digest,
        "--output", str(output/(operation+"-public"))]
    need(not any(value in argv for value in ("--catalog", "--custody", "--store-id", "--custody-limits")),
         "DIRECTORY_PUBLIC_UNEXPECTED_STATE_ARGUMENT")
    save(output/(operation+"-COMMAND.json"), dict(argv=argv, cwd=str(ROOT), attempts=1))
    return argv, digest


async def ready_report(process, path, report):
    """Observe the same live child; never restart on incomplete file publication."""
    until = min(DEADLINE-51, time.monotonic()+15)
    observations = 0
    while time.monotonic() < until:
        check()
        need(process.returncode is None, "DIRECTORY_PUBLIC_SERVICE_EXITED_BEFORE_READY")
        if path.exists():
            size = path.stat().st_size
            need(size <= 65536, "DIRECTORY_PUBLIC_READY_BOUND")
            if size:
                with path.open("rb") as stream:
                    raw = stream.read(65537)
                need(len(raw) <= 65536, "DIRECTORY_PUBLIC_READY_BOUND")
                try:
                    value = json.loads(raw)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    observations += 1
                else:
                    report["ready_partial_observations"] = observations
                    return value
        await asyncio.sleep(0.05)
    raise ValueError("DIRECTORY_PUBLIC_READY_NOT_OBSERVED")


def public_result(args, output, operation, digest, semantic):
    launch = json.loads(read(output/(operation+"-launcher")/"RUN.json"))
    supervision = json.loads(read(output/(operation+"-launcher")/"SUPERVISION.json"))
    public = json.loads(read(output/(operation+"-public")/"RESULT.json"))
    need(launch["ok"] is True and launch["profile_sha256"] == args.profile_sha256 and
         supervision["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and
         supervision["direct_child_reaped"] is True and supervision["job_closed"] is True and
         supervision["cleanup_errors"] == [] and supervision["final_job"]["active_processes"] == 0,
         "DIRECTORY_PUBLIC_JOB_NOT_CLOSED")
    need(public["ok"] is True and public["operation"] == operation and
         public["semantic_id"] == semantic and public["config_sha256"] == digest and
         public["profile_sha256"] == args.profile_sha256 and public["catalog"] is None and
         public["custody"] is None and public["store_id"] is None,
         "DIRECTORY_PUBLIC_RESULT_BINDING")
    return dict(result=public, supervision=supervision, launcher=launch)


async def scenario(args, output, loaded, report):
    api = loaded.peer_api
    F, H, CD = api.F, api.H, api.CD
    adapter = api.OrdinaryExportAdapter(loaded.installation.semantic_id)
    specs = [{"tag": "declaration-kind", "value": "theorem"},
             {"tag": "result-head", "head": {"tag": "sort"}}]
    features = api.compile_query(adapter.namespace, specs)
    raw = F.compact(dict(schema=api.PP.SCHEMA, semantic_id=loaded.installation.semantic_id,
        unit_id=hashlib.sha256(b"directory-public-synthetic-no-proof-or-evidence").hexdigest(),
        export_name=[[0, {"$bytes": list(b"DirectoryPublicSyntheticClaim")}]],
        header=[2, [], [loaded.A.E.EXPR_FORMAT, [[0]], [[1, 0]], 0]], type_bindings=[]))
    expected = adapter.extract(raw)
    need(expected["schema"] == "DMKN_FORMAL_FEATURE_RECORD_V3" and
         set(features) <= set(expected["features"]), "DIRECTORY_PUBLIC_SYNTHETIC_METADATA")
    with (output/"SYNTHETIC-PREVIEW.json").open("xb") as stream:
        stream.write(raw)
    save(output/"EXPECTED-RECORD.json", expected)
    index = provider = None
    children, rows, tasks, writers, cleanup_errors = {}, [], [], [], []

    class ObservedProvider(H.Provider):
        async def _serve(self, reader, writer):
            row = dict(entered=time.monotonic()-START_WALL, closed=False)
            rows.append(row); tasks.append(asyncio.current_task()); writers.append(writer)
            try:
                need(len(rows) <= 4, "DIRECTORY_PUBLIC_CONNECTION_BOUND")
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

    try:
        index = api.DS.Store(output/"fresh-index", adapter,
            dict(max_objects=1, max_postings=64, max_features=64, max_snapshots=2,
                 max_logical_bytes=2*MIB, max_db_pages=256), create=True)
        admitted = index.admit(raw, expected_id=expected["object_id"])
        need(admitted["record"] == expected and index.status()["objects"] == 1,
             "DIRECTORY_PUBLIC_SINGLE_RECORD")
        provider = ObservedProvider(index=index, max_connections=2, max_requests=4,
                                    max_reply_bytes=MIB, operation_ms=5000)
        endpoint = await provider.start("127.0.0.1", 0)
        hint = dict(host=endpoint.host, port=endpoint.port, tls=False, server_name=None)
        service_config = dict(entries=[dict(specs=specs, endpoints=[hint])],
            host="127.0.0.1", port=0, tls=None, lease_seconds=15, cleanup_seconds=10,
            limits=dict(max_connections=2, max_requests=2, max_reply_bytes=65536, operation_ms=5000))
        service_argv, service_pin = command(args, output, "directory-serve", service_config, 60)
        need(DEADLINE-time.monotonic() >= 66, "DIRECTORY_PUBLIC_NO_ROOM_FOR_SERVICE")
        with (output/"service-stdout.txt").open("xb") as service_out, \
                (output/"service-stderr.txt").open("xb") as service_err, \
                (output/"reader-stdout.txt").open("xb") as reader_out, \
                (output/"reader-stderr.txt").open("xb") as reader_err:
            children["service"] = await asyncio.create_subprocess_exec(*service_argv, cwd=ROOT,
                stdout=service_out, stderr=service_err, stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW)
            ready = await ready_report(children["service"],
                                       output/"directory-serve-public"/"READY.json", report)
            need(ready["status"] == "READY" and ready["host"] == "127.0.0.1" and
                 ready["tls"] is False and ready["namespace"] == adapter.namespace and
                 ready["route_count"] == 1 and ready["contact_count"] == 1 and
                 ready["mathematical_acceptance"] is False and ready["port"] != endpoint.port,
                 "DIRECTORY_PUBLIC_READY_BINDING")
            H.Endpoint(ready["host"], ready["port"]).validate()
            report["ready"] = ready
            seed = dict(host=ready["host"], port=ready["port"], tls=False, server_name=None,
                        ca_file=None, ca_sha256=None)
            search_limits = dict(providers=1, snapshots=2, requests=4, pages=2,
                examined=16, candidates=4, bytes=MIB, wall_ms=15000, inflight=1)
            reader_config = dict(contacts={"directory": seed}, directories=["directory"],
                specs=specs, routes=[specs],
                directory=dict(requests=1, reply_bytes=CD.REPLY_MAX, max_contacts=1,
                    max_bytes=CD.REPLY_MAX, max_age_ms=20000, attempt_timeout_ms=4000),
                egress=dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
                    test_endpoints=[dict(host=endpoint.host, port=endpoint.port)]),
                search=dict(limits=search_limits,
                    offer=dict(max_bytes=65536, max_expanded_bytes=MIB, max_age_ms=15000),
                    page=dict(scanned=8, matches=4, bytes=65536, timeout_ms=1000,
                        record_probes=64, node_reads=100000, hash_calls=2000000, sql_vm_steps=1000000)))
            need(list(reader_config["contacts"]) == ["directory"] and
                 all(row["port"] != endpoint.port for row in reader_config["contacts"].values()),
                 "DIRECTORY_PUBLIC_PROVIDER_NOT_SUPPLIED_TO_READER")
            # The egress port is explicit test permission, not a contact source.
            reader_argv, reader_pin = command(args, output, "directory-find", reader_config, 45)
            need(DEADLINE-time.monotonic() >= 51, "DIRECTORY_PUBLIC_NO_ROOM_FOR_READER")
            children["reader"] = await asyncio.create_subprocess_exec(*reader_argv, cwd=ROOT,
                stdout=reader_out, stderr=reader_err, stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW)
            async with asyncio.timeout_at(DEADLINE-8):
                exits = await asyncio.gather(children["reader"].wait(), children["service"].wait())
            need(exits == [0, 0], "DIRECTORY_PUBLIC_LAUNCHER_FAILURE")
        reader = public_result(args, output, "directory-find", reader_pin, loaded.installation.semantic_id)
        service = public_result(args, output, "directory-serve", service_pin, loaded.installation.semantic_id)
        result, served = reader["result"]["result"], service["result"]["result"]
        key = F.digest("DMKN-ORDINARY-ADVISORY-CONTACT-V1", hint)
        need(result["status"] == "INCOMPLETE_SEARCH" and result["global_complete"] is False and
             result["verified_scan_coverage"] is False and result["mathematical_acceptance"] is False,
             "DIRECTORY_PUBLIC_INCOMPLETE_NOT_MATHEMATICS")
        need(result["matches"] == [dict(provider=key, snapshot_id=admitted["snapshot_id"], record=expected)] and
             len(result["learned_contacts"]) == 1 and result["learned_contacts"][0]["endpoint"] == hint,
             "DIRECTORY_PUBLIC_EXACT_LEARNED_RECORD")
        need(result["directory"]["requests"] == 1 and result["directory"]["truncated"] is False and
             result["lookups"][0]["status"] == "ADVISORY_CONTACTS" and
             result["lookups"][0]["adopted"] == 1 and result["cleanup_errors"] == [],
             "DIRECTORY_PUBLIC_ONE_LOOKUP")
        session = result["search"]["search"]["session"]
        need(session["used"]["requests"] == 2 and session["used"]["pages"] == 1 and
             session["pending_requests"] == 0 and all(value == 0 for value in session["reserved"].values()),
             "DIRECTORY_PUBLIC_ONE_SETTLED_SEARCH")
        budget = result["network"]
        need(budget["closed"] is True and budget["pending_requests"] == 0 and
             budget["requests"] == 5 and budget["charged_reply_bytes"] == MIB+CD.REPLY_MAX and
             budget["external_prepaid"] == [dict(label="directory-find", requests=1, reply_bytes=CD.REPLY_MAX),
                 dict(label="peer-find", requests=4, reply_bytes=MIB)], "DIRECTORY_PUBLIC_ONE_GRANT")
        need(served["status"] == "LEASE_FINISHED" and served["quiescent"] is True and
             served["ready"] == ready and served["cleanup_errors"] == [] and
             served["provider"]["requests"] == 1 and served["provider"]["failures"] == 0 and
             served["provider"]["active"] == 0 and served["provider"]["reserved_reply_bytes"] == 0,
             "DIRECTORY_PUBLIC_SERVICE_CLOSED")
        report.update(reader=reader, service=service, assertions_passed=True)
    finally:
        for label, process in children.items():
            if process.returncode is None:
                try:
                    process.kill()
                    async with asyncio.timeout(max(0.001, min(3, DEADLINE-time.monotonic()))):
                        await process.wait()
                except BaseException as error:
                    cleanup_errors.append(label+":"+type(error).__name__)
        report["children_reaped"] = {name: process.returncode is not None for name, process in children.items()}
        if provider is not None:
            try:
                async with asyncio.timeout(max(0.001, min(3, DEADLINE-time.monotonic()))):
                    await provider.stop()
            except BaseException as error:
                cleanup_errors.append("provider:"+type(error).__name__)
            report["provider"] = provider.status()
            report["provider_listener_closed"] = provider.server is None
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
        report["connections"], report["handlers_finished"] = rows, all(task.done() for task in tasks)
        if index is not None:
            try: index.close()
            except BaseException as error: cleanup_errors.append("index:"+type(error).__name__)
            report["index_closed"] = index.db is None
        report["cleanup_errors"] = cleanup_errors
    need(not cleanup_errors and report["children_reaped"] == {"service": True, "reader": True} and
         report.get("provider_listener_closed") is True and report["handlers_finished"] and
         report.get("index_closed") is True, "DIRECTORY_PUBLIC_CLEANUP_UNCERTAIN")
    need(len(rows) == 2 and all(row["closed"] and "error_type" not in row and
         "close_error_type" not in row for row in rows), "DIRECTORY_PUBLIC_PROVIDER_CONNECTIONS")
    need(report["provider"]["requests"] == 2 and report["provider"]["failures"] == 0 and
         report["provider"]["active"] == 0 and report["provider"]["reserved_reply_bytes"] == 0,
         "DIRECTORY_PUBLIC_PROVIDER_SETTLED")
    check()


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for option in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+option, required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "DIRECTORY_PUBLIC_INVOCATION")
    need(output.is_absolute() and output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         not output.exists() and output.parent.is_dir() and output.parent.resolve(strict=True) == output.parent,
         "DIRECTORY_PUBLIC_FRESH_OUTPUT")
    protected = [Path(args.package), Path(args.python_runtime), Path(args.lean_runtime)]
    need(all(path.is_absolute() and not output.is_relative_to(path) and not path.is_relative_to(output)
             for path in protected), "DIRECTORY_PUBLIC_OUTPUT_SUPPORT_OVERLAP")
    output.mkdir()
    report = dict(passed=False, assertions_passed=False, profile_sha256=args.profile_sha256,
                  authority="TWO_REAL_PUBLIC_COMMANDS_LOOPBACK_SYNTHETIC_METADATA_NOT_MATHEMATICS_OR_TLS")
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

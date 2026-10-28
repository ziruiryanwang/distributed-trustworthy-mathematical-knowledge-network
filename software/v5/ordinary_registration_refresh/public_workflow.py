"""Two fresh public refresh cycles under identical registrar configuration.

Source-only until root selects one bounded run. Existing real HashMap query;
public static-feed and refresh commands; direct existing contact reader only.
No mathematical server, owner, database, compiler, proof or automatic retry.
"""
from __future__ import annotations

import time
START, CPU = time.monotonic(), time.process_time()
import argparse
import asyncio
from contextlib import ExitStack
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
DEADLINE = START+100
HELPER = ROOT/"software/v5/ordinary_contact_federation/test_public.py"
HELPER_SHA = "98f3eb0b60e95bcdadca280c636c65ddaa2b6be47793ea43c264ab20abef7879"
QUERY = ROOT/"software/v5/ordinary_finite_map_refinement/find-config02.json"
QUERY_SHA = "eec3a9399a341e2bd1e604c87f123819f099d53864ba99c2e110b9f36f8518c6"
NAMESPACE = "d966de54aa32c6cd059ab9553a0968a320594a63561cadf742cca6265858079c"


def need(ok, code):
    if not ok:
        raise ValueError("REFRESH_PUBLIC_"+code)


def check():
    need(time.monotonic() < DEADLINE and time.process_time()-CPU < 45, "ORIGINAL_ENVELOPE")


def pinned(path, expected):
    check()
    need(path.is_file() and 0 < path.stat().st_size <= 2*MIB, "INPUT_BOUND")
    raw = path.read_bytes()
    need(len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == expected, "INPUT_PIN")
    return raw


def helpers():
    raw = pinned(HELPER, HELPER_SHA)
    spec = importlib.util.spec_from_file_location("_refresh_public_helpers", HELPER)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(HELPER), "exec", dont_inherit=True), module.__dict__)
    # Select this fresh runner's single original envelope before any operations.
    # Only reusable file/CLI/loader helpers are called, never the old scenario.
    module.START_WALL, module.START_CPU, module.DEADLINE = START, CPU, DEADLINE
    return module


async def scenario(args, output, loaded, helper, report):
    api = loaded.peer_api
    H, CD, X = api.H, api.CD, api.X
    specs = json.loads(pinned(QUERY, QUERY_SHA))["specs"]
    namespace = api.OrdinaryExportAdapter(loaded.installation.semantic_id).namespace
    need(namespace == NAMESPACE, "UNCHANGED_NAMESPACE")
    features = api.compile_query(namespace, specs)
    helper.save(output/"SPECS.json", specs)
    report.update(namespace=namespace, query_sha256=QUERY_SHA, cycles=[], reader_attempts=[])
    children, listeners, trap_writers, trap_hits, cleanup_errors = [], [], [], [], []
    refresh_pin = feed_port = None

    def trap(reader, writer):
        trap_hits.append(dict(local=writer.get_extra_info("sockname"),
                              remote=writer.get_extra_info("peername")))
        trap_writers.append(writer)
        writer.close()

    async def launch(stack, cycle, operation, config):
        check()
        need(DEADLINE-time.monotonic() > 51, "NO_CHILD_SLICE")
        argv, digest = helper.command(args, cycle, operation, config, 45)
        out = stack.enter_context((cycle/(operation+"-stdout.txt")).open("xb"))
        err = stack.enter_context((cycle/(operation+"-stderr.txt")).open("xb"))
        child = await asyncio.create_subprocess_exec(*argv, cwd=ROOT, stdin=subprocess.DEVNULL,
            stdout=out, stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
        children.append(child)
        ready = await helper.ready_report(child, cycle/(operation+"-public")/"READY.json", {})
        need(ready["status"] == "READY" and ready["host"] == "127.0.0.1" and
             ready["tls"] is False and ready["namespace"] == namespace and
             ready["mathematical_acceptance"] is False, "READY_BINDING")
        return child, digest, ready, time.monotonic()

    async def contact_read(ready, label, expected):
        check()
        request = dict(schema=CD.REQUEST_SCHEMA, namespace=namespace, features=features,
                       nonce=secrets.token_hex(32), max_contacts=2, max_bytes=32768)
        started = time.monotonic()
        response = await X.exchange(H.Endpoint(ready["host"], ready["port"]),
            H.CONTACT_DIRECTORY_ROUTE, request, 32768, 2000,
            absolute_deadline=min(DEADLINE-8, started+2))
        row = dict(label=label, elapsed_seconds=time.monotonic()-started, request=request)
        report["reader_attempts"].append(row)
        if type(response) is X.SettledRefusal:
            row.update(status="SETTLED_REFUSAL", reason=response.reason)
            need(expected is None and response.reason == "CONNECTION_REFUSED", "READER_REFUSAL")
        else:
            need(expected is not None and type(response) is dict and response["status"] == 200,
                 "READER_STATUS")
            reply = CD.read_reply(response["raw"], request)
            row.update(status="CONTACT_REPLY", reply=reply,
                       wire={key: value for key, value in response.items() if key != "raw"})
            need(reply["contacts"] == [expected] and not reply["truncated"] and
                 reply["global_complete"] is False and reply["mathematical_acceptance"] is False,
                 "EXACT_REPLACED_CONTACT")

    try:
        # These inert observers never provide mathematical or discovery data.
        # Any learned-endpoint dial is recorded and fails the workflow.
        for _ in range(3):
            listeners.append(await asyncio.start_server(trap, "127.0.0.1", 0))
        hints = [dict(host="127.0.0.1", port=server.sockets[0].getsockname()[1],
                      tls=False, server_name=None) for server in listeners]
        hint_a, hint_b, outside = hints
        need(len({row["port"] for row in hints}) == 3, "DISTINCT_OBSERVER_ENDPOINTS")
        egress = dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
            test_endpoints=sorted([dict(host=row["host"], port=row["port"]) for row in hints],
                                  key=lambda row: row["port"]))
        limits = dict(max_connections=2, max_requests=2, max_reply_bytes=65536, operation_ms=2000)
        refresh_config = None
        for number, expected in enumerate((hint_a, hint_b), 1):
            cycle = output/("cycle-"+str(number)); cycle.mkdir()
            cycle_report = dict(cycle=number, expected=expected)
            report["cycles"].append(cycle_report)
            feed = dict(entries=[dict(specs=specs, endpoints=[expected, outside] if number == 1 else [expected])],
                        host="127.0.0.1", port=feed_port or 0, tls=None,
                        lease_seconds=12, cleanup_seconds=10, limits=limits)
            with ExitStack() as stack:
                feed_child, feed_pin, feed_ready, feed_seen = await launch(stack, cycle, "directory-serve", feed)
                if feed_port is None:
                    feed_port = feed_ready["port"]
                    refresh_config = dict(
                        contacts={"library": dict(host="127.0.0.1", port=feed_port, tls=False,
                            server_name=None, ca_file=None, ca_sha256=None)},
                        slots=[dict(feed="library", specs=specs, max_contacts=2, max_bytes=32768)],
                        endpoint_scopes={"library": dict(tls_names=[], endpoints=[hint_a, hint_b])},
                        egress=egress,
                        refresh=dict(requests=1, reply_bytes=32768, attempt_timeout_ms=4000,
                                     max_age_ms=6000, min_service_ms=2000),
                        service=dict(host="127.0.0.1", port=0, tls=None, lease_seconds=30,
                                     cleanup_seconds=10, limits=limits))
                need(feed_ready["port"] == feed_port, "SAME_FEED_ORIGIN")
                refresh_child, pin, ready, refresh_seen = await launch(stack, cycle, "directory-refresh-serve", refresh_config)
                if refresh_pin is None:
                    refresh_pin = pin
                need(pin == refresh_pin and ready["route_count"] == ready["contact_count"] == 1 and
                     ready["selected_slots"] == 1 and ready["refresh_complete"] is (number == 2) and
                     ready["lease_seconds"] == 30 and 2000 <= ready["remaining_ms"] <= 6000 and
                     ready["contact_horizon"] == "LOCAL_MONOTONIC_ISSUANCE_CUTOFF", "REFRESH_READY")
                await contact_read(ready, "cycle-"+str(number), expected)
                # Observe termination against the clipped READY interval plus
                # existing cleanup and a finite wrapper-reporting reserve.
                close_bound = ready["remaining_ms"]/1000+10+3
                async with asyncio.timeout_at(min(DEADLINE-8, refresh_seen+close_bound)):
                    need(await refresh_child.wait() == 0, "REFRESH_CHILD_EXIT")
                refresh_closed = time.monotonic()
                need(refresh_closed-refresh_seen <= close_bound < 30, "CLIPPED_READY_TO_CLOSURE")
                if number == 1:
                    await contact_read(ready, "after-first-cutoff", None)
                async with asyncio.timeout_at(min(DEADLINE-8, feed_seen+12+10+3)):
                    need(await feed_child.wait() == 0, "FEED_CHILD_EXIT")
                cycle_report.update(feed_ready_seconds=feed_seen-START,
                    refresh_ready_seconds=refresh_seen-START,
                    refresh_closed_seconds=refresh_closed-START,
                    refresh_ready_to_close_bound_seconds=close_bound,
                    feed_closed_seconds=time.monotonic()-START)
            served = helper.public_result(args, cycle, "directory-refresh-serve", pin,
                                          loaded.installation.semantic_id)
            fed = helper.public_result(args, cycle, "directory-serve", feed_pin,
                                       loaded.installation.semantic_id)
            result, source = served["result"]["result"], fed["result"]["result"]
            lookup, network, service = result["lookups"][0], result["network"], result["service"]
            need(result["status"] == ("INCOMPLETE_REFRESH_SERVICE_FINISHED" if number == 1 else
                                      "REFRESH_SERVICE_FINISHED") and result["quiescent"] and
                 result["termination"] == "FINITE_SERVICE_CLOSED" and result["cleanup_errors"] == [] and
                 result["ready"] == ready and result["refresh"]["requests"] == 1, "REFRESH_RESULT")
            need(lookup["status"] == "ADVISORY_CONTACTS" and lookup["included"] and
                 lookup["adopted"] == 1 and lookup["rejected"] == (1 if number == 1 else 0) and
                 not lookup["truncated"], "SCOPED_SOURCE_SUBSET")
            need(network["closed"] and network["pending_requests"] == 0 and
                 network["requests"] == 1 and network["charged_reply_bytes"] == 32768 and
                 network["external_prepaid"] == [dict(label="directory-refresh-serve", requests=1,
                                                     reply_bytes=32768)], "ONE_REFRESH_GRANT")
            for item in (service, source):
                need(item["status"] == "LEASE_FINISHED" and item["quiescent"] and
                     item["cleanup_errors"] == [] and item["provider"]["requests"] == 1 and
                     item["provider"]["active"] == item["provider"]["reserved_reply_bytes"] == 0 and
                     item["provider"]["failures"] == 0, "PUBLIC_SERVICE_CLOSED")
            cycle_report.update(feed=fed, refresh=served, feed_ready=feed_ready, refresh_ready=ready)
            need(not trap_hits, "LEARNED_ENDPOINT_WAS_DIALED")
        need(len(report["reader_attempts"]) == 3, "EXACT_READER_ATTEMPTS")
        report.update(registrar_config_sha256=refresh_pin, feed_port=feed_port,
                      assertions_passed=True, learned_endpoint_dials=trap_hits)
    finally:
        for child in children:
            if child.returncode is None:
                try:
                    child.kill()
                    async with asyncio.timeout(3):
                        await child.wait()
                except BaseException as error:
                    cleanup_errors.append("child:"+type(error).__name__)
        for server in listeners:
            server.close()
        for server in listeners:
            try:
                async with asyncio.timeout(2):
                    await server.wait_closed()
            except BaseException as error:
                cleanup_errors.append("observer:"+type(error).__name__)
        for writer in trap_writers:
            writer.close()
            try:
                async with asyncio.timeout(1):
                    await writer.wait_closed()
            except BaseException as error:
                cleanup_errors.append("observer-client:"+type(error).__name__)
        report.update(children_reaped=[child.returncode is not None for child in children],
                      observer_listeners_closed=all(not server.is_serving() for server in listeners),
                      learned_endpoint_dials=trap_hits, cleanup_errors=cleanup_errors)
    need(not cleanup_errors and len(children) == 4 and all(report["children_reaped"]) and
         report["observer_listeners_closed"] and not trap_hits, "CLEANUP")
    pinned(HELPER, HELPER_SHA); pinned(QUERY, QUERY_SHA); check()


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for option in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+option, required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "INVOCATION")
    need(output.is_absolute() and output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         not output.exists() and output.parent.is_dir() and output.parent.resolve(strict=True) == output.parent,
         "FRESH_OUTPUT")
    need(all(not output.is_relative_to(Path(path)) and not Path(path).is_relative_to(output)
             for path in (args.package, args.python_runtime, args.lean_runtime)), "OUTPUT_OVERLAP")
    output.mkdir()
    helper = helpers()
    report = dict(passed=False, assertions_passed=False, profile_sha256=args.profile_sha256,
                  authority="PUBLIC_CONTACT_MAINTENANCE_LOOPBACK_NOT_MATHEMATICS_OR_INDEPENDENT_HOSTS")
    try:
        loaded = helper.load_package(args)
        report["semantic_id"] = loaded.installation.semantic_id
        asyncio.run(scenario(args, output, loaded, helper, report))
        report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:1000])
    report.update(wall_seconds=time.monotonic()-START, harness_cpu_seconds=time.process_time()-CPU)
    helper.save(output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

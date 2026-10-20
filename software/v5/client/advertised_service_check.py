"""One data-only check of ordinary hosting through existing located search.

Two real retained Node roles, one new service entry, one synthetic descriptor.
No proof owner, Lean check, receipt creation, authoring or mathematical READY.
Run only through the exact source-selected enclosing Job, not as a daemon.
"""
import argparse
import asyncio
import hashlib
import json
from pathlib import Path
import socket
import sys
import time

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE/"portable_runtime"), str(SOURCE)]
from client import serve_advertised as S
from client import test_serve_workspace as T
from discovery import formal_features as F
from discovery.module_export_adapter import compile_query
from location import protocol as P
from location.controller import AdoptedLocationRuntime, SOURCE_NAMES
from location.controller_services import ROLE_NAMES, ServiceLocatedWorkflow, ServiceLocationProcess

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
BASE = PROJECT/"product-local/v4-library-commons-02/commons-v4"
MIB = 1024**2


def ports():
    """Reserve three different ephemeral choices, then release; no retry."""
    sockets = []
    try:
        for _ in range(3):
            stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockets.append(stream)
            stream.bind(("127.0.0.1", 0))
        return tuple(stream.getsockname()[1] for stream in sockets)
    finally:
        for stream in sockets:
            stream.close()


def limits(service_ms):
    return dict(service_ms=service_ms, operation_ms=10000, query_events=256,
        provider_limit=2, advertised_keys=1, provider_ttl_ms=120000,
        reprovide_interval_ms=30000, maintenance_ms=60000, commands=24,
        descriptor_requests=4, descriptor_reply_bytes=16384, metadata={},
        transport=dict(outbound_attempts=32, inbound_upgrades=32,
                       receive_bytes=2*MIB, send_bytes=2*MIB))


async def operation(output):
    T.OUTPUT = output
    fixture_owner = T.ServingControls("test_existing_data_offer_group_finite_stop_and_reopen")
    fixture_owner.setUp()
    fixture = fixture_owner.fixture()
    context = fixture_owner.context(fixture, lifetime=45)
    context.installation = BASE
    context.deadline = time.monotonic()+105
    context.source_sha256.update({
        "portable/location/"+name: hashlib.sha256(
            (SOURCE/"portable_runtime/location"/name).read_bytes()).hexdigest()
        for name in SOURCE_NAMES | ROLE_NAMES})
    reader_port, provider_port, http_port = ports()
    policy = {"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test",
        "public_ports": [], "test_endpoints": [
            {"host": "127.0.0.1", "port": value}
            for value in sorted((reader_port, provider_port, http_port))]}
    features = compile_query(fixture.namespace, [
        {"tag": "declaration-kind", "value": "theorem"},
        {"tag": "result-head", "head": {"tag": "sort"}}])
    reader_root = output/"reader"
    reader_root.mkdir()
    adoption = AdoptedLocationRuntime(SOURCE/"portable_runtime/location",
        {name: context.source_sha256["portable/location/"+name] for name in SOURCE_NAMES},
        installation_root=BASE, workspace_root=reader_root)
    reader = ServiceLocationProcess(adoption,
        {name: context.source_sha256["portable/location/"+name] for name in ROLE_NAMES},
        {"schema": "DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", "role": "reader",
         "state": str(reader_root/"state"), "namespace": fixture.namespace,
         "egress": policy, "listen": [f"/ip4/127.0.0.1/tcp/{reader_port}"],
         "announce": [], "bootstrap": [], "endpoints": [], "limits": limits(95000)},
        reader_root/"channel", deadline=context.deadline-8)
    report = {"status": "FAIL", "service": None, "reader": None, "cleanup_errors": [],
        "mathematical_acceptance": False, "global_complete": False,
        "real_node_roles": 2, "native_calls": 0, "proof_calls": 0,
        "fixture": "SYNTHETIC_STRUCTURAL_DESCRIPTOR_WITH_NO_MATHEMATICAL_WARRANT",
        "consumer_contact_input": "EXACT_EGRESS_ALLOWLIST_AND_FORMAL_QUERY_NOT_CONFIGURED_HTTP_CONTACT",
        "scope": "SAME_HOST_COMPOSED_SERVICE_AND_EXISTING_AUTHENTICATED_SEARCH"}
    task = None
    try:
        ready = await reader.start()
        F.need(ready["status"] == "RUNNING" and ready["role"] == "reader", "CHECK_READER_START")
        bootstrap = f'/ip4/127.0.0.1/tcp/{reader_port}/p2p/{P.peer_id(ready["peer_id"])}'
        context.parameters["schema"] = S.SCHEMA
        context.parameters["bind"]["port"] = http_port
        context.parameters["service_limits"].update(
            max_requests=4, max_reply_bytes=MIB, operation_ms=5000)
        context.parameters["location"] = {
            "installation_root": str(BASE), "egress": policy,
            "listen": [f"/ip4/127.0.0.1/tcp/{provider_port}"], "announce": [],
            "bootstrap": [bootstrap], "limits": limits(70000),
            "routes": [{"features": features, "stripe": 0}], "health_interval_ms": 5000}
        task = asyncio.create_task(S.serve(context))
        ready_path = context.location_workspace/"service-ready.json"
        # Local test synchronization only; no network retries or new allowance.
        while not ready_path.exists():
            F.need(not task.done(), "CHECK_SERVICE_ENDED_BEFORE_READY")
            F.need(time.monotonic() < context.deadline-25, "CHECK_READY_DEADLINE")
            await asyncio.sleep(0.02)
        service_ready = json.loads(ready_path.read_bytes())
        F.need(service_ready["namespace"] == fixture.namespace
               and service_ready["mathematical_acceptance"] is False, "CHECK_SERVICE_READY")
        # Start from a formal query. No provider endpoint or provider identity
        # from service_ready enters the reader's route/descriptor/search path.
        search_limits = dict(providers=1, snapshots=1, requests=2, pages=1,
            examined=4, candidates=4, bytes=262144, wall_ms=25000, inflight=1)
        route_limits = dict(wall_ms=25000, route_operations=1, routing_events=256,
            routing_peer_slots=2, descriptor_requests=1, contacts=1, reply_bytes=266240)
        workflow = ServiceLocatedWorkflow(reader, fixture.namespace, features,
            route_limits, search_limits, P.OwnerEgressPolicy(policy))
        route = await workflow.route(features, 0, event_cap=256, peer_cap=2)
        F.need(len(route["peers"]) == 1, "CHECK_ONE_LOCATED_PROVIDER")
        descriptor = await workflow.descriptor(route["peers"][0], route["route_key"],
                                               max_bytes=4096, max_age_ms=25000)
        search = workflow.begin_search()
        F.need(len(search.endpoints) == 1, "CHECK_ONE_DISCOVERED_ENDPOINT")
        contact = next(iter(search.endpoints))
        endpoint = search.endpoints[contact]
        F.need({name: getattr(endpoint, name) for name in ("host", "port", "tls", "server_name")}
               == service_ready["endpoint"], "CHECK_DESCRIPTOR_LIVE_HTTP_BINDING")
        offer = await search.offer(contact, 65536, max_expanded_bytes=131072, max_age_ms=20000)
        F.need(offer["status"] == "OFFERED", "CHECK_AUTHENTICATED_OFFER")
        partition = next(row for row in offer["partitions"] if row["anchor_count"] > 0)
        page = await search.page(contact, offer["snapshot_id"], partition["partition"], 0,
            dict(examined=4, matches=4, bytes=65536, timeout_ms=1000, node_reads=4096))
        F.need(page["status"] == "VERIFIED_PAGE" and len(page["matches"]) == 1
               and page["matches"][0]["object_id"] == fixture.record["object_id"],
               "CHECK_AUTHENTICATED_EXPECTED_MATCH")
        report.update(route=route, descriptor=descriptor, offer=offer, page=page,
                      workflow=workflow.report(), service_ready=service_ready)
        report["service"] = await task
        F.need(report["service"]["status"] == "PASS", "CHECK_COMPOSED_SERVICE_PASS")
        F.need(report["service"]["counters"]["requests"] == 2, "CHECK_EXACT_HTTP_REQUESTS")
        fixture_owner.reopen(fixture)
        report["workspace_reopened"] = True
        report["status"] = "PASS"
    except BaseException as error:
        report["error"] = {"type": type(error).__name__, "message": str(error)[:1000]}
    finally:
        if task is not None and not task.done():
            task.cancel()
        if task is not None:
            result = await asyncio.gather(task, return_exceptions=True)
            if report["service"] is None and isinstance(result[0], dict):
                report["service"] = result[0]
        try:
            if not reader.closed and not reader.channel_failed and reader.process is not None \
                    and reader.process.returncode is None:
                await reader.command("stop", {}, until=min(reader.deadline, time.monotonic()+5))
        except BaseException as error:
            report["cleanup_errors"].append("reader-stop:"+str(error)[:500])
        try:
            await reader.close()
        except BaseException as error:
            report["cleanup_errors"].append("reader-close:"+str(error)[:500])
        report["reader"] = reader.report()
        if not (report["reader"]["closed"] and report["reader"]["returncode"] == 0
                and not report["reader"]["channel_failed"]
                and not report["reader"]["forced_termination"]):
            report["cleanup_errors"].append("READER_UNCLEAN_CLOSE")
        await fixture_owner.asyncTearDown()
        if report["cleanup_errors"] or time.monotonic() >= context.deadline:
            report["status"] = "FAIL"
        with (output/"actual-result.json").open("xb") as stream:
            stream.write(F.compact(report))
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    F.need(Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
           and sys.dont_write_bytecode and not sys.flags.optimize, "CHECK_ISOLATED_OWNER")
    output = Path(args.output)
    F.need(output.is_absolute() and output.resolve() == output and not output.exists()
           and output.is_relative_to(PROJECT/"experiments") and output.parent.is_dir(),
           "CHECK_FRESH_OUTPUT")
    output.mkdir()
    report = asyncio.run(operation(output))
    print(json.dumps({"status": report["status"], "error": report.get("error"),
                      "cleanup_errors": report["cleanup_errors"]}), flush=True)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

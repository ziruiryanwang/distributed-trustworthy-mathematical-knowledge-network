"""One installed public hosting/located-search boundary; no mathematics run.

Selected by the root under the existing outer Windows Job, never a daemon.
Runtime verification stays with the installed public launcher and controllers.
"""
import time
STARTED = time.monotonic()
DEADLINE = STARTED + 570
import argparse
import asyncio
from dataclasses import asdict
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import socket
import subprocess
import sys

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
INSTALLATION = PROJECT/"product-local/v5-distribution-connected-01/Mathematical Commons v5"
MIB = 1024**2
NAME = "installed-advertised-01"
BASE_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
BUILDER_SHA = "8e34df2a98fc3bf017f3d57ea2f92211bbcf156ee801479cbfaf9261f76763a6"
INPUT_SHA = "557269158f76933177eae962cb97c2862a8512709dbee9842051649552573309"


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def ordinary(path, *, directory=False, fresh=False):
    path = Path(path)
    need(path.is_absolute() and path.resolve() == path and all(
        not part.is_symlink() and not part.is_junction() for part in (path, *path.parents)),
        "CHECK_ORDINARY_PATH")
    if fresh:
        need(not path.exists() and path.parent.is_dir(), "CHECK_FRESH_PATH")
    else:
        need(path.is_dir() if directory else path.is_file(), "CHECK_EXISTING_PATH")
    return path


def read(path, maximum=MIB):
    path = ordinary(path)
    size = path.stat().st_size
    need(size <= maximum, "CHECK_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "CHECK_FILE_CHANGED")
    return raw


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def save(path, value):
    raw = encode(value)
    need(len(raw) <= MIB, "CHECK_REPORT_BOUND")
    with ordinary(path, fresh=True).open("xb") as stream:
        stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def pin(path, row, maximum=2*MIB):
    raw = read(path, maximum)
    need(set(row) == {"bytes", "sha256"} and len(raw) == row["bytes"]
         and hashlib.sha256(raw).hexdigest() == row["sha256"], "CHECK_FILE_PIN")
    return raw


def adopt(root, expected):
    need(root == INSTALLATION, "CHECK_SELECTED_INSTALLATION")
    ordinary(root, directory=True)
    raw = read(root/"V5-RELEASE.json", 8*MIB)
    need(hashlib.sha256(raw).hexdigest() == expected, "CHECK_ADOPTED_RELEASE")
    release = json.loads(raw)
    need(release["schema"] == "DMKN_V5_DIRECTORY_RELEASE_V3"
         and release["base_role"] == "mathematical-client-location-v1"
         and release["base_manifest_sha256"] == BASE_SHA
         and release["build_input_sha256"] == INPUT_SHA
         and release["files"]["distribution.py"]["sha256"] == BUILDER_SHA,
         "CHECK_EXACT_CONNECTED_RELEASE")
    sources = release["sdk_sources"]
    need(len(sources) == 106, "CHECK_SDK_COUNT")
    for key, name in sources.items():
        parts = PurePosixPath(key).parts
        need(len(parts) >= 2 and parts[0] in ("v5", "portable")
             and all(part not in ("", ".", "..") for part in parts)
             and PurePosixPath(key).as_posix() == key and name == "sdk/"+key,
             "CHECK_SDK_PATH")
        pin(root.joinpath(*PurePosixPath(name).parts), release["files"][name])
    pin(root/"distribution.py", release["files"]["distribution.py"])
    # Do not redundantly inspect large assets or the 5,896-file Node runtime.
    # The adopted installed entry and each concrete controller own those checks.
    sys.path[:0] = [str(root/"sdk/portable"), str(root/"sdk/v5")]
    return release


def check_origins(root, release):
    prefixes = {PurePosixPath(key).parts[1] for key in release["sdk_sources"]}
    selected = {root/name for name in release["sdk_sources"].values()}
    origins = {}
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] not in prefixes:
            continue
        origin = getattr(module, "__file__", None)
        if origin is None:
            paths = getattr(module, "__path__", ())
            need(paths and all(Path(path).is_relative_to(root/"sdk") for path in paths),
                 "CHECK_NAMESPACE_ORIGIN")
        else:
            path = ordinary(origin)
            need(path in selected, "CHECK_IMPORTED_ORIGIN")
            origins[name] = path.relative_to(root).as_posix()
    for key, name in release["sdk_sources"].items():
        pin(root/name, release["files"][name])
    return origins


def ports():
    streams = []
    try:
        for _ in range(3):
            stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            streams.append(stream)
            stream.bind(("127.0.0.1", 0))
        return [stream.getsockname()[1] for stream in streams]
    finally:
        for stream in streams:
            stream.close()


def limits(service_ms):
    return dict(service_ms=service_ms, operation_ms=10000, query_events=256,
        provider_limit=2, advertised_keys=1, provider_ttl_ms=120000,
        reprovide_interval_ms=30000, maintenance_ms=60000, commands=24,
        descriptor_requests=4, descriptor_reply_bytes=16384, metadata={},
        transport=dict(outbound_attempts=32, inbound_upgrades=32,
                       receive_bytes=2*MIB, send_bytes=2*MIB))


async def operation(root, release_sha, release, output):
    from aggregate_claims import bindings as B
    from client import workspace_atomic as WA
    from discovery.module_export_adapter import compile_query
    from frontier_network import custody as IC
    from location import protocol as P
    from location.controller import AdoptedLocationRuntime, SOURCE_NAMES
    from location.controller_services import ROLE_NAMES, ServiceLocatedWorkflow, ServiceLocationProcess
    from mixed_claims.packet import Envelope
    from modules import codec as C

    report = dict(status="FAIL", mathematical_acceptance=False, global_complete=False,
        scope="SAME_HOST_INSTALLED_PUBLIC_SERVICE_AND_AUTHENTICATED_SEARCH",
        fixture="SYNTHETIC_STRUCTURAL_DESCRIPTOR_WITH_NO_MATHEMATICAL_WARRANT",
        consumer_contact_input="OWNER_ALLOWLIST_AND_FORMAL_QUERY_NOT_CONFIGURED_HTTP_CONTACT",
        proof_calls=0, native_calls=0, real_node_roles=2, cleanup_errors=[],
        started=STARTED, deadline=DEADLINE, installation=str(root), release_sha256=release_sha)
    reader = public = None
    log_tasks = []
    log_streams = []
    config = dict(schema=WA.SCHEMA, wire_profile=IC.public_profile(),
        module_limits=dict(modules=8, groups=16, declarations=32, bodies=8,
                           logical_bytes=MIB, db_pages=256),
        packet_limits=dict(packets=8, offers=16, offers_per_module=4,
                           packet_bytes=65536, logical_bytes=MIB, db_pages=256),
        index_limits=dict(max_objects=8, max_postings=1024, max_features=128,
                          max_snapshots=16, max_logical_bytes=4*MIB, max_db_pages=2048),
        packet_envelope=asdict(Envelope()), max_operations=8,
        max_report_bytes=MIB, ledger_pages=256)
    workspace_path = output/"mathematical-workspace"
    operations, reader_root = output/"operations", output/"reader"
    operations.mkdir(); reader_root.mkdir()
    public_deadline = None
    try:
        workspace = WA.Workspace.open(workspace_path, config, create=True)
        try:
            name = [["s", "syntheticServingDescriptor"]]
            spec = {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
                "groups": [{"kind": "ordinary", "declarations": [{"kind": "theorem",
                    "name": name, "universes": 0, "type": ["sort", ["zero"]],
                    "value_hash": None, "meta": {}}]}]}
            module, opening = C.module_id(spec), C.group_opening(spec, 0)
            workspace.modules.put_group(module, opening)
            descriptor = workspace.adapter.encode_opening(module, name, opening)
            described = workspace.adapter.describe(descriptor)
            need(described["mathematical_acceptance"] is False, "CHECK_SYNTHETIC_NOT_AUTHORITY")
            workspace.index.admit(descriptor, expected_id=C.export_id(module, name))
            namespace = workspace.adapter.namespace
            expected_object = described["record"]["object_id"]
        finally:
            workspace.close()
        reader_port, provider_port, http_port = ports()
        policy = dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test",
            public_ports=[], test_endpoints=[dict(host="127.0.0.1", port=value)
                                            for value in sorted((reader_port, provider_port, http_port))])
        features = compile_query(namespace, [dict(tag="declaration-kind", value="theorem"),
                                             dict(tag="result-head", head=dict(tag="sort"))])
        def source_sha(name):
            key = "portable/location/"+name
            return release["files"][release["sdk_sources"][key]]["sha256"]
        adoption = AdoptedLocationRuntime(root/"sdk/portable/location",
            {name: source_sha(name) for name in SOURCE_NAMES},
            installation_root=root/"base", workspace_root=reader_root)
        reader = ServiceLocationProcess(adoption,
            {name: source_sha(name) for name in ROLE_NAMES},
            dict(schema="DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", role="reader",
                state=str(reader_root/"state"), namespace=namespace, egress=policy,
                listen=[f"/ip4/127.0.0.1/tcp/{reader_port}"], announce=[], bootstrap=[],
                endpoints=[], limits=limits(560000)), reader_root/"channel", deadline=DEADLINE-80)
        async with asyncio.timeout_at(min(DEADLINE-480, time.monotonic()+90)):
            ready = await reader.start()
        need(ready["status"] == "RUNNING" and ready["role"] == "reader", "CHECK_READER_READY")
        bootstrap = f'/ip4/127.0.0.1/tcp/{reader_port}/p2p/{P.peer_id(ready["peer_id"])}'
        child_wall = min(390, math.floor(DEADLINE-time.monotonic()-90))
        need(child_wall >= 350, "CHECK_COLD_LAUNCH_AND_CLOSE_RESERVATION")
        request = dict(schema="DMKN_V5_INSTALLED_REQUEST_V1", name=NAME,
            workspace_root=str(operations), owner=None, runtime_mode=None,
            parameters=dict(schema="DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_V1", mode="atomic",
                workspace_path=str(workspace_path), workspace_config=config,
                bind=dict(host="127.0.0.1", port=http_port), tls=None,
                service_limits=dict(max_connections=2, max_requests=4, max_reply_bytes=MIB,
                                    operation_ms=5000, lifetime_seconds=120),
                location=dict(egress=policy, listen=[f"/ip4/127.0.0.1/tcp/{provider_port}"],
                    announce=[], bootstrap=[bootstrap], limits=limits(150000),
                    routes=[dict(features=features, stripe=0)], health_interval_ms=10000)),
            limits=dict(cpu_seconds=100, wall_seconds=child_wall, memory_mib=384,
                        active_processes=3, stdout_bytes=MIB, stderr_bytes=MIB),
            output_limits=dict(entries=4096, bytes=32*MIB))
        request_path = output/"request.json"
        request_sha = save(request_path, request)
        argv = [str(root/"base/receiver/runtime/python/python.exe"), "-I", "-S", "-B",
                str(root/"distribution.py"), "launch", release_sha, "serve-advertised",
                str(request_path), request_sha]
        report.update(argv=argv, request_sha256=request_sha, child_wall_seconds=child_wall)
        # This cut is fixed before spawn. Interpreter startup cannot renew it.
        public_deadline = min(DEADLINE-90, time.monotonic()+child_wall)
        public = await asyncio.create_subprocess_exec(*argv, cwd=root,
            stdin=subprocess.DEVNULL, stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        async def log_pipe(pipe, name):
            count = 0
            stream = (output/name).open("xb")
            log_streams.append(stream)
            try:
                while True:
                    raw = await pipe.read(65536)
                    if not raw:
                        return count
                    count += len(raw)
                    need(count <= MIB, "CHECK_PUBLIC_LOG_BOUND")
                    stream.write(raw)
            except BaseException:
                if public.returncode is None:
                    public.kill()
                raise
            finally:
                stream.close()
        log_tasks = [asyncio.create_task(log_pipe(public.stdout, "public-stdout.txt")),
                     asyncio.create_task(log_pipe(public.stderr, "public-stderr.txt"))]
        run = operations/NAME
        ready_path = run/"work/service-ready.json"
        while not ready_path.exists():
            need(public.returncode is None, "CHECK_PUBLIC_ENDED_BEFORE_READY")
            need(time.monotonic() < public_deadline-100, "CHECK_PUBLIC_READY_RESERVE")
            await asyncio.sleep(0.05)
        service_ready = json.loads(read(ready_path))
        need(service_ready["namespace"] == namespace
             and service_ready["mathematical_acceptance"] is False
             and service_ready["deadline"]-time.monotonic() >= 25,
             "CHECK_LIVE_READY_QUERY_WINDOW")
        workflow = ServiceLocatedWorkflow(reader, namespace, features,
            dict(wall_ms=25000, route_operations=1, routing_events=256,
                 routing_peer_slots=2, descriptor_requests=1, contacts=1, reply_bytes=266240),
            dict(providers=1, snapshots=1, requests=2, pages=1, examined=4,
                 candidates=4, bytes=262144, wall_ms=25000, inflight=1), P.OwnerEgressPolicy(policy))
        route = await workflow.route(features, 0, event_cap=256, peer_cap=2)
        need(len(route["peers"]) == 1, "CHECK_ONE_LOCATED_PROVIDER")
        acquired = await workflow.descriptor(route["peers"][0], route["route_key"],
                                             max_bytes=4096, max_age_ms=25000)
        search = workflow.begin_search()
        need(len(search.endpoints) == 1, "CHECK_ONE_DISCOVERED_ENDPOINT")
        contact = next(iter(search.endpoints))
        endpoint = search.endpoints[contact]
        need({name: getattr(endpoint, name) for name in ("host", "port", "tls", "server_name")}
             == service_ready["endpoint"], "CHECK_ACQUIRED_LIVE_ENDPOINT")
        offer = await search.offer(contact, 65536, max_expanded_bytes=131072, max_age_ms=20000)
        need(offer["status"] == "OFFERED", "CHECK_OFFER")
        partition = next(row for row in offer["partitions"] if row["anchor_count"] > 0)
        page = await search.page(contact, offer["snapshot_id"], partition["partition"], 0,
            dict(examined=4, matches=4, bytes=65536, timeout_ms=1000, node_reads=4096))
        need(page["status"] == "VERIFIED_PAGE" and len(page["matches"]) == 1
             and page["matches"][0]["object_id"] == expected_object, "CHECK_EXACT_INDEX_RESULT")
        report.update(route=route, descriptor=acquired, offer=offer, page=page,
                      workflow=workflow.report(), service_ready=service_ready)
        await asyncio.wait_for(public.wait(), max(0.001, public_deadline-time.monotonic()))
        need(public.returncode == 0, "CHECK_INSTALLED_PUBLIC_SUCCESS")
        report["public_logs"] = await asyncio.gather(*log_tasks)
        launch = json.loads(read(run/"RESULT.json"))
        boot = json.loads(read(run/"BOOT-RESULT.json"))
        service = json.loads(read(run/"work/service-result.json"))
        plan = json.loads(read(operations/(NAME+"-request")/"launch.json"))
        need(launch["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED"
             and launch["result"]["final_job"]["active_processes"] == 0
             and not launch["result"]["cleanup_errors"]
             and boot["status"] == "OWNER_EXITED_ZERO", "CHECK_PUBLIC_CLOSURE")
        need(plan["installation_root"] == str(root/"base")
             and plan["source_roots"] == dict(v5=str(root/"sdk/v5"),
                 portable=str(root/"sdk/portable"), owner=str(root/"owners"))
             and plan["owner_entry"] == "serve-advertised.py"
             and plan["parameters"]["location"]["installation_root"] == str(root/"base")
             and "runtime_adoption" not in plan["parameters"], "CHECK_INSTALLED_ROLE_BINDING")
        need(service["status"] == "PASS" and service["counters"]["requests"] == 2
             and service["health_checks"] >= 3 and len(service["route_dispatch"]) == 1
             and service["location_status"]["status"] == "STOPPED"
             and service["cleanup"] == dict(location_closed=True, http_closed=True,
                                            workspace_closed=True, errors=[]), "CHECK_SERVICE_CLOSED")
        for channel in (reader_root/"channel", run/"work/location-channel"):
            source_map = json.loads(read(channel/"source-map.json"))
            need(source_map["installation_root"] == str(root/"base")
                 and source_map["manifest_sha256"] == BASE_SHA, "CHECK_NODE_INSTALLED_BASE")
            expected_source = root/"sdk/portable/location" if channel.parent == reader_root else run/"sources/portable/location"
            need(source_map["root"] == str(expected_source), "CHECK_NODE_SOURCE_ORIGIN")
        workspace = WA.Workspace.open(workspace_path, config, create=False)
        workspace.close()
        report.update(public_launch=launch, public_boot=boot, service=service,
                      workspace_reopened=True, status="PASS")
    except BaseException as error:
        report["error"] = dict(type=type(error).__name__, message=str(error)[:1000])
    finally:
        if public is not None and public.returncode is None:
            try:
                # Preserve the service's normal finite shutdown even if query assertions fail.
                await asyncio.wait_for(public.wait(), max(0.001, public_deadline-time.monotonic()))
            except BaseException as error:
                report["cleanup_errors"].append("public-wait:"+str(error)[:300])
                if public.returncode is None:
                    public.kill()
                await public.wait()
        if log_tasks:
            results = await asyncio.gather(*log_tasks, return_exceptions=True)
            for value in results:
                if isinstance(value, BaseException):
                    report["cleanup_errors"].append("public-log:"+str(value)[:300])
        if reader is not None:
            try:
                if not reader.closed and not reader.channel_failed and reader.process is not None \
                        and reader.process.returncode is None:
                    stopped = await reader.command("stop", {}, until=min(reader.deadline, time.monotonic()+10))
                    need(stopped["status"] == "STOPPED", "CHECK_READER_STOP")
                await reader.close()
            except BaseException as error:
                report["cleanup_errors"].append("reader-close:"+str(error)[:300])
                try:
                    await reader.close()
                except BaseException as nested:
                    report["cleanup_errors"].append("reader-reap:"+str(nested)[:300])
            report["reader"] = reader.report()
            state = report["reader"]
            if not (state["closed"] and state["returncode"] == 0
                    and not state["channel_failed"] and not state["forced_termination"]):
                report["cleanup_errors"].append("READER_UNCLEAN_CLOSE")
        try:
            report["reader_imported_origins"] = check_origins(root, release)
            need(hashlib.sha256(read(root/"V5-RELEASE.json", 8*MIB)).hexdigest() == release_sha,
                 "CHECK_RELEASE_CHANGED")
        except BaseException as error:
            report["cleanup_errors"].append("source-final:"+str(error)[:300])
        report["finished"] = time.monotonic()
        report["wall_seconds"] = report["finished"]-STARTED
        if report["cleanup_errors"] or report["finished"] >= DEADLINE:
            report["status"] = "FAIL"
        save(output/"actual-result.json", report)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--installation", required=True)
    parser.add_argument("--release-sha", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(Path.cwd() == PROJECT and os.name == "nt" and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "CHECK_CANONICAL_ISOLATED_OWNER")
    root = Path(args.installation)
    release = adopt(root, args.release_sha)
    output = ordinary(args.output, directory=True, fresh=True)
    need(output.is_relative_to(PROJECT/"experiments") and not output.is_relative_to(root),
         "CHECK_FRESH_OUTPUT_SCOPE")
    output.mkdir()
    report = asyncio.run(operation(root, args.release_sha, release, output))
    print(json.dumps(dict(status=report["status"], error=report.get("error"),
                         cleanup_errors=report["cleanup_errors"])), flush=True)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""One installed, finite retained-placement restart and goal-only acquisition.

Trusted local smoke owner; no verifier/native/proof call or trust adoption.
The installed SDK and runtime are used in place, never copied or overlaid.
"""
import time
STARTED = time.monotonic()
OUTER = STARTED + 280
import argparse
import asyncio
from copy import deepcopy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import socket
import sys

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
INSTALLATION = PROJECT/"product-local/v5-distribution-consolidated-01/Mathematical Commons v5"
SOURCE = Path(__file__).resolve().parents[1]
MIB = 1024**2
BASE_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
# Same eighteen binary/runtime pins selected by actual02 and the root selector;
# do not mistake these for the entire bundled Python standard-library census.
PYTHON_RUNTIME = (
    "python.exe", "python3.dll", "python314.dll", "vcruntime140.dll", "vcruntime140_1.dll",
    "DLLs/_asyncio.pyd", "DLLs/_overlapped.pyd", "DLLs/_socket.pyd", "DLLs/select.pyd",
    "DLLs/_ssl.pyd", "DLLs/libssl-3.dll", "DLLs/libcrypto-3.dll", "DLLs/_hashlib.pyd",
    "DLLs/_sqlite3.pyd", "DLLs/sqlite3.dll", "DLLs/_queue.pyd", "DLLs/_ctypes.pyd", "DLLs/libffi-8.dll",
)
HELPERS = {
    "formal_terms": ("examples/mirror_method/method_query.py", "0ddbc8dac7e60180f3f9aad3216873158d8b2722a9d31c48112e20262298c642"),
    "congruence_query": ("examples/terminal_i/congruence_query.py", "07a323edd3b10f94f6fc7f9790191b1145666b547b4575c70c4a7261b3d8fadd"),
}
FIXTURES = {
    "receipt": (223594, "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"),
    "journal": (184, "22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682"),
    "bundle": (53769, "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926"),
}
OPENING = (1595, "0c74d294730fc2d005a082aba01350e5a9ab54a5aa797036f35d607ce17c900a")
PACKET = (447887, "a737e8f650e9d3abb4781bb2c85c0e625ed4573b7170d71aff1799dbb54495e3")
HTTP = dict(max_connections=2, max_requests=16, max_reply_bytes=32*MIB, operation_ms=5000)
SEARCH = dict(providers=1, snapshots=1, requests=4, pages=2, examined=8,
              candidates=4, bytes=262144, inflight=1, wall_ms=60000)
LOCATION = dict(route_operations=1, routing_events=256, routing_peer_slots=2,
                descriptor_requests=2, contacts=1, reply_bytes=270336, wall_ms=60000)


def need(ok, code):
    if not ok: raise ValueError(code)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def error_fields(error):
    text = str(error)
    code = text if re.fullmatch(r"[A-Z][A-Z0-9_]{0,127}", text) else "LOCAL_OPERATION_FAILED"
    return dict(error_type=type(error).__name__, error_code=code)


def ordinary(path, *, directory=False):
    path = Path(path)
    need(path.is_absolute() and path.resolve() == path and all(
        not part.is_symlink() and not part.is_junction() for part in (path, *path.parents)), "ORDINARY_PATH")
    need(path.is_dir() if directory else path.is_file(), "EXISTING_PATH")
    return path


def pair(row): return {key: row[key] for key in ("bytes", "sha256")}


def read(row, maximum):
    need(set(row) == {"path", "bytes", "sha256"}, "CLOSED_FILE_PIN")
    path = ordinary(row["path"])
    need(type(row["bytes"]) is int and 0 < row["bytes"] <= maximum
         and path.stat().st_size == row["bytes"], "INPUT_SIZE")
    with path.open("rb") as stream: raw = stream.read(maximum+1)
    need(len(raw) == row["bytes"] and sha(raw) == row["sha256"]
         and path.stat().st_size == len(raw), "INPUT_PIN")
    return raw


def pin(path, row, maximum=2*MIB):
    return read(dict(path=str(path), **pair(row)), maximum)


def save(path, value):
    raw = encode(value)+b"\n"
    need(len(raw) <= MIB and not path.exists(), "FRESH_BOUNDED_REPORT")
    ordinary(path.parent, directory=True)
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "SHORT_WRITE")
        stream.flush(); os.fsync(stream.fileno())


def adopt(request):
    need(Path(request["installation"]) == INSTALLATION, "EXACT_INSTALLATION")
    ordinary(INSTALLATION, directory=True)
    need(Path(request["release"]["path"]) == INSTALLATION/"V5-RELEASE.json"
         and Path(request["build_input"]["path"]) == PROJECT/"experiments/v5-local-checks/distribution-consolidated-01-input.json",
         "EXACT_RELEASE_AND_BUILD_INPUT")
    release = json.loads(read(request["release"], 8*MIB))
    build = json.loads(read(request["build_input"], 8*MIB))
    need(release["schema"] == "DMKN_V5_DIRECTORY_RELEASE_V3"
         and release["base_role"] == "mathematical-client-location-v1"
         and release["base_manifest_sha256"] == BASE_SHA
         and release["build_input_sha256"] == request["build_input"]["sha256"], "EXACT_ADOPTED_RELEASE")
    sources = release["sdk_sources"]
    need(len(sources) == 121 and set(sources) == set(build["sdk_sources"])
         and sum(k.startswith("v5/") and k.endswith(".py") for k in sources) == 100, "EXACT_SDK_CENSUS")
    selected = {}
    for logical, relative in sources.items():
        parts = PurePosixPath(logical).parts
        need(len(parts) >= 2 and parts[0] in ("v5", "portable") and "\\" not in logical
             and all(part not in ("", ".", "..") for part in parts)
             and PurePosixPath(logical).as_posix() == logical and relative == "sdk/"+logical, "SDK_LOGICAL_PATH")
        row = release["files"][relative]
        need(pair(row) == pair(build["sdk_sources"][logical]), "BUILD_INSTALLED_BINDING")
        pin(INSTALLATION/relative, row)
        selected[logical] = dict(path=str(INSTALLATION/relative), **pair(row))
    need(pair(release["files"]["distribution.py"]) == pair(build["distribution_source"]), "INSTALLED_BUILDER_BINDING")
    pin(INSTALLATION/"distribution.py", release["files"]["distribution.py"])
    base = release["files"]["base/RELEASE-MANIFEST.json"]
    need(base["sha256"] == BASE_SHA, "BASE_MANIFEST_BINDING")
    pin(INSTALLATION/"base/RELEASE-MANIFEST.json", base, 8*MIB)
    runtime = {"base/receiver/runtime/python/"+suffix:
               release["files"]["base/receiver/runtime/python/"+suffix] for suffix in PYTHON_RUNTIME}
    need(len(runtime) == 18 and Path(sys.executable).resolve() ==
         INSTALLATION/"base/receiver/runtime/python/python.exe", "INSTALLED_PYTHON_RUNTIME")
    for relative,row in runtime.items(): pin(INSTALLATION/relative, row, 32*MIB)
    prefixes = {PurePosixPath(logical).parts[1] for logical in sources}
    need(not any(name.split(".")[0] in prefixes for name in sys.modules), "NO_EARLY_PRODUCT_IMPORT")
    sys.path[:0] = [str(INSTALLATION/"sdk/v5"), str(INSTALLATION/"sdk/portable")]
    helpers = {}
    for alias,(relative,digest) in HELPERS.items():
        path = ordinary(SOURCE/relative)
        row = dict(path=str(path), bytes=path.stat().st_size, sha256=digest)
        read(row, MIB); need(alias not in sys.modules, "NO_EARLY_GOAL_IMPORT")
        spec = importlib.util.spec_from_file_location(alias, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[alias] = module; spec.loader.exec_module(module)
        helpers[alias] = row
    return release, selected, runtime, helpers


def rebind(request, release, selected, runtime, helpers):
    need(json.loads(read(request["release"], 8*MIB)) == release, "RELEASE_UNCHANGED")
    read(request["build_input"], 8*MIB)
    for row in selected.values(): read(row, 2*MIB)
    for relative,row in runtime.items(): pin(INSTALLATION/relative, row, 32*MIB)
    for relative in ("distribution.py", "base/RELEASE-MANIFEST.json"):
        pin(INSTALLATION/relative, release["files"][relative], 8*MIB)
    for alias,row in helpers.items():
        read(row, MIB)
        need(Path(sys.modules[alias].__file__).resolve() == Path(row["path"]), "GOAL_HELPER_ORIGIN")
    for name in FIXTURES: read(request[name], MIB)
    prefixes = {PurePosixPath(logical).parts[1] for logical in selected}
    paths = {Path(row["path"]) for row in selected.values()}
    origins = {}
    for name,module in tuple(sys.modules.items()):
        if name.split(".")[0] not in prefixes: continue
        origin = getattr(module, "__file__", None)
        if origin is None:
            dirs = getattr(module, "__path__", ())
            need(dirs and all(ordinary(p, directory=True).is_relative_to(INSTALLATION/"sdk") for p in dirs),
                 "INSTALLED_NAMESPACE_ORIGIN")
        else:
            path = ordinary(origin); need(path in paths, "INSTALLED_IMPORT_ORIGIN")
            origins[name] = path.relative_to(INSTALLATION).as_posix()
    return origins


def ports():
    held = []
    try:
        for unused in range(6):
            stream = socket.socket(); held.append(stream); stream.bind(("127.0.0.1", 0))
        numbers = [s.getsockname()[1] for s in held]
        need(len(set(numbers)) == 6, "DISTINCT_PORTS")
        return dict(zip(("source_http", "custody_http", "placement_http", "reader_node", "custody_node1", "custody_node2"), numbers))
    finally:
        for stream in held: stream.close()


def location_limits():
    return dict(service_ms=210000, operation_ms=10000, query_events=256,
        provider_limit=2, advertised_keys=1, provider_ttl_ms=120000,
        reprovide_interval_ms=30000, maintenance_ms=60000, commands=16,
        descriptor_requests=4, descriptor_reply_bytes=16384, metadata={},
        transport=dict(outbound_attempts=32, inbound_upgrades=32, receive_bytes=2*MIB, send_bytes=2*MIB))


def channel(selected, directory, deadline, namespace, policy, port, *, role, endpoints, bootstrap):
    from location.controller import AdoptedLocationRuntime, SOURCE_NAMES
    from location.controller_services import ServiceLocationProcess, ROLE_NAMES
    pins = lambda names: {name:selected["portable/location/"+name]["sha256"] for name in names}
    adoption = AdoptedLocationRuntime(INSTALLATION/"sdk/portable/location", pins(SOURCE_NAMES),
        installation_root=INSTALLATION/"base", workspace_root=directory)
    config = dict(schema="DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", role=role,
        state=str(directory/"location-state"), namespace=namespace, egress=deepcopy(policy),
        listen=[f"/ip4/127.0.0.1/tcp/{port}"], announce=[], bootstrap=bootstrap,
        endpoints=endpoints, limits=location_limits())
    return ServiceLocationProcess(adoption, pins(ROLE_NAMES), config,
                                  directory/"location-channel", deadline=deadline)


def seed(workspace, request):
    from modules import codec as C
    from aggregate_claims import bindings as B
    from evidence_network.packet import pack_terminal_i
    blobs = {}
    for key,identity in FIXTURES.items():
        need((request[key]["bytes"],request[key]["sha256"]) == identity, "FIXTURE_IDENTITY")
        blobs[key] = read(request[key], MIB)
    bundle = C.parse_json(blobs["bundle"])
    module = C.module_id(bundle["spec"]); member = B.member_journal(blobs["journal"])
    need(member["module"] == module and member["summary"] == C.summarize(bundle["spec"]), "FIXTURE_JOURNAL")
    opening = C.group_opening(bundle["spec"], 10)
    name = [["s", "CommonsV5"], ["s", "binary_congr"]]
    need(opening == bundle["openings"][10] and opening["group"]["declarations"][0]["name"] == name,
         "FIXTURE_SELECTED_OPENING")
    workspace.modules.put_group(module, opening)
    packet = pack_terminal_i(blobs["journal"], blobs["receipt"],
        aggregate_image=workspace.config["wire_profile"]["aggregate_image"], envelope=workspace._envelope,
        terminal_receipt_bytes=workspace.config["terminal_receipt_bytes"], terminal_i=True)
    workspace.packets.put(module, packet)
    need((len(C.canonical(opening)),sha(C.canonical(opening))) == OPENING
         and (len(packet),sha(packet)) == PACKET, "EXACT_RETAINED_FIXTURE")
    return module, name, opening, packet


def horizon(request, deadline=None):
    h = request["generation_horizons"]
    need(set(h) == {"admission_close_ms", "retention_not_after_ms", "write_until_ms",
                    "retention_until_ms", "retention_end_ms"}
         and all(type(v) is int for v in h.values()), "FIXED_GENERATION_HORIZONS")
    need(h["write_until_ms"] < h["admission_close_ms"] < h["retention_end_ms"]
         < h["retention_until_ms"] < h["retention_not_after_ms"], "ORDERED_GENERATION_HORIZONS")
    mono = time.monotonic(); now = int(time.time()*1000)
    # Same existing cleanup-reserve formula: drain35, operation10, native6.
    end = min(mono+120, STARTED+200-20, OUTER-(2*35+2*10+6+5)) if deadline is None else deadline
    need(end-mono >= 1 and now+math.ceil(1000*(end-mono)) <= h["retention_end_ms"],
         "ORIGINAL_RETENTION_HORIZON")
    return h


def state_snapshot(service):
    """Bounded read-only tiny-fixture diagnostics; no raw grant/token output."""
    def digest_rows(rows):
        rows = list(rows); need(len(rows) <= 16, "FIXTURE_ROW_BOUND")
        tagged = [[{"blob":v.hex()} if isinstance(v,bytes) else v for v in row] for row in rows]
        raw = encode(tagged); need(len(raw) <= 2*MIB, "FIXTURE_ROW_BYTES")
        return dict(rows=len(rows), bytes=len(raw), sha256=sha(raw))
    stores = {}
    for name,db in (("workspace",service.workspace.db), ("custody",service.workspace.modules.db),
                    ("packets",service.workspace.packets.db), ("index",service.workspace.index.db)):
        digest = hashlib.sha256(); size = lines = 0
        for line in db.iterdump():
            raw = line.encode()+b"\n"; size += len(raw); lines += 1
            need(size <= 8*MIB and lines <= 4096, "TINY_FIXTURE_DUMP_BOUND")
            digest.update(raw)
        stores[name] = dict(bytes=size, lines=lines, sha256=digest.hexdigest())
    db = service.ledger.db
    result = dict(stores=stores)
    for table in ("requests", "grants", "cells"):
        result[table] = digest_rows(db.execute("SELECT * FROM "+table+" ORDER BY id"))
    result["meta"] = digest_rows(db.execute("SELECT config,state,used FROM meta WHERE id=1"))
    return result


def route_snapshot(service):
    db = service.advertisement.db
    def rows(query):
        found = list(db.execute(query)); need(len(found) <= 2, "TWO_RUN_ROUTE_BOUND")
        return [sha(encode([{"blob":v.hex()} if isinstance(v,bytes) else v for v in row])) for row in found]
    return dict(meta=rows("SELECT * FROM meta ORDER BY id"),
                runs=rows("SELECT * FROM runs ORDER BY n"),
                routes=rows("SELECT * FROM routes ORDER BY cell,run"))


def core_state(service):
    state,runs = service.ledger.db.execute("SELECT state,runs FROM meta WHERE id=1").fetchone()
    return dict(state=state, runs=runs, run_id=service.grant.run_id, route_run=service.advertisement.run)


def node_ready(node):
    from location.protocol import peer_id
    task = node._start_task
    need(task is not None and task.done() and not task.cancelled(), "ACTUAL_NODE_READY_TASK")
    result = task.result(); peer_id(result["peer_id"])
    need(result["status"] == "RUNNING" and result["role"] == node.config["role"], "ACTUAL_NODE_READY")
    return result


async def close_service(service, report, key):
    value = await service.close(); report[key] = value
    clean = value["cleanup"]; node = value["observed"]["location"]
    need(value["status"] == "CLOSED" and not clean["errors"]
         and all(clean[k] is True for k in ("intake_closed", "retained_closed", "location_closed", "read_closed",
                                           "journal_closed", "controller_closed", "workspace_closed")), "SERVICE_ALL_ROLES_CLOSED")
    need(node["closed"] and node["returncode"] == 0 and not node["channel_failed"]
         and not node["forced_termination"], "SERVICE_ACTUAL_NODE_CLEAN")
    tasks = [getattr(service,n) for n in ("_start_task", "_close_task", "_monitor_task", "_retained_task")]
    tasks += [getattr(service.location,n) for n in ("_start_task", "_close_task", "_spawn_task", "stderr_task")]
    need(all(t is None or t.done() for t in tasks) and not service.controller._busy
         and not service.advertisement._busy and service.read_provider.server is None
         and not service.read_provider.tasks and service.intake_provider.server is None
         and not service.intake_provider.tasks, "NO_PENDING_CUSTODIAN_ACTOR")
    report[key+"_no_pending_actors"] = True


async def stop_reader(node, report):
    if node is None: return
    try:
        if not node.closed and not node.channel_failed and node.process is not None and node.process.returncode is None:
            result = await node.command("stop", {}, until=min(node.deadline,time.monotonic()+10))
            need(result.get("status") == "STOPPED", "READER_STOP")
    finally:
        await node.close(); report["reader_node_close"] = node.report()
    value = report["reader_node_close"]
    need(value["closed"] and value["returncode"] == 0 and not value["channel_failed"]
         and not value["forced_termination"], "READER_CLEAN_CLOSE")


async def discover(workspace, reader_node, closed_goal, policy, deadline, report):
    """Inputs contain no answer IDs/bytes, manifest or selected custodian peer."""
    from discovery import conclusion_fingerprint as FP
    from location.controller_services import ServiceLocatedWorkflow
    from location.observed_route import route
    from location.available_descriptor import descriptor
    from location.protocol import OwnerEgressPolicy
    from transport.receipt_client import AcquisitionBudget
    from transport.located_receipts import _ExpiringContact
    from evidence_network.transport import EvidenceAcquisition
    from modules import codec as C
    policy = OwnerEgressPolicy(policy)
    fingerprint = FP.conclusion_spec(C, "00"*32, closed_goal["universes"], closed_goal["type"],
                                    workspace.config["discovery_profile"])
    features = workspace.adapter.compile_query([fingerprint,*closed_goal["specs"]])
    route_features = workspace.adapter.compile_query([fingerprint])
    budget = AcquisitionBudget(deadline, dict(requests=12, reply_bytes=2*MIB,
        verify_attempts=1, verification_input_bytes=1, worker_cpu_seconds=1))
    budget.charge_external("location-and-search", 7, LOCATION["reply_bytes"])
    workflow = ServiceLocatedWorkflow(reader_node, workspace.adapter.namespace, features, LOCATION, SEARCH, policy)
    # Both location and acquisition stay under the same original owner cutoff.
    workflow.deadline = min(workflow.deadline,deadline)
    workflow._workflow._deadline = workflow.deadline
    acquired = None
    report.update(descriptors=[], mathematical_acceptance=False, global_complete=False)
    try:
        observed = await route(workflow, route_features, 0, event_cap=256, peer_cap=2)
        report["route"] = observed
        peers = observed["peers"]
        need(len(peers) <= 2 and len(set(peers)) == len(peers), "BOUNDED_RETURNED_PEERS")
        for peer in peers:
            value = await descriptor(workflow, peer, observed["route_key"], max_bytes=4096, max_age_ms=30000)
            report["descriptors"].append(dict(requested_peer=peer, result=value))
            if value["status"] == "DESCRIPTOR_UNAVAILABLE": continue
            need(value["status"] == "ADOPTED_ADVISORY_CONTACTS", "ADOPTED_DESCRIPTOR_CONTACT")
        contacts = workflow._workflow._contacts
        expiries = workflow._workflow._expiries
        if not any(time.monotonic() < expiries[name] for name in contacts):
            report.update(status="INCOMPLETE_DISCOVERY", reason="NO_UNEXPIRED_RETURNED_CONTACT",
                          mathematical_nonexistence=False)
            return None
        search = workflow.begin_search()
        need(len(search.endpoints) == 1, "ONE_RETURNED_READ_CONTACT")
        provider = next(iter(search.endpoints))
        offer = await search.offer(provider, 131072, max_expanded_bytes=262144, max_age_ms=60000)
        report["offer"] = offer
        need(offer["status"] == "OFFERED", "AUTHENTICATED_OFFER")
        partitions = [p for p in offer["partitions"] if p["anchor_count"]]
        need(len(partitions) == 1, "ONE_NONEMPTY_PARTITION")
        page = await search.page(provider, offer["snapshot_id"], partitions[0]["partition"], 0,
            dict(examined=4, matches=2, bytes=131072, timeout_ms=1000, node_reads=50000))
        report["page"] = page
        need(page["status"] == "VERIFIED_PAGE" and len(page["matches"]) == 1, "ONE_AUTHENTICATED_MATCH")
        endpoint = _ExpiringContact(search.endpoints[provider], search._expiries[provider], policy, budget)
        acquired = EvidenceAcquisition(workspace.adapter, {provider:endpoint}, workspace.packets.profile,
                                      budget, workspace.modules, workspace.packets)
        result = await acquired.export(provider, page["matches"][0]); loc = result["locator"]
        opening,declaration = workspace.modules.get_group(loc["module_id"],loc["relative_name"],loc["group_index"])
        need(declaration["kind"] == "theorem" and declaration["universes"] == closed_goal["universes"]
             and declaration["type"] == closed_goal["type"], "INDEPENDENT_FULL_TYPE_MATCH")
        offered = await acquired.offers(provider, loc["module_id"], max_offers=1, max_bytes=4096)
        need(len(offered["packets"]) == 1, "ONE_OFFERED_PACKET")
        entry = {key:offered["packets"][0][key] for key in ("packet_sha256", "packet_bytes")}
        await acquired.packet(provider, loc["module_id"], entry)
        packet = workspace.packets.get(entry["packet_sha256"],entry["packet_bytes"])
        report.update(status="ACQUIRED", locator=loc, evidence=entry,
            goal_sha256=sha(C.canonical(closed_goal["type"])), acquisition=acquired.report())
        return opening,declaration,packet
    finally:
        if acquired is not None: acquired.close()
        report["discovery"] = workflow.report()
        report["acquisition_used"] = dict(budget.used)
        need(all(budget.used[k] == 0 for k in ("verify_attempts", "verification_input_bytes", "worker_cpu_seconds")),
             "ZERO_MATHEMATICAL_CHECKS")


async def run(output, request, selected, report):
    from client.workspace_evidence import Workspace, CONCLUSION_FINGERPRINT_SCHEMA
    from client.serve_placement import PlacementService
    from placement.network import PlacementClient
    from placement import codec as P
    from discovery import formal_features as F
    from evidence_network.transport import CompositeProvider
    from location.protocol import peer_id
    from modules import codec as C
    import congruence_query
    config = deepcopy(request["workspace_config"])
    config.update(schema=CONCLUSION_FINGERPRINT_SCHEMA,
        discovery_profile=dict(schema="DMKN_MODULE_EXPORT_CONCLUSION_FINGERPRINT_PROFILE_V1", paths=[[]]))
    all_ports = ports()
    policy = dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
        test_endpoints=[dict(host="127.0.0.1",port=p) for p in sorted(all_ports.values())])
    contact = lambda key: dict(host="127.0.0.1",port=all_ports[key],tls=False,server_name=None)
    source = receiver = provider = reader_node = client = None
    services = []; nodes = []; secret = None; primary = None; acquired = None
    report.update(stage="source", ports=all_ports, cleanup_errors=[], source_closed=False, receiver_closed=False)
    try:
        h = horizon(request)
        need(int(time.time()*1000) < h["write_until_ms"], "ORIGINAL_WRITE_WINDOW")
        source = Workspace.open(output/"source-workspace",config,create=True)
        module,name,opening,packet = seed(source,request)
        report["fixture"] = dict(opening=dict(bytes=OPENING[0],sha256=OPENING[1]),
                                 packet=dict(bytes=PACKET[0],sha256=PACKET[1]))
        provider = CompositeProvider(index=source.index,custody=source.modules,packets=source.packets,**HTTP)
        await provider.start(host="127.0.0.1",port=all_ports["source_http"])
        reader_state = output/"reader-location"; reader_state.mkdir()
        reader_node = channel(selected,reader_state,STARTED+210,source.adapter.namespace,policy,
                              all_ports["reader_node"],role="reader",endpoints=[],bootstrap=[])
        report["stage"] = "reader-bootstrap"; report["reader_ready"] = await reader_node.start()
        bootstrap = f'/ip4/127.0.0.1/tcp/{all_ports["reader_node"]}/p2p/{peer_id(report["reader_ready"]["peer_id"])}'
        allowances = {key:(8 if key in ("placements","index_calls","recovery_passes","new_cells")
                          else 64 if key == "requests" else 128*MIB) for key in P.RESOURCES}
        generation = dict(schema=P.CONFIG_SCHEMA,service_epoch=sha(str(output).encode()+b"epoch"),
            generation=sha(str(output).encode()+b"generation"),namespace=source.adapter.namespace,
            wire_profile_id=source.packets.profile_id,admission_close_ms=h["admission_close_ms"],
            retention_not_after_ms=h["retention_not_after_ms"],max_grants=2,max_requests=2,max_cells=1,
            max_runs=2,ledger_pages=256,limits=allowances)
        limits = dict(lifetime_seconds=120,controller_cpu_seconds=90,controller_calls=128,
            health_interval_ms=30000,journal_pages=256,read=deepcopy(HTTP),
            intake=dict(max_connections=2,max_requests=8,incoming_bytes=MIB,outgoing_bytes=MIB,operation_ms=30000))
        def open_service(number):
            horizon(request)
            directory = output/("custodian-location-"+str(number)); directory.mkdir()
            node = channel(selected,directory,STARTED+200,generation["namespace"],policy,
                all_ports["custody_node"+str(number)],role="index-provider",endpoints=[contact("custody_http")],bootstrap=[bootstrap])
            nodes.append(node)
            value = PlacementService.open(output/"custodian-workspace",config,generation,policy,node,
                read_endpoint=contact("custody_http"),intake_endpoint=contact("placement_http"),limits=limits,
                outer_deadline=OUTER,create=number == 1,placement_create=number == 1,journal_create=number == 1)
            services.append(value); horizon(request,value.deadline)
            return value
        first = open_service(1)
        report["stage"] = "custodian-one-start"; report["custodian_one_ready"] = await first.start()
        report["custodian_one_node_ready"] = node_ready(first.location)
        need(first.workspace.index.status()["objects"] == 0 and core_state(first)["runs"] == 1, "FRESH_FIRST_RUN")
        grant = first.issue_token(contact("source_http"),write_until_ms=h["write_until_ms"],
                                  retention_until_ms=h["retention_until_ms"],limits=allowances)
        secret = grant["token"]
        expected = {key:generation[key] for key in ("service_epoch","generation","namespace","wire_profile_id")}
        client = PlacementClient(policy,contact("placement_http"),expected,secret,deadline=first.deadline,
                                 requests=1,incoming_bytes=90112,outgoing_bytes=25600,operation_ms=30000)
        export = source.adapter.encode_opening(module,name,opening)
        fingerprint = [s for s in source.adapter.describe(export)["specs"] if s["tag"] == "conclusion-fingerprint"]
        need(len(fingerprint) == 1,"SOURCE_SINGLE_FINGERPRINT")
        manifest = dict(schema=P.REQUEST_SCHEMA,generation=generation["generation"],namespace=generation["namespace"],
            wire_profile_id=generation["wire_profile_id"],module_id=module,relative_name=name,
            export_id=C.export_id(module,name),fingerprint=fingerprint[0],cell=P.cell(source.adapter,fingerprint[0])[0],
            export_object_sha256=sha(export),export_object_bytes=len(export),opening_max_bytes=65536,
            packet_sha256=sha(packet),packet_bytes=len(packet),bodies=[],retention_end_ms=h["retention_end_ms"])
        raw = F.compact(manifest); report["stage"] = "one-remote-submit"
        observed = await client.submit(raw); response = observed["response"]; rid = response["request_id"]
        need(observed["acknowledgement"] == "LOOPBACK_RESPONSE_OBSERVED"
             and response["placement"]["phase"] == "RECEIPT_COMMITTED"
             and response["placement"]["outcome"]["status"] == "INDEXED_UNADVERTISED"
             and response["route"]["status"] == "HINT_DISPATCHED_UNACKNOWLEDGED"
             and response["route"]["add_provider_write"] > 0,"ACTUAL_PLACEMENT_AND_DISPATCH")
        committed = first.ledger.request(rid)
        need(committed["manifest"] == raw and committed["outcome"] == response["placement"]["outcome"], "EXACT_COMMITTED_REQUEST_RECEIPT")
        report.update(first_response=observed,original_manifest=manifest,original_manifest_sha256=sha(raw),
                      original_request_id=rid,placement_client=client.report())
        client.close(); client = None
        await provider.stop(); report["source_http"] = provider.status()
        need(provider.server is None and not provider.tasks,"SOURCE_OFFLINE")
        source.close(); source = None; report["source_closed"] = True
        first.controller.seal(first.grant)
        sealed = state_snapshot(first); old_route = route_snapshot(first); one = core_state(first)
        need(one["state"] == "SEALED_SERVING" and one["runs"] == one["route_run"] == 1
             and all(sealed[k]["rows"] == 1 for k in ("requests","grants","cells"))
             and len(old_route["runs"]) == len(old_route["routes"]) == 1,"SEALED_ONE_PLACEMENT")
        report.update(sealed_before_close=sealed,route_before_close=old_route,core_before_close=one)
        report["stage"] = "close-custodian-one"
        await close_service(first,report,"custodian_one_close")
        # Never bind the first Node port again; do not clear R's routing state.
        second = open_service(2)
        two = core_state(second); report["core_reopened"] = two
        need(two["state"] == "SEALED_SERVING" and two["runs"] == two["route_run"] == 2
             and two["run_id"] != one["run_id"],"ORIGINAL_TWO_RUN_SEALED_GENERATION")
        reopened = state_snapshot(second); routes = route_snapshot(second)
        need(reopened == sealed and routes["meta"] == old_route["meta"] and routes["routes"] == old_route["routes"]
             and len(routes["runs"]) == 2 and routes["runs"][:1] == old_route["runs"],"PRESERVED_REOPENED_STATE")
        report.update(reopened=reopened,route_reopened=routes)
        report["stage"] = "custodian-two-start"; report["custodian_two_ready"] = await second.start()
        report["custodian_two_node_ready"] = node_ready(second.location)
        need(report["custodian_two_node_ready"]["peer_id"] != report["custodian_one_node_ready"]["peer_id"],"FRESH_NODE_IDENTITY")
        horizon(request,second.deadline); report["stage"] = "advertise-original-retained-request"
        restored = await second.advertise_retained(rid,until=second.deadline)
        report["restored_route"] = restored
        need(restored["request_id"] == rid and restored["run_id"] == two["run_id"]
             and restored["status"] == "HINT_DISPATCHED_UNACKNOWLEDGED" and restored["add_provider_write"] > 0,
             "CURRENT_RUN_OBSERVED_READVERTISEMENT")
        final_route = route_snapshot(second)
        need(state_snapshot(second) == sealed and second.ledger.request(rid) == committed
             and core_state(second) == two and final_route["meta"] == routes["meta"]
             and final_route["runs"] == routes["runs"] and len(final_route["routes"]) == 2
             and final_route["routes"][:1] == old_route["routes"],"ONLY_CURRENT_ROUTE_ROW_GREW")
        report["route_restored"] = final_route
        report["stage"] = "goal-only-discovery-after-restart"
        receiver = Workspace.open(output/"reader-workspace",config,create=True); report["reader"] = {}
        acquired = await discover(receiver,reader_node,congruence_query.query(C,2),policy,STARTED+200,report["reader"])
        stale = report["custodian_one_node_ready"]["peer_id"]
        report["stale_peer_returned"] = stale in report["reader"]["route"]["peers"]
        report["typed_stale_dial_miss"] = any(x["requested_peer"] == stale and
            x["result"]["status"] == "DESCRIPTOR_UNAVAILABLE" for x in report["reader"]["descriptors"])
        if acquired is not None:
            held,decl = second.workspace.modules.get_group(module,name,10)
            need(acquired[0] == opening == held and acquired[1] == decl
                 and acquired[2] == packet == second.workspace.packets.get(sha(packet),len(packet)),"EXACT_POST_RESTART_ACQUISITION")
            report["exact_acquisition_postcondition"] = True
        need(state_snapshot(second) == sealed and route_snapshot(second) == final_route
             and second.ledger.request(rid) == committed,"READ_ONLY_RETAINED_DATA_UNCHANGED")
        report["retained_state_after_reader"] = sealed
    except BaseException as error:
        primary = error; report["primary_error"] = error_fields(error)
    finally:
        if client is not None:
            try: report["placement_client"] = client.report(); client.close()
            except BaseException: report["cleanup_errors"].append("placement-client")
        for number,service in reversed(list(enumerate(services,1))):
            if number == 1 and report.get("custodian_one_close_no_pending_actors"): continue
            try: await close_service(service,report,"custodian_one_close" if number == 1 else "custodian_two_close")
            except BaseException: report["cleanup_errors"].append("custodian-"+str(number))
        for node in nodes:
            if node.closed: continue
            try: await node.close()
            except BaseException: report["cleanup_errors"].append("partial-custodian-node")
        try: await stop_reader(reader_node,report)
        except BaseException: report["cleanup_errors"].append("reader-node")
        if provider is not None:
            try:
                await provider.stop(); report["source_http"] = provider.status()
                need(provider.server is None and not provider.tasks,"SOURCE_ACTORS_CLOSED")
            except BaseException: report["cleanup_errors"].append("source-http")
        if source is not None:
            try: source.close(); report["source_closed"] = True
            except BaseException: report["cleanup_errors"].append("source-workspace")
        if receiver is not None:
            try: receiver.close(); report["receiver_closed"] = True
            except BaseException: report["cleanup_errors"].append("reader-workspace")
        pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]
        report["pending_async_tasks"] = len(pending)
        if pending: report["cleanup_errors"].append("pending-async-actors")
        if time.monotonic() >= OUTER: report["cleanup_errors"].append("original-owner-deadline")
        if secret is not None and secret.encode() in encode(report):
            report.clear(); report.update(status="FAIL",error_code="REPORT_TOKEN_DISCLOSURE",cleanup_errors=[])
            raise ValueError("REPORT_TOKEN_DISCLOSURE")
    if primary is None and not report["cleanup_errors"]:
        report.update(status="PASS" if acquired is not None else "INCOMPLETE_DISCOVERY",stage="done")
    else: report["status"] = "FAIL"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",required=True); parser.add_argument("--input",required=True)
    parser.add_argument("--input-sha",required=True); args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == PROJECT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,"ISOLATED_CANONICAL_OWNER")
    output = ordinary(args.output,directory=True)
    need(output.is_relative_to(PROJECT/"experiments") and not output.is_relative_to(INSTALLATION),"SELECTED_EXTERNAL_OUTPUT")
    path = ordinary(args.input); need(path.stat().st_size <= MIB,"INPUT_BYTES")
    input_row = dict(path=str(path),bytes=path.stat().st_size,sha256=args.input_sha)
    request = json.loads(read(input_row,MIB))
    need(set(request) == {"schema","installation","release","build_input","receipt","journal","bundle",
                          "workspace_config","generation_horizons"}
         and request["schema"] == "DMKN_CONSOLIDATED_RESTART_SMOKE_INPUT_V1","CLOSED_OWNER_INPUT")
    report = dict(schema="DMKN_CONSOLIDATED_RESTART_SMOKE_RESULT_V1",status="FAIL",
        scope="INSTALLED_RETAINED_PLACEMENT_RESTART_AND_GOAL_ONLY_EXACT_ACQUISITION",
        mathematical_acceptance=False,verifier_calls=0,native_calls=0,proof_calls=0,trust_adoptions=0,
        independent_hosts=False,public_tls_tested=False,global_complete=False,full_v5_release=False,
        started=STARTED,original_outer_deadline=OUTER,input_sha256=args.input_sha,
        release_sha256=request["release"]["sha256"],build_input_sha256=request["build_input"]["sha256"])
    try:
        release,selected,runtime,helpers = adopt(request)
        save(output/"installed-smoke-sources.json",dict(sdk=selected,goal_helpers=helpers,
             python_runtime={name:pair(row) for name,row in runtime.items()}))
        asyncio.run(run(output,request,selected,report))
        report["imported_origins"] = rebind(request,release,selected,runtime,helpers)
        read(input_row,MIB); need(time.monotonic() < OUTER,"ORIGINAL_OWNER_DEADLINE")
    except BaseException as error:
        report["status"] = "FAIL"; report["terminal_error"] = error_fields(error)
    report["elapsed_seconds"] = time.monotonic()-STARTED
    save(output/"consolidated-restart-smoke-result.json",report)
    return 0 if report["status"] == "PASS" and not report.get("cleanup_errors") else 1


if __name__ == "__main__": raise SystemExit(main())

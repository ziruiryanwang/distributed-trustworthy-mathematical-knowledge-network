"""Fresh remote placement, original-source withdrawal, goal-only rediscovery.

Trusted bounded local integration. Retained receipt is untrusted input until
the real receiver accepts it. No prover, frontend, fake issuer or test import.
"""
import argparse
import asyncio
from copy import deepcopy
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import socket
import sys
import time

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = Path(__file__).resolve().parents[1]
MIB = 1024**2
MAP_SHA = "d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0"
MAP_BYTES = 2805479
QUALIFIED = {
    "v5/admission/pin_phase.py": ("standalone_validation/admission/pin_phase.py", "ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881"),
    "v5/mixed_claims/imports_atomic.py": ("standalone_validation/mixed_claims/imports_atomic.py", "8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595"),
    "v5/mixed_claims/receiver.py": ("incremental_native/mixed_claims/receiver.py", "5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b"),
    "v5/discovery/discovery_store.py": ("selective_placement/discovery/discovery_store.py", "1c8543d4903754174b80d107ee923116ddb402d41a3b5af3f1d255abdfc6a328"),
    "v5/placement/__init__.py": ("selective_placement/placement/__init__.py", "8fe08470d7fd15e96d1305f0e49a8b359cb53ce0c542bf7473b68d869159112e"),
    "v5/placement/codec.py": ("selective_placement/placement/codec.py", "6f32569d4807f96130350b85233161603f6860f082c75f81a8bfacf4f0a58999"),
    "v5/placement/ledger.py": ("selective_placement/placement/ledger.py", "d955990c347ed466617c752893dded8b8494dd266a050b045352c77c48f21a91"),
    "v5/placement/controller.py": ("selective_placement/placement/controller.py", "ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49"),
}
NETWORK = ("placement/network.py", "placement/advertisement.py", "client/serve_placement.py")
HELPERS = {
    "formal_terms.py": ("examples/mirror_method/method_query.py", "0ddbc8dac7e60180f3f9aad3216873158d8b2722a9d31c48112e20262298c642"),
    "congruence_query.py": ("examples/terminal_i/congruence_query.py", "07a323edd3b10f94f6fc7f9790191b1145666b547b4575c70c4a7261b3d8fadd"),
}
FIXTURES = {
    "receipt": (223594, "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"),
    "journal": (184, "22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682"),
    "bundle": (53769, "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926"),
}
HTTP = dict(max_connections=2, max_requests=16, max_reply_bytes=8*MIB, operation_ms=5000)
SEARCH = dict(providers=1, snapshots=1, requests=4, pages=2, examined=8,
              candidates=4, bytes=262144, inflight=1, wall_ms=60000)
LOCATION = dict(route_operations=1, routing_events=256, routing_peer_slots=2,
                descriptor_requests=1, contacts=1, reply_bytes=270336, wall_ms=60000)


def need(ok, code):
    if not ok: raise ValueError(code)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def error_fields(error):
    text = str(error)
    code = text if re.fullmatch(r"[A-Z][A-Z0-9_]{0,127}", text) else "LOCAL_OPERATION_FAILED"
    return dict(error_type=type(error).__name__, error_code=code)


def pair(row): return {key: row[key] for key in ("bytes", "sha256")}


def read(row, maximum):
    path = Path(row["path"])
    need(path.is_absolute() and path.resolve() == path and path.is_file(), "ORDINARY_INPUT")
    need(all(not p.is_symlink() and not p.is_junction() for p in (path, *path.parents)), "NO_INPUT_LINKS")
    need(0 < row["bytes"] <= maximum and path.stat().st_size == row["bytes"], "INPUT_SIZE")
    raw = path.read_bytes()
    need(len(raw) == row["bytes"] and sha(raw) == row["sha256"], "INPUT_PIN")
    return raw


def write(path, raw):
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "SHORT_WRITE")
        stream.flush(); os.fsync(stream.fileno())


def save(path, value):
    write(path, json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()+b"\n")


def stage(output, request):
    need(pair(request["map"]) == dict(bytes=MAP_BYTES, sha256=MAP_SHA), "CURRENT_MAP")
    basis = json.loads(read(request["map"], MAP_BYTES))["sdk_sources"]
    need(len(basis) == 114 and set(request["network_sources"]) == set(NETWORK), "EXACT_SOURCE_SET")
    rows = {}
    for logical, row in basis.items():
        relative = Path(row["path"]).relative_to(PROJECT/"software/v5")
        rows[logical] = dict(path=str(SOURCE/relative), **pair(row))
    for logical, (relative, digest) in QUALIFIED.items():
        path = SOURCE/relative
        rows[logical] = dict(path=str(path), bytes=path.stat().st_size, sha256=digest)
    for relative, row in request["network_sources"].items():
        need(Path(row["path"]) == PROJECT/"software/v5/placement_network"/relative, "NETWORK_SOURCE_SCOPE")
        rows["v5/"+relative] = dict(path=str(SOURCE/"placement_network"/relative), **pair(row))
    need(len(rows) == 121, "PRODUCT_SOURCE_COUNT")
    code = output/"selected-code"; code.mkdir()
    selected = {}
    for logical, row in sorted(rows.items()):
        need(logical.startswith(("v5/", "portable/")) and ".." not in logical and "\\" not in logical,
             "LOGICAL_SOURCE_PATH")
        raw = read(row, 2*MIB); target = code/logical
        target.parent.mkdir(parents=True, exist_ok=True); write(target, raw)
        need(target.read_bytes() == raw, "STAGED_READBACK")
        selected[logical] = dict(path=str(target), source=row["path"], **pair(row))
    owner = code/"owner"; owner.mkdir()
    for name, (relative, digest) in HELPERS.items():
        path = SOURCE/relative
        raw = read(dict(path=str(path), bytes=path.stat().st_size, sha256=digest), MIB)
        write(owner/name, raw)
        selected["owner/"+name] = dict(path=str(owner/name), source=str(path), bytes=len(raw), sha256=digest)
    need(not any(name in sys.modules for name in ("placement", "modules", "client", "location")), "EARLY_IMPORT")
    sys.path[:0] = [str(code/"v5"), str(code/"portable"), str(owner)]
    return code, selected


def ports():
    held = []
    try:
        for unused in range(5):
            stream = socket.socket(); held.append(stream)
            stream.bind(("127.0.0.1", 0))
        numbers = [s.getsockname()[1] for s in held]
        need(len(set(numbers)) == 5, "DISTINCT_PORTS")
        return dict(zip(("source_http", "custody_http", "placement_http", "reader_node", "custody_node"), numbers))
    finally:
        for stream in held: stream.close()


def location_limits():
    return dict(service_ms=210000, operation_ms=10000, query_events=256,
        provider_limit=2, advertised_keys=1, provider_ttl_ms=120000,
        reprovide_interval_ms=30000, maintenance_ms=60000, commands=16,
        descriptor_requests=4, descriptor_reply_bytes=16384, metadata={},
        transport=dict(outbound_attempts=32, inbound_upgrades=32, receive_bytes=2*MIB, send_bytes=2*MIB))


def channel(code, selected, installation, directory, deadline, namespace, policy, port,
            *, role, endpoints, bootstrap):
    from location.controller import AdoptedLocationRuntime, SOURCE_NAMES
    from location.controller_services import ServiceLocationProcess, ROLE_NAMES
    pins = lambda names: {name: selected["portable/location/"+name]["sha256"] for name in names}
    adoption = AdoptedLocationRuntime(code/"portable/location", pins(SOURCE_NAMES),
        installation_root=installation/"base", workspace_root=directory)
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
    for name, identity in FIXTURES.items():
        need((request[name]["bytes"], request[name]["sha256"]) == identity, "FIXTURE_IDENTITY")
        blobs[name] = read(request[name], MIB)
    bundle = C.parse_json(blobs["bundle"])
    module = C.module_id(bundle["spec"]); exact = blobs["journal"]
    member = B.member_journal(exact)
    need(member["module"] == module and member["summary"] == C.summarize(bundle["spec"]), "FIXTURE_JOURNAL")
    opening = C.group_opening(bundle["spec"], 10)
    name = [["s", "CommonsV5"], ["s", "binary_congr"]]
    need(opening == bundle["openings"][10] and opening["group"]["declarations"][0]["name"] == name,
         "FIXTURE_SELECTED_OPENING")
    workspace.modules.put_group(module, opening)
    packet = pack_terminal_i(exact, blobs["receipt"], aggregate_image=workspace.config["wire_profile"]["aggregate_image"],
        envelope=workspace._envelope, terminal_receipt_bytes=workspace.config["terminal_receipt_bytes"], terminal_i=True)
    workspace.packets.put(module, packet)
    # Source needs custody only; B's new placement, not seeding, creates the index.
    return module, name, opening, packet


async def discover(workspace, reader_node, closed_goal, policy, deadline, report):
    """No publisher/custodian module ID, name, manifest or packet pin argument."""
    from discovery import conclusion_fingerprint as FP, formal_features as F
    from location.controller_services import ServiceLocatedWorkflow
    from location.protocol import OwnerEgressPolicy
    from transport.receipt_client import AcquisitionBudget
    from transport.located_receipts import _ExpiringContact
    from evidence_network.transport import EvidenceAcquisition
    from modules import codec as C
    policy = OwnerEgressPolicy(policy)
    fingerprint = FP.conclusion_spec(C, "00"*32, closed_goal["universes"], closed_goal["type"],
                                    workspace.config["discovery_profile"])
    specs = [fingerprint, *closed_goal["specs"]]
    features = workspace.adapter.compile_query(specs)
    route_features = workspace.adapter.compile_query([fingerprint])
    budget = AcquisitionBudget(deadline, dict(requests=12, reply_bytes=2*MIB,
        verify_attempts=1, verification_input_bytes=1, worker_cpu_seconds=1))
    budget.charge_external("location-and-search", 6, LOCATION["reply_bytes"])
    workflow = ServiceLocatedWorkflow(reader_node, workspace.adapter.namespace, features, LOCATION, SEARCH, policy)
    route = await workflow.route(route_features, 0, event_cap=256, peer_cap=2)
    need(len(route["peers"]) == 1, "ONE_ACTUALLY_LOCATED_CUSTODIAN")
    descriptor = await workflow.descriptor(route["peers"][0], route["route_key"], max_bytes=4096, max_age_ms=30000)
    need(len(descriptor["contacts"]) == 1, "ONE_DESCRIPTOR_CONTACT")
    search = workflow.begin_search(); provider = descriptor["contacts"][0]
    offer = await search.offer(provider, 131072, max_expanded_bytes=262144, max_age_ms=60000)
    need(offer["status"] == "OFFERED", "AUTHENTICATED_OFFER")
    partitions = [p for p in offer["partitions"] if p["anchor_count"]]
    need(len(partitions) == 1, "ONE_NONEMPTY_PARTITION")
    page = await search.page(provider, offer["snapshot_id"], partitions[0]["partition"], 0,
        dict(examined=4, matches=2, bytes=131072, timeout_ms=1000, node_reads=50000))
    need(page["status"] == "VERIFIED_PAGE" and len(page["matches"]) == 1, "ONE_AUTHENTICATED_MATCH")
    endpoint = _ExpiringContact(search.endpoints[provider], search._expiries[provider], policy, budget)
    acquired = EvidenceAcquisition(workspace.adapter, {provider:endpoint}, workspace.packets.profile,
                                  budget, workspace.modules, workspace.packets)
    try:
        result = await acquired.export(provider, page["matches"][0])
        loc = result["locator"]
        opening, declaration = workspace.modules.get_group(loc["module_id"], loc["relative_name"], loc["group_index"])
        need(declaration["kind"] == "theorem" and declaration["universes"] == closed_goal["universes"]
             and declaration["type"] == closed_goal["type"], "INDEPENDENT_FULL_TYPE_MATCH")
        offered = await acquired.offers(provider, loc["module_id"], max_offers=1, max_bytes=4096)
        need(len(offered["packets"]) == 1, "ONE_OFFERED_PACKET")
        entry = {key:offered["packets"][0][key] for key in ("packet_sha256", "packet_bytes")}
        await acquired.packet(provider, loc["module_id"], entry)
        packet = workspace.packets.get(entry["packet_sha256"], entry["packet_bytes"])
        structural_report = acquired.report()
        need(all(budget.used[key] == 0 for key in
                 ("verify_attempts", "verification_input_bytes", "worker_cpu_seconds")),
             "STRUCTURAL_ACQUISITION_NO_MATHEMATICAL_CHECK")
        report.update(route=route, descriptor=descriptor, offer=offer, page=page, locator=loc,
            discovery=workflow.report(), acquisition=structural_report,
            goal_sha256=sha(C.canonical(closed_goal["type"])), evidence=entry,
            mathematical_acceptance=False)
        return opening, declaration, packet
    finally:
        acquired.close()


def admit_received(output, request, selected, opening, declaration, packet, report):
    """Only R's acquired bytes and a newly live owner can establish admission."""
    from admission.trust import TrustDomain, SUPPORT_SCHEMA, support_id
    from admission.verifier import ReceiptVerifier
    from aggregate_claims import bindings as B
    from evidence_network.packet import parse_terminal_i
    from mixed_claims.packet import Envelope
    from modules import codec as C
    envelope = Envelope(**request["workspace_config"]["packet_envelope"])
    receipt, exact, unused = parse_terminal_i(packet, envelope,
        aggregate_image=request["workspace_config"]["wire_profile"]["aggregate_image"],
        terminal_receipt_bytes=request["workspace_config"]["terminal_receipt_bytes"], terminal_i=True)
    installation = Path(request["installation"])
    supervisor = request["supervisor_manifest"]
    need(Path(supervisor["path"]) == installation/"base/RELEASE-MANIFEST.json", "SUPERVISOR_ROLE")
    manifest = json.loads(read(supervisor, 8*MIB))
    executable = request["receipt_executable"]
    need(Path(executable["path"]) == installation/"assets/receipt/module_host.exe", "RECEIPT_EXECUTABLE_ROLE")
    read(executable, 64*MIB)
    runtime_pins = {}
    need(len(request["python_runtime"]) == 18, "PYTHON_RUNTIME_COUNT")
    for row in request["python_runtime"]:
        read(row, 32*MIB); runtime_pins[row["path"]] = pair(row)
    need(str(Path(sys.executable).resolve()) in runtime_pins, "ACTUAL_PYTHON_RUNTIME")
    source_pins = {row["path"]:pair(row) for name,row in selected.items() if name.endswith(".py")}
    roles = {"source/"+name:pair(row) for name,row in selected.items()}
    roles.update({"runtime/"+str(i):pair(row) for i,row in enumerate(request["python_runtime"])})
    roles.update({"supervisor-manifest":pair(supervisor), "receipt-executable":pair(executable),
                  "current-map":pair(request["map"])})
    for relative in ("operator/commons.py", "receiver/helpers/domains.py", "receiver/helpers/run_stage.py"):
        row = dict(path=str(installation/"base"/relative), **manifest["files"][relative])
        read(row, 4*MIB); roles["supervisor/"+relative] = pair(row)
    own = Path(__file__).read_bytes()
    roles["owner/integration"] = dict(bytes=len(own), sha256=sha(own))
    support = dict(schema=SUPPORT_SCHEMA, identities=dict(relation_image=B.RELATION_IMAGE,
        aggregate_image=None, foundation=B.FOUNDATION, policy=B.POLICY,
        receipt_scheme="resolved-succinct-poseidon2"), roles=roles)
    save(output/"receiver-support.json", support)
    domain = verifier = None
    try:
        domain = TrustDomain.create(output/"reader-trust", sha(str(output).encode()), support)
        need(domain.identity()["support_id"] == support_id(support), "EXACT_TEMPORARY_ADOPTION")
        verifier = ReceiptVerifier(supervisor_manifest=supervisor["path"],
            supervisor_manifest_sha256=supervisor["sha256"], executable=executable["path"],
            runtime_pins={**source_pins, **runtime_pins, executable["path"]:pair(executable)},
            image_id=B.RELATION_IMAGE, foundation=B.FOUNDATION, policy=B.POLICY,
            operations=1, submitted_bytes=len(receipt), reserved_cpu_seconds=10,
            wall_seconds=45, trust_binding=domain.bind())
        handle = verifier.receive(receipt, opening["summary"], output/"received-i",
                                  cpu_seconds=10, wall_seconds=30, memory_mib=512)
        fact = verifier.describe(handle)
        need(fact["journal"] == exact and fact["module"] == C.summary_id(opening["summary"]), "ACQUIRED_SAME_CALL_JOURNAL")
        group = verifier.open_group(handle, opening)
        need(declaration in group["declarations"], "ACQUIRED_OPENING_MATHEMATICAL_MEMBERSHIP")
        report.update(mathematical_acceptance=True, module=fact["module"], journal_hex=exact.hex(),
            declaration_type_sha256=sha(C.canonical(declaration["type"])),
            receipt_sha256=sha(receipt), before_close=verifier.report())
    finally:
        if verifier is not None:
            verifier.close(); report["after_close"] = verifier.report()
        if domain is not None:
            domain.withdraw("End of explicitly temporary remote-placement integration")
            report["domain_withdrawn"] = True


async def stop_reader(node, report):
    if node is None: return
    try:
        if not node.closed and not node.channel_failed and node.process is not None and node.process.returncode is None:
            result = await node.command("stop", {}, until=min(node.deadline, time.monotonic()+10))
            need(result.get("status") == "STOPPED", "READER_STOP")
    finally:
        await node.close(); report["reader_node"] = node.report()
    need(report["reader_node"]["closed"] and report["reader_node"]["returncode"] == 0
         and not report["reader_node"]["channel_failed"] and not report["reader_node"]["forced_termination"],
         "READER_CLEAN_CLOSE")


def placement_observation(service):
    """Local test diagnostics only; no token value and no synthesized success."""
    ledger = service.ledger.db
    return dict(requests=ledger.execute("SELECT count(*) FROM requests").fetchone()[0],
        grants=ledger.execute("SELECT count(*) FROM grants").fetchone()[0],
        funding=json.loads(ledger.execute("SELECT used FROM meta WHERE id=1").fetchone()[0]),
        routes=service.advertisement.db.execute("SELECT cell,run,request_id,phase FROM routes ORDER BY cell,run").fetchall(),
        custody=service.workspace.modules.status(), packets=service.workspace.packets.status(),
        index=service.workspace.index.status())


async def run(output, request, code, selected, report):
    from client.workspace_evidence import Workspace, CONCLUSION_FINGERPRINT_SCHEMA
    from client.serve_placement import PlacementService
    from placement.network import PlacementClient
    from placement import codec as P
    from discovery import formal_features as F
    from evidence_network.transport import CompositeProvider
    from location.protocol import peer_id
    from modules import codec as C
    import congruence_query
    started = time.monotonic(); outer = started+280
    config = deepcopy(request["workspace_config"])
    config.update(schema=CONCLUSION_FINGERPRINT_SCHEMA,
        discovery_profile=dict(schema="DMKN_MODULE_EXPORT_CONCLUSION_FINGERPRINT_PROFILE_V1", paths=[[]]))
    all_ports = ports()
    policy = dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
        test_endpoints=[dict(host="127.0.0.1", port=p) for p in sorted(all_ports.values())])
    contact = lambda key: dict(host="127.0.0.1", port=all_ports[key], tls=False, server_name=None)
    source = receiver = provider = reader_node = custody_node = service = client = None
    secret = None; acquired = None; primary = None
    report.update(stage="source", ports=all_ports, cleanup_errors=[],
        source_closed=False, receiver_closed=False, network_closed_before_admission=False)
    try:
        source = Workspace.open(output/"source-workspace", config, create=True)
        module, name, opening, packet = seed(source, request)
        provider = CompositeProvider(index=source.index, custody=source.modules, packets=source.packets, **HTTP)
        await provider.start(host="127.0.0.1", port=all_ports["source_http"])
        # R's transport can hold an ordinary DHT announcement before R chooses
        # its local query. No query, manifest or answer is given to this channel.
        reader_state = output/"reader-location"; reader_state.mkdir()
        reader_node = channel(code, selected, Path(request["installation"]), reader_state,
            started+210, source.adapter.namespace, policy, all_ports["reader_node"],
            role="reader", endpoints=[], bootstrap=[])
        report["stage"] = "reader-bootstrap"
        report["reader_ready"] = await reader_node.start()
        bootstrap = f'/ip4/127.0.0.1/tcp/{all_ports["reader_node"]}/p2p/{peer_id(report["reader_ready"]["peer_id"])}'
        custody_state = output/"custodian-location"; custody_state.mkdir()
        custody_node = channel(code, selected, Path(request["installation"]), custody_state,
            started+200, source.adapter.namespace, policy, all_ports["custody_node"],
            role="index-provider", endpoints=[contact("custody_http")], bootstrap=[bootstrap])
        now = int(time.time()*1000)
        allowances = {key:(8 if key in ("placements", "index_calls", "recovery_passes", "new_cells")
                          else 64 if key == "requests" else 128*MIB) for key in P.RESOURCES}
        generation = dict(schema=P.CONFIG_SCHEMA, service_epoch=sha(str(output).encode()+b"epoch"),
            generation=sha(str(output).encode()+b"generation"), namespace=source.adapter.namespace,
            wire_profile_id=source.packets.profile_id, admission_close_ms=now+180000,
            retention_not_after_ms=now+240000, max_grants=2, max_requests=2, max_cells=1,
            max_runs=1, ledger_pages=256, limits=allowances)
        service_limits = dict(lifetime_seconds=120, controller_cpu_seconds=90, controller_calls=128,
            health_interval_ms=30000, journal_pages=256, read=deepcopy(HTTP),
            intake=dict(max_connections=2, max_requests=8, incoming_bytes=MIB, outgoing_bytes=MIB, operation_ms=30000))
        service = PlacementService.open(output/"custodian-workspace", config, generation, policy, custody_node,
            read_endpoint=contact("custody_http"), intake_endpoint=contact("placement_http"),
            limits=service_limits, outer_deadline=outer, create=True, placement_create=True, journal_create=True)
        report["stage"] = "custodian-start"
        report["custodian_ready"] = await service.start()
        need(service.workspace.index.status()["objects"] == 0, "EMPTY_CUSTODIAN")
        grant = service.issue_token(contact("source_http"), write_until_ms=now+150000,
            retention_until_ms=now+220000, limits=allowances)
        secret = grant["token"]
        expected = {key:generation[key] for key in ("service_epoch", "generation", "namespace", "wire_profile_id")}
        client = PlacementClient(policy, contact("placement_http"), expected, secret,
            deadline=service.deadline, requests=3, incoming_bytes=3*90112,
            outgoing_bytes=3*25600, operation_ms=30000)
        export = source.adapter.encode_opening(module, name, opening)
        fingerprint = [s for s in source.adapter.describe(export)["specs"] if s["tag"] == "conclusion-fingerprint"]
        need(len(fingerprint) == 1, "SOURCE_SINGLE_FINGERPRINT")
        manifest = dict(schema=P.REQUEST_SCHEMA, generation=generation["generation"], namespace=generation["namespace"],
            wire_profile_id=generation["wire_profile_id"], module_id=module, relative_name=name,
            export_id=C.export_id(module,name), fingerprint=fingerprint[0], cell=P.cell(source.adapter,fingerprint[0])[0],
            export_object_sha256=sha(export), export_object_bytes=len(export), opening_max_bytes=65536,
            packet_sha256=sha(packet), packet_bytes=len(packet), bodies=[], retention_end_ms=now+210000)
        raw = F.compact(manifest)
        report["stage"] = "remote-submit"
        first = await client.submit(raw)
        response = first["response"]
        need(first["acknowledgement"] == "LOOPBACK_RESPONSE_OBSERVED"
             and response["placement"]["phase"] == "RECEIPT_COMMITTED"
             and response["placement"]["outcome"]["status"] == "INDEXED_UNADVERTISED"
             and response["route"]["status"] == "HINT_DISPATCHED_UNACKNOWLEDGED"
             and response["route"]["add_provider_write"] > 0, "ACTUAL_PLACEMENT_AND_DISPATCH")
        stable_source = lambda: {key:value for key,value in provider.status().items()
                                if key in ("requests", "request_bytes", "reply_bytes", "header_bytes", "failures", "refused")}
        before = placement_observation(service); source_before = stable_source()
        again = await client.submit(raw)
        status = await client.status(response["request_id"])
        need(again["response"] == response == status["response"], "DUPLICATE_STATUS_SAME_OBSERVATION")
        need(placement_observation(service) == before and stable_source() == source_before,
             "DUPLICATE_NO_RESERVATION_CUSTODY_INDEX_ROUTE_OR_FETCH")
        report.update(first_response=first, duplicate_response=again, status_response=status,
            placement=before, source_after_placement=source_before, placement_client=client.report())
        client.close(); client = None
        # A completely leaves before the independent reader function is called.
        await provider.stop(); report["source_http"] = provider.status()
        need(provider.server is None and not provider.tasks, "SOURCE_OFFLINE")
        source.close(); source = None; report["source_closed"] = True
        report["stage"] = "unknown-id-discovery-after-source-withdrawal"
        receiver = Workspace.open(output/"reader-workspace", config, create=True)
        report["reader"] = {}
        closed_goal = congruence_query.query(C, 2)
        acquired = await discover(receiver, reader_node, closed_goal, policy, started+200, report["reader"])
        need(sha(acquired[2]) == sha(packet), "ACQUIRED_ORIGINAL_PACKET_POSTCONDITION")
        report["stage"] = "close-network"
    except BaseException as error:
        primary = error
        # Trusted diagnostic type only; never serialize an exception that may
        # contain a request or token into any saved report.
        report.update(error_fields(error))
    finally:
        if client is not None:
            try: client.close()
            except BaseException: report["cleanup_errors"].append("placement-client")
        if service is not None:
            try:
                report["custodian_close"] = await service.close()
                need(report["custodian_close"]["status"] == "CLOSED", "CUSTODIAN_CLEAN_CLOSE")
            except BaseException: report["cleanup_errors"].append("custodian-service")
        elif custody_node is not None:
            try: await custody_node.close()
            except BaseException: report["cleanup_errors"].append("unstarted-custodian-node")
        try: await stop_reader(reader_node, report)
        except BaseException: report["cleanup_errors"].append("reader-node")
        if provider is not None:
            try: await provider.stop()
            except BaseException: report["cleanup_errors"].append("source-http")
        if source is not None:
            try: source.close(); report["source_closed"] = True
            except BaseException: report["cleanup_errors"].append("source-workspace")
    try:
        need(primary is None and not report["cleanup_errors"] and acquired is not None, "NETWORK_WORKFLOW_OR_CLEANUP_FAILED")
        report["network_closed_before_admission"] = True
        report["stage"] = "genuine-received-i-admission"
        report["mathematics"] = {}
        admit_received(output, request, selected, *acquired, report["mathematics"])
        need(time.monotonic() < outer, "ORIGINAL_OUTER_DEADLINE")
        report.update(status="PASS", stage="done")
    finally:
        if receiver is not None:
            try: receiver.close(); report["receiver_closed"] = True
            except BaseException:
                report["cleanup_errors"].append("reader-workspace"); report["status"] = "FAIL"
        # This check happens before writing any report. It supplements the
        # product's fixed projection; it is not a general secret scanner.
        if secret is not None:
            encoded = json.dumps(report, sort_keys=True, allow_nan=False).encode()
            if secret.encode() in encoded:
                report.clear()
                report.update(schema="DMKN_PLACEMENT_NETWORK_INTEGRATION_RESULT_V1", status="FAIL",
                              error_code="REPORT_TOKEN_DISCLOSURE", cleanup_errors=[])
                raise ValueError("REPORT_TOKEN_DISCLOSURE")


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--output", required=True); args.add_argument("--input", required=True)
    parsed = args.parse_args(); output = Path(parsed.output)
    need(os.name == "nt" and Path.cwd() == PROJECT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_CANONICAL_OWNER")
    need(output.is_absolute() and output.is_dir() and output.is_relative_to(PROJECT/"experiments"), "FRESH_SELECTED_OUTPUT")
    raw = Path(parsed.input).read_bytes(); need(0 < len(raw) <= MIB, "INPUT_BYTES")
    request = json.loads(raw)
    need(set(request) == {"schema", "map", "network_sources", "installation", "supervisor_manifest",
        "receipt_executable", "python_runtime", "receipt", "journal", "bundle", "workspace_config"}
        and request["schema"] == "DMKN_PLACEMENT_NETWORK_INTEGRATION_INPUT_V1", "CLOSED_OWNER_INPUT")
    code, selected = stage(output, request); save(output/"integration-sources.json", selected)
    report = dict(schema="DMKN_PLACEMENT_NETWORK_INTEGRATION_RESULT_V1", status="FAIL",
        scope="REAL_LOOPBACK_REMOTE_PLACEMENT_SOURCE_WITHDRAWAL_GOAL_ONLY_DISCOVERY_AND_I_ADMISSION",
        public_tls_tested=False, independent_hosts=False, new_proof_calls=0,
        new_native_calls=0, full_cost_growth_proved=False, full_v5_release=False)
    try:
        asyncio.run(run(output, request, code, selected, report))
    except BaseException as error:
        report["status"] = "FAIL"; report.update(error_fields(error))
    save(output/"placement-network-integration-result.json", report)
    return 0 if report["status"] == "PASS" and not report.get("cleanup_errors") else 1


if __name__ == "__main__": raise SystemExit(main())

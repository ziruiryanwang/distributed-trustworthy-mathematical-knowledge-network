"""One installed real-wire, same-reader exact-body custody integration.

Trusted owner adapter only. Retained packet, three loopback Nodes, no proof
production/authoring. Runtime and launch selection belong to the root owner.
"""
import asyncio
from copy import deepcopy
from dataclasses import replace
from importlib import import_module
from pathlib import Path
import socket
import time
from types import MappingProxyType, SimpleNamespace

from admission import trust as T
from client import located_queries as L, remote_reader, serve_advertised as A
from client import serve_workspace as H
from client.runtime import RuntimeProfile, read_pin
from client.semantic_reader import SemanticReader, READY
from client.workspace_mixed import CommonsClient as MixedClient
from client.workspace_validated import Workspace
from custody.module_store import BODY_SCHEMA, permitted_hashes
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from evidence_network.transport import CompositeProvider
from location import protocol as P
from location.controller import AdoptedLocationRuntime, SOURCE_NAMES
from location.controller_services import ServiceLocationProcess, ROLE_NAMES
from modules import codec as C

MIB = 1024**2
SCHEMA = "DMKN_V5_EXACT_CUSTODY_INSTALLED_V1"
RESULT_SCHEMA = "DMKN_V5_EXACT_CUSTODY_INSTALLED_RESULT_V1"
PACKET_SHA = "6998ba92d064c8ce790192a434655d4b99bf0e7018f422ec24be757de55db2eb"
FOUNDATION_SHA = "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"
EXPORT = [["s", "ClientV5"], ["s", "project_summary"]]
SPLIT = dict(module_id="2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e",
    relative_name=[["s", "CommonsV5"], ["s", "fold"]], universes=2,
    body_hash="0b5f265dfb01a1ed1232443bfdc79c5217be78664b15ee9d12e01fa77d2e6e55")
SOURCES = {relative: relative[:-3].replace("/", ".") for relative in (
    "client/body_custody.py", "client/workspace_evidence.py", "client/semantic_reader.py",
    "transport/acquisition_resilience.py", "client/located_queries.py", "client/serve_advertised.py")}
SEARCH = dict(providers=1, snapshots=1, requests=4, pages=1, examined=8,
    candidates=4, bytes=262144, inflight=1, wall_ms=180000)
LOCATION = dict(route_operations=1, routing_events=256, routing_peer_slots=2,
    descriptor_requests=1, contacts=1, reply_bytes=270336, wall_ms=180000)
BODY = dict(schema="DMKN_V5_BODY_LOCATION_ALLOWANCE_V1", route_operations=1,
    routing_events=256, routing_peer_slots=2, descriptor_requests=1, capabilities=1)
HELPER = dict(modules=4, names=32, groups=32, bodies=32, steps=128, data_bytes=4*MIB)
ADMISSION = dict(native_cpu_seconds=10, receipt_cpu_seconds=10, wall_seconds=30, memory_mib=512)
HTTP = dict(max_connections=2, max_requests=32, max_reply_bytes=96*MIB, operation_ms=5000)


def _error(error):
    return dict(type=type(error).__name__, message=str(error)[:1000])


def _separate(context, value):
    path = ordinary(value, fresh=True)
    for base in (context.installation, context.run, context.sources_owner,
                 context.sources_v5, context.sources_portable):
        base = ordinary(base)
        F.need(not path.is_relative_to(base) and not base.is_relative_to(path), "BODY_CHECK_STATE_SCOPE")
    return path


def _sources(context, expected, runtime, client):
    F.fields(expected, SOURCES)
    description, rows = runtime.describe(), {}
    for relative, name in SOURCES.items():
        wanted = C.digest_string(expected[relative])
        path = ordinary(context.sources_v5/relative, directory=False)
        module = import_module(name)
        row = description["sources"].get(relative)
        F.need(context.source_sha256["v5/"+relative] == wanted
               and Path(module.__file__).resolve() == path
               and row is not None and row["path"] == str(path) and row["sha256"] == wanted,
               "BODY_CHECK_ACTUAL_SOURCE_ORIGIN")
        read_pin(row, 2*MIB)
        F.need(all(owner is not None and owner._pins.get(path) ==
                   {key: row[key] for key in ("bytes", "sha256")}
                   for owner in client._origin_owners[:3]), "BODY_CHECK_ACTUAL_ISSUER_PINS")
        rows[relative] = {**row, "loaded_module": name}
    return rows


def _ports():
    streams = []
    try:
        for unused in range(5):
            stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            streams.append(stream)
            stream.bind(("127.0.0.1", 0))
        values = [stream.getsockname()[1] for stream in streams]
        F.need(len(set(values)) == 5, "BODY_CHECK_DISTINCT_PORTS")
        return dict(zip(("p_http", "q_http", "p_node", "q_node", "r_node"), values))
    finally:
        for stream in streams: stream.close()


def _location_limits():
    return dict(service_ms=180000, operation_ms=10000, query_events=256,
        provider_limit=2, advertised_keys=1, provider_ttl_ms=120000,
        reprovide_interval_ms=30000, maintenance_ms=60000, commands=24,
        descriptor_requests=4, descriptor_reply_bytes=16384, metadata={},
        transport=dict(outbound_attempts=32, inbound_upgrades=32,
                       receive_bytes=2*MIB, send_bytes=2*MIB))


def _channel(context, workspace, directory, deadline, namespace, egress, port,
             *, role, endpoints, bootstrap, body_domain=None):
    def pins(names):
        return {name: C.digest_string(context.source_sha256["portable/location/"+name]) for name in names}
    adoption = AdoptedLocationRuntime(context.sources_portable/"location", pins(SOURCE_NAMES),
        installation_root=context.installation, workspace_root=workspace.root)
    config = dict(schema="DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", role=role,
        state=str(directory/"location-state"), namespace=namespace, egress=deepcopy(egress),
        listen=[f"/ip4/127.0.0.1/tcp/{port}"], announce=[], bootstrap=bootstrap,
        endpoints=endpoints, limits=_location_limits())
    if body_domain is not None:
        config.update(schema="DMKN_V5_MAINTAINED_LOCATION_ROLES_V2", body_domain=deepcopy(body_domain))
    return ServiceLocationProcess(adoption, pins(ROLE_NAMES), config,
                                  directory/"location-channel", deadline=deadline)


def _inventory(p, q):
    key = SPLIT["module_id"], SPLIT["universes"], SPLIT["body_hash"]
    F.need(p.modules.db.execute("SELECT 1 FROM bodies WHERE module=? AND universes=? AND hash=?",
                               key).fetchone() is None, "BODY_CHECK_P_BODY_ABSENT")
    body = q.modules.get_body(SPLIT["module_id"], SPLIT["relative_name"],
                             SPLIT["universes"], SPLIT["body_hash"])
    F.need(C.body_id(body["expression"], body["universes"]) == SPLIT["body_hash"], "BODY_CHECK_Q_EXACT_BODY")
    pc, qc = p.modules.status()["counts"], q.modules.status()["counts"]
    F.need(pc["groups"] == 13 and pc["bodies"] == 10 and qc["groups"] == qc["bodies"] == 1
           and p.index.status()["objects"] == 1 and q.index.status()["objects"] == 0
           and p.packets.status()["counts"]["packets"] == 1
           and q.packets.status()["counts"]["packets"] == 0, "BODY_CHECK_SPLIT_INVENTORY")
    return dict(p=pc, q=qc, p_selected_body_absent=True, q_exact_body_readback=True,
        scope="PUBLIC_BODY_STORE_ABSENCE_NOT_INFORMATION_THEORETIC_PACKET_ABSENCE",
        mathematical_acceptance=False)


def _seed(p, q, packet, image):
    # Pure packet extraction and storage: this namespace is NOT a live issuer.
    extractor = SimpleNamespace(workspace=SimpleNamespace(_envelope=p._envelope), _aggregate_image=image)
    summary, groups, values, census = MixedClient._semantic_plan(extractor, packet)
    F.need(census["claims"] == census["frontiers"] == 1 and census["deltas"] == 2
           and census["warrants"] == 3, "BODY_CHECK_RETAINED_PACKET_SHAPE")
    root, selected, bodies, withheld = C.summary_id(summary), [], set(), 0
    split_key = SPLIT["module_id"], SPLIT["universes"], SPLIT["body_hash"]
    for (owner, unused), raw in sorted(groups.items()):
        opening = C.parse_json(raw); group = C.verify_group_opening(owner, opening)
        p.modules.put_group(owner, opening)
        for declaration in group["declarations"]:
            if owner == root and declaration["name"] == EXPORT: selected.append(opening)
            for digest in sorted(permitted_hashes(declaration)):
                arity = declaration["universes"]; key = owner, arity, digest
                if key in bodies: continue
                raw_value = values.get((arity, digest))
                F.need(raw_value is not None, "BODY_CHECK_NO_OTHER_MISSING_BODY")
                response = dict(schema=BODY_SCHEMA, module_id=owner, relative_name=declaration["name"],
                    universes=arity, body_hash=digest, expression=C.parse_json(raw_value))
                if key == split_key:
                    F.need(declaration["name"] == SPLIT["relative_name"], "BODY_CHECK_EXACT_SPLIT_NAME")
                    q.modules.put_group(owner, opening)
                    q.modules.put_body(owner, declaration["name"], response); withheld += 1
                else: p.modules.put_body(owner, declaration["name"], response)
                bodies.add(key)
    F.need(len(selected) == 1 and len(groups) == 13 and len(bodies) == 11 and withheld == 1,
           "BODY_CHECK_SEED_CENSUS")
    p.packets.put(root, packet)
    p.index.admit(p.adapter.encode_opening(root, EXPORT, selected[0]), expected_id=C.export_id(root, EXPORT))
    return dict(module=root, inventory=_inventory(p, q), packet_census=census, mathematical_acceptance=False)


def _endpoint(value):
    return {name: getattr(value, name) for name in ("host", "port", "tls", "server_name")}


def _capture(client, reader, channel):
    acquisition, search = client._acquisition, client._search
    return dict(objects=(client, reader, client.grant, client._budget, search, acquisition,
                        acquisition.structural, channel, channel.process, channel._start_task),
        owners=client._origin_owners,
        endpoints=(dict(search.endpoints), dict(search._adopted_endpoints),
                   dict(acquisition.endpoints), dict(acquisition.structural.endpoints)),
        deadlines=(client.grant.deadline, client._budget.deadline, search.session.deadline,
                   acquisition.structural.deadline, client._query_envelope.deadline,
                   client._body_pool.deadline, channel.deadline),
        limits=deepcopy((client._budget.limits, search.session.limits, channel.config)))


def _unchanged(before, client, reader, channel):
    after = _capture(client, reader, channel)
    F.need(all(a is b for a, b in zip(before["objects"], after["objects"]))
           and all(a is b for a, b in zip(before["owners"], after["owners"]))
           and all(before[key] == after[key] for key in ("endpoints", "deadlines", "limits")),
           "BODY_CHECK_ORIGINAL_IDENTITIES_MAPS_DEADLINES")


async def _stop(channel, context):
    if not channel.closed and not channel.channel_failed and channel.process is not None \
            and channel.process.returncode is None:
        result = await channel.command("stop", {}, until=min(channel.deadline, context.deadline-10,
                                                            time.monotonic()+10))
        F.need(result.get("status") == "STOPPED", "BODY_CHECK_NORMAL_NODE_STOP")
    async with asyncio.timeout_at(context.deadline-5): await channel.close()
    value = channel.report()
    F.need(value["closed"] and value["returncode"] == 0 and not value["channel_failed"]
           and not value["forced_termination"] and value["runtime_pre"] is not None
           and value["runtime_post"] is not None and value["role_pre"] == value["role_post"],
           "BODY_CHECK_CLEAN_NODE_CLOSE")
    raw = bytes(channel.stderr)
    F.need(0 < len(raw) <= 65536, "BODY_CHECK_NODE_DIAGNOSTIC_BOUND")
    lines = raw.splitlines()
    F.need(len(lines) == 1, "BODY_CHECK_NO_UNEXPECTED_NODE_STDERR")
    final = C.parse_json(lines[0], C.Limits(max_bytes=65536))
    F.need(final.get("status") == "LOCATION_IPC_CLOSED" and final["sequence"] == channel.sequence
           and final["mathematical_acceptance"] is False, "BODY_CHECK_NODE_TERMINAL")
    return dict(channel=value, stderr_hex=raw.hex(), terminal=final)


async def _discover(client, features, expected_endpoint, expected_root):
    located = await L.next_located_query(client, [dict(tag="declaration-kind", value="theorem")],
        deepcopy(LOCATION), deepcopy(SEARCH),
        routes=[dict(features=features, stripe=0, event_cap=256, peer_cap=2, descriptors=1)],
        descriptor_bytes=4096, descriptor_age_ms=60000)
    F.need(located["status"] == "QUERY_CONTACTS_READY" and len(located["contacts"]) == 1
           and located["generation"] == 1, "BODY_CHECK_GENUINE_INDEX_CONTACT")
    provider = located["contacts"][0]
    F.need(_endpoint(client._search.endpoints[provider]) == expected_endpoint, "BODY_CHECK_DISCOVERED_P")
    offer = await client.search_offer(provider, max_bytes=65536, max_expanded_bytes=131072,
                                     max_age_ms=60000, attempt_timeout_ms=5000)
    F.need(offer["status"] == "OFFERED", "BODY_CHECK_OFFER")
    partitions = [row for row in offer["partitions"] if row["anchor_count"] > 0]
    F.need(len(partitions) == 1, "BODY_CHECK_ONE_NONEMPTY_PARTITION")
    page = await client.search_page(provider, offer["snapshot_id"], partitions[0]["partition"], 0,
        dict(bytes=65536, hash_calls=200000, matches=4, node_reads=10000, record_probes=64,
             scanned=8, sql_vm_steps=100000, timeout_ms=1000),
        candidates_only=True, attempt_timeout_ms=5000)
    F.need(page["status"] == "VERIFIED_CANDIDATES" and len(page["matches"]) == 1,
           "BODY_CHECK_DISCOVERED_CANDIDATE")
    candidate = await client.resolve(provider, page["matches"][0])
    description = client.describe_candidate(candidate)
    F.need(description["locator"]["module_id"] == expected_root
           and description["locator"]["relative_name"] == EXPORT, "BODY_CHECK_RETURNED_EXPORT")
    packets = await client.packet_offers(candidate, max_offers=1, max_bytes=4096)
    F.need(len(packets["packets"]) == 1, "BODY_CHECK_ONE_PACKET_OFFER")
    return candidate, packets["packets"][0], dict(located=located, offer=offer, page=page,
        provider=provider, locator=description["locator"], packet=packets["packets"][0])


async def _collect(helper, client, channel, expected_q, report):
    staged = report["staged"]
    inventory, root = staged["members"], staged["module"]
    F.need(len(inventory) == 3, "BODY_CHECK_PACKET_MEMBERS")
    original = _capture(client, helper, channel)
    report["original_deadlines"] = dict(zip(("grant", "budget", "query", "structural", "envelope",
                                            "body_pool", "channel"), original["deadlines"]))
    report["original_endpoint_keys"] = [sorted(mapping) for mapping in original["endpoints"]]
    F.need(all(len(mapping) == 1 and all(_endpoint(endpoint) != expected_q for endpoint in mapping.values())
               for mapping in original["endpoints"]), "BODY_CHECK_Q_NOT_ORDINARY_CONTACT")
    report["rounds"], report["selected_internal_members"] = [], []
    selected_body = 0
    for ordinal in range(32):
        preview = helper.preview()
        row = dict(round=ordinal, preview=preview, actions=[]); report["rounds"].append(row)
        if preview["status"] == READY: break
        progressed = False
        for demand in preview["demands"]:
            if demand["kind"] == "NeedModuleEvidence":
                matches = [item for item in inventory if item["module"] == demand["module"]]
                F.need(len(matches) == 1, "BODY_CHECK_SINGLETON_MEMBER_SELECTION")
                result = helper.select_member(root, bytes(matches[0]["journal"]))
                row["actions"].append(dict(kind="select_member", **result))
                if result["status"] == "SELECTED_MEMBER":
                    report["selected_internal_members"].append(result); progressed = True
            resolved = await helper.resolve(demand, max_bytes=65536)
            row["actions"].append(dict(kind="resolve", demand=demand, status=resolved["status"],
                supplier=resolved["description"]["provider"], locator=resolved["description"]["locator"]))
            progressed |= resolved["status"] == "RESOLVED"
            if demand["kind"] != "NeedBody": continue
            if (demand["module"], demand["name"], demand["universes"], demand["body_hash"]) == (
                    SPLIT["module_id"], SPLIT["relative_name"], SPLIT["universes"], SPLIT["body_hash"]):
                F.need(selected_body == 0, "BODY_CHECK_ONE_EXACT_LOCATION")
                located = await helper.locate_body(demand, event_cap=256, peer_cap=2,
                                                  descriptor_requests=1, max_age_ms=60000)
                F.need(located["status"] == "BODY_CUSTODIANS_LOCATED"
                       and len(located["capabilities"]) == 1, "BODY_CHECK_Q_LOCATED")
                # Opaque capability never appears in reports; only the local
                # test verifies its selected endpoint and authenticated Q peer.
                capability = located["capabilities"][0]
                held = client._body_pool._entries[capability]
                F.need(_endpoint(held["endpoint"]) == expected_q
                       and held["peer"] == report["q_ready"]["location_ready"]["peer_id"],
                       "BODY_CHECK_ACTUAL_Q_DESCRIPTOR")
                report["body_location"] = {key: value for key, value in located.items() if key != "capabilities"}
                result = await helper.try_fetch_body_from(demand, capability, max_bytes=65536,
                                                         attempt_timeout_ms=5000)
                selected_body += 1
                _unchanged(original, client, helper, channel)
            else: result = await helper.fetch_body(demand, max_bytes=65536)
            row["actions"].append(dict(kind="fetch_body", demand=demand, **result))
            progressed |= result["status"] == "FETCHED"
        F.need(progressed, "BODY_CHECK_NO_STRUCTURAL_PROGRESS")
    else: F.need(False, "BODY_CHECK_ROUND_LIMIT")
    _unchanged(original, client, helper, channel)
    state = helper.report(); pool = client._body_pool.report()
    F.need(selected_body == 1 and state["modules"] == 2 and state["groups"] == 9
           and state["bodies"] == 9 and preview["cost"]["declarations"] == 12,
           "BODY_CHECK_SELECTED_CLOSURE")
    F.need(all(pool["used"][key] == 1 for key in ("route_operations_issued", "descriptor_requests_issued",
        "capabilities_issued", "capabilities_consumed", "body_attempts", "body_successes"))
        and pool["used"]["settled_unavailable"] == 0 and pool["retained_capabilities"] == 0,
        "BODY_CHECK_ONE_CONSUMED_CAPABILITY")
    report.update(structural=state, body_pool=pool, same_reader_owners_maps_deadlines=True,
                  reader_pid=channel.process.pid, before_admission=client.report())
    F.need(all(report["before_admission"][key]["attempts"] == 0 for key in ("receipt", "aggregate", "mixed"))
           and report["before_admission"]["counts"]["admission_submissions"] == 0
           and report["before_admission"]["counts"]["new_import_sessions"] == 0,
           "BODY_CHECK_STRUCTURAL_NOT_ACCEPTANCE")
    return original


async def run(context):
    params = deepcopy(dict(context.parameters))
    F.fields(params, ("schema", "action", "runtime_adoption", "foundation", "packet", "domain_path",
                     "domain_id", "workspace_paths", "workspace_config", "operation_limits", "expected_sources"))
    F.need(params["schema"] == SCHEMA and params["action"] == "explicit-temporary-adoption-and-located-body",
           "BODY_CHECK_EXPLICIT_SCOPE")
    F.need(params["foundation"]["sha256"] == FOUNDATION_SHA and params["foundation"]["bytes"] == 23313
           and params["packet"]["sha256"] == PACKET_SHA and params["packet"]["bytes"] == 658554,
           "BODY_CHECK_RETAINED_INPUT_IDENTITIES")
    F.fields(params["workspace_paths"], ("p", "q", "r"))
    F.need(context.limits["memory_mib"] == 512 and context.limits["cpu_seconds"] <= 150
           and context.limits["wall_seconds"] <= 300 and context.limits["active_processes"] <= 6,
           "BODY_CHECK_OUTER_ENVELOPE")
    limits = params["operation_limits"]
    F.need(limits["wall_seconds"] == 210 and limits["controller_cpu_seconds"] == 120
           and limits["worker_cpu_seconds"] == 30 and limits["acquisition"] == dict(requests=40,
               reply_bytes=16*MIB, verify_attempts=1, verification_input_bytes=MIB, worker_cpu_seconds=30),
           "BODY_CHECK_ORIGINAL_OPERATION_ENVELOPE")
    output = ordinary(context.location_workspace/"exact-custody-installed-result.json", fresh=True, directory=False)
    report = dict(schema=RESULT_SCHEMA, status="FAILED", stage="paths", error=None, cleanup_errors=[],
        mathematical_acceptance=False, global_complete=False, full_v5_release=False,
        new_proof_calls=0, authoring_calls=0, public_network_calls=0, expected_node_roles=3,
        domain_created=False, domain_withdrawn=False, client_closed=False, reader_workspace_closed=False,
        p_workspace_closed=False, p_http_closed=False, nodes_closed=False, q_service=None,
        authority="OPERATION_EVIDENCE_NOT_TRANSFERABLE_AUTHORITY", started=time.monotonic(),
        outer_deadline=context.deadline,
        q_diagnostics_scope="PUBLIC_SERVICE_REPORT_AND_STDERR_BYTE_COUNT_RAW_CHILD_STDERR_NOT_EXPOSED",
        scope="INSTALLED_LOCATED_EXACT_BODY_SAME_READER_RETAINED_I_NATIVE_IMPORT")
    workspaces, p_provider, p_node, r_node = {}, None, None, None
    client = helper = domain = q_task = None
    primary = cancelled = None
    try:
        paths = {key: _separate(context, value) for key, value in params["workspace_paths"].items()}
        domain_path = _separate(context, params["domain_path"])
        all_paths = [*paths.values(), domain_path]
        F.need(all(not a.is_relative_to(b) and not b.is_relative_to(a)
                   for i, a in enumerate(all_paths) for b in all_paths[i+1:]), "BODY_CHECK_DISJOINT_STATE")
        config = params["workspace_config"]
        packet = read_pin(params["packet"], MIB)
        foundation = read_pin(params["foundation"], 16*MIB)
        for role in ("p", "q"): workspaces[role] = Workspace.open(paths[role], config, create=True)
        report["seed"] = _seed(workspaces["p"], workspaces["q"], packet, config["wire_profile"]["aggregate_image"])
        namespace = workspaces["p"].adapter.namespace
        body_domain = dict(foundation=workspaces["q"].modules.foundation, policy=workspaces["q"].modules.policy)
        for workspace in workspaces.values(): workspace.close()
        workspaces.clear()
        ports = report["ports"] = _ports()
        egress = dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
            test_endpoints=[dict(host="127.0.0.1", port=value) for value in sorted(ports.values())])
        p_endpoint = dict(host="127.0.0.1", port=ports["p_http"], tls=False, server_name=None)
        q_endpoint = dict(host="127.0.0.1", port=ports["q_http"], tls=False, server_name=None)
        workspaces["p"] = Workspace.open(paths["p"], config, create=False)
        p_workspace = workspaces["p"]
        features = p_workspace.adapter.compile_query([dict(tag="declaration-kind", value="theorem")])
        p_provider = CompositeProvider(index=p_workspace.index, custody=p_workspace.modules,
                                       packets=p_workspace.packets, **HTTP)
        endpoint = await p_provider.start(host="127.0.0.1", port=ports["p_http"], tls_context=None)
        F.need(_endpoint(endpoint) == p_endpoint, "BODY_CHECK_P_ENDPOINT")
        p_node = _channel(context, p_workspace, p_workspace.root, context.deadline-40,
            namespace, egress, ports["p_node"], role="index-provider", endpoints=[p_endpoint], bootstrap=[])
        report["stage"] = "p-start"
        # Conservative lower bound on actual child-start service horizon.
        p_start_lower = time.monotonic()
        report["p_ready"] = await p_node.start()
        A._live_status(report["p_ready"], namespace)
        bootstrap = f'/ip4/127.0.0.1/tcp/{ports["p_node"]}/p2p/{P.peer_id(report["p_ready"]["peer_id"])}'
        q_output = context.location_workspace/"q-service"; q_output.mkdir()
        q_params = dict(schema=A.SCHEMA_V3, mode="validated", workspace_path=str(paths["q"]),
            workspace_config=config, bind=dict(host="127.0.0.1", port=ports["q_http"]), tls=None,
            service_limits={**HTTP, "lifetime_seconds": 90}, index_view=None, body_routes=[deepcopy(SPLIT)],
            location=dict(installation_root=str(context.installation), egress=egress,
                listen=[f'/ip4/127.0.0.1/tcp/{ports["q_node"]}'], announce=[], bootstrap=[bootstrap],
                limits=_location_limits(), routes=[], health_interval_ms=30000))
        q_context = replace(context, location_workspace=q_output, parameters=MappingProxyType(q_params))
        report["stage"] = "q-start"
        q_task = asyncio.create_task(A.serve(q_context))
        ready_path = q_output/"service-ready.json"
        while not ready_path.exists():
            F.need(not q_task.done() and time.monotonic() < min(context.deadline-100, p_start_lower+60),
                   "BODY_CHECK_Q_READY_WINDOW")
            await asyncio.sleep(0.05)
        F.need(ready_path.stat().st_size <= MIB, "BODY_CHECK_READY_BYTES")
        ready = C.parse_json(ready_path.read_bytes(), C.Limits(max_bytes=MIB)); report["q_ready"] = ready
        report["clocks"] = dict(p_start_lower=p_start_lower, p_service_end_lower=p_start_lower+180,
            p_controller_deadline=p_node.deadline, q_ready_observed=time.monotonic(), q_deadline=ready["deadline"])
        F.need(ready["schema"] == "DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_READY_V3"
               and ready["endpoint"] == q_endpoint and ready["route_dispatch"] == []
               and len(ready["body_route_dispatch"]) == 1 and ready["body_readback"]["domain"] == body_domain
               and ready["body_readback"]["observations"]["bodies_read"] == 1
               and ready["deadline"] > time.monotonic()+45
               and p_start_lower+180 > ready["deadline"]+55,
               "BODY_CHECK_Q_V3_READBACK_AND_NESTED_SERVICE_CLOCKS")
        published = await p_node.command("publish", dict(features=features, stripe=0),
                                        until=min(p_node.deadline, time.monotonic()+10))
        A._hint(published, P.route_key(namespace, features, 0)); report["p_publication"] = published
        report["stage"] = "original-reader-owners"
        support = RuntimeProfile.support_manifest(context, params["runtime_adoption"])
        domain = T.TrustDomain.create(domain_path, C.digest_string(params["domain_id"]), support)
        report["domain_created"] = True; report["identity"] = domain.identity()
        runtime = RuntimeProfile.from_context(context, params["runtime_adoption"], trust_domain=domain)
        workspaces["r"] = Workspace.open(paths["r"], config, create=True)
        workspace = workspaces["r"]
        grant = workspace.reserve(limits, outer_deadline=context.deadline-10)
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=False,
            foundation_bytes=foundation, foundation_sha256=FOUNDATION_SHA)
        report["operation_id"] = grant.identifier
        report["installed_sources"] = _sources(context, params["expected_sources"], runtime, client)
        r_node = _channel(context, workspace, grant.directory, grant.deadline, namespace, egress,
            ports["r_node"], role="reader", endpoints=[], bootstrap=[bootstrap], body_domain=body_domain)
        report["reservation"] = L.reserve_located_queries(client, r_node,
            dict(search={**SEARCH, "generations": 1}, location=deepcopy(LOCATION)), P.OwnerEgressPolicy(egress))
        report["body_reservation"] = client.reserve_body_location(deepcopy(BODY))
        F.need(client._budget.report()["external_prepaid"] == [
            dict(label="located-query-envelope", requests=6, reply_bytes=270336),
            dict(label="body-location", requests=2, reply_bytes=4096)], "BODY_CHECK_TWO_ORIGINAL_PREPAYMENTS")
        report["stage"] = "located-query"
        candidate, entry, report["discovery"] = await _discover(client, features, p_endpoint, report["seed"]["module"])
        helper = SemanticReader(client, candidate, limits=deepcopy(HELPER))
        report["staged"] = await helper.stage(candidate, entry)
        initial = helper.report()
        F.need(initial["groups"] == initial["modules"] == 1 and initial["bodies"] == 0,
               "BODY_CHECK_TARGET_OPENING_ONLY")
        F.need(min(grant.deadline, client._acquisition.structural.deadline,
                   client._search.session.deadline, client._query_envelope.deadline) > ready["deadline"]+55,
               "BODY_CHECK_FINISH_CLOCK_RESERVE")
        report["stage"] = "same-reader-body"
        original = await _collect(helper, client, r_node, q_endpoint, report)
        report["stage"] = "network-closure"
        # Keep P/R available until Q's finite maintenance and cleanup finish.
        async with asyncio.timeout_at(min(context.deadline-60, ready["deadline"]+35, p_start_lower+160)):
            report["q_service"] = await q_task
        q_result = report["q_service"]
        F.need(q_result["status"] == "PASS" and q_result["counters"]["requests"] == 1
               and q_result["counters"]["failures"] == 0
               and q_result["cleanup"] == dict(location_closed=True, http_closed=True,
                                               workspace_closed=True, errors=[]), "BODY_CHECK_Q_NORMAL_CLOSE_ONE_GET")
        F.need(time.monotonic()+11 < p_start_lower+180, "BODY_CHECK_OLDEST_NODE_STOP_MARGIN")
        report["p_close"] = await _stop(p_node, context)
        report["r_close"] = await _stop(r_node, context)
        report["nodes_closed"] = True
        report["clocks"]["nodes_closed"] = time.monotonic()
        async with asyncio.timeout_at(context.deadline-45): await p_provider.stop()
        report["p_http"] = p_provider.status()
        F.need(p_provider.server is None and not p_provider.tasks and p_provider.reserved_reply_bytes == 0
               and report["p_http"]["failures"] == 0, "BODY_CHECK_P_HTTP_CLOSED")
        report["p_http_closed"] = True
        workspaces["p"].close(); del workspaces["p"]; report["p_workspace_closed"] = True
        _unchanged(original, client, helper, r_node)
        F.need(time.monotonic()+35 < min(grant.deadline, context.deadline-10), "BODY_CHECK_RETAINED_ADMISSION_MARGIN")
        report["stage"] = "retained-admission"
        report["clocks"]["admission_started"] = time.monotonic()
        result = helper.finish({report["staged"]["module"]: deepcopy(ADMISSION)})
        report["clocks"]["admission_finished"] = time.monotonic()
        after = client.report()
        F.need(result["status"] == "READY" and result["context"] is not None
               and result["mathematical_acceptance"] is False
               and result["cost"]["groups"] == 9 and result["cost"]["declarations"] == 12
               and result["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
               "BODY_CHECK_RETAINED_LIVE_CONTEXT")
        F.need(after["receipt"]["attempts"] == after["mixed"]["attempts"] == 1
               and after["aggregate"]["attempts"] == 0 and after["mixed"]["reserved_worker_cpu"] == 30
               and after["counts"]["admission_submissions"] == after["counts"]["new_import_sessions"] == 1
               and after["counts"]["author_calls"] == after["counts"]["publication_attempts"] == 0
               and after["preparation"] is None and all(after["acquisition"]["used"][key] ==
                   report["before_admission"]["acquisition"]["used"][key] for key in ("requests", "reply_bytes")),
               "BODY_CHECK_ONE_UNCHANGED_ADMISSION_NO_POST_CLOSURE_NETWORK")
        report.update(after_admission=after, live_context_returned=True,
            result={key: result[key] for key in ("status", "demands", "cost", "mathematical_acceptance")},
            retained_receipt_verified=True, retained_mixed_admission=True, helper=helper.report())
        for role in ("p", "q"): workspaces[role] = Workspace.open(paths[role], config, create=False)
        report["post_service_inventory"] = _inventory(workspaces["p"], workspaces["q"])
        report["status"] = "COMPLETED"
    except BaseException as error:
        primary = error; report["error"] = _error(error)
        if isinstance(error, asyncio.CancelledError): cancelled = error
    finally:
        if q_task is not None:
            try:
                if not q_task.done():
                    async with asyncio.timeout_at(context.deadline-25): await asyncio.shield(q_task)
                report["q_service"] = await q_task
                F.need(report["q_service"]["status"] == "PASS", "BODY_CHECK_Q_SERVICE_FAILED")
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="q-service", **_error(error)))
                if not q_task.done(): q_task.cancel()
                try:
                    async with asyncio.timeout_at(context.deadline-5): await q_task
                except BaseException as tail:
                    report["cleanup_errors"].append(dict(component="q-reap", **_error(tail)))
        for role, channel in (("r", r_node), ("p", p_node)):
            if channel is None: continue
            try:
                if role+"_close" not in report: report[role+"_close"] = await _stop(channel, context)
            except BaseException as error:
                report["cleanup_errors"].append(dict(component=role+"-node", **_error(error)))
                try:
                    async with asyncio.timeout_at(context.deadline-5): await channel.close()
                except BaseException as tail:
                    report["cleanup_errors"].append(dict(component=role+"-reap", **_error(tail)))
                report[role+"_failed_channel"] = channel.report()
                report[role+"_stderr_hex"] = bytes(channel.stderr).hex()
        if p_provider is not None and not report["p_http_closed"]:
            try:
                async with asyncio.timeout_at(context.deadline-5): await p_provider.stop()
                report["p_http"] = p_provider.status()
                report["p_http_closed"] = p_provider.server is None and not p_provider.tasks
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="p-http", **_error(error)))
        if helper is not None:
            try:
                if "helper" not in report: report["helper"] = helper.report()
                helper.close()
            except BaseException as error: report["cleanup_errors"].append(dict(component="helper", **_error(error)))
        if client is not None:
            try:
                report["client"] = closed = await client.close()
                F.need(closed["closed"] and not closed["cleanup_uncertain"]
                       and all(closed[name] is not None and closed[name]["closed"]
                               for name in ("receipt", "aggregate", "mixed"))
                       and closed["preparation"] is None, "BODY_CHECK_OWNER_CLEANUP")
                if report["status"] == "COMPLETED":
                    F.need(closed["status"] == "CLOSED" and not closed["failures"], "BODY_CHECK_CLEAN_CLIENT")
                report["client_closed"] = True
            except BaseException as error: report["cleanup_errors"].append(dict(component="client", **_error(error)))
        for role, workspace in workspaces.items():
            closed = H._close_workspace(workspace, report["cleanup_errors"])
            if role == "r": report["reader_workspace_closed"] = closed
            if role == "p": report["p_workspace_closed"] = closed
        if domain is not None:
            try:
                domain.withdraw("Explicit temporary exact-custody installed boundary completed or failed")
                marker = ordinary(Path(params["domain_path"])/"WITHDRAWN", directory=False)
                F.need(marker.stat().st_size <= 16384, "BODY_CHECK_WITHDRAWAL_BOUND")
                value = C.parse_json(marker.read_bytes(), C.Limits(max_bytes=16384))
                F.need(value["schema"] == "DMKN_LOCAL_TRUST_WITHDRAWN_V1"
                       and value["adoption"] == report["identity"], "BODY_CHECK_EXACT_WITHDRAWAL")
                report.update(domain_withdrawn=True, withdrawal=dict(path=str(marker), marker=value))
            except BaseException as error: report["cleanup_errors"].append(dict(component="withdrawal", **_error(error)))
        required = ("domain_created", "domain_withdrawn", "client_closed", "reader_workspace_closed",
                    "p_workspace_closed", "p_http_closed", "nodes_closed")
        report["finished"] = time.monotonic()
        if report["cleanup_errors"] or not all(report[key] for key in required) or report["finished"] >= context.deadline:
            report["status"] = "FAILED"
        if report["status"] == "COMPLETED": report["stage"] = "done"
        try: remote_reader._save(output, report)
        except BaseException as error:
            if primary is not None: raise BaseExceptionGroup("Custody boundary and evidence save failed", [primary, error])
            raise
    if cancelled is not None: raise cancelled
    return report


def main(context):
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1

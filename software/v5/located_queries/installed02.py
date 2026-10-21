"""One explicitly provisioned installed boundary, not ordinary trust auto-adoption.

Real original issuers and one real loopback location child; two isolated queries,
no provider, mathematical admission or native/proof production. Root selects the
exact installed request and enclosing Job. All temporary trust is withdrawn.
"""
import asyncio
from copy import deepcopy
from importlib import import_module
from pathlib import Path
import socket
import time

from admission import trust as T
from client import located_queries as L, remote_reader
from client.runtime import RuntimeProfile, read_pin
from client.serve_workspace import _close_workspace
from client.workspace_evidence import SCHEMA as WORKSPACE_SCHEMA
from client.workspace_validated import Workspace
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from location.controller import AdoptedLocationRuntime, SOURCE_NAMES
from location.controller_services import ServiceLocationProcess, ROLE_NAMES
from location.protocol import OwnerEgressPolicy
from modules import codec as C

MIB = 1024**2
SCHEMA = "DMKN_V5_ADAPTIVE_INSTALLED_V1"
RESULT_SCHEMA = "DMKN_V5_ADAPTIVE_INSTALLED_RESULT_V1"
SOURCES = {
    "client/direct_contacts.py": "client.direct_contacts",
    "client/workspace_validated.py": "client.workspace_validated",
    "client/semantic_reader.py": "client.semantic_reader",
    "evidence_network/transport.py": "evidence_network.transport",
    "client/located_queries.py": "client.located_queries",
}
SEARCH = dict(providers=1, snapshots=1, requests=1, pages=1, examined=1,
              candidates=1, bytes=1024, inflight=1, wall_ms=90000)
LOCATION = dict(route_operations=1, routing_events=8, routing_peer_slots=1,
                descriptor_requests=1, contacts=1, reply_bytes=2048, wall_ms=90000)


def _separate(context, value):
    path = ordinary(value, fresh=True)
    for value in (context.installation, context.run, context.sources_owner,
                  context.sources_v5, context.sources_portable):
        root = ordinary(value)
        F.need(not path.is_relative_to(root) and not root.is_relative_to(path),
               "ADAPTIVE_STATE_DISJOINT_FROM_LAUNCH")
    return path


def _sources(context, expected, runtime, client):
    F.fields(expected, SOURCES)
    root, described = ordinary(context.sources_v5), runtime.describe()
    rows = {}
    for relative, name in SOURCES.items():
        wanted = C.digest_string(expected[relative])
        path = ordinary(root/relative, directory=False)
        F.need(context.source_sha256.get("v5/"+relative) == wanted,
               "ADAPTIVE_LAUNCHER_SOURCE_PIN")
        module = import_module(name)
        F.need(Path(module.__file__).resolve() == path, "ADAPTIVE_LOADED_SOURCE_ORIGIN")
        row = described["sources"].get(relative)
        F.need(row is not None and row["path"] == str(path) and row["sha256"] == wanted,
               "ADAPTIVE_RUNTIME_SOURCE_PIN")
        read_pin(row, 2*MIB)
        for owner in client._origin_owners[:3]:
            F.need(owner is not None and owner._pins.get(path) ==
                   {key: row[key] for key in ("bytes", "sha256")},
                   "ADAPTIVE_REAL_ORIGINAL_ISSUER_PIN")
        rows[relative] = {**row, "loaded_module": name}
    return {"sources": rows, "runtime_python_source_count": len(described["sources"]),
            "all_changed_sources_in_real_owners": True}


def _ephemeral_port():
    # The port is selected once. A race before the child's bind is a failure,
    # never a retry or an expanded loopback egress policy.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
        stream.bind(("127.0.0.1", 0))
        return stream.getsockname()[1]


def _child(context, workspace, grant):
    def pins(names):
        return {name: C.digest_string(context.source_sha256["portable/location/"+name])
                for name in names}
    adoption = AdoptedLocationRuntime(Path(context.sources_portable)/"location", pins(SOURCE_NAMES),
        installation_root=context.installation, workspace_root=workspace.root)
    port = _ephemeral_port()
    egress = dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test",
                  public_ports=[], test_endpoints=[dict(host="127.0.0.1", port=port)])
    limits = dict(service_ms=120000, operation_ms=1000, query_events=8,
        provider_limit=1, advertised_keys=1, provider_ttl_ms=120000,
        reprovide_interval_ms=30000, maintenance_ms=60000, commands=2,
        descriptor_requests=1, descriptor_reply_bytes=4096, metadata={},
        transport=dict(outbound_attempts=1, inbound_upgrades=1,
                       receive_bytes=1024, send_bytes=1024))
    configuration = dict(schema="DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", role="reader",
        state=str(grant.directory/"location-state"), namespace=workspace.adapter.namespace,
        egress=egress, listen=[f"/ip4/127.0.0.1/tcp/{port}"], announce=[], bootstrap=[],
        endpoints=[], limits=limits)
    channel = ServiceLocationProcess(adoption, pins(ROLE_NAMES), configuration,
        grant.directory/"location-channel", deadline=grant.deadline)
    return channel, OwnerEgressPolicy(egress)


def _envelope():
    return {
        "search": {**SEARCH, **{key: 2*SEARCH[key] for key in L.SEARCH_ADDITIVE},
                   "generations": 2, "wall_ms": 120000},
        "location": {**LOCATION, **{key: 2*LOCATION[key] for key in L.LOCATION_ADDITIVE},
                     "wall_ms": 120000},
    }


def _no_math(value):
    F.need(all(count == 0 for count in value["counts"].values())
           and all(value[name] is not None and value[name]["attempts"] == 0
                   for name in ("receipt", "aggregate", "mixed"))
           and value["preparation"] is None
           and all(value[name] is None for name in ("search", "location", "transport"))
           and not value["publications"], "ADAPTIVE_NO_MATHEMATICAL_OR_HTTP_WORK")


def _completed_queries(client):
    value = client.report()
    _no_math(value)
    F.need(value["calls"] == 3 and not value["failures"]
           and not value["cleanup_uncertain"], "ADAPTIVE_EXPECTED_CLIENT_CALLS")
    budget, envelope = value["acquisition"], value["iterative_queries"]
    F.need(budget["used"] == dict(requests=6, reply_bytes=4096, verify_attempts=0,
                                  verification_input_bytes=0, worker_cpu_seconds=0)
           and budget["pending_requests"] == budget["reserved_reply_bytes"] == 0
           and budget["external_prepaid"] == [dict(label="located-query-envelope",
                                                    requests=6, reply_bytes=4096)],
           "ADAPTIVE_ONE_EXACT_PREPAYMENT")
    F.need(envelope["status"] == "NO_CONTACTS"
           and envelope["search_allocated"] == {key: 2*SEARCH[key] for key in L.SEARCH_ADDITIVE}
           and envelope["location_allocated"] == {key: 2*LOCATION[key] for key in L.LOCATION_ADDITIVE}
           and envelope["child_started"] is True and len(envelope["generations"]) == 2,
           "ADAPTIVE_TWO_FUNDED_GENERATIONS")
    rows = envelope["generations"]
    F.need(rows[0]["query_sha256"] != rows[1]["query_sha256"], "ADAPTIVE_DISTINCT_QUERIES")
    for ordinal, row in enumerate(rows, 1):
        outcome = row["outcome"]
        F.need(row["generation"] == ordinal and row["status"] == "NO_CONTACTS_IN_SELECTED_ROUTE_PLAN"
               and sum(row["route_terminations"].values()) == 1
               and outcome["location"]["status"] == "RETIRED_NO_CONTACTS"
               and outcome["location"]["pending_requests"] == outcome["location"]["contacts"] == 0
               and outcome["location"]["used"]["route_operations"] == 1
               and outcome["location"]["used"]["descriptor_requests"] == 0
               and all(outcome[key] is None for key in
                       ("search", "search_http", "acquisition_http", "structural_http")),
               "ADAPTIVE_SETTLED_EMPTY_GENERATION")
    return value


def _closed_channel(channel):
    result = channel.report()
    F.need(result["closed"] and not result["channel_failed"] and result["returncode"] == 0
           and not result["forced_termination"] and result["commands"] == 2
           and result["reply_frames"] == 3 and result["runtime_pre"] is not None
           and result["runtime_post"] is not None
           and result["role_pre"] == result["role_post"], "ADAPTIVE_REAL_CHILD_CLEANUP")
    raw = bytes(channel.stderr)
    F.need(0 < len(raw) <= 65536, "ADAPTIVE_TERMINAL_DIAGNOSTIC_BOUND")
    terminal = []
    for line in raw.splitlines():
        if not line.startswith(b'{"status":"LOCATION_IPC_CLOSED"'):
            continue
        item = C.parse_json(line, C.Limits(max_bytes=65536))
        if item.get("status") == "LOCATION_IPC_CLOSED": terminal.append(item)
    F.need(len(terminal) == 1, "ADAPTIVE_ONE_CHILD_TERMINAL_DIAGNOSTIC")
    final = terminal[0]
    F.need(final["sequence"] == 2 and final["descriptor_unavailable"] == 0
           and final["mathematical_acceptance"] is False, "ADAPTIVE_CHILD_SEQUENCE")
    transport = final["transport"]
    for key in ("outbound_attempts", "inbound_upgrades", "refused_outbound", "refused_inbound",
                "receive_observed_bytes", "receive_admitted_bytes", "receive_refused_bytes",
                "send_admitted_bytes", "send_refused_bytes", "attached_connections", "active_connections"):
        F.need(transport[key] == 0, "ADAPTIVE_ISOLATED_TRANSPORT:"+key)
    F.need(transport["exhausted"] is None, "ADAPTIVE_TRANSPORT_NOT_EXHAUSTED")
    return {"channel": result, "terminal": final,
            "local_listening_socket": True, "external_peer_exchange_observed": False}


async def run(context):
    params = deepcopy(dict(context.parameters))
    F.fields(params, {"schema", "action", "runtime_adoption", "foundation", "domain_path",
        "domain_id", "workspace_path", "workspace_config", "operation_limits", "expected_sources"})
    F.need(params["schema"] == SCHEMA and params["action"] == "explicit-temporary-adoption-and-query",
           "ADAPTIVE_EXPLICIT_TEST_PROVISIONING")
    F.need(params["workspace_config"]["schema"] == WORKSPACE_SCHEMA,
           "ADAPTIVE_ORDINARY_WORKSPACE")
    work, run_path = ordinary(context.location_workspace), ordinary(context.run)
    F.need(work != run_path and work.is_relative_to(run_path), "ADAPTIVE_OUTPUT_SCOPE")
    output = ordinary(work/"adaptive-installed-result.json", fresh=True, directory=False)
    F.need(time.monotonic() < context.deadline-10, "ADAPTIVE_CLEANUP_MARGIN")
    workspace = client = channel = domain = None
    primary = cancelled = None
    report = dict(schema=RESULT_SCHEMA, status="FAILED", stage="paths", error=None,
        cleanup_errors=[], client=None, client_closed=False, workspace_closed=False,
        channel_closed=False, domain_created=False, domain_withdrawn=False,
        proof_calls=0, native_calls=0, authoring_calls=0, mathematical_acceptance=False,
        full_v5_release=False, global_complete=False, started=time.monotonic(),
        scope="EXPLICIT_TEMPORARY_TRUST_REAL_OWNERS_ONE_ISOLATED_CHILD_TWO_QUERIES")
    try:
        domain_path = _separate(context, params["domain_path"])
        workspace_path = _separate(context, params["workspace_path"])
        F.need(not domain_path.is_relative_to(workspace_path)
               and not workspace_path.is_relative_to(domain_path), "ADAPTIVE_DISJOINT_STATE")
        C.digest_string(params["domain_id"])
        report["stage"] = "explicit-temporary-adoption"
        support = RuntimeProfile.support_manifest(context, params["runtime_adoption"])
        domain = T.TrustDomain.create(domain_path, params["domain_id"], support)
        report["domain_created"] = True
        report["identity"] = domain.identity()
        report["trust_domain"] = dict(directory=str(domain_path), **report["identity"])
        report["stage"] = "real-original-owners"
        runtime = RuntimeProfile.from_context(context, params["runtime_adoption"], trust_domain=domain)
        foundation = read_pin(params["foundation"], 16*MIB)
        workspace = Workspace.open(workspace_path, params["workspace_config"], create=True)
        grant = workspace.reserve(params["operation_limits"], outer_deadline=context.deadline-10)
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=False,
            foundation_bytes=foundation, foundation_sha256=params["foundation"]["sha256"])
        report["operation_id"] = grant.identifier
        report["installed_sources"] = _sources(context, params["expected_sources"], runtime, client)
        channel, policy = _child(context, workspace, grant)
        original = client.grant, client._budget, client._origin_owners
        report["stage"] = "reserve-located-envelope"
        report["reservation"] = L.reserve_located_queries(client, channel, _envelope(), policy)
        path = Path(L.__file__).resolve()
        F.need(client._required_origins.get("client.located_queries") == path
               and client._source_pins.get(path) == {key: report["installed_sources"]["sources"]
                    ["client/located_queries.py"][key] for key in ("bytes", "sha256")}
               and client._query_envelope is client._origin_query_envelope,
               "ADAPTIVE_REGISTERED_HELPER_AND_ENVELOPE")
        report["helper_registered_in_client"] = True
        report["queries"] = []
        process = start_task = None
        for ordinal, kind in enumerate(("theorem", "definition"), 1):
            report["stage"] = "query-"+str(ordinal)
            specs = [dict(tag="declaration-kind", value=kind)]
            features = workspace.adapter.compile_query(specs)
            result = await L.next_located_query(client, specs, deepcopy(LOCATION), deepcopy(SEARCH),
                routes=[dict(features=features, stripe=0, event_cap=8, peer_cap=1, descriptors=0)],
                descriptor_bytes=1024)
            F.need(result["status"] == "NO_CONTACTS_IN_SELECTED_ROUTE_PLAN"
                   and result["generation"] == ordinal and result["contacts"] == [],
                   "ADAPTIVE_ACTUAL_NO_CONTACT_RESULT")
            if ordinal == 1: process, start_task = channel.process, channel._start_task
            F.need(process is not None and channel.process is process
                   and channel._start_task is start_task and process.returncode is None
                   and channel.sequence == ordinal and client._channel is channel
                   and client.grant is original[0] and client._budget is original[1]
                   and all(now is before for now, before in zip(client._origin_owners, original[2])),
                   "ADAPTIVE_ONE_ORIGINAL_CHILD_AND_AUTHORITY")
            report["queries"].append(dict(specs=specs, features=features, result=result,
                                          child_pid=process.pid, command_sequence=channel.sequence))
        report["before_close"] = _completed_queries(client)
        report["same_original_child_and_owners"] = True
        report["stage"] = "cleanup"
        report["status"] = "COMPLETED"
    except BaseException as error:
        primary = error
        report["error"] = remote_reader._error(error)
        if isinstance(error, asyncio.CancelledError): cancelled = error
    finally:
        if client is not None:
            try:
                closed = await client.close()
                report["client"] = closed
                F.need(closed["closed"] and closed["status"] in ("CLOSED", "FAILED")
                       and not closed["cleanup_uncertain"]
                       and all(closed[name] is not None and closed[name]["closed"]
                               for name in ("receipt", "aggregate", "mixed"))
                       and closed["preparation"] is None, "ADAPTIVE_OWNER_CLEANUP")
                _no_math(closed)
                if report["status"] == "COMPLETED":
                    F.need(closed["status"] == "CLOSED" and not closed["failures"],
                           "ADAPTIVE_SUCCESS_REQUIRES_CLEAN_CLIENT_CLOSE")
                report["client_closed"] = True
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="client", **remote_reader._error(error)))
                if isinstance(error, asyncio.CancelledError): cancelled = error
        if channel is not None:
            try:
                # Also covers failures before the client took channel ownership.
                await channel.close()
                report["channel"] = channel.report()
                F.need(channel.closed and (channel.process is None or channel.process.returncode is not None),
                       "ADAPTIVE_CHILD_REAPED")
                report["channel_closed"] = True
                raw_stderr = bytes(channel.stderr)
                F.need(len(raw_stderr) <= 65536, "ADAPTIVE_RAW_DIAGNOSTIC_BOUND")
                report["channel_stderr_hex"] = raw_stderr.hex()
                if report["status"] == "COMPLETED": report["isolated_child"] = _closed_channel(channel)
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="channel", **remote_reader._error(error)))
                if isinstance(error, asyncio.CancelledError): cancelled = error
        if workspace is not None:
            report["workspace_closed"] = _close_workspace(workspace, report["cleanup_errors"])
        if domain is not None:
            try:
                domain.withdraw("Explicit temporary installed adaptive-query boundary completed or failed")
                marker = ordinary(Path(params["domain_path"])/"WITHDRAWN", directory=False)
                F.need(marker.stat().st_size <= 16384, "ADAPTIVE_WITHDRAWAL_BOUND")
                with marker.open("rb") as stream: raw = stream.read(16385)
                value = C.parse_json(raw, C.Limits(max_bytes=16384))
                F.fields(value, ("schema", "adoption", "reason"))
                F.need(value["schema"] == "DMKN_LOCAL_TRUST_WITHDRAWN_V1"
                       and value["adoption"] == report["identity"], "ADAPTIVE_EXACT_WITHDRAWAL")
                report["withdrawal"] = dict(path=str(marker), marker=value)
                report["domain_withdrawn"] = True
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="withdrawal", **remote_reader._error(error)))
        required = ("domain_created", "domain_withdrawn", "client_closed", "workspace_closed", "channel_closed")
        if report["cleanup_errors"] or not all(report[key] for key in required): report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        if report["finished"] >= context.deadline:
            report["status"] = "FAILED"
            report["cleanup_errors"].append(dict(component="deadline", message="ORIGINAL_DEADLINE"))
        if report["status"] == "COMPLETED": report["stage"] = "done"
        try: remote_reader._save(output, report)
        except BaseException as error:
            if primary is not None:
                raise BaseExceptionGroup("Adaptive boundary and evidence write failed", [primary, error])
            raise
    if cancelled is not None: raise cancelled
    return report


def main(context):
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1

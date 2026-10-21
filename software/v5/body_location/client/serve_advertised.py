"""Finite retained-workspace HTTP service plus existing maintained location.

Trusted local owner entry through client.boot, not a daemon or remote code API.
Discovery hints carry no mathematical, availability, or completeness authority.
The HTTP-only predecessor and retained location implementation stay unchanged.
"""
import asyncio
from copy import deepcopy
import ipaddress
import math
import re
import time
from types import SimpleNamespace

from client import serve_workspace as H
from discovery import formal_features as F
from location import controller as B, protocol as P
from location.controller import AdoptedLocationRuntime, SOURCE_NAMES
from location.controller_services import ServiceLocationProcess, ROLE_NAMES
from modules import codec as C

SCHEMA = "DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_V1"
SCHEMA_V2 = "DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_V2"
SCHEMA_V3 = "DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_V3"
_types = H._types
LOCATION_CLOSE_SECONDS = 6
FINAL_MARGIN_SECONDS = 5
LOCATION_LIMITS = {
    "service_ms": (1000, 3600000), "operation_ms": (1, 60000),
    "query_events": (1, 4096), "provider_limit": (1, 64),
    "advertised_keys": (1, 4096), "provider_ttl_ms": (3000, 172800000),
    "reprovide_interval_ms": (500, 3600000), "maintenance_ms": (1000, 3600000),
    "commands": (1, 8192), "descriptor_requests": (1, 8192),
    "descriptor_reply_bytes": (4096, 1024**3),
}
TRANSPORT_LIMITS = {"outbound_attempts": (1, 8192), "inbound_upgrades": (1, 8192),
                    "receive_bytes": (1024, 1024**3), "send_bytes": (1024, 1024**3)}
METADATA_LIMITS = {"entries": (32, 65536), "bytes": (65536, 128*1024**2),
                   "valueBytes": (1024, 65536), "providersPerKey": (1, 128),
                   "pages": (256, 65536)}


def _body_routes(rows):
    """Finite owner-selected addresses; no scan or authority from advertisements."""
    H._need(type(rows) is list and 1 <= len(rows) <= 8, "ADVERTISED_BODY_ROUTES")
    keys = set()
    for row in rows:
        H._fields(row, {"module_id", "relative_name", "universes", "body_hash"})
        ref = P.body_ref({"module_id": F.hexid(row["module_id"]),
            "export_id": C.export_id(row["module_id"], row["relative_name"]),
            "universes": row["universes"], "body_hash": row["body_hash"]})
        key = P.body_route_key("00"*32, ref)
        H._need(key not in keys, "ADVERTISED_BODY_DUPLICATE_ROUTE")
        keys.add(key)
    return deepcopy(rows)


def _body_readback(workspace, routes, deadline):
    """Read each committed body once before any service starts, under owner lock."""
    routes = _body_routes(routes)
    H._need(type(deadline) in (int, float) and math.isfinite(deadline),
            "ADVERTISED_BODY_DEADLINE")
    H._need(not workspace._closed and workspace._lock is not None,
            "ADVERTISED_BODY_WORKSPACE_LOCK")
    store = workspace.modules
    domain = {"foundation": F.hexid(store.foundation), "policy": F.hexid(store.policy)}
    namespace = P.body_namespace(domain)
    H._need(store.codec is C and workspace.adapter.codec is C
            and (workspace.adapter.foundation, workspace.adapter.policy)
                == (domain["foundation"], domain["policy"])
            and all(profile["foundation"] == domain["foundation"]
                    and profile["policy"] == domain["policy"]
                    for profile in (workspace.config["wire_profile"], workspace.packets.profile)),
            "ADVERTISED_BODY_DOMAIN_BINDING")
    refs, keys = [], set()
    for row in routes:
        H._need(time.monotonic() < deadline, "ADVERTISED_BODY_READBACK_DEADLINE")
        # Existing get_body checks the held declaration, permissions, canonical
        # stored expression and exact body hash. No descriptor-only shortcut.
        body = store.get_body(row["module_id"], row["relative_name"],
                              row["universes"], row["body_hash"])
        ref = P.body_ref({"module_id": body["module_id"],
            "export_id": C.export_id(body["module_id"], body["relative_name"]),
            "universes": body["universes"], "body_hash": body["body_hash"]})
        del body  # No decoded expression accumulates across selected rows.
        key = P.body_route_key(namespace, ref)
        H._need(key not in keys, "ADVERTISED_BODY_DUPLICATE_ROUTE")
        keys.add(key); refs.append(ref)
        H._need(time.monotonic() < deadline, "ADVERTISED_BODY_READBACK_DEADLINE")
    return {"domain": domain, "namespace": namespace, "refs": refs,
        "observations": {"bodies_read": len(refs),
            "encoded_input_ceiling_bytes": len(refs)*2*16*H.MIB,
            "input_bound_scope": "GROUP_AND_EXPRESSION_INPUT_CEILING_NOT_RAM_OR_MEASURED_BYTES",
            "assurance": "READ_BACK_BEFORE_SERVICE_NOT_CONTINUOUS_AVAILABILITY_PROOF",
            "remote_placement_confirmed": False, "mathematical_acceptance": False}}


def _parameters(context):
    params = deepcopy(dict(context.parameters))
    selected = params.get("schema")
    H._need(selected in (SCHEMA, SCHEMA_V2, SCHEMA_V3), "ADVERTISED_SERVICE_SCHEMA")
    fields = {"schema", "mode", "workspace_path", "workspace_config",
              "bind", "tls", "service_limits", "location"}
    extra = {"index_view", "body_routes"} if selected == SCHEMA_V3 else (
        {"index_view"} if selected == SCHEMA_V2 else set())
    H._fields(params, fields | extra)
    projected = selected == SCHEMA_V2 or (selected == SCHEMA_V3 and params["index_view"] is not None)
    http = {name: value for name, value in params.items() if name not in ("location", "body_routes")}
    if not projected:
        http.pop("index_view", None)
    http["schema"] = H.SCHEMA_V2 if projected else H.SCHEMA
    proxy = SimpleNamespace(parameters=http, **{name: getattr(context, name) for name in
        ("deadline", "run", "location_workspace", "installation", "sources_v5",
         "sources_portable", "sources_owner")})
    validated_http, path, outputs, tls, http_reserve = H._parameters(proxy)
    if projected:
        params["index_view"] = validated_http["index_view"]
    body_count = 0
    if selected == SCHEMA_V3:
        params["body_routes"] = _body_routes(params["body_routes"])
        body_count = len(params["body_routes"])
    location = params["location"]
    H._fields(location, {"installation_root", "egress", "listen", "announce",
                         "bootstrap", "limits", "routes", "health_interval_ms"})
    policy = P.OwnerEgressPolicy(location["egress"])
    H._need(type(params["bind"]["host"]) is str
            and ipaddress.ip_address(params["bind"]["host"]).version == 4
            and params["bind"]["port"] != 0, "ADVERTISED_SERVICE_EXPLICIT_IPV4_ENDPOINT")
    policy.endpoint({**params["bind"], "tls": tls is not None, "server_name": None})
    listen, announce, bootstrap = (location[name] for name in ("listen", "announce", "bootstrap"))
    H._need(type(listen) is list and len(listen) == 1
            and type(announce) is list and len(announce) <= 4
            and type(bootstrap) is list and len(bootstrap) <= 16,
            "ADVERTISED_SERVICE_PEER_LISTS")
    value = listen[0]
    match = re.fullmatch(r"/ip4/([0-9.]+)/tcp/([1-9][0-9]{0,4})", value) if type(value) is str else None
    H._need(match is not None, "ADVERTISED_SERVICE_LISTEN")
    host, port = match.groups()
    H._need(str(ipaddress.IPv4Address(host)) == host, "ADVERTISED_SERVICE_LISTEN")
    F.uint(int(port), 1, 65535, "ADVERTISED_SERVICE_LISTEN")
    if host == "0.0.0.0" and location["egress"]["mode"] == "public-ipv4":
        H._need(int(port) in location["egress"]["public_ports"], "ADVERTISED_SERVICE_LISTEN_PORT")
    else:
        policy.peer_address(value)
    for value in announce:
        policy.peer_address(value)
    for value in bootstrap:
        policy.peer_address(value)
        H._need("/p2p/" in value, "ADVERTISED_SERVICE_BOOTSTRAP_ID")
    H._need(location["egress"]["mode"] != "public-ipv4" or announce,
            "ADVERTISED_SERVICE_PUBLIC_ANNOUNCE")
    limits = location["limits"]
    H._fields(limits, {*LOCATION_LIMITS, "transport", "metadata"})
    for name, bounds in LOCATION_LIMITS.items():
        F.uint(limits[name], *bounds, "ADVERTISED_SERVICE_LIMIT:"+name)
    H._need(limits["operation_ms"] <= limits["service_ms"]
            and limits["reprovide_interval_ms"]*3 <= limits["provider_ttl_ms"],
            "ADVERTISED_SERVICE_LIMIT_RELATIONS")
    H._fields(limits["transport"], TRANSPORT_LIMITS)
    for name, bounds in TRANSPORT_LIMITS.items():
        F.uint(limits["transport"][name], *bounds, "ADVERTISED_SERVICE_TRANSPORT:"+name)
    metadata = limits["metadata"]
    H._need(type(metadata) is dict and set(metadata) <= set(METADATA_LIMITS),
            "ADVERTISED_SERVICE_METADATA_FIELDS")
    for name, value in metadata.items():
        F.uint(value, *METADATA_LIMITS[name], "ADVERTISED_SERVICE_METADATA:"+name)
    interval = F.uint(location["health_interval_ms"], 100, 3600000,
                      "ADVERTISED_SERVICE_HEALTH_INTERVAL")/1000
    routes = location["routes"]
    H._need(type(routes) is list and (0 if selected == SCHEMA_V3 else 1) <= len(routes) <= 32,
            "ADVERTISED_SERVICE_ROUTES")
    keys = set()
    for route in routes:
        H._fields(route, {"features", "stripe"})
        key = P.route_key("00"*32, route["features"], route["stripe"])
        H._need(key not in keys, "ADVERTISED_SERVICE_DUPLICATE_ROUTE")
        keys.add(key)
    # Reserve all health requests plus publish and stop in the original channel.
    # Extras cover the immediate post-publication and pre-stop health checks.
    health_cap = math.ceil(params["service_limits"]["lifetime_seconds"]/interval)+2
    command_cap = len(routes)+body_count+health_cap+1
    H._need(len(routes)+body_count <= limits["advertised_keys"]
            and command_cap <= min(limits["commands"], 60),
            "ADVERTISED_SERVICE_COMMAND_RESERVATION")
    reserve = (http_reserve + 2*limits["operation_ms"]/1000
               + LOCATION_CLOSE_SECONDS + FINAL_MARGIN_SECONDS)
    H._need(time.monotonic() < context.deadline-reserve,
            "ADVERTISED_SERVICE_NO_CLEANUP_MARGIN")
    H._need(type(location["installation_root"]) is str, "ADVERTISED_SERVICE_RUNTIME_PATH")
    installation = B.ordinary(location["installation_root"], directory=True)
    for mutable in (path, B.ordinary(context.run, directory=True)):
        H._need(B.disjoint(installation, mutable), "ADVERTISED_SERVICE_RUNTIME_OVERLAP")
    # The explicit owner selects a retained installation, never a new manifest
    # authority or arbitrary executable. Full exact-role verification is in start.
    H._need(B.pin(installation/"RELEASE-MANIFEST.json", 8*H.MIB)["sha256"] == B.MANIFEST_SHA,
            "ADVERTISED_SERVICE_RUNTIME_MANIFEST")
    B.ordinary(installation/"runtime/node/node.exe")
    selected = context.source_sha256
    source_pins = {name: selected["portable/location/"+name] for name in SOURCE_NAMES}
    role_pins = {name: selected["portable/location/"+name] for name in ROLE_NAMES}
    for digest in (*source_pins.values(), *role_pins.values()):
        F.hexid(digest)
    adoption = AdoptedLocationRuntime(context.sources_portable/"location", source_pins,
        installation_root=installation, workspace_root=context.location_workspace)
    state = B.fresh_workspace_path(adoption.workspace, adoption.workspace/"location-state")
    channel = B.fresh_workspace_path(adoption.workspace, adoption.workspace/"location-channel")
    return (params, path, outputs, tls, reserve, http_reserve, policy, adoption,
            role_pins, state, channel, health_cap)


def _live_status(value, namespace):
    H._need(type(value) is dict and value.get("status") == "RUNNING"
            and value.get("namespace") == namespace and value.get("role") == "index-provider"
            and value.get("mathematical_acceptance") is False
            and value.get("global_complete") is False, "ADVERTISED_SERVICE_LOCATION_NOT_LIVE")


def _hint(value, key):
    H._need(type(value) is dict and value.get("route_key") == key
            and value.get("status") == "HINT_DISPATCHED_UNACKNOWLEDGED"
            and value.get("error") is None
            and value.get("remote_placement_confirmed") is False
            and value.get("global_complete") is False
            and value.get("mathematical_acceptance") is False,
            "ADVERTISED_SERVICE_DISPATCH_INCOMPLETE")
    census = value.get("census")
    H._need(type(census) is dict and type(census.get("add_provider_write")) is int
            and census["add_provider_write"] > 0, "ADVERTISED_SERVICE_NO_DISPATCH_WRITE")


def _http_live(provider):
    H._need(provider.server is not None and provider.server.is_serving(),
            "ADVERTISED_SERVICE_HTTP_NOT_LIVE")


async def _health(node, provider, namespace, deadline, health_cap, report):
    H._need(not node.closed and not node.channel_failed
            and node.process is not None and node.process.returncode is None,
            "ADVERTISED_SERVICE_LOCATION_EARLY_EXIT")
    _http_live(provider)
    H._need(report["health_checks"] < health_cap, "ADVERTISED_SERVICE_HEALTH_CAP")
    report["health_checks"] += 1
    until = min(deadline, time.monotonic()+report["location_limits"]["operation_ms"]/1000)
    value = await node.command("status", {}, until=until)
    report["location_status"] = value
    _live_status(value, namespace)
    _http_live(provider)


async def _monitor(node, provider, namespace, deadline, interval, health_cap, report):
    """Bounded IPC health plus immediate process death; no network retry."""
    waiter = asyncio.create_task(node.process.wait())
    try:
        while time.monotonic() < deadline:
            H._need(not node.closed and not node.channel_failed and not waiter.done(),
                    "ADVERTISED_SERVICE_LOCATION_EARLY_EXIT")
            remaining = deadline-time.monotonic()
            done, _ = await asyncio.wait({waiter}, timeout=min(interval, remaining))
            H._need(not done, "ADVERTISED_SERVICE_LOCATION_EARLY_EXIT")
            if time.monotonic() < deadline:
                await _health(node, provider, namespace, deadline, health_cap, report)
        H._need(not node.closed and not node.channel_failed and not waiter.done()
                and node.process.returncode is None, "ADVERTISED_SERVICE_LOCATION_EARLY_EXIT")
        _http_live(provider)
    finally:
        if not waiter.done():
            waiter.cancel()
        await asyncio.gather(waiter, return_exceptions=True)


async def _close_http(provider, context, cleanup, report):
    if provider is None:
        cleanup["http_closed"] = True
        return
    errors = cleanup["errors"]
    try:
        remaining = min(5, context.deadline-time.monotonic())
        H._need(remaining > 0, "ADVERTISED_SERVICE_HTTP_CLEANUP_DEADLINE")
        async with asyncio.timeout(remaining):
            await provider.stop()
        cleanup["http_closed"] = (provider.server is None and not provider.tasks
                                   and provider.reserved_reply_bytes == 0)
        H._need(cleanup["http_closed"], "ADVERTISED_SERVICE_HTTP_CLEANUP_UNCERTAIN")
    except BaseException as error:
        errors.append({"component": "http", **H._error(error)})
        if provider.server is not None:
            try:
                provider.server.close()
            except BaseException as tail:
                errors.append({"component": "http_listener", **H._error(tail)})
        tasks = tuple(provider.tasks)
        for task in tasks:
            task.cancel()
        remaining = min(1, context.deadline-time.monotonic())
        if tasks and remaining > 0:
            try:
                async with asyncio.timeout(remaining):
                    await asyncio.gather(*tasks, return_exceptions=True)
            except BaseException as tail:
                errors.append({"component": "http_handlers", **H._error(tail)})
    try:
        report["counters"] = provider.status()
    except BaseException as error:
        errors.append({"component": "http_status", **H._error(error)})


async def serve(context):
    (params, path, (ready_path, result_path), tls, reserve, http_reserve, policy,
     adoption, role_pins, state, evidence, health_cap) = _parameters(context)
    Workspace, Provider = _types(params["mode"])
    location = params["location"]
    started = time.monotonic()
    stop_seconds = location["limits"]["operation_ms"]/1000
    deadline = min(started+params["service_limits"]["lifetime_seconds"],
                   started+location["limits"]["service_ms"]/1000-2*stop_seconds,
                   context.deadline-reserve)
    final_health_deadline = deadline+stop_seconds
    stop_deadline = final_health_deadline+stop_seconds
    H._need(time.monotonic() < deadline, "ADVERTISED_SERVICE_ACTIVE_INTERVAL")
    workspace = provider = node = view = None
    cancelled = None
    cleanup = {"location_closed": False, "http_closed": False,
               "workspace_closed": False, "errors": []}
    report = {"schema": "DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_RESULT_V1", "status": "FAILED",
        "error": None, "cleanup": cleanup, "endpoint": None, "namespace": None,
        "wire_profile": None, "counters": None, "location_ready": None,
        "route_dispatch": [], "location_status": None, "location_report": None,
        "health_checks": 0, "health_cap": health_cap,
        "health_interval_ms": location["health_interval_ms"],
        "health_detection_scope": "BOUNDED_STATUS_OBSERVATIONS_NOT_CONTINUOUS_READINESS",
        "health_detection_delay_bound_seconds": location["health_interval_ms"]/1000+stop_seconds,
        "health_bound_assumptions": "DELAY_BOUND_REQUIRES_TIMELY_EVENT_LOOP_OTHERWISE_ONLY_ORIGINAL_OUTER_JOB_CEILING",
        "location_installation": str(adoption.installation), "started": started,
        "deadline": deadline, "final_health_deadline": final_health_deadline,
        "stop_deadline": stop_deadline,
        "outer_deadline": context.deadline, "cleanup_reserve_seconds": reserve,
        "mode": params["mode"], "workspace_path": str(path),
        "service_limits": params["service_limits"], "location_limits": location["limits"],
        "authority": "OPERATIONAL_SERVICE_DATA_NOT_MATHEMATICAL_AUTHORITY",
        "advertisement_assurance": "HINT_DISPATCHED_UNACKNOWLEDGED_NOT_REMOTE_PLACEMENT",
        "expiry_assurance": "LOCAL_RENEWAL_STOPS_REMOTE_HINT_RETENTION_IS_RECEIVER_POLICY",
        "global_complete": False, "mathematical_acceptance": False}
    body_enabled = params["schema"] == SCHEMA_V3
    projected = params["schema"] == SCHEMA_V2 or (body_enabled and params["index_view"] is not None)
    if projected:
        report.update(schema="DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_RESULT_V2",
                      index_view=None, source_namespace=None, coverage=H.COVERAGE)
        cleanup["projection_closed"] = False
    if body_enabled:
        report.update(schema="DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_RESULT_V3",
                      body_readback=None, body_route_dispatch=[],
                      remote_placement_confirmed=False)
    try:
        workspace = Workspace.open(path, params["workspace_config"], create=False)
        index, view = H._selected_index(workspace, {**params,
            "schema": H.SCHEMA_V2 if projected else H.SCHEMA})
        if projected:
            report["index_view"] = view.descriptor()
            report["source_namespace"] = workspace.index.namespace
        if body_enabled:
            report["body_readback"] = _body_readback(workspace, params["body_routes"], deadline)
        H._need(time.monotonic() < deadline, "ADVERTISED_SERVICE_STARTUP_DEADLINE")
        provider = Provider(index=index, custody=workspace.modules,
            packets=workspace.packets, **{name: params["service_limits"][name] for name in H.LIMITS})
        namespace = report["namespace"] = F.hexid(index.namespace)
        report["wire_profile"] = workspace.packets.profile_id
        async with asyncio.timeout_at(deadline):
            endpoint = await provider.start(**params["bind"], tls_context=tls)
        actual = {name: getattr(endpoint, name) for name in ("host", "port", "tls", "server_name")}
        policy.endpoint(actual)
        H._need(actual == {**params["bind"], "tls": tls is not None, "server_name": None},
                "ADVERTISED_SERVICE_HTTP_ENDPOINT_CHANGED")
        report["endpoint"] = actual
        limits = deepcopy(location["limits"])
        H._need(time.monotonic() < deadline, "ADVERTISED_SERVICE_STARTUP_DEADLINE")
        # The retained child schema has a one-second minimum. The parent still
        # enforces the earlier absolute stop cutoff, including for short roles.
        limits["service_ms"] = min(limits["service_ms"], max(1000, limits["operation_ms"],
            math.ceil((stop_deadline-time.monotonic())*1000)))
        config = {"schema": "DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", "role": "index-provider",
            "state": str(state), "namespace": namespace, "egress": location["egress"],
            "listen": location["listen"], "announce": location["announce"],
            "bootstrap": location["bootstrap"], "endpoints": [actual], "limits": limits}
        if body_enabled:
            config.update(schema="DMKN_V5_MAINTAINED_LOCATION_ROLES_V2",
                          body_domain=report["body_readback"]["domain"])
        report["effective_location_limits"] = limits
        node = ServiceLocationProcess(adoption, role_pins, config, evidence, deadline=stop_deadline)
        async with asyncio.timeout_at(deadline):
            report["location_ready"] = await node.start()
        _live_status(report["location_ready"], namespace)
        for route in location["routes"]:
            value = await node.command("publish", route,
                                       until=min(deadline, time.monotonic()+stop_seconds))
            report["route_dispatch"].append(value)
            _hint(value, P.route_key(namespace, route["features"], route["stripe"]))
        if body_enabled:
            for ref in report["body_readback"]["refs"]:
                value = await node.command("publish-body", {"body": ref},
                                           until=min(deadline, time.monotonic()+stop_seconds))
                report["body_route_dispatch"].append(value)
                _hint(value, P.body_route_key(report["body_readback"]["namespace"], ref))
        H._need(time.monotonic() < deadline and not node.closed and not node.channel_failed
                and node.process is not None and node.process.returncode is None,
                "ADVERTISED_SERVICE_READY_DEADLINE_OR_CHILD")
        await _health(node, provider, namespace, deadline, health_cap, report)
        ready = {"schema": "DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_READY_V1",
            "endpoint": actual, "namespace": namespace, "wire_profile": report["wire_profile"],
            "deadline": deadline, "outer_deadline": context.deadline, "mode": params["mode"],
            "route_dispatch": report["route_dispatch"], "location_ready": report["location_ready"],
            "location_status": report["location_status"],
            "health_interval_ms": report["health_interval_ms"],
            "health_detection_scope": report["health_detection_scope"],
            "authority": report["authority"], "advertisement_assurance": report["advertisement_assurance"],
            "global_complete": False, "mathematical_acceptance": False}
        if projected:
            ready.update(schema="DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_READY_V2",
                         index_view=report["index_view"], source_namespace=report["source_namespace"],
                         coverage=H.COVERAGE)
        if body_enabled:
            ready.update(schema="DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_READY_V3",
                         body_readback=report["body_readback"],
                         body_route_dispatch=report["body_route_dispatch"],
                         remote_placement_confirmed=False)
        H._save(ready_path, ready)
        await _monitor(node, provider, namespace, deadline, location["health_interval_ms"]/1000,
                       health_cap, report)
        # A locator can stop internally while Node still waits for IPC. The
        # final reserved status observes that last interval before normal stop.
        await _health(node, provider, namespace, final_health_deadline, health_cap, report)
        if view is not None:
            view.assert_current()
        report["status"] = "PASS"
    except BaseException as error:
        report["error"] = H._error(error)
        if isinstance(error, asyncio.CancelledError):
            cancelled = error
    finally:
        errors = cleanup["errors"]
        if node is None:
            cleanup["location_closed"] = True
        else:
            try:
                if not node.closed and not node.channel_failed and node.process is not None \
                        and node.process.returncode is None:
                    until = min(stop_deadline, time.monotonic()+stop_seconds)
                    value = await node.command("stop", {}, until=until)
                    report["location_status"] = value
                    H._need(type(value) is dict and value.get("status") == "STOPPED"
                            and value.get("namespace") == report["namespace"]
                            and value.get("role") == "index-provider",
                            "ADVERTISED_SERVICE_STOP_UNCONFIRMED")
            except BaseException as error:
                errors.append({"component": "location_stop", **H._error(error)})
            try:
                # Reserve HTTP drain even if location teardown fails. The
                # retained controller owns process reap and its post-pin checks.
                remaining = context.deadline-http_reserve-time.monotonic()
                H._need(remaining > 0, "ADVERTISED_SERVICE_LOCATION_CLEANUP_DEADLINE")
                async with asyncio.timeout(remaining):
                    await node.close()
            except BaseException as error:
                errors.append({"component": "location_close", **H._error(error)})
            try:
                state_report = report["location_report"] = node.report()
                cleanup["location_closed"] = (state_report["closed"] is True
                    and state_report["returncode"] == 0
                    and state_report["channel_failed"] is False
                    and state_report["forced_termination"] is False)
                H._need(cleanup["location_closed"], "ADVERTISED_SERVICE_LOCATION_CLEANUP_UNCERTAIN")
            except BaseException as error:
                errors.append({"component": "location_report", **H._error(error)})
        await _close_http(provider, context, cleanup, report)
        if projected:
            H._close_projection(view, cleanup)
        if workspace is not None:
            cleanup["workspace_closed"] = H._close_workspace(workspace, errors)
        required_closes = ("location_closed", "http_closed", "workspace_closed") + (("projection_closed",) if projected else ())
        if errors or not all(cleanup[name] for name in required_closes):
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        if report["finished"] >= context.deadline:
            report["status"] = "FAILED"
            errors.append({"component": "deadline", "type": "DeadlineExceeded",
                           "message": "ADVERTISED_SERVICE_ORIGINAL_DEADLINE_EXHAUSTED"})
        H._save(result_path, report)
    if cancelled is not None:
        raise cancelled
    return report


def main(context):
    return 0 if asyncio.run(serve(context))["status"] == "PASS" else 1


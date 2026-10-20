"""One retained-packet, demand-directed semantic acquisition integration.

Provider seeding is untrusted data preparation, not acceptance. The fresh
receiver obtains only its discovered target opening initially; every further
opening/body comes from an actual helper demand and service response. This
trusted test caller selects singleton internal journals, not new proof policy.
"""
import asyncio
from copy import deepcopy
from dataclasses import replace
import json
import time
from types import MappingProxyType, SimpleNamespace

from client import remote_reader, serve_workspace
from client.direct_contacts import bind
from client.runtime import RuntimeProfile, read_pin
from client.semantic_reader import SemanticReader, READY
from client.workspace_mixed import CommonsClient as MixedClient
from client.workspace_validated import Workspace
from custody.module_store import BODY_SCHEMA, permitted_hashes
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from location.protocol import OwnerEgressPolicy
from modules import codec as C

MIB = 1024**2
SCHEMA = "DMKN_V5_SEMANTIC_CHECK_V1"


def _error(error):
    return {"type": type(error).__name__, "message": str(error)[:1000]}


def _save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     allow_nan=False).encode("utf-8")
    F.need(len(raw) <= 2*MIB, "SEMANTIC_CHECK_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def _seed(workspace, packet, name, image):
    # This namespace is only the two fields read by the existing pure extractor.
    # It is NOT a live client, fabricated verifier, warrant, or admitted context.
    extractor = SimpleNamespace(workspace=SimpleNamespace(_envelope=workspace._envelope),
                                _aggregate_image=image)
    summary, groups, values, census = MixedClient._semantic_plan(extractor, packet)
    F.need(census["claims"] == census["frontiers"] == 1
           and census["deltas"] == 2 and census["warrants"] == 3,
           "SEMANTIC_CHECK_RETAINED_PACKET_SHAPE")
    module = C.summary_id(summary)
    selected, bodies, missing = [], set(), []
    for (owner, unused_index), raw in sorted(groups.items()):
        opening = C.parse_json(raw)
        group = C.verify_group_opening(owner, opening)
        workspace.modules.put_group(owner, opening)
        for declaration in group["declarations"]:
            if owner == module and declaration["name"] == name:
                selected.append(opening)
            for digest in sorted(permitted_hashes(declaration)):
                arity = declaration["universes"]
                key = owner, arity, digest
                if key in bodies:
                    continue
                value = values.get((arity, digest))
                if value is None:
                    missing.append({"module": owner, "name": declaration["name"],
                                    "universes": arity, "body_hash": digest})
                    continue
                workspace.modules.put_body(owner, declaration["name"], {
                    "schema": BODY_SCHEMA, "module_id": owner,
                    "relative_name": declaration["name"], "universes": arity,
                    "body_hash": digest, "expression": C.parse_json(value)})
                bodies.add(key)
    F.need(len(selected) == 1, "SEMANTIC_CHECK_EXPORTED_DECLARATION")
    F.need(not missing and len(groups) == 13 and len(bodies) == 11,
           "SEMANTIC_CHECK_COMPLETE_PROVIDER_SEMANTICS")
    # Only this root packet is offered. No standalone evidence for its internal
    # members is synthesized, and only the target export is indexed.
    workspace.packets.put(module, packet)
    workspace.index.admit(workspace.adapter.encode_opening(module, name, selected[0]),
                          expected_id=C.export_id(module, name))
    return {"module": module, "groups": len(groups), "bodies": len(bodies),
            "missing_bodies": missing, "packet_census": census,
            "indexed_exports": 1, "offered_packets": 1,
            "mathematical_acceptance": False}


async def _discover(client, q, detail):
    choice, provider = q["selection"], q["selection"]["provider"]
    detail["binding"] = bind(client, q["contacts"], q["specs"],
        OwnerEgressPolicy(q["egress_policy"]), q["search_limits"],
        contact_lifetime_ms=q["contact_lifetime_ms"])
    offer = await client.search_offer(provider, **q["offer"])
    F.need(offer["status"] == "OFFERED", "SEMANTIC_CHECK_QUERY_OFFER")
    partitions = [row for row in offer["partitions"] if row["anchor_count"] > 0]
    F.need(choice["partition_index"] < len(partitions), "SEMANTIC_CHECK_PARTITION")
    partition = partitions[choice["partition_index"]]
    F.need(choice["start"] < partition["anchor_count"], "SEMANTIC_CHECK_PAGE_START")
    page = await client.search_page(provider, offer["snapshot_id"], partition["partition"],
        choice["start"], q["page"]["limits"], candidates_only=True,
        attempt_timeout_ms=q["page"]["attempt_timeout_ms"])
    F.need(page["status"] == "VERIFIED_CANDIDATES"
           and choice["candidate_index"] < len(page["matches"]), "SEMANTIC_CHECK_QUERY_MATCH")
    candidate = await client.resolve(provider, page["matches"][choice["candidate_index"]])
    description = client.describe_candidate(candidate)
    packets = await client.packet_offers(candidate, **q["packets"])
    F.need(len(packets["packets"]) == 1 and choice["packet_index"] == 0,
           "SEMANTIC_CHECK_SINGLETON_PACKET_POLICY")
    entry = packets["packets"][0]
    detail.update(snapshot_id=offer["snapshot_id"], partition=partition["partition"],
                  selection=choice, returned_candidates=len(page["matches"]),
                  locator=description["locator"], packet=entry)
    return candidate, entry


async def _read(context, params, helper_limits, max_rounds, semantic_max_bytes):
    q = remote_reader._query(params["query"])
    path, unused_output = remote_reader._paths(context, params)
    output = ordinary(context.location_workspace/"semantic-read-result.json",
                      fresh=True, directory=False)
    F.need(q["admission"]["memory_mib"] <= context.limits["memory_mib"],
           "SEMANTIC_CHECK_OUTER_MEMORY")
    F.need(time.monotonic() < context.deadline-5, "SEMANTIC_CHECK_CLEANUP_MARGIN")
    workspace = client = helper = None
    cancelled = None
    report = {"schema": "DMKN_V5_SEMANTIC_READ_RESULT_V1", "status": "FAILED",
        "error": None, "cleanup_errors": [], "client_closed": False,
        "workspace_closed": False, "discovery": {}, "rounds": [],
        "selected_internal_members": [], "result": None, "client": None,
        "global_complete": False, "mathematical_acceptance": False,
        "authority": "OPERATION_EVIDENCE_NOT_TRANSFERABLE_AUTHORITY"}
    try:
        runtime = RuntimeProfile.from_context(context, params["runtime_adoption"])
        foundation = read_pin(params["foundation"], 16*MIB)
        workspace = Workspace.open(path, params["workspace_config"], create=True)
        grant = workspace.reserve(params["operation_limits"], outer_deadline=context.deadline-5)
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=False,
            foundation_bytes=foundation, foundation_sha256=params["foundation"]["sha256"])
        report["operation_id"] = grant.identifier
        candidate, entry = await _discover(client, q, report["discovery"])
        helper = SemanticReader(client, candidate, limits=helper_limits)
        staged = await helper.stage(candidate, entry)
        report["staged"] = staged
        report["initial_helper"] = helper.report()
        F.need(report["initial_helper"]["groups"] == 1
               and report["initial_helper"]["bodies"] == 0
               and report["initial_helper"]["modules"] == 1,
               "SEMANTIC_CHECK_TARGET_OPENING_ONLY")
        inventory, root = staged["members"], staged["module"]
        F.need(len(inventory) == 3, "SEMANTIC_CHECK_PACKET_INVENTORY")
        # Each iteration acts only on the current actual preview. Processing
        # the whole bounded demand batch avoids rescanning after each response.
        for ordinal in range(max_rounds):
            preview = helper.preview()
            row = {"round": ordinal, "preview": preview, "actions": []}
            report["rounds"].append(row)
            if preview["status"] == READY:
                break
            progressed = False
            for demand in preview["demands"]:
                if demand["kind"] == "NeedModuleEvidence":
                    matches = [member for member in inventory
                               if member["module"] == demand["module"]]
                    F.need(len(matches) == 1, "SEMANTIC_CHECK_SINGLETON_MEMBER_POLICY")
                    chosen = helper.select_member(root, bytes(matches[0]["journal"]))
                    row["actions"].append({"kind": "select_member", **chosen})
                    if chosen["status"] == "SELECTED_MEMBER":
                        report["selected_internal_members"].append(chosen)
                        progressed = True
                resolved = await helper.resolve(demand, max_bytes=semantic_max_bytes)
                # Never serialize an opaque candidate as evidence or authority.
                row["actions"].append({"kind": "resolve", "demand": demand,
                    "status": resolved["status"],
                    "locator": resolved["description"]["locator"]})
                progressed |= resolved["status"] == "RESOLVED"
                if demand["kind"] == "NeedBody":
                    body = await helper.fetch_body(demand, max_bytes=semantic_max_bytes)
                    row["actions"].append({"kind": "fetch_body", **body})
                    progressed |= body["status"] == "FETCHED"
            F.need(progressed, "SEMANTIC_CHECK_NO_STRUCTURAL_PROGRESS")
        else:
            F.need(False, "SEMANTIC_CHECK_ROUND_LIMIT")
        report["before_admission"] = client.report()
        F.need(report["before_admission"]["counts"]["admission_submissions"] == 0
               and report["before_admission"]["counts"]["new_import_sessions"] == 0
               and all(report["before_admission"][key]["attempts"] == 0
                       for key in ("receipt", "aggregate", "mixed")),
               "SEMANTIC_CHECK_PREVIEW_NOT_AUTHORITY")
        structural = helper.report()
        F.need(structural["modules"] == 2 and structural["groups"] == 9
               and structural["bodies"] == 9 and preview["cost"]["declarations"] == 12,
               "SEMANTIC_CHECK_EXPECTED_SELECTED_CLOSURE")
        result = helper.finish({root: q["admission"]})
        after = client.report()
        F.need(all(after["acquisition"]["used"][key]
                   == report["before_admission"]["acquisition"]["used"][key]
                   for key in ("requests", "reply_bytes")),
               "SEMANTIC_CHECK_NO_POST_PREVIEW_NETWORK")
        report["result"] = {key: result[key] for key in
                            ("status", "demands", "cost", "mathematical_acceptance")}
        report["live_context_returned"] = result["context"] is not None
        report["helper"] = helper.report()
        F.need(result["status"] == "READY" and result["context"] is not None,
               "SEMANTIC_CHECK_ACTUAL_LIVE_READY")
        F.need(result["cost"]["groups"] == 9 and result["cost"]["declarations"] == 12,
               "SEMANTIC_CHECK_ACTUAL_SELECTED_CLOSURE")
        F.need(report["helper"]["packets"] == 1
               and report["helper"]["modules"] > 1
               and report["selected_internal_members"]
               and report["helper"]["bodies"] > 0,
               "SEMANTIC_CHECK_ACTUAL_INTERNAL_SEMANTICS")
        F.need(result["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
               "SEMANTIC_CHECK_NO_ANCESTRAL_PROOF_FRONTEND")
        report["status"] = "COMPLETED"
    except BaseException as error:
        report["error"] = _error(error)
        if isinstance(error, asyncio.CancelledError):
            cancelled = error
    finally:
        if helper is not None:
            if "helper" not in report:
                report["helper"] = helper.report()
            try:
                helper.close()
            except BaseException as error:
                report["cleanup_errors"].append({"component": "helper", **_error(error)})
        if client is not None:
            try:
                closed = await client.close()
                report["client"] = closed
                states = ("CLOSED",) if report["status"] == "COMPLETED" else ("CLOSED", "FAILED")
                F.need(closed["closed"] and closed["status"] in states
                       and all(closed[name] is None or closed[name]["closed"]
                               for name in ("receipt", "aggregate", "mixed"))
                       and closed["preparation"] is None, "SEMANTIC_CHECK_CLIENT_CLEANUP")
                report["client_closed"] = True
            except BaseException as error:
                report["cleanup_errors"].append({"component": "client", **_error(error)})
                if isinstance(error, asyncio.CancelledError):
                    cancelled = error
        if workspace is not None:
            report["workspace_closed"] = serve_workspace._close_workspace(
                workspace, report["cleanup_errors"])
        if report["cleanup_errors"] or not report["client_closed"] or not report["workspace_closed"]:
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        if report["finished"] >= context.deadline:
            report["status"] = "FAILED"
            report["cleanup_errors"].append({"component": "deadline",
                "type": "DeadlineExceeded", "message": "SEMANTIC_CHECK_ORIGINAL_DEADLINE"})
        _save(output, report)
    if cancelled is not None:
        raise cancelled
    return report


async def run(context):
    params = deepcopy(dict(context.parameters))
    F.fields(params, {"schema", "packet", "reader", "service_limits", "export_name",
                      "helper_limits", "max_rounds", "semantic_max_bytes"})
    F.need(params["schema"] == SCHEMA, "SEMANTIC_CHECK_SCHEMA")
    F.uint(params["max_rounds"], 1, 128, "SEMANTIC_CHECK_MAX_ROUNDS")
    F.uint(params["semantic_max_bytes"], 1, 16*MIB, "SEMANTIC_CHECK_RESPONSE_BYTES")
    reader = deepcopy(params["reader"])
    F.fields(reader, {"schema", "runtime_adoption", "workspace_path", "workspace_config",
                      "create_workspace", "operation_limits", "foundation", "query"})
    F.need(reader["schema"] == remote_reader.SCHEMA, "SEMANTIC_CHECK_READER_SCHEMA")
    config = reader["workspace_config"]
    image = config["wire_profile"]["aggregate_image"]
    packet = read_pin(params["packet"], 16*MIB)
    name = params["export_name"]
    C.validate_name(name)
    provider_path = ordinary(context.workspace_root/(context.run.name+"-custody"), fresh=True)
    reader_path = ordinary(context.workspace_root/(context.run.name+"-reader"), fresh=True)
    for value in (context.installation, context.run, context.sources_v5,
                  context.sources_portable, context.sources_owner):
        root = ordinary(value)
        for target in (provider_path, reader_path):
            F.need(not target.is_relative_to(root) and not root.is_relative_to(target),
                   "SEMANTIC_CHECK_FRESH_WORKSPACE_DISJOINT")
    service_output = context.location_workspace/"service"
    reader_output = context.location_workspace/"reader"
    service_output.mkdir()
    reader_output.mkdir()
    workspace = task = None
    report = {"schema": "DMKN_V5_SEMANTIC_CHECK_RESULT_V1", "status": "FAILED",
        "error": None, "cleanup_errors": [], "reader": None, "service": None,
        "scope": "ACTUAL_DEMAND_DIRECTED_HTTP_SEMANTICS_AND_LIVE_I_NATIVE_IMPORT",
        "authority": "OPERATION_EVIDENCE_NOT_TRANSFERABLE_AUTHORITY",
        "new_proof_calls": 0, "authoring_calls": 0, "public_network_calls": 0}
    try:
        workspace = Workspace.open(provider_path, config, create=True)
        seed = _seed(workspace, packet, name, image)
        report["provider_seed"] = seed
        workspace.close()
        workspace = None
        service_params = {"schema": serve_workspace.SCHEMA, "mode": "validated",
            "workspace_path": str(provider_path), "workspace_config": config,
            "bind": {"host": "127.0.0.1", "port": 0}, "tls": None,
            "service_limits": params["service_limits"]}
        service_context = replace(context, location_workspace=service_output,
                                  parameters=MappingProxyType(service_params))
        task = asyncio.create_task(serve_workspace.serve(service_context))
        ready_path = service_output/"service-ready.json"
        while not ready_path.exists():
            context.remaining_seconds()
            F.need(not task.done(), "SEMANTIC_CHECK_SERVICE_FAILED_BEFORE_READY")
            await asyncio.sleep(0.02)
        raw = ready_path.read_bytes()
        F.need(len(raw) <= MIB, "SEMANTIC_CHECK_READY_BOUND")
        endpoint = json.loads(raw)["endpoint"]
        F.need(endpoint["host"] == "127.0.0.1" and not endpoint["tls"],
               "SEMANTIC_CHECK_LOOPBACK_ONLY")
        reader.update(workspace_path=str(reader_path), create_workspace=True)
        label = reader["query"]["selection"]["provider"]
        reader["query"]["contacts"] = {label: endpoint}
        reader["query"]["egress_policy"] = {"schema": "DMKN_V5_OWNER_EGRESS_V1",
            "mode": "loopback-test", "public_ports": [],
            "test_endpoints": [{"host": endpoint["host"], "port": endpoint["port"]}]}
        reader_context = replace(context, location_workspace=reader_output,
                                 parameters=MappingProxyType(reader))
        outcome = await _read(reader_context, reader, params["helper_limits"],
                              params["max_rounds"], params["semantic_max_bytes"])
        report["reader"] = outcome
        F.need(outcome["status"] == "COMPLETED"
               and outcome["discovery"]["locator"]["module_id"] == seed["module"]
               and outcome["discovery"]["locator"]["relative_name"] == name,
               "SEMANTIC_CHECK_RETURNED_TARGET_READY")
        actual = outcome["client"]
        F.need(actual["receipt"]["attempts"] == actual["mixed"]["attempts"] == 1
               and actual["aggregate"]["attempts"] == 0
               and actual["mixed"]["reserved_worker_cpu"]
                   == 2*reader["query"]["admission"]["native_cpu_seconds"]
                      +reader["query"]["admission"]["receipt_cpu_seconds"]
               and actual["counts"]["admission_submissions"] == 1
               and actual["counts"]["new_import_sessions"] == 1
               and actual["counts"]["author_calls"] == actual["counts"]["publication_attempts"] == 0
               and actual["preparation"] is None and actual["location"] is None,
               "SEMANTIC_CHECK_ONE_REAL_MIXED_ADMISSION")
        report["service"] = await task
        F.need(report["service"]["status"] == "PASS", "SEMANTIC_CHECK_SERVICE_CLOSURE")
        report.update(status="PASS", packet_pin=params["packet"], target_module=seed["module"])
    except BaseException as error:
        report["error"] = _error(error)
        raise
    finally:
        if task is not None and not task.done():
            task.cancel()
        if task is not None:
            try:
                report["service"] = await task
            except asyncio.CancelledError:
                report["cleanup_errors"].append({"component": "service",
                    "type": "CancelledError", "message": "cancelled_after_integration_failure"})
            except BaseException as error:
                report["cleanup_errors"].append({"component": "service", **_error(error)})
        if workspace is not None:
            if not serve_workspace._close_workspace(workspace, report["cleanup_errors"]):
                report["cleanup_errors"].append({"component": "seed_workspace",
                    "type": "CleanupFailure", "message": "workspace_not_closed"})
        if report["cleanup_errors"]:
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        if report["finished"] >= context.deadline:
            report["status"] = "FAILED"
        _save(context.location_workspace/"semantic-check-result.json", report)
    return 0 if report["status"] == "PASS" else 1


def main(context):
    return asyncio.run(run(context))

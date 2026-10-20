"""Retained mathematics across two genuinely split semantic service stores.

P retains the exact packet and index but has no selected body row; Q alone
serves that row. This proves public-service inventory separation, not absence
of reconstructable information from P's retained packet. No new proof runs.
"""
import asyncio
from copy import deepcopy
from dataclasses import replace
import json
import time
from types import MappingProxyType, SimpleNamespace

from client import remote_reader, serve_workspace
from client.semantic_check import _error, _save, _discover
from client.runtime import RuntimeProfile, read_pin
from client.semantic_reader import SemanticReader, READY
from client.workspace_mixed import CommonsClient as MixedClient
from client.workspace_validated import Workspace
from custody.module_store import BODY_SCHEMA, permitted_hashes
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from modules import codec as C

MIB = 1024**2
SCHEMA = "DMKN_V5_SPLIT_CUSTODY_CHECK_V1"
Q = "semantic-supplier"
SPLIT = {"module": "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e",
         "name": [["s", "CommonsV5"], ["s", "fold"]], "universes": 2,
         "body_hash": "0b5f265dfb01a1ed1232443bfdc79c5217be78664b15ee9d12e01fa77d2e6e55"}


def _supplier(demand):
    return Q if demand["module"] == SPLIT["module"] and demand["name"] == SPLIT["name"] else None


def _split_inventory(p, q):
    key = SPLIT["module"], SPLIT["universes"], SPLIT["body_hash"]
    missing = p.modules.db.execute(
        "SELECT 1 FROM bodies WHERE module=? AND universes=? AND hash=?", key).fetchone() is None
    F.need(missing, "SPLIT_P_BODY_MUST_BE_ABSENT")
    held = q.modules.get_body(SPLIT["module"], SPLIT["name"], SPLIT["universes"], SPLIT["body_hash"])
    F.need(C.body_id(held["expression"], held["universes"]) == SPLIT["body_hash"],
           "SPLIT_Q_EXACT_BODY")
    p_counts, q_counts = p.modules.status()["counts"], q.modules.status()["counts"]
    F.need(p_counts["groups"] == 13 and p_counts["bodies"] == 10
           and q_counts["groups"] == q_counts["bodies"] == 1
           and p.index.status()["objects"] == 1 and q.index.status()["objects"] == 0
           and p.packets.status()["counts"]["packets"] == 1
           and q.packets.status()["counts"]["packets"] == 0, "SPLIT_EXACT_STORE_CENSUS")
    return {"address": deepcopy(SPLIT), "p_body_row_absent": missing,
            "q_body_exact_readback": True, "mathematical_acceptance": False,
            "p_counts": p_counts, "q_counts": q_counts,
            "scope": "PUBLIC_SEMANTIC_STORE_NOT_INFORMATION_THEORETIC_PACKET_ABSENCE"}


def _seed_split(p, q, packet, name, image):
    extractor = SimpleNamespace(workspace=SimpleNamespace(_envelope=p._envelope),
                                _aggregate_image=image)
    summary, groups, values, census = MixedClient._semantic_plan(extractor, packet)
    F.need(census["claims"] == census["frontiers"] == 1 and census["deltas"] == 2
           and census["warrants"] == 3, "SPLIT_RETAINED_PACKET_SHAPE")
    module = C.summary_id(summary)
    selected, bodies, q_groups = [], set(), set()
    split_key = SPLIT["module"], SPLIT["universes"], SPLIT["body_hash"]
    withheld = []
    for (owner, unused_index), raw in sorted(groups.items()):
        opening = C.parse_json(raw)
        group = C.verify_group_opening(owner, opening)
        p.modules.put_group(owner, opening)
        for declaration in group["declarations"]:
            if owner == module and declaration["name"] == name:
                selected.append(opening)
            for digest in sorted(permitted_hashes(declaration)):
                arity = declaration["universes"]
                key = owner, arity, digest
                if key in bodies:
                    continue
                value = values.get((arity, digest))
                F.need(value is not None, "SPLIT_NO_UNINTENDED_MISSING_SEMANTICS")
                response = {"schema": BODY_SCHEMA, "module_id": owner,
                    "relative_name": declaration["name"], "universes": arity,
                    "body_hash": digest, "expression": C.parse_json(value)}
                if key == split_key:
                    F.need(declaration["name"] == SPLIT["name"], "SPLIT_EXACT_SELECTED_NAME")
                    q.modules.put_group(owner, opening)
                    q.modules.put_body(owner, declaration["name"], response)
                    q_groups.add((owner, opening["index"]))
                    withheld.append(deepcopy(SPLIT))
                else:
                    p.modules.put_body(owner, declaration["name"], response)
                bodies.add(key)
    F.need(len(selected) == 1 and len(groups) == 13 and len(bodies) == 11
           and withheld == [SPLIT] and len(q_groups) == 1, "SPLIT_EXPECTED_SERVICE_INVENTORIES")
    p.packets.put(module, packet)
    p.index.admit(p.adapter.encode_opening(module, name, selected[0]),
                  expected_id=C.export_id(module, name))
    inventory = _split_inventory(p, q)
    return {"module": module, "p": {"groups": 13, "bodies": 10,
            "indexed_exports": 1, "offered_packets": 1},
            "q": {"groups": 1, "bodies": 1, "indexed_exports": 0, "offered_packets": 0},
            "inventory": inventory, "packet_census": census, "mathematical_acceptance": False}


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
                resolved = await helper.resolve(demand, max_bytes=semantic_max_bytes,
                                                supplier=_supplier(demand))
                # Never serialize an opaque candidate as evidence or authority.
                row["actions"].append({"kind": "resolve", "demand": demand,
                    "status": resolved["status"], "supplier": resolved["description"]["provider"],
                    "locator": resolved["description"]["locator"]})
                progressed |= resolved["status"] == "RESOLVED"
                if demand["kind"] == "NeedBody":
                    body = await helper.fetch_body(demand, max_bytes=semantic_max_bytes,
                                                   supplier=_supplier(demand))
                    row["actions"].append({"kind": "fetch_body", "demand": demand,
                                           "supplier": _supplier(demand), **body})
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
    F.need(params["schema"] == SCHEMA, "SPLIT_CHECK_SCHEMA")
    F.uint(params["max_rounds"], 1, 128, "SPLIT_CHECK_MAX_ROUNDS")
    F.uint(params["semantic_max_bytes"], 1, 16*MIB, "SPLIT_CHECK_RESPONSE_BYTES")
    reader = deepcopy(params["reader"])
    F.fields(reader, {"schema", "runtime_adoption", "workspace_path", "workspace_config",
                      "create_workspace", "operation_limits", "foundation", "query"})
    F.need(reader["schema"] == remote_reader.SCHEMA, "SPLIT_CHECK_READER_SCHEMA")
    config = reader["workspace_config"]
    image = config["wire_profile"]["aggregate_image"]
    packet = read_pin(params["packet"], 16*MIB)
    name = params["export_name"]
    C.validate_name(name)
    p_label = reader["query"]["selection"]["provider"]
    F.need(p_label != Q and reader["query"]["search_limits"]["providers"] >= 2,
           "SPLIT_TWO_EXPLICIT_CONTACTS")
    paths = {role: ordinary(context.workspace_root/(context.run.name+"-"+role), fresh=True)
             for role in ("custody-p", "custody-q", "reader")}
    for value in (context.installation, context.run, context.sources_v5,
                  context.sources_portable, context.sources_owner):
        root = ordinary(value)
        for target in paths.values():
            F.need(not target.is_relative_to(root) and not root.is_relative_to(target),
                   "SPLIT_FRESH_WORKSPACE_DISJOINT")
    outputs = {role: context.location_workspace/role for role in ("service-p", "service-q", "reader")}
    for output in outputs.values():
        output.mkdir()
    workspaces, tasks = {}, {}
    report = {"schema": "DMKN_V5_SPLIT_CUSTODY_CHECK_RESULT_V1", "status": "FAILED",
        "error": None, "cleanup_errors": [], "reader": None, "services": {},
        "scope": "ACTUAL_EXPLICIT_SPLIT_SEMANTIC_SERVICES_AND_UNCHANGED_LIVE_I_NATIVE_IMPORT",
        "split_scope": "P_PUBLIC_BODY_STORE_LACKS_SELECTED_ROW_NOT_ABSENCE_FROM_PACKET_INFORMATION",
        "authority": "OPERATION_EVIDENCE_NOT_TRANSFERABLE_AUTHORITY",
        "new_proof_calls": 0, "authoring_calls": 0, "public_network_calls": 0}
    try:
        for role in ("custody-p", "custody-q"):
            workspaces[role] = Workspace.open(paths[role], config, create=True)
        seed = _seed_split(workspaces["custody-p"], workspaces["custody-q"], packet, name, image)
        report["provider_seed"] = seed
        for workspace in workspaces.values():
            workspace.close()
        workspaces.clear()
        # Both unchanged finite service lifetimes start concurrently. No
        # deadline extension, serial lifetime wait or new lifecycle is added.
        for role, output in (("custody-p", "service-p"), ("custody-q", "service-q")):
            service_params = {"schema": serve_workspace.SCHEMA, "mode": "validated",
                "workspace_path": str(paths[role]), "workspace_config": config,
                "bind": {"host": "127.0.0.1", "port": 0}, "tls": None,
                "service_limits": params["service_limits"]}
            service_context = replace(context, location_workspace=outputs[output],
                                      parameters=MappingProxyType(service_params))
            tasks[role] = asyncio.create_task(serve_workspace.serve(service_context))
        ready_paths = {role: outputs[output]/"service-ready.json" for role, output in
                       (("custody-p", "service-p"), ("custody-q", "service-q"))}
        while not all(path.exists() for path in ready_paths.values()):
            context.remaining_seconds()
            F.need(not any(task.done() for task in tasks.values()),
                   "SPLIT_SERVICE_FAILED_BEFORE_READY")
            await asyncio.sleep(0.02)
        endpoints = {}
        for role, path in ready_paths.items():
            raw = path.read_bytes()
            F.need(len(raw) <= MIB, "SPLIT_READY_BOUND")
            endpoint = json.loads(raw)["endpoint"]
            F.need(endpoint["host"] == "127.0.0.1" and not endpoint["tls"],
                   "SPLIT_LOOPBACK_ONLY")
            endpoints[role] = endpoint
        F.need(endpoints["custody-p"]["port"] != endpoints["custody-q"]["port"],
               "SPLIT_DISTINCT_SERVICE_ENDPOINTS")
        reader.update(workspace_path=str(paths["reader"]), create_workspace=True)
        reader["query"]["contacts"] = {p_label: endpoints["custody-p"], Q: endpoints["custody-q"]}
        reader["query"]["egress_policy"] = {"schema": "DMKN_V5_OWNER_EGRESS_V1",
            "mode": "loopback-test", "public_ports": [], "test_endpoints": [
                {"host": endpoint["host"], "port": endpoint["port"]}
                for endpoint in endpoints.values()]}
        reader_context = replace(context, location_workspace=outputs["reader"],
                                 parameters=MappingProxyType(reader))
        outcome = await _read(reader_context, reader, params["helper_limits"],
                              params["max_rounds"], params["semantic_max_bytes"])
        report["reader"] = outcome
        F.need(outcome["status"] == "COMPLETED"
               and outcome["discovery"]["locator"]["module_id"] == seed["module"]
               and outcome["discovery"]["locator"]["relative_name"] == name,
               "SPLIT_RETURNED_TARGET_READY")
        selected = [action for row in outcome["rounds"] for action in row["actions"]
                    if action["kind"] == "fetch_body"
                    and action["demand"].get("body_hash") == SPLIT["body_hash"]]
        F.need(len(selected) == 1 and selected[0]["supplier"] == Q
               and selected[0]["status"] == "FETCHED", "SPLIT_ACTUAL_Q_BODY_DEMAND")
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
               "SPLIT_ONE_UNCHANGED_REAL_ADMISSION")
        services = await asyncio.gather(*tasks.values())
        report["services"] = dict(zip(tasks, services))
        F.need(all(service["status"] == "PASS" for service in services),
               "SPLIT_SERVICE_CLOSURE")
        # Q receives only the one exact group demand and one committed body.
        # No search, index hit or packet offer is fabricated for Q.
        F.need(report["services"]["custody-q"]["counters"]["requests"] == 2
               and report["services"]["custody-q"]["counters"]["failures"] == 0
               and sum(service["counters"]["requests"] for service in services) == 23
               and all(service["counters"]["failures"] == 0 for service in services),
               "SPLIT_ACTUAL_TWO_SERVICE_COUNTS")
        for role in ("custody-p", "custody-q"):
            workspaces[role] = Workspace.open(paths[role], config, create=False)
        report["post_service_inventory"] = _split_inventory(
            workspaces["custody-p"], workspaces["custody-q"])
        report.update(status="PASS", packet_pin=params["packet"], target_module=seed["module"])
    except BaseException as error:
        report["error"] = _error(error)
        raise
    finally:
        for task in tasks.values():
            if not task.done():
                task.cancel()
        for role, task in tasks.items():
            try:
                report["services"][role] = await task
            except asyncio.CancelledError:
                report["cleanup_errors"].append({"component": role,
                    "type": "CancelledError", "message": "cancelled_after_integration_failure"})
            except BaseException as error:
                report["cleanup_errors"].append({"component": role, **_error(error)})
        for role, workspace in workspaces.items():
            if not serve_workspace._close_workspace(workspace, report["cleanup_errors"]):
                report["cleanup_errors"].append({"component": role,
                    "type": "CleanupFailure", "message": "workspace_not_closed"})
        if report["cleanup_errors"]:
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        if report["finished"] >= context.deadline:
            report["status"] = "FAILED"
        _save(context.location_workspace/"split-check-result.json", report)
    return 0 if report["status"] == "PASS" else 1


def main(context):
    return asyncio.run(run(context))



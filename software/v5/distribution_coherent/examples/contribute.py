"""Trusted local-owner example: reuse, author, check, then index.

Run through the installed ``run`` command. This chooses one explicit input;
it is not an autonomous researcher, proof producer or global usefulness policy.
All mathematical authority remains in the unchanged client and exact owners.
"""
import asyncio
from copy import deepcopy
import hashlib
import time

from admission.trust import TrustDomain
from client import remote_reader
from client.runtime import RuntimeProfile, read_pin
from client.serve_workspace import _close_workspace
from client.workspace_validated import Workspace
from discovery.discovery_store import ordinary
from discovery import formal_features as F
from modules import codec as C

SCHEMA = "DMKN_V5_CONTRIBUTE_EXAMPLE_WITHDRAWAL_V1"
MIB = 1024**2


def _parameters(context):
    params = deepcopy(dict(context.parameters))
    F.fields(params, {"schema", "runtime_adoption", "foundation", "workspace_path",
        "workspace_config", "create_workspace", "operation_limits", "input",
        "source", "roots", "export_names", "author_limits", "admission_limits", "trust_domain"})
    F.need(params["schema"] == SCHEMA, "CONTRIBUTOR_SCHEMA")
    selected = params["input"]
    F.need(type(selected) is dict and selected.get("mode") in ("remote", "local-packet"),
           "CONTRIBUTOR_INPUT_MODE")
    if selected["mode"] == "remote":
        F.fields(selected, {"mode", "query"})
        selected["query"] = remote_reader._query(selected["query"])
    else:
        F.fields(selected, {"mode", "module", "packet"})
        F.hexid(selected["module"])
    for field in ("roots", "export_names"):
        names = params[field]
        F.need(type(names) is list and 1 <= len(names) <= 64, "CONTRIBUTOR_NAMES")
        for name in names:
            C.validate_name(name)
        F.need(len({C.name_key(name) for name in names}) == len(names),
               "CONTRIBUTOR_DUPLICATE_NAMES")
    author, admission = params["author_limits"], params["admission_limits"]
    F.fields(author, {"cpu_seconds", "wall_seconds", "memory_mib"})
    F.uint(author["cpu_seconds"], 1, 1200, "CONTRIBUTOR_AUTHOR_CPU")
    F.uint(author["wall_seconds"], 1, 600, "CONTRIBUTOR_AUTHOR_WALL")
    F.fields(admission, {"native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds", "memory_mib"})
    for key in ("native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds"):
        F.uint(admission[key], 1, 600, "CONTRIBUTOR_ADMISSION:"+key)
    memory_rows = [author, admission]
    if selected["mode"] == "remote":
        memory_rows.append(selected["query"]["admission"])
    for row in memory_rows:
        F.uint(row["memory_mib"], 64, 4096, "CONTRIBUTOR_MEMORY")
        F.need(row["memory_mib"] <= context.limits["memory_mib"],
               "CONTRIBUTOR_OUTER_MEMORY")
    # The pinned UTF-8 source is caller data, not a downloaded strategy or a
    # theorem chosen by this example. The frontend remains inside its owner Job.
    source = read_pin(params["source"], 65536).decode("utf-8")
    return params, source


def _paths(context, params):
    F.need(type(params["workspace_path"]) is str and type(params["create_workspace"]) is bool,
           "CONTRIBUTOR_WORKSPACE_SELECTION")
    workspace = ordinary(params["workspace_path"], fresh=params["create_workspace"])
    run, work = ordinary(context.run), ordinary(context.location_workspace)
    F.need(work != run and work.is_relative_to(run), "CONTRIBUTOR_OUTPUT_SCOPE")
    for value in (context.installation, run, context.sources_v5,
                  context.sources_portable, context.sources_owner):
        root = ordinary(value)
        F.need(not workspace.is_relative_to(root) and not root.is_relative_to(workspace),
               "CONTRIBUTOR_WORKSPACE_DISJOINT")
    return workspace, ordinary(work/"contribution-result.json", fresh=True, directory=False)


def _store_and_admit(client, workspace, grant, module, raw, limits):
    # Public lower-level custody: bounded by storage quotas, the original grant
    # callback and enclosing Job, NOT separately charged as a client action.
    # Neither put nor its successful structural inspection is an acceptance.
    grant.remaining_seconds()
    workspace.packets.put(module, raw, before_commit=grant.remaining_seconds)
    return client.admit_local(module, hashlib.sha256(raw).hexdigest(), len(raw), **limits)


def _local_import(client, workspace, grant, selected, limits):
    maximum = min(workspace.config["packet_limits"]["packet_bytes"],
                  grant.limits["input_bytes"], 128*MIB)
    raw = read_pin(selected["packet"], maximum)
    warrant = _store_and_admit(client, workspace, grant, selected["module"], raw, limits)
    fact = client.describe(warrant)
    detail = {"status": None, "mode": "local-packet",
        "module": fact["live"]["module"], "journal": list(fact["live"]["journal"]),
        "packet_sha256": selected["packet"]["sha256"], "packet_bytes": len(raw),
        "global_complete": False, "mathematical_acceptance": False}
    material = client.semantic_material(warrant)
    if material["status"] != "AVAILABLE_PACKET_SEMANTICS":
        detail.update(status="NEED_SEMANTICS", reason=material["status"],
            demands=[{"module": fact["live"]["module"], "kind": "committed-module-semantics"}])
        return {"report": detail, "context": None}
    selected_members = [member["journal"] for member in fact["members"]]
    ready = client.import_context([{"warrant": warrant, "resolutions": None}], selected_members,
                                  material["openings"], material["bodies"])
    detail.update(status=("READY" if ready["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY"
                          else "NEED_SEMANTICS"), import_status=ready["status"],
                  demands=ready.get("demands", []), context_cost=ready["cost"])
    return {"report": detail, "context": ready["context"]}


async def _contribute(client, workspace, grant, params, source, report):
    selected = params["input"]
    report["stage"] = "input"
    if selected["mode"] == "remote":
        answer = await remote_reader.read(client, selected["query"])
    else:
        answer = _local_import(client, workspace, grant, selected, params["admission_limits"])
    report["input"] = answer["report"]
    if answer["report"]["status"] != "READY":
        report["outcome"] = "NOT_CONTRIBUTED"
        return
    report["stage"] = "author"
    prepared = client.author(answer["context"], source, params["roots"], **params["author_limits"])
    report["preparation"] = {"status": prepared["status"]}
    if prepared["status"] == "NEED_AUTHORING_CONTEXT_DATA":
        report["preparation"]["demands"] = prepared.get("demands", [])
        report["outcome"] = "NOT_CONTRIBUTED"
        return
    F.need(prepared["status"] == "UNTRUSTED_MIXED_DELTA_PACKET_PREPARED"
           and prepared["mathematical_acceptance"] is False, "CONTRIBUTOR_UNTRUSTED_PREPARATION")
    child = prepared["child"]
    raw = child["packet"]
    F.need(child["status"] == "UNTRUSTED_MIXED_DELTA_PACKET"
           and child["mathematical_acceptance"] is False and type(raw) is bytes
           and hashlib.sha256(raw).hexdigest() == child["packet_sha256"],
           "CONTRIBUTOR_PREPARED_PACKET")
    report["preparation"].update(module=child["local_module"], packet_sha256=child["packet_sha256"],
        packet_bytes=len(raw), source_sha256=child["source_sha256"], roots=child["roots"])
    report["stage"] = "check-output"
    checked = _store_and_admit(client, workspace, grant, child["local_module"], raw,
                              params["admission_limits"])
    fact = client.describe(checked)
    F.need(fact["live"]["module"] == child["local_module"], "CONTRIBUTOR_OUTPUT_BINDING")
    # This record describes a same-operation check. It is not a saved warrant.
    report["checked_output"] = {"kind": fact["kind"], "module": fact["live"]["module"],
                               "journal": list(fact["live"]["journal"])}
    report["stage"] = "publish"
    publication = client.publish(raw, params["export_names"],
        retention_policy={"mode": "quota-bounded-local-custody"})
    report["publication"] = publication
    F.need(publication["phase"] == "LOCALLY_PUBLISHED"
           and publication["intent"]["module"] == child["local_module"]
           and publication["intent"]["packet_sha256"] == child["packet_sha256"],
           "CONTRIBUTOR_PUBLICATION_BINDING")
    report["stage"], report["outcome"] = "done", "CONTRIBUTED"


async def run(context):
    """One original grant, no retries; close live authority before returning."""
    started = time.monotonic()
    params, source = _parameters(context)
    path, output = _paths(context, params)
    F.need(time.monotonic() < context.deadline-5, "CONTRIBUTOR_CLEANUP_MARGIN")
    workspace = client = None
    primary = cancelled = None
    report = {"schema": "DMKN_V5_CONTRIBUTE_EXAMPLE_RESULT_V1", "status": "FAILED",
        "outcome": None, "stage": "open", "error": None, "cleanup_errors": [],
        "client_closed": False, "workspace_closed": False,
        "started": started, "outer_deadline": context.deadline,
        "input": None, "preparation": None, "checked_output": None, "publication": None,
        "client": None, "global_complete": False, "mathematical_acceptance": False,
        "authority": "OPERATIONAL_CONTRIBUTION_REPORT_NOT_TRANSFERABLE_AUTHORITY"}
    try:
        # Ordinary use opens existing owner policy; adoption is a separate action.
        trust = params["trust_domain"]
        F.fields(trust, {"directory", "domain_id", "support_id"})
        domain = TrustDomain.open(trust["directory"], trust["domain_id"], trust["support_id"])
        runtime = RuntimeProfile.from_context(context, params["runtime_adoption"],
                                              trust_domain=domain)
        foundation = read_pin(params["foundation"], 16*MIB)
        workspace = Workspace.open(path, params["workspace_config"], create=params["create_workspace"])
        grant = workspace.reserve(params["operation_limits"], outer_deadline=context.deadline-5)
        report["operation_id"] = grant.identifier
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=True,
            foundation_bytes=foundation, foundation_sha256=params["foundation"]["sha256"])
        await _contribute(client, workspace, grant, params, source, report)
        report["status"] = "COMPLETED"
    except BaseException as error:
        primary = error
        report["error"] = remote_reader._error(error)
        if isinstance(error, asyncio.CancelledError):
            cancelled = error
    finally:
        if client is not None:
            try:
                closed = await client.close()
                report["client"] = closed
                states = ("CLOSED",) if report["status"] == "COMPLETED" else ("CLOSED", "FAILED")
                F.need(closed["closed"] and closed["status"] in states
                       and all(closed[name] is None or closed[name]["closed"]
                               for name in ("receipt", "aggregate", "mixed", "preparation")),
                       "CONTRIBUTOR_CLIENT_CLEANUP")
                report["client_closed"] = True
            except BaseException as error:
                report["cleanup_errors"].append({"component": "client", **remote_reader._error(error)})
                if isinstance(error, asyncio.CancelledError) and cancelled is None:
                    cancelled = error
                    if primary is None:
                        primary = error
        if workspace is not None:
            report["workspace_closed"] = _close_workspace(workspace, report["cleanup_errors"])
        if report["cleanup_errors"] or not report["client_closed"] or not report["workspace_closed"]:
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        if report["finished"] >= context.deadline:
            report["status"] = "FAILED"
            report["cleanup_errors"].append({"component": "deadline", "type": "DeadlineExceeded",
                                             "message": "CONTRIBUTOR_ORIGINAL_DEADLINE"})
        try:
            remote_reader._save(output, report)
        except BaseException as error:
            if primary is not None:
                failures = [primary]
                if cancelled is not None and cancelled is not primary:
                    failures.append(cancelled)
                raise BaseExceptionGroup("Contribution failed; result write also failed", [*failures, error])
            raise
    if cancelled is not None:
        if primary is not None and primary is not cancelled:
            raise BaseExceptionGroup("Contribution failed; cleanup was cancelled", [primary, cancelled])
        raise cancelled
    return report


def main(context):
    # A clean miss/demand is a completed bounded operation, not a contribution.
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1

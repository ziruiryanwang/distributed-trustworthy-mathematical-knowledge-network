"""One ordinary bounded remote read, admission and semantic import.

This is an example local selection policy, not a usefulness ranker or planner.
Run main through client.boot; trusted callers can use read in a live operation.
"""
import asyncio
from copy import deepcopy
import json
import time

from client.direct_contacts import bind
from client.runtime import RuntimeProfile, read_pin
from client.serve_workspace import _close_workspace
from client.workspace_validated import Workspace, CommonsClient
from discovery.discovery_store import ordinary
from discovery import formal_features as F
from location.protocol import OwnerEgressPolicy

SCHEMA = "DMKN_V5_REMOTE_READER_V1"
MIB = 1024**2


def _error(error):
    return {"type": type(error).__name__, "message": str(error)[:1000]}


def _save(path, value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                     allow_nan=False).encode("utf-8")
    F.need(len(raw) <= MIB, "REMOTE_READER_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def _query(value):
    q = deepcopy(value)
    F.fields(q, {"contacts", "egress_policy", "specs", "search_limits",
                 "contact_lifetime_ms", "selection", "offer", "page", "packets", "admission"})
    choice = q["selection"]
    F.fields(choice, {"provider", "partition_index", "start", "candidate_index", "packet_index"})
    F.need(type(q["contacts"]) is dict and type(choice["provider"]) is str
           and choice["provider"] in q["contacts"], "REMOTE_READER_SELECTED_PROVIDER")
    for name in ("partition_index", "start", "candidate_index", "packet_index"):
        F.uint(choice[name], 0, 2**32-1, "REMOTE_READER_SELECTION:"+name)
    F.fields(q["offer"], {"max_bytes", "max_expanded_bytes", "max_age_ms", "attempt_timeout_ms"})
    F.fields(q["page"], {"limits", "attempt_timeout_ms"})
    F.fields(q["packets"], {"max_offers", "max_bytes"})
    F.fields(q["admission"], {"native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds", "memory_mib"})
    for name in ("native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds"):
        F.uint(q["admission"][name], 1, 600, "REMOTE_READER_ADMISSION:"+name)
    F.uint(q["admission"]["memory_mib"], 64, 4096, "REMOTE_READER_ADMISSION_MEMORY")
    return q


async def read(client, query):
    """One caller-chosen page/result, no retry or automatic semantic resolver.

    Return JSON ``report`` plus opaque candidate/warrant/context references.
    Those references are usable only inside this same still-live client.
    Exceptions preserve the client's existing fail-stop/charging behavior.
    """
    F.need(type(client) is CommonsClient, "REMOTE_READER_EXACT_VALIDATED_CLIENT")
    q = _query(query)
    choice, provider = q["selection"], q["selection"]["provider"]
    detail = {"status": None, "stage": "bind", "selection": choice,
              "global_complete": False, "mathematical_acceptance": False,
              "authority": "OPERATIONAL_READ_REPORT_NOT_TRANSFERABLE_AUTHORITY"}
    answer = {"report": detail, "candidate": None, "warrant": None, "context": None}
    detail["binding"] = bind(client, q["contacts"], q["specs"],
        OwnerEgressPolicy(q["egress_policy"]), q["search_limits"],
        contact_lifetime_ms=q["contact_lifetime_ms"])
    detail["stage"] = "offer"
    offer = await client.search_offer(provider, **q["offer"])
    if offer["status"] != "OFFERED":
        detail.update(status="REFUSED" if offer["status"] != "NO_OFFER" else "MISS",
                      reason=offer.get("reason", offer["status"]), response_status=offer["status"])
        return answer
    detail["snapshot_id"] = offer["snapshot_id"]
    # This scans only the bounded returned partition metadata, never records.
    # The ordinal is among nonempty partitions in the provider's verified offer.
    partitions = [row for row in offer["partitions"] if row["anchor_count"] > 0]
    if choice["partition_index"] >= len(partitions):
        detail.update(status="MISS", reason="SELECTED_PARTITION_NOT_RETURNED")
        return answer
    partition = partitions[choice["partition_index"]]
    detail["partition"] = partition["partition"]
    if choice["start"] >= partition["anchor_count"]:
        detail.update(status="MISS", reason="SELECTED_PAGE_HAS_NO_ANCHOR_POSITION")
        return answer
    detail["stage"] = "page"
    page = await client.search_page(provider, offer["snapshot_id"], partition["partition"],
        choice["start"], q["page"]["limits"], candidates_only=True,
        attempt_timeout_ms=q["page"]["attempt_timeout_ms"])
    if page["status"] != "VERIFIED_CANDIDATES":
        detail.update(status="REFUSED", reason=page.get("reason", page["status"]),
                      response_status=page["status"])
        return answer
    detail["returned_candidates"] = len(page["matches"])
    detail["advisory_next"] = page.get("advisory_next")
    if choice["candidate_index"] >= len(page["matches"]):
        detail.update(status="MISS", reason="SELECTED_CANDIDATE_NOT_RETURNED")
        return answer
    detail["stage"] = "resolve"
    candidate = await client.resolve(provider, page["matches"][choice["candidate_index"]])
    answer["candidate"] = candidate
    description = client.describe_candidate(candidate)
    detail["locator"] = description["locator"]
    detail["stage"] = "packet-offer"
    packets = await client.packet_offers(candidate, **q["packets"])
    if choice["packet_index"] >= len(packets["packets"]):
        detail.update(status="MISS", reason="SELECTED_PACKET_NOT_OFFERED")
        return answer
    entry = packets["packets"][choice["packet_index"]]
    detail["packet"] = entry
    detail["stage"] = "acquire"
    warrant = await client.acquire(candidate, entry, **q["admission"])
    answer["warrant"] = warrant
    fact = client.describe(warrant)
    detail["admitted"] = {"kind": fact["kind"], "module": fact["live"]["module"],
                         "journal": list(fact["live"]["journal"])}
    detail["stage"] = "semantics"
    material = client.semantic_material(warrant)
    if material["status"] != "AVAILABLE_PACKET_SEMANTICS":
        detail.update(status="NEED_SEMANTICS", reason=material["status"],
                      demands=[{"module": fact["live"]["module"], "kind": "committed-module-semantics"}])
        return answer
    # All members of this ONE admitted packet are an explicit example import
    # policy, not an inferred optimal dependency slice. Conflicts still refuse.
    selected = [member["journal"] for member in fact["members"]]
    ready = client.import_context([{"warrant": warrant, "resolutions": None}], selected,
                                  material["openings"], material["bodies"])
    answer["context"] = ready["context"]
    detail.update(status=("READY" if ready["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY"
                          else "NEED_SEMANTICS"), import_status=ready["status"],
                  demands=ready.get("demands", []), context_cost=ready["cost"],
                  unavailable_committed_bodies=material.get("unavailable_committed_bodies", []))
    return answer


def _paths(context, params):
    F.need(type(params["workspace_path"]) is str and type(params["create_workspace"]) is bool,
           "REMOTE_READER_WORKSPACE_SELECTION")
    workspace = ordinary(params["workspace_path"], fresh=params["create_workspace"])
    run, work = ordinary(context.run), ordinary(context.location_workspace)
    F.need(work != run and work.is_relative_to(run), "REMOTE_READER_OUTPUT_SCOPE")
    for value in (context.installation, run, context.sources_v5,
                  context.sources_portable, context.sources_owner):
        root = ordinary(value)
        F.need(not workspace.is_relative_to(root) and not root.is_relative_to(workspace),
               "REMOTE_READER_WORKSPACE_DISJOINT")
    return workspace, ordinary(work/"remote-reader-result.json", fresh=True, directory=False)


async def run(context):
    """Own one reader-only validated operation and retain nonauthoritative evidence."""
    started = time.monotonic()
    params = deepcopy(dict(context.parameters))
    F.fields(params, {"schema", "runtime_adoption", "workspace_path", "workspace_config",
                      "create_workspace", "operation_limits", "foundation", "query"})
    F.need(params["schema"] == SCHEMA, "REMOTE_READER_SCHEMA")
    q = _query(params["query"])
    path, output = _paths(context, params)
    F.need(q["admission"]["memory_mib"] <= context.limits["memory_mib"],
           "REMOTE_READER_OUTER_MEMORY")
    F.need(time.monotonic() < context.deadline-5, "REMOTE_READER_CLEANUP_MARGIN")
    workspace = client = None
    primary = cancelled = None
    report = {"schema": "DMKN_V5_REMOTE_READER_RESULT_V1", "status": "FAILED",
        "error": None, "cleanup_errors": [], "client_closed": False, "workspace_closed": False,
        "started": started, "outer_deadline": context.deadline,
        "read": None, "client": None, "global_complete": False, "mathematical_acceptance": False,
        "authority": "OPERATIONAL_READ_REPORT_NOT_TRANSFERABLE_AUTHORITY"}
    try:
        runtime = RuntimeProfile.from_context(context, params["runtime_adoption"])
        foundation = read_pin(params["foundation"], 16*MIB)
        workspace = Workspace.open(path, params["workspace_config"],
                                   create=params["create_workspace"])
        grant = workspace.reserve(params["operation_limits"], outer_deadline=context.deadline-5)
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=False,
            foundation_bytes=foundation, foundation_sha256=params["foundation"]["sha256"])
        outcome = await read(client, q)
        report["read"] = outcome["report"]
        # Live handles are intentionally not persisted; custom owner code uses
        # read() before close when it needs to continue from yielded demands.
        report["operation_id"] = grant.identifier
        report["status"] = "COMPLETED"
    except BaseException as error:
        primary = error
        report["error"] = _error(error)
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
                               for name in ("receipt", "aggregate", "mixed"))
                       and closed["preparation"] is None, "REMOTE_READER_CLIENT_CLEANUP")
                report["client_closed"] = True
            except BaseException as error:
                report["cleanup_errors"].append({"component": "client", **_error(error)})
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
                                             "message": "REMOTE_READER_ORIGINAL_DEADLINE"})
        try:
            _save(output, report)
        except BaseException as error:
            if primary is not None:
                failures = [primary]
                if cancelled is not None and cancelled is not primary:
                    failures.append(cancelled)
                raise BaseExceptionGroup("Remote read failed; result write also failed",
                                         [*failures, error])
            raise
    if cancelled is not None:
        if primary is not None and primary is not cancelled:
            raise BaseExceptionGroup("Remote read failed; cleanup was cancelled", [primary, cancelled])
        raise cancelled
    return report


def main(context):
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1

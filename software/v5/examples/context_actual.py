"""One genuine selected-context continuation; no network or proof production.

Trusted installed owner code. Retained input is data, not restored authority.
One fresh operation checks it, imports only selected semantics, then exercises
contribution.py. This is an integration case, not a growth benchmark.
"""
import asyncio
from copy import deepcopy
import hashlib
import json
import sys
import time

from aggregate_claims import bindings as B
from authoring.source import NATIVE_NAME_LIMITS
from client import remote_reader
from client.runtime import RuntimeProfile, read_pin
from client.serve_workspace import _close_workspace
from client.workspace_validated import Workspace
from custody.module_store import permitted_hashes
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from modules import codec as C
from modules.model import Address
from modules.source_rows import decode_source

MIB = 1024**2
BASE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
TARGET = "6ea8fa600c3ec9eb64992466c2c897d6455b53a6d0461a2b655fcb3f2c86d55f"
PACKET_SHA = "6998ba92d064c8ce790192a434655d4b99bf0e7018f422ec24be757de55db2eb"
PROJECTION = [["s", "ClientV5"], ["s", "project_summary"]]
ROOT = [["s", "ClientV5"], ["s", "summary_independence"]]


def _source():
    return """set_option autoImplicit false
noncomputable section
universe u v w z
namespace ClientV5
theorem summary_independence {A : Type u} {B : Type v} {C : Type w} {D : Type z}
    (leafB : A -> B) (nodeB : B -> B -> B)
    (leafC : A -> C) (nodeC : C -> C -> C)
    (leafD : A -> D) (nodeD : D -> D -> D)
    (e : DMKN.Mod.«@BASE@».CommonsV5.Tree A) :
    (DMKN.Mod.«@BASE@».CommonsV5.fold (fun x => (leafB x, leafC x))
      (fun x y => (nodeB x.1 y.1, nodeC x.2 y.2)) e).1 =
    (DMKN.Mod.«@BASE@».CommonsV5.fold (fun x => (leafB x, leafD x))
      (fun x y => (nodeB x.1 y.1, nodeD x.2 y.2)) e).1 :=
  Eq.trans (DMKN.Mod.«@TARGET@».ClientV5.project_summary leafB nodeB leafC nodeC e)
    (Eq.symm (DMKN.Mod.«@TARGET@».ClientV5.project_summary leafB nodeB leafD nodeD e))
end ClientV5
""".replace("@BASE@", BASE).replace("@TARGET@", TARGET)


def _selection(client, raw, fact):
    # Existing pure packet extraction is structural, not a fabricated live
    # owner. Only these selected groups/bodies enter the real import below.
    summary, groups, values, census = client._semantic_plan(raw)
    F.need(C.summary_id(summary) == TARGET and len(groups) == 13
           and census["claims"] == census["frontiers"] == 1
           and census["deltas"] == 2, "CONTEXT_ACTUAL_INPUT_STRUCTURE")
    keys = [(BASE, index) for index in range(8)] + [(TARGET, 0)]
    openings, bodies, seen = [], [], set()
    declarations = 0
    for module, index in keys:
        opening = C.parse_json(groups[module, index])
        group = opening["group"]
        if module == TARGET:
            F.need(len(group["declarations"]) == 1
                   and group["declarations"][0]["name"] == PROJECTION,
                   "CONTEXT_ACTUAL_TARGET_GROUP")
        declarations += len(group["declarations"])
        openings.append({"module": module, "opening": opening})
        for declaration in group["declarations"]:
            for digest in sorted(permitted_hashes(declaration)):
                arity = declaration["universes"]
                key = module, arity, digest
                if key in seen:
                    continue
                bodies.append({"module": module, "universes": arity,
                    "expression": C.parse_json(values[arity, digest])})
                seen.add(key)
    F.need(len(openings) == 9 and declarations == 12 and len(bodies) == 9,
           "CONTEXT_ACTUAL_SELECTED_CLOSURE")
    selected = []
    for module in (BASE, TARGET):
        matches = [member for member in fact["members"] if member["module"] == module]
        F.need(len(matches) == 1, "CONTEXT_ACTUAL_EXACT_MEMBER")
        selected.append(bytes(matches[0]["journal"]))
    return selected, openings, bodies


def _read_raw(path, maximum):
    path = ordinary(path, directory=False)
    F.need(path.stat().st_size <= maximum, "CONTEXT_ACTUAL_EVIDENCE_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    F.need(len(raw) <= maximum, "CONTEXT_ACTUAL_EVIDENCE_BOUND")
    return raw


def _inspect_export(grant, source, result, output_packet):
    # RuntimeProfile's existing first preparation location. No callback or
    # replacement author is installed to intercept the actual helper calls.
    directory = grant.directory / "preparation" / "author-1"
    request_raw = _read_raw(directory / "source-request.json", 16*MIB)
    export_raw = _read_raw(directory / "frontend" / "EXPORT.json", 16*MIB)
    # Operational telemetry permits timing floats; mathematical data retains
    # its strict parser. Bind actual file bytes, never reserialized JSON.
    worker = json.loads(_read_raw(directory / "worker-result.json", MIB))
    F.need(worker["schema"] == "DMKN_OWNER_LEAN_WORKER_RESULT_V1"
           and worker["status"] == "PASS_NATIVE_EXPORT_ONLY"
           and worker["request_sha256"] == hashlib.sha256(request_raw).hexdigest()
           and worker["export_sha256"] == hashlib.sha256(export_raw).hexdigest()
           and worker["export_bytes"] == len(export_raw)
           and worker["native_return_code"] == 0 and worker["native_timed_out"] is False
           and worker["direct_child_reaped"] is True,
           "CONTEXT_ACTUAL_WORKER_EXPORT_BINDING")
    F.need(_read_raw(directory / "mixed-packet.json", 16*MIB) == output_packet,
           "CONTEXT_ACTUAL_AUTHOR_ADMITTED_PACKET_BINDING")
    request, exported = C.parse_json(request_raw), C.parse_json(export_raw)
    source_sha = hashlib.sha256(source.encode("utf-8")).hexdigest()
    F.need(request["source"] == source and request["roots"] == exported["roots"] == [ROOT]
           and exported["source_sha256"] == result["preparation"]["source_sha256"] == source_sha,
           "CONTEXT_ACTUAL_EXPORTED_SOURCE_BINDING")
    context = request["context"]
    F.need(len(context["imports"]) == 9
           and {item["owner"] for item in context["imports"]} == {BASE, TARGET},
           "CONTEXT_ACTUAL_EXPORTED_SELECTED_CONTEXT")
    external = [{"source_name": C.relocated_name(item["owner"], declaration["name"]),
                 "module": item["owner"], "relative_name": declaration["name"]}
                for item in context["imports"] for declaration in item["group"]["declarations"]]
    env = decode_source(exported["rows"], exported["local_names"],
        context["foundation_view"]["names"], B.FOUNDATION, B.POLICY, external, NATIVE_NAME_LIMITS)
    witness = C.parse_json(output_packet)["deltas"][-1]
    F.need(env.module == result["checked_output"]["module"] and env.spec == witness["local_spec"],
           "CONTEXT_ACTUAL_EXPORT_CHECKED_PACKET")
    declarations = {C.name_key(d["name"]): d for group in env.spec["groups"] for d in group["declarations"]}
    declaration = declarations[C.name_key(ROOT)]
    F.need(declaration["kind"] == "theorem" and declaration["universes"] == 4,
           "CONTEXT_ACTUAL_GENERIC_THEOREM")
    digest = env.local_proofs[Address.of(env.module, ROOT)]
    proof = C.parse_json(env.bodies[declaration["universes"], digest])
    # Same bounded traversal as the existing actual-owner export inspector,
    # over already decoded expressions. Count occurrences, not shared DAG IDs.
    edges = {"sort": (), "bvar": (), "const": (), "app": (1, 2),
             "lam": (2, 3), "forall": (2, 3), "let": (1, 2, 3), "proj": (3,)}
    stack, visits, occurrences, equalities = [proof], 0, 0, set()
    while stack:
        node = stack.pop(); visits += 1
        F.need(visits <= 500000, "CONTEXT_ACTUAL_INSPECTION_BOUND")
        if node[0] == "const":
            reference = node[1]
            occurrences += reference == ["external", TARGET, PROJECTION]
            if reference[0] == "foundation":
                equalities.add(C.name_key(reference[1]))
        stack.extend(node[index] for index in edges[node[0]])
    F.need(occurrences == 2 and all(C.name_key([["s", "Eq"], ["s", name]]) in equalities
                                  for name in ("trans", "symm")),
           "CONTEXT_ACTUAL_TWO_REAL_PROJECTION_USES")
    return {"module": env.module, "root": ROOT, "universes": 4,
        "imported_projection_module": TARGET, "projection_occurrences": occurrences,
        "equality_transitivity_and_symmetry": True, "inspected_expression_nodes": visits,
        "type_sha256": hashlib.sha256(C.canonical(declaration["type"])).hexdigest(),
        "proof_body_sha256": hashlib.sha256(C.canonical(proof)).hexdigest(),
        "authority": "ACTUAL_EXPORT_INSPECTION_NOT_MATHEMATICAL_ACCEPTANCE"}


async def run(context):
    params = deepcopy(dict(context.parameters))
    F.fields(params, {"schema", "runtime_adoption", "foundation", "workspace_path",
        "workspace_config", "operation_limits", "packet", "author_limits", "admission_limits"})
    F.need(params["schema"] == "DMKN_V5_CONTEXT_ACTUAL_V1", "CONTEXT_ACTUAL_SCHEMA")
    F.need(params["packet"]["bytes"] == 658554 and params["packet"]["sha256"] == PACKET_SHA,
           "CONTEXT_ACTUAL_RETAINED_PACKET_PIN")
    for limits in (params["author_limits"], params["admission_limits"]):
        F.need(limits["memory_mib"] <= context.limits["memory_mib"], "CONTEXT_ACTUAL_OUTER_MEMORY")
    workspace_path = ordinary(params["workspace_path"], fresh=True)
    work = ordinary(context.location_workspace)
    run_path = ordinary(context.run)
    F.need(work != run_path and work.is_relative_to(run_path), "CONTEXT_ACTUAL_OUTPUT_SCOPE")
    for root in (context.installation, run_path, context.sources_owner,
                 context.sources_v5, context.sources_portable):
        root = ordinary(root)
        F.need(not workspace_path.is_relative_to(root) and not root.is_relative_to(workspace_path),
               "CONTEXT_ACTUAL_DISJOINT_WORKSPACE")
    output = ordinary(work / "context-contribution-result.json", fresh=True, directory=False)
    original_path = list(sys.path)
    try:
        sys.path.insert(0, str(context.sources_owner))
        from contribution import contribute_from_context
    finally:
        sys.path[:] = original_path
    F.need(time.monotonic() < context.deadline - 5, "CONTEXT_ACTUAL_CLEANUP_MARGIN")
    workspace = client = None
    primary = cancelled = None
    report = {"schema": "DMKN_V5_CONTEXT_ACTUAL_RESULT_V1", "status": "FAILED", "stage": "open",
        "error": None, "cleanup_errors": [], "client_closed": False, "workspace_closed": False,
        "client": None, "proof_calls": 0, "guest_calls": 0, "network_calls": 0,
        "full_v5_release": False, "mathematical_acceptance": False}
    try:
        runtime = RuntimeProfile.from_context(context, params["runtime_adoption"])
        foundation = read_pin(params["foundation"], 16*MIB)
        raw = read_pin(params["packet"], MIB)
        workspace = Workspace.open(workspace_path, params["workspace_config"], create=True)
        grant = workspace.reserve(params["operation_limits"], outer_deadline=context.deadline - 5)
        report["operation_id"] = grant.identifier
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=True,
            foundation_bytes=foundation, foundation_sha256=params["foundation"]["sha256"])
        report["stage"] = "admit-input"
        grant.remaining_seconds()
        workspace.packets.put(TARGET, raw, before_commit=grant.remaining_seconds)
        warrant = client.admit_local(TARGET, PACKET_SHA, len(raw), **params["admission_limits"])
        fact = client.describe(warrant)
        F.need(fact["live"]["module"] == TARGET and fact["live"]["packet_sha256"] == PACKET_SHA,
               "CONTEXT_ACTUAL_ADMITTED_INPUT")
        report["stage"] = "select-context"
        selected, openings, bodies = _selection(client, raw, fact)
        ready = client.import_context([{"warrant": warrant, "resolutions": None}], selected, openings, bodies)
        report["input_context"] = {"status": ready["status"], "cost": ready["cost"],
            "selected_members": [list(value) for value in selected], "groups": len(openings),
            "bodies": len(bodies), "demands": ready.get("demands", [])}
        F.need(ready["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY" and ready["context"] is not None
               and not ready.get("demands") and ready["cost"]["groups"] == 9
               and ready["cost"]["declarations"] == 12
               and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
               "CONTEXT_ACTUAL_GENUINE_SELECTED_CONTEXT")
        report["before_contribution"] = client.report()
        report["stage"] = "contribute"
        source = _source()
        result = contribute_from_context(client, ready["context"], source=source, roots=[ROOT],
            export_names=[ROOT], author_limits=params["author_limits"],
            admission_limits=params["admission_limits"])
        report["contribution"] = result
        F.need(result["status"] == "CONTRIBUTED" and result["operation_id"] == grant.identifier,
               "CONTEXT_ACTUAL_CONTRIBUTED")
        report["stage"] = "inspect-export"
        intent = result["publication"]["intent"]
        output_packet = workspace.packets.get(intent["packet_sha256"], intent["packet_bytes"])
        report["export_inspection"] = _inspect_export(grant, source, result, output_packet)
        after = client.report()
        report["after_contribution"] = after
        F.need(after["operation_id"] == grant.identifier
               and after["counts"]["admission_submissions"] == 2
               and after["counts"]["author_calls"] == after["counts"]["new_import_sessions"] == 1
               and after["counts"]["publication_attempts"] == 1
               and after["mixed"]["attempts"] == 2 and after["preparation"]["calls"] == 1
               and after["aggregate"]["attempts"] == 0
               and after["search"] is None and after["location"] is None and after["transport"] is None,
               "CONTEXT_ACTUAL_ONE_OPERATION_SUFFIX_COUNTS")
        report.update(status="COMPLETED", stage="done")
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
                       "CONTEXT_ACTUAL_CLIENT_CLEANUP")
                report["client_closed"] = True
            except BaseException as error:
                report["cleanup_errors"].append({"component": "client", **remote_reader._error(error)})
                if isinstance(error, asyncio.CancelledError):
                    cancelled = error
        if workspace is not None:
            report["workspace_closed"] = _close_workspace(workspace, report["cleanup_errors"])
        if report["cleanup_errors"] or not report["client_closed"] or not report["workspace_closed"]:
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        if report["finished"] >= context.deadline:
            report["status"] = "FAILED"
            report["cleanup_errors"].append({"component": "deadline", "message": "ORIGINAL_DEADLINE"})
        try:
            remote_reader._save(output, report)
        except BaseException as error:
            if primary is not None:
                raise BaseExceptionGroup("Continuation and evidence write failed", [primary, error])
            raise
    if cancelled is not None:
        if primary is not None and primary is not cancelled:
            raise BaseExceptionGroup("Continuation failed; cleanup cancelled", [primary, cancelled])
        raise cancelled
    return report


def main(context):
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1

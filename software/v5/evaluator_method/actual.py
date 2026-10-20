"""One ordinary I-parent evaluator-method authoring and native-witness gate.

Trusted local owner, not a new API/checker/producer. No cryptographic production,
snapshot, guest, publication or network action. A distinct mathematical target
must not be treated as a controlled speedup of the retained fold-map workload.
"""
import asyncio
from copy import deepcopy
import hashlib
import json
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
ROOT = [["s", "OwnerV5"], ["s", "evaluator_unique"]]
TREE = [["s", "CommonsV5"], ["s", "Tree"]]
CONGR = [["s", "CommonsV5"], ["s", "binary_congr"]]
PINS = {
    "receipt": "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47",
    "bundle": "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926",
    "source": "e9beebfd492cfe3a809ee02fd1d010ca043ea33814161b580c5d62d97fcbb686",
    "reference_witness": "88b71b8282afc99297bf6564d22616fce6211eed9a9e18afa1cb42a41d1206e1",
}


def _selection(bundle):
    F.fields(bundle, {"schema", "module", "spec", "openings", "bodies",
                      "certificate_verification", "mathematical_admission"})
    F.need(bundle["schema"] == "DMKN_V5_OWNER_WORKLOAD_BUNDLE_V1"
           and bundle["module"] == C.module_id(bundle["spec"]) == BASE,
           "EVALUATOR_EXACT_BASE_SEMANTICS")
    # Historical acceptance fields are never restored as authority.
    openings, bodies = [], []
    for index in (0, 10):
        opening = C.group_opening(bundle["spec"], index)
        F.need(opening == bundle["openings"][index], "EVALUATOR_BASE_OPENING_BINDING")
        openings.append({"module": BASE, "opening": opening})
    declarations = [d for item in openings for d in item["opening"]["group"]["declarations"]]
    F.need(len(declarations) == 5 and declarations[0]["name"] == TREE
           and declarations[-1]["name"] == CONGR
           and [d["kind"] for d in declarations]
               == ["inductive", "constructor", "constructor", "recursor", "theorem"],
           "EVALUATOR_SELECTED_INTERFACE")
    for declaration in declarations:
        if declaration["kind"] != "recursor":
            continue
        for digest in sorted(permitted_hashes(declaration)):
            candidates = [row for row in bundle["bodies"]
                          if row["digest"] == digest and row["universes"] == declaration["universes"]]
            F.need(len(candidates) == 1, "EVALUATOR_EXACT_RULE_BODY")
            row = candidates[0]
            F.need(C.body_id(row["expression"], row["universes"]) == digest,
                   "EVALUATOR_RULE_BODY_HASH")
            bodies.append({"module": BASE, "universes": row["universes"], "expression": row["expression"]})
    F.need(len(bodies) == 2, "EVALUATOR_TWO_RULE_BODIES")
    return C.summarize(bundle["spec"]), openings, bodies


def _raw(path, maximum=16*MIB):
    path = ordinary(path, directory=False)
    size = path.stat().st_size
    F.need(0 < size <= maximum, "EVALUATOR_INSPECTION_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    F.need(len(raw) == size, "EVALUATOR_INSPECTION_CHANGED")
    return raw


def _shape(witness, raw):
    return {"witness_bytes": len(raw), "witness_sha256": hashlib.sha256(raw).hexdigest(),
        "rows": len(witness["rows"]), "parents": len(witness["parents"]),
        "parent_groups": sum(len(item["openings"]) for item in witness["parents"]),
        "bodies": len(witness["bodies"]), "local_groups": len(witness["local_spec"]["groups"]),
        "local_declarations": sum(len(group["declarations"]) for group in witness["local_spec"]["groups"]),
        "rank": witness["rank"]}


def _inspect(grant, source, prepared, live, journal, openings, bodies, reference_raw, destination):
    directory = grant.directory / "preparation" / "author-1"
    request_raw = _raw(directory / "source-request.json")
    export_raw = _raw(directory / "frontend" / "EXPORT.json")
    worker = json.loads(_raw(directory / "worker-result.json", MIB))
    F.need(worker["schema"] == "DMKN_OWNER_LEAN_WORKER_RESULT_V1"
           and worker["status"] == "PASS_NATIVE_EXPORT_ONLY"
           and worker["request_sha256"] == hashlib.sha256(request_raw).hexdigest()
           and worker["export_sha256"] == hashlib.sha256(export_raw).hexdigest()
           and worker["export_bytes"] == len(export_raw)
           and worker["native_return_code"] == 0 and worker["native_timed_out"] is False
           and worker["direct_child_reaped"] is True, "EVALUATOR_ACTUAL_EXPORT_BINDING")
    child = prepared["child"]
    raw = child["packet"]
    F.need(_raw(directory / "mixed-packet.json") == raw, "EVALUATOR_ACTUAL_PACKET_BINDING")
    request, exported = C.parse_json(request_raw), C.parse_json(export_raw)
    F.need(request["source"] == source and request["roots"] == exported["roots"] == [ROOT]
           and exported["source_sha256"] == child["source_sha256"] == PINS["source"],
           "EVALUATOR_ACTUAL_SOURCE_BINDING")
    context = request["context"]
    F.need(context.get("definition_mode", "eager") == "eager"
           and len(context["imports"]) == 2
           and {item["owner"] for item in context["imports"]} == {BASE}
           and {item["index"] for item in context["imports"]} == {0, 10}
           and sum(len(item["bodies"]) for item in context["imports"]) == 2,
           "EVALUATOR_ACTUAL_SELECTED_CONTEXT")
    original = {item["opening"]["index"]: item["opening"] for item in openings}
    F.need(all(item["group"] == original[item["index"]]["group"] for item in context["imports"]),
           "EVALUATOR_NO_INTERFACE_REWRITING")
    external = [{"source_name": C.relocated_name(item["owner"], d["name"]),
                 "module": item["owner"], "relative_name": d["name"]}
                for item in context["imports"] for d in item["group"]["declarations"]]
    env = decode_source(exported["rows"], exported["local_names"], context["foundation_view"]["names"],
        B.FOUNDATION, B.POLICY, external, NATIVE_NAME_LIMITS)
    packet = C.parse_json(raw)
    F.need(len(packet["deltas"]) == 1, "EVALUATOR_SINGLE_NEW_DELTA")
    witness = packet["deltas"][0]
    image = bytes.fromhex(B.RELATION_IMAGE)
    words = [int.from_bytes(image[i:i+4], "little") for i in range(0, 32, 4)]
    F.need(witness["schema"] == "DMKN_CERTIFIED_MODULES_V2" and witness["image"] == words
           and witness["rank"] == 1 and len(witness["parents"]) == 1
           and bytes(witness["parents"][0]["journal"]) == journal
           and witness["parents"][0]["openings"] == [original[0], original[10]],
           "EVALUATOR_EXACT_GENUINE_I_PARENT")
    expected_bodies = {(row["universes"], C.body_id(row["expression"], row["universes"])): row["expression"]
                       for row in bodies}
    actual_bodies = {(row["universes"], row["digest"]): row["expression"] for row in witness["bodies"]}
    F.need(len(witness["bodies"]) == len(actual_bodies) == 2 and actual_bodies == expected_bodies,
           "EVALUATOR_ONLY_REQUIRED_RULE_BODIES")
    declarations = [d for group in env.spec["groups"] for d in group["declarations"]]
    F.need(env.module == live["module"] == child["local_module"] and env.spec == witness["local_spec"]
           and len(env.spec["groups"]) == len(declarations) == 1
           and declarations[0]["name"] == ROOT and declarations[0]["kind"] == "theorem"
           and declarations[0]["universes"] == 2, "EVALUATOR_SINGLE_GENERIC_THEOREM")
    declaration = declarations[0]
    conclusion, binders = declaration["type"], 0
    while conclusion[0] == "forall":
        binders += 1
        conclusion = conclusion[3]
    head, arguments = conclusion, []
    while head[0] == "app":
        arguments.append(head[2]); head = head[1]
    arguments.reverse()
    F.need(binders == 11 and head[0] == "const"
           and head[1] == ["foundation", [["s", "Eq"]]]
           and arguments == [["bvar", 9], ["app", ["bvar", 6], ["bvar", 0]],
                             ["app", ["bvar", 5], ["bvar", 0]]],
           "EVALUATOR_DISTINCT_ARBITRARY_EVALUATORS")
    proof_hash = env.local_proofs[Address.of(env.module, ROOT)]
    proof = C.parse_json(env.bodies[declaration["universes"], proof_hash])
    edges = {"sort": (), "bvar": (), "const": (), "app": (1, 2),
             "lam": (2, 3), "forall": (2, 3), "let": (1, 2, 3), "proj": (3,)}
    stack, visits, recursors, congruences = [proof], 0, 0, 0
    foundation_constants = set()
    while stack:
        node = stack.pop(); visits += 1
        F.need(visits <= 500000, "EVALUATOR_INSPECTION_BOUND")
        if node[0] == "const":
            reference = node[1]
            recursors += reference == ["external", BASE, TREE + [["s", "rec"]]]
            congruences += reference == ["external", BASE, CONGR]
            if reference[0] == "foundation":
                foundation_constants.add(C.name_key(reference[1]))
        stack.extend(node[index] for index in edges[node[0]])
    F.need(recursors == congruences == 1
           and all(C.name_key([["s", "Eq"], ["s", name]]) in foundation_constants
                   for name in ("trans", "symm")), "EVALUATOR_SUBSTANTIVE_INDUCTION_AND_REUSE")
    witness_raw = C.canonical(witness)
    reference = C.parse_json(reference_raw)
    F.need(reference["schema"] == witness["schema"] and reference["image"] == witness["image"],
           "EVALUATOR_REFERENCE_SAME_RELATION")
    with destination.open("xb") as stream:
        stream.write(witness_raw)
    return {"module": env.module, "root": ROOT, "universes": 2, "outer_binders": binders,
        "tree_recursor_uses": recursors, "binary_congr_uses": congruences,
        "inspected_expression_nodes": visits,
        "type_sha256": hashlib.sha256(C.canonical(declaration["type"])).hexdigest(),
        "proof_body_sha256": hashlib.sha256(C.canonical(proof)).hexdigest(),
        "source_request_bytes": len(request_raw), "export_rows": len(exported["rows"]),
        "method_witness": {"path": str(destination), **_shape(witness, witness_raw)},
        "reference_witness": _shape(reference, reference_raw),
        "comparison_scope": "DISTINCT_THEOREMS_AND_CONTEXTS_NOT_CONTROLLED_SPEEDUP",
        "authority": "ACTUAL_EXPORT_INSPECTION_NOT_MATHEMATICAL_ACCEPTANCE"}


async def run(context):
    params = deepcopy(dict(context.parameters))
    F.fields(params, {"schema", "runtime_adoption", "foundation", "workspace_path", "workspace_config",
        "operation_limits", "receipt", "bundle", "source", "reference_witness", "receipt_limits",
        "author_limits", "admission_limits"})
    F.need(params["schema"] == "DMKN_V5_EVALUATOR_METHOD_ACTUAL_V1", "EVALUATOR_ACTUAL_SCHEMA")
    for name, digest in PINS.items():
        F.need(params[name]["sha256"] == digest, "EVALUATOR_REVIEWED_INPUT_PIN:" + name)
    for name in ("receipt_limits", "author_limits", "admission_limits"):
        F.need(params[name]["memory_mib"] <= context.limits["memory_mib"], "EVALUATOR_OUTER_MEMORY")
    workspace_path = ordinary(params["workspace_path"], fresh=True)
    work, run_path = ordinary(context.location_workspace), ordinary(context.run)
    F.need(work != run_path and work.is_relative_to(run_path), "EVALUATOR_OUTPUT_SCOPE")
    for root in (context.installation, run_path, context.sources_owner, context.sources_v5, context.sources_portable):
        root = ordinary(root)
        F.need(not workspace_path.is_relative_to(root) and not root.is_relative_to(workspace_path),
               "EVALUATOR_DISJOINT_WORKSPACE")
    output = ordinary(work / "evaluator-method-result.json", fresh=True, directory=False)
    destination = ordinary(work / "method-witness.json", fresh=True, directory=False)
    F.need(time.monotonic() < context.deadline - 5, "EVALUATOR_CLEANUP_MARGIN")
    workspace = client = None
    primary = cancelled = None
    report = {"schema": "DMKN_V5_EVALUATOR_METHOD_ACTUAL_RESULT_V1", "status": "FAILED", "stage": "open",
        "error": None, "cleanup_errors": [], "client_closed": False, "workspace_closed": False,
        "client": None, "cryptographic_production_calls": 0, "guest_calls": 0, "network_calls": 0,
        "new_receipt": False, "full_v5_release": False, "mathematical_acceptance": False}
    try:
        runtime = RuntimeProfile.from_context(context, params["runtime_adoption"])
        foundation = read_pin(params["foundation"], 16*MIB)
        receipt = read_pin(params["receipt"], MIB)
        bundle = C.parse_json(read_pin(params["bundle"], MIB))
        source = read_pin(params["source"], MIB).decode("utf-8")
        reference_raw = read_pin(params["reference_witness"], MIB)
        summary, openings, bodies = _selection(bundle)
        workspace = Workspace.open(workspace_path, params["workspace_config"], create=True)
        grant = workspace.reserve(params["operation_limits"], outer_deadline=context.deadline - 5)
        report["operation_id"] = grant.identifier
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=True,
            foundation_bytes=foundation, foundation_sha256=params["foundation"]["sha256"])
        report["stage"] = "admit-genuine-I-parent"
        warrant = client.admit_receipt(receipt, summary, **params["receipt_limits"])
        fact = client.describe(warrant)
        journal = bytes(fact["live"]["journal"])
        F.need(fact["kind"] == "I" and fact["live"]["module"] == BASE
               and fact["live"]["receipt_sha256"] == PINS["receipt"], "EVALUATOR_GENUINE_I_WARRANT")
        report["parent"] = {"module": BASE, "receipt_sha256": PINS["receipt"], "journal": list(journal)}
        report["stage"] = "import-two-groups"
        ready = client.import_context([{"warrant": warrant, "resolutions": None}], [journal], openings, bodies)
        report["context"] = {"status": ready["status"], "cost": ready["cost"], "demands": ready.get("demands", [])}
        F.need(ready["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY" and ready["context"] is not None
               and not ready.get("demands") and ready["cost"]["groups"] == 2
               and ready["cost"]["declarations"] == 5
               and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0, "EVALUATOR_READY_CONTEXT")
        report["stage"] = "author-once"
        prepared = client.author(ready["context"], source, [ROOT], **params["author_limits"])
        F.need(prepared["status"] == "UNTRUSTED_MIXED_DELTA_PACKET_PREPARED"
               and prepared["mathematical_acceptance"] is False, "EVALUATOR_UNTRUSTED_PREPARATION")
        child = prepared["child"]
        raw = child["packet"]
        F.need(type(raw) is bytes and child["status"] == "UNTRUSTED_MIXED_DELTA_PACKET"
               and child["mathematical_acceptance"] is False and child["roots"] == [ROOT]
               and child["packet_sha256"] == hashlib.sha256(raw).hexdigest()
               and child["source_sha256"] == PINS["source"], "EVALUATOR_PREPARATION_BINDING")
        report["stage"] = "fresh-native-admission"
        workspace.packets.put(child["local_module"], raw, before_commit=grant.remaining_seconds)
        checked = client.admit_local(child["local_module"], child["packet_sha256"], len(raw),
                                     **params["admission_limits"])
        output_fact = client.describe(checked)
        live = output_fact["live"]
        F.need(output_fact["kind"] == "mixed" and live["module"] == child["local_module"]
               and live["packet_sha256"] == child["packet_sha256"] and live["summary"] == child["summary"],
               "EVALUATOR_FRESH_OUTPUT_ADMISSION")
        report["checked_output"] = {"module": live["module"], "journal": list(live["journal"]),
            "packet_sha256": child["packet_sha256"], "packet_bytes": len(raw)}
        report["stage"] = "inspect-native-witness"
        report["inspection"] = _inspect(grant, source, prepared, live, journal, openings, bodies,
                                        reference_raw, destination)
        after = client.report()
        report["before_close"] = after
        F.need(after["counts"]["admission_submissions"] == 2
               and after["counts"]["author_calls"] == after["counts"]["new_import_sessions"] == 1
               and after["counts"]["publication_attempts"] == 0
               and after["receipt"]["attempts"] == 2 and after["aggregate"]["attempts"] == 0
               and after["mixed"]["attempts"] == after["preparation"]["calls"] == 1
               and all(after[name] is None for name in ("search", "location", "transport")),
               "EVALUATOR_EXACT_EXISTING_ROUTE_COUNTS")
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
                       "EVALUATOR_CLIENT_CLEANUP")
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
                raise BaseExceptionGroup("Evaluator continuation and evidence write failed", [primary, error])
            raise
    if cancelled is not None:
        if primary is not None and primary is not cancelled:
            raise BaseExceptionGroup("Evaluator continuation failed; cleanup cancelled", [primary, cancelled])
        raise cancelled
    return report


def main(context):
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1

"""Ordinary reader example: pinned runtime -> real receipt -> semantic context.

Invoked as a trusted owner by client.boot. Parameters contain local adoption and
mathematical input pins, not a fixed theorem, fixture phase, or acceptance report.
No authoring, proof generation, native-delta execution, or network call occurs.
"""
import asyncio
from copy import deepcopy
import hashlib
import json
import time

from client.runtime import RuntimeProfile, read_pin
from client.workspace_atomic import Workspace
from modules import codec as C

MIB = 1024**2
SCHEMA = "DMKN_V5_RUNTIME_CHECK_V1"


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def _evidence(path):
    """Identity of newly produced evidence, never an acceptance loader."""
    size = path.stat().st_size
    need(0 < size <= MIB, "RUNTIME_CHECK_EVIDENCE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(size+1)
    need(len(raw) == size, "RUNTIME_CHECK_EVIDENCE_CHANGED")
    return {"path": str(path), "bytes": size, "sha256": hashlib.sha256(raw).hexdigest()}


def _save(path, report):
    raw = json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                     allow_nan=False).encode("utf-8")
    need(len(raw) <= MIB, "RUNTIME_CHECK_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


async def _run(context):
    started, cpu = time.monotonic(), time.process_time()
    workspace = client = None
    report = {"schema": "DMKN_V5_RUNTIME_CHECK_RESULT_V1", "status": "FAIL",
        "scope": "REAL_FACTORY_I_RECEIPT_AND_SEMANTIC_IMPORT_ONLY",
        "authority": "OPERATION_EVIDENCE_NOT_TRANSFERABLE_MATHEMATICAL_AUTHORITY",
        "error": None, "cleanup_errors": [], "client_closed": False, "workspace_closed": False}
    try:
        context.remaining_seconds()
        params = deepcopy(dict(context.parameters))
        C.fields(params, {"schema", "runtime_adoption", "workspace_config", "operation_limits",
                          "foundation", "receipt", "bundle", "verification_limits"})
        need(params["schema"] == SCHEMA, "RUNTIME_CHECK_PARAMETERS")
        call = params["verification_limits"]
        C.fields(call, {"cpu_seconds", "wall_seconds", "memory_mib"})
        for key, cap in (("cpu_seconds", 600), ("wall_seconds", 600), ("memory_mib", 4096)):
            need(type(call[key]) is int and 0 < call[key] <= cap, "RUNTIME_CHECK_CALL_LIMIT")
        need(call["cpu_seconds"] <= params["operation_limits"]["acquisition"]["worker_cpu_seconds"]
             and call["cpu_seconds"] <= context.limits["cpu_seconds"]
             and call["wall_seconds"] <= context.limits["wall_seconds"]
             and call["memory_mib"] <= context.limits["memory_mib"], "RUNTIME_CHECK_OUTER_SUBLIMIT")
        runtime = RuntimeProfile.from_context(context, params["runtime_adoption"])
        foundation = read_pin(params["foundation"], 16*MIB)
        receipt = read_pin(params["receipt"], MIB)
        bundle = C.parse_json(read_pin(params["bundle"], MIB))
        C.fields(bundle, {"schema", "module", "spec", "openings", "bodies",
                          "certificate_verification", "mathematical_admission"})
        need(bundle["schema"] == "DMKN_V5_OWNER_WORKLOAD_BUNDLE_V1", "RUNTIME_CHECK_BUNDLE_SCHEMA")
        # The bundle's historical verification/admission fields are not consulted.
        # Exact current mathematical authority comes only from admit_receipt.
        summary = C.summarize(bundle["spec"])
        module = C.summary_id(summary)
        need(bundle["module"] == module, "RUNTIME_CHECK_BUNDLE_MODULE")
        need(type(bundle["openings"]) is list and type(bundle["bodies"]) is list,
             "RUNTIME_CHECK_SEMANTIC_LISTS")
        workspace = Workspace.open(context.location_workspace/"runtime-workspace",
                                   params["workspace_config"], create=True)
        grant = workspace.reserve(params["operation_limits"], outer_deadline=context.deadline)
        client = runtime.open_operation(workspace, grant, mode="atomic", authoring=False,
            foundation_bytes=foundation, foundation_sha256=params["foundation"]["sha256"])
        warrant = client.admit_receipt(receipt, summary, **call)
        described = client.describe(warrant)
        need(described["kind"] == "I" and described["live"]["module"] == module
             and described["live"]["summary"] == summary
             and described["live"]["receipt_sha256"] == params["receipt"]["sha256"],
             "RUNTIME_CHECK_SAME_CALL_RECEIPT_TARGET")
        ready = client.import_context([{"warrant": warrant, "resolutions": None}],
            [described["live"]["journal"]],
            [{"module": module, "opening": row} for row in bundle["openings"]],
            [{"module": module, "universes": row["universes"], "expression": row["expression"]}
             for row in bundle["bodies"]])
        need(ready["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY"
             and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
             "RUNTIME_CHECK_CONTEXT_READY")
        live = client.report()
        need(live["receipt"]["attempts"] == 1 and live["mixed"]["attempts"] == 0
             and live["counts"]["admission_submissions"] == 1
             and live["counts"]["new_import_sessions"] == 1
             and live["counts"]["author_calls"] == live["counts"]["publication_attempts"] == 0
             and live["preparation"] is None and live["search"] is None
             and live["location"] is None and live["transport"] is None,
             "RUNTIME_CHECK_EXACT_READER_ONLY_CALLS")
        receipt_dir = grant.directory/"receipt-1"
        report.update(module=module, summary=summary, operation_id=grant.identifier,
            input_pins={name: params[name] for name in ("foundation", "receipt", "bundle")},
            runtime_adoption=params["runtime_adoption"],
            runtime_profile_sha256=hashlib.sha256(C.canonical(runtime.describe())).hexdigest(),
            context={"status": ready["status"], "cost": ready["cost"],
                     "demands": ready.get("demands", []), "mathematical_acceptance": False},
            same_call_evidence={name: _evidence(receipt_dir/name)
                               for name in ("request.json", "binding.json", "process.json")},
            verifier_stdout=_evidence(receipt_dir/"command"/"stdout.txt"),
            counts=live["counts"], receipt=live["receipt"], mixed=live["mixed"],
            verification_limits=call, operation_limits=grant.limits,
            status="PASS_REAL_RUNTIME_I_RECEIPT_AND_SEMANTIC_IMPORT")
        context.remaining_seconds()
    except BaseException as error:
        report["status"] = "FAIL"
        report["error"] = type(error).__name__+":"+str(error)[:2000]
    finally:
        if client is not None:
            try:
                closed = await client.close()
                clean_states = ("CLOSED",) if report["status"].startswith("PASS_") else ("CLOSED", "FAILED")
                need(closed["status"] in clean_states and closed["closed"] is True
                     and closed["receipt"]["closed"] is True and closed["mixed"]["closed"] is True,
                     "RUNTIME_CHECK_CLIENT_CLOSURE")
                report["client_closed"] = True
                report["closed_client_status"] = closed["status"]
                report["closed_client_cost"] = {
                    "controller_cpu_since_grant": closed["observed_controller_cpu_since_grant"],
                    "wall_since_grant": closed["wall_since_grant"],
                    "counts": closed["counts"],
                    "scope": "INCLUSIVE_CONTROLLER_LIFETIME_NOT_ADDITIVE_TO_OUTER_JOB"}
            except BaseException as error:
                report["cleanup_errors"].append(type(error).__name__+":"+str(error)[:1000])
        if workspace is not None:
            try:
                workspace.close()
                report["workspace_closed"] = workspace._closed
                need(workspace._closed, "RUNTIME_CHECK_WORKSPACE_CLOSURE")
            except BaseException as error:
                report["cleanup_errors"].append(type(error).__name__+":"+str(error)[:1000])
        if report["cleanup_errors"]:
            report["status"] = "FAIL_CLEANUP"
        report["owner_controller_cpu_seconds"] = time.process_time()-cpu
        report["owner_wall_seconds"] = time.monotonic()-started
        report["cost_scope"] = "INCLUSIVE_OWNER_OBSERVATION;OUTER_JOB_AND_EXIT_TAIL_REPORTED_BY_LAUNCHER"
        _save(context.location_workspace/"runtime-result.json", report)
    return 0 if report["status"] == "PASS_REAL_RUNTIME_I_RECEIPT_AND_SEMANTIC_IMPORT" else 1


def main(context):
    return asyncio.run(_run(context))

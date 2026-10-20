"""One genuine receipt and persisted withdrawal through ordinary public owners.

Trusted local operator. No substitute issuer, new proof, authoring, native delta
or network. Historical acceptance flags are never loaded as live authority.
"""
import asyncio
from copy import deepcopy
import time

from admission import trust as T
from client import remote_reader
from client.runtime import RuntimeProfile, read_pin
from client.serve_workspace import _close_workspace
from client.workspace_validated import Workspace
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from modules import codec as C

MIB = 1024**2
BASE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
RECEIPT = "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"
BUNDLE = "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926"


def refuse(report, name, call, prefixes):
    try:
        call()
    except ValueError as error:
        message = str(error)
        F.need(message.startswith(prefixes), "WITHDRAWAL_UNRELATED_REFUSAL:"+name+":"+message)
        report["refusals"][name] = message
    else:
        raise ValueError("WITHDRAWAL_UNEXPECTED_SUCCESS:"+name)


async def run(context):
    p = deepcopy(dict(context.parameters))
    F.fields(p, {"schema", "runtime_adoption", "foundation", "workspace_path",
        "workspace_config", "operation_limits", "receipt", "bundle", "receipt_limits",
        "domain_path", "domain_id"})
    F.need(p["schema"] == "DMKN_V5_WITHDRAWAL_ACTUAL_V1", "WITHDRAWAL_ACTUAL_SCHEMA")
    F.need(p["receipt"]["sha256"] == RECEIPT and p["bundle"]["sha256"] == BUNDLE,
           "WITHDRAWAL_GENUINE_INPUT_PINS")
    F.need(p["receipt_limits"]["memory_mib"] <= context.limits["memory_mib"],
           "WITHDRAWAL_OUTER_MEMORY")
    workspace_path = ordinary(p["workspace_path"], fresh=True)
    domain_path = ordinary(p["domain_path"], fresh=True)
    work, run_path = ordinary(context.location_workspace), ordinary(context.run)
    F.need(work != run_path and work.is_relative_to(run_path), "WITHDRAWAL_OUTPUT_SCOPE")
    for target in (workspace_path, domain_path):
        for root in (context.installation, run_path, context.sources_owner,
                     context.sources_v5, context.sources_portable):
            root = ordinary(root)
            F.need(not target.is_relative_to(root) and not root.is_relative_to(target),
                   "WITHDRAWAL_DISJOINT_STATE")
    F.need(not domain_path.is_relative_to(workspace_path)
           and not workspace_path.is_relative_to(domain_path), "WITHDRAWAL_DISJOINT_DOMAIN")
    output = ordinary(work/"withdrawal-result.json", fresh=True, directory=False)
    F.need(time.monotonic() < context.deadline-5, "WITHDRAWAL_CLEANUP_MARGIN")
    workspace = client = None
    primary = cancelled = None
    report = {"schema": "DMKN_V5_WITHDRAWAL_ACTUAL_RESULT_V1", "status": "FAILED",
        "stage": "open", "error": None, "cleanup_errors": [], "client_closed": False,
        "workspace_closed": False, "refusals": {}, "proof_calls": 0,
        "authoring_calls": 0, "native_delta_calls": 0, "network_calls": 0,
        "new_mathematics": False, "full_v5_release": False}
    try:
        support = RuntimeProfile.support_manifest(context, p["runtime_adoption"])
        support_id = T.support_id(support)
        # Provisioning is an explicit one-time owner action, not startup recovery.
        T.TrustDomain.create(domain_path, p["domain_id"], support)
        domain = T.TrustDomain.open(domain_path, p["domain_id"], support_id)
        runtime = RuntimeProfile.from_context(context, p["runtime_adoption"], trust_domain=domain)
        operator = T.TrustDomain.open(domain_path, p["domain_id"], support_id)
        report["adoption"] = domain.identity()
        foundation = read_pin(p["foundation"], 16*MIB)
        receipt = read_pin(p["receipt"], MIB)
        bundle = C.parse_json(read_pin(p["bundle"], MIB))
        F.need(C.module_id(bundle["spec"]) == bundle["module"] == BASE,
               "WITHDRAWAL_BASE_SEMANTICS")
        summary = C.summarize(bundle["spec"])
        workspace = Workspace.open(workspace_path, p["workspace_config"], create=True)
        grant = workspace.reserve(p["operation_limits"], outer_deadline=context.deadline-5)
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=False,
            foundation_bytes=foundation, foundation_sha256=p["foundation"]["sha256"])
        report["stage"] = "one-genuine-receipt"
        token = client.admit_receipt(receipt, summary, **p["receipt_limits"])
        fact = client.describe(token)
        F.need(fact["kind"] == "I" and fact["live"]["module"] == BASE
               and fact["live"]["receipt_sha256"] == RECEIPT, "WITHDRAWAL_GENUINE_ACCEPTANCE")
        F.need(client.admit_receipt(receipt, summary, **p["receipt_limits"]) is token,
               "WITHDRAWAL_GENUINE_CACHE_PRIMED")
        # Read the existing original handle only for the direct-owner control.
        handle = client._warrants[token][1]
        report["before_withdrawal"] = client.report()
        F.need(report["before_withdrawal"]["receipt"]["attempts"] == 1
               and report["before_withdrawal"]["counts"]["same_live_hits"] == 1,
               "WITHDRAWAL_EXACT_RECEIPT_COUNT")
        report["stage"] = "apply-local-withdrawal"
        operator.withdraw("Selected local adoption withdrawn by operator integration control")
        refuse(report, "original_receipt_handle", lambda: client.receipt.describe(handle), ("TRUST_",))
        refuse(report, "aggregate_owner", lambda: client.aggregate._active(), ("TRUST_",))
        refuse(report, "cached_public_admission", lambda: client.admit_receipt(
            receipt, summary, **p["receipt_limits"]), ("TRUST_", "ADMISSION_CLOSED_OR_EXPIRED"))
        F.need(not client._warrants and not client._receipt_cache, "WITHDRAWAL_CACHE_NOT_CLEARED")
        closed = await client.close()
        report["client"] = closed
        F.need(closed["closed"] and closed["status"] == "FAILED"
               and closed["receipt"]["attempts"] == 1
               and closed["receipt"]["submitted_bytes"] == len(receipt)
               and closed["receipt"]["reserved_cpu_seconds"] == p["receipt_limits"]["cpu_seconds"]
               and closed["aggregate"]["attempts"] == closed["mixed"]["attempts"] == 0
               and all(closed[name]["closed"] for name in ("receipt", "aggregate", "mixed")),
               "WITHDRAWAL_CLEAN_CLOSED_DENIAL")
        report["client_closed"] = True
        grant2 = workspace.reserve(p["operation_limits"], outer_deadline=context.deadline-5)
        refuse(report, "new_operation", lambda: runtime.open_operation(workspace, grant2,
            mode="validated", authoring=False, foundation_bytes=foundation,
            foundation_sha256=p["foundation"]["sha256"]), ("TRUST_",))
        F.need(not grant2._used and workspace._client is None, "WITHDRAWAL_TRANSFER_ON_DENIAL")
        refuse(report, "new_profile", lambda: RuntimeProfile.from_context(
            context, p["runtime_adoption"], trust_domain=domain), ("TRUST_",))
        refuse(report, "reopen_existing_domain", lambda: T.TrustDomain.open(
            domain_path, p["domain_id"], support_id), ("TRUST_",))
        report.update(status="COMPLETED", stage="done")
    except BaseException as error:
        primary = error
        report["error"] = remote_reader._error(error)
        if isinstance(error, asyncio.CancelledError):
            cancelled = error
    finally:
        if client is not None and not report["client_closed"]:
            try:
                closed = await client.close()
                report["client"] = closed
                F.need(closed["closed"] and closed["status"] in ("CLOSED", "FAILED"),
                       "WITHDRAWAL_FAILURE_CLEANUP")
                report["client_closed"] = True
            except BaseException as error:
                report["cleanup_errors"].append({"component": "client", **remote_reader._error(error)})
                if isinstance(error, asyncio.CancelledError):
                    cancelled = error
        if workspace is not None:
            report["workspace_closed"] = _close_workspace(workspace, report["cleanup_errors"])
        if report["cleanup_errors"] or not report["client_closed"] or not report["workspace_closed"]:
            report["status"] = "FAILED"
        if time.monotonic() >= context.deadline:
            report["status"] = "FAILED"
            report["cleanup_errors"].append({"component": "deadline", "message": "ORIGINAL_DEADLINE"})
        try:
            remote_reader._save(output, report)
        except BaseException as error:
            if primary is not None:
                raise BaseExceptionGroup("Withdrawal and evidence write failed", [primary, error])
            raise
    if cancelled is not None:
        raise cancelled
    return report


def main(context):
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1

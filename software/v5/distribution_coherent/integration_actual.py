"""Installed adoption, ordinary owner lifetime and withdrawal integration.

Each action is a separate public installed launch. No mathematical fixture,
receipt admission, native checking, proof production or networking is invoked.
The saved result is evidence of local operations, never transferable authority.
"""
import asyncio
from copy import deepcopy
from importlib import import_module
from pathlib import Path
import time

from admission import trust as T
from client import remote_reader
from client.runtime import RuntimeProfile, read_pin
from client.serve_workspace import _close_workspace
from client.workspace_evidence import CONJUNCTION_SCHEMA
from client.workspace_validated import Workspace
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from discovery.module_export_adapter import compile_query
from modules import codec as C

MIB = 1024**2
SCHEMA = "DMKN_V5_DISTRIBUTION_COHERENT_INTEGRATION_V1"
RESULT_SCHEMA = "DMKN_V5_DISTRIBUTION_COHERENT_INTEGRATION_RESULT_V1"
SOURCES = {
    "admission/trust.py": "admission.trust",
    "admission/verifier.py": "admission.verifier",
    "aggregate_claims/aggregate_admission.py": "aggregate_claims.aggregate_admission",
    "client/runtime.py": "client.runtime",
    "client/remote_reader.py": "client.remote_reader",
    "discovery/formal_features.py": "discovery.formal_features",
    "discovery/authenticated_index.py": "discovery.authenticated_index",
    "discovery/discovery_store.py": "discovery.discovery_store",
    "discovery/module_export_adapter.py": "discovery.module_export_adapter",
    "client/workspace_evidence.py": "client.workspace_evidence",
    "client/workspace_atomic.py": "client.workspace_atomic",
    "client/direct_contacts.py": "client.direct_contacts",
    "mixed_claims/interface_projection.py": "mixed_claims.interface_projection",
}
FIELDS = {
    "adopt": {"schema", "action", "runtime_adoption", "domain_path", "domain_id"},
    "startup": {"schema", "action", "runtime_adoption", "foundation", "trust_domain",
        "workspace_path", "workspace_config", "operation_limits", "query_specs", "expected_sources"},
    "withdraw": {"schema", "action", "trust_domain"},
}


def _separate(context, value, *, fresh):
    path = ordinary(value, fresh=fresh)
    for root in (context.installation, context.run, context.sources_owner,
                 context.sources_v5, context.sources_portable):
        root = ordinary(root)
        F.need(not path.is_relative_to(root) and not root.is_relative_to(path),
               "COHERENT_STATE_DISJOINT_FROM_LAUNCH")
    return path


def _trust(context, value):
    F.fields(value, {"directory", "domain_id", "support_id"})
    path = _separate(context, value["directory"], fresh=False)
    return T.TrustDomain.open(path, value["domain_id"], value["support_id"])


def _inspect_sources(context, expected, runtime, client):
    F.fields(expected, SOURCES)
    root, described = ordinary(context.sources_v5), runtime.describe()
    records = {}
    for relative, name in SOURCES.items():
        wanted = C.digest_string(expected[relative])
        path = ordinary(root/relative, directory=False)
        F.need(context.source_sha256.get("v5/"+relative) == wanted,
               "COHERENT_LAUNCHER_SOURCE_PIN")
        module = import_module(name)
        F.need(Path(module.__file__).resolve() == path, "COHERENT_LOADED_SOURCE_ORIGIN")
        row = described["sources"].get(relative)
        F.need(row is not None and row["path"] == str(path) and row["sha256"] == wanted,
               "COHERENT_RUNTIME_SOURCE_PIN")
        read_pin(row, 2*MIB)
        short = {key: row[key] for key in ("bytes", "sha256")}
        for owner in (client.receipt, client.aggregate, client.delta):
            F.need(owner is not None and owner._pins.get(path) == short,
                   "COHERENT_REAL_ISSUER_SOURCE_PIN")
        F.need(client.preparation is not None and client.preparation._pins.get(str(path)) == row,
               "COHERENT_PREPARATION_SOURCE_PIN")
        records[relative] = {**row, "loaded_module": name}
    projection = root/"mixed_claims/interface_projection.py"
    row = records["mixed_claims/interface_projection.py"]
    F.need(client._source_pins.get(projection) == {key: row[key] for key in ("bytes", "sha256")},
           "COHERENT_RETAINED_INTERFACE_GUARD")
    return {"sources": records, "runtime_python_source_count": len(described["sources"]),
        "trust": described["trust"], "all_sources_in_real_owners": True,
        "interface_projection_in_client_guard": True}


def _no_work(value):
    F.need(value["calls"] == 0 and all(count == 0 for count in value["counts"].values())
        and all(value[name] is not None and value[name]["attempts"] == 0
                for name in ("receipt", "aggregate", "mixed"))
        and value["preparation"] is not None and value["preparation"]["calls"] == 0
        and value["preparation"]["worker_cpu_charge"] == 0
        and value["preparation"]["unknown_worker_accounting"] is False
        and all(value[name] is None for name in ("search", "location", "transport"))
        and not value["publications"] and not value["failures"],
        "COHERENT_NO_MATHEMATICAL_OR_NETWORK_WORK")


async def _close_client(client, report):
    closed = await client.close()
    report["client"] = closed
    F.need(closed["closed"] and closed["status"] == "CLOSED"
        and all(closed[name] is not None and closed[name]["closed"]
                for name in ("receipt", "aggregate", "mixed", "preparation")),
        "COHERENT_CLIENT_CLEANUP")
    _no_work(closed)
    report["client_closed"] = True


async def run(context):
    params = deepcopy(dict(context.parameters))
    F.need(type(params.get("action")) is str and params["action"] in FIELDS,
           "COHERENT_EXPLICIT_ACTION")
    action = params["action"]
    F.fields(params, FIELDS[action])
    F.need(params["schema"] == SCHEMA, "COHERENT_INTEGRATION_SCHEMA")
    work, run_path = ordinary(context.location_workspace), ordinary(context.run)
    F.need(work != run_path and work.is_relative_to(run_path), "COHERENT_OUTPUT_SCOPE")
    output = ordinary(work/"coherent-integration-result.json", fresh=True, directory=False)
    F.need(time.monotonic() < context.deadline-5, "COHERENT_CLEANUP_MARGIN")
    workspace = client = None
    primary = cancelled = None
    report = {"schema": RESULT_SCHEMA, "action": action, "status": "FAILED", "stage": "open",
        "error": None, "cleanup_errors": [], "client": None,
        "client_closed": False, "workspace_closed": False,
        "proof_calls": 0, "native_calls": 0, "network_calls": 0, "authoring_calls": 0,
        "mathematical_acceptance": False, "full_v5_release": False,
        "scope": "INSTALLED_TRUST_PAIR_PROFILE_AND_REAL_OWNER_INTEGRATION"}
    try:
        if action == "adopt":
            path = _separate(context, params["domain_path"], fresh=True)
            support = RuntimeProfile.support_manifest(context, params["runtime_adoption"])
            support_id = T.support_id(support)
            # Explicit provisioning in this action only. Ordinary startup cannot repair it.
            domain = T.TrustDomain.create(path, params["domain_id"], support)
            report["trust_domain"] = {"directory": str(path), "domain_id": params["domain_id"],
                                      "support_id": support_id}
            report["identity"] = domain.identity()
            report["support_roles"] = len(support["roles"])
        elif action == "withdraw":
            domain = _trust(context, params["trust_domain"])
            report["identity_before_withdrawal"] = domain.identity()
            domain.withdraw("Explicit installed integration withdrawal by the local owner")
            report["withdrawal_marker"] = str(Path(params["trust_domain"]["directory"])/"WITHDRAWN")
        else:
            F.fields(params["expected_sources"], SOURCES)
            F.need(params["workspace_config"]["schema"] == CONJUNCTION_SCHEMA,
                   "COHERENT_PAIRED_WORKSPACE_REQUIRED")
            path = _separate(context, params["workspace_path"], fresh=True)
            domain_path = Path(params["trust_domain"]["directory"])
            F.need(not path.is_relative_to(domain_path) and not domain_path.is_relative_to(path),
                   "COHERENT_DISJOINT_DOMAIN_AND_WORKSPACE")
            domain = _trust(context, params["trust_domain"])
            report["identity"] = domain.identity()
            runtime = RuntimeProfile.from_context(context, params["runtime_adoption"], trust_domain=domain)
            foundation = read_pin(params["foundation"], 16*MIB)
            workspace = Workspace.open(path, params["workspace_config"], create=True)
            namespace = workspace.adapter.namespace
            atomic = compile_query(namespace, params["query_specs"])
            paired = workspace.adapter.compile_query(params["query_specs"])
            F.need(len(atomic) == 2 and len(paired) == 1, "COHERENT_SELECTED_PAIR_COMPILED")
            report["query"] = {"namespace": namespace, "atomic": atomic, "compiled": paired}
            grant = workspace.reserve(params["operation_limits"], outer_deadline=context.deadline-5)
            report["operation_id"] = grant.identifier
            client = runtime.open_operation(workspace, grant, mode="validated", authoring=True,
                foundation_bytes=foundation, foundation_sha256=params["foundation"]["sha256"])
            report["stage"] = "installed-source-origins"
            report["installed_sources"] = _inspect_sources(context, params["expected_sources"], runtime, client)
            report["before_close"] = client.report()
            _no_work(report["before_close"])
            await _close_client(client, report)
            F.need(_close_workspace(workspace, report["cleanup_errors"]), "COHERENT_WORKSPACE_CLEANUP")
            report["workspace_closed"] = True
            workspace = None
            report["stage"] = "workspace-reopen"
            workspace = Workspace.open(path, params["workspace_config"])
            report["workspace_closed"] = False
            F.need(workspace.adapter.namespace == namespace
                and workspace.adapter.compile_query(params["query_specs"]) == paired,
                "COHERENT_REOPENED_PROFILE_CHANGED")
            status = workspace.status()
            F.need(status["schema"] == CONJUNCTION_SCHEMA and status["operations"] == {"CLOSED": 1}
                and not status["active_client"] and status["index"]["objects"] == 0,
                "COHERENT_REOPENED_WORKSPACE_STATE")
            report["reopened_workspace"] = status
        context.remaining_seconds()
        report.update(status="COMPLETED", stage="done")
    except BaseException as error:
        primary = error
        report["error"] = remote_reader._error(error)
        if isinstance(error, asyncio.CancelledError): cancelled = error
    finally:
        if client is not None and not report["client_closed"]:
            try:
                await _close_client(client, report)
            except BaseException as error:
                report["cleanup_errors"].append({"component": "client", **remote_reader._error(error)})
                if isinstance(error, asyncio.CancelledError): cancelled = error
        if workspace is not None:
            report["workspace_closed"] = _close_workspace(workspace, report["cleanup_errors"])
        if report["cleanup_errors"] or (action == "startup" and
            (not report["client_closed"] or not report["workspace_closed"])):
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        if report["finished"] >= context.deadline:
            report["status"] = "FAILED"
            report["cleanup_errors"].append({"component": "deadline", "message": "ORIGINAL_DEADLINE"})
        try:
            remote_reader._save(output, report)
        except BaseException as error:
            if primary is not None:
                raise BaseExceptionGroup("Integration and evidence write failed", [primary, error])
            raise
    if cancelled is not None: raise cancelled
    return report


def main(context):
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1

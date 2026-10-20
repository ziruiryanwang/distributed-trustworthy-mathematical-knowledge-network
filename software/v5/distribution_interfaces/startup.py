"""Installed source/pin and ordinary owner-lifetime integration only.

Trusted local run owner. No mathematics, authoring, proof, native or network
request is made. This adapter never constructs a substitute issuer or imports
test helpers, and its report is inert evidence, not mathematical authority.
"""
import asyncio
from copy import deepcopy
import hashlib
from importlib import import_module
from pathlib import Path
import time

from client import remote_reader
from client.runtime import RuntimeProfile, read_pin
from client.serve_workspace import _close_workspace
from client.workspace_validated import Workspace
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from modules import codec as C

MIB = 1024**2
SOURCES = {
    "mixed_claims/authoring_atomic.py": "mixed_claims.authoring_atomic",
    "mixed_claims/imports_atomic.py": "mixed_claims.imports_atomic",
    "mixed_claims/interface_projection.py": "mixed_claims.interface_projection",
    "client/workspace_evidence.py": "client.workspace_evidence",
    "client/workspace_staged.py": "client.workspace_staged",
    "client/semantic_reader.py": "client.semantic_reader",
    "transport/semantic_staging.py": "transport.semantic_staging",
    "transport/declaration_resilience.py": "transport.declaration_resilience",
}


def _inspect_sources(context, expected, runtime, client):
    F.fields(expected, SOURCES)
    root = ordinary(context.sources_v5)
    described = runtime.describe()
    records = {}
    for relative, module_name in SOURCES.items():
        wanted = expected[relative]
        C.digest_string(wanted)
        F.need(context.source_sha256.get("v5/" + relative) == wanted,
               "INTERFACE_STARTUP_LAUNCHER_SOURCE_PIN")
        module = import_module(module_name)
        path = ordinary(root / relative, directory=False)
        F.need(Path(module.__file__).resolve() == path,
               "INTERFACE_STARTUP_LOADED_SOURCE_ORIGIN")
        row = described["sources"].get(relative)
        F.need(row is not None and row["path"] == str(path) and row["sha256"] == wanted,
               "INTERFACE_STARTUP_RUNTIME_SOURCE_PIN")
        # Source bytes are small; no binary/proof campaign is performed here.
        read_pin(row, 2*MIB)
        short = {key: row[key] for key in ("bytes", "sha256")}
        for owner in (client.receipt, client.aggregate, client.delta):
            if owner is not None:
                F.need(owner._pins.get(path) == short,
                       "INTERFACE_STARTUP_CONCRETE_ISSUER_SOURCE_PIN")
        F.need(client.preparation._pins.get(str(path)) == row,
               "INTERFACE_STARTUP_CONCRETE_PREPARATION_SOURCE_PIN")
        records[relative] = {**row, "loaded_module": module_name}
    projection = root / "mixed_claims/interface_projection.py"
    projection_row = records["mixed_claims/interface_projection.py"]
    F.need(client._source_pins.get(projection) == {
        key: projection_row[key] for key in ("bytes", "sha256")},
        "INTERFACE_STARTUP_CLIENT_PROJECTION_PIN")
    return {"sources": records, "runtime_python_source_count": len(described["sources"]),
        "profile_sha256": hashlib.sha256(C.canonical(described)).hexdigest(),
        "projection_in_client_guard": True, "all_sources_in_real_owners": True}


def _no_work(report):
    F.need(report["calls"] == 0 and all(value == 0 for value in report["counts"].values())
           and all(report[name] is None or report[name]["attempts"] == 0
                   for name in ("receipt", "aggregate", "mixed"))
           and report["aggregate"] is not None and report["mixed"] is not None
           and report["preparation"] is not None
           and report["preparation"]["calls"] == 0
           and report["preparation"]["worker_cpu_charge"] == 0
           and report["preparation"]["unknown_worker_accounting"] is False
           and all(report[name] is None for name in ("search", "location", "transport"))
           and not report["publications"] and not report["failures"],
           "INTERFACE_STARTUP_ZERO_MATHEMATICAL_AND_NETWORK_CALLS")


async def run(context):
    params = deepcopy(dict(context.parameters))
    F.fields(params, {"schema", "runtime_adoption", "foundation", "workspace_path",
        "workspace_config", "operation_limits", "expected_sources"})
    F.need(params["schema"] == "DMKN_V5_DISTRIBUTION_INTERFACE_STARTUP_V1",
           "INTERFACE_STARTUP_SCHEMA")
    F.fields(params["expected_sources"], SOURCES)
    workspace_path = ordinary(params["workspace_path"], fresh=True)
    work = ordinary(context.location_workspace)
    run_path = ordinary(context.run)
    F.need(work != run_path and work.is_relative_to(run_path), "INTERFACE_STARTUP_OUTPUT_SCOPE")
    for root in (context.installation, run_path, context.sources_owner,
                 context.sources_v5, context.sources_portable):
        root = ordinary(root)
        F.need(not workspace_path.is_relative_to(root) and not root.is_relative_to(workspace_path),
               "INTERFACE_STARTUP_DISJOINT_WORKSPACE")
    output = ordinary(work / "interface-startup-result.json", fresh=True, directory=False)
    F.need(time.monotonic() < context.deadline - 5, "INTERFACE_STARTUP_CLEANUP_MARGIN")
    workspace = client = None
    primary = cancelled = None
    report = {"schema": "DMKN_V5_DISTRIBUTION_INTERFACE_STARTUP_RESULT_V1", "status": "FAILED",
        "stage": "open", "error": None, "cleanup_errors": [], "client_closed": False,
        "workspace_closed": False, "client": None, "mathematical_acceptance": False,
        "full_v5_release": False, "scope": "INSTALLED_SOURCE_PINS_AND_REAL_OWNER_LIFETIME_ONLY"}
    try:
        runtime = RuntimeProfile.from_context(context, params["runtime_adoption"])
        foundation = read_pin(params["foundation"], 16*MIB)
        workspace = Workspace.open(workspace_path, params["workspace_config"], create=True)
        grant = workspace.reserve(params["operation_limits"], outer_deadline=context.deadline - 5)
        report["operation_id"] = grant.identifier
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=True,
            foundation_bytes=foundation, foundation_sha256=params["foundation"]["sha256"])
        report["stage"] = "inspect-installed-source-origins"
        report["installed_sources"] = _inspect_sources(
            context, params["expected_sources"], runtime, client)
        report["before_close"] = client.report()
        _no_work(report["before_close"])
        context.remaining_seconds()
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
                       "INTERFACE_STARTUP_CLIENT_CLEANUP")
                _no_work(closed)
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
                raise BaseExceptionGroup("Startup and evidence write failed", [primary, error])
            raise
    if cancelled is not None:
        if primary is not None and primary is not cancelled:
            raise BaseExceptionGroup("Startup failed; cleanup cancelled", [primary, cancelled])
        raise cancelled
    return report


def main(context):
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1

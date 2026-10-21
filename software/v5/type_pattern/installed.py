"""One ordinary installed-run boundary; no mathematical runtime or networking.

The launcher supplies real installed modules and exact copied-source bindings.
This owner checks seven changed origins, compiles a local query, and reopens a
fresh empty structural workspace. It never creates an issuer or operation grant.
"""
from copy import deepcopy
import hashlib
from importlib import import_module
import os
from pathlib import Path
import time

from client.workspace_validated import Workspace
from client.workspace_evidence import TYPE_PATTERN_SCHEMA
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from discovery.module_export_adapter import PATTERN_PROFILE_SCHEMA
from discovery.type_pattern import pattern_spec
from modules import codec as C

MIB = 1024**2
SCHEMA = "DMKN_V5_INSTALLED_DISCOVERY_BOUNDARY_V1"
RESULT_SCHEMA = "DMKN_V5_INSTALLED_DISCOVERY_BOUNDARY_RESULT_V1"
SOURCES = {
    "modules/source_rows.py": "modules.source_rows",
    "discovery/formal_features.py": "discovery.formal_features",
    "discovery/module_export_adapter.py": "discovery.module_export_adapter",
    "discovery/type_pattern.py": "discovery.type_pattern",
    "discovery/authenticated_index.py": "discovery.authenticated_index",
    "discovery/discovery_store.py": "discovery.discovery_store",
    "client/workspace_evidence.py": "client.workspace_evidence",
}


def _error(error):
    return {"type": type(error).__name__, "message": str(error)[:2000]}


def _sources(context, expected):
    F.fields(expected, SOURCES)
    root = ordinary(context.sources_v5)
    result = {}
    for relative, name in SOURCES.items():
        row = expected[relative]
        F.fields(row, {"bytes", "sha256"})
        F.uint(row["bytes"], 1, 2*MIB)
        wanted = C.digest_string(row["sha256"])
        F.need(context.source_sha256.get("v5/"+relative) == wanted,
               "INSTALLED_DISCOVERY_LAUNCHER_SOURCE_PIN")
        path = ordinary(root/relative, directory=False)
        module = import_module(name)
        F.need(Path(module.__file__).resolve() == path,
               "INSTALLED_DISCOVERY_LOADED_SOURCE_ORIGIN")
        F.need(path.stat().st_size == row["bytes"], "INSTALLED_DISCOVERY_SOURCE_SIZE")
        with path.open("rb") as stream:
            raw = stream.read(row["bytes"]+1)
        F.need(len(raw) == row["bytes"] and path.stat().st_size == row["bytes"]
               and hashlib.sha256(raw).hexdigest() == wanted,
               "INSTALLED_DISCOVERY_SOURCE_BYTES")
        result[relative] = {**row, "path": str(path), "loaded_module": name}
        context.remaining_seconds()
    return result


def _state_path(context, value):
    path = ordinary(value, fresh=True)
    for value in (context.installation, context.run, context.sources_owner,
                  context.sources_v5, context.sources_portable):
        root = ordinary(value)
        F.need(not path.is_relative_to(root) and not root.is_relative_to(path),
               "INSTALLED_DISCOVERY_STATE_DISJOINT")
    return path


def _local_query():
    # All input symbols are this local template's own names. No target record,
    # remote ModuleID or theorem name is accepted as a query-generation input.
    owner = "11" * 32
    names = lambda text: [["s", text]]
    T = ["const", ["local", names("T")], []]
    f = ["const", ["local", names("f")], []]
    x = ["bvar", 0]
    app = lambda fn, arg: ["app", fn, arg]
    eq = ["const", ["foundation", names("Eq")], [["succ", ["zero"]]]]
    law = ["forall", "default", T, app(app(app(eq, T), app(f, app(f, x))), x)]
    spec = pattern_spec(C, owner, 0, law)
    return {"local_template_owner": owner, "universes": 0, "type": law,
            "specs": [{"tag": "declaration-kind", "value": "theorem"}, spec],
            "remote_identity_used": False, "mathematical_acceptance": False}


def _empty(workspace):
    status = workspace.status()
    F.need(status["schema"] == TYPE_PATTERN_SCHEMA and status["operations"] == {}
           and not status["active_client"] and status["index"]["objects"] == 0
           and status["mathematical_acceptance"] is False,
           "INSTALLED_DISCOVERY_EMPTY_STRUCTURAL_WORKSPACE")
    return status


def main(context):
    params = deepcopy(dict(context.parameters))
    F.fields(params, {"schema", "workspace_path", "workspace_config", "expected_sources"})
    F.need(params["schema"] == SCHEMA, "INSTALLED_DISCOVERY_REQUEST_SCHEMA")
    F.need(type(params["workspace_config"]) is dict
           and params["workspace_config"].get("schema") == TYPE_PATTERN_SCHEMA
           and params["workspace_config"].get("discovery_profile") ==
               {"schema": PATTERN_PROFILE_SCHEMA}, "INSTALLED_DISCOVERY_PATTERN_CONFIG")
    work, run = ordinary(context.location_workspace), ordinary(context.run)
    F.need(work != run and work.is_relative_to(run), "INSTALLED_DISCOVERY_OUTPUT_SCOPE")
    output = ordinary(work/"discovery-installed-result.json", fresh=True, directory=False)
    F.need(time.monotonic() < context.deadline-5, "INSTALLED_DISCOVERY_CLEANUP_MARGIN")
    workspace = None
    report = {"schema": RESULT_SCHEMA, "status": "FAILED", "stage": "source-origins",
        "deadline": context.deadline,
        "scope": "INSTALLED_CHANGED_SOURCES_QUERY_AND_EMPTY_WORKSPACE_REOPEN",
        "error": None, "cleanup_errors": [], "workspace_closed": False,
        "proof_calls": 0, "native_calls": 0, "network_calls": 0,
        "runtime_profiles_created": 0, "issuers_created": 0, "operation_grants": 0,
        "mathematical_acceptance": False, "full_v5_release": False}
    try:
        report["installed_sources"] = _sources(context, params["expected_sources"])
        path = _state_path(context, params["workspace_path"])
        query = _local_query()
        report["stage"] = "fresh-pattern-workspace"
        workspace = Workspace.open(path, params["workspace_config"], create=True)
        namespace = workspace.adapter.namespace
        keys = workspace.adapter.compile_query(query["specs"])
        F.need(len(keys) == 2 and keys == sorted(set(keys)), "INSTALLED_DISCOVERY_QUERY_KEYS")
        report["query"] = {**query, "namespace": namespace, "compiled": keys}
        report["created_workspace"] = _empty(workspace)
        workspace.close()
        F.need(workspace._closed, "INSTALLED_DISCOVERY_FIRST_CLOSE")
        workspace = None
        report["workspace_closed"] = True
        context.remaining_seconds()
        report["stage"] = "pattern-workspace-reopen"
        workspace = Workspace.open(path, params["workspace_config"])
        report["workspace_closed"] = False
        F.need(workspace.adapter.namespace == namespace
               and workspace.adapter.compile_query(query["specs"]) == keys,
               "INSTALLED_DISCOVERY_REOPENED_PROFILE_CHANGED")
        report["reopened_workspace"] = _empty(workspace)
        report["workspace_path"] = str(path)
        context.remaining_seconds()
        report.update(status="COMPLETED", stage="done")
    except BaseException as error:
        report["error"] = _error(error)
    finally:
        if workspace is not None:
            try:
                workspace.close()
                F.need(workspace._closed, "INSTALLED_DISCOVERY_FINAL_CLOSE")
                report["workspace_closed"] = True
            except BaseException as error:
                report["cleanup_errors"].append(_error(error))
        report["finished"] = time.monotonic()
        if report["cleanup_errors"] or not report["workspace_closed"] or report["finished"] >= context.deadline:
            report["status"] = "FAILED"
        raw = C.canonical(report)
        F.need(len(raw) <= MIB, "INSTALLED_DISCOVERY_REPORT_BOUND")
        with output.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    return 0 if report["status"] == "COMPLETED" else 1

"""One synchronous installed import boundary; no algorithm or service workload.

The ordinary launcher supplies the real source whitelist, copied modules and
original bounded Job. This trusted owner imports nine selected SDK modules and
checks their origins/bytes. No overlay, store, mathematical owner, query,
event loop, native/proof worker, socket or location process is created here.
"""
from copy import deepcopy
import hashlib
from importlib import import_module
import os
from pathlib import Path
import time

from discovery import formal_features as F
from discovery.discovery_store import ordinary
from modules import codec as C

MIB = 1024**2
SCHEMA = "DMKN_V5_INSTALLED_PROJECTION_IMPORT_V1"
RESULT_SCHEMA = "DMKN_V5_INSTALLED_PROJECTION_IMPORT_RESULT_V1"
SOURCES = {
    "client/workspace_evidence.py": "client.workspace_evidence",
    "discovery/authenticated_index.py": "discovery.authenticated_index",
    "discovery/discovery_store.py": "discovery.discovery_store",
    "discovery/formal_features.py": "discovery.formal_features",
    "discovery/module_export_adapter.py": "discovery.module_export_adapter",
    "client/serve_workspace.py": "client.serve_workspace",
    "client/serve_advertised.py": "client.serve_advertised",
    "discovery/conclusion_fingerprint.py": "discovery.conclusion_fingerprint",
    "client/base_projection.py": "client.base_projection",
}


def _error(error):
    return {"type": type(error).__name__, "message": str(error)[:2000]}


def _expectations(value):
    F.fields(value, SOURCES)
    for row in value.values():
        F.fields(row, {"bytes", "sha256"})
        F.uint(row["bytes"], 1, 2*MIB)
        C.digest_string(row["sha256"])


def _sources(context, expected, report):
    root = ordinary(context.sources_v5)
    for relative, name in SOURCES.items():
        context.remaining_seconds()
        report["current_source"] = relative
        row = expected[relative]
        wanted = row["sha256"]
        F.need(context.source_sha256.get("v5/"+relative) == wanted,
               "INSTALLED_PROJECTION_LAUNCHER_SOURCE_PIN")
        path = ordinary(root/relative, directory=False)
        module = import_module(name)
        F.need(Path(module.__file__).resolve() == path,
               "INSTALLED_PROJECTION_LOADED_SOURCE_ORIGIN")
        F.need(path.stat().st_size == row["bytes"], "INSTALLED_PROJECTION_SOURCE_SIZE")
        with path.open("rb") as stream:
            raw = stream.read(row["bytes"]+1)
        F.need(len(raw) == row["bytes"] and path.stat().st_size == row["bytes"]
               and hashlib.sha256(raw).hexdigest() == wanted,
               "INSTALLED_PROJECTION_SOURCE_BYTES")
        report["installed_sources"][relative] = {**row, "path": str(path), "loaded_module": name}
        context.remaining_seconds()
    report["current_source"] = None


def main(context):
    params = deepcopy(dict(context.parameters))
    F.fields(params, {"schema", "expected_sources"})
    F.need(params["schema"] == SCHEMA, "INSTALLED_PROJECTION_REQUEST_SCHEMA")
    _expectations(params["expected_sources"])
    work, run = ordinary(context.location_workspace), ordinary(context.run)
    F.need(work != run and work.is_relative_to(run), "INSTALLED_PROJECTION_OUTPUT_SCOPE")
    output = ordinary(work/"projection-installed-result.json", fresh=True, directory=False)
    F.need(time.monotonic() < context.deadline-5, "INSTALLED_PROJECTION_REPORT_MARGIN")
    report = {"schema": RESULT_SCHEMA, "status": "FAILED", "stage": "source-census",
        "started": time.monotonic(), "deadline": context.deadline, "error": None,
        "sdk_sources": None, "owner_sources": None, "total_sources": None,
        "current_source": None, "installed_sources": {},
        "scope": "INSTALLED_NINE_MODULE_WHITELIST_ORIGINS_AND_BYTES_ONLY",
        "evidence_limit": "NO_ALGORITHM_EXECUTION_OR_HOSTILE_LOADER_QUALIFICATION",
        "stores_created": 0, "runtime_profiles_created": 0, "issuers_created": 0,
        "trust_domains_created": 0, "operation_grants": 0, "query_calls": 0,
        "proof_calls": 0, "native_calls": 0, "network_calls": 0,
        "mathematical_acceptance": False, "full_v5_release": False}
    try:
        selected = set(context.source_sha256)
        sdk = {name for name in selected if name.startswith(("v5/", "portable/"))}
        owner = {name for name in selected if name.startswith("owner/")}
        report.update(sdk_sources=len(sdk), owner_sources=len(owner), total_sources=len(selected))
        F.need(len(sdk) == 113 and len(owner) == 1 and len(selected) == 114
               and selected == sdk | owner, "INSTALLED_PROJECTION_SOURCE_CENSUS")
        report["stage"] = "source-origins"
        _sources(context, params["expected_sources"], report)
        F.need(set(report["installed_sources"]) == set(SOURCES), "INSTALLED_PROJECTION_NINE_ORIGINS")
        context.remaining_seconds()
        report.update(status="COMPLETED", stage="done")
    except BaseException as error:
        report["error"] = _error(error)
    finally:
        report["finished"] = time.monotonic()
        if report["finished"] >= context.deadline:
            report["status"] = "FAILED"
            report["deadline_exceeded"] = True
        raw = C.canonical(report)
        F.need(len(raw) <= 65536, "INSTALLED_PROJECTION_REPORT_BOUND")
        with output.open("xb") as stream:
            F.need(stream.write(raw) == len(raw), "INSTALLED_PROJECTION_REPORT_SHORT_WRITE")
            stream.flush()
            os.fsync(stream.fileno())
    return 0 if report["status"] == "COMPLETED" else 1

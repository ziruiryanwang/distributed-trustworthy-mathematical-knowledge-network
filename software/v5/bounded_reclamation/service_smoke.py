"""One real empty service close and fresh-fixture reclamation; root launch only.

No existing state is enrolled. The fixed UTC lower bound is an explicit local
owner premise, not a time-synchronization result. No mathematical work is done.
"""
import time
STARTED = time.monotonic()
OUTER = STARTED + 170
import argparse
import asyncio
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import socket
import sys
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
INSTALL = PROJECT/"product-local/v5-distribution-consolidated-01/Mathematical Commons v5"
SNAPSHOT = Path(__file__).resolve().parents[3]
RELEASE = "1fd0ae63faa84cc1f3ef82f17d2056657f8d6a3e5dea3686ace433987bd1e5be"
BASIS = PROJECT/"experiments/v5-local-checks/placement-network-integration-02-input.json"
BASIS_SHA = "6e14ba3b8abbce616a8115b7ce3a229242869a3b8861c427c52e3221a2f47f58"
MIB = 1024**2
CLOCK_LOWER = 1577836800000  # Explicit owner premise: UTC is already past 2020-01-01.
EXTRA = {
    "v5/placement/lifecycle.py": "software/v5/bounded_reclamation/placement/lifecycle.py",
    "v5/placement/reclaim.py": "software/v5/bounded_reclamation/placement/reclaim.py",
    "v5/client/serve_generations.py": "software/v5/bounded_generations/client/serve_generations.py",
}


def need(value, why):
    if not value: raise ValueError(why)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(raw): return hashlib.sha256(raw).hexdigest()


def ordinary(path, *, directory=False):
    path = Path(path)
    need(path.is_absolute() and path.resolve() == path and all(
        not p.is_symlink() and not p.is_junction() for p in (path, *path.parents)), "SMOKE_ORDINARY_PATH")
    need(path.is_dir() if directory else path.is_file(), "SMOKE_PATH_KIND")
    return path


def read(path, digest, maximum=2*MIB):
    path = ordinary(path)
    need(path.stat().st_size <= maximum, "SMOKE_INPUT_SIZE")
    with path.open("rb") as stream: raw = stream.read(maximum+1)
    need(len(raw) <= maximum and sha(raw) == digest, "SMOKE_INPUT_PIN")
    return raw


def save(path, value):
    raw = encode(value)+b"\n"; need(len(raw) <= MIB, "SMOKE_REPORT_SIZE")
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "SMOKE_SHORT_REPORT")
        stream.flush(); os.fsync(stream.fileno())


def error_fields(error):
    code = str(error)
    return dict(error_type=type(error).__name__,
        error_code=code if re.fullmatch(r"[A-Z][A-Z0-9_]{0,127}", code) else "SMOKE_OPERATION_FAILED")


def adopt(request):
    need(set(request) == {"schema", "additions"} and request["schema"] ==
         "DMKN_BOUNDED_RECLAMATION_SERVICE_INPUT_V1", "SMOKE_INPUT_SCHEMA")
    need(type(request["additions"]) is dict and set(request["additions"]) == set(EXTRA), "SMOKE_EXACT_ADDITIONS")
    release = json.loads(read(INSTALL/"V5-RELEASE.json", RELEASE, 8*MIB))
    need(release["schema"] == "DMKN_V5_DIRECTORY_RELEASE_V3" and len(release["sdk_sources"]) == 121,
         "SMOKE_INSTALLED_MAP")
    need(Path(sys.executable).resolve() == INSTALL/"base/receiver/runtime/python/python.exe", "SMOKE_INSTALLED_PYTHON")
    selected = {}
    for logical, relative in release["sdk_sources"].items():
        need(relative == "sdk/"+logical and "\\" not in relative and
             all(p not in (".", "..", "") for p in PurePosixPath(relative).parts), "SMOKE_SDK_PATH")
        row = release["files"][relative]; path = INSTALL/relative
        raw = read(path, row["sha256"]); need(len(raw) == row["bytes"], "SMOKE_SDK_EXTENT")
        selected[logical] = dict(path=str(path), bytes=len(raw), sha256=row["sha256"])
    for logical, relative in EXTRA.items():
        row = request["additions"][logical]
        need(type(row) is dict and set(row) == {"bytes", "sha256"} and logical not in selected,
             "SMOKE_NEW_LOGICAL_SOURCE")
        path = SNAPSHOT/relative; raw = read(path, row["sha256"])
        need(len(raw) == row["bytes"], "SMOKE_ADDITION_EXTENT")
        selected[logical] = dict(path=str(path), **row)
    prefixes = {PurePosixPath(logical).parts[1] for logical in selected}
    need(not any(name.split(".")[0] in prefixes for name in sys.modules), "SMOKE_EARLY_PRODUCT_IMPORT")
    sys.path[:0] = [str(INSTALL/"sdk/v5"), str(INSTALL/"sdk/portable")]
    # Bind exact reviewed modules; namespace package paths remain installed.
    for name, logical in (("placement.reclaim", "v5/placement/reclaim.py"),
                          ("placement.lifecycle", "v5/placement/lifecycle.py"),
                          ("client.serve_generations", "v5/client/serve_generations.py")):
        __import__(name.split(".")[0])
        spec = importlib.util.spec_from_file_location(name, selected[logical]["path"])
        module = importlib.util.module_from_spec(spec); sys.modules[name] = module
        spec.loader.exec_module(module)
    basis = json.loads(read(BASIS, BASIS_SHA))
    need(basis["schema"] == "DMKN_PLACEMENT_NETWORK_INTEGRATION_INPUT_V1", "SMOKE_WORKSPACE_BASIS")
    return selected, deepcopy(basis["workspace_config"])


def rebind(selected):
    read(INSTALL/"V5-RELEASE.json", RELEASE, 8*MIB); read(BASIS, BASIS_SHA)
    paths = {Path(row["path"]) for row in selected.values()}
    prefixes = {PurePosixPath(logical).parts[1] for logical in selected}
    origins = {}
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] not in prefixes: continue
        origin = getattr(module, "__file__", None)
        if origin is None:
            namespaces = getattr(module, "__path__", ())
            need(namespaces and all(Path(p).is_relative_to(INSTALL/"sdk") for p in namespaces),
                 "SMOKE_NAMESPACE_ORIGIN")
            continue
        need(ordinary(origin) in paths, "SMOKE_PRODUCT_ORIGIN")
        origins[name] = str(Path(origin))
    for row in selected.values():
        need(len(read(row["path"], row["sha256"])) == row["bytes"], "SMOKE_FINAL_EXTENT")
    return origins


def ports():
    held = []
    try:
        for unused in range(6):
            stream = socket.socket(); held.append(stream); stream.bind(("127.0.0.1", 0))
        values = [stream.getsockname()[1] for stream in held]
        need(len(set(values)) == 6, "SMOKE_DISTINCT_PORTS")
        return values
    finally:
        for stream in held: stream.close()


def pending():
    return sum(not task.done() and task is not asyncio.current_task() for task in asyncio.all_tasks())


async def scenario(output, selected, workspace_config, report):
    from placement.lifecycle import ManagedGenerations, SCHEMA
    from client.serve_generations import GenerationServices
    from client.workspace_evidence import CONCLUSION_FINGERPRINT_SCHEMA
    from placement import codec as P
    from modules import codec as C
    from aggregate_claims import bindings as B
    from discovery.module_export_adapter import ModuleExportAdapter
    from evidence_network.custody import profile_id
    from location.controller import SOURCE_NAMES
    from location.controller_services import ROLE_NAMES

    numbers = ports(); endpoint = lambda port:dict(host="127.0.0.1", port=port, tls=False, server_name=None)
    egress = dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
                  test_endpoints=[dict(host="127.0.0.1", port=port) for port in sorted(numbers)])
    config = dict(schema=SCHEMA, epoch=sha(str(output).encode()),
        clock_model_id=sha(b"OWNER_PREMISE_UTC_AFTER_2020_FINITE_LOCAL_LIFECYCLE_TEST"),
        registry_pages=256, owner_reserved_bytes=36*MIB, registry_reserved_bytes=2*MIB,
        cleanup_reserved_bytes=2*MIB, protected_roots=[str(INSTALL), str(PROJECT/"software"),
            str(PROJECT/"research"), str(output/"sources")], slots=[dict(reserved_bytes=16*MIB,
                max_cells=1, max_runs=1, read_endpoint=endpoint(numbers[3*i]),
                intake_endpoint=endpoint(numbers[3*i+1]), listen=[f"/ip4/127.0.0.1/tcp/{numbers[3*i+2]}"])
                for i in range(2)])
    workspace_config.update(schema=CONCLUSION_FINGERPRINT_SCHEMA,
        discovery_profile=dict(schema="DMKN_MODULE_EXPORT_CONCLUSION_FINGERPRINT_PROFILE_V1", paths=[[]]))
    adapter = ModuleExportAdapter(C, B.FOUNDATION, B.POLICY, discovery_profile=workspace_config["discovery_profile"])
    limits = dict(lifetime_seconds=60, controller_cpu_seconds=40, controller_calls=16,
        health_interval_ms=30000, journal_pages=256,
        read=dict(max_connections=1, max_requests=2, max_reply_bytes=MIB, operation_ms=5000),
        intake=dict(max_connections=1, max_requests=2, incoming_bytes=25600, outgoing_bytes=90112, operation_ms=5000))
    location_limits = dict(service_ms=150000, operation_ms=10000, query_events=64, provider_limit=1,
        advertised_keys=1, provider_ttl_ms=120000, reprovide_interval_ms=30000, maintenance_ms=60000,
        commands=16, descriptor_requests=2, descriptor_reply_bytes=16384, metadata={},
        transport=dict(outbound_attempts=2, inbound_upgrades=2, receive_bytes=MIB, send_bytes=MIB))
    def generation(slot):
        spec = config["slots"][slot]
        return dict(workspace=deepcopy(workspace_config), service_limits=deepcopy(limits), egress=deepcopy(egress),
            placement=dict(schema=P.CONFIG_SCHEMA, service_epoch=config["epoch"], namespace=adapter.namespace,
                wire_profile_id=profile_id(workspace_config["wire_profile"]), admission_close_ms=CLOCK_LOWER-2000,
                retention_not_after_ms=CLOCK_LOWER-1000, max_grants=1, max_requests=1, max_cells=1,
                max_runs=1, ledger_pages=256, limits={key:1 for key in P.RESOURCES}),
            location=dict(schema="DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", role="index-provider",
                namespace=adapter.namespace, egress=deepcopy(egress), listen=spec["listen"], announce=[],
                bootstrap=[], endpoints=[spec["read_endpoint"]], limits=deepcopy(location_limits)))
    runtime = dict(source_root=str(INSTALL/"sdk/portable/location"), installation_root=str(INSTALL/"base"),
        source_pins={name:selected["portable/location/"+name]["sha256"] for name in SOURCE_NAMES},
        role_pins={name:selected["portable/location/"+name]["sha256"] for name in ROLE_NAMES})
    manager = services = service = primary = None
    report.update(stage="create-manager", cleanup_errors=[], deletion_events=[])
    try:
        manager = ManagedGenerations.open(output/"managed", config, create=True, deadline=OUTER, calls=128, cpu_seconds=60)
        first = manager.allocate(0, generation(0)); other = manager.allocate(1, generation(1))
        root = manager.generation_path(first); other_path = manager.generation_path(other)
        other_marker = (other_path/"generation.json").read_bytes()
        need(root.is_relative_to(output/"managed/slot-0") and root.parent.parent == manager.root,
             "SMOKE_FRESH_GENERATION_SCOPE")
        services = GenerationServices(manager, runtime)
        report["stage"] = "real-service-start"
        report["ready"] = await services.start_slot(first["generation"], outer_deadline=OUTER,
                                                    location_deadline=STARTED+140)
        service = services.service(first["generation"])
        report["node_ready"] = service.location._start_task.result()
        need(service.workspace.index.status()["objects"] == 0, "SMOKE_EMPTY_SERVICE")
        for table in ("requests", "grants", "cells"):
            need(service.ledger.db.execute("SELECT count(*) FROM "+table).fetchone()[0] == 0, "SMOKE_NO_PROMISES_OR_REQUESTS")
        clock = manager.adopt_clock(lower_utc_ms=CLOCK_LOWER, valid_for_ms=120000, rate_error_ppm=10000,
                                    model_id=config["clock_model_id"])
        report["stage"] = "real-retirement-and-close"
        retired = await services.retire_slot(first["generation"], clock)
        report["retired"] = retired; report["service_close"] = service.report()
        need(retired["phase"] == "RETIRED" and retired["run_state"] == "CLOSED" and retired["runs"] == 1
             and "closure_sha256" in retired and not manager._handles, "SMOKE_REAL_DURABLE_CLOSURE")
        need(service.report()["status"] == "CLOSED" and service.location.process.returncode == 0
             and service._close_task.done() and service.location._close_task.done(), "SMOKE_REAL_ACTORS_CLOSED")
        report["stage"] = "reclaim-exact-fresh-generation"
        profile = dict(layout="DMKN_V5_CLOSED_GENERATION_LAYOUT_V1",
            ownership="PRIVATE_ENROLLED_NO_OTHER_WRITERS_OR_RESTORES_V1", max_calls=2,
            max_entries_per_call=64, max_apparent_bytes=16*MIB)
        report["reclaim_begin"] = manager.begin_reclamation(first["generation"], profile)
        def guard_delete(original, kind):
            def checked(path, *args, **kwargs):
                target = Path(path)
                need(not args and not kwargs and target.is_absolute() and (target == root or target.is_relative_to(root))
                     and target != manager.root and target != output, "SMOKE_EXACT_ENROLLED_DELETE_ONLY")
                ordinary(target, directory=kind == "rmdir")
                result = original(target)
                report["deletion_events"].append(dict(kind=kind, relative=target.relative_to(root).as_posix()))
                need(len(report["deletion_events"]) <= 29, "SMOKE_DELETION_COUNT")
                return result
            return checked
        with ExitStack() as guards:
            guards.enter_context(patch.object(os, "unlink", guard_delete(os.unlink, "unlink")))
            guards.enter_context(patch.object(os, "rmdir", guard_delete(os.rmdir, "rmdir")))
            report["reclaim_step"] = manager.reclaim_step(first["generation"], max_entries=64, deadline=OUTER)
        state = manager.status()
        need(state["slots"][0] is None and not os.path.lexists(root), "SMOKE_ABSENT_BEFORE_REUSE")
        need(state["slots"][1] == other and (other_path/"generation.json").read_bytes() == other_marker,
             "SMOKE_OTHER_SLOT_PRESERVED")
        replacement = manager.allocate(0, generation(0))
        need(replacement["sequence"] == 3 and replacement["generation"] != first["generation"], "SMOKE_NEW_IDENTITY")
        try: manager.reserve_run(first["generation"], outer_deadline=OUTER)
        except ValueError as error: need(str(error) == "GENERATIONS_NOT_CURRENTLY_REGISTERED", "SMOKE_OLD_ID_REFUSAL")
        else: raise ValueError("SMOKE_OLD_ID_RESURRECTED")
        report.update(replacement=replacement, final_state=manager.status(), exact_reclaimed_root=str(root),
                      real_closed_run_tested=True, slot_reused=True, other_slot_preserved=True, stage="complete")
    except BaseException as error:
        primary = error
        raise
    finally:
        if services is not None:
            try:
                for result in await services.close():
                    if isinstance(result, BaseException): report["cleanup_errors"].append(error_fields(result))
            except BaseException as error: report["cleanup_errors"].append(error_fields(error))
        if manager is not None:
            try: manager.close()
            except BaseException as error: report["cleanup_errors"].append(error_fields(error))
        report["pending_before_settlement"] = pending()
        await asyncio.sleep(0)
        report["pending_after_settlement"] = pending()
        for valid, code in ((not report["cleanup_errors"] and report["pending_after_settlement"] == 0,
                             "SMOKE_CLEANUP"), (time.monotonic() < OUTER, "SMOKE_ORIGINAL_DEADLINE")):
            if not valid:
                if primary is not None: primary.add_note(code)
                else: raise ValueError(code)


def main():
    parser = argparse.ArgumentParser()
    for key in ("output", "input", "input-sha"): parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "SMOKE_ISOLATED_OWNER")
    output = ordinary(args.output, directory=True)
    need(output.parent == PROJECT/"experiments/v5-local-checks" and output.name == "bounded-reclamation-service-01"
         and SNAPSHOT == output/"sources", "SMOKE_EXACT_FRESH_RUN")
    request = json.loads(read(args.input, args.input_sha, MIB))
    report = dict(schema="DMKN_BOUNDED_RECLAMATION_SERVICE_RESULT_V1", status="FAIL",
        input_sha256=args.input_sha, release_sha256=RELEASE, original_outer_deadline=OUTER,
        clock_premise="OWNER_ADOPTED_UTC_AFTER_2020_NOT_SYNCHRONIZATION_EVIDENCE",
        native_calls=0, proof_calls=0, verifier_calls=0, trust_adoptions=0, mathematical_acceptance=False,
        independent_hosts=False, retained_contents_tested=False, full_v5_release=False)
    try:
        selected, workspace = adopt(request)
        save(output/"service-sources.json", selected)
        def no_recursive_delete(*unused, **ignored): raise ValueError("SMOKE_RECURSIVE_DELETE_FORBIDDEN")
        with patch.object(shutil, "rmtree", no_recursive_delete):
            asyncio.run(scenario(output, selected, workspace, report))
        report["imported_origins"] = rebind(selected)
        read(args.input, args.input_sha, MIB)
        need(time.monotonic() < OUTER, "SMOKE_ORIGINAL_DEADLINE")
        report["status"] = "PASS"
    except BaseException as error: report["terminal_error"] = error_fields(error)
    report["wall_seconds"] = time.monotonic()-STARTED
    save(output/"bounded-reclamation-service-result.json", report)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())

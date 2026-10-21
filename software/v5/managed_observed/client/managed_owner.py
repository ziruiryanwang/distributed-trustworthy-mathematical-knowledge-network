"""Installed trusted owner for finite, prospectively supervised generations.

Select this file through the unchanged installed public `run` entry. It does
not create mathematical trust, accept closure reports as authority, launch
arbitrary owner callbacks, or recover after loss of the actual supervisor.
"""
import asyncio
from copy import deepcopy
import json
from pathlib import Path
import sys
import time

from discovery import formal_features as F
from location.controller import SOURCE_NAMES
from location.controller_services import ROLE_NAMES
from placement.lifecycle import ManagedGenerations
from placement import sessions as S
from client.serve_generations import GenerationServices
from client.serve_workspace import _tls_pin
from client import private_credentials as C
from transport.http_provider import server_tls

SCHEMA = "DMKN_V5_MANAGED_OWNER_V2"
WORKER_SCHEMA = "DMKN_V5_MANAGED_OWNER_WORKER_V2"
RESULT_SCHEMA = "DMKN_V5_MANAGED_OWNER_RESULT_V2"
COMMON = {"schema", "operation", "release_sha256", "manager_root", "manager_config", "owner_limits"}
SERVICE = {"create_manager", "selection", "inner_limits", "worker_owner_limits",
           "startup_seconds", "service_seconds", "close_seconds", "boot_tail_seconds",
           "parent_tail_seconds", "supervisor_cleanup_seconds", "seal_before_close",
           "restore_requests", "tls", "intake_grant"}
PINS = {
    "v5/client/launch.py": "523a3031da86457037af3c41f87425cd406e5fe3fcf6a2edb2d87eff9b59ef78",
    "v5/client/boot.py": "76cdcd42379d61c5fe37dc86a23363687c084c56887302dcdd922aa9b089ce2b",
    "v5/client/serve_generations.py": "404365849dd0e41860ba8ccda01a5b064d028241a2d8b0063d76936fcd306687",
    "v5/placement/lifecycle.py": "bec62143313e1abd400550bae45a6334be2ddffb94d77a14ba9b5853b565042f",
    "v5/placement/sessions.py": "b4cfab61c990464756e87a7344e2a029a5374602283a4255d4d5aa854090b7f7",
    "v5/placement/reclaim.py": "19713fc4baec821a5c77a0071182c63401b292cbe79a7ed7c04b7deba50e1894",
}
OWNER_LOGICAL = "v5/client/managed_owner.py"


def _error(error):
    return {"type": type(error).__name__, "message": str(error)[:2000],
            "notes": [str(note)[:500] for note in getattr(error, "__notes__", ())][:16]}


_CLOSE_FLAGS = ("intake_closed", "retained_closed", "location_closed", "read_closed",
                "journal_closed", "controller_closed", "workspace_closed")
_CLOSE_COMPONENTS = frozenset(("_monitor_task", "_start_task", "intake", "retained",
    "location_stop", "location_close", "read", "advertisement", "controller",
    "workspace", "live_actor_prevents_store_close", "intake_report", "read_report",
    "location_report", "original_outer_deadline"))
_CLOSE_FAILURES = frozenset(("PLACEMENT_SERVICE_START_FAILED", "PLACEMENT_SERVICE_HEALTH_FAILED"))


def _close_enum(value, allowed):
    # Never stringify an unexpected value, including an exception or secret.
    if value is None: return None
    return value if type(value) is str and len(value) <= 64 and value in allowed else "UNRECOGNIZED_REDACTED"


def _close_scalars(value, *, flags=(), counts=()):
    value = value if type(value) is dict else {}
    result = {key: value.get(key) if type(value.get(key)) is bool else None for key in flags}
    for key in counts:
        number = value.get(key)
        result[key] = number if type(number) is int and 0 <= number <= 2**53-1 else None
    return result


def _project_service_close(raw):
    """Closed diagnostic vocabulary; never a mathematical/closure authority."""
    if type(raw) is not dict or type(raw.get("schema")) is not str or raw.get("schema") not in (
            "DMKN_V5_PLACEMENT_SERVICE_RESULT_V1", "DMKN_V5_PLACEMENT_SERVICE_STATUS_V1"):
        return {"schema": "DMKN_V5_MANAGED_SERVICE_CLOSE_OBSERVATION_V1",
                "observation_status": "UNRECOGNIZED_REPORT",
                "closure_authority": False, "mathematical_acceptance": False}
    final = raw["schema"] == "DMKN_V5_PLACEMENT_SERVICE_RESULT_V1"
    service = _close_scalars(raw, flags=("started", "closing", "closed", "retained_active"))
    service["status"] = _close_enum(raw.get("status"), frozenset(("CLOSED", "FAILED")))
    service["failure_code"] = _close_enum(raw.get("failure_code"), _CLOSE_FAILURES)
    cleanup_raw = raw.get("cleanup")
    cleanup = _close_scalars(cleanup_raw, flags=_CLOSE_FLAGS)
    errors = cleanup_raw.get("errors") if type(cleanup_raw) is dict else None
    cleanup["errors_available"] = type(errors) is list
    cleanup["errors_truncated"] = type(errors) is list and len(errors) > 32
    cleanup["errors"] = []
    if type(errors) is list:
        for row in errors[:32]:
            row = row if type(row) is dict else {}
            cleanup["errors"].append({
                "component": _close_enum(row.get("component"), _CLOSE_COMPONENTS),
                "code": _close_enum(row.get("code"), frozenset(("CLEANUP_UNCERTAIN",)))})
    observed = raw.get("observed")
    observed = observed if type(observed) is dict else {}
    location_raw = observed.get("location")
    location = _close_scalars(location_raw,
        flags=("closed", "channel_failed", "forced_termination"),
        counts=("sent_bytes", "received_bytes", "commands", "reply_frames", "stderr_bytes",
                "cleanup_allowance_seconds"))
    code = location_raw.get("returncode") if type(location_raw) is dict else None
    location["returncode"] = code if type(code) is int and -2**31 <= code <= 2**32-1 else None
    location["available"] = type(location_raw) is dict
    intake_raw = observed.get("intake")
    intake = _close_scalars(intake_raw, flags=("active_intake", "accepting", "stopped"),
        counts=("active_connections", "retained_closing_connections"))
    used = intake_raw.get("used") if type(intake_raw) is dict else None
    intake["used"] = _close_scalars(used, counts=("requests", "incoming_reserved",
        "outgoing_reserved", "observed_incoming", "attempted_outgoing", "busy", "refused",
        "completed_actions", "cancelled", "cleanup_errors", "handler_errors"))
    intake["available"] = type(intake_raw) is dict
    result = {"schema": "DMKN_V5_MANAGED_SERVICE_CLOSE_OBSERVATION_V1",
        "observation_status": "FINAL_SNAPSHOT" if final else "PARTIAL_SNAPSHOT",
        "service": service, "cleanup": cleanup, "location": location, "intake": intake,
        "closure_authority": False, "mathematical_acceptance": False}
    F.need(len(F.compact(result)) <= 8192, "MANAGED_CLOSE_OBSERVATION_BOUND")
    return result


def _service_close_observation(service):
    # The worker retains its exact owned reference before serving. Only call
    # after the existing cleanup attempt; do not await, retry, stop or adopt it.
    unavailable = {"schema": "DMKN_V5_MANAGED_SERVICE_CLOSE_OBSERVATION_V1",
        "observation_status": "NO_OWNED_SERVICE" if service is None else "OBSERVATION_UNAVAILABLE",
        "closure_authority": False, "mathematical_acceptance": False}
    if service is None: return unavailable
    try: return _project_service_close(service.report())
    except BaseException:
        # In particular, do not call _error/str/repr on diagnostic failures.
        # An unavailable observation cannot replace the primary/close error.
        return unavailable


def _owner_limits(value):
    F.fields(value, ("calls", "cpu_seconds"))
    F.uint(value["calls"], 1, 8192); F.uint(value["cpu_seconds"], 1, 3600)


def _parameters(value):
    p = deepcopy(value)
    F.need(type(p) is dict and p.get("schema") == SCHEMA, "MANAGED_OWNER_SCHEMA")
    op = p.get("operation")
    extras = {"initialize": set(), "status": set(), "serve": SERVICE, "seal": SERVICE,
              "retire": {"generation", "clock"},
              "reclaim": {"generation", "reclamation_profile", "max_entries", "action_seconds"}}
    F.need(type(op) is str and op in extras, "MANAGED_OWNER_OPERATION")
    F.fields(p, COMMON | extras[op]); F.hexid(p["release_sha256"])
    F.need(type(p["manager_root"]) is str and type(p["manager_config"]) is dict,
           "MANAGED_OWNER_MANAGER_ARGUMENTS")
    _owner_limits(p["owner_limits"])
    if op in ("retire", "reclaim"): F.hexid(p["generation"])
    if op == "retire":
        c = p["clock"]
        F.fields(c, ("lower_utc_ms", "valid_for_ms", "rate_error_ppm", "model_id"))
        F.uint(c["lower_utc_ms"], 1, 2**53-1); F.uint(c["valid_for_ms"], 1, 3600000)
        F.uint(c["rate_error_ppm"], 0, 999999); F.hexid(c["model_id"])
    if op == "reclaim":
        F.need(p["reclamation_profile"] is None or type(p["reclamation_profile"]) is dict,
               "MANAGED_OWNER_RECLAMATION_PROFILE")
        F.uint(p["max_entries"], 1, 2**31-1); F.uint(p["action_seconds"], 1, 3600)
    if op in ("serve", "seal"):
        F.need(type(p["create_manager"]) is bool and type(p["seal_before_close"]) is bool,
               "MANAGED_OWNER_EXPLICIT_FLAGS")
        F.need(op != "seal" or p["seal_before_close"], "MANAGED_OWNER_SEAL_REQUIRED")
        choice = p["selection"]
        F.need(type(choice) is dict, "MANAGED_OWNER_SELECTION")
        if "generation" in choice:
            F.fields(choice, ("generation",)); F.hexid(choice["generation"])
            F.need(not p["create_manager"], "MANAGED_OWNER_EXISTING_GENERATION_CREATE")
        else:
            F.fields(choice, ("slot", "generation_config")); F.uint(choice["slot"], 0, 1)
            F.need(type(choice["generation_config"]) is dict, "MANAGED_OWNER_GENERATION_CONFIG")
        _owner_limits(p["worker_owner_limits"])
        F.need(p["owner_limits"]["cpu_seconds"] >= 11,
               "MANAGED_OWNER_SUPERVISION_CPU_RESERVATION")
        F.fields(p["inner_limits"], ("cpu_seconds", "memory_mib", "active_processes",
                                     "wall_seconds", "stdout_bytes", "stderr_bytes"))
        for n in ("startup_seconds", "service_seconds", "close_seconds", "boot_tail_seconds",
                  "parent_tail_seconds"):
            F.uint(p[n], 1, 3600)
        F.uint(p["supervisor_cleanup_seconds"], 25, 60)
        requests = p["restore_requests"]
        F.need(type(requests) is list and len(requests) <= 256, "MANAGED_OWNER_RESTORE_BOUND")
        for request in requests: F.hexid(request)
        F.need(len(set(requests)) == len(requests), "MANAGED_OWNER_DUPLICATE_RESTORE")
        F.fields(p["tls"], ("read", "intake"))
        for value in p["tls"].values():
            if value is not None: F.fields(value, ("certificate", "private_key"))
        F.need(p["intake_grant"] is None or type(p["intake_grant"]) is dict,
               "MANAGED_OWNER_INTAKE_GRANT")
    return p


def _active(context):
    F.need(time.monotonic() < context.deadline, "MANAGED_OWNER_ORIGINAL_DEADLINE")


def _bindings(context, request):
    """Authenticate the installed release, ordinary boot and relocated source map."""
    F.need(len(sys.argv) == 5, "MANAGED_OWNER_ORDINARY_BOOT_REQUIRED")
    L = sys.modules.get("_dmkn_client_launch")
    F.need(L is not None, "MANAGED_OWNER_BOOT_HELPER_REQUIRED")
    # L was pinned by unchanged boot before any owner byte was executed.
    plan, raw, installation, workspace, roots, run = L.read_plan(sys.argv[1], sys.argv[2])
    F.need(Path(sys.argv[1]) == run/"plan.json" and context.installation == installation
           and context.workspace_root == workspace and context.run == run
           and context.location_workspace == run/"work"
           and context.sources_v5 == run/"sources/v5"
           and context.sources_portable == run/"sources/portable"
           and context.sources_owner == run/"sources/owner"
           and dict(context.limits) == plan["limits"]
           and dict(context.parameters) == plan["parameters"], "MANAGED_OWNER_CONTEXT_BINDING")
    F.need(all(s.isascii() and s.isdigit() and len(s) <= 20 for s in sys.argv[3:]),
           "MANAGED_OWNER_BOOT_CLOCKS")
    started_ns, deadline_ns = map(int, sys.argv[3:])
    F.need(context.started == started_ns/1e9 and context.deadline == deadline_ns/1e9
           and deadline_ns-started_ns == plan["limits"]["wall_seconds"]*1000000000,
           "MANAGED_OWNER_BOOT_CLOCK_BINDING")
    _active(context)
    F.need(Path(L.__file__) == roots["v5"]/"client/launch.py", "MANAGED_OWNER_HELPER_ORIGIN")
    L.pinned(Path(L.__file__), plan["sources"]["v5/client/launch.py"], L.SOURCE_MAX)
    F.need(dict(context.source_sha256) == {n: row["sha256"] for n, row in plan["sources"].items()},
           "MANAGED_OWNER_CONTEXT_SOURCE_MAP")
    release_root = L.ordinary(installation.parent, directory=True)
    release_raw = L.read(release_root/"V5-RELEASE.json", 8*L.MIB)
    F.need(L.sha(release_raw) == request["release_sha256"], "MANAGED_OWNER_RELEASE_ADOPTION")
    release = L.strict(release_raw)
    F.need(release.get("schema") == "DMKN_V5_DIRECTORY_RELEASE_V3"
           and release.get("base_manifest_sha256") == L.MANIFEST_SHA,
           "MANAGED_OWNER_RELEASE_SCHEMA")
    sdk = release.get("sdk_sources"); files = release.get("files")
    F.need(type(sdk) is dict and len(sdk) == 127 and type(files) is dict,
           "MANAGED_OWNER_SELECTED_127_MAP")
    F.need(all(type(name) is str and selected == "sdk/"+name for name, selected in sdk.items()),
           "MANAGED_OWNER_LOGICAL_SDK_MAP")
    selected = {name: files[path] for name, path in sdk.items()}
    F.need(OWNER_LOGICAL in selected and "v5/client/private_credentials.py" in selected
           and len(plan["sources"]) == 128 and plan["owner_entry"] == "managed_owner.py"
           and {n: row for n, row in plan["sources"].items() if not n.startswith("owner/")} == selected
           and {n: row for n, row in plan["sources"].items() if n.startswith("owner/")} ==
               {"owner/managed_owner.py": selected[OWNER_LOGICAL]}, "MANAGED_OWNER_EXACT_OWNER_MAP")
    F.need(Path(__file__) == context.sources_owner/"managed_owner.py", "MANAGED_OWNER_ENTRY_ORIGIN")
    for name, digest in PINS.items():
        F.need(name in selected and selected[name]["sha256"] == digest, "MANAGED_OWNER_FROZEN_SOURCE_PIN:"+name)
    for name, row in plan["sources"].items():
        _active(context); parts = L.relative(name)
        L.pinned(run/"sources"/Path(*parts), row, L.SOURCE_MAX)
    runtime_files, unused_raw = L.load_manifest(installation)
    helpers = {n: runtime_files[n] for n in L.HELPERS.values()}
    F.need(helpers["operator/commons.py"]["sha256"] == S.OPERATOR_SHA
           and helpers["receiver/helpers/run_stage.py"]["sha256"] == S.JOB_SHA,
           "MANAGED_OWNER_FIXED_SUPERVISOR")
    profile = F.digest("DMKN-V5-INSTALLED-MANAGED-WORKER-V2", {
        "release_sha256": request["release_sha256"], "base_manifest_sha256": L.MANIFEST_SHA,
        "sources": selected, "owner_entry": "managed_owner.py", "helpers": helpers,
        "role": WORKER_SCHEMA, "ownership": S.OWNERSHIP})
    protected = [release_root, run, workspace/(plan["name"]+"-request"),
                 *roots.values(), context.sources_v5,
                 context.sources_portable, context.sources_owner]
    original, original_workspace, original_run, original_roots = plan, workspace, run, roots
    original_sha = sys.argv[2]
    if plan["parameters"].get("schema") == WORKER_SCHEMA:
        # The pinned parent generated this internal pin. Reconstruct its exact
        # nested plan, so relocation cannot discard the public output exclusions.
        original_sha = plan["parameters"]["parent_plan_sha256"]
        parent_run = workspace.parent
        original, parent_raw, parent_installation, original_workspace, original_roots, original_run = \
            L.read_plan(parent_run/"plan.json", original_sha)
        F.need(parent_installation == installation and original_run == parent_run
               and original["parameters"] == request, "MANAGED_OWNER_PARENT_REQUEST_BINDING")
        expected = deepcopy(original)
        expected.update(name="managed-worker", workspace_root=str(parent_run/"work"),
            source_roots={key: str(parent_run/"sources"/key) for key in ("v5", "portable", "owner")},
            limits=request["inner_limits"], parameters={"schema": WORKER_SCHEMA,
                "request": request, "profile_sha256": profile, "parent_plan_sha256": original_sha})
        F.need(plan == expected, "MANAGED_OWNER_PARENT_PLAN_BINDING")
    else:
        F.need(plan["parameters"] == request, "MANAGED_OWNER_PUBLIC_REQUEST_BINDING")
    operation = {"name": original["name"], "run": str(original_run),
                 "workspace_root": str(original_workspace), "plan_sha256": original_sha}
    # Distinct public requests must reuse exact manager config bytes. Do not
    # insert changing operation paths into that persistent configuration.
    root = Path(request["manager_root"])
    F.need(all(not L.overlap(root, path) for path in protected), "MANAGED_OWNER_ROOT_OVERLAP")
    if request["operation"] in ("serve", "seal"):
        for value in request["tls"].values():
            if value is not None:
                for row in value.values():
                    path = _tls_pin(row)
                    F.need(all(not L.overlap(path, item) for item in [root, *protected]),
                           "MANAGED_OWNER_TLS_IMMUTABLE_OR_STATE_OVERLAP")
    credential_protected = [root, workspace, original_workspace, original_run,
        original_workspace/(original["name"]+"-request"), *original_roots.values(), *protected]
    if request.get("intake_grant") is not None:
        C.preflight(request["intake_grant"], credential_protected)
    return L, plan, runtime_files, profile, operation, credential_protected


def _save(context, value):
    raw = F.compact(value)
    F.need(len(raw) <= 1024**2, "MANAGED_OWNER_REPORT_BOUND")
    with (context.location_workspace/"managed-result.json").open("xb") as stream:
        stream.write(raw)


def _read_report(L, path):
    # Operational reports contain finite monotonic floats. Unlike public
    # parameters these are not canonical policy or accepted closure authority.
    def pairs(items):
        value = {}
        for key, item in items:
            F.need(key not in value, "MANAGED_OWNER_REPORT_DUPLICATE")
            value[key] = item
        return value
    def reject(value): raise ValueError("MANAGED_OWNER_REPORT_NONFINITE")
    value = json.loads(L.read(path, L.MIB), object_pairs_hook=pairs, parse_constant=reject)
    F.compact(value)  # Also rejects overflowing floating-point input.
    F.need(type(value) is dict, "MANAGED_OWNER_REPORT_OBJECT")
    return value


def _open(context, p, *, worker=False, deadline=None):
    create = not worker and (p["operation"] == "initialize" or p.get("create_manager", False))
    caps = p["worker_owner_limits"] if worker else p["owner_limits"]
    return ManagedGenerations.open(p["manager_root"], p["manager_config"], create=create,
        deadline=context.deadline if deadline is None else deadline, **caps)


def _record(status, generation):
    rows = [row for row in status["slots"] if row is not None and row["generation"] == generation]
    F.need(len(rows) == 1, "MANAGED_OWNER_GENERATION_NOT_PRESENT")
    return rows[0]


def _admin(context, p, report):
    manager = _open(context, p)
    try:
        if p["operation"] == "retire":
            clock = manager.adopt_clock(**p["clock"])
            report["retirement_intent"] = manager.begin_retire(p["generation"], clock)
            report["retired"] = manager.commit_retired(p["generation"], clock)
        elif p["operation"] == "reclaim":
            before = manager.status(); record = _record(before, p["generation"])
            if record["phase"] == "RETIRED":
                F.need(p["reclamation_profile"] is not None, "MANAGED_OWNER_RECLAMATION_ADOPTION_REQUIRED")
                report["enrollment"] = manager.begin_reclamation(p["generation"], p["reclamation_profile"])
            else:
                F.need(record["phase"] == "RECLAIMING" and p["reclamation_profile"] is None,
                       "MANAGED_OWNER_NO_RECLAMATION_PROFILE_RENEWAL")
            until = time.monotonic()+p["action_seconds"]
            F.need(until < context.deadline, "MANAGED_OWNER_RECLAMATION_ORIGINAL_DEADLINE")
            report["reclamation"] = manager.reclaim_step(p["generation"],
                max_entries=p["max_entries"], deadline=until)
        report["manager"] = manager.status()
    finally:
        manager.close()


def _supervise(context, p, L, plan, files, profile, report):
    A = L.load_helper("_dmkn_managed_supervisor", context.installation/"operator/commons.py",
                      files["operator/commons.py"])
    # The fixed run_stage helper imports domains by its fixed absolute name.
    # Refuse a preexisting name rather than replace arbitrary loaded code.
    L.load_helper("domains", context.installation/"receiver/helpers/domains.py",
                  files["receiver/helpers/domains.py"])
    J = L.load_helper("_dmkn_managed_job", context.installation/"receiver/helpers/run_stage.py",
                      files["receiver/helpers/run_stage.py"])
    inner = A.limits_checked(p["inner_limits"])
    F.need(inner["active_processes"] <= 8 and inner["wall_seconds"] <= 3600
           and inner["memory_mib"] <= 4096 and inner["cpu_seconds"] <= 86400,
           "MANAGED_OWNER_INNER_FINITE_LIMITS")
    for key in ("cpu_seconds", "memory_mib", "active_processes"):
        F.need(inner[key] <= context.limits[key], "MANAGED_OWNER_INNER_LIMIT_EXTENSION:"+key)
    budget = sum(p[n] for n in ("startup_seconds", "service_seconds", "close_seconds", "boot_tail_seconds"))
    F.need(budget < inner["wall_seconds"], "MANAGED_OWNER_CHILD_INTERVALS")
    parent_end = context.deadline-p["parent_tail_seconds"]
    F.need(time.monotonic()+inner["wall_seconds"]+p["supervisor_cleanup_seconds"] < parent_end,
           "MANAGED_OWNER_ORIGINAL_PARENT_RESERVATION")
    child = deepcopy(plan)
    child.update(name="managed-worker", workspace_root=str(context.location_workspace),
        source_roots={"v5": str(context.sources_v5), "portable": str(context.sources_portable),
                      "owner": str(context.sources_owner)}, limits=inner,
        parameters={"schema": WORKER_SCHEMA, "request": p, "profile_sha256": profile,
                    "parent_plan_sha256": sys.argv[2]})
    raw = F.compact(child); F.need(len(raw) <= L.MIB, "MANAGED_OWNER_CHILD_PLAN_BOUND")
    child_run = L.ordinary(context.location_workspace/child["name"], directory=True, fresh=True)
    child_run.mkdir()
    plan_path = child_run/"plan.json"
    with plan_path.open("xb") as stream: stream.write(raw)
    plan_sha = L.sha(raw)
    # Validate the ordinary plan before durable manager effects.
    L.read_plan(plan_path, plan_sha)
    manager = _open(context, p, deadline=parent_end)
    try:
        started_ns = time.monotonic_ns()
        child_deadline_ns = started_ns+inner["wall_seconds"]*1000000000
        argv = [str(L.invocation(context.installation)), "-I", "-S", "-B",
            str(context.sources_v5/"client/boot.py"), str(plan_path), plan_sha,
            str(started_ns), str(child_deadline_ns)]
        report["worker_plan_sha256"] = plan_sha
        result = S.supervise(manager, profile={"sha256": profile, "ownership": S.OWNERSHIP},
            argv=argv, cwd=context.installation, evidence=context.location_workspace/"managed-supervisor",
            limits=inner, operator_module=A, job_module=J,
            cleanup_seconds=p["supervisor_cleanup_seconds"])
        report["supervision"] = result
    finally:
        # supervise consumes and closes its owner before launching. close is
        # idempotent on a closed manager, but cannot fabricate actor closure.
        manager.close()
    # Preserve actual failed child/supervisor results. Recovery is never success.
    for key, path in (("worker", child_run/"work/managed-result.json"),
                      ("worker_boot", child_run/"BOOT-RESULT.json"),
                      ("worker_boot_failure", child_run/"BOOT-FAILED.json")):
        if path.exists(): report[key] = _read_report(L, path)
    F.need(result["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED"
           and result["direct_child_reaped"] and result["job_closed"]
           and not result["cleanup_errors"] and result["final_job"]["active_processes"] == 0
           and result["session_recovery"]["status"] == "QUIESCED",
           "MANAGED_OWNER_SUPERVISED_OPERATION_FAILED")
    worker = report.get("worker", {}); boot = report.get("worker_boot", {})
    F.need(worker.get("status") == "COMPLETE" and worker.get("profile_sha256") == profile
           and worker.get("operation") == p["operation"]
           and boot.get("status") == "OWNER_EXITED_ZERO" and boot.get("plan_sha256") == plan_sha,
           "MANAGED_OWNER_WORKER_COMPLETION_MISSING")
    report["generation"] = worker["generation"]


def _tls(value):
    if value is None: return None
    return server_tls(_tls_pin(value["certificate"]), _tls_pin(value["private_key"]))


async def _worker(context, p, profile, operation, credential_protected, report):
    end = context.deadline-p["boot_tail_seconds"]
    F.need(time.monotonic()+p["startup_seconds"]+p["service_seconds"]+p["close_seconds"] < end,
           "MANAGED_OWNER_WORKER_ORIGINAL_RESERVATION")
    manager = _open(context, p, worker=True, deadline=end)
    services = None; service = None; primary = None
    try:
        report["join"] = manager.join_current_worker(profile)
        choice = p["selection"]
        if "generation" in choice:
            generation = choice["generation"]
        else:
            report["allocation"] = manager.allocate(choice["slot"], choice["generation_config"])
            generation = report["allocation"]["generation"]
        report["generation"] = generation
        runtime = {"source_root": str(context.sources_portable/"location"),
            "installation_root": str(context.installation),
            "source_pins": {name: context.source_sha256["portable/location/"+name] for name in SOURCE_NAMES},
            "role_pins": {name: context.source_sha256["portable/location/"+name] for name in ROLE_NAMES}}
        services = GenerationServices(manager, runtime)
        read_tls, intake_tls = _tls(p["tls"]["read"]), _tls(p["tls"]["intake"])
        async with asyncio.timeout(p["startup_seconds"]):
            report["ready"] = await services.start_slot(generation, outer_deadline=end,
                location_deadline=end-7, read_tls_context=read_tls, intake_tls_context=intake_tls)
        service = services.service(generation)
        until = time.monotonic()+p["service_seconds"]
        F.need(until < service.deadline and until+p["close_seconds"] < end,
               "MANAGED_OWNER_SERVICE_INTERVAL_UNAVAILABLE")
        numerator, denominator = until.as_integer_ratio()
        service_until_ns = numerator*1000000000//denominator
        report["service_until_ns"] = service_until_ns
        report["intake_handoff"] = None
        if p["intake_grant"] is not None:
            try:
                report["intake_handoff"] = C.publish(service, p["intake_grant"],
                    release_sha256=p["release_sha256"], profile_sha256=profile, operation=operation,
                    session={key: report["join"][key] for key in ("number", "nonce", "worker")},
                    service_until_ns=service_until_ns, protected=credential_protected)
            except C.CredentialError as error:
                report["intake_handoff"] = error.observation()
                raise
        F.need(time.monotonic_ns() < service_until_ns, "MANAGED_OWNER_READY_ORIGINAL_INTERVAL")
        # Endpoint/status only: no bearer token is written to any report.
        with (context.location_workspace/"managed-ready.json").open("xb") as stream:
            stream.write(F.compact({"profile_sha256": profile, "generation": generation,
                "service": service.ready(), "service_until_ns": service_until_ns,
                "intake_handoff": report["intake_handoff"], "mathematical_acceptance": False}))
        F.need(time.monotonic_ns() < service_until_ns, "MANAGED_OWNER_READY_ORIGINAL_INTERVAL")
        restored = []
        async with asyncio.timeout_at(until):
            for request in p["restore_requests"]:
                restored.append(await service.advertise_retained(request, until=until))
        report["restored"] = restored
        await asyncio.sleep(max(0, until-time.monotonic()))
        service.ready()  # A failed/early-expired service is not successful serving.
        if p["seal_before_close"]: report["sealed"] = manager.seal(generation)
    except BaseException as error:
        primary = error
    finally:
        close_errors = []
        if services is not None:
            try:
                # Every handle is attempted by the composer; failed gather
                # entries are failures, not silently accepted successful awaits.
                close_until = min(end, time.monotonic()+p["close_seconds"])
                async with asyncio.timeout_at(close_until):
                    outcomes = await services.close()
                report["closures"] = [(_error(v) if isinstance(v, BaseException) else v) for v in outcomes]
                close_errors.extend(v for v in outcomes if isinstance(v, BaseException))
            except BaseException as error: close_errors.append(error)
        report["service_close_observation"] = _service_close_observation(service)
        try: report["manager"] = manager.status()
        except BaseException as error: close_errors.append(error)
        try: manager.close()
        except BaseException as error: close_errors.append(error)
        if close_errors:
            report["close_errors"] = [_error(error) for error in close_errors]
            if primary is None: primary = close_errors[0]
            else: primary.add_note("MANAGED_OWNER_ADDITIONAL_CLOSE_FAILURE")
    if primary is not None: raise primary
    record = _record(report["manager"], report["generation"])
    F.need(record["run_state"] == "CLOSED", "MANAGED_OWNER_ORDERLY_CLOSE_REQUIRED")
    if p["seal_before_close"]:
        F.need(record["phase"] == "SEALED_SERVING", "MANAGED_OWNER_SEAL_NOT_COMMITTED")


def main(context):
    report = {"schema": RESULT_SCHEMA, "status": "FAILED", "mathematical_acceptance": False,
              "global_complete": False, "public_deployment_qualified": False}
    try:
        supplied = deepcopy(dict(context.parameters))
        worker = supplied.get("schema") == WORKER_SCHEMA
        if worker:
            F.fields(supplied, ("schema", "request", "profile_sha256", "parent_plan_sha256"))
            F.hexid(supplied["profile_sha256"]); F.hexid(supplied["parent_plan_sha256"])
            p = _parameters(supplied["request"])
            F.need(p["operation"] in ("serve", "seal"), "MANAGED_OWNER_WORKER_OPERATION")
        else: p = _parameters(supplied)
        report["operation"] = p["operation"]
        L, plan, files, profile, operation, credential_protected = _bindings(context, p)
        report["profile_sha256"] = profile
        if worker:
            F.need(supplied["profile_sha256"] == profile and dict(context.limits) == p["inner_limits"],
                   "MANAGED_OWNER_WORKER_PROFILE")
            asyncio.run(_worker(context, p, profile, operation, credential_protected, report))
        elif p["operation"] in ("serve", "seal"):
            _supervise(context, p, L, plan, files, profile, report)
        else: _admin(context, p, report)
        _active(context); report["status"] = "COMPLETE"
    except BaseException as error:
        report["error"] = _error(error)
    _save(context, report)
    return 0 if report["status"] == "COMPLETE" else 1


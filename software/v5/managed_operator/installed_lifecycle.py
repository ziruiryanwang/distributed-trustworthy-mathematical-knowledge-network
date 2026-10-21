"""One installed public managed lifecycle, selected once by the root.

No SDK imports, direct lifecycle/SQL calls, injected worker, synthetic close,
recovery/retry, proof, intake or trust action. Failed artifacts remain intact.
"""
import time
STARTED = time.monotonic()
DEADLINE = STARTED + 570
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import secrets
import socket
import sys

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
NAME = "managed-operator-lifecycle-01"
INSTALL = PROJECT/"product-local/v5-distribution-managed-owner-01/Mathematical Commons v5"
TEMPLATE = PROJECT/"experiments/v5-local-checks/bounded-reclamation-service-01/bounded-reclamation-service-result.json"
TEMPLATE_SHA = "21ee791482d385521467673ad67630f7f6626ceb840c7adaf6ea61b7ce263a5b"
BASE_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
OPERATOR_SHA = "6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9"
JOB_SHA = "bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028"
PINS = {
    "v5/client/launch.py": "523a3031da86457037af3c41f87425cd406e5fe3fcf6a2edb2d87eff9b59ef78",
    "v5/client/boot.py": "76cdcd42379d61c5fe37dc86a23363687c084c56887302dcdd922aa9b089ce2b",
    "v5/client/serve_generations.py": "404365849dd0e41860ba8ccda01a5b064d028241a2d8b0063d76936fcd306687",
    "v5/placement/lifecycle.py": "bec62143313e1abd400550bae45a6334be2ddffb94d77a14ba9b5853b565042f",
    "v5/placement/sessions.py": "b4cfab61c990464756e87a7344e2a029a5374602283a4255d4d5aa854090b7f7",
    "v5/placement/reclaim.py": "19713fc4baec821a5c77a0071182c63401b292cbe79a7ed7c04b7deba50e1894",
}
MIB = 1024**2
SUCCESS = "COMMAND_EXITED_ZERO_AND_CLOSED"
OWNERSHIP = "PRIVATE_FIXED_WORKER_NO_EXTERNAL_WRITERS_OR_OUT_OF_JOB_LAUNCHERS_V1"
CLEANUP = ("intake_closed", "retained_closed", "location_closed", "read_closed",
           "journal_closed", "controller_closed", "workspace_closed")


def need(value, reason):
    if not value:
        raise ValueError(reason)


def active(reserve=0):
    need(time.monotonic()+reserve < DEADLINE, "CHECK_ORIGINAL_DEADLINE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(domain, value):
    return sha(domain.encode("ascii")+b"\0"+encode(value))


def strict(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            need(key not in value, "CHECK_DUPLICATE_JSON_KEY")
            value[key] = item
        return value
    def reject(value):
        raise ValueError("CHECK_NONFINITE_JSON")
    value = json.loads(raw, object_pairs_hook=pairs, parse_constant=reject)
    encode(value)
    return value


def ordinary(path, *, directory=False, fresh=False):
    path = Path(path)
    need(path.is_absolute() and path.resolve() == path and all(
        not item.is_symlink() and not item.is_junction() for item in (path, *path.parents)),
        "CHECK_ORDINARY_PATH")
    if fresh:
        need(not path.exists() and path.parent.is_dir(), "CHECK_FRESH_PATH")
    else:
        need(path.is_dir() if directory else path.is_file(), "CHECK_PATH_KIND")
    return path


def read(path, maximum=MIB):
    path = ordinary(path)
    size = path.stat().st_size
    need(size <= maximum, "CHECK_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "CHECK_FILE_CHANGED")
    return raw


def pin(path, row, maximum=MIB):
    raw = read(path, maximum)
    need(row == {"bytes": len(raw), "sha256": sha(raw)}, "CHECK_FILE_PIN")
    return raw


def save(path, value):
    raw = encode(value)
    need(len(raw) <= MIB, "CHECK_REPORT_BOUND")
    with ordinary(path, fresh=True).open("xb") as stream:
        stream.write(raw)
    return sha(raw)


def load_helper(name, path, row):
    need(name not in sys.modules, "CHECK_HELPER_MODULE_COLLISION")
    raw = pin(path, row, 4*MIB)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def limits(cpu, wall, processes):
    return {"cpu_seconds": cpu, "wall_seconds": wall, "memory_mib": 768,
            "active_processes": processes, "stdout_bytes": MIB, "stderr_bytes": MIB}


def check_supervision(value):
    need(value["status"] == SUCCESS and value["child_exit_code"] == 0
         and value["direct_child_reaped"] is True and value["job_closed"] is True
         and value["cleanup_errors"] == [] and value["termination_requested"] is False
         and value["final_job"]["active_processes"] == 0
         and value["final_job"]["terminated_processes"] == 0, "CHECK_CLEAN_SUPERVISION")
    # TotalProcesses is a raw cumulative OS counter, not a scripted actor count.


def claim_flags(value):
    need(value["mathematical_acceptance"] is False and value["global_complete"] is False
         and value["public_deployment_qualified"] is False, "CHECK_CLAIM_BOUNDARY")


def check_boot(boot, plan_raw, selected):
    plan = strict(plan_raw)
    need(plan["sources"] == selected and len(selected) == 127
         and plan["owner_entry"] == "managed_owner.py", "CHECK_EXACT_BOOT_SOURCE_MAP")
    need(boot["schema"] == "DMKN_V5_CLIENT_BOOT_RESULT_V1"
         and boot["status"] == "OWNER_EXITED_ZERO" and boot["plan_sha256"] == sha(plan_raw)
         and boot["source_files"] == 127, "CHECK_ORDINARY_BOOT")
    origins = {name: path.replace("\\", "/") for name, path in boot["imported_origins"].items()}
    need(all(path in selected for path in origins.values()), "CHECK_BOOT_ORIGINS")
    for name in ("placement.lifecycle", "placement.sessions", "placement.reclaim", "client.serve_generations"):
        need(origins.get(name) == "v5/"+name.replace(".", "/")+".py", "CHECK_SELECTED_MODULE_ORIGIN")
    return plan


def free_ports():
    streams = []
    try:
        for unused in range(6):
            stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            streams.append(stream)
            stream.bind(("127.0.0.1", 0))
        ports = [stream.getsockname()[1] for stream in streams]
        need(len(set(ports)) == 6, "CHECK_DISTINCT_PORTS")
        return ports
    finally:
        for stream in streams:
            stream.close()


def endpoint(port):
    return {"host": "127.0.0.1", "port": port, "tls": False, "server_name": None}


def execute(output, supplied, report):
    active()
    need(set(supplied) == {"schema", "installation_root", "release_sha256", "template"}
         and supplied["schema"] == "DMKN_MANAGED_OPERATOR_INSTALLED_LIFECYCLE_INPUT_V1"
         and Path(supplied["installation_root"]) == INSTALL, "CHECK_SELECTED_INPUT")
    ordinary(INSTALL, directory=True)
    release_raw = read(INSTALL/"V5-RELEASE.json", 8*MIB)
    need(sha(release_raw) == supplied["release_sha256"], "CHECK_ADOPTED_RELEASE")
    release = strict(release_raw)
    need(release["schema"] == "DMKN_V5_DIRECTORY_RELEASE_V3"
         and release["base_role"] == "mathematical-client-location-v1"
         and release["base_manifest_sha256"] == BASE_SHA, "CHECK_RELEASE_ROLE")
    sdk = release["sdk_sources"]
    need(type(sdk) is dict and len(sdk) == 126, "CHECK_SDK_COUNT")
    for logical, relative in sdk.items():
        parts = PurePosixPath(logical).parts
        need(relative == "sdk/"+logical and len(parts) >= 2 and parts[0] in ("v5", "portable")
             and "\\" not in logical and all(part not in ("", ".", "..") for part in parts)
             and PurePosixPath(logical).as_posix() == logical, "CHECK_SDK_PATH")
    selected = {logical: release["files"][relative] for logical, relative in sdk.items()}
    for logical, expected in PINS.items():
        need(selected[logical]["sha256"] == expected, "CHECK_FROZEN_SOURCE")
    owner = selected["v5/client/managed_owner.py"]
    pin(INSTALL/"sdk/v5/client/managed_owner.py", owner, 2*MIB)
    pin(INSTALL/"distribution.py", release["files"]["distribution.py"], 2*MIB)
    manifest_raw = read(INSTALL/"base/RELEASE-MANIFEST.json", 8*MIB)
    need(sha(manifest_raw) == BASE_SHA, "CHECK_BASE_MANIFEST")
    files = strict(manifest_raw)["files"]
    helpers = {name: files[name] for name in
               ("operator/commons.py", "receiver/helpers/domains.py", "receiver/helpers/run_stage.py")}
    need(helpers["operator/commons.py"]["sha256"] == OPERATOR_SHA
         and helpers["receiver/helpers/run_stage.py"]["sha256"] == JOB_SHA, "CHECK_SUPERVISOR_PINS")
    profile = digest("DMKN-V5-INSTALLED-MANAGED-WORKER-V1", {
        "release_sha256": supplied["release_sha256"], "base_manifest_sha256": BASE_SHA,
        "sources": selected, "owner_entry": "managed_owner.py", "helpers": helpers,
        "role": "DMKN_V5_MANAGED_OWNER_WORKER_V1", "ownership": OWNERSHIP})
    selected = {**selected, "owner/managed_owner.py": owner}
    A = load_helper("_managed_check_supervisor", INSTALL/"base/operator/commons.py", helpers["operator/commons.py"])
    load_helper("domains", INSTALL/"base/receiver/helpers/domains.py", helpers["receiver/helpers/domains.py"])
    J = load_helper("_managed_check_job", INSTALL/"base/receiver/helpers/run_stage.py", helpers["receiver/helpers/run_stage.py"])
    row = supplied["template"]
    need(row == {"path": str(TEMPLATE), "bytes": 53427, "sha256": TEMPLATE_SHA}, "CHECK_DATA_ONLY_TEMPLATE")
    template = strict(pin(TEMPLATE, {k: row[k] for k in ("bytes", "sha256")}))
    generation_config = deepcopy(template["retired"]["config"])
    del generation_config["placement"]["generation"]
    need(generation_config["placement"]["admission_close_ms"] == 1577836798000
         and generation_config["placement"]["retention_not_after_ms"] == 1577836799000,
         "CHECK_ORIGINAL_HORIZONS")
    operations, commands, requests = output/"operations", output/"public-commands", output/"inputs"
    for path in (operations, commands, requests):
        ordinary(path, fresh=True).mkdir()
    manager_root = ordinary(output/"managed", fresh=True)
    ports = free_ports()  # Release before launch; a race is a failure, never a retry.
    epoch, clock_model = secrets.token_hex(32), secrets.token_hex(32)
    slots = [{"reserved_bytes": 16*MIB, "max_cells": 1, "max_runs": 1,
              "read_endpoint": endpoint(ports[n]), "intake_endpoint": endpoint(ports[n+1]),
              "listen": ["/ip4/127.0.0.1/tcp/"+str(ports[n+2])]} for n in (0, 3)]
    manager_config = {"schema": "DMKN_V5_TWO_GENERATION_MANAGER_SUPERVISED_V1",
        "epoch": epoch, "clock_model_id": clock_model, "registry_pages": 256,
        "owner_reserved_bytes": 36*MIB, "registry_reserved_bytes": 2*MIB,
        "cleanup_reserved_bytes": 2*MIB, "max_sessions": 1, "slots": slots,
        "protected_roots": [str(p) for p in (INSTALL, output/"sources", operations, commands, requests)]}
    egress = {"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test", "public_ports": [],
              "test_endpoints": [{"host": "127.0.0.1", "port": port} for port in ports]}
    generation_config["placement"]["service_epoch"] = epoch
    generation_config["egress"] = deepcopy(egress)
    generation_config["location"].update(egress=deepcopy(egress), listen=slots[0]["listen"],
                                         endpoints=[slots[0]["read_endpoint"]])
    common = {"schema": "DMKN_V5_MANAGED_OWNER_V1", "release_sha256": supplied["release_sha256"],
              "manager_root": str(manager_root), "manager_config": manager_config,
              "owner_limits": {"calls": 64, "cpu_seconds": 20}}
    report.update(release_sha256=supplied["release_sha256"], profile_sha256=profile,
                  manager_root=str(manager_root), manager_config=manager_config,
                  generation_config=generation_config, operations=[])

    def public(name, parameters, *, serving=False):
        wrapper_limits = limits(110, 180, 7) if serving else limits(20, 65, 7)
        active(wrapper_limits["wall_seconds"]+20)
        request = {"schema": "DMKN_V5_INSTALLED_REQUEST_V1", "name": name,
            "workspace_root": str(operations), "parameters": parameters,
            "limits": limits(90, 140, 6) if serving else limits(15, 45, 6),
            "output_limits": {"bytes": 64*MIB, "entries": 1024},
            "owner": {"root": str(INSTALL/"sdk/v5/client"), "entry": "managed_owner.py",
                      "sources": {"managed_owner.py": owner}}, "runtime_mode": "atomic"}
        request_path = requests/(name+".json")
        request_sha = save(request_path, request)
        argv = [str(INSTALL/"base/receiver/runtime/python/python.exe"), "-I", "-S", "-B",
                str(INSTALL/"distribution.py"), "launch", supplied["release_sha256"], "run",
                str(request_path), request_sha]
        item = {"name": name, "request_sha256": request_sha, "artifacts": {}}
        report["operations"].append(item)
        raw_result = A.supervise(argv, PROJECT, commands/name, wrapper_limits, J.Job)
        item["supervision"] = raw_result
        save(commands/(name+"-result.json"), raw_result)
        run = operations/name
        paths = {"plan": run/"plan.json", "launch": run/"RESULT.json",
            "boot": run/"BOOT-RESULT.json", "boot_failure": run/"BOOT-FAILED.json",
            "owner": run/"work/managed-result.json",
            "request": operations/(name+"-request")/"request.json",
            "prepared_plan": operations/(name+"-request")/"launch.json",
            "preparation": operations/(name+"-request")/"preparation.json"}
        if serving:
            paths.update(worker_plan=run/"work/managed-worker/plan.json",
                worker_boot=run/"work/managed-worker/BOOT-RESULT.json",
                worker_owner=run/"work/managed-worker/work/managed-result.json")
        values, raws = {}, {}
        for key, path in paths.items():
            if path.exists():
                raw = read(path)
                item["artifacts"][key] = {"path": str(path), "bytes": len(raw), "sha256": sha(raw)}
                raws[key], values[key] = raw, strict(raw)
        # Raw process and owner failure evidence has been captured before checks.
        check_supervision(raw_result)
        need(set(paths)-{"boot_failure"} <= set(values), "CHECK_REQUIRED_PUBLIC_ARTIFACT")
        need(values["request"] == request and raws["plan"] == raws["prepared_plan"], "CHECK_PUBLIC_REQUEST_BINDING")
        launch, result = values["launch"], values["owner"]
        need(launch["schema"] == "DMKN_V5_CLIENT_LAUNCH_RESULT_V1" and launch["status"] == SUCCESS
             and launch["final_error"] is None and launch["plan_sha256"] == sha(raws["plan"]), "CHECK_PUBLIC_LAUNCH")
        check_supervision(launch["result"])
        plan = check_boot(values["boot"], raws["plan"], selected)
        need(plan["parameters"] == parameters and plan["limits"] == request["limits"]
             and plan["installation_root"] == str(INSTALL/"base"), "CHECK_ORDINARY_PARAMETERS")
        need(result["schema"] == "DMKN_V5_MANAGED_OWNER_RESULT_V1" and result["status"] == "COMPLETE"
             and result["operation"] == parameters["operation"] and result["profile_sha256"] == profile,
             "CHECK_OWNER_COMPLETION")
        claim_flags(result)
        if serving:
            child = check_boot(values["worker_boot"], raws["worker_plan"], selected)
            need(child["parameters"] == {"schema": "DMKN_V5_MANAGED_OWNER_WORKER_V1",
                 "request": parameters, "profile_sha256": profile}
                 and child["limits"] == parameters["inner_limits"]
                 and result["worker_plan_sha256"] == sha(raws["worker_plan"])
                 and result["worker"] == values["worker_owner"]
                 and result["worker_boot"] == values["worker_boot"], "CHECK_NESTED_PUBLIC_BINDING")
        active()
        return result

    report["stage"] = "public-create-serve-seal-close"
    service = public("serve", {**deepcopy(common), "operation": "serve", "create_manager": True,
        "selection": {"slot": 0, "generation_config": generation_config},
        "inner_limits": limits(60, 80, 3), "worker_owner_limits": {"calls": 64, "cpu_seconds": 35},
        "startup_seconds": 20, "service_seconds": 2, "close_seconds": 25,
        "boot_tail_seconds": 10, "parent_tail_seconds": 10, "supervisor_cleanup_seconds": 25,
        "seal_before_close": True, "restore_requests": [], "tls": {"read": None, "intake": None}}, serving=True)
    check_supervision(service["supervision"])
    recovery = service["supervision"]["session_recovery"]
    need(recovery["status"] == "QUIESCED" and recovery["unclean_slots"] == []
         and recovery["orderly_close_claim"] is False, "CHECK_CLOSED_NOT_UNCLEAN_RECOVERY")
    worker = service["worker"]
    need(worker["status"] == "COMPLETE" and worker["operation"] == "serve"
         and worker["profile_sha256"] == profile and not worker.get("close_errors"), "CHECK_WORKER_COMPLETE")
    claim_flags(worker)
    generation = service["generation"]
    state = worker["manager"]
    record = state["slots"][0]
    need(state["slots"][1] is None and state["allocated_sequence"] == 1 and state["retired_floor"] == 0
         and record["slot"] == 0 and record["sequence"] == 1 and record["runs"] == 1
         and record["generation"] == generation == worker["generation"]
         and record["run_state"] == "CLOSED" and record["phase"] == "SEALED_SERVING"
         and record["failure"] is None and "quiescence" not in record, "CHECK_ONE_ORDERLY_RUN")
    bound_config = deepcopy(generation_config)
    bound_config["placement"]["generation"] = generation
    need(record["config"] == bound_config and worker["allocation"]["runs"] == 0
         and worker["allocation"]["sequence"] == 1 and worker["allocation"]["generation"] == generation
         and worker["sealed"]["phase"] == "SEALED_SERVING" and worker["ready"]["run"] == 1
         and len(worker["closures"]) == 1, "CHECK_ALLOCATION_SERVICE_SEAL")
    closed = worker["closures"][0]
    need(closed["status"] == "CLOSED" and closed["cleanup"]["errors"] == []
         and all(closed["cleanup"][key] is True for key in CLEANUP)
         and closed["bindings"]["generation"] == generation
         and record["closure_sha256"] == sha(encode(closed)), "CHECK_REAL_CLOSED_DIGEST")
    claim_flags(closed)
    location = closed["observed"]["location"]
    need(location["closed"] is True and location["returncode"] == 0
         and location["forced_termination"] is False and location["channel_failed"] is False,
         "CHECK_NODE_ORDERLY_EXIT")
    session = state["session"]
    need(session["number"] == 1 and session["state"] == "BOUND" and session["profile_sha256"] == profile
         and worker["join"]["number"] == 1 and worker["join"]["nonce"] == session["nonce"]
         and worker["join"]["worker"] == session["worker"]
         and record["session"]["worker"] == session["worker"], "CHECK_ONE_BOUND_SESSION")
    report.update(generation=generation, closure_sha256=record["closure_sha256"], real_closed_run_tested=True)
    report["stage"] = "separate-public-status"
    status = public("status", {**deepcopy(common), "operation": "status"})["manager"]
    expected_status = deepcopy(state)
    expected_status["session"]["state"] = "QUIESCED"
    need(status == expected_status, "CHECK_ONLY_BOUND_TO_QUIESCED_NO_CLOSED_REWRITE")
    generation_root = manager_root/"slot-0/g00000000000000000001"
    ordinary(generation_root, directory=True)
    marker_raw = read(manager_root/"manager.json")
    need(strict(marker_raw) == {"schema": manager_config["schema"], "root": str(manager_root),
         "config_sha256": sha(encode(manager_config))}, "CHECK_EXACT_MANAGER_MARKER")
    derived = digest("DMKN-V5-TWO-SLOT-GENERATION-V1", {
        "manager": sha(marker_raw), "sequence": 1, "slot": 0, "config": generation_config})
    need(generation == derived, "CHECK_DERIVED_GENERATION")
    report["stage"] = "fresh-public-retirement"
    # Fresh explicit owner premise, not a clock synchronization or TTL experiment.
    clock = {"lower_utc_ms": 1577836800000, "valid_for_ms": 60000,
             "rate_error_ppm": 0, "model_id": clock_model}
    report["clock_premise"] = {**clock, "assertion": "LOCAL_OWNER_UTC_IS_AFTER_2020_01_01",
                               "fresh_request": True, "clock_synchronization_claim": False}
    retired_result = public("retire", {**deepcopy(common), "operation": "retire",
                                       "generation": generation, "clock": clock})
    retired = retired_result["retired"]
    unchanged = set(record)-{"phase", "retirement_lower_ms"}
    need({key: retired[key] for key in unchanged} == {key: record[key] for key in unchanged}
         and retired["phase"] == "RETIRED" and retired["retirement_lower_ms"] >= clock["lower_utc_ms"],
         "CHECK_RETIRE_PRESERVES_CLOSED_AND_CHARGES")
    expected_retired = deepcopy(status)
    expected_retired.update(retired_floor=1, slots=[retired, None])
    need(retired_result["manager"] == expected_retired
         and retired_result["retirement_intent"]["phase"] == "RETIRING", "CHECK_RETIREMENT_COMMIT")
    # Pin only finite public/control evidence, never secret identity.key contents.
    held = {row["path"]: {key: row[key] for key in ("bytes", "sha256")}
            for operation in report["operations"] for row in operation["artifacts"].values()}
    held[str(manager_root/"manager.json")] = {"bytes": len(marker_raw), "sha256": sha(marker_raw)}
    report["stage"] = "one-public-bounded-reclaim"
    profile_reclaim = {"layout": "DMKN_V5_CLOSED_GENERATION_LAYOUT_V1",
        "ownership": "PRIVATE_ENROLLED_NO_OTHER_WRITERS_OR_RESTORES_V1", "max_calls": 2,
        "max_entries_per_call": 64, "max_apparent_bytes": 16*MIB}
    reclaimed = public("reclaim", {**deepcopy(common), "operation": "reclaim", "generation": generation,
        "reclamation_profile": profile_reclaim, "max_entries": 64, "action_seconds": 15})
    enrollment, freed = reclaimed["enrollment"], reclaimed["reclamation"]
    need(enrollment["run_state"] == "CLOSED" and enrollment["closure_sha256"] == record["closure_sha256"]
         and enrollment["reclaim"]["profile"] == profile_reclaim and enrollment["reclaim"]["calls"] == 0
         and enrollment["reclaim"]["root"] == str(generation_root), "CHECK_EXACT_RECLAIM_ENROLLMENT")
    need(freed["status"] == "FREE" and freed["generation"] == generation and freed["slot"] == 0
         and freed["sequence"] == 1 and freed["charged_reclaim_calls"] == 1
         and freed["physical_envelope_adopted"] is False, "CHECK_ONE_CHARGED_RECLAIM")
    expected_free = deepcopy(expected_retired)
    expected_free["slots"] = [None, None]
    need(reclaimed["manager"] == expected_free and not generation_root.exists(), "CHECK_EXACT_FREE_ROOT")
    for path, row in held.items():
        active()
        pin(path, row)
    for name in ("generations.sqlite", "owner.lock"):
        ordinary(manager_root/name)
    for name in ("slot-0", "slot-1"):
        ordinary(manager_root/name, directory=True)
    for operation in report["operations"]:
        ordinary(operations/operation["name"], directory=True)
        ordinary(operations/(operation["name"]+"-request"), directory=True)
        ordinary(commands/operation["name"], directory=True)
    report.update(stage="complete", status="PASS", final_state=reclaimed["manager"],
        exact_reclaimed_root=str(generation_root), charged_reclaim_calls=1,
        prior_public_evidence_unchanged=True, orderly_close_preserved=True,
        cumulative_process_count_asserted=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--input-sha", required=True)
    args = parser.parse_args()
    output = ordinary(args.output, directory=True)
    need(output == PROJECT/"experiments/v5-local-checks"/NAME and Path.cwd() == PROJECT
         and Path(__file__) == output/"sources/software/v5/managed_operator/installed_lifecycle.py"
         and os.name == "nt" and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "CHECK_SELECTED_ISOLATED_INVOCATION")
    report = {"schema": "DMKN_MANAGED_OPERATOR_INSTALLED_LIFECYCLE_RESULT_V1", "status": "FAIL",
        "stage": "input", "input_sha256": args.input_sha, "original_deadline": DEADLINE,
        "full_v5_release": False, "mathematical_acceptance": False, "global_complete": False,
        "public_deployment_qualified": False, "independent_hosts": False,
        "unclean_recovery_retirement_tested": False, "physical_envelope_adopted": False,
        "proof_calls": 0, "native_calls": 0, "verifier_calls": 0, "trust_adoptions": 0}
    try:
        input_path = ordinary(args.input)
        need(input_path == output.parent/(NAME+"-input.json"), "CHECK_INPUT_LOCATION")
        raw = read(input_path)
        need(sha(raw) == args.input_sha, "CHECK_INPUT_SHA")
        execute(output, strict(raw), report)
        active()
    except BaseException as error:
        report["status"] = "FAIL"
        report["error"] = {"type": type(error).__name__, "message": str(error)[:2000]}
    report["wall_seconds"] = time.monotonic()-STARTED
    save(output/(NAME+"-result.json"), report)
    print(json.dumps({"status": report["status"], "stage": report["stage"],
                      "wall_seconds": report["wall_seconds"]}, sort_keys=True), flush=True)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

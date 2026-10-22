"""Four installed storage-boundary commands; source selected before any run.

No SDK import, SQL connection, credential read, mathematical operation,
reclamation or retry. All product calls use the ordinary installed public CLI.
"""
import time
STARTED = time.monotonic()
DEADLINE = STARTED + 580
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import secrets
import sys

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
NAME = "managed-storage-installed-01"
INSTALL = PROJECT/"product-local/v5-distribution-managed-storage-01/Mathematical Commons v5"
BUILD_INPUT = PROJECT/"experiments/v5-local-checks/distribution-managed-storage-01-input.json"
SUPPORT = "software/v5/managed_operator/installed_lifecycle.py"
SUPPORT_SHA = "b64579269104b866e5ed45aeef121e799bcd8c505532913a5a5faf687c9c310e"
MIB = 1024**2
STORAGE = "DMKN_V5_MANAGED_APPARENT_STREAMS_P4096_S65536_A1_V1"
REGISTRY_BOUND = 9372161
GENERATION_BOUND = 252035073
PINS = {
    "v5/client/managed_owner.py": "6991ac58310b0c3a6456f033bff7bccbb02dd1299c67716d805762e0dea69a0f",
    "v5/client/serve_generations.py": "e12f3899f28cab8a95a9b497a6a7f5148cdc537912bed3d357310e2c0d220a83",
    "v5/client/workspace_evidence.py": "d94e38257444da3bda04e4d9b298d422280a573becc27eaa063fdbc01f9c02a2",
    "v5/custody/module_store.py": "580515e461c95b424bc59011b8bf87e4776039f7d6cb87c27599f295c602dcbb",
    "v5/evidence_network/custody.py": "4264841e55ebc21899d8967ef9ac439d0682da5ea4a0d1c2097eddc930f1300e",
    "v5/discovery/discovery_store.py": "7f3c884b3ef3455e51563d233a2ca4a19087bc8097186e6b43e949abededa2c5",
    "v5/placement/ledger.py": "59f87b9334c44a8a9f8feb236084f419081d2484582917aded55eaac15f8351d",
    "v5/placement/advertisement.py": "13b0ef1ae400990f237e5e1957a77008d7f2ac51fb96758560152cfda3ecdf28",
    "v5/placement/lifecycle.py": "0fa3dcc4285aa4afc87dfda5741e5c68334f8c0398138c3f218351e705a1f427",
    "v5/placement/sessions.py": "6e07010c47b0e95abbb80125e838b759e2a4206bdc3cafa735e31c7015d1a63b",
    "v5/placement/storage_profile.py": "3b535a337c1731ead3b9930c7cbe1f7c340a17152bd8b57e32981552ec061c90",
    "v5/placement/storage_paths.py": "e1bcba2730e432b4dfc428d9c56ebb2e5b7bc0f4d8a9bfa0751b8818557eb9da",
    "portable/location/intent.mjs": "6c30e8793f737f0512e3e7e9d785d1311cafa35116784f4f8b3dda5c1a75fa29",
    "portable/location/maintained_roles.mjs": "d69d0b123e52f5cfbf4c2eef2e2d2dfecf9b9b11c9ddfabc4c5e37499e1a12e0",
}


def need(value, reason):
    if not value: raise ValueError(reason)


def active(reserve=0):
    need(time.monotonic()+reserve < DEADLINE, "CHECK_ORIGINAL_DEADLINE")


def load_support(output):
    path = output/"sources"/SUPPORT
    with path.open("rb") as stream: raw = stream.read(25839)
    need(len(raw) == 25838 and hashlib.sha256(raw).hexdigest() == SUPPORT_SHA, "CHECK_SUPPORT_PIN")
    spec = importlib.util.spec_from_file_location("_storage_public_support", path)
    need(spec.name not in sys.modules, "CHECK_SUPPORT_COLLISION")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def clean_process(value, success):
    expected = "COMMAND_EXITED_ZERO_AND_CLOSED" if success else "COMMAND_FAILED"
    need(value["status"] == expected and value["child_exit_code"] == (0 if success else 1)
         and value["direct_child_reaped"] is True and value["job_closed"] is True
         and value["cleanup_errors"] == [] and value["termination_requested"] is False
         and value["final_job"]["active_processes"] == 0
         and value["final_job"]["terminated_processes"] == 0,
         "CHECK_CLEAN_EXPECTED_PROCESS_RESULT")
    need(value["final_job"]["cpu_seconds"] <= value["limits"]["cpu_seconds"]
         and value["wall_seconds_through_cleanup"] <= value["limits"]["wall_seconds"]
         and all(value["observed_logs"][key] <= value["limits"][key]
                 for key in ("stdout_bytes", "stderr_bytes")), "CHECK_PROCESS_BUDGET")


def refusal(value, code):
    need(value["status"] == "FAILED" and value["error"] ==
         {"type": "ValueError", "message": code, "notes": []}, "CHECK_EXACT_OWNER_REFUSAL")


def plan_check(H, raw, selected):
    plan = H.strict(raw)
    need(plan["sources"] == {**selected, "owner/managed_owner.py": selected["v5/client/managed_owner.py"]}
         and len(plan["sources"]) == 130 and plan["owner_entry"] == "managed_owner.py"
         and plan["installation_root"] == str(INSTALL/"base"), "CHECK_EXACT_130_PLAN")
    return plan


def boot_check(H, value, raw, selected):
    plan_check(H, raw, selected)
    need(value["schema"] == "DMKN_V5_CLIENT_BOOT_RESULT_V1" and value["status"] == "OWNER_EXITED_ZERO"
         and value["source_files"] == 130 and value["plan_sha256"] == H.sha(raw), "CHECK_130_BOOT")
    origins = {name: path.replace("\\", "/") for name, path in value["imported_origins"].items()}
    need(all(path in selected for path in origins.values()), "CHECK_IMPORTED_SOURCE_ORIGINS")
    for name in ("placement.lifecycle", "placement.sessions", "placement.storage_profile",
                 "placement.storage_paths", "client.serve_generations", "client.workspace_evidence",
                 "custody.module_store", "evidence_network.custody", "discovery.discovery_store",
                 "placement.ledger", "placement.advertisement"):
        need(origins.get(name) == "v5/"+name.replace(".", "/")+".py", "CHECK_STORAGE_IMPORTED_ORIGIN")


def database_metadata(H, path, pages):
    H.ordinary(path)
    before = path.stat()
    need(before.st_nlink == 1 and 4096 <= before.st_size <= pages*4096
         and before.st_size % 4096 == 0, "CHECK_ACTUAL_DATABASE_LENGTH")
    for suffix in ("-journal", "-wal", "-shm"):
        need(not os.path.lexists(str(path)+suffix), "CHECK_CLOSED_DATABASE_SIDECAR")
    # The fixed header is nonsecret. No SQLite connection or payload scan.
    with path.open("rb") as stream: header = stream.read(100)
    after = path.stat()
    need((before.st_size, before.st_mtime_ns, before.st_ino) ==
         (after.st_size, after.st_mtime_ns, after.st_ino), "CHECK_DATABASE_HEADER_RACE")
    need(len(header) == 100 and header[:16] == b"SQLite format 3\0"
         and int.from_bytes(header[16:18], "big") == 4096
         and header[18:20] == b"\x01\x01"
         and int.from_bytes(header[52:56], "big") == 0, "CHECK_ACTUAL_DATABASE_FORMAT")
    return {"path": str(path), "bytes": before.st_size, "page_cap": pages,
            "header_sha256": H.sha(header), "header_read_bytes": 100,
            "connection_local_pragmas_inferred_from_header": False}


def execute(H, output, supplied, report):
    active()
    need(set(supplied) == {"schema", "installation_root", "release_sha256", "template"}
         and supplied["schema"] == "DMKN_MANAGED_STORAGE_INSTALLED_INPUT_V1"
         and supplied["installation_root"] == str(INSTALL), "CHECK_SELECTED_INPUT")
    H.ordinary(INSTALL, directory=True)
    release_raw = H.read(INSTALL/"V5-RELEASE.json", 8*MIB)
    need(H.sha(release_raw) == supplied["release_sha256"], "CHECK_EXACT_RELEASE")
    release = H.strict(release_raw)
    need(release["schema"] == "DMKN_V5_DIRECTORY_RELEASE_V3"
         and release["base_role"] == "mathematical-client-location-v1"
         and release["base_manifest_sha256"] == H.BASE_SHA, "CHECK_EXACT_BASE_ROLE")
    sdk = release["sdk_sources"]
    need(type(sdk) is dict and len(sdk) == 129, "CHECK_129_SDK")
    for logical, relative in sdk.items():
        parts = PurePosixPath(logical).parts
        need(relative == "sdk/"+logical and len(parts) >= 2 and parts[0] in ("v5", "portable")
             and PurePosixPath(logical).as_posix() == logical
             and all(part not in ("", ".", "..") for part in parts)
             and "\\" not in logical and ":" not in logical, "CHECK_LOGICAL_SOURCE_PATH")
    selected = {logical: release["files"][relative] for logical, relative in sdk.items()}
    build_raw = H.read(BUILD_INPUT, 8*MIB)
    need(H.sha(build_raw) == release["build_input_sha256"], "CHECK_SELECTED_BUILD_INPUT")
    build = H.strict(build_raw)
    need(selected == {logical: {key: row[key] for key in ("bytes", "sha256")}
                      for logical, row in build["sdk_sources"].items()}, "CHECK_COMPLETE_BUILD_MAP")
    for logical, sha in PINS.items(): need(selected[logical]["sha256"] == sha, "CHECK_STORAGE_SOURCE_PIN")
    for logical, row in selected.items():
        active(); H.pin(INSTALL/"sdk"/logical, row, 2*MIB)
    owner = selected["v5/client/managed_owner.py"]
    H.pin(INSTALL/"distribution.py", release["files"]["distribution.py"], 2*MIB)
    manifest_raw = H.read(INSTALL/"base/RELEASE-MANIFEST.json", 8*MIB)
    need(H.sha(manifest_raw) == H.BASE_SHA, "CHECK_BASE_MANIFEST")
    base = H.strict(manifest_raw)["files"]
    helpers = {key: base[key] for key in ("operator/commons.py", "receiver/helpers/domains.py",
                                         "receiver/helpers/run_stage.py")}
    need(helpers["operator/commons.py"]["sha256"] == H.OPERATOR_SHA
         and helpers["receiver/helpers/run_stage.py"]["sha256"] == H.JOB_SHA, "CHECK_FIXED_SUPERVISOR")
    A = H.load_helper("_storage_public_supervisor", INSTALL/"base/operator/commons.py", helpers["operator/commons.py"])
    H.load_helper("domains", INSTALL/"base/receiver/helpers/domains.py", helpers["receiver/helpers/domains.py"])
    J = H.load_helper("_storage_public_job", INSTALL/"base/receiver/helpers/run_stage.py", helpers["receiver/helpers/run_stage.py"])
    writer = H.digest("DMKN-V5-MANAGED-STORAGE-WRITER-V1", {
        "storage_profile": STORAGE, "base_manifest_sha256": H.BASE_SHA, "sdk_sources": selected})
    profile = H.digest("DMKN-V5-INSTALLED-MANAGED-WORKER-V2", {
        "release_sha256": supplied["release_sha256"], "base_manifest_sha256": H.BASE_SHA,
        "sources": selected, "owner_entry": "managed_owner.py", "helpers": helpers,
        "role": "DMKN_V5_MANAGED_OWNER_WORKER_V2", "ownership": H.OWNERSHIP})
    template = supplied["template"]
    need(template == {"path": str(H.TEMPLATE), "bytes": 53427, "sha256": H.TEMPLATE_SHA}, "CHECK_DATA_ONLY_TEMPLATE")
    generation = deepcopy(H.strict(H.pin(H.TEMPLATE, {k: template[k] for k in ("bytes", "sha256")}))["retired"]["config"])
    del generation["placement"]["generation"]
    need(generation["placement"]["admission_close_ms"] == 1577836798000
         and generation["placement"]["retention_not_after_ms"] == 1577836799000
         and generation["placement"]["max_runs"] == 1, "CHECK_ORIGINAL_TEMPLATE_SCOPE")
    operations, commands, inputs = output/"operations", output/"public-commands", output/"inputs"
    for path in (operations, commands, inputs): H.ordinary(path, fresh=True).mkdir()
    manager_root = H.ordinary(output/"managed", fresh=True)
    refused_root = H.ordinary(output/"registry-refused", fresh=True)
    ports = H.free_ports()
    epoch = secrets.token_hex(32)
    slots = [{"reserved_bytes": GENERATION_BOUND, "max_cells": 1, "max_runs": 1,
              "read_endpoint": H.endpoint(ports[i]), "intake_endpoint": H.endpoint(ports[i+1]),
              "listen": ["/ip4/127.0.0.1/tcp/"+str(ports[i+2])]} for i in (0, 3)]
    manager = dict(schema="DMKN_V5_TWO_GENERATION_MANAGER_STORAGE_V1", epoch=epoch,
        clock_model_id=secrets.token_hex(32), registry_pages=64,
        owner_reserved_bytes=2*GENERATION_BOUND+REGISTRY_BOUND+2*MIB,
        registry_reserved_bytes=REGISTRY_BOUND, cleanup_reserved_bytes=2*MIB,
        max_sessions=2, slots=slots, storage_profile=STORAGE, writer_profile_sha256=writer,
        protected_roots=[str(p) for p in (INSTALL, output/"sources", operations, commands, inputs)])
    egress = dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
                  test_endpoints=[dict(host="127.0.0.1", port=port) for port in ports])
    generation["placement"].update(service_epoch=epoch, ledger_pages=256)
    generation["egress"] = deepcopy(egress)
    generation["location"].update(egress=deepcopy(egress), listen=slots[0]["listen"],
                                   endpoints=[slots[0]["read_endpoint"]])
    # Materialize the prior four non-page defaults; only page admission changes.
    generation["location"]["limits"]["metadata"] = dict(entries=16384, bytes=16*MIB,
        valueBytes=32768, providersPerKey=32, pages=256)
    generation["service_limits"]["journal_pages"] = 256
    generation["workspace"]["ledger_pages"] = 256
    generation["workspace"]["module_limits"]["db_pages"] = 256
    generation["workspace"]["packet_limits"]["db_pages"] = 256
    generation["workspace"]["index_limits"]["max_db_pages"] = 256
    database_bound = lambda pages: 139272*pages+327680
    need(database_bound(64)+131073 == REGISTRY_BOUND
         and 7*database_bound(256)+34816+131073 == GENERATION_BOUND
         and manager["owner_reserved_bytes"] == 515539459, "CHECK_INDEPENDENT_EXACT_ARITHMETIC")
    common = dict(schema="DMKN_V5_MANAGED_OWNER_V2", release_sha256=supplied["release_sha256"],
        manager_root=str(manager_root), manager_config=manager, owner_limits=dict(calls=64, cpu_seconds=25))
    report.update(release_sha256=supplied["release_sha256"], build_input_sha256=H.sha(build_raw),
        profile_sha256=profile, storage_writer_profile_sha256=writer, manager_root=str(manager_root),
        manager_config=manager, generation_config=generation, operations=[],
        envelope=dict(registry_bound_bytes=REGISTRY_BOUND, generation_bound_bytes=GENERATION_BOUND,
            owner_charged_bytes=manager["owner_reserved_bytes"], scope="CONDITIONAL_APPARENT_MANAGED_DATA_STREAM_BYTES"))

    def public(name, parameters, *, serving=False, success=True):
        wrapper = H.limits(100, 180, 7) if serving else H.limits(15, 65, 7)
        active(wrapper["wall_seconds"]+20)
        request = dict(schema="DMKN_V5_INSTALLED_REQUEST_V1", name=name, workspace_root=str(operations),
            parameters=parameters, limits=H.limits(90, 140, 6) if serving else H.limits(12, 45, 6),
            output_limits=dict(bytes=64*MIB, entries=1024), runtime_mode="atomic",
            owner=dict(root=str(INSTALL/"sdk/v5/client"), entry="managed_owner.py", sources={"managed_owner.py": owner}))
        request_path = inputs/(name+".json"); request_sha = H.save(request_path, request)
        item = dict(name=name, expected_success=success, request_sha256=request_sha, artifacts={})
        report["operations"].append(item)
        argv = [str(INSTALL/"base/receiver/runtime/python/python.exe"), "-I", "-S", "-B",
                str(INSTALL/"distribution.py"), "launch", supplied["release_sha256"], "run", str(request_path), request_sha]
        observed = A.supervise(argv, PROJECT, commands/name, wrapper, J.Job)
        item["supervision"] = observed; H.save(commands/(name+"-result.json"), observed)
        run = operations/name
        paths = dict(plan=run/"plan.json", launch=run/"RESULT.json", boot=run/"BOOT-RESULT.json",
            boot_failure=run/"BOOT-FAILED.json", owner=run/"work/managed-result.json",
            request=operations/(name+"-request")/"request.json",
            prepared_plan=operations/(name+"-request")/"launch.json")
        if serving:
            child = run/"work/managed-worker"
            paths.update(worker_plan=child/"plan.json", worker_boot=child/"BOOT-RESULT.json",
                worker_boot_failure=child/"BOOT-FAILED.json", worker_owner=child/"work/managed-result.json")
        values, raws = {}, {}
        for key, path in paths.items():
            if path.exists():
                raw = H.read(path); raws[key], values[key] = raw, H.strict(raw)
                item["artifacts"][key] = dict(path=str(path), bytes=len(raw), sha256=H.sha(raw))
        # Capture failures first. An expected nonzero exit is never called success.
        clean_process(observed, success)
        required = {"plan", "launch", "owner", "request", "prepared_plan"}
        required.add("boot" if success else "boot_failure")
        if serving: required |= {"worker_plan", "worker_owner", "worker_boot" if success else "worker_boot_failure"}
        need(required <= set(values), "CHECK_REQUIRED_PUBLIC_EVIDENCE")
        need(values["request"] == request and raws["plan"] == raws["prepared_plan"], "CHECK_PUBLIC_REQUEST_BINDING")
        launch, result = values["launch"], values["owner"]
        need(launch["schema"] == "DMKN_V5_CLIENT_LAUNCH_RESULT_V1"
             and launch["plan_sha256"] == H.sha(raws["plan"]) and launch["final_error"] is None
             and launch["status"] == (H.SUCCESS if success else "COMMAND_FAILED"), "CHECK_PUBLIC_LAUNCH")
        clean_process(launch["result"], success)
        plan = plan_check(H, raws["plan"], selected)
        need(plan["parameters"] == parameters and plan["limits"] == request["limits"], "CHECK_PARAMETERS")
        need(result["schema"] == "DMKN_V5_MANAGED_OWNER_RESULT_V2" and result["operation"] == parameters["operation"]
             and result["profile_sha256"] == profile and result["storage_writer_profile_sha256"] == writer,
             "CHECK_AUTHENTICATED_OWNER_BINDINGS")
        H.claim_flags(result)
        if success:
            need("boot_failure" not in values and result["status"] == "COMPLETE", "CHECK_OWNER_SUCCESS")
            boot_check(H, values["boot"], raws["plan"], selected)
        else:
            need("boot" not in values and values["boot_failure"] == {
                "status": "CLIENT_BOOT_OR_OWNER_FAILED", "error": "ValueError: CLIENT_OWNER_NONZERO_OR_INVALID_RESULT"},
                "CHECK_EXPECTED_FAILED_BOOT")
        if serving:
            child_plan = plan_check(H, raws["worker_plan"], selected)
            expected = deepcopy(plan)
            expected.update(name="managed-worker", workspace_root=str(run/"work"),
                source_roots={key: str(run/"sources"/key) for key in ("v5", "portable", "owner")},
                limits=parameters["inner_limits"], parameters=dict(schema="DMKN_V5_MANAGED_OWNER_WORKER_V2",
                    request=parameters, profile_sha256=profile, parent_plan_sha256=H.sha(raws["plan"])))
            need(child_plan == expected and result["worker_plan_sha256"] == H.sha(raws["worker_plan"])
                 and result["worker"] == values["worker_owner"], "CHECK_EXACT_WORKER_DERIVATION")
            worker = values["worker_owner"]
            need(worker["schema"] == "DMKN_V5_MANAGED_OWNER_RESULT_V2" and worker["operation"] == "serve"
                 and worker["profile_sha256"] == profile and worker["storage_writer_profile_sha256"] == writer,
                 "CHECK_WORKER_STORAGE_PROFILE")
            H.claim_flags(worker); clean_process(result["supervision"], success)
            need(result["supervision"]["session_recovery"] == dict(status="QUIESCED", unclean_slots=[],
                orderly_close_claim=False, mathematical_acceptance=False), "CHECK_EXACT_QUIESCENCE")
            if success:
                need("worker_boot_failure" not in values and result["worker_boot"] == values["worker_boot"],
                     "CHECK_WORKER_BOOT_COMPLETION")
                boot_check(H, values["worker_boot"], raws["worker_plan"], selected)
            else:
                need("worker_boot" not in values and result["worker_boot_failure"] == values["worker_boot_failure"]
                     and values["worker_boot_failure"] == values["boot_failure"], "CHECK_WORKER_FAILED_BOOT")
        active()
        return result

    report["stage"] = "registry-refusal"
    under = deepcopy(common)
    under.update(operation="initialize", manager_root=str(refused_root))
    under["manager_config"]["registry_reserved_bytes"] -= 1
    rejected_registry = public("registry-refusal", under, success=False)
    refusal(rejected_registry, "MANAGED_STORAGE_REGISTRY_RESERVATION")
    need(not os.path.lexists(refused_root), "CHECK_REGISTRY_REFUSAL_BEFORE_MANAGED_WRITE")
    report["registry_refusal_before_managed_write"] = True

    def service_parameters(config, create):
        return dict(**deepcopy(common), operation="serve", create_manager=create,
            selection=dict(slot=0, generation_config=config), inner_limits=H.limits(60, 80, 3),
            worker_owner_limits=dict(calls=64, cpu_seconds=35), startup_seconds=20, service_seconds=2,
            close_seconds=25, boot_tail_seconds=10, parent_tail_seconds=10, supervisor_cleanup_seconds=25,
            seal_before_close=True, restore_requests=[], tls=dict(read=None, intake=None), intake_grant=None)

    report["stage"] = "allocation-refusal"
    excessive = deepcopy(generation); excessive["workspace"]["ledger_pages"] = 257
    rejected = public("allocation-refusal", service_parameters(excessive, True), serving=True, success=False)
    refusal(rejected, "MANAGED_OWNER_SUPERVISED_OPERATION_FAILED")
    first = rejected["worker"]
    refusal(first, "MANAGED_STORAGE_GENERATION_RESERVATION")
    need(not any(key in first for key in ("allocation", "generation", "ready", "closures", "close_errors"))
         and first["service_close_observation"]["observation_status"] == "NO_OWNED_SERVICE", "CHECK_NO_GENERATION_ACTORS")
    empty = first["manager"]
    need(empty["allocated_sequence"] == empty["retired_floor"] == 0 and empty["slots"] == [None, None]
         and empty["session"]["number"] == first["join"]["number"] == 1
         and empty["session"]["state"] == "BOUND"
         and empty["session"]["profile_sha256"] == profile
         and empty["session"]["worker"] == first["join"]["worker"], "CHECK_CHARGED_FAILED_SESSION_ONLY")
    for slot in (0, 1):
        path = H.ordinary(manager_root/str("slot-"+str(slot)), directory=True)
        need(not any(path.iterdir()), "CHECK_ALLOCATION_REFUSAL_NO_GENERATION_PATH")
    marker_raw = H.read(manager_root/"manager.json")
    need(H.strict(marker_raw) == dict(schema=manager["schema"], root=str(manager_root),
         config_sha256=H.sha(H.encode(manager))), "CHECK_IMMUTABLE_MANAGER_MARKER")
    report["allocation_refusal"] = dict(reason="MANAGED_STORAGE_GENERATION_RESERVATION",
        charged_session_number=1, allocated_sequence=0, slots=[None, None], run_charge_created=False,
        quiescence=rejected["supervision"]["session_recovery"], failed_command_preserved=True)
    retained = {row["path"]: {key: row[key] for key in ("bytes", "sha256")}
                for item in report["operations"] for row in item["artifacts"].values()}

    report["stage"] = "serve"
    served = public("serve", service_parameters(deepcopy(generation), False), serving=True)
    worker = served["worker"]; state = worker["manager"]; record = state["slots"][0]
    need(state["allocated_sequence"] == 1 and state["retired_floor"] == 0 and state["slots"][1] is None
         and record["slot"] == 0 and record["sequence"] == record["runs"] == 1
         and record["run_state"] == "CLOSED" and record["phase"] == "SEALED_SERVING"
         and record["failure"] is None and "quiescence" not in record, "CHECK_ONE_REAL_CLOSED_GENERATION")
    expected_generation = H.digest("DMKN-V5-TWO-SLOT-GENERATION-V1", {
        "manager": H.sha(marker_raw), "sequence": 1, "slot": 0, "config": generation})
    need(record["generation"] == served["generation"] == worker["generation"] == expected_generation,
         "CHECK_EXACT_GENERATION_ID")
    bound = deepcopy(generation); bound["placement"]["generation"] = expected_generation
    need(record["config"] == bound and worker["allocation"]["config"] == bound
         and worker["allocation"]["runs"] == 0 and worker["allocation"]["sequence"] == 1
         and worker["ready"]["run"] == 1 and worker["ready"]["physical_envelope_adopted"] is False
         and worker["sealed"]["phase"] == "SEALED_SERVING" and worker["intake_handoff"] is None
         and worker["restored"] == [] and not worker.get("close_errors")
         and len(worker["closures"]) == 1, "CHECK_EXACT_VALID_ALLOCATION")
    closed = worker["closures"][0]
    need(closed["status"] == "CLOSED" and closed["cleanup"]["errors"] == []
         and all(closed["cleanup"][key] is True for key in H.CLEANUP)
         and closed["bindings"]["generation"] == expected_generation
         and record["closure_sha256"] == H.sha(H.encode(closed)), "CHECK_GENUINE_CLOSE_DIGEST")
    H.claim_flags(closed)
    location = closed["observed"]["location"]
    need(location["closed"] is True and location["returncode"] == 0
         and location["forced_termination"] is False and location["channel_failed"] is False,
         "CHECK_ACTUAL_NODE_ORDERLY_CLOSE")
    need(state["session"]["number"] == worker["join"]["number"] == record["session"]["number"] == 2
         and state["session"]["state"] == "BOUND"
         and state["session"]["profile_sha256"] == profile
         and state["session"]["nonce"] == worker["join"]["nonce"] == record["session"]["nonce"]
         and state["session"]["worker"] == worker["join"]["worker"] == record["session"]["worker"],
         "CHECK_FAILED_SESSION_NOT_REFUNDED")

    report["stage"] = "status"
    final = public("status", dict(**deepcopy(common), operation="status"))["manager"]
    expected_state = deepcopy(state); expected_state["session"]["state"] = "QUIESCED"
    need(final == expected_state and final["reserved_bytes"] == 2*GENERATION_BOUND
         and final["physical_envelope_adopted"] is False, "CHECK_PUBLIC_PROFILE_REOPEN_AND_CLOSED_PRESERVED")
    need(H.read(manager_root/"manager.json") == marker_raw and not os.path.lexists(refused_root),
         "CHECK_MARKER_AND_REFUSAL_ROOT_PRESERVED")
    for path, row in retained.items(): active(); H.pin(Path(path), row)
    root = manager_root/"slot-0/g00000000000000000001"
    dbpaths = [manager_root/"generations.sqlite", *[root/path for path in (
        "workspace/workspace.sqlite", "workspace/modules/modules.sqlite",
        "workspace/packets/evidence-packets.sqlite", "workspace/index/discovery.sqlite",
        "workspace/placement.sqlite", "workspace/placement-routes.sqlite",
        "run-0001/location-state/metadata.sqlite")]]
    metadata = [database_metadata(H, path, 64 if i == 0 else 256) for i, path in enumerate(dbpaths)]
    for relative, cap in (("run-0001/location-state/identity.key", 1024),
                          ("run-0001/location-state/adopted.json", 1024)):
        file = H.ordinary(root/relative); stat = file.stat()
        need(stat.st_nlink == 1 and 0 < stat.st_size <= cap, "CHECK_NODE_IDENTITY_METADATA_ONLY")
    need(not any((root/"workspace/operations").iterdir()), "CHECK_NO_MATHEMATICAL_OPERATIONS")
    active()
    report.update(status="PASS", stage="complete", final_state=final,
        generation=expected_generation, closure_sha256=record["closure_sha256"], database_metadata=metadata,
        retained_failure_artifacts=len(retained), actual_node_started_and_closed=True,
        secret_bytes_read=False, public_commands=4, failed_session_charge_retained=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True); parser.add_argument("--input", required=True)
    parser.add_argument("--input-sha", required=True); args = parser.parse_args()
    output = Path(args.output)
    need(output == PROJECT/"experiments/v5-local-checks"/NAME and Path.cwd() == PROJECT
         and Path(__file__) == output/"sources/software/v5/managed_storage/installed_controls.py"
         and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "CHECK_EXACT_SELECTED_INVOCATION")
    H = load_support(output)
    report = dict(schema="DMKN_MANAGED_STORAGE_INSTALLED_RESULT_V1", status="FAIL", stage="input",
        mathematical_acceptance=False, full_v5_release=False, independent_hosts=False,
        public_deployment_qualified=False, physical_envelope_adopted=False, deletion_performed=False)
    try:
        raw = H.read(Path(args.input), 2*MIB)
        need(H.sha(raw) == args.input_sha, "CHECK_EXACT_INPUT_SHA")
        execute(H, output, H.strict(raw), report)
    except BaseException as error:
        report["error"] = dict(type=type(error).__name__, message=str(error)[:1000])
    report["elapsed_seconds"] = time.monotonic()-STARTED
    H.save(output/"managed-storage-installed-result.json", report)
    print(json.dumps({"status": report["status"], "stage": report["stage"]}, separators=(",", ":")))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())

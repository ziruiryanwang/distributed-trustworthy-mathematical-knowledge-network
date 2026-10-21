"""One finite ordinary managed-owner/contributor handoff, no new proof work.

Services run through the unchanged public distribution/boot/supervisor. This
trusted local check reads closed databases only after both actors have exited.
It never retires/reclaims data or retries a failed operation.
"""
import time
STARTED = time.monotonic()
DEADLINE = STARTED+400
import argparse
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import secrets
import socket
import sqlite3
import sys

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
NAME = "managed-contribution-02"
INSTALL = PROJECT/"product-local/v5-distribution-managed-observed-01/Mathematical Commons v5"
SUPPORT = "software/v5/managed_operator/installed_lifecycle.py"
SUPPORT_SHA = "b64579269104b866e5ed45aeef121e799bcd8c505532913a5a5faf687c9c310e"
MIB = 1024**2
QUOTE = dict(index_calls=2, new_cells=1, placements=1, recovery_passes=1,
    reply_bytes=517519, requests=3, storage_bytes=34138740, structural_bytes=17010880,
    wire_overhead_bytes=98304)
MODULE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
PACKET = (447887, "a737e8f650e9d3abb4781bb2c85c0e625ed4573b7170d71aff1799dbb54495e3")
OPENING = (1595, "0c74d294730fc2d005a082aba01350e5a9ab54a5aa797036f35d607ce17c900a")


def need(value, reason):
    if not value: raise ValueError(reason)


def load_support(output):
    path = output/"sources"/SUPPORT
    raw = path.read_bytes()
    need(len(raw) == 25838 and hashlib.sha256(raw).hexdigest() == SUPPORT_SHA, "SUPPORT_PIN")
    spec = importlib.util.spec_from_file_location("_managed_public_support", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def ports():
    streams = []
    try:
        for unused in range(7):
            stream = socket.socket(); streams.append(stream); stream.bind(("127.0.0.1", 0))
        result = [s.getsockname()[1] for s in streams]
        need(len(set(result)) == 7, "DISTINCT_PORTS")
        return result
    finally:
        for stream in streams: stream.close()


def db_read(H, path, queries):
    H.ordinary(path)
    before = H.read(path, 16*MIB)
    need(not Path(str(path)+"-wal").exists() and not Path(str(path)+"-journal").exists(), "CLOSED_SQLITE_ONLY")
    connection = sqlite3.connect(path.as_uri()+"?mode=ro&immutable=1", uri=True)
    try:
        need(connection.execute("PRAGMA integrity_check").fetchone() == ("ok",), "SQLITE_INTEGRITY")
        rows = [connection.execute(sql, args).fetchall() for sql, args in queries]
        need(all(len(items) <= 4 for items in rows), "SQLITE_FIXTURE_ROWS")
    finally: connection.close()
    need(H.read(path, 16*MIB) == before, "IMMUTABLE_SQLITE_UNCHANGED")
    return rows, {"path": str(path), "bytes": len(before), "sha256": H.sha(before)}


def check_no_leak(H, credential, paths):
    # This local diagnostic never returns/logs the token or a credential object.
    raw = H.pin(Path(credential["path"]), {k: credential[k] for k in ("bytes", "sha256")}, 8192)
    secret = H.strict(raw)["token"].encode("ascii")
    need(len(secret) == 64, "PRIVATE_TOKEN_SHAPE")
    need(len(paths) <= 100, "PUBLIC_SCAN_COUNT")
    count = total = 0
    for path in sorted(set(paths)):
        if not path.exists(): continue
        content = H.read(path, 2*MIB); total += len(content); count += 1
        need(total <= 16*MIB and secret not in content, "PUBLIC_SECRET_LEAK_OR_SCAN_BOUND")
    return {"files": count, "bytes": total, "raw_token_found": False,
            "scope": "SELECTED_PUBLIC_CONTROL_REPORT_STDOUT_STDERR_ONLY"}


def execute(H, output, supplied, report):
    need(set(supplied) == {"schema", "release_sha256", "template", "fixtures", "horizons",
                          "contributor", "credential_directory", "private_directory_adoption"}
         and supplied["schema"] == "DMKN_MANAGED_CONTRIBUTION_CHECK_V1", "SELECTED_INPUT")
    release_raw = H.read(INSTALL/"V5-RELEASE.json", 8*MIB)
    need(H.sha(release_raw) == supplied["release_sha256"], "EXACT_RELEASE")
    release = H.strict(release_raw)
    sdk = release["sdk_sources"]
    need(release["base_manifest_sha256"] == H.BASE_SHA and len(sdk) == 127
         and all(relative == "sdk/"+logical for logical, relative in sdk.items()), "EXACT_127_RELEASE")
    selected = {logical: release["files"][relative] for logical, relative in sdk.items()}
    for logical, pin in H.PINS.items(): need(selected[logical]["sha256"] == pin, "FROZEN_PRODUCT_SOURCE")
    owner = selected["v5/client/managed_owner.py"]
    H.pin(INSTALL/"distribution.py", release["files"]["distribution.py"], 2*MIB)
    manifest_raw = H.read(INSTALL/"base/RELEASE-MANIFEST.json", 8*MIB)
    need(H.sha(manifest_raw) == H.BASE_SHA, "EXACT_BASE_MANIFEST")
    base = H.strict(manifest_raw)["files"]
    helpers = {key: base[key] for key in ("operator/commons.py", "receiver/helpers/domains.py", "receiver/helpers/run_stage.py")}
    need(helpers["operator/commons.py"]["sha256"] == H.OPERATOR_SHA
         and helpers["receiver/helpers/run_stage.py"]["sha256"] == H.JOB_SHA, "FIXED_SUPERVISOR")
    A = H.load_helper("_contribution_check_supervisor", INSTALL/"base/operator/commons.py", helpers["operator/commons.py"])
    H.load_helper("domains", INSTALL/"base/receiver/helpers/domains.py", helpers["receiver/helpers/domains.py"])
    J = H.load_helper("_contribution_check_job", INSTALL/"base/receiver/helpers/run_stage.py", helpers["receiver/helpers/run_stage.py"])
    profile = H.digest("DMKN-V5-INSTALLED-MANAGED-WORKER-V2", {
        "release_sha256": supplied["release_sha256"], "base_manifest_sha256": H.BASE_SHA,
        "sources": selected, "owner_entry": "managed_owner.py", "helpers": helpers,
        "role": "DMKN_V5_MANAGED_OWNER_WORKER_V2", "ownership": H.OWNERSHIP})
    template = supplied["template"]
    need(template == {"path": str(H.TEMPLATE), "bytes": 53427, "sha256": H.TEMPLATE_SHA}, "DATA_ONLY_TEMPLATE")
    generation = deepcopy(H.strict(H.pin(H.TEMPLATE, {k: template[k] for k in ("bytes", "sha256")}))["retired"]["config"])
    del generation["placement"]["generation"]
    horizon = supplied["horizons"]
    need(set(horizon) == {"selected_ms", "write_until_ms", "admission_close_ms", "retention_end_ms",
                          "retention_until_ms", "retention_not_after_ms"}
         and all(type(v) is int for v in horizon.values()), "EXACT_HORIZONS")
    now = int(time.time()*1000)
    need(horizon["selected_ms"] <= now and now+300000 < horizon["write_until_ms"]
         < horizon["admission_close_ms"] < horizon["retention_end_ms"]
         < horizon["retention_until_ms"] < horizon["retention_not_after_ms"]
         <= horizon["selected_ms"]+1200000, "ORIGINAL_FINITE_LIVE_HORIZONS")
    credential_dir = H.ordinary(supplied["credential_directory"], directory=True)
    need(credential_dir == PROJECT/"experiments/v5-private-credentials/managed-contribution-02"
         and not any(credential_dir.iterdir())
         and supplied["private_directory_adoption"]["policy"] == "CURRENT_USER_AND_SYSTEM_PROTECTED_DACL_V1",
         "PRIVATE_DIRECTORY_ADOPTION")
    credential_path = credential_dir/"credentials.json"
    operations, commands, inputs = output/"operations", output/"public-commands", output/"inputs"
    for path in (operations, commands, inputs): H.ordinary(path, fresh=True).mkdir()
    manager_root = output/"managed"
    port = ports(); epoch = secrets.token_hex(32)
    slots = [{"reserved_bytes": 64*MIB, "max_cells": 1, "max_runs": 1,
              "read_endpoint": H.endpoint(port[i]), "intake_endpoint": H.endpoint(port[i+1]),
              "listen": [f"/ip4/127.0.0.1/tcp/{port[i+2]}"]} for i in (0, 3)]
    manager = dict(schema="DMKN_V5_TWO_GENERATION_MANAGER_SUPERVISED_V1", epoch=epoch,
        clock_model_id=secrets.token_hex(32), registry_pages=256, owner_reserved_bytes=132*MIB,
        registry_reserved_bytes=2*MIB, cleanup_reserved_bytes=2*MIB, max_sessions=1, slots=slots,
        protected_roots=[str(p) for p in (INSTALL, output/"sources", operations, commands, inputs, credential_dir)])
    egress = dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
                  test_endpoints=[dict(host="127.0.0.1", port=p) for p in sorted(port)])
    generation["placement"].update(service_epoch=epoch, limits=deepcopy(QUOTE),
        admission_close_ms=horizon["admission_close_ms"], retention_not_after_ms=horizon["retention_not_after_ms"])
    generation["egress"] = deepcopy(egress)
    generation["location"].update(egress=deepcopy(egress), listen=slots[0]["listen"], endpoints=[slots[0]["read_endpoint"]])
    generation["location"]["limits"]["service_ms"] = 210000
    generation["service_limits"].update(lifetime_seconds=120, controller_cpu_seconds=45, controller_calls=64)
    generation["service_limits"]["intake"]["operation_ms"] = 30000
    contributor = supplied["contributor"]
    contributor_path = output/"sources/software/v5/managed_contribution02/contributor.py"
    need(contributor["path"] == str(PROJECT/"software/v5/managed_contribution02/contributor.py"), "SELECTED_CONTRIBUTOR")
    contributor_pin = {k: contributor[k] for k in ("bytes", "sha256")}
    H.pin(contributor_path, contributor_pin)
    report.update(profile_sha256=profile, release_sha256=supplied["release_sha256"],
        horizons=horizon, manager_root=str(manager_root), manager_config=manager,
        generation_config=generation, operations=[])
    scan_paths = []

    def prepare(name, parameters, owner_entry, owner_root, owner_pin, serving):
        limits = H.limits(100, 300, 6) if serving else H.limits(35, 60, 3)
        request = dict(schema="DMKN_V5_INSTALLED_REQUEST_V1", name=name, workspace_root=str(operations),
            parameters=parameters, limits=limits, output_limits=dict(bytes=64*MIB, entries=1024),
            owner=dict(root=str(owner_root), entry=owner_entry, sources={owner_entry: owner_pin}), runtime_mode="atomic")
        path = inputs/(name+".json"); digest = H.save(path, request); scan_paths.append(path)
        item = dict(name=name, request_sha256=digest, artifacts={}); report["operations"].append(item)
        argv = [str(INSTALL/"base/receiver/runtime/python/python.exe"), "-I", "-S", "-B",
                str(INSTALL/"distribution.py"), "launch", supplied["release_sha256"], "run", str(path), digest]
        return item, request, argv, H.limits(125, 335, 7) if serving else H.limits(50, 85, 4)

    def complete(prepared, observed):
        item, request, unused, limits = prepared
        item["supervision"] = observed
        H.save(commands/(item["name"]+"-result.json"), observed)
        run = operations/item["name"]
        paths = {"plan": run/"plan.json", "launch": run/"RESULT.json", "boot": run/"BOOT-RESULT.json",
                 "owner": run/"work"/("managed-result.json" if item["name"] == "serve" else "contributor-result.json")}
        values = {}
        for key, path in paths.items():
            if path.exists():
                raw = H.read(path); values[key] = H.strict(raw)
                item["artifacts"][key] = dict(path=str(path), bytes=len(raw), sha256=H.sha(raw))
                scan_paths.append(path)
        H.check_supervision(observed)
        need(set(values) == set(paths), "PUBLIC_COMPLETION_ARTIFACTS")
        H.check_supervision(values["launch"]["result"])
        need(values["launch"]["status"] == H.SUCCESS and values["launch"]["final_error"] is None,
             "PUBLIC_LAUNCH_CLOSED")
        expected_sources = {**selected, "owner/"+request["owner"]["entry"]: next(iter(request["owner"]["sources"].values()))}
        need(values["plan"]["parameters"] == request["parameters"]
             and values["plan"]["sources"] == expected_sources
             and values["boot"]["status"] == "OWNER_EXITED_ZERO"
             and values["boot"]["source_files"] == 128
             and values["boot"]["plan_sha256"] == item["artifacts"]["plan"]["sha256"], "PUBLIC_BOOT_BINDING")
        return values

    common = dict(schema="DMKN_V5_MANAGED_OWNER_V2", release_sha256=supplied["release_sha256"],
        manager_root=str(manager_root), manager_config=manager, owner_limits=dict(calls=64, cpu_seconds=25))
    grant = dict(source=H.endpoint(port[6]), write_until_ms=horizon["write_until_ms"],
        retention_until_ms=horizon["retention_until_ms"], limits=deepcopy(QUOTE),
        credential_path=str(credential_path), confidentiality="OWNER_PROVISIONED_PRIVATE_CREDENTIAL_DIRECTORY_V1")
    service_parameters = dict(**common, operation="serve", create_manager=True,
        selection=dict(slot=0, generation_config=generation), inner_limits=H.limits(75, 230, 3),
        worker_owner_limits=dict(calls=64, cpu_seconds=40), startup_seconds=20, service_seconds=60,
        close_seconds=25, boot_tail_seconds=10, parent_tail_seconds=10, supervisor_cleanup_seconds=25,
        seal_before_close=True, restore_requests=[], tls=dict(read=None, intake=None), intake_grant=grant)
    hosting = prepare("serve", service_parameters, "managed_owner.py", INSTALL/"sdk/v5/client", owner, True)
    need(time.monotonic()+hosting[3]["wall_seconds"]+20 < DEADLINE, "ORIGINAL_DRIVER_HOST_RESERVATION")
    report["stage"] = "start-public-host"
    primary_error = None
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(A.supervise, hosting[2], PROJECT, commands/"serve", hosting[3], J.Job)
        try:
            worker_root = operations/"serve/work/managed-worker"
            ready_path = worker_root/"work/managed-ready.json"
            wait_until = min(STARTED+75, DEADLINE-150)
            ready = None
            while time.monotonic() < wait_until:
                if ready_path.exists():
                    try: ready = H.strict(H.read(ready_path))
                    except (ValueError, OSError): ready = None  # Fresh xb writer may not have closed yet.
                    if ready is not None: break
                need(not future.done(), "HOST_ENDED_BEFORE_READY")
                time.sleep(.1)
            need(ready is not None, "HOST_READY_DEADLINE")
            facet = ready["intake_handoff"]; metadata = facet["metadata"]
            parent_plan = H.read(operations/"serve/plan.json")
            need(facet["status"] == "READY" and facet["recipient_receipt_confirmed"] is False
                 and facet["credential"]["path"] == str(credential_path)
                 and metadata["release_sha256"] == supplied["release_sha256"]
                 and metadata["profile_sha256"] == profile
                 and metadata["operation"] == dict(name="serve", run=str(operations/"serve"),
                     workspace_root=str(operations), plan_sha256=H.sha(parent_plan))
                 and metadata["bindings"] == ready["service"]["bindings"]
                 and metadata["source"] == grant["source"] and metadata["limits"] == QUOTE
                 and metadata["intake_endpoint"] == slots[0]["intake_endpoint"]
                 and metadata["read_endpoint"] == slots[0]["read_endpoint"]
                 and metadata["write_until_ms"] == horizon["write_until_ms"]
                 and metadata["retention_until_ms"] == horizon["retention_until_ms"]
                 and time.monotonic_ns()+35*10**9 < metadata["service_until_ns"], "INDEPENDENT_READY_SELECTION")
            report["ready"] = ready; scan_paths.append(ready_path)
            params = dict(schema="DMKN_MANAGED_CONTRIBUTION_ACTOR_V1", workspace_config=generation["workspace"],
                fixtures=supplied["fixtures"], credential=facet["credential"], expected=metadata,
                egress=egress, source_endpoint=grant["source"], intake_endpoint=slots[0]["intake_endpoint"],
                retention_end_ms=horizon["retention_end_ms"])
            prepared = prepare("contribute", params, "contributor.py", contributor_path.parent, contributor_pin, False)
            report["stage"] = "separate-public-contribution"
            response = A.supervise(prepared[2], PROJECT, commands/"contribute", prepared[3], J.Job)
            actor = complete(prepared, response)["owner"]
            report["contributor"] = actor
            need(actor["status"] == "PASS" and actor["quote"] == QUOTE and actor["cleanup_errors"] == [],
                 "GENUINE_CONTRIBUTOR_COMPLETE")
            pulled = actor["source_provider"]
            need(pulled["requests"] == 3 and pulled["request_bytes"] > 0
                 and OPENING[0]+PACKET[0] <= pulled["reply_bytes"] <= QUOTE["reply_bytes"]
                 and all(pulled[key] == 0 for key in ("active", "failures", "refused", "reserved_reply_bytes")),
                 "GENUINE_SOURCE_PULLS")
        except BaseException as error:
            # Keep the first failed boundary even if host completion also fails.
            # No exception message, traceback or secret-bearing object is saved.
            report["primary_failure"] = {"stage": report["stage"],
                "exception_type": type(error).__name__}
            primary_error = error
            raise
        finally:
            # The separately bounded supervisor owns cleanup. Wait for its same
            # original finite call, never cancel/restart or fabricate closure.
            report["stage"] = "wait-original-host-close"
            try:
                hosting_result = future.result(timeout=max(1, DEADLINE-time.monotonic()))
                host = complete(hosting, hosting_result)["owner"]
                report["host"] = host
            except BaseException as error:
                report["host_completion_failure"] = {"stage": report["stage"],
                    "exception_type": type(error).__name__}
                if primary_error is None:
                    raise
    report["stage"] = "validate-closed-custody"
    need(host["status"] == "COMPLETE" and host["profile_sha256"] == profile, "HOST_COMPLETE")
    H.check_supervision(host["supervision"])
    worker = host["worker"]
    need(worker["intake_handoff"] == facet
         and {key: worker["join"][key] for key in ("number", "nonce", "worker")} == metadata["session"]
         and worker["join"]["mathematical_acceptance"] is False
         and worker["status"] == "COMPLETE" and len(worker["closures"]) == 1, "HANDOFF_SESSION_AND_COMPLETION")
    closed = worker["closures"][0]
    need(closed["status"] == "CLOSED" and closed["cleanup"]["errors"] == []
         and all(closed["cleanup"][key] is True for key in H.CLEANUP), "GENUINE_ORDERLY_CLOSE")
    intake = closed["observed"]["intake"]
    need(intake["used"]["requests"] == intake["used"]["completed_actions"] == 1
         and all(intake["used"][key] == 0 for key in ("refused", "busy", "cancelled", "cleanup_errors", "handler_errors"))
         and intake["active_connections"] == intake["retained_closing_connections"] == 0
         and intake["stopped"] is True and intake["active_intake"] is False, "GENUINE_HOST_INTAKE")
    record = worker["manager"]["slots"][0]
    need(record["run_state"] == "CLOSED" and record["phase"] == "SEALED_SERVING"
         and record["closure_sha256"] == H.sha(H.encode(closed)), "DURABLE_CLOSED_BINDING")
    root = manager_root/"slot-0/g00000000000000000001/workspace"
    need(H.ordinary(root/"operations", directory=True).is_dir()
         and not any((root/"operations").iterdir()), "POPULATED_HOST_OPERATIONS_EMPTY")
    manifest = actor["manifest"]; rid = actor["observed"]["response"]["request_id"]
    rows, ledger_pin = db_read(H, root/"placement.sqlite", [
        ("SELECT config,state,runs,used FROM meta WHERE id=1", ()),
        ("SELECT id,runtime,policy,used FROM grants", ()),
        ("SELECT id,grant_id,manifest,reservation,phase,outcome FROM requests", ())])
    need(all(len(x) == 1 for x in rows), "ONE_DURABLE_GRANT_REQUEST")
    meta, issued, saved = [items[0] for items in rows]
    need(meta[1:3] == ("SEALED_SERVING", 1) and H.strict(meta[3]) == QUOTE
         and issued[0] == metadata["grant_id"] and issued[1] == metadata["issuing_runtime"]
         and H.strict(issued[3]) == QUOTE and saved[:2] == (rid, metadata["grant_id"])
         and H.strict(saved[2]) == manifest and H.strict(saved[3]) == QUOTE
         and saved[4] == "RECEIPT_COMMITTED", "DURABLE_CHARGES_AND_RECEIPT")
    need(H.strict(issued[2]) == {key: grant[key] for key in
         ("source", "write_until_ms", "retention_until_ms", "limits")}, "DURABLE_GRANTED_POLICY")
    outcome = H.strict(saved[5])
    public_receipt = actor["observed"]["response"]["placement"]["outcome"]
    stable = ("status", "request_id", "service_epoch", "generation", "namespace", "wire_profile_id",
              "export_id", "record_id", "snapshot_id", "export_object_sha256", "export_object_bytes",
              "packet_sha256", "packet_bytes", "retention_end_ms", "reservation", "recovery")
    need({key: outcome[key] for key in stable} == {key: public_receipt[key] for key in stable},
         "DURABLE_PUBLIC_RECEIPT_STABLE_FIELDS")
    opening, opening_pin = db_read(H, root/"modules/modules.sqlite", [("SELECT module,idx,opening FROM groups", ())])
    packet, packet_pin = db_read(H, root/"packets/evidence-packets.sqlite", [("SELECT module,size,digest,blob FROM packets", ())])
    need(len(opening[0]) == len(packet[0]) == 1 and opening[0][0][:2] == (MODULE, 10)
         and (len(opening[0][0][2]), H.sha(opening[0][0][2])) == OPENING
         and packet[0][0][:3] == (MODULE, PACKET[0], PACKET[1])
         and (len(packet[0][0][3]), H.sha(packet[0][0][3])) == PACKET, "EXACT_RETAINED_CUSTODY")
    for name in ("serve", "contribute"):
        run = operations/name
        for folder in (commands/name, run/"command", run.parent/(name+"-request")):
            scan_paths.extend(folder/file for file in ("command.json", "stdout.txt", "stderr.txt", "request.json", "launch.json", "preparation.json"))
        scan_paths.append(commands/(name+"-result.json"))
    for folder in (operations/"serve/work/managed-supervisor", worker_root/"command"):
        scan_paths.extend(folder/file for file in ("command.json", "stdout.txt", "stderr.txt"))
    scan_paths.extend(worker_root/file for file in ("plan.json", "BOOT-RESULT.json", "BOOT-FAILED.json"))
    scan_paths.append(worker_root/"work/managed-result.json")
    need(time.monotonic() < DEADLINE, "ORIGINAL_DRIVER_COMPLETION_DEADLINE")
    report.update(database_pins=[ledger_pin, opening_pin, packet_pin], hosting_operations_empty=True,
        token_leak_scan=check_no_leak(H, facet["credential"], scan_paths),
        preserved_generation=str(root.parent), status="PASS", stage="complete")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True); parser.add_argument("--input", required=True)
    parser.add_argument("--input-sha", required=True); args = parser.parse_args()
    output = Path(args.output)
    need(output == PROJECT/"experiments/v5-local-checks"/NAME and Path.cwd() == PROJECT
         and Path(__file__) == output/"sources/software/v5/managed_contribution02/installed_contribution.py"
         and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "EXACT_SELECTED_INVOCATION")
    H = load_support(output)
    report = dict(schema="DMKN_MANAGED_CONTRIBUTION_CHECK_RESULT_V1", status="FAIL", stage="input",
        mathematical_acceptance=False, full_v5_release=False, independent_hosts=False,
        public_deployment_qualified=False, deletion_performed=False)
    try:
        raw = H.read(Path(args.input), 2*MIB)
        need(H.sha(raw) == args.input_sha, "INPUT_PIN")
        execute(H, output, H.strict(raw), report)
    except BaseException:
        report["error_code"] = "MANAGED_CONTRIBUTION_CHECK_FAILED"
        if "primary_failure" in report:
            report["stage"] = report["primary_failure"]["stage"]
    report["elapsed_seconds"] = time.monotonic()-STARTED
    H.save(output/"managed-contribution-result.json", report)
    print(json.dumps({"status": report["status"], "stage": report["stage"]}, separators=(",", ":")))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())

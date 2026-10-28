"""One public incremental host: init, two bounded appends, serve, four typed reads.

Source-only until root selects execution. Reuse retained inert evidence, the
existing public launcher and ordinary acquisition. No owner, native call, new
supervisor, dependency fetch, discovery campaign, retry or automatic renewal.
"""
from __future__ import annotations

import time
START, CPU = time.monotonic(), time.process_time()
import argparse
import asyncio
from contextlib import ExitStack
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
DEADLINE = START+220
PACKAGE = ROOT/"experiments/v5-local-checks/incremental-host-assembly01/distribution/package"
PROFILE = "e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13"
ASSEMBLY = PACKAGE.parent/"ASSEMBLY.json"
ASSEMBLY_SHA = "d9bc9f90b0a77bfee2b4103b6c0dbc7c7d1fbf7a2f579d79699b65665efe1be2"
HELPER = ROOT/"software/v5/ordinary_contact_federation/test_public.py"
HELPER_SHA = "98f3eb0b60e95bcdadca280c636c65ddaa2b6be47793ea43c264ab20abef7879"
FIXTURE_PLAN = ROOT/"software/v5/ordinary_dedicated_host/ACTUAL-PLAN.md"
FIXTURE_PLAN_SHA = "d05b7a6997fc7092e70507543be2be825cdd7e751da22e44e87c4f978636b48e"
BUNDLE = ROOT/"experiments/v5-local-checks/observation-growth-produce01"
MANIFEST_SHA = "d31ee8536962cff8c60c856f107594610d7b82f851c518ec37a838885f3bb4b6"
PRODUCER = ROOT/"experiments/v5-local-checks/observation-growth-produce-launch01/child/stdout.txt"
PRODUCER_SHA = "06e3eba09f5b92b687c0ca57d342793a0451a0a34ca19c8b9f6acd4f70343283"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
HOST_IDENTITY = "STABLE_INCREMENTAL_CONFIGURATION_NOT_CONTENT_IDENTITY"
UNITS = (
    ("fill", "4af85fd28ee3188b147f8d16633e45296165f04326b6943031a9aa344d5d8c71",
     "9c99432c3c567d7ca63d40e9e2a76e11df45d985218361a63a15cc565bd58c9c",
     6384, "8bb24aa780ed89563921671715cc2659c75abe68707be5722294ea418caf527b"),
    ("contextual_iff", "c59ee7bd4eed61193dc06729ca76e28887ad83171f11173353e93bb46305c2c4",
     "b093eb970b89de31662abccdb05552270225e26b93e4f0dc47a6463b1590f8be",
     26650, "bf13287aed53c34ccf58798d3e77ab0df1b60f74ed780641de88a9dc7fd813bd"))


def need(ok, code):
    if not ok:
        raise ValueError("INCREMENTAL_PUBLIC_"+code)


def check():
    need(time.monotonic() < DEADLINE and time.process_time()-CPU < 45, "ORIGINAL_ENVELOPE")


def causes(error):
    rows, seen = [], set()
    while error is not None and len(rows) < 6 and id(error) not in seen:
        seen.add(id(error))
        row = dict(type=type(error).__name__, message=str(error)[:300])
        for name in ("errno", "winerror"):
            value = getattr(error, name, None)
            row[name] = value if type(value) is int or value is None else str(value)[:80]
        rows.append(row)
        error = error.__cause__ if error.__cause__ is not None else error.__context__
    return rows


def pinned(path, digest):
    check()
    need(path.is_file() and 0 < path.stat().st_size <= 2*MIB, "INPUT_BOUND")
    raw = path.read_bytes()
    need(len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == digest, "INPUT_PIN")
    return raw


def helpers():
    raw = pinned(HELPER, HELPER_SHA)
    spec = importlib.util.spec_from_file_location("_incremental_public_helpers", HELPER)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(HELPER), "exec", dont_inherit=True), module.__dict__)
    module.START_WALL, module.START_CPU, module.DEADLINE = START, CPU, DEADLINE
    return module


def command(args, helper, directory, host, operation, config, host_pin=None):
    wall = 60 if operation == "serve" else 45
    check(); need(DEADLINE-time.monotonic() > wall+6, "NO_CHILD_SLICE")
    directory.mkdir()
    path = directory/"config.json"
    helper.save(path, config)
    digest = hashlib.sha256(helper.read(path)).hexdigest()
    argv = [str(Path(args.python_runtime)/"python.exe"), "-I", "-S", "-B",
        str(PACKAGE/"run.py"), "--profile-sha256", PROFILE,
        "--python-runtime", args.python_runtime, "--lean-runtime", args.lean_runtime,
        "--diagnostics", str(directory/"launcher"), "--wall-seconds", str(wall),
        "--cpu-seconds", "25", "--memory-mib", "512", "--active-processes", "3",
        "--stdout-bytes", str(MIB), "--stderr-bytes", str(MIB), "host", "--", operation,
        "--host-root", str(host), "--config", str(path), "--config-sha256", digest,
        "--output", str(directory/"public")]
    if host_pin is not None:
        argv.extend(("--host-sha256", host_pin))
    need(not any(value in argv for value in ("--catalog", "--custody", "--store-id")),
         "UNEXPECTED_OWNER_ARGUMENT")
    helper.save(directory/"COMMAND.json", dict(argv=argv, cwd=str(ROOT), attempts=1))
    return argv, digest, wall


def public_result(helper, directory, operation, digest, host):
    launch = json.loads(helper.read(directory/"launcher/RUN.json"))
    supervision = json.loads(helper.read(directory/"launcher/SUPERVISION.json"))
    public = json.loads(helper.read(directory/"public/RESULT.json"))
    need(launch["ok"] is True and launch["tool"] == "host" and launch["profile_sha256"] == PROFILE and
         supervision["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and
         supervision["direct_child_reaped"] is True and supervision["job_closed"] is True and
         supervision["cleanup_errors"] == [] and supervision["final_job"]["active_processes"] == 0 and
         supervision["final_job"]["terminated_processes"] == 0, "CHILD_NOT_NATURALLY_CLOSED")
    need(public["ok"] is True and public["operation"] == "host-"+operation and
         public["profile_sha256"] == PROFILE and public["config_sha256"] == digest and
         public["semantic_id"] == SEMANTIC and public["host_root"] == str(host) and
         public["mathematical_acceptance"] is False and public["mathematical_owner_opened"] is False and
         public["cost"]["worker_cpu_seconds"] == 0, "PUBLIC_BINDING")
    result = public["result"]
    need(result["host_identity_kind"] == HOST_IDENTITY and result["cleanup_errors"] == [] and
         result["index_closure"] == result["custody_closure"] == result["host_lock_closure"] == "CLOSED" and
         result["mathematical_acceptance"] is False, "HOST_CLOSURE_OR_IDENTITY")
    return dict(result=public, supervision=supervision, launcher=launch)


async def scenario(args, output, loaded, helper, report):
    A, api, B = loaded.A, loaded.peer_api, loaded.baseline_intake.B
    O, H = api.O, api.H
    report["phase"] = "BIND_INPUTS_AND_PROJECT_MANIFESTS"
    pinned(FIXTURE_PLAN, FIXTURE_PLAN_SHA)
    assembly = json.loads(pinned(ASSEMBLY, ASSEMBLY_SHA))
    need(assembly["status"] == "ASSEMBLED_NOT_ADOPTED" and assembly["profile_sha256"] == PROFILE and
         assembly["native_calls"] == 0, "ASSEMBLY_BINDING")
    manifest = B.read_manifest(pinned(BUNDLE/"manifest.json", MANIFEST_SHA), MANIFEST_SHA,
                               check_budget=check)
    producer = json.loads(pinned(PRODUCER, PRODUCER_SHA))
    need(producer["ok"] is True and producer["result"]["semantic_id"] == SEMANTIC and
         manifest.unit_count == 47 and manifest.evidence_bytes == 695269, "FIXTURE_BINDING")
    targets = {row["export_id"]: row for row in producer["result"]["targets"]}
    held_entries = {entry.unit_id: entry for batch in manifest.batches for entry in batch}
    selections = []
    for label, uid, eid, count, digest in UNITS:
        target = targets[eid]
        need(target["unit_id"] == uid and target["name"] ==
             [[0, {"$bytes": list(b"ResetEffects")}], [0, {"$bytes": list(label.encode("ascii"))}]],
             "RETAINED_TARGET")
        raw = pinned(BUNDLE/"units"/(uid+".json"), digest)
        need(len(raw) == count and held_entries[uid].raw_sha256 == digest and
             held_entries[uid].raw_bytes == count, "SELECTED_UNIT_PIN")
        projected = B.make_manifest(((raw,),), check_budget=check)
        need(projected.unit_count == 1 and projected.evidence_bytes == count and
             projected.batches[0][0] == held_entries[uid], "EXACT_MANIFEST_PROJECTION")
        path = output/(label+"-manifest.json")
        with path.open("xb") as stream:
            stream.write(projected.raw)
        selections.append(dict(label=label, target=target, count=count, digest=digest,
            manifest_path=str(path), manifest_sha256=projected.sha256))
    helper.save(output/"SELECTIONS.json", selections)
    report.update(selections=selections, steps=[], reads=[], children_reaped=[], cleanup_errors=[])
    host = output/"host"
    children, budget, client = [], None, None
    host_pin = None
    try:
        with ExitStack() as stack:
            async def launch(label, operation, config):
                report["phase"] = label
                directory = output/label
                argv, digest, wall = command(args, helper, directory, host, operation, config, host_pin)
                row = dict(label=label, operation=operation, config_sha256=digest, status="STARTED")
                report["steps"].append(row)
                out = stack.enter_context((directory/"stdout.txt").open("xb"))
                err = stack.enter_context((directory/"stderr.txt").open("xb"))
                started = time.monotonic()
                child = await asyncio.create_subprocess_exec(*argv, cwd=ROOT, stdin=subprocess.DEVNULL,
                    stdout=out, stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
                children.append(child)
                return child, directory, digest, wall, started, row

            async def finish(item):
                child, directory, digest, wall, started, row = item
                async with asyncio.timeout_at(min(DEADLINE-8, started+wall+4)):
                    need(await child.wait() == 0, "CHILD_EXIT")
                result = public_result(helper, directory, row["operation"], digest, host)
                row.update(status="CLOSED", public=result, elapsed_seconds=time.monotonic()-started)
                return result["result"]["result"]

            init = dict(schema="DMKN_INCREMENTAL_HOST_INIT_V1", partial_publication=True,
                custody_limits=dict(objects=16, exports=128, logical_bytes=2*MIB, db_pages=1024),
                index_limits=dict(max_objects=8, max_postings=4096, max_features=1024,
                    max_snapshots=9, max_logical_bytes=4*MIB, max_db_pages=2048))
            initial = await finish(await launch("init", "init", init))
            need(initial["status"] == "INITIALIZED_INCREMENTAL_INERT_HOST" and initial["initialized"] and
                 initial["current_content"]["index_objects"] == 0 and
                 initial["current_content"]["custody_counts"] == dict(objects=0, exports=0, logical_bytes=0),
                 "EMPTY_INITIALIZATION")
            host_raw = helper.read(host/"HOST.json")
            host_pin = hashlib.sha256(host_raw).hexdigest()
            need(host_pin == initial["host_sha256"], "INITIAL_DESCRIPTOR_PIN")
            current = initial["current_content"]
            snapshots = [current["index_snapshot_id"]]
            for number, selected in enumerate(selections, 1):
                config = dict(schema="DMKN_INCREMENTAL_HOST_APPEND_V1", bundle_directory=str(BUNDLE),
                    manifest=dict(path=selected["manifest_path"], sha256=selected["manifest_sha256"]),
                    targets=[selected["target"]], share_all_bundle=True, allow_partial_publication=True,
                    bundle_limits=dict(max_units=1, max_bytes=65536, max_batch_units=1, max_batch_bytes=65536))
                result = await finish(await launch("append-"+str(number), "append", config))
                need(result["status"] == "APPENDED_INERT_HOST" and result["batch_complete"] is True and
                     result["before_content"] == current and result["census"]["units"] == 1 and
                     result["census"]["bytes"] == selected["count"] and
                     len(result["publications"]) == 1 and result["publications"][0]["new"] is True and
                     result["publications"][0]["export_id"] == selected["target"]["export_id"], "APPEND_RESULT")
                current = result["current_content"]
                need(current["index_objects"] == number and current["custody_counts"]["objects"] == 2*number and
                     current["index_snapshot_id"] == result["publications"][0]["snapshot_id"] and
                     current["index_snapshot_id"] not in snapshots and
                     helper.read(host/"HOST.json") == host_raw, "GROWING_CONTENT_STABLE_DESCRIPTOR")
                snapshots.append(current["index_snapshot_id"])
            service = dict(schema="DMKN_DEDICATED_HOST_SERVE_V1", host="127.0.0.1", port=0, tls=None,
                lease_seconds=20, cleanup_seconds=10, share_all_custody=True, exclusive=True,
                limits=dict(max_connections=2, max_requests=4, max_reply_bytes=262144, operation_ms=3000))
            item = await launch("serve", "serve", service)
            ready = await helper.ready_report(item[0], item[1]/"public/READY.json", report)
            need(ready["status"] == "READY" and ready["host"] == "127.0.0.1" and ready["tls"] is False and
                 ready["host_sha256"] == host_pin and ready["host_identity_kind"] == HOST_IDENTITY and
                 ready["current_content"] == current and ready["prior_append_completion"] == "NOT_ASSERTED_BY_SERVICE",
                 "CURRENT_CONTENT_READY")
            report["ready"] = ready
            budget = O.OrdinaryBudget(deadline=min(DEADLINE-8, time.monotonic()+16),
                                      requests=4, reply_bytes=2*(32768+65536))
            client = O.OrdinaryAcquisition(api.OrdinaryExportAdapter(SEMANTIC),
                {"host": H.Endpoint(ready["host"], ready["port"])}, budget, local_custody=None)
            for selected in selections:
                target = selected["target"]
                for kind in ("locator", "evidence"):
                    report["phase"] = "READ_"+kind.upper()
                    started = time.monotonic()
                    row = dict(label=selected["label"], kind=kind, status="STARTED",
                               phase="awaiting_typed_acquisition")
                    report["reads"].append(row)
                    try:
                        if kind == "locator":
                            value = await client.locator("host", SEMANTIC, target["export_id"], 32768,
                                expected_name=target["name"], attempt_timeout_ms=3000)
                            need(value["locator"]["unit_id"] == target["unit_id"], "LOCATOR_TARGET")
                        else:
                            value = await client.evidence("host", SEMANTIC, target["unit_id"], 65536,
                                expected_export_id=target["export_id"], expected_export_name=target["name"],
                                attempt_timeout_ms=3000)
                            need(value["raw_bytes"] == selected["count"] and value["raw_sha256"] == selected["digest"],
                                 "EXACT_OLD_AND_NEW_EVIDENCE")
                        row["phase"] = "validating_and_saving_reply"
                        need(value["mathematical_acceptance"] is False, "INERT_READ_ONLY")
                        path = output/(selected["label"]+"-"+kind+"-response.json")
                        with path.open("xb") as stream:
                            stream.write(value["raw"])
                        row.update(status="COMPLETE", phase="complete",
                            response={key: item for key, item in value.items() if key != "raw"},
                            raw_sha256=hashlib.sha256(value["raw"]).hexdigest(), raw_bytes=len(value["raw"]))
                    except BaseException as error:
                        row.update(status="EXCEPTION", error_chain=causes(error))
                        raise
                    finally:
                        row["elapsed_seconds"] = time.monotonic()-started
            budget.close()
            report["acquisition"] = client.report()
            need(report["acquisition"]["budget"]["requests"] == 4 and
                 report["acquisition"]["budget"]["pending_requests"] == 0 and
                 report["acquisition"]["http"]["completed_responses"] == 4 and
                 report["acquisition"]["http"]["failed_attempts"] == 0, "EXACT_FOUR_READS")
            report["phase"] = "WAIT_NATURAL_SERVICE_END"
            served = await finish(item)
            need(served["status"] == "LEASE_FINISHED" and served["current_content"] == current and
                 served["prior_append_completion"] == "NOT_ASSERTED_BY_SERVICE" and
                 served["service"]["quiescent"] is True and served["service"]["cleanup_errors"] == [],
                 "NATURAL_SERVICE_END")
            provider = served["service"]["provider"]
            need(provider["requests"] == 4 and provider["active"] == provider["reserved_reply_bytes"] == 0 and
                 provider["failures"] == 0 and helper.read(host/"HOST.json") == host_raw, "CLOSED_STABLE_HOST")
            report.update(host_sha256=host_pin, current_content=current, snapshots=snapshots,
                          assertions_passed=True)
    finally:
        if budget is not None:
            try:
                if not budget.closed:
                    budget.close()
            except BaseException as error:
                report["cleanup_errors"].append("budget:"+type(error).__name__)
            if client is not None:
                report["acquisition"] = client.report()
        for child in children:
            if child.returncode is None:
                try:
                    child.kill()
                    async with asyncio.timeout(3):
                        await child.wait()
                except BaseException as error:
                    report["cleanup_errors"].append("child:"+type(error).__name__)
        report["children_reaped"] = [child.returncode is not None for child in children]
    need(not report["cleanup_errors"] and len(children) == 4 and all(report["children_reaped"]), "CLEANUP")
    for path, digest in ((HELPER, HELPER_SHA), (FIXTURE_PLAN, FIXTURE_PLAN_SHA),
                         (ASSEMBLY, ASSEMBLY_SHA), (PRODUCER, PRODUCER_SHA), (BUNDLE/"manifest.json", MANIFEST_SHA)):
        pinned(path, digest)
    for _, uid, _, _, digest in UNITS:
        pinned(BUNDLE/"units"/(uid+".json"), digest)
    check()
    report["phase"] = "CLOSED"


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "INVOCATION")
    need(Path(args.package) == PACKAGE and args.profile_sha256 == PROFILE, "SELECTED_PACKAGE")
    need(output.is_absolute() and output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         not output.exists() and output.parent.is_dir() and output.parent.resolve(strict=True) == output.parent,
         "FRESH_OUTPUT")
    need(all(not output.is_relative_to(Path(path)) and not Path(path).is_relative_to(output)
             for path in (args.package, args.python_runtime, args.lean_runtime, str(BUNDLE))), "OUTPUT_OVERLAP")
    output.mkdir()
    helper = helpers()
    report = dict(passed=False, assertions_passed=False, profile_sha256=PROFILE,
        scope="PUBLIC_INCREMENTAL_INERT_HOST_NOT_MATHEMATICAL_ACCEPTANCE_OR_DEPENDENCY_COMPLETENESS")
    try:
        loaded = helper.load_package(args)
        need(loaded.installation.semantic_id == SEMANTIC, "SELECTED_SEMANTICS")
        asyncio.run(scenario(args, output, loaded, helper, report))
        report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:1000], error_chain=causes(error))
    report.update(wall_seconds=time.monotonic()-START, harness_cpu_seconds=time.process_time()-CPU)
    helper.save(output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

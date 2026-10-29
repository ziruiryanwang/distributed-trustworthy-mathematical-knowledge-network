"""Four actual Python-only host calls over two retained publication bundles.

Source only until root selects execution under an outer Job. No Lean argument,
owner, product database access, fixture regeneration, retry or renewed allowance.
One exact-type query and four typed reads exercise the existing public routes.
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
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
HOST_IDENTITY = "STABLE_INCREMENTAL_CONFIGURATION_NOT_CONTENT_IDENTITY"
FIXTURE_ROOT = ROOT/"experiments/v5-local-checks/contribution-bundle-controls01/checks"
FIXTURES = (
    ("bundle-contribution", "db5b14d4759d849983b75169cf02c10fd6c63406070140e5c3e27b4e080c1ee1",
     "78c2f5088d5140d9333d71b701ddd6c9c95bc257fa4d53c8bfdaf9e385c9ceb0", 21, 379701, 11, 10),
    ("bundle-completion", "09dafc9677fde2266536714481140d81feb9df0e818a9757298c07e0f206a4ad",
     "0bd22da5351f0f46ee9ac51ed6b856e8f909a2ed9a00a2c80b50a987b60907c9", 3, 10700, 1, 2))
FORBIDDEN_MODULES = ("ordinary_admission", "portable_admission", "baseline_intake",
                     "portable_catalog", "local_catalog", "profile")


def need(ok, code):
    if not ok:
        raise ValueError("INERT_PUBLIC_"+code)


def check():
    need(time.monotonic() < DEADLINE and time.process_time()-CPU < 45, "ORIGINAL_ENVELOPE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, maximum=16*MIB):
    check()
    need(path.is_file() and path.stat().st_size <= maximum, "INPUT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) <= maximum, "INPUT_GREW")
    return raw


def pinned(path, expected, maximum=2*MIB):
    raw = read(path, maximum)
    need(0 < len(raw) <= maximum and sha(raw) == expected, "INPUT_PIN:"+path.name)
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":")).encode("ascii")
    need(0 < len(raw) <= 16*MIB, "REPORT_BOUND")
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "REPORT_SHORT_WRITE")
        stream.flush(); os.fsync(stream.fileno())
    return sha(raw)


def causes(error):
    result, seen = [], set()
    while error is not None and len(result) < 6 and id(error) not in seen:
        seen.add(id(error))
        result.append({"type": type(error).__name__, "message": str(error)[:500]})
        error = error.__cause__ if error.__cause__ is not None else error.__context__
    return result


def client_support(args):
    """Execute only externally selected extracted support, never the old kit."""
    package = Path(args.package)
    manifest_raw = pinned(package/"SOURCES.json", args.profile_sha256)
    manifest = json.loads(manifest_raw)
    pin = manifest["files"]["_entry"]
    need(pin["path"] == "run.py", "ENTRY_PATH")
    raw = pinned(package/"run.py", pin["sha256"])
    need(len(raw) == pin["bytes"], "ENTRY_BYTES")
    spec = importlib.util.spec_from_file_location("_inert_public_selected_entry", package/"run.py")
    entry = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = entry
    exec(compile(raw, str(package/"run.py"), "exec"), entry.__dict__)
    R, selected_raw, selected = entry.bootstrap(package, args.profile_sha256, check)
    bound = R.bind(package, args.profile_sha256, args.python_runtime, check)
    need(bound.manifest_raw == selected_raw == manifest_raw and
         selected["_entry"] == raw, "CAPTURED_SOURCE_BINDING")
    support = R.load_support(bound, check)
    need(support.semantic_id == SEMANTIC and
         not any(name in sys.modules for name in FORBIDDEN_MODULES), "PURE_CLIENT_CLOSURE")
    return R, support


def fixtures(support):
    """Read exact previously prepared bundles; create no new mathematical data."""
    result = []
    for label, config_pin, manifest_pin, count, size, target_count, support_count in FIXTURES:
        root = FIXTURE_ROOT/label
        config_path = root/"append.json"
        config_raw = pinned(config_path, config_pin)
        config = support.F.strict(config_raw, 2*MIB)
        need(config["bundle_directory"] == str(root) and config["manifest"] == {
            "path": str(root/"manifest.json"), "sha256": manifest_pin} and
            config["share_all_bundle"] is True and config["allow_partial_publication"] is True,
            "RETAINED_APPEND_BINDING")
        manifest_raw = pinned(root/"manifest.json", manifest_pin)
        limits = support.B.Limits(**config.get("bundle_limits", {}))
        manifest = support.B.read_manifest(manifest_raw, manifest_pin,
                                            limits=limits, check_budget=check)
        need(manifest.unit_count == count and manifest.evidence_bytes == size and
             manifest.semantic_id == SEMANTIC and len(config["targets"]) == target_count,
             "RETAINED_CENSUS")
        units, entries = {}, []
        for batch in manifest.batches:
            raws = []
            for item in batch:
                raw = pinned(root/item.relative_path, item.raw_sha256, item.raw_bytes)
                need(len(raw) == item.raw_bytes, "RETAINED_UNIT_SIZE")
                units[item.unit_id] = raw; entries.append(item); raws.append(raw)
            support.B.validate_batch(batch, tuple(raws), limits=limits, check_budget=check)
        targets = config["targets"]
        need(len(set(units)-{row["unit_id"] for row in targets}) == support_count,
             "REAL_SUPPORT_ONLY_UNITS")
        records, previews = {}, {}
        adapter = support.OA.OrdinaryExportAdapter(SEMANTIC)
        for target in targets:
            raw = units[target["unit_id"]]
            preview = support.PP.preview_from_evidence(raw, target["name"])
            support.PP.resolve(preview, raw)
            records[target["export_id"]] = adapter.describe(preview, target["export_id"])["record"]
            previews[target["export_id"]] = preview
        result.append(dict(label=label, root=root, config_path=config_path, config_pin=config_pin,
            manifest_pin=manifest_pin, manifest=manifest, entries=entries, units=units,
            targets=targets, records=records, previews=previews))
    need(len({key for f in result for key in f["units"]}) == 24 and
         len({t["export_id"] for f in result for t in f["targets"]}) == 12, "DISJOINT_RETAINED_OUTPUTS")
    return result


def query_selection(support, selected):
    target = selected[1]["targets"][0]
    preview = selected[1]["previews"][target["export_id"]]
    key = support.modules["formal_query"].preview_key(preview)["key"]
    specs = [{"tag": "declaration-kind", "value": "theorem"},
             {"tag": "declared-type-key", "value": key}]
    features = support.OA.compile_query(support.namespace, specs)
    expected = [record for f in selected for record in f["records"].values()
                if set(features) <= set(record["features"])]
    need(len(expected) == 1 and expected[0]["object_id"] == target["export_id"],
         "ONE_RETAINED_EXACT_TYPE_MATCH")
    return {"specs": specs, "features": features, "expected_record": expected[0],
        "scope": "ONE_KNOWN_FIXTURE_TYPE_QUERY_NOT_INDEPENDENT_USEFULNESS_OR_GLOBAL_COVERAGE"}


def command(args, directory, host, operation, config_path, config_pin, host_pin):
    wall = 50 if operation == "serve" else 40
    check(); need(DEADLINE-time.monotonic() > wall+6, "NO_CHILD_SLICE")
    argv = [str(Path(args.python_runtime)/"python.exe"), "-I", "-S", "-B",
        str(Path(args.package)/"run.py"), operation, "--profile-sha256", args.profile_sha256,
        "--python-runtime", args.python_runtime, "--host-root", str(host),
        "--config", str(config_path), "--config-sha256", config_pin,
        "--output", str(directory/"public"), "--diagnostics", str(directory/"launcher"),
        "--wall-seconds", str(wall), "--cpu-seconds", "20", "--memory-mib", "512",
        "--active-processes", "1", "--stdout-bytes", str(MIB), "--stderr-bytes", str(MIB)]
    if host_pin is not None:
        argv.extend(("--host-sha256", host_pin))
    need(not any(value in argv for value in
        ("--lean-runtime", "--catalog", "--custody", "--store-id", "--worker")), "PURE_PUBLIC_ARGUMENTS")
    save(directory/"COMMAND.json", {"argv": argv, "cwd": str(ROOT), "attempts": 1})
    return argv, wall


def public_result(args, R, directory, operation, config_pin, host, namespace):
    launch = R.strict(read(directory/"launcher/RUN.json"), reports=True)
    supervision = R.strict(read(directory/"launcher/SUPERVISION.json"), reports=True)
    worker_raw = read(directory/"public/RESULT.json")
    worker = R.strict(worker_raw, reports=True)
    need(launch["ok"] is True and launch["status"] == "INERT_HOST_OPERATION_COMPLETE" and
         launch["profile_sha256"] == args.profile_sha256 and launch["config_sha256"] == config_pin and
         launch["worker_report_sha256"] == sha(worker_raw) and
         R.operational_result(supervision) and supervision["termination_requested"] is False,
         "NATURAL_PUBLIC_JOB_CLOSURE")
    need(worker["ok"] is True and worker["operation"] == operation and
         worker["profile_sha256"] == args.profile_sha256 and worker["config_sha256"] == config_pin and
         worker["semantic_id"] == SEMANTIC and worker["namespace"] == namespace and
         worker["host_root"] == str(host) and worker["mathematical_acceptance"] is False and
         worker["mathematical_owner_opened"] is False and worker["supervised_completion"] is False,
         "WORKER_REPORT_BINDING")
    result = worker["result"]
    need(result == launch["result"] and result["host_identity_kind"] == HOST_IDENTITY and
         result["cleanup_errors"] == [] and result["mathematical_acceptance"] is False and
         result["host_lock_closure"] == result["index_closure"] == result["custody_closure"] == "CLOSED",
         "HOST_CLOSURE_BINDING")
    need(R.strict(read(directory/"stdout.txt"), reports=True) == launch and
         read(directory/"stderr.txt") == read(directory/"launcher/child/stderr.txt") == b"",
         "EXACT_PUBLIC_OUTPUT")
    return {"launcher": launch, "supervision": supervision, "worker": worker}


async def ready_report(child, path):
    until = min(DEADLINE-15, time.monotonic()+20)
    while child.returncode is None:
        check(); need(time.monotonic() < until, "READY_DEADLINE")
        if path.exists():
            try:
                return json.loads(read(path))
            except json.JSONDecodeError:
                pass  # Same deadline while the fresh report write finishes.
        await asyncio.sleep(0.025)
    raise ValueError("INERT_PUBLIC_SERVICE_EXITED_BEFORE_READY")


async def network(support, ready, selected, query, output, report):
    endpoint = support.H.Endpoint(ready["host"], ready["port"], ready["tls"])
    need(endpoint.host == "127.0.0.1" and endpoint.tls is False, "LOOPBACK_ONLY")
    until = min(DEADLINE-8, time.monotonic()+17)
    budget = client = None
    try:
        async with asyncio.timeout_at(until):
            request = {"namespace": support.namespace, "features": query["features"],
                       "max_bytes": MIB, "max_expanded_bytes": MIB}
            response = await support.H.exchange(endpoint, support.H.OFFER_ROUTE, request, MIB, 3000)
            need(response["status"] == 200, "OFFER_HTTP")
            offer = support.F.strict(response["raw"], MIB)
            need(offer["status"] == "OFFERED" and offer["mathematical_acceptance"] is False, "INERT_OFFER")
            sid = offer["summary"]["snapshot_id"]
            need(sid == ready["current_content"]["index_snapshot_id"], "HELD_SNAPSHOT")
            summary = support.W.decode_summary(support.F.compact(offer["summary"]), sid,
                support.namespace, query["features"], check_budget=check)
            verified = support.Q.verify_summary(sid, support.namespace, query["features"], summary)
            plans = [p for p in support.Q.plan_partitions(verified) if not p["committed_empty"]]
            need(len(plans) == 1 and plans[0]["anchor_count"] == 1, "ONE_QUERY_PARTITION")
            plan = plans[0]
            request = {"schema": "DMKN_FORMAL_CANDIDATE_REQUEST_V1", "namespace": support.namespace,
                "snapshot_id": sid, "features": query["features"], "partition": plan["partition"],
                "anchor": plan["anchor"], "start": 0,
                "limits": {key: high for key, (_, high) in support.C.LIMITS.items()}}
            page = await support.H.exchange(endpoint, support.H.CANDIDATE_ROUTE, request, MIB, 3000)
            need(page["status"] == 200, "CANDIDATE_HTTP")
            result = support.C.verify_page(verified, request, support.F.strict(page["raw"], MIB),
                                           check_budget=check)
            need(result["matches"] == [query["expected_record"]] and
                 result["mathematical_acceptance"] is False, "VERIFIED_EXACT_TYPE_MATCH")
            save(output/"QUERY-RESULT.json", {"offer": offer, "request": request, "verified": result})
            report["discovery"] = {"requests": 2, "snapshot_id": sid,
                "request_bytes": response["request_bytes"]+page["request_bytes"],
                "reply_bytes": response["reply_bytes"]+page["reply_bytes"],
                "matched_export_id": result["matches"][0]["object_id"], "mathematical_acceptance": False}
            budget = support.O.OrdinaryBudget(deadline=until, requests=4, reply_bytes=4*MIB)
            client = support.O.OrdinaryAcquisition(support.OA.OrdinaryExportAdapter(SEMANTIC),
                                                  {"host": endpoint}, budget, local_custody=None)
            record = result["matches"][0]
            preview = await client.preview("host", record, attempt_timeout_ms=3000)
            need(preview["raw"] == selected[1]["previews"][record["object_id"]] and
                 preview["mathematical_acceptance"] is False, "EXACT_NEW_PREVIEW")
            report["reads"].append({"kind": "new-target-preview", "bytes": len(preview["raw"]),
                                    "sha256": sha(preview["raw"]), "mathematical_acceptance": False})
            target = selected[1]["targets"][0]
            supporting = next(entry for entry in selected[1]["entries"] if
                              entry.unit_id not in {t["unit_id"] for t in selected[1]["targets"]})
            old = selected[0]["targets"][0]
            reads = (("new-target", target["unit_id"], selected[1], target),
                     ("support-only", supporting.unit_id, selected[1], None),
                     ("old-target", old["unit_id"], selected[0], old))
            for label, uid, fixture, expected in reads:
                raw = fixture["units"][uid]
                kwargs = {} if expected is None else {"expected_export_id": expected["export_id"],
                                                       "expected_export_name": expected["name"]}
                value = await client.evidence("host", SEMANTIC, uid, len(raw),
                                              attempt_timeout_ms=3000, **kwargs)
                need(value["raw"] == raw and value["mathematical_acceptance"] is False,
                     "EXACT_TYPED_EVIDENCE:"+label)
                report["reads"].append({"kind": label, "unit_id": uid, "bytes": len(raw),
                                        "sha256": sha(raw), "mathematical_acceptance": False})
            budget.close()
            report["acquisition"] = client.report()
            need(report["acquisition"]["budget"]["requests"] == 4 and
                 report["acquisition"]["budget"]["pending_requests"] == 0 and
                 report["acquisition"]["http"]["completed_responses"] == 4 and
                 report["acquisition"]["http"]["failed_attempts"] == 0, "FOUR_SETTLED_TYPED_READS")
    finally:
        if budget is not None and not budget.closed:
            budget.close()
        if client is not None:
            report["acquisition"] = client.report()


async def scenario(args, R, support, selected, query, output, report):
    host, host_pin = output/"host", None
    children = []
    report.update(steps=[], reads=[], cleanup_errors=[], forced_termination=False)
    try:
        with ExitStack() as stack:
            async def launch(label, operation, *, config=None, retained=None):
                report["phase"] = label
                directory = output/label; directory.mkdir()
                if retained is None:
                    config_path = directory/"config.json"
                    config_pin = save(config_path, config)
                else:
                    config_path, config_pin = retained["config_path"], retained["config_pin"]
                    pinned(config_path, config_pin)
                argv, wall = command(args, directory, host, operation, config_path, config_pin, host_pin)
                out = stack.enter_context((directory/"stdout.txt").open("xb"))
                err = stack.enter_context((directory/"stderr.txt").open("xb"))
                environment = dict(os.environ)
                environment["PATH"] = os.pathsep.join((args.python_runtime, str(Path(args.python_runtime)/"DLLs")))
                started = time.monotonic()
                process = await asyncio.create_subprocess_exec(*argv, cwd=ROOT, env=environment,
                    stdin=subprocess.DEVNULL, stdout=out, stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
                row = {"label": label, "operation": operation, "config_sha256": config_pin, "status": "STARTED"}
                item = (process, directory, config_pin, wall, started, row)
                children.append(item); report["steps"].append(row)
                return item

            async def finish(item):
                process, directory, config_pin, wall, started, row = item
                async with asyncio.timeout_at(min(DEADLINE-8, started+wall+4)):
                    need(await process.wait() == 0, "PUBLIC_CHILD_EXIT")
                result = public_result(args, R, directory, row["operation"], config_pin, host, support.namespace)
                row.update(status="CLOSED", public=result, elapsed_seconds=time.monotonic()-started)
                return result["worker"]["result"]

            init = {"schema": "DMKN_INCREMENTAL_HOST_INIT_V1", "partial_publication": True,
                "custody_limits": {"objects": 64, "exports": 1024, "logical_bytes": 8*MIB, "db_pages": 4096},
                "index_limits": {"max_objects": 32, "max_postings": 32768, "max_features": 4096,
                    "max_snapshots": 64, "max_logical_bytes": 16*MIB, "max_db_pages": 8192}}
            initial = await finish(await launch("init", "init", config=init))
            need(initial["status"] == "INITIALIZED_INCREMENTAL_INERT_HOST" and initial["initialized"] is True and
                 initial["current_content"]["index_objects"] == 0 and
                 initial["current_content"]["custody_counts"] == {"objects": 0, "exports": 0, "logical_bytes": 0},
                 "EMPTY_INITIALIZATION")
            host_raw = read(host/"HOST.json"); host_pin = sha(host_raw)
            need(host_pin == initial["host_sha256"], "HOST_PIN")
            lock_id = ((host/"host.lock").stat().st_dev, (host/"host.lock").stat().st_ino)
            current, snapshots = initial["current_content"], [initial["current_content"]["index_snapshot_id"]]
            objects, targets = 0, 0
            for fixture in selected:
                result = await finish(await launch("append-"+fixture["label"], "append", retained=fixture))
                objects += len(fixture["units"])+len(fixture["targets"])
                targets += len(fixture["targets"])
                need(result["status"] == "APPENDED_INERT_HOST" and result["batch_complete"] is True and
                     result["before_content"] == current and result["census"]["units"] == len(fixture["units"]) and
                     result["census"]["bytes"] == fixture["manifest"].evidence_bytes and
                     [row["identity"] for row in result["evidence"]] == [e.unit_id for e in fixture["entries"]] and
                     {row["export_id"] for row in result["publications"]} == set(fixture["records"]) and
                     all(row["new"] is True for row in result["publications"]), "EXACT_APPEND_RESULT")
                current = result["current_content"]
                need(current["index_objects"] == targets and current["custody_counts"]["objects"] == objects and
                     current["index_snapshot_id"] not in snapshots and read(host/"HOST.json") == host_raw and
                     ((host/"host.lock").stat().st_dev, (host/"host.lock").stat().st_ino) == lock_id,
                     "GROWING_CONTENT_STABLE_DESCRIPTOR_AND_LOCK")
                snapshots.append(current["index_snapshot_id"])
            service = {"schema": "DMKN_DEDICATED_HOST_SERVE_V1", "host": "127.0.0.1", "port": 0,
                "tls": None, "lease_seconds": 20, "cleanup_seconds": 10,
                "share_all_custody": True, "exclusive": True,
                "limits": {"max_connections": 2, "max_requests": 8, "max_reply_bytes": 8*MIB, "operation_ms": 3000}}
            item = await launch("serve", "serve", config=service)
            ready = await ready_report(item[0], item[1]/"public/READY.json")
            need(ready["status"] == "READY" and ready["host_sha256"] == host_pin and
                 ready["host_identity_kind"] == HOST_IDENTITY and ready["current_content"] == current and
                 ready["prior_append_completion"] == "NOT_ASSERTED_BY_SERVICE" and
                 ready["mathematical_acceptance"] is False, "CURRENT_CONTENT_READY")
            report["ready"] = ready
            await network(support, ready, selected, query, output, report)
            report["phase"] = "WAIT_NATURAL_SERVICE_END"
            served = await finish(item)
            provider = served["service"]["provider"]
            need(served["status"] == "LEASE_FINISHED" and served["current_content"] == current and
                 served["service"]["quiescent"] is True and served["service"]["cleanup_errors"] == [] and
                 provider["requests"] == 6 and provider["active"] == provider["reserved_reply_bytes"] == 0 and
                 provider["cleanup_pending"] == provider["cleanup_failures"] == provider["failures"] == 0 and
                 read(host/"HOST.json") == host_raw and read(host/"host.lock") == b"\0" and
                 ((host/"host.lock").stat().st_dev, (host/"host.lock").stat().st_ino) == lock_id,
                 "NATURALLY_CLOSED_STABLE_HOST")
            report.update(host_sha256=host_pin, current_content=current, snapshots=snapshots,
                          assertions_passed=True)
    finally:
        # Failure never retries an operation. Wait only within its original slice;
        # if a wrapper is stuck, the outer selected Job settles the complete tree.
        for process, _, _, wall, started, row in children:
            if process.returncode is None:
                try:
                    async with asyncio.timeout_at(min(DEADLINE-5, started+wall+4)):
                        await process.wait()
                except BaseException as error:
                    report["forced_termination"] = True
                    report["cleanup_errors"].append("wrapper-wait:"+type(error).__name__)
                    process.kill()
                    try:
                        async with asyncio.timeout(3): await process.wait()
                    except BaseException as caught:
                        report["cleanup_errors"].append("wrapper-reap:"+type(caught).__name__)
            row["wrapper_reaped"] = process.returncode is not None
        report["children_reaped"] = [p.returncode is not None for p, *_ in children]
    need(len(children) == 4 and all(report["children_reaped"]) and not report["cleanup_errors"] and
         not report["forced_termination"], "PUBLIC_CLOSURE")
    for fixture in selected:
        pinned(fixture["config_path"], fixture["config_pin"])
        pinned(fixture["root"]/"manifest.json", fixture["manifest_pin"])
        for entry in fixture["entries"]:
            pinned(fixture["root"]/entry.relative_path, entry.raw_sha256, entry.raw_bytes)
    support.verify()
    need(not any(name in sys.modules for name in FORBIDDEN_MODULES), "NO_NATIVE_OWNER_IMPORT")
    report["phase"] = "CLOSED"


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("package", "profile-sha256", "python-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    package, output = Path(args.package), Path(args.output)
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "INVOCATION")
    need(package.is_absolute() and package.is_dir() and output.is_absolute() and
         output.is_relative_to(ROOT/"experiments/v5-local-checks") and not os.path.lexists(output) and
         output.parent.resolve(strict=True) == output.parent, "FRESH_OUTPUT")
    need(all(not output.is_relative_to(path) and not path.is_relative_to(output)
             for path in (package, Path(args.python_runtime), FIXTURE_ROOT)), "OUTPUT_OVERLAP")
    output.mkdir()
    report = {"passed": False, "assertions_passed": False, "profile_sha256": args.profile_sha256,
        "package": str(package), "mathematical_acceptance": False, "native_calls": 0,
        "scope": "PURE_PUBLIC_INCREMENTAL_HOST_AND_TYPED_ROUTES_NOT_MATHEMATICAL_OR_GROWTH_EVIDENCE"}
    try:
        R, support = client_support(args)
        selected = fixtures(support)
        query = query_selection(support, selected)
        save(output/"QUERY.json", query)
        save(output/"INPUTS.json", [{"bundle": str(f["root"]), "config_sha256": f["config_pin"],
            "manifest_sha256": f["manifest_pin"], "units": len(f["units"]),
            "evidence_bytes": f["manifest"].evidence_bytes, "targets": len(f["targets"])} for f in selected])
        asyncio.run(scenario(args, R, support, selected, query, output, report))
        report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:1000], error_chain=causes(error))
    report.update(wall_seconds=time.monotonic()-START, harness_cpu_seconds=time.process_time()-CPU)
    save(output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

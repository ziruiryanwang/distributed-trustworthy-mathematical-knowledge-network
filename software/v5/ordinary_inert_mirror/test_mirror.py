"""Changed-boundary controls, inert synthetic data, no mathematical acceptance.

Source only until a reviewed root selection runs this under Run-V5-Check.py.
The existing selected-export fixture constructors are reused, not their campaign.
"""
from __future__ import annotations

import argparse
import asyncio
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import time
from types import SimpleNamespace
from unittest.mock import patch

START, CPU = time.monotonic(), time.process_time()
MIB = 1024**2


def need(ok, message):
    if not ok:
        raise AssertionError(message)


def check():
    need(time.monotonic()-START < 150 and time.process_time()-CPU < 60,
         "TEST_ORIGINAL_ALLOWANCE")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("ascii")


def save(path, value):
    data = value if type(value) is bytes else encode(value)
    with path.open("xb") as stream:
        stream.write(data)
    return sha(data)


def load(name, path):
    need(name not in sys.modules, "TEST_PRELOAD:"+name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def refuses(action, expected):
    try:
        action()
    except (ValueError, RuntimeError, sqlite3.Error) as error:
        need(any(fragment in str(error) for fragment in expected),
             "TEST_UNEXPECTED_REFUSAL:"+str(error))
        return str(error)
    raise AssertionError("TEST_MISSING_REFUSAL:"+str(expected))


def forbidden(*args, **kwargs):
    raise AssertionError("TEST_NATIVE_OR_NETWORK_FORBIDDEN_IN_PREPARATION")


def make_bundle(api, directory, raws):
    directory.mkdir()
    (directory/"units").mkdir()
    batches = api.B.split_units(raws, check_budget=check)
    manifest = api.B.make_manifest(batches, check_budget=check)
    for entries, batch in zip(manifest.batches, batches):
        for entry, data in zip(entries, batch):
            save(directory/entry.relative_path, data)
    save(directory/"manifest.json", manifest.raw)
    return manifest


async def discover_and_acquire(s, ready, expected_raw):
    """No target or snapshot ID is used in the search request."""
    endpoint = s.H.Endpoint(ready["host"], ready["port"], ready["tls"])
    need(endpoint.host == "127.0.0.1" and endpoint.tls is False, "TEST_LOOPBACK_ONLY")
    adapter = s.OA.OrdinaryExportAdapter(s.S.semantic_id())
    features = s.OA.compile_query(adapter.namespace,
        [{"tag": "declaration-kind", "value": "theorem"}])
    request = dict(namespace=adapter.namespace, features=features,
                   max_bytes=MIB, max_expanded_bytes=MIB)
    response = await s.H.exchange(endpoint, s.H.OFFER_ROUTE, request, MIB, 3000)
    need(response["status"] == 200, "TEST_OFFER_HTTP")
    offer = s.F.strict(response["raw"], MIB)
    need(offer["status"] == "OFFERED" and offer["mathematical_acceptance"] is False,
         "TEST_OFFER_INERT")
    sid = offer["summary"]["snapshot_id"]
    summary = s.W.decode_summary(s.F.compact(offer["summary"]), sid,
        adapter.namespace, features, check_budget=check)
    verified = s.Q.verify_summary(sid, adapter.namespace, features, summary)
    plans = [p for p in s.Q.plan_partitions(verified) if not p["committed_empty"]]
    need(len(plans) == 1 and plans[0]["anchor_count"] == 1, "TEST_SELECTED_TARGET_SCOPE")
    p = plans[0]
    candidate_request = dict(schema="DMKN_FORMAL_CANDIDATE_REQUEST_V1",
        namespace=adapter.namespace, snapshot_id=sid, features=features,
        partition=p["partition"], anchor=p["anchor"], start=0,
        limits={key: high for key, (_, high) in s.C.LIMITS.items()})
    page = await s.H.exchange(endpoint, s.H.CANDIDATE_ROUTE, candidate_request, MIB, 3000)
    need(page["status"] == 200, "TEST_CANDIDATE_HTTP")
    result = s.C.verify_page(verified, candidate_request, s.F.strict(page["raw"], MIB),
                             check_budget=check)
    need(len(result["matches"]) == 1 and result["mathematical_acceptance"] is False,
         "TEST_VERIFIED_METADATA_ONLY")
    record = result["matches"][0]
    budget = s.O.OrdinaryBudget(requests=4, reply_bytes=16*MIB,
                               deadline=time.monotonic()+5)
    acquire = s.O.OrdinaryAcquisition(adapter, {"mirror": endpoint}, budget)
    preview = await acquire.preview("mirror", record)
    locator = record["locator"]
    evidence = await acquire.evidence("mirror", s.S.semantic_id(), locator["unit_id"],
        8*MIB, expected_export_id=record["object_id"], expected_export_name=locator["export_name"])
    need(evidence["raw"] == expected_raw and evidence["mathematical_acceptance"] is False
         and preview["mathematical_acceptance"] is False, "TEST_EXACT_INERT_RETRIEVAL")
    budget.close()
    return {"snapshot_id": sid, "export_id": record["object_id"],
        "acquisition": acquire.report(),
        "discovery_requests": 2,
        "discovery_request_bytes": response["request_bytes"]+page["request_bytes"],
        "discovery_reply_bytes": response["reply_bytes"]+page["reply_bytes"],
        "mathematical_acceptance": False}


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--python-runtime", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "TEST_PYTHON_PROFILE")
    output = Path(args.output)
    need(output.is_absolute() and not output.exists() and output.parent.is_dir(), "TEST_FRESH_OUTPUT")
    output.mkdir()
    here = Path(__file__).absolute().parent
    run = load("_mirror_test_entry", here/"run.py")
    helper = load("_mirror_test_core", here/"mirror.py")
    fixture = load("_mirror_existing_fixture", here.parent/"ordinary_selected_export/test_export.py")
    with ExitStack() as guards:
        for name in ("subprocess.Popen", "os.system", "socket.socket", "socket.create_connection"):
            guards.enter_context(patch(name, forbidden))
        s = run.load_support(Path(args.source_root), check)
    need(not any(name in sys.modules for name in
        ("ordinary_admission", "portable_admission", "baseline_intake", "profile")),
        "TEST_NO_NATIVE_OWNER_IMPORT")
    api = SimpleNamespace(E=s.E, S=s.S, PE=s.PE, B=s.B, PP=s.PP)
    first, a = fixture.make_unit(api, "MirrorFixture.First")
    second, b = fixture.make_unit(api, "MirrorFixture.Second", a)
    false_claim, target = fixture.make_unit(api, "MirrorFixture.UnprovedFalse", b, theorem=True)
    group, group_targets = fixture.make_group(api)
    units = [first, second, false_claim, group]
    bundle = output/"bundle"
    manifest = make_bundle(api, bundle, units)
    targets = [target, group_targets[0]]
    results = []

    def prepare(leaf, *, selected_bundle=bundle, selected_manifest=manifest,
                selected_targets=targets, limits=None, share=True):
        return helper.prepare(api=s.api, manifest_raw=selected_manifest.raw,
            manifest_sha256=selected_manifest.sha256, bundle_directory=selected_bundle,
            targets=selected_targets, inventory_raw=s.inventory_raw,
            output_directory=output/leaf, limits=dict(helper.CEILINGS) if limits is None else limits,
            check_budget=check, protected_paths=(Path(args.source_root), here), share_all_bundle=share)

    with ExitStack() as guards:
        for name in ("subprocess.Popen", "os.system", "socket.socket", "socket.create_connection"):
            guards.enter_context(patch(name, forbidden))
        prepared = prepare("direct-prepared")
        need(prepared["status"] == "PREPARED_DATA_NOT_SUPERVISED_READY"
             and prepared["mathematical_acceptance"] is False and prepared["stores_closed"] is True
             and prepared["cleanup_errors"] == [], "TEST_PREPARATION_DISPOSITION")
        need(not (output/"direct-prepared/READY.json").exists(), "TEST_WORKER_NOT_READY")
        save(output/"direct-report.json", prepared)
        descriptor = json.loads((output/"direct-prepared/DESCRIPTOR.json").read_bytes())
        custody = s.O.OrdinaryStore(output/"direct-prepared/custody", s.S.semantic_id(),
                                    descriptor["custody_limits"])
        try:
            for data in units:
                unit_id = s.PE.read_evidence(data).unit_id
                need(custody.get_evidence(s.S.semantic_id(), unit_id, 8*MIB,
                     check_budget=check) == data, "TEST_ALL_EXACT_UNITS_PRESERVED")
            sibling = group_targets[1]
            locator_raw = custody.get_locator(s.S.semantic_id(), sibling["export_id"], MIB,
                                               check_budget=check)
            locator = s.PP.read_locator(s.E.strict_json(locator_raw))
            need(locator["export_name"] == sibling["name"] and locator["unit_id"] == sibling["unit_id"],
                 "TEST_UNINDEXED_SUPPLIED_GROUP_SIBLING_PRESERVED")
        finally:
            custody.close()
        need(descriptor["index_status"]["objects"] == len(targets), "TEST_ONLY_SELECTED_PREVIEWS_INDEXED")
        results.append("fixed_pure_source_closure_and_false_inert_preparation")
        missing_bundle = output/"missing-bundle"
        missing = make_bundle(api, missing_bundle, [second])
        refuses(lambda: prepare("missing", selected_bundle=missing_bundle,
            selected_manifest=missing, selected_targets=[b]), ("IMPORT", "CLOSURE"))
        changed = deepcopy(s.PE.read_evidence(second).document)
        for row in changed["imports"]:
            if row[0] == a["name"]:
                row[1] = "0"*64
        wrong_raw = s.E.canonical_json(changed)
        wrong_bundle = output/"wrong-import-bundle"
        wrong = make_bundle(api, wrong_bundle, [first, wrong_raw])
        refuses(lambda: prepare("wrong-import", selected_bundle=wrong_bundle,
            selected_manifest=wrong, selected_targets=[a]), ("IMPORT", "BINDING", "IDENTITY"))
        collision, unused = fixture.make_unit(api, "MirrorFixture.First", value=1)
        collision_bundle = output/"collision-bundle"
        collision_manifest = make_bundle(api, collision_bundle, [first, collision])
        refuses(lambda: prepare("collision", selected_bundle=collision_bundle,
            selected_manifest=collision_manifest, selected_targets=[a]), ("NAME", "OUTPUT", "CONFLICT"))
        shadow, shadow_target = fixture.make_unit(api, "Nat", theorem=True)
        shadow_bundle = output/"shadow-bundle"
        shadow_manifest = make_bundle(api, shadow_bundle, [shadow])
        refuses(lambda: prepare("shadow", selected_bundle=shadow_bundle,
            selected_manifest=shadow_manifest, selected_targets=[shadow_target]), ("BASIS",))
        wrong_target = deepcopy(target); wrong_target["export_id"] = "0"*64
        refuses(lambda: prepare("wrong-target", selected_targets=[wrong_target]), ("TARGET",))
        refuses(lambda: prepare("no-disclosure", share=False), ("DISCLOS", "SHARE"))
        refuses(lambda: prepare("too-many", limits={**helper.CEILINGS, "units":1}), ("BOUND", "LIMIT"))
        refuses(lambda: prepare("too-small", limits={**helper.CEILINGS, "bytes":1}), ("BOUND", "LIMIT"))
        refuses(lambda: prepare("index-reservation", limits={**helper.CEILINGS, "index_hash_steps":1}),
                ("INDEX_AGGREGATE_RESERVATION",))
        refuses(lambda: prepare("direct-prepared"), ("FRESH", "EXIST"))
        with patch.object(s.DS.Store, "admit", side_effect=ValueError("TEST_LATE_INDEX_REFUSAL")):
            refuses(lambda: prepare("late-failure"), ("TEST_LATE_INDEX_REFUSAL",))
        need((output/"late-failure").is_dir()
             and not (output/"late-failure/READY.json").exists(), "TEST_PARTIAL_FAILURE_NOT_READY")
        results.append("exact_import_target_disclosure_capacity_and_partial_output_refusals")

    def argv(action, request_path, diagnostics, *, helper_sha=None):
        return [str(Path(args.python_runtime)/"python.exe"), "-I", "-S", "-B", str(here/"run.py"), action,
            "--source-root", args.source_root, "--source-manifest-sha256", sha((here/"SOURCES.json").read_bytes()),
            "--python-runtime", args.python_runtime, "--entry-sha256", sha((here/"run.py").read_bytes()),
            "--helper-sha256", helper_sha or sha((here/"mirror.py").read_bytes()),
            "--request", str(request_path), "--request-sha256", sha(request_path.read_bytes()),
            "--diagnostics", str(diagnostics), "--wall-seconds", "60", "--cpu-seconds", "30",
            "--memory-mib", "512", "--active-processes", "1", "--stdout-bytes", str(MIB),
            "--stderr-bytes", str(MIB)]

    request = dict(schema="DMKN_INERT_MIRROR_PREPARE_REQUEST_V1", bundle_directory=str(bundle),
        manifest_sha256=manifest.sha256, targets=targets, output_directory=str(output/"public-prepared"),
        share_all_bundle=True, limits=dict(helper.CEILINGS))
    request_path = output/"prepare-request.json"
    save(request_path, request)
    # The fixed source selection is not a caller-extensible executable manifest.
    wrong_source_command = argv("prepare", request_path, output/"bad-source-diagnostics")
    wrong_source_command[wrong_source_command.index("--source-manifest-sha256")+1] = "0"*64
    with (output/"bad-source-stdout.json").open("xb") as stdout, (output/"bad-source-stderr.txt").open("xb") as stderr:
        refused = subprocess.run(wrong_source_command, stdout=stdout, stderr=stderr,
                                 timeout=10, check=False)
    need(refused.returncode != 0 and not (output/"public-prepared").exists(),
         "TEST_UNAPPROVED_SOURCE_STARTED")
    source_refusal = json.loads((output/"bad-source-stdout.json").read_bytes())
    need("SOURCE_MANIFEST_SELECTION" in source_refusal.get("error", ""), "TEST_SOURCE_SELECTION_REFUSAL")
    # Only the prefix needed to reach the changed first-codec pin is copied.
    # No native artifact, runtime or full package is copied/built.
    source_map = json.loads((here/"SOURCES.json").read_bytes())
    changed_source = output/"changed-source-prefix"
    changed_source.mkdir()
    selected_root = Path(args.source_root)
    for role in ("_launcher", "ordinary_evidence"):
        relative = source_map["files"][role]["source"]
        destination = changed_source/relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = (selected_root/relative).read_bytes()
        save(destination, data if role == "_launcher" else data+b"\n")
    save(changed_source/"INVESTIGATOR-SOURCE-MANIFEST.json",
         (selected_root/"INVESTIGATOR-SOURCE-MANIFEST.json").read_bytes())
    changed_command = argv("prepare", request_path, output/"changed-source-diagnostics")
    changed_command[changed_command.index("--source-root")+1] = str(changed_source)
    with (output/"changed-source-stdout.json").open("xb") as stdout, (output/"changed-source-stderr.txt").open("xb") as stderr:
        changed_result = subprocess.run(changed_command, stdout=stdout, stderr=stderr,
                                        timeout=10, check=False)
    need(changed_result.returncode != 0 and not (output/"public-prepared").exists(),
         "TEST_CHANGED_CODEC_STARTED")
    changed_refusal = json.loads((output/"changed-source-stdout.json").read_bytes())
    need("RUN_PIN_SIZE" in changed_refusal.get("error", ""), "TEST_CHANGED_CODEC_PIN_REFUSAL")
    with (output/"prepare-stdout.json").open("xb") as stdout, (output/"prepare-stderr.txt").open("xb") as stderr:
        completed = subprocess.run(argv("prepare", request_path, output/"prepare-diagnostics"),
            stdout=stdout, stderr=stderr, timeout=65, check=False)
    need(completed.returncode == 0, "TEST_PUBLIC_PREPARE_FAILED")
    state = output/"public-prepared"
    ready_raw, descriptor_raw = (state/"READY.json").read_bytes(), (state/"DESCRIPTOR.json").read_bytes()
    results.append("public_parent_clean_completion_promotes_readiness_without_native_install")
    config = dict(host="127.0.0.1", port=0, tls=None, lease_seconds=5, cleanup_seconds=10,
        limits=dict(max_connections=2, max_requests=16, max_reply_bytes=32*MIB, operation_ms=3000),
        share_all_custody=True, exclusive=True)
    service_request = dict(schema="DMKN_INERT_MIRROR_SERVE_REQUEST_V1", prepared_directory=str(state),
        descriptor_sha256=sha(descriptor_raw), ready_sha256=sha(ready_raw), config=config)
    service_request_path = output/"serve-request.json"
    save(service_request_path, service_request)
    # Refused public startups must not open a listener or mutate the prepared stores.
    for label, changes in (("bad-ready", {"ready_sha256": "0"*64}),
                           ("bad-descriptor", {"descriptor_sha256": "0"*64}),
                           ("unsealed", {"prepared_directory": str(output/"direct-prepared"),
                            "descriptor_sha256": prepared["descriptor_sha256"]})):
        negative_request = output/(label+"-request.json")
        save(negative_request, {**service_request, **changes})
        negative_diagnostics = output/(label+"-diagnostics")
        with (output/(label+"-stdout.json")).open("xb") as stdout, (output/(label+"-stderr.txt")).open("xb") as stderr:
            negative = subprocess.run(argv("serve", negative_request, negative_diagnostics),
                stdout=stdout, stderr=stderr, timeout=10, check=False)
        need(negative.returncode != 0 and not (negative_diagnostics/"SERVICE-READY.json").exists(),
             "TEST_UNSEALED_OR_TAMPERED_SERVICE_STARTED:"+label)
        refusal = json.loads((output/(label+"-stdout.json")).read_bytes())
        need(refusal["status"] == "NO_WORKER_LAUNCHED" and refusal["ok"] is False,
             "TEST_SELECTION_REFUSAL_NOT_PRELAUNCH:"+label)
        if label != "unsealed":
            need("PREPARED_SELECTION" in refusal.get("error", ""), "TEST_WRONG_TAMPER_REFUSAL:"+label)
        else:
            need(refusal.get("error_type") in ("FileNotFoundError", "ValueError"),
                 "TEST_MISSING_SEAL_REFUSAL")
    results.append("fixed_source_selection_unsealed_and_tampered_startup_refusals")
    service_diagnostics = output/"serve-diagnostics"
    process = None
    with (output/"serve-stdout.json").open("xb") as stdout, (output/"serve-stderr.txt").open("xb") as stderr:
        try:
            process = subprocess.Popen(argv("serve", service_request_path, service_diagnostics),
                                       stdout=stdout, stderr=stderr)
            until = time.monotonic()+20
            listening = service_diagnostics/"SERVICE-READY.json"
            peer_ready = None
            while process.poll() is None:
                check(); need(time.monotonic() < until, "TEST_LISTENER_DEADLINE")
                if listening.exists():
                    try:
                        peer_ready = json.loads(listening.read_bytes())
                        break
                    except json.JSONDecodeError:
                        pass  # Publication may be in progress; original deadline is unchanged.
                time.sleep(0.025)
            need(peer_ready is not None, "TEST_PUBLIC_LISTENER_FAILED")
            refuses(lambda: asyncio.run(helper.serve(prepared_directory=state,
                descriptor_raw=descriptor_raw, descriptor_sha256=sha(descriptor_raw),
                ready_raw=ready_raw, ready_sha256=sha(ready_raw), config=config, api=s.api,
                check_budget=check, deadline=time.monotonic()+30)), ("FRESH_PATH",))
            network_result = asyncio.run(discover_and_acquire(s, peer_ready, false_claim))
            save(output/"network.json", network_result)
            need(process.wait(timeout=25) == 0, "TEST_PUBLIC_SERVICE_CLOSURE_FAILED")
        finally:
            if process is not None and process.poll() is None:
                process.terminate(); process.wait(timeout=5)
    need((state/"READY.json").read_bytes() == ready_raw and
         (state/"DESCRIPTOR.json").read_bytes() == descriptor_raw, "TEST_SERVICE_PRESERVED_SELECTION")
    results.append("public_unknown_id_discovery_exact_inert_acquisition_and_finite_service")
    # Deliberate post-service corruption of this test-owned synthetic fixture.
    # The completed positive reports are retained; this is not a repair or live-DB copy.
    descriptor = json.loads(descriptor_raw)
    index = s.DS.Store(state/"index", s.OA.OrdinaryExportAdapter(s.S.semantic_id()),
                       descriptor["index_limits"])
    before = index.status()
    try:
        index.admit(s.PP.preview_from_evidence(first, a["name"]), expected_id=a["export_id"])
        after = index.status()
        need(before["latest"] != after["latest"], "TEST_NONVACUOUS_SNAPSHOT_CHANGE")
    finally:
        index.close()
    save(output/"deliberate-post-service-state-change.json", dict(before=before, after=after,
         purpose="TEST_OWNED_SYNTHETIC_SNAPSHOT_BINDING_REFUSAL;POSITIVE_SERVICE_ALREADY_CLOSED"))
    with patch.object(s.H.Provider, "start", forbidden):
        refuses(lambda: asyncio.run(helper.serve(prepared_directory=state,
            descriptor_raw=descriptor_raw, descriptor_sha256=sha(descriptor_raw),
            ready_raw=ready_raw, ready_sha256=sha(ready_raw), config=config, api=s.api,
            check_budget=check, deadline=time.monotonic()+30)), ("PREPARED_STATE_BINDING",))
    need(not (state/"ACTIVE.lock").exists(), "TEST_REFUSAL_CLEANLY_RELEASED")
    results.append("nonvacuous_snapshot_change_refuses_before_network_and_releases_lock")
    save(output/"TEST-RESULT.json", dict(status="PASS", groups=results, group_count=len(results),
        mathematical_acceptance=False, native_calls=0,
        wall_seconds=time.monotonic()-START, test_process_cpu_seconds=time.process_time()-CPU))
    print(json.dumps({"status": "PASS", "groups": results}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

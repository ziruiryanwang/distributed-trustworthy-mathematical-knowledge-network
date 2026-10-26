"""Remaining mirror02 service boundary; reuse controls01 data, not its campaign.

Source only until reviewed/root-selected. No fixture construction, native Lean,
owner state, external endpoint or modification of the retained controls01 run.
"""
from __future__ import annotations

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
import time
from unittest.mock import patch

START, CPU = time.monotonic(), time.process_time()
MIB = 1024**2
PRIOR_TEST_SHA = "60600a26f4a49a080dedcbc8a8befbf8c48bbbeddba9d8165a320deae1c670d3"
FIXTURE_REQUEST_SHA = "6f2f5aa5849fabbd88c141a05735ae44ac1b6b49dcee790cad9d11b86d494801"
FIXTURE_MANIFEST_SHA = "799bb3c86af8b0af8aa11c1f38cac4d1c6ec8d642858122ab3c92683864f6416"


def need(ok, code):
    if not ok:
        raise AssertionError("MIRROR02_TEST_" + code)


def check():
    need(time.monotonic() - START < 100 and time.process_time() - CPU < 40,
         "ORIGINAL_ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pinned(path, expected, maximum):
    check()
    need(path.is_file() and 0 < path.stat().st_size <= maximum, "INPUT_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    need(len(raw) <= maximum and sha(raw) == expected, "INPUT_PIN")
    return raw


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("source-root", "python-runtime", "fixture-root", "output"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON_PROFILE")
    here = Path(__file__).absolute().parent
    output, fixture_root = Path(args.output), Path(args.fixture_root)
    need(output.is_absolute() and not output.exists() and output.parent.is_dir(), "FRESH_OUTPUT")
    need(fixture_root.is_absolute() and fixture_root.is_dir() and
         not output.is_relative_to(fixture_root) and not fixture_root.is_relative_to(output),
         "RETAINED_INPUT_OUTPUT_SEPARATION")
    prior_path = here.parent / "ordinary_inert_mirror" / "test_mirror.py"
    prior_raw = pinned(prior_path, PRIOR_TEST_SHA, MIB)
    spec = importlib.util.spec_from_file_location("_mirror02_prior_test_helpers", prior_path)
    prior = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = prior
    exec(compile(prior_raw, str(prior_path), "exec"), prior.__dict__)
    # Reuse helper code, not main(), old controls, fixture constructors or budget.
    prior.check = check
    run = prior.load("_mirror02_test_entry", here / "run.py")
    helper = prior.load("_mirror02_test_core", here / "mirror.py")
    with ExitStack() as guards:
        for name in ("subprocess.Popen", "os.system", "socket.socket", "socket.create_connection"):
            guards.enter_context(patch(name, prior.forbidden))
        s = run.load_support(Path(args.source_root), check)
    need(not any(name in sys.modules for name in
        ("ordinary_admission", "portable_admission", "baseline_intake", "profile")), "NO_NATIVE_OWNER_IMPORT")
    old_request_raw = pinned(fixture_root / "prepare-request.json", FIXTURE_REQUEST_SHA, MIB)
    old_request = json.loads(old_request_raw)
    bundle = fixture_root / "bundle"
    manifest_raw = pinned(bundle / "manifest.json", FIXTURE_MANIFEST_SHA, 2*MIB)
    manifest = s.B.read_manifest(manifest_raw, FIXTURE_MANIFEST_SHA, check_budget=check)
    need(manifest.unit_count == 4 and manifest.evidence_bytes == 5149, "EXACT_FOUR_UNIT_FIXTURE")
    units = {}
    for batch in manifest.batches:
        for entry in batch:
            raw = pinned(bundle / entry.relative_path, entry.raw_sha256, entry.raw_bytes)
            need(len(raw) == entry.raw_bytes, "EXACT_UNIT_LENGTH")
            units[entry.unit_id] = raw
    targets = old_request["targets"]
    need(len(targets) == 2 and old_request["manifest_sha256"] == FIXTURE_MANIFEST_SHA and
         old_request["bundle_directory"] == str(bundle), "RETAINED_REQUEST_BINDING")
    expected_raw = units[targets[0]["unit_id"]]
    indexed_ids = {target["export_id"] for target in targets}
    change_raw = change_target = None
    for unit_id, raw in units.items():
        parsed = s.PE.read_evidence(raw)
        need(parsed.unit_id == unit_id, "RETAINED_UNIT_IDENTITY")
        for row in parsed.document["unit"][2]:
            eid = s.S.export_id(s.S.semantic_id(), unit_id, row[0])
            if eid not in indexed_ids and change_target is None:
                change_raw = raw
                change_target = {"name": row[0], "unit_id": unit_id, "export_id": eid}
    need(change_target is not None, "NONINDEXED_SNAPSHOT_CONTROL_TARGET")
    output.mkdir()
    groups = []
    prior.save(output / "INPUTS.json", {"prior_test_sha256": PRIOR_TEST_SHA,
        "request_sha256": FIXTURE_REQUEST_SHA, "manifest_sha256": FIXTURE_MANIFEST_SHA,
        "unit_count": len(units), "evidence_bytes": sum(map(len, units.values())),
        "targets": targets, "fixture_root": str(fixture_root), "new_fixture_construction": False})

    def argv(action, request_path, diagnostics):
        return [str(Path(args.python_runtime) / "python.exe"), "-I", "-S", "-B", str(here / "run.py"), action,
            "--source-root", args.source_root, "--source-manifest-sha256", sha((here / "SOURCES.json").read_bytes()),
            "--python-runtime", args.python_runtime, "--entry-sha256", sha((here / "run.py").read_bytes()),
            "--helper-sha256", sha((here / "mirror.py").read_bytes()), "--request", str(request_path),
            "--request-sha256", sha(request_path.read_bytes()), "--diagnostics", str(diagnostics),
            "--wall-seconds", "40", "--cpu-seconds", "20", "--memory-mib", "512",
            "--active-processes", "1", "--stdout-bytes", str(MIB), "--stderr-bytes", str(MIB)]

    state = output / "public-prepared"
    request = {**old_request, "bundle_directory": str(bundle), "output_directory": str(state)}
    request_path = output / "prepare-request.json"
    prior.save(request_path, request)
    with (output / "prepare-stdout.json").open("xb") as stdout, (output / "prepare-stderr.txt").open("xb") as stderr:
        completed = subprocess.run(argv("prepare", request_path, output / "prepare-diagnostics"),
            stdout=stdout, stderr=stderr, timeout=45, check=False)
    need(completed.returncode == 0, "FRESH_PUBLIC_PREPARATION_FAILED")
    prepare_report = json.loads((output / "prepare-stdout.json").read_bytes())
    need(prepare_report["ok"] is True and prepare_report["status"] == "INERT_MIRROR_PREPARE_COMPLETE",
         "PUBLIC_PREPARE_STATUS")
    ready_raw, descriptor_raw = (state / "READY.json").read_bytes(), (state / "DESCRIPTOR.json").read_bytes()
    ready, descriptor = s.F.strict(ready_raw, MIB), s.F.strict(descriptor_raw, MIB)
    need(ready["helper_sha256"] == sha((here / "mirror.py").read_bytes()) and
         ready["descriptor_sha256"] == sha(descriptor_raw) and
         ready["request_sha256"] == sha(request_path.read_bytes()) and
         ready["mathematical_acceptance"] is False and descriptor["mathematical_acceptance"] is False,
         "FRESH_HELPER_SEAL_AND_METADATA_BINDING")
    # The repair changes only metadata parsing; ordinary evidence still rejects
    # boolean/null syntax. Test exact actual metadata, not a fake acceptance flag.
    prior.refuses(lambda: s.E.strict_json(descriptor_raw), ("JSON_LEXICAL_TOKEN",))
    prior.refuses(lambda: s.E.strict_json(ready_raw), ("JSON_LEXICAL_TOKEN",))
    need(helper._ready(s.E, s.F, state, sha(descriptor_raw), ready_raw, sha(ready_raw), check) == ready,
         "REPAIRED_SEAL_PARSER")
    probe = s.F.compact({"mathematical_acceptance": False, "previous_snapshot": None})
    need(s.F.strict(probe, MIB)["previous_snapshot"] is None, "METADATA_NULL_PROFILE")
    prior.refuses(lambda: s.F.strict(b'{"x":1,"x":2}', MIB), ("JSON_DUPLICATE_KEY",))
    prior.refuses(lambda: s.F.strict(b'{"x":1.0}', MIB), ("JSON_NONINTEGER",))
    prior.save(output / "METADATA-PARSER.json", {"status": "PASS", "descriptor_sha256": sha(descriptor_raw),
        "ready_sha256": sha(ready_raw), "evidence_grammar_unchanged": True,
        "actual_metadata_accepted": True, "duplicate_and_noninteger_refused": True})
    groups.append("fresh_public_prepare_and_metadata_parser_discrimination")

    config = dict(host="127.0.0.1", port=0, tls=None, lease_seconds=5, cleanup_seconds=10,
        limits=dict(max_connections=2, max_requests=16, max_reply_bytes=32*MIB, operation_ms=3000),
        share_all_custody=True, exclusive=True)
    service_request = dict(schema="DMKN_INERT_MIRROR_SERVE_REQUEST_V1", prepared_directory=str(state),
        descriptor_sha256=sha(descriptor_raw), ready_sha256=sha(ready_raw), config=config)
    service_request_path = output / "serve-request.json"
    prior.save(service_request_path, service_request)
    service_diagnostics = output / "serve-diagnostics"
    process = None
    with (output / "serve-stdout.json").open("xb") as stdout, (output / "serve-stderr.txt").open("xb") as stderr:
        try:
            process = subprocess.Popen(argv("serve", service_request_path, service_diagnostics),
                                       stdout=stdout, stderr=stderr)
            until = min(START + 100, time.monotonic() + 20)
            listening = service_diagnostics / "SERVICE-READY.json"
            peer_ready = None
            while process.poll() is None:
                check(); need(time.monotonic() < until, "LISTENER_DEADLINE")
                if listening.exists():
                    try:
                        peer_ready = json.loads(listening.read_bytes())
                        break
                    except json.JSONDecodeError:
                        pass  # Same fixed deadline while report publication completes.
                time.sleep(0.025)
            need(peer_ready is not None, "PUBLIC_LISTENER_FAILED")
            lock_raw = (state / "ACTIVE.lock").read_bytes()
            with patch.object(s.H.Provider, "start", prior.forbidden):
                refusal = prior.refuses(lambda: asyncio.run(helper.serve(prepared_directory=state,
                    descriptor_raw=descriptor_raw, descriptor_sha256=sha(descriptor_raw),
                    ready_raw=ready_raw, ready_sha256=sha(ready_raw), config=config, api=s.api,
                    check_budget=check, deadline=time.monotonic()+20)), ("FRESH_PATH",))
            need((state / "ACTIVE.lock").read_bytes() == lock_raw and process.poll() is None,
                 "LIVE_OWNER_EXCLUSION_PRESERVED")
            prior.save(output / "LIVE-EXCLUSION.json", {"status": "REFUSED_AS_EXPECTED", "reason": refusal,
                "original_lock_unchanged": True, "second_listener_started": False})
            network = asyncio.run(prior.discover_and_acquire(s, peer_ready, expected_raw))
            need(network["export_id"] == targets[0]["export_id"], "EXACT_DISCOVERED_TARGET")
            prior.save(output / "network.json", network)
            need(process.wait(timeout=25) == 0, "PUBLIC_SERVICE_CLOSURE_FAILED")
        finally:
            if process is not None and process.poll() is None:
                process.terminate(); process.wait(timeout=5)
    served = json.loads((output / "serve-stdout.json").read_bytes())
    need(served["ok"] is True and served["status"] == "INERT_MIRROR_SERVE_COMPLETE" and
         served["result"]["status"] == "LEASE_FINISHED" and served["result"]["quiescent"] is True and
         served["result"]["stores_closed"] is True and served["result"]["cleanup_errors"] == [],
         "SERVICE_EXACT_CLEAN_REPORT")
    for action in ("prepare", "serve"):
        supervision = json.loads((output / (action + "-diagnostics") / "SUPERVISION.json").read_bytes())
        need(s.R.operational_result(supervision)["ok"] and
             supervision["termination_requested"] is False, "PUBLIC_JOB_CLEAN_CLOSURE")
    need(not (state / "ACTIVE.lock").exists() and (state / "READY.json").read_bytes() == ready_raw and
         (state / "DESCRIPTOR.json").read_bytes() == descriptor_raw, "SERVICE_PRESERVED_PREPARED_SELECTION")
    groups.append("public_unknown_id_discovery_exact_inert_acquisition_live_exclusion_and_clean_lease")

    # Mutate only THIS fresh test-owned synthetic index, after positive closure.
    # The original controls01 bundle/state and all positive reports stay unchanged.
    index = s.DS.Store(state / "index", s.OA.OrdinaryExportAdapter(s.S.semantic_id()),
                       descriptor["index_limits"])
    before = index.status()
    try:
        index.admit(s.PP.preview_from_evidence(change_raw, change_target["name"]),
                    expected_id=change_target["export_id"])
        after = index.status()
        need(before["latest"] != after["latest"] and after["objects"] == before["objects"] + 1,
             "NONVACUOUS_INDEX_SNAPSHOT_CHANGE")
    finally:
        index.close()
    prior.save(output / "deliberate-post-service-state-change.json", {"before": before, "after": after,
        "purpose": "FRESH_TEST_OWNED_SYNTHETIC_STATE_ONLY_AFTER_CLEAN_POSITIVE_SERVICE"})
    with patch.object(s.H.Provider, "start", prior.forbidden):
        refusal = prior.refuses(lambda: asyncio.run(helper.serve(prepared_directory=state,
            descriptor_raw=descriptor_raw, descriptor_sha256=sha(descriptor_raw), ready_raw=ready_raw,
            ready_sha256=sha(ready_raw), config=config, api=s.api, check_budget=check,
            deadline=time.monotonic()+20)), ("PREPARED_STATE_BINDING",))
    need(not (state / "ACTIVE.lock").exists(), "POST_SNAPSHOT_REFUSAL_RELEASED_LOCK")
    prior.save(output / "SNAPSHOT-REFUSAL.json", {"status": "REFUSED_AS_EXPECTED", "reason": refusal,
        "provider_start_forbidden": True, "lock_released": True})
    groups.append("changed_snapshot_refuses_before_network_with_clean_lock_release")
    # Read-only rebind the small immutable retained inputs after all new work.
    pinned(fixture_root / "prepare-request.json", FIXTURE_REQUEST_SHA, MIB)
    pinned(bundle / "manifest.json", FIXTURE_MANIFEST_SHA, 2*MIB)
    for batch in manifest.batches:
        for entry in batch:
            pinned(bundle / entry.relative_path, entry.raw_sha256, entry.raw_bytes)
    check()
    result = dict(status="PASS", groups=groups, group_count=len(groups), native_calls=0,
        mathematical_acceptance=False, prior_failed_run_preserved=True,
        retained_manifest_sha256=FIXTURE_MANIFEST_SHA, wall_seconds=time.monotonic()-START,
        test_process_cpu_seconds=time.process_time()-CPU)
    prior.save(output / "TEST-RESULT.json", result)
    print(json.dumps(result), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

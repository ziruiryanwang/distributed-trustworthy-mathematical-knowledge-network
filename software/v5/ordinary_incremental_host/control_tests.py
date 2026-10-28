"""Prospective incremental-host controls; root separately selects execution.

Real profile-pinned codecs, SQLite stores and host helper; no mathematical owner,
native process or application network. Exceptions injected AFTER actual commits
exercise legal persistent prefixes with orderly unwinding, not process crashes.
All database writes and deliberate corruption are confined to fresh scratch roots.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack, contextmanager
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import sys
import time
from types import SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PACKAGE = ROOT/"experiments/v5-local-checks/incremental-host-assembly01/distribution/package"
PROFILE_SHA = "e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13"
FIXTURE = ROOT/"experiments/v5-local-checks/observation-growth-produce01"
MANIFEST_SHA = "d31ee8536962cff8c60c856f107594610d7b82f851c518ec37a838885f3bb4b6"
START, CPU = time.monotonic(), time.process_time()
WALL_SECONDS, CPU_SECONDS = 150, 90
MIB = 1024**2
CASES, CONNECTIONS = [], []
CUSTODY_LIMITS = dict(objects=256, exports=2048, logical_bytes=16*MIB, db_pages=4096)
INDEX_LIMITS = dict(max_objects=128, max_postings=32768, max_features=8192,
                    max_snapshots=129, max_logical_bytes=64*MIB, max_db_pages=16384)
BUNDLE_LIMITS = dict(max_units=128, max_bytes=MIB, max_batch_units=128, max_batch_bytes=MIB)


def need(value, code):
    if not value:
        raise AssertionError("INCREMENTAL_CONTROL_"+code)


def check():
    need(time.monotonic()-START < WALL_SECONDS and time.process_time()-CPU < CPU_SECONDS,
         "ORIGINAL_ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                      separators=(",", ":")).encode("ascii")


def read(path, maximum=2*MIB, expected=None):
    check()
    need(path.is_absolute() and path.resolve(strict=True) == path and path.is_file(), "INPUT_PATH")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(0 < len(raw) <= maximum and (expected is None or sha(raw) == expected), "INPUT_PIN")
    return raw


def write(path, raw):
    need(type(raw) is bytes and 0 < len(raw) <= 2*MIB, "OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def save(path, value):
    write(path, canonical(value))


def forbidden(*args, **kwargs):
    raise AssertionError("INCREMENTAL_CONTROL_FORBIDDEN_EFFECT")


class Injected(RuntimeError):
    pass


def refusal(action, text=None, kinds=(ValueError, RuntimeError, OSError)):
    try:
        action()
    except kinds as error:
        need(text is None or text in str(error), "WRONG_REFUSAL:"+str(error))
        return error
    raise AssertionError("INCREMENTAL_CONTROL_EXPECTED_REFUSAL")


def passed(name, **evidence):
    check()
    CASES.append(dict(case=name, status="PASS", **evidence))


def module_from_bytes(name, path, raw):
    need(name not in sys.modules, "PRELOADED_MODULE")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def load(args):
    package = Path(args.package)
    need(package == PACKAGE and args.profile_sha256 == PROFILE_SHA and
         package.is_absolute() and package.resolve(strict=True) == package, "PACKAGE")
    raw = read(package/"PROFILE.json", expected=args.profile_sha256)
    descriptor = json.loads(raw)
    loader_raw = read(package/"profile.py")
    need(descriptor["files"]["profile.py"] == dict(bytes=len(loader_raw), sha256=sha(loader_raw)),
         "LOADER_PIN")
    loader = module_from_bytes("_incremental_control_profile", package/"profile.py", loader_raw)
    loaded = loader.load(package, args.profile_sha256,
        dict(python_runtime=args.python_runtime, lean_runtime=args.lean_runtime),
        START+WALL_SECONDS, check_parent=check)
    helper_raw = read(package/"custodian.py")
    need(descriptor["files"]["custodian.py"] == dict(bytes=len(helper_raw), sha256=sha(helper_raw)),
         "HELPER_PIN")
    helper = module_from_bytes("_incremental_control_custodian", package/"custodian.py", helper_raw)
    return NS(loaded=loaded, H=helper, package=package, profile=args.profile_sha256,
              profile_raw=raw, helper_raw=helper_raw,
              allowance=NS(check=check, deadline=START+WALL_SECONDS))


def fixture(s):
    B, A = s.loaded.baseline_intake.B, s.loaded.A
    raw = read(FIXTURE/"manifest.json", expected=MANIFEST_SHA)
    manifest = B.read_manifest(raw, MANIFEST_SHA, check_budget=check)
    need(manifest.unit_count == 47 and manifest.evidence_bytes == 695269, "RETAINED_FIXTURE_CENSUS")
    units, targets, pins = {}, [], [(FIXTURE/"manifest.json", len(raw), MANIFEST_SHA)]
    for batch in manifest.batches:
        for entry in batch:
            path = FIXTURE/entry.relative_path
            data = read(path, entry.raw_bytes, entry.raw_sha256)
            need(len(data) == entry.raw_bytes, "FIXTURE_LENGTH")
            parsed = A.PE.read_evidence(data)
            need(parsed.unit_id == entry.unit_id, "FIXTURE_IDENTITY")
            units[entry.unit_id] = data
            pins.append((path, len(data), entry.raw_sha256))
            for row in parsed.document["unit"][2]:
                targets.append(dict(name=deepcopy(row[0]), unit_id=entry.unit_id,
                    export_id=A.S.export_id(manifest.semantic_id, entry.unit_id, row[0])))
    targets.sort(key=lambda row: row["export_id"])
    need(len(targets) == 68 and len({row["export_id"] for row in targets}) == 68, "FIXTURE_OUTPUTS")
    small = sorted(targets, key=lambda row: (len(units[row["unit_id"]]), row["export_id"]))
    # Do not synthesize or recheck mathematics. These are exact retained units,
    # and projection may omit dependencies because this is inert custody only.
    return NS(units=units, targets=targets, small=small, pins=pins)


def bundle(s, f, base, name, targets):
    root = base/name
    root.mkdir(); (root/"units").mkdir()
    ids = sorted({row["unit_id"] for row in targets})
    raws = [f.units[uid] for uid in ids]
    B = s.loaded.baseline_intake.B
    manifest = B.make_manifest([raws], limits=B.Limits(**BUNDLE_LIMITS), check_budget=check)
    for uid in ids:
        write(root/"units"/(uid+".json"), f.units[uid])
    write(root/"manifest.json", manifest.raw)
    return dict(schema=s.H.APPEND_SCHEMA, bundle_directory=str(root),
        manifest=dict(path=str(root/"manifest.json"), sha256=manifest.sha256),
        targets=deepcopy(targets), share_all_bundle=True, allow_partial_publication=True,
        bundle_limits=deepcopy(BUNDLE_LIMITS))


def initialize(s, base, name, *, index_limits=None):
    root = base/name
    config = dict(schema=s.H.INIT_SCHEMA, custody_limits=deepcopy(CUSTODY_LIMITS),
        index_limits=deepcopy(index_limits or INDEX_LIMITS), partial_publication=True)
    result = s.H.initialize(s.loaded, root, config, s.allowance,
        profile_sha256=s.profile, finalize=check)
    need(result["status"] == "INITIALIZED_INCREMENTAL_INERT_HOST" and result["initialized"] and
         result["current_content"]["index_objects"] == 0, "INITIALIZATION_RESULT")
    raw = read(root/"HOST.json")
    need(sha(raw) == result["host_sha256"], "INITIAL_DESCRIPTOR_PIN")
    descriptor = json.loads(raw)
    need(set(descriptor) == set(s.H.DESCRIPTOR_FIELDS) and
         "index_snapshot_id" not in descriptor and "targets" not in descriptor,
         "STABLE_DESCRIPTOR_NOT_CONTENT_SEAL")
    clean(result)
    return NS(root=root, pin=sha(raw), descriptor=descriptor, raw=raw, initial=result)


def clean(result):
    need(result["custody_closure"] == result["index_closure"] == result["host_lock_closure"] == "CLOSED",
         "CLEAN_CLOSURE")


def append(s, host, config, *, finalize=check, pin=None):
    return s.H.append(s.loaded, host.root, config, s.allowance, profile_sha256=s.profile,
        expected_host_sha256=host.pin if pin is None else pin, finalize=finalize)


@contextmanager
def state(s, host):
    """Inspect only one scratch host with its normal lock and real store opens."""
    H, api, O = s.H, s.loaded.peer_api, s.loaded.O
    report = H._report("control-inspect", host.root, s.profile)
    with H._locked(s.loaded.A, host.root, report, create=False):
        custody = index = None
        try:
            custody = O.OrdinaryStore(host.root/"custody", host.descriptor["semantic_id"],
                                      host.descriptor["custody_limits"], create=False)
            index = api._index(s.loaded, None, custody,
                H._index_config(host.root, host.descriptor["index_limits"], create=False), check)
            yield NS(custody=custody, index=index, current=H._current_content(api, index, custody))
        finally:
            if index is not None:
                index.close()
            if custody is not None:
                custody.close()


def support(s, f, held, target, *, evidence=True, preview=True, indexed=True):
    api, A = s.loaded.peer_api, s.loaded.A
    raw = f.units[target["unit_id"]]
    prepared = api.PP.preview_from_evidence(raw, target["name"])
    if evidence:
        need(held.custody.get_evidence(A.S.semantic_id(), target["unit_id"], len(raw),
            check_budget=check) == raw, "EXACT_EVIDENCE_RETAINED")
        locator = A.E.strict_json(held.custody.get_locator(A.S.semantic_id(), target["export_id"],
            s.loaded.O.LOCATOR_MAX, check_budget=check))
        need(locator["unit_id"] == target["unit_id"] and locator["export_name"] == target["name"],
             "EXACT_LOCATOR_RETAINED")
    if preview:
        need(held.custody.get_preview(sha(prepared), len(prepared), check_budget=check) == prepared,
             "EXACT_PREVIEW_RETAINED")
    else:
        refusal(lambda: held.custody.get_preview(sha(prepared), len(prepared), check_budget=check),
                "ORDINARY_OBJECT_UNAVAILABLE")
    record = api.OrdinaryExportAdapter(A.S.semantic_id()).extract(prepared, expected_id=target["export_id"])
    rid = api.DS.record_id(record)
    row = held.index.db.execute("SELECT record_id FROM objects WHERE object_id=?", (target["export_id"],)).fetchone()
    if indexed:
        need(row == (rid,) and held.index._record(rid) == record, "INDEX_SUPPORT_INVARIANT")
    else:
        need(row is None, "UNCOMMITTED_TARGET_ABSENT")


def service(s, host, *, incremental=True):
    """Capture the helper's actual reopened snapshot; replace only networking."""
    H, api = s.H, s.loaded.peer_api
    ready_rows, opened = [], []
    async def capture(loaded, custody, config, allowance, *, ready=None):
        need(loaded is s.loaded and custody.root == host.root/"custody", "SERVICE_SELECTED_CUSTODY")
        contender = H._report("control-contend", host.root, s.profile)
        def contend():
            with H._locked(s.loaded.A, host.root, contender, create=False):
                raise AssertionError("INCREMENTAL_CONTROL_SERVICE_LOCK_NOT_HELD")
        refusal(contend, kinds=(OSError, ValueError))
        index = api._index(loaded, None, custody, config["index"], allowance.check)
        try:
            current = H._current_content(api, index, custody)
            opened.append(current)
            ready(dict(endpoint=dict(host="127.0.0.1", port=0), snapshot_id=current["index_snapshot_id"]))
            return dict(status="CONTROL_CAPTURED_SERVICE", quiescent=True,
                        current_snapshot=current["index_snapshot_id"])
        finally:
            index.close()
    config = dict(schema=H.SERVE_SCHEMA, host="127.0.0.1", port=0, tls=None,
        lease_seconds=1, cleanup_seconds=10, share_all_custody=True, exclusive=True,
        limits=dict(max_connections=1, max_requests=1, max_reply_bytes=MIB, operation_ms=1000))
    with patch.object(api, "serve", new=capture):
        result = H.serve(s.loaded, host.root, config, s.allowance, profile_sha256=s.profile,
            expected_host_sha256=host.pin, finalize=check, ready=ready_rows.append)
    clean(result)
    need(len(opened) == len(ready_rows) == 1 and
         result["service"]["current_snapshot"] == opened[0]["index_snapshot_id"], "SERVICE_CURRENT_OPEN")
    if incremental:
        need(result["current_content"] == ready_rows[0]["current_content"] == opened[0] and
             ready_rows[0]["host_sha256"] == host.pin and
             result["host_identity_kind"] == H.INCREMENTAL_IDENTITY and
             ready_rows[0]["prior_append_completion"] == "NOT_ASSERTED_BY_SERVICE" and
             result["prior_append_completion"] == "NOT_ASSERTED_BY_SERVICE" and
             "batch_complete" not in result, "SERVICE_DOES_NOT_CERTIFY_PRIOR_APPEND")
    else:
        need("current_content" not in result and "host_identity_kind" not in result,
             "V1_REPORT_CONTRACT_PRESERVED")
    need(read(host.root/"HOST.json") == host.raw, "DESCRIPTOR_STABLE_AFTER_SERVICE")
    return opened[0]


def interruption_controls(s, f, base, one):
    target = one["targets"][0]
    for stage in ("evidence", "preview", "index"):
        host = initialize(s, base, "interrupt-"+stage)
        owner = s.loaded.peer_api.DS.Store if stage == "index" else s.loaded.O.OrdinaryStore
        name = "admit" if stage == "index" else "put_"+stage
        original = getattr(owner, name)
        fired = []
        def after_commit(self, *args, **kwargs):
            result = original(self, *args, **kwargs)
            need(not fired, "EXACTLY_ONE_POSTCOMMIT_INJECTION")
            fired.append(result)
            raise Injected("AFTER_COMMIT_"+stage.upper())
        with patch.object(owner, name, new=after_commit):
            error = refusal(lambda: append(s, host, one), "AFTER_COMMIT_"+stage.upper(), (s.H.HostFailure,))
        report = error.report
        need(len(fired) == 1 and report["status"] == "FAILED" and report["batch_complete"] is False and
             report["durable_progress"] == "COMMITS_MAY_EXCEED_REPORTED_PROGRESS_ON_FAILURE",
             "POSTCOMMIT_FAILURE_NOT_COMPLETE")
        clean(report)
        field = {"evidence": "evidence", "preview": "previews", "index": "publications"}[stage]
        need(report[field] == [], "COMMIT_PRECEDES_REPORT_UPDATE")
        with state(s, host) as held:
            support(s, f, held, target, preview=stage != "evidence", indexed=stage == "index")
            need(held.current["index_objects"] == int(stage == "index"), "LEGAL_PARTIAL_INDEX_COUNT")
            expected = deepcopy(held.current)
        need(service(s, host) == expected, "SERVICE_REOPENS_PERMITTED_PREFIX")
        # This is an explicit new append, after inspection; no hidden auto-retry.
        completed = append(s, host, one)
        clean(completed)
        need(completed["batch_complete"] and completed["current_content"]["index_objects"] == 1,
             "EXPLICIT_IDEMPOTENT_COMPLETION")
        with state(s, host) as held:
            support(s, f, held, target)
        passed("exception-after-"+stage+"-commit-reopen-and-explicit-completion",
               injection="PYTHON_EXCEPTION_AFTER_REAL_SQLITE_COMMIT_NOT_PROCESS_CRASH",
               failed_progress_rows=len(report[field]), committed_index_before_completion=expected["index_objects"])


def cumulative_controls(s, f, base):
    host = initialize(s, base, "cumulative65")
    first = bundle(s, f, base, "bundle64", f.targets[:64])
    last = bundle(s, f, base, "bundle65", f.targets[64:65])
    a = append(s, host, first); clean(a)
    need(a["batch_complete"] and len(a["publications"]) == 64 and a["current_content"]["index_objects"] == 64,
         "FIRST_BOUNDED_BATCH64")
    old_snapshot = a["current_content"]["index_snapshot_id"]
    b = append(s, host, last); clean(b)
    need(b["batch_complete"] and b["current_content"]["index_objects"] == 65 and
         b["current_content"]["index_snapshot_id"] != old_snapshot, "CUMULATIVE65")
    with state(s, host) as held:
        need(held.index.status()["snapshots"] == 66 and
             s.loaded.peer_api.DS.A.snapshot_id(held.index.snapshot(old_snapshot)) == old_snapshot,
             "HISTORICAL_SNAPSHOT_PRESERVED")
        for target in f.targets[:65]:
            support(s, f, held, target)
    duplicate = append(s, host, last); clean(duplicate)
    need(duplicate["current_content"] == b["current_content"] and
         all(row["new"] is False for key in ("evidence", "previews", "publications") for row in duplicate[key]),
         "DUPLICATES_DO_NOT_GROW_CONTENT_OR_SNAPSHOT")
    need(service(s, host) == b["current_content"] and read(host.root/"HOST.json") == host.raw,
         "SAME_DESCRIPTOR_REPORTS_NEW_CURRENT_SNAPSHOT")
    too_many = deepcopy(first); too_many["targets"] = deepcopy(f.targets[:65])
    refusal(lambda: append(s, host, too_many), "HOST_TARGET_COUNT")
    passed("cumulative65-via64-plus1-stable-descriptor-old-snapshot-and-duplicates",
           cumulative_targets=65, largest_invocation_targets=64, old_snapshot=old_snapshot,
           current_snapshot=b["current_content"]["index_snapshot_id"])


def refusal_controls(s, f, base, one):
    host = initialize(s, base, "refusals")
    before = service(s, host)
    refusal(lambda: append(s, host, one, pin="0"*64), "HOST_SEAL_PIN", (s.H.HostFailure,))
    for flag in ("share_all_bundle", "allow_partial_publication"):
        config = deepcopy(one); config[flag] = False
        refusal(lambda config=config: append(s, host, config), "HOST_APPEND_SCHEMA_OR_DISCLOSURE")
    config = deepcopy(one); config["targets"][0]["export_id"] = "0"*64
    refusal(lambda: append(s, host, config), "HOST_TARGET_IDENTITY_OR_DUPLICATE")
    config = deepcopy(one); config["manifest"]["sha256"] = "0"*64
    refusal(lambda: append(s, host, config))
    # A separately selected descriptor cannot silently change an existing DB's limits.
    for label, edit in (
        ("profile", lambda doc: doc.update(profile_sha256="0"*64)),
        ("namespace", lambda doc: doc.update(namespace="0"*64)),
        ("partial-policy", lambda doc: doc.update(partial_publication=False)),
        ("custody-limits", lambda doc: doc["custody_limits"].update(objects=257)),
        ("index-limits", lambda doc: doc["index_limits"].update(max_objects=129)),
    ):
        altered = deepcopy(host.descriptor); edit(altered)
        data = canonical(altered)
        try:
            (host.root/"HOST.json").write_bytes(data)
            refusal(lambda: append(s, host, one, pin=sha(data)), kinds=(s.H.HostFailure,))
        finally:
            (host.root/"HOST.json").write_bytes(host.raw)
    locked = s.H._report("control-held", host.root, s.profile)
    with s.H._locked(s.loaded.A, host.root, locked, create=False):
        refusal(lambda: append(s, host, one), kinds=(s.H.HostFailure,))
    need(service(s, host) == before, "REFUSALS_PRESERVE_EMPTY_STORES")
    passed("descriptor-pin-profile-namespace-policy-store-limits-target-manifest-and-lock-refusals")


def capacity_and_conflict_controls(s, f, base, one):
    limits = deepcopy(INDEX_LIMITS); limits["max_objects"] = 1
    host = initialize(s, base, "capacity", index_limits=limits)
    first = append(s, host, one); clean(first)
    target = next(row for row in f.small if row["export_id"] != one["targets"][0]["export_id"])
    second = bundle(s, f, base, "capacity-extra", [target])
    error = refusal(lambda: append(s, host, second), "OBJECT_CAP", (s.H.HostFailure,))
    clean(error.report)
    need(error.report["batch_complete"] is False, "CAPACITY_NOT_COMPLETE")
    with state(s, host) as held:
        support(s, f, held, one["targets"][0])
        support(s, f, held, target, indexed=False)
        need(held.current["index_objects"] == 1 and
             held.current["index_snapshot_id"] == first["current_content"]["index_snapshot_id"],
             "CAPACITY_PRESERVES_OLD_INDEX")
        expected = deepcopy(held.current)
    need(service(s, host) == expected, "CAPACITY_PREFIX_SERVABLE")
    passed("index-capacity-refusal-preserves-old-record-and-approved-unindexed-support")

    corrupt = initialize(s, base, "scratch-conflict")
    good = append(s, corrupt, one); clean(good)
    uid = one["targets"][0]["unit_id"]
    # Deliberate test-only database fault, not a supported way to manufacture a
    # content-address collision. Preserve this corrupt scratch root afterward.
    with state(s, corrupt) as held:
        held.custody.db.execute("UPDATE objects SET raw_sha256=? WHERE kind='evidence' AND identity=?",
                                ("0"*64, uid))
    error = refusal(lambda: append(s, corrupt, one), "ORDINARY_CUSTODY_CONFLICT", (s.H.HostFailure,))
    clean(error.report)
    with state(s, corrupt) as held:
        row = held.custody.db.execute("SELECT raw_sha256,raw FROM objects WHERE kind='evidence' AND identity=?",
                                     (uid,)).fetchone()
        need(row == ("0"*64, f.units[uid]) and held.current == good["current_content"],
             "CONFLICT_REFUSES_WITHOUT_OVERWRITE")
    passed("deliberately-corrupted-scratch-digest-refuses-duplicate-without-overwrite",
           scope="DEFENSIVE_CONFLICT_NOT_REACHABLE_CONTENT_HASH_COLLISION")


def initialization_controls(s, base, one):
    config = dict(schema=s.H.INIT_SCHEMA, custody_limits=deepcopy(CUSTODY_LIMITS),
                  index_limits=deepcopy(INDEX_LIMITS), partial_publication=True)
    for point in ("index-create", "pre-descriptor-finalize"):
        root = base/("failed-init-"+point)
        calls = []
        def finalize():
            check(); calls.append(True)
            if point == "pre-descriptor-finalize" and len(calls) == 2:
                raise Injected("INIT_BEFORE_DESCRIPTOR")
        def action():
            return s.H.initialize(s.loaded, root, config, s.allowance,
                profile_sha256=s.profile, finalize=finalize)
        with ExitStack() as patches:
            if point == "index-create":
                patches.enter_context(patch.object(s.loaded.peer_api, "_index", side_effect=Injected("INIT_INDEX_CREATE")))
            error = refusal(action, kinds=(s.H.HostFailure,))
        need(error.report["initialized"] is False and not (root/"HOST.json").exists() and
             (root/s.H.MARKER).is_file() and error.report["custody_closure"] == "CLOSED" and
             error.report["host_lock_closure"] == "CLOSED", "INITIALIZATION_FAILS_CLOSED")
        partial = NS(root=root, pin="0"*64)
        refusal(lambda: append(s, partial, one), kinds=(s.H.HostFailure,))
        refusal(action)
    passed("initialization-failures-preserve-unusable-root-without-descriptor-or-reinitialization")


def static_compatibility(s, f, base, one):
    root = base/"static-v1"
    config = {key: deepcopy(value) for key, value in one.items() if key != "allow_partial_publication"}
    config.update(schema=s.H.PREPARE_SCHEMA, custody_limits=deepcopy(CUSTODY_LIMITS),
                  index_limits=deepcopy(INDEX_LIMITS))
    result = s.H.prepare(s.loaded, root, config, s.allowance, profile_sha256=s.profile, finalize=check)
    clean(result)
    raw = read(root/"HOST.json")
    host = NS(root=root, pin=sha(raw), raw=raw, descriptor=json.loads(raw))
    need(host.descriptor["schema"] == s.H.SEAL_SCHEMA, "V1_PREPARE_PRESERVED")
    refusal(lambda: append(s, host, one), "HOST_APPEND_REQUIRES_INCREMENTAL_HOST", (s.H.HostFailure,))
    service(s, host, incremental=False)
    passed("static-v1-prepare-serve-preserved-and-append-refused")


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTEXT")
    output = Path(args.output)
    need(output.is_absolute() and output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         output.parent.resolve(strict=True) == output.parent and not os.path.lexists(output), "FRESH_OUTPUT")
    output.mkdir()
    own_raw = read(Path(__file__).absolute())
    result = dict(passed=False, cases=CASES, profile_sha256=args.profile_sha256,
        control_sha256=sha(own_raw), fixture_manifest_sha256=MANIFEST_SHA,
        scope="REAL_SQLITE_LIFECYCLE_WITH_POSTCOMMIT_EXCEPTIONS_NOT_PROCESS_CRASH_OR_NETWORK_OR_MATHEMATICS")
    connect = sqlite3.connect
    def scratch_connect(database, *a, **kw):
        path = Path(database)
        need(path.is_absolute() and path.is_relative_to(output) and not kw.get("uri", False),
             "DATABASE_OUTSIDE_SCRATCH")
        connection = connect(database, *a, **kw)
        CONNECTIONS.append(connection)
        return connection
    try:
        with ExitStack() as guards:
            guards.enter_context(patch.object(sqlite3, "connect", new=scratch_connect))
            for name in ("subprocess.Popen", "os.system", "asyncio.open_connection", "asyncio.start_server"):
                guards.enter_context(patch(name, new=forbidden))
            s = load(args)
            guards.enter_context(patch.object(s.loaded.A.OrdinaryAdmission, "__init__", new=forbidden))
            guards.enter_context(patch.object(s.loaded.peer_api.H.Provider, "start", new=forbidden))
            f = fixture(s)
            one = bundle(s, f, output, "small-bundle", f.small[:1])
            interruption_controls(s, f, output, one)
            cumulative_controls(s, f, output)
            refusal_controls(s, f, output, one)
            capacity_and_conflict_controls(s, f, output, one)
            initialization_controls(s, output, one)
            static_compatibility(s, f, output, one)
            s.loaded.profile.verify(check)
            need(read(s.package/"PROFILE.json") == s.profile_raw and
                 read(s.package/"custodian.py") == s.helper_raw and
                 read(Path(__file__).absolute()) == own_raw, "SOURCES_UNCHANGED")
            for path, size, digest in f.pins:
                need(len(read(path, size, digest)) == size, "FIXTURE_UNCHANGED")
            for connection in CONNECTIONS:
                refusal(lambda connection=connection: connection.execute("SELECT 1"),
                        kinds=(sqlite3.ProgrammingError,))
            result["passed"] = True
    except BaseException as error:
        result.update(error_type=type(error).__name__, error=str(error)[:2000])
    result.update(completed_groups=len(CASES), database_connections=len(CONNECTIONS),
                  wall_seconds=time.monotonic()-START, harness_cpu_seconds=time.process_time()-CPU)
    save(output/"RESULT.json", result)
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

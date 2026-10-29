"""Focused standalone inert-host controls; root selects finite execution separately.

Actual pinned pure sources and fresh SQLite stores; no native or application
network execution. One orderly postcommit exception is not a power-loss test.
"""
from __future__ import annotations

import argparse
import asyncio
from contextlib import ExitStack, contextmanager
from copy import deepcopy
import dataclasses
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import sys
import time
from types import ModuleType, SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PACKAGE = ROOT / "experiments/v5-local-checks/inert-host-pack01/packed/inert-host"
PROFILE = "d6c1f02949962d26a565910f7d2bf064987597aeb418446067c66fc8a107c4db"
FIXTURE = ROOT / "experiments/v5-local-checks/ordinary-project-extraction-public-01/project/completion"
FIXTURE_PIN = "d031230312290008c5b09bb0587615d9a02310b4cfdc014ccbee2b491477d298"
OLD_HOST = ROOT / "experiments/v5-local-checks/incremental-host-public01/suite/host/HOST.json"
OLD_HOST_PIN = "45db32b2c53e86b03920ffab2d95fcc31700f40c2a76902899cc0f9ff75058e8"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
START, CPU, MIB = time.monotonic(), time.process_time(), 1024**2
CASES, CONNECTIONS, AUDIT = [], [], None
CUSTODY = dict(objects=64, exports=512, logical_bytes=4*MIB, db_pages=1024)
INDEX = dict(max_objects=16, max_postings=8192, max_features=4096,
             max_snapshots=17, max_logical_bytes=8*MIB, max_db_pages=2048)


def need(value, code):
    if not value:
        raise AssertionError("PURE_HOST_CONTROL_" + code)


def check():
    need(time.monotonic()-START < 150 and time.process_time()-CPU < 75,
         "ORIGINAL_ALLOWANCE")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      allow_nan=False, separators=(",", ":")).encode("ascii")


def read(path, expected=None, maximum=2*MIB):
    check()
    need(path.is_absolute() and path.resolve(strict=True) == path and path.is_file(), "INPUT_PATH")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(0 < len(raw) <= maximum and (expected is None or digest(raw) == expected), "INPUT_PIN")
    return raw


def write(path, raw):
    need(type(raw) is bytes and 0 < len(raw) <= 2*MIB, "OUTPUT_BOUND")
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "SHORT_WRITE")


def forbidden(*_args, **_kwargs):
    raise AssertionError("PURE_HOST_CONTROL_FORBIDDEN_EFFECT")


class Injected(RuntimeError):
    pass


def refusal(action, code=None, kinds=(ValueError, RuntimeError, OSError)):
    try:
        action()
    except kinds as error:
        need(code is None or code in str(error), "WRONG_REFUSAL:" + str(error))
        return error
    raise AssertionError("PURE_HOST_CONTROL_EXPECTED_REFUSAL")


def passed(name, **evidence):
    check(); CASES.append(dict(case=name, status="PASS", **evidence))


def audit(event, args):
    if AUDIT is None:
        return
    if event == "import":
        name = args[0]
        need(not any(name == stem or name.startswith(stem + ".") for stem in
            ("ordinary_admission", "portable_catalog", "local_catalog", "ordinary_contribution",
             "baseline_intake", "peer_api", "owner")), "NATIVE_OR_OWNER_IMPORT:" + name)
    if event == "open" and not isinstance(args[0], int):
        path = Path(os.fsdecode(args[0])).absolute()
        need(not path.is_relative_to(ROOT / "software/runtime") and
             not any(part in ("installation", "lean-lib", "lean-src", "foundation") for part in path.parts),
             "NATIVE_SUPPORT_READ:" + str(path))
        if path.suffix.lower() in (".exe", ".dll") or ".olean" in path.name or path.suffix == ".lean":
            need(path in AUDIT.python_files, "NATIVE_ARTIFACT_READ:" + str(path))


def module(name, path, raw):
    need(name not in sys.modules, "PRELOADED_TEST_MODULE")
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    exec(compile(raw, str(path), "exec", dont_inherit=True), value.__dict__)
    return value


def clone(s, base, label, *, corrupt=None, extra_role=False):
    root = base/label; root.mkdir()
    document = json.loads(s.profile_raw)
    if extra_role:
        document["files"]["ordinary_admission"] = deepcopy(document["files"]["_core"])
    for name, raw in s.bound.raws.items():
        path = root/document["files"][name]["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        write(path, raw+b"\n# altered control copy\n" if name == corrupt else raw)
    manifest = encode(document) if extra_role else s.profile_raw
    write(root/"SOURCES.json", manifest)
    return root, digest(manifest)


def loader_controls(s, base):
    refusal(lambda: s.R.bind(s.package, "0"*64, s.python, check), "PROFILE_PIN")
    altered, pin = clone(s, base, "altered-codec", corrupt="ordinary_evidence")
    refusal(lambda: s.R.bind(altered, pin, s.python, check), "PIN_SIZE_CHANGED")
    extra, pin = clone(s, base, "extra-native-role", extra_role=True)
    refusal(lambda: s.R.bind(extra, pin, s.python, check), "SOURCE_ROLE_SET")
    sys.modules["ordinary_evidence"] = ModuleType("ordinary_evidence")
    try:
        refusal(lambda: s.R.load_support(s.bound, check), "PRELOADED_SUPPORT")
    finally:
        del sys.modules["ordinary_evidence"]
    passed("profile-source-role-and-preloaded-module-refusals")


def load(s):
    s.support = s.R.load_support(s.bound, check)
    s.H = s.R.load_source("_inert_host_core", s.bound.paths["_core"], s.bound.raws["_core"])
    s.allowance = NS(check=check, deadline=START+150)
    S = s.support
    need(type(S) is s.R.InertHostSupport and set(S.modules) == set(s.R.ORDER) and
         S.semantic_id == SEMANTIC and S.namespace == S.OA.namespace_for(SEMANTIC), "REAL_INERT_ROLE")
    need(all(sys.modules[name].__path__ == [] for name in s.R.PACKAGES), "CLOSED_PACKAGE_PATHS")
    need(not any(name in sys.modules for name in
         ("ordinary_admission", "ordinary_contribution", "portable_catalog", "local_catalog", "peer_api")),
         "NO_MATHEMATICAL_MODULES")
    s.H._modules(S, s.allowance, PROFILE, S.verify)
    refusal(lambda: s.H._modules(NS(**S.__dict__), s.allowance, PROFILE, S.verify), "SELECTED_INERT_SUPPORT")
    refusal(lambda: s.H._modules(S, s.allowance, "0"*64, S.verify), "SUPPORT_PROFILE_BINDING")
    def expired():
        raise Injected("ORIGINAL_ALLOWANCE_ALREADY_EXPIRED")
    refusal(lambda: s.H._modules(S, NS(check=expired, deadline=START-1), PROFILE, S.verify),
            "ORIGINAL_ALLOWANCE_ALREADY_EXPIRED")
    passed("standalone-pure-closure-authentic-role-namespace-and-original-budget")


def fixture(s, base):
    raw = read(FIXTURE/"RESULT.json", FIXTURE_PIN)
    doc = json.loads(raw)
    need(len(doc["units"]) == 3 and len(doc["targets"]) == 1 and doc["semantic_id"] == SEMANTIC,
         "FIXTURE_LAYOUT")
    units, pins = {}, [(FIXTURE/"RESULT.json", FIXTURE_PIN)]
    for row in doc["units"]:
        path = FIXTURE/"evidence"/(row["unit_id"]+".json")
        data = read(path, row["sha256"], row["bytes"])
        need(len(data) == row["bytes"], "FIXTURE_SIZE")
        units[row["unit_id"]] = data; pins.append((path, row["sha256"]))
    # Retain applyTwice as support; omit applyTwice_eq while retaining its
    # consumer. This gives a real missing non-foundation import, not just Eq.
    supplied = [doc["units"][i]["unit_id"] for i in (0, 2)]
    missing = doc["units"][1]["unit_id"]
    PE, E, S, B = (s.support.api[key] for key in ("PE", "E", "S", "B"))
    omitted = PE.read_evidence(units[missing])
    omitted_exports = {S.export_id(SEMANTIC, missing, row[0]) for row in omitted.document["unit"][2]}
    consumer = PE.read_evidence(units[supplied[1]])
    need(any(row[1] in omitted_exports for row in consumer.document["imports"]), "REAL_UNSUPPLIED_IMPORT")
    limits = B.Limits(max_units=4, max_bytes=MIB, max_batch_units=4, max_batch_bytes=MIB)
    manifest = B.make_manifest([[units[uid] for uid in supplied]], limits=limits, check_budget=check)
    bundle = base/"sparse-bundle"; bundle.mkdir(); (bundle/"units").mkdir()
    for uid in supplied:
        write(bundle/"units"/(uid+".json"), units[uid])
    write(bundle/"manifest.json", manifest.raw)
    config = dict(schema=s.H.APPEND_SCHEMA, bundle_directory=str(bundle),
        manifest=dict(path=str(bundle/"manifest.json"), sha256=manifest.sha256),
        targets=deepcopy(doc["targets"]), share_all_bundle=True, allow_partial_publication=True,
        bundle_limits=dict(max_units=4, max_bytes=MIB, max_batch_units=4, max_batch_bytes=MIB))
    return NS(units=units, pins=pins, supplied=supplied, missing=missing, omitted_exports=omitted_exports,
              target=doc["targets"][0], config=config, bytes=sum(len(units[uid]) for uid in supplied))


def init(s, base, label):
    root = base/label
    config = dict(schema=s.H.INIT_SCHEMA, custody_limits=CUSTODY, index_limits=INDEX, partial_publication=True)
    result = s.H.initialize(s.support, root, config, s.allowance, profile_sha256=PROFILE,
                           finalize=s.support.verify)
    raw = read(root/"HOST.json")
    need(result["initialized"] and result["host_sha256"] == digest(raw), "INITIAL_DESCRIPTOR")
    clean(result)
    return NS(root=root, raw=raw, pin=digest(raw), descriptor=json.loads(raw),
              lock_inode=(root/"host.lock").stat().st_ino)


def clean(report):
    need(report["mathematical_acceptance"] is False and report["cleanup_errors"] == [] and
         all(report[key+"_closure"] == "CLOSED" for key in ("custody", "index", "host_lock")),
         "CLEAN_INERT_CLOSURE")


def append(s, host, config):
    return s.H.append(s.support, host.root, config, s.allowance, profile_sha256=PROFILE,
        expected_host_sha256=host.pin, finalize=s.support.verify)


@contextmanager
def state(s, host):
    report = s.H._report("control-read", host.root, PROFILE)
    with s.H._locked(s.support, s.support.api, host.root, report, create=False):
        custody = index = None
        try:
            custody = s.support.O.OrdinaryStore(host.root/"custody", SEMANTIC, CUSTODY, create=False)
            index = s.H._index(s.support, custody, s.H._index_config(host.root, INDEX, create=False), check)
            yield NS(custody=custody, index=index)
        finally:
            if index is not None: index.close()
            if custody is not None: custody.close()


def inspect(s, f, host):
    with state(s, host) as held:
        for uid in f.supplied:
            need(held.custody.get_evidence(SEMANTIC, uid, len(f.units[uid]), check_budget=check) == f.units[uid],
                 "SUPPORT_AND_CONSUMER_EXACT_BYTES")
        refusal(lambda: held.custody.get_evidence(SEMANTIC, f.missing, len(f.units[f.missing]), check_budget=check),
                "ORDINARY_OBJECT_UNAVAILABLE")
        preview = s.support.PP.preview_from_evidence(f.units[f.target["unit_id"]], f.target["name"])
        need(held.custody.get_preview(digest(preview), len(preview), check_budget=check) == preview,
             "EXACT_PREVIEW")
        record = s.support.OA.OrdinaryExportAdapter(SEMANTIC).extract(preview, expected_id=f.target["export_id"])
        row = held.index.db.execute("SELECT record_id FROM objects WHERE object_id=?",
                                    (f.target["export_id"],)).fetchone()
        need(row == (s.support.DS.record_id(record),) and held.index._record(row[0]) == record,
             "INDEX_SUPPORT_INVARIANT")
        current = s.H._current_content(s.support.api, held.index, held.custody)
        need(current["index_objects"] == 1, "ONE_SELECTED_TARGET_ONLY")
    need(read(host.root/"HOST.json") == host.raw and (host.root/"host.lock").stat().st_ino == host.lock_inode,
         "IMMUTABLE_DESCRIPTOR_PERMANENT_LOCK")
    return current


def service_config(s):
    return dict(schema=s.H.SERVE_SCHEMA, host="127.0.0.1", port=0, tls=None,
        lease_seconds=1, cleanup_seconds=10, limits=dict(max_connections=1, max_requests=4,
        max_reply_bytes=MIB, operation_ms=1000), share_all_custody=True, exclusive=True)


def serve(s, host, config):
    return s.H.serve(s.support, host.root, config, s.allowance, profile_sha256=PROFILE,
                    expected_host_sha256=host.pin, finalize=s.support.verify)


def storage_controls(s, f, base):
    host = init(s, base, "sparse-host")
    result = append(s, host, f.config); clean(result)
    need(result["batch_complete"] and [row["identity"] for row in result["evidence"]] == f.supplied,
         "SUPPLIED_ORDER_AND_COMPLETION")
    inspect(s, f, host)
    passed("real-sparse-append-keeps-support-unit-without-import-closure", units=2, evidence_bytes=f.bytes)

    prefix = init(s, base, "postcommit-prefix")
    original = s.support.DS.Store.admit
    fired = []
    def after_commit(self, *args, **kwargs):
        value = original(self, *args, **kwargs); fired.append(value)
        raise Injected("AFTER_REAL_INDEX_COMMIT")
    with patch.object(s.support.DS.Store, "admit", new=after_commit):
        error = refusal(lambda: append(s, prefix, f.config), "AFTER_REAL_INDEX_COMMIT", kinds=(s.H.HostFailure,))
    need(len(fired) == 1 and error.report["batch_complete"] is False and
         error.report["publications"] == [] and error.report["host_lock_closure"] == "CLOSED",
         "UNREPORTED_COMMITTED_PREFIX")
    inspect(s, f, prefix)
    passed("one-real-postcommit-exception-preserves-supported-index-prefix")

    report = s.H._report("held-control", host.root, PROFILE)
    with s.H._locked(s.support, s.support.api, host.root, report, create=False):
        refusal(lambda: append(s, host, f.config), kinds=(s.H.HostFailure,))
        need((host.root/"host.lock").stat().st_ino == host.lock_inode, "CONTENDED_LOCK_NOT_REPLACED")
    inspect(s, f, host)
    old_raw = read(OLD_HOST, OLD_HOST_PIN)
    old_root = base/"old-profile-descriptor"; old_root.mkdir()
    write(old_root/s.H.MARKER, s.support.E.canonical_json(dict(schema=s.H.MARKER_SCHEMA)))
    write(old_root/"host.lock", b"\0"); write(old_root/"HOST.json", old_raw)
    old = NS(root=old_root, pin=OLD_HOST_PIN)
    before = len(CONNECTIONS)
    refusal(lambda: append(s, old, f.config), "DESCRIPTOR_IDENTITY", kinds=(s.H.HostFailure,))
    need(len(CONNECTIONS) == before and read(old_root/"HOST.json") == old_raw and
         not (old_root/"custody").exists() and not (old_root/"index").exists(), "OLD_PROFILE_NO_DATABASE_OPEN")
    passed("permanent-lock-contention-and-exact-retained-old-descriptor-refusal")

    static_config = deepcopy(f.config)
    static_config.update(schema=s.H.PREPARE_SCHEMA, custody_limits=CUSTODY, index_limits=INDEX)
    del static_config["allow_partial_publication"]
    static_root = base/"static-host"
    result = s.H.prepare(s.support, static_root, static_config, s.allowance,
                        profile_sha256=PROFILE, finalize=s.support.verify)
    clean(result)
    static = NS(root=static_root, pin=result["host_sha256"])
    refusal(lambda: append(s, static, f.config), "APPEND_REQUIRES_INCREMENTAL_HOST", kinds=(s.H.HostFailure,))
    passed("static-sparse-generation-preserved-and-refuses-append")
    return host


def service_controls(s, host):
    remote = service_config(s); remote["host"] = "192.0.2.1"
    error = refusal(lambda: serve(s, host, remote), "REMOTE_TLS_REQUIRED", kinds=(s.H.HostFailure,))
    need(error.report["custody_closure"] == error.report["host_lock_closure"] == "CLOSED",
         "REMOTE_REFUSAL_CLOSED")
    passed("moved-service-requires-remote-TLS-before-listener")

    created, drained = [], []
    class FailingProvider:
        def __init__(self, *, index, ordinary, **_limits):
            self.index, self.ordinary = index, ordinary
            self.server, self.tasks, self.reserved_reply_bytes = None, set(), 0
            created.append(self)
        async def start(self, *_args, **_kwargs):
            async def pending():
                try:
                    await asyncio.Event().wait()
                finally:
                    contender = s.H._report("drain-contender", host.root, PROFILE)
                    def lock():
                        with s.H._locked(s.support, s.support.api, host.root, contender, create=False):
                            raise AssertionError("PURE_HOST_CONTROL_LOCK_RELEASED_BEFORE_DRAIN")
                    refusal(lock, kinds=(OSError,))
                    drained.append(True)
            self.tasks.add(asyncio.create_task(pending()))
            await asyncio.sleep(0)
            raise Injected("START_FAILURE_AFTER_OWNED_TASK")
        async def stop(self):
            raise Injected("STOP_FAILURE_REQUIRES_FALLBACK_DRAIN")
        def status(self):
            return dict(status="CONTROL_FAKE_PROVIDER", tasks=len(self.tasks),
                        reserved_reply_bytes=self.reserved_reply_bytes)
    with patch.object(s.support.H, "Provider", new=FailingProvider):
        error = refusal(lambda: serve(s, host, service_config(s)), "START_FAILURE_AFTER_OWNED_TASK",
                        kinds=(s.H.HostFailure,))
    report = error.report
    need(len(created) == 1 and drained == [True] and all(task.done() for task in created[0].tasks)
         and created[0].index.db is None and report["service"]["cleanup_errors"] and
         report["service"]["quiescent"] is False and
         report["custody_closure"] == report["host_lock_closure"] == "CLOSED" and
         (host.root/"host.lock").stat().st_ino == host.lock_inode, "FALLBACK_DRAIN_UNDER_PERMANENT_LOCK")
    passed("provider-cleanup-failure-is-terminal-and-drains-before-lock-release")


def main():
    global AUDIT
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("package", "profile-sha256", "python-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTEXT")
    package, output, python = Path(args.package), Path(args.output), Path(args.python_runtime)
    need(package == PACKAGE and args.profile_sha256 == PROFILE and output.is_absolute() and
         output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         output.parent.resolve(strict=True) == output.parent and not os.path.lexists(output) and
         not output.is_relative_to(package) and not package.is_relative_to(output), "SELECTED_OUTPUT")
    own_path = Path(__file__).absolute(); own_raw = read(own_path)
    profile_raw = read(package/"SOURCES.json", PROFILE); profile = json.loads(profile_raw)
    entry_raw = read(package/"run.py", profile["files"]["_entry"]["sha256"])
    output.mkdir()
    result = dict(passed=False, cases=CASES, profile_sha256=PROFILE, control_sha256=digest(own_raw),
                  scope="PURE_HOST_CHANGED_BOUNDARY_NOT_MATHEMATICAL_ACCEPTANCE")
    connect = sqlite3.connect
    def scratch_connect(database, *args, **kwargs):
        path = Path(database)
        need(path.is_absolute() and path.is_relative_to(output) and not kwargs.get("uri", False),
             "DATABASE_OUTSIDE_FRESH_CONTROL_OUTPUT")
        value = connect(database, *args, **kwargs); CONNECTIONS.append(value); return value
    try:
        AUDIT = NS(python_files={python/name for name in ("python.exe", "python314.dll", "python3.dll")})
        sys.addaudithook(audit)
        with ExitStack() as guards:
            guards.enter_context(patch.object(sqlite3, "connect", new=scratch_connect))
            for name in ("subprocess.Popen", "os.system", "asyncio.open_connection", "asyncio.start_server"):
                guards.enter_context(patch(name, new=forbidden))
            entry = module("_inert_control_entry", package/"run.py", entry_raw)
            R, captured_profile, _ = entry.bootstrap(package, PROFILE, check)
            need(captured_profile == profile_raw, "ACTUAL_BOOTSTRAP_PROFILE")
            bound = R.bind(package, PROFILE, python, check)
            s = NS(R=R, package=package, python=python, bound=bound, profile_raw=profile_raw)
            loader_controls(s, output)
            load(s)
            guards.enter_context(patch.object(s.support.H.Provider, "start", new=forbidden))
            guards.enter_context(patch.object(s.support.H, "exchange", new=forbidden))
            f = fixture(s, output)
            host = storage_controls(s, f, output)
            service_controls(s, host)
            s.support.verify()
            need(read(own_path) == own_raw, "CONTROL_SOURCE_UNCHANGED")
            for path, pin in f.pins:
                read(path, pin)
            read(OLD_HOST, OLD_HOST_PIN)
            for connection in CONNECTIONS:
                refusal(lambda connection=connection: connection.execute("SELECT 1"),
                        kinds=(sqlite3.ProgrammingError,))
            result.update(passed=True, native_calls=0, owner_calls=0, application_network_calls=0)
    except BaseException as error:
        result.update(error_type=type(error).__name__, error=str(error)[:2000])
    result.update(completed_groups=len(CASES), database_connections=len(CONNECTIONS),
                  wall_seconds=time.monotonic()-START, harness_cpu_seconds=time.process_time()-CPU)
    write(output/"RESULT.json", encode(result))
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

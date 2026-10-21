"""One selected real owner crash; no service, mathematical work or deletion.

The intentionally failed worker remains failed. A passing fixture means the
surviving supervisor earned QUIESCED_UNCLEAN using its actual live handles.
"""
import time
STARTED = time.monotonic()
OUTER = STARTED + 90
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
INSTALL = PROJECT/"product-local/v5-distribution-consolidated-01/Mathematical Commons v5"
BASE = PROJECT/"product-local/v4-library-commons-02/commons-v4"
SNAPSHOT = Path(__file__).resolve().parents[3]
RELEASE = "1fd0ae63faa84cc1f3ef82f17d2056657f8d6a3e5dea3686ace433987bd1e5be"
MANIFEST = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
MIB = 1024**2
CLOCK_LOWER = 1577836800000  # Owner premise: actual UTC is after 2020-01-01.
EXTRA = {
    "v5/placement/reclaim.py": "software/v5/bounded_reclamation/placement/reclaim.py",
    "v5/placement/sessions.py": "software/v5/supervised_generations/placement/sessions.py",
    "v5/placement/lifecycle.py": "software/v5/supervised_generations/placement/lifecycle.py",
}


def need(ok, why):
    if not ok: raise ValueError(why)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(raw): return hashlib.sha256(raw).hexdigest()


def ordinary(path, *, directory=False):
    path = Path(path)
    need(path.is_absolute() and path.resolve() == path and all(
        not p.is_symlink() and not p.is_junction() for p in (path, *path.parents)), "CRASH_ORDINARY_PATH")
    need(path.is_dir() if directory else path.is_file(), "CRASH_PATH_KIND")
    return path


def read(path, digest=None, maximum=2*MIB):
    path = ordinary(path)
    need(path.stat().st_size <= maximum, "CRASH_INPUT_SIZE")
    with path.open("rb") as stream: raw = stream.read(maximum+1)
    need(len(raw) <= maximum and (digest is None or sha(raw) == digest), "CRASH_INPUT_PIN")
    return raw


def save(path, value):
    raw = encode(value)+b"\n"; need(len(raw) <= MIB, "CRASH_REPORT_SIZE")
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "CRASH_SHORT_REPORT")
        stream.flush(); os.fsync(stream.fileno())


def load(name, path, expected, size):
    raw = read(path, expected); need(len(raw) == size, "CRASH_SOURCE_EXTENT")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def adopt(request):
    need(set(request) == {"schema", "additions"} and request["schema"] ==
         "DMKN_SUPERVISED_CRASH_INPUT_V1" and set(request["additions"]) == set(EXTRA), "CRASH_INPUT_SCHEMA")
    release = json.loads(read(INSTALL/"V5-RELEASE.json", RELEASE, 8*MIB))
    need(release["schema"] == "DMKN_V5_DIRECTORY_RELEASE_V3" and len(release["sdk_sources"]) == 121,
         "CRASH_INSTALLED_MAP")
    need(Path(sys.executable).resolve() == INSTALL/"base/receiver/runtime/python/python.exe", "CRASH_PYTHON")
    selected = {}
    for logical, relative in release["sdk_sources"].items():
        need(relative == "sdk/"+logical and "\\" not in relative and
             all(p not in (".", "..", "") for p in PurePosixPath(relative).parts), "CRASH_SDK_PATH")
        row = release["files"][relative]; path = INSTALL/relative
        raw = read(path, row["sha256"]); need(len(raw) == row["bytes"], "CRASH_SDK_EXTENT")
        selected[logical] = dict(path=str(path), bytes=len(raw), sha256=row["sha256"])
    for logical, relative in EXTRA.items():
        row = request["additions"][logical]
        need(type(row) is dict and set(row) == {"bytes", "sha256"} and logical not in selected,
             "CRASH_NEW_SOURCE")
        path = SNAPSHOT/relative
        need(len(read(path, row["sha256"])) == row["bytes"], "CRASH_ADDITION_EXTENT")
        selected[logical] = dict(path=str(path), **row)
    prefixes = {PurePosixPath(logical).parts[1] for logical in selected}
    need(not any(name.split(".")[0] in prefixes for name in sys.modules), "CRASH_EARLY_IMPORT")
    sys.path[:0] = [str(INSTALL/"sdk/v5"), str(INSTALL/"sdk/portable")]
    for name in ("placement.reclaim", "placement.sessions", "placement.lifecycle"):
        __import__(name.split(".")[0])
        row = selected["v5/"+name.replace(".", "/")+".py"]
        load(name, row["path"], row["sha256"], row["bytes"])
    return selected


def rebind(selected):
    read(INSTALL/"V5-RELEASE.json", RELEASE, 8*MIB)
    paths = {Path(row["path"]) for row in selected.values()}
    prefixes = {PurePosixPath(logical).parts[1] for logical in selected}
    origins = {}
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] not in prefixes: continue
        origin = getattr(module, "__file__", None)
        if origin is None:
            namespaces = getattr(module, "__path__", ())
            need(namespaces and all(Path(p).is_relative_to(INSTALL/"sdk") for p in namespaces), "CRASH_NAMESPACE")
        else:
            need(ordinary(origin) in paths, "CRASH_PRODUCT_ORIGIN")
            origins[name] = str(Path(origin))
    for row in selected.values():
        need(len(read(row["path"], row["sha256"])) == row["bytes"], "CRASH_FINAL_EXTENT")
    return origins


def configurations(output):
    from placement.lifecycle import SCHEMA
    from placement import codec as P
    endpoint = lambda port: dict(host="127.0.0.1", port=port, tls=False, server_name=None)
    config = dict(schema=SCHEMA, epoch=sha(str(output).encode()),
        clock_model_id=sha(b"OWNER_PREMISE_UTC_AFTER_2020_CRASH_TEST"), max_sessions=1,
        registry_pages=256, owner_reserved_bytes=36*MIB, registry_reserved_bytes=2*MIB,
        cleanup_reserved_bytes=2*MIB, protected_roots=[str(INSTALL), str(PROJECT/"software"),
            str(PROJECT/"research"), str(output/"sources")], slots=[dict(reserved_bytes=16*MIB,
                max_cells=1, max_runs=1, read_endpoint=endpoint(33000+3*i),
                intake_endpoint=endpoint(33001+3*i), listen=[f"/ip4/127.0.0.1/tcp/{33002+3*i}"])
                for i in range(2)])
    # Deliberately reservation-only: no workspace/service startup, socket or
    # mathematical authority is constructed from these fixture dictionaries.
    generation = dict(workspace={}, service_limits={}, egress={},
        placement=dict(schema=P.CONFIG_SCHEMA, service_epoch=config["epoch"], namespace="11"*32,
            wire_profile_id="22"*32, admission_close_ms=CLOCK_LOWER-2000,
            retention_not_after_ms=CLOCK_LOWER-1000, max_grants=1, max_requests=1,
            max_cells=1, max_runs=1, ledger_pages=256, limits={key:1 for key in P.RESOURCES}),
        location=dict(schema="DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", role="index-provider",
            namespace="11"*32, egress={}, listen=config["slots"][0]["listen"], announce=[],
            bootstrap=[], endpoints=[config["slots"][0]["read_endpoint"]], limits={}))
    return config, generation


def worker(args, selected):
    from placement.lifecycle import ManagedGenerations
    from placement import sessions as S
    output = ordinary(args.output, directory=True)
    launch = json.loads(read(output/"worker-input.json", args.worker_input_sha))
    need(set(launch) == {"config", "generation", "profile_sha256"}, "CRASH_WORKER_INPUT")
    manager = ManagedGenerations.open(output/"managed", launch["config"], deadline=OUTER, calls=16, cpu_seconds=15)
    joined = manager.join_current_worker(launch["profile_sha256"])
    session = manager.status()["session"]
    record = manager.allocate(0, launch["generation"])
    handle = manager.reserve_run(record["generation"], outer_deadline=session["run_deadline_ns"]/1e9-0.001)
    # No graceful manager close: the OS closes the real lock and SQLite handle
    # on process death. The reservation is durably charged before this Popen.
    descendant = subprocess.Popen([sys.executable, "-I", "-S", "-B", str(Path(__file__).resolve()),
        "--idle", "--output", str(output)], cwd=PROJECT, stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
    ready = output/"descendant-ready.json"
    deadline = min(time.monotonic()+5, session["run_deadline_ns"]/1e9)
    while not ready.exists() and descendant.poll() is None and time.monotonic() < deadline:
        time.sleep(0.02)
    need(ready.exists() and descendant.poll() is None, "CRASH_DESCENDANT_NOT_LIVE")
    observed = json.loads(read(ready))
    need(observed["pid"] == descendant.pid and observed["parent_pid"] == os.getpid(), "CRASH_DESCENDANT_IDENTITY")
    record = manager.status()["slots"][0]
    need(record["runs"] == 1 and record["run_state"] == "RESERVED" and handle is not None,
         "CRASH_CHARGED_BEFORE_EFFECTS")
    save(output/"worker-before-crash.json", dict(joined=joined, session=session, record=record,
        worker=S._process_identity(), descendant=observed, deliberate_exit_code=23,
        orderly_close_attempted=False, origins=rebind(selected)))
    os._exit(23)


def scenario(args, selected, report):
    from placement.lifecycle import ManagedGenerations
    from placement import sessions as S
    output = ordinary(args.output, directory=True)
    manifest = json.loads(read(BASE/"RELEASE-MANIFEST.json", MANIFEST, 8*MIB))
    modules = {}
    for name, relative in (("_crash_operator", "operator/commons.py"), ("domains", "receiver/helpers/domains.py"),
                           ("_crash_job", "receiver/helpers/run_stage.py")):
        row = manifest["files"][relative]
        modules[name] = load(name, BASE/relative, row["sha256"], row["bytes"])
    config, generation = configurations(output)
    source_sha = sha(read(Path(__file__).resolve()))
    profile_sha = sha(encode(dict(adapter_sha256=source_sha, sources=selected,
        operator_manifest_sha256=MANIFEST, worker="FIXED_CRASH_WITH_ONE_IDLE_DESCENDANT_V1")))
    save(output/"worker-input.json", dict(config=config, generation=generation, profile_sha256=profile_sha))
    worker_input_sha = sha(read(output/"worker-input.json"))
    manager = ManagedGenerations.open(output/"managed", config, create=True, deadline=OUTER, calls=16, cpu_seconds=30)
    report.update(stage="supervise-real-crash", manager_config=config, profile_sha256=profile_sha,
                  selected_sources=selected, deletion_performed=False)
    try:
        report["supervisor"] = S.supervise(manager, profile=dict(sha256=profile_sha, ownership=S.OWNERSHIP),
            argv=[sys.executable, "-I", "-S", "-B", str(Path(__file__).resolve()), "--worker",
                  "--output", str(output), "--input", args.input, "--input-sha", args.input_sha,
                  "--worker-input-sha", worker_input_sha], cwd=PROJECT, evidence=output/"crashed-worker",
            limits=dict(cpu_seconds=10, wall_seconds=30, memory_mib=128, active_processes=2,
                        stdout_bytes=65536, stderr_bytes=65536),
            operator_module=modules["_crash_operator"], job_module=modules["_crash_job"], cleanup_seconds=25)
    finally:
        if not manager._closed: manager.close()
    observed = report["supervisor"]
    need(observed["status"] == "COMMAND_FAILED" and observed["child_exit_code"] == 23
         and observed["direct_child_reaped"] and observed["termination_requested"]
         and observed["job_closed"] and not observed["cleanup_errors"]
         and observed["final_job"]["active_processes"] == 0
         and observed["final_job"]["total_processes"] == 2, "CRASH_ACTUAL_TREE_CLOSURE")
    need(observed["session_recovery"] == dict(status="QUIESCED", unclean_slots=[0],
         orderly_close_claim=False, mathematical_acceptance=False), "CRASH_ACTUAL_RECOVERY")
    before = json.loads(read(output/"worker-before-crash.json"))
    report["before_crash"] = before
    manager = ManagedGenerations.open(output/"managed", config, deadline=OUTER, calls=16, cpu_seconds=10)
    try:
        state = manager.status(); current = state["slots"][0]
        expected = deepcopy(before["record"])
        expected["run_state"] = "QUIESCED_UNCLEAN"
        expected["quiescence"] = dict(schema="DMKN_V5_EXACT_JOB_QUIESCENCE_V1",
            session_sha256=expected["session"]["session_sha256"], nonce=before["session"]["nonce"],
            worker=before["worker"])
        need(current == expected and state["slots"][1] is None and state["session"]["state"] == "QUIESCED",
             "CRASH_EXACT_PRESERVED_CHARGE_AND_BINDING")
        report["after_reopen"] = state
        try: manager.reserve_run(current["generation"], outer_deadline=OUTER-1)
        except ValueError as error:
            need(str(error) == "SUPERVISED_CURRENT_WORKER_JOIN_REQUIRED", "CRASH_RESTART_REFUSAL_KIND")
            report["restart_refusal"] = str(error)
        else: raise ValueError("CRASH_UNCLEAN_RESTART_ALLOWED")
        clock = manager.adopt_clock(lower_utc_ms=CLOCK_LOWER, valid_for_ms=60000, rate_error_ppm=10000,
                                    model_id=config["clock_model_id"])
        manager.begin_retire(current["generation"], clock)
        report["retired"] = manager.commit_retired(current["generation"], clock)
        need(report["retired"]["phase"] == "RETIRED" and report["retired"]["run_state"] == "QUIESCED_UNCLEAN"
             and report["retired"]["runs"] == 1 and "closure_sha256" not in report["retired"], "CRASH_RETIRED_NOT_CLOSED")
        need(manager.generation_path(current).is_dir(), "CRASH_NO_DELETION")
    finally:
        manager.close()
    report.update(stage="complete", origins=rebind(selected), mathematical_acceptance=False,
        real_service_tested=False, supervisor_loss_recovery=False, physical_envelope_adopted=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True); parser.add_argument("--input"); parser.add_argument("--input-sha")
    parser.add_argument("--worker-input-sha"); parser.add_argument("--worker", action="store_true")
    parser.add_argument("--idle", action="store_true")
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "CRASH_EXACT_INVOCATION")
    output = ordinary(args.output, directory=True)
    need(output.is_relative_to(PROJECT/"experiments/v5-local-checks") and output != PROJECT/"experiments/v5-local-checks",
         "CRASH_FRESH_TEST_SCOPE")
    if args.idle:
        need(not args.worker and args.input is None, "CRASH_IDLE_MODE")
        save(output/"descendant-ready.json", dict(pid=os.getpid(), parent_pid=os.getppid()))
        time.sleep(20)
        return 24
    request = json.loads(read(args.input, args.input_sha))
    selected = adopt(request)
    if args.worker: return worker(args, selected)
    report = dict(schema="DMKN_SUPERVISED_CRASH_RESULT_V1", status="FAIL", stage="adopted",
                  authority="LOCAL_PROCESS_RECOVERY_EVIDENCE_NOT_MATHEMATICAL_ACCEPTANCE")
    try:
        scenario(args, selected, report)
        need(time.monotonic() < OUTER, "CRASH_ORIGINAL_DEADLINE")
        report["status"] = "PASS_REAL_OWNER_CRASH_RECOVERY"
    except BaseException as error:
        report.update(error_type=type(error).__name__, error_code=str(error) if
            re.fullmatch(r"[A-Z][A-Z0-9_]{0,127}", str(error)) else "CRASH_OPERATION_FAILED")
    finally:
        report["wall_seconds"] = time.monotonic()-STARTED
        save(output/"crash-result.json", report)
    print(json.dumps(dict(status=report["status"], stage=report["stage"])), flush=True)
    return 0 if report["status"] == "PASS_REAL_OWNER_CRASH_RECOVERY" else 1


if __name__ == "__main__":
    raise SystemExit(main())

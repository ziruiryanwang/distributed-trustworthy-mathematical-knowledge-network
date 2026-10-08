"""One pinned native capacity-renewal allocation; root-only reviewed launch.

The qualified test-only outer-sixteen profile contains the worker and all descendants.
This coordinator never imports another test driver or performs product work.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import sys
import time

SOURCE = Path(__file__).absolute().parents[1]
PRODUCT = SOURCE
RUN = SOURCE / "qualification/capacity-native-01"
DATA = SOURCE.parent / "product-local/capacity-native-01"
WORKER = SOURCE / "tests/capacity_native_worker.py"
MIB = 1048576
LIMITS = {"wall_seconds": 450, "cpu_seconds": 450, "memory_mib": 6144,
          "active_processes": 16, "stdout_bytes": 65536,
          "stderr_bytes": 65536, "event_bytes": 65536}
RETAINED = {"bytes": 1073741824, "files": 16384, "entries": 32768}
REQUEST = b'{"op":"test-capacity-native"}\n'
SUCCESS = "PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT"
SCOPE = "fixed native capacity continuation; not indefinite operation or useful-growth qualification"
COUNTS = {"calls": 17, "ordinary_calls": 8, "administrative_calls": 7,
          "ordinary_requests": 4, "owner_grants": 2, "native_stages": 2,
          "pipeline_children": 6, "support_build_stages": 1,
          "support_compilations": 2, "charged_bytes": 301989888}
RESULT_BOUND = 65536


def require(value, code):
    if not value:
        raise RuntimeError(code)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")


def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result

    def bad(_):
        raise RuntimeError("NONFINITE_JSON")

    def finite(token):
        value = float(token)
        require(math.isfinite(value), "NONFINITE_JSON")
        return value

    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_constant=bad, parse_float=finite)


def checked(path):
    path = Path(path)
    require(path.is_absolute(), "ABSOLUTE_PATH")
    # Inspect unresolved ancestors first: resolving a junction first hides it.
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        require(not stat.S_ISLNK(info.st_mode)
                and not getattr(info, "st_file_attributes", 0) & 0x400, "REPARSE_POINT")
    return path.resolve(strict=True)


def read(path, bound=16 * MIB):
    path = checked(path)
    require(stat.S_ISREG(path.stat().st_mode) and path.stat().st_size <= bound, "READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(bound + 1)
    require(len(raw) <= bound, "READ_BOUND")
    return raw


def pin(path):
    path = checked(path)
    raw = read(path)
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def save_raw(path, raw, bound=16 * MIB):
    require(type(raw) is bytes and len(raw) <= bound, "SAVE_BOUND")
    checked(path.parent)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def product_pins():
    paths = [PRODUCT / name for name in ("API.md", "manage.py", "build.py", "assets-lock.json")]
    for path in checked(PRODUCT / "py").iterdir():
        if path.suffix == ".py":
            paths.append(path)
    pending, entries = [checked(PRODUCT / name) for name in ("native", "assets")], 0
    while pending:
        for path in pending.pop().iterdir():
            entries += 1
            require(entries <= 4096, "PRODUCT_ENTRY_BOUND")
            path = checked(path)
            if path.is_dir():
                pending.append(path)
            else:
                require(stat.S_ISREG(path.stat().st_mode), "PRODUCT_REGULAR_FILE")
                paths.append(path)
    require(len(paths) == 101, "EXACT_PRODUCT_COUNT")
    paths.sort(key=lambda path: path.relative_to(PRODUCT).as_posix())
    return [dict(relative=path.relative_to(PRODUCT).as_posix(), **pin(path)) for path in paths]


def census():
    """Post-quiescence endpoint only; no hard transient filesystem quota."""
    rows, entries, total = [], 0, 0
    pending = [("data", DATA, checked(DATA)), ("evidence", RUN, checked(RUN))]
    while pending:
        label, root, directory = pending.pop()
        for path in directory.iterdir():
            entries += 1
            require(entries <= RETAINED["entries"], "RETAINED_ENTRY_LIMIT")
            path = checked(path)
            require(path.is_relative_to(root), "CENSUS_PATH_DOMAIN")
            info = path.stat()
            if stat.S_ISDIR(info.st_mode):
                pending.append((label, root, path))
                continue
            require(stat.S_ISREG(info.st_mode), "RETAINED_REGULAR_FILE")
            total += info.st_size
            require(len(rows) < RETAINED["files"] and total <= RETAINED["bytes"],
                    "RETAINED_FILE_BYTE_LIMIT")
            digest, observed = hashlib.sha256(), 0
            with path.open("rb") as stream:
                while True:
                    chunk = stream.read(MIB)
                    if not chunk:
                        break
                    observed += len(chunk)
                    require(observed <= info.st_size, "QUIESCENT_FILE_GREW")
                    digest.update(chunk)
            require(observed == info.st_size and path.stat().st_size == info.st_size,
                    "QUIESCENT_FILE_SIZE_CHANGED")
            rows.append({"root": label, "relative": path.relative_to(root).as_posix(),
                         "bytes": observed, "sha256": digest.hexdigest()})
    return {"files": sorted(rows, key=lambda row: (row["root"], row["relative"])),
            "entries": entries, "bytes": total, "bounds": RETAINED,
            "endpoint": "worker tree quiescent; before census.json and result.json",
            "remaining_records": {"files": 2, "entries": 2, "result_byte_bound": RESULT_BOUND}}


def quiescent(receipt):
    return (type(receipt) is dict and receipt.get("direct_child_reaped") is True
            and receipt.get("final_active_zero") is True and receipt.get("job_closed") is True
            and not receipt.get("cleanup_errors") and type(receipt.get("final_job")) is dict
            and type(receipt["final_job"].get("active_processes")) is int
            and receipt["final_job"]["active_processes"] == 0)


def nonnegative_number(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", required=True, type=Path)
    args = parser.parse_args()
    require(os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_user_site and sys.flags.no_site, "WINDOWS_STARTUP_PROFILE")
    started, coordinator_cpu = time.monotonic(), time.process_time()
    launch_path = checked(args.launch)
    launch_raw = read(launch_path, 131072)
    launch = strict(launch_raw)
    require(type(launch) is dict and set(launch) == {"schema", "pins", "product", "limits", "retained"}
            and type(launch["schema"]) is int and launch["schema"] == 1
            and encode(launch["limits"]) == encode(LIMITS)
            and encode(launch["retained"]) == encode(RETAINED), "EXACT_LAUNCH_FIELDS")
    paths = [Path(sys.executable), Path(__file__).absolute(), WORKER,
             SOURCE / "tests/scenario_profile.py", PRODUCT / "py/run_stage.py",
             PRODUCT / "py/supervise.py", PRODUCT / "py/domains.py",
             SOURCE / "runtime/lean-4.34.0-windows/bin/lean.exe"]
    pins = [pin(path) for path in paths]
    require(encode(launch["pins"]) == encode(pins), "EXACT_ORDERED_SOURCE_PINS")
    require(encode(launch["product"]) == encode(product_pins()), "EXACT_PRODUCT_PINS")
    launch_pin = pin(launch_path)
    require(launch_pin["bytes"] == len(launch_raw)
            and launch_pin["sha256"] == hashlib.sha256(launch_raw).hexdigest(), "LAUNCH_CHANGED")
    for root in (RUN, DATA):
        checked(root.parent)
        require(not os.path.lexists(root), "FRESH_FIXED_ROOT_REQUIRED")
    require(not any(name in sys.modules for name in ("run_stage", "supervise", "domains", "scenario_profile")),
            "PRODUCT_MODULE_ALREADY_IMPORTED")
    RUN.mkdir(exist_ok=False)
    result = {"schema": 1, "status": "FAILED", "scope": SCOPE, "launch": launch_pin,
              "worker_cpu_complete": False, "total_cpu_complete": False,
              "cpu_scope": "outer Job includes worker, public CLIs and nested native children once",
              "unmetered_cpu": "launcher/interpreter startup and final coordinator report persistence",
              "containment": "worker Windows Job; trusted coordinator outside Job",
              "retry": "none; fixed fresh roots and immutable records"}
    receipt, response, invocation_started, supervise = None, None, False, None
    cases = RUN / "cases"
    try:
        DATA.mkdir(exist_ok=False)
        cases.mkdir()
        sources = RUN / "sources"
        sources.mkdir()
        for path, expected in zip(paths[1:-1], pins[1:-1]):
            raw = read(path)
            require(len(raw) == expected["bytes"]
                    and hashlib.sha256(raw).hexdigest() == expected["sha256"], "SOURCE_SNAPSHOT_CHANGED")
            save_raw(sources / path.name, raw)
        save_raw(RUN / "launch.json", launch_raw, 131072)
        result["source_snapshots"] = [pin(sources / path.name) for path in paths[1:-1]]
        sys.path.insert(0, str(PRODUCT / "py"))
        import run_stage
        import supervise
        import domains
        import scenario_profile
        for module, origin in ((run_stage, PRODUCT / "py/run_stage.py"),
                               (supervise, PRODUCT / "py/supervise.py"),
                               (domains, PRODUCT / "py/domains.py"),
                               (scenario_profile, SOURCE / "tests/scenario_profile.py")):
            require(checked(module.__file__) == checked(origin), "MODULE_ORIGIN")
        limits = dict(LIMITS, pins=[*pins, launch_pin])
        transport = scenario_profile.Transport(sys.executable, WORKER, launch_path, DATA, cases, scenario_profile, limits)
        invocation_started = True
        response = transport("capacity-native", REQUEST)
    except BaseException as error:
        result["error"] = {"type": type(error).__name__, "detail": str(error)[:2048]}
        if supervise is not None and isinstance(error, supervise.SupervisorFailure):
            receipt = error.record
    # Preserve actual CPU and cleanup before any success/count predicates.
    try:
        receipt_path = cases / "capacity-native/supervisor.json"
        if receipt is None and receipt_path.exists():
            receipt = strict(read(receipt_path, MIB))
        if receipt is not None:
            result["observed_job_cpu_seconds"] = receipt.get("final_job", {}).get("cpu_seconds")
            result["worker_cpu_complete"] = (quiescent(receipt)
                and nonnegative_number(result["observed_job_cpu_seconds"]))
            result["cleanup_observation"] = {key: receipt.get(key) for key in
                ("direct_child_reaped", "final_active_zero", "job_closed", "cleanup_errors")}
            observed = encode(receipt)
            save_raw(RUN / "supervisor-observation.json", observed, MIB)
            result["supervisor_observation"] = pin(RUN / "supervisor-observation.json")
            if receipt_path.exists():
                result["supervisor_file"] = pin(receipt_path)
        else:
            result["supervisor_observation"] = "unavailable; no zero-cost claim"
        if response is not None:
            outcome = strict(response["stdout"])
            result["worker_outcome"] = outcome
            require(type(outcome) is dict and set(outcome) == set(COUNTS) | {"status", "scope", "elapsed_seconds"}
                    and outcome["status"] == SUCCESS and outcome["scope"] == SCOPE
                    and encode({key: outcome[key] for key in COUNTS}) == encode(COUNTS)
                    and nonnegative_number(outcome["elapsed_seconds"]), "EXACT_WORKER_SUCCESS")
            require(response["returncode"] == 0 and response["stderr"] == b""
                    and encode(outcome) == response["stdout"], "EXACT_WORKER_OUTPUT")
            event = response["event"]
            require(type(event) is dict and set(event) == {"request_sha256", "response_sha256", "scope"}
                    and event["request_sha256"] == hashlib.sha256(REQUEST).hexdigest()
                    and event["response_sha256"] == hashlib.sha256(response["stdout"]).hexdigest()
                    and event["scope"] == SCOPE, "EXACT_WORKER_EVENT")
            require(quiescent(receipt) and receipt.get("status") == "TRANSPORT_COMPLETE"
                    and receipt.get("returncode") == 0 and receipt.get("job_created_before_process") is True
                    and receipt.get("attach_resume_returned") is True
                    and not any(receipt.get(key) for key in
                                ("cleanup_errors", "output_record_error", "evidence_persistence_error", "failure"))
                    and encode(receipt.get("pins")) == encode([*pins, launch_pin]), "CLEAN_SUPERVISOR_SUCCESS")
            final = receipt["final_job"]
            require(receipt["limits"]["active_processes"] == 16
                    and receipt["sampled_peak_active_processes"] <= 16
                    and nonnegative_number(final.get("cpu_seconds")) and final["cpu_seconds"] <= 450
                    and final.get("terminated_processes") == 0 and final.get("total_processes", 0) >= 1
                    and final.get("peak_job_private_commit_bytes", 6144 * MIB + 1) <= 6144 * MIB
                    and nonnegative_number(receipt.get("wall_seconds")) and receipt["wall_seconds"] <= 450,
                    "ACTUAL_OUTER_LIMITS")
            require("error" not in result, "EARLIER_COORDINATOR_FAILURE")
            result["status"] = SUCCESS
    except BaseException as error:
        result["status"] = "FAILED"
        result["observation_error"] = {"type": type(error).__name__, "detail": str(error)[:2048]}
    try:
        result["worker_tree_quiescent"] = quiescent(receipt) or not invocation_started
        require(result["worker_tree_quiescent"], "CENSUS_REQUIRES_WORKER_QUIESCENCE")
        retained = census()
        census_raw = encode(retained)
        require(retained["bytes"] + len(census_raw) + RESULT_BOUND <= RETAINED["bytes"]
                and len(retained["files"]) + 2 <= RETAINED["files"]
                and retained["entries"] + 2 <= RETAINED["entries"], "FINAL_RETAINED_LIMIT")
        save_raw(RUN / "census.json", census_raw)
        result["census"] = pin(RUN / "census.json")
        result["retained_bytes_before_final_records"] = retained["bytes"]
        result["retained_files_before_final_records"] = len(retained["files"])
        result["final_result_byte_reserve"] = RESULT_BOUND
    except BaseException as error:
        result["status"] = "FAILED"
        result["census_error"] = {"type": type(error).__name__, "detail": str(error)[:2048]}
    result["elapsed_seconds_before_final_result"] = time.monotonic() - started
    result["observed_coordinator_cpu_seconds_before_final_result"] = time.process_time() - coordinator_cpu
    save_raw(RUN / "result.json", encode(result), RESULT_BOUND)
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0 if result["status"] == SUCCESS else 1


if __name__ == "__main__":
    raise SystemExit(main())


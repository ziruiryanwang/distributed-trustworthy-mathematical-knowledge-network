"""One author-reviewed two-case native-free allocation; root-only execution."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
from types import SimpleNamespace


def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def read(path, bound=65536):
    with Path(path).open("rb") as stream:
        raw = stream.read(bound + 1)
    require(len(raw) <= bound, "READ_BOUND")
    return raw


def quiescent(record):
    return (record.get("direct_child_reaped") is True and record.get("final_active_zero") is True
            and record.get("job_closed") is True and not record.get("cleanup_errors")
            and (record.get("final_job") or {}).get("active_processes") == 0)


def membership(observation, required, python, limit):
    require(observation["requested_active_processes"] == limit
            and observation["active_process_limit_readback"] == limit, "LOCAL_GRANT_READBACK")
    members = observation["members"]
    pids = members["pids"]
    require(members["query_ok"] is True and members["number_assigned"] == members["number_listed"]
            == len(pids) <= 16 and all(type(pid) is int and pid > 0 for pid in pids)
            and len(set(pids)) == len(pids) and set(required) <= set(pids), "BOUNDED_PID_MEMBERSHIP")
    for pid in required:
        rows = [item for item in members["images"] if item["pid"] == pid]
        require(len(rows) == 1 and not rows[0].get("close_handle_error")
                and Path(rows[0].get("image", "")).resolve() == python, "REQUIRED_PROCESS_IMAGE")


def validate_shape(helper, mode, receipt, response, launch_path):
    directory = helper.RUN / "cases" / ("shape-" + mode)
    load = lambda name: json.loads(helper.read(directory / name))
    raw = helper.encode({"mode": mode})
    binding = {"mode": mode, "request_sha256": hashlib.sha256(raw).hexdigest(), "native_stages": 0}
    barriers = {role: load("actual-" + role + ".json") for role in helper.ROLES}
    pids = {role: item["pid"] for role, item in barriers.items()}
    require(all(type(pid) is int and pid > 0 for pid in pids.values())
            and len(set(pids.values())) == 5 and pids["worker"] == receipt["pid"], "FIVE_ACTUAL_PIDS")
    args = SimpleNamespace(config=launch_path, state=helper.RUN / "reserved-state",
                           request=directory / "request.json", event=directory / "event.json")
    for index, role in enumerate(helper.ROLES):
        parent = 0 if index == 0 else pids[helper.ROLES[index - 1]]
        require(barriers[role] == dict(binding, role=role, pid=pids[role], parent=parent), "EXACT_ROLE_BARRIER")
        if index:
            require(load("launched-" + role + ".json") == barriers[role], "LAUNCHED_ACTUAL_PID")
            require(load("command-" + role + ".json") == {
                "argv": helper.child_command(args, role, parent), "cwd": str(helper.CODE[1].parent),
                "shell": False, "creationflags": 0x08000000 | (0x4 if role in ("node", "leaf") else 0)},
                "EXACT_CHILD_COMMAND")
    shape, leaf = load("shape.json"), load("leaf-job.json")
    require(all(shape[key] == value and leaf[key] == value for key, value in binding.items())
            and shape["wrapper_pid"] == pids["wrapper"]
            and shape["null_handle_queries_wrapper_containing_job"] is True, "SHAPE_BINDING")
    python = Path(sys.executable).resolve()
    membership(shape["outer"], list(pids.values()), python, 16)
    membership(shape["public"], [pids[key] for key in ("node", "runner", "leaf")], python, 8)
    membership(leaf["observation"], [pids["leaf"]], python, 1)
    require(all(shape[kind][phase]["active_processes"] <= bound
                for kind, bound in (("outer", 16), ("public", 8)) for phase in ("before", "after")),
            "OBSERVED_AGGREGATE_PROCESS_BOUNDS")
    if mode == "normal":
        require(response is not None and response["returncode"] == 0 and response["stderr"] == b""
                and response["stdout"] == helper.encode({"status": "NATIVE_FREE_SHAPE_COMPLETE", "native_stages": 0})
                and receipt["status"] == "TRANSPORT_COMPLETE", "NORMAL_OUTCOME")
        require(response["event"] == dict(binding, response_sha256=hashlib.sha256(response["stdout"]).hexdigest(),
                                           shape=helper.pin(directory / "shape.json")), "EXACT_NORMAL_EVENT")
        for index, role in enumerate(helper.ROLES):
            done = load("complete-" + role + ".json")
            require(all(done[key] == value for key, value in binding.items())
                    and done["role"] == role and done["pid"] == pids[role], "COMPLETION_BINDING")
            if role != "leaf":
                require(done["direct_child_reaped"] is True and done["returncode"] == 0
                        and done["child_pid"] == pids[helper.ROLES[index + 1]], "NORMAL_CHILD_REAP")
            if role in ("wrapper", "runner"):
                require(done["job_closed"] is True and done["final_job"]["active_processes"] == 0
                        and done["final_job"]["terminated_processes"] == 0, "NORMAL_LOCAL_CLEANUP")
    else:
        require(response is None and receipt["status"] == "TRANSPORT_FAILED"
                and receipt.get("failure", {}).get("detail") == "PUBLIC_WALL_LIMIT"
                and receipt.get("job_termination_requested") is True
                and not (directory / "event.json").exists()
                and not (directory / "release.json").exists(), "INTENDED_TIMEOUT")
    return {"barriers": {role: helper.pin(directory / ("actual-" + role + ".json")) for role in helper.ROLES},
            "shape": helper.pin(directory / "shape.json"), "leaf_job": helper.pin(directory / "leaf-job.json")}


def census(helper):
    rows, entries, total, pending = [], 0, 0, [helper.RUN]
    while pending:
        for path in pending.pop().iterdir():
            entries += 1
            require(entries <= helper.RETAINED["entries"] and not path.is_symlink()
                    and not getattr(path.lstat(), "st_file_attributes", 0) & 0x400, "CENSUS_ENTRY_BOUND")
            if path.is_dir():
                pending.append(path)
            else:
                require(path.is_file(), "CENSUS_REGULAR_FILE")
                total += path.stat().st_size
                require(total <= helper.RETAINED["bytes"] and len(rows) < helper.RETAINED["files"],
                        "CENSUS_FILE_BYTE_BOUND")
                rows.append(helper.pin(path))
    return {"files": sorted(rows, key=lambda row: row["path"]), "entries": entries, "bytes": total,
            "endpoint": "after all started trees quiesce; excludes census.json and result.json"}


def main():
    started, coordinator_cpu = time.monotonic(), time.process_time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", type=Path, required=True)
    args = parser.parse_args()
    require(os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_site and sys.flags.no_user_site, "WINDOWS_STARTUP_PROFILE")
    require(args.launch.is_absolute(), "ABSOLUTE_LAUNCH")
    launch_raw, source = read(args.launch), Path(__file__).resolve().parents[1]
    launch = json.loads(launch_raw)
    # Authenticate the helper before importing any task/product module.
    helper_path = source / "tests/scenario_shape_worker.py"
    raw_helper = read(helper_path, 16 * 1048576)
    require(launch["pins"][2] == {"path": str(helper_path), "bytes": len(raw_helper),
            "sha256": hashlib.sha256(raw_helper).hexdigest()}, "PREIMPORT_HELPER_PIN")
    import scenario_shape_worker as helper
    require(Path(helper.__file__).resolve() == helper_path, "HELPER_ORIGIN")
    runtime = helper.load_runtime(launch)
    launch_pin = helper.pin(args.launch)
    require(launch_pin["sha256"] == hashlib.sha256(launch_raw).hexdigest(), "LAUNCH_CHANGED")
    require(not os.path.lexists(helper.RUN), "FRESH_RUN_REQUIRED")
    helper.RUN.mkdir()
    result = {"status": "FAILED", "calls": [], "native_stages": 0,
              "scope": "finite native-free five-layer normal/timeout control; no mathematical acceptance",
              "source_launch": launch_pin, "total_cpu_complete": False,
              "unmetered_cpu": "interpreter/launcher startup and final coordinator persistence",
              "job_cpu_scope": "each disjoint outer Job once; no sum of nested observations"}
    all_quiescent = True
    try:
        (helper.RUN / "cases").mkdir()
        (helper.RUN / "sources").mkdir()
        for path, expected in zip(helper.CODE, launch["pins"][1:]):
            raw = helper.read(path, 16 * 1048576)
            require(helper.pin(path) == expected and hashlib.sha256(raw).hexdigest() == expected["sha256"], "SOURCE_SNAPSHOT_PIN")
            with (helper.RUN / "sources" / path.name).open("xb") as stream:
                stream.write(raw)
        helper.save(helper.RUN / "launch.json", launch)
        limits = dict(helper.LIMITS, pins=[*launch["pins"], launch_pin])
        transport = runtime.profile.Transport(sys.executable, helper.CODE[1], args.launch,
            helper.RUN / "reserved-state", helper.RUN / "cases", runtime.profile, limits)
        for mode in ("normal", "timeout"):
            require(time.monotonic() - started < helper.ALLOCATION["wall_seconds"], "ALLOCATION_EXHAUSTED")
            response, receipt = None, None
            all_quiescent = False
            try:
                response = transport("shape-" + mode, helper.encode({"mode": mode}))
            except runtime.supervisor.SupervisorFailure as error:
                receipt = error.record
            if receipt is None:
                receipt = json.loads(helper.read(helper.RUN / "cases" / ("shape-" + mode) / "supervisor.json"))
            # Cost and cleanup survive every subsequent qualification failure.
            all_quiescent = quiescent(receipt)
            observation = {"mode": mode, "outer_job": receipt.get("final_job"),
                "wall_seconds": receipt.get("wall_seconds"), "quiescent": all_quiescent,
                "cleanup": {key: receipt.get(key) for key in
                            ("direct_child_reaped", "final_active_zero", "job_closed", "cleanup_errors")}}
            result["calls"].append(observation)
            helper.save(helper.RUN / (mode + "-observation.json"), receipt)
            observation["receipt"] = helper.pin(helper.RUN / (mode + "-observation.json"))
            require(all_quiescent and receipt.get("pins") == limits["pins"]
                    and not receipt.get("output_record_error") and not receipt.get("evidence_persistence_error"),
                    "OUTER_CLEANUP_AND_PINS")
            require(receipt["limits"]["active_processes"] == 16
                    and receipt["sampled_peak_active_processes"] <= 16
                    and receipt["final_job"]["cpu_seconds"] <= 15
                    and receipt["final_job"]["peak_job_private_commit_bytes"] <= 512 * 1048576,
                    "ACTUAL_CASE_BOUNDS")
            observation["evidence"] = validate_shape(helper, mode, receipt, response, args.launch)
        result["status"] = "PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT"
    except BaseException as error:
        result["error"] = {"type": type(error).__name__, "detail": str(error)[:2048]}
    try:
        require(all_quiescent, "CENSUS_REQUIRES_ALL_TREES_QUIESCENT")
        retained = census(helper)
        census_raw = helper.encode(retained)
        require(retained["bytes"] + len(census_raw) + 65536 <= helper.RETAINED["bytes"]
                and len(retained["files"]) + 2 <= helper.RETAINED["files"]
                and retained["entries"] + 2 <= helper.RETAINED["entries"], "FINAL_RETAINED_BOUND")
        helper.save(helper.RUN / "census.json", retained)
        result["census"] = helper.pin(helper.RUN / "census.json")
    except BaseException as error:
        result.update(status="FAILED", census_error=str(error)[:2048])
    costs = [(row.get("outer_job") or {}).get("cpu_seconds") for row in result["calls"]]
    result["worker_cpu_complete"] = all_quiescent and all(type(value) in (int, float)
        and math.isfinite(value) and value >= 0 for value in costs)
    result["observed_job_cpu_seconds"] = sum(costs) if result["worker_cpu_complete"] else None
    result["elapsed_seconds_before_final_result"] = time.monotonic() - started
    result["coordinator_cpu_seconds_before_final_result"] = time.process_time() - coordinator_cpu
    if (result["elapsed_seconds_before_final_result"] > helper.ALLOCATION["wall_seconds"]
            or result["observed_job_cpu_seconds"] is None
            or result["observed_job_cpu_seconds"] > helper.ALLOCATION["job_cpu_seconds"]):
        result.update(status="FAILED", allocation_error="ACTUAL_AGGREGATE_BOUND")
    helper.save(helper.RUN / "result.json", result)
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0 if result["status"] == "PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT" else 1


if __name__ == "__main__":
    raise SystemExit(main())

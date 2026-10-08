"""Once-only two-installation PREPARE. No services, authors or contributions.

Root alone launches after review with -B -E -s -S and a pinned launch record.
Only standard-library imports; product commands run as separate public CLIs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

SOURCE = Path(__file__).resolve().parents[1]
PROJECT = SOURCE.parent
RUN = SOURCE / "qualification" / "peer-01"
DATA = PROJECT / "product-local" / "peer-01"
RUNTIME = SOURCE / "runtime" / "lean-4.34.0-windows"
FLAGS = ["-B", "-E", "-s", "-S"]
MIB = 1048576
LIMITS = {"command_seconds": 500, "active_wall_seconds": 1800,
          "observed_cpu_seconds": 1800, "retained_bytes": 1024 * MIB}


def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def parse(raw):
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
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=bad, parse_float=finite)


def safe(path, directory=False):
    path = Path(path).absolute()
    for ancestor in (path, *path.parents):
        stat = ancestor.lstat()
        require(not ancestor.is_symlink() and not (getattr(stat, "st_file_attributes", 0) & 0x400), "REPARSE_POINT")
    require(path.is_dir() if directory else path.is_file(), "PATH_KIND")
    return path.resolve(strict=True)


def read(path, maximum=2 * MIB):
    path = safe(path)
    require(path.stat().st_size <= maximum, "READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    require(len(raw) <= maximum, "READ_BOUND")
    return raw


def pin(path, maximum=16 * MIB):
    path = safe(path)
    raw = read(path, maximum)
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def checked(record, maximum=16 * MIB):
    require(type(record) is dict and set(record) == {"path", "bytes", "sha256"}, "PIN_FIELDS")
    require(type(record["path"]) is str and Path(record["path"]).is_absolute(), "PIN_ABSOLUTE_PATH")
    require(type(record["bytes"]) is int and 0 < record["bytes"] <= maximum, "PIN_BYTES")
    require(type(record["sha256"]) is str and len(record["sha256"]) == 64
            and all(character in "0123456789abcdefABCDEF" for character in record["sha256"]), "PIN_SHA256")
    actual = pin(record["path"], maximum)
    require(actual["bytes"] == record["bytes"] and actual["sha256"] == record["sha256"].lower(), "PIN_CHANGED")
    return actual


def save_raw(path, raw):
    require(len(raw) <= 16 * MIB, "REPORT_BOUND")
    with Path(path).open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    return pin(path)


def save(path, value):
    return save_raw(path, encode(value))


def census(root, budget, hashes=False):
    root = safe(root, directory=True)
    rows, stack, count, total = [], [root], 0, 0
    while stack:
        budget()
        directory = stack.pop()
        with os.scandir(directory) as entries:
            for entry in entries:
                count += 1
                require(count <= 32768, "CENSUS_ENTRY_BOUND")
                path = Path(entry.path)
                stat = path.lstat()
                require(not path.is_symlink() and not (getattr(stat, "st_file_attributes", 0) & 0x400), "REPARSE_POINT")
                require(len(path.relative_to(root).parts) <= 32, "CENSUS_DEPTH")
                if path.is_dir():
                    stack.append(path)
                    continue
                require(path.is_file(), "CENSUS_SPECIAL_FILE")
                total += stat.st_size
                require(total <= LIMITS["retained_bytes"], "RETAINED_BYTES")
                row = {"path": path.relative_to(root).as_posix(), "bytes": stat.st_size}
                if hashes:
                    sha, consumed = hashlib.sha256(), 0
                    with path.open("rb") as stream:
                        while True:
                            raw = stream.read(MIB)
                            if not raw:
                                break
                            consumed += len(raw)
                            require(consumed <= stat.st_size, "FILE_GREW")
                            sha.update(raw)
                            budget()
                    require(consumed == stat.st_size, "FILE_CHANGED")
                    row["sha256"] = sha.hexdigest()
                rows.append(row)
    return {"files": len(rows), "entries": count, "bytes": total,
            "manifest": sorted(rows, key=lambda row: row["path"])}


def product_sources(budget):
    files = [SOURCE / name for name in ("API.md", "manage.py", "build.py", "assets-lock.json")]
    py = safe(SOURCE / "py", directory=True)
    files.extend(sorted(py.glob("*.py")))
    for name in ("native", "assets"):
        root = SOURCE / name
        observed = census(root, budget)
        files.extend(root / row["path"] for row in observed["manifest"])
    require(1 <= len(files) <= 512 and len(set(files)) == len(files), "SOURCE_COUNT")
    return sorted((safe(path) for path in files), key=lambda path: path.relative_to(SOURCE).as_posix())


def ports_preflight(ports):
    held = []
    try:
        for name in ("alpha", "beta"):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            held.append(sock)
            if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            sock.bind(("127.0.0.1", ports[name]))
        return {"ports": ports, "both_simultaneously_bound": True,
                "meaning": "preflight only; sockets closed, no future reservation or service"}
    finally:
        for sock in held:
            sock.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", required=True, type=Path)
    args = parser.parse_args()
    require(args.launch.is_absolute(), "ABSOLUTE_LAUNCH_REQUIRED")
    require(sys.dont_write_bytecode and sys.flags.ignore_environment and sys.flags.no_site
            and sys.flags.no_user_site, "PYTHON_STARTUP_PROFILE")
    started, cpu_started = time.monotonic(), time.process_time()
    observed_job_cpu, cpu_records, calls = 0.0, set(), []
    result = {"scope": "two fresh same-host source installations sharing one external Lean runtime",
              "services_started": 0, "source_submissions": 0, "contributions": 0,
              "build_stage_count": 0, "bootstrap_stage_count": 0,
              "cpu_complete": False,
              "unmetered_cpu": "direct build/manage/configure wrappers and any Jobs without successfully bound final receipts; bound nested Jobs counted once",
              "runtime_sharing": "same external immutable distribution path; not independent runtime/host qualification"}

    def observations():
        return {"active_wall_seconds": time.monotonic() - started,
                "coordinator_cpu_seconds": time.process_time() - cpu_started,
                "observed_job_cpu_seconds": observed_job_cpu,
                "observed_cpu_seconds": time.process_time() - cpu_started + observed_job_cpu,
                "cpu_complete": False, "commands_started": len(calls)}

    def budget():
        now = observations()
        require(now["active_wall_seconds"] <= 1800 and now["observed_cpu_seconds"] <= 1800, "AGGREGATE_LIMIT")
        return 1800 - now["active_wall_seconds"]

    def charge_job(path, record):
        nonlocal observed_job_cpu
        identity = str(Path(path).resolve())
        require(identity not in cpu_records, "DOUBLE_COUNTED_JOB")
        cpu = record["final_job"]["cpu_seconds"]
        require(type(cpu) in (int, float) and math.isfinite(cpu) and cpu >= 0, "CPU_OBSERVATION")
        observed_job_cpu += cpu
        cpu_records.add(identity)
        budget()

    def command(name, argv, cwd):
        require(len(calls) < 10, "COMMAND_COUNT")
        remaining = budget()
        require(remaining >= 1, "NO_TIME_REMAINING")
        directory = RUN / "commands" / name
        directory.mkdir(exist_ok=False)
        record = {"name": name, "argv": argv, "cwd": str(cwd), "shell": False,
                  "timeout_seconds": min(500, remaining), "descendant_quiescence": "NOT_YET_OBSERVED"}
        calls.append(record)
        save(directory / "command.json", record)
        stdout, stderr = directory / "stdout.txt", directory / "stderr.txt"
        begin, process = time.monotonic(), None
        try:
            with stdout.open("xb") as out, stderr.open("xb") as err:
                process = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                           shell=False, close_fds=True, creationflags=subprocess.CREATE_NO_WINDOW)
                record["pid"] = process.pid
                while process.poll() is None:
                    require(time.monotonic() - begin <= record["timeout_seconds"], "COMMAND_TIMEOUT")
                    budget()
                    require(stdout.stat().st_size <= 2 * MIB and stderr.stat().st_size <= MIB, "COMMAND_OUTPUT_LIMIT")
                    time.sleep(0.05)
                record["returncode"] = process.wait(timeout=5)
            record["stdout"], record["stderr"] = pin(stdout, 2 * MIB), pin(stderr, MIB)
            raw = read(stdout, 2 * MIB)
            require(record["returncode"] == 0, "COMMAND_FAILED:" + name)
            require(raw.endswith(b"\n") and raw.count(b"\n") == 1, "COMMAND_RESPONSE_FRAME")
            record["elapsed_seconds"] = time.monotonic() - begin
            save(directory / "result.json", record)
            budget()
            return parse(raw), record["stdout"], directory
        except BaseException as error:
            record["error"] = type(error).__name__ + ": " + str(error)[:1024]
            if process is not None and process.poll() is None:
                try:
                    process.kill()
                    record["direct_child_reaped"] = process.wait(timeout=15) is not None
                except (OSError, subprocess.TimeoutExpired) as cleanup_error:
                    record["direct_child_reaped"] = False
                    record["direct_cleanup_error"] = type(cleanup_error).__name__ + ": " + str(cleanup_error)[:512]
            record["descendant_quiescence"] = "UNCONFIRMED_ON_FAILURE; inspect retained nested supervisor/Job records"
            record["elapsed_seconds"] = time.monotonic() - begin
            save(directory / "failure.json", record)
            raise

    def public_request(name, installation, state, scratch, client, operation, arguments, stages):
        request_raw = encode({"client": client, "request_id": name, "op": operation, "args": arguments})
        request_path = RUN / "requests" / (name + ".json")
        request_pin = save_raw(request_path, request_raw)
        call_root = scratch / "calls"
        before = set(call_root.iterdir()) if call_root.exists() else set()
        reply, reply_pin, command_directory = command(name,
            [str(Path(sys.executable).resolve()), *FLAGS, str(installation / "manage.py"), "request",
             "--config", str(state / "config.json"), "--request", str(request_path)], installation)
        after = set(call_root.iterdir())
        added = after - before
        require(len(added) == 1, "PUBLIC_CALL_EVIDENCE_COUNT")
        case = added.pop()
        safe(case, directory=True)
        supervision = parse(read(case / "supervisor.json"))
        event = parse(read(case / "event.json", 65536))
        require(supervision["status"] == "TRANSPORT_COMPLETE" and supervision["returncode"] == 0
                and supervision["final_active_zero"] is True and supervision["direct_child_reaped"] is True
                and supervision["final_job"]["active_processes"] == 0, "PUBLIC_QUIESCENCE")
        require(supervision["request_sha256"] == request_pin["sha256"]
                and event["request_sha256"] == request_pin["sha256"]
                and event["response_sha256"] == reply_pin["sha256"]
                and event["origin_directory"] == str(case.resolve())
                and read(case / "request.json", 131072) == request_raw
                and read(case / "stdout.txt", MIB) == read(reply_pin["path"], MIB), "PUBLIC_IO_BINDING")
        require(event["stages_allocated"] == stages and event["checker_loaded"] is (stages == 1), "PUBLIC_EXPECTED_WORK")
        require(reply.get("status") == "OK", "PUBLIC_REFUSAL:" + name)
        charge_job(case / "supervisor.json", supervision)
        binding = {"request": request_pin, "response": reply_pin,
                   "supervisor": pin(case / "supervisor.json"), "event": pin(case / "event.json"),
                   "descendant_quiescence": "OBSERVED_IN_BOUND_PUBLIC_SUPERVISOR", "native_stages": stages}
        calls[-1]["binding"] = save(command_directory / "public-binding.json", binding)
        calls[-1]["descendant_quiescence"] = binding["descendant_quiescence"]
        result["bootstrap_stage_count"] += stages
        return reply, binding

    owned_run = False
    try:
        launch_raw = read(args.launch, MIB)
        launch = parse(launch_raw)
        require(type(launch) is dict and set(launch) == {"schema", "coordinator", "python", "source_files", "shared_runtime", "ports", "limits"}
                and type(launch["schema"]) is int and launch["schema"] == 1, "LAUNCH_FIELDS")
        require(launch["limits"] == LIMITS and launch["ports"] == {"alpha": 43171, "beta": 43172}, "FIXED_ALLOCATION")
        require(Path(launch["coordinator"]["path"]).resolve() == Path(__file__).resolve()
                and Path(launch["python"]["path"]).resolve() == Path(sys.executable).resolve(), "EXECUTION_PIN_PATH")
        checked(launch["coordinator"])
        checked(launch["python"])
        require(set(launch["shared_runtime"]) == {"path", "lean"}
                and Path(launch["shared_runtime"]["path"]).resolve() == RUNTIME.resolve()
                and Path(launch["shared_runtime"]["lean"]["path"]).resolve() == RUNTIME / "bin/lean.exe", "SHARED_RUNTIME_PATH")
        safe(RUNTIME, directory=True)
        checked(launch["shared_runtime"]["lean"])
        source_files = product_sources(budget)
        supplied = launch["source_files"]
        require(type(supplied) is list and len(supplied) == len(source_files), "SOURCE_PIN_COUNT")
        expected_paths = [str(path) for path in source_files]
        require([str(Path(row["path"]).resolve()) for row in supplied] == expected_paths, "SOURCE_PIN_SET_ORDER")
        require(sum(row["bytes"] for row in supplied) <= 64 * MIB, "SOURCE_TOTAL_BOUND")
        for row in supplied:
            checked(row)
            budget()
        require(not RUN.exists() and not DATA.exists(), "FRESH_PREPARE_REQUIRED")
        safe(SOURCE / "qualification", directory=True)
        if not DATA.parent.exists():
            DATA.parent.mkdir(exist_ok=False)
        safe(DATA.parent, directory=True)
        RUN.mkdir(exist_ok=False)
        owned_run = True
        DATA.mkdir(exist_ok=False)
        for name in ("commands", "requests", "public"):
            (RUN / name).mkdir()
        result["launch"] = save_raw(RUN / "launch.json", launch_raw)
        result["coordinator_snapshot"] = save_raw(RUN / "coordinator.py", read(__file__, MIB))
        result["ports_preflight"] = ports_preflight(launch["ports"])
        result["shared_runtime"] = dict(launch["shared_runtime"],
            identity_scope="executable checked before/after; full shared distribution trusted, not rehashed/copied by this prepare")
        result["nodes"] = {}
        for name in ("alpha", "beta"):
            budget()
            base = DATA / name
            base.mkdir()
            installation, state, scratch = base / "install", base / "state", base / "scratch"
            installation.mkdir()
            copied = []
            for source_pin in supplied:
                source = safe(source_pin["path"])
                relative = source.relative_to(SOURCE)
                target = installation / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                copied_pin = save_raw(target, read(source, 16 * MIB))
                require(copied_pin["bytes"] == source_pin["bytes"] and copied_pin["sha256"] == source_pin["sha256"].lower(), "SOURCE_COPY_BINDING")
                copied.append(copied_pin)
                budget()
            node = {"install": str(installation), "state": str(state), "scratch": str(scratch),
                    "sources": save(RUN / (name + "-source-pins.json"), copied)}
            result["nodes"][name] = node
            build_work = base / "build-work"
            response, response_pin, build_command = command(name + "-build",
                [str(Path(sys.executable).resolve()), *FLAGS, str(installation / "build.py"),
                 "--lean-runtime", str(RUNTIME), "--work", str(build_work)], installation)
            require(response["status"] == "LOCAL_SUPPORT_BUILD_COMPLETED_NOT_MATH_ACCEPTANCE", "BUILD_STATUS")
            receipt_path = installation / "build/build-receipt.json"
            require(response["receipt"] == pin(receipt_path), "BUILD_RECEIPT_REPLY_BINDING")
            receipt = parse(read(receipt_path))
            stage_pin = checked(receipt["stage_receipt"])
            require(Path(stage_pin["path"]).resolve() == build_work / "scratch/support-build/stage-build/stage.json", "BUILD_STAGE_PATH")
            stage = parse(read(stage_pin["path"]))
            require(stage["status"] == "STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE"
                    and len(stage["steps"]) == 2 and all(step["exit_code"] == 0 for step in stage["steps"])
                    and stage["execution_endpoint"]["children_quiescent"] is True
                    and stage["final_job"]["active_processes"] == 0, "BUILD_STAGE_BINDING")
            charge_job(stage_pin["path"], stage)
            result["build_stage_count"] += 1
            node["build"] = {"response": response_pin, "receipt": pin(receipt_path), "stage": stage_pin}
            calls[-1]["binding"] = save(build_command / "build-binding.json", node["build"])
            calls[-1]["descendant_quiescence"] = "OBSERVED_IN_BOUND_BUILD_STAGE"
            other = "beta" if name == "alpha" else "alpha"
            response, config_response_pin, _ = command(name + "-configure",
                [str(Path(sys.executable).resolve()), *FLAGS, str(installation / "manage.py"), "configure",
                 "--state", str(state), "--scratch", str(scratch), "--lean-runtime", str(RUNTIME),
                 "--client", "local", "--client", "reviewer", "--peer", "other=" + str(launch["ports"][other])], installation)
            require(response["status"] == "CONFIGURED_NOT_INITIALIZED" and response["acceptance"] is False
                    and response["config"] == pin(state / "config.json"), "CONFIGURE_REPLY_BINDING")
            config = parse(read(state / "config.json"))
            require(config["offers"] == [] and config["clients"] == ["local", "reviewer"]
                    and config["peers"] == {"other": {"host": "127.0.0.1", "port": launch["ports"][other]}}
                    and config["domains"] == {"install": str(installation), "state": str(state),
                        "scratch": str(scratch), "lean_runtime": str(RUNTIME)}, "FRESH_CONFIG_DOMAINS")
            for key, value in config["files"].items():
                path = Path(value["path"]).resolve()
                require(path == RUNTIME / "bin/lean.exe" if key == "lean" else path.is_relative_to(installation), "HIDDEN_CONFIG_DEPENDENCY")
                checked(value)
            for package in config["common"]["packages"]:
                path = Path(package["path"]).resolve()
                require(path.is_relative_to(installation / "assets"), "COMMON_ASSET_DOMAIN")
                require(pin(path / "manifest.json")["sha256"] == package["manifest_sha256"], "COMMON_MANIFEST_PIN")
            node["config"] = pin(state / "config.json")
            node["configure_response"] = config_response_pin
            calls[-1]["descendant_quiescence"] = "NOT_INDEPENDENTLY_OBSERVED_CONFIGURATION_ONLY"
            calls[-1]["config"] = node["config"]
            initialized, init_binding = public_request(name + "-init", installation, state, scratch, "owner", "init", {}, 1)
            require(initialized.get("accepted") is True and set(initialized["contexts"]) == {"local", "reviewer"}, "INITIAL_CONTEXTS")
            info, info_binding = public_request(name + "-info", installation, state, scratch, "local", "info", {}, 0)
            require(info["context"] == initialized["contexts"]["local"]
                    and info["description"] == initialized["description"] and info["description_historical"] is True, "PUBLIC_INFO_BINDING")
            found, find_binding = public_request(name + "-find-empty", installation, state, scratch, "local", "find",
                {"provider": "P1", "limit": 4, "max_bytes": 16384}, 0)
            require(found["rows"] == [] and found["complete"] is True and found["cursor"] is None
                    and found["untrusted"] is True and found["snapshot"] == info["snapshots"]["P1"], "EMPTY_LOCAL_CANDIDATE_REGISTRY")
            packet = {"status": "FRESH_LOCAL_AUTHORING_REQUIRED", "node": name,
                      "scope": "public initialized empty-offer context; no theorem source, target or proof hint supplied",
                      "interface": {"manage": str(installation / "manage.py"), "config": str(state / "config.json"),
                                    "api_doc": pin(installation / "API.md"), "client": "local", "python_flags": FLAGS},
                      "input": {"client": "local", "context": info["context"],
                                "bootstrap_description": initialized["description"], "description": info["description"],
                                "snapshot": info["snapshots"]["P1"], "empty_find": found},
                      "evidence": {"init": init_binding, "info": info_binding, "find": find_binding}}
            node["author_packet"] = save(RUN / "public" / (name + "-author-packet.json"), packet)
            node["public_info"] = save(RUN / "public" / (name + "-info.json"), info)
            node["state_seal"] = save(RUN / (name + "-state-seal.json"), census(state, budget, hashes=True))
        require(len(calls) == 10 and result["build_stage_count"] == 2 and result["bootstrap_stage_count"] == 2, "EXACT_PREPARE_WORK")
        require(result["nodes"]["alpha"]["state"] != result["nodes"]["beta"]["state"], "INDEPENDENT_STATE_PATHS")
        checked(launch["shared_runtime"]["lean"])
        for source_pin in supplied:
            checked(source_pin)
        retained_data = census(DATA, budget, hashes=True)
        retained_run = census(RUN, budget, hashes=True)
        require(retained_data["bytes"] + retained_run["bytes"] < LIMITS["retained_bytes"] - 16 * MIB, "TOTAL_RETAINED_BYTES")
        result["data_seal"] = save(RUN / "product-local-seal.json", retained_data)
        result["run_seal"] = save(RUN / "evidence-seal.json", retained_run)
        result["retained_bytes_before_final_records"] = retained_data["bytes"] + retained_run["bytes"]
        result["status"] = "PREPARED_TWO_INSTALLATIONS_AWAITING_INDEPENDENT_AUDIT_AND_LOCAL_AUTHORING"
        result["compute"] = observations()
        result["cpu_record_paths"] = sorted(cpu_records)
        result["commands"] = calls
        result["accounting_endpoint"] = "includes copied source and final pre-record censuses; excludes final record serialization/write and stdout"
        budget()
        result_raw = encode(result)
        require(result["retained_bytes_before_final_records"] + result["data_seal"]["bytes"]
                + result["run_seal"]["bytes"] + len(result_raw) <= LIMITS["retained_bytes"], "FINAL_RETAINED_BYTES")
        result_pin = save_raw(RUN / "prepare-result.json", result_raw)
        print(json.dumps({"status": result["status"], "receipt": result_pin,
                          "alpha": result["nodes"]["alpha"]["author_packet"],
                          "beta": result["nodes"]["beta"]["author_packet"]}))
        return 0
    except BaseException as error:
        result.update(status="STOPPED", error=type(error).__name__, detail=str(error)[:2048],
                      compute=observations(), commands=calls, cpu_record_paths=sorted(cpu_records))
        if owned_run:
            failure = save(RUN / "prepare-failure.json", result)
            print(json.dumps({"status": "STOPPED", "failure": failure}))
        else:
            print(json.dumps({"status": "STOPPED_BEFORE_RUN_CREATION", "detail": str(error)[:2048]}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

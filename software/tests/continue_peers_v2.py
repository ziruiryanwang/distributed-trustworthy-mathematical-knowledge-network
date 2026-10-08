"""Second coordinator cut: preserve actual accounting on public refusals.

Root alone launches after source/allocation review. No product imports, source
repair, direct database access, retries, or negative-control fixture machinery.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time

SOURCE = Path(__file__).resolve().parents[1]
PROJECT = SOURCE.parent
DATA = PROJECT / "product-local/peer-01"
MIB = 1048576
FLAGS = ["-B", "-E", "-s", "-S"]
LIMITS = {"command_seconds": 500, "active_wall_seconds": 1800,
          "observed_cpu_seconds": 1800, "retained_bytes": 1024 * MIB,
          "service_seconds": 120, "service_max_requests": 2,
          "service_max_bytes": 64 * MIB}
PHASES = {"g_to_beta": ("g", "alpha", "beta", 43171),
          "h_to_alpha": ("h", "beta", "alpha", 43172)}
ATTEMPTS = {"g_to_beta": "g02", "h_to_alpha": "h01"}


def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def bootstrap_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    def finite(token):
        value = float(token)
        require(math.isfinite(value), "NONFINITE_JSON")
        return value
    def bad(_):
        raise RuntimeError("NONFINITE_JSON")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=finite, parse_constant=bad)


def bootstrap_read(path, maximum):
    path = Path(path)
    require(path.is_absolute(), "ABSOLUTE_PATH")
    for ancestor in (path, *path.parents):
        stat = ancestor.lstat()
        require(not ancestor.is_symlink() and not (getattr(stat, "st_file_attributes", 0) & 0x400), "REPARSE_POINT")
    require(path.is_file() and path.stat().st_size <= maximum, "FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    require(len(raw) <= maximum, "FILE_BOUND")
    return raw


def bootstrap_pin(record, selected):
    require(type(record) is dict and set(record) == {"path", "bytes", "sha256"}, "PIN_FIELDS")
    require(type(record["path"]) is str and Path(record["path"]).is_absolute()
            and Path(record["path"]).resolve() == Path(selected).resolve(), "PIN_PATH")
    require(type(record["bytes"]) is int and 0 < record["bytes"] <= 16 * MIB
            and type(record["sha256"]) is str and re.fullmatch(r"[a-fA-F0-9]{64}", record["sha256"]), "PIN_SHAPE")
    raw = bootstrap_read(record["path"], 16 * MIB)
    require(len(raw) == record["bytes"] and hashlib.sha256(raw).hexdigest() == record["sha256"].lower(), "PIN_CHANGED")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", required=True, type=Path)
    args = parser.parse_args()
    require(sys.dont_write_bytecode and sys.flags.ignore_environment and sys.flags.no_site
            and sys.flags.no_user_site and os.name == "nt", "PYTHON_WINDOWS_PROFILE")
    started, cpu_started = time.monotonic(), time.process_time()
    run, helper, service = None, None, None
    commands, jobs, observed_job_cpu = [], set(), 0.0
    result = {"schema": 2, "scope": "one direction of same-host public positive reciprocal loop",
              "cpu_complete": False, "native_stages": 0, "public_commands": 0,
              "observed_pipeline_children": 0, "pipeline_children_complete_for_bound_calls": True,
              "services_started": 0, "services_quiescent": 0,
              "substantive_dependency_use_audited": False,
              "unmetered_cpu": "direct manage wrappers and Jobs lacking successfully bound final receipts",
              "containment": "coordinator/direct wrappers use cooperative checkpoints only; no outer OS CPU/memory container"}

    def observations():
        return {"active_wall_seconds": time.monotonic() - started,
                "coordinator_cpu_seconds": time.process_time() - cpu_started,
                "observed_job_cpu_seconds": observed_job_cpu,
                "observed_cpu_seconds": time.process_time() - cpu_started + observed_job_cpu,
                "cpu_complete": False}

    def budget():
        current = observations()
        require(current["active_wall_seconds"] <= 1800 and current["observed_cpu_seconds"] <= 1800, "AGGREGATE_LIMIT")
        return 1800 - current["active_wall_seconds"]

    def exact(left, right):
        return helper.encode(left) == helper.encode(right)

    def object_pin(record, maximum=16 * MIB):
        actual = helper.checked(record, maximum)
        return helper.parse(helper.read(actual["path"], maximum))

    def pin_equal(actual, declared):
        return (Path(actual["path"]).resolve() == Path(declared["path"]).resolve()
                and actual["bytes"] == declared["bytes"]
                and actual["sha256"].lower() == declared["sha256"].lower())

    def account(path, receipt):
        nonlocal observed_job_cpu
        path = str(helper.safe(path))
        require(path not in jobs, "JOB_DOUBLE_COUNT")
        value = receipt["final_job"]["cpu_seconds"]
        require(type(value) in (int, float) and math.isfinite(value) and value >= 0, "JOB_CPU")
        observed_job_cpu += value
        jobs.add(path)

    def start_command(name, argv, installation, maximum=500):
        require(len(commands) < 11, "COMMAND_COUNT")
        remaining = budget()
        require(remaining >= 1, "NO_TIME_REMAINING")
        directory = run / "commands" / name
        directory.mkdir(exist_ok=False)
        record = {"name": name, "argv": argv, "cwd": str(installation), "shell": False,
                  "timeout_seconds": min(maximum, remaining), "started_offset": time.monotonic() - started,
                  "descendant_quiescence": "NOT_YET_OBSERVED"}
        commands.append(record)
        helper.save(directory / "command.json", record)
        stdout, stderr = directory / "stdout.txt", directory / "stderr.txt"
        with stdout.open("xb") as out, stderr.open("xb") as err:
            process = subprocess.Popen(argv, cwd=installation, stdin=subprocess.DEVNULL,
                stdout=out, stderr=err, shell=False, close_fds=True, creationflags=subprocess.CREATE_NO_WINDOW)
        record["pid"] = process.pid
        result["public_commands"] = len(commands)
        return {"process": process, "directory": directory, "record": record,
                "stdout": stdout, "stderr": stderr, "begin": time.monotonic(), "finished": False}

    def poll_command(job):
        budget()
        require(time.monotonic() - job["begin"] <= job["record"]["timeout_seconds"], "COMMAND_TIMEOUT")
        require(job["stdout"].stat().st_size <= 2 * MIB and job["stderr"].stat().st_size <= MIB, "COMMAND_OUTPUT_LIMIT")
        return job["process"].poll()

    def finish_command(job):
        while poll_command(job) is None:
            time.sleep(0.05)
        job["record"]["returncode"] = job["process"].wait(timeout=5)
        job["record"]["direct_child_reaped"] = True
        job["finished"] = True
        job["record"]["stdout"] = helper.pin(job["stdout"], 2 * MIB)
        job["record"]["stderr"] = helper.pin(job["stderr"], MIB)
        job["record"]["elapsed_seconds"] = time.monotonic() - job["begin"]
        helper.save(job["directory"] / "result.json", job["record"])
        raw = helper.read(job["stdout"], 2 * MIB)
        require(job["record"]["returncode"] == 0, "COMMAND_FAILED:" + job["record"]["name"])
        require(raw.endswith(b"\n") and raw.count(b"\n") == 1, "COMMAND_RESPONSE_FRAME")
        return helper.parse(raw), job["record"]["stdout"]

    def failed_direct(job):
        if job is None:
            return
        process, record = job["process"], job["record"]
        if record["descendant_quiescence"] == "OBSERVED_BOUND_JOB_ACTIVE_ZERO_AND_DIRECT_REAP":
            # A later application/workload assertion does not erase the already
            # authenticated original supervisor's process-quiescence evidence.
            return
        try:
            if process.poll() is None:
                process.kill()
            record["returncode"] = process.wait(timeout=15)
            record["direct_child_reaped"] = True
        except (OSError, subprocess.TimeoutExpired) as error:
            record["direct_cleanup_error"] = type(error).__name__ + ":" + str(error)[:512]
            record["direct_child_reaped"] = False
        record["descendant_quiescence"] = "UNCONFIRMED_ON_FAILURE; direct wrapper cleanup is not Job cleanup"

    def binding(job, case, expected_raw, reply_pin, service_call=False):
        case = helper.safe(case, directory=True)
        receipt_path = case / "supervisor.json"
        receipt = helper.parse(helper.read(receipt_path, 65536))
        event = helper.parse(helper.read(case / "event.json", 65536))
        require(receipt["status"] == "TRANSPORT_COMPLETE" and receipt["returncode"] == 0
                and receipt["direct_child_reaped"] is True and receipt["final_active_zero"] is True
                and type(receipt["final_job"]["active_processes"]) is int
                and receipt["final_job"]["active_processes"] == 0
                and receipt.get("cleanup_errors", []) == [], "PUBLIC_QUIESCENCE")
        digest = hashlib.sha256(expected_raw).hexdigest()
        require(receipt["request_sha256"] == digest and event["request_sha256"] == digest
                and event["response_sha256"] == reply_pin["sha256"]
                and helper.read(case / "request.json", 131072) == expected_raw
                and helper.read(case / "stdout.txt", 2 * MIB) == helper.read(reply_pin["path"], 2 * MIB), "PUBLIC_IO_BINDING")
        if not service_call:
            require(event["origin_directory"] == str(case), "PUBLIC_ORIGINAL_CALL")
        job["record"]["descendant_quiescence"] = "OBSERVED_BOUND_JOB_ACTIVE_ZERO_AND_DIRECT_REAP"
        actual_native = event["native_stages"] if service_call else event["stages_allocated"]
        require(type(actual_native) is int and 0 <= actual_native <= 64, "ACTUAL_NATIVE_STAGE_COUNT")
        actual_checker = event["checker_loaded"]
        require(type(actual_checker) is bool, "ACTUAL_CHECKER_LOAD_TYPE")
        metrics = event.get("checker_metrics", {})
        require(type(metrics) is dict, "ACTUAL_CHECKER_METRICS")
        metric_stages, actual_children = metrics.get("stage_allocations"), metrics.get("pipeline_children")
        for value in (metric_stages, actual_children):
            require(value is None or (type(value) is int and 0 <= value <= 320), "ACTUAL_PIPELINE_COUNTER")
        actual = {"stages_allocated": actual_native, "checker_loaded": actual_checker,
                  "checker_stage_allocations": metric_stages, "pipeline_children": actual_children}
        job["record"]["actual_work"] = actual
        result["native_stages"] += actual_native
        if actual_children is not None:
            result["observed_pipeline_children"] += actual_children
        elif actual_checker:
            result["pipeline_children_complete_for_bound_calls"] = False
        account(receipt_path, receipt)
        value = {"supervisor": helper.pin(receipt_path), "event": helper.pin(case / "event.json"),
                 "request_sha256": digest, "response": reply_pin, "native_stages": actual_native,
                 "actual_work": actual,
                 "descendant_quiescence": "OBSERVED_BOUND_JOB_ACTIVE_ZERO_AND_DIRECT_REAP",
                 "observed_offset": time.monotonic() - started}
        job["record"]["binding"] = helper.save(job["directory"] / "binding.json", value)
        job["record"]["descendant_quiescence"] = value["descendant_quiescence"]
        # Accounting and the immutable evidence binding precede status/workload
        # assertions. A one-child source rejection still spent one native stage.
        budget()
        return value

    def success_workload(evidence, native, checker, children=None):
        actual = evidence["actual_work"]
        require(actual["stages_allocated"] == native, "NATIVE_STAGE_COUNT")
        require(actual["checker_loaded"] is checker, "CHECKER_LOAD_PROFILE")
        if children is not None:
            require(actual["checker_stage_allocations"] == native
                    and actual["pipeline_children"] == children, "NATIVE_PIPELINE_PROFILE")

    def request(name, node, op, arguments, native=0, checker=False, children=None):
        request_raw = helper.encode({"client": "local", "request_id": name, "op": op, "args": arguments})
        require(len(request_raw) <= 131072, "PUBLIC_REQUEST_BOUND")
        request_path = run / "requests" / (name + ".json")
        request_pin = helper.save_raw(request_path, request_raw)
        calls = node["scratch"] / "calls"
        before = set(calls.iterdir())
        job = None
        try:
            job = start_command(name, [str(Path(sys.executable).resolve()), *FLAGS,
                str(node["install"] / "manage.py"), "request", "--config", str(node["config_path"]),
                "--request", str(request_path)], node["install"])
            reply, reply_pin = finish_command(job)
            added = set(calls.iterdir()) - before
            require(len(added) == 1, "ACTUAL_PUBLIC_CALL_COUNT")
            evidence = binding(job, added.pop(), request_raw, reply_pin)
            evidence["request"] = request_pin
            require(type(reply) is dict, "PUBLIC_RESPONSE_TYPE")
            job["record"]["public_status"] = reply.get("status")
            job["record"]["public_code"] = reply.get("code")
            require(reply.get("status") == "OK", "PUBLIC_REFUSAL:" + str(reply.get("code", reply.get("status")))[:256])
            success_workload(evidence, native, checker, children)
            return reply, evidence
        except BaseException:
            failed_direct(job)
            raise

    def service_finish(required=True):
        nonlocal service
        if service is None:
            return
        job, node = service["job"], service["node"]
        reply, reply_pin = finish_command(job)
        case = node["scratch"] / "services" / service["session"] / "cases/serve"
        bound = binding(job, case, service["request_raw"], reply_pin, service_call=True)
        require(reply.get("status") == "SERVICE_STOPPED" and reply["session"] == service["session"]
                and reply["view"] == service["view"] and reply["catalog_sha256"] == service["catalog"]
                and reply["mathematicalAcceptance"] is False and reply["native_stages"] == 0, "SERVICE_STOP_BINDING")
        success_workload(bound, 0, False)
        observed = reply["observations"]
        require(observed["bind_host"] == "127.0.0.1" and observed["port"] == service["port"]
                and observed["checker_loaded"] is False and observed["native_stages"] == 0
                and observed["mathematicalAcceptance"] is False
                and observed["connections"] <= 2 and observed["charged_send_bytes"] <= 64 * MIB, "SERVICE_OBSERVATIONS")
        result["service_stop"] = {"response": reply_pin, "binding": bound,
                                  "readiness": service.get("readiness"), "observations": observed}
        result["services_quiescent"] += 1
        service = None
        if required:
            require(type(observed["connections"]) is int and observed["connections"] == 2
                    and type(observed["responses"]) is int and observed["responses"] == 2
                    and "last_error" not in observed, "SERVICE_TWO_SUCCESSFUL_TRANSFERS")

    try:
        launch_raw = bootstrap_read(args.launch, MIB)
        launch = bootstrap_json(launch_raw)
        require(type(launch) is dict and set(launch) == {"schema", "phase", "attempt", "coordinator", "helper", "python",
                "prepare", "previous", "author", "original_failure", "original_outcome", "limits"}
                and type(launch["schema"]) is int and launch["schema"] == 2
                and launch["phase"] in PHASES and launch["attempt"] == ATTEMPTS[launch["phase"]], "LAUNCH_FIELDS")
        require(launch["limits"] == LIMITS, "FIXED_ALLOCATION")
        bootstrap_pin(launch["coordinator"], __file__)
        bootstrap_pin(launch["python"], sys.executable)
        bootstrap_pin(launch["helper"], SOURCE / "tests/prepare_peers.py")
        spec = importlib.util.spec_from_file_location("reviewed_peer_prepare_helpers", launch["helper"]["path"])
        require(spec is not None and spec.loader is not None, "HELPER_LOADER")
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        letter, sender_name, receiver_name, port = PHASES[launch["phase"]]
        attempt = launch["attempt"]
        run = SOURCE / "qualification" / ("peer-01-" + attempt)
        require(not run.exists(), "FRESH_PHASE_REQUIRED")
        helper.safe(run.parent, directory=True)
        prepared = object_pin(launch["prepare"])
        require(prepared["status"] == "PREPARED_TWO_INSTALLATIONS_AWAITING_INDEPENDENT_AUDIT_AND_LOCAL_AUTHORING",
                "PREPARE_STATUS")
        require(helper.safe(launch["prepare"]["path"]) == SOURCE / "qualification/peer-01/prepare-result.json", "PREPARE_PATH")
        previous = object_pin(launch["previous"])
        if letter == "g":
            require(pin_equal(launch["prepare"], launch["previous"]), "INITIAL_PREVIOUS_RECEIPT")
            original_failure = object_pin(launch["original_failure"])
            require(helper.safe(launch["original_failure"]["path"]) == SOURCE / "qualification/peer-01-g/continue-failure.json"
                    and original_failure["status"] == "STOPPED" and original_failure["phase"] == "g_to_beta"
                    and pin_equal(original_failure["prepare"], launch["prepare"]), "ORIGINAL_FAILURE_LINEAGE")
            original_outcome = helper.checked(launch["original_outcome"])
            require(helper.safe(original_outcome["path"]) == SOURCE / "qualification/peer-01-g/OUTCOME.md",
                    "ORIGINAL_OUTCOME_PATH")
        else:
            require(launch["original_failure"] is None and launch["original_outcome"] is None, "H_INHERITS_LINEAGE_ONLY")
            require(type(previous["schema"]) is int and previous["schema"] == 2
                    and previous["attempt"] == "g02" and previous["phase"] == "g_to_beta"
                    and previous["status"] == "G_OFFLINE_ADMITTED_BY_BETA_AWAITING_INDEPENDENT_H_AUTHORING"
                    and pin_equal(previous["prepare"], launch["prepare"])
                    and helper.safe(launch["previous"]["path"]) == SOURCE / "qualification/peer-01-g02/continue-result.json",
                    "G_HANDOFF_REQUIRED")
        prepare_launch = object_pin(prepared["launch"])
        require(pin_equal(prepared["shared_runtime"]["lean"], prepare_launch["shared_runtime"]["lean"])
                and pin_equal(launch["python"], prepare_launch["python"])
                and pin_equal(launch["helper"], prepare_launch["coordinator"]), "PREPARED_RUNTIME_HELPER_BINDING")
        helper.checked(prepared["shared_runtime"]["lean"])
        nodes, expected = {}, {}
        for name in ("alpha", "beta"):
            prior_node = prepared["nodes"][name]
            installation = helper.safe(DATA / name / "install", directory=True)
            state = helper.safe(DATA / name / "state", directory=True)
            scratch = helper.safe(DATA / name / "scratch", directory=True)
            require(prior_node["install"] == str(installation) and prior_node["state"] == str(state)
                    and prior_node["scratch"] == str(scratch), "PREPARED_NODE_DOMAINS")
            source_pins = object_pin(prior_node["sources"])
            require(type(source_pins) is list and 1 <= len(source_pins) <= 512, "INSTALLED_SOURCE_COUNT")
            selected = []
            for source_pin in source_pins:
                checked = helper.checked(source_pin)
                path = Path(checked["path"])
                require(path.is_relative_to(installation), "INSTALLED_SOURCE_DOMAIN")
                selected.append(path)
                budget()
            actual = [installation / item for item in ("API.md", "manage.py", "build.py", "assets-lock.json")]
            actual.extend((installation / "py").glob("*.py"))
            for folder in ("assets", "native"):
                actual.extend(installation / folder / row["path"] for row in helper.census(installation / folder, budget)["manifest"])
            require(len(set(selected)) == len(selected) and set(selected) == set(actual), "INSTALLED_SOURCE_SET")
            config = object_pin(prior_node["config"])
            require(helper.safe(prior_node["config"]["path"]) == state / "config.json"
                    and exact(config["domains"], {"install": str(installation), "state": str(state),
                        "scratch": str(scratch), "lean_runtime": prepared["shared_runtime"]["path"]}), "CONFIG_DOMAINS")
            for key, file_pin in config["files"].items():
                checked = helper.checked(file_pin)
                require(pin_equal(checked, prepared["shared_runtime"]["lean"]) if key == "lean"
                        else Path(checked["path"]).is_relative_to(installation), "CONFIG_FILE_DOMAIN")
            helper.checked(prior_node["build"]["receipt"])
            other_port = 43172 if name == "alpha" else 43171
            require(config["peers"] == {"other": {"host": "127.0.0.1", "port": other_port}}, "FIXED_PEER_ALIAS")
            nodes[name] = {"install": installation, "state": state, "scratch": scratch,
                           "config_path": state / "config.json", "source_pins": source_pins,
                           "config_pin": prior_node["config"], "configured_files": config["files"],
                           "build_receipt": prior_node["build"]["receipt"]}
            if letter == "g":
                info = object_pin(prior_node["public_info"])
                expected[name] = {"context": info["context"], "snapshot": info["snapshots"]["P1"],
                                  "description": info["description"]}
            else:
                expected[name] = previous["expected_public"][name]
        author = object_pin(launch["author"], MIB)
        require(type(author) is dict and set(author) == {"schema", "node", "context", "root", "source"}
                and type(author["schema"]) is int and author["schema"] == 1
                and author["node"] == sender_name and author["context"] == expected[sender_name]["context"]
                and type(author["root"]) is str and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*", author["root"]),
                "AUTHOR_ENVELOPE")
        helper.checked(author["source"], 65536)
        source_raw = helper.read(author["source"]["path"], 65536)
        source_text = source_raw.decode("utf-8", errors="strict")
        run.mkdir(exist_ok=False)
        for directory in ("commands", "requests", "public"):
            (run / directory).mkdir()
        result.update(phase=launch["phase"], attempt=attempt, sender=sender_name, receiver=receiver_name,
                      prepare=launch["prepare"], previous=launch["previous"], author=launch["author"],
                      original_failure=launch["original_failure"], original_outcome=launch["original_outcome"],
                      history_accounting="current allocation only; previous attempts retain their consumed charges and separate audited cost records",
                      launch=helper.save_raw(run / "launch.json", launch_raw),
                      source=helper.save_raw(run / "author-source.lean", source_raw), source_root=author["root"],
                      runtime_sharing=prepared["runtime_sharing"], expected_public=expected,
                      coordinator_snapshot=helper.save_raw(run / "coordinator.py", helper.read(__file__, MIB)))
        result["baseline_data"] = helper.save(run / "baseline-data.json", helper.census(DATA, budget, hashes=True))
        sender, receiver = nodes[sender_name], nodes[receiver_name]
        prefix = "peer-" + attempt
        sender_info, _ = request(prefix + "-sender-info", sender, "info", {})
        receiver_info, _ = request(prefix + "-receiver-info", receiver, "info", {})
        for name, info in ((sender_name, sender_info), (receiver_name, receiver_info)):
            require(exact({"context": info["context"], "snapshot": info["snapshots"]["P1"],
                           "description": info["description"]}, expected[name]) and info["description_historical"] is True,
                    "PUBLIC_HEAD_SNAPSHOT_CHANGED")
        submitted, submit_evidence = request(prefix + "-submit", sender, "submit",
            {"context": author["context"], "source": source_text, "root": author["root"]}, 1, True, 5)
        require(submitted.get("accepted") is True and submitted["context"] == author["context"]
                and submitted["source_sha256"] == hashlib.sha256(source_raw).hexdigest()
                and submitted["source_root"] == author["root"], "EXACT_AUTHOR_SOURCE_ACCEPTANCE")
        published, publish_evidence = request(prefix + "-publish", sender, "publish",
            {"artifact": submitted["artifact"], "snapshot": sender_info["snapshots"]["P1"]}, checker=True, children=0)
        require(published["untrusted"] is True and published["candidate_only"] is True
                and published["existing"] is False, "NEW_LOCAL_PUBLICATION")
        if letter == "h":
            require(not exact(published["descriptor_id"], previous["descriptor_id"]), "DISTINCT_G_H_REQUIRED")
        exposed, expose_evidence = request(prefix + "-expose", sender, "expose",
            {"selected": [published["candidate"]]}, checker=True, children=0)
        require(exposed["entries"] == 1 and exposed["historical_view"] is True
                and exposed["mathematicalAcceptance"] is False and exposed["native_stages"] == 0, "SINGLE_PUBLISHED_EXPOSURE")
        session = prefix + "-service"
        service_root = sender["scratch"] / "services" / session
        require(not service_root.exists(), "FRESH_SERVICE_REQUIRED")
        service_request = {"op": "serve", "session": session, "client": "local", "view": exposed["view"],
                           "port": port, "seconds": 120, "max_requests": 2, "max_bytes": 64 * MIB}
        job = start_command(session, [str(Path(sys.executable).resolve()), *FLAGS,
            str(sender["install"] / "manage.py"), "serve", "--config", str(sender["config_path"]),
            "--client", "local", "--view", exposed["view"], "--session", session,
            "--port", str(port), "--seconds", "120", "--max-requests", "2", "--max-bytes", str(64 * MIB)],
            sender["install"], maximum=180)
        service = {"job": job, "node": sender, "session": session, "view": exposed["view"],
                   "catalog": exposed["catalog_sha256"], "port": port, "request_raw": helper.encode(service_request)}
        result["services_started"] += 1
        ready = service_root / "ready.json"
        while not ready.exists():
            require(poll_command(job) is None, "SERVICE_EXITED_BEFORE_READY")
            require(time.monotonic() - job["begin"] <= 30, "SERVICE_READINESS_TIMEOUT")
            time.sleep(0.05)
        ready_value = helper.parse(helper.read(ready, 4096))
        require(exact(ready_value, {"host": "127.0.0.1", "port": port,
                                  "catalog_sha256": exposed["catalog_sha256"]}), "READINESS_BINDING")
        service["readiness"] = helper.pin(ready)
        found, find_evidence = request(prefix + "-peer-find", receiver, "peer_find", {"peer": "other"})
        require(found["untrusted"] is True and found["candidate_only"] is True
                and found["mathematicalAcceptance"] is False and found["native_stages"] == 0
                and found["complete"] is True and len(found["rows"]) == 1
                and found["catalog_sha256"] == exposed["catalog_sha256"]
                and exact(found["rows"][0]["descriptor_id"], published["descriptor_id"]), "DISCOVERED_PUBLICATION_BINDING")
        acquired, acquire_evidence = request(prefix + "-peer-acquire", receiver, "peer_acquire",
            {"remote": found["rows"][0]["remote"]}, checker=True, children=0)
        require(acquired["untrusted"] is True and acquired["candidate_only"] is True
                and acquired["mathematicalAcceptance"] is False and acquired["native_stages"] == 0
                and acquired["existing"] is False
                and exact(acquired["descriptor_id"], published["descriptor_id"]), "RECEIVER_CANDIDATE_ONLY")
        before_admit, _ = request(prefix + "-before-admit", receiver, "info", {})
        require(before_admit["context"] == receiver_info["context"]
                and exact(before_admit["description"], receiver_info["description"])
                and before_admit["snapshots"]["P1"] == acquired["snapshot"], "ACQUISITION_MUST_NOT_ADVANCE_HEAD")
        service_finish()
        require(service is None and result["services_quiescent"] == 1, "SENDER_MUST_BE_STOPPED_BEFORE_ADMISSION")
        admitted, admit_evidence = request(prefix + "-offline-admit", receiver, "admit",
            {"context": receiver_info["context"], "selected": [acquired["candidate"]]}, 1, True, 1)
        require(admitted.get("accepted") is True and admitted["context"] != receiver_info["context"], "FRESH_RECEIVER_ADMISSION")
        require(commands[-1]["started_offset"] > result["service_stop"]["binding"]["observed_offset"], "OFFLINE_ADMISSION_ORDER")
        after, after_evidence = request(prefix + "-after-admit", receiver, "info", {})
        require(after["context"] == admitted["context"] and exact(after["description"], admitted["description"])
                and after["snapshots"]["P1"] == acquired["snapshot"] and after["description_historical"] is True,
                "ADMITTED_PUBLIC_INFO_BINDING")
        expected[sender_name] = {"context": sender_info["context"], "snapshot": published["snapshot"],
                                 "description": sender_info["description"]}
        expected[receiver_name] = {"context": after["context"], "snapshot": after["snapshots"]["P1"],
                                   "description": after["description"]}
        result.update(descriptor_id=published["descriptor_id"], submission=submit_evidence,
                      publication=publish_evidence, exposure=expose_evidence, discovery=find_evidence,
                      acquisition=acquire_evidence, admission=admit_evidence,
                      receiver_info=helper.save(run / "public" / (receiver_name + "-info.json"), after),
                      expected_public=expected)
        packet = {"status": "FRESH_LOCAL_AUTHORING_REQUIRED" if letter == "g" else "RECIPROCAL_LOOP_AUDIT_REQUIRED",
                  "node": receiver_name, "scope": "actual receiver-local offline-admitted public context; no source/proof hint supplied",
                  "interface": {"manage": str(receiver["install"] / "manage.py"),
                      "config": str(receiver["config_path"]), "api_doc": helper.pin(receiver["install"] / "API.md"),
                      "client": "local", "python_flags": FLAGS},
                  "input": {"client": "local", "context": after["context"], "description": after["description"],
                      "snapshot": after["snapshots"]["P1"], "acquired_descriptor": acquired["descriptor_id"]},
                  "evidence": {"admit": admit_evidence, "info": after_evidence, "sender_stop": result["service_stop"]}}
        result["author_packet"] = helper.save(run / "public" / (receiver_name + "-author-packet.json"), packet)
        require(len(commands) == 11 and result["native_stages"] == 2 and result["services_started"] == 1
                and result["services_quiescent"] == 1, "EXACT_PHASE_WORK")
        for node in nodes.values():
            helper.checked(node["config_pin"])
            helper.checked(node["build_receipt"])
            for file_pin in node["configured_files"].values():
                helper.checked(file_pin)
                budget()
            for source_pin in node["source_pins"]:
                helper.checked(source_pin)
                budget()
        helper.checked(prepared["shared_runtime"]["lean"])
        helper.checked(launch["helper"])
        helper.checked(launch["coordinator"])
        helper.checked(launch["python"])
        helper.checked(launch["author"])
        helper.checked(launch["prepare"])
        helper.checked(launch["previous"])
        if letter == "g":
            helper.checked(launch["original_failure"])
            helper.checked(launch["original_outcome"])
        helper.checked(author["source"], 65536)
        retained_data = helper.census(DATA, budget, hashes=True)
        retained_run = helper.census(run, budget, hashes=True)
        total = retained_data["bytes"] + retained_run["bytes"]
        require(total < LIMITS["retained_bytes"] - 16 * MIB, "RETAINED_TOTAL")
        result["data_seal"] = helper.save(run / "product-local-seal.json", retained_data)
        result["run_seal"] = helper.save(run / "evidence-seal.json", retained_run)
        result["retained_bytes_before_final_records"] = total
        result["status"] = ("G_OFFLINE_ADMITTED_BY_BETA_AWAITING_INDEPENDENT_H_AUTHORING" if letter == "g"
                            else "POSITIVE_RECIPROCAL_OFFLINE_LOOP_COMPLETED_AWAITING_DEPENDENCY_AUDIT")
        result["compute"], result["commands"], result["cpu_record_paths"] = observations(), commands, sorted(jobs)
        result["accounting_endpoint"] = "before final serialization/write/stdout; copied data and phase evidence included, earlier qualification/authoring records excluded"
        raw = helper.encode(result)
        require(total + result["data_seal"]["bytes"] + result["run_seal"]["bytes"] + len(raw)
                <= LIMITS["retained_bytes"], "FINAL_RETAINED_TOTAL")
        budget()
        receipt = helper.save_raw(run / "continue-result.json", raw)
        print(json.dumps({"status": result["status"], "receipt": receipt, "author_packet": result["author_packet"]}))
        return 0
    except BaseException as error:
        if service is not None:
            try:
                # Let the finite original service grant end and inspect its own
                # cleanup. This is not an HTTP stop probe or a new service grant.
                service_finish(required=False)
            except BaseException as cleanup_error:
                result["service_cleanup_error"] = type(cleanup_error).__name__ + ":" + str(cleanup_error)[:1024]
                if service is not None:
                    failed_direct(service["job"])
                result["service_descendants"] = "UNCONFIRMED; inspect retained original service supervisor"
        result.update(status="STOPPED", error=type(error).__name__, detail=str(error)[:2048],
                      compute=observations(), commands=commands, cpu_record_paths=sorted(jobs))
        if helper is not None and run is not None and run.is_dir() and "launch" in result:
            receipt = helper.save(run / "continue-failure.json", result)
            print(json.dumps({"status": "STOPPED", "failure": receipt}))
        else:
            print(json.dumps({"status": "STOPPED_BEFORE_OWNED_PHASE_RECORD", "detail": str(error)[:2048]}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

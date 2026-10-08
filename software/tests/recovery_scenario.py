"""Fresh, genuine slow-transfer recovery qualifier; root-only reviewed launch.

One new receiver, one actual published inert fixture, one intentional timeout.
No source authoring, native admission, database writes, refunds, or retries.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
import json
import math
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import threading
import time

SOURCE = Path(__file__).resolve().parents[1]
PROJECT = SOURCE.parent
RUN = SOURCE / "qualification/recovery-01"
DATA = PROJECT / "product-local/recovery-01"
FLAGS = ["-B", "-E", "-s", "-S"]
MIB = 1048576
LIMITS = {"active_wall_seconds": 1800, "observed_cpu_seconds": 1800,
          "command_seconds": 500, "retained_bytes": 1024 * MIB,
          "sender_seconds": 90, "sender_connections": 3,
          "sender_bytes": 4 * MIB, "interrupt_seconds": 10, "port": 43173}
ORDINARY_NAMES = ("node", "run_stage", "storage", "checking", "domains", "supervise",
                  "peer_wire", "peer_service", "peer_node")
RECOVERY_LIMITS = {"wall_seconds": 30, "cpu_seconds": 15, "memory_mib": 256,
                   "active_processes": 8, "stdout_bytes": MIB, "stderr_bytes": 65536,
                   "event_bytes": 65536, "request_bytes": 16384,
                   "poll_seconds": 0.05, "settle_seconds": 5}
TABLES = {"meta": "id", "requests": "key", "records": "handle", "heads": "client",
          "providers": "provider", "snapshots": "handle", "entries": "provider,seq", "stages": "id"}


def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def bootstrap_read(path, maximum):
    path = Path(path)
    require(path.is_absolute(), "ABSOLUTE_PATH")
    for ancestor in (path, *path.parents):
        stat = ancestor.lstat()
        require(not ancestor.is_symlink() and not (getattr(stat, "st_file_attributes", 0) & 0x400), "REPARSE_POINT")
    require(path.is_file() and path.stat().st_size <= maximum, "READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    require(len(raw) <= maximum, "READ_BOUND")
    return raw


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
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=bad, parse_float=finite)


def bootstrap_pin(pin, target):
    require(type(pin) is dict and set(pin) == {"path", "bytes", "sha256"}
            and type(pin["bytes"]) is int and 0 < pin["bytes"] <= 16 * MIB
            and type(pin["path"]) is str and Path(pin["path"]).is_absolute()
            and Path(pin["path"]).resolve() == Path(target).resolve(), "BOOTSTRAP_PIN")
    raw = bootstrap_read(pin["path"], 16 * MIB)
    require(len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"].lower(), "PIN_CHANGED")


class FaultSender:
    """Trusted cooperative thread; CPU is included in coordinator process CPU."""
    def __init__(self, catalog, bundle, digest, started):
        self.catalog, self.bundle, self.digest, self.started = catalog, bundle, digest, started
        self.stop, self.ready, self.slow_done = threading.Event(), threading.Event(), threading.Event()
        self.lock, self.listener, self.connection = threading.Lock(), None, None
        self.record = {"connections": [], "charged_bytes": 0, "closed_listener": False,
                       "closed_connections": 0, "joined": False, "errors": []}
        self.thread = threading.Thread(target=self.run, name="recovery-fault-sender", daemon=True)

    def offset(self):
        return time.monotonic() - self.started

    def count(self):
        with self.lock:
            return len(self.record["connections"])

    def run(self):
        beginning = time.monotonic()
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener = server
            if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
                server.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            server.bind(("127.0.0.1", LIMITS["port"]))
            server.listen(1)
            server.settimeout(0.2)
            self.record["ready_offset"] = self.offset()
            self.ready.set()
            while self.count() < 3 and not self.stop.is_set():
                require(time.monotonic() - beginning <= 90, "SENDER_SESSION_TIMEOUT")
                try:
                    connection, address = server.accept()
                except socket.timeout:
                    continue
                self.connection = connection
                with connection:
                    require(address[0] == "127.0.0.1", "SENDER_ADDRESS")
                    connection.settimeout(2)
                    request = b""
                    while b"\r\n\r\n" not in request:
                        require(time.monotonic() - beginning <= 90 and not self.stop.is_set(), "SENDER_SESSION_TIMEOUT")
                        require(len(request) < 8192, "SENDER_HEADERS_BOUND")
                        chunk = connection.recv(min(1024, 8192 - len(request)))
                        require(chunk, "SENDER_REQUEST_TRUNCATED")
                        request += chunk
                    number = self.count()
                    path = "/v1/catalog" if number == 0 else "/v1/bundle/" + self.digest
                    expected = ("GET " + path + " HTTP/1.1\r\nHost: 127.0.0.1:" + str(LIMITS["port"])
                                + "\r\nConnection: close\r\n\r\n").encode("ascii")
                    require(request == expected, "EXACT_SENDER_REQUEST")
                    body = self.catalog if number == 0 else self.bundle
                    media = "application/json" if number == 0 else "application/octet-stream"
                    header = ("HTTP/1.1 200 OK\r\nContent-Length: " + str(len(body))
                              + "\r\nContent-Type: " + media + "\r\nConnection: close\r\n\r\n").encode("ascii")
                    row = {"path": path, "request_sha256": hashlib.sha256(request).hexdigest(),
                           "body_sha256": hashlib.sha256(body).hexdigest(), "body_bytes": len(body),
                           "start_offset": self.offset(), "body_bytes_sent": 0, "progress_offsets": []}
                    with self.lock:
                        self.record["charged_bytes"] += len(header) + len(body)
                        require(self.record["charged_bytes"] <= 4 * MIB, "SENDER_BYTE_GRANT")
                        self.record["connections"].append(row)
                    connection.sendall(header)
                    if number == 1:
                        prefix = len(body) - 64
                        connection.sendall(body[:prefix])
                        row["body_bytes_sent"] = prefix
                        row["progress_offsets"].append(self.offset())
                        for index in range(prefix, len(body)):
                            if self.stop.wait(0.25):
                                break
                            require(time.monotonic() - beginning <= 90, "SENDER_SESSION_TIMEOUT")
                            try:
                                connection.sendall(body[index:index + 1])
                            except OSError as error:
                                row["client_disconnect"] = type(error).__name__
                                break
                            row["body_bytes_sent"] += 1
                            row["progress_offsets"].append(self.offset())
                        row["finish_offset"] = self.offset()
                        self.slow_done.set()
                    else:
                        connection.sendall(body)
                        row["body_bytes_sent"] = len(body)
                        row["finish_offset"] = self.offset()
                self.connection = None
                self.record["closed_connections"] += 1
        except BaseException as error:
            self.record["errors"].append(type(error).__name__ + ":" + str(error)[:512])
        finally:
            if self.connection is not None:
                self.connection.close()
                self.connection = None
            if self.listener is not None:
                self.listener.close()
                self.listener = None
                self.record["closed_listener"] = True
            self.record["finish_offset"] = self.offset()
            self.ready.set()
            self.slow_done.set()

    def shutdown(self):
        self.stop.set()
        # Force a blocked trusted socket read/send to become bounded cleanup.
        for selected in (self.connection, self.listener):
            if selected is not None:
                try:
                    selected.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                selected.close()
        self.thread.join(timeout=5)
        self.record["joined"] = not self.thread.is_alive()
        return self.record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", required=True, type=Path)
    args = parser.parse_args()
    require(os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_site and sys.flags.no_user_site, "WINDOWS_PYTHON_PROFILE")
    started, cpu_started = time.monotonic(), time.process_time()
    helper, sender, owned = None, None, False
    jobs, job_cpu, calls = set(), 0.0, []
    result = {"scope": "genuine native-free acquisition interruption recovery on one fresh receiver",
              "cpu_complete": False, "support_build_stages": 0, "native_stages": 0,
              "direct_supervised_calls": 0, "public_cli_calls": 0,
              "unmetered_cpu": "direct CLI wrappers and Jobs without authenticated final receipt",
              "coordinator_containment": "cooperative trusted process/thread; no outer OS CPU/memory Job"}

    def observations():
        return {"active_wall_seconds": time.monotonic() - started,
                "coordinator_and_sender_cpu_seconds": time.process_time() - cpu_started,
                "observed_job_cpu_seconds": job_cpu,
                "observed_cpu_seconds": time.process_time() - cpu_started + job_cpu, "cpu_complete": False}

    def budget():
        now = observations()
        require(now["active_wall_seconds"] < 1800 and now["observed_cpu_seconds"] < 1800, "AGGREGATE_LIMIT")
        return 1800 - now["active_wall_seconds"]

    def exact(left, right):
        return helper.encode(left) == helper.encode(right)

    def pinned(pin, bound=16 * MIB):
        actual = helper.checked(pin, bound)
        return helper.parse(helper.read(actual["path"], bound))

    def account(path, receipt):
        nonlocal job_cpu
        path = str(helper.safe(path))
        require(path not in jobs, "DUPLICATE_JOB")
        value = receipt["final_job"]["cpu_seconds"]
        require(type(value) in (float, int) and math.isfinite(value) and value >= 0, "JOB_CPU")
        jobs.add(path)
        job_cpu += value

    def quiescent(receipt):
        require(receipt.get("direct_child_reaped") is True and receipt.get("final_active_zero") is True
                and receipt.get("job_closed") is True and receipt.get("attach_resume_returned") is True
                and type(receipt["final_job"]["active_processes"]) is int
                and receipt["final_job"]["active_processes"] == 0
                and receipt.get("cleanup_errors", []) == [], "ACTUAL_JOB_QUIESCENCE_REQUIRED")

    def cli(name, argv, cwd, maximum=500):
        require(len(calls) < 11, "CLI_COUNT")
        directory = RUN / "commands" / name
        directory.mkdir(exist_ok=False)
        record = {"name": name, "argv": argv, "cwd": str(cwd), "shell": False,
                  "timeout_seconds": min(maximum, budget()), "descendant_quiescence": "UNBOUND"}
        calls.append(record)
        result["public_cli_calls"] = len(calls)
        helper.save(directory / "command.json", record)
        process, begin = None, time.monotonic()
        stdout, stderr = directory / "stdout.txt", directory / "stderr.txt"
        try:
            with stdout.open("xb") as out, stderr.open("xb") as err:
                process = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                    shell=False, close_fds=True, creationflags=subprocess.CREATE_NO_WINDOW)
                record["pid"] = process.pid
                while process.poll() is None:
                    budget()
                    require(time.monotonic() - begin <= record["timeout_seconds"], "CLI_TIMEOUT")
                    require(stdout.stat().st_size <= 2 * MIB and stderr.stat().st_size <= MIB, "CLI_OUTPUT_BOUND")
                    time.sleep(0.05)
                record["returncode"] = process.wait(timeout=5)
                record["direct_child_reaped"] = True
        except BaseException as error:
            record["transport_error"] = type(error).__name__ + ":" + str(error)[:512]
            if process is not None:
                try:
                    if process.poll() is None:
                        process.kill()
                    record["returncode"] = process.wait(timeout=15)
                    record["direct_child_reaped"] = True
                except (OSError, subprocess.TimeoutExpired):
                    record["direct_child_reaped"] = False
            record["descendant_quiescence"] = "UNCONFIRMED; inspect retained inner Job receipt"
        raw = None
        try:
            record["stdout"], record["stderr"] = helper.pin(stdout, 2 * MIB), helper.pin(stderr, MIB)
            raw = helper.read(stdout, 2 * MIB)
        except BaseException as error:
            record["capture_error"] = type(error).__name__ + ":" + str(error)[:512]
        record["elapsed_seconds"] = time.monotonic() - begin
        helper.save(directory / "result.json", record)
        # Return raw failure outcomes too; available inner evidence is bound
        # before the caller judges transport status, JSON framing or workload.
        return raw, record, directory

    def frame(raw, record):
        require("transport_error" not in record and "capture_error" not in record
                and record.get("returncode") == 0 and type(raw) is bytes
                and raw.endswith(b"\n") and raw.count(b"\n") == 1, "CLI_TRANSPORT_FRAME")
        reply = helper.parse(raw)
        require(type(reply) is dict, "CLI_RESPONSE_OBJECT")
        return reply

    def bind(case, raw, record, directory, recovery=False, interrupted=False):
        case = helper.safe(case, directory=True)
        path = case / "supervisor.json"
        receipt = helper.parse(helper.read(path, 65536))
        require(receipt.get("schema") == 1 and receipt.get("name") == case.name
                and receipt.get("native_acceptance") is False
                and receipt.get("status") in {"TRANSPORT_COMPLETE", "TRANSPORT_NONZERO_EXIT", "TRANSPORT_FAILED"},
                "SUPERVISOR_ORIGIN_PROFILE")
        for item in copied:
            helper.checked(item)
        helper.checked(configured["config"])
        expected_pins = [helper.pin(sys.executable), helper.pin(state / "config.json"),
                         *[helper.pin(installation / "py" / (name + ".py")) for name in ORDINARY_NAMES]]
        expected_limits = {"wall_seconds": 450, "cpu_seconds": 450, "memory_mib": 6144,
            "active_processes": 8, "stdout_bytes": MIB, "stderr_bytes": 65536, "event_bytes": 65536,
            "request_bytes": 131072, "poll_seconds": 0.05, "settle_seconds": 15}
        if helper.parse(raw)["op"] in {"peer_find", "peer_acquire", "expose"}:
            expected_limits.update(wall_seconds=120, cpu_seconds=120, memory_mib=1024)
        worker = installation / "py" / ("recovery_worker.py" if recovery else "node.py")
        if recovery:
            require(case.name == "recover" and case.parent.name == "cases"
                    and case.parent.parent.parent == scratch / "recoveries", "RECOVERY_CASE_DOMAIN")
            selected = helper.parse(raw)["args"]
            original_pin = helper.pin(selected["supervisor_receipt"], 65536)
            expected_pins.extend([helper.pin(worker), helper.pin(installation / "py/recovery_manage.py"),
                                  original_pin, helper.pin(installation / "manage.py")])
            grant_path = case.parent.parent / "grant.json"
            grant = helper.parse(helper.read(grant_path, 65536))
            expected_grant = {"schema": 1, "profile": "draft-owner-recovery-supervision-v1",
                "request_sha256": hashlib.sha256(raw).hexdigest(), "target_client": selected["client"],
                "target_request_id": selected["request_id"], "original_receipt": original_pin,
                "worker": str(worker), "state": str(state), "limits": RECOVERY_LIMITS,
                "inputs": expected_pins,
                "policy": "one explicit invocation; no automatic retries, quota reset, refunds or repair",
                "close_evidence": "CHECKED_CLOSEHANDLE_RETURN; final active-zero and child reap required independently"}
            require(exact(grant, expected_grant), "RECOVERY_GRANT_IDENTITY")
            expected_pins.append(helper.pin(grant_path, 65536))
            expected_limits = RECOVERY_LIMITS
        else:
            require(case.parent == scratch / "calls", "ORDINARY_CASE_DOMAIN")
        require(exact(receipt["pins"], expected_pins) and receipt["bound_pin_count"] == len(expected_pins)
                and receipt["bound_pin_bytes"] == sum(item["bytes"] for item in expected_pins)
                and exact(receipt["limits"], expected_limits)
                and receipt["wall_limit_seconds"] == (10 if interrupted else expected_limits["wall_seconds"]),
                "SUPERVISOR_SOURCE_AND_GRANT_IDENTITY")
        rows = receipt["files"]
        require(type(rows) is dict and set(rows) == {"request.json", "command.json", "stdout.txt", "stderr.txt", "event.json"},
                "SUPERVISOR_FILE_SET")
        for name, maximum in (("request.json", 131072), ("command.json", 65536),
                              ("stdout.txt", MIB), ("stderr.txt", 65536), ("event.json", 65536)):
            selected_file = case / name
            if selected_file.exists():
                selected_bytes = helper.read(selected_file, maximum)
                require(exact(rows[name], {"present": True, "bytes": len(selected_bytes),
                        "sha256": hashlib.sha256(selected_bytes).hexdigest()}), "SUPERVISOR_FILE_METADATA")
            else:
                require(exact(rows[name], {"present": False}), "SUPERVISOR_ABSENT_FILE_METADATA")
        command = helper.parse(helper.read(case / "command.json", 65536))
        expected_command = {"argv": [str(Path(sys.executable).resolve()), *FLAGS, str(worker),
            "--config", str(state / "config.json"), "--state", str(state),
            "--request", str(case / "request.json"), "--event", str(case / "event.json")],
            "cwd": str(installation / "py"), "shell": False, "creationflags": 134217732,
            "environment_override": {"PYTHONDONTWRITEBYTECODE": "1"}}
        require(exact(command, expected_command), "SUPERVISOR_COMMAND_IDENTITY")
        require(receipt["request_sha256"] == hashlib.sha256(raw).hexdigest()
                and helper.read(case / "request.json", 131072) == raw, "REQUEST_BINDING")
        account(path, receipt)
        event = None
        value = {"supervisor": helper.pin(path), "request_sha256": hashlib.sha256(raw).hexdigest(),
                 "event": None, "quiescent": False, "native_stages": None,
                 "source_pin_count": len(expected_pins), "cpu_accounted": True}
        record["actual_observation"] = value
        try:
            require("output_record_error" not in receipt and "evidence_persistence_error" not in receipt,
                    "SUPERVISOR_EVIDENCE_UNCERTAIN")
            quiescent(receipt)
            value["quiescent"] = True
            record["descendant_quiescence"] = "OBSERVED_BOUND_JOB_ACTIVE_ZERO_AND_DIRECT_REAP"
            if (case / "event.json").exists():
                event = helper.parse(helper.read(case / "event.json", 65536))
                require(event["request_sha256"] == hashlib.sha256(raw).hexdigest()
                        and event["response_sha256"] == hashlib.sha256(helper.read(case / "stdout.txt", MIB)).hexdigest(),
                        "EVENT_IO_BINDING")
                if not recovery:
                    require(event["origin_directory"] == str(case), "ORIGINAL_CALL_ORIGIN")
                count = event["stages_allocated"]
                require(type(count) is int and count >= 0, "ACTUAL_STAGE_COUNT_TYPE")
                result["native_stages"] += count
                value.update(event=helper.pin(case / "event.json"), native_stages=count)
        finally:
            # Binding survives unexpected workload, public framing, quiescence
            # and aggregate-limit outcomes; no expected success is needed here.
            record["binding"] = helper.save(directory / "binding.json", value)
        return value, receipt, event

    def public(name, raw, mode="request"):
        path = RUN / "requests" / (name + ".json")
        helper.save_raw(path, raw)
        parent = scratch / ("calls" if mode == "request" else "recoveries")
        before = set(parent.iterdir()) if parent.exists() else set()
        response_raw, record, directory = cli(name, [str(Path(sys.executable).resolve()), *FLAGS,
            str(installation / "manage.py"), mode, "--config", str(state / "config.json"),
            "--request", str(path)], installation, 500 if name == "init" else 150)
        added = (set(parent.iterdir()) if parent.exists() else set()) - before
        require(len(added) == 1, "ACTUAL_CASE_COUNT")
        case = helper.safe(added.pop(), directory=True)
        if mode == "recover":
            case = case / "cases/recover"
        value, receipt, event = bind(case, raw, record, directory, mode == "recover")
        reply = frame(response_raw, record)
        record["public_status"], record["public_code"] = reply.get("status"), reply.get("code")
        require(receipt["status"] == "TRANSPORT_COMPLETE" and receipt["returncode"] == 0 and event is not None
                and helper.read(case / "stdout.txt", MIB) == response_raw, "PUBLIC_RESPONSE_BINDING")
        require(value["native_stages"] <= 1, "ACTUAL_STAGE_COUNT")
        if mode == "recover":
            require(event["checker_loaded"] is False and event["native_stages"] == 0
                    and event["mathematical_acceptance_authority"] is False, "RECOVERY_IS_NOT_ACCEPTANCE")
        budget()
        return reply, response_raw, case, event

    def req(identity, op, arguments, client="local"):
        return helper.encode({"client": client, "request_id": identity, "op": op, "args": arguments})

    def recover(name, identity, original):
        raw = helper.encode({"op": "recover_peer", "client": "owner", "args": {
            "client": "local", "request_id": identity, "supervisor_receipt": str(original / "supervisor.json")}})
        return public(name, raw, "recover")

    def observe_build(work, record, directory):
        request = work / "scratch/support-build"
        stage_dir = request / "stage-build"
        path = stage_dir / "stage.json"
        if not path.exists():
            record["build_observation"] = "UNBOUND; no stage receipt available"
            return None
        stage = helper.parse(helper.read(path, MIB))
        domain_pin = helper.pin(installation / "py/domains.py")
        runner_pin = helper.pin(installation / "py/run_stage.py")
        native_sources = {name: helper.pin(installation / "native" / (name + ".lean"))
                          for name in ("BootstrapSupport", "AgentReplayCore", "AgentClient")}
        domains = {"install": str(installation), "state": str(work / "reserved-state"),
                   "scratch": str(work / "scratch"), "lean_runtime": str(runtime)}
        expected = {"schema": 2, "domains": domains, "domains_source": domain_pin,
            "request_directory": str(request), "stage_directory": str(stage_dir), "stage": "support-build",
            "expected_runner_sha256": runner_pin["sha256"], "lean": helper.pin(runtime / "bin/lean.exe"),
            "python": helper.pin(sys.executable), "seconds": 300, "memory_mib": 4096, "bytes": 128 * MIB,
            "inputs": [{**domain_pin, "as": "domains.py"}, *[
                {**pin, "as": "native/" + name + ".lean"} for name, pin in native_sources.items()]],
            "output_directories": ["lib"], "steps": [
                {"kind": "lean", "label": "build-" + name, "cwd": "$RUN/input/native",
                 "lean_path": ["$RUN/out/lib"], "expected_exit": 0,
                 "argv": ["-R", "$RUN/input/native", "-o", "$RUN/out/lib/" + name + ".olean",
                          "$RUN/input/native/" + name + ".lean"]}
                for name in ("BootstrapSupport", "AgentReplayCore")]}
        plan_path = request / "build-plan.json"
        plan_raw = helper.read(plan_path, MIB)
        require(exact(helper.parse(plan_raw), expected) and helper.read(stage_dir / "plan.json", MIB) == plan_raw
                and stage["stage"] == "support-build" and exact(stage["domains"], domains)
                and stage["request_directory"] == str(request) and stage["accounting_root"] == str(stage_dir)
                and stage["expected_plan_sha256"] == hashlib.sha256(plan_raw).hexdigest()
                and exact(stage["plan"], helper.pin(stage_dir / "plan.json"))
                and exact(stage["lean"], expected["lean"]) and exact(stage["python"], expected["python"]),
                "BUILD_STAGE_ORIGIN")
        runner_snapshot = helper.pin(stage_dir / "run_stage.py")
        require(exact(stage["runner"], runner_snapshot) and runner_snapshot["bytes"] == runner_pin["bytes"]
                and runner_snapshot["sha256"] == runner_pin["sha256"], "BUILD_RUNNER_BINDING")
        for item in copied:
            helper.checked(item)
        value = {"stage": helper.pin(path), "plan": helper.pin(plan_path),
                 "status": stage["status"], "quiescent": False, "cpu_accounted": False,
                 "observed_children": len(stage.get("steps", []))}
        record["actual_observation"] = value
        result["support_build_stages"] += 1
        try:
            account(path, stage)
            value["cpu_accounted"] = True
            require(stage["execution_endpoint"]["children_quiescent"] is True
                    and type(stage["final_job"]["active_processes"]) is int
                    and stage["final_job"]["active_processes"] == 0
                    and "cleanup_error" not in stage, "BUILD_ACTUAL_QUIESCENCE")
            value["quiescent"] = True
            record["descendant_quiescence"] = "OBSERVED_BOUND_BUILD_STAGE"
        finally:
            record["binding"] = helper.save(directory / "binding.json", value)
        return stage

    def snapshot(name):
        # Called only between completed/reaped workers. No active product
        # process or fixture thread accesses this DB; owner stability is assumed.
        database = helper.safe(state / "control.sqlite3")
        for suffix in ("-journal", "-wal", "-shm"):
            path = Path(str(database) + suffix)
            require(not path.exists() or path.stat().st_size == 0, "NONEMPTY_SIDECAR_OUTSIDE_PROFILE")
        require(sqlite3.sqlite_version == "3.50.4", "SQLITE_PROFILE")
        connection = sqlite3.connect(database.as_uri() + "?mode=ro&immutable=1", uri=True, timeout=0)
        connection.row_factory = sqlite3.Row
        steps = 0
        def progress():
            nonlocal steps
            steps += 1
            return int(steps >= 100000)
        connection.set_progress_handler(progress, 1)
        try:
            connection.execute("PRAGMA query_only=ON")
            value = {}
            for table, order in TABLES.items():
                cursor = connection.execute("SELECT * FROM " + table + " ORDER BY " + order)
                rows = cursor.fetchmany(8193)
                require(len(rows) <= 8192, "READONLY_ROWS_BOUND")
                value[table] = [{key: {"hex": item.hex()} if type(item) is bytes else item
                                 for key, item in dict(row).items()} for row in rows]
            require(len(helper.encode(value)) <= 4 * MIB, "READONLY_SNAPSHOT_BOUND")
        finally:
            connection.close()
        helper.save(RUN / "snapshots" / (name + ".json"), {"ledger": value, "sql_vm_steps": steps,
            "authority": "readonly observation after worker quiescence; never promotion or fabricated state"})
        return value

    def same_ledger(left, right, code):
        require(exact(left, right), code)

    try:
        launch_raw = bootstrap_read(args.launch, MIB)
        launch = strict(launch_raw)
        require(type(launch) is dict and set(launch) == {"schema", "coordinator", "helper", "python", "source_files",
            "shared_runtime", "fixture", "limits"} and type(launch["schema"]) is int and launch["schema"] == 1
            and launch["limits"] == LIMITS, "LAUNCH_FIELDS")
        bootstrap_pin(launch["coordinator"], __file__)
        bootstrap_pin(launch["python"], sys.executable)
        bootstrap_pin(launch["helper"], SOURCE / "tests/prepare_peers.py")
        spec = importlib.util.spec_from_file_location("reviewed_recovery_file_helpers", launch["helper"]["path"])
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        sources = launch["source_files"]
        require(type(sources) is list and 1 <= len(sources) <= 512
                and [helper.safe(item["path"]) for item in sources] == helper.product_sources(budget), "EXACT_NEW_SOURCE_CUT")
        require(sum(item["bytes"] for item in sources) <= 64 * MIB, "SOURCE_TOTAL_BOUND")
        for item in sources:
            helper.checked(item)
        runtime = helper.safe(launch["shared_runtime"]["path"], directory=True)
        helper.checked(launch["shared_runtime"]["lean"])
        require(helper.safe(launch["shared_runtime"]["lean"]["path"]) == runtime / "bin/lean.exe", "RUNTIME_PIN")
        fixture = launch["fixture"]
        require(type(fixture) is dict and set(fixture) == {"g02", "catalog", "bundle", "complete"}, "FIXTURE_FIELDS")
        g02 = pinned(fixture["g02"])
        require(g02["schema"] == 2 and g02["attempt"] == "g02" and g02["phase"] == "g_to_beta"
                and g02["status"] == "G_OFFLINE_ADMITTED_BY_BETA_AWAITING_INDEPENDENT_H_AUTHORING",
                "REAL_G02_PUBLICATION_REQUIRED")
        exposure, publication = pinned(g02["exposure"]["response"]), pinned(g02["publication"]["response"])
        exposure_request = pinned(g02["exposure"]["request"])
        fixture_key = hashlib.sha256(helper.encode([exposure_request["client"], exposure_request["request_id"]])).hexdigest()
        view = PROJECT / "product-local/peer-01/alpha/state/work" / fixture_key / "peer-view"
        for name in ("catalog", "bundle", "complete"):
            helper.checked(fixture[name], MIB)
        require(helper.safe(fixture["catalog"]["path"]) == view / "catalog.json"
                and helper.safe(fixture["complete"]["path"]) == view / "complete.json", "REAL_EXPOSED_VIEW_PATH")
        catalog_raw = helper.read(fixture["catalog"]["path"], 65536)
        catalog = helper.parse(catalog_raw)
        require(len(catalog["entries"]) == 1 and exposure["entries"] == 1
                and exposure["catalog_sha256"] == hashlib.sha256(catalog_raw).hexdigest()
                and exact(catalog["entries"][0]["descriptor_id"], publication["descriptor_id"]), "REAL_CATALOG_BINDING")
        entry = catalog["entries"][0]
        require(helper.safe(fixture["bundle"]["path"]) == view / "bundles" / (entry["bundle_sha256"] + ".bundle"), "BUNDLE_PATH")
        bundle = helper.read(fixture["bundle"]["path"], MIB)
        require(hashlib.sha256(bundle).hexdigest() == entry["bundle_sha256"] and len(bundle) == entry["bundle_bytes"], "BUNDLE_PIN")
        completion = pinned(fixture["complete"])
        require(exact(completion, {"schema": 1, "foundation": catalog["foundation"],
                                  "catalog_sha256": hashlib.sha256(catalog_raw).hexdigest()}), "VIEW_COMPLETION")
        magic = b"DTMKN-PEER-BUNDLE-1\n"
        require(bundle.startswith(magic) and len(bundle) > len(magic) + 4, "BUNDLE_FRAMING")
        manifest_length = int.from_bytes(bundle[len(magic):len(magic) + 4], "big")
        start = len(magic) + 4
        require(0 < manifest_length <= MIB and start + manifest_length + 8 < len(bundle) - 64,
                "FIXTURE_NEEDS_64_TRAILING_BODY_BYTES")
        require(hashlib.sha256(bundle[start:start + manifest_length]).hexdigest() == entry["manifest_sha256"], "EMBEDDED_MANIFEST_PIN")
        require(not RUN.exists() and not DATA.exists(), "FRESH_RECOVERY_ROOTS_REQUIRED")
        helper.safe(RUN.parent, directory=True)
        helper.safe(DATA.parent, directory=True)
        RUN.mkdir(exist_ok=False)
        owned = True
        DATA.mkdir(exist_ok=False)
        for name in ("commands", "requests", "snapshots", "fixture"):
            (RUN / name).mkdir()
        result["launch"] = helper.save_raw(RUN / "launch.json", launch_raw)
        result["coordinator"] = helper.save_raw(RUN / "coordinator.py", helper.read(__file__, MIB))
        result["catalog"] = helper.save_raw(RUN / "fixture/catalog.json", catalog_raw)
        result["bundle"] = helper.save_raw(RUN / "fixture/bundle.bin", bundle)
        result["fixture_lineage"] = fixture
        installation, state, scratch = DATA / "install", DATA / "state", DATA / "scratch"
        installation.mkdir()
        copied = []
        for item in sources:
            source = helper.safe(item["path"])
            target = installation / source.relative_to(SOURCE)
            target.parent.mkdir(parents=True, exist_ok=True)
            actual = helper.save_raw(target, helper.read(source, 16 * MIB))
            require(actual["bytes"] == item["bytes"] and actual["sha256"] == item["sha256"].lower(), "SOURCE_COPY")
            copied.append(actual)
        require((installation / "py/recovery_worker.py").is_file() and (installation / "py/recovery_manage.py").is_file(),
                "RECOVERY_CAPABLE_CUT_REQUIRED")
        result["installed_sources"] = helper.save(RUN / "installed-source-pins.json", copied)
        build_work = DATA / "build-work"
        build_raw, build_call, build_directory = cli("build", [str(Path(sys.executable).resolve()), *FLAGS, str(installation / "build.py"),
            "--lean-runtime", str(runtime), "--work", str(build_work)], installation)
        stage = observe_build(build_work, build_call, build_directory)
        built = frame(build_raw, build_call)
        require(built["status"] == "LOCAL_SUPPORT_BUILD_COMPLETED_NOT_MATH_ACCEPTANCE", "BUILD_STATUS")
        build_receipt = pinned(built["receipt"])
        require(exact(build_receipt["stage_receipt"], helper.pin(build_work / "scratch/support-build/stage-build/stage.json"))
                and stage is not None, "BUILD_RECEIPT_BINDING")
        require(stage["status"] == "STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE" and len(stage["steps"]) == 2
                and all(step["exit_code"] == 0 for step in stage["steps"])
                and stage["execution_endpoint"]["children_quiescent"] is True
                and stage["final_job"]["active_processes"] == 0, "BUILD_QUIESCENCE")
        budget()
        configure_raw, configure_call, _ = cli("configure", [str(Path(sys.executable).resolve()), *FLAGS,
            str(installation / "manage.py"), "configure", "--state", str(state), "--scratch", str(scratch),
            "--lean-runtime", str(runtime), "--client", "local", "--peer", "other=43173"], installation)
        configured = frame(configure_raw, configure_call)
        require(configured["status"] == "CONFIGURED_NOT_INITIALIZED" and configured["acceptance"] is False, "CONFIGURE_STATUS")
        config = pinned(configured["config"])
        require(helper.safe(configured["config"]["path"]) == state / "config.json" and config["offers"] == []
                and config["clients"] == ["local"] and config["peers"] == {"other": {"host": "127.0.0.1", "port": 43173}}
                and exact(config["domains"], {"install": str(installation), "state": str(state),
                    "scratch": str(scratch), "lean_runtime": str(runtime)}), "NEW_RECEIVER_CONFIG")
        initialized, _, _, init_event = public("init", req("recovery-init", "init", {}, "owner"))
        require(initialized.get("accepted") is True and init_event["stages_allocated"] == 1
                and exact(initialized["description"]["foundation"], catalog["foundation"]), "BOOTSTRAP_BINDING")
        baseline = snapshot("initialized")
        require(len(baseline["stages"]) == 1 and baseline["entries"] == [] and baseline["meta"][0]["active"] is None,
                "FRESH_EMPTY_RECEIVER")
        # Only these two pinned installed modules are executed by the test
        # coordinator for the one intentional tighter ordinary-call grant.
        sys.path.insert(0, str(installation / "py"))
        runner, supervisor = importlib.import_module("run_stage"), importlib.import_module("supervise")
        for module, name in ((runner, "run_stage.py"), (supervisor, "supervise.py")):
            require(Path(module.__file__).resolve() == installation / "py" / name, "INSTALLED_SUPERVISOR_MODULE")
        ordinary_pins = [helper.pin(sys.executable), helper.pin(state / "config.json"),
                         *[helper.pin(installation / "py" / (name + ".py")) for name in ORDINARY_NAMES]]
        sender = FaultSender(catalog_raw, bundle, entry["bundle_sha256"], started)
        sender.thread.start()
        require(sender.ready.wait(timeout=5) and not sender.record["errors"] and sender.listener is not None, "SENDER_READY")
        found, _, _, _ = public("peer-find", req("recovery-find", "peer_find", {"peer": "other"}))
        require(found["status"] == "OK" and found["mathematicalAcceptance"] is False and len(found["rows"]) == 1
                and exact(found["rows"][0]["descriptor_id"], entry["descriptor_id"]), "REAL_REMOTE_SELECTION")
        before = snapshot("before-interruption")
        interrupted_raw = req("recovery-interrupted", "peer_acquire", {"remote": found["rows"][0]["remote"]})
        helper.save_raw(RUN / "requests/interrupted.json", interrupted_raw)
        case_name = "recovery-original"
        limits = {"pins": ordinary_pins, "wall_seconds": 120, "cpu_seconds": 120, "memory_mib": 1024,
                  "active_processes": 8, "stdout_bytes": MIB, "stderr_bytes": 65536, "event_bytes": 65536,
                  "case_seconds": {case_name: 10}}
        helper.save(RUN / "interruption-grant.json", {"limits": limits, "request_sha256": hashlib.sha256(interrupted_raw).hexdigest(),
            "scope": "unchanged ordinary node command, one test-only tighter wall deadline"})
        transport = supervisor.Transport(sys.executable, installation / "py/node.py", state / "config.json", state,
                                         scratch / "calls", runner, limits)
        interruption_start = time.monotonic() - started
        result["direct_supervised_calls"] = 1
        direct_directory = RUN / "commands/direct-interruption"
        direct_directory.mkdir(exist_ok=False)
        direct_record = {"name": case_name, "descendant_quiescence": "UNBOUND"}
        result["direct_original_call"] = direct_record
        interrupted = False
        try:
            completed = transport(case_name, interrupted_raw)
            direct_record["returned_stdout"] = helper.save_raw(direct_directory / "returned-stdout.txt", completed["stdout"])
            direct_record["returned_event"] = helper.save(direct_directory / "returned-event.json", completed["event"])
        except supervisor.SupervisorFailure as error:
            interrupted = True
            direct_record["transport_failure"] = str(error)[:512]
        original = scratch / "calls" / case_name
        original_binding, original_receipt, _ = bind(original, interrupted_raw, direct_record, direct_directory, interrupted=True)
        result["original_interruption"] = original_binding
        require(interrupted, "INCONCLUSIVE_ORIGINAL_CALL_DID_NOT_INTERRUPT")
        budget()
        require(original_receipt["status"] == "TRANSPORT_FAILED" and original_receipt["wall_limit_seconds"] == 10
                and original_receipt["failure"]["detail"] == "PUBLIC_WALL_LIMIT"
                and original_receipt["job_termination_requested"] is True and original_receipt["returncode"] != 0,
                "REAL_SUPERVISOR_DEADLINE_REQUIRED")
        require(sender.slow_done.wait(timeout=3) and not sender.record["errors"] and sender.count() == 2, "SLOW_SENDER_DISCONNECT")
        slow = sender.record["connections"][1]
        require(interruption_start <= slow["start_offset"] and len(slow["progress_offsets"]) >= 2
                and 0 < slow["body_bytes_sent"] < len(bundle) and "client_disconnect" in slow,
                "REAL_PARTIAL_TRANSFER_REQUIRED")
        pending = snapshot("pending-original")
        key = hashlib.sha256(helper.encode(["local", "recovery-interrupted"])).hexdigest()
        request_row = [row for row in pending["requests"] if row["key"] == key]
        require(len(request_row) == 1 and request_row[0]["phase"] == "pending" and request_row[0]["response"] is None
                and request_row[0]["raw"] == {"hex": interrupted_raw.hex()} and pending["meta"][0]["active"] == key,
                "GENUINE_PENDING_LEDGER_REQUIRED")
        marker_raw = helper.encode({"config": hashlib.sha256(helper.read(state / "config.json", 131072)).hexdigest(),
            "kind": "attempt", "client": "owner", "data": {"request": key, "call_directory": str(original)}})
        marker = {"handle": "attempt:" + hashlib.sha256(marker_raw).hexdigest(), "kind": "attempt",
                  "client": "owner", "raw": {"hex": marker_raw.hex()}}
        require(marker in pending["records"], "REAL_ORIGINAL_ATTEMPT_MARKER")
        expected_pending = helper.parse(helper.encode(before))
        expected_pending["requests"] = sorted(before["requests"] + request_row, key=lambda row: row["key"])
        expected_pending["records"] = sorted(before["records"] + [marker], key=lambda row: row["handle"])
        expected_pending["meta"][0].update(active=key, requests=before["meta"][0]["requests"] + 1,
                                          charged=before["meta"][0]["charged"] + 64 * MIB)
        same_ledger(pending, expected_pending, "INTERRUPTION_CHANGED_VISIBILITY_OR_CHARGES")
        original_binding["native_stages"] = 0
        original_binding["native_stage_basis"] = "post-quiescence readonly ledger equals prior stages; no interrupted-request stage exists"
        partial = state / "work" / key
        partial_before = helper.census(partial, budget, hashes=True)
        require(partial_before["files"] > 0, "REAL_PARTIAL_FILES_REQUIRED")
        helper.save(RUN / "partial-files-before.json", partial_before)
        retry, _, retry_case, _ = public("identical-pending-retry", interrupted_raw)
        require(retry["status"] == "BLOCKED" and retry["code"] == "PENDING_EXECUTION" and retry_case != original,
                "ACTUAL_IDENTICAL_RETRY")
        same_ledger(snapshot("after-pending-retry"), pending, "RETRY_MUST_NOT_RESERVE")
        refused, _, _, refusal_event = recover("reject-retry-receipt", "recovery-interrupted", retry_case)
        require(refused["status"] == "BLOCKED" and refused["code"] == "RECOVERY_ORIGINAL_ATTEMPT_NOT_BOUND"
                and refusal_event["transition_committed"] is False, "RETRY_RECEIPT_SUBSTITUTION_NOT_REJECTED")
        same_ledger(snapshot("after-wrong-receipt"), pending, "WRONG_RECEIPT_CHANGED_LEDGER")
        require(sender.count() == 2, "RETRY_OR_RECOVERY_TOUCHED_SOCKET")
        interrupted_reply = helper.encode({"status": "REFUSED", "code": "INTERRUPTED_PEER_OPERATION"})
        _, recovered_raw, _, recovery_event = recover("recover-original", "recovery-interrupted", original)
        require(recovered_raw == interrupted_reply and recovery_event["transition_committed"] is True
                and recovery_event["historical"] is False and recovery_event["quiescence_authenticated"] is True,
                "ORIGINAL_RECOVERY_RESULT")
        recovered = snapshot("recovered")
        expected_recovered = helper.parse(helper.encode(pending))
        expected_recovered["meta"][0]["active"] = None
        for row in expected_recovered["requests"]:
            if row["key"] == key:
                row.update(phase="terminal", response={"hex": interrupted_reply.hex()})
        same_ledger(recovered, expected_recovered, "RECOVERY_CHANGED_MORE_THAN_TERMINAL_ACTIVE")
        _, replayed_raw, _, replay_event = public("ordinary-terminal-replay", interrupted_raw)
        require(replayed_raw == interrupted_reply and replay_event["historical"] is True, "ORDINARY_EXACT_REPLAY")
        same_ledger(snapshot("after-ordinary-replay"), recovered, "ORDINARY_REPLAY_CHANGED_LEDGER")
        _, repeated_raw, _, repeat_event = recover("recovery-terminal-replay", "recovery-interrupted", original)
        require(repeated_raw == interrupted_reply and repeat_event["historical"] is True
                and repeat_event["transition_committed"] is False, "RECOVERY_EXACT_REPLAY")
        same_ledger(snapshot("after-recovery-replay"), recovered, "RECOVERY_REPLAY_CHANGED_LEDGER")
        require(sender.count() == 2, "REPLAY_TOUCHED_SOCKET")
        fresh, fresh_raw, fresh_case, fresh_event = public("fresh-acquisition",
            req("recovery-fresh", "peer_acquire", {"remote": found["rows"][0]["remote"]}))
        require(fresh["status"] == "OK" and fresh["candidate_only"] is True and fresh["mathematicalAcceptance"] is False
                and fresh["existing"] is False and fresh["native_stages"] == 0 and fresh_event["stages_allocated"] == 0
                and exact(fresh["descriptor_id"], entry["descriptor_id"]), "FRESH_NORMAL_ACQUISITION_REQUIRED")
        sender.thread.join(timeout=5)
        sender_record = sender.shutdown()
        require(sender_record["joined"] is True and sender_record["closed_listener"] is True
                and sender_record["closed_connections"] == 3 and not sender_record["errors"]
                and len(sender_record["connections"]) == 3, "ACTUAL_SENDER_CLOSURE_JOIN")
        result["sender"] = helper.save(RUN / "sender.json", sender_record)
        final_acquired = snapshot("fresh-acquired")
        require(exact(final_acquired["heads"], recovered["heads"]) and exact(final_acquired["stages"], recovered["stages"])
                and len(final_acquired["entries"]) == 1 and final_acquired["providers"][0]["cut"] == 1
                and final_acquired["meta"][0]["active"] is None
                and final_acquired["meta"][0]["requests"] == recovered["meta"][0]["requests"] + 1
                and final_acquired["meta"][0]["charged"] == recovered["meta"][0]["charged"] + 64 * MIB,
                "FRESH_CANDIDATE_WITHOUT_ACCEPTANCE_OR_REFUND")
        _, success_replay, _, success_event = recover("successful-terminal-replay", "recovery-fresh", fresh_case)
        require(success_replay == fresh_raw and success_event["historical"] is True
                and success_event["transition_committed"] is False, "SUCCESSFUL_TERMINAL_BYTES_PRESERVED")
        same_ledger(snapshot("final"), final_acquired, "SUCCESSFUL_REPLAY_CHANGED_LEDGER")
        partial_after = helper.census(partial, budget, hashes=True)
        require(exact(partial_after, partial_before), "RECOVERY_CHANGED_OR_DELETED_PARTIAL_FILES")
        result["partial_files_preserved"] = helper.save(RUN / "partial-files-after.json", partial_after)
        require(len(calls) == 11 and result["direct_supervised_calls"] == 1 and result["native_stages"] == 1
                and result["support_build_stages"] == 1 and len(final_acquired["stages"]) == 1, "EXACT_QUALIFICATION_WORK")
        for item in copied:
            helper.checked(item)
        helper.checked(configured["config"])
        for item in config["files"].values():
            helper.checked(item)
        helper.checked(launch["shared_runtime"]["lean"])
        helper.checked(launch["coordinator"])
        helper.checked(launch["helper"])
        for pin in fixture.values():
            helper.checked(pin)
        data_census, run_census = helper.census(DATA, budget, hashes=True), helper.census(RUN, budget, hashes=True)
        total = data_census["bytes"] + run_census["bytes"]
        require(total < 1024 * MIB - 16 * MIB, "RETAINED_BYTES")
        result["data_seal"] = helper.save(RUN / "data-seal.json", data_census)
        result["evidence_seal"] = helper.save(RUN / "evidence-seal.json", run_census)
        result.update(status="GENUINE_TRANSFER_RECOVERY_SEQUENCE_COMPLETED_AWAITING_INDEPENDENT_AUDIT",
                      compute=observations(), commands=calls, cpu_record_paths=sorted(jobs),
                      native_admissions=0, mathematical_contributions=0,
                      accounting_endpoint="before final report/stdout; runtime and original published fixture tree excluded")
        raw = helper.encode(result)
        require(total + result["data_seal"]["bytes"] + result["evidence_seal"]["bytes"] + len(raw) <= 1024 * MIB,
                "FINAL_RETAINED_BYTES")
        budget()
        receipt = helper.save_raw(RUN / "result.json", raw)
        print(json.dumps({"status": result["status"], "receipt": receipt}))
        return 0
    except BaseException as error:
        if sender is not None:
            try:
                result["sender_failure_observation"] = sender.shutdown()
            except BaseException as cleanup_error:
                result["sender_failure_observation"] = sender.record
                result["sender_cleanup_error"] = type(cleanup_error).__name__ + ":" + str(cleanup_error)[:1024]
        result.update(status="STOPPED_NOT_QUALIFIED", error=type(error).__name__, detail=str(error)[:2048],
                      compute=observations(), commands=calls, cpu_record_paths=sorted(jobs))
        if owned and helper is not None:
            receipt = helper.save(RUN / "failure.json", result)
            print(json.dumps({"status": result["status"], "failure": receipt}))
        else:
            print(json.dumps({"status": "STOPPED_BEFORE_NEW_ROOTS", "detail": str(error)[:2048]}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

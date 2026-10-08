"""DRAFT post-H peer controls. Root alone executes after review/allocation.

Only standard-library code plus authenticated preparation test helpers. No
product imports or database writes. Fault senders are bounded cooperative
threads; public nodes/services retain their own real product supervision.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
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
DATA = SOURCE.parent / "product-local/peer-01"
RUN = SOURCE / "qualification/peer-01-controls"
FLAGS = ["-B", "-E", "-s", "-S"]
MIB = 1048576
MAGIC = b"DTMKN-PEER-BUNDLE-1\n"
LIMITS = {"active_wall_seconds": 900, "observed_cpu_seconds": 900,
          "retained_bytes": 1024 * MIB, "command_seconds": 180,
          "public_commands": 12, "native_stages": 0, "fault_sessions": 4,
          "fault_seconds": 90, "fault_bytes": 4 * MIB,
          "service_seconds": 60, "service_max_requests": 2}


def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def boot_read(path, maximum=MIB):
    path = Path(path)
    require(path.is_absolute(), "ABSOLUTE_INPUT")
    for ancestor in (path, *path.parents):
        stat = ancestor.lstat()
        require(not ancestor.is_symlink() and not getattr(stat, "st_file_attributes", 0) & 0x400, "REPARSE_POINT")
    require(path.is_file() and path.stat().st_size <= maximum, "INPUT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    require(len(raw) <= maximum, "INPUT_BOUND")
    return raw


def boot_json(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            require(key not in value, "DUPLICATE_JSON")
            value[key] = item
        return value
    def finite(token):
        number = float(token)
        require(math.isfinite(number), "NONFINITE_JSON")
        return number
    def bad(_):
        raise RuntimeError("NONFINITE_JSON")
    return json.loads(raw.decode(), object_pairs_hook=pairs, parse_float=finite, parse_constant=bad)


def boot_pin(pin, path):
    require(type(pin) is dict and set(pin) == {"path", "bytes", "sha256"}
            and Path(pin["path"]).resolve() == Path(path).resolve(), "BOOT_PIN_PATH")
    raw = boot_read(pin["path"], 16 * MIB)
    require(type(pin["bytes"]) is int and len(raw) == pin["bytes"]
            and sha(raw) == pin["sha256"].lower(), "BOOT_PIN_CHANGED")
    return raw


class FaultSender:
    """Finite honest test actor, not a hard OS sandbox or general HTTP server."""
    def __init__(self, port, routes, count):
        require(1 <= count <= 2 and 1 <= len(routes) <= 2, "FAULT_ROUTE_COUNT")
        require(sum(len(body) for _media, body in routes.values()) <= 2 * MIB, "FAULT_FIXTURE_BOUND")
        self.port, self.routes, self.count = port, routes, count
        self.stop, self.ready = threading.Event(), threading.Event()
        self.error = None
        self.record = {"connections": [], "attempted_bytes": 0, "listener_closed": False,
                       "thread_joined": False, "containment": "TRUSTED_COOPERATIVE_THREAD_NO_OS_JOB"}
        self.thread = threading.Thread(target=self.run, name="bounded-fault-sender", daemon=False)

    def start(self):
        self.thread.start()
        require(self.ready.wait(timeout=5) and self.error is None, "FAULT_READINESS")

    def run(self):
        server = None
        started = time.monotonic()
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            server.bind(("127.0.0.1", self.port))
            server.listen(1)
            server.settimeout(0.2)
            self.ready.set()
            while len(self.record["connections"]) < self.count and not self.stop.is_set():
                require(time.monotonic() - started <= LIMITS["fault_seconds"], "FAULT_WALL_LIMIT")
                try:
                    connection, address = server.accept()
                except socket.timeout:
                    continue
                observation = {"accepted_at": time.monotonic(), "peer": list(address)}
                self.record["connections"].append(observation)
                with connection:
                    connection.settimeout(2)
                    raw = bytearray()
                    deadline = time.monotonic() + 5
                    while b"\r\n\r\n" not in raw:
                        require(time.monotonic() <= deadline and len(raw) < 8192, "FAULT_REQUEST_BOUND")
                        chunk = connection.recv(min(1024, 8192 - len(raw)))
                        require(chunk, "FAULT_EMPTY_REQUEST")
                        raw.extend(chunk)
                    first = bytes(raw).split(b"\r\n", 1)[0].decode("ascii")
                    parts = first.split(" ")
                    require(len(parts) == 3 and parts[0] == "GET" and parts[2] == "HTTP/1.1"
                            and parts[1] in self.routes, "FAULT_UNEXPECTED_ROUTE")
                    observation["route"] = parts[1]
                    media, body = self.routes[parts[1]]
                    header = ("HTTP/1.1 200 OK\r\nContent-Length: " + str(len(body))
                        + "\r\nContent-Type: " + media + "\r\nConnection: close\r\n\r\n").encode()
                    self.record["attempted_bytes"] += len(header) + len(body)
                    require(self.record["attempted_bytes"] <= LIMITS["fault_bytes"], "FAULT_BYTE_LIMIT")
                    connection.sendall(header + body)
                    observation.update(body_bytes=len(body), body_sha256=sha(body), sent=True)
        except BaseException as error:
            self.error = type(error).__name__ + ":" + str(error)[:512]
        finally:
            if server is not None:
                server.close()
            self.record["listener_closed"] = True
            self.record["elapsed_seconds"] = time.monotonic() - started
            self.ready.set()

    def finish(self, complete=True):
        if not complete:
            self.stop.set()
        self.thread.join(timeout=8)
        self.record["thread_joined"] = not self.thread.is_alive()
        self.record["error"] = self.error
        require(self.record["thread_joined"] and self.record["listener_closed"], "FAULT_THREAD_CLEANUP_UNCONFIRMED")
        if complete:
            require(self.error is None and len(self.record["connections"]) == self.count
                    and all(row.get("sent") is True for row in self.record["connections"]), "FAULT_EXACT_TRANSFERS")
        return self.record


def altered_bundle(bundle):
    """Change one short CBOR uint, preserving framing and canonical syntax."""
    require(bundle.startswith(MAGIC) and len(bundle) <= MIB, "FIXTURE_BUNDLE_PROFILE")
    start = len(MAGIC)
    size = int.from_bytes(bundle[start:start + 4], "big")
    manifest = boot_json(bundle[start + 4:start + 4 + size])
    offset = start + 4 + size
    for identifier in manifest["objects"]:
        require(offset + 8 <= len(bundle), "FIXTURE_FRAME")
        length = int.from_bytes(bundle[offset:offset + 8], "big")
        offset += 8
        raw = bundle[offset:offset + length]
        require(len(raw) == length and length > 0, "FIXTURE_OBJECT_BOUND")
        preimage = b"DTMKN-CAS\0" + identifier[1].to_bytes(2, "big") + identifier[2].to_bytes(2, "big")
        require(hashlib.sha256(preimage + length.to_bytes(8, "big") + raw).digest()
                == bytes(identifier[3]["$bytes"]), "ORIGINAL_FIXTURE_CID")
        cursor = 0
        while cursor < len(raw):
            first = raw[cursor]
            major, info = first >> 5, first & 31
            if major == 0 and info < 24:
                changed = bytearray(bundle)
                changed[offset + cursor] = first ^ 1
                return bytes(changed), {"offset": offset + cursor, "before": first, "after": first ^ 1,
                                        "object_id": identifier, "preserves": "short canonical uint width and all framing"}
            cursor += 1
            require(major in {0, 2, 4} and info <= 27, "FIXTURE_CANONICAL_PROFILE")
            if info < 24:
                amount = info
            else:
                width = 1 << (info - 24)
                require(cursor + width <= len(raw), "FIXTURE_CBOR_TRUNCATED")
                amount = int.from_bytes(raw[cursor:cursor + width], "big")
                cursor += width
            if major == 2:
                cursor += amount
            require(cursor <= len(raw), "FIXTURE_CBOR_BOUND")
        offset += length
    raise RuntimeError("NO_SAFE_SHORT_UINT_MUTATION_FIXTURE")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", type=Path, required=True)
    args = parser.parse_args()
    require(os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_site and sys.flags.no_user_site, "WINDOWS_PYTHON_PROFILE")
    started, cpu_started = time.monotonic(), time.process_time()
    helper = None
    commands, jobs, faults = [], {}, []
    active_fault = service = active_command = None
    result = {"status": "RUNNING", "scope": "post-H01 finite central controls; not all-controls qualification",
              "native_stages": 0, "observed_pipeline_children": 0,
              "work_counters_complete_for_bound_calls": True, "cpu_complete": False,
              "ledger_counters_complete_for_bound_calls": True,
              "observed_new_requests": 0, "observed_charged_bytes": 0, "observed_refusals": [],
              "variant": "NOT_EXERCISED_NO_GENUINE_SEMANTIC_VARIANT_FIXTURE",
              "recovery": "NOT_EXERCISED_SEPARATE_FRESH_CUT_REQUIRED"}

    def budget():
        elapsed = time.monotonic() - started
        cpu = time.process_time() - cpu_started + sum(jobs.values())
        require(elapsed <= LIMITS["active_wall_seconds"] and cpu <= LIMITS["observed_cpu_seconds"], "AGGREGATE_LIMIT")
        return LIMITS["active_wall_seconds"] - elapsed

    def object_pin(value, maximum=16 * MIB):
        helper.checked(value, maximum)
        return helper.parse(helper.read(value["path"], maximum))

    def exact(left, right):
        return encoded(left) == encoded(right)

    def ledger(node, require_idle=True):
        """Quiescent immutable read; never open a hot journal or repair it."""
        path = helper.safe(node["state"] / "control.sqlite3")
        for suffix in ("-journal", "-wal", "-shm"):
            extra = Path(str(path) + suffix)
            require(not extra.exists() or extra.stat().st_size == 0, "NONEMPTY_SQLITE_AUXILIARY")
        db = sqlite3.connect(path.as_uri() + "?mode=ro&immutable=1", uri=True, timeout=0)
        steps = 0
        def progress():
            nonlocal steps
            steps += 1
            return int(steps >= 100000)
        db.set_progress_handler(progress, 1)
        db.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 3 * MIB)
        try:
            db.execute("PRAGMA query_only=ON")
            def rows(sql, maximum=256):
                selected = db.execute(sql).fetchmany(maximum + 1)
                require(len(selected) <= maximum, "LEDGER_ROW_BOUND")
                output = [[{"bytes": len(x), "sha256": sha(x)} if isinstance(x, bytes) else x for x in row]
                          for row in selected]
                require(len(encoded(output)) <= 2 * MIB, "LEDGER_PROJECTION_BOUND")
                return output
            meta = db.execute("SELECT config,initialized,requests,stages,charged,active FROM meta WHERE id=1").fetchone()
            require(meta is not None and meta[0] == node["config"]["sha256"] and meta[1] == 1
                    and all(type(value) is int for value in meta[1:5]), "INITIALIZED_LEDGER")
            require(not require_idle or meta[5] is None, "IDLE_LEDGER_REQUIRED")
            return {"meta": list(meta), "heads": rows("SELECT client,context FROM heads ORDER BY client", 16),
                    "providers": rows("SELECT provider,cut,snapshot FROM providers ORDER BY provider", 16),
                    "entries": rows("SELECT provider,seq,descriptor_key,raw FROM entries ORDER BY provider,seq", 64),
                    "stages": rows("SELECT id,request,purpose,directory,grant_bytes FROM stages ORDER BY id", 64),
                    "authority": rows("SELECT handle,kind,client,raw FROM records WHERE kind IN ('candidate','context','artifact','publication','view') ORDER BY handle")}
        finally:
            db.close()

    def selected_record(node, handle, kind):
        ledger(node)
        db = sqlite3.connect((node["state"] / "control.sqlite3").as_uri() + "?mode=ro&immutable=1", uri=True, timeout=0)
        try:
            rows = db.execute("SELECT kind,client,raw FROM records WHERE handle=?", (handle,)).fetchmany(2)
            require(len(rows) == 1 and rows[0][0] == kind and rows[0][1] == "local", "SELECTED_RECORD")
            raw = bytes(rows[0][2])
            require(len(raw) <= 2 * MIB and handle == kind + ":" + sha(raw), "SELECTED_RECORD_HASH")
            value = helper.parse(raw)
            require(value["config"] == node["config"]["sha256"] and value["kind"] == kind and value["client"] == "local",
                    "SELECTED_RECORD_BINDING")
            return value["data"]
        finally:
            db.close()

    def terminal_observation(node, raw, reply):
        """Observe first; the caller persists mismatches before rejecting them."""
        selected = helper.parse(raw)
        key = sha(encoded([selected["client"], selected["request_id"]]))
        path = helper.safe(node["state"] / "control.sqlite3")
        for suffix in ("-journal", "-wal", "-shm"):
            auxiliary = Path(str(path) + suffix)
            require(not auxiliary.exists() or auxiliary.stat().st_size == 0, "NONEMPTY_SQLITE_AUXILIARY")
        db = sqlite3.connect(path.as_uri() + "?mode=ro&immutable=1", uri=True, timeout=0)
        db.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 3 * MIB)
        steps = 0
        def progress():
            nonlocal steps
            steps += 1
            return int(steps >= 100000)
        db.set_progress_handler(progress, 1)
        try:
            rows = db.execute("SELECT key,client,request_id,raw,phase,response FROM requests WHERE client=? AND request_id=?",
                (selected["client"], selected["request_id"])).fetchmany(2)
            require(len(rows) <= 1, "TERMINAL_ROW_BOUND")
            if not rows:
                return {"present": False, "matches": False}
            row = rows[0]
            stored_raw = bytes(row[3])
            stored_reply = None if row[5] is None else bytes(row[5])
            require(len(stored_raw) <= 131072 and (stored_reply is None or len(stored_reply) <= MIB), "TERMINAL_BYTE_BOUND")
            matches = (row[0] == key and row[1] == selected["client"] and row[2] == selected["request_id"]
                       and stored_raw == raw and row[4] == "terminal" and stored_reply == reply)
            return {"present": True, "key": row[0], "client": row[1], "request_id": row[2], "phase": row[4],
                    "raw_bytes": len(stored_raw), "raw_sha256": sha(stored_raw),
                    "response_bytes": None if stored_reply is None else len(stored_reply),
                    "response_sha256": None if stored_reply is None else sha(stored_reply), "matches": matches}
        finally:
            db.close()

    def unchanged(before, after, charge, count):
        require(all(exact(before[key], after[key]) for key in ("heads", "providers", "entries", "stages", "authority")),
                "CONTROL_PROMOTED_AUTHORITY")
        target = list(before["meta"])
        target[2] += count
        target[4] += charge
        require(exact(target, after["meta"]), "CONTROL_ACCOUNTING_DELTA")

    def start_command(name, argv, node):
        nonlocal active_command
        require(len(commands) < LIMITS["public_commands"], "COMMAND_COUNT")
        directory = RUN / "commands" / name
        directory.mkdir(exist_ok=False)
        record = {"name": name, "argv": argv, "cwd": str(node["install"]), "shell": False,
                  "timeout_seconds": min(LIMITS["command_seconds"], budget()), "started_at": time.monotonic(),
                  "descendant_quiescence": "NOT_YET_AUTHENTICATED"}
        commands.append(record)
        helper.save(directory / "command.json", record)
        out, err = directory / "stdout.txt", directory / "stderr.txt"
        with out.open("xb") as output, err.open("xb") as errors:
            process = subprocess.Popen(argv, cwd=node["install"], stdin=subprocess.DEVNULL,
                stdout=output, stderr=errors, shell=False, close_fds=True, creationflags=subprocess.CREATE_NO_WINDOW)
        active_command = {"record": record, "directory": directory, "out": out, "err": err, "process": process}
        return active_command

    def finish_command(job):
        if job.get("finished"):
            return job["raw"]
        while job["process"].poll() is None:
            budget()
            require(time.monotonic() - job["record"]["started_at"] <= job["record"]["timeout_seconds"], "COMMAND_TIMEOUT")
            require(job["out"].stat().st_size <= MIB and job["err"].stat().st_size <= 65536, "COMMAND_OUTPUT_BOUND")
            time.sleep(0.05)
        code = job["process"].wait(timeout=5)
        job["record"].update(returncode=code, direct_child_reaped=True)
        job["record"]["stdout"] = helper.pin(job["out"], MIB)
        job["record"]["stderr"] = helper.pin(job["err"], 65536)
        job["record"]["elapsed_seconds"] = time.monotonic() - job["record"]["started_at"]
        helper.save(job["directory"] / "result.json", job["record"])
        raw = helper.read(job["out"], MIB)
        job["finished"], job["raw"] = True, raw
        return raw

    def bind(job, case, raw, reply, node, service_call=False):
        nonlocal active_command
        case = helper.safe(case, directory=True)
        if service_call:
            require(case.name == "serve" and case.parent.name == "cases"
                    and case.parent.parent.parent == node["scratch"] / "services", "SERVICE_CASE_DOMAIN")
        else:
            require(case.parent == node["scratch"] / "calls", "NODE_CASE_DOMAIN")
        receipt = helper.parse(helper.read(case / "supervisor.json", 65536))
        event = helper.parse(helper.read(case / "event.json", 65536))
        require(type(receipt["schema"]) is int and receipt["schema"] == 1 and receipt["name"] == case.name
                and receipt["native_acceptance"] is False
                and receipt["status"] == "TRANSPORT_COMPLETE" and type(receipt["returncode"]) is int and receipt["returncode"] == 0
                and receipt["direct_child_reaped"] is True and receipt["final_active_zero"] is True
                and type(receipt["final_job"]["active_processes"]) is int and receipt["final_job"]["active_processes"] == 0
                and receipt.get("cleanup_errors", []) == [] and "output_record_error" not in receipt
                and "evidence_persistence_error" not in receipt, "ACTUAL_PUBLIC_QUIESCENCE")
        require(helper.read(case / "request.json", 131072) == raw and helper.read(case / "stdout.txt", MIB) == reply
                and receipt["request_sha256"] == sha(raw) and event["request_sha256"] == sha(raw)
                and event["response_sha256"] == sha(reply), "PUBLIC_IO_BINDING")
        file_bounds = {"request.json": 131072, "command.json": 65536, "stdout.txt": MIB,
                       "stderr.txt": 65536, "event.json": 65536}
        require(type(receipt["files"]) is dict and set(receipt["files"]) == set(file_bounds), "PUBLIC_FILE_SET")
        for name, maximum in file_bounds.items():
            declared = receipt["files"][name]
            payload = helper.read(case / name, maximum)
            require(type(declared) is dict and set(declared) == {"present", "bytes", "sha256"}
                    and declared["present"] is True and type(declared["bytes"]) is int
                    and declared["bytes"] == len(payload) and declared["sha256"] == sha(payload), "PUBLIC_FILE_PIN:" + name)
        module = "service_worker.py" if service_call else "node.py"
        names = (["service_worker", "inspect_context", "node", "storage", "domains", "run_stage", "supervise", "peer_wire", "peer_service"]
                 if service_call else ["node", "run_stage", "storage", "checking", "domains", "supervise", "peer_wire", "peer_service", "peer_node"])
        expected_paths = {Path(sys.executable).resolve(), Path(node["config"]["path"]),
                          *(node["install"] / "py" / (name + ".py") for name in names)}
        frozen = {Path(item["path"]).resolve(): item for item in [*node["source_pins"], node["config"], launch["python"]]}
        require(type(receipt["pins"]) is list and len(receipt["pins"]) == 11, "PUBLIC_EXACT_ELEVEN_PINS")
        paths, pin_bytes = set(), 0
        for item in receipt["pins"]:
            checked = helper.checked(item)
            path = Path(checked["path"]).resolve()
            require(path in expected_paths and path not in paths and path in frozen
                    and exact(checked, frozen[path]), "PUBLIC_FROZEN_PIN_IDENTITY")
            paths.add(path)
            pin_bytes += checked["bytes"]
        require(paths == expected_paths and type(receipt["bound_pin_count"]) is int and receipt["bound_pin_count"] == 11
                and type(receipt["bound_pin_bytes"]) is int and receipt["bound_pin_bytes"] == pin_bytes, "PUBLIC_PIN_COUNTERS")
        command = helper.parse(helper.read(case / "command.json", 65536))
        expected_command = {"argv": [str(Path(sys.executable).resolve()), *FLAGS, str(node["install"] / "py" / module),
             "--config", node["config"]["path"], "--state", str(node["state"]),
             "--request", str(case / "request.json"), "--event", str(case / "event.json")],
             "cwd": str(node["install"] / "py"), "shell": False, "creationflags": 134217732,
             "environment_override": {"PYTHONDONTWRITEBYTECODE": "1"}}
        require(exact(command, expected_command), "PUBLIC_EXACT_COMMAND")
        if not service_call:
            require(event["origin_directory"] == str(case), "ORIGINAL_CALL_BINDING")
        job["record"]["descendant_quiescence"] = "OBSERVED_BOUND_JOB_ACTIVE_ZERO_AND_DIRECT_REAP"
        if active_command is job:
            active_command = None
        key = str(case / "supervisor.json")
        require(key not in jobs, "CPU_DOUBLE_COUNT")
        cpu = receipt["final_job"]["cpu_seconds"]
        require(type(cpu) in (int, float) and math.isfinite(cpu) and cpu >= 0, "CPU_OBSERVATION")
        jobs[key] = cpu
        count = event.get("native_stages" if service_call else "stages_allocated")
        checker = event.get("checker_loaded")
        metrics = event.get("checker_metrics", {})
        metric_stages = metrics.get("stage_allocations") if type(metrics) is dict else None
        children = metrics.get("pipeline_children") if type(metrics) is dict else None
        actual = {"native_stages": count, "checker_loaded": checker,
                  "checker_stage_allocations": metric_stages, "pipeline_children": children}
        actual["well_typed"] = (type(count) is int and 0 <= count <= 64 and type(checker) is bool
             and type(metrics) is dict and all(value is None or (type(value) is int and 0 <= value <= 320)
                                              for value in (metric_stages, children)))
        if not actual["well_typed"]:
            result["work_counters_complete_for_bound_calls"] = False
        if type(count) is int and 0 <= count <= 64:
            result["native_stages"] += count
        else:
            result["work_counters_complete_for_bound_calls"] = False
        if type(children) is int and 0 <= children <= 320:
            result["observed_pipeline_children"] += children
        elif checker is not False:
            result["work_counters_complete_for_bound_calls"] = False
        value = {"supervisor": helper.pin(case / "supervisor.json"), "event": helper.pin(case / "event.json"),
                 "request_sha256": sha(raw), "response": helper.pin(job["out"]), "actual_work": actual,
                 "observed_job_cpu_seconds": cpu, "descendant_quiescence": job["record"]["descendant_quiescence"]}
        job["record"]["actual_work"] = actual
        job["record"]["binding"] = helper.save(job["directory"] / "binding.json", value)
        # No expected count/status or budget assertion precedes this persistence.
        return event, value

    def request(name, op=None, arguments=None, client="local", raw=None, code=None, historical=False):
        before = ledger(receiver)
        if raw is None:
            raw = encoded({"client": client, "request_id": "controls-" + name, "op": op, "args": arguments})
        selected = helper.parse(raw)
        request_path = RUN / "requests" / (name + ".json")
        helper.save_raw(request_path, raw)
        calls = receiver["scratch"] / "calls"
        previous = set(calls.iterdir())
        job = start_command(name, [str(Path(sys.executable).resolve()), *FLAGS, str(receiver["install"] / "manage.py"),
            "request", "--config", receiver["config"]["path"], "--request", str(request_path)], receiver)
        reply_raw = finish_command(job)
        added = set(calls.iterdir()) - previous
        require(len(added) == 1, "EXACT_NEW_CALL")
        event, binding = bind(job, added.pop(), raw, reply_raw, receiver)
        field = {"peer_acquire": "peer_request_bytes", "expose": "expose_request_bytes"}.get(selected["op"], "request_bytes")
        charge = 0 if historical else receiver["configuration"]["limits"][field]
        record = {"request": helper.pin(request_path), "response": helper.pin(job["out"]), "binding": binding,
                  "before": before, "expected_charged_delta": charge, "expected_code": code,
                  "started_at": job["record"]["started_at"], "event": event}
        reply, after, terminal = None, None, None
        try:
            reply = helper.parse(reply_raw)
            if type(reply) is dict:
                record["public_status"], record["public_code"] = reply.get("status"), reply.get("code")
                job["record"]["public_status"], job["record"]["public_code"] = reply.get("status"), reply.get("code")
                if reply.get("status") == "REFUSED":
                    result["observed_refusals"].append({"name": name, "code": reply.get("code"), "response": record["response"]})
        except Exception as observation_error:
            record["response_parse_error"] = type(observation_error).__name__ + ":" + str(observation_error)[:512]
        try:
            after = ledger(receiver, require_idle=False)
            actual_requests = after["meta"][2] - before["meta"][2]
            actual_charge = after["meta"][4] - before["meta"][4]
            record.update(after=after, observed_request_delta=actual_requests, observed_charged_delta=actual_charge)
            result["observed_new_requests"] += actual_requests
            result["observed_charged_bytes"] += actual_charge
            terminal = terminal_observation(receiver, raw, reply_raw)
            record["terminal"] = terminal
        except Exception as observation_error:
            result["ledger_counters_complete_for_bound_calls"] = False
            record["ledger_observation_error"] = type(observation_error).__name__ + ":" + str(observation_error)[:512]
        # Costs, actual refusal and independently bound cleanup survive a wrong
        # expected-code/count assertion, including a subsequent budget failure.
        helper.save(RUN / "checks" / (name + ".json"), record)
        budget()
        require(job["record"]["returncode"] == 0 and reply_raw.endswith(b"\n") and reply_raw.count(b"\n") == 1
                and type(reply) is dict, "PUBLIC_RESPONSE_PROFILE")
        require(after is not None and terminal is not None, "LEDGER_OBSERVATION_UNAVAILABLE")
        require(terminal["matches"] is True, "EXACT_TERMINAL_REQUEST_RESPONSE_BINDING")
        require(event.get("historical") is historical, "REPLAY_BRANCH")
        unchanged(before, after, charge, 0 if historical else 1)
        actual = binding["actual_work"]
        require(actual["well_typed"] and actual["native_stages"] == 0, "CONTROL_NATIVE_STAGE_FORBIDDEN")
        if actual["checker_loaded"]:
            require(actual["checker_stage_allocations"] == 0 and actual["pipeline_children"] == 0, "NO_NATIVE_PIPELINE")
        if code is None:
            require(reply.get("status") == "OK", "EXPECTED_PUBLIC_SUCCESS:" + str(reply.get("code", reply.get("status")))[:128])
        else:
            require(reply.get("status") == "REFUSED" and reply.get("code") == code, "WRONG_REFUSAL_LAYER:" + name)
        return reply, reply_raw, record

    def finish_service():
        nonlocal service
        if service is None:
            return
        selected_service, job = service, service["job"]
        raw = finish_command(job)
        event, binding = bind(job, service["root"] / "cases/serve", service["request"], raw, sender, True)
        result["private_service"] = {"reply": helper.pin(job["out"]), "binding": binding}
        # The bound Job has already stopped. Later service-result assertions must
        # neither erase this fact nor bind/count the same receipt twice.
        service = None
        reply = helper.parse(raw)
        result["private_service"]["public_status"] = reply.get("status") if type(reply) is dict else None
        helper.save(job["directory"] / "service-observation.json", result["private_service"])
        budget()
        actual = binding["actual_work"]
        require(job["record"]["returncode"] == 0 and actual["well_typed"] and actual["native_stages"] == 0
                and reply["status"] == "SERVICE_STOPPED" and reply["view"] == selected_service["view"]
                and reply["native_stages"] == 0 and reply["mathematicalAcceptance"] is False
                and reply["observations"]["connections"] == 2 and reply["observations"]["responses"] == 2
                and event["checker_loaded"] is False, "PRIVATE_SERVICE_CLEANUP")

    try:
        launch_raw = boot_read(args.launch)
        launch = boot_json(launch_raw)
        require(type(launch) is dict and set(launch) == {"schema", "coordinator", "helper", "python", "prepare", "g", "h", "limits"}
                and type(launch["schema"]) is int and launch["schema"] == 1 and exact(launch["limits"], LIMITS), "LAUNCH_FIELDS")
        boot_pin(launch["coordinator"], __file__)
        boot_pin(launch["python"], sys.executable)
        boot_pin(launch["helper"], SOURCE / "tests/prepare_peers.py")
        spec = importlib.util.spec_from_file_location("peer_controls_verified_test_helpers", launch["helper"]["path"])
        require(spec is not None and spec.loader is not None, "HELPER_LOADER")
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        prepared, g, h = (object_pin(launch[key]) for key in ("prepare", "g", "h"))
        require(Path(launch["prepare"]["path"]) == SOURCE / "qualification/peer-01/prepare-result.json"
                and Path(launch["g"]["path"]) == SOURCE / "qualification/peer-01-g02/continue-result.json"
                and Path(launch["h"]["path"]) == SOURCE / "qualification/peer-01-h01/continue-result.json", "PREDECESSOR_PATHS")
        require(prepared["status"] == "PREPARED_TWO_INSTALLATIONS_AWAITING_INDEPENDENT_AUDIT_AND_LOCAL_AUTHORING"
                and type(g["schema"]) is int and g["schema"] == 2 and g["attempt"] == "g02" and g["phase"] == "g_to_beta"
                and type(h["schema"]) is int and h["schema"] == 2 and h["attempt"] == "h01" and h["phase"] == "h_to_alpha"
                and g["status"] == "G_OFFLINE_ADMITTED_BY_BETA_AWAITING_INDEPENDENT_H_AUTHORING"
                and h["status"] == "POSITIVE_RECIPROCAL_OFFLINE_LOOP_COMPLETED_AWAITING_DEPENDENCY_AUDIT"
                and exact(g["prepare"], launch["prepare"]) and exact(h["prepare"], launch["prepare"])
                and exact(h["previous"], launch["g"]), "COMPLETED_H_REQUIRED")
        g_launch, h_launch = object_pin(g["launch"]), object_pin(h["launch"])
        require(type(g_launch["schema"]) is int and g_launch["schema"] == 2 and g_launch["attempt"] == "g02"
                and type(h_launch["schema"]) is int and h_launch["schema"] == 2 and h_launch["attempt"] == "h01"
                and exact(g_launch["prepare"], launch["prepare"]) and exact(g_launch["previous"], launch["prepare"])
                and exact(h_launch["prepare"], launch["prepare"]) and exact(h_launch["previous"], launch["g"])
                and h_launch["original_failure"] is None and h_launch["original_outcome"] is None, "V2_ATTEMPT_LINEAGE")
        original_failure = object_pin(g_launch["original_failure"])
        require(Path(g_launch["original_failure"]["path"]) == SOURCE / "qualification/peer-01-g/continue-failure.json"
                and original_failure["status"] == "STOPPED" and original_failure["phase"] == "g_to_beta"
                and exact(original_failure["prepare"], launch["prepare"]), "RETAINED_FAILED_G_LINEAGE")
        helper.checked(g_launch["original_outcome"])
        require(Path(g_launch["original_outcome"]["path"]) == SOURCE / "qualification/peer-01-g/OUTCOME.md", "ORIGINAL_OUTCOME_PATH")
        prepare_launch = object_pin(prepared["launch"])
        require(exact(prepare_launch["python"], launch["python"])
                and exact(prepare_launch["coordinator"], launch["helper"]), "FROZEN_HELPER_RUNTIME")
        nodes = {}
        for name in ("alpha", "beta"):
            original = prepared["nodes"][name]
            node = {key: helper.safe(DATA / name / key, directory=True) for key in ("install", "state", "scratch")}
            require(all(original[key] == str(node[key]) for key in node), "PREPARED_NODE_DOMAIN")
            node["config"], node["source_pins"] = original["config"], object_pin(original["sources"])
            node["configuration"] = object_pin(node["config"])
            require(Path(node["config"]["path"]) == node["state"] / "config.json", "CONFIG_PATH")
            require(exact(node["configuration"]["domains"], {"install": str(node["install"]), "state": str(node["state"]),
                "scratch": str(node["scratch"]), "lean_runtime": prepared["shared_runtime"]["path"]}), "CONFIG_EXACT_DOMAINS")
            require(1 <= len(node["source_pins"]) <= 512, "SOURCE_PIN_COUNT")
            source_paths = [Path(item["path"]).resolve() for item in node["source_pins"]]
            require(len(set(source_paths)) == len(source_paths) and all(path.is_relative_to(node["install"]) for path in source_paths),
                    "FROZEN_SOURCE_PATHS")
            for key, file_pin in node["configuration"]["files"].items():
                require(exact(file_pin, prepared["shared_runtime"]["lean"]) if key == "lean"
                        else Path(file_pin["path"]).resolve().is_relative_to(node["install"]), "CONFIG_PIN_DOMAIN")
            for file_pin in [*node["source_pins"], *node["configuration"]["files"].values(), original["build"]["receipt"]]:
                helper.checked(file_pin)
                budget()
            actual = ledger(node)
            public = h["expected_public"][name]
            require(["local", public["context"]] in actual["heads"]
                    and any(row[0] == "P1" and row[2] == public["snapshot"] for row in actual["providers"]), "POST_H_LEDGER_BINDING")
            nodes[name] = node
        receiver, sender = nodes["alpha"], nodes["beta"]
        require(receiver["configuration"]["peers"] == {"other": {"host": "127.0.0.1", "port": 43172}}, "FIXED_ALIAS")
        original_acquire = object_pin(h["acquisition"]["response"])
        original_request = helper.read(h["acquisition"]["request"]["path"], 131072)
        helper.checked(h["acquisition"]["request"])
        require(helper.parse(original_request)["op"] == "peer_acquire"
                and helper.parse(original_request)["request_id"] == "peer-h01-peer-acquire"
                and helper.parse(original_request)["client"] == "local", "ORIGINAL_H01_ACQUISITION_REQUEST")
        old_service = object_pin(h["service_stop"]["binding"]["supervisor"])
        require(old_service["direct_child_reaped"] is True and old_service["final_active_zero"] is True
                and old_service["final_job"]["active_processes"] == 0, "POSITIVE_SERVICE_STOP_REQUIRED")
        exposed = object_pin(h["exposure"]["response"])
        view = selected_record(sender, exposed["view"], "view")
        catalog_raw = helper.read(view["catalog"]["path"], 65536)
        helper.checked(view["catalog"], 65536)
        catalog = helper.parse(catalog_raw)
        require(len(catalog["entries"]) == 1 and exact(catalog["entries"][0]["descriptor_id"], h["descriptor_id"]), "SINGLE_H_FIXTURE")
        entry = catalog["entries"][0]
        bundle_path = helper.safe(Path(view["directory"]) / "bundles" / (entry["bundle_sha256"] + ".bundle"))
        require(bundle_path.is_relative_to(sender["state"] / "work"), "PUBLISHED_FIXTURE_DOMAIN")
        bundle = helper.read(bundle_path, MIB)
        require(len(bundle) == entry["bundle_bytes"] and sha(bundle) == entry["bundle_sha256"], "PUBLISHED_BUNDLE_PIN")
        changed, mutation = altered_bundle(bundle)
        require(not RUN.exists(), "FRESH_CONTROLS_ROOT")
        RUN.mkdir(exist_ok=False)
        for name in ("commands", "requests", "checks", "fixtures"):
            (RUN / name).mkdir()
        result.update(launch=helper.save_raw(RUN / "launch.json", launch_raw),
                      coordinator_snapshot=helper.save_raw(RUN / "coordinator.py", helper.read(__file__, MIB)),
                      predecessor=launch["h"], nodes={name: ledger(node) for name, node in nodes.items()},
                      fixture={"catalog": view["catalog"], "bundle": helper.pin(bundle_path), "mutation": mutation})
        baseline = helper.census(DATA, budget, hashes=True)
        helper.save(RUN / "baseline-data.json", baseline)
        helper.save_raw(RUN / "fixtures/original-catalog.json", catalog_raw)
        helper.save_raw(RUN / "fixtures/original.bundle", bundle)
        helper.save_raw(RUN / "fixtures/changed.bundle", changed)

        # Hold the known port exclusively bound, without listening, during replay.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as offline:
            offline.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            offline.bind(("127.0.0.1", 43172))
            replay, replay_raw, _ = request("offline-replay", raw=original_request, historical=True)
            require(replay_raw == helper.read(h["acquisition"]["response"]["path"], MIB), "EXACT_OFFLINE_REPLAY_BYTES")
        remote = helper.parse(original_request)["args"]["remote"]
        active_fault = FaultSender(43172, {"/v1/bundle/" + entry["bundle_sha256"]: ("application/octet-stream", bundle)}, 1)
        active_fault.start()
        request("wrong-alias", "peer_find", {"peer": "unknown-control-alias"}, code="UNKNOWN_PEER")
        request("wrong-client", "peer_acquire", {"remote": remote}, client="reviewer", code="WRONG_CLIENT_HANDLE")
        request("acquired-expose", "expose", {"selected": [original_acquire["candidate"]]}, code="NOT_LOCALLY_PUBLISHED")
        before_package = selected_record(receiver, original_acquire["acquisition"], "acquisition")["package"]
        duplicate, _, evidence = request("duplicate", "peer_acquire", {"remote": remote})
        require(duplicate["existing"] is True and duplicate["snapshot"] == original_acquire["snapshot"]
                and duplicate["candidate"] == original_acquire["candidate"]
                and exact(selected_record(receiver, duplicate["acquisition"], "acquisition")["package"], before_package), "EXACT_OFFER_REUSE")
        observed = active_fault.finish()
        require(observed["connections"][0]["accepted_at"] >= evidence["started_at"], "LOCAL_REFUSAL_CONNECTED")
        faults.append(observed)
        active_fault = None
        for name, body, expected in (("false-metadata", bundle, "ADVERTISED_METADATA_MISMATCH"),
                                     ("digest-tamper", changed, "BUNDLE_DIGEST_MISMATCH"),
                                     ("cid-tamper", changed, "OBJECT_ID_MISMATCH")):
            advertised = copy.deepcopy(catalog)
            claimed = advertised["entries"][0]
            if name == "false-metadata":
                arity = claimed["formal_metadata"]["universe_arity"]
                require(type(arity) is int and 0 <= arity < (1 << 64) - 1, "ARITY_FIXTURE")
                claimed["formal_metadata"]["universe_arity"] = arity + 1
            if name == "cid-tamper":
                claimed["bundle_sha256"] = sha(body)
            raw = encoded(advertised)
            helper.save_raw(RUN / "fixtures" / (name + "-catalog.json"), raw)
            active_fault = FaultSender(43172, {"/v1/catalog": ("application/json", raw),
                "/v1/bundle/" + claimed["bundle_sha256"]: ("application/octet-stream", body)}, 2)
            active_fault.start()
            found, _, _ = request(name + "-find", "peer_find", {"peer": "other"})
            require(len(found["rows"]) == 1 and found["candidate_only"] is True
                    and found["mathematicalAcceptance"] is False, "SHALLOW_CATALOG_MUST_PASS")
            request(name + "-acquire", "peer_acquire", {"remote": found["rows"][0]["remote"]}, code=expected)
            faults.append(active_fault.finish())
            active_fault = None

        # Real installed service, not the fault actor, must refuse private routes.
        session = "peer-controls-private"
        service_root = sender["scratch"] / "services" / session
        require(not service_root.exists(), "FRESH_PRIVATE_SERVICE")
        service_raw = encoded({"op": "serve", "session": session, "client": "local", "view": exposed["view"],
            "port": 43172, "seconds": 60, "max_requests": 2, "max_bytes": MIB})
        service_job = start_command("private-service", [str(Path(sys.executable).resolve()), *FLAGS,
            str(sender["install"] / "manage.py"), "serve", "--config", sender["config"]["path"],
            "--client", "local", "--view", exposed["view"], "--session", session, "--port", "43172",
            "--seconds", "60", "--max-requests", "2", "--max-bytes", str(MIB)], sender)
        service = {"job": service_job, "root": service_root, "request": service_raw, "view": exposed["view"]}
        ready = service_root / "ready.json"
        while not ready.exists():
            budget()
            require(service_job["process"].poll() is None and time.monotonic() - service_job["record"]["started_at"] < 30, "SERVICE_READINESS")
            time.sleep(0.05)
        require(exact(helper.parse(helper.read(ready, 4096)), {"host": "127.0.0.1", "port": 43172,
                      "catalog_sha256": exposed["catalog_sha256"]}), "PRIVATE_SERVICE_READY_BINDING")
        responses = []
        for route in ("/control.sqlite3", "/v1/bundle/" + "0" * 64):
            with socket.create_connection(("127.0.0.1", 43172), timeout=2) as probe:
                probe.settimeout(2)
                probe.sendall(("GET " + route + " HTTP/1.1\r\nHost: 127.0.0.1:43172\r\nConnection: close\r\n\r\n").encode())
                reply = bytearray()
                while True:
                    require(len(reply) <= 16384, "PRIVATE_REPLY_BOUND")
                    piece = probe.recv(4096)
                    if not piece:
                        break
                    reply.extend(piece)
                require(bytes(reply).startswith(b"HTTP/1.1 404 ") and b"\r\n\r\n" in reply, "PRIVATE_ROUTE_EXPOSED")
                body = bytes(reply).split(b"\r\n\r\n", 1)[1]
                require(body == encoded({"code": "PEER_NOT_FOUND"}), "PRIVATE_RESPONSE_BODY_EXPOSED")
                response_pin = helper.save_raw(RUN / "checks" / ("private-route-%d.http" % len(responses)), bytes(reply))
                responses.append({"route": route, "bytes": len(reply), "sha256": sha(reply), "response": response_pin})
        finish_service()
        result["private_routes"] = responses
        require(len(commands) == 12 and len(faults) == 4 and len(jobs) == 12
                and result["native_stages"] == 0 and result["observed_new_requests"] == 10
                and result["observed_charged_bytes"] == 432 * MIB, "EXACT_CONTROLS_WORK")
        unchanged(result["nodes"]["beta"], ledger(sender), 0, 0)
        for node in nodes.values():
            helper.checked(node["config"])
            for record in [*node["source_pins"], *node["configuration"]["files"].values()]:
                helper.checked(record)
                budget()
        for key in ("coordinator", "helper", "python", "prepare", "g", "h"):
            helper.checked(launch[key])
        final_data = helper.census(DATA, budget, hashes=True)
        final_rows = {row["path"]: row for row in final_data["manifest"]}
        for row in baseline["manifest"]:
            if row["path"] in {"alpha/state/control.sqlite3", "beta/state/control.sqlite3"}:
                continue
            require(row["path"] in final_rows and exact(row, final_rows[row["path"]]), "PREEXISTING_FILE_CHANGED_OR_REMOVED")
        run_census = helper.census(RUN, budget, hashes=True)
        result.update(status="MINIMAL_CENTRAL_CONTROLS_COMPLETED_VARIANT_AND_RECOVERY_NOT_EXERCISED",
                      faults=faults, commands=commands, final_nodes={name: ledger(node) for name, node in nodes.items()},
                      observed_cpu_seconds=time.process_time() - cpu_started + sum(jobs.values()),
                      cpu_record_paths=sorted(jobs), active_wall_seconds=time.monotonic() - started,
                      accounting="coordinator+fault-thread CPU once, bound product Jobs once; manage wrapper CPU unmetered",
                      data_seal=helper.save(RUN / "data-seal.json", final_data),
                      evidence_seal=helper.save(RUN / "evidence-seal.json", run_census))
        raw = encoded(result)
        require(final_data["bytes"] + run_census["bytes"] + result["data_seal"]["bytes"]
                + result["evidence_seal"]["bytes"] + len(raw) <= LIMITS["retained_bytes"], "FINAL_RETAINED_BOUND")
        budget()
        receipt = helper.save_raw(RUN / "controls-result.json", raw)
        print(json.dumps({"status": result["status"], "receipt": receipt}))
        return 0
    except BaseException as error:
        if active_fault is not None:
            try:
                faults.append(active_fault.finish(False))
            except BaseException as cleanup:
                result["fault_cleanup_error"] = str(cleanup)[:512]
        if service is not None:
            try:
                finish_service()
            except BaseException as cleanup:
                result["service_cleanup_error"] = str(cleanup)[:512]
        if active_command is not None and active_command["record"].get("descendant_quiescence") != "OBSERVED_BOUND_JOB_ACTIVE_ZERO_AND_DIRECT_REAP":
            try:
                if active_command["process"].poll() is None:
                    active_command["process"].kill()
                active_command["process"].wait(timeout=5)
            except BaseException as cleanup:
                result["direct_cleanup_error"] = str(cleanup)[:512]
            result["unconfirmed_descendants"] = "DIRECT_WRAPPER_REAP_IS_NOT_PRODUCT_JOB_QUIESCENCE"
        result.update(status="STOPPED", error=type(error).__name__, detail=str(error)[:1024], faults=faults, commands=commands,
                      active_wall_seconds=time.monotonic() - started,
                      observed_cpu_seconds=time.process_time() - cpu_started + sum(jobs.values()),
                      cpu_record_paths=sorted(jobs), bound_public_jobs=len(jobs), public_commands=len(commands),
                      unbound_public_commands=[row["name"] for row in commands if "binding" not in row],
                      accounting="actual bound-call work and readonly charge observations retained before expected-case assertions; unbound calls remain unmeasured")
        if helper is not None and RUN.is_dir() and "launch" in result:
            receipt = helper.save(RUN / "controls-failure.json", result)
            print(json.dumps({"status": "STOPPED", "failure": receipt}))
        else:
            print(json.dumps({"status": "STOPPED_BEFORE_OWNED_CONTROLS", "detail": str(error)[:1024]}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

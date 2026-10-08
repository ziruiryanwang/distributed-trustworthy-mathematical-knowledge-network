"""Seventeen-CLI native renewal experiment inside one reviewed outer Job.

Transparent adaptation of the frozen native03 worker; no prior driver imported.
Only installed public CLIs mutate node state. No synthetic acceptance or retries.
"""
import argparse
from copy import deepcopy
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import sqlite3
import stat
import subprocess
import sys
import time

SOURCE = Path(__file__).resolve().parents[1]
PRODUCT = SOURCE
DATA = SOURCE.parent / "product-local/capacity-native-01"
FLAGS = ["-B", "-E", "-s", "-S"]
MIB = 1048576
LIMITS = {"wall_seconds": 450, "cpu_seconds": 450, "memory_mib": 6144,
          "active_processes": 16, "stdout_bytes": 65536, "stderr_bytes": 65536, "event_bytes": 65536}
RETAINED = {"bytes": 1073741824, "files": 16384, "entries": 32768}
REQUEST = b'{"op":"test-capacity-native"}\n'
SCOPE = "fixed native capacity continuation; not indefinite operation or useful-growth qualification"
TABLES = {"meta": "id", "authorization": "id", "owner_grants": "sequence",
          "requests": "key", "records": "handle", "heads": "client", "providers": "provider",
          "snapshots": "handle", "entries": "provider,seq", "stages": "id"}
FIXTURE = """universe u
noncomputable def RenewalCompose (A B C : Sort u)
    (g : B -> C) (f : A -> B) (a : A) : C :=
  g (f a)
"""


def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")


def strict(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            require(key not in value, "DUPLICATE_JSON_KEY")
            value[key] = item
        return value
    def bad(_):
        raise RuntimeError("NONFINITE_JSON")
    def finite(token):
        value = float(token)
        require(math.isfinite(value), "NONFINITE_JSON")
        return value
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=bad, parse_float=finite)


def checked(path):
    path = Path(path)
    require(path.is_absolute(), "ABSOLUTE_PATH")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        require(not stat.S_ISLNK(info.st_mode)
                and not getattr(info, "st_file_attributes", 0) & 0x400, "REPARSE_POINT")
    return path.resolve(strict=True)


def read(path, bound=16 * MIB):
    path = checked(path)
    require(path.is_file() and path.stat().st_size <= bound, "READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(bound + 1)
    require(len(raw) <= bound, "READ_BOUND")
    return raw


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path):
    path = checked(path)
    raw = read(path)
    return {"path": str(path), "bytes": len(raw), "sha256": sha(raw)}


def save_raw(path, raw):
    require(type(raw) is bytes and len(raw) <= 16 * MIB, "SAVE_BOUND")
    path.parent.mkdir(parents=True, exist_ok=True)
    checked(path.parent)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def save(path, value):
    save_raw(path, encode(value))


def blob(value):
    return {"hex": value.hex()} if type(value) is bytes else value


def product_paths():
    paths = [PRODUCT / name for name in ("API.md", "manage.py", "build.py", "assets-lock.json")]
    paths.extend(path for path in checked(PRODUCT / "py").iterdir() if path.suffix == ".py")
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
    return sorted(paths, key=lambda path: path.relative_to(PRODUCT).as_posix())


def supply(value, remaining, *, enforced):
    required = remaining + 2 * 8192 * 4096 + 1024 * MIB
    require(type(value) is dict and "mocked" not in value and value["sample_only"] is True
            and value["reserved_by_os"] is False and value["filesystem"] == "NTFS"
            and type(value["volume"]) is str and value["volume"]
            and type(value["available_bytes"]) is int and value["available_bytes"] >= 0
            and value["remaining_authorized_bytes"] == remaining and value["metadata_pages"] == 8192
            and value["required_bytes"] == required
            and value["sufficient"] is (value["available_bytes"] >= required)
            and (not enforced or value["sufficient"] is True), "ACTUAL_SUPPLY_SAMPLE")


class Scenario:
    def __init__(self):
        self.install, self.state, self.scratch, self.driver = (DATA / name for name in
                                                            ("install", "state", "scratch", "driver"))
        self.config = self.state / "config.json"
        self.calls, self.snapshots = [], []
        self.installed, self.events = {}, {}
        self.config_pin, self.config_id, self.owner_lock = None, None, None

    def snapshot(self, name):
        require(self.owner_lock is not None and sqlite3.sqlite_version == "3.50.4", "SNAPSHOT_PROFILE")
        db_path = checked(self.state / "control.sqlite3")
        with self.owner_lock(self.state, create=False):
            for suffix in ("-journal", "-wal", "-shm"):
                sidecar = Path(str(db_path) + suffix)
                require(not sidecar.exists() or sidecar.stat().st_size == 0, "NONEMPTY_SQLITE_SIDECAR")
            require(db_path.stat().st_size <= 32 * MIB, "DATABASE_BOUND")
            db = sqlite3.connect(db_path.as_uri() + "?mode=ro", uri=True, timeout=0, isolation_level=None)
            steps = [0]
            def progress():
                steps[0] += 1
                return int(steps[0] >= 100000)
            try:
                db.set_progress_handler(progress, 1)
                db.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 3 * MIB)
                db.execute("PRAGMA query_only=ON")
                db.execute("PRAGMA temp_store=MEMORY")
                db.execute("PRAGMA mmap_size=0")
                require(db.execute("PRAGMA query_only").fetchone()[0] == 1
                        and db.execute("PRAGMA user_version").fetchone()[0] == 3
                        and db.execute("PRAGMA page_size").fetchone()[0] == 4096, "SNAPSHOT_DATABASE_PROFILE")
                db.row_factory = sqlite3.Row
                value = {}
                for table, order in TABLES.items():
                    rows = db.execute("SELECT * FROM " + table + " ORDER BY " + order).fetchmany(129)
                    require(len(rows) <= 128, "SNAPSHOT_ROW_BOUND")
                    value[table] = [{key: blob(row[key]) for key in row.keys()} for row in rows]
                pages = db.execute("PRAGMA page_count").fetchone()[0]
                freelist = db.execute("PRAGMA freelist_count").fetchone()[0]
            finally:
                db.close()
        path = self.driver / "snapshots" / (name + ".json")
        save(path, value)
        self.snapshots.append({"name": name, "tables": pin(path), "pages": pages,
                               "freelist_pages": freelist, "sql_vm_steps": steps[0]})
        return value

    def file_map(self, root):
        require(root.is_dir(), "FILE_MAP_ROOT")
        rows, total = {}, 0
        for number, path in enumerate(root.rglob("*"), 1):
            require(number <= 16384, "FILE_MAP_ENTRY_BOUND")
            path = checked(path)
            if path.is_file():
                require(len(rows) < 8192, "FILE_MAP_FILE_BOUND")
                size = path.stat().st_size
                total += size
                require(total <= 512 * MIB, "FILE_MAP_BYTE_BOUND")
                digest = hashlib.sha256()
                observed = 0
                with path.open("rb") as stream:
                    for raw in iter(lambda: stream.read(MIB), b""):
                        observed += len(raw)
                        require(observed <= size, "FILE_MAP_GREW")
                        digest.update(raw)
                require(observed == size and path.stat().st_size == size, "FILE_MAP_CHANGED")
                rows[path.relative_to(root).as_posix()] = {"bytes": size, "sha256": digest.hexdigest()}
        return rows

    def cli(self, name, arguments, raw=None, *, role="preparation"):
        require(role in {"preparation", "ordinary", "administrative"}, "CLI_ROLE")
        directory = self.driver / "calls" / name
        directory.mkdir(parents=True, exist_ok=False)
        command = [sys.executable, *FLAGS, *map(str, arguments)]
        save(directory / "command.json", {"argv": command, "cwd": str(self.install), "shell": False})
        evidence = self.scratch / ("administration" if role == "administrative" else "calls")
        before = set(evidence.iterdir()) if evidence.exists() else set()
        require(len(before) <= 16, "CALL_DIRECTORY_BOUND")
        started = time.monotonic()
        # The reviewed enclosing Job, not this wait alone, contains descendants.
        with (directory / "stdout.txt").open("xb") as out, (directory / "stderr.txt").open("xb") as err:
            process = subprocess.Popen(command, cwd=self.install, stdin=subprocess.DEVNULL,
                stdout=out, stderr=err, shell=False, close_fds=True, creationflags=subprocess.CREATE_NO_WINDOW)
            process.wait()
        observation = {"name": name, "role": role, "returncode": process.returncode,
            "direct_child_reaped": True, "elapsed_seconds": time.monotonic() - started,
            "stdout": pin(directory / "stdout.txt"), "stderr": pin(directory / "stderr.txt")}
        self.calls.append(observation)
        save(directory / "process.json", observation)
        output = read(directory / "stdout.txt", 65536 if role == "administrative" else MIB)
        event = None
        if role != "preparation":
            require(type(raw) is bytes, "EXPECTED_REQUEST_BYTES")
            after = set(evidence.iterdir())
            require(len(after) <= 17 and before <= after and len(after - before) == 1, "ONE_PUBLIC_CALL")
            public = checked((after - before).pop())
            receipt_path = public / "supervisor.json"
            receipt = strict(read(receipt_path, 65536))
            observation["public_receipt"] = pin(receipt_path)
            observation["actual_job_cpu_seconds"] = receipt.get("final_job", {}).get("cpu_seconds")
            observation["cleanup"] = {key: receipt.get(key) for key in
                ("direct_child_reaped", "final_active_zero", "job_closed", "cleanup_errors")}
            save(directory / "supervisor-observation.json", observation)
            require(receipt["status"] == "TRANSPORT_COMPLETE" and receipt["returncode"] == 0
                    and receipt["job_created_before_process"] is True and receipt["attach_resume_returned"] is True
                    and receipt["direct_child_reaped"] is True and receipt["final_active_zero"] is True
                    and receipt["job_closed"] is True and not any(receipt.get(key) for key in
                        ("cleanup_errors", "output_record_error", "evidence_persistence_error", "failure"))
                    and receipt["final_job"]["active_processes"] == 0
                    and receipt["final_job"]["terminated_processes"] == 0, "PUBLIC_QUIESCENCE")
            if role == "ordinary":
                names = ("node.py", "run_stage.py", "storage.py", "capacity.py", "checking.py", "domains.py",
                         "supervise.py", "peer_wire.py", "peer_service.py", "peer_node.py")
                expected_pins = [self.python_pin, self.config_pin,
                                 *[self.installed["py/" + item] for item in names]]
                module = "node.py"
                expected_limits = {"wall_seconds": 450, "cpu_seconds": 450, "memory_mib": 6144,
                    "active_processes": 8, "request_bytes": 131072, "stdout_bytes": MIB,
                    "stderr_bytes": 65536, "event_bytes": 65536}
            else:
                names = ("admin_worker.py", "node.py", "capacity.py", "storage.py", "domains.py",
                         "run_stage.py", "supervise.py", "admin_manage.py")
                expected_pins = [self.python_pin, self.config_pin, self.installed["manage.py"],
                                 *[self.installed["py/" + item] for item in names]]
                module = "admin_worker.py"
                expected_limits = {"wall_seconds": 10, "cpu_seconds": 5, "memory_mib": 128,
                    "active_processes": 8, "request_bytes": 16384, "stdout_bytes": 65536,
                    "stderr_bytes": 65536, "event_bytes": 65536}
            require(receipt["pins"] == expected_pins and set(receipt["files"]) ==
                    {"request.json", "command.json", "stdout.txt", "stderr.txt", "event.json"}, "EXACT_PUBLIC_ROLES")
            require(all(receipt["limits"][key] == value for key, value in expected_limits.items())
                    and receipt["sampled_peak_active_processes"] <= 8
                    and 0 <= receipt["final_job"]["cpu_seconds"] <= expected_limits["cpu_seconds"]
                    and 0 <= receipt["wall_seconds"] <= expected_limits["wall_seconds"]
                    and 0 <= receipt["final_job"]["peak_job_private_commit_bytes"] <= expected_limits["memory_mib"] * MIB,
                    "EXACT_PUBLIC_LIMITS")
            for item in receipt["pins"]:
                require(pin(item["path"]) == item, "PUBLIC_PIN")
            for filename, metadata in receipt["files"].items():
                actual = pin(public / filename)
                require(metadata["present"] is True and actual["bytes"] == metadata["bytes"]
                        and actual["sha256"] == metadata["sha256"], "PUBLIC_OUTPUT_BINDING")
            require(read(public / "request.json", 131072) == raw
                    and read(public / "stdout.txt", MIB) == output, "EXACT_PUBLIC_IO")
            event = strict(read(public / "event.json", 65536))
            require(receipt["request_sha256"] == sha(raw) and event["request_sha256"] == sha(raw)
                    and event["response_sha256"] == sha(output), "EVENT_IO_BINDING")
            if role == "ordinary":
                require(event["origin_directory"] == str(public), "ORDINARY_ORIGIN_BINDING")
            else:
                require(event["operation"] == strict(raw)["op"] and event["checker_loaded"] is False
                        and event["stages_allocated"] == 0 and "origin_directory" not in event,
                        "ADMIN_EVENT_ROLE")
                require(len(list(public.iterdir())) <= 16 and sum(path.stat().st_size for path in public.iterdir()) <= MIB,
                        "ADMIN_DIAGNOSTIC_BOUND")
            actual_command = strict(read(public / "command.json", 65536))
            require(actual_command["argv"] == [sys.executable, *FLAGS, str(self.install / "py" / module),
                    "--config", str(self.config), "--state", str(self.state), "--request",
                    str(public / "request.json"), "--event", str(public / "event.json")]
                    and actual_command["cwd"] == str(self.install / "py") and actual_command["shell"] is False
                    and actual_command["creationflags"] == 0x4 | subprocess.CREATE_NO_WINDOW
                    and actual_command["environment_override"] == {"PYTHONDONTWRITEBYTECODE": "1"}, "PUBLIC_COMMAND")
            observation["event"] = pin(public / "event.json")
            save(directory / "binding.json", observation)
            self.events[name] = event
        require(process.returncode == 0, "CLI_FAILED:" + name)
        return output, strict(output), event

    def request(self, name, op=None, arguments=None, *, client="local", replay=None):
        raw = read(self.driver / "requests" / (replay + ".json"), 131072) if replay else encode(
            {"client": client, "request_id": name, "op": op, "args": arguments})
        path = self.driver / "requests" / (name + ".json")
        save_raw(path, raw)
        before = self.snapshot(name + "-before") if (self.state / "control.sqlite3").exists() else None
        output, value, event = self.cli(name, [self.install / "manage.py", "request", "--config", self.config,
                                             "--request", path], raw, role="ordinary")
        after = self.snapshot(name + "-after")
        if replay:
            require(output == read(self.driver / "calls" / replay / "stdout.txt", MIB)
                    and after == before and event["historical"] is True
                    and event["checker_loaded"] is False and event["stages_allocated"] == 0
                    and "admission_physical_supply" not in event, "EXACT_ORDINARY_REPLAY")
        return value, event, before, after, raw, output

    def admin(self, name, *, addition=None, replay=None):
        op = "renew" if addition is not None or replay else "status"
        raw = read(self.driver / "requests" / (replay + ".json"), 4096) if replay else encode(
            {"schema": 1, "op": op, "config": self.config_id, **(
                {"grant_id": name, "add": addition} if addition is not None else {})})
        path = self.driver / "requests" / (name + ".json")
        save_raw(path, raw)
        before = self.snapshot(name + "-before")
        state_files = self.file_map(self.state) if op == "status" else None
        argv = [self.install / "manage.py", op, "--config", self.config]
        if op == "renew":
            argv.extend(["--request", path])
        output, value, event = self.cli(name, argv, raw, role="administrative")
        after = self.snapshot(name + "-after")
        if replay:
            require(output == read(self.driver / "calls" / replay / "stdout.txt", 65536)
                    and after == before and event["renewal_historical"] is True
                    and event["renewal_state_outcome"] == "ORIGINAL_GRANT_RESPONSE_REPLAYED"
                    and "renewal_physical_supply" not in event, "EXACT_GRANT_REPLAY")
        elif op == "status":
            require(before == after and self.file_map(self.state) == state_files
                    and event["renewal_historical"] is False, "STATUS_READ_ONLY")
            save(self.driver / "snapshots" / (name + "-state-files.json"), state_files)
        return value, event, before, after, raw, output

    def data(self, snapshot, handle):
        rows = [row for row in snapshot["records"] if row["handle"] == handle]
        require(len(rows) == 1, "RECORD_SINGLETON")
        raw = bytes.fromhex(rows[0]["raw"]["hex"])
        require(handle == rows[0]["kind"] + ":" + sha(raw), "RECORD_DIGEST")
        return strict(raw)["data"]

    def assert_state(self, snapshot, used, authorized, grants):
        require(snapshot["meta"] == [{"id": 1, "config": self.config_id, "initialized": 1,
                "requests": used[0], "stages": used[1], "charged": used[2] * MIB, "active": None}], "EXACT_USAGE")
        require(snapshot["authorization"] == [{"id": 1, "config": self.config_id,
                "requests": authorized[0], "stages": authorized[1], "reserved_bytes": authorized[2] * MIB,
                "metadata_pages": 8192, "grants": grants}], "EXACT_AUTHORIZATION")
        require(len(snapshot["requests"]) == used[0] and len(snapshot["stages"]) == used[1]
                and len(snapshot["owner_grants"]) == grants, "EXACT_LEDGER_COUNTS")

    def metadata_delta(self, invocation):
        _value, event, before, after, raw, output = invocation
        request = strict(raw)
        key = sha(encode([request["client"], request["request_id"]]))
        expected = deepcopy(before)
        expected["meta"][0]["requests"] += 1
        expected["meta"][0]["charged"] += 8 * MIB
        expected["meta"][0]["active"] = None
        expected["requests"].append({"key": key, "client": request["client"], "request_id": request["request_id"],
            "raw": blob(raw), "phase": "terminal", "response": blob(output)})
        expected["requests"].sort(key=lambda row: row["key"])
        marker = encode({"config": self.config_id, "kind": "attempt", "client": "owner",
                         "data": {"request": key, "call_directory": event["origin_directory"]}})
        expected["records"].append({"handle": "attempt:" + sha(marker), "kind": "attempt", "client": "owner", "raw": blob(marker)})
        expected["records"].sort(key=lambda row: row["handle"])
        require(after == expected and event["stages_allocated"] == 0, "EXACT_METADATA_DELTA")

    def grant_delta(self, invocation):
        value, event, before, after, raw, output = invocation
        parsed, expected = strict(raw), deepcopy(before)
        authority = expected["authorization"][0]
        old = {key: authority[key] for key in ("requests", "stages", "reserved_bytes")}
        for key, increment in parsed["add"].items():
            authority[key] += increment
        authority["grants"] += 1
        new = {key: authority[key] for key in old}
        used = {"requests": before["meta"][0]["requests"], "stages": before["meta"][0]["stages"],
                "reserved_bytes": before["meta"][0]["charged"]}
        response = {"status": "OK", "grant_id": parsed["grant_id"], "sequence": authority["grants"],
            "config": self.config_id, "authorized_before": old, "authorized_after": new,
            "metadata_cap_before": {"pages": 8192, "bytes": 32 * MIB},
            "metadata_cap_after": {"pages": 8192, "bytes": 32 * MIB}, "used_at_commit": used,
            "mathematicalAcceptance": False, "refund": False, "grant_recorded": True,
            "state_outcome": "RENEWAL_COMMITTED"}
        require(value == response and output == encode(response), "EXACT_GRANT_RESPONSE")
        expected["owner_grants"].append({"grant_id": parsed["grant_id"], "sequence": authority["grants"],
                                         "raw": blob(raw), "response": blob(output)})
        require(after == expected and event["renewal_historical"] is False
                and event["renewal_state_outcome"] == "RENEWAL_COMMITTED", "EXACT_GRANT_DELTA")
        supply(event["renewal_physical_supply"], new["reserved_bytes"] - used["reserved_bytes"], enforced=True)

    def status(self, name, used, grants, context, snapshot):
        invocation = self.admin(name)
        value, _event, _before, after, _raw, _output = invocation
        self.assert_state(after, used, used, grants)
        vector = {"requests": used[0], "stages": used[1], "reserved_bytes": used[2] * MIB}
        require(value["status"] == "STATUS" and value["config"] == self.config_id
                and value["mathematicalAcceptance"] is False and value["state_read_only"] is True
                and value["live_context_status"] == "UNCHECKED" and value["initialized"] == 1
                and value["used"] == vector and value["authorized"] == vector
                and value["remaining"] == dict.fromkeys(vector, 0) and value["active"] is None
                and value["pending_request"] is None and value["grants"] == grants
                and value["heads"] == [{"client": "local", "context": context}]
                and value["provider"] == {"cut": 0, "snapshot": snapshot}
                and value["metadata"]["pages"] == self.snapshots[-1]["pages"]
                and value["metadata"]["freelist_pages"] == self.snapshots[-1]["freelist_pages"]
                and value["metadata_pages"] == 8192 and value["physical_supply_error"] is None, "EXACT_STATUS")
        supply(value["physical_supply"], 0, enforced=False)
        return after

    def run(self, launch):
        require(type(launch) is dict and set(launch) == {"schema", "pins", "product", "limits", "retained"}
                and type(launch["schema"]) is int and launch["schema"] == 1
                and encode(launch["limits"]) == encode(LIMITS)
                and encode(launch["retained"]) == encode(RETAINED), "EXACT_LAUNCH_FIELDS")
        runtime = SOURCE / "runtime/lean-4.34.0-windows"
        paths = [Path(sys.executable), SOURCE / "tests/run_capacity_native.py", Path(__file__).resolve(),
            SOURCE / "tests/scenario_profile.py", PRODUCT / "py/run_stage.py", PRODUCT / "py/supervise.py",
            PRODUCT / "py/domains.py", runtime / "bin/lean.exe"]
        require(encode(launch["pins"]) == encode([pin(path) for path in paths]), "EXACT_ORDERED_SOURCE_PINS")
        expected_product = [dict(relative=path.relative_to(PRODUCT).as_posix(), **pin(path)) for path in product_paths()]
        require(encode(launch["product"]) == encode(expected_product), "EXACT_PRODUCT_PINS")
        self.python_pin = pin(sys.executable)
        self.install.mkdir()
        for item in expected_product:
            relative = PurePosixPath(item["relative"])
            require(not relative.is_absolute() and ".." not in relative.parts and ":" not in str(relative)
                    and "\\" not in str(relative), "PRODUCT_RELATIVE")
            raw = read(PRODUCT / str(relative))
            require(len(raw) == item["bytes"] and sha(raw) == item["sha256"], "PRODUCT_CHANGED_BEFORE_COPY")
            save_raw(self.install / str(relative), raw)
            copied = pin(self.install / str(relative))
            require(copied["bytes"] == item["bytes"] and copied["sha256"] == item["sha256"], "PRODUCT_COPY")
            self.installed[str(relative)] = copied
        save(self.driver / "installed-source-pins.json", list(self.installed.values()))
        require(not any(name in sys.modules for name in ("storage", "capacity")), "PRODUCT_READER_ALREADY_IMPORTED")
        sys.path.insert(0, str(self.install / "py"))
        import storage
        import capacity
        for module, name in ((storage, "storage.py"), (capacity, "capacity.py")):
            require(pin(module.__file__) == self.installed["py/" + name], "READONLY_OBSERVER_MODULE_ORIGIN")
        self.owner_lock = storage.owner_lock
        self.cli("build", [self.install / "build.py", "--lean-runtime", runtime, "--work", DATA / "build-work"])
        build = strict(read(self.install / "build/build-receipt.json"))
        support = strict(read(build["stage_receipt"]["path"]))
        require(build["status"] == "LOCAL_SUPPORT_BUILD_COMPLETED_NOT_MATH_ACCEPTANCE"
                and build["mathematicalAcceptance"] is False and build["stage_receipt"] == pin(build["stage_receipt"]["path"])
                and support["status"] == "STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE"
                and len(support["steps"]) == 2 and all(step["exit_code"] == 0 for step in support["steps"])
                and support["execution_endpoint"]["children_quiescent"] is True
                and support["final_job"]["active_processes"] == 0, "SUPPORT_BUILD")
        _output, configured, _event = self.cli("configure", [self.install / "manage.py", "configure", "--state", self.state,
            "--scratch", self.scratch, "--lean-runtime", runtime, "--client", "local", "--initial-requests", "2",
            "--initial-stages", "1", "--initial-reserved-mib", "144", "--initial-metadata-mib", "32"])
        config = strict(read(self.config))
        self.config_pin, self.config_id = pin(self.config), sha(read(self.config))
        require(config["schema"] == 3 and config["clients"] == ["local"] and config["peers"] == {}
                and config["domains"] == {"install": str(self.install), "state": str(self.state),
                    "scratch": str(self.scratch), "lean_runtime": str(runtime)}
                and config["offers"] == [] and len(config["common"]["packages"]) == 5
                and config["limits"]["requests"] == 2 and config["limits"]["stages"] == 1
                and config["limits"]["staging_bytes"] == 144 * MIB and config["limits"]["metadata_pages"] == 8192
                and config["limits"]["request_bytes"] == 8 * MIB and config["limits"]["stage_bytes"] == 128 * MIB
                and config["limits"]["packages"] == 16 and not (self.state / "control.sqlite3").exists()
                and configured["status"] == "CONFIGURED_NOT_INITIALIZED" and configured["config"] == self.config_pin,
                "FRESH_V3_SMALL_AUTHORIZATION")
        supply(configured["initial_physical_supply"], 144 * MIB, enforced=True)
        save_raw(self.driver / "RenewalCompose.lean", FIXTURE.encode("utf-8"))
        init = self.request("init", "init", {}, client="owner")
        require(init[0].get("accepted") is True, "INIT_ACCEPTANCE")
        c0, s0 = init[0]["contexts"]["local"], init[0]["snapshots"]["P1"]
        require(len(self.data(init[3], c0)["packages"]) == 5, "BOOTSTRAP_FIVE")
        self.assert_state(init[3], (1, 1, 136), (2, 1, 144), 0)
        supply(init[1]["initial_physical_supply"], 144 * MIB, enforced=True)
        supply(init[1]["admission_physical_supply"], 144 * MIB, enforced=True)
        refused = self.request("submit-exhausted", "submit", {"context": c0, "source": FIXTURE, "root": "RenewalCompose"})
        require(refused[0]["status"] == "REFUSED"
                and refused[0]["code"] == "SELECTED_CHECK_FAILED:Refusal:STAGE_QUOTA"
                and "accepted" not in refused[0]
                and refused[1]["checker_loaded"] is True and refused[1]["checker_metrics"]["stage_allocations"] == 0
                and refused[1]["checker_metrics"]["pipeline_children"] == 0, "EXACT_STAGE_QUOTA_REFUSAL")
        self.metadata_delta(refused)
        self.assert_state(refused[3], (2, 1, 144), (2, 1, 144), 0)
        supply(refused[1]["admission_physical_supply"], 8 * MIB, enforced=True)
        frozen = self.file_map(self.state / "work")
        save(self.driver / "preserved-work-before-renewal.json", frozen)
        self.status("status-exhausted", (2, 1, 144), 0, c0, s0)
        state_files = self.file_map(self.state)
        quota = self.request("info-no-credit", "info", {})
        require(quota[0]["status"] == "REFUSED" and quota[0]["code"] == "REQUEST_QUOTA"
                and quota[2] == quota[3] and state_files == self.file_map(self.state)
                and quota[1]["stages_allocated"] == 0 and quota[1]["checker_loaded"] is False
                and "admission_physical_supply" not in quota[1], "NO_RESERVATION_QUOTA_REFUSAL")
        g1 = self.admin("G1", addition={"requests": 1, "stages": 1, "reserved_bytes": 136 * MIB})
        self.grant_delta(g1)
        self.assert_state(g1[3], (2, 1, 144), (3, 2, 280), 1)
        accepted = self.request("submit-renewed", "submit", {"context": c0, "source": FIXTURE, "root": "RenewalCompose"})
        require(accepted[0].get("accepted") is True and accepted[0]["context"] == c0
                and accepted[0]["source_root"] == "RenewalCompose"
                and accepted[0]["source_sha256"] == sha(FIXTURE.encode("utf-8")), "RENEWED_SOURCE_ACCEPTANCE")
        rows = accepted[0]["description"]["rows"]
        require(len(rows) == 1 and rows[0]["kind"] == "definition" and rows[0]["u"] == 1, "SOURCE_DEFINITION_PROFILE")
        artifact = self.data(accepted[3], accepted[0]["artifact"])
        require(artifact["kind"] == "artifact" and artifact["context"] == c0
                and artifact["source_sha256"] == accepted[0]["source_sha256"]
                and artifact["source_root"] == "RenewalCompose"
                and artifact["description"] == accepted[0]["description"], "STORED_ARTIFACT_BINDING")
        self.assert_state(accepted[3], (3, 2, 280), (3, 2, 280), 1)
        supply(accepted[1]["admission_physical_supply"], 136 * MIB, enforced=True)
        self.status("status-renewed-exhausted", (3, 2, 280), 1, c0, s0)
        self.admin("G1-replay", replay="G1")
        g2 = self.admin("G2", addition={"requests": 1, "stages": 0, "reserved_bytes": 8 * MIB})
        self.grant_delta(g2)
        self.assert_state(g2[3], (3, 2, 280), (4, 2, 288), 2)
        info = self.request("info-renewed", "info", {})
        require(info[0]["status"] == "OK" and info[0]["context"] == c0
                and info[0]["snapshots"] == {"P1": s0} and info[0]["description_historical"] is True
                and info[1]["checker_loaded"] is False, "RENEWED_METADATA_SUCCESS")
        self.metadata_delta(info)
        self.assert_state(info[3], (4, 2, 288), (4, 2, 288), 2)
        supply(info[1]["admission_physical_supply"], 8 * MIB, enforced=True)
        self.request("init-replay", replay="init")
        self.request("refusal-replay", replay="submit-exhausted")
        self.request("source-replay", replay="submit-renewed")
        self.admin("G2-replay", replay="G2")
        final = self.status("status-final", (4, 2, 288), 2, c0, s0)
        require(final["heads"] == [{"client": "local", "context": c0}]
                and final["providers"] == [{"provider": "P1", "cut": 0, "snapshot": s0}]
                and not final["entries"], "PRIVATE_ARTIFACT_NO_HEAD_OR_PUBLICATION_CHANGE")
        actual_stages = []
        sequence = (("init", "owner", "bootstrap", 1), ("submit-renewed", "local", "submit", 5))
        require(len(final["stages"]) == 2, "TWO_RECEIVER_STAGES")
        for index, (stage, (identity, client, purpose, children)) in enumerate(zip(final["stages"], sequence)):
            key = sha(encode([client, identity]))
            directory = self.state / "work" / key / ("stage-%04d" % index)
            require(stage == {"id": index, "request": key, "purpose": purpose,
                    "directory": str(directory), "grant_bytes": 128 * MIB}, "EXACT_STAGE_ASSIGNMENT")
            path, plan_path = directory / "stage.json", directory / "plan.json"
            receipt, plan = strict(read(path, MIB)), strict(read(plan_path, MIB))
            require(receipt["status"] == "STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE"
                    and receipt["final_job"]["active_processes"] == 0
                    and receipt["execution_endpoint"]["children_quiescent"] is True
                    and all(step["exit_code"] == 0 for step in receipt["steps"]), "NATIVE_STAGE_RECEIPT")
            require(plan["schema"] == 2 and receipt["stage"] == str(index) and receipt["accounting_root"] == str(directory)
                    and receipt["request_directory"] == str(directory.parent)
                    and receipt["plan"] == pin(plan_path) and receipt["expected_plan_sha256"] == sha(read(plan_path, MIB))
                    and plan["stage"] == str(index) and plan["stage_directory"] == str(directory)
                    and plan["request_directory"] == str(directory.parent)
                    and receipt["domains"] == config["domains"] and plan["domains"] == config["domains"]
                    and len(receipt["steps"]) == children and len(plan["steps"]) == children
                    and self.events[identity]["stages_allocated"] == 1
                    and self.events[identity]["checker_metrics"]["stage_allocations"] == 1
                    and self.events[identity]["checker_metrics"]["pipeline_children"] == children, "STAGE_PLAN_BINDING")
            actual_stages.append({"receipt": pin(path), "children": len(receipt["steps"])})
        require(sum(stage["children"] for stage in actual_stages) == 6, "EXACT_PIPELINE_COUNT")
        later = self.file_map(self.state / "work")
        require(all(later.get(name) == value for name, value in frozen.items()), "OLD_WORK_CHANGED")
        for table, key in (("records", "handle"), ("requests", "key"), ("stages", "id")):
            current = {row[key]: row for row in final[table]}
            require(all(current.get(row[key]) == row for row in refused[3][table]), "OLD_" + table + "_CHANGED")
        require(all(final[table] == refused[3][table] for table in ("heads", "entries", "providers", "snapshots")),
                "OLD_CONTEXT_AND_PUBLICATION_STATE_CHANGED")
        require(len(self.calls) == 17 and sum(item["role"] == "ordinary" for item in self.calls) == 8
                and sum(item["role"] == "administrative" for item in self.calls) == 7
                and sum(item["role"] == "preparation" for item in self.calls) == 2, "EXACT_CLI_COUNTS")
        for item in self.installed.values():
            require(pin(item["path"]) == item, "INSTALLED_SOURCE_CHANGED")
        require(pin(self.config) == self.config_pin, "CONFIG_CHANGED")
        save(self.driver / "sequence.json", {"calls": self.calls, "snapshots": self.snapshots,
            "bootstrap_context": c0, "snapshot": s0, "artifact": accepted[0]["artifact"], "stages": actual_stages,
            "source_authorship": "fixed noncomputable engineering fixture; not discovery or novelty",
            "outcome_audit": "PENDING; independently bind native capture/replay and all observed transitions"})
        return {"status": "PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT", "calls": 17, "ordinary_calls": 8,
            "administrative_calls": 7, "ordinary_requests": 4, "owner_grants": 2, "native_stages": 2,
            "pipeline_children": 6, "support_build_stages": 1, "support_compilations": 2, "charged_bytes": 288 * MIB}


def main():
    parser = argparse.ArgumentParser()
    for name in ("config", "state", "request", "event"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    require(os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_site and sys.flags.no_user_site, "WINDOWS_STARTUP_PROFILE")
    raw = read(args.request, 1024)
    require(raw == REQUEST and args.state.resolve() == DATA and DATA.is_dir()
            and not any(DATA.iterdir()), "FIXED_FRESH_STATE_REQUEST")
    require(args.event.is_absolute() and args.event.parent == args.request.parent
            and not args.event.exists(), "WORKER_EVENT_PATH")
    scenario, started = Scenario(), time.monotonic()
    try:
        result = scenario.run(strict(read(args.config, 131072)))
    except BaseException as error:
        result = {"status": "FAIL", "error": type(error).__name__, "detail": str(error)[:1024],
            "completed_cli_observations": len(scenario.calls), "native_work": "inspect actual retained prefix, not zero"}
        save(scenario.driver / "failed-prefix.json", {"calls": scenario.calls, "snapshots": scenario.snapshots,
                                                     "failure": result})
    result["scope"], result["elapsed_seconds"] = SCOPE, time.monotonic() - started
    reply = encode(result)
    require(len(reply) <= 65536, "WORKER_RESPONSE_BOUND")
    save(args.event, {"request_sha256": sha(raw), "response_sha256": sha(reply), "scope": SCOPE})
    sys.stdout.buffer.write(reply)
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

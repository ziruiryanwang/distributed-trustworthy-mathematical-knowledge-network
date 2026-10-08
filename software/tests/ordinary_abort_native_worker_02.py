"""Nine-invocation native ordinary-abort experiment inside one reviewed outer Job.

Transparent native-renewal adaptation; no prior driver imported. Product code
alone writes state: eight installed CLIs and one direct supervised original call.
The explicit test hook observes a real native child then uses base Job cleanup.
"""
import argparse
from copy import deepcopy
import ctypes as C
from ctypes import wintypes as W
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
from types import SimpleNamespace

SOURCE = Path(__file__).resolve().parents[1]
PRODUCT = SOURCE
DATA = SOURCE.parent / "product-local/ordinary-abort-native-02"
FLAGS = ["-B", "-E", "-s", "-S"]
MIB = 1048576
LIMITS = {"wall_seconds": 450, "cpu_seconds": 450, "memory_mib": 6144,
          "active_processes": 16, "stdout_bytes": 65536, "stderr_bytes": 65536, "event_bytes": 65536}
RETAINED = {"bytes": 1073741824, "files": 16384, "entries": 32768}
REQUEST = b'{"op":"test-ordinary-abort-native"}\n'
SCOPE = "fixed native ordinary-abort continuation; not crash repair or useful-growth qualification"
TABLES = {"meta": "id", "authorization": "id", "owner_grants": "sequence",
          "requests": "key", "records": "handle", "heads": "client", "providers": "provider",
          "snapshots": "handle", "entries": "provider,seq", "stages": "id"}
FIXTURE = """universe u
noncomputable def AbortCompose (A B C : Sort u)
    (g : B -> C) (f : A -> B) (a : A) : C :=
  g (f a)
"""
PUBLIC_LIMITS = {"wall_seconds": 450, "cpu_seconds": 450, "memory_mib": 6144,
    "active_processes": 8, "request_bytes": 131072, "stdout_bytes": MIB,
    "stderr_bytes": 65536, "event_bytes": 65536}
RECOVERY_LIMITS = {"wall_seconds": 30, "cpu_seconds": 15, "memory_mib": 256,
    "active_processes": 8, "request_bytes": 16384, "stdout_bytes": MIB,
    "stderr_bytes": 65536, "event_bytes": 65536, "poll_seconds": 0.05, "settle_seconds": 5}
INTERRUPTED = b'{"code":"INTERRUPTED_ORDINARY_OPERATION","status":"REFUSED"}\n'


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


def submission_steps():
    def native(args):
        return {"kind": "lean", "label": "selected-native", "lean_path": ["$RUN/input/lib"],
            "cwd": "$RUN/input/native", "argv": ["-R", "$RUN/input/native", "--run",
            "$RUN/input/native/AgentClient.lean", *args], "expected_exit": 0}
    def worker(action, capture, output):
        return {"kind": "python", "label": action, "argv": [*FLAGS, "$RUN/input/checking.py", "_worker",
            action, "$RUN/input/job.json", capture, output]}
    return [native(["--check-source", "$RUN/input/plan.json", "--inventory", "$RUN/input/inventory.json",
                    "--source", "$RUN/input/source.lean", "--root", "AbortCompose"]),
        worker("capture", "$RUN/00.stdout.log", "$RUN/out/candidate"),
        native(["--describe", "$RUN/out/candidate/plan.json", "--inventory", "$RUN/input/inventory.json",
                "--requests", "$RUN/out/candidate/refs.json"]),
        worker("inverse", "$RUN/02.stdout.log", "$RUN/out/inverse"),
        native(["--describe", "$RUN/out/inverse/plan.json", "--inventory", "$RUN/input/inventory.json",
                "--requests", "$RUN/out/inverse/refs.json"])]


class OrdinaryAbortFaultInjected(RuntimeError):
    pass


class NativeObservation:
    """Pinned test-only observer; actual installed Job object remains unmodified."""
    def __init__(self, scenario, runner, config, key, public):
        self.scenario, self.runner, self.config = scenario, runner, config
        self.public, self.stage = public, scenario.state / "work" / key / "stage-0001"
        self.job, self.leaf, self.plan, self.snapshot_raw = None, None, None, None
        self.started = time.monotonic()
        self.facts = {"trigger_count": 0, "observations": 0, "partial_reads": 0,
            "post_trigger_callbacks": 0, "handles_opened": 0, "handles_closed": 0,
            "close_errors": [], "trigger": None, "leaf_signalled_after_cleanup": None,
            "observer_limits": {"seconds": 30, "observations": 600, "receipt_bytes": 256 * 1024,
                                "receipt_reads_per_observation": 2, "plan_bytes": MIB},
            "scope": "test-only live-handle/Job observation; original base supervisor owns termination"}
        self.k = C.WinDLL("kernel32", use_last_error=True)
        self.k.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
        self.k.OpenProcess.restype = W.HANDLE
        self.k.CloseHandle.argtypes = [W.HANDLE]
        self.k.CloseHandle.restype = W.BOOL
        self.k.IsProcessInJob.argtypes = [W.HANDLE, W.HANDLE, C.POINTER(W.BOOL)]
        self.k.IsProcessInJob.restype = W.BOOL
        self.k.QueryFullProcessImageNameW.argtypes = [W.HANDLE, W.DWORD, W.LPWSTR, C.POINTER(W.DWORD)]
        self.k.QueryFullProcessImageNameW.restype = W.BOOL
        self.k.WaitForSingleObject.argtypes = [W.HANDLE, W.DWORD]
        self.k.WaitForSingleObject.restype = W.DWORD

    def capture_job(self, seconds, memory_mib, active_processes):
        require(self.job is None and (seconds, memory_mib, active_processes) == (450, 6144, 8),
                "ONE_UNCHANGED_ORIGINAL_JOB")
        self.job = self.runner.Job(seconds, memory_mib, active_processes)
        return self.job

    def partial(self, path, bound):
        try:
            raw = read(path, bound)
        except FileNotFoundError:
            self.facts["partial_reads"] += 1
            return None
        try:
            value = strict(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.facts["partial_reads"] += 1
            return None
        return raw, value

    def authenticate_plan(self, receipt):
        raw = read(self.stage / "plan.json", MIB)
        plan = strict(raw)
        cfg, s = self.config, self.scenario
        require(plan["schema"] == 2 and plan["domains"] == cfg["domains"]
                and plan["request_directory"] == str(self.stage.parent)
                and plan["stage_directory"] == str(self.stage) and plan["stage"] == "1"
                and plan["domains_source"] == cfg["files"]["domains"]
                and plan["expected_runner_sha256"] == cfg["files"]["runner"]["sha256"]
                and plan["lean"] == cfg["files"]["lean"] and plan["python"] == s.python_pin
                and plan["seconds"] == cfg["limits"]["native_seconds"]
                and plan["memory_mib"] == cfg["limits"]["native_memory_mib"]
                and plan["bytes"] == 128 * MIB and plan["steps"] == submission_steps(), "HOOK_PLAN")
        selected = [row for row in plan["inputs"] if row.get("as") == "source.lean"]
        source = FIXTURE.encode("utf-8")
        require(len(selected) == 1 and selected[0] == {"as": "source.lean",
                "path": str(self.stage.parent / "owner-source.lean"), "bytes": len(source), "sha256": sha(source)}
                and read(self.stage / "input/source.lean", 65536) == source
                and read(self.stage.parent / "owner-source.lean", 65536) == source, "HOOK_SOURCE")
        job = strict(read(self.stage / "input/job.json", MIB))
        require(job["root"] == "AbortCompose" and job["source_sha"] == sha(source)
                and job["domains"] == cfg["domains"], "HOOK_SOURCE_ROOT")
        require(receipt["expected_plan_sha256"] == sha(raw)
                and receipt["plan"] == pin(self.stage / "plan.json")
                and receipt["lean"] == cfg["files"]["lean"] and receipt["python"] == s.python_pin
                and receipt["runner"] == pin(self.stage / "run_stage.py")
                and receipt["runner"]["sha256"] == cfg["files"]["runner"]["sha256"], "HOOK_RECEIPT_PINS")
        self.plan = plan
        self.facts["plan"] = pin(self.stage / "plan.json")

    def close_handle(self, handle):
        if not self.k.CloseHandle(handle):
            self.facts["close_errors"].append("CloseHandle:" + str(C.get_last_error()))
            raise RuntimeError("HOOK_HANDLE_CLOSE_FAILED")
        self.facts["handles_closed"] += 1

    def observe(self, directory):
        require(directory == self.public, "HOOK_PUBLIC_DIRECTORY")
        if self.facts["trigger_count"]:
            # Base currently calls no output callback during failure cleanup;
            # explicitly make any later callback observation-only, never a retrigger.
            self.facts["post_trigger_callbacks"] += 1
            return
        self.facts["observations"] += 1
        require(self.facts["observations"] <= 600 and time.monotonic() - self.started <= 30,
                "HOOK_OBSERVATION_BUDGET_EXHAUSTED")
        require(self.job is not None and self.job.handle, "HOOK_ORIGINAL_JOB_UNAVAILABLE")
        selected = self.partial(self.stage / "stage.json", 256 * 1024)
        if selected is None:
            return
        raw, receipt = selected
        require(type(receipt) is dict and receipt.get("stage") == "1"
                and receipt.get("domains") == self.config["domains"]
                and receipt.get("request_directory") == str(self.stage.parent)
                and receipt.get("accounting_root") == str(self.stage), "HOOK_RECEIPT_DOMAIN")
        steps = receipt.get("steps")
        require(type(steps) is list and len(steps) <= 1
                and receipt.get("status") in {"PREPARING", "RUNNING"}, "HOOK_FIRST_LEAN_WINDOW_MISSED")
        if not steps:
            return
        step = steps[0]
        require(step.get("index") == 0 and step.get("status") in
                {"STARTING", "SUSPENDED_PENDING_JOB_ASSIGNMENT", "RUNNING"}, "HOOK_FIRST_LEAN_WINDOW_MISSED")
        if receipt["status"] != "RUNNING" or step["status"] != "RUNNING":
            return
        if self.plan is None:
            self.authenticate_plan(receipt)
        require(receipt.get("expected_plan_sha256") == self.facts["plan"]["sha256"], "HOOK_PLAN_CHANGED")
        expand = lambda value: value.replace("$RUN", str(self.stage))
        expected = [self.plan["lean"]["path"], "-j", "1", "-M", str(self.plan["memory_mib"]),
                    *map(expand, self.plan["steps"][0]["argv"])]
        require(type(step.get("pid")) is int and step["pid"] > 0
                and step["command"] == expected and step["cwd"] == str(Path(expand(self.plan["steps"][0]["cwd"])))
                and step["lean_path"] == [expand(value) for value in self.plan["steps"][0]["lean_path"]],
                "HOOK_ACTUAL_LEAN_COMMAND")
        handle = self.k.OpenProcess(0x0400 | 0x00100000, False, step["pid"])
        require(handle, "HOOK_OPENPROCESS_FAILED:" + str(C.get_last_error()))
        self.facts["handles_opened"] += 1
        retained = False
        try:
            image, size = C.create_unicode_buffer(32768), W.DWORD(32768)
            require(self.k.QueryFullProcessImageNameW(handle, 0, image, C.byref(size))
                    and 0 < size.value < 32768, "HOOK_PROCESS_IMAGE_QUERY")
            actual_image = checked(image.value)
            require(actual_image == checked(self.plan["lean"]["path"]), "HOOK_LEAN_IMAGE")
            member = W.BOOL()
            require(self.k.IsProcessInJob(handle, self.job.handle, C.byref(member)) and member.value,
                    "HOOK_EXACT_ORIGINAL_JOB_MEMBERSHIP")
            repeated = self.partial(self.stage / "stage.json", 256 * 1024)
            if repeated is None or repeated[0] != raw:
                return
            require(time.monotonic() - self.started <= 30, "HOOK_OBSERVATION_BUDGET_EXHAUSTED")
            wait = self.k.WaitForSingleObject(handle, 0)
            require(wait in {0, 258}, "HOOK_PROCESS_WAIT_FAILED")
            if wait == 0:
                return
            elapsed = time.monotonic() - self.started
            require(elapsed <= 30, "HOOK_OBSERVATION_BUDGET_EXHAUSTED")
            self.leaf, self.snapshot_raw, retained = handle, raw, True
            self.facts["trigger"] = {"pid": step["pid"], "image": str(actual_image),
                "original_job_membership": True, "wait_result": wait, "elapsed_seconds": elapsed,
                "stage_receipt_sha256": sha(raw), "stage_receipt_bytes": len(raw), "step": step,
                "command_count_observed": 1, "completed_command_count": None}
            self.facts["trigger_count"] = 1
            raise OrdinaryAbortFaultInjected("FIXED_LIVE_LEAN_ORIGINAL_JOB_FAULT")
        finally:
            if not retained:
                self.close_handle(handle)

    def finish(self):
        if self.leaf is not None:
            handle, self.leaf = self.leaf, None
            try:
                observed = self.k.WaitForSingleObject(handle, 0)
                self.facts["leaf_wait_after_cleanup"] = observed
                self.facts["leaf_signalled_after_cleanup"] = observed == 0
            finally:
                self.close_handle(handle)
        self.facts["elapsed_seconds"] = time.monotonic() - self.started


class Scenario:
    def __init__(self):
        self.install, self.state, self.scratch, self.driver = (DATA / name for name in
                                                            ("install", "state", "scratch", "driver"))
        self.config = self.state / "config.json"
        self.calls, self.snapshots = [], []
        self.installed, self.events, self.public_receipts = {}, {}, {}
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
        require(role in {"preparation", "ordinary", "recovery"}, "CLI_ROLE")
        directory = self.driver / "calls" / name
        directory.mkdir(parents=True, exist_ok=False)
        command = [sys.executable, *FLAGS, *map(str, arguments)]
        save(directory / "command.json", {"argv": command, "cwd": str(self.install), "shell": False})
        evidence = self.scratch / ("recoveries" if role == "recovery" else "calls")
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
        output = read(directory / "stdout.txt", MIB)
        event = None
        if role != "preparation":
            require(type(raw) is bytes, "EXPECTED_REQUEST_BYTES")
            after = set(evidence.iterdir())
            require(len(after) <= 17 and before <= after and len(after - before) == 1, "ONE_PUBLIC_CALL")
            public = checked((after - before).pop())
            recovery_directory = public if role == "recovery" else None
            if role == "recovery":
                public = checked(public / "cases/recover")
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
                expected_pins = self.ordinary_pins()
                module = "node.py"
                expected_limits = dict(PUBLIC_LIMITS, poll_seconds=0.05, settle_seconds=15)
            else:
                names = ("node.py", "run_stage.py", "storage.py", "capacity.py", "domains.py",
                         "supervise.py", "peer_wire.py", "peer_service.py", "peer_node.py")
                selected = strict(raw)["args"]
                original_pin = pin(selected["supervisor_receipt"])
                inputs = [self.python_pin, self.config_pin,
                    *[self.installed["py/" + item] for item in names],
                    self.installed["py/recovery_worker.py"], self.installed["py/recovery_manage.py"],
                    original_pin, self.installed["manage.py"]]
                grant_path = recovery_directory / "grant.json"
                grant = strict(read(grant_path, 65536))
                require(grant == {"schema": 1, "profile": "draft-owner-recovery-supervision-v1",
                    "request_sha256": sha(raw), "target_client": selected["client"],
                    "target_request_id": selected["request_id"], "original_receipt": original_pin,
                    "worker": str(self.install / "py/recovery_worker.py"), "state": str(self.state),
                    "limits": RECOVERY_LIMITS, "inputs": inputs,
                    "policy": "one explicit invocation; no automatic retries, quota reset, refunds or repair",
                    "close_evidence": "CHECKED_CLOSEHANDLE_RETURN; final active-zero and child reap required independently"},
                    "EXACT_RECOVERY_GRANT")
                expected_pins = [*inputs, pin(grant_path)]
                module, expected_limits = "recovery_worker.py", RECOVERY_LIMITS
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
                require(event["recovery_profile"] == "draft-native-free-ordinary-abort-v1"
                        and event["checker_loaded"] is False and event["stages_allocated"] == 0
                        and event["native_stages"] == 0 and event["original_outputs_used"] is False
                        and event["mathematical_acceptance_authority"] is False
                        and event["original_receipt"] == original_pin
                        and "origin_directory" not in event, "RECOVERY_EVENT_ROLE")
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
            self.public_receipts[name] = receipt_path
        require(process.returncode == 0, "CLI_FAILED:" + name)
        return output, strict(output), event

    def request(self, name, op=None, arguments=None, *, client="local", replay=None, expected_response=None):
        raw = read(self.driver / "requests" / (replay + ".json"), 131072) if replay else encode(
            {"client": client, "request_id": name, "op": op, "args": arguments})
        path = self.driver / "requests" / (name + ".json")
        save_raw(path, raw)
        before = self.snapshot(name + "-before") if (self.state / "control.sqlite3").exists() else None
        output, value, event = self.cli(name, [self.install / "manage.py", "request", "--config", self.config,
                                             "--request", path], raw, role="ordinary")
        after = self.snapshot(name + "-after")
        if replay:
            expected_response = (read(self.driver / "calls" / replay / "stdout.txt", MIB)
                                 if expected_response is None else expected_response)
            require(output == expected_response
                    and after == before and event["historical"] is True
                    and event["checker_loaded"] is False and event["stages_allocated"] == 0
                    and "admission_physical_supply" not in event, "EXACT_ORDINARY_REPLAY")
        return value, event, before, after, raw, output

    def ordinary_pins(self):
        names = ("node.py", "run_stage.py", "storage.py", "capacity.py", "checking.py", "domains.py",
                 "supervise.py", "peer_wire.py", "peer_service.py", "peer_node.py")
        return [self.python_pin, self.config_pin, *[self.installed["py/" + name] for name in names]]

    def recovery(self, name, target, *, replay=None, expected_response=None):
        raw = read(self.driver / "requests" / (replay + ".json"), 16384) if replay else encode({
            "client": "owner", "op": "recover_ordinary", "args": {"client": "local",
            "request_id": target, "supervisor_receipt": str(self.public_receipts[target])}})
        path = self.driver / "requests" / (name + ".json")
        save_raw(path, raw)
        before = self.snapshot(name + "-before")
        work, calls = self.file_map(self.state / "work"), self.file_map(self.scratch / "calls")
        output, value, event = self.cli(name, [self.install / "manage.py", "recover", "--config", self.config,
                                             "--request", path], raw, role="recovery")
        after = self.snapshot(name + "-after")
        require(work == self.file_map(self.state / "work") and calls == self.file_map(self.scratch / "calls"),
                "RECOVERY_ORIGINAL_FILES_CHANGED")
        save(self.driver / "preserved" / (name + ".json"), {"work": work, "calls": calls})
        if expected_response is not None:
            require(output == expected_response and after == before and event["historical"] is True
                    and event["transition_committed"] is False and event["terminal_write_attempted"] is False
                    and event["state_outcome"] == "ORIGINAL_TERMINAL_RESPONSE_REPLAYED", "EXACT_RECOVERY_REPLAY")
        else:
            require(output == INTERRUPTED and event["historical"] is False
                    and event["transition_committed"] is True and event["quiescence_authenticated"] is True
                    and event["state_outcome"] == "INTERRUPTED_RESPONSE_COMMITTED", "ACTUAL_ABORT")
            expected = deepcopy(before)
            key = sha(encode(["local", target]))
            require(expected["meta"][0]["active"] == key, "ABORT_ACTIVE_BEFORE")
            selected = [row for row in expected["requests"] if row["key"] == key]
            require(len(selected) == 1 and selected[0]["phase"] == "pending" and selected[0]["response"] is None,
                    "ABORT_PENDING_BEFORE")
            selected[0].update(phase="terminal", response=blob(INTERRUPTED))
            expected["meta"][0]["active"] = None
            require(after == expected, "EXACT_ABORT_DELTA")
        return value, event, before, after, raw, output

    def interrupted(self, context, config):
        name = "submit-interrupted"
        raw = encode({"client": "local", "request_id": name, "op": "submit",
                      "args": {"context": context, "source": FIXTURE, "root": "AbortCompose"}})
        save_raw(self.driver / "requests" / (name + ".json"), raw)
        before = self.snapshot(name + "-before")
        before_work, before_calls = self.file_map(self.state / "work"), self.file_map(self.scratch / "calls")
        key = sha(encode(["local", name]))
        public = self.scratch / "calls/call-abort-original"
        require(not public.exists(), "FRESH_ORIGINAL_FAULT_CALL")
        import run_stage
        import supervise
        for module, filename in ((run_stage, "run_stage.py"), (supervise, "supervise.py"),
                                 (run_stage.domain_module, "domains.py")):
            require(pin(module.__file__) == self.installed["py/" + filename], "FAULT_MODULE_ORIGIN")
        observer = NativeObservation(self, run_stage, config, key, public)
        class FaultTransport(supervise.Transport):
            def output_within_bounds(self, directory):
                result = super().output_within_bounds(directory)
                observer.observe(directory)
                return result
        # The adapter exposes the actual implementation file for the base pin
        # check. Only this pinned test worker supplies the additional capture.
        adapter = SimpleNamespace(__file__=run_stage.__file__, Job=observer.capture_job)
        transport = FaultTransport(sys.executable, self.install / "py/node.py", self.config,
            self.state, self.scratch / "calls", adapter, dict(PUBLIC_LIMITS, pins=self.ordinary_pins()))
        record = {"name": name, "role": "ordinary", "direct_supervised": True,
                  "installed_cli": False, "original_directory": str(public)}
        self.calls.append(record)
        receipt, exception, finish_error = None, None, None
        try:
            transport(public.name, raw)
        except supervise.SupervisorFailure as error:
            receipt = error.record
            exception = {"type": type(error).__name__, "detail": str(error)[:1024]}
        except BaseException as error:
            exception = {"type": type(error).__name__, "detail": str(error)[:1024]}
        finally:
            try:
                observer.finish()
            except BaseException as error:
                finish_error = type(error).__name__ + ":" + str(error)[:512]
            supplemental = {"observer": observer.facts, "exception": exception,
                "finish_error": finish_error, "worker": pin(Path(__file__).resolve()),
                "request_sha256": sha(raw), "original_receipt_path": str(public / "supervisor.json")}
            original_receipt_path = public / "supervisor.json"
            supplemental["original_receipt"] = (pin(original_receipt_path)
                if original_receipt_path.is_file() else {"present": False, "outcome": "UNAVAILABLE"})
            if observer.snapshot_raw is not None:
                snapshot_path = self.driver / "hook/observed-stage.json"
                save_raw(snapshot_path, observer.snapshot_raw)
                supplemental["observed_stage_snapshot"] = pin(snapshot_path)
            save(self.driver / "hook/observation.json", supplemental)
        require(receipt is not None and exception["type"] == "SupervisorFailure"
                and finish_error is None and observer.facts["trigger_count"] == 1
                and observer.facts["leaf_signalled_after_cleanup"] is True
                and observer.facts["handles_opened"] == observer.facts["handles_closed"]
                and not observer.facts["close_errors"], "EXACT_LIVE_LEAN_TRIGGER_AND_HANDLES")
        receipt_path = public / "supervisor.json"
        require(strict(read(receipt_path, 65536)) == receipt, "PERSISTED_ORIGINAL_RECEIPT")
        record["public_receipt"] = pin(receipt_path)
        record["actual_job_cpu_seconds"] = receipt.get("final_job", {}).get("cpu_seconds")
        record["cleanup"] = {field: receipt.get(field) for field in
                             ("direct_child_reaped", "final_active_zero", "job_closed", "cleanup_errors")}
        save(self.driver / "calls" / name / "observation.json", record)
        require(receipt["status"] == "TRANSPORT_FAILED" and receipt["native_acceptance"] is False
                and receipt["failure"] == {"type": "OrdinaryAbortFaultInjected",
                                           "detail": "FIXED_LIVE_LEAN_ORIGINAL_JOB_FAULT"}
                and receipt["pins"] == self.ordinary_pins()
                and receipt["bound_pin_count"] == 12
                and receipt["bound_pin_bytes"] == sum(row["bytes"] for row in self.ordinary_pins())
                and receipt["request_sha256"] == sha(raw), "EXPECTED_AUTHENTIC_FAULT_RECEIPT")
        require(all(receipt.get(field) is True for field in
                ("job_created_before_process", "attach_resume_returned", "direct_child_reaped",
                 "final_active_zero", "job_closed", "job_termination_requested"))
                and type(receipt["pid"]) is int and receipt["pid"] > 0
                and type(receipt["returncode"]) is int
                and receipt["initial_job"]["active_processes"] == 0
                and receipt["final_job"]["active_processes"] == 0
                and receipt["final_job"]["total_processes"] >= 1
                and not any(receipt.get(field) for field in
                    ("cleanup_errors", "output_record_error", "evidence_persistence_error")), "ORIGINAL_WHOLE_TREE_QUIESCENCE")
        require(all(receipt["limits"][field] == value for field, value in PUBLIC_LIMITS.items())
                and receipt["limits"]["poll_seconds"] == 0.05 and receipt["limits"]["settle_seconds"] == 15
                and receipt["wall_limit_seconds"] == 450 and receipt["wall_seconds"] <= 450
                and receipt["final_job"]["cpu_seconds"] <= 450
                and receipt["final_job"]["peak_job_private_commit_bytes"] <= 6144 * MIB
                and receipt["sampled_peak_active_processes"] <= 8, "ORIGINAL_PROFILE_UNCHANGED")
        for item in receipt["pins"]:
            require(pin(item["path"]) == item, "ORIGINAL_PIN_CHANGED")
        require(set(receipt["files"]) == {"request.json", "command.json", "stdout.txt", "stderr.txt", "event.json"},
                "ORIGINAL_FILE_SET")
        for filename, metadata in receipt["files"].items():
            path = public / filename
            if metadata["present"] is True:
                actual = pin(path)
                require(actual["bytes"] == metadata["bytes"] and actual["sha256"] == metadata["sha256"],
                        "ORIGINAL_FILE_CHANGED")
            else:
                require(metadata == {"present": False} and not path.exists(), "ORIGINAL_ABSENCE_CHANGED")
        require(read(public / "request.json", 131072) == raw, "ORIGINAL_EXACT_REQUEST")
        require(strict(read(public / "command.json", 65536)) == {"argv": [sys.executable, *FLAGS,
            str(self.install / "py/node.py"), "--config", str(self.config), "--state", str(self.state),
            "--request", str(public / "request.json"), "--event", str(public / "event.json")],
            "cwd": str(self.install / "py"), "shell": False, "creationflags": 134217732,
            "environment_override": {"PYTHONDONTWRITEBYTECODE": "1"}}, "ORIGINAL_ACTUAL_COMMAND")
        self.public_receipts[name] = receipt_path
        after = self.snapshot(name + "-after")
        expected = deepcopy(before)
        expected["meta"][0].update(requests=2, stages=2, charged=272 * MIB, active=key)
        expected["requests"].append({"key": key, "client": "local", "request_id": name,
            "raw": blob(raw), "phase": "pending", "response": None})
        expected["requests"].sort(key=lambda row: row["key"])
        marker = encode({"config": self.config_id, "kind": "attempt", "client": "owner",
                         "data": {"request": key, "call_directory": str(public)}})
        expected["records"].append({"handle": "attempt:" + sha(marker), "kind": "attempt", "client": "owner", "raw": blob(marker)})
        expected["records"].sort(key=lambda row: row["handle"])
        expected["stages"].append({"id": 1, "request": key, "purpose": "submit",
            "directory": str(observer.stage), "grant_bytes": 128 * MIB})
        require(after == expected, "REAL_PENDING_CHARGES_WITHOUT_VISIBILITY")
        later_work, later_calls = self.file_map(self.state / "work"), self.file_map(self.scratch / "calls")
        require(all(later_work.get(name) == value for name, value in before_work.items())
                and all(later_calls.get(name) == value for name, value in before_calls.items()), "PREINTERRUPTION_FILES_CHANGED")
        save(self.driver / "preserved/post-interruption.json", {"work": later_work, "calls": later_calls})
        self.hook_facts = observer.facts
        return after, later_work, later_calls

    def data(self, snapshot, handle):
        rows = [row for row in snapshot["records"] if row["handle"] == handle]
        require(len(rows) == 1, "RECORD_SINGLETON")
        raw = bytes.fromhex(rows[0]["raw"]["hex"])
        require(handle == rows[0]["kind"] + ":" + sha(raw), "RECORD_DIGEST")
        return strict(raw)["data"]

    def assert_state(self, snapshot, used, authorized, grants, *, active=None):
        require(snapshot["meta"] == [{"id": 1, "config": self.config_id, "initialized": 1,
                "requests": used[0], "stages": used[1], "charged": used[2] * MIB, "active": active}], "EXACT_USAGE")
        require(snapshot["authorization"] == [{"id": 1, "config": self.config_id,
                "requests": authorized[0], "stages": authorized[1], "reserved_bytes": authorized[2] * MIB,
                "metadata_pages": 8192, "grants": grants}], "EXACT_AUTHORIZATION")
        require(len(snapshot["requests"]) == used[0] and len(snapshot["stages"]) == used[1]
                and len(snapshot["owner_grants"]) == grants, "EXACT_LEDGER_COUNTS")

    def run(self, launch):
        require(type(launch) is dict and set(launch) == {"schema", "pins", "product", "limits", "retained"}
                and type(launch["schema"]) is int and launch["schema"] == 1
                and encode(launch["limits"]) == encode(LIMITS)
                and encode(launch["retained"]) == encode(RETAINED), "EXACT_LAUNCH_FIELDS")
        runtime = SOURCE / "runtime/lean-4.34.0-windows"
        paths = [Path(sys.executable), SOURCE / "tests/run_ordinary_abort_native_02.py", Path(__file__).resolve(),
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
            "--scratch", self.scratch, "--lean-runtime", runtime, "--client", "local", "--initial-requests", "3",
            "--initial-stages", "3", "--initial-reserved-mib", "408", "--initial-metadata-mib", "32"])
        config = strict(read(self.config))
        self.config_pin, self.config_id = pin(self.config), sha(read(self.config))
        require(config["schema"] == 3 and config["clients"] == ["local"] and config["peers"] == {}
                and config["domains"] == {"install": str(self.install), "state": str(self.state),
                    "scratch": str(self.scratch), "lean_runtime": str(runtime)}
                and config["offers"] == [] and len(config["common"]["packages"]) == 5
                and config["limits"]["requests"] == 3 and config["limits"]["stages"] == 3
                and config["limits"]["staging_bytes"] == 408 * MIB and config["limits"]["metadata_pages"] == 8192
                and config["limits"]["request_bytes"] == 8 * MIB and config["limits"]["stage_bytes"] == 128 * MIB
                and config["limits"]["packages"] == 16 and not (self.state / "control.sqlite3").exists()
                and configured["status"] == "CONFIGURED_NOT_INITIALIZED" and configured["config"] == self.config_pin,
                "FRESH_V3_SMALL_AUTHORIZATION")
        supply(configured["initial_physical_supply"], 408 * MIB, enforced=True)
        save_raw(self.driver / "AbortCompose.lean", FIXTURE.encode("utf-8"))
        init = self.request("init", "init", {}, client="owner")
        require(init[0].get("accepted") is True, "INIT_ACCEPTANCE")
        c0, s0 = init[0]["contexts"]["local"], init[0]["snapshots"]["P1"]
        require(len(self.data(init[3], c0)["packages"]) == 5, "BOOTSTRAP_FIVE")
        self.assert_state(init[3], (1, 1, 136), (3, 3, 408), 0)
        supply(init[1]["initial_physical_supply"], 408 * MIB, enforced=True)
        supply(init[1]["admission_physical_supply"], 408 * MIB, enforced=True)
        pending, frozen_work, frozen_calls = self.interrupted(c0, config)
        interrupted_key = sha(encode(["local", "submit-interrupted"]))
        self.assert_state(pending, (2, 2, 272), (3, 3, 408), 0, active=interrupted_key)
        aborted = self.recovery("abort-original", "submit-interrupted")
        self.assert_state(aborted[3], (2, 2, 272), (3, 3, 408), 0)
        replayed = self.request("interrupted-replay", replay="submit-interrupted", expected_response=aborted[5])
        require(self.file_map(self.state / "work") == frozen_work, "ABORT_REPLAY_WORK_CHANGED")
        accepted = self.request("submit-fresh", "submit", {"context": c0, "source": FIXTURE, "root": "AbortCompose"})
        require(accepted[0].get("accepted") is True and accepted[0]["context"] == c0
                and accepted[0]["source_root"] == "AbortCompose"
                and accepted[0]["source_sha256"] == sha(FIXTURE.encode("utf-8")), "FRESH_SOURCE_ACCEPTANCE")
        rows = accepted[0]["description"]["rows"]
        require(len(rows) == 1 and rows[0]["kind"] == "definition" and rows[0]["u"] == 1, "SOURCE_DEFINITION_PROFILE")
        artifact = self.data(accepted[3], accepted[0]["artifact"])
        require(artifact["kind"] == "artifact" and artifact["context"] == c0
                and artifact["source_sha256"] == accepted[0]["source_sha256"]
                and artifact["source_root"] == "AbortCompose"
                and artifact["description"] == accepted[0]["description"], "STORED_ARTIFACT_BINDING")
        expected = deepcopy(replayed[3])
        key = sha(encode(["local", "submit-fresh"]))
        expected["meta"][0].update(requests=3, stages=3, charged=408 * MIB, active=None)
        expected["requests"].append({"key": key, "client": "local", "request_id": "submit-fresh",
            "raw": blob(accepted[4]), "phase": "terminal", "response": blob(accepted[5])})
        expected["requests"].sort(key=lambda row: row["key"])
        marker = encode({"config": self.config_id, "kind": "attempt", "client": "owner",
            "data": {"request": key, "call_directory": accepted[1]["origin_directory"]}})
        expected["records"].append({"handle": "attempt:" + sha(marker), "kind": "attempt", "client": "owner", "raw": blob(marker)})
        actual_artifacts = [row for row in accepted[3]["records"] if row["handle"] == accepted[0]["artifact"]]
        require(len(actual_artifacts) == 1 and actual_artifacts[0]["kind"] == "artifact"
                and actual_artifacts[0]["client"] == "local", "ONE_NEW_ARTIFACT")
        expected["records"].extend(actual_artifacts)
        expected["records"].sort(key=lambda row: row["handle"])
        expected["stages"].append({"id": 2, "request": key, "purpose": "submit",
            "directory": str(self.state / "work" / key / "stage-0002"), "grant_bytes": 128 * MIB})
        require(accepted[3] == expected, "EXACT_FRESH_SUBMISSION_DELTA")
        self.assert_state(accepted[3], (3, 3, 408), (3, 3, 408), 0)
        supply(accepted[1]["admission_physical_supply"], 136 * MIB, enforced=True)
        self.recovery("abort-replay", "submit-interrupted", replay="abort-original", expected_response=aborted[5])
        terminal = self.recovery("success-replay", "submit-fresh", expected_response=accepted[5])
        final = terminal[3]
        self.assert_state(final, (3, 3, 408), (3, 3, 408), 0)
        require(final["heads"] == [{"client": "local", "context": c0}]
                and final["providers"] == [{"provider": "P1", "cut": 0, "snapshot": s0}]
                and not final["entries"], "PRIVATE_ARTIFACT_NO_HEAD_OR_PUBLICATION_CHANGE")
        actual_stages = []
        sequence = ((0, "init", "owner", "bootstrap", 1), (2, "submit-fresh", "local", "submit", 5))
        require(len(final["stages"]) == 3, "THREE_CHARGED_RECEIVER_STAGES")
        for index, identity, client, purpose, children in sequence:
            stage = final["stages"][index]
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
            if identity == "submit-fresh":
                require(plan["steps"] == submission_steps(), "FRESH_COMPLETE_SUBMISSION_PLAN")
            actual_stages.append({"receipt": pin(path), "completed_commands": len(receipt["steps"])})
        require(sum(stage["completed_commands"] for stage in actual_stages) == 6, "SIX_NORMAL_COMPLETED_COMMANDS")
        later_work, later_calls = self.file_map(self.state / "work"), self.file_map(self.scratch / "calls")
        require(all(later_work.get(name) == value for name, value in frozen_work.items())
                and all(later_calls.get(name) == value for name, value in frozen_calls.items()), "ORIGINAL_WORK_AND_CALL_CHANGED")
        for table, field in (("records", "handle"), ("requests", "key"), ("stages", "id")):
            current = {row[field]: row for row in final[table]}
            require(all(current.get(row[field]) == row for row in aborted[3][table]), "OLD_" + table + "_CHANGED")
        require(all(final[table] == aborted[3][table] for table in ("heads", "entries", "providers", "snapshots",
                                                                 "authorization", "owner_grants")),
                "OLD_STATE_CHANGED")
        require(len(self.calls) == 9 and sum(item["role"] == "ordinary" for item in self.calls) == 4
                and sum(item["role"] == "recovery" for item in self.calls) == 3
                and sum(item["role"] == "preparation" for item in self.calls) == 2
                and sum(item.get("direct_supervised") is True for item in self.calls) == 1, "EXACT_NINE_INVOCATIONS")
        for item in self.installed.values():
            require(pin(item["path"]) == item, "INSTALLED_SOURCE_CHANGED")
        require(pin(self.config) == self.config_pin, "CONFIG_CHANGED")
        save(self.driver / "sequence.json", {"calls": self.calls, "snapshots": self.snapshots,
            "bootstrap_context": c0, "snapshot": s0, "artifact": accepted[0]["artifact"],
            "normal_stages": actual_stages, "interrupted_stage": {"id": 1,
                "live_lean_commands_observed": 1, "completed_commands": None, "plan_command_bound": 5,
                "scope": "real observed running prefix; retained partial files are not reconstructed completion"},
            "hook": pin(self.driver / "hook/observation.json"),
            "aborted_admission_supply_sample": "may be lost with original event; actual product checks remain enabled",
            "source_authorship": "fixed noncomputable engineering fixture; not discovery or novelty",
            "outcome_audit": "PENDING; independently bind original lifecycle, native replay and all transitions"})
        return {"status": "PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT", "calls": 9, "installed_cli_calls": 8,
            "ordinary_calls": 4, "recovery_calls": 3, "ordinary_requests": 3, "owner_grants": 0,
            "native_stages": 3, "normal_pipeline_commands": 6, "aborted_live_lean_observations": 1,
            "aborted_completed_commands": None, "support_build_stages": 1,
            "support_compilations": 2, "charged_bytes": 408 * MIB}


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

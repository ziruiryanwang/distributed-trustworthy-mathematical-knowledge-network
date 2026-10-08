"""Fixed same-host original-byte replica custody and genuine Lean reuse.

Root-only execution after exact launch review. Historical files are inert input.
The static A mode has transport authority only; B and C use installed product CLIs.
"""
import argparse
from copy import deepcopy
import hashlib
import io
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
DATA = SOURCE.parent / "product-local/replica-native-02"
FLAGS = ["-B", "-E", "-s", "-S"]
MIB = 1048576
LIMITS = {"wall_seconds": 450, "cpu_seconds": 450, "memory_mib": 6144,
          "active_processes": 16, "stdout_bytes": 65536, "stderr_bytes": 65536, "event_bytes": 65536}
RETAINED = {"bytes": 1073741824, "files": 16384, "entries": 32768}
REQUEST = b'{"op":"test-replica-native"}\n'
SCOPE = "same-host replica custody and fresh native reuse; not independent hosts or useful growth"
SUCCESS = "PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT"
TABLES = {"meta": "id", "authorization": "id", "owner_grants": "sequence",
          "requests": "key", "records": "handle", "heads": "client", "providers": "provider",
          "snapshots": "handle", "entries": "provider,seq", "stages": "id"}
OLD_VIEW = SOURCE.parent / "product-local/peer-01/alpha/state/work/3daeca50176b8a36737de2b41180d13f0a2ab12a8339f57bd1aa988bbbf2acd2/peer-view"
HISTORICAL = [OLD_VIEW / "catalog.json", OLD_VIEW / "complete.json",
    OLD_VIEW / "bundles/32ac4a51e45013550f17b9bbe79fcd453e7f2a96ea50f7f652fb36a5910c1221.bundle",
    SOURCE / "qualification/peer-01-h01/author-source.lean",
    SOURCE / "qualification/peer-01-g02/OUTCOME.md", SOURCE / "qualification/peer-01-h01/OUTCOME.md"]
PORT_A, PORT_B = 42381, 42382
PUBLIC_LIMITS = {"wall_seconds": 450, "cpu_seconds": 450, "memory_mib": 6144,
    "active_processes": 8, "request_bytes": 131072, "stdout_bytes": MIB,
    "stderr_bytes": 65536, "event_bytes": 65536, "poll_seconds": 0.05, "settle_seconds": 15}
SERVICE_LIMITS = dict(PUBLIC_LIMITS, wall_seconds=150, cpu_seconds=120,
                      memory_mib=256, request_bytes=16384, stdout_bytes=65536)
PEER_OPS = {"peer_find", "peer_acquire", "expose", "replica_expose"}

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



def quiescent(receipt):
    return (receipt.get("direct_child_reaped") is True
        and receipt.get("final_active_zero") is True and receipt.get("job_closed") is True
        and not receipt.get("cleanup_errors") and receipt.get("final_job", {}).get("active_processes") == 0)


def data(snapshot, handle):
    rows = [row for row in snapshot["records"] if row["handle"] == handle]
    require(len(rows) == 1, "ONE_RECORD")
    value = strict(bytes.fromhex(rows[0]["raw"]["hex"]))
    require(value["kind"] == rows[0]["kind"] and value["client"] == rows[0]["client"], "RECORD_WRAPPER")
    return value["data"]


class Scenario:
    def __init__(self):
        self.install, self.driver = DATA / "install", DATA / "driver"
        self.calls, self.snapshots, self.jobs = [], [], []
        self.installed, self.events, self.states = {}, {}, {}
        self.started = time.monotonic()
        self.owner_lock = None

    def offset(self):
        return time.monotonic() - self.started

    def snapshot(self, node, name):
        require(self.owner_lock is not None and sqlite3.sqlite_version == "3.50.4", "SNAPSHOT_PROFILE")
        db_path = checked(node["state"] / "control.sqlite3")
        with self.owner_lock(node["state"], create=False):
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
        path = self.driver / "snapshots" / (node["name"] + "-" + name + ".json")
        save(path, value)
        self.snapshots.append({"node": node["name"], "name": name, "tables": pin(path), "pages": pages,
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

    def start(self, name, arguments, role, node=None):
        directory = self.driver / "calls" / name
        directory.mkdir(parents=True, exist_ok=False)
        command = [sys.executable, *FLAGS, *map(str, arguments)]
        save(directory / "command.json", {"argv": command, "cwd": str(self.install), "shell": False})
        record = {"name": name, "role": role, "node": node["name"] if node else None,
                  "started_offset": self.offset(), "command": pin(directory / "command.json")}
        self.calls.append(record)
        job = {"record": record, "directory": directory, "process": None, "closed": False}
        self.jobs.append(job)
        with (directory / "stdout.txt").open("xb") as out, (directory / "stderr.txt").open("xb") as err:
            job["process"] = subprocess.Popen(command, cwd=self.install, stdin=subprocess.DEVNULL,
                stdout=out, stderr=err, shell=False, close_fds=True, creationflags=subprocess.CREATE_NO_WINDOW)
        save(directory / "started.json", record)
        return job

    def finish(self, job):
        require(not job["closed"], "ONE_DIRECT_REAP")
        job["process"].wait()  # enclosing finite Job owns aggregate deadline/cleanup
        job["closed"] = True
        record, directory = job["record"], job["directory"]
        record.update(returncode=job["process"].returncode, direct_child_reaped=True,
                      finished_offset=self.offset(), stdout=pin(directory / "stdout.txt"),
                      stderr=pin(directory / "stderr.txt"))
        save(directory / "process.json", record)
        raw = read(directory / "stdout.txt", MIB)
        return raw, strict(raw)

    def cli(self, name, arguments):
        job = self.start(name, arguments, "preparation")
        raw, value = self.finish(job)
        require(job["record"]["returncode"] == 0, "PREPARATION_FAILED:" + name)
        if name == "build":
            # build.py deliberately redirects the stage status envelope here.
            # prepare() immediately binds that bounded record to the actual
            # authenticated support receipt before issuing any configure call.
            require(arguments[0] == self.install / "build.py", "BUILD_COMMAND_ROLE")
            strict(read(job["directory"] / "stderr.txt", 65536))
        else:
            require(read(job["directory"] / "stderr.txt", 65536) == b"", "PREPARATION_STDERR:" + name)
        return value

    def module_pins(self, node, service=False):
        names = (["service_worker.py", "inspect_context.py", "node.py", "storage.py", "capacity.py",
                  "domains.py", "run_stage.py", "supervise.py", "peer_wire.py", "peer_service.py", "peer_node.py"]
                 if service else ["node.py", "run_stage.py", "storage.py", "capacity.py", "checking.py",
                  "domains.py", "supervise.py", "peer_wire.py", "peer_service.py", "peer_node.py"])
        return [self.python_pin, node["config_pin"], *[self.installed["py/" + name] for name in names]]

    def binding(self, job, public, raw, module, config, state, pins, limits, worker_exit=0):
        """Retain observed costs/cleanup before checking the expected workload."""
        public = checked(public)
        receipt = strict(read(public / "supervisor.json", MIB))
        inner_raw = read(public / "stdout.txt", MIB)
        event = strict(read(public / "event.json", 65536))
        observation = {"receipt": pin(public / "supervisor.json"), "event": pin(public / "event.json"),
            "response": pin(public / "stdout.txt"), "actual_job_cpu_seconds": receipt.get("final_job", {}).get("cpu_seconds"),
            "cleanup": {key: receipt.get(key) for key in
                ("direct_child_reaped", "final_active_zero", "job_closed", "cleanup_errors")},
            "actual_work": {key: event.get(key) for key in
                ("checker_loaded", "stages_allocated", "native_stages", "checker_metrics")},
            "observed_offset": self.offset()}
        job["record"]["binding"] = observation
        save(job["directory"] / "binding.json", observation)
        expected_status = "TRANSPORT_COMPLETE" if worker_exit == 0 else "TRANSPORT_NONZERO_EXIT"
        require(quiescent(receipt) and receipt["status"] == expected_status
                and receipt["returncode"] == worker_exit and receipt["job_created_before_process"] is True
                and receipt["attach_resume_returned"] is True
                and not any(receipt.get(key) for key in
                    ("cleanup_errors", "output_record_error", "evidence_persistence_error", "failure"))
                and receipt["final_job"]["terminated_processes"] == 0, "PUBLIC_TREE_QUIESCENCE")
        require(receipt["pins"] == pins and receipt["limits"] == limits
                and receipt["sampled_peak_active_processes"] <= limits["active_processes"]
                and 0 <= receipt["final_job"]["cpu_seconds"] <= limits["cpu_seconds"]
                and 0 <= receipt["wall_seconds"] <= limits["wall_seconds"]
                and 0 <= receipt["final_job"]["peak_job_private_commit_bytes"] <= limits["memory_mib"] * MIB,
                "EXACT_PUBLIC_PROFILE")
        for expected in pins:
            require(pin(expected["path"]) == expected, "BOUND_SOURCE_CHANGED")
        require(set(receipt["files"]) == {"request.json", "command.json", "stdout.txt", "stderr.txt", "event.json"},
                "EXACT_PUBLIC_FILE_SET")
        for name, metadata in receipt["files"].items():
            actual = pin(public / name)
            require(metadata == {"present": True, "bytes": actual["bytes"], "sha256": actual["sha256"]},
                    "PUBLIC_FILE_BINDING")
        require(read(public / "request.json", 131072) == raw and receipt["request_sha256"] == sha(raw)
                and event["request_sha256"] == sha(raw) and event["response_sha256"] == sha(inner_raw)
                and read(public / "stderr.txt", 65536) == b"", "PUBLIC_IO_BINDING")
        require(strict(read(public / "command.json", 65536)) == {
            "argv": [sys.executable, *FLAGS, str(module), "--config", str(config), "--state", str(state),
                     "--request", str(public / "request.json"), "--event", str(public / "event.json")],
            "cwd": str(module.parent), "shell": False, "creationflags": 134217732,
            "environment_override": {"PYTHONDONTWRITEBYTECODE": "1"}}, "PUBLIC_COMMAND_BINDING")
        return inner_raw, strict(inner_raw), event

    def request(self, node, name, op=None, arguments=None, *, owner=False, replay=None, native=0, children=0):
        raw = read(self.driver / "requests" / (replay + ".json"), 131072) if replay else encode({
            "client": "owner" if owner else "local", "request_id": name, "op": op, "args": arguments})
        path = self.driver / "requests" / (name + ".json")
        save_raw(path, raw)
        before = self.snapshot(node, name + "-before") if (node["state"] / "control.sqlite3").exists() else None
        root = node["scratch"] / "calls"
        previous = set(root.iterdir()) if root.exists() else set()
        require(len(previous) <= 14, "CALL_COUNT_BOUND")
        job = self.start(name, [self.install / "manage.py", "request", "--config", node["config"],
                               "--request", path], "request", node)
        wrapper_raw, value = self.finish(job)
        current = set(root.iterdir())
        require(previous <= current and len(current - previous) == 1, "ONE_NEW_CALL_DIRECTORY")
        public = (current - previous).pop()
        limits = dict(PUBLIC_LIMITS)
        if strict(raw)["op"] in PEER_OPS:
            limits.update(wall_seconds=120, cpu_seconds=120, memory_mib=1024)
        inner, value, event = self.binding(job, public, raw, self.install / "py/node.py",
            node["config"], node["state"], self.module_pins(node), limits)
        require(inner == wrapper_raw and job["record"]["returncode"] == 0
                and read(job["directory"] / "stderr.txt", 65536) == b""
                and event["origin_directory"] == str(public), "ORDINARY_PUBLIC_FORWARDING")
        after = self.snapshot(node, name + "-after")
        self.events[name], self.states[node["name"]] = event, after
        require(event["stages_allocated"] == native, "ACTUAL_STAGE_COUNT")
        metrics = event.get("checker_metrics")
        if event["checker_loaded"] is True:
            require(metrics["stage_allocations"] == native and metrics["pipeline_children"] == children,
                    "ACTUAL_PIPELINE_CHILD_COUNT")
        else:
            require(native == children == 0 and metrics == {}, "MISSING_NATIVE_METRICS")
        if replay:
            require(inner == read(self.driver / "calls" / replay / "stdout.txt", MIB)
                    and after == before and event["historical"] is True and event["checker_loaded"] is False
                    and "admission_physical_supply" not in event, "EXACT_REPLAY_NO_NEW_RESERVATION")
        else:
            prior = before["meta"][0] if before else {"requests": 0, "stages": 0, "charged": 0}
            charge = (64 if op == "peer_acquire" else 80 if op in {"expose", "replica_expose"} else 8) * MIB
            meta = after["meta"][0]
            require(meta["requests"] == prior["requests"] + 1 and meta["stages"] == prior["stages"] + native
                    and meta["charged"] == prior["charged"] + charge + native * 128 * MIB
                    and meta["active"] is None, "EXACT_REQUEST_RESERVATION")
            remaining = node["reserved"] - prior["charged"]
            supply(event["admission_physical_supply"], remaining, enforced=True)
        return {"reply": value, "raw": inner, "before": before, "after": after,
                "event": event, "job": job, "public": public}

    def ready(self, service):
        deadline = time.monotonic() + 30
        path = service["ready"]
        while not path.exists():
            require(service["job"]["process"].poll() is None, "SERVICE_EXITED_BEFORE_READY")
            require(time.monotonic() < deadline, "SERVICE_READINESS_TIMEOUT")
            time.sleep(0.05)
        require(time.monotonic() <= deadline, "SERVICE_READINESS_TIMEOUT")
        require(strict(read(path, 4096)) == {"host": "127.0.0.1", "port": service["port"],
                "catalog_sha256": service["catalog"]}, "EXACT_SERVICE_READINESS")
        service["readiness"] = pin(path)
        save(service["job"]["directory"] / "readiness.json", {"pin": service["readiness"], "offset": self.offset()})

    def start_b(self, node, view, catalog, session, *, positive):
        raw = encode({"op": "serve", "session": session, "client": "local", "view": view,
            "port": PORT_B, "seconds": 120, "max_requests": 2, "max_bytes": 64 * MIB})
        root = node["scratch"] / "services" / session
        require(not root.exists(), "FRESH_SERVICE_SESSION")
        job = self.start(session, [self.install / "manage.py", "serve", "--config", node["config"],
            "--client", "local", "--view", view, "--session", session, "--port", PORT_B,
            "--seconds", 120, "--max-requests", 2, "--max-bytes", 64 * MIB], "service", node)
        service = {"job": job, "raw": raw, "root": root, "ready": root / "ready.json",
                   "catalog": catalog, "port": PORT_B, "view": view, "session": session, "node": node}
        if positive:
            self.ready(service)
        return service

    def finish_service(self, service, *, refused=False, fixture=False):
        wrapper_raw, wrapper = self.finish(service["job"])
        require(read(service["job"]["directory"] / "stderr.txt", 65536) == b"", "SERVICE_WRAPPER_STDERR")
        node = service.get("node")
        if fixture:
            config, state, module, pins = (service["grant"], DATA / "a", Path(__file__).resolve(), service["pins"])
            public = service["root"] / "cases/serve"
        else:
            config, state, module, pins = (node["config"], node["state"], self.install / "py/service_worker.py",
                                          self.module_pins(node, service=True))
            public = service["root"] / "cases/serve"
            grant = strict(read(service["root"] / "grant.json", 65536))
            require(grant == {"schema": 1, "request": strict(service["raw"]),
                "limits": {key: value for key, value in dict(SERVICE_LIMITS, pins=pins).items()
                           if key not in {"poll_seconds", "settle_seconds"}},
                "policy": "one explicitly issued local session; no automatic retries or counter reset"}, "EXACT_SERVICE_GRANT")
        inner, reply, event = self.binding(service["job"], public, service["raw"], module, config, state,
                                         pins, SERVICE_LIMITS, worker_exit=1 if refused else 0)
        require(event["checker_loaded"] is False and event["native_stages"] == 0, "CHECKER_FREE_SERVICE")
        if refused:
            require(service["job"]["record"]["returncode"] == 1
                and wrapper == {"status": "SERVICE_REFUSED", "worker": reply,
                    "evidence": str(service["root"]), "mathematicalAcceptance": False}
                and reply["status"] == "SERVICE_REFUSED" and reply["code"] == "BUNDLE_DIGEST_MISMATCH"
                and reply["mathematicalAcceptance"] is False and reply["native_stages"] == 0
                and not service["ready"].exists(), "TAMPERED_SERVICE_REFUSED_BEFORE_READINESS")
        else:
            require(service["job"]["record"]["returncode"] == 0 and wrapper_raw == inner
                    and reply["status"] == "SERVICE_STOPPED" and reply["catalog_sha256"] == service["catalog"]
                    and reply["mathematicalAcceptance"] is False and reply["native_stages"] == 0,
                    "SUCCESSFUL_SERVICE_FORWARDING")
            if not fixture:
                require(reply["session"] == service["session"] and reply["view"] == service["view"], "SERVICE_SELECTION")
            observed = reply["observations"]
            require(observed["connections"] == 2 and observed["responses"] == 2 and "last_error" not in observed
                    and observed["bind_host"] == "127.0.0.1" and observed["port"] == service["port"]
                    and observed["checker_loaded"] is False and observed["native_stages"] == 0
                    and observed["mathematicalAcceptance"] is False
                    and 0 < observed["completed_send_bytes"] <= observed["charged_send_bytes"] <= 64 * MIB,
                    "TWO_BOUNDED_SUCCESSFUL_TRANSFERS")
        service["stop_offset"] = self.offset()
        save(service["job"]["directory"] / "service-stop.json", {
            "offset": service["stop_offset"], "reply": reply,
            "readiness": service.get("readiness"), "receipt": pin(public / "supervisor.json")})
        return reply

    def prepare(self, launch):
        require(type(launch) is dict and set(launch) == {"schema", "pins", "product", "limits", "retained"}
                and type(launch["schema"]) is int and launch["schema"] == 1
                and encode(launch["limits"]) == encode(LIMITS)
                and encode(launch["retained"]) == encode(RETAINED), "EXACT_LAUNCH_FIELDS")
        self.runtime = SOURCE / "runtime/lean-4.34.0-windows"
        paths = [Path(sys.executable), SOURCE / "tests/run_replica_native_v2.py", Path(__file__).resolve(),
            SOURCE / "tests/scenario_profile.py", PRODUCT / "py/run_stage.py", PRODUCT / "py/supervise.py",
            PRODUCT / "py/domains.py", self.runtime / "bin/lean.exe", *HISTORICAL]
        require(encode(launch["pins"]) == encode([pin(path) for path in paths]), "EXACT_ORDERED_SOURCE_PINS")
        products = [dict(relative=path.relative_to(PRODUCT).as_posix(), **pin(path)) for path in product_paths()]
        require(encode(launch["product"]) == encode(products), "EXACT_PRODUCT_PINS")
        self.python_pin = pin(sys.executable)
        self.install.mkdir()
        for expected in products:
            relative = PurePosixPath(expected["relative"])
            require(not relative.is_absolute() and ".." not in relative.parts and ":" not in str(relative)
                    and "\\" not in str(relative), "PRODUCT_RELATIVE")
            raw = read(PRODUCT / str(relative))
            require(len(raw) == expected["bytes"] and sha(raw) == expected["sha256"], "PRODUCT_CHANGED")
            save_raw(self.install / str(relative), raw)
            copied = pin(self.install / str(relative))
            require(copied["bytes"] == expected["bytes"] and copied["sha256"] == expected["sha256"], "PRODUCT_COPY")
            self.installed[str(relative)] = copied
        save(self.driver / "installed-source-pins.json", list(self.installed.values()))
        require(not any(name in sys.modules for name in ("storage", "capacity", "peer_wire", "checking")),
                "PRODUCT_MODULE_ALREADY_IMPORTED")
        sys.path.insert(0, str(self.install / "py"))
        import storage
        import peer_wire
        for module, name in ((storage, "storage.py"), (peer_wire, "peer_wire.py")):
            require(pin(module.__file__) == self.installed["py/" + name], "INERT_MODULE_ORIGIN")
        self.owner_lock, self.wire = storage.owner_lock, peer_wire
        build_reply = self.cli("build", [self.install / "build.py", "--lean-runtime", self.runtime, "--work", DATA / "build-work"])
        build = strict(read(self.install / "build/build-receipt.json"))
        support = strict(read(build["stage_receipt"]["path"]))
        self.support = {"build": pin(self.install / "build/build-receipt.json"), "stage": build["stage_receipt"]}
        save(self.driver / "support-observation.json", {"pins": self.support, "receipt": support})
        require(build["status"] == "LOCAL_SUPPORT_BUILD_COMPLETED_NOT_MATH_ACCEPTANCE"
                and build["mathematicalAcceptance"] is False and pin(build["stage_receipt"]["path"]) == build["stage_receipt"]
                and support["status"] == "STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE"
                and len(support["steps"]) == 2 and all(step["exit_code"] == 0 for step in support["steps"])
                and support["execution_endpoint"]["children_quiescent"] is True
                and support["final_job"]["active_processes"] == 0
                and support["final_job"]["terminated_processes"] == 0, "GENUINE_NEW_SUPPORT_BUILD")
        require(build_reply == {"status": build["status"], "receipt": self.support["build"]}
                and strict(read(self.driver / "calls/build/stderr.txt", 65536))
                    == {"record": build["stage_receipt"]["path"], "status": support["status"]},
                "BUILD_STDOUT_STDERR_RECEIPT_BINDING")
        self.b = self.configure("b", "a", PORT_A, 6, 1, 448)
        self.c = self.configure("c", "b", PORT_B, 7, 3, 568)
        self.fixture(launch["pins"][8:])

    def configure(self, name, peer, port, requests, stages, reserved):
        node = {"name": name, "state": DATA / name / "state", "scratch": DATA / name / "scratch",
                "requests": requests, "stages": stages, "reserved": reserved * MIB}
        node["config"] = node["state"] / "config.json"
        configured = self.cli("configure-" + name, [self.install / "manage.py", "configure",
            "--state", node["state"], "--scratch", node["scratch"], "--lean-runtime", self.runtime,
            "--client", "local", "--peer", peer + "=" + str(port), "--initial-requests", requests,
            "--initial-stages", stages, "--initial-reserved-mib", reserved, "--initial-metadata-mib", 32])
        config = strict(read(node["config"]))
        node["config_pin"], node["value"] = pin(node["config"]), config
        require(config["schema"] == 3 and config["clients"] == ["local"]
                and config["peers"] == {peer: {"host": "127.0.0.1", "port": port}}
                and config["domains"] == {"install": str(self.install), "state": str(node["state"]),
                    "scratch": str(node["scratch"]), "lean_runtime": str(self.runtime)}
                and config["offers"] == [] and len(config["common"]["packages"]) == 5
                and config["limits"]["requests"] == requests and config["limits"]["stages"] == stages
                and config["limits"]["staging_bytes"] == reserved * MIB
                and config["limits"]["metadata_pages"] == 8192
                and config["limits"]["request_bytes"] == 8 * MIB and config["limits"]["stage_bytes"] == 128 * MIB
                and not (node["state"] / "control.sqlite3").exists()
                and configured["status"] == "CONFIGURED_NOT_INITIALIZED"
                and configured["config"] == node["config_pin"], "NEW_DISJOINT_NODE_CONFIGURATION")
        supply(configured["initial_physical_supply"], reserved * MIB, enforced=True)
        return node

    def fixture(self, pins):
        require(len(pins) == 6, "EXACT_HISTORICAL_INPUTS")
        selected = []
        destinations = [DATA / "a/original-view/catalog.json", DATA / "a/original-view/complete.json",
            DATA / "a/original-view/bundles/32ac4a51e45013550f17b9bbe79fcd453e7f2a96ea50f7f652fb36a5910c1221.bundle",
            self.driver / "historical/author-source.lean", self.driver / "historical/g-outcome.md",
            self.driver / "historical/h-outcome.md"]
        for original, expected, destination in zip(HISTORICAL, pins, destinations):
            raw = read(original)
            require(pin(original) == expected and sha(raw) == expected["sha256"], "HISTORICAL_INPUT_CHANGED")
            save_raw(destination, raw)
            selected.append({"original": expected, "copy": pin(destination)})
        for index, size, digest in (
            (0, 3680, "ab5f311da32b03f03e892069de93c81fee98b020429130ff2359d1c4bb57b55a"),
            (1, 245, "b497b792e08d56eaf69d0c209aab2a4e8b30d6780559edc2355eec254b74f456"),
            (2, 298037, "32ac4a51e45013550f17b9bbe79fcd453e7f2a96ea50f7f652fb36a5910c1221"),
            (3, 1465, "95d1ffdfff0c93a6dfaa2381c64daf940792b770a292002097960a26e54bebeb")):
            require(selected[index]["copy"]["bytes"] == size and selected[index]["copy"]["sha256"] == digest,
                    "EXACT_SELECTED_HISTORICAL_FIXTURE")
        original = self.wire.load_view(DATA / "a/original-view")
        require(len(original["catalog"]["entries"]) == 1, "ONE_HISTORICAL_G")
        self.foundation = original["catalog"]["foundation"]
        entry = original["catalog"]["entries"][0]
        bundle = read(destinations[2], MIB)
        width = len(self.wire.MAGIC)
        require(bundle[:width] == self.wire.MAGIC, "FIXTURE_FRAMING")
        length = int.from_bytes(bundle[width:width + 4], "big")
        manifest = bundle[width + 4:width + 4 + length]
        require(sha(manifest) == entry["manifest_sha256"], "ORIGINAL_MANIFEST_BINDING")
        changed_manifest = b" " + manifest
        changed = bundle[:width] + (length + 1).to_bytes(4, "big") + changed_manifest + bundle[width + 4 + length:]
        require(len(changed) == 298038 and self.wire.parse_manifest(changed_manifest, self.foundation)
                == self.wire.parse_manifest(manifest, self.foundation), "PRESENTATION_ONLY_DERIVATIVE")
        self.entry = dict(entry, manifest_sha256=sha(changed_manifest), bundle_sha256=sha(changed), bundle_bytes=len(changed))
        self.a_view = DATA / "a/derivative-view"
        catalog_raw = self.wire.encoded({"schema": 1, "foundation": self.foundation, "entries": [self.entry]})
        save_raw(self.a_view / "bundles" / (sha(changed) + ".bundle"), changed)
        save_raw(self.a_view / "catalog.json", catalog_raw)
        save_raw(self.a_view / "complete.json", self.wire.encoded({"schema": 1,
            "foundation": self.foundation, "catalog_sha256": sha(catalog_raw)}))
        loaded = self.wire.load_view(self.a_view)
        structural = self.wire.receive_bundle(io.BytesIO(changed), self.entry, self.foundation, DATA / "a/structural-package")
        require(loaded["catalog"]["entries"] == [self.entry] and structural["mathematicalAcceptance"] is False
                and structural["native_stages"] == 0
                and self.wire.make_bundle(structural["package"]["path"]) == changed, "INERT_DERIVATIVE_VALIDATION")
        self.bundle, self.a_catalog = changed, sha(catalog_raw)
        self.h_source = read(destinations[3], 65536)
        self.h_text = self.h_source.decode("utf-8")
        require(self.h_text.encode("utf-8") == self.h_source, "EXACT_H_UTF8")
        save(self.driver / "fixture-freeze.json", {"historical_inputs": selected,
            "original_view": self.file_map(DATA / "a/original-view"), "derivative_view": self.file_map(self.a_view),
            "structural_package": self.file_map(DATA / "a/structural-package"), "entry": self.entry,
            "transformation": "prefix manifest with one ASCII space; preserve object bytes/order and mathematical metadata",
            "mathematical_acceptance": False, "historical_acceptance_reused": False})

    def start_a(self):
        root = DATA / "a/service"
        root.mkdir()
        (root / "cases").mkdir()
        grant = root / "grant.json"
        pins = [self.python_pin, pin(Path(__file__).resolve()),
                *[self.installed["py/" + name] for name in
                  ("peer_wire.py", "peer_service.py", "run_stage.py", "supervise.py", "domains.py")]]
        raw = encode({"op": "serve-static-fixture", "port": PORT_A, "seconds": 120,
                      "max_requests": 2, "max_bytes": 64 * MIB})
        grant_value = {"schema": 1, "mode": "inert-static-fixture", "install": str(self.install),
            "state": str(DATA / "a"), "root": str(root), "view": str(self.a_view), "request": strict(raw),
            "view_files": self.file_map(self.a_view), "inputs": pins, "limits": SERVICE_LIMITS,
            "authority": "test-only supplier of canonical mathematical bytes; no product view or accepting receipt"}
        save(grant, grant_value)
        job = self.start("a-service", [Path(__file__).resolve(), "--fixture-owner", "--config", grant], "fixture-service")
        service = {"job": job, "grant": grant, "root": root, "raw": raw, "ready": root / "ready.json",
                   "port": PORT_A, "catalog": self.a_catalog, "pins": [*pins, pin(grant)]}
        self.ready(service)
        return service

    def mutation_file(self, name, target, original, replacement, allowed):
        """Only two prospectively selected new-copy files may be overwritten."""
        target = checked(target)
        require(target == allowed and target.is_relative_to(checked(self.b["state"] / "work"))
                and target.is_file() and read(target) == original, "EXACT_OWNED_FAULT_TARGET")
        parent_before = self.file_map(target.parent)
        saved = self.driver / "faults" / (name + "-original.bin")
        save_raw(saved, original)
        require(read(saved) == original, "FAULT_ORIGINAL_DURABLY_PRESERVED")
        save(self.driver / "faults" / (name + "-intent.json"), {"target": pin(target), "saved": pin(saved),
             "replacement_bytes": len(replacement), "replacement_sha256": sha(replacement), "parent_before": parent_before})
        # No delete, rollback or repair. The exact new-owned file remains damaged.
        with target.open("r+b") as stream:
            require(stream.read() == original, "FAULT_TARGET_CHANGED")
            stream.seek(0)
            stream.write(replacement)
            stream.truncate()
            stream.flush()
            os.fsync(stream.fileno())
        after = self.file_map(target.parent)
        expected = dict(parent_before)
        expected[target.name] = {"bytes": len(replacement), "sha256": sha(replacement)}
        require(after == expected and read(target) == replacement, "FAULT_EXACT_FILE_DELTA")
        save(self.driver / "faults" / (name + "-outcome.json"), {"target": pin(target), "parent_after": after})

    def quarantine(self, acquisition, view):
        work = checked(self.b["state"] / "work")
        request_root = checked(work / acquisition["request"])
        incoming, normalized = (checked(acquisition[field]["path"]) for field in ("received_package", "package"))
        targets = [(incoming, request_root / "quarantine-incoming"), (normalized, request_root / "quarantine-normalized")]
        require(incoming == request_root / "incoming" and normalized != incoming
                and not incoming.is_relative_to(normalized) and not normalized.is_relative_to(incoming), "DISJOINT_CUSTODY_COPIES")
        for path, destination in targets:
            require(path.is_dir() and path != work and path.is_relative_to(request_root) and request_root != work
                    and path != request_root and not path.is_relative_to(view) and not view.is_relative_to(path)
                    and not os.path.lexists(destination) and checked(destination.parent) == request_root,
                    "SAFE_EXACT_QUARANTINE_TARGET")
        before = self.file_map(request_root)
        intent = [{"from": str(path), "to": str(destination), "files": self.file_map(path)} for path, destination in targets]
        save(self.driver / "faults/quarantine-intent.json", {"targets": intent, "request_root_before": before})
        for (path, destination), row in zip(targets, intent):
            require(checked(path) == path and not os.path.lexists(destination), "QUARANTINE_TARGET_CHANGED")
            path.rename(destination)
            require(not path.exists() and self.file_map(destination) == row["files"], "QUARANTINE_PRESERVED_BYTES")
        after = self.file_map(request_root)
        expected = {}
        for relative, metadata in before.items():
            source = request_root / relative
            replacements = [destination / source.relative_to(path) for path, destination in targets if source.is_relative_to(path)]
            require(len(replacements) <= 1, "QUARANTINE_OVERLAP")
            expected[(replacements[0] if replacements else source).relative_to(request_root).as_posix()] = metadata
        require(after == expected, "QUARANTINE_EXACT_CENSUS_DELTA")
        save(self.driver / "faults/quarantine-outcome.json", {"targets": intent, "request_root_after": after})

    def native_evidence(self, node, snapshot, expected):
        observed = []
        require(len(snapshot["stages"]) == len(expected), "EXACT_NATIVE_STAGE_LEDGER")
        for row, (identity, client, purpose, children) in zip(snapshot["stages"], expected):
            directory = checked(row["directory"])
            require(directory.is_relative_to(node["state"] / "work"), "NATIVE_STAGE_DOMAIN")
            receipt, plan = strict(read(directory / "stage.json", MIB)), strict(read(directory / "plan.json", MIB))
            observation = {"node": node["name"], "request": identity, "row": row,
                "receipt": pin(directory / "stage.json"), "plan": pin(directory / "plan.json"),
                "completed_commands": len(receipt.get("steps", [])), "actual_final_job": receipt.get("final_job"),
                "actual_execution_endpoint": receipt.get("execution_endpoint")}
            observed.append(observation)
            save(self.driver / "stages" / (node["name"] + "-" + identity + ".json"), observation)
            require(row == {"id": row["id"], "request": sha(encode([client, identity])), "purpose": purpose,
                    "directory": str(node["state"] / "work" / sha(encode([client, identity])) / ("stage-%04d" % row["id"])),
                    "grant_bytes": 128 * MIB}, "EXACT_STAGE_ASSIGNMENT")
            require(receipt["status"] == "STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE"
                    and receipt["final_job"]["active_processes"] == 0
                    and receipt["final_job"]["terminated_processes"] == 0
                    and receipt["execution_endpoint"]["children_quiescent"] is True
                    and len(receipt["steps"]) == children and all(step["exit_code"] == 0 for step in receipt["steps"])
                    and receipt["plan"] == pin(directory / "plan.json")
                    and receipt["expected_plan_sha256"] == sha(read(directory / "plan.json", MIB))
                    and plan["schema"] == 2 and len(plan["steps"]) == children
                    and receipt["stage"] == plan["stage"] == str(row["id"])
                    and receipt["accounting_root"] == plan["stage_directory"] == str(directory)
                    and receipt["request_directory"] == plan["request_directory"] == str(directory.parent)
                    and receipt["domains"] == plan["domains"] == node["value"]["domains"], "NATIVE_STAGE_BINDING")
        return observed

    def run(self, launch):
        self.prepare(launch)
        initialized = {}
        for node in (self.b, self.c):
            name = node["name"] + "-init"
            result = self.request(node, name, "init", {}, owner=True, native=1, children=1)
            reply, state = result["reply"], result["after"]
            require(reply.get("accepted") is True and reply["status"] == "OK"
                    and reply["description"]["foundation"] == self.foundation and not state["entries"]
                    and state["providers"] == [{"provider": "P1", "cut": 0, "snapshot": reply["snapshots"]["P1"]}],
                    "FRESH_COMPATIBLE_EMPTY_NODE")
            node["initial_context"], node["initial_snapshot"] = reply["contexts"]["local"], reply["snapshots"]["P1"]
            require(len(data(state, node["initial_context"])["packages"]) == 5, "FIVE_FRESH_BOOTSTRAP_PACKAGES")
            initialized[node["name"]] = state
        a_service = self.start_a()
        found = self.request(self.b, "b-find", "peer_find", {"peer": "a"})
        require(found["reply"]["status"] == "OK" and len(found["reply"]["rows"]) == 1
                and found["reply"]["catalog_sha256"] == self.a_catalog
                and {key: found["reply"]["rows"][0][key] for key in self.entry} == self.entry,
                "B_DISCOVERED_EXACT_DERIVATIVE")
        acquired = self.request(self.b, "b-acquire", "peer_acquire", {"remote": found["reply"]["rows"][0]["remote"]})
        require(acquired["reply"]["status"] == "OK" and acquired["reply"]["candidate_only"] is True
                and acquired["reply"]["mathematicalAcceptance"] is False
                and acquired["reply"]["descriptor_id"] == self.entry["descriptor_id"], "B_CUSTODY_NOT_ACCEPTANCE")
        b_acq = data(acquired["after"], acquired["reply"]["acquisition"])
        require(b_acq["request"] == sha(encode(["local", "b-acquire"]))
                and acquired["after"]["heads"] == initialized["b"]["heads"]
                and acquired["after"]["stages"] == initialized["b"]["stages"]
                and not any(row["kind"] in {"publication", "view", "artifact"} for row in acquired["after"]["records"]),
                "B_UNADMITTED_CUSTODY_ONLY")
        incoming, normalized = Path(b_acq["received_package"]["path"]), Path(b_acq["package"]["path"])
        incoming_raw, normalized_raw = read(incoming / "manifest.json"), read(normalized / "manifest.json")
        require(incoming_raw != normalized_raw and sha(incoming_raw) != sha(normalized_raw)
                and sha(incoming_raw) == self.entry["manifest_sha256"]
                and sha(normalized_raw) == b_acq["package"]["manifest_sha256"]
                and self.wire.make_bundle(incoming) == self.bundle, "REPRESENTATION_DISCRIMINATOR")
        original_manifest, local_manifest = strict(incoming_raw), strict(normalized_raw)
        require(all(original_manifest[field] == local_manifest[field] for field in ("foundation", "root", "inventories"))
                and {self.wire.object_name(item) for item in original_manifest["objects"]}
                    == {self.wire.object_name(item) for item in local_manifest["objects"]}
                and self.file_map(incoming / "objects") == self.file_map(normalized / "objects"), "SAME_CANONICAL_OBJECT_BYTES")
        save(self.driver / "representation-discriminator.json", {"incoming": pin(incoming / "manifest.json"),
            "normalized": pin(normalized / "manifest.json"), "bundle_sha256": sha(self.bundle),
            "acquisition": acquired["reply"]["acquisition"], "canonical_objects": self.file_map(incoming / "objects")})
        self.finish_service(a_service, fixture=True)
        ordinary_expose = self.request(self.b, "b-unpublished-expose", "expose", {"selected": [acquired["reply"]["candidate"]]})
        require(ordinary_expose["reply"] == {"status": "REFUSED", "code": "NOT_LOCALLY_PUBLISHED", "detail": ""},
                "UNPUBLISHED_CUSTODY_NOT_PUBLICATION")
        replica = self.request(self.b, "b-replica", "replica_expose", {"acquisition": acquired["reply"]["acquisition"]})
        require(replica["job"]["record"]["started_offset"] > a_service["stop_offset"]
                and replica["reply"]["status"] == "OK" and replica["reply"]["basis"] == "replica-custody"
                and replica["reply"]["entries"] == 1 and replica["reply"]["mathematicalAcceptance"] is False,
                "ACTUAL_POST_PRODUCER_REPLICA")
        view = data(replica["after"], replica["reply"]["view"])
        view_path = checked(view["directory"])
        require(self.wire.load_view(view_path)["catalog"]["entries"] == [self.entry]
                and read(view_path / "bundles" / (self.entry["bundle_sha256"] + ".bundle"), MIB) == self.bundle,
                "REPLICA_EXACT_ORIGINAL_REPRESENTATION")
        expected_ledger = deepcopy(replica["before"])
        require(replica["after"]["heads"] == expected_ledger["heads"]
                and all(replica["after"][table] == expected_ledger[table] for table in
                    ("stages", "entries", "providers", "snapshots", "authorization", "owner_grants"))
                and len([row for row in replica["after"]["records"] if row["kind"] == "view"]) == 1,
                "VIEW_NOT_MATHEMATICAL_ADMISSION_OR_PUBLICATION")
        self.mutation_file("received-manifest", incoming / "manifest.json", incoming_raw, normalized_raw,
                           self.b["state"] / "work" / b_acq["request"] / "incoming/manifest.json")
        refused_replica = self.request(self.b, "b-replica-changed", "replica_expose", {"acquisition": acquired["reply"]["acquisition"]})
        require(refused_replica["reply"] == {"status": "REFUSED", "code": "REPLICA_RECEIVED_CHANGED", "detail": ""}
                and len([row for row in refused_replica["after"]["records"] if row["kind"] == "view"]) == 1,
                "CHANGED_RECEIVED_BYTES_REFUSE_NEW_VIEW")
        self.quarantine(b_acq, view_path)
        before_replay = self.file_map(self.b["state"] / "work")
        self.request(self.b, "b-replica-replay", replay="b-replica")
        require(self.file_map(self.b["state"] / "work") == before_replay, "REPLAY_NO_PREPARATION")
        b_service = self.start_b(self.b, replica["reply"]["view"], replica["reply"]["catalog_sha256"], "b-positive", positive=True)
        c_found = self.request(self.c, "c-find", "peer_find", {"peer": "b"})
        require(c_found["reply"]["status"] == "OK" and len(c_found["reply"]["rows"]) == 1
                and c_found["reply"]["catalog_sha256"] == self.a_catalog
                and {key: c_found["reply"]["rows"][0][key] for key in self.entry} == self.entry, "C_FOUND_B_EXACT_REPLICA")
        c_acquired = self.request(self.c, "c-acquire", "peer_acquire", {"remote": c_found["reply"]["rows"][0]["remote"]})
        require(c_acquired["reply"]["status"] == "OK" and c_acquired["reply"]["candidate_only"] is True
                and c_acquired["reply"]["mathematicalAcceptance"] is False
                and c_acquired["reply"]["descriptor_id"] == self.entry["descriptor_id"]
                and c_acquired["after"]["heads"] == initialized["c"]["heads"]
                and c_acquired["after"]["stages"] == initialized["c"]["stages"], "C_NOT_ADMITTED_BY_TRANSFER")
        c_acq = data(c_acquired["after"], c_acquired["reply"]["acquisition"])
        require(c_acq["peer"] == "b" and self.wire.make_bundle(c_acq["received_package"]["path"]) == self.bundle,
                "C_RECONSTRUCTS_EXACT_A_DERIVATIVE_FROM_B")
        save(self.driver / "transfer-correspondence.json", {"a_derivative": pin(self.a_view / "bundles" / (sha(self.bundle) + ".bundle")),
            "b_view": pin(view_path / "bundles" / (sha(self.bundle) + ".bundle")), "c_acquisition": c_acq,
            "c_received_package": self.file_map(Path(c_acq["received_package"]["path"])),
            "reconstructed_bytes": len(self.bundle), "reconstructed_sha256": sha(self.bundle)})
        self.finish_service(b_service)
        bundle_path = checked(view_path / "bundles" / (self.entry["bundle_sha256"] + ".bundle"))
        damaged = self.bundle[:-1] + bytes([self.bundle[-1] ^ 1])
        self.mutation_file("replica-bundle", bundle_path, self.bundle, damaged,
                           self.b["state"] / "work" / sha(encode(["local", "b-replica"])) / "peer-view/bundles" / bundle_path.name)
        negative_service = self.start_b(self.b, replica["reply"]["view"], replica["reply"]["catalog_sha256"], "b-tampered", positive=False)
        self.finish_service(negative_service, refused=True)
        admitted = self.request(self.c, "c-admit", "admit", {"context": self.c["initial_context"],
            "selected": [c_acquired["reply"]["candidate"]]}, native=1, children=1)
        require(admitted["job"]["record"]["started_offset"] > max(a_service["stop_offset"], b_service["stop_offset"], negative_service["stop_offset"])
                and admitted["reply"].get("accepted") is True and admitted["reply"]["context"] != self.c["initial_context"],
                "FRESH_OFFLINE_C_ACCEPTANCE")
        submitted = self.request(self.c, "c-submit", "submit", {"context": admitted["reply"]["context"],
            "source": self.h_text, "root": "PeerBetaStableLiftFixed"}, native=1, children=5)
        require(submitted["reply"].get("accepted") is True
                and submitted["reply"]["context"] == admitted["reply"]["context"]
                and submitted["reply"]["source_sha256"] == sha(self.h_source)
                and submitted["reply"]["source_root"] == "PeerBetaStableLiftFixed", "EXACT_FIXED_H_SOURCE_ACCEPTANCE")
        artifact = data(submitted["after"], submitted["reply"]["artifact"])
        require(read(artifact["source"]["path"], 65536) == self.h_source
                and pin(artifact["source"]["path"]) == artifact["source"]
                and artifact["context"] == admitted["reply"]["context"]
                and artifact["source_sha256"] == sha(self.h_source), "CHECKED_ARTIFACT_SOURCE_BINDING")
        published = self.request(self.c, "c-publish", "publish", {"artifact": submitted["reply"]["artifact"],
            "snapshot": c_acquired["reply"]["snapshot"]})
        require(published["reply"]["status"] == "OK" and published["reply"]["existing"] is False
                and published["reply"]["descriptor_id"] != self.entry["descriptor_id"]
                and data(published["after"], published["reply"]["publication"]), "DISTINCT_H_PUBLICATION")
        exposed = self.request(self.c, "c-expose", "expose", {"selected": [published["reply"]["candidate"]]})
        h_view = data(exposed["after"], exposed["reply"]["view"])
        loaded_h = self.wire.load_view(h_view["directory"])
        require(exposed["reply"]["status"] == "OK" and exposed["reply"]["entries"] == 1
                and exposed["reply"]["mathematicalAcceptance"] is False
                and loaded_h["catalog"]["entries"][0]["descriptor_id"] == published["reply"]["descriptor_id"]
                and loaded_h["catalog"]["entries"][0]["root"] == artifact["root"]
                and h_view["selected"][0]["publication"] == published["reply"]["publication"], "CHECKED_PORTABLE_H_VIEW")
        final_b = self.snapshot(self.b, "final")
        final_c = self.snapshot(self.c, "final")
        for node, state, count, stages, charged in ((self.b, final_b, 6, 1, 448), (self.c, final_c, 7, 3, 568)):
            require((state["meta"][0]["requests"], state["meta"][0]["stages"], state["meta"][0]["charged"])
                    == (count, stages, charged * MIB) and state["meta"][0]["active"] is None
                    and not state["owner_grants"] and state["authorization"] == initialized[node["name"]]["authorization"],
                    "EXACT_EXHAUSTED_UNRENEWED_AUTHORIZATION")
        require(final_b == refused_replica["after"] and final_b["heads"] == initialized["b"]["heads"]
                and len(final_b["entries"]) == 1 and len(final_c["entries"]) == 2
                and final_c["heads"] == [{"client": "local", "context": admitted["reply"]["context"]}], "FINAL_RECIPROCAL_STATE")
        stages = self.native_evidence(self.b, final_b, [("b-init", "owner", "bootstrap", 1)])
        stages += self.native_evidence(self.c, final_c, [("c-init", "owner", "bootstrap", 1),
                     ("c-admit", "local", "admit", 1), ("c-submit", "local", "submit", 5)])
        for expected in self.installed.values():
            require(pin(expected["path"]) == expected, "INSTALLED_CUT_CHANGED")
        for node in (self.b, self.c):
            require(pin(node["config"]) == node["config_pin"], "CONFIG_CHANGED")
        require(len(self.calls) == 20 and sum(row["role"] == "request" for row in self.calls) == 14
                and sum(row["role"] == "preparation" for row in self.calls) == 3
                and sum(row["role"] == "service" for row in self.calls) == 2
                and sum(row["role"] == "fixture-service" for row in self.calls) == 1
                and all(job["closed"] for job in self.jobs), "EXACT_TWENTY_INVOCATIONS")
        save(self.driver / "sequence.json", {"calls": self.calls, "snapshots": self.snapshots,
            "support": self.support, "native_stages": stages,
            "b_acquisition": acquired["reply"], "b_replica": replica["reply"], "c_acquisition": c_acquired["reply"],
            "c_admission": admitted["reply"], "c_artifact": artifact, "c_publication": published["reply"], "c_view": h_view,
            "order": {"a_stop": a_service["stop_offset"], "b_stop": b_service["stop_offset"],
                      "b_tamper_stop": negative_service["stop_offset"], "c_admit": admitted["job"]["record"]["started_offset"]},
            "substantive_G_dependency": "independent audit required: follow actual H proof value, establish both G applications",
            "historical_source_scope": "inert G bytes and exact H engineering workload; no borrowed acceptance or novel-growth claim"})
        return {"status": SUCCESS, "calls": 20, "installed_cli_calls": 19, "request_calls": 14,
            "new_requests": 13, "historical_replays": 1, "native_stages": 4, "pipeline_commands": 8,
            "support_build_stages": 1, "support_compilations": 2, "positive_services": 2,
            "refused_services": 1, "charged_bytes": 1016 * MIB}


def fixture_mode(args, grant):
    """One A wrapper and one genuine finite supervised static supplier."""
    require(set(grant) == {"schema", "mode", "install", "state", "root", "view", "request",
                          "view_files", "inputs", "limits", "authority"}
            and grant["schema"] == 1 and grant["mode"] == "inert-static-fixture"
            and grant["limits"] == SERVICE_LIMITS and grant["install"] == str(DATA / "install")
            and grant["state"] == str(DATA / "a") and grant["root"] == str(DATA / "a/service")
            and grant["view"] == str(DATA / "a/derivative-view"), "EXACT_FIXTURE_GRANT")
    install, root, view = checked(grant["install"]), checked(grant["root"]), checked(grant["view"])
    expected_paths = [Path(sys.executable), Path(__file__).resolve(), *[install / "py" / name for name in
                      ("peer_wire.py", "peer_service.py", "run_stage.py", "supervise.py", "domains.py")]]
    require(grant["inputs"] == [pin(path) for path in expected_paths]
            and grant["view_files"] == Scenario().file_map(view)
            and grant["request"] == {"op": "serve-static-fixture", "port": PORT_A, "seconds": 120,
                "max_requests": 2, "max_bytes": 64 * MIB}, "FIXTURE_INPUT_PINS")
    sys.path.insert(0, str(install / "py"))
    raw = encode(grant["request"])
    if args.fixture_owner:
        require(args.state is None and args.request is None and args.event is None, "FIXTURE_WRAPPER_ARGUMENTS")
        import run_stage
        import supervise
        import domains
        for module, name in ((run_stage, "run_stage.py"), (supervise, "supervise.py"), (domains, "domains.py")):
            require(pin(module.__file__) == pin(install / "py" / name), "FIXTURE_SUPERVISOR_ORIGIN")
        transport = supervise.Transport(sys.executable, Path(__file__).resolve(), args.config, DATA / "a",
            root / "cases", run_stage, dict(SERVICE_LIMITS, pins=[*grant["inputs"], pin(args.config)]))
        response = transport("serve", raw)
        sys.stdout.buffer.write(response["stdout"])
        sys.stdout.buffer.flush()
        return response["returncode"]
    require(args.state == DATA / "a" and args.request == root / "cases/serve/request.json"
            and args.event == root / "cases/serve/event.json" and not args.event.exists()
            and read(args.request, 16384) == raw, "FIXTURE_WORKER_ARGUMENTS")
    import peer_service
    import peer_wire
    for module, name in ((peer_service, "peer_service.py"), (peer_wire, "peer_wire.py")):
        require(pin(module.__file__) == pin(install / "py" / name), "FIXTURE_INERT_MODULE_ORIGIN")
    observed = peer_service.serve(view, PORT_A, root / "ready.json", session_seconds=120, max_requests=2, max_bytes=64 * MIB)
    require("checking" not in sys.modules, "FIXTURE_CHECKER_FORBIDDEN")
    reply = encode({"status": "SERVICE_STOPPED", "catalog_sha256": sha(read(view / "catalog.json", 65536)),
                    "observations": observed, "mathematicalAcceptance": False, "native_stages": 0})
    save(args.event, {"request_sha256": sha(raw), "response_sha256": sha(reply),
                     "checker_loaded": False, "native_stages": 0, "authority": "INERT_TEST_SUPPLIER_ONLY"})
    sys.stdout.buffer.write(reply)
    sys.stdout.buffer.flush()
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-owner", action="store_true")
    parser.add_argument("--config", type=Path, required=True)
    for name in ("state", "request", "event"):
        parser.add_argument("--" + name, type=Path)
    args = parser.parse_args()
    require(os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_site and sys.flags.no_user_site, "WINDOWS_STARTUP_PROFILE")
    launch = strict(read(args.config, 131072))
    if launch.get("mode") == "inert-static-fixture":
        return fixture_mode(args, launch)
    require(not args.fixture_owner and args.state == DATA and DATA.is_dir() and not any(DATA.iterdir())
            and args.request is not None and args.event is not None
            and args.event.is_absolute() and args.event.parent == args.request.parent and not args.event.exists(),
            "FIXED_FRESH_WORKER_ARGUMENTS")
    raw = read(args.request, 1024)
    require(raw == REQUEST, "FIXED_WORKER_REQUEST")
    scenario = Scenario()
    try:
        result = scenario.run(launch)
    except BaseException as error:
        result = {"status": "FAIL", "error": type(error).__name__, "detail": str(error)[:1024],
            "invocations_started": len(scenario.calls), "native_work": "inspect actual charged prefix; not zero"}
        # No further mutable-state reads after an unauthenticated lifecycle.
        # The outer Job owns all descendants and preserves cleanup/total costs.
        save(scenario.driver / "failed-prefix.json", {"calls": scenario.calls, "snapshots": scenario.snapshots,
            "failure": result, "direct_processes": [{"name": job["record"]["name"],
                "reaped": job["closed"], "observed_returncode": job["process"].poll() if job["process"] else None}
                for job in scenario.jobs]})
    result["scope"], result["elapsed_seconds"] = SCOPE, scenario.offset()
    reply = encode(result)
    require(len(reply) <= 65536, "WORKER_RESPONSE_BOUND")
    save(args.event, {"request_sha256": sha(raw), "response_sha256": sha(reply), "scope": SCOPE})
    sys.stdout.buffer.write(reply)
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

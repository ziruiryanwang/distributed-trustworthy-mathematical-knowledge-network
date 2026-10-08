"""Six-stage context-branch regression, contained by one enclosing Windows Job.

Only public installed CLIs mutate the new node. SQL observations are read-only.
Fixed engineering fixtures are not independent-agent research or useful growth.
"""
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sqlite3
import subprocess
import sys
import time

SOURCE = Path(__file__).resolve().parents[1]
DATA = SOURCE.parent / "product-local/context-native-02"
FLAGS = ["-B", "-E", "-s", "-S"]
MIB = 1048576
TABLES = {"meta": "id", "requests": "key", "records": "handle", "heads": "client",
          "providers": "provider", "snapshots": "handle", "entries": "provider,seq", "stages": "id"}
X = """universe u
def BranchCompose (A B C : Sort u) (g : B -> C) (f : A -> B) (a : A) : C :=
  g (f a)
"""
Y = """universe u
def BranchFlip (A B C : Sort u) (f : A -> B -> C) (b : B) (a : A) : C :=
  f a b
"""
Z = """universe u
def BranchComposeThree (A B C D : Sort u)
    (h : C -> D) (g : B -> C) (f : A -> B) (a : A) : D :=
  @__COMPOSE__.{u} A C D h (@__COMPOSE__.{u} A B C g f) a
"""


def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def read(path, bound=16 * MIB):
    with Path(path).open("rb") as stream:
        raw = stream.read(bound + 1)
    require(len(raw) <= bound, "READ_BOUND")
    return raw


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path):
    path = Path(path).resolve(strict=True)
    for ancestor in (path, *path.parents):
        require(not ancestor.is_symlink() and not getattr(ancestor.lstat(), "st_file_attributes", 0) & 0x400,
                "REPARSE_POINT")
    raw = read(path)
    return {"path": str(path), "bytes": len(raw), "sha256": sha(raw)}


def save_raw(path, raw):
    require(len(raw) <= 16 * MIB, "SAVE_BOUND")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def save(path, value):
    save_raw(path, encode(value))


def blob(value):
    return {"hex": value.hex()} if isinstance(value, bytes) else value


class Scenario:
    def __init__(self):
        self.install, self.state, self.scratch, self.driver = (DATA / name for name in
                                                            ("install", "state", "scratch", "driver"))
        self.config = self.state / "config.json"
        self.calls = []
        self.snapshots = []
        self.installed = {}
        self.config_pin = None

    def snapshot(self, name):
        db_path = self.state / "control.sqlite3"
        for suffix in ("-journal", "-wal", "-shm"):
            sidecar = Path(str(db_path) + suffix)
            require(not sidecar.exists() or sidecar.stat().st_size == 0, "NONEMPTY_SQLITE_SIDECAR")
        require(db_path.stat().st_size <= 32 * MIB, "DATABASE_BOUND")
        db = sqlite3.connect(db_path.as_uri() + "?mode=ro", uri=True, timeout=0, isolation_level=None)
        try:
            db.execute("PRAGMA query_only=ON")
            db.row_factory = sqlite3.Row
            value = {}
            for table, order in TABLES.items():
                rows = db.execute("SELECT * FROM " + table + " ORDER BY " + order).fetchmany(129)
                require(len(rows) <= 128, "SNAPSHOT_ROW_BOUND")
                value[table] = [{key: blob(row[key]) for key in row.keys()} for row in rows]
            save(self.driver / "snapshots" / (name + ".json"), value)
            self.snapshots.append(name)
            return value
        finally:
            db.close()

    def cli(self, name, arguments, raw=None):
        directory = self.driver / "calls" / name
        directory.mkdir(parents=True, exist_ok=False)
        command = [sys.executable, *FLAGS, *map(str, arguments)]
        save(directory / "command.json", {"argv": command, "cwd": str(self.install), "shell": False})
        before = set((self.scratch / "calls").iterdir()) if (self.scratch / "calls").exists() else set()
        started = time.monotonic()
        # The enclosing reviewed Job bounds and kills this entire process tree;
        # do not pretend a direct-wrapper timeout alone quiesces descendants.
        with (directory / "stdout.txt").open("xb") as out, (directory / "stderr.txt").open("xb") as err:
            process = subprocess.Popen(command, cwd=self.install, stdin=subprocess.DEVNULL,
                stdout=out, stderr=err, shell=False, close_fds=True, creationflags=subprocess.CREATE_NO_WINDOW)
            process.wait()
        observation = {"name": name, "returncode": process.returncode, "direct_child_reaped": True,
                       "elapsed_seconds": time.monotonic() - started,
                       "stdout": pin(directory / "stdout.txt"), "stderr": pin(directory / "stderr.txt")}
        self.calls.append(observation)
        save(directory / "process.json", observation)  # Preserve before expected outcome checks.
        output = read(directory / "stdout.txt", MIB)
        event = None
        if raw is not None:
            after = set((self.scratch / "calls").iterdir())
            added = after - before
            require(len(added) == 1, "ONE_PUBLIC_CALL")
            public = added.pop()
            receipt_path = public / "supervisor.json"
            receipt = json.loads(read(receipt_path, 65536))
            require(receipt["status"] == "TRANSPORT_COMPLETE" and receipt["returncode"] == 0
                    and receipt["direct_child_reaped"] is True and receipt["final_active_zero"] is True
                    and receipt["job_closed"] is True and not receipt.get("cleanup_errors")
                    and receipt["final_job"]["active_processes"] == 0, "PUBLIC_QUIESCENCE")
            names = ("node.py", "run_stage.py", "storage.py", "checking.py", "domains.py", "supervise.py",
                     "peer_wire.py", "peer_service.py", "peer_node.py")
            expected_pins = [self.python_pin, self.config_pin,
                             *[self.installed["py/" + name] for name in names]]
            require(receipt["pins"] == expected_pins and set(receipt["files"]) ==
                    {"request.json", "command.json", "stdout.txt", "stderr.txt", "event.json"}, "EXACT_PUBLIC_ROLES")
            for item in receipt["pins"]:
                require(pin(item["path"]) == item, "PUBLIC_PIN")
            for filename, metadata in receipt["files"].items():
                actual = pin(public / filename)
                require(metadata["present"] is True and actual["bytes"] == metadata["bytes"]
                        and actual["sha256"] == metadata["sha256"], "PUBLIC_OUTPUT_BINDING")
            require(read(public / "request.json", 131072) == raw
                    and read(public / "stdout.txt", MIB) == output, "EXACT_PUBLIC_IO")
            event = json.loads(read(public / "event.json", 65536))
            require(receipt["request_sha256"] == sha(raw) and event["request_sha256"] == sha(raw)
                    and event["response_sha256"] == sha(output)
                    and event["origin_directory"] == str(public), "EVENT_IO_BINDING")
            actual_command = json.loads(read(public / "command.json", 65536))
            require(actual_command["argv"] == [sys.executable, *FLAGS, str(self.install / "py/node.py"),
                    "--config", str(self.config), "--state", str(self.state), "--request",
                    str(public / "request.json"), "--event", str(public / "event.json")]
                    and actual_command["cwd"] == str(self.install / "py") and actual_command["shell"] is False
                    and actual_command["creationflags"] == 0x4 | subprocess.CREATE_NO_WINDOW
                    and actual_command["environment_override"] == {"PYTHONDONTWRITEBYTECODE": "1"}, "PUBLIC_COMMAND")
            observation["public"] = pin(receipt_path)
            observation["event"] = pin(public / "event.json")
            save(directory / "binding.json", observation)
        require(process.returncode == 0, "CLI_FAILED:" + name)
        return output, json.loads(output), event

    def request(self, name, op=None, arguments=None, *, client="local", replay=None):
        raw = read(self.driver / "requests" / (replay + ".json"), 131072) if replay else encode(
            {"client": client, "request_id": name, "op": op, "args": arguments})
        path = self.driver / "requests" / (name + ".json")
        save_raw(path, raw)
        before = self.snapshot(name + "-before") if self.config.exists() and (self.state / "control.sqlite3").exists() else None
        output, value, event = self.cli(name, [self.install / "manage.py", "request", "--config", self.config,
                                             "--request", path], raw)
        after = self.snapshot(name + "-after")
        if replay:
            require(output == read(self.driver / "calls" / replay / "stdout.txt", MIB)
                    and after == before and event["historical"] is True
                    and event["checker_loaded"] is False and event["stages_allocated"] == 0, "EXACT_REPLAY")
        return value, event, before, after, raw, output

    def data(self, snapshot, handle):
        rows = [row for row in snapshot["records"] if row["handle"] == handle]
        require(len(rows) == 1, "RECORD_SINGLETON")
        raw = bytes.fromhex(rows[0]["raw"]["hex"])
        require(handle == rows[0]["kind"] + ":" + sha(raw), "RECORD_DIGEST")
        return json.loads(raw)["data"]

    def metadata_delta(self, invocation, selected=None):
        value, event, before, after, raw, output = invocation
        request = json.loads(raw)
        key = sha(encode([request["client"], request["request_id"]]))
        expected = deepcopy(before)
        expected["meta"][0]["requests"] += 1
        expected["meta"][0]["charged"] += 8 * MIB
        expected["meta"][0]["active"] = None
        expected["requests"].append({"key": key, "client": request["client"],
            "request_id": request["request_id"], "raw": blob(raw), "phase": "terminal", "response": blob(output)})
        expected["requests"].sort(key=lambda row: row["key"])
        marker = encode({"config": before["meta"][0]["config"], "kind": "attempt", "client": "owner",
                         "data": {"request": key, "call_directory": event["origin_directory"]}})
        expected["records"].append({"handle": "attempt:" + sha(marker), "kind": "attempt", "client": "owner", "raw": blob(marker)})
        expected["records"].sort(key=lambda row: row["handle"])
        if selected is not None:
            require(len(expected["heads"]) == 1, "SINGLE_LOCAL_HEAD")
            expected["heads"][0]["context"] = selected
        require(after == expected and event["stages_allocated"] == 0, "EXACT_METADATA_DELTA")

    def frozen_files(self):
        files = list((self.state / "work").rglob("*"))
        require(len(files) <= 8192, "FROZEN_FILE_BOUND")
        return [pin(path) for path in files if path.is_file()]

    def run(self, launch):
        require(set(launch) == {"schema", "pins", "product", "limits", "retained"}
                and type(launch["schema"]) is int and launch["schema"] == 1, "LAUNCH_FIELDS")
        require(type(launch["product"]) is list and len(launch["product"]) == 98, "PRODUCT_COUNT")
        self.python_pin = pin(sys.executable)
        require(self.python_pin == launch["pins"][0], "PYTHON_PIN")
        self.install.mkdir()
        relative_seen = set()
        for item in launch["product"]:
            require(set(item) == {"relative", "path", "bytes", "sha256"}, "PRODUCT_PIN_FIELDS")
            relative = PurePosixPath(item["relative"])
            require(not relative.is_absolute() and ".." not in relative.parts and ":" not in str(relative)
                    and "\\" not in str(relative) and str(relative) not in relative_seen, "PRODUCT_RELATIVE")
            relative_seen.add(str(relative))
            source = SOURCE / str(relative)
            require(pin(source) == {key: item[key] for key in ("path", "bytes", "sha256")}, "PRODUCT_PIN")
            save_raw(self.install / str(relative), read(source))
            copied = pin(self.install / str(relative))
            require(copied["bytes"] == item["bytes"] and copied["sha256"] == item["sha256"], "PRODUCT_COPY")
            self.installed[str(relative)] = copied
        save(self.driver / "installed-source-pins.json", [pin(self.install / name) for name in sorted(relative_seen)])
        runtime = SOURCE / "runtime/lean-4.34.0-windows"
        require(pin(runtime / "bin/lean.exe") == launch["pins"][-1], "LEAN_PIN")
        self.cli("build", [self.install / "build.py", "--lean-runtime", runtime, "--work", DATA / "build-work"])
        build = json.loads(read(self.install / "build/build-receipt.json"))
        support = json.loads(read(build["stage_receipt"]["path"]))
        require(build["status"] == "LOCAL_SUPPORT_BUILD_COMPLETED_NOT_MATH_ACCEPTANCE"
                and len(support["steps"]) == 2 and support["final_job"]["active_processes"] == 0, "SUPPORT_BUILD")
        self.cli("configure", [self.install / "manage.py", "configure", "--state", self.state,
                "--scratch", self.scratch, "--lean-runtime", runtime, "--client", "local", "--context-packages", "6"])
        config = json.loads(read(self.config))
        self.config_pin = pin(self.config)
        require(config["limits"]["packages"] == 6 and len(config["common"]["packages"]) == 5, "CAP_SIX")
        init = self.request("init", "init", {}, client="owner")
        require(init[0].get("accepted") is True, "INIT_ACCEPTANCE")
        c0, s0 = init[0]["contexts"]["local"], init[0]["snapshots"]["P1"]
        require(len(self.data(init[3], c0)["packages"]) == 5, "BOOTSTRAP_FIVE")
        save_raw(self.driver / "X.lean", X.encode())
        save_raw(self.driver / "Y.lean", Y.encode())
        x = self.request("submit-x", "submit", {"context": c0, "source": X, "root": "BranchCompose"})
        require(x[0].get("accepted") is True, "X_ACCEPTANCE")
        px = self.request("publish-x", "publish", {"artifact": x[0]["artifact"], "snapshot": s0})
        require(px[0]["status"] == "OK" and px[0]["existing"] is False, "X_PUBLICATION")
        y = self.request("submit-y", "submit", {"context": c0, "source": Y, "root": "BranchFlip"})
        require(y[0].get("accepted") is True, "Y_ACCEPTANCE")
        py = self.request("publish-y", "publish", {"artifact": y[0]["artifact"], "snapshot": px[0]["snapshot"]})
        require(py[0]["status"] == "OK" and py[0]["existing"] is False
                and px[0]["descriptor_id"] != py[0]["descriptor_id"], "Y_DISTINCT_PUBLICATION")
        ay = self.request("admit-y", "admit", {"context": c0, "selected": [py[0]["candidate"]]})
        require(ay[0].get("accepted") is True, "Y_ADMISSION")
        cy = ay[0]["context"]
        require(len(self.data(ay[3], cy)["packages"]) == 6, "Y_CONTEXT_SIX")
        refused = self.request("refused-x", "admit", {"context": cy, "selected": [px[0]["candidate"]]})
        require(refused[0]["status"] == "REFUSED" and refused[0]["code"] == "CONTEXT_PACKAGE_COUNT",
                "EXACT_CAP_REFUSAL")
        require(refused[1]["checker_loaded"] is True and refused[1]["checker_metrics"]["stage_allocations"] == 0
                and refused[1]["checker_metrics"]["pipeline_children"] == 0, "CAP_REFUSAL_NO_NATIVE")
        self.metadata_delta(refused)
        frozen = self.frozen_files()
        save(self.driver / "preserved-work-before-selection.json", frozen)
        selected = self.request("select-bootstrap", "select_context", {"context": cy, "selected": c0})
        require(selected[0] == {"status": "OK", "client": "local", "previous_context": cy,
                "context": c0, "changed": True, "mathematicalAcceptance": False,
                "context_record_authenticated": True, "live_context_status": "UNCHECKED", "native_stages": 0}
                and selected[1]["checker_loaded"] is False, "SELECTION_RESPONSE")
        self.metadata_delta(selected, c0)
        ax = self.request("admit-x", "admit", {"context": c0, "selected": [px[0]["candidate"]]})
        require(ax[0].get("accepted") is True, "X_ADMISSION")
        cx = ax[0]["context"]
        require(len(self.data(ax[3], cx)["packages"]) == 6, "X_CONTEXT_SIX")
        rows = ax[0]["description"]["rows"]
        require(len(rows) == 1 and rows[0]["kind"] == "definition" and rows[0]["u"] == 1, "X_PUBLIC_DEFINITION")
        original_rows = x[0]["description"]["rows"]
        require(len(original_rows) == 1 and rows[0] == original_rows[0], "X_RECEPTION_DESCRIPTION_IDENTITY")
        name = rows[0]["leanName"]
        require(type(name) is str and len(name) <= 256
                and re.fullmatch(r"DTMKN\.d\.\u00ab[0-9a-f]+\u00bb", name), "X_PUBLIC_NAME")
        source_z = Z.replace("__COMPOSE__", name)
        save_raw(self.driver / "Z.lean", source_z.encode())
        z = self.request("submit-z", "submit", {"context": cx, "source": source_z, "root": "BranchComposeThree"})
        require(z[0].get("accepted") is True, "Z_ACCEPTANCE")
        self.request("selection-replay", replay="select-bootstrap")
        final = self.request("refusal-replay", replay="refused-x")[3]
        require(final["heads"] == [{"client": "local", "context": cx}], "FINAL_HEAD")
        require(final["meta"][0]["requests"] == 10 and final["meta"][0]["stages"] == 6
                and final["meta"][0]["charged"] == 848 * MIB and final["meta"][0]["active"] is None,
                "FINAL_CHARGES")
        require(len(self.calls) == 14 and len(final["stages"]) == 6, "EXACT_CALL_STAGE_COUNTS")
        actual_stages = []
        stage_sequence = (("init", "owner", "bootstrap", 1), ("submit-x", "local", "submit", 5),
                          ("submit-y", "local", "submit", 5), ("admit-y", "local", "admit", 1),
                          ("admit-x", "local", "admit", 1), ("submit-z", "local", "submit", 5))
        for index, (stage, (identity, client, purpose, children)) in enumerate(zip(final["stages"], stage_sequence)):
            key = sha(encode([client, identity]))
            directory = self.state / "work" / key / ("stage-%04d" % index)
            require(stage == {"id": index, "request": key, "purpose": purpose,
                    "directory": str(directory), "grant_bytes": 128 * MIB}, "EXACT_STAGE_ASSIGNMENT")
            path = Path(stage["directory"]) / "stage.json"
            receipt = json.loads(read(path, MIB))
            plan_path = directory / "plan.json"
            plan = json.loads(read(plan_path, MIB))
            require(receipt["status"] == "STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE"
                    and receipt["final_job"]["active_processes"] == 0
                    and receipt["execution_endpoint"]["children_quiescent"] is True
                    and all(step["exit_code"] == 0 for step in receipt["steps"]), "NATIVE_STAGE_RECEIPT")
            require(receipt["stage"] == str(index) and receipt["accounting_root"] == str(directory)
                    and receipt["request_directory"] == str(directory.parent)
                    and receipt["plan"] == pin(plan_path) and receipt["expected_plan_sha256"] == sha(read(plan_path, MIB))
                    and plan["stage"] == str(index) and plan["stage_directory"] == str(directory)
                    and plan["request_directory"] == str(directory.parent)
                    and receipt["domains"] == config["domains"] and plan["domains"] == config["domains"]
                    and len(receipt["steps"]) == children and len(plan["steps"]) == children, "STAGE_PLAN_BINDING")
            actual_stages.append({"receipt": pin(path), "children": len(receipt["steps"])})
        require(sum(stage["children"] for stage in actual_stages) == 18, "EXACT_PIPELINE_COUNT")
        for old in frozen:
            require(pin(old["path"]) == old, "OLD_WORK_CHANGED")
        before_records = {row["handle"]: row for row in refused[3]["records"]}
        final_records = {row["handle"]: row for row in final["records"]}
        require(all(final_records.get(key) == row for key, row in before_records.items()), "OLD_RECORD_CHANGED")
        for table, key in (("requests", "key"), ("stages", "id")):
            current = {row[key]: row for row in final[table]}
            require(all(current.get(row[key]) == row for row in refused[3][table]), "OLD_" + table + "_CHANGED")
        require(all(final[table] == refused[3][table] for table in ("entries", "providers", "snapshots")),
                "PUBLISHED_CORPUS_CHANGED")
        save(self.driver / "sequence.json", {"calls": self.calls, "snapshots": self.snapshots,
            "contexts": {"bootstrap": c0, "y": cy, "x": cx}, "artifacts": {"x": x[0]["artifact"],
            "y": y[0]["artifact"], "z": z[0]["artifact"]}, "stages": actual_stages,
            "source_authorship": "fixed engineering fixtures; Z replaces only the returned X identifier",
            "dependency_audit": "PENDING; distinct descriptors alone do not prove dependency separation/reuse"})
        return {"status": "PASS_PENDING_DEPENDENCY_AUDIT", "calls": 14, "ordinary_requests": 10,
                "native_stages": 6, "pipeline_children": 18, "support_build_stages": 1,
                "support_compilations": 2, "charged_bytes": 848 * MIB}


def main():
    parser = argparse.ArgumentParser()
    for name in ("config", "state", "request", "event"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    require(os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_site and sys.flags.no_user_site, "WINDOWS_STARTUP_PROFILE")
    raw = read(args.request, 1024)
    require(raw == b'{"op":"test-context-native"}\n' and args.state.resolve() == DATA
            and DATA.is_dir() and not any(DATA.iterdir()), "FIXED_FRESH_STATE_REQUEST")
    scenario = Scenario()
    started = time.monotonic()
    try:
        result = scenario.run(json.loads(read(args.config, 131072)))
    except BaseException as error:
        result = {"status": "FAIL", "error": type(error).__name__, "detail": str(error)[:1024],
                  "completed_cli_observations": len(scenario.calls), "native_work": "inspect actual retained prefix, not zero"}
        save(scenario.driver / "failed-prefix.json", {"calls": scenario.calls, "snapshots": scenario.snapshots,
                                                     "failure": result})
    result["scope"] = "fixed native context-branch regression; not useful growth or independent-host qualification"
    result["elapsed_seconds"] = time.monotonic() - started
    reply = encode(result)
    save(args.event, {"request_sha256": sha(raw), "response_sha256": sha(reply),
                      "scope": result["scope"]})
    sys.stdout.buffer.write(reply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Four native-free v3 integration contracts; root alone stages and executes.

Real SQLite/dispatcher paths, explicitly synthetic workloads and mocked supply.
No proof, context, support build, native execution or acceptance is fabricated.
"""
from contextlib import ExitStack
import hashlib
import io
import json
import os
from pathlib import Path
import sqlite3
import stat
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

if not (os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
        and sys.flags.no_site and sys.flags.no_user_site):
    raise RuntimeError("WINDOWS_PYTHON_PROFILE")
if sqlite3.sqlite_version != "3.50.4":
    raise RuntimeError("SQLITE_PROFILE")

INSTALL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(INSTALL))
sys.path.insert(0, str(INSTALL / "py"))
import capacity as C
import storage as S
import domains as D
import node as N
import manage as M
import build as B
import run_stage as R

for module, relative in ((C, "py/capacity.py"), (S, "py/storage.py"),
        (D, "py/domains.py"), (N, "py/node.py"), (M, "manage.py"),
        (B, "build.py"), (R, "py/run_stage.py")):
    if Path(module.__file__).resolve() != INSTALL / relative:
        raise RuntimeError("STAGED_MODULE_ORIGIN")

MIB = 1048576
CONFIG = "c" * 64
TABLES = {"meta": "id", "authorization": "id", "owner_grants": "sequence",
          "requests": "key", "records": "handle", "heads": "client",
          "providers": "provider", "snapshots": "handle", "entries": "provider,seq", "stages": "id"}


class PrefixBoundary(Exception):
    pass


def event():
    return {"checker_loaded": False, "checker_metrics": {}, "sql_vm_steps": 0,
            "sql_opened": False, "sql_rows": {}, "stages_allocated": 0,
            "historical": False, "fetched_sequences": [], "consumed_sequences": []}


def safe(path):
    path = Path(path)
    S.require(path.is_absolute(), "ABSOLUTE_TEST_ROOT")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        S.require(not stat.S_ISLNK(info.st_mode)
                  and not getattr(info, "st_file_attributes", 0) & 0x400, "TEST_REPARSE_POINT")
    return path.resolve(strict=True)


class CapacityIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = safe(os.environ.get("DTMKN_TEST_ROOT", ""))
        S.require(parent.is_dir() and not parent.is_relative_to(INSTALL)
                  and not INSTALL.is_relative_to(parent), "EXTERNAL_TEST_ROOT")
        cls.suite = parent / "capacity-integration"
        cls.suite.mkdir(exist_ok=False)

    def setUp(self):
        self.root = self.suite / self._testMethodName
        self.root.mkdir(exist_ok=False)
        self.stores, self.notes = [], {}
        for target, name, replacement in ((S, "physical_supply", self.fake_supply),
                (N.Dispatcher, "checking", self.forbidden), (N.Dispatcher, "peering", self.forbidden),
                (subprocess, "Popen", self.forbidden), (R, "Job", self.forbidden)):
            handle = patch.object(target, name, replacement)
            handle.start()
            self.addCleanup(handle.stop)

    def forbidden(self, *args, **kwargs):
        raise AssertionError("UNALLOCATED_NATIVE_PROCESS_OR_SIDE_EFFECT")

    def fake_supply(self, root, scratch, remaining, pages, *, enforce=True):
        return {"mocked": True, "sample_only": True, "reserved_by_os": False,
                "sufficient": True, "remaining_authorized_bytes": remaining,
                "metadata_pages": pages, "enforce": enforce}

    def save(self, path, raw):
        self.assertLessEqual(len(raw), MIB)
        with path.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())

    def files(self, root=None):
        root = self.root if root is None else Path(root)
        result, total = {}, 0
        for count, path in enumerate(root.rglob("*"), 1):
            S.require(count <= 1024, "FIXTURE_ENTRY_BOUND")
            safe(path)
            if path.is_file():
                size = path.stat().st_size
                total += size
                S.require(total <= 64 * MIB and len(result) < 256, "FIXTURE_FILE_BOUND")
                digest = hashlib.sha256()
                with path.open("rb") as stream:
                    for raw in iter(lambda: stream.read(MIB), b""):
                        digest.update(raw)
                result[path.relative_to(root).as_posix()] = {"bytes": size, "sha256": digest.hexdigest()}
        return result

    def configuration(self, name="node"):
        base = self.root / name
        base.mkdir(exist_ok=False)
        for child in ("runtime", "scratch"):
            (base / child).mkdir()
        return {"schema": 3, "config_id": CONFIG, "clients": ["local"],
            "limits": {"requests": 4, "stages": 1, "staging_bytes": 160 * MIB,
                "metadata_pages": 8192, "request_bytes": 8 * MIB, "stage_bytes": 128 * MIB,
                "peer_request_bytes": 64 * MIB, "expose_request_bytes": 80 * MIB,
                "native_seconds": 30, "native_memory_mib": 128, "entries": 8192},
            "domains": {"install": str(INSTALL), "state": str(base / "state"),
                "scratch": str(base / "scratch"), "lean_runtime": str(base / "runtime")}}

    def open(self, config, *, create=False):
        store = S.ControlStore(config["domains"]["state"], CONFIG, config["limits"], event(),
                               create=create, scratch=config["domains"]["scratch"])
        self.stores.append(store)
        return store

    def close(self, store):
        store.close()
        self.stores.remove(store)

    def snapshot(self, store):
        def compact(value):
            return {"bytes": len(value), "sha256": S.digest(value)} if type(value) is bytes else value
        return {table: [[compact(value) for value in row] for row in
            store.rows("test_" + table, "SELECT * FROM " + table + " ORDER BY " + order, maximum=128)]
            for table, order in TABLES.items()}

    def test_configure_capacity_types_refuse_before_pin_build_or_write(self):
        runtime = self.root / "runtime"
        runtime.mkdir()
        args = {"state": self.root / "absent-state", "scratch": self.root / "absent-scratch",
            "lean_runtime": runtime, "client": ["local"], "peer": [], "context_packages": 16,
            "initial_requests": 2, "initial_stages": 1,
            "initial_reserved_mib": 144, "initial_metadata_mib": 32}
        before, cases = self.files(), 0
        with ExitStack() as stack:
            for target, name in ((M, "pin"), (M, "save_new"), (B, "assets"), (B, "read_record"),
                    (B, "build"), (C, "physical_supply"), (Path, "mkdir"), (Path, "open")):
                stack.enter_context(patch.object(target, name, side_effect=self.forbidden))
            for field, code, boundaries in (
                    ("initial_requests", "INITIAL_REQUESTS", (0, 4097)),
                    ("initial_stages", "INITIAL_STAGES", (0, 257)),
                    ("initial_reserved_mib", "INITIAL_RESERVED_MIB", (135, 65537)),
                    ("initial_metadata_mib", "INITIAL_METADATA_MIB", (0, 33))):
                for bad in (True, False, -1, 1.5, "2", None, 2 ** 100, *boundaries):
                    with self.subTest(field=field, value=repr(bad)):
                        with self.assertRaises(S.Refusal) as failure:
                            M.configure(SimpleNamespace(**dict(args, **{field: bad})))
                        self.assertEqual(failure.exception.code, code)
                        cases += 1
        self.assertEqual(before, self.files())
        self.assertFalse(args["state"].exists())
        self.assertFalse(args["scratch"].exists())
        self.notes["rejected_configuration_cases"] = cases

    def test_distinct_domain_readers_and_actual_runner_builder_prefixes(self):
        config = self.configuration()
        domains = D.Domains.from_config(config)
        plan = {"schema": 2, "domains": domains.as_dict()}
        self.assertEqual(D.Domains.from_stage_plan(plan).as_dict(), domains.as_dict())
        for schema in (2, True, 3.0):
            with self.subTest(reader="config", schema=schema), self.assertRaisesRegex(ValueError, "CONFIG_DOMAIN_SCHEMA"):
                D.Domains.from_config(dict(config, schema=schema))
        for schema in (3, True, 2.0):
            with self.subTest(reader="stage", schema=schema), self.assertRaisesRegex(ValueError, "STAGE_DOMAIN_SCHEMA"):
                D.Domains.from_stage_plan(dict(plan, schema=schema))
        for schema in (2, 3):
            path = self.root / ("stage-prefix-" + str(schema) + ".json")
            raw = S.encode(dict(plan, schema=schema, request_directory=str(self.root / "uncreated-request")))
            self.save(path, raw)
            before = self.files()
            with patch.object(D.Domains, "from_config", side_effect=self.forbidden), \
                 patch.object(D.Domains, "from_stage_plan", wraps=D.Domains.from_stage_plan) as reader, \
                 patch.object(D.Domains, "require_work", side_effect=PrefixBoundary("validated-stage-domains")), \
                 patch.object(Path, "mkdir", side_effect=self.forbidden):
                if schema == 2:
                    with self.assertRaisesRegex(PrefixBoundary, "validated-stage-domains"):
                        R.execute(path, self.root / "uncreated-stage", "prefix", S.digest(raw))
                else:
                    with self.assertRaisesRegex(ValueError, "STAGE_DOMAIN_SCHEMA"):
                        R.execute(path, self.root / "uncreated-stage", "prefix", S.digest(raw))
                reader.assert_called_once()
                self.assertEqual(reader.call_args.args[0]["schema"], schema)
            self.assertEqual(before, self.files())
        # A fresh test-only install domain permits build's real prefix to reach
        # its assets boundary; no source pin/build receipt/output is fabricated.
        install = self.root / "prefix-install"
        (install / "py").mkdir(parents=True)
        before = self.files()
        args = SimpleNamespace(work=self.root / "uncreated-build", lean_runtime=Path(config["domains"]["lean_runtime"]))
        with patch.object(B, "INSTALL", install), \
             patch.object(D.Domains, "from_config", side_effect=self.forbidden), \
             patch.object(D.Domains, "from_stage_plan", wraps=D.Domains.from_stage_plan) as reader, \
             patch.object(B, "assets", side_effect=PrefixBoundary("validated-build-domains")), \
             patch.object(B, "pin", side_effect=self.forbidden), \
             patch.object(B, "save_new", side_effect=self.forbidden), \
             patch.object(Path, "mkdir", side_effect=self.forbidden):
            with self.assertRaisesRegex(PrefixBoundary, "validated-build-domains"):
                B.build(args)
            reader.assert_called_once()
            self.assertEqual(reader.call_args.args[0]["schema"], 2)
        self.assertEqual(before, self.files())
        self.notes["reader_scope"] = "actual runner/build prefixes only; no stage or support build"

    def test_real_sqlite_full_dispatcher_rollback_terminal_refusal_and_replay(self):
        config = self.configuration()
        raw = S.encode({"client": "local", "request_id": "real-full", "op": "info", "args": {}})
        req = N.request(raw, config["clients"])
        observed = {"attempts": 0, "payload_bytes": 0, "sqlite_errorcode": None, "terminal_calls": 0}
        self.notes["real_full"] = observed
        with S.owner_lock(config["domains"]["state"]):
            store = self.open(config, create=True)
            dispatcher = N.Dispatcher(config, store, store.event)
            baseline, pending = self.snapshot(store), {}
            def prepare(_request):
                pending.update(self.snapshot(store))
                return None
            def workload(_request, _prepared):
                for index in range(12):
                    data = {"index": index, "padding": "x" * (2 * MIB - 1024)}
                    payload = S.encode({"config": CONFIG, "kind": "synthetic-pressure", "client": "local", "data": data})
                    observed["attempts"] += 1
                    observed["payload_bytes"] += len(payload)
                    self.assertLessEqual(observed["payload_bytes"], 30 * MIB)
                    try:
                        store.put_record("synthetic-pressure", "local", data)
                    except sqlite3.Error as error:
                        observed["sqlite_errorcode"] = getattr(error, "sqlite_errorcode", None)
                        raise
                raise AssertionError("BOUNDED_FIXTURE_DID_NOT_REACH_SQLITE_FULL")
            terminal = store.terminal_refusal
            def after_rollback(key, reply):
                observed["terminal_calls"] += 1
                self.assertFalse(store.db.in_transaction)
                self.assertTrue(store.event["transaction_rollback_confirmed"])
                self.assertEqual(self.snapshot(store), pending)
                return terminal(key, reply)
            with patch.object(dispatcher, "prepare", side_effect=prepare), \
                 patch.object(dispatcher, "commit_operation", side_effect=workload), \
                 patch.object(store, "terminal_refusal", side_effect=after_rollback):
                reply = dispatcher.execute(req, raw)
            self.assertEqual(observed["sqlite_errorcode"], sqlite3.SQLITE_FULL)
            self.assertLessEqual(observed["attempts"], 12)
            self.assertEqual(observed["terminal_calls"], 1)
            self.assertEqual(S.decode(reply), {"status": "REFUSED", "code": "METADATA_SPACE", "detail": ""})
            self.assertLessEqual(len(reply), 4096)
            self.assertTrue(store.event["terminal_only_completion"])
            self.assertFalse(store._uncertain)
            self.assertFalse(store.event["checker_loaded"])
            self.assertEqual(store.event["stages_allocated"], 0)
            self.assertEqual(store.authorization_state()["used"], {"requests": 1, "stages": 0, "reserved_bytes": 8 * MIB})
            self.assertIsNone(store.meta()["active"])
            after = self.snapshot(store)
            for table in set(TABLES) - {"meta", "requests"}:
                self.assertEqual(baseline[table], after[table], table)
            with patch.object(dispatcher, "prepare", side_effect=self.forbidden), \
                 patch.object(store, "reserve", side_effect=self.forbidden), \
                 patch.object(S, "physical_supply", side_effect=self.forbidden):
                self.assertEqual(dispatcher.execute(req, raw), reply)
            self.assertTrue(store.event["historical"])
            self.assertEqual(after, self.snapshot(store))
            self.notes["post_refusal_pages"] = store.page_count()
            self.close(store)

    def test_node_commit_uncertainty_blocks_without_secondary_terminal_clear(self):
        outcomes = []
        self.notes["commit_boundaries"] = outcomes
        for operation in ("reserve", "completion"):
            for after_commit in (False, True):
                with self.subTest(operation=operation, after_commit=after_commit):
                    config = self.configuration(operation + str(after_commit))
                    state = Path(config["domains"]["state"])
                    with S.owner_lock(state):
                        store = self.open(config, create=True)
                        before = self.snapshot(store)
                        self.close(store)
                    raw = S.encode({"client": "local", "request_id": "uncertain", "op": "info", "args": {}})
                    request_path = state.parent / "request.json"
                    event_path = Path(config["domains"]["scratch"]) / "event.json"
                    self.save(request_path, raw)
                    stdout = SimpleNamespace(buffer=io.BytesIO())
                    argv = ["node.py", "--config", str(state.parent / "mocked-config.json"),
                        "--state", str(state), "--request", str(request_path), "--event", str(event_path)]
                    actual_exec, commits = S.ControlStore.exec, []
                    target = 1 if operation == "reserve" else 2
                    def injected(instance, name, statement, values=()):
                        if name == "commit":
                            commits.append(name)
                            if len(commits) == target:
                                if after_commit:
                                    actual_exec(instance, name, statement, values)
                                raise OSError("synthetic-commit-boundary")
                        return actual_exec(instance, name, statement, values)
                    completion = {"status": "REFUSED", "code": "SYNTHETIC_COMPLETION"}
                    with patch.object(S.ControlStore, "exec", new=injected), \
                         patch.object(S.ControlStore, "terminal_refusal", side_effect=self.forbidden) as terminal, \
                         patch.object(N.Dispatcher, "prepare", return_value=None), \
                         patch.object(N.Dispatcher, "commit_operation", return_value=completion), \
                         patch.object(N, "load_config", return_value=config), \
                         patch.object(sys, "argv", argv), patch.object(sys, "stdout", stdout):
                        code = N.main()
                    self.assertEqual(code, 0)
                    terminal.assert_not_called()
                    self.assertEqual(len(commits), target)
                    reply_raw = stdout.buffer.getvalue()
                    reply = S.decode(reply_raw)
                    self.assertEqual(reply["status"], "BLOCKED")
                    self.assertEqual(reply["code"], "TRANSACTION_OUTCOME_UNKNOWN")
                    if operation == "reserve":
                        self.assertEqual(reply["state_outcome"], "UNKNOWN")
                    else:
                        self.assertNotIn("state_outcome", reply)  # Current explicit contract, not an inferred field.
                    with event_path.open("rb") as stream:
                        observation = json.load(stream)  # Runtime events contain finite timing floats.
                    self.assertTrue(observation["transaction_outcome_unknown"])
                    self.assertEqual(observation["response_sha256"], S.digest(reply_raw))
                    self.assertFalse(observation["checker_loaded"])
                    self.assertEqual(observation["stages_allocated"], 0)
                    with S.owner_lock(state, create=False):
                        store = self.open(config)
                        reserved = operation == "completion" or after_commit
                        completed = operation == "completion" and after_commit
                        self.assertEqual(store.authorization_state()["used"], {
                            "requests": int(reserved), "stages": 0, "reserved_bytes": int(reserved) * 8 * MIB})
                        key = S.digest(S.encode(["local", "uncertain"]))
                        self.assertEqual(store.meta()["active"], key if reserved and not completed else None)
                        rows = store.rows("observed_request", "SELECT phase,response FROM requests WHERE key=?", (key,))
                        self.assertEqual(len(rows), int(reserved))
                        if reserved:
                            self.assertEqual(rows[0]["phase"], "terminal" if completed else "pending")
                            self.assertEqual(rows[0]["response"], S.encode(completion) if completed else None)
                        else:
                            self.assertEqual(before, self.snapshot(store))
                        outcomes.append({"operation": operation, "after_actual_commit": after_commit,
                            "reply": reply, "reserved": reserved, "completed": completed,
                            "no_secondary_terminal_refusal": True})
                        self.close(store)

    def tearDown(self):
        errors = []
        for store in self.stores:
            try:
                store.close()
            except BaseException as error:
                errors.append(type(error).__name__)
        rows, observation_error = {}, None
        try:
            rows = self.files()
        except Exception as error:
            observation_error = type(error).__name__ + ":" + str(error)[:512]
        report = S.encode({"test": self.id(), "synthetic_workloads": True, "native_acceptance": False,
            "physical_supply_mocked": True, "notes": self.notes, "close_errors": errors,
            "observation_error": observation_error, "retained_files_before_report": rows,
            "outcome_authority": "separate unittest result, not existence of this report"})
        self.save(self.root / "observations.json", report)
        self.assertIsNone(observation_error)
        self.assertLessEqual(sum(row["bytes"] for row in rows.values()) + len(report), 32 * MIB)
        self.assertLessEqual(sum(row["bytes"] for row in self.files(self.suite).values()), 64 * MIB)
        self.assertFalse(errors)


if __name__ == "__main__":
    unittest.main(verbosity=2)

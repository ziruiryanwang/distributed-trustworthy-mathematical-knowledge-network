"""Ordinary-abort state contracts, not native interruption qualification.

Real SQLite transactions and Windows owner locks; synthetic initialization,
stage bookkeeping and quiescence receipts; mocked physical supply. No Lean,
process launch, mathematical acceptance or source-cut attestation is fabricated.
Root alone imports/executes after review under a fresh bounded allocation.
"""
from contextlib import ExitStack
from copy import deepcopy
import hashlib
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
sys.path.insert(0, str(INSTALL / "py"))
import storage as S
import capacity as C
import node as N
import domains as D
import recovery_worker as R
import recovery_manage as M

for module, name in ((S, "storage"), (C, "capacity"), (N, "node"), (D, "domains"),
                     (R, "recovery_worker"), (M, "recovery_manage")):
    if Path(module.__file__).resolve() != INSTALL / "py" / (name + ".py"):
        raise RuntimeError("PRODUCT_MODULE_ORIGIN")

MIB = 1048576
CONFIG = "d" * 64
TABLES = {"meta": "id", "authorization": "id", "owner_grants": "sequence",
          "requests": "key", "records": "handle", "heads": "client",
          "providers": "provider", "snapshots": "handle", "entries": "provider,seq", "stages": "id"}


def event():
    return {"sql_vm_steps": 0, "sql_rows": {}, "sql_opened": False,
            "stages_allocated": 0, "historical": False,
            "terminal_write_attempted": False, "transition_committed": False,
            "state_outcome": "UNCHANGED_BY_RECOVERY"}


def quiescence():
    # Explicit synthetic input to guard tests, NOT an observed supervisor result.
    return {"job_created_before_process": True, "attach_resume_returned": True,
            "direct_child_reaped": True, "final_active_zero": True, "job_closed": True,
            "pid": 123, "returncode": 1, "initial_job": {"active_processes": 0},
            "final_job": {"active_processes": 0, "total_processes": 4,
                          "terminated_processes": 3}, "cleanup_errors": []}


def safe(path):
    path = Path(path)
    S.require(path.is_absolute(), "ABSOLUTE_TEST_ROOT")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        S.require(not stat.S_ISLNK(info.st_mode)
                  and not getattr(info, "st_file_attributes", 0) & 0x400, "TEST_REPARSE_POINT")
    return path.resolve(strict=True)


class OrdinaryAbortTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = safe(os.environ.get("DTMKN_TEST_ROOT", ""))
        S.require(parent.is_dir() and not parent.is_relative_to(INSTALL)
                  and not INSTALL.is_relative_to(parent), "EXTERNAL_TEST_ROOT")
        cls.suite = parent / "ordinary-abort"
        cls.suite.mkdir(exist_ok=False)

    def setUp(self):
        self.root = self.suite / self._testMethodName
        self.root.mkdir(exist_ok=False)
        self.stack, self.stores, self.notes = ExitStack(), [], {}
        self.stack.enter_context(patch.object(S, "physical_supply", self.fake_supply))
        self.stack.enter_context(patch.object(N.Dispatcher, "checking", self.forbidden))
        self.stack.enter_context(patch.object(subprocess, "Popen", self.forbidden))

    def forbidden(self, *args, **kwargs):
        raise AssertionError("NATIVE_OR_PROCESS_EXECUTION_FORBIDDEN")

    def fake_supply(self, *args, **kwargs):
        return {"mocked": True, "sufficient": True, "reserved_by_os": False}

    def save(self, path, raw):
        S.require(type(raw) is bytes and len(raw) <= MIB, "FIXTURE_OUTPUT_BOUND")
        with path.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())

    def fixture(self, name="node", *, op="submit", stage=True, saturated=False, attempt=True):
        base = self.root / name
        base.mkdir(exist_ok=False)
        state, scratch = base / "state", base / "scratch"
        scratch.mkdir()
        self.stack.enter_context(S.owner_lock(state))
        limits = {"requests": 1 if saturated else 8, "stages": 1 if saturated else 4,
            "staging_bytes": (136 if saturated else 1024) * MIB, "metadata_pages": 8192,
            "request_bytes": 8 * MIB, "stage_bytes": 128 * MIB,
            "peer_request_bytes": 64 * MIB, "expose_request_bytes": 80 * MIB,
            "native_seconds": 30, "native_memory_mib": 128, "entries": 8192}
        ev = event()
        origin = scratch / "original-call"
        origin.mkdir()
        if attempt:
            ev["origin_directory"] = str(origin)
        store = S.ControlStore(state, CONFIG, limits, ev, create=True, scratch=scratch)
        self.stores.append(store)
        # Synthetic prerequisite only, with no accepted context or proof record.
        with store.transaction():
            store.exec("fixture", "UPDATE meta SET initialized=1 WHERE id=1")
            store.snapshot("P1", 0)
        raw = S.encode({"client": "local", "request_id": name, "op": op, "args": {}})
        key = store.reserve("local", name, raw)
        if stage:
            lease = store.stage(key, "submit")  # Real charged row, never a native process.
            directory = Path(lease["directory"])
            directory.mkdir(parents=True)
            self.save(directory / "ACTIVE.lock", b"synthetic-stale-stage-marker\n")
        selected = {"client": "local", "request_id": name,
                    "supervisor_receipt": str(origin / "supervisor.json")}
        return store, selected, raw, key, origin

    def close(self, store):
        store.close()
        self.stores.remove(store)

    def reopen(self, store):
        root, limits, scratch = store.root, store.limits, store.scratch
        self.close(store)
        new = S.ControlStore(root, CONFIG, limits, event(), create=False, scratch=scratch)
        self.stores.append(new)
        return new

    def snapshot(self, store):
        def atom(value):
            return {"hex": value.hex()} if type(value) is bytes else value
        return {table: [{key: atom(row[key]) for key in row.keys()} for row in
            store.rows("test_" + table, "SELECT * FROM " + table + " ORDER BY " + order,
                       maximum=128)] for table, order in TABLES.items()}

    def files(self, root):
        rows, total = {}, 0
        if not root.exists():
            return rows
        for number, path in enumerate(root.rglob("*"), 1):
            S.require(number <= 1024, "FIXTURE_ENTRY_BOUND")
            safe(path)
            if path.is_file():
                size = path.stat().st_size
                total += size
                S.require(size <= MIB and total <= 16 * MIB and len(rows) < 256, "FIXTURE_FILE_BOUND")
                raw = S.read(path, MIB)
                rows[path.relative_to(root).as_posix()] = {"bytes": len(raw), "sha256": S.digest(raw)}
        return rows

    def recover(self, fixture, *, receipt=None, directory=None, selected=None, raw=None, mode="recover_ordinary"):
        store, sel, original, _key, origin = fixture
        ev = event()
        try:
            reply = R.recover(store, sel if selected is None else selected,
                original if raw is None else raw, quiescence() if receipt is None else receipt,
                origin if directory is None else directory, ev, mode=mode)
        except Exception as error:
            self.last_event = ev
            raise
        self.last_event = ev
        return reply, ev

    def assert_refusal(self, code, function, *args, **kwargs):
        with self.assertRaises(S.Refusal) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)
        return caught.exception

    def test_owner_envelopes_and_exact_mode_sets(self):
        self.assertEqual(R.RECOVERY_OPERATIONS, {
            "recover_peer": {"peer_find", "peer_acquire", "expose"},
            "recover_ordinary": {"info", "find", "preview", "select_context", "admit", "submit", "publish"}})
        self.assertEqual(R.ORDINARY_INTERRUPTED, S.encode({"status": "REFUSED", "code": "INTERRUPTED_ORDINARY_OPERATION"}))
        selection = {"client": "local", "request_id": "r", "supervisor_receipt": "C:\\synthetic\\supervisor.json"}
        for mode in ("recover_peer", "recover_ordinary"):
            envelope = {"client": "owner", "op": mode, "args": selection}
            self.assertEqual(R.owner_request(S.encode(envelope), ["local"]), selection)
            for field, bad in (("op", "init"), ("op", "recover_all"), ("client", "local")):
                with self.subTest(mode=mode, field=field, bad=bad), self.assertRaises(S.Refusal):
                    R.owner_request(S.encode(dict(envelope, **{field: bad})), ["local"])
            with self.assertRaises(S.Refusal):
                R.owner_request(S.encode(dict(envelope, response={"accepted": True})), ["local"])
        self.notes["scope"] = "Pure worker envelope/mode constants; wrapper/source-cut authentication not exercised"

    def test_evidence_mode_allowlist_and_actual_pin_binding(self):
        # Synthetic receipt identity tests, not a real process/cleanup attestation.
        scratch, state = self.root / "scratch", self.root / "state"
        scratch.mkdir()
        state.mkdir()
        calls = scratch / "calls"
        calls.mkdir()
        config_path = state / "config.json"
        self.save(config_path, S.encode({"synthetic_identity_fixture": True}))
        def pin(path):
            raw = S.read(path, 16 * MIB)
            return {"path": str(Path(path).resolve()), "bytes": len(raw), "sha256": S.digest(raw)}
        pins = [pin(Path(sys.executable)), pin(config_path),
                *[pin(INSTALL / "py" / (name + ".py")) for name in R.SOURCE_NAMES]]
        config = {"config_id": pins[1]["sha256"], "clients": ["local"], "files": {
            name: pin(INSTALL / "py" / (name + ".py"))
            for name in ("checking", "domains", "peer_wire", "peer_service", "peer_node")}}
        domains = SimpleNamespace(install=INSTALL, state=state, scratch=scratch)
        cases = []
        for index, op in enumerate(sorted(R.ORDINARY_OPERATIONS | R.PEER_OPERATIONS)):
            directory = calls / ("call-" + str(index))
            directory.mkdir()
            original = S.encode({"client": "local", "request_id": "request-" + str(index), "op": op, "args": {}})
            command = S.encode({"argv": [str(Path(sys.executable).resolve()), *D.PYTHON_FLAGS,
                str(INSTALL / "py/node.py"), "--config", str(config_path), "--state", str(state),
                "--request", str(directory / "request.json"), "--event", str(directory / "event.json")],
                "cwd": str(INSTALL / "py"), "shell": False, "creationflags": 134217732,
                "environment_override": {"PYTHONDONTWRITEBYTECODE": "1"}})
            self.save(directory / "request.json", original)
            self.save(directory / "command.json", command)
            receipt = {"schema": 1, "name": directory.name, "status": "TRANSPORT_FAILED",
                "native_acceptance": False, "request_sha256": S.digest(original), "pins": pins,
                "bound_pin_count": len(pins), "bound_pin_bytes": sum(row["bytes"] for row in pins),
                "files": {name: {"present": True, "bytes": len(raw), "sha256": S.digest(raw)}
                          for name, raw in (("request.json", original), ("command.json", command))}}
            self.save(directory / "supervisor.json", S.encode(receipt))
            selected = {"client": "local", "request_id": "request-" + str(index),
                        "supervisor_receipt": str(directory / "supervisor.json")}
            for mode, allowed in R.RECOVERY_OPERATIONS.items():
                if op in allowed:
                    observed = event()
                    actual = R.authenticate_evidence(selected, config, config_path, domains, observed, mode=mode)
                    self.assertEqual(actual, (receipt, directory, original))
                    self.assertEqual(observed["authenticated_pin_count"], 12)
                else:
                    code = "RECOVERY_NATIVE_OPERATION_FORBIDDEN" if mode == "recover_peer" else "RECOVERY_ORDINARY_OPERATION_FORBIDDEN"
                    self.assert_refusal(code, R.authenticate_evidence, selected, config, config_path,
                                        domains, event(), mode=mode)
                cases.append({"operation": op, "mode": mode, "permitted": op in allowed})
            raw_owner = S.encode({"client": "owner", "op": "recover_ordinary", "args": selected})
            wrapper_selected, wrapper_pin = M.selected_owner_request(raw_owner, config, domains)
            self.assertEqual(wrapper_selected, selected)
            self.assertEqual(wrapper_pin, pin(directory / "supervisor.json"))
        broken = deepcopy(receipt)
        broken["pins"][2]["sha256"] = "0" * 64
        self.assert_refusal("RECOVERY_ORIGINAL_CUT_CHANGED", R.authenticate_pins,
                            broken, config, config_path, domains, event())
        self.notes.update(cases=cases, pins=pins,
            scope="Synthetic receipt with actual byte pins; no load_config/main/supervisor execution or native claim")

    def test_pending_stage_abort_at_exhaustion_and_replay(self):
        f = self.fixture(saturated=True)
        store, _selected, raw, key, _origin = f
        before, work = self.snapshot(store), self.files(store.root / "work")
        state = store.authorization_state()
        self.assertEqual(state["used"], state["authorized"])
        reply, ev = self.recover(f)
        self.assertEqual(reply, R.ORDINARY_INTERRUPTED)
        expected = deepcopy(before)
        expected["meta"][0]["active"] = None
        expected["requests"][0].update(phase="terminal", response={"hex": reply.hex()})
        self.assertEqual(self.snapshot(store), expected)
        self.assertEqual(self.files(store.root / "work"), work)
        self.assertTrue(ev["transition_committed"])
        self.assertFalse(ev["historical"])
        self.assertEqual(store.prior("local", "node", raw), reply)
        replay, replay_event = self.recover(f, receipt={})
        self.assertEqual(replay, reply)
        self.assertTrue(replay_event["historical"])
        self.assertFalse(replay_event["terminal_write_attempted"])
        self.assertEqual(self.snapshot(store), expected)
        self.notes.update(before=before, after=expected, work_preserved=work, recovery=ev, replay=replay_event)

    def test_peer_no_stage_policy_preserved(self):
        f = self.fixture("peer-staged", op="peer_acquire", stage=True)
        before = self.snapshot(f[0])
        self.assert_refusal("RECOVERY_NATIVE_STAGE_PRESENT", self.recover, f, mode="recover_peer")
        self.assertEqual(self.snapshot(f[0]), before)
        no_stage = self.fixture("peer-free", op="peer_find", stage=False)
        reply, ev = self.recover(no_stage, mode="recover_peer")
        self.assertEqual(reply, R.INTERRUPTED)
        self.assertTrue(ev["transition_committed"])
        self.notes["peer_response"] = S.decode(reply)

    def test_terminal_replay_with_stage_and_unrelated_active_request(self):
        f = self.fixture()
        store = f[0]
        success = b'{ "status": "OK", "synthetic_no_math": true }\n'
        with store.transaction():
            store.terminal(f[3], success)
        second_raw = S.encode({"client": "local", "request_id": "other", "op": "info", "args": {}})
        other = store.reserve("local", "other", second_raw)
        before = self.snapshot(store)
        reply, ev = self.recover(f, receipt={}, directory=self.root / "later-retry")
        self.assertEqual(reply, success)
        self.assertEqual(store.meta()["active"], other)
        self.assertEqual(self.snapshot(store), before)
        self.assertTrue(ev["historical"])
        self.assertFalse(ev["terminal_write_attempted"])
        self.notes.update(response_hex=reply.hex(), replay=ev)

    def test_pending_original_attempt_and_identity_guards(self):
        f = self.fixture()
        before = self.snapshot(f[0])
        self.assert_refusal("RECOVERY_ORIGINAL_ATTEMPT_NOT_BOUND", self.recover, f,
                            directory=self.root / "later-same-bytes-retry")
        self.assert_refusal("RECOVERY_LEDGER_REQUEST_BINDING", self.recover, f, raw=f[2] + b" ")
        self.assert_refusal("RECOVERY_REQUEST_NOT_FOUND", self.recover, f,
                            selected=dict(f[1], client="other"))
        self.assertEqual(self.snapshot(f[0]), before)
        no_attempt = self.fixture("unbound", attempt=False)
        untouched = self.snapshot(no_attempt[0])
        self.assert_refusal("RECOVERY_ORIGINAL_ATTEMPT_NOT_BOUND", self.recover, no_attempt)
        self.assertEqual(self.snapshot(no_attempt[0]), untouched)

    def test_pending_active_and_initialization_guards(self):
        f = self.fixture()
        for active in (None, "a" * 64):
            with f[0].transaction():
                f[0].exec("fixture", "UPDATE meta SET active=? WHERE id=1", (active,))
            before = self.snapshot(f[0])
            self.assert_refusal("RECOVERY_ACTIVE_REQUEST_BINDING", self.recover, f)
            self.assertEqual(self.snapshot(f[0]), before)
        with f[0].transaction():
            f[0].exec("fixture", "UPDATE meta SET initialized=0 WHERE id=1")
        before = self.snapshot(f[0])
        self.assert_refusal("NOT_INITIALIZED", self.recover, f)
        self.assertEqual(self.snapshot(f[0]), before)

    def test_incomplete_quiescence_never_clears_pending(self):
        f = self.fixture()
        before = self.snapshot(f[0])
        bad = []
        for field in ("job_created_before_process", "attach_resume_returned", "direct_child_reaped",
                      "final_active_zero", "job_closed"):
            for value in (False, 1, None):
                bad.append(dict(quiescence(), **{field: value}))
        bad.extend([dict(quiescence(), final_job={"active_processes": 1, "total_processes": 4}),
                    dict(quiescence(), cleanup_errors=["synthetic-unknown"]),
                    dict(quiescence(), evidence_persistence_error="synthetic"),
                    dict(quiescence(), output_record_error="synthetic"),
                    dict(quiescence(), returncode=True)])
        for index, receipt in enumerate(bad):
            with self.subTest(index=index), self.assertRaises(S.Refusal):
                self.recover(f, receipt=receipt)
            self.assertEqual(self.snapshot(f[0]), before)
        self.notes["rejected_synthetic_receipts"] = len(bad)

    def test_terminal_write_failure_retains_pending_without_second_clear(self):
        f = self.fixture()
        store, before = f[0], self.snapshot(f[0])
        original, attempted = store.exec, []
        def fail(name, statement, values=()):
            if name == "terminal":
                attempted.append(name)
                error = sqlite3.OperationalError("synthetic terminal FULL")
                error.sqlite_errorcode = sqlite3.SQLITE_FULL
                raise error
            return original(name, statement, values)
        with patch.object(store, "exec", fail):
            with self.assertRaises(sqlite3.OperationalError) as caught:
                self.recover(f)
        blocked = S.decode(R.blocked(caught.exception, self.last_event))
        self.assertEqual(blocked["status"], "BLOCKED")
        self.assertEqual(blocked["code"], "RECOVERY_PERSISTENCE_UNCERTAIN")
        self.assertEqual(attempted, ["terminal"])
        self.assertFalse(store._uncertain)  # Confirmed rollback; recovery reply is conservative.
        self.assertEqual(self.snapshot(store), before)
        grant = S.encode({"schema": 1, "op": "renew", "grant_id": "not-a-repair", "config": CONFIG,
            "add": {"requests": 1, "stages": 0, "reserved_bytes": 8 * MIB}})
        self.assert_refusal("PENDING_EXECUTION", store.renew, grant, C.parse_grant(grant, CONFIG))
        self.assertEqual(self.snapshot(store), before)
        self.notes.update(injection="synthetic SQLITE_FULL, not physical fill", response=blocked,
                          before=before, after=self.snapshot(store))

    def test_commit_uncertainty_before_and_after_actual_commit(self):
        self.notes["cases"] = []
        for durable in (False, True):
            f = self.fixture("after" if durable else "before")
            store, before = f[0], self.snapshot(f[0])
            original, writes = store.exec, []
            def fail(name, statement, values=()):
                if name in {"terminal", "inactive", "commit"}:
                    writes.append(name)
                if name == "commit":
                    if durable:
                        original(name, statement, values)
                    raise OSError("synthetic COMMIT uncertainty")
                return original(name, statement, values)
            with patch.object(store, "exec", fail):
                error = self.assert_refusal("TRANSACTION_OUTCOME_UNKNOWN", self.recover, f)
            reply = S.decode(R.blocked(error, self.last_event))
            self.assertEqual(reply["code"], "RECOVERY_PERSISTENCE_UNCERTAIN")
            self.assertEqual(writes, ["terminal", "inactive", "commit"])
            self.assertTrue(store._uncertain)
            self.assert_refusal("TRANSACTION_OUTCOME_UNKNOWN", store.terminal_refusal, f[3], R.ORDINARY_INTERRUPTED)
            store = self.reopen(store)
            expected = deepcopy(before)
            if durable:
                expected["meta"][0]["active"] = None
                expected["requests"][0].update(phase="terminal", response={"hex": R.ORDINARY_INTERRUPTED.hex()})
            self.assertEqual(self.snapshot(store), expected)
            retry, retry_event = self.recover((store, *f[1:]))
            self.assertEqual(retry, R.ORDINARY_INTERRUPTED)
            self.assertEqual(retry_event["historical"], durable)
            self.assertEqual(retry_event["transition_committed"], not durable)
            self.notes["cases"].append({"actual_commit_before_error": durable, "response": reply,
                                       "reopened": expected, "retry": retry_event})

    def test_nonempty_sidecar_refused_and_preserved(self):
        f = self.fixture()
        store = f[0]
        state, limits, scratch = store.root, store.limits, store.scratch
        self.close(store)
        journal = state / "control.sqlite3-journal"
        self.save(journal, b"synthetic nonempty sidecar; not a real hot journal\n")
        before = self.files(state / "work")
        db_before = S.digest(S.read(state / "control.sqlite3", MIB))
        self.assert_refusal("UNEXPECTED_SQLITE_AUXILIARY", S.ControlStore,
                            state, CONFIG, limits, event(), create=False, scratch=scratch)
        self.assertEqual(S.digest(S.read(state / "control.sqlite3", MIB)), db_before)
        self.assertEqual(self.files(state / "work"), before)
        self.assertEqual(S.read(journal, MIB), b"synthetic nonempty sidecar; not a real hot journal\n")
        self.notes["scope"] = "No SQLite journal recovery; refused before open, synthetic sidecar retained"

    def tearDown(self):
        errors = []
        for store in list(self.stores):
            try:
                self.close(store)
            except Exception as error:
                errors.append(type(error).__name__ + ":" + str(error)[:256])
        try:
            self.stack.close()
        except Exception as error:
            errors.append(type(error).__name__ + ":" + str(error)[:256])
        files = self.files(self.root)
        report = {"test": self._testMethodName, "synthetic_initialization": True,
            "synthetic_original_quiescence": True, "mocked_supply": True,
            "native_executions": 0, "mathematical_acceptance_claim": False,
            "notes": self.notes, "close_errors": errors, "fixture_files": files}
        self.save(self.root / "report.json", S.encode(report))
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()

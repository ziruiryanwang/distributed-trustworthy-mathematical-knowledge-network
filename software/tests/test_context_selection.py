"""Prospective native-free context contracts; author has not executed this file.

Root-only, separately bounded invocation with -B -E -s -S and an existing
absolute DTMKN_TEST_ROOT outside the software installation. Fixtures are
retained, synthetic ledger metadata, never checked mathematics or supervisor
evidence. No native process, checker or network service may be invoked.
"""
from copy import deepcopy
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

if not (sys.dont_write_bytecode and sys.flags.ignore_environment
        and sys.flags.no_site and sys.flags.no_user_site):
    raise RuntimeError("CONTEXT_TESTS_REQUIRE_PYTHON_B_E_s_S")

INSTALL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(INSTALL))
sys.path.insert(0, str(INSTALL / "py"))

import domains as D
import manage as M
import node as N
import storage as S

for module, relative in ((D, "py/domains.py"), (M, "manage.py"),
                         (N, "py/node.py"), (S, "py/storage.py")):
    if Path(module.__file__).resolve() != INSTALL / relative:
        raise RuntimeError("CONTEXT_TEST_INSTALLED_MODULE_IDENTITY")

MIB = 1048576
TABLES = {"meta": "id", "requests": "key", "records": "handle", "heads": "client",
          "providers": "provider", "snapshots": "handle", "entries": "provider,seq", "stages": "id"}
OMITTED = object()


def event(origin=None):
    value = {"checker_loaded": False, "checker_metrics": {}, "sql_vm_steps": 0,
             "sql_opened": False, "sql_rows": {}, "stages_allocated": 0,
             "historical": False, "fetched_sequences": [], "consumed_sequences": []}
    if origin is not None:
        value["origin_directory"] = str(origin)
    return value


def pin(path):
    path = Path(path).resolve(strict=True)
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": S.digest(raw)}


def observable(value):
    if type(value) is bytes:
        return {"hex": value.hex()}
    if type(value) is dict:
        return {key: observable(item) for key, item in value.items()}
    if type(value) in (list, tuple):
        return [observable(item) for item in value]
    return value


class FixtureCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = os.environ.get("DTMKN_TEST_ROOT")
        if type(parent) is not str or not parent or not Path(parent).is_absolute():
            raise RuntimeError("EXPLICIT_ABSOLUTE_TEST_ROOT_REQUIRED")
        cls.parent = D.absolute_directory(parent, existing=True)
        if cls.parent.is_relative_to(INSTALL) or INSTALL.is_relative_to(cls.parent):
            raise RuntimeError("CONTEXT_TEST_ROOT_MUST_NOT_OVERLAP_INSTALL")

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="context-" + self._testMethodName[5:25] + "-", dir=self.parent))
        self.state, self.scratch, self.runtime = (self.root / name for name in ("state", "scratch", "runtime"))
        (self.runtime / "bin").mkdir(parents=True)
        self.serial = 0
        self.write("fixture-scope.json", S.encode({"test": self.id(), "retained": True,
            "synthetic_metadata_only": True, "native_qualification": False,
            "mathematical_acceptance": False, "supervised_execution_evidence": False}))

    def write(self, name, raw):
        path = self.root / name
        self.assertTrue(path.resolve().is_relative_to(self.root.resolve()))
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(raw)
        return path

    def configuration(self, packages=16, common_count=5):
        value = {"schema": 2, "owner_source_execution": True,
            "domains": {"install": str(INSTALL), "state": str(self.state),
                        "scratch": str(self.scratch), "lean_runtime": str(self.runtime)},
            "clients": ["alice", "bob"], "peers": {}, "offers": [],
            "common": {"packages": [{"unit_fixture_only": True, "index": index,
                "path": str(self.root / "intentionally-missing" / str(index)),
                "manifest_sha256": "0" * 64} for index in range(common_count)]},
            "files": {name: pin(INSTALL / "py" / (name + ".py")) for name in
                      ("checking", "domains", "peer_node", "peer_wire", "peer_service")},
            "limits": {"requests": 128, "stages": 16, "stage_bytes": 128 * MIB,
                "staging_bytes": 4096 * MIB, "native_seconds": 300, "native_memory_mib": 4096,
                "entries": 8192, "request_bytes": 8 * MIB, "source_bytes": 65536,
                "peer_request_bytes": 64 * MIB, "expose_request_bytes": 80 * MIB,
                "canonical_bytes": 64 * MIB, "inprocess_seconds": 120}}
        if packages is not OMITTED:
            value["limits"]["packages"] = packages
        return value

    def config_file(self, value):
        self.serial += 1
        return self.write("configuration-" + str(self.serial) + ".json", S.encode(value))

    def refusal(self, code, function, *args, **kwargs):
        with self.assertRaises(S.Refusal) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)


class ContextPackageLimitTests(FixtureCase):
    def test_shared_helper_accepts_exact_integer_profile(self):
        for common in range(1, 17):
            for cap in range(common, 17):
                with self.subTest(common=common, cap=cap):
                    self.assertEqual(N.context_package_limit(cap, common), cap)
                    self.assertIs(type(N.context_package_limit(cap, common)), int)

    def test_shared_helper_rejects_cap_types_and_bounds(self):
        for cap in (True, False, None, -1, 0, 1, 4, 17, 2 ** 64,
                    5.0, 16.0, 5.5, "5", "16", [], {}):
            with self.subTest(cap=repr(cap)):
                self.refusal("CONFIG_LIMIT:packages", N.context_package_limit, cap, 5)

    def test_shared_helper_rejects_common_count_types_and_bounds(self):
        for common in (True, False, None, -1, 0, 17, 2 ** 64, 5.0, "5", [], {}):
            with self.subTest(common=repr(common)):
                self.refusal("CONFIG_PACKAGES", N.context_package_limit, 16, common)

    def test_load_config_accepts_all_current_caps_and_missing_default(self):
        for cap in (*range(5, 17), OMITTED):
            with self.subTest(cap="omitted" if cap is OMITTED else cap):
                path = self.config_file(self.configuration(cap))
                value = N.load_config(path)
                self.assertEqual(value["limits"].get("packages", 16), 16 if cap is OMITTED else cap)
                self.assertEqual(value["config_id"], S.digest(path.read_bytes()))
                self.assertFalse(self.state.exists())
                self.assertFalse(self.scratch.exists())

    def test_load_config_refuses_invalid_json_cap_representations(self):
        for cap in (True, False, None, -1, 0, 4, 17, 2 ** 64, "5", "16", [], {}):
            with self.subTest(cap=repr(cap)):
                self.refusal("CONFIG_LIMIT:packages", N.load_config, self.config_file(self.configuration(cap)))
        for cap in (5.0, 5.5, 16.0):
            with self.subTest(cap=repr(cap)):
                self.refusal("INVALID_JSON", N.load_config, self.config_file(self.configuration(cap)))
        self.assertFalse(self.state.exists())
        self.assertFalse(self.scratch.exists())

    def test_load_config_uses_actual_common_count(self):
        self.refusal("CONFIG_LIMIT:packages", N.load_config,
                     self.config_file(self.configuration(5, common_count=6)))
        self.assertEqual(N.load_config(self.config_file(self.configuration(6, common_count=6)))["limits"]["packages"], 6)
        for count in (0, 17):
            with self.subTest(common_count=count):
                self.refusal("CONFIG_PACKAGES", N.load_config,
                             self.config_file(self.configuration(16, common_count=count)))

    def args(self, cap=OMITTED):
        value = SimpleNamespace(state=self.state, scratch=self.scratch,
                                lean_runtime=self.runtime, client=["alice"], peer=[])
        if cap is not OMITTED:
            value.context_packages = cap
        return value

    def test_configure_invalid_caps_precede_pin_build_and_directory_creation(self):
        with patch.object(M, "pin", side_effect=AssertionError("PINNING_BEFORE_INVALID_CAP_REFUSAL")) as forbidden:
            for cap in (True, False, None, -1, 0, 1, 4, 17, 2 ** 64,
                        5.0, 16.0, "5", "16", [], {}):
                with self.subTest(cap=repr(cap)):
                    self.refusal("CONFIG_LIMIT:packages", M.configure, self.args(cap))
                    self.assertFalse(self.state.exists())
                    self.assertFalse(self.scratch.exists())
            forbidden.assert_not_called()

    def test_configure_valid_caps_and_default_reach_only_pin_boundary(self):
        class PinBoundaryReached(RuntimeError):
            pass
        for cap in (*range(5, 17), OMITTED):
            with self.subTest(cap="omitted" if cap is OMITTED else cap):
                with patch.object(N, "context_package_limit", wraps=N.context_package_limit) as validate:
                    with patch.object(M, "pin", side_effect=PinBoundaryReached) as boundary:
                        with self.assertRaises(PinBoundaryReached):
                            M.configure(self.args(cap))
                        boundary.assert_called_once()
                    validate.assert_called_once_with(16 if cap is OMITTED else cap, 5)
                self.assertFalse(self.state.exists())
                self.assertFalse(self.scratch.exists())
                self.assertFalse((self.runtime / "bin/lean.exe").exists())


class ContextSelectionTests(FixtureCase):
    def setUp(self):
        super().setUp()
        self.config = N.load_config(self.config_file(self.configuration()))
        self.state.mkdir()
        self.lock = S.owner_lock(self.state)
        self.lock.__enter__()
        self.addCleanup(self.lock.__exit__, None, None, None)
        self.store = S.ControlStore(self.state, self.config["config_id"], self.config["limits"], event(), create=True)
        self.addCleanup(self.store.close)
        with self.store.transaction():
            self.a0 = self.store.put_record("context", "alice", self.context_data("a0"))
            self.a1 = self.store.put_record("context", "alice", self.context_data("a1"))
            self.a2 = self.store.put_record("context", "alice", self.context_data("a2"))
            self.b0 = self.store.put_record("context", "bob", self.context_data("b0"))
            self.store.set_head("alice", self.a0)
            self.store.set_head("bob", self.b0)
            self.store.snapshot("P1", 0)
            descriptor = {"unit_fixture_only": "retained-descriptor-not-mathematics"}
            self.offer = {"descriptor_id": descriptor, "unit_fixture_only": True}
            snapshot, sequence, _ = self.store.append("P1", self.offer)
            self.candidate = self.store.put_record("candidate", "alice", {
                "snapshot": snapshot, "sequence": sequence, "descriptor_id": descriptor})
            self.artifact = self.store.put_record("artifact", "alice", {
                "unit_fixture_only": True, "context": self.a0, "kind": "artifact"})
            self.store.mark_published("P1", sequence, descriptor)
            # Synthetic initialized metadata only. No bootstrap or accepted
            # native context is claimed by this deliberately constructed fixture.
            self.store.exec("fixture_initialized", "UPDATE meta SET initialized=1 WHERE id=1")
        self.guard_check = patch.object(N.Dispatcher, "checking", side_effect=AssertionError("CHECKER_FORBIDDEN"))
        self.guard_peer = patch.object(N.Dispatcher, "peering", side_effect=AssertionError("PEERING_FORBIDDEN"))
        self.guard_stage = patch.object(S.ControlStore, "stage", side_effect=AssertionError("NATIVE_STAGE_FORBIDDEN"))
        self.checker, self.peer, self.stage = (guard.start() for guard in (self.guard_check, self.guard_peer, self.guard_stage))
        for guard in (self.guard_check, self.guard_peer, self.guard_stage):
            self.addCleanup(guard.stop)
        self.addCleanup(self.assert_forbidden_unused)

    def context_data(self, label):
        return {"kind": "context", "unit_fixture_only": True,
            "packages": [{"path": str(self.root / "intentionally-missing" / label), "manifest_sha256": "0" * 64}],
            "description": {"unit_fixture_only": label}, "evidence": []}

    def assert_forbidden_unused(self):
        self.checker.assert_not_called()
        self.peer.assert_not_called()
        self.stage.assert_not_called()
        self.assertFalse((self.state / "work").exists())

    def snapshot(self):
        return {table: [dict(row) for row in self.store.db.execute("SELECT * FROM " + table + " ORDER BY " + order)]
                for table, order in TABLES.items()}

    def raw(self, identity, current=None, selected=None, client="alice"):
        return S.encode({"client": client, "request_id": identity, "op": "select_context",
                         "args": {"context": current or self.a0, "selected": selected or self.a1}})

    def dispatch(self, raw):
        self.serial += 1
        prefix = "invocation-" + str(self.serial)
        self.write(prefix + "-request.json", raw)
        observed = event(self.root / "fixture-origins" / prefix)
        self.store.event = observed
        before = self.snapshot()
        dispatcher, response, raised = None, None, None
        try:
            parsed = N.request(raw, self.config["clients"])
            dispatcher = N.Dispatcher(self.config, self.store, observed)
            response = dispatcher.execute(parsed, raw)
            self.write(prefix + "-response.json", response)
            return response, observed, before, self.snapshot()
        except S.Refusal as error:
            raised = error.code
            raise
        finally:
            self.write(prefix + "-observation.json", S.encode(observable({
                "scope": "synthetic-unit-metadata-not-supervisor-or-math-evidence",
                "before": before, "after": self.snapshot(), "event": observed,
                "response": response, "raised_refusal": raised})))
            if dispatcher is not None:
                self.assertIsNone(dispatcher.math)
                self.assertIsNone(dispatcher.math_module)
                self.assertIsNone(dispatcher.peer)
            self.assertIs(observed["checker_loaded"], False)
            self.assertEqual(observed["stages_allocated"], 0)
            self.assertEqual(observed["checker_metrics"], {})
            self.assert_forbidden_unused()

    def assert_fresh_delta(self, raw, response, observed, before, after, selected=None):
        request = S.decode(raw)
        key = S.digest(S.encode([request["client"], request["request_id"]]))
        expected = deepcopy(before)
        expected["meta"][0]["requests"] += 1
        expected["meta"][0]["charged"] += self.config["limits"]["request_bytes"]
        expected["meta"][0]["active"] = None
        expected["requests"].append({"key": key, "client": request["client"],
            "request_id": request["request_id"], "raw": raw, "phase": "terminal", "response": response})
        expected["requests"].sort(key=lambda row: row["key"])
        marker_raw = S.encode({"config": self.config["config_id"], "kind": "attempt", "client": "owner",
            "data": {"request": key, "call_directory": observed["origin_directory"]}})
        expected["records"].append({"handle": "attempt:" + S.digest(marker_raw), "kind": "attempt",
                                    "client": "owner", "raw": marker_raw})
        expected["records"].sort(key=lambda row: row["handle"])
        if selected is not None:
            for row in expected["heads"]:
                if row["client"] == request["client"]:
                    row["context"] = selected
        self.assertEqual(after, expected)
        self.assertEqual(observed["reserved_request_bytes"], self.config["limits"]["request_bytes"])
        self.assertIs(observed["historical"], False)

    def assert_success(self, raw, current, selected):
        response, observed, before, after = self.dispatch(raw)
        expected = {"status": "OK", "client": "alice", "previous_context": current,
            "context": selected, "changed": current != selected, "mathematicalAcceptance": False,
            "context_record_authenticated": True, "live_context_status": "UNCHECKED", "native_stages": 0}
        self.assertEqual(response, S.encode(expected))
        self.assert_fresh_delta(raw, response, observed, before, after, selected)
        return response

    def assert_terminal_refusal(self, raw, code):
        response, observed, before, after = self.dispatch(raw)
        value = S.decode(response)
        self.assertEqual((value["status"], value["code"]), ("REFUSED", code))
        self.assertNotIn("accepted", value)
        self.assert_fresh_delta(raw, response, observed, before, after)
        return response

    def test_success_exact_response_full_ledger_and_no_authority(self):
        self.assert_success(self.raw("select"), self.a0, self.a1)

    def test_current_head_noop_is_successful_and_charged(self):
        self.assert_success(self.raw("noop", selected=self.a0), self.a0, self.a0)

    def test_metadata_selection_does_not_require_live_dependency_files(self):
        self.assertFalse((self.root / "intentionally-missing").exists())
        self.assert_success(self.raw("unchecked"), self.a0, self.a1)
        self.assertFalse((self.root / "intentionally-missing").exists())

    def test_expected_and_selected_context_require_ownership_kind_and_identity(self):
        cases = (("current-foreign", self.b0, self.a1, "WRONG_CLIENT_HANDLE"),
                 ("selected-foreign", self.a0, self.b0, "WRONG_CLIENT_HANDLE"),
                 ("current-kind", self.artifact, self.a1, "HANDLE_KIND"),
                 ("selected-artifact", self.a0, self.artifact, "HANDLE_KIND"),
                 ("selected-candidate", self.a0, self.candidate, "HANDLE_KIND"),
                 ("current-unknown", "context:" + "1" * 64, self.a1, "UNKNOWN_HANDLE"),
                 ("selected-unknown", self.a0, "context:" + "1" * 64, "UNKNOWN_HANDLE"))
        for identity, current, selected, code in cases:
            with self.subTest(identity=identity):
                self.assert_terminal_refusal(self.raw(identity, current, selected), code)

    def test_stale_expected_head_refuses_after_normal_reservation(self):
        self.assert_terminal_refusal(self.raw("stale", current=self.a2), "STALE_CONTEXT")

    def test_malformed_arguments_refuse_without_pointer_change(self):
        for index, arguments in enumerate(({}, {"context": self.a0}, {"selected": self.a1},
                {"context": self.a0, "selected": self.a1, "extra": True})):
            raw = S.encode({"client": "alice", "request_id": "arguments-" + str(index),
                            "op": "select_context", "args": arguments})
            self.assert_terminal_refusal(raw, "INVALID_FIELDS")

    def test_parser_owner_and_argument_type_refuse_before_reservation(self):
        for client, arguments, code in (("owner", {}, "CLIENT_OPERATION_SCOPE"),
                                      ("unknown", {}, "UNKNOWN_CLIENT"),
                                      ("alice", [], "INVALID_ARGUMENTS")):
            before = self.snapshot()
            raw = S.encode({"client": client, "request_id": "parser", "op": "select_context", "args": arguments})
            self.refusal(code, self.dispatch, raw)
            self.assertEqual(self.snapshot(), before)

    def test_exact_terminal_replay_after_later_head_change_never_reselects(self):
        first = self.raw("first")
        original = self.assert_success(first, self.a0, self.a1)
        self.assert_success(self.raw("later", self.a1, self.a2), self.a1, self.a2)
        response, observed, before, after = self.dispatch(first)
        self.assertEqual(response, original)
        self.assertEqual(after, before)
        self.assertEqual(self.store.head("alice"), self.a2)
        self.assertIs(observed["historical"], True)
        self.assertNotIn("reserved_request_bytes", observed)

    def test_same_request_id_different_bytes_conflict_without_new_charge(self):
        original = self.raw("original")
        self.assert_success(original, self.a0, self.a1)
        for conflicting in (self.raw("original", self.a1, self.a2), original + b" "):
            before = self.snapshot()
            self.refusal("REQUEST_ID_CONFLICT", self.dispatch, conflicting)
            self.assertEqual(self.snapshot(), before)

    def test_content_handle_aba_allows_unexecuted_request_after_return(self):
        deferred = self.raw("unexecuted-before-aba", self.a0, self.a2)
        self.assert_success(self.raw("aba-away", self.a0, self.a1), self.a0, self.a1)
        self.assert_success(self.raw("aba-return", self.a1, self.a0), self.a1, self.a0)
        self.assert_success(deferred, self.a0, self.a2)

    def test_refusal_replay_remains_exact_after_head_later_matches(self):
        refused_raw = self.raw("initially-stale", self.a2, self.a1)
        refused = self.assert_terminal_refusal(refused_raw, "STALE_CONTEXT")
        self.assert_success(self.raw("later-match", self.a0, self.a2), self.a0, self.a2)
        response, observed, before, after = self.dispatch(refused_raw)
        self.assertEqual(response, refused)
        self.assertEqual(after, before)
        self.assertEqual(self.store.head("alice"), self.a2)
        self.assertIs(observed["historical"], True)

    def test_pending_retry_remains_blocked_without_new_reservation(self):
        raw = self.raw("synthetic-pending")
        self.store.event = event(self.root / "fixture-origins" / "synthetic-pending")
        key = self.store.reserve("alice", "synthetic-pending", raw)
        before = self.snapshot()
        self.refusal("PENDING_EXECUTION", self.dispatch, raw)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.store.meta()["active"], key)

    def prepared(self, identity):
        raw = self.raw(identity)
        observed = event(self.root / "fixture-origins" / identity)
        self.store.event = observed
        parsed = N.request(raw, self.config["clients"])
        dispatcher = N.Dispatcher(self.config, self.store, observed)
        dispatcher.operation = "select_context"
        dispatcher.key = self.store.reserve("alice", identity, raw)
        return dispatcher, parsed, dispatcher.prepare(parsed)

    def test_commit_rechecks_head_after_intervening_pointer_change(self):
        dispatcher, parsed, prepared = self.prepared("prepared-stale")
        with self.store.transaction():
            self.store.set_head("alice", self.a2)
        before = self.snapshot()
        with self.assertRaises(S.Refusal) as caught:
            with self.store.transaction():
                dispatcher.commit_operation(parsed, prepared)
        self.assertEqual(caught.exception.code, "STALE_CONTEXT")
        self.assertEqual(self.snapshot(), before)

    def commit_changed_record(self, handle, identity):
        dispatcher, parsed, prepared = self.prepared(identity)
        with self.store.transaction():
            self.store.exec("fixture_corrupt_record", "UPDATE records SET raw=? WHERE handle=?",
                            (S.encode({"unit_fixture_only": "deliberately-invalidated-binding"}), handle))
        before = self.snapshot()
        with self.assertRaises(S.Refusal) as caught:
            with self.store.transaction():
                dispatcher.commit_operation(parsed, prepared)
        self.assertEqual(caught.exception.code, "RECORD_BINDING")
        self.assertEqual(self.snapshot(), before)

    def test_commit_reauthenticates_expected_context_record(self):
        self.commit_changed_record(self.a0, "changed-current")

    def test_commit_reauthenticates_selected_context_record(self):
        self.commit_changed_record(self.a1, "changed-selected")

    def test_head_and_terminal_commit_roll_back_together(self):
        ordinary_terminal = self.store.terminal
        calls = []
        def first_terminal_fails(key, response):
            calls.append((key, response))
            if len(calls) == 1:
                raise S.Refusal("FIXTURE_TERMINAL_FAILURE")
            return ordinary_terminal(key, response)
        with patch.object(self.store, "terminal", side_effect=first_terminal_fails):
            self.assert_terminal_refusal(self.raw("atomic-refusal"), "FIXTURE_TERMINAL_FAILURE")
        self.assertEqual(len(calls), 2)
        self.assertEqual(self.store.head("alice"), self.a0)


if __name__ == "__main__":
    unittest.main()

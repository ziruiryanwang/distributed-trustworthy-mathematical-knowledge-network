"""Owner-local contract tests; no native stages or mathematical acceptance.

Root executes only through a separately reviewed, bounded owner-test worker.
Every test fixture is retained below the explicit existing DTMKN_TEST_ROOT.
Do not add this module to the frozen transport-only discovery pattern.
"""
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest

if not (sys.dont_write_bytecode and sys.flags.ignore_environment
        and sys.flags.no_user_site and sys.flags.no_site):
    raise RuntimeError("OWNER_TESTS_REQUIRE_PYTHON_B_E_s_S")

INSTALL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(INSTALL))
sys.path.insert(0, str(INSTALL / "py"))

import build as B
import domains as D
import manage as M
from storage import Refusal, decode


class OwnerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = os.environ.get("DTMKN_TEST_ROOT")
        if not isinstance(parent, str) or not parent or not Path(parent).is_absolute():
            raise RuntimeError("EXPLICIT_ABSOLUTE_TEST_ROOT_REQUIRED")
        cls.test_parent = D.absolute_directory(parent, existing=True)

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(
            prefix="owner-" + self._testMethodName[5:29] + "-", dir=self.test_parent))
        self.serial = 0
        self.write_fixture(self.root / "test-case.json", json.dumps({
            "test": self._testMethodName, "retained": True,
            "scope": "owner-contracts-not-mathematical-acceptance",
        }, sort_keys=True).encode("utf-8") + b"\n")
        # These sibling fixture domains are not the product's real install.
        # No source, .olean, build receipt or acceptance record is manufactured.
        self.install = self.root / "install"
        self.runtime = self.root / "runtime"
        self.state = self.root / "state"
        self.scratch = self.root / "scratch"
        (self.install / "py").mkdir(parents=True)
        (self.runtime / "bin").mkdir(parents=True)
        self.record = {"install": str(self.install), "lean_runtime": str(self.runtime),
                       "state": str(self.state), "scratch": str(self.scratch)}

    def write_fixture(self, path, raw):
        path = Path(path)
        self.assertTrue(path.is_absolute())
        self.assertTrue(path.resolve().is_relative_to(self.root.resolve()))
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(raw)
        return path

    def record_fixture(self, raw):
        self.serial += 1
        return self.write_fixture(self.root / ("record-" + str(self.serial) + ".json"), raw)

    def expect_value_error(self, code, function, *args, **kwargs):
        with self.assertRaises(ValueError) as captured:
            function(*args, **kwargs)
        self.assertEqual(str(captured.exception), code)

    def expect_refusal(self, code, function, *args, **kwargs):
        with self.assertRaises(Refusal) as captured:
            function(*args, **kwargs)
        self.assertEqual(captured.exception.code, code)

    def policy(self, **changes):
        return D.Domains.from_record(dict(self.record, **changes))

    def test_isolated_python_profile(self):
        self.assertEqual(D.PYTHON_FLAGS, ["-B", "-E", "-s", "-S"])
        self.assertIsNone(D.require_python_profile())

    def test_exact_domain_fields_and_integer_schema(self):
        for record in (None, [], {}, dict(self.record, extra="unused"),
                       {key: value for key, value in self.record.items() if key != "state"}):
            with self.subTest(record=record):
                self.expect_value_error("DOMAIN_FIELDS", D.Domains.from_record, record)
        for schema in (True, False, 1, 3, 2.0, "2", None):
            with self.subTest(schema=schema):
                self.expect_value_error("CONFIG_DOMAIN_SCHEMA", D.Domains.from_config,
                                        {"schema": schema, "domains": self.record})
        self.assertEqual(D.Domains.from_config({"schema": 2, "domains": self.record}).as_dict(),
                         self.policy().as_dict())

    def test_domain_construction_does_not_create_writable_paths(self):
        policy = self.policy()
        expected = {key: str(Path(value).resolve()) for key, value in self.record.items()}
        self.assertEqual(policy.as_dict(), expected)
        self.assertEqual(list(policy.as_dict()), sorted(D.DOMAIN_KEYS))
        self.assertFalse(self.state.exists())
        self.assertFalse(self.scratch.exists())
        missing_py = self.root / "install-without-py"
        missing_py.mkdir()
        self.expect_value_error("INSTALL_PY_DIRECTORY_REQUIRED", self.policy, install=str(missing_py))

    def test_state_scratch_overlap_refused(self):
        for changes in ({"scratch": str(self.state)},
                        {"scratch": str(self.state / "nested")},
                        {"state": str(self.scratch / "nested")}):
            with self.subTest(changes=changes):
                self.expect_value_error("STATE_SCRATCH_OVERLAP", self.policy, **changes)

    def test_writable_immutable_overlap_refused(self):
        for writable in ("state", "scratch"):
            for immutable in (self.install, self.runtime):
                for path in (immutable, immutable / "nested"):
                    with self.subTest(writable=writable, path=str(path)):
                        self.expect_value_error("WRITABLE_IMMUTABLE_DOMAIN_OVERLAP", self.policy,
                                                **{writable: str(path)})
        container = self.root / "immutable-container"
        contained_install = container / "install"
        (contained_install / "py").mkdir(parents=True)
        self.expect_value_error("WRITABLE_IMMUTABLE_DOMAIN_OVERLAP", self.policy,
                                install=str(contained_install), state=str(container))

    def test_runtime_nesting_is_directional(self):
        nested = self.install / "runtime"
        nested.mkdir()
        self.assertEqual(self.policy(lean_runtime=str(nested)).lean_runtime, nested.resolve())
        for path in (self.install, self.root):
            with self.subTest(path=str(path)):
                self.expect_value_error("RUNTIME_MUST_NOT_CONTAIN_INSTALL", self.policy,
                                        lean_runtime=str(path))

    def test_domain_path_spelling_and_file_refusals(self):
        for value in (None, 1, "", "x" * 32768):
            with self.subTest(value_type=type(value).__name__):
                self.expect_value_error("DOMAIN_PATH_TYPE", D.absolute_directory,
                                        value, existing=False)
        self.expect_value_error("DOMAIN_ABSOLUTE_PATH_REQUIRED", D.absolute_directory,
                                "relative-domain", existing=False)
        self.expect_value_error("DOMAIN_ROOT_FORBIDDEN", D.absolute_directory,
                                self.root.anchor, existing=False)
        # Path normalizes '.' before validation; do not assert it remains visible.
        for component in ("bad.", "bad ", "bad:stream", "CON", ".."):
            with self.subTest(component=component):
                self.expect_value_error("DOMAIN_PATH_COMPONENT", D.absolute_directory,
                                        str(self.root / component), existing=False)
        ordinary_file = self.write_fixture(self.root / "not-a-directory", b"path fixture\n")
        self.expect_value_error("DOMAIN_NOT_DIRECTORY", D.absolute_directory,
                                str(ordinary_file), existing=True)

    def test_state_binding_is_exact(self):
        policy = self.policy()
        self.assertEqual(policy.require_state(self.state), self.state.resolve())
        for path in (self.scratch, self.state / "child", self.root / "state-prefix", Path("state")):
            with self.subTest(path=str(path)):
                self.expect_value_error("CONFIG_STATE_PATH_MISMATCH", policy.require_state, path)

    def test_read_paths_must_exist_inside_a_domain(self):
        policy = self.policy()
        for directory in (self.install, self.runtime, self.state, self.scratch):
            path = self.write_fixture(directory / "read-marker.txt", b"read marker\n")
            with self.subTest(path=str(path)):
                self.assertEqual(policy.require_read(path), path.resolve())
                self.assertEqual(policy.require_read(directory), directory.resolve())
        outsider = self.write_fixture(self.root / "state-prefix" / "outside.txt", b"outside domains\n")
        self.expect_value_error("READ_DOMAIN", policy.require_read, outsider)
        self.expect_value_error("READ_ABSOLUTE_PATH_REQUIRED", policy.require_read, "relative.txt")
        with self.assertRaises(FileNotFoundError):
            policy.require_read(self.state / "missing.txt")

    def test_work_and_write_are_strict_selected_descendants(self):
        policy = self.policy()
        for method in (policy.require_work, policy.require_write):
            for path in (self.state / "work" / "request-a", self.scratch / "request-b"):
                with self.subTest(method=method.__name__, path=str(path)):
                    self.assertEqual(method(path), path.resolve())
            for path in (self.state, self.state / "work", self.scratch,
                         self.state / "workspace" / "request", self.root / "scratch-prefix" / "request",
                         self.install / "request", self.runtime / "request"):
                with self.subTest(method=method.__name__, path=str(path)):
                    self.expect_value_error("SELECTED_WORK_DOMAIN", method, path)
            self.expect_value_error("WORK_ABSOLUTE_PATH_REQUIRED", method, "relative-work")
        self.assertFalse(self.state.exists())
        self.assertFalse(self.scratch.exists())

    def test_stage_stays_below_its_selected_request(self):
        policy = self.policy()
        selected = self.scratch / "request-a"
        stage = selected / "stage-a"
        self.assertEqual(policy.require_stage(stage, selected), stage.resolve())
        for path in (selected, self.scratch / "request-b" / "stage-a",
                     self.state / "work" / "request-a" / "stage-a"):
            with self.subTest(path=str(path)):
                self.expect_value_error("SELECTED_REQUEST_STAGE_DOMAIN", policy.require_stage,
                                        path, selected)
        self.expect_value_error("SELECTED_WORK_DOMAIN", policy.require_stage, stage, self.scratch)

    def test_package_paths_have_a_narrower_read_policy(self):
        policy = self.policy()
        for path in (self.install / "assets" / "package", self.state / "package", self.scratch / "package"):
            path.mkdir(parents=True)
            with self.subTest(path=str(path)):
                self.assertEqual(policy.require_package(path), path.resolve())
        file_path = self.write_fixture(self.install / "assets" / "not-a-package", b"file only\n")
        for path in (self.install, self.install / "py", self.runtime, file_path):
            with self.subTest(path=str(path)):
                self.expect_value_error("CANONICAL_PACKAGE_DOMAIN", policy.require_package, path)
        outsider = self.root / "outside-package"
        outsider.mkdir()
        self.expect_value_error("READ_DOMAIN", policy.require_package, outsider)

    def test_lean_selection_is_an_exact_path_not_native_evidence(self):
        policy = self.policy()
        # This inert text marker tests only path selection. Never execute it.
        marker = b"INERT OWNER TEST PATH MARKER; NOT A LEAN EXECUTABLE\n"
        selected = self.write_fixture(self.runtime / "bin" / "lean.exe", marker)
        self.assertEqual(policy.require_lean(selected), selected.resolve())
        for path in (self.write_fixture(self.runtime / "bin" / "other.exe", marker),
                     self.write_fixture(self.install / "lean.exe", marker),
                     self.write_fixture(self.scratch / "lean.exe", marker), self.runtime / "bin"):
            with self.subTest(path=str(path)):
                self.expect_value_error("EXACT_LEAN_RUNTIME_EXECUTABLE", policy.require_lean, path)

    def test_record_floats_are_finite_and_not_public_request_numbers(self):
        raw = b'{"elapsed":0.125,"nested":{"cpu":1.5e2},"tiny":1e-400,"count":3}\n'
        value = B.read_record(self.record_fixture(raw))
        self.assertEqual(value, {"elapsed": 0.125, "nested": {"cpu": 150.0}, "tiny": 0.0, "count": 3})
        self.assertIs(type(value["elapsed"]), float)
        self.expect_refusal("INVALID_JSON", decode, raw)

    def test_record_duplicate_keys_are_rejected_at_all_levels(self):
        for raw in (b'{"x":1,"x":2}', b'{"outer":{"x":1,"x":2}}', b'[{"x":1,"x":2}]'):
            with self.subTest(raw=raw):
                self.expect_refusal("DUPLICATE_RECORD_KEY", B.read_record, self.record_fixture(raw))

    def test_record_nonfinite_literals_and_float_overflow_are_rejected(self):
        for token in (b"NaN", b"Infinity", b"-Infinity"):
            with self.subTest(token=token):
                self.expect_value_error("NONFINITE_RECORD_NUMBER", B.read_record,
                                        self.record_fixture(b'{"timing":' + token + b"}"))
        for token in (b"1e400", b"-1e400", b"1.7976931348623159e308"):
            with self.subTest(token=token):
                self.expect_refusal("NONFINITE_RECORD_NUMBER", B.read_record,
                                    self.record_fixture(b'{"timing":' + token + b"}"))

    def test_record_size_boundary_and_json_framing(self):
        at_limit = b"0" + b" " * (B.MIB - 1)
        self.assertEqual(B.read_record(self.record_fixture(at_limit)), 0)
        self.expect_refusal("INPUT_LIMIT", B.read_record, self.record_fixture(at_limit + b" "))
        for raw in (b"", b"{", b"{}{}", b"{} trailing"):
            with self.subTest(raw=raw):
                with self.assertRaises(json.JSONDecodeError):
                    B.read_record(self.record_fixture(raw))

    def test_configure_invalid_clients_precedes_path_creation(self):
        # Only hashable scalar client entries: argparse's real CLI produces strings.
        # Empty client input selects ['local']; it is not an invalid-input case.
        cases = (["owner"], ["a", "a"], ["bad/name"], [""], ["x" * 65],
                 [7], [True], ["client-" + str(number) for number in range(17)])
        for clients in cases:
            with self.subTest(clients=clients):
                args = SimpleNamespace(state=self.state, scratch=self.scratch,
                                       lean_runtime=self.runtime, client=clients)
                self.expect_refusal("CONFIG_CLIENTS", M.configure, args)
                self.assertFalse(self.state.exists())
                self.assertFalse(self.scratch.exists())

    def test_configure_existing_paths_refuse_without_touching_sibling(self):
        for existing_name in ("state", "scratch"):
            with self.subTest(existing=existing_name):
                selected = self.root / ("existing-" + existing_name)
                state, scratch = selected / "state", selected / "scratch"
                existing = state if existing_name == "state" else scratch
                sibling = scratch if existing_name == "state" else state
                marker = self.write_fixture(existing / "preserve.txt", b"preserve existing owner data\n")
                args = SimpleNamespace(state=state, scratch=scratch,
                                       lean_runtime=self.runtime, client=["local"])
                self.expect_refusal("FRESH_STATE_AND_SCRATCH_REQUIRED", M.configure, args)
                self.assertFalse(sibling.exists())
                self.assertEqual(marker.read_bytes(), b"preserve existing owner data\n")
                self.assertEqual(sorted(path.name for path in existing.iterdir()), ["preserve.txt"])

    def test_build_existing_work_refuses_before_native_work(self):
        work = self.root / "existing-build-work"
        marker = self.write_fixture(work / "preserve.txt", b"preserve existing build work\n")
        # This runtime has no executable, so a preflight regression cannot run Lean.
        self.assertFalse((self.runtime / "bin" / "lean.exe").exists())
        args = SimpleNamespace(work=work, lean_runtime=self.runtime)
        self.expect_refusal("FRESH_BUILD_REQUIRED", B.build, args)
        self.assertEqual(marker.read_bytes(), b"preserve existing build work\n")
        self.assertEqual(sorted(path.name for path in work.iterdir()), ["preserve.txt"])


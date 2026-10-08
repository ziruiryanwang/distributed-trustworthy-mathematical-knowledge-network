"""Twelve native-free request-builder contracts; retained inert fixtures only.

Root alone runs this through the reviewed bounded test runner. No node imports,
Lean, SQL, subprocesses, network calls, temporary-directory cleanup or acceptance.
"""
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

if not (sys.dont_write_bytecode and sys.flags.ignore_environment
        and sys.flags.no_user_site and sys.flags.no_site):
    raise RuntimeError("PYTHON_B_E_s_S_REQUIRED")
SOURCE = Path(__file__).resolve().parents[1]
BUILDER = SOURCE / "make_request.py"
if (BUILDER.stat().st_size != 6178 or hashlib.sha256(BUILDER.read_bytes()).hexdigest()
        != "0e5eb63c95f6277e7ebb73ac7cc0b210c3a755687bfab3e1e0292cddd9d88719"):
    raise RuntimeError("REVIEWED_BUILDER_PIN")
spec = importlib.util.spec_from_file_location("request_builder_under_test", BUILDER)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
if Path(M.__file__).resolve() != BUILDER:
    raise RuntimeError("BUILDER_MODULE_ORIGIN")


class MakeRequestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        value = os.environ.get("DTMKN_TEST_ROOT")
        if not value or not Path(value).is_absolute():
            raise RuntimeError("EXPLICIT_ABSOLUTE_TEST_ROOT_REQUIRED")
        parent = Path(value)
        for current in (parent, *parent.parents):
            info = current.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                raise RuntimeError("TEST_REPARSE_PATH")
        if not parent.is_dir() or parent.is_relative_to(SOURCE) or SOURCE.is_relative_to(parent):
            raise RuntimeError("EXTERNAL_EXISTING_TEST_ROOT_REQUIRED")
        cls.parent = parent

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="request-" + self._testMethodName[5:22] + "-", dir=self.parent))
        self.serial = 0
        self.fixture("case.json", json.dumps({"test": self._testMethodName, "retained": True,
                                             "scope": "request-serialization-not-acceptance"}).encode())

    def fixture(self, name, raw):
        path = self.root / name
        self.assertTrue(path.resolve().is_relative_to(self.root.resolve()))
        with path.open("xb") as stream:
            stream.write(raw)
        return path

    def call(self, operation, extra=(), *, output=None, client="local", request_id=None):
        self.serial += 1
        output = output if output is not None else self.root / f"request-{self.serial:02d}.json"
        argv = [operation, "--client", client, "--request-id", request_id or f"request-{self.serial:02d}",
                "--output", str(output), *map(str, extra)]
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                code = M.main(argv)
            except SystemExit as error:
                code = error.code
        self.fixture(f"call-{self.serial:02d}.json", json.dumps({"argv": argv, "exit_code": code}).encode())
        self.fixture(f"call-{self.serial:02d}.stdout", stdout.getvalue().encode())
        self.fixture(f"call-{self.serial:02d}.stderr", stderr.getvalue().encode())
        return code, Path(output), stdout.getvalue(), stderr.getvalue()

    def submit(self, source, **kwargs):
        return self.call("submit", ("--context", "context:" + "c" * 64, "--source-file", source,
                                    "--root", "Example.Result"), **kwargs)

    def failure(self, result, code=None):
        status, path, _, error = result
        self.assertNotEqual(status, 0)
        self.assertFalse(path.exists())
        if code is not None:
            self.assertIn(code, error)

    def test_01_source_bytes_and_receipt_preserved(self):
        raw = '-- inert λ «name» "quoted" \\ text\r\n-- second line\n'.encode("utf-8")
        source = self.fixture("source.lean", raw)
        status, path, out, error = self.submit(source)
        self.assertEqual((status, error), (0, ""))
        request = json.loads(path.read_bytes())
        self.assertEqual(set(request), {"client", "request_id", "op", "args"})
        self.assertEqual(request["args"]["source"].encode("utf-8"), raw)
        self.assertEqual(request["args"]["root"], "Example.Result")
        receipt = json.loads(out)
        self.assertEqual(receipt["status"], "REQUEST_FILE_CREATED_NOT_SENT")
        self.assertIs(receipt["sent"], False)
        self.assertEqual(receipt["source"]["sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(receipt["request"]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertFalse(path.read_bytes().startswith(b"\xef\xbb\xbf"))

    def test_02_ordinary_operation_shapes_and_exact_handles(self):
        cases = [("info", (), {}),
                 ("publish", ("--artifact", "artifact:" + "a" * 64, "--snapshot", "snapshot:" + "b" * 64),
                  {"artifact": "artifact:" + "a" * 64, "snapshot": "snapshot:" + "b" * 64}),
                 ("peer-find", ("--peer", "peer_name-1"), {"peer": "peer_name-1"}),
                 ("peer-acquire", ("--remote", "remote:" + "d" * 64), {"remote": "remote:" + "d" * 64}),
                 ("admit", ("--context", "context:" + "c" * 64, "--candidate", "candidate:" + "e" * 64),
                  {"context": "context:" + "c" * 64, "selected": ["candidate:" + "e" * 64]})]
        for operation, args, expected in cases:
            with self.subTest(operation=operation):
                status, path, _, _ = self.call(operation, args)
                self.assertEqual(status, 0)
                request = json.loads(path.read_bytes())
                self.assertEqual(request["op"], operation.replace("-", "_"))
                self.assertEqual(request["args"], expected)

    def test_03_exclusive_create_never_overwrites(self):
        original = b"unchanged owner bytes\r\n"
        output = self.fixture("occupied.json", original)
        result = self.call("info", output=output)
        self.assertEqual(result[0], 1)
        self.assertIn("OUTPUT_ALREADY_EXISTS", result[3])
        self.assertEqual(output.read_bytes(), original)

    def test_04_bom_and_invalid_utf8_rejected(self):
        for number, raw in enumerate((b"\xef\xbb\xbf-- text\n", b"\xff\xfe")):
            with self.subTest(number=number):
                self.failure(self.submit(self.fixture(f"encoding-{number}.lean", raw)))

    def test_05_source_byte_bounds(self):
        self.failure(self.submit(self.fixture("empty.lean", b"")), "SOURCE_BYTE_LIMIT")
        self.failure(self.submit(self.fixture("large.lean", b"x" * 65537)), "SOURCE_BYTE_LIMIT")
        result = self.submit(self.fixture("ceiling.lean", b"x" * 65536))
        self.assertEqual(result[0], 0)
        self.assertEqual(len(json.loads(result[1].read_bytes())["args"]["source"].encode()), 65536)

    def test_06_encoded_request_bound_is_independent(self):
        self.failure(self.submit(self.fixture("escaped.lean", b"\n" * 65536)), "REQUEST_BYTE_LIMIT")

    def test_07_labels_and_declaration_root(self):
        self.failure(self.call("info", client="owner"), "LOCAL_CLIENT_LABEL_REQUIRED")
        self.failure(self.call("info", client="local user"), "LOCAL_CLIENT_LABEL_REQUIRED")
        self.failure(self.call("info", request_id="x" * 65), "REQUEST_ID_REQUIRED")
        self.failure(self.call("info", request_id="bad/id"), "REQUEST_ID_REQUIRED")
        source = self.fixture("root.lean", b"-- inert\n")
        for root in ("Bad..Root", "Bad-root", "x" * 257):
            self.failure(self.call("submit", ("--context", "context:x", "--source-file", source,
                                               "--root", root)), "DECLARATION_ROOT_REQUIRED")

    def test_08_candidate_count_duplicates_and_order(self):
        base = ["--context", "context:x"]
        self.failure(self.call("admit", base))
        self.failure(self.call("admit", [*base, "--candidate", "candidate:x", "--candidate", "candidate:x"]))
        selected = [f"candidate:{n}" for n in range(5)]
        all_args = [value for item in selected for value in ("--candidate", item)]
        self.failure(self.call("admit", [*base, *all_args]))
        result = self.call("admit", [*base, *all_args[:8]])
        self.assertEqual(result[0], 0)
        self.assertEqual(json.loads(result[1].read_bytes())["args"]["selected"], selected[:4])

    def test_09_relative_and_traversal_paths_refused(self):
        self.failure(self.call("info", output="relative-request.json"), "ABSOLUTE_LOCAL_NONROOT_PATH_REQUIRED")
        self.failure(self.submit("relative-source.lean"), "ABSOLUTE_LOCAL_NONROOT_PATH_REQUIRED")
        self.failure(self.call("info", output=self.root / ".." / "escape.json"), "ABSOLUTE_LOCAL_NONROOT_PATH_REQUIRED")

    def test_10_reparse_ancestor_refused_with_explicit_mock(self):
        original = Path.lstat
        def substituted(path, *args, **kwargs):
            info = original(path, *args, **kwargs)
            if path == self.root:
                return SimpleNamespace(st_mode=info.st_mode, st_file_attributes=0x400)
            return info
        with patch.object(Path, "lstat", substituted):
            result = self.call("info")
        self.failure(result, "LINK_OR_REPARSE_PATH_REFUSED")

    def test_11_missing_parent_and_directory_output_refused(self):
        self.failure(self.call("info", output=self.root / "absent" / "request.json"))
        directory = self.root / "directory"
        directory.mkdir()
        result = self.call("info", output=directory)
        self.assertNotEqual(result[0], 0)
        self.assertEqual(list(directory.iterdir()), [])

    def test_12_missing_or_extra_fields_and_control_handles_refused(self):
        self.failure(self.call("publish", ("--artifact", "artifact:x")))
        self.failure(self.call("info", ("--unexpected", "x")))
        self.failure(self.call("peer-find", ("--peer", "bad peer")), "PEER_ALIAS_REQUIRED")
        self.failure(self.call("peer-acquire", ("--remote", "remote:\ninvalid")), "BOUNDED_OPAQUE_HANDLE_REQUIRED")


if __name__ == "__main__":
    unittest.main()

"""Ten offline source-package contracts on inert, owner-created source trees.

Only the hash-selected packager and the Python standard library are imported.
Fixtures contain no executable product or Lean inputs. Native execution, network,
installation, mathematical acceptance and authentic CLI origin are not tested.
Root alone may import/run this suite after review and a fresh bounded allocation.
"""
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

if not (os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
        and sys.flags.no_site and sys.flags.no_user_site):
    raise RuntimeError("WINDOWS_PYTHON_PROFILE")

INSTALL = Path(__file__).resolve().parents[1]
BUILDER = INSTALL / "release" / "package_source.py"
BUILDER_SHA = "c74ad2abb9ce8696328785f634623c20891a1dd3a11cf3fd511d1f084d080c51"
if BUILDER.stat().st_size != 14492 or hashlib.sha256(BUILDER.read_bytes()).hexdigest() != BUILDER_SHA:
    raise RuntimeError("REVIEWED_PACKAGER_PIN")
_spec = importlib.util.spec_from_file_location("source_package_under_test", BUILDER)
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)
if Path(P.__file__).resolve() != BUILDER:
    raise RuntimeError("PACKAGER_MODULE_ORIGIN")

MIB = 1048576
# Independent fixture vocabulary, not a copy obtained from the imported builder.
PY_FILES = ("admin_manage.py", "admin_worker.py", "capacity.py", "checking.py",
    "codec.py", "domains.py", "hosting.py", "inspect_context.py", "node.py", "peer_node.py",
    "peer_service.py", "peer_wire.py", "recovery_manage.py", "recovery_worker.py",
    "run_stage.py", "service_worker.py", "source_codec.py", "storage.py",
    "supervise.py", "symbol_index.py")
LEAN_FILES = ("AgentClient.lean", "AgentReplayCore.lean", "BootstrapSupport.lean")
DOC_FILES = ("API.md", "CORE.md", "PEER.md", "RECOVERY.md", "README.md", "HOSTING.md", "AGENT-QUICKSTART.md")
COMMON = ("ext", "injective", "property", "subtype", "val")
LOCKED = {"py/codec.py", "py/source_codec.py", "py/symbol_index.py"} | {
    "native/" + name for name in LEAN_FILES}


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def safe(path):
    if not path.is_absolute():
        raise RuntimeError("ABSOLUTE_TEST_ROOT")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise RuntimeError("TEST_REPARSE_POINT")
    return path.resolve(strict=True)


class SourcePackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = safe(Path(os.environ.get("DTMKN_TEST_ROOT", "")))
        if (not parent.is_dir() or parent.is_relative_to(INSTALL)
                or INSTALL.is_relative_to(parent)):
            raise RuntimeError("EXTERNAL_TEST_ROOT")
        cls.suite = parent / "source-package"
        cls.suite.mkdir(exist_ok=False)

    def setUp(self):
        self.root = self.suite / self._testMethodName
        self.root.mkdir(exist_ok=False)
        self.stack, self.notes = ExitStack(), {}

    def save(self, path, raw):
        self.assertIs(type(raw), bytes)
        self.assertLessEqual(len(raw), 2 * MIB + 1)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())

    def fixture(self, name="source", *, quick="draft", omit=(), extra=None,
                overrides=None, lock_change=None):
        source = self.root / name
        source.mkdir(exist_ok=False)
        names = {"build.py", "manage.py", "make_request.py", "release/package_source.py", "release/README.md",
            *DOC_FILES, *("py/" + item for item in PY_FILES),
            *("native/" + item for item in LEAN_FILES),
            "assets/foundation/seed-verified.json", "assets/foundation/seed-inventory-json.json",
            *("assets/common/" + item + "/manifest.json" for item in COMMON)}
        names.update("assets/common/" + COMMON[i % 5] + "/objects/" + format(i + 1, "02x") + ".cbor"
                     for i in range(68))
        payloads = {item: b"INERT fixture, never execute: " + item.encode("ascii") + b"\n"
                    for item in names}
        payloads.update(overrides or {})
        lock = {"schema": 1, "scope": "Synthetic inert source-package contract only",
                "files": [{"path": item, "bytes": len(payloads[item]), "sha256": digest(payloads[item])}
                          for item in sorted(names) if item.startswith("assets/") or item in LOCKED]}
        self.assertEqual(len(lock["files"]), 81)
        if lock_change is not None:
            lock_change(lock)
        payloads["assets-lock.json"] = encoded(lock)
        payloads["QUICKSTART.md"] = b"INERT synthetic operator quickstart; no accepted mathematics.\n"
        self.assertEqual(len(payloads), 112)
        mapping = {item: item for item in payloads}
        mapping["QUICKSTART.md"] = "QUICKSTART.md" if quick == "extracted" else "drafts/OPERATOR-QUICKSTART.md"
        for item, raw in sorted(payloads.items()):
            path = source / mapping[item]
            path.parent.mkdir(parents=True, exist_ok=True)
            if item not in omit and not (item == "QUICKSTART.md" and quick == "none"):
                self.save(path, raw)
        if quick == "both":
            self.save(source / "QUICKSTART.md", payloads["QUICKSTART.md"])
        for item, raw in (extra or {}).items():
            self.save(source / item, raw)
        return SimpleNamespace(source=source, payloads=payloads, mapping=mapping, lock=lock)

    def output(self, name):
        path = self.root / name
        path.mkdir(exist_ok=False)
        return path

    def refusal(self, code, function, *args, **kwargs):
        with self.assertRaises(ValueError) as caught:
            function(*args, **kwargs)
        self.assertEqual(str(caught.exception), code)

    def invoke_main(self, source, output, *, fixture_origin=True):
        # __file__ replacement qualifies argument/error flow only, NOT that an
        # authentic public CLI was executed from the selected source tree.
        captured = io.BytesIO()
        with ExitStack() as stack:
            stack.enter_context(patch.object(P.sys, "argv", [str(BUILDER), "--source", str(source),
                                                           "--output", str(output)]))
            stack.enter_context(patch.object(P.sys, "stdout", SimpleNamespace(buffer=captured)))
            if fixture_origin:
                stack.enter_context(patch.object(P, "__file__", str(source / "release/package_source.py")))
            status = P.main()
        raw = captured.getvalue()
        self.assertLessEqual(len(raw), 4096)
        reply = json.loads(raw)
        self.save(self.root / (output.name + "-stdout.json"), raw)
        self.assertIs(reply["mathematical_acceptance"], False)
        return status, reply

    def failed_main(self, source, output, code, *, created=False, fixture_origin=True):
        status, reply = self.invoke_main(source, output, fixture_origin=fixture_origin)
        self.assertEqual(status, 1)
        self.assertEqual(reply["status"], "SOURCE_PACKAGE_FAILED")
        self.assertEqual(reply["code"], "ValueError")
        self.assertEqual(reply["detail"], code)
        self.assertIs(reply["partial_output_preserved"], created)
        self.assertFalse((output / "PACKAGE-RESULT.json").exists())
        if created:
            self.assertEqual(json.loads((output / "PACKAGE-FAILURE.json").read_bytes()), reply)
        else:
            self.assertFalse((output / "PACKAGE-FAILURE.json").exists())
        return reply

    def test_01_archive_members_hashes_and_determinism(self):
        fixture = self.fixture()
        first, second = self.output("first"), self.output("second")
        result = P.package(fixture.source, first)
        self.assertEqual(P.package(fixture.source, second), result)
        self.assertEqual(result["status"], "DEVELOPMENT_SOURCE_PACKAGED_UNQUALIFIED")
        for flag in ("runtime_included", "mathematical_acceptance", "external_publication"):
            self.assertIs(result[flag], False)
        self.assertEqual(result["source_files"], 112)
        self.assertEqual(result["source_bytes"], sum(map(len, fixture.payloads.values())))
        self.assertEqual(set(item.name for item in first.iterdir()),
                         {"math-commons-source.zip", "SOURCE-MANIFEST.json", "PACKAGE-RESULT.json"})
        for item in first.iterdir():
            self.assertEqual(item.read_bytes(), (second / item.name).read_bytes())
        manifest_raw = (first / "SOURCE-MANIFEST.json").read_bytes()
        manifest = json.loads(manifest_raw)
        rows = [{"path": item, "bytes": len(raw), "sha256": digest(raw)}
                for item, raw in sorted(fixture.payloads.items())]
        self.assertEqual(manifest["files"], rows)
        self.assertEqual(manifest["source_bytes"], result["source_bytes"])
        self.assertEqual(manifest["status"], "DEVELOPMENT_SOURCE_UNQUALIFIED")
        self.assertIsNone(manifest["signature"])
        archive_raw = (first / "math-commons-source.zip").read_bytes()
        self.assertEqual(result["archive_bytes"], len(archive_raw))
        self.assertEqual(result["archive_sha256"], digest(archive_raw))
        self.assertEqual(result["manifest_sha256"], digest(manifest_raw))
        self.assertEqual(json.loads((first / "PACKAGE-RESULT.json").read_bytes()), result)
        expected = {**fixture.payloads, "SOURCE-MANIFEST.json": manifest_raw}
        with zipfile.ZipFile(first / "math-commons-source.zip") as archive:
            self.assertEqual(archive.namelist(), sorted(expected))
            self.assertEqual(len(archive.infolist()), 113)
            self.assertEqual(archive.comment, b"")
            for info in archive.infolist():
                self.assertEqual(archive.read(info), expected[info.filename])
                self.assertEqual(info.file_size, len(expected[info.filename]))
                self.assertEqual(info.compress_size, info.file_size)
                self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
                self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertEqual(info.create_system, 3)
                self.assertEqual(info.external_attr, (stat.S_IFREG | 0o644) << 16)
                self.assertEqual((info.extra, info.comment), (b"", b""))
        self.notes.update(source_files=112, zip_members=113, byte_identical_packages=2,
                          archive_sha256=result["archive_sha256"])

    def test_02_quickstart_export_repackage_and_exclusions(self):
        excluded = {"runtime/private.txt": b"excluded runtime\n", "state/private.db": b"excluded state\n",
                    "tests/private.py": b"excluded tests\n", "drafts/OTHER.md": b"excluded draft\n"}
        fixture = self.fixture(extra=excluded)
        first = self.output("draft-package")
        P.package(fixture.source, first)
        extracted = self.output("extracted")
        with zipfile.ZipFile(first / "math-commons-source.zip") as archive:
            self.assertEqual(set(archive.namelist()), set(fixture.payloads) | {"SOURCE-MANIFEST.json"})
            self.assertEqual(archive.read("QUICKSTART.md"), fixture.payloads["QUICKSTART.md"])
            self.assertTrue(set(excluded).isdisjoint(archive.namelist()))
            self.assertNotIn("drafts/OPERATOR-QUICKSTART.md", archive.namelist())
            for item in archive.namelist():
                self.assertFalse(Path(item).is_absolute())
                self.assertNotIn("..", Path(item).parts)
                self.save(extracted / item, archive.read(item))
        second = self.output("extracted-package")
        P.package(extracted, second)
        for name in ("math-commons-source.zip", "SOURCE-MANIFEST.json", "PACKAGE-RESULT.json"):
            self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())
        self.notes.update(real_zip_extraction=True, excluded_paths=sorted(excluded),
                          extracted_source_repackage_byte_identical=True)

    def test_03_exact_selected_trees_reject_missing_and_extra(self):
        missing = ("py/admin_manage.py", "native/AgentClient.lean", "assets/foundation/seed-verified.json")
        for index, item in enumerate(missing):
            with self.subTest(missing=item):
                fixture = self.fixture("missing-" + str(index), omit=(item,))
                self.refusal("MISSING_SELECTED_TREE_ENTRY", P.sources, fixture.source)
        for prefix in ("py", "native", "assets"):
            with self.subTest(extra=prefix):
                fixture = self.fixture("extra-" + prefix, extra={prefix + "/unselected.txt": b"unexpected\n"})
                self.refusal("UNKNOWN_SELECTED_TREE_ENTRY", P.sources, fixture.source)
        self.notes.update(real_missing_selected_files=list(missing), real_extra_selected_trees=["py", "native", "assets"])

    def test_04_asset_lock_paths_pins_duplicates_and_types(self):
        fixture = self.fixture()
        rows = P.asset_rows(encoded(fixture.lock))
        self.assertEqual(len(rows), 81)
        self.assertEqual(sum(name.startswith("assets/") for name in rows), 75)
        cases = []
        def variant(name, code, edit):
            value = deepcopy(fixture.lock)
            edit(value)
            cases.append((name, code, encoded(value)))
        variant("boolean-schema", "ASSET_LOCK_SHAPE", lambda v: v.update(schema=True))
        variant("boolean-bytes", "ASSET_PIN_SHAPE", lambda v: v["files"][0].update(bytes=True))
        variant("bad-hash", "ASSET_PIN_SHAPE", lambda v: v["files"][0].update(sha256="z" * 64))
        variant("duplicate-path", "ASSET_PIN_SHAPE", lambda v: v["files"].__setitem__(1, deepcopy(v["files"][0])))
        variant("traversal", "ASSET_PATH_NOT_ALLOWLISTED", lambda v: v["files"][0].update(path="assets/../secret"))
        variant("uppercase-object", "ASSET_PATH_NOT_ALLOWLISTED", lambda v: v["files"][0].update(path="assets/common/ext/objects/AB.cbor"))
        variant("extra-row-key", "ASSET_LOCK_ROW", lambda v: v["files"][0].update(extra=0))
        variant("missing-row", "ASSET_LOCK_SELECTED_COUNT", lambda v: v["files"].pop())
        foundation_index = next(i for i, row in enumerate(fixture.lock["files"])
                                if row["path"] == "assets/foundation/seed-verified.json")
        variant("missing-foundation", "ASSET_LOCK_SELECTED_SHAPE", lambda v: v["files"][foundation_index].update(
            path="assets/common/ext/objects/ffff.cbor"))
        duplicate_key = encoded(fixture.lock).replace(b'"schema":1', b'"schema":1,"schema":1', 1)
        cases.append(("duplicate-json-key", "DUPLICATE_JSON_KEY", duplicate_key))
        for name, code, raw in cases:
            with self.subTest(case=name):
                self.save(self.root / (name + ".json"), raw)
                self.refusal(code, P.asset_rows, raw)
        for name, update in (("content-hash", {"sha256": "0" * 64}), ("content-size", {"bytes": 1})):
            with self.subTest(case=name):
                altered = self.fixture(name, lock_change=lambda v, update=update: v["files"][0].update(update))
                self.refusal("ASSET_LOCK_MISMATCH", P.sources, altered.source)
        self.notes.update(lock_shape_refusals=[name for name, _, _ in cases], actual_asset_binding_refusals=2)

    def test_05_ambiguous_or_missing_quickstart_refuses(self):
        for mode in ("both", "none"):
            with self.subTest(mode=mode):
                fixture = self.fixture(mode, quick=mode)
                self.refusal("EXACTLY_ONE_SELECTED_QUICKSTART_REQUIRED", P.sources, fixture.source)
        self.notes.update(quickstart_refusals=["both", "none"])

    def test_06_real_per_file_and_aggregate_byte_bounds(self):
        maximum, excessive = self.root / "exact-2mib.bin", self.root / "over-2mib.bin"
        self.save(maximum, b"x" * (2 * MIB))
        self.save(excessive, b"x" * (2 * MIB + 1))
        self.assertEqual(len(P.bounded_read(maximum)[0]), 2 * MIB)
        self.refusal("FILE_SIZE_BOUND", P.bounded_read, excessive)
        # Windows path/handle ctime can differ. Keep each API's stability
        # guard while matching common identity fields across the two APIs.
        fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns",
                  "st_birthtime_ns", "st_file_attributes", "st_mode")
        def altered(info, **changes):
            values = {name: getattr(info, name) for name in fields}
            return SimpleNamespace(**dict(values, **changes))
        path_stat = maximum.lstat()
        real_fstat = os.fstat
        def distinct_ctime(descriptor):
            return altered(real_fstat(descriptor), st_ctime_ns=path_stat.st_ctime_ns + 1000)
        with patch.object(P.os, "fstat", distinct_ctime):
            self.assertEqual(len(P.bounded_read(maximum)[0]), 2 * MIB)
        with patch.object(P.os, "fstat", lambda descriptor: altered(
                real_fstat(descriptor), st_ino=path_stat.st_ino + 1)):
            self.refusal("FILE_CHANGED_BEFORE_READ", P.bounded_read, maximum)
        handle_calls = []
        def changing_handle_ctime(descriptor):
            handle_calls.append(descriptor)
            return altered(real_fstat(descriptor), st_ctime_ns=path_stat.st_ctime_ns + len(handle_calls))
        with patch.object(P.os, "fstat", changing_handle_ctime):
            self.refusal("FILE_CHANGED_DURING_READ", P.bounded_read, maximum)
        self.assertEqual(len(handle_calls), 2)
        with patch.object(P, "checked_stat", side_effect=[path_stat,
                altered(path_stat, st_ctime_ns=path_stat.st_ctime_ns + 1)]):
            self.refusal("FILE_CHANGED_AFTER_READ", P.bounded_read, maximum)
        self.notes.update(mocked_cross_api_ctime_difference_accepted=True,
                          mocked_identity_handle_change_and_path_change_refused=True)
        large_names = ("build.py", "manage.py", "API.md", "CORE.md", "PEER.md",
                       "RECOVERY.md", "README.md", "release/README.md", "py/admin_manage.py")
        self.assertEqual(len(large_names), 9)
        self.assertTrue(set(large_names).isdisjoint(LOCKED))
        fixture = self.fixture(overrides={name: b"y" * (2 * MIB) for name in large_names})
        self.assertEqual(sum((fixture.source / name).stat().st_size for name in large_names), 18 * MIB)
        self.refusal("SOURCE_TOTAL_BYTES", P.sources, fixture.source)
        self.notes.update(real_file_limit=2 * MIB, real_refused_file_bytes=2 * MIB + 1,
                          real_aggregate_large_files=9, real_aggregate_large_bytes=18 * MIB,
                          aggregate_guard=16 * MIB, mocked_size_limits=False)

    def test_07_windows_namespace_and_mocked_reparse_guards(self):
        namespaces = ("relative", r"C:relative", r"\\server\share\part", r"\\?\C:\part", r"\\.\C:\part")
        for raw in namespaces:
            with self.subTest(namespace=raw):
                self.refusal("LOCAL_DRIVE_PATH_REQUIRED", P.absolute, Path(raw))
        for raw in ("C:\\", r"C:\base\..\child"):
            self.refusal("ABSOLUTE_NONROOT_PATH", P.absolute, Path(raw))
        components = (r"C:\base\file:stream", r"C:\base\NUL", "C:\\base\\tail.", "C:\\base\\tail ")
        for raw in components:
            with self.subTest(component=raw):
                self.refusal("PATH_COMPONENT", P.absolute, Path(raw))
        self.assertEqual(P.absolute(self.root), self.root)
        selected = self.root / "ordinary.txt"
        self.save(selected, b"actual regular file\n")
        P.checked_stat(selected, directory=False)
        P.checked_stat(self.root, directory=True)
        real_lstat = Path.lstat
        def reparse(path, *args, **kwargs):
            if path == selected:
                return SimpleNamespace(st_mode=stat.S_IFREG | 0o644, st_file_attributes=0x400)
            return real_lstat(path, *args, **kwargs)
        with patch.object(Path, "lstat", reparse):
            self.refusal("LINK_OR_REPARSE_PATH", P.checked_stat, selected, directory=False)
        self.notes.update(refused_namespace_spellings=list(namespaces), refused_components=list(components),
                          mocked_reparse_stat=True, actual_reparse_creation=False)

    def test_08_main_freshness_overlap_origin_and_mocked_alias(self):
        fixture = self.fixture()
        reused = self.output("reused")
        self.save(reused / "sentinel.txt", b"must remain unchanged\n")
        self.failed_main(fixture.source, reused, "FRESH_OUTPUT_REQUIRED")
        self.assertEqual((reused / "sentinel.txt").read_bytes(), b"must remain unchanged\n")
        self.assertEqual([path.name for path in reused.iterdir()], ["sentinel.txt"])
        nested = fixture.source / "nested-output"
        self.failed_main(fixture.source, nested, "SOURCE_OUTPUT_OVERLAP")
        self.assertFalse(nested.exists())
        self.failed_main(fixture.source, self.root, "SOURCE_OUTPUT_OVERLAP")
        wrong = self.root / "wrong-origin"
        self.failed_main(fixture.source, wrong, "RUN_SELECTED_SOURCE_BUILDER", fixture_origin=False)
        self.assertFalse(wrong.exists())
        alias_parent = self.output("mock-alias-parent")
        alias_output = alias_parent / "aliased-output"
        real_resolve = Path.resolve
        def alias(path, *args, **kwargs):
            if path == alias_parent:
                return fixture.source
            return real_resolve(path, *args, **kwargs)
        with patch.object(Path, "resolve", alias):
            self.failed_main(fixture.source, alias_output, "SOURCE_OUTPUT_OVERLAP")
        self.assertFalse(alias_output.exists())
        self.assertFalse((fixture.source / alias_output.name).exists())
        self.notes.update(mocked_fixture_entrypoint_for_main=True, mocked_canonical_parent_alias=True,
                          actual_os_alias_created=False, authentic_public_cli_origin_qualified=False)

    def test_09_observed_source_change_preserves_failed_output(self):
        fixture = self.fixture()
        original = fixture.payloads["README.md"]
        self.save(self.root / "retained-original-README.md", original)
        altered = b"INERT changed fixture README during package recheck\n"
        calls = []
        real_check_shape = P.check_shape
        def change_at_second_check(source, mapping):
            calls.append(str(source))
            if len(calls) == 2:
                self.assertEqual(source, fixture.source)
                with (source / "README.md").open("wb") as stream:
                    stream.write(altered)
                    stream.flush()
                    os.fsync(stream.fileno())
            return real_check_shape(source, mapping)
        output = self.root / "changed-source-output"
        with patch.object(P, "check_shape", change_at_second_check):
            self.failed_main(fixture.source, output, "SOURCE_CHANGED_DURING_PACKAGE", created=True)
        self.assertEqual(len(calls), 2)
        self.assertEqual((fixture.source / "README.md").read_bytes(), altered)
        self.assertEqual((self.root / "retained-original-README.md").read_bytes(), original)
        self.assertEqual(set(path.name for path in output.iterdir()),
                         {"math-commons-source.zip", "PACKAGE-FAILURE.json"})
        with zipfile.ZipFile(output / "math-commons-source.zip") as archive:
            self.assertEqual(archive.read("README.md"), original)
        self.notes.update(injected_actual_owned_source_mutation=True, original_retained=True,
                          mocked_fixture_entrypoint_for_main=True,
                          partial_output="Complete ZIP retained but post-write source check refused; no success marker")

    def test_10_archive_member_corruption_preserves_failed_output(self):
        fixture = self.fixture()
        output = self.root / "corrupt-archive-output"
        archive_path = output / "math-commons-source.zip"
        real_read = P.bounded_read
        injected = []
        def corrupt_before_verification(path, maximum=P.FILE_MAX):
            if path == archive_path and not injected:
                injected.append(str(path))
                self.save(self.root / "retained-precorruption.zip", path.read_bytes())
                with zipfile.ZipFile(path, "a", compression=zipfile.ZIP_STORED, allowZip64=False) as archive:
                    archive.writestr("UNEXPECTED.txt", b"Injected unselected archive member\n")
            return real_read(path, maximum)
        with patch.object(P, "bounded_read", corrupt_before_verification):
            self.failed_main(fixture.source, output, "ARCHIVE_MEMBER_SET", created=True)
        self.assertEqual(len(injected), 1)
        self.assertEqual(set(path.name for path in output.iterdir()),
                         {"math-commons-source.zip", "PACKAGE-FAILURE.json"})
        with zipfile.ZipFile(self.root / "retained-precorruption.zip") as archive:
            self.assertEqual(len(archive.namelist()), 113)
            self.assertNotIn("UNEXPECTED.txt", archive.namelist())
        with zipfile.ZipFile(archive_path) as archive:
            self.assertEqual(len(archive.namelist()), 114)
            self.assertEqual(archive.read("UNEXPECTED.txt"), b"Injected unselected archive member\n")
        self.notes.update(injected_actual_archive_member_corruption=True, original_archive_retained=True,
                          mocked_verification_boundary=True, mocked_fixture_entrypoint_for_main=True,
                          authentic_public_cli_origin_qualified=False)

    def census(self):
        rows, total, entries = {}, 0, 0
        for path in self.root.rglob("*"):
            entries += 1
            self.assertLessEqual(entries, 4096)
            safe(path)
            if path.is_file():
                size = path.stat().st_size
                total += size
                self.assertLessEqual(size, 2 * MIB + 1)
                self.assertLessEqual(total, 64 * MIB)
                self.assertLess(len(rows), 2048)
                raw = path.read_bytes()
                self.assertEqual(len(raw), size)
                rows[path.relative_to(self.root).as_posix()] = {"bytes": size, "sha256": digest(raw)}
        return {"files": rows, "bytes": total, "entries": entries,
                "scope": "Per-method retained fixture census before this report"}

    def tearDown(self):
        self.stack.close()
        imported_product = sorted(str(Path(module.__file__).resolve())
            for module in tuple(sys.modules.values())
            if getattr(module, "__file__", None) and Path(module.__file__).is_absolute()
            and Path(module.__file__).resolve().is_relative_to(INSTALL / "py"))
        self.assertEqual(imported_product, [])
        report = {"test": self._testMethodName, "builder_sha256": BUILDER_SHA,
            "fixture_source_bytes_are_inert": True, "native_executions": 0,
            "mathematical_acceptance_claim": False, "external_publication": False,
            "authentic_public_cli_execution_claim": False, "imported_product_modules": imported_product,
            "notes": self.notes, "census": self.census()}
        raw = encoded(report)
        self.assertLessEqual(len(raw), 192 * 1024)
        self.save(self.root / "report.json", raw)


if __name__ == "__main__":
    unittest.main()

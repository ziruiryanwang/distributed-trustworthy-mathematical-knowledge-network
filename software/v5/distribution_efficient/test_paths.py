"""Tiny directory-cache controls; no SDK, native worker or proof is invoked."""
import hashlib
import importlib.util
import json
from pathlib import Path
import stat
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("_tested_efficient_distribution",
                                             HERE/"distribution.py")
D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(D)
METRICS = {}


def expected(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


class Controls(unittest.TestCase):
    def setUp(self):
        self.root = OUTPUT/self._testMethodName
        self.root.mkdir()

    def leaf(self, name, raw=b"one\n"):
        path = self.root/name
        with path.open("xb") as stream:
            stream.write(raw)
        return path

    def test_resolve_cost_tracks_new_directories_not_files(self):
        left, right = self.root/"left", self.root/"right"
        left.mkdir()
        right.mkdir()
        files = [left/"a", left/"b", left/"c", right/"a", right/"b"]
        for path in files:
            with path.open("xb") as stream:
                stream.write(b"x")
        original = Path.resolve
        calls = []

        def counted(path, *args, **kwargs):
            calls.append(path)
            return original(path, *args, **kwargs)

        with patch.object(Path, "resolve", counted), D.path_scope():
            D.ordinary(files[0])
            initial = len(calls)
            self.assertGreater(initial, 0)
            self.assertLessEqual(initial, len(files[0].parents))
            self.assertEqual(len(set(calls)), initial)
            self.assertTrue(all(path.is_dir() for path in calls))
            for path in files[:3]:
                D.ordinary(path)
            self.assertEqual(len(calls), initial)
            D.ordinary(files[3])
            self.assertEqual(len(calls), initial+1)
            D.ordinary(files[4])
            self.assertEqual(len(calls), initial+1)
        METRICS["resolve_cost"] = {"first_directory_chain": initial,
            "same_directory_additional_leaf_resolves": 0,
            "one_new_directory_additional_resolves": 1,
            "file_leaf_resolves": sum(path in files for path in calls)}
        self.assertEqual(METRICS["resolve_cost"]["file_leaf_resolves"], 0)

    def test_fresh_existence_and_leaf_kind_are_never_cached(self):
        path = self.leaf("mutable-leaf")
        with D.path_scope():
            D.ordinary(path)
            with self.assertRaisesRegex(ValueError, "DIST_FRESH_PATH"):
                D.ordinary(path, fresh=True)
            path.unlink()  # Only this tiny synthetic fixture is replaced.
            with self.assertRaises(FileNotFoundError):
                D.ordinary(path)
            D.ordinary(path, fresh=True)
            path.mkdir()
            D.ordinary(path, directory=True)
            with self.assertRaisesRegex(ValueError, "DIST_ORDINARY_TARGET"):
                D.ordinary(path)
            with self.assertRaisesRegex(ValueError, "DIST_FRESH_PATH"):
                D.ordinary(path, directory=True, fresh=True)

    def test_every_leaf_lstat_rejects_reparse_and_wrong_kind(self):
        path = self.leaf("metadata-leaf")
        original = Path.lstat
        mode = {"override": None, "leaf_calls": 0}

        def inspected(current, *args, **kwargs):
            info = original(current, *args, **kwargs)
            if current == path:
                mode["leaf_calls"] += 1
                if mode["override"] == "reparse":
                    return SimpleNamespace(st_mode=info.st_mode,
                        st_file_attributes=getattr(info, "st_file_attributes", 0) | 0x400)
                if mode["override"] == "directory":
                    return SimpleNamespace(st_mode=stat.S_IFDIR | 0o700,
                                           st_file_attributes=0)
            return info

        with patch.object(Path, "lstat", inspected), D.path_scope():
            D.ordinary(path)
            after_first = mode["leaf_calls"]
            for override in ("reparse", "directory"):
                mode["override"] = override
                with self.assertRaisesRegex(ValueError, "DIST_ORDINARY_TARGET"):
                    D.ordinary(path)
            mode["override"] = None
            D.ordinary(path)
            self.assertEqual(mode["leaf_calls"]-after_first, 3)
        METRICS["leaf_metadata"] = {"repeated_calls_checked": 3,
                                   "synthetic_reparse_and_wrong_kind_rejected": True}

    def test_size_and_hash_checks_are_never_cached(self):
        original = b"abcd"
        path = self.leaf("pin-leaf", original)
        pin = expected(original)
        with D.path_scope():
            D.pinned(path, pin)
            path.write_bytes(b"abce")
            with self.assertRaisesRegex(ValueError, "DIST_PIN:"):
                D.pinned(path, pin)
            path.write_bytes(b"abcde")
            with self.assertRaisesRegex(ValueError, "DIST_PIN_SIZE:"):
                D.pinned(path, pin)
            path.write_bytes(original)
            D.pinned(path, pin)

    def test_size_is_rechecked_after_digest(self):
        raw = b"same"
        path = self.leaf("changed-during-digest", raw)
        file_digest = hashlib.file_digest

        def mutate_after_digest(stream, algorithm):
            result = file_digest(stream, algorithm)
            with path.open("ab") as writer:
                writer.write(b"x")
            return result

        with D.path_scope():
            D.pinned(path, expected(raw))
            with patch.object(hashlib, "file_digest", mutate_after_digest):
                with self.assertRaisesRegex(ValueError, "DIST_PIN:"):
                    D.pinned(path, expected(raw))
        self.assertEqual(path.read_bytes(), raw+b"x")

    def test_scope_reset_nesting_and_exception_restore(self):
        path = self.leaf("scope-leaf")
        original = Path.resolve
        calls = []

        def counted(current, *args, **kwargs):
            calls.append(current)
            return original(current, *args, **kwargs)

        class SelectedFailure(Exception):
            pass

        with patch.object(Path, "resolve", counted):
            with self.assertRaises(SelectedFailure):
                with D.path_scope():
                    D.ordinary(path)
                    chain = len(calls)
                    self.assertGreater(chain, 0)
                    with D.path_scope():
                        D.ordinary(path)
                    self.assertEqual(len(calls), 2*chain)
                    D.ordinary(path)
                    self.assertEqual(len(calls), 2*chain)
                    with self.assertRaises(SelectedFailure):
                        with D.path_scope():
                            D.ordinary(path)
                            raise SelectedFailure()
                    self.assertEqual(len(calls), 3*chain)
                    D.ordinary(path)
                    self.assertEqual(len(calls), 3*chain)
                    raise SelectedFailure()
            with D.path_scope():
                D.ordinary(path)
            self.assertEqual(len(calls), 4*chain)
            # Outside a scope the original uncached ordinary() behavior remains.
            D.ordinary(path)
            D.ordinary(path)
            self.assertEqual(len(calls), 4*chain+2)
            self.assertEqual(calls[-2:], [path, path])
        METRICS["scope_lifecycle"] = {"directory_chain_per_fresh_scope": chain,
            "fresh_scopes_checked": 4, "unscoped_file_resolves": 2,
            "normal_and_exception_nesting_restore_outer": True}


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
    OUTPUT = Path(sys.argv[2])
    D.ordinary(OUTPUT, directory=True)
    D.ordinary(OUTPUT/"controls.json", fresh=True)
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    report = {
        "status": "PASS" if result.wasSuccessful() else "FAIL",
        "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "scope": "DIRECTORY_CACHE_CHANGED_BOUNDARIES_NO_MATH_AUTHORITY",
        "sources": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                    for name in ("distribution.py", "test_paths.py")},
        "metrics": METRICS, "native_calls": 0, "proof_calls": 0, "sdk_imports": 0,
    }
    with (OUTPUT/"controls.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

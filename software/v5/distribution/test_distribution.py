"""Small changed-boundary checks; no SDK, native worker or proof is invoked."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("_tested_distribution", HERE/"distribution.py")
D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(D)
SAMPLE = {"bytes": 1, "sha256": "12"*32}


def manifest():
    files = {key: deepcopy(SAMPLE) for key in (
        "distribution.py", "README.md", "owners/reader.py", "owners/serve.py",
        "base/RELEASE-MANIFEST.json", "base/python.exe", "base/python.dll",
        "sdk/v5/authoring/worker.py", "assets/lean/bin/selected.dll")}
    files["base/RELEASE-MANIFEST.json"]["sha256"] = D.BASE_SHA
    roles = {name: "assets/"+name+"/selected" for name in D.ROLES}
    files.update({value: deepcopy(SAMPLE) for value in roles.values()})
    def pin(path):
        return {"path": path, **files[path]}
    profile = {
        "schema": "DMKN_V5_PREPARATION_PROFILE_V1",
        "producer": {
            "schema": "DMKN_V5_PRODUCER_PROFILE_V1",
            "supervisor_manifest": pin("base/RELEASE-MANIFEST.json"),
            "host": pin(roles["receipt"]),
            "python": pin("base/python.exe"), "python_dll": pin("base/python.dll"),
            "source_pins": [], "runtime_pins": [],
            "image_id": D.RELATION, "foundation": D.FOUNDATION, "policy": D.POLICY,
        },
        "image": pin(roles["image"]), "worker": pin("sdk/v5/authoring/worker.py"),
        "native_executable": pin(roles["frontend"]), "lean_root": "assets/lean",
        "lean_runtime_pins": [pin("assets/lean/bin/selected.dll")], "source_pins": [],
    }
    return {
        "schema": D.RELEASE_SCHEMA, "base_manifest_sha256": D.BASE_SHA, "files": files,
        "sdk_sources": {"v5/authoring/worker.py": "sdk/v5/authoring/worker.py"},
        "roles": roles, "aggregate_image": "ab"*32, "preparation": profile,
        "build_input_sha256": "cd"*32,
    }


class Controls(unittest.TestCase):
    def test_strict_json(self):
        self.assertEqual(D.parse(b'{"integer":1}'), {"integer": 1})
        for raw in (b'{"x":1,"x":2}', b'{"x":1.1}', b'{"x":NaN}'):
            with self.assertRaises(ValueError):
                D.parse(raw)

    def test_relative_paths(self):
        self.assertEqual(D.relative("sdk/v5/worker.py"), ("sdk", "v5", "worker.py"))
        for name in ("../a", "/a", "E:/a", "a\\b", "a//b", "a/./b", "NUL",
                     "a/b.", "a/b ", "a/b:c", "a/\n", ""):
            with self.subTest(name=name), self.assertRaises(ValueError):
                D.relative(name)

    def test_map_aliases_and_bounds(self):
        D.file_map({"one/a": SAMPLE, "one/b": SAMPLE})
        for value in (
            {"one/a": SAMPLE, "one/A": SAMPLE},
            {"one/a": SAMPLE, "One/b": SAMPLE},
            {"one": SAMPLE, "one/a": SAMPLE},
            {"one/a": {"bytes": True, "sha256": SAMPLE["sha256"]}},
            {"one/a": {"bytes": D.MIB*129, "sha256": SAMPLE["sha256"]}},
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                D.file_map(value)

    def test_profile_role_binding(self):
        D.validate_manifest(manifest())
        bad = manifest()
        bad["preparation"]["producer"]["host"]["path"] = bad["roles"]["native"]
        with self.assertRaises(ValueError):
            D.validate_manifest(bad)
        bad = manifest()
        bad["preparation"]["producer"]["policy"] = "00"*32
        with self.assertRaises(ValueError):
            D.validate_manifest(bad)
        bad = manifest()
        bad["preparation"]["worker"]["sha256"] = "ff"*32
        with self.assertRaises(ValueError):
            D.validate_manifest(bad)
        bad = manifest()
        bad["preparation"]["image"]["path"] = "../outside"
        with self.assertRaises(ValueError):
            D.validate_manifest(bad)

    def test_profile_materialization(self):
        source = manifest()["preparation"]
        saved = deepcopy(source)
        root = Path(r"E:\Owner Chosen Installation")
        actual = D.materialize(root, source)
        self.assertEqual(source, saved)
        self.assertEqual(actual["lean_root"], str(root/"assets/lean"))
        def check(value):
            if type(value) is dict:
                if "path" in value:
                    self.assertTrue(Path(value["path"]).is_relative_to(root))
                else:
                    for child in value.values():
                        check(child)
            elif type(value) is list:
                for child in value:
                    check(child)
        check(actual)

    def test_explicit_nested_role_substitution(self):
        roles = {"runtime_adoption": {"marker": [1]}, "foundation": {"bytes": 4}}
        source = {"reader": {"runtime_adoption": {"$installed": "runtime_adoption"},
                             "foundation": {"$installed": "foundation"}},
                  "unchanged": ["literal"]}
        actual = D.substitute(source, roles)
        self.assertEqual(set(actual), {"reader", "unchanged"})
        self.assertEqual(actual["reader"], roles)
        actual["reader"]["runtime_adoption"]["marker"].append(2)
        self.assertEqual(roles["runtime_adoption"], {"marker": [1]})
        self.assertEqual(source["reader"]["foundation"], {"$installed": "foundation"})
        for bad in ({"$installed": "arbitrary_path"},
                    {"$installed": "foundation", "extra": True}):
            with self.assertRaises(ValueError):
                D.substitute(bad, roles)
        deep = None
        for unused in range(66):
            deep = [deep]
        with self.assertRaises(ValueError):
            D.substitute(deep, roles)

    def test_streamed_copy_and_no_overwrite(self):
        source = OUTPUT/"copy-source"
        raw = b"small selected file\n"
        source.write_bytes(raw)
        expected = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        target = OUTPUT/"copy-good"
        D.copy_pinned(source, target, expected)
        self.assertEqual(target.read_bytes(), raw)
        with self.assertRaises(ValueError):
            D.copy_pinned(source, target, expected)
        self.assertEqual(target.read_bytes(), raw)
        bad = OUTPUT/"copy-bad"
        with self.assertRaises(ValueError):
            D.copy_pinned(source, bad, {**expected, "sha256": "ff"*32})
        self.assertEqual(bad.read_bytes(), raw)  # retain failed bytes, do not erase.


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
    OUTPUT = Path(sys.argv[2])
    D.ordinary(OUTPUT, directory=True)
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    report = {
        "status": "PASS" if result.wasSuccessful() else "FAIL",
        "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "scope": "SYNTHETIC_DISTRIBUTION_BOUNDARIES_NO_MATH_AUTHORITY",
        "sources": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                    for name in ("distribution.py", "test_distribution.py")},
        "native_calls": 0, "proof_calls": 0, "sdk_imports": 0,
    }
    with (OUTPUT/"controls.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

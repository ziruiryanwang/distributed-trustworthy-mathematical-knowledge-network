"""Pure changed-role/closure controls; no SDK, compiler or native calls."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE/filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


D = load("_tested_complete_distribution", "distribution.py")
S = load("_tested_complete_selector", "select_inputs.py")
SAMPLE = {"bytes": 1, "sha256": "12"*32}


def support(modules=None):
    modules = {"Init": ["Init.Small"], "Init.Small": []} if modules is None else modules
    return {"profile": D.LEAN_SUPPORT, "modules": deepcopy(modules),
        "files": {"lib/lean/"+name.replace(".", "/")+suffix:
                  {"path": "assets/lean/lib/lean/"+name.replace(".", "/")+suffix, **SAMPLE}
                  for name in modules for suffix in D.LEAN_SUFFIXES}}


def fixture():
    catalogue = {name: deepcopy(SAMPLE) for name in (
        *sorted(D.BASE_HELPERS), "receiver/runtime/python/python.exe",
        "receiver/runtime/python/python.dll", "receiver/runtime/node/unused.js",
        "operator/old-v4-only.py")}
    files = {name: deepcopy(SAMPLE) for name in (
        "distribution.py", "README.md", "owners/reader.py", "owners/serve.py",
        "base/RELEASE-MANIFEST.json", "sdk/v5/authoring/worker.py")}
    files.update({"base/"+name: deepcopy(row)
                  for name, row in D.base_projection(catalogue).items()})
    files["base/RELEASE-MANIFEST.json"]["sha256"] = D.BASE_SHA
    roles = {name: "assets/"+name+"/selected" for name in D.ROLES}
    files.update({name: deepcopy(SAMPLE) for name in roles.values()})
    lean = support()
    files.update({item["path"]: {key: item[key] for key in ("bytes", "sha256")}
                  for item in lean["files"].values()})

    def pin(name):
        return {"path": name, **files[name]}

    profile = {"schema": "DMKN_V5_PREPARATION_PROFILE_V1",
        "producer": {"schema": "DMKN_V5_PRODUCER_PROFILE_V1",
            "supervisor_manifest": pin("base/RELEASE-MANIFEST.json"),
            "host": pin(roles["receipt"]), "python": pin("base/receiver/runtime/python/python.exe"),
            "python_dll": pin("base/receiver/runtime/python/python.dll"),
            "source_pins": [], "runtime_pins": [], "image_id": D.RELATION,
            "foundation": D.FOUNDATION, "policy": D.POLICY},
        "image": pin(roles["image"]), "worker": pin("sdk/v5/authoring/worker.py"),
        "native_executable": pin(roles["frontend"]), "lean_root": "assets/lean",
        "lean_runtime_pins": [pin("assets/lean/lib/lean/Init.olean")], "source_pins": []}
    manifest = {"schema": D.RELEASE_SCHEMA, "base_manifest_sha256": D.BASE_SHA,
        "base_role": D.BASE_ROLE, "files": files,
        "sdk_sources": {"v5/authoring/worker.py": "sdk/v5/authoring/worker.py"},
        "roles": roles, "aggregate_image": "ab"*32, "preparation": profile,
        "lean_support": lean, "build_input_sha256": "cd"*32}
    return catalogue, manifest


class Controls(unittest.TestCase):
    def test_header_comments_multiline_and_modifiers(self):
        raw = """/- outer /- nested import Init.False -/ end -/
module
prelude
public meta import
  Init.One -- retained occurrence
meta import all Init.Two
import Init.One
public section
def ignoredBody := "import Init.NotAHeader"
"""
        self.assertEqual(S.parse_header(raw), [
            {"module": "Init.One", "public": True, "meta": True, "all": False},
            {"module": "Init.Two", "public": False, "meta": True, "all": True},
            {"module": "Init.One", "public": False, "meta": False, "all": False}])
        for bad in ("prelude\nimport Init.One", "module\nimport Init.One",
                    "module\nprelude\nimport Other.One",
                    "module\nprelude\npublic import all Init.One",
                    "module\nprelude\nimport Init..One",
                    "module\nprelude\nimport «Init.One»", "/- never closed"):
            with self.subTest(source=bad), self.assertRaises(ValueError):
                S.parse_header(bad)

    def test_source_fingerprint_binds_bytes_edges_and_flags(self):
        rows = {"Init": {"bytes": 4, "sha256": "ab"*32}}
        edges = {"Init": [{"module": "Init.Small", "public": True, "meta": False, "all": False}]}
        expected_raw = ("Init\t4\t"+"ab"*32+"\tInit.Small:100\n").encode("utf-8")
        original = S.graph_fingerprint(rows, edges)
        self.assertEqual(original, (hashlib.sha256(expected_raw).hexdigest(), len(expected_raw)))
        for change in ("source", "new-edge", "flag"):
            changed_rows, changed_edges = deepcopy(rows), deepcopy(edges)
            if change == "source":
                changed_rows["Init"]["sha256"] = "ac"*32
            elif change == "new-edge":
                changed_edges["Init"].append(
                    {"module": "Init.Other", "public": False, "meta": True, "all": False})
            else:
                changed_edges["Init"][0]["meta"] = True
            self.assertNotEqual(S.graph_fingerprint(changed_rows, changed_edges)[0], original[0])

    def test_graph_closure_missing_extra_and_bad_edges(self):
        good = support()
        self.assertEqual(len(D.support_layout(good)), 10)
        bad_cases = []
        bad = deepcopy(good)
        del bad["files"]["lib/lean/Init/Small.olean.server"]
        bad_cases.append(bad)
        bad = deepcopy(good)
        bad["files"]["lib/lean/Other.olean"] = deepcopy(SAMPLE)
        bad_cases.append(bad)
        bad = deepcopy(good)
        bad["modules"]["Init"].append("Init.Missing")
        bad_cases.append(bad)
        bad_cases.append(support({"Init": [], "Init.Unreachable": []}))
        bad_cases.append(support({"Init": ["Other"], "Other": []}))
        bad_cases.append(support({"Init": ["Init.Small", "Init.Small"], "Init.Small": []}))
        bad_cases.append(support({"Init": ["Init..Small"], "Init..Small": []}))
        for bad in bad_cases:
            with self.subTest(value=bad), self.assertRaises(ValueError):
                D.support_layout(bad)

    def test_support_role_overlap_and_exact_artifact_scope(self):
        unused, good = fixture()
        D.validate_manifest(good)
        for change in ("support-pin", "minimum-pin", "support-path", "extra-file"):
            bad = deepcopy(good)
            support_row = bad["lean_support"]["files"]["lib/lean/Init.olean"]
            if change == "support-pin":
                support_row["sha256"] = "ff"*32
            elif change == "minimum-pin":
                bad["preparation"]["lean_runtime_pins"][0]["sha256"] = "ff"*32
            elif change == "support-path":
                support_row["path"] = "assets/receipt/selected"
            else:
                bad["files"]["assets/lean/lib/lean/Unselected.olean"] = deepcopy(SAMPLE)
            with self.subTest(change=change), self.assertRaises(ValueError):
                D.validate_manifest(bad)

    def test_exact_base_projection_rejects_missing_and_extra_payload(self):
        catalogue, good = fixture()
        projected = D.base_projection(catalogue)
        self.assertEqual(set(projected), D.BASE_HELPERS |
                         {"receiver/runtime/python/python.exe", "receiver/runtime/python/python.dll"})
        missing_helper = deepcopy(catalogue)
        del missing_helper[sorted(D.BASE_HELPERS)[0]]
        with self.assertRaisesRegex(ValueError, "DIST_BASE_HELPERS_MISSING"):
            D.base_projection(missing_helper)
        root = Path(r"E:\Selected Test Installation")
        with patch.object(D, "census"), patch.object(D, "pinned"), \
                patch.object(D, "checked_json", return_value={"files": catalogue}):
            D._verify_release(root, good, full=False)
            for change in ("omitted-helper", "extra-base"):
                bad = deepcopy(good)
                if change == "omitted-helper":
                    del bad["files"]["base/"+sorted(D.BASE_HELPERS)[0]]
                else:
                    bad["files"]["base/receiver/runtime/node/unused.js"] = deepcopy(SAMPLE)
                with self.subTest(change=change), self.assertRaisesRegex(
                        ValueError, "DIST_EXACT_BASE_ROLE_MAP"):
                    D._verify_release(root, bad, full=False)

    def test_each_launch_verification_checks_every_support_payload(self):
        catalogue, manifest = fixture()
        root, calls = Path(r"E:\Selected Test Installation"), []

        def checked(path, row):
            calls.append((path, deepcopy(row)))
            return path

        with patch.object(D, "census"), patch.object(D, "pinned", side_effect=checked), \
                patch.object(D, "checked_json", return_value={"files": catalogue}):
            D._verify_release(root, manifest, full=False)
            first = deepcopy(calls)
            D._verify_release(root, manifest, full=False)
            self.assertEqual(calls, first+first)
        for item in manifest["lean_support"]["files"].values():
            self.assertEqual(first.count((root/item["path"],
                {key: item[key] for key in ("bytes", "sha256")})), 1)

    def test_sdk_overrides_are_exact_and_preserve_other_rows(self):
        sdk = {name: {"path": "retained", **SAMPLE} for name in S.OVERRIDES-{S.NEW_SOURCE}}
        sdk["v5/unchanged.py"] = {"path": "unchanged", **SAMPLE}
        selected = {name: {"path": str(S.ROOT/"software/v5/runtime_efficient"/
                                     name.removeprefix("v5/")), **SAMPLE}
                    for name in S.OVERRIDES}
        with patch.object(D, "checked_json", return_value=selected), \
                patch.object(D, "absolute_pin", side_effect=lambda row:
                             {key: row[key] for key in ("bytes", "sha256")}), \
                patch.object(D, "pinned") as checked, patch.object(D, "pin", return_value={}):
            result, unused = S.replace_sdk(D, sdk, "selected.json", "ab"*32)
            self.assertEqual(result["v5/unchanged.py"], sdk["v5/unchanged.py"])
            self.assertEqual(set(result), set(sdk) | {S.NEW_SOURCE})
            self.assertEqual(checked.call_count, 4)
        for bad in ({key: row for key, row in selected.items() if key != S.NEW_SOURCE},
                    {**selected, "v5/unselected.py": deepcopy(SAMPLE)}):
            with patch.object(D, "checked_json", return_value=bad), self.assertRaisesRegex(
                    ValueError, "SELECT_EXACT_SDK_OVERRIDES"):
                S.replace_sdk(D, sdk, "selected.json", "ab"*32)


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
    output = D.ordinary(Path(sys.argv[2]), directory=True)
    D.ordinary(output/"controls.json", fresh=True)
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL",
        "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "scope": "PURE_CHANGED_COMPLETE_RUNTIME_AND_BASE_ROLE_CONTRACTS",
        "sources": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                    for name in ("distribution.py", "select_inputs.py", "test_complete.py")},
        "io_mocks": "BASE_CENSUS_PIN_DISPATCH_AND_OVERRIDE_SELECTION_ONLY",
        "native_calls": 0, "proof_calls": 0, "sdk_imports": 0}
    with (output/"controls.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

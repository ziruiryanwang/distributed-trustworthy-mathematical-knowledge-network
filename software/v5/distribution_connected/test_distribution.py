"""Focused connected-distribution boundaries; no build or mathematical run.

Reuse only a predecessor manifest helper. Ordinary-import checks copy selected
small SDK sources, never runtimes/assets or an installation. Launcher is inert.
"""
import asyncio
from copy import deepcopy
import hashlib
import importlib
import importlib.util
import inspect
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent
PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
INPUT = PROJECT/"experiments/v5-local-checks/distribution-03-input.json"
INPUT_SHA = "d71ab60ff1be199e86278fa10fe9a84a6161b822343ad90a35594d0e98a40042"
OUTPUT = None
OBSERVED = {}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


D = load("_connected_distribution", HERE/"distribution.py")
T = load("_prior_manifest_fixture_only", SOURCE/"distribution_complete/test_complete.py")
SAMPLE = {"bytes": 1, "sha256": "12"*32}
DELTAS = {
    "v5/client/workspace_evidence.py": ("client/supplier_resilient/workspace_evidence.py",
        "a7c4979c35e904f096cba23b7fcb5cb8361e4679fc16d37d2fcec69041afd5ab"),
    "v5/client/workspace_staged.py": ("staging_members/workspace_staged.py",
        "1a0922c395eb233f6fb4f1e8b10b5c538d69d445c732a9ae492539b568877f8d"),
    "v5/client/semantic_reader.py": ("client/supplier_resilient/semantic_reader.py",
        "9b82de53bdcc8db74908622fc43c965a7b003111a752a8f579d25b5964dffe60"),
    "v5/transport/acquisition_resilience.py": ("transport/acquisition_resilience.py",
        "43fa1acd66219c7d28a37a263dee04a20edd993bd24383c54680aa303202c09d"),
    "v5/client/serve_advertised.py": ("client/serve_advertised.py",
        "80d6c0746eca23398cfe735af5d8de1076eb3725439414cce68de743c518a7ed"),
}


def pin_bytes(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def manifest(role):
    catalogue, result = T.fixture()
    result.update(schema=D.RELEASE_SCHEMA, base_role=role)
    for command, raw in D.wrappers(role).items():
        result["files"]["owners/"+command+".py"] = pin_bytes(raw)
    for name in D.required_sources(role):
        result["sdk_sources"][name] = "sdk/"+name
        result["files"].setdefault("sdk/"+name, deepcopy(SAMPLE))
    if role == D.LOCATION_ROLE:
        rows = {"runtime/node/node.exe": deepcopy(SAMPLE),
                "overlay/quota_store.mjs": deepcopy(SAMPLE)}
        rows.update({"overlay/fixture/"+str(n)+".mjs": deepcopy(SAMPLE) for n in range(5894)})
        catalogue.update(rows)
        result["files"].update({"base/"+name: deepcopy(row) for name, row in rows.items()})
    return catalogue, result


class Controls(unittest.TestCase):
    def test_exact_two_role_projection_preserves_small_role_and_rejects_bad_location(self):
        value = D.checked_json(INPUT, INPUT_SHA)
        base = D.checked_json(value["base_manifest"]["path"], D.BASE_SHA)
        small = D.base_projection(base["files"], D.BASE_ROLE)
        located = D.base_projection(base["files"], D.LOCATION_ROLE)
        expected = {name: row for name, row in base["files"].items()
                    if name.startswith(("overlay/", "runtime/node/"))}
        self.assertEqual(located, {**small, **expected})
        self.assertEqual(len(small), 587)
        self.assertEqual(len(expected), 5896)
        self.assertEqual(len(located), 6483)
        self.assertFalse(any(name.startswith(("overlay/", "runtime/node/")) for name in small))
        for defect in ("node", "extra", "unknown-role"):
            bad = deepcopy(base["files"])
            if defect == "node": del bad["runtime/node/node.exe"]
            elif defect == "extra": bad["overlay/unselected-extra.mjs"] = deepcopy(SAMPLE)
            with self.subTest(defect=defect), self.assertRaises(ValueError):
                D.base_projection(bad, "arbitrary" if defect == "unknown-role" else D.LOCATION_ROLE)
        OBSERVED["role_payload_counts"] = {"small": len(small), "located": len(located),
                                           "location_added": len(expected)}

    def test_manifest_wrapper_bindings_and_required_semantic_source_closure(self):
        for role in D.BASE_ROLES:
            unused, good = manifest(role)
            D.validate_manifest(good)
            required = D.required_sources(role)
            self.assertTrue(set(DELTAS)-{"v5/client/serve_advertised.py"} <= required)
            self.assertEqual("serve-advertised" in D.wrappers(role), role == D.LOCATION_ROLE)
            for defect in ("wrapper", "extra-owner", "semantic", "staged"):
                bad = deepcopy(good)
                if defect == "wrapper": bad["files"]["owners/serve.py"]["sha256"] = "00"*32
                elif defect == "extra-owner": bad["files"]["owners/unselected.py"] = deepcopy(SAMPLE)
                else:
                    key = "v5/client/semantic_reader.py" if defect == "semantic" else "v5/client/workspace_staged.py"
                    del bad["sdk_sources"][key]
                with self.subTest(role=role, defect=defect), self.assertRaises(ValueError):
                    D.validate_manifest(bad)
        self.assertEqual(len(D.LOCATION_SOURCES), 21)
        self.assertTrue({"portable/location/"+name for name in D.LOCATION_SOURCES}
                        <= D.required_sources(D.LOCATION_ROLE))

    def test_verify_uses_selected_role_and_rejects_extra_or_missing_projected_files(self):
        for role in D.BASE_ROLES:
            catalogue, good = manifest(role)
            root = OUTPUT/("inert-"+role)
            with patch.object(D, "census"), patch.object(D, "pinned"), \
                    patch.object(D, "checked_json", return_value={"files": catalogue}):
                D._verify_release(root, good, full=False)
                for defect in ("omitted-helper", "extra-base"):
                    bad = deepcopy(good)
                    if defect == "omitted-helper": del bad["files"]["base/receiver/helpers/domains.py"]
                    else: bad["files"]["base/unselected-file"] = deepcopy(SAMPLE)
                    with self.subTest(role=role, defect=defect), self.assertRaisesRegex(
                            ValueError, "DIST_EXACT_BASE_ROLE_MAP"):
                        D._verify_release(root, bad, full=False)

    def test_builtin_dispatch_relocation_and_reserved_location_root(self):
        roots = (OUTPUT/"install-one", OUTPUT/"relocated-install")
        original = {"location": {"routes": [{"features": ["12"*32], "stripe": 0}]}}
        for root in roots:
            actual = D.builtin_parameters(root, D.LOCATION_ROLE, "serve-advertised", original)
            self.assertEqual(actual["schema"], "DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_V1")
            self.assertEqual(actual["location"]["installation_root"], str(root/"base"))
            self.assertNotIn("installation_root", original["location"])
            actual["location"]["routes"].clear()
            self.assertEqual(len(original["location"]["routes"]), 1)
        for command, schema in D.ENTRY_SCHEMAS.items():
            supplied = {"location": {}} if command == "serve-advertised" else {}
            self.assertEqual(D.builtin_parameters(roots[0], D.LOCATION_ROLE, command, supplied)["schema"], schema)
            with self.assertRaisesRegex(ValueError, "DIST_ENTRY_SCHEMA"):
                D.builtin_parameters(roots[0], D.LOCATION_ROLE, command, {**supplied, "schema": "wrong"})
        with self.assertRaisesRegex(ValueError, "DIST_COMMAND_NOT_IN_BASE_ROLE"):
            D.builtin_parameters(roots[0], D.BASE_ROLE, "serve-advertised", original)
        with self.assertRaisesRegex(ValueError, "DIST_INSTALLED_LOCATION_ROOT_RESERVED"):
            D.builtin_parameters(roots[0], D.LOCATION_ROLE, "serve-advertised",
                {"location": {"installation_root": str(roots[0]/"base")}})

    def launch_fixture(self, role, command, *, mode=None):
        unused, selected = manifest(role)
        root = OUTPUT/(role+"-"+command+"-installation")
        work = OUTPUT/(role+"-"+command+"-work")
        work.mkdir()
        raw = b'import sys\ndef main():\n return {"ns": STARTED_NS, "cpu": STARTED_CPU, "argv": list(sys.argv)}\n'
        selected["files"]["sdk/v5/client/launch.py"] = pin_bytes(raw)
        request = {"schema": D.REQUEST_SCHEMA, "name": "selected", "workspace_root": str(work),
            "parameters": {"location": {}} if command == "serve-advertised" else {},
            "limits": {}, "output_limits": {}, "owner": None, "runtime_mode": mode}
        return root, work, raw, selected, request

    def test_serving_launch_uses_no_math_profile_and_preserves_original_clock(self):
        for command in D.SERVING:
            root, work, raw, selected, request = self.launch_fixture(D.LOCATION_ROLE, command)
            with patch.object(D, "__file__", str(root/"distribution.py")), \
                    patch.object(D, "ordinary", side_effect=lambda value, **options: Path(value)), \
                    patch.object(D, "checked_json", side_effect=[selected, request]), \
                    patch.object(D, "verify_release"), patch.object(D, "pinned"), \
                    patch.object(D, "read", return_value=raw), \
                    patch.object(D, "materialize", side_effect=AssertionError("NO_MATH_PROFILE")), \
                    patch.object(sys, "executable", str(root/"base/receiver/runtime/python/python.exe")), \
                    patch.object(sys, "argv", list(sys.argv)):
                answer = D._launch("ab"*32, command, work/"owner-request.json", "cd"*32)
            self.assertEqual((answer["ns"], answer["cpu"]), (D.STARTED_NS, D.STARTED_CPU))
            control = work/"selected-request"
            self.assertFalse((control/"preparation.json").exists())
            plan = json.loads((control/"launch.json").read_bytes())
            self.assertEqual(plan["owner_entry"], command+".py")
            self.assertEqual(plan["parameters"]["schema"], D.ENTRY_SCHEMAS[command])
            self.assertEqual(plan["installation_root"], str(root/"base"))
            self.assertNotIn("runtime_adoption", plan["parameters"])
            if command == "serve-advertised":
                self.assertEqual(plan["parameters"]["location"]["installation_root"], str(root/"base"))
        sys.modules.pop("_dmkn_installed_client_launch", None)

    def test_node_free_launch_refuses_before_controls_or_delegate(self):
        root, work, unused, selected, request = self.launch_fixture(D.BASE_ROLE, "serve-advertised")
        with patch.object(D, "__file__", str(root/"distribution.py")), \
                patch.object(D, "ordinary", side_effect=lambda value, **options: Path(value)), \
                patch.object(D, "checked_json", side_effect=[selected, request]), \
                patch.object(D, "verify_release"), \
                patch.object(D, "write_new", side_effect=AssertionError("NO_CONTROL_WRITES")) as writes, \
                patch.object(sys, "executable", str(root/"base/receiver/runtime/python/python.exe")), \
                self.assertRaisesRegex(ValueError, "DIST_COMMAND_NOT_IN_BASE_ROLE"):
            D._launch("ab"*32, "serve-advertised", work/"owner-request.json", "cd"*32)
        self.assertFalse(writes.called)
        self.assertFalse((work/"selected-request").exists())

    def test_serving_non_null_math_runtime_refuses_before_outputs(self):
        root, work, unused, selected, request = self.launch_fixture(D.BASE_ROLE, "serve", mode="aggregate")
        with patch.object(D, "__file__", str(root/"distribution.py")), \
                patch.object(D, "ordinary", side_effect=lambda value, **options: Path(value)), \
                patch.object(D, "checked_json", side_effect=[selected, request]), \
                patch.object(D, "verify_release"), \
                patch.object(D, "write_new", side_effect=AssertionError("NO_CONTROL_WRITES")) as writes, \
                patch.object(sys, "executable", str(root/"base/receiver/runtime/python/python.exe")), \
                self.assertRaisesRegex(ValueError, "DIST_SERVICE_NO_RUNTIME_OWNER"):
            D._launch("ab"*32, "serve", work/"owner-request.json", "cd"*32)
        self.assertFalse(writes.called)
        self.assertFalse((work/"selected-request").exists())

    def test_exact_five_sdk_aliases_import_ordinary_connected_interfaces(self):
        value = D.checked_json(INPUT, INPUT_SHA)
        selected = deepcopy(value["sdk_sources"])
        self.assertEqual(len(selected), 103)
        for logical, (relative, expected) in DELTAS.items():
            path = SOURCE/relative
            row = D.pin(path)
            self.assertEqual(row["sha256"], expected)
            selected[logical] = row
        self.assertEqual(len(selected), 106)
        self.assertEqual(sum(key.startswith("v5/") and key.endswith(".py") for key in selected), 85)
        self.assertTrue(D.required_sources(D.LOCATION_ROLE) <= set(selected))
        for key, row in value["sdk_sources"].items():
            if key not in DELTAS: self.assertEqual(selected[key], row)
        view = OUTPUT/"ordinary-sdk-only"
        view.mkdir()
        total = 0
        for key, row in selected.items():
            self.assertLessEqual(row["bytes"], 2*D.MIB)
            total += row["bytes"]
            self.assertLessEqual(total, 4*D.MIB)
            source_path = Path(row["path"])
            original_root = PROJECT/"software/v5"
            if source_path.is_relative_to(original_root):
                source_path = SOURCE/source_path.relative_to(original_root)
            self.assertTrue(source_path.is_relative_to(SOURCE))
            D.copy_pinned(source_path, view.joinpath(*D.relative(key)),
                          {name: row[name] for name in ("bytes", "sha256")})
        namespaces = {key.split("/")[1] for key in selected if key.endswith(".py")}
        self.assertFalse(any(name.split(".")[0] in namespaces for name in sys.modules))
        old_path = list(sys.path)
        try:
            sys.path[:0] = [str(view/"portable"), str(view/"v5")]
            V = importlib.import_module("client.workspace_validated")
            E = importlib.import_module("client.workspace_evidence")
            S = importlib.import_module("client.workspace_staged")
            H = importlib.import_module("client.semantic_reader")
            A = importlib.import_module("transport.acquisition_resilience")
            self.assertIs(V.CommonsClient.try_acquire_body, E.CommonsClient.try_acquire_body)
            self.assertIs(V.CommonsClient.preview_context, S.CommonsClient.preview_context)
            self.assertIn("selected_members", inspect.signature(S.CommonsClient.preview_context).parameters)
            self.assertIs(H.CommonsClient, V.CommonsClient)
            self.assertTrue(callable(H.SemanticReader.try_fetch_body))
            self.assertIs(E.AR, A)
            for command, raw in D.wrappers(D.LOCATION_ROLE).items():
                owner = {}
                exec(compile(raw, "inert-owner-"+command, "exec"), owner)
                self.assertTrue(callable(owner["main"]))
            observed = {}
            for name, module in tuple(sys.modules.items()):
                if name.split(".")[0] not in namespaces or not getattr(module, "__file__", None):
                    continue
                path = Path(module.__file__).resolve()
                self.assertTrue(path.is_relative_to(view), (name, str(path)))
                logical = path.relative_to(view).as_posix()
                self.assertIn(logical, selected)
                self.assertEqual(pin_bytes(path.read_bytes()),
                                 {key: selected[logical][key] for key in ("bytes", "sha256")})
                observed[name] = logical
            OBSERVED["sdk"] = {"files": len(selected), "bytes": total, "imports": observed,
                               "logical_deltas": {key: row[1] for key, row in DELTAS.items()}}
        finally:
            sys.path[:] = old_path
            for name in tuple(sys.modules):
                if name.split(".")[0] in namespaces: sys.modules.pop(name, None)


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output": raise ValueError("OUTPUT_REQUIRED")
    D.need(Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
           and sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_CANONICAL_CONTROLS")
    OUTPUT = D.ordinary(Path(sys.argv[2]), directory=True)
    D.need(OUTPUT.is_relative_to(PROJECT/"experiments"), "CONTROLS_OUTPUT_SCOPE")
    with patch.object(subprocess, "Popen", side_effect=AssertionError("PROCESS_FORBIDDEN")), \
            patch.object(asyncio, "create_subprocess_exec", side_effect=AssertionError("PROCESS_FORBIDDEN")), \
            patch.object(asyncio, "open_connection", side_effect=AssertionError("NETWORK_FORBIDDEN")), \
            patch.object(asyncio, "start_server", side_effect=AssertionError("NETWORK_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "scope": "CONNECTED_ROLE_DISPATCH_AND_ORDINARY_SOURCE_IMPORTS_NO_INSTALL_OR_MATHEMATICS",
        "observed": OBSERVED, "native_calls": 0, "proof_calls": 0, "network_calls": 0,
        "installation_builds": 0, "mathematical_acceptance": False,
        "sources": {name: pin_bytes((HERE/name).read_bytes()) for name in
                    ("distribution.py", "test_distribution.py")}}
    with (OUTPUT/"controls-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

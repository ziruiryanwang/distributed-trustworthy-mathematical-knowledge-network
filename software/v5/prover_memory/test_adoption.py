"""Seven inert controls for the allocation-refined adoption seam only.

The synthetic fixture substitutes the descriptor trust anchor, not validation
logic. Its compiler outputs, runtime inventory and accounting are NOT genuine
build evidence. No compiler, native process, proof or predecessor suite runs.
"""
from copy import deepcopy
import argparse
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE))
from prover_memory import adoption as A, producer as R
from aggregate_small import producer as S
from aggregate_lifecycle import producer as L
from production import producer as P

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OUTPUT = None


def content(raw):
    return {"bytes": len(raw), "sha256": P.hash_bytes(raw)}


def save(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
    return {"path": str(path), **content(raw)}


def stats(cpu=0):
    return {"cpu_seconds": cpu, "user_cpu_seconds": cpu, "kernel_cpu_seconds": 0,
        "active_processes": 0, "total_processes": int(cpu != 0),
        "terminated_processes": 0, "peak_job_private_commit_bytes": int(cpu != 0)*4096}


class InertSupport:
    def __init__(self):
        self.closed = False

    def absolute(self, value):
        path = Path(value)
        P.require(path.is_absolute() and path.resolve() == path and path.is_file()
                  and not path.is_symlink(), "SYNTHETIC_ORDINARY_FILE")
        return path

    def _check(self, pins):
        for path, pin in pins.items():
            self.absolute(path)
            P.require(P.file_pin(Path(path)) == pin, "SYNTHETIC_INPUT_PIN_CHANGED")

    def _read(self, pin, maximum):
        P.pin_fields(pin, maximum); self._check({pin["path"]: pin})
        with Path(pin["path"]).open("rb") as stream:
            raw = stream.read(maximum+1)
        P.require(len(raw) <= maximum, "SYNTHETIC_READ_BOUND")
        return raw

    def close(self):
        self.closed = True


class Fixture:
    """Small actual files; fake compile records and fake unscanned toolchain map."""
    def __init__(self, name, change=None):
        self.root = OUTPUT/name/"prover-allocation-build-00"
        self.files = {}
        fake = b"SYNTHETIC-NOT-EXECUTABLE\n"
        patch_relative = "software/v5/prover_memory/preflight.patch"
        preflight = "risc0/circuit/rv32im/src/prove/preflight.rs"
        self.files["source/sdk/"+preflight] = fake+b"PATCHED\n"
        runtime = {str(self.root.parent/("absent-runtime-"+str(i))): "00"*32 for i in range(1071)}
        old_root = PROJECT/"retained/small-aggregate-stage-host-build-01"
        old_env = {"explicit_environment": {"PATH": "SYNTHETIC-NO-TOOLS",
            "OUT_DIR": str(old_root/"generated"), "CARGO_PKG_NAME": "old",
            "CARGO_MANIFEST_DIR": str(old_root), "CARGO_MANIFEST_PATH": str(old_root/"Cargo.toml")},
            "host_binaries": {"synthetic": "00"*32}}
        retained = []
        rows = [("retained/small-aggregate-stage-host-build-01/environment-profile.json", P.encoded(old_env)),
            ("retained/small-aggregate-stage-host-build-01/selection.json", P.encoded({"runtime_pins": runtime})),
            ("retained/proof-validation-integration-build-01/source-map.json", P.encoded({"library.rs": content(fake)})),
            ("retained/small-aggregate-stage-host-build-01/source-map.json", P.encoded({"stage.rs": content(fake)})),
            ("retained/generated/preflight_opt_gen.rs", fake), ("retained/empty/output", b"")]
        for index, (relative, raw) in enumerate(rows):
            retained.append({"path": relative, **content(raw)})
            evidence = "source/evidence/"+str(index).zfill(2)+"-"+Path(relative).name
            self.files[evidence] = raw
            if not raw:
                self.empty = self.root/evidence
        self.files.update({"source/integration/library.rs": fake, "source/stage/stage.rs": fake,
                           "generated/rv32im/preflight_opt_gen.rs": fake})
        steps = []
        for index, name in enumerate(A.NAMES):
            dependencies = list(A.NAMES[max(0, index-1):index])
            steps.append({"name": name, "argv_template": ["SYNTHETIC-NOT-A-COMPILER", name,
                *[d+"=${RUN}\\lib\\"+d+".fake" for d in dependencies]],
                "output_template": "${RUN}\\lib\\"+name+".fake", "depends_on": dependencies,
                "environment_overlay": {"OUT_DIR": "${RUN}/generated", "CARGO_PKG_NAME": name}})
        preserved = {"aggregate_image": "aa"*32, "individual_image": "bb"*32,
                     "foundation": "cc"*32, "policy": "dd"*32}
        descriptor = {"canonical_root": str(PROJECT), "source": {"path": "retained/sdk/"+preflight},
            "preserved": preserved, "patch": {"path": patch_relative, **content(fake)},
            "expected_patched": content(self.files["source/sdk/"+preflight]),
            "sdk_source_inventories": [{"files": [{"path": preflight, **content(fake)}]}],
            "retained_records": retained, "compiler_recipe": {"ordered_steps": steps}}
        for relative in A.ADAPTERS:
            self.files["source/adapters/"+relative] = P.encoded(descriptor) if relative.endswith("SOURCE.json") else fake
        self.descriptor_sha = P.hash_bytes(P.encoded(descriptor))
        adapters = {k: content(self.files["source/adapters/"+k]) for k in A.ADAPTERS}
        source_map = {"adapters": adapters, "files": {k: content(v) for k,v in self.files.items()}}
        selected = {"schema": A.SCHEMA+"_V1", "name": self.root.name,
            "authorizes_compile_only": True, "sources": adapters,
            "runtime_pins": runtime, "limits": dict(A.LIMITS)}
        commands = [{"name": s["name"], "argv": [v.replace("${RUN}", str(self.root))
                     for v in s["argv_template"]]} for s in steps]
        base_env = {k: v.replace(str(old_root), str(self.root)) for k,v in old_env["explicit_environment"].items()}
        base_env.update(VCToolsUserTelemetryOptOut="1", CARGO_NET_OFFLINE="true")
        step_env = {}
        for step in steps:
            env = {k:v for k,v in base_env.items() if k != "OUT_DIR" and not k.startswith("CARGO_PKG_")
                   and k not in ("CARGO_MANIFEST_DIR", "CARGO_MANIFEST_PATH")}
            env.update({k:v.replace("${RUN}", str(self.root)) for k,v in step["environment_overlay"].items()})
            step_env[step["name"]] = env
        environment = {"explicit_environment": base_env, "step_environments": step_env,
            "environment_keys_only": sorted(base_env), "no_inherited_environment": True,
            "host_binaries": old_env["host_binaries"]}
        input_map = {"source_inputs": {}, "runtime_pins": deepcopy(runtime), "helper_pins": {},
                     "trust_boundary": "SYNTHETIC-NOT-A-TOOLCHAIN"}
        outputs = {s["name"]: {"path": s["output_template"].replace("${RUN}", str(self.root)),
                   **content(fake)} for s in steps}
        actual = [{"argv": c["argv"], "cwd": str(PROJECT), "label": c["name"],
            "status": "COMMAND_COMPLETED", "exit_code": 0, "cleanup_errors": [],
            "job_before": stats(), "job_after": stats(1), "inclusive_cpu_delta": 1,
            "wall_seconds": 1} for c in deepcopy(commands)]
        total = stats(5); total["total_processes"] = 5
        total["phase_jobs"] = [{"name": n, "stats": stats(1)} for n in A.NAMES]
        result = dict.fromkeys(A.RESULT_FIELDS)
        result.update(schema=A.SCHEMA+"_RESULT_V1", status=A.PASS, descriptor_sha256=self.descriptor_sha,
            patch_sha256=content(fake)["sha256"], limits=dict(A.LIMITS), runtime_pin_count=1071,
            runtime_pin_bytes=2320491997, authority="SYNTHETIC_NOT_BUILD_OR_MATHEMATICS",
            outputs=outputs, executable=outputs[A.NAMES[-1]], job=total, commands=actual,
            controller_cpu_seconds=1, wall_seconds=5, output_census={"working_bytes": 1, "entries": 1},
            sampled_peaks={"working_bytes": 1, "entries": 1}, accounting="SYNTHETIC_NOT_MEASURED", **A.COUNTS)
        self.records = {"result": result, "selection": selected, "source_map": source_map,
                        "command": commands, "environment": environment, "input_map": input_map}
        if change:
            change(self)
        for relative, raw in self.files.items():
            save(self.root/relative, raw)
        for pin in outputs.values():
            save(Path(pin["path"]), fake)
        pins = {}
        for role, filename in (("selection", "selection.json"), ("source_map", "source-map.json"),
                               ("command", "compile-commands.json")):
            pins[role] = save(self.root/filename, P.encoded(self.records[role]))
        for role, field, filename in (("environment", "environment_sha256", "environment-profile.json"),
                                     ("input_map", "input_map_sha256", "INPUT-MAP.json")):
            result[field] = save(self.root/filename, P.encoded(self.records[role]))["sha256"]
        result.update(selection_sha256=pins["selection"]["sha256"],
                      source_map_sha256=pins["source_map"]["sha256"], commands_sha256=pins["command"]["sha256"])
        pins["result"] = save(self.root/"RESULT.json", P.encoded(result))
        pins["attempt"] = save(self.root.parent/(self.root.name+"-attempt.json"),
                               P.encoded({"status": A.PASS, "result_sha256": pins["result"]["sha256"]}))
        self.pins, self.preserved = pins, preserved

    def owner(self, kind=R.RefinedAggregateProducer, change_runtime=None):
        owner = object.__new__(kind)
        runtime = [P.file_pin(p) for p in R.required_source_paths()]
        if change_runtime:
            change_runtime(runtime)
        owner.profile = {"relation_image": self.preserved["individual_image"], "support_profile": {
            "image_id": self.preserved["aggregate_image"], "foundation": self.preserved["foundation"],
            "policy": self.preserved["policy"], "runtime_pins": runtime}}
        owner._raw = P.encoded(owner.profile)
        owner._pins = {}; owner._support = InertSupport(); owner._A = owner._support
        owner._closed = False; owner._lifecycle_ready = False
        return owner

    def adopt(self, owner=None):
        owner = self.owner() if owner is None else owner
        table = {}
        with patch.object(A, "SOURCE_SHA", self.descriptor_sha):
            pin = owner._adopt_host_build(self.pins, table, "stage")
        return owner, table, pin


class AdoptionControls(unittest.TestCase):
    def test_exact_build_and_both_refined_stage_hooks(self):
        reviewed = SOURCE/"prover_memory/SOURCE.json"
        self.assertEqual(P.file_pin(reviewed)["sha256"], A.SOURCE_SHA)
        descriptor = P.parse(reviewed.read_bytes())
        self.assertEqual(tuple(s["name"] for s in descriptor["compiler_recipe"]["ordered_steps"]), A.NAMES)
        fixture = Fixture("positive")
        for kind in (R.RefinedAggregateProducer, R.RefinedLifecycleProducer):
            with self.subTest(owner=kind.__name__):
                owner, table, pin = fixture.adopt(fixture.owner(kind))
                self.assertEqual(pin, fixture.records["result"]["outputs"][A.NAMES[-1]])
                self.assertTrue(set(R.required_source_paths()) <= {Path(p) for p in table})
                self.assertEqual(owner._refinement_empty_evidence, (fixture.empty,))
                owner._check(table)

    def rejected(self, name, change, reason):
        with self.subTest(case=name):
            with self.assertRaisesRegex(ValueError, reason):
                Fixture(name, change).adopt()

    def test_scope_limits_and_exact_five_commands(self):
        self.rejected("limit", lambda f: f.records["selection"]["limits"].update(
            memory_mib=A.LIMITS["memory_mib"]+1), "REFINEMENT_BUILD_SCOPE")
        self.rejected("count", lambda f: f.records["result"].update(backend_rust_crate_rebuilds=0),
                      "REFINEMENT_REBUILD_COUNTS")
        self.rejected("four", lambda f: f.records["result"]["commands"].pop(), "REFINEMENT_EXACT_FIVE_COMMANDS")
        self.rejected("command-edge", lambda f: f.records["command"][1]["argv"].__setitem__(
            -1, "risc0_circuit_rv32im=SYNTHETIC-OLD-LIBRARY"), "REFINEMENT_EXACT_FIVE_COMMANDS")

    def test_exact_sources_and_empty_evidence_rebinding(self):
        self.rejected("omitted-source", lambda f: f.records["source_map"]["files"].pop(
            "source/integration/library.rs"), "REFINEMENT_EXACT_DERIVED_SOURCE_MAP")
        self.rejected("traversal", lambda f: f.records["source_map"]["files"].update(
            {"source/../escape": content(b"x")}), "REFINEMENT_RELATIVE_PATH")
        self.rejected("empty-code", lambda f: f.records["source_map"]["files"].update(
            {"source/sdk/empty.rs": content(b"")}), "REFINEMENT_EMPTY_EVIDENCE_ONLY")
        fixture = Fixture("empty-rebind"); owner, table, unused = fixture.adopt()
        with fixture.empty.open("ab") as stream:
            stream.write(b"MUTATED-SYNTHETIC-EVIDENCE")
        with self.assertRaisesRegex(ValueError, "REFINEMENT_EMPTY_EVIDENCE_CHANGED"):
            owner._check(table)

    def test_compiler_environment_and_retained_runtime_identity(self):
        self.rejected("environment", lambda f: f.records["environment"].update(no_inherited_environment=False),
                      "REFINEMENT_EXACT_COMPILER_ENVIRONMENTS")
        self.rejected("runtime", lambda f: f.records["input_map"]["runtime_pins"].pop(
            next(iter(f.records["input_map"]["runtime_pins"]))), "REFINEMENT_EXACT_RETAINED_RUNTIME_MAP")

    def test_serial_job_closure_accounting_and_phase_limits(self):
        self.rejected("live-job", lambda f: f.records["result"]["commands"][0]["job_after"].update(
            active_processes=1), "REFINEMENT_BUILD_JOB_CLOSURE")
        self.rejected("phase-limit", lambda f: f.records["result"]["commands"][0].update(
            wall_seconds=A.LIMITS["worker_wall_seconds"]+1), "REFINEMENT_PHASE_LIMITS")
        self.rejected("job-sum", lambda f: f.records["result"]["job"].update(cpu_seconds=4),
                      "REFINEMENT_EXACT_JOB_TOTALS")
        self.rejected("serial-peak", lambda f: f.records["result"]["job"].update(
            peak_job_private_commit_bytes=20480), "REFINEMENT_SERIAL_JOB_PEAK")

    def test_complete_support_closure_missing_duplicate_digest_and_origin(self):
        fixture = Fixture("source-closure")
        inherited = Path(L.__file__).resolve()
        def omit(rows):
            rows[:] = [p for p in rows if Path(p["path"]) != inherited]
        for name, change, reason in (
            ("missing-inherited", omit, "REFINEMENT_SOURCE_NOT_SELECTED"),
            ("duplicate", lambda rows: rows.append(dict(rows[0])), "REFINEMENT_DUPLICATE_RUNTIME_PIN"),
            ("wrong-digest", lambda rows: rows[0].update(sha256="00"*32), "SYNTHETIC_INPUT_PIN_CHANGED")):
            with self.subTest(case=name):
                with self.assertRaisesRegex(ValueError, reason):
                    fixture.adopt(fixture.owner(change_runtime=change))
        with patch.object(A, "__file__", str(fixture.root/"foreign-adoption.py")):
            with self.assertRaisesRegex(ValueError, "REFINEMENT_SOURCE_ORIGIN:prover_memory.adoption"):
                R.required_source_paths()

    def test_nonstage_delegation_and_failed_constructor_cleanup(self):
        fixture = Fixture("delegation"); owner = fixture.owner()
        with patch.object(S.AggregateProducer, "_adopt_host_build", return_value="INERT-SNAPSHOT") as inherited, \
             patch.object(R, "adopt_build", side_effect=AssertionError("STAGE_ADOPTER_MUST_NOT_RUN")):
            self.assertEqual(owner._adopt_host_build({}, {}, "snapshot"), "INERT-SNAPSHOT")
            inherited.assert_called_once_with({}, {}, "snapshot")
        for kind, base in ((R.RefinedAggregateProducer, S.AggregateProducer),
                           (R.RefinedLifecycleProducer, L.LifecycleProducer)):
            support = InertSupport(); allocated = object.__new__(kind)
            def fail(instance, profile):
                instance._support = support
                raise ValueError("SYNTHETIC_CONSTRUCTOR_REFUSAL")
            with self.subTest(owner=kind.__name__), patch.object(base, "__init__", fail):
                with self.assertRaisesRegex(ValueError, "SYNTHETIC_CONSTRUCTOR_REFUSAL"):
                    kind.__init__(allocated, {})
                self.assertTrue(support.closed and allocated._closed)


def main():
    global OUTPUT
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True)
    OUTPUT = Path(parser.parse_args().output)
    P.require(Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
              and sys.dont_write_bytecode and not sys.flags.optimize, "CANONICAL_ISOLATED_CONTROLS")
    P.require(OUTPUT.is_absolute() and OUTPUT.resolve() == OUTPUT and OUTPUT.is_relative_to(PROJECT/"experiments")
              and not OUTPUT.exists() and OUTPUT.parent.is_dir(), "FRESH_CONTROL_OUTPUT")
    OUTPUT.mkdir()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AdoptionControls)
    P.require(suite.countTestCases() == 7, "EXACT_SEVEN_ADOPTION_CONTROLS")
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_PROCESS_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    imports = []
    for name, module in sorted(sys.modules.items()):
        location = getattr(module, "__file__", None)
        if location and Path(location).is_relative_to(SOURCE):
            imports.append({"name": name, **P.file_pin(Path(location))})
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skips": len(result.skipped),
        "scope": "SYNTHETIC_ADOPTION_ONLY_NO_COMPILER_NATIVE_GUEST_PROOF_OR_NETWORK",
        "trust_anchor_substitution": "Synthetic descriptor only; real descriptor hash separately checked",
        "reviewed_descriptor": P.file_pin(SOURCE/"prover_memory/SOURCE.json"),
        "native_process_calls": 0, "imports": imports}
    save(OUTPUT/"RESULT.json", P.encoded(report)); print(P.encoded(report).decode(), end="", flush=True)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

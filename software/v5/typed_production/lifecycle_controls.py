"""Finite entry-boundary controls; all producer/authority seams are inert.

Only the selected stdlib-first entry is imported. Small fresh local files exercise
its pin/selection/report boundary; no producer module, snapshot, native checker,
proof, database, network or genuine production request is opened.
"""
import argparse
from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SELECTED = ("test_01_preimport_refusals", "test_02_snapshot_selection_binding",
            "test_03_actions_are_separate", "test_04_owner_failure_closure",
            "test_05_finalization_failure_overrides")
FORBIDDEN, OBSERVED = [], {}
CASE = 0


def need(ok, why):
    if not ok:
        raise AssertionError(why)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def save(path, value):
    raw = value if type(value) is bytes else encoded(value)
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "CONTROL_WRITE")
    return pin(path)


def fields(value, expected):
    need(type(value) is dict and set(value) == set(expected), "INERT_FIELDS")


def declared(*values):
    result, pending = {}, list(values)
    while pending:
        value = pending.pop()
        if type(value) is dict:
            if set(value) == {"path", "bytes", "sha256"}:
                need(value["path"] not in result or result[value["path"]] == value, "INERT_PIN_CONFLICT")
                result[value["path"]] = value
            else:
                pending.extend(value.values())
        elif type(value) is list:
            pending.extend(value)
    return result


def forbidden(*args, **kwargs):
    FORBIDDEN.append("FORBIDDEN_PRODUCER_OR_EXTERNAL_CALL")
    raise AssertionError(FORBIDDEN[-1])


def new_case():
    global CASE
    CASE += 1
    result = OUTPUT/("case-"+str(CASE))
    result.mkdir()
    return result


class Fixture:
    """Real small-file boundary with explicit fake owner and configuration data."""
    def __init__(self, action="request", fault=None, selection_fault=None):
        self.root, self.action, self.fault = new_case(), action, fault
        self.events, self.closed, self.report_saved = [], False, False
        self.output = self.root/"future-output"
        self.request_output, self.report_path = self.root/"request-output.json", self.root/"owner.json"
        self.source_root, self.install = self.root/"stable", self.root/"installation"
        self.source_root.mkdir(); self.install.mkdir()
        self.profile = dict(base_profile=dict(support_profile=dict(
            supervisor_manifest=save(self.install/"manifest.json", {"INERT": True}))))
        profile_pin = save(self.root/"profile.json", self.profile)
        self.snapshot = self.root/"sources"; self.snapshot.mkdir()
        entry_pin = save(self.snapshot/"entry.py", b"# INERT selected entry identity\n")
        self.invocation = ["INERT-PYTHON", "INERT-ENTRY"]
        if action == "snapshot":
            packet = save(self.root/"packet.bin", b"INERT-PACKET")
            self.value = dict(schema="INERT_SNAPSHOT_CONFIG", profile_id="INERT-PROFILE",
                profile_document=profile_pin, packet=packet, target_journal="00"*184,
                envelope=dict(packet_bytes=1024), cycles=1, po2=18, diagnostic_mode="stats",
                limits={"INERT": True}, output_directory=str(self.output))
        else:
            evidence = {name: save(self.root/(name+".json"), {"INERT": name})
                        for name in ("result", "outer", "selection", "configuration", "command")}
            self.value = dict(schema=ENTRY.REQUEST_SCHEMA, snapshot_evidence=evidence,
                allowance_id="INERT-NOT-FUNDING", budget={"INERT": True}, checkpoints=[], prior_attempts=[],
                output_directory=str(self.output), stage_limit=1, carried_external_costs={"INERT": True},
                request_output=str(self.request_output))
        input_pin = save(self.root/"input.json", self.value)
        self.boot = SimpleNamespace(source_root=self.source_root, entry_pin=entry_pin,
            profile=self.profile, profile_pin=profile_pin,
            pins={row["path"]: row for row in (entry_pin, profile_pin)}, invocation=self.invocation)
        self.selection_path = self.root/"selection.json"
        if action == "snapshot":
            selection = dict(schema="DMKN_V5_LOCAL_CHECK_V1", name=self.root.name,
                sources={"entry.py": entry_pin["sha256"]},
                runtime_pins={input_pin["path"]: input_pin["sha256"], profile_pin["path"]: profile_pin["sha256"]},
                argv=list(self.invocation), limits={"INERT": True})
            if selection_fault == "argv": selection["argv"].append("wrong")
            if selection_fault == "source": selection["sources"]["entry.py"] = "00"*32
            if selection_fault == "name": selection["name"] = "wrong"
            save(self.selection_path, selection)
        self.input_pin = input_pin
        self.argv = [action, "--source-root", str(self.source_root), "--entry-sha256", entry_pin["sha256"],
            "--profile", profile_pin["path"], "--profile-sha256", profile_pin["sha256"],
            "--input", input_pin["path"], "--input-sha256", input_pin["sha256"],
            "--owner-report", str(self.report_path)]
        if action == "snapshot": self.argv += ["--outer-selection", str(self.selection_path)]
        fixture = self

        def separate(outputs, protected):
            for output in outputs:
                for value in protected:
                    other = Path(value)
                    need(not (output.is_relative_to(other) or other.is_relative_to(output)), "INERT_OVERLAP")

        def rebind(rows):
            if (fault == "rebind" and fixture.closed) or (fault == "late-rebind" and fixture.report_saved):
                raise ValueError("INERT_REBIND_FAILURE")
            for row in rows.values(): ENTRY._read_pin(row)

        def save_new(path, value, maximum):
            need(len(encoded(value)) <= maximum, "INERT_SAVE_BOUND")
            ENTRY._ordinary(path, fresh=True)
            if fault == "save-report" and path == fixture.report_path:
                raise ValueError("INERT_REPORT_SAVE_FAILURE")
            fixture.events.append("save-report" if path == fixture.report_path else "save-other")
            result = save(path, value)
            if path == fixture.report_path: fixture.report_saved = True
            return result

        class Owner:
            def __init__(self, selected):
                fixture.events.append("construct")
                if fault == "constructor": raise ValueError("INERT_CONSTRUCTOR_FAILURE")
                need(selected == fixture.profile, "INERT_PROFILE")
                self.profile_id, self._pins, self._install = "INERT-PROFILE", {}, fixture.install
            def _read(self, row, maximum): return ENTRY._read_pin(row, maximum)
            def prepare(self, raw, target, *, envelope):
                fixture.events.append("prepare")
                need(raw == b"INERT-PACKET" and target == b"\0"*184, "INERT_PREPARE_ARGUMENTS")
                return "INERT-PREPARED"
            def snapshot(self, prepared, **kwargs):
                fixture.events.append("snapshot")
                need(prepared == "INERT-PREPARED" and kwargs["configuration"] == input_pin
                    and kwargs["selection"] == pin(fixture.selection_path), "INERT_SNAPSHOT_ARGUMENTS")
                if fault == "work": raise ValueError("INERT_WORK_FAILURE")
                fixture.output.mkdir()
                result = dict(status="INERT_SNAPSHOT_PASS", host_calls_attempted=0,
                              session={"INERT": True}, mathematical_admission=False)
                save(fixture.output/"RESULT.json", result)
                return result
            def production_request(self, evidence, **kwargs):
                fixture.events.append("request")
                need(evidence == fixture.value["snapshot_evidence"] and kwargs == {name: fixture.value[name]
                    for name in ("allowance_id", "budget", "checkpoints", "prior_attempts", "output_directory",
                                 "stage_limit", "carried_external_costs")}, "INERT_REQUEST_ARGUMENTS")
                if fault == "work": raise ValueError("INERT_WORK_FAILURE")
                if fault == "created-output": fixture.output.mkdir()
                return dict(schema="INERT-NOT-A-PRODUCTION-REQUEST", output_directory=str(fixture.output))
            def close(self):
                fixture.events.append("close"); fixture.closed = True
                if fault == "close": raise ValueError("INERT_CLOSE_FAILURE")
            def report(self): return dict(closed=fixture.closed, scope="INERT_OWNER")
            run = preflight = forbidden

        class Envelope:
            def __init__(self, packet_bytes): self.packet_bytes = packet_bytes
            def validate(self): need(self.packet_bytes == 1024, "INERT_ENVELOPE")

        def result_shape(actual, profile):
            need(actual["status"] == "INERT_SNAPSHOT_PASS" and profile == "INERT-PROFILE", "INERT_RESULT_SHAPE")

        self.boot.O = SimpleNamespace(ordinary=ENTRY._ordinary, document=ENTRY._pin_document,
            declared_pins=declared, separate=separate, rebind=rebind, save_new=save_new)
        self.boot.P = SimpleNamespace(fields=fields, require=need, encoded=encoded,
            hash_bytes=lambda raw: hashlib.sha256(raw).hexdigest(), file_pin=pin,
            pin_fields=lambda row, maximum: Path(row["path"]))
        self.boot.T = SimpleNamespace(TypedLifecycleProducer=Owner)
        self.boot.N = SimpleNamespace(CONFIG_SCHEMA="INERT_SNAPSHOT_CONFIG", result_shape=result_shape,
            EVIDENCE_FIELDS=("result", "outer", "selection", "configuration", "command"))
        self.boot.Envelope = Envelope

    def run(self):
        stdout = io.StringIO()
        with patch.object(ENTRY, "_bootstrap", return_value=self.boot), redirect_stdout(stdout):
            code = ENTRY.main(self.argv)
        result = json.loads(stdout.getvalue())
        need(not FORBIDDEN, "NO_FORBIDDEN_CALLS")
        return code, result


class Controls(unittest.TestCase):
    def test_01_preimport_refusals(self):
        with patch.object(ENTRY, "import_module", forbidden):
            args = SimpleNamespace(entry_sha256="00"*32)
            with self.assertRaisesRegex(ValueError, "LIFECYCLE_ENTRY_PIN_CHANGED"):
                ENTRY._bootstrap(args)
            root = new_case(); stable = root/"stable"; stable.mkdir()
            rows = []
            for name in ENTRY.IMPORT_MODULES:
                path = ENTRY._module_path(stable, name); path.parent.mkdir(parents=True, exist_ok=True)
                rows.append(save(path, b"# INERT; never imported\n"))
            profile = dict(schema="DMKN_TYPED_AGGREGATE_LIFECYCLE_PROFILE_V1", source_pins=rows[:-1],
                base_profile=dict(support_profile=dict(runtime_pins=rows)), snapshot_host_build={})
            profile_pin = save(root/"profile.json", profile)
            args = SimpleNamespace(entry_sha256=ENTRY_SHA, source_root=str(stable),
                profile=profile_pin["path"], profile_sha256=profile_pin["sha256"])
            with patch.dict(sys.modules, {"typed_production": SimpleNamespace(INERT=True)}):
                with self.assertRaisesRegex(ValueError, "LIFECYCLE_ENTRY_PRELOADED_PRODUCT_MODULE"):
                    ENTRY._bootstrap(args)
            save(root/"wrong.json", {**profile, "source_pins": rows[1:]})
            wrong = pin(root/"wrong.json"); args.profile, args.profile_sha256 = wrong["path"], wrong["sha256"]
            with self.assertRaisesRegex(ValueError, "LIFECYCLE_ENTRY_EXACT_SOURCE_ROOT"):
                ENTRY._bootstrap(args)
        self.assertEqual(FORBIDDEN, [])
        OBSERVED[self._testMethodName] = dict(real_preimport_refusals=3, product_imports=0,
            scope="REAL_BOOTSTRAP_WITH_EXPLICIT_INERT_PINNED_FILES_NO_IMPORT")

    def test_02_snapshot_selection_binding(self):
        good = Fixture("snapshot")
        unused, selected_pin = ENTRY._snapshot_selection(good.boot, good.selection_path, good.input_pin)
        self.assertEqual(selected_pin, pin(good.selection_path))
        for fault, reason in (("argv", "EXACT_OUTER_ARGV"), ("source", "SELECTED_SOURCE_PIN"),
                              ("name", "COPIED_SELECTION")):
            with self.subTest(fault=fault):
                fixture = Fixture("snapshot", selection_fault=fault)
                with self.assertRaisesRegex(ValueError, reason):
                    ENTRY._snapshot_selection(fixture.boot, fixture.selection_path, fixture.input_pin)
        OBSERVED[self._testMethodName] = dict(real_selection_bindings=True, refusals=3,
            scope="REAL_FILE_PIN_AND_ACYCLIC_SELECTION_CHECK_WITH_INERT_INVOCATION")

    def test_03_actions_are_separate(self):
        for action in ("snapshot", "request"):
            with self.subTest(action=action):
                fixture = Fixture(action); code, report = fixture.run()
                self.assertEqual(code, 0)
                self.assertEqual(report["status"], "PASS_ONE_SNAPSHOT" if action == "snapshot"
                                 else "PASS_REQUEST_CONSTRUCTION_ONLY")
                self.assertTrue(report["owner_closed"] and report["final_binding_validated"])
                self.assertFalse(report["mathematical_admission"] or report["funding"])
                self.assertEqual((report["run_calls_attempted"], report["proof_calls"]), (0, 0))
                self.assertEqual(fixture.events[:4], ["construct", "prepare", "snapshot", "close"]
                                 if action == "snapshot" else ["construct", "request", "close", "save-other"])
                self.assertEqual(report["production_request_calls_attempted"], int(action == "request"))
                if action == "request":
                    self.assertFalse(fixture.output.exists())
                    self.assertEqual(pin(fixture.request_output), report["request"])
                self.assertEqual(json.loads(fixture.report_path.read_bytes())["status"], report["status"])
        OBSERVED[self._testMethodName] = dict(scope="REAL_ENTRY_FLOW_WITH_INERT_OWNER_AND_FILE_HELPERS",
            snapshot_calls=0, genuine_requests=0, extra_preflight_calls=0, proof_calls=0)

    def test_04_owner_failure_closure(self):
        cases = (("request", "constructor"), ("request", "work"), ("snapshot", "work"),
                 ("request", "close"), ("request", "created-output"))
        for action, fault in cases:
            with self.subTest(action=action, fault=fault):
                fixture = Fixture(action, fault); code, report = fixture.run()
                self.assertEqual((code, report["status"]), (1, "FAIL"))
                self.assertFalse(fixture.request_output.exists())
                if fault == "constructor":
                    self.assertEqual(report["owner_creation"], "ATTEMPTED_UNCONFIRMED")
                    self.assertNotIn("close", fixture.events)
                else:
                    self.assertIn("close", fixture.events)
                if action == "snapshot": self.assertIsNone(report["host_calls_attempted"])
        OBSERVED[self._testMethodName] = dict(cases=len(cases), scope="EXPLICIT_CONSTRUCTOR_WORK_CLOSE_DOUBLES")

    def test_05_finalization_failure_overrides(self):
        for fault in ("rebind", "save-report", "late-rebind"):
            with self.subTest(fault=fault):
                fixture = Fixture("request", fault); code, report = fixture.run()
                self.assertEqual((code, report["status"]), (1, "FAIL"))
                self.assertTrue(fixture.closed)
                self.assertFalse(report["final_binding_validated"])
                self.assertFalse(report["mathematical_admission"] or report["funding"])
                self.assertEqual((report["run_calls_attempted"], report["proof_calls"]), (0, 0))
                sentinel = Path(str(fixture.report_path)+".FINALIZATION-FAILED.json")
                self.assertTrue(sentinel.is_file())
                override = json.loads(sentinel.read_bytes())
                self.assertTrue(override["overrides_generated_request"] and override["overrides_owner_report"])
                if fault == "rebind": self.assertFalse(fixture.request_output.exists())
                if fault == "late-rebind":
                    self.assertEqual(json.loads(fixture.report_path.read_bytes())["status"], "PASS_REQUEST_CONSTRUCTION_ONLY")
        OBSERVED[self._testMethodName] = dict(cases=3, scope="INERT_FAILURES_WITH_REAL_FRESH_REPORT_SENTINEL_FILES")


def main():
    global ENTRY, ENTRY_SHA, OUTPUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entry", required=True); parser.add_argument("--entry-sha256", required=True)
    parser.add_argument("--output", required=True); args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, "ISOLATED_WINDOWS_CONTROLS")
    OUTPUT = Path(args.output).resolve(); entry_path = Path(args.entry).resolve()
    selection = json.loads((OUTPUT/"selection.json").read_bytes()); sources = selection["sources"]
    need(len(sources) == 3 and entry_path == OUTPUT/"sources/software/v5/typed_production/lifecycle_operator.py"
         and Path(__file__).resolve() == OUTPUT/"sources/software/v5/typed_production/lifecycle_controls.py",
         "EXACT_THREE_SOURCE_CONTROL_SNAPSHOT")
    source_rows = {}
    for relative, expected in sources.items():
        row = pin(OUTPUT/"sources"/relative); need(row["sha256"] == expected, "SELECTED_SOURCE_PIN")
        source_rows[relative] = row
    ENTRY_SHA = args.entry_sha256
    need(ENTRY_SHA == sources["software/v5/typed_production/lifecycle_operator.py"], "EXACT_ENTRY_PIN")
    need(not any(name.split(".")[0] in {"typed_production", "aggregate_small", "production"}
                 for name in sys.modules), "NO_PRODUCT_PRELOAD")
    spec = importlib.util.spec_from_file_location("_typed_lifecycle_entry_controls", entry_path)
    ENTRY = importlib.util.module_from_spec(spec); sys.modules[spec.name] = ENTRY
    with patch.object(subprocess, "Popen", forbidden), patch.object(os, "system", forbidden):
        spec.loader.exec_module(ENTRY)
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
    passed = result.wasSuccessful() and result.testsRun == len(SELECTED) and not result.skipped and not FORBIDDEN
    report = dict(schema="DMKN_TYPED_LIFECYCLE_ENTRY_CONTROLS_V1", status="PASS" if passed else "FAIL",
        selected=list(SELECTED), tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
        skipped=len(result.skipped), forbidden_calls=FORBIDDEN, observations=OBSERVED, sources=source_rows,
        entry_sha256=ENTRY_SHA, actual_producer_constructions=0, actual_snapshot_calls=0,
        genuine_production_requests=0, proof_calls=0, mathematical_admission=False,
        scope="ENTRY_ONLY_REAL_SMALL_FILE_PINS_WITH_EXPLICIT_INERT_BOOTSTRAP_OWNER_AND_HELPERS")
    save(OUTPUT/"lifecycle-controls-result.json", report)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

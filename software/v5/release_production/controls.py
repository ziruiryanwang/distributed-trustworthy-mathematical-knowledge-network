"""Changed release-adoption controls, one real owner, no producer dispatch.

Uses an explicitly staged complete component and its exact interpreter. The
frozen typed lifecycle test file supplies inert fixtures only; none of its tests
run. Descriptor negatives use tiny files, not cloned runtime trees. Python-level
file/import observations are not an OS sandbox or full distribution validation.
"""
import argparse
from contextlib import ExitStack, redirect_stdout
import copy
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

GROUPS = ("test_01_entry_adoption", "test_02_descriptor_authority",
          "test_03_paths_and_origins", "test_04_identity_and_failed_construction",
          "test_05_real_relocated_owner", "test_06_inert_entry_dispatch")
OBSERVED, FORBIDDEN, READS = {}, [], set()
AUDIT_ACTIVE = False
OLD_DOMAIN = b"DMKN-TYPED-AGGREGATE-LIFECYCLE-PROFILE-V1\0"


def need(ok, reason):
    if not ok:
        raise AssertionError(reason)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()


def pin(path):
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return dict(path=str(path), bytes=path.stat().st_size, sha256=digest)


def save(path, value):
    raw = encoded(value)
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "CONTROL_SAVE")
    return pin(path)


def forbidden(*unused, **ignored):
    FORBIDDEN.append("FORBIDDEN_EXTERNAL_OR_PRODUCER_DISPATCH")
    raise AssertionError(FORBIDDEN[-1])


def audit(event, args):
    if not AUDIT_ACTIVE:
        return
    if event in ("subprocess.Popen", "os.system", "socket.connect", "socket.bind"):
        forbidden()
    value = args[0] if event in ("open", "os.listdir", "os.scandir") and args else None
    if event == "import" and len(args) > 1:
        value = args[1]
    if not isinstance(value, (str, bytes, os.PathLike)):
        return
    path = Path(os.fsdecode(value)).resolve()
    need(path in ALLOWED_FILES or any(path.is_relative_to(root) for root in ALLOWED_ROOTS),
         "CONTROL_UNSELECTED_FILE_ACCESS:"+str(path))
    READS.add(str(path))
    need(len(READS) <= 4096, "CONTROL_TRACE_BOUND")


def load_file(name, path, expected):
    need(pin(path)["sha256"] == expected, "CONTROL_SELECTED_SOURCE")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def case(name):
    path = OUTPUT/name
    path.mkdir()
    return path


def bootstrap_args(profile_pin=None):
    row = PROFILE_PIN if profile_pin is None else profile_pin
    return SimpleNamespace(entry_sha256=ENTRY_PIN["sha256"], source_root=str(SOURCE_ROOT),
        profile=row["path"], profile_sha256=row["sha256"])


def bad_descriptor(name, change):
    """Real pinned JSON, synthetic root; expected refusal precedes binary reads."""
    root = case(name)
    descriptor = copy.deepcopy(DESCRIPTOR)
    change(descriptor)
    descriptor_pin = save(root/"descriptor.json", descriptor)
    files = {"descriptor.json": {k: descriptor_pin[k] for k in ("bytes", "sha256")}}
    manifest = save(root/"V5-RELEASE.json", dict(schema=A.MANIFEST_SCHEMA, files=files))
    return dict(root=str(root), manifest=manifest, descriptor=descriptor_pin)


class Controls(unittest.TestCase):
    def test_01_entry_adoption(self):
        with patch.object(ENTRY, "import_module", forbidden):
            args = bootstrap_args(); args.profile_sha256 = "00"*32
            with self.assertRaisesRegex(ValueError, "LIFECYCLE_ENTRY_DOCUMENT_PIN"):
                ENTRY._bootstrap(args)
            for label, mutation, reason in (
                ("entry-old-schema", lambda v: v.update(schema="DMKN_TYPED_AGGREGATE_LIFECYCLE_PROFILE_V1"),
                 "LIFECYCLE_ENTRY_RELEASE_PROFILE"),
                ("entry-source-count", lambda v: v["source_pins"].pop(), "LIFECYCLE_ENTRY_27_SOURCES"),
                ("entry-installed-self", lambda v: next(row for row in v["base_profile"]["support_profile"]["runtime_pins"]
                    if row["path"] == str(SOURCE_ROOT/"release_production/operator.py")).update(sha256="00"*32),
                 "LIFECYCLE_ENTRY_INSTALLED_ENTRY_BINDING")):
                value = copy.deepcopy(PROFILE); mutation(value)
                row = save(case(label)/"profile.json", value)
                with self.assertRaisesRegex(ValueError, reason):
                    ENTRY._bootstrap(bootstrap_args(row))
        OBSERVED[self._testMethodName] = dict(refusals=4, actual_import_dispatches=0)

    def test_02_descriptor_authority(self):
        release = copy.deepcopy(PROFILE["release"])
        release["manifest"]["sha256"] = "00"*32
        with self.assertRaisesRegex(P.ProductionError, "RELEASE_DOCUMENT_PIN"):
            A.load(release, PROFILE["source_pins"], PROFILE["base_profile"]["support_profile"])
        for label, mutation, reason in (
            ("descriptor-schema", lambda v: v.update(schema="INERT_WRONG_SCHEMA"),
             "RELEASE_EXACT_MATHEMATICAL_PROFILE"),
            ("descriptor-policy", lambda v: v.update(policy="00"*32),
             "RELEASE_EXACT_MATHEMATICAL_PROFILE"),
            ("descriptor-role", lambda v: v["roles"]["guest_image"].update(sha256="00"*32),
             "RELEASE_EXACT_SELECTED_ARTIFACT:guest_image")):
            selected = bad_descriptor(label, mutation)
            with self.assertRaisesRegex(P.ProductionError, reason):
                A.load(selected, PROFILE["source_pins"], PROFILE["base_profile"]["support_profile"])
        OBSERVED[self._testMethodName] = dict(refusals=4, synthetic_descriptor_roots=3,
            scope="REAL_LOADER_EARLY_REFUSALS_NO_BINARY_COPIES_OR_OWNER")

    def test_03_paths_and_origins(self):
        selected = bad_descriptor("descriptor-traversal",
            lambda v: v["roles"]["guest_image"].update(path="../escape.exe"))
        with self.assertRaisesRegex(P.ProductionError, "RELEASE_RELATIVE_COMPONENT"):
            A.load(selected, PROFILE["source_pins"], PROFILE["base_profile"]["support_profile"])
        row = dict(bytes=1, sha256="11"*32)
        with self.assertRaisesRegex(P.ProductionError, "RELEASE_CASE_ALIAS"):
            A._files({"Case.py": row, "case.py": row})
        with patch.object(A, "__file__", str(OUTPUT/"foreign-adoption.py")):
            with self.assertRaisesRegex(P.ProductionError, "RELEASE_SOURCE_ORIGIN:release_production.adoption"):
                T.source_paths()
        OBSERVED[self._testMethodName] = dict(refusals=3, source_origin_restored=True)

    def test_04_identity_and_failed_construction(self):
        roles = {name: {**row, "path": str(RELEASE_ROOT/row["path"])}
                 for name, row in DESCRIPTOR["roles"].items()}
        # An explicit inert adoption result isolates constructor ownership/error
        # plumbing. It is never used for the actual constructor in test_05.
        adopted = SimpleNamespace(root=RELEASE_ROOT, roles=roles,
            pins={row["path"]: row for row in PROFILE["source_pins"]},
            manifest_pin=PROFILE["release"]["manifest"], descriptor_pin=PROFILE["release"]["descriptor"])
        value = copy.deepcopy(PROFILE)
        value["base_profile"]["host_build"]["descriptor"]["sha256"] = "00"*32
        with patch.object(A, "load", return_value=adopted), patch.object(P, "Producer", forbidden):
            with self.assertRaisesRegex(P.ProductionError, "RELEASE_EXACT_ARTIFACT_REFERENCE_MAPS"):
                T.ReleaseLifecycleProducer(value)
        events = []
        class Support:
            _A = SimpleNamespace(CEILINGS={"memory_mib": 8192})
            _Job = object()
            _install = RELEASE_ROOT
            def __init__(self, unused): events.append("inert-support-created")
            def close(self): events.append("inert-support-closed")
        value = copy.deepcopy(PROFILE); value["base_profile"]["stage_memory_ceiling_mib"] = 8193
        with patch.object(A, "load", return_value=adopted), patch.object(P, "Producer", Support):
            with self.assertRaisesRegex(P.ProductionError, "INTEGER_LIMIT"):
                T.ReleaseLifecycleProducer(value)
        self.assertEqual(events, ["inert-support-created", "inert-support-closed"])
        self.assertNotEqual(T.PROFILE_DOMAIN, OLD_DOMAIN)
        self.assertNotEqual(P.hash_bytes(T.PROFILE_DOMAIN+P.encoded(PROFILE)),
                            P.hash_bytes(OLD_DOMAIN+P.encoded(PROFILE)))
        self.assertIs(T.ReleaseLifecycleProducer._snapshot, sys.modules["aggregate_lifecycle.producer"].LifecycleProducer._snapshot)
        self.assertIs(T.ReleaseLifecycleProducer._request, sys.modules["aggregate_small.producer"].AggregateProducer._request)
        self.assertFalse(any(name.split(".")[0] == "typed_production" for name in sys.modules))
        for name, arguments in (("_adopt_build", ()), ("_adopt_image", ()),
                                ("_adopt_host_build", ({}, {}, "stage"))):
            with self.assertRaisesRegex(P.ProductionError, "RELEASE_HISTORICAL_ADOPTION_FORBIDDEN"):
                getattr(T.ReleaseLifecycleProducer, name)(None, *arguments)
        OBSERVED[self._testMethodName] = dict(fake_supports=1, fake_support_closes=1,
            real_supports=0, historical_adoption_refusals=3, new_profile_domain=True,
            scope="EXPLICIT_INERT_ADOPTION_ONLY_FOR_TWO_CONSTRUCTOR_REFUSALS")

    def test_05_real_relocated_owner(self):
        owner = None
        before = P.encoded(PROFILE)
        with ExitStack() as stack:
            for name in ("prepare", "snapshot", "production_request", "preflight", "run"):
                stack.enter_context(patch.object(T.ReleaseLifecycleProducer, name, forbidden))
            try:
                owner = T.ReleaseLifecycleProducer(PROFILE)
                self.assertEqual(owner._install, RELEASE_ROOT)
                self.assertEqual(owner.profile_id, P.hash_bytes(T.PROFILE_DOMAIN+before))
                self.assertEqual(owner.profile_document(), PROFILE)
                self.assertFalse(owner.report()["closed"])
                self.assertEqual(owner._history, {})
                self.assertLessEqual(len(owner._pins), 64)
                self.assertLessEqual(sum(row["bytes"] for row in owner._pins.values()), 512*P.MIB)
                self.assertTrue(all(Path(path).is_relative_to(RELEASE_ROOT) for path in owner._pins))
                self.assertEqual(set(T.source_paths()), {Path(row["path"]) for row in PROFILE["source_pins"]})
                with self.assertRaisesRegex(P.ProductionError, "OPERATOR_REPORT_OVERLAP"):
                    BOOT.O.separate((RELEASE_ROOT/"other-component/future-output",), (owner._install,))
                original = owner.profile["stage_memory_ceiling_mib"]
                try:
                    owner.profile["stage_memory_ceiling_mib"] = original+1
                    with self.assertRaisesRegex(P.ProductionError, "AGGREGATE_PROFILE_MUTATED"):
                        owner.profile_document()
                finally:
                    owner.profile["stage_memory_ceiling_mib"] = original
                with patch.object(owner, "_snapshot_build_pins", {**owner._snapshot_build_pins,
                        "inert-extra": PROFILE["release"]["descriptor"]}):
                    with self.assertRaisesRegex(P.ProductionError, "RELEASE_RUNTIME_BINDING_MUTATED"):
                        owner.profile_document()
                visited = []
                actual_no_override = owner._no_override
                def observed_no_override(rows):
                    held = list(rows); visited.append({row["path"] for row in held})
                    return actual_no_override(held)
                with patch.object(owner, "_no_override", side_effect=observed_no_override):
                    self.assertEqual(owner.profile_document(), PROFILE)
                for selected in (owner.profile["host_build"], owner.profile["image_adoption"],
                                 owner._snapshot_build_pins):
                    self.assertIn({row["path"] for row in selected.values()}, visited)
                result = dict(profile_id=owner.profile_id, installation_pin_count=len(owner._pins),
                    installation_pin_bytes=sum(row["bytes"] for row in owner._pins.values()),
                    pin_map_sha256=P.hash_bytes(P.encoded(owner._pins)),
                    source_origins={name: str(Path(sys.modules[name].__file__).resolve()) for name in T.SOURCE_MODULES},
                    release_root=str(owner._install), profile_unchanged=P.encoded(PROFILE) == before,
                    scope="REAL_CONSTRUCTOR_COMPONENT_ONLY_NOT_FULL_DISTRIBUTION_OR_MATHEMATICS")
            finally:
                if owner is not None:
                    owner.close()
            self.assertTrue(owner.report()["closed"])
            self.assertFalse(owner.report()["busy"])
            self.assertTrue(owner._support.report()["closed"])
        result.update(real_constructors=1, real_closes=1, actual_stage_calls=0,
            actual_snapshots=0, actual_proof_calls=0, closed=True)
        OBSERVED[self._testMethodName] = result

    def test_06_inert_entry_dispatch(self):
        actions = []
        original_save = FIX.save
        def fixture_save(path, value):
            if path.name == "profile.json" and type(value) is dict and "base_profile" in value:
                value["release"] = {"root": str(path.parent/"installation")}
            return original_save(path, value)
        for action, fault in (("snapshot", None), ("request", None), ("preflight", None),
                              ("run", None), ("run", "raised"), ("run", "unknown-closure")):
            with patch.object(FIX, "save", side_effect=fixture_save):
                fixture = FIX.Fixture("snapshot" if action == "snapshot" else "request")
            Owner = fixture.boot.T.TypedLifecycleProducer
            fixture.boot.T = SimpleNamespace(ReleaseLifecycleProducer=Owner)
            fixture.action = action
            if action in ("preflight", "run"):
                fixture.value = dict(schema="DMKN_V5_SMALL_AGGREGATE_PRODUCER_REQUEST_V1",
                    allowance_id="INERT", session={"INERT": True}, checkpoints=[], prior_attempts=[],
                    output_directory=str(fixture.output), stage_limit=1, budget={"INERT": True},
                    carried_external_costs={"INERT": True})
                input_pin = save(fixture.root/"stage-input.json", fixture.value)
                fixture.argv[0] = action
                fixture.argv[fixture.argv.index("--input")+1] = input_pin["path"]
                fixture.argv[fixture.argv.index("--input-sha256")+1] = input_pin["sha256"]
            def preflight(inert_owner, value):
                fixture.events.append("preflight")
                need(value == fixture.value, "INERT_PREFLIGHT_INPUT")
                return dict(status="PASS_REQUEST_PREFLIGHT_ONLY", profile_id=inert_owner.profile_id,
                    host_calls=0, proof_calls=0, mathematical_admission=False, funding=False)
            def run(inert_owner, value):
                fixture.events.append("run")
                need(value == fixture.value, "INERT_RUN_INPUT")
                if fault == "raised": raise ValueError("INERT_RAISED_RUN")
                fixture.output.mkdir()
                result = dict(status="PASS_SELECTED_PREFIX_ONLY", profile_id=inert_owner.profile_id,
                    host_calls_attempted=2, reported_proof_stage_calls=2,
                    closure_accounting_known=fault != "unknown-closure", final_binding_validated=True)
                save(fixture.output/"RESULT.json", result)
                return result
            with patch.object(Owner, "preflight", preflight if action == "preflight" else forbidden), \
                 patch.object(Owner, "run", run if action == "run" else forbidden):
                code, report = fixture.run()
            expected = ["construct"]+(["prepare", "snapshot"] if action == "snapshot" else
                ["request"] if action == "request" else [action])+["close"]
            self.assertEqual([event for event in fixture.events if not event.startswith("save-")], expected)
            self.assertEqual(code, 1 if fault else 0)
            self.assertEqual(report["status"].startswith("PASS_"), fault is None)
            self.assertFalse(report["funding"]); self.assertFalse(report["mathematical_admission"])
            if fault == "raised":
                self.assertIsNone(report["host_calls_attempted"]); self.assertIsNone(report["proof_calls"])
            if action in ("request", "preflight"): self.assertFalse(fixture.output.exists())
            actions.append(dict(action=action, fault=fault, exit_code=code, status=report["status"]))
        with patch.object(FIX, "save", side_effect=fixture_save):
            fixture = FIX.Fixture("request")
        fixture.boot.T = SimpleNamespace(ReleaseLifecycleProducer=forbidden)
        # This explicit bootstrap double makes the release root independent of
        # the support/source roots, so only the new whole-release guard refuses.
        release_only = fixture.root/"separate-release-root"
        release_only.mkdir()
        fixture.boot.profile["release"]["root"] = str(release_only)
        profile_pin = save(fixture.root/"overlap-profile.json", fixture.boot.profile)
        fixture.boot.profile_pin = profile_pin
        fixture.boot.pins[profile_pin["path"]] = profile_pin
        fixture.argv[fixture.argv.index("--profile")+1] = profile_pin["path"]
        fixture.argv[fixture.argv.index("--profile-sha256")+1] = profile_pin["sha256"]
        unsafe_report = release_only/"forbidden-owner-report.json"
        fixture.argv[fixture.argv.index("--owner-report")+1] = str(unsafe_report)
        code, report = fixture.run()
        self.assertEqual(code, 1)
        self.assertIn("INERT_OVERLAP", report["error"])
        self.assertEqual(report["owner_creation"], "NOT_ATTEMPTED")
        self.assertEqual(fixture.events, [])
        self.assertFalse(unsafe_report.exists())
        OBSERVED[self._testMethodName] = dict(cases=actions, actual_producer_calls=0,
            full_release_report_overlap_refused=True,
            scope="REAL_ENTRY_FLOW_EXPLICIT_INERT_OWNER_AND_INERT_AUTHORITY")


def main():
    global ENTRY, ENTRY_PIN, FIX, BOOT, PROFILE, PROFILE_PIN, DESCRIPTOR, RELEASE_ROOT
    global SOURCE_ROOT, OUTPUT, A, T, P, ALLOWED_FILES, ALLOWED_ROOTS, AUDIT_ACTIVE
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("entry", "entry-sha256", "entry-fixtures", "entry-fixtures-sha256",
                 "profile", "profile-sha256", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    OUTPUT = Path(args.output).resolve(strict=True)
    ENTRY_PIN = pin(Path(args.entry).resolve(strict=True))
    PROFILE_PIN = pin(Path(args.profile).resolve(strict=True))
    need(ENTRY_PIN["sha256"] == args.entry_sha256 and PROFILE_PIN["sha256"] == args.profile_sha256,
         "CONTROL_ENTRY_PROFILE_PINS")
    PROFILE = json.loads(Path(PROFILE_PIN["path"]).read_bytes())
    RELEASE_ROOT = Path(PROFILE["release"]["root"])
    SOURCE_ROOT = RELEASE_ROOT/"sdk/v5"
    ALLOWED_ROOTS = (RELEASE_ROOT, Path(sys.executable).resolve().parent, OUTPUT)
    ALLOWED_FILES = {Path(__file__).resolve(), Path(ENTRY_PIN["path"]), Path(PROFILE_PIN["path"]),
                     Path(args.entry_fixtures).resolve(strict=True)}
    sys.addaudithook(audit)
    AUDIT_ACTIVE = True
    with patch.object(subprocess, "Popen", forbidden), patch.object(os, "system", forbidden):
        ENTRY = load_file("_release_entry_control_target", Path(ENTRY_PIN["path"]), args.entry_sha256)
        FIX = load_file("_frozen_inert_entry_fixtures", Path(args.entry_fixtures), args.entry_fixtures_sha256)
        FIX.ENTRY, FIX.ENTRY_SHA, FIX.OUTPUT, FIX.FORBIDDEN = ENTRY, args.entry_sha256, OUTPUT, FORBIDDEN
        BOOT = ENTRY._bootstrap(bootstrap_args())
        P, T = BOOT.P, BOOT.T
        A = sys.modules["release_production.adoption"]
        DESCRIPTOR = A._document(PROFILE["release"]["descriptor"], P.MIB)
        result = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(
            unittest.TestSuite(Controls(name) for name in GROUPS))
    need(not FORBIDDEN, "CONTROL_FORBIDDEN_CALL_OCCURRED")
    record = dict(schema="DMKN_RELEASE_PRODUCER_CHANGED_BOUNDARY_CONTROLS_V1",
        status="PASS" if result.wasSuccessful() else "FAIL", tests_run=result.testsRun,
        failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
        groups=list(GROUPS), observations=OBSERVED, forbidden_calls=FORBIDDEN,
        selected=dict(entry=ENTRY_PIN, profile=PROFILE_PIN, controls=pin(Path(__file__).resolve()),
                      entry_fixtures=pin(Path(args.entry_fixtures))),
        python_file_import_trace=sorted(READS), file_monitor_scope="PYTHON_EVENTS_NOT_OS_SANDBOX",
        complete_distribution_validation=False, mathematical_admission=False, funding=False,
        actual_host_calls=0, actual_snapshots=0, actual_proof_calls=0)
    save(OUTPUT/"release-producer-controls-result.json", record)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

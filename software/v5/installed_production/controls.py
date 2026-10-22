"""Three native-free installed-producer boundary groups; not installed-core tests.

Real contract and parent/profile state machines, tiny synthetic metadata only.
No complete installation, owner, database, snapshot, host or proof is created.
The parent bootstrap and supervisor substitutions are explicit observations.
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
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

GROUPS = ("test_01_metadata_profile", "test_02_public_evidence", "test_03_parent_commit")
OBSERVED, FORBIDDEN = {}, []


def need(ok, reason):
    if not ok:
        raise AssertionError(reason)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "CONTROL_WRITE")
    return pin(path)


def save(path, value):
    return write(path, encoded(value))


def forbidden(*unused, **ignored):
    FORBIDDEN.append("FORBIDDEN_PROCESS_NETWORK_OR_NATIVE_DISPATCH")
    raise AssertionError(FORBIDDEN[-1])


def audit(event, unused):
    if event in ("subprocess.Popen", "os.system", "socket.connect", "socket.bind"):
        forbidden()


def load(name, path, expected):
    row = pin(path)
    need(row["sha256"] == expected, "CONTROL_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Metadata:
    """Virtual payload rows plus a few tiny files; never a genuine installation."""
    def __init__(self, name):
        self.home = OUTPUT/name
        self.home.mkdir()
        self.root = self.home/"metadata-root"
        self.root.mkdir()
        files = {}
        def virtual(relative, raw=None):
            raw = b"INERT_UNEXECUTED_CONTROL_PAYLOAD\n" if raw is None else raw
            row = dict(path=relative, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
            files[relative] = {key:row[key] for key in ("bytes", "sha256")}
            return row
        def physical(relative, raw):
            write(self.root/relative, raw)
            return virtual(relative, raw)
        sources = {}
        for name in C.SOURCE_MODULES:
            suffix = name.replace(".", "/")+(".py" if "." in name else "/__init__.py")
            sources[name] = virtual("sdk/v5/"+suffix)
        entry = physical("sdk/v5/release_production/operator.py", b"# INERT ENTRY; NEVER EXECUTED\n")
        physical(L.SELF, b"# INERT LAUNCHER IDENTITY; REAL TARGET IS EXPLICITLY SUBSTITUTED\n")
        physical(L.CONTRACT, b"# INERT CONTRACT IDENTITY; REAL TARGET IS EXPLICITLY SUBSTITUTED\n")
        sources["release_production.launch_contract"] = dict(path=L.CONTRACT, **files[L.CONTRACT])
        helper_files = {}
        for relative in L.HELPERS.values():
            row = physical("base/"+relative, b"# INERT SUPERVISOR DOUBLE; NEVER IMPORTED\n")
            helper_files[relative] = {key:row[key] for key in ("bytes", "sha256")}
        base = physical("base/RELEASE-MANIFEST.json", encoded(dict(files=helper_files)))
        python = physical("base/receiver/runtime/python/python.exe", b"INERT NOT AN EXECUTABLE\n")
        python_dll = physical("base/receiver/runtime/python/python314.dll", b"INERT NOT A DLL\n")
        runtime = list(sources.values())
        runtime += [virtual("sdk/v5/aggregate_small/operator.py"), entry]
        runtime += [virtual("base/receiver/runtime/python/"+name) for name in C.PYTHON_RUNTIME_NAMES]
        roles = {}
        for name, (filename, size, sha) in C.ARTIFACTS.items():
            relative = "assets/producer/"+filename
            roles[name] = dict(path=relative, bytes=size, sha256=sha)
            files[relative] = dict(bytes=size, sha256=sha)
        self.descriptor = dict(schema=C.DESCRIPTOR_SCHEMA, foundation=C.FOUNDATION, policy=C.POLICY,
            relation_image=C.RELATION, aggregate_image=C.IMAGE, roles=roles, sources=sources)
        self.template = dict(schema=C.TEMPLATE_SCHEMA, source_pins=list(sources.values()),
            base_source_pins=[sources["aggregate_small"], sources["aggregate_small.producer"]],
            stage_memory_ceiling_mib=4096,
            support_profile=dict(schema="DMKN_V5_PRODUCER_PROFILE_V1", supervisor_manifest=base,
                host=roles["stage_host"], python=python, python_dll=python_dll,
                source_pins=[sources["production"], sources["production.producer"]],
                runtime_pins=runtime, image_id=C.IMAGE, foundation=C.FOUNDATION, policy=C.POLICY))
        descriptor = physical("production/ARTIFACTS.json", encoded(self.descriptor))
        template = physical("production/PROFILE-TEMPLATE.json", encoded(self.template))
        self.manifest = dict(schema=C.MANIFEST_SCHEMA, files=files,
            aggregate_image="99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60",
            production=dict(descriptor=descriptor, profile_template=template))
        manifest_pin = save(self.root/"V5-RELEASE.json", self.manifest)
        self.release = dict(root=str(self.root), manifest=manifest_pin,
            descriptor=pin(self.root/descriptor["path"]))
        self.profile = C.materialize_profile(self.root, manifest_pin, self.release["descriptor"], self.template)
        self.profile_pin = save(self.home/"profile.json", self.profile)
        self.entry = pin(self.root/entry["path"])

    def operation(self, name, action, *, input_pin=None, prior=None, input_launch=None, value=None):
        run, output = self.home/name, self.home/(name+"-action")
        if input_pin is None:
            value = dict(output_directory=str(output), allowance_id="INERT_ALLOWANCE",
                         prior_attempts=[]) if value is None else copy.deepcopy(value)
            if action == "request":
                value["request_output"] = str(run/"request.json")
            input_pin = save(self.home/(name+"-input.json"), value)
            output = Path(value["output_directory"])
        else:
            value = C.document(input_pin)
            output = Path(value["output_directory"])
        selection = dict(schema=C.SELECTION_SCHEMA, name=name, action=action,
            release=self.release, profile=self.profile_pin, input=input_pin, entry=self.entry,
            run_directory=str(run), runtime_pins={row["path"]:row["sha256"]
                for row in (self.profile_pin, input_pin, self.entry)},
            limits=dict(cpu_seconds=10, wall_seconds=60, memory_mib=128, active_processes=1,
                stdout_bytes=C.MIB, stderr_bytes=C.MIB),
            output_limits=dict(bytes=C.MIB, entries=128), prior_launches=prior or [], input_launch=input_launch)
        selected = save(self.home/(name+"-selection.json"), selection)
        return SimpleNamespace(selection=selection, original=selected, value=value, run=run,
                               output=output, fixture=self, copied=None)


def worker(op, produced_value=None):
    """Synthetic child data; real shared checker must still accept its bindings."""
    selection = op.selection
    op.copied = pin(op.run/"selection.json")
    action = selection["action"]
    profile_id = hashlib.sha256(C.PROFILE_DOMAIN+C.encoded(op.fixture.profile)).hexdigest()
    record = dict(schema="DMKN_RELEASE_LIFECYCLE_OPERATOR_RESULT_V1",
        status={"request":"PASS_REQUEST_CONSTRUCTION_ONLY", "preflight":"PASS_REQUEST_PREFLIGHT_ONLY",
                "run":"PASS_ONE_FINITE_ATTEMPT", "snapshot":"PASS_ONE_SNAPSHOT"}[action],
        action=action, profile_document=selection["profile"], input_document=selection["input"],
        outer_selection=op.copied, profile_id=profile_id,
        source_root=str(op.fixture.root/"sdk/v5"), owner_report=str(op.run/"OWNER-RESULT.json"),
        output_directory=str(op.output), owner_created=True, owner_closed=True,
        final_binding_validated=True, error=None, close_error=None, final_binding_error=None,
        entry_source=pin(op.run/"entry.py"))
    if action == "request":
        value = produced_value if produced_value is not None else dict(
            output_directory=str(op.fixture.home/(op.run.name+"-future")),
            allowance_id="INERT_ALLOWANCE", prior_attempts=[])
        record["request"] = save(op.run/"request.json", value)
    elif action in ("snapshot", "run"):
        op.output.mkdir()
        record["snapshot_result" if action == "snapshot" else "production_result"] = save(
            op.output/"RESULT.json", dict(allowance_id="INERT_ALLOWANCE", profile_id=profile_id))
    op.worker = record
    return save(op.run/"OWNER-RESULT.json", record)


def process_result(op):
    return dict(status="COMMAND_EXITED_ZERO_AND_CLOSED", child_exit_code=0,
        direct_child_reaped=True, job_closed=True, cleanup_errors=[], termination_requested=False,
        final_job=dict(active_processes=0, terminated_processes=0, cpu_seconds=0),
        argv=C.command(op.selection, op.copied), cwd=str(op.fixture.root), limits=op.selection["limits"])


def complete(op, *, produced_value=None, mutate=None):
    op.run.mkdir()
    op.copied = write(op.run/"selection.json", C.read_pin(op.original))
    write(op.run/"entry.py", C.read_pin(op.fixture.entry))
    worker_pin = worker(op, produced_value)
    outer = dict(schema=C.RESULT_SCHEMA, status="COMMAND_EXITED_ZERO_AND_CLOSED", selection=op.copied,
        worker_report=worker_pin, result=process_result(op), final_error=None,
        observed_output=dict(entries=4, bytes=4096, scope="DISJOINT_OPERATION_AND_SELECTED_ACTION_OUTPUT_ROOTS"),
        bootstrap_cpu_seconds=0, wrapper_cpu_seconds=0, wall_seconds=0,
        pre_clock_interpreter_startup="SYNTHETIC", bootstrap_containment="SYNTHETIC_NO_PROCESS",
        authority="SYNTHETIC_OPERATIONAL_FIXTURE_NOT_MATHEMATICS")
    if mutate is not None:
        mutate(outer)
    op.outer = save(op.run/"RESULT.json", outer)
    return op


class Controls(unittest.TestCase):
    def test_01_metadata_profile(self):
        fixture = Metadata("metadata")
        original = C.encoded(fixture.template)
        C.validate_production_metadata(fixture.manifest, fixture.descriptor, fixture.template)
        second = C.materialize_profile(fixture.root, fixture.release["manifest"],
                                       fixture.release["descriptor"], fixture.template)
        self.assertEqual(C.encoded(second), C.encoded(fixture.profile))
        self.assertEqual(original, C.encoded(fixture.template))
        self.assertNotEqual(fixture.manifest["aggregate_image"], fixture.descriptor["aggregate_image"])
        for label, change, reason in (
            ("policy", lambda m,d,t: d.update(policy="00"*32), "PUBLIC_METADATA_MATHEMATICS"),
            ("path", lambda m,d,t: t["source_pins"][0].update(path="../bad.py"), "PUBLIC_PATH_COMPONENT"),
            ("closure", lambda m,d,t: t["source_pins"].pop(), "PUBLIC_METADATA_LIST_LENGTH")):
            with self.subTest(label=label):
                m,d,t = copy.deepcopy((fixture.manifest, fixture.descriptor, fixture.template))
                change(m,d,t)
                with self.assertRaisesRegex(ValueError, reason):
                    C.validate_production_metadata(m,d,t)
        relocated = Metadata("metadata-relocated")
        self.assertEqual(C.encoded(relocated.template), original)
        self.assertNotEqual(C.encoded(relocated.profile), C.encoded(fixture.profile))
        # Real profile command with explicit complete-release adoption double.
        output = fixture.home/"created-profile"
        request = save(fixture.home/"profile-request.json",
            dict(schema=D.PRODUCTION_PROFILE_REQUEST, output_directory=str(output)))
        adopted = (fixture.root, fixture.manifest, C, fixture.descriptor, fixture.template, fixture.release)
        with patch.object(D, "installed_production_release", return_value=adopted), \
             patch.object(D, "verify_release", return_value=(C, fixture.descriptor, fixture.template)), \
             patch.object(D, "STARTED_CPU", time.process_time()), \
             patch.object(D, "STARTED_NS", time.monotonic_ns()), redirect_stdout(io.StringIO()):
            result = D.producer_profile(fixture.release["manifest"]["sha256"], request["path"], request["sha256"])
        self.assertEqual(C.read_pin(result["profile"]), C.encoded(fixture.profile))
        self.assertFalse((output/"PROFILE-PENDING.json").exists())
        self.assertFalse((output/"PROFILE-FAILED.json").exists())
        consumer = {"v5/control/p%03d.py"%index:"sdk/v5/control/p%03d.py"%index for index in range(109)}
        consumer.update({"portable/location/f%03d.mjs"%index:"sdk/portable/location/f%03d.mjs"%index
                         for index in range(21)})
        producer = {name:"sdk/"+name for name in D.PRODUCER_ONLY_SOURCES}
        full = {**consumer, **producer}
        self.assertEqual((len(producer),len(full)),(14,144))
        projected = D.consumer_sdk_sources(full)
        self.assertEqual(projected,consumer)
        self.assertEqual((len(projected),sum(name.startswith("v5/") and name.endswith(".py")
                                            for name in projected)),(130,109))
        missing = dict(full); missing.pop(sorted(producer)[0])
        with self.assertRaisesRegex(ValueError,"DIST_PRODUCER_ONLY_SOURCES_REQUIRED"):
            D.consumer_sdk_sources(missing)
        OBSERVED[self._testMethodName] = dict(deterministic=True, relocation_changes_identity=True,
            pure_refusals=4, profile_command_commit=True, actual_complete_release_adoptions=0,
            full_sdk_count=144,consumer_sdk_count=130,consumer_preparation_python_count=109,
            explicit_doubles=["distribution.installed_production_release", "distribution.verify_release"])

    def test_02_public_evidence(self):
        fixture = Metadata("evidence")
        first = complete(fixture.operation("request-one", "request"))
        run = complete(fixture.operation("run-one", "run", input_pin=first.worker["request"], input_launch=first.outer))
        next_value = dict(output_directory=str(fixture.home/"next-action"), allowance_id="INERT_ALLOWANCE",
                          prior_attempts=[run.worker["production_result"]])
        origin = complete(fixture.operation("request-two", "request", prior=[run.outer], value=next_value),
                          produced_value=next_value)
        current = fixture.operation("run-two", "run", input_pin=origin.worker["request"],
                                    prior=[run.outer], input_launch=origin.outer)
        selected = C.validate_selection(current.selection, current.original, fresh_run=True)
        C.rebind_selection(selected)
        self.assertIn(run.worker["entry_source"]["path"], selected.pins)
        bad = copy.deepcopy(current.selection); bad["prior_launches"] = []
        with self.assertRaisesRegex(ValueError, "PUBLIC_EXACT_PRIOR_LINEAGE"):
            C._lineage(bad, fixture.profile, current.value, {})
        bad = copy.deepcopy(current.selection); bad["input_launch"] = first.outer
        with self.assertRaisesRegex(ValueError, "PUBLIC_GENERATED_REQUEST_ORIGIN"):
            C._lineage(bad, fixture.profile, current.value, {})
        altered = complete(fixture.operation("bad-argv", "request"),
            mutate=lambda result: result["result"]["argv"].append("--unselected"))
        with self.assertRaisesRegex(ValueError, "PUBLIC_EXACT_CLEAN_COMMAND"):
            C.completed_outer(altered.outer)
        pending = complete(fixture.operation("pending", "request"))
        save(pending.run/"FINALIZATION-PENDING.json", dict(synthetic=True))
        C.validate_worker_report(pending.selection, pending.copied, pin(pending.run/"OWNER-RESULT.json"))
        with self.assertRaisesRegex(ValueError, "PUBLIC_FINALIZATION_OVERRIDE"):
            C.completed_outer(pending.outer)
        failed = complete(fixture.operation("failed", "request"))
        save(failed.run/"FINALIZATION-FAILED.json", dict(synthetic=True))
        with self.assertRaisesRegex(ValueError, "PUBLIC_FINALIZATION_OVERRIDE"):
            C.completed_outer(failed.outer)
        bad = copy.deepcopy(current.selection); bad["entry"]["bytes"] = C.PUBLIC_ENTRY_REPORT_LIMIT+1
        with self.assertRaisesRegex(ValueError, "PUBLIC_INTEGER_BOUND"):
            C._shape(bad)
        oversized = dict(path=str(fixture.home/"not-created.json"), bytes=C.PUBLIC_ENTRY_REPORT_LIMIT+1, sha256="00"*32)
        with self.assertRaisesRegex(ValueError, "PUBLIC_INTEGER_BOUND"):
            C.validate_worker_report(first.selection, first.copied, {**oversized, "path":str(first.run/"OWNER-RESULT.json")})
        # Read only this operation; its nested historical graph is not replayed.
        shallow = fixture.operation("shallow", "request", prior=[dict(
            path=str(fixture.home/"absent-old-outer.json"), bytes=1, sha256="00"*32)])
        complete(shallow)
        self.assertEqual(C.completed_outer(shallow.outer).selection["prior_launches"], shallow.selection["prior_launches"])
        OBSERVED[self._testMethodName] = dict(real_pin_validators=True, public_refusals=7,
            shallow_evidence=True, pending_precommit_allowed=True, pending_adoption_refused=True,
            actual_public_operations=0, scope="SYNTHETIC_LOCAL_EVIDENCE_NOT_TRUSTED_EXECUTION")

    def test_03_parent_commit(self):
        outcomes = []
        for fault in (None, "late-check", "late-check-and-marker", "commit-unlink"):
            fixture = Metadata("parent-"+(fault or "success"))
            op = fixture.operation("launch", "request")
            calls = []
            def supervise(argv, cwd, prefix, limits, job, started):
                calls.append(dict(argv=argv, cwd=str(cwd), limits=limits))
                self.assertTrue((op.run/"FINALIZATION-PENDING.json").exists())
                worker(op)
                return process_result(op)
            supervisor = SimpleNamespace(limits_checked=lambda value: dict(value), supervise=supervise)
            modules = {"_dmkn_release_producer_contract_parent": C,
                "_dmkn_release_producer_supervisor":supervisor,
                "domains":SimpleNamespace(), "_dmkn_release_producer_job":SimpleNamespace(Job=forbidden)}
            original_checked, original_write, original_unlink = L.checked, L.write_new, Path.unlink
            def checked(row, *args, **kwargs):
                if fault in ("late-check", "late-check-and-marker") and row["path"] == str(op.run/"RESULT.json"):
                    raise ValueError("CONTROL_INJECTED_LATE_REBIND")
                return original_checked(row, *args, **kwargs)
            def write_new(path, raw):
                if fault == "late-check-and-marker" and Path(path).name == "FINALIZATION-FAILED.json":
                    raise OSError("CONTROL_INJECTED_MARKER_WRITE_FAILURE")
                return original_write(path, raw)
            def unlink(path, *args, **kwargs):
                if fault == "commit-unlink" and path == op.run/"FINALIZATION-PENDING.json":
                    raise OSError("CONTROL_INJECTED_COMMIT_FAILURE")
                return original_unlink(path, *args, **kwargs)
            with ExitStack() as stack:
                for target, name, value in (
                    (L,"__file__",str(fixture.root/L.SELF)),
                    (L,"BASE_SHA",pin(fixture.root/"base/RELEASE-MANIFEST.json")["sha256"]),
                    (L,"STARTED_NS",time.monotonic_ns()), (L,"STARTED_CPU",time.process_time()),
                    (sys,"executable",str(fixture.root/"base/receiver/runtime/python/python.exe")),
                    (sys,"argv",["INERT_PARENT",op.original["path"],op.original["sha256"]])):
                    stack.enter_context(patch.object(target,name,value))
                stack.enter_context(patch.object(L,"held_module",side_effect=lambda name,row:modules[name]))
                stack.enter_context(patch.object(L,"checked",side_effect=checked))
                stack.enter_context(patch.object(L,"write_new",side_effect=write_new))
                stack.enter_context(patch.object(Path,"unlink",unlink))
                stack.enter_context(redirect_stdout(io.StringIO()))
                code = L.main()
            self.assertEqual(len(calls),1)
            result_pin = pin(op.run/"RESULT.json")
            saved = C.document(result_pin)
            self.assertEqual(saved["status"], "COMMAND_EXITED_ZERO_AND_CLOSED")
            self.assertEqual(code,0 if fault is None else 1)
            pending = (op.run/"FINALIZATION-PENDING.json").exists()
            self.assertEqual(pending,fault is not None)
            if fault is None:
                C.completed_outer(result_pin)
            else:
                with self.assertRaisesRegex(ValueError,"PUBLIC_FINALIZATION_OVERRIDE"):
                    C.completed_outer(result_pin)
            if fault == "late-check-and-marker":
                self.assertFalse((op.run/"FINALIZATION-FAILED.json").exists())
            outcomes.append(dict(fault=fault,exit_code=code,pending_retained=pending,
                                 saved_result_provisional=fault is not None))
        OBSERVED[self._testMethodName] = dict(cases=outcomes, actual_child_processes=0,
            explicit_doubles=["installed __file__ and executable identities", "fixed base manifest digest",
                "held bootstrap module dispatcher", "supervisor and Job", "original clocks for each synthetic call"],
            real_contract=True, real_parent_main=True, real_small_file_persistence=True)


def main():
    global C,L,D,OUTPUT
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("contract","contract-sha256","launcher","launcher-sha256","distribution","distribution-sha256","output"):
        parser.add_argument("--"+name,required=True)
    args=parser.parse_args()
    need(os.name=="nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize,"CONTROL_ISOLATED_WINDOWS")
    OUTPUT=Path(args.output).resolve(strict=True)
    selected={name:pin(Path(getattr(args,name)).resolve(strict=True)) for name in ("contract","launcher","distribution")}
    for name,row in selected.items():
        need(row["sha256"]==getattr(args,name+"_sha256"),"CONTROL_ARGUMENT_PIN")
    sys.addaudithook(audit)
    with patch.object(subprocess,"Popen",forbidden),patch.object(os,"system",forbidden):
        C=load("_installed_contract_controls",Path(args.contract),args.contract_sha256)
        L=load("_installed_launcher_controls",Path(args.launcher),args.launcher_sha256)
        D=load("_installed_distribution_controls",Path(args.distribution),args.distribution_sha256)
        result=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in GROUPS))
    passed=result.wasSuccessful() and result.testsRun==len(GROUPS) and not result.skipped and not FORBIDDEN
    for name,row in selected.items():
        need(pin(Path(row["path"]))==row,"CONTROL_FINAL_SOURCE_PIN")
    save(OUTPUT/"installed-producer-controls-result.json",dict(
        schema="DMKN_INSTALLED_PRODUCER_BOUNDARY_CONTROLS_V1",status="PASS" if passed else "FAIL",
        tests_run=result.testsRun,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
        groups=list(GROUPS),observations=OBSERVED,selected_sources=selected,controls=pin(Path(__file__).resolve()),
        forbidden_calls=FORBIDDEN,actual_child_processes=0,actual_producer_constructions=0,actual_snapshots=0,
        actual_host_calls=0,actual_proof_calls=0,complete_installation_validation=False,
        mathematical_acceptance=False,funding=False,scope="NATIVE_FREE_CHANGED_BOUNDARIES_WITH_EXPLICIT_DOUBLES"))
    return 0 if passed else 1


if __name__=="__main__":
    raise SystemExit(main())

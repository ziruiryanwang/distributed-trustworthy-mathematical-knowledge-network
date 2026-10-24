"""Six remaining public owner calls over the preserved accepted owner.

Only the existing pinned supervision/diagnostic helpers are imported. This
adapter never creates accepted state, calls owner APIs, compiles the retained
fixture, adopts an old correspondence report or launches a network service.
One root-selected enclosing Job and one remaining parent budget own all calls.
The controlled Flag example is integration evidence, not useful-growth evidence.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import os
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_reference_package/"
NAME = "ordinary-reference-public-continuation-01"
PACKAGE = LOCAL/"ordinary-reference-assembly-02/package"
PREVIOUS = LOCAL/"ordinary-reference-public-workflow-01"
STATE = PREVIOUS/"workflow"
ORIGIN = "97440ed1f77850e5b58a7256172246dc45efbded96ed160faef827e65b86874a"
SNAPSHOT = "71bc7058363c9972c71e7e560d70ccc467fc18cba4c8c93cdbb6c3bceae95f7b"
BASIS_ROOT = "138c02d2de87fcc82cdfd11ac292ee9a9fb2ff41761f00174c6793337f1f8ee4"
INTAKE_ROOT = "72b399a0e3ad4a1673ec369115c255dd0f3016ae2956572c5def4ce1081f96b1"
STORE = "0096ade6422b06862c21d8f051a0c3d714ef65aec6f2607a2941443741c138c8"
PREVIOUS_PINS = {
    "RESULT.json": "9742b6dbcf8c9453cf5a6f8095b1bb373f149e863b4e6e4e1e240fc65f9da061",
    "selection.json": "99796dea391f7ead5f97bb80ed3131e15ed9bdf042230a69a54ed8f485e7ac5b",
    "workflow/WORKFLOW.json": "b99ae315a7f17cf5df9019d739f0d6577c65df929bdb8044bec42cbbd2a81734",
    "workflow/catalog/ADOPTION.json": "dcb9b9e3bc820558feec8aef4c220a8594c986ad9cbf7c07574fa894b47bfd7c",
    "workflow/catalog/ordinary-realizations-v1/STORE.json": "74b2b99afd2880bb619968965b8ed4492579e2a05a4c2b05ed8cad7fcd6a6884",
    "workflow/catalog/ordinary-realizations-v1/operations/"+ORIGIN+"/RESERVATION.json":
        "15e7211cb67a1b8cfe2158772c4a79f75915be49d9d83de1c029a33cea062da2",
    "workflow/catalog/ordinary-realizations-v1/operations/"+ORIGIN+"/CLOSED.json":
        "e808baed8c10be9bd2b666ee671f6507958f2eedb43db090d481eb33b6bdc8fb",
    "workflow/catalog/ordinary-realizations-v1/operations/"+ORIGIN+"/snapshot/prepared-manifest.json": SNAPSHOT,
}
RETAINED = LOCAL/"ordinary-baseline-native-workflow-02/workflow"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
HELPER = ROOT/"software/v5/ordinary_distribution/relocated_smoke.py"
HELPER_SHA = "aaba6e2e30906414f539842fd7678aaaf3ab7f9c077b30c6f115db7407584831"
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
MANIFEST = "b601bee8f6be2b2fc2315818ba81f340ed8bd72a43ac89cf547db001e7bc9cde"
PROJECT = "bb2753d5999774e4da0530503734633c48dcbc623ce29f5c3cc8a57f60fdfb45"
ARTIFACTS = "49003f08190856d675e6dd26f602cfdae1acfe8dac422e7cc2e9d6b720d80fff"
MIB = 1024**2
CAPS = (("01-register-retained", "register-reference", 120, 80),
        ("02-author-A", "contribute-reference", 150, 100),
        ("03-delta-A", "export-reference-delta", 140, 100),
        ("04-author-B", "contribute-reference", 150, 100),
        ("05-refuse-sorry", "contribute-reference", 100, 65),
        ("06-status", "status", 45, 20))
BODY_A = b"""open DMKNBaselineFixture
open scoped DMKNBaselineFixture

namespace DMKNReferenceA

theorem flip_apply (f : Flag -> Flag) : f (flip lowF) = f Flag.high := by
  simp

theorem flip_involution (x : Flag) : flip (flip x) = x := by
  cases x <;> rfl

end DMKNReferenceA
"""
BODY_B = b"""open DMKNBaselineFixture
open scoped DMKNBaselineFixture

namespace DMKNReferenceB

theorem flip_injective (x y : Flag) (h : flip x = flip y) : x = y :=
  (DMKNReferenceA.flip_involution x).symm.trans
    ((congrArg flip h).trans (DMKNReferenceA.flip_involution y))

theorem high_fiber (x : Flag) (h : flip x = Flag.high) : x = lowF :=
  flip_injective x lowF (h.trans flip_low.symm)

end DMKNReferenceB
"""
A_NAMES = ("DMKNReferenceA.flip_apply", "DMKNReferenceA.flip_involution")
B_NAMES = ("DMKNReferenceB.flip_injective", "DMKNReferenceB.high_fiber")
BODY_FALSE = b"theorem reference_false : False := by sorry\n"


def need(ok, code):
    if not ok:
        raise ValueError(code)


def helpers():
    with HELPER.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == HELPER_SHA,
         "REFERENCE_WORKFLOW_HELPER_PIN")
    name = "_reference_public_saved_helpers"
    need(name not in sys.modules, "REFERENCE_WORKFLOW_PRELOADED_HELPER")
    spec = importlib.util.spec_from_file_location(name, HELPER)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    exec(compile(raw, str(HELPER), "exec"), value.__dict__)
    value.ordinary(HELPER)
    return value


def inspect_static(h, profile_sha, assembly_sha, check):
    """Inventory exact named inputs, with no product imports or mutable state."""
    pins = {}

    def keep(path, expected=None, maximum=128*MIB):
        pin = h.pin(path, check, maximum)
        need(expected is None or pin == expected or pin["sha256"] == expected,
             "REFERENCE_WORKFLOW_INPUT_PIN:"+str(path))
        need(str(path) not in pins or pins[str(path)] == pin, "REFERENCE_WORKFLOW_CONFLICTING_PIN")
        pins[str(path)] = pin
        return pin

    def document(path, expected, maximum=2*MIB):
        pin = keep(path, expected, maximum)
        raw = h.read(path, maximum)
        need(h.sha(raw) == pin["sha256"], "REFERENCE_WORKFLOW_INPUT_CHANGED")
        return h.diagnostic_json(raw)

    profile = document(PACKAGE/"PROFILE.json", profile_sha)
    manifest = document(PACKAGE/"installation/INSTALLATION.json", INSTALLATION)
    receipt = document(PACKAGE/"ASSEMBLY.json", assembly_sha)
    need(profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
         profile["installation_manifest_sha256"] == INSTALLATION and len(profile["files"]) == 137 and
         receipt["schema"] == "DMKN_ORDINARY_REFERENCE_SUCCESSOR_ASSEMBLY_V1" and
         receipt["status"] == "ASSEMBLED_NOT_ADOPTED" and receipt["profile_sha256"] == profile_sha and
         receipt["installation_manifest_sha256"] == INSTALLATION and
         receipt["implementation_id"] == IMPLEMENTATION and receipt["files_excluding_profile"] == 165 and
         receipt["added"] == [] and receipt["changed"] ==
             ["owner.py", "reference/reference_registration.py", "reference/reference_store.py"] and
         len(receipt["unchanged"]) == 162 and
         receipt["base_profile_sha256"] == "2d965cb67cb6729dfe42380146377bb1ab85ef42713c1de3f6668da09ba2fb13" and
         receipt["base_receipt_sha256"] == "ae7ff57af40576ca2b7683baf188d366f3803b5c3e44f7a72f0f25540ef81671", "REFERENCE_WORKFLOW_PACKAGE_IDENTITY")
    package_files = {"PROFILE.json", "ASSEMBLY.json", "installation/INSTALLATION.json"}
    for logical, expected in profile["files"].items():
        keep(PACKAGE/h.relative(logical), expected); package_files.add(logical)
    roots = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    for logical, expected in manifest["files"].items():
        parts = h.relative(logical).parts
        if parts[0] in roots:
            keep(roots[parts[0]].joinpath(*parts[1:]), expected)
        else:
            keep(PACKAGE/"installation"/logical, expected)
            package_files.add("installation/"+logical)
    need(len(package_files) == 167 and manifest["implementation"]["semantic_id"] == SEMANTIC and
         h.identity("DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1", h.canonical(manifest["implementation"])) == IMPLEMENTATION,
         "REFERENCE_WORKFLOW_INSTALLATION_IDENTITY")
    bundle = document(RETAINED/"bundle/manifest.json", MANIFEST)
    project = document(RETAINED/"project-selection.json", PROJECT)
    artifacts = document(RETAINED/"artifact-report.json", ARTIFACTS, 16*MIB)
    need(bundle["schema"] == "DMKN_ORDINARY_BASELINE_BUNDLE_V1" and bundle["semantic_id"] == SEMANTIC and
         len(bundle["batches"]) == 1 and len(bundle["batches"][0]) == 6 and
         project == {"schema": "DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1",
                     "modules": [h.name("DMKNBaselineFixture02")],
                     "project_search_paths": [str(RETAINED/"original-library")]},
         "REFERENCE_WORKFLOW_RETAINED_FIXTURE")
    units, bindings = {}, {}
    for row in bundle["batches"][0]:
        raw = h.read(RETAINED/"bundle/units"/(row["unit_id"]+".json"), 8*MIB)
        keep(RETAINED/"bundle/units"/(row["unit_id"]+".json"),
             {"bytes": row["raw_bytes"], "sha256": row["raw_sha256"]}, 8*MIB)
        need(h.identity("DMKN-ORDINARY-EVIDENCE-V2", raw) == row["unit_id"], "REFERENCE_WORKFLOW_UNIT_ID")
        doc = h.diagnostic_json(raw)
        need(doc["schema"] == "DMKN_LEAN_ORDINARY_EVIDENCE_V2" and doc["semantic_id"] == SEMANTIC,
             "REFERENCE_WORKFLOW_UNIT_SEMANTICS")
        units[row["unit_id"]] = doc
        for entry in doc["unit"][2]:
            key = h.canonical(entry[0])
            need(key not in bindings, "REFERENCE_WORKFLOW_DUPLICATE_FIXTURE_EXPORT")
            bindings[key] = {"name": entry[0], "unit_id": row["unit_id"], "export_id": h.identity(
                "DMKN-ORDINARY-EXPORT-V2", h.canonical([SEMANTIC, row["unit_id"], entry[0]]))}
    # The five original fixture parts are owner-approved execution inputs, not
    # warrants. Standard Lean library files remain the selected runtime premise;
    # the product hashes its actual full snapshot during real registration.
    for suffix in h.PARTS:
        keep(RETAINED/"original-library"/("DMKNBaselineFixture02"+suffix), maximum=64*MIB)
    keep(HELPER, HELPER_SHA, 2*MIB)
    # These pins preserve provenance, not mathematical authority. The actual
    # owner reopens its current catalog and validates warrants under its lock.
    previous = {name: document(PREVIOUS/name, digest, 4*MIB)
                for name, digest in PREVIOUS_PINS.items()}
    prior = previous["workflow/WORKFLOW.json"]
    outer = previous["RESULT.json"]
    need(prior["status"] == "FAILED" and prior["phase"] == "REGISTER" and len(prior["calls"]) == 3 and
         prior["confirmed_roots"] == [BASIS_ROOT, INTAKE_ROOT] and
         prior["calls"][0]["public_result"]["store_id"] == STORE and
         prior["calls"][2]["public_result"]["detail"]["error"] == "REFERENCE_OPERATION_FILE" and
         outer["selection_sha256"] == PREVIOUS_PINS["selection.json"],
         "REFERENCE_CONTINUATION_EXACT_FAILED_PREDECESSOR")
    h.clean(outer["result"], exit_code=1)
    sidecar = h.ordinary(STATE/"catalog/ordinary-realizations-v1", directory=True)
    need(not any(h.ordinary(sidecar/"records", directory=True).iterdir()),
         "REFERENCE_CONTINUATION_EXPECTED_UNREGISTERED")
    need({path.name for path in h.ordinary(sidecar/"operations", directory=True).iterdir()} == {ORIGIN},
         "REFERENCE_CONTINUATION_EXPECTED_OLD_OPERATION")
    origin = sidecar/"operations"/ORIGIN
    need(not (origin/"record.staged.json").exists(), "REFERENCE_CONTINUATION_NO_STAGED_RECORD")
    fixtures = {
        "custody-limits.json": {"objects": 512, "exports": 4096,
                               "logical_bytes": 128*MIB, "db_pages": 16384},
        "A.lean": BODY_A, "B.lean": BODY_B, "False.lean": BODY_FALSE,
        "A-targets.json": [h.name(name) for name in A_NAMES],
        "B-targets.json": [h.name(name) for name in B_NAMES],
        "False-targets.json": [h.name("reference_false")],
        "reference-targets.json": [{key: bindings[h.canonical(h.name(name))][key]
            for key in ("name", "export_id")}
            for name in ("DMKNBaselineFixture.flip", "DMKNBaselineFixture.flip_low")],
    }
    for name, expected in fixtures.items():
        raw = expected if type(expected) is bytes else h.canonical(expected)
        keep(STATE/"fixtures"/name, {"bytes": len(raw), "sha256": h.sha(raw)}, MIB)
    need(len(pins) <= 256, "REFERENCE_WORKFLOW_INPUT_CENSUS")
    return {"pins": pins, "profile": profile, "manifest": manifest,
            "package_files": package_files, "bundle": bundle, "units": units,
            "bindings": bindings, "artifact_report": artifacts}


class Workflow:
    def __init__(self, args, h):
        self.args, self.h = args, h
        self.started, self.cpu_started = START_WALL, START_CPU
        self.deadline = START_WALL+args.wall_seconds
        self.charged, self.complete = 0.0, True
        self.calls, self.held, self.confirmed = [], {}, []
        self.output_created = False

    def check(self):
        need(time.monotonic() < self.deadline and time.process_time()-self.cpu_started+self.charged <
             self.args.cpu_seconds, "REFERENCE_WORKFLOW_ORIGINAL_ALLOWANCE")

    def hold(self, path, expected=None, maximum=128*MIB):
        actual = self.h.pin(path, self.check, maximum)
        need(expected is None or actual == expected, "REFERENCE_WORKFLOW_EXACT_PIN:"+str(path))
        need(self.held.setdefault(str(path), actual) == actual, "REFERENCE_WORKFLOW_IMMUTABLE_CHANGED")
        return actual

    def document(self, path, maximum=4*MIB):
        self.check()
        return self.h.diagnostic_json(self.h.read(path, maximum))

    def save(self, path, value):
        return self.hold(path, self.h.save(path, value))

    def capture_tree(self, path):
        return self.h.Smoke.capture_tree(self, path)

    def native(self, path, *, extraction=False):
        value = self.document(path, 2*MIB)
        self.h.clean(value, extraction=extraction); self.hold(path)
        return value

    def prepare(self):
        h = self.h
        self.output = h.ordinary(self.args.output, directory=True, fresh=True)
        need(self.output == LOCAL/NAME/"workflow" and Path(sys.executable).resolve() == PYTHON/"python.exe",
             "REFERENCE_WORKFLOW_LOCATION")
        self.static = inspect_static(h, self.args.profile_sha256, self.args.assembly_sha256, self.check)
        self.manifest = self.static["manifest"]
        for path, pin in self.static["pins"].items():
            self.held[path] = pin
        need(self.capture_tree(PACKAGE) == self.static["package_files"], "REFERENCE_WORKFLOW_PACKAGE_TREE")
        roles = self.manifest["roles"]
        for role, name in (("supervisor", "_reference_workflow_supervisor"),
                           ("domains", "domains"), ("job", "_reference_workflow_job")):
            logical = roles[role]
            need(logical.startswith("supervisor/"), "REFERENCE_WORKFLOW_SUPERVISOR_ROLE")
            module = h.load_exact(PACKAGE/"installation"/h.relative(logical), name,
                                  self.manifest["files"][logical], self.check)
            if role == "supervisor":
                self.supervisor = module
            elif role == "job":
                self.jobs = module
        self.output.mkdir(); self.output_created = True
        self.catalog = h.ordinary(STATE/"catalog", directory=True)
        self.custody = h.ordinary(STATE/"custody", directory=True)
        self.fixtures = h.ordinary(STATE/"fixtures", directory=True)
        self.new_fixtures = self.output/"fixtures"
        self.new_fixtures.mkdir(); (self.output/"calls").mkdir()
        self.store = STORE
        self.confirmed = [BASIS_ROOT, INTAKE_ROOT]
        self.reference_targets = [self.static["bindings"][h.canonical(h.name(name))]
                                 for name in ("DMKNBaselineFixture.flip", "DMKNBaselineFixture.flip_low")]
        self.save(self.output/"INPUTS.json", self.held.copy())
        self.save(self.output/"PLAN.json", {"scope": "SIX_REMAINING_PUBLIC_CALLS_RETAINED_OWNER_NOT_GROWTH_OR_DEPLOYMENT",
            "call_caps": CAPS, "original_allowance": vars(self.args), "fixture_manifest": MANIFEST,
            "trust": "OWNER_APPROVED_SOURCE_AND_LIBRARY_NO_HOSTILE_SOURCE_SANDBOX",
            "snapshot": "RETAINED_IN_PLACE_CURRENT_WARRANTS_NEW_LIVE_MATCH_NO_COPY",
            "mathematical_authority": "ONLY_ACTUAL_PUBLIC_ADMISSION_NOT_THIS_HARNESS"})

    def fixture(self, name, value):
        path = self.new_fixtures/name
        self.save(path, value)
        return path

    def call(self, operation, extra=(), *, refused=False):
        self.check()
        number = len(self.calls)
        need(number < len(CAPS), "REFERENCE_WORKFLOW_CALL_BOUND")
        label, selected, wall_cap, cpu_cap = CAPS[number]
        need(operation == selected and refused == (number == 4), "REFERENCE_WORKFLOW_CALL_ORDER")
        grant = self.supervisor.limits_checked({
            "wall_seconds": min(wall_cap, math.floor(self.deadline-time.monotonic())-20),
            "cpu_seconds": min(cpu_cap, math.floor(self.args.cpu_seconds-self.charged-
                                  (time.process_time()-self.cpu_started))-4),
            "memory_mib": self.args.memory_mib, "active_processes": 6,
            "stdout_bytes": 4*MIB, "stderr_bytes": MIB})
        need(grant["wall_seconds"] >= 45 and grant["cpu_seconds"] >= 8,
             "REFERENCE_WORKFLOW_REMAINING_GRANT")
        argv = [str(PYTHON/"python.exe"), "-I", "-S", "-B", str(PACKAGE/"owner.py"), operation,
            "--profile-sha256", self.args.profile_sha256, "--python-runtime", str(PYTHON),
            "--lean-runtime", str(LEAN), "--catalog", str(self.catalog), "--custody", str(self.custody),
            "--store-id", self.store, "--custody-limits", str(self.fixtures/"custody-limits.json"),
            "--wall-seconds", str(grant["wall_seconds"]-5), "--cpu-seconds", str(grant["cpu_seconds"]-2),
            "--memory-mib", str(self.args.memory_mib), *map(str, extra)]
        event = {"label": label, "operation": operation, "argv": argv, "limits": grant,
                 "charged_cpu_seconds": grant["cpu_seconds"], "cpu_complete": False, "public_result": None}
        self.calls.append(event)
        self.charged += grant["cpu_seconds"]
        supervision = None
        try:
            supervision = self.supervisor.supervise(argv, self.output, self.output/"calls"/label, grant, self.jobs.Job)
            event["supervision"] = supervision
        except BaseException as error:
            event["exception"] = {"type": type(error).__name__, "message": str(error)[:2048]}
            raise
        finally:
            final = supervision.get("final_job") if type(supervision) is dict else None
            value = final.get("cpu_seconds") if type(final) is dict else None
            known = (type(value) in (int, float) and math.isfinite(value) and value >= 0 and
                     final.get("active_processes") == 0 and final.get("total_processes", 0) >= 1 and
                     supervision.get("direct_child_reaped") is True)
            if known:
                self.charged += value-grant["cpu_seconds"]
                event.update(charged_cpu_seconds=value, cpu_complete=True)
            else:
                self.complete = False
            try:
                raw = self.h.read(self.output/"calls"/label/"stdout.txt", 4*MIB)
                if raw:
                    event["public_result"] = self.h.diagnostic_json(raw)
            except BaseException as error:
                event["reply_parse_error"] = str(error)[:2048]
            self.h.save(self.output/"calls"/(label+"-EVENT.json"), event)
        # Saved partial/error replies and possible acceptance survive failure.
        need(known, "REFERENCE_WORKFLOW_UNKNOWN_CPU_FULL_GRANT_CHARGED")
        observed_exit = supervision.get("child_exit_code")
        need(type(observed_exit) is int, "REFERENCE_WORKFLOW_UNCLEAN_SUPERVISION_MISSING_EXIT")
        self.h.clean(supervision, exit_code=observed_exit)
        need(observed_exit == (1 if refused else 0),
             "REFERENCE_WORKFLOW_CLEAN_COMMAND_EXIT_MISMATCH:"+str(observed_exit))
        need(self.h.read(self.output/"calls"/label/"stderr.txt", MIB) == b"", "REFERENCE_WORKFLOW_STDERR")
        result = event["public_result"]
        if refused:
            need(type(result) is dict and result.get("ok") is False and
                 result.get("operation") == operation and result.get("phase") == "CONTRIBUTE_REFERENCE" and
                 result.get("error_type") == "AuthoringError" and result.get("accepted") is None and
                 not result.get("close_errors"), "REFERENCE_WORKFLOW_EXPECTED_REFUSAL_REPLY")
            self.check()
            return result
        need(type(result) is dict and result.get("ok") is True and not result.get("close_errors") and
             result["operation"] == operation and result["implementation_id"] == IMPLEMENTATION and
             result["profile_sha256"] == self.args.profile_sha256 and result["store_id"] == self.store and
             result["catalog"] == str(self.catalog) and result["custody"] == str(self.custody),
             "REFERENCE_WORKFLOW_PUBLIC_REPLY")
        self.check()
        return result["result"]

    def evidence(self, result, directory, names, parent, delta):
        h = self.h
        need(result == self.document(directory/"RESULT.json") and
             result["admission"] == self.document(directory/"ADMISSION.json") and
             result["status"] == "CHECKED_REFERENCE_SOURCE_CONTRIBUTION" and
             result["parent_root"] == parent and result["local_root"] != parent and
             result["local_root"] == result["admission"]["local_root"] and
             result["reference_id"] == self.reference_id and result["parent_delta_id"] == delta and
             [row["name"] for row in result["targets"]] == [h.name(name) for name in names] and
             1 <= len(result["units"]) <= 32 and result["original_proofs_reconstructed_for_authoring"] is False,
             "REFERENCE_WORKFLOW_CONTRIBUTION_BINDING")
        by_name, unit_ids, inventories = {}, [], []
        for row in result["units"]:
            path = directory/"evidence"/(row["unit_id"]+".json")
            need(row["file"] == str(path), "REFERENCE_WORKFLOW_EVIDENCE_PATH")
            self.hold(path, {k: row[k] for k in ("bytes", "sha256")})
            raw = h.read(path, 4*MIB)
            need(h.identity("DMKN-ORDINARY-EVIDENCE-V2", raw) == row["unit_id"] and
                 row["unit_id"] not in self.static["units"] and row["unit_id"] not in unit_ids,
                 "REFERENCE_WORKFLOW_NEW_UNIT_ID")
            doc = h.diagnostic_json(raw)
            need(doc["schema"] == "DMKN_LEAN_ORDINARY_EVIDENCE_V2" and doc["semantic_id"] == SEMANTIC,
                 "REFERENCE_WORKFLOW_NEW_UNIT_SCHEMA")
            unit_ids.append(row["unit_id"])
            for entry in doc["unit"][2]:
                key = h.canonical(entry[0])
                need(key not in by_name and key not in self.static["bindings"], "REFERENCE_WORKFLOW_NO_OLD_REDECLARATION")
                by_name[key] = (row["unit_id"], doc, entry)
                inventories.append(entry[0])
        self.h.Smoke.admission(self, result["admission"], unit_ids, inventories)
        for target in result["targets"]:
            unit, _, entry = by_name[h.canonical(target["name"])]
            need(target["unit_id"] == unit and entry[1] == 2 and target["export_id"] ==
                 h.identity("DMKN-ORDINARY-EXPORT-V2", h.canonical([SEMANTIC, unit, target["name"]])),
                 "REFERENCE_WORKFLOW_THEOREM_EXPORT_ID")
        self.confirmed.append(result["local_root"])
        self.capture_tree(directory)
        return by_name

    def dependency(self, by_name, theorem, target):
        h = self.h
        _, doc, entry = by_name[h.canonical(h.name(theorem))]
        need([target["name"], target["export_id"]] in doc["imports"], "REFERENCE_WORKFLOW_EXACT_REUSE_IMPORT")
        body = entry[4][0]
        need(body[0] == "DMKN_LEAN_ORIGINAL_EXPR_V1" and any(type(node) is list and
             len(node) == 3 and node[0] == 2 and node[1] == target["name"] for node in body[2]),
             "REFERENCE_WORKFLOW_PROOF_ACTUALLY_USES_IMPORT")

    def run(self, report):
        h = self.h
        basis, parent = BASIS_ROOT, INTAKE_ROOT
        report.update(basis_root=basis, retained_intake_root=parent,
                      retained_predecessor_sha256=PREVIOUS_PINS["workflow/WORKFLOW.json"],
                      repeated_initialization=False, repeated_intake=False)
        bundle_args = ("--bundle-directory", RETAINED/"bundle", "--bundle-manifest", RETAINED/"bundle/manifest.json",
                       "--bundle-manifest-sha256", MANIFEST)
        report["phase"] = "REGISTER"
        reference = self.call("register-reference", ("--parent-root", parent, *bundle_args,
            "--reference-targets", self.fixtures/"reference-targets.json",
            "--reference-project", RETAINED/"project-selection.json", "--reference-project-sha256", PROJECT,
            "--reference-artifact-report", RETAINED/"artifact-report.json", "--reference-artifact-report-sha256", ARTIFACTS,
            "--retained-snapshot-operation", ORIGIN, "--retained-snapshot-sha256", SNAPSHOT))
        need(reference["status"] == "REGISTERED_LOCAL_ORIGINAL_REFERENCE" and
             reference["source_context_root"] == parent and reference["native_calls"] == 1 and
             reference["snapshot_id"] == SNAPSHOT and reference["retained_snapshot_operation"] == ORIGIN and
             reference["public_units"] == 5 and reference["public_names"] == 8 and
             reference["usable_basis_names"] == 522 and reference["new_catalog_acceptance"] is False,
             "REFERENCE_WORKFLOW_REAL_REFERENCE")
        self.reference_id = reference["reference_id"]; report["reference"] = reference
        report["phase"] = "AUTHOR_A"
        first = self.call("contribute-reference", ("--parent-root", parent, "--reference-id", self.reference_id,
            "--source", self.fixtures/"A.lean", "--output-names", self.fixtures/"A-targets.json",
            "--output", self.output/"author-A"))
        a = self.evidence(first, self.output/"author-A", A_NAMES, parent, "")
        self.dependency(a, A_NAMES[0], self.reference_targets[1])
        report["contribution_A"] = first
        targets = self.fixture("delta-targets.json", first["targets"])
        report["phase"] = "DELTA_A"
        delta = self.call("export-reference-delta", ("--parent-root", first["local_root"],
            "--reference-id", self.reference_id, "--reference-targets", targets))
        need(delta["status"] == "CHECKED_AND_REGISTERED_LOCAL_REFERENCE_DELTA" and
             delta["reference_id"] == self.reference_id and delta["parent_delta_id"] == "" and
             delta["source_context_root"] == first["local_root"] and delta["snapshot_id"] == reference["snapshot_id"] and
             delta["targets"] == sorted(first["targets"], key=lambda row: h.canonical(row["name"])) and
             set(delta["ordered_unit_ids"]) == {row["unit_id"] for row in first["units"]} and
             not set(delta["ordered_unit_ids"]).intersection(self.static["units"]) and
             delta["new_catalog_acceptance"] is False and delta["native_calls"] == 3,
             "REFERENCE_WORKFLOW_NEW_ONLY_DELTA")
        report["delta_A"] = delta
        report["phase"] = "AUTHOR_B"
        second = self.call("contribute-reference", ("--parent-root", first["local_root"],
            "--reference-id", self.reference_id, "--parent-delta-id", delta["delta_id"],
            "--source", self.fixtures/"B.lean", "--output-names", self.fixtures/"B-targets.json",
            "--output", self.output/"author-B"))
        b = self.evidence(second, self.output/"author-B", B_NAMES, first["local_root"], delta["delta_id"])
        a_involution = next(row for row in first["targets"] if row["name"] == h.name(A_NAMES[1]))
        self.dependency(b, B_NAMES[0], a_involution)
        self.dependency(b, B_NAMES[1], self.reference_targets[1])
        need(not {row["unit_id"] for row in first["units"]}.intersection(row["unit_id"] for row in second["units"]),
             "REFERENCE_WORKFLOW_B_NOT_A_REPLAY")
        setup = self.document(self.output/"author-B/setup.json", 20*MIB)
        need(setup["imports"] == [{"module": delta["module_name"], "importAll": False,
              "isExported": True, "isMeta": False}] and delta["module_name"] in setup["importArts"],
             "REFERENCE_WORKFLOW_B_IMPORTS_GENERATED_DELTA")
        report["contribution_B"] = second
        report["phase"] = "REFUSE_SORRY"
        bad = self.output/"author-refused"
        refusal = self.call("contribute-reference", ("--parent-root", second["local_root"],
            "--reference-id", self.reference_id, "--parent-delta-id", delta["delta_id"],
            "--source", self.fixtures/"False.lean", "--output-names", self.fixtures/"False-targets.json",
            "--output", bad), refused=True)
        failure = self.document(bad/"FAILURE.json")
        need(failure == refusal["detail"] and failure["phase"] == "EXTRACT_NEW_MATHEMATICS" and
             failure["error_type"] == "ExchangeError" and failure["accepted"] is None and
             failure["admission_entered"] is False and failure["possible_unreported_commit"] is False and
             failure["accounting_errors"] == [], "REFERENCE_WORKFLOW_PRE_ADMISSION_REFUSAL")
        # Compile success (including all five actual artifact parts) is necessary:
        # an unavailable import or parser failure does not test the trust boundary.
        self.native(bad/"AUTHORING-SUPERVISION.json")
        compiled = self.document(bad/"author-report.json")
        need(compiled["schema"] == "DMKN_ORDINARY_REFERENCE_AUTHOR_OUTPUT_V1" and
             compiled["assurance"] == "OWNER_APPROVED_SOURCE_OUTPUT_NOT_MATHEMATICAL_ACCEPTANCE" and
             len(compiled["artifact_parts"]) == 5, "REFERENCE_WORKFLOW_REFUSAL_COMPILED")
        artifact_paths = []
        for part in compiled["artifact_parts"]:
            path = Path(part["path"])
            need(path.parent == bad/"modules" and path.name.startswith(compiled["module_name"]),
                 "REFERENCE_WORKFLOW_REFUSAL_ARTIFACT_LOCATION")
            self.hold(path, {key: part[key] for key in ("bytes", "sha256")}, 64*MIB)
            artifact_paths.append(path.name)
        need(set(artifact_paths) == {compiled["module_name"]+suffix for suffix in h.PARTS},
             "REFERENCE_WORKFLOW_REFUSAL_FIVE_PARTS")
        exchange = self.document(bad/"extraction/EXTRACTION-SUPERVISION.json")
        final = exchange.get("final_job", {})
        need(exchange == failure["stage_detail"] and exchange["status"] == "EXTRACTION_FAILED" and
             exchange["child_exit_code"] != 0 and exchange["child_exit_code"] is not None and
             exchange["direct_child_reaped"] is True and exchange["job_closed"] is True and
             exchange["job_attach_resume_completed"] is True and exchange["threads_joined"] is True and
             exchange["cleanup_errors"] == [] and exchange["accounting_complete"] is True and
             exchange["done"] is None and final["active_processes"] == 0 and final["total_processes"] >= 1 and
             type(final["cpu_seconds"]) in (int, float) and math.isfinite(final["cpu_seconds"]) and
             0 <= final["cpu_seconds"] == exchange["native_cpu_seconds"] <= exchange["limits"]["cpu_seconds"],
             "REFERENCE_WORKFLOW_REFUSAL_CLOSED_AND_ACCOUNTED")
        stderr = h.read(bad/"extraction/native.stderr.txt", MIB)
        need(b"ORDINARY_EXTENSION SORRY_REFERENCE" in stderr,
             "REFERENCE_WORKFLOW_REQUIRED_SEMANTIC_REFUSAL")
        need(not any((bad/name).exists() for name in ("candidate.json", "ADMISSION.json", "RESULT.json")),
             "REFERENCE_WORKFLOW_REFUSAL_NO_CANDIDATE_OR_ADMISSION")
        self.capture_tree(bad)
        report["refusal"] = {"public_reply": refusal, "compiled_parts": compiled["artifact_parts"],
            "native_refusal_stderr_sha256": h.sha(stderr), "extraction": exchange,
            "claim": "COMPILER_SUCCESS_IS_NOT_AUTHORITY_SORRY_DEPENDENCY_REJECTED_BEFORE_ADMISSION"}
        report["phase"] = "STATUS_AFTER_REFUSAL"
        status = self.call("status", ("--context-root", second["local_root"], "--limit", "32"))
        expected_roots = [{"local_root": root, "parent_root": "" if index == 0 else self.confirmed[index-1]}
                          for index, root in enumerate(self.confirmed)]
        need(status["status"] == "LOCAL_OWNER_OPEN" and status["basis_root_identity"] == basis and
             status["roots"] == sorted(expected_roots, key=lambda row: row["local_root"]) and
             status["has_more"] is False and status["next_after_root"] is None and
             status["selected_context"]["local_root"] == second["local_root"],
             "REFERENCE_WORKFLOW_EXACT_FOUR_ROOTS_AFTER_REFUSAL")
        report["final_status"] = status
        need(len(self.calls) == 6 and len(self.confirmed) == 4, "REFERENCE_WORKFLOW_EXACT_OPERATIONS")
        report.update(status="PASS_RETAINED_PUBLIC_REFERENCE_RECIPROCAL_CONTINUATION_NOT_FINAL_V5",
                      phase="COMPLETE", final_root=second["local_root"],
                      new_mathematical_targets=4, original_fixture_recompiled=False, snapshot_recopied=False,
                      old_diagnostic_correspondence_rerun=False,
                      claim="REAL_LOCAL_ADMISSION_REFERENCE_NORMAL_SOURCE_DELTA_REUSE_NOT_GROWTH_OR_GLOBAL_DEPLOYMENT")

    def finish(self, report):
        report.update(calls=self.calls, confirmed_roots=self.confirmed,
            wall_seconds=time.monotonic()-self.started,
            controller_cpu_seconds=time.process_time()-self.cpu_started,
            charged_whole_child_job_cpu_seconds=self.charged,
            cpu_accounting_complete=self.complete,
            retention="ALL_INPUTS_ACCEPTED_STATE_AND_PARTIAL_OUTPUT_PRESERVED_NO_AUTOMATIC_RETRY")
        if self.output_created:
            self.h.save(self.output/"WORKFLOW.json", report)
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("profile-sha256", "assembly-sha256", "output"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+name, required=True, type=int)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and args.wall_seconds == 480 and
         args.cpu_seconds == 330 and args.memory_mib == 1536, "REFERENCE_WORKFLOW_CONTEXT_AND_FIXED_BUDGET")
    for digest in (args.profile_sha256, args.assembly_sha256):
        need(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest), "REFERENCE_WORKFLOW_HASH")
    h = helpers(); workflow = Workflow(args, h)
    report = {"schema": "DMKN_ORDINARY_REFERENCE_PUBLIC_CONTINUATION_V1", "status": "FAILED", "phase": "PREPARE"}
    try:
        workflow.prepare(); workflow.run(report)
        for path, expected in workflow.held.items():
            need(h.pin(Path(path), workflow.check, 128*MIB) == expected, "REFERENCE_WORKFLOW_FINAL_PIN")
    except BaseException as error:
        report.update(status="FAILED", error_type=type(error).__name__, error=str(error)[:4096])
    workflow.finish(report)
    print(json.dumps({k: v for k, v in report.items() if k != "calls"}, sort_keys=True, allow_nan=False), flush=True)
    return 0 if report["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())


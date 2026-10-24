"""Three public calls for approved-project extraction; no runtime until selected.

Uses one already-paid controlled module and the saved owner's initial basis.
Preserves prior immutable files. No initialization, helper/module rebuild,
anchor use/migration, state copy, network or claimed external-user/growth result.
Requires an enclosing finite Windows Job; all child CPU is charged once.
"""
from __future__ import annotations

import time
BOOT_WALL, BOOT_CPU = time.monotonic(), time.process_time()
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PACKAGE = LOCAL/"ordinary-project-extraction-build-01/integration/package"
SAVED = LOCAL/"ordinary-current-relocated-smoke-01/smoke"
REGISTRY = SAVED/"catalog/module-anchors-v1"
PYTHON = Path(r"D:\Python314\python.exe")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
HELPER = ROOT/"software/v5/ordinary_distribution/relocated_smoke.py"
HELPER_PIN = {"bytes": 38940, "sha256": "aaba6e2e30906414f539842fd7678aaaf3ab7f9c077b30c6f115db7407584831"}
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
BASIS = "8c74aadc460b8efdbfedfa4f6a2468c93dc8c7b617b65870040cbbe22a0c2e8e"
STORE = "c60f943f157cccf4c4be478cc2b600b609f79e81084fda3eca691ef0ccbddfeb"
MODULE = "DMKNBridge_9609cb4a4b9392e37ec5ffccbc6d66121eb23be6107d9f12cb48f58fa9b4f215"
MODULE_PIN = "4e3abb741add01af00a4300542420ae6c67e313be3567f299d7186cc8fdde3d5"
TARGET = "CommonsProjectIntake.applyFour_eq"
MISSING = ("CommonsPackageExample.applyTwice", "CommonsPackageExample.applyTwice_eq")
CHANGED = {"owner.py", "authoring/py/library_extraction.py", "authoring/bin/MissingImportExporter.exe"}
CAPS = {"01-contribute": (70, 30), "02-extract-project": (60, 25), "03-complete": (80, 35)}
MIB = 1024**2
BODY = b"""universe u

theorem CommonsProjectIntake.applyFour_eq {a : Type u} (f : a -> a) (x : a) :
    CommonsPackageExample.applyTwice f (CommonsPackageExample.applyTwice f x) =
      f (f (f (f x))) :=
  Eq.trans (CommonsPackageExample.applyTwice_eq f (CommonsPackageExample.applyTwice f x))
    (congrArg (fun y => f (f y)) (CommonsPackageExample.applyTwice_eq f x))
"""


def need(ok, code):
    if not ok:
        raise ValueError(code)


def helpers():
    with HELPER.open("rb") as stream:
        raw = stream.read(HELPER_PIN["bytes"]+1)
    need(len(raw) == HELPER_PIN["bytes"] and hashlib.sha256(raw).hexdigest() == HELPER_PIN["sha256"],
         "PROJECT_CHECK_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_project_check_helpers", HELPER)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(HELPER), "exec"), module.__dict__)
    module.ordinary(HELPER)
    return module


class Check:
    def __init__(self, args, h):
        self.args, self.h = args, h
        self.started, self.cpu_started = BOOT_WALL, BOOT_CPU
        self.deadline, self.charged = self.started+args.wall_seconds, 0.0
        self.calls, self.held, self.cpu_complete, self.output_created = [], {}, True, False

    def check(self):
        need(time.monotonic() < self.deadline and
             time.process_time()-self.cpu_started+self.charged < self.args.cpu_seconds,
             "PROJECT_CHECK_ORIGINAL_ALLOWANCE")

    def hold(self, path, expected=None):
        pin = self.h.pin(path, self.check)
        need(expected is None or pin == expected, "PROJECT_CHECK_EXACT_PIN:"+str(path))
        need(self.held.setdefault(str(path), pin) == pin, "PROJECT_CHECK_IMMUTABLE_CHANGED")
        return pin

    def document(self, path, maximum=8*MIB):
        self.check()
        return self.h.diagnostic_json(self.h.read(path, maximum))

    def save(self, path, value):
        return self.hold(path, self.h.save(path, value))

    def tree(self, root):
        return self.h.Smoke.capture_tree(self, root)

    def saved_tree(self):
        # The two exact mutable SQL stores are not immutable evidence. No DB is
        # opened here. All other saved files, including owner.lock and anchors,
        # are hash-held; existing transient journals would refuse this selection.
        excluded = {SAVED/"catalog/catalog.sqlite", SAVED/"custody/ordinary.sqlite"}
        pending, entries, result = [self.h.ordinary(SAVED, directory=True)], 0, set()
        while pending:
            folder = pending.pop()
            with os.scandir(folder) as listing:
                for entry in listing:
                    self.check(); entries += 1
                    need(entries <= 2048, "PROJECT_CHECK_SAVED_CENSUS")
                    path = Path(entry.path)
                    need(len(path.relative_to(SAVED).parts) <= 10, "PROJECT_CHECK_SAVED_DEPTH")
                    if entry.is_dir(follow_symlinks=False):
                        pending.append(self.h.ordinary(path, directory=True))
                    else:
                        self.h.ordinary(path)
                        need(not path.name.endswith(("-journal", "-wal", "-shm")),
                             "PROJECT_CHECK_UNSETTLED_SAVED_STORE")
                        if path not in excluded:
                            self.hold(path); result.add(path.relative_to(SAVED).as_posix())
        return result

    def prepare(self):
        h, args = self.h, self.args
        self.package = h.ordinary(args.package, directory=True)
        self.output = h.ordinary(args.output, directory=True, fresh=True)
        need(self.package == PACKAGE and self.output.is_relative_to(LOCAL),
             "PROJECT_CHECK_SELECTED_PATHS")
        self.runtimes = {"python_runtime": h.ordinary(PYTHON.parent, directory=True),
                         "lean_runtime": h.ordinary(LEAN, directory=True)}
        roots = [self.package, self.output, SAVED, *self.runtimes.values()]
        need(all(not a.is_relative_to(b) and not b.is_relative_to(a)
                 for i, a in enumerate(roots) for b in roots[i+1:]), "PROJECT_CHECK_DISJOINT_ROOTS")
        self.hold(Path(__file__).resolve()); self.hold(HELPER, HELPER_PIN)
        for value in (args.profile_sha256, args.assembly_sha256):
            need(re.fullmatch(r"[0-9a-f]{64}", value), "PROJECT_CHECK_HASH")
        raw = h.read(self.package/"PROFILE.json", 2*MIB)
        need(h.sha(raw) == args.profile_sha256, "PROJECT_CHECK_PROFILE_PIN")
        self.profile = h.diagnostic_json(raw)
        need(set(self.profile) == {"schema", "files", "installation_manifest_sha256", "helper_paths", "author_worker"}
             and self.profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1"
             and self.profile["installation_manifest_sha256"] == INSTALLATION,
             "PROJECT_CHECK_PROFILE")
        manifest_raw = h.read(self.package/"installation/INSTALLATION.json", 2*MIB)
        need(h.sha(manifest_raw) == INSTALLATION, "PROJECT_CHECK_UNCHANGED_INSTALLATION")
        self.manifest = h.diagnostic_json(manifest_raw)
        self.semantic, self.implementation = SEMANTIC, IMPLEMENTATION
        need(self.manifest["implementation"]["semantic_id"] == SEMANTIC and
             h.identity("DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1",
                        h.canonical(self.manifest["implementation"])) == IMPLEMENTATION,
             "PROJECT_CHECK_IMPLEMENTATION")
        payload = dict(self.profile["files"])
        for logical, pin in self.manifest["files"].items():
            parts = h.relative(logical).parts
            if parts[0] in self.runtimes:
                self.hold(self.runtimes[parts[0]].joinpath(*parts[1:]), pin)
            else:
                payload["installation/"+logical] = pin
        payload["installation/INSTALLATION.json"] = {"bytes": len(manifest_raw), "sha256": INSTALLATION}
        need(len(payload) == 134, "PROJECT_CHECK_PAYLOAD_CENSUS")
        receipt_raw = h.read(self.package/"ASSEMBLY.json", 2*MIB)
        need(h.sha(receipt_raw) == args.assembly_sha256, "PROJECT_CHECK_ASSEMBLY_PIN")
        receipt = h.diagnostic_json(receipt_raw)
        need(receipt["status"] == "ASSEMBLED_NOT_ADOPTED" and
             receipt["profile_sha256"] == args.profile_sha256 and
             receipt["installation_manifest_sha256"] == INSTALLATION and
             receipt["implementation_id"] == IMPLEMENTATION and
             receipt["files_excluding_profile"] == 134 and
             set(receipt["changed"]) == CHANGED and receipt["added"] == [] and
             receipt["changed_or_added"] == {name: payload[name] for name in CHANGED},
             "PROJECT_CHECK_ASSEMBLY_BINDING")
        payload["PROFILE.json"] = {"bytes": len(raw), "sha256": args.profile_sha256}
        payload["ASSEMBLY.json"] = {"bytes": len(receipt_raw), "sha256": args.assembly_sha256}
        for logical, pin in payload.items():
            self.hold(self.package/h.relative(logical), pin)
        need(self.tree(self.package) == set(payload), "PROJECT_CHECK_PACKAGE_TREE")
        self.before_saved = self.saved_tree()
        self.before_registry = self.tree(REGISTRY)
        adoption = self.document(SAVED/"catalog/ADOPTION.json")
        need(adoption["store_id"] == STORE and adoption["implementation"] == self.manifest["implementation"],
             "PROJECT_CHECK_EXISTING_ADOPTION")
        initial = self.document(SAVED/"init/stdout.txt")
        need(initial["ok"] is True and initial["result"]["basis"]["local_root"] == BASIS,
             "PROJECT_CHECK_SELECTED_INITIAL_BASIS")
        basis_report_path = SAVED/("catalog/admission-calls/"
            "5738b0360d4a5a233ec2f84fdef0c3950f521bde72b93e6b403e8470c40fc9ed/worker-report.json")
        need(self.hold(basis_report_path)["sha256"] ==
             "d939807af438541e98a52c3ad0f2eeb1b09cad8180b54a57aa6109600c4702a6",
             "PROJECT_CHECK_ORIGINAL_BASIS_REPORT")
        basis_report = self.document(basis_report_path)
        basis_names = {h.canonical(name) for name in basis_report["names"]}
        need(basis_report["kind"] == "basis" and len(basis_names) == 581 and
             {h.canonical(h.name(name)) for name in ("Eq", "Eq.refl", "Eq.trans", "congrArg")} <= basis_names and
             all(h.canonical(h.name(name)) not in basis_names for name in MISSING),
             "PROJECT_CHECK_TWO_MISSING_SOURCE_PRECONDITION")
        module_raw = h.read(SAVED/"export/MODULE.json", MIB)
        module = h.diagnostic_json(module_raw)
        need(h.sha(module_raw) == MODULE_PIN and module["module_name"] == MODULE and
             module["status"] == "CHECKED_PROOF_COMPLETE_LOCAL_MODULE", "PROJECT_CHECK_PAID_MODULE")
        expected_parts = {MODULE+suffix for suffix in h.PARTS}
        need(set(module["artifact_parts"]) == expected_parts and
             self.tree(SAVED/"export/modules") == expected_parts, "PROJECT_CHECK_MODULE_PARTS")
        for filename, pin in module["artifact_parts"].items():
            self.hold(SAVED/"export/modules"/filename, pin)
        roles = self.manifest["roles"]
        def helper(role, module):
            logical = roles[role]
            need(logical.startswith("supervisor/"), "PROJECT_CHECK_SUPERVISOR_ROLE")
            return h.load_exact(self.package/"installation"/h.relative(logical), module,
                                self.manifest["files"][logical], self.check)
        self.supervisor = helper("supervisor", "_project_check_supervisor")
        helper("domains", "domains")
        self.jobs = helper("job", "_project_check_jobs")
        self.catalog, self.custody = SAVED/"catalog", SAVED/"custody"
        self.output.mkdir(); self.output_created = True
        self.fixtures = self.output/"fixtures"; self.fixtures.mkdir()
        (self.output/"calls").mkdir(); (self.output/"project-workspace").mkdir()
        self.outputs = [h.name(TARGET)]
        self.missing = sorted((h.name(name) for name in MISSING), key=h.canonical)
        self.project = {"schema": "DMKN_ORDINARY_TRUSTED_PROJECT_AUTHORING_V1",
            "module_name": "CommonsProjectIntake", "project_cwd": str(self.output/"project-workspace"),
            "project_search_paths": [str(SAVED/"export/modules")],
            "imports": [{"module": MODULE, "meta": False}]}
        self.extraction = {"schema": "DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1",
            "project_search_paths": [str(SAVED/"export/modules")], "modules": [h.name(MODULE)]}
        self.fixture_pins = {filename: self.save(self.fixtures/filename, value)
            for filename, value in {"body.lean": BODY, "acquired.json": [], "outputs.json": self.outputs,
                "project.json": self.project, "extraction.json": self.extraction}.items()}
        self.save(self.output/"PRESERVED-BEFORE.json", {
            "saved_immutable_files": sorted(self.before_saved),
            "anchor_files": sorted(self.before_registry), "pins": self.held.copy(),
            "mutable_stores": ["catalog/catalog.sqlite", "custody/ordinary.sqlite"]})

    def owner(self, label, operation, extra, *, expected_exit=0):
        self.check()
        need(label in CAPS and not any(row["label"] == label for row in self.calls),
             "PROJECT_CHECK_FINITE_CALLS")
        wall, cpu = CAPS[label]
        grant = self.supervisor.limits_checked({
            "wall_seconds": min(wall, math.floor(self.deadline-time.monotonic())-20),
            "cpu_seconds": min(cpu, math.floor(self.args.cpu_seconds-self.charged-
                (time.process_time()-self.cpu_started))-3),
            "memory_mib": self.args.memory_mib, "active_processes": 8,
            "stdout_bytes": 8*MIB, "stderr_bytes": 8*MIB})
        need(grant["wall_seconds"] >= 40 and grant["cpu_seconds"] >= 5,
             "PROJECT_CHECK_REMAINING_GRANT")
        argv = [str(PYTHON), "-I", "-S", "-B", str(self.package/"owner.py"), operation,
            "--profile-sha256", self.args.profile_sha256, "--python-runtime", str(PYTHON.parent),
            "--lean-runtime", str(LEAN), "--catalog", str(self.catalog), "--custody", str(self.custody),
            "--store-id", STORE, "--custody-limits", str(SAVED/"fixtures/custody-limits.json"),
            "--wall-seconds", str(grant["wall_seconds"]-5), "--cpu-seconds", str(grant["cpu_seconds"]-1),
            "--memory-mib", str(self.args.memory_mib), "--parent-root", BASIS, *map(str, extra)]
        event = {"label": label, "argv": argv, "limits": grant, "public_result": None,
                 "cpu_complete": False, "charged_cpu_seconds": grant["cpu_seconds"]}
        self.calls.append(event)
        supervision = None
        try:
            supervision = self.supervisor.supervise(argv, self.output,
                self.output/"calls"/label, grant, self.jobs.Job)
            event["supervision"] = supervision
        finally:
            final = supervision.get("final_job") if type(supervision) is dict else None
            observed = final.get("cpu_seconds") if type(final) is dict else None
            known = type(observed) in (int, float) and math.isfinite(observed) and observed >= 0
            charged = observed if known else grant["cpu_seconds"]
            self.charged += charged; self.cpu_complete = self.cpu_complete and known
            event.update(cpu_complete=known, charged_cpu_seconds=charged)
            self.h.save(self.output/"calls"/(label+"-SUPERVISION.json"), event)
        # Retain an actual accepted result before asserting later success. A
        # failed harness is not evidence that the mathematical commit rolled back.
        raw = self.h.read(self.output/"calls"/label/"stdout.txt", 8*MIB)
        if raw:
            event["public_result"] = self.h.diagnostic_json(raw)
        need(known, "PROJECT_CHECK_UNKNOWN_CPU_FULL_GRANT_CHARGED")
        self.h.clean(supervision, exit_code=expected_exit)
        need(self.h.read(self.output/"calls"/label/"stderr.txt", MIB) == b"", "PROJECT_CHECK_CHILD_STDERR")
        public = event["public_result"]
        need(type(public) is dict and public.get("ok") is (expected_exit == 0) and
             public.get("operation") == operation and not public.get("close_errors"),
             "PROJECT_CHECK_PUBLIC_RESULT")
        if expected_exit == 0:
            need(public["store_id"] == STORE and public["catalog"] == str(self.catalog) and
                 public["custody"] == str(self.custody) and public["profile_sha256"] == self.args.profile_sha256 and
                 public["implementation_id"] == IMPLEMENTATION, "PROJECT_CHECK_PUBLIC_BINDING")
        self.check()
        return public

    def native(self, path, *, extraction=False):
        return self.h.Smoke.native(self, path, extraction=extraction)

    def capture_tree(self, root):
        return self.tree(root)

    def run(self, report):
        h = self.h
        missing, extraction, completion = (self.output/name for name in ("missing", "extraction", "completion"))
        report["phase"] = "PUBLIC_PROJECT_CONTRIBUTION"
        refused = self.owner("01-contribute", "contribute", (
            "--source", self.fixtures/"body.lean", "--acquired-targets", self.fixtures/"acquired.json",
            "--output-names", self.fixtures/"outputs.json", "--project-authoring", self.fixtures/"project.json",
            "--project-authoring-sha256", self.fixture_pins["project.json"]["sha256"],
            "--output", missing), expected_exit=1)
        detail = refused.get("detail", {})
        need(refused.get("accepted") is None and refused.get("phase") == "CONTRIBUTE" and
             detail.get("phase") == "BINDING" and detail.get("accepted") is None and
             detail.get("error") == "CONTRIBUTION_CANDIDATE_NEEDS_INTERPRETATIONS" and
             detail.get("needs_local_interpretations") == self.missing and
             self.document(missing/"FAILURE.json") == detail, "PROJECT_CHECK_EXPECTED_MISSING")
        self.native(missing/"AUTHORING-SUPERVISION.json")
        candidate_raw, request_raw = h.read(missing/"candidate.json"), h.read(missing/"REQUEST.json")
        candidate, request = h.diagnostic_json(candidate_raw), h.diagnostic_json(request_raw)
        need(request["parent_root"] == BASIS and request["source_body_sha256"] == h.sha(BODY) and
             request["output_names"] == self.outputs and request["acquired_targets"] == [] and
             request["project_authoring"]["configuration"] == self.project and
             candidate["context_root"] == BASIS and candidate["targets"] == self.outputs and
             len(candidate["units"]) == 1, "PROJECT_CHECK_RETAINED_REQUEST")
        self.tree(missing)
        report["phase"] = "PUBLIC_PROJECT_EXTRACTION"
        extracted = self.owner("02-extract-project", "extract-project", (
            "--retained-contribution", missing, "--retained-request-sha256", h.sha(request_raw),
            "--retained-candidate-sha256", h.sha(candidate_raw), "--project-extraction", self.fixtures/"extraction.json",
            "--project-extraction-sha256", self.fixture_pins["extraction.json"]["sha256"],
            "--output", extraction))["result"]
        need(extracted == self.document(extraction/"EXTRACTION-RESULT.json") and
             extracted["status"] == "EXTRACTED_COMPLETION_INPUTS_NOT_ACCEPTED" and
             extracted["mathematical_acceptance"] is False and extracted["parent_root"] == BASIS and
             extracted["missing_targets"] == self.missing and extracted["supplemental_units"] == 2 and
             extracted["consumer_units"] == 1 and extracted["modules"] == self.extraction["modules"] and
             extracted["project_search_paths"] == self.extraction["project_search_paths"] and
             extracted["project_selection_sha256"] == self.fixture_pins["extraction.json"]["sha256"] and
             extracted["trust_boundary"] == "OWNER_APPROVED_LOCAL_PROJECT_PRIVATE_ARTIFACTS_NOT_PEER_BINARIES",
             "PROJECT_CHECK_EXACT_EXTRACTION")
        native = self.native(extraction/"EXTRACTION-SUPERVISION.json", extraction=True)
        need(native["argv"][0] == str(self.package/"authoring/bin/MissingImportExporter.exe") and
             native["native_cpu_seconds"] == extracted["native_cpu_seconds"], "PROJECT_CHECK_EXTRACTION_EVENT")
        pins = extracted["pins"]
        for key, filename in (("candidate", "candidate.json"), ("targets", "targets.json"),
                ("prepared_bindings", "prepared-bindings.json"), ("extraction_request", "request.json"),
                ("project_selection", "project-selection.json"), ("supplement", "supplement.json")):
            self.hold(extraction/filename, pins[key])
        native_request = self.document(extraction/"request.json")
        need(native_request == {"schema": "DMKN_ORDINARY_PROJECT_MISSING_IMPORT_REQUEST_V1",
            "profile_id": SEMANTIC, "context_id": BASIS,
            "basis_id": candidate["foundation_id"], "modules": self.extraction["modules"],
            "targets": self.missing, "project_search_paths": self.extraction["project_search_paths"],
            "project_selection_sha256": pins["project_selection"]["sha256"],
            "capacity": extracted["capacity"]}, "PROJECT_CHECK_PROJECT_REQUEST")
        need(h.read(extraction/"candidate.json") == candidate_raw and
             h.read(extraction/"project-selection.json") == h.read(self.fixtures/"extraction.json") and
             self.document(extraction/"targets.json") == self.outputs, "PROJECT_CHECK_UNCHANGED_SELECTION")
        self.tree(extraction)
        report["phase"] = "PUBLIC_SAME_PARENT_COMPLETION"
        completed = self.owner("03-complete", "complete", (
            "--candidate", extraction/"candidate.json", "--candidate-sha256", pins["candidate"]["sha256"],
            "--supplement", extraction/"supplement.json", "--supplement-sha256", pins["supplement"]["sha256"],
            "--prepared-bindings", extraction/"prepared-bindings.json",
            "--prepared-bindings-sha256", pins["prepared_bindings"]["sha256"],
            "--output-names", extraction/"targets.json", "--output", completion))["result"]
        report["accepted"] = completed["admission"]
        need(completed == self.document(completion/"RESULT.json") and
             completed["admission"] == self.document(completion/"ADMISSION.json") and
             completed["status"] == "CHECKED_COMPLETION_WITH_DURABLE_PUBLICATION_BYTES" and
             completed["parent_root"] == BASIS and completed["local_root"] != BASIS and
             completed["admission"]["local_root"] == completed["local_root"] and
             completed["candidate_sha256"] == h.sha(candidate_raw) and
             completed["supplement_sha256"] == pins["supplement"]["sha256"] and
             completed["semantic_id"] == SEMANTIC and completed["implementation_id"] == IMPLEMENTATION and
             len(completed["units"]) == 3 and [row["name"] for row in completed["targets"]] == self.outputs and
             len(completed["previews"]) == 1 and h.read(completion/"candidate.json") == candidate_raw,
             "PROJECT_CHECK_CHECKED_COMPLETION")
        evidence, inventory, by_name = [], [], {}
        for row in completed["units"]:
            path = completion/"evidence"/(row["unit_id"]+".json")
            need(row["file"] == str(path), "PROJECT_CHECK_EVIDENCE_PATH")
            self.hold(path, {key: row[key] for key in ("bytes", "sha256")})
            raw = h.read(path); doc = h.diagnostic_json(raw)
            need(h.identity("DMKN-ORDINARY-EVIDENCE-V2", raw) == row["unit_id"] and
                 doc["semantic_id"] == SEMANTIC, "PROJECT_CHECK_EVIDENCE_ID")
            evidence.append(doc)
            for item in doc["unit"][2]:
                key = h.canonical(item[0]); need(key not in by_name, "PROJECT_CHECK_DUPLICATE_OUTPUT")
                by_name[key] = (row["unit_id"], doc, item); inventory.append(item[0])
        need(set(by_name) == {h.canonical(name) for name in [*self.missing, *self.outputs]},
             "PROJECT_CHECK_EXACT_OUTPUT_CENSUS")
        self.h.Smoke.admission(self, completed["admission"],
            [row["unit_id"] for row in completed["units"]], inventory)
        target = completed["targets"][0]
        unit_id, consumer, entry = by_name[h.canonical(self.outputs[0])]
        need(consumer["unit"] == candidate["units"][0] and target["unit_id"] == unit_id and
             target["export_id"] == h.identity("DMKN-ORDINARY-EXPORT-V2",
                h.canonical([SEMANTIC, unit_id, target["name"]])), "PROJECT_CHECK_UNCHANGED_CONSUMER")
        imports = {h.canonical(name): identity for name, identity in consumer["imports"]}
        for name in self.missing:
            key = h.canonical(name); supplying_id = by_name[key][0]
            need(imports.get(key) == h.identity("DMKN-ORDINARY-EXPORT-V2",
                h.canonical([SEMANTIC, supplying_id, name])), "PROJECT_CHECK_ACTUAL_METHOD_REUSE")
        preview = completed["previews"][0]
        preview_path = completion/"previews"/(target["export_id"]+".json")
        need(preview["file"] == str(preview_path) and all(preview[key] == value for key, value in target.items()),
             "PROJECT_CHECK_PREVIEW_TARGET")
        self.hold(preview_path, {key: preview[key] for key in ("bytes", "sha256")})
        viewed = self.document(preview_path)
        need(viewed["schema"] == "DMKN_ORDINARY_LEAN_TYPE_PREVIEW_V2" and
             viewed["semantic_id"] == SEMANTIC and viewed["unit_id"] == unit_id and
             viewed["export_name"] == target["name"] and
             viewed["header"] == entry[1:4], "PROJECT_CHECK_EXACT_PREVIEW")
        self.tree(completion)
        report["phase"] = "PRESERVATION"
        for path, pin in tuple(self.held.items()):
            self.hold(Path(path), pin)
        need(self.tree(REGISTRY) == self.before_registry, "PROJECT_CHECK_NO_ANCHOR_CHANGE")
        need(len(self.calls) == 3 and all(row["cpu_complete"] for row in self.calls),
             "PROJECT_CHECK_THREE_CALLS_CLOSED")
        self.save(self.output/"IMMUTABLE-FILES.json", self.held.copy())
        report.update(status="PASS_APPROVED_PROJECT_EXTRACTION_AND_CHECKED_COMPLETION", phase="COMPLETE",
            prior_immutable_files=len(self.before_saved), anchor_files=len(self.before_registry),
            target=target, candidate_sha256=h.sha(candidate_raw), same_parent=BASIS,
            extracted_units=2, consumer_units=1, no_anchor_use_or_migration=True)


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize and Path(sys.executable).resolve() == PYTHON, "PROJECT_CHECK_RUNTIME")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "profile-sha256", "assembly-sha256", "output"):
        parser.add_argument("--"+key, required=True)
    for key in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+key, required=True, type=int)
    args = parser.parse_args()
    need(120 <= args.wall_seconds <= 180 and 60 <= args.cpu_seconds <= 100 and
         256 <= args.memory_mib <= 1536, "PROJECT_CHECK_FINITE_ENVELOPE")
    check = Check(args, helpers())
    report = {"status": "FAILED", "phase": "PREFLIGHT", "calls": check.calls, "accepted": None,
        "claim": "CONTROLLED_LOCAL_PROJECT_INTEROPERABILITY_NOT_EXTERNAL_USER_GROWTH_OR_FINAL_V5",
        "retention": "ALL_PRIOR_AND_PARTIAL_OUTPUTS_PRESERVED_NO_RETRY"}
    try:
        check.prepare(); check.run(report)
    except BaseException as error:
        report.update(status="FAILED", error_type=type(error).__name__, error=str(error)[:2000],
            immutable_preservation="POST_FAILURE_SAVED_FILE_AUDIT_REQUIRED_NO_RENEWED_ALLOWANCE")
    finally:
        report.update(wall_seconds=time.monotonic()-check.started,
            controller_cpu_seconds=time.process_time()-check.cpu_started,
            inclusive_child_job_cpu_charged=check.charged, child_cpu_complete=check.cpu_complete,
            accounting="CHILD_JOB_CPU_ONCE_NO_NESTED_DOUBLE_CHARGE_UNKNOWN_FULL_GRANT_THEN_STOP")
        if (not check.cpu_complete or report["wall_seconds"] >= args.wall_seconds or
                report["controller_cpu_seconds"]+check.charged >= args.cpu_seconds):
            report.update(status="FAILED", budget_error="PROJECT_CHECK_ORIGINAL_ALLOWANCE")
        if check.output_created:
            check.h.save(check.output/"PROJECT-CHECK-RESULT.json", report)
    print(json.dumps({"status": report["status"], "phase": report["phase"]}, sort_keys=True), flush=True)
    return 0 if report["status"] == "PASS_APPROVED_PROJECT_EXTRACTION_AND_CHECKED_COMPLETION" else 1


if __name__ == "__main__":
    raise SystemExit(main())

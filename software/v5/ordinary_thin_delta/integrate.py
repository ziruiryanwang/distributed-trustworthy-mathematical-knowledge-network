"""One retained-base thin-delta boundary, not a growth benchmark or release.

Source-only until root selects this exact file and actual A export. A cheap
inert closure check precedes every owner/native call. Saved frontier reports
are rejection hints only: new registration, intake and delta checking establish
their own authority. No owner init, source authoring, fixture rebuild or retry.
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
PREFIX = "software/v5/ordinary_thin_delta/"
NAME = "thin-delta-integration-01"
PACKAGE = LOCAL/"thin-delta-assembly-01/package"
STATE = LOCAL/"ordinary-reference-public-workflow-01/workflow"
BASE = LOCAL/"ordinary-baseline-native-workflow-02/workflow"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
HELPER = ROOT/"software/v5/ordinary_distribution/relocated_smoke.py"
HELPER_SHA = "aaba6e2e30906414f539842fd7678aaaf3ab7f9c077b30c6f115db7407584831"
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
FOUNDATION = "884f408f0e7d647a1b72714cfa78685804dea9e07289a67176692cfbfe2c8282"
BASE_ROOT = "72b399a0e3ad4a1673ec369115c255dd0f3016ae2956572c5def4ce1081f96b1"
STORE = "0096ade6422b06862c21d8f051a0c3d714ef65aec6f2607a2941443741c138c8"
ORIGIN = "97440ed1f77850e5b58a7256172246dc45efbded96ed160faef827e65b86874a"
SNAPSHOT = "71bc7058363c9972c71e7e560d70ccc467fc18cba4c8c93cdbb6c3bceae95f7b"
OLD_REFERENCE = "7a48dd24b43abdef20fe09bd505ef229f56cb9bdd1094f2bf24c6f2f01fd2914"
OLD_SUPPORT = "bcf0198ddd7a5aa44da3118d3cb3d7c43edb35450d4b9b65eaf04cf1e55a9efc"
MANIFEST = "b601bee8f6be2b2fc2315818ba81f340ed8bd72a43ac89cf547db001e7bc9cde"
PROJECT = "bb2753d5999774e4da0530503734633c48dcbc623ce29f5c3cc8a57f60fdfb45"
ARTIFACTS = "49003f08190856d675e6dd26f602cfdae1acfe8dac422e7cc2e9d6b720d80fff"
FRONTIER = STATE/"catalog/ordinary-realizations-v1/operations/bfe694e5015793c577bd5ae820a2f642b895fe1af92c512e9aaf0c63205ec120/events/reference-report.json"
FRONTIER_SHA = "2c225a66ae197521a75470219dcc51dd89f25615ecedb7b1fcfbf23cbc68f689"
SNAPSHOT_DIR = STATE/"catalog/ordinary-realizations-v1/operations"/ORIGIN/"snapshot"
A_NAMES = ("DMKNReferenceA.flip_apply", "DMKNReferenceA.flip_involution")
MIB = 1024**2
# One nonrenewing parent allowance. Successful unused child CPU is not counted
# as consumption; missing final accounting conservatively consumes the grant.
CAPS = (("01-register", "register-reference", 130, 90),
        ("02-intake", "intake-baseline", 120, 90),
        ("03-delta", "export-reference-delta", 160, 110),
        ("04-private-refusal", "export-reference-delta", 55, 30),
        ("05-recipient", "ordinary-lean-compile", 65, 45))
BODY = b"""open DMKNBaselineFixture
open scoped DMKNBaselineFixture

namespace DMKNThinRecipient

theorem flip_injective (x y : Flag) (h : flip x = flip y) : x = y :=
  (DMKNReferenceA.flip_involution x).symm.trans
    ((congrArg flip h).trans (DMKNReferenceA.flip_involution y))

theorem retained_notation : flip (flip lowF) = flip Flag.high :=
  DMKNReferenceA.flip_apply flip

end DMKNThinRecipient
"""


def need(ok, code):
    if not ok:
        raise ValueError(code)


def digest(value):
    need(type(value) is str and len(value) == 64 and
         all(c in "0123456789abcdef" for c in value), "THIN_HASH")
    return value


def helpers():
    with HELPER.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == HELPER_SHA, "THIN_HELPER_PIN")
    name = "_thin_integration_helpers"
    need(name not in sys.modules, "THIN_HELPER_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, HELPER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(HELPER), "exec"), module.__dict__)
    return module


def module_text(h, value):
    parts = []
    for tag, payload in value:
        need(tag == 0 and type(payload) is dict and set(payload) == {"$bytes"}, "THIN_MODULE_COMPONENT")
        text = bytes(payload["$bytes"]).decode("ascii")
        need(text and (text[0].isalpha() or text[0] == "_") and
             all(c.isalnum() or c == "_" for c in text), "THIN_MODULE_IDENTIFIER")
        parts.append(text)
    need(parts, "THIN_MODULE_EMPTY")
    return ".".join(parts)


def inspect_static(h, args, check):
    """Exact files plus cheap closure compatibility, never mathematical admission."""
    pins = {}
    bundle_directory = h.ordinary(args.bundle_directory, directory=True)
    need(bundle_directory.is_relative_to(LOCAL) and bundle_directory != LOCAL and
         bundle_directory.name == "bundle" and
         all(not bundle_directory.is_relative_to(path) and not path.is_relative_to(bundle_directory)
             for path in (STATE, BASE, PACKAGE, LOCAL/NAME)), "THIN_EXPLICIT_BUNDLE_LOCATION")

    def keep(path, expected=None, maximum=128*MIB):
        pin = h.pin(path, check, maximum)
        need(expected is None or pin == expected or pin["sha256"] == expected, "THIN_INPUT_PIN:"+str(path))
        need(pins.setdefault(str(path), pin) == pin, "THIN_PIN_CHANGED")
        return pin

    def document(path, expected, maximum=4*MIB):
        pin = keep(path, expected, maximum)
        raw = h.read(path, maximum)
        need(h.sha(raw) == pin["sha256"], "THIN_DOCUMENT_CHANGED")
        return h.diagnostic_json(raw)

    profile = document(PACKAGE/"PROFILE.json", args.profile_sha256)
    receipt = document(PACKAGE/"ASSEMBLY.json", args.assembly_sha256)
    manifest = document(PACKAGE/"installation/INSTALLATION.json", INSTALLATION)
    need(profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
         profile["installation_manifest_sha256"] == INSTALLATION and len(profile["files"]) == 137 and
         receipt["schema"] == "DMKN_ORDINARY_REFERENCE_SUCCESSOR_ASSEMBLY_V1" and
         receipt["status"] == "ASSEMBLED_NOT_ADOPTED" and receipt["profile_sha256"] == args.profile_sha256 and
         receipt["changed"] == ["reference/ReferenceModule.lean"] and receipt["added"] == [] and
         len(receipt["unchanged"]) == 164 and receipt["files_excluding_profile"] == 165 and
         receipt["base_profile_sha256"] == "a10e1f3ae0e1ac04cfa01240c9c07c3ca2d3da91616a3ca34b1f28b88adadbbc" and
         receipt["implementation_id"] == IMPLEMENTATION and
         manifest["implementation"]["semantic_id"] == SEMANTIC and
         h.identity("DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1", h.canonical(manifest["implementation"])) == IMPLEMENTATION,
         "THIN_PACKAGE_IDENTITY")
    for logical, expected in profile["files"].items():
        keep(PACKAGE/h.relative(logical), expected)
    runtimes = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    for logical, expected in manifest["files"].items():
        parts = h.relative(logical).parts
        path = (runtimes[parts[0]].joinpath(*parts[1:]) if parts[0] in runtimes else
                PACKAGE/"installation"/logical)
        keep(path, expected)
    document(BASE/"project-selection.json", PROJECT)
    document(BASE/"artifact-report.json", ARTIFACTS, 16*MIB)
    keep(STATE/"fixtures/custody-limits.json", "abf5b2dc515a06691194c47e7a320a7fdeaedbbaa18ec45e074807649968ecbe")
    reference_targets = document(STATE/"fixtures/reference-targets.json", None)
    for suffix in h.PARTS:
        keep(BASE/"original-library"/("DMKNBaselineFixture02"+suffix), maximum=64*MIB)
    keep(HELPER, HELPER_SHA, 2*MIB)

    def bundle(directory, selected_sha):
        doc = document(directory/"manifest.json", selected_sha, MIB)
        need(doc["schema"] == "DMKN_ORDINARY_BASELINE_BUNDLE_V1" and doc["semantic_id"] == SEMANTIC and
             type(doc["batches"]) is list and len(doc["batches"]) == 1 and
             0 < len(doc["batches"][0]) <= 32, "THIN_BUNDLE_SHAPE")
        units, bindings = {}, {}
        total = 0
        for row in doc["batches"][0]:
            identity = digest(row["unit_id"])
            path = directory/"units"/(identity+".json")
            keep(path, {"bytes": row["raw_bytes"], "sha256": row["raw_sha256"]}, 4*MIB)
            raw = h.read(path, 4*MIB)
            total += len(raw)
            need(total <= 4*MIB and identity not in units and
                 h.identity("DMKN-ORDINARY-EVIDENCE-V2", raw) == identity, "THIN_BUNDLE_ID_OR_BOUND")
            item = h.diagnostic_json(raw)
            need(item["schema"] == "DMKN_LEAN_ORDINARY_EVIDENCE_V2" and
                 item["semantic_id"] == SEMANTIC, "THIN_EVIDENCE_SCHEMA")
            units[identity] = item
            for entry in item["unit"][2]:
                key = h.canonical(entry[0])
                need(key not in bindings, "THIN_DUPLICATE_EXPORT")
                bindings[key] = {"name": entry[0], "unit_id": identity, "export_id":
                    h.identity("DMKN-ORDINARY-EXPORT-V2", h.canonical([SEMANTIC, identity, entry[0]]))}
        return units, bindings

    base_units, base_bindings = bundle(BASE/"bundle", MANIFEST)
    units, bindings = bundle(bundle_directory, args.bundle_manifest_sha256)
    old = document(FRONTIER, FRONTIER_SHA)
    need(old["context_root"] == BASE_ROOT and old["snapshot_id"] == SNAPSHOT and
         old["foundation_id"] == FOUNDATION and old["semantic_id"] == SEMANTIC, "THIN_FRONTIER_HINT_BINDING")
    anchors = {h.canonical(row["name"]): row["export_id"]
               for group in old["public_units"] for row in group["outputs"]}
    anchors.update({h.canonical(name): h.identity("DMKN-ORDINARY-BASIS-SYMBOL-V2",
        h.canonical([SEMANTIC, FOUNDATION, name])) for name in old["usable_basis_names"]})
    new_units = {identity: doc for identity, doc in units.items() if identity not in base_units}
    need(0 < len(new_units) <= 32, "THIN_NEW_CLOSURE_REQUIRED")
    new_bindings = {key: row for key, row in bindings.items() if row["unit_id"] in new_units}
    need(not set(new_bindings).intersection(base_bindings) and
         all(entry[1] == 2 for doc in new_units.values() for entry in doc["unit"][2]),
         "THIN_THEOREM_ONLY_NO_BASE_REDECLARATION")
    targets = [new_bindings[h.canonical(h.name(name))] for name in A_NAMES]
    edges = {}
    for identity, doc in new_units.items():
        dependencies = set()
        for name, export in doc["imports"]:
            key = h.canonical(name)
            if key in new_bindings:
                need(new_bindings[key]["export_id"] == export, "THIN_NEW_IMPORT_ID")
                dependencies.add(new_bindings[key]["unit_id"])
            else:
                need(anchors.get(key) == export, "THIN_PREFLIGHT_PRIVATE_OR_UNSUPPORTED_IMPORT")
        edges[identity] = dependencies
    visiting, reached = set(), set()

    def visit(identity):
        check()
        need(identity not in visiting, "THIN_CYCLIC_CLOSURE")
        if identity in reached:
            return
        visiting.add(identity)
        for dependency in edges[identity]:
            visit(dependency)
        visiting.remove(identity); reached.add(identity)

    for row in targets:
        visit(row["unit_id"])
    need(reached == set(new_units), "THIN_EXTRANEOUS_NEW_MATHEMATICS")
    expected_refs = [{k: base_bindings[h.canonical(h.name(name))][k] for k in ("name", "export_id")}
                     for name in ("DMKNBaselineFixture.flip", "DMKNBaselineFixture.flip_low")]
    need(reference_targets == expected_refs, "THIN_REFERENCE_TARGETS")
    private = next(row for row in base_bindings.values() if row["export_id"] ==
                   "db7607937b63a1ac281f24d0220b28650aa1d13a475f618a344bf6d4f380fff8")
    need(private["unit_id"] == "eff2c275d01946403792e9b4f663f28d3d4368c165c1f621f6d9bb45c966d93e" and
         h.canonical(private["name"]) not in anchors, "THIN_GENUINE_PRIVATE_TARGET")
    need(len(pins) <= 256, "THIN_INPUT_PIN_COUNT")
    return {"pins": pins, "manifest": manifest, "targets": targets, "private": private,
            "bundle_directory": bundle_directory,
            "new_units": set(new_units), "base_units": set(base_units),
            "bundle_units": set(units), "preflight": "HINT_ONLY_NOT_CURRENT_WARRANTS_OR_ACCEPTANCE"}


class Workflow:
    def __init__(self, args, h):
        self.args, self.h = args, h
        self.deadline = START_WALL+args.wall_seconds
        self.charged, self.complete, self.calls, self.held = 0.0, True, [], {}
        self.output_created = False

    def check(self):
        need(time.monotonic() < self.deadline and
             time.process_time()-START_CPU+self.charged < self.args.cpu_seconds, "THIN_ORIGINAL_ALLOWANCE")

    def hold(self, path, expected=None, maximum=128*MIB):
        pin = self.h.pin(path, self.check, maximum)
        need(expected is None or pin == expected or pin["sha256"] == expected, "THIN_IMMUTABLE_PIN:"+str(path))
        need(self.held.setdefault(str(path), pin) == pin, "THIN_IMMUTABLE_CHANGED")
        return pin

    def document(self, path, maximum=4*MIB):
        self.check()
        return self.h.diagnostic_json(self.h.read(path, maximum))

    def save(self, path, value):
        return self.hold(path, self.h.save(path, value))

    def prepare(self):
        h = self.h
        self.output = h.ordinary(self.args.output, directory=True, fresh=True)
        need(self.output == LOCAL/NAME/"workflow" and Path(sys.executable).resolve() == PYTHON/"python.exe",
             "THIN_LOCATION")
        self.static = inspect_static(h, self.args, self.check)
        self.held.update(self.static["pins"])
        manifest = self.static["manifest"]
        for role, name in (("supervisor", "_thin_supervisor"), ("domains", "domains"), ("job", "_thin_job")):
            logical = manifest["roles"][role]
            need(logical.startswith("supervisor/"), "THIN_SUPERVISOR_ROLE")
            module = h.load_exact(PACKAGE/"installation"/logical, name, manifest["files"][logical], self.check)
            if role == "supervisor":
                self.supervisor = module
            elif role == "job":
                self.jobs = module
        self.output.mkdir(); self.output_created = True
        (self.output/"calls").mkdir()
        self.save(self.output/"INPUTS.json", self.held.copy())
        self.save(self.output/"PLAN.json", {"call_caps": CAPS, "original_allowance": vars(self.args),
            "scope": "FRESH_REGISTRATION_CHECKED_THIN_DELTA_ORDINARY_USE_NO_GROWTH_SPEEDUP_CLAIM",
            "preflight": self.static["preflight"], "targets": self.static["targets"],
            "new_unit_ids": sorted(self.static["new_units"]), "owner_initialization": False})

    def invoke(self, operation, extra=(), *, refused=False, worker=None):
        self.check()
        index = len(self.calls)
        need(index < len(CAPS), "THIN_CALL_COUNT")
        label, selected, wall, cpu = CAPS[index]
        need(operation == selected and refused == (index == 3) and (worker is not None) == (index == 4),
             "THIN_CALL_ORDER")
        grant = self.supervisor.limits_checked({
            "wall_seconds": min(wall, math.floor(self.deadline-time.monotonic())-15),
            "cpu_seconds": min(cpu, math.floor(self.args.cpu_seconds-self.charged-(time.process_time()-START_CPU))-3),
            "memory_mib": self.args.memory_mib, "active_processes": 6,
            "stdout_bytes": 4*MIB, "stderr_bytes": MIB})
        need(grant["wall_seconds"] >= 45 and grant["cpu_seconds"] >= (80 if index == 1 else 8),
             "THIN_REMAINING_GRANT")
        argv = worker or [str(PYTHON/"python.exe"), "-I", "-S", "-B", str(PACKAGE/"owner.py"), operation,
            "--profile-sha256", self.args.profile_sha256, "--python-runtime", str(PYTHON),
            "--lean-runtime", str(LEAN), "--catalog", str(STATE/"catalog"), "--custody", str(STATE/"custody"),
            "--store-id", STORE, "--custody-limits", str(STATE/"fixtures/custody-limits.json"),
            "--wall-seconds", str(grant["wall_seconds"]-5), "--cpu-seconds", str(grant["cpu_seconds"]-2),
            "--memory-mib", str(self.args.memory_mib), *map(str, extra)]
        event = {"label": label, "operation": operation, "argv": argv, "limits": grant,
                 "charged_cpu_seconds": grant["cpu_seconds"], "cpu_complete": False, "public_result": None}
        self.calls.append(event); self.charged += grant["cpu_seconds"]
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
                if raw and worker is None:
                    event["public_result"] = self.h.diagnostic_json(raw)
            except BaseException as error:
                event["reply_parse_error"] = str(error)[:2048]
            self.h.save(self.output/"calls"/(label+"-EVENT.json"), event)
        need(known, "THIN_UNKNOWN_CPU_FULL_GRANT_CHARGED")
        self.h.clean(supervision, exit_code=1 if refused else 0)
        need(self.h.read(self.output/"calls"/label/"stderr.txt", MIB) == b"", "THIN_STDERR")
        if worker is not None:
            need(self.h.read(self.output/"calls"/label/"stdout.txt", MIB) == b"", "THIN_COMPILER_STDOUT")
            self.check(); return None
        result = event["public_result"]
        if refused:
            need(type(result) is dict and result.get("ok") is False and result.get("operation") == operation and
                 result.get("phase") == "EXPORT_REFERENCE_DELTA" and result.get("error_type") == "ModuleError" and
                 result.get("accepted") is None and not result.get("close_errors"), "THIN_REFUSAL_REPLY")
            self.check(); return result
        need(type(result) is dict and result.get("ok") is True and not result.get("close_errors") and
             result["operation"] == operation and result["implementation_id"] == IMPLEMENTATION and
             result["profile_sha256"] == self.args.profile_sha256 and result["store_id"] == STORE and
             result["catalog"] == str(STATE/"catalog") and result["custody"] == str(STATE/"custody"),
             "THIN_PUBLIC_REPLY")
        self.check(); return result["result"]

    def recipient(self, delta):
        h = self.h
        replay_path = SNAPSHOT_DIR/"replay-request.json"
        need(delta["original_replay_request"] == str(replay_path), "THIN_ORIGINAL_REPLAY_PATH")
        prepared_path = SNAPSHOT_DIR/"prepared-manifest.json"
        self.hold(prepared_path, SNAPSHOT, 4*MIB)
        prepared = self.document(prepared_path)
        self.hold(replay_path, prepared["replay_request_sha256"], 4*MIB)
        replay = self.document(replay_path)
        need(replay["schema"] == "DMKN_ORDINARY_BASELINE_ARTIFACT_REQUEST_V1" and replay["mode"] == "replay" and
             replay["modules"] == [h.name("DMKNBaselineFixture02")] and
             len(replay["artifacts"]) == len(prepared["modules"]) <= 4096, "THIN_REPLAY_SELECTION")
        artifacts = {}
        for row, saved in zip(replay["artifacts"], prepared["modules"]):
            need(row["module"] == saved["module"] and row["parts"] == saved["parts"], "THIN_REPLAY_MAP")
            name = module_text(h, row["module"])
            need(name not in artifacts and [len(parts) for parts in row["parts"]] == [3, 2], "THIN_ARTIFACT_MAP")
            for paths, pins in zip(row["parts"], saved["pins"]):
                need(len(paths) == len(pins), "THIN_ARTIFACT_PIN_COUNT")
                for path, pin in zip(paths, pins):
                    need(Path(path).is_relative_to(SNAPSHOT_DIR/"modules"), "THIN_SNAPSHOT_PATH")
                    self.hold(Path(path), pin, 64*MIB)
            artifacts[name] = row["parts"]
        original = artifacts["DMKNBaselineFixture02"]
        for path, suffix in zip(original[0]+original[1], h.PARTS):
            need(self.held[path] == self.held[str(BASE/"original-library"/("DMKNBaselineFixture02"+suffix))],
                 "THIN_ORIGINAL_P_NOT_REPLACEMENT")
        name = delta["module_name"]
        need(type(name) is str and name.startswith("DMKNBridge_") and digest(name[11:]) and name not in artifacts,
             "THIN_DELTA_MODULE_NAME")
        directory = Path(delta["module_directory"])
        need(directory.is_relative_to(STATE/"catalog/ordinary-realizations-v1/operations"), "THIN_DELTA_LOCATION")
        paths = [directory/(name+suffix) for suffix in h.PARTS]
        need(set(delta["artifact_parts"]) == {path.name for path in paths}, "THIN_DELTA_PART_CENSUS")
        for path in paths:
            self.hold(path, delta["artifact_parts"][path.name], 64*MIB)
        artifacts[name] = [[str(path) for path in paths[:3]], [str(path) for path in paths[3:]]]
        consumer = self.output/"recipient"; consumer.mkdir()
        module = "DMKNAuthor_"+h.sha(BODY+name.encode("ascii"))
        imports = ["DMKNBaselineFixture02", name]
        source = consumer/(module+".lean")
        source_raw = ("module\nprelude\n"+"".join("public import "+part+"\n" for part in imports)+
                      "\npublic section\n\n").encode("ascii")+BODY
        self.save(source, source_raw)
        setup = consumer/"setup.json"
        self.save(setup, {"name": module, "package": None, "isModule": True,
            "imports": [{"module": part, "importAll": False, "isExported": True, "isMeta": False} for part in imports],
            "importArts": artifacts, "dynlibs": [], "plugins": [], "options": {"Elab.async": False}})
        report_path = consumer/"compile-report.json"
        self.invoke("ordinary-lean-compile", worker=[str(PYTHON/"python.exe"), "-I", "-S", "-B",
            str(PACKAGE/"reference/reference_author_worker.py"), str(LEAN/"bin/lean.exe"),
            str(consumer), str(source), str(setup), str(consumer/(module+".olean")), str(report_path)])
        report = self.document(report_path)
        need(report["schema"] == "DMKN_ORDINARY_REFERENCE_AUTHOR_OUTPUT_V1" and report["module_name"] == module and
             report["source"]["sha256"] == h.sha(source_raw) and len(report["artifact_parts"]) == 5,
             "THIN_RECIPIENT_COMPILED")
        self.hold(report_path)
        for row, suffix in zip(report["artifact_parts"], h.PARTS):
            path = consumer/(module+suffix)
            need(row["path"] == str(path), "THIN_RECIPIENT_OUTPUT_PATH")
            self.hold(path, {key: row[key] for key in ("bytes", "sha256")}, 64*MIB)
        return {"source": str(source), "source_sha256": h.sha(source_raw), "imports": imports,
                "compile_report": report, "claim": "ORDINARY_P_PLUS_DELTA_USE_NOT_NEW_COMMONS_ADMISSION"}

    def run(self, report):
        report["phase"] = "FRESH_REFERENCE"
        reference = self.invoke("register-reference", ("--parent-root", BASE_ROOT,
            "--bundle-directory", BASE/"bundle", "--bundle-manifest", BASE/"bundle/manifest.json",
            "--bundle-manifest-sha256", MANIFEST, "--reference-targets", STATE/"fixtures/reference-targets.json",
            "--reference-project", BASE/"project-selection.json", "--reference-project-sha256", PROJECT,
            "--reference-artifact-report", BASE/"artifact-report.json", "--reference-artifact-report-sha256", ARTIFACTS,
            "--retained-snapshot-operation", ORIGIN, "--retained-snapshot-sha256", SNAPSHOT))
        report["reference"] = reference
        need(reference["status"] == "REGISTERED_LOCAL_ORIGINAL_REFERENCE" and
             reference["source_context_root"] == BASE_ROOT and reference["snapshot_id"] == SNAPSHOT and
             reference["reference_id"] != OLD_REFERENCE and reference["support_id"] != OLD_SUPPORT and
             reference["retained_snapshot_operation"] == ORIGIN and reference["native_calls"] == 1 and
             reference["new_catalog_acceptance"] is False, "THIN_GENUINELY_NEW_SUPPORT_REGISTRATION")
        reference_id = digest(reference["reference_id"])
        report["phase"] = "ACTUAL_A_INTAKE"
        bundle_directory = self.static["bundle_directory"]
        intake = self.invoke("intake-baseline", ("--parent-root", BASE_ROOT, "--bundle-directory", bundle_directory,
            "--bundle-manifest", bundle_directory/"manifest.json", "--bundle-manifest-sha256", self.args.bundle_manifest_sha256))
        report["intake"] = intake
        need(intake["status"] == "BASELINE_INTAKE_COMPLETE" and intake["selected_root"] == BASE_ROOT and
             intake["manifest_sha256"] == self.args.bundle_manifest_sha256 and intake["local_root"] != BASE_ROOT and
             len(intake["batches"]) == 1 and intake["batches"][0]["status"] == "CHECKED" and
             intake["batches"][0]["units_checked"] == len(self.static["new_units"]) and
             intake["batches"][0]["local_root"] == intake["local_root"], "THIN_NEW_A_CHECKED")
        root = digest(intake["local_root"])
        target_path = self.output/"delta-targets.json"; self.save(target_path, self.static["targets"])
        report["phase"] = "DELTA"
        delta = self.invoke("export-reference-delta", ("--parent-root", root, "--reference-id", reference_id,
            "--reference-targets", target_path))
        report["delta"] = delta
        need(delta["status"] == "CHECKED_AND_REGISTERED_LOCAL_REFERENCE_DELTA" and
             delta["reference_id"] == reference_id and delta["support_id"] == reference["support_id"] and
             delta["parent_delta_id"] == "" and delta["source_context_root"] == root and
             delta["snapshot_id"] == SNAPSHOT and delta["native_calls"] == 3 and
             delta["new_catalog_acceptance"] is False and
             delta["targets"] == sorted(self.static["targets"], key=lambda row: self.h.canonical(row["name"])) and
             set(delta["ordered_unit_ids"]) == self.static["new_units"] and
             not set(delta["ordered_unit_ids"]).intersection(self.static["base_units"]), "THIN_NEW_ONLY_DELTA")
        report["phase"] = "PRIVATE_FRONTIER_REFUSAL"
        bad_path = self.output/"private-target.json"; self.save(bad_path, [self.static["private"]])
        refusal = self.invoke("export-reference-delta", ("--parent-root", root, "--reference-id", reference_id,
            "--reference-targets", bad_path), refused=True)
        report["refusal"] = refusal
        detail = refusal["detail"]
        need(detail["phase"] == "RESERVE_AND_COLLECT_DELTA" and detail["error_type"] == "ClosureError" and
             detail["error"] == "REFERENCE_CLOSURE_PRIVATE_OR_UNUSABLE_IMPORT" and
             detail["native_cpu_seconds"] == 0.0 and detail["conservative_cpu_reservation_charged"] == 0 and
             detail["new_catalog_acceptance"] is False and not detail.get("closure_error") and
             not detail.get("committed_delta_id"), "THIN_PRE_NATIVE_PRIVATE_REFUSAL")
        report["phase"] = "ORDINARY_RECIPIENT"
        report["recipient"] = self.recipient(delta)
        need(len(self.calls) == 5, "THIN_EXACT_OPERATIONS")
        report.update(status="PASS_SAME_BASE_THIN_DELTA_INTEGRATION_NOT_FINAL_V5", phase="COMPLETE",
            final_root=root, original_fixture_recompiled=False, producer_author_module_imported=False,
            old_reference_reused_as_authority=False, snapshot_recopied=False,
            growth_claim="CAPABILITY_BOUNDARY_ONLY_NOT_MEASURED_USEFUL_GROWTH_OR_LARGE_SCALE_DEPLOYMENT")

    def finish(self, report):
        report.update(calls=self.calls, wall_seconds=time.monotonic()-START_WALL,
            controller_cpu_seconds=time.process_time()-START_CPU, charged_whole_child_job_cpu_seconds=self.charged,
            cpu_accounting_complete=self.complete,
            retention="ALL_INPUTS_ACCEPTED_STATE_AND_PARTIAL_OUTPUTS_PRESERVED_NO_AUTOMATIC_RETRY")
        if self.output_created:
            self.h.save(self.output/"WORKFLOW.json", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("profile-sha256", "assembly-sha256", "bundle-directory", "bundle-manifest-sha256", "output"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+name, type=int, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and args.wall_seconds == 500 and
         args.cpu_seconds == 350 and args.memory_mib == 1536, "THIN_CONTEXT_AND_FIXED_ALLOWANCE")
    for value in (args.profile_sha256, args.assembly_sha256, args.bundle_manifest_sha256):
        digest(value)
    h = helpers(); workflow = Workflow(args, h)
    report = {"schema": "DMKN_THIN_DELTA_INTEGRATION_V1", "status": "FAILED", "phase": "PREPARE"}
    try:
        workflow.prepare(); workflow.run(report)
        for path, pin in workflow.held.items():
            need(h.pin(Path(path), workflow.check, 128*MIB) == pin, "THIN_FINAL_IMMUTABLE_PIN")
    except BaseException as error:
        report.update(status="FAILED", error_type=type(error).__name__, error=str(error)[:4096])
    workflow.finish(report)
    print(json.dumps({key: value for key, value in report.items() if key != "calls"}, sort_keys=True, allow_nan=False), flush=True)
    return 0 if report["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())

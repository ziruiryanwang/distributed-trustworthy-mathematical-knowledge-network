"""One root-selected original-library discriminator, never an owner operation.

Run only in the selected Run-V5-Check enclosing Job. The compile, collection,
export, exact-map correspondence and one changed-body refusal share its original
allowance. Test-only context/support labels are not current protected warrants.
All partial output is retained; no retry, package adoption or registration.
"""
from pathlib import Path
import argparse
from contextlib import ExitStack
import copy
import hashlib
import importlib.util
import json
import os
import re
import socket
import sqlite3
import subprocess
import sys
import time
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_baseline/"
PACKAGE = LOCAL/"ordinary-preview-assembly-01/package"
PROFILE = "ab04e72440bcd09381a81d4b721d1103fa2e62bc260fa6c0434e6c568419016f"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
BUILDER = "software/v5/ordinary_package/build.py"
BUILDER_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
NAME = "ordinary-baseline-native-workflow-01"
MIB = 1024**2
SPOOL = 1024*MIB
PARTS = (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir")
FIXED_SOURCES = {
    "baseline_bundle.py": "d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce",
    "baseline_snapshot.py": "ab2a0adcdd0b632d14fe2ec7058f9ef496b788760eff4ddd4852d01d11dd3468",
    "reference_request.py": "a4cadb4beb75bdf86b7314a2c05e301cbbafd42da8500ccd524c82c7a7503923",
    "DMKNBaselineFixture.lean": "bb58ee2a0246e4d33c5c3ebf16df9ee4986be75756d3a3ba597b7f9ad60928d6",
}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def read(path, maximum=2*MIB):
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(0 < len(raw) <= maximum, "NATIVE_WORKFLOW_READ_BOUND:"+str(path))
    return raw


def module(name, path, expected=None):
    raw = read(path)
    need(expected is None or sha(raw) == expected, "NATIVE_WORKFLOW_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    exec(compile(raw, str(path), "exec"), value.__dict__)
    return value


def helper():
    return module("_native_workflow_builder", ROOT/BUILDER, BUILDER_SHA)


def inspect_build(B, number, authorized, check):
    """Require exact root-authorized successful provenance, never path discovery."""
    need(type(number) is str and re.fullmatch(r"[0-9]{2}", number) and number != "00",
         "NATIVE_WORKFLOW_BUILD_NUMBER")
    directory = LOCAL/("ordinary-baseline-native-build-"+number)
    pins = {}

    def keep(path, expected=None, maximum=32*MIB):
        pin = B.pin(B.ordinary(path), check, maximum)
        need(expected is None or pin == expected or pin["sha256"] == expected,
             "NATIVE_WORKFLOW_BUILD_PIN:"+str(path))
        pins[str(path)] = pin
        return pin

    def document(relative, digest):
        path = directory/relative
        expected = keep(path, digest, 2*MIB)
        raw = read(path)
        need({"bytes": len(raw), "sha256": sha(raw)} == expected,
             "NATIVE_WORKFLOW_BUILD_DOCUMENT_CHANGED")
        return json.loads(raw)

    build = document("build/BUILD.json", authorized["build"])
    result = document("RESULT.json", authorized["result"])
    selection = document("selection.json", authorized["selection"])
    event = result["result"]
    need(result["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1" and
         result["selection_sha256"] == authorized["selection"] and
         event["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and event["child_exit_code"] == 0 and
         event["direct_child_reaped"] is True and event["job_closed"] is True and
         event["cleanup_errors"] == [] and event["termination_requested"] is False and
         event["final_job"]["active_processes"] == 0 and
         event["final_job"]["terminated_processes"] == 0, "NATIVE_WORKFLOW_BUILD_NOT_CLOSED_SUCCESS")
    need(build["schema"] == "DMKN_ORDINARY_BASELINE_NATIVE_BUILD_V1" and
         build["status"] == "BUILT_CANDIDATES_NOT_INSTALLED_OR_ADOPTED" and
         build["mathematical_acceptance"] is False and
         selection["schema"] == "DMKN_V5_LOCAL_CHECK_V1" and
         selection["name"] == directory.name and
         len(build["completed_commands"]) == 9 and
         all(row["exit_code"] == 0 for row in build["completed_commands"]),
         "NATIVE_WORKFLOW_BUILD_SCOPE")
    need(set(build["metadata"]) == {"INPUTS.json", "NATIVE-OUTPUTS.json"},
         "NATIVE_WORKFLOW_BUILD_METADATA_CENSUS")
    for relative, pin in build["metadata"].items():
        need(relative in ("INPUTS.json", "NATIVE-OUTPUTS.json"), "NATIVE_WORKFLOW_BUILD_METADATA")
        keep(directory/"build"/relative, pin, 2*MIB)
    outputs = json.loads(read(directory/"build/NATIVE-OUTPUTS.json"))
    need(outputs == build["all_candidate_outputs"] and len(outputs) == 15,
         "NATIVE_WORKFLOW_BUILD_OUTPUT_CENSUS")
    for filename, pin in outputs.items():
        need(re.fullmatch(r"[A-Za-z0-9]+\.(?:olean|c|o|exe)", filename),
             "NATIVE_WORKFLOW_BUILD_FILENAME")
        keep(directory/"build/objects"/filename, pin)
    native = {"exporter": "BaselineExporter", "collector": "BaselineArtifacts"+number,
              "reference": "OrdinaryReferenceBase"+number}
    for name in (*native.values(), "BaselineArtifactCore"+number):
        relative = PREFIX+name+".lean"
        pin = build["source_files"][relative]
        need(selection["sources"][relative] == pin["sha256"], "NATIVE_WORKFLOW_BUILD_SOURCE_SELECTION")
        keep(ROOT/relative, pin, 2*MIB)
        keep(directory/"sources"/relative, pin, 2*MIB)
    executables = {role: directory/"build/objects"/(name+".exe") for role, name in native.items()}
    need(set(build["executable_links"]) == {path.name for path in executables.values()},
         "NATIVE_WORKFLOW_BUILD_EXECUTABLE_ROLES")
    return pins, executables


def name(*parts):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in parts]


def main(args):
    started, cpu = time.monotonic(), time.process_time()
    deadline = started+270

    def check():
        need(time.monotonic() < deadline and time.process_time()-cpu < 100,
             "NATIVE_WORKFLOW_ORIGINAL_ALLOWANCE")

    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON/"python.exe", "NATIVE_WORKFLOW_PROCESS")
    B = helper()
    output = B.ordinary(Path(args.output), directory=True, fresh=True)
    source_root = B.ordinary(Path(args.source_root), directory=True)
    need(output == LOCAL/NAME/"workflow" and
         Path(__file__).resolve() == source_root/PREFIX/"native_workflow.py", "NATIVE_WORKFLOW_LOCATIONS")
    authorized = {"build": args.build_sha256, "result": args.build_result_sha256,
                  "selection": args.build_selection_sha256}
    build_pins, native = inspect_build(B, args.build_number, authorized, check)
    source = source_root/PREFIX
    for relative, digest in FIXED_SOURCES.items():
        need(B.pin(source/relative, check, 2*MIB)["sha256"] == digest,
             "NATIVE_WORKFLOW_FIXED_SOURCE")
    profile_raw = read(PACKAGE/"PROFILE.json")
    need(sha(profile_raw) == PROFILE, "NATIVE_WORKFLOW_PROFILE")
    descriptor = json.loads(profile_raw)
    base = module("_native_workflow_owner", PACKAGE/"owner.py",
                  descriptor["files"]["owner.py"]["sha256"])
    loader = base.bootstrap(PACKAGE, PROFILE, check)
    loaded = loader.load(PACKAGE, PROFILE, {"python_runtime": PYTHON, "lean_runtime": LEAN},
                         deadline, check_parent=check)
    A, O = loaded.A, loaded.O
    bundle_api = module("baseline_bundle", source/"baseline_bundle.py")
    S = module("baseline_snapshot", source/"baseline_snapshot.py")
    Q = module("reference_request", source/"reference_request.py")
    R = module("reference_report", source/"reference_report.py", args.report_sha256)
    need(bundle_api.E is A.E and bundle_api.S is A.S and S.A is A and Q.A is A and R.A is A and
         type(loaded.installation) is A.NativeInstallation, "NATIVE_WORKFLOW_REAL_SHARED_CODECS")
    output.mkdir()
    fixture, bundle_dir = output/"original-library", output/"bundle"
    fixture.mkdir(); bundle_dir.mkdir(); (bundle_dir/"units").mkdir()
    completed, cases, forbidden_calls, saved = [], [], [], {}
    phase = "INPUTS"

    def save(path, raw, maximum=32*MIB):
        check()
        need(type(raw) is bytes and 0 < len(raw) <= maximum, "NATIVE_WORKFLOW_SAVE_BOUND")
        B.fresh_bytes(path, raw)
        pin = {"bytes": len(raw), "sha256": sha(raw)}
        need(B.pin(path, check, maximum) == pin, "NATIVE_WORKFLOW_SAVE_READBACK")
        saved[str(path)] = pin
        return pin

    def census():
        check()
        total, count = 0, 0
        for directory, dirs, files in os.walk(output, followlinks=False):
            check()
            for child in dirs:
                B.ordinary(Path(directory)/child, directory=True)
            for child in files:
                path = B.ordinary(Path(directory)/child)
                total += path.stat().st_size
                count += 1
                need(total <= SPOOL and count <= 30000, "NATIVE_WORKFLOW_SPOOL_BOUND")
        return {"bytes": total, "files": count}

    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON", "RUST", "CARGO", "RISC0", "NODE"))
           and key.upper() not in ("PATH", "VIRTUAL_ENV")}
    env["PATH"] = str(LEAN/"bin")

    def run(label, argv, expected_failure=None):
        nonlocal phase
        check(); phase = label
        need(len(completed) < 5 and sum(len(value)+3 for value in argv) <= 30000,
             "NATIVE_WORKFLOW_COMMAND_BOUND")
        before = time.monotonic()
        # No PIPE buffering or child-specific renewed allowance. Output inherits
        # the enclosing runner's bounded logs and all descendants its finite Job.
        if expected_failure:
            # This selected native program emits a fixed bounded phase/error
            # protocol. Retain and read its one negative diagnostic (cooperative
            # file bound), then also expose it to the enclosing bounded log.
            diagnostic_path = output/"native-negative-stderr.txt"
            with diagnostic_path.open("xb") as diagnostic:
                result = subprocess.run(argv, cwd=output, env=env, stdin=subprocess.DEVNULL,
                    stderr=diagnostic, creationflags=subprocess.CREATE_NO_WINDOW,
                    timeout=max(0.001, deadline-before))
            diagnostic_raw = read(diagnostic_path, MIB)
            saved[str(diagnostic_path)] = {"bytes": len(diagnostic_raw), "sha256": sha(diagnostic_raw)}
            sys.stderr.write(diagnostic_raw.decode("utf-8", errors="strict"))
            sys.stderr.flush()
        else:
            result = subprocess.run(argv, cwd=output, env=env, stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW, timeout=max(0.001, deadline-before))
        row = {"phase": label, "argv": argv, "exit_code": result.returncode,
               "wall_seconds": time.monotonic()-before,
               "expected_failure": expected_failure}
        completed.append(row)
        print(json.dumps(row, sort_keys=True), flush=True)
        need(result.returncode == (1 if expected_failure else 0), "NATIVE_WORKFLOW_COMMAND_RESULT:"+label)
        if expected_failure:
            need(expected_failure.encode("ascii") in diagnostic_raw,
                 "NATIVE_WORKFLOW_WRONG_NATIVE_REFUSAL")
        census()

    def forbidden(*_, **__):
        forbidden_calls.append("FORBIDDEN_OWNER_OR_NETWORK")
        raise AssertionError("NATIVE_WORKFLOW_FORBIDDEN_OWNER_OR_NETWORK")

    try:
        with ExitStack() as stack:
            for obj, attribute in ((sqlite3, "connect"), (socket, "socket"),
                    (A.OrdinaryAdmission, "open"), (A.OrdinaryAdmission, "_execute"),
                    (A.P.PortableCatalog, "open"), (A.P.PortableCatalog, "_commit_checked"),
                    (O.OrdinaryStore, "__init__"), (O.OrdinaryStore, "put_evidence")):
                stack.enter_context(patch.object(obj, attribute, forbidden))
            inventory_raw = loaded.installation.read("inventory", MIB)
            inventory_path = output/"inventory.json"
            save(inventory_path, inventory_raw, MIB)
            save(output/"INPUTS.json", encoded({"schema": "DMKN_NATIVE_WORKFLOW_INPUTS_V1",
                "build_number": args.build_number, "authorized_build_pins": authorized,
                "files": build_pins, "profile_sha256": PROFILE, "fixed_sources": FIXED_SOURCES,
                "reference_report_sha256": args.report_sha256,
                "context": "TEST_ONLY_NOT_CURRENT_WARRANTS",
                "mathematical_acceptance": False, "spool_maximum_bytes": SPOOL}))
            run("fixture-compile", [str(LEAN/"bin/lean.exe"), "-DElab.async=false", "-R", str(source),
                "-o", str(fixture/"DMKNBaselineFixture.olean"), str(source/"DMKNBaselineFixture.lean")])
            need({path.name for path in fixture.iterdir()} == {"DMKNBaselineFixture"+part for part in PARTS},
                 "NATIVE_WORKFLOW_EXACT_FIXTURE_PARTS")
            for part in PARTS:
                path = fixture/("DMKNBaselineFixture"+part)
                saved[str(path)] = B.pin(path, check, 16*MIB)
            modules = [name("DMKNBaselineFixture")]
            targets = [name("DMKNBaselineFixture", "flip"), name("DMKNBaselineFixture", "flip_low")]
            project = A.E.canonical_json({"schema": "DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1",
                "project_search_paths": [str(fixture)], "modules": modules})
            collect = encoded({"schema": S.REQUEST_SCHEMA, "mode": "collect", "modules": modules,
                               "project_search_paths": [str(fixture)]})
            export = encoded({"schema": "DMKN_ORDINARY_BASELINE_EXPORT_REQUEST_V1",
                "project_search_paths": [str(fixture)], "modules": modules, "targets": targets})
            save(output/"project-selection.json", project)
            save(output/"collect-request.json", collect)
            save(output/"export-request.json", export)
            run("collect-original-library", [str(native["collector"]), str(LEAN),
                str(output/"collect-request.json"), str(output/"artifact-report.json")])
            artifact_raw = read(output/"artifact-report.json", S.MAX_REPORT)
            saved[str(output/"artifact-report.json")] = {"bytes": len(artifact_raw), "sha256": sha(artifact_raw)}
            run("export-selected-targets", [str(native["exporter"]), str(LEAN), str(inventory_path),
                str(output/"export-request.json"), str(output/"writer-bundle.json")])
            writer = read(output/"writer-bundle.json", 32*MIB)
            saved[str(output/"writer-bundle.json")] = {"bytes": len(writer), "sha256": sha(writer)}
            phase = "BIND_AND_SNAPSHOT"
            bundle = bundle_api.bind_writer(writer, inventory_raw, targets, check_budget=check)
            save(bundle_dir/"manifest.json", bundle.manifest.raw)
            raw_units = [raw for batch in bundle.batches for raw in batch]
            need(sum(map(len, raw_units)) <= 64*MIB, "NATIVE_WORKFLOW_PORTABLE_BOUND")
            for raw in raw_units:
                item = A.PE.read_evidence(raw)
                save(bundle_dir/"units"/(item.unit_id+".json"), raw, 8*MIB)
            snapshot = S.prepare_snapshot(loaded.installation,
                project_selection_raw=project, project_selection_sha256=sha(project),
                report_raw=artifact_raw, report_sha256=sha(artifact_raw),
                output_directory=output/"snapshot", spool_bytes=S.MAX_ARTIFACTS+S.METADATA_RESERVATION,
                check_budget=check)
            # Explicit fixture request: no fake owner and no prepare_request call.
            units, ids, pins, bindings = [], [], [], []
            for raw in raw_units:
                check()
                item = A.PE.read_evidence(raw)
                outputs = []
                for row in item.document["unit"][2]:
                    symbol = A.S.export_id(A.S.semantic_id(), item.unit_id, row[0])
                    outputs.append({"name": row[0], "export_id": symbol})
                    bindings.append((A.E.name_key(row[0]), symbol, item.unit_id))
                units.append({"unit_id": item.unit_id, "unit": item.document["unit"], "outputs": outputs})
                ids.append(item.unit_id); pins.append((item.unit_id, len(raw), sha(raw)))
            selected = {"schema": Q.SCHEMA, "semantic_id": A.S.semantic_id(),
                "foundation_id": A.S.foundation_id(),
                "context_root": sha(b"DMKN_TEST_ONLY_NOT_ACCEPTED_CONTEXT_V1"+bundle.manifest.raw),
                "snapshot_id": snapshot.manifest_sha256,
                "support_id": sha(b"DMKN_TEST_ONLY_NOT_ACCEPTED_SUPPORT_V1"+encoded(authorized)),
                "units": units,
                "targets": [{"name": A.E.strict_json(target.name), "export_id": target.export_id}
                            for target in bundle.targets]}
            request_raw = A.E.canonical_json(selected)
            save(output/"test-only-reference-request.json", request_raw)
            request = Q.ReferenceRequest(request_raw, sha(request_raw), inventory_raw, tuple(ids),
                tuple(pins), tuple(sorted(bindings)), bundle.census.nodes, bundle.census.edges)
            report_path = output/"reference-report.json"
            run("exact-map-correspondence", [str(native["reference"]), str(inventory_path),
                str(snapshot.directory/"replay-request.json"),
                str(output/"test-only-reference-request.json"), str(report_path)])
            report_raw = read(report_path, 16*MIB)
            saved[str(report_path)] = {"bytes": len(report_raw), "sha256": sha(report_raw)}
            bound = R.bind_report(report_raw, sha(report_raw), request=request,
                replay_request_raw=snapshot.replay_request_raw, check_budget=check)
            report = A._writer_json(report_raw, 16*MIB)
            public_lookup = {key: (symbol, identity, projection, kernel_projection)
                             for key, symbol, identity, projection, kernel_projection in bound.public_bindings}
            need(public_lookup[A.E.name_key(targets[0])][2:] == ("full", "full"),
                 "NATIVE_WORKFLOW_COMPUTATION_MUST_REMAIN_FULL")
            helper_names = [key for key, _, _ in request.output_bindings
                            if A.E.strict_json(key)[-1] == name("hidden_low")[0]]
            cases.append({"case": "real-original-private-public-correspondence",
                          "private_units": len(ids), "public_units": len(bound.public_unit_ids),
                          "checked_units": 0, "mathematical_acceptance": False})

            def refuse(label, change, expected):
                check()
                altered = copy.deepcopy(report)
                change(altered)
                raw = encoded(altered)
                try:
                    R.bind_report(raw, sha(raw), request=request,
                        replay_request_raw=snapshot.replay_request_raw, check_budget=check)
                except ValueError as error:
                    need(str(error) == expected, "NATIVE_WORKFLOW_WRONG_REPORT_REFUSAL:"+str(error))
                else:
                    raise AssertionError("NATIVE_WORKFLOW_MISSING_REPORT_REFUSAL:"+label)
                cases.append({"case": label, "expected_refusal": expected, "altered_sha256": sha(raw)})

            refuse("changed-context", lambda doc: doc.__setitem__("context_root", "0"*64),
                   "REFERENCE_REPORT_IDENTITY:context_root")
            refuse("missing-target", lambda doc: doc.__setitem__("targets", []), "REFERENCE_REPORT_TARGETS")
            refuse("changed-private-census", lambda doc: doc["private_unit_ids"].pop(),
                   "REFERENCE_REPORT_PRIVATE_CENSUS")

            def illegal_erasure(doc):
                for unit in doc["public_units"]:
                    for row in unit["outputs"]:
                        if row["name"] == targets[0]:
                            row["projection"] = "erased_singleton_theorem"
                            return
                raise AssertionError("NATIVE_WORKFLOW_MISSING_PUBLIC_FLIP")

            refuse("erase-computational-definition", illegal_erasure, "REFERENCE_REPORT_PROJECTION")
            refuse("changed-node-census", lambda doc: doc.__setitem__("encoded_nodes", doc["encoded_nodes"]+1),
                   "REFERENCE_REPORT_COUNTER_CENSUS")
            refuse("changed-unit-byte-census", lambda doc: doc.__setitem__("unit_array_bytes", doc["unit_array_bytes"]+1),
                   "REFERENCE_REPORT_UNIT_BYTES")
            phase = "NATIVE_NEGATIVE_PREPARATION"
            negative = copy.deepcopy(selected)
            flip_rows = [row for row in negative["units"] if row["unit"][1][1] == targets[0]]
            need(len(flip_rows) == 1, "NATIVE_WORKFLOW_UNIQUE_FLIP")
            unit = flip_rows[0]["unit"]
            need(unit[1][0] == 0 and len(unit[2]) == 1 and unit[2][0][1] == 1,
                 "NATIVE_WORKFLOW_FLIP_DEFINITION_SHAPE")
            low, high = name("DMKNBaselineFixture", "Flag", "low"), name("DMKNBaselineFixture", "Flag", "high")

            def swap(value):
                if value == low:
                    return copy.deepcopy(high)
                if value == high:
                    return copy.deepcopy(low)
                if type(value) is list:
                    return [swap(child) for child in value]
                if type(value) is dict:
                    return {key: swap(child) for key, child in value.items()}
                return value

            changed_body = swap(unit[1][4])
            need(changed_body != unit[1][4] and unit[2][0][4][0] == unit[1][4],
                 "NATIVE_WORKFLOW_CHANGED_BODY_PRECONDITION")
            unit[1][4] = changed_body
            unit[2][0][4][0] = copy.deepcopy(changed_body)
            negative_raw = A.E.canonical_json(negative)
            negative_path, negative_report = output/"test-only-changed-body-request.json", output/"negative-report.json"
            save(negative_path, negative_raw)
            expected = "ORDINARY_REFERENCE_BASE PRIVATE_INVENTORY_MISMATCH name=DMKNBaselineFixture.flip"
            # This input intentionally has no warrant, and its original labels
            # do not claim identities for the altered mathematics. The native
            # matcher must inspect actual records and reject the changed body.
            run("reject-changed-transparent-body", [str(native["reference"]), str(inventory_path),
                str(snapshot.directory/"replay-request.json"), str(negative_path), str(negative_report)], expected)
            need(not os.path.lexists(negative_report), "NATIVE_WORKFLOW_NEGATIVE_CREATED_REPORT")
            cases.append({"case": "native-changed-transparent-body", "expected_refusal": expected,
                "request_sha256": sha(negative_raw), "report_created": False,
                "diagnostic_sha256": saved[str(output/"native-negative-stderr.txt")]["sha256"]})
            need(not forbidden_calls and len(completed) == 5 and len(cases) == 8,
                 "NATIVE_WORKFLOW_EXACT_SCOPE")
            phase = "FINAL_REHASH"
            for path, pin in (*build_pins.items(), *saved.items()):
                need(B.pin(Path(path), check, 64*MIB) == pin, "NATIVE_WORKFLOW_FINAL_PIN:"+path)
            manifest = A.E.strict_json(snapshot.manifest_raw, A.E.Limits(max_bytes=S.MAX_MANIFEST))
            for row in manifest["modules"]:
                for path, pin in zip(S._matrix(row["parts"]), S._matrix(row["pins"])):
                    need(B.pin(Path(path), check, S.MAX_PART) == pin, "NATIVE_WORKFLOW_SNAPSHOT_CHANGED")
            for filename, raw in (("prepared-manifest.json", snapshot.manifest_raw),
                                  ("replay-request.json", snapshot.replay_request_raw),
                                  ("source-report.json", artifact_raw)):
                need(read(snapshot.directory/filename, S.MAX_MANIFEST) == raw,
                     "NATIVE_WORKFLOW_SNAPSHOT_METADATA_CHANGED")
            spool = census()
            receipt = {"schema": "DMKN_ORDINARY_BASELINE_NATIVE_WORKFLOW_V1",
                "status": "COMPLETED_BOUNDARY_DISCRIMINATOR_REQUIRES_OUTER_CLOSURE_AUDIT",
                "mathematical_acceptance": False, "protected_reference_registered": False,
                "context": "TEST_ONLY_NOT_CURRENT_WARRANTS", "completed_commands": completed,
                "cases": cases, "forbidden_calls": forbidden_calls,
                "fixture_parts": {Path(path).name: pin for path, pin in saved.items() if Path(path).parent == fixture},
                "bundle_manifest_sha256": bundle.manifest.sha256,
                "snapshot_manifest_sha256": snapshot.manifest_sha256,
                "request_sha256": request.sha256, "report_sha256": bound.sha256,
                "private_names": len(request.output_bindings), "public_bindings":
                    [{"name": A.E.strict_json(key), "export_id": symbol, "unit_id": identity,
                      "projection": projection, "kernel_projection": kernel_projection}
                     for key, symbol, identity, projection, kernel_projection in bound.public_bindings],
                "hidden_helper_observations": [{"name": A.E.strict_json(key),
                    "in_private_closure": True, "in_public_closure": key in public_lookup,
                    "projections": list(public_lookup[key][2:]) if key in public_lookup else None}
                    for key in helper_names],
                "artifact_bytes": snapshot.artifact_bytes, "spool_before_receipt": spool,
                "spool_maximum_bytes": SPOOL, "spool_kind": "COOPERATIVE_CENSUS_NOT_HARD_QUOTA",
                "wall_seconds": time.monotonic()-started, "controller_cpu_seconds": time.process_time()-cpu,
                "inclusive_cpu_and_closure": "ONLY_ENCLOSING_JOB_RESULT",
                "next_step": "REVIEW_ONLY_NO_AUTOMATIC_ADMISSION_REGISTRATION_OR_RETRY"}
            save(output/"WORKFLOW.json", encoded(receipt), 2*MIB)
            census()
            print(json.dumps({"status": receipt["status"], "cases": len(cases)}), flush=True)
    except BaseException as error:
        try:
            B.fresh_bytes(output/"WORKFLOW-FAILURE.json", encoded({
                "phase": phase, "error_type": type(error).__name__, "error": str(error)[:2048],
                "completed_commands": completed, "cases": cases,
                "retention": "ALL_PARTIAL_FILES_PRESERVED_NO_RETRY", "mathematical_acceptance": False,
                "wall_seconds": time.monotonic()-started, "controller_cpu_seconds": time.process_time()-cpu,
                "inclusive_cpu_and_closure": "ONLY_ENCLOSING_JOB_RESULT"}))
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("source-root", "output", "build-number", "build-sha256", "build-result-sha256",
                "build-selection-sha256", "report-sha256"):
        parser.add_argument("--"+key, required=True)
    main(parser.parse_args())

"""One selected correspondence continuation over retained workflow02 bytes.

No compile, collection, export, snapshot copy, owner or registry action. Two
native matcher calls and nine report mutations share one enclosing finite Job.
The explicit test request and saved reports confer no mathematical authority.
"""
from pathlib import Path
import argparse
from contextlib import ExitStack
import copy
import hashlib
import importlib.util
import json
import os
import socket
import sqlite3
import subprocess
import sys
import time
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_baseline/"
LOCAL = ROOT/"experiments/v5-local-checks"
RETAINED = LOCAL/"ordinary-baseline-native-workflow-02"
OLD = RETAINED/"workflow"
NAME = "ordinary-reference-continuation-01"
MIB = 1024**2
INNER_SPOOL = 106*MIB
UTILITY = "native_workflow02.py"
FIXED = {
    UTILITY: "4ed662dfdfe04172ce74d2b2f0ad460b4a6ef09bf171eaa27ed9e8abdd72ad56",
    "baseline_bundle.py": "d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce",
    "baseline_snapshot.py": "ab2a0adcdd0b632d14fe2ec7058f9ef496b788760eff4ddd4852d01d11dd3468",
    "reference_request.py": "a4cadb4beb75bdf86b7314a2c05e301cbbafd42da8500ccd524c82c7a7503923",
    "snapshot_reopen.py": "74bb337025bacbde6274bf72ca06d37c23e7b16dca46750b333f363c7a1774d7",
}
PRESERVED = {
    "RESULT.json": "8461abd6cd7a4d971bb22c9058133fa51065b9eeb24ea383d1d89d9f0e0c8fab",
    "selection.json": "9ed0c25ff7a3ade3a72dfa5889c6a8f6aa48e580b04093e911a4dfa2ffcba9cc",
    "workflow/WORKFLOW-FAILURE.json": "63ed0081ca3c16f74931850dea4510dfab5417afea677be84b9e7ca97dd7b3dd",
    "workflow/INPUTS.json": "bd3ad9c5663470cae532298ae32f3c85c88db5ea4a27b9b0e2c42d3bb68b9680",
    "workflow/inventory.json": "c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0",
    "workflow/writer-bundle.json": "9768cb31cebb62c7743705d342caca6625cb92760010ede3c12d6bfc5dd9999b",
    "workflow/bundle/manifest.json": "b601bee8f6be2b2fc2315818ba81f340ed8bd72a43ac89cf547db001e7bc9cde",
    "workflow/test-only-reference-request.json": "638b89e486f3b66e2c9089ac721274351aa29cd48ddb358f00a95faebc1395d2",
    "workflow/snapshot/prepared-manifest.json": "f47f738be2fc3e6497e7cd839d4c9f61674e9c6d951f863105be50877ff21238",
    "command/stderr.txt": "a7fde21cdbeb5ae9fad88edd63aad1b9900287aad9f3b590a96d9e3b5f1ad2dd",
    "command/stdout.txt": "c6ab5589c2b06c18b044dcbaef5045ca6127c977f887aa28d9c2d8946e0de150",
}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def load_utilities(source):
    path = source/UTILITY
    raw = path.read_bytes()
    need(len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == FIXED[UTILITY],
         "REFERENCE_CONTINUATION_UTILITY_PIN")
    spec = importlib.util.spec_from_file_location("_reference_continuation_utilities", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def pin(B, path, expected, check, maximum=32*MIB):
    value = B.pin(B.ordinary(Path(path)), check, maximum)
    need(value == expected or value["sha256"] == expected, "REFERENCE_CONTINUATION_PIN:"+str(path))
    return value


def inspect_retained(B, H, check):
    pins = {str(RETAINED/key): pin(B, RETAINED/key, digest, check)
            for key, digest in PRESERVED.items()}
    result = json.loads(H.read(RETAINED/"RESULT.json"))
    failure = json.loads(H.read(OLD/"WORKFLOW-FAILURE.json"))
    event = result["result"]
    need(result["selection_sha256"] == PRESERVED["selection.json"] and
         event["status"] == "COMMAND_FAILED" and event["child_exit_code"] == 1 and
         event["direct_child_reaped"] is True and event["job_closed"] is True and
         event["cleanup_errors"] == [] and event["termination_requested"] is False and
         event["final_job"]["active_processes"] == event["final_job"]["terminated_processes"] == 0 and
         failure["phase"] == "exact-map-correspondence" and failure["cases"] == [] and
         [(row["phase"], row["exit_code"]) for row in failure["completed_commands"]] ==
         [("fixture-compile", 0), ("collect-original-library", 0),
          ("export-selected-targets", 0), ("exact-map-correspondence", 1)],
         "REFERENCE_CONTINUATION_PRESERVED_FAILURE")
    need(b"PRIVATE_CORRESPONDENCE_COMPLETE units=6 names=9" in H.read(RETAINED/"command/stderr.txt") and
         b"PUBLIC_COMPUTATIONAL_OR_NONSINGLETON_ERASURE" in H.read(RETAINED/"command/stderr.txt"),
         "REFERENCE_CONTINUATION_PRESERVED_PHASES")
    return pins


def inspect_matcher(B, H, args, check):
    """Bind explicit owner-selected successful build, never infer from presence."""
    paths = {key: B.ordinary(Path(getattr(args, key))) for key in
             ("matcher", "matcher_source", "matcher_build", "matcher_result", "matcher_selection")}
    source_root = ROOT/PREFIX
    need(paths["matcher_source"].parent == source_root and paths["matcher_source"].suffix == ".lean",
         "REFERENCE_CONTINUATION_MATCHER_SOURCE_SCOPE")
    build_root = paths["matcher_build"].parent
    need(build_root.name == "build" and build_root.parent.parent == LOCAL and
         paths["matcher_result"] == build_root.parent/"RESULT.json" and
         paths["matcher_selection"] == build_root.parent/"selection.json" and
         paths["matcher"].is_relative_to(build_root) and paths["matcher"].suffix == ".exe",
         "REFERENCE_CONTINUATION_BUILD_SCOPE")
    pins = {str(path): pin(B, path, getattr(args, key+"_sha256"), check)
            for key, path in paths.items()}
    build = json.loads(H.read(paths["matcher_build"]))
    result = json.loads(H.read(paths["matcher_result"]))
    selection = json.loads(H.read(paths["matcher_selection"]))
    event = result["result"]
    need(result["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1" and
         result["selection_sha256"] == args.matcher_selection_sha256 and
         event["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and event["child_exit_code"] == 0 and
         event["direct_child_reaped"] is True and event["job_closed"] is True and
         event["cleanup_errors"] == [] and event["termination_requested"] is False and
         event["final_job"]["active_processes"] == event["final_job"]["terminated_processes"] == 0,
         "REFERENCE_CONTINUATION_BUILD_CLOSURE")
    need(build["schema"] == "DMKN_ORDINARY_REFERENCE_NATIVE_BUILD_V1" and
         build["status"] == "BUILT_CANDIDATE_NOT_INSTALLED_OR_ADOPTED" and
         build["mathematical_acceptance"] is False and len(build["completed_commands"]) == 3 and
         all(row["exit_code"] == 0 for row in build["completed_commands"]),
         "REFERENCE_CONTINUATION_BUILD_RECEIPT")
    for key, role in (("matcher_source", "source"), ("matcher", "executable")):
        need(build[role] == {"path": str(paths[key]), **pins[str(paths[key])]},
             "REFERENCE_CONTINUATION_BUILD_ROLE")
    relative = paths["matcher_source"].relative_to(ROOT).as_posix()
    need(selection["schema"] == "DMKN_V5_LOCAL_CHECK_V1" and
         selection["name"] == build_root.parent.name and
         selection["sources"][relative] == args.matcher_source_sha256,
         "REFERENCE_CONTINUATION_BUILD_SOURCE_SELECTION")
    snapshot = build_root.parent/"sources"/relative
    pins[str(snapshot)] = pin(B, snapshot, pins[str(paths["matcher_source"])], check)
    need(type(build["inputs"]) is dict and 1 <= len(build["inputs"]) <= 128,
         "REFERENCE_CONTINUATION_BUILD_INPUT_CENSUS")
    for filename, expected in build["inputs"].items():
        path = B.ordinary(Path(filename))
        need(filename in selection["runtime_pins"] and
             selection["runtime_pins"][filename] == expected["sha256"],
             "REFERENCE_CONTINUATION_BUILD_INPUT_SELECTION")
        observed = pin(B, path, expected, check, 512*MIB)
        need(filename not in pins or pins[filename] == observed, "REFERENCE_CONTINUATION_PIN_CONFLICT")
        pins[filename] = observed
    return pins, paths["matcher"]


def add_arguments(parser):
    for key in ("matcher", "matcher-source", "matcher-build", "matcher-result", "matcher-selection"):
        parser.add_argument("--"+key, required=True)
        parser.add_argument("--"+key+"-sha256", required=True)
    parser.add_argument("--report-source", required=True)
    parser.add_argument("--report-sha256", required=True)


def main(args):
    started, cpu = time.monotonic(), time.process_time()
    deadline = started+105

    def check():
        need(time.monotonic() < deadline and time.process_time()-cpu < 50,
             "REFERENCE_CONTINUATION_ORIGINAL_ALLOWANCE")

    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "REFERENCE_CONTINUATION_PROCESS")
    source_root = Path(args.source_root)
    H = load_utilities(source_root/PREFIX)
    need(Path(sys.executable).resolve() == H.PYTHON/"python.exe", "REFERENCE_CONTINUATION_PYTHON")
    B = H.helper()
    source_root = B.ordinary(source_root, directory=True)
    output = B.ordinary(Path(args.output), directory=True, fresh=True)
    need(output == LOCAL/NAME/"continuation" and
         Path(__file__).resolve() == source_root/PREFIX/"reference_continuation.py",
         "REFERENCE_CONTINUATION_LOCATIONS")
    source = source_root/PREFIX
    for filename, digest in FIXED.items():
        pin(B, source/filename, digest, check, 2*MIB)
    report_source = B.ordinary(Path(args.report_source))
    need(report_source.parent == ROOT/PREFIX and report_source.suffix == ".py" and
         report_source.name.startswith("reference_report"), "REFERENCE_CONTINUATION_REPORT_SCOPE")
    report_local = source/report_source.name
    pin(B, report_local, args.report_sha256, check, 2*MIB)
    retained_pins = inspect_retained(B, H, check)
    matcher_pins, executable = inspect_matcher(B, H, args, check)
    descriptor_raw = H.read(H.PACKAGE/"PROFILE.json")
    need(H.sha(descriptor_raw) == H.PROFILE, "REFERENCE_CONTINUATION_PROFILE")
    descriptor = json.loads(descriptor_raw)
    owner_module = H.module("_reference_continuation_owner", H.PACKAGE/"owner.py",
                            descriptor["files"]["owner.py"]["sha256"])
    loader = owner_module.bootstrap(H.PACKAGE, H.PROFILE, check)
    loaded = loader.load(H.PACKAGE, H.PROFILE, {"python_runtime": H.PYTHON, "lean_runtime": H.LEAN},
                         deadline, check_parent=check)
    A, O = loaded.A, loaded.O
    D = H.module("baseline_bundle", source/"baseline_bundle.py", FIXED["baseline_bundle.py"])
    S = H.module("baseline_snapshot", source/"baseline_snapshot.py", FIXED["baseline_snapshot.py"])
    Q = H.module("reference_request", source/"reference_request.py", FIXED["reference_request.py"])
    V = H.module("snapshot_reopen", source/"snapshot_reopen.py", FIXED["snapshot_reopen.py"])
    R = H.module("reference_report", report_local, args.report_sha256)
    need(D.E is A.E and D.S is A.S and D.PE is A.PE and S.A is A and Q.A is A and
         V.A is A and V.S is S and R.A is A and R.Q is Q and R.S is S,
         "REFERENCE_CONTINUATION_SHARED_MODULES")
    output.mkdir()
    saved, completed, cases, forbidden_calls = {}, [], [], []
    phase = "RETAINED_VALIDATION"

    def save(path, raw, maximum=2*MIB):
        check()
        need(type(raw) is bytes and 0 < len(raw) <= maximum, "REFERENCE_CONTINUATION_SAVE_BOUND")
        B.fresh_bytes(path, raw)
        expected = {"bytes": len(raw), "sha256": H.sha(raw)}
        pin(B, path, expected, check, maximum)
        saved[str(path)] = expected

    def census():
        total, count = 0, 0
        for path in output.iterdir():
            check()
            B.ordinary(path)
            total += path.stat().st_size
            count += 1
            need(total <= INNER_SPOOL and count <= 16, "REFERENCE_CONTINUATION_SPOOL_BOUND")
        return {"bytes": total, "files": count}

    def forbidden(*_, **__):
        forbidden_calls.append("FORBIDDEN_OWNER_OR_NETWORK")
        raise AssertionError("REFERENCE_CONTINUATION_FORBIDDEN_OWNER_OR_NETWORK")

    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON", "RUST", "CARGO", "RISC0", "NODE"))
           and key.upper() not in ("PATH", "VIRTUAL_ENV")}
    env["PATH"] = str(H.LEAN/"bin")

    def run(label, request_path, report_path, refusal=None):
        nonlocal phase
        check(); phase = label
        need(len(completed) < 2, "REFERENCE_CONTINUATION_NATIVE_COUNT")
        argv = [str(executable), str(OLD/"inventory.json"), str(OLD/"snapshot/replay-request.json"),
                str(request_path), str(report_path)]
        need(sum(len(value)+3 for value in argv) <= 30000, "REFERENCE_CONTINUATION_COMMAND_BOUND")
        before = time.monotonic()
        if refusal:
            diagnostic = output/"negative-stderr.txt"
            with diagnostic.open("xb") as stream:
                result = subprocess.run(argv, cwd=output, env=env, stdin=subprocess.DEVNULL,
                    stderr=stream, creationflags=subprocess.CREATE_NO_WINDOW,
                    timeout=max(0.001, deadline-before))
            raw = H.read(diagnostic, MIB)
            saved[str(diagnostic)] = {"bytes": len(raw), "sha256": H.sha(raw)}
            sys.stderr.write(raw.decode("utf-8", errors="strict")); sys.stderr.flush()
        else:
            result = subprocess.run(argv, cwd=output, env=env, stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW, timeout=max(0.001, deadline-before))
        completed.append({"phase": label, "argv": argv, "exit_code": result.returncode,
                          "wall_seconds": time.monotonic()-before, "expected_failure": refusal})
        print(json.dumps(completed[-1], sort_keys=True), flush=True)
        need(result.returncode == (1 if refusal else 0), "REFERENCE_CONTINUATION_NATIVE_RESULT")
        if refusal:
            need(refusal.encode("ascii") in raw and not os.path.lexists(report_path),
                 "REFERENCE_CONTINUATION_NATIVE_NEGATIVE")
        census()

    try:
        with ExitStack() as stack:
            for obj, key in ((sqlite3, "connect"), (socket, "socket"),
                    (A.OrdinaryAdmission, "open"), (A.OrdinaryAdmission, "_execute"),
                    (A.P.PortableCatalog, "open"), (A.P.PortableCatalog, "_commit_checked"),
                    (O.OrdinaryStore, "__init__"), (O.OrdinaryStore, "put_evidence")):
                stack.enter_context(patch.object(obj, key, forbidden))
            snapshot_sha = PRESERVED["workflow/snapshot/prepared-manifest.json"]
            before_view = V.read_snapshot(OLD/"snapshot", snapshot_sha,
                loaded.installation.manifest_sha256, check_budget=check)
            inventory = H.read(OLD/"inventory.json", MIB)
            targets = [H.name("DMKNBaselineFixture", "flip"), H.name("DMKNBaselineFixture", "flip_low")]
            bundle = D.bind_writer(H.read(OLD/"writer-bundle.json", 32*MIB), inventory, targets, check_budget=check)
            need(bundle.manifest.raw == H.read(OLD/"bundle/manifest.json"),
                 "REFERENCE_CONTINUATION_RETAINED_BUNDLE")
            units, identities, evidence_pins, bindings = [], [], [], []
            for batch in bundle.batches:
                for raw in batch:
                    check()
                    item = A.PE.read_evidence(raw)
                    path = OLD/"bundle/units"/(item.unit_id+".json")
                    need(H.read(path, 8*MIB) == raw, "REFERENCE_CONTINUATION_RETAINED_UNIT")
                    retained_pins[str(path)] = {"bytes": len(raw), "sha256": H.sha(raw)}
                    outputs = []
                    for row in item.document["unit"][2]:
                        symbol = A.S.export_id(A.S.semantic_id(), item.unit_id, row[0])
                        outputs.append({"name": row[0], "export_id": symbol})
                        bindings.append((A.E.name_key(row[0]), symbol, item.unit_id))
                    units.append({"unit_id": item.unit_id, "unit": item.document["unit"], "outputs": outputs})
                    identities.append(item.unit_id)
                    evidence_pins.append((item.unit_id, len(raw), H.sha(raw)))
            old_inputs = json.loads(H.read(OLD/"INPUTS.json"))
            selected = {"schema": Q.SCHEMA, "semantic_id": A.S.semantic_id(),
                "foundation_id": A.S.foundation_id(),
                "context_root": H.sha(b"DMKN_TEST_ONLY_NOT_ACCEPTED_CONTEXT_V1"+bundle.manifest.raw),
                "snapshot_id": snapshot_sha,
                "support_id": H.sha(b"DMKN_TEST_ONLY_NOT_ACCEPTED_SUPPORT_V1"+
                                    H.encoded(old_inputs["authorized_build_pins"])),
                "units": units, "targets": [{"name": A.E.strict_json(target.name),
                    "export_id": target.export_id} for target in bundle.targets]}
            request_raw = A.E.canonical_json(selected)
            need(request_raw == H.read(OLD/"test-only-reference-request.json", 16*MIB),
                 "REFERENCE_CONTINUATION_IDENTICAL_TEST_REQUEST")
            request = Q.ReferenceRequest(request_raw, H.sha(request_raw), inventory, tuple(identities),
                tuple(evidence_pins), tuple(sorted(bindings)), bundle.census.nodes, bundle.census.edges)
            request_path, report_path = output/"test-request.json", output/"positive-report.json"
            save(request_path, request_raw, 16*MIB)
            save(output/"INPUTS.json", H.encoded({"schema": "DMKN_REFERENCE_CONTINUATION_INPUTS_V1",
                "retained": retained_pins, "matcher": matcher_pins,
                "report_source": str(report_source), "report_sha256": args.report_sha256,
                "required_flip_projections": ["full", "full"],
                "context": "TEST_ONLY_NOT_CURRENT_WARRANTS", "mathematical_acceptance": False,
                "snapshot_manifest_sha256": snapshot_sha, "snapshot_copied": False}))
            run("changed-matcher-correspondence", request_path, report_path)
            report_raw = H.read(report_path, 32*MIB)
            saved[str(report_path)] = {"bytes": len(report_raw), "sha256": H.sha(report_raw)}
            bound = R.bind_report(report_raw, H.sha(report_raw), request=request,
                replay_request_raw=before_view.replay_raw, check_budget=check)
            report = A._writer_json(report_raw, 32*MIB)
            lookup = {key: (symbol, identity, projection, kernel_projection)
                      for key, symbol, identity, projection, kernel_projection in bound.public_bindings}
            need(lookup[A.E.name_key(targets[0])][2:] == ("full", "full"),
                 "REFERENCE_CONTINUATION_EXPECTED_FLIP_PROJECTIONS")
            need(lookup[A.E.name_key(targets[1])][2:] ==
                 ("erased_singleton_theorem", "erased_singleton_theorem"),
                 "REFERENCE_CONTINUATION_EXPECTED_THEOREM_PROJECTIONS")
            hidden_keys = [key for key, _, _ in request.output_bindings
                           if A.E.strict_json(key)[-1] == H.name("hidden_low")[0]]
            need(len(hidden_keys) == 1 and hidden_keys[0] not in lookup,
                 "REFERENCE_CONTINUATION_PRIVATE_HELPER_NOT_PUBLIC")
            cases.append({"case": "retained-original-private-public-correspondence",
                          "public_units": len(bound.public_unit_ids), "mathematical_acceptance": False})

            def refuse(label, change, expected):
                check()
                altered = copy.deepcopy(report)
                change(altered)
                raw = H.encoded(altered)
                try:
                    R.bind_report(raw, H.sha(raw), request=request,
                        replay_request_raw=before_view.replay_raw, check_budget=check)
                except ValueError as error:
                    need(str(error) == expected, "REFERENCE_CONTINUATION_REPORT_REFUSAL:"+str(error))
                else:
                    raise AssertionError("REFERENCE_CONTINUATION_REPORT_ACCEPTED:"+label)
                cases.append({"case": label, "expected_refusal": expected, "altered_sha256": H.sha(raw)})

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
                raise AssertionError("REFERENCE_CONTINUATION_MISSING_FLIP")

            refuse("erase-computational-definition", illegal_erasure, "REFERENCE_REPORT_PROJECTION")
            refuse("changed-node-census", lambda doc: doc.__setitem__("encoded_nodes", doc["encoded_nodes"]+1),
                   "REFERENCE_REPORT_COUNTER_CENSUS")
            refuse("changed-unit-byte-census", lambda doc: doc.__setitem__("unit_array_bytes", doc["unit_array_bytes"]+1),
                   "REFERENCE_REPORT_UNIT_BYTES")
            refuse("basis-node-budget-overflow", lambda doc: doc.__setitem__("basis_scan_nodes", 20000001),
                   "REFERENCE_REPORT_COUNTER_CENSUS")

            def absent_basis_usable(doc):
                absent = [row["name"] for row in doc["public_basis"]
                          if "absent" in (row["projection"], row["kernel_projection"])]
                need(bool(absent), "REFERENCE_CONTINUATION_ABSENT_BASIS_PRECONDITION")
                keys = {A.E.name_key(name) for name in doc["usable_basis_names"]}
                key = A.E.name_key(absent[0])
                need(key not in keys, "REFERENCE_CONTINUATION_ABSENT_BASIS_NOT_ALREADY_USABLE")
                keys.add(key)
                # Preserve inventory order so the rejected fact is absence,
                # not an unrelated duplicate or ordering violation.
                doc["usable_basis_names"] = [row["name"] for row in doc["public_basis"]
                                               if A.E.name_key(row["name"]) in keys]

            def wrong_basis_abstract_kind(doc):
                for row in doc["public_basis"]:
                    if row["kind"] == 1 and row["projection"] == "abstract_singleton_definition":
                        row["projection"] = "abstract_singleton_opaque"
                        return
                raise AssertionError("REFERENCE_CONTINUATION_ABSTRACT_BASIS_PRECONDITION")

            refuse("absent-basis-declared-usable", absent_basis_usable, "REFERENCE_REPORT_USABLE_BASIS")
            refuse("basis-abstract-kind-mismatch", wrong_basis_abstract_kind, "REFERENCE_REPORT_BASIS_PROJECTION")
            phase = "NATIVE_NEGATIVE_PREPARATION"
            negative = copy.deepcopy(selected)
            flip_rows = [row for row in negative["units"] if row["unit"][1][1] == targets[0]]
            need(len(flip_rows) == 1, "REFERENCE_CONTINUATION_UNIQUE_FLIP")
            unit = flip_rows[0]["unit"]
            need(unit[1][0] == 0 and len(unit[2]) == 1 and unit[2][0][1] == 1,
                 "REFERENCE_CONTINUATION_FLIP_SHAPE")
            low, high = H.name("DMKNBaselineFixture", "Flag", "low"), H.name("DMKNBaselineFixture", "Flag", "high")

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

            changed = swap(unit[1][4])
            need(changed != unit[1][4] and unit[2][0][4][0] == unit[1][4],
                 "REFERENCE_CONTINUATION_NEGATIVE_PRECONDITION")
            unit[1][4] = changed; unit[2][0][4][0] = copy.deepcopy(changed)
            negative_path = output/"changed-body-request.json"
            save(negative_path, A.E.canonical_json(negative), 16*MIB)
            expected = "ORDINARY_REFERENCE_BASE PRIVATE_INVENTORY_MISMATCH name=DMKNBaselineFixture.flip"
            run("reject-changed-transparent-body", negative_path, output/"negative-report.json", expected)
            cases.append({"case": "native-changed-transparent-body", "expected_refusal": expected,
                          "report_created": False})
            phase = "FINAL_REVALIDATION"
            after_view = V.read_snapshot(OLD/"snapshot", snapshot_sha,
                loaded.installation.manifest_sha256, check_budget=check)
            need(after_view == before_view, "REFERENCE_CONTINUATION_SNAPSHOT_CHANGED")
            for path, expected in (*retained_pins.items(), *matcher_pins.items(), *saved.items()):
                pin(B, Path(path), expected, check, 512*MIB)
            need(not forbidden_calls and len(completed) == 2 and len(cases) == 11,
                 "REFERENCE_CONTINUATION_EXACT_SCOPE")
            receipt = {"schema": "DMKN_ORDINARY_REFERENCE_CONTINUATION_V1",
                "status": "COMPLETED_BOUNDARY_CONTINUATION_REQUIRES_OUTER_CLOSURE_AUDIT",
                "mathematical_acceptance": False, "protected_reference_registered": False,
                "context": "TEST_ONLY_NOT_CURRENT_WARRANTS", "completed_commands": completed,
                "cases": cases, "forbidden_calls": forbidden_calls, "snapshot_copied": False,
                "retained_snapshot_bytes": before_view.artifact_bytes,
                "snapshot_manifest_sha256": snapshot_sha, "request_sha256": request.sha256,
                "report_sha256": bound.sha256, "private_units": len(identities),
                "basis_summary": {"bound_names": len(bound.basis_bindings),
                    "common_present_names": sum(projection != "absent" and kernel_projection != "absent"
                        for _, _, _, projection, kernel_projection in bound.basis_bindings),
                    "usable_names": len(bound.usable_basis_keys),
                    "scan_nodes": report["basis_scan_nodes"], "edges": report["basis_edges"],
                    "pruning_rounds": report["basis_pruning_rounds"],
                    "authority": "LIVE_CORRESPONDENCE_METADATA_NOT_PROTECTED_REGISTRATION"},
                "hidden_helper": {"name": A.E.strict_json(hidden_keys[0]),
                                  "present_private": True, "present_public": False},
                "public_bindings": [{"name": A.E.strict_json(key), "export_id": symbol,
                    "unit_id": identity, "projection": projection, "kernel_projection": kernel_projection}
                    for key, symbol, identity, projection, kernel_projection in bound.public_bindings],
                "spool_before_receipt": census(), "fresh_spool_maximum_bytes": INNER_SPOOL,
                "spool_kind": "COOPERATIVE_CENSUS_NOT_HARD_QUOTA",
                "wall_seconds": time.monotonic()-started, "controller_cpu_seconds": time.process_time()-cpu,
                "inclusive_cpu_and_closure": "ONLY_ENCLOSING_JOB_RESULT",
                "next_step": "REVIEW_ONLY_NO_AUTOMATIC_ADMISSION_REGISTRATION_OR_RETRY"}
            save(output/"CONTINUATION.json", H.encoded(receipt)); census()
            print(json.dumps({"status": receipt["status"], "cases": len(cases)}), flush=True)
    except BaseException as error:
        try:
            B.fresh_bytes(output/"CONTINUATION-FAILURE.json", H.encoded({"phase": phase,
                "error_type": type(error).__name__, "error": str(error)[:2048],
                "completed_commands": completed, "cases": cases, "mathematical_acceptance": False,
                "retention": "ALL_RETAINED_AND_FRESH_OUTPUT_PRESERVED_NO_RETRY",
                "wall_seconds": time.monotonic()-started, "controller_cpu_seconds": time.process_time()-cpu,
                "inclusive_cpu_and_closure": "ONLY_ENCLOSING_JOB_RESULT"}))
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output", required=True)
    add_arguments(parser)
    main(parser.parse_args())

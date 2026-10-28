"""Only native02's two unrun negatives; root selects execution separately."""
from pathlib import Path
from types import SimpleNamespace
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
OLD = LOCAL / "demand-frontier-native02/workflow"
PACKAGE = LOCAL / "demand-frontier-package01/distribution/package"
PROFILE = "6af0c3dee0a08d0ba0ec9f126dc6510481fc99569535c41b4ecb56c4bf3c3735"
INPUTS = {
    OLD.parent / "RESULT.json": "2fd85217844d559a6a7f11376fd610453e24810c2d14daf7843f0836c3aee300",
    OLD / "OUTCOME.json": "b7c325064c378a137c55d182ebe18190e4494ddb19642138d7bb20f5b525f277",
    OLD / "LIMITS.json": "3db1141f914388742d97f51539260c9a7e22eb0979472321b731faa911f802af",
    OLD / "FRONTEND-PINS.json": "cda4598055aa787ad57d34ae64afe8310ee4fde0a6a62c253e7e10600c0c6c68",
}
F = "90825f1b8218c08af43335b1692e8b3a7918c84732bf1a450ef359484c20fefd"
P = "d0b4bcfa16e72ec840e52aa0b31ecd94b3457e7bd717c1d34b1f2bff0b57453c"


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    helper = OLD.parent / "sources/software/v5/ordinary_demand_frontier/native_workflow02.py"
    raw = helper.read_bytes()
    if len(raw) != 24213 or hashlib.sha256(raw).hexdigest() != \
            "e5ac5c841b48431ce3d627a2b42ad751254350cea478c616dbae436edca5ed05":
        raise ValueError("FRONTIER_REMAINING_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_frontier_remaining_frozen", helper)
    W = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = W
    exec(compile(raw, str(helper), "exec", dont_inherit=True), W.__dict__)
    need, name = W.need, W.name
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and Path(sys.executable).resolve() == W.PYTHON,
         "CANONICAL_PROCESS")
    source = Path(__file__).resolve().parent
    need(source.is_relative_to(LOCAL) and source.parts[-4:] ==
         ("sources", "software", "v5", "ordinary_demand_frontier"), "SOURCE_SNAPSHOT")
    utility = helper.parent.parent / "ordinary_fair_search/assemble.py"
    H = W.load(utility, "_frontier_remaining_files",
               {"bytes": utility.stat().st_size, "sha256": W.HELPER_SHA})
    allowance = W.Allowance(180, 100)
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    need(output == source.parents[3] / "workflow" and output != OLD and
         not output.is_relative_to(OLD) and not OLD.is_relative_to(output), "FRESH_OUTPUT")
    old_docs, pins = {}, {}
    for path, sha in INPUTS.items():
        old_docs[path], pins[str(path)] = H.read_json(path, sha, allowance.check)
    W.closed(old_docs[OLD.parent / "RESULT.json"]["result"], False)
    old = old_docs[OLD / "OUTCOME.json"]
    need(old["status"] == "FAILED" and old["phase"] == "positive" and old["close_errors"] == [] and
         old["error"] == "FRONTIER_NATIVE_EXACT_REFLEXIVITY_PROOF" and
         len(old["setup"]) == 2 and len(old["cases"]) == 1, "EXACT_CLOSED_PREDECESSOR")
    support = old_docs[OLD / "FRONTEND-PINS.json"]
    expected_support = {str(OLD / folder / (module + suffix)) for folder, module in
        (("setup-f/lean-build", "OrdinaryProducer"), ("alternate/lean-lib", "AlternateBase")) for suffix in W.PARTS}
    need(set(support) == expected_support, "EXACT_EXISTING_FRONTENDS")
    pins.update(support)
    pins[str(helper)] = H.pin(helper, allowance.check)
    pins[str(utility)] = H.pin(utility, allowance.check)
    for row in (*old["setup"], old["cases"][0]["result"]):
        need(len(row["units"]) == len(row["targets"]) == 1 and row["admission"]["status"] == "CHECKED",
             "ACCEPTED_PREDECESSOR_CONTRIBUTION")
        unit = row["units"][0]
        pins[unit["file"]] = {key: unit[key] for key in ("bytes", "sha256")}
    for path, pin in pins.items():
        need(H.pin(Path(path), allowance.check, 32*W.MIB) == pin, "PRESERVED_INPUT_CHANGED")
    profile, profile_pin = H.read_json(PACKAGE / "PROFILE.json", PROFILE, allowance.check)
    cli = W.load(PACKAGE / "owner.py", "_frontier_remaining_owner", profile["files"]["owner.py"])
    loaded = cli.bootstrap(PACKAGE, PROFILE, allowance.check).load(PACKAGE, PROFILE,
        {"python_runtime": W.PYTHON.parent, "lean_runtime": W.LEAN}, allowance.deadline,
        check_parent=allowance.check)
    A, G, O, installation = loaded.A, loaded.G, loaded.O, loaded.installation
    need(installation.manifest_sha256 == W.INSTALLATION and
         installation.implementation_id == W.IMPLEMENTATION, "UNCHANGED_RECEIVER")
    output.mkdir()
    save = lambda path, value: H.fresh_bytes(path, H.canonical(value))
    read_json = lambda path: json.loads(A.C.read_bounded(path, 2*W.MIB))
    report = {"status": "FAILED", "phase": "REOPEN", "cases": [], "predecessor": str(OLD),
              "profile_sha256": PROFILE, "implementation_id": W.IMPLEMENTATION}
    owner = custody = None
    try:
        save(output / "PRESERVED-INPUTS.json", pins)
        save(output / "LIMITS.json", {"wall_seconds": 180, "cpu_seconds": 100,
            "false_parent": [90, 45], "missing": [60, 25], "unchanged_owner_limits": old_docs[OLD / "LIMITS.json"]})
        limits = old_docs[OLD / "LIMITS.json"]
        custody = O.OrdinaryStore(OLD / "custody", installation.semantic_id, limits["custody"], create=False)
        owner = A.OrdinaryAdmission.open(installation, OLD / "catalog",
            H.digest(b"DMKN-FRONTIER-CONTROL\0" + str(OLD).encode("utf-8")), custody,
            create=False, limits=A.P.Limits(**limits["catalog"]))
        inventory = lambda: cli.status(owner, custody,
            SimpleNamespace(limit=16, after_root="", context_root=None), allowance.check)["roots"]

        def calls():
            entries = list(owner.calls.iterdir())
            need(len(entries) <= 5 and all(H.ordinary(path, directory=True) for path in entries), "CALL_CENSUS")
            return set(entries)

        first, second = old["setup"]
        positive = old["cases"][0]["result"]
        base, above = first["targets"][0], second["targets"][0]
        need(first["local_root"] == F and second["local_root"] == P and second["parent_root"] == F and
             positive["admission"]["status"] == "CHECKED" and positive["parent_root"] == P,
             "EXACT_SAVED_LINEAGE")
        expected_roots = [{"local_root": old["basis"]["local_root"], "parent_root": ""}] + [
            {"local_root": row["local_root"], "parent_root": row["parent_root"]} for row in (first, second, positive)]
        initial_roots = inventory()
        need(initial_roots == sorted(expected_roots, key=lambda row: row["local_root"]), "EXACT_FOUR_ROOTS")
        expected_calls = {Path(row["operation_directory"]) for row in
                          (old["basis"], first["admission"], second["admission"], positive["admission"])}
        need(len(expected_calls) == 4 and calls() == expected_calls, "EXACT_FOUR_CALLS")
        frontier, parent = owner.catalog.context(F), owner.catalog.context(P)
        G._require_frontier_prefix(parent, frontier, P, F, allowance.check)
        for row, target, text, body in ((first, base, "Base.c", W.numeral(0)),
                (second, above, "Above.d", W.app(W.constant("Nat.succ"), W.constant("Base.c")))):
            item = A.PE.read_evidence(A.C.read_bounded(Path(row["units"][0]["file"]), W.MIB))
            unit = item.document["unit"]
            need(item.unit_id == target["unit_id"] and target["name"] == name(text) and
                 unit[1][:3] == [0, name(text), []] and W.expression(unit[1][3]) == W.constant("Nat") and
                 W.expression(unit[1][4]) == body and
                 parent["bindings"][A.P.E.name_key(name(text))] == target["export_id"], "EXACT_PARENT_MEANING")
        need(frontier["bindings"][A.P.E.name_key(base["name"])] == base["export_id"] and
             A.P.E.name_key(above["name"]) not in frontier["bindings"] and
             [base["name"], base["export_id"]] in item.document["imports"], "EXACT_CUT_BINDING")
        save(output / "BEFORE.json", {"roots": initial_roots, "calls": sorted(map(str, expected_calls)),
            "frontier": {k: v for k, v in frontier.items() if k != "bindings"},
            "parent": {k: v for k, v in parent.items() if k != "bindings"}, "base": base, "above": above})
        for label, theorem, rhs, imported, cap in (
                ("false-parent", "FrontierFalse.wrong", "Nat.succ (Nat.succ Nat.zero)", "AlternateBase", (90, 45)),
                ("missing", "FrontierMissing.unreachable", "Nat.succ Nat.zero", "Init", (60, 25))):
            report["phase"] = label
            stage, before_calls = W.Allowance(*cap, parent=allowance), calls()
            trace, saved_get = [], custody.get_evidence

            def traced(semantic_id, unit_id, max_bytes, *, check_budget=None):
                need(not trace and unit_id == above["unit_id"] and unit_id != base["unit_id"],
                     "FORBIDDEN_OR_REPEATED_EVIDENCE_FETCH")
                trace.append({"semantic_id": semantic_id, "unit_id": unit_id, "maximum": max_bytes})
                raw = saved_get(semantic_id, unit_id, max_bytes, check_budget=check_budget)
                trace[-1].update(bytes=len(raw), sha256=H.digest(raw))
                return raw

            backend = G.TrustedProjectAuthoring.from_document({"schema": G.PROJECT_SCHEMA,
                "module_name": theorem.split(".")[0], "project_cwd": str(output),
                "project_search_paths": [str(OLD / "alternate/lean-lib")],
                "imports": [{"module": imported, "meta": False}]})
            body = f"theorem {theorem} : Above.d = {rhs} := Eq.refl Above.d\n".encode("ascii")
            save(output / (label + "-INPUTS.json"), {"parent_root": P, "frontier_root": F, "acquired": [above],
                "source": body.decode("ascii"), "backend": backend.to_document(), "wall_cpu_seconds": list(cap)})
            directory, result, failure = output / label, None, None
            custody.get_evidence = traced
            try:
                result = G.contribute_source(owner, P, [above], body, [name(theorem)], output_directory=directory,
                    profile=loaded.profile, parent_deadline=stage.deadline, make_budget=lambda: stage.operation(A),
                    account_worker_cpu=stage.account, check_parent=stage.check,
                    authoring_backend=backend, authoring_frontier_root=F)
            except G.ContributionError as error:
                failure = error.report
            finally:
                custody.get_evidence = saved_get
                save(output / (label + "-FETCHES.json"), trace)
            row = {"case": label, "result": result, "failure": failure, "evidence_reads": trace}
            report["cases"].append(row)
            request, header = read_json(directory / "REQUEST.json"), read_json(directory / "owner-request/header.json")
            need(request["parent_root"] == P and request["acquired_targets"] == [above] and
                 request["project_authoring"]["frontier_root"] == F and request["groups"] == len(trace) == 1 and
                 len(request["fetched"]) == 1 and request["fetched"][0]["unit_id"] == above["unit_id"] and
                 header["schema"] == "DMKN_OWNER_REQUEST_V3" and header["frontier_root"] == F and
                 header["frontier_labels"] == [[name("Base.c"), base["export_id"]]], "ACTUAL_FRONTIER_REQUEST")
            authoring = read_json(directory / "AUTHORING-SUPERVISION.json")
            log = (directory / "authoring-supervision/stdout.txt").read_bytes()
            need(log.count(b"PORTABLE_OWNER_CONSTRUCT_PHASE ENTERED_EXISTING_OWNER_ENVIRONMENT") == 1,
                 "SINGLE_AUTHORING_CONSTRUCTION")
            new_calls = calls() - before_calls
            if label == "false-parent":
                need(result is None and failure["phase"] == "ADMISSION" and failure["accepted"] is None and
                     failure["error"] == "ADMISSION_NATIVE_EVENT_NOT_CLEAN" and len(new_calls) == 1,
                     "SEMANTIC_NEGATIVE_INCONCLUSIVE_EARLY_REFUSAL")
                W.closed(authoring, True)
                need(log.count(b"CONSTRUCTED_READY_FOR_AUTHORING_INSTALL") == 1 and b"checkedUnits=1 " in log,
                     "NEGATIVE_DID_NOT_CONSTRUCT_RECEIVED_DEFINITION")
                call = next(iter(new_calls))
                W.closed(read_json(call / "supervision-result.json"), False)
                units = read_json(call / "units.json")
                need(len(units) == 1 and not (call / "worker-report.json").exists(), "NEGATIVE_NATIVE_INPUT")
                row["mathematics"] = W.theorem_shape(units[0], theorem, 2)
                diagnostic = (call / "supervision/stdout.txt").read_bytes() + (call / "supervision/stderr.txt").read_bytes()
                need(b"KERNEL_REJECTED_OR_RESOURCE_LIMIT" in diagnostic, "NEGATIVE_NATIVE_MARKER")
            else:
                need(result is None and failure["phase"] == "AUTHORING" and failure["accepted"] is None and
                     not new_calls and not (directory / "candidate.json").exists(), "MISSING_AUTHORING_FAILURE")
                W.closed(authoring, False)
                need(b"CONSTRUCTED_READY_FOR_AUTHORING_INSTALL" not in log, "MISSING_CONSTRUCTION_COMPLETED")
                diagnostic = log + (directory / "authoring-supervision/stderr.txt").read_bytes()
                need(b"MISSING_DEMANDED_FRONTIER_KERNEL Base.c" in diagnostic or
                     b"MISSING_DEMANDED_FRONTIER_FRONTEND Base.c" in diagnostic, "MISSING_WRONG_REFUSAL")
            need(inventory() == initial_roots and owner.catalog.context(P) == parent and
                 owner.catalog.context(F) == frontier, "ACCEPTED_STATE_CHANGED")
            row["status"] = "PASS"
            save(output / (label + "-OUTCOME.json"), row)
        for path, pin in pins.items():
            need(H.pin(Path(path), allowance.check, 32*W.MIB) == pin, "PRESERVED_INPUT_CHANGED")
        need(H.pin(PACKAGE / "PROFILE.json", allowance.check) == profile_pin, "PROFILE_CHANGED")
        loaded.profile.verify(allowance.check)
        need(H.pin(PACKAGE / "installation/INSTALLATION.json", allowance.check)["sha256"] == W.INSTALLATION,
             "INSTALLATION_CHANGED")
        for logical, pin in installation.doc["files"].items():
            need(H.pin(installation.resolve(logical), allowance.check) == pin, "RECEIVER_SUPPORT_CHANGED")
        need(len(calls()) == 5 and inventory() == initial_roots, "EXACT_FINAL_CENSUS")
        save(output / "AFTER.json", {"roots": inventory(), "calls": sorted(map(str, calls()))})
        report.update(status="PASS_TWO_REMAINING_FRONTIER_NEGATIVES", frontier_root=F, parent_root=P,
            new_admission_calls=1, authoring_invocations=2, compilations=0, accepted_roots=4,
            claim="FINITE_NEGATIVE_CONTINUATION_NOT_REPLACEMENT_FOR_FAILED_PREDECESSOR_OR_V5_RELEASE")
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error))
        raise
    finally:
        close_errors = []
        for label, value in (("owner", owner), ("custody", custody)):
            if value is not None:
                try:
                    value.close()
                except BaseException as error:
                    close_errors.append({"component": label, "error": str(error)})
        report.update(close_errors=close_errors, wall_seconds=time.monotonic() - allowance.started,
            controller_cpu_seconds=time.process_time() - allowance.cpu_started,
            observed_or_conservatively_reserved_worker_cpu=allowance.charged)
        if close_errors:
            report["status"] = "FAILED_CLOSE"
        save(output / "OUTCOME.json", report)
    need(report["status"] == "PASS_TWO_REMAINING_FRONTIER_NEGATIVES", "FINAL_OUTCOME")
    print(H.canonical(report).decode("utf-8"), flush=True)


if __name__ == "__main__":
    main()

"""One public normal-project contribution using an already paid local module.

Source-only until separately selected. One original150wall/90CPU allowance;
outer180wall/110CPU/2048MiB/8process, derived1536MiB native grants. No module
rebuild, initialization, state copy, network, certificate or automatic retry.
This is reciprocal interoperability, NOT a novelty or mathematical-growth test.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import re
import stat
import sys

UTILITY_SHA = "20f6c613eb8fdd051b1f7df923e528e2c01874eb2e2c6277e3aca73d8475ccfd"
MODULE_NAME = "DMKNBridge_450bf7c15f3af7aa703934147ce9cd2fa1fbb5a50ec2dca7f7e41bbf1714f458"
MODULE_MANIFEST_SHA = "d447b491cb4166035063377e36757c1f14b1340fe6dcec423a60a3b18b6735e8"
MODULE_REPORT_SHA = "035de7d52abe5a71ba41b7a48ba0b1382f0e9037dae50cdb7cb4ba26bb968b48"
INSTALLATION_SHA = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
TWICE_EXPORT = "b5054e3c29436f1fe8d175b47df405405f76683d7c1e27531d9e597f2e55ee02"


def diagnostic_json(raw):
    """Operational reports allow booleans and finite floats; math parsers do not."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("PROJECT_RETURN_DUPLICATE_REPORT_KEY")
            result[key] = value
        return result
    def finite_float(text):
        value = float(text)
        if not math.isfinite(value):
            raise ValueError("PROJECT_RETURN_NONFINITE_NUMBER")
        return value
    def reject(_):
        raise ValueError("PROJECT_RETURN_REPORT_CONSTANT")
    return json.loads(raw, object_pairs_hook=pairs, parse_float=finite_float, parse_constant=reject)


def name(text):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in text.split(".")]


def source_body():
    return b"""universe u v

theorem CommonsReturnExample.mapFour {a : Type u} {b : Type v}
    (f : a -> a) (g : b -> b) (h : a -> b)
    (step : forall y, h (f y) = g (h y)) (x : a) :
    h (CommonsPackageExample.applyTwice f (CommonsPackageExample.applyTwice f x)) =
      CommonsPackageExample.applyTwice g (CommonsPackageExample.applyTwice g (h x)) :=
  Eq.trans (congrArg h (@CommonsPeerExample.applyFour_eq a f x))
    (Eq.trans (step (f (f (f x))))
      (Eq.trans (congrArg g (step (f (f x))))
        (Eq.trans (congrArg (fun z => g (g z)) (step (f x)))
          (Eq.trans (congrArg (fun z => g (g (g z))) (step x))
            (Eq.symm (@CommonsPeerExample.applyFour_eq b g (h x)))))))
"""


def load_utility(args):
    utility = Path(args.utility)
    expected = Path(args.output)/"sources/software/v5/ordinary_module_bridge/native_check03.py"
    if args.utility_sha256 != UTILITY_SHA or not utility.is_absolute() or \
            ".." in utility.parts or utility != expected:
        raise ValueError("PROJECT_RETURN_REVIEWED_UTILITY")
    for item in (*reversed(utility.parents), utility):
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("PROJECT_RETURN_UTILITY_REDIRECT")
    info = utility.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or not 0 < info.st_size <= 2*1024**2:
        raise ValueError("PROJECT_RETURN_UTILITY_BOUND")
    with utility.open("rb") as stream:
        raw = stream.read(2*1024**2+1)
    if len(raw) != info.st_size or hashlib.sha256(raw).hexdigest() != UTILITY_SHA:
        raise ValueError("PROJECT_RETURN_UTILITY_PIN")
    spec = importlib.util.spec_from_file_location("_project_return_utility", utility)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    exec(compile(raw, str(utility), "exec"), module.__dict__)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("package", "profile-sha256", "utility", "utility-sha256", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    U = load_utility(args)
    U.need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
           not sys.flags.optimize and Path(sys.executable) == U.PYTHON, "PROJECT_RETURN_PYTHON")
    output = U.ordinary(Path(args.output), directory=True)
    package = U.ordinary(Path(args.package), directory=True)
    previous = U.LOCAL/"ordinary-module-public-native-01/export"
    U.need(output.is_relative_to(U.LOCAL) and package.is_relative_to(U.LOCAL) and
           all(not output.is_relative_to(path) and not path.is_relative_to(output)
               for path in (package, U.OLD, previous.parent)), "PROJECT_RETURN_SELECTED_PATHS")
    allowance = U.Allowance()
    report = {"status": "FAILED", "phase": "SUPPORT", "public_result": None,
              "new_catalog_acceptance": None,
              "claim": "NORMAL_PROJECT_MODULE_TO_CHECKED_CONTRIBUTION_INTEROPERABILITY_NOT_GROWTH"}
    preserved = None

    def retained_map():
        rows = U.retained_map()
        for path in (previous/"MODULE.json", previous/"native-report.json",
                     *(previous/"modules"/(MODULE_NAME+suffix) for suffix in
                       (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir"))):
            raw = U.read(path, 64*U.MIB)
            rows[str(path)] = {"bytes": len(raw), "sha256": U.sha(raw)}
        U.need(len(rows) == 16, "PROJECT_RETURN_PRESERVED_CENSUS")
        return rows

    try:
        allowance.check()
        profile_raw = U.read(package/"PROFILE.json", 2*U.MIB)
        U.need(U.sha(profile_raw) == args.profile_sha256, "PROJECT_RETURN_PROFILE_PIN")
        descriptor = diagnostic_json(profile_raw)
        cli = U.load_exact(package/"owner.py", "_project_return_owner", descriptor["files"]["owner.py"])
        loader = cli.bootstrap(package, args.profile_sha256, allowance.check)
        loaded = loader.load(package, args.profile_sha256,
            {"python_runtime": U.PYTHON.parent, "lean_runtime": U.LEAN}, allowance.deadline,
            check_parent=allowance.check)
        A, G, installation = loaded.A, loaded.G, loaded.installation
        U.need(installation.manifest_sha256 == INSTALLATION_SHA,
               "PROJECT_RETURN_SAME_NATIVE_INSTALLATION")
        acquired = [{"name": name("CommonsPeerExample.applyFour_eq"),
                     "export_id": U.EXPORT, "unit_id": U.UNIT}]
        output_names = [name("CommonsReturnExample.mapFour")]
        module_raw = U.read(previous/"MODULE.json", U.MIB)
        module = diagnostic_json(module_raw)
        U.need(U.sha(module_raw) == MODULE_MANIFEST_SHA and module["module_name"] == MODULE_NAME and
               module["status"] == "CHECKED_PROOF_COMPLETE_LOCAL_MODULE" and
               module["source_context_root"] == U.PARENT and module["targets"] == acquired and
               module["semantic_id"] == installation.semantic_id and
               module["foundation_id"] == A.S.foundation_id() and
               module["report_sha256"] == MODULE_REPORT_SHA and
               U.sha(U.read(previous/"native-report.json", 8*U.MIB)) == MODULE_REPORT_SHA,
               "PROJECT_RETURN_PAID_MODULE_BINDING")
        expected_names = {MODULE_NAME+suffix for suffix in
                          (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir")}
        U.need(set(module["artifact_parts"]) == expected_names and
               {path.name for path in (previous/"modules").iterdir()} == expected_names,
               "PROJECT_RETURN_PAID_MODULE_CENSUS")
        for filename, expected_pin in module["artifact_parts"].items():
            raw = U.read(previous/"modules"/filename, 64*U.MIB)
            U.need(expected_pin == {"bytes": len(raw), "sha256": U.sha(raw)},
                   "PROJECT_RETURN_PAID_MODULE_PIN")
        preserved = retained_map()
        U.save(output/"PRESERVED-BEFORE.json", preserved)
        project = output/"project-workspace"
        project.mkdir()
        configuration = {"schema": G.PROJECT_SCHEMA, "module_name": "CommonsReturnExample",
            "project_cwd": str(project), "project_search_paths": [str(previous/"modules")],
            "imports": [{"module": MODULE_NAME, "meta": False}]}
        backend = G.TrustedProjectAuthoring.from_document(configuration)
        U.need(backend.verify(allowance.check) == configuration, "PROJECT_RETURN_IMPORT_PREFLIGHT")
        inputs = {"mapFour.lean": source_body(), "acquired-targets.json": acquired,
                  "output-names.json": output_names, "project.json": configuration}
        input_pins = {filename: U.save(output/filename, value) for filename, value in inputs.items()}
        command_dir = output/"public-command"
        command_dir.mkdir()
        allocation = allowance.operation(A)
        allocation.claim()
        limits = installation._supervisor.limits_checked(allocation.allowance(allowance.deadline))
        wall, cpu = int(limits["wall_seconds"])-3, int(limits["cpu_seconds"])-1
        U.need(wall >= 35 and cpu >= 4, "PROJECT_RETURN_REMAINING_CLI_GRANT")
        argv = [str(U.PYTHON), "-I", "-S", "-B", str(package/"owner.py"), "contribute",
            "--profile-sha256", args.profile_sha256,
            "--python-runtime", str(U.PYTHON.parent), "--lean-runtime", str(U.LEAN),
            "--catalog", str(U.OLD/"B-catalog"), "--custody", str(U.OLD/"B-custody"),
            "--store-id", U.STORE, "--custody-limits", str(U.OLD/"B-custody-limits.json"),
            "--wall-seconds", str(wall), "--cpu-seconds", str(cpu), "--memory-mib", "1536",
            "--parent-root", U.PARENT, "--source", str(output/"mapFour.lean"),
            "--acquired-targets", str(output/"acquired-targets.json"),
            "--output-names", str(output/"output-names.json"),
            "--project-authoring", str(output/"project.json"),
            "--project-authoring-sha256", input_pins["project.json"]["sha256"],
            "--output", str(output/"contribution")]
        U.save(command_dir/"COMMAND.json", {"argv": argv, "limits": limits, "inputs": input_pins,
            "operation": "PUBLIC_CONTRIBUTE_USING_EXISTING_PAID_MODULE_ONLY"})
        report["phase"] = "PUBLIC_CONTRIBUTE"
        supervision = None
        try:
            supervision = installation._supervisor.supervise(argv, U.ROOT,
                command_dir/"supervision", limits, installation._job_module.Job)
        finally:
            final = supervision.get("final_job") if type(supervision) is dict else None
            cpu = final.get("cpu_seconds") if type(final) is dict else None
            measured = type(cpu) in (int, float) and math.isfinite(cpu) and cpu >= 0
            charged = cpu if measured else limits["cpu_seconds"]
            allowance.account(charged)
            report["public_accounting"] = {"measured_cpu_seconds": cpu if measured else None,
                "conservative_cpu_reservation_charged": 0 if measured else charged}
        U.save(command_dir/"SUPERVISION.json", supervision)
        report["public_supervision"] = supervision
        stdout = U.read(command_dir/"supervision/stdout.txt", U.MIB)
        if stdout:
            report["public_result"] = diagnostic_json(stdout)
        # Preserve the actual response, including any already accepted result,
        # before checking subsequent assertions. Failure never implies rollback.
        public = report["public_result"]
        if type(public) is dict:
            nested_result = public.get("result")
            report["accepted_outcome"] = (nested_result.get("admission", public.get("accepted"))
                if type(nested_result) is dict else public.get("accepted"))
        U.need(A._clean_worker(supervision) and
               U.read(command_dir/"supervision/stderr.txt", U.MIB) == b"",
               "PROJECT_RETURN_COMMAND_FAILED")
        U.need(type(public) is dict and public.get("ok") is True and public["operation"] == "contribute" and
               public["store_id"] == U.STORE and public["profile_sha256"] == args.profile_sha256 and
               public["catalog"] == str(U.OLD/"B-catalog") and public["custody"] == str(U.OLD/"B-custody"),
               "PROJECT_RETURN_PUBLIC_RESPONSE")
        result = public["result"]
        report["new_catalog_acceptance"] = result["admission"]
        directory = output/"contribution"
        U.need(result == diagnostic_json(U.read(directory/"RESULT.json", U.MIB)) and
               result["admission"] == diagnostic_json(U.read(directory/"ADMISSION.json", U.MIB)) and
               result["status"] == "CHECKED_CONTRIBUTION_WITH_DURABLE_PUBLICATION_BYTES" and
               result["parent_root"] == U.PARENT and result["local_root"] != U.PARENT and
               result["admission"]["status"] == "CHECKED" and result["admission"]["units_checked"] == 1 and
               result["admission"]["local_root"] == result["local_root"] and
               result["acquired_targets"] == acquired and len(result["targets"]) == 1 and
               result["targets"][0]["name"] == output_names[0] and len(result["units"]) == 1 and
               len(result["previews"]) == 1, "PROJECT_RETURN_CHECKED_FRESH_RESULT")
        request = diagnostic_json(U.read(directory/"REQUEST.json", 2*U.MIB))
        U.need(request["parent_root"] == U.PARENT and request["acquired_targets"] == acquired and
               request["output_names"] == output_names and
               request["source_body_sha256"] == input_pins["mapFour.lean"]["sha256"] and
               request["project_authoring"]["configuration"] == configuration,
               "PROJECT_RETURN_REQUEST_BINDING")
        generated_path = directory/"owner-source/CommonsReturnExample.lean"
        generated = U.read(generated_path, 2*U.MIB)
        expected_generated = G.assemble_source(source_body=source_body(),
            request_directory=directory/"owner-request", semantic_id=installation.semantic_id,
            context_root=U.PARENT, foundation_id=A.S.foundation_id(), targets_file=directory/"targets.json",
            candidate_file=directory/"candidate.json", authoring_backend=backend)
        U.need(generated == expected_generated and request["generated_source"] ==
               {"bytes": len(generated), "sha256": U.sha(generated)} and
               not list(project.iterdir()), "PROJECT_RETURN_EXACT_GENERATED_PROJECT_SOURCE")
        authoring = diagnostic_json(U.read(directory/"AUTHORING-SUPERVISION.json", U.MIB))
        U.need(A._clean_worker(authoring) and "--project-author-worker" in authoring["argv"] and
               U.read(directory/"authoring-supervision/stderr.txt", U.MIB) == b"",
               "PROJECT_RETURN_PROJECT_AUTHORING")
        construction_lines = [line for line in U.read(directory/"authoring-supervision/stdout.txt", U.MIB)
            .decode("utf-8").splitlines() if line.startswith(
                "PORTABLE_OWNER_CONSTRUCT_PHASE CONSTRUCTED_READY_FOR_AUTHORING_INSTALL ")]
        U.need(len(construction_lines) == 1 and re.search(
            r"\bintroducedNames=0 introducedSignatures=#\[\] checkedUnits=0\b", construction_lines[0]) is not None,
            "PROJECT_RETURN_IMPORTED_RECORDS_REUSED_WITHOUT_SCRATCH")
        candidate = A._writer_json(U.read(directory/"candidate.json", 4*U.MIB), 4*U.MIB)
        U.need(candidate["context_root"] == U.PARENT and candidate["targets"] == output_names and
               candidate["unresolved_imports"] == [] and len(candidate["units"]) == 1 and
               candidate["stats"]["source_records_enumerated"] == 0,
               "PROJECT_RETURN_COMPLETE_CANDIDATE")
        selected_unit = result["units"][0]
        evidence_path = directory/"evidence"/(selected_unit["unit_id"]+".json")
        evidence = U.read(evidence_path, 4*U.MIB)
        U.need(selected_unit == {"unit_id": selected_unit["unit_id"], "file": str(evidence_path),
               "bytes": len(evidence), "sha256": U.sha(evidence)}, "PROJECT_RETURN_EVIDENCE_PIN")
        item = A.PE.read_evidence(evidence)
        U.need(item.unit_id == selected_unit["unit_id"] and item.document["semantic_id"] == installation.semantic_id and
               item.document["unit"] == candidate["units"][0] and
               result["admission"]["retained_unit_ids"] == [item.unit_id], "PROJECT_RETURN_EXACT_ADMITTED_UNIT")
        imports = {A.E.name_key(row[0]): row[1] for row in item.document["imports"]}
        boundary = {A.E.name_key(row[0]): row[1] for row in candidate["boundary_imports"]}
        for symbol, identity in ((acquired[0]["name"], U.EXPORT),
                                 (name("CommonsPackageExample.applyTwice"), TWICE_EXPORT)):
            U.need(imports.get(A.E.name_key(symbol)) == identity and
                   boundary.get(A.E.name_key(symbol)) == identity, "PROJECT_RETURN_EXACT_PARENT_IMPORT")
        unit = item.document["unit"]
        U.need(unit[1][0] == 1 and unit[1][1] == output_names[0] and
               len(unit[2]) == 1 and unit[2][0][0] == output_names[0] and unit[2][0][1] == 2,
               "PROJECT_RETURN_GENUINE_THEOREM")
        proof_nodes = unit[1][4][2]
        use_count = sum(node[0] == 2 and node[1] == acquired[0]["name"] for node in proof_nodes)
        U.need(use_count == 2, "PROJECT_RETURN_TWO_UNIVERSE_ACQUIRED_PROOF_USES")
        target = result["targets"][0]
        U.need(target["unit_id"] == item.unit_id and
               A.S.export_id(installation.semantic_id, item.unit_id, output_names[0]) == target["export_id"],
               "PROJECT_RETURN_PUBLICATION_IDENTITY")
        preview = result["previews"][0]
        preview_path = directory/"previews"/(target["export_id"]+".json")
        preview_raw = U.read(preview_path, U.MIB)
        U.need(preview == dict(target, file=str(preview_path), bytes=len(preview_raw), sha256=U.sha(preview_raw)),
               "PROJECT_RETURN_PREVIEW_PIN")
        G.PP.resolve(preview_raw, evidence)
        for filename, pin in input_pins.items():
            raw = U.read(output/filename, U.MIB)
            U.need(pin == {"bytes": len(raw), "sha256": U.sha(raw)}, "PROJECT_RETURN_INPUT_CHANGED")
        loaded.profile.verify(allowance.check)
        U.need(U.read(package/"PROFILE.json", 2*U.MIB) == profile_raw, "PROJECT_RETURN_PROFILE_CHANGED")
        allowance.check()
        report.update(status="PASS_PUBLIC_ORDINARY_PROJECT_RETURN", phase="COMPLETE",
            constructed_without_scratch=construction_lines[0], acquired_proof_constant_instantiations=use_count,
            new_target=target, retained_paid_module=MODULE_NAME, reused_module_rebuilt=False,
            mathematical_novelty_claim=False, measured_growth_claim=False)
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error))
    finally:
        if preserved is not None:
            try:
                after = retained_map()
                U.save(output/"PRESERVED-AFTER.json", after)
                U.need(after == preserved, "PROJECT_RETURN_PRIOR_ARTIFACT_CHANGED")
                report["prior_module_and_branch_artifacts_preserved"] = True
            except BaseException as error:
                report.update(status="FAILED", preservation_error=str(error))
        report.update(wall_seconds=U.time.monotonic()-U.START_WALL,
            controller_cpu_seconds=U.time.process_time()-U.START_CPU,
            charged_worker_cpu_seconds=allowance.charged_worker_cpu,
            cost_scope="Outer Job aggregate is authoritative; nested charges must not be added twice.")
        if report["wall_seconds"] >= 150 or report["controller_cpu_seconds"]+allowance.charged_worker_cpu >= 90:
            report.update(status="FAILED", budget_error="PROJECT_RETURN_ORIGINAL_ALLOWANCE")
        U.save(output/"PROJECT-RETURN-RESULT.json", report)
        print(json.dumps({"status": report["status"], "phase": report["phase"]}), flush=True)
    return 0 if report["status"] == "PASS_PUBLIC_ORDINARY_PROJECT_RETURN" else 1


if __name__ == "__main__":
    raise SystemExit(main())

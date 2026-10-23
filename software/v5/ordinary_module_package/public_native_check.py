"""One installed public export and normal consumer; no owner reset or network.

Reuses the already-reviewed normal-consumer/allowance utility as selected source.
Outer selection contains this entire process tree; no retry or budget renewal.
"""
from pathlib import Path
import argparse
import importlib.util
import json
import math
import stat
import sys


def diagnostic_json(raw):
    """Local operational reports contain booleans/floats, unlike math wire JSON."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("PUBLIC_MODULE_DUPLICATE_REPORT_KEY")
            result[key] = value
        return result
    def finite_float(text):
        value = float(text)
        if not math.isfinite(value):
            raise ValueError("PUBLIC_MODULE_NONFINITE_REPORT_NUMBER")
        return value
    def reject_constant(_):
        raise ValueError("PUBLIC_MODULE_REPORT_CONSTANT")
    return json.loads(raw, object_pairs_hook=pairs, parse_float=finite_float,
                      parse_constant=reject_constant)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("package", "profile-sha256", "utility", "utility-sha256", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    utility = Path(args.utility)
    if args.utility_sha256 != "20f6c613eb8fdd051b1f7df923e528e2c01874eb2e2c6277e3aca73d8475ccfd":
        raise ValueError("PUBLIC_MODULE_REVIEWED_UTILITY")
    expected = Path(args.output)/"sources/software/v5/ordinary_module_bridge/native_check03.py"
    if not utility.is_absolute() or ".." in utility.parts or utility != expected:
        raise ValueError("PUBLIC_MODULE_UTILITY_LOCATION")
    for item in (*reversed(utility.parents), utility):
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("PUBLIC_MODULE_UTILITY_REDIRECT")
    info = utility.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or not 0 < info.st_size <= 2*1024**2:
        raise ValueError("PUBLIC_MODULE_UTILITY_BOUND")
    # This exact source only defines functions; no owner or native action on import.
    with utility.open("rb") as source:
        raw = source.read(2*1024**2+1)
    import hashlib
    if hashlib.sha256(raw).hexdigest() != args.utility_sha256 or len(raw) != info.st_size:
        raise ValueError("PUBLIC_MODULE_UTILITY_PIN")
    spec = importlib.util.spec_from_file_location("_public_module_utility", utility)
    U = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = U
    exec(compile(raw, str(utility), "exec"), U.__dict__)
    U.need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
           not sys.flags.optimize and Path(sys.executable) == U.PYTHON,
           "PUBLIC_MODULE_PYTHON")
    output = U.ordinary(Path(args.output), directory=True)
    package = U.ordinary(Path(args.package), directory=True)
    U.need(output.is_relative_to(U.LOCAL) and package.is_relative_to(U.LOCAL) and
           not output.is_relative_to(package) and not package.is_relative_to(output) and
           utility == output/"sources/software/v5/ordinary_module_bridge/native_check03.py" and
           not output.is_relative_to(U.OLD) and not U.OLD.is_relative_to(output),
           "PUBLIC_MODULE_SELECTED_PATHS")
    allowance = U.Allowance()
    report = {"status": "FAILED", "phase": "SUPPORT", "public_result": None,
              "new_catalog_acceptance": False,
              "claim": "INSTALLED_PUBLIC_EXPORT_AND_NORMAL_CONSUMER_NOT_GENERAL_LIBRARY_OR_GROWTH"}
    preserved = None
    try:
        allowance.check()
        profile_raw = U.read(package/"PROFILE.json", 2*U.MIB)
        U.need(U.sha(profile_raw) == args.profile_sha256, "PUBLIC_MODULE_PROFILE_PIN")
        descriptor = json.loads(profile_raw)
        cli = U.load_exact(package/"owner.py", "_public_module_owner",
                           descriptor["files"]["owner.py"])
        loader = cli.bootstrap(package, args.profile_sha256, allowance.check)
        loaded = loader.load(package, args.profile_sha256,
            {"python_runtime": U.PYTHON.parent, "lean_runtime": U.LEAN},
            allowance.deadline, check_parent=allowance.check)
        A, installation = loaded.A, loaded.installation
        preserved = U.retained_map()
        U.save(output/"PRESERVED-BEFORE.json", preserved)
        target_name = [[0, {"$bytes": list(p.encode("ascii"))}]
                       for p in ("CommonsPeerExample", "applyFour_eq")]
        targets = [{"name": target_name, "export_id": U.EXPORT, "unit_id": U.UNIT}]
        target_path = output/"targets.json"
        target_pin = U.save(target_path, targets)
        command_dir = output/"public-command"
        command_dir.mkdir()
        allocation = allowance.operation(A)
        allocation.claim()
        limits = installation._supervisor.limits_checked(allocation.allowance(allowance.deadline))
        # Child CLI grant is strictly inside the enclosing selected command grant.
        wall = int(limits["wall_seconds"])-3
        cpu = int(limits["cpu_seconds"])-1
        U.need(wall >= 35 and cpu >= 4, "PUBLIC_MODULE_REMAINING_CLI_GRANT")
        argv = [str(U.PYTHON), "-I", "-S", "-B", str(package/"owner.py"), "export-module",
            "--profile-sha256", args.profile_sha256,
            "--python-runtime", str(U.PYTHON.parent), "--lean-runtime", str(U.LEAN),
            "--catalog", str(U.OLD/"B-catalog"), "--custody", str(U.OLD/"B-custody"),
            "--store-id", U.STORE, "--custody-limits", str(U.OLD/"B-custody-limits.json"),
            "--wall-seconds", str(wall), "--cpu-seconds", str(cpu), "--memory-mib", "1536",
            "--parent-root", U.PARENT, "--module-targets", str(target_path),
            "--output", str(output/"export")]
        U.save(command_dir/"COMMAND.json", {"argv": argv, "limits": limits,
            "targets": target_pin, "operation": "PUBLIC_EXPORT_MODULE_ONLY"})
        report["phase"] = "PUBLIC_EXPORT"
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
        U.need(A._clean_worker(supervision) and
               U.read(command_dir/"supervision/stderr.txt", U.MIB) == b"",
               "PUBLIC_MODULE_COMMAND_FAILED")
        public = report["public_result"]
        U.need(type(public) is dict and public.get("ok") is True and
               public["operation"] == "export-module" and public["store_id"] == U.STORE and
               public["profile_sha256"] == args.profile_sha256,
               "PUBLIC_MODULE_RESPONSE")
        result = public["result"]
        U.need(result["status"] == "CHECKED_PROOF_COMPLETE_LOCAL_MODULE" and
               result["source_context_root"] == U.PARENT and result["targets"] == targets and
               result["new_catalog_acceptance"] is False and
               result["module_directory"] == str(output/"export/modules") and
               result["manifest_path"] == str(output/"export/MODULE.json"),
               "PUBLIC_MODULE_SELECTED_RESULT")
        expected_runtime = {"installation_manifest_sha256": installation.manifest_sha256,
            "implementation_id": installation.implementation_id, "lean_runtime": str(U.LEAN),
            "lean_executable": str(installation.path("lean")),
            "lean_executable_pin": dict(installation.doc["files"][installation.doc["roles"]["lean"]]),
            "claim": "EXACT_SELECTED_LOCAL_RUNTIME_NOT_DOWNSTREAM_PROJECT_VALIDATION"}
        U.need(result["supported_runtime"] == expected_runtime, "PUBLIC_MODULE_RUNTIME_METADATA")
        manifest = diagnostic_json(U.read(output/"export/MODULE.json", U.MIB))
        U.need({k: v for k, v in result.items() if k not in
               ("module_directory", "manifest_path", "supported_runtime")} == manifest,
               "PUBLIC_MODULE_EXACT_MANIFEST")
        report["phase"] = "NORMAL_CONSUMER"
        report["normal_consumer"] = U.normal_consumer(loaded, result, output, allowance, report)
        for filename, pin in result["artifact_parts"].items():
            contents = U.read(output/"export/modules"/filename, 64*U.MIB)
            U.need(pin == {"bytes": len(contents), "sha256": U.sha(contents)},
                   "PUBLIC_MODULE_EXPORTED_PART_CHANGED")
        loaded.profile.verify(allowance.check)
        U.need(U.read(package/"PROFILE.json", 2*U.MIB) == profile_raw and
               target_pin == {"bytes": len(U.read(target_path)), "sha256": U.sha(U.read(target_path))},
               "PUBLIC_MODULE_INPUT_CHANGED")
        allowance.check()
        report.update(status="PASS_INSTALLED_PUBLIC_MODULE_REUSE", phase="COMPLETE")
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error))
    finally:
        if preserved is not None:
            try:
                after = U.retained_map()
                U.save(output/"PRESERVED-AFTER.json", after)
                U.need(after == preserved, "PUBLIC_MODULE_PRIOR_ARTIFACT_CHANGED")
                report["prior_branch_artifacts_preserved"] = True
            except BaseException as error:
                report.update(status="FAILED", preservation_error=str(error))
        report.update(wall_seconds=U.time.monotonic()-U.START_WALL,
            controller_cpu_seconds=U.time.process_time()-U.START_CPU,
            charged_worker_cpu_seconds=allowance.charged_worker_cpu,
            cost_scope="Outer Job aggregate is authoritative; child measurements are not added twice.")
        if report["wall_seconds"] >= 150 or report["controller_cpu_seconds"]+allowance.charged_worker_cpu >= 90:
            report.update(status="FAILED", budget_error="PUBLIC_MODULE_ORIGINAL_ALLOWANCE")
        U.save(output/"PUBLIC-MODULE-RESULT.json", report)
        print(json.dumps({"status": report["status"], "phase": report["phase"]}), flush=True)
    return 0 if report["status"] == "PASS_INSTALLED_PUBLIC_MODULE_REUSE" else 1


if __name__ == "__main__":
    raise SystemExit(main())

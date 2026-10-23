"""Existing-owner module export, normal consumer and exact collision refusal.

SOURCE-ONLY until root selects execution. Requires an outer Windows Job:
180 wall / 110 CPU / 2048 MiB / 8 processes. One original inner allowance:
150 wall / 90 CPU / 1536 MiB, including derived native grants and cleanup.
No owner initialization, new admission, state copy, network or certificate.
Three sequential native stages share that one original allowance; no retry.
"""
from pathlib import Path
import argparse
from dataclasses import replace
import hashlib
import importlib.util
import json
import math
import os
import stat
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
OLD = LOCAL/"ordinary-peer-reciprocal-02"
PYTHON = Path(r"D:\Python314\python.exe")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
BRIDGE = Path(__file__).absolute().parent
PROFILE = "e4c1734390c372f6884e14419ed1301825f1f58e98c4d0b86b4d5ac4e454c7bb"
STORE = "23421e020e9fe30b3aec293b6567996285af72fc16f54b311b71ffb113367167"
PARENT = "84dd6a9cf7ece45c4820ab3c28fc50ec072168c77e3cef9b890183bff5af9e13"
UNIT = "d52aed3d1d0f94b8ee2236a7ee84435c983c9523dca0f100f4369c183c3d4e51"
EXPORT = "0447787d07c5ada8730972d027bc25c5927e7c6552ef99c8fe4bdcda23285a6b"
COLLISION_PARENT = "b8363a72212a04c283cb9079fa3ea876aa172ad492e80cbc1fa9cc34da0c8928"
COLLISION_UNIT = "6f0a5a17f40dbca4e4f0eabb86c6d6a2dfd0eeb0056d36e81373a2e185cd51c8"
COLLISION_EXPORT = "ff50a5653b4cfd7c9ff2dac8c5403fcce66251bcabb5e05f9a8574871b51c093"
PREVIOUS_SHA = "c484d96cddf0a4e3985116a7632dabecbcac0386870926cd13a5bdc707282d5a"
ARTIFACTS = (
    "55cbddc0310a3d93ae4e2c555baa83e0ada1536b0290bf24f95b33d02f448bfe",
    "99303d20602ddd2932ed1fa693f5f29cf3ad91f4698f171e6192cec4d66241bb",
    "f156ac506d2a64dc89c344ead48a3f970834f1602d957a11b2de982a072693f2",
    "87e6a8c39afbadc98e8cab5ef2dc305e27ff265107fe4d2471a6c97fbd538494")
SOURCES = ("module_closure.py", "module_export.py", "module_worker03.py", "OrdinaryModule03.lean")
MIB = 1024**2
START_WALL, START_CPU = time.monotonic(), time.process_time()


def need(condition, code):
    if not condition:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      allow_nan=False, separators=(",", ":")).encode("ascii")


def ordinary(path, directory=False):
    need(path.is_absolute() and "." not in path.parts and ".." not in path.parts,
         "MODULE_CHECK_ABSOLUTE_PATH")
    for part in (path, *path.parents):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "MODULE_CHECK_REDIRECT")
    info = path.lstat()
    need(stat.S_ISDIR(info.st_mode) if directory else
         stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "MODULE_CHECK_PATH_KIND")
    return path


def read(path, maximum=4*MIB):
    ordinary(path)
    size = path.stat().st_size
    need(0 <= size <= maximum, "MODULE_CHECK_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "MODULE_CHECK_FILE_CHANGED")
    return raw


def save(path, value):
    ordinary(path.parent, directory=True)
    raw = value if type(value) is bytes else canonical(value)
    need(len(raw) <= 8*MIB, "MODULE_CHECK_OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)
    return {"bytes": len(raw), "sha256": sha(raw)}


def load_exact(path, name, pin):
    raw = read(path, 2*MIB)
    need(pin == {"bytes": len(raw), "sha256": sha(raw)} and name not in sys.modules,
         "MODULE_CHECK_EXECUTED_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


class Allowance:
    deadline = START_WALL+150

    def __init__(self):
        self.charged_worker_cpu = 0.0

    def check(self):
        need(time.monotonic() < self.deadline and
             time.process_time()-START_CPU+self.charged_worker_cpu < 90,
             "MODULE_CHECK_ORIGINAL_ALLOWANCE")

    def account(self, value):
        need(type(value) in (int, float) and math.isfinite(value) and value >= 0,
             "MODULE_CHECK_CPU_CHARGE")
        self.charged_worker_cpu += value

    def operation(self, A):
        self.check()
        wall = math.floor(self.deadline-time.monotonic())-3
        cpu = math.floor(90-(time.process_time()-START_CPU)-self.charged_worker_cpu)-1
        need(wall >= 30 and cpu >= 2, "MODULE_CHECK_REMAINING_GRANT")
        budget = A.OperationBudget(wall, cpu, 1536, active_processes=4, output_bytes=64*MIB)
        budget.deadline = min(budget.deadline, self.deadline)
        return budget


def retained_map():
    paths = [OLD/"RECIPROCAL-RESULT.json", OLD/"B-catalog/ADOPTION.json",
             OLD/"B-custody-limits.json", OLD/"B-contribution/ADMISSION.json",
             OLD/"B-contribution/RESULT.json",
             *(OLD/"B-catalog/operations"/item/"chunk.olean" for item in ARTIFACTS)]
    pins, total = {}, 0
    for path in paths:
        raw = read(path, 32*MIB)
        total += len(raw)
        need(total <= 64*MIB, "MODULE_CHECK_PRIOR_ARTIFACT_BOUND")
        pins[str(path)] = {"bytes": len(raw), "sha256": sha(raw)}
    return pins


def consumer_source(module_name):
    need(type(module_name) is str and len(module_name) == 75 and module_name.startswith("DMKNBridge_") and
         all(c in "0123456789abcdef" for c in module_name[11:]), "MODULE_CHECK_CONSUMER_IMPORT")
    return ("module\n\npublic import Init\npublic import "+module_name+"\n\npublic section\n\n"
        "universe u\n\n"
        "theorem NormalConsumer.applyFour {a : Type u} (f : a -> a) (x : a) :\n"
        "    CommonsPackageExample.applyTwice f (CommonsPackageExample.applyTwice f x) =\n"
        "      f (f (f (f x))) :=\n"
        "  @CommonsPeerExample.applyFour_eq a f x\n\n"
        "theorem NormalConsumer.reduceTwice {a : Type u} (f : a -> a) (x : a) :\n"
        "    CommonsPackageExample.applyTwice f x = f (f x) := rfl\n").encode("ascii")


def consumer_child(args):
    need(len(args) == 4, "MODULE_CHECK_CONSUMER_ARGS")
    lean, modules, source, output = map(Path, args)
    need(lean == LEAN/"bin/lean.exe" and source.name == "Consumer.lean" and
         output == source.with_suffix(".olean") and not os.path.lexists(output),
         "MODULE_CHECK_CONSUMER_FIXED_PATHS")
    ordinary(lean); ordinary(modules, directory=True); ordinary(source)
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
    env["LEAN_PATH"] = os.pathsep.join((str(LEAN/"lib/lean"), str(modules)))
    env["PATH"] = os.pathsep.join((str(PYTHON.parent), str(lean.parent)))
    argv = [str(lean), "-DElab.async=false", "-R", str(source.parent), "-o", str(output), str(source)]
    return subprocess.call(argv, cwd=source.parent, env=env, stdin=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)


def normal_consumer(loaded, module_result, output, allowance, report):
    A, installation = loaded.A, loaded.installation
    directory = output/"normal-consumer"
    directory.mkdir()
    source, olean = directory/"Consumer.lean", directory/"Consumer.olean"
    source_pin = save(source, consumer_source(module_result["module_name"]))
    script = ordinary(Path(__file__).absolute())
    self_pin = sha(read(script))
    argv = [str(PYTHON), "-I", "-S", "-B", str(script), "--consumer-child",
            str(installation.path("lean")), str(output/"export/modules"), str(source), str(olean)]
    budget = allowance.operation(A)
    budget.claim()
    limits = installation._supervisor.limits_checked(budget.allowance(allowance.deadline))
    save(directory/"COMMAND.json", {"argv": argv, "limits": limits,
        "source": source_pin, "search_path": "RUNTIME_AND_GENERATED_MODULES_ONLY"})
    supervision = None
    try:
        supervision = installation._supervisor.supervise(argv, directory, directory/"supervision",
            limits, installation._job_module.Job)
    finally:
        final = supervision.get("final_job") if type(supervision) is dict else None
        cpu = final.get("cpu_seconds") if type(final) is dict else None
        measured = type(cpu) in (int, float) and math.isfinite(cpu) and cpu >= 0
        charged = cpu if measured else limits["cpu_seconds"]
        allowance.account(charged)
        report["consumer_accounting"] = {"native_cpu_seconds": cpu if measured else None,
            "conservative_cpu_reservation_charged": 0 if measured else charged}
    save(directory/"SUPERVISION.json", supervision)
    report["consumer_supervision"] = supervision
    need(A._clean_worker(supervision) and
         read(directory/"supervision/stdout.txt", MIB) == b"" and
         read(directory/"supervision/stderr.txt", MIB) == b"", "MODULE_CHECK_NORMAL_CONSUMER_FAILED")
    need(read(source) == consumer_source(module_result["module_name"]) and
         sha(read(script)) == self_pin, "MODULE_CHECK_CONSUMER_SOURCE_CHANGED")
    produced = {}
    for suffix in (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir"):
        path = directory/("Consumer"+suffix)
        if os.path.lexists(path):
            raw = read(path, 16*MIB)
            need(bool(raw), "MODULE_CHECK_EMPTY_CONSUMER_PART")
            produced[path.name] = {"bytes": len(raw), "sha256": sha(raw)}
    need({"Consumer.olean", "Consumer.olean.server", "Consumer.olean.private"} <= set(produced),
         "MODULE_CHECK_NORMAL_CONSUMER_MODULE_PARTS")
    allowance.check()
    return {"source": source_pin, "parts": produced, "ordinary_import": True,
            "exact_theorem_application": True, "definition_reduction_by_rfl": True}


def collision_refusal(export_api, owner, profile, output, allowance, A, report):
    """One real selected boundary collision, not a malformed/forged proof."""
    target_name = [[0, {"$bytes": list(p.encode("ascii"))}]
                   for p in ("CommonsLibraryExample", "add_zero")]
    targets = [{"name": target_name, "export_id": COLLISION_EXPORT, "unit_id": COLLISION_UNIT}]
    directory = output/"collision-refusal"
    caught = None
    try:
        unexpected = export_api.export_module(owner, COLLISION_PARENT, targets,
            output_directory=directory, profile=profile,
            native_source=BRIDGE/"OrdinaryModule03.lean", worker_script=BRIDGE/"module_worker03.py",
            parent_deadline=allowance.deadline, make_budget=lambda: allowance.operation(A),
            account_worker_cpu=allowance.account, check_parent=allowance.check)
        report["unexpected_collision_success"] = unexpected
    except export_api.ModuleExportError as error:
        caught = error.report
        report["collision_failure"] = caught
    need(caught is not None and caught["phase"] == "NATIVE_MODULE" and
         caught["error"] == "MODULE_EXPORT_NATIVE_NOT_CLEAN" and
         caught["native_cpu_seconds"] is not None and
         caught["conservative_cpu_reservation_charged"] == 0 and
         caught["new_catalog_acceptance"] is False, "MODULE_CHECK_EXPECTED_COLLISION_FAILURE")
    supervision = json.loads(read(directory/"SUPERVISION.json", MIB))
    final = supervision.get("final_job")
    need(supervision.get("status") == "COMMAND_FAILED" and supervision.get("child_exit_code") == 1 and
         supervision.get("direct_child_reaped") is True and supervision.get("job_closed") is True and
         supervision.get("cleanup_errors") == [] and supervision.get("termination_requested") is False and
         type(final) is dict and final.get("active_processes") == 0 and
         final.get("terminated_processes") == 0 and type(final.get("total_processes")) is int and
         final["total_processes"] >= 1 and final.get("cpu_seconds") == caught["native_cpu_seconds"],
         "MODULE_CHECK_COLLISION_TREE_CLOSURE")
    need(read(directory/"supervision/stdout.txt", MIB) == b"" and
         read(directory/"supervision/stderr.txt", MIB).splitlines() ==
             [b"ORDINARY_EXTENSION OVERWRITE_OR_DUPLICATE"], "MODULE_CHECK_EXACT_COLLISION_REASON")
    need(not list(ordinary(directory/"modules", directory=True).iterdir()) and
         not os.path.lexists(directory/"native-report.json") and not os.path.lexists(directory/"MODULE.json") and
         json.loads(read(directory/"FAILURE.json", MIB)) == caught,
         "MODULE_CHECK_COLLISION_BEFORE_WRITER")
    allowance.check()
    return {"status": "EXPECTED_INIT_COLLISION_REFUSED_BEFORE_WRITING", "source_root": COLLISION_PARENT,
            "native_cpu_seconds": caught["native_cpu_seconds"], "supervision": supervision}


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize and Path(sys.executable) == PYTHON, "MODULE_CHECK_PYTHON")
    if sys.argv[1:2] == ["--consumer-child"]:
        return consumer_child(sys.argv[2:])
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("package", "profile-sha256", "bridge-pins", "bridge-pins-sha256", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    package, output = Path(args.package), Path(args.output)
    ordinary(package, directory=True); ordinary(output, directory=True)
    need(package.is_relative_to(LOCAL) and output.is_relative_to(LOCAL) and
         all(not output.is_relative_to(p) and not p.is_relative_to(output) for p in (OLD, package)),
         "MODULE_CHECK_DISJOINT_OUTPUT")
    need(BRIDGE == output/"sources/software/v5/ordinary_module_bridge" and
         Path(__file__).name == "native_check03.py", "MODULE_CHECK_SELECTED_SNAPSHOT_LOCATION")
    allowance, owner, custody, preserved = Allowance(), None, None, None
    report = {"status": "FAILED", "phase": "SUPPORT", "module_export": None,
              "new_catalog_acceptance": False, "close_errors": [],
              "claim": "SELECTED_EXISTING_OWNER_TO_NORMAL_LEAN_MODULE_NOT_GENERAL_LIBRARY_OR_GROWTH"}
    try:
        allowance.check()
        profile_raw = read(package/"PROFILE.json", 2*MIB)
        need(args.profile_sha256 == PROFILE and sha(profile_raw) == PROFILE, "MODULE_CHECK_PROFILE_PIN")
        descriptor = json.loads(profile_raw)
        cli = load_exact(package/"owner.py", "_module_check_owner", descriptor["files"]["owner.py"])
        loader = cli.bootstrap(package, PROFILE, allowance.check)
        loaded = loader.load(package, PROFILE,
            {"python_runtime": PYTHON.parent, "lean_runtime": LEAN}, allowance.deadline,
            check_parent=allowance.check)
        A, G, O, installation = loaded.A, loaded.G, loaded.O, loaded.installation
        bridge_raw = read(Path(args.bridge_pins), 65536)
        need(sha(bridge_raw) == args.bridge_pins_sha256, "MODULE_CHECK_BRIDGE_SELECTION_PIN")
        pins = A.E.strict_json(bridge_raw, A.E.Limits(max_bytes=65536))
        need(type(pins) is dict and set(pins) == set(SOURCES), "MODULE_CHECK_BRIDGE_SOURCE_SET")
        extra = []
        for filename in SOURCES:
            raw = read(BRIDGE/filename, 2*MIB)
            need(pins[filename] == {"bytes": len(raw), "sha256": sha(raw)}, "MODULE_CHECK_BRIDGE_SOURCE_PIN")
            extra.append((BRIDGE/filename, len(raw), sha(raw)))
        load_exact(BRIDGE/"module_closure.py", "module_closure", pins["module_closure.py"])
        export_api = load_exact(BRIDGE/"module_export.py", "module_export", pins["module_export.py"])
        need(export_api.A is A and export_api.G is G, "MODULE_CHECK_SHARED_CORE")
        profile = replace(loaded.profile, file_pins=loaded.profile.file_pins+tuple(extra))
        profile.verify(allowance.check)
        previous_raw = read(OLD/"RECIPROCAL-RESULT.json", 2*MIB)
        need(sha(previous_raw) == PREVIOUS_SHA and json.loads(previous_raw)["B_contributed"] == PARENT,
             "MODULE_CHECK_PRIOR_BRANCH")
        preserved = retained_map(); save(output/"PRESERVED-BEFORE.json", preserved)
        marker = A.E.strict_json(read(OLD/"B-catalog/ADOPTION.json", 65536), A.E.Limits(max_bytes=65536))
        A.P.fields(marker, ("schema", "store_id", "implementation", "limits"), "MODULE_CHECK_ADOPTION_FIELDS")
        need(marker["schema"] == A.P.SCHEMA and marker["store_id"] == STORE and
             marker["implementation"] == installation.doc["implementation"], "MODULE_CHECK_ADOPTION")
        custody_limits = A._writer_json(read(OLD/"B-custody-limits.json", 65536), 65536)
        target_name = [[0, {"$bytes": list(p.encode("ascii"))}]
                       for p in ("CommonsPeerExample", "applyFour_eq")]
        targets = [{"name": target_name, "export_id": EXPORT, "unit_id": UNIT}]
        report["phase"] = "OPEN_EXISTING_OWNER"
        custody = O.OrdinaryStore(OLD/"B-custody", installation.semantic_id, custody_limits, create=False)
        owner = A.OrdinaryAdmission.open(installation, OLD/"B-catalog", STORE, custody,
            create=False, limits=A.P.Limits(**marker["limits"]))
        report["phase"] = "EXPORT_MODULE"
        result = export_api.export_module(owner, PARENT, targets, output_directory=output/"export",
            profile=profile, native_source=BRIDGE/"OrdinaryModule03.lean", worker_script=BRIDGE/"module_worker03.py",
            parent_deadline=allowance.deadline, make_budget=lambda: allowance.operation(A),
            account_worker_cpu=allowance.account, check_parent=allowance.check)
        # Preserve real partial success before subsequent assertions/consumer.
        report["module_export"] = result
        need(result["status"] == "CHECKED_PROOF_COMPLETE_LOCAL_MODULE" and
             result["source_context_root"] == PARENT and result["targets"] == targets and
             result["new_catalog_acceptance"] is False, "MODULE_CHECK_EXPORT_RESULT")
        report["phase"] = "NORMAL_CONSUMER"
        report["normal_consumer"] = normal_consumer(loaded, result, output, allowance, report)
        report["phase"] = "INIT_COLLISION_REFUSAL"
        report["collision_refusal"] = collision_refusal(export_api, owner, profile, output, allowance, A, report)
        for filename, pin in result["artifact_parts"].items():
            raw = read(output/"export/modules"/filename, 64*MIB)
            need(pin == {"bytes": len(raw), "sha256": sha(raw)}, "MODULE_CHECK_EXPORTED_ARTIFACT_CHANGED")
        profile.verify(allowance.check)
        need(read(package/"PROFILE.json", 2*MIB) == profile_raw and
             read(Path(args.bridge_pins), 65536) == bridge_raw, "MODULE_CHECK_SELECTED_INPUT_CHANGED")
        allowance.check()
        report.update(status="PASS_EXISTING_OWNER_NORMAL_MODULE_REUSE", phase="COMPLETE")
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error))
        if hasattr(error, "report"):
            report["operation_failure"] = error.report
    finally:
        for label, resource in (("owner", owner), ("custody", custody)):
            if resource is not None:
                try:
                    resource.close()
                except BaseException as error:
                    report["close_errors"].append({"resource": label, "error": str(error)})
                    report["status"] = "FAILED"
        if preserved is not None:
            try:
                after = retained_map(); save(output/"PRESERVED-AFTER.json", after)
                need(after == preserved, "MODULE_CHECK_PRIOR_BRANCH_ARTIFACTS_CHANGED")
                report["prior_branch_artifacts_preserved"] = True
            except BaseException as error:
                report.update(status="FAILED", preservation_error=str(error))
        report.update(wall_seconds=time.monotonic()-START_WALL,
            controller_cpu_seconds=time.process_time()-START_CPU,
            charged_worker_cpu_seconds=allowance.charged_worker_cpu,
            cost_scope="Parent allocation is original. Outer Job aggregate is authoritative; do not double-count child receipts.")
        if report["wall_seconds"] >= 150 or report["controller_cpu_seconds"]+allowance.charged_worker_cpu >= 90:
            report.update(status="FAILED", budget_error="MODULE_CHECK_ORIGINAL_ALLOWANCE")
        save(output/"MODULE-NATIVE-RESULT.json", report)
        print(json.dumps({"status": report["status"], "phase": report["phase"]}), flush=True)
    return 0 if report["status"] == "PASS_EXISTING_OWNER_NORMAL_MODULE_REUSE" else 1


if __name__ == "__main__":
    raise SystemExit(main())


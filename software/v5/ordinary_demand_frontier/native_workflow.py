"""Three real frontier outcomes sharing one tiny fresh ordinary owner.

Source-only until root selects the exact package, sources and finite outer Job.
No network, old state, retry, migration or replacement acceptance machinery.
"""
from pathlib import Path
from types import SimpleNamespace
import argparse
import hashlib
import importlib.util
import json
import math
import os
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
PYTHON = Path(r"D:\Python314\python.exe")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
INSTALLATION = "9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27"
IMPLEMENTATION = "86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea"
PARTS = (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")
MIB = 1024**2
ALT_SOURCE = b"module\npublic import Init\npublic section\n@[expose] def Base.c : Nat := Nat.succ Nat.zero\n"


def need(ok, code):
    if not ok:
        raise ValueError("FRONTIER_NATIVE_" + code)


def name(text):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in text.split(".")]


def load(path, module_name, pin):
    raw = path.read_bytes()
    need({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()} == pin and
         module_name not in sys.modules, "LOADED_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


class Allowance:
    def __init__(self, wall, cpu, parent=None):
        self.started, self.cpu_started = time.monotonic(), time.process_time()
        self.deadline, self.cpu, self.charged, self.parent = self.started + wall, cpu, 0.0, parent
        if parent is not None:
            self.deadline = min(self.deadline, parent.deadline)

    def check(self):
        if self.parent is not None:
            self.parent.check()
        need(time.monotonic() < self.deadline and
             time.process_time() - self.cpu_started + self.charged < self.cpu, "ORIGINAL_ALLOWANCE")

    def account(self, value):
        need(type(value) in (int, float) and math.isfinite(value) and value >= 0, "CPU_OBSERVATION")
        self.charged += value
        if self.parent is not None:
            self.parent.account(value)

    def operation(self, A):
        self.check()
        wall = math.floor(self.deadline - time.monotonic()) - 3
        cpu = math.floor(self.cpu - (time.process_time() - self.cpu_started) - self.charged) - 1
        if self.parent is not None:
            cpu = min(cpu, math.floor(self.parent.cpu - self.parent.charged -
                                     (time.process_time() - self.parent.cpu_started)) - 1)
        need(wall >= 30 and cpu >= 2, "REMAINING_OPERATION_ALLOWANCE")
        budget = A.OperationBudget(wall, cpu, 1536, active_processes=4, output_bytes=32*MIB)
        budget.deadline = min(budget.deadline, self.deadline)
        return budget


def closed(report, success):
    final = report.get("final_job")
    need(report.get("status") == ("COMMAND_EXITED_ZERO_AND_CLOSED" if success else "COMMAND_FAILED") and
         (report.get("child_exit_code") == 0 if success else
          type(report.get("child_exit_code")) is int and report["child_exit_code"] != 0) and
         report.get("direct_child_reaped") is True and report.get("job_closed") is True and
         report.get("cleanup_errors") == [] and report.get("termination_requested") is False and
         type(final) is dict and final.get("active_processes") == 0 and
         final.get("terminated_processes") == 0 and "error" not in report,
         "NATIVE_CLOSURE_OR_UNEXPECTED_FAILURE")


def compile_alternate(args):
    need(len(args) == 2 and os.name == "nt" and Path.cwd() == ROOT and
         sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize and Path(sys.executable).resolve() == PYTHON, "ALTERNATE_PROCESS")
    source, objects = map(Path, args)
    need(source.is_relative_to(LOCAL) and objects.is_relative_to(source.parent) and
         source.name == "AlternateBase.lean" and objects.name == "lean-lib" and
         source.read_bytes() == ALT_SOURCE and objects.is_dir() and not any(objects.iterdir()),
         "ALTERNATE_FIXED_INPUTS")
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON", "ELAN")) and key.upper() != "PATH"}
    env["PATH"] = os.pathsep.join((str(PYTHON.parent), str(LEAN / "bin")))
    env["LEAN_PATH"] = str(LEAN / "lib/lean")
    return subprocess.call([str(LEAN / "bin/lean.exe"), "-DElab.async=false", "-R", str(source.parent),
        "-o", str(objects / "AlternateBase.olean"), str(source)], cwd=ROOT, env=env,
        stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)


def expression(packet):
    """Small diagnostic projection of already checked/bound fixture syntax only."""
    need(type(packet) is list and len(packet) == 4 and packet[0] == "DMKN_LEAN_ORIGINAL_EXPR_V1" and
         type(packet[2]) is list and 0 < len(packet[2]) <= 64, "TINY_EXPRESSION")
    nodes = []
    for row in packet[2]:
        if row[0] == 2 and len(row) == 3:
            parts = row[1]
            need(parts and all(part[0] == 0 for part in parts), "TINY_CONSTANT")
            nodes.append(("const", ".".join(bytes(part[1]["$bytes"]).decode("ascii") for part in parts)))
        else:
            need(row[0] == 3 and len(row) == 3 and
                 all(type(i) is int and 0 <= i < len(nodes) for i in row[1:]), "TINY_APPLICATION")
            nodes.append(("app", nodes[row[1]], nodes[row[2]]))
    need(packet[3] == len(nodes) - 1, "TINY_EXPRESSION_ROOT")
    return nodes[-1]


def constant(text):
    return ("const", text)


def app(fn, arg):
    return ("app", fn, arg)


def numeral(value):
    term = constant("Nat.zero")
    for _ in range(value):
        term = app(constant("Nat.succ"), term)
    return term


def theorem_shape(unit, output_name, right):
    descriptor = unit[1]
    need(unit[0] == "DMKN_LEAN_ORDINARY_UNIT_V1" and descriptor[0] == 1 and
         descriptor[1] == name(output_name) and descriptor[2] == [] and len(unit[2]) == 1,
         "EXACT_THEOREM_DESCRIPTOR")
    expected = app(app(app(constant("Eq"), constant("Nat")), constant("Above.d")), numeral(right))
    need(expression(descriptor[3]) == expected, "EXACT_THEOREM_STATEMENT")
    proof = expression(descriptor[4])
    need(proof[0] == "app" and proof[1] == app(constant("Eq.refl"), constant("Nat")),
         "EXACT_REFLEXIVITY_PROOF")
    return {"statement": f"Above.d = {right}", "proof_head": "Eq.refl",
            "proof_witness": proof[2], "actual_parent_value_of_Above_d": 1,
            "false_under_actual_parent": right != 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "profile-sha256", "output"):
        parser.add_argument("--" + key, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and Path(sys.executable).resolve() == PYTHON,
         "CANONICAL_PROCESS")
    source = Path(__file__).resolve().parent
    need(source.is_relative_to(LOCAL) and
         source.parts[-4:] == ("sources", "software", "v5", "ordinary_demand_frontier"), "SOURCE_SNAPSHOT")
    utility = source.parent / "ordinary_fair_search/assemble.py"
    raw = utility.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == HELPER_SHA, "FILE_UTILITY_PIN")
    H = load(utility, "_frontier_native_files", {"bytes": len(raw), "sha256": HELPER_SHA})
    allowance = Allowance(360, 220)
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    package = H.ordinary(Path(args.package), directory=True)
    need(output == source.parents[3] / "workflow" and package.is_relative_to(LOCAL) and
         not output.is_relative_to(package) and not package.is_relative_to(output), "SELECTED_PATHS")
    profile, profile_pin = H.read_json(package / "PROFILE.json", H.hexid(args.profile_sha256), allowance.check)
    owner_cli = load(package / "owner.py", "_frontier_native_owner", profile["files"]["owner.py"])
    loader = owner_cli.bootstrap(package, args.profile_sha256, allowance.check)
    loaded = loader.load(package, args.profile_sha256,
        {"python_runtime": PYTHON.parent, "lean_runtime": LEAN}, allowance.deadline,
        check_parent=allowance.check)
    A, G, O, installation = loaded.A, loaded.G, loaded.O, loaded.installation
    need(installation.manifest_sha256 == INSTALLATION and installation.implementation_id == IMPLEMENTATION,
         "UNCHANGED_RECEIVER")
    output.mkdir()

    def save(path, value):
        H.fresh_bytes(path, value if type(value) is bytes else H.canonical(value))

    def read_json(path):
        return json.loads(A.C.read_bounded(path, 2*MIB))

    def calls():
        entries = list(owner.calls.iterdir())
        need(len(entries) <= 8 and all(H.ordinary(path, directory=True) for path in entries), "CALL_CENSUS")
        return set(entries)

    def inventory():
        return owner_cli.status(owner, custody,
            SimpleNamespace(limit=16, after_root="", context_root=None), allowance.check)["roots"]

    report = {"status": "FAILED", "phase": "INITIALIZE", "cases": [], "setup": [],
              "profile_sha256": args.profile_sha256, "implementation_id": IMPLEMENTATION}
    owner = custody = None
    try:
        custody_limits = {"objects": 32, "exports": 32, "logical_bytes": 8*MIB, "db_pages": 512}
        catalog_limits = A.P.Limits(max_roots=8, max_operations=8, max_names=1024,
            max_manifest_bytes=2*MIB, max_artifact_bytes=32*MIB, max_total_artifact_bytes=256*MIB,
            max_db_pages=1024, max_batch_bytes=4*MIB, max_batch_units=32)
        save(output / "LIMITS.json", {"custody": custody_limits, "catalog": vars(catalog_limits),
            "whole_wall_seconds": 360, "whole_cpu_seconds": 220, "native_memory_mib": 1536})
        custody = O.OrdinaryStore(output / "custody", installation.semantic_id, custody_limits, create=True)
        owner = A.OrdinaryAdmission.open(installation, output / "catalog",
            H.digest(b"DMKN-FRONTIER-CONTROL\0" + str(output).encode("utf-8")), custody,
            create=True, limits=catalog_limits)
        initial = Allowance(120, 70, allowance)
        budget = initial.operation(A)
        try:
            basis = owner.initialize(budget)
        finally:
            initial.account(budget.worker_cpu)
        need(basis["status"] == "CHECKED" and basis["units_checked"] == 456, "REAL_FIXED_BASIS")
        report["basis"] = basis
        save(output / "BASIS.json", basis)

        def contribute(label, parent, acquired, body, output_name, *, backend=None, frontier=None, limit=(90, 45)):
            stage = Allowance(*limit, parent=allowance)
            directory = output / label
            save(output / (label + "-INPUTS.json"), {"parent_root": parent, "acquired": acquired,
                "source": body.decode("ascii"), "output_name": name(output_name), "frontier_root": frontier,
                "backend": None if backend is None else backend.to_document(),
                "wall_seconds": limit[0], "cpu_seconds": limit[1]})
            return G.contribute_source(owner, parent, acquired, body, [name(output_name)],
                output_directory=directory, profile=loaded.profile, parent_deadline=stage.deadline,
                make_budget=lambda: stage.operation(A), account_worker_cpu=stage.account,
                check_parent=stage.check, authoring_backend=backend, authoring_frontier_root=frontier)

        report["phase"] = "SETUP_F"
        first = contribute("setup-f", basis["local_root"], [],
            b"@[expose] def Base.c : Nat := Nat.zero\n", "Base.c")
        report["setup"].append(first)
        base = first["targets"][0]
        need(len(first["targets"]) == len(first["units"]) == 1 and base["name"] == name("Base.c"), "BASE_TARGET")
        base_unit = A.PE.read_evidence(A.C.read_bounded(Path(first["units"][0]["file"]), MIB)).document["unit"]
        need(base_unit[1][0] == 0 and base_unit[1][1] == name("Base.c") and base_unit[1][2] == [] and
             expression(base_unit[1][3]) == constant("Nat") and
             expression(base_unit[1][4]) == numeral(0), "REAL_PARENT_BASE_MEANING")
        report["phase"] = "SETUP_P"
        second = contribute("setup-p", first["local_root"], [base],
            b"def Above.d : Nat := Nat.succ Base.c\n", "Above.d")
        report["setup"].append(second)
        above = second["targets"][0]
        need(len(second["targets"]) == len(second["units"]) == 1 and above["name"] == name("Above.d"), "ABOVE_TARGET")
        above_item = A.PE.read_evidence(A.C.read_bounded(Path(second["units"][0]["file"]), MIB))
        above_unit = above_item.document["unit"]
        need(above_unit[1][0] == 0 and above_unit[1][1] == name("Above.d") and above_unit[1][2] == [] and
             expression(above_unit[1][3]) == constant("Nat") and
             expression(above_unit[1][4]) == app(constant("Nat.succ"), constant("Base.c")) and
             [name("Base.c"), base["export_id"]] in above_item.document["imports"], "REAL_PARENT_ABOVE_MEANING")
        F, P = first["local_root"], second["local_root"]
        original_parent = owner.catalog.context(P)
        positive_modules = output / "setup-f/lean-build"
        support_pins = {str(positive_modules / ("OrdinaryProducer" + suffix)):
                        H.pin(positive_modules / ("OrdinaryProducer" + suffix), allowance.check, 32*MIB)
                        for suffix in PARTS}

        report["phase"] = "ALTERNATE_FRONTEND"
        alternate = output / "alternate"
        alternate.mkdir()
        alt_objects = alternate / "lean-lib"
        alt_objects.mkdir()
        save(alternate / "AlternateBase.lean", ALT_SOURCE)
        stage = Allowance(60, 25, allowance)
        budget = stage.operation(A)
        budget.claim()
        limits = installation._supervisor.limits_checked(budget.allowance(stage.deadline))
        argv = [str(PYTHON), "-I", "-S", "-B", str(Path(__file__).resolve()), "--compile-alternate",
                str(alternate / "AlternateBase.lean"), str(alt_objects)]
        save(alternate / "COMMAND.json", {"argv": argv, "limits": limits})
        supervision = None
        try:
            supervision = installation._supervisor.supervise(argv, ROOT, alternate / "supervision",
                limits, installation._job_module.Job)
        finally:
            final = supervision.get("final_job") if type(supervision) is dict else None
            observed = final.get("cpu_seconds") if type(final) is dict else None
            stage.account(observed if type(observed) in (int, float) and math.isfinite(observed) and observed >= 0
                          else limits["cpu_seconds"])
        save(alternate / "SUPERVISION.json", supervision)
        closed(supervision, True)
        H.census(alt_objects, {"AlternateBase" + suffix for suffix in PARTS}, allowance.check)
        support_pins.update({str(alt_objects / ("AlternateBase" + suffix)):
                            H.pin(alt_objects / ("AlternateBase" + suffix), allowance.check, 32*MIB)
                            for suffix in PARTS})
        save(output / "FRONTEND-PINS.json", support_pins)

        cases = (("positive", "FrontierPositive.correct", "Nat.succ Nat.zero", positive_modules, "OrdinaryProducer"),
                 ("false-parent", "FrontierFalse.wrong", "Nat.succ (Nat.succ Nat.zero)", alt_objects, "AlternateBase"),
                 ("missing", "FrontierMissing.unreachable", "Nat.succ Nat.zero", alt_objects, "Init"))
        for label, theorem, rhs, modules, imported in cases:
            report["phase"] = label
            before_roots, before_calls = inventory(), calls()
            trace, saved_get = [], custody.get_evidence

            def traced(semantic_id, unit_id, max_bytes, *, check_budget=None):
                event = {"semantic_id": semantic_id, "unit_id": unit_id, "maximum": max_bytes}
                trace.append(event)
                need(len(trace) <= 16 and unit_id != base["unit_id"], "FORBIDDEN_FRONTIER_EVIDENCE_FETCH")
                raw = saved_get(semantic_id, unit_id, max_bytes, check_budget=check_budget)
                event.update(bytes=len(raw), sha256=H.digest(raw))
                return raw

            backend = G.TrustedProjectAuthoring.from_document({"schema": G.PROJECT_SCHEMA,
                "module_name": theorem.split(".")[0], "project_cwd": str(output),
                "project_search_paths": [str(modules)], "imports": [{"module": imported, "meta": False}]})
            body = f"theorem {theorem} : Above.d = {rhs} := rfl\n".encode("ascii")
            result, failure = None, None
            custody.get_evidence = traced
            try:
                result = contribute(label, P, [above], body, theorem, backend=backend, frontier=F,
                                    limit=(60, 25) if label == "missing" else (90, 45))
            except G.ContributionError as error:
                failure = error.report
            finally:
                custody.get_evidence = saved_get
                save(output / (label + "-FETCHES.json"), trace)
            row = {"case": label, "result": result, "failure": failure, "evidence_reads": trace}
            report["cases"].append(row)
            directory = output / label
            request = read_json(directory / "REQUEST.json")
            header = read_json(directory / "owner-request/header.json")
            need(request["parent_root"] == P and request["acquired_targets"] == [above] and
                 request["project_authoring"]["frontier_root"] == F and request["groups"] == 1 and
                 len(request["fetched"]) == 1 and request["fetched"][0]["unit_id"] == above["unit_id"] and
                 header["schema"] == "DMKN_OWNER_REQUEST_V3" and header["frontier_root"] == F and
                 header["frontier_labels"] == [[name("Base.c"), base["export_id"]]], "ACTUAL_FRONTIER_REQUEST")
            authoring = read_json(directory / "AUTHORING-SUPERVISION.json")
            authoring_log = (directory / "authoring-supervision/stdout.txt").read_bytes()
            need(authoring_log.count(b"PORTABLE_OWNER_CONSTRUCT_PHASE ENTERED_EXISTING_OWNER_ENVIRONMENT") == 1,
                 "SINGLE_AUTHORING_CONSTRUCTION")
            new_calls = calls() - before_calls
            if label == "positive":
                need(failure is None and result["admission"]["status"] == "CHECKED" and
                     result["parent_root"] == P and len(result["units"]) == 1 and len(new_calls) == 1,
                     "POSITIVE_NOT_ACCEPTED")
                closed(authoring, True)
                need(authoring_log.count(b"CONSTRUCTED_READY_FOR_AUTHORING_INSTALL") == 1 and
                     b"checkedUnits=1 " in authoring_log, "POSITIVE_DID_NOT_CONSTRUCT_RECEIVED_DEFINITION")
                item = A.PE.read_evidence(A.C.read_bounded(Path(result["units"][0]["file"]), MIB))
                need([name("Above.d"), above["export_id"]] in item.document["imports"], "POSITIVE_INTENDED_BINDING")
                row["mathematics"] = theorem_shape(item.document["unit"], theorem, 1)
                closed(read_json(next(iter(new_calls)) / "supervision-result.json"), True)
                need(len(inventory()) == len(before_roots) + 1, "POSITIVE_ROOT_COUNT")
            elif label == "false-parent":
                need(result is None and failure["phase"] == "ADMISSION" and failure["accepted"] is None and
                     failure["error"] == "ADMISSION_NATIVE_EVENT_NOT_CLEAN" and len(new_calls) == 1,
                     "SEMANTIC_NEGATIVE_INCONCLUSIVE_EARLY_REFUSAL")
                closed(authoring, True)
                need(authoring_log.count(b"CONSTRUCTED_READY_FOR_AUTHORING_INSTALL") == 1 and
                     b"checkedUnits=1 " in authoring_log, "NEGATIVE_DID_NOT_CONSTRUCT_RECEIVED_DEFINITION")
                call = next(iter(new_calls))
                closed(read_json(call / "supervision-result.json"), False)
                units = read_json(call / "units.json")
                need(len(units) == 1 and not (call / "worker-report.json").exists(), "NEGATIVE_NATIVE_INPUT")
                row["mathematics"] = theorem_shape(units[0], theorem, 2)
                diagnostic = (call / "supervision/stdout.txt").read_bytes() + (call / "supervision/stderr.txt").read_bytes()
                need(b"KERNEL_REJECTED_OR_RESOURCE_LIMIT" in diagnostic, "NEGATIVE_NOT_KERNEL_REJECTION")
                need(inventory() == before_roots, "NEGATIVE_ADDED_ROOT")
            else:
                need(result is None and failure["phase"] == "AUTHORING" and failure["accepted"] is None and
                     not new_calls and not (directory / "candidate.json").exists(), "MISSING_NOT_SINGLE_AUTHORING_FAILURE")
                closed(authoring, False)
                need(b"CONSTRUCTED_READY_FOR_AUTHORING_INSTALL" not in authoring_log,
                     "MISSING_CONSTRUCTION_UNEXPECTEDLY_COMPLETED")
                diagnostic = (directory / "authoring-supervision/stdout.txt").read_bytes() + \
                             (directory / "authoring-supervision/stderr.txt").read_bytes()
                need(b"MISSING_DEMANDED_FRONTIER_KERNEL Base.c" in diagnostic or
                     b"MISSING_DEMANDED_FRONTIER_FRONTEND Base.c" in diagnostic, "MISSING_WRONG_REFUSAL")
                need(inventory() == before_roots, "MISSING_ADDED_ROOT")
            need(owner.catalog.context(P) == original_parent, "ACCEPTED_PARENT_CHANGED")
            row["status"] = "PASS"
            save(output / (label + "-OUTCOME.json"), row)
        for path, pin in support_pins.items():
            need(H.pin(Path(path), allowance.check, 32*MIB) == pin, "APPROVED_FRONTEND_CHANGED")
        need(H.pin(package / "PROFILE.json", allowance.check) == profile_pin, "PROFILE_CHANGED")
        loaded.profile.verify(allowance.check)
        need(H.pin(package / "installation/INSTALLATION.json", allowance.check)["sha256"] == INSTALLATION,
             "INSTALLATION_CHANGED")
        for logical, pin in installation.doc["files"].items():
            need(H.pin(installation.resolve(logical), allowance.check) == pin, "RECEIVER_SUPPORT_CHANGED")
        need(len(calls()) == 5 and len(inventory()) == 4, "EXACT_FINAL_CENSUS")
        report.update(status="PASS_THREE_REAL_FRONTIER_OUTCOMES", frontier_root=F, parent_root=P,
            native_admission_calls=5, authoring_invocations=5, extra_frontend_compilations=1,
            claim="FINITE_OPTIONAL_AUTHORING_BOUNDARY_NOT_GENERAL_DEPLOYMENT_OR_GROWTH")
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
    need(report["status"] == "PASS_THREE_REAL_FRONTIER_OUTCOMES", "FINAL_OUTCOME")
    print(H.canonical(report).decode("utf-8"), flush=True)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--compile-alternate"]:
        raise SystemExit(compile_alternate(sys.argv[2:]))
    main()

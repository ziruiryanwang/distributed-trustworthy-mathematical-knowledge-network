"""Focused native-free producer CLI boundaries; doubles grant no mathematical evidence."""
from pathlib import Path
from types import SimpleNamespace as NS
import argparse
import ast
import hashlib
import importlib.util
import json
import sys
import time


def need(value, label):
    if not value:
        raise AssertionError(label)


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--source-root", required=True)
    args = parser.parse_args()
    directory = Path(args.source_root)/"software/v5/ordinary_producer_package"
    owner_path = directory/"owner.py"
    spec = importlib.util.spec_from_file_location("producer_cli_subject", owner_path)
    M = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(M)
    cases = []
    common = ["--profile-sha256", "a"*64, "--python-runtime", r"C:\runtime\python",
              "--lean-runtime", r"C:\runtime\lean", "--wall-seconds", "120",
              "--cpu-seconds", "90", "--memory-mib", "512"]
    project_raw = b'{"approved":"test double only"}'
    digest = hashlib.sha256(project_raw).hexdigest()
    producer = ["produce-baseline", *common,
                "--project-production", r"C:\approved\selection.json",
                "--project-production-sha256", digest,
                "--approve-local-project", "--spool-mib", "144",
                "--output-names", r"C:\approved\targets.json",
                "--output", r"C:\outputs\bundle"]

    def parse(argv):
        previous = sys.argv
        try:
            sys.argv = [str(owner_path), *argv]
            return M.arguments()
        finally:
            sys.argv = previous

    def record(label, check):
        check()
        cases.append(label)

    valid = parse(producer)
    record("owner_free_arguments", lambda: need(all(getattr(valid, key) is None for key in
        ("catalog", "custody", "store_id", "custody_limits", "limit", "after_root")), "owner-free parse"))
    old = parse(["status", *common, "--catalog", "catalog", "--custody", "custody",
                 "--store-id", "b"*64, "--custody-limits", "limits"])
    record("old_status_defaults", lambda: need(old.limit == 32 and old.after_root == "" and
        old.approve_local_project is False, "old defaults"))

    def no_support(*unused, **keywords):
        raise AssertionError("support must not open for invalid arguments")
    M.bootstrap = no_support
    for flag, value in (("--catalog", "catalog"), ("--parent-root", "c"*64),
                        ("--limit", "32"), ("--after-root", ""),
                        ("--source", "unapproved.lean"), ("--reference-id", "d"*64)):
        result = M.run(parse([*producer, flag, value]))
        need(result.get("phase") == "ARGUMENTS" and result.get("error") ==
             "PRODUCER_IRRELEVANT_ARGUMENT" and result["cost"]["worker_cpu_seconds"] == 0,
             "irrelevant option refused before support: "+flag)
        cases.append("reject_"+flag[2:])
    unapproved = producer.copy(); unapproved.remove("--approve-local-project")
    result = M.run(parse(unapproved))
    need(not result["ok"] and result["phase"] == "ARGUMENTS" and
         result["error"] == "PRODUCER_EXPLICIT_PROJECT_TARGETS_OUTPUT_REQUIRED", "explicit approval")
    cases.append("explicit_project_approval")
    for spool in ("143", "257"):
        selected = producer.copy(); selected[selected.index("--spool-mib")+1] = spool
        result = M.run(parse(selected))
        need(not result["ok"] and result["error"] == "PRODUCER_EXPLICIT_SPOOL_ALLOCATION", "spool bounds")
    cases.append("bounded_explicit_spool")
    for argv, expected in ((["status", *common], "OWNER_STATE_ARGUMENTS_REQUIRED"),
                           (["status", *common, "--catalog", "catalog", "--custody", "custody",
                             "--store-id", "b"*64, "--custody-limits", "limits",
                             "--approve-local-project"], "OWNER_PRODUCTION_ARGUMENTS_ONLY")):
        result = M.run(parse(argv))
        need(not result["ok"] and result["error"] == expected, expected)
    cases.append("old_operations_keep_state_and_reject_production")

    # All files/native execution/state APIs below are doubles. Their role is to
    # test CLI dispatch/charging, not to requalify the already separate producer.
    events, budgets = [], []
    class Budget:
        def __init__(self, wall, cpu, memory, *, output_bytes):
            self.deadline = time.monotonic()+wall
            self.worker_cpu = 0
            self.output_bytes = output_bytes
            self.wall, self.cpu = wall, cpu
            budgets.append(self)
    def hexid(value):
        need(len(value) == 64 and all(c in "0123456789abcdef" for c in value), "test hash")
    def read(path, maximum):
        events.append("read")
        if path == Path(valid.project_production): return project_raw
        if path == Path(valid.output_names): return b'[[[0,{"$bytes":[84]}]]]'
        raise AssertionError("unexpected file read")
    C = NS(hexid=hexid, ordinary=lambda path, **kw: Path(path), read_bounded=read)
    A = NS(C=C, sha=lambda raw: hashlib.sha256(raw).hexdigest(),
           _writer_json=lambda raw, maximum: json.loads(raw), OperationBudget=Budget)
    G, extraction, profile = object(), object(), object()
    installation = NS(implementation_id="e"*64)
    P = NS(A=A, G=G, X=extraction)
    loaded = NS(A=A, G=G, library_extraction=extraction, installation=installation,
                baseline_production=P, profile=profile)
    def load(*unused, **keywords):
        events.append("load")
        keywords["check_parent"]()
        return loaded
    M.bootstrap = lambda *unused: NS(load=load)
    def successful(inst, chosen, **kwargs):
        events.append("produce")
        need(inst is installation and chosen is profile and kwargs["project_selection_raw"] == project_raw,
             "selected exact inputs")
        need(kwargs["project_selection_sha256"] == digest and kwargs["output_directory"] == Path(valid.output),
             "selected exact output")
        need(kwargs["budget"].output_bytes == 144*1024**2 and kwargs["budget"].wall < 120 and
             kwargs["budget"].cpu < 90, "remaining envelope and spool")
        kwargs["budget"].worker_cpu = 7.25
        return {"status": "PRODUCED_INERT_BASELINE_NOT_ACCEPTED", "mathematical_acceptance": False}
    P.produce_bundle = successful
    result = M.run(valid)
    need(result["ok"] and result["mathematical_acceptance"] is False and
         result["cost"]["worker_cpu_seconds"] == 7.25 and events.count("produce") == 1,
         "success without owner APIs and exactly-once native charge")
    cases.append("single_owner_free_dispatch_and_remaining_budget")
    class Failure(Exception):
        report = {"native_accounting_complete": False, "native_cpu_charge": 11}
    def failed(inst, chosen, **kwargs):
        kwargs["budget"].worker_cpu = 11
        raise Failure("injected uncertainty, no native launched")
    P.produce_bundle = failed
    result = M.run(valid)
    need(not result["ok"] and result["cost"]["worker_cpu_seconds"] == 11 and
         result["detail"] == Failure.report and result["accepted"] is None, "failure charge")
    cases.append("unknown_accounting_retains_reservation")
    original_start = M.START_CPU
    def late(inst, chosen, **kwargs):
        value = successful(inst, chosen, **kwargs)
        M.START_CPU = time.process_time()-100
        return value
    P.produce_bundle = late
    result = M.run(valid); M.START_CPU = original_start
    need(not result["ok"] and result["production_result"]["status"] ==
         "PRODUCED_INERT_BASELINE_NOT_ACCEPTED" and result["cost"]["worker_cpu_seconds"] == 7.25,
         "late failure retains production result")
    cases.append("late_parent_failure_preserves_output_observation")
    bad = parse(producer); bad.project_production_sha256 = "0"*64
    events.clear(); result = M.run(bad)
    need(not result["ok"] and result["error"] == "PRODUCER_PROJECT_SELECTION_PIN" and
         "produce" not in events, "selection mismatch before producer")
    cases.append("project_pin_refused_before_export")

    # Exercise only the changed role resolver with path/module doubles. No file
    # or executable is loaded. Its returned root protects every package subtree.
    source_tree = ast.parse((directory/"baseline_production.py").read_bytes())
    resolver = next(node for node in source_tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == "_selected_support")
    root = Path(r"E:\producer-package")
    class Installation: manifest_sha256 = "a"*64
    class Profile:
        installation_manifest_sha256 = "a"*64
        author_worker_script = root/"author_worker.py"
        def verify(self, check): check()
    core = NS(NativeInstallation=Installation, E=object(), S=object(), PE=object(),
              need=need, C=NS(ordinary=lambda path: Path(path)))
    candidate = NS(__file__=str(root/"authoring/py/portable_candidate.py"))
    general = NS(A=core, B=candidate, AuthoringProfile=Profile,
                 __file__=str(root/"authoring/py/ordinary_contribution.py"))
    binder = NS(E=core.E, S=core.S, PE=core.PE, C=candidate,
                __file__=str(root/"reference/baseline_bundle.py"))
    extract = NS(A=core, G=general, B=candidate,
                 __file__=str(root/"authoring/py/library_extraction.py"))
    for key, filename in (("L", "library_completion"), ("R", "portable_owner_request"),
                          ("X", "supervised_library_exchange")):
        setattr(extract, key, NS(__file__=str(root/"authoring/py"/(filename+".py"))))
    controller = root/"authoring/py/baseline_production.py"
    worker = root/"authoring/py/baseline_worker.py"
    executable = root/"authoring/bin/BaselineExporter.exe"
    selected = {controller, worker, executable, *(Path(module.__file__) for module in
                (binder, extract, general, candidate, extract.L, extract.R, extract.X))}
    chosen = Profile()
    chosen.file_pins = tuple((path, 32, "b"*64) for path in selected)
    scope = {"A": core, "G": general, "B": binder, "X": extract, "Path": Path,
             "__file__": str(controller), "MIB": 1024**2, "EXECUTABLE_MAXIMUM": 32*1024**2}
    exec(compile(ast.Module(body=[resolver], type_ignores=[]), "role-resolver-test", "exec"), scope)
    resolved = scope["_selected_support"](Installation(), chosen, lambda: None)
    need(resolved[0] == worker and resolved[1] == executable and resolved[3] == root,
         "consolidated support roles and full protected root")
    need((root/"reference/new-output").is_relative_to(resolved[3]),
         "sibling subtree must be inside protected root")
    cases.append("split_roles_and_entire_package_protection")
    binder.__file__ = str(root/"authoring/py/baseline_bundle.py")
    chosen.file_pins += ((Path(binder.__file__), 32, "c"*64),)
    try:
        scope["_selected_support"](Installation(), chosen, lambda: None)
    except AssertionError as error:
        need(str(error) == "BASELINE_PRODUCTION_PACKAGE_ROLES", "exact misplaced binder refusal")
    else:
        raise AssertionError("a pinned but wrongly located binder must not be selected")
    cases.append("pinned_alternate_role_refused")

    # Structural regression checks are source assertions, not runtime validation
    # of profile/native roles; the independent source review covers those roles.
    for filename in ("owner.py", "profile.py", "baseline_production.py"):
        ast.parse((directory/filename).read_bytes(), filename)
    profile_tree = ast.parse((directory/"profile.py").read_bytes())
    assignments = {node.targets[0].id: node.value for node in profile_tree.body
                   if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)}
    need("baseline_production" in ast.literal_eval(assignments["AUTHOR"]), "producer profile role")
    cases.append("source_parse_and_profile_declaration")
    print(json.dumps({"status": "PASS_NATIVE_FREE_CLI_BOUNDARIES", "cases": cases,
        "case_count": len(cases), "native_calls": 0, "owner_state_opens": 0,
        "scope": "PARSER_DISPATCH_AND_ACCOUNTING_WITH_DOUBLES_NOT_INSTALLED_OR_MATHEMATICAL_QUALIFICATION"}), flush=True)


if __name__ == "__main__":
    main()

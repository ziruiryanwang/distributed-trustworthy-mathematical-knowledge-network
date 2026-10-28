"""Ordinary Lean-first owner with optional inert project interchange.

Approved source/project authoring, exact local module export and checked return
retain the selected preview implementation. Produce-baseline is owner-free;
intake-baseline independently admits its exact inert bundle. Neither operation
needs an original-library reference or a cryptographic certificate.

Run with the selected Python -I -S -B. The entrypoint/runtime/OS and immutable
owner-controlled support are trust premises; resource limits are not a security
sandbox. No project build, download, network operation, automatic retry, state
migration or implicit parent inference occurs. A supplied package hash selects
bytes, not a trusted publisher. Approved project plugins remain executable local
support. Exported kernel declarations do not recreate original frontend metadata.
This facade has a new exact module-anchor support identity; old anchors retain
their original supported package and are not silently migrated.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import stat
import sys

MIB = 1024**2


def need(condition, code):
    if not condition:
        raise ValueError(code)


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("init", "status", "contribute", "complete",
                                            "extract-std", "extract-project", "export-module",
                                            "intake-baseline", "produce-baseline"))
    for name in ("profile-sha256", "python-runtime", "lean-runtime"):
        parser.add_argument("--"+name, required=True)
    for name in ("catalog", "custody", "store-id", "custody-limits"):
        parser.add_argument("--"+name, help="Required for owner operations; forbidden for produce-baseline")
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+name, required=True, type=int)
    parser.add_argument("--catalog-limits", help="Optional init-only JSON; default is P.Limits()")
    parser.add_argument("--parent-root", help="Explicit local context for contribution, completion, extraction or export")
    parser.add_argument("--source", help="Owner-approved UTF-8 Lean source body")
    parser.add_argument("--acquired-targets", help="JSON exact name/export_id/unit_id records, or []")
    parser.add_argument("--module-targets", help="Export-module-only nonempty JSON exact name/export_id/unit_id records")
    parser.add_argument("--module-anchor", help="Export-module-only exact locally registered AnchorID; omitted means cold checking")
    parser.add_argument("--output-names", help="JSON list of structured Lean names")
    parser.add_argument("--output", help="Fresh contribution/completion/extraction/export output directory")
    parser.add_argument("--project-authoring", help="Contribute-only owner-approved project JSON")
    parser.add_argument("--project-authoring-sha256", help="Exact SHA-256 of project-authoring JSON")
    parser.add_argument("--authoring-frontier-root",
                        help="Contribute-only optimistic checked ancestor; requires project-authoring")
    for name in ("candidate", "supplement", "prepared-bindings"):
        parser.add_argument("--"+name, help="Complete-only explicit retained inert input file")
        parser.add_argument("--"+name+"-sha256", help="Exact SHA-256 for that completion input")
    for name in ("retained-contribution", "retained-request-sha256", "retained-candidate-sha256"):
        parser.add_argument("--"+name, help="Extraction-only exact retained contribution input")
    parser.add_argument("--library-modules", help="Extract-std-only installed module list")
    parser.add_argument("--project-extraction", help="Extract-project-only canonical local approval JSON")
    parser.add_argument("--project-extraction-sha256", help="Exact SHA-256 of local extraction selection")
    parser.add_argument("--context-root", help="Status-only exact context to validate without Lean replay")
    parser.add_argument("--after-root", help="Status-only lexicographic root cursor")
    parser.add_argument("--limit", type=int, help="Status page size, default 32, at most 256")
    for name in ("bundle-directory", "bundle-manifest", "bundle-manifest-sha256"):
        parser.add_argument("--"+name, help="Intake-baseline-only exact inert bundle input")
    parser.add_argument("--project-production", help="Produce-baseline-only approved compiled-project selection JSON")
    parser.add_argument("--project-production-sha256", help="Exact SHA-256 of the production selection JSON")
    parser.add_argument("--approve-local-project", action="store_true",
                        help="Explicit approval to load the selected local compiled project; not mathematical trust")
    parser.add_argument("--spool-mib", type=int,
                        help="Produce-baseline-only total output allowance, 144..256 MiB; not a hard disk quota")
    args = parser.parse_args()
    if args.operation != "produce-baseline":
        if args.after_root is None:
            args.after_root = ""
        if args.limit is None:
            args.limit = 32
    return args


def project_json(raw):
    """Bound owner configuration before parsing; exact fields belong to G.

    Project imports use JSON booleans, unlike inert mathematical evidence.
    Reject duplicate keys and all numeric values; no peer parser is relaxed.
    """
    need(type(raw) is bytes and 0 < len(raw) <= 65536, "OWNER_PROJECT_JSON_BOUND")
    stack, quoted, escaped = [], False, False
    for byte in raw:
        if quoted:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
        elif byte == 34:
            quoted = True
        elif byte in (91, 123):
            stack.append(byte)
            need(len(stack) <= 8, "OWNER_PROJECT_JSON_DEPTH")
        elif byte in (93, 125):
            need(stack and stack.pop() == (91 if byte == 93 else 123),
                 "OWNER_PROJECT_JSON_BRACKETS")
    need(not quoted and not escaped and not stack, "OWNER_PROJECT_JSON_UNTERMINATED")
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "OWNER_PROJECT_JSON_DUPLICATE")
            result[key] = value
        return result
    def reject(_):
        raise ValueError("OWNER_PROJECT_JSON_NUMBER")
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                          parse_int=reject, parse_float=reject, parse_constant=reject)
    except (json.JSONDecodeError, RecursionError, UnicodeError) as error:
        raise ValueError("OWNER_PROJECT_JSON_SYNTAX") from error


class Allowance:
    """Original parent allocation; worker CPU never resets between stages.

    Python controller checks are cooperative. Each native tree is contained by
    the existing Windows Job supervisor. A caller needing hard controller limits
    must supervise this process too; memory-mib is not a controller RSS cap.
    """
    def __init__(self, args):
        need(type(args.wall_seconds) is int and 35 <= args.wall_seconds <= 3600 and
             type(args.cpu_seconds) is int and 4 <= args.cpu_seconds <= 200000 and
             type(args.memory_mib) is int and 1 <= args.memory_mib <= 8192,
             "OWNER_ORIGINAL_ALLOCATION")
        self.deadline = START_WALL+args.wall_seconds
        self.cpu_seconds, self.memory_mib = args.cpu_seconds, args.memory_mib
        self.worker_cpu = 0.0

    def check(self):
        need(time.monotonic() < self.deadline and
             time.process_time()-START_CPU+self.worker_cpu < self.cpu_seconds,
             "OWNER_ORIGINAL_ALLOCATION_EXHAUSTED")

    def account(self, seconds):
        need(type(seconds) in (int, float) and math.isfinite(seconds) and seconds >= 0,
             "OWNER_WORKER_CPU_CHARGE")
        self.worker_cpu += seconds

    def operation(self, A, *, output_bytes=64*MIB):
        self.check()
        wall = math.floor(self.deadline-time.monotonic())-3
        cpu = math.floor(self.cpu_seconds-(time.process_time()-START_CPU)-self.worker_cpu)-1
        need(wall >= 30 and cpu >= 2, "OWNER_REMAINING_OPERATION_ALLOCATION")
        value = A.OperationBudget(wall, cpu, self.memory_mib, output_bytes=output_bytes)
        value.deadline = min(value.deadline, self.deadline)
        return value

    def report(self):
        return {"wall_seconds": time.monotonic()-START_WALL,
                "controller_cpu_seconds": time.process_time()-START_CPU,
                "worker_cpu_seconds": self.worker_cpu,
                "controller_limits": "COOPERATIVE_NOT_HARD_PROCESS_CONTAINMENT"}


def bootstrap(package_root, expected_hash, check):
    """Check exact selected profile.py bytes before executing that loader.

    This deliberately small stdlib bootstrap cannot establish its own trust.
    The loader then performs complete descriptor/path/census validation before
    importing any other package Python code, including installed core modules.
    """
    need(type(expected_hash) is str and len(expected_hash) == 64 and
         all(c in "0123456789abcdef" for c in expected_hash), "OWNER_PROFILE_HASH")
    def read(path, maximum):
        need(path.is_absolute() and ".." not in path.parts, "OWNER_BOOTSTRAP_PATH")
        for part in (*reversed(path.parents), path):
            info = part.lstat()
            need(not stat.S_ISLNK(info.st_mode) and not
                 (getattr(info, "st_file_attributes", 0) & 0x400), "OWNER_BOOTSTRAP_REDIRECT")
            need(stat.S_ISDIR(info.st_mode) if part != path else
                 stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "OWNER_BOOTSTRAP_FILE")
        size = path.stat().st_size
        need(0 < size <= maximum, "OWNER_BOOTSTRAP_BOUND")
        check()
        with path.open("rb") as stream:
            raw = stream.read(maximum+1)
        need(len(raw) == size, "OWNER_BOOTSTRAP_READ_CHANGED")
        return raw
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "OWNER_BOOTSTRAP_DUPLICATE")
            result[key] = value
        return result
    raw = read(package_root/"PROFILE.json", 2*MIB)
    need(hashlib.sha256(raw).hexdigest() == expected_hash, "OWNER_PROFILE_PIN")
    doc = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    need(type(doc) is dict and type(doc.get("files")) is dict, "OWNER_BOOTSTRAP_DESCRIPTOR")
    selected = {}
    for filename in ("owner.py", "profile.py"):
        pin = doc["files"].get(filename)
        need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
             type(pin["bytes"]) is int and 0 < pin["bytes"] <= 2*MIB,
             "OWNER_BOOTSTRAP_PIN")
        selected[filename] = read(package_root/filename, 2*MIB)
        need(len(selected[filename]) == pin["bytes"] and
             hashlib.sha256(selected[filename]).hexdigest() == pin["sha256"],
             "OWNER_BOOTSTRAP_CHANGED")
    path, name = package_root/"profile.py", "_dmkn_ordinary_owner_profile"
    need(name not in sys.modules, "OWNER_BOOTSTRAP_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(selected["profile.py"], str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    return module


def reject_dedicated(path):
    """Refuse this package's ordinary operations inside dedicated inert hosts.

    The permanent marker is an exclusion convention, not a sandbox against old
    executables or arbitrary same-user SDK/source code. Presence alone refuses;
    malformed markers and unexpected path errors cannot authorize access.
    """
    path = Path(path)
    need(path.is_absolute() and ".." not in path.parts and len(path.parts) <= 128,
         "OWNER_DEDICATED_PATH")
    for ancestor in (path, *path.parents):
        try:
            (ancestor/"DMKN-DEDICATED-HOST.json").lstat()
        except FileNotFoundError:
            continue
        raise ValueError("OWNER_DEDICATED_HOST_PATH")


def separated(paths, code):
    for path in paths:
        reject_dedicated(path)
    for position, left in enumerate(paths):
        for right in paths[position+1:]:
            need(not left.is_relative_to(right) and not right.is_relative_to(left), code)


def status(owner, custody, args, check):
    """Bounded inventory under owner lock, plus optional exact context check.

    Ordinary owner open may mark abandoned RESERVED operations INTERRUPTED.
    Accordingly this command is not advertised as a read-only database open.
    Inventory IDs alone are not transferable mathematical warrants.
    """
    A = sys.modules["ordinary_admission"]
    A.P.uint(args.limit, 1, 256, "OWNER_STATUS_LIMIT")
    if args.after_root:
        A.C.hexid(args.after_root)
    check()
    rows = owner.catalog._db.execute(
        "SELECT id,parent FROM roots WHERE id>? ORDER BY id LIMIT ?",
        (args.after_root, args.limit+1)).fetchall()
    more, selected = len(rows) > args.limit, rows[:args.limit]
    result = {"status": "LOCAL_OWNER_OPEN", "basis_root_identity": owner.catalog.basis_root,
              "roots": [{"local_root": identity, "parent_root": parent or ""}
                        for identity, parent in selected],
              "has_more": more, "next_after_root": selected[-1][0] if more else None,
              "custody": custody.status(), "selected_context": None,
              "claim": "LOCAL_STORED_ROOT_INVENTORY_NOT_PEER_WARRANT"}
    if args.context_root is not None:
        A.C.hexid(args.context_root)
        context = owner.catalog.context(args.context_root)
        result["selected_context"] = {key: context[key] for key in (
            "local_root", "basis_root", "semantic_id", "foundation_id", "implementation_id")}
        result["selected_context"].update(names=len(context["bindings"]),
            modules=len(context["modules"]),
            artifact_bytes=sum(row["artifact_bytes"] for row in context["modules"]))
    check()
    return result


def validate_producer_arguments(args):
    """Reject state and unrelated operations' arguments before support loading."""
    allowed = {"operation", "profile_sha256", "python_runtime", "lean_runtime",
               "wall_seconds", "cpu_seconds", "memory_mib", "project_production",
               "project_production_sha256", "approve_local_project", "spool_mib",
               "output_names", "output"}
    need(args.operation == "produce-baseline" and
         all(value is None for key, value in vars(args).items() if key not in allowed),
         "PRODUCER_IRRELEVANT_ARGUMENT")
    need(args.approve_local_project is True and all(value is not None for value in
         (args.project_production, args.project_production_sha256, args.output_names, args.output)),
         "PRODUCER_EXPLICIT_PROJECT_TARGETS_OUTPUT_REQUIRED")
    # Default producer bounds reserve 64 MiB writer + 64 MiB evidence +
    # 2 MiB manifest + 12 MiB metadata + two 1 MiB logs. No implicit increase.
    need(type(args.spool_mib) is int and 144 <= args.spool_mib <= 256,
         "PRODUCER_EXPLICIT_SPOOL_ALLOCATION")


def run_producer(args):
    """One approved-local export; never open or fabricate mathematical state."""
    allocation = Allowance(args)
    phase, result, budget = "ARGUMENTS", None, None
    report = None
    try:
        validate_producer_arguments(args)
        allocation.check()
        phase = "SUPPORT"
        root = Path(__file__).absolute().parent
        loader = bootstrap(root, args.profile_sha256, allocation.check)
        loaded = loader.load(root, args.profile_sha256,
            {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
            allocation.deadline, check_parent=allocation.check)
        A, G, installation = loaded.A, loaded.G, loaded.installation
        producer = loaded.baseline_production
        need(producer.A is A and producer.G is G and producer.X is loaded.library_extraction,
             "PRODUCER_SHARED_SUPPORT")
        phase = "INPUTS"
        allocation.check()
        A.C.hexid(args.project_production_sha256)
        project_raw = A.C.read_bounded(A.C.ordinary(Path(args.project_production)), MIB)
        need(A.sha(project_raw) == args.project_production_sha256, "PRODUCER_PROJECT_SELECTION_PIN")
        targets = A._writer_json(A.C.read_bounded(
            A.C.ordinary(Path(args.output_names)), MIB), MIB)
        output = A.C.ordinary(Path(args.output), directory=True, fresh=True)
        reject_dedicated(output)
        phase = "PRODUCE_BASELINE"
        budget = allocation.operation(A, output_bytes=args.spool_mib*MIB)
        try:
            result = producer.produce_bundle(installation, loaded.profile,
                project_selection_raw=project_raw,
                project_selection_sha256=args.project_production_sha256,
                targets=targets, output_directory=output, budget=budget)
        finally:
            # The controller retains the entire native reservation when actual
            # accounting is unknown. Charge exactly once, also on failure.
            allocation.account(budget.worker_cpu)
        allocation.check()
        report = {"ok": True, "operation": args.operation, "result": result,
                  "profile_sha256": args.profile_sha256,
                  "implementation_id": installation.implementation_id,
                  "mathematical_acceptance": False,
                  "acquisition_fit": "NOT_ESTABLISHED_RECEIVER_RELATIVE"}
    except BaseException as error:
        report = {"ok": False, "operation": args.operation, "phase": phase,
                  "error_type": type(error).__name__, "error": str(error),
                  "accepted": None, "mathematical_acceptance": False,
                  "retention": "PRESERVE_ALL_OUTPUTS_NO_AUTOMATIC_RETRY"}
        if hasattr(error, "report"):
            report["detail"] = error.report
        if result is not None:
            # Late parent-budget/reporting failure cannot erase complete bytes.
            report["production_result"] = result
    finally:
        report["cost"] = allocation.report()
        report["project_production_selection"] = {
            "file": args.project_production, "sha256": args.project_production_sha256,
            "approval_requested": args.approve_local_project}
    return report


def run(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "OWNER_PYTHON_PROFILE")
    if args.operation == "produce-baseline":
        return run_producer(args)
    allocation = Allowance(args)
    owner = custody = None
    accepted, module_result, report, phase = None, None, None, "SUPPORT"
    intake_accounting = None
    try:
        need(all(value is not None for value in
             (args.catalog, args.custody, args.store_id, args.custody_limits)),
             "OWNER_STATE_ARGUMENTS_REQUIRED")
        need(args.project_production is None and args.project_production_sha256 is None and
             args.approve_local_project is False and args.spool_mib is None,
             "OWNER_PRODUCTION_ARGUMENTS_ONLY")
        root = Path(__file__).absolute().parent
        loader = bootstrap(root, args.profile_sha256, allocation.check)
        loaded = loader.load(root, args.profile_sha256,
            {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
            allocation.deadline, check_parent=allocation.check)
        A, G, O, installation = loaded.A, loaded.G, loaded.O, loaded.installation
        A.C.hexid(args.store_id)
        create = args.operation == "init"
        external_output = args.operation in ("contribute", "complete", "extract-std", "extract-project", "export-module")
        baseline_intake = args.operation == "intake-baseline"
        need((args.parent_root is not None) == (external_output or baseline_intake) and
             (args.output is not None) == external_output, "OWNER_OPERATION_ARGUMENTS")
        bundle_args = (args.bundle_directory, args.bundle_manifest, args.bundle_manifest_sha256)
        need(all(value is not None for value in bundle_args) if baseline_intake
             else all(value is None for value in bundle_args), "OWNER_BASELINE_ARGUMENTS")
        need((args.output_names is not None) == (args.operation in ("contribute", "complete")),
             "OWNER_OUTPUT_NAME_ARGUMENT")
        contribution_args = (args.source, args.acquired_targets)
        need(all(value is not None for value in contribution_args) if args.operation == "contribute"
             else all(value is None for value in contribution_args), "OWNER_CONTRIBUTION_ARGUMENTS")
        need((args.module_targets is not None) == (args.operation == "export-module"),
             "OWNER_MODULE_EXPORT_ARGUMENTS")
        need(args.module_anchor is None or args.operation == "export-module",
             "OWNER_MODULE_ANCHOR_ARGUMENT")
        if args.module_anchor is not None:
            A.C.hexid(args.module_anchor)
        completion_args = (args.candidate, args.candidate_sha256, args.supplement,
                           args.supplement_sha256, args.prepared_bindings, args.prepared_bindings_sha256)
        need(all(value is not None for value in completion_args) if args.operation == "complete"
             else all(value is None for value in completion_args), "OWNER_COMPLETION_ARGUMENTS")
        extraction_args = (args.retained_contribution, args.retained_request_sha256,
                           args.retained_candidate_sha256)
        need(all(value is not None for value in extraction_args)
             if args.operation in ("extract-std", "extract-project")
             else all(value is None for value in extraction_args), "OWNER_EXTRACTION_ARGUMENTS")
        need((args.library_modules is not None) == (args.operation == "extract-std"),
             "OWNER_EXTRACTION_STD_MODULES_ONLY")
        extraction_project_args = (args.project_extraction, args.project_extraction_sha256)
        need(all(value is not None for value in extraction_project_args)
             if args.operation == "extract-project"
             else all(value is None for value in extraction_project_args),
             "OWNER_EXTRACTION_PROJECT_ARGUMENTS")
        project_args = (args.project_authoring, args.project_authoring_sha256)
        need(all(value is None for value in project_args) or
             (args.operation == "contribute" and all(value is not None for value in project_args)),
             "OWNER_PROJECT_AUTHORING_ARGUMENTS")
        need(args.authoring_frontier_root is None or
             (args.operation == "contribute" and all(value is not None for value in project_args)),
             "OWNER_FRONTIER_REQUIRES_PROJECT_CONTRIBUTION")
        authoring_options = {}
        if args.authoring_frontier_root is not None:
            A.C.hexid(args.authoring_frontier_root)
            authoring_options["authoring_frontier_root"] = args.authoring_frontier_root
        need(args.catalog_limits is None or create, "OWNER_INIT_LIMITS_ONLY")
        need(args.operation == "status" or
             (args.context_root is None and args.after_root == "" and args.limit == 32),
             "OWNER_STATUS_ARGUMENTS_ONLY")
        if args.operation == "status":
            A.P.uint(args.limit, 1, 256, "OWNER_STATUS_LIMIT")
            if args.after_root:
                A.C.hexid(args.after_root)
            if args.context_root is not None:
                A.C.hexid(args.context_root)
        catalog_path = A.C.ordinary(Path(args.catalog), directory=True, fresh=create)
        custody_path = A.C.ordinary(Path(args.custody), directory=True, fresh=create)
        protected = [root, *installation.runtime_roots.values()]
        separated([catalog_path, custody_path, *protected], "OWNER_STATE_SUPPORT_OVERLAP")
        custody_limits = A._writer_json(A.C.read_bounded(Path(args.custody_limits), 65536), 65536)
        A.P.fields(custody_limits, O.STORE_LIMITS, "OWNER_CUSTODY_LIMITS")
        for key, bounds in O.STORE_LIMITS.items():
            A.P.uint(custody_limits[key], *bounds, "OWNER_CUSTODY_LIMIT:"+key)
        if create:
            limits = A.P.Limits() if args.catalog_limits is None else A.P.Limits(
                **A._writer_json(A.C.read_bounded(Path(args.catalog_limits), 65536), 65536))
        else:
            marker = A.E.strict_json(A.C.read_bounded(catalog_path/"ADOPTION.json", 65536),
                                    A.E.Limits(max_bytes=65536))
            A.P.fields(marker, ("schema", "store_id", "implementation", "limits"), "OWNER_ADOPTION_FIELDS")
            need(marker["schema"] == A.P.SCHEMA and marker["store_id"] == args.store_id and
                 marker["implementation"] == installation.doc["implementation"], "OWNER_ADOPTION_BINDING")
            limits = A.P.Limits(**marker["limits"])
        if external_output:
            A.C.hexid(args.parent_root)
            output = A.C.ordinary(Path(args.output), directory=True, fresh=True)
            separated([output, catalog_path, custody_path, *protected], "OWNER_OUTPUT_STATE_SUPPORT_OVERLAP")
        if baseline_intake:
            A.C.hexid(args.parent_root)
            bundle_directory = A.C.ordinary(Path(args.bundle_directory), directory=True)
            A.C.hexid(args.bundle_manifest_sha256)
            manifest_raw = A.C.read_bounded(A.C.ordinary(Path(args.bundle_manifest)), 2*MIB)
            need(A.sha(manifest_raw) == args.bundle_manifest_sha256, "OWNER_REFERENCE_BUNDLE_PIN")
        if args.operation == "export-module":
            module_targets = G._acquired(installation.semantic_id, A._writer_json(
                A.C.read_bounded(A.C.ordinary(Path(args.module_targets)), 65536), 65536))
            need(bool(module_targets), "OWNER_MODULE_EXPORT_TARGETS_EMPTY")
        if args.operation in ("extract-std", "extract-project"):
            retained = A.C.ordinary(Path(args.retained_contribution), directory=True)
            separated([output, retained], "OWNER_EXTRACTION_OUTPUT_INPUT_OVERLAP")
            for filename, digest, maximum in (("REQUEST.json", args.retained_request_sha256, MIB),
                    ("candidate.json", args.retained_candidate_sha256, 4*MIB)):
                allocation.check()
                A.C.hexid(digest)
                raw = A.C.read_bounded(A.C.ordinary(retained/filename), maximum)
                need(hashlib.sha256(raw).hexdigest() == digest, "OWNER_EXTRACTION_INPUT_PIN")
            extraction_options = {}
            if args.operation == "extract-std":
                extraction_options["modules"] = loaded.library_extraction.selected_modules(A._writer_json(
                    A.C.read_bounded(A.C.ordinary(Path(args.library_modules)), 65536), 65536))
            else:
                # This is an explicit local controller choice, never a path or
                # approval token supplied by an inert candidate or a peer.
                A.C.hexid(args.project_extraction_sha256)
                project_raw = A.C.read_bounded(A.C.ordinary(Path(args.project_extraction)), MIB)
                need(hashlib.sha256(project_raw).hexdigest() == args.project_extraction_sha256,
                     "OWNER_EXTRACTION_PROJECT_PIN")
                extraction_options.update(project_selection_raw=project_raw,
                    project_selection_sha256=args.project_extraction_sha256)
        if args.operation == "complete":
            def selected_input(path, digest, maximum):
                allocation.check()
                A.C.hexid(digest)
                raw = A.C.read_bounded(A.C.ordinary(Path(path)), maximum)
                need(hashlib.sha256(raw).hexdigest() == digest, "OWNER_COMPLETION_INPUT_PIN")
                return raw
            candidate_raw = selected_input(args.candidate, args.candidate_sha256, 4*MIB)
            supplement_raw = selected_input(args.supplement, args.supplement_sha256, 4*MIB)
            need(len(candidate_raw)+len(supplement_raw) <= 4*MIB, "OWNER_COMPLETION_INPUT_BYTES")
            rows = A._writer_json(selected_input(args.prepared_bindings,
                args.prepared_bindings_sha256, MIB), MIB)
            A.E._array(rows, maximum=4096)
            prepared_bindings = {}
            for row in rows:
                name, identity = A.E._array(row, 2)
                key = A.E.name_key(name)
                A.E._hex(identity)
                need(key not in prepared_bindings, "OWNER_COMPLETION_DUPLICATE_PREPARED_NAME")
                prepared_bindings[key] = identity
            names = G._outputs(A._writer_json(A.C.read_bounded(Path(args.output_names), 65536), 65536))
        if args.operation == "contribute":
            body = A.C.read_bounded(Path(args.source), MIB)
            acquired = A._writer_json(A.C.read_bounded(Path(args.acquired_targets), 65536), 65536)
            names = A._writer_json(A.C.read_bounded(Path(args.output_names), 65536), 65536)
            G.validate_inputs(installation.semantic_id, acquired, body, names)
            if args.project_authoring is not None:
                A.C.hexid(args.project_authoring_sha256)
                raw = A.C.read_bounded(Path(args.project_authoring), 65536)
                need(hashlib.sha256(raw).hexdigest() == args.project_authoring_sha256,
                     "OWNER_PROJECT_AUTHORING_PIN")
                backend = G.TrustedProjectAuthoring.from_document(project_json(raw))
                backend.verify(allocation.check)
                authoring_options["authoring_backend"] = backend
        allocation.check()
        phase = "OPEN_OWNER"
        custody = O.OrdinaryStore(custody_path, installation.semantic_id, custody_limits, create=create)
        owner = A.OrdinaryAdmission.open(installation, catalog_path, args.store_id,
                                       custody, create=create, limits=limits)
        allocation.check()
        if create:
            phase = "INITIALIZE"
            budget = allocation.operation(A)
            try:
                accepted = owner.initialize(budget)
            finally:
                allocation.account(budget.worker_cpu)
            result = {"status": "INITIALIZED_LOCAL_OWNER", "basis": accepted}
        elif args.operation == "status":
            phase = "STATUS"
            result = status(owner, custody, args, allocation.check)
        elif args.operation == "intake-baseline":
            phase = "INTAKE_BASELINE"
            I = loaded.baseline_intake
            need(I.A is A and I.O is O, "OWNER_BASELINE_SHARED_CORE")
            allocation.check()
            wall = math.floor(allocation.deadline-time.monotonic())-3
            cpu = math.floor(allocation.cpu_seconds-(time.process_time()-START_CPU)-allocation.worker_cpu)-1
            need(wall >= 35 and cpu >= 4, "OWNER_BASELINE_REMAINING_BUDGET")
            budget = I.IntakeBudget(wall, cpu, allocation.memory_mib)
            budget.deadline = min(budget.deadline, allocation.deadline)
            try:
                result = I.intake(owner, args.parent_root, bundle_directory, manifest_raw,
                                  args.bundle_manifest_sha256, budget=budget)
                accepted = {"local_root": result["local_root"], "status": result["status"]}
            finally:
                allocation.account(budget.observed_worker_cpu)
                intake_accounting = {"observed_worker_cpu_seconds": budget.observed_worker_cpu,
                    "reserved_cpu_seconds": budget.reserved_cpu,
                    "scope": "PARTIAL_CORE_OBSERVATION_NOT_COMPLETE_MEASURED_CPU"}
        elif args.operation == "export-module":
            phase = "EXPORT_MODULE"
            need(loaded.module_export.A is A and loaded.module_export.G is G,
                 "OWNER_MODULE_EXPORT_SHARED_CORE")
            module_result = loaded.module_export.export_module(owner, args.parent_root,
                module_targets, output_directory=output, profile=loaded.profile,
                native_source=root/"module/OrdinaryModule.lean",
                worker_script=root/"module_worker.py", parent_deadline=allocation.deadline,
                make_budget=lambda: allocation.operation(A),
                account_worker_cpu=allocation.account, check_parent=allocation.check,
                module_anchor=args.module_anchor or "")
            # Local export success is retained even if later reporting/closure fails.
            # Runtime identity describes this export, not an unspecified consumer project.
            result = dict(module_result,
                manifest_path=str(output/"MODULE.json"), supported_runtime={
                    "installation_manifest_sha256": installation.manifest_sha256,
                    "implementation_id": installation.implementation_id,
                    "lean_runtime": str(installation.runtime_roots["lean_runtime"]),
                    "lean_executable": str(installation.path("lean")),
                    "lean_executable_pin": dict(installation.doc["files"][installation.doc["roles"]["lean"]]),
                    "claim": "EXACT_SELECTED_LOCAL_RUNTIME_NOT_DOWNSTREAM_PROJECT_VALIDATION"})
        elif args.operation in ("extract-std", "extract-project"):
            phase = "EXTRACT_STD" if args.operation == "extract-std" else "EXTRACT_PROJECT"
            need(loaded.library_extraction.A is A, "OWNER_EXTRACTION_SHARED_CORE")
            result = loaded.library_extraction.extract_retained(owner, args.parent_root, retained,
                request_sha256=args.retained_request_sha256,
                candidate_sha256=args.retained_candidate_sha256,
                exporter=root/"authoring/bin/MissingImportExporter.exe", profile=loaded.profile,
                output_directory=output, parent_deadline=allocation.deadline,
                make_budget=lambda: allocation.operation(A),
                account_worker_cpu=allocation.account, check_parent=allocation.check,
                **extraction_options)
        elif args.operation == "complete":
            phase = "COMPLETE"
            need(loaded.completion_api.A is A, "OWNER_COMPLETION_SHARED_CORE")
            result = loaded.completion_api.complete_source(owner, args.parent_root,
                candidate_raw, supplement_raw, expected_targets=names,
                prepared_bindings=prepared_bindings, output_directory=output,
                parent_deadline=allocation.deadline,
                make_budget=lambda: allocation.operation(A),
                account_worker_cpu=allocation.account, check_parent=allocation.check)
            accepted = result["admission"]
        else:
            phase = "CONTRIBUTE"
            result = G.contribute_source(owner, args.parent_root, acquired, body, names,
                output_directory=output, profile=loaded.profile,
                parent_deadline=allocation.deadline,
                make_budget=lambda: allocation.operation(A),
                account_worker_cpu=allocation.account, check_parent=allocation.check,
                **authoring_options)
            accepted = result["admission"]
        allocation.check()
        report = {"ok": True, "operation": args.operation, "result": result,
                  "catalog": str(catalog_path), "custody": str(custody_path),
                  "store_id": args.store_id, "profile_sha256": args.profile_sha256,
                  "implementation_id": installation.implementation_id,
                  "catalog_limits": vars(limits), "custody_limits": custody_limits}
    except BaseException as error:
        report = {"ok": False, "operation": args.operation, "phase": phase,
                  "error_type": type(error).__name__, "error": str(error),
                  "accepted": accepted,
                  "retention": "EXISTING_ACCEPTED_STATE_AND_ALL_PARTIAL_OUTPUTS_PRESERVED_NO_RETRY"}
        if module_result is not None:
            report["module_export"] = module_result
        if hasattr(error, "report"):
            # In particular preserve contribution acceptance even when the
            # subsequent preview/result logging failed. Do not infer rollback.
            report["detail"] = error.report
            report["accepted"] = error.report.get("accepted", accepted)
    finally:
        failures = []
        for name, value in (("owner", owner), ("custody", custody)):
            if value is not None:
                try:
                    value.close()
                except BaseException as error:
                    failures.append({"component": name, "error_type": type(error).__name__, "error": str(error)})
        if failures:
            report["close_errors"] = failures
            report["ok"] = False
        if args.project_authoring is not None:
            # Selection metadata is not proof that configuration or admission passed.
            report["project_authoring_selection"] = {"file": args.project_authoring,
                "sha256": args.project_authoring_sha256}
            if args.authoring_frontier_root is not None:
                report["project_authoring_selection"]["frontier_root"] = args.authoring_frontier_root
        if args.project_extraction is not None:
            # Selection metadata records intent to use these local bytes; it
            # is not a claim that validation, extraction or admission succeeded.
            report["project_extraction_selection"] = {"file": args.project_extraction,
                "sha256": args.project_extraction_sha256}
        report["cost"] = allocation.report()
        if intake_accounting is not None:
            report["cost"]["baseline_intake_accounting"] = intake_accounting
            report["cost"]["worker_cpu_scope"] = "PARTIAL_CORE_OBSERVATION_NOT_COMPLETE_MEASURED_CPU"
    return report


if __name__ == "__main__":
    result = run(arguments())
    print(json.dumps(result, sort_keys=True, ensure_ascii=True, allow_nan=False), flush=True)
    raise SystemExit(0 if result["ok"] else 1)

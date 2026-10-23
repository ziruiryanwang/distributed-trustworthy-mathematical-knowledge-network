"""Persistent local ordinary owner: init, status, contribute.

Run with the selected Python -I -S -B. This entrypoint, runtime and local OS are
owner-trusted. A supplied package hash selects bytes; it does not authenticate
an unknown publisher. No network operation, source sandbox, automatic retry,
state copying, parent inference or cryptographic proof production occurs here.
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
    parser.add_argument("operation", choices=("init", "status", "contribute"))
    for name in ("profile-sha256", "python-runtime", "lean-runtime", "catalog", "custody",
                 "store-id", "custody-limits"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+name, required=True, type=int)
    parser.add_argument("--catalog-limits", help="Optional init-only JSON; default is P.Limits()")
    parser.add_argument("--parent-root", help="Explicit local parent, required for contribute")
    parser.add_argument("--source", help="Owner-approved UTF-8 Lean source body")
    parser.add_argument("--acquired-targets", help="JSON exact name/export_id/unit_id records, or []")
    parser.add_argument("--output-names", help="JSON list of structured Lean names")
    parser.add_argument("--output", help="Fresh contribution output directory")
    parser.add_argument("--context-root", help="Status-only exact context to validate without Lean replay")
    parser.add_argument("--after-root", default="", help="Status-only lexicographic root cursor")
    parser.add_argument("--limit", type=int, default=32, help="Status page size, at most 256")
    return parser.parse_args()


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

    def operation(self, A):
        self.check()
        wall = math.floor(self.deadline-time.monotonic())-3
        cpu = math.floor(self.cpu_seconds-(time.process_time()-START_CPU)-self.worker_cpu)-1
        need(wall >= 30 and cpu >= 2, "OWNER_REMAINING_OPERATION_ALLOCATION")
        value = A.OperationBudget(wall, cpu, self.memory_mib, output_bytes=64*MIB)
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


def separated(paths, code):
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


def run(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "OWNER_PYTHON_PROFILE")
    allocation = Allowance(args)
    owner = custody = None
    accepted, report, phase = None, None, "SUPPORT"
    try:
        root = Path(__file__).absolute().parent
        loader = bootstrap(root, args.profile_sha256, allocation.check)
        loaded = loader.load(root, args.profile_sha256,
            {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
            allocation.deadline, check_parent=allocation.check)
        A, G, O, installation = loaded.A, loaded.G, loaded.O, loaded.installation
        A.C.hexid(args.store_id)
        create = args.operation == "init"
        contribution_args = (args.parent_root, args.source, args.acquired_targets,
                             args.output_names, args.output)
        need(all(value is not None for value in contribution_args) if args.operation == "contribute"
             else all(value is None for value in contribution_args), "OWNER_OPERATION_ARGUMENTS")
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
        if args.operation == "contribute":
            A.C.hexid(args.parent_root)
            output = A.C.ordinary(Path(args.output), directory=True, fresh=True)
            separated([output, catalog_path, custody_path, *protected], "OWNER_OUTPUT_STATE_SUPPORT_OVERLAP")
            body = A.C.read_bounded(Path(args.source), MIB)
            acquired = A._writer_json(A.C.read_bounded(Path(args.acquired_targets), 65536), 65536)
            names = A._writer_json(A.C.read_bounded(Path(args.output_names), 65536), 65536)
            G.validate_inputs(installation.semantic_id, acquired, body, names)
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
        else:
            phase = "CONTRIBUTE"
            result = G.contribute_source(owner, args.parent_root, acquired, body, names,
                output_directory=output, profile=loaded.profile,
                parent_deadline=allocation.deadline,
                make_budget=lambda: allocation.operation(A),
                account_worker_cpu=allocation.account, check_parent=allocation.check)
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
        report["cost"] = allocation.report()
    return report


if __name__ == "__main__":
    result = run(arguments())
    print(json.dumps(result, sort_keys=True, ensure_ascii=True, allow_nan=False), flush=True)
    raise SystemExit(0 if result["ok"] else 1)

"""New baseline boundary controls: real syntax/planning, inert owner and storage.

No owner/catalog/SQLite/native/network operation is performed. Retained small
evidence is read as syntax only. The accepted contexts, commit results, custody
rows and input filesystem below are explicit test doubles, never warrants.
The selected current package supplies unchanged parsers and planner. Only the
new baseline modules come from the runner's immutable source snapshot.
"""
from pathlib import Path
import argparse
from contextlib import ExitStack
from copy import deepcopy
from dataclasses import replace
import hashlib
import importlib.util
import json
import os
import socket
import sqlite3
import subprocess
import sys
import time
from types import SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PROFILE = "ab04e72440bcd09381a81d4b721d1103fa2e62bc260fa6c0434e6c568419016f"
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()
FIXTURES = (
    ("ordinary-package-lifecycle-continuation-01/contribution/evidence/"
     "25ae588e95228a64196a576aa9c9dd78249c23b0c26189c5671a434b93afa1b3.json",
     "c7266a3047afcf59059b7884853b4d6b9be4244509f260e78dd072973f9704aa"),
    ("ordinary-package-lifecycle-continuation-01/contribution/evidence/"
     "c4639e6e5f70e259ea1611adba8e168aa74dbfb91f98e2512cd465f82705e61e.json",
     "88c8b3b9da6bfd39fff9c827a1bec8b51ce4289c949c9d7507bfad5e53bc421f"),
    ("ordinary-peer-reciprocal-02/B-contribution/evidence/"
     "d52aed3d1d0f94b8ee2236a7ee84435c983c9523dca0f100f4369c183c3d4e51.json",
     "d0bb18c957c41f3f15d0b47b4eda2f41b8c1f72107d5065929625228a63558ae"),
)


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU < 25,
         "BASELINE_CONTROLS_ORIGINAL_ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def module(name, path, expected=None):
    with path.open("rb") as stream:
        data = stream.read(2*MIB+1)
    need(len(data) <= 2*MIB and (expected is None or sha(data) == expected),
         "BASELINE_CONTROL_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    exec(compile(data, str(path), "exec"), value.__dict__)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--package", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "BASELINE_CONTROL_PROCESS")
    package, output = Path(args.package), Path(args.output)
    need(output.is_absolute() and output.resolve().is_relative_to(LOCAL) and
         output.parent.is_dir() and not os.path.lexists(output), "BASELINE_CONTROL_OUTPUT")
    profile_raw = (package/"PROFILE.json").read_bytes()
    need(sha(profile_raw) == PROFILE, "BASELINE_CONTROL_PROFILE")
    profile = json.loads(profile_raw)
    base = module("_baseline_control_owner", package/"owner.py",
                  profile["files"]["owner.py"]["sha256"])
    loader = base.bootstrap(package, PROFILE, check)
    loaded = loader.load(package, PROFILE, {"python_runtime": Path(r"D:\Python314"),
        "lean_runtime": ROOT/"software/runtime/lean-4.34.0-windows"},
        START+45, check_parent=check)
    source = Path(__file__).resolve().parent
    B = module("baseline_bundle", source/"baseline_bundle.py")
    I = module("_baseline_controls_intake", source/"baseline_intake.py")
    A, O = I.A, I.O
    need(A is loaded.A and O is loaded.O and I.B is B and B.E is A.E and B.PE is A.PE,
         "BASELINE_CONTROL_SHARED_HELPERS")
    inventory_raw = loaded.installation.read("inventory", MIB)
    inventory = A._writer_json(inventory_raw, MIB)
    fixed = {A.E.name_key(row[0]): A.S.basis_symbol_id(A.S.semantic_id(),
             A.S.foundation_id(), row[0]) for row in inventory}
    raws = []
    for relative, expected in FIXTURES:
        with (LOCAL/relative).open("rb") as stream:
            raw = stream.read(MIB+1)
        need(len(raw) <= MIB and sha(raw) == expected, "BASELINE_CONTROL_FIXTURE_PIN")
        raws.append(raw)
    raws = tuple(raws)
    items = tuple(A.PE.read_evidence(raw) for raw in raws)
    units = [item.document["unit"] for item in items]
    target = units[-1][2][0][0]
    writer = {"schema": B.WRITER_SCHEMA, "assurance": B.WRITER_ASSURANCE,
        "targets": [target], "basis_names": [row[0] for row in inventory],
        "units": units, "stats": {"source_records": 584, "selected_units": 3,
            "dependency_edges": sum(len(item.document["imports"]) for item in items),
            "scan_nodes": sum(item.census.total_nodes for item in items),
            "unit_json_bytes": sum(len(A.E.canonical_json(unit)) for unit in units)}}
    cases, forbidden_calls = [], []

    def forbidden(*_, **__):
        forbidden_calls.append("FORBIDDEN")
        raise AssertionError("BASELINE_CONTROL_FORBIDDEN_EXTERNAL_OPERATION")

    def reject(label, action, code):
        check()
        try:
            action()
        except ValueError as error:
            need(code in str(error), "BASELINE_CONTROL_WRONG_REFUSAL:"+label+":"+str(error))
        else:
            raise AssertionError("BASELINE_CONTROL_MISSING_REFUSAL:"+label)
        cases.append({"case": label, "expected_refusal": code})

    def bind(doc=writer, *, inv=inventory_raw, targets=None, limits=B.Limits()):
        return B.bind_writer(encoded(doc), inv, [target] if targets is None else targets,
                             limits=limits, check_budget=check)

    class Result:
        def __init__(self, row):
            self.row = row
        def fetchone(self):
            return self.row

    class FakeDB:
        """Recognize only the exact read-only SQL statements under test."""
        def __init__(self, held, locators):
            self.held, self.locators = held, locators
            self.queries = []
        def execute(self, sql, values=()):
            self.queries.append(sql)
            if sql == "SELECT count(*) FROM roots":
                return Result((1,))
            if sql == "SELECT count(*),COALESCE(sum(reserved_bytes),0) FROM operations":
                return Result((1, 1024))
            if sql == "SELECT COALESCE(sum(reserved_bytes),0) FROM imports":
                return Result((0,))
            if sql == "SELECT length(raw),raw_sha256 FROM objects WHERE kind='evidence' AND identity=?":
                value = self.held.get(values[0])
                return Result(None if value is None else (len(value), sha(value)))
            if sql == "SELECT unit_id,locator FROM exports WHERE export_id=?":
                return Result(self.locators.get(values[0]))
            raise AssertionError("BASELINE_CONTROL_UNEXPECTED_SQL:"+sql)

    def intake_case(label, batches, *, existing=(), parent="a"*64, failure=None,
                    fail_at=None, changed_on_second=None, bundle_limits=None,
                    catalog_limits=None, custody_limits=None, cpu=100,
                    calls=None, expected_calls=0, expected_statuses=None):
        check()
        bundle_limits = bundle_limits or B.Limits()
        manifest = B.make_manifest(batches)
        virtual = output/"not-created"/label
        directory = virtual/"bundle"
        files = {directory/entry.relative_path: raw for batch, entries in zip(batches, manifest.batches)
                 for raw, entry in zip(batch, entries)}
        reads, events, children = {}, [], []
        bindings, held, locators = dict(fixed), {}, {}
        store = O.OrdinaryStore.__new__(O.OrdinaryStore)
        store.semantic_id, store.root = A.S.semantic_id(), virtual/"custody"
        store.limits = {"objects": 1000, "exports": 1000, "logical_bytes": 8*MIB,
                        "db_pages": 256} if custody_limits is None else custody_limits
        for raw in existing:
            item = A.PE.read_evidence(raw)
            held[item.unit_id] = raw
            for row in item.document["unit"][2]:
                bindings[A.E.name_key(row[0])] = A.S.export_id(store.semantic_id, item.unit_id, row[0])
            for export, locator in store._export_locators(item, check):
                locators[export] = (item.unit_id, locator)
        store.db = FakeDB(held, locators)
        store.status = lambda: {"semantic_id": store.semantic_id,
            "counts": {"objects": len(held), "exports": len(locators),
                       "logical_bytes": sum(len(raw) for raw in held.values())},
            "mathematical_acceptance": False}
        store.get_evidence = lambda semantic, identity, maximum, check_budget: held[identity]
        basis_module = A.C.module_name(parent)
        contexts = {parent: {"local_root": parent, "semantic_id": store.semantic_id,
            "bindings": bindings, "basis_module": basis_module, "root_module": basis_module,
            "modules": [{"module_name": basis_module, "parent_module": [],
                "path": str(virtual/"catalog/operations"/("f"*64)/"chunk.olean"),
                "artifact_bytes": 1024, "names_count": len(bindings)}]}}
        catalog = NS(_grant=None, _limits=catalog_limits or A.P.Limits(),
            _db=FakeDB({}, {}), _active=check,
            context=lambda root: deepcopy(contexts[root]))
        owner = A.OrdinaryAdmission.__new__(A.OrdinaryAdmission)
        owner.catalog, owner.evidence_store, owner.directory = catalog, store, virtual/"catalog"
        owner.installation = NS(semantic_id=store.semantic_id, root=virtual/"support",
                               runtime_roots={"runtime": virtual/"runtime"})

        def preflight(root, supplied, *, budget):
            events.append(("preflight", root))
            children.append(budget)
            return A._plan(catalog.context(root), supplied, A.PreflightLimits(), budget.check)

        def admit(root, plan, child):
            events.append(("admit", root))
            child.claim()
            actual = A._plan(catalog.context(root), plan.raw_units, A.PreflightLimits(), child.check)
            need(actual.status == "READY", "BASELINE_CONTROL_DOUBLE_READY")
            count = sum(event[0] == "admit" for event in events)
            new_root = root if not actual.ordered_units else sha((root+str(count)).encode("ascii"))
            current = catalog.context(root)
            current["local_root"] = new_root
            for raw in actual.ordered_units:
                item = A.PE.read_evidence(raw)
                for row in item.document["unit"][2]:
                    current["bindings"][A.E.name_key(row[0])] = A.S.export_id(
                        store.semantic_id, item.unit_id, row[0])
            contexts[new_root] = current
            if count == fail_at:
                # Deliberately simulate durable change followed by lost response.
                # The wrapper must not call it rollback or retry the operation.
                raise ValueError("CATALOG_TRANSACTION_UNCERTAIN_REOPEN_REQUIRED")
            return {"status": "CHECKED" if actual.ordered_units else "REUSED",
                    "local_root": new_root, "units_checked": len(actual.ordered_units)}

        owner.preflight, owner.admit = preflight, admit

        def read_bounded(path, maximum):
            need(path in files, "BASELINE_CONTROL_UNSELECTED_READ")
            reads[path] = reads.get(path, 0)+1
            value = files[path]
            if changed_on_second is not None and path.name == changed_on_second+".json" and reads[path] > 1:
                value = value[:-1]+b"!"
            need(len(value) <= maximum, "BASELINE_CONTROL_READ_BOUND")
            return value

        budget = I.IntakeBudget(40, cpu, 64, active_processes=2)
        chosen_calls = calls or I.CallLimits(cpu_seconds=2, output_bytes=MIB)
        with patch.object(A.C, "ordinary", lambda path, **kw: Path(path)), \
                patch.object(A.C, "read_bounded", read_bounded):
            try:
                result = I.intake(owner, parent, directory, manifest.raw, manifest.sha256,
                                  budget=budget, limits=bundle_limits, calls=chosen_calls)
                need(failure is None, "BASELINE_CONTROL_EXPECTED_STOP:"+label)
            except I.IntakeError as error:
                result = error.report
                need(failure is not None and failure in result["error"],
                     "BASELINE_CONTROL_WRONG_STOP:"+label+":"+str(result))
        actual_calls = sum(event[0] == "admit" for event in events)
        need(actual_calls == expected_calls and all(child.deadline <= budget.deadline for child in children),
             "BASELINE_CONTROL_CALL_COUNT_OR_DEADLINE:"+label)
        need(result["ordinary_library_registered"] is False, "BASELINE_CONTROL_NO_REFERENCE_AUTHORITY")
        need(result["resources"]["worker_cpu_accounting"] ==
             "PARTIAL_CORE_OBSERVATION_NO_COMPLETENESS_CLAIM",
             "BASELINE_CONTROL_PARTIAL_CPU_OBSERVATION_LABEL")
        if expected_statuses is not None:
            need([row["status"] for row in result["batches"]] == expected_statuses,
                 "BASELINE_CONTROL_PREFIX_STATUS:"+label)
        if failure is None:
            expected_rows = [[row[0], A.S.export_id(store.semantic_id, item.unit_id, row[0])]
                for batch in batches for raw in batch for item in (A.PE.read_evidence(raw),)
                for row in item.document["unit"][2]]
            need(result["planning"]["census"]["binding_bytes"] == len(encoded(expected_rows)),
                 "BASELINE_CONTROL_EXACT_AGGREGATE_BINDING_BYTES")
        if fail_at is not None:
            need(result["possible_unreported_commit"] is True and len(result["batches"]) == fail_at-1 and
                 result["last_confirmed_root"] == result["batches"][-1]["local_root"] and
                 budget.reserved_cpu == fail_at*chosen_calls.cpu_seconds,
                 "BASELINE_CONTROL_UNCERTAIN_PREFIX_AND_FULL_RESERVATION")
        if changed_on_second is not None:
            need(result["possible_unreported_commit"] is False and len(result["batches"]) == 1 and
                 result["last_confirmed_root"] == result["batches"][0]["local_root"],
                 "BASELINE_CONTROL_CHANGED_BYTES_PRESERVE_PREFIX")
        cases.append({"case": label, "result": result, "actual_admit_calls": actual_calls,
                      "authority": "INERT_OWNER_DOUBLE_NOT_MATHEMATICAL_ACCEPTANCE"})
        return budget

    with ExitStack() as stack:
        for obj, attribute in ((sqlite3, "connect"), (subprocess, "Popen"), (socket, "socket"),
                (A.OrdinaryAdmission, "open"), (A.OrdinaryAdmission, "_execute"),
                (A.P.PortableCatalog, "open"), (A.P.PortableCatalog, "_commit_checked"),
                (O.OrdinaryStore, "__init__"), (O.OrdinaryStore, "put_evidence")):
            stack.enter_context(patch.object(obj, attribute, forbidden))
        bound = bind(limits=B.Limits(max_batch_units=1))
        need(tuple(raw for batch in bound.batches for raw in batch) == raws and
             len(bound.batches) == 3 and bound.targets[0].unit_id == items[-1].unit_id and
             bound.targets[0].export_id == A.S.export_id(A.S.semantic_id(), items[-1].unit_id, target) and
             bound.mathematical_acceptance is False and bound.manifest.mathematical_acceptance is False,
             "BASELINE_CONTROL_EXACT_V2_BIND_AND_WHOLE_UNIT_SPLIT")
        cases.append({"case": "exact-fixed-seed-v2-bind-and-whole-unit-split", "units": 3})
        reject("wrong-fixed-inventory", lambda: bind(inv=inventory_raw+b" "), "BASELINE_FIXED_INVENTORY_PIN")
        reject("basis-target-not-fabricated", lambda: bind(targets=[inventory[0][0]]), "BASELINE_TARGET_ALREADY_IN_BASIS")
        altered = deepcopy(writer); altered["units"] = [units[1], units[0], units[2]]
        reject("producer-forward-reference", lambda: bind(altered), "BASELINE_UNBOUND_OR_FORWARD_REFERENCE")
        altered = deepcopy(writer); altered["stats"]["unit_json_bytes"] += 1
        reject("writer-byte-census", lambda: bind(altered), "BASELINE_WRITER_BYTE_CENSUS_OR_TARGET_OUTPUT")
        altered = deepcopy(writer); altered["targets"] = [units[0][2][0][0]]
        reject("writer-target-selection", lambda: bind(altered), "BASELINE_WRITER_BASIS_OR_TARGETS")
        reject("aggregate-bind-count", lambda: bind(limits=B.Limits(max_units=2)), "ARRAY_BOUND")
        manifest = B.make_manifest(((raws[0],), raws[1:]))
        reject("manifest-pin", lambda: B.read_manifest(manifest.raw, "0"*64), "BASELINE_MANIFEST_HASH")
        altered = json.loads(manifest.raw); altered["batches"][1].append(deepcopy(altered["batches"][0][0]))
        reject("duplicate-across-batches", lambda: B.read_manifest(encoded(altered), sha(encoded(altered))),
               "BASELINE_DUPLICATE_UNIT")
        altered = json.loads(manifest.raw); altered["batches"][0][0]["path"] = "../input"
        reject("manifest-path-not-authority", lambda: B.read_manifest(encoded(altered), sha(encoded(altered))),
               "BASELINE_ENTRY_FIELDS")
        entry = manifest.batches[0][0]
        reject("entry-unit-identity", lambda: B.validate_batch((B.Entry("0"*64, entry.raw_sha256,
            entry.raw_bytes),), (raws[0],)), "BASELINE_EVIDENCE_IDENTITY")
        linked = ((raws[0],), raws[1:])
        successful = intake_case("dependency-linked-two-batch", linked, expected_calls=2,
                                  expected_statuses=["CHECKED", "CHECKED"])
        reject("intake-budget-not-renewable", successful.claim, "BASELINE_BUDGET_ALREADY_USED")
        intake_case("forward-batch-before-any-admit", (raws[1:], (raws[0],)),
                    failure="BASELINE_FORWARD_OR_MISSING_DEPENDENCY")
        broken = json.loads(raws[1]); broken["imports"][0][1] = "f"*64
        intake_case("late-batch-conflict-before-any-admit", ((raws[0],), (encoded(broken),)),
                    failure="ADMISSION_PARENT_IMPORT_CONFLICT")
        intake_case("all-exact-reuse", linked, existing=raws, expected_calls=2,
                    expected_statuses=["REUSED", "REUSED"])
        intake_case("all-reused-no-new-artifact-reservation", linked, existing=raws,
                    catalog_limits=replace(A.P.Limits(), max_artifact_bytes=2048),
                    expected_calls=2, expected_statuses=["REUSED", "REUSED"])
        intake_case("compatible-independent-root-plus-new-unit", (raws[:2], (raws[2],)),
                    existing=raws[:2], parent="d"*64, expected_calls=2,
                    expected_statuses=["REUSED", "CHECKED"])
        intake_case("root-capacity-before-any-admit", linked,
                    catalog_limits=replace(A.P.Limits(), max_roots=2), failure="BASELINE_CATALOG_CAPACITY")
        intake_case("custody-locator-overhead-before-any-admit", linked,
                    custody_limits={"objects": 1000, "exports": 1000,
                        "logical_bytes": sum(map(len, raws)), "db_pages": 256},
                    failure="BASELINE_CUSTODY_CAPACITY")
        intake_case("aggregate-cpu-before-any-admit", linked, cpu=4,
                    failure="BASELINE_AGGREGATE_CPU_RESERVATION")
        intake_case("spool-reservation-before-any-admit", linked,
                    calls=I.CallLimits(cpu_seconds=2, output_bytes=MIB, max_spool_bytes=MIB),
                    failure="BASELINE_SPOOL_RESERVATION")
        intake_case("changed-second-batch-preserves-confirmed-prefix", linked,
                    changed_on_second=items[1].unit_id, expected_calls=1,
                    failure="BASELINE_EVIDENCE_EXACT_BYTES", expected_statuses=["CHECKED"])
        intake_case("lost-second-response-no-retry-or-rollback", linked, fail_at=2,
                    expected_calls=2, failure="CATALOG_TRANSACTION_UNCERTAIN_REOPEN_REQUIRED",
                    expected_statuses=["CHECKED"])
        need(not forbidden_calls, "BASELINE_CONTROL_NO_FORBIDDEN_SIDE_EFFECT")
    check()
    report = {"status": "PASS_REAL_BASELINE_SYNTAX_AND_PLANNING_INERT_OWNER", "cases": cases,
        "case_count": len(cases), "forbidden_calls": forbidden_calls,
        "profile_sha256": PROFILE, "mathematical_acceptance": False,
        "state": "NO_REAL_OWNER_DATABASE_NATIVE_OR_NETWORK_OPERATION",
        "wall_seconds": time.monotonic()-START, "controller_cpu_seconds": time.process_time()-CPU}
    data = encoded(report)
    need(len(data) <= MIB, "BASELINE_CONTROL_OUTPUT_BOUND")
    output.mkdir()
    with (output/"RESULT.json").open("xb") as stream:
        stream.write(data)
    print(json.dumps({"status": report["status"], "case_count": len(cases)}), flush=True)


if __name__ == "__main__":
    main()

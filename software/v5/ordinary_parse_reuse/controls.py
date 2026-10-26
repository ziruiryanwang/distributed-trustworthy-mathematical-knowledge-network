"""Focused parse-reuse controls; all catalog/custody/native events are doubles.

Real strict parsers, planners, admission control flow and native-input projection
are compared with the pinned predecessor. No database, native, network or actual
mathematical acceptance occurs. Only one fresh small report is written.
"""
from pathlib import Path
import argparse
from collections import Counter
from contextlib import ExitStack
from copy import deepcopy
from dataclasses import asdict, fields, replace
import gc
import hashlib
import importlib.util
import json
import os
import socket
import sqlite3
import subprocess
import sys
import time
from types import ModuleType, SimpleNamespace as NS
from unittest.mock import patch
import weakref

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
PACKAGE = LOCAL / "current-release-build01/distribution/package"
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()
PINS = {
    "installation/py/ordinary_evidence.py": "fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6",
    "installation/py/ordinary_semantics.py": "ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915",
    "installation/py/portable_evidence.py": "f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8",
    "installation/py/local_catalog.py": "860a9d731290b2a7fbacd4852bb68185516329ee42845648f4ba3c3856d7c751",
    "installation/py/portable_catalog.py": "aeaf0c7d507baa6b63d401c432ca71557bf29b6b576b1f6cd8381e4e87c7473e",
    "installation/py/ordinary_admission.py": "9653a710a089393d189830a26aa8dd0723ee75859ce577d9713dae569b5e8575",
    "authoring/py/portable_candidate.py": "29ae111a362472b09b2b1ff16b567b352be793d76c2cd1b5421e0aee29219331",
    "reference/baseline_bundle.py": "e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6",
    "reference/baseline_intake.py": "b5a17aa580f8d9cfdeaaded7d93c2b12ad6e19e5018bf5e7c087cb56760069d8",
}
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
        raise AssertionError("PARSE_REUSE_CONTROL_" + code)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU < 30, "FINITE_ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def source(name, path, expected=None):
    raw = path.read_bytes()
    need(len(raw) <= 2*MIB and (expected is None or sha(raw) == expected), "SOURCE_PIN:"+str(path))
    module = importlib.util.module_from_spec(importlib.util.spec_from_file_location(name, path))
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


class Reads:
    def __init__(self, reader):
        self.reader, self.counts, self.refs, self.peak = reader, Counter(), [], 0

    def live(self):
        return sum(reference() is not None for reference in self.refs)

    def __call__(self, raw, *args, **kwargs):
        item = self.reader(raw, *args, **kwargs)
        self.counts[raw] += 1
        self.refs.append(weakref.ref(item))
        self.peak = max(self.peak, self.live())
        return item

    def released(self):
        gc.collect()
        need(self.live() == 0, "PARSED_VALUE_ESCAPED")


class StoreDouble:
    """No SQLite; one real strict read models the unchanged put boundary."""
    def put_evidence(self, raw, *, before_commit):
        before_commit()
        # The caller's current _stage parse is the only expected live Evidence.
        if self.observer is not None:
            need(self.observer.live() == 1, "PRIVATE_PARSE_REACHED_STAGE_CALLBACK")
        if self.fail_put:
            raise ValueError("DOUBLE_CUSTODY_FAILURE")
        item = self.PE.read_evidence(raw)
        self.held[item.unit_id] = raw
        return {"semantic_id": self.semantic_id, "identity": item.unit_id,
                "raw_sha256": sha(raw), "raw_bytes": len(raw), "mathematical_acceptance": False}

    def get_evidence(self, semantic, identity, maximum, *, check_budget):
        check_budget()
        value = self.held[identity]
        need(semantic == self.semantic_id and len(value) <= maximum, "DOUBLE_READBACK")
        return value

    def _export_locators(self, item, check_budget):
        # Explicit inert locator shape: compare old/new quota projections only.
        # This does not qualify the real custody schema or durability.
        result = []
        for row in item.document["unit"][2]:
            check_budget()
            result.append((self.S.export_id(self.semantic_id, item.unit_id, row[0]),
                           encoded({"unit": item.unit_id, "name": row[0]})))
        return result

    def status(self):
        return {"counts": {"objects": len(self.held), "exports": len(self.locators),
                           "logical_bytes": sum(map(len, self.held.values()))}}


class DBReadDouble:
    def __init__(self, store):
        self.store = store

    def execute(self, sql, values=()):
        if sql == "SELECT count(*) FROM roots":
            row = (1,)
        elif sql == "SELECT count(*),COALESCE(sum(reserved_bytes),0) FROM operations":
            row = (1, 1024)
        elif sql == "SELECT COALESCE(sum(reserved_bytes),0) FROM imports":
            row = (0,)
        elif sql == "SELECT length(raw),raw_sha256 FROM objects WHERE kind='evidence' AND identity=?":
            raw = self.store.held.get(values[0])
            row = None if raw is None else (len(raw), sha(raw))
        elif sql == "SELECT unit_id,locator FROM exports WHERE export_id=?":
            row = self.store.locators.get(values[0])
        else:
            raise AssertionError("UNEXPECTED_DOUBLE_SQL:"+sql)
        return NS(fetchone=lambda: row)


class Model:
    """Virtual paths, real admission flow, synthetic grant/event/commit authority."""
    def __init__(self, A, PE, fixed, items, base, *, existing=(), mode="ok"):
        self.A, self.PE, self.base, self.mode = A, PE, base, mode
        self.events, self.writes, self.files, self.native = [], {}, {}, []
        self.observer = None
        semantic = A.S.semantic_id()
        self.store = StoreDouble()
        self.store.PE, self.store.S = PE, A.S
        self.store.semantic_id, self.store.root = semantic, base/"custody"
        self.store.held, self.store.locators = {}, {}
        self.store.observer, self.store.fail_put = None, mode == "put-failure"
        self.store.limits = dict(objects=4096, exports=8192, logical_bytes=128*MIB, db_pages=65536)
        bindings = dict(fixed)
        for index in existing:
            item = items[index]
            self.store.held[item.unit_id] = item.raw
            for row in item.document["unit"][2]:
                bindings[A.E.name_key(row[0])] = A.S.export_id(semantic, item.unit_id, row[0])
            for export, raw in self.store._export_locators(item, check):
                self.store.locators[export] = (item.unit_id, raw)
        self.store.db = DBReadDouble(self.store)
        parent = "a"*64
        module = A.C.module_name(parent)
        self.contexts = {parent: {"local_root": parent, "semantic_id": semantic,
            "bindings": bindings, "basis_module": module, "root_module": module,
            "modules": []}}
        self.catalog = NS(semantic_id=semantic, _grant=None, _closed=False,
                          _limits=A.P.Limits(), _db=DBReadDouble(self.store), _active=check)
        self.catalog.context = lambda root: deepcopy(self.contexts[root])
        self.catalog._reserve = self.reserve
        self.catalog.reserve_extension = lambda *args, **kwargs: A.P.PortableCatalog.reserve_extension(
            self.catalog, *args, **kwargs)
        self.catalog._commit_checked = self.commit
        self.catalog.abandon = self.abandon
        self.catalog.close = self.close
        self.owner = A.OrdinaryAdmission.__new__(A.OrdinaryAdmission)
        self.owner.catalog, self.owner.evidence_store = self.catalog, self.store
        self.owner.directory = base/"catalog"
        self.owner._call_directory = lambda: base/"call"/str(len(self.native))
        self.owner._write = self.write
        self.owner.installation = NS(semantic_id=semantic, root=base/"support",
            runtime_roots={"python_runtime": base/"python", "lean_runtime": base/"lean"},
            manifest_raw=b"{}", manifest_sha256=sha(b"{}"),
            path=lambda role: base/"support"/role,
            _supervisor=NS(limits_checked=lambda limits: limits, supervise=self.supervise,
                           save_new=lambda path, value: self.write(path, encoded(value), MIB)),
            _job_module=NS(Job=object))

    def reserve(self, kind, parent, request, bindings, identities, modules, *,
                seconds, output_bytes, parent_deadline):
        check()
        root = sha(encoded([parent, identities]))
        self.introduced = deepcopy(bindings)
        self.events.append("reserve")
        grant = NS(kind=kind, parent=parent, root=root, input_unit_ids=tuple(identities),
            request_hash=request, parent_plan_raw=encoded(modules),
            parent_module_raw=encoded(self.contexts[parent]["root_module"]),
            module_name_raw=encoded(self.A.C.module_name(root)),
            deadline=min(parent_deadline, time.monotonic()+seconds), directory=self.base/"grant"/root)
        if self.mode == "grant-mismatch":
            grant.input_unit_ids = ("f"*64,)
        self.catalog._grant = grant
        return grant

    def commit(self, grant):
        self.events.append("commit-double")
        current = deepcopy(self.contexts[grant.parent])
        current["local_root"], current["root_module"] = grant.root, json.loads(grant.module_name_raw)
        for name, symbol in self.introduced:
            current["bindings"][self.A.E.name_key(name)] = symbol
        self.contexts[grant.root] = current
        self.catalog._grant = None
        return grant.root

    def abandon(self, grant):
        self.events.append("abandon")
        need(self.catalog._grant is grant, "DOUBLE_GRANT_IDENTITY")
        self.catalog._grant = None

    def close(self):
        self.events.append("close-quarantine")
        self.catalog._closed = True

    def write(self, path, raw, maximum):
        need(type(raw) is bytes and 0 < len(raw) <= maximum, "DOUBLE_WRITE_BOUND")
        self.writes[Path(path)] = raw

    def ordinary(self, path, **kwargs):
        path = Path(path)
        if path.name == "chunk.olean":
            return NS(stat=lambda: NS(st_size=1))
        if path.name in ("stdout.txt", "stderr.txt"):
            return NS(stat=lambda: NS(st_size=0))
        return path

    def read(self, path, maximum):
        path = Path(path)
        raw = self.files[path] if path in self.files else self.writes[path]
        need(len(raw) <= maximum, "DOUBLE_READ_BOUND")
        return raw

    def supervise(self, argv, call, output, limits, job):
        check()
        if self.observer is not None:
            need(self.observer.live() == 0, "PRIVATE_PARSE_REACHED_NATIVE_CALLBACK")
        grant = self.catalog._grant
        units = json.loads(self.writes[call/"units.json"])
        names = [row[0] for unit in units for row in unit[2]]
        self.native.append({"units": self.writes[call/"units.json"],
                            "plan": self.writes[call/"plan.json"],
                            "ids": grant.input_unit_ids, "names": deepcopy(names)})
        report = {"schema": "DMKN_ORDINARY_WORKER_OUTPUT_V1", "kind": "extension",
            "module_name": json.loads(grant.module_name_raw),
            "parent_module": json.loads(grant.parent_module_raw), "names": names,
            "units_checked": len(units), "artifact_bytes": 1}
        if self.mode == "report-mismatch":
            report["names"] = []
        self.writes[call/"worker-report.json"] = encoded(report)
        clean = self.mode not in ("native-failure", "native-uncertain")
        return {"status": "COMMAND_EXITED_ZERO_AND_CLOSED" if clean else "COMMAND_FAILED",
            "child_exit_code": 0 if clean else 1, "direct_child_reaped": True,
            "job_closed": self.mode != "native-uncertain", "cleanup_errors": [],
            "termination_requested": False,
            "final_job": {"active_processes": 0, "terminated_processes": 0, "cpu_seconds": 0.0}}

    def patches(self, stack):
        stack.enter_context(patch.object(self.A.C, "ordinary", self.ordinary))
        stack.enter_context(patch.object(self.A.C, "read_bounded", self.read))
        stack.enter_context(patch.object(self.A.os.path, "lexists", lambda path: False))


def run_controls(output):
    forbidden_calls, groups = [], []

    def forbidden(*args, **kwargs):
        forbidden_calls.append("FORBIDDEN")
        raise AssertionError("PARSE_REUSE_FORBIDDEN_EXTERNAL_OPERATION")

    with ExitStack() as barrier:
        for obj, attribute in ((subprocess, "Popen"), (subprocess, "run"),
                (subprocess, "call"), (os, "system"), (sqlite3, "connect"), (socket, "socket")):
            barrier.enter_context(patch.object(obj, attribute, forbidden))
        loaded = {}
        for name, rel in (("ordinary_evidence", "installation/py/ordinary_evidence.py"),
                ("ordinary_semantics", "installation/py/ordinary_semantics.py"),
                ("portable_evidence", "installation/py/portable_evidence.py"),
                ("local_catalog", "installation/py/local_catalog.py"),
                ("portable_catalog", "installation/py/portable_catalog.py"),
                ("portable_candidate", "authoring/py/portable_candidate.py"),
                ("baseline_bundle", "reference/baseline_bundle.py"),
                ("_parse_predecessor_admission", "installation/py/ordinary_admission.py")):
            loaded[name] = source(name, PACKAGE/rel, PINS[rel])
        old = loaded["_parse_predecessor_admission"]
        new = source("ordinary_admission", Path(__file__).parent/"ordinary_admission.py")
        transport, acquisition = ModuleType("transport"), ModuleType("transport.ordinary_acquisition")
        acquisition.OrdinaryStore = StoreDouble
        transport.ordinary_acquisition = acquisition
        barrier.enter_context(patch.dict(sys.modules, {"transport": transport,
                                                      "transport.ordinary_acquisition": acquisition}))
        before = source("_parse_predecessor_intake", PACKAGE/"reference/baseline_intake.py",
                        PINS["reference/baseline_intake.py"])
        before.A = old
        after = source("_parse_successor_intake", Path(__file__).parent/"baseline_intake.py")
        E, PE, B = new.E, new.PE, loaded["baseline_bundle"]
        need(old.PE is PE and old.E is E and B.PE is PE and after.A is new, "SHARED_REAL_PARSERS")
        for A in (old, new):
            barrier.enter_context(patch.object(A.OrdinaryAdmission, "open", forbidden))
            barrier.enter_context(patch.object(A.P.PortableCatalog, "open", forbidden))
        raws = tuple((LOCAL/relative).read_bytes() for relative, digest in FIXTURES)
        need(all(len(raw) <= 64*1024 and sha(raw) == digest
                 for raw, (_, digest) in zip(raws, FIXTURES)), "SMALL_FIXTURE_PINS")
        items = tuple(PE.read_evidence(raw) for raw in raws)
        outputs = {E.name_key(row[0]) for item in items for row in item.document["unit"][2]}
        fixed = {}
        for item in items:
            for name, symbol in item.document["imports"]:
                key = E.name_key(name)
                if key not in outputs:
                    need(key not in fixed or fixed[key] == symbol, "FIXTURE_IMPORT_AGREEMENT")
                    fixed[key] = symbol
        need(bool(fixed), "FIXTURE_NONEMPTY_BASIS_IMPORTS")
        parent, base = "a"*64, output/"virtual-not-created"

        def record(name, **details):
            check(); groups.append({"group": name, **details})

        def observe(action, model=None):
            watch = Reads(PE.read_evidence)
            if model is not None:
                model.observer = model.store.observer = watch
            with patch.object(PE, "read_evidence", watch):
                result = action()
            watch.released()
            return result, watch

        def model(A, **kwargs):
            return Model(A, PE, fixed, items, base, **kwargs)

        def refuse(action, code):
            try:
                action()
            except ValueError as error:
                need(code in str(error), "WRONG_REFUSAL:"+code+":"+str(error))
                return
            raise AssertionError("MISSING_REFUSAL:"+code)

        public_fields = {"status", "parent_root", "raw_units", "ordered_units", "missing", "reused_unit_ids"}
        for existing, supplied in (((), raws), ((), tuple(reversed(raws))),
                ((), (raws[0], raws[0], *raws[1:])), ((0,), raws), ((0, 1, 2), raws)):
            expected, actual = None, None
            for A in (old, new):
                instance = model(A, existing=existing)
                plan, watch = observe(lambda: instance.owner.preflight(parent, supplied))
                need({field.name for field in fields(plan)} == public_fields and
                     all(type(raw) is bytes for raw in plan.raw_units) and
                     sum(watch.counts.values()) == len(supplied), "RAW_ONLY_PUBLIC_PLAN")
                if A is old:
                    expected = asdict(plan)
                else:
                    actual = asdict(plan)
            need(expected == actual, "PLAN_EQUIVALENCE")
        record("public-plans-equivalent-reversed-duplicates-mixed-and-reused")

        fresh_context = model(new).catalog.context(parent)
        private_plan, parsed = new._plan_with_parsed(fresh_context, raws, new.PreflightLimits(), check)
        need(set(parsed) == set(raws) and all(key == value.raw and type(key) is bytes
             for key, value in parsed.items()), "PRIVATE_EXACT_RAW_KEYS")
        parsed[raws[0]].document["schema"] = "MUTATED_PRIVATE_TEST_VALUE"
        del parsed, private_plan
        again = new._plan(fresh_context, raws, new.PreflightLimits(), check)
        need(asdict(again) == asdict(old._plan(fresh_context, raws, old.PreflightLimits(), check)),
             "NO_CROSS_CALL_MUTABLE_CACHE")
        record("private-map-exact-byte-key-and-next-call-freshness")

        for A in (old, new):
            missing_context = deepcopy(fresh_context)
            missing_context["bindings"] = {}
            missing = A._plan(missing_context, raws, A.PreflightLimits(), check)
            need(missing.status == "NEEDS" and bool(missing.missing), "MISSING_IMPORTS_STILL_NEEDS")
            changed = json.loads(raws[1]); changed["imports"][0][1] = "f"*64
            refuse(lambda: A._plan(fresh_context, (raws[1], encoded(changed)),
                                  A.PreflightLimits(), check), "ADMISSION_SELECTED_NAME_CONFLICT")
        record("missing-imports-and-distinct-identity-selected-name-conflict")

        def admission(A, *, supplied=raws, existing=(), forged=False, mode="ok"):
            instance = model(A, existing=existing, mode=mode)
            budget = A.OperationBudget(40, 20, 64)
            def action():
                plan = instance.owner.preflight(parent, supplied, budget=budget)
                if forged:
                    plan = replace(plan, status="NEEDS", ordered_units=(b"not evidence",),
                                   missing=((b"forged", "f"*64),), reused_unit_ids=("e"*64,))
                    object.__setattr__(plan, "parsed", {raws[0]: "UNTRUSTED"})
                return instance.owner.admit(parent, plan, budget)
            with ExitStack() as scope:
                instance.patches(scope)
                result, watch = observe(action, instance)
            return instance, result, watch

        pair = [admission(A) for A in (old, new)]
        need(pair[0][0].native == pair[1][0].native and len(pair[1][0].native) == 1,
             "EXACT_NATIVE_INPUT_AND_ORDER_EQUIVALENCE")
        for index, (_, result, watch) in enumerate(pair):
            need(result["status"] == "CHECKED" and result["units_checked"] == 3 and
                 watch.counts == Counter({raw: (8 if index == 0 else 5) for raw in raws}),
                 "ADMISSION_EXACT_PARSE_COUNT")
        record("native-input-projection-equivalence-and-eight-to-five-count",
               predecessor_reads=24, successor_reads=15, authority="SYNTHETIC_NATIVE_EVENT_ONLY")
        for A in (old, new):
            instance, result, watch = admission(A, forged=True)
            need(instance.native == pair[0][0].native and result["units_checked"] == 3,
                 "FORGED_PUBLIC_METADATA_IGNORED")
            instance, result, watch = admission(A, existing=(0, 1, 2))
            need(result["status"] == "REUSED" and not instance.native and
                 watch.counts == Counter({raw: 4 for raw in raws}), "REUSED_RECHECK_AND_NO_NATIVE")
            instance, first, _ = admission(A)
            next_parent = first["local_root"]
            def next_call():
                budget = A.OperationBudget(40, 20, 64)
                plan = instance.owner.preflight(next_parent, raws, budget=budget)
                return instance.owner.admit(next_parent, plan, budget)
            with ExitStack() as scope:
                instance.patches(scope)
                next_result, next_watch = observe(next_call, instance)
            need(next_result["status"] == "REUSED" and len(instance.native) == 1 and
                 next_watch.counts == Counter({raw: 4 for raw in raws}), "SAME_OWNER_NEXT_CALL_REPARSES")
        record("forged-public-metadata-recomputed-and-reused-staging-unchanged")

        for A in (old, new):
            for kind in ("raw", "parent", "context", "imports"):
                instance = model(A)
                plan = instance.owner.preflight(parent, raws)
                if kind == "raw":
                    plan = replace(plan, raw_units=(raws[0][:-1]+b"!",))
                    code = "JSON_"
                elif kind == "parent":
                    plan = replace(plan, parent_root="b"*64)
                    code = "ADMISSION_PLAN_TYPE_OR_PARENT"
                elif kind == "context":
                    key = next(iter(fixed))
                    instance.contexts[parent]["bindings"][key] = "f"*64
                    code = "ADMISSION_PARENT_IMPORT_CONFLICT"
                else:
                    doc = json.loads(raws[1]); doc["imports"][0][1] = "f"*64
                    plan = replace(plan, raw_units=(raws[0], encoded(doc), raws[2]))
                    code = "ADMISSION_PARENT_IMPORT_CONFLICT"
                with ExitStack() as scope:
                    instance.patches(scope)
                    observe(lambda: refuse(lambda: instance.owner.admit(parent, plan,
                        A.OperationBudget(40, 20, 64)), code), instance)
                need(not instance.events and not instance.store.held and not instance.native,
                     "REVALIDATION_BEFORE_SIDE_EFFECT")
        record("changed-raw-parent-current-context-and-imports-refused")

        for changed in ("order", "ids"):
            instance = model(new)
            original_execute = instance.owner._execute
            def corrupt(*args, **kwargs):
                raw_order, identities, unit_json = kwargs["_prepared_extension"]
                need(type(raw_order) is tuple and all(type(raw) is bytes for raw in raw_order) and
                     type(identities) is tuple and all(type(value) is str for value in identities) and
                     type(unit_json) is bytes, "PRIVATE_PROJECTION_ONLY_IMMUTABLE_VALUES")
                kwargs["_prepared_extension"] = (
                    tuple(reversed(raw_order)) if changed == "order" else raw_order,
                    ("f"*64, *identities[1:]) if changed == "ids" else identities, unit_json)
                return original_execute(*args, **kwargs)
            instance.owner._execute = corrupt
            plan = instance.owner.preflight(parent, raws)
            with ExitStack() as scope:
                instance.patches(scope)
                observe(lambda: refuse(lambda: instance.owner.admit(parent, plan,
                    new.OperationBudget(40, 20, 64)), "ADMISSION_PRIVATE_RAW_BINDING"), instance)
            need(instance.events == ["reserve", "abandon"] and not instance.native,
                 "PRIVATE_PROJECTION_REFUSED_BEFORE_NATIVE")
        record("private-immutable-projection-order-and-id-guards")

        for A in (old, new):
            for mode, code, ending in (("put-failure", "DOUBLE_CUSTODY_FAILURE", []),
                    ("grant-mismatch", "ADMISSION_EXTENSION_GRANT", ["reserve", "abandon"]),
                    ("native-failure", "ADMISSION_NATIVE_EVENT_NOT_CLEAN", ["reserve", "abandon"]),
                    ("report-mismatch", "ADMISSION_ACTUAL_REPORT_BINDING", ["reserve", "abandon"]),
                    ("native-uncertain", "ADMISSION_NATIVE_EVENT_NOT_CLEAN", ["reserve", "close-quarantine"])):
                instance = model(A, mode=mode)
                plan = instance.owner.preflight(parent, raws)
                with ExitStack() as scope:
                    instance.patches(scope)
                    observe(lambda: refuse(lambda: instance.owner.admit(parent, plan,
                        A.OperationBudget(40, 20, 64)), code), instance)
                need(instance.events == ending and "commit-double" not in instance.events,
                     "FAILURE_CLEANUP_UNCHANGED:"+mode)
                if mode == "native-uncertain":
                    need(instance.owner.directory/"WITHDRAWN" in instance.writes,
                         "QUARANTINE_MARKER_PRESERVED")
        record("five-failure-paths-preserve-abandon-or-quarantine-no-commit")

        batches = (raws[:2], raws[2:])
        manifest = B.make_manifest(batches)

        def intake(I, A, *, full, existing=(), mutate_second=False):
            instance = model(A, existing=existing)
            directory = base/"bundle"
            instance.files = {directory/entry.relative_path: raw
                for batch, entries in zip(batches, manifest.batches)
                for raw, entry in zip(batch, entries)}
            seen = Counter()
            first_of_second = directory/manifest.batches[1][0].relative_path
            original_read = instance.read
            def read(path, maximum):
                path = Path(path)
                if path in instance.files:
                    seen[path] += 1
                    if A is new and path == first_of_second and seen[path] == 1:
                        need(instance.observer.live() == 0, "PREVIOUS_PLANNING_BATCH_RETAINED")
                    if mutate_second and path == first_of_second and seen[path] == 2:
                        raw = original_read(path, maximum)
                        return raw[:-1]+b"!"
                return original_read(path, maximum)
            instance.read = read
            budget = I.IntakeBudget(40, 25, 64)
            calls = I.CallLimits(cpu_seconds=5, output_bytes=MIB)
            def action():
                if full:
                    return I.intake(instance.owner, parent, directory, manifest.raw, manifest.sha256,
                                    budget=budget, calls=calls)
                return I._plan_all(instance.owner, instance.catalog.context(parent), manifest,
                                   directory, B.Limits(), calls, budget)
            with ExitStack() as scope:
                instance.patches(scope)
                if mutate_second:
                    def stopped():
                        try:
                            action()
                        except I.IntakeError as error:
                            # Drop the exception/traceback before checking object lifetime.
                            return deepcopy(error.report)
                        raise AssertionError("MISSING_CHANGED_SECOND_BATCH_REFUSAL")
                    result, watch = observe(stopped, instance)
                else:
                    result, watch = observe(action, instance)
            return instance, result, watch

        planned = [intake(I, A, full=False) for I, A in ((before, old), (after, new))]
        need(planned[0][1] == planned[1][1], "METADATA_PROJECTION_EQUIVALENCE")
        for index, (_, result, watch) in enumerate(planned):
            need(watch.counts == Counter({raw: (4 if index == 0 else 2) for raw in raws}),
                 "METADATA_EXACT_COUNT")
            if index == 1:
                need(watch.peak <= 2, "SUCCESSOR_METADATA_BATCH_LIFETIME")
        for I, A in ((before, old), (after, new)):
            instance, result, watch = intake(I, A, full=False, existing=(0, 1, 2))
            need(result["native_launches"] == 0 and result["custody_additions"] ==
                 dict(objects=0, exports=0, logical_bytes=0), "REUSED_METADATA_EXACT")
            need(watch.counts == Counter({raw: (3 if A is old else 2) for raw in raws}),
                 "REUSED_METADATA_PARSE_COUNT")
        record("metadata-equivalence-four-to-two-reused-three-to-two-and-batch-release")

        whole = [intake(I, A, full=True) for I, A in ((before, old), (after, new))]
        for index, (instance, result, watch) in enumerate(whole):
            need(result["status"] == "BASELINE_INTAKE_COMPLETE" and
                 [row["units_checked"] for row in result["batches"]] == [2, 1] and
                 watch.counts == Counter({raw: (13 if index == 0 else 8) for raw in raws}),
                 "WHOLE_THIRTEEN_TO_EIGHT_COUNT")
        need(whole[0][0].native == whole[1][0].native and whole[0][1]["planning"] ==
             whole[1][1]["planning"], "WHOLE_NATIVE_AND_METADATA_EQUIVALENCE")
        record("full-inert-flow-thirteen-to-eight-and-exact-projections",
               predecessor_reads=39, successor_reads=24, authority="SYNTHETIC_NATIVE_EVENTS_ONLY")
        for I, A in ((before, old), (after, new)):
            instance, result, watch = intake(I, A, full=True, mutate_second=True)
            need(result["status"] == "BASELINE_INTAKE_STOPPED" and
                 result["phase"] == "BATCH_PREFLIGHT" and
                 "BASELINE_EVIDENCE_EXACT_BYTES" in result["error"] and
                 len(result["batches"]) == len(instance.native) == 1 and
                 result["last_confirmed_root"] == result["batches"][0]["local_root"] and
                 result["possible_unreported_commit"] is False, "PREFIX_NO_RETRY_OR_ROLLBACK")
        record("changed-second-read-preserves-first-confirmed-double-prefix")
        need(not forbidden_calls, "FORBIDDEN_OPERATION_ATTEMPTED")
    return {"status": "PASS_FOCUSED_PARSE_REUSE_INERT_CONTROLS", "groups": groups,
            "group_count": len(groups), "forbidden_calls": forbidden_calls,
            "mathematical_acceptance": False,
            "authority": "REAL_SYNTAX_AND_CONTROL_FLOW_WITH_EXPLICIT_CATALOG_CUSTODY_NATIVE_DOUBLES",
            "state": "NO_REAL_OWNER_DATABASE_NATIVE_OR_NETWORK_OPERATION"}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize, "PROCESS")
    output = Path(args.output)
    need(output == LOCAL/"parse-reuse-controls01/controls" and output.parent.is_dir()
         and not os.path.lexists(output), "FRESH_EXACT_OUTPUT")
    output.mkdir()
    try:
        report = run_controls(output)
    except BaseException as error:
        report = {"status": "FAIL", "error_type": type(error).__name__, "error": str(error),
                  "mathematical_acceptance": False}
    report.update(wall_seconds=time.monotonic()-START, cpu_seconds=time.process_time()-CPU)
    raw = encoded(report)
    need(len(raw) <= MIB, "REPORT_BOUND")
    with (output/"RESULT.json").open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    print(json.dumps(report, sort_keys=True), flush=True)
    return 0 if report["status"] == "PASS_FOCUSED_PARSE_REUSE_INERT_CONTROLS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

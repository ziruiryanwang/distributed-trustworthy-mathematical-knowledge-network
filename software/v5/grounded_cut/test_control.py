"""Focused SOURCE-selected native-free controls, never mathematical acceptance.

Real codecs, summary preparation and SQLite map; explicit synthetic runtime,
anchor, custody and catalog doubles for controller orchestration. No native
installation, existing protected state, Lean, package or network is opened.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import stat
import sys
import time
from types import ModuleType, SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()
CASES = []


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic() - START < 60 and time.process_time() - CPU < 30,
         "CONTROL_ORIGINAL_ALLOWANCE")


def refusal(code, action, exception=ValueError):
    try:
        action()
    except exception as error:
        need(code in str(error), "WRONG_REFUSAL:" + str(error))
        return error
    raise AssertionError("MISSING_REFUSAL:" + code)


def case(label, action):
    check()
    action()
    CASES.append(label)


def module(name, path):
    need(name not in sys.modules and path.is_file(), "CONTROL_FIXED_SOURCE")
    need(path.is_absolute() and ".." not in path.parts, "CONTROL_SOURCE_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             (getattr(info, "st_file_attributes", 0) & 0x400), "CONTROL_SOURCE_REDIRECTION")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "CONTROL_SOURCE_KIND")
    with path.open("rb") as stream:
        raw = stream.read(2 * MIB + 1)
    need(0 < len(raw) <= 2 * MIB, "CONTROL_SOURCE_BOUND")
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    exec(compile(raw, str(path), "exec", dont_inherit=True), value.__dict__)
    need(Path(value.__file__).absolute() == path, "CONTROL_SOURCE_IDENTITY")
    return value, {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def name(text):
    return [[0, {"$bytes": list(text.encode("ascii"))}]]


def allowance():
    return M.Allowance(100000, 100000, 16 * MIB, 16 * MIB)


def claim(text, imports=(), *, concrete=False):
    """Syntactically valid but intentionally UNCHECKED synthetic Lean claims."""
    own = name(text)
    sort = [E.EXPR_FORMAT, [[0]], [[1, 0]], 0]
    nodes = [[2, encoded, []] for encoded, _ in imports]
    if not nodes:
        proof = sort  # Deliberately not asserted to be a well-typed theorem.
    else:
        for index in range(1, len(imports)):
            nodes.append([3, 0 if index == 1 else len(nodes) - 1, index])
        proof = [E.EXPR_FORMAT, [], nodes, len(nodes) - 1]
    if concrete:
        descriptor = [0, own, [], sort, proof, [0], [own]]
        inventory = [own, 1, [], sort, [proof, [0], [own]]]
    else:
        descriptor = [1, own, [], sort, proof, [own]]
        inventory = [own, 2, [], sort, [proof, [own]]]
    return E.canonical_json({"schema": PE.SCHEMA, "semantic_id": S.semantic_id(),
        "imports": sorted([list(row) for row in imports], key=lambda row: E.name_key(row[0])),
        "unit": [E.UNIT_FORMAT, descriptor, [inventory]]})


def fixture():
    # These 581 strings satisfy only the parser's caller precondition, not the
    # genuine basis contract. Native kernel/seed acceptance is intentionally absent.
    basis = {E.name_key(name("fake_basis_" + str(i))): "0" * 64 for i in range(581)}
    old = Q.project(claim("old", [(name("proof_only_ancestor"), "a" * 64)]))
    key, symbol = old.bindings[0]
    raw_new = claim("new", [(E.strict_json(key), symbol)])
    return basis, old, raw_new


def prepare(raw_new, basis, summaries, bindings):
    return Q.prepare(raw_new, semantic_id=S.semantic_id(), basis=basis,
        lookup=lambda encoded: bindings.get(E.name_key(encoded)),
        read_summary=lambda digest: summaries[digest], check=check)


def map_controls(output):
    database = output / "map.sqlite"
    db = sqlite3.connect(database, isolation_level=None)
    db.execute("BEGIN IMMEDIATE")
    M.create_schema(db, allowance())
    one = M.insert(db, M.EMPTY_ROOT, E.name_key(name("one")), b"first", allowance())
    two = M.insert(db, one, E.name_key(name("two")), b"second", allowance())
    db.execute("COMMIT")
    db.close()
    db = sqlite3.connect(database, isolation_level=None)
    try:
        db.execute("BEGIN IMMEDIATE")
        queries = []
        db.set_trace_callback(queries.append)
        need(M.lookup(db, one, E.name_key(name("one")), allowance()) == b"first" and
             M.lookup(db, one, E.name_key(name("two")), allowance()) is None and
             M.lookup(db, two, E.name_key(name("two")), allowance()) == b"second", "MAP_PERSISTENCE")
        need(all("WHERE node_id =" in sql for sql in queries if sql.startswith("SELECT")),
             "MAP_NOT_PRIMARY_KEY_LOCAL")
        case("map-reopen-old-root-exact-absence", lambda: None)
        same = M.insert(db, two, E.name_key(name("one")), b"first", allowance())
        need(same == two, "MAP_DUPLICATE_ROOT_CHANGED")
        refusal("KEY_ALREADY_BOUND", lambda: M.insert(db, two, E.name_key(name("one")), b"bad", allowance()))
        case("map-identical-idempotence-and-conflicting-binding", lambda: None)
        refusal("ALLOWANCE_READS", lambda: M.lookup(db, two, E.name_key(name("one")), M.Allowance(0, 0, 0, 0)))
        case("map-zero-read-allowance", lambda: None)
        three = M.insert(db, two, E.name_key(name("three")), b"third", allowance())
        db.execute("ROLLBACK")
        db.execute("BEGIN IMMEDIATE")
        refusal("MISSING_NODE", lambda: M.lookup(db, three, E.name_key(name("three")), allowance()))
        need(M.lookup(db, two, E.name_key(name("three")), allowance()) is None, "MAP_ROLLBACK")
        case("map-uncommitted-prefix-not-reusable", lambda: None)
        db.execute("UPDATE grounded_cut_nodes SET payload=? WHERE node_id=?", (b"broken", two))
        refusal("NODE_HASH", lambda: M.lookup(db, two, E.name_key(name("one")), allowance()))
        case("map-selected-node-corruption", lambda: None)
        db.execute("ROLLBACK")
    finally:
        db.close()


def summary_controls():
    basis, old, raw_new = fixture()
    key, symbol = old.bindings[0]
    summaries, bindings = {old.summary_id: old.raw}, {key: (symbol, old.summary_id)}
    prepared = prepare(raw_new, basis, summaries, bindings)
    need(prepared.stats.acquired_summaries == 1 and len(prepared.signature_rows) == 1 and
         not prepared.concrete_units and E.strict_json(old.raw)["imports"] == [], "SIGNATURE_CUT")
    case("summary-proof-only-ancestry-not-acquired", lambda: None)
    case("summary-missing-parent-binding", lambda: refusal("UNGROUNDED_IMPORT",
        lambda: prepare(raw_new, basis, summaries, {})))
    case("summary-wrong-exact-symbol", lambda: refusal("UNGROUNDED_IMPORT",
        lambda: prepare(raw_new, basis, summaries, {key: ("f" * 64, old.summary_id)})))
    case("summary-content-hash-refusal", lambda: refusal("CUT_SUMMARY_HASH",
        lambda: prepare(raw_new, basis, {old.summary_id: old.raw + b" "}, bindings)))
    alias = name("zz_alias")
    alias_symbol = S.export_id(S.semantic_id(), old.unit_id, alias)
    forged = dict(bindings)
    forged[E.name_key(alias)] = (alias_symbol, old.summary_id)
    alias_new = claim("new", [(E.strict_json(key), symbol), (alias, alias_symbol)])
    case("summary-omitted-demanded-group-member", lambda: refusal("DEMANDED_GROUP_MEMBER",
        lambda: prepare(alias_new, basis, summaries, forged)))
    concrete = Q.project(claim("concrete", [(E.strict_json(key), symbol)], concrete=True))
    ckey, csymbol = concrete.bindings[0]
    mixed = {**summaries, concrete.summary_id: concrete.raw}
    mapping = {**bindings, ckey: (csymbol, concrete.summary_id)}
    case("summary-concrete-needs-omitted-theorem", lambda: refusal("CONCRETE_NEEDS_OLD_THEOREM",
        lambda: prepare(claim("new", [(E.strict_json(ckey), csymbol)]), basis, mixed, mapping)))


class Budget:
    def __init__(self):
        self.claimed = False
        self.deadline = START + 60
        self.output_bytes, self.log_bytes, self.worker_cpu = 64 * MIB, 1024, 0
    def check(self):
        check()
    def claim(self):
        need(not self.claimed, "DOUBLE_BUDGET_CLAIM")
        self.claimed = True
    def allowance(self, deadline):
        need(deadline == self.deadline, "BUDGET_REPLENISHED")
        return {"synthetic": True}


class Scenario:
    """TEST DOUBLE: nothing in this class establishes mathematical authority."""
    def __init__(self, directory, mode="good"):
        self.directory, self.mode = directory, mode
        directory.mkdir()
        self.target, self.call = directory / "synthetic-store", directory / "call"
        self.target.mkdir()
        self.basis, self.old, self.raw_new = fixture()
        self.key, self.symbol = self.old.bindings[0]
        self.new_key = E.name_key(name("new"))
        self.parent_id, self.parent_map = "1" * 64, "2" * 64
        self.worker_calls, self.commits, self.inserts = 0, 0, []
        self.selected_allowance = None
        self.committed, self.blobs = {}, {self.old.summary_id: self.old.raw}
        self.closed = False
        self.runtime = NS(support_id="3" * 64, semantic_id=S.semantic_id(),
                          verify=lambda callback: callback(), check_packet=self.worker)
        self.anchor = NS(check=self.anchor_check)
        self.catalog = NS(_root=self.target, _limits=K.Limits(),
            _identity=dict(store_id="4" * 64, support_id=self.runtime.support_id,
                           epoch="5" * 64, source_binding_sha256="6" * 64),
            _begin=lambda original: need(original is self.selected_allowance, "ALLOWANCE_IDENTITY"),
            root=self.root, lookup=self.lookup, read_summary=self.blobs.__getitem__,
            put_summary=self.put, _insert=self.insert, _commit_root=self.commit,
            _read=self.read, close=lambda: setattr(self, "closed", True))
        self.catalog._record = lambda record: K.CutCatalog._record(self.catalog, record)
        self.custody = NS(put_evidence=self.hold, get_evidence=lambda *args, **kwargs: self.raw_new)

    def anchor_check(self):
        check()
        if self.mode == "withdraw" and self.worker_calls:
            raise ValueError("SYNTHETIC_SOURCE_WITHDRAWN")

    def root(self, identifier):
        return deepcopy(self.committed[identifier] if identifier in self.committed else
                        {"map_root": self.parent_map})

    def lookup(self, parent, key):
        need(parent == self.parent_id, "WRONG_PARENT_SELECTED")
        if key == self.new_key:
            return b"collision" if self.mode == "collision" and self.worker_calls else None
        if key == self.key and self.mode != "sibling":
            return E.canonical_json([self.symbol, "f" * 64 if self.mode == "frontier" and
                                    self.worker_calls else self.old.summary_id])
        return None

    def put(self, raw):
        digest = hashlib.sha256(K.SUMMARY_DOMAIN + raw).hexdigest()
        self.blobs[digest] = raw
        return digest

    def insert(self, root, key, value):
        need(root == self.parent_map and key == self.new_key, "MAP_NOT_EXTENDED_FROM_PARENT")
        self.inserts.append((root, key, value))
        return "7" * 64

    def hold(self, raw, *, before_commit):
        before_commit()
        return dict(semantic_id=S.semantic_id(), identity=PE.read_evidence(raw).unit_id,
                    raw_sha256=hashlib.sha256(raw).hexdigest(), raw_bytes=len(raw),
                    mathematical_acceptance=self.mode == "custody")

    def worker(self, packet, call, budget):
        self.worker_calls += 1
        call.mkdir()
        if self.mode == "uncertain":
            raise R.UncertainWorker("SYNTHETIC_UNCERTAIN")
        return b"SYNTHETIC_REPORT_NOT_NATIVE_EVIDENCE", {"synthetic": 1}

    def commit(self, record):
        raw = self.catalog._record(record)
        candidate = hashlib.sha256(K.ROOT_DOMAIN + raw).hexdigest()
        intent = E.strict_json(P.read_bounded(self.call / "COMMIT-INTENT.json", 128 * 1024))
        need(intent["candidate_root"] == candidate and intent["record"] == record, "INTENT_MUST_PRECEDE_COMMIT")
        self.commits += 1
        self.committed[candidate] = deepcopy(record)
        if self.mode == "lost-reply":
            raise K.CommitDisposition(candidate, "COMMITTED")
        return candidate

    def read(self, table, candidate, cap, domain, optional):
        need(table == "roots" and domain == K.ROOT_DOMAIN and optional, "RESOLVE_NOT_ROOT_PK")
        return None if candidate not in self.committed else E.canonical_json(self.committed[candidate])

    def patches(self):
        stack = ExitStack()
        def claimed(runtime, budget, original):
            need(runtime is self.runtime and original is self.selected_allowance, "ORIGINAL_OPERATION")
            budget.claim()
        stack.enter_context(patch.object(T, "_claim", claimed))
        stack.enter_context(patch.object(T, "_marker", lambda *args: (self.target, b"synthetic", {"directory": self.directory})))
        stack.enter_context(patch.object(T, "_paths", lambda *args, **kwargs: (self.target, self.call)))
        stack.enter_context(patch.object(T, "_basis", lambda *args: (self.basis, 0)))
        scenario = self
        class Anchor:
            def __enter__(self):
                return scenario.anchor
            def __exit__(self, *_):
                return False
        stack.enter_context(patch.object(H.SourceAnchor, "open", lambda *args, **kwargs: Anchor()))
        def opened(*args, **kwargs):
            kwargs["check"]()
            if self.mode == "journal":
                raise K.CatalogError("CUT_CATALOG_RECOVERY_REQUIRED")
            return self.catalog
        stack.enter_context(patch.object(K.CutCatalog, "open", opened))
        return stack

    def extend(self):
        self.selected_allowance = allowance()
        return T.extend(self.runtime, self.target, self.parent_id, self.raw_new, self.custody,
                        self.call, store_id="4" * 64, epoch="5" * 64,
                        budget=Budget(), allowance=self.selected_allowance)

    def resolve(self):
        self.selected_allowance = allowance()
        return T.resolve(self.runtime, self.target, self.call, store_id="4" * 64,
                         epoch="5" * 64, budget=Budget(), allowance=self.selected_allowance)


def controller_controls(output):
    for mode, code in (("good", None), ("lost-reply", "CUT_COMMIT_COMMITTED"),
                       ("sibling", "UNGROUNDED_IMPORT"), ("frontier", "FRONTIER_CHANGED"),
                       ("collision", "GLOBAL_NAME_NOT_FRESH"), ("custody", "CUSTODY_BINDING"),
                       ("withdraw", "SYNTHETIC_SOURCE_WITHDRAWN"), ("uncertain", "SYNTHETIC_UNCERTAIN")):
        scenario = Scenario(output / mode, mode)
        with scenario.patches():
            result = scenario.extend() if code is None else refusal(code, scenario.extend)
            need(scenario.closed, "CONTROLLER_MUST_CLOSE")
            if mode in ("good", "lost-reply"):
                need(scenario.commits == 1 and len(scenario.inserts) == 1, "CONTROLLER_SINGLE_COMMIT")
                resolved = scenario.resolve()
                need(resolved["disposition"] == "COMMITTED" and resolved["reexecuted"] is False and
                     scenario.worker_calls == 1 and scenario.commits == 1, "RESOLUTION_REPLAYED")
                candidate = result["local_root"] if mode == "good" else result.root_id
                need(resolved["local_root"] == candidate, "RESOLVED_DIFFERENT_CANDIDATE")
                if mode == "good":
                    scenario.committed.clear()
                    need(scenario.resolve()["disposition"] == "NOT_COMMITTED" and scenario.worker_calls == 1,
                         "ABSENCE_MUST_NOT_REEXECUTE")
                    scenario.mode = "journal"
                    refusal("RECOVERY_REQUIRED", scenario.resolve)
            else:
                need(scenario.commits == 0 and not scenario.inserts, "FAILED_CONTROLLER_PROMOTED")
                if mode == "uncertain":
                    need((scenario.target / "WITHDRAWN").is_file(), "UNCERTAIN_NOT_QUARANTINED")
        case("controller-" + mode, lambda: None)
    missing = Scenario(output / "missing-intent")
    missing.call.mkdir()
    with missing.patches():
        refusal("CATALOG_MISSING_PATH", missing.resolve)
        need(missing.worker_calls == missing.commits == 0, "MISSING_INTENT_REPLAYED")
    case("controller-missing-intent-refuses", lambda: None)


def runtime_control(output):
    runtime = object.__new__(R.CutRuntime)
    runtime.root = output / "unused-support"
    installation = NS(runtime_roots={"python_runtime": output / "unused-python",
                                    "lean_runtime": output / "unused-lean"},
                      path=lambda role: output / "never-executed.exe", _job_module=NS(Job=object))
    runtime.base = NS(root=output / "unused-base", installation=installation, A=A)
    runtime.manifest_sha = "a" * 64
    def supervise(argv, call, spool, limits, job):
        # Even a plausible saved successful report must not override live cleanup.
        P.PortableCatalog._write_fresh(call / "report.json", b'{"PASS":true}')
        return {"job_closed": False, "direct_child_reaped": True, "cleanup_errors": [],
                "final_job": {"active_processes": 1}}
    installation._supervisor = NS(limits_checked=lambda value: value, supervise=supervise)
    packet = E.canonical_json(dict(schema="DMKN_GROUNDED_CUT_REQUEST_V1", request_id="b" * 64,
                                   concrete_units=[], signature_rows=[], new_unit=[]))
    with patch.object(A, "OperationBudget", Budget), patch.object(R.CutRuntime, "verify", lambda self, callback: callback()):
        refusal("CLEANUP_UNCERTAIN", lambda: runtime.check_packet(packet, output / "runtime-call", Budget()),
                R.UncertainWorker)
    case("runtime-saved-success-cannot-override-live-cleanup", lambda: None)


def loader_controls(modules, source):
    B._graph(modules, A, E, S, C, P, PE)
    with patch.object(K, "A", object()):
        refusal("LOADED_GRAPH_IDENTITY", lambda: B._graph(modules, A, E, S, C, P, PE))
    with patch.object(T, "R", NS(CutRuntime=R.CutRuntime)):
        refusal("LOADED_GRAPH_IDENTITY", lambda: B._graph(modules, A, E, S, C, P, PE))
    case("loader-refuses-mixed-helper-objects", lambda: None)
    case("loader-refuses-preloaded-cut-modules", lambda: refusal("PRELOADED_CUT_MODULE",
        lambda: B.load(source / "grounded_cut", "a" * 64, NS(), check=check)))
    case("loader-refuses-replacement-base-admission", lambda: refusal("BASE_ADMISSION_MODULE",
        lambda: B._base(NS(A=ModuleType("ordinary_admission")), check)))


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source, output = Path(args.source_root), Path(args.output)
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTROL_PROCESS")
    need(source.is_absolute() and source.resolve().is_relative_to(ROOT) and
         output.is_absolute() and output.resolve().is_relative_to(ROOT / "experiments") and
         not output.is_relative_to(source) and not source.is_relative_to(output) and
         output.parent.is_dir() and not os.path.lexists(output), "CONTROL_PATHS")
    loaded, pins = {}, {}
    names = ("ordinary_evidence", "ordinary_semantics", "portable_evidence", "local_catalog",
             "portable_catalog", "ordinary_admission", "cut_map", "cut_summary", "source_anchor",
             "cut_catalog", "cut_runtime", "cut_controller", "cut_bootstrap")
    for index, identifier in enumerate(names):
        check()
        relative = ("ordinary_lean/" if index < 6 else "grounded_cut/") + identifier + ".py"
        loaded[identifier], pins[relative] = module(identifier, source / relative)
    globals().update(E=loaded[names[0]], S=loaded[names[1]], PE=loaded[names[2]], C=loaded[names[3]],
                     P=loaded[names[4]], A=loaded[names[5]], M=loaded[names[6]], Q=loaded[names[7]],
                     H=loaded[names[8]], K=loaded[names[9]], R=loaded[names[10]], T=loaded[names[11]],
                     B=loaded[names[12]])
    C.ordinary(source, directory=True)
    C.ordinary(output, directory=True, fresh=True)
    output.mkdir()
    map_controls(output)
    summary_controls()
    controller_controls(output)
    runtime_control(output)
    loader_controls(loaded, source)
    check()
    report = {"schema": "DMKN_GROUNDED_CUT_NATIVE_FREE_CONTROLS_V1", "cases": CASES,
              "count": len(CASES), "source_pins": pins, "native_runs": 0,
              "mathematical_acceptance": False, "protected_stores_opened": 0,
              "wall_seconds": time.monotonic() - START, "cpu_seconds": time.process_time() - CPU}
    P.PortableCatalog._write_fresh(output / "result.json", json.dumps(report, sort_keys=True).encode())
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()

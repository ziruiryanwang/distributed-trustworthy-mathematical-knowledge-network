"""Focused inert handoff controls: real codecs, custody SQLite and bundle bytes.

SOURCE ONLY until root selects a fresh finite run. All claims are synthetic and
unchecked. No existing mathematical catalog/custody, Lean, network or subprocess
is used. The cycle defense uses one explicitly corrupted-parser test double.
"""
from __future__ import annotations

import argparse
import asyncio
from contextlib import ExitStack, redirect_stdout
from copy import deepcopy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import ssl
import stat
import subprocess
import sys
import time
from types import SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PROFILE = "9c41b9a3fe36f7283af130ac6ef290e82c2a78c432980b2bea75ccdcf197a6d4"
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()
CASES, FORBIDDEN = [], []


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 60 and time.process_time()-CPU < 30,
         "RETURN_CONTROLS_ORIGINAL_ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def refusal(code, action):
    check()
    try:
        action()
    except ValueError as error:
        need(code in str(error), "WRONG_REFUSAL:" + code + ":" + str(error))
        return
    raise AssertionError("MISSING_REFUSAL:" + code)


def case(label, action):
    check()
    action()
    CASES.append(label)


def forbidden(*args, **kwargs):
    FORBIDDEN.append("UNEXPECTED_EXTERNAL_OPERATION")
    raise AssertionError(FORBIDDEN[-1])


def module(name, path):
    need(name not in sys.modules and path.is_absolute() and ".." not in path.parts,
         "CONTROL_SOURCE_PATH")
    for item in (*reversed(path.parents), path):
        info = item.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             (getattr(info, "st_file_attributes", 0) & 0x400), "CONTROL_SOURCE_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if item != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "CONTROL_SOURCE_KIND")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB, "CONTROL_SOURCE_BOUND")
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    exec(compile(raw, str(path), "exec", dont_inherit=True), value.__dict__)
    return value, {"bytes": len(raw), "sha256": sha(raw)}


def name(text):
    return [[0, {"$bytes": list(text.encode("ascii"))}]]


def claim(text, imports=()):
    """Valid inert grammar, not asserted to be a well-typed Lean declaration."""
    own = name(text)
    sort = [E.EXPR_FORMAT, [[0]], [[1, 0]], 0]
    nodes = [[2, encoded, []] for encoded, _ in imports]
    if not nodes:
        proof = sort
    else:
        for index in range(1, len(imports)):
            nodes.append([3, 0 if index == 1 else len(nodes)-1, index])
        proof = [E.EXPR_FORMAT, [], nodes, len(nodes)-1]
    unit = [E.UNIT_FORMAT, [1, own, [], sort, proof, [own]],
            [[own, 2, [], sort, [proof, [own]]]]]
    return E.canonical_json({"schema": PE.SCHEMA, "semantic_id": S.semantic_id(),
        "imports": sorted([list(row) for row in imports], key=lambda row: E.name_key(row[0])),
        "unit": unit})


def group():
    own, constructor = name("ReturnGroup"), name("ReturnConstructor")
    sort = [E.EXPR_FORMAT, [[0]], [[1, 0]], 0]
    unit = [E.UNIT_FORMAT, [3, [], 0, [[own, sort, [[constructor, sort]]]]],
            [[own, 4, [], sort, [0, 0, [own], [constructor], 0, 0, 0, 0]],
             [constructor, 5, [], sort, [own, 0, 0, 0, 0]]]]
    return E.canonical_json({"schema": PE.SCHEMA, "semantic_id": S.semantic_id(),
                             "imports": [], "unit": unit})


def export(raw, index=0):
    item = PE.read_evidence(raw)
    return S.export_id(S.semantic_id(), item.unit_id, item.document["unit"][2][index][0])


class Scenario:
    def __init__(self, label, raws):
        self.root = OUTPUT / label
        self.root.mkdir()
        self.output = self.root / "bundle"
        self.custody_root = self.root / "custody"
        self.limits = {"objects": 100, "exports": 100, "logical_bytes": MIB, "db_pages": 256}
        self.store = O.OrdinaryStore(self.custody_root, S.semantic_id(), self.limits, create=True)
        for raw in raws:
            self.store.put_evidence(raw, before_commit=check)
        self.reads, self.sql = [], []
        self.store.db.set_trace_callback(self.sql.append)

    def run(self, targets, policy="selected-units", limits=None, callback=check):
        original_locator, original_evidence = self.store.get_locator, self.store.get_evidence
        def locator(semantic, identity, maximum, *, check_budget):
            self.reads.append(("locator", identity, maximum))
            return original_locator(semantic, identity, maximum, check_budget=check_budget)
        def evidence(semantic, identity, maximum, *, check_budget):
            self.reads.append(("evidence", identity, maximum))
            return original_evidence(semantic, identity, maximum, check_budget=check_budget)
        with patch.object(self.store, "get_locator", locator), patch.object(self.store, "get_evidence", evidence):
            return R.write_bundle(LOADED, self.store, targets, policy=policy, output=self.output,
                                  limits=limits or R.Limits(), check=callback)

    def close(self):
        self.store.close()

    def evidence_reads(self):
        return [identity for kind, identity, _ in self.reads if kind == "evidence"]

    def manifest(self, result):
        raw = (self.output / "manifest.json").read_bytes()
        manifest = B.read_manifest(raw, result["bundle_manifest_sha256"])
        rows = [entry for batch in manifest.batches for entry in batch]
        return rows, E.strict_json((self.output / "obligations.json").read_bytes())


def with_scenario(label, raws, action):
    scenario = Scenario(label, raws)
    try:
        action(scenario)
    finally:
        scenario.close()


def controls(raw_a, raw_b, raw_c):
    chain = (raw_a, raw_b, raw_c)
    ids = [PE.read_evidence(raw).unit_id for raw in chain]
    def selected(s):
        before = (s.custody_root / "ordinary.sqlite").read_bytes()
        result = s.run([export(raw_c)])
        rows, obligations = s.manifest(result)
        need([entry.unit_id for entry in rows] == [ids[2]] and
             (s.output / rows[0].relative_path).read_bytes() == raw_c and
             obligations["receiver_parent"] == [[name("ReturnB"), export(raw_b)]] and
             not obligations["fixed_basis"] and s.evidence_reads() == [ids[2]] and
             result["mathematical_acceptance"] is False and
             (s.custody_root / "ordinary.sqlite").read_bytes() == before,
             "SELECTED_EXACT_BYTES_OR_ANCESTRY_OR_MUTATION")
    case("selected-only-exact-bytes-obligations-no-custody-write",
         lambda: with_scenario("selected", chain, selected))

    def closed(s):
        result = s.run([export(raw_c)], "closed-basis")
        rows, obligations = s.manifest(result)
        need([entry.unit_id for entry in rows] == ids and not obligations["receiver_parent"] and
             obligations["fixed_basis"] == [[BASIS_NAME, BASIS_SYMBOL]] and
             s.evidence_reads() == list(reversed(ids)), "CLOSED_TOPOLOGICAL_FULL_PROOF_IMPORTS")
        need(all((s.output / row.relative_path).read_bytes() == raw for row, raw in zip(rows, chain)),
             "CLOSED_EXACT_UNIT_BYTES")
    case("closed-basis-exact-bytes-and-topological-order", lambda: with_scenario("closed", chain, closed))

    def reordered(s):
        result = s.run([export(raw_c), export(raw_a), export(raw_b)])
        rows, obligations = s.manifest(result)
        need([row.unit_id for row in rows] == ids and not obligations["receiver_parent"] and
             len(s.evidence_reads()) == 3, "SELECTED_TOPOLOGICAL_REORDER")
    case("selected-target-order-does-not-become-dependency-order",
         lambda: with_scenario("reordered", chain, reordered))

    raw_group = group()
    def whole(s):
        result = s.run([export(raw_group, 1), export(raw_group, 0)])
        rows, obligations = s.manifest(result)
        need(len(rows) == 1 and len(obligations["targets"]) == 2 and
             len(s.reads) == 2 and (s.output / rows[0].relative_path).read_bytes() == raw_group,
             "GENERATED_GROUP_SPLIT_OR_REFETCH")
    case("whole-generated-group-two-targets-one-acquisition",
         lambda: with_scenario("whole-group", (raw_group,), whole))

    def fail(s, code, targets=None, **kwargs):
        refusal(code, lambda: s.run(targets or [export(raw_c)], **kwargs))
        need(not (s.output / "manifest.json").exists(), "FAILED_HANDOFF_ADVERTISED_MANIFEST")
    case("selected-succeeds-with-unavailable-ancestor",
         lambda: with_scenario("selected-no-parent", (raw_c,), selected))
    case("closed-refuses-unavailable-ancestor-no-fallback",
         lambda: with_scenario("closed-no-parent", (raw_c,),
             lambda s: fail(s, "ORDINARY_EXPORT_LOCALLY_UNAVAILABLE", policy="closed-basis")))
    case("absent-exact-target-locator", lambda: with_scenario("absent", chain,
        lambda s: fail(s, "ORDINARY_EXPORT_LOCALLY_UNAVAILABLE", targets=["f"*64])))

    def bad_locator(s):
        row = s.store.db.execute("SELECT locator FROM exports WHERE export_id=?", (export(raw_c),)).fetchone()
        locator = E.strict_json(bytes(row[0]))
        locator["unit_id"] = "e"*64
        s.store.db.execute("UPDATE exports SET locator=? WHERE export_id=?",
                           (E.canonical_json(locator), export(raw_c)))
        fail(s, "ORDINARY_CUSTODY_EXPORT_BINDING")
        need(not s.evidence_reads(), "CORRUPT_LOCATOR_REACHED_EVIDENCE")
    case("corrupt-locator-stops-before-evidence", lambda: with_scenario("bad-locator", chain, bad_locator))

    def absent_output(s):
        uid, fake = ids[2], name("NotGenerated")
        identity = S.export_id(S.semantic_id(), uid, fake)
        locator = E.canonical_json(dict(schema=R.PP.LOCATOR_SCHEMA, semantic_id=S.semantic_id(),
                                       unit_id=uid, export_name=fake))
        s.store.db.execute("INSERT INTO exports VALUES(?,?,?)", (identity, uid, locator))
        fail(s, "LOCATOR_OUTPUT_ABSENT", targets=[identity])
    case("self-consistent-locator-for-absent-generated-output",
         lambda: with_scenario("absent-output", chain, absent_output))

    def bad_evidence(s):
        s.store.db.execute("UPDATE objects SET raw=? WHERE kind='evidence' AND identity=?", (raw_c+b" ", ids[2]))
        fail(s, "ORDINARY_CUSTODY_EXACT_BINDING")
    case("corrupt-selected-proof-bytes", lambda: with_scenario("bad-evidence", chain, bad_evidence))

    conflict = claim("ReturnA")
    case("conflicting-exact-name-versions", lambda: with_scenario("conflict", (raw_a, conflict),
        lambda s: fail(s, "CONFLICTING_NAME_BINDING", targets=[export(raw_a), export(conflict)])))
    bad_basis = claim("UsesWrongBasis", [(BASIS_NAME, "d"*64)])
    case("fixed-basis-import-identity-not-waived", lambda: with_scenario("bad-basis", (bad_basis,),
        lambda s: fail(s, "FIXED_BASIS_BINDING", targets=[export(bad_basis)])))

    def byte_limit(s):
        fail(s, "ORDINARY_CUSTODY_OBJECT_BOUND", policy="closed-basis",
             limits=R.Limits(max_bytes=len(raw_c)+len(raw_b)-1))
        reads = [row for row in s.reads if row[0] == "evidence"]
        need(len(reads) == 2 and reads[1][2] == len(raw_b)-1 and
             sum(sql.startswith("SELECT raw FROM objects") for sql in s.sql) == 1,
             "REMAINING_BYTE_BOUND_NOT_BEFORE_MATERIALIZATION")
    case("aggregate-byte-room-precedes-next-blob", lambda: with_scenario("byte-bound", chain, byte_limit))
    case("whole-unit-count-bound", lambda: with_scenario("unit-bound", chain,
        lambda s: fail(s, "ACQUISITION_BOUND", policy="closed-basis", limits=R.Limits(max_units=1))))
    case("parsed-node-bound", lambda: with_scenario("node-bound", chain,
        lambda s: fail(s, "UNIT_NODE_BOUND", limits=R.Limits(max_nodes=1))))
    two_imports = claim("TwoImports", [(name("ReturnA"), export(raw_a)), (name("ReturnB"), export(raw_b))])
    case("import-edge-bound", lambda: with_scenario("edge-bound", (two_imports,),
        lambda s: fail(s, "ARRAY_BOUND", targets=[export(two_imports)], limits=R.Limits(max_edges=1))))
    case("distinct-name-bound-includes-import-obligation", lambda: with_scenario("name-bound", chain,
        lambda s: fail(s, "DISTINCT_NAME_OR_BINDING_BOUND", limits=R.Limits(max_names=1))))
    case("locator-byte-bound-before-materialization", lambda: with_scenario("locator-bound", chain,
        lambda s: fail(s, "ORDINARY_LOCATOR_BYTES", limits=R.Limits(max_binding_bytes=1))))
    case("duplicate-targets-refuse-before-output", lambda: with_scenario("duplicates", chain,
        lambda s: fail(s, "DUPLICATE_TARGET", targets=[export(raw_c), export(raw_c)])))

    def original_stop(s):
        retained = s.output / "units" / (ids[2] + ".json")
        def stop():
            check()
            if retained.exists():
                raise ValueError("TEST_ORIGINAL_ALLOCATION_EXHAUSTED")
        fail(s, "TEST_ORIGINAL_ALLOCATION_EXHAUSTED", policy="closed-basis", callback=stop)
        need(len(s.evidence_reads()) == 1 and retained.read_bytes() == raw_c,
             "BUDGET_RENEWED_OR_PARTIAL_OUTPUT_LOST")
    case("original-budget-stop-has-no-retry", lambda: with_scenario("budget-stop", chain, original_stop))

    # A true content-hash cycle needs a hash fixed point, not an ordinary fixture.
    # Inject inconsistent parsed imports AFTER real parsing solely to exercise
    # the graph's defensive refusal; do not claim these are byte-valid cycles.
    cyclic_a = claim("CycleA", [(name("CycleB"), "0"*64)])
    cyclic_b = claim("CycleB", [(name("CycleA"), "0"*64)])
    cycle_ids = (export(cyclic_a), export(cyclic_b))
    def cycle(s):
        original = PE.read_evidence
        def corrupt_parser(raw, *args, **kwargs):
            item = original(raw, *args, **kwargs)
            doc = deepcopy(item.document)
            doc["imports"][0][1] = cycle_ids[1 if raw == cyclic_a else 0]
            return PE.Evidence(item.raw, doc, item.unit_id, item.census)
        with patch.object(PE, "read_evidence", corrupt_parser):
            fail(s, "DEPENDENCY_CYCLE", targets=list(cycle_ids))
    case("cycle-defense-corrupted-parser-double-not-valid-hash-cycle",
         lambda: with_scenario("cycle", (cyclic_a, cyclic_b), cycle))


def cli_controls(source, package, runtimes, pins, raw):
    """Real command path after a disclosed already-loaded-profile seam double.

    The real bootstrap/profile loader was exercised once in main. It cannot be
    loaded again in this process because its preloaded-module guard is correct.
    This double returns that same namespace; all subsequent command logic and
    helper hash loading, config parsing, store open and bundle writing are real.
    """
    scenario = Scenario("public-command", (raw,))
    scenario.close()
    args = ["return_bundle.py", "--package", str(package), "--profile-sha256", PROFILE,
        "--helper-sha256", pins["custody_return.py"]["sha256"],
        "--python-runtime", str(runtimes["python_runtime"]), "--lean-runtime", str(runtimes["lean_runtime"]),
        "--custody", str(scenario.custody_root), "--policy", "selected-units",
        "--wall-seconds", "60", "--cpu-seconds", "30", "--approve-local-custody"]
    for flag, value in (("custody-limits", scenario.limits), ("targets", [export(raw)])):
        encoded = E.canonical_json(value)
        path = scenario.root / (flag + ".json")
        R._write(path, encoded, MIB, check)
        args += ["--"+flag, str(path), "--"+flag+"-sha256", sha(encoded)]
    loader = NS(load=lambda *args, **kwargs: LOADED)
    owner = NS(bootstrap=lambda *args: loader)
    def run(label, code=None, replacements=()):
        selected = args + ["--output", str(scenario.root / label)]
        for flag, value in replacements:
            selected[selected.index(flag)+1] = value
        capture = io.StringIO()
        with patch.object(CMD, "_owner", lambda *args: owner), patch.object(sys, "argv", selected), \
                patch.dict(sys.modules), redirect_stdout(capture):
            if code:
                with patch.object(O, "OrdinaryStore", forbidden):
                    refusal(code, CMD.main)
            else:
                need(CMD.main() == 0, "CLI_NONZERO")
        if not code:
            result = json.loads(capture.getvalue())
            need(result["mathematical_acceptance"] is False and
                 result["status"] == "INERT_BUNDLE_WRITTEN" and
                 result["custody_open"] == "READ_WRITE_HANDLE_PRAGMAS_NO_LOGICAL_WRITES" and
                 Path(result["bundle_manifest"]).is_file(), "CLI_RESULT")
    case("cli-main-real-config-store-output-with-reused-loader-double", lambda: run("success"))
    case("cli-helper-pin-before-custody-open", lambda: run("helper-pin", "HELPER_PIN",
        (("--helper-sha256", "0"*64),)))
    case("cli-input-pin-before-custody-open", lambda: run("input-pin", "INPUT_PIN",
        (("--targets-sha256", "0"*64),)))
    journal = scenario.custody_root / "ordinary.sqlite-journal"
    R._write(journal, b"inert-synthetic-sidecar", 64, check)
    case("cli-preexisting-journal-refuses-before-store-open",
         lambda: run("sidecar", "CUSTODY_SIDECAR_REQUIRES_OWNER_RECOVERY"))


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for arg in ("source-root", "package", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+arg, required=True)
    args = parser.parse_args()
    source, package, output = Path(args.source_root), Path(args.package), Path(args.output)
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTROL_PROCESS")
    need(source.is_absolute() and source.resolve().is_relative_to(ROOT) and
         package.is_absolute() and package.resolve().is_relative_to(ROOT) and
         output.is_absolute() and output.resolve().is_relative_to(ROOT / "experiments") and
         output.parent.is_dir() and not os.path.lexists(output) and
         not output.is_relative_to(source) and not source.is_relative_to(output) and
         not output.is_relative_to(package) and not package.is_relative_to(output), "CONTROL_PATHS")
    command, command_pin = module("_return_controls_command", source / "return_bundle.py")
    runtimes = {"python_runtime": Path(args.python_runtime), "lean_runtime": Path(args.lean_runtime)}
    pins = {"return_bundle.py": command_pin}
    # Standard asyncio/SSL types are imported before replacing socket.socket:
    # their import-time class definitions must not inherit a test function.
    # No source project build or subprocess is even available to this suite.
    with ExitStack() as stack:
        stack.enter_context(patch.object(subprocess, "Popen", forbidden))
        stack.enter_context(patch.object(socket, "socket", forbidden))
        case("cli-bootstrap-rejects-wrong-profile-hash",
             lambda: refusal("PROFILE_PIN", lambda: command._owner(package, "0"*64, check)))
        owner = command._owner(package, PROFILE, check)
        loader = owner.bootstrap(package, PROFILE, check)
        loaded = loader.load(package, PROFILE, runtimes, START+60, check_parent=check)
        helper, pins["custody_return.py"] = module("_return_controls_helper", source / "custody_return.py")
        globals().update(CMD=command, R=helper, LOADED=loaded, A=loaded.A, O=loaded.O,
                         E=loaded.A.E, S=loaded.A.S, PE=loaded.A.PE, B=helper.B, OUTPUT=output)
        stack.enter_context(patch.object(A.OrdinaryAdmission, "open", forbidden))
        stack.enter_context(patch.object(A.P.PortableCatalog, "open", forbidden))
        stack.enter_context(patch.object(A.C.LocalCatalog, "open", forbidden))
        A.C.ordinary(source, directory=True)
        A.C.ordinary(output, directory=True, fresh=True)
        output.mkdir()
        case("actual-pinned-owner-and-complete-ordinary-profile-loader", lambda: None)
        inventory = A._writer_json(loaded.installation.read("inventory", MIB), MIB)
        basis_name = inventory[0][0]
        basis_symbol = S.basis_symbol_id(S.semantic_id(), S.foundation_id(), basis_name)
        globals().update(BASIS_NAME=basis_name, BASIS_SYMBOL=basis_symbol)
        raw_a = claim("ReturnA", [(basis_name, basis_symbol)])
        raw_b = claim("ReturnB", [(name("ReturnA"), export(raw_a))])
        raw_c = claim("ReturnC", [(name("ReturnB"), export(raw_b))])
        controls(raw_a, raw_b, raw_c)
        cli_controls(source, package, runtimes, pins, raw_c)
        need(not FORBIDDEN, "FORBIDDEN_CALL_RECORDED")
        check()
        report = {"schema": "DMKN_ORDINARY_RETURN_NATIVE_FREE_CONTROLS_V1", "cases": CASES,
            "count": len(CASES), "source_pins": pins, "profile_sha256": PROFILE,
            "native_runs": 0, "protected_mathematical_stores_opened": 0,
            "mathematical_acceptance": False, "synthetic_claims_unchecked": True,
            "cycle_control": "CORRUPTED_PARSER_DOUBLE_NOT_BYTE_VALID_CYCLE",
            "cli_main_loader": "REUSES_NAMESPACE_AFTER_SEPARATE_ACTUAL_PROFILE_LOAD",
            "wall_seconds": time.monotonic()-START, "cpu_seconds": time.process_time()-CPU}
        R._write(output / "result.json", json.dumps(report, sort_keys=True).encode(), MIB, check)
        print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()

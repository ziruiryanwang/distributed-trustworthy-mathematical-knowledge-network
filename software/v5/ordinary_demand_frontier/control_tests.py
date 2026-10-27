"""Finite native-free controls for optional scratch-authoring frontier.

Source only until separately selected by root. Synthetic declarations and context
dictionaries are NOT mathematical evidence or catalog warrants. The unchanged
frozen package supplies the V2 oracle and real pure parsers. No native process,
owner, custody, database, peer or network operation is permitted.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
from contextlib import ExitStack
import copy
from dataclasses import asdict
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import sqlite3
import stat
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import patch

MIB = 1024**2
PROFILE = "60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b"
SOURCE_PINS = {
    "owner.py": "b6091c27a36cd1906785f99f0364a04184007cd4017288de84b763896944a927",
    "ordinary_contribution.py": "67962af468d9d8ef8c0d8b48d95b29e31c1112a519b944c96058df1efc1449f4",
    "portable_owner_request.py": "7b0d262b340f2d4422675f546002db95cab48ac6e9c8b8360ff699d371609f22",
    "retained_preparation.py": "ad8f35652a970e73387918d551b97d73c2ded0ae0db386bd526840b7c905ec1a",
}
PARENT, FRONTIER = "a"*64, "b"*64
FORBIDDEN = []


def need(value, code):
    if not value:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START_WALL < 50 and time.process_time()-START_CPU < 30,
         "FRONTIER_CONTROL_ORIGINAL_ALLOWANCE")


def forbidden(label):
    def refuse(*_, **__):
        FORBIDDEN.append(label)
        raise AssertionError("FRONTIER_CONTROL_FORBIDDEN:"+label)
    return refuse


def read(path, maximum=2*MIB):
    check()
    need(path.is_absolute() and ".." not in path.parts, "CONTROL_ABSOLUTE_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "CONTROL_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "CONTROL_REGULAR")
    size = path.stat().st_size
    need(0 < size <= maximum, "CONTROL_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "CONTROL_READ_CHANGED")
    return raw


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def load_source(name, path, pin):
    raw = read(path)
    need(digest(raw) == pin and name not in sys.modules, "CONTROL_SOURCE_PIN:"+name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def load_selected(args):
    package = Path(args.package)
    profile_raw = read(package/"PROFILE.json")
    need(args.profile_sha256 == PROFILE and digest(profile_raw) == PROFILE, "CONTROL_PROFILE_PIN")
    descriptor = json.loads(profile_raw)
    old_owner = load_source("_frontier_old_owner", package/"owner.py",
                            descriptor["files"]["owner.py"]["sha256"])
    loader = old_owner.bootstrap(package, PROFILE, check)
    loaded = loader.load(package, PROFILE,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        START_WALL+50, check_parent=check)
    old_r, old_retained = sys.modules["portable_owner_request"], sys.modules["retained_preparation"]
    source = Path(args.source_directory)
    request = load_source("_frontier_new_request", source/"portable_owner_request.py",
                          SOURCE_PINS["portable_owner_request.py"])
    with patch.dict(sys.modules, {"portable_owner_request": request}):
        contribution = load_source("_frontier_new_contribution", source/"ordinary_contribution.py",
                                   SOURCE_PINS["ordinary_contribution.py"])
        retained = load_source("_frontier_new_retained", source/"retained_preparation.py",
                               SOURCE_PINS["retained_preparation.py"])
    owner = load_source("_frontier_new_owner", source/"owner.py", SOURCE_PINS["owner.py"])
    need(contribution.R is request and retained.R is request and old_r is not request,
         "CONTROL_SUCCESSOR_IMPORT_BINDING")
    return loaded, SimpleNamespace(R=request, G=contribution, T=retained, O=owner,
                                   old_R=old_r, old_T=old_retained)


def refuses(code, action):
    check()
    try:
        action()
    except ValueError as error:
        need(str(error) == code, "CONTROL_WRONG_REFUSAL:"+str(error)+" expected="+code)
        return
    raise AssertionError("CONTROL_MISSING_REFUSAL:"+code)


def name(text):
    return [[0, {"$bytes": list(text.encode("utf-8"))}]]


class Fixtures:
    def __init__(self, loaded, lane, inventory_raw):
        self.E, self.S, self.PE = loaded.A.E, loaded.A.S, loaded.A.PE
        self.lane, self.inventory_raw = lane, inventory_raw
        self.s, self.f = self.S.semantic_id(), self.S.foundation_id()
        need(digest(inventory_raw) == self.S.INVENTORY, "CONTROL_INVENTORY_PIN")
        self.basis = {self.E.name_key(row[0]): self.S.basis_symbol_id(self.s, self.f, row[0])
                      for row in json.loads(inventory_raw)}
        self.parent, self.raws, self.ids = dict(self.basis), {}, {}
        self.add("Leaf")
        self.add("SecondLeaf")
        self.add("Above", ("Leaf",))
        self.add("TwoCuts", ("SecondLeaf", "Leaf"))
        self.add("Theorem", ("Leaf",), theorem=True)

    def add(self, text, dependencies=(), *, theorem=False):
        E, S = self.E, self.S
        own, typ = name(text), name("True" if theorem else "Nat")
        type_dag = [E.EXPR_FORMAT, [], [[2, typ, []]], 0]
        nodes = [[2, name(dep), []] for dep in dependencies]
        if nodes:
            root = 0
            for index in range(1, len(nodes)):
                nodes.append([3, root, index]); root = len(nodes)-1
        else:
            nodes, root = [[7, {"$bytes": []}]], 0
        value = [E.EXPR_FORMAT, [], nodes, root]
        if theorem:
            unit = [E.UNIT_FORMAT, [1, own, [], type_dag, value, [own]],
                    [[own, 2, [], type_dag, [value, [own]]]]]
        else:
            unit = [E.UNIT_FORMAT, [0, own, [], type_dag, value, [2, 1], [own]],
                    [[own, 1, [], type_dag, [value, [2, 1], [own]]]]]
        imports = [[typ, self.basis[E.name_key(typ)]]]
        imports += [[name(dep), self.parent[E.name_key(name(dep))]] for dep in dependencies]
        imports.sort(key=lambda row: E.name_key(row[0]))
        raw = E.canonical_json({"schema": self.PE.SCHEMA, "semantic_id": self.s,
                                "imports": imports, "unit": unit})
        evidence = self.PE.read_evidence(raw)
        key = E.name_key(own)
        self.parent[key] = S.export_id(self.s, evidence.unit_id, own)
        self.raws[key], self.ids[key] = raw, evidence.unit_id

    def target(self, text):
        key = self.E.name_key(name(text))
        return [name(text), self.parent[key]]

    def triple(self, text):
        key = self.E.name_key(name(text))
        return {"name": name(text), "export_id": self.parent[key], "unit_id": self.ids[key]}

    def prepare(self, text="Above", *, module=None, cuts=None, overrides=None):
        R, E = module or self.lane.R, self.E
        fetched, looked_up = [], []
        cut_map = {} if cuts is None else {E.name_key(name(t)): self.parent[E.name_key(name(t))]
                                          for t in cuts}
        def warrant(n):
            key = E.name_key(n); looked_up.append(key)
            return self.parent.get(key)
        def fetch(n, identity):
            key = E.name_key(n)
            need(key not in cut_map, "CONTROL_FRONTIER_EVIDENCE_FETCH")
            need(self.parent[key] == identity, "CONTROL_FETCH_ID")
            fetched.append(key)
            return self.raws[key]
        params = dict(semantic_id=self.s, foundation_id=self.f, context_root=PARENT,
            inventory_raw=self.inventory_raw, targets=[self.target(text)],
            warranted_symbol=warrant, fetch_evidence=fetch, owner_absent=lambda _: True)
        if cuts is not None:
            params.update(frontier_root=FRONTIER, frontier_symbol=lambda n: cut_map.get(E.name_key(n)))
        params.update(overrides or {})
        result = R.prepare(**params)
        return result, fetched, looked_up

    def retained(self, prepared, *, module=None, header_change=None, request_change=None,
                 groups_change=None, parent=None):
        E, T = self.E, module or self.lane.T
        header = E.strict_json(prepared.header)
        if header_change:
            header_change(header)
        header_raw = E.canonical_json(header)
        groups = list(prepared.groups)
        if groups_change:
            groups_change(groups)
        groups = tuple(groups)
        outputs = [name("Output")]
        targets_raw = E.canonical_json(outputs)
        pin = lambda raw: {"bytes": len(raw), "sha256": digest(raw)}
        pins = {"header.json": pin(header_raw)}
        pins.update({f"group-{i:05d}.json": pin(raw) for i, raw in enumerate(groups)})
        metadata = {"parent_root": PARENT, "acquired_targets": [], "output_names": outputs,
            "output_targets": pin(targets_raw), "request_files": pins, "groups": len(groups),
            "fetched": [], "payload_bytes": len(header_raw)+sum(map(len, groups)),
            "acquired_bytes": prepared.acquired_bytes, "source_body_sha256": "c"*64,
            "generated_source": pin(b"-- synthetic controller metadata\n"),
            "authoring_profile": {}, "mathematical_acceptance": False}
        if header.get("schema") == "DMKN_OWNER_REQUEST_V3":
            metadata["project_authoring"] = {"frontier_root": FRONTIER}
        if request_change:
            request_change(metadata)
        request_raw = json.dumps(metadata, sort_keys=True, separators=(",", ":")).encode("ascii")
        result = T.reconstruct_preparation(request_raw, header_raw, groups, targets_raw,
            semantic_id=self.s, foundation_id=self.f, context_root=PARENT,
            warranted_symbol=lambda n: (self.parent if parent is None else parent).get(E.name_key(n)),
            check_budget=check)
        return asdict(result)


def controls(loaded, lane, fixture, args):
    E, R, G = fixture.E, lane.R, lane.G

    def v2_differential():
        for text in ("Above", "Theorem", "Eq"):
            old = fixture.prepare(text, module=lane.old_R)
            new = fixture.prepare(text)
            need(asdict(old[0]) == asdict(new[0]) and old[1:] == new[1:], "CONTROL_V2_DIFFERENTIAL")
            need(fixture.retained(old[0], module=lane.old_T) == fixture.retained(new[0]),
                 "CONTROL_V2_RETAINED_DIFFERENTIAL")
        need(fixture.prepare("Theorem")[1] == [E.name_key(name("Theorem"))],
             "CONTROL_THEOREM_PROOF_ANCESTRY_OMITTED")
        need(fixture.prepare("Above")[1] == [E.name_key(name("Above")), E.name_key(name("Leaf"))],
             "CONTROL_V2_DEFINITION_BODY_RETAINED")

    def cut_and_exact_targets():
        prepared, fetched, _ = fixture.prepare(cuts=("Leaf",))
        header = E.strict_json(prepared.header)
        need(len(header) == 9 and header["schema"] == R.FRONTIER_REQUEST_FORMAT and
             header["frontier_root"] == FRONTIER and header["frontier_labels"] == [fixture.target("Leaf")]
             and fetched == [E.name_key(name("Above"))] and len(prepared.groups) == 1,
             "CONTROL_REACHED_CUT_ONLY")
        direct = fixture.prepare("Leaf", cuts=("Leaf",))[0]
        need(not direct.groups and direct.acquired_bytes == 0, "CONTROL_DIRECT_FRONTIER_TARGET")
        empty = fixture.prepare("Eq", cuts=())[0]
        need(E.strict_json(empty.header)["frontier_labels"] == [] and not empty.groups,
             "CONTROL_EMPTY_REACHED_FRONTIER")
        for field in ("unit_id", "export_id"):
            wrong = fixture.triple("Above"); wrong[field] = "f"*64
            refuses("CONTRIBUTION_ACQUIRED_EXPORT_BINDING", lambda wrong=wrong: G._acquired(fixture.s, [wrong]))
        good = fixture.triple("Above")
        need(G.request_targets(fixture.s, [good], lambda n: fixture.parent.get(E.name_key(n))) ==
             [fixture.target("Above")], "CONTROL_ACQUIRED_TRIPLE")
        refuses("CONTRIBUTION_TARGET_NOT_WARRANTED",
            lambda: G.request_targets(fixture.s, [good], lambda _: None))
        refuses("REQUEST_FRONTIER_ID_MISMATCH", lambda: fixture.prepare(cuts=("Leaf",),
            overrides={"frontier_symbol": lambda n: "f"*64 if n == name("Leaf") else None}))
        refuses("REQUEST_UNWARRANTED_NAME", lambda: fixture.prepare(cuts=("Leaf",),
            overrides={"warranted_symbol": lambda n: None if n == name("Leaf") else
                       fixture.parent.get(E.name_key(n))}))
        refuses("REQUEST_WARRANTED_ID_MISMATCH", lambda: fixture.prepare(cuts=("Leaf",),
            overrides={"targets": [[name("Above"), "f"*64]]}))

    def prefix_predicate():
        modules = [{"root": "1"*64, "artifact_bytes": 10}, {"root": "2"*64, "artifact_bytes": 20}]
        parent = dict(local_root=PARENT, semantic_id=fixture.s, foundation_id=fixture.f,
                      implementation_id="3"*64, basis_root="4"*64, modules=modules)
        ancestor = dict(parent, local_root=FRONTIER, modules=modules[:1])
        calls = []
        def check_count():
            check(); calls.append(1)
        G._require_frontier_prefix(parent, ancestor, PARENT, FRONTIER, check_count)
        need(len(calls) == 3, "CONTROL_PREFIX_CHARGED")
        G._require_frontier_prefix(parent, parent, PARENT, PARENT, check)
        for field in ("local_root", "semantic_id", "foundation_id", "implementation_id", "basis_root"):
            changed = copy.deepcopy(ancestor); changed[field] = "f"*64
            refuses("CONTRIBUTION_FRONTIER_CONTEXT", lambda changed=changed:
                G._require_frontier_prefix(parent, changed, PARENT, FRONTIER, check))
        for value in ([], list(reversed(modules)), modules+[modules[0]],
                      [dict(modules[0], artifact_bytes=11)], [modules[1]]):
            changed = dict(ancestor, modules=value)
            refuses("CONTRIBUTION_FRONTIER_NOT_ANCESTOR", lambda changed=changed:
                G._require_frontier_prefix(parent, changed, PARENT, FRONTIER, check))

    def cli_scope():
        common = ["--profile-sha256", PROFILE, "--python-runtime", args.python_runtime,
                  "--lean-runtime", args.lean_runtime, "--wall-seconds", "50",
                  "--cpu-seconds", "30", "--memory-mib", "256"]
        state = ["--catalog", "X:\\not-opened-catalog", "--custody", "X:\\not-opened-custody",
                 "--store-id", "d"*64, "--custody-limits", "X:\\not-read-limits.json"]
        def parse(operation, extra):
            with patch.object(sys, "argv", ["owner.py", operation, *common, *extra]):
                return lane.O.arguments()
        def fake_bootstrap(*_, **__):
            return SimpleNamespace(load=lambda *a, **k: loaded)
        with patch.object(lane.O, "bootstrap", fake_bootstrap), \
             patch.object(loaded.A.C, "ordinary", forbidden("cli-state-path")):
            report = lane.O.run(parse("status", state+["--authoring-frontier-root", FRONTIER]))
            need(not report["ok"] and report["error"] == "OWNER_FRONTIER_REQUIRES_PROJECT_CONTRIBUTION",
                 "CONTROL_CLI_NONCONTRIBUTE")
            contribution = state+["--source", "X:\\not-read.lean", "--acquired-targets", "X:\\not-read.json",
                "--output-names", "X:\\not-read-names.json", "--output", "X:\\not-written",
                "--parent-root", PARENT, "--authoring-frontier-root", FRONTIER]
            report = lane.O.run(parse("contribute", contribution))
            need(not report["ok"] and report["error"] == "OWNER_FRONTIER_REQUIRES_PROJECT_CONTRIBUTION",
                 "CONTROL_CLI_NO_PROJECT")
        producer = parse("produce-baseline", ["--authoring-frontier-root", FRONTIER])
        with patch.object(lane.O, "bootstrap", forbidden("producer-bootstrap")):
            report = lane.O.run(producer)
        need(not report["ok"] and report["phase"] == "ARGUMENTS" and
             report["error"] == "PRODUCER_IRRELEVANT_ARGUMENT", "CONTROL_CLI_PRODUCER_REFUSAL")
        need(parse("status", state).authoring_frontier_root is None, "CONTROL_CLI_ABSENT_OPTION")

    def wire_and_limits():
        prepared = fixture.prepare("TwoCuts", cuts=("Leaf", "SecondLeaf"))[0]
        header = E.strict_json(prepared.header)
        need(header["frontier_labels"] == sorted([fixture.target("Leaf"), fixture.target("SecondLeaf")],
             key=lambda row: E.name_key(row[0])), "CONTROL_CANONICAL_FRONTIER_ORDER")
        for overrides in ({"frontier_root": None}, {"frontier_symbol": None}):
            refuses("REQUEST_FRONTIER_CONFIGURATION", lambda overrides=overrides:
                fixture.prepare(cuts=("Leaf",), overrides=overrides))
        refuses("HASH_ENCODING", lambda: fixture.prepare(cuts=("Leaf",), overrides={"frontier_root": "wrong"}))
        for row_limit, ok in ((583, True), (582, False)):
            action = lambda row_limit=row_limit: fixture.prepare(cuts=("Leaf",),
                         overrides={"limits": R.Limits(max_rows=row_limit)})
            if ok:
                action()
            else:
                refuses("REQUEST_SELECTED_NAME_BOUND", action)
        # Observe actual effective Limits construction, not a copy of prepare's
        # branch. Large caller overrides must be clipped; each lower ceiling stays.
        caps = dict(max_groups=32, max_rows=4096, max_targets=32,
                    max_group_bytes=MIB, max_payload_bytes=4*MIB,
                    max_acquired_bytes=4*MIB, max_acquired_nodes=131072, max_edges=32768)
        supplied = R.Limits(**{k: v+1 for k, v in caps.items()})
        captures, original = [], R.Limits.__post_init__
        def capture(value):
            original(value); captures.append(asdict(value))
        with patch.object(R.Limits, "__post_init__", capture):
            fixture.prepare("Eq", cuts=(), overrides={"limits": supplied})
        need(captures == [caps], "CONTROL_CANNOT_ENLARGE_V3_CEILINGS")
        for key, cap in caps.items():
            low = cap-1
            if key == "max_rows":
                low = 581
            supplied = R.Limits(**{**caps, key: low})
            captures.clear()
            with patch.object(R.Limits, "__post_init__", capture):
                fixture.prepare("Eq", cuts=(), overrides={"limits": supplied})
            need(captures == [{**caps, key: low}], "CONTROL_LOWER_CEILING:"+key)
        refuses("ARRAY_BOUND", lambda: fixture.prepare(cuts=(), overrides={
            "targets": [fixture.target("Eq")]*33}))
        # Small real chains exercise the fixed group cap without a large corpus.
        for i in range(33):
            fixture.add("Chain"+str(i), () if i == 0 else ("Chain"+str(i-1),))
        need(len(fixture.prepare("Chain31", cuts=())[0].groups) == 32, "CONTROL_GROUP_CAP_EDGE")
        refuses("REQUEST_GROUP_BOUND", lambda: fixture.prepare("Chain32", cuts=()))
        ordinary = fixture.prepare(cuts=("Leaf",))[0]
        for limits, code in ((R.Limits(max_group_bytes=1), "REQUEST_GROUP_BYTE_BOUND"),
                (R.Limits(max_payload_bytes=len(ordinary.groups[0])), "REQUEST_PAYLOAD_BYTE_BOUND"),
                (R.Limits(max_acquired_bytes=1), "REQUEST_ACQUISITION_BOUND"),
                (R.Limits(max_acquired_nodes=1), "REQUEST_ACQUISITION_NODE_BOUND"),
                (R.Limits(max_edges=1), "REQUEST_EDGE_BOUND")):
            refuses(code, lambda limits=limits: fixture.prepare(cuts=("Leaf",), overrides={"limits": limits}))

    def retained_tampering():
        prepared = fixture.prepare("TwoCuts", cuts=("Leaf", "SecondLeaf"))[0]
        actual = fixture.retained(prepared)
        need(actual["status"] == "READY" and dict(actual["bindings"])[E.name_key(name("Leaf"))] ==
             fixture.parent[E.name_key(name("Leaf"))], "CONTROL_RETAINED_EXACT_CUT_BINDING")
        cases = [
            (lambda h: h.update(frontier_root="e"*64), "RETAINED_FRONTIER_ROOT_BINDING"),
            (lambda h: h.update(extra=[]), "RETAINED_HEADER_FIELDS"),
            (lambda h: h.pop("frontier_labels"), "RETAINED_HEADER_FIELDS"),
            (lambda h: h.update(schema=R.REQUEST_FORMAT), "RETAINED_HEADER_FIELDS"),
            (lambda h: h["frontier_labels"].reverse(), "RETAINED_FRONTIER_LABEL_ORDER"),
            (lambda h: h["frontier_labels"].append(copy.deepcopy(h["frontier_labels"][-1])),
             "RETAINED_FRONTIER_LABEL_ORDER"),
            (lambda h: h["frontier_labels"][0].__setitem__(1, "e"*64), "RETAINED_UNWARRANTED_BINDING"),
            (lambda h: h["frontier_labels"].__setitem__(0, [name("Leaf")]), "ARRAY_ARITY"),
            (lambda h: h.update(frontier_labels=[fixture.target("Eq")]), "RETAINED_DUPLICATE_OR_NAME_BOUND"),
            (lambda h: h.update(frontier_labels=[fixture.target("TwoCuts")]), "RETAINED_DUPLICATE_OR_NAME_BOUND"),
        ]
        for change, code in cases:
            refuses(code, lambda change=change: fixture.retained(prepared, header_change=change))
        for change in (lambda r: r.pop("project_authoring"),
                       lambda r: r["project_authoring"].update(frontier_root="e"*64)):
            refuses("RETAINED_FRONTIER_ROOT_BINDING", lambda change=change:
                fixture.retained(prepared, request_change=change))
        wrong_parent = dict(fixture.parent)
        wrong_parent.pop(E.name_key(name("Leaf")))
        refuses("RETAINED_UNWARRANTED_BINDING", lambda: fixture.retained(prepared, parent=wrong_parent))
        refuses("RETAINED_FILE_CHANGED", lambda: fixture.retained(prepared,
            request_change=lambda r: r["request_files"]["header.json"].update(sha256="e"*64)))

    return [("v2-full-output-and-retained-differential", v2_differential),
            ("v3-reached-cuts-and-exact-acquired-targets", cut_and_exact_targets),
            ("authenticated-context-prefix-predicate", prefix_predicate),
            ("actual-cli-scope-before-state-or-native-work", cli_scope),
            ("v3-order-shape-and-fixed-or-lowered-limits", wire_and_limits),
            ("retained-v3-bindings-and-tamper-refusals", retained_tampering)]


def main(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTROL_PYTHON_PROFILE")
    rows = []
    with ExitStack() as guards:
        for obj, method, label in ((sqlite3, "connect", "database"),
                (subprocess, "Popen", "child-process"), (os, "system", "system"),
                (socket.socket, "connect", "socket-connect"),
                (socket.socket, "connect_ex", "socket-connect-ex"),
                (socket.socket, "bind", "socket-bind"),
                (socket.socket, "listen", "socket-listen"),
                (socket.socket, "sendto", "socket-sendto")):
            guards.enter_context(patch.object(obj, method, forbidden(label)))
        loaded, lane = load_selected(args)
        for obj, method, label in ((loaded.O, "OrdinaryStore", "custody"),
                (loaded.A.OrdinaryAdmission, "open", "owner-open"),
                (loaded.A.OrdinaryAdmission, "initialize", "owner-initialize"),
                (loaded.A.OrdinaryAdmission, "preflight", "preflight"),
                (loaded.A.OrdinaryAdmission, "admit", "admission"),
                (lane.G, "contribute_source", "contribution"),
                (loaded.installation._supervisor, "supervise", "native-supervisor"),
                (loaded.peer_api.H, "exchange", "peer-exchange"),
                (loaded.peer_api.H.Provider, "start", "peer-provider")):
            guards.enter_context(patch.object(obj, method, forbidden(label)))
        output = loaded.A.C.ordinary(Path(args.output), directory=True)
        for protected in (loaded.root, Path(args.source_directory), *loaded.installation.runtime_roots.values()):
            need(not output.is_relative_to(protected) and not protected.is_relative_to(output),
                 "CONTROL_OUTPUT_OVERLAP")
        fixture = Fixtures(loaded, lane, read(Path(args.inventory), MIB))
        for title, control in controls(loaded, lane, fixture, args):
            check()
            try:
                control(); check()
                rows.append({"group": title, "ok": True})
            except BaseException as error:
                rows.append({"group": title, "ok": False, "error_type": type(error).__name__,
                             "error": str(error)[:1000]})
        loaded.profile.verify(check)
        for filename, pin in SOURCE_PINS.items():
            need(digest(read(Path(args.source_directory)/filename)) == pin, "CONTROL_FINAL_SOURCE_PIN")
    report = {"ok": len(rows) == 6 and all(row["ok"] for row in rows) and not FORBIDDEN,
        "groups": rows, "profile_sha256": PROFILE, "source_pins": SOURCE_PINS,
        "native_operations": 0, "owner_opens": 0, "custody_opens": 0,
        "forbidden_attempts": FORBIDDEN, "wall_seconds": time.monotonic()-START_WALL,
        "controller_cpu_seconds": time.process_time()-START_CPU,
        "claim": "PURE_CHANGED_BOUNDARY_CONTROLS_NOT_MATHEMATICAL_ACCEPTANCE_OR_NATIVE_FRONTIER_QUALIFICATION"}
    check()
    raw = json.dumps(report, sort_keys=True, ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(raw) <= MIB, "CONTROL_REPORT_BOUND")
    with (output/"FRONTIER-CONTROLS.json").open("xb") as stream:
        stream.write(raw)
    print(raw.decode("ascii"), flush=True)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("package", "profile-sha256", "python-runtime", "lean-runtime",
                "source-directory", "inventory", "output"):
        parser.add_argument("--"+key, required=True)
    raise SystemExit(main(parser.parse_args()))

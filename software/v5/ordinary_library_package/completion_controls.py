"""Native-free changed-boundary controls for one selected completion package.

Load the actual successor profile once. Exercise its real pure planner/binder;
explicitly mock owner admission/custody only when testing coordinator retention
and CLI forwarding. Synthetic declarations are NOT checked mathematics. Guards
prohibit databases, subprocesses and peer connections. Root separately selects
this source, its installed package and the finite outer allowance before use.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
from contextlib import ExitStack
import copy
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


def need(condition, code):
    if not condition:
        raise AssertionError(code)


class Allowance:
    deadline = START_WALL+50

    def check(self):
        need(time.monotonic() < self.deadline and time.process_time()-START_CPU < 30,
             "COMPLETION_CONTROL_ORIGINAL_ALLOWANCE")


def forbidden(*_, **__):
    raise AssertionError("COMPLETION_CONTROL_FORBIDDEN_EXTERNAL_OPERATION")


def read(path, maximum=2*MIB):
    need(path.is_absolute() and ".." not in path.parts, "COMPLETION_CONTROL_ABSOLUTE_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "COMPLETION_CONTROL_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "COMPLETION_CONTROL_REGULAR_FILE")
    size = path.stat().st_size
    need(0 < size <= maximum, "COMPLETION_CONTROL_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "COMPLETION_CONTROL_FILE_CHANGED")
    return raw


def save(path, value):
    raw = value if type(value) is bytes else json.dumps(value, sort_keys=True,
        ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode("ascii")
    need(0 < len(raw) <= MIB, "COMPLETION_CONTROL_OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def selected_package(args, allowance):
    root = Path(args.package)
    raw = read(root/"PROFILE.json")
    need(hashlib.sha256(raw).hexdigest() == args.profile_sha256, "COMPLETION_CONTROL_PROFILE_PIN")
    descriptor = json.loads(raw)
    path, name = root/"owner.py", "_completion_controls_owner"
    source, pin = read(path), descriptor["files"]["owner.py"]
    need(len(source) == pin["bytes"] and hashlib.sha256(source).hexdigest() == pin["sha256"]
         and name not in sys.modules, "COMPLETION_CONTROL_CODE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    owner = importlib.util.module_from_spec(spec)
    sys.modules[name] = owner
    exec(compile(source, str(path), "exec"), owner.__dict__)
    loader = owner.bootstrap(root, args.profile_sha256, allowance.check)
    loaded = loader.load(root, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        allowance.deadline, check_parent=allowance.check)
    need(loaded.G.A is loaded.A and loaded.completion_api.A is loaded.A
         and loaded.completion_api.G is loaded.G and loaded.peer_api.A is loaded.A,
         "COMPLETION_CONTROL_SHARED_CORE")
    return owner, loaded


def refuses(code, call, kind=ValueError):
    try:
        call()
    except kind as error:
        need(str(error) == code, "COMPLETION_CONTROL_WRONG_REFUSAL:"+str(error))
        return
    raise AssertionError("COMPLETION_CONTROL_EXPECTED_REFUSAL:"+code)


def name(text):
    return [[0, {"$bytes": list(part.encode("utf-8"))}] for part in text.split(".")]


def controls(args, owner_cli, loaded, output, allowance):
    A, G, C = loaded.A, loaded.G, loaded.completion_api
    L, B, E, S = C.L, C.B, C.B.E, A.S
    semantic, foundation, parent = loaded.installation.semantic_id, S.foundation_id(), "5"*64
    nat_key = E.name_key(name("Nat"))
    nat_id = S.basis_symbol_id(semantic, foundation, name("Nat"))
    parent_map, prepared = {nat_key: nat_id}, {nat_key: nat_id}
    fixture = output/"fixture"
    fixture.mkdir()

    def unit(own, refs=(), *, nat_type=True):
        """Syntactically valid inert data, deliberately not a mathematical proof."""
        own = name(own)
        ty = [E.EXPR_FORMAT, [], [[2, name("Nat"), []]] if nat_type else [[7, {"$bytes": []}]], 0]
        nodes = [[2, name(ref), []] for ref in refs] or [[7, {"$bytes": []}]]
        root = 0
        for index in range(1, len(refs)):
            nodes.append([3, root, index])
            root = len(nodes)-1
        value = [E.EXPR_FORMAT, [], nodes, root]
        return [E.UNIT_FORMAT, [0, own, [], ty, value, [2, 1], [own]],
                [[own, 1, [], ty, [value, [2, 1], [own]]]]]

    def bundle(units=None, boundary=None, unresolved=None):
        units = [unit("Consumer", ("Missing",))] if units is None else units
        boundary = [[name("Nat"), nat_id]] if boundary is None else boundary
        unresolved = [name("Missing")] if unresolved is None else unresolved
        return {"schema": B.SCHEMA, "assurance": B.ASSURANCE,
            "semantic_id": semantic, "foundation_id": foundation, "context_root": parent,
            "targets": [name("Consumer")], "boundary_imports": boundary,
            "unresolved_imports": unresolved, "units": units,
            "stats": {"source_records_enumerated": 0, "selected_units": len(units),
                "dependency_edges": 0, "scan_nodes": 0,
                "unit_json_bytes": sum(len(E.canonical_json(u)) for u in units),
                "boundary_imports": len(boundary), "unresolved_imports": len(unresolved)}}

    def supplement(units=None, boundary=None):
        units = [unit("Missing")] if units is None else units
        boundary = [[name("Nat"), nat_id]] if boundary is None else boundary
        return {"schema": L.SUPPLEMENT_SCHEMA, "assurance": B.ASSURANCE,
            "profile_id": semantic, "basis_id": foundation, "context_id": parent,
            "targets": [name("Missing")], "boundary_imports": boundary, "units": units,
            "stats": {"source_records_enumerated": 0, "selected_units": len(units),
                "dependency_edges": 0, "scan_nodes": 0,
                "unit_json_bytes": sum(len(E.canonical_json(u)) for u in units),
                "boundary_imports": len(boundary), "lookup_count": 0}}

    candidate_doc, supplement_doc = bundle(), supplement()
    candidate_raw, supplement_raw = map(E.canonical_json, (candidate_doc, supplement_doc))
    targets = [name("Consumer")]

    def plan(candidate=None, supplied=None, **changes):
        options = dict(semantic_id=semantic, foundation_id=foundation, context_root=parent,
            expected_targets=targets, prepared_bindings=prepared,
            warranted_symbol=lambda n: parent_map.get(E.name_key(n)), check_budget=allowance.check)
        options.update(changes)
        return L.complete_candidate(candidate_raw if candidate is None else E.canonical_json(candidate),
            supplement_raw if supplied is None else E.canonical_json(supplied), **options)

    def positive_graph_and_preservation():
        before = copy.deepcopy((candidate_doc, supplement_doc, prepared, parent_map, targets))
        lookups = []
        def lookup(n):
            key = E.name_key(n)
            lookups.append(key)
            return parent_map.get(key)
        result = plan(warranted_symbol=lookup)
        need(result.status == "READY" and not result.mathematical_acceptance
            and result.consumer_units == result.supplemental_units == 1,
            "COMPLETION_CONTROL_INERT_READY")
        items = [A.PE.read_evidence(raw) for raw in result.raw_units]
        need([item.document["unit"] for item in items] ==
            [*supplement_doc["units"], *candidate_doc["units"]], "COMPLETION_CONTROL_ORIGINAL_UNITS_AND_ORDER")
        missing_id = S.export_id(semantic, items[0].unit_id, name("Missing"))
        need(dict((E.name_key(n), i) for n, i in items[1].document["imports"])[E.name_key(name("Missing"))]
            == missing_id, "COMPLETION_CONTROL_DERIVED_IMPORT_ID")
        need(result.consumer_unit_sha256s == tuple(hashlib.sha256(E.canonical_json(u)).hexdigest()
            for u in candidate_doc["units"]) and result.candidate_sha256 == hashlib.sha256(candidate_raw).hexdigest()
            and result.supplement_sha256 == hashlib.sha256(supplement_raw).hexdigest()
            and len(lookups) == len(set(lookups)) == result.parent_lookups,
            "COMPLETION_CONTROL_PINS_AND_MEMOIZATION")
        need(before == (candidate_doc, supplement_doc, prepared, parent_map, targets),
             "COMPLETION_CONTROL_INPUT_MUTATION")
        chain = supplement([unit("Helper"), unit("Missing", ("Helper",))])
        chained = plan(supplied=chain)
        need(chained.supplemental_units == 2 and len(chained.raw_units) == 3,
             "COMPLETION_CONTROL_SUPPLEMENTAL_DEPENDENCY_CHAIN")

    def graph_and_identity_refusals():
        refuses("CANDIDATE_UNBOUND_OR_FORWARD_REFERENCE", lambda:
            plan(candidate=bundle([unit("Consumer", ("Undeclared",))]),
                 supplied=supplement([unit("Undeclared"), unit("Missing")])))
        for key in ("semantic_id", "foundation_id", "context_root", "schema", "assurance"):
            bad = copy.deepcopy(candidate_doc); bad[key] = "0"*64
            refuses("CANDIDATE_BUNDLE_CONTEXT", lambda bad=bad: plan(candidate=bad))
        for key in ("profile_id", "basis_id", "context_id", "schema", "assurance"):
            bad = copy.deepcopy(supplement_doc); bad[key] = "0"*64
            refuses("COMPLETION_PORTABLE_LABEL_BINDING", lambda bad=bad: plan(supplied=bad))
        for selected_targets in ([], [name("Extra")], [name("Missing"), name("Extra")],
                                 [name("Missing"), name("Missing")]):
            bad = copy.deepcopy(supplement_doc); bad["targets"] = selected_targets
            refuses("COMPLETION_EXACT_MISSING_TARGETS", lambda bad=bad: plan(supplied=bad))
        known = dict(parent_map)
        known[E.name_key(name("Missing"))] = "7"*64
        refuses("COMPLETION_NOT_NEEDED", lambda: plan(warranted_symbol=lambda n: known.get(E.name_key(n))))
        refuses("COMPLETION_MISSING_TARGET_NOT_PRODUCED", lambda:
            plan(supplied=supplement([unit("Other")])))
        for identity in ("0"*64, E.basis_symbol_id(semantic, foundation, name("Nat"))):
            need(identity != nat_id, "COMPLETION_CONTROL_DISTINCT_LEGACY_DOMAIN")
            refuses("COMPLETION_SUPPLEMENT_PARENT_IDENTITY", lambda identity=identity:
                plan(supplied=supplement(boundary=[[name("Nat"), identity]])))
            bad = bundle(boundary=[[name("Nat"), identity]])
            refuses("CANDIDATE_CLAIMED_IDENTITY", lambda bad=bad: plan(candidate=bad))
        refuses("CANDIDATE_CLAIMED_IDENTITY", lambda: plan(prepared_bindings={nat_key: "0"*64}))
        refuses("COMPLETION_SUPPLEMENT_PARENT_IDENTITY", lambda:
            plan(supplied=supplement(boundary=[[name("Nat"), nat_id]]*2)))
        for units in ([unit("Nat")], [unit("Consumer")], [unit("Missing"), unit("Missing")]):
            refuses("COMPLETION_EXISTING_OR_DUPLICATE_OUTPUT", lambda units=units:
                plan(supplied=supplement(units)))
        for units in ([unit("Missing", ("Consumer",))],
                      [unit("Missing", ("Later",)), unit("Later")]):
            refuses("COMPLETION_UNBOUND_OR_FORWARD_SUPPLEMENT_REFERENCE", lambda units=units:
                plan(supplied=supplement(units)))
        other_key, other_id = E.name_key(name("ConsumerOnlyImport")), "8"*64
        extended = {**parent_map, other_key: other_id}
        refuses("COMPLETION_UNBOUND_OR_FORWARD_SUPPLEMENT_REFERENCE", lambda:
            plan(candidate=bundle(boundary=[[name("Nat"), nat_id], [name("ConsumerOnlyImport"), other_id]]),
                supplied=supplement([unit("Missing", ("ConsumerOnlyImport",))]),
                prepared_bindings=extended, warranted_symbol=lambda n: extended.get(E.name_key(n))))
        bad = copy.deepcopy(supplement_doc); bad["stats"]["unit_json_bytes"] += 1
        refuses("COMPLETION_SUPPLEMENT_UNIT_BYTES", lambda: plan(supplied=bad))

    def aggregate_bounds():
        result = plan()
        total_nodes = [E.inspect_unit(u).total_nodes for u in
                       (*candidate_doc["units"], *supplement_doc["units"])]
        cases = [("max_bundle_bytes", max(len(candidate_raw), len(supplement_raw)),
                  "COMPLETION_COMBINED_INPUT_BYTES"),
                 ("max_units", 1, "COMPLETION_COMBINED_UNIT_BOUND"),
                 ("max_bindings", 2, "COMPLETION_COMBINED_BOUNDARY_BOUND"),
                 ("max_total_nodes", max(total_nodes), "COMPLETION_COMBINED_CONTENT_BOUND"),
                 ("max_evidence_bytes", max(map(len, result.raw_units)), "CANDIDATE_EVIDENCE_BYTE_BOUND")]
        for field, value, code in cases:
            refuses(code, lambda field=field, value=value: plan(limits=B.Limits(**{field: value})))
        no_parent_candidate = bundle([unit("Consumer", ("Missing",), nat_type=False)], boundary=[])
        no_parent_supplement = supplement([unit("Missing", nat_type=False)], boundary=[])
        refuses("COMPLETION_COMBINED_OUTPUT_BOUND", lambda:
            plan(candidate=no_parent_candidate, supplied=no_parent_supplement,
                 prepared_bindings={}, limits=B.Limits(max_bindings=1)))
        refuses("COMPLETION_COMBINED_NAME_BOUND", lambda:
            plan(supplied=no_parent_supplement, limits=B.Limits(max_bindings=2)))

    def cancellation_and_lookup_failure():
        class Cancelled(RuntimeError):
            pass
        def stop():
            raise Cancelled("CONTROL_CANCELLED")
        refuses("CONTROL_CANCELLED", lambda: plan(check_budget=stop), Cancelled)
        def lookup_failure(_):
            raise Cancelled("CONTROL_PARENT_LOOKUP_FAILED")
        refuses("CONTROL_PARENT_LOOKUP_FAILED", lambda: plan(warranted_symbol=lookup_failure), Cancelled)
        calls = []
        def count():
            allowance.check(); calls.append(None)
        plan(check_budget=count)
        total, position = len(calls), 0
        def late_stop():
            nonlocal position
            allowance.check(); position += 1
            if position == total:
                stop()
        refuses("CONTROL_CANCELLED", lambda: plan(check_budget=late_stop), Cancelled)
        need(position == total and total > 2, "COMPLETION_CONTROL_FINAL_CHECK_CANCELS")
        refuses("COMPLETION_LOOKUP_TYPE", lambda: plan(warranted_symbol=lambda _: object()))

    def mocked_coordinator():
        # An exact-class shell, not an opened owner. Native entrypoints stay
        # forbidden except the explicit per-test preflight/admit replacements.
        native_owner = object.__new__(A.OrdinaryAdmission)
        native_owner.installation = loaded.installation
        preview_memory = {}
        def put_preview(raw, *, before_commit):
            before_commit(); preview_memory[hashlib.sha256(raw).hexdigest()] = raw
        def get_preview(digest, size, *, check_budget):
            check_budget(); raw = preview_memory[digest]
            need(len(raw) == size, "COMPLETION_CONTROL_PREVIEW_SIZE")
            return raw
        native_owner.evidence_store = SimpleNamespace(put_preview=put_preview, get_preview=get_preview)
        def context(root):
            need(root == parent, "COMPLETION_CONTROL_CONTEXT_SELECTION")
            return {"bindings": dict(parent_map)}
        native_owner.catalog = SimpleNamespace(context=context)
        expected_units = plan().raw_units

        for mode in ("success", "preview-failure", "preflight-refusal"):
            calls, charges, budgets = [], [], []
            accepted = {"status": "CHECKED", "units_checked": len(expected_units),
                        "local_root": "6"*64, "mock_only": True}
            def make_budget():
                budget = A.OperationBudget(30, 10, 64)
                budget.deadline = min(budget.deadline, allowance.deadline)
                budgets.append(budget)
                return budget
            selected_plan = SimpleNamespace(status="NEEDS" if mode == "preflight-refusal" else "READY")
            def preflight(self, root, units, *, budget, limits):
                need(self is native_owner and root == parent and units == expected_units
                    and budget is budgets[0] and limits.max_units == 32,
                    "COMPLETION_CONTROL_PREFLIGHT_FORWARDING")
                calls.append("preflight")
                return selected_plan
            def admit(self, root, checked, budget):
                need(self is native_owner and root == parent and checked is selected_plan
                    and budget is budgets[0] and calls == ["preflight"],
                    "COMPLETION_CONTROL_ADMISSION_FORWARDING")
                budget.claim(); budget.worker_cpu = 0.25  # Explicit synthetic charge; no worker exists.
                calls.append("admit")
                return accepted
            destination = fixture/("coordinator-"+mode)
            with ExitStack() as mocks:
                mocks.enter_context(patch.object(A.OrdinaryAdmission, "preflight", preflight))
                mocks.enter_context(patch.object(A.OrdinaryAdmission, "admit", admit))
                if mode == "preview-failure":
                    def fail_preview(*_, **__):
                        raise RuntimeError("CONTROL_PREVIEW_FAILED")
                    mocks.enter_context(patch.object(C.PP, "preview_from_evidence", fail_preview))
                try:
                    result = C.complete_source(native_owner, parent, candidate_raw, supplement_raw,
                        expected_targets=targets, prepared_bindings=prepared, output_directory=destination,
                        parent_deadline=allowance.deadline, make_budget=make_budget,
                        account_worker_cpu=charges.append, check_parent=allowance.check)
                except G.ContributionError as error:
                    need(mode != "success", "COMPLETION_CONTROL_UNEXPECTED_COORDINATOR_FAILURE:"+str(error))
                    expected_accepted = accepted if mode == "preview-failure" else None
                    expected_phase = "PUBLICATION_BYTES" if mode == "preview-failure" else "PREFLIGHT"
                    expected_error = "CONTROL_PREVIEW_FAILED" if mode == "preview-failure" else "COMPLETION_PREFLIGHT_NEEDS"
                    need(error.report["accepted"] == expected_accepted
                        and error.report["phase"] == "COMPLETION_"+expected_phase
                        and error.report["error"] == expected_error
                        and error.report["native_cpu_seconds"] == (0.25 if mode == "preview-failure" else 0.0),
                        "COMPLETION_CONTROL_FAILURE_ACCEPTANCE_RETENTION")
                    need(json.loads(read(destination/"FAILURE.json"))["accepted"] == expected_accepted
                        and not (destination/"RESULT.json").exists(), "COMPLETION_CONTROL_FAILURE_RECORD")
                else:
                    need(mode == "success" and result["admission"] == accepted
                        and len(result["units"]) == len(expected_units) and len(result["previews"]) == 1
                        and result["native_cpu_seconds"] == 0.25 and (destination/"RESULT.json").is_file(),
                        "COMPLETION_CONTROL_MOCKED_SUCCESS")
                need(calls == (["preflight"] if mode == "preflight-refusal" else ["preflight", "admit"])
                    and charges == ([] if mode == "preflight-refusal" else [0.25]) and len(budgets) == 1,
                    "COMPLETION_CONTROL_ONE_BUDGET_ONE_ADMISSION")
                need(read(destination/"candidate.json") == candidate_raw
                    and read(destination/"supplement.json") == supplement_raw,
                    "COMPLETION_CONTROL_RETAINED_INPUT_BYTES")
                if mode != "preflight-refusal":
                    need(json.loads(read(destination/"ADMISSION.json")) == accepted,
                         "COMPLETION_CONTROL_DURABLE_MOCK_ADMISSION_RECORD")
                else:
                    need(not (destination/"ADMISSION.json").exists() and not budgets[0].claimed,
                         "COMPLETION_CONTROL_PREFLIGHT_REFUSAL_NO_ADMISSION")

    catalog, custody = fixture/"catalog", fixture/"custody"
    catalog.mkdir(); custody.mkdir()
    files = {key: fixture/(key+".json") for key in ("candidate", "supplement", "prepared", "names", "limits")}
    pins = {"candidate": save(files["candidate"], candidate_raw),
            "supplement": save(files["supplement"], supplement_raw),
            "prepared": save(files["prepared"], [[name("Nat"), nat_id]])}
    save(files["names"], targets)
    save(files["limits"], {key: bounds[0] for key, bounds in loaded.O.STORE_LIMITS.items()})
    store_id = "4"*64
    save(catalog/"ADOPTION.json", {"schema": A.P.SCHEMA, "store_id": store_id,
        "implementation": loaded.installation.doc["implementation"], "limits": vars(A.P.Limits())})
    malformed, duplicate = fixture/"malformed-prepared.json", fixture/"duplicate-prepared.json"
    malformed_pin = save(malformed, b"[")
    duplicate_pin = save(duplicate, [[name("Nat"), nat_id]]*2)

    def cli_args(**changes):
        selected = dict(operation="complete", profile_sha256=args.profile_sha256,
            python_runtime=args.python_runtime, lean_runtime=args.lean_runtime,
            catalog=str(catalog), custody=str(custody), store_id=store_id, custody_limits=str(files["limits"]),
            wall_seconds=50, cpu_seconds=30, memory_mib=256, catalog_limits=None,
            parent_root=parent, source=None, acquired_targets=None, output_names=str(files["names"]),
            output=str(fixture/"not-created-cli-output"), context_root=None, after_root="", limit=32,
            project_authoring=None, project_authoring_sha256=None,
            candidate=str(files["candidate"]), candidate_sha256=pins["candidate"],
            supplement=str(files["supplement"]), supplement_sha256=pins["supplement"],
            prepared_bindings=str(files["prepared"]), prepared_bindings_sha256=pins["prepared"])
        return SimpleNamespace(**(selected | changes))

    fake_loader = SimpleNamespace(load=lambda *_, **__: loaded)

    def preopen_cli_refusals():
        cases = [({"supplement": None}, "OWNER_COMPLETION_ARGUMENTS"),
                 ({"candidate_sha256": None}, "OWNER_COMPLETION_ARGUMENTS"),
                 ({"source": "unselected"}, "OWNER_CONTRIBUTION_ARGUMENTS"),
                 ({"project_authoring": "unselected", "project_authoring_sha256": "0"*64},
                  "OWNER_PROJECT_AUTHORING_ARGUMENTS"),
                 ({"prepared_bindings": str(malformed), "prepared_bindings_sha256": malformed_pin},
                  "ADMISSION_WRITER_UNTERMINATED"),
                 ({"prepared_bindings": str(duplicate), "prepared_bindings_sha256": duplicate_pin},
                  "OWNER_COMPLETION_DUPLICATE_PREPARED_NAME")]
        for key in ("candidate_sha256", "supplement_sha256", "prepared_bindings_sha256"):
            cases.append(({key: "0"*64}, "OWNER_COMPLETION_INPUT_PIN"))
        with patch.object(owner_cli, "bootstrap", lambda *_, **__: fake_loader), \
                patch.object(loaded.O, "OrdinaryStore", forbidden):
            for changes, code in cases:
                report = owner_cli.run(cli_args(**changes))
                need(report["ok"] is False and report["phase"] == "SUPPORT" and report["error"] == code,
                     "COMPLETION_CONTROL_PREOPEN_REFUSAL:"+str(report))
            report = owner_cli.run(cli_args(operation="status", parent_root=None, output_names=None, output=None))
            need(report["ok"] is False and report["phase"] == "SUPPORT"
                and report["error"] == "OWNER_COMPLETION_ARGUMENTS", "COMPLETION_CONTROL_COMPLETE_ONLY")
        need(not (fixture/"not-created-cli-output").exists(), "COMPLETION_CONTROL_NO_CLI_OUTPUT")

    def mocked_cli_forwarding():
        captured, closed = [], []
        fake_owner = SimpleNamespace(close=lambda: closed.append("owner"))
        fake_custody = SimpleNamespace(close=lambda: closed.append("custody"))
        accepted = {"status": "CHECKED", "local_root": "6"*64, "mock_only": True}
        def complete(*positional, **keywords):
            captured.append((positional, keywords))
            return {"admission": accepted, "claim": "MOCK_ONLY"}
        def fail_after_acceptance(*positional, **keywords):
            complete(*positional, **keywords)
            raise G.ContributionError("COMPLETION_PUBLICATION_BYTES", RuntimeError("CONTROL_AFTER_ACCEPT"), accepted)
        with patch.object(owner_cli, "bootstrap", lambda *_, **__: fake_loader), \
                patch.object(loaded.O, "OrdinaryStore", lambda *_, **__: fake_custody), \
                patch.object(A.OrdinaryAdmission, "open", lambda *_, **__: fake_owner):
            with patch.object(C, "complete_source", complete):
                report = owner_cli.run(cli_args())
            with patch.object(C, "complete_source", fail_after_acceptance):
                failure = owner_cli.run(cli_args())
        need(report["ok"] and report["result"]["admission"] == accepted and not failure["ok"]
            and failure["accepted"] == accepted and failure["detail"]["accepted"] == accepted,
            "COMPLETION_CONTROL_CLI_ACCEPTANCE_RETENTION")
        need(len(captured) == 2 and closed == ["owner", "custody"]*2,
             "COMPLETION_CONTROL_CLI_CLOSES_MOCKS")
        for positional, keywords in captured:
            need(positional == (fake_owner, parent, candidate_raw, supplement_raw)
                and keywords["expected_targets"] == targets and keywords["prepared_bindings"] == prepared
                and keywords["output_directory"] == fixture/"not-created-cli-output"
                and keywords["parent_deadline"] <= time.monotonic()+50
                and all(callable(keywords[key]) for key in ("make_budget", "account_worker_cpu", "check_parent")),
                "COMPLETION_CONTROL_CLI_EXACT_FORWARDING")

    return [("pure-positive-graph-and-preservation", positive_graph_and_preservation),
            ("pure-graph-and-identity-refusals", graph_and_identity_refusals),
            ("pure-combined-resource-bounds", aggregate_bounds),
            ("pure-cancellation-and-lookup-failure", cancellation_and_lookup_failure),
            ("mocked-coordinator-success-and-acceptance-retention", mocked_coordinator),
            ("preopen-cli-refusals", preopen_cli_refusals),
            ("mocked-cli-forwarding-and-retention", mocked_cli_forwarding)]


def main(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "COMPLETION_CONTROL_PYTHON")
    allowance, rows = Allowance(), []
    with ExitStack() as guards:
        guards.enter_context(patch.object(sqlite3, "connect", forbidden))
        guards.enter_context(patch.object(subprocess, "Popen", forbidden))
        guards.enter_context(patch.object(socket.socket, "connect", forbidden))
        guards.enter_context(patch.object(socket.socket, "connect_ex", forbidden))
        owner, loaded = selected_package(args, allowance)
        guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, "open", forbidden))
        guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, "preflight", forbidden))
        guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, "admit", forbidden))
        guards.enter_context(patch.object(loaded.peer_api.H, "exchange", forbidden))
        guards.enter_context(patch.object(loaded.peer_api.H.Provider, "start", forbidden))
        output = loaded.A.C.ordinary(Path(args.output), directory=True)
        for protected in (loaded.root, *loaded.installation.runtime_roots.values()):
            need(not output.is_relative_to(protected) and not protected.is_relative_to(output),
                 "COMPLETION_CONTROL_OUTPUT_OVERLAP")
        for group, control in controls(args, owner, loaded, output, allowance):
            allowance.check()
            try:
                control(); allowance.check()
                rows.append({"group": group, "ok": True})
            except BaseException as error:
                rows.append({"group": group, "ok": False, "error_type": type(error).__name__,
                             "error": str(error)[:1000]})
    report = {"ok": len(rows) == 7 and all(row["ok"] for row in rows), "groups": rows,
        "profile_sha256": args.profile_sha256, "implementation_id": loaded.installation.implementation_id,
        "wall_seconds": time.monotonic()-START_WALL, "controller_cpu_seconds": time.process_time()-START_CPU,
        "native_operations": 0, "owner_opens": 0,
        "claim": "PURE_PLANNER_AND_EXPLICIT_MOCKS_NOT_MATHEMATICAL_ACCEPTANCE_OR_PROJECT_COMPATIBILITY"}
    save(output/"COMPLETION-CONTROLS.json", report)
    print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    raise SystemExit(main(parser.parse_args()))

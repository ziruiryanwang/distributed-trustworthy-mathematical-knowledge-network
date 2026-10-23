"""Native-free focused closure controls using three retained real evidence units.

Authority is an explicit fixture-derived MOCK warrant map. No owner, SQLite,
native compiler, process, network, admission or mathematical acceptance occurs.
One selected 50 wall /30 CPU lifetime; outer supervisor owns hard limits.
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
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
MIB = 1024**2
PARENT = "84dd6a9cf7ece45c4820ab3c28fc50ec072168c77e3cef9b890183bff5af9e13"
TWICE = "25ae588e95228a64196a576aa9c9dd78249c23b0c26189c5671a434b93afa1b3"
TWICE_EQ = "c4639e6e5f70e259ea1611adba8e168aa74dbfb91f98e2512cd465f82705e61e"
FOUR = "d52aed3d1d0f94b8ee2236a7ee84435c983c9523dca0f100f4369c183c3d4e51"
FIXTURES = {
    "ordinary-package-lifecycle-continuation-01/contribution/evidence/"+TWICE+".json":
        "c7266a3047afcf59059b7884853b4d6b9be4244509f260e78dd072973f9704aa",
    "ordinary-package-lifecycle-continuation-01/contribution/evidence/"+TWICE_EQ+".json":
        "88c8b3b9da6bfd39fff9c827a1bec8b51ce4289c949c9d7507bfad5e53bc421f",
    "ordinary-peer-reciprocal-02/B-contribution/evidence/"+FOUR+".json":
        "d0bb18c957c41f3f15d0b47b4eda2f41b8c1f72107d5065929625228a63558ae",
}


def need(condition, code):
    if not condition:
        raise AssertionError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check():
    need(time.monotonic() < START_WALL+50 and time.process_time()-START_CPU < 30,
         "CLOSURE_CONTROL_ORIGINAL_ALLOWANCE")


def forbidden(*_, **__):
    raise AssertionError("CLOSURE_CONTROL_FORBIDDEN_EXTERNAL_OPERATION")


def read(path, maximum=2*MIB):
    need(path.is_absolute() and ".." not in path.parts, "CLOSURE_CONTROL_ABSOLUTE_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "CLOSURE_CONTROL_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "CLOSURE_CONTROL_REGULAR")
    size = path.stat().st_size
    need(0 < size <= maximum, "CLOSURE_CONTROL_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "CLOSURE_CONTROL_FILE_CHANGED")
    return raw


def save(path, value):
    raw = value if type(value) is bytes else json.dumps(value, sort_keys=True,
        ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode("ascii")
    need(0 < len(raw) <= MIB, "CLOSURE_CONTROL_OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def name(text):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in text.split(".")]


def refuses(code, call):
    try:
        call()
    except ValueError as error:
        need(str(error) == code, "CLOSURE_CONTROL_WRONG_REFUSAL:"+str(error))
        return
    raise AssertionError("CLOSURE_CONTROL_MISSING_REFUSAL:"+code)


def load_source(path, expected, module_name):
    raw = read(path)
    need(sha(raw) == expected and module_name not in sys.modules, "CLOSURE_CONTROL_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def selected_package(args):
    package = Path(args.package)
    raw = read(package/"PROFILE.json")
    need(sha(raw) == args.profile_sha256, "CLOSURE_CONTROL_PROFILE_PIN")
    profile = json.loads(raw)
    owner = load_source(package/"owner.py", profile["files"]["owner.py"]["sha256"],
                        "_closure_controls_owner")
    loader = owner.bootstrap(package, args.profile_sha256, check)
    return loader.load(package, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        START_WALL+50, check_parent=check)


def controls(A, C, loaded, output):
    E, S, PE = A.E, A.S, A.PE
    semantic, foundation = S.semantic_id(), S.foundation_id()
    inventory = loaded.installation.read("inventory", MIB)
    need(sha(inventory) == S.INVENTORY, "CLOSURE_CONTROL_FIXED_INVENTORY")
    raws = {Path(relative).stem: read(LOCAL/relative, MIB) for relative in FIXTURES}
    need({relative: sha(raws[Path(relative).stem]) for relative in FIXTURES} == FIXTURES,
         "CLOSURE_CONTROL_RETAINED_FIXTURE_PINS")
    items = {identity: PE.read_evidence(raw) for identity, raw in raws.items()}
    need(all(item.unit_id == identity and item.document["semantic_id"] == semantic
             for identity, item in items.items()), "CLOSURE_CONTROL_REAL_UNIT_IDENTITIES")
    # Explicit local fixture-derived map: NOT an opened owner or actual warrant.
    mapping = {E.name_key(row[0]): S.basis_symbol_id(semantic, foundation, row[0])
               for row in json.loads(inventory)}
    exports, by_name = {}, {}
    for identity, item in items.items():
        for row in item.document["unit"][2]:
            key = E.name_key(row[0])
            need(key not in mapping, "CLOSURE_CONTROL_FIXTURE_NAME_CONFLICT")
            binding = {"name": row[0], "unit_id": identity,
                       "export_id": S.export_id(semantic, identity, row[0])}
            mapping[key] = binding["export_id"]
            exports[identity] = binding
            by_name[key] = identity
    need(len(mapping) == 584 and len(exports) == 3, "CLOSURE_CONTROL_FIXTURE_CENSUS")
    module = name("DMKNBridge_"+"a"*64)
    fixture_target = [exports[FOUR]]

    def collect(*, selected=None, mock_map=None, fetch=None, calls=None, **changes):
        chosen = mapping if mock_map is None else mock_map
        selected = copy.deepcopy(fixture_target if selected is None else selected)
        def default_fetch(encoded_name, identity, maximum):
            key = E.name_key(encoded_name)
            if calls is not None:
                calls.append((key, identity, maximum))
            unit = by_name[key]
            raw = raws[unit]
            need(len(raw) <= maximum, "CLOSURE_CONTROL_MOCK_FETCH_BOUND")
            return raw
        options = dict(admission_api=A, semantic_id=semantic, foundation_id=foundation,
            context_root=PARENT, inventory_raw=inventory, targets=selected,
            module_name=copy.deepcopy(module), warranted_symbol=lambda n: chosen.get(E.name_key(n)),
            fetch_evidence=default_fetch if fetch is None else fetch, check_budget=check)
        options.update(changes)
        return C.collect_closure(**options)

    def complete_proof_only_closure():
        calls = []
        result = collect(calls=calls)
        descriptor = items[FOUR].document["unit"][1]
        type_refs, _ = E._dag_references(descriptor[3], descriptor[2], E.DEFAULT_LIMITS)
        proof_refs, _ = E._dag_references(descriptor[4], descriptor[2], E.DEFAULT_LIMITS)
        lemma = E.name_key(name("CommonsPackageExample.applyTwice_eq"))
        need(lemma in proof_refs and lemma not in type_refs, "CLOSURE_CONTROL_GENUINE_PROOF_ONLY_IMPORT")
        need(result.status == "READY_FOR_NATIVE_MODULE_RECHECK" and result.mathematical_acceptance is False and
             result.ordered_unit_ids == (TWICE, TWICE_EQ, FOUR) and
             result.ordered_evidence == tuple(raws[unit] for unit in (TWICE, TWICE_EQ, FOUR)) and
             result.inventory == inventory, "CLOSURE_CONTROL_COMPLETE_ORIGINAL_PROOFS")
        need(result.fetch_calls == len(calls) == 3 and len({row[0] for row in calls}) == 3 and
             result.acquired_bytes == sum(map(len, raws.values())) and result.output_names == 3 and
             result.warrant_lookups == 584 and len(result.basis_bindings) == 581,
             "CLOSURE_CONTROL_EXACT_COUNTS")
        request = E.strict_json(result.request)
        need(set(request) == {"schema", "semantic_id", "foundation_id", "context_root",
                             "module_name", "targets", "unit_ids", "units"} and
             request["schema"] == C.REQUEST_SCHEMA and request["module_name"] == module and
             request["targets"] == [exports[FOUR]["name"]] and
             request["unit_ids"] == list(result.ordered_unit_ids) and
             request["units"] == [items[unit].document["unit"] for unit in result.ordered_unit_ids],
             "CLOSURE_CONTROL_NATIVE_REQUEST")
        save(output/"closure-request.json", result.request)
        save(output/"closure-evidence-manifest.json", [{"unit_id": identity,
             "bytes": len(raws[identity]), "sha256": sha(raws[identity])} for identity in result.ordered_unit_ids])

    def authority_vs_availability():
        lemma = E.name_key(exports[TWICE_EQ]["name"])
        absent = dict(mapping); absent.pop(lemma)
        refuses("MODULE_CLOSURE_NOT_WARRANTED", lambda: collect(mock_map=absent))
        calls = []
        def unavailable(encoded_name, identity, maximum):
            key = E.name_key(encoded_name); calls.append(key)
            return None if key == lemma else raws[by_name[key]]
        refuses("MODULE_CLOSURE_EVIDENCE_UNAVAILABLE", lambda: collect(fetch=unavailable))
        need(lemma in calls, "CLOSURE_CONTROL_UNAVAILABLE_WAS_REQUESTED")
        wrong = dict(mapping); wrong[lemma] = "0"*64
        refuses("MODULE_CLOSURE_WARRANT_MISMATCH", lambda: collect(mock_map=wrong))
        def io_failure(*_):
            raise ValueError("CLOSURE_CONTROL_INJECTED_RETRIEVAL_FAILURE")
        refuses("CLOSURE_CONTROL_INJECTED_RETRIEVAL_FAILURE", lambda: collect(fetch=io_failure))

    def exact_id_and_import_tampering():
        wrong = copy.deepcopy(fixture_target); wrong[0]["export_id"] = "0"*64
        refuses("MODULE_CLOSURE_TARGET_EXPORT_BINDING", lambda: collect(selected=wrong))
        refuses("MODULE_CLOSURE_ACTUAL_TARGET_BINDING", lambda:
                collect(fetch=lambda *_: raws[TWICE_EQ]))
        changed = copy.deepcopy(items[FOUR].document)
        lemma = E.name_key(exports[TWICE_EQ]["name"])
        next(row for row in changed["imports"] if E.name_key(row[0]) == lemma)[1] = "0"*64
        raw = E.canonical_json(changed)
        altered = PE.read_evidence(raw)  # Valid existing syntax; changed identity.
        target = copy.deepcopy(exports[FOUR]); target["unit_id"] = altered.unit_id
        target["export_id"] = S.export_id(semantic, altered.unit_id, target["name"])
        changed_map = dict(mapping); changed_map[E.name_key(target["name"])] = target["export_id"]
        refuses("MODULE_CLOSURE_WARRANT_MISMATCH", lambda: collect(selected=[target],
                mock_map=changed_map, fetch=lambda *_: raw))

    def basis_and_target_guards():
        refuses("MODULE_CLOSURE_FIXED_INVENTORY", lambda: collect(inventory_raw=inventory+b" "))
        wrong = dict(mapping)
        wrong[E.name_key(name("Eq"))] = "0"*64
        refuses("MODULE_CLOSURE_WARRANT_MISMATCH", lambda: collect(mock_map=wrong))
        refuses("MODULE_CLOSURE_SELECTED_FOUNDATION", lambda: collect(foundation_id="0"*64))
        refuses("MODULE_CLOSURE_DUPLICATE_TARGET", lambda: collect(selected=fixture_target*2))
        refuses("MODULE_CLOSURE_MODULE_NAME", lambda: collect(module_name=name("WrongModule")))
        basis_target = {"name": name("Eq"), "export_id": mapping[E.name_key(name("Eq"))], "unit_id": "0"*64}
        refuses("MODULE_CLOSURE_NONBASIS_TARGET_REQUIRED", lambda: collect(selected=[basis_target]))

    def bounds_and_cancellation():
        refuses("MODULE_CLOSURE_UNIT_BOUND", lambda: collect(limits=C.Limits(max_units=2)))
        refuses("MODULE_CLOSURE_SCHEDULE_BOUND", lambda: collect(limits=C.Limits(max_names=1)))
        refuses("MODULE_CLOSURE_REQUEST_BYTES", lambda: collect(limits=C.Limits(max_request_bytes=1)))
        offered = []
        def oversized(encoded_name, identity, maximum):
            offered.append(maximum)
            return raws[FOUR]
        refuses("MODULE_CLOSURE_EVIDENCE_BYTES", lambda:
                collect(fetch=oversized, limits=C.Limits(max_total_bytes=1)))
        need(offered == [1], "CLOSURE_CONTROL_REMAINING_BYTES_FORWARDED")
        def canceled():
            raise ValueError("CLOSURE_CONTROL_CANCELED")
        refuses("CLOSURE_CONTROL_CANCELED", lambda: collect(check_budget=canceled))
        refuses("MODULE_CLOSURE_LIMIT:max_units", lambda: C.Limits(max_units=True))

    def deterministic_order_and_single_fetch():
        first_calls, second_calls = [], []
        first = collect(selected=[exports[FOUR], exports[TWICE]], calls=first_calls)
        second = collect(selected=[exports[TWICE], exports[FOUR]], calls=second_calls,
                         mock_map=dict(reversed(tuple(mapping.items()))))
        need(first.ordered_unit_ids == second.ordered_unit_ids == (TWICE, TWICE_EQ, FOUR) and
             first.ordered_evidence == second.ordered_evidence and
             first.fetch_calls == second.fetch_calls == len(first_calls) == len(second_calls) == 3,
             "CLOSURE_CONTROL_ORDER_NOT_TRAVERSAL_ORDER")

    def callback_mutation_detachment():
        mutable_targets = copy.deepcopy(fixture_target)
        mutable_module = copy.deepcopy(module)
        visited, fetched = [], []
        def mutating_warrant(encoded_name):
            key = E.name_key(encoded_name); visited.append(key)
            result = mapping.get(key)
            encoded_name.clear()
            mutable_targets.clear(); mutable_module.clear()
            return result
        def mutating_fetch(encoded_name, identity, maximum):
            key = E.name_key(encoded_name); fetched.append(key)
            raw = raws[by_name[key]]
            need(len(raw) <= maximum, "CLOSURE_CONTROL_MUTATION_FETCH_BOUND")
            encoded_name.clear()
            return raw
        result = C.collect_closure(admission_api=A, semantic_id=semantic, foundation_id=foundation,
            context_root=PARENT, inventory_raw=inventory, targets=mutable_targets, module_name=mutable_module,
            warranted_symbol=mutating_warrant, fetch_evidence=mutating_fetch, check_budget=check)
        request = E.strict_json(result.request)
        need(not mutable_targets and not mutable_module and request["module_name"] == module and
             request["targets"] == [exports[FOUR]["name"]] and
             result.ordered_evidence == tuple(raws[unit] for unit in (TWICE, TWICE_EQ, FOUR)) and
             len(visited) == len(set(visited)) == 584 and len(fetched) == 3,
             "CLOSURE_CONTROL_CALLBACKS_CANNOT_REWRITE_SELECTED_INPUT")

    return [("complete-original-proofs-including-proof-only-import", complete_proof_only_closure),
            ("authority-mismatch-versus-evidence-unavailable", authority_vs_availability),
            ("exact-unit-export-and-import-binding", exact_id_and_import_tampering),
            ("fixed-basis-target-and-module-boundaries", basis_and_target_guards),
            ("bounded-acquisition-planning-and-cancellation", bounds_and_cancellation),
            ("deterministic-topology-and-fetch-once", deterministic_order_and_single_fetch),
            ("callback-and-caller-mutation-detachment", callback_mutation_detachment)]


def main(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CLOSURE_CONTROL_PYTHON")
    rows = []
    with ExitStack() as guards:
        guards.enter_context(patch.object(sqlite3, "connect", forbidden))
        guards.enter_context(patch.object(subprocess, "Popen", forbidden))
        guards.enter_context(patch.object(socket.socket, "connect", forbidden))
        guards.enter_context(patch.object(socket.socket, "connect_ex", forbidden))
        loaded = selected_package(args)
        for operation in ("open", "preflight", "admit", "initialize"):
            guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, operation, forbidden))
        output = loaded.A.C.ordinary(Path(args.output), directory=True)
        for protected in (loaded.root, *loaded.installation.runtime_roots.values(),
                          LOCAL/"ordinary-package-lifecycle-continuation-01", LOCAL/"ordinary-peer-reciprocal-02"):
            need(not output.is_relative_to(protected) and not protected.is_relative_to(output),
                 "CLOSURE_CONTROL_OUTPUT_OVERLAP")
        collector_path = Path(__file__).absolute().parent/"module_closure.py"
        collector = load_source(collector_path, args.collector_sha256, "_closure_controls_collector")
        for label, control in controls(loaded.A, collector, loaded, output):
            check()
            try:
                control(); check()
                rows.append({"group": label, "ok": True})
            except BaseException as error:
                rows.append({"group": label, "ok": False,
                             "error_type": type(error).__name__, "error": str(error)[:1000]})
        need({relative: sha(read(LOCAL/relative, MIB)) for relative in FIXTURES} == FIXTURES,
             "CLOSURE_CONTROL_RETAINED_BYTES_CHANGED")
    report = {"ok": len(rows) == 7 and all(row["ok"] for row in rows), "groups": rows,
        "profile_sha256": args.profile_sha256, "collector_sha256": args.collector_sha256,
        "fixture_sha256s": FIXTURES, "owner_opens": 0, "native_operations": 0,
        "wall_seconds": time.monotonic()-START_WALL, "controller_cpu_seconds": time.process_time()-START_CPU,
        "claim": "PURE_FULL_EVIDENCE_CLOSURE_UNDER_EXPLICIT_MOCK_WARRANTS_NOT_MODULE_OR_MATHEMATICAL_ACCEPTANCE"}
    save(output/"CLOSURE-CONTROLS.json", report)
    print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output", "collector-sha256"):
        parser.add_argument("--"+option, required=True)
    raise SystemExit(main(parser.parse_args()))

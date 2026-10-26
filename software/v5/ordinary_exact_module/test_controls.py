"""Focused native-free exact-installed metadata controls; source-only until selected.

Load pinned inert codecs and the selected two Python payloads, with owner APIs
stubbed. No owner/catalog is opened and no native/database/network operation is
allowed. The commit test stops before copying or publication; the restore test
uses an explicitly invented record and non-Lean artifacts in one fresh output.
Neither fixtures nor a passing report supply live mathematical authority.
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
import socket
import sqlite3
import stat
import subprocess
import sys
import time
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
BASE = Path(__file__).absolute().parent
LOCAL = ROOT/"experiments/v5-local-checks"
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()
SOURCE_PINS = {
    "ordinary_evidence": ("software/v5/ordinary_lean/ordinary_evidence.py",
        "fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6"),
    "ordinary_semantics": ("software/v5/ordinary_lean/ordinary_semantics.py",
        "ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915"),
    "portable_evidence": ("software/v5/ordinary_lean/portable_evidence.py",
        "f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8"),
    "module_closure": ("software/v5/ordinary_module_anchor/module_closure.py",
        "f053e9726bdba24724e7e44baa03ffa0006f80b068440086a36023068512aa8c"),
}
FIXTURES = {
    "definition": ("concept-theory-b-export-01/bundle/units/"
        "52c32f0b4de89b9fed93bd099499dd7d029c6bc62e5de32bfeeaa25b08c9e3dd.json",
        "fe0d8a292f3532f7da7a4a74ac41de7b267457193c8f417f7210e7a33767e90f"),
    "group": ("concept-theory-b-export-01/bundle/units/"
        "cde627fdcccf8557e5a024aa6d11ad8d87ed5bdaa16dd9e1686dc5338f4c5503.json",
        "212318dac8468b2f72eeafece1bcdec4fc5b337b5c4a541b25eec68eb79462ef"),
    "list_group": ("concept-theory-b-export-01/bundle/units/"
        "e8d02c6c1c6e72fa4c1e8e6a9390b71eb2836653cb32b7bc9838dfa3e25f4b98.json",
        "1c6276e1ca5fad236286fbbbb2aba7499bdce74a3f9bb327a76223de4b3982f6"),
    "theorem": ("ordinary-package-lifecycle-continuation-01/contribution/evidence/"
        "c4639e6e5f70e259ea1611adba8e168aa74dbfb91f98e2512cd465f82705e61e.json",
        "88c8b3b9da6bfd39fff9c827a1bec8b51ce4289c949c9d7507bfad5e53bc421f"),
}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def check():
    need(time.monotonic()-START < 40 and time.process_time()-CPU < 25,
         "EXACT_CONTROLS_ORIGINAL_ALLOWANCE")


def forbidden(*_, **__):
    raise AssertionError("EXACT_CONTROLS_FORBIDDEN_EXTERNAL_OPERATION")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ordinary(path, *, directory=False, fresh=False):
    path = Path(path)
    need(path.is_absolute() and path.is_relative_to(ROOT) and ".." not in path.parts,
         "EXACT_CONTROLS_LOCAL_PATH")
    parts = (*reversed(path.parents), path)
    for part in parts:
        if fresh and part == path:
            need(not os.path.lexists(part), "EXACT_CONTROLS_FRESH_PATH")
            continue
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "EXACT_CONTROLS_REDIRECT")
        if part != path or directory:
            need(stat.S_ISDIR(info.st_mode), "EXACT_CONTROLS_DIRECTORY")
        else:
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "EXACT_CONTROLS_REGULAR_FILE")
    return path


def read(path, maximum=2*MIB):
    path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "EXACT_CONTROLS_READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "EXACT_CONTROLS_READ_CHANGED")
    return raw


def load(name, path, digest):
    raw = read(path)
    need(sha(raw) == digest and name not in sys.modules, "EXACT_CONTROLS_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def name(text):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in text.split(".")]


def report_for(units, indices):
    added, matched = [], []
    for index, unit in enumerate(units):
        (matched if index in indices else added).extend(deepcopy(unit[2]))
    return {"matched_unit_indices": indices, "units_checked": len(units)-len(indices),
        "units_matched": len(indices), "added_names": [row[0] for row in added],
        "matched_names": [row[0] for row in matched], "added_inventories": added,
        "matched_inventories": matched}


def controls(E, S, PE, K, C, output):
    cases, fixtures = [], {}
    for label, (relative, digest) in FIXTURES.items():
        raw = read(LOCAL/relative, MIB)
        need(sha(raw) == digest, "EXACT_CONTROLS_FIXTURE_PIN")
        item = PE.read_evidence(raw)
        need(item.unit_id == Path(relative).stem and item.document["semantic_id"] == S.semantic_id(),
             "EXACT_CONTROLS_FIXTURE_IDENTITY")
        fixtures[label] = item.document["unit"]

    def positive(label, call):
        check()
        call()
        cases.append({"case": label, "outcome": "PASS"})

    def negative(label, expected, call):
        check()
        try:
            call()
        except ValueError as error:
            need(str(error) == expected, "EXACT_CONTROLS_WRONG_REFUSAL:"+label+":"+str(error))
        else:
            raise AssertionError("EXACT_CONTROLS_MISSING_REFUSAL:"+label)
        cases.append({"case": label, "outcome": "EXPECTED_REFUSAL", "reason": expected})

    def renamed_definition(label):
        unit = deepcopy(fixtures["definition"])
        own = name(label)
        unit[1][1], unit[1][-1] = own, [own]
        unit[2][0][0], unit[2][0][4][-1] = own, [own]
        return unit

    opaque = renamed_definition("Inert.ExactOpaque")
    opaque[1] = [2, *opaque[1][1:5], opaque[1][-1]]
    opaque[2][0][1] = 3
    opaque[2][0][4][1] = 0
    added = renamed_definition("Inert.ActuallyAddedOnlyInMockRequest")
    units = [deepcopy(fixtures[key]) for key in ("theorem", "definition", "group", "list_group")]
    units.extend([opaque, added])
    request = {"units": units}
    base_report = report_for(units, list(range(5)))
    positive("mixed-theorem-definition-groups-opaque-and-addition",
             lambda: C.validate_partition(request, base_report))
    positive("all-additions", lambda: C.validate_partition(request, report_for(units, [])))
    need(C.POLICY == "ORDINARY_EXACT_INSTALLED_PUBLIC_MODULE_V2", "EXACT_CONTROLS_POLICY")
    for label, value in (("bool", [True]), ("unhashable", [[]]), ("duplicate", [0, 0]),
            ("unsorted", [2, 0]), ("negative", [-1]), ("out-of-range", [6]),
            ("all-matched", list(range(6)))):
        changed = deepcopy(base_report)
        changed["matched_unit_indices"] = value
        negative("partition-indices-"+label, "MODULE_EXPORT_MATCHED_INDICES",
                 lambda changed=changed: C.validate_partition(request, changed))
    for field, value in (("units_checked", True), ("units_matched", 4), ("matched_names", []),
            ("matched_inventories", []), ("added_names", []), ("added_inventories", [])):
        changed = deepcopy(base_report)
        changed[field] = value
        negative("partition-"+field, "MODULE_EXPORT_MATCHED_ADDED_PARTITION",
                 lambda changed=changed: C.validate_partition(request, changed))

    def mutation(label, source, mutate, code):
        changed = deepcopy(source)
        mutate(changed)
        negative(label, code, lambda: K.matched_realization(changed))

    # Every mutated body/type packet remains syntactically valid. These are
    # descriptor/metadata controls, not proof or installed-record controls.
    replacement = [E.EXPR_FORMAT, [[0]], [[1, 0]], 0]
    mutation("definition-descriptor-body-row-mismatch", units[1],
        lambda u: u[1].__setitem__(4, replacement), "ANCHOR_MATCHED_DESCRIPTOR_INVENTORY")
    mutation("definition-reducibility-row-mismatch", units[1],
        lambda u: u[2][0][4].__setitem__(1, [0]), "ANCHOR_MATCHED_DESCRIPTOR_INVENTORY")
    mutation("singleton-mutual-metadata", units[1],
        lambda u: u[1][-1].append(name("Inert.Other")), "ANCHOR_MATCHED_SINGLETON_ALL")
    mutation("opaque-row-body-mismatch", opaque,
        lambda u: u[2][0][4].__setitem__(0, replacement), "ANCHOR_MATCHED_DESCRIPTOR_INVENTORY")
    mutation("opaque-unsafe", opaque,
        lambda u: u[2][0][4].__setitem__(1, 1), "UNSAFE_INVENTORY")
    mutation("opaque-axiom-kind", opaque,
        lambda u: u[2][0].__setitem__(1, 0), "INVENTORY_KIND")
    group = fixtures["group"]
    type_index = next(i for i, row in enumerate(group[2]) if row[1] == 4)
    ctor_index = next(i for i, row in enumerate(group[2]) if row[1] == 5)
    rec_index = next(i for i, row in enumerate(group[2]) if row[1] == 6)
    mutation("group-descriptor-type-mismatch", group,
        lambda u: u[1][3][0].__setitem__(1, replacement), "ANCHOR_MATCHED_GROUP_TYPE")
    mutation("group-descriptor-constructor-mismatch", group,
        lambda u: u[1][3][0][2][0].__setitem__(1, replacement), "ANCHOR_MATCHED_GROUP_CONSTRUCTOR")
    mutation("group-constructor-owner-mismatch", group,
        lambda u: u[2][ctor_index][4].__setitem__(0, name("Inert.Other")),
        "ANCHOR_MATCHED_GROUP_CONSTRUCTOR")
    mutation("group-inductive-all-mismatch", group,
        lambda u: u[2][type_index][4][2].append(name("Inert.Other")), "ANCHOR_MATCHED_GROUP_TYPE")
    mutation("group-recursor-all-mismatch", group,
        lambda u: u[2][rec_index][4][0].append(name("Inert.Other")), "ANCHOR_MATCHED_GROUP_RECURSOR")
    mutation("group-recursor-rule-owner-mismatch", group,
        lambda u: u[2][rec_index][4][5][0].__setitem__(0, name("Inert.Other")),
        "ANCHOR_MATCHED_GROUP_RULE")
    mutation("group-recursor-rule-field-mismatch", group,
        lambda u: u[2][rec_index][4][5][0].__setitem__(1, 999), "ANCHOR_MATCHED_GROUP_RULE")
    mutation("group-missing-constructor", group,
        lambda u: u[2].pop(ctor_index), "GROUP_INVENTORY_MISSING_NAME")
    mutation("group-mixed-theorem-output", group,
        lambda u: u[2].append(deepcopy(units[0][2][0])), "ANCHOR_MATCHED_GROUP_KIND")

    store = K.Store()
    store.semantic_id, store.foundation_id = S.semantic_id(), S.foundation_id()
    store.implementation_id, store.support_id, store.store_binding = "7"*64, "8"*64, "9"*64
    store.root, store.basis_names = output/"inert-registry", frozenset()
    store.root.mkdir()
    store._live = lambda callback: callback()
    identities = [sha(b"INERT-NO-ACCEPTANCE\0"+E.canonical_json(unit)) for unit in units]
    targets = [{"name": added[2][0][0], "unit_id": identities[-1],
        "export_id": S.export_id(store.semantic_id, identities[-1], added[2][0][0])}]
    key = K.materialization_key(store.support_id, "", targets)
    plan_raw = store.plan()
    full_request = dict(request, schema=K.M.REQUEST_SCHEMA, semantic_id=store.semantic_id,
        foundation_id=store.foundation_id, context_root="a"*64,
        module_name=K.module_name("DMKNBridge_"+key), targets=[targets[0]["name"]],
        unit_ids=identities, anchor_id="", anchor_plan_sha256=sha(plan_raw))
    raw_request = E.canonical_json(full_request)
    selection = {"source_context_root": "a"*64, "targets": targets, "materialization_key": key,
        "request": {"bytes": len(raw_request), "sha256": sha(raw_request)},
        "anchor_plan": {"bytes": len(plan_raw), "sha256": sha(plan_raw)}}
    grant = K._Grant("b"*64, output/"never-created-grant", time.monotonic()+30,
                     None, E.canonical_json(selection), check)
    def grant_live(selected, callback):
        need(selected is grant and callback is check, "EXACT_CONTROLS_INERT_GRANT")
        callback()
    store._grant_live = grant_live
    full_report = dict(base_report, checking_passes=2)
    full_report.update({field: full_request[field] for field in ("semantic_id", "foundation_id",
        "context_root", "module_name", "targets", "unit_ids", "anchor_id", "anchor_plan_sha256")})

    class Captured(Exception):
        pass

    def derive(report, request_raw=raw_request):
        captured = []
        def capture(value):
            captured.append(deepcopy(value))
            raise Captured()
        live = {"request": request_raw, "report": report, "artifact_parts": [], "event_files": {}}
        with patch.object(store, "_units", capture):
            try:
                store._commit_generated(grant, live, check)
            except Captured:
                pass
        need(len(captured) == 1, "EXACT_CONTROLS_PRECOPY_CAPTURE")
        return captured[0]

    registered = derive(full_report)
    need([row["realization"] for row in registered] == ["installed-singleton-theorem",
         *(["installed-exact-nontheorem"]*4), "added"], "EXACT_CONTROLS_DERIVED_TAGS")
    positive("protected-request-derived-tags", lambda: store._units(registered))
    # The public report schema rejects invented fields separately. At this
    # private seam they cannot influence the tag derived from the protected unit.
    forged_labels = dict(full_report, realization="added", unit_realizations=["added"]*6)
    need(derive(forged_labels) == registered, "EXACT_CONTROLS_REPORT_TAG_NOT_AUTHORITY")
    positive("report-label-cannot-select-realization", lambda: None)
    changed_request = deepcopy(full_request)
    changed_request["units"][1][1][4] = replacement
    negative("live-request-pin-before-tag", "ANCHOR_LIVE_REQUEST_PIN",
             lambda: derive(full_report, E.canonical_json(changed_request)))
    for label, indices in (("all-matched", list(range(6))), ("unhashable", [[]])):
        changed = dict(full_report, matched_unit_indices=indices)
        negative("commit-indices-"+label, "ANCHOR_MATCHED_INDICES", lambda changed=changed: derive(changed))
    for index, tag, code in ((0, "installed-exact-nontheorem", "ANCHOR_MATCHED_EXACT_NONTHEOREM"),
            (1, "installed-singleton-theorem", "ANCHOR_MATCHED_SINGLETON"),
            (2, "unknown-match", "ANCHOR_REALIZATION")):
        changed = deepcopy(registered)
        changed[index]["realization"] = tag
        negative("persisted-tag-family-"+str(index), code, lambda changed=changed: store._units(changed))
    changed = deepcopy(registered)
    changed[2]["outputs"] = [row for row in changed[2]["outputs"] if row["kind"] != 4]
    negative("persisted-generated-owner-required", "ANCHOR_MATCHED_EXACT_NONTHEOREM",
             lambda: store._units(changed))

    _, mapping, added_names, matched_names = store._units(registered)
    context = {"semantic_id": store.semantic_id, "foundation_id": store.foundation_id,
        "implementation_id": store.implementation_id,
        "bindings": {key: value[0] for key, value in mapping.items()}}
    text = "DMKNBridge_"+key
    artifact_directory = store.root/"operations"/grant.identifier/"modules"
    artifact_directory.mkdir(parents=True)
    parts = []
    for suffix in K.PART_SUFFIXES:
        path = artifact_directory/(text+suffix)
        data = ("INERT-NOT-LEAN:"+suffix).encode("ascii")
        with path.open("xb") as stream:
            stream.write(data)
        parts.append({"path": path.relative_to(store.root).as_posix(), "bytes": len(data), "sha256": sha(data)})
    events = {event: {"path": f"operations/{grant.identifier}/events/{event}", "bytes": 1,
        "sha256": sha(b"X")} for event in K.EVENT_NAMES}
    record = {"schema": K.RECORD_SCHEMA, "store_binding": store.store_binding,
        "support_id": store.support_id, "operation_id": grant.identifier,
        "source_context_root": "a"*64, "parent_anchor_id": "", "module_name": full_request["module_name"],
        "direct_imports": [name("Init")], "targets": targets, "materialization_key": key,
        "artifact_parts": parts, "units": registered, "added_names": added_names,
        "matched_names": matched_names, "event_files": events}
    record_raw = E.canonical_json(record)
    anchor_id = sha(K.RECORD_DOMAIN+record_raw)
    (store.root/"records").mkdir()
    with (store.root/"records"/(anchor_id+".json")).open("xb") as stream:
        stream.write(record_raw)
    positive("record-schema-roundtrip", lambda: store._record(record_raw, anchor_id))
    def restore():
        with patch.object(E, "inspect_unit", forbidden):
            view = store.load(anchor_id, context, check)
        restored = E.strict_json(view.plan_raw)["bindings"]
        need(restored == registered and [row["realization"] for row in restored] ==
             [row["realization"] for row in registered], "EXACT_CONTROLS_RESTORE_TAGS")
        need(len(view.frontier.units) == 6, "EXACT_CONTROLS_RESTORE_WHOLE_UNITS")
    positive("persisted-exact-tags-restored-without-proof-decoding", restore)
    missing = deepcopy(context)
    del missing["bindings"][E.name_key(group[2][ctor_index][0])]
    negative("restore-every-group-sibling-warrant", "ANCHOR_CURRENT_CONTEXT_MISMATCH",
             lambda: store.load(anchor_id, missing, check))
    old_support = store.support_id
    store.support_id = "c"*64
    negative("old-support-record-refused-no-migration", "ANCHOR_RECORD_SUPPORT",
             lambda: store.load(anchor_id, context, check))
    store.support_id = old_support
    need(read(store.root/"records"/(anchor_id+".json")) == record_raw,
         "EXACT_CONTROLS_REFUSAL_PRESERVES_RECORD")
    for relative, digest in FIXTURES.values():
        need(sha(read(LOCAL/relative, MIB)) == digest, "EXACT_CONTROLS_FIXTURE_CHANGED")
    return cases


def main(args):
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "EXACT_CONTROLS_CONTEXT")
    output = Path(args.output)
    need(output.is_relative_to(LOCAL), "EXACT_CONTROLS_OUTPUT_ROOT")
    ordinary(output, directory=True, fresh=True).mkdir()
    with ExitStack() as guards:
        for target in ("subprocess.Popen", "socket.socket", "socket.create_connection", "sqlite3.connect"):
            guards.enter_context(patch(target, forbidden))
        # No package bootstrap, owner module, owner database or runtime import.
        modules = {name: load(name, ROOT/relative, digest)
                   for name, (relative, digest) in SOURCE_PINS.items()}
        E, S, PE = (modules[name] for name in ("ordinary_evidence", "ordinary_semantics", "portable_evidence"))
        admission = ModuleType("ordinary_admission")
        admission.E, admission.S, admission.need, admission.sha = E, S, need, sha
        admission.C = SimpleNamespace(hexid=E._hex, ordinary=ordinary, read_bounded=read)
        stubs = {"ordinary_admission": admission, "ordinary_contribution": ModuleType("ordinary_contribution"),
                 "portable_preview": ModuleType("portable_preview")}
        guards.enter_context(patch.dict(sys.modules, stubs))
        K = load("anchor_store", BASE/"anchor_store.py", args.store_sha256)
        C = load("_exact_module_controller", BASE/"module_export.py", args.controller_sha256)
        cases = controls(E, S, PE, K, C, output)
    check()
    result = {"status": "PASS_FOCUSED_EXACT_INSTALLED_METADATA_CONTROLS", "cases": cases,
        "controller_sha256": args.controller_sha256, "store_sha256": args.store_sha256,
        "source_pins": SOURCE_PINS, "fixture_pins": FIXTURES,
        "wall_seconds": time.monotonic()-START, "controller_cpu_seconds": time.process_time()-CPU,
        "owner_opens": 0, "native_operations": 0,
        "claim": "INERT_PARTITION_TAG_AND_RECORD_RESTORE_ONLY_NOT_INSTALLED_MATCH_OR_ACCEPTANCE"}
    raw = json.dumps(result, sort_keys=True, allow_nan=False, separators=(",", ":")).encode("ascii")
    need(len(raw) <= MIB, "EXACT_CONTROLS_REPORT_BOUND")
    pending = ordinary(output/"CONTROLS.pending.json", fresh=True)
    final = ordinary(output/"CONTROLS.json", fresh=True)
    with pending.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    need(read(pending, MIB) == raw, "EXACT_CONTROLS_REPORT_READBACK")
    check()
    # main requires Windows: same-volume rename refuses an existing destination.
    os.rename(pending, final)
    print(json.dumps(result, sort_keys=True, allow_nan=False), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for field in ("controller-sha256", "store-sha256", "output"):
        parser.add_argument("--"+field, required=True)
    main(parser.parse_args())

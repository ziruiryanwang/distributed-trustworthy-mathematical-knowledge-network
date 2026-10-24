"""Changed-boundary pure frontier controls; no native, owner or network calls.

Retained mathematical bytes are real; the warrant/frontier maps here are explicit
test fixtures, not registration or mathematical acceptance. The earlier closure
campaign is not repeated. Its pinned loading/IO helpers are reused only.
"""
from __future__ import annotations

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
import subprocess
import sys
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HELPER = ROOT/"software/v5/ordinary_module_bridge/closure_controls.py"
HELPER_SHA = "8015039fff02678d74adda770042309fb6a3a54085e8b787594414430163dc7f"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def helper():
    with HELPER.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == HELPER_SHA, "ANCHOR_CONTROL_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_anchor_control_helpers", HELPER)
    value = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = value
    exec(compile(raw, str(HELPER), "exec"), value.__dict__)
    return value


def controls(A, C, loaded, H):
    E, S, PE = A.E, A.S, A.PE
    semantic, foundation = S.semantic_id(), S.foundation_id()
    inventory = loaded.installation.read("inventory", MIB)
    raws = {Path(path).stem: H.read(H.LOCAL/path, MIB) for path in H.FIXTURES}
    need({path: H.sha(raws[Path(path).stem]) for path in H.FIXTURES} == H.FIXTURES,
         "ANCHOR_CONTROL_FIXTURES")
    items = {unit: PE.read_evidence(raw) for unit, raw in raws.items()}
    mapping = {E.name_key(row[0]): S.basis_symbol_id(semantic, foundation, row[0])
               for row in json.loads(inventory)}
    targets, names = {}, {}
    for unit, item in items.items():
        need(unit == item.unit_id, "ANCHOR_CONTROL_UNIT_PIN")
        rows = item.document["unit"][2]
        need(len(rows) == 1, "ANCHOR_CONTROL_SINGLETON_FIXTURE")
        name = rows[0][0]
        key = E.name_key(name)
        targets[unit] = {"name": name, "unit_id": unit,
                         "export_id": S.export_id(semantic, unit, name)}
        mapping[key], names[key] = targets[unit]["export_id"], unit
    anchored = (H.TWICE, H.TWICE_EQ)
    def frontier(units=anchored):
        return C.AnchorFrontier("a"*64, tuple((unit, ((E.name_key(targets[unit]["name"]),
            targets[unit]["export_id"]),)) for unit in units))

    def run(*, target_ids=(H.FOUR,), selected=None, anchor=None, warrants=None,
            fetch=None, calls=None, visits=None, **changes):
        chosen = mapping if warrants is None else warrants
        def warranted(name):
            key = E.name_key(name)
            if visits is not None:
                visits.append(key)
            return chosen.get(key)
        def acquire(name, identity, maximum):
            key = E.name_key(name)
            if calls is not None:
                calls.append(names[key])
            raw = raws[names[key]]
            need(identity == mapping[key] and len(raw) <= maximum, "ANCHOR_CONTROL_FETCH_CONTRACT")
            return raw
        options = dict(admission_api=A, semantic_id=semantic, foundation_id=foundation,
            context_root=H.PARENT, inventory_raw=inventory,
            targets=copy.deepcopy([targets[unit] for unit in target_ids] if selected is None else selected),
            module_name=H.name("DMKNBridge_"+"c"*64), warranted_symbol=warranted,
            fetch_evidence=acquire if fetch is None else fetch, check_budget=H.check,
            anchor_frontier=frontier() if anchor is None else anchor, anchor_plan_sha256="b"*64)
        options.update(changes)
        return C.collect_closure(**options)

    def rejected(call, fragment):
        try:
            call()
        except ValueError as error:
            need(fragment in str(error), "ANCHOR_CONTROL_WRONG_REFUSAL:"+str(error))
        else:
            raise AssertionError("ANCHOR_CONTROL_MISSING_REFUSAL:"+fragment)

    def delta_only_no_old_decoding():
        calls, visits = [], []
        original = PE.read_evidence
        def delta_reader(raw, *args, **kwargs):
            need(raw not in (raws[H.TWICE], raws[H.TWICE_EQ]), "ANCHOR_CONTROL_OLD_PROOF_DECODED")
            return original(raw, *args, **kwargs)
        with patch.object(PE, "read_evidence", delta_reader):
            value = run(calls=calls, visits=visits, limits=C.Limits(max_units=1))
        need(value.ordered_unit_ids == (H.FOUR,) and value.ordered_evidence == (raws[H.FOUR],) and
             calls == [H.FOUR] and value.fetch_calls == 1 and value.acquired_bytes == len(raws[H.FOUR]),
             "ANCHOR_CONTROL_DELTA_ONLY")
        need(value.anchor_id == "a"*64 and value.cut_unit_ids == tuple(sorted(anchored)) and
             value.status == "READY_FOR_NATIVE_MODULE_RECHECK" and value.mathematical_acceptance is False,
             "ANCHOR_CONTROL_CUT_IDENTITIES")
        need(len(visits) == len(set(visits)) == 584, "ANCHOR_CONTROL_ONCE_PER_WARRANT")
        request = E.strict_json(value.request)
        need(request["schema"] == "DMKN_ORDINARY_MODULE_REQUEST_V2" and
             request["anchor_id"] == "a"*64 and request["anchor_plan_sha256"] == "b"*64 and
             request["units"] == [items[H.FOUR].document["unit"]] and
             request["unit_ids"] == [H.FOUR], "ANCHOR_CONTROL_DELTA_REQUEST")

    def all_anchored_no_fetch_or_planner():
        with patch.object(A, "_plan", H.forbidden), patch.object(PE, "read_evidence", H.forbidden):
            value = run(target_ids=(H.TWICE_EQ,), fetch=H.forbidden)
        need(value.request is None and value.ordered_unit_ids == () and value.ordered_evidence == () and
             value.fetch_calls == value.acquired_bytes == value.acquired_nodes == 0 and
             value.cut_unit_ids == (H.TWICE_EQ,) and value.status == "REUSED_LOCAL_MODULE_ANCHOR" and
             value.mathematical_acceptance is False, "ANCHOR_CONTROL_ZERO_NATIVE_REUSE_INPUT")

    def every_frontier_warrant_is_required():
        # TWICE is not a target and traversal is empty, but its registration must
        # still agree with the selected current owner context.
        altered = dict(mapping)
        del altered[E.name_key(targets[H.TWICE]["name"])]
        rejected(lambda: run(target_ids=(H.TWICE_EQ,), warrants=altered, fetch=H.forbidden), "WARRANT")
        altered[E.name_key(targets[H.TWICE]["name"])] = "0"*64
        rejected(lambda: run(target_ids=(H.TWICE_EQ,), warrants=altered, fetch=H.forbidden), "WARRANT")

    def malformed_frontiers():
        f = frontier()
        for malformed in (C.AnchorFrontier("", f.units), C.AnchorFrontier("a"*64, ()),
                          C.AnchorFrontier("a"*64, f.units+f.units[:1]),
                          C.AnchorFrontier("a"*64, ((f.units[0][0], ()),))):
            rejected(lambda m=malformed: run(anchor=m, fetch=H.forbidden), "MODULE_CLOSURE")
        rejected(lambda: run(anchor=C.AnchorFrontier("bad", f.units), fetch=H.forbidden), "HASH_ENCODING")
        changed = C.AnchorFrontier("a"*64, ((H.TWICE, ((f.units[0][1][0][0], "0"*64),)),))
        rejected(lambda: run(anchor=changed, fetch=H.forbidden), "MODULE_CLOSURE")

    def target_unit_identity_is_not_just_name():
        changed = copy.deepcopy(targets[H.TWICE])
        changed["unit_id"] = H.FOUR
        changed["export_id"] = S.export_id(semantic, H.FOUR, changed["name"])
        rejected(lambda: run(selected=[changed], fetch=H.forbidden), "MODULE_CLOSURE")

    def partial_frontier_overlap_refuses():
        # Conflicting declared ownership of one exact name cannot be another
        # whole-unit frontier, even when the injected warrant map repeats it.
        f = frontier()
        overlap = C.AnchorFrontier(f.anchor_id, f.units+((H.FOUR, f.units[0][1]),))
        rejected(lambda: run(anchor=overlap, fetch=H.forbidden), "MODULE_CLOSURE")

    def unanchored_dependency_still_needed():
        calls = []
        value = run(anchor=frontier((H.TWICE,)), calls=calls, limits=C.Limits(max_units=2))
        need(value.ordered_unit_ids == (H.TWICE_EQ, H.FOUR) and set(calls) == {H.TWICE_EQ, H.FOUR} and
             value.cut_unit_ids == (H.TWICE,), "ANCHOR_CONTROL_DO_NOT_CUT_WARRANT_ONLY")
        rejected(lambda: run(anchor=frontier((H.TWICE,)), limits=C.Limits(max_units=1)), "UNIT_BOUND")

    return [("delta-only-and-no-old-proof-decoding", delta_only_no_old_decoding),
        ("all-anchored-zero-fetch-zero-planner", all_anchored_no_fetch_or_planner),
        ("all-frontier-warrants-including-unreached", every_frontier_warrant_is_required),
        ("frontier-schema-id-group-boundaries", malformed_frontiers),
        ("exact-target-unit-identity", target_unit_identity_is_not_just_name),
        ("conflicting-unit-name-ownership", partial_frontier_overlap_refuses),
        ("unanchored-proof-dependencies-still-fetched", unanchored_dependency_still_needed)]


def main(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "ANCHOR_CONTROL_PYTHON")
    H, results = helper(), []
    with ExitStack() as guards:
        for target, attr in ((sqlite3, "connect"), (subprocess, "Popen"),
                             (socket.socket, "connect"), (socket.socket, "connect_ex")):
            guards.enter_context(patch.object(target, attr, H.forbidden))
        loaded = H.selected_package(args)
        for operation in ("open", "preflight", "admit", "initialize"):
            guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, operation, H.forbidden))
        output = loaded.A.C.ordinary(Path(args.output), directory=True)
        collector = H.load_source(Path(__file__).absolute().parent/"module_closure.py",
            args.collector_sha256, "_anchor_control_collector")
        for label, call in controls(loaded.A, collector, loaded, H):
            H.check()
            try:
                call()
                results.append({"group": label, "ok": True})
            except BaseException as error:
                results.append({"group": label, "ok": False, "error_type": type(error).__name__,
                                "error": str(error)[:1000]})
        for relative, digest in H.FIXTURES.items():
            need(H.sha(H.read(H.LOCAL/relative, MIB)) == digest, "ANCHOR_CONTROL_SAVED_CHANGED")
    report = {"ok": len(results) == 7 and all(row["ok"] for row in results), "groups": results,
        "collector_sha256": args.collector_sha256, "owner_opens": 0, "native_operations": 0,
        "claim": "PURE_FRONTIER_CONTROLS_UNDER_TEST_WARRANTS_NOT_REGISTERED_MATHEMATICS"}
    H.save(output/"FRONTIER-CONTROLS.json", report)
    print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output", "collector-sha256"):
        parser.add_argument("--"+name, required=True)
    raise SystemExit(main(parser.parse_args()))

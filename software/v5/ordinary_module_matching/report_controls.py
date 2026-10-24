"""Focused V2 report controls; mathematical/native gates are not simulated passes.

Only the actual controller's pure partition validator and worker's pending-report
reader run. Imports of owner APIs are inert stubs; native/database/network calls
are forbidden. Invented report rows carry no mathematical authority.
"""
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
import subprocess
import sys
import time
from types import ModuleType
from unittest.mock import patch

START, CPU = time.monotonic(), time.process_time()
ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
CONTROLLER_SHA = "7f10008692bf1bd361d2fdd2caab41f8059930be32ac98fc8412c0243716cff0"
WORKER_SHA = "3872864a27e9fbb12e56eaa2ebabd9299d97a336c5e58840648a86b5c371df18"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def check():
    need(time.monotonic()-START < 35 and time.process_time()-CPU < 20,
         "REPORT_CONTROLS_ORIGINAL_ALLOWANCE")


def forbidden(*_, **__):
    raise AssertionError("REPORT_CONTROLS_FORBIDDEN_EXTERNAL_CALL")


def load(name, path, digest):
    need(path.is_absolute() and path.is_relative_to(ROOT) and ".." not in path.parts,
         "REPORT_CONTROLS_SELECTED_LOCAL_SOURCE")
    with path.open("rb") as stream:
        raw = stream.read(MIB+1)
    need(0 < len(raw) <= MIB and hashlib.sha256(raw).hexdigest() == digest,
         "REPORT_CONTROLS_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def theorem(label):
    name = [[0, {"$bytes": list(label.encode("ascii"))}]]
    # Deliberately inert type/proof placeholders: these tests validate accounting,
    # not decoder validity, theorem truth or any native matching premise.
    descriptor = [1, name, [], ["INERT-TYPE"], ["INERT-PROOF"], [name]]
    return [[], descriptor, [[name, 2, [], descriptor[3], [descriptor[4], [name]]]]]


def report_for(request, indices):
    matched, added = [], []
    for i, unit in enumerate(request["units"]):
        (matched if i in indices else added).extend(deepcopy(unit[2]))
    return {"matched_unit_indices": indices, "units_checked": len(request["units"])-len(indices),
        "units_matched": len(indices), "added_names": [row[0] for row in added],
        "matched_names": [row[0] for row in matched], "added_inventories": added,
        "matched_inventories": matched}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("controller", "worker", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "REPORT_CONTROLS_CONTEXT")
    output = Path(args.output)
    need(output.is_absolute() and output.is_relative_to(ROOT / "experiments/v5-local-checks") and
         ".." not in output.parts and not os.path.lexists(output) and output.parent.is_dir(),
         "REPORT_CONTROLS_FRESH_OUTPUT")
    output.mkdir()
    cases = []

    def positive(label, call):
        check()
        call()
        cases.append({"case": label, "outcome": "PASS"})

    def negative(label, expected, call):
        check()
        try:
            call()
        except ValueError as error:
            need(str(error) == expected, "REPORT_CONTROLS_WRONG_REFUSAL:"+label+":"+str(error))
        else:
            raise AssertionError("REPORT_CONTROLS_MISSING_REFUSAL:"+label)
        cases.append({"case": label, "outcome": "EXPECTED_REFUSAL", "reason": expected})

    stubs = {name: ModuleType(name) for name in
             ("ordinary_admission", "ordinary_contribution", "portable_preview", "module_closure")}
    stubs["ordinary_admission"].need = need
    with ExitStack() as stack:
        stack.enter_context(patch.dict(sys.modules, stubs))
        for target in ("subprocess.Popen", "socket.socket", "socket.create_connection", "sqlite3.connect"):
            stack.enter_context(patch(target, forbidden))
        controller = load("_matching_report_controller", Path(args.controller), CONTROLLER_SHA)
        worker = load("_matching_report_worker", Path(args.worker), WORKER_SHA)
        request = {"units": [theorem(label) for label in ("A", "B", "C", "D")]}
        base = report_for(request, [0, 2])
        positive("mixed-ordered-partition", lambda: controller.validate_partition(request, base))
        positive("all-additions", lambda: controller.validate_partition(request, report_for(request, [])))
        for label, value in (("not-list", (0,)), ("boolean", [True]), ("float", [0.0]),
                ("duplicate", [0, 0]), ("unsorted", [2, 0]), ("negative", [-1]),
                ("out-of-range", [4]), ("all-matched", [0, 1, 2, 3])):
            changed = deepcopy(base)
            changed["matched_unit_indices"] = value
            negative("indices-"+label, "MODULE_EXPORT_MATCHED_INDICES",
                     lambda changed=changed: controller.validate_partition(request, changed))
        for label in ("definition-kind", "mutual-metadata", "extra-output", "proof-inventory-mismatch"):
            changed_request = deepcopy(request)
            unit = changed_request["units"][0]
            if label == "definition-kind":
                unit[1][0] = 0
            elif label == "mutual-metadata":
                unit[1][5].append(request["units"][1][1][1])
            elif label == "extra-output":
                unit[2].append(deepcopy(unit[2][0]))
            else:
                unit[2][0][4][0] = ["DIFFERENT-INERT-PROOF"]
            negative(label, "MODULE_EXPORT_MATCHED_SINGLETON_THEOREM",
                     lambda changed_request=changed_request: controller.validate_partition(changed_request, base))
        changes = (("units_checked", 3), ("units_checked", True), ("units_matched", 1),
                   ("units_matched", 2.0), ("added_names", []), ("added_inventories", []),
                   ("matched_names", []), ("matched_inventories", []))
        for i, (field, value) in enumerate(changes):
            changed = deepcopy(base)
            changed[field] = value
            negative("partition-field-"+str(i), "MODULE_EXPORT_MATCHED_ADDED_PARTITION",
                     lambda changed=changed: controller.validate_partition(request, changed))
        pending = {key: [] for key in worker.REPORT_FIELDS}
        pending.update(schema=worker.PENDING_SCHEMA, assurance=worker.PENDING_ASSURANCE)
        for label in ("v2", "v1", "missing-partition-field"):
            value = deepcopy(pending)
            if label == "v1":
                value["schema"] = "DMKN_ORDINARY_MODULE_PENDING_V1"
            if label == "missing-partition-field":
                del value["matched_unit_indices"]
            path = output / (label+".json")
            raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("ascii")
            with path.open("xb") as stream:
                stream.write(raw)
            selected = worker.pin(path, 8*MIB)
            call = lambda path=path, selected=selected: worker.read_pending(path, selected)
            if label == "v2":
                positive("worker-v2-field-shape-only", call)
            else:
                negative("worker-"+label, "MODULE_WORKER_PENDING_REQUIRED", call)
    check()
    result = {"status": "PASS_SELECTED_REPORT_CONTROLS", "cases": cases,
        "source_pins": {"controller": CONTROLLER_SHA, "worker": WORKER_SHA},
        "wall_seconds": time.monotonic()-START, "controller_cpu_seconds": time.process_time()-CPU,
        "scope": "PURE_ACCOUNTING_AND_SCHEMA_ONLY_NOT_NATIVE_MATCHING_OR_ACCEPTANCE"}
    with (output / "REPORT.json").open("x", encoding="ascii") as stream:
        json.dump(result, stream, sort_keys=True, allow_nan=False)
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

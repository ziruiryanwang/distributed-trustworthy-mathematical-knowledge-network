"""Finite, native-free controls for the offline ordinary operator preparer.

Only fresh synthetic JSON, empty directories and configuration outputs are used.
No existing owner state is opened and no mathematics, command, native process or
network operation is executed. Root selects a separate finite runtime allocation.
All fixtures and partial outputs remain for inspection; this suite deletes none.
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
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PROFILE = "9c41b9a3fe36f7283af130ac6ef290e82c2a78c432980b2bea75ccdcf197a6d4"
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()
CASES = []


def need(condition, code):
    if not condition:
        raise AssertionError(code)


def check():
    need(time.monotonic() - START < 60 and time.process_time() - CPU < 30,
         "CONTROL_ORIGINAL_ALLOWANCE")


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      allow_nan=False, separators=(",", ":")).encode("utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def name(*parts):
    return [[0, {"$bytes": list(part.encode("utf-8"))}] for part in parts]


def export(semantic, unit, encoded_name):
    return digest(b"DMKN-ORDINARY-EXPORT-V2\0" + canonical([semantic, unit, encoded_name]))


def fresh(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def ordinary_path(path, *, fresh_directory=False):
    need(path.is_absolute() and path != Path(path.anchor) and ".." not in path.parts,
         "CONTROL_PATH")
    target = path.parent if fresh_directory else path
    for part in (*reversed(target.parents), target):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             (getattr(info, "st_file_attributes", 0) & 0x400), "CONTROL_REDIRECT")
    if fresh_directory:
        need(target.is_dir() and not os.path.lexists(path), "CONTROL_FRESH")


def load(path):
    ordinary_path(path)
    info = path.stat()
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and
         0 < info.st_size < 2*MIB, "CONTROL_SOURCE")
    raw = path.read_bytes()
    spec = importlib.util.spec_from_file_location("_operator_prepare_control", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module, {"bytes": len(raw), "sha256": digest(raw)}


class Fixture:
    def __init__(self, root):
        self.root = root
        self.inputs, self.outputs = root / "inputs", root / "outputs"
        self.inputs.mkdir(); self.outputs.mkdir()
        self.serial = 0
        self.catalog, self.custody = root / "synthetic-catalog", root / "synthetic-custody"
        self.catalog.mkdir(); self.custody.mkdir()
        self.project, self.bundle = root / "synthetic-project", root / "synthetic-bundle"
        self.project.mkdir(); self.bundle.mkdir()
        self.index = root / "synthetic-index"
        self.index.mkdir()
        self.state = {"catalog": str(self.catalog), "custody": str(self.custody),
                      "store_id": "1"*64}
        self.custody_limits = {"objects": 100, "exports": 1000,
                               "logical_bytes": MIB, "db_pages": 256}
        self.index_limits = {"max_objects": 100, "max_postings": 1000,
                             "max_features": 1000, "max_snapshots": 100,
                             "max_logical_bytes": MIB, "max_db_pages": 256}
        self.contacts = {"synthetic-peer": {"host": "127.0.0.1", "port": 39301,
            "tls": False, "server_name": None, "ca_file": None, "ca_sha256": None}}
        self.semantic, self.parent, self.accepted = "2"*64, "3"*64, "4"*64
        self.target = {"name": name("Synthetic", "new_concept"), "unit_id": "5"*64}
        self.target["export_id"] = export(self.semantic, self.target["unit_id"], self.target["name"])
        self.target2 = {"name": name("Synthetic", "new_law"), "unit_id": "6"*64}
        self.target2["export_id"] = export(self.semantic, self.target2["unit_id"], self.target2["name"])
        self.manifest = {"schema": "DMKN_ORDINARY_BASELINE_BUNDLE_V1",
            "semantic_id": self.semantic, "batches": [[
                {"unit_id": self.target["unit_id"], "raw_sha256": "7"*64, "raw_bytes": 123},
                {"unit_id": self.target2["unit_id"], "raw_sha256": "8"*64, "raw_bytes": 234}]]}
        manifest_raw = canonical(self.manifest)
        fresh(self.bundle / "manifest.json", manifest_raw)
        self.manifest_ref = {"path": str(self.bundle / "manifest.json"), "sha256": digest(manifest_raw)}
        common = {"ok": True, "profile_sha256": PROFILE, "implementation_id": "9"*64,
                  **self.state}
        self.init = {**common, "operation": "init", "result": {
            "status": "INITIALIZED_LOCAL_OWNER", "basis": {
                "status": "CHECKED", "local_root": self.parent, "units_checked": 456,
                "retained_unit_ids": []}}}
        self.producer = {"ok": True, "operation": "produce-baseline",
            "profile_sha256": PROFILE, "implementation_id": "9"*64,
            "mathematical_acceptance": False, "result": {
                "schema": "DMKN_ORDINARY_BASELINE_PRODUCTION_OBSERVATION_V1",
                "status": "PRODUCED_INERT_BASELINE_NOT_ACCEPTED",
                "semantic_id": self.semantic, "mathematical_acceptance": False,
                "output_directory": str(self.bundle), "manifest_path": self.manifest_ref["path"],
                "manifest": {"bytes": len(manifest_raw), "sha256": digest(manifest_raw)},
                "targets": [self.target, self.target2], "batches": 1,
                "native_accounting_complete": True, "native_closure_known": True}}
        self.intake = {**common, "operation": "intake-baseline", "result": {
            "status": "BASELINE_INTAKE_COMPLETE", "manifest_sha256": digest(manifest_raw),
            "selected_root": self.parent, "local_root": self.accepted,
            "batches": [{"batch": 0, "status": "CHECKED", "local_root": self.accepted,
                         "units_checked": 2}], "ordinary_library_registered": False,
            "peer_transferable_warrant": False}}
        self.selection = {"provider": "synthetic-peer", "snapshot_id": "a"*64,
            "record": {"schema": "DMKN_FORMAL_FEATURE_RECORD_V3",
                "namespace": "b"*64, "kind": "ordinary-lean-export-v2",
                "object_id": self.target["export_id"], "object_sha256": "c"*64,
                "object_bytes": 4096, "features": ["d"*64], "locator": {
                    "schema": "DMKN_ORDINARY_LEAN_EXPORT_LOCATOR_V2",
                    "semantic_id": self.semantic, "unit_id": self.target["unit_id"],
                    "export_name": self.target["name"]}}}
        self.find = {"ok": True, "operation": "find", "profile_sha256": PROFILE,
            "result": {"operation": "find", "status": "INCOMPLETE_SEARCH",
                       "mathematical_acceptance": False, "cleanup_errors": [],
                       "matches": [self.selection], "global_complete": False,
                       "verified_scan_coverage": False}}
        self.preview = {"ok": True, "operation": "preview", "profile_sha256": PROFILE,
            "result": {"operation": "preview", "status": "PREVIEW_BOUND_NOT_ACCEPTED",
                "mathematical_acceptance": False, "cleanup_errors": [],
                "selection": self.selection, "preview": {
                    "schema": "DMKN_ORDINARY_LEAN_TYPE_PREVIEW_V2", "semantic_id": self.semantic,
                    "unit_id": self.target["unit_id"], "export_name": self.target["name"],
                    "type_bindings": [[self.target2["name"], self.target2["export_id"]]]}}}

    def ref(self, value, *, raw=None):
        self.serial += 1
        path = self.inputs / ("input-%03d.json" % self.serial)
        encoded = canonical(value) if raw is None else raw
        fresh(path, encoded)
        return {"path": str(path), "sha256": digest(encoded)}

    def output(self):
        self.serial += 1
        return self.outputs / ("prepare-%03d" % self.serial)

    def operation_output(self):
        self.serial += 1
        return str(self.outputs / ("operation-%03d" % self.serial))

    def request(self, action):
        common = {"action": action}
        if action in ("init", "receive", "intake-baseline", "publish", "serve"):
            common.update(state=deepcopy(self.state), custody_limits=deepcopy(self.custody_limits))
        if action in ("find", "preview", "receive", "inspect", "authoring-offers"):
            common["contacts"] = deepcopy(self.contacts)
        if action not in ("init", "intake-baseline"):
            common["operation_output"] = self.operation_output()
        if action == "init":
            common["state"].update(catalog=str(self.root / "fresh-catalog"),
                                   custody=str(self.root / "fresh-custody"))
        elif action == "find":
            common.update(providers=["synthetic-peer"], specs=[{"tag": "type-symbol",
                "symbol": {"kind": "portable-symbol", "symbol_id": self.target["export_id"]}}],
                limits={"providers": 1, "snapshots": 2, "requests": 4, "pages": 2,
                    "examined": 32, "candidates": 8, "bytes": 65536, "wall_ms": 1000, "inflight": 1},
                offer={"max_bytes": 4096, "max_expanded_bytes": 4096, "max_age_ms": 1000},
                page={"scanned": 32, "matches": 8, "bytes": 8192, "timeout_ms": 100,
                    "record_probes": 64, "node_reads": 128, "hash_calls": 1024, "sql_vm_steps": 10000})
        elif action in ("preview", "receive"):
            common.update(find_report=self.ref(self.find), match_index=0)
            if action == "preview":
                common["limits"] = {"requests": 1, "reply_bytes": 8192}
            else:
                common.update(parent_report=self.ref(self.init), dependency_policy="selected-unit-only",
                    limits={"requests": 4, "reply_bytes": 65536, "units": 4,
                        "unit_bytes": 8192, "total_bytes": 32768, "missing": 16,
                        "preflights": 5, "locator_bytes": 4096})
        elif action == "produce-baseline":
            common.update(project_search_paths=[str(self.project)], modules=[name("Synthetic")],
                output_names=[self.target["name"]], approve_local_project=True, spool_mib=144)
        elif action in ("inspect", "authoring-offers"):
            common["preview_report"] = self.ref(self.preview)
            if action == "inspect":
                common.update(binding_index=0, limits={"requests": 2, "reply_bytes": 12288,
                              "locator_bytes": 4096, "unit_bytes": 8192})
            else:
                common["limits"] = {"requests": 1, "reply_bytes": 32768, "max_offers": 8}
        elif action == "intake-baseline":
            common.update(parent_report=self.ref(self.init), producer_report=self.ref(self.producer),
                          bundle_directory=str(self.bundle), manifest=deepcopy(self.manifest_ref))
        elif action == "publish":
            common.update(producer_report=self.ref(self.producer), intake_report=self.ref(self.intake),
                target_indices=[1, 0], index={"path": str(self.index), "limits": deepcopy(self.index_limits),
                    "create": False}, max_unit_bytes=8192, max_total_bytes=32768)
        elif action == "serve":
            common.update(index={"path": str(self.index), "limits": deepcopy(self.index_limits),
                "create": False}, host="127.0.0.1", port=0, tls=None, lease_seconds=10,
                cleanup_seconds=10, limits={"max_connections": 2, "max_requests": 10,
                    "max_reply_bytes": 65536, "operation_ms": 1000},
                share_all_custody=True, exclusive=True)
        else:
            raise AssertionError("CONTROL_UNKNOWN_ACTION")
        return common


def argv_value(arguments, flag):
    need(arguments.count(flag) == 1, "CONTROL_SINGLE_ARGUMENT:" + flag)
    return arguments[arguments.index(flag)+1]


def recorded(label):
    check()
    need(label not in CASES, "CONTROL_DUPLICATE_CASE")
    CASES.append(label)


def positive(kit, fixture, request, label):
    check()
    request_ref = fixture.ref(request)
    output = fixture.output()
    receipt = kit.prepare(Path(request_ref["path"]), output)
    need(receipt["mathematical_acceptance"] is False and receipt["commands_executed"] == 0 and
         receipt["protected_state_opened"] is False and receipt["profile_sha256"] == PROFILE,
         "CONTROL_RECEIPT_BOUNDARY")
    need(json.loads((output / "RECEIPT.json").read_bytes()) == receipt, "CONTROL_RECEIPT_FILE")
    need(set(p.name for p in output.iterdir()) == {*receipt["files"], "RECEIPT.json"},
         "CONTROL_OUTPUT_CENSUS")
    for filename, pin in receipt["files"].items():
        raw = (output / filename).read_bytes()
        need(pin == {"bytes": len(raw), "sha256": digest(raw)}, "CONTROL_OUTPUT_PIN")
    arguments = json.loads((output / "arguments.json").read_bytes())
    need(arguments["requires_launcher"] is True and arguments["mathematical_acceptance"] is False and
         arguments["profile_sha256"] == PROFILE and
         arguments["arguments"][0] == request["action"], "CONTROL_ARGUMENTS_BOUNDARY")
    args = arguments["arguments"]
    need(type(args) is list and all(type(part) is str for part in args), "CONTROL_STRUCTURED_ARGUMENTS")
    need(arguments["entry"] == ("owner" if request["action"] in
         ("init", "produce-baseline", "intake-baseline") else "peer"), "CONTROL_ENTRY")
    if "state" in request:
        for key in ("catalog", "custody", "store_id"):
            need(argv_value(args, "--"+key.replace("_", "-")) == request["state"][key],
                 "CONTROL_STATE_ARGUMENT")
        need(json.loads(Path(argv_value(args, "--custody-limits")).read_bytes()) == request["custody_limits"],
             "CONTROL_CUSTODY_LIMITS")
    else:
        need(not any(flag in args for flag in ("--catalog", "--custody", "--store-id", "--custody-limits")),
             "CONTROL_STATE_FREE")
    if "operation_output" in request:
        need(argv_value(args, "--output") == request["operation_output"] and
             not os.path.lexists(request["operation_output"]), "CONTROL_NO_OPERATION")
    config = None
    if arguments["entry"] == "peer":
        raw = Path(argv_value(args, "--config")).read_bytes()
        need(digest(raw) == argv_value(args, "--config-sha256"), "CONTROL_CONFIG_PIN")
        config = json.loads(raw)
    recorded(label)
    return arguments, config, output


def negative(kit, fixture, request, label, *, raw=None, output=None, code="KIT_"):
    check()
    request_ref = fixture.ref(request, raw=raw)
    output = fixture.output() if output is None else output
    existed = os.path.lexists(output)
    before = {p.name: p.read_bytes() for p in output.iterdir()} if existed and output.is_dir() else None
    try:
        kit.prepare(Path(request_ref["path"]), output)
    except ValueError as error:
        need(code in str(error), "CONTROL_WRONG_REFUSAL:"+label+":"+str(error))
    else:
        raise AssertionError("CONTROL_MISSING_REFUSAL:"+label)
    if existed:
        need(before == {p.name: p.read_bytes() for p in output.iterdir()}, "CONTROL_EXISTING_OUTPUT_CHANGED")
    else:
        need(not os.path.lexists(output), "CONTROL_EARLY_REFUSAL_WROTE_OUTPUT:"+label)
    recorded(label)


def good_handoffs(kit, f):
    for action in ("init", "find", "preview", "receive", "inspect", "authoring-offers",
                   "produce-baseline", "intake-baseline", "publish", "serve"):
        request = f.request(action)
        args, config, _ = positive(kit, f, request, "valid-"+action)
        tokens = args["arguments"]
        if action in ("preview", "receive"):
            need(config["selection"] == f.selection, "CONTROL_EXACT_SEARCH_SELECTION")
        if action == "receive":
            need(config["parent_root"] == f.parent and config["dependency_policy"] == "selected-unit-only",
                 "CONTROL_EXPLICIT_PARENT_POLICY")
        if action == "inspect":
            need(config["selection"] == {"provider": "synthetic-peer", "name": f.target2["name"],
                 "export_id": f.target2["export_id"]}, "CONTROL_EXACT_TYPE_BINDING")
        if action == "authoring-offers":
            need(config["selection"] == {"provider": "synthetic-peer", "export_id": f.target["export_id"]},
                 "CONTROL_OWN_EXPORT_OFFER")
        if action == "produce-baseline":
            project_raw = Path(argv_value(tokens, "--project-production")).read_bytes()
            need(digest(project_raw) == argv_value(tokens, "--project-production-sha256"), "CONTROL_PROJECT_PIN")
            need(json.loads(project_raw) == {"schema": "DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1",
                "project_search_paths": request["project_search_paths"], "modules": request["modules"]},
                "CONTROL_PROJECT_SHAPE")
            need(json.loads(Path(argv_value(tokens, "--output-names")).read_bytes()) == request["output_names"] and
                 tokens.count("--approve-local-project") == 1, "CONTROL_APPROVAL_NAMES")
        if action == "intake-baseline":
            need(argv_value(tokens, "--parent-root") == f.parent and
                 argv_value(tokens, "--bundle-manifest-sha256") == f.manifest_ref["sha256"] and
                 argv_value(tokens, "--bundle-directory") == str(f.bundle), "CONTROL_INTAKE_BINDING")
        if action == "publish":
            need(config["context_root"] == f.accepted and config["targets"] == [f.target2, f.target],
                 "CONTROL_EXACT_TARGET_ORDER_ROOT")
        if action == "serve":
            need(config["share_all_custody"] is True and config["exclusive"] is True and
                 config["lease_seconds"] == 10 and config["tls"] is None, "CONTROL_FINITE_DISCLOSURE")
    request = f.request("receive")
    request["parent_report"] = f.ref(f.intake)
    request["dependency_policy"] = "bounded-closure"
    _, config, _ = positive(kit, f, request, "completed-intake-parent")
    need(config["parent_root"] == f.accepted, "CONTROL_INTAKE_PARENT_ROOT")
    request = f.request("receive")
    reused = {**f.init, "operation": "receive", "result": {
        "status": "REUSED_LOCAL_ACCEPTANCE", "mathematical_acceptance": False,
        "local_acceptance_available": True, "admission": {
            "status": "REUSED", "local_root": f.accepted, "units_checked": 0}}}
    request["parent_report"] = f.ref(reused)
    _, config, _ = positive(kit, f, request, "reused-local-acceptance-parent")
    need(config["parent_root"] == f.accepted, "CONTROL_REUSED_PARENT")


def report_controls(kit, f):
    for field, value in (("ok", False), ("ok", 1), ("operation", "serve"),
                         ("profile_sha256", "0"*64), ("close_errors", ["failed"]),
                         ("final_budget_error", {"error": "exhausted"})):
        report = deepcopy(f.find); report[field] = value
        request = f.request("preview"); request["find_report"] = f.ref(report)
        negative(kit, f, request, "report-"+field+"-"+str(value)[:8])
    for field, value in (("status", "FAILED"), ("cleanup_errors", ["unclosed"]), ("matches", [])):
        report = deepcopy(f.find); report["result"][field] = value
        request = f.request("preview"); request["find_report"] = f.ref(report)
        negative(kit, f, request, "find-result-"+field)
    for key in f.state:
        report = deepcopy(f.init)
        report[key] = "f"*64 if key == "store_id" else str(f.project)
        request = f.request("receive"); request["parent_report"] = f.ref(report)
        negative(kit, f, request, "parent-state-"+key, code="KIT_REPORT_STATE_MISMATCH")
    for status in ("BASELINE_INTAKE_STOPPED", "PREPARED", "CHECKED"):
        report = deepcopy(f.intake); report["result"]["status"] = status
        request = f.request("publish"); request["intake_report"] = f.ref(report)
        negative(kit, f, request, "partial-intake-"+status)
    report = deepcopy(f.intake); report["result"]["local_root"] = f.parent
    request = f.request("publish"); request["intake_report"] = f.ref(report)
    negative(kit, f, request, "intake-final-root-mismatch")
    report = deepcopy(f.intake); report["result"]["batches"][0]["status"] = "FAILED"
    request = f.request("publish"); request["intake_report"] = f.ref(report)
    negative(kit, f, request, "intake-failed-batch")
    report = deepcopy(f.init); report["ok"] = False; report["accepted"] = report["result"]["basis"]
    request = f.request("receive"); request["parent_report"] = f.ref(report)
    negative(kit, f, request, "failure-accepted-diagnostic-not-parent")
    report = deepcopy(f.producer); report["result"]["status"] = "PREPARED_FOR_MANIFEST_WRITE_NOT_COMPLETION"
    request = f.request("intake-baseline"); request["producer_report"] = f.ref(report)
    negative(kit, f, request, "producer-intermediate-not-complete")


def identity_controls(kit, f):
    request = f.request("preview"); request["find_report"]["sha256"] = "0"*64
    negative(kit, f, request, "exact-report-pin", code="KIT_INPUT_PIN")
    for value in (-1, True, 1):
        request = f.request("preview"); request["match_index"] = value
        negative(kit, f, request, "match-index-"+str(value))
    for value in ([0, 0], [True], [2], []):
        request = f.request("publish"); request["target_indices"] = value
        negative(kit, f, request, "target-indices-"+str(value))
    for field in ("export_id", "unit_id", "name"):
        report = deepcopy(f.producer)
        report["result"]["targets"][0][field] = name("Different") if field == "name" else "0"*64
        request = f.request("publish"); request["producer_report"] = f.ref(report)
        negative(kit, f, request, "exact-target-"+field, code="KIT_PRODUCER_EXPORT_BINDING")
    report = deepcopy(f.intake); report["result"]["manifest_sha256"] = "0"*64
    request = f.request("publish"); request["intake_report"] = f.ref(report)
    negative(kit, f, request, "intake-producer-manifest-mismatch")
    report = deepcopy(f.producer); report["result"]["manifest"]["bytes"] += 1
    request = f.request("intake-baseline"); request["producer_report"] = f.ref(report)
    negative(kit, f, request, "actual-manifest-length-binding")
    report = deepcopy(f.producer)
    report["result"]["output_directory"] = "Z:\\unavailable-original-producer\\bundle"
    report["result"]["manifest_path"] = "Z:\\unavailable-original-producer\\bundle\\manifest.json"
    request = f.request("intake-baseline"); request["producer_report"] = f.ref(report)
    args, _, _ = positive(kit, f, request, "relocated-exact-bundle-original-path-unfollowed")
    need(argv_value(args["arguments"], "--bundle-directory") == str(f.bundle),
         "CONTROL_RECEIVER_LOCAL_BUNDLE")
    report = deepcopy(f.find); report["result"]["matches"][0]["provider"] = "unselected-peer"
    request = f.request("preview"); request["find_report"] = f.ref(report)
    negative(kit, f, request, "selected-provider-required")
    report = deepcopy(f.find); report["result"]["matches"][0]["record"]["object_id"] = "0"*64
    request = f.request("preview"); request["find_report"] = f.ref(report)
    negative(kit, f, request, "locator-export-binding", code="KIT_LOCATOR_EXPORT_BINDING")
    report = deepcopy(f.preview); report["result"]["preview"]["unit_id"] = "0"*64
    request = f.request("authoring-offers"); request["preview_report"] = f.ref(report)
    negative(kit, f, request, "preview-own-export-binding")
    request = f.request("inspect"); request["binding_index"] = 1
    negative(kit, f, request, "inspection-binding-index")
    request = f.request("produce-baseline")
    request["output_names"] = [name("Synthetic", "math α")]
    arguments, _, _ = positive(kit, f, request, "unicode-structured-name-not-dotted-string")
    need(json.loads(Path(argv_value(arguments["arguments"], "--output-names")).read_bytes()) == request["output_names"],
         "CONTROL_UNICODE_NAME_EXACT")


def input_controls(kit, f):
    for label, raw in (("duplicate-json", b'{"action":"find","action":"serve"}'),
                       ("nonfinite-json", b'{"action":"find","budget":NaN}'),
                       ("overflow-float-json", b'{"action":"find","budget":1e999}'),
                       ("too-deep-json", b'['*65+b'0'+b']'*65),
                       ("oversize-json", b' '*MIB+b'{}')):
        negative(kit, f, {}, label, raw=raw)
    request = f.request("find"); request["shell"] = "must-not-execute"
    negative(kit, f, request, "extra-request-field")
    request = f.request("find"); request["limits"]["requests"] = True
    negative(kit, f, request, "boolean-not-budget")
    request = f.request("find"); request["limits"]["requests"] = 513
    negative(kit, f, request, "finite-search-ceiling")
    request = f.request("receive"); del request["dependency_policy"]
    negative(kit, f, request, "explicit-policy-required")
    request = f.request("receive"); request["dependency_policy"] = "automatic"
    negative(kit, f, request, "no-automatic-dependency-policy")
    request = f.request("produce-baseline"); request["approve_local_project"] = False
    negative(kit, f, request, "project-approval-required")
    request = f.request("serve"); request["share_all_custody"] = False
    negative(kit, f, request, "whole-custody-disclosure-required")
    request = f.request("serve"); request["host"] = "192.0.2.10"
    negative(kit, f, request, "remote-serving-tls-required")
    request = f.request("find"); request["contacts"]["synthetic-peer"]["host"] = "192.0.2.10"
    negative(kit, f, request, "remote-contact-tls-required")
    request = f.request("find"); request["operation_output"] = "REPLACE_ME"
    negative(kit, f, request, "unresolved-placeholder")
    request = f.request("find"); request["operation_output"] = "relative-output"
    negative(kit, f, request, "absolute-operation-output-required")
    request = f.request("find"); request["operation_output"] = str(f.outputs / "absent-parent" / "child")
    negative(kit, f, request, "fresh-operation-existing-parent-required")
    request = f.request("receive"); request["state"]["catalog"] = str(f.root / "missing-catalog")
    negative(kit, f, request, "existing-receiver-state-required")
    output = f.output(); output.mkdir(); fresh(output / "preserved.txt", b"DO-NOT-OVERWRITE")
    negative(kit, f, f.request("find"), "no-output-overwrite", output=output)
    output = f.inputs / "inside-inputs"
    request = f.request("produce-baseline"); request["project_search_paths"] = [str(f.inputs)]
    negative(kit, f, request, "no-kit-output-inside-selected-project", output=output)
    request = f.request("find")
    negative(kit, f, request, "output-path-traversal", output=f.outputs / ".." / "traversal-output")


def filesystem_controls(kit, f):
    report_ref = f.ref(f.find)
    selected = Path(report_ref["path"])
    alias = f.inputs / "hardlinked-report.json"
    os.link(selected, alias)
    request = f.request("preview")
    request["find_report"] = {"path": str(alias), "sha256": report_ref["sha256"]}
    negative(kit, f, request, "hardlinked-report-refused", code="KIT_PATH_KIND")
    report_ref = f.ref(f.find)
    selected = Path(report_ref["path"])
    original_lstat = Path.lstat
    def redirected(path, *args, **kwargs):
        info = original_lstat(path, *args, **kwargs)
        if path == selected:
            return SimpleNamespace(st_mode=info.st_mode, st_nlink=info.st_nlink,
                                   st_file_attributes=0x400)
        return info
    request = f.request("preview"); request["find_report"] = report_ref
    with patch.object(Path, "lstat", redirected):
        negative(kit, f, request, "reparse-metadata-refused", code="KIT_REDIRECTED_PATH")
    request = f.request("find")
    request_ref, output = f.ref(request), f.output()
    original_open = Path.open
    def write_failure(path, mode="r", *args, **kwargs):
        if path == output / "arguments.json" and mode == "xb":
            raise OSError("SYNTHETIC_OUTPUT_WRITE_FAILURE")
        return original_open(path, mode, *args, **kwargs)
    with patch.object(Path, "open", write_failure):
        try:
            kit.prepare(Path(request_ref["path"]), output)
        except OSError as error:
            need(str(error) == "SYNTHETIC_OUTPUT_WRITE_FAILURE", "CONTROL_WRITE_FAILURE")
        else:
            raise AssertionError("CONTROL_WRITE_FAILURE_MISSING")
    need(output.is_dir() and (output / "config.json").is_file() and
         not (output / "arguments.json").exists() and not (output / "RECEIPT.json").exists(),
         "CONTROL_PARTIAL_OUTPUT_NOT_PRESERVED")
    recorded("failed-write-preserves-partial-output")


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTROL_PROCESS")
    source = args.source_root / "ordinary_operator_kit" / "prepare.py"
    ordinary_path(source)
    ordinary_path(args.output, fresh_directory=True)
    need(source.is_relative_to(ROOT) and args.output.is_relative_to(ROOT / "experiments") and
         not args.output.is_relative_to(args.source_root) and not args.source_root.is_relative_to(args.output),
         "CONTROL_SCOPED_PATHS")
    args.output.mkdir()
    # This entire kit invocation layer is forbidden from executing any product,
    # opening protected state or networking. No method below supplies fake math.
    with ExitStack() as stack:
        for owner, attribute in ((subprocess, "Popen"), (subprocess, "run"),
                (os, "system"), (os, "popen"), (socket, "socket"),
                (socket, "create_connection"), (sqlite3, "connect")):
            stack.enter_context(patch.object(owner, attribute, side_effect=AssertionError(
                "CONTROL_FORBIDDEN_EXECUTION_OR_STATE:"+attribute)))
        kit, pin = load(source)
        fixture = Fixture(args.output)
        good_handoffs(kit, fixture)
        report_controls(kit, fixture)
        identity_controls(kit, fixture)
        input_controls(kit, fixture)
        filesystem_controls(kit, fixture)
    check()
    need(len(CASES) == 74 and len(set(CASES)) == 74, "CONTROL_EXPECTED_CASE_CENSUS")
    report = {"schema": "DMKN_OPERATOR_KIT_NATIVE_FREE_CONTROLS_V1", "cases": CASES, "count": len(CASES),
        "source_pin": pin, "native_runs": 0, "commands_executed": 0, "network_calls": 0,
        "existing_protected_stores_opened": 0, "mathematical_acceptance": False,
        "fixture_kind": "SYNTHETIC_REPORTS_AND_EMPTY_DIRECTORIES_NOT_REAL_ACCEPTANCE",
        "disclosed_doubles": ["one reparse-metadata refusal", "one output-write failure"],
        "wall_seconds": time.monotonic()-START, "cpu_seconds": time.process_time()-CPU}
    fresh(args.output / "RESULT.json", canonical(report))
    print(canonical(report).decode("utf-8"))


if __name__ == "__main__":
    main()

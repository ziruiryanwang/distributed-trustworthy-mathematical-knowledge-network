"""Small offline controls for the new operator-kit boundary; no product imports.

The sparse find report is an unchanged actual public result. The directory
envelope is explicitly synthetic; it is not another executed directory search.
Socket, subprocess and database entrypoints are forbidden while the kit runs.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
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
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2


def need(ok, why):
    if not ok:
        raise AssertionError(why)


def check():
    need(time.monotonic()-START_WALL < 45 and time.process_time()-START_CPU < 25,
         "ORIGINAL_TEST_ALLOWANCE")


def raw(path):
    check()
    need(path.is_file() and 0 < path.stat().st_size <= 2*MIB, "READ_BOUND")
    with path.open("rb") as stream:
        value = stream.read(2*MIB+1)
    need(len(value) <= 2*MIB, "READ_GREW")
    return value


def save(path, value, *, diagnostic=False):
    if not diagnostic:
        check()
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(encoded) <= 2*MIB, "WRITE_BOUND")
    with path.open("xb") as stream:
        stream.write(encoded)


def controls(args, report):
    source = Path(__file__).resolve().parent / "prepare_selected.py"
    spec = importlib.util.spec_from_file_location("_network_test_wrapper", source)
    wrapper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wrapper)
    kit = wrapper.load_helper()
    output, cases = args.output, report["cases"]
    selected_raw = raw(args.find_report)
    need(hashlib.sha256(selected_raw).hexdigest() == args.find_sha256, "ACTUAL_FIND_PIN")
    selected_doc = kit.Inputs().json(selected_raw)
    need(selected_doc["profile_sha256"] == args.profile_sha256 and
         selected_doc["operation"] == "find" and selected_doc["ok"] is True and
         len(selected_doc["result"]["matches"]) == 1, "ACTUAL_FIND_SHAPE")
    profile_raw = raw(args.package/"PROFILE.json")
    need(hashlib.sha256(profile_raw).hexdigest() == args.profile_sha256 == kit.PROFILE,
         "SELECTED_PROFILE")
    match = selected_doc["result"]["matches"][0]
    provider = match["provider"]
    endpoint = dict(host="127.0.0.1", port=43123, tls=False,
                    server_name=None, ca_file=None, ca_sha256=None)
    explicit = {provider: endpoint}
    specs = [dict(tag="type-symbol", symbol=dict(kind="portable-symbol", symbol_id="1"*64)),
             dict(tag="type-symbol", symbol=dict(kind="portable-symbol", symbol_id="2"*64))]
    settings = dict(limits=dict(providers=2, snapshots=2, requests=4, pages=2,
        examined=16, candidates=8, bytes=MIB, wall_ms=10000, inflight=1),
        offer=dict(max_bytes=65536, max_expanded_bytes=MIB, max_age_ms=10000),
        page=dict(scanned=8, matches=4, bytes=65536, timeout_ms=1000,
            record_probes=64, node_reads=100000, hash_calls=2000000, sql_vm_steps=1000000))
    generated = []

    def prepare(label, request, *, selected=False):
        check()
        path, destination = output/(label+"-request.json"), output/(label+"-prepared")
        save(path, request)
        if selected:
            result = wrapper.prepare_selected(args.package, args.profile_sha256, path, destination)
            need(result["interface"] == "contact-sparse-v2" and result["known_noncompiled_roles"] == 45 and
                 result["native_artifacts_checked"] is False and result["mathematical_acceptance"] is False,
                 "SELECTED_INTERFACE_BOUNDARY")
            receipt = result["preparation"]
        else:
            receipt = kit.prepare(path, destination)
        need(receipt["profile_sha256"] == args.profile_sha256 and receipt["commands_executed"] == 0 and
             receipt["protected_state_opened"] is False and receipt["mathematical_acceptance"] is False,
             "PREPARATION_IS_INERT")
        config = kit.Inputs().json(raw(destination/"config.json"))
        arguments = kit.Inputs().json(raw(destination/"arguments.json"))
        need(arguments["entry"] == "peer" and arguments["arguments"][0] == request["action"] and
             arguments["requires_launcher"] is True, "PREPARED_PUBLIC_ACTION")
        for name, pin in receipt["files"].items():
            data = raw(destination/name)
            need(pin == dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest()), "PREPARED_FILE_PIN")
        need(not Path(request["operation_output"]).exists(), "NO_PRODUCT_OUTPUT")
        generated.append(dict(label=label, receipt=receipt))
        return config, path, destination

    def refuse(label, request, code):
        path, destination = output/(label+"-request.json"), output/(label+"-prepared")
        save(path, request)
        try:
            kit.prepare(path, destination)
        except ValueError as error:
            need(str(error) == code, label+":WRONG_REFUSAL:"+str(error))
        else:
            raise AssertionError(label+":ACCEPTED")
        need(not destination.exists(), label+":WROTE_BEFORE_REFUSAL")

    find = dict(action="find", operation_output=str(output/"later-find"), contacts=explicit,
                providers=[provider], specs=specs, **settings)
    config, _, _ = prepare("atomic-default", find, selected=True)
    need("candidate_mode" not in config and config == {k: v for k, v in find.items()
         if k not in ("action", "operation_output")}, "DEFAULT_UNCHANGED")
    sparse = deepcopy(find); sparse["candidate_mode"] = "sparse-v2"
    config, _, _ = prepare("sparse-opt-in", sparse)
    need(config["candidate_mode"] == "sparse-v2", "MODE_FORWARDING")
    for label, value in (("null-mode", None), ("boolean-mode", True), ("unknown-mode", "future")):
        bad = deepcopy(sparse); bad["candidate_mode"] = value
        refuse(label, bad, "KIT_CANDIDATE_MODE")
    cases.append("known-source-interface-default-and-explicit-sparse-mode")

    directory = dict(action="directory-find", operation_output=str(output/"later-directory"),
        contacts=explicit, directories=[provider], specs=specs, routes=[[specs[0]], specs],
        directory=dict(requests=2, reply_bytes=65536, max_contacts=4, max_bytes=32768,
                       max_age_ms=10000, attempt_timeout_ms=3000),
        egress=dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
                    test_endpoints=[dict(host="127.0.0.1", port=43123)]),
        search={**deepcopy(settings), "candidate_mode": "sparse-v2"})
    config, _, _ = prepare("directory-find", directory)
    need(config == {k: v for k, v in directory.items() if k not in ("action", "operation_output")},
         "DIRECTORY_FORWARDING")
    for label, alter, code in (
        ("duplicate-route", lambda d: d.update(routes=[specs, list(reversed(specs))]), "KIT_DIRECTORY_ROUTES"),
        ("route-outside-query", lambda d: d.update(routes=[[dict(tag="declaration-kind", value="theorem")]]), "KIT_DIRECTORY_ROUTES"),
        ("extra-search-field", lambda d: d["search"].update(retry=True), "KIT_FIELDS"),
        ("extra-egress-authority", lambda d: d["egress"].update(allow_all=True), "KIT_FIELDS"),
    ):
        bad = deepcopy(directory); alter(bad); refuse(label, bad, code)
    cases.append("directory-search-original-config-and-strict-route-egress-limits")

    service = dict(host="127.0.0.1", port=0, tls=None, lease_seconds=10, cleanup_seconds=10,
                   limits=dict(max_connections=2, max_requests=8, max_reply_bytes=MIB, operation_ms=1000))
    hint = {k: endpoint[k] for k in ("host", "port", "tls", "server_name")}
    serve_directory = dict(action="directory-serve", operation_output=str(output/"later-directory-service"),
        entries=[dict(specs=specs, endpoints=[hint])], **service)
    config, _, _ = prepare("directory-serve", serve_directory)
    need(config["entries"] == serve_directory["entries"] and config["lease_seconds"] == 10,
         "DIRECTORY_FINITE_SERVICE")
    for label, alter, code in (
        ("directory-hint-ca", lambda d: d["entries"][0]["endpoints"][0].update(ca_file="ignored"), "KIT_FIELDS"),
        ("duplicate-registration", lambda d: d["entries"].append(deepcopy(d["entries"][0])), "KIT_DIRECTORY_DUPLICATE_KEY"),
        ("boolean-lease", lambda d: d.update(lease_seconds=True), "KIT_INTEGER"),
    ):
        bad = deepcopy(serve_directory); alter(bad); refuse(label, bad, code)
    cases.append("directory-service-finite-no-hint-authority")

    # Empty test directories satisfy only path metadata. No store is created or
    # accepted mathematics invented, and sqlite3.connect is forbidden throughout.
    state = dict(catalog=str(output/"synthetic-empty-catalog"),
                 custody=str(output/"synthetic-empty-custody"), store_id="3"*64)
    for key in ("catalog", "custody"):
        Path(state[key]).mkdir()
    index_dir = output/"synthetic-empty-index"; index_dir.mkdir()
    access = dict(pairs=[["1"*64, "2"*64]], limits=dict(max_rows=10, max_logical_bytes=4096))
    idx = dict(path=str(index_dir), create=False, limits=dict(max_objects=10, max_postings=100,
        max_features=100, max_snapshots=11, max_logical_bytes=MIB, max_db_pages=256))
    serve = dict(action="serve", operation_output=str(output/"later-index-service"), state=state,
        custody_limits=dict(objects=10, exports=20, logical_bytes=MIB, db_pages=256),
        index={**idx, "access_pairs": access}, share_all_custody=True, exclusive=True, **service)
    config, _, _ = prepare("pair-enabled-serve", serve)
    need(config["index"]["access_pairs"] == access, "PAIR_CONFIG_FORWARDING")
    for label, value in (("pair-null", None), ("pair-omitted", "omitted")):
        selected = deepcopy(serve)
        if value == "omitted":
            del selected["index"]["access_pairs"]
        else:
            selected["index"]["access_pairs"] = value
        config, _, _ = prepare(label, selected)
        need(config["index"] == selected["index"], "PAIR_DEFAULT_FORWARDING")
    for label, alter, code in (
        ("boolean-pair-quota", lambda d: d["index"]["access_pairs"]["limits"].update(max_rows=True), "KIT_INTEGER"),
        ("reversed-pair", lambda d: d["index"]["access_pairs"]["pairs"][0].reverse(), "KIT_ACCESS_PAIR_ORDER"),
        ("extra-pair-field", lambda d: d["index"]["access_pairs"].update(backfill=True), "KIT_FIELDS"),
    ):
        bad = deepcopy(serve); alter(bad); refuse(label, bad, code)
    # Fresh-index preparation validator, not creation or backfill in a database.
    fresh = {**idx, "path": str(output/"later-fresh-index"), "create": True, "access_pairs": access}
    need(kit.index(fresh, []) == fresh and not Path(fresh["path"]).exists(), "FRESH_INDEX_INERT")
    cases.append("optional-static-pairs-and-fresh-reopen-paths-not-database-acceptance")

    preview = dict(action="preview", operation_output=str(output/"later-preview"), contacts=explicit,
        find_report=dict(path=str(args.find_report), sha256=args.find_sha256), match_index=0,
        limits=dict(requests=1, reply_bytes=MIB))
    config, actual_request, actual_output = prepare("actual-find-preview", preview)
    need(config["selection"] == match and config["contacts"] == explicit, "ACTUAL_REPORT_EXACT_SELECTION")
    cases.append("unchanged-actual-sparse-public-report-to-preview")

    synthetic = deepcopy(selected_doc)
    synthetic.update(operation="directory-find", test_fixture="SYNTHETIC_DIRECTORY_ENVELOPE_NOT_AN_EXECUTED_SEARCH")
    synthetic["result"].update(operation="directory-find", learned_contacts={provider: {
        **endpoint, "host": "192.0.2.123", "port": 443, "tls": True, "server_name": "unapproved.example"}})
    synthetic_path = output/"synthetic-directory-report.json"; save(synthetic_path, synthetic)
    synthetic_pin = hashlib.sha256(raw(synthetic_path)).hexdigest()
    from_directory = deepcopy(preview)
    from_directory["find_report"] = dict(path=str(synthetic_path), sha256=synthetic_pin)
    config, _, _ = prepare("synthetic-directory-preview", from_directory)
    need(config["selection"] == match and config["contacts"] == explicit and
         "learned_contacts" not in config, "EXPLICIT_CONTACTS_ONLY")
    bad = deepcopy(from_directory); bad["contacts"] = {"another-explicit-contact": endpoint}
    refuse("no-selected-contact", bad, "KIT_SELECTED_CONTACT")
    cases.append("synthetic-directory-report-requires-new-explicit-contact-no-hint-promotion")

    for label, alter, code in (
        ("failed-report", lambda d: d.update(ok=False), "KIT_SUCCESSFUL_SELECTED_REPORT_REQUIRED"),
        ("wrong-report-profile", lambda d: d.update(profile_sha256="0"*64), "KIT_SUCCESSFUL_SELECTED_REPORT_REQUIRED"),
        ("mismatched-operation", lambda d: d["result"].update(operation="find"), "KIT_FIND_STATUS_OR_OPERATION"),
        ("changed-locator", lambda d: d["result"]["matches"][0]["record"]["locator"].update(unit_id="0"*64), "KIT_LOCATOR_EXPORT_BINDING"),
    ):
        changed = deepcopy(synthetic); alter(changed)
        path = output/(label+"-report.json"); save(path, changed)
        bad = deepcopy(from_directory)
        bad["find_report"] = dict(path=str(path), sha256=hashlib.sha256(raw(path)).hexdigest())
        refuse(label, bad, code)
    bad = deepcopy(preview); bad["find_report"]["sha256"] = "0"*64
    refuse("wrong-report-pin", bad, "KIT_INPUT_PIN")
    cases.append("report-identity-failure-operation-and-locator-refusals-before-write")

    before = {p.name: hashlib.sha256(raw(p)).hexdigest() for p in actual_output.iterdir()}
    try:
        kit.prepare(actual_request, actual_output)
    except ValueError as error:
        need(str(error) == "KIT_OUTPUT_EXISTS", "OVERWRITE_REFUSAL")
    else:
        raise AssertionError("OVERWRITE_ALLOWED")
    need(before == {p.name: hashlib.sha256(raw(p)).hexdigest() for p in actual_output.iterdir()},
         "EXISTING_OUTPUT_UNCHANGED")
    wrong_output = output/"wrong-wrapper-profile"
    try:
        wrapper.prepare_selected(args.package, "0"*64, actual_request, wrong_output)
    except ValueError as error:
        need(str(error) == "KIT_SELECT_PROFILE_PIN", "WRAPPER_PROFILE_REFUSAL")
    else:
        raise AssertionError("WRONG_PROFILE_ALLOWED")
    need(not wrong_output.exists(), "WRAPPER_REFUSAL_BEFORE_WRITE")
    mapping = kit.Inputs().json(raw(source.parent/"compatibility.json"))
    original_profile = kit.Inputs().json(profile_raw)
    for label, alter in (
        ("unknown-code", lambda d: d["files"]["owner.py"].update(sha256="0"*64)),
        ("extra-role", lambda d: d["files"].update({"extra.py": dict(bytes=1, sha256="0"*64)})),
    ):
        changed = deepcopy(original_profile); alter(changed)
        try:
            wrapper.known_layout(kit, changed, mapping)
        except ValueError as error:
            need(str(error) == "KIT_SELECT_UNKNOWN_INTERFACE", label+":INTERFACE_REFUSAL")
        else:
            raise AssertionError(label+":UNKNOWN_INTERFACE_ALLOWED")
    cases.append("fresh-output-and-selected-package-identity")
    need(raw(args.find_report) == selected_raw and raw(args.package/"PROFILE.json") == profile_raw,
         "ACTUAL_INPUTS_UNCHANGED")
    need(all(not list(Path(state[key]).iterdir()) for key in ("catalog", "custody")) and
         not list(index_dir.iterdir()), "NO_DATABASE_OR_STATE_WRITES")
    need(len(cases) == 8, "GROUP_CENSUS")
    report.update(preparations=generated, actual_find_sha256=args.find_sha256,
        synthetic_directory_sha256=synthetic_pin, actual_inputs_unchanged=True,
        synthetic_directory_not_actual_execution=True, product_execution=False,
        protected_state_opened=False, mathematical_acceptance=False)


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("package", "find-report", "output"):
        parser.add_argument("--"+name, type=Path, required=True)
    for name in ("profile-sha256", "find-sha256"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode, "CANONICAL_ISOLATED_INVOCATION")
    need(args.output.is_absolute() and args.output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         not args.output.exists() and args.output.parent.is_dir() and
         args.output.parent.resolve(strict=True) == args.output.parent, "FRESH_OUTPUT")
    need(all(p.is_absolute() and not p.is_relative_to(args.output) and not args.output.is_relative_to(p)
             for p in (args.package, args.find_report, Path(__file__).resolve().parent)), "DISJOINT_INPUTS")
    args.output.mkdir()
    report = dict(passed=False, cases=[], profile_sha256=args.profile_sha256,
                  scope="OFFLINE_NETWORK_KIT_CONFIG_REPORT_BOUNDARY_NOT_PRODUCT_OR_MATHEMATICS")
    try:
        with ExitStack() as stack:
            for module, name in ((subprocess, "Popen"), (subprocess, "run"), (os, "system"),
                                 (socket, "socket"), (socket, "create_connection"), (sqlite3, "connect")):
                stack.enter_context(patch.object(module, name, side_effect=AssertionError("NO_PRODUCT_EXECUTION")))
            controls(args, report)
        report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:1000])
    report.update(wall_seconds=time.monotonic()-START_WALL, harness_cpu_seconds=time.process_time()-START_CPU)
    save(args.output/"RESULT.json", report, diagnostic=True)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

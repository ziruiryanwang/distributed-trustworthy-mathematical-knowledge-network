"""One file-only assembly and strict offline configuration integration.

No product/native import, network, real mathematical owner or checking. Parent
and find reports below are explicit synthetic metadata, NEVER accepted evidence.
The separately selected outer Job bounds this test and its one assembly.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from contextlib import ExitStack
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
from types import SimpleNamespace as NS
from unittest.mock import patch

START, CPU = time.monotonic(), time.process_time()
MIB = 1024**2
POLICY = dict(acquisition_sources=["B", "A"], attempt_timeout_ms=3000,
              finalization_reserve_ms=2000)
HELPER_SLOT = "_multi_source_assembly_files"


def need(ok, why):
    if not ok:
        raise AssertionError("MULTI_INTEGRATION_TEST_"+why)


def check():
    need(time.monotonic()-START < 110 and time.process_time()-CPU < 60, "ORIGINAL_ALLOWANCE")


def forbidden(*args, **kwargs):
    raise AssertionError("MULTI_INTEGRATION_TEST_UNSELECTED_EXECUTION")


def pin(path):
    check()
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return dict(bytes=path.stat().st_size, sha256=digest)


def read(path):
    check(); need(0 < path.stat().st_size <= 2*MIB, "SMALL_METADATA")
    return path.read_bytes()


def doc(path):
    return json.loads(read(path))


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
    need(len(raw) <= 2*MIB, "REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest())


def load(path, label):
    spec = importlib.util.spec_from_file_location(label, path)
    value = importlib.util.module_from_spec(spec)
    exec(compile(read(path), str(path), "exec"), value.__dict__)
    return value


def refuses(action, text):
    try:
        action()
    except ValueError as error:
        need(text in str(error), "WRONG_REFUSAL:"+str(error))
        return str(error)
    raise AssertionError("MULTI_INTEGRATION_TEST_MISSING_REFUSAL:"+text)


def assembly_call(assembler, args):
    # Independent entry-call isolation, not a relaxation of the product guard.
    # Only the approved file-only helper's test registration is removed.
    need(HELPER_SLOT not in sys.modules, "HELPER_NOT_ISOLATED")
    try:
        return assembler.assemble(args)
    finally:
        sys.modules.pop(HELPER_SLOT, None)


def fixture(kit, output, profile):
    state = dict(catalog=str(output/"empty-catalog-metadata-fixture"),
                 custody=str(output/"empty-custody-metadata-fixture"), store_id="1"*64)
    Path(state["catalog"]).mkdir(); Path(state["custody"]).mkdir()
    name, semantic, unit = [[0, {"$bytes": [84]}]], "2"*64, "3"*64
    identity = kit.export_identity(semantic, unit, name)
    selected = dict(provider="origin", snapshot_id="4"*64, record=dict(
        schema="DMKN_FORMAL_FEATURE_RECORD_V3", kind="ordinary-lean-export-v2",
        namespace="5"*64, object_id=identity, object_sha256="6"*64,
        object_bytes=576, features=["7"*64], locator=dict(
            schema="DMKN_ORDINARY_LEAN_EXPORT_LOCATOR_V2", semantic_id=semantic,
            unit_id=unit, export_name=name)))
    parent = dict(ok=True, operation="init", profile_sha256=profile, **state,
        result=dict(status="INITIALIZED_LOCAL_OWNER", basis=dict(status="CHECKED", local_root="8"*64)))
    found = dict(ok=True, operation="find", profile_sha256=profile,
        result=dict(status="INCOMPLETE_SEARCH", operation="find", matches=[selected]))
    parent_ref = save(output/"synthetic-parent.json", parent)
    found_ref = save(output/"synthetic-find.json", found)
    contacts = {name: dict(host="127.0.0.1", port=42000+i, tls=False,
                          server_name=None, ca_file=None, ca_sha256=None)
                for i, name in enumerate(("origin", "A", "B"))}
    request = dict(action="receive", state=state, custody_limits=dict(objects=32,
        exports=64, logical_bytes=MIB, db_pages=256), operation_output=str(output/"unexecuted-operation"),
        contacts=contacts, find_report=found_ref, match_index=0, parent_report=parent_ref,
        dependency_policy="bounded-closure", limits=dict(requests=32, reply_bytes=MIB,
        units=4, unit_bytes=4096, total_bytes=16384, missing=4, preflights=4, locator_bytes=1024))
    save(output/"METADATA-NOT-MATHEMATICS.json", dict(authority="EXPLICIT_SYNTHETIC_METADATA_ONLY",
        owner_databases_created=False, reports_are_actual=False, mathematical_acceptance=False))
    return request, selected, parent, found


def run(args, here, output):
    root = here.parents[2]
    assembler = load(here/"assemble.py", "_selected_multi_assembler")
    selector = load(here/"prepare_selected.py", "_selected_multi_preparer")
    kit = selector.load_helper()
    base, receipt_path = Path(args.base_package), Path(args.base_receipt)
    old, old_receipt = doc(base/"PROFILE.json"), doc(receipt_path)
    selection = doc(here/"OVERLAY.json")
    call = NS(source_root=str(root), base_package=str(base), base_profile_sha256=args.base_profile_sha256,
        base_receipt=str(receipt_path), base_receipt_sha256=args.base_receipt_sha256,
        overlay=str(here/"OVERLAY.json"), overlay_sha256=pin(here/"OVERLAY.json")["sha256"],
        output=str(output/"assembled"), wall_seconds=60, cpu_seconds=30)
    result = assembly_call(assembler, call)
    package = Path(result["package"])
    new = doc(package/"PROFILE.json")
    need(result["status"] == "ASSEMBLED_NOT_ADOPTED" and result["unchanged_payloads"] == 150
         and result["files_excluding_profile"] == 153 and result["auxiliary_files"] == 117,
         "ASSEMBLY_CENSUS")
    changed = sorted(name for name in old["files"] if old["files"][name] != new["files"].get(name))
    need(changed == sorted(selection["files"]) and set(old["files"]) == set(new["files"]), "EXACT_THREE_ROLES")
    need({key: value for key, value in old.items() if key != "files"} ==
         {key: value for key, value in new.items() if key != "files"}, "NONROLE_PROFILE_UNCHANGED")
    before = {p.relative_to(base).as_posix(): pin(p) for p in base.rglob("*") if p.is_file()}
    after = {p.relative_to(package).as_posix(): pin(p) for p in package.rglob("*") if p.is_file()}
    need(len(before) == len(after) == 154 and set(before) == set(after), "FULL_CENSUS")
    need(sorted(key for key in before if before[key] != after[key]) == sorted(changed+["PROFILE.json"]),
         "ONLY_THREE_AND_PROFILE_CHANGED")
    need(read(base/"installation/INSTALLATION.json") == read(package/"installation/INSTALLATION.json")
         and pin(package/"PROFILE.json")["sha256"] == result["profile_sha256"], "EXACT_INSTALLATION_PROFILE")
    for target, filename in assembler.PAYLOADS.items():
        need(after[target] == selection["files"][target] == pin(root/assembler.PREFIX/filename), "TESTED_BYTES_INSTALLED")
    save(output/"MAP.json", dict(changed=changed, old_profile=args.base_profile_sha256,
        new_profile=result["profile_sha256"], installation_manifest_sha256=new["installation_manifest_sha256"],
        files=after, native_and_anchor_support_unchanged=True, actual_state_opened=False))
    groups = ["actual_file_only_assembly_exact_three_payloads"]

    refusals = []
    for field, code in (("base_profile_sha256", "JSON_PIN"), ("base_receipt_sha256", "JSON_PIN"),
                        ("overlay_sha256", "JSON_PIN")):
        negative = NS(**vars(call)); setattr(negative, field, "0"*64)
        negative.output = str(output/("refuse-"+field))
        refusals.append(refuses(lambda n=negative: assembly_call(assembler, n), code))
        need(not Path(negative.output).exists(), "REFUSAL_BEFORE_OUTPUT")
    refusals.append(refuses(lambda: assembly_call(assembler, call), "OUTPUT_EXISTS"))
    # Test fixed base role/receipt validation without copying the package again.
    helper = assembler.helper(root)
    try:
        compatibility = doc(root/assembler.BASE_MAP)
        installation = doc(base/"installation/INSTALLATION.json")
        altered = deepcopy(old); altered["files"]["peer_api.py"]["sha256"] = "0"*64
        refusals.append(refuses(lambda: assembler.base_map(helper, altered, old_receipt, installation,
                                                         compatibility, args.base_profile_sha256), "BASE_SOURCE_INTERFACE"))
        altered_receipt = deepcopy(old_receipt); altered_receipt["assembler"]["sha256"] = "0"*64
        refusals.append(refuses(lambda: assembler.base_map(helper, old, altered_receipt, installation,
                                                         compatibility, args.base_profile_sha256), "BASE_RECEIPT"))
    finally:
        sys.modules.pop(HELPER_SLOT, None)
    groups.append("assembly_pins_interface_receipt_and_output_refusals")

    request, selected, parent, found = fixture(kit, output, result["profile_sha256"])
    def prepare(label, value):
        path = output/(label+"-request.json"); save(path, value)
        leaf = output/(label+"-prepared")
        prepared = selector.prepare_selected(package, result["profile_sha256"], path, leaf)
        need(prepared["interface"] == "multi-source-investigator-v1" and not prepared["mathematical_acceptance"]
             and not prepared["native_artifacts_checked"] and prepared["preparation"]["commands_executed"] == 0,
             "INERT_PREPARATION_SCOPE")
        receipt = doc(leaf/"RECEIPT.json")
        for name, expected in receipt["files"].items():
            need(pin(leaf/name) == expected, "PREPARED_PIN")
        args_doc = doc(leaf/"arguments.json")
        position = args_doc["arguments"].index("--config-sha256")
        need(args_doc["arguments"][position+1] == pin(leaf/"config.json")["sha256"], "CONFIG_HASH_ARGUMENT")
        return leaf, doc(leaf/"config.json")
    default_leaf, default_cfg = prepare("default", request)
    expected = dict(contacts=request["contacts"], selection=selected, limits=request["limits"],
                    parent_root="8"*64, dependency_policy="bounded-closure")
    need(default_cfg == expected and not set(POLICY)&set(default_cfg), "DEFAULT_CONFIGURATION_UNCHANGED")
    legacy = load(root/"software/v5/ordinary_network_kit/prepare.py", "_old_offline_preparer")
    legacy.PROFILE = result["profile_sha256"]  # Same explicit private configuration as the selector.
    legacy_leaf = output/"legacy-default-prepared"
    legacy.prepare(output/"default-request.json", legacy_leaf)
    need(read(default_leaf/"config.json") == read(legacy_leaf/"config.json"), "OLD_DEFAULT_EXACT_BYTES")
    old_args = doc(legacy_leaf/"arguments.json"); new_args = doc(default_leaf/"arguments.json")
    old_args["arguments"] = [item.replace(str(legacy_leaf), str(default_leaf)) for item in old_args["arguments"]]
    need(old_args == new_args, "OLD_DEFAULT_ARGUMENTS")
    _, extended = prepare("multi", dict(request, **POLICY))
    need(extended == dict(expected, **POLICY), "OPTIONAL_ORDER_AND_FIELDS_FORWARDED")
    groups.append("strict_selected_preparer_default_and_optional_policy")

    invalid = [dict(request, acquisition_sources=["A"]),
        dict(request, attempt_timeout_ms=3000), dict(request, finalization_reserve_ms=2000),
        dict(request, acquisition_sources=["A"], attempt_timeout_ms=3000),
        dict(request, acquisition_sources=["A"], finalization_reserve_ms=2000),
        dict(request, attempt_timeout_ms=3000, finalization_reserve_ms=2000),
        dict(request, **{**POLICY, "acquisition_sources": []}),
        dict(request, **{**POLICY, "acquisition_sources": ["A", "A"]}),
        dict(request, **{**POLICY, "acquisition_sources": ["unknown"]}),
        dict(request, **{**POLICY, "acquisition_sources": ["A"]*9}),
        dict(request, **{**POLICY, "acquisition_sources": [True]}),
        dict(request, **{**POLICY, "attempt_timeout_ms": True}),
        dict(request, **{**POLICY, "attempt_timeout_ms": 0}),
        dict(request, **{**POLICY, "finalization_reserve_ms": 60001}),
        dict(request, **{**POLICY, "finalization_reserve_ms": 1.5}),
        dict(request, **POLICY, unknown_field=True)]
    for i, value in enumerate(invalid):
        label = "bad-policy-"+str(i)
        refusals.append(refuses(lambda label=label, value=value: prepare(label, value), "KIT_"))
        need(not (output/(label+"-prepared")).exists(), "POLICY_FAILURE_NO_OUTPUT")
    preview = {key: request[key] for key in ("contacts", "find_report", "match_index", "operation_output")}
    preview.update(action="preview", limits=dict(requests=1, reply_bytes=1024), **POLICY)
    refusals.append(refuses(lambda: prepare("preview-policy", preview), "KIT_FIELDS"))
    need(not (output/"preview-policy-prepared").exists(), "POLICY_RECEIVE_ONLY")
    for role, original in (("parent", parent), ("find", found)):
        historical = deepcopy(original); historical["profile_sha256"] = args.base_profile_sha256
        ref = save(output/("old-"+role+"-report.json"), historical)
        value = dict(request); value["parent_report" if role == "parent" else "find_report"] = ref
        refusals.append(refuses(lambda role=role, value=value: prepare("old-"+role, value),
            "PARENT_SUCCESS" if role == "parent" else "SUCCESSFUL_SELECTED_REPORT_REQUIRED"))
        need(not (output/("old-"+role+"-prepared")).exists(), "HISTORICAL_REPORT_NOT_RELABELED")
    groups.append("invalid_policies_and_historical_profile_reports_refused")

    refusals.append(refuses(lambda: selector.prepare_selected(base, args.base_profile_sha256,
        output/"default-request.json", output/"old-interface-prepared"), "SELECT_UNKNOWN_INTERFACE"))
    refusals.append(refuses(lambda: selector.prepare_selected(package, "0"*64,
        output/"default-request.json", output/"bad-profile-prepared"), "SELECT_PROFILE_PIN"))
    refusals.append(refuses(lambda: selector.prepare_selected(package, result["profile_sha256"],
        output/"default-request.json", default_leaf), "OUTPUT_EXISTS"))
    need(list(Path(request["state"]["catalog"]).iterdir()) == [] and
         list(Path(request["state"]["custody"]).iterdir()) == [] and
         not Path(request["operation_output"]).exists(), "NO_OWNER_OR_OPERATION_EXECUTED")
    need(before == {p.relative_to(base).as_posix(): pin(p) for p in base.rglob("*") if p.is_file()},
         "BASE_PRESERVED")
    need(after == {p.relative_to(package).as_posix(): pin(p) for p in package.rglob("*") if p.is_file()},
         "ASSEMBLED_PACKAGE_PRESERVED")
    groups.append("profile_interface_output_refusals_and_final_immutable_maps")
    save(output/"REFUSALS.json", refusals)
    return dict(status="PASS", groups=groups, group_count=len(groups), assembly=result,
        refused_cases=len(refusals), mathematical_acceptance=False, native_operations=0,
        real_state_opened=False, metadata_authority="EXPLICIT_SYNTHETIC_NOT_MATHEMATICS",
        wall_seconds=time.monotonic()-START, test_cpu_seconds=time.process_time()-CPU)


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for field in ("base-package", "base-profile-sha256", "base-receipt", "base-receipt-sha256", "output"):
        parser.add_argument("--"+field, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_WINDOWS")
    here, output = Path(__file__).absolute().parent, Path(args.output)
    need(output.is_absolute() and not output.exists() and output.parent.is_dir(), "FRESH_OUTPUT")
    output.mkdir()
    try:
        with ExitStack() as guards:
            for name in ("subprocess.Popen", "os.system", "socket.socket", "socket.create_connection"):
                guards.enter_context(patch(name, forbidden))
            result = run(args, here, output)
        check(); save(output/"TEST-RESULT.json", result)
        print(json.dumps(result), flush=True)
    except BaseException as error:
        save(output/"FAILURE.json", dict(status="FAILED", error_type=type(error).__name__, error=str(error),
            mathematical_acceptance=False, wall_seconds=time.monotonic()-START,
            test_cpu_seconds=time.process_time()-CPU))
        raise


if __name__ == "__main__":
    main()

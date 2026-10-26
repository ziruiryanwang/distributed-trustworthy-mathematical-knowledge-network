"""One exact network source pack, relocation and two inert public entrypoints.

No compiler/product/database/socket operation and no old archive campaign.
The previous manifest is read only to prove unchanged source input identity.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_network_bundle/"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START_WALL < 60 and time.process_time()-START_CPU < 30,
         "ORIGINAL_ENVELOPE")


def read(path, maximum=2*MIB):
    check()
    size = path.stat().st_size
    need(0 < size <= maximum, "READ_BOUND")
    with path.open("rb") as stream:
        value = stream.read(maximum+1)
    need(len(value) == size, "READ_CHANGED")
    return value


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def save(path, value):
    data = canonical(value)
    need(len(data) <= 2*MIB, "SAVE_BOUND")
    with path.open("xb") as stream:
        stream.write(data)


def pin(data):
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def public(args, label, tokens, report):
    check()
    need(60-(time.monotonic()-START_WALL) >= 20, "NO_ROOM_FOR_CHILD")
    argv = [sys.executable, "-I", "-S", "-B", *map(str, tokens)]
    save(args.output/(label+"-COMMAND.json"), dict(argv=argv, cwd=str(ROOT), timeout_seconds=15))
    with (args.output/(label+"-stdout.txt")).open("xb") as out, \
            (args.output/(label+"-stderr.txt")).open("xb") as err:
        result = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=out,
                                stderr=err, timeout=15, creationflags=subprocess.CREATE_NO_WINDOW)
    need(result.returncode == 0 and (args.output/(label+"-stderr.txt")).stat().st_size == 0,
         label+":PUBLIC_FAILED")
    data = json.loads(read(args.output/(label+"-stdout.txt"), MIB))
    report.setdefault("public", {})[label] = dict(result=data, exit_code=result.returncode, reaped=True)
    return data


def controls(args, report):
    spec = importlib.util.spec_from_file_location("_network_bundle_controls", Path(__file__).with_name("bundle.py"))
    bundle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bundle)
    old_raw = read(args.old_manifest)
    need(pin(old_raw)["sha256"] == args.old_manifest_sha256, "OLD_MANIFEST_PIN")
    old = json.loads(old_raw)
    need(old["schema"] == "DMKN_ORDINARY_SOURCE_DISTRIBUTION_V1" and len(old["files"]) == 105,
         "OLD_BASELINE")
    old_inputs = {n: p for n, p in old["files"].items() if not n.startswith("software/v5/ordinary_source_bundle/")}
    need(len(old_inputs) == 102, "UNCHANGED_SOURCE_COUNT")
    packed = bundle.pack(args.source_root, args.output/"packed", check=check)
    need(packed["payload_files"] == 136 and packed["archive_files"] == 137 and
         packed["status"] == "PACKED_SOURCE_NOT_BUILT", "NEW_PACK_CENSUS")
    archive = args.output/"packed"/"source.zip"
    need(pin(read(archive, 16*MIB)) == packed["archive"], "ACTUAL_ARCHIVE_PIN")
    with zipfile.ZipFile(archive, "r") as zip_file:
        doc_raw = zip_file.read("SOURCE-MANIFEST.json")
        doc = json.loads(doc_raw)
        need(pin(doc_raw) == packed["manifest"] and len(doc["files"]) == 136,
             "ACTUAL_MANIFEST")
        need(all(doc["files"].get(name) == value for name, value in old_inputs.items()), "OLD102_UNCHANGED")
        expected = set(old_inputs)
        overlay_counts = {}
        for folder, count in (("ordinary_contact_federation", 10), ("ordinary_sparse_access", 12)):
            base = "software/v5/"+folder+"/"
            mapping = json.loads(read(args.source_root/(base+"OVERLAY.json")))
            # Overlay's map is inspected as inert data, never imported/executed.
            sources = {base+name.rsplit("/", 1)[-1] for name in mapping["files"]}
            need(len(sources) == count, "OVERLAY_PAYLOAD_CENSUS")
            need(all(doc["files"].get(base+name.rsplit("/", 1)[-1]) == selected_pin
                     for name, selected_pin in mapping["files"].items()), "EXACT_OVERLAY_SOURCE_PINS")
            additions = sources | {base+"assemble.py", base+"OVERLAY.json"}
            need(not expected & additions, "DISJOINT_OVERLAY_INPUTS")
            expected.update(additions); overlay_counts[folder] = len(additions)
        expected.update("software/v5/ordinary_network_kit/"+name for name in
            ("prepare.py", "prepare_selected.py", "compatibility.json", "START-HERE.md", "examples.json"))
        expected.update(PREFIX+name for name in ("bundle.py", "README.md", "LICENSE-STATUS.md"))
        need(set(doc["files"]) == expected and len(expected) == 136, "INDEPENDENT_DELTA_CLOSURE")
        entries = dict(build="software/v5/ordinary_bounded_operations/build.py",
            fair_overlay="software/v5/ordinary_fair_search/assemble.py",
            contact_overlay="software/v5/ordinary_contact_federation/assemble.py",
            sparse_overlay="software/v5/ordinary_sparse_access/assemble.py",
            operator="software/v5/ordinary_network_kit/prepare_selected.py",
            operator_guide="software/v5/ordinary_network_kit/START-HERE.md")
        need(doc["entrypoints"] == entries and set(entries.values()) <= expected and
             doc["license_status"] == "UNDECIDED_NO_PUBLIC_RELEASE_AUTHORIZATION", "ENTRYPOINTS_AND_LICENSE")
        need(zip_file.namelist() == sorted(expected | {"SOURCE-MANIFEST.json"}), "EXACT_ARCHIVE_NAMES")
        destination = args.output/"relocated-source"; destination.mkdir()
        for name in sorted(expected | {"SOURCE-MANIFEST.json"}):
            bundle.relative(name)
            target = destination/name
            need(target.is_relative_to(destination), "EXTRACTION_PATH")
            data = zip_file.read(name)
            need(pin(data) == (packed["manifest"] if name == "SOURCE-MANIFEST.json" else doc["files"][name]),
                 "EXTRACTED_BYTES")
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(data)
    report.update(pack=packed, unchanged_source_inputs=102, overlay_inputs=overlay_counts)
    report["cases"].append("exact136-payload-delta-old102-unchanged-and-new-entrypoints")
    verified = public(args, "relocated-verify", [destination/(PREFIX+"bundle.py"), "verify",
        "--source-root", destination, "--manifest-sha256", packed["manifest"]["sha256"]], report)
    need(verified["status"] == "VERIFIED_EXACT_SOURCE_NOT_BUILT" and verified["payload_files"] == 136 and
         verified["manifest"] == packed["manifest"], "RELOCATED_PUBLIC_VERIFIER")
    report["cases"].append("relocated-public-exact-source-verifier")

    find_raw = read(args.find_report)
    need(pin(find_raw)["sha256"] == args.find_sha256, "FIND_PIN")
    find = json.loads(find_raw)
    match = find["result"]["matches"][0]
    request = dict(action="preview", operation_output=str(args.output/"later-preview"),
        contacts={match["provider"]: dict(host="127.0.0.1", port=43123, tls=False,
                                         server_name=None, ca_file=None, ca_sha256=None)},
        find_report=dict(path=str(args.find_report), sha256=args.find_sha256), match_index=0,
        limits=dict(requests=1, reply_bytes=MIB))
    request_path = args.output/"preview-request.json"; save(request_path, request)
    prepared = args.output/"prepared-preview"
    chosen = public(args, "relocated-operator", [destination/entries["operator"],
        "--package", args.package, "--profile-sha256", args.profile_sha256,
        "--request", request_path, "--output", prepared], report)
    need(chosen["interface"] == "contact-sparse-v2" and chosen["known_noncompiled_roles"] == 45 and
         chosen["native_artifacts_checked"] is False and chosen["mathematical_acceptance"] is False,
         "RELOCATED_OPERATOR_BOUNDARY")
    receipt = json.loads(read(prepared/"RECEIPT.json"))
    need(receipt == chosen["preparation"] and receipt["commands_executed"] == 0 and
         receipt["protected_state_opened"] is False, "INERT_PREPARATION")
    config = json.loads(read(prepared/"config.json"))
    need(config == dict(contacts=request["contacts"], selection=match, limits=request["limits"]) and
         not (args.output/"later-preview").exists(), "EXACT_INERT_PREVIEW")
    for name, expected_pin in receipt["files"].items():
        need(pin(read(prepared/name)) == expected_pin, "PREPARATION_FILE_PIN")
    report["cases"].append("relocated-public-network-kit-actual-find-to-inert-preview")

    mutations = [("old-manifest", old, "SOURCE_BUNDLE_MANIFEST_PROFILE")]
    wrong_entry = deepcopy(doc); wrong_entry["entrypoints"]["operator"] = old["entrypoints"]["operator"]
    mutations.append(("old-operator-entry", wrong_entry, "SOURCE_BUNDLE_MANIFEST_PROFILE"))
    missing = deepcopy(doc); del missing["files"]["software/v5/ordinary_sparse_access/pair_access.py"]
    mutations.append(("missing-sparse-input", missing, "SOURCE_BUNDLE_MANIFEST_CENSUS"))
    for label, changed, code in mutations:
        try:
            bundle.validate_manifest(changed)
        except ValueError as error:
            need(str(error) == code, label+":WRONG_REFUSAL")
        else:
            raise AssertionError(label+":ACCEPTED")
    report["cases"].append("old-format-old-entrypoint-missing-new-input-refuse")
    bundle.census(destination, expected | {"SOURCE-MANIFEST.json"}, check)
    for name, expected_pin in doc["files"].items():
        need(pin(read(destination/name)) == expected_pin and pin(read(args.source_root/name)) == expected_pin,
             "SOURCE_OR_EXTRACTION_CHANGED")
    need(read(args.old_manifest) == old_raw and read(args.find_report) == find_raw,
         "OLD_MANIFEST_OR_PUBLIC_REPORT_CHANGED")
    report["cases"].append("all136-source-and-relocated-payloads-unchanged-no-extra-files")
    need(len(report["cases"]) == 5, "FIVE_GROUP_CENSUS")


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("source-root", "old-manifest", "package", "find-report", "output"):
        parser.add_argument("--"+name, type=Path, required=True)
    for name in ("old-manifest-sha256", "profile-sha256", "find-sha256"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and args.source_root == ROOT, "CANONICAL_INVOCATION")
    need(args.output.is_absolute() and args.output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         not args.output.exists() and args.output.parent.resolve(strict=True) == args.output.parent,
         "FRESH_TEST_OUTPUT")
    args.output.mkdir()
    report = dict(passed=False, cases=[], scope="SOURCE_DELIVERY_AND_INERT_PREPARATION_NOT_NATIVE_OR_GROWTH")
    try:
        controls(args, report)
        report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:1000])
    report.update(wall_seconds=time.monotonic()-START_WALL, harness_cpu_seconds=time.process_time()-START_CPU)
    save(args.output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

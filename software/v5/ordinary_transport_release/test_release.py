"""Changed source-build boundary, one file-only assembly, and relocated handoff.

No native build/import, owner state, socket, mathematical event or old test rerun.
Synthetic identity controls are parsed metadata only, never executable outputs.
"""
from __future__ import annotations

import time
START, CPU = time.monotonic(), time.process_time()
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
RELEASE = "software/v5/ordinary_transport_release/"
BUNDLE = "software/v5/ordinary_release_bundle/"
REPAIR = "software/v5/ordinary_bounded_transport/"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 60 and time.process_time()-CPU < 30,
         "ORIGINAL_RELEASE_ALLOWANCE")


def read(path, maximum=2*MIB):
    check()
    size = path.stat().st_size
    need(0 < size <= maximum, "READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size, "READ_CHANGED")
    return raw


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def pin(raw):
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def save(path, value):
    raw = canonical(value)
    need(len(raw) <= 2*MIB, "SAVE_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def load(name, path):
    # Only reviewed source utilities are loaded; no product/native module.
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(read(path), str(path), "exec"), module.__dict__)
    return module


def public(args, label, tokens, report):
    check()
    need(60-(time.monotonic()-START) > 20, "NO_ROOM_FOR_PUBLIC_CHILD")
    argv = [sys.executable, "-I", "-S", "-B", *map(str, tokens)]
    save(args.output/(label+"-COMMAND.json"), dict(argv=argv, cwd=str(ROOT), timeout_seconds=20))
    with (args.output/(label+"-stdout.txt")).open("xb") as out, \
            (args.output/(label+"-stderr.txt")).open("xb") as err:
        result = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=out,
                                stderr=err, timeout=20, creationflags=subprocess.CREATE_NO_WINDOW)
    need(result.returncode == 0 and (args.output/(label+"-stderr.txt")).stat().st_size == 0,
         label+":PUBLIC_FAILED")
    value = json.loads(read(args.output/(label+"-stdout.txt")))
    report.setdefault("public", {})[label] = dict(result=value, exit_code=result.returncode, reaped=True)
    return value


def compatibility_controls(args, report):
    A = load("_release_assembly_controls", args.source_root/(RELEASE+"assemble.py"))
    H = A.helper(args.source_root)
    profile_raw, receipt_raw = read(args.base_package/"PROFILE.json"), read(args.base_receipt)
    need(pin(profile_raw)["sha256"] == args.base_profile_sha256 and
         pin(receipt_raw)["sha256"] == args.base_receipt_sha256, "BASE_SELECTION")
    profile, receipt = json.loads(profile_raw), json.loads(receipt_raw)
    installed_raw = read(args.base_package/"installation/INSTALLATION.json")
    need(pin(installed_raw)["sha256"] == profile["installation_manifest_sha256"], "BASE_INSTALLATION_PIN")
    installed = json.loads(installed_raw)
    compatibility = json.loads(read(args.source_root/"software/v5/ordinary_network_kit/compatibility.json"))
    source_map = json.loads(read(args.source_root/"software/v5/ordinary_bounded_operations/source-map.json"))

    def validate(p=profile, r=receipt, i=installed, c=compatibility, m=source_map):
        return A.validate_base_interface(H, p, r, i, c, m, profile_sha256=r["profile_sha256"])

    base = validate()
    need(set(base) == {"auxiliary", "installation_files", "documents", "implementation_id"}
         and len(base["auxiliary"]) == 117 and len(base["installation_files"]) == 27
         and len(base["documents"]) == 6, "BASE_INTERFACE_RESULT")
    report["cases"].append("exact-sparse-interface-accepted")

    # New native identity is synthetic metadata, not a compiler or safety claim.
    changed = deepcopy(profile)
    role = "authoring/bin/BaselineExporter.exe"
    changed["files"][role] = dict(bytes=123, sha256="1"*64)
    new_installation = deepcopy(installed)
    receiver_role = "lean-lib/OrdinaryWorkflowWorker.olean"
    new_installation["files"][receiver_role] = dict(bytes=456, sha256="8"*64)
    for field, names in new_installation["support_groups"].items():
        support = dict(field=field, files={name: new_installation["files"][name] for name in names})
        if field == "controller_support":
            support.update(roles=new_installation["roles"], compiled_dirs=new_installation["compiled_dirs"])
        new_installation["implementation"][field] = hashlib.sha256(
            b"DMKN-ORDINARY-INSTALLED-SUPPORT-V1\0"+canonical(support)).hexdigest()
    changed["installation_manifest_sha256"] = pin(canonical(new_installation))["sha256"]
    changed_receipt = deepcopy(receipt)
    changed_receipt["profile_sha256"] = pin(canonical(changed))["sha256"]
    changed_receipt["installation_manifest_sha256"] = changed["installation_manifest_sha256"]
    changed_receipt["package"] = "C:\\synthetic-metadata-only\\independent-build"
    changed_receipt["wall_seconds"] = 0.125
    value = validate(changed, changed_receipt, new_installation)
    need(value["auxiliary"][role] == changed["files"][role] and
         value["installation_files"][receiver_role] == new_installation["files"][receiver_role] and
         value["implementation_id"] != base["implementation_id"] and
         changed["installation_manifest_sha256"] != profile["installation_manifest_sha256"] and
         changed_receipt["profile_sha256"] != args.base_profile_sha256 and
         pin(canonical(changed_receipt))["sha256"] != args.base_receipt_sha256,
         "GENERATED_IDENTITY_NOT_HISTORICAL_CONSTANT")
    report["synthetic_native_identity"] = dict(roles=[role, receiver_role], executed=False,
        mathematical_acceptance=False, claim="PARSED_INTERFACE_COMPATIBILITY_ONLY")
    report["cases"].append("different-generated-identity-and-receipt-metadata-accepted-as-data")

    negatives = []
    p = deepcopy(profile); p["files"]["owner.py"]["sha256"] = "2"*64
    negatives.append(("changed-auxiliary-source", p, receipt, installed, compatibility, source_map))
    p = deepcopy(profile); del p["files"][role]
    negatives.append(("missing-native-role", p, receipt, installed, compatibility, source_map))
    p = deepcopy(profile); p["files"][role]["bytes"] = True
    negatives.append(("boolean-native-size", p, receipt, installed, compatibility, source_map))
    r = deepcopy(receipt); r["installation_manifest_sha256"] = "3"*64
    negatives.append(("receipt-installation-mismatch", profile, r, installed, compatibility, source_map))
    r = deepcopy(receipt); r["assembler"]["sha256"] = "4"*64
    negatives.append(("wrong-predecessor-source", profile, r, installed, compatibility, source_map))
    r = deepcopy(receipt); r["files_excluding_profile"] = 150
    negatives.append(("wrong-receipt-census", profile, r, installed, compatibility, source_map))
    i = deepcopy(installed); i["files"]["py/ordinary_admission.py"]["sha256"] = "5"*64
    negatives.append(("changed-checker-source", profile, receipt, i, compatibility, source_map))
    i = deepcopy(installed); i["files"]["python_runtime/python.exe"]["sha256"] = "6"*64
    negatives.append(("changed-supported-runtime", profile, receipt, i, compatibility, source_map))
    i = deepcopy(installed); i["implementation"]["kernel_support"] = "7"*64
    negatives.append(("incorrect-native-support-commitment", profile, receipt, i, compatibility, source_map))
    i = deepcopy(installed); i["compiled_dirs"] = []
    negatives.append(("incorrect-compiled-layout", profile, receipt, i, compatibility, source_map))
    expected_codes = {
        "changed-auxiliary-source": "TRANSPORT_STABLE_AUXILIARY_PIN",
        "missing-native-role": "TRANSPORT_BASE_LAYOUT", "boolean-native-size": "PIN_SHAPE",
        "receipt-installation-mismatch": "TRANSPORT_BASE_RECEIPT",
        "wrong-predecessor-source": "TRANSPORT_BASE_RECEIPT", "wrong-receipt-census": "TRANSPORT_BASE_RECEIPT",
        "changed-checker-source": "TRANSPORT_INSTALLATION_SOURCE_PIN",
        "changed-supported-runtime": "TRANSPORT_RUNTIME_PIN",
        "incorrect-native-support-commitment": "TRANSPORT_IMPLEMENTATION_SUPPORT",
        "incorrect-compiled-layout": "TRANSPORT_INSTALLATION_BINDINGS",
    }
    for label, p, r, i, c, m in negatives:
        try:
            validate(p, r, i, c, m)
        except ValueError as error:
            need(str(error) == "FAIR_ASSEMBLY_"+expected_codes[label], label+":UNEXPECTED_ERROR")
            report.setdefault("refusals", {})[label] = str(error)
        else:
            raise AssertionError(label+":ACCEPTED")
    need(len(report["refusals"]) == 10, "REFUSAL_CENSUS")
    report["cases"].append("ten-source-role-runtime-and-receipt-refusals")
    return profile, receipt, installed


def handoff(args, report, base):
    profile, receipt, installed = base
    B = load("_release_bundle_controls", args.source_root/(BUNDLE+"bundle.py"))
    old_raw = read(args.old_manifest)
    need(pin(old_raw)["sha256"] == args.old_manifest_sha256, "PREDECESSOR_MANIFEST_PIN")
    old = json.loads(old_raw)
    old_inputs = {name: value for name, value in old["files"].items()
                  if not name.startswith("software/v5/ordinary_network_bundle/")}
    need(len(old_inputs) == 133, "UNCHANGED133_CENSUS")
    expected = set(old_inputs)
    additions = {RELEASE+name for name in ("assemble.py", "README.md", "OVERLAY.json")}
    additions |= {REPAIR+name for name in
                  ("http_provider.py", "EXECUTION-TRUST.md", "prepare_selected.py", "compatibility.json")}
    expected |= additions | {BUNDLE+name for name in ("bundle.py", "README.md", "LICENSE-STATUS.md")}
    need(len(additions) == 7 and len(expected) == 143, "NEW143_CENSUS")
    packed = B.pack(args.source_root, args.output/"packed", check=check)
    need(packed["payload_files"] == 143 and packed["archive_files"] == 144, "PACK_CENSUS")
    archive = args.output/"packed/source.zip"
    need(pin(read(archive, 16*MIB)) == packed["archive"], "ARCHIVE_PIN")
    destination = args.output/"relocated-source"; destination.mkdir()
    with zipfile.ZipFile(archive, "r") as z:
        manifest_raw = z.read("SOURCE-MANIFEST.json")
        manifest = json.loads(manifest_raw)
        need(pin(manifest_raw) == packed["manifest"] and set(manifest["files"]) == expected and
             all(manifest["files"].get(n) == p for n, p in old_inputs.items()), "EXACT_SOURCE_CLOSURE")
        entries = manifest["entrypoints"]
        need(entries["transport_overlay"] == RELEASE+"assemble.py" and
             entries["operator"] == REPAIR+"prepare_selected.py" and
             set(entries.values()) <= expected and
             manifest["license_status"] == "UNDECIDED_NO_PUBLIC_RELEASE_AUTHORIZATION", "NEW_ENTRYPOINTS")
        need(z.namelist() == sorted(expected | {"SOURCE-MANIFEST.json"}), "ZIP_NAMES")
        for name in z.namelist():
            B.relative(name)
            target = destination/name
            need(target.is_relative_to(destination), "EXTRACTION_PATH")
            raw = z.read(name)
            need(pin(raw) == (packed["manifest"] if name == "SOURCE-MANIFEST.json" else
                             manifest["files"][name]), "EXTRACTION_PIN")
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(raw)
    report.update(pack=packed, unchanged_source_inputs=133, source_additions=sorted(additions))
    report["cases"].append("exact143-source-pack-relocation-and-repaired-entrypoints")
    verified = public(args, "relocated-verify", [destination/(BUNDLE+"bundle.py"), "verify",
        "--source-root", destination, "--manifest-sha256", packed["manifest"]["sha256"]], report)
    need(verified["payload_files"] == 143 and verified["manifest"] == packed["manifest"], "VERIFIER_RESULT")

    overlay = destination/(RELEASE+"OVERLAY.json")
    assembled = public(args, "relocated-assembly", [destination/entries["transport_overlay"],
        "--source-root", destination, "--base-package", args.base_package,
        "--base-profile-sha256", args.base_profile_sha256, "--base-receipt", args.base_receipt,
        "--base-receipt-sha256", args.base_receipt_sha256,
        "--overlay", overlay, "--overlay-sha256", pin(read(overlay))["sha256"],
        "--output", args.output/"assembled", "--wall-seconds", "20", "--cpu-seconds", "15"], report)
    need(assembled["status"] == "ASSEMBLED_NOT_ADOPTED" and
         assembled["profile_sha256"] == "b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7" and
         assembled["installation_manifest_sha256"] == profile["installation_manifest_sha256"],
         "UNCHANGED_ACTUAL_RUNTIME_PROFILE")
    package = args.output/"assembled/package"
    expected_package = dict(profile["files"])
    expected_package.update({"installation/"+n: p for n, p in installed["files"].items()
                             if not n.startswith(("python_runtime/", "lean_runtime/"))})
    expected_package["installation/INSTALLATION.json"] = pin(read(args.base_package/"installation/INSTALLATION.json"))
    expected_package.update(receipt["documentation_files"])
    expected_package.update(json.loads(read(overlay))["files"])
    expected_package["PROFILE.json"] = pin(read(package/"PROFILE.json"))
    need(len(expected_package) == 154 and
         pin(read(package/"PROFILE.json"))["sha256"] == assembled["profile_sha256"], "OUTPUT_MAP_CENSUS")
    B.census(package, set(expected_package), check)
    for name, selected in expected_package.items():
        need(pin(read(package/name, 128*MIB)) == selected, "ASSEMBLED_FILE:"+name)
    report["cases"].append("relocated-assembler-exact154-output-unchanged-runtime-profile")

    request = dict(action="directory-serve", entries=[dict(
        specs=[dict(tag="declaration-kind", value="theorem")],
        endpoints=[dict(host="127.0.0.1", port=38191, tls=False, server_name=None)])],
        host="127.0.0.1", port=0, tls=None, lease_seconds=2, cleanup_seconds=10,
        limits=dict(max_connections=1, max_requests=4, max_reply_bytes=MIB, operation_ms=60000),
        operation_output=str(args.output/"never-launched-service"))
    request_path = args.output/"request.json"; save(request_path, request)
    prepared = public(args, "relocated-operator", [destination/entries["operator"],
        "--package", package, "--profile-sha256", assembled["profile_sha256"],
        "--request", request_path, "--output", args.output/"prepared"], report)
    need(prepared["interface"] == "bounded-transport-v1" and
         prepared["native_artifacts_checked"] is False and
         prepared["preparation"]["commands_executed"] == 0 and
         prepared["preparation"]["protected_state_opened"] is False and
         not (args.output/"never-launched-service").exists(), "INERT_SELECTOR_ONLY")
    report["cases"].append("relocated-exact-compatible-selector-prepares-without-execution")
    B.census(destination, expected | {"SOURCE-MANIFEST.json"}, check)
    for name, selected in manifest["files"].items():
        need(pin(read(destination/name)) == selected and pin(read(args.source_root/name)) == selected,
             "FINAL_SOURCE_PIN:"+name)
    need(read(args.old_manifest) == old_raw, "OLD_MANIFEST_CHANGED")
    report["cases"].append("all-source-and-extraction-bytes-preserved")


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("source-root", "base-package", "base-receipt", "old-manifest", "output"):
        parser.add_argument("--"+name, type=Path, required=True)
    for name in ("base-profile-sha256", "base-receipt-sha256", "old-manifest-sha256"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and args.source_root == ROOT and
         sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "CANONICAL_ISOLATED_INVOCATION")
    need(args.output.is_absolute() and args.output.is_relative_to(ROOT/"experiments/v5-local-checks")
         and not args.output.exists() and args.output.parent.resolve(strict=True) == args.output.parent,
         "FRESH_OUTPUT")
    args.output.mkdir()
    report = dict(passed=False, cases=[], mathematical_acceptance=False,
                  scope="SOURCE_COMPATIBILITY_FILE_ASSEMBLY_AND_INERT_HANDOFF_NOT_NEW_NATIVE_BUILD")
    try:
        base = compatibility_controls(args, report)
        handoff(args, report, base)
        need(len(report["cases"]) == 7, "SEVEN_GROUP_CENSUS")
        report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:1000])
    report.update(wall_seconds=time.monotonic()-START, harness_cpu_seconds=time.process_time()-CPU)
    save(args.output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

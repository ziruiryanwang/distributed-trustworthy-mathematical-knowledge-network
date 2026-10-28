"""Assemble historical name-directory roles into the exact adopted local kit package.

Only the selected package subtree, its pinned kit manifest/pack receipt, and the
six fresh Python roles are inputs. No historical overlay pipeline, product code,
native compiler, owner database, service, or mathematical worker is executed.
Immutable operator-controlled input/output storage is a premise. Partial output
is retained on failure; this file-only operation is not product adoption.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import time

HELPER = "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
PREFIX = "software/v5/ordinary_name_directory/"
MAP_SHA = "46709b30199384ad1e14f0d54529fe185d429d83c341dfebb117869bbe22ead3"
BASE_MAP = "source/software/v5/ordinary_reply_capacity/source-map.json"
BASE_MAP_SHA = "05d96f671ecb755b20bcb55d0a93a33a8e70abdaa559017c750635deaba1eef5"
KIT_MANIFEST_SHA = "0b027eedfc768a3dbde08c1b389b19fd316e17cf1cbe6c5b421e5cc735b86ec8"
KIT_RECEIPT_SHA = "7443cec2b4159c7c2a66c110cf88c3b1656ce8c9e858e983d646dd7091d9457d"
BASE_PROFILE_SHA = "c8c8b5971e43361b7b09847b35b0e44c2645b284e59c59b90ab993136ccdb146"
INSTALLATION_SHA = "9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27"
REPLACED = ("advisory_context.py", "profile.py", "query.py", "run.py")
ADDED = ("directory_index.py", "lookup_directory.py")
ROLES = REPLACED + ADDED


def need(condition, code):
    if not condition:
        raise ValueError("DIRECTORY_ASSEMBLY_" + code)


def mapping_delta(old, current, H):
    """Allow exactly the six Python role selections and their count changes."""
    need(old.get("schema") == "DMKN_ORDINARY_CURRENT_SOURCE_MAP_V1" and
         type(old.get("sources")) is dict and len(old["sources"]) == 91 and
         type(old.get("copies")) is dict and len(old["copies"]) == 76,
         "BASE_SOURCE_MAP")
    expected = json.loads(H.canonical(old))
    for role in REPLACED:
        del expected["sources"][expected["copies"].pop(role)]
    for role in ROLES:
        source = PREFIX + role
        pin = current.get("sources", {}).get(source)
        H.pin_shape(pin)
        need(pin["bytes"] <= 2 * H.MIB, "SOURCE_SIZE")
        expected["copies"][role] = source
        expected["sources"][source] = pin
    expected["counts"].update(source_inputs=93, direct_copies=78,
        auxiliary_direct=50, payloads_excluding_profile=159, auxiliary_payloads=122)
    need(current == expected and len(current["sources"]) == 93 and
         len(current["copies"]) == 78, "EXACT_SOURCE_MAP_DELTA")


def assemble(args):
    started, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON")
    source_root = Path(args.source_root)
    helper_path = source_root / HELPER
    need(source_root.is_absolute() and helper_path.is_file() and
         helper_path.stat().st_size <= 2 * 1024**2, "HELPER_PATH")
    with helper_path.open("rb") as stream:
        helper_raw = stream.read(2 * 1024**2 + 1)
    need(hashlib.sha256(helper_raw).hexdigest() == HELPER_SHA, "HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_name_directory_assembly_helpers", helper_path)
    H = importlib.util.module_from_spec(spec)
    # This module defines helpers only; its historical assembly main is not run.
    exec(compile(helper_raw, str(helper_path), "exec", dont_inherit=True), H.__dict__)

    def check():
        need(time.monotonic() - started < 60 and time.process_time() - cpu < 30,
             "ALLOWANCE")

    source_root = H.ordinary(source_root, directory=True)
    kit = H.ordinary(Path(args.base_kit), directory=True)
    base = H.ordinary(kit / "package", directory=True)
    receipt_path = H.ordinary(Path(args.kit_receipt))
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    for selected in (kit, receipt_path, source_root / PREFIX, helper_path):
        need(not output.is_relative_to(selected) and not selected.is_relative_to(output),
             "OUTPUT_OVERLAP")
    need(not source_root.is_relative_to(output), "OUTPUT_CONTAINS_SOURCE")
    own_path = H.ordinary(Path(__file__).absolute())
    own_pin = H.pin(own_path, check, 2 * H.MIB)
    need(H.pin(helper_path, check, 2 * H.MIB)["sha256"] == HELPER_SHA, "HELPER_CHANGED")

    manifest, manifest_pin = H.read_json(kit / "KIT-MANIFEST.json", KIT_MANIFEST_SHA, check)
    receipt, receipt_pin = H.read_json(receipt_path, KIT_RECEIPT_SHA, check)
    verification = receipt.get("verification")
    need(manifest.get("schema") == "DMKN_ORDINARY_USABLE_LOCAL_KIT_V1" and
         manifest.get("profile_sha256") == BASE_PROFILE_SHA and
         manifest.get("installation_sha256") == INSTALLATION_SHA and
         type(manifest.get("files")) is dict and len(manifest["files"]) == 260,
         "KIT_MANIFEST")
    need(receipt.get("status") == "PACKED_AND_RELOCATED_LOCAL_KIT" and
         receipt.get("manifest") == manifest_pin and type(verification) is dict and
         verification.get("status") == "VERIFIED_LOCAL_KIT_BYTES" and
         verification.get("manifest") == manifest_pin and
         verification.get("profile_sha256") == BASE_PROFILE_SHA and
         verification.get("payload_files") == 260, "KIT_RECEIPT_BINDING")
    for name, pin in manifest["files"].items():
        H.relative(name); H.pin_shape(pin)
    baseline = {name[len("package/"):]: pin for name, pin in manifest["files"].items()
                if name.startswith("package/")}
    need(len(baseline) == 158 and sum(pin["bytes"] for pin in baseline.values()) <= 256 * H.MIB,
         "BASE_PACKAGE_BOUND")
    H.census(base, baseline, check)
    for name, pin in baseline.items():
        need(H.pin(base / H.relative(name), check) == pin, "BASE_PACKAGE_BYTES")

    profile, profile_pin = H.read_json(base / "PROFILE.json", BASE_PROFILE_SHA, check)
    installed, installed_pin = H.read_json(base / "installation/INSTALLATION.json", INSTALLATION_SHA, check)
    old_map, old_map_pin = H.read_json(kit / BASE_MAP, BASE_MAP_SHA, check)
    mapping, map_pin = H.read_json(source_root / PREFIX / "source-map.json", MAP_SHA, check)
    need(manifest["files"].get(BASE_MAP) == old_map_pin, "BASE_SOURCE_MAP_BINDING")
    mapping_delta(old_map, mapping, H)
    need(set(profile) == {"schema", "installation_manifest_sha256", "helper_paths",
                          "author_worker", "files"} and
         profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
         profile["installation_manifest_sha256"] == INSTALLATION_SHA and
         profile["helper_paths"] == ["authoring/helpers"] and
         profile["author_worker"] == "author_worker.py" and
         type(profile["files"]) is dict and len(profile["files"]) == 120 and
         baseline.get("PROFILE.json") == profile_pin and
         baseline.get("installation/INSTALLATION.json") == installed_pin and
         all(baseline.get(name) == pin for name, pin in profile["files"].items()),
         "BASE_PROFILE_BINDING")
    need(installed.get("schema") == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1" and
         type(installed.get("implementation")) is dict and
         type(installed.get("files")) is dict, "BASE_INSTALLATION")
    local_installed = {"installation/" + name: pin for name, pin in installed["files"].items()
                       if "installation/" + name in baseline}
    need(len(local_installed) == 27 and
         all(baseline[name] == pin for name, pin in local_installed.items()) and
         set(baseline) == set(profile["files"]) | set(local_installed) |
             set(old_map["documentation"]) | {"PROFILE.json", "installation/INSTALLATION.json"} and
         all(baseline.get(name) == old_map["sources"][source]
             for name, source in old_map["copies"].items()), "BASE_ROLE_CLOSURE")
    implementation_id = H.digest(b"DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1\0" +
                                  H.canonical(installed["implementation"]))

    selected = {name: base / name for name in baseline if name != "PROFILE.json"}
    expected = dict(baseline)
    for role in ROLES:
        source = source_root / PREFIX / role
        pin = mapping["sources"][PREFIX + role]
        need(H.pin(source, check, 2 * H.MIB) == pin and pin != baseline.get(role), "FRESH_SOURCE_PIN")
        selected[role], expected[role] = source, pin
    new_profile = H.canonical(dict(profile, files=dict(profile["files"],
        **{role: expected[role] for role in ROLES})))
    expected["PROFILE.json"] = {"bytes": len(new_profile), "sha256": H.digest(new_profile)}
    changed = sorted(name for name in baseline if expected[name] != baseline[name])
    added = sorted(set(expected) - set(baseline))
    need(changed == sorted((*REPLACED, "PROFILE.json")) and added == sorted(ADDED) and
         len(expected) == 160 and len(profile["files"]) + len(ADDED) == 122 and
         len(baseline) - len(changed) == 153 and
         sum(pin["bytes"] for pin in expected.values()) <= 256 * H.MIB, "EXACT_PACKAGE_DELTA")

    output.mkdir(); package = output / "package"; package.mkdir()
    for name, origin in sorted(selected.items()):
        check(); target = package / H.relative(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        H.ordinary(target.parent, directory=True)
        with H.ordinary(origin).open("rb") as incoming, H.ordinary(target, fresh=True).open("xb") as outgoing:
            shutil.copyfileobj(incoming, outgoing, H.MIB)
            outgoing.flush(); os.fsync(outgoing.fileno())
        need(H.pin(target, check) == expected[name], "COPY_READBACK")
    H.census(package, selected, check)
    H.census(base, baseline, check)
    for name, pin in baseline.items():
        need(H.pin(base / name, check) == pin, "BASE_CHANGED")
    for name, origin in selected.items():
        need(H.pin(origin, check) == expected[name] and H.pin(package / name, check) == expected[name],
             "SOURCE_OR_OUTPUT_CHANGED")
    for path, pin in ((kit / "KIT-MANIFEST.json", manifest_pin), (receipt_path, receipt_pin),
                      (kit / BASE_MAP, old_map_pin),
                      (source_root / PREFIX / "source-map.json", map_pin), (own_path, own_pin)):
        need(H.pin(path, check, 2 * H.MIB) == pin, "SELECTED_INPUT_CHANGED")
    need(H.pin(helper_path, check, 2 * H.MIB)["sha256"] == HELPER_SHA, "HELPER_CHANGED")
    # Commit the package profile only after every selected payload is present.
    check(); H.fresh_bytes(package / "PROFILE.json", new_profile)
    H.census(package, expected, check)
    need(H.pin(package / "PROFILE.json", check) == expected["PROFILE.json"], "PROFILE_READBACK")
    report = {"status": "ASSEMBLED_NOT_ADOPTED", "package": str(package), "files": expected,
        "base_kit_manifest": manifest_pin, "base_kit_receipt": receipt_pin,
        "base_profile_sha256": BASE_PROFILE_SHA,
        "profile_sha256": expected["PROFILE.json"]["sha256"],
        "installation_manifest_sha256": INSTALLATION_SHA, "implementation_id": implementation_id,
        "changed_files": changed, "added_files": added, "unchanged_files": 153,
        "files_excluding_profile": 159, "auxiliary_files": 122,
        "source_map": map_pin, "base_source_map": old_map_pin, "assembler": own_pin,
        "native_calls": 0, "owner_opened": False,
        "input_scope": "EXACT_158_FILE_PACKAGE_SUBTREE_AND_PINNED_KIT_METADATA_NOT_WHOLE_KIT_REVERIFICATION",
        "wall_seconds": time.monotonic() - started, "cpu_seconds": time.process_time() - cpu,
        "allowance": "COOPERATIVE_60_WALL_30_CPU_SECONDS",
        "claim": "FILE_ASSEMBLY_NOT_RUNTIME_OR_MATHEMATICAL_ACCEPTANCE"}
    check(); H.fresh_bytes(output / "ASSEMBLY.json", H.canonical(report)); check()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for option in ("source-root", "base-kit", "kit-receipt", "output"):
        parser.add_argument("--" + option, required=True)
    report = assemble(parser.parse_args())
    print(json.dumps(report, sort_keys=True, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    main()

"""File-only incremental-host package delta; no product/native code execution.

Inputs are the adopted owned-connect kit, its external receipt, and an exact selected
five-source delta. Original bytes and partial failed output remain preserved.
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
PREFIX = "software/v5/ordinary_incremental_host/"
BASE_MAP = "source/software/v5/ordinary_connect_ownership/source-map.json"
BASE_MAP_SHA = "80d46cbedad723a90a87db80c4b5ac1dd6054526911c643c425ede48ce00f713"
KIT_MANIFEST_SHA = "f67dcfac7d27f319f899665b50d044deb7d6035622209e71c5761efe73006e0d"
KIT_RECEIPT_SHA = "06daf9ee12308bf6fb47904ca81c183b60d21c9cbac35107bac5953333ed6e5f"
BASE_PROFILE_SHA = "d8eb8e4bfa4845ad44673ee037c739973dc5d03f89ed38ee80979c47888fa3cb"
INSTALLATION_SHA = "9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27"
ROLES = {name: PREFIX+name for name in
         ("host.py", "custodian.py", "run.py", "HOSTING.md", "LAUNCHER.md")}


def need(ok, code):
    if not ok:
        raise ValueError("INCREMENTAL_HOST_ASSEMBLY_"+code)


def assemble(args):
    started, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON")
    source_root = Path(args.source_root)
    helper_path = source_root/HELPER
    need(source_root.is_absolute() and helper_path.is_file() and
         0 < helper_path.stat().st_size <= 2*1024**2, "HELPER_PATH")
    with helper_path.open("rb") as stream:
        helper_raw = stream.read(2*1024**2+1)
    need(hashlib.sha256(helper_raw).hexdigest() == HELPER_SHA, "HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_incremental_host_assembly_files", helper_path)
    H = importlib.util.module_from_spec(spec)
    exec(compile(helper_raw, str(helper_path), "exec", dont_inherit=True), H.__dict__)

    def check():
        need(time.monotonic()-started < 60 and time.process_time()-cpu < 30, "ALLOWANCE")
    source_root = H.ordinary(source_root, directory=True)
    kit = H.ordinary(Path(args.base_kit), directory=True)
    base = H.ordinary(kit/"package", directory=True)
    receipt_path = H.ordinary(Path(args.kit_receipt))
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    for path in (kit, receipt_path, source_root/PREFIX, helper_path):
        need(not output.is_relative_to(path) and not path.is_relative_to(output), "OUTPUT_OVERLAP")
    need(not source_root.is_relative_to(output), "OUTPUT_CONTAINS_SOURCE")
    own_path = H.ordinary(Path(__file__).absolute())
    own_pin = H.pin(own_path, check, 2*H.MIB)
    manifest, manifest_pin = H.read_json(kit/"KIT-MANIFEST.json", KIT_MANIFEST_SHA, check)
    receipt, receipt_pin = H.read_json(receipt_path, KIT_RECEIPT_SHA, check)
    need(manifest["schema"] == "DMKN_ORDINARY_USABLE_LOCAL_KIT_V1" and
         manifest["profile_sha256"] == BASE_PROFILE_SHA and
         manifest["installation_sha256"] == INSTALLATION_SHA and len(manifest["files"]) == 266,
         "KIT_IDENTITY")
    need(receipt["status"] == "PACKED_AND_RELOCATED_LOCAL_KIT" and
         receipt["manifest"] == manifest_pin and
         receipt["verification"]["status"] == "VERIFIED_LOCAL_KIT_BYTES" and
         receipt["verification"]["manifest"] == manifest_pin and
         receipt["verification"]["profile_sha256"] == BASE_PROFILE_SHA and
         receipt["verification"]["payload_files"] == 266, "KIT_RECEIPT")
    baseline = {name.removeprefix("package/"): pin for name, pin in manifest["files"].items()
                if name.startswith("package/")}
    need(len(baseline) == 160 and sum(pin["bytes"] for pin in baseline.values()) <= 256*H.MIB,
         "BASE_PACKAGE_BOUND")
    H.census(base, baseline, check)
    for name, pin in baseline.items():
        need(H.pin(base/H.relative(name), check) == pin, "BASE_PACKAGE_BYTES")
    profile, profile_pin = H.read_json(base/"PROFILE.json", BASE_PROFILE_SHA, check)
    installed, installed_pin = H.read_json(base/"installation/INSTALLATION.json", INSTALLATION_SHA, check)
    old_map, old_map_pin = H.read_json(kit/BASE_MAP, BASE_MAP_SHA, check)
    mapping_path = source_root/PREFIX/"source-map.json"
    mapping, map_pin = H.read_json(mapping_path, args.source_map_sha256, check)
    need(manifest["files"][BASE_MAP] == old_map_pin and
         profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
         profile["installation_manifest_sha256"] == INSTALLATION_SHA and
         len(profile["files"]) == 122 and baseline["PROFILE.json"] == profile_pin and
         baseline["installation/INSTALLATION.json"] == installed_pin and
         all(baseline.get(name) == pin for name, pin in profile["files"].items()), "BASE_BINDING")
    need(old_map["schema"] == "DMKN_ORDINARY_CURRENT_SOURCE_MAP_V1" and
         len(old_map["sources"]) == 93 and len(old_map["copies"]) == 78 and
         all(baseline[name] == old_map["sources"][source]
             for name, source in old_map["copies"].items()), "BASE_MAP_BINDING")
    expected_map = json.loads(H.canonical(old_map))
    for role, source in ROLES.items():
        old_source = expected_map["copies"].pop(role)
        del expected_map["sources"][old_source]
        pin = mapping["sources"].get(source)
        H.pin_shape(pin)
        need(pin["bytes"] <= 2*H.MIB, "SOURCE_BOUND")
        expected_map["copies"][role] = source
        expected_map["sources"][source] = pin
        if role in expected_map["documentation"]:
            expected_map["documentation"][role] = source
    need(mapping == expected_map, "EXACT_MAP_DELTA")
    selected = {name: base/name for name in baseline if name != "PROFILE.json"}
    expected = dict(baseline)
    for role, relative in ROLES.items():
        pin, path = mapping["sources"][relative], source_root/relative
        need(H.pin(path, check, 2*H.MIB) == pin and pin != baseline[role], "FRESH_SOURCE_PIN")
        selected[role], expected[role] = path, pin
    new_profile = H.canonical(dict(profile, files=dict(profile["files"],
        **{role: expected[role] for role in ROLES if role in profile["files"]})))
    expected["PROFILE.json"] = {"bytes": len(new_profile), "sha256": H.digest(new_profile)}
    changed = sorted(name for name in baseline if expected[name] != baseline[name])
    need(changed == sorted((*ROLES, "PROFILE.json")) and len(expected) == 160 and
         len(baseline)-len(changed) == 154, "EXACT_PACKAGE_DELTA")
    output.mkdir(); package = output/"package"; package.mkdir()
    for name, source in sorted(selected.items()):
        check(); target = package/H.relative(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        H.ordinary(target.parent, directory=True)
        with H.ordinary(source).open("rb") as incoming, H.ordinary(target, fresh=True).open("xb") as outgoing:
            shutil.copyfileobj(incoming, outgoing, H.MIB)
            outgoing.flush(); os.fsync(outgoing.fileno())
        need(H.pin(target, check) == expected[name], "COPY_READBACK")
    H.census(package, selected, check); H.census(base, baseline, check)
    for name, pin in baseline.items():
        need(H.pin(base/name, check) == pin, "BASE_CHANGED")
    for name, source in selected.items():
        need(H.pin(source, check) == expected[name] and H.pin(package/name, check) == expected[name],
             "SOURCE_OR_OUTPUT_CHANGED")
    for path, pin in ((kit/"KIT-MANIFEST.json", manifest_pin), (receipt_path, receipt_pin),
                      (kit/BASE_MAP, old_map_pin), (mapping_path, map_pin), (own_path, own_pin)):
        need(H.pin(path, check, 2*H.MIB) == pin, "INPUT_CHANGED")
    need(H.pin(helper_path, check, 2*H.MIB)["sha256"] == HELPER_SHA, "HELPER_CHANGED")
    check(); H.fresh_bytes(package/"PROFILE.json", new_profile)
    H.census(package, expected, check)
    need(H.pin(package/"PROFILE.json", check) == expected["PROFILE.json"], "PROFILE_READBACK")
    report = dict(status="ASSEMBLED_NOT_ADOPTED", package=str(package), files=expected,
        base_kit_manifest=manifest_pin, base_kit_receipt=receipt_pin, base_profile_sha256=BASE_PROFILE_SHA,
        profile_sha256=expected["PROFILE.json"]["sha256"], installation_manifest_sha256=INSTALLATION_SHA,
        implementation_id=H.digest(b"DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1\0"+H.canonical(installed["implementation"])),
        changed_files=changed, added_files=[], unchanged_files=154, files_excluding_profile=159,
        auxiliary_files=122, source_map=map_pin, base_source_map=old_map_pin, assembler=own_pin,
        native_calls=0, owner_opened=False, wall_seconds=time.monotonic()-started,
        cpu_seconds=time.process_time()-cpu, claim="FILE_ASSEMBLY_NOT_RUNTIME_OR_MATHEMATICAL_ACCEPTANCE")
    check(); H.fresh_bytes(output/"ASSEMBLY.json", H.canonical(report)); check()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("source-root", "base-kit", "kit-receipt", "source-map-sha256", "output"):
        parser.add_argument("--"+key, required=True)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    main()

"""Changed-interface checks only; no product, native, owner or network operation.

Run inside the root-selected outer Job. The source root may be a relocated
investigator archive. Actual package bytes are read, never executed or modified.
Only a fresh synthetic output tree and inert prepared requests are written.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import types


def need(ok, label):
    if not ok:
        raise AssertionError(label)


def refusal(call, expected):
    try:
        call()
    except ValueError as error:
        need(str(error) == expected, (expected, str(error)))
    else:
        raise AssertionError("missing refusal: " + expected)


def run(source_root: Path, package: Path, profile_sha256: str, output: Path):
    here = source_root / "software/v5/ordinary_investigator_bundle"
    selected = here / "prepare_selected.py"
    raw = selected.read_bytes()
    need(hashlib.sha256(raw).hexdigest() ==
         "72f27b6644f998a16b5fb3eb785d576a68d48338949b135cc4e96c18b8b89afc",
         "selected source")
    wrapper = types.ModuleType("_investigator_selector_checks")
    wrapper.__file__ = str(selected)
    exec(compile(raw, str(selected), "exec"), wrapper.__dict__)
    kit = wrapper.load_helper()  # Exact pinned inert request preparer, not product code.
    output = kit.ordinary_path(output, directory=True, fresh=True)
    kit.ordinary_path(output.parent, directory=True, existing=True)
    kit.disjoint(output, source_root)
    kit.disjoint(output, package)
    mapping = json.loads((here / "compatibility.json").read_bytes())
    prior = json.loads((source_root /
        "software/v5/ordinary_bounded_transport/compatibility.json").read_bytes())
    overlay = json.loads((source_root /
        "software/v5/ordinary_exact_module/OVERLAY.json").read_bytes())["files"]
    changed = {name for name, pin in prior["sparse_noncompiled"].items()
               if mapping["sparse_noncompiled"][name] != pin}
    need(changed == set(overlay) and len(changed) == 3 and
         all(mapping["sparse_noncompiled"][name] == overlay[name] for name in changed)
         and mapping["native_roles"] == prior["native_roles"] and
         mapping["schema"] == prior["schema"], "exact three-role successor")
    profile_raw = (package / "PROFILE.json").read_bytes()
    need(hashlib.sha256(profile_raw).hexdigest() == profile_sha256, "profile fixture")
    profile = json.loads(profile_raw)
    label, sources = wrapper.known_layout(kit, profile, mapping)
    need(label == "exact-module-investigator-v1" and len(sources) == 45,
         "actual current interface")
    cases = ["exact-three-role-map-and-current-profile"]

    # No mixtures of the old/new exact-module sources are silently compatible.
    for name in sorted(changed):
        mixed = deepcopy(profile)
        mixed["files"][name] = prior["sparse_noncompiled"][name]
        refusal(lambda: wrapper.known_layout(kit, mixed, mapping),
                "KIT_SELECT_UNKNOWN_INTERFACE")
        cases.append("mixed-old-source-refused:" + name)
    refusal(lambda: wrapper.known_layout(kit, profile, prior),
            "KIT_SELECT_UNKNOWN_INTERFACE")
    cases.append("old-map-cannot-approve-current-profile")

    # Native identities can vary across approved builds; this selector must not
    # pretend to check native artifacts merely by recognizing their role names.
    native_variant = deepcopy(profile)
    native_variant["files"][mapping["native_roles"][0]]["sha256"] = "0" * 64
    need(wrapper.known_layout(kit, native_variant, mapping)[0] == label,
         "native identities are a separate approval boundary")
    cases.append("native-role-shape-not-native-authentication")

    output.mkdir()
    request = {"action": "init", "state": {
        "catalog": str(output / "future-catalog"),
        "custody": str(output / "future-custody"), "store_id": "1" * 64},
        "custody_limits": {"objects": 100, "exports": 1000,
                           "logical_bytes": 1048576, "db_pages": 256}}
    request_path = output / "request.json"
    with request_path.open("xb") as stream:
        stream.write(kit.canonical(request))
    result = wrapper.prepare_selected(package, profile_sha256, request_path,
                                      output / "prepared")
    need(result["interface"] == label and result["known_noncompiled_roles"] == 45
         and result["preparation"]["profile_sha256"] == profile_sha256
         and result["preparation"]["commands_executed"] == 0
         and result["native_artifacts_checked"] is False
         and result["mathematical_acceptance"] is False
         and not (output / "future-catalog").exists()
         and not (output / "future-custody").exists(), "inert preparation")
    cases.append("actual-source-pins-and-inert-init")

    bad_output = output / "wrong-profile-output"
    refusal(lambda: wrapper.prepare_selected(package, "0" * 64, request_path,
                                             bad_output), "KIT_SELECT_PROFILE_PIN")
    need(not bad_output.exists(), "wrong-profile no output")
    cases.append("wrong-profile-before-output")

    # One actual altered source tests pin enforcement. The unchanged selector
    # loop already validates every one of the 45 roles; no native files are copied.
    counterfeit = output / "altered-source"
    counterfeit.mkdir()
    with (counterfeit / "PROFILE.json").open("xb") as stream:
        stream.write(profile_raw)
    for name in sources:
        data = (package / name).read_bytes()
        if name == "authoring/py/anchor_store.py":
            data = bytes([data[0] ^ 1]) + data[1:]
        target = counterfeit / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(data)
    bad_output = output / "wrong-source-output"
    refusal(lambda: wrapper.prepare_selected(counterfeit, profile_sha256,
        request_path, bad_output), "KIT_SELECT_ACTUAL_SOURCE_PIN")
    need(not bad_output.exists(), "wrong-source no output")
    cases.append("altered-actual-source-before-output")
    need(len(cases) == 9, "case census")
    report = {"passed": True, "cases": cases, "preparation": result,
              "native_operations": 0, "mathematical_acceptance": False}
    with (output / "RESULT.json").open("xb") as stream:
        stream.write(kit.canonical(report))
    return report


if __name__ == "__main__":
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, "isolated interpreter")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for option in ("source-root", "package", "profile-sha256", "output"):
        parser.add_argument("--" + option, required=True)
    args = parser.parse_args()
    print(json.dumps(run(Path(args.source_root), Path(args.package),
                         args.profile_sha256, Path(args.output)), sort_keys=True))

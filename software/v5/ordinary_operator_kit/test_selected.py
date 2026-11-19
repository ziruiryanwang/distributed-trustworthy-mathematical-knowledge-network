"""Small native-free controls for explicit known-interface selection only."""
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

BASE_PROFILE = "9c41b9a3fe36f7283af130ac6ef290e82c2a78c432980b2bea75ccdcf197a6d4"


def need(ok, code):
    if not ok: raise AssertionError(code)


def main():
    p = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("source-root", "base-package", "output"):
        p.add_argument("--"+name, type=Path, required=True)
    p.add_argument("--fair-package", type=Path, required=True)
    p.add_argument("--fair-profile", required=True)
    args = p.parse_args()
    need(all(path.is_absolute() for path in (args.source_root, args.base_package, args.fair_package, args.output)) and
         not args.output.exists() and args.output.parent.is_dir(), "FRESH_ABSOLUTE_OUTPUT")
    source = args.source_root / "ordinary_operator_kit" / "prepare_selected.py"
    spec = importlib.util.spec_from_file_location("selected_control", source)
    wrapper = importlib.util.module_from_spec(spec)
    args.output.mkdir()
    cases = []
    with ExitStack() as stack:
        for module, name in ((subprocess, "Popen"), (subprocess, "run"), (os, "system"),
                             (socket, "socket"), (socket, "create_connection"), (sqlite3, "connect")):
            stack.enter_context(patch.object(module, name, side_effect=AssertionError("NO_PRODUCT_EXECUTION")))
        spec.loader.exec_module(wrapper)
        kit = wrapper.load_helper()
        profile_raw = kit.Inputs().read(args.base_package / "PROFILE.json", 2*1024**2)
        need(hashlib.sha256(profile_raw).hexdigest() == BASE_PROFILE, "EXACT_BASE_PROFILE")
        doc = kit.Inputs().json(profile_raw)
        mapping = kit.Inputs().json((source.parent / "compatibility.json").read_bytes())
        need(wrapper.known_layout(kit, doc, mapping)[0] == "ordinary", "BASE_LAYOUT")
        cases.append("base-layout")
        fair = deepcopy(doc); fair["files"].update(mapping["fair_overrides"])
        need(wrapper.known_layout(kit, fair, mapping)[0] == "fair-search", "FAIR_LAYOUT")
        cases.append("coherent-fair-layout")
        rebuilt = deepcopy(fair)
        rebuilt["installation_manifest_sha256"] = "f"*64
        for name in mapping["native_roles"]:
            rebuilt["files"][name] = {"bytes": 123, "sha256": "e"*64}
        need(wrapper.known_layout(kit, rebuilt, mapping)[0] == "fair-search", "NATIVE_NOT_APPROVED_HERE")
        cases.append("native-identity-variation-not-native-approval")
        for label, alter in (
            ("hybrid-refused", lambda d: d["files"].update({"profile.py": mapping["fair_overrides"]["profile.py"]})),
            ("extra-role-refused", lambda d: d["files"].update({"extra.py": {"bytes": 1, "sha256": "0"*64}})),
            ("unknown-code-refused", lambda d: d["files"]["owner.py"].update(sha256="0"*64)),
            ("boolean-native-size-refused", lambda d: d["files"][mapping["native_roles"][0]].update(bytes=True)),
            ("schema-refused", lambda d: d.update(schema="unknown")),
        ):
            changed = deepcopy(doc); alter(changed)
            try: wrapper.known_layout(kit, changed, mapping)
            except ValueError: cases.append(label)
            else: raise AssertionError(label)
        request = {"action": "init", "state": {"catalog": str(args.output/"future-catalog"),
                   "custody": str(args.output/"future-custody"), "store_id": "1"*64},
                   "custody_limits": {"objects": 100, "exports": 1000,
                                      "logical_bytes": 1048576, "db_pages": 256}}
        request_path = args.output / "request.json"
        with request_path.open("xb") as f: f.write(kit.canonical(request))
        result = wrapper.prepare_selected(args.base_package, BASE_PROFILE, request_path, args.output/"prepared")
        need(result["interface"] == "ordinary" and result["known_noncompiled_roles"] == 41 and
             not result["native_artifacts_checked"] and not result["mathematical_acceptance"], "SELECTION_BOUNDARY")
        need(result["preparation"]["profile_sha256"] == BASE_PROFILE and
             result["preparation"]["commands_executed"] == 0 and
             not (args.output/"future-catalog").exists() and not (args.output/"future-custody").exists(),
             "INERT_OUTPUT")
        cases.append("actual-base-source-pins-and-inert-init")
        result_fair = wrapper.prepare_selected(args.fair_package, args.fair_profile,
                                               request_path, args.output/"prepared-fair")
        need(result_fair["interface"] == "fair-search" and
             result_fair["known_noncompiled_roles"] == 43 and
             result_fair["preparation"]["profile_sha256"] == args.fair_profile and
             not result_fair["native_artifacts_checked"], "ACTUAL_FAIR_SELECTION")
        cases.append("actual-fair-source-pins-and-inert-init")
        rejected = args.output/"bad-profile-output"
        try: wrapper.prepare_selected(args.base_package, "0"*64, request_path, rejected)
        except ValueError as e: need(str(e) == "KIT_SELECT_PROFILE_PIN", "EXACT_PROFILE_REFUSAL")
        else: raise AssertionError("MISSING_PROFILE_REFUSAL")
        need(not rejected.exists(), "REFUSAL_BEFORE_WRITE")
        cases.append("wrong-profile-refuses-before-write")
        # Fresh synthetic metadata/code only; omit native artifacts deliberately.
        # A same-length altered source must refuse, not be executed.
        counterfeit = args.output/"altered-code"; counterfeit.mkdir()
        with (counterfeit/"PROFILE.json").open("xb") as f: f.write(profile_raw)
        for name in mapping["base_noncompiled"]:
            path = counterfeit/name; path.parent.mkdir(parents=True, exist_ok=True)
            raw = (args.base_package/name).read_bytes()
            if name == "owner.py": raw = bytes([raw[0] ^ 1]) + raw[1:]
            with path.open("xb") as f: f.write(raw)
        rejected = args.output/"bad-source-output"
        try: wrapper.prepare_selected(counterfeit, BASE_PROFILE, request_path, rejected)
        except ValueError as e: need(str(e) == "KIT_SELECT_ACTUAL_SOURCE_PIN", "EXACT_SOURCE_REFUSAL")
        else: raise AssertionError("MISSING_SOURCE_REFUSAL")
        need(not rejected.exists(), "SOURCE_REFUSAL_BEFORE_WRITE")
        cases.append("changed-source-refuses-before-write")
    need(len(cases) == 12, "CASE_CENSUS")
    report = {"cases": cases, "count": len(cases), "passed": True,
              "scope": "CONFIG_COMPATIBILITY_NOT_NATIVE_OR_MATHEMATICS", "product_execution": False}
    with (args.output/"RESULT.json").open("xb") as f: f.write(kit.canonical(report))
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()

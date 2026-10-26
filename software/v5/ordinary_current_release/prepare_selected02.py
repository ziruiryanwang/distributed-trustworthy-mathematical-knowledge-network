"""Current offline interface selection; never executes product or opens state."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import time

MIB = 1024**2
RELEASE = "software/v5/ordinary_current_release/release.json"
RELEASE_SHA = "821796aa5b4996edd3f34babdb3be186d8321e0b3b4208b1e3f18705400caf78"
HELPER = "software/v5/ordinary_multi_source_package/prepare.py"
HELPER_SHA = "77f0bc5c6d02e1a87c29e44d71cbb77de4f1655998b980c9b71eb14085afb2b0"


def load_helper(source_root):
    path = Path(source_root) / HELPER
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("SELECT_ABSOLUTE_HELPER")
    for ancestor in (*reversed(path.parents), path):
        info = ancestor.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("SELECT_REDIRECTED_HELPER")
        if ancestor != path and not stat.S_ISDIR(info.st_mode):
            raise ValueError("SELECT_HELPER_ANCESTRY")
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size != 34599:
        raise ValueError("SELECT_HELPER_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(MIB + 1)
    if len(raw) != 34599 or hashlib.sha256(raw).hexdigest() != HELPER_SHA:
        raise ValueError("SELECT_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_current_inert_preparer", path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def known_layout(kit, doc, release):
    kit.fields(doc, {"schema", "installation_manifest_sha256", "helper_paths", "author_worker", "files"})
    kit.need(release.get("schema") == "DMKN_ORDINARY_CURRENT_RELEASE_SELECTION_V1",
             "SELECT_RELEASE_SCHEMA")
    build = release["build"]
    layout = build["profile"]
    kit.need(doc["schema"] == layout["owner_schema"] and
             doc["helper_paths"] == layout["helper_paths"] and
             doc["author_worker"] == layout["author_worker"], "SELECT_PROFILE_LAYOUT")
    kit.identifier(doc["installation_manifest_sha256"])
    sources, native = build["noncompiled_roles"], build["native_roles"]
    kit.need(type(sources) is dict and len(sources) == 45 and type(native) is list and
             len(native) == 72 and len(set(native)) == 72 and not set(sources) & set(native),
             "SELECT_KNOWN_ROLE_CENSUS")
    files = doc["files"]
    kit.need(type(files) is dict and set(files) == set(sources) | set(native) and
             all(files.get(name) == pin for name, pin in sources.items()), "SELECT_UNKNOWN_INTERFACE")
    total = 0
    for pin in files.values():
        kit.fields(pin, {"bytes", "sha256"})
        kit.integer(pin["bytes"], 1, 128*MIB)
        kit.identifier(pin["sha256"])
        total += pin["bytes"]
    kit.need(total <= 512*MIB, "SELECT_PROFILE_TOTAL")
    return "current-investigator-v1", sources


def prepare_selected(source_root, package, profile_sha256, request, output):
    started, cpu = time.monotonic(), time.process_time()
    kit = load_helper(source_root)
    def check():
        kit.need(time.monotonic()-started < 60 and time.process_time()-cpu < 30,
                 "SELECT_COOPERATIVE_ALLOWANCE")
    check()
    root = kit.ordinary_path(source_root, existing=True, directory=True)
    package = kit.ordinary_path(package, existing=True, directory=True)
    output = kit.ordinary_path(output, fresh=True, directory=True)
    kit.disjoint(root, output)
    kit.disjoint(package, output)
    kit.disjoint(Path(__file__).absolute().parent, output)
    profile_sha256 = kit.identifier(profile_sha256)
    reader = kit.Inputs()
    release_raw = reader.read(root/RELEASE, 2*MIB)
    kit.need(kit.digest(release_raw) == RELEASE_SHA, "SELECT_RELEASE_PIN")
    release = reader.json(release_raw)
    raw = reader.read(package/"PROFILE.json", 2*MIB)
    kit.need(kit.digest(raw) == profile_sha256, "SELECT_PROFILE_PIN")
    label, sources = known_layout(kit, reader.json(raw), release)
    for name, expected in sources.items():
        check()
        source = kit.Inputs().read(package/name, 2*MIB)
        kit.need({"bytes": len(source), "sha256": kit.digest(source)} == expected,
                 "SELECT_ACTUAL_SOURCE_PIN")
    kit.need(reader.read(root/RELEASE, 2*MIB) == release_raw and
             reader.read(package/"PROFILE.json", 2*MIB) == raw and
             kit.digest(reader.read(root/HELPER, MIB)) == HELPER_SHA, "SELECT_INPUT_CHANGED")
    check()
    kit.PROFILE = profile_sha256  # One fresh private helper; old reports stay bound to their own profile.
    result = kit.prepare(Path(request), output)
    check()
    kit.need(reader.read(root/RELEASE, 2*MIB) == release_raw and
             reader.read(package/"PROFILE.json", 2*MIB) == raw and
             kit.digest(reader.read(root/HELPER, MIB)) == HELPER_SHA, "SELECT_INPUT_CHANGED")
    return {"schema": "DMKN_OPERATOR_SELECTED_INTERFACE_PREPARATION_V1",
            "interface": label, "package": str(package), "profile_sha256": profile_sha256,
            "release_sha256": RELEASE_SHA, "known_noncompiled_roles": len(sources),
            "preparation": result, "native_artifacts_checked": False,
            "mathematical_acceptance": False,
            "boundary": "KNOWN_CONFIG_INTERFACE_NOT_PACKAGE_AUTHENTICATION_OR_NATIVE_APPROVAL"}


def main():
    if (os.name != "nt" or not sys.flags.isolated or not sys.flags.no_site or
            not sys.dont_write_bytecode or sys.flags.optimize):
        raise ValueError("SELECT_APPROVED_ISOLATED_PYTHON_REQUIRED")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("source-root", "package", "profile-sha256", "request", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    result = prepare_selected(Path(args.source_root), Path(args.package), args.profile_sha256,
                              Path(args.request), Path(args.output))
    print(json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()

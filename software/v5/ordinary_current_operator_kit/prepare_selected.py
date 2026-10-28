"""Explicit current-interface package selection for the offline preparer.

Never imports product code or checks native artifacts/mathematics. The operator
approves the package/profile; this only binds compatible report/config schemas.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import stat
import sys
import time

HELPER_SHA = "359bd0e8bd6e5cabd0495bd25eb5a631f16edd92c12afb3b5a5b523434416247"
MAP_SHA = "08129a60872238eb5dec174fb21a996fc7f5db69748ae623121fe3b51c4af719"
MIB = 1024**2


def load_helper():
    path = Path(__file__).absolute().parent / "prepare.py"
    for ancestor in (*reversed(path.parents), path):
        info = ancestor.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("SELECT_REDIRECTED_HELPER")
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or not 0 < info.st_size <= MIB:
        raise ValueError("SELECT_HELPER_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(MIB+1)
    if hashlib.sha256(raw).hexdigest() != HELPER_SHA:
        raise ValueError("SELECT_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_selected_inert_preparer", path)
    module = importlib.util.module_from_spec(spec)
    # No sys.path changes, product import, reload or persistent shared module.
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def known_layout(kit, doc, compatibility):
    kit.fields(doc, {"schema", "installation_manifest_sha256", "helper_paths", "author_worker", "files"})
    kit.need(doc["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
             doc["helper_paths"] == ["authoring/helpers"] and
             doc["author_worker"] == "author_worker.py", "SELECT_PROFILE_LAYOUT")
    kit.identifier(doc["installation_manifest_sha256"])
    kit.fields(compatibility, {"schema", "direct_sources", "generated_roles"})
    kit.need(compatibility["schema"] == "DMKN_OPERATOR_CURRENT_INTERFACE_V1", "SELECT_MAP_SCHEMA")
    sources, generated = compatibility["direct_sources"], compatibility["generated_roles"]
    kit.need(type(sources) is dict and len(sources) == 45 and
             type(generated) is list and len(generated) == 72 and
             len(set(generated)) == len(generated) and not set(sources) & set(generated), "SELECT_MAP_ROLES")
    files = doc["files"]
    kit.need(type(files) is dict, "SELECT_PROFILE_FILES")
    kit.need(set(files) == set(sources) | set(generated) and
             all(files.get(name) == pin for name, pin in sources.items()), "SELECT_UNKNOWN_INTERFACE")
    total = 0
    for pin in files.values():
        kit.fields(pin, {"bytes", "sha256"})
        kit.integer(pin["bytes"], 1, 128*MIB)
        kit.identifier(pin["sha256"])
        total += pin["bytes"]
    kit.need(total <= 512*MIB, "SELECT_PROFILE_TOTAL")
    return "current-frontier-sparse-multisource", sources


def prepare_selected(package, profile_sha256, request, output):
    started, cpu = time.monotonic(), time.process_time()
    kit = load_helper()
    def check():
        kit.need(time.monotonic()-started < 60 and time.process_time()-cpu < 30,
                 "SELECT_COOPERATIVE_ALLOWANCE")
    check()
    package = kit.ordinary_path(package, existing=True, directory=True)
    output = kit.ordinary_path(output, fresh=True, directory=True)
    kit.disjoint(package, output)
    kit.disjoint(Path(__file__).absolute().parent, output)
    profile_sha256 = kit.identifier(profile_sha256)
    profile_path = package / "PROFILE.json"
    reader = kit.Inputs()
    raw = reader.read(profile_path, 2*MIB)
    kit.need(kit.digest(raw) == profile_sha256, "SELECT_PROFILE_PIN")
    map_path = Path(__file__).absolute().parent / "compatibility.json"
    map_raw = reader.read(map_path, MIB)
    kit.need(kit.digest(map_raw) == MAP_SHA, "SELECT_COMPATIBILITY_PIN")
    doc, mapping = reader.json(raw), reader.json(map_raw)
    label, sources = known_layout(kit, doc, mapping)
    for name, expected in sources.items():
        check()
        # Names come only from the exact pinned local compatibility map.
        source = kit.Inputs().read(package / name, 2*MIB)
        kit.need({"bytes": len(source), "sha256": kit.digest(source)} == expected,
                 "SELECT_ACTUAL_SOURCE_PIN")
    check()
    kit.need(reader.read(profile_path, 2*MIB) == raw, "SELECT_PROFILE_CHANGED")
    # Explicit selected configuration, not an edit to the frozen helper constant.
    # This private module is freshly loaded for this one call and is never shared.
    kit.PROFILE = profile_sha256
    result = kit.prepare(Path(request), output)
    check()
    return {"schema": "DMKN_OPERATOR_SELECTED_INTERFACE_PREPARATION_V1",
            "interface": label, "package": str(package), "profile_sha256": profile_sha256,
            "known_noncompiled_roles": len(sources), "preparation": result,
            "native_artifacts_checked": False, "mathematical_acceptance": False,
            "boundary": "KNOWN_CONFIG_INTERFACE_NOT_PACKAGE_AUTHENTICATION_OR_NATIVE_APPROVAL"}


def main():
    if os.name != "nt" or not sys.flags.isolated or not sys.flags.no_site or not sys.dont_write_bytecode:
        raise ValueError("SELECT_APPROVED_ISOLATED_PYTHON_REQUIRED")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("package", "profile-sha256", "request", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    result = prepare_selected(Path(args.package), args.profile_sha256, Path(args.request), Path(args.output))
    import json
    print(json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()

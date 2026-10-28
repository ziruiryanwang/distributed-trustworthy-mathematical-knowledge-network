"""Pack or verify a selected local commons kit; never execute product code.

The selection and external manifest digest are operator approvals of exact
bytes. They are not signatures, mathematical warrants or source execution.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import types
import zipfile

MIB = 1024**2
HELPER_SHA = "b5d211a83644b61c6a6fe673785ccd1e1960816a2d58f20787b9d4dfdb3c9da9"
MANIFEST = "KIT-MANIFEST.json"
SCHEMA = "DMKN_ORDINARY_USABLE_LOCAL_KIT_V1"
PROFILE = "f75dda6e534450cdf5d4db2901c3e1964501514da817bc3eb8aadebc0c350f7b"
INSTALLATION = "9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27"
SOURCE_MAP = "source/software/v5/ordinary_registration_refresh/source-map.json"
SOURCE_MAP_SHA = "aeab07b21fb755614ea1432ca9b748d2f8abbfe8c6f43f262de9d2da66cbdb85"
BUILDER = "source/software/v5/ordinary_registration_refresh/build.py"
BUILDER_SHA = "08580aa9348cc1c84ceb2719fcd7748feba7c8ce51bd5d10eb82924918b1ccc3"
REQUIRED = {"GUIDE.md", "REQUESTS.json", "REFRESH-USAGE.md", "REFRESH-REQUESTS.json", "kit.py", "file_helpers.py",
            "operator/prepare.py", "operator/prepare_selected.py", "operator/compatibility.json",
            "preview/view_preview.py", "preview/render.py", SOURCE_MAP, BUILDER}
EXTERNAL = {"os": "Windows x86-64", "python": "3.14.6", "lean": "4.34.0"}
CLAIM = "LOCAL_UNPUBLISHED_DISTRIBUTION_NOT_NEW_MATHEMATICAL_ACCEPTANCE"


def need(condition, code):
    if not condition:
        raise ValueError("KIT_" + code)


def helper():
    path = Path(__file__).absolute().parent / "file_helpers.py"
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "HELPER_REDIRECT")
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and 0 < info.st_size <= MIB,
         "HELPER_KIND")
    with path.open("rb") as stream:
        raw = stream.read(MIB+1)
    need(hashlib.sha256(raw).hexdigest() == HELPER_SHA, "HELPER_PIN")
    module = types.ModuleType("_kit_file_helpers")
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def files_checked(H, files):
    need(type(files) is dict and 250 <= len(files) <= 384 and
         len({name.casefold() for name in files}) == len(files), "FILE_COUNT")
    need(REQUIRED <= set(files) and MANIFEST not in files, "REQUIRED_FILES")
    total = 0
    for name, pin in files.items():
        H.relative(name)
        need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
             type(pin["bytes"]) is int and 0 < pin["bytes"] <= 8*MIB, "PIN")
        H.hexid(pin["sha256"])
        need(not any(p.as_posix() in files for p in PurePosixPath(name).parents), "FILE_DIR_ALIAS")
        total += pin["bytes"]
    need(total <= 64*MIB, "TOTAL")
    need(sum(name.startswith("package/") for name in files) == 160 and
         files["package/PROFILE.json"]["sha256"] == PROFILE and
         files[SOURCE_MAP]["sha256"] == SOURCE_MAP_SHA and
         files[BUILDER]["sha256"] == BUILDER_SHA and
         files["file_helpers.py"]["sha256"] == HELPER_SHA, "CURRENT_SELECTION")
    return files


def census(H, root, files, check):
    allowed_dirs = {p.as_posix() for name in files for p in PurePosixPath(name).parents
                    if p.as_posix() != "."}
    seen, dirs, pending, count = set(), set(), [root], 0
    while pending:
        with os.scandir(H.ordinary(pending.pop(), directory=True)) as listing:
            for entry in listing:
                check(); count += 1
                need(count <= 1024, "TREE_BOUND")
                path = Path(entry.path)
                name = H.relative(path.relative_to(root).as_posix())
                if entry.is_dir(follow_symlinks=False):
                    H.ordinary(path, directory=True)
                    need(name in allowed_dirs and name not in dirs, "EXTRA_DIRECTORY")
                    dirs.add(name); pending.append(path)
                else:
                    H.ordinary(path)
                    need(name in files and name not in seen, "EXTRA_FILE")
                    seen.add(name)
    need(seen == set(files) and dirs == allowed_dirs, "TREE_CENSUS")


def content_relations(H, data):
    profile = H.strict_json(data["package/PROFILE.json"])
    need(profile.get("installation_manifest_sha256") == INSTALLATION, "INSTALLATION")
    installation_raw = data["package/installation/INSTALLATION.json"]
    need(H.sha(installation_raw) == INSTALLATION, "INSTALLATION_BYTES")
    installation = H.strict_json(installation_raw)
    for name, pin in installation["files"].items():
        H.relative(name)
        # The exact pinned installation manifest also names external toolchains.
        # This kit carries no runtime and does not validate those installations.
        if name.startswith(("python_runtime/", "lean_runtime/")):
            continue
        need("package/installation/"+name in data and
             H.pin(data["package/installation/"+name]) == pin, "INSTALLATION_PAYLOAD")
    for name, pin in profile["files"].items():
        need("package/" + name in data and H.pin(data["package/"+name]) == pin, "PROFILE_PAYLOAD")
    mapping = H.strict_json(data[SOURCE_MAP])
    need(len(mapping["sources"]) == 93, "SOURCE_COUNT")
    for name, pin in mapping["sources"].items():
        H.relative(name)
        need("source/"+name in data and H.pin(data["source/"+name]) == pin, "SOURCE_CLOSURE")


def verify(root, manifest_sha256, *, H=None, check=None):
    H = H or helper()
    check = H.guard(check)
    root = H.ordinary(root, directory=True)
    raw = H.read(root/MANIFEST, check)
    need(H.sha(raw) == H.hexid(manifest_sha256), "MANIFEST_PIN")
    doc = H.strict_json(raw)
    need(type(doc) is dict and set(doc) == {"schema", "files", "external_profile", "claim",
         "license_status", "profile_sha256", "installation_sha256"} and
         doc["schema"] == SCHEMA and doc["external_profile"] == EXTERNAL and
         doc["claim"] == CLAIM and doc["license_status"] == "UNDECIDED_LOCAL_ONLY" and
         doc["profile_sha256"] == PROFILE and doc["installation_sha256"] == INSTALLATION and
         H.canonical(doc) == raw, "MANIFEST_SCHEMA")
    files = files_checked(H, doc["files"])
    census(H, root, set(files) | {MANIFEST}, check)
    data = {}
    for name, pin in sorted(files.items()):
        data[name] = H.read(root/name, check, 8*MIB)
        need(H.pin(data[name]) == pin, "PAYLOAD:" + name)
    content_relations(H, data)
    need(H.read(root/MANIFEST, check) == raw, "MANIFEST_CHANGED")
    census(H, root, set(files) | {MANIFEST}, check)
    return {"status": "VERIFIED_LOCAL_KIT_BYTES", "manifest": H.pin(raw),
            "payload_files": len(files), "profile_sha256": PROFILE, "claim": CLAIM}


def pack(source_root, package, selection, selection_sha256, output):
    H = helper(); check = H.guard()
    root = H.ordinary(source_root, directory=True)
    package = H.ordinary(package, directory=True)
    selection = H.ordinary(selection)
    output = H.ordinary(output, directory=True, fresh=True)
    need(not root.is_relative_to(output) and not package.is_relative_to(output) and
         not output.is_relative_to(package) and not selection.is_relative_to(output), "OUTPUT_OVERLAP")
    selected_raw = H.read(selection, check)
    need(H.sha(selected_raw) == H.hexid(selection_sha256), "SELECTION_PIN")
    selected = H.strict_json(selected_raw)
    need(set(selected) == {"schema", "files"} and
         selected["schema"] == "DMKN_LOCAL_KIT_SOURCE_SELECTION_V1", "SELECTION_SCHEMA")
    rows = selected["files"]
    need(type(rows) is dict and 250 <= len(rows) <= 384, "SELECTION_COUNT")
    data, origins, pins = {}, {}, {}
    for name, row in sorted(rows.items()):
        H.relative(name)
        need(type(row) is dict and set(row) == {"origin", "path", "bytes", "sha256"} and
             row["origin"] in ("source", "package"), "SELECTION_ROW")
        relative = H.relative(row["path"])
        need(row["origin"] != "source" or relative.startswith(("software/v5/", "software/assets/foundation/")),
             "SOURCE_SCOPE")
        pins[name] = {"bytes": row["bytes"], "sha256": row["sha256"]}
        origins[name] = (root if row["origin"] == "source" else package) / relative
        need(not origins[name].is_relative_to(output), "SELECTED_OUTPUT_OVERLAP")
    files_checked(H, pins)
    need({name: pin for name, pin in pins.items() if name.startswith("package/")} ==
         {"package/"+row["path"]: pins[name] for name, row in rows.items() if row["origin"] == "package"},
         "PACKAGE_MAPPING")
    for name, path in origins.items():
        data[name] = H.read(path, check, 8*MIB)
        need(H.pin(data[name]) == pins[name], "SELECTED_PAYLOAD:" + name)
    need(H.read(Path(__file__).absolute(), check) == data["kit.py"], "RUNNING_UTILITY")
    content_relations(H, data)
    census(H, package, {name.removeprefix("package/") for name in pins if name.startswith("package/")}, check)
    doc = {"schema": SCHEMA, "files": pins, "external_profile": EXTERNAL,
           "claim": CLAIM, "license_status": "UNDECIDED_LOCAL_ONLY",
           "profile_sha256": PROFILE, "installation_sha256": INSTALLATION}
    manifest_raw = H.canonical(doc)
    need(len(manifest_raw) <= 2*MIB, "MANIFEST_BOUND")
    data[MANIFEST] = manifest_raw
    output.mkdir()
    archive_path = output/"commons-local.zip"
    with H.ordinary(archive_path, fresh=True).open("xb") as stream:
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED, allowZip64=False) as archive:
            for name, raw in sorted(data.items()):
                check()
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3; info.external_attr = 0o100644 << 16
                archive.writestr(info, raw)
        stream.flush(); os.fsync(stream.fileno())
    archive_pin = H.pin(H.read(archive_path, check, 72*MIB))
    # Extract only this exact freshly produced archive into one fresh directory.
    # No extractall, peer archive, implicit overwrite or path supplied by a peer.
    extracted = output/"commons"; extracted.mkdir()
    with zipfile.ZipFile(archive_path, "r") as archive:
        entries = archive.infolist()
        need(archive.comment == b"" and [row.filename for row in entries] == sorted(data), "ZIP_CENSUS")
        for row in entries:
            check(); name = H.relative(row.filename)
            need(row.compress_type == zipfile.ZIP_STORED and row.extra == row.comment == b"" and
                 row.file_size == row.compress_size == len(data[name]) and
                 row.date_time == (1980, 1, 1, 0, 0, 0) and
                 row.create_system == 3 and row.external_attr == 0o100644 << 16 and row.flag_bits == 0,
                 "ZIP_METADATA")
            raw = archive.read(row)
            need(raw == data[name], "ZIP_BYTES")
            target = extracted/name; target.parent.mkdir(parents=True, exist_ok=True)
            H.fresh_bytes(target, raw)
    verified = verify(extracted, H.sha(manifest_raw), H=H, check=check)
    for name, path in origins.items():
        need(H.read(path, check, 8*MIB) == data[name], "INPUT_CHANGED:"+name)
    need(H.read(selection, check) == selected_raw, "SELECTION_CHANGED")
    census(H, package, {name.removeprefix("package/") for name in pins if name.startswith("package/")}, check)
    need(H.pin(H.read(archive_path, check, 72*MIB)) == archive_pin, "ARCHIVE_CHANGED")
    receipt = {"status": "PACKED_AND_RELOCATED_LOCAL_KIT", "manifest": H.pin(manifest_raw),
               "archive": archive_pin, "selection_sha256": selection_sha256,
               "verification": verified, "claim": CLAIM}
    H.fresh_bytes(output/"RECEIPT.json", H.canonical(receipt))
    return receipt


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_PYTHON")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    sub = parser.add_subparsers(dest="action", required=True)
    packing = sub.add_parser("pack", allow_abbrev=False)
    for name in ("source-root", "package", "selection", "selection-sha256", "output"):
        packing.add_argument("--"+name, required=True)
    verifying = sub.add_parser("verify", allow_abbrev=False)
    verifying.add_argument("--root", required=True)
    verifying.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args()
    result = pack(Path(args.source_root), Path(args.package), Path(args.selection),
                  args.selection_sha256, Path(args.output)) if args.action == "pack" else \
             verify(Path(args.root), args.manifest_sha256)
    print(json.dumps(result, sort_keys=True, ensure_ascii=True, allow_nan=False))


if __name__ == "__main__":
    main()

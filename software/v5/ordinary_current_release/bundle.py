"""Flat current source/prebuilt pack and exact-tree verify; no product execution.

Approved code, immutable local inputs and external archive approval are premises.
Only one pinned file-helper module executes. No compiler, state or network access.
Failures preserve partial output; no overwrite, cleanup, retry or prior packer chain.
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
PREFIX = "software/v5/ordinary_current_release/"
UTILITY = PREFIX + "bundle.py"
RELEASE = PREFIX + "release.json"
RELEASE_SHA = "821796aa5b4996edd3f34babdb3be186d8321e0b3b4208b1e3f18705400caf78"
HELPER = "software/v5/ordinary_release_bundle/bundle.py"
HELPER_SHA = "5a8742bec0c13f3c7e8104111ba883887d5569cbb1a5498d79567e998dcd4d32"
MANIFEST = "CURRENT-RELEASE-MANIFEST.json"
SCHEMA = "DMKN_ORDINARY_CURRENT_RELEASE_DISTRIBUTION_V1"
CLAIM = "EXACT_CURRENT_DISTRIBUTION_NOT_NEW_MATHEMATICAL_OR_DEPLOYMENT_ACCEPTANCE"
CAPS = {"source": (2*MIB, 8*MIB, 16*MIB), "prebuilt": (8*MIB, 64*MIB, 72*MIB)}
_helper = None


def need(condition, code):
    if not condition:
        raise ValueError("CURRENT_BUNDLE_"+code)


def helper():
    global _helper
    if _helper is not None:
        return _helper
    path = Path(__file__).absolute().parents[3] / HELPER
    for ancestor in (*reversed(path.parents), path):
        info = ancestor.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "HELPER_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if ancestor != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == 22041,
             "HELPER_PATH")
    with path.open("rb") as stream:
        raw = stream.read(22042)
    need(len(raw) == 22041 and hashlib.sha256(raw).hexdigest() == HELPER_SHA, "HELPER_PIN")
    module = types.ModuleType("_current_release_file_helpers")
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    _helper = module
    return module


def checked_pin(value, maximum=8*MIB):
    H = helper()
    need(type(value) is dict and set(value) == {"bytes", "sha256"} and
         type(value["bytes"]) is int and 0 < value["bytes"] <= maximum, "PIN_SHAPE")
    H.hexid(value["sha256"])
    return value


def selection(root, check):
    H = helper()
    raw = H.read(root/RELEASE, check)
    need(H.sha(raw) == RELEASE_SHA, "RELEASE_PIN")
    doc = H.strict_json(raw)
    need(doc["schema"] == "DMKN_ORDINARY_CURRENT_RELEASE_SELECTION_V1" and
         doc["release_support"]["manifest"] == MANIFEST,
         "RELEASE_SCHEMA")
    return doc, raw


def selected_paths(release, kind):
    """Return destination -> (source selector, relative input, fixed pin or None)."""
    H = helper()
    need(kind in CAPS, "KIND")
    paths = {}
    if kind == "source":
        paths.update({name: ("source", name, checked_pin(pin, 2*MIB))
                      for name, pin in release["build"]["sources"].items()})
    else:
        paths.update({"package/"+name: ("package", name, checked_pin(pin))
                      for name, pin in release["prebuilt"]["files"].items()})
    for name, row in release["companions"].items():
        need(name not in paths, "COMPANION_OVERLAP")
        paths[name] = ("source", row["source"], checked_pin(
            {"bytes": row["bytes"], "sha256": row["sha256"]}, 2*MIB))
    for name, source in release["release_support"][kind].items():
        need(name not in paths, "SUPPORT_OVERLAP")
        paths[name] = ("source", source, None)
    need(len(paths) == (106 if kind == "source" else 166) and
         len({name.casefold() for name in paths}) == len(paths) and MANIFEST not in paths,
         "SELECTED_CENSUS")
    for name, (_, source, _) in paths.items():
        H.relative(name); H.relative(source)
        need(not any(parent.as_posix() in paths for parent in
                     PurePosixPath(name).parents), "FILE_DIRECTORY_ALIAS")
    return paths


def check_tree(root, files, check):
    """Complete directory census and every selected byte, not only manifest rows."""
    H = helper()
    root = H.ordinary(Path(root), directory=True)
    need(type(files) is dict and 0 < len(files) <= 256 and
         len({name.casefold() for name in files}) == len(files), "TREE_FILES")
    for name, pin in files.items():
        H.relative(name); checked_pin(pin)
    H.census(root, files, check)
    for name, pin in sorted(files.items()):
        need(H.pin(H.read(root/name, check, pin["bytes"])) == pin, "TREE_PAYLOAD:"+name)
    H.census(root, files, check)


def inspect_archive(path, files, check, *, maximum=72*MIB):
    """Read actual stored ZIP members; no extraction or executable member import."""
    H = helper()
    raw_pin = H.pin(H.read(Path(path), check, maximum))
    need(type(files) is dict and 0 < len(files) <= 256 and
         len({name.casefold() for name in files}) == len(files), "ZIP_FILES")
    for name, pin in files.items():
        H.relative(name); checked_pin(pin)
    with zipfile.ZipFile(H.ordinary(Path(path)), "r") as archive:
        rows = archive.infolist()
        need(archive.comment == b"" and [row.filename for row in rows] == sorted(files), "ZIP_CENSUS")
        for row in rows:
            check(); H.relative(row.filename)
            expected = files[row.filename]
            need(row.date_time == (1980, 1, 1, 0, 0, 0) and row.create_system == 3 and
                 row.external_attr == 0o100644 << 16 and row.compress_type == zipfile.ZIP_STORED and
                 row.extra == row.comment == b"" and row.flag_bits == 0 and
                 row.file_size == row.compress_size == expected["bytes"], "ZIP_METADATA")
            need(H.pin(archive.read(row)) == expected, "ZIP_PAYLOAD")
    need(H.pin(H.read(Path(path), check, maximum)) == raw_pin, "ZIP_CHANGED")
    return raw_pin


def manifest_files(H, doc, release, release_raw):
    need(type(doc) is dict and set(doc) == {"schema", "kind", "claim", "release", "files",
         "entrypoints", "external_profile", "license_status"}, "MANIFEST_FIELDS")
    kind = doc["kind"]
    need(kind in CAPS and doc["schema"] == SCHEMA and doc["claim"] == CLAIM and
         doc["release"] == {"path": RELEASE, **H.pin(release_raw)} and
         doc["entrypoints"] == release["entrypoints"][kind] and
         doc["external_profile"] == release["external_profile"] and
         doc["license_status"] == release["license_status"], "MANIFEST_SELECTION")
    selected, files = selected_paths(release, kind), doc["files"]
    need(type(files) is dict and set(files) == set(selected), "MANIFEST_CENSUS")
    maximum, total, _ = CAPS[kind]
    for name, pin in files.items():
        checked_pin(pin, maximum)
        expected = selected[name][2]
        need(expected is None or pin == expected, "MANIFEST_FIXED_PIN:"+name)
    need(sum(pin["bytes"] for pin in files.values()) <= total and
         files[RELEASE] == H.pin(release_raw), "MANIFEST_TOTAL_OR_RELEASE")
    for name, target in doc["entrypoints"].items():
        need(target in files or (name == "package" and target == "package" and
             any(path.startswith("package/") for path in files)), "ENTRYPOINT")
    return files


def verify(source_root, manifest_sha256, *, check=None):
    H = helper(); check = H.guard(check)
    root = H.ordinary(Path(source_root), directory=True)
    raw = H.read(root/MANIFEST, check)
    need(H.sha(raw) == H.hexid(manifest_sha256), "MANIFEST_PIN")
    release, release_raw = selection(root, check)
    doc = H.strict_json(raw)
    need(H.canonical(doc) == raw, "MANIFEST_CANONICAL")
    files = manifest_files(H, doc, release, release_raw)
    check_tree(root, dict(files, **{MANIFEST: H.pin(raw)}), check)
    need(H.read(root/MANIFEST, check) == raw and H.read(root/RELEASE, check) == release_raw,
         "VERIFICATION_INPUT_CHANGED")
    return {"status": "VERIFIED_EXACT_CURRENT_DISTRIBUTION", "kind": doc["kind"],
            "files": files, "manifest": H.pin(raw), "manifest_file": MANIFEST,
            "release_sha256": RELEASE_SHA, "source_root": str(root), "claim": CLAIM}


def pack(source_root, output, *, kind="source", package=None, check=None):
    H = helper(); check = H.guard(check)
    root = H.ordinary(Path(source_root), directory=True)
    output = H.ordinary(Path(output), directory=True, fresh=True)
    need(kind in CAPS and (package is None) == (kind == "source"), "PACK_KIND_ARGUMENTS")
    selected_package = H.ordinary(Path(package), directory=True) if package is not None else None
    need(not root.is_relative_to(output) and (selected_package is None or not
         (output.is_relative_to(selected_package) or selected_package.is_relative_to(output))),
         "OUTPUT_OVERLAP")
    release, release_raw = selection(root, check)
    selected = selected_paths(release, kind)
    maximum, total_bound, archive_bound = CAPS[kind]
    data, inputs = {}, {}
    for name, (origin, source, expected) in sorted(selected.items()):
        path = (root if origin == "source" else selected_package) / source
        need(not path.is_relative_to(output), "INPUT_OUTPUT_OVERLAP")
        raw = H.read(path, check, maximum if origin == "package" else 2*MIB)
        need(expected is None or H.pin(raw) == expected, "INPUT_PIN:"+name)
        data[name], inputs[name] = raw, path
        need(sum(map(len, data.values())) <= total_bound, "PAYLOAD_TOTAL")
    need(data[RELEASE] == release_raw and H.read(Path(__file__).absolute(), check) == data[UTILITY],
         "RUNNING_SOURCE_OR_RELEASE")
    if selected_package is not None:
        check_tree(selected_package, release["prebuilt"]["files"], check)
    doc = {"schema": SCHEMA, "kind": kind, "claim": CLAIM,
           "release": {"path": RELEASE, **H.pin(release_raw)},
           "files": {name: H.pin(raw) for name, raw in data.items()},
           "entrypoints": release["entrypoints"][kind],
           "external_profile": release["external_profile"], "license_status": release["license_status"]}
    files = manifest_files(H, doc, release, release_raw)
    manifest_raw = H.canonical(doc)
    need(len(manifest_raw) <= 2*MIB, "MANIFEST_BOUND")
    archive_data = dict(data, **{MANIFEST: manifest_raw})
    archive_files = {name: H.pin(raw) for name, raw in archive_data.items()}
    check(); output.mkdir()
    relocated = output/"relocated"
    archive_file = "source.zip" if kind == "source" else "package.zip"
    archive_path = output/archive_file
    with H.ordinary(archive_path, fresh=True).open("xb") as stream:
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED, allowZip64=False) as archive:
            for name, raw in sorted(archive_data.items()):
                check()
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_STORED
                archive.writestr(info, raw)
        stream.flush(); os.fsync(stream.fileno())
    archive_pin = inspect_archive(archive_path, archive_files, check, maximum=archive_bound)
    # Materialize the sole relocated tree from the actual inspected ZIP, not
    # the in-memory source dictionary. Each bounded member is checked again
    # before exclusive publication; the archive is rehashed at finalization.
    relocated.mkdir()
    with zipfile.ZipFile(H.ordinary(archive_path), "r") as archive:
        need([row.filename for row in archive.infolist()] == sorted(archive_files), "EXTRACTION_CENSUS")
        for name, expected in sorted(archive_files.items()):
            check(); H.relative(name)
            with archive.open(name, "r") as member:
                raw = member.read(expected["bytes"]+1)
            need(H.pin(raw) == expected, "EXTRACTION_PAYLOAD")
            target = relocated/name
            target.parent.mkdir(parents=True, exist_ok=True)
            H.ordinary(target.parent, directory=True)
            H.fresh_bytes(target, raw)
    check_tree(relocated, archive_files, check)
    for name, path in sorted(inputs.items()):
        need(H.read(path, check, maximum) == data[name], "SOURCE_CHANGED:"+name)
    need(H.read(Path(__file__).absolute(), check) == data[UTILITY], "RUNNING_SOURCE_CHANGED")
    if selected_package is not None:
        check_tree(selected_package, release["prebuilt"]["files"], check)
    check_tree(relocated, archive_files, check)
    need(H.pin(H.read(archive_path, check, archive_bound)) == archive_pin, "FINAL_ZIP_CHANGED")
    check()
    result = {"schema": "DMKN_ORDINARY_CURRENT_RELEASE_BUNDLE_RECEIPT_V1",
              "status": "PACKED_CURRENT_DISTRIBUTION_NOT_NEW_ACCEPTANCE", "kind": kind,
              "files": files, "archive": archive_pin, "archive_file": archive_file,
              "manifest": H.pin(manifest_raw), "manifest_file": MANIFEST,
              "release_sha256": RELEASE_SHA, "relocated": str(relocated),
              "payload_files": len(files), "archive_files": len(archive_files),
              "payload_bytes": sum(pin["bytes"] for pin in files.values()), "claim": CLAIM}
    H.fresh_bytes(output/"RECEIPT.json", H.canonical(result))
    return result


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON_PROFILE")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    subs = parser.add_subparsers(dest="action", required=True)
    packing = subs.add_parser("pack", allow_abbrev=False)
    packing.add_argument("--source-root", required=True)
    packing.add_argument("--kind", choices=tuple(CAPS), required=True)
    packing.add_argument("--package")
    packing.add_argument("--output", required=True)
    verifying = subs.add_parser("verify", allow_abbrev=False)
    verifying.add_argument("--source-root", required=True)
    verifying.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args()
    result = pack(args.source_root, args.output, kind=args.kind, package=args.package) if args.action == "pack" else \
        verify(args.source_root, args.manifest_sha256)
    print(json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()

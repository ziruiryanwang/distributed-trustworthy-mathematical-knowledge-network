"""Pack/verify the exact ordinary source workflow; no build, network or product import.

Only the approved original file-only bundle helper is executed, after exact-byte
and ordinary-path checks. Owner-controlled immutable inputs are a premise; hashes
are selection, not authenticity, licensing or source-execution approval.
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

PREFIX = "software/v5/ordinary_workflow_bundle/"
UTILITY = PREFIX + "bundle.py"
MANIFEST = "WORKFLOW-SOURCE-MANIFEST.json"
BASE_MANIFEST = "BASE-SOURCE-MANIFEST.json"
BASE_SHA256 = "f1beab01d43e4b5fc6d7b9999ff2795598e3f2ee77c0dc85f1d99e82a15b31f1"
HELPER = "software/v5/ordinary_release_bundle/bundle.py"
HELPER_SHA256 = "5a8742bec0c13f3c7e8104111ba883887d5569cbb1a5498d79567e998dcd4d32"
SCHEMA = "DMKN_ORDINARY_WORKFLOW_SOURCE_DISTRIBUTION_V1"
CLAIM = "EXACT_SOURCE_WORKFLOW_NOT_BUILD_OR_MATHEMATICAL_ACCEPTANCE"
COUNT = 154
# Archive destination -> canonical repository input. No recursive input discovery.
SOURCES = {
    "software/v5/ordinary_selected_export/export.py": "software/v5/ordinary_selected_export/export.py",
    "software/v5/ordinary_selected_export/selected_export.py": "software/v5/ordinary_selected_export/selected_export.py",
    "software/v5/ordinary_selected_export/README.md": PREFIX + "guides/SELECTED-EXPORT.md",
    "software/v5/ordinary_selected_export/INTAKE.md": "software/v5/ordinary_selected_export/INTAKE.md",
    "software/v5/ordinary_reuse_workflow/README.md": "software/v5/ordinary_reuse_workflow/README.md",
    "software/v5/UPDATE-AND-RECOVERY.md": PREFIX + "guides/UPDATE-AND-RECOVERY.md",
    "software/v5/ordinary_service_plan/service_plan.py": "software/v5/ordinary_service_plan/service_plan.py",
    "software/v5/ordinary_service_plan/README.md": PREFIX + "guides/SERVICE-PLAN.md",
    UTILITY: UTILITY,
    "START-HERE.md": PREFIX + "README.md",
}
UNCHANGED = {
    "software/v5/ordinary_selected_export/export.py": (19039, "79f61b6d1d52b1bb15130c866909ddbc61e3b1f643a91d3943a631e0fb4f6a05"),
    "software/v5/ordinary_selected_export/selected_export.py": (14944, "49ee6de8c6daa5fb7fd1a445ae7d4c9a1a0312b816697ae4ce6634b504a65eb2"),
    "software/v5/ordinary_selected_export/INTAKE.md": (7479, "b0d8e19e74fef6167afc7bf432535ea10caf21f8d134b77a4e90229d7ce8bb5e"),
    "software/v5/ordinary_reuse_workflow/README.md": (13371, "0558657ff9cfb32fd5c0ec4f76617a6b43e5a6ee7ad4d61953dfefd50879876a"),
    "software/v5/ordinary_service_plan/service_plan.py": (30967, "3245a5f50d694ef5ca9714c6408e9cfc93b1378606398c433cdda4a4e113ee01"),
}
ENTRYPOINTS = {
    "guide": "START-HERE.md", "verify": UTILITY,
    "build_guide": "software/v5/ordinary_release_bundle/README.md",
    "operator": "software/v5/ordinary_bounded_transport/prepare_selected.py",
    "export": "software/v5/ordinary_selected_export/export.py",
    "intake_guide": "software/v5/ordinary_selected_export/INTAKE.md",
    "reuse_guide": "software/v5/ordinary_reuse_workflow/README.md",
    "service": "software/v5/ordinary_service_plan/service_plan.py",
    "recovery_guide": "software/v5/UPDATE-AND-RECOVERY.md",
}


def require(ok, code):
    if not ok:
        raise ValueError("WORKFLOW_BUNDLE_" + code)


def bootstrap_path(value, *, directory=False):
    """Validate before executing any helper, including all path ancestors."""
    path = Path(value)
    require(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":" and
            path.drive[0].isalpha() and path != Path(path.anchor) and
            len(path.parts) <= 128 and len(str(path)) <= 32768 and
            not str(path).startswith(("\\\\", "//")), "BOOTSTRAP_PATH")
    for part in path.parts[1:]:
        require(part not in (".", "..") and not part.endswith((".", " ")) and
                not os.path.isreserved(part) and
                not any(ord(c) < 32 or c in ':*?"<>|\\' for c in part), "BOOTSTRAP_PART")
    for ancestor in (*reversed(path.parents), path):
        info = ancestor.lstat()
        require(not stat.S_ISLNK(info.st_mode) and
                not getattr(info, "st_file_attributes", 0) & 0x400, "BOOTSTRAP_REDIRECT")
        require(stat.S_ISDIR(info.st_mode) if ancestor != path or directory else
                stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "BOOTSTRAP_KIND")
    return path


def helper():
    here = bootstrap_path(Path(__file__).absolute())
    require(len(here.parents) > 3, "BOOTSTRAP_LAYOUT")
    path = bootstrap_path(here.parents[3] / HELPER)
    require(path.stat().st_size == 22041, "BOOTSTRAP_LENGTH")
    with path.open("rb") as stream:
        raw = stream.read(22042)
    require(len(raw) == 22041 and hashlib.sha256(raw).hexdigest() == HELPER_SHA256,
            "BOOTSTRAP_PIN")
    require(bootstrap_path(path).stat().st_size == 22041, "BOOTSTRAP_CHANGED")
    module = types.ModuleType("_approved_workflow_file_helpers")
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def base_files(base, raw, root, check):
    require(base.sha(raw) == BASE_SHA256, "BASE_MANIFEST_PIN")
    doc = base.strict_json(raw)
    files = base.validate_manifest(doc)
    require(base.canonical(doc) == raw, "BASE_CANONICAL")
    expected = base.known_pins(root, check)
    require(set(files) == set(expected) | base.NEW and
            all(files[name] == value for name, value in expected.items()), "BASE_SELECTION")
    return files


def validate_manifest(base, doc, original):
    require(type(doc) is dict and set(doc) == {"schema", "claim", "base_manifest",
            "files", "entrypoints", "external_profile", "license_status"}, "MANIFEST_FIELDS")
    require(doc["schema"] == SCHEMA and doc["claim"] == CLAIM and
            doc["base_manifest"] == {"path": BASE_MANIFEST, "sha256": BASE_SHA256} and
            doc["entrypoints"] == ENTRYPOINTS and doc["external_profile"] == base.EXTERNAL and
            doc["license_status"] == base.LICENSE, "MANIFEST_PROFILE")
    files = doc["files"]
    require(type(files) is dict and len(files) == COUNT and
            set(files) == set(original) | set(SOURCES) | {BASE_MANIFEST} and
            len({n.casefold() for n in files}) == COUNT and
            not set(original) & (set(SOURCES) | {BASE_MANIFEST, MANIFEST}), "EXACT_SELECTION")
    for name, value in files.items():
        base.relative(name); base.pin_shape(value)
        require(not any(p.as_posix() in files for p in PurePosixPath(name).parents), "PATH_ALIAS")
    require(all(files[name] == value for name, value in original.items()), "BASE_PROJECTION")
    require(all(files[name] == {"bytes": length, "sha256": digest}
                for name, (length, digest) in UNCHANGED.items()), "COMPANION_PIN")
    require(sum(value["bytes"] for value in files.values()) <= 8*base.MIB, "TOTAL_BOUND")
    return files


def verify(source_root, manifest_sha256, *, check=None):
    base = helper(); check = base.guard(check)
    root = base.ordinary(source_root, directory=True)
    raw = base.read(root/MANIFEST, check)
    require(base.sha(raw) == base.hexid(manifest_sha256), "MANIFEST_PIN")
    association = base.read(root/BASE_MANIFEST, check)
    original = base_files(base, association, root, check)
    doc = base.strict_json(raw)
    files = validate_manifest(base, doc, original)
    require(base.canonical(doc) == raw and files[BASE_MANIFEST] == base.pin(association),
            "MANIFEST_CANONICAL_OR_ASSOCIATION")
    base.census(root, set(files) | {MANIFEST}, check)
    for name, value in sorted(files.items()):
        require(base.pin(base.read(root/name, check)) == value, "PAYLOAD_PIN:" + name)
    require(base.read(root/MANIFEST, check) == raw, "MANIFEST_CHANGED")
    require(base.read(Path(__file__).absolute(), check) == base.read(root/UTILITY, check),
            "RUNNING_SOURCE")
    base.census(root, set(files) | {MANIFEST}, check); check()
    return {"status": "VERIFIED_EXACT_WORKFLOW_SOURCE_NOT_BUILT", "manifest": base.pin(raw),
            "payload_files": len(files), "payload_bytes": sum(p["bytes"] for p in files.values()),
            "base_manifest_sha256": BASE_SHA256, "claim": CLAIM}


def pack(source_root, base_manifest, output, *, check=None):
    base = helper(); check = base.guard(check)
    root = base.ordinary(source_root, directory=True)
    selected_base = base.ordinary(base_manifest)
    output = base.ordinary(output, directory=True, fresh=True)
    association = base.read(selected_base, check)
    original = base_files(base, association, root, check)
    mapping = {name: name for name in original} | SOURCES
    require(not root.is_relative_to(output) and not selected_base.is_relative_to(output) and
            all(not (root/name).is_relative_to(output) for name in mapping.values()), "OUTPUT_OVERLAP")
    data = {}
    for destination, source in sorted(mapping.items()):
        base.relative(destination); base.relative(source)
        data[destination] = base.read(root/source, check)
    data[BASE_MANIFEST] = association
    require(base.read(Path(__file__).absolute(), check) == data[UTILITY], "RUNNING_SOURCE")
    doc = {"schema": SCHEMA, "claim": CLAIM,
           "base_manifest": {"path": BASE_MANIFEST, "sha256": BASE_SHA256},
           "files": {name: base.pin(raw) for name, raw in data.items()},
           "entrypoints": ENTRYPOINTS, "external_profile": base.EXTERNAL, "license_status": base.LICENSE}
    validate_manifest(base, doc, original)
    manifest_raw = base.canonical(doc)
    require(len(manifest_raw) <= 2*base.MIB, "MANIFEST_BOUND")
    payload_bytes = sum(len(raw) for raw in data.values())
    data[MANIFEST] = manifest_raw
    check(); base.ordinary(output, directory=True, fresh=True).mkdir()
    archive_path = output/"source.zip"
    with base.ordinary(archive_path, fresh=True).open("xb") as stream:
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED, allowZip64=False) as archive:
            for name, raw in sorted(data.items()):
                check()
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3; info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_STORED
                archive.writestr(info, raw)
        stream.flush(); os.fsync(stream.fileno())
    archive_raw = base.read(archive_path, check, 16*base.MIB)
    with zipfile.ZipFile(base.ordinary(archive_path), "r") as archive:
        rows = archive.infolist()
        require(archive.comment == b"" and [r.filename for r in rows] == sorted(data), "ZIP_CENSUS")
        for row in rows:
            check(); base.relative(row.filename)
            require(row.date_time == (1980, 1, 1, 0, 0, 0) and row.create_system == 3 and
                    row.external_attr == 0o100644 << 16 and row.compress_type == zipfile.ZIP_STORED and
                    row.extra == row.comment == b"" and row.flag_bits == 0 and
                    row.file_size == row.compress_size == len(data[row.filename]), "ZIP_METADATA")
            require(archive.read(row) == data[row.filename], "ZIP_PAYLOAD")
    for destination, source in sorted(mapping.items()):
        require(base.read(root/source, check) == data[destination], "SOURCE_CHANGED:" + source)
    require(base.read(selected_base, check) == association and
            base.read(Path(__file__).absolute(), check) == data[UTILITY], "SELECTION_CHANGED")
    require(base.read(archive_path, check, 16*base.MIB) == archive_raw, "ZIP_CHANGED")
    check()
    receipt = {"schema": "DMKN_ORDINARY_WORKFLOW_SOURCE_BUNDLE_RECEIPT_V1",
               "status": "PACKED_WORKFLOW_SOURCE_NOT_BUILT", "manifest": base.pin(manifest_raw),
               "archive": base.pin(archive_raw), "payload_files": COUNT, "archive_files": COUNT+1,
               "payload_bytes": payload_bytes, "base_manifest_sha256": BASE_SHA256,
               "source_root": str(root), "output": str(output), "claim": CLAIM}
    base.fresh_bytes(output/"RECEIPT.json", base.canonical(receipt))
    return receipt


def main():
    require(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
            sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON_PROFILE")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    commands = parser.add_subparsers(dest="action", required=True)
    packing = commands.add_parser("pack", allow_abbrev=False)
    packing.add_argument("--source-root", required=True)
    packing.add_argument("--base-manifest", required=True)
    packing.add_argument("--output", required=True)
    verifying = commands.add_parser("verify", allow_abbrev=False)
    verifying.add_argument("--source-root", required=True)
    verifying.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args()
    result = pack(args.source_root, args.base_manifest, args.output) if args.action == "pack" else \
        verify(args.source_root, args.manifest_sha256)
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

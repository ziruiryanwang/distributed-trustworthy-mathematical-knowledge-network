"""Pack/verify the bounded exact-module investigator source distribution.

Only two byte-approved file-only helpers are executed. No product import,
compiler, network, owner state, deletion or overwrite. Independently approved
source and immutable owner-controlled inputs remain premises; hashes alone
are not execution approval, authentication, a license or mathematical evidence.
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

PREFIX = "software/v5/ordinary_investigator_bundle/"
UTILITY = PREFIX + "bundle.py"
MANIFEST = "INVESTIGATOR-SOURCE-MANIFEST.json"
PRIOR_MANIFEST = "PRIOR-WORKFLOW-SOURCE-MANIFEST.json"
PRIOR_SHA256 = "1c9a8b381b614a05ddf2c5b96e12c8adc07bf0eb473ab238af6ef9ba71f76417"
HELPER = "software/v5/ordinary_workflow_bundle/bundle.py"
HELPER_SHA256 = "ceae62463c13dccd3a58faea0b8548d1454e09de3877b8058303dd51619b10c7"
SCHEMA = "DMKN_ORDINARY_INVESTIGATOR_SOURCE_DISTRIBUTION_V1"
CLAIM = "EXACT_INVESTIGATOR_SOURCE_NOT_BUILD_OR_MATHEMATICAL_ACCEPTANCE"
COUNT = 169
# Archive destination -> repository input. The 154 old payloads are read directly
# from the separately selected exact workflow extraction, never remapped/edited.
SOURCES = {
    UTILITY: UTILITY,
    "README.md": PREFIX + "README.md",
    PREFIX + "prepare_selected.py": PREFIX + "prepare_selected.py",
    PREFIX + "compatibility.json": PREFIX + "compatibility.json",
    PREFIX + "guides/BUILD-MODULE.md": PREFIX + "guides/BUILD-MODULE.md",
    PREFIX + "guides/QUESTIONS.md": PREFIX + "guides/QUESTIONS.md",
    PREFIX + "guides/CONTINUE.md": PREFIX + "guides/CONTINUE.md",
    "software/v5/ordinary_exact_module/assemble.py": "software/v5/ordinary_exact_module/assemble.py",
    "software/v5/ordinary_exact_module/OrdinaryModule.lean": "software/v5/ordinary_exact_module/OrdinaryModule.lean",
    "software/v5/ordinary_exact_module/module_export.py": "software/v5/ordinary_exact_module/module_export.py",
    "software/v5/ordinary_exact_module/anchor_store.py": "software/v5/ordinary_exact_module/anchor_store.py",
    "software/v5/ordinary_exact_module/OVERLAY.json": "software/v5/ordinary_exact_module/OVERLAY.json",
    "software/v5/ordinary_basis_query/query.py": "software/v5/ordinary_basis_query/query.py",
    "software/v5/ordinary_anchor_query/query.py": "software/v5/ordinary_anchor_query/query.py",
}
FIXED = {
    "software/v5/ordinary_exact_module/assemble.py": (12326, "f7d5f3496d010c591a4de3872f47ff169c30413354c2576bf670b7b30c77a82b"),
    "software/v5/ordinary_exact_module/OrdinaryModule.lean": (48835, "54f36991e4707b487a21f237e0854f6bd4127c2c2da805440c6119abf7cfd3d5"),
    "software/v5/ordinary_exact_module/module_export.py": (23050, "5a2250a564188838922f0d990935313076d5bd5c0fee153a7b7375c5e8e3b581"),
    "software/v5/ordinary_exact_module/anchor_store.py": (45094, "97b93bed9dabcdea00933da5a46d3655e588f496a797837cfc1a2445f7549cf5"),
    "software/v5/ordinary_exact_module/OVERLAY.json": (429, "1f26c65c48789cb891beda7a15deae9a2609611d93185960b589c3f2fd02315b"),
    "software/v5/ordinary_basis_query/query.py": (23406, "a3d0e7d4ec7da30296c0349a67d63d90d1fc611e22e2b4cfb69e7a6ff5a8a68a"),
    "software/v5/ordinary_anchor_query/query.py": (34937, "52c48ed1da4d0f4955d88eb54b00df7475ec5f7bf4ae85497907b247adb261a1"),
    PREFIX + "prepare_selected.py": (5945, "72f27b6644f998a16b5fb3eb785d576a68d48338949b135cc4e96c18b8b89afc"),
    PREFIX + "compatibility.json": (10728, "de4937bdcac4d9ed5550d4da9c59d4f4af4551275dcaaf9d36bc85affbddd1f0"),
}
ENTRYPOINTS = {
    "guide": "README.md", "verify": UTILITY,
    "build_module_guide": PREFIX + "guides/BUILD-MODULE.md",
    "questions_guide": PREFIX + "guides/QUESTIONS.md",
    "continuation_guide": PREFIX + "guides/CONTINUE.md",
    "exact_overlay": "software/v5/ordinary_exact_module/assemble.py",
    "operator": PREFIX + "prepare_selected.py",
    "basis_query": "software/v5/ordinary_basis_query/query.py",
    "anchor_query": "software/v5/ordinary_anchor_query/query.py",
}


def require(ok, code):
    if not ok:
        raise ValueError("INVESTIGATOR_BUNDLE_" + code)


def bootstrap_path(value, *, directory=False):
    """Validate the script/helper and every ancestor before executing helpers."""
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


def helpers():
    here = bootstrap_path(Path(__file__).absolute())
    require(len(here.parents) > 3, "BOOTSTRAP_LAYOUT")
    path = bootstrap_path(here.parents[3]/HELPER)
    require(path.stat().st_size == 13182, "BOOTSTRAP_LENGTH")
    with path.open("rb") as stream:
        raw = stream.read(13183)
    require(len(raw) == 13182 and hashlib.sha256(raw).hexdigest() == HELPER_SHA256,
            "BOOTSTRAP_PIN")
    require(bootstrap_path(path).stat().st_size == 13182, "BOOTSTRAP_CHANGED")
    workflow = types.ModuleType("_approved_investigator_file_helpers")
    workflow.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), workflow.__dict__)
    # Its helper independently ordinary-path/byte-checks the approved release
    # bundle helper before executing it; neither imports product/native code.
    return workflow, workflow.helper()


def prior_files(workflow, base, raw, root, check):
    require(base.sha(raw) == PRIOR_SHA256, "PRIOR_MANIFEST_PIN")
    association = base.read(root/workflow.BASE_MANIFEST, check)
    original = workflow.base_files(base, association, root, check)
    doc = base.strict_json(raw)
    files = workflow.validate_manifest(base, doc, original)
    require(base.canonical(doc) == raw and
            files[workflow.BASE_MANIFEST] == base.pin(association), "PRIOR_ASSOCIATION")
    return files


def validate_manifest(base, doc, original, prior_raw):
    require(type(doc) is dict and set(doc) == {"schema", "claim", "prior_manifest",
            "files", "entrypoints", "external_profile", "license_status"}, "MANIFEST_FIELDS")
    require(doc["schema"] == SCHEMA and doc["claim"] == CLAIM and
            doc["prior_manifest"] == {"path": PRIOR_MANIFEST, "sha256": PRIOR_SHA256} and
            doc["entrypoints"] == ENTRYPOINTS and doc["external_profile"] == base.EXTERNAL and
            doc["license_status"] == base.LICENSE, "MANIFEST_PROFILE")
    files = doc["files"]
    require(type(files) is dict and len(files) == COUNT and
            set(files) == set(original) | set(SOURCES) | {PRIOR_MANIFEST} and
            len({n.casefold() for n in files}) == COUNT and
            not set(original) & (set(SOURCES) | {PRIOR_MANIFEST, MANIFEST}), "EXACT_SELECTION")
    for name, value in files.items():
        base.relative(name); base.pin_shape(value)
        require(not any(p.as_posix() in files for p in PurePosixPath(name).parents), "PATH_ALIAS")
    require(all(files[name] == value for name, value in original.items()), "PRIOR_PROJECTION")
    require(files[PRIOR_MANIFEST] == base.pin(prior_raw), "PRIOR_ASSOCIATION")
    require(all(files[name] == {"bytes": length, "sha256": digest}
                for name, (length, digest) in FIXED.items()), "ADDITION_PIN")
    require(sum(value["bytes"] for value in files.values()) <= 8*base.MIB, "TOTAL_BOUND")
    directories = {p.as_posix() for name in files for p in PurePosixPath(name).parents
                   if p.as_posix() != "."}
    require(len(files) + 1 + len(directories) <= 256, "CENSUS_SELECTION_BOUND")
    return files


def verify(source_root, manifest_sha256, *, check=None):
    workflow, base = helpers(); check = base.guard(check)
    root = base.ordinary(source_root, directory=True)
    raw = base.read(root/MANIFEST, check)
    require(base.sha(raw) == base.hexid(manifest_sha256), "MANIFEST_PIN")
    prior_raw = base.read(root/PRIOR_MANIFEST, check)
    original = prior_files(workflow, base, prior_raw, root, check)
    doc = base.strict_json(raw)
    files = validate_manifest(base, doc, original, prior_raw)
    require(base.canonical(doc) == raw, "MANIFEST_CANONICAL")
    base.census(root, set(files) | {MANIFEST}, check)
    for name, value in sorted(files.items()):
        require(base.pin(base.read(root/name, check)) == value, "PAYLOAD_PIN:" + name)
    require(base.read(root/MANIFEST, check) == raw, "MANIFEST_CHANGED")
    require(base.read(Path(__file__).absolute(), check) == base.read(root/UTILITY, check),
            "RUNNING_SOURCE")
    base.census(root, set(files) | {MANIFEST}, check); check()
    return {"status": "VERIFIED_EXACT_INVESTIGATOR_SOURCE_NOT_BUILT", "manifest": base.pin(raw),
            "payload_files": len(files), "payload_bytes": sum(p["bytes"] for p in files.values()),
            "prior_manifest_sha256": PRIOR_SHA256, "claim": CLAIM}


def pack(source_root, workflow_root, output, *, check=None):
    workflow, base = helpers(); check = base.guard(check)
    root = base.ordinary(source_root, directory=True)
    prior_root = base.ordinary(workflow_root, directory=True)
    output = base.ordinary(output, directory=True, fresh=True)
    require(not root.is_relative_to(output) and not prior_root.is_relative_to(output) and
            not output.is_relative_to(prior_root), "OUTPUT_OVERLAP")
    prior_raw = base.read(prior_root/workflow.MANIFEST, check)
    original = prior_files(workflow, base, prior_raw, prior_root, check)
    base.census(prior_root, set(original) | {workflow.MANIFEST}, check)
    require(all(not (root/name).is_relative_to(output) for name in SOURCES.values()), "INPUT_OUTPUT_OVERLAP")
    data = {}
    for name, value in sorted(original.items()):
        raw = base.read(prior_root/name, check)
        require(base.pin(raw) == value, "PRIOR_PAYLOAD_PIN:" + name)
        data[name] = raw
    for destination, source in sorted(SOURCES.items()):
        base.relative(destination); base.relative(source)
        require(destination not in data, "ADDITION_OVERLAP")
        data[destination] = base.read(root/source, check)
    data[PRIOR_MANIFEST] = prior_raw
    require(base.read(Path(__file__).absolute(), check) == data[UTILITY], "RUNNING_SOURCE")
    doc = {"schema": SCHEMA, "claim": CLAIM,
           "prior_manifest": {"path": PRIOR_MANIFEST, "sha256": PRIOR_SHA256},
           "files": {name: base.pin(raw) for name, raw in data.items()},
           "entrypoints": ENTRYPOINTS, "external_profile": base.EXTERNAL, "license_status": base.LICENSE}
    validate_manifest(base, doc, original, prior_raw)
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
    for name in sorted(original):
        require(base.read(prior_root/name, check) == data[name], "PRIOR_SOURCE_CHANGED:" + name)
    for destination, source in sorted(SOURCES.items()):
        require(base.read(root/source, check) == data[destination], "SOURCE_CHANGED:" + source)
    require(base.read(prior_root/workflow.MANIFEST, check) == prior_raw and
            base.read(Path(__file__).absolute(), check) == data[UTILITY], "SELECTION_CHANGED")
    base.census(prior_root, set(original) | {workflow.MANIFEST}, check)
    require(base.read(archive_path, check, 16*base.MIB) == archive_raw, "ZIP_CHANGED")
    check()
    receipt = {"schema": "DMKN_ORDINARY_INVESTIGATOR_SOURCE_BUNDLE_RECEIPT_V1",
               "status": "PACKED_INVESTIGATOR_SOURCE_NOT_BUILT", "manifest": base.pin(manifest_raw),
               "archive": base.pin(archive_raw), "payload_files": COUNT, "archive_files": COUNT+1,
               "payload_bytes": payload_bytes, "prior_manifest_sha256": PRIOR_SHA256,
               "source_root": str(root), "workflow_root": str(prior_root), "output": str(output), "claim": CLAIM}
    base.fresh_bytes(output/"RECEIPT.json", base.canonical(receipt))
    return receipt


def main():
    require(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
            sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON_PROFILE")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    commands = parser.add_subparsers(dest="action", required=True)
    packing = commands.add_parser("pack", allow_abbrev=False)
    packing.add_argument("--source-root", required=True)
    packing.add_argument("--workflow-root", required=True)
    packing.add_argument("--output", required=True)
    verifying = commands.add_parser("verify", allow_abbrev=False)
    verifying.add_argument("--source-root", required=True)
    verifying.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args()
    result = pack(args.source_root, args.workflow_root, args.output) if args.action == "pack" else \
        verify(args.source_root, args.manifest_sha256)
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

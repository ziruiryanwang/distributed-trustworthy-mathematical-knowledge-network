"""Pack/verify one bounded commons source handoff, without product imports.

One byte-approved file-only helper is executed. No compiler, native artifact,
owner state, network, deletion or overwrite. Independent software approval and
protected immutable inputs remain premises; hashes are not a security sandbox.
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

PREFIX = "software/v5/ordinary_commons_bundle/"
UTILITY = PREFIX + "bundle.py"
MANIFEST = "COMMONS-SOURCE-MANIFEST.json"
PRIOR_MANIFEST = "INVESTIGATOR-SOURCE-MANIFEST.json"
PRIOR_SHA256 = "65edf28f928d4100346a4603fe508252ddc6393950c34a373fbb33da4c6491f5"
HISTORICAL_README = "HISTORICAL-INVESTIGATOR-README.md"
HELPER = "software/v5/ordinary_release_bundle/bundle.py"
HELPER_SHA256 = "5a8742bec0c13f3c7e8104111ba883887d5569cbb1a5498d79567e998dcd4d32"
SCHEMA = "DMKN_ORDINARY_COMMONS_SOURCE_DISTRIBUTION_V1"
CLAIM = "EXACT_COMMONS_SOURCE_NOT_BUILD_OR_MATHEMATICAL_ACCEPTANCE"
COUNT = 186
SOURCES = {
    UTILITY: UTILITY,
    "README.md": PREFIX + "README.md",
    "software/v5/ordinary_inert_mirror02/README.md": PREFIX + "MIRROR.md",
    "software/v5/METHOD-DISCOVERY.md": PREFIX + "METHOD-DISCOVERY.md",
    **{("software/v5/" + folder + "/" + name): ("software/v5/" + folder + "/" + name)
       for folder, names in (
           ("ordinary_inert_mirror02", ("run.py", "mirror.py", "SOURCES.json")),
           ("ordinary_multi_source", ("http_provider.py", "ordinary_acquisition.py", "peer_api.py")),
           ("ordinary_multi_source_package", ("assemble.py", "README.md", "prepare.py",
                                              "prepare_selected.py", "compatibility.json", "OVERLAY.json")))
       for name in names},
}
FIXED = {
    "software/v5/ordinary_inert_mirror02/run.py": (23456, "cef9b50b8a98231e7f9e60afb0f9021b7d5f495266b2320957076ab4e1c55bd0"),
    "software/v5/ordinary_inert_mirror02/mirror.py": (26820, "86d0716d51f55040233bf2572c74bfdd7307a203a241ef2815c74f7958458920"),
    "software/v5/ordinary_inert_mirror02/SOURCES.json": (6303, "1bc43d4c9896476443d0d6aab95015db7af32bc46a04cfb1624a5c40e638feb9"),
    "software/v5/ordinary_multi_source/http_provider.py": (31361, "d9c342d1dcb5ee3e4b293e8dc0566397a321cc59a6f545e2f2afde452c760251"),
    "software/v5/ordinary_multi_source/ordinary_acquisition.py": (30121, "076130f7a34b505df33ee550501d1c4276bb46e408ff226df765225933a0658e"),
    "software/v5/ordinary_multi_source/peer_api.py": (68115, "dcaea5226f58e4254dd4cff0d6c621cf593aabe9b4d511d127194816c8ddc0ef"),
    "software/v5/ordinary_multi_source_package/assemble.py": (12445, "7ec9032943524953b2e3b57538f34d39844d5c081edd5a5960f6e5c40a552f16"),
    "software/v5/ordinary_multi_source_package/README.md": (14675, "b9e8b36c0208714e5fdcbd44071d5373d47cc3af6bc6b60a6c71a95616297c53"),
    "software/v5/ordinary_multi_source_package/prepare.py": (34599, "77f0bc5c6d02e1a87c29e44d71cbb77de4f1655998b980c9b71eb14085afb2b0"),
    "software/v5/ordinary_multi_source_package/prepare_selected.py": (5913, "f0acfe0e718f14ce902c8b97db1508c952931ef3c54edaca5732f3e8309ae00c"),
    "software/v5/ordinary_multi_source_package/compatibility.json": (10728, "e3357c5f51819b3086149226d16c887e708324bbfa6774d7b744246d920b0bc1"),
    "software/v5/ordinary_multi_source_package/OVERLAY.json": (525, "8506361cf583328edc15f1cff28b1e5325f5156f82fe6a75bac170d58d6b3049"),
}
ENTRYPOINTS = {
    "guide": "README.md", "verify": UTILITY,
    "build_module_guide": "software/v5/ordinary_investigator_bundle/guides/BUILD-MODULE.md",
    "questions_guide": "software/v5/ordinary_investigator_bundle/guides/QUESTIONS.md",
    "continuation_guide": "software/v5/ordinary_investigator_bundle/guides/CONTINUE.md",
    "methods_guide": "software/v5/METHOD-DISCOVERY.md",
    "multi_source_guide": "software/v5/ordinary_multi_source_package/README.md",
    "multi_source_overlay": "software/v5/ordinary_multi_source_package/assemble.py",
    "operator": "software/v5/ordinary_multi_source_package/prepare_selected.py",
    "exact_overlay": "software/v5/ordinary_exact_module/assemble.py",
    "basis_query": "software/v5/ordinary_basis_query/query.py",
    "anchor_query": "software/v5/ordinary_anchor_query/query.py",
    "mirror": "software/v5/ordinary_inert_mirror02/run.py",
    "mirror_guide": "software/v5/ordinary_inert_mirror02/README.md",
}


def require(ok, code):
    if not ok:
        raise ValueError("COMMONS_BUNDLE_" + code)


def bootstrap_path(value, *, directory=False):
    """Check the utility/helper and ancestors before executing the helper."""
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
    require(path.stat().st_size == 22041, "BOOTSTRAP_LENGTH")
    with path.open("rb") as stream:
        raw = stream.read(22042)
    require(len(raw) == 22041 and hashlib.sha256(raw).hexdigest() == HELPER_SHA256,
            "BOOTSTRAP_PIN")
    require(bootstrap_path(path).stat().st_size == 22041, "BOOTSTRAP_CHANGED")
    base = types.ModuleType("_approved_commons_file_helpers")
    base.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), base.__dict__)
    return base


def project(name):
    return HISTORICAL_README if name == "README.md" else name


def prior_files(base, raw):
    require(len(raw) == 25231 and base.sha(raw) == PRIOR_SHA256, "PRIOR_MANIFEST_PIN")
    doc = base.strict_json(raw)
    require(type(doc) is dict and set(doc) == {"schema", "claim", "prior_manifest", "files",
            "entrypoints", "external_profile", "license_status"} and
            doc["schema"] == "DMKN_ORDINARY_INVESTIGATOR_SOURCE_DISTRIBUTION_V1" and
            base.canonical(doc) == raw, "PRIOR_MANIFEST_SHAPE")
    files = doc["files"]
    require(type(files) is dict and len(files) == 169 and "README.md" in files and
            len({n.casefold() for n in files}) == 169, "PRIOR_SELECTION")
    for name, pin in files.items():
        base.relative(name); base.pin_shape(pin)
        require(not any(p.as_posix() in files for p in PurePosixPath(name).parents), "PRIOR_ALIAS")
    return files


def validate_manifest(base, doc, original, prior_raw):
    require(type(doc) is dict and set(doc) == {"schema", "claim", "prior_manifest", "files",
            "entrypoints", "external_profile", "license_status"}, "MANIFEST_FIELDS")
    require(doc["schema"] == SCHEMA and doc["claim"] == CLAIM and
            doc["prior_manifest"] == {"path": PRIOR_MANIFEST, "sha256": PRIOR_SHA256,
                                      "path_projection": {"README.md": HISTORICAL_README}} and
            doc["entrypoints"] == ENTRYPOINTS and doc["external_profile"] == base.EXTERNAL and
            doc["license_status"] == base.LICENSE, "MANIFEST_PROFILE")
    projected = {project(name): pin for name, pin in original.items()}
    files = doc["files"]
    require(len(projected) == 169 and not set(projected) & (set(SOURCES) | {PRIOR_MANIFEST, MANIFEST}),
            "PROJECTION_OVERLAP")
    require(type(files) is dict and len(files) == COUNT and
            set(files) == set(projected) | set(SOURCES) | {PRIOR_MANIFEST} and
            len({n.casefold() for n in files}) == COUNT, "EXACT_SELECTION")
    for name, pin in files.items():
        base.relative(name); base.pin_shape(pin)
        require(not any(p.as_posix() in files for p in PurePosixPath(name).parents), "PATH_ALIAS")
    require(all(files[name] == pin for name, pin in projected.items()), "PRIOR_PROJECTION")
    require(files[PRIOR_MANIFEST] == base.pin(prior_raw), "PRIOR_ASSOCIATION")
    require(all(files[name] == {"bytes": size, "sha256": digest}
                for name, (size, digest) in FIXED.items()), "ADDITION_PIN")
    require(set(ENTRYPOINTS.values()) <= set(files), "ENTRYPOINT_SELECTION")
    require(sum(pin["bytes"] for pin in files.values()) <= 8*base.MIB, "TOTAL_BOUND")
    directories = {p.as_posix() for name in files for p in PurePosixPath(name).parents
                   if p.as_posix() != "."}
    require(len(files) + 1 + len(directories) <= 256, "CENSUS_SELECTION_BOUND")
    return files


def verify(source_root, manifest_sha256, *, check=None):
    base = helpers(); check = base.guard(check)
    root = base.ordinary(source_root, directory=True)
    raw = base.read(root/MANIFEST, check)
    require(base.sha(raw) == base.hexid(manifest_sha256), "MANIFEST_PIN")
    prior_raw = base.read(root/PRIOR_MANIFEST, check)
    original = prior_files(base, prior_raw)
    doc = base.strict_json(raw)
    files = validate_manifest(base, doc, original, prior_raw)
    require(base.canonical(doc) == raw, "MANIFEST_CANONICAL")
    base.census(root, set(files) | {MANIFEST}, check)
    for name, pin in sorted(files.items()):
        require(base.pin(base.read(root/name, check)) == pin, "PAYLOAD_PIN:" + name)
    require(base.read(root/MANIFEST, check) == raw, "MANIFEST_CHANGED")
    require(base.read(Path(__file__).absolute(), check) == base.read(root/UTILITY, check), "RUNNING_SOURCE")
    base.census(root, set(files) | {MANIFEST}, check); check()
    return {"status": "VERIFIED_EXACT_COMMONS_SOURCE_NOT_BUILT", "manifest": base.pin(raw),
            "payload_files": len(files), "payload_bytes": sum(p["bytes"] for p in files.values()),
            "prior_manifest_sha256": PRIOR_SHA256, "claim": CLAIM}


def pack(source_root, investigator_root, output, *, check=None):
    base = helpers(); check = base.guard(check)
    root = base.ordinary(source_root, directory=True)
    prior_root = base.ordinary(investigator_root, directory=True)
    output = base.ordinary(output, directory=True, fresh=True)
    require(not root.is_relative_to(output) and not prior_root.is_relative_to(output) and
            not output.is_relative_to(prior_root) and not output.is_relative_to(root/PREFIX),
            "OUTPUT_OVERLAP")
    require(all(not (root/name).is_relative_to(output) for name in SOURCES.values()), "INPUT_OUTPUT_OVERLAP")
    prior_raw = base.read(prior_root/PRIOR_MANIFEST, check)
    original = prior_files(base, prior_raw)
    base.census(prior_root, set(original) | {PRIOR_MANIFEST}, check)
    data = {}
    for name, pin in sorted(original.items()):
        raw = base.read(prior_root/name, check)
        require(base.pin(raw) == pin, "PRIOR_PAYLOAD_PIN:" + name)
        data[project(name)] = raw
    for destination, source in sorted(SOURCES.items()):
        base.relative(destination); base.relative(source)
        require(destination not in data, "ADDITION_OVERLAP")
        data[destination] = base.read(root/source, check)
    data[PRIOR_MANIFEST] = prior_raw
    require(base.read(Path(__file__).absolute(), check) == data[UTILITY], "RUNNING_SOURCE")
    doc = {"schema": SCHEMA, "claim": CLAIM,
           "prior_manifest": {"path": PRIOR_MANIFEST, "sha256": PRIOR_SHA256,
                              "path_projection": {"README.md": HISTORICAL_README}},
           "files": {name: base.pin(raw) for name, raw in data.items()}, "entrypoints": ENTRYPOINTS,
           "external_profile": base.EXTERNAL, "license_status": base.LICENSE}
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
        require(base.read(prior_root/name, check) == data[project(name)], "PRIOR_SOURCE_CHANGED:" + name)
    for destination, source in sorted(SOURCES.items()):
        require(base.read(root/source, check) == data[destination], "SOURCE_CHANGED:" + source)
    require(base.read(prior_root/PRIOR_MANIFEST, check) == prior_raw and
            base.read(Path(__file__).absolute(), check) == data[UTILITY], "SELECTION_CHANGED")
    base.census(prior_root, set(original) | {PRIOR_MANIFEST}, check)
    require(base.read(archive_path, check, 16*base.MIB) == archive_raw, "ZIP_CHANGED")
    check()
    receipt = {"schema": "DMKN_ORDINARY_COMMONS_SOURCE_BUNDLE_RECEIPT_V1",
               "status": "PACKED_COMMONS_SOURCE_NOT_BUILT", "manifest": base.pin(manifest_raw),
               "archive": base.pin(archive_raw), "payload_files": COUNT, "archive_files": COUNT+1,
               "payload_bytes": payload_bytes, "prior_manifest_sha256": PRIOR_SHA256,
               "source_root": str(root), "investigator_root": str(prior_root), "output": str(output), "claim": CLAIM}
    base.fresh_bytes(output/"RECEIPT.json", base.canonical(receipt))
    return receipt


def main():
    require(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
            sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON_PROFILE")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    commands = parser.add_subparsers(dest="action", required=True)
    packing = commands.add_parser("pack", allow_abbrev=False)
    packing.add_argument("--source-root", required=True)
    packing.add_argument("--investigator-root", required=True)
    packing.add_argument("--output", required=True)
    verifying = commands.add_parser("verify", allow_abbrev=False)
    verifying.add_argument("--source-root", required=True)
    verifying.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args()
    result = pack(args.source_root, args.investigator_root, args.output) if args.action == "pack" else \
        verify(args.source_root, args.manifest_sha256)
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

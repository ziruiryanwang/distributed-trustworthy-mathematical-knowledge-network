"""Create/verify one bounded, offline, exact ordinary-commons source handoff.

No product import, compiler, state, network, runtime copy, overwrite or deletion.
Owner-approved immutable files and an independently selected utility/hash are
premises. File identity is not authenticity, a license or a security sandbox.
Use an outer Job if hard containment beyond cooperative 60 wall/30 CPU is needed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import time
import zipfile

MIB = 1024**2
MAP = "software/v5/ordinary_bounded_operations/source-map.json"
PREFIX = "software/v5/ordinary_source_bundle/"
MANIFEST = "SOURCE-MANIFEST.json"
CLAIM = "EXACT_SOURCE_INPUTS_NOT_BUILD_OR_MATHEMATICAL_ACCEPTANCE"
ENTRYPOINTS = {
    "build": "software/v5/ordinary_bounded_operations/build.py",
    "overlay": "software/v5/ordinary_fair_search/assemble.py",
    "operator": "software/v5/ordinary_operator_kit/prepare_selected.py",
}
EXTERNAL = {"os": "Windows x86-64", "python": "3.14.6", "lean": "4.34.0"}
LICENSE = "UNDECIDED_NO_PUBLIC_RELEASE_AUTHORIZATION"
NEW = {PREFIX + name for name in ("bundle.py", "README.md", "LICENSE-STATUS.md")}
# Existing reviewed bytes, not a source search/glob or approval of arbitrary code.
FIXED = {
    MAP: (34049, "e9b7a873c8e509651833de51e5bd6beda130c74fdf7391859a8661c08426396a"),
    "software/v5/ordinary_bounded_operations/build.py": (29162, "79a056932d5720e9ab964ee50a01d1b04569a60a5e6445df0070a2b6556b42f9"),
    "software/v5/ordinary_fair_search/assemble.py": (18374, "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"),
    "software/v5/ordinary_fair_search/profile.py": (13451, "828031e82f3dd43865d189587affa61dd6f8abe5b8667d45da0673949a069743"),
    "software/v5/ordinary_fair_search/peer_api.py": (43706, "06663bcda04345cb9ea38ca422d7545b5736a208c2d79742bebc095f5409b7e5"),
    "software/v5/ordinary_fair_search/fair_exchange.py": (5504, "3fe626b2dc4e63c345e54a517b1b37eea6eedada6d0fbb497aa18745a93eb828"),
    "software/v5/ordinary_fair_search/fair_search.py": (12594, "2567fcb2308c7e477c08b958a3661348eee682c5a98ce2389dd9add02d48e652"),
    "software/v5/ordinary_fair_search/README.md": (7098, "c3d8642b6fe9ece1b12c3a313910d14c52442b78a94c8af1b44dbe0901115aa5"),
    "software/v5/ordinary_operator_kit/prepare.py": (28501, "a843efb7a5b2518469260e5d5acedad530068147cf86851c867c75d9e22e855e"),
    "software/v5/ordinary_operator_kit/prepare_selected.py": (5549, "9a2436210a869d815ec3c353250345424d540c6f1b4e765a20c4f8af86bcc6cc"),
    "software/v5/ordinary_operator_kit/compatibility.json": (10697, "b5a812c90a8edc930a3a1b2859a7f77e5799772a516e1478bb04ae7add7abfe2"),
    "software/v5/ordinary_operator_kit/examples.json": (5509, "c585172795401aca25a7fabaf9173dcd9ee38f1cdceeed129d13e2e9b6742b3a"),
    "software/v5/ordinary_operator_kit/START-HERE.md": (16487, "3af7eea96011a18642eb5d3039b47284b2d6dbbcee6c912a821c8e72c654947c"),
    "software/v5/ordinary_operator_kit/SELECTED-PACKAGE.md": (2749, "365a6d76a36e338cd6dfb7d71daddb8136e63743fb1e395afb169cc89167b63c"),
    "software/v5/ordinary_operator_kit/SELECTED-KIT.json": (1751, "058d02d095b34b253303f4326f115b65d5046ae990960e828b0260a89f10ca38"),
    "software/v5/ordinary_operator_kit/AUTHORING-OFFERS.md": (10125, "0954e276c5e6de80e9eb3a66da1ed273bb67f304f5ed84d12bc9c60b158fb2b2"),
    "software/v5/ordinary_authoring_offers/CODEC.md": (4333, "7a12096fcb7818c823f6cd6f0735b3f1cdfe431d8dd7123c1271445392f93709"),
    "software/v5/ordinary_authoring_offers/API.md": (4166, "e51d0083c9827210762442733d23e7150dbb5e6ad754615c9cc51b48eb0cbdbb"),
}


def need(ok, code):
    if not ok:
        raise ValueError("SOURCE_BUNDLE_" + code)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def hexid(value):
    need(type(value) is str and len(value) == 64 and
         all(c in "0123456789abcdef" for c in value), "HASH")
    return value


def relative(name):
    need(type(name) is str and 0 < len(name) <= 1024, "RELATIVE_PATH")
    path = PurePosixPath(name)
    need(not path.is_absolute() and path.as_posix() == name and
         1 <= len(path.parts) <= 12 and all(part not in (".", "..") and
             not part.endswith((".", " ")) and not os.path.isreserved(part) and
             not any(ord(c) < 32 or c in ':*?"<>|\\' for c in part)
             for part in path.parts), "RELATIVE_PATH")
    return name


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":" and
         path.drive[0].isalpha() and path != Path(path.anchor) and
         len(path.parts) <= 128 and len(str(path)) <= 32768 and
         not str(path).startswith(("\\\\", "//")) and ".." not in path.parts,
         "ABSOLUTE_LOCAL_PATH")
    for part in path.parts[1:]:
        relative(part)
    for ancestor in (*reversed(path.parents), path):
        try:
            info = ancestor.lstat()
        except FileNotFoundError:
            need(fresh and ancestor == path, "MISSING_PATH")
            return path
        need(not stat.S_ISLNK(info.st_mode) and
             not getattr(info, "st_file_attributes", 0) & 0x400, "REDIRECTED_PATH")
        if ancestor != path or directory:
            need(stat.S_ISDIR(info.st_mode), "DIRECTORY")
        else:
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "SINGLE_FILE")
    need(not fresh, "OUTPUT_EXISTS")
    return path


def guard(callback=None):
    started, cpu = time.monotonic(), time.process_time()
    def check():
        need(time.monotonic()-started < 60 and time.process_time()-cpu < 30,
             "COOPERATIVE_ALLOWANCE")
        if callback is not None:
            callback()
    return check


def read(path, check, maximum=2*MIB):
    check(); path = ordinary(path)
    length = path.stat().st_size
    need(0 < length <= maximum, "FILE_BOUND")
    parts, count = [], 0
    with path.open("rb") as stream:
        while block := stream.read(min(MIB, maximum + 1 - count)):
            check(); count += len(block)
            need(count <= length, "FILE_GREW")
            parts.append(block)
    need(ordinary(path).stat().st_size == count == length, "FILE_CHANGED")
    return b"".join(parts)


def pin(raw):
    return {"bytes": len(raw), "sha256": sha(raw)}


def pin_shape(value):
    need(type(value) is dict and set(value) == {"bytes", "sha256"} and
         type(value["bytes"]) is int and 0 < value["bytes"] <= 2*MIB, "PIN_SHAPE")
    hexid(value["sha256"])
    return value


def strict_json(raw):
    need(type(raw) is bytes and 0 < len(raw) <= 2*MIB, "JSON_BOUND")
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    def reject(_):
        raise ValueError("SOURCE_BUNDLE_JSON_NUMBER")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=reject, parse_constant=reject)


def known_pins(root, check):
    raw = read(root/MAP, check)
    need(pin(raw) == {"bytes": FIXED[MAP][0], "sha256": FIXED[MAP][1]}, "SOURCE_MAP_PIN")
    mapping = strict_json(raw)
    need(type(mapping) is dict and
         mapping.get("schema") == "DMKN_ORDINARY_DISTRIBUTION_SOURCE_MAP_V1" and
         type(mapping.get("sources")) is dict and len(mapping["sources"]) == 84,
         "SOURCE_MAP_SHAPE")
    expected = dict(mapping["sources"])
    for name, value in expected.items():
        relative(name); pin_shape(value)
        need(name.startswith(("software/v5/", "software/assets/foundation/")), "SOURCE_SCOPE")
    need(not set(expected) & (set(FIXED) | NEW), "SOURCE_MAP_OVERLAP")
    expected.update({name: {"bytes": size, "sha256": digest}
                     for name, (size, digest) in FIXED.items()})
    need(len(expected) == 102 and len({n.casefold() for n in expected}) == 102,
         "KNOWN_SOURCE_COUNT")
    return expected


def validate_manifest(doc):
    need(type(doc) is dict and set(doc) == {"schema", "claim", "files", "entrypoints",
         "external_profile", "license_status"}, "MANIFEST_FIELDS")
    need(doc["schema"] == "DMKN_ORDINARY_SOURCE_DISTRIBUTION_V1" and
         doc["claim"] == CLAIM and doc["entrypoints"] == ENTRYPOINTS and
         doc["external_profile"] == EXTERNAL and doc["license_status"] == LICENSE,
         "MANIFEST_PROFILE")
    files = doc["files"]
    need(type(files) is dict and len(files) == 105 and all(type(name) is str for name in files) and
         len({name.casefold() for name in files}) == 105, "MANIFEST_CENSUS")
    total = 0
    for name, value in files.items():
        relative(name); total += pin_shape(value)["bytes"]
        need(name != MANIFEST, "MANIFEST_SELF_REFERENCE")
        need(not any(parent.as_posix() in files for parent in PurePosixPath(name).parents),
             "FILE_DIRECTORY_ALIAS")
    need(total <= 8*MIB, "SOURCE_TOTAL")
    return files


def census(root, files, check):
    names, folders, pending = set(), set(), [(root, 0)]
    allowed_dirs = {parent.as_posix() for name in files
                    for parent in PurePosixPath(name).parents if parent.as_posix() != "."}
    entries = 0
    while pending:
        folder, depth = pending.pop()
        with os.scandir(ordinary(folder, directory=True)) as listing:
            for entry in listing:
                check(); entries += 1
                need(entries <= 256 and depth < 12, "CENSUS_BOUND")
                path = Path(entry.path)
                name = relative(path.relative_to(root).as_posix())
                if entry.is_dir(follow_symlinks=False):
                    ordinary(path, directory=True)
                    need(name in allowed_dirs and name.casefold() not in folders,
                         "EXTRA_OR_ALIASED_DIRECTORY")
                    folders.add(name.casefold()); pending.append((path, depth + 1))
                else:
                    ordinary(path)
                    need(name in files and name.casefold() not in names,
                         "EXTRA_OR_ALIASED_FILE")
                    names.add(name.casefold())
    need(names == {name.casefold() for name in files} and
         folders == {name.casefold() for name in allowed_dirs}, "EXACT_CENSUS")


def verify(source_root, manifest_sha256, *, check=None):
    check = guard(check)
    check(); root = ordinary(source_root, directory=True)
    raw = read(root/MANIFEST, check)
    need(sha(raw) == hexid(manifest_sha256), "MANIFEST_PIN")
    doc = strict_json(raw)
    files = validate_manifest(doc)
    need(canonical(doc) == raw, "MANIFEST_CANONICAL")
    expected = known_pins(root, check)
    need(set(files) == set(expected) | NEW and
         all(files[name] == value for name, value in expected.items()), "EXACT_SELECTION")
    census(root, set(files) | {MANIFEST}, check)
    for name, value in sorted(files.items()):
        need(pin(read(root/name, check)) == value, "PAYLOAD_PIN:"+name)
    need(read(root/MANIFEST, check) == raw, "MANIFEST_CHANGED")
    census(root, set(files) | {MANIFEST}, check)
    check()
    return {"status": "VERIFIED_EXACT_SOURCE_NOT_BUILT", "manifest": pin(raw),
            "payload_files": len(files), "payload_bytes": sum(p["bytes"] for p in files.values()),
            "claim": CLAIM}


def fresh_bytes(path, raw):
    with ordinary(path, fresh=True).open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def pack(source_root, output, *, check=None):
    check = guard(check)
    check(); root = ordinary(source_root, directory=True)
    output = ordinary(output, directory=True, fresh=True)
    need(not root.is_relative_to(output), "SOURCE_OUTPUT_OVERLAP")
    expected = known_pins(root, check)
    selected = set(expected) | NEW
    need(all(not (root/name).is_relative_to(output) for name in selected), "INPUT_OUTPUT_OVERLAP")
    data = {}
    for name in sorted(selected):
        raw = read(root/relative(name), check)
        if name in expected:
            need(pin(raw) == expected[name], "SOURCE_PIN:"+name)
        data[name] = raw
    need(read(Path(__file__).absolute(), check) == data[PREFIX+"bundle.py"], "RUNNING_SOURCE")
    doc = {"schema": "DMKN_ORDINARY_SOURCE_DISTRIBUTION_V1", "claim": CLAIM,
           "files": {name: pin(raw) for name, raw in data.items()},
           "entrypoints": ENTRYPOINTS, "external_profile": EXTERNAL, "license_status": LICENSE}
    validate_manifest(doc)
    manifest_raw = canonical(doc)
    need(len(manifest_raw) <= 2*MIB, "MANIFEST_BOUND")
    payload_bytes = sum(len(raw) for raw in data.values())
    data[MANIFEST] = manifest_raw
    check(); ordinary(output, directory=True, fresh=True).mkdir()
    archive_path = output/"source.zip"
    # Stored entries avoid compression-version variability. The selected source
    # payload is about 3 MiB, so compression is not worth another dependency.
    with ordinary(archive_path, fresh=True).open("xb") as stream:
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED,
                             allowZip64=False) as archive:
            for name, raw in sorted(data.items()):
                check()
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_STORED
                archive.writestr(info, raw)
        stream.flush(); os.fsync(stream.fileno())
    archive_raw = read(archive_path, check, 16*MIB)
    # Read the actual ZIP back without extracting or importing any member.
    with zipfile.ZipFile(ordinary(archive_path), "r") as archive:
        rows = archive.infolist()
        need(archive.comment == b"" and [r.filename for r in rows] == sorted(data), "ZIP_CENSUS")
        for row in rows:
            check(); relative(row.filename)
            need(row.date_time == (1980, 1, 1, 0, 0, 0) and row.create_system == 3 and
                 row.external_attr == 0o100644 << 16 and row.compress_type == zipfile.ZIP_STORED and
                 row.extra == row.comment == b"" and row.flag_bits == 0 and
                 row.file_size == row.compress_size == len(data[row.filename]), "ZIP_METADATA")
            need(archive.read(row) == data[row.filename], "ZIP_PAYLOAD")
    for name in sorted(selected):
        need(read(root/name, check) == data[name], "SOURCE_CHANGED:"+name)
    need(read(Path(__file__).absolute(), check) == data[PREFIX+"bundle.py"], "RUNNING_SOURCE_CHANGED")
    need(read(archive_path, check, 16*MIB) == archive_raw, "ZIP_CHANGED")
    check()
    receipt = {"schema": "DMKN_ORDINARY_SOURCE_BUNDLE_RECEIPT_V1",
               "status": "PACKED_SOURCE_NOT_BUILT", "manifest": pin(manifest_raw),
               "archive": pin(archive_raw), "payload_files": 105, "archive_files": 106,
               "payload_bytes": payload_bytes, "source_root": str(root), "output": str(output),
               "claim": CLAIM}
    # This external terminal receipt is not part of the deterministic ZIP. Any
    # failure retains partial files; no retry or destructive cleanup is performed.
    fresh_bytes(output/"RECEIPT.json", canonical(receipt))
    return receipt


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON_PROFILE")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    subs = parser.add_subparsers(dest="action", required=True)
    packing = subs.add_parser("pack", allow_abbrev=False)
    packing.add_argument("--source-root", required=True)
    packing.add_argument("--output", required=True)
    verifying = subs.add_parser("verify", allow_abbrev=False)
    verifying.add_argument("--source-root", required=True)
    verifying.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args()
    result = pack(args.source_root, args.output) if args.action == "pack" else \
        verify(args.source_root, args.manifest_sha256)
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

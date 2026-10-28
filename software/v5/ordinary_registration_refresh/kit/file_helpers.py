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
MAP = "software/v5/ordinary_current_distribution/source-map.json"
PREFIX = "software/v5/ordinary_current_source_bundle/"
MANIFEST = "SOURCE-MANIFEST.json"
CLAIM = "EXACT_SOURCE_INPUTS_NOT_BUILD_OR_MATHEMATICAL_ACCEPTANCE"
ENTRYPOINTS = {"build": "software/v5/ordinary_current_distribution/build.py"}

EXTERNAL = {"os": "Windows x86-64", "python": "3.14.6", "lean": "4.34.0"}
LICENSE = "UNDECIDED_NO_PUBLIC_RELEASE_AUTHORIZATION"
NEW = {PREFIX + name for name in ("bundle.py", "README.md", "LICENSE-STATUS.md")}
# Existing reviewed bytes, not a source search/glob or approval of arbitrary code.
FIXED = {
    'software/v5/ordinary_current_distribution/source-map.json': (33503, "65fde356b8ce6146b07ab49fad40a859af5bf0ce32e8d7beea76e32da60a9c9e"),
    'software/v5/ordinary_current_distribution/build.py': (38889, "d14f2910003b8f8bc36dacc50796b37f87befbc60de76fb9cb575e30e8ce9ef1"),
    'software/v5/ordinary_current_distribution/README.md': (3624, "a9c6634977408a822d10245096c69df8109481b8e4b803fe2217f2301413696f"),
    'software/v5/ordinary_current_distribution/CONTRACT.md': (6287, "385f4bdbe52fdd36f0661b6eca444ed1d6fd9a4f6e44d9cf7cd3f91cee864be6"),
    'software/v5/ordinary_demand_frontier/API.md': (2814, "b3befdc821e6ff53f869cc5d274eb1a3cd146912978b839191d65ba9300e31d0"),
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
         mapping.get("schema") == "DMKN_ORDINARY_CURRENT_SOURCE_MAP_V1" and
         type(mapping.get("sources")) is dict and len(mapping["sources"]) == 87,
         "SOURCE_MAP_SHAPE")
    expected = dict(mapping["sources"])
    for name, value in expected.items():
        relative(name); pin_shape(value)
        need(name.startswith(("software/v5/", "software/assets/foundation/")), "SOURCE_SCOPE")
    need(not set(expected) & (set(FIXED) | NEW), "SOURCE_MAP_OVERLAP")
    expected.update({name: {"bytes": size, "sha256": digest}
                     for name, (size, digest) in FIXED.items()})
    need(len(expected) == 92 and len({n.casefold() for n in expected}) == 92,
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
    need(type(files) is dict and len(files) == 95 and all(type(name) is str for name in files) and
         len({name.casefold() for name in files}) == 95, "MANIFEST_CENSUS")
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
               "archive": pin(archive_raw), "payload_files": 95, "archive_files": 96,
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

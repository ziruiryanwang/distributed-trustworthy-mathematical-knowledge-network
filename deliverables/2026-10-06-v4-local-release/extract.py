"""Exact bounded v4 extraction, using an independently trusted Windows Python.

Obtain this script's hash, the archive hash and manifest hash independently.
No archive code, subprocess, network, build or mathematical check is executed.
Failed partial destinations are retained and never overwritten or retried.
"""
from __future__ import annotations

import time
BOOT_WALL, BOOT_CPU = time.monotonic(), time.process_time()
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import sys
import zipfile

MIB, GIB = 1024**2, 1024**3
PROFILE = {"bytes": 1881622, "sha256": "298d790ec380f50ca45307069fd577908131a0622e57a3aa455813268213bfc7"}
READ_BYTES = WRITE_BYTES = 0
PREFIX = "commons-v4/"


def need(value, code):
    if not value:
        raise ValueError(code)


def check():
    need(time.monotonic()-BOOT_WALL <= 1200 and time.process_time()-BOOT_CPU <= 600,
         "FINITE_EXTRACTION_TIME_ENVELOPE")
    need(READ_BYTES <= 16*GIB and WRITE_BYTES <= 4*GIB, "EXPLICIT_EXTRACTION_IO_ENVELOPE")


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":"
         and path != Path(path.anchor), "ABSOLUTE_NONROOT_LOCAL_PATH")
    need(all(p not in (".", "..") and not p.endswith((".", " "))
             and not os.path.isreserved(p) and not any(ord(c) < 32 or c in ':*?"<>|' for c in p)
             for p in path.parts[1:]), "ORDINARY_PATH_COMPONENT")
    for ancestor in reversed(path.parents):
        info = ancestor.lstat()
        need(stat.S_ISDIR(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "ORDINARY_PATH_ANCESTRY")
    if fresh:
        need(not os.path.lexists(path), "FRESH_DESTINATION_REQUIRED")
    else:
        info = path.lstat()
        need(not getattr(info, "st_file_attributes", 0) & 0x400
             and (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)),
             "ORDINARY_PATH_TARGET")
    need(path.resolve(strict=not fresh) == path, "CANONICAL_PATH_REQUIRED")
    return path


def relative(name):
    need(type(name) is str and 0 < len(name) <= 1024 and "\\" not in name, "RELATIVE_MEMBER")
    p = PurePosixPath(name)
    need(p.parts and p.as_posix() == name and not p.is_absolute()
         and all(x not in (".", "..") and not x.endswith((".", " "))
                 and not os.path.isreserved(x) and not any(ord(c) < 32 or c in ':*?"<>|' for c in x)
                 for x in p.parts), "SAFE_RELATIVE_MEMBER")
    return p.parts


def strict(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            need(key not in value, "DUPLICATE_JSON_KEY")
            value[key] = item
        return value
    def reject(_):
        raise ValueError("NONINTEGER_JSON_NUMBER")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=reject, parse_constant=reject)


def read_small(path, maximum=8*MIB):
    global READ_BYTES
    ordinary(path)
    need(0 < path.stat().st_size <= maximum, "SMALL_INPUT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    READ_BYTES += len(raw)
    need(0 < len(raw) <= maximum, "SMALL_INPUT_GREW"); check()
    return raw


def digest(path, maximum):
    global READ_BYTES
    ordinary(path)
    expected = path.stat().st_size
    need(0 <= expected <= maximum, "EXACT_INPUT_SIZE_BOUND")
    size, h = 0, hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            size += len(block); READ_BYTES += len(block)
            need(size <= expected, "HASH_INPUT_GREW")
            h.update(block); check()
    need(size == expected == path.stat().st_size, "HASH_INPUT_CHANGED")
    return {"bytes": size, "sha256": h.hexdigest()}


def manifest_members(raw):
    value = strict(raw)
    need(type(value) is dict and set(value) == {"schema", "release", "profile", "files"}
         and value["schema"] == "DMKN_V4_LOCAL_RELEASE_MANIFEST_V1"
         and value["release"] == "v4-2026-10-06" and value["profile"] == "contributor/profile.json",
         "EXACT_RELEASE_MANIFEST")
    files = value["files"]
    need(type(files) is dict and 12470 <= len(files) <= 12600, "COMPLETE_BOUNDED_PAYLOAD_MAP")
    aliases, total = {}, 0
    components = {"contributor", "fragment-peer", "source", "operator", "docs", "examples"}
    for name, row in files.items():
        parts = relative(name)
        need(len(parts) >= 2 and parts[0] in components, "EXACT_COMPONENT_MEMBER")
        need(type(row) is dict and set(row) == {"bytes", "sha256"}
             and type(row["bytes"]) is int and 0 <= row["bytes"] <= 512*MIB
             and type(row["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]),
             "EXACT_MEMBER_PIN")
        for length in range(1, len(parts)+1):
            prefix = "/".join(parts[:length])
            previous = aliases.setdefault(prefix.casefold(), prefix)
            need(previous == prefix, "MEMBER_OR_DIRECTORY_CASE_ALIAS")
            if length < len(parts):
                need(prefix not in files, "FILE_DIRECTORY_COLLISION")
        total += row["bytes"]
    need(total <= 3*GIB and len(aliases) <= 14000, "PAYLOAD_BYTE_OR_ENTRY_LIMIT")
    need(files.get("contributor/profile.json") == PROFILE, "EXACT_ADOPTED_PROFILE")
    need(sum(n.startswith("contributor/") for n in files) == 12399
         and sum(n.startswith("fragment-peer/") for n in files) == 11
         and sum(n.startswith("source/") for n in files) == 61, "EXACT_FROZEN_COMPONENT_COUNTS")
    return {**files, "RELEASE-MANIFEST.json": {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}}


def bounded_directory(stream, archive_bytes, expected_members):
    """Bound central-directory allocation before stdlib ZipFile parses it.

The selected producer has no ZIP comment or multidisk archive. Its optional
ZIP64 records have fixed standard lengths; payload members are below 512 MiB.
"""
    global READ_BYTES
    need(22 <= archive_bytes <= 4*GIB, "ARCHIVE_SIZE_BOUND")
    stream.seek(archive_bytes-22)
    tail = stream.read(22); READ_BYTES += len(tail)
    need(len(tail) == 22, "ARCHIVE_END_TRUNCATED")
    signature, disk, first_disk, count_disk, count, size, offset, comment = struct.unpack("<4s4H2LH", tail)
    need(signature == b"PK\x05\x06" and disk == first_disk == comment == 0
         and count_disk == count == expected_members and 0 < size <= 16*MIB
         and 0 <= offset < 0xffffffff and offset+size <= archive_bytes-22,
         "BOUNDED_SINGLE_DISK_CENTRAL_DIRECTORY")
    gap = archive_bytes-22-(offset+size)
    need(gap in (0, 76), "ONLY_STANDARD_ZIP64_TRAILER")
    if gap:
        stream.seek(offset+size)
        raw = stream.read(76); READ_BYTES += len(raw)
        need(len(raw) == 76, "ZIP64_TRAILER_TRUNCATED")
        zsig, length, made, needed, zdisk, zfirst, n_disk, n, zsize, zoffset = struct.unpack("<4sQ2H2L4Q", raw[:56])
        lsig, ldisk, location, disks = struct.unpack("<4sLQL", raw[56:])
        need(zsig == b"PK\x06\x06" and length == 44 and zdisk == zfirst == 0
             and n_disk == n == count and zsize == size and zoffset == offset
             and lsig == b"PK\x06\x07" and ldisk == 0 and location == offset+size and disks == 1,
             "EXACT_STANDARD_ZIP64_TRAILER")
    check(); stream.seek(0)


def safe_extra(raw):
    # Python's ZIP64 writer may encode a large header offset in central extras.
    if not raw:
        return
    need(len(raw) >= 4, "ZIP_EXTRA_TRUNCATED")
    tag, size = struct.unpack("<HH", raw[:4])
    need(tag == 1 and size in (8, 16, 24, 28) and len(raw) == 4+size, "ONLY_ZIP64_EXTRA")


def write_report(path, value):
    global WRITE_BYTES
    raw = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+"\n").encode()
    need(len(raw) <= 128*1024 and WRITE_BYTES+len(raw) <= 4*GIB, "RESULT_BYTE_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    WRITE_BYTES += len(raw)


def main(argv=None):
    global READ_BYTES, WRITE_BYTES
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--archive-sha256", required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args(argv)
    need(os.name == "nt" and sys.version_info >= (3, 13) and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "TRUSTED_WINDOWS_PYTHON313PLUS_ISOLATED_REQUIRED")
    need(all(re.fullmatch(r"[0-9a-f]{64}", value) for value in (args.archive_sha256, args.manifest_sha256)),
         "EXTERNALLY_ADOPTED_SHA256_REQUIRED")
    archive, manifest = ordinary(args.archive), ordinary(args.manifest)
    destination = ordinary(args.destination, directory=True, fresh=True)
    need(not archive.is_relative_to(destination) and not manifest.is_relative_to(destination), "INPUT_DESTINATION_OVERLAP")
    raw = read_small(manifest)
    need(hashlib.sha256(raw).hexdigest() == args.manifest_sha256, "EXTERNAL_MANIFEST_PIN")
    members = manifest_members(raw)
    archive_pin = digest(archive, 4*GIB)
    need(archive_pin["sha256"] == args.archive_sha256, "EXTERNAL_ARCHIVE_PIN")
    result = {"status": "FAIL", "scope": "FILE_IDENTITY_ONLY_NOT_RUNTIME_OR_MATH_QUALIFICATION",
        "workers_launched": 0, "archive": {"path": str(archive), **archive_pin},
        "manifest": {"path": str(manifest), **members["RELEASE-MANIFEST.json"]},
        "destination": str(destination), "release": str(destination / "commons-v4"),
        "expected_members": len(members), "copied_members": 0, "readback_members": 0}
    created = False
    try:
        with archive.open("rb") as held:
            bounded_directory(held, archive_pin["bytes"], len(members))
            with zipfile.ZipFile(held) as source:
                infos = source.infolist()
                need(source.comment == b"" and len(infos) == len(members)
                     and len({x.filename for x in infos}) == len(infos)
                     and {x.filename for x in infos} == {PREFIX+n for n in members}, "EXACT_ARCHIVE_MEMBER_MAP")
                for info in infos:
                    name = info.filename[len(PREFIX):]
                    relative(name)
                    need(not info.is_dir() and not info.flag_bits & 1 and info.comment == b""
                         and info.compress_type == zipfile.ZIP_STORED and info.create_system == 3
                         and stat.S_IFMT(info.external_attr >> 16) == stat.S_IFREG
                         and info.file_size == info.compress_size == members[name]["bytes"], "REGULAR_STORED_EXACT_MEMBER")
                    safe_extra(info.extra); check()
                ordinary(destination, directory=True, fresh=True)
                destination.mkdir(); created = True
                release = destination / "commons-v4"
                release.mkdir()
                for info in sorted(infos, key=lambda item: item.filename):
                    name = info.filename[len(PREFIX):]
                    path = release.joinpath(*relative(name))
                    path.parent.mkdir(parents=True, exist_ok=True)
                    ordinary(path.parent, directory=True); ordinary(path, fresh=True)
                    h, count = hashlib.sha256(), 0
                    with source.open(info) as inp, path.open("xb") as out:
                        while block := inp.read(MIB):
                            count += len(block); READ_BYTES += len(block)
                            need(count <= members[name]["bytes"], "EXTRACT_MEMBER_GREW")
                            out.write(block); WRITE_BYTES += len(block); h.update(block); check()
                        out.flush(); os.fsync(out.fileno())
                    need({"bytes": count, "sha256": h.hexdigest()} == members[name], "EXACT_EXTRACTED_MEMBER")
                    result["copied_members"] += 1
        release = destination / "commons-v4"
        observed, entries = set(), 0
        for directory, folders, leaves in os.walk(release, followlinks=False):
            ordinary(Path(directory), directory=True); check()
            for name in folders+leaves:
                entries += 1; need(entries <= 14001, "EXTRACTED_ENTRY_LIMIT")
                ordinary(Path(directory)/name, directory=name in folders)
            observed.update((Path(directory)/name).relative_to(release).as_posix() for name in leaves)
        need(observed == set(members), "EXACT_EXTRACTED_FILE_MAP")
        for name, wanted in members.items():
            need(digest(release.joinpath(*relative(name)), 512*MIB) == wanted, "EXTRACTED_READBACK_PIN")
            result["readback_members"] += 1
        profile = strict(read_small(release / "contributor/profile.json"))
        need({name[len("contributor/"):]: row for name, row in members.items() if name.startswith("contributor/")}
             == {**profile["assets"], "profile.json": PROFILE}, "EXACT_CONTRIBUTOR_PROFILE_MAP")
        need(read_small(manifest) == raw and read_small(release / "RELEASE-MANIFEST.json") == raw, "MANIFEST_BYTES_UNCHANGED")
        need(digest(archive, 4*GIB) == archive_pin, "ARCHIVE_BYTES_UNCHANGED")
        check()
        result["status"] = "PASS_EXACT_V4_EXTRACTION_NOT_RUNTIME_QUALIFICATION"
    except BaseException as exc:
        result["error"] = type(exc).__name__+": "+str(exc)[:2000]
    result.update(explicit_read_bytes=READ_BYTES, explicit_written_bytes=WRITE_BYTES,
                  controller_cpu_seconds=time.process_time()-BOOT_CPU, wall_seconds=time.monotonic()-BOOT_WALL)
    if created:
        write_report(destination / "EXTRACT-RESULT.json", result)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status": "EXTRACT_REFUSED_OR_REPORT_FAILED", "error": type(exc).__name__+": "+str(exc)[:2000]}),
              file=sys.stderr)
        raise SystemExit(1)
    finally:
        print(json.dumps({"event": "file-extract-final", "workers_launched": 0,
            "cpu_seconds": time.process_time()-BOOT_CPU, "wall_seconds": time.monotonic()-BOOT_WALL}), file=sys.stderr)

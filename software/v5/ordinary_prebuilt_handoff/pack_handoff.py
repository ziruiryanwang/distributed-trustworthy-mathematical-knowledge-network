"""Maintainer-only exact native-package ZIP/readback/relocation, not an installer.

Only one pinned file-only helper is executed. No product/native imports, runtime
downloads, state, compilation, network, overwrite or cleanup. Approve software
independently and protect inputs; hashes are not publisher authentication.
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
import types
import zipfile

MIB = 1024**2
HELPER = "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
PROFILE_SHA = "ca257419f464c2e9d968011983673160377f743ebbe2a27e2399b510dce1ce67"
INSTALLATION_SHA = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
ASSEMBLY_SHA = "ec5ab7709aba2c4a896fa1898e925effb8f7a95f17bdb300c55307fcc5c10d6c"
COUNT = 154
PAYLOAD_BYTES = 39148493
DOCUMENTS = {"README.md", "LAUNCHER.md", "PRODUCER.md", "RECEIVE-POLICY.md",
             "CONTACTS.md", "SPARSE-SEARCH.md", "BOUNDED-TRANSPORT.md", "EXECUTION-TRUST.md"}
CLAIM = "EXACT_PREBUILT_BYTES_NOT_EXECUTION_MATHEMATICAL_ACCEPTANCE_OR_PUBLIC_RELEASE"


def require(ok, code):
    if not ok:
        raise ValueError("PREBUILT_HANDOFF_" + code)


def bootstrap_path(value):
    path = Path(value)
    require(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":" and
            path.drive[0].isalpha() and path != Path(path.anchor) and
            len(path.parts) <= 128 and len(str(path)) <= 32768 and
            not str(path).startswith(("\\\\", "//")), "BOOTSTRAP_PATH")
    for part in path.parts[1:]:
        require(part not in (".", "..") and not part.endswith((".", " ")) and
                not os.path.isreserved(part) and
                not any(ord(c) < 32 or c in ':*?"<>|\\' for c in part), "BOOTSTRAP_PART")
    for parent in (*reversed(path.parents), path):
        info = parent.lstat()
        require(not stat.S_ISLNK(info.st_mode) and
                not getattr(info, "st_file_attributes", 0) & 0x400, "BOOTSTRAP_REDIRECT")
        require(stat.S_ISDIR(info.st_mode) if parent != path else
                stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "BOOTSTRAP_KIND")
    return path


def helpers():
    here = bootstrap_path(Path(__file__).absolute())
    require(len(here.parents) > 3, "BOOTSTRAP_LAYOUT")
    path = bootstrap_path(here.parents[3]/HELPER)
    require(path.stat().st_size == 18374, "BOOTSTRAP_LENGTH")
    with path.open("rb") as stream:
        raw = stream.read(18375)
    require(len(raw) == 18374 and hashlib.sha256(raw).hexdigest() == HELPER_SHA,
            "BOOTSTRAP_PIN")
    require(bootstrap_path(path).stat().st_size == 18374, "BOOTSTRAP_CHANGED")
    module = types.ModuleType("_approved_prebuilt_file_helpers")
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def selected_map(H, package, assembly_receipt, check):
    package = H.ordinary(package, directory=True)
    profile, profile_pin = H.read_json(package/"PROFILE.json", PROFILE_SHA, check)
    receipt, receipt_pin = H.read_json(assembly_receipt, ASSEMBLY_SHA, check)
    installed, installed_pin = H.read_json(package/"installation/INSTALLATION.json", INSTALLATION_SHA, check)
    require(profile.get("schema") == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
            profile.get("installation_manifest_sha256") == INSTALLATION_SHA and
            type(profile.get("files")) is dict and len(profile["files"]) == 117,
            "PROFILE_SELECTION")
    require(installed.get("schema") == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1" and
            type(installed.get("files")) is dict and
            set(installed["files"]) == H.INST_FILES | H.RUNTIME_FILES, "INSTALLATION_SELECTION")
    require(receipt.get("status") == "ASSEMBLED_NOT_ADOPTED" and
            receipt.get("profile_sha256") == PROFILE_SHA and
            receipt.get("installation_manifest_sha256") == INSTALLATION_SHA and
            type(receipt.get("documentation_files")) is dict and
            set(receipt["documentation_files"]) == DOCUMENTS, "ASSEMBLY_SELECTION")
    files = dict(profile["files"])
    files.update({"installation/" + name: pin for name, pin in installed["files"].items()
                  if name in H.INST_FILES})
    files.update(receipt["documentation_files"])
    files.update({"PROFILE.json": profile_pin, "installation/INSTALLATION.json": installed_pin})
    require(len(files) == COUNT and len({name.casefold() for name in files}) == COUNT,
            "EXACT_FILE_SELECTION")
    for name, pin in files.items():
        H.relative(name); H.pin_shape(pin)
        require(not any(p.as_posix() in files for p in PurePosixPath(name).parents), "FILE_DIRECTORY_ALIAS")
    require(sum(pin["bytes"] for pin in files.values()) == PAYLOAD_BYTES, "EXACT_BYTE_SELECTION")
    for name in H.RUNTIME_FILES:
        H.pin_shape(installed["files"][name])  # Attachments are not opened/copied.
    require(receipt_pin["sha256"] == ASSEMBLY_SHA, "ASSEMBLY_PIN")
    return files, profile, installed, receipt


def check_tree(H, root, files, check):
    """Maintainer exact-byte census; not a new product loader or trust mode."""
    root = H.ordinary(root, directory=True)
    H.census(root, files, check)
    allowed = {p.as_posix() for name in files for p in PurePosixPath(name).parents
               if p.as_posix() != "."}
    seen, count = set(), 0
    # The reused helper checks files; additionally reject empty extra directories.
    for folder, directories, names in os.walk(root, followlinks=False):
        check(); count += len(directories) + len(names)
        require(count <= 512, "DIRECTORY_CENSUS_BOUND")
        for name in directories:
            path = H.ordinary(Path(folder)/name, directory=True)
            relative = H.relative(path.relative_to(root).as_posix())
            require(relative in allowed and relative.casefold() not in seen, "EXTRA_OR_ALIASED_DIRECTORY")
            seen.add(relative.casefold())
    require(seen == {name.casefold() for name in allowed}, "DIRECTORY_CENSUS")
    for name, expected in sorted(files.items()):
        require(H.pin(root/H.relative(name), check) == expected, "PAYLOAD_PIN:" + name)


def stream_checked(inp, out, expected, check):
    count, digest = 0, hashlib.sha256()
    while block := inp.read(MIB):
        check(); count += len(block)
        require(count <= expected["bytes"], "STREAM_BOUND")
        digest.update(block)
        if out is not None:
            out.write(block)
    require(count == expected["bytes"] and digest.hexdigest() == expected["sha256"], "STREAM_PIN")


def inspect_archive(H, archive_path, files, check):
    require(type(files) is dict and 0 < len(files) <= COUNT and
            len({name.casefold() for name in files}) == len(files), "ZIP_SELECTION_ALIAS")
    for name, pin in files.items():
        check(); H.relative(name); H.pin_shape(pin)
    before = H.pin(archive_path, check, 64*MIB)
    with zipfile.ZipFile(H.ordinary(archive_path), "r") as archive:
        rows = archive.infolist()
        require(archive.comment == b"" and [row.filename for row in rows] == sorted(files), "ZIP_CENSUS")
        for row in rows:
            check(); H.relative(row.filename)
            pin = files[row.filename]
            require(not row.is_dir() and row.date_time == (1980, 1, 1, 0, 0, 0) and
                    row.create_system == 3 and row.external_attr == 0o100644 << 16 and
                    row.compress_type == zipfile.ZIP_STORED and row.flag_bits == 0 and
                    row.extra == row.comment == b"" and
                    row.file_size == row.compress_size == pin["bytes"], "ZIP_METADATA")
            with archive.open(row, "r") as stream:
                stream_checked(stream, None, pin, check)
    require(H.pin(archive_path, check, 64*MIB) == before, "ZIP_CHANGED")
    return before


def pack(package, assembly_receipt, output, *, check=None):
    started, cpu = time.monotonic(), time.process_time()
    parent_check = check
    def budget():
        require(time.monotonic()-started < 120 and time.process_time()-cpu < 60, "COOPERATIVE_ALLOWANCE")
        if parent_check is not None:
            parent_check()
    H = helpers(); budget()
    package = H.ordinary(package, directory=True)
    assembly_receipt = H.ordinary(assembly_receipt)
    output = H.ordinary(output, directory=True, fresh=True)
    utility = H.ordinary(Path(__file__).absolute())
    guide = H.ordinary(utility.parent/"README.md")
    helper = H.ordinary(utility.parents[3]/HELPER)
    for path in (package, assembly_receipt, utility.parent, helper):
        require(not output.is_relative_to(path) and not path.is_relative_to(output), "OUTPUT_OVERLAP")
    files, _, _, _ = selected_map(H, package, assembly_receipt, budget)
    check_tree(H, package, files, budget)
    utility_pin, guide_pin = H.pin(utility, budget, 2*MIB), H.pin(guide, budget, 2*MIB)
    assembly_pin, helper_pin = H.pin(assembly_receipt, budget, 2*MIB), H.pin(helper, budget, 2*MIB)
    require(assembly_pin["sha256"] == ASSEMBLY_SHA and helper_pin["sha256"] == HELPER_SHA, "SUPPORT_CHANGED")
    with guide.open("rb") as stream:
        guide_raw = stream.read(2*MIB+1)
    require({"bytes": len(guide_raw), "sha256": H.digest(guide_raw)} == guide_pin, "GUIDE_CHANGED")
    budget(); H.ordinary(output, directory=True, fresh=True).mkdir()
    archive_path = output/"package.zip"
    with H.ordinary(archive_path, fresh=True).open("xb") as stream:
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED, allowZip64=False) as archive:
            for name, pin in sorted(files.items()):
                budget()
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3; info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_STORED; info.file_size = pin["bytes"]
                with H.ordinary(package/name).open("rb") as inp, archive.open(info, "w") as out:
                    stream_checked(inp, out, pin, budget)
        stream.flush(); os.fsync(stream.fileno())
    archive_pin = inspect_archive(H, archive_path, files, budget)
    relocated = output/"relocated"
    H.ordinary(relocated, directory=True, fresh=True).mkdir()
    with zipfile.ZipFile(H.ordinary(archive_path), "r") as archive:
        for name, pin in sorted(files.items()):
            budget(); target = relocated/H.relative(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            H.ordinary(target.parent, directory=True)
            with archive.open(name, "r") as inp, H.ordinary(target, fresh=True).open("xb") as out:
                stream_checked(inp, out, pin, budget)
                out.flush(); os.fsync(out.fileno())
    check_tree(H, relocated, files, budget)
    H.fresh_bytes(output/"README.md", guide_raw)
    require(H.pin(output/"README.md", budget, 2*MIB) == guide_pin, "OUTPUT_GUIDE_PIN")
    check_tree(H, package, files, budget)
    for path, pin in ((utility, utility_pin), (guide, guide_pin), (helper, helper_pin),
                      (assembly_receipt, assembly_pin)):
        require(H.pin(path, budget, 2*MIB) == pin, "INPUT_CHANGED")
    require(H.pin(archive_path, budget, 64*MIB) == archive_pin, "FINAL_ARCHIVE_PIN")
    budget()
    receipt = {"schema": "DMKN_ORDINARY_PREBUILT_HANDOFF_RECEIPT_V1",
        "status": "PACKED_AND_RELOCATED_EXACT_PREBUILT_NOT_EXECUTED", "files": files,
        "archive": archive_pin, "guide": guide_pin, "utility": utility_pin,
        "profile_sha256": PROFILE_SHA, "installation_manifest_sha256": INSTALLATION_SHA,
        "assembly_receipt": assembly_pin, "package": str(package), "output": str(output),
        "relocated": str(relocated), "payload_files": COUNT, "payload_bytes": PAYLOAD_BYTES,
        "archive_files": COUNT, "claim": CLAIM,
        "wall_seconds": time.monotonic()-started, "cpu_seconds": time.process_time()-cpu}
    H.fresh_bytes(output/"RECEIPT.json", H.canonical(receipt))
    return receipt


def main():
    require(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
            sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON_PROFILE")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("package", "assembly-receipt", "output"):
        parser.add_argument("--"+name, required=True, type=Path)
    args = parser.parse_args()
    result = pack(args.package, args.assembly_receipt, args.output)
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

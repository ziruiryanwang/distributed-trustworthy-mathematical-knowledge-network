"""Small owner-only assembler for an ordinary admission installation.

No compilation, native call, catalog opening, migration or mathematical adoption.
An explicit pinned owner plan selects each source file; no recursive copy or file
discovery occurs. Named runtimes are verified at external owner roots, not copied.
Copied support is bounded and checked before/copy/after. Failure preserves a
partial fresh destination; INSTALLATION.json is written last. Its existence is
an assembly result, not authority to trust the implementation or use old stores.

Plan canonical JSON: schema, roles, compiled_dirs, support_groups, files.
Each files[logical_path] is {source:absolute_owner_path,bytes,sha256}. The other
fields have ordinary_admission's manifest shapes. The admission core separately
enforces its exact supported-role/module/layout requirements when opened.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import struct
import sys
import time

_SOURCE = Path(__file__).resolve().parent
if str(_SOURCE) not in sys.path:
    sys.path.insert(0, str(_SOURCE))
import ordinary_admission as A
import ordinary_evidence as E
import ordinary_semantics as S
import local_catalog as C
import portable_catalog as P

PLAN_SCHEMA = "DMKN_ORDINARY_INSTALLATION_PLAN_V1"
MIB = 1024*1024
need = C.need


def assemble(destination, plan_raw, expected_plan_sha256, *, runtime_roots, deadline):
    """Build fresh local support from owner-selected bytes; never adopt it.

    deadline is one absolute monotonic parent deadline, not a renewable timeout.
    Runtime support is named/nonhermetic and immutable-owner storage remains a
    premise. Copy quota excludes runtime attachments because they are not copied.
    """
    need(type(deadline) in (int, float) and math.isfinite(deadline) and
         0 < deadline-time.monotonic() <= 3600, "INSTALLATION_DEADLINE")
    def live():
        need(time.monotonic() < deadline, "INSTALLATION_DEADLINE")
    live()
    C.hexid(expected_plan_sha256)
    need(type(plan_raw) is bytes and P.sha(plan_raw) == expected_plan_sha256, "INSTALLATION_OWNER_PLAN_PIN")
    plan = E.strict_json(plan_raw, E.Limits(max_bytes=2*MIB))
    P.fields(plan, ("schema", "roles", "compiled_dirs", "support_groups", "files"), "INSTALLATION_PLAN_FIELDS")
    need(plan["schema"] == PLAN_SCHEMA, "INSTALLATION_PLAN_SCHEMA")
    P.fields(plan["roles"], A.ROLE_FILES, "INSTALLATION_PLAN_ROLES")
    P.fields(plan["support_groups"], P.SUPPORT_FIELDS, "INSTALLATION_PLAN_GROUPS")
    P.fields(runtime_roots, A.RUNTIME_ROOTS, "INSTALLATION_RUNTIME_ROOTS")
    attachments = {key: C.ordinary(value, directory=True) for key, value in runtime_roots.items()}
    target = C.ordinary(destination, directory=True, fresh=True)
    roots = [target, *attachments.values()]
    for position, left in enumerate(roots):
        for right in roots[position+1:]:
            need(not left.is_relative_to(right) and not right.is_relative_to(left), "INSTALLATION_ROOT_OVERLAP")
    files = plan["files"]
    need(type(files) is dict and 1 <= len(files) <= 512 and
         len({key.casefold() for key in files}) == len(files), "INSTALLATION_FILE_CENSUS")
    sources, pins, copied, total_bytes, copied_bytes = {}, {}, {}, 0, 0
    for logical, selected in files.items():
        live()
        relative = A.relative(logical)
        P.fields(selected, ("source", "bytes", "sha256"), "INSTALLATION_SELECTED_FILE")
        need(type(selected["source"]) is str, "INSTALLATION_SOURCE_PATH")
        source = C.ordinary(selected["source"])
        need(not source.is_relative_to(target) and not target.is_relative_to(source), "INSTALLATION_SOURCE_DESTINATION_OVERLAP")
        pin = {"bytes": P.uint(selected["bytes"], 1, 512*MIB, "INSTALLATION_FILE_SIZE"),
               "sha256": C.hexid(selected["sha256"])}
        sources[logical], pins[logical] = source, pin
        total_bytes += pin["bytes"]
        need(total_bytes <= 2*1024*MIB, "INSTALLATION_NAMED_SUPPORT_BOUND")
        if relative.parts[0] in attachments:
            need(len(relative.parts) >= 2 and
                 source == attachments[relative.parts[0]].joinpath(*relative.parts[1:]),
                 "INSTALLATION_RUNTIME_ATTACHMENT_BINDING")
        else:
            need(logical not in ("INSTALLATION.json", ".INSTALLATION.pending"), "INSTALLATION_RESERVED_MANIFEST")
            copied[logical] = target.joinpath(*relative.parts)
            copied_bytes += pin["bytes"]
            need(copied_bytes <= 256*MIB, "INSTALLATION_COPY_BYTE_BOUND")
            for parent in relative.parents:
                need(parent.as_posix() not in files, "INSTALLATION_FILE_DIRECTORY_ALIAS")
    need(copied, "INSTALLATION_EMPTY_SUPPORT")
    for role, logical in plan["roles"].items():
        need(type(logical) is str and logical in files, "INSTALLATION_UNPINNED_ROLE:"+role)
    groups = plan["support_groups"]
    covered = set()
    for field, selected in groups.items():
        need(type(selected) is list and selected == sorted(set(selected)) and
             set(selected) <= set(files), "INSTALLATION_GROUP_CENSUS:"+field)
        covered.update(selected)
    need(covered == set(files), "INSTALLATION_UNCOMMITTED_FILE")
    compiled = plan["compiled_dirs"]
    need(type(compiled) is dict and 1 <= len(compiled) <= 8, "INSTALLATION_COMPILED_DIRECTORIES")
    for directory, names in compiled.items():
        relative = A.relative(directory)
        need(relative.parts[0] not in attachments and type(names) is list and
             names == sorted(set(names)) and 1 <= len(names) <= 8, "INSTALLATION_COMPILED_CENSUS")
        need(set(names) == {A.relative(path).name for path in copied
                           if A.relative(path).parent == relative}, "INSTALLATION_COMPILED_EXACT_FILES")
        need(all(type(name) is str and name in {n+".olean" for n in A.NATIVE_MODULES}
                 for name in names), "INSTALLATION_COMPILED_MODULE_NAME")

    def verify(path, pin):
        live()
        C.ordinary(path)
        need(path.stat().st_size == pin["bytes"], "INSTALLATION_PIN_SIZE")
        digest, size = hashlib.sha256(), 0
        with path.open("rb") as stream:
            while block := stream.read(MIB):
                live(); size += len(block)
                need(size <= pin["bytes"], "INSTALLATION_PIN_GREW")
                digest.update(block)
        need(size == pin["bytes"] and path.stat().st_size == size and digest.hexdigest() == pin["sha256"],
             "INSTALLATION_PIN_CHANGED")
    for logical, source in sources.items():
        verify(source, pins[logical])

    architecture = {"amd64": "x86_64", "x86_64": "x86_64", "arm64": "aarch64",
                    "aarch64": "aarch64"}.get(platform.machine().lower())
    implementation = {"schema": S.IMPLEMENTATION_SCHEMA, "semantic_id": S.semantic_id(),
        "platform": {"os": "windows", "architecture": architecture,
                     "word_bits": struct.calcsize("P")*8, "byte_order": sys.byteorder},
        "snapshot_format": "LEAN_4_34_MODULEDATA_NO_EXTENSIONS_NO_IR",
        "support_scope": "EXPLICIT_NAMED_SUPPORT_NOT_HERMETIC_TOOLCHAIN"}
    need(sys.platform == "win32", "INSTALLATION_SUPPORTED_HOST")
    manifest = {"schema": A.INSTALL_SCHEMA, "implementation": implementation, "roles": plan["roles"],
                "compiled_dirs": compiled, "support_groups": groups, "files": pins}
    for field in P.SUPPORT_FIELDS:
        implementation[field] = A.support_digest(field, manifest)
    implementation_raw = E.canonical_json(implementation)
    S.read_implementation(implementation_raw)
    manifest_raw = E.canonical_json(manifest)
    need(len(manifest_raw) <= 2*MIB, "INSTALLATION_MANIFEST_BOUND")
    live()
    target.mkdir()
    directories = {parent for path in copied.values() for parent in path.parents
                   if parent != target and parent.is_relative_to(target)}
    for directory in sorted(directories, key=lambda path: (len(path.parts), str(path))):
        live(); C.ordinary(directory, directory=True, fresh=True).mkdir()
    for logical, destination_path in sorted(copied.items()):
        live()
        source, pin = sources[logical], pins[logical]
        C.ordinary(destination_path, fresh=True)
        digest, size = hashlib.sha256(), 0
        with source.open("rb") as incoming, destination_path.open("xb") as outgoing:
            while block := incoming.read(MIB):
                live(); size += len(block)
                need(size <= pin["bytes"], "INSTALLATION_COPY_GREW")
                outgoing.write(block); digest.update(block)
            outgoing.flush()
            os.fsync(outgoing.fileno())
        need(size == pin["bytes"] and digest.hexdigest() == pin["sha256"], "INSTALLATION_COPY_CHANGED")
        verify(destination_path, pin)
        verify(source, pin)
    live()
    manifest_path = target/"INSTALLATION.json"
    pending = target/".INSTALLATION.pending"
    P.PortableCatalog._write_fresh(pending, manifest_raw)
    result = {"status": "ASSEMBLED_NOT_ADOPTED", "manifest_path": str(manifest_path),
            "manifest_sha256": P.sha(manifest_raw), "implementation_id": S.implementation_id(implementation_raw),
            "files_copied": len(copied), "bytes_copied": copied_bytes,
            "runtime_attachment_files": len(files)-len(copied)}
    live()
    C.ordinary(manifest_path, fresh=True)
    # Same-directory Windows rename is non-overwriting. A failed prior write
    # leaves only .pending, not a completed public manifest.
    pending.rename(manifest_path)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("destination", "plan", "plan-sha256", "python-runtime", "lean-runtime"):
        parser.add_argument("--"+flag, required=True)
    parser.add_argument("--seconds", type=int, required=True)
    args = parser.parse_args()
    P.uint(args.seconds, 1, 3600, "INSTALLATION_FINITE_SECONDS")
    deadline = time.monotonic()+args.seconds
    result = assemble(args.destination, C.read_bounded(Path(args.plan), 2*MIB), args.plan_sha256,
        runtime_roots={"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime}, deadline=deadline)
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

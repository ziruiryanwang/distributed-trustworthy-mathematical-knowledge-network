"""Focused source-only bundle controls; root owns the single finite launch.

Imports only the separately selected bundle utility, never product/build code.
One real pack, test-owned extraction and isolated public verify subprocess;
no native build, sockets or owner state.
All fixtures and partial outputs are retained, including after failure.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import socket
import sqlite3
import stat
import subprocess
import sys
from unittest.mock import patch
import zipfile

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
MANIFEST = "SOURCE-MANIFEST.json"
MAP = "software/v5/ordinary_bounded_operations/source-map.json"
EXTRAS = {
    "software/v5/ordinary_bounded_operations/build.py": "79a056932d5720e9ab964ee50a01d1b04569a60a5e6445df0070a2b6556b42f9",
    MAP: "e9b7a873c8e509651833de51e5bd6beda130c74fdf7391859a8661c08426396a",
    "software/v5/ordinary_fair_search/assemble.py": "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30",
    "software/v5/ordinary_fair_search/profile.py": "828031e82f3dd43865d189587affa61dd6f8abe5b8667d45da0673949a069743",
    "software/v5/ordinary_fair_search/peer_api.py": "06663bcda04345cb9ea38ca422d7545b5736a208c2d79742bebc095f5409b7e5",
    "software/v5/ordinary_fair_search/fair_exchange.py": "3fe626b2dc4e63c345e54a517b1b37eea6eedada6d0fbb497aa18745a93eb828",
    "software/v5/ordinary_fair_search/fair_search.py": "2567fcb2308c7e477c08b958a3661348eee682c5a98ce2389dd9add02d48e652",
    "software/v5/ordinary_fair_search/README.md": "c3d8642b6fe9ece1b12c3a313910d14c52442b78a94c8af1b44dbe0901115aa5",
    "software/v5/ordinary_operator_kit/prepare.py": "a843efb7a5b2518469260e5d5acedad530068147cf86851c867c75d9e22e855e",
    "software/v5/ordinary_operator_kit/prepare_selected.py": "9a2436210a869d815ec3c353250345424d540c6f1b4e765a20c4f8af86bcc6cc",
    "software/v5/ordinary_operator_kit/compatibility.json": "b5a812c90a8edc930a3a1b2859a7f77e5799772a516e1478bb04ae7add7abfe2",
    "software/v5/ordinary_operator_kit/examples.json": "c585172795401aca25a7fabaf9173dcd9ee38f1cdceeed129d13e2e9b6742b3a",
    "software/v5/ordinary_operator_kit/START-HERE.md": "3af7eea96011a18642eb5d3039b47284b2d6dbbcee6c912a821c8e72c654947c",
    "software/v5/ordinary_operator_kit/SELECTED-PACKAGE.md": "365a6d76a36e338cd6dfb7d71daddb8136e63743fb1e395afb169cc89167b63c",
    "software/v5/ordinary_operator_kit/SELECTED-KIT.json": "058d02d095b34b253303f4326f115b65d5046ae990960e828b0260a89f10ca38",
    "software/v5/ordinary_operator_kit/AUTHORING-OFFERS.md": "0954e276c5e6de80e9eb3a66da1ed273bb67f304f5ed84d12bc9c60b158fb2b2",
    "software/v5/ordinary_authoring_offers/CODEC.md": "7a12096fcb7818c823f6cd6f0735b3f1cdfe431d8dd7123c1271445392f93709",
    "software/v5/ordinary_authoring_offers/API.md": "e51d0083c9827210762442733d23e7150dbb5e6ad754615c9cc51b48eb0cbdbb",
}
NEW = tuple("software/v5/ordinary_source_bundle/" + name
            for name in ("bundle.py", "README.md", "LICENSE-STATUS.md"))


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START_WALL < 60 and time.process_time()-START_CPU < 30,
         "CONTROLS_ORIGINAL_ENVELOPE")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, maximum=2*MIB):
    check()
    length = path.stat().st_size
    need(0 < length <= maximum, "CONTROLS_INPUT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == length, "CONTROLS_INPUT_CHANGED")
    return raw


def original_inputs(root):
    """Independent closure: pinned map plus explicit extras, not utility constants."""
    map_raw = read(root/MAP)
    need(digest(map_raw) == EXTRAS[MAP], "CONTROL_EXACT_SOURCE_MAP")
    doc = json.loads(map_raw)
    need(doc["schema"] == "DMKN_ORDINARY_DISTRIBUTION_SOURCE_MAP_V1" and
         len(doc["sources"]) == 84, "CONTROL_84_INPUTS")
    expected = dict(doc["sources"])
    need(not (set(expected) & (set(EXTRAS) | set(NEW))) and len(EXTRAS) == 18,
         "CONTROL_DISJOINT_EXTRAS")
    selected = {}
    for name in sorted(set(expected) | set(EXTRAS) | set(NEW)):
        path = PurePosixPath(name)
        need(not path.is_absolute() and ".." not in path.parts and "\\" not in name,
             "CONTROL_SELECTED_NAME")
        raw = read(root/name)
        pin = dict(bytes=len(raw), sha256=digest(raw))
        if name in expected:
            need(pin == expected[name], "CONTROL_MAP_INPUT_PIN")
        elif name in EXTRAS:
            need(pin["sha256"] == EXTRAS[name], "CONTROL_EXTRA_INPUT_PIN")
        expected[name], selected[name] = pin, raw
    need(len(expected) == 105 and sum(len(raw) for raw in selected.values()) < 8*MIB,
         "CONTROL_ALLOWLIST_BOUND")
    return expected, selected


def manifest_doc(files):
    return dict(schema="DMKN_ORDINARY_SOURCE_DISTRIBUTION_V1",
        claim="EXACT_SOURCE_INPUTS_NOT_BUILD_OR_MATHEMATICAL_ACCEPTANCE", files=files,
        entrypoints=dict(build="software/v5/ordinary_bounded_operations/build.py",
                         overlay="software/v5/ordinary_fair_search/assemble.py",
                         operator="software/v5/ordinary_operator_kit/prepare_selected.py"),
        external_profile=dict(os="Windows x86-64", python="3.14.6", lean="4.34.0"),
        license_status="UNDECIDED_NO_PUBLIC_RELEASE_AUTHORIZATION")


def exercise(args, output, report):
    source = Path(args.bundle_script)
    raw = read(source)
    need(digest(raw) == args.bundle_sha256, "CONTROL_UTILITY_PIN")
    files, selected = original_inputs(Path(args.source_root))
    need(selected[NEW[0]] == raw, "CONTROL_RUNNING_UTILITY_EXACT_BYTES")
    expected_manifest = manifest_doc(files)
    manifest_raw = canonical(expected_manifest)
    # Selected from approved inputs BEFORE pack, not trusted from the archive.
    selected_manifest_sha = digest(manifest_raw)
    report.update(manifest_sha256=selected_manifest_sha,
                  payload_files=len(files), payload_bytes=sum(p["bytes"] for p in files.values()))
    written = 0

    def write(path, value):
        nonlocal written
        check()
        written += len(value)
        need(written <= 48*MIB and not path.exists() and path.is_relative_to(output),
             "CONTROL_FRESH_BOUNDED_WRITE")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(value)

    def completed(label, **details):
        report["cases"].append(dict(name=label, passed=True, **details))

    def refuse(label, call):
        check()
        try:
            call()
        except ValueError as error:
            code = str(error)
            need(code.startswith("SOURCE_BUNDLE_"), "CONTROL_UNEXPECTED_REFUSAL:"+code)
            completed(label, refusal=code)
        else:
            raise AssertionError("CONTROL_EXPECTED_REFUSAL:"+label)

    def fixture(label, *, omit=None, altered=None, added=False, replacement=None):
        root = output/label
        root.mkdir()
        write(root/MANIFEST, manifest_raw)
        for name, value in selected.items():
            if name == omit or name == replacement:
                continue
            if name == altered:
                value = bytes([value[0] ^ 1])+value[1:]
            write(root/name, value)
        if added:
            write(root/"unselected.txt", b"not selected")
        return root

    with ExitStack() as stack:
        for module, name in ((subprocess, "Popen"), (subprocess, "run"), (os, "system"),
                             (socket, "socket"), (socket, "create_connection"), (sqlite3, "connect")):
            stack.enter_context(patch.object(module, name,
                                side_effect=AssertionError("NO_NATIVE_NETWORK_OR_STATE")))
        spec = importlib.util.spec_from_file_location("_selected_source_bundle_controls", source)
        bundle = importlib.util.module_from_spec(spec)
        exec(compile(raw, str(source), "exec", dont_inherit=True), bundle.__dict__)
        write(output/"PRESELECTED-MANIFEST.json", manifest_raw)
        packed = output/"packed"
        receipt = bundle.pack(Path(args.source_root), packed, check=check)
        check()
        archive_raw = read(packed/"source.zip", 9*MIB)
        receipt_raw = read(packed/"RECEIPT.json")
        need(json.loads(receipt_raw) == receipt and
             receipt["schema"] == "DMKN_ORDINARY_SOURCE_BUNDLE_RECEIPT_V1" and
             receipt["status"] == "PACKED_SOURCE_NOT_BUILT" and
             receipt["manifest"] == dict(bytes=len(manifest_raw), sha256=selected_manifest_sha) and
             receipt["archive"] == dict(bytes=len(archive_raw), sha256=digest(archive_raw)) and
             receipt["payload_files"] == 105 and receipt["archive_files"] == 106 and
             receipt["payload_bytes"] == report["payload_bytes"], "CONTROL_EXACT_PACK_RECEIPT")
        completed("actual-pack-exact-preselected-manifest")
        relocated = output/"relocated-source"
        relocated.mkdir()
        expected_members = dict(selected, **{MANIFEST: manifest_raw})
        # Not a generic ZIP extractor: exact known names/content are checked first.
        with zipfile.ZipFile(packed/"source.zip", "r") as archive:
            rows = archive.infolist()
            need(archive.comment == b"" and [row.filename for row in rows] == sorted(expected_members),
                 "CONTROL_ZIP_EXACT_ORDER")
            for row in rows:
                check()
                need(row.date_time == (1980, 1, 1, 0, 0, 0) and
                     row.compress_type == zipfile.ZIP_STORED and row.create_system == 3 and
                     row.external_attr == (0o100644 << 16) and row.flag_bits == 0 and
                     row.extra == b"" and row.comment == b"" and not row.is_dir(),
                     "CONTROL_ZIP_FIXED_METADATA")
                value = archive.read(row)
                need(row.file_size == row.compress_size == len(expected_members[row.filename]) and
                     value == expected_members[row.filename], "CONTROL_ZIP_EXACT_PAYLOAD")
                write(relocated/row.filename, value)
        completed("exact-archive-census-content-deterministic-metadata")
        refuse("existing-pack-output-refused", lambda: bundle.pack(Path(args.source_root), packed, check=check))
        need(read(packed/"source.zip", 9*MIB) == archive_raw and
             read(packed/"RECEIPT.json") == receipt_raw, "CONTROL_NO_OVERWRITE")
        refuse("wrong-manifest-sha-refused", lambda: bundle.verify(relocated, "0"*64, check=check))
        target = "software/v5/ordinary_operator_kit/examples.json"
        tampered = fixture("tampered-source", altered=target)
        refuse("tampered-payload-refused", lambda: bundle.verify(tampered, selected_manifest_sha, check=check))
        missing = fixture("missing-source", omit=target)
        refuse("missing-payload-refused", lambda: bundle.verify(missing, selected_manifest_sha, check=check))
        extra = fixture("extra-source", added=True)
        refuse("extra-payload-refused", lambda: bundle.verify(extra, selected_manifest_sha, check=check))

        for label, bad_name in (("traversal", "../escape.py"), ("absolute", "C:/escape.py"),
                                ("reserved", "software/CON.py"), ("alternate-stream", "software/a:b"),
                                ("trailing-dot", "software/name."), ("backslash", "software\\name.py")):
            changed = deepcopy(expected_manifest)
            changed["files"][bad_name] = changed["files"].pop(target)
            refuse("manifest-"+label+"-refused", lambda changed=changed: bundle.validate_manifest(changed))
        changed = deepcopy(expected_manifest)
        other = "software/v5/ordinary_operator_kit/prepare.py"
        changed["files"][target.upper()] = changed["files"].pop(other)
        refuse("manifest-case-alias-refused", lambda: bundle.validate_manifest(changed))
        changed = deepcopy(expected_manifest)
        changed["files"][target]["bytes"] = True
        refuse("manifest-boolean-size-refused", lambda: bundle.validate_manifest(changed))
        refuse("duplicate-json-key-refused", lambda: bundle.strict_json(b'{"schema":1,"schema":2}'))

        linked = fixture("hardlinked-source", replacement=target)
        link_target = output/"hardlink-target.json"
        write(link_target, selected[target])
        (linked/target).parent.mkdir(parents=True, exist_ok=True)
        os.link(link_target, linked/target)
        need((linked/target).stat().st_nlink == 2, "CONTROL_REAL_HARDLINK")
        refuse("actual-hardlinked-payload-refused", lambda: bundle.verify(linked, selected_manifest_sha, check=check))
        # A privilege limitation is disclosed, never mistaken for a refusal pass.
        symlink_target = output/"symlink-target.json"
        write(symlink_target, selected[target])
        symbolic = fixture("symlinked-source", replacement=target)
        (symbolic/target).parent.mkdir(parents=True, exist_ok=True)
        try:
            os.symlink(symlink_target, symbolic/target)
        except OSError as error:
            need(getattr(error, "winerror", None) == 1314, "CONTROL_UNEXPECTED_SYMLINK_FAILURE")
            report["not_executed"].append(dict(name="actual-symlinked-payload-refusal",
                                                reason="WINDOWS_PRIVILEGE_NOT_HELD", winerror=1314))
        else:
            need(stat.S_ISLNK((symbolic/target).lstat().st_mode), "CONTROL_REAL_SYMLINK")
            refuse("actual-symlinked-payload-refused", lambda: bundle.verify(symbolic, selected_manifest_sha, check=check))
        after_files, after_selected = original_inputs(Path(args.source_root))
        need(after_files == files and after_selected == selected, "CONTROL_ORIGINAL_INPUTS_UNCHANGED")
        completed("all105-original-source-inputs-unchanged")
        report.update(pack_receipt=receipt, product_execution=False)
    # The sole allowed child is the exact extracted, source-only public verifier.
    # It is outside the traps above, with no new allowance or successful fallback.
    check()
    argv = [sys.executable, "-I", "-S", "-B", str(relocated/NEW[0]), "verify",
            "--source-root", str(relocated), "--manifest-sha256", selected_manifest_sha]
    write(output/"PUBLIC-VERIFY-COMMAND.json", canonical(dict(argv=argv, cwd=str(output), attempts=1)))
    remaining = 60-(time.monotonic()-START_WALL)-2
    need(remaining > 0, "CONTROL_NO_CLI_ALLOWANCE_REMAINING")
    process = None
    with (output/"verify-stdout.txt").open("xb") as stdout, \
            (output/"verify-stderr.txt").open("xb") as stderr:
        try:
            process = subprocess.Popen(argv, cwd=output, stdin=subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
            returncode = process.wait(timeout=remaining)
        finally:
            if process is not None and process.poll() is None:
                process.kill()
                process.wait(timeout=max(0.001, min(2, 60-(time.monotonic()-START_WALL))))
            report["public_verifier_reaped"] = process is not None and process.poll() is not None
    need(returncode == 0 and report["public_verifier_reaped"] and
         (output/"verify-stderr.txt").stat().st_size == 0, "CONTROL_PUBLIC_VERIFY_FAILED")
    observed = json.loads(read(output/"verify-stdout.txt", MIB))
    need(observed["status"] == "VERIFIED_EXACT_SOURCE_NOT_BUILT" and
         observed["manifest"] == receipt["manifest"] and observed["payload_files"] == 105 and
         observed["payload_bytes"] == report["payload_bytes"], "CONTROL_RELOCATED_VERIFY")
    write(output/"RELOCATED-VERIFICATION.json", canonical(observed))
    expected_dirs = {p.as_posix() for name in expected_members
                     for p in PurePosixPath(name).parents if p.as_posix() != "."}
    actual_files, actual_dirs = set(), set()
    for path in relocated.rglob("*"):
        check()
        name = path.relative_to(relocated).as_posix()
        need(not path.is_symlink() and not getattr(path.lstat(), "st_file_attributes", 0) & 0x400,
             "CONTROL_EXTRACTED_REDIRECTION")
        (actual_dirs if path.is_dir() else actual_files).add(name)
    need(actual_files == set(expected_members) and actual_dirs == expected_dirs,
         "CONTROL_NO_UNSELECTED_FILES_OR_PYCACHE")
    completed("actual-relocated-public-cli-verification")
    need(len(report["cases"]) == 20-len(report["not_executed"]) and
         len({row["name"] for row in report["cases"]}) == len(report["cases"]), "CONTROL_CASE_CENSUS")
    report.update(relocated_verification=observed, fixture_bytes_written=written,
                  public_verifier_attempts=1,
                  cpu_scope="HARNESS_PROCESS_CPU_ONLY;OUTER_JOB_INCLUDES_PUBLIC_VERIFIER")
    check()


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("source-root", "bundle-script", "bundle-sha256", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTROL_ISOLATED_CANONICAL_INVOCATION")
    need(Path(args.source_root) == ROOT and Path(args.bundle_script).is_absolute() and
         output.is_absolute() and output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         not output.exists() and output.parent.is_dir() and output.parent.resolve(strict=True) == output.parent,
         "CONTROL_FRESH_OUTPUT_AND_SOURCE_SCOPE")
    output.mkdir()
    report = dict(passed=False, cases=[], not_executed=[],
                  scope="OFFLINE_SOURCE_DISTRIBUTION_NOT_BUILD_OR_MATHEMATICS")
    try:
        exercise(args, output, report)
        report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:1000])
    report.update(completed_cases=len(report["cases"]), wall_seconds=time.monotonic()-START_WALL,
                  harness_cpu_seconds=time.process_time()-START_CPU)
    raw = canonical(report)
    need(len(raw) <= MIB, "CONTROL_RESULT_BOUND")
    with (output/"RESULT.json").open("xb") as stream:
        stream.write(raw+b"\n")
    print(raw.decode("utf-8"))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""One bounded coherent-source pack/relocation; no native or network work.

Root selects exact sources and execution separately. Test mutations are fresh
synthetic fixtures, never edits to previously used source or evidence.
"""
from __future__ import annotations

import time
START, CPU = time.monotonic(), time.process_time()
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import urllib.parse
import zipfile

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
DEADLINE = START+110
BASE_ARCHIVE_SHA = "897a6eb57056b911b200551413c65ce7788ba3d448ff8b6b8c143d883180ebd0"
BASE_MANIFEST_SHA = "f1beab01d43e4b5fc6d7b9999ff2795598e3f2ee77c0dc85f1d99e82a15b31f1"
BASE_UTILITY_SHA = "5a8742bec0c13f3c7e8104111ba883887d5569cbb1a5498d79567e998dcd4d32"
UNION_MANIFEST = "WORKFLOW-SOURCE-MANIFEST.json"
BASE_MANIFEST = "BASE-SOURCE-MANIFEST.json"
UTILITY = "software/v5/ordinary_workflow_bundle/bundle.py"
NEW_SOURCES = {
    "software/v5/ordinary_selected_export/export.py": "software/v5/ordinary_selected_export/export.py",
    "software/v5/ordinary_selected_export/selected_export.py": "software/v5/ordinary_selected_export/selected_export.py",
    "software/v5/ordinary_selected_export/README.md": "software/v5/ordinary_workflow_bundle/guides/SELECTED-EXPORT.md",
    "software/v5/ordinary_selected_export/INTAKE.md": "software/v5/ordinary_selected_export/INTAKE.md",
    "software/v5/ordinary_reuse_workflow/README.md": "software/v5/ordinary_reuse_workflow/README.md",
    "software/v5/UPDATE-AND-RECOVERY.md": "software/v5/ordinary_workflow_bundle/guides/UPDATE-AND-RECOVERY.md",
    "software/v5/ordinary_service_plan/service_plan.py": "software/v5/ordinary_service_plan/service_plan.py",
    "software/v5/ordinary_service_plan/README.md": "software/v5/ordinary_workflow_bundle/guides/SERVICE-PLAN.md",
    UTILITY: UTILITY,
    "START-HERE.md": "software/v5/ordinary_workflow_bundle/README.md",
}
GUIDES = ("START-HERE.md", "software/v5/ordinary_selected_export/README.md",
          "software/v5/ordinary_selected_export/INTAKE.md", "software/v5/ordinary_reuse_workflow/README.md",
          "software/v5/UPDATE-AND-RECOVERY.md", "software/v5/ordinary_service_plan/README.md")


def need(condition, code):
    if not condition:
        raise AssertionError(code)


def check():
    need(time.monotonic() < DEADLINE and time.process_time()-CPU < 45,
         "WORKFLOW_TEST_ORIGINAL_ENVELOPE")


def read(path, maximum=16*MIB):
    check()
    with Path(path).open("rb") as stream:
        raw = stream.read(maximum+1)
    need(0 < len(raw) <= maximum, "WORKFLOW_TEST_READ_BOUND")
    return raw


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(raw):
    return dict(bytes=len(raw), sha256=digest(raw))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def fresh(path, raw):
    need(type(raw) is bytes and len(raw) <= 16*MIB, "WORKFLOW_TEST_WRITE_BOUND")
    with Path(path).open("xb") as stream:
        stream.write(raw)


def save(path, value):
    fresh(path, canonical(value))


def load_source(path, expected, name="_workflow_test_subject"):
    raw = read(path, 2*MIB)
    need(digest(raw) == expected, "WORKFLOW_TEST_SOURCE_PIN")
    need(name not in sys.modules, "WORKFLOW_TEST_MODULE_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def archive_members(raw, expected_count):
    need(len(raw) <= 16*MIB, "WORKFLOW_TEST_ARCHIVE_BOUND")
    values = {}
    with zipfile.ZipFile(io.BytesIO(raw), "r") as archive:
        rows = archive.infolist()
        need(len(rows) == expected_count and archive.comment == b"" and
             [row.filename for row in rows] == sorted(row.filename for row in rows),
             "WORKFLOW_TEST_ARCHIVE_CENSUS")
        total = 0
        for row in rows:
            check()
            name, path = row.filename, PurePosixPath(row.filename)
            need(not path.is_absolute() and path.as_posix() == name and
                 all(part not in ("", ".", "..") and "\\" not in part and ":" not in part
                     for part in path.parts) and name not in values and
                 name.casefold() not in {key.casefold() for key in values},
                 "WORKFLOW_TEST_MEMBER_NAME")
            need(row.date_time == (1980, 1, 1, 0, 0, 0) and row.create_system == 3 and
                 row.external_attr == 0o100644 << 16 and row.compress_type == zipfile.ZIP_STORED and
                 row.extra == row.comment == b"" and row.flag_bits == 0 and
                 0 < row.file_size == row.compress_size <= 2*MIB, "WORKFLOW_TEST_MEMBER_METADATA")
            total += row.file_size
            need(total <= 8*MIB, "WORKFLOW_TEST_EXPANDED_BOUND")
            values[name] = archive.read(row)
            need(len(values[name]) == row.file_size, "WORKFLOW_TEST_MEMBER_READBACK")
    return values


def extract(values, destination):
    need(not destination.exists() and destination.parent.is_dir(), "WORKFLOW_TEST_FRESH_EXTRACTION")
    destination.mkdir()
    for name, raw in sorted(values.items()):
        check()
        target = destination.joinpath(*PurePosixPath(name).parts)
        need(target.is_relative_to(destination), "WORKFLOW_TEST_EXTRACT_BOUNDARY")
        target.parent.mkdir(parents=True, exist_ok=True)
        fresh(target, raw)
    return census(destination, values)


def census(root, values):
    expected_dirs = {parent.as_posix() for name in values for parent in PurePosixPath(name).parents
                     if parent.as_posix() != "."}
    files, dirs, pending = {}, set(), [root]
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as listing:
            for item in listing:
                check()
                name = Path(item.path).relative_to(root).as_posix()
                info = item.stat(follow_symlinks=False)
                need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0)&0x400,
                     "WORKFLOW_TEST_REDIRECTED_EXTRACTION")
                if stat.S_ISDIR(info.st_mode):
                    dirs.add(name); pending.append(Path(item.path))
                else:
                    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and name in values,
                         "WORKFLOW_TEST_EXTRA_FILE")
                    raw = read(item.path, 2*MIB)
                    need(raw == values[name], "WORKFLOW_TEST_EXACT_EXTRACTED_BYTES")
                    files[name] = pin(raw)
                need(len(files)+len(dirs) <= 256, "WORKFLOW_TEST_CENSUS_BOUND")
    need(set(files) == set(values) and dirs == expected_dirs, "WORKFLOW_TEST_FULL_CENSUS")
    return dict(files=len(files), directories=len(dirs), bytes=sum(row["bytes"] for row in files.values()),
                map_sha256=digest(canonical(files)))


def cli(output, label, entry, tokens, expected_exit=0):
    argv = [sys.executable, "-I", "-S", "-B", str(entry), *tokens]
    save(output/(label+"-COMMAND.json"), dict(argv=argv, cwd=str(ROOT), attempts=1))
    with (output/(label+".stdout")).open("xb") as stdout, \
            (output/(label+".stderr")).open("xb") as stderr:
        child = subprocess.Popen(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=stdout,
                                 stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            code = child.wait(timeout=max(1, min(65, DEADLINE-time.monotonic()-5)))
        except BaseException:
            if child.poll() is None:
                child.kill(); child.wait(timeout=5)
            raise
    need(code == expected_exit, "WORKFLOW_TEST_PUBLIC_EXIT:"+label)
    return json.loads(read(output/(label+".stdout"), 2*MIB)) if code == 0 else dict(
        exit_code=code, stderr=read(output/(label+".stderr"), 2*MIB).decode("utf-8", "replace")[-1500:])


def refuses(call, label):
    check()
    try:
        call()
    except ValueError as error:
        return dict(case=label, error=str(error)[:350])
    raise AssertionError("WORKFLOW_TEST_UNEXPECTED_ACCEPTANCE:"+label)


def document_closure(root, members, doc, base_doc):
    links, scripts = [], []
    for guide in GUIDES:
        text = members[guide].decode("utf-8")
        # Deliberately a bounded check of inline links in the six selected
        # operational guides, not a complete CommonMark/anchor parser.
        for raw in re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", text):
            target = raw.strip()
            need(not target.startswith("<") and not re.search(r'\s+[\"\']', target),
                 "WORKFLOW_TEST_UNSUPPORTED_LINK_SYNTAX")
            parsed = urllib.parse.urlsplit(target)
            if parsed.scheme or parsed.netloc:
                need(parsed.scheme in ("https", "http"), "WORKFLOW_TEST_UNSUPPORTED_EXTERNAL_LINK")
                links.append(dict(guide=guide, target=target, scope="external-reference-not-fetched"))
                continue
            if not parsed.path:
                continue
            resolved = (root/guide).parent.joinpath(urllib.parse.unquote(parsed.path)).resolve()
            need(resolved.is_relative_to(root), "WORKFLOW_TEST_DOC_LINK_ESCAPES")
            destination = resolved.relative_to(root).as_posix()
            need(destination in members, "WORKFLOW_TEST_MISSING_OPERATIONAL_LINK:"+guide+":"+target)
            links.append(dict(guide=guide, target=target, delivered=destination))
        for selected in re.findall(r"software[/\\]v5(?:[/\\][A-Za-z0-9_.-]+)+\.py", text):
            normalized = selected.replace("\\", "/")
            need(normalized in members, "WORKFLOW_TEST_MISSING_SOURCE_COMMAND:"+normalized)
            scripts.append(dict(guide=guide, source=normalized))
    entries = {"workflow:"+key: value for key, value in doc["entrypoints"].items()}
    entries.update({"base:"+key: value for key, value in base_doc["entrypoints"].items()})
    need(all(value in members for value in entries.values()), "WORKFLOW_TEST_MISSING_ENTRYPOINT")
    need(len(links) >= 12 and len(scripts) >= 1, "WORKFLOW_TEST_DOCUMENT_SCAN_EMPTY")
    return dict(guides=list(GUIDES), inline_links=links, explicit_source_scripts=scripts,
        entrypoints=entries,
        scope="SELECTED_OPERATIONAL_INLINE_FILE_LINKS_AND_EXPLICIT_SOURCE_COMMAND_PATHS;ANCHORS_AND_PROSE_REVIEW_SEPARATE",
        historical_base_evidence_links="ARCHIVAL_NOT_RECURSIVELY_PACKED_OR_TESTED")


def manifest_controls(helper, base, doc, original, relocated, source_root, base_raw):
    cases = []
    changed = deepcopy(doc); changed["base_manifest"]["sha256"] = "0"*64
    cases.append(refuses(lambda: helper.validate_manifest(base, changed, original), "wrong-base-association"))
    changed = deepcopy(doc); changed["files"][next(iter(original))]["sha256"] = "0"*64
    cases.append(refuses(lambda: helper.validate_manifest(base, changed, original), "changed-base-projection"))
    changed = deepcopy(doc); changed["files"]["software/v5/ordinary_service_plan/service_plan.py"]["sha256"] = "0"*64
    cases.append(refuses(lambda: helper.validate_manifest(base, changed, original), "changed-approved-companion"))
    changed = deepcopy(doc); del changed["files"]["software/v5/ordinary_selected_export/selected_export.py"]
    cases.append(refuses(lambda: helper.validate_manifest(base, changed, original), "missing-adjacent-export-code"))
    changed = deepcopy(doc)
    changed["files"]["SOURCE-MANIFEST.json"] = changed["files"].pop(BASE_MANIFEST)
    cases.append(refuses(lambda: helper.validate_manifest(base, changed, original), "competing-old-root-manifest"))
    changed = deepcopy(doc)
    changed["files"]["extra-guide.md"] = changed["files"].pop("START-HERE.md")
    cases.append(refuses(lambda: helper.validate_manifest(base, changed, original), "extra-replaces-required-guide"))
    changed = deepcopy(doc); changed["entrypoints"]["verify"] = "software/v5/ordinary_release_bundle/bundle.py"
    cases.append(refuses(lambda: helper.validate_manifest(base, changed, original), "wrong-full-root-verifier"))
    cases.append(refuses(lambda: helper.base_files(base, base_raw+b"\n", source_root, check),
                         "wrong-exact-base-manifest-bytes"))
    cases.append(refuses(lambda: helper.verify(relocated, BASE_MANIFEST_SHA, check=check),
                         "base-hash-is-not-union-selection"))
    return dict(group="new_union_manifest_boundaries", refusals=cases)


def helper_bootstrap_controls(source_raw, output):
    cases = []
    for label, bad_helper in (
        ("length", b"raise AssertionError('UNAPPROVED_HELPER_EXECUTED')\n"),
        ("hash", b"raise AssertionError('UNAPPROVED_HELPER_EXECUTED')\n".ljust(22041, b" ")),
    ):
        fixture = output/("bootstrap-"+label)
        entry = fixture/UTILITY
        old_helper = fixture/"software/v5/ordinary_release_bundle/bundle.py"
        entry.parent.mkdir(parents=True)
        old_helper.parent.mkdir(parents=True)
        fresh(entry, source_raw); fresh(old_helper, bad_helper)
        subject = load_source(entry, digest(source_raw), "_workflow_bootstrap_"+label)
        result = refuses(subject.helper, "unapproved-helper-"+label)
        need("BOOTSTRAP_"+("LENGTH" if label == "length" else "PIN") in result["error"],
             "WORKFLOW_TEST_HELPER_REJECTED_BEFORE_EXEC")
        cases.append(result)
    return dict(group="new_pinned_helper_bootstrap", refusals=cases,
                scope="FRESH_SYNTHETIC_HELPER_BYTES;NO_UNAPPROVED_HELPER_EXECUTION")


def scenario(args, output, report):
    source, source_root = Path(args.source), Path(args.source_root)
    need(source_root.is_absolute() and source_root.resolve(strict=True) == source_root and
         source == source_root/UTILITY, "WORKFLOW_TEST_EXPLICIT_SOURCE_ROOT")
    helper = load_source(source, args.source_sha256)
    need(helper.SOURCES == NEW_SOURCES and helper.COUNT == 154 and helper.UTILITY == UTILITY and
         helper.MANIFEST == UNION_MANIFEST and helper.BASE_MANIFEST == BASE_MANIFEST,
         "WORKFLOW_TEST_EXACT_NEW_MAP")
    base_raw_zip = read(args.base_archive)
    need(digest(base_raw_zip) == BASE_ARCHIVE_SHA, "WORKFLOW_TEST_APPROVED_BASE_ARCHIVE")
    base_members = archive_members(base_raw_zip, 144)
    base_raw = base_members.pop("SOURCE-MANIFEST.json")
    need(digest(base_raw) == BASE_MANIFEST_SHA and len(base_members) == 143,
         "WORKFLOW_TEST_APPROVED_BASE_MANIFEST")
    base_doc = json.loads(base_raw)
    original = base_doc["files"]
    need(set(original) == set(base_members) and all(pin(raw) == original[name]
         for name, raw in base_members.items()), "WORKFLOW_TEST_COMPLETE_BASE_PROJECTION_INPUT")
    need(digest(base_members["software/v5/ordinary_release_bundle/bundle.py"]) == BASE_UTILITY_SHA,
         "WORKFLOW_TEST_APPROVED_BASE_HELPER")
    base_path = output/"base-manifest.json"; fresh(base_path, base_raw)
    packed = cli(output, "pack", source, ["pack", "--source-root", str(source_root),
        "--base-manifest", str(base_path), "--output", str(output/"packed")])
    need(packed == json.loads(read(output/"packed"/"RECEIPT.json")), "WORKFLOW_TEST_RECEIPT_AGREEMENT")
    archive_raw = read(output/"packed"/"source.zip")
    members = archive_members(archive_raw, 155)
    manifest_raw = members[UNION_MANIFEST]
    doc = json.loads(manifest_raw)
    need(canonical(doc) == manifest_raw and
         packed["schema"] == "DMKN_ORDINARY_WORKFLOW_SOURCE_BUNDLE_RECEIPT_V1" and
         packed["status"] == "PACKED_WORKFLOW_SOURCE_NOT_BUILT" and
         packed["archive"] == pin(archive_raw) and
         packed["manifest"] == pin(manifest_raw) and packed["payload_files"] == 154 and
         packed["archive_files"] == 155 and packed["base_manifest_sha256"] == BASE_MANIFEST_SHA and
         packed["payload_bytes"] == sum(len(raw) for name, raw in members.items() if name != UNION_MANIFEST) and
         members[BASE_MANIFEST] == base_raw, "WORKFLOW_TEST_COMPLETE_NEW_RECEIPT")
    need(set(members) == set(base_members) | set(NEW_SOURCES) | {BASE_MANIFEST, UNION_MANIFEST},
         "WORKFLOW_TEST_COMPLETE_NEW_ALLOWLIST")
    need(set(doc["files"]) == set(members)-{UNION_MANIFEST} and
         all(doc["files"][name] == pin(raw) for name, raw in members.items() if name != UNION_MANIFEST),
         "WORKFLOW_TEST_COMPLETE_NEW_MANIFEST")
    need(all(members[name] == raw for name, raw in base_members.items()),
         "WORKFLOW_TEST_143_BASE_BYTES_PRESERVED")
    mapping = {}
    for destination, selected in NEW_SOURCES.items():
        raw = read(source_root/selected, 2*MIB)
        need(members[destination] == raw, "WORKFLOW_TEST_NEW_SOURCE_MAPPING:"+destination)
        mapping[destination] = dict(source=selected, **pin(raw))
    report["groups"].append(dict(group="actual_pack_complete_union_and_base_projection", receipt=packed,
        exact_base_payloads=143, new_source_mapping=mapping, old_root_manifest_absent="SOURCE-MANIFEST.json" not in members))
    relocated = output/"relocated-workflow"
    before = extract(members, relocated)
    verification = cli(output, "relocated-verify", relocated/UTILITY,
                       ["verify", "--source-root", str(relocated), "--manifest-sha256", digest(manifest_raw)])
    need(verification["status"] == "VERIFIED_EXACT_WORKFLOW_SOURCE_NOT_BUILT" and
         verification["manifest"] == pin(manifest_raw) and verification["payload_files"] == 154,
         "WORKFLOW_TEST_RELOCATED_VERIFIER")
    after = census(relocated, members)
    need(before == after, "WORKFLOW_TEST_RELOCATED_NO_WRITES")
    report["groups"].append(dict(group="relocated_public_verification_and_exact_census",
                                 before=before, after=after, verification=verification))
    report["groups"].append(dict(group="current_operational_document_file_closure",
        **document_closure(relocated, members, doc, base_doc)))
    base = helper.helper()
    need(helper.validate_manifest(base, doc, original) == doc["files"], "WORKFLOW_TEST_POSITIVE_MANIFEST_API")
    report["groups"].append(manifest_controls(helper, base, doc, original, relocated, source_root, base_raw))
    report["groups"].append(helper_bootstrap_controls(members[UTILITY], output))
    bad = output/"extra-member-workflow"
    extract(members, bad)
    fresh(bad/"UNSELECTED.txt", b"Fresh inert extra-member refusal fixture.\n")
    extra = refuses(lambda: helper.verify(bad, digest(manifest_raw), check=check), "extra-union-root-member")
    need("EXTRA_OR_ALIASED_FILE" in extra["error"], "WORKFLOW_TEST_ACTUAL_CENSUS_REFUSAL")
    report["groups"].append(dict(group="complete_union_extra_member_refusal", result=extra,
        preserved_fixture=str(bad), original_relocated_census=census(relocated, members)))
    need(read(args.base_archive) == base_raw_zip and read(source, 2*MIB) == members[UTILITY],
         "WORKFLOW_TEST_INPUTS_STABLE")
    return report


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and Path.cwd() == ROOT,
         "WORKFLOW_TEST_PROFILE")
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for option in ("source", "source-sha256", "source-root", "base-archive", "output"):
        parser.add_argument("--"+option, required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(output.is_absolute() and output.parent.is_dir() and not output.exists(),
         "WORKFLOW_TEST_FRESH_OUTPUT")
    output.mkdir()
    report = dict(status="RUNNING", groups=[], scope="SOURCE_DISTRIBUTION_NOT_NATIVE_MATH_OR_NETWORK")
    try:
        scenario(args, output, report)
        check(); report["status"] = "PASS"
    except BaseException as error:
        report.update(status="FAILED", error_type=type(error).__name__, error=str(error)[:1600])
    report.update(wall_seconds=time.monotonic()-START, controller_cpu_seconds=time.process_time()-CPU)
    save(output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True, ensure_ascii=True, allow_nan=False), flush=True)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

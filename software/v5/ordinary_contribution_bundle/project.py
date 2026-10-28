"""Project explicitly selected public contribution bytes into an inert bundle.

Only five pinned inert codecs execute. No owner, database, native artifact,
network, dependency traversal or mathematical acceptance is involved. Report
paths and success/cleanup claims are data, never execution or trust authority.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import stat
import sys
import time

MIB = 1024**2
METADATA_MAX = 2*MIB
UNIT_COUNT_MAX = 32
EVIDENCE_MAX = 4*MIB
TARGET_COUNT_MAX = 32
WALL_SECONDS = 60
CPU_SECONDS = 30
RECEIPT_SCHEMA = "DMKN_ORDINARY_PUBLICATION_BUNDLE_PREPARATION_V1"
STATUS = "INERT_PUBLICATION_BUNDLE_PREPARED"
APPEND_SCHEMA = "DMKN_INCREMENTAL_HOST_APPEND_V1"
STATUSES = {
    "contribute": "CHECKED_CONTRIBUTION_WITH_DURABLE_PUBLICATION_BYTES",
    "complete": "CHECKED_COMPLETION_WITH_DURABLE_PUBLICATION_BYTES",
}
CODECS = (
    ("ordinary_evidence", "installation/py/ordinary_evidence.py", 17058,
     "fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6"),
    ("ordinary_semantics", "installation/py/ordinary_semantics.py", 10283,
     "ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915"),
    ("portable_evidence", "installation/py/portable_evidence.py", 2993,
     "f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8"),
    ("portable_candidate", "authoring/py/portable_candidate.py", 10437,
     "29ae111a362472b09b2b1ff16b567b352be793d76c2cd1b5421e0aee29219331"),
    ("baseline_bundle", "reference/baseline_bundle.py", 21363,
     "e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6"),
)
BUNDLE_LIMITS = {
    "max_units": UNIT_COUNT_MAX, "max_bytes": EVIDENCE_MAX,
    "max_unit_bytes": EVIDENCE_MAX, "max_nodes": 131072,
    "max_names": 4096, "max_edges": 32768,
    "max_targets": TARGET_COUNT_MAX, "max_batch_units": UNIT_COUNT_MAX,
    "max_batch_bytes": EVIDENCE_MAX, "max_batch_nodes": 131072,
    "max_batch_names": 4096, "max_batch_edges": 32768,
}


def need(condition, code):
    if not condition:
        raise ValueError("PROJECTION_" + code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def identifier(value):
    need(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None,
         "IDENTIFIER")
    return value


def integer(value, minimum, maximum):
    need(type(value) is int and minimum <= value <= maximum, "INTEGER_BOUND")
    return value


def fields(value, names):
    need(type(value) is dict and set(value) == set(names), "FIELDS")


def ordinary_path(value, *, directory=False, fresh=False):
    """Inspect only caller-selected path ancestry, never enumerate directories."""
    need(isinstance(value, (str, Path)), "PATH_TYPE")
    path = Path(value)
    need(path.is_absolute() and path != Path(path.anchor) and
         ".." not in path.parts and len(path.parts) <= 128 and
         len(str(path)) <= 32768 and not str(path).startswith(("\\\\", "//")),
         "ABSOLUTE_LOCAL_PATH")
    for part in path.parts[1:]:
        need(part not in (".", "..") and not part.endswith((".", " ")) and
             not any(ord(char) < 32 or char in ':*?"<>|' for char in part) and
             not (os.name == "nt" and os.path.isreserved(part)), "PATH_COMPONENT")
    for part in (*reversed(path.parents), path):
        if fresh and part == path:
            need(not os.path.lexists(part), "OUTPUT_EXISTS")
            continue
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if part != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PATH_KIND")
    return path


def separate(left, right):
    need(not left.is_relative_to(right) and not right.is_relative_to(left),
         "OUTPUT_OVERLAP")


def read(path, maximum, check):
    check()
    path = ordinary_path(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "INPUT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    check()
    need(len(raw) == size and path.stat().st_size == size, "INPUT_CHANGED")
    return raw


def strict_report(raw):
    """Bound metadata JSON depth/numbers; product codecs own portable syntax."""
    need(type(raw) is bytes and 0 < len(raw) <= METADATA_MAX, "METADATA_BOUND")
    depth, quoted, escaped = 0, False, False
    for byte in raw:
        if quoted:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
        elif byte == 34:
            quoted = True
        elif byte in (91, 123):
            depth += 1
            need(depth <= 64, "JSON_DEPTH")
        elif byte in (93, 125):
            depth -= 1
            need(depth >= 0, "JSON_DEPTH")

    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "JSON_DUPLICATE_KEY")
            result[key] = value
        return result

    def parse_int(token):
        need(len(token) <= 20, "JSON_INTEGER")
        return int(token)

    def parse_float(token):
        need(len(token) <= 64, "JSON_FLOAT")
        value = float(token)
        need(math.isfinite(value), "JSON_NONFINITE")
        return value

    def reject_constant(_token):
        raise ValueError("PROJECTION_JSON_NONFINITE")

    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_int=parse_int, parse_float=parse_float,
                      parse_constant=reject_constant)


def encoded(document):
    raw = json.dumps(document, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":")).encode("ascii")
    need(0 < len(raw) <= METADATA_MAX, "OUTPUT_METADATA_BOUND")
    return raw


@contextmanager
def selected_modules(package, profile, check):
    """Capture/hash only fixed inert sources; restore temporary import slots."""
    need(type(profile) is dict and
         profile.get("schema") == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
         type(profile.get("files")) is dict, "PROFILE_SCHEMA")
    sources = []
    for name, role, size, pin in CODECS:
        check()
        expected = {"bytes": size, "sha256": pin}
        # Installation codecs belong to the separately pinned installation
        # manifest, not PROFILE.files. Authenticate their captured bytes below;
        # opening the full installation/native loader is unnecessary here.
        if not role.startswith("installation/"):
            need(profile["files"].get(role) == expected, "PROFILE_CODEC_PIN:" + name)
        path = package / role
        raw = read(path, MIB, check)
        need(len(raw) == size and digest(raw) == pin, "CODEC_PIN:" + name)
        sources.append((name, path, raw))
    sentinel = object()
    previous = {name: sys.modules.get(name, sentinel) for name, _, _ in sources}
    modules = {}
    try:
        for name, path, raw in sources:
            check()
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
            modules[name] = module
        yield modules
    finally:
        for name, previous_module in previous.items():
            if previous_module is sentinel:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = previous_module


def publication_result(document):
    """Recognize two explicit layouts; saved success claims remain untrusted."""
    need(type(document) is dict, "REPORT_OBJECT")
    if "operation" in document or "result" in document:
        operation = document.get("operation")
        need(operation in STATUSES and type(document.get("result")) is dict,
             "WRAPPER_LAYOUT")
        result = document["result"]
        need(result.get("status") == STATUSES[operation], "WRAPPER_RESULT_STATUS")
        layout = "owner-wrapper"
        reported_profile = document.get("profile_sha256")
        if reported_profile is not None:
            identifier(reported_profile)
        provenance = {"reported_profile_sha256": reported_profile,
            "reported_ok": document.get("ok"),
            "reported_close_errors": document.get("close_errors"),
            "reported_final_budget_error": document.get("final_budget_error")}
    else:
        matches = [operation for operation, status in STATUSES.items()
                   if document.get("status") == status]
        need(len(matches) == 1, "HELPER_RESULT_STATUS")
        operation, result, layout = matches[0], document, "helper-result"
        provenance = {"reported_profile_sha256": None, "reported_ok": None,
                      "reported_close_errors": None, "reported_final_budget_error": None}
    semantic = identifier(result.get("semantic_id"))
    # These identifiers describe the saved source event, not a current warrant.
    provenance.update(parent_root=identifier(result.get("parent_root")),
        local_root=identifier(result.get("local_root")),
        implementation_id=identifier(result.get("implementation_id")),
        reported_status=result["status"], original_closure_verified=False)
    return operation, layout, semantic, result, provenance


def project_selected(package, profile_sha256, report, report_sha256,
                     evidence_directory, output, *, share_all_bundle=False,
                     allow_partial_publication=False):
    """Prepare a fresh file-only bundle; retain any partial output on failure.

    One cooperative 60-wall/30-CPU-second allowance spans the entire invocation.
    It is not OS process containment. Inputs and source paths are owner-controlled;
    the caller serializes any concurrent mutation. No native runtime is required.
    """
    started, cpu_started = time.monotonic(), time.process_time()

    def check():
        need(time.monotonic()-started < WALL_SECONDS and
             time.process_time()-cpu_started < CPU_SECONDS, "ALLOWANCE_EXHAUSTED")

    check()
    need(share_all_bundle is True and allow_partial_publication is True,
         "EXPLICIT_DISCLOSURE_REQUIRED")
    package = ordinary_path(package, directory=True)
    report = ordinary_path(report)
    evidence_directory = ordinary_path(evidence_directory, directory=True)
    output = ordinary_path(output, directory=True, fresh=True)
    for protected in (package, report, evidence_directory, Path(__file__).absolute().parent):
        separate(output, protected)
    profile_sha256, report_sha256 = identifier(profile_sha256), identifier(report_sha256)
    profile_path = package / "PROFILE.json"
    profile_raw, report_raw = read(profile_path, METADATA_MAX, check), read(report, METADATA_MAX, check)
    need(digest(profile_raw) == profile_sha256, "PROFILE_PIN")
    need(digest(report_raw) == report_sha256, "REPORT_PIN")
    profile, document = strict_report(profile_raw), strict_report(report_raw)
    operation, layout, semantic, result, provenance = publication_result(document)
    rows, targets = result.get("units"), result.get("targets")
    need(type(rows) is list and 1 <= len(rows) <= UNIT_COUNT_MAX, "UNIT_COUNT")
    need(type(targets) is list and 1 <= len(targets) <= TARGET_COUNT_MAX, "TARGET_COUNT")
    unit_pins, raws, parsed_units, total_bytes = [], [], {}, 0
    with selected_modules(package, profile, check) as modules:
        E, S, PE, B = (modules[name] for name in
                      ("ordinary_evidence", "ordinary_semantics", "portable_evidence", "baseline_bundle"))
        need(semantic == S.semantic_id(), "REPORT_SEMANTICS")
        limits = B.Limits(**BUNDLE_LIMITS)
        for row in rows:
            check()
            fields(row, {"unit_id", "file", "bytes", "sha256"})
            uid, pin = identifier(row["unit_id"]), identifier(row["sha256"])
            size = integer(row["bytes"], 1, EVIDENCE_MAX)
            need(type(row["file"]) is str and 0 < len(row["file"]) <= 32768,
                 "REPORTED_FILE_TEXT")
            need(uid not in parsed_units, "DUPLICATE_UNIT")
            need(total_bytes + size <= EVIDENCE_MAX, "EVIDENCE_TOTAL")
            # The report's file field is never a filesystem input, even locally.
            raw = read(evidence_directory / (uid + ".json"), size, check)
            need(len(raw) == size and digest(raw) == pin, "EVIDENCE_PIN")
            parsed = PE.read_evidence(raw)
            check()
            need(parsed.unit_id == uid and parsed.document["semantic_id"] == semantic,
                 "EVIDENCE_IDENTITY_OR_SEMANTICS")
            unit_pins.append({"unit_id": uid, "raw_bytes": size, "raw_sha256": pin})
            raws.append(raw)
            parsed_units[uid] = parsed
            total_bytes += size

        seen_names, seen_exports = set(), set()
        for target in targets:
            check()
            fields(target, {"name", "unit_id", "export_id"})
            key = E.name_key(target["name"])
            uid, eid = identifier(target["unit_id"]), identifier(target["export_id"])
            need(key not in seen_names and eid not in seen_exports, "DUPLICATE_TARGET")
            seen_names.add(key)
            seen_exports.add(eid)
            need(uid in parsed_units and key in parsed_units[uid].census.expected_names and
                 S.export_id(semantic, uid, target["name"]) == eid, "TARGET_BINDING")
        batches = B.split_units(raws, limits=limits, check_budget=check)
        manifest = B.make_manifest(batches, limits=limits, check_budget=check)
        manifest = B.read_manifest(manifest.raw, manifest.sha256, limits=limits,
                                   check_budget=check)
        need([entry.unit_id for batch in manifest.batches for entry in batch] ==
             [pin["unit_id"] for pin in unit_pins], "MANIFEST_ORDER")
        # The host will revalidate later. This preparation validates the exact
        # persisted bundle now without opening host or owner state.
        append = {"schema": APPEND_SCHEMA, "bundle_directory": str(output),
            "manifest": {"path": str(output / "manifest.json"), "sha256": manifest.sha256},
            "targets": targets, "share_all_bundle": True, "allow_partial_publication": True,
            "bundle_limits": dict(BUNDLE_LIMITS)}
        append_raw = encoded(append)
        need(read(profile_path, METADATA_MAX, check) == profile_raw and
             read(report, METADATA_MAX, check) == report_raw, "SELECTED_INPUT_CHANGED")
        check()
        output.mkdir()
        (output / "units").mkdir()
        written = 0

        def save(path, raw, maximum):
            nonlocal written
            check()
            need(type(raw) is bytes and 0 < len(raw) <= maximum and
                 written + len(raw) <= EVIDENCE_MAX + 3*METADATA_MAX, "OUTPUT_BYTE_BOUND")
            ordinary_path(path, fresh=True)
            with path.open("xb") as stream:
                need(stream.write(raw) == len(raw), "OUTPUT_SHORT_WRITE")
                stream.flush()
                os.fsync(stream.fileno())
            written += len(raw)
            need(read(path, maximum, check) == raw, "OUTPUT_READBACK")

        for pin, raw in zip(unit_pins, raws):
            save(output / "units" / (pin["unit_id"] + ".json"), raw, EVIDENCE_MAX)
        save(output / "manifest.json", manifest.raw, METADATA_MAX)
        save(output / "append.json", append_raw, METADATA_MAX)
        stored_manifest = B.read_manifest(read(output / "manifest.json", METADATA_MAX, check),
            manifest.sha256, limits=limits, check_budget=check)
        for entries in stored_manifest.batches:
            stored_raws = [read(output / entry.relative_path, entry.raw_bytes, check)
                           for entry in entries]
            B.validate_batch(entries, stored_raws, limits=limits, check_budget=check)
        need(read(output / "append.json", METADATA_MAX, check) == append_raw and
             read(profile_path, METADATA_MAX, check) == profile_raw and
             read(report, METADATA_MAX, check) == report_raw, "FINAL_INPUT_OR_CONFIG_CHANGED")
        check()
        receipt = {"schema": RECEIPT_SCHEMA, "status": STATUS,
            "operation": operation, "source_layout": layout, "semantic_id": semantic,
            "selected_profile_sha256": profile_sha256,
            "report": {"path": str(report), "bytes": len(report_raw), "sha256": report_sha256},
            "reported_provenance": provenance, "evidence_directory": str(evidence_directory),
            "output_directory": str(output), "units": unit_pins, "unit_count": len(unit_pins),
            "evidence_bytes": total_bytes, "target_count": len(targets), "targets": targets,
            "manifest": {"path": "manifest.json", "bytes": len(manifest.raw), "sha256": manifest.sha256},
            "append_config": {"path": "append.json", "bytes": len(append_raw), "sha256": digest(append_raw)},
            "share_all_bundle": True, "allow_partial_publication": True,
            "mathematical_acceptance": False, "dependencies_checked": False,
            "host_publication": False, "package_authenticated": False,
            "native_artifacts_checked": False, "original_closure_verified": False,
            "assurance": "EXACT_INERT_PUBLICATION_BYTES_NOT_ACCEPTANCE_OR_DEPENDENCY_COMPLETENESS",
            "limits": dict(BUNDLE_LIMITS),
            "cost": {"wall_seconds_before_receipt": time.monotonic()-started,
                     "controller_cpu_seconds_before_receipt": time.process_time()-cpu_started,
                     "wall_limit_seconds": WALL_SECONDS, "cpu_limit_seconds": CPU_SECONDS,
                     "containment": "COOPERATIVE_NOT_HARD_PROCESS_LIMITS"},
            "retention": "PARTIAL_OUTPUT_PRESERVED_ON_FAILURE_NO_ROLLBACK_OR_AUTOMATIC_RETRY",
            "relocation": "RESELECT_AND_REPIN_APPEND_CONFIG_LOCAL_PATHS_AFTER_MOVING_BUNDLE"}
        save(output / "PREPARATION.json", encoded(receipt), METADATA_MAX)
        check()
        return receipt


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_PYTHON_REQUIRED")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("package", "profile-sha256", "report", "report-sha256",
                 "evidence-directory", "output"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--share-all-bundle", action="store_true")
    parser.add_argument("--allow-partial-publication", action="store_true")
    args = parser.parse_args()
    result = project_selected(args.package, args.profile_sha256, args.report,
        args.report_sha256, args.evidence_directory, args.output,
        share_all_bundle=args.share_all_bundle,
        allow_partial_publication=args.allow_partial_publication)
    print(json.dumps(result, sort_keys=True, ensure_ascii=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(json.dumps({"status": "REFUSED", "error_type": type(error).__name__,
            "error": str(error)[:2048], "mathematical_acceptance": False,
            "retention": "PARTIAL_OUTPUT_MAY_EXIST_NO_ROLLBACK_OR_AUTOMATIC_RETRY"},
            sort_keys=True, ensure_ascii=True, allow_nan=False))
        raise SystemExit(1)

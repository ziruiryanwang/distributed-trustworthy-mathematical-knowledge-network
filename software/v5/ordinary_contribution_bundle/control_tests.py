"""Prospective file-only publication projection controls; no owner/native/DB.

Uses two retained real publication results and explicitly relocated evidence.
Root selects execution separately. Every output is fresh, bounded and preserved.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager, redirect_stdout
from copy import deepcopy
import dataclasses  # Preload standard dependencies before the file-read guard.
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import time
from types import SimpleNamespace as NS

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PROFILE = "e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()
CASES, ACTIVE = [], None
FIXTURES = (
    dict(label="contribution", root="experiments/v5-local-checks/finite-map-refinement-contribution02/contribution",
         sha="37ea97b2c006b216782e7a53142ed741a53a26a86a3b89ded9252dae1279b9b0",
         wrapper="experiments/v5-local-checks/finite-map-refinement-contribution02/launcher/child/stdout.txt",
         wrapper_sha="06534e767bf4a04de3f2e2b4ec26d4aeb5872bfe8059a2b4a1e015763ee0bebb",
         units=21, targets=11, evidence_bytes=379701, support=10),
    dict(label="completion", root="experiments/v5-local-checks/ordinary-project-extraction-public-01/project/completion",
         sha="d031230312290008c5b09bb0587615d9a02310b4cfdc014ccbee2b491477d298",
         wrapper="experiments/v5-local-checks/ordinary-project-extraction-public-01/project/calls/03-complete/stdout.txt",
         wrapper_sha="b8f768361cc1378da6cb659a5e426f2721790eccd737285c6cb382424fb31e94",
         units=3, targets=1, evidence_bytes=10700, support=2),
)


def need(ok, code):
    if not ok:
        raise AssertionError("BUNDLE_CONTROL_"+code)


def check():
    need(time.monotonic()-START < 120 and time.process_time()-CPU < 60, "ORIGINAL_ENVELOPE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(doc):
    return json.dumps(doc, sort_keys=True, ensure_ascii=True, allow_nan=False,
                      separators=(",", ":")).encode("ascii")


def read(path, expected=None, maximum=2*MIB):
    check()
    need(path.is_absolute() and path.resolve(strict=True) == path and path.is_file(), "INPUT_PATH")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(0 < len(raw) <= maximum and (expected is None or sha(raw) == expected), "INPUT_PIN")
    return raw


def write(path, raw):
    need(type(raw) is bytes and 0 < len(raw) <= 2*MIB, "WRITE_BOUND")
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "SHORT_WRITE")


def audit(event, arguments):
    if ACTIVE is None:
        return
    check()
    if event in {"sqlite3.connect", "subprocess.Popen", "os.system", "socket.connect", "socket.bind"}:
        raise AssertionError("BUNDLE_CONTROL_FORBIDDEN_EFFECT:"+event)
    if event not in {"open", "os.listdir", "os.scandir"}:
        return
    value = arguments[0]
    if isinstance(value, int):
        return  # Descriptor operations use handles obtained by already observed opens.
    path = Path(os.fsdecode(value)).absolute()
    need(".." not in path.parts, "DOT_COMPONENT_OPEN")
    if event == "open":
        mode, flags = arguments[1], arguments[2]
        writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or bool(
            flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if writing:
            need(path.is_relative_to(ACTIVE.output), "WRITE_OUTSIDE_NEW_OUTPUT:"+str(path))
        else:
            need(path in ACTIVE.files or any(path.is_relative_to(p) for p in ACTIVE.roots),
                 "READ_OUTSIDE_SELECTED_FILES:"+str(path))
            ACTIVE.reads.append(str(path))
    else:
        need(path == ACTIVE.output or path.is_relative_to(ACTIVE.output),
             "UNNECESSARY_INPUT_ENUMERATION:"+str(path))


@contextmanager
def guarded(package, report, evidence, output, codec_paths):
    global ACTIVE
    need(ACTIVE is None, "NESTED_GUARD")
    # No old fixture, owner, catalog, custody or source-project directory belongs
    # here. The selected data is only a report plus exact relocated evidence.
    state = NS(files={report, package/"PROFILE.json", *codec_paths,
                      *(evidence/(uid+".json") for uid in evidence_ids(evidence))},
               roots=(output,), output=output, reads=[])
    ACTIVE = state
    try:
        yield state
    finally:
        ACTIVE = None


def evidence_ids(directory):
    # Test fixture setup only, before the production call's enumeration guard.
    return [path.stem for path in directory.iterdir() if path.suffix == ".json" and len(path.stem) == 64]


def load_fixture(spec):
    root = ROOT/spec["root"]
    raw = read(root/"RESULT.json", spec["sha"])
    doc = json.loads(raw)
    outer_raw = read(ROOT/spec["wrapper"], spec["wrapper_sha"])
    outer = json.loads(outer_raw)
    need(outer["ok"] is True and outer["result"] == doc and doc["semantic_id"] == SEMANTIC,
         "HISTORICAL_RESULT_BINDING")
    need(len(doc["units"]) == spec["units"] and len(doc["targets"]) == spec["targets"] and
         sum(row["bytes"] for row in doc["units"]) == spec["evidence_bytes"], "FIXTURE_CENSUS")
    target_ids = {row["unit_id"] for row in doc["targets"]}
    need(len(doc["units"])-len(target_ids) == spec["support"], "SUPPORT_UNIT_CENSUS")
    units, pins = {}, [(root/"RESULT.json", spec["sha"]), (ROOT/spec["wrapper"], spec["wrapper_sha"])]
    for row in doc["units"]:
        path = root/"evidence"/(row["unit_id"]+".json")
        data = read(path, row["sha256"], maximum=row["bytes"])
        need(len(data) == row["bytes"], "FIXTURE_UNIT_LENGTH")
        units[row["unit_id"]] = data
        pins.append((path, row["sha256"]))
    return NS(spec=spec, doc=doc, outer=outer, units=units, pins=pins)


def relocated(base, label, fixture, *, outer=False, change=None, omit=None, data_change=None):
    root = base/label
    root.mkdir(); evidence = root/"evidence"; evidence.mkdir()
    doc = deepcopy(fixture.outer if outer else fixture.doc)
    if change is not None:
        change(doc)
    for uid, raw in fixture.units.items():
        if uid != omit:
            write(evidence/(uid+".json"), data_change(uid, raw) if data_change else raw)
    # A directory scan / accidental bulk copying would expose an unrelated file.
    write(evidence/"UNRELATED-NOT-SELECTED.json", b'{"must_not_be_read":true}')
    report = root/"report.json"; raw = encoded(doc); write(report, raw)
    return NS(root=root, evidence=evidence, report=report, pin=sha(raw), doc=doc, fixture=fixture)


def inner(doc):
    return doc["result"] if "result" in doc else doc


def invoke(s, fixture, output, *, cli=False, profile=None, pin=None,
           share=True, partial=True):
    names = [row[0] for row in s.P.CODECS]
    missing = object()
    previous = {name: sys.modules.get(name, missing) for name in names}
    with guarded(s.package, fixture.report, fixture.evidence, output, s.codec_paths) as observation:
        try:
            if cli:
                args = [str(s.source), "--package", str(s.package), "--profile-sha256", profile or PROFILE,
                    "--report", str(fixture.report), "--report-sha256", pin or fixture.pin,
                    "--evidence-directory", str(fixture.evidence), "--output", str(output)]
                if share: args.append("--share-all-bundle")
                if partial: args.append("--allow-partial-publication")
                old_argv, stream = sys.argv, io.StringIO()
                try:
                    sys.argv = args
                    with redirect_stdout(stream):
                        need(s.P.main() == 0, "CLI_RETURN")
                finally:
                    sys.argv = old_argv
                result = json.loads(stream.getvalue())
            else:
                result = s.P.project_selected(s.package, profile or PROFILE, fixture.report,
                    pin or fixture.pin, fixture.evidence, output,
                    share_all_bundle=share, allow_partial_publication=partial)
        finally:
            need(all(sys.modules.get(name, missing) is value for name, value in previous.items()),
                 "TEMPORARY_MODULE_SLOTS_RESTORED")
    return result, observation


def validate(s, f, output, receipt, observation):
    doc, P = inner(f.doc), s.P
    need(receipt == json.loads(read(output/"PREPARATION.json")) and
         receipt["schema"] == P.RECEIPT_SCHEMA and receipt["status"] == P.STATUS and
         receipt["semantic_id"] == SEMANTIC and receipt["selected_profile_sha256"] == PROFILE,
         "RECEIPT_BINDING")
    for flag in ("mathematical_acceptance", "dependencies_checked", "host_publication",
                 "package_authenticated", "native_artifacts_checked", "original_closure_verified"):
        need(receipt[flag] is False, "INERT_FLAG:"+flag)
    pins = [dict(unit_id=row["unit_id"], raw_bytes=row["bytes"], raw_sha256=row["sha256"])
            for row in doc["units"]]
    need(receipt["units"] == pins and receipt["targets"] == doc["targets"] and
         receipt["unit_count"] == len(pins) and receipt["target_count"] == len(doc["targets"]) and
         receipt["evidence_bytes"] == sum(row["bytes"] for row in doc["units"]), "ALL_SUPPORT_RETAINED")
    manifest_raw, append_raw = read(output/"manifest.json"), read(output/"append.json")
    config = json.loads(append_raw)
    need(config["schema"] == "DMKN_INCREMENTAL_HOST_APPEND_V1" and
         config["bundle_directory"] == str(output) and
         config["manifest"] == dict(path=str(output/"manifest.json"), sha256=sha(manifest_raw)) and
         config["targets"] == doc["targets"] and config["share_all_bundle"] is True and
         config["allow_partial_publication"] is True, "UNCHANGED_HOST_CONFIG_COMPATIBILITY")
    for key, raw in (("manifest", manifest_raw), ("append_config", append_raw)):
        need(receipt[key]["bytes"] == len(raw) and receipt[key]["sha256"] == sha(raw), "OUTPUT_PINS")
    # Independently read/validate emitted files through the unchanged pure bundle
    # APIs. This does not open a host, mathematical owner or admission code.
    with P.selected_modules(s.package, s.profile_doc, check) as modules:
        B = modules["baseline_bundle"]
        limits = B.Limits(**config["bundle_limits"])
        manifest = B.read_manifest(manifest_raw, sha(manifest_raw), limits=limits, check_budget=check)
        entries = [entry for batch in manifest.batches for entry in batch]
        need([entry.unit_id for entry in entries] == [row["unit_id"] for row in doc["units"]],
             "MANIFEST_ALL_UNIT_ORDER")
        for batch in manifest.batches:
            raws = [read(output/entry.relative_path, entry.raw_sha256, entry.raw_bytes) for entry in batch]
            B.validate_batch(batch, raws, limits=limits, check_budget=check)
        for row in doc["units"]:
            need(read(output/"units"/(row["unit_id"]+".json")) == f.fixture.units[row["unit_id"]],
                 "EXACT_OUTPUT_EVIDENCE")
    expected_files = {"manifest.json", "append.json", "PREPARATION.json"} | {
        "units/"+row["unit_id"]+".json" for row in doc["units"]}
    actual = {path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()}
    need(actual == expected_files, "NO_UNSELECTED_OUTPUT_OR_CORPUS_EXPORT")
    evidence_reads = {Path(path).name for path in observation.reads if Path(path).parent == f.evidence}
    need(evidence_reads == {row["unit_id"]+".json" for row in doc["units"]}, "EXACT_EVIDENCE_READ_SET")


def passed(name, **evidence):
    check(); CASES.append(dict(case=name, status="PASS", **evidence))


def expect_refusal(s, f, output, code=None, **kwargs):
    try:
        invoke(s, f, output, **kwargs)
    except (ValueError, OSError) as error:
        need(code is None or code in str(error), "WRONG_REFUSAL:"+str(error))
        need(not output.exists(), "PREFLIGHT_REFUSAL_CREATED_OUTPUT")
        return type(error).__name__+":"+str(error)
    raise AssertionError("BUNDLE_CONTROL_EXPECTED_REFUSAL")


def controls(s, base, contribution, completion):
    first = relocated(base, "real-contribution", contribution, outer=True)
    out = base/"bundle-contribution"
    receipt, observation = invoke(s, first, out, cli=True)
    validate(s, first, out, receipt, observation)
    need(receipt["source_layout"] == "owner-wrapper" and
         receipt["reported_provenance"]["reported_profile_sha256"] != PROFILE, "OLD_SOURCE_PROFILE_SUPPORTED")
    passed("real-contribution-cli-21-units-11-targets-10-support-units", evidence_bytes=379701)

    second = relocated(base, "real-completion", completion)
    out = base/"bundle-completion"
    receipt, observation = invoke(s, second, out)
    validate(s, second, out, receipt, observation)
    need(receipt["source_layout"] == "helper-result", "HELPER_LAYOUT")
    passed("real-completion-3-units-in-supplement-then-consumer-order", support_units=2, evidence_bytes=10700)

    def untrusted_metadata(doc):
        doc.update(ok=False, profile_sha256="1"*64, close_errors=["historical closure not established"],
                   final_budget_error="historical limit")
        for row in doc["result"]["units"]:
            row["file"] = "../../MUST-NOT-OPEN-PREVIOUS-CORPUS/"+row["unit_id"]+".json"
    untrusted = relocated(base, "untrusted-provenance-and-paths", completion, outer=True, change=untrusted_metadata)
    out = base/"bundle-untrusted-metadata"
    receipt, observation = invoke(s, untrusted, out)
    validate(s, untrusted, out, receipt, observation)
    provenance = receipt["reported_provenance"]
    need(provenance["reported_ok"] is False and provenance["reported_profile_sha256"] == "1"*64 and
         provenance["reported_close_errors"] and provenance["original_closure_verified"] is False,
         "FALSE_WRAPPER_IS_PROVENANCE_NOT_ACCEPTANCE")
    passed("explicit-relocation-ignores-malicious-file-paths-and-false-outer-success")

    errors = [expect_refusal(s, second, base/"bad-report-pin", "PROJECTION_REPORT_PIN", pin="0"*64),
              expect_refusal(s, second, base/"bad-profile-pin", "PROJECTION_PROFILE_PIN", profile="0"*64)]
    passed("report-and-selected-profile-hash-refusals", errors=errors)

    def wrong_unit_membership(doc):
        # Recompute a syntactically consistent ExportID for the wrong supplied
        # support unit. This can pass hash derivation but must fail membership.
        target = doc["targets"][0]
        target["unit_id"] = doc["units"][0]["unit_id"]
        with s.P.selected_modules(s.package, s.profile_doc, check) as modules:
            E, S, PE = (modules[name] for name in
                       ("ordinary_evidence", "ordinary_semantics", "portable_evidence"))
            support = PE.read_evidence(completion.units[target["unit_id"]])
            need(E.name_key(target["name"]) not in support.census.expected_names,
                 "MEMBERSHIP_CONTROL_IS_GENUINELY_ABSENT")
            target["export_id"] = S.export_id(SEMANTIC, target["unit_id"], target["name"])

    changes = (
        ("unit-hash", lambda doc: doc["units"][0].update(sha256="0"*64), "PROJECTION_EVIDENCE_PIN"),
        ("target", lambda doc: doc["targets"][0].update(export_id="0"*64), "PROJECTION_TARGET_BINDING"),
        ("target-membership", wrong_unit_membership, "PROJECTION_TARGET_BINDING"),
        ("status", lambda doc: doc.update(status="NOT_A_PUBLICATION_RESULT"), "PROJECTION_HELPER_RESULT_STATUS"),
        ("duplicate-unit", lambda doc: doc["units"].append(deepcopy(doc["units"][0])), "PROJECTION_DUPLICATE_UNIT"),
        ("duplicate-target", lambda doc: doc["targets"].append(deepcopy(doc["targets"][0])), "PROJECTION_DUPLICATE_TARGET"),
        ("unit-count", lambda doc: doc.update(units=[deepcopy(doc["units"][0]) for _ in range(33)]), "PROJECTION_UNIT_COUNT"),
        ("target-count", lambda doc: doc.update(targets=[deepcopy(doc["targets"][0]) for _ in range(33)]), "PROJECTION_TARGET_COUNT"),
        ("unit-bytes", lambda doc: doc["units"][0].update(bytes=4*MIB+1), "PROJECTION_INTEGER_BOUND"),
        ("aggregate-bytes", lambda doc: doc["units"][1].update(bytes=4*MIB), "PROJECTION_EVIDENCE_TOTAL"),
        ("semantic", lambda doc: doc.update(semantic_id="0"*64), "PROJECTION_REPORT_SEMANTICS"),
    )
    errors = []
    for label, change, code in changes:
        f = relocated(base, "reject-"+label, completion, change=change)
        errors.append(dict(case=label, error=expect_refusal(s, f, base/("no-output-"+label), code)))
    passed("evidence-target-layout-duplicate-count-byte-cap-and-semantic-refusals", errors=errors)

    missing = relocated(base, "missing-unit", completion, omit=completion.doc["units"][0]["unit_id"])
    error = expect_refusal(s, missing, base/"no-missing-output")
    passed("missing-selected-evidence-refuses-without-historical-fallback", error=error)

    bad_uid = completion.doc["units"][0]["unit_id"]
    bad_data = json.loads(completion.units[bad_uid]); bad_data["schema"] = "NOT_PORTABLE_EVIDENCE"
    bad_raw = encoded(bad_data)
    def bad_schema_row(doc):
        doc["units"][0].update(bytes=len(bad_raw), sha256=sha(bad_raw))
    malformed = relocated(base, "malformed-evidence", completion, change=bad_schema_row,
        data_change=lambda uid, raw: bad_raw if uid == bad_uid else raw)
    error = expect_refusal(s, malformed, base/"no-malformed-output")
    passed("actual-codec-refuses-malformed-evidence-with-correct-byte-pin", error=error)

    errors = [expect_refusal(s, second, base/"no-disclosure-output", "PROJECTION_EXPLICIT_DISCLOSURE_REQUIRED", share=False),
              expect_refusal(s, second, base/"no-partial-output", "PROJECTION_EXPLICIT_DISCLOSURE_REQUIRED", partial=False),
              expect_refusal(s, second, second.evidence/"overlap-output", "PROJECTION_OUTPUT_OVERLAP")]
    existing = base/"already-exists"; existing.mkdir()
    try:
        invoke(s, second, existing)
    except ValueError as error:
        need("PROJECTION_OUTPUT_EXISTS" in str(error) and not list(existing.iterdir()), "EXISTING_OUTPUT_PRESERVED")
    else:
        need(False, "EXISTING_OUTPUT_REFUSAL")
    passed("explicit-approval-output-overlap-and-existing-output-refusals", errors=errors)


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("package", "profile-sha256", "project", "project-sha256", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTEXT")
    package, source, output = Path(args.package), Path(args.project), Path(args.output)
    need(args.profile_sha256 == PROFILE and package.is_absolute() and
         output.is_absolute() and output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         output.parent.resolve(strict=True) == output.parent and not os.path.lexists(output) and
         not output.is_relative_to(package) and not package.is_relative_to(output), "SELECTED_FRESH_OUTPUT")
    source_raw = read(source, args.project_sha256)
    profile_raw = read(package/"PROFILE.json", PROFILE)
    own_path = Path(__file__).absolute(); own_raw = read(own_path)
    output.mkdir()
    report = dict(passed=False, cases=CASES, profile_sha256=PROFILE, project_sha256=args.project_sha256,
        control_sha256=sha(own_raw), scope="INERT_FILE_ONLY_PROJECTION_NOT_MATHEMATICAL_ACCEPTANCE_OR_HOSTING")
    try:
        spec = importlib.util.spec_from_file_location("_publication_projection_controls", source)
        P = importlib.util.module_from_spec(spec)
        exec(compile(source_raw, str(source), "exec", dont_inherit=True), P.__dict__)
        s = NS(P=P, source=source, package=package, profile_doc=json.loads(profile_raw),
               codec_paths=[package/row[1] for row in P.CODECS])
        fixtures = [load_fixture(f) for f in FIXTURES]
        sys.addaudithook(audit)
        controls(s, output, *fixtures)
        need(read(source, args.project_sha256) == source_raw and read(package/"PROFILE.json", PROFILE) == profile_raw and
             read(own_path) == own_raw, "SELECTED_SOURCES_UNCHANGED")
        for f in fixtures:
            for path, digest in f.pins:
                read(path, digest)
        need(ACTIVE is None, "GUARD_CLOSED")
        report.update(passed=True, original_evidence_bytes=390401, owner_calls=0, native_calls=0,
                      database_calls=0, network_calls=0)
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:2000])
    report.update(completed_groups=len(CASES), wall_seconds=time.monotonic()-START,
                  harness_cpu_seconds=time.process_time()-CPU)
    write(output/"RESULT.json", encoded(report))
    print(json.dumps(report, sort_keys=True), flush=True)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""One bounded file-only commons archive gate; no product/native/state work.

Pack once and run the relocated approved verifier once. All other negatives
are in-process file/manifest checks against fresh preserved test-only roots.
An independently selected outer Job encloses this test and its sole child.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import time
import types
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_commons_bundle/"
PRIOR_SHA = "65edf28f928d4100346a4603fe508252ddc6393950c34a373fbb33da4c6491f5"
MIRROR = "software/v5/ordinary_inert_mirror02/"
MIRROR_MAP_SHA = "1bc43d4c9896476443d0d6aab95015db7af32bc46a04cfb1624a5c40e638feb9"
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()


def need(ok, why):
    if not ok:
        raise AssertionError("COMMONS_BUNDLE_TEST_"+why)


def check():
    need(time.monotonic()-START < 100 and time.process_time()-CPU < 45,
         "ORIGINAL_ALLOWANCE")


def pin(raw):
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def read(path, maximum=2*MIB):
    check()
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and
         not getattr(info, "st_file_attributes", 0) & 0x400 and
         0 < info.st_size <= maximum, "REGULAR_BOUNDED_INPUT:"+str(path))
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == info.st_size, "INPUT_CHANGED")
    return raw


def save(path, value):
    check()
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(raw) <= 2*MIB, "REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def load(path, expected):
    raw = read(path)
    need(pin(raw)["sha256"] == expected, "UTILITY_PIN")
    module = types.ModuleType("_approved_commons_bundle_subject")
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def refuses(action, expected):
    try:
        action()
    except ValueError as error:
        need(expected in str(error), "WRONG_REFUSAL:"+str(error))
        return str(error)
    raise AssertionError("COMMONS_BUNDLE_TEST_MISSING_REFUSAL:"+expected)


def members(raw, base):
    need(len(raw) <= 16*MIB, "ARCHIVE_BOUND")
    with zipfile.ZipFile(io.BytesIO(raw), "r") as archive:
        rows = archive.infolist()
        names = [row.filename for row in rows]
        need(len(rows) == 187 and names == sorted(names) and len(set(names)) == 187
             and len({name.casefold() for name in names}) == 187 and not archive.comment,
             "ZIP_EXACT_CENSUS")
        data = {}
        for row in rows:
            check(); base.relative(row.filename)
            need(not row.is_dir() and row.date_time == (1980, 1, 1, 0, 0, 0) and
                 row.create_system == 3 and row.external_attr == 0o100644 << 16 and
                 row.compress_type == zipfile.ZIP_STORED and row.flag_bits == 0 and
                 row.extra == row.comment == b"" and
                 0 < row.file_size == row.compress_size <= 2*MIB, "ZIP_METADATA")
            data[row.filename] = archive.read(row)
            need(len(data[row.filename]) == row.file_size, "ZIP_MEMBER_SIZE")
        need(sum(map(len, data.values())) <= 10*MIB, "ZIP_EXPANDED_BOUND")
        return data


def extract(data, destination, base):
    check(); base.ordinary(destination, directory=True, fresh=True)
    need(destination.is_relative_to(ROOT/"experiments/v5-local-checks"), "EXTRACT_SCOPE")
    destination.mkdir()
    for name, raw in sorted(data.items()):
        check(); base.relative(name)
        path = destination.joinpath(*PurePosixPath(name).parts)
        need(path.is_relative_to(destination), "EXTRACT_TARGET")
        path.parent.mkdir(parents=True, exist_ok=True)
        base.ordinary(path.parent, directory=True)
        with base.ordinary(path, fresh=True).open("xb") as stream:
            stream.write(raw)
    return destination


def verify_cli(script, relocated, digest, output):
    """The only child is the exact approved relocated file-only verifier."""
    check()
    stdout, stderr = output/"verify-stdout.json", output/"verify-stderr.txt"
    argv = [sys.executable, "-I", "-S", "-B", str(script), "verify",
            "--source-root", str(relocated), "--manifest-sha256", digest]
    save(output/"VERIFY-COMMAND.json", dict(argv=argv, cwd=str(ROOT),
        authority="FILE_ONLY_SOURCE_VERIFIER_NOT_PRODUCT", native_operations=0))
    with stdout.open("xb") as out, stderr.open("xb") as err:
        completed = subprocess.run(argv, cwd=ROOT, shell=False, stdin=subprocess.DEVNULL,
            stdout=out, stderr=err, timeout=min(60, max(1, 100-(time.monotonic()-START))))
    check()
    need(completed.returncode == 0 and stderr.stat().st_size == 0, "RELOCATED_CLI_EXIT")
    return json.loads(read(stdout, MIB))


def guide_links(data, doc, relocated):
    guides = sorted({path for path in doc["entrypoints"].values() if path.endswith(".md")})
    need(len(guides) == 7, "CURRENT_GUIDE_CENSUS")
    links = []
    for guide in guides:
        for target in re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", data[guide].decode("utf-8")):
            target = target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                need(parsed.scheme in ("https", "http"), "GUIDE_URL_SCHEME")
                continue
            if not parsed.path:
                continue
            path = (relocated/guide).parent.joinpath(unquote(parsed.path)).resolve()
            need(path.is_relative_to(relocated) and path.is_file() and
                 path.relative_to(relocated).as_posix() in doc["files"],
                 "GUIDE_LINK:"+guide+":"+target)
            links.append(dict(guide=guide, target=target))
    need(links, "GUIDE_LINKS_PRESENT")
    return links


def run(args, output, cases):
    root, prior_root = Path(args.source_root), Path(args.investigator_root)
    need(root == ROOT, "SELECTED_CANONICAL_SOURCE")
    B = load(root/PREFIX/"bundle.py", args.bundle_sha256)
    base = B.helpers()
    need(B.COUNT == 186 and B.PRIOR_SHA256 == PRIOR_SHA and len(B.SOURCES) == 16,
         "FIXED_COMMONS_SHAPE")
    original_raw = read(prior_root/B.PRIOR_MANIFEST)
    need(pin(original_raw) == dict(bytes=25231, sha256=PRIOR_SHA), "PRIOR_SELECTED_PIN")
    original = json.loads(original_raw)["files"]
    need(len(original) == 169, "PRIOR_MAP_SIZE")
    receipt = B.pack(root, prior_root, output/"packed", check=check)
    need(receipt["status"] == "PACKED_COMMONS_SOURCE_NOT_BUILT" and
         receipt["payload_files"] == 186 and receipt["archive_files"] == 187 and
         json.loads(read(output/"packed/RECEIPT.json")) == receipt, "TERMINAL_PACK_RECEIPT")
    archive = read(output/"packed/source.zip", 16*MIB)
    need(pin(archive) == receipt["archive"], "ARCHIVE_RECEIPT")
    data = members(archive, base)
    doc = json.loads(data[B.MANIFEST])
    projected = {"HISTORICAL-INVESTIGATOR-README.md" if name == "README.md" else name: value
                 for name, value in original.items()}
    need(set(data) == set(projected) | set(B.SOURCES) | {B.PRIOR_MANIFEST, B.MANIFEST}
         and set(doc["files"]) == set(data)-{B.MANIFEST}, "EXACT_PROJECTED_MAP")
    need(doc["prior_manifest"] == dict(path=B.PRIOR_MANIFEST, sha256=PRIOR_SHA,
         path_projection={"README.md": "HISTORICAL-INVESTIGATOR-README.md"}), "EXPLICIT_PROJECTION")
    for name, expected in original.items():
        destination = "HISTORICAL-INVESTIGATOR-README.md" if name == "README.md" else name
        need(pin(data[destination]) == expected and data[destination] == read(prior_root/name),
             "PRESERVED_OLD_BYTES:"+name)
    for destination, source in B.SOURCES.items():
        need(data[destination] == read(root/source), "SELECTED_NEW_BYTES:"+destination)
    need(data[B.PRIOR_MANIFEST] == original_raw and pin(data[B.MANIFEST]) == receipt["manifest"],
         "MANIFEST_ASSOCIATIONS")
    for name, expected in doc["files"].items():
        need(pin(data[name]) == expected, "CURRENT_PAYLOAD_PIN:"+name)
    directories = {p.as_posix() for name in data for p in PurePosixPath(name).parents if p.as_posix() != "."}
    need(len(directories) == 47 and len(data)+len(directories) == 234, "BOUNDED_CENSUS")
    cases.append("one_pack_full_readback_exact169projection_plus17")

    relocated = extract(data, output/"relocated", base)
    verified = verify_cli(relocated/B.UTILITY, relocated, receipt["manifest"]["sha256"], output)
    need(verified["status"] == "VERIFIED_EXACT_COMMONS_SOURCE_NOT_BUILT" and
         verified["manifest"] == receipt["manifest"] and verified["payload_files"] == 186,
         "RELOCATED_CURRENT_VERIFICATION")
    cases.append("one_relocated_public_file_only_verifier")

    need(doc["entrypoints"] == B.ENTRYPOINTS and set(B.ENTRYPOINTS.values()) <= set(doc["files"]),
         "CURRENT_ENTRYPOINT_CLOSURE")
    links = guide_links(data, doc, relocated)
    mirror_raw = data[MIRROR+"SOURCES.json"]
    need(pin(mirror_raw)["sha256"] == MIRROR_MAP_SHA, "MIRROR_FIXED_MAP")
    mirror = json.loads(mirror_raw)
    need(mirror["schema"] == "DMKN_INERT_MIRROR_SOURCES_V1" and
         mirror["source_manifest_sha256"] == pin(data[B.PRIOR_MANIFEST])["sha256"] and
         len(mirror["files"]) == 27, "MIRROR_PREDECESSOR_ASSOCIATION")
    source_names = []
    for role, selected in mirror["files"].items():
        source = selected["source"]; source_names.append(source)
        need(source in original and source in doc["files"] and pin(data[source]) ==
             {key: selected[key] for key in ("bytes", "sha256")} == original[source],
             "MIRROR27_SOURCE:"+role)
    need(len(set(source_names)) == 27 and
         not any("/ordinary_multi_source/" in source for source in source_names),
         "MIRROR_NOT_SILENTLY_REBOUND")
    cases.append("seven_current_guides_entrypoints_and_static_mirror27")

    refusals = []
    mutations = [
        ("missing-new-file", lambda d: d["files"].pop(MIRROR+"mirror.py"), "EXACT_SELECTION"),
        ("old-row-changed", lambda d: d["files"]["START-HERE.md"].update(sha256="0"*64), "PRIOR_PROJECTION"),
        ("wrong-projection", lambda d: d["prior_manifest"]["path_projection"].update({"README.md": "README.md"}), "MANIFEST_PROFILE"),
        ("wrong-prior-association", lambda d: d["files"][B.PRIOR_MANIFEST].update(sha256="0"*64), "PRIOR_ASSOCIATION"),
        ("changed-fixed-mirror", lambda d: d["files"][MIRROR+"run.py"].update(sha256="0"*64), "ADDITION_PIN"),
        ("wrong-selector", lambda d: d["entrypoints"].update(operator="software/v5/ordinary_investigator_bundle/prepare_selected.py"), "MANIFEST_PROFILE"),
        ("case-alias", lambda d: d["files"].update({"Readme.md": d["files"]["README.md"]}), "EXACT_SELECTION"),
    ]
    for label, alter, expected in mutations:
        changed = deepcopy(doc); alter(changed)
        refusals.append(dict(case=label, error=refuses(
            lambda changed=changed: B.validate_manifest(base, changed, original, original_raw), expected)))
    refusals.append(dict(case="fabricated-prior", error=refuses(
        lambda: B.prior_files(base, original_raw+b" "), "PRIOR_MANIFEST_PIN")))
    cases.append("eight_manifest_projection_association_and_role_refusals")

    faulty = [
        ("wrong-prior", {**data, B.PRIOR_MANIFEST: original_raw+b" "}, "PRIOR_MANIFEST_PIN"),
        ("wrong-old-payload", {**data, "START-HERE.md": data["START-HERE.md"]+b"\n"}, "PAYLOAD_PIN"),
        ("missing-payload", {name: raw for name, raw in data.items() if name != MIRROR+"mirror.py"}, "EXACT_CENSUS"),
        ("extra-payload", {**data, "unexpected.txt": b"test-only extra\n"}, "EXTRA_OR_ALIASED_FILE"),
    ]
    for label, malformed, expected in faulty:
        bad_root = extract(malformed, output/label, base)
        refusals.append(dict(case=label, error=refuses(
            lambda bad_root=bad_root: B.verify(bad_root, receipt["manifest"]["sha256"], check=check), expected)))
    refusals.append(dict(case="wrong-current-manifest", error=refuses(
        lambda: B.verify(relocated, "0"*64, check=check), "MANIFEST_PIN")))
    refusals.append(dict(case="nonfresh-pack-output", error=refuses(
        lambda: B.pack(root, prior_root, output/"packed", check=check), "OUTPUT_EXISTS")))
    # The old full-root census is inapplicable; no historical packer is imported.
    refusals.append(dict(case="old-census-on-new-root", error=refuses(
        lambda: base.census(relocated, set(original)|{B.PRIOR_MANIFEST}, check), "EXTRA_OR_ALIASED_")))
    cases.append("four_actual_malformed_roots_manifest_and_output_refusals")

    base.census(relocated, set(data), check)
    for name, raw in data.items():
        need(read(relocated/name) == raw, "FINAL_RELOCATED_IMMUTABILITY")
    base.census(prior_root, set(original)|{B.PRIOR_MANIFEST}, check)
    need(read(prior_root/B.PRIOR_MANIFEST) == original_raw, "FINAL_PRIOR_MANIFEST")
    for name, expected in original.items():
        need(pin(read(prior_root/name)) == expected, "FINAL_PRIOR_PIN")
    for destination, source in B.SOURCES.items():
        need(read(root/source) == data[destination], "FINAL_SELECTED_SOURCE")
    need(pin(read(output/"packed/source.zip", 16*MIB)) == receipt["archive"], "FINAL_ARCHIVE_PIN")
    cases.append("final_immutable_input_archive_and_relocated_maps")
    need(len(cases) == 6 and len(refusals) == 15, "EXPECTED_CASE_CENSUS")
    return dict(status="PASS", cases=cases, refusals=refusals, receipt=receipt,
        verified=verified, guide_links=links, mirror_source_files=27,
        extracted_files=187, extracted_directories=47, native_operations=0,
        product_imports=0, state_opened=False, mathematical_acceptance=False,
        wall_seconds=time.monotonic()-START, harness_cpu_seconds=time.process_time()-CPU,
        cpu_scope="HARNESS_ONLY_CHILD_ALREADY_INCLUDED_IN_OUTER_JOB_MEASUREMENT")


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("source-root", "investigator-root", "bundle-sha256", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "ISOLATED_CANONICAL_WINDOWS")
    output = Path(args.output)
    need(output.is_absolute() and output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         not output.exists() and output.parent.is_dir(), "FRESH_OUTPUT_SCOPE")
    output.mkdir(); cases = []
    try:
        result = run(args, output, cases)
        check(); save(output/"RESULT.json", result)
        print(json.dumps(result, sort_keys=True, allow_nan=False), flush=True)
    except BaseException as error:
        save(output/"FAILURE.json", dict(status="FAILED", completed_cases=cases,
            error_type=type(error).__name__, error=str(error)[:2000],
            retention="PRESERVED_NO_AUTOMATIC_RETRY", mathematical_acceptance=False))
        raise


if __name__ == "__main__":
    main()

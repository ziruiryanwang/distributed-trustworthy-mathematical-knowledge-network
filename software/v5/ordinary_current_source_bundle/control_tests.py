"""One source pack/relocation and changed-selection refusals; no native build."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
import zipfile

PREFIX = "software/v5/ordinary_current_source_bundle/"
MAP = "software/v5/ordinary_current_distribution/source-map.json"
MAP_SHA = "65fde356b8ce6146b07ab49fad40a859af5bf0ce32e8d7beea76e32da60a9c9e"
BUNDLE_SHA = "b5d211a83644b61c6a6fe673785ccd1e1960816a2d58f20787b9d4dfdb3c9da9"
# Independent path oracle, not the utility's FIXED/NEW or known_pins result.
ADDITIONS = {
    MAP, "software/v5/ordinary_current_distribution/build.py",
    "software/v5/ordinary_current_distribution/README.md",
    "software/v5/ordinary_current_distribution/CONTRACT.md",
    "software/v5/ordinary_demand_frontier/API.md",
    PREFIX+"bundle.py", PREFIX+"README.md", PREFIX+"LICENSE-STATUS.md",
}


def need(ok, code):
    if not ok:
        raise AssertionError("CURRENT_BUNDLE_CONTROL_"+code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(raw):
    return {"bytes": len(raw), "sha256": sha(raw)}


def fresh(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)


def refuses(fn, expected):
    try:
        fn()
    except ValueError as error:
        need(str(error) == expected, "WRONG_REFUSAL:"+str(error))
    else:
        raise AssertionError("CURRENT_BUNDLE_CONTROL_EXPECTED_REFUSAL:"+expected)


def main():
    need(sys.platform == "win32" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_WINDOWS_PROCESS")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root, output = Path(args.source_root), Path(args.output)
    need(root.is_absolute() and root.is_dir() and output.is_absolute() and
         output.parent.is_dir() and not output.exists() and not root.is_relative_to(output),
         "SELECTED_FRESH_PATHS")
    start = time.monotonic()
    def check():
        need(time.monotonic()-start < 60, "ORIGINAL_DEADLINE")
    utility_path = root/PREFIX/"bundle.py"
    raw = utility_path.read_bytes()
    need(sha(raw) == BUNDLE_SHA, "UTILITY_PIN")
    spec = importlib.util.spec_from_file_location("_current_bundle_control", utility_path)
    utility = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(utility_path), "exec", dont_inherit=True), utility.__dict__)
    map_raw = (root/MAP).read_bytes()
    need(sha(map_raw) == MAP_SHA, "MAP_PIN")
    mapping = json.loads(map_raw)
    need(mapping["schema"] == "DMKN_ORDINARY_CURRENT_SOURCE_MAP_V1" and
         len(mapping["sources"]) == 87 and not set(mapping["sources"]) & ADDITIONS,
         "INDEPENDENT_MAP_ORACLE")
    expected = set(mapping["sources"]) | ADDITIONS
    need(len(expected) == 95, "INDEPENDENT_PAYLOAD_COUNT")
    originals = {name: (root/name).read_bytes() for name in sorted(expected)}
    need(sum(len(raw) for raw in originals.values()) <= 8*1024**2, "INPUT_BOUND")
    output.mkdir()
    receipt = utility.pack(root, output/"packed", check=check)
    need(receipt["status"] == "PACKED_SOURCE_NOT_BUILT" and
         receipt["payload_files"] == 95 and receipt["archive_files"] == 96,
         "PACK_COUNTS")
    archive_path = output/"packed/source.zip"
    need(pin(archive_path.read_bytes()) == receipt["archive"], "ACTUAL_ARCHIVE_PIN")
    with zipfile.ZipFile(archive_path, "r") as archive:
        rows = archive.infolist()
        need(len(rows) == 96 and {row.filename for row in rows} == expected | {"SOURCE-MANIFEST.json"},
             "INDEPENDENT_ARCHIVE_CENSUS")
        data = {row.filename: archive.read(row) for row in rows}
    need(all(data[name] == originals[name] for name in expected) and
         pin(data["SOURCE-MANIFEST.json"]) == receipt["manifest"], "ARCHIVED_SOURCE_AND_MANIFEST")
    doc = json.loads(data["SOURCE-MANIFEST.json"])
    need(doc["entrypoints"] == {"build": "software/v5/ordinary_current_distribution/build.py"} and
         set(doc["files"]) == expected and
         all(doc["files"][name] == pin(originals[name]) for name in expected), "CURRENT_MANIFEST_SELECTION")
    passed = ["exact_current_source_pack_and_independent95path_census"]

    def fixture(name, *, omit=None, extra=False, corrupt_map=False):
        check(); target = output/name
        target.mkdir()
        for path, content in sorted(data.items()):
            check()
            if path == omit:
                continue
            fresh(target/path, content+b"\n" if corrupt_map and path == MAP else content)
        if extra:
            fresh(target/"EXTRA.txt", b"deliberate extra fixture file")
        return target

    relocated = fixture("relocated-source")
    command = [sys.executable, "-I", "-S", "-B", str(relocated/PREFIX/"bundle.py"),
               "verify", "--source-root", str(relocated),
               "--manifest-sha256", receipt["manifest"]["sha256"]]
    check()
    result = subprocess.run(command, cwd=output, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=max(0.01, 60-(time.monotonic()-start)),
        creationflags=subprocess.CREATE_NO_WINDOW, check=False)
    fresh(output/"relocated-stdout.txt", result.stdout)
    fresh(output/"relocated-stderr.txt", result.stderr)
    need(result.returncode == 0 and not result.stderr and len(result.stdout) <= 65536, "RELOCATED_PUBLIC_VERIFY")
    verified = json.loads(result.stdout)
    need(verified["status"] == "VERIFIED_EXACT_SOURCE_NOT_BUILT" and
         verified["payload_files"] == 95 and verified["manifest"] == receipt["manifest"],
         "RELOCATED_VERIFY_BINDING")
    passed.append("actual_relocated_public_verifier")
    refuses(lambda: utility.verify(relocated, "0"*64, check=check), "SOURCE_BUNDLE_MANIFEST_PIN")
    passed.append("wrong_external_manifest_pin_refused")
    missing = fixture("missing-source", omit="software/v5/ordinary_demand_frontier/owner.py")
    refuses(lambda: utility.verify(missing, receipt["manifest"]["sha256"], check=check),
            "SOURCE_BUNDLE_EXACT_CENSUS")
    passed.append("missing_current_source_refused")
    extra = fixture("extra-source", extra=True)
    refuses(lambda: utility.verify(extra, receipt["manifest"]["sha256"], check=check),
            "SOURCE_BUNDLE_EXTRA_OR_ALIASED_FILE")
    passed.append("extra_source_refused")
    wrong_map = fixture("changed-map", corrupt_map=True)
    refuses(lambda: utility.verify(wrong_map, receipt["manifest"]["sha256"], check=check),
            "SOURCE_BUNDLE_SOURCE_MAP_PIN")
    passed.append("changed_current_map_refused")
    stale = deepcopy(doc)
    stale["entrypoints"]["overlay"] = "software/v5/ordinary_fair_search/assemble.py"
    refuses(lambda: utility.validate_manifest(stale), "SOURCE_BUNDLE_MANIFEST_PROFILE")
    passed.append("obsolete_overlay_entrypoint_refused")
    for name, original in originals.items():
        check(); need((root/name).read_bytes() == original and (relocated/name).read_bytes() == original,
                      "SOURCE_OR_RELOCATED_INPUT_CHANGED")
    need({p.relative_to(relocated).as_posix() for p in relocated.rglob("*") if p.is_file()} ==
         expected | {"SOURCE-MANIFEST.json"}, "RELOCATED_EXACT_FINAL_CENSUS")
    report = {"status": "CURRENT_SOURCE_BUNDLE_FOCUSED_CONTROLS_PASSED", "groups": passed,
              "bundle_sha256": BUNDLE_SHA, "map_sha256": MAP_SHA, "receipt": receipt,
              "relocated_source": str(relocated), "public_verifier": verified,
              "child_launches": 1, "native_builds": 0, "product_imports": 0, "owner_operations": 0,
              "claim": "EXACT_SOURCE_PACK_AND_RELOCATION_NOT_NATIVE_OR_MATHEMATICAL_ACCEPTANCE"}
    fresh(output/"RESULT.json", json.dumps(report, sort_keys=True, separators=(",", ":"),
          ensure_ascii=True, allow_nan=False).encode("ascii"))
    print(json.dumps(report, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

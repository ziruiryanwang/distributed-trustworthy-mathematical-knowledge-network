"""File-only standalone inert-host ZIP and verified extraction.

The external source-profile and guide pins select all shipped bytes. No product,
native, owner, storage or network code executes. Approved immutable inputs and
the existing bounded file-helper policy are explicit premises.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import sys
import time
import zipfile

HELPER = "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
MODULES = (
    "ordinary_evidence ordinary_semantics portable_evidence portable_candidate "
    "ordinary_preview portable_preview formal_query baseline_bundle "
    "discovery.formal_features discovery.authenticated_index discovery.pair_access "
    "discovery.discovery_store discovery.discovery_query discovery.candidate_query "
    "discovery.summary_wire discovery.ordinary_export_adapter custody.module_store "
    "transport.http_provider transport.clients transport.ordinary_acquisition "
    "transport.authoring_offers transport.contact_directory").split()
PATHS = {name: "support/" + name.replace(".", "/") + ".py" for name in MODULES}
PATHS.update({"_entry": "run.py", "_support": "support.py", "_core": "host_core.py",
              "_supervisor": "supervisor/commons.py", "domains": "supervisor/domains.py",
              "_job": "supervisor/run_stage.py"})


def need(ok, code):
    if not ok:
        raise ValueError("INERT_ASSEMBLY_" + code)


def assemble(args):
    started, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON")
    source_root = Path(args.source_root)
    helper_path = source_root / HELPER
    need(source_root.is_absolute() and helper_path.is_file() and
         0 < helper_path.stat().st_size <= 2 * 1024**2, "HELPER")
    with helper_path.open("rb") as stream:
        helper_raw = stream.read(2 * 1024**2 + 1)
    need(hashlib.sha256(helper_raw).hexdigest() == HELPER_SHA, "HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_inert_assembly_files", helper_path)
    H = importlib.util.module_from_spec(spec)
    exec(compile(helper_raw, str(helper_path), "exec", dont_inherit=True), H.__dict__)

    def check():
        need(time.monotonic() - started < 45 and time.process_time() - cpu < 20,
             "ALLOWANCE")

    source_root = H.ordinary(source_root, directory=True)
    profile_path = H.ordinary(Path(args.profile))
    guide_path = H.ordinary(Path(args.guide))
    own_path = H.ordinary(Path(__file__).absolute())
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    need(not source_root.is_relative_to(output), "OUTPUT_CONTAINS_SOURCE")
    selected_paths = (profile_path, guide_path, helper_path, own_path)
    for path in selected_paths:
        need(not path.is_relative_to(output) and not output.is_relative_to(path),
             "OUTPUT_OVERLAP")
    profile, profile_pin = H.read_json(profile_path, args.profile_sha256, check)
    need(set(profile) == {"schema", "python", "files"} and
         profile["schema"] == "DMKN_INERT_HOST_SOURCES_V1" and
         type(profile["files"]) is dict and set(profile["files"]) == set(PATHS),
         "PROFILE_LAYOUT")
    python = profile["python"]
    need(type(python) is dict and set(python) == {"version", "files"} and
         python["version"] == "3.14.6" and type(python["files"]) is dict and
         set(python["files"]) == {"python.exe", "python3.dll", "python314.dll"},
         "PYTHON_SELECTION")
    for pin in python["files"].values():
        H.pin_shape(pin)

    captured, sources, expected = {}, {}, {}

    def capture(name, path, pin):
        check(); H.relative(name); H.pin_shape(pin)
        need(pin["bytes"] <= 2 * H.MIB and
             not path.is_relative_to(output) and not output.is_relative_to(path),
             "PAYLOAD_BOUND_OR_OVERLAP")
        need(H.pin(path, check, 2 * H.MIB) == pin, "SOURCE_PIN")
        with H.ordinary(path).open("rb") as stream:
            raw = stream.read(2 * H.MIB + 1)
        need({"bytes": len(raw), "sha256": H.digest(raw)} == pin, "CAPTURE_PIN")
        need(name not in captured, "DUPLICATE_PAYLOAD")
        captured[name], sources[name], expected[name] = raw, path, pin

    for role, record in profile["files"].items():
        need(type(record) is dict and set(record) == {"path", "source", "bytes", "sha256"}
             and record["path"] == PATHS[role], "ROLE")
        relative = H.relative(record["source"])
        need(relative.startswith("software/v5/"), "SOURCE_SCOPE")
        capture(record["path"], source_root / relative,
                {"bytes": record["bytes"], "sha256": record["sha256"]})
    guide_pin = H.pin(guide_path, check, 2 * H.MIB)
    need(guide_pin["sha256"] == H.hexid(args.guide_sha256), "GUIDE_PIN")
    capture("SOURCES.json", profile_path, profile_pin)
    capture("USAGE.md", guide_path, guide_pin)
    own_pin = H.pin(own_path, check, 2 * H.MIB)
    need(len(captured) == 30 and len({name.casefold() for name in captured}) == 30
         and sum(map(len, captured.values())) <= 4 * H.MIB, "DISTRIBUTION_BOUND")

    output.mkdir()
    archive = output / "inert-host.zip"
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_STORED) as packed:
        for name in sorted(captured):
            check()
            entry = zipfile.ZipInfo("inert-host/" + name, (1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            packed.writestr(entry, captured[name])
    package = output / "inert-host"
    package.mkdir()
    with zipfile.ZipFile(archive, "r") as packed:
        need(packed.namelist() == ["inert-host/" + name for name in sorted(captured)],
             "ARCHIVE_CENSUS")
        for name, original in sorted(captured.items()):
            check()
            entry = packed.getinfo("inert-host/" + name)
            need(entry.file_size == len(original) and entry.compress_type == zipfile.ZIP_STORED
                 and entry.compress_size == len(original), "ARCHIVE_ENTRY")
            raw = packed.read(entry)
            need(raw == original, "ARCHIVE_BYTES")
            target = package / name
            target.parent.mkdir(parents=True, exist_ok=True)
            H.ordinary(target.parent, directory=True)
            H.fresh_bytes(target, raw)
    H.census(package, expected, check)
    for name, pin in expected.items():
        need(H.pin(package / name, check, 2 * H.MIB) == pin and
             H.pin(sources[name], check, 2 * H.MIB) == pin, "FINAL_BINDING")
    need(H.pin(own_path, check, 2 * H.MIB) == own_pin and
         H.pin(helper_path, check, 2 * H.MIB)["sha256"] == HELPER_SHA, "BUILDER_CHANGED")
    report = {
        "schema": "DMKN_INERT_HOST_BUILD_V1", "status": "PACKED_AND_EXTRACTED",
        "profile": profile_pin, "guide": guide_pin, "builder": own_pin,
        "archive": H.pin(archive, check, 8 * H.MIB), "files": expected,
        "payload_bytes": sum(map(len, captured.values())), "payload_files": len(captured),
        "claim": "EXACT_FILE_DISTRIBUTION_NOT_OPERATION_OR_MATHEMATICAL_ACCEPTANCE",
        "wall_seconds": time.monotonic() - started, "cpu_seconds": time.process_time() - cpu,
    }
    check()
    H.fresh_bytes(output / "BUILD.json", H.canonical(report))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source-root", "profile", "profile-sha256", "guide", "guide-sha256", "output"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    result = assemble(args)
    import json
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

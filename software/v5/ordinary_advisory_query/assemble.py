"""Apply the reviewed advisory-query sources to an explicitly selected package.

File-only assembly: no product imports, compiler, network, or mathematical state.
The unchanged native support comes from the exact caller-approved base receipt.
Source and destination must remain under the operator's control during assembly.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import sys
import time

HELPER = "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
COMPATIBILITY = "software/v5/ordinary_current_operator_kit/compatibility.json"
COMPATIBILITY_SHA = "08129a60872238eb5dec174fb21a996fc7f5db69748ae623121fe3b51c4af719"
PREFIX = "software/v5/ordinary_advisory_query/"
PAYLOAD_MAP_SHA = "7678332f97cd86429c820d24ec29a7ea737616dd1b065e38e284d72d194e33cf"
PAYLOAD_SOURCES = {'query.py': 'software/v5/ordinary_advisory_query/query.py', 'profile.py': 'software/v5/ordinary_advisory_query/profile.py', 'advisory_context.py': 'software/v5/ordinary_advisory_query/advisory_context.py', 'LAUNCHER.md': 'software/v5/ordinary_advisory_query/LAUNCHER.md', 'run.py': 'software/v5/ordinary_symbol_query/run.py'}
PAYLOAD_NAMES = set(PAYLOAD_SOURCES)


def assemble(args):
    started, cpu = time.monotonic(), time.process_time()
    if not (os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
            sys.dont_write_bytecode and not sys.flags.optimize):
        raise ValueError("SYMBOL_ASSEMBLY_PYTHON")
    source_root = Path(args.source_root)
    helper_path = source_root / HELPER
    # Bounded read before executing the already reviewed file/path helpers.
    with helper_path.open("rb") as stream:
        helper_raw = stream.read(2 * 1024**2 + 1)
    if hashlib.sha256(helper_raw).hexdigest() != HELPER_SHA:
        raise ValueError("SYMBOL_ASSEMBLY_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_symbol_assembly_helpers", helper_path)
    H = importlib.util.module_from_spec(spec)
    exec(compile(helper_raw, str(helper_path), "exec"), H.__dict__)

    def check():
        H.need(time.monotonic() - started < 60 and time.process_time() - cpu < 30,
               "SYMBOL_ASSEMBLY_ALLOWANCE")

    source_root = H.ordinary(source_root, directory=True)
    H.need(H.pin(helper_path, check, 2 * H.MIB)["sha256"] == HELPER_SHA,
           "SYMBOL_HELPER_CHANGED")
    base = H.ordinary(Path(args.base_package), directory=True)
    receipt_path = H.ordinary(Path(args.base_receipt))
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    for path in (base, receipt_path, source_root / PREFIX):
        H.need(not output.is_relative_to(path) and not path.is_relative_to(output),
               "SYMBOL_OUTPUT_OVERLAP")
    H.need(not source_root.is_relative_to(output), "SYMBOL_OUTPUT_CONTAINS_SOURCE")
    profile, profile_pin = H.read_json(base / "PROFILE.json", args.base_profile_sha256, check)
    receipt, receipt_pin = H.read_json(receipt_path, args.base_receipt_sha256, check)
    compatibility, _ = H.read_json(source_root / COMPATIBILITY, COMPATIBILITY_SHA, check)
    payloads, map_pin = H.read_json(source_root / PREFIX / "PAYLOADS.json", PAYLOAD_MAP_SHA, check)
    H.need(set(payloads) == PAYLOAD_NAMES, "SYMBOL_PAYLOAD_ROLES")
    H.need(set(profile) == {"schema", "installation_manifest_sha256", "helper_paths",
                           "author_worker", "files"} and
           profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
           profile["helper_paths"] == ["authoring/helpers"] and
           profile["author_worker"] == "author_worker.py", "SYMBOL_BASE_PROFILE")
    direct, generated = compatibility["direct_sources"], compatibility["generated_roles"]
    H.need(set(profile["files"]) == set(direct) | set(generated) and
           len(direct) == 45 and len(generated) == 72 and
           all(profile["files"][name] == pin for name, pin in direct.items()),
           "SYMBOL_BASE_INTERFACE")
    baseline = receipt.get("files")
    H.need(receipt.get("status") == "BUILT_NOT_ADOPTED" and
           receipt.get("profile_sha256") == args.base_profile_sha256 and
           receipt.get("installation_manifest_sha256") == profile["installation_manifest_sha256"] and
           type(baseline) is dict and len(baseline) == 154 and
           baseline.get("PROFILE.json") == profile_pin and
           all(baseline.get(name) == pin for name, pin in profile["files"].items()),
           "SYMBOL_BASE_RECEIPT")
    H.census(base, baseline, check)
    for name, pin in baseline.items():
        H.relative(name); H.pin_shape(pin)
        H.need(H.pin(base / name, check) == pin, "SYMBOL_BASE_BYTES")
    selected = {name: base / name for name in baseline if name != "PROFILE.json"}
    expected = dict(baseline)
    for name, pin in payloads.items():
        H.pin_shape(pin)
        source = source_root / PAYLOAD_SOURCES[name]
        H.need(H.pin(source, check, 2 * H.MIB) == pin and pin != baseline.get(name),
               "SYMBOL_SOURCE_PIN")
        selected[name], expected[name] = source, pin
    new_profile = H.canonical(dict(profile, files=dict(profile["files"],
        **{name: expected[name] for name in ("query.py", "run.py", "profile.py", "advisory_context.py")})))
    expected["PROFILE.json"] = {"bytes": len(new_profile), "sha256": H.digest(new_profile)}
    changed = sorted(name for name in baseline if expected[name] != baseline[name])
    added = sorted(set(expected) - set(baseline))
    H.need(changed == ["LAUNCHER.md", "PROFILE.json", "profile.py", "query.py", "run.py"] and
           added == ["advisory_context.py"] and
           sum(pin["bytes"] for pin in expected.values()) <= 256 * H.MIB,
           "SYMBOL_EXACT_DELTA")
    output.mkdir(); package = output / "package"; package.mkdir()
    for name, origin in sorted(selected.items()):
        check(); target = package / H.relative(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        H.ordinary(target.parent, directory=True)
        with H.ordinary(origin).open("rb") as incoming, H.ordinary(target, fresh=True).open("xb") as outgoing:
            shutil.copyfileobj(incoming, outgoing, H.MIB)
            outgoing.flush(); os.fsync(outgoing.fileno())
        H.need(H.pin(target, check) == expected[name], "SYMBOL_COPY_READBACK")
    H.census(package, selected, check); H.census(base, baseline, check)
    for name, pin in baseline.items():
        H.need(H.pin(base / name, check) == pin, "SYMBOL_BASE_CHANGED")
    for name, origin in selected.items():
        H.need(H.pin(origin, check) == expected[name] and H.pin(package / name, check) == expected[name],
               "SYMBOL_SOURCE_OR_OUTPUT_CHANGED")
    H.need(H.pin(receipt_path, check) == receipt_pin and
           H.pin(source_root / PREFIX / "PAYLOADS.json", check) == map_pin and
           H.pin(helper_path, check)["sha256"] == HELPER_SHA,
           "SYMBOL_INPUT_CHANGED")
    H.fresh_bytes(package / "PROFILE.json", new_profile)
    H.census(package, expected, check)
    H.need(H.pin(package / "PROFILE.json", check) == expected["PROFILE.json"], "SYMBOL_PROFILE")
    report = {"status": "ASSEMBLED_NOT_ADOPTED", "package": str(package), "files": expected,
        "base_receipt_sha256": args.base_receipt_sha256,
        "base_profile_sha256": args.base_profile_sha256,
        "profile_sha256": expected["PROFILE.json"]["sha256"],
        "installation_manifest_sha256": profile["installation_manifest_sha256"],
        "implementation_id": receipt["implementation_id"], "changed_files": changed,
        "added_files": added, "unchanged_files": len(baseline) - len(changed), "native_calls": 0, "owner_opened": False,
        "payload_map": map_pin, "wall_seconds": time.monotonic() - started,
        "cpu_seconds": time.process_time() - cpu,
        "claim": "FILE_ASSEMBLY_NOT_RUNTIME_OR_MATHEMATICAL_ACCEPTANCE"}
    check(); H.fresh_bytes(output / "ASSEMBLY.json", H.canonical(report)); check()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for option in ("source-root", "base-package", "base-receipt", "base-receipt-sha256",
                   "base-profile-sha256", "output"):
        parser.add_argument("--" + option, required=True)
    report = assemble(parser.parse_args())
    import json
    print(json.dumps(report, sort_keys=True, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    main()

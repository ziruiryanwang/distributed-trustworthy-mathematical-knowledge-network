"""Restore exact saved-manifest preimages; never produce or accept new evidence."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import time
import types

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE_ROOT = Path(__file__).resolve().parents[3]
LOCAL = ROOT / "experiments/v5-local-checks"
HELPER = "software/v5/ordinary_binding_reuse/measure_saved_writer.py"
HELPER_BYTES = 8449
HELPER_SHA = "42670eb615d3ba69140804ce8af593a4f984d283156dfbab08a589684ceecd1c"
MANIFEST = LOCAL / "binding-saved-writer01/binding/manifest.json"
MANIFEST_BYTES = 468097
MANIFEST_SHA = "1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c"
TARGET_UNIT = "ab6f1b22d8760ba5615e9ec7e5a1fda99313c71a8cab34183c2fe88aad31381c"
TARGET_EXPORT = "bf281176862c75a7c8be1d00359f85bdcfe4904f4aefd5977c954e822e79070c"
START, CPU_START = time.monotonic(), time.process_time()
PHASE, ACTIVE_UNIT, WRITTEN, WRITTEN_BYTES = "SETUP", None, 0, 0


def need(ok, code):
    if not ok:
        raise ValueError("STD_RECONSTRUCT_" + code)


def budget():
    need(time.monotonic()-START <= 90 and time.process_time()-CPU_START <= 70,
         "FIXED_90_WALL_70_CPU")


def helper():
    path = SOURCE_ROOT / HELPER
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and not
         getattr(info, "st_file_attributes", 0) & 0x400 and info.st_size == HELPER_BYTES,
         "HELPER_FILE")
    with path.open("rb") as stream:
        raw = stream.read(HELPER_BYTES+1)
    need(len(raw) == HELPER_BYTES and hashlib.sha256(raw).hexdigest() == HELPER_SHA,
         "HELPER_PIN")
    module = types.ModuleType("_std_reconstruction_saved_helper")
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    module.START, module.CPU_START = START, CPU_START
    return module


def main():
    global PHASE, ACTIVE_UNIT, WRITTEN, WRITTEN_BYTES
    need(os.name == "nt" and Path.cwd() == ROOT and len(sys.argv) == 2 and
         sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize, "PROCESS")
    budget()
    M = helper()
    output = Path(sys.argv[1])
    need(output.is_absolute() and output.name == "materialized" and
         output.parent.name == "std-reconstruct01" and output.parent.parent == LOCAL and
         output.parent.resolve(strict=True) == output.parent, "FRESH_OUTPUT_LOCATION")
    output.mkdir()
    units_directory = output / "units"
    units_directory.mkdir()
    input_keys = ("ordinary_evidence", "ordinary_semantics", "portable_evidence",
                  "writer", "inventory", "request")
    E, S, PE = [M.load(key) for key in input_keys[:3]]
    PHASE = "PIN_FIXED_INPUTS"
    writer, inventory, request = [M.pinned(key) for key in input_keys[3:]]
    manifest_raw = M.read(MANIFEST, MANIFEST_BYTES)
    need(len(manifest_raw) == MANIFEST_BYTES and M.sha(manifest_raw) == MANIFEST_SHA,
         "SAVED_MANIFEST_PIN")
    PHASE = "DECODE_KNOWN_MANIFEST"
    manifest = json.loads(manifest_raw)
    semantic, foundation = S.semantic_id(), S.foundation_id()
    need(manifest["semantic_id"] == semantic and len(manifest["batches"]) == 3,
         "MANIFEST_SEMANTICS")
    entries = [row for batch in manifest["batches"] for row in batch]
    batches = [{"units": len(batch), "bytes": sum(row["raw_bytes"] for row in batch)}
               for batch in manifest["batches"]]
    need(batches == [{"units": 1024, "bytes": 9997243},
                     {"units": 1024, "bytes": 17147916},
                     {"units": 603, "bytes": 17767684}] and len(entries) == 2651,
         "SAVED_BATCH_CENSUS")
    expected = {}
    for entry in entries:
        need(set(entry) == {"unit_id", "raw_sha256", "raw_bytes"} and
             all(re.fullmatch(r"[0-9a-f]{64}", entry[key]) is not None
                 for key in ("unit_id", "raw_sha256")) and
             type(entry["raw_bytes"]) is int and 0 < entry["raw_bytes"] <= 8*1024**2,
             "MANIFEST_ENTRY")
        name = "units/" + entry["unit_id"] + ".json"
        need(name not in expected, "MANIFEST_DUPLICATE")
        expected[name] = {"bytes": entry["raw_bytes"], "sha256": entry["raw_sha256"]}

    PHASE = "DECODE_PINNED_WRITER"
    # These exact bytes already passed the preserved diagnostic's general parser.
    # This is not an arbitrary-input API: final output hashes are independently fixed.
    doc, basis, requested = json.loads(writer), json.loads(inventory), json.loads(request)
    budget()
    fixed_names = [row[0] for row in basis]
    need(len(basis) == 581 and doc["basis_names"] == fixed_names and
         doc["targets"] == requested["targets"] and len(doc["targets"]) == 1 and
         len(doc["units"]) == len(entries), "PINNED_INPUT_CENSUS")
    available = {E.name_key(name): S.basis_symbol_id(semantic, foundation, name) for name in fixed_names}
    need(len(available) == 581, "FIXED_BASIS_NAMES")
    target_key = E.name_key(doc["targets"][0])
    PHASE = "PARTIAL_BEFORE"
    partial = M.partial_census()
    partial_directory = ROOT / M.FIXTURE / "units"
    partial_names = {path.name for path in partial_directory.iterdir()}
    need(len(partial_names) == 708, "PARTIAL_CENSUS")
    compared, target = set(), None

    def write_exact(path, raw, expected_pin):
        budget()
        need(path.parent in (output, units_directory) and
             {"bytes": len(raw), "sha256": M.sha(raw)} == expected_pin, "WRITE_INPUT")
        with path.open("xb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        need(M.read(path, expected_pin["bytes"]) == raw, "WRITE_READBACK")

    for index, (unit, entry) in enumerate(zip(doc["units"], entries, strict=True)):
        ACTIVE_UNIT = index
        PHASE = "INSPECT_REFERENCES"
        budget()
        census = E.inspect_unit(unit)
        need(all(key in available for key in census.external_names), "UNBOUND_REFERENCE")
        PHASE = "ENCODE_PREIMAGE"
        imports = [[json.loads(key), available[key]] for key in census.external_names]
        raw = E.canonical_json({"schema": PE.SCHEMA, "semantic_id": semantic,
                                "imports": imports, "unit": unit})
        PHASE = "MATCH_SAVED_PREIMAGE"
        name = "units/" + entry["unit_id"] + ".json"
        need({"bytes": len(raw), "sha256": M.sha(raw)} == expected[name] and
             hashlib.sha256(PE.EVIDENCE_DOMAIN.encode("ascii") + b"\0" + raw).hexdigest() == entry["unit_id"],
             "EXACT_MANIFEST_PREIMAGE")
        if Path(name).name in partial_names:
            need(M.read(partial_directory / Path(name).name, len(raw)) == raw,
                 "OLD_PARTIAL_EXACT_BYTES")
            compared.add(Path(name).name)
        PHASE = "WRITE_EXACT_UNIT"
        write_exact(output / name, raw, expected[name])
        WRITTEN += 1
        WRITTEN_BYTES += len(raw)
        PHASE = "BIND_ALREADY_MATCHED_OUTPUTS"
        for row in unit[2]:
            key = E.name_key(row[0])
            need(key not in available, "DUPLICATE_OUTPUT")
            symbol = S.export_id(semantic, entry["unit_id"], row[0])
            available[key] = symbol
            if key == target_key:
                need(target is None, "DUPLICATE_TARGET")
                target = {"name": row[0], "export_id": symbol, "unit_id": entry["unit_id"]}
    ACTIVE_UNIT = None
    need(WRITTEN == 2651 and WRITTEN_BYTES == 44912843 and compared == partial_names and
         target is not None and target["unit_id"] == TARGET_UNIT and target["export_id"] == TARGET_EXPORT,
         "COMPLETE_RECONSTRUCTION")
    PHASE = "FINAL_INPUT_PINS"
    for key in input_keys:
        M.pinned(key)
    need(M.read(MANIFEST, MANIFEST_BYTES) == manifest_raw and
         M.sha(M.read(SOURCE_ROOT / HELPER, HELPER_BYTES)) == HELPER_SHA and
         M.partial_census() == partial, "FINAL_INPUT_CHANGED")

    def census_output():
        budget()
        need({path.name for path in output.iterdir()} ==
             {"units"} | {name for name in expected if "/" not in name}, "ROOT_CENSUS")
        info = units_directory.lstat()
        need(stat.S_ISDIR(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "UNITS_DIRECTORY")
        seen, total = set(), 0
        with os.scandir(units_directory) as children:
            for child in children:
                budget()
                name = "units/" + child.name
                need(name in expected and name not in seen and len(seen) < 2651, "UNIT_CENSUS")
                expected_pin = expected[name]
                raw = M.read(Path(child.path), expected_pin["bytes"])
                need({"bytes": len(raw), "sha256": M.sha(raw)} == expected_pin, "FINAL_UNIT_PIN")
                seen.add(name); total += len(raw)
        need(seen == {name for name in expected if name.startswith("units/")} and
             len(seen) == 2651 and total == 44912843, "COMPLETE_UNIT_CENSUS")
        for name, expected_pin in expected.items():
            if "/" not in name:
                raw = M.read(output / name, expected_pin["bytes"])
                need({"bytes": len(raw), "sha256": M.sha(raw)} == expected_pin, "FINAL_METADATA_PIN")
        return {"unit_files": len(seen), "unit_bytes": total, "files": len(expected),
                "bytes": sum(row["bytes"] for row in expected.values())}

    PHASE = "PRE_MANIFEST_CENSUS"
    census_output()
    report = {"schema": "DMKN_RETAINED_STD_EXACT_RECONSTRUCTION_V1",
        "status": "PREPARED_FOR_MANIFEST_NOT_COMPLETION", "binder_calls": 0,
        "mathematical_acceptance": False, "original_public_production": "FAILED_UNCHANGED",
        "failed_materialize01": "FAILED_UNCHANGED",
        "manifest": {"path": "manifest.json", "bytes": MANIFEST_BYTES, "sha256": MANIFEST_SHA},
        "semantic_id": semantic, "batches": batches, "targets": [target],
        "partial_comparison": {**partial, "all_compared_exactly": True},
        "input_pins": {key: M.PINS[key][2] for key in input_keys},
        "saved_helper_sha256": HELPER_SHA, "inner_limits": {"wall_seconds": 90, "cpu_seconds": 70},
        "wall_seconds_before_manifest": time.monotonic()-START,
        "cpu_seconds_before_manifest": time.process_time()-CPU_START,
        "claim": "EXACT_SAVED_MANIFEST_PREIMAGES_ONLY_NOT_NEW_PRODUCTION_OR_MATHEMATICAL_ACCEPTANCE"}
    report_raw = E.canonical_json(report)
    need(len(report_raw) <= 128*1024, "REPORT_BOUND")
    expected["RECONSTRUCTION.json"] = {"bytes": len(report_raw), "sha256": M.sha(report_raw)}
    PHASE = "PREPARED_METADATA"
    write_exact(output / "RECONSTRUCTION.json", report_raw, expected["RECONSTRUCTION.json"])
    expected["manifest.json"] = {"bytes": MANIFEST_BYTES, "sha256": MANIFEST_SHA}
    PHASE = "MANIFEST_LAST"
    write_exact(output / "manifest.json", manifest_raw, expected["manifest.json"])
    PHASE = "FINAL_CENSUS"
    final_census = census_output()
    budget()
    return {"status": "RESTORED_EXACT_INERT_BASELINE_NOT_ACCEPTED", "output": str(output),
        "manifest_path": str(output / "manifest.json"), "manifest": expected["manifest.json"],
        "report": expected["RECONSTRUCTION.json"], "census": final_census,
        "binder_calls": 0, "mathematical_acceptance": False,
        "original_public_production": "FAILED_UNCHANGED", "failed_materialize01": "FAILED_UNCHANGED",
        "wall_seconds": time.monotonic()-START, "cpu_seconds": time.process_time()-CPU_START}


if __name__ == "__main__":
    try:
        print(json.dumps(main(), sort_keys=True, separators=(",", ":")))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "phase": PHASE, "active_unit_index": ACTIVE_UNIT,
            "unit_files_written": WRITTEN, "unit_bytes_written": WRITTEN_BYTES,
            "error": type(exc).__name__ + ":" + str(exc), "wall_seconds": time.monotonic()-START,
            "cpu_seconds": time.process_time()-CPU_START}, sort_keys=True))
        raise SystemExit(1)

"""Materialize the retained genuine Std writer; no native export or acceptance.

Test-only finite continuation. Reuse the frozen saved-writer input/binding helper;
write a fresh exact full bundle, never alter or recover the failed producer run.
"""
from dataclasses import asdict
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
MIB = 1024**2
START, CPU_START = time.monotonic(), time.process_time()
PHASE = "SETUP"


def need(ok, code):
    if not ok:
        raise ValueError("STD_MATERIALIZE_" + code)


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
    module = types.ModuleType("_std_materialization_saved_helper")
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    # Preserve the helper's identical cumulative cap, including our bootstrap.
    module.START, module.CPU_START = START, CPU_START
    return module


def main():
    global PHASE
    need(os.name == "nt" and Path.cwd() == ROOT and len(sys.argv) == 2 and
         sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize, "PROCESS")
    budget()
    M = helper()
    output = Path(sys.argv[1])
    need(output.is_absolute() and output.name == "materialized" and
         output.parent.parent == LOCAL and output.parent.resolve(strict=True) == output.parent,
         "FRESH_OUTPUT_LOCATION")
    output.mkdir()
    units = output / "units"
    units.mkdir()

    def write_exact(path, raw, expected):
        budget()
        need(path.parent in (output, units) and
             {"bytes": len(raw), "sha256": M.sha(raw)} == expected, "WRITE_INPUT")
        with path.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        need(M.read(path, expected["bytes"]) == raw, "WRITE_READBACK")

    def census(expected):
        budget()
        need({path.name for path in output.iterdir()} ==
             {"units"} | {name for name in expected if "/" not in name}, "ROOT_CENSUS")
        info = units.lstat()
        need(stat.S_ISDIR(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "UNITS_DIRECTORY")
        seen, total = set(), 0
        with os.scandir(units) as entries:
            for entry in entries:
                budget()
                name = "units/" + entry.name
                need(name in expected and name not in seen and len(seen) < 2651,
                     "UNIT_CENSUS")
                pin = expected[name]
                raw = M.read(Path(entry.path), pin["bytes"])
                need({"bytes": len(raw), "sha256": M.sha(raw)} == pin, "FINAL_UNIT_PIN")
                seen.add(name); total += len(raw)
        need(seen == {name for name in expected if name.startswith("units/")} and
             len(seen) == 2651 and total == 44912843, "COMPLETE_UNIT_CENSUS")
        for name, pin in expected.items():
            if "/" not in name:
                raw = M.read(output/name, pin["bytes"])
                need({"bytes": len(raw), "sha256": M.sha(raw)} == pin, "FINAL_METADATA_PIN")
        return {"unit_files": len(seen), "unit_bytes": total, "files": len(expected),
                "bytes": sum(pin["bytes"] for pin in expected.values())}

    E, S, PE, C, B = [M.load(key) for key in (
        "ordinary_evidence", "ordinary_semantics", "portable_evidence", "portable_candidate", "new_bundle")]
    writer, inventory, request = [M.pinned(key) for key in ("writer", "inventory", "request")]
    saved_manifest = M.read(MANIFEST, MANIFEST_BYTES)
    need(len(saved_manifest) == MANIFEST_BYTES and M.sha(saved_manifest) == MANIFEST_SHA,
         "SAVED_MANIFEST_PIN")
    PHASE = "PARTIAL_BEFORE"
    M.partial_census()
    PHASE = "BIND_ONCE"
    bind_wall, bind_cpu = time.monotonic(), time.process_time()
    bundle = B.bind_writer(writer, inventory, json.loads(request)["targets"], check_budget=budget)
    binding_cost = {"wall_seconds": time.monotonic()-bind_wall,
                    "cpu_seconds": time.process_time()-bind_cpu}
    need(not bundle.mathematical_acceptance and bundle.manifest.raw == saved_manifest and
         bundle.manifest.unit_count == 2651, "EXACT_SAVED_COMPLETE_MANIFEST")
    bound, expected, batches = {}, {}, []
    for entries, raws in zip(bundle.manifest.batches, bundle.batches, strict=True):
        size = 0
        for entry, raw in zip(entries, raws, strict=True):
            budget()
            need(re.fullmatch(r"[0-9a-f]{64}", entry.unit_id) is not None and
                 entry.relative_path == "units/" + entry.unit_id + ".json" and
                 entry.unit_id not in bound and len(raw) == entry.raw_bytes and
                 M.sha(raw) == entry.raw_sha256, "EXACT_ENTRY")
            bound[entry.unit_id] = raw
            expected[entry.relative_path] = {"bytes": entry.raw_bytes, "sha256": entry.raw_sha256}
            size += len(raw)
        batches.append({"units": len(entries), "bytes": size})
    need(batches == [{"units": 1024, "bytes": 9997243},
                     {"units": 1024, "bytes": 17147916},
                     {"units": 603, "bytes": 17767684}] and
         len(bound) == bundle.census.units == 2651 and bundle.census.bytes == 44912843,
         "EXACT_BATCH_CENSUS")
    PHASE = "PARTIAL_COMPARE"
    partial = M.partial_census(bound)
    PHASE = "WRITE_UNITS"
    for name, pin in expected.items():
        write_exact(output/name, bound[Path(name).stem], pin)
    PHASE = "FINAL_INPUT_PINS"
    for key in M.PINS:
        M.pinned(key)
    need(M.read(MANIFEST, MANIFEST_BYTES) == saved_manifest and
         M.sha(M.read(SOURCE_ROOT/HELPER, HELPER_BYTES)) == HELPER_SHA,
         "FINAL_MANIFEST_OR_HELPER_CHANGED")
    need(M.partial_census(bound) == partial, "FINAL_PARTIAL_CHANGED")
    PHASE = "PRE_MANIFEST_CENSUS"
    census(expected)
    report = {"schema": "DMKN_RETAINED_STD_MATERIALIZATION_V1",
        "status": "PREPARED_FOR_MANIFEST_NOT_COMPLETION", "binder_calls": 1,
        "mathematical_acceptance": False, "original_public_production": "FAILED_UNCHANGED",
        "manifest": {"path": "manifest.json", "bytes": MANIFEST_BYTES, "sha256": MANIFEST_SHA},
        "semantic_id": bundle.manifest.semantic_id, "aggregate": asdict(bundle.census),
        "batches": batches,
        "targets": [{"name": json.loads(t.name), "export_id": t.export_id, "unit_id": t.unit_id}
                    for t in bundle.targets], "partial_comparison": partial,
        "input_pins": {key: row[2] for key, row in M.PINS.items()},
        "saved_helper_sha256": HELPER_SHA, "binding_cost": binding_cost,
        "inner_limits": {"wall_seconds": 90, "cpu_seconds": 70},
        "memory_boundary": "outer 1792 MiB Job; no new internal memory mechanism",
        "wall_seconds_before_manifest": time.monotonic()-START,
        "cpu_seconds_before_manifest": time.process_time()-CPU_START,
        "claim": "EXACT_INERT_MATERIALIZATION_NOT_NATIVE_EXPORT_RECOVERY_OR_MATHEMATICAL_ACCEPTANCE"}
    report_raw = E.canonical_json(report)
    need(len(report_raw) <= 128*1024, "REPORT_BOUND")
    expected["MATERIALIZATION.json"] = {"bytes": len(report_raw), "sha256": M.sha(report_raw)}
    write_exact(output/"MATERIALIZATION.json", report_raw, expected["MATERIALIZATION.json"])
    PHASE = "MANIFEST_WRITE"
    expected["manifest.json"] = {"bytes": MANIFEST_BYTES, "sha256": MANIFEST_SHA}
    write_exact(output/"manifest.json", bundle.manifest.raw, expected["manifest.json"])
    # No required file is written after this manifest. Its presence alone is
    # not completion: the final census and supervising terminal result remain.
    PHASE = "FINAL_CENSUS"
    final_census = census(expected)
    budget()
    return {"status": "MATERIALIZED_INERT_BASELINE_NOT_ACCEPTED", "output": str(output),
        "manifest_path": str(output/"manifest.json"), "manifest": expected["manifest.json"],
        "report": expected["MATERIALIZATION.json"], "census": final_census,
        "binder_calls": 1, "mathematical_acceptance": False,
        "original_public_production": "FAILED_UNCHANGED",
        "wall_seconds": time.monotonic()-START, "cpu_seconds": time.process_time()-CPU_START}


if __name__ == "__main__":
    try:
        print(json.dumps(main(), sort_keys=True, separators=(",", ":")))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "phase": PHASE,
            "error": type(exc).__name__ + ":" + str(exc), "wall_seconds": time.monotonic()-START,
            "cpu_seconds": time.process_time()-CPU_START}, sort_keys=True))
        raise SystemExit(1)

"""One retained Std writer binding; inert diagnostic, never production recovery."""
from dataclasses import asdict
from pathlib import Path
import hashlib
import json
import os
import re
import stat
import sys
import time
import types

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE_ROOT = Path(__file__).resolve().parents[3]
LOCAL = ROOT / "experiments/v5-local-checks"
PACKAGE = "experiments/v5-local-checks/multi-source-package01/suite/assembled/package/"
FIXTURE = "experiments/v5-local-checks/std-export01/bundle/"
PINS = {
    "ordinary_evidence": (PACKAGE + "installation/py/ordinary_evidence.py", 17058, "fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6"),
    "ordinary_semantics": (PACKAGE + "installation/py/ordinary_semantics.py", 10283, "ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915"),
    "portable_evidence": (PACKAGE + "installation/py/portable_evidence.py", 2993, "f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8"),
    "portable_candidate": (PACKAGE + "authoring/py/portable_candidate.py", 10437, "29ae111a362472b09b2b1ff16b567b352be793d76c2cd1b5421e0aee29219331"),
    "new_bundle": ("software/v5/ordinary_binding_reuse/baseline_bundle.py", 21363, "e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6"),
    "writer": (FIXTURE + "writer.json", 38154768, "5a2f721127cfef3ae39613c1ec723b2f710cc410c872650fb2acfd7d04078b7a"),
    "inventory": (FIXTURE + "inventory.json", 823690, "c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0"),
    "request": (FIXTURE + "request.json", 496, "bcb647fa96824cc82aebda1dab151a88d678ca3d8756cd150e0103e9f41993bd"),
}
PARTIAL_PIN = "82df4b3e84e8e53a21ab87f94507f0ba8ecbf8c82fbc6fad1e3b0459d6bae4d0"
START, CPU_START = time.monotonic(), time.process_time()
PHASE = "SETUP"


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def budget():
    need(time.monotonic()-START <= 90 and time.process_time()-CPU_START <= 70,
         "FIXED_90_WALL_70_CPU")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ordinary(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and
         not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT,
         "ORDINARY_INPUT_FILE")
    return info


def read(path, maximum):
    budget()
    info = ordinary(path)
    need(0 < info.st_size <= maximum, "INPUT_LENGTH_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == info.st_size, "INPUT_LENGTH_CHANGED")
    budget()
    return raw


def pinned(key):
    relative, length, digest = PINS[key]
    base = SOURCE_ROOT if key == "new_bundle" else ROOT
    raw = read(base / relative, length)
    need(len(raw) == length and sha(raw) == digest, "INPUT_PIN:" + key)
    return raw


def load(key):
    need(key not in sys.modules, "MODULE_ALREADY_LOADED:" + key)
    module = types.ModuleType(key)
    module.__file__ = str((SOURCE_ROOT if key == "new_bundle" else ROOT) / PINS[key][0])
    sys.modules[key] = module
    exec(compile(pinned(key), module.__file__, "exec"), module.__dict__)
    return module


def partial_census(bound=None):
    directory = ROOT / FIXTURE / "units"
    paths = sorted(directory.iterdir(), key=lambda p: p.name)
    need(len(paths) == 708, "EXACT_PARTIAL_FILE_COUNT")
    digest, total = hashlib.sha256(b"PARTIAL_UNITS_V1\0"), 0
    for path in paths:
        need(re.fullmatch(r"[0-9a-f]{64}\.json", path.name), "PARTIAL_FILENAME")
        raw = read(path, 8*1024**2)
        total += len(raw)
        digest.update(f"{path.name}:{len(raw)}:{sha(raw)}\n".encode("ascii"))
        if bound is not None:
            need(path.stem in bound and bound[path.stem] == raw, "PARTIAL_EXACT_BYTES:" + path.name)
    need(total == 6389257 and digest.hexdigest() == PARTIAL_PIN, "PARTIAL_MAP_PIN")
    return {"files": len(paths), "bytes": total, "map_sha256": digest.hexdigest(),
            "all_compared_exactly": bound is not None}


def main():
    global PHASE
    need(os.name == "nt" and len(sys.argv) == 2, "WINDOWS_AND_FRESH_OUTPUT_REQUIRED")
    sys.dont_write_bytecode = True
    budget()
    output = Path(sys.argv[1])
    need(output.is_absolute() and output.name == "binding" and output.parent.parent == LOCAL
         and output.parent.resolve(strict=True) == output.parent, "FRESH_OUTPUT_LOCATION")
    output.mkdir()  # exclusive fresh child of the supervising run; never overwrite
    E, S, PE, C, B = [load(key) for key in (
        "ordinary_evidence", "ordinary_semantics", "portable_evidence", "portable_candidate", "new_bundle")]
    writer, inventory, request = [pinned(key) for key in ("writer", "inventory", "request")]
    targets = json.loads(request)["targets"]
    PHASE = "PARTIAL_BEFORE"
    partial_census()
    PHASE = "BIND_ONCE"
    bind_wall, bind_cpu = time.monotonic(), time.process_time()
    bundle = B.bind_writer(writer, inventory, targets, check_budget=budget)
    bind_cost = {"wall_seconds": time.monotonic()-bind_wall,
                 "cpu_seconds": time.process_time()-bind_cpu}
    need(not bundle.mathematical_acceptance and bundle.manifest.unit_count == 2651,
         "INERT_COMPLETE_UNIT_COUNT")
    PHASE = "SUMMARIZE"
    batches, bound = [], {}
    for entries, raws in zip(bundle.manifest.batches, bundle.batches, strict=True):
        batch_bytes = 0
        for entry, raw in zip(entries, raws, strict=True):
            budget()
            need(entry.unit_id not in bound and entry.raw_bytes == len(raw) and entry.raw_sha256 == sha(raw),
                 "EXACT_BOUND_ENTRY")
            bound[entry.unit_id] = raw
            batch_bytes += len(raw)
        need(len(entries) <= B.DEFAULT_LIMITS.max_batch_units and batch_bytes <= B.DEFAULT_LIMITS.max_batch_bytes,
             "BATCH_UNIT_BYTE_LIMITS")
        batches.append({"units": len(entries), "bytes": batch_bytes})
    need(len(bound) == bundle.census.units == 2651 and
         sum(batch["bytes"] for batch in batches) == bundle.census.bytes, "COMPLETE_CENSUS")
    PHASE = "PARTIAL_COMPARE"
    partial = partial_census(bound)
    PHASE = "FINAL_INPUT_PINS"
    for key in PINS:
        pinned(key)
    budget()
    report = {"schema": "DMKN_SAVED_WRITER_BINDING_DIAGNOSTIC_V1", "status": "PASS",
        "mathematical_acceptance": False, "original_public_production": "FAILED_UNCHANGED",
        "binder_calls": 1,
        "manifest_sha256": sha(bundle.manifest.raw), "manifest_bytes": len(bundle.manifest.raw),
        "aggregate": asdict(bundle.census), "batches": batches,
        "per_batch_nodes_names_edges": "not retained; unchanged binder enforces their limits",
        "targets": [{"name": json.loads(t.name), "export_id": t.export_id, "unit_id": t.unit_id}
                    for t in bundle.targets], "partial_comparison": partial,
        "default_bundle_limits": asdict(B.DEFAULT_LIMITS), "binding_cost": bind_cost,
        "wall_seconds": time.monotonic()-START, "cpu_seconds": time.process_time()-CPU_START,
        "inner_limits": {"wall_seconds": 90, "cpu_seconds": 70},
        "memory_boundary": "requires outer 1792 MiB supervisor; no internal hard memory cap",
        "input_pins": {key: row[2] for key, row in PINS.items()},
        "claim": "one inert binder fit and retained partial byte correspondence; no speedup, admission, native re-export or recovered production"}
    PHASE = "SAVE_SMALL_OUTPUT"
    summary = E.canonical_json(report)
    need(len(summary) <= 128*1024 and len(bundle.manifest.raw) <= 2*1024**2, "SMALL_OUTPUT_BOUND")
    for name, raw in (("manifest.json", bundle.manifest.raw), ("summary.json", summary)):
        budget()
        with (output / name).open("xb") as stream:
            stream.write(raw)
    budget()
    return {"status": "PASS", "summary_sha256": sha(summary), "manifest_sha256": sha(bundle.manifest.raw),
            "output": str(output), "wall_seconds": time.monotonic()-START,
            "cpu_seconds": time.process_time()-CPU_START}


if __name__ == "__main__":
    try:
        print(json.dumps(main(), sort_keys=True, separators=(",", ":")))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "phase": PHASE,
            "error": type(exc).__name__ + ":" + str(exc), "wall_seconds": time.monotonic()-START,
            "cpu_seconds": time.process_time()-CPU_START}, sort_keys=True))
        raise SystemExit(1)

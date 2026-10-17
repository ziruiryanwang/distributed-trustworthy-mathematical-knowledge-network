"""One owner-selected H2 geometry observation, not a proof or admission.

Only this entry file executes from the outer source snapshot. The explicitly
pinned canonical modules are deliberately imported in place. Complete identical
snapshots are retained for audit; this local harness is not a hermetic package.
The enclosing Run-V5-Check Job bounds imports, construction and all final tails.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
CHECKS = ROOT / "experiments/v5-local-checks"
NAME = "geometry17-layout-01"
MIB = 1024**2
OUTER_LIMITS = {"cpu_seconds": 120, "wall_seconds": 180, "memory_mib": 1024,
    "active_processes": 3, "stdout_bytes": MIB, "stderr_bytes": MIB}
NATIVE_LIMITS = {"worker_cpu_seconds": 60, "controller_cpu_seconds": 30,
    "wall_seconds": 120, "memory_mib": 512, "active_processes": 2,
    "stdout_bytes": MIB, "stderr_bytes": MIB, "output_bytes": 208*MIB, "output_entries": 544}
MODULES = (
    "aggregate_geometry", "aggregate_geometry.layout_owner", "aggregate_geometry.adoption",
    "aggregate_geometry.snapshot", "aggregate_small", "aggregate_small.producer",
    "production", "production.producer", "aggregate_claims", "aggregate_claims.bindings",
    "aggregate_claims.input", "aggregate_claims.prepare_mixed", "mixed_claims", "mixed_claims.packet",
    "delta", "delta.packet", "delta.receiver", "delta_claims", "delta_claims.claims",
    "delta_claims.receiver", "admission", "admission.bindings", "admission.verifier",
    "modules", "modules.codec", "aggregate_geometry.prepare_h2")
SELF = "software/v5/aggregate_geometry/run_layout.py"
RUNNER = "tools/Run-V5-Check.py"


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()


def parse(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "DUPLICATE_KEY")
            result[key] = value
        return result
    def reject(value):
        raise ValueError("NONFINITE_JSON:"+value)
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=reject)


def absolute(path, *, directory=False):
    path = Path(path)
    need(path.is_absolute() and path.resolve(strict=True) == path, "EXACT_ABSOLUTE_PATH")
    for item in (path, *path.parents):
        need(not item.is_symlink() and not (item.stat().st_file_attributes & 0x400), "NO_REPARSE")
    need(path.is_dir() if directory else path.is_file(), "PATH_KIND")
    return path


def read(path, maximum=MIB):
    path = absolute(path)
    need(0 < path.stat().st_size <= maximum, "READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(0 < len(raw) <= maximum and path.stat().st_size == len(raw), "READ_SIZE_CHANGED")
    return raw


def pin(path, maximum=128*MIB):
    path = absolute(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "PIN_BOUND")
    h, count = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            count += len(block); need(count <= maximum, "PIN_GREW"); h.update(block)
    need(count == size == path.stat().st_size, "PIN_CHANGED")
    return {"path": str(path), "bytes": size, "sha256": h.hexdigest()}


def save(path, value):
    raw = encoded(value)
    need(len(raw) <= MIB, "REPORT_BOUND")
    absolute(path.parent, directory=True)
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def census(output):
    size, entries = 0, 0
    for directory, dirs, files in os.walk(output, followlinks=False):
        for name in dirs+files:
            path = absolute(Path(directory)/name, directory=name in dirs)
            entries += 1
            if name in files:
                size += path.stat().st_size
            need(size+4*MIB <= 224*MIB and entries+4 <= 640, "OUTER_CUSTODY_BOUND")
    return {"observed_bytes": size, "observed_entries": entries,
        "reserved_tail_bytes": 4*MIB, "reserved_tail_entries": 4,
        "maximum_bytes": 224*MIB, "maximum_entries": 640,
        "scope": "SAMPLED_CENSUS_AND_TAIL_RESERVE_NOT_FILESYSTEM_QUOTA"}


def main():
    wall, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "CANONICAL_ISOLATED_INVOCATION")
    args = argparse.ArgumentParser()
    args.add_argument("--configuration", required=True)
    args.add_argument("--configuration-sha256", required=True)
    args.add_argument("--selection", required=True)
    args = args.parse_args()
    output = CHECKS/NAME
    absolute(output, directory=True)
    selected_path = CHECKS/(NAME+"-selection.json")
    need(Path(args.selection) == selected_path, "EXACT_OUTER_SELECTION_PATH")
    raw_selection = read(selected_path)
    need(read(output/"selection.json") == raw_selection, "ACTUAL_OUTER_SELECTION_COPY")
    selection_pin = pin(selected_path)
    selection = parse(raw_selection)
    need(set(selection) == {"schema", "name", "sources", "runtime_pins", "argv", "limits"}
         and selection["schema"] == "DMKN_V5_LOCAL_CHECK_V1" and selection["name"] == NAME
         and selection["limits"] == OUTER_LIMITS, "EXACT_OUTER_PLAN")
    configuration_path = CHECKS/(NAME+"-configuration.json")
    need(Path(args.configuration) == configuration_path, "EXACT_CONFIGURATION_PATH")
    configuration_pin = pin(configuration_path, MIB)
    need(configuration_pin["sha256"] == args.configuration_sha256, "CONFIGURATION_HASH")
    configuration = parse(read(configuration_path))
    need(configuration["limits"] == NATIVE_LIMITS
         and configuration["output_directory"] == str(output/"evidence"), "EXACT_LAYOUT_LIMITS_OUTPUT")
    runtime, sources = selection["runtime_pins"], selection["sources"]
    need(type(runtime) is dict and 1 <= len(runtime) <= 256, "RUNTIME_MAP")
    relative = {name: "software/v5/"+name.replace(".", "/")+
        (".py" if "." in name else "/__init__.py") for name in MODULES}
    need(type(sources) is dict and set(sources) == set(relative.values())|{SELF, RUNNER},
         "EXACT_28_SOURCE_CLOSURE")
    snapshot = output/"sources"
    need(Path(__file__).resolve() == snapshot/SELF, "COPIED_ENTRY_ONLY")

    def rebind_sources():
        total = 0
        need(read(selected_path) == raw_selection and read(output/"selection.json") == raw_selection,
             "SELECTION_REBOUND")
        for rel, expected in sources.items():
            original, copied = pin(ROOT/rel, 2*MIB), pin(snapshot/rel, 2*MIB)
            need(original["sha256"] == copied["sha256"] == expected
                 and original["bytes"] == copied["bytes"]
                 and runtime.get(original["path"]) == expected, "ORIGINAL_SNAPSHOT_BINDING:"+rel)
            total += original["bytes"]
        need(total <= 2*MIB, "SOURCE_CUSTODY_RESERVE")
        need(pin(configuration_path, MIB) == configuration_pin, "CONFIGURATION_REBOUND")

    rebind_sources()
    need(runtime.get(configuration_pin["path"]) == configuration_pin["sha256"], "SELECTED_CONFIGURATION")
    expected_argv = [sys.executable, "-I", "-S", "-B", "{snapshot}\\"+SELF.replace("/", "\\"),
        "--configuration", str(configuration_path), "--configuration-sha256", configuration_pin["sha256"],
        "--selection", str(selected_path)]
    need(selection["argv"] == expected_argv, "EXACT_SELECTED_ENTRY_ARGV")
    # Canonical imports are an explicit local-harness choice, not hidden fallback.
    sys.path.insert(0, str(ROOT/"software/v5"))
    from aggregate_geometry.layout_owner import LayoutOwner, SOURCE_MODULES
    from aggregate_geometry import snapshot as S
    from aggregate_geometry.prepare_h2 import prepare_h2
    from mixed_claims.packet import Envelope
    from production import producer as P
    need(tuple(MODULES[:-1]) == SOURCE_MODULES, "OWNER_SOURCE_CLOSURE_AGREEMENT")

    def origins():
        for name, rel in relative.items():
            module = sys.modules.get(name)
            need(module is not None and Path(getattr(module, "__file__", "")).resolve() == ROOT/rel,
                 "CANONICAL_SOURCE_ORIGIN:"+name)

    owner, report, error = None, None, None
    try:
        origins()
        profile_pin = configuration["profile_document"]
        need(pin(profile_pin["path"], MIB) == profile_pin
             and runtime.get(profile_pin["path"]) == profile_pin["sha256"], "SELECTED_PROFILE")
        raw_profile = read(profile_pin["path"])
        profile = parse(raw_profile)
        need(P.encoded(profile) == raw_profile, "EXACT_CANONICAL_PROFILE_BYTES")
        owner = LayoutOwner(profile)
        need(owner.profile_id == configuration["profile_id"], "PROFILE_DOMAIN_BINDING")
        envelope = Envelope(**configuration["envelope"])
        references = configuration["reference_inputs"]
        need(len(references["parents"]) == 1, "ONE_H2_PARENT")
        data = []
        for reference in (references["wire"], references["expected"], references["parents"][0]):
            need(pin(reference["path"]) == reference
                 and runtime.get(reference["path"]) == reference["sha256"], "ACTUAL_H2_REFERENCE")
            data.append(read(reference["path"]))
        packet, prepared = prepare_h2(*data, envelope=envelope)
        need(pin(configuration["packet"]["path"]) == configuration["packet"]
             and packet == read(configuration["packet"]["path"])
             and prepared.target_journal.hex() == configuration["target_journal"],
             "DISPATCH_REGENERATED_H2_PACKET_EQUALITY")
        report = owner.snapshot(prepared, configuration=configuration_pin, selection=selection_pin)
        S.result_shape(report, owner.profile_id)
    except BaseException as caught:
        error = type(caught).__name__+": "+str(caught)[:2000]
    finally:
        if owner is not None:
            try:
                owner.close()
            except BaseException as caught:
                error = "CLOSE:"+type(caught).__name__+": "+str(caught)[:2000]
    try:
        rebind_sources(); origins()
        if owner is not None:
            owner._check(owner._pins)
        need(time.process_time()-cpu <= 60 and time.monotonic()-wall <= 170, "ADAPTER_FINAL_TAIL_BOUND")
        output_census = census(output)
    except BaseException as caught:
        error = "FINAL_BINDING:"+type(caught).__name__+": "+str(caught)[:2000]
        output_census = None
    result = {"schema": "DMKN_GEOMETRY17_LAYOUT_ENTRY_RESULT_V1",
        "status": "PASS_ONE_H2_GEOMETRY17_LAYOUT_ONLY" if error is None else "FAIL",
        "configuration": configuration_pin, "selection": selection_pin,
        "layout_result": pin(output/"evidence/RESULT.json") if report is not None else None,
        "owner": owner.report() if owner is not None else None, "error": error,
        "source_count": len(sources), "runtime_pin_count": len(runtime),
        "source_origins": {name: str(ROOT/rel) for name,rel in relative.items()},
        "output_census": output_census, "controller_cpu_seconds": time.process_time()-cpu,
        "wall_seconds": time.monotonic()-wall, "proof_calls": 0, "mathematical_admission": False,
        "authority": "EXECUTION_CAPSULE_ONLY_NOT_CERTIFICATE_OR_PROOF_FUNDING",
        "accounting": "OUTER_JOB_INCLUDES_ENTRY_AND_NATIVE;DO_NOT_ADD_NESTED_NATIVE_CPU;OUTER_WRAPPER_SEPARATE"}
    save(output/"adapter-result.json", result)
    print(encoded(result).decode(), end="", flush=True)
    return 0 if error is None else 1


if __name__ == "__main__":
    raise SystemExit(main())

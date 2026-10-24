"""Pin one reviewed native workflow and successful build; never launch it."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_baseline/"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("workflow-sha256", "report-sha256", "build-number", "build-sha256",
                "build-result-sha256", "build-selection-sha256"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "NATIVE_WORKFLOW_SELECTION_CONTEXT")
    for key, digest in vars(args).items():
        if key == "build_number":
            continue
        need(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest),
             "NATIVE_WORKFLOW_SELECTION_HASH")
    path = ROOT/PREFIX/"native_workflow02.py"
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == args.workflow_sha256,
         "NATIVE_WORKFLOW_SELECTION_REVIEWED_ADAPTER")
    spec = importlib.util.spec_from_file_location("_selected_native_workflow", path)
    H = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = H
    exec(compile(raw, str(path), "exec"), H.__dict__)
    B = H.helper()
    deadline, runtime = time.monotonic()+60, {}

    def check():
        need(time.monotonic() < deadline, "NATIVE_WORKFLOW_SELECTION_DEADLINE")

    def pin(path, expected=None, maximum=128*MIB):
        value = B.pin(B.ordinary(path), check, maximum)["sha256"]
        need(expected is None or value == expected, "NATIVE_WORKFLOW_SELECTION_PIN:"+str(path))
        need(str(path) not in runtime or runtime[str(path)] == value, "NATIVE_WORKFLOW_SELECTION_CONFLICT")
        runtime[str(path)] = value
        return value

    authorized = {"build": args.build_sha256, "result": args.build_result_sha256,
                  "selection": args.build_selection_sha256}
    build_pins, executables = H.inspect_build(B, args.build_number, authorized, check)
    for name, value in build_pins.items():
        pin(Path(name), value["sha256"])
    template = H.LOCAL/"ordinary-preview-public-01.selection.json"
    template_hash = "613e28c8da5fde5d5e570e46d52bfe94cb56b6fa2b0c6037f26592095796c5c7"
    pin(template, template_hash)
    raw = H.read(template)
    need(H.sha(raw) == template_hash, "NATIVE_WORKFLOW_SELECTION_TEMPLATE_CHANGED")
    selected = {name: digest for name, digest in json.loads(raw)["runtime_pins"].items()
                if any(Path(name).is_relative_to(root) for root in (H.PACKAGE, H.PYTHON, H.LEAN))}
    need(len(selected) >= 140, "NATIVE_WORKFLOW_SELECTION_RUNTIME_CENSUS")
    for name, digest in selected.items():
        pin(Path(name), digest)
    # Package/public-use pins already include Lean's native loader dependencies.
    # The successful compiler build also pins the selected compiler toolchain.
    build_selection_path = H.LOCAL/("ordinary-baseline-native-build-"+args.build_number)/"selection.json"
    build_selection_raw = H.read(build_selection_path)
    need(H.sha(build_selection_raw) == args.build_selection_sha256,
         "NATIVE_WORKFLOW_SELECTION_BUILD_SELECTION_CHANGED")
    for name, digest in json.loads(build_selection_raw)["runtime_pins"].items():
        if Path(name).is_relative_to(H.LEAN) or Path(name).is_relative_to(H.PYTHON):
            pin(Path(name), digest)
    expected = {PREFIX+name: digest for name, digest in H.FIXED_SOURCES.items()}
    expected.update({PREFIX+"native_workflow02.py": args.workflow_sha256,
                     PREFIX+"reference_report.py": args.report_sha256})
    sources = {name: pin(ROOT/name, digest, 2*MIB) for name, digest in expected.items()}
    for name in (PREFIX+"select_native_workflow02.py", "tools/Run-V5-Check.py"):
        sources[name] = pin(ROOT/name, maximum=2*MIB)
    pin(ROOT/H.BUILDER, H.BUILDER_SHA, 2*MIB)
    need(len(runtime) <= 256 and len(executables) == 3 and
         str(H.LEAN/"bin/lean.exe") in runtime and str(H.PYTHON/"python.exe") in runtime,
         "NATIVE_WORKFLOW_SELECTION_COMPLETE_BOUNDED_PINS")
    destination = H.LOCAL/(H.NAME+".selection.json")
    B.ordinary(destination, fresh=True); B.ordinary(H.LOCAL/H.NAME, directory=True, fresh=True)
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": H.NAME,
        "sources": sources, "runtime_pins": runtime,
        "argv": [str(H.PYTHON/"python.exe"), "-I", "-S", "-B",
                 "{snapshot}/"+PREFIX+"native_workflow02.py", "--source-root", "{snapshot}",
                 "--output", "{output}/workflow", "--build-number", args.build_number,
                 "--build-sha256", args.build_sha256,
                 "--build-result-sha256", args.build_result_sha256,
                 "--build-selection-sha256", args.build_selection_sha256,
                 "--report-sha256", args.report_sha256],
        "limits": {"wall_seconds": 300, "cpu_seconds": 120, "memory_mib": 1536,
                   "active_processes": 6, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
    need(len(raw) <= MIB, "NATIVE_WORKFLOW_SELECTION_BYTES")
    B.fresh_bytes(destination, raw)
    need(B.pin(destination, check, MIB) == {"bytes": len(raw), "sha256": H.sha(raw)},
         "NATIVE_WORKFLOW_SELECTION_READBACK")
    print(json.dumps({"selection": str(destination), "sha256": H.sha(raw),
                      "runtime_pin_count": len(runtime), "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()

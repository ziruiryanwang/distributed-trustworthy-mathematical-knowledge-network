"""Pin one reviewed retained-snapshot continuation; never launch it."""
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
    # Read the explicitly selected source before loading its argument schema.
    initial = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    initial.add_argument("--continuation-sha256", required=True)
    known, _ = initial.parse_known_args()
    path = ROOT/PREFIX/"reference_continuation.py"
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == known.continuation_sha256,
         "REFERENCE_CONTINUATION_SELECTION_SOURCE")
    spec = importlib.util.spec_from_file_location("_selected_reference_continuation", path)
    C = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = C
    exec(compile(raw, str(path), "exec"), C.__dict__)
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--continuation-sha256", required=True)
    C.add_arguments(parser)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "REFERENCE_CONTINUATION_SELECTION_CONTEXT")
    for key, value in vars(args).items():
        if key.endswith("sha256"):
            need(len(value) == 64 and all(c in "0123456789abcdef" for c in value),
                 "REFERENCE_CONTINUATION_SELECTION_HASH")
    H = C.load_utilities(ROOT/PREFIX)
    B = H.helper()
    deadline, runtime = time.monotonic()+60, {}

    def check():
        need(time.monotonic() < deadline, "REFERENCE_CONTINUATION_SELECTION_DEADLINE")

    def keep(path, expected=None, maximum=512*MIB):
        value = B.pin(B.ordinary(Path(path)), check, maximum)["sha256"]
        need(expected is None or value == expected, "REFERENCE_CONTINUATION_SELECTION_PIN:"+str(path))
        need(str(path) not in runtime or runtime[str(path)] == value,
             "REFERENCE_CONTINUATION_SELECTION_PIN_CONFLICT")
        runtime[str(path)] = value
        return value

    retained = C.inspect_retained(B, H, check)
    matcher, _ = C.inspect_matcher(B, H, args, check)
    for name, pin in (*retained.items(), *matcher.items()):
        keep(Path(name), pin["sha256"])
    # Reuse only the existing package and named runtime attachments. The old
    # matcher/extractors are never invoked by this continuation.
    previous = json.loads(H.read(C.RETAINED/"selection.json"))
    selected = {name: digest for name, digest in previous["runtime_pins"].items()
                if any(Path(name).is_relative_to(root) for root in (H.PACKAGE, H.PYTHON, H.LEAN))}
    need(len(selected) >= 140, "REFERENCE_CONTINUATION_SELECTION_RUNTIME_CENSUS")
    for name, digest in selected.items():
        keep(Path(name), digest)
    expected = {PREFIX+name: digest for name, digest in C.FIXED.items()}
    report_source = B.ordinary(Path(args.report_source))
    need(report_source.parent == ROOT/PREFIX and report_source.suffix == ".py" and
         report_source.name.startswith("reference_report"), "REFERENCE_CONTINUATION_SELECTION_REPORT_SCOPE")
    expected.update({PREFIX+"reference_continuation.py": args.continuation_sha256,
                     report_source.relative_to(ROOT).as_posix(): args.report_sha256})
    sources = {name: keep(ROOT/name, digest, 2*MIB) for name, digest in expected.items()}
    for name in (PREFIX+"select_reference_continuation.py", "tools/Run-V5-Check.py"):
        sources[name] = keep(ROOT/name, maximum=2*MIB)
    keep(ROOT/H.BUILDER, H.BUILDER_SHA, 2*MIB)
    need(len(runtime) <= 256 and str(H.PYTHON/"python.exe") in runtime,
         "REFERENCE_CONTINUATION_SELECTION_PIN_BOUND")
    destination = C.LOCAL/(C.NAME+".selection.json")
    B.ordinary(destination, fresh=True); B.ordinary(C.LOCAL/C.NAME, directory=True, fresh=True)
    argv = [str(H.PYTHON/"python.exe"), "-I", "-S", "-B",
            "{snapshot}/"+PREFIX+"reference_continuation.py", "--source-root", "{snapshot}",
            "--output", "{output}/continuation"]
    for key, value in vars(args).items():
        if key != "continuation_sha256":
            argv.extend(("--"+key.replace("_", "-"), value))
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": C.NAME,
        "sources": sources, "runtime_pins": runtime, "argv": argv,
        "limits": {"wall_seconds": 120, "cpu_seconds": 60, "memory_mib": 1536,
                   "active_processes": 4, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    for name, digest in runtime.items():
        need(B.pin(Path(name), check, 512*MIB)["sha256"] == digest,
             "REFERENCE_CONTINUATION_SELECTION_FINAL_PIN")
    raw = H.encoded(selection)
    need(len(raw) <= MIB, "REFERENCE_CONTINUATION_SELECTION_BYTES")
    B.fresh_bytes(destination, raw)
    need(B.pin(destination, check, MIB) == {"bytes": len(raw), "sha256": H.sha(raw)},
         "REFERENCE_CONTINUATION_SELECTION_READBACK")
    print(json.dumps({"selection": str(destination), "sha256": H.sha(raw),
                      "runtime_pin_count": len(runtime), "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()

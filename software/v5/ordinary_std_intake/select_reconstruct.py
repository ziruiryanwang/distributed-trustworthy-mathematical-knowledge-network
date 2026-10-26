"""Select one exact saved-manifest reconstruction; no product import or launch."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_std_intake/"
PREVIOUS = LOCAL / "binding-saved-writer01.selection.json"
PREVIOUS_SHA = "412dd6bf0220eb98b03e1746295f840a5eda47a0af42b98bf299f5daa8578299"
MANIFEST = LOCAL / "binding-saved-writer01/binding/manifest.json"
MANIFEST_SHA = "1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c"
HELPER = "software/v5/ordinary_binding_reuse/measure_saved_writer.py"
UNUSED_CANDIDATE = ROOT / "experiments/v5-local-checks/multi-source-package01/suite/assembled/package/authoring/py/portable_candidate.py"
PYTHON = Path(r"D:\Python314\python.exe")
MIB = 1024**2
START, CPU_START = time.monotonic(), time.process_time()


def need(ok, code):
    if not ok:
        raise ValueError("STD_RECONSTRUCTION_SELECTION_" + code)


def check():
    need(time.monotonic()-START < 60 and time.process_time()-CPU_START < 30,
         "COOPERATIVE_ALLOWANCE")


def ordinary(path, *, fresh=False, directory=False):
    need(path.is_absolute() and ".." not in path.parts, "ABSOLUTE_PATH")
    for ancestor in (*reversed(path.parents), path):
        try:
            info = ancestor.lstat()
        except FileNotFoundError:
            need(fresh and ancestor == path, "MISSING_PATH")
            return path
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if ancestor != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "ORDINARY_PATH")
    need(not fresh, "OUTPUT_EXISTS")
    return path


def digest(path, maximum=512*MIB):
    check(); ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "FILE_BOUND")
    count, hashed = 0, hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            check(); count += len(block)
            need(count <= size, "FILE_GREW")
            hashed.update(block)
    need(count == ordinary(path).stat().st_size == size, "FILE_CHANGED")
    return hashed.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--reconstructor-sha256", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON and
         Path(__file__).absolute() == ROOT / PREFIX / "select_reconstruct.py", "PROCESS")
    need(re.fullmatch(r"[0-9a-f]{64}", args.reconstructor_sha256) is not None, "ARGUMENTS")
    destination = ordinary(LOCAL / "std-reconstruct01.selection.json", fresh=True)
    ordinary(LOCAL / "std-reconstruct01", directory=True, fresh=True)
    need(digest(PREVIOUS, MIB) == PREVIOUS_SHA, "ADOPTED_PREDECESSOR_SELECTION")
    previous_raw = PREVIOUS.read_bytes()
    need(hashlib.sha256(previous_raw).hexdigest() == PREVIOUS_SHA, "PREDECESSOR_READ")
    previous = json.loads(previous_raw)
    need(previous["schema"] == "DMKN_V5_LOCAL_CHECK_V1" and
         previous["name"] == "binding-saved-writer01" and
         len(previous["runtime_pins"]) == 10, "PREDECESSOR_SCHEMA")
    runtime = dict(previous["runtime_pins"])
    need(runtime.pop(str(UNUSED_CANDIDATE)) ==
         "29ae111a362472b09b2b1ff16b567b352be793d76c2cd1b5421e0aee29219331",
         "ONLY_UNUSED_CANDIDATE_OMITTED")
    need(str(MANIFEST) not in runtime and str(PREVIOUS) not in runtime, "INPUT_OVERLAP")
    runtime[str(MANIFEST)], runtime[str(PREVIOUS)] = MANIFEST_SHA, PREVIOUS_SHA
    need(len(runtime) == 11 and str(PYTHON) in runtime and
         len({name.casefold() for name in runtime}) == 11, "RUNTIME_CENSUS")
    selected = ("tools/Run-V5-Check.py", PREFIX + "reconstruct.py",
                PREFIX + "select_reconstruct.py", PREFIX + "RECONSTRUCT-PLAN.md", HELPER)
    sources = {name: digest(ROOT / name, 2*MIB) for name in selected}
    need(sources[PREFIX + "reconstruct.py"] == args.reconstructor_sha256 and
         all(sources[name] == previous["sources"][name]
             for name in ("tools/Run-V5-Check.py", HELPER)), "REVIEWED_SOURCES")
    for name, expected in runtime.items():
        need(digest(Path(name)) == expected, "RUNTIME_PIN:" + name)
    plan = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": "std-reconstruct01",
        "sources": sources, "runtime_pins": runtime,
        "argv": [str(PYTHON), "-I", "-S", "-B",
                 r"{snapshot}\software\v5\ordinary_std_intake\reconstruct.py",
                 r"{output}\materialized"],
        "limits": {"wall_seconds": 120, "cpu_seconds": 90, "memory_mib": 1792,
                   "active_processes": 1, "stdout_bytes": 262144, "stderr_bytes": 131072}}
    for name, expected in sources.items():
        need(digest(ROOT / name, 2*MIB) == expected, "SOURCE_CHANGED")
    for name, expected in runtime.items():
        need(digest(Path(name)) == expected, "RUNTIME_CHANGED")
    raw = json.dumps(plan, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(raw) <= MIB, "SELECTION_SIZE")
    check()
    with ordinary(destination, fresh=True).open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    need(destination.read_bytes() == raw, "SELECTION_READBACK")
    print(json.dumps({"selection": str(destination),
        "sha256": hashlib.sha256(raw).hexdigest(), "sources": len(sources),
        "runtime_pins": len(runtime), "partial_files": "708; aggregate checked inside operation",
        "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()

"""Select one inert parse-reuse control run; do not import or launch product code."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
PACKAGE = LOCAL / "current-release-build01/distribution/package"
PREFIX = "software/v5/ordinary_parse_reuse/"
PYTHON = Path(r"D:\Python314")
MIB = 1024**2
START, CPU_START = time.monotonic(), time.process_time()
RUNNER_SHA = "44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651"
ADMISSION_SHA = "98c88eb0e7ea5e101f6ccd8e94b56a0cc248167c317a0440ba00dc86f503cd9a"
INTAKE_SHA = "9b243232603206b3a0925f639a0b8b1a6cbf0de8ca093ad4aa3642c595ff1142"
PYTHON_PINS = {
    "python.exe": "03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38",
    "python3.dll": "22c6e46d8bd563cdb072650901461ef68be2ea6cb1e80af859559d9395a27e39",
    "python314.dll": "fde89cdb5c2d08ae65de7ef4abca1876c93ba3796002f5ac0bf7e4d4f5a94da0",
}


def need(ok, code):
    if not ok:
        raise ValueError("PARSE_REUSE_SELECTION_" + code)


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


def relative(value):
    need(type(value) is str and "\\" not in value and ":" not in value and
         not value.startswith("/") and PurePosixPath(value).as_posix() == value and
         all(part not in ("", ".", "..") for part in value.split("/")), "RELATIVE_PATH")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--controls-sha256", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON / "python.exe" and
         Path(__file__).absolute() == ROOT / PREFIX / "select_controls.py", "PROCESS")
    need(re.fullmatch(r"[0-9a-f]{64}", args.controls_sha256) is not None, "REVIEWED_CONTROLS_HASH")
    destination = ordinary(LOCAL / "parse-reuse-controls01.selection.json", fresh=True)
    ordinary(LOCAL / "parse-reuse-controls01", fresh=True, directory=True)
    selected = ("tools/Run-V5-Check.py", PREFIX + "controls.py", PREFIX + "ordinary_admission.py",
                PREFIX + "baseline_intake.py", PREFIX + "CONTRACT.md",
                PREFIX + "TEST-PLAN.md", PREFIX + "select_controls.py")
    sources = {name: digest(ROOT / name, 2*MIB) for name in selected}
    need(sources["tools/Run-V5-Check.py"] == RUNNER_SHA and
         sources[PREFIX + "ordinary_admission.py"] == ADMISSION_SHA and
         sources[PREFIX + "baseline_intake.py"] == INTAKE_SHA and
         sources[PREFIX + "controls.py"] == args.controls_sha256, "REVIEWED_SOURCE_PINS")
    with (ROOT / PREFIX / "controls.py").open("rb") as stream:
        controls_raw = stream.read(2*MIB+1)
    need(hashlib.sha256(controls_raw).hexdigest() == args.controls_sha256, "CONTROLS_CHANGED")
    # Read only literal input maps from the reviewed source. Never import the
    # test module, execute its loader, or invoke a product function here.
    literals = {}
    for node in ast.parse(controls_raw, filename="controls.py").body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ("PINS", "FIXTURES"):
                need(name not in literals, "DUPLICATE_INPUT_LITERAL")
                literals[name] = ast.literal_eval(node.value)
    need(set(literals) == {"PINS", "FIXTURES"} and type(literals["PINS"]) is dict and
         len(literals["PINS"]) == 9 and type(literals["FIXTURES"]) is tuple and
         len(literals["FIXTURES"]) == 3, "EXACT_INPUT_LITERAL_CENSUS")
    runtime = {str(PYTHON / name): expected for name, expected in PYTHON_PINS.items()}

    def add(path, expected):
        need(type(expected) is str and re.fullmatch(r"[0-9a-f]{64}", expected) is not None and
             str(path) not in runtime, "INPUT_PIN_OR_OVERLAP")
        runtime[str(path)] = expected

    for name, expected in literals["PINS"].items():
        add(PACKAGE / relative(name), expected)
    for row in literals["FIXTURES"]:
        need(type(row) is tuple and len(row) == 2, "FIXTURE_ROW")
        add(LOCAL / relative(row[0]), row[1])
    need(len(runtime) == 15 and len({name.casefold() for name in runtime}) == 15,
         "EXACT_RUNTIME_CENSUS")
    for name, expected in runtime.items():
        need(digest(Path(name)) == expected, "RUNTIME_PIN:" + name)
    plan = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": "parse-reuse-controls01",
        "sources": sources, "runtime_pins": runtime,
        "argv": [str(PYTHON / "python.exe"), "-I", "-S", "-B",
                 r"{snapshot}\software\v5\ordinary_parse_reuse\controls.py",
                 "--output", r"{output}\controls"],
        "limits": {"wall_seconds": 60, "cpu_seconds": 45, "memory_mib": 512,
                   "active_processes": 1, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    for name, expected in sources.items():
        need(digest(ROOT / name, 2*MIB) == expected, "SOURCE_CHANGED")
    for name, expected in runtime.items():
        need(digest(Path(name)) == expected, "RUNTIME_CHANGED")
    raw = json.dumps(plan, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
    need(len(raw) <= MIB, "SELECTION_BOUND")
    check()
    with ordinary(destination, fresh=True).open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    need(destination.read_bytes() == raw, "SELECTION_READBACK")
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
        "source_snapshots": len(sources), "runtime_pins": len(runtime), "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()

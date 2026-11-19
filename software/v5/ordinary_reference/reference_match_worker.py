"""Run exactly one selected local correspondence matcher inside the owner's Job.

This is environment setup, not a sandbox or an acceptance authority. The parent
has pinned this worker, the executable, its runtime, and all selected inputs;
it holds the owner lock and checks the actual event and unchanged files afterward.
The outer Job owns the nonrenewing resource allowance and descendant cleanup.
"""
from pathlib import Path
import os
import subprocess
import sys


def need(condition, code):
    if not condition:
        raise ValueError(code)


def absolute(value, *, directory=False):
    path = Path(value)
    need(path.is_absolute() and path == path.resolve(strict=True), "REFERENCE_WORKER_ABSOLUTE_PATH")
    info = path.lstat()
    need(not (getattr(info, "st_file_attributes", 0) & 0x400), "REFERENCE_WORKER_REPARSE_POINT")
    need(path.is_dir() if directory else path.is_file(), "REFERENCE_WORKER_PATH_KIND")
    return path


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv) == 7,
         "REFERENCE_WORKER_INVOCATION")
    matcher = absolute(sys.argv[1])
    lean_bin = absolute(sys.argv[2], directory=True)
    inventory, replay, request = (absolute(value) for value in sys.argv[3:6])
    report = Path(sys.argv[6])
    parent = absolute(str(report.parent), directory=True)
    need(matcher.suffix.lower() == ".exe" and report.is_absolute() and
         report.name == "reference-report.json" and not os.path.lexists(report) and
         report == parent/report.name, "REFERENCE_WORKER_SELECTED_OUTPUT")
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON", "RUST", "CARGO", "RISC0", "NODE"))
           and key.upper() not in ("PATH", "VIRTUAL_ENV")}
    env["PATH"] = str(lean_bin)
    argv = [str(matcher), str(inventory), str(replay), str(request), str(report)]
    need(sum(len(value)+3 for value in argv) <= 30000, "REFERENCE_WORKER_ARGUMENT_BOUND")
    completed = subprocess.run(argv, cwd=parent, env=env, stdin=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
    return completed.returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        sys.stderr.write("REFERENCE_MATCH_WORKER "+str(error)[:1024]+"\n")
        raise SystemExit(1)

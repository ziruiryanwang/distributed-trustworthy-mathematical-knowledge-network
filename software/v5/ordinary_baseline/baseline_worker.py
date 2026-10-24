"""Fixed baseline-export launcher inside the parent's one selected Windows Job.

The parent authenticates installation/profile and approved project selection.
This tiny stdlib-only worker sets the native DLL/search environment and binds
exact request/inventory/program bytes. No new Job, allocation, retry, source
build, owner opening or mathematical acceptance. Direct invocation is no warrant.
"""
from pathlib import Path
import hashlib
import os
import stat
import subprocess
import sys


MIB = 1024**2


def need(condition, code):
    if not condition:
        raise ValueError(code)


def hexid(value):
    need(type(value) is str and len(value) == 64 and
         all(c in "0123456789abcdef" for c in value), "BASELINE_WORKER_HASH")
    return value


def ordinary(path, *, directory=False, fresh=False):
    need(path.is_absolute() and len(str(path)) <= 32768 and len(path.drive) == 2 and
         path.drive[1] == ":" and path != Path(path.anchor) and
         all(part not in (".", "..") for part in path.parts), "BASELINE_WORKER_PATH")
    for ancestor in reversed(path.parents):
        info = ancestor.lstat()
        need(stat.S_ISDIR(info.st_mode) and
             not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT,
             "BASELINE_WORKER_ANCESTRY")
    if fresh:
        need(not os.path.lexists(path), "BASELINE_WORKER_FRESH_OUTPUT")
    else:
        info = path.lstat()
        need(not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT and
             (stat.S_ISDIR(info.st_mode) if directory else
              stat.S_ISREG(info.st_mode) and info.st_nlink == 1), "BASELINE_WORKER_FILE")
    return path


def pin(path, maximum):
    ordinary(path)
    expected_size = path.stat().st_size
    need(0 < expected_size <= maximum, "BASELINE_WORKER_INPUT_SIZE")
    size, digest = 0, hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(min(65536, maximum+1-size)):
            size += len(block)
            need(size <= maximum, "BASELINE_WORKER_INPUT_GREW")
            digest.update(block)
    need(size == expected_size and path.stat().st_size == expected_size,
         "BASELINE_WORKER_INPUT_SIZE_CHANGED")
    return size, digest.hexdigest()


def main(args):
    need(os.name == "nt" and len(args) == 5 and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "BASELINE_WORKER_PROFILE")
    sysroot_raw, size_raw, executable_sha, inventory_sha, request_sha = args
    need(size_raw.isascii() and size_raw.isdigit() and 1 <= len(size_raw) <= 8 and
         not size_raw.startswith("0"), "BASELINE_WORKER_EXECUTABLE_SIZE")
    executable_size = int(size_raw)
    need(0 < executable_size <= 32*MIB, "BASELINE_WORKER_EXECUTABLE_SIZE")
    for value in (executable_sha, inventory_sha, request_sha):
        hexid(value)
    source = ordinary(Path(__file__).absolute())
    executable = ordinary(source.parent.parent/"bin/BaselineExporter.exe")
    sysroot = ordinary(Path(sysroot_raw), directory=True)
    ordinary(sysroot/"bin", directory=True)
    ordinary(sysroot/"lib/lean", directory=True)
    output = ordinary(Path.cwd(), directory=True)
    inventory, request, writer = output/"inventory.json", output/"request.json", output/"writer.json"
    ordinary(writer, fresh=True)
    inputs = {executable: (executable_size, executable_sha),
              inventory: pin(inventory, MIB), request: pin(request, MIB)}
    need(inputs[inventory][1] == inventory_sha and inputs[request][1] == request_sha,
         "BASELINE_WORKER_REQUEST_OR_INVENTORY_PIN")

    def unchanged():
        for path, expected in inputs.items():
            need(pin(path, expected[0]) == expected, "BASELINE_WORKER_INPUT_CHANGED")

    unchanged()
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON", "RUST", "CARGO", "RISC0", "NODE")) and
           key.upper() not in ("PATH", "VIRTUAL_ENV")}
    env["PATH"] = str(sysroot/"bin")
    argv = [str(executable), str(sysroot), str(inventory), str(request), str(writer)]
    need(sum(len(part)+3 for part in argv) <= 30000, "BASELINE_WORKER_ARGV_BOUND")
    # The native descendant inherits the same Job and standard-output handles.
    # No fresh per-phase budget or wrapper-controlled subprocess tree is created.
    code = subprocess.call(argv, cwd=output, env=env, stdin=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)
    unchanged()
    if code == 0:
        pin(writer, 64*MIB)
    return code


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as error:
        sys.stderr.write("BASELINE_WORKER_FAILURE "+str(error)[:2048]+"\n")
        raise SystemExit(1)

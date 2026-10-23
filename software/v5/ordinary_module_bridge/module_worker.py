"""Fixed local module-builder command inside an already selected Windows Job.

The owning controller verifies every source/helper/runtime before launch. This
worker neither opens a catalog nor accepts metadata from a peer. It does not
compile a new executable, resolve dependencies or run Lake.
"""
from pathlib import Path
import os
import subprocess
import sys


def need(condition, code):
    if not condition:
        raise ValueError(code)


def main(args):
    need(len(args) == 8 and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "MODULE_WORKER_PROFILE")
    lean, source, helpers_raw, sysroot, inventory, request, output, report = args
    paths = tuple(map(Path, (lean, source, sysroot, inventory, request, output, report)))
    helpers = tuple(Path(part) for part in helpers_raw.split(os.pathsep))
    need(1 <= len(helpers) <= 8 and len(set(helpers)) == len(helpers) and
         all(p.is_absolute() and ".." not in p.parts for p in (*paths, *helpers)),
         "MODULE_WORKER_PATHS")
    lean, source, sysroot, inventory, request, output, report = paths
    need(lean == sysroot/"bin/lean.exe" and all(p.is_file() for p in
         (lean, source, inventory, request)) and all(p.is_dir() for p in
         (sysroot/"lib/lean", output.parent, report.parent, *helpers)) and
         not os.path.lexists(output) and not os.path.lexists(report),
         "MODULE_WORKER_INPUTS")
    need(sum(len(value)+3 for value in args) <= 30000, "MODULE_WORKER_ARGV_BOUND")
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
    env["LEAN_PATH"] = os.pathsep.join(map(str, (sysroot/"lib/lean", *helpers)))
    env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), str(lean.parent)))
    argv = [str(lean), "-DElab.async=false", "-R", str(source.parent), "--run", str(source),
            "build", str(sysroot), str(inventory), str(request), str(output), str(report)]
    return subprocess.call(argv, cwd=Path.cwd(), env=env, stdin=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

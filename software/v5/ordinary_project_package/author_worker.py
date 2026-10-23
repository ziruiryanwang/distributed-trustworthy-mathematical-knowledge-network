"""One owner-approved Lean compile inside the selected Windows Job.

Extracted from the existing ordinary API producer's author_worker branch. This
is not a hostile-source sandbox, a peer endpoint or mathematical acceptance.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


def need(condition, code):
    if not condition:
        raise ValueError(code)


def author_worker(args):
    need(len(args) == 5 and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "OWNER_AUTHOR_WORKER_PROFILE")
    lean, source, build, helpers_raw, candidate = args
    paths = [Path(lean), Path(source), Path(build), Path(candidate)]
    helpers = [Path(part) for part in helpers_raw.split(os.pathsep)]
    need(all(path.is_absolute() for path in [*paths, *helpers]) and 1 <= len(helpers) <= 8,
         "OWNER_AUTHOR_WORKER_PATHS")
    need(paths[0].is_file() and paths[1].is_file() and paths[2].is_dir() and
         all(path.is_dir() for path in helpers) and not os.path.lexists(paths[3]),
         "OWNER_AUTHOR_WORKER_INPUTS")
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
    env["LEAN_PATH"] = os.pathsep.join(map(str, helpers))
    env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), str(paths[0].parent)))
    argv = [lean, "-DElab.async=false", "-R", str(paths[1].parent),
            "-o", str(paths[2]/"OrdinaryProducer.olean"), source]
    return subprocess.call(argv, cwd=Path.cwd(), env=env, stdin=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)


def project_author_worker(args):
    """Approved prebuilt project support; no Lake, resolution or installation.

    This separate branch preserves the predecessor's default invocation. The
    module root contains only generated source; cwd may serve trusted plugins.
    Project modules are owner-trusted code, not sandboxed or receiver authority.
    """
    need(len(args) == 8 and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "OWNER_PROJECT_WORKER_PROFILE")
    lean, source, build, helpers_raw, candidate, root, cwd, project_raw = args
    lean, source, build, candidate, root, cwd = map(Path, (lean, source, build, candidate, root, cwd))
    helpers = [Path(part) for part in helpers_raw.split(os.pathsep)]
    project = [Path(part) for part in project_raw.split(os.pathsep)]
    need(1 <= len(helpers) <= 8 and 1 <= len(project) <= 16 and
         len(set(project)) == len(project) and
         all(path.is_absolute() and ".." not in path.parts for path in
             (lean, source, build, candidate, root, cwd, *helpers, *project)),
         "OWNER_PROJECT_WORKER_PATHS")
    need(lean.is_file() and source.is_file() and source.is_relative_to(root) and
         source != root and build.is_dir() and root.is_dir() and cwd.is_dir() and
         all(path.is_dir() for path in (*helpers, *project)) and
         not os.path.lexists(candidate), "OWNER_PROJECT_WORKER_INPUTS")
    # Lean's implicit runtime path is appended AFTER LEAN_PATH. Supply it here
    # before project directories to prevent project Init/Lean/Std shadowing.
    runtime = lean.parent.parent/"lib"/"lean"
    need(runtime.is_dir(), "OWNER_PROJECT_WORKER_RUNTIME_LIBRARY")
    need(sum(len(argument)+3 for argument in args) <= 30000,
         "OWNER_PROJECT_WORKER_ARGV_BOUND")
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
    env["LEAN_PATH"] = os.pathsep.join(map(str, (*helpers, runtime, *project)))
    env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), str(lean.parent)))
    argv = [str(lean), "-DElab.async=false", "-R", str(root),
            "-o", str(build/"OrdinaryProducer.olean"), str(source)]
    return subprocess.call(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)


if __name__ == "__main__":
    need(sys.argv[1:2] in (["--author-worker"], ["--project-author-worker"]),
         "OWNER_AUTHOR_WORKER_ENTRY")
    worker = author_worker if sys.argv[1] == "--author-worker" else project_author_worker
    raise SystemExit(worker(sys.argv[2:]))

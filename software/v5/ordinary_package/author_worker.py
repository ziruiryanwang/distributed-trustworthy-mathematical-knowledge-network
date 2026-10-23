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


if __name__ == "__main__":
    need(sys.argv[1:2] == ["--author-worker"], "OWNER_AUTHOR_WORKER_ENTRY")
    raise SystemExit(author_worker(sys.argv[2:]))

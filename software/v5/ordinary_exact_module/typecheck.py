"""One native elaboration under the enclosing selected Job; no main execution."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
BASE = ROOT / "experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package"


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("source", "source-sha256"):
        parser.add_argument("--" + key, required=True)
    args = parser.parse_args()
    source = Path(args.source)
    if not (os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
            sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize and
            source.is_absolute() and source.is_relative_to(ROOT / "experiments/v5-local-checks")):
        raise ValueError("EXACT_MODULE_TYPECHECK_CONTEXT")
    raw = source.read_bytes()
    if hashlib.sha256(raw).hexdigest() != args.source_sha256:
        raise ValueError("EXACT_MODULE_TYPECHECK_PIN")
    env = dict(os.environ)
    for key in list(env):
        if key.upper().startswith("LEAN"):
            del env[key]
    env["LEAN_PATH"] = os.pathsep.join(map(str, (LEAN / "lib/lean", BASE / "authoring/helpers")))
    env["LEAN_SYSROOT"] = str(LEAN)
    code = subprocess.call([str(LEAN / "bin/lean.exe"), str(source)], cwd=ROOT,
                           env=env, stdin=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)
    if source.read_bytes() != raw:
        raise ValueError("EXACT_MODULE_TYPECHECK_CHANGED")
    print(json.dumps({"status": "ELABORATED_NO_MAIN" if code == 0 else "ELABORATION_FAILED",
                      "exit_code": code, "source_sha256": args.source_sha256}), flush=True)
    return code


if __name__ == "__main__":
    raise SystemExit(main())

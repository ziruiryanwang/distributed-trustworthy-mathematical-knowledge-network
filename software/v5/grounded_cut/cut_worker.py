"""Internal fixed-command child. Parent authenticates all support before launch.

No catalog, state promotion, arbitrary command or peer code. This child inherits
the original enclosing Job; direct invocation creates no mathematical authority.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys


def need(ok, code):
    if not ok:
        raise ValueError("GROUNDED_CHILD_" + code)


def bounded(path, maximum=2 * 1024 * 1024):
    size = path.stat().st_size
    need(0 < size <= maximum, "MANIFEST_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    need(len(raw) == size, "MANIFEST_CHANGED")
    return raw


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv) == 8,
         "FIXED_INVOCATION")
    addition, base, python, lean = (Path(value) for value in sys.argv[1:5])
    expected, request, report = sys.argv[5], Path(sys.argv[6]), Path(sys.argv[7])
    for path in (addition, base, python, lean, request, report):
        need(path.is_absolute() and ".." not in path.parts, "ABSOLUTE_PATH")
    need(Path(__file__).resolve() == addition / "cut_worker.py" and
         Path(sys.executable).resolve() == python / "python.exe", "RUNNING_SUPPORT")
    raw = bounded(addition / "CUT-SUPPORT.json")
    need(len(raw) <= 2 * 1024 * 1024 and hashlib.sha256(raw).hexdigest() == expected,
         "SUPPORT_PIN")
    doc = json.loads(raw)
    need(doc["schema"] == "DMKN_GROUNDED_CUT_SUPPORT_V1", "SCHEMA")
    base_raw = bounded(base / "PROFILE.json")
    need(len(base_raw) <= 2 * 1024 * 1024 and
         hashlib.sha256(base_raw).hexdigest() == doc["base_profile_sha256"], "BASE_PIN")
    base_doc = json.loads(base_raw)
    installation_raw = bounded(base / "installation/INSTALLATION.json")
    need(len(installation_raw) <= 2 * 1024 * 1024 and
         hashlib.sha256(installation_raw).hexdigest() == base_doc["installation_manifest_sha256"],
         "INSTALLATION_PIN")
    installation = json.loads(installation_raw)
    # The currently selected ordinary package has one fixed receiver directory.
    need(set(installation["compiled_dirs"]) == {"lean-lib"}, "RECEIVER_LAYOUT")
    need(not os.path.lexists(report) and request.is_file(), "FRESH_REPORT")
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
    env["PATH"] = os.pathsep.join((str(python), str(lean / "bin")))
    env["LEAN_PATH"] = os.pathsep.join(map(str, (
        addition / "lean-lib", base / "authoring/helpers", base / "installation/lean-lib")))
    command = [str(lean / "bin/lean.exe"), "-R", str(addition), "--run",
               str(addition / "GroundedCutDriver.lean"),
               str(base / "installation/foundation/seed.json"),
               str(base / "installation/foundation/inventory.json"), str(request), str(report)]
    return subprocess.call(command, cwd=Path.cwd(), env=env,
                           stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)


if __name__ == "__main__":
    raise SystemExit(main())

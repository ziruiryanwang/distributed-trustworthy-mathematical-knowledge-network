"""One read-only aggregate diagnostic; root owns selection and supervision.

Three fresh Lean processes avoid retaining imported regions between modes. There
is no .olean output, owner open, proof replay, module registration or repair.
The only write is a fresh diagnostic report below the explicitly selected output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "software/v5/ordinary_module_anchor"
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
MODULE = "DMKNBridge_1705759ee440d55396e5bdf0c78e153a64c9275453f61e5ef92f5c908946ef4c"
DIRECTORY = ROOT / ("experiments/v5-local-checks/ordinary-current-relocated-smoke-01/smoke/catalog/"
                    "module-anchors-v1/operations/"
                    "2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/modules")
PARTS = (
    (".olean", 3128, "f45fbd7ba0e5d6f5d0f7d9f247190bb73f13a9cb6314aa99dfa1d07ae830fbc7"),
    (".olean.server", 96, "92ed38256ea9b810d804c4e8feec6d472f23dc67167e4b19f2beeb9a81bef6e9"),
    (".olean.private", 96, "49a8c513f584222cc634eda9aa1c3b1fae8f16b28ee5464de3d42cd1fd394ae7"),
    (".ir.sig", 176, "8b4cb3a33bdcc82c6845a42e83626d8b0d5806202d01ccd8e22f27a5bdca695c"),
    (".ir", 1152, "9f174435bb2bb65c1575996e4f385c79c52ba66a351e0cb77e1c9e9df22b1255"),
)


def selected_parts():
    result = []
    for suffix, size, digest in PARTS:
        path = DIRECTORY / (MODULE + suffix)
        stat = path.lstat()
        if not path.is_file() or path.is_symlink() or stat.st_nlink != 1 or stat.st_size != size:
            raise RuntimeError("selected artifact metadata changed: " + str(path))
        data = path.read_bytes()
        if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
            raise RuntimeError("selected artifact bytes changed: " + str(path))
        result.append({"path": str(path), "path_characters": len(str(path)),
                       "bytes": size, "sha256": digest})
    return result


def run(mode, source, arguments, directory=None):
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and
           key.upper() not in ("PATH", "VIRTUAL_ENV")}
    env["PATH"] = str(LEAN / "bin")
    paths = [str(LEAN / "lib/lean")]
    if directory is not None:
        paths.append(directory)
    env["LEAN_PATH"] = os.pathsep.join(paths)
    command = [str(LEAN / "bin/lean.exe"), "-DElab.async=false", "-R", str(HERE)]
    if arguments is not None:
        command += ["--run", str(source), *arguments]
    else:
        command += [str(source)]
    started = time.monotonic()
    try:
        child = subprocess.run(command, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        report = {"mode": mode, "command": command, "lean_path": env["LEAN_PATH"],
                  "returncode": child.returncode, "wall_seconds": time.monotonic()-started,
                  "stdout": child.stdout.decode("utf-8", errors="replace"),
                  "stderr": child.stderr.decode("utf-8", errors="replace")}
        if arguments is not None and child.returncode == 0:
            report["native"] = json.loads(report["stdout"])
        return report
    except subprocess.TimeoutExpired as error:
        return {"mode": mode, "command": command, "lean_path": env["LEAN_PATH"],
                "timeout": True, "wall_seconds": time.monotonic()-started,
                "stdout": (error.stdout or b"").decode("utf-8", errors="replace"),
                "stderr": (error.stderr or b"").decode("utf-8", errors="replace")}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    if not output.is_absolute() or not output.is_relative_to(ROOT / "experiments/v5-local-checks"):
        raise RuntimeError("fresh canonical local-check output required")
    if output.exists() or output.is_symlink() or not output.parent.is_dir():
        raise RuntimeError("fresh report path with existing parent required")
    report = {"schema": "DMKN_LONG_PATH_PROBE_V1", "parts_before": selected_parts(), "calls": []}
    try:
        for visibility in ("private", "exported"):
            report["calls"].append(run("explicit-extended-" + visibility,
                HERE / "LongPathProbe.lean", [str(LEAN), str(DIRECTORY), MODULE, "extended", visibility]))
        report["calls"].append(run("ordinary-extended",
            HERE / "LongPathConsumer.lean", None, "\\\\?\\" + str(DIRECTORY)))
        report["parts_after"] = selected_parts()
        report["unchanged"] = report["parts_before"] == report["parts_after"]
    finally:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, sort_keys=True, indent=2)
            stream.write("\n")
    print(json.dumps({"report": str(output), "calls": len(report["calls"]),
                      "unchanged": report.get("unchanged", False)}))


if __name__ == "__main__":
    main()

"""Prepare one fresh pure-frontier selection; no test or native launch."""
from pathlib import Path, PurePosixPath
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PACKAGE = LOCAL/"ordinary-query-assembly-01/assembled/package"
PROFILE = "2b8ac8cad152dde90a1b51d19dd1a821305bd7242b601c10eaa7a39f0db572f5"
PREFIX = "software/v5/ordinary_module_anchor/"
NAME = "ordinary-module-anchor-frontier-01"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and len(sys.argv) == 1, "ANCHOR_SELECTION_CONTEXT")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    with builder.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5",
         "ANCHOR_SELECTION_BUILDER_PIN")
    spec = importlib.util.spec_from_file_location("_anchor_selection_builder", builder)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(builder), "exec"), B.__dict__)
    deadline, runtime = time.monotonic()+60, {}
    def check():
        need(time.monotonic() < deadline, "ANCHOR_SELECTION_DEADLINE")
    def pin(path, expected=None):
        value = B.pin(path, check, 128*MIB)
        need(expected is None or value == expected, "ANCHOR_SELECTION_PIN:"+str(path))
        runtime[str(path)] = value["sha256"]
        return value
    def read_doc(path, digest):
        value = pin(path)
        need(value["bytes"] <= 2*MIB and value["sha256"] == digest, "ANCHOR_SELECTION_DOCUMENT")
        with path.open("rb") as stream:
            raw = stream.read(2*MIB+1)
        need(hashlib.sha256(raw).hexdigest() == digest, "ANCHOR_SELECTION_DOCUMENT_CHANGED")
        def unique(items):
            result = {}
            for key, item in items:
                need(key not in result, "ANCHOR_SELECTION_DUPLICATE_KEY")
                result[key] = item
            return result
        return json.loads(raw.decode("utf-8"), object_pairs_hook=unique)
    def parts(name):
        value = PurePosixPath(name)
        need(type(name) is str and value.parts and not value.is_absolute() and
             value.as_posix() == name and "\\" not in name and
             all(p not in (".", "..") and not any(c in ':*?"<>|' for c in p) for p in value.parts),
             "ANCHOR_SELECTION_RELATIVE_PATH")
        return value.parts
    profile = read_doc(PACKAGE/"PROFILE.json", PROFILE)
    for name, expected in profile["files"].items():
        pin(PACKAGE.joinpath(*parts(name)), expected)
    installation = read_doc(PACKAGE/"installation/INSTALLATION.json", profile["installation_manifest_sha256"])
    roots = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    for name, expected in installation["files"].items():
        components = parts(name)
        path = roots[components[0]].joinpath(*components[1:]) if components[0] in roots else PACKAGE/"installation"/name
        pin(path, expected)
    for path in (builder, ROOT/"software/v5/ordinary_module_bridge/closure_controls.py",
            LOCAL/"ordinary-package-lifecycle-continuation-01/contribution/evidence/25ae588e95228a64196a576aa9c9dd78249c23b0c26189c5671a434b93afa1b3.json",
            LOCAL/"ordinary-package-lifecycle-continuation-01/contribution/evidence/c4639e6e5f70e259ea1611adba8e168aa74dbfb91f98e2512cd465f82705e61e.json",
            LOCAL/"ordinary-peer-reciprocal-02/B-contribution/evidence/d52aed3d1d0f94b8ee2236a7ee84435c983c9523dca0f100f4369c183c3d4e51.json"):
        pin(path)
    source_names = ("tools/Run-V5-Check.py", PREFIX+"select_frontier.py",
                    PREFIX+"frontier_controls.py", PREFIX+"module_closure.py")
    sources = {name: B.pin(ROOT/name, check, 2*MIB)["sha256"] for name in source_names}
    destination = LOCAL/(NAME+".selection.json")
    B.ordinary(destination, fresh=True); B.ordinary(LOCAL/NAME, directory=True, fresh=True)
    need(len(runtime) <= 256, "ANCHOR_SELECTION_RUNTIME_COUNT")
    document = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": NAME, "sources": sources,
        "runtime_pins": runtime, "limits": {"wall_seconds": 60, "cpu_seconds": 35,
            "memory_mib": 512, "active_processes": 2, "stdout_bytes": MIB, "stderr_bytes": MIB},
        "argv": [str(PYTHON/"python.exe"), "-I", "-S", "-B", "{snapshot}/"+PREFIX+"frontier_controls.py",
            "--package", str(PACKAGE), "--profile-sha256", PROFILE, "--python-runtime", str(PYTHON),
            "--lean-runtime", str(LEAN), "--output", "{output}",
            "--collector-sha256", sources[PREFIX+"module_closure.py"]]}
    raw = json.dumps(document, sort_keys=True, separators=(",", ":")).encode("ascii")
    B.fresh_bytes(destination, raw)
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()

"""Prepare the fixed five-call module-anchor check; never launch native work."""
from pathlib import Path, PurePosixPath
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PACKAGE = LOCAL/"ordinary-module-anchor-assembly-01/package"
PROFILE = "8404d56996180520c88f98f3fec61100809bde59297b983de686fede8958ac93"
PREFIX = "software/v5/ordinary_module_anchor_package/"
NAME = "ordinary-module-anchor-native-01"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
SAVED = LOCAL/"ordinary-current-relocated-smoke-01/smoke"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and len(sys.argv) == 1,
         "ANCHOR_SELECTION_CONTEXT")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    with builder.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5",
         "ANCHOR_SELECTION_BUILDER_PIN")
    spec = importlib.util.spec_from_file_location("_anchor_native_selection_builder", builder)
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
    for path in (builder, PACKAGE/"ASSEMBLY.json",
            ROOT/"software/v5/ordinary_distribution/relocated_smoke.py",
            LOCAL/"ordinary-current-relocated-smoke-01-payload/installation/INSTALLATION.json",
            SAVED/"IMMUTABLE-FILES.json", SAVED/"catalog/ADOPTION.json",
            SAVED/"fixtures/custody-limits.json", SAVED/"module-contribution/RESULT.json"):
        pin(path)
    source_names = ("tools/Run-V5-Check.py", PREFIX+"select_native.py", PREFIX+"native_check.py",
                    "software/v5/ordinary_distribution/relocated_smoke.py")
    sources = {name: B.pin(ROOT/name, check, 2*MIB)["sha256"] for name in source_names}
    destination = LOCAL/(NAME+".selection.json")
    B.ordinary(destination, fresh=True); B.ordinary(LOCAL/NAME, directory=True, fresh=True)
    need(not (SAVED/"catalog/module-anchors-v1").exists(), "ANCHOR_SELECTION_NO_PRIOR_REGISTRY")
    need(len(runtime) <= 256, "ANCHOR_SELECTION_RUNTIME_COUNT")
    document = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": NAME, "sources": sources,
        "runtime_pins": runtime, "limits": {"wall_seconds": 270, "cpu_seconds": 165,
            "memory_mib": 2048, "active_processes": 8, "stdout_bytes": MIB, "stderr_bytes": MIB},
        "argv": [str(PYTHON/"python.exe"), "-I", "-S", "-B", "{snapshot}/"+PREFIX+"native_check.py",
            "--package", str(PACKAGE), "--profile-sha256", PROFILE,
            "--assembly-sha256", runtime[str(PACKAGE/"ASSEMBLY.json")], "--python-runtime", str(PYTHON),
            "--lean-runtime", str(LEAN), "--output", "{output}/native", "--wall-seconds", "240",
            "--cpu-seconds", "140", "--memory-mib", "1536"]}
    raw = json.dumps(document, sort_keys=True, separators=(",", ":")).encode("ascii")
    B.fresh_bytes(destination, raw)
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()

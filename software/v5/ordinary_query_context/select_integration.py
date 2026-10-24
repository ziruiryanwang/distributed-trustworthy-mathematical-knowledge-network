"""Prepare one saved-input real-owner query selection; never launch it."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_query_context/"
NAME = "ordinary-context-query-integration-01"
HARNESS_SHA = "c51ef8c55d7b95f8170e72127d639fbff579fc85ab3d0053464a6dfa7483dd65"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for field in ("package", "profile-sha256", "assembly-sha256"):
        parser.add_argument("--"+field, required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTEXT_SELECTION_PROCESS")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    with builder.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    builder_sha = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
    need(hashlib.sha256(raw).hexdigest() == builder_sha, "CONTEXT_SELECTION_BUILDER_PIN")
    spec = importlib.util.spec_from_file_location("_context_integration_selection_builder", builder)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(builder), "exec"), B.__dict__)
    deadline, runtime = time.monotonic()+60, {}
    def check():
        need(time.monotonic() < deadline, "CONTEXT_SELECTION_DEADLINE")
    def pin(path, expected=None):
        value = B.pin(path, check, 128*MIB)
        need(expected is None or value == expected, "CONTEXT_SELECTION_PIN:"+str(path))
        runtime[str(path)] = value["sha256"]
        return value
    def document(path, digest):
        value = pin(path)
        need(value["bytes"] <= 2*MIB and value["sha256"] == digest, "CONTEXT_SELECTION_DOCUMENT_PIN")
        with path.open("rb") as stream:
            raw = stream.read(2*MIB+1)
        need(hashlib.sha256(raw).hexdigest() == digest, "CONTEXT_SELECTION_DOCUMENT_CHANGED")
        return json.loads(raw)
    def parts(name):
        path = PurePosixPath(name)
        need(type(name) is str and path.parts and not path.is_absolute() and
             path.as_posix() == name and "\\" not in name and
             all(p not in (".", "..") and not any(c in ':*?"<>|' for c in p) for p in path.parts),
             "CONTEXT_SELECTION_RELATIVE_PATH")
        return path.parts
    package = B.ordinary(args.package, directory=True)
    need(package.is_relative_to(LOCAL), "CONTEXT_SELECTION_LOCAL_PACKAGE")
    for digest in (args.profile_sha256, args.assembly_sha256):
        need(re.fullmatch(r"[0-9a-f]{64}", digest), "CONTEXT_SELECTION_HASH_ARGUMENT")
    harness = ROOT/PREFIX/"integration.py"
    need(pin(harness)["sha256"] == HARNESS_SHA, "CONTEXT_SELECTION_HARNESS_PIN")
    with harness.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == HARNESS_SHA, "CONTEXT_SELECTION_HARNESS_CHANGED")
    spec = importlib.util.spec_from_file_location("_selected_context_integration", harness)
    C = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(harness), "exec"), C.__dict__)
    profile = document(package/"PROFILE.json", args.profile_sha256)
    need(profile["installation_manifest_sha256"] == C.INSTALLATION and
         profile["files"]["query.py"]["sha256"] == C.QUERY_SHA, "CONTEXT_SELECTION_SELECTED_QUERY")
    for name, expected in profile["files"].items():
        pin(package.joinpath(*parts(name)), expected)
    manifest = document(package/"installation/INSTALLATION.json", C.INSTALLATION)
    roots = {"python_runtime": C.PYTHON.parent, "lean_runtime": C.LEAN}
    for name, expected in manifest["files"].items():
        components = parts(name)
        path = roots[components[0]].joinpath(*components[1:]) if components[0] in roots else package/"installation"/name
        pin(path, expected)
    assembly = document(package/"ASSEMBLY.json", args.assembly_sha256)
    need(assembly["profile_sha256"] == args.profile_sha256 and
         assembly["installation_manifest_sha256"] == C.INSTALLATION and
         assembly["implementation_id"] == C.IMPLEMENTATION, "CONTEXT_SELECTION_ASSEMBLY_IDENTITY")
    pin(C.HELPER, C.HELPER_PIN)
    for path, digest in C.PINS.items():
        need(pin(path)["sha256"] == digest, "CONTEXT_SELECTION_PRESERVED_INPUT")
    need(pin(builder)["sha256"] == builder_sha, "CONTEXT_SELECTION_BUILDER_CHANGED")
    names = ["tools/Run-V5-Check.py", PREFIX+"select_integration.py", PREFIX+"integration.py",
             "software/v5/ordinary_distribution/relocated_smoke.py"]
    sources = {name: pin(ROOT/name)["sha256"] for name in names}
    need(sources[PREFIX+"integration.py"] == HARNESS_SHA, "CONTEXT_SELECTION_HARNESS_FINAL_PIN")
    need(len(runtime) <= 256, "CONTEXT_SELECTION_RUNTIME_BOUND")
    destination = LOCAL/(NAME+".selection.json")
    B.ordinary(destination, fresh=True); B.ordinary(LOCAL/NAME, directory=True, fresh=True)
    selection = dict(schema="DMKN_V5_LOCAL_CHECK_V1", name=NAME, sources=sources, runtime_pins=runtime,
        argv=[str(C.PYTHON), "-I", "-S", "-B", "{snapshot}/"+PREFIX+"integration.py",
              "--package", str(package), "--profile-sha256", args.profile_sha256,
              "--assembly-sha256", args.assembly_sha256, "--output", "{output}/integration",
              "--wall-seconds", "90", "--cpu-seconds", "45", "--memory-mib", "512"],
        limits=dict(wall_seconds=120, cpu_seconds=60, memory_mib=768, active_processes=3,
                    stdout_bytes=MIB, stderr_bytes=MIB))
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":")).encode("ascii")
    B.fresh_bytes(destination, raw)
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()

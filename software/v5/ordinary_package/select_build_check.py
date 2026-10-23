"""Root-selected finite package build/lifecycle plans; never launches them.

Validation-only, not shipped in the owner payload. Build uses exact real source
pins because the preserved outer supervisor snapshots v5 sources, not foundation
assets. Lifecycle copies only manifest-selected package payload into a fresh
location without _build or source dependencies, then selects one boundary check.
No state copy, old proof replay, automatic retry, native work or network access.
"""
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
PREFIX = "software/v5/ordinary_package/"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"


def need(condition, code):
    if not condition:
        raise ValueError(code)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def fresh(path, value):
    raw = json.dumps(value, ensure_ascii=True, sort_keys=True,
                     allow_nan=False, separators=(",", ":")).encode("ascii")
    with path.open("xb") as stream:
        stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "lifecycle"))
    parser.add_argument("--name", required=True)
    parser.add_argument("--package")
    parser.add_argument("--profile-sha256")
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode, "CANONICAL_PACKAGE_SELECTION")
    need(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", args.name) is not None,
         "PACKAGE_SELECTION_NAME")
    selection = LOCAL/(args.name+".selection.json")
    need(not selection.exists() and not (LOCAL/args.name).exists(), "FRESH_PACKAGE_SELECTION")
    spec = importlib.util.spec_from_file_location("_selected_ordinary_builder", ROOT/PREFIX/"build.py")
    B = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = B
    spec.loader.exec_module(B)  # only constants/function definitions, not build().
    deadline = time.monotonic()+90
    def check():
        need(time.monotonic() < deadline, "PACKAGE_SELECTION_DEADLINE")
    runtime = {}
    for logical, (size, expected) in B.RUNTIME_PINS.items():
        category, relative = logical.split("/", 1)
        path = {"python_runtime": PYTHON, "lean_runtime": LEAN}[category]/relative
        need(B.pin(path, check) == {"bytes": size, "sha256": expected}, "PACKAGE_RUNTIME_SELECTION")
        runtime[str(path)] = expected
    sources = {"tools/Run-V5-Check.py", PREFIX+"select_build_check.py", PREFIX+"build.py"}
    if args.mode == "build":
        need(args.package is None and args.profile_sha256 is None, "PACKAGE_BUILD_ARGUMENTS")
        for path in B.source_paths(ROOT):
            relative = path.relative_to(ROOT).as_posix()
            expected = B.pin(path, check, 2*1024**2)["sha256"]
            runtime[str(path)] = expected
            if relative.startswith("software/v5/"):
                sources.add(relative)
        argv = [str(PYTHON/"python.exe"), "-I", "-S", "-B",
            r"{snapshot}\software\v5\ordinary_package\build.py",
            "--source-root", str(ROOT), "--python-runtime", str(PYTHON),
            "--lean-runtime", str(LEAN), "--output", r"{output}\package",
            "--wall-seconds", "360", "--cpu-seconds", "260", "--memory-mib", "2048"]
        limits = dict(cpu_seconds=300, wall_seconds=420, memory_mib=2304, active_processes=6,
                      stdout_bytes=1048576, stderr_bytes=1048576)
    else:
        need(args.package is not None and args.profile_sha256 is not None, "PACKAGE_LIFECYCLE_ARGUMENTS")
        source = B.ordinary(Path(args.package), directory=True)
        need(source.is_relative_to(LOCAL) and re.fullmatch(r"[0-9a-f]{64}", args.profile_sha256),
             "SELECTED_LOCAL_PACKAGE")
        def descriptor(path, expected):
            selected = B.pin(path, check, 2*1024**2)
            need(selected["sha256"] == expected, "PACKAGE_DESCRIPTOR_PIN")
            with path.open("rb") as stream:
                raw = stream.read(2*1024**2+1)
            need(len(raw) == selected["bytes"] and hashlib.sha256(raw).hexdigest() == expected,
                 "PACKAGE_DESCRIPTOR_READ_CHANGED")
            def pairs(items):
                result = {}
                for key, value in items:
                    need(key not in result, "PACKAGE_DESCRIPTOR_DUPLICATE")
                    result[key] = value
                return result
            return json.loads(raw, object_pairs_hook=pairs), selected
        profile_path = source/"PROFILE.json"
        profile, profile_pin = descriptor(profile_path, args.profile_sha256)
        need(type(profile) is dict and set(profile) == {"schema", "installation_manifest_sha256",
             "helper_paths", "author_worker", "files"} and
             profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
             profile["helper_paths"] == ["authoring/helpers"] and
             profile["author_worker"] == "author_worker.py", "PACKAGE_PROFILE_FIELDS")
        required = set(B.ENTRY_POINTS) | {"authoring/py/"+name for name in B.AUTHORING_PY} | {
            "support/"+name for name in B.SUPPORT_PY}
        native_required = {"authoring/helpers/"+name+".olean" for name in B.AUTHORING_MODULES}
        native_allowed = {"authoring/helpers/"+name+suffix
                          for name in B.AUTHORING_MODULES for suffix in B.COMPANIONS}
        need(type(profile["files"]) is dict and
             required | native_required <= set(profile["files"]) <= required | native_allowed,
             "PACKAGE_PROFILE_EXACT_PAYLOAD")
        manifest_path = source/"installation/INSTALLATION.json"
        manifest, manifest_pin = descriptor(manifest_path, profile["installation_manifest_sha256"])
        installed = {"py/"+name for name in B.CORE_PY} | {
            "supervisor/"+name for name in B.SUPERVISOR} | {
            "foundation/seed.json", "foundation/inventory.json"} | {
            "lean-src/"+name+".lean" for name in B.RECEIVER_MODULES} | {
            "lean-lib/"+name+".olean" for name in B.RECEIVER_MODULES}
        need(type(manifest) is dict and set(manifest) == {"schema", "implementation", "roles",
             "compiled_dirs", "support_groups", "files"} and
             manifest["schema"] == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1" and
             type(manifest.get("files")) is dict and
             set(manifest["files"]) == installed | set(B.RUNTIME_PINS), "PACKAGE_INSTALLATION_EXACT_PAYLOAD")
        payload = dict(profile["files"])
        payload["PROFILE.json"] = profile_pin
        payload["installation/INSTALLATION.json"] = manifest_pin
        for logical, pin in manifest["files"].items():
            if not logical.startswith(("python_runtime/", "lean_runtime/")):
                payload["installation/"+logical] = pin
        need(all(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
                 type(pin["bytes"]) is int and 0 < pin["bytes"] <= 128*1024**2 and
                 type(pin["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"])
                 for pin in payload.values()), "PACKAGE_PAYLOAD_PIN_FIELDS")
        need(1 <= len(payload) <= 220 and sum(pin["bytes"] for pin in payload.values()) <= 256*1024**2,
             "PACKAGE_PAYLOAD_BOUND")
        target = B.ordinary(LOCAL/(args.name+"-payload"), directory=True, fresh=True)
        target.mkdir()
        for logical, pin in sorted(payload.items()):
            relative = PurePosixPath(logical)
            need(not relative.is_absolute() and relative.as_posix() == logical and
                 all(part not in (".", "..") and not any(c in part for c in "\\:")
                     for part in relative.parts), "PACKAGE_PAYLOAD_RELATIVE")
            original, copied = source.joinpath(*relative.parts), target.joinpath(*relative.parts)
            need(B.pin(original, check, 128*1024**2) == pin, "PACKAGE_PAYLOAD_SOURCE_PIN")
            copied.parent.mkdir(parents=True, exist_ok=True)
            B.ordinary(copied.parent, directory=True)
            copied_bytes = 0
            with original.open("rb") as incoming, copied.open("xb") as outgoing:
                while block := incoming.read(1024**2):
                    check(); copied_bytes += len(block)
                    need(copied_bytes <= pin["bytes"], "PACKAGE_PAYLOAD_SOURCE_GREW")
                    outgoing.write(block)
            need(B.pin(copied, check, 128*1024**2) == pin, "PACKAGE_PAYLOAD_COPY_PIN")
            runtime[str(copied)] = pin["sha256"]
        fresh(LOCAL/(args.name+".payload.json"), {"source": str(source), "target": str(target),
              "files": payload, "claim": "EXACT_RUNTIME_PAYLOAD_COPY_NO_OWNER_STATE_NO_BUILD_TREE"})
        sources.add(PREFIX+"lifecycle_check.py")
        argv = [str(PYTHON/"python.exe"), "-I", "-S", "-B",
            r"{snapshot}\software\v5\ordinary_package\lifecycle_check.py",
            "--package", str(target), "--profile-sha256", args.profile_sha256,
            "--python-runtime", str(PYTHON), "--lean-runtime", str(LEAN), "--output", "{output}"]
        limits = dict(cpu_seconds=180, wall_seconds=240, memory_mib=2048, active_processes=8,
                      stdout_bytes=1048576, stderr_bytes=1048576)
    need(len(runtime) <= 256, "PACKAGE_RUNTIME_PIN_COUNT")
    plan = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": args.name,
        "sources": {name: digest(ROOT/name) for name in sorted(sources)},
        "runtime_pins": runtime, "argv": argv, "limits": limits}
    check()
    pin = fresh(selection, plan)
    print(json.dumps({"selection": str(selection), "sha256": pin,
                      "sources": len(sources), "runtime_pins": len(runtime), "runtime": "NOT_STARTED"}))


if __name__ == "__main__":
    main()

"""Copy only reviewed runtime payloads and select one fresh public smoke.

File-only validation preparation; no owner, compiler, extractor or network call.
No installation state, build intermediates or old mathematical results are copied.
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
LOCAL = ROOT / "experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_distribution/"
BASE = "software/v5/ordinary_package/build.py"
BASE_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
MAP_SHA = "b021ae3225fe85a874cea82266c0c380d08fc755fee4fc282872f0f506f298bf"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "SMOKE_SELECTION_DUPLICATE_KEY")
        result[key] = value
    return result


def relative(name):
    need(type(name) is str, "SMOKE_SELECTION_RELATIVE_TYPE")
    path = PurePosixPath(name)
    need(path.parts and path.as_posix() == name and not path.is_absolute() and
         all(part not in (".", "..") and not part.endswith((".", " ")) and
             not os.path.isreserved(part) and not any(ord(c) < 32 or c in ':*?"<>|\\'
                                                    for c in part) for part in path.parts),
         "SMOKE_SELECTION_RELATIVE_PATH")
    return path.parts


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("name", "package", "profile-sha256", "smoke-sha256"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "CANONICAL_ISOLATED_SMOKE_SELECTION")
    need(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", args.name) is not None and
         all(re.fullmatch(r"[0-9a-f]{64}", pin) is not None for pin in
             (args.profile_sha256, args.smoke_sha256)), "SMOKE_SELECTION_ARGUMENTS")
    deadline = time.monotonic() + 90

    def check():
        need(time.monotonic() < deadline, "SMOKE_SELECTION_DEADLINE")

    raw = (ROOT / BASE).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == BASE_SHA, "SMOKE_SELECTION_BASE_PIN")
    spec = importlib.util.spec_from_file_location("_smoke_selection_helpers", ROOT / BASE)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(ROOT / BASE), "exec"), B.__dict__)
    source = B.ordinary(args.package, directory=True)
    need(source.is_relative_to(LOCAL), "SMOKE_SELECTION_LOCAL_PACKAGE")
    target = B.ordinary(LOCAL / (args.name + "-payload"), directory=True, fresh=True)
    selection = B.ordinary(LOCAL / (args.name + ".selection.json"), fresh=True)
    receipt = B.ordinary(LOCAL / (args.name + ".payload.json"), fresh=True)
    B.ordinary(LOCAL / args.name, directory=True, fresh=True)
    runtime = {}

    def document(path, expected):
        pin = B.pin(path, check, 2*MIB)
        need(pin["sha256"] == expected, "SMOKE_SELECTION_DESCRIPTOR_PIN")
        raw = path.read_bytes()
        need(pin == {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()},
             "SMOKE_SELECTION_DESCRIPTOR_CHANGED")
        return json.loads(raw, object_pairs_hook=unique), pin

    mapping, _ = document(ROOT / PREFIX / "source-map.json", MAP_SHA)
    profile, profile_pin = document(source / "PROFILE.json", args.profile_sha256)
    need(set(profile) == {"schema", "installation_manifest_sha256", "helper_paths",
                         "author_worker", "files"} and
         profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
         profile["helper_paths"] == ["authoring/helpers"] and
         profile["author_worker"] == "author_worker.py", "SMOKE_SELECTION_PROFILE_FIELDS")
    manifest, manifest_pin = document(source / "installation/INSTALLATION.json",
                                      profile["installation_manifest_sha256"])
    need(manifest["schema"] == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1",
         "SMOKE_SELECTION_MANIFEST_SCHEMA")
    payload = dict(profile["files"])
    roots = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    for logical, pin in manifest["files"].items():
        parts = relative(logical)
        if parts[0] in roots:
            path = roots[parts[0]].joinpath(*parts[1:])
            need(B.pin(path, check) == pin, "SMOKE_SELECTION_RUNTIME_PIN")
            runtime[str(path)] = pin["sha256"]
        else:
            payload["installation/" + logical] = pin
    payload["installation/INSTALLATION.json"] = manifest_pin
    expected = set(mapping["copies"]) | {"installation/INSTALLATION.json", mapping["extractor_output"]}
    expected.update("installation/lean-lib/" + row["module"] + ".olean"
                    for row in mapping["lanes"]["receiver"])
    expected.update("authoring/helpers/" + row["module"] + suffix
                    for row in mapping["lanes"]["authoring"] for suffix in mapping["authoring_suffixes"])
    need(len(profile["files"]) == 98 and set(payload) == expected and len(payload) == 126,
         "SMOKE_SELECTION_CURRENT_PAYLOAD_CENSUS")
    payload["PROFILE.json"] = profile_pin
    need(sum(pin["bytes"] for pin in payload.values()) <= 768*MIB, "SMOKE_SELECTION_PAYLOAD_BOUND")
    for logical, pin in mapping["native_runtime_pins"].items():
        parts = relative(logical)
        path = roots[parts[0]].joinpath(*parts[1:])
        need(B.pin(path, check) == pin, "SMOKE_SELECTION_NAMED_TOOLCHAIN_PIN")
        runtime[str(path)] = pin["sha256"]
    # Bind the specifically selected installed module parts as well. Remaining
    # runtime dependencies retain the stated full-distribution premise.
    for suffix in B.COMPANIONS:
        path = LEAN / ("lib/lean/Std/Data/Internal/List/Defs" + suffix)
        runtime[str(path)] = B.pin(path, check, 128*MIB)["sha256"]
    target.mkdir()
    for logical, pin in sorted(payload.items()):
        parts = relative(logical)
        original, copied = source.joinpath(*parts), target.joinpath(*parts)
        need(B.pin(original, check, 128*MIB) == pin, "SMOKE_SELECTION_PAYLOAD_SOURCE")
        copied.parent.mkdir(parents=True, exist_ok=True)
        B.ordinary(copied.parent, directory=True)
        B.ordinary(copied, fresh=True)
        observed = 0
        with original.open("rb") as incoming, copied.open("xb") as outgoing:
            while block := incoming.read(MIB):
                check()
                observed += len(block)
                need(observed <= pin["bytes"], "SMOKE_SELECTION_PAYLOAD_GREW")
                outgoing.write(block)
        need(observed == pin["bytes"] and B.pin(copied, check, 128*MIB) == pin and
             B.pin(original, check, 128*MIB) == pin,
             "SMOKE_SELECTION_PAYLOAD_COPY")
        runtime[str(copied)] = pin["sha256"]
    need({p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file()} == set(payload),
         "SMOKE_SELECTION_EXACT_RELOCATION")
    B.save_json(receipt, {"schema": "DMKN_ORDINARY_RELOCATED_PAYLOAD_V1", "source": str(source),
        "target": str(target), "files": payload,
        "claim": "RUNTIME_PAYLOAD_ONLY_NO_BUILD_TREE_NO_OWNER_STATE"})
    runtime[str(receipt)] = B.pin(receipt, check, 2*MIB)["sha256"]
    names = ("tools/Run-V5-Check.py", PREFIX + "select_relocated_smoke.py", PREFIX + "relocated_smoke.py")
    sources = {name: B.pin(ROOT / name, check, 2*MIB)["sha256"] for name in names}
    need(sources[PREFIX + "relocated_smoke.py"] == args.smoke_sha256 and len(runtime) <= 256,
         "SMOKE_SELECTION_FINAL_BINDING")
    plan = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": args.name,
        "sources": sources, "runtime_pins": runtime,
        "argv": [str(PYTHON / "python.exe"), "-I", "-S", "-B",
            r"{snapshot}\software\v5\ordinary_distribution\relocated_smoke.py",
            "--package", str(target), "--profile-sha256", args.profile_sha256,
            "--python-runtime", str(PYTHON), "--lean-runtime", str(LEAN),
            "--output", r"{output}\smoke", "--wall-seconds", "360",
            "--cpu-seconds", "240", "--memory-mib", "1536"],
        "limits": {"wall_seconds": 420, "cpu_seconds": 300, "memory_mib": 2048,
                   "active_processes": 8, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    check()
    B.save_json(selection, plan)
    print(json.dumps({"selection": str(selection), "sha256": B.pin(selection, check, MIB)["sha256"],
        "relocated_package": str(target), "runtime_pins": len(runtime), "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()

"""Select one pure project-grammar or public project-return check; never run it."""
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
PREFIX = "software/v5/ordinary_project_return/"
BRIDGE = "software/v5/ordinary_module_bridge/"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
MIB = 1024**2


def need(condition, code):
    if not condition:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", required=True, choices=("controls", "native"))
    parser.add_argument("--name", required=True)
    parser.add_argument("--package")
    parser.add_argument("--profile-sha256")
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "MODULE_PUBLIC_SELECTION_CONTEXT")
    need(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", args.name) is not None,
         "MODULE_PUBLIC_SELECTION_NAME")
    need(args.package is not None and args.profile_sha256 is not None and
         re.fullmatch(r"[0-9a-f]{64}", args.profile_sha256) is not None,
         "MODULE_PUBLIC_SELECTION_PACKAGE_ARGS")
    destination = LOCAL/(args.name+".selection.json")
    need(not destination.exists() and not (LOCAL/args.name).exists(), "MODULE_PUBLIC_SELECTION_FRESH")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    with builder.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5",
         "MODULE_PUBLIC_SELECTION_BUILDER_PIN")
    spec = importlib.util.spec_from_file_location("_module_selected_builder", builder)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(builder), "exec"), B.__dict__)
    deadline = time.monotonic()+60
    def check():
        need(time.monotonic() < deadline, "MODULE_PUBLIC_SELECTION_DEADLINE")
    runtime = {}
    def pin(path, expected=None, maximum=128*MIB):
        actual = B.pin(path, check, maximum)
        need(expected is None or actual == expected, "MODULE_PUBLIC_SELECTION_INPUT_PIN")
        runtime[str(path)] = actual["sha256"]
        return actual
    def document(path, digest):
        actual = pin(path, maximum=2*MIB)
        need(actual["sha256"] == digest, "MODULE_PUBLIC_SELECTION_DOCUMENT_PIN")
        with path.open("rb") as stream:
            raw = stream.read(2*MIB+1)
        need(actual == {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()},
             "MODULE_PUBLIC_SELECTION_DOCUMENT_CHANGED")
        def pairs(items):
            result = {}
            for key, value in items:
                need(key not in result, "MODULE_PUBLIC_SELECTION_DUPLICATE_KEY")
                result[key] = value
            return result
        return json.loads(raw, object_pairs_hook=pairs)
    def relative(name):
        path = PurePosixPath(name)
        need(type(name) is str and path.parts and not path.is_absolute() and path.as_posix() == name and
             "\\" not in name and all(p not in (".", "..") and not any(c in ':*?"<>|' for c in p)
                                      for p in path.parts), "MODULE_PUBLIC_SELECTION_RELATIVE")
        return path.parts
    selected = {"tools/Run-V5-Check.py", PREFIX+"select_checks.py"}
    package = B.ordinary(args.package, directory=True)
    need(package.is_relative_to(LOCAL), "MODULE_PUBLIC_SELECTION_LOCAL_PACKAGE")
    profile = document(package/"PROFILE.json", args.profile_sha256)
    for name, expected in profile["files"].items():
        pin(package.joinpath(*relative(name)), expected)
    installation = document(package/"installation/INSTALLATION.json", profile["installation_manifest_sha256"])
    roots = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    for name, expected in installation["files"].items():
        parts = relative(name)
        path = roots[parts[0]].joinpath(*parts[1:]) if parts[0] in roots else package/"installation"/name
        pin(path, expected)
    runner = PREFIX+("project_controls.py" if args.kind == "controls" else "public_native_check.py")
    selected.add(runner)
    argv = [str(PYTHON/"python.exe"), "-I", "-S", "-B", "{snapshot}/"+runner,
            "--package", str(package), "--profile-sha256", args.profile_sha256, "--output", "{output}"]
    if args.kind == "controls":
        argv += ["--python-runtime", str(PYTHON), "--lean-runtime", str(LEAN)]
        limits = dict(wall_seconds=60, cpu_seconds=35, memory_mib=512, active_processes=2,
                      stdout_bytes=MIB, stderr_bytes=MIB)
    else:
        utility = BRIDGE+"native_check03.py"
        selected.add(utility)
        utility_pin = B.pin(ROOT/utility, check, 2*MIB)
        need(utility_pin["sha256"] == "20f6c613eb8fdd051b1f7df923e528e2c01874eb2e2c6277e3aca73d8475ccfd",
             "MODULE_PUBLIC_SELECTION_UTILITY_PIN")
        argv += ["--utility", "{snapshot}/"+utility, "--utility-sha256", utility_pin["sha256"]]
        old = LOCAL/"ordinary-peer-reciprocal-02"
        for name in ("RECIPROCAL-RESULT.json", "B-custody-limits.json", "B-catalog/ADOPTION.json",
                     "B-contribution/ADMISSION.json", "B-contribution/RESULT.json"):
            pin(old/name, maximum=2*MIB)
        for operation in ("55cbddc0310a3d93ae4e2c555baa83e0ada1536b0290bf24f95b33d02f448bfe",
                "99303d20602ddd2932ed1fa693f5f29cf3ad91f4698f171e6192cec4d66241bb",
                "f156ac506d2a64dc89c344ead48a3f970834f1602d957a11b2de982a072693f2",
                "87e6a8c39afbadc98e8cab5ef2dc305e27ff265107fe4d2471a6c97fbd538494"):
            pin(old/"B-catalog/operations"/operation/"chunk.olean", maximum=32*MIB)
        exported = LOCAL/"ordinary-module-public-native-01/export"
        manifest = document(exported/"MODULE.json",
            "d447b491cb4166035063377e36757c1f14b1340fe6dcec423a60a3b18b6735e8")
        need(pin(exported/"native-report.json", maximum=2*MIB)["sha256"] ==
             "035de7d52abe5a71ba41b7a48ba0b1382f0e9037dae50cdb7cb4ba26bb968b48",
             "RETURN_SELECTION_NATIVE_REPORT_PIN")
        module_name = "DMKNBridge_450bf7c15f3af7aa703934147ce9cd2fa1fbb5a50ec2dca7f7e41bbf1714f458"
        need(manifest["module_name"] == module_name, "RETURN_SELECTION_MODULE_NAME")
        for suffix in (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig"):
            pin(exported/"modules"/(module_name+suffix),
                manifest["artifact_parts"][module_name+suffix], maximum=32*MIB)
        limits = dict(wall_seconds=180, cpu_seconds=110, memory_mib=2048, active_processes=8,
                      stdout_bytes=MIB, stderr_bytes=MIB)
    sources = {name: B.pin(ROOT/name, check, 2*MIB)["sha256"] for name in sorted(selected)}
    need(len(runtime) <= 256, "MODULE_PUBLIC_SELECTION_PIN_COUNT")
    plan = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": args.name, "sources": sources,
            "runtime_pins": runtime, "argv": argv, "limits": limits}
    raw = json.dumps(plan, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":")).encode("ascii")
    B.fresh_bytes(destination, raw)
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}))


if __name__ == "__main__":
    main()

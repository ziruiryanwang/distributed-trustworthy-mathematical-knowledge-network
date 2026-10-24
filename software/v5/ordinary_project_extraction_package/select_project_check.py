"""Select the three-call approved-project boundary check; never launch it.

Run only after independent review of the actual package/assembly and harness.
The explicit three hashes bind that review; this selector grants no authority
from a package success flag and does not open an owner or copy its state.
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
PACKAGE = LOCAL/"ordinary-project-extraction-build-01/integration/package"
SAVED = LOCAL/"ordinary-current-relocated-smoke-01/smoke"
PREFIX = "software/v5/ordinary_project_extraction_package/"
NAME = "ordinary-project-extraction-public-01"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
HELPER_SHA = "aaba6e2e30906414f539842fd7678aaaf3ab7f9c077b30c6f115db7407584831"
MODULE_SHA = "4e3abb741add01af00a4300542420ae6c67e313be3567f299d7186cc8fdde3d5"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("profile-sha256", "assembly-sha256", "check-sha256"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "PROJECT_SELECTION_CONTEXT")
    for digest in vars(args).values():
        need(re.fullmatch(r"[0-9a-f]{64}", digest), "PROJECT_SELECTION_HASH")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    with builder.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5",
         "PROJECT_SELECTION_BUILDER_PIN")
    spec = importlib.util.spec_from_file_location("_project_selection_builder", builder)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(builder), "exec"), B.__dict__)
    deadline, runtime = time.monotonic()+60, {}
    def check():
        need(time.monotonic() < deadline, "PROJECT_SELECTION_DEADLINE")
    def pin(path, expected=None):
        value = B.pin(path, check, 128*MIB)
        need(expected is None or value == expected, "PROJECT_SELECTION_PIN:"+str(path))
        runtime[str(path)] = value["sha256"]
        return value
    def document(path, digest):
        value = pin(path)
        need(value["bytes"] <= 2*MIB and value["sha256"] == digest, "PROJECT_SELECTION_DOCUMENT")
        with path.open("rb") as stream:
            raw = stream.read(2*MIB+1)
        need(hashlib.sha256(raw).hexdigest() == digest, "PROJECT_SELECTION_DOCUMENT_CHANGED")
        def unique(items):
            result = {}
            for key, item in items:
                need(key not in result, "PROJECT_SELECTION_DUPLICATE_KEY")
                result[key] = item
            return result
        return json.loads(raw.decode("utf-8"), object_pairs_hook=unique)
    def parts(name):
        value = PurePosixPath(name)
        need(type(name) is str and value.parts and not value.is_absolute() and
             value.as_posix() == name and "\\" not in name and
             all(part not in (".", "..") and not any(c in ':*?"<>|' for c in part)
                 for part in value.parts), "PROJECT_SELECTION_RELATIVE_PATH")
        return value.parts
    profile = document(PACKAGE/"PROFILE.json", args.profile_sha256)
    need(profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
         profile["installation_manifest_sha256"] == INSTALLATION, "PROJECT_SELECTION_PROFILE")
    for name, expected in profile["files"].items():
        pin(PACKAGE.joinpath(*parts(name)), expected)
    installation = document(PACKAGE/"installation/INSTALLATION.json", INSTALLATION)
    roots = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    for name, expected in installation["files"].items():
        components = parts(name)
        path = (roots[components[0]].joinpath(*components[1:]) if components[0] in roots
                else PACKAGE/"installation"/name)
        pin(path, expected)
    receipt = document(PACKAGE/"ASSEMBLY.json", args.assembly_sha256)
    need(receipt["status"] == "ASSEMBLED_NOT_ADOPTED" and
         receipt["profile_sha256"] == args.profile_sha256 and
         receipt["installation_manifest_sha256"] == INSTALLATION and
         receipt["files_excluding_profile"] == 134 and receipt["added"] == [] and
         set(receipt["changed"]) == {"owner.py", "authoring/py/library_extraction.py",
                                    "authoring/bin/MissingImportExporter.exe"},
         "PROJECT_SELECTION_REVIEWED_ASSEMBLY")
    module = document(SAVED/"export/MODULE.json", MODULE_SHA)
    for name, expected in module["artifact_parts"].items():
        need(len(parts(name)) == 1, "PROJECT_SELECTION_MODULE_BASENAME")
        pin(SAVED/"export/modules"/name, expected)
    for path in (builder, SAVED/"IMMUTABLE-FILES.json", SAVED/"catalog/ADOPTION.json",
                 SAVED/"fixtures/custody-limits.json", SAVED/"init/stdout.txt"):
        pin(path)
    helper = ROOT/"software/v5/ordinary_distribution/relocated_smoke.py"
    need(pin(helper)["sha256"] == HELPER_SHA, "PROJECT_SELECTION_REVIEWED_HELPER")
    names = ("tools/Run-V5-Check.py", PREFIX+"select_project_check.py",
             PREFIX+"project_check.py", "software/v5/ordinary_distribution/relocated_smoke.py")
    sources = {name: B.pin(ROOT/name, check, 2*MIB)["sha256"] for name in names}
    need(sources[PREFIX+"project_check.py"] == args.check_sha256 and len(runtime) <= 256,
         "PROJECT_SELECTION_REVIEWED_CHECK")
    destination = LOCAL/(NAME+".selection.json")
    B.ordinary(destination, fresh=True); B.ordinary(LOCAL/NAME, directory=True, fresh=True)
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": NAME,
        "sources": sources, "runtime_pins": runtime,
        "argv": [str(PYTHON/"python.exe"), "-I", "-S", "-B",
            "{snapshot}/"+PREFIX+"project_check.py", "--package", str(PACKAGE),
            "--profile-sha256", args.profile_sha256, "--assembly-sha256", args.assembly_sha256,
            "--output", "{output}/project", "--wall-seconds", "180",
            "--cpu-seconds", "100", "--memory-mib", "1536"],
        "limits": {"wall_seconds": 210, "cpu_seconds": 120, "memory_mib": 2048,
            "active_processes": 8, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":")).encode("ascii")
    B.fresh_bytes(destination, raw)
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()

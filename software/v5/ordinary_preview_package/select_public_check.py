"""Select two actual packaged preview HTTP calls; never launch them.

Run only after independent review of the exact assembly and public harness.
Pins only immutable package/runtime/preview/support sources. No owner, index,
database, native compiler, listening socket or child process is opened here.
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
PACKAGE = LOCAL/"ordinary-preview-assembly-01/package"
PREFIX = "software/v5/ordinary_preview_package/"
NAME = "ordinary-preview-public-01"
FIXTURE = LOCAL/("ordinary-project-extraction-public-01/project/completion/previews/"
    "d0c7be50520d2b91b72e43308b8f1ec75022b32c37fe9561381f4aef879fff1a.json")
FIXTURE_PIN = {"bytes": 1351,
    "sha256": "362292c8237bd4cf0f9127ed5575723f188b51efa7ab0a784ac0bf1c1489193c"}
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
HELPER_SHA = "aaba6e2e30906414f539842fd7678aaaf3ab7f9c077b30c6f115db7407584831"
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
         "PREVIEW_PUBLIC_SELECTION_CONTEXT")
    for digest in vars(args).values():
        need(re.fullmatch(r"[0-9a-f]{64}", digest), "PREVIEW_PUBLIC_SELECTION_HASH")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    with builder.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5",
         "PREVIEW_PUBLIC_SELECTION_BUILDER_PIN")
    spec = importlib.util.spec_from_file_location("_preview_public_selection_builder", builder)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(builder), "exec"), B.__dict__)
    deadline, runtime = time.monotonic()+60, {}

    def check():
        need(time.monotonic() < deadline, "PREVIEW_PUBLIC_SELECTION_DEADLINE")

    def pin(path, expected=None):
        value = B.pin(path, check, 128*MIB)
        need(expected is None or value == expected, "PREVIEW_PUBLIC_SELECTION_PIN:"+str(path))
        runtime[str(path)] = value["sha256"]
        return value

    def document(path, digest):
        selected = pin(path)
        need(selected["bytes"] <= 2*MIB and selected["sha256"] == digest,
             "PREVIEW_PUBLIC_SELECTION_DOCUMENT")
        with path.open("rb") as stream:
            data = stream.read(2*MIB+1)
        need(hashlib.sha256(data).hexdigest() == digest, "PREVIEW_PUBLIC_SELECTION_DOCUMENT_CHANGED")
        def pairs(items):
            result = {}
            for key, value in items:
                need(key not in result, "PREVIEW_PUBLIC_SELECTION_DUPLICATE_KEY")
                result[key] = value
            return result
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs)

    def parts(name):
        need(type(name) is str, "PREVIEW_PUBLIC_SELECTION_PATH_TYPE")
        path = PurePosixPath(name)
        need(path.parts and not path.is_absolute() and path.as_posix() == name and "\\" not in name
             and all(part not in (".", "..") and not part.endswith((".", " ")) and
                 not os.path.isreserved(part) and not any(ord(c) < 32 or c in ':*?"<>|' for c in part)
                 for part in path.parts), "PREVIEW_PUBLIC_SELECTION_RELATIVE_PATH")
        return path.parts

    profile = document(PACKAGE/"PROFILE.json", args.profile_sha256)
    need(profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
         profile["installation_manifest_sha256"] == INSTALLATION, "PREVIEW_PUBLIC_SELECTION_PROFILE")
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
         set(receipt["changed"]) == {"peer.py", "peer_api.py"} and
         receipt["changed_or_added"] == {name: profile["files"][name] for name in ("peer.py", "peer_api.py")},
         "PREVIEW_PUBLIC_SELECTION_REVIEWED_ASSEMBLY")
    pin(FIXTURE, FIXTURE_PIN)
    helper = ROOT/"software/v5/ordinary_distribution/relocated_smoke.py"
    need(pin(helper)["sha256"] == HELPER_SHA, "PREVIEW_PUBLIC_SELECTION_HELPER_PIN")
    pin(builder)
    names = ("tools/Run-V5-Check.py", PREFIX+"select_public_check.py", PREFIX+"public_check.py",
             "software/v5/ordinary_distribution/relocated_smoke.py")
    sources = {name: B.pin(ROOT/name, check, 2*MIB)["sha256"] for name in names}
    need(sources[PREFIX+"public_check.py"] == args.check_sha256 and len(runtime) <= 256,
         "PREVIEW_PUBLIC_SELECTION_REVIEWED_HARNESS")
    destination = LOCAL/(NAME+".selection.json")
    B.ordinary(destination, fresh=True); B.ordinary(LOCAL/NAME, directory=True, fresh=True)
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": NAME,
        "sources": sources, "runtime_pins": runtime,
        "argv": [str(PYTHON/"python.exe"), "-I", "-S", "-B", "{snapshot}/"+PREFIX+"public_check.py",
            "--package", str(PACKAGE), "--profile-sha256", args.profile_sha256,
            "--assembly-sha256", args.assembly_sha256, "--output", "{output}/public",
            "--wall-seconds", "75", "--cpu-seconds", "32", "--memory-mib", "512"],
        "limits": {"wall_seconds": 90, "cpu_seconds": 40, "memory_mib": 768,
            "active_processes": 4, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":")).encode("ascii")
    B.fresh_bytes(destination, raw)
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()

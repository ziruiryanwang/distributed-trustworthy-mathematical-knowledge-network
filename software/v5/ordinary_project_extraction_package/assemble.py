"""Compile only the changed extractor; assemble exactly three replacement payloads.

Run only under the selected existing Run-V5-Check enclosing Job. This adapter
adds no supervisor, owner/catalog operation, retry, helper rebuild or acceptance.
The Job owns inclusive CPU/memory/process accounting and all descendants.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_project_extraction_package/"
NATIVE = "software/v5/ordinary_project_extraction/MissingImportExporter.lean"
CONTROLLER = "software/v5/ordinary_project_extraction/library_extraction.py"
OWNER = PREFIX+"owner.py"
BASE = LOCAL/"ordinary-module-anchor-assembly-04/package"
BASE_PROFILE = "b0802fbe33b08bbf57e8050a18e96c2b1d277a75ba53192e51b487d34a3682a9"
BASE_RECEIPT = "ca433382b93bdd30d73555925f2c7f1b9397b2be04d9d4fae55e0dc205080de9"
BASE_OWNER = "a17f7905f479929bf55f3ddbe8f857de9d48e528a132e4c27f2a000d1adb028d"
OLD_HELPER = "software/v5/ordinary_module_anchor_package/assemble.py"
OLD_HELPER_SHA = "1c426a2ce3484448effe5dee559d52cf0c43650fcfd2f50946aba97e05c6481d"
BUILDER = "software/v5/ordinary_package/build.py"
BUILDER_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
BUILD_BASE = LOCAL/"ordinary-current-source-build-01/distribution/_build"
SHARED = BUILD_BASE/"extractor-objects"
SHARED_MANIFEST = BUILD_BASE/"EXTRACTOR-OUTPUTS.json"
SHARED_MANIFEST_SHA = "f55d4c5b56fc299564b76d68c66d63d3090f439b44479b597b016113c4b53768"
RUNTIME_TEMPLATE = LOCAL/"ordinary-current-source-build-01.selection.json"
RUNTIME_TEMPLATE_SHA = "97a4c0d19aea620d067f9cf2a227706fd460654bf06b978cc201a2b7b2e8790b"
SHARED_MODULES = ("OriginalExpr", "OriginalDecl", "CheckedExtension",
                  "BootstrapSupport", "OrdinaryExport")
RUNTIMES = {"python_runtime": Path(r"D:\Python314"),
            "lean_runtime": ROOT/"software/runtime/lean-4.34.0-windows"}
NAME = "ordinary-project-extraction-build-01"
OUTPUT = LOCAL/NAME/"integration"
MIB = 1024**2
SOURCE_FILES = (PREFIX+"assemble.py", PREFIX+"select_build.py", OWNER,
                CONTROLLER, NATIVE, OLD_HELPER, BUILDER)
CHANGED = ("authoring/bin/MissingImportExporter.exe",
           "authoring/py/library_extraction.py", "owner.py")


def need(ok, code):
    if not ok:
        raise ValueError(code)


def helpers():
    path = ROOT/OLD_HELPER
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == OLD_HELPER_SHA, "PROJECT_BUILD_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_project_assembly_helper", path)
    S = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec"), S.__dict__)
    B = S.bootstrap(ROOT/BUILDER, "_project_assembly_builder", BUILDER_SHA)
    return S, B


def inspect_inputs(S, B, check, deadline):
    """Read-only selected package/support loading; never construct an owner."""
    owner = S.bootstrap(BASE/"owner.py", "_project_assembly_base_owner", BASE_OWNER)
    loader = owner.bootstrap(BASE, BASE_PROFILE, check)
    loaded = loader.load(BASE, BASE_PROFILE, RUNTIMES, deadline, check_parent=check)
    old = loaded.descriptor
    installed_raw = loader.bounded(BASE/"installation/INSTALLATION.json", 2*MIB)
    installed = loader.owner_json(installed_raw)
    selected = {name: (BASE/name, pin) for name, pin in old["files"].items()}
    for name, pin in installed["files"].items():
        loader.relative(name)
        if name.split("/", 1)[0] not in RUNTIMES:
            selected["installation/"+name] = (BASE/"installation"/name, pin)
    selected["installation/INSTALLATION.json"] = (BASE/"installation/INSTALLATION.json",
        {"bytes": len(installed_raw), "sha256": old["installation_manifest_sha256"]})
    need(len(selected) == 134 and len(old["files"]) == 106 and
         len({name.casefold() for name in selected}) == 134, "PROJECT_BUILD_BASE_CENSUS")
    pins = {}

    def keep(path, expected=None, maximum=128*MIB):
        actual = B.pin(path, check, maximum)
        need(expected is None or actual == expected, "PROJECT_BUILD_INPUT_PIN:"+str(path))
        need(path not in pins or pins[path] == actual, "PROJECT_BUILD_INPUT_CONFLICT")
        pins[path] = actual
        return actual

    for name, (path, expected) in selected.items():
        loader.relative(name); keep(path, expected)
    for path, digest in ((BASE/"PROFILE.json", BASE_PROFILE),
                         (BASE/"ASSEMBLY.json", BASE_RECEIPT),
                         (SHARED_MANIFEST, SHARED_MANIFEST_SHA),
                         (RUNTIME_TEMPLATE, RUNTIME_TEMPLATE_SHA)):
        need(keep(path, maximum=2*MIB)["sha256"] == digest, "PROJECT_BUILD_MANIFEST_PIN")
    manifest = json.loads(loader.bounded(SHARED_MANIFEST, 2*MIB))
    shared = {}
    for name in SHARED_MODULES:
        for suffix in (".olean", ".o"):
            key = name+suffix
            shared[key] = keep(SHARED/key, manifest[key])
    # Reuse only the named toolchain pins from the saved successful build.
    # They are not a complete authentication of transitive runtime libraries.
    template = json.loads(loader.bounded(RUNTIME_TEMPLATE, 2*MIB))
    runtime = {}
    for name, digest in template["runtime_pins"].items():
        path = Path(name)
        if any(path.is_relative_to(root) for root in RUNTIMES.values()):
            actual = keep(path, maximum=512*MIB)
            need(actual["sha256"] == digest, "PROJECT_BUILD_TOOLCHAIN_PIN")
            runtime[path] = actual
    required = {RUNTIMES["python_runtime"]/"python.exe",
                *(RUNTIMES["lean_runtime"]/"bin"/name for name in
                  ("lean.exe", "leanc.exe", "clang.exe", "ld.lld.exe"))}
    need(required <= set(runtime) and len(runtime) == 23, "PROJECT_BUILD_TOOLCHAIN_CENSUS")
    sources = {name: keep(ROOT/name, maximum=2*MIB) for name in SOURCE_FILES}
    need(len(pins) < 256, "PROJECT_BUILD_INPUT_COUNT")
    return loaded, selected, pins, shared, sources


def assemble(args):
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PROJECT_BUILD_CONTEXT")
    need(Path(sys.executable).resolve() == RUNTIMES["python_runtime"]/"python.exe",
         "PROJECT_BUILD_PYTHON")
    started, cpu = time.monotonic(), time.process_time()
    deadline = started+160

    def check():
        need(time.monotonic() < deadline and time.process_time()-cpu < 120,
             "PROJECT_BUILD_ALLOWANCE")

    S, B = helpers()
    output = B.ordinary(args.output, directory=True, fresh=True)
    source_root = B.ordinary(args.source_root, directory=True)
    need(output == OUTPUT, "PROJECT_BUILD_SELECTED_OUTPUT")
    for path in (BASE, SHARED, source_root, *RUNTIMES.values()):
        need(not output.is_relative_to(path) and not path.is_relative_to(output),
             "PROJECT_BUILD_OUTPUT_OVERLAP")
    loaded, predecessor, input_pins, shared, sources = inspect_inputs(S, B, check, deadline)
    for name, expected in sources.items():
        need(B.pin(source_root/name, check, 2*MIB) == expected, "PROJECT_BUILD_SNAPSHOT_PIN")
    need(B.pin(Path(__file__).resolve(), check, 2*MIB) == sources[PREFIX+"assemble.py"],
         "PROJECT_BUILD_RUNNING_SOURCE")
    output.mkdir()
    work, package = output/"_build", output/"package"
    work.mkdir(); package.mkdir()
    stage_source, shared_copy, objects = work/"source", work/"shared", work/"objects"
    for path in (stage_source, shared_copy, objects):
        path.mkdir()
    completed, phase = [], "STAGING"

    def copy_exact(source, target, expected):
        check()
        target.parent.mkdir(parents=True, exist_ok=True)
        B.ordinary(target.parent, directory=True); B.ordinary(source)
        B.ordinary(target, fresh=True)
        digest, size = hashlib.sha256(), 0
        with source.open("rb") as inp, target.open("xb") as out:
            while block := inp.read(MIB):
                check(); size += len(block)
                need(size <= expected["bytes"], "PROJECT_BUILD_SOURCE_GREW")
                digest.update(block); out.write(block)
            out.flush(); os.fsync(out.fileno())
        need({"bytes": size, "sha256": digest.hexdigest()} == expected and
             B.pin(target, check, 128*MIB) == expected, "PROJECT_BUILD_COPY_PIN")

    try:
        for name, expected in shared.items():
            copy_exact(SHARED/name, shared_copy/name, expected)
        native_source = stage_source/"MissingImportExporter.lean"
        copy_exact(source_root/NATIVE, native_source, sources[NATIVE])
        B.save_json(work/"INPUTS.json", {"files": {str(p): v for p, v in input_pins.items()},
            "shared_manifest_sha256": SHARED_MANIFEST_SHA,
            "runtime_scope": "EXPLICIT_NAMED_PINS_NOT_HERMETIC_TOOLCHAIN"})
        runtime = RUNTIMES["lean_runtime"]
        env = {key: value for key, value in os.environ.items()
               if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
        env["PATH"] = str(runtime/"bin")
        env["LEAN_PATH"] = str(shared_copy)

        def run(label, argv):
            check()
            before = time.monotonic()
            # Inherit the enclosing Job. Timeout is an additional fixed-deadline
            # guard, not a replacement supervisor or a fresh allowance.
            result = subprocess.run(argv, cwd=work, env=env, stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW, timeout=max(0.001, deadline-before))
            row = {"phase": label, "exit_code": result.returncode,
                   "wall_seconds": time.monotonic()-before}
            completed.append(row)
            print(json.dumps(row, sort_keys=True), flush=True)
            need(result.returncode == 0, "PROJECT_BUILD_COMMAND_FAILED:"+label)
            check()

        phase = "COMPILE_CHANGED_NATIVE"
        run("native-codegen", [str(runtime/"bin/lean.exe"), "-R", str(stage_source),
            "-o", str(objects/"MissingImportExporter.olean"),
            "-c", str(objects/"MissingImportExporter.c"), str(native_source)])
        run("native-object", [str(runtime/"bin/leanc.exe"), "-c", "-O0",
            str(objects/"MissingImportExporter.c"), "-o", str(objects/"MissingImportExporter.o")])
        run("native-link", [str(runtime/"bin/leanc.exe"), "-leanshared",
            *(str(shared_copy/(name+".o")) for name in SHARED_MODULES),
            str(objects/"MissingImportExporter.o"), "-o", str(objects/"MissingImportExporter.exe")])
        native_outputs = {"MissingImportExporter"+suffix:
            B.pin(objects/("MissingImportExporter"+suffix), check, 32*MIB)
            for suffix in (".olean", ".c", ".o", ".exe")}
        need({p.name for p in objects.iterdir()} == set(native_outputs), "PROJECT_BUILD_OUTPUT_CENSUS")
        B.save_json(work/"NATIVE-OUTPUTS.json", native_outputs)
        selected = dict(predecessor)
        replacements = {"owner.py": (source_root/OWNER, sources[OWNER]),
            "authoring/py/library_extraction.py": (source_root/CONTROLLER, sources[CONTROLLER]),
            "authoring/bin/MissingImportExporter.exe":
                (objects/"MissingImportExporter.exe", native_outputs["MissingImportExporter.exe"])}
        selected.update(replacements)
        changed = sorted(name for name in selected if selected[name][1] != predecessor[name][1])
        unchanged = sorted(set(selected)-set(changed))
        need(changed == list(CHANGED) and len(unchanged) == 131 and len(selected) == 134,
             "PROJECT_BUILD_EXACT_THREE_DELTA")
        need(sum(pin["bytes"] for _, pin in selected.values()) <= 768*MIB, "PROJECT_BUILD_PACKAGE_BYTES")
        phase = "ASSEMBLING"
        for name, (path, expected) in sorted(selected.items()):
            copy_exact(path, package/name, expected)
        phase = "FINAL_INPUT_REHASH"
        for path, expected in input_pins.items():
            need(B.pin(path, check, 512*MIB) == expected, "PROJECT_BUILD_FINAL_INPUT")
        for name, expected in sources.items():
            need(B.pin(source_root/name, check, 2*MIB) == expected, "PROJECT_BUILD_FINAL_SNAPSHOT")
        for name, expected in shared.items():
            need(B.pin(shared_copy/name, check, 128*MIB) == expected, "PROJECT_BUILD_FINAL_SHARED")
        need(B.pin(native_source, check, 2*MIB) == sources[NATIVE], "PROJECT_BUILD_FINAL_NATIVE_SOURCE")
        for name, expected in native_outputs.items():
            need(B.pin(objects/name, check, 32*MIB) == expected, "PROJECT_BUILD_FINAL_NATIVE_OUTPUT")
        for name, (path, expected) in selected.items():
            need(B.pin(path, check, 128*MIB) == expected and
                 B.pin(package/name, check, 128*MIB) == expected, "PROJECT_BUILD_FINAL_PAYLOAD")
        descriptor = dict(loaded.descriptor, files=dict(loaded.descriptor["files"],
            **{name: pin for name, (_, pin) in replacements.items()}))
        profile_raw = loaded.A.E.canonical_json(descriptor)
        need(len(profile_raw) <= 2*MIB, "PROJECT_BUILD_PROFILE_BYTES")
        receipt = {"status": "ASSEMBLED_NOT_ADOPTED", "base_profile_sha256": BASE_PROFILE,
            "base_assembly_sha256": BASE_RECEIPT,
            "profile_sha256": hashlib.sha256(profile_raw).hexdigest(),
            "installation_manifest_sha256": descriptor["installation_manifest_sha256"],
            "implementation_id": loaded.installation.implementation_id,
            "files_excluding_profile": 134, "added": [], "changed": changed, "unchanged": unchanged,
            "changed_or_added": {name: pin for name, (_, pin) in replacements.items()},
            "assembler": sources[PREFIX+"assemble.py"],
            "native_compilation": {"source": sources[NATIVE],
                "shared_manifest_sha256": SHARED_MANIFEST_SHA,
                "shared_modules": list(SHARED_MODULES), "outputs": native_outputs,
                "completed_commands": len(completed), "accounting": "ENCLOSING_JOB_RESULT"},
            "wall_seconds_before_commit": time.monotonic()-started,
            "controller_cpu_seconds_before_commit": time.process_time()-cpu,
            "claim": "ONE_CHANGED_NATIVE_BUILD_THREE_PAYLOAD_ASSEMBLY_NOT_MATHEMATICAL_ACCEPTANCE"}
        B.save_json(package/"ASSEMBLY.json", receipt)
        B.fresh_bytes(package/".PROFILE.pending", profile_raw)
        check(); B.ordinary(package/"PROFILE.json", fresh=True)
        (package/".PROFILE.pending").rename(package/"PROFILE.json")
        return receipt
    except BaseException as error:
        try:
            B.save_json(work/"BUILD-FAILURE.json", {"phase": phase,
                "error_type": type(error).__name__, "error": str(error)[:2000],
                "completed_commands": completed, "wall_seconds": time.monotonic()-started,
                "controller_cpu_seconds": time.process_time()-cpu,
                "inclusive_cpu_accounting": "ENCLOSING_JOB_RESULT",
                "retention": "PARTIAL_FILES_PRESERVED_NO_RETRY"})
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output", required=True)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True, allow_nan=False), flush=True)

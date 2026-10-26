"""File-only integration of the exact reviewed eight-module receiver build.

Execution requires a separate root selection after focused controls are adopted.
No Lean, owner database, migration, native acceptance or authoring rebuild occurs.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE_ROOT = Path(__file__).resolve().parents[3]
LOCAL = ROOT / "experiments/v5-local-checks"
BASE = LOCAL / "intake-progress-package01/distribution/package"
BASE_RECEIPT = BASE.parent / "ASSEMBLY.json"
RECEIPT_SHA = "d3aec3e91b9b4b82bbc1a0aed8300530fb0c4870ec090c670f8a58f4a1749a8a"
PROFILE_SHA = "b850b12a96667b9a31984fe86fc0330517db9b5172bd6e63982782c10ee3ae47"
INSTALLATION_SHA = "a7403d6b798a654f7e5c76a863304bf415ad6016c6634a35513e73657ab0f9eb"
OLD_IMPLEMENTATION = "89450cdf07416e0c07cb3ef51ae3f4e1c0393c12376207582b1f03bbb5a6de60"
NATIVE = LOCAL / "kernel-admission-build01/native"
BUILD_SHA = "275764e8b0da12ffb2254d0c257452e5ea2082082072de9e965618723866ded9"
HELPER = "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
INSTALLER = "software/v5/ordinary_lean/ordinary_installation.py"
INSTALLER_SHA = "637142362b667e639d5895300dae9d9d575323ea30687dda1dafeebc00812467"
CORE = ("ordinary_evidence", "ordinary_semantics", "portable_evidence",
        "local_catalog", "portable_catalog", "ordinary_admission")
CHANGED_SOURCES = {"CheckedExtension", "LocalSnapshot", "OrdinaryWorkflowWorker"}
RECOMPILED = CHANGED_SOURCES | {"OrdinaryExport", "BasisSnapshot"}
REUSED = {"OriginalExpr", "OriginalDecl", "BootstrapSupport"}
MODULES = RECOMPILED | REUSED
DOCUMENTS = {"BOUNDED-TRANSPORT.md", "CONTACTS.md", "EXECUTION-TRUST.md", "LAUNCHER.md",
             "PRODUCER.md", "README.md", "RECEIVE-POLICY.md", "SPARSE-SEARCH.md"}
MIB = 1024**2


def load(name, path):
    if name in sys.modules:
        raise ValueError("KERNEL_ASSEMBLY_MODULE_ALREADY_LOADED:" + name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def main():
    start, cpu = time.monotonic(), time.process_time()
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if not (os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
            sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize and
            Path(sys.executable).resolve() == Path(r"D:\Python314\python.exe")):
        raise ValueError("KERNEL_ASSEMBLY_ISOLATED_CANONICAL_PROCESS")
    helper_path = SOURCE_ROOT / HELPER
    if hashlib.sha256(helper_path.read_bytes()).hexdigest() != HELPER_SHA:
        raise ValueError("KERNEL_ASSEMBLY_FILE_HELPER_PIN")
    H = load("_kernel_assembly_files", helper_path)

    def check():
        H.need(time.monotonic() - start < 90 and time.process_time() - cpu < 45,
               "KERNEL_ASSEMBLY_ORIGINAL_ALLOWANCE")

    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    H.need(output == LOCAL / "kernel-admission-package01/distribution" and
           SOURCE_ROOT == output.parent / "sources", "OWNER_SNAPSHOT_OUTPUT_SCOPE")
    selected = {}

    def remember(path, expected=None, maximum=128*MIB):
        actual = H.pin(path, check, maximum)
        H.need(expected is None or actual == expected or
               isinstance(expected, str) and actual["sha256"] == expected, "INPUT_PIN")
        key = str(path)
        H.need(key not in selected or selected[key] == actual, "INPUT_OVERLAP")
        selected[key] = actual
        return actual

    def document(path, digest):
        value, pin = H.read_json(path, digest, check)
        remember(path, pin)
        return value, pin

    receipt, _ = document(BASE_RECEIPT, RECEIPT_SHA)
    profile, profile_pin = document(BASE / "PROFILE.json", PROFILE_SHA)
    manifest, manifest_pin = document(BASE / "installation/INSTALLATION.json", INSTALLATION_SHA)
    runtimes = {"python_runtime": Path(r"D:\Python314"),
                "lean_runtime": ROOT / "software/runtime/lean-4.34.0-windows"}
    projected = dict(profile["files"])
    for name, pin in manifest["files"].items():
        if name.split("/", 1)[0] not in runtimes:
            H.need("installation/" + name not in projected, "BASE_PATH_OVERLAP")
            projected["installation/" + name] = pin
    projected.update({"PROFILE.json": profile_pin, "installation/INSTALLATION.json": manifest_pin})
    baseline = dict(receipt["files"])
    H.need(len(projected) == 146 and len(baseline) == 154 and len(profile["files"]) == 117 and
           set(baseline) - set(projected) == DOCUMENTS and
           all(baseline.get(name) == pin for name, pin in projected.items()) and
           profile["installation_manifest_sha256"] == INSTALLATION_SHA and
           receipt["status"] == "ASSEMBLED_NOT_ADOPTED" and
           receipt["package"] == str(BASE) and receipt["implementation_id"] == OLD_IMPLEMENTATION,
           "EXACT_CURRENT_BASE")
    H.census(BASE, baseline, check)
    for name, pin in baseline.items():
        H.relative(name); H.pin_shape(pin); remember(BASE / name, pin)
    for name, pin in manifest["files"].items():
        first, rest = name.split("/", 1)
        if first in runtimes:
            remember(runtimes[first] / H.relative(rest), pin)
    build, _ = document(NATIVE / "BUILD.json", BUILD_SHA)
    H.need(build["status"] == "COMPILED_NOT_TESTED_OR_ADOPTED" and
           build["base_profile_sha256"] == PROFILE_SHA and
           build["base_installation_sha256"] == INSTALLATION_SHA and
           set(build["modules"]) == MODULES and
           set(build["compiled_files"]) == {name + ".olean" for name in MODULES}, "ACTUAL_BUILD_BINDING")
    H.census(NATIVE / "lean-src", {name + ".lean" for name in MODULES}, check)
    H.census(NATIVE / "lean-lib", {name + ".olean" for name in MODULES}, check)
    replacements = {}
    for module in sorted(MODULES):
        row = build["modules"][module]
        H.need(row["object"] == build["compiled_files"][module + ".olean"] and
               row["object_origin"] == ("reused_exact" if module in REUSED else "compiled"),
               "MODULE_OBJECT_BINDING")
        for kind, suffix, field, changed in (("src", ".lean", "source", CHANGED_SOURCES),
                                            ("lib", ".olean", "object", RECOMPILED)):
            name = "lean-" + kind + "/" + module + suffix
            path = NATIVE / name
            remember(path, row[field])
            if module in changed:
                replacements[name] = (path, row[field])
            else:
                H.need(row[field] == manifest["files"][name], "UNCHANGED_MODULE_PIN")
    remember(helper_path, HELPER_SHA)
    remember(Path(__file__).resolve())
    installer_path = SOURCE_ROOT / INSTALLER
    remember(installer_path, INSTALLER_SHA)
    # These six current installation files include the selected parse-reuse core.
    # Preload in dependency order so the older assembler cannot choose historical
    # siblings from its own source directory. Importing definitions opens no DB.
    H.need(all(name not in sys.modules for name in CORE), "CORE_MODULE_COLLISION")
    for name in CORE:
        path = BASE / "installation/py" / (name + ".py")
        remember(path, manifest["files"]["py/" + name + ".py"])
        load(name, path)
    installer = load("_kernel_existing_installer", installer_path)
    for name in CORE:
        H.need(Path(sys.modules[name].__file__).resolve() == BASE / "installation/py" / (name + ".py"),
               "CURRENT_CORE_ORIGIN")
    A, E, S, P = installer.A, installer.E, installer.S, installer.P
    H.need(A is sys.modules["ordinary_admission"] and E is A.E and S is A.S and
           P is A.P and installer.C is A.C and A.PE is sys.modules["portable_evidence"],
           "CURRENT_CORE_MODULE_BINDING")
    H.need(S.implementation_id(E.canonical_json(manifest["implementation"])) == OLD_IMPLEMENTATION and
           all(manifest["implementation"][field] == A.support_digest(field, manifest)
               for field in P.SUPPORT_FIELDS), "BASE_IMPLEMENTATION_BINDING")
    files = {}
    for name, pin in manifest["files"].items():
        first, rest = name.split("/", 1)
        path = runtimes[first] / rest if first in runtimes else BASE / "installation" / name
        if name in replacements:
            path, pin = replacements[name]
        files[name] = {"source": str(path), **pin}
    plan = {"schema": installer.PLAN_SCHEMA, "files": files,
            **{key: manifest[key] for key in ("roles", "compiled_dirs", "support_groups")}}
    plan_raw = E.canonical_json(plan)
    output.mkdir(); package = output / "package"; package.mkdir()
    H.fresh_bytes(output / "INSTALLATION-PLAN.json", plan_raw)
    result = installer.assemble(package / "installation", plan_raw, H.digest(plan_raw),
                                runtime_roots=runtimes, deadline=start + 90)
    check()
    installed, installed_pin = H.read_json(package / "installation/INSTALLATION.json",
                                          result["manifest_sha256"], check)
    expected_files = dict(manifest["files"], **{name: pin for name, (_, pin) in replacements.items()})
    H.need(installed["files"] == expected_files and
           all(installed[key] == manifest[key] for key in ("schema", "roles", "compiled_dirs", "support_groups")) and
           set(installed["implementation"]) == set(manifest["implementation"]) and
           {key for key in installed["implementation"] if installed["implementation"][key] !=
            manifest["implementation"][key]} == {"adapter_support", "snapshot_support"} and
           S.implementation_id(E.canonical_json(installed["implementation"])) == result["implementation_id"] and
           result["implementation_id"] != OLD_IMPLEMENTATION, "EXACT_IMPLEMENTATION_DELTA")
    updated_profile = dict(profile, installation_manifest_sha256=installed_pin["sha256"])
    profile_raw = E.canonical_json(updated_profile)
    updated_pin = {"bytes": len(profile_raw), "sha256": H.digest(profile_raw)}
    expected = dict(baseline, **{"installation/" + name: pin for name, (_, pin) in replacements.items()})
    expected.update({"installation/INSTALLATION.json": installed_pin, "PROFILE.json": updated_pin})
    auxiliary = {name: pin for name, pin in baseline.items()
                 if name != "PROFILE.json" and not name.startswith("installation/")}
    H.need(len(auxiliary) == 125 and set(auxiliary) == set(profile["files"]) | DOCUMENTS,
           "EXACT_AUXILIARY_AND_DOCUMENT_CENSUS")
    for name, pin in auxiliary.items():
        destination = package / H.relative(name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        H.ordinary(destination.parent, directory=True)
        with H.ordinary(BASE / name).open("rb") as incoming, H.ordinary(destination, fresh=True).open("xb") as outgoing:
            size = 0
            while block := incoming.read(MIB):
                check(); size += len(block); H.need(size <= pin["bytes"], "COPY_GREW")
                outgoing.write(block)
            outgoing.flush(); os.fsync(outgoing.fileno())
        H.need(H.pin(destination, check) == pin, "AUXILIARY_COPY_PIN")
    H.census(package, set(expected) - {"PROFILE.json"}, check)
    for name in set(expected) - {"PROFILE.json"}:
        H.need(H.pin(package / name, check) == expected[name], "PACKAGE_OUTPUT_PIN")
    for path, pin in selected.items():
        H.need(H.pin(Path(path), check) == pin, "INPUT_CHANGED")
    H.census(BASE, baseline, check)
    changed = sorted(name for name in expected if expected[name] != baseline[name])
    expected_changed = {"PROFILE.json", "installation/INSTALLATION.json"} | {
        "installation/lean-src/" + name + ".lean" for name in CHANGED_SOURCES} | {
        "installation/lean-lib/" + name + ".olean" for name in RECOMPILED - {"BasisSnapshot"}}
    H.need(set(changed) == expected_changed and len(changed) == 9, "EXACT_NINE_FILE_DELTA")
    H.fresh_bytes(package / "PROFILE.json", profile_raw)
    H.census(package, expected, check)
    H.need(H.pin(package / "PROFILE.json", check) == updated_pin, "FINAL_PROFILE")
    report = {"status": "ASSEMBLED_NOT_ADOPTED", "package": str(package), "files": expected,
        "profile_sha256": updated_pin["sha256"], "installation_manifest_sha256": installed_pin["sha256"],
        "implementation_id": result["implementation_id"], "base_implementation_id": OLD_IMPLEMENTATION,
        "build_sha256": BUILD_SHA, "changed_files": changed, "unchanged_files": len(expected) - len(changed),
        "native_calls": 0, "owner_opened": False, "wall_seconds": time.monotonic() - start,
        "cpu_seconds": time.process_time() - cpu,
        "claim": "FILE_ASSEMBLY_NOT_MATHEMATICAL_ACCEPTANCE_OR_STATE_MIGRATION"}
    H.fresh_bytes(output / "ASSEMBLY.json", H.canonical(report))
    check()
    print(json.dumps(report, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

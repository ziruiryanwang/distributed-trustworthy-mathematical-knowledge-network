"""Fresh four-file parse-reuse successor using the existing file-only installer."""
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
BASE = ROOT / "experiments/v5-local-checks/current-release-build01/distribution/package"
PREFIX = "software/v5/ordinary_parse_reuse/"
RELEASE = ROOT / "software/v5/ordinary_current_release/release.json"
RELEASE_SHA = "821796aa5b4996edd3f34babdb3be186d8321e0b3b4208b1e3f18705400caf78"
BASE_PROFILE = "7c41db618e17dd9b296df6aa566d2673b72edd859023bcfb7369e11925685541"
BASE_INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
HELPER = "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
ORDINARY = "software/v5/ordinary_lean/"
CORE = "ordinary_admission ordinary_evidence ordinary_semantics portable_evidence portable_catalog local_catalog".split()
MIB = 1024**2


def load(name, path):
    if name in sys.modules:
        raise ValueError("PARSE_ASSEMBLY_MODULE_ALREADY_LOADED")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def main():
    start, cpu = time.monotonic(), time.process_time()
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("admission-sha256", "intake-sha256", "output"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    if not (os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
            sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize):
        raise ValueError("PARSE_ASSEMBLY_ISOLATED_CANONICAL_PROCESS")
    helper_path = SOURCE_ROOT / HELPER
    if hashlib.sha256(helper_path.read_bytes()).hexdigest() != HELPER_SHA:
        raise ValueError("PARSE_ASSEMBLY_HELPER_PIN")
    H = load("_parse_assembly_files", helper_path)

    def check():
        H.need(time.monotonic()-start < 150 and time.process_time()-cpu < 70,
               "PARSE_ASSEMBLY_150_WALL_70_CPU")

    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    H.need(output.name == "distribution" and output.parent.name == "parse-reuse-package01" and
           output.parent.parent == ROOT / "experiments/v5-local-checks", "OUTPUT_SCOPE")
    selected = {}

    def remember(path, expected=None, maximum=128*MIB):
        actual = H.pin(path, check, maximum)
        H.need(expected is None or actual == expected or
               isinstance(expected, str) and actual["sha256"] == expected, "SELECTED_PIN")
        key = str(path)
        H.need(key not in selected or selected[key] == actual, "SELECTED_OVERLAP")
        selected[key] = actual
        return actual

    release, _ = H.read_json(RELEASE, RELEASE_SHA, check)
    remember(RELEASE, RELEASE_SHA)
    profile, profile_pin = H.read_json(BASE / "PROFILE.json", BASE_PROFILE, check)
    manifest, manifest_pin = H.read_json(BASE / "installation/INSTALLATION.json", BASE_INSTALLATION, check)
    baseline = dict(release["prebuilt"]["files"])
    for name in ("authoring/bin/BaselineExporter.exe", "authoring/bin/MissingImportExporter.exe"):
        baseline[name] = profile["files"][name]
    baseline["PROFILE.json"] = profile_pin
    H.need(len(baseline) == 154 and len(profile["files"]) == 117 and
           profile["installation_manifest_sha256"] == BASE_INSTALLATION and
           baseline["installation/INSTALLATION.json"] == manifest_pin, "BASE_LAYOUT")
    H.census(BASE, baseline, check)
    for name, pin in baseline.items():
        H.relative(name); remember(BASE / name, pin)
    for key, pin in release["build"]["runtime_pins"].items():
        category, relative = key.split("/", 1)
        runtime_root = {"python_runtime": Path(r"D:\Python314"),
                        "lean_runtime": ROOT / "software/runtime/lean-4.34.0-windows"}[category]
        remember(runtime_root / H.relative(relative), pin, 512*MIB)
    core_source, intake_source = (SOURCE_ROOT / PREFIX / name for name in
                                  ("ordinary_admission.py", "baseline_intake.py"))
    core_pin = remember(core_source, H.hexid(args.admission_sha256))
    intake_pin = remember(intake_source, H.hexid(args.intake_sha256))
    H.need(core_pin != baseline["installation/py/ordinary_admission.py"] and
           intake_pin != baseline["reference/baseline_intake.py"], "TWO_NEW_SOURCES_REQUIRED")
    remember(helper_path, HELPER_SHA)
    remember(Path(__file__).resolve())
    remember(SOURCE_ROOT / PREFIX / "INSTALLATION-PLAN.md")
    for name in CORE:
        remember(SOURCE_ROOT / ORDINARY / (name + ".py"), manifest["files"]["py/"+name+".py"])
    remember(SOURCE_ROOT / ORDINARY / "ordinary_installation.py")
    H.need(all(name not in sys.modules for name in CORE), "INSTALLER_MODULE_COLLISION")
    installer = load("_parse_existing_installer", SOURCE_ROOT / ORDINARY / "ordinary_installation.py")
    for name in CORE:
        H.need(Path(sys.modules[name].__file__).resolve() == SOURCE_ROOT / ORDINARY / (name+".py"),
               "INSTALLER_SUPPORT_ORIGIN")
    E, S, A = installer.E, installer.S, installer.A
    old_implementation = S.implementation_id(E.canonical_json(manifest["implementation"]))
    H.need(all(manifest["implementation"][field] == A.support_digest(field, manifest)
               for field in installer.P.SUPPORT_FIELDS), "BASE_SUPPORT_DIGESTS")
    runtimes = {"python_runtime": Path(r"D:\Python314"),
                "lean_runtime": ROOT / "software/runtime/lean-4.34.0-windows"}
    files = {}
    for name, pin in manifest["files"].items():
        first, rest = name.split("/", 1)
        source = runtimes[first] / rest if first in runtimes else BASE / "installation" / name
        if name == "py/ordinary_admission.py":
            source, pin = core_source, core_pin
        files[name] = {"source": str(source), **pin}
    plan = {"schema": installer.PLAN_SCHEMA, "files": files,
            **{key: manifest[key] for key in ("roles", "compiled_dirs", "support_groups")}}
    plan_raw = E.canonical_json(plan)
    output.mkdir(); package = output / "package"; package.mkdir()
    H.fresh_bytes(output / "INSTALLATION-PLAN.json", plan_raw)
    check()
    result = installer.assemble(package / "installation", plan_raw, H.digest(plan_raw),
                                runtime_roots=runtimes, deadline=start+150)
    check()
    installed, installed_pin = H.read_json(package / "installation/INSTALLATION.json",
                                          result["manifest_sha256"], check)
    expected_files = dict(manifest["files"], **{"py/ordinary_admission.py": core_pin})
    H.need(installed["files"] == expected_files and
           all(installed[key] == manifest[key] for key in ("schema", "roles", "compiled_dirs", "support_groups")) and
           {key for key in installed["implementation"] if installed["implementation"][key] !=
            manifest["implementation"].get(key)} == {"controller_support"} and
           result["implementation_id"] != old_implementation and
           S.implementation_id(E.canonical_json(installed["implementation"])) == result["implementation_id"],
           "NEW_INSTALLATION_EXACT_DELTA")
    new_profile = dict(profile, installation_manifest_sha256=installed_pin["sha256"],
                       files=dict(profile["files"], **{"reference/baseline_intake.py": intake_pin}))
    profile_raw = E.canonical_json(new_profile)
    new_profile_pin = {"bytes": len(profile_raw), "sha256": H.digest(profile_raw)}
    expected = dict(baseline, **{"installation/py/ordinary_admission.py": core_pin,
        "reference/baseline_intake.py": intake_pin, "installation/INSTALLATION.json": installed_pin,
        "PROFILE.json": new_profile_pin})
    for name, pin in expected.items():
        if name == "PROFILE.json" or name.startswith("installation/"):
            continue
        source = intake_source if name == "reference/baseline_intake.py" else BASE / name
        destination = package / H.relative(name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        H.ordinary(destination.parent, directory=True)
        with H.ordinary(source).open("rb") as incoming, H.ordinary(destination, fresh=True).open("xb") as outgoing:
            size = 0
            while block := incoming.read(MIB):
                check(); size += len(block); H.need(size <= pin["bytes"], "COPY_GREW")
                outgoing.write(block)
            outgoing.flush(); os.fsync(outgoing.fileno())
        H.need(H.pin(destination, check) == pin, "COPY_PIN")
    H.census(package, set(expected)-{"PROFILE.json"}, check)
    for name in set(expected)-{"PROFILE.json"}:
        H.need(H.pin(package / name, check) == expected[name], "OUTPUT_PIN")
    for path, pin in selected.items():
        H.need(H.pin(Path(path), check, 512*MIB) == pin, "INPUT_CHANGED")
    H.census(BASE, baseline, check)
    changed = sorted(name for name in expected if expected[name] != baseline[name])
    H.need(changed == ["PROFILE.json", "installation/INSTALLATION.json",
                       "installation/py/ordinary_admission.py", "reference/baseline_intake.py"], "FOUR_FILE_DELTA")
    H.fresh_bytes(package / "PROFILE.json", profile_raw)
    H.census(package, expected, check)
    H.need(H.pin(package / "PROFILE.json", check) == new_profile_pin, "FINAL_PROFILE")
    receipt = {"status": "ASSEMBLED_NOT_ADOPTED", "files": expected, "package": str(package),
        "profile_sha256": new_profile_pin["sha256"], "installation_manifest_sha256": installed_pin["sha256"],
        "implementation_id": result["implementation_id"], "base_implementation_id": old_implementation,
        "changed_files": changed, "unchanged_files": 150, "native_calls": 0,
        "wall_seconds": time.monotonic()-start, "cpu_seconds": time.process_time()-cpu,
        "claim": "FILE_ASSEMBLY_NOT_MATHEMATICAL_ACCEPTANCE_OR_STATE_MIGRATION"}
    H.fresh_bytes(output / "ASSEMBLY.json", H.canonical(receipt))
    check()
    print(json.dumps(receipt, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

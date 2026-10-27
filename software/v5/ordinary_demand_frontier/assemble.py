"""File-only authoring frontier overlay; no product import, Lean or owner state.

Derived from the retained ordinary_intake_progress file-only copier. Select real
build/result and payload-map hashes after review. Never infer build success from
partial files. Existing package and failed partial output remain untouched.
"""
import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
BASE = LOCAL / "kernel-admission-package01/distribution/package"
RECEIPT = BASE.parent / "ASSEMBLY.json"
RECEIPT_SHA = "4515b25967ca432f9512df445eb870b3d5e276356339a5ac6a1ac5f73c6e37fe"
PROFILE_SHA = "60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b"
INSTALLATION_SHA = "9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27"
IMPLEMENTATION = "86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
MODULES = ("OwnerConstruction", "PortableOwnerConstructCommand",
           "PortableConstructExportCommand", "PortableContributionExportCommand")
PARTS = (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")
PYTHON_FILES = {
    "owner.py": "owner.py",
    "authoring/py/ordinary_contribution.py": "ordinary_contribution.py",
    "authoring/py/portable_owner_request.py": "portable_owner_request.py",
    "authoring/py/retained_preparation.py": "retained_preparation.py",
}
DOCUMENTS = {"BOUNDED-TRANSPORT.md", "CONTACTS.md", "EXECUTION-TRUST.md", "LAUNCHER.md",
             "PRODUCER.md", "README.md", "RECEIVE-POLICY.md", "SPARSE-SEARCH.md"}
MIB = 1024**2


def main():
    start, cpu = time.monotonic(), time.process_time()
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("build-root", "build-sha256", "build-result-sha256",
                 "payload-map-sha256", "output"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    if not (os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
            sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize and
            Path(sys.executable).resolve() == Path(r"D:\Python314\python.exe")):
        raise ValueError("FRONTIER_ASSEMBLY_CANONICAL_PROCESS")
    source = Path(__file__).resolve().parent
    if not (source.is_relative_to(LOCAL) and
            source.parts[-4:] == ("sources", "software", "v5", "ordinary_demand_frontier")):
        raise ValueError("FRONTIER_ASSEMBLY_SOURCE_SNAPSHOT")
    helper = source.parent / "ordinary_fair_search/assemble.py"
    helper_raw = helper.read_bytes()
    if hashlib.sha256(helper_raw).hexdigest() != HELPER_SHA:
        raise ValueError("FRONTIER_ASSEMBLY_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_frontier_assembly_files", helper)
    H = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = H
    exec(compile(helper_raw, str(helper), "exec", dont_inherit=True), H.__dict__)

    def check():
        H.need(time.monotonic() - start < 90 and time.process_time() - cpu < 45,
               "FRONTIER_ASSEMBLY_ALLOWANCE")

    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    H.need(output == source.parents[3] / "distribution", "FRONTIER_OUTPUT_SCOPE")
    native = H.ordinary(Path(args.build_root), directory=True)
    H.need(native.is_relative_to(LOCAL) and native.name == "native" and
           native.parent != output.parent, "FRONTIER_BUILD_SCOPE")
    inputs = {}

    def remember(path, expected=None, maximum=128*MIB):
        actual = H.pin(path, check, maximum)
        H.need(expected is None or actual == expected or
               isinstance(expected, str) and actual["sha256"] == expected, "FRONTIER_INPUT_PIN")
        H.need(not path.is_relative_to(output) and not output.is_relative_to(path),
               "FRONTIER_INPUT_OUTPUT_OVERLAP")
        key = str(path)
        H.need(key not in inputs or inputs[key] == actual, "FRONTIER_INPUT_CONFLICT")
        inputs[key] = actual
        return actual

    def document(path, digest):
        doc, pin = H.read_json(path, digest, check)
        remember(path, pin)
        return doc, pin

    remember(Path(__file__), maximum=2*MIB)
    remember(helper, HELPER_SHA, 2*MIB)
    receipt, _ = document(RECEIPT, RECEIPT_SHA)
    profile, profile_pin = document(BASE / "PROFILE.json", PROFILE_SHA)
    installation, installation_pin = document(BASE / "installation/INSTALLATION.json", INSTALLATION_SHA)
    baseline = receipt["files"]
    projected = dict(profile["files"])
    for name, pin in installation["files"].items():
        H.relative(name)
        if name.partition("/")[0] not in ("python_runtime", "lean_runtime"):
            H.need("installation/" + name not in projected, "FRONTIER_BASE_OVERLAP")
            projected["installation/" + name] = pin
    projected.update({"PROFILE.json": profile_pin, "installation/INSTALLATION.json": installation_pin})
    H.need(receipt["status"] == "ASSEMBLED_NOT_ADOPTED" and receipt["package"] == str(BASE) and
           receipt["implementation_id"] == IMPLEMENTATION and
           receipt["profile_sha256"] == PROFILE_SHA and
           receipt["installation_manifest_sha256"] == INSTALLATION_SHA and
           profile["installation_manifest_sha256"] == INSTALLATION_SHA and
           len(baseline) == 154 and len(profile["files"]) == 117 and len(projected) == 146 and
           set(baseline) - set(projected) == DOCUMENTS and
           all(baseline.get(name) == pin for name, pin in projected.items()), "FRONTIER_EXACT_BASE")
    H.need(H.digest(b"DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1\0" +
                    H.canonical(installation["implementation"])) == IMPLEMENTATION,
           "FRONTIER_UNCHANGED_IMPLEMENTATION")
    H.census(BASE, baseline, check)
    for name, pin in baseline.items():
        H.relative(name); H.pin_shape(pin); remember(BASE / name, pin)

    build, _ = document(native / "BUILD.json", H.hexid(args.build_sha256))
    outer, _ = document(native.parent / "RESULT.json", H.hexid(args.build_result_sha256))
    output_names = {module + suffix for module in MODULES for suffix in PARTS}
    H.need(outer["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1" and
           outer["result"]["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and
           build["status"] == "FOUR_AUTHORING_HELPERS_COMPILED_NOT_TESTED_OR_INSTALLED" and
           build["base_profile_sha256"] == PROFILE_SHA and
           build["base_installation_sha256"] == INSTALLATION_SHA and
           build["native_compilations"] == 4 and build["owner_states_opened"] == 0 and
           build["receiver_compilations"] == 0 and set(build["source_pins"]) == set(MODULES) and
           set(build["compiled_files"]) == output_names and len(build["commands"]) == 4 and
           [row["module"] for row in build["commands"]] == list(MODULES) and
           all(row["exit_code"] == 0 for row in build["commands"]), "FRONTIER_ACTUAL_BUILD")
    selection, _ = document(native.parent / "selection.json", H.hexid(outer["selection_sha256"]))
    H.need(selection["schema"] == "DMKN_V5_LOCAL_CHECK_V1" and
           selection["name"] == native.parent.name, "FRONTIER_BUILD_SELECTION")
    H.census(native / "lean-src", {m + ".lean" for m in MODULES}, check)
    H.census(native / "lean-lib", output_names, check)
    for module in MODULES:
        expected = H.pin_shape(build["source_pins"][module])
        H.need(selection["sources"]["software/v5/ordinary_demand_frontier/" + module + ".lean"] ==
               expected["sha256"], "FRONTIER_BUILD_SOURCE_SELECTION")
        remember(native / "lean-src" / (module + ".lean"), expected, 2*MIB)
        remember(source / (module + ".lean"), expected, 2*MIB)
    replacements = {}
    for name, local in PYTHON_FILES.items():
        replacements[name] = (source / local, remember(source / local, maximum=2*MIB))
        H.need(replacements[name][1] != baseline[name], "FRONTIER_PYTHON_NOT_CHANGED")
    for name in sorted(output_names):
        pin = H.pin_shape(build["compiled_files"][name])
        path = native / "lean-lib" / name
        replacements["authoring/helpers/" + name] = (path, remember(path, pin, 64*MIB))
    payloads = {name: pin for name, (_, pin) in replacements.items()}
    H.need(len(payloads) == 24 and set(payloads) <= set(profile["files"]) and
           H.digest(H.canonical(payloads)) == H.hexid(args.payload_map_sha256),
           "FRONTIER_REVIEWED_REPLACEMENT_MAP")
    updated_profile = dict(profile, files=dict(profile["files"], **payloads))
    profile_raw = H.canonical(updated_profile)
    updated_pin = {"bytes": len(profile_raw), "sha256": H.digest(profile_raw)}
    expected = dict(baseline, **payloads)
    expected["PROFILE.json"] = updated_pin
    H.need(len(expected) == 154 and len(updated_profile["files"]) == 117 and
           sum(pin["bytes"] for pin in expected.values()) <= 256*MIB,
           "FRONTIER_SUCCESSOR_CENSUS_AND_SIZE")
    changed = sorted(name for name in expected if expected[name] != baseline[name])
    H.need(set(changed) <= set(payloads) | {"PROFILE.json"} and
           set(PYTHON_FILES) | {"PROFILE.json"} <= set(changed) and
           all(expected[name] == baseline[name] for name in DOCUMENTS) and
           all(expected[name] == baseline[name] for name in baseline if name.startswith("installation/")),
           "FRONTIER_AUXILIARY_ONLY_DELTA")

    output.mkdir()
    package = output / "package"
    package.mkdir()
    for name in sorted(set(expected) - {"PROFILE.json"}):
        origin = replacements[name][0] if name in replacements else BASE / name
        target = package / H.relative(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        H.ordinary(target.parent, directory=True)
        count = 0
        with H.ordinary(origin).open("rb") as incoming, H.ordinary(target, fresh=True).open("xb") as outgoing:
            while block := incoming.read(MIB):
                check(); count += len(block)
                H.need(count <= expected[name]["bytes"], "FRONTIER_COPY_GREW")
                outgoing.write(block)
            outgoing.flush(); os.fsync(outgoing.fileno())
        H.need(H.pin(target, check) == expected[name], "FRONTIER_COPY_READBACK")
    H.census(package, set(expected) - {"PROFILE.json"}, check)
    H.census(BASE, baseline, check)
    for path, pin in inputs.items():
        H.need(H.pin(Path(path), check) == pin, "FRONTIER_INPUT_CHANGED")
    for name in set(expected) - {"PROFILE.json"}:
        H.need(H.pin(package / name, check) == expected[name], "FRONTIER_OUTPUT_CHANGED")
    H.fresh_bytes(package / "PROFILE.json", profile_raw)
    H.census(package, expected, check)
    H.need(H.pin(package / "PROFILE.json", check) == updated_pin, "FRONTIER_FINAL_PROFILE")
    report = {"status": "ASSEMBLED_NOT_ADOPTED", "package": str(package), "files": expected,
        "base_profile_sha256": PROFILE_SHA, "profile_sha256": updated_pin["sha256"],
        "installation_manifest_sha256": INSTALLATION_SHA, "implementation_id": IMPLEMENTATION,
        "build_sha256": args.build_sha256, "build_result_sha256": args.build_result_sha256,
        "reviewed_payload_map_sha256": args.payload_map_sha256, "replacement_files": payloads,
        "changed_files": changed, "unchanged_files": len(expected) - len(changed),
        "native_calls": 0, "owner_opened": False, "wall_seconds": time.monotonic() - start,
        "cpu_seconds": time.process_time() - cpu,
        "claim": "AUXILIARY_ONLY_FILE_ASSEMBLY_NOT_MATHEMATICAL_ACCEPTANCE"}
    H.fresh_bytes(output / "ASSEMBLY.json", H.canonical(report))
    check()
    print(H.canonical(report).decode("utf-8"), flush=True)


if __name__ == "__main__":
    main()

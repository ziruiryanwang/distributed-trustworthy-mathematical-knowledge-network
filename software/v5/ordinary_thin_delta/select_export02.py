"""Select one existing public export of retained compiled author-A declarations.

File inspection/selection only: no package imports, native work, owner opening,
intake or registration. The selected public produce-baseline command, if root
separately launches it, extracts complete proofs; production is not acceptance.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_thin_delta/"
NAME = "thin-delta-export-02"
BUILD_RUN = LOCAL/"native-src01"
PACKAGE = BUILD_RUN/"distribution/package"
AUTHOR = LOCAL/"ordinary-reference-public-continuation-02/workflow/author-A"
BASE = LOCAL/"ordinary-baseline-native-workflow-02/workflow/original-library"
TARGET_FILE = LOCAL/"ordinary-reference-public-workflow-01/workflow/fixtures/A-targets.json"
MODULE = "DMKNAuthor_9c9ea8a5496754b2a6e369b198f863ad7cd70c826642c2be283bab15de4a6306"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
MIB = 1024**2
ASSEMBLER_FILE = "software/v5/ordinary_producer_package/assemble.py"
ASSEMBLER = "39b7525a9881099f1c07190ec13d848c6d9b94078fc8ea0d07298b87ab3d741a"
RESULT = "d7a7b6f42ff0986ab9c2708c8a1a4f2386245f0798931f303eed46aaa8fa5b2f"
BUILD = "26e975ad71675ccc13cc93e0d80f343922b0a9ff046f20cfe37c54ea713c2f82"
BUILD_SELECTION = "6f5205b1590d2031e60617691424530c8b87ee5a86e1798f54b82c6664c3a172"
PROFILE = "fc45893cef624978f0ab5212d0e1e172ff7c71f821124daa8751727bf7123ef6"
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
PROJECT = "60376198a6fd6459564d55f1b8cccf0e57ff31ca6b4018ee8a0e17b7142fc59c"
TARGETS = "ddea2b29e902165a70df7cad854fd8eb2cc3116d18d86f0e43d5d287ae620882"
RUNNER = "44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651"
AUTHOR_FILES = {
    ".olean": (5240, "3ee1fd2f23700c30e23592768113aa3221d9d4c6c75dae1bb85848586d631ef2"),
    ".olean.server": (832, "63c4b9381552fc1a449e4770be6e6fd5e6adaee9e105bf20eba937f197d6deba"),
    ".olean.private": (5800, "14de18521ae883159f7de4e2fed2721728ef6dad2c83289e44493b8dd8c18785"),
    ".ir.sig": (176, "37e7bcaad7a6f0a216ecb5b842495c065ab3bd96a3c6bf0af35870d250adb9ef"),
    ".ir": (1168, "29f7369966d8f1fdd766653067679cd7d436d4af25165175ea7dab5758a6a523"),
}
BASE_FILES = {
    ".olean": (55576, "c01be446c82658d45c0cbbd0f86a5316cd90618921e8a48c061e781fdc451780"),
    ".olean.server": (2680, "113ca315690481fa73fcf68cc8bd00820c6dfa9756bb2a40e1283bd51c3fe8e4"),
    ".olean.private": (44008, "56a11d5b524ee9b379b4dc32deb197dfb8850cfe5ea4279068d548c7b1e842ef"),
    ".ir.sig": (176, "bed050bcdf93311893e40b34d22bb094663135dddb31587f3751f6033a69c21d"),
    ".ir": (19280, "259c08a7feba059da16a30f65816b649e75218ecd246402956afb7ee4250bc62"),
}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    started, cpu = time.monotonic(), time.process_time()
    need(len(sys.argv) == 1 and os.name == "nt" and Path.cwd() == ROOT and
         Path(__file__).resolve() == ROOT/PREFIX/"select_export02.py" and
         Path(sys.executable).resolve() == PYTHON/"python.exe" and
         sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize, "THIN_EXPORT_SELECTION_CONTEXT")

    def check():
        need(time.monotonic()-started < 60 and time.process_time()-cpu < 40,
             "THIN_EXPORT_SELECTION_ALLOWANCE")

    # Only previously reviewed file helpers are executed, never package code.
    assembler_path = ROOT/ASSEMBLER_FILE
    with assembler_path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == ASSEMBLER,
         "THIN_EXPORT_ASSEMBLER_PIN")
    name = "_thin_export_selection_files"
    need(name not in sys.modules, "THIN_EXPORT_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, assembler_path)
    S = importlib.util.module_from_spec(spec); sys.modules[name] = S
    exec(compile(raw, str(assembler_path), "exec"), S.__dict__)
    B = S.helper()
    pins = {}

    def keep(path, expected=None, maximum=128*MIB):
        check()
        pin = B.pin(path, check, maximum)
        need(expected is None or pin == expected or pin["sha256"] == expected,
             "THIN_EXPORT_INPUT_PIN:"+str(path))
        need(pins.setdefault(str(path), pin) == pin, "THIN_EXPORT_PIN_CONFLICT")
        return pin

    def document(path, expected):
        pin = keep(path, expected, 2*MIB)
        with path.open("rb") as stream:
            data = stream.read(2*MIB+1)
        need({"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()} == pin,
             "THIN_EXPORT_DOCUMENT_CHANGED")

        def pairs(items):
            result = {}
            for key, value in items:
                need(key not in result, "THIN_EXPORT_DUPLICATE_KEY")
                result[key] = value
            return result

        def reject(_):
            raise ValueError("THIN_EXPORT_NONFINITE_JSON")
        return json.loads(data, object_pairs_hook=pairs, parse_constant=reject)

    target = LOCAL/(NAME+".selection.json")
    B.ordinary(target, fresh=True); B.ordinary(LOCAL/NAME, directory=True, fresh=True)
    result = document(BUILD_RUN/"RESULT.json", RESULT)
    terminal = result["result"]
    need(result["selection_sha256"] == BUILD_SELECTION and
         terminal["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and
         terminal["child_exit_code"] == 0 and terminal["job_closed"] is True and
         terminal["direct_child_reaped"] is True and terminal["cleanup_errors"] == [] and
         terminal["termination_requested"] is False and
         terminal["final_job"]["active_processes"] == 0 and
         terminal["final_job"]["terminated_processes"] == 0,
         "THIN_EXPORT_BUILD_NOT_CLOSED")
    build = document(BUILD_RUN/"distribution/_build/BUILD-RESULT.json", BUILD)
    profile = document(PACKAGE/"PROFILE.json", PROFILE)
    manifest = document(PACKAGE/"installation/INSTALLATION.json", INSTALLATION)
    need(build["status"] == "BUILT_NOT_ADOPTED" and build["package"] == str(PACKAGE) and
         build["profile_sha256"] == PROFILE and
         build["installation_manifest_sha256"] == INSTALLATION and
         build["implementation_id"] == IMPLEMENTATION and
         build["files_excluding_profile"] == 141 and build["auxiliary_files"] == 111 and
         profile["installation_manifest_sha256"] == INSTALLATION and
         len(profile["files"]) == 111 and
         set(build["documentation_files"]) == {"README.md", "PRODUCER.md"},
         "THIN_EXPORT_BUILD_BINDING")
    payloads = dict(profile["files"])
    runtimes = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    for logical, pin in manifest["files"].items():
        parts = S.relative(logical).parts
        if parts[0] in runtimes:
            keep(runtimes[parts[0]].joinpath(*parts[1:]), pin)
        else:
            need("installation/"+logical not in payloads, "THIN_EXPORT_PAYLOAD_CONFLICT")
            payloads["installation/"+logical] = pin
    payloads["installation/INSTALLATION.json"] = pins[str(PACKAGE/"installation/INSTALLATION.json")]
    for logical, pin in build["documentation_files"].items():
        need(logical not in payloads, "THIN_EXPORT_DOCUMENT_CONFLICT")
        payloads[logical] = pin
    need(len(payloads) == 141 and
         S.tree(B, PACKAGE, check) == set(payloads) | {"PROFILE.json"},
         "THIN_EXPORT_PACKAGE_CENSUS")
    for logical, pin in payloads.items():
        keep(PACKAGE.joinpath(*S.relative(logical).parts), pin)
    need(payloads["authoring/bin/BaselineExporter.exe"] == {
         "bytes": 809472,
         "sha256": "0908634fbab219414acb7fc79bacc077612f39572b1957e22a2fb0d52438057a"},
         "THIN_EXPORT_ACTUAL_EXPORTER")

    project = document(ROOT/PREFIX/"project-selection02.json", PROJECT)
    with (ROOT/PREFIX/"project-selection02.json").open("rb") as stream:
        project_raw = stream.read(2*MIB+1)
    need(S.encoded(project) == project_raw and
         hashlib.sha256(project_raw).hexdigest() == PROJECT,
         "THIN_EXPORT_CANONICAL_PROJECT_BYTES")
    targets = document(TARGET_FILE, TARGETS)

    def lean_name(*components):
        return [[0, {"$bytes": list(part.encode("utf-8"))}] for part in components]

    need(project == {"schema": "DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1",
         "project_search_paths": [str(AUTHOR/"modules"), str(BASE)],
         "modules": [lean_name(MODULE)]} and targets == [
             lean_name("DMKNReferenceA", "flip_apply"),
             lean_name("DMKNReferenceA", "flip_involution")],
         "THIN_EXPORT_PROJECT_AND_TARGETS")
    for directory, stem, files in ((AUTHOR/"modules", MODULE, AUTHOR_FILES),
                                   (BASE, "DMKNBaselineFixture02", BASE_FILES)):
        need(S.tree(B, directory, check) == {stem+suffix for suffix in files},
             "THIN_EXPORT_MODULE_CENSUS")
        for suffix, (size, digest) in files.items():
            keep(directory/(stem+suffix), {"bytes": size, "sha256": digest})

    # The immutable existing targets remain runtime-pinned. The new project
    # config is snapshotted and supplies the runner's direct-command binding.
    expected_sources = {
        PREFIX+"select_export02.py": None,
        PREFIX+"project-selection02.json": PROJECT,
        ASSEMBLER_FILE: ASSEMBLER,
        S.BUILDER: S.BUILDER_SHA,
        "tools/Run-V5-Check.py": RUNNER,
    }
    sources = {relative: keep(ROOT/relative, expected, 2*MIB)["sha256"]
               for relative, expected in expected_sources.items()}
    runtime = {path: pin["sha256"] for path, pin in pins.items()}
    need(1 <= len(runtime) <= 256 and str(PYTHON/"python.exe") in runtime,
         "THIN_EXPORT_RUNTIME_BOUND")
    selection = {
        "schema": "DMKN_V5_LOCAL_CHECK_V1", "name": NAME,
        "sources": sources, "runtime_pins": runtime,
        "argv": [str(PYTHON/"python.exe"), "-I", "-S", "-B", str(PACKAGE/"owner.py"),
                 "produce-baseline", "--profile-sha256", PROFILE,
                 "--python-runtime", str(PYTHON), "--lean-runtime", str(LEAN),
                 "--project-production", "{snapshot}/"+PREFIX+"project-selection02.json",
                 "--project-production-sha256", PROJECT, "--approve-local-project",
                 "--output-names", str(TARGET_FILE), "--output", "{output}/bundle",
                 "--wall-seconds", "120", "--cpu-seconds", "90",
                 "--memory-mib", "1536", "--spool-mib", "144"],
        "limits": {"wall_seconds": 150, "cpu_seconds": 120, "memory_mib": 1792,
                   "active_processes": 6, "stdout_bytes": 4*MIB, "stderr_bytes": MIB},
    }
    for filename, expected in pins.items():
        need(B.pin(Path(filename), check, 128*MIB) == expected, "THIN_EXPORT_INPUT_CHANGED")
    data = S.encoded(selection)
    need(len(data) <= MIB, "THIN_EXPORT_SELECTION_SIZE")
    check(); B.fresh_bytes(target, data)
    digest = hashlib.sha256(data).hexdigest()
    need(B.pin(target, check, MIB) == {"bytes": len(data), "sha256": digest},
         "THIN_EXPORT_SELECTION_READBACK")
    print(json.dumps({"selection": str(target), "sha256": digest,
        "profile_sha256": PROFILE, "runtime_pin_count": len(runtime),
        "native_execution": "NOT_STARTED", "mathematical_acceptance": False}), flush=True)


if __name__ == "__main__":
    main()

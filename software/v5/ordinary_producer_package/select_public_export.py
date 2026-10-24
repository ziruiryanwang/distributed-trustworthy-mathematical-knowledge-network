"""Select one installed owner-free export of retained approved compiled inputs.

Selection only: no package import, native call, owner open, build or experiment.
The actual later call runs the installed owner.py directly, not a new harness.
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
PREFIX = "software/v5/ordinary_producer_package/"
NAME = "ordinary-producer-public-export-01"
ASSEMBLY_RUN = LOCAL/"ordinary-producer-assembly-01"
PACKAGE = ASSEMBLY_RUN/"package"
FIXTURE = LOCAL/"ordinary-baseline-native-workflow-02/workflow"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
MIB = 1024**2
ASSEMBLER = "39b7525a9881099f1c07190ec13d848c6d9b94078fc8ea0d07298b87ab3d741a"
RESULT = "3324a99685ffe9ddee6f28ead0c068968b7ed4e72f8f75efb0c5624cd98cd54a"
ASSEMBLY = "906634eb009ec7c275bef3a00ae295aebf78e3561fa16fadc7b20c632fc3d6cb"
PROFILE = "3e7caee37ebd969212246cdee6bc56f4d5458c417186537de982f4f09b2cd723"
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
PROJECT = "bb2753d5999774e4da0530503734633c48dcbc623ce29f5c3cc8a57f60fdfb45"
REQUEST = "db0cf7d2a7ed204b0919e62afbcfca6c7f9e06d7834288bd0a1a385ad5686d32"
TARGETS = "9e790e05aee9d1ba0ae5fc8fb9273afb815803d698da5085e90d54bc1662c722"
RUNNER = "44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651"
FIXTURE_FILES = {
    "DMKNBaselineFixture02.olean": (55576, "c01be446c82658d45c0cbbd0f86a5316cd90618921e8a48c061e781fdc451780"),
    "DMKNBaselineFixture02.olean.server": (2680, "113ca315690481fa73fcf68cc8bd00820c6dfa9756bb2a40e1283bd51c3fe8e4"),
    "DMKNBaselineFixture02.olean.private": (44008, "56a11d5b524ee9b379b4dc32deb197dfb8850cfe5ea4279068d548c7b1e842ef"),
    "DMKNBaselineFixture02.ir.sig": (176, "bed050bcdf93311893e40b34d22bb094663135dddb31587f3751f6033a69c21d"),
    "DMKNBaselineFixture02.ir": (19280, "259c08a7feba059da16a30f65816b649e75218ecd246402956afb7ee4250bc62"),
}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    started, cpu = time.monotonic(), time.process_time()
    need(len(sys.argv) == 1 and os.name == "nt" and Path.cwd() == ROOT and
         Path(__file__).resolve() == ROOT/PREFIX/"select_public_export.py" and
         Path(sys.executable).resolve() == PYTHON/"python.exe" and
         sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize, "PRODUCER_PUBLIC_SELECTION_CONTEXT")

    def check():
        need(time.monotonic()-started < 60 and time.process_time()-cpu < 40,
             "PRODUCER_PUBLIC_SELECTION_ALLOWANCE")

    # Reuse the already reviewed file-only path/pin helpers, never package code.
    assembler_path = ROOT/PREFIX/"assemble.py"
    with assembler_path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == ASSEMBLER,
         "PRODUCER_PUBLIC_ASSEMBLER_PIN")
    name = "_producer_public_selection_files"
    need(name not in sys.modules, "PRODUCER_PUBLIC_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, assembler_path)
    S = importlib.util.module_from_spec(spec); sys.modules[name] = S
    exec(compile(raw, str(assembler_path), "exec"), S.__dict__)
    B = S.helper()
    pins = {}

    def keep(path, expected=None, maximum=128*MIB):
        check()
        pin = B.pin(path, check, maximum)
        need(expected is None or pin == expected or pin["sha256"] == expected,
             "PRODUCER_PUBLIC_INPUT_PIN:"+str(path))
        need(pins.setdefault(str(path), pin) == pin, "PRODUCER_PUBLIC_PIN_CONFLICT")
        return pin

    def document(path, expected):
        pin = keep(path, expected, 2*MIB)
        with path.open("rb") as stream:
            data = stream.read(2*MIB+1)
        need({"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()} == pin,
             "PRODUCER_PUBLIC_DOCUMENT_CHANGED")
        def pairs(items):
            result = {}
            for key, value in items:
                need(key not in result, "PRODUCER_PUBLIC_DUPLICATE_KEY")
                result[key] = value
            return result
        def reject(_):
            raise ValueError("PRODUCER_PUBLIC_NONFINITE_JSON")
        return json.loads(data, object_pairs_hook=pairs, parse_constant=reject)

    target = LOCAL/(NAME+".selection.json")
    B.ordinary(target, fresh=True); B.ordinary(LOCAL/NAME, directory=True, fresh=True)
    terminal = document(ASSEMBLY_RUN/"RESULT.json", RESULT)["result"]
    need(terminal["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and
         terminal["child_exit_code"] == 0 and terminal["job_closed"] is True and
         terminal["direct_child_reaped"] is True and terminal["cleanup_errors"] == [] and
         terminal["final_job"]["active_processes"] == 0,
         "PRODUCER_PUBLIC_ASSEMBLY_NOT_CLOSED")
    assembly = document(PACKAGE/"ASSEMBLY.json", ASSEMBLY)
    profile = document(PACKAGE/"PROFILE.json", PROFILE)
    need(assembly["schema"] == "DMKN_ORDINARY_PRODUCER_ASSEMBLY_V1" and
         assembly["status"] == "ASSEMBLED_NOT_ADOPTED" and
         assembly["profile_sha256"] == PROFILE and
         assembly["installation_manifest_sha256"] == INSTALLATION and
         profile["installation_manifest_sha256"] == INSTALLATION,
         "PRODUCER_PUBLIC_ASSEMBLY_BINDING")
    payloads = assembly["payloads"]
    need(len(payloads) == 169 and len(profile["files"]) == 140 and
         S.tree(B, PACKAGE, check) == set(payloads) | {"PROFILE.json", "ASSEMBLY.json"},
         "PRODUCER_PUBLIC_PACKAGE_CENSUS")
    for logical, pin in payloads.items():
        keep(PACKAGE.joinpath(*S.relative(logical).parts), pin)
    need(all(payloads.get(logical) == pin for logical, pin in profile["files"].items()),
         "PRODUCER_PUBLIC_PROFILE_PAYLOADS")
    manifest = document(PACKAGE/"installation/INSTALLATION.json", INSTALLATION)
    runtimes = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    for logical, pin in manifest["files"].items():
        parts = S.relative(logical).parts
        if parts[0] in runtimes:
            keep(runtimes[parts[0]].joinpath(*parts[1:]), pin)
        else:
            need(payloads.get("installation/"+logical) == pin,
                 "PRODUCER_PUBLIC_INSTALLATION_PAYLOAD")

    project = document(FIXTURE/"project-selection.json", PROJECT)
    request = document(FIXTURE/"export-request.json", REQUEST)
    targets = document(ROOT/PREFIX/"selected_targets.json", TARGETS)
    need(project["schema"] == "DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1" and
         project["project_search_paths"] == [str(FIXTURE/"original-library")] and
         project["modules"] == request["modules"] and
         targets == request["targets"] and len(targets) == 2,
         "PRODUCER_PUBLIC_RETAINED_TARGET_SELECTION")
    need(S.tree(B, FIXTURE/"original-library", check) == set(FIXTURE_FILES),
         "PRODUCER_PUBLIC_COMPILED_FIXTURE_CENSUS")
    for filename, (size, digest) in FIXTURE_FILES.items():
        keep(FIXTURE/"original-library"/filename, {"bytes": size, "sha256": digest})

    # The retained project selection is immutable and runtime-pinned. The target
    # file is snapshotted, satisfying Run-V5-Check's direct-command input rule.
    expected_sources = {
        PREFIX+"select_public_export.py": None,
        PREFIX+"selected_targets.json": TARGETS,
        PREFIX+"assemble.py": ASSEMBLER,
        S.BUILDER: S.BUILDER_SHA,
        "tools/Run-V5-Check.py": RUNNER,
    }
    sources = {relative: keep(ROOT/relative, expected, 2*MIB)["sha256"]
               for relative, expected in expected_sources.items()}
    runtime = {path: pin["sha256"] for path, pin in pins.items()}
    need(1 <= len(runtime) <= 256 and str(PYTHON/"python.exe") in runtime,
         "PRODUCER_PUBLIC_RUNTIME_BOUND")
    selection = {
        "schema": "DMKN_V5_LOCAL_CHECK_V1", "name": NAME,
        "sources": sources, "runtime_pins": runtime,
        "argv": [str(PYTHON/"python.exe"), "-I", "-S", "-B", str(PACKAGE/"owner.py"),
                 "produce-baseline", "--profile-sha256", PROFILE,
                 "--python-runtime", str(PYTHON), "--lean-runtime", str(LEAN),
                 "--project-production", str(FIXTURE/"project-selection.json"),
                 "--project-production-sha256", PROJECT, "--approve-local-project",
                 "--output-names", "{snapshot}/"+PREFIX+"selected_targets.json",
                 "--output", "{output}/bundle", "--wall-seconds", "120",
                 "--cpu-seconds", "90", "--memory-mib", "1536", "--spool-mib", "144"],
        "limits": {"wall_seconds": 150, "cpu_seconds": 120, "memory_mib": 1792,
                   "active_processes": 6, "stdout_bytes": 4*MIB, "stderr_bytes": MIB},
    }
    for filename, expected in pins.items():
        need(B.pin(Path(filename), check, 128*MIB) == expected, "PRODUCER_PUBLIC_INPUT_CHANGED")
    data = S.encoded(selection)
    need(len(data) <= MIB, "PRODUCER_PUBLIC_SELECTION_SIZE")
    check(); B.fresh_bytes(target, data)
    digest = hashlib.sha256(data).hexdigest()
    need(B.pin(target, check, MIB) == {"bytes": len(data), "sha256": digest},
         "PRODUCER_PUBLIC_SELECTION_READBACK")
    print(json.dumps({"selection": str(target), "sha256": digest,
        "profile_sha256": PROFILE, "runtime_pin_count": len(runtime),
        "native_execution": "NOT_STARTED", "mathematical_acceptance": False}), flush=True)


if __name__ == "__main__":
    main()

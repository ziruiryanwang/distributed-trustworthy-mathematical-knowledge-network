"""Copy one reviewed auxiliary successor; never open owner state or run Lean."""
import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE_ROOT = Path(__file__).resolve().parents[3]
LOCAL = ROOT / "experiments/v5-local-checks"
BASE = LOCAL / "parse-reuse-package01/distribution/package"
RECEIPT = LOCAL / "parse-reuse-package01/distribution/ASSEMBLY.json"
RECEIPT_SHA = "3be10529e729de0602cc6779fa563e305db742f41ec69683e12f79a017a3b5c9"
PROFILE_SHA = "37fcb52050beada7c1f9cdabd957d57a6a3a5adfc8b822d873595773734ff750"
INSTALLATION_SHA = "a7403d6b798a654f7e5c76a863304bf415ad6016c6634a35513e73657ab0f9eb"
IMPLEMENTATION = "89450cdf07416e0c07cb3ef51ae3f4e1c0393c12376207582b1f03bbb5a6de60"
OLD_INTAKE = "9b243232603206b3a0925f639a0b8b1a6cbf0de8ca093ad4aa3642c595ff1142"
HELPER = "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
PREFIX = "software/v5/ordinary_intake_progress/"
MIB = 1024**2


def main():
    start, cpu = time.monotonic(), time.process_time()
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--intake-sha256", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if not (os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
            sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize):
        raise ValueError("PROGRESS_ASSEMBLY_PROCESS")
    helper = SOURCE_ROOT / HELPER
    helper_raw = helper.read_bytes()
    if hashlib.sha256(helper_raw).hexdigest() != HELPER_SHA:
        raise ValueError("PROGRESS_ASSEMBLY_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_progress_assembly_files", helper)
    H = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = H
    exec(compile(helper_raw, str(helper), "exec"), H.__dict__)

    def check():
        H.need(time.monotonic()-start < 90 and time.process_time()-cpu < 45,
               "PROGRESS_ASSEMBLY_ALLOWANCE")

    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    H.need(output == LOCAL / "intake-progress-package01/distribution", "OUTPUT_SCOPE")
    receipt, receipt_pin = H.read_json(RECEIPT, RECEIPT_SHA, check)
    profile, profile_pin = H.read_json(BASE / "PROFILE.json", PROFILE_SHA, check)
    installed, installed_pin = H.read_json(BASE / "installation/INSTALLATION.json",
                                          INSTALLATION_SHA, check)
    baseline = receipt["files"]
    H.need(receipt["status"] == "ASSEMBLED_NOT_ADOPTED" and
           receipt["package"] == str(BASE) and receipt["implementation_id"] == IMPLEMENTATION and
           len(baseline) == 154 and baseline["PROFILE.json"] == profile_pin and
           baseline["installation/INSTALLATION.json"] == installed_pin and
           profile["installation_manifest_sha256"] == INSTALLATION_SHA and
           len(profile["files"]) == 117 and
           all(baseline[name] == pin for name, pin in profile["files"].items()) and
           baseline["reference/baseline_intake.py"]["sha256"] == OLD_INTAKE,
           "EXACT_ADOPTED_BASE")
    H.need(hashlib.sha256(b"DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1\0" +
           H.canonical(installed["implementation"])).hexdigest() == IMPLEMENTATION,
           "UNCHANGED_IMPLEMENTATION")
    H.census(BASE, baseline, check)
    for name, expected in baseline.items():
        H.relative(name); H.pin_shape(expected)
        H.need(H.pin(BASE / name, check) == expected, "BASE_PIN")
    source = SOURCE_ROOT / PREFIX / "baseline_intake.py"
    source_pin = H.pin(source, check, 2*MIB)
    H.need(source_pin["sha256"] == H.hexid(args.intake_sha256) and
           source_pin["sha256"] != OLD_INTAKE, "REVIEWED_NEW_INTAKE")
    updated_profile = dict(profile, files=dict(profile["files"], **{
        "reference/baseline_intake.py": source_pin}))
    profile_raw = H.canonical(updated_profile)
    updated_pin = {"bytes": len(profile_raw), "sha256": H.digest(profile_raw)}
    expected = dict(baseline, **{"reference/baseline_intake.py": source_pin,
                                "PROFILE.json": updated_pin})
    output.mkdir()
    package = output / "package"
    package.mkdir()
    for name in sorted(set(expected)-{"PROFILE.json"}):
        origin = source if name == "reference/baseline_intake.py" else BASE / name
        target = package / H.relative(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        H.ordinary(target.parent, directory=True)
        count = 0
        with H.ordinary(origin).open("rb") as incoming, H.ordinary(target, fresh=True).open("xb") as outgoing:
            while block := incoming.read(MIB):
                check(); count += len(block)
                H.need(count <= expected[name]["bytes"], "COPY_GREW")
                outgoing.write(block)
            outgoing.flush(); os.fsync(outgoing.fileno())
        H.need(H.pin(target, check) == expected[name], "COPY_READBACK")
    H.census(package, set(expected)-{"PROFILE.json"}, check)
    H.census(BASE, baseline, check)
    for name, pin in baseline.items():
        H.need(H.pin(BASE / name, check) == pin, "BASE_CHANGED")
    H.need(H.pin(source, check, 2*MIB) == source_pin and
           H.pin(RECEIPT, check) == receipt_pin and
           H.pin(helper, check)["sha256"] == HELPER_SHA, "INPUT_CHANGED")
    H.need(sorted(name for name in expected if expected[name] != baseline[name]) ==
           ["PROFILE.json", "reference/baseline_intake.py"], "EXACT_TWO_FILE_DELTA")
    H.fresh_bytes(package / "PROFILE.json", profile_raw)
    H.census(package, expected, check)
    H.need(H.pin(package / "PROFILE.json", check) == updated_pin, "FINAL_PROFILE")
    report = {"status": "ASSEMBLED_NOT_ADOPTED", "package": str(package), "files": expected,
        "profile_sha256": updated_pin["sha256"], "installation_manifest_sha256": INSTALLATION_SHA,
        "implementation_id": IMPLEMENTATION, "unchanged_files": 152,
        "changed_files": ["PROFILE.json", "reference/baseline_intake.py"],
        "native_calls": 0, "owner_opened": False,
        "wall_seconds": time.monotonic()-start, "cpu_seconds": time.process_time()-cpu,
        "claim": "AUXILIARY_ONLY_FILE_ASSEMBLY_NOT_MATHEMATICAL_ACCEPTANCE"}
    H.fresh_bytes(output / "ASSEMBLY.json", H.canonical(report))
    check()
    print(H.canonical(report).decode("utf-8"), flush=True)


if __name__ == "__main__":
    main()

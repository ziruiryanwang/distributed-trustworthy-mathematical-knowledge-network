"""Select one direct public Std init/intake under the actual parse-reuse assembly."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_parse_reuse/"
STD_PREFIX = "software/v5/ordinary_std_intake/"
ASSEMBLY = LOCAL / "parse-reuse-package01"
PACKAGE = ASSEMBLY / "distribution/package"
BASE = LOCAL / "current-release-build01/distribution/package"
RELEASE = ROOT / "software/v5/ordinary_current_release/release.json"
RELEASE_SHA = "821796aa5b4996edd3f34babdb3be186d8321e0b3b4208b1e3f18705400caf78"
BASE_PROFILE_SHA = "7c41db618e17dd9b296df6aa566d2673b72edd859023bcfb7369e11925685541"
BASE_INSTALLATION_SHA = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
BASE_IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
PROFILE_SHA = "37fcb52050beada7c1f9cdabd957d57a6a3a5adfc8b822d873595773734ff750"
INSTALLATION_SHA = "a7403d6b798a654f7e5c76a863304bf415ad6016c6634a35513e73657ab0f9eb"
IMPLEMENTATION = "89450cdf07416e0c07cb3ef51ae3f4e1c0393c12376207582b1f03bbb5a6de60"
ADMISSION_SHA = "98c88eb0e7ea5e101f6ccd8e94b56a0cc248167c317a0440ba00dc86f503cd9a"
INTAKE_SHA = "9b243232603206b3a0925f639a0b8b1a6cbf0de8ca093ad4aa3642c595ff1142"
ASSEMBLER_SHA = "a7ec0d5393fadb62b17f8cecd9a38c44a1f669828c6d0591a3eec71a956cf064"
RUNNER_SHA = "44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651"
RECONSTRUCTOR_SHA = "244f1e17b80101961099cddf1bd557a655b3e76adb34894aa32ff14e31151868"
MANIFEST_SHA = "1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
RECONSTRUCTION = LOCAL / "std-reconstruct01"
BUNDLE = RECONSTRUCTION / "materialized"
INIT = LOCAL / "std-init01"
CATALOG, CUSTODY = LOCAL / "std-catalog01", LOCAL / "std-custody01"
STORE_ID = hashlib.sha256(b"DMKN_STD_RICH_BASE_LOCAL_STORE_V1:std-init01").hexdigest()
QUOTA = {"db_pages": 65536, "exports": 8192, "logical_bytes": 134217728, "objects": 4096}
CHANGED = ["PROFILE.json", "installation/INSTALLATION.json",
           "installation/py/ordinary_admission.py", "reference/baseline_intake.py"]
MIB = 1024**2
START, CPU_START = time.monotonic(), time.process_time()


def need(ok, code):
    if not ok:
        raise ValueError("STD_PARSE_SELECTION_" + code)


def check():
    need(time.monotonic()-START < 60 and time.process_time()-CPU_START < 30,
         "COOPERATIVE_60_WALL_30_CPU")


def hexid(value):
    need(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None, "HEX_ID")
    return value


def ordinary(path, *, fresh=False, directory=False):
    need(path.is_absolute() and ".." not in path.parts, "ABSOLUTE_PATH")
    for ancestor in (*reversed(path.parents), path):
        try:
            info = ancestor.lstat()
        except FileNotFoundError:
            need(fresh and ancestor == path, "MISSING_PATH")
            return path
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if ancestor != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "ORDINARY_PATH")
    need(not fresh, "OUTPUT_EXISTS")
    return path


def pin(path, maximum=512*MIB):
    check(); ordinary(path)
    size = path.stat().st_size
    need(0 <= size <= maximum, "FILE_BOUND")
    count, digest = 0, hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            check(); count += len(block)
            need(count <= size, "FILE_GREW")
            digest.update(block)
    need(count == ordinary(path).stat().st_size == size, "FILE_CHANGED")
    return {"bytes": size, "sha256": digest.hexdigest()}


def relative(name):
    need(type(name) is str and "\\" not in name and ":" not in name and
         not name.startswith("/") and PurePosixPath(name).as_posix() == name and
         all(part not in ("", ".", "..") for part in name.split("/")), "RELATIVE_PATH")
    return name


def clean(report):
    need(report.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED" and
         report.get("child_exit_code") == 0 and report.get("direct_child_reaped") is True and
         report.get("job_closed") is True and report.get("cleanup_errors") == [] and
         report.get("termination_requested") is False and
         report.get("final_job", {}).get("active_processes") == 0 and
         report.get("final_job", {}).get("terminated_processes") == 0 and
         report.get("observed_logs", {}).get("stderr_bytes") == 0, "UNCLEAN_OPERATION")


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--operation", choices=("init", "intake"), required=True)
    parser.add_argument("--assembly-result-sha256", required=True)
    parser.add_argument("--reconstruction-result-sha256", required=True)
    parser.add_argument("--init-result-sha256")
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON / "python.exe" and
         Path(__file__).absolute() == ROOT / PREFIX / "select_std.py", "PROCESS")
    hexid(args.assembly_result_sha256); hexid(args.reconstruction_result_sha256)
    need((args.init_result_sha256 is not None) == (args.operation == "intake"), "INIT_RESULT_ARGUMENT")
    if args.init_result_sha256 is not None:
        hexid(args.init_result_sha256)
    name = "std-init01" if args.operation == "init" else "std-intake01"
    destination = ordinary(LOCAL / (name + ".selection.json"), fresh=True)
    ordinary(LOCAL / name, fresh=True, directory=True)
    ordinary(CATALOG, fresh=args.operation == "init", directory=True)
    ordinary(CUSTODY, fresh=args.operation == "init", directory=True)
    need(shutil.disk_usage(ROOT).free >= 3*1024**3, "THREE_GIB_DISK_HEADROOM")
    pins = {}

    def retain(path, expected=None, maximum=512*MIB):
        actual = pin(path, maximum)
        if type(expected) is str:
            need(actual["sha256"] == hexid(expected), "INPUT_SHA:" + str(path))
        elif expected is not None:
            need(actual == expected, "INPUT_PIN:" + str(path))
        key = str(path)
        need(key not in pins or pins[key] == actual, "INPUT_OVERLAP")
        pins[key] = actual
        return actual

    def document(path, expected=None, maximum=2*MIB):
        actual = retain(path, expected, maximum)
        with path.open("rb") as stream:
            raw = stream.read(maximum+1)
        need(len(raw) == actual["bytes"] and hashlib.sha256(raw).hexdigest() == actual["sha256"],
             "DOCUMENT_CHANGED")
        def pairs(items):
            value = {}
            for key, item in items:
                need(key not in value, "DUPLICATE_JSON_KEY")
                value[key] = item
            return value
        return json.loads(raw, object_pairs_hook=pairs)

    def completed(run, result_sha, required_name):
        result = document(run / "RESULT.json", result_sha)
        selection = document(run / "selection.json", result["selection_sha256"])
        need(result["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1" and
             selection["schema"] == "DMKN_V5_LOCAL_CHECK_V1" and
             selection["name"] == required_name, "COMPLETION_BINDING")
        clean(result["result"])
        need(retain(run / "command/stderr.txt")["bytes"] == 0, "OUTER_STDERR")
        return selection, document(run / "command/stdout.txt", maximum=4*MIB)

    assembly_selection, assembly_stdout = completed(
        ASSEMBLY, args.assembly_result_sha256, "parse-reuse-package01")
    assembly = document(ASSEMBLY / "distribution/ASSEMBLY.json")
    need(assembly == assembly_stdout and assembly["status"] == "ASSEMBLED_NOT_ADOPTED" and
         assembly["package"] == str(PACKAGE) and assembly["native_calls"] == 0 and
         assembly["profile_sha256"] == PROFILE_SHA and
         assembly["installation_manifest_sha256"] == INSTALLATION_SHA and
         assembly["implementation_id"] == IMPLEMENTATION and
         assembly["base_implementation_id"] == BASE_IMPLEMENTATION and
         assembly["changed_files"] == CHANGED and assembly["unchanged_files"] == 150 and
         assembly["claim"] == "FILE_ASSEMBLY_NOT_MATHEMATICAL_ACCEPTANCE_OR_STATE_MIGRATION",
         "ASSEMBLY_COMPLETE")
    need(assembly_selection["sources"][PREFIX + "assemble.py"] == ASSEMBLER_SHA and
         assembly_selection["sources"][PREFIX + "ordinary_admission.py"] == ADMISSION_SHA and
         assembly_selection["sources"][PREFIX + "baseline_intake.py"] == INTAKE_SHA and
         assembly_selection["sources"]["tools/Run-V5-Check.py"] == RUNNER_SHA,
         "ASSEMBLY_SOURCE_BINDING")
    release = document(RELEASE, RELEASE_SHA)
    base_profile = document(BASE / "PROFILE.json", BASE_PROFILE_SHA)
    base_installation = document(BASE / "installation/INSTALLATION.json", BASE_INSTALLATION_SHA)
    baseline = dict(release["prebuilt"]["files"])
    for filename in ("authoring/bin/BaselineExporter.exe", "authoring/bin/MissingImportExporter.exe"):
        baseline[filename] = base_profile["files"][filename]
    baseline["PROFILE.json"] = pins[str(BASE / "PROFILE.json")]
    expected = assembly["files"]
    need(len(baseline) == len(expected) == 154 and set(expected) == set(baseline) and
         sorted(key for key in expected if expected[key] != baseline[key]) == CHANGED and
         expected["installation/py/ordinary_admission.py"] == {"bytes": 41372, "sha256": ADMISSION_SHA} and
         expected["reference/baseline_intake.py"] == {"bytes": 17024, "sha256": INTAKE_SHA},
         "EXACT_FOUR_FILE_DELTA")
    profile = document(PACKAGE / "PROFILE.json", PROFILE_SHA)
    installation = document(PACKAGE / "installation/INSTALLATION.json", INSTALLATION_SHA)
    need(len(profile["files"]) == 117 and
         base_profile["installation_manifest_sha256"] == BASE_INSTALLATION_SHA and
         baseline["installation/INSTALLATION.json"] == pins[str(BASE / "installation/INSTALLATION.json")] and
         profile == dict(base_profile, installation_manifest_sha256=INSTALLATION_SHA,
                         files=dict(base_profile["files"], **{
                             "reference/baseline_intake.py": expected["reference/baseline_intake.py"]})),
         "PROFILE_EXACT_DELTA")
    need(set(installation) == set(base_installation) and
         all(installation[key] == base_installation[key] for key in installation
             if key not in ("implementation", "files")) and
         installation["files"] == dict(base_installation["files"], **{
             "py/ordinary_admission.py": expected["installation/py/ordinary_admission.py"]}) and
         set(installation["implementation"]) == set(base_installation["implementation"]) and
         {key for key in installation["implementation"] if installation["implementation"][key] !=
          base_installation["implementation"][key]} == {"controller_support"}, "INSTALLATION_EXACT_DELTA")
    for descriptor, expected_id in ((base_installation["implementation"], BASE_IMPLEMENTATION),
                                    (installation["implementation"], IMPLEMENTATION)):
        raw = json.dumps(descriptor, sort_keys=True, ensure_ascii=False,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
        need(hashlib.sha256(b"DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1\0" + raw).hexdigest() == expected_id,
             "IMPLEMENTATION_BINDING")

    def package_census():
        seen = set()
        for directory, folders, files in os.walk(ordinary(PACKAGE, directory=True)):
            check(); ordinary(Path(directory), directory=True)
            for folder in folders:
                ordinary(Path(directory) / folder, directory=True)
            for filename in files:
                path = Path(directory) / filename
                key = path.relative_to(PACKAGE).as_posix()
                need(key in expected and key not in seen, "PACKAGE_CENSUS")
                seen.add(key)
        need(seen == set(expected), "COMPLETE_PACKAGE_CENSUS")

    package_census()
    for filename, expected_pin in expected.items():
        retain(PACKAGE / relative(filename), expected_pin)
    runtime = release["build"]["runtime_pins"]
    need(len(runtime) == 23, "RUNTIME_CENSUS")
    roots = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    for key, expected_pin in runtime.items():
        category, filename = relative(key).split("/", 1)
        need(category in roots, "RUNTIME_ROOT")
        retain(roots[category] / filename, expected_pin)

    mat_selection, mat = completed(RECONSTRUCTION, args.reconstruction_result_sha256, "std-reconstruct01")
    need(mat_selection["sources"][STD_PREFIX + "reconstruct.py"] == RECONSTRUCTOR_SHA and
         mat["status"] == "RESTORED_EXACT_INERT_BASELINE_NOT_ACCEPTED" and
         mat["output"] == str(BUNDLE) and mat["manifest_path"] == str(BUNDLE / "manifest.json") and
         mat["mathematical_acceptance"] is False and mat["binder_calls"] == 0 and
         mat["original_public_production"] == "FAILED_UNCHANGED" and
         mat["failed_materialize01"] == "FAILED_UNCHANGED" and
         mat["manifest"] == {"bytes": 468097, "sha256": MANIFEST_SHA} and
         mat["census"]["unit_files"] == 2651 and mat["census"]["unit_bytes"] == 44912843 and
         mat["census"]["files"] == 2653, "RECONSTRUCTION_COMPLETE")
    prepared = document(BUNDLE / "RECONSTRUCTION.json", mat["report"])
    need(prepared["status"] == "PREPARED_FOR_MANIFEST_NOT_COMPLETION" and
         prepared["mathematical_acceptance"] is False, "RECONSTRUCTION_METADATA")
    retain(BUNDLE / "manifest.json", mat["manifest"])
    # Inert units are selected by manifest and revalidated by actual intake,
    # not executed or added individually to the runner's 256-external-pin list.
    parent = None
    if args.operation == "intake":
        init_selection, public_stdout = completed(INIT, args.init_result_sha256, "std-init01")
        launch = document(INIT / "public-launch/LAUNCH.json")
        public = document(INIT / "public-launch/RUN.json")
        supervision = document(INIT / "public-launch/SUPERVISION.json")
        clean(supervision)
        need(public_stdout == public and public["ok"] is True and public["status"] == "CLI_EXITED_ZERO" and
             public["profile_sha256"] == PROFILE_SHA and
             public["installation_manifest_sha256"] == INSTALLATION_SHA and
             launch["profile_sha256"] == PROFILE_SHA and launch["tool"] == "owner", "PUBLIC_INIT_CLOSED")
        need(retain(INIT / "public-launch/child/stderr.txt")["bytes"] == 0, "INIT_CHILD_STDERR")
        owner = document(INIT / "public-launch/child/stdout.txt")
        need(owner["ok"] is True and owner["operation"] == "init" and
             owner.get("close_errors", []) == [] and owner["catalog"] == str(CATALOG) and
             owner["custody"] == str(CUSTODY) and owner["store_id"] == STORE_ID and
             owner["profile_sha256"] == PROFILE_SHA and owner["implementation_id"] == IMPLEMENTATION and
             owner["custody_limits"] == QUOTA and
             owner["result"]["status"] == "INITIALIZED_LOCAL_OWNER" and
             owner["result"]["basis"]["status"] == "CHECKED" and
             owner["result"]["basis"]["units_checked"] == 456, "PUBLIC_INIT_ACCEPTED")
        parent = hexid(owner["result"]["basis"]["local_root"])
        need(init_selection["runtime_pins"][str(PACKAGE / "PROFILE.json")] == PROFILE_SHA and
             init_selection["runtime_pins"][str(ASSEMBLY / "RESULT.json")] == args.assembly_result_sha256 and
             init_selection["sources"][PREFIX + "select_std.py"] == pin(Path(__file__))["sha256"] and
             init_selection["sources"][STD_PREFIX + "custody_limits.json"] ==
             pin(ROOT / STD_PREFIX / "custody_limits.json")["sha256"], "INIT_INPUT_BINDING")

    source_names = ("tools/Run-V5-Check.py", PREFIX + "select_std.py",
                    PREFIX + "PUBLIC-PLAN.md", STD_PREFIX + "custody_limits.json")
    sources = {key: pin(ROOT / key, 2*MIB) for key in source_names}
    need(sources["tools/Run-V5-Check.py"]["sha256"] == RUNNER_SHA and
         json.loads((ROOT / STD_PREFIX / "custody_limits.json").read_bytes()) == QUOTA, "SOURCE_BINDING")
    public_limits = (90, 60, 1280) if args.operation == "init" else (360, 300, 1536)
    outer_limits = (120, 90, 1536) if args.operation == "init" else (420, 330, 1792)
    argv = [str(PYTHON / "python.exe"), "-I", "-S", "-B", str(PACKAGE / "run.py"),
        "--profile-sha256", PROFILE_SHA, "--python-runtime", str(PYTHON), "--lean-runtime", str(LEAN),
        "--diagnostics", r"{output}\public-launch", "--wall-seconds", str(public_limits[0]),
        "--cpu-seconds", str(public_limits[1]), "--memory-mib", str(public_limits[2]),
        "--active-processes", "3", "--stdout-bytes", str(MIB), "--stderr-bytes", str(MIB),
        "owner", "--", "init" if args.operation == "init" else "intake-baseline",
        "--catalog", str(CATALOG), "--custody", str(CUSTODY), "--store-id", STORE_ID,
        "--custody-limits", r"{snapshot}\software\v5\ordinary_std_intake\custody_limits.json"]
    if parent is not None:
        argv += ["--parent-root", parent, "--bundle-directory", str(BUNDLE),
                 "--bundle-manifest", str(BUNDLE / "manifest.json"), "--bundle-manifest-sha256", MANIFEST_SHA]
    need(len(pins) == (191 if args.operation == "init" else 200) and
         len({key.casefold() for key in pins}) == len(pins), "EXACT_EXTERNAL_PIN_CENSUS")
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": name,
        "sources": {key: value["sha256"] for key, value in sources.items()},
        "runtime_pins": {key: value["sha256"] for key, value in pins.items()}, "argv": argv,
        "limits": {"wall_seconds": outer_limits[0], "cpu_seconds": outer_limits[1],
                   "memory_mib": outer_limits[2], "active_processes": 4,
                   "stdout_bytes": 4*MIB, "stderr_bytes": MIB}}
    package_census()
    for key, value in pins.items():
        need(pin(Path(key)) == value, "FINAL_INPUT_CHANGED")
    for key, value in sources.items():
        need(pin(ROOT / key, 2*MIB) == value, "FINAL_SOURCE_CHANGED")
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
    need(len(raw) <= MIB, "SELECTION_BOUND")
    check()
    with ordinary(destination, fresh=True).open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    need(destination.read_bytes() == raw, "SELECTION_READBACK")
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
        "runtime_pins": len(pins), "source_snapshots": len(sources), "store_id": STORE_ID,
        "parent_root": parent, "runtime": "NOT_STARTED", "protected_state_opened": False}), flush=True)


if __name__ == "__main__":
    main()

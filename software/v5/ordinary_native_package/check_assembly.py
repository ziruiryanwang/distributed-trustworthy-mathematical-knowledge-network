"""One selected file-assembly/refusal/loader boundary; no Lean or owner operation.

Run only inside the separately selected aggregate Job. Retain every output on
failure. This is a local qualification harness, not a distribution payload.
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

MIB = 1024**2
PREFIX = "software/v5/ordinary_native_package/"


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("source-root", "base-package", "exporter", "python-runtime",
                 "lean-runtime", "output", "source-map-sha256", "assembler-sha256",
                 "profile-source-sha256"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "ASSEMBLY_CHECK_PROFILE")
    started, cpu = time.monotonic(), time.process_time()
    root, output = Path(args.source_root), Path(args.output)
    need(root.is_absolute() and output.is_absolute() and output.is_dir(),
         "ASSEMBLY_CHECK_PATHS")
    # The outer runner already created output; this check owns only fresh children.
    negative, package = output/"wrong-map", output/"package"
    need(all(not path.is_relative_to(root) and not root.is_relative_to(path)
             for path in (negative, package)), "ASSEMBLY_CHECK_SOURCE_OUTPUT_OVERLAP")
    need(not negative.exists() and not package.exists(), "ASSEMBLY_CHECK_FRESH")
    source = root/PREFIX/"assemble.py"
    raw = source.read_bytes()
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == args.assembler_sha256,
         "ASSEMBLY_CHECK_SOURCE_PIN")
    common = [str(Path(args.python_runtime)/"python.exe"), "-I", "-S", "-B", str(source),
              "--source-root", str(root), "--base-package", args.base_package,
              "--exporter", args.exporter, "--python-runtime", args.python_runtime,
              "--lean-runtime", args.lean_runtime, "--wall-seconds", "60",
              "--cpu-seconds", "35"]
    history = []

    def invoke(label, destination, digest):
        result = subprocess.run(common+["--output", str(destination),
            "--source-map-sha256", digest], stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=65,
            creationflags=subprocess.CREATE_NO_WINDOW)
        need(len(result.stdout) <= MIB and len(result.stderr) <= MIB,
             "ASSEMBLY_CHECK_LOG_BOUND")
        for suffix, contents in (("stdout", result.stdout), ("stderr", result.stderr)):
            with (output/(label+"."+suffix)).open("xb") as stream:
                stream.write(contents)
        row = {"step": label, "exit_code": result.returncode}
        history.append(row)
        return result

    try:
        bad = invoke("wrong-map", negative, "0"*64)
        need(bad.returncode != 0 and not negative.exists(), "ASSEMBLY_CHECK_MAP_REFUSAL")
        expected_refusal = ("NATIVE_ASSEMBLY_INPUT_PIN:"+str(root/PREFIX/"source-map.json")).encode("utf-8")
        need(expected_refusal in bad.stderr,
             "ASSEMBLY_CHECK_EXPECTED_REFUSAL")
        good = invoke("assembly", package, args.source_map_sha256)
        need(good.returncode == 0, "ASSEMBLY_CHECK_POSITIVE_FAILED")
        profile_raw = (package/"PROFILE.json").read_bytes()
        profile_sha = hashlib.sha256(profile_raw).hexdigest()
        profile_source = package/"profile.py"
        loader_raw = profile_source.read_bytes()
        need(hashlib.sha256(loader_raw).hexdigest() == args.profile_source_sha256,
             "ASSEMBLY_CHECK_LOADER_PIN")
        name = "_native_assembly_checked_loader"
        need(name not in sys.modules, "ASSEMBLY_CHECK_PRELOADED")
        spec = importlib.util.spec_from_file_location(name, profile_source)
        module = importlib.util.module_from_spec(spec); sys.modules[name] = module
        exec(compile(loader_raw, str(profile_source), "exec"), module.__dict__)

        def check():
            need(time.monotonic()-started < 105 and time.process_time()-cpu < 55,
                 "ASSEMBLY_CHECK_ORIGINAL_ALLOWANCE")

        support = module.load(package, profile_sha,
            {"python_runtime": Path(args.python_runtime), "lean_runtime": Path(args.lean_runtime)},
            started+105, check_parent=check)
        names = set(support.descriptor["files"])
        need(len(names) == 111 and {n for n in names if n.startswith("reference/")} ==
             {"reference/baseline_bundle.py", "reference/baseline_intake.py"} and
             support.baseline_intake is sys.modules["baseline_intake"] and
             support.baseline_production is sys.modules["baseline_production"],
             "ASSEMBLY_CHECK_SELECTED_ROLES")
        check()
        history.append({"step": "actual-profile-load", "profile_sha256": profile_sha,
                        "profile_files": len(names), "owner_state_opened": False})
        report = {"status": "PASS_FILE_ASSEMBLY_REFUSAL_AND_SUPPORT_LOAD", "steps": history,
                  "wall_seconds": time.monotonic()-started,
                  "harness_cpu_seconds": time.process_time()-cpu,
                  "claim": "NOT_MATHEMATICAL_ACCEPTANCE_OR_GROWTH_MEASUREMENT"}
    except BaseException as error:
        report = {"status": "FAILED", "steps": history, "error_type": type(error).__name__,
                  "error": str(error)[:2000], "retention": "KEEP_ALL_OUTPUT_NO_RETRY"}
        with (output/"CHECK-FAILURE.json").open("x", encoding="utf-8") as stream:
            json.dump(report, stream, sort_keys=True, allow_nan=False)
        raise
    with (output/"CHECK.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, allow_nan=False)
    print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)


if __name__ == "__main__":
    main()

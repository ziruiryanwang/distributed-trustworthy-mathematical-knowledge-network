"""Four installed offline lookup controls over one retained real directory.

Source-only until root selects a bounded enclosing Windows Job. Four independent
inert child CLIs may run concurrently. No owner, Lean, network or original
directory mutation; no scan or whole-file hash of ENTRIES.bin/TREE.bin.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time


ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024 ** 2
START = time.monotonic()
STDOUT_CAP, STDERR_CAP = 2 * MIB, 128 * 1024


def need(ok, code):
    if not ok:
        raise AssertionError("DIRECTORY_LOOKUP_CONTROL_" + code)


def check():
    need(time.monotonic() - START < 55, "WALL_ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def compact(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      allow_nan=False, separators=(",", ":")).encode("utf-8")


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and ".." not in path.parts, "ABSOLUTE_PATH")
    for part in (*reversed(path.parents), path):
        if fresh and part == path:
            need(not part.exists() and not part.is_symlink(), "FRESH_OUTPUT")
            continue
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and
             not getattr(info, "st_file_attributes", 0) & 0x400, "REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if part != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PATH_KIND")
    need(path.resolve(strict=not fresh) == path, "CANONICAL_PATH")
    return path


def read(path, cap, *, empty=False):
    check()
    path = ordinary(path)
    size = path.stat().st_size
    need((empty or size > 0) and size <= cap, "READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(cap + 1)
    need(len(raw) == size, "READ_CHANGED")
    return raw


def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "JSON_DUPLICATE")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs)


def changed(pin):
    need(type(pin) is str and len(pin) == 64 and
         all(c in "0123456789abcdef" for c in pin), "PIN_FORMAT")
    return ("1" if pin[0] == "0" else "0") + pin[1:]


def selected_file(path, expected, cap, pins):
    raw = read(path, cap)
    need(sha(raw) == expected, "INPUT_PIN:" + str(path))
    pins[str(path)] = {"sha256": expected, "bytes": len(raw), "cap": cap}
    return raw


def main():
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "CANONICAL_ISOLATED_WINDOWS")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for flag in ("package", "profile-sha256", "directory", "directory-sha256",
                 "symbol-names", "symbol-names-sha256", "expected-report",
                 "expected-report-sha256", "checks-sha256", "output"):
        parser.add_argument("--" + flag, required=True)
    args = parser.parse_args()
    package = ordinary(args.package, directory=True)
    directory = ordinary(args.directory, directory=True)
    names_path = ordinary(args.symbol_names)
    prior_path = ordinary(args.expected_report)
    output = ordinary(args.output, directory=True, fresh=True)
    need(output.is_relative_to(ROOT / "experiments/v5-local-checks"), "OUTPUT_SCOPE")
    for path in (package, directory, names_path, prior_path):
        need(not output.is_relative_to(path) and not path.is_relative_to(output), "OVERLAP")

    pins = {}
    selected_file(Path(__file__).absolute(), args.checks_sha256, MIB, pins)
    profile_raw = selected_file(package / "PROFILE.json", args.profile_sha256, 2*MIB, pins)
    profile = strict(profile_raw)
    need(type(profile) is dict and profile.get("schema") == "DMKN_ORDINARY_OWNER_PROFILE_V1"
         and type(profile.get("files")) is dict, "PROFILE")
    # PROFILE lists auxiliary files; its pinned INSTALLATION lists the two
    # imported core codecs. Read only that small manifest, not native artifacts.
    installation_raw = selected_file(package / "installation/INSTALLATION.json",
        profile.get("installation_manifest_sha256"), 2*MIB, pins)
    installation = strict(installation_raw)
    need(type(installation) is dict and
         installation.get("schema") == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1" and
         type(installation.get("roles")) is dict and
         type(installation.get("files")) is dict, "INSTALLATION")
    selected_sources = [
        (relative, profile["files"].get(relative)) for relative in (
            "lookup_directory.py", "directory_index.py",
            "support/discovery/formal_features.py",
            "support/discovery/authenticated_index.py")]
    for role, relative in (("evidence", "py/ordinary_evidence.py"),
                           ("semantics", "py/ordinary_semantics.py")):
        need(installation["roles"].get(role) == relative, "CORE_SOURCE_ROLE")
        selected_sources.append(("installation/" + relative,
                                 installation["files"].get(relative)))
    for relative, pin in selected_sources:
        need(type(pin) is dict and set(pin) == {"bytes", "sha256"}, "SOURCE_ROLE")
        raw = selected_file(package / relative, pin["sha256"], 2*MIB, pins)
        need(type(pin["bytes"]) is int and len(raw) == pin["bytes"], "SOURCE_SIZE")
    manifest_raw = selected_file(directory / "DIRECTORY.json", args.directory_sha256, 8192, pins)
    names_raw = selected_file(names_path, args.symbol_names_sha256, 65536, pins)
    prior_raw = selected_file(prior_path, args.expected_report_sha256, 2*MIB, pins)
    manifest, names, prior = map(strict, (manifest_raw, names_raw, prior_raw))
    need(type(names) is list and 1 <= len(names) <= 8, "NAME_COUNT")
    need(type(prior) is dict and prior.get("ok") is True and
         prior.get("query_kind") == "symbol-neighborhood" and
         prior.get("names_sha256") == sha(names_raw) and
         type(prior.get("specs")) is list and len(prior["specs"]) == len(names),
         "PRIOR_QUERY_COMPARATOR")
    need(type(manifest) is dict and type(manifest.get("metadata")) is dict,
         "DIRECTORY_MANIFEST")
    # Record only fixed-file metadata, never read/hash the binary directory.
    data_sizes = {name: ordinary(directory / name).stat().st_size
                  for name in ("ENTRIES.bin", "TREE.bin")}

    output.mkdir()
    missing_name = [[0, {"$bytes": list(b"DirectoryLookupNegative")}],
                    [0, {"$bytes": list(sha(str(output).encode("utf-8") + manifest_raw).encode("ascii"))}]]
    need(missing_name not in names, "NEGATIVE_NAME_DUPLICATE")
    mixed_names = [names[0], missing_name]
    mixed_path = output / "mixed-names.json"
    mixed_raw = compact(mixed_names)
    with mixed_path.open("xb") as stream:
        need(stream.write(mixed_raw) == len(mixed_raw), "MIXED_WRITE")
    pins[str(mixed_path)] = {"sha256": sha(mixed_raw), "bytes": len(mixed_raw), "cap": 65536}
    cases = [
        ("positive", names_path, args.profile_sha256, args.directory_sha256, None),
        ("mixed-missing", mixed_path, args.profile_sha256, args.directory_sha256, None),
        ("wrong-manifest", names_path, args.profile_sha256, changed(args.directory_sha256), "DIRECTORY_MANIFEST_PIN"),
        ("wrong-profile", names_path, changed(args.profile_sha256), args.directory_sha256, "DIRECTORY_LOOKUP_PROFILE_PIN"),
    ]
    running, opened = [], []
    try:
        for label, query_path, profile_pin, directory_pin, expected_error in cases:
            check()
            stdout_path, stderr_path = output / (label + ".stdout"), output / (label + ".stderr")
            stdout, stderr = stdout_path.open("xb"), stderr_path.open("xb")
            opened.extend((stdout, stderr))
            target = output / (label + "-result")
            argv = [sys.executable, "-I", "-S", "-B", str(package / "lookup_directory.py"),
                    "--profile-sha256", profile_pin, "--directory", str(directory),
                    "--directory-sha256", directory_pin, "--symbol-names", str(query_path),
                    "--output", str(target)]
            proc = subprocess.Popen(argv, cwd=ROOT, stdin=subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
            running.append({"label": label, "process": proc, "argv": argv,
                            "stdout": stdout_path, "stderr": stderr_path,
                            "target": target, "expected_error": expected_error})
        need(len(running) == 4, "CHILD_COUNT")
        while any(row["process"].poll() is None for row in running):
            check()
            for row in running:
                need(row["stdout"].stat().st_size <= STDOUT_CAP and
                     row["stderr"].stat().st_size <= STDERR_CAP, "CHILD_OUTPUT_BOUND")
            time.sleep(0.05)
        for row in running:
            row["returncode"] = row["process"].wait(timeout=1)
    finally:
        cleanup = []
        for row in running:
            proc = row["process"]
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    cleanup.append(row["label"])
        for stream in opened:
            stream.close()
        need(not cleanup, "CHILD_CLEANUP:" + ",".join(cleanup))

    results = []
    for row in running:
        out = read(row["stdout"], STDOUT_CAP, empty=True)
        err = read(row["stderr"], STDERR_CAP, empty=True)
        if row["expected_error"] is not None:
            need(row["returncode"] != 0 and not out and not row["target"].exists() and
                 ("ValueError: " + row["expected_error"]).encode("ascii") in err,
                 "EXPECTED_REFUSAL:" + row["label"])
            record = {"case": row["label"], "status": "EXPECTED_REFUSAL",
                      "error": row["expected_error"], "returncode": row["returncode"]}
        else:
            need(row["returncode"] == 0 and not err, "CLEAN_CHILD:" + row["label"])
            saved_raw = read(row["target"] / "RESULT.json", MIB)
            result = strict(saved_raw)
            need(result == strict(out) and result["metadata"] == manifest["metadata"] and
                 result["directory_manifest_sha256"] == args.directory_sha256 and
                 result["profile_sha256"] == args.profile_sha256 and
                 result["mathematical_acceptance"] is False and
                 result["owner_opened"] is False and
                 result["coverage"] == "SELECTED_HISTORICAL_DIRECTORY_ONLY",
                 "RESULT_SCOPE:" + row["label"])
            if row["label"] == "positive":
                need(result["status"] == "DIRECTORY_QUERY_READY" and
                     result["missing_names"] == [] and result["specs"] == prior["specs"] and
                     [binding[0] for binding in result["bindings"]] == names and
                     strict(read(row["target"] / "SPECS.json", 65536)) == prior["specs"],
                     "POSITIVE_SPECS")
            else:
                need(result["status"] == "DIRECTORY_NAMES_MISSING" and
                     result["missing_names"] == [missing_name] and
                     result["bindings"] == [[names[0], prior["specs"][0]["symbol"]["symbol_id"]]] and
                     "specs" not in result and not (row["target"] / "SPECS.json").exists(),
                     "MIXED_NO_PARTIAL_QUERY")
            record = {"case": row["label"], "status": result["status"],
                      "result_sha256": sha(saved_raw), "io": result["io"],
                      "returncode": row["returncode"]}
        results.append({**record, "argv": row["argv"],
                        "stdout_sha256": sha(out), "stderr_sha256": sha(err)})

    for path, pin in pins.items():
        raw = read(path, pin["cap"])
        need(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"], "SELECTED_INPUT_CHANGED")
    need({name: ordinary(directory / name).stat().st_size for name in data_sizes} == data_sizes,
         "DIRECTORY_FILE_SIZE_CHANGED")
    check()
    result = {"status": "PASS_INSTALLED_OFFLINE_LOOKUP", "groups": 4,
              "cases": results, "input_pins": pins, "directory_file_sizes": data_sizes,
              "source_profile_sha256": manifest["metadata"]["source_profile_sha256"],
              "current_profile_sha256": args.profile_sha256,
              "mathematical_acceptance": False, "owner_calls": 0,
              "native_calls": 0, "network_calls": 0,
              "scope": "REAL_HISTORICAL_DIRECTORY_FOUR_INERT_INSTALLED_CLIS_NO_BINARY_SCAN",
              "wall_seconds": time.monotonic()-START}
    raw = compact(result)
    need(len(raw) <= MIB, "REPORT_BOUND")
    with (output / "RESULT.json").open("xb") as stream:
        need(stream.write(raw) == len(raw), "RESULT_WRITE")
    print(raw.decode("utf-8"), flush=True)


if __name__ == "__main__":
    main()

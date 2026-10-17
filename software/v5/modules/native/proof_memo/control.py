"""One serde-only syntax build/control run inside the selected outer Job.

Reuse the adopted compile argv and dependencies, not its old workload. No Cargo,
kernel, module/aggregate build, guest execution or proof production. The outer
Run-V5-Check owns inclusive CPU/memory/process/time bounds and exact-file pins.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
RUN = HERE / "proof-memo-controls-01"
PRIOR = HERE / "proof-validation-controls-01"
COMMAND_SHA = "6c4c3767f45a4a7f44410ade8880d76bbba24bf6ecbddfbe3ea8f4a1aec28244"
ENVIRONMENT_SHA = "34525808d26848e9582ad5ada38ff66fae2205f79ae0421a33f72fbd67af4e18"


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load(path, expected):
    need(path.stat().st_size <= 1024**2 and digest(path) == expected, "EXACT_SMALL_RECORD")
    return json.loads(path.read_bytes())


def save(path, value):
    raw = (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    need(len(raw) <= 1024**2, "RECORD_SIZE")
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def main():
    source = Path(__file__).resolve(strict=True)
    snapshot = RUN / "sources"
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize
         and source == snapshot / "software/v5/modules/native/proof_memo/control.py"
         and len(sys.argv) == 3, "SELECTED_SNAPSHOT_ONLY")
    config = load(Path(sys.argv[1]), sys.argv[2])
    need(set(config) == {"schema", "tests", "wire"}
         and config["schema"] == "DMKN_PROOF_MEMO_CONTROLS_V1", "CONFIG_SCHEMA")
    tests = config["tests"]
    need(type(tests) is list and 1 <= len(tests) <= 32 and len(set(tests)) == len(tests)
         and all(type(name) is str and re.fullmatch(r"[a-z0-9_]+", name) for name in tests),
         "EXACT_TEST_GROUPS")
    wire = Path(config["wire"])
    need(wire == HERE / "bounded-parse-aggregate-snapshot-01/evidence/wire.bin"
         and wire.stat().st_size <= 16 * 1024**2, "RETAINED_WIRE")
    old_commands = load(PRIOR / "compile-and-test-commands.json", COMMAND_SHA)
    profile = load(PRIOR / "environment-profile.json", ENVIRONMENT_SHA)
    need(len(old_commands) == 2 and old_commands[0][0] == "serde-compile", "OLD_COMMAND_PAIR")
    command = list(old_commands[0][1])
    need(command.count("--extern") == 2 and command.count("--test") == 1
         and command.count("-o") == 1 and command.count("--crate-name") == 1,
         "SERDE_ONLY_COMMAND")
    work = RUN / "syntax"
    need(not work.exists(), "FRESH_SYNTAX_OUTPUT")
    work.mkdir()
    binary = work / "proof_memo_tests.exe"
    replacements = {
        "dmkn_proof_validation_controls": "dmkn_proof_memo_controls",
        str(PRIOR / "source/software/v5/modules/native/proof_validation/control_root.rs"):
            str(snapshot / "software/v5/modules/native/proof_memo/control_root.rs"),
        str(PRIOR / "proof_validation_tests.exe"): str(binary),
    }
    for before, after in replacements.items():
        need(command.count(before) == 1, "EXACT_RECIPE_SUBSTITUTION")
        command[command.index(before)] = after
    need(command[command.index("-o") + 1] == str(binary), "EXACT_OUTPUT")
    host_tools = {Path(row["path"]).name: Path(row["path"]) for row in profile["host_binaries"]}
    for row in profile["host_binaries"]:
        path = Path(row["path"])
        need(path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], "HOST_TOOL_PIN")
    temporary = work / "temp"
    temporary.mkdir()
    # Explicit allowlist, no inherited compiler/language/search options or secrets.
    environment = {key: os.environ[key] for key in
                   ("SystemRoot", "WINDIR", "ComSpec", "USERPROFILE", "APPDATA", "LOCALAPPDATA")
                   if key in os.environ}
    need("SystemRoot" in environment, "OS_ROOT")
    environment.update({
        "PATH": os.pathsep.join(str(path) for path in
            (Path(command[0]).parent, host_tools["link.exe"].parent,
             host_tools["rc.exe"].parent, Path(environment["SystemRoot"]) / "System32")),
        "LIB": os.pathsep.join(profile["library_directories"]),
        "INCLUDE": os.pathsep.join(profile["include_directories"]),
        "TEMP": str(temporary), "TMP": str(temporary),
        "VCToolsUserTelemetryOptOut": "1", "DMKN_PROOF_MEMO_WIRE": str(wire),
    })
    test_command = [str(binary), "--test-threads=1", "--nocapture"]
    report = {"schema": "DMKN_PROOF_MEMO_CONTROLS_RESULT_V1", "status": "FAIL",
              "commands": [command, test_command], "test_groups": tests,
              "guest_calls": 0, "proof_calls": 0, "kernel_calls": 0,
              "dependency_rebuilds": 0, "environment_keys": sorted(environment),
              "authority": "SYNTAX_DIFFERENTIAL_NOT_MATHEMATICAL_ADMISSION"}
    save(work / "COMMANDS.json", report)
    try:
        for name, argv in (("compile", command), ("controls", test_command)):
            # Descendants inherit the root-owned Windows Job; no breakaway flag.
            log = work / (name + ".log")
            with log.open("xb") as stream:
                child = subprocess.run(argv, cwd=ROOT, env=environment, stdin=subprocess.DEVNULL,
                    stdout=stream, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW,
                    timeout=100)
            need(log.stat().st_size <= 2 * 1024**2, "BOUNDED_LOG")
            need(child.returncode == 0, "COMMAND_FAILED:" + name)
            if name == "compile":
                need(binary.stat().st_size <= 64 * 1024**2, "BINARY_SIZE")
                report["binary"] = {"path": str(binary), "bytes": binary.stat().st_size,
                                    "sha256": digest(binary)}
        output = (work / "controls.log").read_text(encoding="utf-8")
        # nocapture may insert test-owned metric text before the final 'ok'.
        found = re.findall(r"^test module_correspondence::correspondence_controls::([a-z0-9_]+) ",
                           output, re.MULTILINE)
        need(len(found) == len(tests) and set(found) == set(tests)
             and f"test result: ok. {len(tests)} passed; 0 failed; 0 ignored; 0 measured; 0 filtered out;" in output,
             "EXACT_ALL_CONTROLS_PASSED")
        need(digest(binary) == report["binary"]["sha256"], "BINARY_CHANGED")
        report["status"] = "PASS_MEMO_SYNTAX_CONTROLS_ONLY"
    except Exception as error:
        report["error"] = type(error).__name__ + ": " + str(error)[:3000]
    save(work / "RESULT.json", report)
    print(json.dumps({"status": report["status"], "result": str(work / "RESULT.json")}))
    return 0 if report["status"] == "PASS_MEMO_SYNTAX_CONTROLS_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())

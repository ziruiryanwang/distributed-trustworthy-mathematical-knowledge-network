"""One owner-selected Lean authoring call inside an existing supervised Job.

This is not a standalone resource allocator, sandbox or remote command endpoint.
Only the trusted owner supplies this configuration. No caller argv/environment,
network, retries, proof verification or process-local module handles are exposed.
Native stdout/stderr remain inherited so the outer supervisor preserves partial
diagnostics and enforces its sampled log caps. It alone verifies whole-Job closure.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import time

SCHEMA = "DMKN_OWNER_LEAN_WORKER_V1"
RESULT_SCHEMA = "DMKN_OWNER_LEAN_WORKER_RESULT_V1"
MAX_CONFIG = 128*1024
MAX_EXPORT = 16*1024**2
REQUIRED_DLLS = {"libInit_shared.dll", "libleanshared.dll", "libleanshared_1.dll",
                 "libleanshared_2.dll", "libc++.dll"}
CONFIG_FIELDS = {"schema", "worker", "executable", "lean_root", "runtime_pins", "request",
                 "output_directory", "report_path", "deadline_monotonic"}


def require(ok, why):
    if not ok: raise ValueError(why)


def digest(value):
    require(type(value) is str and len(value) == 64
            and all(c in "0123456789abcdef" for c in value), "WORKER_DIGEST")
    return value


def absolute(value):
    require(type(value) is str and 0 < len(value) <= 4096 and "\0" not in value, "WORKER_PATH")
    path = Path(value)
    require(path.is_absolute() and path.resolve() == path, "WORKER_ABSOLUTE_CANONICAL_PATH")
    return path


def live(deadline):
    require(time.monotonic() < deadline, "WORKER_ORIGINAL_DEADLINE")


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "WORKER_DUPLICATE_KEY")
            result[key] = value
        return result

    def bad_constant(value): raise ValueError("WORKER_NONFINITE_JSON:"+value)

    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=bad_constant)


def pin_shape(item, maximum):
    require(type(item) is dict and set(item) == {"path", "bytes", "sha256"}, "WORKER_PIN_FIELDS")
    path = absolute(item["path"])
    require(type(item["bytes"]) is int and 0 < item["bytes"] <= maximum, "WORKER_PIN_SIZE")
    digest(item["sha256"])
    return path


def verify_pin(item, maximum, deadline):
    path = pin_shape(item, maximum)
    live(deadline)
    require(path.is_file() and path.stat().st_size == item["bytes"], "WORKER_FILE_SIZE")
    hashed, count = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024**2):
            count += len(chunk)
            require(count <= item["bytes"], "WORKER_FILE_GREW")
            hashed.update(chunk)
            live(deadline)
    require(count == item["bytes"] and path.stat().st_size == count
            and hashed.hexdigest() == item["sha256"], "WORKER_FILE_PIN")
    live(deadline)


def parse_configuration(raw, *, worker_path):
    require(type(raw) is bytes and 0 < len(raw) <= MAX_CONFIG, "WORKER_CONFIG_BYTES")
    config = strict_json(raw)
    require(type(config) is dict and set(config) == CONFIG_FIELDS and config["schema"] == SCHEMA,
            "WORKER_CONFIG_FIELDS")
    deadline = config["deadline_monotonic"]
    require(type(deadline) in (int, float) and math.isfinite(deadline)
            and 0 < deadline-time.monotonic() <= 600, "WORKER_FINITE_EFFECTIVE_DEADLINE")
    selected_worker = pin_shape(config["worker"], 2*1024**2)
    require(selected_worker == worker_path.resolve(), "WORKER_SELF_SELECTION")
    executable = pin_shape(config["executable"], 64*1024**2)
    require(executable.suffix.lower() == ".exe", "WORKER_NATIVE_EXECUTABLE")
    request = pin_shape(config["request"], 16*1024**2)
    root = absolute(config["lean_root"])
    require(root.is_dir() and (root/"bin").is_dir() and (root/"lib/lean").is_dir(), "WORKER_LEAN_ROOT")
    runtime = config["runtime_pins"]
    require(type(runtime) is list and 1 <= len(runtime) <= 128, "WORKER_RUNTIME_COUNT")
    seen, total = set(), 0
    for item in runtime:
        path = pin_shape(item, 512*1024**2)
        require(path.is_relative_to(root) and path not in seen, "WORKER_RUNTIME_OWNER_OR_DUPLICATE")
        seen.add(path); total += item["bytes"]
    require(total <= 2*1024**3 and {root/"bin"/name for name in REQUIRED_DLLS} <= seen,
            "WORKER_RUNTIME_REQUIRED_PINS")
    output, report = absolute(config["output_directory"]), absolute(config["report_path"])
    require(output.parent == report.parent and output.parent.is_dir()
            and output != report and not output.exists() and not report.exists(), "WORKER_FRESH_OUTPUT_AND_REPORT")
    require(output not in {selected_worker, executable, request} and
            report not in {selected_worker, executable, request}, "WORKER_OUTPUT_INPUT_OVERLAP")
    live(deadline)
    return config


def environment(root):
    """Operation-local adopted Lean lookup; never arbitrary forwarded settings."""
    selected = {key: value for key, value in os.environ.items()
                if not key.upper().startswith("LEAN_") and key.upper() not in
                {"CPATH", "C_INCLUDE_PATH", "CPLUS_INCLUDE_PATH", "LIBRARY_PATH", "CC", "CFLAGS", "LDFLAGS"}}
    selected["LEAN_SYSROOT"] = str(root)
    selected["PATH"] = str(root/"bin") + os.pathsep + os.environ.get("PATH", "")
    return selected


def write_report(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    require(len(raw) <= 1024**2, "WORKER_REPORT_BYTE_LIMIT")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def run(config_path, config_sha256):
    """No resource allowance is created here; the caller must own an outer Job."""
    config_path = absolute(str(config_path)); digest(config_sha256)
    require(config_path.is_file() and 0 < config_path.stat().st_size <= MAX_CONFIG, "WORKER_CONFIG_FILE")
    with config_path.open("rb") as stream: raw = stream.read(MAX_CONFIG+1)
    require(len(raw) <= MAX_CONFIG and hashlib.sha256(raw).hexdigest() == config_sha256, "WORKER_CONFIG_PIN")
    config = parse_configuration(raw, worker_path=Path(__file__))
    deadline = config["deadline_monotonic"]
    output, report_path = absolute(config["output_directory"]), absolute(config["report_path"])
    require(config_path != report_path and not config_path.is_relative_to(output), "WORKER_CONFIG_OUTPUT_OVERLAP")
    report = {"schema": RESULT_SCHEMA, "status": "FAIL", "mathematical_acceptance": False,
              "config_sha256": config_sha256, "request_sha256": config["request"]["sha256"],
              "executable_sha256": config["executable"]["sha256"], "worker_sha256": config["worker"]["sha256"],
              "deadline_monotonic": deadline, "native_return_code": None, "native_timed_out": False,
              "direct_child_reaped": False, "export_sha256": None, "export_bytes": None,
              "outer_job_closure_required": True, "native_logs": "INHERITED_OUTER_SUPERVISOR",
              "runtime_scope": "EXPLICIT_OWNER_PINS_NOT_HERMETIC_OR_SANDBOX"}
    child = None
    started = time.monotonic()

    def rebind():
        for item, maximum in ((config["worker"], 2*1024**2), (config["executable"], 64*1024**2),
                              (config["request"], 16*1024**2)):
            verify_pin(item, maximum, deadline)
        for item in config["runtime_pins"]: verify_pin(item, 512*1024**2, deadline)
        require(config_path.stat().st_size == len(raw) and config_path.read_bytes() == raw, "WORKER_CONFIG_CHANGED")
        live(deadline)

    try:
        rebind()
        require(not output.exists() and not report_path.exists(), "WORKER_OUTPUT_BECAME_OCCUPIED")
        live(deadline)
        # stdout/stderr intentionally inherited, never PIPE/capture_output: the
        # outer bounded Job owns their persistent logs, including partial output.
        child = subprocess.Popen([config["executable"]["path"], config["request"]["path"], str(output)],
                                 cwd=str(output.parent), stdin=subprocess.DEVNULL,
                                 env=environment(absolute(config["lean_root"])))
        try:
            remaining = deadline-time.monotonic()
            if remaining <= 0: raise subprocess.TimeoutExpired(child.args, 0)
            report["native_return_code"] = child.wait(timeout=remaining)
            report["direct_child_reaped"] = True
        except subprocess.TimeoutExpired:
            report["native_timed_out"] = True
            child.kill()
            report["native_return_code"] = child.wait(timeout=5)
            report["direct_child_reaped"] = True
            raise ValueError("WORKER_NATIVE_DEADLINE")
        require(report["native_return_code"] == 0, "WORKER_NATIVE_REFUSED")
        live(deadline)
        export = output/"EXPORT.json"
        require(export.resolve() == export and export.is_file() and 0 < export.stat().st_size <= MAX_EXPORT,
                "WORKER_EXPORT_FILE_BOUND")
        with export.open("rb") as stream: export_raw = stream.read(MAX_EXPORT+1)
        require(0 < len(export_raw) <= MAX_EXPORT and export.stat().st_size == len(export_raw), "WORKER_EXPORT_BYTES")
        rebind()
        report.update(status="PASS_NATIVE_EXPORT_ONLY", export_sha256=hashlib.sha256(export_raw).hexdigest(),
                      export_bytes=len(export_raw))
        live(deadline)
    except BaseException as error:
        report["status"] = "FAIL"
        report["error"] = str(error)[:4096]
    finally:
        if child is not None and not report["direct_child_reaped"]:
            try:
                if child.poll() is None: child.kill()
                report["native_return_code"] = child.wait(timeout=5)
                report["direct_child_reaped"] = True
            except BaseException as error:
                report["status"] = "FAIL"
                report["cleanup_error"] = str(error)[:4096]
        report["wall_seconds"] = time.monotonic()-started
        # Retain failure reports even after expiry. This grants no renewed work
        # budget; the outer original Job/deadline may terminate cleanup too.
        write_report(report_path, report)
    return report


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--config", required=True)
    parser.add_argument("--config-sha256", required=True)
    args = parser.parse_args()
    try:
        require(os.name == "nt" and sys.flags.isolated and sys.flags.no_site
                and sys.dont_write_bytecode and not sys.flags.optimize, "WORKER_ISOLATED_WINDOWS_INVOCATION")
        report = run(args.config, args.config_sha256)
        return 0 if report["status"] == "PASS_NATIVE_EXPORT_ONLY" else 1
    except BaseException as error:
        print(json.dumps({"schema": RESULT_SCHEMA, "status": "WORKER_INPUT_OR_REPORT_REFUSED",
                          "error": str(error)[:4096], "mathematical_acceptance": False}), file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__": raise SystemExit(main())

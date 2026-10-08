"""One separately pinned context-contract allocation; old cuts are not rerun."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time

INSTALL = Path(__file__).resolve().parents[1]
SOURCES = ("tests/run_context_contract.py", "tests/context_contract_worker.py",
           "tests/test_context_selection.py", "manage.py", "build.py", "py/node.py",
           "py/storage.py", "py/domains.py", "py/run_stage.py", "py/supervise.py",
           "py/peer_node.py", "py/peer_wire.py", "py/peer_service.py", "py/checking.py")
LIMITS = {"wall_seconds": 60, "cpu_seconds": 30, "memory_mib": 512,
          "active_processes": 8, "stdout_bytes": 65536,
          "stderr_bytes": 65536, "event_bytes": 65536}
RETAINED = {"files": 4096, "entries": 8192, "bytes": 64 * 1048576}


def pin(path):
    path = Path(path).resolve(strict=True)
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink() or getattr(ancestor.lstat(), "st_file_attributes", 0) & 0x400:
            raise RuntimeError("REPARSE_POINT")
    if not path.is_file() or path.stat().st_size > 16 * 1048576:
        raise RuntimeError("PIN_SIZE")
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def save(path, value):
    raw = encoded(value)
    if len(raw) > 1048576:
        raise RuntimeError("RECORD_SIZE")
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def census(roots):
    """Post-quiescence endpoint accounting, not a hard transient disk quota."""
    rows, entries, total = [], 0, 0
    pending = list(roots)
    while pending:
        directory = pending.pop()
        for path in directory.iterdir():
            entries += 1
            if entries > RETAINED["entries"]:
                raise RuntimeError("RETAINED_ENTRY_LIMIT")
            if path.is_symlink() or getattr(path.lstat(), "st_file_attributes", 0) & 0x400:
                raise RuntimeError("RETAINED_REPARSE_POINT")
            if path.is_dir():
                pending.append(path)
            elif path.is_file():
                total += path.stat().st_size
                if len(rows) >= RETAINED["files"] or total > RETAINED["bytes"]:
                    raise RuntimeError("RETAINED_FILE_BYTE_LIMIT")
                rows.append(pin(path))
            else:
                raise RuntimeError("RETAINED_NONREGULAR_FILE")
    return {"entries": entries, "files": sorted(rows, key=lambda row: row["path"]),
            "bytes": total, "bounds": RETAINED,
            "endpoint": "after worker quiescence; before census and result files"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", required=True, type=Path)
    args = parser.parse_args()
    if not (sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_site and sys.flags.no_user_site and os.name == "nt"):
        raise RuntimeError("WINDOWS_STARTUP_PROFILE")
    if not args.launch.is_absolute() or args.launch.stat().st_size > 65536:
        raise RuntimeError("LAUNCH_BOUND")
    launch = json.loads(args.launch.read_bytes())
    if (set(launch) != {"schema", "tests", "pins", "limits", "retained"} or type(launch["schema"]) is not int
            or launch["schema"] != 1 or type(launch["tests"]) is not int
            or not 1 <= launch["tests"] <= 64 or encoded(launch["limits"]) != encoded(LIMITS)
            or encoded(launch["retained"]) != encoded(RETAINED)):
        raise RuntimeError("LAUNCH_FIELDS")
    pins = [pin(sys.executable), *[pin(INSTALL / name) for name in SOURCES]]
    if encoded(launch["pins"]) != encoded(pins):
        raise RuntimeError("EXACT_SOURCE_PINS")
    root = INSTALL / "qualification/context-contract-01"
    state = INSTALL.parent / "product-local/context-contract-01"
    if root.exists() or state.exists():
        raise RuntimeError("EXCLUSIVE_NEW_ROOTS_REQUIRED")
    sys.path.insert(0, str(INSTALL / "py"))
    import run_stage
    import supervise
    root.mkdir(exist_ok=False)
    state.mkdir(exist_ok=False)
    # Preserve the executed development cut without requiring mutable source
    # paths to remain unchanged forever. No product execution uses these copies.
    for name, expected in zip(SOURCES, pins[1:]):
        source = INSTALL / name
        raw = source.read_bytes()
        if pin(source) != expected or hashlib.sha256(raw).hexdigest() != expected["sha256"]:
            raise RuntimeError("SOURCE_CHANGED_BEFORE_SNAPSHOT")
        target = root / "sources" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(raw)
    cases = root / "cases"
    cases.mkdir()
    config = root / "config.json"
    save(config, {"schema": 1, "tests": launch["tests"], "state": str(state)})
    limits = dict(LIMITS, pins=[*pins, pin(config)])
    save(root / "launch.json", {"selected_launch": pin(args.launch), "pins": pins, "limits": limits})
    started = time.monotonic()
    result = {"status": "RUNNING", "native_stages": 0, "cpu_complete": False,
              "scope": "synthetic metadata contract controls, no native acceptance",
              "containment": "worker Windows Job; trusted coordinator outside it",
              "unmetered_cpu": "coordinator/interpreter startup outside worker Job"}
    response = None
    try:
        transport = supervise.Transport(sys.executable, INSTALL / "tests/context_contract_worker.py",
                                        config, state, cases, run_stage, limits)
        response = transport("all-tests", b'{"op":"test-context-contract"}\n')
    except BaseException as error:
        result.update(status="FAILED", error=type(error).__name__, detail=str(error)[:1024])
    # Retain actual worker cost/cleanup before interpreting success or test count.
    receipt_path = cases / "all-tests/supervisor.json"
    try:
        receipt = json.loads(receipt_path.read_bytes())
        result["supervisor"] = pin(receipt_path)
        result["observed_job_cpu_seconds"] = receipt.get("final_job", {}).get("cpu_seconds")
        result["cleanup_observation"] = {key: receipt.get(key) for key in
            ("direct_child_reaped", "final_active_zero", "job_closed", "cleanup_errors")}
        if response is not None:
            outcome = json.loads(response["stdout"])
            result["outcome"] = outcome
            if (response["returncode"] != 0 or outcome["status"] != "PASS"
                    or outcome["tests"] != launch["tests"] or outcome["skipped"] != 0):
                raise RuntimeError("CONTEXT_CONTRACT_TESTS_FAILED")
            result["status"] = "PASS_PENDING_OUTCOME_REVIEW"
    except BaseException as error:
        result.update(status="FAILED", observation_error=type(error).__name__ + ":" + str(error)[:1024])
    try:
        if not (receipt.get("direct_child_reaped") is True and receipt.get("final_active_zero") is True
                and receipt.get("job_closed") is True and not receipt.get("cleanup_errors")):
            raise RuntimeError("CENSUS_REQUIRES_WORKER_QUIESCENCE")
        retained = census((state, root))
        save(root / "census.json", retained)
        result["census"] = pin(root / "census.json")
        result["retained_files_before_final_records"] = len(retained["files"])
        result["retained_bytes_before_final_records"] = retained["bytes"]
        # Charge both prospective final records as well as all observed files.
        if (retained["bytes"] + result["census"]["bytes"] + len(encoded(result)) + 4096 > RETAINED["bytes"]
                or len(retained["files"]) + 2 > RETAINED["files"]
                or retained["entries"] + 2 > RETAINED["entries"]):
            raise RuntimeError("FINAL_RETAINED_LIMIT")
    except BaseException as error:
        result.update(status="FAILED", census_error=type(error).__name__ + ":" + str(error)[:1024])
    result["elapsed_seconds"] = time.monotonic() - started
    save(root / "result.json", result)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS_PENDING_OUTCOME_REVIEW" else 1


if __name__ == "__main__":
    raise SystemExit(main())

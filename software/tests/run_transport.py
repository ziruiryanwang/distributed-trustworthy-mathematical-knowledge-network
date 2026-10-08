"""Once-only native-free product transport qualification, retaining all artifacts."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import time

INSTALL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(INSTALL / "py"))
import run_stage
import supervise


def pin(path):
    path = Path(path).resolve(strict=True)
    with path.open("rb") as stream:
        raw = stream.read(16*1048576+1)
    if len(raw) > 16*1048576:
        raise RuntimeError("PIN_SIZE")
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def save(path, value):
    with path.open("xb") as stream:
        stream.write((json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"transport-[0-9]{2}", args.run):
        raise RuntimeError("RUN_NAME")
    if not (sys.dont_write_bytecode and sys.flags.ignore_environment and sys.flags.no_site and sys.flags.no_user_site):
        raise RuntimeError("PYTHON_STARTUP_PROFILE")
    root = INSTALL / "qualification" / args.run
    root.mkdir(parents=True, exist_ok=False)
    cases, fixtures = root / "cases", root / "fixtures"
    cases.mkdir()
    fixtures.mkdir()
    config = root / "config.json"
    save(config, {"schema": 1, "tests": 18, "state": str(fixtures)})
    names = ["tests/transport_worker.py", "tests/run_transport.py", "tests/test_peer_wire.py",
             "py/peer_wire.py", "py/peer_service.py", "py/run_stage.py", "py/domains.py", "py/supervise.py"]
    pins = [pin(sys.executable), pin(config), *[pin(INSTALL / name) for name in names]]
    limits = {"pins": pins, "wall_seconds": 60, "cpu_seconds": 60, "memory_mib": 512,
              "active_processes": 8, "stdout_bytes": 65536, "stderr_bytes": 65536, "event_bytes": 65536}
    save(root / "launch.json", {"pins": pins, "limits": limits, "native_stages": 0})
    started = time.monotonic()
    try:
        transport = supervise.Transport(sys.executable, INSTALL / "tests/transport_worker.py", config,
                                         fixtures, cases, run_stage, limits)
        reply = transport("all-tests", b'{"op":"test-transport"}\n')
        outcome = json.loads(reply["stdout"])
        if reply["returncode"] != 0 or outcome["status"] != "PASS" or outcome["tests"] != 18 or outcome["skipped"] != 0:
            raise RuntimeError("TRANSPORT_TESTS_FAILED")
        result = {"status": "PASS_PENDING_OUTCOME_REVIEW", "outcome": outcome,
                  "elapsed_seconds": time.monotonic()-started, "native_stages": 0}
    except BaseException as error:
        result = {"status": "FAILED", "error": type(error).__name__, "detail": str(error)[:2048],
                  "elapsed_seconds": time.monotonic()-started, "native_stages": 0}
    save(root / "result.json", result)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS_PENDING_OUTCOME_REVIEW" else 1


if __name__ == "__main__":
    raise SystemExit(main())

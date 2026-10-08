"""Small native-free socket smoke using the existing bounded Job supervisor.

Each invocation needs a fresh name; fixtures, source snapshots and failures stay.
The worker selects three tests, never a mathematical checking workflow.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import unittest

import run_transport as R

INSTALL = Path(__file__).resolve().parents[1]
COUNT = 3
SCOPE = "synthetic packages, real child-process loopback and faults; no mathematical acceptance"
REQUEST = b'{"op":"easy-network-smoke"}\n'


def worker():
    parser = argparse.ArgumentParser()
    for name in ("config", "state", "request", "event"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    raw = args.request.read_bytes()
    config = json.loads(args.config.read_bytes())
    expected = {"schema": 1, "tests": COUNT, "state": str(args.state.resolve())}
    if raw != REQUEST or config != expected or not args.state.is_absolute() or not args.state.is_dir():
        raise RuntimeError("SMOKE_INPUT_BINDING")
    os.environ["DTMKN_TEST_ROOT"] = str(args.state.resolve())
    suite = unittest.defaultTestLoader.discover(str(INSTALL / "tests"), pattern="test_local_network_smoke.py")
    observed = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    forbidden = [name for name in ("checking", "codec", "source_codec", "sqlite3") if name in sys.modules]
    passed = observed.wasSuccessful() and observed.testsRun == COUNT and not observed.skipped and not forbidden
    response = {"status": "PASS" if passed else "FAIL", "tests": observed.testsRun,
                "errors": len(observed.errors), "failures": len(observed.failures),
                "skipped": len(observed.skipped), "forbidden_modules": forbidden,
                "native_stages": 0, "scope": SCOPE}
    reply = (json.dumps(response, sort_keys=True) + "\n").encode()
    R.save(args.event, {"request_sha256": hashlib.sha256(raw).hexdigest(),
                        "response_sha256": hashlib.sha256(reply).hexdigest(), "native_stages": 0})
    sys.stdout.buffer.write(reply)
    return 0 if passed else 1


def coordinator():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"local-network-smoke-[0-9]{2}", args.run):
        raise RuntimeError("SMOKE_RUN_NAME")
    root = INSTALL / "qualification" / args.run
    root.mkdir(exist_ok=False)
    cases, fixtures, sources = (root / name for name in ("cases", "fixtures", "sources"))
    for path in (cases, fixtures, sources):
        path.mkdir()
    config = root / "config.json"
    R.save(config, {"schema": 1, "tests": COUNT, "state": str(fixtures.resolve())})
    names = ["tests/run_easy_network.py", "tests/test_local_network_smoke.py", "tests/test_peer_wire.py",
             "tests/run_transport.py", "py/peer_wire.py", "py/peer_service.py", "py/run_stage.py",
             "py/domains.py", "py/supervise.py"]
    pins = [R.pin(sys.executable), R.pin(config)]
    snapshots = []
    for name in names:
        source = INSTALL / name
        selected_pin = R.pin(source)
        target = sources / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(source.read_bytes())
        snapshot_pin = R.pin(target)
        if (snapshot_pin["bytes"], snapshot_pin["sha256"]) != (selected_pin["bytes"], selected_pin["sha256"]):
            raise RuntimeError("SMOKE_SOURCE_CHANGED")
        pins.append(selected_pin)
        snapshots.append(snapshot_pin)
    limits = {"pins": pins, "wall_seconds": 60, "cpu_seconds": 30, "memory_mib": 512,
              "active_processes": 8, "stdout_bytes": 65536, "stderr_bytes": 65536, "event_bytes": 65536}
    R.save(root / "launch.json", {"pins": pins, "snapshots": snapshots, "limits": limits,
                                  "native_stages": 0, "scope": SCOPE})
    started = time.monotonic()
    try:
        transport = R.supervise.Transport(sys.executable, Path(__file__).resolve(), config,
                                          fixtures, cases, R.run_stage, limits)
        response = transport("three-tests", REQUEST)
        outcome = json.loads(response["stdout"])
        if response["returncode"] != 0 or outcome["status"] != "PASS" or outcome["tests"] != COUNT:
            raise RuntimeError("SMOKE_TESTS_FAILED")
        result = {"status": "PASS_PENDING_OUTCOME_REVIEW", "outcome": outcome}
    except BaseException as error:
        result = {"status": "FAILED", "error": type(error).__name__, "detail": str(error)[:2048]}
    result.update(elapsed_seconds=time.monotonic() - started, native_stages=0)
    R.save(root / "result.json", result)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS_PENDING_OUTCOME_REVIEW" else 1


if __name__ == "__main__":
    if not (sys.dont_write_bytecode and sys.flags.ignore_environment and sys.flags.no_site and sys.flags.no_user_site):
        raise RuntimeError("PYTHON_STARTUP_PROFILE")
    raise SystemExit(coordinator() if "--run" in sys.argv else worker())

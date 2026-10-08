"""Native-free owner-contract suite under the product process supervisor."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest


def main():
    parser = argparse.ArgumentParser()
    for name in ("config", "state", "request", "event"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    if not (sys.dont_write_bytecode and sys.flags.ignore_environment and sys.flags.no_site and sys.flags.no_user_site):
        raise RuntimeError("PYTHON_STARTUP_PROFILE")
    with args.request.open("rb") as stream:
        raw = stream.read(1025)
    if raw != b'{"op":"test-owner"}\n':
        raise RuntimeError("FIXED_TEST_REQUEST")
    config = json.loads(args.config.read_bytes())
    if config != {"schema": 1, "tests": 20, "state": str(args.state.resolve())}:
        raise RuntimeError("TEST_CONFIG_BINDING")
    if not args.state.is_absolute() or not args.state.is_dir():
        raise RuntimeError("TEST_ROOT_REQUIRED")
    os.environ["DTMKN_TEST_ROOT"] = str(args.state.resolve())
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parent), pattern="test_owner_contracts.py")
    outcome = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    response = {"status": "PASS" if outcome.wasSuccessful() and outcome.testsRun == 20 else "FAIL",
                "tests": outcome.testsRun, "failures": len(outcome.failures), "errors": len(outcome.errors),
                "skipped": len(outcome.skipped), "native_stages": 0,
                "scope": "path/record/operator refusal contracts; not native or peer acceptance"}
    reply = (json.dumps(response, sort_keys=True, separators=(",", ":")) + "\n").encode()
    event = {"request_sha256": hashlib.sha256(raw).hexdigest(),
             "response_sha256": hashlib.sha256(reply).hexdigest(), "native_stages": 0}
    with args.event.open("xb") as stream:
        stream.write((json.dumps(event, sort_keys=True) + "\n").encode())
    sys.stdout.buffer.write(reply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Native-free context contract tests; retained synthetic state, no mathematics."""
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
    if not (sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_site and sys.flags.no_user_site and os.name == "nt"):
        raise RuntimeError("WINDOWS_STARTUP_PROFILE")
    if args.request.stat().st_size > 1024 or args.config.stat().st_size > 65536:
        raise RuntimeError("INPUT_BOUND")
    raw = args.request.read_bytes()
    if raw != b'{"op":"test-context-contract"}\n':
        raise RuntimeError("FIXED_REQUEST")
    config = json.loads(args.config.read_bytes())
    if (set(config) != {"schema", "tests", "state"} or type(config["schema"]) is not int
            or config["schema"] != 1 or type(config["tests"]) is not int
            or not 1 <= config["tests"] <= 64):
        raise RuntimeError("CONFIG_FIELDS")
    expected_state = Path(__file__).resolve().parents[2] / "product-local/context-contract-01"
    if args.state.resolve() != expected_state or config["state"] != str(expected_state) or not expected_state.is_dir():
        raise RuntimeError("FIXED_STATE_BINDING")
    os.environ["DTMKN_TEST_ROOT"] = str(expected_state)
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parent),
                                              pattern="test_context_selection.py")
    outcome = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    passed = outcome.wasSuccessful() and outcome.testsRun == config["tests"] and not outcome.skipped
    value = {"status": "PASS" if passed else "FAIL", "tests": outcome.testsRun,
             "failures": len(outcome.failures), "errors": len(outcome.errors),
             "skipped": len(outcome.skipped), "native_stages": 0,
             "scope": "synthetic metadata contract controls; no native mathematics or saturation qualification"}
    reply = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
    event = {"request_sha256": hashlib.sha256(raw).hexdigest(),
             "response_sha256": hashlib.sha256(reply).hexdigest(), "native_stages": 0}
    with args.event.open("xb") as stream:
        stream.write((json.dumps(event, sort_keys=True) + "\n").encode())
    sys.stdout.buffer.write(reply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

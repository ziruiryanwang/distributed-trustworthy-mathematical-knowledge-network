"""Native-free CloseHandle regression controls in a separately bounded worker."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import unittest


def main():
    parser = argparse.ArgumentParser()
    for name in ('config', 'state', 'request', 'event'):
        parser.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args()
    if not (sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_site and sys.flags.no_user_site):
        raise RuntimeError('PYTHON_STARTUP_PROFILE')
    raw = args.request.read_bytes()
    if raw != b'{"op":"test-close"}\n':
        raise RuntimeError('FIXED_REQUEST')
    config = json.loads(args.config.read_bytes())
    if set(config) != {'schema', 'tests', 'state'} or config['schema'] != 1:
        raise RuntimeError('CONFIG_FIELDS')
    if type(config['tests']) is not int or not 1 <= config['tests'] <= 8:
        raise RuntimeError('TEST_COUNT')
    if config['state'] != str(args.state.resolve()) or not args.state.is_dir():
        raise RuntimeError('STATE_BINDING')
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parent),
                                              pattern='test_job_close.py')
    outcome = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    passed = outcome.wasSuccessful() and outcome.testsRun == config['tests'] and not outcome.skipped
    value = {'status': 'PASS' if passed else 'FAIL', 'tests': outcome.testsRun,
             'failures': len(outcome.failures), 'errors': len(outcome.errors),
             'skipped': len(outcome.skipped), 'native_stages': 0,
             'scope': 'mocked close branches; actual enclosing worker supervision, not peer recovery'}
    reply = (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()
    event = {'request_sha256': hashlib.sha256(raw).hexdigest(),
             'response_sha256': hashlib.sha256(reply).hexdigest(), 'native_stages': 0}
    with args.event.open('xb') as stream:
        stream.write((json.dumps(event, sort_keys=True) + '\n').encode())
    sys.stdout.buffer.write(reply)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

"""One fresh native-free close-01 run; no existing qualification is rerun."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time

INSTALL = Path(__file__).resolve().parents[1]
SOURCES = ('tests/run_close.py', 'tests/close_worker.py', 'tests/test_job_close.py',
           'py/run_stage.py', 'py/supervise.py', 'py/domains.py')


def pin(path):
    path = Path(path).resolve(strict=True)
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink() or getattr(ancestor.lstat(), 'st_file_attributes', 0) & 0x400:
            raise RuntimeError('REPARSE_POINT')
    if not path.is_file() or path.stat().st_size > 16 * 1048576:
        raise RuntimeError('PIN_SIZE')
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def save(path, value):
    raw = (json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode()
    if len(raw) > 1048576:
        raise RuntimeError('RECORD_SIZE')
    with path.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--launch', required=True, type=Path)
    args = parser.parse_args()
    if not (sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_site and sys.flags.no_user_site and os.name == 'nt'):
        raise RuntimeError('WINDOWS_STARTUP_PROFILE')
    if not args.launch.is_absolute() or args.launch.stat().st_size > 65536:
        raise RuntimeError('LAUNCH_BOUND')
    launch = json.loads(args.launch.read_bytes())
    if set(launch) != {'schema', 'tests', 'pins'} or type(launch['schema']) is not int or launch['schema'] != 1:
        raise RuntimeError('LAUNCH_FIELDS')
    if type(launch['tests']) is not int or not 1 <= launch['tests'] <= 8:
        raise RuntimeError('TEST_COUNT')
    pins = [pin(sys.executable), *[pin(INSTALL / name) for name in SOURCES]]
    if launch['pins'] != pins:
        raise RuntimeError('EXACT_SOURCE_PINS')
    sys.path.insert(0, str(INSTALL / 'py'))
    import run_stage
    import supervise
    root = INSTALL / 'qualification' / 'close-01'
    root.mkdir(exist_ok=False)
    cases, state = root / 'cases', root / 'state'
    cases.mkdir()
    state.mkdir()
    config = root / 'config.json'
    save(config, {'schema': 1, 'tests': launch['tests'], 'state': str(state)})
    limits = {'pins': [*pins, pin(config)], 'wall_seconds': 30, 'cpu_seconds': 15,
              'memory_mib': 256, 'active_processes': 8, 'stdout_bytes': 65536,
              'stderr_bytes': 65536, 'event_bytes': 65536}
    save(root / 'launch.json', {'selected_launch': pin(args.launch), 'pins': pins, 'limits': limits})
    started = time.monotonic()
    try:
        transport = supervise.Transport(sys.executable, INSTALL / 'tests/close_worker.py',
                                        config, state, cases, run_stage, limits)
        response = transport('all-tests', b'{"op":"test-close"}\n')
        outcome = json.loads(response['stdout'])
        if response['returncode'] != 0 or outcome['status'] != 'PASS' or outcome['tests'] != launch['tests']:
            raise RuntimeError('CLOSE_TESTS_FAILED')
        result = {'status': 'PASS_PENDING_OUTCOME_REVIEW', 'outcome': outcome,
                  'elapsed_seconds': time.monotonic() - started, 'native_stages': 0}
    except BaseException as error:
        result = {'status': 'FAILED', 'error': type(error).__name__, 'detail': str(error)[:1024],
                  'elapsed_seconds': time.monotonic() - started, 'native_stages': 0}
    save(root / 'result.json', result)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] == 'PASS_PENDING_OUTCOME_REVIEW' else 1


if __name__ == '__main__':
    raise SystemExit(main())

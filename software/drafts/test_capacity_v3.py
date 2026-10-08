"""Native-free v3 contracts against staged real storage/capacity/admin modules.

Synthetic initialization and stage-reservation rows are NOT native acceptance.
Physical supply is mocked here; the real same-volume probe is a separate grant.
Root alone stages/imports/executes this file after source and launch review.
"""
from copy import deepcopy
import ctypes
import hashlib
import os
from pathlib import Path
import sqlite3
import stat
import subprocess
import sys
import unittest
from unittest.mock import patch

if not (os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
        and sys.flags.no_site and sys.flags.no_user_site):
    raise RuntimeError("WINDOWS_PYTHON_PROFILE")
if sqlite3.sqlite_version != "3.50.4":
    raise RuntimeError("SQLITE_PROFILE")

INSTALL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(INSTALL / "py"))
import capacity as C
import storage as S
import admin_worker as A
import domains as D
import node as N

for module, filename in ((C, "capacity.py"), (S, "storage.py"), (A, "admin_worker.py"),
                         (D, "domains.py"), (N, "node.py")):
    if Path(module.__file__).resolve() != INSTALL / "py" / filename:
        raise RuntimeError("STAGED_MODULE_ORIGIN")

MIB = 1048576
CONFIG = "a" * 64
REFUSED = S.encode({"status": "REFUSED", "code": "SYNTHETIC_NO_NATIVE_WORK"})
TABLES = {"meta": "id", "authorization": "id", "owner_grants": "sequence",
          "requests": "key", "records": "handle", "heads": "client",
          "providers": "provider", "snapshots": "handle", "entries": "provider,seq", "stages": "id"}


def event():
    return {"sql_vm_steps": 0, "sql_rows": {}, "sql_opened": False, "stages_allocated": 0}


def limits(**changes):
    return dict({"requests": 2, "stages": 1, "staging_bytes": 144 * MIB,
        "metadata_pages": 8192, "request_bytes": 8 * MIB, "stage_bytes": 128 * MIB,
        "peer_request_bytes": 64 * MIB, "expose_request_bytes": 80 * MIB,
        "native_seconds": 30, "native_memory_mib": 128, "entries": 8192}, **changes)


def grant(name="grant", requests=1, stages=0, reserved_bytes=8 * MIB, cap=None):
    value = {"schema": 1, "op": "renew", "grant_id": name, "config": CONFIG,
             "add": {"requests": requests, "stages": stages, "reserved_bytes": reserved_bytes}}
    if cap is not None:
        value["metadata_cap_mib"] = cap
    return S.encode(value)


def compact(value):
    return {"bytes": len(value), "sha256": hashlib.sha256(value).hexdigest()} if type(value) is bytes else value


def safe(path):
    path = Path(path)
    S.require(path.is_absolute(), "ABSOLUTE_TEST_ROOT")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        S.require(not stat.S_ISLNK(info.st_mode)
                  and not getattr(info, "st_file_attributes", 0) & 0x400, "TEST_REPARSE_POINT")
    return path.resolve(strict=True)


class FakeCall:
    def __init__(self, function):
        self.function = function
    def __call__(self, *args):
        return self.function(*args)


class FakeVolume:
    """Explicit mocked Win32 supply outcomes; never an OS volume observation."""
    def __init__(self, available, *, mismatch=False, filesystem="NTFS", drive=3):
        self.count = 0
        def mount(_path, output, _size):
            output.value = "X:\\"
            return 1
        def name(_mount, output, _size):
            self.count += 1
            output.value = "mock-volume-" + str(self.count if mismatch else 1)
            return 1
        def information(*args):
            args[6].value = filesystem
            return 1
        def free(_path, available_pointer, total_pointer, free_pointer):
            for pointer, value in ((available_pointer, available), (total_pointer, 2 ** 48), (free_pointer, available)):
                ctypes.cast(pointer, ctypes.POINTER(ctypes.c_ulonglong))[0] = value
            return 1
        self.GetVolumePathNameW = FakeCall(mount)
        self.GetVolumeNameForVolumeMountPointW = FakeCall(name)
        self.GetDriveTypeW = FakeCall(lambda _mount: drive)
        self.GetVolumeInformationW = FakeCall(information)
        self.GetDiskFreeSpaceExW = FakeCall(free)


class CapacityV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = safe(os.environ.get("DTMKN_TEST_ROOT", ""))
        S.require(parent.is_dir() and not parent.is_relative_to(INSTALL)
                  and not INSTALL.is_relative_to(parent), "EXTERNAL_TEST_ROOT")
        cls.suite = parent / "capacity-v3"
        cls.suite.mkdir(exist_ok=False)

    def setUp(self):
        self.root = self.suite / self._testMethodName
        self.root.mkdir(exist_ok=False)
        self.stores, self.supplies, self.notes = [], [], {}
        for target, attribute, replacement in ((S, "physical_supply", self.fake_supply),
                (A, "physical_supply", self.fake_supply),
                (N.Dispatcher, "checking", self.forbidden), (subprocess, "Popen", self.forbidden)):
            handle = patch.object(target, attribute, replacement)
            handle.start()
            self.addCleanup(handle.stop)

    def forbidden(self, *args, **kwargs):
        raise AssertionError("NATIVE_OR_PROCESS_WORK_FORBIDDEN")

    def fake_supply(self, root, scratch, remaining, pages, *, enforce=True):
        self.supplies.append({"root": str(root), "scratch": str(scratch), "remaining": remaining,
                              "pages": pages, "enforce": enforce, "mocked": True})
        return {"mocked": True, "sample_only": True, "reserved_by_os": False, "sufficient": True,
                "volume": "mock-volume", "filesystem": "NTFS", "available_bytes": 2 ** 48,
                "required_bytes": remaining + 2 * pages * 4096 + 1024 * MIB,
                "remaining_authorized_bytes": remaining, "metadata_pages": pages}

    def configuration(self, name="node", selected_limits=None):
        base = self.root / name
        base.mkdir(exist_ok=False)
        scratch, runtime = base / "scratch", base / "runtime"
        scratch.mkdir()
        runtime.mkdir()
        return {"schema": 3, "config_id": CONFIG, "limits": selected_limits or limits(),
            "domains": {"install": str(INSTALL), "state": str(base / "state"),
                        "scratch": str(scratch), "lean_runtime": str(runtime)}}

    def open(self, config, *, create=False, readonly=False):
        store = S.ControlStore(config["domains"]["state"], CONFIG, config["limits"], event(),
                               create=create, readonly=readonly, scratch=config["domains"]["scratch"])
        self.stores.append(store)
        return store

    def close(self, store):
        store.close()
        self.stores.remove(store)

    def fresh(self, name="node", selected_limits=None, initialized=True):
        config = self.configuration(name, selected_limits)
        with S.owner_lock(config["domains"]["state"]):
            store = self.open(config, create=True)
            if initialized:
                # Synthetic bookkeeping prerequisite only: no context, proof,
                # accepted response or native evidence is manufactured.
                with store.transaction():
                    store.exec("fixture_initialized", "UPDATE meta SET initialized=1 WHERE id=1")
                    store.snapshot("P1", 0)
        return config, store

    def snapshot(self, store):
        return {table: [[compact(value) for value in row] for row in
            store.rows("test_" + table, "SELECT * FROM " + table + " ORDER BY " + order, maximum=128)]
            for table, order in TABLES.items()}

    def files(self, root=None):
        root = self.root if root is None else Path(root)
        if not root.exists():
            return {}
        result, total = {}, 0
        for number, path in enumerate(root.rglob("*"), 1):
            S.require(number <= 1024, "FIXTURE_ENTRY_BOUND")
            safe(path)
            if path.is_file():
                size = path.stat().st_size
                total += size
                S.require(total <= 128 * MIB and len(result) < 256, "FIXTURE_FILE_BOUND")
                h = hashlib.sha256()
                with path.open("rb") as stream:
                    for data in iter(lambda: stream.read(MIB), b""):
                        h.update(data)
                result[path.relative_to(root).as_posix()] = {"bytes": size, "sha256": h.hexdigest()}
        return result

    def refuses(self, code, function, *args, **kwargs):
        with self.assertRaises(S.Refusal) as error:
            function(*args, **kwargs)
        self.assertEqual(error.exception.code, code)

    def request(self, store, name):
        raw = S.encode({"synthetic": True, "id": name})
        return store.reserve("local", name, raw), raw

    def finish(self, store, key):
        store.terminal_refusal(key, REFUSED)

    def renew(self, store, raw):
        return store.renew(raw, C.parse_grant(raw, CONFIG))

    def exhaust(self, store):
        first, first_raw = self.request(store, "first")
        store.stage(first, "submit")  # Real reservation row; no native execution.
        self.finish(store, first)
        second, second_raw = self.request(store, "second")
        self.refuses("STAGE_QUOTA", store.stage, second, "submit")
        self.finish(store, second)
        return first_raw, second_raw

    def test_exact_integer_initial_and_grant_parsers(self):
        self.assertEqual(C.initial_authorization(limits()), {"requests": 2, "stages": 1,
                         "reserved_bytes": 144 * MIB, "metadata_pages": 8192, "grants": 0})
        for field in ("requests", "stages", "staging_bytes", "metadata_pages", "stage_bytes", "request_bytes"):
            for bad in (True, False, -1, 1.5, "2", None, 2 ** 100):
                with self.subTest(field=field, value=repr(bad)), self.assertRaises(S.Refusal):
                    C.initial_authorization(limits(**{field: bad}))
        base = S.decode(grant())
        invalid = []
        for field in ("requests", "stages", "reserved_bytes"):
            for bad in (True, False, -1, 1.5, "1", None, 2 ** 100):
                item = deepcopy(base)
                item["add"][field] = bad
                invalid.append(S.encode(item))
        for change in ({"schema": True}, {"op": "status"}, {"config": "b" * 64},
                       {"grant_id": "../bad"}, {"grant_id": "x" * 65}, {"metadata_cap_mib": True},
                       {"metadata_cap_mib": 33}, {"unknown": 1}):
            invalid.append(S.encode(dict(base, **change)))
        invalid.extend([b" " * 4097, b'{"schema":1,"schema":1}', b'{"x":NaN}',
                        grant(requests=0, stages=0, reserved_bytes=0)])
        for raw in invalid:
            with self.subTest(raw=raw[:80]), self.assertRaises(S.Refusal):
                C.parse_grant(raw, CONFIG)
        self.assertEqual(C.parse_grant(grant(requests=0, reserved_bytes=0, cap=64), CONFIG)["metadata_pages"], 16384)
        self.assertFalse(self.supplies)

    def test_fresh_schema_three_and_old_versions_have_no_mutation(self):
        config, store = self.fresh(initialized=False)
        self.assertEqual(store.scalar("version", "PRAGMA user_version"), 3)
        tables = {row[0] for row in store.rows("tables", "SELECT name FROM sqlite_schema WHERE type='table'", maximum=16)}
        self.assertEqual(tables, set(TABLES))
        state = store.authorization_state()
        self.assertEqual(state["used"], {"requests": 0, "stages": 0, "reserved_bytes": 0})
        self.assertEqual(state["initialized"], 0)
        self.close(store)
        for version in (0, 2, 4):
            other = self.configuration("legacy-" + str(version))
            root = Path(other["domains"]["state"])
            root.mkdir()
            db = sqlite3.connect(root / "control.sqlite3")
            db.execute("CREATE TABLE old_marker(value TEXT)")
            db.execute("INSERT INTO old_marker VALUES('synthetic-old-version')")
            db.execute("PRAGMA user_version=" + str(version))
            db.commit()
            db.close()
            before = self.files(root)
            self.refuses("SQLITE_SCHEMA_VERSION", self.open, other, create=True)
            self.assertEqual(before, self.files(root))

    def test_small_quotas_preserve_used_authorized_and_old_replies(self):
        _config, store = self.fresh()
        first_raw, second_raw = self.exhaust(store)
        state = store.authorization_state()
        self.assertEqual(state["used"], {"requests": 2, "stages": 1, "reserved_bytes": 144 * MIB})
        self.assertEqual(state["used"], state["authorized"])
        before = self.snapshot(store)
        self.refuses("REQUEST_QUOTA", self.request, store, "third")
        self.assertEqual(store.prior("local", "first", first_raw), REFUSED)
        self.assertEqual(store.prior("local", "second", second_raw), REFUSED)
        self.assertEqual(before, self.snapshot(store))

    def test_two_renewals_change_only_authorization_and_grant_rows(self):
        _config, store = self.fresh()
        self.exhaust(store)
        for name, additions in (("one", (1, 1, 136 * MIB)), ("two", (1, 0, 8 * MIB))):
            before = self.snapshot(store)
            reply = S.decode(self.renew(store, grant(name, *additions)))
            after = self.snapshot(store)
            for table in set(TABLES) - {"authorization", "owner_grants"}:
                self.assertEqual(before[table], after[table], table)
            self.assertFalse(reply["mathematicalAcceptance"])
            self.assertFalse(reply["refund"])
            self.assertEqual(reply["used_at_commit"], store.authorization_state()["used"])
            key, _ = self.request(store, name)
            if name == "one":
                store.stage(key, "submit")
            self.finish(store, key)
        self.assertEqual(store.authorization_state()["used"],
                         {"requests": 4, "stages": 2, "reserved_bytes": 288 * MIB})
        self.assertEqual(store.authorization_state()["used"], store.authorization_state()["authorized"])

    def test_exact_grant_replay_and_conflict_precede_pending_and_exhaustion(self):
        _config, store = self.fresh()
        _first, second = self.exhaust(store)
        raw = grant("last")
        original = self.renew(store, raw)
        key, _ = self.request(store, "pending-last")
        before = self.snapshot(store)
        with patch.object(S, "physical_supply", side_effect=AssertionError("SUPPLY_ON_REPLAY")):
            self.assertEqual(self.renew(store, raw), original)
            self.assertTrue(store.event["renewal_historical"])
            self.refuses("GRANT_ID_CONFLICT", self.renew, store, b" " + raw)
        self.assertEqual(store.prior("local", "second", second), REFUSED)
        self.assertEqual(before, self.snapshot(store))
        self.assertEqual(store.meta()["active"], key)

    def test_sixty_four_grants_and_unrecorded_refused_id_reuse(self):
        config, store = self.fresh(selected_limits=limits(requests=1, staging_bytes=136 * MIB))
        key, _ = self.request(store, "pending")
        raw = grant("reusable")
        self.refuses("PENDING_EXECUTION", self.renew, store, raw)
        self.assertEqual(store.scalar("grants", "SELECT count(*) FROM owner_grants"), 0)
        self.finish(store, key)
        original = self.renew(store, raw)
        self.close(store)
        for i in range(2, 65):
            store = self.open(config)
            self.renew(store, grant("g-" + str(i), requests=1, reserved_bytes=0))
            self.close(store)
        store = self.open(config)
        self.assertEqual(store.authorization_state()["grants"], 64)
        before = self.snapshot(store)
        self.refuses("GRANT_QUOTA", self.renew, store, grant("sixty-five"))
        self.assertEqual(self.renew(store, raw), original)
        self.assertEqual(before, self.snapshot(store))

    def test_cap_only_expansion_restores_real_metadata_headroom(self):
        _config, store = self.fresh()
        for i in range(9):
            with store.transaction():
                store.put_record("synthetic-pressure", "local", {"i": i, "padding": "x" * (2 * MIB - 1024)})
        self.assertGreater(store.page_count(), 4096)
        before = self.snapshot(store)
        self.refuses("METADATA_HEADROOM", self.request, store, "too-full")
        self.assertEqual(before, self.snapshot(store))
        self.renew(store, grant("cap", requests=0, reserved_bytes=0, cap=64))
        self.assertEqual(store.authorization_state()["used"], {"requests": 0, "stages": 0, "reserved_bytes": 0})
        self.assertEqual(store.authorization_state()["metadata_pages"], 16384)
        key, _ = self.request(store, "fits-after-expansion")
        self.finish(store, key)
        self.notes["actual_pages_after_expansion"] = store.page_count()

    def test_status_is_state_byte_read_only_uninitialized_pending_exhausted(self):
        config, store = self.fresh(selected_limits=limits(requests=1, staging_bytes=136 * MIB), initialized=False)
        status_raw = S.encode({"schema": 1, "op": "status", "config": CONFIG})
        self.close(store)
        before = self.files(Path(config["domains"]["state"]))
        result = S.decode(A.run(config, status_raw, event()))
        self.assertEqual(result["initialized"], 0)
        self.assertTrue(result["state_read_only"])
        self.assertEqual(before, self.files(Path(config["domains"]["state"])))
        store = self.open(config)
        with store.transaction():
            store.exec("fixture_initialize", "UPDATE meta SET initialized=1")
            store.snapshot("P1", 0)
        key, _ = self.request(store, "pending-exhausted")
        store.stage(key, "submit")
        self.close(store)
        before = self.files(Path(config["domains"]["state"]))
        result = S.decode(A.run(config, status_raw, event()))
        self.assertEqual(result["active"], key)
        self.assertEqual(result["remaining"], {"requests": 0, "stages": 0, "reserved_bytes": 0})
        self.assertEqual(result["pending_request"]["phase"], "pending")
        self.assertEqual(before, self.files(Path(config["domains"]["state"])))
        self.notes["status_pending_exhausted"] = result

    def test_status_no_store_and_real_locked_busy_create_no_state(self):
        config = self.configuration()
        raw = S.encode({"schema": 1, "op": "status", "config": CONFIG})
        before = self.files()
        self.assertEqual(S.decode(A.run(config, raw, event()))["status"], "NOT_INITIALIZED")
        self.assertEqual(before, self.files())
        state = Path(config["domains"]["state"])
        with S.owner_lock(state):
            pass
        before = self.files()
        self.assertEqual(S.decode(A.run(config, raw, event()))["status"], "NOT_INITIALIZED")
        self.assertEqual(before, self.files())
        with S.owner_lock(state):
            # A second real handle attempts the same Windows byte-range lock.
            # No fake BUSY exception or subprocess supplies this observation.
            self.refuses("BUSY", A.run, config, raw, event())
        self.assertEqual(before, self.files())
        self.assertFalse((state / "control.sqlite3").exists())

    def test_terminal_refusal_only_exact_pending_after_confirmed_rollback(self):
        _config, store = self.fresh()
        key, _ = self.request(store, "pending")
        before = self.snapshot(store)
        for value in ({"status": "OK", "accepted": True},
                      {"status": "REFUSED", "code": "X", "accepted": False},
                      {"status": "REFUSED", "code": "X", "mathematicalAcceptance": True},
                      {"status": "REFUSED", "code": "X", "mathematicalAcceptance": 1}):
            self.refuses("TERMINAL_REFUSAL_ONLY", store.terminal_refusal, key, S.encode(value))
        self.refuses("METADATA_REFUSAL_BOUND", store.terminal_refusal, key,
                     S.encode({"status": "REFUSED", "code": "METADATA_SPACE", "padding": "x" * 4096}))
        self.refuses("PENDING_BINDING", store.terminal_refusal, "b" * 64, REFUSED)
        with store.transaction():
            self.refuses("ROLLBACK_NOT_COMPLETE", store.terminal_refusal, key, REFUSED)
        with self.assertRaisesRegex(RuntimeError, "synthetic-precommit"):
            with store.transaction():
                store.put_record("synthetic-unpromoted", "local", {"not_mathematics": True})
                raise RuntimeError("synthetic-precommit")
        self.assertEqual(before, self.snapshot(store))
        self.finish(store, key)
        after = self.snapshot(store)
        for table in set(TABLES) - {"meta", "requests"}:
            self.assertEqual(before[table], after[table])
        self.assertEqual(store.authorization_state()["used"], {"requests": 1, "stages": 0, "reserved_bytes": 8 * MIB})
        self.assertIsNone(store.meta()["active"])

    def test_commit_before_after_errors_are_unknown_and_cannot_clear(self):
        for operation in ("renewal", "ordinary"):
            for after_commit in (False, True):
                with self.subTest(operation=operation, after_commit=after_commit):
                    config, store = self.fresh(operation + str(after_commit))
                    key, request_raw = (self.request(store, "pending") if operation == "ordinary" else ("b" * 64, None))
                    before = self.snapshot(store)
                    raw, original_exec = grant("uncertain"), store.exec
                    def injected(name, statement, values=()):
                        if name == "commit":
                            if after_commit:
                                original_exec(name, statement, values)
                            raise OSError("synthetic-commit-boundary")
                        return original_exec(name, statement, values)
                    with patch.object(store, "exec", side_effect=injected):
                        if operation == "renewal":
                            self.refuses("RENEWAL_OUTCOME_UNKNOWN", self.renew, store, raw)
                            self.assertEqual(store.event["renewal_state_outcome"], "UNKNOWN_REPLAY_REQUIRED")
                        else:
                            with self.assertRaises(S.Refusal) as failure:
                                with store.transaction():
                                    store.terminal(key, REFUSED)
                            self.assertEqual(failure.exception.code, "TRANSACTION_OUTCOME_UNKNOWN")
                    self.refuses("TRANSACTION_OUTCOME_UNKNOWN", store.terminal_refusal, key, REFUSED)
                    self.close(store)
                    store = self.open(config)
                    if not after_commit:
                        self.assertEqual(before, self.snapshot(store))
                    if operation == "renewal":
                        self.assertEqual(store.authorization_state()["grants"], int(after_commit))
                        self.renew(store, raw)
                        self.assertEqual(store.event["renewal_historical"], after_commit)
                        self.assertEqual(store.authorization_state()["grants"], 1)
                    elif after_commit:
                        self.assertEqual(store.prior("local", "pending", request_raw), REFUSED)
                        self.assertIsNone(store.meta()["active"])
                    else:
                        self.assertEqual(store.meta()["active"], key)
                    self.close(store)

    def test_physical_supply_mocked_volume_space_and_parser_boundaries(self):
        config = self.configuration()
        state, scratch = Path(config["domains"]["state"]), Path(config["domains"]["scratch"])
        state.mkdir()
        remaining, pages = 17 * MIB, 8192
        required = remaining + 2 * pages * 4096 + 1024 * MIB
        for kwargs, code in (({"enforce": 1}, "SUPPLY_OBSERVATION_MODE"),
                             ({"remaining_bytes": True}, "REMAINING_CAPACITY"),
                             ({"metadata_pages": 8192.0}, "METADATA_CAP"),
                             ({"scratch": None}, "SUPPLY_SCRATCH_REQUIRED")):
            arguments = dict(root=state, scratch=scratch, remaining_bytes=remaining, metadata_pages=pages, enforce=True)
            arguments.update(kwargs)
            with patch.object(ctypes, "WinDLL", side_effect=AssertionError("OS_QUERY_BEFORE_VALIDATION")):
                self.refuses(code, C.physical_supply, **arguments)
        for available, enforced in ((required, True), (required - 1, False)):
            with patch.object(ctypes, "WinDLL", return_value=FakeVolume(available)):
                observed = C.physical_supply(state, scratch, remaining, pages, enforce=enforced)
            self.assertEqual(observed["required_bytes"], required)
            self.assertEqual(observed["sufficient"], available >= required)
            self.assertFalse(observed["reserved_by_os"])
        for kernel, code in ((FakeVolume(required - 1), "PHYSICAL_SUPPLY"),
                             (FakeVolume(required, mismatch=True), "STATE_SCRATCH_VOLUME"),
                             (FakeVolume(required, filesystem="FAT32"), "NTFS_STORAGE_REQUIRED"),
                             (FakeVolume(required, drive=2), "LOCAL_FIXED_VOLUME_REQUIRED")):
            with patch.object(ctypes, "WinDLL", return_value=kernel):
                self.refuses(code, C.physical_supply, state, scratch, remaining, pages)
        self.notes["real_os_supply_probe"] = "not executed by unit suite; separate root allocation required"

    def tearDown(self):
        errors = []
        for store in self.stores:
            try:
                store.close()
            except BaseException as error:
                errors.append(type(error).__name__)
        rows, observation_error = {}, None
        try:
            rows = self.files()
        except Exception as error:
            observation_error = type(error).__name__ + ":" + str(error)[:512]
        report = S.encode({"test": self.id(), "synthetic_only": True, "native_acceptance": False,
            "notes": self.notes, "mocked_physical_supply_calls": self.supplies,
            "retained_files_before_report": rows, "close_errors": errors,
            "observation_error": observation_error,
            "outcome_authority": "separate unittest result, not existence of this report"})
        self.assertLessEqual(len(report), MIB)
        with (self.root / "observations.json").open("xb") as stream:
            stream.write(report)
            stream.flush()
            os.fsync(stream.fileno())
        self.assertIsNone(observation_error)
        bound = 24 * MIB if self._testMethodName == "test_cap_only_expansion_restores_real_metadata_headroom" else 8 * MIB
        self.assertLessEqual(sum(row["bytes"] for row in rows.values()) + len(report), bound)
        self.assertLessEqual(sum(row["bytes"] for row in self.files(self.suite).values()), 128 * MIB)
        self.assertFalse(errors)


if __name__ == "__main__":
    unittest.main(verbosity=2)

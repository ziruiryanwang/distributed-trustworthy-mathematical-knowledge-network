"""Replica ledger contracts against the integrated replica implementation only.

Real SQLite and owner locks; synthetic initialization, offers, original acquire
preparation and quiescence; mocked physical supply. Selected package/view paths
do not exist. View preparation is mocked only in dispatch/commit tests. No
checker, native process, real transport, accepted proof or availability claim.
Root alone imports/runs this file after independent review and fresh allocation.
"""
from contextlib import ExitStack
from copy import deepcopy
import os
from pathlib import Path
import socket
import sqlite3
import stat
import subprocess
import sys
from types import SimpleNamespace
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
import domains as D
import node as N
import peer_wire as W
import peer_service as T
import peer_node as P
import inspect_context as I
import service_worker as V
import recovery_worker as R

MODULES = ((C, "capacity"), (S, "storage"), (D, "domains"), (N, "node"),
           (W, "peer_wire"), (T, "peer_service"), (P, "peer_node"),
           (I, "inspect_context"), (V, "service_worker"), (R, "recovery_worker"))
for module, name in MODULES:
    if Path(module.__file__).resolve() != INSTALL / "py" / (name + ".py"):
        raise RuntimeError("PRODUCT_MODULE_ORIGIN")
if "replica_expose" not in N.PEER_OPS or not hasattr(P, "replica_custody"):
    raise RuntimeError("REVIEWED_REPLICA_INTEGRATION_REQUIRED")

MIB = 1048576
CONFIG = "d" * 64
TABLES = {"meta": "id", "authorization": "id", "owner_grants": "sequence",
          "requests": "key", "records": "handle", "heads": "client",
          "providers": "provider", "snapshots": "handle", "entries": "provider,seq", "stages": "id"}


def event():
    return {"sql_vm_steps": 0, "sql_rows": {}, "sql_opened": False,
            "stages_allocated": 0, "historical": False,
            "terminal_write_attempted": False, "transition_committed": False,
            "state_outcome": "UNCHANGED_BY_RECOVERY", "checker_loaded": False}


def typed(tag, version, byte):
    # Schema-valid synthetic IDs, NOT content identities of checked mathematics.
    return [1, tag, version, {"$bytes": [byte] * 32}]


def quiescence():
    # Synthetic guard input; never a claimed supervisor observation.
    return {"job_created_before_process": True, "attach_resume_returned": True,
            "direct_child_reaped": True, "final_active_zero": True, "job_closed": True,
            "pid": 123, "returncode": 1, "initial_job": {"active_processes": 0},
            "final_job": {"active_processes": 0, "total_processes": 1}, "cleanup_errors": []}


def safe(path):
    path = Path(path)
    S.require(path.is_absolute(), "ABSOLUTE_TEST_ROOT")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        S.require(not stat.S_ISLNK(info.st_mode)
                  and not getattr(info, "st_file_attributes", 0) & 0x400, "TEST_REPARSE_POINT")
    return path.resolve(strict=True)


class ReplicaCustodyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = safe(os.environ.get("DTMKN_TEST_ROOT", ""))
        S.require(parent.is_dir() and not parent.is_relative_to(INSTALL)
                  and not INSTALL.is_relative_to(parent), "EXTERNAL_TEST_ROOT")
        cls.suite = parent / "replica-custody"
        cls.suite.mkdir(exist_ok=False)

    def setUp(self):
        self.root = self.suite / self._testMethodName
        self.root.mkdir(exist_ok=False)
        self.stack, self.stores, self.notes = ExitStack(), [], {}
        self.stack.enter_context(patch.object(S, "physical_supply", self.fake_supply))
        self.stack.enter_context(patch.object(N.Dispatcher, "checking", self.forbidden))
        self.stack.enter_context(patch.object(I, "load_checker", self.forbidden))
        self.stack.enter_context(patch.object(subprocess, "Popen", self.forbidden))
        self.stack.enter_context(patch.object(socket, "socket", self.forbidden))
        for name in ("acquire", "fetch_catalog", "serve"):
            self.stack.enter_context(patch.object(T, name, self.forbidden))

    def forbidden(self, *args, **kwargs):
        raise AssertionError("CHECKER_NATIVE_PROCESS_OR_NETWORK_FORBIDDEN")

    def fake_supply(self, *args, **kwargs):
        return {"mocked": True, "sufficient": True, "reserved_by_os": False}

    def save(self, path, raw):
        S.require(type(raw) is bytes and len(raw) <= MIB, "FIXTURE_OUTPUT_BOUND")
        with path.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())

    def fixture(self, name="node"):
        base = self.root / name
        base.mkdir(exist_ok=False)
        state, scratch = base / "state", base / "scratch"
        scratch.mkdir()
        self.stack.enter_context(S.owner_lock(state))
        limits = {"requests": 8, "stages": 4, "staging_bytes": 1024 * MIB,
            "metadata_pages": 8192, "request_bytes": 8 * MIB, "stage_bytes": 128 * MIB,
            "peer_request_bytes": 64 * MIB, "expose_request_bytes": 80 * MIB,
            "native_seconds": 30, "native_memory_mib": 128, "entries": 8192}
        ev = event()
        origin = scratch / "original-call"
        origin.mkdir()
        ev["origin_directory"] = str(origin)
        store = S.ControlStore(state, CONFIG, limits, ev, create=True, scratch=scratch)
        self.stores.append(store)
        foundation, descriptor, replay = typed(1, 2, 1), typed(0x8111, 3, 2), typed(0x15, 3, 3)
        formal = {key: None for key in W.FORMAL_FIELDS}
        formal.update(replay=replay, descriptor_id=descriptor, symbols=[], trace=[])
        entry = {"descriptor_id": descriptor, "root": replay, "manifest_sha256": "b" * 64,
                 "bundle_sha256": "c" * 64, "bundle_bytes": 100, "formal_metadata": formal}
        W.validate_entry(entry)
        endpoint = {"host": "127.0.0.1", "port": 19999}
        config = {"config_id": CONFIG, "limits": limits, "clients": ["local", "other"],
                  "peers": {"source": endpoint}}
        selection = {"peer": "source", "endpoint": endpoint, "foundation": foundation,
                     "catalog_sha256": "e" * 64, "entry": entry}
        offer = {"package": {"path": str(base / "absent-normalized"), "manifest_sha256": "a" * 64},
                 "descriptor_id": descriptor, "formal_metadata": formal, "symbols": []}
        with store.transaction():
            # Synthetic initialization marker/context, not an accepted context.
            store.exec("fixture", "UPDATE meta SET initialized=1 WHERE id=1")
            store.snapshot("P1", 0)
            context = store.put_record("context", "local", {
                "kind": "synthetic-fixture-not-accepted", "description": {"foundation": foundation}})
            store.set_head("local", context)
            remote = store.put_record("remote", "local", selection)
        req = {"client": "local", "request_id": "acquire", "op": "peer_acquire", "args": {"remote": remote}}
        raw = S.encode(req)
        key = store.reserve("local", "acquire", raw, grant=64 * MIB)
        received = {"path": str(state / "work" / key / "incoming"), "manifest_sha256": entry["manifest_sha256"]}
        dispatcher = N.Dispatcher(config, store, ev)
        dispatcher.key, dispatcher.operation = key, "peer_acquire"
        dispatcher.peer = P.PeerOperations(dispatcher)
        # Actual commit of explicitly synthetic preparation; no transport/checker.
        with store.transaction():
            reply = dispatcher.peer.commit(req, {"offer": offer, "selection": selection,
                "remote": remote, "received_package": received})
            store.terminal(key, S.encode(reply))
        acquisition = store.record(reply["acquisition"], "acquisition", "local")
        return SimpleNamespace(store=store, config=config, event=ev, origin=origin,
            dispatcher=dispatcher, foundation=foundation, entry=entry, offer=offer,
            selection=selection, remote=remote, req=req, raw=raw, key=key, received=received,
            reply=reply, acquisition=acquisition, handle=reply["acquisition"])

    def snapshot(self, store):
        def atom(value):
            return {"hex": value.hex()} if type(value) is bytes else value
        return {table: [{key: atom(row[key]) for key in row.keys()} for row in
            store.rows("test_" + table, "SELECT * FROM " + table + " ORDER BY " + order,
                       maximum=128)] for table, order in TABLES.items()}

    def readonly(self, fixture):
        control = I.ReadOnlyControl(fixture.store.root, CONFIG, event())
        self.stores.append(control)
        return control

    def close(self, store):
        store.close()
        self.stores.remove(store)

    def assert_refusal(self, code, function, *args, **kwargs):
        with self.assertRaises(S.Refusal) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def custody(self, f, handle=None, *, store=None, client="local"):
        return P.replica_custody(f.store if store is None else store, f.config,
                                 client, f.handle if handle is None else handle)

    def rebind(self, f, *, acquisition=None, selection=None, candidate=None, reply=None):
        """Synthetic malformed-ledger construction, not a tested product mutation."""
        acq = deepcopy(f.acquisition if acquisition is None else acquisition)
        response = deepcopy(f.reply if reply is None else reply)
        with f.store.transaction():
            if selection is not None:
                remote = f.store.put_record("remote", "local", selection)
                acq["remote"] = remote
                raw = S.encode(dict(f.req, args={"remote": remote}))
                f.store.exec("fixture", "UPDATE requests SET raw=? WHERE key=?", (raw, f.key))
            if candidate is not None:
                response["candidate"] = f.store.put_record("candidate", "local", candidate)
            handle = f.store.put_record("acquisition", "local", acq)
            response["acquisition"] = handle
            f.store.exec("fixture", "UPDATE requests SET response=? WHERE key=?", (S.encode(response), f.key))
        return handle

    def malformed(self, f, code, handle):
        before = self.snapshot(f.store)
        self.assert_refusal(code, self.custody, f, handle)
        read_only = self.readonly(f)
        try:
            self.assert_refusal(code, self.custody, f, handle, store=read_only)
        finally:
            self.close(read_only)
        self.assertEqual(self.snapshot(f.store), before)

    def prepared(self, f, request_id="expose"):
        key = S.digest(S.encode(["local", request_id]))
        directory = f.store.root / "work" / key / "peer-view"
        def pin(name):
            return {"path": str(directory / name), "bytes": 1, "sha256": "f" * 64}
        return {"view": {"kind": "peer_view", "directory": str(directory), "foundation": f.foundation,
            "catalog": pin("catalog.json"), "complete": pin("complete.json"),
            "selected": [{"provider": "P1", "sequence": f.acquisition["sequence"],
                "descriptor_id": f.entry["descriptor_id"], "basis": "replica-custody", "acquisition": f.handle}],
            "mathematicalAcceptance": False}, "custody": list(self.custody(f))}

    def dispatch(self, f, request_id, prepared):
        req = {"client": "local", "request_id": request_id, "op": "replica_expose", "args": {"acquisition": f.handle}}
        raw = S.encode(req)
        self.assertEqual(N.request(raw, f.config["clients"]), req)
        # Only filesystem/canonical/checker preparation is replaced here.
        with patch.object(f.dispatcher.peer, "replica_expose", return_value=prepared) as mocked:
            reply = f.dispatcher.execute(req, raw)
            self.assertEqual(mocked.call_count, 1)
        return req, raw, reply

    def test_acquire_commit_retains_received_and_normalized_pins(self):
        f = self.fixture()
        self.assertEqual(f.acquisition["received_package"], f.received)
        self.assertEqual(f.acquisition["package"], f.offer["package"])
        self.assertNotEqual(f.received["manifest_sha256"], f.offer["package"]["manifest_sha256"])
        self.assertEqual(f.reply["mathematicalAcceptance"], False)
        self.assertEqual(f.reply["native_stages"], 0)
        self.assertNotIn("accepted", f.reply)
        self.assertEqual(dict(f.store.meta())["charged"], 64 * MIB)
        self.assert_refusal("NOT_LOCALLY_PUBLISHED", f.store.require_published,
                            "P1", f.acquisition["sequence"], f.entry["descriptor_id"])
        self.assertEqual(self.snapshot(f.store)["stages"], [])
        self.notes["scope"] = "Actual acquire commit only; original transport and normalization were synthetic preparation"

    def test_exact_ledger_both_interfaces_without_source_copies(self):
        f = self.fixture()
        before = self.snapshot(f.store)
        self.assertFalse(Path(f.received["path"]).exists())
        self.assertFalse(Path(f.offer["package"]["path"]).exists())
        with patch.object(W, "safe_path", self.forbidden), patch.object(W, "read_local", self.forbidden):
            self.assertEqual(self.custody(f), (f.acquisition, f.selection, f.offer))
            read_only = self.readonly(f)
            try:
                self.assertEqual(self.custody(f, store=read_only), (f.acquisition, f.selection, f.offer))
                self.assert_refusal("READ_ONLY_QUERY_REQUIRED", read_only.exec,
                                    "forbidden", "UPDATE meta SET initialized=0 WHERE id=1")
            finally:
                self.close(read_only)
        self.assertEqual(self.snapshot(f.store), before)
        self.notes["scope"] = "Ledger-only source-copy independence, not serving or package validity"

    def test_legacy_no_custody_and_wrong_client_refuse(self):
        f = self.fixture()
        legacy = deepcopy(f.acquisition)
        del legacy["received_package"]
        self.malformed(f, "REPLICA_CUSTODY_UNAVAILABLE", self.rebind(f, acquisition=legacy))
        before = self.snapshot(f.store)
        self.assert_refusal("WRONG_CLIENT_HANDLE", self.custody, f, client="other")
        self.assert_refusal("HANDLE_KIND", self.custody, f, f.reply["candidate"])
        self.assert_refusal("UNKNOWN_HANDLE", self.custody, f, "acquisition:" + "0" * 64)
        self.assertEqual(self.snapshot(f.store), before)

    def test_acquisition_exact_fields_received_and_request_key(self):
        cases = [("mathematicalAcceptance", 0, "REPLICA_ACQUISITION_BINDING"),
                 ("request", "F" * 64, "REPLICA_REQUEST_KEY"),
                 ("request", True, "REPLICA_REQUEST_KEY"),
                 ("received_package", {"path": "C:\\synthetic\\wrong", "manifest_sha256": "b" * 64}, "REPLICA_RECEIVED_PIN"),
                 ("received_package", {"path": "replace", "manifest_sha256": "0" * 64}, "REPLICA_RECEIVED_PIN"),
                 ("extra", False, "INVALID_FIELDS")]
        for index, (field, value, code) in enumerate(cases):
            with self.subTest(index=index):
                f = self.fixture("case-" + str(index))
                acq = deepcopy(f.acquisition)
                if field == "received_package" and value["path"] == "replace":
                    value = dict(value, path=f.received["path"])
                acq[field] = value
                self.malformed(f, code, self.rebind(f, acquisition=acq))
        self.notes["cases"] = len(cases)

    def test_remote_endpoint_catalog_descriptor_and_bundle_bindings(self):
        for index, field in enumerate(("peer", "endpoint", "catalog_sha256", "descriptor_id", "bundle_sha256")):
            with self.subTest(field=field):
                f = self.fixture("acq-" + str(index))
                value = {"peer": "unknown", "endpoint": {"host": "127.0.0.1", "port": 20000},
                         "catalog_sha256": "0" * 64, "descriptor_id": typed(0x8111, 3, 9),
                         "bundle_sha256": "0" * 64}[field]
                self.malformed(f, "REPLICA_REMOTE_BINDING", self.rebind(f, acquisition=dict(f.acquisition, **{field: value})))
        for index, (field, value) in enumerate((("peer", "unknown"), ("catalog_sha256", "E" * 64),
                                               ("endpoint", {"host": "127.0.0.1", "port": 20000}))):
            f = self.fixture("remote-" + str(index))
            self.malformed(f, "REPLICA_REMOTE_BINDING", self.rebind(f, selection=dict(f.selection, **{field: value})))
        self.notes["cases"] = 8

    def test_snapshot_membership_and_offer_correspondence(self):
        for index, sequence in enumerate((True, 0, 2, 8193)):
            f = self.fixture("sequence-" + str(index))
            self.malformed(f, "REPLICA_SNAPSHOT_MEMBERSHIP",
                           self.rebind(f, acquisition=dict(f.acquisition, sequence=sequence)))
        for index, (provider, cut) in enumerate((("P1", 0), ("P2", 1), ("P1", True))):
            f = self.fixture("cut-" + str(index))
            with f.store.transaction():
                snapshot = f.store.snapshot(provider, cut)
            self.malformed(f, "REPLICA_SNAPSHOT_MEMBERSHIP",
                           self.rebind(f, acquisition=dict(f.acquisition, snapshot=snapshot)))
        for index, field in enumerate(("package", "descriptor_id", "formal_metadata")):
            f = self.fixture("offer-" + str(index))
            offer = deepcopy(f.offer)
            offer[field] = {"package": dict(f.offer["package"], manifest_sha256="0" * 64),
                "descriptor_id": typed(0x8111, 3, 9),
                "formal_metadata": dict(f.offer["formal_metadata"], universe_arity=True)}[field]
            with f.store.transaction():
                f.store.exec("fixture", "UPDATE entries SET raw=? WHERE provider='P1' AND seq=1", (S.encode(offer),))
            self.malformed(f, "REPLICA_OFFER_BINDING", f.handle)
        self.notes["cases"] = 10

    def test_original_request_exact_binding_and_terminal_phase(self):
        cases = [("UPDATE requests SET client='other' WHERE key=?", ()),
                 ("UPDATE requests SET request_id='different' WHERE key=?", ()),
                 ("UPDATE requests SET raw=? WHERE key=?", (S.encode({"client": "local", "request_id": "acquire", "op": "expose", "args": {}}),)),
                 ("UPDATE requests SET raw=? WHERE key=?", (b"",)),
                 ("UPDATE requests SET phase='pending',response=NULL WHERE key=?", ()),
                 ("DELETE FROM requests WHERE key=?", ())]
        for index, (sql, values) in enumerate(cases):
            f = self.fixture("case-" + str(index))
            with f.store.transaction():
                f.store.exec("fixture", sql, (*values, f.key))
            self.malformed(f, "REPLICA_REQUEST_BINDING", f.handle)
        f = self.fixture("remote-args")
        raw = S.encode(dict(f.req, args={"remote": "remote:" + "0" * 64}))
        with f.store.transaction():
            f.store.exec("fixture", "UPDATE requests SET raw=? WHERE key=?", (raw, f.key))
        self.malformed(f, "REPLICA_REQUEST_BINDING", f.handle)
        self.notes["cases"] = 7

    def test_candidate_and_terminal_response_exact_binding(self):
        for index, field in enumerate(("snapshot", "sequence", "descriptor_id", "extra")):
            f = self.fixture("candidate-" + str(index))
            candidate = f.store.record(f.reply["candidate"], "candidate", "local")
            candidate[field] = {"snapshot": "snapshot:" + "0" * 64, "sequence": True,
                                "descriptor_id": typed(0x8111, 3, 9), "extra": False}[field]
            self.malformed(f, "REPLICA_CANDIDATE_BINDING", self.rebind(f, candidate=candidate))
        for index, (field, value) in enumerate((("existing", 0), ("native_stages", False),
                ("mathematicalAcceptance", 0), ("accepted", True), ("status", "REFUSED"), ("candidate", True))):
            f = self.fixture("reply-" + str(index))
            self.malformed(f, "REPLICA_TERMINAL_BINDING", self.rebind(f, reply=dict(f.reply, **{field: value})))
        f = self.fixture("wrong-client-candidate")
        candidate = f.store.record(f.reply["candidate"], "candidate", "local")
        with f.store.transaction():
            handle = f.store.put_record("candidate", "other", candidate)
        self.malformed(f, "WRONG_CLIENT_HANDLE", self.rebind(f, reply=dict(f.reply, candidate=handle)))
        self.notes["cases"] = 11

    def test_new_preparation_requires_received_copy_before_checker(self):
        f = self.fixture()
        before = self.snapshot(f.store)
        req = {"client": "local", "request_id": "missing-copy", "op": "replica_expose", "args": {"acquisition": f.handle}}
        self.assert_refusal("PEER_LOCAL_IO_FAILURE", f.dispatcher.peer.prepare, req)
        self.assertEqual(self.snapshot(f.store), before)
        self.assertFalse(f.event["checker_loaded"])
        self.notes["scope"] = "Real new-view preparation refuses absent incoming copy; no successful canonical preparation claim"

    def test_dispatch_precise_view_only_charge_and_historical_replay(self):
        f = self.fixture()
        prepared = self.prepared(f)
        before = self.snapshot(f.store)
        req, raw, reply_raw = self.dispatch(f, "expose", prepared)
        reply = S.decode(reply_raw)
        view_raw = S.encode({"config": CONFIG, "kind": "view", "client": "local", "data": prepared["view"]})
        handle = "view:" + S.digest(view_raw)
        expected_reply = {"status": "OK", "untrusted": True, "candidate_only": True,
            "mathematicalAcceptance": False, "native_stages": 0, "view": handle,
            "catalog_sha256": prepared["view"]["catalog"]["sha256"], "entries": 1,
            "historical_view": True, "basis": "replica-custody"}
        self.assertEqual(reply, expected_reply)
        key = S.digest(S.encode(["local", "expose"]))
        attempt = S.encode({"config": CONFIG, "kind": "attempt", "client": "owner",
                           "data": {"request": key, "call_directory": str(f.origin)}})
        expected = deepcopy(before)
        expected["meta"][0]["requests"] += 1
        expected["meta"][0]["charged"] += 80 * MIB
        expected["requests"].append({"key": key, "client": "local", "request_id": "expose", "raw": {"hex": raw.hex()},
                                     "phase": "terminal", "response": {"hex": reply_raw.hex()}})
        expected["requests"].sort(key=lambda row: row["key"])
        expected["records"].extend([
            {"handle": handle, "kind": "view", "client": "local", "raw": {"hex": view_raw.hex()}},
            {"handle": "attempt:" + S.digest(attempt), "kind": "attempt", "client": "owner", "raw": {"hex": attempt.hex()}}])
        expected["records"].sort(key=lambda row: row["handle"])
        self.assertEqual(self.snapshot(f.store), expected)
        self.assertEqual(f.event["reserved_request_bytes"], 80 * MIB)
        self.assert_refusal("NATIVE_EXECUTION_FORBIDDEN", f.dispatcher.allocate, "submit")
        self.assertEqual(self.snapshot(f.store), expected)
        with patch.object(f.dispatcher, "prepare", self.forbidden), patch.object(f.store, "reserve", self.forbidden):
            self.assertEqual(f.dispatcher.execute(req, raw), reply_raw)
        self.assertTrue(f.event["historical"])
        self.assertEqual(self.snapshot(f.store), expected)
        self.assertFalse(Path(prepared["view"]["directory"]).exists())
        self.notes.update(before=before, after=expected, reply=reply,
                          scope="Mocked view preparation only; actual reservation, commit, terminalization and replay")

    def test_commit_rechecks_custody_foundation_and_exact_selected_row(self):
        for index, field in enumerate(("custody", "foundation", "selected")):
            f = self.fixture("case-" + str(index))
            prepared = deepcopy(self.prepared(f))
            if field == "custody":
                prepared["custody"][0]["sequence"] = True
            elif field == "foundation":
                prepared["view"]["foundation"] = typed(1, 2, 9)
            else:
                prepared["view"]["selected"][0]["publication"] = "publication:" + "0" * 64
            before = self.snapshot(f.store)
            _req, _raw, response = self.dispatch(f, "expose", prepared)
            self.assertEqual(S.decode(response)["code"], "REPLICA_COMMIT_BINDING")
            after = self.snapshot(f.store)
            for table in ("authorization", "owner_grants", "heads", "providers", "snapshots", "entries", "stages"):
                self.assertEqual(after[table], before[table])
            self.assertEqual(after["meta"][0], dict(before["meta"][0], requests=2, charged=144 * MIB, active=None))
            self.assertFalse(any(row["kind"] in {"view", "publication", "artifact"} for row in after["records"]))
            self.assertEqual([row for row in after["records"] if row["kind"] != "attempt"],
                             [row for row in before["records"] if row["kind"] != "attempt"])
        f = self.fixture("origin-changed-after-preparation")
        prepared = deepcopy(self.prepared(f))
        with f.store.transaction():
            f.store.exec("fixture", "UPDATE requests SET raw=? WHERE key=?", (b"{}", f.key))
        _req, _raw, response = self.dispatch(f, "expose", prepared)
        self.assertEqual(S.decode(response)["code"], "REPLICA_REQUEST_BINDING")
        self.assertFalse(any(row["kind"] == "view" for row in self.snapshot(f.store)["records"]))
        self.notes["cases"] = 4

    def test_service_replica_exact_selection_and_absent_source_independence(self):
        f = self.fixture()
        view = self.prepared(f)["view"]
        parsed = {"entries": [f.entry]}
        before = self.snapshot(f.store)
        read_only = self.readonly(f)
        try:
            with patch.object(W, "safe_path", self.forbidden), patch.object(W, "read_local", self.forbidden):
                for control in (f.store, read_only):
                    self.assertIsNone(V.validate_selection(control, f.config, "local", view, parsed, P))
                    cases = []
                    for key, value, code in (("sequence", True, "VIEW_SELECTED_ROW"),
                        ("provider", "P2", "VIEW_SELECTED_ROW"), ("basis", "publication", "VIEW_REPLICA_SELECTION"),
                        ("descriptor_id", typed(0x8111, 3, 9), "VIEW_SELECTED_ENTRY"),
                        ("publication", "publication:" + "0" * 64, "VIEW_SELECTED_ROW")):
                        bad = deepcopy(view)
                        bad["selected"][0][key] = value
                        cases.append((bad, parsed, code))
                    cases.append((dict(view, selected=[]), parsed, "VIEW_SELECTION_COUNT"))
                    cases.append((dict(view, foundation=typed(1, 2, 9)), parsed, "VIEW_REPLICA_ENTRY"))
                    altered_entry = dict(f.entry, bundle_sha256="0" * 64)
                    cases.append((view, {"entries": [altered_entry]}, "VIEW_REPLICA_ENTRY"))
                    doubled = deepcopy(view)
                    doubled["selected"].append(dict(view["selected"][0], sequence=2))
                    cases.append((doubled, {"entries": [f.entry, f.entry]}, "VIEW_REPLICA_SELECTION"))
                    for bad, catalog, code in cases:
                        self.assert_refusal(code, V.validate_selection, control, f.config, "local", bad, catalog, P)
        finally:
            self.close(read_only)
        self.assertEqual(self.snapshot(f.store), before)
        self.notes["scope"] = "Actual ledger selection validator, both store types, 9 negative cases each; no HTTP service startup"

    def test_publication_authority_has_no_custody_fallback(self):
        f = self.fixture()
        view = self.prepared(f)["view"]
        row = {"provider": "P1", "sequence": 1, "descriptor_id": f.entry["descriptor_id"],
               "publication": "publication:" + "0" * 64}
        published_view = dict(view, selected=[row])
        parsed = {"entries": [f.entry]}
        self.assert_refusal("NOT_LOCALLY_PUBLISHED", V.validate_selection,
                            f.store, f.config, "local", published_view, parsed, P)
        req = {"client": "local", "request_id": "ordinary-expose", "op": "expose",
               "args": {"selected": [f.reply["candidate"]]}}
        self.assert_refusal("NOT_LOCALLY_PUBLISHED", f.dispatcher.peer.prepare, req)
        # Synthetic publication row tests only the service ledger branch.
        with f.store.transaction():
            publication = f.store.mark_published("P1", 1, f.entry["descriptor_id"])
        published_view["selected"][0]["publication"] = publication
        self.assert_refusal("VIEW_PUBLICATION_ENTRY", V.validate_selection,
                            f.store, f.config, "local", published_view, parsed, P)
        local_entry = dict(f.entry, manifest_sha256=f.offer["package"]["manifest_sha256"])
        local_parsed = {"entries": [local_entry]}
        read_only = self.readonly(f)
        try:
            self.assertIsNone(V.validate_selection(read_only, f.config, "local", published_view, local_parsed, P))
            wrong = deepcopy(published_view)
            wrong["selected"][0]["publication"] = "publication:" + "0" * 64
            self.assert_refusal("VIEW_PUBLICATION_BINDING", V.validate_selection,
                                read_only, f.config, "local", wrong, local_parsed, P)
            duplicate = dict(published_view, selected=[row, row])
            self.assert_refusal("VIEW_SELECTED_ROW", V.validate_selection, read_only, f.config,
                                "local", duplicate, {"entries": [local_entry, local_entry]}, P)
        finally:
            self.close(read_only)
        self.notes["scope"] = "Synthetic publication bookkeeping only; no accepted or published mathematics claimed"

    def test_replica_peer_recovery_and_ordinary_mode_guard(self):
        self.assertEqual(N.PEER_OPS, {"peer_find", "peer_acquire", "expose", "replica_expose"})
        self.assertEqual(R.RECOVERY_OPERATIONS, {
            "recover_peer": N.PEER_OPS,
            "recover_ordinary": {"info", "find", "preview", "select_context", "admit", "submit", "publish"}})
        f = self.fixture()
        req = {"client": "local", "request_id": "pending", "op": "replica_expose", "args": {"acquisition": f.handle}}
        raw = S.encode(req)
        key = f.store.reserve("local", "pending", raw, grant=80 * MIB)
        selected = {"client": "local", "request_id": "pending", "supervisor_receipt": str(f.origin / "supervisor.json")}
        before = self.snapshot(f.store)
        ev = event()
        response = R.recover(f.store, selected, raw, quiescence(), f.origin, ev, mode="recover_peer")
        self.assertEqual(response, R.INTERRUPTED)
        expected = deepcopy(before)
        expected["meta"][0]["active"] = None
        for row in expected["requests"]:
            if row["key"] == key:
                row.update(phase="terminal", response={"hex": response.hex()})
        self.assertEqual(self.snapshot(f.store), expected)
        self.assertEqual(R.recover(f.store, selected, raw, {}, f.origin, event(), mode="recover_peer"), response)
        self.assertEqual(self.snapshot(f.store), expected)
        other = dict(req, request_id="staged")
        other_raw = S.encode(other)
        other_key = f.store.reserve("local", "staged", other_raw, grant=80 * MIB)
        f.store.stage(other_key, "submit")  # Synthetic charged row, no directory/process.
        staged = self.snapshot(f.store)
        self.assert_refusal("RECOVERY_NATIVE_STAGE_PRESENT", R.recover, f.store,
            dict(selected, request_id="staged"), other_raw, quiescence(), f.origin, event(), mode="recover_peer")
        self.assertEqual(self.snapshot(f.store), staged)
        # The ordinary operation guard precedes pin/command authentication.
        # This fixture intentionally cannot authenticate as a real supervisor.
        calls = f.store.scratch / "calls"
        calls.mkdir()
        origin = calls / "synthetic-receipt"
        origin.mkdir()
        self.save(origin / "request.json", raw)
        command = S.encode({"synthetic_unauthenticated_command": True})
        self.save(origin / "command.json", command)
        receipt = {"schema": 1, "name": origin.name, "status": "TRANSPORT_FAILED",
            "native_acceptance": False, "request_sha256": S.digest(raw), "files": {
                "request.json": {"present": True, "bytes": len(raw), "sha256": S.digest(raw)},
                "command.json": {"present": True, "bytes": len(command), "sha256": S.digest(command)}}}
        self.save(origin / "supervisor.json", S.encode(receipt))
        domains = SimpleNamespace(scratch=f.store.scratch, state=f.store.root, install=INSTALL)
        self.assert_refusal("RECOVERY_ORDINARY_OPERATION_FORBIDDEN", R.authenticate_evidence,
            dict(selected, supervisor_receipt=str(origin / "supervisor.json")), f.config,
            self.root / "absent-config.json", domains, event(), mode="recover_ordinary")
        self.assertEqual(self.snapshot(f.store), staged)
        self.notes.update(scope="Synthetic quiescence, actual pending/replay transitions; ordinary pre-authentication refusal only",
                          before=before, after=expected)

    def files(self, root):
        rows, total = {}, 0
        for number, path in enumerate(root.rglob("*"), 1):
            S.require(number <= 2048, "FIXTURE_ENTRY_BOUND")
            safe(path)
            if path.is_file():
                size = path.stat().st_size
                total += size
                S.require(size <= MIB and total <= 16 * MIB and len(rows) < 512, "FIXTURE_FILE_BOUND")
                raw = S.read(path, MIB)
                rows[path.relative_to(root).as_posix()] = {"bytes": len(raw), "sha256": S.digest(raw)}
        return rows

    def tearDown(self):
        errors = []
        for store in reversed(list(self.stores)):
            try:
                self.close(store)
            except Exception as error:
                errors.append(type(error).__name__ + ":" + str(error)[:256])
        try:
            self.stack.close()
        except Exception as error:
            errors.append(type(error).__name__ + ":" + str(error)[:256])
        imported = {str(Path(module.__file__).resolve()) for module in tuple(sys.modules.values())
                    if getattr(module, "__file__", None) and Path(module.__file__).is_absolute()
                    and Path(module.__file__).resolve().is_relative_to(INSTALL / "py")}
        allowed = {str(INSTALL / "py" / (name + ".py")) for _module, name in MODULES}
        self.assertEqual(imported, allowed)
        report = {"test": self._testMethodName, "synthetic_initialization_and_packages": True,
            "mocked_supply": True, "native_executions": 0, "mathematical_acceptance_claim": False,
            "successful_transport_or_serving_claim": False, "notes": self.notes,
            "imported_product_sources": sorted(imported), "close_errors": errors,
            "fixture_files": self.files(self.root)}
        self.save(self.root / "report.json", S.encode(report))
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()

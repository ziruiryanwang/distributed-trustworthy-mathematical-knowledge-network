"""Focused placement controls: real SQLite/index; explicitly simulated delivery.

Receipt bytes are inert and NEVER verified. No sockets, native checkers, proofs,
frontend, distribution build, old test suite or external fixture is needed.
"""
import asyncio
from contextlib import ExitStack, closing
from copy import deepcopy
from dataclasses import asdict
import hashlib
import importlib
import json
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = Path(__file__).resolve().parents[1]
MAP = PROJECT/"experiments/v5-local-checks/distribution-terminal-i-01-input.json"
MAP_SHA = "d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0"
MAP_BYTES, MIB = 2805479, 1024**2
REPLACEMENTS = {
    "v5/admission/pin_phase.py": ("standalone_validation/admission/pin_phase.py", "ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881"),
    "v5/mixed_claims/imports_atomic.py": ("standalone_validation/mixed_claims/imports_atomic.py", "8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595"),
    "v5/mixed_claims/receiver.py": ("incremental_native/mixed_claims/receiver.py", "5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b"),
    "v5/discovery/discovery_store.py": ("selective_placement/discovery/discovery_store.py", "1c8543d4903754174b80d107ee923116ddb402d41a3b5af3f1d255abdfc6a328"),
}
ADDITIONS = {
    "__init__.py": "8fe08470d7fd15e96d1305f0e49a8b359cb53ce0c542bf7473b68d869159112e",
    "codec.py": "6f32569d4807f96130350b85233161603f6860f082c75f81a8bfacf4f0a58999",
    "ledger.py": "d955990c347ed466617c752893dded8b8494dd266a050b045352c77c48f21a91",
    "controller.py": "ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49",
}
OUTPUT = C = B = F = WV = PC = PL = P = EP = EC = ET = TC = DT = MS = EXPECTED = ENV = None
SOURCES, OBSERVED, FORBIDDEN, LOOP_ERRORS = {}, {}, [], []
IMAGE = "7a"*32
INERT_RECEIPT = b"PLACEMENT-CONTROL-UNVERIFIED-NOT-A-CERTIFICATE"
ENDPOINT = dict(host="127.0.0.1", port=43517, tls=False, server_name=None)
EGRESS = dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
              test_endpoints=[dict(host="127.0.0.1", port=43517)])


def sha(raw): return hashlib.sha256(raw).hexdigest()


def write_new(path, raw):
    with path.open("xb") as stream:
        if stream.write(raw) != len(raw): raise ValueError("CONTROL_SHORT_WRITE")


def stage(output):
    if MAP.stat().st_size != MAP_BYTES: raise ValueError("CURRENT_MAP_SIZE")
    raw = MAP.read_bytes()
    if len(raw) != MAP_BYTES or sha(raw) != MAP_SHA: raise ValueError("CURRENT_MAP_PIN")
    basis = json.loads(raw)["sdk_sources"]
    if len(basis) != 114 or not set(REPLACEMENTS) <= set(basis): raise ValueError("CURRENT_MAP_SHAPE")
    rows = dict(basis)
    for logical, (relative, expected) in REPLACEMENTS.items():
        rows[logical] = dict(path=str(SOURCE/relative), sha256=expected)
    for name, expected in ADDITIONS.items():
        logical = "v5/placement/"+name
        if logical in rows: raise ValueError("FRESH_PLACEMENT_SOURCE_REQUIRED")
        rows[logical] = dict(path=str(SOURCE/"selective_placement/placement"/name), sha256=expected)
    code = output/"selected-code"; code.mkdir()
    for logical, row in sorted(rows.items()):
        path = Path(row["path"])
        if logical not in REPLACEMENTS and not logical.startswith("v5/placement/"):
            path = SOURCE/path.relative_to(PROJECT/"software/v5")
        raw = path.read_bytes()
        if not 0 < len(raw) <= 2*MIB or sha(raw) != row["sha256"] \
                or "bytes" in row and len(raw) != row["bytes"]:
            raise ValueError("SELECTED_SOURCE_PIN:"+logical)
        target = code/logical; target.parent.mkdir(parents=True, exist_ok=True)
        write_new(target, raw)
        if target.read_bytes() != raw: raise ValueError("SELECTED_SOURCE_READBACK")
        SOURCES[logical] = dict(source=str(path), bytes=len(raw), sha256=sha(raw))
    if len(SOURCES) != 118: raise ValueError("EXACT_SELECTED_SOURCE_COUNT")
    if any(name in sys.modules for name in ("placement", "modules", "client", "discovery")):
        raise ValueError("EARLY_PRODUCT_IMPORT")
    sys.path[:0] = [str(code/"v5"), str(code/"portable")]


def forbidden(*args, **kwargs):
    FORBIDDEN.append("FORBIDDEN_PROCESS_SOCKET_OR_VERIFICATION")
    raise AssertionError("FORBIDDEN_PROCESS_SOCKET_OR_VERIFICATION")


def configuration():
    return dict(schema=WV.CONCLUSION_FINGERPRINT_SCHEMA,
        discovery_profile=dict(schema="DMKN_MODULE_EXPORT_CONCLUSION_FINGERPRINT_PROFILE_V1", paths=[[]]),
        wire_profile=EC.public_profile(IMAGE, terminal_i=True), terminal_receipt_bytes=4096,
        module_limits=dict(modules=8, groups=16, declarations=32, bodies=8, logical_bytes=MIB, db_pages=256),
        packet_limits=dict(packets=8, offers=16, offers_per_module=4, packet_bytes=65536,
                           logical_bytes=MIB, db_pages=256),
        index_limits=dict(max_objects=8, max_postings=1024, max_features=128,
                          max_snapshots=16, max_logical_bytes=4*MIB, max_db_pages=2048),
        packet_envelope=asdict(ENV()), max_operations=8, max_report_bytes=MIB, ledger_pages=256)


class Controls(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.root = OUTPUT/("c"+str(SELECTED.index(self._testMethodName)+1).zfill(2)); self.root.mkdir()
        self.serial, self.now = 0, 1800000000000
        self.fixtures, self.delivery, self.exchanges, self.fail_routes = [], None, [], set()
        self.patches = ExitStack()
        self.patches.enter_context(patch.object(PC, "_now_ms", lambda: self.now))
        self.patches.enter_context(patch.object(TC, "exchange", self.exchange))
        self.patches.enter_context(patch.object(DT, "exchange", self.exchange))
        # Asyncio's loop/socketpair exists before setUp; subsequent actual dials are forbidden.
        self.patches.enter_context(patch.object(socket.socket, "__init__", forbidden))
        for name in ("open_connection", "start_server", "create_subprocess_exec", "create_subprocess_shell"):
            self.patches.enter_context(patch.object(asyncio, name, forbidden))

    async def asyncSetUp(self):
        self.loop = asyncio.get_running_loop(); self.old_handler = self.loop.get_exception_handler()
        self.loop.set_exception_handler(lambda unused, context: LOOP_ERRORS.append(
            {"test": self._testMethodName, "message": str(context.get("message", "")),
             "exception": repr(context.get("exception"))}))

    async def asyncTearDown(self):
        try:
            for f in reversed(self.fixtures):
                if not f["controller"].closed: f["controller"].close()
                for source in f.get("sources", ()): source.close()
                if not f["workspace"]._closed: f["workspace"].close()
            OBSERVED.setdefault(self._testMethodName, {})["simulated_exchange_count"] = len(self.exchanges)
        finally:
            self.loop.set_exception_handler(self.old_handler)

    def tearDown(self): self.patches.close()

    def note(self, **values): OBSERVED[self._testMethodName] = values

    def fixture(self, *, body=False, local=False, max_runs=4, calls=128):
        self.serial += 1
        root = self.root/str(self.serial); root.mkdir()
        w = WV.Workspace.open(root/"workspace", configuration(), create=True)
        limits = {name: (16 if name in ("placements", "index_calls", "recovery_passes", "new_cells")
                         else 128 if name == "requests" else 128*MIB) for name in P.RESOURCES}
        cfg = dict(schema=P.CONFIG_SCHEMA, service_epoch=sha((str(root)+"epoch").encode()),
            generation=sha((str(root)+"generation").encode()), namespace=w.adapter.namespace,
            wire_profile_id=w.packets.profile_id, admission_close_ms=self.now+20000,
            retention_not_after_ms=self.now+60000, max_grants=8, max_requests=8,
            max_cells=8, max_runs=max_runs, ledger_pages=256, limits=limits)
        ledger = PL.PlacementLedger.open(w, cfg, create=True)
        controller = PC.PlacementController(ledger, EGRESS)
        service = controller.start_service(wall_seconds=60, controller_cpu_seconds=30, calls=calls)
        token = controller.issue_token(service, ENDPOINT, write_until_ms=self.now+10000,
            retention_until_ms=self.now+50000, limits=limits)
        f = dict(root=root, workspace=w, ledger=ledger, controller=controller, service=service,
                 token=token, config=cfg, limits=limits)
        self.fixtures.append(f)
        name = [["s", "fixture"]]; expr = ["sort", ["zero"]]
        declaration = dict(name=name, kind="definition" if body else "theorem", universes=0,
            type=expr, value_hash=C.body_id(expr, 0) if body else None,
            meta={"hint": "abbrev", "safety": "safe"} if body else {})
        spec = dict(schema=C.SPEC_SCHEMA, foundation=B.FOUNDATION, policy=B.POLICY,
                    groups=[dict(kind="ordinary", declarations=[declaration])])
        module = C.module_id(spec); opening = C.group_opening(spec, 0)
        export = w.adapter.encode_opening(module, name, opening)
        described = w.adapter.describe(export)
        fingerprint = [x for x in described["specs"] if x["tag"] == "conclusion-fingerprint"][0]
        packet = EP.pack_terminal_i(EXPECTED(C.summarize(spec), 0, B.RELATION_IMAGE), INERT_RECEIPT,
                                   aggregate_image=IMAGE, envelope=ENV(), terminal_i=True)
        response = None if not body else dict(schema=MS.BODY_SCHEMA, module_id=module,
            relative_name=name, universes=0, body_hash=declaration["value_hash"], expression=expr)
        value = dict(schema=P.REQUEST_SCHEMA, generation=cfg["generation"], namespace=w.adapter.namespace,
            wire_profile_id=w.packets.profile_id, module_id=module, relative_name=name,
            export_id=C.export_id(module, name), fingerprint=fingerprint, cell=P.cell(w.adapter, fingerprint)[0],
            export_object_sha256=sha(export), export_object_bytes=len(export), opening_max_bytes=4096,
            packet_sha256=sha(packet), packet_bytes=len(packet), bodies=[] if not body else
                [dict(body_hash=response["body_hash"], max_bytes=4096)], retention_end_ms=self.now+40000)
        f.update(name=name, spec=spec, module=module, opening=opening, export=export,
                 packet=packet, body=response, value=value, raw=F.compact(value))
        if local: self.seed(f, group=True, packet=True, body=True)
        return f

    def seed(self, f, *, group=False, packet=False, body=False):
        w = f["workspace"]
        if group: w.modules.put_group(f["module"], f["opening"])
        if packet: w.packets.put(f["module"], f["packet"])
        if body and f["body"] is not None: w.modules.put_body(f["module"], f["name"], f["body"])

    def remote(self, f):
        w = f["workspace"]
        modules = MS.ModuleStore(f["root"]/"source-modules", C, B.FOUNDATION, B.POLICY,
                                 w.config["module_limits"], create=True)
        packets = EC.PacketStore(f["root"]/"source-packets", w.packets.profile, w.config["packet_limits"],
                                envelope=ENV(), terminal_receipt_bytes=4096, create=True)
        f["sources"] = (modules, packets)
        modules.put_group(f["module"], f["opening"]); packets.put(f["module"], f["packet"])
        if f["body"] is not None: modules.put_body(f["module"], f["name"], f["body"])
        f["provider"] = ET.CompositeProvider(index=w.index, custody=modules, packets=packets,
                                             max_requests=8, max_reply_bytes=MIB)
        self.delivery = f

    async def exchange(self, endpoint, route, request, maximum, timeout_ms):
        endpoint.validate()
        f = self.delivery
        self.assertIsNotNone(f, "Unexpected delivery: local-only operation must not fetch")
        # Independent SQLite connection sees the reservation before every simulated effect.
        with closing(sqlite3.connect(f["ledger"]._path)) as observed:
            row = observed.execute("SELECT phase,reservation FROM requests").fetchall()
            self.assertEqual(len(row), 1)
            self.assertEqual(row[0][0], "PULLING")
            self.assertEqual(json.loads(row[0][1])["placements"], 1)
        self.exchanges.append(route)
        if route in self.fail_routes: raise ValueError("INJECTED_DELIVERY_FAILURE")
        response = f["provider"].dispatch(route, deepcopy(request), check_budget=endpoint.validate)
        raw = response if type(response) is bytes else F.compact(response)
        self.assertLessEqual(len(raw), maximum)
        return dict(status=200, raw=raw, request_bytes=len(F.compact(request)), reply_bytes=len(raw),
                    header_bytes=0, elapsed_ms=0)  # Simulated transport accounting, not wire measurements.

    async def submit(self, f, raw=None, token=None):
        return await f["controller"].submit(f["service"], f["token"]["token"] if token is None else token,
                                             f["raw"] if raw is None else raw)

    def rid(self, f, raw=None, token=None):
        grant = f["token"]["grant_id"] if token is None else sha(token.encode())
        return P.request_id(f["raw"] if raw is None else raw, grant, f["config"]["generation"])

    def used(self, f):
        return json.loads(f["ledger"].db.execute("SELECT used FROM meta WHERE id=1").fetchone()[0])

    def restart(self, f):
        f["controller"].close()
        ledger = PL.PlacementLedger.open(f["workspace"], f["config"])
        controller = PC.PlacementController(ledger, EGRESS)
        f.update(ledger=ledger, controller=controller)
        f["service"] = controller.start_service(wall_seconds=60, controller_cpu_seconds=30, calls=128)

    async def test_reserved_pull_custody_and_index(self):
        f = self.fixture(body=True); self.remote(f)
        result = await self.submit(f)
        self.assertEqual(result["phase"], "RECEIPT_COMMITTED")
        out = result["outcome"]
        self.assertEqual(out["status"], "INDEXED_UNADVERTISED")
        self.assertEqual(out["route"]["status"], "INTENT_ONLY")
        self.assertEqual(out["route"]["cell"], f["value"]["cell"])
        self.assertEqual(out["route"]["stripe"], 0)
        self.assertEqual(self.exchanges, ["/v5/modules/group", DT.OFFER_ROUTE, DT.PACKET_ROUTE, "/v5/modules/body"])
        self.assertEqual(f["workspace"].index.status()["objects"], 1)
        self.assertEqual(out["observed"]["acquisition"]["budget"]["used"]["verify_attempts"], 0)
        for key in P.FLAGS: self.assertFalse(out[key])
        self.assertNotIn(f["token"]["token"].encode(), f["ledger"]._path.read_bytes())
        self.note(real_custody_commits=True, real_index=True, mathematical_acceptance=False)

    async def test_duplicate_request_expiry_and_restart_are_observational(self):
        f = self.fixture(local=True)
        first = await self.submit(f); used = self.used(f)
        self.now += 11000
        for restarted in (False, True):
            if restarted: self.restart(f)
            with patch.object(f["controller"], "_local_group", side_effect=AssertionError("DUPLICATE_READBACK")), \
                    patch.object(f["workspace"].index, "admit", side_effect=AssertionError("DUPLICATE_INDEX")):
                self.assertEqual(await self.submit(f), first)
                self.assertEqual(f["controller"].status(f["service"], f["token"]["token"], self.rid(f)), first)
            changed = {**f["value"], "retention_end_ms": f["value"]["retention_end_ms"]-1}
            with self.assertRaisesRegex(ValueError, "TOKEN_STATUS_ONLY"):
                await self.submit(f, F.compact(changed))
            self.assertEqual(self.used(f), used)
        self.assertEqual(len(self.exchanges), 0)
        self.assertEqual(f["ledger"].db.execute("SELECT count(*) FROM requests").fetchone()[0], 1)

    async def test_distinct_request_same_content_deduplicates_locally(self):
        f = self.fixture(local=True)
        first = await self.submit(f); w = f["workspace"]
        before = (w.modules.status(), w.packets.status(), w.index.status())
        token = f["controller"].issue_token(f["service"], ENDPOINT, write_until_ms=self.now+10000,
            retention_until_ms=self.now+50000, limits=f["limits"])["token"]
        with patch.object(w.modules, "get_group", wraps=w.modules.get_group) as readback:
            second = await self.submit(f, token=token)
            self.assertGreater(readback.call_count, 0)
        self.assertNotEqual(first["request_id"], second["request_id"])
        self.assertEqual(before, (w.modules.status(), w.packets.status(), w.index.status()))
        self.assertEqual(self.used(f)["placements"], 2)
        self.assertEqual(self.used(f)["new_cells"], 1)
        self.assertEqual(second["outcome"]["observed"]["new_store_logical_bytes"], dict(modules=0, packets=0, index=0))
        self.assertFalse(self.exchanges)

    async def test_corrupt_local_group_packet_and_body_never_refetch(self):
        for kind in ("group", "packet", "body"):
            with self.subTest(kind=kind):
                f = self.fixture(body=True, local=True); w = f["workspace"]
                if kind == "group": w.modules.db.execute("UPDATE groups SET opening=?", (b"!",))
                elif kind == "packet": w.packets.db.execute("UPDATE packets SET blob=?", (b"!"*len(f["packet"]),))
                else: w.modules.db.execute("UPDATE bodies SET expression=?", (b"!",))
                with self.assertRaises(ValueError): await self.submit(f)
                self.assertEqual(w.index.status()["objects"], 0)
                self.assertEqual(f["ledger"].request(self.rid(f))["phase"], "INCOMPLETE")
                self.assertEqual(self.used(f)["placements"], 1)
        self.assertFalse(self.exchanges)

    async def test_namespace_cell_fingerprint_and_target_bindings(self):
        f = self.fixture(local=True)
        for field in ("namespace", "wire_profile_id", "generation", "cell"):
            bad = {**f["value"], field: "01"*32}
            with self.subTest(field=field), self.assertRaises(ValueError): await self.submit(f, F.compact(bad))
        self.assertEqual(self.used(f)["placements"], 0)
        fingerprint = {**f["value"]["fingerprint"], "value": "02"*32}
        bad = {**f["value"], "fingerprint": fingerprint,
               "cell": P.cell(f["workspace"].adapter, fingerprint)[0]}
        with self.assertRaisesRegex(ValueError, "DERIVED_FINGERPRINT"): await self.submit(f, F.compact(bad))
        other = self.fixture(body=True, local=True)
        f["workspace"].packets.put(other["module"], other["packet"])
        crossed = {**f["value"], "packet_sha256": sha(other["packet"]), "packet_bytes": len(other["packet"])}
        with self.assertRaisesRegex(ValueError, "TARGET_BINDING"): await self.submit(f, F.compact(crossed))
        self.assertEqual(f["workspace"].index.status()["objects"], 0)
        self.assertFalse(self.exchanges)

    async def test_store_guard_on_fresh_and_duplicate_commit(self):
        f = self.fixture(); index = f["workspace"].index; before = index.status(); calls = []
        def deny():
            self.assertTrue(index.db.in_transaction); calls.append(True)
            raise ValueError("INJECTED_BEFORE_COMMIT")
        with self.assertRaisesRegex(ValueError, "INJECTED_BEFORE_COMMIT"):
            index.admit(f["export"], f["value"]["export_id"], before_commit=deny)
        self.assertEqual(index.status(), before); self.assertFalse(index.db.in_transaction)
        admitted = index.admit(f["export"], f["value"]["export_id"])
        before = index.status()
        with self.assertRaisesRegex(ValueError, "INJECTED_BEFORE_COMMIT"):
            index.admit(f["export"], f["value"]["export_id"], before_commit=deny)
        self.assertEqual(index.status(), before); self.assertFalse(index.db.in_transaction)
        self.assertEqual(index._record(admitted["record_id"]), admitted["record"])
        self.assertEqual(len(calls), 2)

    async def test_partial_index_commit_one_prepaid_local_recovery(self):
        f = self.fixture(local=True)
        with patch.object(f["ledger"], "finish", side_effect=ValueError("INJECTED_POST_INDEX_FAILURE")):
            with self.assertRaisesRegex(ValueError, "INJECTED_POST_INDEX_FAILURE"): await self.submit(f)
        used = self.used(f); index = f["workspace"].index.status()
        self.assertEqual(index["objects"], 1)
        self.assertEqual(f["ledger"].request(self.rid(f))["phase"], "INCOMPLETE")
        self.now += 21000  # Both token write and admission expired; retention remains original.
        with patch.object(PC, "_OwnedAcquisition", side_effect=AssertionError("RECOVERY_MUST_BE_LOCAL")):
            result = await f["controller"].reconcile(f["service"], self.rid(f))
            again = await f["controller"].reconcile(f["service"], self.rid(f))
        self.assertEqual(result, again)
        self.assertTrue(result["recovery_used"]); self.assertTrue(result["outcome"]["recovery"])
        self.assertEqual(result["outcome"]["retention_end_ms"], f["value"]["retention_end_ms"])
        self.assertEqual(self.used(f), used); self.assertEqual(f["workspace"].index.status(), index)
        self.assertIsNone(result["outcome"]["observed"]["acquisition"])
        self.assertFalse(self.exchanges)

    async def test_failed_recovery_consumes_slot_without_network_or_reset(self):
        f = self.fixture(); self.remote(f); self.fail_routes.add(DT.OFFER_ROUTE)
        with self.assertRaisesRegex(ValueError, "INJECTED_DELIVERY_FAILURE"): await self.submit(f)
        used = self.used(f); count = len(self.exchanges)
        self.assertEqual(f["workspace"].modules.status()["counts"]["groups"], 1)
        with patch.object(PC, "_OwnedAcquisition", side_effect=AssertionError("RECOVERY_NETWORK")):
            with self.assertRaisesRegex(ValueError, "RECOVERY_PACKET_NOT_RETAINED"):
                await f["controller"].reconcile(f["service"], self.rid(f))
            self.seed(f, packet=True)
            with self.assertRaisesRegex(ValueError, "RECOVERY_EXHAUSTED"):
                await f["controller"].reconcile(f["service"], self.rid(f))
        row = f["ledger"].request(self.rid(f))
        self.assertTrue(row["recovery_used"]); self.assertEqual(row["phase"], "RECOVERY_INCOMPLETE")
        self.assertEqual(self.used(f), used); self.assertEqual(len(self.exchanges), count)
        self.assertEqual(f["workspace"].index.status()["objects"], 0)

    async def test_original_guard_reaches_each_nested_custody_commit(self):
        for kind in ("group", "packet", "body"):
            with self.subTest(kind=kind):
                f = self.fixture(body=True); self.remote(f); w = f["workspace"]
                owner, method = ((w.modules, "put_group") if kind == "group" else
                                 (w.packets, "put") if kind == "packet" else (w.modules, "put_body"))
                original = getattr(owner, method); hooks = []
                def crossed(*args, **kwargs):
                    guard = kwargs["before_commit"]
                    def expire():
                        hooks.append(owner.db.in_transaction)
                        self.now = f["token"]["write_until_ms"]
                        guard()
                    kwargs["before_commit"] = expire
                    return original(*args, **kwargs)
                with patch.object(owner, method, crossed):
                    with self.assertRaisesRegex(ValueError, "WRITE_OR_ADMISSION_EXPIRED"): await self.submit(f)
                self.assertEqual(hooks, [True]); self.assertFalse(owner.db.in_transaction)
                key = "groups" if kind == "group" else "bodies"
                counts = w.packets.status()["counts"] if kind == "packet" else w.modules.status()["counts"]
                self.assertEqual(counts["packets" if kind == "packet" else key], 0)
                self.assertEqual(w.index.status()["objects"], 0)
                self.assertEqual(self.used(f)["placements"], 1)

    async def test_cleanup_failure_propagates_with_historical_state(self):
        for initial_error in (False, True):
            with self.subTest(initial_error=initial_error):
                f = self.fixture(local=not initial_error)
                if initial_error:
                    self.remote(f); self.fail_routes.add(DT.OFFER_ROUTE)
                original = PC._OwnedAcquisition.close
                def close_failed(acquisition):
                    original(acquisition)
                    raise ValueError("INJECTED_CLOSE_FAILURE")
                with patch.object(PC._OwnedAcquisition, "close", close_failed):
                    with self.assertRaises(PC.PlacementCleanupError) as raised: await self.submit(f)
                error = raised.exception
                self.assertEqual(error.request_id, self.rid(f))
                self.assertEqual(error.receipt_committed, not initial_error)
                self.assertEqual(error.original_error is not None, initial_error)
                self.assertIsInstance(error.__cause__, ValueError)
                self.assertTrue(f["service"].closed)
                phase = f["ledger"].request(self.rid(f))["phase"]
                self.assertEqual(phase, "INCOMPLETE" if initial_error else "RECEIPT_COMMITTED")
                with self.assertRaisesRegex(ValueError, "LIVE_SERVICE_GRANT"):
                    f["controller"].status(f["service"], f["token"]["token"], self.rid(f))

    async def test_original_funding_calls_runtime_and_retention_caps(self):
        f = self.fixture()
        zero = {**f["limits"], "storage_bytes": 0}
        token = f["controller"].issue_token(f["service"], ENDPOINT, write_until_ms=self.now+10000,
            retention_until_ms=self.now+50000, limits=zero)["token"]
        with self.assertRaisesRegex(ValueError, "RESERVED_CAP:storage_bytes"): await self.submit(f, token=token)
        self.assertEqual(self.used(f)["placements"], 0)
        capped = self.fixture(calls=1)
        with self.assertRaisesRegex(ValueError, "SERVICE_CALL_CAP"): await self.submit(capped)
        self.assertEqual(self.used(capped)["placements"], 0)
        with patch.object(PC.time, "process_time", return_value=f["service"].started_cpu+31):
            with self.assertRaisesRegex(ValueError, "SERVICE_RESOURCE_LIMIT"): await self.submit(f)
        with patch.object(PC.time, "monotonic", return_value=f["service"].deadline):
            with self.assertRaisesRegex(ValueError, "SERVICE_RESOURCE_LIMIT"): await self.submit(f)
        once = self.fixture(max_runs=1)
        with self.assertRaisesRegex(ValueError, "RUNTIME_CAP"): self.restart(once)
        self.now = f["value"]["retention_end_ms"]
        with self.assertRaises(ValueError): await self.submit(f)
        self.assertEqual(self.used(f)["placements"], 0)
        self.assertFalse(self.exchanges)

    async def test_seal_and_exact_owner_registration(self):
        f = self.fixture(local=True)
        with self.assertRaisesRegex(ValueError, "LEDGER_ALREADY_OPEN"):
            PL.PlacementLedger.open(f["workspace"], f["config"])
        with self.assertRaisesRegex(ValueError, "CONTROLLER_ALREADY_OPEN"):
            PC.PlacementController(f["ledger"], EGRESS)
        first = await self.submit(f); used = self.used(f)
        f["controller"].seal(f["service"])
        self.assertEqual(await self.submit(f), first)
        changed = {**f["value"], "retention_end_ms": f["value"]["retention_end_ms"]-1}
        with self.assertRaisesRegex(ValueError, "GENERATION_SEALED"): await self.submit(f, F.compact(changed))
        self.assertEqual(self.used(f), used)
        self.assertEqual(f["ledger"].db.execute("SELECT state FROM meta").fetchone()[0], "SEALED_SERVING")
        self.assertFalse(self.exchanges)


SELECTED = (
    "test_reserved_pull_custody_and_index",
    "test_duplicate_request_expiry_and_restart_are_observational",
    "test_distinct_request_same_content_deduplicates_locally",
    "test_corrupt_local_group_packet_and_body_never_refetch",
    "test_namespace_cell_fingerprint_and_target_bindings",
    "test_store_guard_on_fresh_and_duplicate_commit",
    "test_partial_index_commit_one_prepaid_local_recovery",
    "test_failed_recovery_consumes_slot_without_network_or_reset",
    "test_original_guard_reaches_each_nested_custody_commit",
    "test_cleanup_failure_propagates_with_historical_state",
    "test_original_funding_calls_runtime_and_retention_caps",
    "test_seal_and_exact_owner_registration",
)


def main():
    global OUTPUT,C,B,F,WV,PC,PL,P,EP,EC,ET,TC,DT,MS,EXPECTED,ENV
    if len(sys.argv) != 3 or sys.argv[1] != "--output": raise ValueError("OUTPUT_REQUIRED")
    OUTPUT = Path(sys.argv[2])
    if not OUTPUT.is_absolute() or not OUTPUT.is_dir() or not OUTPUT.is_relative_to(PROJECT):
        raise ValueError("CANONICAL_EXISTING_OUTPUT")
    if not (os.name == "nt" and sys.flags.isolated and sys.flags.no_site
            and sys.dont_write_bytecode and not sys.flags.optimize): raise ValueError("ISOLATED_WINDOWS")
    stage(OUTPUT)
    with ExitStack() as guards:
        guards.enter_context(patch.object(subprocess, "Popen", forbidden))
        guards.enter_context(patch.object(os, "system", forbidden))
        C = importlib.import_module("modules.codec"); B = importlib.import_module("aggregate_claims.bindings")
        F = importlib.import_module("discovery.formal_features")
        WV = importlib.import_module("client.workspace_evidence")
        PC = importlib.import_module("placement.controller"); PL = importlib.import_module("placement.ledger")
        P = importlib.import_module("placement.codec"); EP = importlib.import_module("evidence_network.packet")
        EC = importlib.import_module("evidence_network.custody"); ET = importlib.import_module("evidence_network.transport")
        TC = importlib.import_module("transport.clients"); DT = importlib.import_module("delta.transport")
        MS = importlib.import_module("custody.module_store")
        EXPECTED = importlib.import_module("delta_claims.claims").expected_journal
        ENV = importlib.import_module("mixed_claims.packet").Envelope
        for module, name in (("admission.verifier", "ReceiptVerifier"),
                             ("aggregate_claims.aggregate_admission", "AggregateReceiptVerifier"),
                             ("mixed_claims.receiver", "MixedDeltaVerifier")):
            guards.enter_context(patch.object(getattr(importlib.import_module(module), name), "receive", forbidden))
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
    passed = result.wasSuccessful() and result.testsRun == len(SELECTED) and not result.skipped \
             and not FORBIDDEN and not LOOP_ERRORS
    report = dict(schema="DMKN_SELECTIVE_PLACEMENT_CONTROLS_V1", status="PASS" if passed else "FAIL",
        selected=list(SELECTED), tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
        skipped=len(result.skipped), observations=OBSERVED, sources=SOURCES,
        forbidden_calls=FORBIDDEN, loop_errors=LOOP_ERRORS, actual_network_calls=0,
        actual_native_calls=0, actual_proof_calls=0, mathematical_acceptance=False,
        transport="SIMULATED_EXCHANGE_REAL_PROVIDER_DISPATCH_AND_STRUCTURAL_CUSTODY",
        receipt_bytes="INERT_UNVERIFIED_FIXTURES_NEVER_ADMITTED",
        fault_injections="CLOCK_HORIZONS_PRECOMMIT_CRASH_CORRUPTION_AND_CLOSE_FAILURE",
        scope="OWNER_LOCAL_RESERVATION_CUSTODY_INDEX_RECOVERY_NOT_HTTP_OR_GLOBAL_PLACEMENT")
    write_new(OUTPUT/"placement-controls-result.json", json.dumps(report, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode()+b"\n")
    return 0 if passed else 1


if __name__ == "__main__": raise SystemExit(main())

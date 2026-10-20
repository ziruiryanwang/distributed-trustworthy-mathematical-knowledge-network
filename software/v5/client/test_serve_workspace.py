"""Finite retained-workspace service controls, not mathematical qualification.

Fixtures are fresh real stores containing one explicitly synthetic structural
descriptor. No saved acceptance report, receipt owner, native checker, prover or
old test suite is loaded. Only the selected ordinary service entry is exercised.
"""
import argparse
import asyncio
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE/"portable_runtime"), str(SOURCE)]
from aggregate_claims import bindings as B
from client import serve_workspace as S
from client import workspace_atomic as WA
from client import workspace_mixed as WM
from client import workspace_evidence as WE
from client import workspace_staged as WS
from client import workspace_validated as WV
from discovery import formal_features as F
from discovery.module_export_adapter import compile_query
from evidence_network import custody as EC
from evidence_network import transport as ET
from frontier_network import custody as IC
from frontier_network import transport as IT
from mixed_claims.packet import Envelope
from mixed_network import custody as MC
from mixed_network import transport as MT
from modules import codec as C
from transport import http_provider_receipts as H

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
IMAGE = "81"*32
OUTPUT = None
OBSERVED = {"loopback_exchanges": 0, "successful_service_lifetimes": 0,
            "synthetic_workspaces": 0, "injected_lifecycle_faults": 0}
MODES = {
    "atomic": (WA.Workspace, IT.CompositeProvider),
    "mixed": (WM.Workspace, MT.CompositeProvider),
    "evidence": (WE.Workspace, ET.CompositeProvider),
    "staged": (WS.Workspace, ET.CompositeProvider),
    "validated": (WV.Workspace, ET.CompositeProvider),
}


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def configuration(mode="atomic"):
    value = {
        "schema": WA.SCHEMA, "wire_profile": IC.public_profile(),
        "module_limits": dict(modules=8, groups=16, declarations=32, bodies=8,
                              logical_bytes=MIB, db_pages=256),
        "packet_limits": dict(packets=8, offers=16, offers_per_module=4,
                             packet_bytes=65536, logical_bytes=MIB, db_pages=256),
        "index_limits": dict(max_objects=8, max_postings=1024, max_features=128,
                            max_snapshots=16, max_logical_bytes=4*MIB, max_db_pages=2048),
        "packet_envelope": asdict(Envelope()),
        "max_operations": 8, "max_report_bytes": MIB, "ledger_pages": 256,
    }
    if mode == "mixed":
        value.update(schema=WM.SCHEMA, wire_profile=MC.public_profile(IMAGE))
    elif mode in ("evidence", "staged", "validated"):
        value.update(schema=WE.SCHEMA, wire_profile=EC.public_profile(IMAGE),
                     terminal_receipt_bytes=65536)
    return value


class ServingControls(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.root = OUTPUT/self._testMethodName
        self.root.mkdir()
        self.tasks = []
        self.opened = []

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)
        for workspace in reversed(self.opened):
            if not workspace._closed:
                workspace.close()

    def fixture(self, mode="atomic", *, name="fixture"):
        """Data-only descriptor deliberately has no mathematical warrant."""
        config = configuration(mode)
        root = self.root/name
        root.mkdir()
        workspace = MODES[mode][0].open(root/"workspace", config, create=True)
        self.opened.append(workspace)
        relative_name = [["s", "syntheticServingDescriptor"]]
        spec = {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
                "groups": [{"kind": "ordinary", "declarations": [{
                    "kind": "theorem", "name": relative_name, "universes": 0,
                    "type": ["sort", ["zero"]], "value_hash": None, "meta": {}}]}]}
        module, opening = C.module_id(spec), C.group_opening(spec, 0)
        workspace.modules.put_group(module, opening)
        raw = workspace.adapter.encode_opening(module, relative_name, opening)
        described = workspace.adapter.describe(raw)
        self.assertFalse(described["mathematical_acceptance"])
        workspace.index.admit(raw, expected_id=C.export_id(module, relative_name))
        namespace = workspace.adapter.namespace
        workspace.close()
        OBSERVED["synthetic_workspaces"] += 1
        return SimpleNamespace(root=root/"workspace", config=config, module=module,
            opening=opening, name=relative_name, raw=raw, record=described["record"],
            namespace=namespace, mode=mode)

    def context(self, fixture, *, name="operation", lifetime=1):
        root = self.root/name
        root.mkdir()
        installation, run = root/"installation", root/"run"
        installation.mkdir()
        run.mkdir()
        work = run/"work"
        work.mkdir()
        portable = SOURCE/"portable_runtime"
        owner = root/"owner"
        owner.mkdir()
        started = time.monotonic()
        context = SimpleNamespace(
            installation=installation, workspace_root=root, run=run,
            location_workspace=work, sources_v5=SOURCE, sources_portable=portable,
            sources_owner=owner, started=started, deadline=started+30,
            limits={"wall_seconds": 30, "cpu_seconds": 20, "memory_mib": 256},
            parameters={
                "schema": "DMKN_V5_WORKSPACE_SERVICE_V1", "mode": fixture.mode,
                "workspace_path": str(fixture.root), "workspace_config": deepcopy(fixture.config),
                "bind": {"host": "127.0.0.1", "port": 0}, "tls": None,
                "service_limits": {"max_connections": 2, "max_requests": 8,
                    "max_reply_bytes": 32*MIB, "operation_ms": 1000,
                    "lifetime_seconds": lifetime}},
            source_sha256={"v5/client/serve_workspace.py": pin(SOURCE/"client/serve_workspace.py")["sha256"]})

        def remaining():
            value = int(context.deadline-time.monotonic())
            if value < 1:
                raise ValueError("CLIENT_ORIGINAL_DEADLINE_EXHAUSTED")
            return value
        context.remaining_seconds = remaining
        return context

    async def invoke(self, context):
        return await asyncio.wait_for(S.serve(context), timeout=5)

    def saved(self, context):
        return json.loads((context.location_workspace/"service-result.json").read_bytes())

    def reopen(self, fixture):
        workspace = MODES[fixture.mode][0].open(fixture.root, fixture.config, create=False)
        self.opened.append(workspace)
        self.assertEqual(workspace.modules.get_group(fixture.module, fixture.name)[0],
                         fixture.opening)
        self.assertEqual(workspace.adapter.describe(fixture.raw)["record"], fixture.record)
        held = workspace.index.db.execute("SELECT record FROM objects WHERE object_id=?",
                                           (fixture.record["object_id"],)).fetchone()
        self.assertIsNotNone(held)
        self.assertEqual(F.strict(bytes(held[0]), 65536), fixture.record)
        self.assertFalse(workspace.status()["mathematical_acceptance"])
        workspace.close()

    async def ready(self, context, task):
        path = context.location_workspace/"service-ready.json"
        until = time.monotonic()+3
        while not path.exists():
            if task.done():
                self.fail("Service terminated before ready: "+str(task.result()))
            self.assertLess(time.monotonic(), until, "SERVICE_READY_TIMEOUT")
            await asyncio.sleep(0.005)
        return json.loads(path.read_bytes())

    async def exchange(self, endpoint, route, request, maximum=65536):
        response = await H.exchange(endpoint, route, request, maximum, 1000)
        OBSERVED["loopback_exchanges"] += 1
        self.assertEqual(response["status"], 200)
        return F.strict(response["raw"], maximum)

    async def assert_listener_closed(self, endpoint):
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(endpoint.host, endpoint.port), 0.5)
        except OSError:
            return
        writer.close()
        await writer.wait_closed()
        self.fail("SERVICE_LISTENER_REMAINS_OPEN")

    def assert_failed(self, report, reason=None):
        self.assertTrue(report["status"].startswith("FAIL"), report)
        self.assertFalse(report["mathematical_acceptance"])
        if reason is not None:
            self.assertIn(reason, str(report))

    async def test_existing_data_offer_group_finite_stop_and_reopen(self):
        fixture = self.fixture()
        for number in range(2):
            context = self.context(fixture, name="service-"+str(number))
            task = asyncio.create_task(S.serve(context))
            self.tasks.append(task)
            ready = await self.ready(context, task)
            self.assertFalse(ready["mathematical_acceptance"])
            endpoint = H.Endpoint(**ready["endpoint"])
            endpoint.validate()
            features = compile_query(fixture.namespace, [
                {"tag": "declaration-kind", "value": "theorem"},
                {"tag": "result-head", "head": {"tag": "sort"}}])
            offer = await self.exchange(endpoint, H.OFFER_ROUTE, {
                "namespace": fixture.namespace, "features": features,
                "max_bytes": 65536, "max_expanded_bytes": 65536})
            self.assertEqual(offer["status"], "OFFERED")
            self.assertEqual(offer["features"], features)
            self.assertFalse(offer["global_complete"])
            self.assertFalse(offer["mathematical_acceptance"])
            opening = await self.exchange(endpoint, "/v5/modules/group", {
                "module_id": fixture.module, "relative_name": fixture.name, "group_index": 0})
            self.assertEqual(opening, fixture.opening)
            C.verify_group_opening(fixture.module, opening)
            report = await asyncio.wait_for(task, 4)
            self.assertEqual(report["status"], "PASS", report)
            self.assertFalse(report["mathematical_acceptance"])
            self.assertTrue(report["cleanup"]["workspace_closed"])
            self.assertTrue(report["cleanup"]["http_closed"])
            self.assertEqual(report["cleanup"]["errors"], [])
            self.assertEqual(report["counters"]["requests"], 2)
            self.assertEqual(report["counters"]["failures"], 0)
            self.assertEqual(report["counters"]["reserved_reply_bytes"], 0)
            self.assertEqual(report["counters"]["active"], 0)
            self.assertEqual(report["service_limits"], context.parameters["service_limits"])
            self.assertEqual(report["deadline"], report["started"]+1)
            self.assertGreaterEqual(report["finished"], report["deadline"])
            self.assertLess(report["finished"], report["outer_deadline"])
            self.assertEqual(self.saved(context), report)
            await self.assert_listener_closed(endpoint)
            self.reopen(fixture)
            OBSERVED["successful_service_lifetimes"] += 1

    async def test_missing_workspace_is_never_created(self):
        fixture = self.fixture()
        context = self.context(fixture)
        absent = self.root/"missing-workspace"
        context.parameters["workspace_path"] = str(absent)
        with patch.object(IT.CompositeProvider, "start",
                          side_effect=AssertionError("START_MUST_NOT_RUN")) as start:
            with self.assertRaises(FileNotFoundError):
                await self.invoke(context)
        self.assertFalse(absent.exists())
        self.assertFalse(start.called)
        self.assertFalse((context.location_workspace/"service-ready.json").exists())

    async def test_configuration_and_mode_mismatch_refuse_without_migration(self):
        fixture = self.fixture()
        for number, change in enumerate(("config", "mode", "unknown-mode")):
            context = self.context(fixture, name="refusal-"+str(number))
            if change == "config":
                context.parameters["workspace_config"]["max_operations"] += 1
            else:
                context.parameters["mode"] = "evidence" if change == "mode" else "unknown"
            with patch.object(H.Provider, "start",
                              side_effect=AssertionError("START_MUST_NOT_RUN")) as start:
                if change == "unknown-mode":
                    with self.assertRaisesRegex(ValueError, "SERVICE_MODE"):
                        await self.invoke(context)
                else:
                    report = await self.invoke(context)
                    self.assert_failed(report)
            self.assertFalse(start.called)
            self.reopen(fixture)

    async def test_all_explicit_modes_select_exact_existing_store_provider(self):
        observed = []
        for mode, (workspace_class, provider_class) in MODES.items():
            fixture = self.fixture(mode, name="fixture-"+mode)
            context = self.context(fixture, name="service-"+mode)

            async def stop_before_bind(provider, *args, **kwargs):
                observed.append((mode, type(provider), type(provider.packets)))
                OBSERVED["injected_lifecycle_faults"] += 1
                raise ValueError("INERT_SELECTED_MODE_BEFORE_BIND")

            with patch.object(provider_class, "start", stop_before_bind):
                report = await self.invoke(context)
            self.assert_failed(report, "INERT_SELECTED_MODE_BEFORE_BIND")
            self.assertEqual(observed[-1][1], provider_class)
            expected_packets = (IC.PacketStore if mode == "atomic" else
                                MC.PacketStore if mode == "mixed" else EC.PacketStore)
            self.assertEqual(observed[-1][2], expected_packets)
            self.assertTrue(report["cleanup"]["workspace_closed"])
            self.assertEqual(report["cleanup"]["errors"], [])
            self.reopen(fixture)
        self.assertEqual([row[0] for row in observed], list(MODES))

    async def test_nonloopback_without_tls_and_unbounded_limits_refuse_before_open(self):
        fixture = self.fixture()
        for number, change in enumerate(("remote-http", "lifetime", "requests")):
            context = self.context(fixture, name="refusal-"+str(number))
            if change == "remote-http":
                context.parameters["bind"]["host"] = "192.0.2.1"
            elif change == "lifetime":
                context.parameters["service_limits"]["lifetime_seconds"] = 0
            else:
                context.parameters["service_limits"]["max_requests"] = 0
            with patch.object(WA.Workspace, "open",
                              side_effect=AssertionError("OPEN_MUST_NOT_RUN")) as opened:
                reason = {"remote-http": "SERVICE_BIND_POLICY",
                          "lifetime": "SERVICE_LIFETIME",
                          "requests": "SERVICE_LIMIT:max_requests"}[change]
                with self.assertRaisesRegex(ValueError, reason):
                    await self.invoke(context)
            self.assertFalse(opened.called)
        self.reopen(fixture)

    async def test_output_source_and_installation_overlap_refuse_before_open(self):
        fixture = self.fixture()
        for number, target in enumerate(("output", "source", "installation")):
            context = self.context(fixture, name="overlap-"+str(number))
            if target == "output":
                context.location_workspace = fixture.root
            elif target == "source":
                context.sources_v5 = fixture.root
            else:
                context.installation = fixture.root
            with patch.object(WA.Workspace, "open",
                              side_effect=AssertionError("OPEN_MUST_NOT_RUN")) as opened:
                with self.assertRaisesRegex(ValueError, "SERVICE_OUTPUT_SCOPE|SERVICE_WORKSPACE_DISJOINT"):
                    await self.invoke(context)
            self.assertFalse(opened.called)
            self.assertFalse((fixture.root/"service-ready.json").exists())
            self.assertFalse((fixture.root/"service-result.json").exists())
        self.reopen(fixture)

    async def test_partial_bind_failure_stops_listener_and_releases_workspace(self):
        fixture = self.fixture()
        context = self.context(fixture)
        held = {}
        original = IT.CompositeProvider.start

        async def fail_after_bind(provider, *args, **kwargs):
            held["provider"] = provider
            held["endpoint"] = await original(provider, *args, **kwargs)
            OBSERVED["injected_lifecycle_faults"] += 1
            raise ValueError("INERT_FAILURE_AFTER_REAL_BIND")

        with patch.object(IT.CompositeProvider, "start", fail_after_bind):
            report = await self.invoke(context)
        self.assert_failed(report, "INERT_FAILURE_AFTER_REAL_BIND")
        self.assertTrue(report["cleanup"]["workspace_closed"])
        self.assertEqual(report["cleanup"]["errors"], [])
        self.assertIsNone(held["provider"].server)
        self.assertFalse(held["provider"].tasks)
        endpoint = held["endpoint"]
        await self.assert_listener_closed(endpoint)
        self.reopen(fixture)

    async def test_stop_fault_preserves_primary_error_and_attempts_workspace_cleanup(self):
        fixture = self.fixture()
        context = self.context(fixture)
        held = {}
        original_start = IT.CompositeProvider.start

        async def fail_after_bind(provider, *args, **kwargs):
            held["provider"] = provider
            endpoint = await original_start(provider, *args, **kwargs)
            held["endpoint"] = endpoint
            held["reader"], held["writer"] = await asyncio.wait_for(
                asyncio.open_connection(endpoint.host, endpoint.port), 1)
            until = time.monotonic()+1
            while not provider.tasks:
                self.assertLess(time.monotonic(), until, "INERT_HANDLER_DID_NOT_START")
                await asyncio.sleep(0.005)
            held["active_before_fault"] = len(provider.tasks)
            raise ValueError("INERT_PRIMARY_START_FAILURE")

        async def stop_before_any_cleanup(provider):
            OBSERVED["injected_lifecycle_faults"] += 1
            raise ValueError("INERT_STOP_CLEANUP_FAILURE")

        try:
            with patch.object(IT.CompositeProvider, "start", fail_after_bind), \
                    patch.object(IT.CompositeProvider, "stop", stop_before_any_cleanup):
                report = await self.invoke(context)
            self.assertEqual(await asyncio.wait_for(held["reader"].read(1), 1), b"")
        finally:
            if "writer" in held:
                held["writer"].close()
                await held["writer"].wait_closed()
        self.assert_failed(report, "INERT_PRIMARY_START_FAILURE")
        self.assertIn("INERT_STOP_CLEANUP_FAILURE", str(report["cleanup"]["errors"]))
        self.assertTrue(report["cleanup"]["workspace_closed"])
        self.assertFalse(report["cleanup"]["http_closed"])
        self.assertEqual(held["active_before_fault"], 1)
        self.assertFalse(held["provider"].server.is_serving())
        self.assertFalse(held["provider"].tasks)
        await self.assert_listener_closed(held["endpoint"])
        self.reopen(fixture)

    async def test_original_deadline_shortens_lifetime_and_preserves_cleanup_margin(self):
        fixture = self.fixture()
        context = self.context(fixture, lifetime=20)
        # Real short service interval; no global clock or sleep replacement.
        context.deadline = time.monotonic()+7.5
        report = await self.invoke(context)
        self.assertEqual(report["status"], "PASS", report)
        self.assertEqual(report["deadline"], context.deadline-6)
        self.assertLess(report["deadline"], report["started"]+20)
        self.assertGreaterEqual(report["finished"], report["deadline"])
        self.assertLess(report["finished"], context.deadline)
        self.assertTrue(report["cleanup"]["http_closed"])
        self.assertTrue(report["cleanup"]["workspace_closed"])
        self.reopen(fixture)

    async def test_cancellation_propagates_after_listener_and_workspace_cleanup(self):
        fixture = self.fixture()
        context = self.context(fixture, lifetime=20)
        task = asyncio.create_task(S.serve(context))
        self.tasks.append(task)
        ready = await self.ready(context, task)
        endpoint = H.Endpoint(**ready["endpoint"])
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        report = self.saved(context)
        self.assert_failed(report, "CancelledError")
        self.assertTrue(report["cleanup"]["http_closed"])
        self.assertTrue(report["cleanup"]["workspace_closed"])
        self.assertEqual(report["cleanup"]["errors"], [])
        await self.assert_listener_closed(endpoint)
        self.reopen(fixture)

    async def test_workspace_close_fault_attempts_remaining_owned_closes(self):
        fixture = self.fixture()
        context = self.context(fixture)
        observed = {}
        original_close = WA.Workspace.close

        async def fail_before_bind(provider, *args, **kwargs):
            raise ValueError("INERT_PRIMARY_BEFORE_BIND")

        def fail_workspace_close(workspace):
            observed["workspace"] = workspace
            OBSERVED["injected_lifecycle_faults"] += 1
            raise ValueError("INERT_WORKSPACE_CLOSE_FAILURE")

        with patch.object(IT.CompositeProvider, "start", fail_before_bind), \
                patch.object(WA.Workspace, "close", fail_workspace_close):
            report = await self.invoke(context)
        self.assert_failed(report, "INERT_PRIMARY_BEFORE_BIND")
        self.assertIn("INERT_WORKSPACE_CLOSE_FAILURE", str(report["cleanup"]["errors"]))
        self.assertFalse(report["cleanup"]["workspace_closed"])
        self.assertTrue(report["cleanup"]["http_closed"])
        workspace = observed["workspace"]
        self.opened.append(workspace)
        self.assertTrue(all(store.db is None for store in
                            (workspace.index, workspace.packets, workspace.modules)))
        self.assertTrue(workspace._lock.closed)
        with self.assertRaises(sqlite3.ProgrammingError):
            workspace.db.execute("SELECT 1")
        # Already closed underlying handles do not mean the entry may report
        # clean success after a close error. Release the inert object's markers.
        original_close(workspace)
        self.reopen(fixture)


SELECTED = (
    "test_existing_data_offer_group_finite_stop_and_reopen",
    "test_missing_workspace_is_never_created",
    "test_configuration_and_mode_mismatch_refuse_without_migration",
    "test_all_explicit_modes_select_exact_existing_store_provider",
    "test_nonloopback_without_tls_and_unbounded_limits_refuse_before_open",
    "test_output_source_and_installation_overlap_refuse_before_open",
    "test_partial_bind_failure_stops_listener_and_releases_workspace",
    "test_stop_fault_preserves_primary_error_and_attempts_workspace_cleanup",
    "test_original_deadline_shortens_lifetime_and_preserves_cleanup_margin",
    "test_cancellation_propagates_after_listener_and_workspace_cleanup",
    "test_workspace_close_fault_attempts_remaining_owned_closes",
)


def main():
    global OUTPUT
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    F.need(Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
           and sys.dont_write_bytecode and not sys.flags.optimize,
           "CANONICAL_ISOLATED_SERVING_CONTROLS")
    OUTPUT = Path(args.output)
    F.need(OUTPUT.is_absolute() and OUTPUT.resolve() == OUTPUT
           and OUTPUT.is_relative_to(PROJECT/"experiments") and not OUTPUT.exists()
           and OUTPUT.parent.is_dir(), "FRESH_SERVING_OUTPUT")
    OUTPUT.mkdir()
    suite = unittest.TestSuite(ServingControls(name) for name in SELECTED)
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_PROCESS_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    imports = [{"name": name, **pin(Path(module.__file__))}
               for name, module in sorted(sys.modules.items())
               if getattr(module, "__file__", None) and Path(module.__file__).is_relative_to(SOURCE)]
    report = {
        "status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skips": len(result.skipped),
        "selected": list(SELECTED), "imports": imports,
        "scope": "REAL_FRESH_STRUCTURAL_STORES_AND_LOOPBACK_SERVING_WITH_EXPLICIT_LIFECYCLE_FAULTS",
        "mathematical_acceptance": False, "real_aggregate_checks": 0, "real_native_checks": 0,
        "proof_calls": 0, "subprocess_calls": 0, "public_network_calls": 0,
        "fixture_observations": dict(OBSERVED),
    }
    with (OUTPUT/"RESULT.json").open("xb") as stream:
        stream.write(encoded(report))
    print(encoded(report).decode(), flush=True)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

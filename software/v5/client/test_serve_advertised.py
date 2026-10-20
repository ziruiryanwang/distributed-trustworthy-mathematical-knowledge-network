"""New advertised-service lifecycle controls; HTTP/Node are explicitly inert.

Reuse the existing serving fixture's real fresh synthetic SQLite workspace.
No prior suite, Node process, socket, Lean, proof or mathematical owner runs.
"""
import asyncio
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE/"portable_runtime"), str(SOURCE)]
from client import serve_advertised as A
from client import test_serve_workspace as T
from discovery.module_export_adapter import compile_query
from location.controller import SOURCE_NAMES
from location.controller_services import ROLE_NAMES
from transport.http_provider import Endpoint

OUTPUT = None
OBSERVED = {"inert_http_starts": 0, "inert_location_starts": 0,
            "inert_publication_attempts": 0}
RESULTS = {}
RETAINED = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\v4-library-commons-02\commons-v4")


class Process:
    def __init__(self):
        self.returncode = None
        self.done = asyncio.get_running_loop().create_future()

    async def wait(self):
        return await asyncio.shield(self.done)

    def exit(self, code):
        self.returncode = code
        if not self.done.done(): self.done.set_result(code)


class ServingControls(T.ServingControls):
    def setUp(self):
        super().setUp()
        self.events, self.channels, self.http = [], [], []
        self.adoptions = []
        self.fault = None
        self.publish_number = 0
        owner = self

        @dataclass
        class InertAdoption:
            source: Path
            source_pins: dict
            installation: Path
            workspace: Path

            def __init__(self, source, source_pins, *, installation_root, workspace_root):
                self.source, self.source_pins = Path(source), dict(source_pins)
                self.installation, self.workspace = Path(installation_root), Path(workspace_root)
                owner.adoptions.append(self)

        class Server:
            def __init__(self): self.closed = False
            def close(self): self.closed = True
            def is_serving(self): return not self.closed
            async def wait_closed(self): pass

        class HTTP:
            def __init__(self, **roles):
                self.roles = roles
                self.server = None
                self.tasks = set()
                self.reserved_reply_bytes = 0
                owner.http.append(self)

            async def start(self, host, port, *, tls_context=None):
                owner.events.append("http.start")
                OBSERVED["inert_http_starts"] += 1
                self.server = Server()
                self.endpoint = Endpoint(host, 43021 if port == 0 else port, tls_context is not None)
                return self.endpoint

            async def stop(self):
                owner.events.append("http.stop")
                if self.server is not None: self.server.close()
                self.server = None
                if owner.fault == "http-close": raise ValueError("INERT_HTTP_STOP_FAILURE")

            def status(self):
                return {"requests": 0, "failures": 0, "active": len(self.tasks),
                        "reserved_reply_bytes": self.reserved_reply_bytes,
                        "mathematical_acceptance": False}

        class Channel:
            def __init__(self, adoption, role_pins, configuration, evidence, *, deadline):
                owner.events.append("location.construct")
                self.adoption, self.role_pins = adoption, dict(role_pins)
                self.config, self.evidence = deepcopy(configuration), Path(evidence)
                self.deadline, self.process = deadline, Process()
                self.closed = self.channel_failed = self.forced_termination = False
                self.stopped = False
                self.commands = []
                owner.channels.append(self)

            def status(self):
                return {"status": "STOPPED" if self.stopped else "RUNNING",
                        "namespace": self.config["namespace"], "role": "index-provider",
                        "global_complete": False, "mathematical_acceptance": False,
                        "joins": []}

            async def start(self):
                owner.events.append("location.start")
                OBSERVED["inert_location_starts"] += 1
                if owner.fault == "start": raise ValueError("INERT_LOCATION_START_FAILURE")
                return self.status()

            async def command(self, command, payload, *, until=None):
                owner.events.append("location."+command)
                self.commands.append({"command": command, "until": until})
                if command == "publish":
                    OBSERVED["inert_publication_attempts"] += 1
                    owner.publish_number += 1
                    result = {"status": "HINT_DISPATCHED_UNACKNOWLEDGED",
                        "route_key": A.P.route_key(self.config["namespace"], payload["features"], payload["stripe"]),
                        "error": None, "census": {"add_provider_write": 1},
                        "remote_placement_confirmed": False, "global_complete": False,
                        "mathematical_acceptance": False}
                    if owner.fault == "publish" and owner.publish_number == 2:
                        result.update(error="INERT_INCOMPLETE_DISPATCH", census={"add_provider_write": 0})
                    if owner.fault == "wrong-route": result["route_key"] = "0"*64
                    return result
                if command == "status":
                    if owner.fault == "health-stopped": self.stopped = True
                    if owner.fault == "final-health-stopped" and until > (
                            self.deadline-2*self.config["limits"]["operation_ms"]/1000+1e-6):
                        self.stopped = True
                    return self.status()
                if command == "stop":
                    if owner.fault == "stop": raise ValueError("INERT_LOCATION_STOP_FAILURE")
                    self.stopped = True
                    self.process.exit(0)
                    return self.status()
                raise AssertionError("UNSELECTED_INERT_COMMAND:"+command)

            async def close(self):
                owner.events.append("location.close")
                self.process.exit(0 if self.process.returncode is None else self.process.returncode)
                if owner.fault == "close": raise ValueError("INERT_LOCATION_CLOSE_FAILURE")
                self.closed = True

            def report(self):
                return {"closed": self.closed, "returncode": self.process.returncode,
                        "channel_failed": self.channel_failed,
                        "forced_termination": self.forced_termination,
                        "role": "index-provider", "mathematical_acceptance": False}

        self.Channel, self.HTTP = Channel, HTTP
        self.InertAdoption = InertAdoption
        for name, replacement in (("AdoptedLocationRuntime", InertAdoption),
                                  ("ServiceLocationProcess", Channel),
                                  ("_types", lambda mode: (T.MODES[mode][0], HTTP))):
            guard = patch.object(A, name, replacement)
            guard.start()
            self.addCleanup(guard.stop)
        original_close = T.WA.Workspace.close

        def close(workspace):
            self.events.append("workspace.close")
            return original_close(workspace)

        guard = patch.object(T.WA.Workspace, "close", close)
        guard.start()
        self.addCleanup(guard.stop)

    async def asyncTearDown(self):
        for channel in self.channels:
            if channel.process.returncode is None: channel.process.exit(0)
        await super().asyncTearDown()

    def context(self, fixture, *, name="operation", lifetime=1.1):
        context = super().context(fixture, name=name, lifetime=lifetime)
        context.parameters["schema"] = A.SCHEMA
        context.parameters["bind"]["port"] = 43021
        context.source_sha256.update({"portable/location/"+name:
            T.pin(SOURCE/"portable_runtime/location"/name)["sha256"]
            for name in SOURCE_NAMES | ROLE_NAMES})
        features = compile_query(fixture.namespace, [{"tag": "declaration-kind", "value": "theorem"}])
        context.parameters["location"] = {
            "installation_root": str(RETAINED),
            "egress": {"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test",
                       "public_ports": [], "test_endpoints": [
                           {"host": "127.0.0.1", "port": 43021},
                           {"host": "127.0.0.1", "port": 43022}]},
            "listen": ["/ip4/127.0.0.1/tcp/43022"], "announce": [], "bootstrap": [],
            "limits": {"service_ms": 30000, "operation_ms": 1000,
                "query_events": 32, "provider_limit": 2, "advertised_keys": 2,
                "provider_ttl_ms": 3000, "reprovide_interval_ms": 500,
                "maintenance_ms": 1000, "commands": 32, "descriptor_requests": 4,
                "descriptor_reply_bytes": 4096, "metadata": {},
                "transport": {"outbound_attempts": 8, "inbound_upgrades": 8,
                              "receive_bytes": 65536, "send_bytes": 65536}},
            "routes": [{"features": features, "stripe": 0}, {"features": features, "stripe": 1}],
            "health_interval_ms": 100,
        }
        self.events.clear()  # Discard fixture setup close, not service events.
        return context

    async def invoke(self, context):
        return await asyncio.wait_for(A.serve(context), timeout=5)

    async def ready(self, context, task):
        path = context.location_workspace/"service-ready.json"
        until = time.monotonic()+2
        while not path.exists():
            if task.done(): self.fail("ADVERTISED_SERVICE_TERMINATED_BEFORE_READY:"+str(task.result()))
            self.assertLess(time.monotonic(), until)
            await asyncio.sleep(0.005)
        return json.loads(path.read_bytes())

    def cleanup_order(self):
        self.assertLess(self.events.index("location.close"), self.events.index("http.stop"))
        self.assertLess(self.events.index("http.stop"), self.events.index("workspace.close"))

    async def test_derived_endpoint_namespace_pins_and_original_lifetime(self):
        fixture = self.fixture()
        context = self.context(fixture)
        report = await self.invoke(context)
        self.assertEqual(report["status"], "PASS", report)
        channel, adoption, provider = self.channels[0], self.adoptions[0], self.http[0]
        self.assertEqual(adoption.installation, RETAINED)
        self.assertNotEqual(adoption.installation, context.installation)
        self.assertEqual(adoption.source, context.sources_portable/"location")
        self.assertEqual(set(adoption.source_pins), set(SOURCE_NAMES))
        self.assertEqual(set(channel.role_pins), set(ROLE_NAMES))
        self.assertEqual(channel.config["namespace"], fixture.namespace)
        self.assertEqual(channel.config["endpoints"], [{"host": provider.endpoint.host,
            "port": provider.endpoint.port, "tls": provider.endpoint.tls,
            "server_name": provider.endpoint.server_name}])
        self.assertEqual(channel.config["role"], "index-provider")
        self.assertLessEqual(channel.deadline, context.deadline)
        self.assertLess(report["deadline"], channel.deadline)
        self.assertEqual(report["deadline"], report["started"]+1.1)
        self.assertEqual(report["final_health_deadline"], report["deadline"]+1)
        self.assertEqual(report["stop_deadline"], report["final_health_deadline"]+1)
        self.assertEqual(channel.deadline, report["stop_deadline"])
        self.assertGreaterEqual(report["finished"], report["deadline"])
        self.assertLess(report["finished"], context.deadline)
        self.assertLessEqual(channel.config["limits"]["service_ms"], 30000)
        self.assertEqual(len(report["route_dispatch"]), 2)
        self.assertTrue(all(row["remote_placement_confirmed"] is False for row in report["route_dispatch"]))
        self.assertGreaterEqual(report["health_checks"], 2)
        self.assertLessEqual(report["health_checks"], report["health_cap"])
        self.assertEqual([row["command"] for row in channel.commands[-2:]], ["status", "stop"])
        self.assertTrue(all(row["until"] <= channel.deadline for row in channel.commands))
        self.assertLessEqual(len(channel.commands), context.parameters["location"]["limits"]["commands"])
        self.assertTrue(report["cleanup"]["location_closed"])
        self.assertTrue(report["cleanup"]["http_closed"])
        self.assertTrue(report["cleanup"]["workspace_closed"])
        self.assertEqual(report["cleanup"]["errors"], [])
        self.cleanup_order()
        self.assertFalse(report["mathematical_acceptance"])
        self.assertEqual(self.saved(context), report)
        RESULTS[self._testMethodName] = {"events": list(self.events),
            "location_config": channel.config, "report": report,
            "scope": "INERT_SERVICES_REAL_FRESH_SYNTHETIC_WORKSPACE"}
        self.reopen(fixture)

    async def test_invalid_location_inputs_refuse_before_workspace_or_http(self):
        fixture = self.fixture()
        for index, defect in enumerate(("runtime", "overlap", "pins", "routes", "budget", "endpoint", "ephemeral")):
            context = self.context(fixture, name="invalid-"+str(index))
            location = context.parameters["location"]
            if defect == "runtime": location["installation_root"] = str(self.root/"missing-runtime")
            elif defect == "overlap": location["installation_root"] = str(context.location_workspace)
            elif defect == "pins": context.source_sha256.pop("portable/location/node_entry_services.mjs")
            elif defect == "routes": location["routes"] = []
            elif defect == "budget": location["limits"]["commands"] = 1
            elif defect == "endpoint": location["endpoints"] = [{"host": "127.0.0.1", "port": 1, "tls": False, "server_name": None}]
            else: context.parameters["bind"]["port"] = 0
            with patch.object(T.WA.Workspace, "open", side_effect=AssertionError("INVALID_MUST_NOT_OPEN")) as opened:
                with self.assertRaises(Exception): await self.invoke(context)
            self.assertFalse(opened.called)
            self.assertEqual(self.http, [])
            self.assertFalse((context.location_workspace/"service-ready.json").exists())
        self.reopen(fixture)

    async def test_location_start_failure_after_http_still_closes_all(self):
        fixture = self.fixture()
        context = self.context(fixture)
        self.fault = "start"
        report = await self.invoke(context)
        self.assert_failed(report, "INERT_LOCATION_START_FAILURE")
        self.assertEqual(self.events[:3], ["http.start", "location.construct", "location.start"])
        self.cleanup_order()
        self.assertTrue(report["cleanup"]["http_closed"])
        self.assertTrue(report["cleanup"]["workspace_closed"])
        self.assertFalse((context.location_workspace/"service-ready.json").exists())
        self.reopen(fixture)

    async def test_incomplete_or_mismatched_publication_never_announces_ready(self):
        fixture = self.fixture()
        for index, defect in enumerate(("publish", "wrong-route")):
            context = self.context(fixture, name="publish-"+str(index))
            self.fault, self.publish_number = defect, 0
            report = await self.invoke(context)
            self.assert_failed(report)
            self.assertFalse((context.location_workspace/"service-ready.json").exists())
            self.cleanup_order()
            self.assertTrue(report["cleanup"]["http_closed"])
            self.assertTrue(report["cleanup"]["workspace_closed"])
            self.reopen(fixture)

    async def test_early_location_process_exit_fails_without_http_fallback(self):
        fixture = self.fixture()
        context = self.context(fixture)
        task = asyncio.create_task(A.serve(context)); self.tasks.append(task)
        await self.ready(context, task)
        self.channels[0].process.exit(7)
        report = await asyncio.wait_for(task, 2)
        self.assert_failed(report)
        self.assertLess(report["finished"], report["deadline"])
        self.cleanup_order()
        self.assertTrue(report["cleanup"]["http_closed"])
        self.assertTrue(report["cleanup"]["workspace_closed"])
        self.reopen(fixture)

    async def test_post_ready_http_or_locator_health_failure_is_terminal(self):
        fixture = self.fixture()
        for index, fault in enumerate(("health-stopped", "final-health-stopped", "http-stopped")):
            context = self.context(fixture, name="health-"+str(index))
            self.fault = None
            task = asyncio.create_task(A.serve(context)); self.tasks.append(task)
            await self.ready(context, task)
            self.assertIsNone(self.channels[-1].process.returncode)
            self.fault = fault
            if fault == "http-stopped": self.http[-1].server.close()
            report = await asyncio.wait_for(task, 2)
            reason = ("ADVERTISED_SERVICE_HTTP_NOT_LIVE" if fault == "http-stopped"
                      else "ADVERTISED_SERVICE_LOCATION_NOT_LIVE")
            self.assert_failed(report, reason)
            self.assertIn("location.status", self.events)
            self.cleanup_order()
            self.assertTrue(report["cleanup"]["http_closed"])
            self.assertTrue(report["cleanup"]["workspace_closed"])
            if fault == "final-health-stopped":
                self.assertGreaterEqual(report["finished"], report["deadline"])
            else:
                self.assertLess(report["finished"], report["deadline"])
            self.reopen(fixture)

    async def test_cancellation_propagates_after_ordered_cleanup(self):
        fixture = self.fixture()
        context = self.context(fixture)
        task = asyncio.create_task(A.serve(context)); self.tasks.append(task)
        await self.ready(context, task)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError): await task
        report = self.saved(context)
        self.assert_failed(report)
        self.cleanup_order()
        self.assertTrue(report["cleanup"]["http_closed"])
        self.assertTrue(report["cleanup"]["workspace_closed"])
        self.reopen(fixture)

    async def test_location_stop_or_close_failure_does_not_skip_other_cleanup(self):
        fixture = self.fixture()
        for index, defect in enumerate(("stop", "close")):
            context = self.context(fixture, name="cleanup-"+str(index))
            self.fault = defect
            report = await self.invoke(context)
            self.assert_failed(report, "INERT_LOCATION_"+defect.upper()+"_FAILURE")
            self.cleanup_order()
            self.assertTrue(report["cleanup"]["http_closed"])
            self.assertTrue(report["cleanup"]["workspace_closed"])
            self.assertTrue(report["cleanup"]["errors"])
            self.reopen(fixture)

    async def test_http_cleanup_failure_after_location_still_releases_workspace(self):
        fixture = self.fixture()
        context = self.context(fixture)
        self.fault = "http-close"
        report = await self.invoke(context)
        self.assert_failed(report, "INERT_HTTP_STOP_FAILURE")
        self.cleanup_order()
        self.assertTrue(report["cleanup"]["location_closed"])
        self.assertTrue(report["cleanup"]["workspace_closed"])
        self.assertTrue(report["cleanup"]["errors"])
        self.reopen(fixture)


SELECTED = (
    "test_derived_endpoint_namespace_pins_and_original_lifetime",
    "test_invalid_location_inputs_refuse_before_workspace_or_http",
    "test_location_start_failure_after_http_still_closes_all",
    "test_incomplete_or_mismatched_publication_never_announces_ready",
    "test_early_location_process_exit_fails_without_http_fallback",
    "test_post_ready_http_or_locator_health_failure_is_terminal",
    "test_cancellation_propagates_after_ordered_cleanup",
    "test_location_stop_or_close_failure_does_not_skip_other_cleanup",
    "test_http_cleanup_failure_after_location_still_releases_workspace",
)


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output": raise ValueError("OUTPUT_REQUIRED")
    T.F.need(Path.cwd() == T.PROJECT and sys.flags.isolated and sys.flags.no_site
             and sys.dont_write_bytecode and not sys.flags.optimize,
             "CANONICAL_ISOLATED_ADVERTISED_CONTROLS")
    OUTPUT = Path(sys.argv[2])
    if (not OUTPUT.is_dir() or OUTPUT.resolve() != OUTPUT
            or not OUTPUT.is_relative_to(T.PROJECT/"experiments")):
        raise ValueError("EXISTING_CANONICAL_OUTPUT_REQUIRED")
    T.OUTPUT = OUTPUT
    suite = unittest.TestSuite(ServingControls(name) for name in SELECTED)
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "create_subprocess_exec", side_effect=AssertionError("NODE_FORBIDDEN")), \
         patch.object(asyncio, "open_connection", side_effect=AssertionError("NETWORK_FORBIDDEN")), \
         patch.object(asyncio, "start_server", side_effect=AssertionError("NETWORK_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "selected": list(SELECTED), "observed": OBSERVED, "results": RESULTS,
        "scope": "REAL_FRESH_STRUCTURAL_WORKSPACE_WITH_INERT_HTTP_AND_LOCATION_LIFECYCLES",
        "mathematical_acceptance": False, "node_calls": 0, "native_calls": 0, "proof_calls": 0,
        "network_calls": 0, "sources": {name: hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()
            for name in ("client/serve_advertised.py", "client/test_serve_advertised.py",
                         "client/serve_workspace.py", "client/test_serve_workspace.py")}}
    with (OUTPUT/"controls-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

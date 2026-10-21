"""Eight changed-boundary controls; real stores, inert HTTP/location, no proofs.

The frozen fingerprint module supplies its overlay map and tiny syntax helpers,
not its suite. Existing service fixtures supply configuration/context helpers,
not their tests. Root separately selects one finite execution of SELECTED.
"""
import asyncio
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import socket
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
OUTPUT = None
RESULTS = {}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


K = load("projection_fingerprint_support", SOURCE/"instantiation_discovery/controls.py")
BP = K.overlay("client.base_projection", "base_projection/client/base_projection.py")
H = K.overlay("client.serve_workspace", "base_projection/client/serve_workspace.py")
A = K.overlay("client.serve_advertised", "base_projection/client/serve_advertised.py")
D = load("projection_distribution", SOURCE/"base_projection/distribution.py")
from client import test_serve_workspace as T
from evidence_network import transport as ET
from transport import http_provider_receipts as HTTP

C, F, S, E, Q, CQ = K.C, K.F, K.S, K.E, K.Q, K.CQ
INDEX_LIMITS = dict(K.INDEX_LIMITS)
BASE = K.adapter()
QUERY = [{"tag": "declaration-kind", "value": "theorem"}]
FEATURES = BASE.compile_query(QUERY)  # Before any selected export identifiers.
RETAINED = PROJECT/"product-local/v4-library-commons-02/commons-v4"


class InertProcess:
    def __init__(self):
        self.returncode = None
        self.done = asyncio.get_running_loop().create_future()

    async def wait(self):
        return await asyncio.shield(self.done)

    def exit(self):
        self.returncode = 0
        if not self.done.done():
            self.done.set_result(0)


class ProjectionControls(T.ServingControls):
    """Explicit SELECTED excludes every inherited predecessor test."""
    def setUp(self):
        T.OUTPUT = OUTPUT
        super().setUp()
        self.serial, self.events = 0, []
        self.providers, self.channels, self.views = [], [], []
        self.fault = None
        self.provider_started = asyncio.Event()
        # IsolatedAsyncioTestCase has already created its event-loop wakeup
        # infrastructure. No tested code may open a service/network socket.
        for owner, name in ((socket, "socket"), (subprocess, "Popen"),
                            (asyncio, "create_subprocess_exec"),
                            (asyncio, "create_subprocess_shell"),
                            (asyncio, "open_connection"), (asyncio, "start_server")):
            guard = patch.object(owner, name, side_effect=AssertionError("UNSELECTED_IO:"+name))
            guard.start()
            self.addCleanup(guard.stop)
        self._install_inert_services()

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done(): task.cancel()
        if self.tasks: await asyncio.gather(*self.tasks, return_exceptions=True)
        for channel in self.channels: channel.process.exit()
        errors = []
        for view in reversed(self.views):
            if not view.closed:
                try: view.close()
                except BaseException as error: errors.append(str(error))
        for workspace in reversed(self.opened):
            if not workspace._closed:
                tail = []
                if not H._close_workspace(workspace, tail):
                    errors.append(str(tail))
        if errors:
            RESULTS.setdefault(self._testMethodName, {})["unexpected_teardown_errors"] = errors
            self.fail("UNEXPECTED_TEARDOWN_ERRORS:"+str(errors))

    def fresh(self, label):
        self.serial += 1
        return self.root/(str(self.serial)+"-"+label)

    def fixture(self, *, count=1, label="fixture"):
        config = T.configuration("evidence")
        config.update(schema=K.WE.CONCLUSION_FINGERPRINT_SCHEMA,
                      discovery_profile=K.profile(["arg"]))
        config["index_limits"] = dict(INDEX_LIMITS)
        path = self.fresh(label)
        workspace = K.WE.Workspace.open(path, config, create=True)
        self.opened.append(workspace)
        rows = [self.add_export(workspace, "Law"+str(number)) for number in range(count)]
        result = SimpleNamespace(root=path, config=config, mode="evidence", rows=rows,
            namespace=workspace.adapter.namespace, source_status=workspace.index.status())
        workspace.close()
        return result

    def add_export(self, workspace, label):
        name = K.name(label)
        spec = {"schema": C.SPEC_SCHEMA, "foundation": K.B.FOUNDATION, "policy": K.B.POLICY,
            "groups": [{"kind": "ordinary", "declarations": [{"name": name,
                "kind": "theorem", "universes": 0, "type": K.law(),
                "value_hash": None, "meta": {}}]}]}
        module, opening = C.module_id(spec), C.group_opening(spec, 0)
        workspace.modules.put_group(module, opening)
        raw = workspace.adapter.encode_opening(module, name, opening)
        described = workspace.adapter.describe(raw)
        self.assertFalse(described["mathematical_acceptance"])
        workspace.index.admit(raw, expected_id=C.export_id(module, name))
        return dict(locator={"module_id": module, "relative_name": name, "group_index": 0},
                    opening=opening, raw=raw, record=described["record"],
                    export_id=C.export_id(module, name))

    def open_workspace(self, fixture):
        workspace = K.WE.Workspace.open(fixture.root, fixture.config, create=False)
        self.opened.append(workspace)
        return workspace

    def context(self, fixture, *, name=None, lifetime=1):
        if name is None:
            self.serial += 1
            name = "operation-"+str(self.serial)
        return super().context(fixture, name=name, lifetime=lifetime)

    def prepare_context(self, fixture, *, rows=None, limits=None, create=True):
        context = self.context(fixture)
        context.parameters = {"schema": BP.PREPARE_SCHEMA, "mode": fixture.mode,
            "workspace_path": str(fixture.root), "workspace_config": deepcopy(fixture.config),
            "create": create, "index_limits": dict(INDEX_LIMITS if limits is None else limits),
            "exports": [deepcopy(row["locator"]) for row in (fixture.rows if rows is None else rows)],
            "limits": {"export_bytes": 64*MIB, "wall_seconds": 20}}
        return context

    def prepare(self, fixture, **kwargs):
        context = self.prepare_context(fixture, **kwargs)
        report = BP.prepare(context)
        saved = context.location_workspace/"base-projection-result.json"
        self.assertLessEqual(saved.stat().st_size, 65536)
        self.assertEqual(json.loads(saved.read_bytes()), report)
        RESULTS.setdefault(self._testMethodName, {}).setdefault("preparations", []).append(report)
        return report

    def selector(self, fixture, limits=None):
        limits = dict(INDEX_LIMITS if limits is None else limits)
        index = S.Store(fixture.root/"base-projection-index", BASE, limits, create=False)
        try:
            snapshot = index.snapshot()
            sid = K.A.snapshot_id(snapshot)
            self.assertEqual(index.status()["latest"], sid)
            return {"schema": BP.VIEW_SCHEMA, "index_limits": limits, "expected_snapshot_id": sid}
        finally:
            index.close()

    def view(self, workspace, selector):
        return BP.open_view(workspace, selector)

    def record(self, index, export_id):
        row = index.db.execute("SELECT record FROM objects WHERE object_id=?", (export_id,)).fetchone()
        return None if row is None else F.strict(bytes(row[0]), 65536)

    def hits(self, index, *, provider=None):
        sid = index.status()["latest"]
        summary = Q.verify_summary(sid, index.namespace, FEATURES, index.summary(sid, FEATURES))
        hits = []
        for plan in Q.plan_partitions(summary):
            if not plan["anchor_count"]: continue
            request = {"schema": "DMKN_FORMAL_CANDIDATE_REQUEST_V1", "namespace": index.namespace,
                "snapshot_id": sid, "features": FEATURES, "partition": plan["partition"],
                "anchor": plan["anchor"], "start": 0, "limits": dict(K.PAGE_LIMITS)}
            response = CQ.page(index, request) if provider is None else provider.dispatch(HTTP.CANDIDATE_ROUTE, request)
            checked = CQ.verify_page(summary, request, response)
            self.assertFalse(checked["mathematical_acceptance"])
            self.assertEqual(response["termination"], "anchor_boundary")
            hits.extend(item["object_id"] for item in checked["matches"])
        return sorted(hits)

    def offer(self, provider, namespace, features=FEATURES):
        raw = provider.dispatch(HTTP.OFFER_ROUTE, {"namespace": namespace, "features": features,
            "max_bytes": 262144, "max_expanded_bytes": 262144})
        return F.strict(raw, 262144)

    def assert_source(self, fixture, workspace):
        self.assertEqual(workspace.adapter.namespace, fixture.namespace)
        self.assertEqual(workspace.index.status(), fixture.source_status)
        for row in fixture.rows:
            loc = row["locator"]
            self.assertEqual(workspace.modules.get_group(loc["module_id"], loc["relative_name"],
                                                        loc["group_index"])[0], row["opening"])
            self.assertEqual(self.record(workspace.index, row["export_id"]), row["record"])

    def service_context(self, fixture, selector=None):
        context = self.context(fixture)
        if selector is not None:
            context.parameters.update(schema=H.SCHEMA_V2, index_view=deepcopy(selector))
        return context

    def _install_inert_services(self):
        owner = self

        class Server:
            def __init__(self): self.closed = False
            def close(self): self.closed = True
            def is_serving(self): return not self.closed
            async def wait_closed(self): pass

        class Provider(ET.CompositeProvider):
            def __init__(self, **roles):
                super().__init__(**roles)  # Actual strict custody types/profile checks.
                owner.providers.append(self)
                if owner.fault == "provider-constructor":
                    raise ValueError("INJECTED_PROVIDER_CONSTRUCTOR")

            async def start(self, host, port, *, tls_context=None):
                owner.events.append("http.start")
                if owner.fault == "http-start": raise ValueError("INJECTED_HTTP_START")
                self.server = Server()
                self.endpoint = HTTP.Endpoint(host, port or 43021, tls_context is not None)
                self.observed_offer = owner.offer(self, self.index.namespace,
                    self.index.adapter.compile_query(QUERY))
                owner.provider_started.set()
                return self.endpoint

            async def stop(self):
                owner.events.append("http.stop")
                if self.server is not None: self.server.close()
                self.server = None

        class Adoption:
            def __init__(self, source, source_pins, *, installation_root, workspace_root):
                self.source, self.source_pins = Path(source), dict(source_pins)
                self.installation, self.workspace = Path(installation_root), Path(workspace_root)

        class Channel:
            def __init__(self, adoption, role_pins, configuration, evidence, *, deadline):
                self.config, self.deadline = deepcopy(configuration), deadline
                self.process = InertProcess()
                self.closed = self.channel_failed = self.forced_termination = self.stopped = False
                owner.channels.append(self)

            def status(self):
                return {"status": "STOPPED" if self.stopped else "RUNNING",
                    "namespace": self.config["namespace"], "role": "index-provider",
                    "global_complete": False, "mathematical_acceptance": False}

            async def start(self):
                owner.events.append("location.start")
                if owner.fault == "location-start": raise ValueError("INJECTED_LOCATION_START")
                return self.status()

            async def command(self, command, payload, *, until=None):
                owner.events.append("location."+command)
                if command == "publish":
                    return {"status": "HINT_DISPATCHED_UNACKNOWLEDGED",
                        "route_key": A.P.route_key(self.config["namespace"], payload["features"], payload["stripe"]),
                        "error": None, "census": {"add_provider_write": 1},
                        "remote_placement_confirmed": False, "global_complete": False,
                        "mathematical_acceptance": False}
                if command == "stop":
                    self.stopped = True
                    self.process.exit()
                elif command != "status": raise AssertionError("UNSELECTED_LOCATION_COMMAND")
                return self.status()

            async def close(self):
                owner.events.append("location.close")
                self.process.exit()
                self.closed = True

            def report(self):
                return {"closed": self.closed, "returncode": self.process.returncode,
                    "channel_failed": False, "forced_termination": False,
                    "role": "index-provider", "mathematical_acceptance": False}

        original_close = BP.ProjectionView.close
        workspace_close = K.WE.Workspace.close
        original_open = BP.open_view

        def close(view):
            owner.events.append("projection.close")
            return original_close(view)

        def close_workspace(workspace):
            owner.events.append("workspace.close")
            return workspace_close(workspace)

        def open_view(workspace, selector):
            view = original_open(workspace, selector)
            owner.views.append(view)
            owner.served_workspace = workspace
            return view

        for module, name, replacement in ((H, "_types", lambda mode: (K.WE.Workspace, Provider)),
                (A, "_types", lambda mode: (K.WE.Workspace, Provider)),
                (A, "AdoptedLocationRuntime", Adoption), (A, "ServiceLocationProcess", Channel),
                (BP, "open_view", open_view), (BP.ProjectionView, "close", close),
                (K.WE.Workspace, "close", close_workspace)):
            guard = patch.object(module, name, replacement)
            guard.start()
            self.addCleanup(guard.stop)

    def advertised_context(self, fixture, selector):
        context = self.service_context(fixture, selector)
        context.parameters["schema"] = A.SCHEMA_V2
        context.parameters["bind"]["port"] = 43021
        # The location child/adoption are inert. These explicit synthetic pins
        # test closed parameter propagation, not runtime-source verification.
        context.source_sha256.update({"portable/location/"+name: "91"*32
            for name in A.SOURCE_NAMES | A.ROLE_NAMES})
        context.parameters["location"] = {"installation_root": str(RETAINED),
            "egress": {"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test",
                "public_ports": [], "test_endpoints": [{"host": "127.0.0.1", "port": 43021},
                    {"host": "127.0.0.1", "port": 43022}]},
            "listen": ["/ip4/127.0.0.1/tcp/43022"], "announce": [], "bootstrap": [],
            "limits": {"service_ms": 30000, "operation_ms": 1000, "query_events": 32,
                "provider_limit": 2, "advertised_keys": 2, "provider_ttl_ms": 3000,
                "reprovide_interval_ms": 500, "maintenance_ms": 1000, "commands": 32,
                "descriptor_requests": 4, "descriptor_reply_bytes": 4096, "metadata": {},
                "transport": {"outbound_attempts": 8, "inbound_upgrades": 8,
                    "receive_bytes": 65536, "send_bytes": 65536}},
            "routes": [{"features": FEATURES, "stripe": 0}], "health_interval_ms": 100}
        return context

    def test_two_namespaces_one_held_export(self):
        fixture = self.fixture()
        workspace = self.open_workspace(fixture)
        source = ET.CompositeProvider(index=workspace.index, custody=workspace.modules,
                                      packets=workspace.packets)
        refusal = self.offer(source, BASE.namespace)
        self.assertEqual((refusal["status"], refusal["reason"]), ("NO_OFFER", "NAMESPACE_NOT_SERVED"))
        empty = S.Store(self.fresh("empty-base"), BASE, INDEX_LIMITS, create=True)
        try: self.assertEqual(self.hits(empty), [])
        finally: empty.close()
        workspace.close()
        report = self.prepare(fixture)
        self.assertEqual(report["status"], "PASS", report)
        workspace = self.open_workspace(fixture)
        view = self.view(workspace, self.selector(fixture))
        provider = ET.CompositeProvider(index=view.index, custody=workspace.modules, packets=workspace.packets)
        self.assertEqual(self.hits(view.index, provider=provider), [fixture.rows[0]["export_id"]])
        self.assertEqual(provider.dispatch("/v5/modules/group", fixture.rows[0]["locator"]),
                         fixture.rows[0]["opening"])
        self.assertIs(provider.custody, workspace.modules)
        self.assertIs(provider.packets, workspace.packets)
        self.assert_source(fixture, workspace)
        self.assertEqual(view.index.adapter.encode_opening(fixture.rows[0]["locator"]["module_id"],
            fixture.rows[0]["locator"]["relative_name"], fixture.rows[0]["opening"]), fixture.rows[0]["raw"])
        view.close()
        workspace.close()

    def test_namespace_record_and_feature_isolation(self):
        fixture = self.fixture()
        self.assertEqual(self.prepare(fixture)["status"], "PASS")
        workspace = self.open_workspace(fixture)
        view = self.view(workspace, self.selector(fixture))
        row = fixture.rows[0]
        base_record = self.record(view.index, row["export_id"])
        self.assertEqual(base_record, BASE.extract(row["raw"]))
        self.assertNotEqual(base_record, row["record"])
        self.assertNotEqual(F.record_id(base_record), F.record_id(row["record"]))
        self.assertNotEqual(FEATURES, workspace.adapter.compile_query(QUERY))
        forged = deepcopy(row["record"])
        forged["namespace"] = BASE.namespace
        with self.assertRaises(ValueError): BASE.resolve(forged, row["raw"])
        with self.assertRaises(ValueError): BASE.resolve(row["record"], row["raw"])
        provider = ET.CompositeProvider(index=view.index, custody=workspace.modules, packets=workspace.packets)
        self.assertEqual(self.offer(provider, fixture.namespace)["reason"], "NAMESPACE_NOT_SERVED")
        self.assert_source(fixture, workspace)
        view.close()
        workspace.close()

    def test_finite_preflight_and_exclusive_borrow(self):
        fixture = self.fixture(count=2)
        invalid = []
        for defect in ("duplicate", "over-count", "over-bytes", "extra-path", "bool-index", "bad-hash", "bytes", "wall", "quota"):
            context = self.prepare_context(fixture)
            params = context.parameters
            if defect == "duplicate": params["exports"] = [params["exports"][0]]*2
            elif defect == "over-count": params["exports"] *= 33
            elif defect == "over-bytes": params["exports"] = [
                {"module_id": format(i, "064x"), "relative_name": K.name("x"*1024), "group_index": 0}
                for i in range(64)]
            elif defect == "extra-path": params["target_path"] = str(self.fresh("forbidden-target"))
            elif defect == "bool-index": params["exports"][0]["group_index"] = True
            elif defect == "bad-hash": params["exports"][0]["module_id"] = "bad"
            elif defect == "bytes": params["limits"]["export_bytes"] = 16*MIB-1
            elif defect == "wall": params["limits"]["wall_seconds"] = float("inf")
            else: params["index_limits"]["extra"] = 1
            with patch.object(S.Store, "__init__", side_effect=AssertionError("PREMATURE_STORE_OPEN")) as opened:
                with self.assertRaises((ValueError, TypeError)): BP.prepare(context)
            self.assertFalse(opened.called)
            self.assertFalse((fixture.root/"base-projection-index").exists())
            invalid.append(defect)
        self.assertEqual(self.prepare(fixture, rows=fixture.rows[:1])["status"], "PASS")
        selector = self.selector(fixture)
        workspace = self.open_workspace(fixture)
        original = (workspace.adapter, workspace.index, workspace.modules, workspace.packets, workspace._lock)
        view = self.view(workspace, selector)
        self.assertEqual(view.index.root, fixture.root/"base-projection-index")
        self.assertEqual(self.hits(view.index), [fixture.rows[0]["export_id"]])
        with self.assertRaises(ValueError): BP.open_view(workspace, selector)
        with self.assertRaises(OSError): K.WE.Workspace.open(fixture.root, fixture.config, create=False)
        self.assertEqual(original, (workspace.adapter, workspace.index, workspace.modules, workspace.packets, workspace._lock))
        view.close()
        with self.assertRaises(ValueError):
            BP.open_view(workspace, {**selector, "namespace": fixture.namespace})
        wrong_config = deepcopy(selector)
        wrong_config["index_limits"]["max_objects"] += 1
        with self.assertRaises(BP.ProjectionOpenError): BP.open_view(workspace, wrong_config)
        for attr, value in (("_poisoned", True), ("_client", object()), ("_grants", {"reserved": object()})):
            before = getattr(workspace, attr)
            setattr(workspace, attr, value)
            try:
                with self.assertRaises(ValueError): BP.open_view(workspace, selector)
            finally: setattr(workspace, attr, before)
        replacement = self.view(workspace, selector)
        replacement.close()
        workspace.close()
        with self.assertRaises(ValueError): BP.open_view(workspace, selector)
        RESULTS[self._testMethodName]["invalid_preflight"] = invalid

    def test_partial_quota_uncertainty_and_explicit_reconciliation(self):
        fixture = self.fixture(count=2)
        limits = {**INDEX_LIMITS, "max_objects": 1}
        failed = self.prepare(fixture, limits=limits)
        self.assertEqual(failed["status"], "FAILED", failed)
        self.assertEqual(failed["attempted"], 2)
        self.assertEqual([row["export_id"] for row in failed["acknowledged"]],
                         [fixture.rows[0]["export_id"]])
        self.assertEqual(failed["outcome"], "COMMIT_OUTCOME_UNKNOWN")
        self.assertIn("OBJECT_CAP", str(failed["error"]))
        self.assertIsNone(failed["snapshot_id"])
        self.assertIsNone(failed["local_cut"])
        self.assertEqual(failed["current_export_id"], fixture.rows[1]["export_id"])
        self.assertEqual(failed["submitted_export_bytes"], sum(len(row["raw"]) for row in fixture.rows))
        self.assertEqual([row["phase"] for row in failed["store_work"]["samples"]],
                         ["constructor", "admit:1", "admit:2"])
        self.assertEqual(failed["store_work"]["unknown"], [])
        for key in BP.WORK_KEYS:
            self.assertEqual(failed["store_work"]["known_totals"][key],
                             sum(sample["work"][key] for sample in failed["store_work"]["samples"]))
        self.assertTrue(failed["cleanup"]["projection_closed"])
        self.assertTrue(failed["cleanup"]["workspace_closed"])
        cut = self.selector(fixture, limits)
        workspace = self.open_workspace(fixture)
        view = self.view(workspace, cut)
        self.assertEqual(self.hits(view.index), [fixture.rows[0]["export_id"]])
        self.assertIsNone(self.record(view.index, fixture.rows[1]["export_id"]))
        self.assertEqual(view.index.status()["seq"], 1)
        self.assert_source(fixture, workspace)
        view.close()
        workspace.close()
        reconciled = self.prepare(fixture, limits=limits, rows=fixture.rows[:1], create=False)
        self.assertEqual(reconciled["status"], "PASS", reconciled)
        self.assertFalse(reconciled["acknowledged"][0]["new"])
        self.assertEqual(reconciled["snapshot_id"], cut["expected_snapshot_id"])
        self.assertEqual(reconciled["local_cut"], 1)
        self.assertGreater(reconciled["submitted_export_bytes"], 0)
        with patch.object(S.Store, "admit", side_effect=RuntimeError("INJECTED_BEFORE_WORK_RESET")) as entry:
            unmeasured = self.prepare(fixture, limits=limits, rows=fixture.rows[:1], create=False)
        self.assertEqual(entry.call_count, 1)
        self.assertEqual(unmeasured["outcome"], "COMMIT_OUTCOME_UNKNOWN")
        self.assertEqual(unmeasured["acknowledged"], [])
        self.assertEqual(unmeasured["store_work"]["unknown"], ["admit:1"])
        self.assertIsNone(unmeasured["store_work"]["samples"][1]["work"])
        self.assertEqual(unmeasured["store_work"]["known_totals"],
                         unmeasured["store_work"]["samples"][0]["work"])

        committed = self.fixture(label="uncertain-after-commit")
        original, calls = S.Store.admit, []
        def after_commit(index, raw, expected_id=None):
            result = original(index, raw, expected_id=expected_id)
            calls.append(result)
            raise RuntimeError("INJECTED_AFTER_ACTUAL_COMMIT")
        with patch.object(S.Store, "admit", after_commit):
            unknown = self.prepare(committed)
        self.assertEqual(len(calls), 1)  # No automatic retry.
        self.assertEqual(unknown["status"], "FAILED", unknown)
        self.assertEqual(unknown["attempted"], 1)
        self.assertEqual(unknown["acknowledged"], [])
        self.assertIsNone(unknown["last_acknowledged_snapshot"])
        self.assertIsNone(unknown["snapshot_id"])
        self.assertEqual(unknown["outcome"], "COMMIT_OUTCOME_UNKNOWN")
        actual = self.selector(committed)
        self.assertEqual(actual["expected_snapshot_id"], calls[0]["snapshot_id"])
        confirmed = self.prepare(committed, create=False)
        self.assertEqual(confirmed["status"], "PASS", confirmed)
        self.assertFalse(confirmed["acknowledged"][0]["new"])
        self.assertEqual(confirmed["local_cut"], 1)
        self.assertEqual(confirmed["snapshot_id"], actual["expected_snapshot_id"])

    def test_latest_cut_is_explicit_not_all_source_coverage(self):
        fixture = self.fixture(count=2)
        self.assertEqual(self.prepare(fixture, rows=fixture.rows[:1])["status"], "PASS")
        first = self.selector(fixture)
        workspace = self.open_workspace(fixture)
        late = self.add_export(workspace, "LaterSourceOnly")
        view = self.view(workspace, first)
        self.assertEqual(self.hits(view.index), [fixture.rows[0]["export_id"]])
        self.assertIsNone(self.record(view.index, late["export_id"]))
        first_snapshot = view.index.snapshot()
        self.assertEqual(first_snapshot["local_cut"], 1)
        view.close()
        workspace.close()
        self.assertEqual(self.prepare(fixture, rows=fixture.rows[1:], create=False)["status"], "PASS")
        latest = self.selector(fixture)
        self.assertNotEqual(first["expected_snapshot_id"], latest["expected_snapshot_id"])
        workspace = self.open_workspace(fixture)
        with self.assertRaises(BP.ProjectionOpenError): BP.open_view(workspace, first)
        view = self.view(workspace, latest)  # Stale-constructor failure released the borrow.
        self.assertEqual(view.index.snapshot(first["expected_snapshot_id"]), first_snapshot)
        self.assertEqual(view.index.snapshot()["local_cut"], 2)
        self.assertIsNone(self.record(view.index, late["export_id"]))
        view.close()
        workspace.close()
        RESULTS.setdefault(self._testMethodName, {})["latest_not_source_complete"] = True

    async def test_http_v1_v2_real_provider_same_custody(self):
        fixture = self.fixture()
        self.assertEqual(self.prepare(fixture)["status"], "PASS")
        selector = self.selector(fixture)
        for selected in (None, selector):
            context = self.service_context(fixture, selected)
            self.events.clear()
            report = await H.serve(context)
            self.assertEqual(report["status"], "PASS", report)
            self.assertEqual(self.saved(context), report)
            provider = self.providers[-1]
            self.assertEqual(provider.observed_offer["status"], "OFFERED")
            if selected is None:
                self.assertEqual(report["schema"], "DMKN_V5_WORKSPACE_SERVICE_RESULT_V1")
                self.assertEqual(report["namespace"], fixture.namespace)
                self.assertNotIn("index_view", report)
                self.assertNotIn("projection_closed", report["cleanup"])
            else:
                self.assertEqual(report["schema"], "DMKN_V5_WORKSPACE_SERVICE_RESULT_V2")
                self.assertEqual(report["namespace"], BASE.namespace)
                self.assertEqual(report["source_namespace"], fixture.namespace)
                self.assertEqual(report["coverage"], H.COVERAGE)
                self.assertEqual(report["index_view"]["snapshot_id"], selector["expected_snapshot_id"])
                self.assertEqual(provider.observed_offer["summary"]["snapshot_id"],
                                 selector["expected_snapshot_id"])
                self.assertIs(provider.index, self.views[-1].index)
                self.assertIsNot(provider.index, self.served_workspace.index)
                self.assertIs(provider.custody, self.served_workspace.modules)
                self.assertIs(provider.packets, self.served_workspace.packets)
                self.assertTrue(report["cleanup"]["projection_closed"])
                self.assertLess(self.events.index("http.stop"), self.events.index("projection.close"))
                self.assertLess(self.events.index("projection.close"), self.events.index("workspace.close"))
            RESULTS.setdefault(self._testMethodName, {}).setdefault("services", []).append(report)
        crossed = self.service_context(fixture, selector)
        crossed.parameters["schema"] = H.SCHEMA
        with self.assertRaises(ValueError): H._parameters(crossed)
        no_view = self.service_context(fixture)
        no_view.parameters["schema"] = H.SCHEMA_V2
        with self.assertRaises(ValueError): H._parameters(no_view)

    async def test_advertised_v2_and_pure_builder_selection(self):
        fixture = self.fixture()
        self.assertEqual(self.prepare(fixture)["status"], "PASS")
        selector = self.selector(fixture)
        context = self.advertised_context(fixture, selector)
        self.events.clear()
        with patch.object(H, "_parameters", wraps=H._parameters) as proxy:
            report = await A.serve(context)
        self.assertEqual(proxy.call_args.args[0].parameters["schema"], H.SCHEMA_V2)
        self.assertEqual(proxy.call_args.args[0].parameters["index_view"], selector)
        self.assertEqual(report["status"], "PASS", report)
        self.assertEqual(report["namespace"], BASE.namespace)
        self.assertEqual(report["source_namespace"], fixture.namespace)
        self.assertEqual(report["coverage"], H.COVERAGE)
        self.assertEqual(self.channels[-1].config["namespace"], BASE.namespace)
        route = context.parameters["location"]["routes"][0]
        self.assertEqual(report["route_dispatch"][0]["route_key"],
            A.P.route_key(BASE.namespace, route["features"], route["stripe"]))
        ready = json.loads((context.location_workspace/"service-ready.json").read_bytes())
        self.assertEqual(ready["index_view"], report["index_view"])
        self.assertEqual(ready["coverage"], H.COVERAGE)
        self.assertLess(self.events.index("location.close"), self.events.index("http.stop"))
        self.assertLess(self.events.index("http.stop"), self.events.index("projection.close"))
        self.assertLess(self.events.index("projection.close"), self.events.index("workspace.close"))
        for command, schema in (("serve", H.SCHEMA_V2), ("serve-advertised", A.SCHEMA_V2)):
            params = {"schema": schema, "index_view": selector}
            if command == "serve-advertised": params["location"] = {}
            before = deepcopy(params)
            result = D.builtin_parameters(RETAINED, D.LOCATION_ROLE, command, params)
            self.assertEqual(result["schema"], schema)
            self.assertEqual(result["index_view"], selector)
            self.assertEqual(params, before)
            if command == "serve-advertised":
                self.assertEqual(result["location"]["installation_root"], str(RETAINED/"base"))
            for wrong in ("unknown", A.SCHEMA_V2 if command == "serve" else H.SCHEMA_V2):
                with self.assertRaises(ValueError):
                    D.builtin_parameters(RETAINED, D.LOCATION_ROLE, command, {**params, "schema": wrong})
            default = {"location": {}} if command == "serve-advertised" else {}
            self.assertEqual(D.builtin_parameters(RETAINED, D.LOCATION_ROLE, command, default)["schema"],
                             D.ENTRY_SCHEMAS[command])
        self.assertIn("v5/client/base_projection.py", D.required_sources(D.LOCATION_ROLE))
        RESULTS[self._testMethodName]["advertised_service"] = report

    async def test_cleanup_stale_start_cancel_and_uncertain_close(self):
        fixture = self.fixture()
        self.assertEqual(self.prepare(fixture)["status"], "PASS")
        selector = self.selector(fixture)
        for fault in ("provider-constructor", "http-start", "location-start"):
            self.fault, self.events = fault, []
            context = (self.advertised_context(fixture, selector) if fault == "location-start"
                       else self.service_context(fixture, selector))
            report = await (A.serve(context) if fault == "location-start" else H.serve(context))
            self.assert_failed(report)
            self.assertTrue(report["cleanup"]["projection_closed"])
            self.assertTrue(report["cleanup"]["workspace_closed"])
            self.assertLess(self.events.index("projection.close"), self.events.index("workspace.close"))
            self.assertFalse((context.location_workspace/"service-ready.json").exists())
            workspace = self.open_workspace(fixture)
            workspace.close()
        self.fault = None
        self.provider_started.clear()
        cancelled = self.service_context(fixture, selector)
        task = asyncio.create_task(H.serve(cancelled))
        self.tasks.append(task)
        await asyncio.wait_for(self.provider_started.wait(), 3)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError): await task
        report = self.saved(cancelled)
        self.assert_failed(report)
        self.assertTrue(report["cleanup"]["projection_closed"])
        self.assertTrue(report["cleanup"]["workspace_closed"])
        stale = self.service_context(fixture, {**selector, "expected_snapshot_id": "00"*32})
        count = len(self.providers)
        report = await H.serve(stale)
        self.assert_failed(report)
        self.assertEqual(len(self.providers), count)
        self.assertFalse((stale.location_workspace/"service-ready.json").exists())
        self.assertTrue(report["cleanup"]["workspace_closed"])
        # The helper owns target-close fallbacks. Inject exactly there, leaving
        # the source workspace and its original Store close implementation real.
        original = S.Store.close
        def fail_target(index):
            if index.root.name == "base-projection-index":
                raise ValueError("INJECTED_TARGET_CLOSE")
            return original(index)
        uncertain = self.service_context(fixture, selector)
        with patch.object(S.Store, "close", fail_target):
            report = await H.serve(uncertain)
        self.assert_failed(report)
        self.assertFalse(report["cleanup"]["projection_closed"])
        self.assertTrue(report["cleanup"]["workspace_closed"])
        self.assertIsNone(self.views[-1].index.db)
        workspace = self.open_workspace(fixture)
        view = self.view(workspace, selector)
        view.close()
        workspace.close()
        RESULTS[self._testMethodName]["uncertain_cleanup"] = report


SELECTED = (
    "test_two_namespaces_one_held_export",
    "test_namespace_record_and_feature_isolation",
    "test_finite_preflight_and_exclusive_borrow",
    "test_partial_quota_uncertainty_and_explicit_reconciliation",
    "test_latest_cut_is_explicit_not_all_source_coverage",
    "test_http_v1_v2_real_provider_same_custody",
    "test_advertised_v2_and_pure_builder_selection",
    "test_cleanup_stale_start_cancel_and_uncertain_close",
)


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output": raise ValueError("OUTPUT_REQUIRED")
    F.need(Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
           and sys.dont_write_bytecode and not sys.flags.optimize, "CANONICAL_ISOLATED_CONTROLS")
    OUTPUT = Path(sys.argv[2])
    F.need(OUTPUT.is_dir() and OUTPUT.resolve() == OUTPUT
           and OUTPUT.is_relative_to(PROJECT/"experiments"), "EXISTING_CANONICAL_OUTPUT_REQUIRED")
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestSuite(ProjectionControls(name) for name in SELECTED))
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "selected": list(SELECTED), "results": RESULTS,
        "scope": "REAL_STRUCTURAL_CUSTODY_INDEX_WORKSPACE_WITH_INERT_HTTP_LOCATION",
        "mathematical_acceptance": False, "native_calls": 0, "proof_calls": 0,
        "service_socket_calls": 0, "location_process_calls": 0,
        "sources": {name: hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() for name in (
            "base_projection/client/base_projection.py", "base_projection/client/serve_workspace.py",
            "base_projection/client/serve_advertised.py", "base_projection/distribution.py",
            "base_projection/controls.py", "instantiation_discovery/controls.py")}}
    with (OUTPUT/"controls-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

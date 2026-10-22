"""Finite exact-packet controls: actual HTTP/SQLite, inert unverified receipts.

Higher facade methods are separately AST-extracted with labelled owner doubles.
No cryptographic admission, native checker, Node runtime or existing state opens.
Root alone selects execution. All fixtures and failed attempts remain retained.
"""
import ast
import asyncio
from contextlib import ExitStack, nullcontext
from copy import deepcopy
from dataclasses import asdict
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from types import MethodType, SimpleNamespace
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SELF = Path("software/v5/exact_packet/controls.py")
MAP = PROJECT/"experiments/v5-local-checks/distribution-managed-storage-01-input.json"
MAP_BYTES = 2813368
MAP_SHA = "a629df82718f6a9d0560cacbfdc459739c15a56a1f2a46dd87929a1db51c22a4"
REPLACE = ("evidence_network/transport.py", "placement/controller.py",
           "client/workspace_evidence.py", "client/workspace_staged.py",
           "client/semantic_reader.py", "client/managed_owner.py")
MIB, IMAGE = 1024**2, "7a"*32
OUTPUT = CODE = C = B = F = WV = WS = SR = PC = PL = P = EP = EC = ET = DT = None
MS = AB = ENV = EXPECTED = LP = CONTACT = None
SOURCES, OBSERVED, FORBIDDEN, LOOP_ERRORS, PORTS = {}, {}, [], [], set()


def need(ok, reason):
    if not ok: raise ValueError(reason)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def ordinary(path):
    need(path.is_absolute() and path.resolve() == path and all(
        not p.is_symlink() and not p.is_junction() for p in (path, *path.parents)),
        "CONTROL_ORDINARY_PATH")
    return path


def write_new(path, raw):
    need(path.is_relative_to(OUTPUT) and not os.path.lexists(path), "CONTROL_FRESH_OUTPUT")
    with path.open("xb") as stream: need(stream.write(raw) == len(raw), "CONTROL_SHORT_WRITE")


def stage():
    global CODE
    root = OUTPUT/"sources"
    need(Path(__file__).resolve() == root/SELF, "CONTROL_SNAPSHOT_EXECUTION_REQUIRED")
    ordinary(MAP); need(MAP.stat().st_size == MAP_BYTES, "CONTROL_MAP_SIZE")
    raw = MAP.read_bytes(); need(sha(raw) == MAP_SHA, "CONTROL_MAP_PIN")
    basis = json.loads(raw)["sdk_sources"]
    selection = json.loads((OUTPUT/"selection.json").read_bytes())
    pins = selection["sources"]
    need(len(basis) == 129 and type(pins) is dict, "CONTROL_SOURCE_MAP")
    CODE = OUTPUT/"selected-code"; CODE.mkdir()
    for logical, original in sorted(basis.items()):
        relative = Path(original["path"]).relative_to(PROJECT).as_posix()
        expected, size = original["sha256"], original["bytes"]
        suffix = logical.removeprefix("v5/")
        if logical.startswith("v5/") and suffix in REPLACE:
            relative = "software/v5/exact_packet/"+suffix
            need(relative in pins, "CONTROL_REPLACEMENT_NOT_SELECTED")
            expected, size = pins[relative], None
        else:
            need(pins.get(relative) == expected, "CONTROL_BASE_NOT_SELECTED")
        source = ordinary(root/relative)
        need(source.is_file() and 0 < source.stat().st_size <= 2*MIB, "CONTROL_SOURCE_BOUND")
        data = source.read_bytes()
        need(sha(data) == expected and (size is None or len(data) == size), "CONTROL_SOURCE_PIN")
        target = CODE/logical; target.parent.mkdir(parents=True, exist_ok=True)
        write_new(target, data)
        need(target.read_bytes() == data, "CONTROL_STAGING_READBACK")
        SOURCES[logical] = dict(source=relative, bytes=len(data), sha256=expected)
    need(len(SOURCES) == 129 and all("v5/"+x in SOURCES for x in REPLACE), "CONTROL_EXACT_129")
    need(not any(x in sys.modules for x in ("placement", "modules", "client", "discovery")),
         "CONTROL_EARLY_PRODUCT_IMPORT")
    sys.path[:0] = [str(CODE/"v5"), str(CODE/"portable")]


def forbidden(*args, **kwargs):
    FORBIDDEN.append("FORBIDDEN_PROCESS_OR_MATHEMATICAL_VERIFICATION")
    raise AssertionError(FORBIDDEN[-1])


def configuration(terminal=True):
    return dict(schema=WV.CONCLUSION_FINGERPRINT_SCHEMA,
        discovery_profile=dict(schema="DMKN_MODULE_EXPORT_CONCLUSION_FINGERPRINT_PROFILE_V1", paths=[[]]),
        wire_profile=EC.public_profile(IMAGE, terminal_i=terminal), terminal_receipt_bytes=4096,
        module_limits=dict(modules=8, groups=16, declarations=32, bodies=8, logical_bytes=MIB, db_pages=256),
        packet_limits=dict(packets=32, offers=64, offers_per_module=16, packet_bytes=65536,
                           logical_bytes=MIB, db_pages=256),
        index_limits=dict(max_objects=8, max_postings=1024, max_features=128,
                          max_snapshots=16, max_logical_bytes=4*MIB, max_db_pages=2048),
        packet_envelope=asdict(ENV()), max_operations=8, max_report_bytes=MIB, ledger_pages=256)


def extract(module, cls, names):
    """Exact selected method bodies; decorators intentionally not executed here."""
    tree = ast.parse(Path(module.__file__).read_bytes(), filename=module.__file__)
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cls]
    need(len(classes) == 1, "CONTROL_EXACT_CLASS")
    nodes = [n for n in classes[0].body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
             and n.name in names]
    need({n.name for n in nodes} == set(names), "CONTROL_EXACT_METHODS")
    for node in nodes: node.decorator_list = []
    scope = dict(module.__dict__)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), module.__file__, "exec",
                 dont_inherit=True), scope)
    return {name: scope[name] for name in names}


class Controls(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.root = OUTPUT/("c"+str(SELECTED.index(self._testMethodName)+1).zfill(2)); self.root.mkdir()
        self.fixtures, self.acquisitions, self.controllers = [], [], []
        self.routes = []; self.loop = asyncio.get_event_loop()
        self.old_handler = self.loop.get_exception_handler()
        self.loop.set_exception_handler(lambda loop, ctx: LOOP_ERRORS.append(
            dict(test=self._testMethodName, message=str(ctx.get("message", "")),
                 exception=repr(ctx.get("exception")))))

    async def asyncTearDown(self):
        try:
            for fixture in reversed(self.fixtures):
                await fixture.provider.stop(); PORTS.discard(fixture.endpoint.port)
            for acquisition in reversed(self.acquisitions):
                if not acquisition.closed: acquisition.close()
            for controller in reversed(self.controllers):
                if not controller.closed: controller.close()
            for fixture in reversed(self.fixtures):
                fixture.source_packets.close(); fixture.source_modules.close(); fixture.w.close()
            OBSERVED.setdefault(self._testMethodName, {})["http_routes"] = list(self.routes)
        finally: self.loop.set_exception_handler(self.old_handler)

    async def fixture(self, terminal=True):
        root = self.root/str(len(self.fixtures)+1); root.mkdir()
        w = WV.Workspace.open(root/"workspace", configuration(terminal), create=True)
        modules = MS.ModuleStore(root/"source-modules", C, B.FOUNDATION, B.POLICY,
                                 w.config["module_limits"], create=True)
        packets = EC.PacketStore(root/"source-packets", EC.public_profile(IMAGE, terminal_i=True),
            w.config["packet_limits"], envelope=ENV(), terminal_receipt_bytes=4096, create=True)
        name = [["s", "exactPacketFixture"]]
        spec = dict(schema=C.SPEC_SCHEMA, foundation=B.FOUNDATION, policy=B.POLICY,
            groups=[dict(kind="ordinary", declarations=[dict(name=name, kind="theorem", universes=0,
                type=["sort", ["zero"]], value_hash=None, meta={})])])
        module, opening = C.module_id(spec), C.group_opening(spec, 0)
        modules.put_group(module, opening)
        journal = EXPECTED(C.summarize(spec), 0, B.RELATION_IMAGE)
        variants = sorted((sha(raw), raw) for raw in [EP.pack_terminal_i(journal,
            b"EXACT-CONTROL-INERT-UNVERIFIED-RECEIPT-"+bytes([n]), aggregate_image=IMAGE,
            envelope=ENV(), terminal_i=True) for n in range(9)])
        for unused, raw in variants: packets.put(module, raw)
        digest, raw = variants[-1]
        provider = ET.CompositeProvider(index=w.index, custody=modules, packets=packets,
            max_requests=64, max_reply_bytes=8*MIB, operation_ms=3000)
        original = provider.dispatch
        def observe(route, request, **kwargs):
            self.routes.append(route); return original(route, request, **kwargs)
        provider.dispatch = observe
        endpoint = await provider.start("127.0.0.1", 0); PORTS.add(endpoint.port)
        export = w.adapter.encode_opening(module, name, opening)
        described = w.adapter.describe(export)
        resolved = {**w.adapter.resolve(described["record"], export), "opening": opening}
        fixture = SimpleNamespace(root=root, w=w, source_modules=modules, source_packets=packets,
            provider=provider, endpoint=endpoint, module=module, name=name, opening=opening,
            journal=journal, raw=raw, entry=dict(packet_sha256=digest, packet_bytes=len(raw)),
            export=export, described=described, resolved=resolved, variants=variants)
        self.fixtures.append(fixture); return fixture

    def acquisition(self, f, *, requests=32, expiring=False):
        budget = AB(time.monotonic()+45, dict(requests=requests, reply_bytes=MIB,
            verify_attempts=1, verification_input_bytes=1, worker_cpu_seconds=1))
        endpoint = f.endpoint
        if expiring:
            policy = LP.OwnerEgressPolicy(self.egress(f))
            endpoint = CONTACT(endpoint, time.monotonic()+40, policy, budget)
        result = ET.EvidenceAcquisition(f.w.adapter, {"source": endpoint}, f.w.packets.profile,
            budget, f.w.modules, f.w.packets, verifier=None)
        self.acquisitions.append(result); return result

    @staticmethod
    def egress(f):
        return dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
                    test_endpoints=[dict(host="127.0.0.1", port=f.endpoint.port)])

    async def test_01_beyond_eight_actual_http_and_unchanged_offered_gate(self):
        f = await self.fixture(); a = self.acquisition(f)
        offered = await a.offers("source", f.module, max_offers=8)
        self.assertEqual(len(offered["packets"]), 8); self.assertNotIn(f.entry, offered["packets"])
        before = a.budget.used.copy(); offers = set(a._offers)
        with self.assertRaisesRegex(ValueError, "NOT_OFFERED"):
            await a.packet("source", f.module, f.entry)
        self.assertEqual(a.budget.used, before)
        result = await a.packet_exact("source", f.module, f.entry)
        self.assertFalse(result["mathematical_acceptance"])
        self.assertEqual(f.w.packets.get(f.entry["packet_sha256"], f.entry["packet_bytes"]), f.raw)
        self.assertEqual(a._offers, offers)
        self.assertEqual(a.budget.used["requests"], 2)
        self.assertEqual(a.budget.used["reply_bytes"]-before["reply_bytes"], len(f.raw))
        held = f.w.packets.status()
        await a.packet_exact("source", f.module, f.entry)
        self.assertEqual(f.w.packets.status(), held)
        self.assertEqual(a.budget.used["requests"], 3)
        self.assertEqual(a.budget.used["verify_attempts"], 0)
        with self.assertRaisesRegex(ValueError, "NOT_OFFERED"):
            await a.packet("source", f.module, f.entry)
        OBSERVED[self._testMethodName] = dict(variants=9, offered=8, selected_rank=9,
            actual_http=True, fake_offer_added=False, mathematical_acceptance=False)

    async def test_02_exact_input_frozen_during_actual_request(self):
        f = await self.fixture(); a = self.acquisition(f); demand = dict(f.entry)
        original = f.provider.dispatch
        def mutate(route, request, **kwargs):
            reply = original(route, request, **kwargs)
            if route == DT.PACKET_ROUTE: demand.update(packet_sha256="ff"*32, packet_bytes=1)
            return reply
        f.provider.dispatch = mutate
        result = await a.packet_exact("source", f.module, demand)
        self.assertEqual({key: result[key] for key in f.entry}, f.entry)
        self.assertEqual(f.w.packets.get(f.entry["packet_sha256"], len(f.raw)), f.raw)
        self.assertFalse(a._offers)

    async def test_03_hash_size_target_and_profile_refusals(self):
        f = await self.fixture(); a = self.acquisition(f); before = f.w.packets.status()
        for entry in ({**f.entry, "packet_bytes": True}, {**f.entry, "packet_bytes": 65537},
                      {**f.entry, "packet_sha256": "malformed"}, {**f.entry, "extra": "not-permitted"}):
            with self.assertRaises(ValueError): await a.packet_exact("source", f.module, entry)
        self.assertEqual(a.budget.used["requests"], 0); self.assertEqual(f.provider.requests, 0)
        saved_profile = deepcopy(a.profile)
        a.profile["aggregate_image"] = "01"*32
        with self.assertRaisesRegex(ValueError, "PROFILE"):
            await a.packet_exact("source", f.module, f.entry)
        a.profile = saved_profile
        self.assertEqual(a.budget.used["requests"], 0)
        for label, module, entry in (
            ("missing-sha", f.module, {**f.entry, "packet_sha256": "00"*32}),
            ("wrong-size", f.module, {**f.entry, "packet_bytes": len(f.raw)+1}),
            ("wrong-module", "01"*32, f.entry)):
            with self.subTest(label=label), self.assertRaises((ValueError, asyncio.IncompleteReadError, ConnectionError)):
                await a.packet_exact("source", module, entry)
            self.assertIsNone(a.budget.pending); self.assertEqual(f.w.packets.status(), before)
        self.assertEqual(a.budget.used["requests"], 3)
        original = f.provider.dispatch
        def malicious(route, request, **kwargs):
            reply = original(route, request, **kwargs)
            return bytes([reply[0]^1])+reply[1:] if route == DT.PACKET_ROUTE else reply
        with patch.object(f.provider, "dispatch", malicious):
            with self.assertRaisesRegex(ValueError, "HASH_BINDING"):
                await a.packet_exact("source", f.module, f.entry)
        self.assertEqual(f.w.packets.status(), before)
        crossed = await self.fixture(terminal=False); b = self.acquisition(crossed)
        with self.assertRaises(ValueError): await b.packet_exact("source", crossed.module, crossed.entry)
        self.assertEqual(crossed.w.packets.status()["counts"]["packets"], 0)
        self.assertEqual(b.budget.used["requests"], 1)
        OBSERVED[self._testMethodName] = dict(malicious_payload_injection="SERVER_DISPATCH_ONE_BYTE",
            wrong_profile="REAL_V1_CUSTODY_REFUSES_TERMINAL_I_V2", mathematical_acceptance=False)

    async def test_04_budget_contact_and_commit_expiry(self):
        f = await self.fixture(); a = self.acquisition(f, requests=1)
        await a.offers("source", f.module, max_offers=8)
        count = f.provider.requests
        with self.assertRaisesRegex(ValueError, "AGGREGATE_BUDGET"):
            await a.packet_exact("source", f.module, f.entry)
        self.assertEqual(f.provider.requests, count)
        b = self.acquisition(f, expiring=True)
        b.endpoints["source"]._expires = time.monotonic()-1
        with self.assertRaisesRegex(ValueError, "CONTACT_EXPIRED"):
            await b.packet_exact("source", f.module, f.entry)
        self.assertEqual(b.budget.used["requests"], 1)
        self.assertEqual(b.budget.used["reply_bytes"], len(f.raw)); self.assertIsNone(b.budget.pending)
        self.assertEqual(f.provider.requests, count)
        c = self.acquisition(f)
        with self.assertRaisesRegex(ValueError, "ENDPOINT_NOT_CONFIGURED"):
            await c.packet_exact("missing", f.module, f.entry)
        self.assertEqual(c.budget.used["requests"], 0)
        original = f.w.packets.put
        def expire_at_commit(module, raw, *, before_commit=None):
            def expiry():
                self.assertTrue(f.w.packets.db.in_transaction)
                with patch.object(c.budget, "active", side_effect=ValueError("INJECTED_COMMIT_EXPIRY")):
                    before_commit()
            return original(module, raw, before_commit=expiry)
        with patch.object(f.w.packets, "put", expire_at_commit):
            with self.assertRaisesRegex(ValueError, "INJECTED_COMMIT_EXPIRY"):
                await c.packet_exact("source", f.module, f.entry)
        self.assertEqual(f.w.packets.status()["counts"]["packets"], 0)
        self.assertEqual(c.budget.used["requests"], 1); self.assertEqual(c.budget.used["reply_bytes"], len(f.raw))
        self.assertFalse(f.w.packets.db.in_transaction)
        with self.assertRaisesRegex(ValueError, "PUBLIC_CLIENT_ADMISSION_REQUIRED"):
            c.admit()
        count = f.provider.requests
        for retired in (False, True):
            ended = self.acquisition(f)
            if retired: ended.retire_generation()
            else: ended.close()
            with self.assertRaisesRegex(ValueError, "ORIGIN_OR_CLOSED"):
                await ended.packet_exact("source", f.module, f.entry)
            self.assertEqual(ended.budget.used["requests"], 0)
        self.assertEqual(f.provider.requests, count)
        OBSERVED[self._testMethodName] = dict(commit_fault="INJECTED_BUDGET_EXPIRY_AT_REAL_SQLITE_COMMIT",
            rollback=True, failed_requests_charged=True)

    async def test_05_actual_placement_exact_and_duplicate_accounting(self):
        f = await self.fixture(); now = int(time.time()*1000)
        limits = {key: 16 if key in ("placements", "index_calls", "recovery_passes", "new_cells")
                  else 128 if key == "requests" else 128*MIB for key in P.RESOURCES}
        cfg = dict(schema=P.CONFIG_SCHEMA, service_epoch=sha(b"exact-control-epoch"),
            generation=sha(str(f.root).encode()), namespace=f.w.adapter.namespace,
            wire_profile_id=f.w.packets.profile_id, admission_close_ms=now+60000,
            retention_not_after_ms=now+120000, max_grants=4, max_requests=4, max_cells=4,
            max_runs=2, ledger_pages=256, limits=limits)
        ledger = PL.PlacementLedger.open(f.w, cfg, create=True)
        controller = PC.PlacementController(ledger, self.egress(f)); self.controllers.append(controller)
        service = controller.start_service(wall_seconds=45, controller_cpu_seconds=20, calls=128)
        source = dict(host=f.endpoint.host, port=f.endpoint.port, tls=False, server_name=None)
        token = controller.issue_token(service, source, write_until_ms=now+30000,
            retention_until_ms=now+100000, limits=limits)
        fp = next(x for x in f.described["specs"] if x["tag"] == "conclusion-fingerprint")
        value = dict(schema=P.REQUEST_SCHEMA, generation=cfg["generation"], namespace=cfg["namespace"],
            wire_profile_id=cfg["wire_profile_id"], module_id=f.module, relative_name=f.name,
            export_id=C.export_id(f.module, f.name), fingerprint=fp, cell=P.cell(f.w.adapter, fp)[0],
            export_object_sha256=sha(f.export), export_object_bytes=len(f.export), opening_max_bytes=4096,
            **f.entry, bodies=[], retention_end_ms=now+80000)
        raw = F.compact(value)
        with patch.object(ET.EvidenceAcquisition, "offers", side_effect=AssertionError("PLACEMENT_MUST_NOT_OFFER")):
            result = await controller.submit(service, token["token"], raw)
        self.assertEqual(result["phase"], "RECEIPT_COMMITTED")
        quote = P.quote(value, new_cell=True, index_logical_cap=f.w.config["index_limits"]["max_logical_bytes"])
        self.assertEqual(result["outcome"]["reservation"], quote)
        self.assertEqual(self.routes, ["/v5/modules/group", DT.PACKET_ROUTE])
        self.assertEqual(result["outcome"]["observed"]["acquisition"]["budget"]["used"]["requests"], 2)
        for key in P.FLAGS: self.assertFalse(result["outcome"][key])
        self.assertEqual(f.w.packets.get(f.entry["packet_sha256"], len(f.raw)), f.raw)
        used = ledger.db.execute("SELECT used FROM meta WHERE id=1").fetchone()[0]
        self.assertEqual(json.loads(used), quote)
        self.assertEqual(await controller.submit(service, token["token"], raw), result)
        self.assertEqual(ledger.db.execute("SELECT used FROM meta WHERE id=1").fetchone()[0], used)
        again = controller.issue_token(service, source, write_until_ms=now+30000,
            retention_until_ms=now+100000, limits=limits)
        second = await controller.submit(service, again["token"], raw)
        self.assertNotEqual(result["request_id"], second["request_id"])
        quote2 = P.quote(value, new_cell=False, index_logical_cap=f.w.config["index_limits"]["max_logical_bytes"])
        self.assertEqual(second["outcome"]["reservation"], quote2)
        self.assertEqual(json.loads(ledger.db.execute("SELECT used FROM meta WHERE id=1").fetchone()[0]),
                         {key: quote[key]+quote2[key] for key in quote})
        self.assertEqual(len(self.routes), 2)
        OBSERVED[self._testMethodName] = dict(real_ledger_index_http=True,
            duplicate_request_no_reservation=True, new_request_local_reuse_charged=True,
            mathematical_acceptance=False)

    def facade(self, f, mutate=None):
        """Owner/issuer doubles; exact selected facade method bodies only."""
        token, candidate, calls = object(), object(), []
        async def packet(kind, provider, module, entry):
            calls.append((kind, deepcopy(entry)))
            if mutate is not None: mutate()
        async def body(provider, resolved, digest, maximum):
            calls.append(("body", digest, maximum))
            if mutate is not None: mutate()
            return {"body": {"fixture": True}}
        acquisition = SimpleNamespace(_offers=set(), packet=lambda *a: packet("offered", *a),
            packet_exact=lambda *a: packet("exact", *a), body=body,
            custody_ready=lambda *a: calls.append(("readback", deepcopy(a[1]))))
        def selected(value):
            need(value is candidate, "DOUBLE_FOREIGN_CANDIDATE")
            return "source", deepcopy(f.resolved)
        def admission(*args): calls.append(("admission-double", args[0])); return token
        owner = SimpleNamespace(open_group=lambda *a: calls.append(("open-group-double",)))
        obj = SimpleNamespace(_candidate=selected, _charge=lambda raw: None,
            _acquisition=acquisition, _packet_cache={}, _store=lambda fn, *a: fn(*a),
            workspace=SimpleNamespace(packets=SimpleNamespace(get=lambda *a: f.raw)),
            grant=SimpleNamespace(remaining_seconds=lambda: 30,
                _limits={"imports": {"max_sources": 4, "max_members": 4, "data_bytes": MIB}}),
            _admit_evidence=admission, _warrant=lambda unused: ("I", object(), f.raw, {"journal": f.journal}),
            receipt=owner, aggregate=owner, delta=owner, _expected=lambda *a: None,
            _active=lambda: None, _staged={}, _staging_counts={"packets_staged": 0})
        return obj, candidate, token, calls

    async def test_06_extracted_direct_facade_dispatch_freeze_and_cache_guard(self):
        f = await self.fixture(); entry = dict(f.entry)
        bodies = [dict(digest="02"*32, max_bytes=4096), dict(digest="03"*32, max_bytes=2048)]
        def mutate():
            entry["packet_sha256"] = "ff"*32
            bodies[0]["digest"] = "ee"*32
            bodies[1].update(digest="dd"*32, max_bytes=1)
        obj, candidate, token, calls = self.facade(f, mutate)
        methods = extract(WV, "CommonsClient", ("acquire", "acquire_exact", "_acquire_packet"))
        for name, fn in methods.items(): setattr(obj, name, MethodType(fn, obj))
        self.assertIs(await obj.acquire_exact(candidate, entry, bodies=bodies), token)
        self.assertIn(("exact", f.entry), calls)
        self.assertEqual([x for x in calls if x[0] == "body"],
                         [("body", "02"*32, 4096), ("body", "03"*32, 2048)])
        self.assertTrue(any(x[0] == "admission-double" for x in calls))
        before = len(calls)
        with self.assertRaisesRegex(ValueError, "UNOFFERE[D]"): await obj.acquire(candidate, f.entry)
        self.assertEqual(len(calls), before)
        with self.assertRaisesRegex(ValueError, "FOREIGN_CANDIDATE"): await obj.acquire_exact(object(), f.entry)
        obj._packet_cache[(f.entry["packet_sha256"], f.entry["packet_bytes"], C.canonical(f.opening["summary"]))] = token
        def stale(unused): raise ValueError("DOUBLE_STALE_WARRANT")
        obj._warrant = stale
        with self.assertRaisesRegex(ValueError, "STALE_WARRANT"): await obj.acquire_exact(candidate, f.entry)
        self.assertEqual(len(calls), before)

        # The retained final exact-journal guard must still run. The issuance
        # and changing warrant below are explicit doubles, not proof evidence.
        obj, candidate, token, calls = self.facade(f)
        for name, fn in methods.items(): setattr(obj, name, MethodType(fn, obj))
        other = EXPECTED(f.opening["summary"], 1, B.RELATION_IMAGE)
        journals = iter((f.journal, other))
        obj._warrant = lambda unused: ("I", object(), f.raw, {"journal": next(journals)})
        with self.assertRaisesRegex(ValueError, "FINAL_TARGET"):
            await obj.acquire_exact(candidate, f.entry, expected_exact_journal=f.journal)
        self.assertTrue(any(x[0] == "admission-double" for x in calls))
        OBSERVED[self._testMethodName] = dict(scope="EXTRACTED_METHODS_WITH_OWNER_AND_ADMISSION_DOUBLES",
            actual_admission=False, input_snapshot=True, later_body_snapshot=True,
            stale_cache_refusal=True, final_exact_journal_refusal=True)

    async def test_07_extracted_staged_facade_keeps_untrusted_token(self):
        f = await self.fixture(); entry = dict(f.entry)
        obj, candidate, unused, calls = self.facade(f, lambda: entry.update(packet_sha256="ff"*32))
        methods = extract(WS, "CommonsClient", ("stage_packet", "stage_packet_exact", "_stage_packet", "_staging_census"))
        for name, fn in methods.items(): setattr(obj, name, MethodType(fn, obj))
        obj._inspect = lambda raw: EP.inspect_evidence(raw, ENV(), aggregate_image=IMAGE,
            terminal_receipt_bytes=4096, terminal_i=True)
        obj._structural_members = lambda raw, kind, exact: WS._member_inventory(raw, kind, exact,
            envelope=ENV(), aggregate_image=IMAGE, max_members=4)
        token = await obj.stage_packet_exact(candidate, entry)
        self.assertIs(type(token), WS.StagedEvidence)
        snapshot = C.parse_json(obj._staged[token][0])
        self.assertEqual(snapshot["selection"]["packet_sha256"], f.entry["packet_sha256"])
        self.assertFalse(obj._staged[token][1]); self.assertIn(("exact", f.entry), calls)
        self.assertFalse(any(x[0] == "admission-double" for x in calls))
        obj._staged.clear()
        with self.assertRaisesRegex(ValueError, "UNOFFERE[D]"): await obj.stage_packet(candidate, f.entry)
        OBSERVED[self._testMethodName] = dict(scope="EXTRACTED_STAGING_WITH_ACQUISITION_DOUBLE",
            actual_packet_parse=True, mathematical_acceptance=False)

    async def test_08_extracted_semantic_reader_exact_dispatch_and_demand_guard(self):
        f = await self.fixture(); candidate, token, calls = object(), object(), []
        entry = dict(f.entry)
        snapshot = dict(status="STAGED_UNTRUSTED_EVIDENCE", mathematical_acceptance=False,
            admission_consumed=False, provider="source", candidate=f.resolved,
            selection=dict(module=f.module, summary=f.opening["summary"], journal=list(f.journal), **f.entry),
            members=[dict(module=f.module, summary=f.opening["summary"], journal=list(f.journal))])
        async def stage(kind, chosen, demand):
            calls.append((kind, deepcopy(demand))); entry["packet_sha256"] = "ff"*32; return token
        obj = SimpleNamespace(_call=nullcontext, _encode=C.canonical,
            _description=lambda chosen: {"provider": "source", **f.resolved},
            _address=lambda desc: (f.module, C.name_key(f.name)), _selected={}, _pending={},
            _origin=candidate, _limits={"modules": 4}, _revision=0,
            _grant=SimpleNamespace(_limits={"imports": {"max_sources": 4, "max_members": 4}}),
            _client=SimpleNamespace(stage_packet=lambda *a: stage("offered", *a),
                stage_packet_exact=lambda *a: stage("exact", *a), describe_staged=lambda t: deepcopy(snapshot)),
            _retain=lambda raw: None, _choose_member=lambda *a: None, _group=lambda desc: None)
        methods = extract(SR, "SemanticReader", ("stage", "stage_exact", "_stage"))
        for name, fn in methods.items(): setattr(obj, name, MethodType(fn, obj))
        result = await obj.stage_exact(candidate, entry)
        self.assertEqual(result["status"], "STAGED"); self.assertEqual(calls, [("exact", f.entry)])
        self.assertEqual((await obj.stage_exact(candidate, f.entry))["status"], "NO_PROGRESS")
        with self.assertRaisesRegex(ValueError, "VARIANT_CONFLICT"):
            await obj.stage_exact(candidate, {**f.entry, "packet_sha256": "aa"*32})
        obj._selected.clear()
        with self.assertRaisesRegex(ValueError, "UNDEMANDED_MODULE"):
            await obj.stage_exact(object(), f.entry)
        await obj.stage(candidate, f.entry)
        self.assertEqual(calls[-1], ("offered", f.entry))
        OBSERVED[self._testMethodName] = dict(scope="EXTRACTED_READER_WITH_CLIENT_AND_CALL_GUARD_DOUBLES",
            actual_journal_parse=True, mathematical_acceptance=False)


SELECTED = tuple("test_"+name for name in (
    "01_beyond_eight_actual_http_and_unchanged_offered_gate", "02_exact_input_frozen_during_actual_request",
    "03_hash_size_target_and_profile_refusals", "04_budget_contact_and_commit_expiry",
    "05_actual_placement_exact_and_duplicate_accounting", "06_extracted_direct_facade_dispatch_freeze_and_cache_guard",
    "07_extracted_staged_facade_keeps_untrusted_token", "08_extracted_semantic_reader_exact_dispatch_and_demand_guard"))


def main():
    global OUTPUT,C,B,F,WV,WS,SR,PC,PL,P,EP,EC,ET,DT,MS,AB,ENV,EXPECTED,LP,CONTACT
    need(len(sys.argv) == 3 and sys.argv[1] == "--output", "CONTROL_OUTPUT_REQUIRED")
    OUTPUT = ordinary(Path(sys.argv[2]))
    need(OUTPUT.is_dir() and OUTPUT.is_relative_to(PROJECT) and os.name == "nt"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, "CONTROL_ISOLATED_WINDOWS")
    stage()
    with ExitStack() as guards:
        guards.enter_context(patch.object(subprocess, "Popen", forbidden))
        guards.enter_context(patch.object(os, "system", forbidden))
        C = importlib.import_module("modules.codec"); B = importlib.import_module("aggregate_claims.bindings")
        F = importlib.import_module("discovery.formal_features")
        WV = importlib.import_module("client.workspace_evidence"); WS = importlib.import_module("client.workspace_staged")
        SR = importlib.import_module("client.semantic_reader")
        PC = importlib.import_module("placement.controller"); PL = importlib.import_module("placement.ledger")
        P = importlib.import_module("placement.codec"); EP = importlib.import_module("evidence_network.packet")
        EC = importlib.import_module("evidence_network.custody"); ET = importlib.import_module("evidence_network.transport")
        DT = importlib.import_module("delta.transport"); MS = importlib.import_module("custody.module_store")
        AB = importlib.import_module("transport.receipt_client").AcquisitionBudget
        ENV = importlib.import_module("mixed_claims.packet").Envelope
        EXPECTED = importlib.import_module("delta_claims.claims").expected_journal
        LP = importlib.import_module("location.protocol")
        CONTACT = importlib.import_module("transport.located_receipts")._ExpiringContact
        for module, name in (("admission.verifier", "ReceiptVerifier"),
                             ("aggregate_claims.aggregate_admission", "AggregateReceiptVerifier"),
                             ("mixed_claims.receiver", "MixedDeltaVerifier")):
            guards.enter_context(patch.object(getattr(importlib.import_module(module), name), "receive", forbidden))
        dial = asyncio.open_connection
        async def loopback(host, port, **kwargs):
            need(host == "127.0.0.1" and port in PORTS, "CONTROL_LOOPBACK_SELECTED_PORT_ONLY")
            return await dial(host, port, **kwargs)
        guards.enter_context(patch.object(asyncio, "open_connection", loopback))
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
    success = result.wasSuccessful() and result.testsRun == len(SELECTED) and not result.skipped \
        and not FORBIDDEN and not LOOP_ERRORS and not PORTS
    report = dict(schema="DMKN_V5_EXACT_PACKET_CONTROLS_V1", status="PASS" if success else "FAIL",
        tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
        selected=list(SELECTED), sources=SOURCES, observations=OBSERVED, forbidden_calls=FORBIDDEN,
        loop_errors=LOOP_ERRORS, source_map_sha256=MAP_SHA, mathematical_acceptance=False,
        native_calls=0, proof_calls=0, node_calls=0,
        receipts="INERT_UNVERIFIED_SYNTACTIC_PACKET_FIXTURES",
        higher_facade_scope="EXACT_AST_METHODS_WITH_EXPLICIT_OWNER_AND_ADMISSION_DOUBLES_NOT_LIVE_OWNER_PASS",
        scope="REAL_LOOPBACK_HTTP_STRUCTURAL_CUSTODY_PLACEMENT_AND_CHANGED_API_DISPATCH_ONLY")
    write_new(OUTPUT/"exact-packet-controls-result.json", json.dumps(report, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode()+b"\n")
    return 0 if success else 1


if __name__ == "__main__": raise SystemExit(main())

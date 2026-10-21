"""Ten new-boundary controls. Real stores/controller; memory HTTP and simulated Node.

No old suite is imported. Inert receipt bytes are never admitted. Socket/native/
proof/process entry points are forbidden; source qualification needs root launch.
"""
import asyncio
from contextlib import ExitStack
from copy import deepcopy
from dataclasses import asdict
import hashlib
import importlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = Path(__file__).resolve().parents[1]
MAP = PROJECT/"experiments/v5-local-checks/distribution-terminal-i-01-input.json"
MAP_SHA, MAP_BYTES = "d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0", 2805479
MIB = 1024**2
REPLACEMENTS = {
    "v5/admission/pin_phase.py":("standalone_validation/admission/pin_phase.py","ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881"),
    "v5/mixed_claims/imports_atomic.py":("standalone_validation/mixed_claims/imports_atomic.py","8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595"),
    "v5/mixed_claims/receiver.py":("incremental_native/mixed_claims/receiver.py","5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b"),
    "v5/discovery/discovery_store.py":("selective_placement/discovery/discovery_store.py","1c8543d4903754174b80d107ee923116ddb402d41a3b5af3f1d255abdfc6a328"),
}
ADDITIONS = {
    "v5/placement/__init__.py":("selective_placement/placement/__init__.py","8fe08470d7fd15e96d1305f0e49a8b359cb53ce0c542bf7473b68d869159112e"),
    "v5/placement/codec.py":("selective_placement/placement/codec.py","6f32569d4807f96130350b85233161603f6860f082c75f81a8bfacf4f0a58999"),
    "v5/placement/ledger.py":("selective_placement/placement/ledger.py","d955990c347ed466617c752893dded8b8494dd266a050b045352c77c48f21a91"),
    "v5/placement/controller.py":("selective_placement/placement/controller.py","ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49"),
    "v5/placement/network.py":("placement_network/placement/network.py","1ec5c452ec129ae033f0577ebac6223e2cf3192d4724a3d31fe2e5c27a06cd4b"),
    "v5/placement/advertisement.py":("placement_network/placement/advertisement.py","b5523f82f6d5eba4ba9e72639888f1c9da014f298aa9c1081c76aa3f920f35a6"),
    "v5/client/serve_placement.py":("placement_network/client/serve_placement.py","07c60c4f33401d41694228d0f6bde35d9148e769947b75211e9ed4098ec68674"),
}
OUTPUT = C = B = F = WV = P = EP = EC = ENV = EXPECTED = S = J = N = L = LS = None
SOURCES, OBSERVED, FORBIDDEN, LOOP_ERRORS = {}, {}, [], []
IMAGE = "5e"*32
INERT_RECEIPT = b"NETWORK-CONTROL-INERT-NOT-A-CERTIFICATE"
READ = dict(host="127.0.0.1",port=43521,tls=False,server_name=None)
INTAKE = dict(host="127.0.0.1",port=43522,tls=False,server_name=None)
SOURCE_ENDPOINT = dict(host="127.0.0.1",port=43523,tls=False,server_name=None)
EGRESS = dict(schema="DMKN_V5_OWNER_EGRESS_V1",mode="loopback-test",public_ports=[],
    test_endpoints=[dict(host="127.0.0.1",port=p) for p in (43521,43522,43523,43524)])


def sha(raw): return hashlib.sha256(raw).hexdigest()


def write_new(path,raw):
    with path.open("xb") as stream:
        if stream.write(raw) != len(raw): raise ValueError("CONTROL_SHORT_WRITE")


def stage(output):
    if MAP.stat().st_size != MAP_BYTES: raise ValueError("CURRENT_MAP_SIZE")
    raw = MAP.read_bytes()
    if sha(raw) != MAP_SHA or len(raw) != MAP_BYTES: raise ValueError("CURRENT_MAP_PIN")
    rows = json.loads(raw)["sdk_sources"]
    if len(rows) != 114 or set(rows)&set(ADDITIONS): raise ValueError("CURRENT_MAP_SHAPE")
    rows = dict(rows)
    for logical,(relative,digest) in {**REPLACEMENTS,**ADDITIONS}.items():
        rows[logical] = dict(path=str(SOURCE/relative),sha256=digest)
    code = output/"selected-code"; code.mkdir()
    for logical,row in sorted(rows.items()):
        path = Path(row["path"])
        if logical not in REPLACEMENTS and logical not in ADDITIONS:
            path = SOURCE/path.relative_to(PROJECT/"software/v5")
        raw = path.read_bytes()
        if not 0 < len(raw) <= 2*MIB or sha(raw) != row["sha256"] or \
                "bytes" in row and len(raw) != row["bytes"]:
            raise ValueError("SELECTED_SOURCE_PIN:"+logical)
        target = code/logical; target.parent.mkdir(parents=True,exist_ok=True)
        write_new(target,raw)
        if target.read_bytes() != raw: raise ValueError("SELECTED_SOURCE_READBACK")
        SOURCES[logical] = dict(source=str(path),bytes=len(raw),sha256=sha(raw))
    if len(SOURCES) != 121: raise ValueError("EXACT_SOURCE_COUNT")
    if any(name in sys.modules for name in ("placement","modules","client","discovery")):
        raise ValueError("EARLY_PRODUCT_IMPORT")
    sys.path[:0] = [str(code/"v5"),str(code/"portable")]


def forbidden(*unused,**ignored):
    FORBIDDEN.append("FORBIDDEN_PROCESS_SOCKET_OR_MATH")
    raise AssertionError("FORBIDDEN_PROCESS_SOCKET_OR_MATH")


class MemoryServer:
    def __init__(self,callback,host,port):
        self.callback,self.live = callback,True
        self.sockets = [SimpleNamespace(getsockname=lambda:(host,port))]
    def close(self): self.live = False
    def is_serving(self): return self.live
    async def wait_closed(self): return None


class MemoryWriter:
    def __init__(self): self.data,self.closed = bytearray(),False
    def write(self,raw):
        if self.closed: raise RuntimeError("MEMORY_WRITER_CLOSED")
        self.data.extend(raw)
    async def drain(self): await asyncio.sleep(0)
    def close(self): self.closed = True
    async def wait_closed(self): return None


def configuration():
    return dict(schema=WV.CONCLUSION_FINGERPRINT_SCHEMA,
        discovery_profile=dict(schema="DMKN_MODULE_EXPORT_CONCLUSION_FINGERPRINT_PROFILE_V1",paths=[[]]),
        wire_profile=EC.public_profile(IMAGE,terminal_i=True),terminal_receipt_bytes=4096,
        module_limits=dict(modules=8,groups=16,declarations=32,bodies=8,logical_bytes=MIB,db_pages=256),
        packet_limits=dict(packets=8,offers=16,offers_per_module=4,packet_bytes=65536,logical_bytes=MIB,db_pages=256),
        index_limits=dict(max_objects=8,max_postings=1024,max_features=128,max_snapshots=16,
                          max_logical_bytes=4*MIB,max_db_pages=2048),
        packet_envelope=asdict(ENV()),max_operations=8,max_report_bytes=MIB,ledger_pages=256)


class Controls(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.root = OUTPUT/("c"+str(SELECTED.index(self._testMethodName)+1).zfill(2)); self.root.mkdir()
        self.patches = ExitStack(); self.fixtures = []; self.node_calls = []
        self.entered,self.release = asyncio.Event(),asyncio.Event()
        self.mode = "ok"; self.servers = []
        self.patches.enter_context(patch.object(socket.socket,"__init__",forbidden))
        for name in ("open_connection","create_subprocess_exec","create_subprocess_shell"):
            self.patches.enter_context(patch.object(asyncio,name,forbidden))
        self.patches.enter_context(patch.object(asyncio,"start_server",self.memory_server))
        for name,method in (("start",self.node_start),("command",self.node_command),
                            ("close",self.node_close),("report",self.node_report)):
            # Bound control methods are installed as per-instance-independent
            # class wrappers; ordinary exact locator construction still occurs.
            if name == "report":
                replacement = lambda node,m=method:m(node)
            elif name == "command":
                async def replacement(node,*args,_method=method,**kw): return await _method(node,*args,**kw)
            else:
                async def replacement(node,_method=method): return await _method(node)
            self.patches.enter_context(patch.object(LS.ServiceLocationProcess,name,replacement))

    async def asyncSetUp(self):
        self.loop = asyncio.get_running_loop(); self.old_handler = self.loop.get_exception_handler()
        self.loop.set_exception_handler(lambda unused,context:LOOP_ERRORS.append(
            {"test":self._testMethodName,"code":"UNHANDLED_ASYNC_EXCEPTION"}))

    async def asyncTearDown(self):
        try:
            self.release.set()
            for f in reversed(self.fixtures):
                result = await f["service"].close()
                self.assertEqual(result["status"],"CLOSED",result["cleanup"])
                self.assertFalse(f["service"].intake_provider.tasks)
                self.assertFalse(f["service"].intake_provider.writers)
            self.assertTrue(all(not server.live for server in self.servers))
            OBSERVED.setdefault(self._testMethodName,{})["simulated_node_commands"] = list(self.node_calls)
        finally:
            self.loop.set_exception_handler(self.old_handler)

    def tearDown(self): self.patches.close()

    async def memory_server(self,callback,host,port,**unused):
        server = MemoryServer(callback,host,port); self.servers.append(server); return server

    async def node_start(self,node):
        node.process = SimpleNamespace(returncode=None)
        return dict(status="RUNNING",role="index-provider",namespace=node.config["namespace"],
                    global_complete=False,mathematical_acceptance=False)

    async def node_command(self,node,command,payload,*,until=None):
        self.assertLess(time.monotonic(),until)
        node.sequence += 1; self.node_calls.append(command)
        if command == "publish":
            f = next(x for x in self.fixtures if x["location"] is node)
            row = f["service"].advertisement.db.execute("SELECT phase FROM routes").fetchone()
            self.assertEqual(row,("DISPATCH_ATTEMPTED",))
            self.entered.set()
            if self.mode == "wait": await self.release.wait()
            if self.mode == "fail": raise OSError("SIMULATED_LOCATOR_FAILURE")
            return dict(route_key=f["value"]["cell"],status="HINT_DISPATCHED_UNACKNOWLEDGED",
                error=None,census=dict(add_provider_write=1,last_query_error="LOCAL-DIAGNOSTIC-ONLY"),
                remote_placement_confirmed=False,global_complete=False,mathematical_acceptance=False)
        if command == "stop": node.process.returncode = 0
        return dict(status="STOPPED" if command == "stop" else "RUNNING",role="index-provider",
                    namespace=node.config["namespace"],global_complete=False,mathematical_acceptance=False)

    async def node_close(self,node):
        node.closed = True
        if node.process is not None: node.process.returncode = 0

    def node_report(self,node):
        return dict(closed=node.closed,returncode=None if node.process is None else node.process.returncode,
                    channel_failed=False,forced_termination=False,commands=node.sequence,
                    simulation="NO_NODE_CHILD_OR_DHT_DISPATCH")

    async def fixture(self,*,lifetime=30,intake_requests=16):
        root = self.root/str(len(self.fixtures)+1); root.mkdir()
        for name in ("node-source","node-installation","node-work"): (root/name).mkdir()
        config = configuration()
        adapter = importlib.import_module("discovery.module_export_adapter").ModuleExportAdapter(
            C,B.FOUNDATION,B.POLICY,discovery_profile=config["discovery_profile"])
        now = int(time.time()*1000)
        allowance = {key:16 if key in ("placements","index_calls","recovery_passes","new_cells")
                     else 64 if key == "requests" else 128*MIB for key in P.RESOURCES}
        generation = dict(schema=P.CONFIG_SCHEMA,service_epoch=sha((str(root)+"epoch").encode()),
            generation=sha((str(root)+"generation").encode()),namespace=adapter.namespace,
            wire_profile_id=EC.profile_id(config["wire_profile"]),admission_close_ms=now+60000,
            retention_not_after_ms=now+120000,max_grants=4,max_requests=4,max_cells=2,max_runs=2,
            ledger_pages=256,limits=allowance)
        adoption = L.AdoptedLocationRuntime(root/"node-source",{x:"00"*32 for x in L.SOURCE_NAMES},
            installation_root=root/"node-installation",workspace_root=root/"node-work")
        node_limits = dict(service_ms=120000,operation_ms=1000,commands=60,advertised_keys=2)
        location = LS.ServiceLocationProcess(adoption,{x:"00"*32 for x in LS.ROLE_NAMES},
            dict(schema="DMKN_V5_MAINTAINED_LOCATION_ROLES_V1",role="index-provider",
                 state=str(root/"node-work/state"),namespace=adapter.namespace,egress=EGRESS,
                 endpoints=[READ],limits=node_limits),root/"node-work/evidence",deadline=time.monotonic()+90)
        limits = dict(lifetime_seconds=lifetime,controller_cpu_seconds=30,controller_calls=128,
            health_interval_ms=10000,journal_pages=256,
            read=dict(max_connections=2,max_requests=16,max_reply_bytes=MIB,operation_ms=1000),
            intake=dict(max_connections=2,max_requests=intake_requests,incoming_bytes=intake_requests*N.IN_RESERVE,
                        outgoing_bytes=intake_requests*N.OUT_RESERVE,operation_ms=5000))
        service = S.PlacementService.open(root/"workspace",config,generation,EGRESS,location,
            read_endpoint=READ,intake_endpoint=INTAKE,limits=limits,outer_deadline=time.monotonic()+120,
            create=True,placement_create=True,journal_create=True)
        f = dict(root=root,service=service,location=location,generation=generation)
        self.fixtures.append(f)
        await service.start()
        token = service.issue_token(SOURCE_ENDPOINT,write_until_ms=now+50000,
                                    retention_until_ms=now+110000,limits=allowance)
        name = [["s","wireControl"]]; expr = ["sort",["zero"]]
        spec = dict(schema=C.SPEC_SCHEMA,foundation=B.FOUNDATION,policy=B.POLICY,
            groups=[dict(kind="ordinary",declarations=[dict(name=name,kind="theorem",universes=0,
                type=expr,value_hash=None,meta={})])])
        module,opening = C.module_id(spec),C.group_opening(spec,0)
        export = adapter.encode_opening(module,name,opening)
        fingerprint = next(x for x in adapter.describe(export)["specs"] if x["tag"] == "conclusion-fingerprint")
        packet = EP.pack_terminal_i(EXPECTED(C.summarize(spec),0,B.RELATION_IMAGE),INERT_RECEIPT,
                                   aggregate_image=IMAGE,envelope=ENV(),terminal_i=True)
        service.workspace.modules.put_group(module,opening); service.workspace.packets.put(module,packet)
        value = dict(schema=P.REQUEST_SCHEMA,generation=generation["generation"],namespace=adapter.namespace,
            wire_profile_id=service.workspace.packets.profile_id,module_id=module,relative_name=name,
            export_id=C.export_id(module,name),fingerprint=fingerprint,cell=P.cell(adapter,fingerprint)[0],
            export_object_sha256=sha(export),export_object_bytes=len(export),opening_max_bytes=4096,
            packet_sha256=sha(packet),packet_bytes=len(packet),bodies=[],retention_end_ms=now+100000)
        raw = F.compact(value); rid = P.request_id(raw,token["grant_id"],generation["generation"])
        f.update(token=token["token"],raw=raw,rid=rid,value=value)
        return f

    def accept(self,f,route,payload):
        raw = N.request_bytes(route,f["token"],payload)
        reader = asyncio.StreamReader(limit=N.H.HEADER_MAX); writer = MemoryWriter()
        reader.feed_data(N.H._header("POST "+route+" HTTP/1.1",len(raw),"127.0.0.1:43522")+raw)
        reader.feed_eof()
        provider = f["service"].intake_provider
        old = set(provider.tasks); provider._accept(reader,writer)
        new = provider.tasks-old
        self.assertEqual(len(new),1)
        return next(iter(new)),writer

    async def wire(self,f,route,payload):
        task,writer = self.accept(f,route,payload); await task
        self.assertTrue(writer.closed)
        return F.strict(bytes(writer.data).split(b"\r\n\r\n",1)[1],N.REPLY_MAX)

    async def test_closed_envelope_maximum_and_overflow(self):
        token = "ab"*32
        overhead = len(F.compact({"x":""}))
        raw = F.compact({"x":"a"*(P.REQUEST_MAX-overhead)})
        self.assertEqual(len(raw),16384)
        wire = N.request_bytes(N.SUBMIT,token,raw)
        self.assertGreater(len(wire),16384); self.assertLessEqual(len(wire),N.SUBMIT_MAX)
        self.assertTrue(N.parse_request(N.SUBMIT,wire) == (token,raw),"ENVELOPE_ROUNDTRIP")
        for bad in (raw+b" ",F.compact({"x":"a"*(P.REQUEST_MAX-overhead+1)})):
            with self.assertRaises(ValueError): N.request_bytes(N.SUBMIT,token,bad)
        with self.assertRaises(ValueError): N.parse_request(N.SUBMIT,b"x"*(N.SUBMIT_MAX+1))
        with self.assertRaises(ValueError): N.parse_request(N.STATUS,F.compact(
            dict(schema=N.STATUS_SCHEMA,token=token,request_id="00"*32,extra=True)))
        OBSERVED[self._testMethodName] = dict(inner=16384,envelope=len(wire),source_effects=0)

    async def test_projection_removes_local_diagnostics_and_binds_success(self):
        f = await self.fixture(); s = f["service"]
        joined = await s.submit(f["token"],f["raw"],until=s.deadline)
        joined["placement"]["outcome"]["observed"]["acquisition"] = {"reason":f["token"]}
        checked = N.public_response(joined,dict(s.bindings),f["rid"])
        self.assertTrue(f["token"].encode() not in F.compact(checked),"SUCCESS_TOKEN_NOT_EXPOSED")
        self.assertTrue(b"LOCAL-DIAGNOSTIC-ONLY" not in F.compact(checked),"ROUTE_DIAGNOSTIC_NOT_EXPOSED")
        for field in N.BINDINGS:
            wrong = dict(s.bindings); wrong[field] = "ef"*32
            with self.assertRaises(ValueError): N.public_response(joined,wrong,f["rid"])
        partial = deepcopy(joined); partial["placement"].update(phase="INCOMPLETE",outcome={"reason":f["token"]})
        projected = N.public_response(partial,dict(s.bindings),f["rid"])
        self.assertTrue(projected["placement"]["outcome"] == dict(status="INCOMPLETE",code="PLACEMENT_INCOMPLETE"),
                        "INCOMPLETE_CLOSED_PROJECTION")
        self.assertTrue(f["token"].encode() not in F.compact(projected),"INCOMPLETE_TOKEN_NOT_EXPOSED")
        malicious = deepcopy(joined); malicious["route"]["error"] = f["token"]
        with self.assertRaises(ValueError): N.public_response(malicious,dict(s.bindings),f["rid"])
        # A distinct actual request fails after its durable reservation. Its
        # retained local diagnostic is deliberately secret-bearing; status and
        # duplicate submission must sanitize it without rewriting either row.
        original = s.ledger.request(f["rid"])
        fresh_value = deepcopy(f["value"]); fresh_value["retention_end_ms"] -= 1
        fresh_raw = F.compact(fresh_value)
        fresh_rid = P.request_id(fresh_raw,s.ledger.authenticate(f["token"])[0],f["generation"]["generation"])
        self.assertNotEqual(fresh_rid,f["rid"])
        with patch.object(s.controller,"_local_group",side_effect=OSError("LOCAL_ONLY:"+f["token"])):
            refused = await self.wire(f,N.SUBMIT,fresh_raw)
        self.assertEqual(refused["code"],"REFUSED_OR_INCOMPLETE")
        saved = s.ledger.request(fresh_rid)
        self.assertEqual(saved["phase"],"INCOMPLETE")
        self.assertTrue(f["token"] in saved["outcome"]["reason"],"LOCAL_DIAGNOSTIC_RETAINED")
        changes = (s.ledger.db.total_changes,s.advertisement.db.total_changes)
        observed = await self.wire(f,N.STATUS,fresh_rid)
        replay = await self.wire(f,N.SUBMIT,fresh_raw)
        self.assertTrue(observed == replay,"INCOMPLETE_REPLAY_UNCHANGED")
        self.assertTrue(observed["placement"]["outcome"] == dict(status="INCOMPLETE",code="PLACEMENT_INCOMPLETE"),
                        "SAVED_INCOMPLETE_CLOSED_PROJECTION")
        for response in (refused,observed,replay):
            self.assertTrue(f["token"].encode() not in F.compact(response),"SAVED_TOKEN_NOT_EXPOSED")
            self.assertTrue(b"LOCAL_ONLY" not in F.compact(response),"SAVED_DIAGNOSTIC_NOT_EXPOSED")
        self.assertEqual((s.ledger.db.total_changes,s.advertisement.db.total_changes),changes)
        self.assertTrue(s.ledger.request(fresh_rid) == saved,"SAVED_INCOMPLETE_UNCHANGED")
        self.assertTrue(s.ledger.request(f["rid"]) == original,"SAVED_COMPLETED_UNCHANGED")
        self.assertEqual(self.node_calls.count("publish"),1)
        OBSERVED[self._testMethodName] = dict(saved_incomplete_wire_observations=2,
            diagnostic_retained_locally=True,diagnostic_exposed=False,completed_receipt_unchanged=True)

    async def test_duplicate_wire_is_no_effect_observation(self):
        f = await self.fixture(); s = f["service"]
        first = await self.wire(f,N.SUBMIT,f["raw"])
        changes = (s.ledger.db.total_changes,s.advertisement.db.total_changes)
        publishes = self.node_calls.count("publish")
        second = await self.wire(f,N.SUBMIT,f["raw"])
        status = await self.wire(f,N.STATUS,f["rid"])
        self.assertTrue(first == second == status,"DUPLICATE_AND_STATUS_UNCHANGED")
        self.assertEqual((s.ledger.db.total_changes,s.advertisement.db.total_changes),changes)
        self.assertEqual(self.node_calls.count("publish"),publishes)
        self.assertEqual(self.node_calls.count("publish"),1)
        self.assertEqual(s.workspace.index.status()["objects"],1)
        self.assertTrue(f["token"].encode() not in s.ledger._path.read_bytes(),"TOKEN_NOT_IN_CORE_LEDGER")
        self.assertTrue(f["token"].encode() not in s.advertisement._path.read_bytes(),"TOKEN_NOT_IN_ROUTE_JOURNAL")
        OBSERVED[self._testMethodName] = dict(real_store_transactions=True,simulated_publish_calls=1,
                                            observation_requests=2,new_duplicate_effects=0)

    async def test_single_intake_busy_is_charged_not_queued(self):
        f = await self.fixture(); self.mode = "wait"
        first,writer = self.accept(f,N.SUBMIT,f["raw"])
        await asyncio.wait_for(self.entered.wait(),2)
        busy = await self.wire(f,N.SUBMIT,f["raw"])
        self.assertEqual(busy["code"],"BUSY")
        self.assertFalse(first.done())
        self.assertEqual(f["service"].ledger.db.execute("SELECT count(*) FROM requests").fetchone()[0],1)
        self.release.set(); await first
        report = f["service"].intake_provider.report()
        self.assertEqual(report["used"]["busy"],1); self.assertEqual(report["used"]["requests"],2)
        self.assertEqual(report["used"]["incoming_reserved"],2*N.IN_RESERVE)
        self.assertEqual(report["used"]["outgoing_reserved"],2*N.OUT_RESERVE)

    async def test_dispatch_failure_stays_charged_and_duplicate_does_not_retry(self):
        f = await self.fixture(); self.mode = "fail"; s = f["service"]
        response = await self.wire(f,N.SUBMIT,f["raw"])
        self.assertEqual(response["code"],"REFUSED_OR_INCOMPLETE")
        row = s.advertisement.db.execute("SELECT phase FROM routes").fetchone()
        self.assertEqual(row,("DISPATCH_ATTEMPTED",))
        self.mode = "ok"
        observed = await self.wire(f,N.STATUS,f["rid"])
        self.assertEqual(observed["placement"]["phase"],"RECEIPT_COMMITTED")
        self.assertEqual(observed["route"]["status"],"DISPATCH_UNCERTAIN")
        duplicate = await self.wire(f,N.SUBMIT,f["raw"])
        self.assertTrue(observed == duplicate,"UNCERTAIN_DUPLICATE_UNCHANGED")
        self.assertEqual(self.node_calls.count("publish"),1)

    async def test_post_dispatch_journal_failure_is_not_no_attempt(self):
        f = await self.fixture(); journal = f["service"].advertisement
        actual = journal._transaction; calls = 0
        def fault(*args,**kw):
            nonlocal calls
            calls += 1
            if calls == 2: raise OSError("SIMULATED_JOURNAL_COMMIT_FAILURE")
            return actual(*args,**kw)
        with patch.object(journal,"_transaction",fault):
            response = await self.wire(f,N.SUBMIT,f["raw"])
        self.assertEqual(response["code"],"REFUSED_OR_INCOMPLETE")
        observed = await self.wire(f,N.STATUS,f["rid"])
        self.assertEqual(observed["route"]["status"],"DISPATCH_UNCERTAIN")
        self.assertEqual(self.node_calls.count("publish"),1)
        self.assertEqual(journal.db.execute("SELECT count(*) FROM routes").fetchone()[0],1)

    async def test_cancelled_intake_retains_receipt_and_releases_slot(self):
        f = await self.fixture(); s = f["service"]; self.mode = "wait"
        task,writer = self.accept(f,N.SUBMIT,f["raw"])
        await asyncio.wait_for(self.entered.wait(),2)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError): await task
        self.assertTrue(writer.closed); self.assertFalse(s.intake_provider._busy)
        self.assertFalse(s.advertisement._busy); self.assertFalse(s.controller._busy)
        self.mode = "ok"
        status = await self.wire(f,N.STATUS,f["rid"])
        self.assertEqual(status["placement"]["phase"],"RECEIPT_COMMITTED")
        self.assertEqual(status["route"]["status"],"DISPATCH_UNCERTAIN")
        self.assertEqual(s.intake_provider.report()["used"]["cancelled"],1)

    async def test_automatic_lifetime_closes_original_resources(self):
        f = await self.fixture(lifetime=2); s = f["service"]
        allocation = json.loads(s.advertisement.db.execute("SELECT allocation FROM runs").fetchone()[0])
        self.assertEqual(allocation["commands"],allocation["health"]+2*allocation["cells"]+1)
        self.assertLessEqual(allocation["commands"],60)
        await asyncio.wait_for(s._monitor_task,3)
        result = await s.close()
        self.assertEqual(result["status"],"CLOSED")
        self.assertTrue(s.grant.closed); self.assertTrue(s.workspace._closed)
        self.assertTrue(all(result["cleanup"][key] for key in ("intake_closed","location_closed","read_closed",
                                                              "journal_closed","controller_closed","workspace_closed")))
        with self.assertRaises(ValueError): s._active()
        self.assertEqual(self.node_calls.count("stop"),1)

    async def test_client_rejects_changed_binding_without_network(self):
        f = await self.fixture(); s = f["service"]
        client = N.PlacementClient(EGRESS,INTAKE,dict(s.bindings),f["token"],deadline=s.deadline,
            requests=2,incoming_bytes=2*N.OUT_RESERVE,outgoing_bytes=2*N.IN_RESERVE)
        wrong = deepcopy(f["value"]); wrong["generation"] = "ed"*32
        with self.assertRaises(N.PlacementWireError) as held: await client.submit(F.compact(wrong))
        self.assertEqual(held.exception.code,"CLIENT_REQUEST_INVALID")
        self.assertEqual(client.report()["used"]["requests"],0)
        client._contact["port"] = SOURCE_ENDPOINT["port"]
        with self.assertRaises(N.PlacementWireError) as held: await client.status(f["rid"])
        self.assertEqual(held.exception.code,"CLIENT_BINDING_CHANGED")
        self.assertEqual(client.report()["used"]["requests"],0)
        self.assertTrue(f["token"].encode() not in F.compact(client.report()),"CLIENT_REPORT_OMITS_TOKEN")
        client.close()
        joined = await s.submit(f["token"],f["raw"],until=s.deadline)
        response = F.compact(N.public_response(joined,dict(s.bindings),f["rid"]))
        for failure_mode,expected_code in (("binding","CLIENT_BINDING_CHANGED"),("close","CLEANUP_UNCERTAIN"),
                                           ("cleanup_cancel",None),("send_and_cleanup_cancel",None)):
            client = N.PlacementClient(EGRESS,INTAKE,dict(s.bindings),f["token"],deadline=s.deadline,
                requests=1,incoming_bytes=N.OUT_RESERVE,outgoing_bytes=N.IN_RESERVE)
            class ResponseReader(asyncio.StreamReader):
                async def read(self,count=-1):
                    value = await super().read(count)
                    if count == 1 and failure_mode == "binding":
                        client._contact["port"] = SOURCE_ENDPOINT["port"]
                    if count == 1 and failure_mode == "send_and_cleanup_cancel":
                        raise asyncio.CancelledError()
                    return value
            class ClosingWriter(MemoryWriter):
                def close(self):
                    super().close()
                    if failure_mode == "close": raise OSError("PRIVATE_CLOSE_DIAGNOSTIC:"+f["token"])
                async def wait_closed(self):
                    if failure_mode in ("cleanup_cancel","send_and_cleanup_cancel"):
                        raise asyncio.CancelledError()
                    return await super().wait_closed()
            reader,writer = ResponseReader(limit=N.H.HEADER_MAX),ClosingWriter()
            reader.feed_data(N.H._header("HTTP/1.1 200 OK",len(response))+response); reader.feed_eof()
            async def memory_connection(*unused,**ignored): return reader,writer
            caught = None
            with patch.object(asyncio,"open_connection",memory_connection):
                try: await client.submit(f["raw"])
                except BaseException as error: caught = error
            # Catch even an accidentally raw exception before asserting so a
            # regression cannot leak its deliberately token-bearing diagnostic.
            if expected_code is None:
                self.assertTrue(type(caught) is asyncio.CancelledError,"CLIENT_CANCELLATION_PROPAGATED")
            else:
                self.assertTrue(type(caught) is N.PlacementWireError,"CLIENT_CLOSED_ERROR_TYPE")
                self.assertTrue(caught.code == expected_code and str(caught) == expected_code,"CLIENT_CLOSED_ERROR_CODE")
                self.assertTrue(caught.uncertain,"POST_ALLOCATION_SUBMIT_UNCERTAIN")
            self.assertTrue(writer.closed); self.assertFalse(client._busy)
            used = client.report()["used"]
            self.assertEqual(used["requests"],1); self.assertEqual(used["uncertain_submits"],1)
            self.assertGreater(used["attempted_outgoing"],0)
            self.assertEqual(used["incoming_reserved"],N.OUT_RESERVE)
            self.assertEqual(used["outgoing_reserved"],N.IN_RESERVE)
            if failure_mode != "binding":
                self.assertTrue(client.closed); self.assertEqual(used["cleanup_errors"],1)
            self.assertTrue(f["token"].encode() not in F.compact(client.report()),"FAILED_CLIENT_REPORT_OMITS_TOKEN")
            client.close()
        OBSERVED[self._testMethodName] = dict(preallocation_refusals=2,
            postallocation_memory_transport_failures=4,uncertain_submit_outcomes=4,
            cleanup_cancellations=2,cancellation_doublecount=0,actual_client_dials=0)

    async def test_unauthorized_unknown_status_and_wire_exhaustion(self):
        f = await self.fixture(intake_requests=2); s = f["service"]
        before = (s.ledger.db.total_changes,s.advertisement.db.total_changes)
        wrong = dict(f,token="00"*32)
        refused = await self.wire(wrong,N.SUBMIT,f["raw"])
        unknown = await self.wire(f,N.STATUS,"ed"*32)
        for response in (refused,unknown):
            self.assertEqual(response["schema"],N.ERROR_SCHEMA)
            self.assertEqual(response["code"],"REFUSED_OR_INCOMPLETE")
            self.assertTrue(f["token"].encode() not in F.compact(response),"REFUSAL_OMITS_TOKEN")
            self.assertTrue(wrong["token"].encode() not in F.compact(response),"REFUSAL_OMITS_UNKNOWN_TOKEN")
            self.assertEqual(set(response),{"schema","status","code","mathematical_acceptance"})
        self.assertEqual((s.ledger.db.total_changes,s.advertisement.db.total_changes),before)
        self.assertEqual(s.ledger.db.execute("SELECT count(*) FROM requests").fetchone()[0],0)
        self.assertEqual(self.node_calls.count("publish"),0)
        provider = s.intake_provider
        raw = N.request_bytes(N.SUBMIT,f["token"],f["raw"])
        reader = asyncio.StreamReader(limit=N.H.HEADER_MAX); writer = MemoryWriter()
        reader.feed_data(N.H._header("POST "+N.SUBMIT+" HTTP/1.1",len(raw),"127.0.0.1:43522")+raw)
        reader.feed_eof(); provider._accept(reader,writer)
        self.assertTrue(writer.closed); self.assertFalse(writer.data); self.assertFalse(provider.tasks)
        report = provider.report()
        self.assertEqual(report["used"]["requests"],2)
        self.assertEqual(report["used"]["incoming_reserved"],2*N.IN_RESERVE)
        self.assertEqual(report["used"]["outgoing_reserved"],2*N.OUT_RESERVE)
        self.assertFalse(report["accepting"])
        self.assertEqual((s.ledger.db.total_changes,s.advertisement.db.total_changes),before)
        OBSERVED[self._testMethodName] = dict(charged_refusals=2,third_closed_without_dispatch=True,
                                            core_or_route_mutations=0)


SELECTED = (
    "test_closed_envelope_maximum_and_overflow",
    "test_projection_removes_local_diagnostics_and_binds_success",
    "test_duplicate_wire_is_no_effect_observation",
    "test_single_intake_busy_is_charged_not_queued",
    "test_dispatch_failure_stays_charged_and_duplicate_does_not_retry",
    "test_post_dispatch_journal_failure_is_not_no_attempt",
    "test_cancelled_intake_retains_receipt_and_releases_slot",
    "test_automatic_lifetime_closes_original_resources",
    "test_client_rejects_changed_binding_without_network",
    "test_unauthorized_unknown_status_and_wire_exhaustion",
)


def main():
    global OUTPUT,C,B,F,WV,P,EP,EC,ENV,EXPECTED,S,J,N,L,LS
    if len(sys.argv) != 3 or sys.argv[1] != "--output": raise ValueError("OUTPUT_REQUIRED")
    OUTPUT = Path(sys.argv[2])
    if not OUTPUT.is_absolute() or not OUTPUT.is_dir() or not OUTPUT.is_relative_to(PROJECT):
        raise ValueError("CANONICAL_EXISTING_OUTPUT")
    if not (os.name == "nt" and sys.flags.isolated and sys.flags.no_site
            and sys.dont_write_bytecode and not sys.flags.optimize): raise ValueError("ISOLATED_WINDOWS")
    stage(OUTPUT)
    with ExitStack() as guards:
        guards.enter_context(patch.object(subprocess,"Popen",forbidden))
        guards.enter_context(patch.object(os,"system",forbidden))
        def load(name): return importlib.import_module(name)
        C=load("modules.codec"); B=load("aggregate_claims.bindings"); F=load("discovery.formal_features")
        WV=load("client.workspace_evidence"); P=load("placement.codec")
        EP=load("evidence_network.packet"); EC=load("evidence_network.custody")
        ENV=load("mixed_claims.packet").Envelope; EXPECTED=load("delta_claims.claims").expected_journal
        S=load("client.serve_placement"); J=load("placement.advertisement"); N=load("placement.network")
        L=load("location.controller"); LS=load("location.controller_services")
        for module,name in (("admission.verifier","ReceiptVerifier"),
                            ("aggregate_claims.aggregate_admission","AggregateReceiptVerifier"),
                            ("mixed_claims.receiver","MixedDeltaVerifier")):
            guards.enter_context(patch.object(getattr(load(module),name),"receive",forbidden))
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
    passed = result.wasSuccessful() and result.testsRun == len(SELECTED) and not result.skipped \
             and not FORBIDDEN and not LOOP_ERRORS
    report = dict(schema="DMKN_PLACEMENT_NETWORK_CONTROLS_V1",status="PASS" if passed else "FAIL",
        selected=list(SELECTED),tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
        skipped=len(result.skipped),observations=OBSERVED,sources=SOURCES,
        forbidden_calls=FORBIDDEN,loop_errors=LOOP_ERRORS,actual_network_calls=0,actual_node_children=0,
        actual_native_calls=0,actual_proof_calls=0,mathematical_acceptance=False,
        transport="MEMORY_HTTP_FRAMING_AND_SIMULATED_NODE_COMMANDS_REAL_SQLITE_AND_CONTROLLER",
        receipt_bytes="INERT_UNVERIFIED_FIXTURES_NEVER_ADMITTED",old_suites_imported=False,
        scope="CHANGED_WIRE_DISPATCH_LIFECYCLE_BOUNDARIES_NOT_TLS_DHT_OR_GLOBAL_PLACEMENT")
    write_new(OUTPUT/"placement-network-controls-result.json",json.dumps(report,sort_keys=True,
        separators=(",",":"),allow_nan=False).encode()+b"\n")
    return 0 if passed else 1


if __name__ == "__main__": raise SystemExit(main())

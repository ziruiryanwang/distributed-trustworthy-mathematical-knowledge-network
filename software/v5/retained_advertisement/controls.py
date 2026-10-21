"""New retained-route boundaries: real SQLite/controller, simulated local services.

No old test module is imported. Inert packet bytes never enter a verifier.
Only root may select execution of these source-only controls.
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
import sqlite3
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
    "v5/placement/advertisement.py":("retained_advertisement/placement/advertisement.py","5aa23ee76115355ad319ae4acfd4ab418e010166e53b6ed02c82eb25d34d4510"),
    "v5/client/serve_placement.py":("retained_advertisement/client/serve_placement.py","7e735337d595894e25fd07a8dcc9ad8cd3ba9f1c042ba930684b7798232cb7fa"),
}
OUTPUT = C = B = F = WV = P = EP = EC = ENV = EXPECTED = S = J = N = L = LS = PC = None
SOURCES, OBSERVED, FORBIDDEN, LOOP_ERRORS = {}, {}, [], []
IMAGE = "5e"*32
INERT_RECEIPT = b"RETAINED-ROUTE-CONTROL-NOT-A-MATHEMATICAL-CERTIFICATE"
READ = dict(host="127.0.0.1",port=43531,tls=False,server_name=None)
INTAKE = dict(host="127.0.0.1",port=43532,tls=False,server_name=None)
SOURCE_ENDPOINT = dict(host="127.0.0.1",port=43533,tls=False,server_name=None)
OTHER_READ = dict(host="127.0.0.1",port=43534,tls=False,server_name=None)
EGRESS = dict(schema="DMKN_V5_OWNER_EGRESS_V1",mode="loopback-test",public_ports=[],
    test_endpoints=[dict(host="127.0.0.1",port=p) for p in (43531,43532,43533,43534)])


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
        self.patches = ExitStack(); self.fixtures = []; self.sessions = []; self.node_calls = []
        self.entered,self.release = asyncio.Event(),asyncio.Event()
        self.mode = "ok"; self.servers = []; self.after_dispatch = None
        self.patches.enter_context(patch.object(socket.socket,"__init__",forbidden))
        for name in ("open_connection","create_subprocess_exec","create_subprocess_shell"):
            self.patches.enter_context(patch.object(asyncio,name,forbidden))
        self.patches.enter_context(patch.object(asyncio,"start_server",self.memory_server))
        for name,method in (("start",self.node_start),("command",self.node_command),
                            ("close",self.node_close),("report",self.node_report)):
            if name == "report": replacement = lambda node,m=method:m(node)
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
            for row in reversed(self.sessions):
                s = row["service"]
                result = await s.close()
                self.assertEqual(result["status"],"CLOSED",result["cleanup"])
                self.assertTrue(result["cleanup"]["retained_closed"])
                self.assertFalse(s.intake_provider.tasks); self.assertFalse(s.intake_provider.writers)
                self.assertTrue(s._retained_task is None or s._retained_task.done())
            self.assertTrue(all(not server.live for server in self.servers))
            OBSERVED.setdefault(self._testMethodName,{})["simulated_node_commands"] = list(self.node_calls)
        finally: self.loop.set_exception_handler(self.old_handler)

    def tearDown(self): self.patches.close()

    async def memory_server(self,callback,host,port,**unused):
        server = MemoryServer(callback,host,port); self.servers.append(server); return server

    async def node_start(self,node):
        node.process = SimpleNamespace(returncode=None)
        return dict(status="RUNNING",role="index-provider",namespace=node.config["namespace"],
                    global_complete=False,mathematical_acceptance=False)

    async def node_command(self,node,command,payload,*,until=None):
        self.assertLess(time.monotonic(),until)
        node.sequence += 1
        row = next(x for x in self.sessions if x["location"] is node)
        s,f = row["service"],row["fixture"]
        self.node_calls.append(dict(command=command,run=s.advertisement.run))
        if command == "publish":
            saved = s.advertisement.db.execute("SELECT phase FROM routes WHERE cell=? AND run=?",
                (f["value"]["cell"],s.advertisement.run)).fetchone()
            self.assertEqual(saved,("DISPATCH_ATTEMPTED",))
            self.entered.set()
            if self.mode == "wait": await self.release.wait()
            if self.mode == "fail": raise OSError("SIMULATED_RETAINED_DISPATCH_FAILURE")
            if self.after_dispatch is not None: self.after_dispatch()
            return dict(route_key=f["value"]["cell"],status="HINT_DISPATCHED_UNACKNOWLEDGED",
                error=None,census=dict(add_provider_write=1,last_query_error=None),
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

    async def open_service(self,f,*,create=False,generation=None,read=None):
        cfg = f["generation"] if generation is None else generation
        endpoint = READ if read is None else read
        f["open_attempts"] += 1
        run = f["root"]/"node-work"/("run-"+str(f["open_attempts"])); run.mkdir()
        adoption = L.AdoptedLocationRuntime(f["root"]/"node-source",{x:"00"*32 for x in L.SOURCE_NAMES},
            installation_root=f["root"]/"node-installation",workspace_root=f["root"]/"node-work")
        node_limits = dict(service_ms=120000,operation_ms=1000,commands=60,advertised_keys=2)
        location = LS.ServiceLocationProcess(adoption,{x:"00"*32 for x in LS.ROLE_NAMES},
            dict(schema="DMKN_V5_MAINTAINED_LOCATION_ROLES_V1",role="index-provider",
                 state=str(run/"state"),namespace=cfg["namespace"],egress=EGRESS,
                 endpoints=[endpoint],limits=node_limits),run/"evidence",deadline=time.monotonic()+90)
        service = S.PlacementService.open(f["root"]/"workspace",f["config"],cfg,EGRESS,location,
            read_endpoint=endpoint,intake_endpoint=INTAKE,limits=f["limits"],outer_deadline=time.monotonic()+120,
            create=create,placement_create=create,journal_create=create)
        f["service"] = service
        self.sessions.append(dict(service=service,location=location,fixture=f))
        await service.start()
        return service

    async def fixture(self,*,max_runs=2,commit=True):
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
            retention_not_after_ms=now+120000,max_grants=4,max_requests=4,max_cells=2,max_runs=max_runs,
            ledger_pages=256,limits=allowance)
        limits = dict(lifetime_seconds=30,controller_cpu_seconds=30,controller_calls=128,
            health_interval_ms=10000,journal_pages=256,
            read=dict(max_connections=2,max_requests=16,max_reply_bytes=MIB,operation_ms=1000),
            intake=dict(max_connections=2,max_requests=16,incoming_bytes=16*N.IN_RESERVE,
                        outgoing_bytes=16*N.OUT_RESERVE,operation_ms=5000))
        f = dict(root=root,config=config,generation=generation,limits=limits,open_attempts=0)
        self.fixtures.append(f); s = await self.open_service(f,create=True)
        token = s.issue_token(SOURCE_ENDPOINT,write_until_ms=now+50000,
                             retention_until_ms=now+110000,limits=allowance)
        name = [["s","retainedControl"]]; expr = ["sort",["zero"]]
        body_hash = C.body_id(expr,0)
        spec = dict(schema=C.SPEC_SCHEMA,foundation=B.FOUNDATION,policy=B.POLICY,
            groups=[dict(kind="ordinary",declarations=[dict(name=name,kind="definition",universes=0,
                type=["sort",["succ",["zero"]]],value_hash=body_hash,meta=dict(hint="abbrev",safety="safe"))])])
        module,opening = C.module_id(spec),C.group_opening(spec,0)
        export = adapter.encode_opening(module,name,opening)
        fingerprint = next(x for x in adapter.describe(export)["specs"] if x["tag"] == "conclusion-fingerprint")
        packet = EP.pack_terminal_i(EXPECTED(C.summarize(spec),0,B.RELATION_IMAGE),INERT_RECEIPT,
                                   aggregate_image=IMAGE,envelope=ENV(),terminal_i=True)
        s.workspace.modules.put_group(module,opening); s.workspace.packets.put(module,packet)
        body = dict(schema="DMKN_MODULE_BODY_V1",module_id=module,relative_name=name,universes=0,
                    body_hash=body_hash,expression=expr)
        s.workspace.modules.put_body(module,name,body)
        value = dict(schema=P.REQUEST_SCHEMA,generation=generation["generation"],namespace=adapter.namespace,
            wire_profile_id=s.workspace.packets.profile_id,module_id=module,relative_name=name,
            export_id=C.export_id(module,name),fingerprint=fingerprint,cell=P.cell(adapter,fingerprint)[0],
            export_object_sha256=sha(export),export_object_bytes=len(export),opening_max_bytes=4096,
            packet_sha256=sha(packet),packet_bytes=len(packet),bodies=[dict(body_hash=body_hash,max_bytes=4096)],
            retention_end_ms=now+100000)
        raw = F.compact(value); rid = P.request_id(raw,token["grant_id"],generation["generation"])
        f.update(token=token["token"],raw=raw,rid=rid,value=value)
        if commit:
            result = await s.submit(f["token"],raw,until=s.deadline)
            self.assertEqual(result["placement"]["phase"],"RECEIPT_COMMITTED")
        return f

    async def restart(self,f):
        old = f["service"]
        old.controller.seal(old.grant)
        self.assertEqual((await old.close())["status"],"CLOSED")
        s = await self.open_service(f)
        self.assertEqual(s.ledger.db.execute("SELECT state,runs FROM meta").fetchone(),("SEALED_SERVING",2))
        self.assertEqual(s.advertisement.run,2)
        self.assertNotEqual(s.grant.run_id,old.grant.run_id)
        self.assertNotEqual(s.location.state,old.location.state)
        self.assertNotEqual(s.location.evidence,old.location.evidence)
        return s

    def publish_count(self): return sum(row["command"] == "publish" for row in self.node_calls)

    def immutable_state(self,s):
        # Tiny test fixture only; product restoration must not scan the corpus.
        databases = [s.workspace.db,s.workspace.modules.db,s.workspace.packets.db,s.workspace.index.db]
        return dict(databases=[sha("\n".join(db.iterdump()).encode()) for db in databases],
            requests=list(s.ledger.db.execute("SELECT * FROM requests ORDER BY id")),
            grants=list(s.ledger.db.execute("SELECT * FROM grants ORDER BY id")),
            cells=list(s.ledger.db.execute("SELECT * FROM cells ORDER BY id")),
            meta=s.ledger.db.execute("SELECT config,state,used FROM meta").fetchone())

    def no_data_work(self,s):
        stack = ExitStack()
        for owner,names in ((s.workspace.modules,("put_group","put_body","get_body")),
                            (s.workspace.packets,("put","get","inspect")),
                            (s.workspace.index,("admit",)),
                            (s.controller,("_local_group","_local_packet","_local_body"))):
            for name in names: stack.enter_context(patch.object(owner,name,forbidden))
        return stack

    async def refused(self,s,rid):
        before = self.immutable_state(s); changes = s.advertisement.db.total_changes
        publishes,calls = self.publish_count(),s.grant.calls
        with self.no_data_work(s),self.assertRaises(ValueError):
            await s.advertise_retained(rid,until=s.deadline)
        self.assertEqual(s.grant.calls,calls+1)
        self.assertEqual(self.publish_count(),publishes)
        self.assertEqual(s.advertisement.db.total_changes,changes)
        self.assertEqual(self.immutable_state(s),before)
        self.assertFalse(s.advertisement._busy)

    async def test_sealed_restart_restores_without_rewriting_retained_data(self):
        f = await self.fixture(); first = f["service"]
        before = self.immutable_state(first)
        s = await self.restart(f)
        self.assertEqual(self.immutable_state(s),{**before,"meta":(before["meta"][0],"SEALED_SERVING",before["meta"][2])})
        stable = self.immutable_state(s)
        duplicate = await s.submit(f["token"],f["raw"],until=s.deadline)
        observed = s.status(f["token"],f["rid"],until=s.deadline)
        self.assertEqual(duplicate,observed)
        self.assertEqual(observed["route"]["run_id"],first.grant.run_id)
        self.assertEqual(self.publish_count(),1)
        changed = deepcopy(f["value"]); changed["retention_end_ms"] -= 1
        with self.assertRaises(ValueError): await s.submit(f["token"],F.compact(changed),until=s.deadline)
        changes = [db.total_changes for db in (s.workspace.db,s.workspace.modules.db,
            s.workspace.packets.db,s.workspace.index.db,s.ledger.db)]
        calls = s.grant.calls
        # Simulate elapsed original publisher and service horizons, not elapsed
        # retention. The owner guard must not reuse the original write guard.
        wall = f["value"]["retention_end_ms"]-35000
        with patch.object(J,"_now_ms",return_value=wall),patch.object(PC,"_now_ms",return_value=wall),self.no_data_work(s):
            route = await s.advertise_retained(f["rid"],until=s.deadline)
        self.assertEqual(s.grant.calls,calls+1)
        self.assertEqual(route["status"],"HINT_DISPATCHED_UNACKNOWLEDGED")
        self.assertEqual(route["run_id"],s.grant.run_id); self.assertEqual(route["request_id"],f["rid"])
        self.assertNotIn("placement",route); self.assertEqual(self.publish_count(),2)
        self.assertEqual(self.immutable_state(s),stable)
        self.assertEqual([db.total_changes for db in (s.workspace.db,s.workspace.modules.db,
            s.workspace.packets.db,s.workspace.index.db,s.ledger.db)],changes)
        route_changes = s.advertisement.db.total_changes
        with self.no_data_work(s): again = await s.advertise_retained(f["rid"],until=s.deadline)
        self.assertEqual(again,route); self.assertEqual(self.publish_count(),2)
        self.assertEqual(s.advertisement.db.total_changes,route_changes)
        OBSERVED[self._testMethodName] = dict(funded_runs=2,restoration_dispatches=1,
            unchanged_receipt_custody_index=True,old_token_new_write_refused=True,expired_original_windows=True)

    async def test_open_partial_malformed_and_unknown_representatives_refuse(self):
        f = await self.fixture(); await self.refused(f["service"],f["rid"])
        s = await self.restart(f)
        for variant in ("unknown","partial","outcome_domain","oversized_manifest"):
            with self.subTest(variant=variant):
                original = s.ledger.db.execute("SELECT manifest,phase,outcome FROM requests WHERE id=?",(f["rid"],)).fetchone()
                rid = f["rid"]
                if variant == "unknown": rid = "ed"*32
                elif variant == "partial": s.ledger.db.execute("UPDATE requests SET phase='INCOMPLETE' WHERE id=?",(rid,))
                elif variant == "outcome_domain":
                    outcome = F.strict(bytes(original[2]),P.OUTCOME_MAX); outcome["generation"] = "ed"*32
                    s.ledger.db.execute("UPDATE requests SET outcome=? WHERE id=?",(F.compact(outcome),rid))
                else: s.ledger.db.execute("UPDATE requests SET manifest=? WHERE id=?",(b"x"*(P.REQUEST_MAX+1),rid))
                try: await self.refused(s,rid)
                finally: s.ledger.db.execute("UPDATE requests SET manifest=?,phase=?,outcome=? WHERE id=?",(*original,f["rid"]))
        OBSERVED[self._testMethodName] = dict(rejected_representative_cases=5,restoration_dispatches=0)

    async def test_missing_local_index_packet_group_and_body_metadata_refuse(self):
        variants = ("posting","snapshot","name","offer","body")
        for variant in variants:
            with self.subTest(variant=variant):
                f = await self.fixture(); s = await self.restart(f)
                value = f["value"]; outcome = s.ledger.request(f["rid"])["outcome"]
                if variant == "posting":
                    s.workspace.index.db.execute("DELETE FROM postings WHERE object_id=?",(value["export_id"],))
                elif variant == "snapshot":
                    s.workspace.index.db.execute("DELETE FROM snapshots WHERE snapshot_id=?",(outcome["snapshot_id"],))
                elif variant == "name":
                    s.workspace.modules.db.execute("DELETE FROM names WHERE module=?",(value["module_id"],))
                elif variant == "offer":
                    s.workspace.packets.db.execute("DELETE FROM offers WHERE digest=?",(value["packet_sha256"],))
                else:
                    s.workspace.modules.db.execute("DELETE FROM bodies WHERE module=?",(value["module_id"],))
                await self.refused(s,f["rid"])
                self.assertEqual((await s.close())["status"],"CLOSED")
        OBSERVED[self._testMethodName] = dict(missing_metadata_cases=list(variants),automatic_refetches=0)

    async def test_original_retention_end_and_postawait_expiry_guard(self):
        f = await self.fixture(); s = await self.restart(f)
        for wall in (f["value"]["retention_end_ms"]-1,f["value"]["retention_end_ms"]):
            with patch.object(J,"_now_ms",return_value=wall): await self.refused(s,f["rid"])
        before = self.immutable_state(s); publishes = self.publish_count()
        clock = {"now":int(time.time()*1000)}; actual = s.advertisement._transaction
        def expire_after_commit(*args,**kw):
            result = actual(*args,**kw)
            clock["now"] = f["value"]["retention_end_ms"]
            return result
        with patch.object(J,"_now_ms",side_effect=lambda:clock["now"]),\
                patch.object(s.advertisement,"_transaction",expire_after_commit),\
                self.no_data_work(s),self.assertRaises(ValueError):
            await s.advertise_retained(f["rid"],until=s.deadline)
        self.assertEqual(self.publish_count(),publishes)
        self.assertEqual(s.advertisement.db.execute("SELECT phase FROM routes WHERE run=2").fetchone(),
                         ("DISPATCH_ATTEMPTED",))
        with self.no_data_work(s): route = await s.advertise_retained(f["rid"],until=s.deadline)
        self.assertEqual(route["status"],"DISPATCH_UNCERTAIN")
        self.assertEqual(self.publish_count(),publishes); self.assertEqual(self.immutable_state(s),before)
        self.assertEqual((await s.close())["status"],"CLOSED")
        f = await self.fixture(); s = await self.restart(f)
        before = self.immutable_state(s)
        clock = {"now":int(time.time()*1000)}
        self.after_dispatch = lambda:clock.update(now=f["value"]["retention_end_ms"])
        with patch.object(J,"_now_ms",side_effect=lambda:clock["now"]),self.no_data_work(s),self.assertRaises(ValueError):
            await s.advertise_retained(f["rid"],until=s.deadline)
        self.after_dispatch = None
        row = s.advertisement.db.execute("SELECT phase FROM routes WHERE run=2").fetchone()
        self.assertEqual(row,("DISPATCH_ATTEMPTED",)); self.assertEqual(self.publish_count(),publishes+2)
        self.assertEqual(self.immutable_state(s),before)
        # Restoring the fixture's clock does not create another run opportunity.
        with self.no_data_work(s): route = await s.advertise_retained(f["rid"],until=s.deadline)
        self.assertEqual(route["status"],"DISPATCH_UNCERTAIN"); self.assertEqual(self.publish_count(),publishes+2)
        OBSERVED[self._testMethodName] = dict(pre_dispatch_horizon_refusals=2,post_dispatch_expiry=True,
            after_reservation_commit_expiry=True,retained_uncertain_attempt=True,retry_dispatches=0)

    async def test_failed_and_unrecorded_restore_have_no_same_run_retry(self):
        for failure in ("dispatch","observation_commit"):
            with self.subTest(failure=failure):
                f = await self.fixture(); s = await self.restart(f)
                before = self.immutable_state(s); changes = s.advertisement.db.total_changes
                journal = s.advertisement; original = journal._transaction; count = 0
                def fail_second(*args,**kw):
                    nonlocal count
                    count += 1
                    if count == 2: raise OSError("SIMULATED_RETAINED_OBSERVATION_COMMIT_FAILURE")
                    return original(*args,**kw)
                self.mode = "fail" if failure == "dispatch" else "ok"
                with patch.object(journal,"_transaction",fail_second),self.no_data_work(s),self.assertRaises(OSError):
                    await s.advertise_retained(f["rid"],until=s.deadline)
                self.mode = "ok"; publishes = self.publish_count()
                with self.no_data_work(s): route = await s.advertise_retained(f["rid"],until=s.deadline)
                self.assertEqual(route["status"],"DISPATCH_UNCERTAIN")
                self.assertEqual(route["run_id"],s.grant.run_id)
                self.assertEqual(self.publish_count(),publishes)
                self.assertEqual(journal.db.total_changes,changes+1)
                self.assertEqual(self.immutable_state(s),before)
                self.assertEqual((await s.close())["status"],"CLOSED")
        OBSERVED[self._testMethodName] = dict(uncertainty_modes=2,unchanged_placement_charges=True,retry_dispatches=0)

    async def test_original_run_cap_and_reopen_configuration_remain_immutable(self):
        f = await self.fixture(max_runs=1); old = f["service"]
        old.controller.seal(old.grant); await old.close()
        with self.assertRaisesRegex(ValueError,"PLACEMENT_RUNTIME_CAP"): await self.open_service(f)
        changed = deepcopy(f["generation"]); changed["max_runs"] = 2
        with self.assertRaisesRegex(ValueError,"PLACEMENT_LEDGER_CONFIG"):
            await self.open_service(f,generation=changed)
        g = await self.fixture(); old = g["service"]
        old.controller.seal(old.grant); await old.close()
        with self.assertRaisesRegex(ValueError,"PLACEMENT_ROUTE_CONFIG_CHANGED"):
            await self.open_service(g,read=OTHER_READ)
        # Failed route-open consumed the original second core run; it is not
        # refunded even though no second locator was started.
        db = sqlite3.connect(g["root"]/"workspace/placement.sqlite")
        try:
            self.assertEqual(db.execute("SELECT runs FROM meta").fetchone(),(2,))
        finally: db.close()
        with self.assertRaisesRegex(ValueError,"PLACEMENT_RUNTIME_CAP"): await self.open_service(g)
        OBSERVED[self._testMethodName] = dict(reopen_refusals=4,core_run_charge_survives_route_open_failure=True)

    async def test_cancelled_owner_restore_keeps_attempt_and_releases_busy_slot(self):
        f = await self.fixture(); s = await self.restart(f); before = self.immutable_state(s)
        self.mode = "wait"; self.entered.clear()
        with self.no_data_work(s):
            task = asyncio.create_task(s.advertise_retained(f["rid"],until=s.deadline))
            await asyncio.wait_for(self.entered.wait(),2)
            self.assertIsNotNone(s._retained_task); self.assertFalse(s._retained_task.done())
            with self.assertRaises(ValueError): await s.advertise_retained(f["rid"],until=s.deadline)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError): await task
        self.assertTrue(s._retained_task is None or s._retained_task.done())
        self.assertFalse(s.advertisement._busy); self.assertFalse(s.controller._busy)
        self.mode = "ok"
        with self.no_data_work(s): route = await s.advertise_retained(f["rid"],until=s.deadline)
        self.assertEqual(route["status"],"DISPATCH_UNCERTAIN"); self.assertEqual(self.publish_count(),2)
        self.assertEqual(self.immutable_state(s),before)
        OBSERVED[self._testMethodName] = dict(owner_cancellation=True,concurrent_restore_refused=True,retry_dispatches=0)

    async def test_close_drains_tracked_owner_restore_before_closing_stores(self):
        f = await self.fixture(); s = await self.restart(f)
        self.mode = "wait"; self.entered.clear()
        with self.no_data_work(s):
            task = asyncio.create_task(s.advertise_retained(f["rid"],until=s.deadline))
            await asyncio.wait_for(self.entered.wait(),2)
            self.assertIsNotNone(s._retained_task); self.assertFalse(s._retained_task.done())
            result = await asyncio.wait_for(s.close(),3)
            with self.assertRaises(asyncio.CancelledError): await task
        self.assertEqual(result["status"],"CLOSED",result["cleanup"])
        for key in ("retained_closed","intake_closed","location_closed","read_closed",
                    "journal_closed","controller_closed","workspace_closed"):
            self.assertTrue(result["cleanup"][key],key)
        self.assertTrue(s.grant.closed); self.assertFalse(s.advertisement._busy)
        self.assertEqual(self.publish_count(),2)
        db = sqlite3.connect(f["root"]/"workspace/placement-routes.sqlite")
        try:
            self.assertEqual(db.execute("SELECT phase FROM routes WHERE run=2").fetchone(),("DISPATCH_ATTEMPTED",))
        finally: db.close()
        OBSERVED[self._testMethodName] = dict(close_cancels_owner_task=True,stores_closed_after_drain=True,
            original_outer_deadline=s.outer_deadline,uncertain_attempt_retained=True)

    async def test_close_tracks_owner_task_before_advertisement_busy_entry(self):
        f = await self.fixture(); s = await self.restart(f)
        self.entered.clear(); original_close = s.workspace.close
        async def before_busy(*unused,**ignored):
            self.entered.set()
            await self.release.wait()
            raise AssertionError("CONTROL_OWNER_TASK_MUST_HAVE_BEEN_CANCELLED")
        def checked_close():
            self.assertTrue(s._retained_task is None or s._retained_task.done())
            return original_close()
        with patch.object(s.advertisement,"advertise_retained",before_busy),\
                patch.object(s.workspace,"close",checked_close):
            task = asyncio.create_task(s.advertise_retained(f["rid"],until=s.deadline))
            await asyncio.wait_for(self.entered.wait(),2)
            self.assertFalse(s.advertisement._busy)
            self.assertIsNotNone(s._retained_task); self.assertFalse(s._retained_task.done())
            result = await asyncio.wait_for(s.close(),3)
            with self.assertRaises(asyncio.CancelledError): await task
        self.assertEqual(result["status"],"CLOSED",result["cleanup"])
        self.assertTrue(result["cleanup"]["retained_closed"])
        self.assertTrue(result["cleanup"]["workspace_closed"])
        self.assertEqual(self.publish_count(),1)
        OBSERVED[self._testMethodName] = dict(tracked_before_busy_entry=True,store_close_after_task=True,
            restoration_dispatches=0)


SELECTED = (
    "test_sealed_restart_restores_without_rewriting_retained_data",
    "test_open_partial_malformed_and_unknown_representatives_refuse",
    "test_missing_local_index_packet_group_and_body_metadata_refuse",
    "test_original_retention_end_and_postawait_expiry_guard",
    "test_failed_and_unrecorded_restore_have_no_same_run_retry",
    "test_original_run_cap_and_reopen_configuration_remain_immutable",
    "test_cancelled_owner_restore_keeps_attempt_and_releases_busy_slot",
    "test_close_drains_tracked_owner_restore_before_closing_stores",
    "test_close_tracks_owner_task_before_advertisement_busy_entry",
)


def main():
    global OUTPUT,C,B,F,WV,P,EP,EC,ENV,EXPECTED,S,J,N,L,LS,PC
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
        WV=load("client.workspace_evidence"); P=load("placement.codec"); PC=load("placement.controller")
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
    report = dict(schema="DMKN_RETAINED_ADVERTISEMENT_CONTROLS_V1",status="PASS" if passed else "FAIL",
        selected=list(SELECTED),tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
        skipped=len(result.skipped),observations=OBSERVED,sources=SOURCES,
        forbidden_calls=FORBIDDEN,loop_errors=LOOP_ERRORS,actual_network_calls=0,actual_node_children=0,
        actual_native_calls=0,actual_proof_calls=0,mathematical_acceptance=False,
        transport="SIMULATED_NODE_AND_LISTENERS_REAL_SQLITE_CONTROLLER_AND_OWNER_API",
        receipt_bytes="INERT_UNVERIFIED_FIXTURES_NEVER_ADMITTED",old_suites_imported=False,
        scope="RETAINED_ROUTE_RESTART_GUARDS_AND_LIFECYCLE_NOT_DHT_DISCOVERY_OR_PHYSICAL_QUOTA")
    write_new(OUTPUT/"retained-advertisement-controls-result.json",json.dumps(report,sort_keys=True,
        separators=(",",":"),allow_nan=False).encode()+b"\n")
    return 0 if passed else 1


if __name__ == "__main__": raise SystemExit(main())

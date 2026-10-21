"""Focused real-SQLite registry controls; no real service start or reclamation.

The root alone selects execution. Clock anchors and crash-phase injections are
explicit test inputs, not real UTC/actor-closure evidence or a physical quota.
"""
import argparse
import asyncio
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import socket
import ssl
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
INSTALLATION = PROJECT/"product-local/v5-distribution-consolidated-01/Mathematical Commons v5"
SOURCE = Path(__file__).resolve().parent
MIB = 1024**2
T = 2000000000000
EXTRA = {
    "placement.lifecycle": ("placement/lifecycle.py", 31764, "6852b5a20d4b188d328c5554f40e0bdfb2b20f84943ac689350459a5e8b2f90d"),
    "client.serve_generations": ("client/serve_generations.py", 8896, "404365849dd0e41860ba8ccda01a5b064d028241a2d8b0063d76936fcd306687"),
}
L = G = OUTPUT = None
FORBIDDEN, OBSERVED, SOURCES = [], {}, {}


def need(ok, code):
    if not ok: raise ValueError(code)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def encode(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()


def ordinary(path, directory=False):
    path = Path(path)
    need(path.is_absolute() and path.resolve() == path and all(
        not p.is_symlink() and not p.is_junction() for p in (path,*path.parents)),"CONTROL_ORDINARY_PATH")
    need(path.is_dir() if directory else path.is_file(),"CONTROL_PATH_KIND")
    return path


def pinned(path, size, digest, maximum=8*MIB):
    path = ordinary(path)
    need(0 < size <= maximum and path.stat().st_size == size,"CONTROL_PIN_SIZE")
    with path.open("rb") as stream: raw = stream.read(maximum+1)
    need(len(raw) == size and sha(raw) == digest,"CONTROL_PIN")
    return raw


def forbidden(*unused, **ignored):
    FORBIDDEN.append("PROCESS_SOCKET_OR_DELETE_FORBIDDEN")
    raise AssertionError("PROCESS_SOCKET_OR_DELETE_FORBIDDEN")


def adopt(release_sha):
    global L,G
    path = ordinary(INSTALLATION/"V5-RELEASE.json")
    raw = pinned(path,path.stat().st_size,release_sha)
    release = json.loads(raw)
    need(release["schema"] == "DMKN_V5_DIRECTORY_RELEASE_V3"
         and release["base_role"] == "mathematical-client-location-v1"
         and len(release["sdk_sources"]) == 121,"CONTROL_INSTALLED_MAP")
    need(Path(sys.executable).resolve() == INSTALLATION/"base/receiver/runtime/python/python.exe",
         "CONTROL_INSTALLED_PYTHON")
    for logical,relative in release["sdk_sources"].items():
        need(relative == "sdk/"+logical and ".." not in PurePosixPath(relative).parts
             and "\\" not in relative,"CONTROL_INSTALLED_SOURCE_PATH")
        row = release["files"][relative]; target = INSTALLATION/relative
        pinned(target,row["bytes"],row["sha256"],2*MIB)
        SOURCES[logical] = dict(path=str(target),bytes=row["bytes"],sha256=row["sha256"])
    need(not any(name in sys.modules for name in ("placement","discovery","client","location")),
         "CONTROL_EARLY_PRODUCT_IMPORT")
    sys.path[:0] = [str(INSTALLATION/"sdk/v5"),str(INSTALLATION/"sdk/portable")]
    for name,(relative,size,digest) in EXTRA.items():
        target = SOURCE/relative; pinned(target,size,digest,2*MIB)
        # Only these two fresh additions are loaded from the selected snapshot.
        # Every unchanged dependency resolves through the installed SDK above.
        __import__(name.split(".")[0])
        spec = importlib.util.spec_from_file_location(name,target)
        module = importlib.util.module_from_spec(spec); sys.modules[name] = module
        spec.loader.exec_module(module)
        SOURCES["v5/"+relative] = dict(path=str(target),bytes=size,sha256=digest)
    L,G = sys.modules["placement.lifecycle"],sys.modules["client.serve_generations"]
    return release


def verify_sources(release):
    selected = {Path(row["path"]) for row in SOURCES.values()}
    prefixes = {PurePosixPath(logical).parts[1] for logical in SOURCES}
    origins = {}
    for name,module in tuple(sys.modules.items()):
        if name.split(".")[0] not in prefixes: continue
        origin = getattr(module,"__file__",None)
        if origin is None:
            paths = getattr(module,"__path__",())
            need(paths and all(Path(p).is_relative_to(INSTALLATION/"sdk") for p in paths),"CONTROL_NAMESPACE_ORIGIN")
        else:
            path = ordinary(origin); need(path in selected,"CONTROL_PRODUCT_ORIGIN")
            origins[name] = str(path)
    for row in SOURCES.values(): pinned(row["path"],row["bytes"],row["sha256"],2*MIB)
    need(len(SOURCES) == 123,"CONTROL_EXACT_121_PLUS_TWO")
    return origins


class Controls(unittest.TestCase):
    def setUp(self):
        self.root = OUTPUT/("c%02d" % (SELECTED.index(self._testMethodName)+1)); self.root.mkdir()
        self.protected = self.root/"protected"; self.protected.mkdir()
        self.managers = []; self.synthetic = []; self.events = {}

    def tearDown(self):
        # No real actor was constructed. The composition-fault tests use
        # only explicitly registered synthetic objects with no process/socket.
        # Releasing a RESERVED/UNKNOWN session models loss of the owner;
        # it does NOT mark the run CLOSED or grant recovery authority.
        for manager in reversed(self.managers):
            for handle in manager._handles.values():
                self.assertTrue(handle.service is None or any(handle.service is item for item in self.synthetic))
                self.assertTrue(handle.location is None or any(handle.location is item for item in self.synthetic))
            if manager._closed: continue
            if manager._handles: manager._release()
            else: manager.close()
        OBSERVED[self._testMethodName] = self.events

    def config(self):
        endpoint = lambda port:dict(host="127.0.0.1",port=port,tls=False,server_name=None)
        return dict(schema=L.SCHEMA,epoch=sha(str(self.root).encode()),clock_model_id="c1"*32,
            registry_pages=64,owner_reserved_bytes=4*MIB,registry_reserved_bytes=MIB,
            cleanup_reserved_bytes=MIB,protected_roots=[str(self.protected),str(INSTALLATION),str(SOURCE)],
            slots=[dict(reserved_bytes=MIB,max_cells=1,max_runs=2,
                        read_endpoint=endpoint(44201+3*i),intake_endpoint=endpoint(44202+3*i),
                        listen=["/ip4/127.0.0.1/tcp/"+str(44203+3*i)]) for i in range(2)])

    def manager(self, name="managed", *, create=True, config=None, calls=256):
        manager = L.ManagedGenerations.open(self.root/name,self.config() if config is None else config,
            create=create,deadline=time.monotonic()+60,calls=calls,cpu_seconds=30)
        self.managers.append(manager); return manager

    def generation(self, manager, slot, *, horizon=T, max_runs=2):
        spec = manager.config["slots"][slot]
        egress = dict(schema="DMKN_V5_OWNER_EGRESS_V1",mode="loopback-test",public_ports=[],
            test_endpoints=[dict(host="127.0.0.1",port=p) for p in range(44201,44207)])
        placement = dict(schema=L.P.CONFIG_SCHEMA,service_epoch=manager.config["epoch"],
            namespace="a1"*32,wire_profile_id="b1"*32,admission_close_ms=horizon-1000,
            retention_not_after_ms=horizon,max_grants=1,max_requests=1,max_cells=1,
            max_runs=max_runs,ledger_pages=256,limits={key:1 for key in L.P.RESOURCES})
        # These payloads are registry metadata only; no Workspace/service is
        # opened and no mathematical fixture or valid-custody claim is implied.
        return dict(workspace={"control":"UNOPENED_OPAQUE_WORKSPACE_CONFIGURATION"},placement=placement,
            service_limits={"control":"UNOPENED_SERVICE_LIMITS"},egress=egress,
            location=dict(schema="DMKN_V5_MAINTAINED_LOCATION_ROLES_V1",role="index-provider",
                namespace=placement["namespace"],egress=egress,listen=deepcopy(spec["listen"]),
                announce=[],bootstrap=[],endpoints=[deepcopy(spec["read_endpoint"])],limits={}))

    def snapshot(self, manager):
        def tag(value): return {"blob":value.hex()} if isinstance(value,bytes) else value
        rows = {"meta":[[tag(v) for v in row] for row in manager.db.execute("SELECT * FROM meta ORDER BY id")],
                "slots":[[tag(v) for v in row] for row in manager.db.execute("SELECT * FROM slots ORDER BY id")]}
        return sha(encode(rows))

    def paths(self, root):
        rows = sorted(p.relative_to(root).as_posix() for p in root.rglob("*"))
        self.assertLessEqual(len(rows),64); return rows

    def refused(self, manager, operation, code):
        before,paths = self.snapshot(manager),self.paths(manager.root)
        with self.assertRaises(ValueError) as error: operation()
        self.assertEqual(str(error.exception),code)
        self.assertEqual(self.snapshot(manager),before); self.assertEqual(self.paths(manager.root),paths)
        self.events.setdefault("refusals",[]).append(code)

    def clock(self, manager, lower=T):
        return manager.adopt_clock(lower_utc_ms=lower,valid_for_ms=60000,rate_error_ppm=0,
                                   model_id=manager.config["clock_model_id"])

    def interrupt_session(self, manager):
        for handle in manager._handles.values():
            self.assertIsNone(handle.service); self.assertIsNone(handle.location)
        manager._release()
        self.events["simulated_owner_loss_without_constructed_actor"] = True

    def test_configuration_requires_two_disjoint_funded_slots(self):
        for label,change,code in (
            ("three",lambda c:c["slots"].append(deepcopy(c["slots"][0])),"GENERATIONS_EXACTLY_TWO_SLOTS"),
            ("ports",lambda c:c["slots"][1].update(read_endpoint=c["slots"][0]["read_endpoint"]),"GENERATIONS_DISTINCT_ROLE_PORTS"),
            ("budget",lambda c:c.update(owner_reserved_bytes=1),"GENERATIONS_OWNER_ALLOCATION")):
            cfg=self.config(); change(cfg)
            with self.assertRaises(ValueError) as error: self.manager(label,config=cfg)
            self.assertEqual(str(error.exception),code); self.assertFalse((self.root/label).exists())
        with self.assertRaisesRegex(ValueError,"^GENERATIONS_PROTECTED_PATH_OVERLAP$"):
            L.ManagedGenerations.open(self.protected/"blocked",self.config(),create=True,deadline=time.monotonic()+60)
        self.assertFalse((self.protected/"blocked").exists())
        manager=self.manager(); state=manager.status()
        self.assertEqual(state["slots"],[None,None]); self.assertEqual(state["reserved_bytes"],2*MIB)
        self.assertFalse(state["physical_envelope_adopted"])
        self.events.update(config_refusals=4,logical_reservation_only=True)

    def test_two_slots_and_monotone_horizons_refuse_extra_allocation(self):
        manager=self.manager(); a=manager.allocate(0,self.generation(manager,0))
        self.refused(manager,lambda:manager.allocate(1,self.generation(manager,1,horizon=T-1)),"GENERATIONS_HORIZON_REGRESSION")
        b=manager.allocate(1,self.generation(manager,1,horizon=T+1))
        self.refused(manager,lambda:manager.allocate(0,self.generation(manager,0)),"GENERATIONS_SLOT_OCCUPIED")
        state=manager.status()
        self.assertEqual(state["allocated_sequence"],2); self.assertEqual(state["retired_floor"],0)
        self.assertEqual([x["sequence"] for x in state["slots"]],[1,2])
        self.assertNotEqual(a["generation"],b["generation"])
        self.events.update(sequence=2,occupied_slots=2,third_generation_created=False)

    def test_failed_marker_creation_keeps_provisioning_charge(self):
        manager=self.manager(); original=L._write_new
        def fail_marker(path,raw):
            if Path(path).name == "generation.json": raise OSError("CONTROL_MARKER_WRITE_FAILURE")
            return original(path,raw)
        with patch.object(L,"_write_new",fail_marker),self.assertRaisesRegex(OSError,"CONTROL_MARKER_WRITE_FAILURE"):
            manager.allocate(0,self.generation(manager,0))
        state=manager.status(); record=state["slots"][0]
        self.assertEqual((state["allocated_sequence"],record["phase"],record["runs"]),(1,"PROVISIONING",0))
        path=manager.generation_path(record)
        self.assertTrue(path.is_dir()); self.assertFalse((path/"generation.json").exists())
        self.refused(manager,lambda:manager.allocate(0,self.generation(manager,0)),"GENERATIONS_SLOT_OCCUPIED")
        before=self.snapshot(manager)
        with self.assertRaises(FileNotFoundError): manager.reserve_run(record["generation"],outer_deadline=time.monotonic()+30)
        self.assertEqual(self.snapshot(manager),before); self.assertFalse((path/"generation.json").exists())
        manager.close(); reopened=self.manager(create=False)
        self.assertEqual(self.snapshot(reopened),before)
        self.events.update(durable_provisioning=True,missing_marker_not_recreated=True,sequence_consumed=1)

    def test_run_reservation_precedes_path_and_unknown_restart_never_refunds(self):
        manager=self.manager(); record=manager.allocate(0,self.generation(manager,0,max_runs=1))
        handle=manager.reserve_run(record["generation"],outer_deadline=time.monotonic()+30)
        self.assertFalse(handle.path.exists())
        held=manager.status()["slots"][0]
        self.assertEqual((held["runs"],held["run_state"]),(1,"RESERVED"))
        self.refused(manager,lambda:manager.reserve_run(record["generation"],outer_deadline=time.monotonic()+30),
                     "GENERATIONS_RUN_PHASE_OR_UNKNOWN")
        with self.assertRaisesRegex(ValueError,"^GENERATIONS_ACTORS_REQUIRE_CLOSE_OR_OUTER_RECOVERY$"): manager.close()
        self.interrupt_session(manager); reopened=self.manager(create=False)
        held=reopened.status()["slots"][0]
        self.assertEqual((held["runs"],held["run_state"]),(1,"UNKNOWN"))
        self.assertEqual(held["config"],record["config"])
        self.refused(reopened,lambda:reopened.reserve_run(record["generation"],outer_deadline=time.monotonic()+30),
                     "GENERATIONS_RUN_PHASE_OR_UNKNOWN")
        clock=self.clock(reopened); reopened.begin_retire(record["generation"],clock)
        self.refused(reopened,lambda:reopened.commit_retired(record["generation"],clock),"GENERATIONS_RETIRE_CLOSURE_UNKNOWN")
        self.assertFalse(handle.path.exists())
        self.events.update(run_charge=1,configured_cap=1,no_constructed_actor=True,unknown_closure_still_held=True)

    def test_current_identity_marker_and_no_service_seal_refuse(self):
        manager=self.manager(); record=manager.allocate(0,self.generation(manager,0))
        self.refused(manager,lambda:manager.reserve_run("ef"*32,outer_deadline=time.monotonic()+30),
                     "GENERATIONS_NOT_CURRENTLY_REGISTERED")
        self.refused(manager,lambda:manager.seal(record["generation"]),"GENERATIONS_NO_CURRENT_SERVICE")
        marker=manager.generation_path(record)/"generation.json"
        self.assertTrue(marker.is_relative_to(self.root))
        # Corrupt only this newly created fixture marker, retain it as evidence.
        with marker.open("wb") as stream: stream.write(b"CONTROL_WRONG_GENERATION_MARKER")
        self.refused(manager,lambda:manager.reserve_run(record["generation"],outer_deadline=time.monotonic()+30),
                     "GENERATIONS_GENERATION_MARKER")
        self.assertEqual(manager.status()["slots"][0]["runs"],0)
        self.events["existing_workspace_or_service_created"] = False

    def test_conservative_clock_early_expired_backwards_model_and_session(self):
        manager=self.manager(); record=manager.allocate(0,self.generation(manager,0)); anchor=1000000000
        with patch.object(L.time,"monotonic_ns",return_value=anchor):
            early=manager.adopt_clock(lower_utc_ms=T-1,valid_for_ms=10,rate_error_ppm=0,model_id=manager.config["clock_model_id"])
            with patch.object(L.time,"time",return_value=10**15):
                self.refused(manager,lambda:manager.begin_retire(record["generation"],early),"GENERATIONS_RETENTION_STILL_PROMISED")
            with self.assertRaisesRegex(ValueError,"^GENERATIONS_CLOCK_MODEL$"):
                manager.adopt_clock(lower_utc_ms=T,valid_for_ms=10,rate_error_ppm=0,model_id="c2"*32)
        for ns in (anchor-1,anchor+10000001):
            with patch.object(L.time,"monotonic_ns",return_value=ns):
                self.refused(manager,lambda:manager.begin_retire(record["generation"],early),"GENERATIONS_CLOCK_EXPIRED_OR_BACKWARDS")
        with patch.object(L.time,"monotonic_ns",return_value=anchor):
            drift=manager.adopt_clock(lower_utc_ms=T-10,valid_for_ms=100,rate_error_ppm=500000,model_id=manager.config["clock_model_id"])
        with patch.object(L.time,"monotonic_ns",return_value=anchor+20000000):
            self.assertEqual(drift.lower_bound_ms(),T)
        foreign=self.manager("foreign"); clock=self.clock(foreign)
        self.refused(manager,lambda:manager.begin_retire(record["generation"],clock),"GENERATIONS_CURRENT_CLOCK")
        self.events.update(system_wall_jump_used_as_authority=False,deterministic_clock_input=True,drift_floor_exact=True)

    def test_retirement_floor_plan_and_both_retired_slots_stay_occupied(self):
        manager=self.manager(); a=manager.allocate(0,self.generation(manager,0)); b=manager.allocate(1,self.generation(manager,1))
        clock=self.clock(manager)
        manager.begin_retire(b["generation"],clock); manager.commit_retired(b["generation"],clock)
        self.assertEqual(manager.status()["retired_floor"],0)
        manager.begin_retire(a["generation"],clock); manager.commit_retired(a["generation"],clock)
        self.assertEqual(manager.status()["retired_floor"],2)
        # Unknown inventory is not certified by this boundary-only planner.
        extra=manager.generation_path(a)/"unclassified-control-file"
        with extra.open("xb") as stream: stream.write(b"PRESERVE_NO_RECLAIMER_SELECTED")
        before,paths=self.snapshot(manager),self.paths(manager.root)
        plan=manager.plan_reclamation(a["generation"])
        self.assertFalse(plan["deletion_authorized"]); self.assertTrue(plan["slot_remains_occupied"])
        self.assertIn("NOT_IMPLEMENTED",plan["required_boundary"])
        self.assertEqual(self.snapshot(manager),before); self.assertEqual(self.paths(manager.root),paths)
        self.refused(manager,lambda:manager.reserve_run(a["generation"],outer_deadline=time.monotonic()+30),"GENERATIONS_RETIRED_IDENTITY")
        self.refused(manager,lambda:manager.allocate(0,self.generation(manager,0)),"GENERATIONS_SLOT_OCCUPIED")
        self.assertEqual([r["phase"] for r in manager.status()["slots"]],["RETIRED","RETIRED"])
        self.events.update(retired_floor=2,never_started_generations=True,closure_evidence_fabricated=False,
                           unknown_file_preserved=True,reclaimed=False,free_transition=False)

    def test_crash_intents_preserve_unknown_seal_and_retirement(self):
        manager=self.manager(); a=manager.allocate(0,self.generation(manager,0))
        handle=manager.reserve_run(a["generation"],outer_deadline=time.monotonic()+30); manager._closing(handle)
        # Explicit crash-state fixture injection, not a service or closure receipt.
        record=manager._find(a["generation"]); record["phase"]="SEALING"
        manager.db.execute("UPDATE slots SET record=? WHERE id=0",(L.F.compact(record),))
        self.interrupt_session(manager); reopened=self.manager(create=False)
        state=reopened.status()["slots"][0]
        self.assertEqual((state["phase"],state["run_state"],state["runs"]),("SEALING","UNKNOWN",1))
        self.refused(reopened,lambda:reopened.reserve_run(a["generation"],outer_deadline=time.monotonic()+30),"GENERATIONS_RUN_PHASE_OR_UNKNOWN")
        b=reopened.allocate(1,self.generation(reopened,1)); old_clock=self.clock(reopened)
        reopened.begin_retire(b["generation"],old_clock); reopened.close()
        again=self.manager(create=False)
        self.assertEqual(again.status()["slots"][1]["phase"],"RETIRING")
        self.refused(again,lambda:again.commit_retired(b["generation"],old_clock),"GENERATIONS_CURRENT_CLOCK")
        again.commit_retired(b["generation"],self.clock(again))
        self.assertEqual(again.status()["retired_floor"],0)
        self.events.update(synthetic_sealing_intent=True,unknown_prefix_blocks_floor=True,
                           retirement_requires_fresh_session_clock=True)

    def test_owner_call_and_sequence_exhaustion_preserve_state(self):
        manager=self.manager(calls=2); manager.status(); manager.status()
        self.refused(manager,manager.status,"GENERATIONS_OWNER_CALL_CAP")
        exhausted=self.manager("sequence")
        exhausted.db.execute("UPDATE meta SET sequence=? WHERE id=1",(L.MAX_SEQUENCE,))
        self.refused(exhausted,lambda:exhausted.allocate(0,self.generation(exhausted,0)),"GENERATIONS_SEQUENCE_EXHAUSTED")
        self.events.update(call_cap=2,sequence_saturation="EXPLICIT_SQL_FIXTURE_NOT_ITERATED",no_counter_wrap=True)

    def test_release_attempts_database_and_lock_after_first_failure(self):
        called=[]; failure=OSError("CONTROL_DB_CLOSE_FAILURE")
        def db_close(): called.append("db"); raise failure
        def lock_close(): called.append("lock")
        manager=L.ManagedGenerations.__new__(L.ManagedGenerations)
        manager.db=SimpleNamespace(close=db_close); manager._lock=SimpleNamespace(close=lock_close)
        manager._closed=manager._poisoned=False
        with self.assertRaises(OSError) as error: manager._release()
        self.assertIs(error.exception,failure); self.assertEqual(called,["db","lock"])
        self.assertIsNone(manager._lock); self.assertTrue(manager._closed); self.assertTrue(manager._poisoned)
        self.events.update(resource_faults="SIMULATED_CLOSE_METHODS_ONLY",both_attempted=True,
                           original_failure_preserved=True,managed_actors_marked_closed=False)

    def test_unattached_synthetic_service_failure_attempts_both_closes_and_holds(self):
        manager=self.manager(); record=manager.allocate(0,self.generation(manager,0))
        handle=manager.reserve_run(record["generation"],outer_deadline=time.monotonic()+30)
        self.assertFalse(handle.path.exists())
        called=[]; primary=[]; close_failure=OSError("CONTROL_SYNTHETIC_SERVICE_CLOSE_FAILURE")
        async def service_close(): called.append("service"); raise close_failure
        async def location_close(): called.append("location")
        service=SimpleNamespace(close=service_close); location=SimpleNamespace(close=location_close)
        self.synthetic.append(location)
        # Constructor/open stand-ins are not real services or closure evidence.
        # The actual manager._attach must reject their non-exact service type.
        original_attach=manager._attach
        def attach(h,s):
            try: return original_attach(h,s)
            except BaseException as error: primary.append(error); raise
        composer=G.GenerationServices.__new__(G.GenerationServices)
        composer.manager=manager
        composer.runtime=dict(source_root=str(SOURCE),source_pins={},
                              installation_root=str(INSTALLATION),role_pins={})
        with patch.object(G,"AdoptedLocationRuntime",return_value=object()), \
             patch.object(G,"ServiceLocationProcess",return_value=location), \
             patch.object(G.PlacementService,"open",return_value=service), \
             patch.object(manager,"_attach",side_effect=attach):
            coroutine=composer._start(handle,time.monotonic()+20,None,None)
            try:
                # This selected failure branch has only non-suspending mock
                # closes. Drive it once: no event loop, listener or task exists.
                with self.assertRaisesRegex(ValueError,"^GENERATIONS_EXACT_SERVICE_ATTACHMENT$") as error:
                    coroutine.send(None)
            finally: coroutine.close()
        self.assertEqual(len(primary),1); self.assertIs(error.exception,primary[0])
        self.assertEqual(called,["service","location"])
        self.assertEqual(error.exception.__notes__,["GENERATIONS_UNATTACHED_SERVICE_CLOSE_UNCERTAIN"])
        self.assertIsNone(handle.service); self.assertIs(handle.location,location)
        self.assertFalse(handle.closed); self.assertIsNone(handle._roles)
        held=manager.status()["slots"][0]
        self.assertEqual((held["phase"],held["run_state"],held["runs"]),("INCOMPLETE","UNKNOWN",1))
        self.assertNotIn("closure_sha256",held); self.assertTrue(handle.path.is_dir())
        self.refused(manager,lambda:manager.reserve_run(record["generation"],outer_deadline=time.monotonic()+30),
                     "GENERATIONS_RUN_PHASE_OR_UNKNOWN")
        # Resource-only release, not actor closure; these are known synthetic
        # objects. The durable UNKNOWN charge must survive another owner session.
        manager._release(); reopened=self.manager(create=False)
        self.assertEqual(reopened.status()["slots"][0],held)
        self.events.update(synthetic_constructors_and_closes=True,actual_attachment_type_refusal=True,
                           composition_failure_branch_executed=True,event_loop_created=False,
                           original_error_preserved=True,both_close_attempts=True,
                           positive_actor_closure=False,durable_unknown_run_charge=1)

    def test_retirement_wake_preserves_exact_monitor_close_scheduling(self):
        manager=self.manager(); record=manager.allocate(0,self.generation(manager,0))
        handle=manager.reserve_run(record["generation"],outer_deadline=time.monotonic()+30)
        # Exact class shell, not open()/attachment or a genuine service. This
        # isolates the retire-wake/monitor branch and grants no close authority.
        service=G.PlacementService.__new__(G.PlacementService)
        service.grant=SimpleNamespace(closed=False); service._wake=asyncio.Event()
        service._closing=False; service._close_task=None
        service.limits={"health_interval_ms":1}
        self.synthetic.append(service); handle.service=service
        clock=self.clock(manager); manager.begin_retire(record["generation"],clock)
        self.assertTrue(service.grant.closed); self.assertTrue(service._wake.is_set())
        self.assertFalse(service._closing)
        scheduled=[]; fake_task=object()
        async def unused_close(): raise AssertionError("CONTROL_REAL_CLOSE_NOT_SELECTED")
        def capture_task(coroutine):
            scheduled.append(coroutine); coroutine.close(); return fake_task
        with patch.object(service,"_close",unused_close),patch.object(asyncio,"create_task",capture_task):
            monitor=service._monitor()
            try:
                with self.assertRaises(StopIteration): monitor.send(None)
            finally: monitor.close()
        self.assertEqual(len(scheduled),1); self.assertIs(service._close_task,fake_task)
        self.assertFalse(service._closing); self.assertFalse(handle.closed)
        held=manager.status()["slots"][0]
        self.assertEqual((held["phase"],held["run_state"],held["runs"]),("RETIRING","RESERVED",1))
        self.assertNotIn("closure_sha256",held)
        # A late service-start continuation cannot overwrite durable RETIRING.
        # The actual phase guard must refuse before consulting shell internals.
        self.refused(manager,lambda:manager._started(handle),"GENERATIONS_START_PHASE")
        self.refused(manager,lambda:manager.commit_retired(record["generation"],clock),"GENERATIONS_RETIRE_CLOSURE_UNKNOWN")
        self.events.update(exact_monitor_coroutine_branch=True,unopened_exact_class_shell=True,
                           task_scheduler_mocked=True,real_close_executed=False,positive_actor_closure=False,
                           grant_revoked=True,wake_set=True,monitor_close_scheduled=True,
                           late_start_preserves_retirement=True,run_charge=1)


SELECTED = (
    "test_configuration_requires_two_disjoint_funded_slots",
    "test_two_slots_and_monotone_horizons_refuse_extra_allocation",
    "test_failed_marker_creation_keeps_provisioning_charge",
    "test_run_reservation_precedes_path_and_unknown_restart_never_refunds",
    "test_current_identity_marker_and_no_service_seal_refuse",
    "test_conservative_clock_early_expired_backwards_model_and_session",
    "test_retirement_floor_plan_and_both_retired_slots_stay_occupied",
    "test_crash_intents_preserve_unknown_seal_and_retirement",
    "test_owner_call_and_sequence_exhaustion_preserve_state",
    "test_release_attempts_database_and_lock_after_first_failure",
    "test_unattached_synthetic_service_failure_attempts_both_closes_and_holds",
    "test_retirement_wake_preserves_exact_monitor_close_scheduling",
)


def main():
    global OUTPUT
    parser=argparse.ArgumentParser(); parser.add_argument("--output",required=True)
    parser.add_argument("--release-sha",required=True); args=parser.parse_args()
    need(os.name == "nt" and Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize,"CONTROL_ISOLATED_CANONICAL_OWNER")
    OUTPUT=ordinary(args.output,directory=True)
    need(OUTPUT.is_relative_to(PROJECT/"experiments") and not OUTPUT.is_relative_to(INSTALLATION),"CONTROL_FRESH_OUTPUT_SCOPE")
    # asyncio/ssl are preloaded above so ssl does not try to subclass the
    # forbidden socket-constructor function during a later product import.
    with ExitStack() as guards:
        for owner,name in ((subprocess,"Popen"),(os,"system"),(os,"unlink"),(os,"remove"),(os,"rmdir"),
                           (shutil,"rmtree"),(socket,"socket")):
            guards.enter_context(patch.object(owner,name,forbidden))
        release=adopt(args.release_sha)
        result=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
        origins=verify_sources(release)
    passed=result.wasSuccessful() and result.testsRun == len(SELECTED) and not result.skipped and not FORBIDDEN
    report=dict(schema="DMKN_BOUNDED_GENERATIONS_REGISTRY_CONTROLS_V1",status="PASS" if passed else "FAIL",
        selected=list(SELECTED),tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
        skipped=len(result.skipped),observations=OBSERVED,forbidden_calls=FORBIDDEN,sources=SOURCES,origins=origins,
        release_sha256=args.release_sha,actual_network_calls=0,actual_node_children=0,actual_native_calls=0,
        actual_proof_calls=0,actual_verifier_calls=0,explicit_reclamation_deletions=0,mathematical_acceptance=False,
        sqlite_native_journal_lifecycle="NORMAL_SQLITE_INTERNAL_OPERATIONS_NOT_RECLAMATION_OR_COUNTED_UNLINKS",
        scope="REAL_SQLITE_REGISTRY_WITH_EXPLICIT_CLOCK_CRASH_AND_SYNTHETIC_COMPOSITION_FAULTS_NO_REAL_SERVICE_START",
        real_service_composition_executed=False,synthetic_composition_fault_cases_selected=2,
        positive_actor_closure_tested=False,reclamation_executed=False,
        physical_envelope_adopted=False,old_suites_imported=False)
    raw=encode(report)+b"\n"; need(len(raw)<=MIB,"CONTROL_REPORT_BOUND")
    with (OUTPUT/"bounded-generations-controls-result.json").open("xb") as stream:
        need(stream.write(raw)==len(raw),"CONTROL_SHORT_WRITE")
    return 0 if passed else 1


if __name__ == "__main__": raise SystemExit(main())

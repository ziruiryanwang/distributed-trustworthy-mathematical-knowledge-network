"""Five refusal-only controls; root separately selects any execution.

Synthetic sessions/rows are negative inputs, never current launch or closure
authority. No process, service, deletion or positive Job observation is run.
"""
import argparse
from contextlib import ExitStack, closing
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import socket
import sqlite3
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

PROJECT=Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
INSTALLATION=PROJECT/"product-local/v5-distribution-consolidated-01/Mathematical Commons v5"
SOURCE=Path(__file__).resolve().parent
SNAPSHOT=SOURCE.parents[2]
MIB=1024**2
T=2000000000000
PROFILE="91"*32
EXTRA={
    "placement.reclaim":("software/v5/bounded_reclamation/placement/reclaim.py",12387,
        "19713fc4baec821a5c77a0071182c63401b292cbe79a7ed7c04b7deba50e1894"),
    "placement.sessions":("software/v5/supervised_generations/placement/sessions.py",20233,
        "b4cfab61c990464756e87a7344e2a029a5374602283a4255d4d5aa854090b7f7"),
    "placement.lifecycle":("software/v5/supervised_generations/placement/lifecycle.py",38399,
        "bec62143313e1abd400550bae45a6334be2ddffb94d77a14ba9b5853b565042f"),
}
L=S=OUTPUT=None
SOURCES={}; OBSERVED={}; FORBIDDEN=[]


def need(ok,code):
    if not ok: raise ValueError(code)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def encode(value): return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()


def ordinary(path,directory=False):
    path=Path(path)
    need(path.is_absolute() and path.resolve()==path and all(
        not p.is_symlink() and not p.is_junction() for p in (path,*path.parents)),"CONTROL_ORDINARY")
    need(path.is_dir() if directory else path.is_file(),"CONTROL_PATH_KIND")
    return path


def pin(path,size,digest):
    path=ordinary(path); need(0<size<=8*MIB and path.stat().st_size==size,"CONTROL_PIN_SIZE")
    with path.open("rb") as stream: raw=stream.read(8*MIB+1)
    need(len(raw)==size and sha(raw)==digest,"CONTROL_PIN")
    return raw


def forbidden(*unused,**ignored):
    FORBIDDEN.append("FORBIDDEN_PROCESS_SOCKET_DELETE_OR_POSITIVE_QUIESCENCE")
    raise AssertionError(FORBIDDEN[-1])


def adopt(release_sha):
    global L,S
    path=ordinary(INSTALLATION/"V5-RELEASE.json")
    release=json.loads(pin(path,path.stat().st_size,release_sha))
    need(release["schema"]=="DMKN_V5_DIRECTORY_RELEASE_V3" and len(release["sdk_sources"])==121,
         "CONTROL_EXACT_INSTALLED_RELEASE")
    need(Path(sys.executable).resolve()==INSTALLATION/"base/receiver/runtime/python/python.exe",
         "CONTROL_INSTALLED_PYTHON")
    for logical,relative in release["sdk_sources"].items():
        parts=PurePosixPath(logical).parts
        need(len(parts)>=2 and parts[0] in ("v5","portable") and relative=="sdk/"+logical
             and ".." not in parts and "\\" not in logical,"CONTROL_SOURCE_PATH")
        row=release["files"][relative]; target=INSTALLATION/relative
        pin(target,row["bytes"],row["sha256"])
        SOURCES[logical]=dict(path=str(target),bytes=row["bytes"],sha256=row["sha256"])
    prefixes={PurePosixPath(name).parts[1] for name in SOURCES}
    need(not any(name.split(".")[0] in prefixes for name in sys.modules),"CONTROL_EARLY_PRODUCT_IMPORT")
    sys.path[:0]=[str(INSTALLATION/"sdk/v5"),str(INSTALLATION/"sdk/portable")]
    for name,(relative,size,digest) in EXTRA.items():
        target=SNAPSHOT/relative; pin(target,size,digest)
        parent=__import__(name.split(".")[0])
        spec=importlib.util.spec_from_file_location(name,target)
        module=importlib.util.module_from_spec(spec); sys.modules[name]=module
        spec.loader.exec_module(module); setattr(parent,name.split(".")[1],module)
        SOURCES["v5/"+name.replace(".","/")+".py"]=dict(path=str(target),bytes=size,sha256=digest)
    L,S=sys.modules["placement.lifecycle"],sys.modules["placement.sessions"]


def rebind(release_sha):
    path=INSTALLATION/"V5-RELEASE.json"; pin(path,path.stat().st_size,release_sha)
    selected={Path(row["path"]) for row in SOURCES.values()}
    prefixes={PurePosixPath(name).parts[1] for name in SOURCES}; origins={}
    for name,module in tuple(sys.modules.items()):
        if name.split(".")[0] not in prefixes: continue
        origin=getattr(module,"__file__",None)
        if origin is None:
            paths=getattr(module,"__path__",())
            need(paths and all(Path(p).is_relative_to(INSTALLATION/"sdk") for p in paths),"CONTROL_NAMESPACE")
        else:
            path=ordinary(origin); need(path in selected,"CONTROL_PRODUCT_ORIGIN"); origins[name]=str(path)
    for row in SOURCES.values(): pin(row["path"],row["bytes"],row["sha256"])
    need(len(SOURCES)==124,"CONTROL_121_PLUS_THREE")
    return origins


def rows(db):
    def tag(value): return {"blob":value.hex()} if isinstance(value,bytes) else value
    return {table:[[tag(value) for value in row]
                   for row in db.execute("SELECT * FROM "+table+" ORDER BY id")]
            for table in ("meta","slots")}


def saved_rows(root):
    with closing(sqlite3.connect((root/"generations.sqlite").as_uri()+"?mode=ro",uri=True)) as db:
        return rows(db)


class BindFault:
    """Real SQLite; one explicit failed COMMIT or lost successful COMMIT ack."""
    def __init__(self,db,mode): self.db=db; self.mode=mode; self.armed=False; self.fired=False
    def __getattr__(self,name): return getattr(self.db,name)
    def execute(self,sql,parameters=()):
        if sql=="UPDATE meta SET session_sequence=?,session=? WHERE id=1":
            self.armed=json.loads(parameters[1])["state"]=="BOUND"
        if sql=="COMMIT" and self.armed and not self.fired:
            self.fired=True
            if self.mode=="after-commit": self.db.execute(sql,parameters)
            raise OSError("CONTROL_BIND_"+self.mode)
        return self.db.execute(sql,parameters)


class Controls(unittest.TestCase):
    def setUp(self):
        self.root=OUTPUT/("c%02d"%(SELECTED.index(self._testMethodName)+1)); self.root.mkdir()
        self.managers=[]; self.events={}

    def tearDown(self):
        for manager in reversed(self.managers):
            self.assertFalse(manager._handles)
            if not manager._closed: manager._release()
        OBSERVED[self._testMethodName]=self.events

    def config(self):
        endpoint=lambda port:dict(host="127.0.0.1",port=port,tls=False,server_name=None)
        return dict(schema=L.SCHEMA,epoch=sha(str(self.root).encode()),clock_model_id="c1"*32,
            registry_pages=64,owner_reserved_bytes=4*MIB,registry_reserved_bytes=MIB,
            cleanup_reserved_bytes=MIB,protected_roots=[str(SOURCE),str(INSTALLATION)],max_sessions=2,
            slots=[dict(reserved_bytes=MIB,max_cells=1,max_runs=2,read_endpoint=endpoint(44401+3*i),
                intake_endpoint=endpoint(44402+3*i),listen=["/ip4/127.0.0.1/tcp/"+str(44403+3*i)]) for i in range(2)])

    def manager(self,name="managed"):
        manager=L.ManagedGenerations.open(self.root/name,self.config(),create=True,
            deadline=time.monotonic()+120,calls=128,cpu_seconds=30)
        self.managers.append(manager); return manager

    def foreign_worker(self):
        # Actual read-only kernel identity is deliberately made unequal; it is
        # never used to forge a successful current-process join.
        actual=S._process_identity()
        return dict(pid=actual["pid"],created=actual["created"]+1)

    def session(self,manager,state="BOUND",number=1):
        started=time.monotonic_ns()
        return dict(schema=S.SCHEMA,number=number,nonce="21"*32,binding=S._binding(manager),
            profile_sha256=PROFILE,command_sha256="31"*32,
            limits=dict(cpu_seconds=1,memory_mib=32,active_processes=1,wall_seconds=60,
                        stdout_bytes=1024,stderr_bytes=1024),
            run_deadline_ns=started+60*10**9,recovery_deadline_ns=started+85*10**9,
            cleanup_seconds=25,bind_calls=2,recovery_calls=2,owner_cpu_seconds=5,
            state=state,worker=None if state=="RESERVED" else self.foreign_worker())

    def store_session(self,manager,session):
        # Directly injected negative fixture, not a real supervisor reservation.
        manager._transaction(lambda:S._save_session(manager,session))

    def launch(self,manager,session):
        # Deliberately fabricated *negative input*. Never issued with _KEY,
        # never supplied a successful observation, never used to run a process.
        launch=object.__new__(S._Launch)
        launch.root=manager.root; launch.config=deepcopy(manager.config)
        launch.session=deepcopy(session); launch.job_created=False; launch.bound=False
        launch.outcome=dict(status="UNKNOWN",reason="SYNTHETIC_REFUSAL_INPUT_ONLY")
        return launch

    def record(self,manager,session,slot=0,state="LIVE"):
        spec=manager.config["slots"][slot]
        placement=dict(schema=L.P.CONFIG_SCHEMA,service_epoch=manager.config["epoch"],namespace="a1"*32,
            wire_profile_id="b1"*32,admission_close_ms=T-1000,retention_not_after_ms=T,max_grants=1,
            max_requests=1,max_cells=1,max_runs=2,ledger_pages=256,limits={key:1 for key in L.P.RESOURCES})
        cfg=dict(workspace={"synthetic":"UNOPENED"},service_limits={"synthetic":"UNOPENED"},
                 placement=placement,egress={},location={"listen":deepcopy(spec["listen"])})
        sequence=slot+1
        generation=L.F.digest("DMKN-V5-TWO-SLOT-GENERATION-V1",dict(
            manager=L.P.digest(manager._marker),sequence=sequence,slot=slot,config=cfg))
        cfg["placement"]["generation"]=generation
        record=dict(slot=slot,sequence=sequence,generation=generation,phase="OPEN",runs=1,
                    run_state=state,failure="SYNTHETIC_UNCLOSED_NEGATIVE",retirement_lower_ms=None,config=cfg)
        record["session"]=S.run_binding(session,record)
        return record

    def store_records(self,manager,records):
        def store():
            manager.db.execute("UPDATE meta SET sequence=?,last_horizon=? WHERE id=1",(len(records),T))
            for record in records: manager._save(record)
        manager._transaction(store)

    def refusal(self,code,call):
        with self.assertRaisesRegex(ValueError,"^"+code+"$"): call()

    def test_schema_and_missing_worker_join_refuse_before_effects(self):
        manager=self.manager(); before=rows(manager.db)
        old=self.config(); old["schema"]="DMKN_V5_TWO_GENERATION_MANAGER_RECLAIM_V1"
        old_root=self.root/"old-schema"
        self.refusal("GENERATIONS_SCHEMA",lambda:L.ManagedGenerations.open(old_root,old,create=True,
            deadline=time.monotonic()+60))
        self.assertFalse(old_root.exists())
        self.refusal("SUPERVISED_NO_CURRENT_BOUND_WORKER",lambda:manager.join_current_worker(PROFILE))
        self.refusal("SUPERVISED_CURRENT_WORKER_JOIN_REQUIRED",lambda:manager.allocate(0,{}))
        self.refusal("SUPERVISED_CURRENT_WORKER_JOIN_REQUIRED",lambda:manager.reserve_run("00"*32,
            outer_deadline=time.monotonic()+20))
        manager._worker_session={"nonce":"21"*32,"profile_sha256":PROFILE}
        self.refusal("SUPERVISED_CURRENT_WORKER_JOIN_REQUIRED",lambda:S.current_worker(manager))
        manager._worker_session=None
        self.assertEqual(rows(manager.db),before); self.assertEqual(manager._calls,3)
        self.assertEqual(list((manager.root/"slot-0").iterdir()),[])
        self.assertEqual(list((manager.root/"slot-1").iterdir()),[])
        self.events.update(old_schema_no_root=True,missing_and_serialized_join_refused=True,
                           charged_owner_calls=manager._calls,run_and_slot_rows_unchanged=True)

    def test_profile_foreign_process_expiry_and_census_refusals(self):
        manager=self.manager(); session=self.session(manager); self.store_session(manager,session)
        before=rows(manager.db)
        self.refusal("SUPERVISED_NO_CURRENT_BOUND_WORKER",lambda:manager.join_current_worker("92"*32))
        self.refusal("SUPERVISED_NOT_CURRENT_DIRECT_WORKER",lambda:manager.join_current_worker(PROFILE))
        self.assertIsNone(manager._worker_session); self.assertEqual(rows(manager.db),before)
        expired=deepcopy(session); expired["run_deadline_ns"]=time.monotonic_ns()-1
        expired["recovery_deadline_ns"]=expired["run_deadline_ns"]+25*10**9
        self.store_session(manager,expired); before=rows(manager.db)
        self.refusal("SUPERVISED_RUN_EXPIRED",lambda:manager.join_current_worker(PROFILE))
        self.assertEqual(rows(manager.db),before); self.assertIsNone(manager._worker_session)
        invalid=deepcopy(session); invalid["number"]=3
        self.store_session(manager,invalid); before=rows(manager.db)
        self.refusal("SUPERVISED_SESSION_CENSUS",lambda:S.validate(manager))
        self.assertEqual(rows(manager.db),before)
        self.assertEqual(manager.db.execute("SELECT count(*) FROM meta").fetchone()[0],1)
        self.assertEqual(manager.db.execute("SELECT count(*) FROM slots").fetchone()[0],2)
        self.events.update(foreign_creation_time=True,no_positive_worker_join=True,
                           unchanged_original_limits=True,finite_census_refused=True)

    def test_stale_launch_open_cannot_rewrite_foreign_charged_rows(self):
        manager=self.manager(); current=self.session(manager,number=2); self.store_session(manager,current)
        records=[self.record(manager,current,0,"LIVE"),self.record(manager,current,1,"UNKNOWN")]
        records[0].update(phase="RETIRING",retirement_lower_ms=T)
        self.store_records(manager,records)
        self.assertEqual(manager._records(),records)
        stale=deepcopy(current); stale["number"]=1; stale["nonce"]="22"*32
        launch=self.launch(manager,stale); before=rows(manager.db); manager.close()
        self.refusal("SUPERVISED_OPEN_SESSION_MISMATCH",lambda:S._open_launch(launch,2))
        self.assertEqual(saved_rows(manager.root),before)
        copied=deepcopy(current); copied["binding"]["epoch"]="41"*32
        launch=self.launch(manager,copied)
        self.refusal("SUPERVISED_OPEN_SESSION_MISMATCH",lambda:S._open_launch(launch,2))
        self.assertEqual(saved_rows(manager.root),before)
        self.refusal("SUPERVISED_EXACT_LAUNCH",lambda:S._open_launch(dict(session=current),2))
        self.assertEqual(saved_rows(manager.root),before)
        self.events.update(stale_and_foreign_open_before_rewrite=True,logical_rows_byte_exact=True,
                           preserved_run_charges=[1,1],preserved_session_charge=2,
                           synthetic_retirement_intent_preserved=True,
                           no_generation_or_run_directories_created=True)

    def test_imported_unbound_and_failed_observation_never_quiesce(self):
        manager=self.manager(); session=self.session(manager); self.store_session(manager,session)
        record=self.record(manager,session); self.store_records(manager,[record]); before=rows(manager.db)
        observed=[]
        def reject_observation():
            observed.append("EXPLICIT_FAILED_OBSERVATION")
            raise ValueError("CONTROL_NO_LIVE_JOB_OBSERVATION")
        for imported in (True,dict(status="QUIESCED",active_processes=0,direct_waited=True,session=session)):
            self.refusal("SUPERVISED_UNBOUND_RECOVERY",lambda value=imported:S._commit_quiescence(value,reject_observation))
        launch=self.launch(manager,session)
        self.refusal("SUPERVISED_UNBOUND_RECOVERY",lambda:S._commit_quiescence(launch,reject_observation))
        self.assertEqual(observed,[])
        launch.bound=True
        self.refusal("CONTROL_NO_LIVE_JOB_OBSERVATION",lambda:S._commit_quiescence(launch,reject_observation))
        self.assertEqual(observed,["EXPLICIT_FAILED_OBSERVATION"])
        self.assertEqual(rows(manager.db),before); self.assertEqual(launch.outcome["status"],"UNKNOWN")
        malformed=deepcopy(record); malformed["run_state"]="QUIESCED_UNCLEAN"
        self.refusal("SUPERVISED_STORED_QUIESCENCE",lambda:S.validate_run(manager,malformed))
        malformed["quiescence"]=dict(schema="DMKN_V5_EXACT_JOB_QUIESCENCE_V1",
            session_sha256=record["session"]["session_sha256"],nonce="ff"*32,worker=session["worker"])
        self.refusal("SUPERVISED_STORED_QUIESCENCE",lambda:S.validate_run(manager,malformed))
        joined=deepcopy(record); joined["session"]["run"]=2
        self.refusal("SUPERVISED_STORED_RUN_JOIN",lambda:S.validate_run(manager,joined))
        self.assertEqual(rows(manager.db),before)
        self.events.update(imported_report_not_authority=True,only_observer_raises=True,
                           malformed_unclean_and_run_join_refused=True,no_quiescence_committed=True)

    def test_failed_or_ambiguous_binding_never_arms_launch(self):
        outcomes=[]
        for mode in ("before-commit","after-commit","close-failure"):
            manager=self.manager(mode); session=self.session(manager,state="RESERVED")
            self.store_session(manager,session); launch=self.launch(manager,session)
            root=manager.root; manager.close(); worker=self.foreign_worker(); opened=[]
            original_open=S._open_launch
            def open_with_fault(value,calls):
                actual=original_open(value,calls); opened.append(actual); self.managers.append(actual)
                if mode=="close-failure":
                    original_close=actual.close
                    def fail_closed():
                        original_close()
                        raise OSError("CONTROL_BIND_close-failure")
                    actual.close=fail_closed
                else:
                    actual.db=BindFault(actual.db,mode)
                return actual
            with patch.object(S,"_open_launch",open_with_fault):
                with self.assertRaisesRegex(OSError,"^CONTROL_BIND_"+mode+"$"):
                    S._bind_process(launch,worker)
            self.assertEqual(len(opened),1); actual=opened[0]
            self.assertTrue(actual._closed); self.assertIsNone(actual.db); self.assertIsNone(actual._lock)
            self.assertFalse(launch.bound); self.assertFalse(launch.job_created)
            self.assertEqual(launch.session,session); self.assertEqual(launch.outcome["status"],"UNKNOWN")
            if mode!="close-failure": self.assertTrue(actual._poisoned)
            with closing(sqlite3.connect((root/"generations.sqlite").as_uri()+"?mode=ro",uri=True)) as db:
                number,raw=db.execute("SELECT session_sequence,session FROM meta WHERE id=1").fetchone()
                durable=json.loads(raw); self.assertEqual(number,1)
                self.assertEqual(db.execute("SELECT record FROM slots ORDER BY id").fetchall(),[(None,),(None,)])
            expected=deepcopy(session)
            if mode!="before-commit": expected.update(state="BOUND",worker=worker)
            self.assertEqual(durable,expected)
            if mode!="before-commit":
                before=saved_rows(root)
                self.refusal("SUPERVISED_OPEN_SESSION_MISMATCH",lambda:S._open_launch(launch,2))
                self.assertEqual(saved_rows(root),before)
            outcomes.append(dict(mode=mode,durable_state=durable["state"],session_charge=number,
                                 owner_poisoned=actual._poisoned,launch_armed=False))
        self.events.update(bind_faults=outcomes,launcher_not_invoked=True,synthetic_foreign_worker_only=True,
                           source_ordering_places_resume_after_successful_bind=True)


SELECTED=(
    "test_schema_and_missing_worker_join_refuse_before_effects",
    "test_profile_foreign_process_expiry_and_census_refusals",
    "test_stale_launch_open_cannot_rewrite_foreign_charged_rows",
    "test_imported_unbound_and_failed_observation_never_quiesce",
    "test_failed_or_ambiguous_binding_never_arms_launch",
)


def main():
    global OUTPUT
    parser=argparse.ArgumentParser(); parser.add_argument("--output",required=True)
    parser.add_argument("--release-sha",required=True); args=parser.parse_args()
    need(os.name=="nt" and Path.cwd()==PROJECT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize,"CONTROL_ISOLATED_CANONICAL_OWNER")
    OUTPUT=ordinary(args.output,directory=True)
    need(OUTPUT.is_relative_to(PROJECT/"experiments") and not OUTPUT.is_relative_to(INSTALLATION),"CONTROL_OUTPUT_SCOPE")
    with ExitStack() as guards:
        for owner,name in ((subprocess,"Popen"),(os,"system"),(socket,"socket"),(os,"remove"),
                           (os,"unlink"),(os,"rmdir"),(shutil,"rmtree")):
            guards.enter_context(patch.object(owner,name,forbidden))
        adopt(args.release_sha)
        original_save_session=S._save_session
        def reject_positive_session(manager,session):
            if session["state"]=="QUIESCED": forbidden()
            return original_save_session(manager,session)
        guards.enter_context(patch.object(S,"_save_session",reject_positive_session))
        result=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
        origins=rebind(args.release_sha)
    passed=result.wasSuccessful() and result.testsRun==len(SELECTED) and not result.skipped and not FORBIDDEN
    report=dict(schema="DMKN_SUPERVISED_GENERATIONS_REFUSAL_CONTROLS_V1",status="PASS" if passed else "FAIL",
        selected=list(SELECTED),tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
        skipped=len(result.skipped),observations=OBSERVED,forbidden_calls=FORBIDDEN,sources=SOURCES,origins=origins,
        release_sha256=args.release_sha,actual_processes_started=0,actual_network_calls=0,actual_native_calls=0,
        actual_proof_calls=0,actual_verifier_calls=0,positive_worker_join=False,positive_actor_closure=False,
        positive_os_quiescence=False,synthetic_sessions_and_rows="REFUSAL_INPUTS_ONLY",
        sqlite_internal_journal_deletions="NOT_OBSERVED_OR_COUNTED",managed_deletions=0,
        old_suites_imported=False,old_data_deleted=False,physical_envelope_adopted=False,mathematical_acceptance=False)
    raw=encode(report)+b"\n"; need(len(raw)<=MIB,"CONTROL_REPORT_BOUND")
    with (OUTPUT/"supervised-generations-controls-result.json").open("xb") as stream:
        need(stream.write(raw)==len(raw),"CONTROL_SHORT_WRITE")
    return 0 if passed else 1


if __name__=="__main__": raise SystemExit(main())

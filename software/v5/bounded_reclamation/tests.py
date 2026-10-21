"""Fixture-only reclamation controls. Root separately selects any execution.

No existing generation is adopted. Positive fixtures use legitimate zero-run
retirement and synthetic known-layout bytes, not real Workspace/actor closure.
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

PROJECT=Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
INSTALLATION=PROJECT/"product-local/v5-distribution-consolidated-01/Mathematical Commons v5"
SOURCE=Path(__file__).resolve().parent
MIB=1024**2
T=2000000000000
EXTRA={
    "placement.reclaim":("placement/reclaim.py",12387,"19713fc4baec821a5c77a0071182c63401b292cbe79a7ed7c04b7deba50e1894"),
    "placement.lifecycle":("placement/lifecycle.py",36902,"d59615b664ca8dc934d07778046164313d226965cc3b2486e1e98d15bd57d9ef"),
}
L=R=OUTPUT=None
SOURCES={}; OBSERVED={}; ENROLLED={}; EFFECTS=[]; FORBIDDEN=[]
RAW_UNLINK,RAW_RMDIR=os.unlink,os.rmdir


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
    FORBIDDEN.append("FORBIDDEN_PROCESS_SOCKET_OR_BROAD_DELETE")
    raise AssertionError(FORBIDDEN[-1])


def effect(kind,path,*args,**kwargs):
    need(not args and not kwargs and isinstance(path,(str,Path)),"CONTROL_NO_RELATIVE_FD_DELETE")
    target=Path(path)
    roots=[root for root,items in ENROLLED.items() if items.get(target)==kind]
    need(len(roots)==1,"CONTROL_EXACT_ENROLLED_DELETE_TARGET")
    root=roots[0]
    need(root.is_relative_to(OUTPUT) and root!=OUTPUT and root.name.startswith("g")
         and root.parent.name in ("slot-0","slot-1"),"CONTROL_FRESH_GENERATION_DELETE_SCOPE")
    ordinary(target,directory=kind=="directory")
    if kind=="file": need(target.stat().st_nlink==1,"CONTROL_NO_ALIAS_DELETE")
    (RAW_UNLINK if kind=="file" else RAW_RMDIR)(target)
    EFFECTS.append(dict(kind=kind,path=str(target),root=str(root)))


def adopt(release_sha):
    global L,R
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
        target=SOURCE/relative; pin(target,size,digest)
        parent=__import__(name.split(".")[0])
        spec=importlib.util.spec_from_file_location(name,target)
        module=importlib.util.module_from_spec(spec); sys.modules[name]=module
        spec.loader.exec_module(module); setattr(parent,name.split(".")[1],module)
        SOURCES["v5/"+relative]=dict(path=str(target),bytes=size,sha256=digest)
    R,L=sys.modules["placement.reclaim"],sys.modules["placement.lifecycle"]
    return release


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
    need(len(SOURCES)==123,"CONTROL_121_PLUS_TWO")
    return origins


class CommitFault:
    """Real SQLite proxy; inject one before-COMMIT or lost-acknowledgment fault."""
    def __init__(self,db,mode): self.db=db; self.mode=mode; self.armed=False; self.fired=False
    def __getattr__(self,name): return getattr(self.db,name)
    def execute(self,sql,parameters=()):
        if sql=="UPDATE slots SET record=NULL WHERE id=?" and self.mode=="after-free": self.armed=True
        if sql=="UPDATE slots SET record=? WHERE id=?" and self.mode=="before-window":
            value=json.loads(parameters[0]); facet=value.get("reclaim",{})
            if facet.get("window_end",0)>facet.get("cursor",0): self.armed=True
        if sql=="COMMIT" and self.armed and not self.fired:
            self.fired=True
            if self.mode=="after-free": self.db.execute(sql,parameters)
            raise OSError("CONTROL_COMMIT_UNCERTAIN_"+self.mode)
        return self.db.execute(sql,parameters)


class Controls(unittest.TestCase):
    def setUp(self):
        self.root=OUTPUT/("c%02d"%(SELECTED.index(self._testMethodName)+1)); self.root.mkdir()
        self.managers=[]; self.events={}; self.effect_start=len(EFFECTS)

    def tearDown(self):
        for manager in reversed(self.managers):
            for handle in manager._handles.values():
                self.assertIsNone(handle.service); self.assertIsNone(handle.location)
            if not manager._closed: manager._release()
        self.events["managed_effects"]=len(EFFECTS)-self.effect_start
        OBSERVED[self._testMethodName]=self.events

    def config(self,cleanup=MIB):
        endpoint=lambda p:dict(host="127.0.0.1",port=p,tls=False,server_name=None)
        return dict(schema=L.SCHEMA,epoch=sha(str(self.root).encode()),clock_model_id="c1"*32,
            registry_pages=64,owner_reserved_bytes=4*MIB,registry_reserved_bytes=MIB,
            cleanup_reserved_bytes=cleanup,protected_roots=[str(SOURCE),str(INSTALLATION)],
            slots=[dict(reserved_bytes=MIB,max_cells=1,max_runs=1,read_endpoint=endpoint(44301+3*i),
                intake_endpoint=endpoint(44302+3*i),listen=["/ip4/127.0.0.1/tcp/"+str(44303+3*i)]) for i in range(2)])

    def manager(self,name="managed",create=True,cleanup=MIB):
        manager=L.ManagedGenerations.open(self.root/name,self.config(cleanup),create=create,
            deadline=time.monotonic()+60,calls=512,cpu_seconds=30)
        self.managers.append(manager); return manager

    def allocate(self,manager,slot=0):
        spec=manager.config["slots"][slot]
        egress=dict(schema="DMKN_V5_OWNER_EGRESS_V1",mode="loopback-test",public_ports=[],
            test_endpoints=[dict(host="127.0.0.1",port=p) for p in range(44301,44307)])
        placement=dict(schema=L.P.CONFIG_SCHEMA,service_epoch=manager.config["epoch"],namespace="a1"*32,
            wire_profile_id="b1"*32,admission_close_ms=T-1000,retention_not_after_ms=T,max_grants=1,
            max_requests=1,max_cells=1,max_runs=1,ledger_pages=256,limits={key:1 for key in L.P.RESOURCES})
        record=manager.allocate(slot,dict(workspace={"fixture":"UNOPENED"},service_limits={"fixture":"UNOPENED"},
            placement=placement,egress=egress,location=dict(schema="DMKN_V5_MAINTAINED_LOCATION_ROLES_V1",
            role="index-provider",namespace=placement["namespace"],egress=egress,listen=deepcopy(spec["listen"]),
            announce=[],bootstrap=[],endpoints=[deepcopy(spec["read_endpoint"])],limits={})))
        root=manager.generation_path(record)
        self.assertTrue(root.is_relative_to(self.root)); self.assertNotIn(root,ENROLLED)
        ENROLLED[root]={root/relative if relative else root:kind for relative,kind in R.layout(0)}
        return record

    def clock(self,manager,lower=T):
        return manager.adopt_clock(lower_utc_ms=lower,valid_for_ms=60000,rate_error_ppm=0,
                                   model_id=manager.config["clock_model_id"])

    def retire(self,manager,record):
        clock=self.clock(manager); manager.begin_retire(record["generation"],clock)
        return manager.commit_retired(record["generation"],clock)

    def profile(self,**changes):
        value=dict(layout=R.LAYOUT,ownership=R.OWNERSHIP,max_calls=4,max_entries_per_call=20,max_apparent_bytes=MIB)
        value.update(changes); return value

    def fill(self,manager,record):
        root=manager.generation_path(record)
        for relative,kind in R.layout(0):
            if not relative or relative=="generation.json": continue
            path=root/relative
            if kind=="directory": path.mkdir(parents=True,exist_ok=True)
            else:
                path.parent.mkdir(parents=True,exist_ok=True)
                with path.open("xb") as stream: stream.write(b"SYNTHETIC_KNOWN_LAYOUT_NOT_A_WORKSPACE_DATABASE")

    def fixture(self,name,full=False,**manager_args):
        manager=self.manager(name,**manager_args); record=self.allocate(manager)
        if full: self.fill(manager,record)
        return manager,self.retire(manager,record)

    def reopen(self,manager):
        name=manager.root.name; cleanup=manager.config["cleanup_reserved_bytes"]
        manager._release(); return self.manager(name,create=False,cleanup=cleanup)

    def step(self,manager,record,entries=20):
        return manager.reclaim_step(record["generation"],max_entries=entries,deadline=time.monotonic()+10)

    def rows(self,manager):
        def tag(x): return {"blob":x.hex()} if isinstance(x,bytes) else x
        return {table:[[tag(x) for x in row] for row in manager.db.execute("SELECT * FROM "+table+" ORDER BY id")]
                for table in ("meta","slots")}

    def tree(self,root):
        if not root.exists(): return None
        paths=sorted(root.rglob("*")); self.assertLessEqual(len(paths),128); rows=[]
        for path in paths:
            if path.parent==root and path.name in ("generations.sqlite","generations.sqlite-journal","owner.lock"): continue
            if path.is_dir(): rows.append((path.relative_to(root).as_posix(),"directory"))
            else:
                self.assertLessEqual(path.stat().st_size,MIB)
                with path.open("rb") as stream: digest=sha(stream.read(MIB+1))
                rows.append((path.relative_to(root).as_posix(),digest))
        return rows

    def refuse(self,manager,operation,code,charged=False):
        before=self.rows(manager); files=self.tree(manager.root); effects=len(EFFECTS)
        with self.assertRaisesRegex(ValueError,"^"+code+"$"): operation()
        self.assertEqual(self.tree(manager.root),files); self.assertEqual(len(EFFECTS),effects)
        if not charged: self.assertEqual(self.rows(manager),before)
        else:
            old=json.loads(bytes.fromhex(before["slots"][0][1]["blob"]))
            now=manager._find(old["generation"],retired=True)
            expected=deepcopy(old); expected["reclaim"]["calls"]+=1
            expected["reclaim"]["failure"]="RECLAIM_STEP_INCOMPLETE"
            self.assertEqual(now,expected)
        self.events.setdefault("refusals",[]).append(code)

    def test_none_retirement_reclaims_exact_layout_and_reuses_higher_sequence(self):
        manager,a=self.fixture("positive",full=True); b=self.allocate(manager,1)
        root=manager.generation_path(a); other=manager.generation_path(b)
        other_before=self.tree(other); record_before=manager._find(b["generation"])
        before=len(EFFECTS); intent=manager.begin_reclamation(a["generation"],self.profile())
        self.assertEqual(len(EFFECTS),before); self.assertEqual(intent["reclaim"]["entry_count"],20)
        self.assertTrue(all(R.validate(manager,intent)))
        result=self.step(manager,a); self.assertEqual(result["status"],"FREE")
        self.assertEqual(result["charged_reclaim_calls"],1); self.assertFalse(root.exists())
        deleted=EFFECTS[before:]; self.assertEqual(len(deleted),20)
        self.assertEqual([row["path"] for row in deleted[-2:]],[str(root/"generation.json"),str(root)])
        self.assertEqual(self.tree(other),other_before); self.assertEqual(manager._find(b["generation"]),record_before)
        self.refuse(manager,lambda:self.step(manager,a),"GENERATIONS_NOT_CURRENTLY_REGISTERED")
        new=self.allocate(manager); self.assertEqual(new["sequence"],3); self.assertNotEqual(new["generation"],a["generation"])
        state=manager.status(); self.assertEqual(state["retired_floor"],1); self.assertFalse(state["physical_envelope_adopted"])
        self.events.update(zero_run_no_actor_closure=True,synthetic_layout_bytes=True,other_slot_unchanged=True,
                           marker_then_root_last=True,higher_sequence=3)

    def test_retirement_clock_closure_and_initial_marker_authority_refuse(self):
        manager=self.manager("unretired"); record=self.allocate(manager)
        self.refuse(manager,lambda:manager.begin_reclamation(record["generation"],self.profile()),"RECLAIM_RETIRED_CLOSURE_REQUIRED")
        early=self.clock(manager,T-100000)
        self.refuse(manager,lambda:manager.begin_retire(record["generation"],early),"GENERATIONS_RETENTION_STILL_PROMISED")
        handle=manager.reserve_run(record["generation"],outer_deadline=time.monotonic()+20)
        manager=self.reopen(manager); self.assertIsNone(handle.service); self.assertIsNone(handle.location)
        clock=self.clock(manager); manager.begin_retire(record["generation"],clock)
        self.refuse(manager,lambda:manager.commit_retired(record["generation"],clock),"GENERATIONS_RETIRE_CLOSURE_UNKNOWN")
        self.refuse(manager,lambda:manager.begin_reclamation(record["generation"],self.profile()),"RECLAIM_RETIRED_CLOSURE_REQUIRED")
        wrong,a=self.fixture("marker"); marker=wrong.generation_path(a)/"generation.json"
        with marker.open("wb") as stream: stream.write(b"FOREIGN_FIXTURE_MARKER")
        self.refuse(wrong,lambda:wrong.begin_reclamation(a["generation"],self.profile()),"GENERATIONS_GENERATION_MARKER")
        missing,b=self.fixture("missing-marker"); original=L._read
        def absent(path,*args):
            if Path(path)==missing.generation_path(b)/"generation.json": raise FileNotFoundError("CONTROL_MISSING_MARKER")
            return original(path,*args)
        before=self.rows(missing); files=self.tree(missing.root)
        with patch.object(L,"_read",absent),self.assertRaises(FileNotFoundError):
            missing.begin_reclamation(b["generation"],self.profile())
        self.assertEqual(self.rows(missing),before); self.assertEqual(self.tree(missing.root),files)
        original_path=L.ordinary
        def absent_root(path,*args,**kwargs):
            if Path(path)==missing.generation_path(b): raise FileNotFoundError("CONTROL_MISSING_ROOT")
            return original_path(path,*args,**kwargs)
        with patch.object(L,"ordinary",absent_root),self.assertRaises(FileNotFoundError):
            missing.begin_reclamation(b["generation"],self.profile())
        self.assertEqual(self.rows(missing),before); self.assertEqual(self.tree(missing.root),files)
        self.events.update(missing_marker_and_root_simulated=True,unknown_not_forged_closed=True)

    def test_unknown_operations_sibling_alias_and_reparse_preserve_targets(self):
        for label,relative in (("unknown","unclassified"),("operations","workspace/operations/owner-work"),("extra-run","run-0001")):
            manager,record=self.fixture(label); path=manager.generation_path(record)/relative
            path.parent.mkdir(parents=True,exist_ok=True)
            with path.open("xb") as stream: stream.write(b"PRESERVE")
            self.refuse(manager,lambda:manager.begin_reclamation(record["generation"],self.profile()),"RECLAIM_UNKNOWN_ENTRY")
        manager,record=self.fixture("sibling"); (manager.root/"slot-0"/"g99999999999999999999").mkdir()
        self.refuse(manager,lambda:manager.begin_reclamation(record["generation"],self.profile()),"RECLAIM_UNEXPECTED_SLOT_ENTRY")
        manager,record=self.fixture("hardlink"); root=manager.generation_path(record); (root/"workspace").mkdir()
        first=root/"workspace/owner.lock"; second=root/"workspace/workspace.sqlite"
        with first.open("xb") as stream: stream.write(b"OWN_FIXTURE_ALIAS")
        os.link(first,second)
        self.refuse(manager,lambda:manager.begin_reclamation(record["generation"],self.profile()),"RECLAIM_HARDLINK_ALIAS")
        manager,record=self.fixture("reparse",full=True); target=manager.generation_path(record)/"workspace/owner.lock"
        original=Path.lstat; before=self.rows(manager); files=self.tree(manager.root)
        def reparse(path,*args,**kwargs):
            info=original(path,*args,**kwargs)
            if path==target:
                return SimpleNamespace(st_mode=info.st_mode,st_file_attributes=0x400,st_nlink=info.st_nlink,
                                       st_size=info.st_size,st_dev=info.st_dev,st_ino=info.st_ino)
            return info
        with patch.object(Path,"lstat",reparse),self.assertRaisesRegex(ValueError,"^RECLAIM_LINK_OR_REPARSE$"):
            manager.begin_reclamation(record["generation"],self.profile())
        self.assertEqual(self.rows(manager),before); self.assertEqual(self.tree(manager.root),files)
        self.events.update(actual_hardlink_only_between_fresh_files=True,reparse_stat_synthetic=True)

    def test_profile_bitmap_metadata_and_apparent_byte_bounds(self):
        manager,record=self.fixture("profile")
        self.refuse(manager,lambda:manager.begin_reclamation(record["generation"],self.profile(ownership="UNKNOWN")),"RECLAIM_LAYOUT_OR_OWNERSHIP")
        self.refuse(manager,lambda:manager.begin_reclamation(record["generation"],self.profile(max_apparent_bytes=1)),"RECLAIM_APPARENT_BYTE_CAP")
        small,small_record=self.fixture("metadata",cleanup=1)
        self.refuse(small,lambda:small.begin_reclamation(small_record["generation"],self.profile()),"RECLAIM_METADATA_ALLOCATION")
        items=R.layout(4096); self.assertEqual(len(items),36884); self.assertEqual(len(set(items)),36884)
        self.assertEqual(items[-2:],[("generation.json","file"),("","directory")])
        bits=R._bits([True]*len(items)); self.assertEqual(len(bits),9222); self.assertTrue(all(R._flags(bits,len(items))))
        with self.assertRaisesRegex(ValueError,"^RECLAIM_BITMAP_PADDING$"): R._flags("0000f0",20)
        with self.assertRaisesRegex(ValueError,"^RECLAIM_RUN_BOUND$"): R.layout(4097)
        intent=manager.begin_reclamation(record["generation"],self.profile())
        self.assertLessEqual(len(L.F.compact(intent)),L.MAX_RECORD)
        self.refuse(manager,lambda:self.step(manager,record,21),"RECLAIM_WINDOW_BOUND")
        self.refuse(manager,lambda:manager.reclaim_step(record["generation"],max_entries=20,
            deadline=time.monotonic()-1),"GENERATIONS_DEADLINE")
        altered=deepcopy(intent); altered["reclaim"]["entry_count"]+=1
        with self.assertRaisesRegex(ValueError,"^RECLAIM_STORED_CENSUS$"): R.validate(manager,altered)
        self.events.update(maximum_layout_logic_only=True,no_maximum_tree_created=True,synthetic_bad_facet=True)

    def test_admitted_census_refusal_charges_cap_and_identity_change_holds(self):
        manager,record=self.fixture("cap"); manager.begin_reclamation(record["generation"],self.profile(max_calls=1))
        with (manager.generation_path(record)/"new-unknown").open("xb") as stream: stream.write(b"PRESERVE")
        self.refuse(manager,lambda:self.step(manager,record),"RECLAIM_UNKNOWN_ENTRY",charged=True)
        manager=self.reopen(manager)
        self.refuse(manager,lambda:self.step(manager,record),"RECLAIM_CALL_CAP")
        self.refuse(manager,lambda:self.allocate(manager),"GENERATIONS_SLOT_OCCUPIED")
        other,b=self.fixture("identity"); other.begin_reclamation(b["generation"],self.profile())
        expected=other.generation_path(b).stat().st_ino; original=R._identity
        def changed(info):
            result=original(info)
            return [result[0],result[1]+1] if info.st_ino==expected else result
        with patch.object(R,"_identity",changed):
            self.refuse(other,lambda:self.step(other,b),"RECLAIM_ROOT_IDENTITY_CHANGED",charged=True)
        self.events.update(census_refusal_consumes_original_cap=True,identity_fault_synthetic=True,
                           owner_mutation_after_intent_explicit=True)

    def test_interrupted_effect_prefix_and_midwindow_deadline(self):
        manager,record=self.fixture("prefix",full=True); root=manager.generation_path(record)
        manager.begin_reclamation(record["generation"],self.profile()); original=os.unlink
        def interrupt(path,*args,**kwargs):
            original(path,*args,**kwargs); raise OSError("CONTROL_AFTER_UNLINK")
        with patch.object(R.os,"unlink",interrupt),self.assertRaisesRegex(OSError,"CONTROL_AFTER_UNLINK"):
            self.step(manager,record)
        held=manager._find(record["generation"],retired=True)["reclaim"]
        self.assertEqual((held["cursor"],held["window_end"],held["calls"]),(0,20,1))
        self.assertFalse((root/"workspace/owner.lock").exists()); self.assertTrue((root/"workspace/workspace.sqlite").exists())
        manager=self.reopen(manager); result=self.step(manager,record)
        self.assertEqual((result["status"],result["charged_reclaim_calls"]),("FREE",2)); self.assertFalse(root.exists())
        timed,b=self.fixture("deadline",full=True); timed.begin_reclamation(b["generation"],self.profile())
        now=time.monotonic(); deadline=now+10; clock=[now]
        def expire(path,*args,**kwargs): original(path,*args,**kwargs); clock[0]=deadline+1
        with patch.object(L.time,"monotonic",side_effect=lambda:clock[0]),patch.object(R.os,"unlink",expire):
            with self.assertRaisesRegex(ValueError,"^RECLAIM_ACTION_DEADLINE$"):
                timed.reclaim_step(b["generation"],max_entries=20,deadline=deadline)
        held=timed._find(b["generation"],retired=True)["reclaim"]
        self.assertEqual((held["cursor"],held["window_end"],held["calls"]),(0,20,1))
        self.assertTrue(timed.generation_path(b).exists())
        self.events.update(after_effect_exception_synthetic=True,prepaid_prefix_resumed=True,
                           monotonic_deadline_jump_synthetic=True,timeout_held=True)

    def test_marker_root_and_before_free_interruptions_resume_without_recreation(self):
        for label in ("marker","root","before-free"):
            manager,record=self.fixture(label); root=manager.generation_path(record)
            manager.begin_reclamation(record["generation"],self.profile()); before=len(EFFECTS)
            unlink,rmdir,absent=os.unlink,os.rmdir,R.absent; calls=[0]
            def marker_fault(path,*args,**kwargs):
                unlink(path,*args,**kwargs)
                if label=="marker": raise OSError("CONTROL_MARKER_WINDOW")
            def root_fault(path,*args,**kwargs):
                rmdir(path,*args,**kwargs)
                if label=="root": raise OSError("CONTROL_ROOT_WINDOW")
            def free_fault(*args):
                calls[0]+=1; result=absent(*args)
                if label=="before-free" and calls[0]==2: raise OSError("CONTROL_BEFORE_FREE")
                return result
            with patch.object(R.os,"unlink",marker_fault),patch.object(R.os,"rmdir",root_fault),patch.object(R,"absent",free_fault):
                with self.assertRaises(OSError): self.step(manager,record)
            held=manager._find(record["generation"],retired=True)
            self.assertEqual((held["phase"],held["reclaim"]["calls"]),("RECLAIMING",1))
            self.assertFalse((root/"generation.json").exists()); self.assertEqual(root.exists(),label=="marker")
            manager=self.reopen(manager); result=self.step(manager,record)
            self.assertEqual((result["status"],result["charged_reclaim_calls"]),("FREE",2))
            self.assertFalse(root.exists()); self.assertEqual(len(EFFECTS)-before,2)
        self.events.update(explicit_exception_windows=["marker","root","before-free"],actual_two_effects_each=True,
                           no_root_or_marker_recreation=True)

    def test_reconciliation_rejects_unpaid_holes_reappearance_and_unenrolled_roles(self):
        original=[True]*4
        self.assertEqual(R.reconcile(original,[False,True,True,True],0,2),1)
        for current,cursor,end,code in (([True,False,True,True],0,2,"RECLAIM_NONPREFIX_ABSENCE"),
            ([True,True,False,True],0,2,"RECLAIM_UNPREPAID_ABSENCE"),
            ([True,True,True,True],1,2,"RECLAIM_DELETED_ENTRY_REAPPEARED")):
            with self.assertRaisesRegex(ValueError,"^"+code+"$"): R.reconcile(original,current,cursor,end)
        with self.assertRaisesRegex(ValueError,"^RECLAIM_UNENROLLED_ENTRY$"):
            R.reconcile([False,True],[True,True],0,2)
        self.events.update(pure_presence_vectors=True,no_extra_files_deleted=True)

    def test_commit_uncertainty_preserves_charge_or_durable_free_and_poisons_session(self):
        for mode in ("before-window","after-free"):
            manager,record=self.fixture(mode); root=manager.generation_path(record)
            manager.begin_reclamation(record["generation"],self.profile()); before=len(EFFECTS)
            proxy=CommitFault(manager.db,mode); manager.db=proxy
            with self.assertRaisesRegex(OSError,"CONTROL_COMMIT_UNCERTAIN_"): self.step(manager,record)
            self.assertTrue(proxy.fired); self.assertTrue(manager._poisoned)
            with self.assertRaisesRegex(ValueError,"^GENERATIONS_CLOSED_OR_UNCERTAIN$"): manager.status()
            manager=self.reopen(manager); state=manager.status()
            if mode=="before-window":
                held=state["slots"][0]; self.assertEqual(held["phase"],"RECLAIMING")
                self.assertEqual((held["reclaim"]["calls"],held["reclaim"]["window_end"]),(1,0))
                self.assertTrue(root.exists()); self.assertEqual(len(EFFECTS),before)
            else:
                self.assertIsNone(state["slots"][0]); self.assertFalse(root.exists())
                self.assertEqual(len(EFFECTS)-before,2); self.assertEqual(self.allocate(manager)["sequence"],2)
        self.events.update(real_sqlite_with_explicit_commit_faults=True,postcommit_ack_loss_synthetic=True,
                           poison_prevents_stale_rewrite=True)


SELECTED=(
    "test_none_retirement_reclaims_exact_layout_and_reuses_higher_sequence",
    "test_retirement_clock_closure_and_initial_marker_authority_refuse",
    "test_unknown_operations_sibling_alias_and_reparse_preserve_targets",
    "test_profile_bitmap_metadata_and_apparent_byte_bounds",
    "test_admitted_census_refusal_charges_cap_and_identity_change_holds",
    "test_interrupted_effect_prefix_and_midwindow_deadline",
    "test_marker_root_and_before_free_interruptions_resume_without_recreation",
    "test_reconciliation_rejects_unpaid_holes_reappearance_and_unenrolled_roles",
    "test_commit_uncertainty_preserves_charge_or_durable_free_and_poisons_session",
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
        for owner,name in ((subprocess,"Popen"),(os,"system"),(socket,"socket"),(os,"remove"),(shutil,"rmtree")):
            guards.enter_context(patch.object(owner,name,forbidden))
        guards.enter_context(patch.object(os,"unlink",lambda p,*a,**k:effect("file",p,*a,**k)))
        guards.enter_context(patch.object(os,"rmdir",lambda p,*a,**k:effect("directory",p,*a,**k)))
        adopt(args.release_sha)
        result=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
        origins=rebind(args.release_sha)
    passed=result.wasSuccessful() and result.testsRun==len(SELECTED) and not result.skipped and not FORBIDDEN
    report=dict(schema="DMKN_BOUNDED_RECLAMATION_FIXTURE_CONTROLS_V1",status="PASS" if passed else "FAIL",
        selected=list(SELECTED),tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
        skipped=len(result.skipped),observations=OBSERVED,forbidden_calls=FORBIDDEN,sources=SOURCES,origins=origins,
        enrolled_roots=[str(p) for p in ENROLLED],managed_reclamation_effects=EFFECTS,
        release_sha256=args.release_sha,actual_node_children=0,actual_network_calls=0,actual_native_calls=0,
        actual_proof_calls=0,actual_verifier_calls=0,real_service_started=False,positive_actor_closure=False,
        synthetic_known_layout_bytes=True,sqlite_internal_journal_deletions="NOT_OBSERVED_OR_COUNTED",
        old_suites_imported=False,old_data_deleted=False,physical_envelope_adopted=False,mathematical_acceptance=False)
    raw=encode(report)+b"\n"; need(len(raw)<=MIB,"CONTROL_REPORT_BOUND")
    with (OUTPUT/"bounded-reclamation-controls-result.json").open("xb") as stream:
        need(stream.write(raw)==len(raw),"CONTROL_SHORT_WRITE")
    return 0 if passed else 1


if __name__=="__main__": raise SystemExit(main())

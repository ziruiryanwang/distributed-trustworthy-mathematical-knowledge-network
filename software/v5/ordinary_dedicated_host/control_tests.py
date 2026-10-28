"""Focused dedicated-host boundary controls; root selects execution separately.

Loads only exact package-pinned owner/run/custodian source. Uses inert SDK doubles
and scratch files; no mathematical owner, database, native worker or application
network. Real Windows byte locks and asyncio cancellation ordering are exercised.
"""
from __future__ import annotations

import argparse
import asyncio
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import time
from types import SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
START, CPU = time.monotonic(), time.process_time()
MIB = 1024**2


def need(value, code):
    if not value:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU < 25,
         "CONTROL_ORIGINAL_ALLOWANCE")


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                      separators=(",", ":")).encode("ascii")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, expected=None):
    path = Path(path)
    need(path.is_absolute() and ".." not in path.parts, "CONTROL_PATH")
    for item in (path, *path.parents):
        info = item.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "CONTROL_REDIRECT")
    need(path.is_file() and path.stat().st_nlink == 1, "CONTROL_SINGLE_FILE")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB, "CONTROL_SOURCE_BOUND")
    if expected is not None:
        need(digest(raw) == expected, "CONTROL_PIN")
    return raw


def refused(call, text=None, kinds=(ValueError,)):
    try:
        call()
    except kinds as error:
        if text is not None:
            need(text in str(error), "CONTROL_WRONG_REFUSAL:"+str(error))
        return error
    raise AssertionError("CONTROL_EXPECTED_REFUSAL")


def forbidden(*args, **kwargs):
    raise AssertionError("CONTROL_FORBIDDEN_EFFECT")


def fields(value, keys, code):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError(code)


def uint(value, low, high, code):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(code)
    return value


def hexid(value):
    if type(value) is not str or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise ValueError("INERT_HEX")
    return value


def fake_support():
    """No evidence codec or mathematical authority is claimed by these doubles."""
    def bounded(path, maximum):
        raw = Path(path).read_bytes()
        need(0 < len(raw) <= maximum, "INERT_READ_BOUND")
        return raw
    def fresh(path, raw):
        with Path(path).open("xb") as stream:
            stream.write(raw)
    A = NS(C=NS(ordinary=lambda path, **kw: Path(path), read_bounded=bounded, hexid=hexid),
        E=NS(canonical_json=canonical, name_key=lambda name: canonical(name)),
        P=NS(fields=fields, uint=uint, PortableCatalog=NS(_write_fresh=fresh)),
        S=NS(semantic_id=lambda: "1"*64, export_id=lambda *args: "3"*64))
    custody_limits = dict(objects=256, exports=2048, logical_bytes=16*MIB, db_pages=4096)
    index_limits = dict(max_objects=256, max_postings=32768, max_features=8192,
                        max_snapshots=257, max_logical_bytes=16*MIB, max_db_pages=4096)
    O = NS(STORE_LIMITS={key: (1, value) for key, value in custody_limits.items()})
    def limits(value, bounds, code):
        fields(value, bounds, code)
        for key, (low, high) in bounds.items():
            uint(value[key], low, high, code)
    api = NS(F=NS(compact=canonical, strict=lambda raw, maximum: json.loads(raw)),
        _limits=limits, _fields=fields, DS=NS(LIMITS={key:(1,value) for key,value in index_limits.items()}),
        OrdinaryExportAdapter=lambda semantic: NS(namespace="2"*64))
    return A, O, api, custody_limits, index_limits


def guard_controls(owner, launcher, base):
    marked = base/"marked"; marked.mkdir()
    (marked/"DMKN-DEDICATED-HOST.json").write_bytes(b"malformed-still-excludes")
    child = marked/"custody"; child.mkdir()
    clean = base/"clean"; clean.mkdir()
    for selected in (marked, child, child/"fresh-output"):
        refused(lambda selected=selected: owner.reject_dedicated(selected), "OWNER_DEDICATED_HOST_PATH")
        refused(lambda selected=selected: owner.separated([selected, clean], "OVERLAP"),
                "OWNER_DEDICATED_HOST_PATH")
    owner.reject_dedicated(clean/"fresh")
    with patch.object(Path, "lstat", side_effect=PermissionError("injected")):
        refused(lambda: owner.reject_dedicated(clean), kinds=(PermissionError,))
    support = [base/name for name in ("package", "python", "lean")]
    for path in support:
        path.mkdir()
    options = {"host-root": str(marked), "output": str(base/"host-output")}
    launcher.separate_arguments(*support, base/"host-logs", options, tool="host")
    refused(lambda: launcher.separate_arguments(*support, base/"ordinary-logs", options, tool="peer"),
            "DEDICATED_HOST")
    refused(lambda: launcher.separate_arguments(*support, marked/"logs", options, tool="host"))
    refused(lambda: launcher.separate_arguments(*support, base/"logs2",
        {"host-root":str(marked), "output":str(marked/"out")}, tool="host"))
    refused(lambda: launcher.separate_arguments(*support, base/"logs3", {},
                                                extra_state=(child,), tool="peer"), "DEDICATED_HOST")
    need(not (marked/"logs").exists() and not (marked/"out").exists(), "NO_LAUNCH_LOG_EFFECT")
    return marked


def producer_control(owner, marked, base):
    raw = canonical({"inert": True}); calls = []
    A = NS(C=NS(hexid=hexid, ordinary=lambda path, **kw:Path(path),
                read_bounded=lambda path, maximum: raw), sha=digest,
           _writer_json=lambda value, maximum:json.loads(value))
    G, X = object(), object()
    def prohibited_producer(*args, **kwargs):
        calls.append("producer"); raise AssertionError("PRODUCER_REACHED_MARKED_ROOT")
    loaded = NS(A=A, G=G, installation=object(), profile=object(), library_extraction=X,
                baseline_production=NS(A=A,G=G,X=X,produce_bundle=prohibited_producer))
    allocation = NS(check=check, deadline=time.monotonic()+30, report=lambda:{},
                    operation=forbidden)
    args = NS(operation="produce-baseline", profile_sha256="a"*64,
        python_runtime=str(base/"python"), lean_runtime=str(base/"lean"),
        wall_seconds=45,cpu_seconds=20,memory_mib=768,
        project_production=str(base/"project.json"),project_production_sha256=digest(raw),
        approve_local_project=True,spool_mib=144,output_names=str(base/"names.json"),
        output=str(marked/"producer-output"))
    with patch.object(owner,"Allowance",return_value=allocation), patch.object(owner,"bootstrap",
            return_value=NS(load=lambda *args,**kwargs:loaded)):
        report = owner.run_producer(args)
    need(report["ok"] is False and report["error"] == "OWNER_DEDICATED_HOST_PATH" and
         not calls and not (marked/"producer-output").exists(), "PRODUCER_GUARD_BEFORE_EFFECT")


def lock_and_close_controls(H, A, base):
    root = base/"lock-host"
    report = H._report("prepare", root, "a"*64)
    with H._locked(A, root, report, create=True):
        need(report["host_lock_closure"] == "OPEN", "REAL_LOCK_OPEN")
        def contend():
            other = H._report("serve", root, "a"*64)
            with H._locked(A, root, other, create=False):
                raise AssertionError("OVERLAPPING_LOCK_ENTERED")
        refused(contend, kinds=(OSError, ValueError))
    need(report["host_lock_closure"] == "CLOSED", "REAL_LOCK_CLOSED")
    with H._locked(A, root, H._report("serve",root,"a"*64),create=False):
        pass
    events = []
    class Broken:
        db = object()
        def close(self):
            events.append("index"); raise ValueError("injected close")
    class Good:
        db = object()
        def close(self):
            events.append("custody"); self.db = None
    failed = H._report("serve",root,"a"*64)
    error = H._close(Broken(),Good(),failed)
    need(error is not None and events == ["index","custody"] and
         failed["index_closure"] == "UNCERTAIN" and failed["custody_closure"] == "CLOSED",
         "CLOSE_FAILURE_ATTEMPTS_BOTH")
    unresolved = NS(db=object(),close=lambda:None)
    failed = H._report("serve",root,"a"*64)
    need(H._close(unresolved,None,failed) is not None and failed["index_closure"] == "UNCERTAIN",
         "FALSE_CLEAN_CLOSE_REFUSED")
    return root


def seal_controls(H, A, O, api, custody_limits, index_limits, base):
    root = base/"seal-host"; root.mkdir()
    seal = dict(schema=H.SEAL_SCHEMA,profile_sha256="a"*64,semantic_id="1"*64,namespace="2"*64,
        manifest_sha256="5"*64,targets=[dict(name=[[0,{"$bytes":[88]}]],export_id="3"*64,unit_id="4"*64)],
        custody_limits=custody_limits,index_limits=index_limits,
        custody_counts=dict(objects=2,exports=1,logical_bytes=100),index_snapshot_id="6"*64,
        index_objects=1,assurance=H.ASSURANCE,mathematical_acceptance=False)
    def parse(value, pin=None):
        raw = canonical(value); (root/"HOST.json").write_bytes(raw)
        return H._read_seal(A,O,api,root,"a"*64,pin or digest(raw))
    need(parse(seal) == seal,"SEAL_LITERAL_BOUNDARY")
    refused(lambda:parse(seal,"0"*64),"SEAL_PIN")
    variants=[]
    for key,value in (("mathematical_acceptance",True),("profile_sha256","b"*64),
                      ("namespace","7"*64),("index_objects",2)):
        bad=deepcopy(seal);bad[key]=value;variants.append(bad)
    duplicate=deepcopy(seal);duplicate["targets"]*=2;duplicate["index_objects"]=2;variants.append(duplicate)
    extra=deepcopy(seal);extra["arbitrary_path"]="ignored-must-refuse";variants.append(extra)
    for bad in variants:
        refused(lambda bad=bad:parse(bad))
    return seal


def service_failure_control(H,A,O,api,seal,root):
    events=[]; allowance=NS(check=check)
    class Store:
        db=object()
        def status(self): return {"counts":seal["custody_counts"]}
        def close(self): events.append("custody-close");self.db=None
    class Index:
        db=object()
        def status(self): return {"latest":seal["index_snapshot_id"],"objects":1}
        def close(self): events.append("index-close");self.db=None
    O.OrdinaryStore=lambda *a,**kw:Store()
    api._index=lambda *a,**kw:Index()
    async def service(*args,**kwargs):
        async def pending():
            try:
                await asyncio.Event().wait()
            finally:
                def contend():
                    with H._locked(A,root,H._report("serve",root,"a"*64),create=False):
                        raise AssertionError("RUNNER_RELEASED_LOCK_EARLY")
                refused(contend,kinds=(OSError,ValueError))
                events.append("pending-under-lock")
                await asyncio.sleep(0)
                events.append("pending-drained")
        task = asyncio.create_task(pending())
        await asyncio.sleep(0)
        need(not task.done(), "PENDING_TASK_REALLY_ACTIVE")
        raise ValueError("injected SDK cleanup failure")
    api.serve=service
    config=dict(schema=H.SERVE_SCHEMA,host="127.0.0.1",port=0,tls=None,
        lease_seconds=1,cleanup_seconds=10,limits={},share_all_custody=True,exclusive=True)
    def finalize(): check();events.append("finalize")
    with patch.object(H,"_modules",return_value=(A,O,api,None)), \
         patch.object(H,"_root",return_value=root),patch.object(H,"_read_seal",return_value=seal):
        for field in ("share_all_custody","exclusive"):
            bad=dict(config);bad[field]=False
            refused(lambda bad=bad:H.serve(NS(),root,bad,allowance,profile_sha256="a"*64,
                expected_host_sha256="b"*64,finalize=finalize),"DISCLOSURE")
        error=refused(lambda:H.serve(NS(),root,config,allowance,profile_sha256="a"*64,
            expected_host_sha256="b"*64,finalize=finalize),"injected SDK",(H.HostFailure,))
    need(events == ["index-close","finalize","pending-under-lock","pending-drained",
                    "custody-close","finalize"],"RUNNER_DRAIN_BEFORE_CUSTODY_CLOSE")
    need(error.report["host_lock_closure"] == "CLOSED" and
         error.report["custody_closure"] == "CLOSED" and
         error.report["index_closure"] == "NOT_CONFIRMED" and
         error.report["mathematical_acceptance"] is False,"FAILED_SERVICE_HONEST_REPORT")
    with H._locked(A,root,H._report("serve",root,"a"*64),create=False):
        pass


def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--package",required=True);parser.add_argument("--profile-sha256",required=True)
    parser.add_argument("--output",required=True);args=parser.parse_args()
    need(os.name=="nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize,"CONTROL_PYTHON")
    package,output=Path(args.package),Path(args.output)
    need(output.is_absolute() and ".." not in output.parts and output.parent.is_dir() and
         not os.path.lexists(output) and output.resolve().is_relative_to(ROOT/"experiments/v5-local-checks"),
         "CONTROL_OUTPUT")
    profile_raw=read(package/"PROFILE.json",args.profile_sha256);profile=json.loads(profile_raw)
    selected={}
    for key in ("owner","run","custodian"):
        filename=key+".py";pin=profile["files"][filename];path=package/filename
        raw=read(path,pin["sha256"]);need(len(raw)==pin["bytes"],"CONTROL_SOURCE_SIZE")
        selected[key]=(path,raw)
    output.mkdir();cases=[]
    with ExitStack() as stack:
        for target in ("subprocess.Popen","sqlite3.connect","socket.create_connection",
                       "asyncio.open_connection","asyncio.start_server","os.system","os.startfile"):
            stack.enter_context(patch(target,forbidden))
        modules={}
        for key,(path,raw) in selected.items():
            name="_dedicated_control_"+key
            need(name not in sys.modules,"CONTROL_PRELOADED")
            spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec)
            stack.enter_context(patch.dict(sys.modules,{name:module}))
            exec(compile(raw,str(path),"exec"),module.__dict__);modules[key]=module
        owner,launcher,H=(modules[key] for key in ("owner","run","custodian"))
        marked=guard_controls(owner,launcher,output);cases.append("ordinary-and-launcher-path-exclusion")
        producer_control(owner,marked,output);cases.append("producer-output-before-production")
        A,O,api,custody_limits,index_limits=fake_support()
        lock_root=lock_and_close_controls(H,A,output);cases.append("real-two-handle-lock-and-close-refusals")
        seal=seal_controls(H,A,O,api,custody_limits,index_limits,output);cases.append("seal-pin-shape-status-refusals")
        service_failure_control(H,A,O,api,seal,lock_root);cases.append("pending-task-drain-under-lock-on-sdk-failure")
    check()
    for path,raw in selected.values():need(read(path)==raw,"CONTROL_SOURCE_CHANGED")
    need(read(package/"PROFILE.json")==profile_raw,"CONTROL_PROFILE_CHANGED")
    result=dict(status="PASS_DEDICATED_HOST_CONTROLS",groups=len(cases),cases=cases,
        profile_sha256=args.profile_sha256,
        source_pins={key:dict(path=str(path),bytes=len(raw),sha256=digest(raw))
                     for key,(path,raw) in selected.items()},
        wall_seconds=time.monotonic()-START,cpu_seconds=time.process_time()-CPU,
        scope="PACKAGE_PINNED_SOURCE_INERT_SDK_DOUBLES_REAL_WINDOWS_LOCK_NO_MATHEMATICAL_ACCEPTANCE")
    raw=canonical(result)
    with (output/"RESULT.json").open("xb") as stream:stream.write(raw)
    print(raw.decode(),flush=True)


if __name__=="__main__":
    main()

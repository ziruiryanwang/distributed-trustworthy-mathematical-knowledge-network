"""Finite pure symbol-query controls; root selects execution separately.

Uses real inert codecs/query features with synthetic bindings. Lifecycle doubles
have no owner authority. Native, network and database effects are forbidden.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import time
from types import ModuleType, SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU < 25, "CONTROL_ALLOWANCE")


def forbidden(*args, **kwargs):
    raise AssertionError("CONTROL_FORBIDDEN_NATIVE_NETWORK_DATABASE")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, expected=None):
    raw = path.read_bytes()
    need(0 < len(raw) <= 2*MIB, "CONTROL_FILE_BOUND")
    if expected is not None:
        need(digest(raw) == expected, "CONTROL_INPUT_PIN:"+str(path))
    return raw


def refused(call, expected=None):
    try:
        call()
    except ValueError as error:
        if expected is not None:
            need(str(error) == expected, "CONTROL_REFUSAL:"+str(error))
        return
    raise AssertionError("CONTROL_EXPECTED_REFUSAL")


def lifecycle(entry, Q, adapter, destination, names, mapping, missing):
    events = []
    E, S = Q.E, Q.S
    context_id, store_id, implementation = "1"*64, "2"*64, "3"*64
    fake = destination.parent/"inert-nonexistent-state"
    source, limits_path = fake/"names.json", fake/"limits.json"
    catalog, custody_path = fake/"catalog", fake/"custody"
    inputs = {source: E.canonical_json(names), limits_path: b'{"cap":1}',
        catalog/"ADOPTION.json": E.canonical_json({"schema":"INERT", "store_id":store_id,
            "implementation":implementation, "limits":{}})}
    context = dict(local_root=context_id, semantic_id=S.semantic_id(),
        foundation_id=S.foundation_id(), implementation_id=implementation, bindings=mapping)
    def input_read(path, maximum):
        value = inputs[path]; need(len(value) <= maximum, "INERT_READ_BOUND"); return value
    def selected(root):
        need(root == context_id, "INERT_EXACT_CONTEXT"); events.append("context"); return context
    def write(path, value):
        need(events[-2:] == ["owner-close", "custody-close"] or "write" in events,
             "INERT_WRITE_BEFORE_CLOSE")
        need(events.count("owner-close") == events.count("custody-close") == 1,
             "INERT_BOTH_CLOSED")
        need(path.parent == destination, "INERT_OUTPUT_PATH")
        events.append("write")
        with path.open("xb") as stream:
            stream.write(value)
    owner = NS(catalog=NS(context=selected), close=lambda: events.append("owner-close"))
    custody = NS(close=lambda: events.append("custody-close"))
    installation = NS(semantic_id=S.semantic_id(), implementation_id=implementation,
        runtime_roots={}, doc={"implementation":implementation})
    def open_store(*args, **kwargs):
        need(args == (custody_path, S.semantic_id(), {"cap":1}) and kwargs == {"create":False},
             "INERT_STORE_SELECTION"); events.append("custody-open"); return custody
    def open_owner(*args, **kwargs):
        need(args == (installation,catalog,store_id,custody) and kwargs == {"create":False,"limits":{}},
             "INERT_OWNER_SELECTION"); events.append("owner-open"); return owner
    A = NS(E=E,S=S,C=NS(ordinary=lambda path,**kw:path,read_bounded=input_read,hexid=E._hex),
        P=NS(SCHEMA="INERT",fields=lambda *a:None,uint=lambda *a:None,Limits=lambda **kw:kw,
             PortableCatalog=NS(_write_fresh=write)), _writer_json=lambda raw,maximum:json.loads(raw),
        OrdinaryAdmission=NS(open=open_owner))
    O = NS(STORE_LIMITS={"cap":(1,2)},OrdinaryStore=open_store)
    allocation = NS(deadline=START+45,check=check,report=lambda:{"scope":"INERT"})
    loaded = NS(A=A,O=O,formal_query=Q,installation=installation,
        profile=NS(verify=lambda callback:callback()))
    base = NS(Allowance=lambda args:allocation,separated=lambda *a:None,
        bootstrap=lambda *a:NS(load=lambda *a,**kw:loaded))
    args = NS(bindings=None,context_root=context_id,catalog=str(catalog),custody=str(custody_path),
        store_id=store_id,custody_limits=str(limits_path),native_type=None,symbol_names=str(source),
        output=str(destination),profile_sha256="4"*64,python_runtime="INERT",lean_runtime="INERT",
        wall_seconds=35,cpu_seconds=20,memory_mib=256)
    with patch.object(entry,"bootstrap_owner",lambda *a:base):
        result,raw = entry.run(args)
    need(json.loads(raw) == result and result["mathematical_acceptance"] is False,"INERT_REPORT")
    need(result["owner_closure"] == result["custody_closure"] == "CLOSED","INERT_CLOSURE")
    if missing:
        need(not result["ok"] and result["status"] == "UNMAPPED_REFERENCES" and
             result["missing_names"] == missing and not destination.exists(),"INERT_NO_PARTIAL_QUERY")
        need("specs" not in result and "features" not in result,"INERT_NO_READY_SPEC_FIELDS")
        need("write" not in events,"INERT_MISSING_NO_WRITE")
    else:
        need(result["ok"] and result["operation"] == "prepare-symbol-query" and
             result["query_kind"] == "symbol-neighborhood","INERT_SYMBOL_RESULT")
        need((destination/"RESULT.json").read_bytes() == raw,"INERT_SUCCESS_MARKER")
        need(sorted(p.name for p in destination.iterdir()) ==
             ["BINDINGS.json","RESULT.json","SPECS.json","SYMBOL-NAMES.json"],"INERT_OUTPUT_CENSUS")
        rows = json.loads((destination/"BINDINGS.json").read_bytes())
        expected = [{"tag":"type-symbol","symbol":{"kind":"portable-symbol","symbol_id":x[1]}}
                    for x in rows]
        need(result["specs"] == expected and result["features"] ==
             adapter.compile_query(adapter.namespace_for(S.semantic_id()),expected),"INERT_EXACT_FEATURES")
    return {"events":events,"result":result}


def main():
    parser = argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    for option in ("package","profile-sha256","query","query-sha256","output"):
        parser.add_argument("--"+option,required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize,"CONTROL_PROCESS")
    package,entry_path,output = Path(args.package),Path(args.query),Path(args.output)
    need(package.is_absolute() and entry_path.is_absolute() and output.is_absolute() and
         output.parent.is_dir() and not os.path.lexists(output) and
         output.resolve().is_relative_to(ROOT/"experiments/v5-local-checks"),"CONTROL_PATHS")
    profile_raw = read(package/"PROFILE.json",args.profile_sha256)
    profile = json.loads(profile_raw)
    selected = {}
    def source(name,role):
        path = package/role; raw = read(path,profile["files"][role]["sha256"])
        need(len(raw) == profile["files"][role]["bytes"],"CONTROL_SOURCE_SIZE")
        selected[name] = (path,raw)
    installation = json.loads(read(package/"installation/INSTALLATION.json",
                                  profile["installation_manifest_sha256"]))
    for name in ("ordinary_evidence","ordinary_semantics","portable_evidence"):
        role = "py/"+name+".py"; path = package/"installation"/role
        pin = installation["files"][role]; raw = read(path,pin["sha256"])
        need(len(raw) == pin["bytes"],"CONTROL_INSTALL_SOURCE_SIZE"); selected[name]=(path,raw)
    for name in ("ordinary_preview","portable_preview","formal_query"):
        source(name,"authoring/py/"+name+".py")
    for name in ("formal_features","ordinary_export_adapter"):
        source("discovery."+name,"support/discovery/"+name+".py")
    selected["_symbol_query_entry"]=(entry_path,read(entry_path,args.query_sha256))
    need(not any(name in sys.modules for name in selected),"CONTROL_PRELOADED")
    output.mkdir(); cases=[]
    with ExitStack() as stack:
        for target in ("subprocess.Popen","socket.socket","socket.create_connection",
                       "sqlite3.connect","os.system","os.startfile"):
            stack.enter_context(patch(target,forbidden))
        discovery=ModuleType("discovery"); discovery.__path__=[]
        stack.enter_context(patch.dict(sys.modules,{"discovery":discovery}))
        for name,(path,raw) in selected.items():
            spec=importlib.util.spec_from_file_location(name,path); module=importlib.util.module_from_spec(spec)
            stack.enter_context(patch.dict(sys.modules,{name:module}))
            exec(compile(raw,str(path),"exec"),module.__dict__)
            if name.startswith("discovery."):
                setattr(discovery,name.split(".")[1],module)
        Q,entry,adapter=(sys.modules[name] for name in
            ("formal_query","_symbol_query_entry","discovery.ordinary_export_adapter"))
        E=Q.E; name=lambda value:[[0,{"$bytes":list(part.encode())}] for part in value.split(".")]
        names=[name("Example.A"),name("Example.B")]; keys=[E.name_key(x) for x in names]
        mapping={keys[1]:"b"*64,keys[0]:"a"*64,b"irrelevant":"malformed"}
        need(entry.read_symbol_names(Q,E.canonical_json(names)) == names,"VALID_NAMES")
        need(entry.read_symbol_names(Q,E.canonical_json(names[:1])) == names[:1],"ONE_NAME")
        numeric=[[0,{"$bytes":list(b"Example")}],[1,3]]
        distinct=[numeric,name("Example.3")]
        need(entry.read_symbol_names(Q,E.canonical_json(distinct)) == distinct,
             "NUMERIC_AND_STRING_COMPONENTS_DISTINCT")
        eight=[name("Example.N"+str(i)) for i in range(8)]
        need(entry.read_symbol_names(Q,E.canonical_json(eight)) == eight,"EIGHT_NAMES")
        for value in ([],eight+[name("Example.N8")],names+[names[0]],"Example.A",
                      ["Example.A"],[[]],[[[2,0]]],[[[0,{"$bytes":[255]}]]],
                      [name("_kernel_fresh.X")]):
            refused(lambda value=value:entry.read_symbol_names(Q,E.canonical_json(value)))
        for raw in (b" "+E.canonical_json(names),E.canonical_json(names)+b"\n",b"[true]",b"x"*65537):
            refused(lambda raw=raw:entry.read_symbol_names(Q,raw))
        cases.append("names:1..8/order/duplicates/shape/reserved/noncanonical/oversize")
        bound,missing=entry.resolve_names(Q,names,mapping,check)
        need(not missing and json.loads(bound)==[[names[0],"a"*64],[names[1],"b"*64]],"ORDERED_BINDINGS")
        alternative=dict(mapping); alternative[keys[0]]="c"*64
        other,_=entry.resolve_names(Q,names,alternative,check)
        need(json.loads(other)[0][1]=="c"*64 and other!=bound,"EXACT_SELECTED_CONTEXT")
        for subset,absent in (({},names),({keys[0]:"a"*64},names[1:])):
            rows,missing=entry.resolve_names(Q,names,subset,check)
            need(rows is None and missing==absent,"ALL_OR_PARTIAL_MISSING")
        bad=dict(mapping); bad[keys[0]]="bad"
        refused(lambda:entry.resolve_names(Q,names,bad,check),"HASH_ENCODING")
        cases.append("resolution:context-dependent/order/all-and-partial-missing/bad-selected-id")
        native=E.canonical_json([Q.NATIVE_SCHEMA,[],[E.EXPR_FORMAT,[],[[2,names[0],[]]],0]])
        legacy,_=entry.resolve_context_bindings(Q,native,mapping,check)
        direct,_=entry.resolve_names(Q,Q.reference_names(native),mapping,check)
        need(legacy==direct,"OLD_TYPE_PROJECTION")
        Q.read_query(Q.bind_native_type(native,legacy,semantic_id=Q.S.semantic_id()))
        for native_path,symbol_path,bindings,context in ((None,None,"b",None),("n","s",None,"c"),
                                                       (None,"s","b",None)):
            refused(lambda:entry.query_kind(NS(native_type=native_path,symbol_names=symbol_path,
                bindings=bindings,context_root=context,catalog=None,custody=None,store_id=None,custody_limits=None)))
        cases.append("old-type-projection-and-exclusive-input-modes")
        cases.append(lifecycle(entry,Q,adapter,output/"success",names,mapping,[]))
        cases.append(lifecycle(entry,Q,adapter,output/"partial-missing",names,{keys[0]:"a"*64},names[1:]))
    check()
    for path,raw in selected.values():
        need(read(path)==raw,"CONTROL_SOURCE_CHANGED")
    need(read(package/"PROFILE.json")==profile_raw,"CONTROL_PROFILE_CHANGED")
    result={"status":"PASS_SYMBOL_QUERY_PURE_CONTROLS","groups":len(cases),"cases":cases,
        "source_pins":{name:{"path":str(path),"bytes":len(raw),"sha256":digest(raw)}
                       for name,(path,raw) in selected.items()},"profile_sha256":args.profile_sha256,
        "wall_seconds":time.monotonic()-START,"cpu_seconds":time.process_time()-CPU,
        "scope":"REAL_PURE_HELPERS_WITH_INERT_OWNER_DOUBLES_NO_MATHEMATICAL_ACCEPTANCE"}
    raw=E.canonical_json(result)
    with (output/"RESULT.json").open("xb") as stream:
        stream.write(raw)
    print(raw.decode(),flush=True)


if __name__ == "__main__":
    main()

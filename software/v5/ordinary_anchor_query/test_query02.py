"""Changed-boundary anchor-query controls and one separately selected public use.

Control mode uses synthetic authority doubles, not mathematical witnesses, and
forbids native/network/database effects. Public mode invokes the exact companion
once; it reads saved public files only, never owner/catalog/custody APIs.
Execution requires root's separate finite selection and independent review.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack, redirect_stdout
from copy import deepcopy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import time
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
PACKAGE = LOCAL / "exact-module-assembly01/assembled/package"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
OWNER = LOCAL / "concept-recipient-init-01"
CUSTODY_LIMITS = LOCAL / "exact-module-public01/sources/software/v5/concept_episode/CUSTODY-LIMITS.json"
CUSTODY_PIN = "abf5b2dc515a06691194c47e7a320a7fdeaedbbaa18ec45e074807649968ecbe"
PROFILE = "bde63019d1a6ac2bccd8e0c245a405ad3ca551d0606c01a5193fee6897c60346"
INSTALL = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
STORE = "dbaa21256e87cbbf12e1694e183b8d3d25c290af9c73da54395fa4e3923f6b09"
CONTEXT = "03de3aa800949731dfc0823d8661374c9f216262211c9bfe1ac6afd930421e20"
ANCHOR = "79db183e7c154929cb8aca320082854ddde304466a3dd901da071aac425f9325"
MODULE = "DMKNBridge_1a3b16fc61d27a93a3187cc140d70cdc05c59b24816cf114bc4f3a1e93fac1cf"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
FOUNDATION = "884f408f0e7d647a1b72714cfa78685804dea9e07289a67176692cfbfe2c8282"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
KEY_PROFILE = "09fceff93c77a65852e6509db9badfb3330d20737aea5297bd031f8b8845a953"
NAMESPACE = "d966de54aa32c6cd059ab9553a0968a320594a63561cadf742cca6265858079c"
FEATURES = ["941dc31cba88a2758910984aad0f044cb074b6614b8b78494a46524c150356ca"]
PREVIOUS = LOCAL / "received-query01/query"
COLD_REPORT = LOCAL / "exact-module-public01/public/cold-stdout.json"
COLD_REPORT_PIN = "0806e4720a5305d7665b2a006a840b5f32fe3134aeddbd61c9803507915f8c5a"
PREVIOUS_PINS = {
    "native/type.json": "333415560e87565ec9a774baaa317ff9e96d0773530da341391b174a9c91c915",
    "query/BINDINGS.json": "e93217483f53b1d78bef162e41f56be4c704dfae755930ee2e823ca8245e21dc",
    "query/QUERY.json": "083a2e8f588345dcd1a1b371f3f2edfa684e2f6094564e7bea9a0b56363ebbd3",
    "query/SPECS.json": "689c10b92a751b3f217838c02d6a800a1ff86e1343426dd76985380aa632479d",
}
MIB = 1024**2
LIMITS = dict(wall_seconds=60, cpu_seconds=30, memory_mib=1024,
              active_processes=4, stdout_bytes=MIB, stderr_bytes=MIB)
START, CPU = time.monotonic(), time.process_time()


def need(ok, message):
    if not ok:
        raise AssertionError("ANCHOR_TEST_" + message)


def check():
    need(time.monotonic()-START < 110 and time.process_time()-CPU < 35, "ORIGINAL_ALLOWANCE")


def raw(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path, maximum=4*MIB):
    check()
    with Path(path).open("rb") as stream:
        result = stream.read(maximum+1)
    need(0 < len(result) <= maximum, "READ_BOUND")
    return result


def save(path, value):
    data = value if type(value) is bytes else raw(value)
    need(0 < len(data) <= 4*MIB, "WRITE_BOUND")
    with Path(path).open("xb") as stream:
        stream.write(data)
    return dict(bytes=len(data), sha256=sha(data))


def forbidden(*_args, **_kwargs):
    raise AssertionError("ANCHOR_TEST_FORBIDDEN_NATIVE_NETWORK_DATABASE")


def forbid_effects(stack, *, native=True):
    targets = ["sqlite3.connect", "socket.socket", "socket.create_connection", "os.system"]
    if native:
        targets += ["subprocess.Popen", "subprocess.run", "subprocess.call",
                    "subprocess.check_call", "subprocess.check_output"]
    for target in targets:
        stack.enter_context(patch(target, side_effect=forbidden))


def load_subject(path, pin):
    data = read(path)
    need(sha(data) == pin, "SOURCE_PIN")
    label = "_anchor_query_changed_boundary_subject"
    need(label not in sys.modules, "PRELOADED_SUBJECT")
    spec = importlib.util.spec_from_file_location(label, path)
    subject = importlib.util.module_from_spec(spec)
    sys.modules[label] = subject
    exec(compile(data, str(path), "exec"), subject.__dict__)
    return subject


def refuses(call, label, expected):
    check()
    try:
        call()
    except (ValueError, KeyError, TypeError, OSError) as error:
        need(expected in str(error), "WRONG_REFUSAL:" + label + ":" + str(error))
        return dict(case=label, error_type=type(error).__name__, error=str(error)[:500])
    raise AssertionError("ANCHOR_TEST_UNEXPECTED_ACCEPTANCE:" + label)


def name(text):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in text.split(".")]


def config_document(query, query_sha):
    return dict(schema="DMKN_ORDINARY_ANCHOR_QUERY_V1", package=str(PACKAGE),
        profile_sha256=PROFILE, python_runtime=str(PYTHON), lean_runtime=str(LEAN),
        query=dict(path=str(query), sha256=query_sha), limits=deepcopy(LIMITS),
        owner=dict(catalog=str(OWNER/"catalog"), custody=str(OWNER/"custody"), store_id=STORE,
                   context_root=CONTEXT, anchor_id=ANCHOR,
                   custody_limits=dict(path=str(CUSTODY_LIMITS), sha256=CUSTODY_PIN)))


def config_controls(subject, base):
    good = config_document(base/"synthetic-question.json", "1"*64)
    need(subject.validate_config(good) == good, "EXACT_CONFIG")
    variants = []
    for key in good["owner"]:
        changed = deepcopy(good); del changed["owner"][key]
        variants.append(("missing-owner:"+key, changed, "OWNER_FIELDS"))
    for key in ("context_root", "anchor_id", "store_id"):
        changed = deepcopy(good); changed["owner"][key] = "not-a-hash"
        variants.append(("wrong-owner-id:"+key, changed, "HASH"))
    for key in ("project", "imports", "bindings", "anchor_plan"):
        changed = deepcopy(good); changed["owner"][key] = []
        variants.append(("extra-owner:"+key, changed, "OWNER_FIELDS"))
    changed = deepcopy(good); changed["schema"] = "DMKN_ORDINARY_BASIS_QUERY_V1"
    variants.append(("old-config", changed, "CONFIG_FIELDS"))
    changed = deepcopy(good); changed["imports"] = []
    variants.append(("caller-import-paths", changed, "CONFIG_FIELDS"))
    changed = deepcopy(good); changed["owner"]["custody_limits"]["sha256"] = "invalid"
    variants.append(("limits-pin", changed, "HASH"))
    output = base/"never-created-native.json"
    source = subject.source_text(("u",), "forall {T : Type u}, T -> T", output, MODULE)
    need(("public import "+MODULE+"\n").encode() in source and
         source.count(b"public import Init\n") == 1 and
         source.count(b"public meta import OwnerQueryCommand\n") == 1 and
         b"forall {T : Type u}, T -> T" in source, "SELECTED_IMPORT_WRAPPER")
    results = [refuses(lambda doc=doc: subject.validate_config(doc), label, error)
               for label, doc, error in variants]
    results.append(refuses(lambda:subject.source_text((), "Nat", output, "Foreign\nimport X"),
                           "unselected-module-name", "MODULE_NAME"))
    return dict(group="new_config_and_selected_import", refusals=results, synthetic=True)


def synthetic_semantics():
    """Only a deterministic routing fixture; none of its IDs warrant mathematics."""
    E = SimpleNamespace(name_key=lambda value:raw(value).decode("ascii"), canonical_json=raw,
        strict_json=lambda data, _limits=None:json.loads(data), Limits=lambda **kw:SimpleNamespace(**kw))
    inventory = [[name("Basis"+str(i))] for i in range(581)]
    inventory_raw = raw(inventory)
    S = SimpleNamespace(INVENTORY=sha(inventory_raw), semantic_id=lambda:"a"*64,
        foundation_id=lambda:"b"*64,
        basis_symbol_id=lambda semantic, foundation, value:sha(raw(["SYNTHETIC_BASIS",semantic,foundation,value])),
        export_id=lambda semantic, unit, value:sha(raw(["SYNTHETIC_EXPORT",semantic,unit,value])))
    Q = SimpleNamespace(E=E, S=S, reference_names=lambda data:json.loads(data)["synthetic_references"])
    context = {E.name_key(row[0]):S.basis_symbol_id(S.semantic_id(), S.foundation_id(), row[0])
               for row in inventory}
    units = []
    for identity, names in (("c"*64, ["Earlier.Dependency"]),
                            ("d"*64, ["Current.Target", "Current.Nontarget"])):
        outputs = []
        for label in names:
            value = name(label); symbol = S.export_id(S.semantic_id(), identity, value)
            context[E.name_key(value)] = symbol
            outputs.append(dict(name=value, export_id=symbol, kind="def", level_params=[], inventory_sha256="e"*64))
        units.append(dict(unit_id=identity, outputs=outputs, realization={"synthetic":True}))
    plan = dict(schema="DMKN_LOCAL_MODULE_ANCHOR_PLAN_V1", anchor_id="f"*64,
                support_id="1"*64, modules=["synthetic-earlier", "synthetic-top"], bindings=units)
    refs = list(map(name, ("Current.Nontarget", "Basis2", "Earlier.Dependency", "Current.Target")))
    return Q, S, inventory_raw, plan, context, refs


def binding_controls(subject):
    Q, S, inventory, plan, context, refs = synthetic_semantics()
    native = raw(dict(synthetic_references=refs))
    def bind(p=plan, c=context, n=native, inv=inventory):
        return subject.realized_bindings(Q,S,n,inv,S.semantic_id(),raw(p),c,check)
    actual = bind()
    need(actual == raw([[value, context[Q.E.name_key(value)]] for value in refs]),
         "FULL_CHAIN_ORDER_AND_NONTARGET_BINDING")
    cases = []
    changed = deepcopy(context); changed[Q.E.name_key(name("Context.Only"))] = "2"*64
    cases.append(refuses(lambda:bind(c=changed,n=raw(dict(synthetic_references=[name("Context.Only")]))),
                         "context-only-not-imported", "UNKNOWN_VOCABULARY"))
    for label, value in (("basis-context-id",name("Basis2")), ("realized-context-id",name("Earlier.Dependency"))):
        changed = deepcopy(context); changed[Q.E.name_key(value)] = "0"*64
        expected = "REFERENCE_CONTEXT_BINDING" if label.startswith("basis") else "REALIZED_EXPORT_BINDING"
        cases.append(refuses(lambda c=changed:bind(c=c),label,expected))
    for label, mutate in (
        ("wrong-export-id",lambda p:p["bindings"][0]["outputs"][0].update(export_id="0"*64)),
        ("duplicate-export",lambda p:p["bindings"].append(deepcopy(p["bindings"][0]))),
        ("basis-overlap",lambda p:p["bindings"][0]["outputs"][0].update(name=name("Basis2"))),
    ):
        changed = deepcopy(plan); mutate(changed)
        cases.append(refuses(lambda p=changed:bind(p=p),label,"REALIZED_EXPORT_BINDING"))
    changed = deepcopy(context); del changed[Q.E.name_key(name("Current.Target"))]
    cases.append(refuses(lambda:bind(c=changed),"missing-realized-context","REALIZED_EXPORT_BINDING"))
    changed = deepcopy(plan); changed["bindings"] = []
    cases.append(refuses(lambda:bind(p=changed),"empty-realization","PLAN_BINDINGS"))
    changed = deepcopy(plan); changed["unselected"] = True
    cases.append(refuses(lambda:bind(p=changed),"extra-plan-field","PLAN_FIELDS"))
    cases.append(refuses(lambda:bind(inv=inventory+b" "),"inventory-pin","INVENTORY_PIN"))
    return dict(group="complete_realized_vocabulary", positive_references=4,
                earlier_chain_dependency=True, nontarget_export=True, refusals=cases, synthetic=True)


def selection_controls(subject, base):
    calls = []
    context = dict(local_root=CONTEXT,semantic_id=SEMANTIC,foundation_id=FOUNDATION,
                   implementation_id=IMPLEMENTATION,bindings={})
    installation = SimpleNamespace(semantic_id=SEMANTIC,implementation_id=IMPLEMENTATION)
    selected_context = [context]
    owner = SimpleNamespace(catalog=SimpleNamespace(context=lambda root:selected_context[0]))
    need(subject.checked_context(owner,installation,CONTEXT,FOUNDATION) is context,"CONTEXT_SELECTION")
    cases = []
    for key in ("local_root","semantic_id","foundation_id","implementation_id"):
        selected_context[0] = dict(context,**{key:"0"*64})
        cases.append(refuses(lambda:subject.checked_context(owner,installation,CONTEXT,FOUNDATION),
                             "wrong-context:"+key,"CONTEXT_IDENTITY"))
    selected_context[0] = context
    catalog = base/"synthetic-catalog"; catalog.mkdir()
    sidecar = catalog/"module-anchors-v1"
    def ordinary(path, *, directory):
        calls.append(("ordinary",str(path)))
        need(path == sidecar and directory is True,"PREEXISTING_SIDECAR_SELECTION")
        if not path.is_dir(): raise ValueError("SYNTHETIC_SIDECAR_MISSING")
        return path
    A = SimpleNamespace(C=SimpleNamespace(ordinary=ordinary))
    support = {"synthetic_support":True}
    view = dict(anchor_id=ANCHOR,module_name=MODULE,plan_raw=b"synthetic-plan",records=("record",),
                import_directories=(base/"imports",),artifact_bytes={"x":1})
    fault = [None]
    def load(anchor, current, checked):
        checked(); calls.append(("load",anchor))
        need(anchor == ANCHOR and current is context,"EXACT_ANCHOR_CONTEXT")
        if fault[0]: raise ValueError(fault[0])
        return deepcopy(view)
    store = SimpleNamespace(load=load)
    def open_for_owner(actual_owner, actual_support, checked):
        checked(); calls.append(("open",None))
        need(actual_owner is owner and actual_support is support,"EXACT_OWNER_SUPPORT")
        return store
    def support_descriptor(inst,profile,source,worker):
        calls.append(("support",None))
        need(inst is installation and profile is loaded.profile and source==loaded.root/"module/OrdinaryModule.lean"
             and worker==loaded.root/"module_worker.py","UNCHANGED_SUPPORT_DERIVATION")
        return support
    M = SimpleNamespace(A=A,K=SimpleNamespace(A=A,open_for_owner=open_for_owner),support_descriptor=support_descriptor)
    loaded = SimpleNamespace(A=A,module_export=M,installation=installation,profile=object(),root=base/"package")
    cases.append(refuses(lambda:subject.registered_view(loaded,owner,catalog,context,ANCHOR,check),
                         "missing-sidecar-before-open","SYNTHETIC_SIDECAR_MISSING"))
    need(calls == [("ordinary",str(sidecar))] and not sidecar.exists(),"NO_SIDECAR_CREATION")
    calls.clear(); sidecar.mkdir()
    got_store,got_view = subject.registered_view(loaded,owner,catalog,context,ANCHOR,check)
    need(got_store is store and got_view==view and [x[0] for x in calls]==["ordinary","support","open","load"],
         "REGISTERED_CHAIN_PATH")
    for refusal in ("SYNTHETIC_MISSING_ANCHOR", "SYNTHETIC_SUPPORT_MISMATCH", "SYNTHETIC_ARTIFACT_CHANGED"):
        fault[0] = refusal
        cases.append(refuses(lambda:subject.registered_view(loaded,owner,catalog,context,ANCHOR,check),refusal,refusal))
    fault[0] = None
    subject.unchanged_view(store,ANCHOR,context,deepcopy(view),check)
    for key in view:
        changed = deepcopy(view); changed[key] = ("CHANGED",key)
        cases.append(refuses(lambda v=changed:subject.unchanged_view(store,ANCHOR,context,v,check),
                             "reloaded-view:"+key,"ANCHOR_CHANGED"))
    fault[0] = "SYNTHETIC_RECHECK_ARTIFACT_CHANGED"
    cases.append(refuses(lambda:subject.unchanged_view(store,ANCHOR,context,view,check),
                         "recheck-artifact-refusal",fault[0]))
    return dict(group="context_support_sidecar_and_revalidation",refusals=cases,synthetic=True)


def close_controls(subject):
    cases=[]
    for failures in ((),("owner",),("custody",),("owner","custody")):
        events=[]
        def handle(label):
            def close():
                events.append(label)
                if label in failures: raise OSError("SYNTHETIC_CLOSE_"+label)
            return SimpleNamespace(close=close)
        result=subject.close_handles(handle("owner"),handle("custody"))
        need(events==["owner","custody"] and [item["component"] for item in result]==list(failures),
             "BOTH_HANDLES_CLOSE_EVEN_AFTER_ERROR")
        cases.append(dict(failures=list(failures),returned_errors=result))
    need(subject.close_handles(None,None)==[],"ABSENT_HANDLES_CLOSE")
    return dict(group="both_handle_close_attempts",cases=cases,synthetic=True)


def setup_order_controls(subject,base):
    """Real setup/parent order with synthetic bootstrap I/O and no owner opening."""
    cases=[]
    for variant in ("catalog-sidecar-output","custody-output","limits-in-output","catalog-path-separator"):
        work=base/("setup-"+variant); work.mkdir()
        catalog=work/("catalog;unselected" if variant=="catalog-path-separator" else "catalog")
        custody=work/"custody"
        catalog.mkdir(); custody.mkdir()
        output=(catalog/"module-anchors-v1" if variant=="catalog-sidecar-output" else
                custody/"query" if variant=="custody-output" else work/"candidate")
        limits_path=output/"limits.json" if variant=="limits-in-output" else work/"limits.json"
        query_path=work/"question.json"; config_path=work/"config.json"
        query_raw=raw(dict(universes=[],type="Nat")); limits_raw=b'{"objects":1}'
        doc=config_document(query_path,sha(query_raw))
        doc["owner"].update(catalog=str(catalog),custody=str(custody),
            custody_limits=dict(path=str(limits_path),sha256=sha(limits_raw)))
        config_raw=raw(doc); entry=Path(subject.__file__).absolute()
        contents={config_path:config_raw,query_path:query_raw,limits_path:limits_raw,
                  entry:b"SYNTHETIC_ENTRY",PACKAGE/"run.py":b"SYNTHETIC_LAUNCHER"}
        events=[]
        def overlap(a,b):
            a,b=Path(a),Path(b)
            return a==b or a in b.parents or b in a.parents
        def separated(paths,label):
            events.append("separated")
            need(output in paths and catalog in paths and custody in paths,"ALL_STATE_PATHS_SEPARATED")
            for index,left in enumerate(paths):
                for right in paths[index+1:]:
                    if overlap(left,right): raise ValueError(label)
        R=SimpleNamespace(ordinary=lambda p,**kw:Path(p),read=lambda p,m,c:contents[Path(p)],
            separated=separated,overlap=overlap,bind_support=forbidden,load_supervision=forbidden)
        args=SimpleNamespace(config=str(config_path),config_sha256=sha(config_raw),output=str(output),
            approve_local_query=True,worker=False,origin=None,deadline=None,entry_sha256=None)
        printed=io.StringIO()
        with patch.object(subject,"initial_read",side_effect=lambda p,m:contents[Path(p)]),\
             patch.object(subject,"RUN_SHA",sha(b"SYNTHETIC_LAUNCHER")),\
             patch.object(subject,"load_source",return_value=R),redirect_stdout(printed):
            code=subject.parent(args)
        result=json.loads(printed.getvalue())
        expected=("SEARCH_PATH_SEPARATOR" if variant=="catalog-path-separator" else
                  "OUTPUT_INPUT_OVERLAP" if variant=="limits-in-output" else "ANCHOR_QUERY_PATH_OVERLAP")
        expected_events=[] if variant=="catalog-path-separator" else ["separated"]
        need(code==1 and result["ok"] is False and expected in result["error"] and
             events==expected_events and not output.exists(),"SETUP_BEFORE_OUTPUT_CREATION")
        cases.append(dict(case=variant,error=result["error"],output_created=False))
    return dict(group="setup_separation_precedes_parent_mkdir",cases=cases,synthetic=True)


def worker_controls(subject,base):
    """Real worker lifecycle; only native dispatch/owner authority are synthetic."""
    cases=[]
    for variant in ("ready","anchor-changed","context-changed","artifact-refused","owner-close-failed"):
        work=base/("worker-"+variant); work.mkdir()
        output=work/"candidate"; output.mkdir()
        catalog=work/"catalog"; catalog.mkdir(); (catalog/"module-anchors-v1").mkdir()
        Q,S,inventory,plan,bindings,refs=synthetic_semantics()
        Q.PROFILE_ID="2"*64
        Q.bind_native_type=lambda native,mapping,**kw:raw(dict(synthetic_native=json.loads(native),bindings=json.loads(mapping)))
        Q.query_spec=lambda query:dict(tag="synthetic-not-mathematical",value=sha(query))
        native_raw=raw(dict(synthetic_references=refs)); plan["anchor_id"]=ANCHOR
        events=[]; load_count=[0]; context_count=[0]
        state={"owner_closed":False,"custody_closed":False,"owner_open":False}
        context=dict(local_root=CONTEXT,semantic_id=S.semantic_id(),foundation_id=S.foundation_id(),
                     implementation_id=IMPLEMENTATION,bindings=bindings)
        def get_context(root):
            need(state["owner_open"] and not state["owner_closed"] and root==CONTEXT,"LIVE_OWNER_CONTEXT")
            context_count[0]+=1; events.append("context")
            return dict(context,local_root="0"*64) if variant=="context-changed" and context_count[0]>1 else context
        def close_owner():
            events.append("owner-close")
            if variant=="owner-close-failed": raise OSError("SYNTHETIC_OWNER_CLOSE_FAILED")
            state["owner_closed"]=True
        def close_custody():
            events.append("custody-close"); state["custody_closed"]=True
        owner=SimpleNamespace(catalog=SimpleNamespace(context=get_context),close=close_owner)
        custody=SimpleNamespace(close=close_custody)
        def open_owner(installation,path,store_id,received,**kw):
            need(not state["owner_open"] and path==catalog and store_id==STORE and received is custody and
                 kw["create"] is False,"ONE_SELECTED_OWNER_OPEN")
            state["owner_open"]=True; events.append("owner-open"); return owner
        def open_custody(path,semantic,limits,**kw):
            need(path==work/"custody" and semantic==S.semantic_id() and kw["create"] is False,"CUSTODY_OPEN")
            events.append("custody-open"); return custody
        implementation={"synthetic_implementation":True}
        installation=SimpleNamespace(semantic_id=S.semantic_id(),implementation_id=IMPLEMENTATION,
            doc=dict(implementation=implementation),path=lambda role:LEAN/"bin/lean.exe",
            read=lambda role,maximum:inventory)
        marker=dict(schema="SYNTHETIC_ADOPTION",store_id=STORE,implementation=implementation,limits={})
        def fields(doc,expected,label):
            need(set(doc)==set(expected),"SYNTHETIC_FIELDS:"+label)
        A=SimpleNamespace(S=S,E=Q.E,_writer_json=lambda data,maximum:json.loads(data),
            C=SimpleNamespace(ordinary=lambda p,**kw:Path(p),read_bounded=lambda p,m:raw(marker)),
            P=SimpleNamespace(fields=fields,uint=lambda *a:None,SCHEMA="SYNTHETIC_ADOPTION",Limits=lambda **kw:kw),
            OrdinaryAdmission=SimpleNamespace(open=open_owner))
        O=SimpleNamespace(STORE_LIMITS={"objects":(1,100)},OrdinaryStore=open_custody)
        view=SimpleNamespace(anchor_id=ANCHOR,module_name=MODULE,support_id="1"*64,plan_raw=raw(plan),
            records=(b"SYNTHETIC_RECORD",),artifact_bytes={"SYNTHETIC":1},store_binding={"synthetic":True},
            import_directories=(work/"module-imports",))
        def load(anchor,current,checked):
            checked(); need(state["owner_open"] and not state["owner_closed"],"LOAD_UNDER_OWNER_LOCK")
            need(anchor==ANCHOR and current is context,"LOAD_SELECTED_CONTEXT")
            load_count[0]+=1; events.append("anchor-load")
            if load_count[0]>1 and variant=="artifact-refused": raise ValueError("SYNTHETIC_ARTIFACT_CHANGED")
            if load_count[0]>1 and variant=="anchor-changed":
                changed=deepcopy(view); changed.plan_raw=b"SYNTHETIC_CHANGED_PLAN"; return changed
            return deepcopy(view)
        store=SimpleNamespace(load=load)
        module=SimpleNamespace(A=A,K=SimpleNamespace(A=A,open_for_owner=lambda *a:store,
                                                    parse=lambda data,maximum:json.loads(data)),
                               support_descriptor=lambda *a:{"synthetic":True})
        profile=SimpleNamespace(helper_paths=(work/"helpers",),verify=lambda checked:checked())
        loaded=SimpleNamespace(A=A,O=O,formal_query=Q,installation=installation,module_export=module,
                               profile=profile,root=work/"package")
        loader=SimpleNamespace(load=lambda *a,**kw:loaded)
        entry_module=SimpleNamespace(bootstrap=lambda *a:loader)
        config_path=work/"config.json"; query_path=work/"question.json"; limits_path=work/"limits.json"
        config=config_document(query_path,"3"*64); config["owner"].update(catalog=str(catalog),custody=str(work/"custody"))
        for path in (config_path,query_path,limits_path): save(path,b"SYNTHETIC_INPUT")
        input_map={config_path:read(config_path),query_path:read(query_path),limits_path:read(limits_path),
                   Path(subject.__file__):read(subject.__file__)}
        def selected_read(path,maximum,checked):
            checked(); path=Path(path)
            if path==PACKAGE/"PROFILE.json": return raw(dict(files={"owner.py":{"synthetic":True}}))
            return input_map[path] if path in input_map else read(path,maximum)
        R=SimpleNamespace(strict=json.loads,read=selected_read,bound_file=lambda *a,**kw:b"SYNTHETIC_OWNER",
            load_source=lambda *a:entry_module,ordinary=lambda p,**kw:Path(p))
        s=SimpleNamespace(R=R,package=PACKAGE,config=config,config_path=config_path,config_raw=input_map[config_path],
            query_path=query_path,query_raw=input_map[query_path],custody_limits_path=limits_path,
            custody_limits_raw=b'{"objects":1}',catalog=catalog,custody=work/"custody",python=PYTHON,lean=LEAN,
            entry=Path(subject.__file__),entry_raw=input_map[Path(subject.__file__)],output=output,
            bound=dict(installation_manifest_sha256=INSTALL),deadline=subject.START+60,check=check,
            universes=("u",),term="forall {T : Type u}, T -> T")
        input_map[limits_path]=s.custody_limits_raw
        def native_call(argv,**kw):
            need(state["owner_open"] and not state["owner_closed"] and not state["custody_closed"],"NATIVE_UNDER_LOCK")
            expected_paths=(*profile.helper_paths,LEAN/"lib/lean",*view.import_directories)
            need(kw["env"]["LEAN_PATH"]==os.pathsep.join("\\\\?\\"+str(p) for p in expected_paths) and
                 argv==[str(LEAN/"bin/lean.exe"),"-j","1","-DElab.async=false","-R",str(output/"native"),
                        str(output/"native/Query.lean")],"EXACT_NATIVE_CHAIN_IMPORTS")
            events.append("native"); save(output/"native/type.json",native_raw); return 0
        original_save=subject.save_bytes
        def tracked_save(path,data,maximum=MIB):
            if Path(path).name in {"BINDINGS.json","QUERY.json","SPECS.json","ANCHOR.json"}:
                need(state["owner_closed"] and state["custody_closed"],"NO_HINT_BEFORE_CLOSE")
                events.append("publish:"+Path(path).name)
            if Path(path).name=="WORKER.json":
                need("owner-close" in events and "custody-close" in events,"WORKER_REPORT_AFTER_BOTH_CLOSE_ATTEMPTS")
            return original_save(path,data,maximum)
        adapter=SimpleNamespace(Q=Q,namespace_for=lambda semantic:"synthetic",compile_query=lambda *a:["synthetic"])
        printed=io.StringIO()
        args=SimpleNamespace(config_sha256=sha(s.config_raw))
        with patch.object(subject,"setup",return_value=s),patch.object(subject.subprocess,"call",side_effect=native_call),\
             patch.object(subject,"save_bytes",side_effect=tracked_save),\
             patch.dict(sys.modules,{"discovery.ordinary_export_adapter":adapter}),redirect_stdout(printed):
            code=subject.worker(args)
        result=json.loads(printed.getvalue()); save(work/"captured-stdout.json",printed.getvalue().encode())
        need(events.count("native")==1 and events.count("owner-open")==1 and
             events.count("owner-close")==1 and events.count("custody-close")==1,"SINGLE_LIFECYCLE")
        if variant=="ready":
            need(code==0 and result["ok"] is True and result["owner_handles_closed"] is True and
                 load_count[0]==2 and context_count[0]==2 and
                 events.index("custody-close")<events.index("publish:BINDINGS.json"),"SUCCESS_AFTER_RECHECK_AND_CLOSE")
        else:
            need(code==1 and result["ok"] is False and
                 all(not (output/name).exists() for name in ("BINDINGS.json","QUERY.json","SPECS.json","ANCHOR.json")),
                 "NO_HINT_AFTER_RECHECK_OR_CLOSE_FAILURE")
            expected={"anchor-changed":"ANCHOR_CHANGED","context-changed":"CONTEXT_IDENTITY",
                      "artifact-refused":"SYNTHETIC_ARTIFACT_CHANGED","owner-close-failed":"FAILED_OWNER_CLOSURE"}[variant]
            need(expected in str(result),"EXPECTED_LIFECYCLE_REFUSAL")
        need(json.loads(read(output/"WORKER.json"))==result,"WORKER_STDOUT_AGREEMENT")
        cases.append(dict(case=variant,exit_code=code,events=events,owner_handles_closed=result["owner_handles_closed"]))
    return dict(group="worker_live_lock_recheck_and_closed_publication",cases=cases,synthetic=True,native_processes=0)


def metered(limits):
    return dict(status="COMMAND_EXITED_ZERO_AND_CLOSED",child_exit_code=0,direct_child_reaped=True,
        job_closed=True,cleanup_errors=[],termination_requested=False,
        final_job=dict(active_processes=0,terminated_processes=0,cpu_seconds=0.25),
        limits=deepcopy(limits),wall_seconds_through_cleanup=0.5,wrapper_supervision_cpu_seconds=0.1,
        observed_logs=dict(stdout_bytes=0,stderr_bytes=0))


def fake_read(path, maximum, checked):
    checked(); return read(path,maximum)


def parent_controls(subject,base):
    """One new-parent happy path and failed-supervisor guard; no real worker."""
    cases=[]
    for variant in ("ready","unclean","handles-open","owner-changed","candidate-changed","pending-write"):
        work=base/("parent-"+variant); work.mkdir()
        config,query,entry,limits_file=(work/x for x in ("config.json","query.json","entry.py","limits.json"))
        for path in (config,query,entry,limits_file): save(path,b"SYNTHETIC_NOT_PRODUCT_INPUT")
        config_doc=config_document(query,sha(read(query)))
        s=SimpleNamespace(config_path=config,config_raw=read(config),query_path=query,query_raw=read(query),
            entry=entry,entry_raw=read(entry),custody_limits_path=limits_file,custody_limits_raw=read(limits_file),
            output=work/"candidate",python=PYTHON,lean=LEAN,package=PACKAGE,check=check,config=config_doc,
            bound=dict(installation_manifest_sha256=INSTALL),limits=deepcopy(LIMITS),
            origin=subject.START,deadline=subject.START+LIMITS["wall_seconds"])
        args=SimpleNamespace(config=str(config),config_sha256=sha(s.config_raw),output=str(s.output),
            approve_local_query=True,worker=False,origin=None,deadline=None,entry_sha256=None)
        environment=lambda cwd:{"SYNTHETIC":True}
        supervisor=SimpleNamespace(child_environment=environment)
        s.R=SimpleNamespace(read=fake_read,ordinary=lambda path,**kw:Path(path),
            bind_support=lambda *a:s.bound,load_supervision=lambda bound:(supervisor,None))
        calls=[]
        def supervise(argv,cwd,evidence,limits,job,*,started):
            need(not calls and started==s.origin and limits==dict(LIMITS,wall_seconds=55) and
                 argv[:5]==[str(PYTHON/"python.exe"),"-I","-S","-B",str(entry)] and
                 argv[argv.index("--deadline")+1]==repr(s.deadline-5),"FIXED_PARENT_WORKER_ALLOWANCE")
            calls.append(argv); (s.output/"native").mkdir()
            for filename in sorted(subject.OUTPUTS): save(s.output/filename,("SYNTHETIC:"+filename).encode())
            files=subject.candidate_pins(s)
            worker=dict(schema="DMKN_ORDINARY_ANCHOR_QUERY_WORKER_V1",ok=True,
                status="CANDIDATE_HINTS_NOT_SUPERVISED_SUCCESS",supervised_completion=False,
                mathematical_acceptance=False,native_exit_code=0,files=files,
                config_sha256=args.config_sha256,profile_sha256=PROFILE,entry_sha256=sha(s.entry_raw),
                query_sha256=sha(s.query_raw),installation_manifest_sha256=INSTALL,
                owner_handles_closed=True,
                interpretation=dict(vocabulary="FIXED_BASIS_AND_REGISTERED_CHAIN",store_id=STORE,
                    context_root=CONTEXT,anchor_id=ANCHOR,semantic_id="1"*64,foundation_id="2"*64,
                    implementation_id="3"*64,inventory_sha256="4"*64,key_profile="5"*64,
                    support_id="6"*64,plan_sha256="7"*64),namespace="synthetic",features=["synthetic"])
            if variant=="handles-open": worker["owner_handles_closed"]=False
            if variant=="owner-changed": worker["interpretation"]["anchor_id"]="0"*64
            if variant=="candidate-changed": worker["files"]["ANCHOR.json"]["sha256"]="0"*64
            save(s.output/"WORKER.json",worker)
            evidence.mkdir()
            save(evidence/"command.json",dict(synthetic=True))
            for label in ("stdout.txt","stderr.txt"):
                with (evidence/label).open("xb"): pass
            report=metered(limits)
            if variant=="unclean": report["direct_child_reaped"]=False
            return report
        supervisor.supervise=supervise
        original_save=subject.save_bytes
        def save_candidate(path,data,maximum=MIB):
            if variant=="pending-write" and Path(path).name=="RESULT.pending.json":
                raise OSError("SYNTHETIC_PENDING_FAILURE")
            return original_save(path,data,maximum)
        printed=io.StringIO()
        with patch.object(subject,"setup",return_value=s),patch.object(subject,"save_bytes",side_effect=save_candidate),redirect_stdout(printed):
            code=subject.parent(args)
        result=json.loads(printed.getvalue())
        save(work/"captured-stdout.json",printed.getvalue().encode())
        need(len(calls)==1 and supervisor.child_environment is environment,"SINGLE_PARENT_WORKER")
        marker=s.output/"RESULT.json"
        if variant=="ready":
            need(code==0 and result["ok"] is True and result["status"]=="ANCHOR_QUERY_READY" and
                 json.loads(read(marker))==result,"PARENT_READY")
        elif variant=="pending-write":
            need(code==1 and result["ok"] is False and result["status"]=="RESULT_WRITE_FAILED" and
                 not marker.exists(),"NO_SUCCESS_AFTER_PENDING_FAILURE")
        else:
            expected={"unclean":"WORKER_NOT_CLEANLY_COMPLETE","handles-open":"WORKER_BINDING",
                      "owner-changed":"WORKER_OWNER_SELECTION","candidate-changed":"CANDIDATE_CHANGED"}[variant]
            need(code==1 and result["ok"] is False and expected in result["error"] and
                 json.loads(read(marker))["ok"] is False,"PARENT_REJECTS_SYNTHETIC_SUCCESS")
        cases.append(dict(case=variant,exit_code=code,status=result["status"]))
    return dict(group="parent_closure_before_public_success",cases=cases,synthetic=True)


def ignore_forall_display_names(native):
    """Fixture comparator only: preserve every mathematical/reference field."""
    value=deepcopy(native)
    need(type(value) is list and len(value)==3 and value[0]=="DMKN_ORDINARY_LEAN_QUERY_TYPE_AST_V1",
         "PUBLIC_NATIVE_ENVELOPE")
    expr=value[2]
    need(type(expr) is list and len(expr)==4 and expr[0]=="DMKN_LEAN_ORIGINAL_EXPR_V1",
         "PUBLIC_NATIVE_EXPR")
    for node in expr[2]:
        if node[0]==5:
            need(len(node)==5,"PUBLIC_FORALL_SHAPE")
            node[1]=["DISPLAY_NAME_IGNORED_ONLY"]
    return value


def public_check(subject,args,base):
    previous={}
    for relative,pin in PREVIOUS_PINS.items():
        previous[relative]=subject.initial_read(PREVIOUS/relative,MIB)
        need(sha(previous[relative])==pin,"PREVIOUS_FIXTURE_PIN:"+relative)
    cold_raw=subject.initial_read(COLD_REPORT,MIB)
    need(sha(cold_raw)==COLD_REPORT_PIN,"COLD_PUBLIC_REPORT_PIN")
    cold=json.loads(cold_raw)["result"]
    need(sha(subject.initial_read(CUSTODY_LIMITS,65536))==CUSTODY_PIN,"CUSTODY_LIMITS_PIN")
    question=dict(universes=["u"],type=(
        "forall {T : Type u} (o : RepairTheory.ClosureBridge.OrderData T)\n"
        "  (r : RepairTheory.Repair T) (rs : List (RepairTheory.Repair T)),\n"
        "  RepairTheory.ClosureBridge.AllClosure o (List.cons r rs) ->\n"
        "  RepairTheory.ClosureBridge.AllClosure o rs"))
    query_path=base/"question.json"; query_raw=raw(question); save(query_path,query_raw)
    config_doc=config_document(query_path,sha(query_raw)); subject.validate_config(config_doc)
    config=base/"config.json"; config_raw=raw(config_doc); save(config,config_raw)
    output=base/"query"
    argv=[str(PYTHON/"python.exe"),"-I","-S","-B",args.source,"--config",str(config),
          "--config-sha256",sha(config_raw),"--output",str(output),"--approve-local-query"]
    save(base/"PUBLIC-INVOCATION.json",dict(argv=argv,source_sha256=args.source_sha256,
        config_sha256=sha(config_raw),question_sha256=sha(query_raw),public_invocations=1))
    env={k:v for k,v in os.environ.items() if not k.upper().startswith(
        ("LEAN","PYTHON","RUST","CARGO","RISC0","NODE")) and k.upper() not in {"PATH","VIRTUAL_ENV"}}
    env["PATH"]=os.pathsep.join(map(str,(PYTHON,PYTHON/"DLLs",LEAN/"bin")))
    check(); remaining=100-(time.monotonic()-START)
    need(remaining>65,"PUBLIC_PREFLIGHT_ALLOWANCE")
    with (base/"stdout.txt").open("xb") as stdout,(base/"stderr.txt").open("xb") as stderr:
        code=subprocess.call(argv,cwd=ROOT,env=env,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,
                             timeout=remaining,creationflags=subprocess.CREATE_NO_WINDOW)
    need(code==0,"PUBLIC_FAILED_NO_RETRY")
    result_raw=read(output/"RESULT.json"); result=json.loads(result_raw)
    worker_raw=read(output/"WORKER.json"); worker=json.loads(worker_raw)
    supervision=json.loads(read(output/"SUPERVISION.json")); launch=json.loads(read(output/"LAUNCH.json"))
    need(subject.clean_supervision(supervision,dict(LIMITS,wall_seconds=55)) and
         launch["original_limits"]==LIMITS,"PUBLIC_CLEAN_ORIGINAL_ALLOWANCE")
    need(result["schema"]=="DMKN_ORDINARY_ANCHOR_QUERY_RESULT_V1" and result["ok"] is True and
         result["status"]=="ANCHOR_QUERY_READY" and result["mathematical_acceptance"] is False and
         result["profile_sha256"]==PROFILE and result["config_sha256"]==sha(config_raw) and
         result["query_sha256"]==sha(query_raw) and result["worker_report_sha256"]==sha(worker_raw) and
         result["owner_handles_closed"] is True and result["installation_manifest_sha256"]==INSTALL and
         json.loads(read(base/"stdout.txt"))==result and not (output/"RESULT.pending.json").exists(),
         "PUBLIC_RESULT_BINDING")
    need(worker["ok"] is True and worker["supervised_completion"] is False and
         worker["mathematical_acceptance"] is False and worker["entry_sha256"]==args.source_sha256 and
         worker["owner_handles_closed"] is True and "close_errors" not in worker and
         worker["installation_manifest_sha256"]==INSTALL and type(worker["native_exit_code"]) is int and
         worker["native_exit_code"]==0,"PUBLIC_WORKER_BINDING")
    pins=subject.candidate_pins(SimpleNamespace(output=output,check=check,
        R=SimpleNamespace(ordinary=lambda p,**kw:Path(p),read=fake_read)))
    need(pins==result["files"]==worker["files"],"PUBLIC_CANDIDATE_PINS")
    native_raw=read(output/"native/type.json"); native=json.loads(native_raw)
    need(ignore_forall_display_names(native)==ignore_forall_display_names(json.loads(previous["native/type.json"])),
         "PUBLIC_SAME_QUESTION_STRUCTURE")
    bindings_raw=read(output/"BINDINGS.json"); bindings=json.loads(bindings_raw)
    expected_query=dict(schema="DMKN_ORDINARY_FORMAL_TYPE_QUERY_V1",key_profile=KEY_PROFILE,
        semantic_id=SEMANTIC,type=native[2],type_bindings=bindings,universe_params=native[1])
    need(bindings_raw==previous["query/BINDINGS.json"] and
         read(output/"QUERY.json")==raw(expected_query) and
         read(output/"SPECS.json")==previous["query/SPECS.json"],"PUBLIC_EXACT_BINDINGS_AND_KEY")
    need(result["namespace"]==worker["namespace"]==NAMESPACE and
         result["features"]==worker["features"]==FEATURES and
         result["interpretation"]==worker["interpretation"],"PUBLIC_DISCOVERY_HANDOFF")
    interpretation=result["interpretation"]
    need(interpretation["semantic_id"]==SEMANTIC and interpretation["foundation_id"]==FOUNDATION and
         interpretation["implementation_id"]==IMPLEMENTATION and interpretation["store_id"]==STORE and
         interpretation["context_root"]==CONTEXT and interpretation["anchor_id"]==ANCHOR and
         interpretation["module_name"]==MODULE and interpretation["reference_count"]==5 and
         interpretation["key_profile"]==KEY_PROFILE and
         interpretation["vocabulary"]=="FIXED_BASIS_AND_REGISTERED_CHAIN","PUBLIC_INTERPRETATION")
    anchor=json.loads(read(output/"ANCHOR.json"))
    need(anchor["schema"]=="DMKN_ORDINARY_ANCHOR_QUERY_SELECTION_V1" and
         all(anchor[key]==value for key,value in interpretation.items()) and
         anchor["import_directories"]==cold["import_directories"] and len(anchor["modules"])==1 and
         len(anchor["record_sha256"])==1,"PUBLIC_ANCHOR_SELECTION")
    selected_module=anchor["modules"][0]
    need(selected_module["anchor_id"]==ANCHOR and selected_module["module_name"]==name(MODULE) and
         selected_module["direct_imports"]==[name("Init")] and selected_module["added_names"]==cold["added_names"],
         "PUBLIC_EXACT_CHAIN_MODULE")
    parts=selected_module["artifact_parts"]
    need(len(parts)==5 and {Path(part["path"]).name:{k:part[k] for k in ("bytes","sha256")} for part in parts}
         ==cold["artifact_parts"] and all(str(Path(part["path"]).parent)==cold["module_directory"] for part in parts) and
         anchor["artifact_bytes"]==sum(part["bytes"] for part in parts),"PUBLIC_REGISTERED_ARTIFACT_PINS")
    expected_paths=[str(PACKAGE/"authoring/helpers"),str(LEAN/"lib/lean"),*cold["import_directories"]]
    need(anchor["lean_path"]==["\\\\?\\"+path for path in expected_paths],"PUBLIC_EXACT_IMPORT_PATHS")
    need(read(output/"native/Query.lean")==subject.source_text(("u",),question["type"],output/"native/type.json",MODULE),
         "PUBLIC_FIXED_SOURCE")
    need(read(config)==config_raw and read(query_path)==query_raw and sha(read(args.source))==args.source_sha256,
         "PUBLIC_FINAL_INPUT_PINS")
    deltas={name:dict(previous_sha256=old,current_sha256=pins[name]["sha256"],byte_identical=old==pins[name]["sha256"])
            for name,old in (("native/type.json",PREVIOUS_PINS["native/type.json"]),
                              ("QUERY.json",PREVIOUS_PINS["query/QUERY.json"]))}
    return dict(group="one_public_registered_anchor_question",public_invocations=1,
        native_extractions_reported=1,result_sha256=sha(result_raw),output_pins=pins,raw_comparison=deltas,
        comparison="EXACT_STRUCTURE_EXCEPT_FORALL_DISPLAY_NAMES;EXACT_REFERENCE_BINDINGS_AND_TYPE_KEY",
        namespace=NAMESPACE,features=FEATURES,interpretation=interpretation,
        inclusive_worker_job_cpu_seconds=supervision["final_job"]["cpu_seconds"],
        wrapper_cpu_seconds=result["wrapper_cpu_seconds_before_final_report"],
        mathematical_acceptance=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    parser.add_argument("--mode",required=True,choices=("controls","public"))
    for key in ("source","source-sha256","output"): parser.add_argument("--"+key,required=True)
    args=parser.parse_args()
    report=dict(schema="DMKN_ORDINARY_ANCHOR_QUERY_TEST_V1",ok=False,mode=args.mode,
                source_sha256=args.source_sha256,groups=[],mathematical_acceptance=False)
    output=None
    try:
        need(os.name=="nt" and Path.cwd()==ROOT and Path(sys.executable)==PYTHON/"python.exe" and
             sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
             "RUNTIME_PROFILE")
        with ExitStack() as stack:
            forbid_effects(stack,native=args.mode=="controls")
            source=Path(args.source)
            need(source==ROOT/"software/v5/ordinary_anchor_query/query.py","SUBJECT_SELECTION")
            subject=load_subject(source,args.source_sha256)
            proposed=Path(args.output)
            need(proposed.is_absolute() and proposed.parent.parent==LOCAL and
                 proposed.name in ("controls","public") and proposed.resolve()==proposed and
                 proposed.parent.is_dir() and not proposed.exists(),"FRESH_OUTPUT_DOMAIN")
            # Every ancestor must be ordinary; no redirected output or retained state path.
            for path in (*reversed(proposed.parents),):
                info=path.lstat()
                need(path.is_dir() and not path.is_symlink() and not getattr(info,"st_file_attributes",0)&0x400,
                     "OUTPUT_ANCESTOR_REDIRECT")
            proposed.mkdir(); output=proposed
            if args.mode=="controls":
                for action in (lambda:config_controls(subject,output),lambda:binding_controls(subject),
                               lambda:selection_controls(subject,output),lambda:close_controls(subject),
                               lambda:setup_order_controls(subject,output),lambda:worker_controls(subject,output),
                               lambda:parent_controls(subject,output)):
                    report["groups"].append(action()); check()
                report["native_processes"]=0
            else:
                report["groups"].append(public_check(subject,args,output))
            need(sha(read(source))==args.source_sha256,"FINAL_SOURCE_PIN")
        report.update(ok=True,status="PASS")
    except BaseException as error:
        report.update(ok=False,status="FAIL_PRESERVED_NO_RETRY",error_type=type(error).__name__,error=str(error)[:3000])
    report.update(wall_seconds_before_report=time.monotonic()-START,
        harness_cpu_seconds_before_report=time.process_time()-CPU,
        cost_scope="OUTER_JOB_INCLUDES_HARNESS_AND_ALL_DESCENDANTS;NESTED_OBSERVATIONS_NOT_SUMMED")
    if output is not None: save(output/"TEST-RESULT.json",report)
    print(raw(report).decode("ascii"),flush=True)
    return 0 if report["ok"] else 1


if __name__=="__main__":
    raise SystemExit(main())

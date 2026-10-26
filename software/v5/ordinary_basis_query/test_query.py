"""Focused basis-query controls; source only until root selects execution.

Controls load only selected stateless codecs, never an owner/catalog/custody.
Synthetic ASTs and supervision reports are explicitly inert test data, not
accepted mathematics. Public mode is a separate one-extraction selection.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack, redirect_stdout
from copy import deepcopy
import hashlib
import importlib.util
import io
import json
import math
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
START_WALL, START_CPU = time.monotonic(), time.process_time()
MIB = 1024**2
PROFILE = "b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7"
INSTALL = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
NATIVE_AST = "226bb411b2a7255eabc522f482afd2c199877ad624737fddf7b27ec0f8658480"
MODULES = {
    "ordinary_evidence": "installation/py/ordinary_evidence.py",
    "ordinary_semantics": "installation/py/ordinary_semantics.py",
    "portable_evidence": "installation/py/portable_evidence.py",
    "ordinary_preview": "authoring/py/ordinary_preview.py",
    "portable_preview": "authoring/py/portable_preview.py",
    "formal_query": "authoring/py/formal_query.py",
}
KNOWN = {
    "Eq": "80b9689fa00451ea0cb456c6e822415c8ca66d4d0cd6a47c890c84371a59d6d5",
    "Nat.zero": "ea54d1998d3fd8cec06155ef7bdc70690bb898be6faea2ce18243c32cfab82c9",
    "Nat.add": "b6e338b03825275ae69439503bc2266eb3c691e511a0036b6ad92b696330a63b",
    "Nat": "ca48e6ac6a5c8bfe6df0d8156961a55a1f3aec59783b8f31b5fd2e0c151eace2",
}
LIMITS = dict(wall_seconds=60, cpu_seconds=30, memory_mib=768,
              active_processes=4, stdout_bytes=MIB, stderr_bytes=MIB)


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START_WALL < 105 and time.process_time()-START_CPU < 40,
         "BASIS_TEST_ORIGINAL_ALLOWANCE")


def raw(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path, maximum=4*MIB):
    check()
    with Path(path).open("rb") as stream:
        data = stream.read(maximum+1)
    need(0 < len(data) <= maximum, "BASIS_TEST_READ_BOUND")
    return data


def save(path, value):
    data = value if type(value) is bytes else raw(value)
    need(0 < len(data) <= 4*MIB, "BASIS_TEST_WRITE_BOUND")
    with Path(path).open("xb") as stream:
        stream.write(data)
    return dict(bytes=len(data), sha256=sha(data))


def load_source(path, expected, label):
    data = read(path)
    need(sha(data) == expected and label not in sys.modules, "BASIS_TEST_SOURCE_PIN:"+label)
    spec = importlib.util.spec_from_file_location(label, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[label] = module
    try:
        exec(compile(data, str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[label]
        raise
    return module


def refuses(call, label, fragment=None):
    check()
    try:
        call()
    except (ValueError, TypeError, KeyError, OSError) as error:
        if fragment is not None:
            need(fragment in str(error), "BASIS_TEST_WRONG_REFUSAL:"+label+":"+str(error))
        return dict(case=label, error_type=type(error).__name__, error=str(error)[:300])
    raise AssertionError("BASIS_TEST_UNEXPECTED_ACCEPTANCE:"+label)


def forbidden(*_args, **_kwargs):
    raise AssertionError("BASIS_TEST_FORBIDDEN_NATIVE_NETWORK_OR_DATABASE")


def forbid_effects(stack):
    for target in ("subprocess.Popen", "subprocess.run", "subprocess.call",
                   "subprocess.check_call", "subprocess.check_output",
                   "sqlite3.connect", "socket.socket", "socket.create_connection", "os.system"):
        stack.enter_context(patch(target, side_effect=forbidden))


def name(text):
    return [[0, {"$bytes": list(part.encode("utf-8"))}] for part in text.split(".")]


def codec_api(package):
    profile_raw = read(package/"PROFILE.json")
    install_raw = read(package/"installation/INSTALLATION.json")
    need(sha(profile_raw) == PROFILE and sha(install_raw) == INSTALL, "BASIS_TEST_APPROVED_PACKAGE")
    profile, install = json.loads(profile_raw), json.loads(install_raw)
    loaded, pins = {}, {}
    for label, relative in MODULES.items():
        expected = (install["files"][relative[len("installation/"):]]
                    if relative.startswith("installation/") else profile["files"][relative])
        data = read(package/relative)
        need(dict(bytes=len(data), sha256=sha(data)) == expected, "BASIS_TEST_CODEC_PIN:"+label)
        pins[relative] = expected
        loaded[label] = load_source(package/relative, expected["sha256"], label)
    Q, S = loaded["formal_query"], loaded["ordinary_semantics"]
    inventory = read(package/"installation/foundation/inventory.json")
    need(sha(inventory) == S.INVENTORY, "BASIS_TEST_FIXED_INVENTORY")
    need(Q.S is S and Q.E is loaded["ordinary_evidence"], "BASIS_TEST_SHARED_STATELESS_HELPERS")
    return Q, S, inventory, pins


def query_controls(subject, base):
    refusals = []
    for malformed in (b'{"x":1,"x":2}', b'{"type":"Nat","type":"Prop","universes":[]}',
                      b'{"x":NaN}', b'{"x":Infinity}', b'{"x":1.25}', b'{',
                      b'[] trailing', b'\xff', b'\xef\xbb\xbf{}'):
        refusals.append(refuses(lambda item=malformed: subject.strict_json(item), "strict-json:"+repr(malformed)))
    valid = dict(universes=["u", "v"], type="forall (A : Type u) (B : Type v), A -> B -> A")
    universes, term = subject.validate_query(deepcopy(valid))
    need(universes == ("u", "v") and term == valid["type"], "BASIS_TEST_QUERY_DETACH_ORDER")
    bad_queries = [dict(universes=[], type=""), dict(universes=[], type=" "*4),
                   dict(universes=[], type=True), dict(universes="u", type="Nat"),
                   dict(universes=["u", "u"], type="Nat"),
                   dict(universes=["u.v"], type="Nat"), dict(universes=["u\nuniverse x"], type="Nat"),
                   dict(universes=[True], type="Nat"), dict(universes=["u"+str(i) for i in range(33)], type="Nat"),
                   dict(universes=[], type="a"*65537), dict(universes=[], type="λ"*32769),
                   dict(universes=[], type="Nat\0"), {"type":"Nat"},
                   dict(universes=[], type="Nat", imports=["UnselectedProject"])]
    for index, doc in enumerate(bad_queries):
        refusals.append(refuses(lambda item=doc: subject.validate_query(item), "query:"+str(index)))
    output_path = base/"source directory"/"native-type.json"
    source = subject.source_text(universes, term, output_path)
    need(type(source) is bytes and source.count(b"public import Init") == 1 and
         source.count(b"public meta import OwnerQueryCommand") == 1 and
         source.count(b"#ordinary_type_query") == 1 and
         "universe «u» «v»".encode("utf-8") in source and term.encode("utf-8") in source,
         "BASIS_TEST_FIXED_SOURCE_AND_UNIVERSE_ORDER")
    # The output path is a quoted string literal, never executable Lean text.
    command_tail = source.decode("utf-8").split("#ordinary_type_query", 1)[1]
    start = command_tail.index('"')
    decoded_path, end = json.JSONDecoder().raw_decode(command_tail[start:])
    need(Path(decoded_path) == output_path and command_tail[start+end:].lstrip().startswith(":"),
         "BASIS_TEST_QUOTED_NATIVE_OUTPUT_PATH")
    # The explicitly approved term is not claimed to be sandboxed or filtered.
    approved_text = 'Nat\n-- owner supplied text remains subject to execution approval'
    need(approved_text.encode() in subject.source_text((), approved_text, output_path),
         "BASIS_TEST_NO_INVENTED_SOURCE_SANDBOX")
    return dict(group="strict_query_and_fixed_source", refusals=refusals,
                source_sha256=sha(source), mathematical_acceptance=False)


def config_document(args, query_path):
    return dict(schema="DMKN_ORDINARY_BASIS_QUERY_V1", package=args.package,
                profile_sha256=PROFILE, python_runtime=args.python_runtime, lean_runtime=args.lean_runtime,
                query=dict(path=str(query_path), sha256="1"*64), limits=deepcopy(LIMITS))


def config_controls(subject, args, base):
    doc = config_document(args, base/"query.json")
    got = subject.validate_config(deepcopy(doc))
    need(got == doc, "BASIS_TEST_CONFIG_SHAPE_PRESERVED")
    bad = []
    for key in doc:
        changed = deepcopy(doc); del changed[key]
        bad.append(("missing:"+key, changed))
    for key, value in (("argv", ["arbitrary.exe"]), ("project_search_paths", []),
                       ("imports", ["Foreign"]), ("executable", "anything.exe"),
                       ("catalog", str(base/"not-an-owner"))):
        changed = deepcopy(doc); changed[key] = value
        bad.append(("extra:"+key, changed))
    for key, value in (("schema", "unknown"), ("profile_sha256", "g"*64),
                       ("profile_sha256", "a"*63), ("package", True)):
        changed = deepcopy(doc); changed[key] = value
        bad.append(("field:"+key+":"+str(value), changed))
    for key, low, high in (("wall_seconds",35,600), ("cpu_seconds",4,600),
                          ("memory_mib",1,4096), ("active_processes",2,4),
                          ("stdout_bytes",1,MIB), ("stderr_bytes",1,MIB)):
        for value in (True, low-1, high+1):
            changed = deepcopy(doc); changed["limits"][key] = value
            bad.append(("limit:"+key+":"+str(value), changed))
    changed = deepcopy(doc); changed["limits"]["renew"] = 1; bad.append(("renew",changed))
    changed = deepcopy(doc); changed["query"]["sha256"] = "x"*64; bad.append(("query-pin",changed))
    changed = deepcopy(doc); changed["query"]["argv"] = []; bad.append(("query-argv",changed))
    refusals = [refuses(lambda item=item:subject.validate_config(item), label) for label,item in bad]
    return dict(group="exact_config_and_finite_limits", refusals=refusals, mathematical_acceptance=False)


def basis_controls(subject, args, Q, S, inventory):
    native = read(Path(args.native_fixture), MIB)
    need(sha(native) == NATIVE_AST, "BASIS_TEST_RETAINED_AST_PIN")
    names = Q.reference_names(native)
    expected_by_key = {Q.E.name_key(name(label)): identity for label,identity in KNOWN.items()}
    need({Q.E.name_key(item) for item in names} == set(expected_by_key), "BASIS_TEST_RETAINED_REFERENCE_CENSUS")
    expected = Q.E.canonical_json([[item, expected_by_key[Q.E.name_key(item)]] for item in names])
    bindings = subject.basis_bindings(Q, S, native, inventory, S.semantic_id(), check)
    need(bindings == expected, "BASIS_TEST_EXACT_BASIS_IDENTITIES_AND_ORDER")
    hints = subject.make_hints(Q, S, native, inventory, S.semantic_id(), check)
    expected_query = Q.bind_native_type(native, expected, semantic_id=S.semantic_id())
    expected_specs = Q.E.canonical_json([Q.query_spec(expected_query)])
    need(hints["bindings_raw"] == expected and hints["query_raw"] == expected_query and
         hints["specs_raw"] == expected_specs and hints["interpretation"],
         "BASIS_TEST_EXISTING_QUERY_SPEC_SEMANTICS")
    return dict(group="actual_fixed_basis_binding", reference_count=len(names),
                bindings_sha256=sha(bindings), query_sha256=sha(expected_query),
                specs_sha256=sha(expected_specs), mathematical_acceptance=False)


def vocabulary_controls(subject, Q, S, inventory):
    unknown = name("NotInFixedBasis")
    # Syntax-only negative fixture. It claims neither native validity nor acceptance.
    native = Q.E.canonical_json([Q.NATIVE_SCHEMA, [], [Q.E.EXPR_FORMAT, [], [[2, unknown, []]], 0]])
    need(Q.reference_names(native) == [unknown], "BASIS_TEST_UNKNOWN_AST_CENSUS")
    with patch.object(S, "basis_symbol_id", side_effect=AssertionError("DERIVED_ID_BEFORE_VOCABULARY_REFUSAL")):
        try:
            subject.basis_bindings(Q,S,native,inventory,S.semantic_id(),check)
        except subject.UnknownVocabulary as error:
            need(error.names == [unknown], "BASIS_TEST_EXACT_UNSUPPORTED_NAMES")
        else:
            raise AssertionError("BASIS_TEST_NONBASIS_ACCEPTED")
    refusals = []
    for index, bad_inventory in enumerate((inventory+b" ", inventory[:-1], b"[]")):
        refusals.append(refuses(lambda item=bad_inventory:
            subject.basis_bindings(Q,S,native,item,S.semantic_id(),check), "inventory:"+str(index)))
    refusals.append(refuses(lambda:subject.basis_bindings(Q,S,native,inventory,"0"*64,check),
                            "semantic-selection"))
    return dict(group="nonbasis_and_fixed_inventory_refusals", unsupported_names=[unknown],
                refusals=refusals, mathematical_acceptance=False)


def clean_fixture():
    return dict(status="COMMAND_EXITED_ZERO_AND_CLOSED", child_exit_code=0,
                direct_child_reaped=True, job_closed=True, termination_requested=False,
                cleanup_errors=[], final_job=dict(active_processes=0, terminated_processes=0,
                                                  cpu_seconds=0.25))


def closure_controls(subject):
    good = clean_fixture()
    need(subject.clean_supervision(deepcopy(good)) is True, "BASIS_TEST_SYNTHETIC_CLEAN")
    cases = []
    for key,value in (("status","FAILED"),("child_exit_code",1),("child_exit_code",False),
                      ("direct_child_reaped",False),("direct_child_reaped",1),
                      ("job_closed",False),("termination_requested",True),
                      ("cleanup_errors",["unknown"]),("final_job",None)):
        changed = deepcopy(good); changed[key] = value; cases.append((key+":"+repr(value),changed))
    for key,value in (("active_processes",1),("active_processes",False),
                      ("terminated_processes",1),("terminated_processes",False),
                      ("cpu_seconds",True),("cpu_seconds",float("nan")),
                      ("cpu_seconds",float("inf")),("cpu_seconds",-1)):
        changed = deepcopy(good); changed["final_job"][key] = value; cases.append((key+":"+repr(value),changed))
    for key in good:
        changed = deepcopy(good); del changed[key]; cases.append(("missing:"+key,changed))
    for label,case in cases:
        need(subject.clean_supervision(case) is False, "BASIS_TEST_UNCLEAN_ACCEPTED:"+label)
    return dict(group="synthetic_terminal_closure", rejected=[label for label,_ in cases],
                synthetic=True, mathematical_acceptance=False)


def call_args(config, config_raw, output, **changes):
    result = SimpleNamespace(config=str(config), config_sha256=sha(config_raw),
        output=str(output), approve_local_query=True, worker=False,
        origin=None, deadline=None, entry_sha256=None)
    for key, value in changes.items():
        setattr(result, key, value)
    return result


def path_controls(subject, args, base, launch):
    """Real prelaunch helpers; only duplicate test-module loading is intercepted."""
    work = base/"prelaunch"; work.mkdir()
    query = work/"query.json"; query_raw = raw(dict(universes=[], type="Nat"))
    save(query, query_raw)
    doc = config_document(args, query); doc["query"]["sha256"] = sha(query_raw)
    config = work/"config.json"; config_raw = raw(doc); save(config, config_raw)
    def already_pinned(label, path, data):
        need(label == "_basis_query_launch_support" and Path(path) == Path(args.package)/"run.py" and
             sha(data) == subject.RUN_SHA, "BASIS_TEST_EXACT_LAUNCHER_REUSE")
        return launch
    cases = []
    def refuse_case(label, selected, fragment):
        cases.append(refuses(lambda:subject.setup(selected), label, fragment))
    with patch.object(subject, "load_source", side_effect=already_pinned):
        accepted = subject.setup(call_args(config, config_raw, work/"valid-never-created"))
        need(accepted.query_raw == query_raw and accepted.universes == () and
             accepted.bound["installation_manifest_sha256"] == INSTALL and
             not accepted.output.exists(), "BASIS_TEST_SETUP_WITHOUT_OUTPUT_OR_OWNER")
        refuse_case("approval", call_args(config,config_raw,work/"no-approval",approve_local_query=False),
                    "LOCAL_EXECUTION_APPROVAL_REQUIRED")
        refuse_case("config-pin", call_args(config,config_raw,work/"bad-pin",config_sha256="0"*64), "CONFIG_PIN")
        refuse_case("public-private-options", call_args(config,config_raw,work/"private",origin=0.0),
                    "PRIVATE_WORKER_OPTIONS")
        refuse_case("worker-entry-pin", call_args(config,config_raw,work/"entry-pin",worker=True,
                    origin=subject.START,deadline=subject.START+LIMITS["wall_seconds"]-5,
                    entry_sha256="0"*64), "WORKER_ENTRY_PIN")
        existing = work/"existing"; existing.mkdir(); sentinel = existing/"retain.txt"
        save(sentinel,b"preserve this pre-existing file")
        refuse_case("fresh-output",call_args(config,config_raw,existing),"RUN_FRESH_PATH")
        for label, output in (("package",Path(args.package)/"basis-query-must-not-create"),
                              ("python",Path(args.python_runtime)/"basis-query-must-not-create"),
                              ("lean",Path(args.lean_runtime)/"basis-query-must-not-create"),
                              ("source",Path(args.source).parent/"basis-query-must-not-create")):
            refuse_case("output-overlap:"+label,call_args(config,config_raw,output),"OUTPUT_INPUT_OVERLAP")
            need(not output.exists(),"BASIS_TEST_OVERLAP_CREATED:"+label)
        refuse_case("relative-output",call_args(config,config_raw,Path("relative-output")),"RUN_ABSOLUTE_NONROOT_PATH")
        refuse_case("alias-component",call_args(config,config_raw,str(work)+"\\..\\alias-output"),"RUN_PATH_COMPONENT")
        changes = [("query-pin", {"query":dict(path=str(query),sha256="0"*64)}, "QUERY_PIN"),
                   ("support-overlap", {"python_runtime":args.package}, "BASIS_QUERY_SUPPORT_OVERLAP"),
                   ("profile-pin", {"profile_sha256":"0"*64}, "RUN_PROFILE_PIN")]
        for label, updates, fragment in changes:
            changed = deepcopy(doc); changed.update(updates)
            data = raw(changed); path = work/(label+".json"); save(path,data)
            refuse_case(label,call_args(path,data,work/(label+"-output")),fragment)
        need(read(sentinel) == b"preserve this pre-existing file" and read(query) == query_raw and
             read(config) == config_raw,"BASIS_TEST_PRELAUNCH_INPUTS_PRESERVED")
    return dict(group="prelaunch_pins_approval_paths",refusals=cases,owner_loaded=False,
                native_processes=0,mathematical_acceptance=False)


def metered_fixture(limits):
    result = clean_fixture()
    result.update(limits=deepcopy(limits),wall_seconds_through_cleanup=0.5,
        wrapper_supervision_cpu_seconds=0.1,observed_logs=dict(stdout_bytes=0,stderr_bytes=0))
    return result


def allowance_controls(subject):
    limits = dict(LIMITS,wall_seconds=LIMITS["wall_seconds"]-5)
    good = metered_fixture(limits)
    need(subject.clean_supervision(good,limits) is True,"BASIS_TEST_METERED_CLEAN")
    cases = []
    for key in ("limits","wall_seconds_through_cleanup","wrapper_supervision_cpu_seconds","observed_logs"):
        changed = deepcopy(good); del changed[key]; cases.append(("missing:"+key,changed))
    for key,value in (("wall_seconds_through_cleanup",limits["wall_seconds"]+0.1),
                      ("wall_seconds_through_cleanup",True),("wrapper_supervision_cpu_seconds",float("nan"))):
        changed = deepcopy(good); changed[key]=value; cases.append((key+":"+repr(value),changed))
    for key,value in (("cpu_seconds",limits["cpu_seconds"]+0.1),("cpu_seconds",True)):
        changed=deepcopy(good); changed["final_job"][key]=value; cases.append((key+":"+repr(value),changed))
    for key in ("stdout_bytes","stderr_bytes"):
        for value in (True,-1,limits[key]+1):
            changed=deepcopy(good); changed["observed_logs"][key]=value; cases.append((key+":"+repr(value),changed))
    changed=deepcopy(good); changed["limits"]["wall_seconds"]+=1; cases.append(("renewed-limits",changed))
    for label,case in cases:
        need(subject.clean_supervision(case,limits) is False,"BASIS_TEST_BAD_METERED_REPORT:"+label)
    return dict(group="synthetic_allowance_accounting",rejected=[label for label,_ in cases],
                synthetic=True,mathematical_acceptance=False)


def terminal_controls(subject,args,base,launch):
    """Inert parent-state doubles, real bounded files/pins and publication path."""
    cases=[]
    variants=("ready","unclean","native-bool","candidate-pin","input-pin","support-pin",
              "extra-native","missing-native","pending-fsync","pending-readback")
    for variant in variants:
        check(); work=base/("terminal-"+variant); work.mkdir()
        config=work/"config.json"; query=work/"query.json"; entry=work/"synthetic-entry.py"
        config_raw=b'{"synthetic":"not a usable product config"}'
        query_raw=b'{"synthetic":"not native mathematics"}'
        entry_raw=b'# explicitly inert parent-control fixture\n'
        for path,data in ((config,config_raw),(query,query_raw),(entry,entry_raw)):
            save(path,data)
        selected=call_args(config,config_raw,work/"candidate")
        s=SimpleNamespace(config_path=config,config_raw=config_raw,query_path=query,query_raw=query_raw,
            entry=entry,entry_raw=entry_raw,output=Path(selected.output),python=Path(args.python_runtime),
            lean=Path(args.lean_runtime),package=Path(args.package),check=check,
            config=dict(profile_sha256=PROFILE,query=dict(sha256=sha(query_raw))),
            bound=dict(installation_manifest_sha256=INSTALL),limits=deepcopy(LIMITS),
            origin=subject.START,deadline=subject.START+LIMITS["wall_seconds"])
        child_limits=dict(LIMITS,wall_seconds=LIMITS["wall_seconds"]-5)
        calls=[]
        original_environment=lambda cwd:{"SYNTHETIC_TEST":"YES"}
        supervisor=SimpleNamespace(child_environment=original_environment)
        def bind_support(package,profile,python,checked):
            need((package,profile,python)==(s.package,PROFILE,s.python),"BASIS_TEST_FINAL_SUPPORT_SELECTION")
            checked()
            if variant=="support-pin":
                raise ValueError("SYNTHETIC_FINAL_SUPPORT_PIN")
            return s.bound
        s.R=SimpleNamespace(ordinary=launch.ordinary,read=launch.read,bind_support=bind_support,
                            load_supervision=lambda bound:(supervisor,None))
        def supervise(argv,cwd,evidence,limits,job,*,started):
            need(not calls and cwd==s.output and evidence==s.output/"child" and limits==child_limits and
                 started==s.origin and argv[:5]==[str(s.python/"python.exe"),"-I","-S","-B",str(s.entry)] and
                 argv.count("--worker")==1 and argv.count("--approve-local-query")==1 and
                 argv[argv.index("--deadline")+1]==repr(s.deadline-5),"BASIS_TEST_FIXED_WORKER_ALLOWANCE")
            calls.append(list(argv)); (s.output/"native").mkdir()
            for name in sorted(subject.REQUIRED_OUTPUTS):
                save(s.output/name,("SYNTHETIC_NOT_NATIVE:"+name).encode())
            files=subject.candidate_pins(s)
            worker=dict(schema="DMKN_ORDINARY_BASIS_QUERY_WORKER_V1",ok=True,
                status="CANDIDATE_HINTS_NOT_SUPERVISED_SUCCESS",supervised_completion=False,
                mathematical_acceptance=False,native_exit_code=0,files=files,
                config_sha256=selected.config_sha256,profile_sha256=PROFILE,
                entry_sha256=sha(entry_raw),query_sha256=sha(query_raw),installation_manifest_sha256=INSTALL,
                interpretation={"synthetic":True},namespace="synthetic-not-a-real-namespace",
                features=["synthetic-not-a-real-feature"])
            if variant=="native-bool": worker["native_exit_code"]=False
            if variant=="candidate-pin": worker["files"]["BINDINGS.json"]["sha256"]="0"*64
            save(s.output/"WORKER.json",worker)
            if variant=="input-pin":
                with query.open("ab") as stream: stream.write(b" ")
            if variant=="extra-native": save(s.output/"native/unselected.bin",b"inert")
            if variant=="missing-native":
                # Move a fresh synthetic test fixture only; preserve its original bytes.
                (s.output/"native/Query.olean").rename(work/"retained-missing-Query.olean")
            report=metered_fixture(limits)
            if variant=="unclean": report["direct_child_reaped"]=False
            return report
        supervisor.supervise=supervise
        normal_save=subject.save_bytes
        def faulted_save(path,data,maximum=MIB):
            if Path(path).name=="RESULT.pending.json" and variant=="pending-fsync":
                with patch.object(subject.os,"fsync",side_effect=OSError("SYNTHETIC_PENDING_FSYNC")):
                    return normal_save(path,data,maximum)
            if Path(path).name=="RESULT.pending.json" and variant=="pending-readback":
                with patch.object(subject,"initial_read",side_effect=ValueError("SYNTHETIC_PENDING_READBACK")):
                    return normal_save(path,data,maximum)
            return normal_save(path,data,maximum)
        printed=io.StringIO()
        with patch.object(subject,"setup",return_value=s),patch.object(subject,"save_bytes",side_effect=faulted_save),redirect_stdout(printed):
            code=subject.parent(selected)
        result=subject.strict_json(printed.getvalue().strip().encode(),reports=True)
        save(work/"captured-parent-stdout.json",printed.getvalue().encode())
        need(len(calls)==1 and supervisor.child_environment is original_environment,
             "BASIS_TEST_SINGLE_SYNTHETIC_SUPERVISION_AND_RESTORE")
        need(result["mathematical_acceptance"] is False and result["known_worker_job_cpu_seconds"]==0.25 and
             result["cost_scope"]=="WORKER_AND_LEAN_INCLUSIVE_JOB;TRUSTED_WRAPPER_CPU_SEPARATE;NO_DOUBLE_COUNT",
             "BASIS_TEST_NO_ACCEPTANCE_OR_CPU_DOUBLE_COUNT")
        marker=s.output/"RESULT.json"; pending=s.output/"RESULT.pending.json"
        if variant=="ready":
            need(code==0 and result["ok"] is True and result["status"]=="BASIS_QUERY_READY" and
                 marker.is_file() and not pending.exists() and json.loads(read(marker))==result,
                 "BASIS_TEST_SYNTHETIC_READY_GATE")
        elif variant.startswith("pending-"):
            need(code==1 and result["ok"] is False and result["status"]=="RESULT_WRITE_FAILED" and
                 not marker.exists() and pending.is_file(),"BASIS_TEST_NO_MARKER_AFTER_PUBLICATION_FAULT")
        else:
            need(code==1 and result["ok"] is False and result["status"]=="QUERY_NOT_READY" and
                 marker.is_file() and json.loads(read(marker))["ok"] is False,
                 "BASIS_TEST_FALSE_READY:"+variant)
            expected={"unclean":"WORKER_NOT_CLEANLY_COMPLETE","native-bool":"WORKER_BINDING",
                "candidate-pin":"CANDIDATE_CHANGED","input-pin":"INPUT_CHANGED",
                "support-pin":"SYNTHETIC_FINAL_SUPPORT_PIN","extra-native":"NATIVE_CENSUS",
                "missing-native":"NATIVE_CENSUS"}[variant]
            need(expected in result["error"],"BASIS_TEST_WRONG_TERMINAL_GATE:"+variant)
        cases.append(dict(case=variant,status=result["status"],exit_code=code,synthetic=True))
    return dict(group="synthetic_parent_terminal_and_publication",cases=cases,
                native_processes=0,synthetic=True,mathematical_acceptance=False)


def public_check(subject,args,base,Q,S,inventory,launch):
    """Exactly one future public invocation; this function is never used by controls."""
    query=base/"query.json"
    query_doc=dict(universes=[],type="forall (p q : Prop), And p q -> And q p")
    query_raw=raw(query_doc); save(query,query_raw)
    config_doc=config_document(args,query); config_doc["query"]["sha256"]=sha(query_raw)
    config=base/"config.json"; config_raw=raw(config_doc); save(config,config_raw)
    output=base/"public"
    argv=[str(Path(args.python_runtime)/"python.exe"),"-I","-S","-B",args.source,
          "--config",str(config),"--config-sha256",sha(config_raw),"--output",str(output),"--approve-local-query"]
    save(base/"PUBLIC-INVOCATION.json",dict(argv=argv,query_sha256=sha(query_raw),
        config_sha256=sha(config_raw),source_sha256=args.source_sha256,public_invocations=1))
    env={key:value for key,value in os.environ.items() if not key.upper().startswith(
        ("LEAN","PYTHON","RUST","CARGO","RISC0","NODE")) and key.upper() not in {"PATH","VIRTUAL_ENV"}}
    env["PATH"]=os.pathsep.join(map(str,(Path(args.python_runtime),Path(args.python_runtime)/"DLLs",Path(args.lean_runtime)/"bin")))
    check()
    remaining=min(85,100-(time.monotonic()-START_WALL))
    need(remaining>65,"BASIS_TEST_PUBLIC_PREFLIGHT_ALLOWANCE")
    with (base/"public-stdout.txt").open("xb") as stdout,(base/"public-stderr.txt").open("xb") as stderr:
        code=subprocess.call(argv,cwd=ROOT,env=env,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,
                             timeout=remaining,creationflags=subprocess.CREATE_NO_WINDOW)
    check(); need(code==0,"BASIS_TEST_PUBLIC_FAILED_NO_RETRY")
    result_raw=read(output/"RESULT.json",MIB)
    result=subject.strict_json(result_raw,reports=True)
    worker_raw=read(output/"WORKER.json",MIB); worker=subject.strict_json(worker_raw,reports=True)
    supervision=subject.strict_json(read(output/"SUPERVISION.json",MIB),reports=True)
    launch_report=subject.strict_json(read(output/"LAUNCH.json",MIB),reports=True)
    child_limits=dict(LIMITS,wall_seconds=LIMITS["wall_seconds"]-5)
    need(subject.clean_supervision(supervision,child_limits) and launch_report["limits"]==child_limits and
         launch_report["original_limits"]==LIMITS,"BASIS_TEST_PUBLIC_CLEAN_ORIGINAL_ALLOWANCE")
    need(result["schema"]=="DMKN_ORDINARY_BASIS_QUERY_RESULT_V1" and result["ok"] is True and
         result["status"]=="BASIS_QUERY_READY" and result["mathematical_acceptance"] is False and
         result["profile_sha256"]==PROFILE and result["config_sha256"]==sha(config_raw) and
         result["query_sha256"]==sha(query_raw) and result["worker_report_sha256"]==sha(worker_raw) and
         Path(result["specs_file"])==output/"SPECS.json","BASIS_TEST_PUBLIC_TERMINAL_BINDING")
    need(worker["ok"] is True and worker["supervised_completion"] is False and
         worker["mathematical_acceptance"] is False and type(worker["native_exit_code"]) is int and
         worker["native_exit_code"]==0 and worker["entry_sha256"]==args.source_sha256 and
         worker["installation_manifest_sha256"]==INSTALL,"BASIS_TEST_PUBLIC_WORKER_BINDING")
    pins=subject.candidate_pins(SimpleNamespace(output=output,R=launch,check=check))
    need(pins==result["files"]==worker["files"],"BASIS_TEST_PUBLIC_OUTPUT_PINS")
    native=read(output/"native/type.json",MIB)
    need(Q.reference_names(native)==[name("And")],"BASIS_TEST_PUBLIC_EXACT_AND_CENSUS")
    expected_bindings=Q.E.canonical_json([[name("And"),S.basis_symbol_id(S.semantic_id(),S.foundation_id(),name("And"))]])
    expected_query=Q.bind_native_type(native,expected_bindings,semantic_id=S.semantic_id())
    expected_specs=Q.E.canonical_json([Q.query_spec(expected_query)])
    need(read(output/"BINDINGS.json",MIB)==expected_bindings and read(output/"QUERY.json",MIB)==expected_query and
         read(output/"SPECS.json",MIB)==expected_specs,"BASIS_TEST_PUBLIC_EXISTING_CODEC_CORRESPONDENCE")
    expected_interpretation=dict(semantic_id=S.semantic_id(),foundation_id=S.foundation_id(),
        inventory_sha256=S.INVENTORY,vocabulary="EXACT_FIXED_BASIS_ONLY",key_profile=Q.PROFILE_ID)
    need(result["interpretation"]==worker["interpretation"]==expected_interpretation and
         result["namespace"]==worker["namespace"] and result["features"]==worker["features"] and
         result["namespace"] and result["features"],"BASIS_TEST_PUBLIC_DISCOVERY_HANDOFF")
    need(read(output/"native/Query.lean",MIB)==subject.source_text((),query_doc["type"],output/"native/type.json") and
         read(config)==config_raw and read(query)==query_raw and sha(read(Path(args.source)))==args.source_sha256 and
         not (output/"RESULT.pending.json").exists(),"BASIS_TEST_PUBLIC_FINAL_INPUT_AND_SOURCE_BINDINGS")
    need(subject.strict_json(read(base/"public-stdout.txt",MIB).strip(),reports=True)==result,
         "BASIS_TEST_PUBLIC_STDOUT_TERMINAL_AGREEMENT")
    return dict(group="one_public_proof_free_extraction",public_invocations=1,native_extractions_reported=1,
        references=["And"],result_sha256=sha(result_raw),output_pins=pins,
        interpretation=expected_interpretation,namespace=result["namespace"],features=result["features"],
        inclusive_worker_job_cpu_seconds=supervision["final_job"]["cpu_seconds"],
        wrapper_cpu_seconds=result["wrapper_cpu_seconds_before_final_report"],
        cost_scope="Nested observations only; outer selected Job is inclusive; do not sum again",
        mathematical_acceptance=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    parser.add_argument("--mode",required=True,choices=("controls","public"))
    for key in ("source","source-sha256","package","python-runtime","lean-runtime","output"):
        parser.add_argument("--"+key,required=True)
    parser.add_argument("--native-fixture")
    args=parser.parse_args()
    report=dict(schema="DMKN_ORDINARY_BASIS_QUERY_TEST_V1",ok=False,mode=args.mode,
                mathematical_acceptance=False,groups=[],source_sha256=args.source_sha256)
    output=None
    try:
        need(os.name=="nt" and Path.cwd()==ROOT and sys.flags.isolated and sys.flags.no_site and
             sys.dont_write_bytecode and not sys.flags.optimize,"BASIS_TEST_RUNTIME_PROFILE")
        need(args.mode!="controls" or args.native_fixture is not None,"BASIS_TEST_RETAINED_FIXTURE_REQUIRED")
        need(args.mode!="public" or args.native_fixture is None,"BASIS_TEST_PUBLIC_NO_OLD_FIXTURE")
        with ExitStack() as stack:
            if args.mode=="controls": forbid_effects(stack)
            else:
                for target in ("sqlite3.connect","socket.socket","socket.create_connection","os.system"):
                    stack.enter_context(patch(target,side_effect=forbidden))
            subject=load_source(Path(args.source),args.source_sha256,"_basis_query_subject")
            launch=load_source(Path(args.package)/"run.py",subject.RUN_SHA,"_basis_query_control_launch")
            package=launch.ordinary(args.package,directory=True)
            python=launch.ordinary(args.python_runtime,directory=True)
            lean=launch.ordinary(args.lean_runtime,directory=True)
            source=launch.ordinary(args.source)
            proposed=launch.ordinary(args.output,directory=True,fresh=True)
            need(proposed.is_relative_to(ROOT) and all(not launch.overlap(proposed,path) for path in
                 (package,python,lean,source.parent)),"BASIS_TEST_OUTPUT_SELECTION")
            if args.native_fixture:
                fixture=launch.ordinary(args.native_fixture)
                need(not launch.overlap(proposed,fixture),"BASIS_TEST_FIXTURE_OUTPUT_OVERLAP")
            proposed.mkdir(); output=proposed
            Q,S,inventory,codec_pins=codec_api(package); report["stateless_codec_pins"]=codec_pins
            if args.mode=="controls":
                for action in (lambda:query_controls(subject,output),lambda:config_controls(subject,args,output),
                               lambda:path_controls(subject,args,output,launch),
                               lambda:basis_controls(subject,args,Q,S,inventory),
                               lambda:vocabulary_controls(subject,Q,S,inventory),lambda:closure_controls(subject),
                               lambda:allowance_controls(subject),lambda:terminal_controls(subject,args,output,launch)):
                    report["groups"].append(action()); check()
                report["native_processes"]=0
            else:
                report["groups"].append(public_check(subject,args,output,Q,S,inventory,launch))
            need(sha(read(source))==args.source_sha256,"BASIS_TEST_FINAL_SUBJECT_PIN")
        report.update(ok=True,status="PASS")
    except BaseException as error:
        report.update(ok=False,status="FAIL_PRESERVED_NO_RETRY",error_type=type(error).__name__,error=str(error)[:3000])
    report.update(wall_seconds_before_report=time.monotonic()-START_WALL,
                  harness_cpu_seconds_before_report=time.process_time()-START_CPU,
                  cost_scope="Harness CPU separate observation; selected outer Job includes all descendants")
    if output is not None:
        save(output/"TEST-RESULT.json",report)
    print(raw(report).decode("utf-8"),flush=True)
    return 0 if report["ok"] else 1


if __name__=="__main__":
    raise SystemExit(main())

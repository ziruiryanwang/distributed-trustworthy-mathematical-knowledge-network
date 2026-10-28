"""Finite advisory-query controls; no real owner, native or network operation.

Actual pinned catalog validators handle synthetic records and fresh tiny files.
Opening/SQL/activation are explicitly inert doubles, never checking authority.
The private reader class is inspected only inside a test-only opener intercept.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from copy import deepcopy
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
from types import SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()


def need(value, code):
    if not value:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU < 25, "CONTROL_ALLOWANCE")


def forbidden(*args, **kwargs):
    raise AssertionError("CONTROL_FORBIDDEN_NATIVE_NETWORK_DATABASE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, expected=None):
    value = path.read_bytes()
    need(0 < len(value) <= 2*MIB, "CONTROL_READ_BOUND")
    if expected is not None:
        need(sha(value) == expected, "CONTROL_SOURCE_PIN:"+str(path))
    return value


def refuse(call, expected=None):
    try:
        call()
    except (ValueError, OSError) as error:
        if expected is not None:
            need(str(error) == expected, "CONTROL_REFUSAL:"+str(error))
        return
    raise AssertionError("CONTROL_EXPECTED_REFUSAL")


def name(text):
    return [[0, {"$bytes": list(part.encode("utf-8"))}] for part in text.split(".")]


def validator_cases(reader, P, installation, directory):
    """Actual base validators, synthetic extension rows; no accepted context."""
    E, S, L = P.E, P.S, P.L
    parent, unit, operation = "1"*64, "2"*64, "3"*64
    request = P.batch_id([unit])
    root = S.local_root_id(installation.implementation_raw, reader._store_id,
                           "extension", parent, request)
    snapshot = dict(module_name=L.module_name(root), parent_module=L.module_name(parent),
        relative_path="operations/"+operation+"/chunk.olean", artifact_bytes=11,
        artifact_sha256="4"*64, writer_origin="native-check")
    row = dict(schema=P.ROOT_SCHEMA, local_root=root, parent_root=parent, kind="extension",
        semantic_id=reader.semantic_id, foundation_id=reader.foundation_id,
        input_unit_ids=[unit], request_hash=request, bindings=[[name("Example.A"), "5"*64]],
        snapshot=snapshot, origin="native-check",
        provenance=dict(implementation_id=reader.implementation_id, operation_id=operation))
    reader._db.operation = (root, "COMMITTED", 11)
    raw = E.canonical_json(row)
    expected_path = directory.joinpath(*snapshot["relative_path"].split("/"))
    need(not expected_path.exists(), "SYNTHETIC_SNAPSHOT_MUST_BE_ABSENT")
    need(reader._validate_record(raw, row, None, {}) == expected_path and
         reader._verified_artifacts == set(), "ADVISORY_NO_SNAPSHOT_READ_OR_MARK")
    # The same unchanged base validator on this instance, outside the scope
    # wrapper, still attempts ordinary snapshot verification and refuses absence.
    refuse(lambda: P.PortableCatalog._validate_record(reader, raw, row, None, {}))
    reader._db.operation = (root, "INTERRUPTED", 11)
    refuse(lambda: reader._validate_record(raw, row, None, {}), "PORTABLE_NATIVE_OPERATION_BINDING")
    need(reader._advisory_snapshot is None, "SCOPE_CLEARED_AFTER_REFUSAL")
    reader._db.operation = (root, "COMMITTED", 11)
    bad = deepcopy(row); bad["request_hash"] = "6"*64
    refuse(lambda: reader._validate_record(E.canonical_json(bad), bad, None, {}),
           "PORTABLE_ROOT_INPUT_BINDING")
    bad = deepcopy(row); bad["bindings"].append(deepcopy(bad["bindings"][0]))
    refuse(lambda: reader._validate_record(E.canonical_json(bad), bad, None, {}),
           "PORTABLE_DUPLICATE_BINDING")
    bad = deepcopy(row); bad["snapshot"]["relative_path"] = "imports/../chunk.olean"
    refuse(lambda: reader._validate_record(E.canonical_json(bad), bad, None, {}),
           "ADVISORY_SNAPSHOT_PATH")

    # A complete synthetic imported extension exercises original source-record
    # digest/name/origin checks, while its generated snapshot remains absent.
    import_id, source_store, source_parent = "7"*64, "8"*64, "9"*64
    profile = dict(schema=L.PROFILE, kernel_support="a"*64, adapter_support="b"*64,
        basis_receiver_support="c"*64, basis_seed=L.SEED, basis_inventory=L.INVENTORY,
        expression_format=E.EXPR_FORMAT, declaration_format=E.UNIT_FORMAT,
        axiom_policy="FIXED_BASIS_NO_NEW_AXIOM_UNSAFE_SORRY",
        snapshot_format="LEAN_4_34_MODULEDATA_NO_EXTENSIONS_NO_IR")
    profile_id = L.digest("ordinary-native-profile-v1", profile)
    source_request = "d"*64
    source_root = L.digest("ordinary-extension-root-v1", [profile_id, source_parent, source_request])
    local_root = P.legacy_root_id(reader.semantic_id, reader.foundation_id,
        reader._store_id, import_id, source_root, parent)
    source_doc = dict(root=source_root, profile_id=profile_id, kind="extension", parent=source_parent,
        operation="e"*64, request_hash=source_request, artifact_bytes=11, artifact_sha256="4"*64,
        bindings=[[name("Example.A"), "f"*64]])
    source_raw = E.canonical_json(source_doc)
    folder = directory/"imports"/import_id
    (folder/"0").mkdir(parents=True)
    source_path = folder/"0"/"source-record.json"
    source_path.write_bytes(source_raw)
    legacy = deepcopy(row)
    legacy.update(local_root=local_root, origin="legacy-translation",
        provenance=dict(import_id=import_id, ordinal=0, source_store_id=source_store,
            source_profile_id=profile_id, source_root=source_root, source_parent_root=source_parent,
            source_record_sha256=sha(source_raw), source_operation_id="e"*64,
            source_check_support=["a"*64,"b"*64,"c"*64], translation_support="d"*64))
    legacy["snapshot"].update(module_name=L.module_name(source_root), parent_module=L.module_name(source_parent),
        relative_path="imports/"+import_id+"/0/chunk.olean", writer_origin="retained-v1-check")
    legacy_raw = E.canonical_json(legacy)
    import_doc = dict(schema=P.IMPORT_SCHEMA, import_id=import_id, semantic_id=reader.semantic_id,
        foundation_id=reader.foundation_id, implementation_id=reader.implementation_id,
        store_id=reader._store_id, source_store_id=source_store, source_profile=profile,
        source_selected_root=source_root, source_manifest_sha256="e"*64,
        correspondence_sha256=sha(b"[]"), translation_support="d"*64,
        source_check_support=["a"*64,"b"*64,"c"*64],
        retained_support=sorted(set(reader._current_support+["a"*64,"b"*64,"c"*64,"d"*64])),
        roots=[[local_root,sha(legacy_raw)]],
        audit=dict(relative_path="imports/"+import_id+"/audit.json", artifact_bytes=2,
                   artifact_sha256=sha(b"{}")))
    (folder/"audit.json").write_bytes(b"{}")
    (folder/"correspondence.json").write_bytes(b"[]")
    need(reader._validate_import(E.canonical_json(import_doc)) == import_doc,
         "ACTUAL_IMPORT_METADATA_VALIDATION")
    need(reader._validate_record(legacy_raw, legacy, import_doc, {local_root:sha(legacy_raw)}) ==
         folder/"0"/"chunk.olean", "IMPORTED_SNAPSHOT_BYPASS")
    need(not (folder/"0"/"chunk.olean").exists(), "IMPORTED_SNAPSHOT_ABSENT")
    bad_import = deepcopy(import_doc); bad_import["audit"]["artifact_sha256"] = "0"*64
    refuse(lambda: reader._validate_import(E.canonical_json(bad_import)), "CATALOG_ARTIFACT_DIGEST")
    source_path.write_bytes(b"[]")
    refuse(lambda: reader._validate_record(legacy_raw, legacy, import_doc, {local_root:sha(legacy_raw)}),
           "PORTABLE_SOURCE_RECORD_DIGEST")
    need(reader._advisory_snapshot is None, "LEGACY_SCOPE_CLEARED")
    return "actual-native/import-record-validators:missing-snapshots-succeed;bad-root/operation/duplicate/path/audit/source-refuse"


def projection_case(helper, entry, Q, A, installation, directory, *, mode):
    P, E, S = A.P, A.E, A.S
    requested = [name("Example.A"), name("Example.B")]
    mapping = {E.name_key(requested[0]):"5"*64, E.name_key(requested[1]):"6"*64}
    if mode == "missing":
        del mapping[E.name_key(requested[1])]
    events, evidence = [], []
    selected_root, store_id = "1"*64, "2"*64
    class InertDB:
        operation = None
        def execute(self, sql, parameters=()):
            need(sql == "SELECT root,state,reserved_bytes FROM operations WHERE id=?",
                 "INERT_UNEXPECTED_SQL")
            return NS(fetchone=lambda:self.operation)
        def close(self):
            events.append("db-close")
            if mode == "close-failure":
                raise OSError("INERT_CLOSE_FAILURE")
    def opener(cls, directory, implementation_raw, selected_store, *, create, limits, importing):
        need(create is False and importing is None and selected_store == store_id and
             implementation_raw == installation.implementation_raw, "INERT_OPEN_ARGUMENTS")
        events.append("open")
        reader = cls.__new__(cls)
        reader._root, reader._limits = directory, limits
        reader._implementation_raw, reader._store_id = implementation_raw, selected_store
        reader.semantic_id, reader.foundation_id = installation.semantic_id, S.foundation_id()
        reader.implementation_id = installation.implementation_id
        reader._basis_request = P.basis_request_id(reader.semantic_id, reader.foundation_id)
        reader._current_support = sorted({installation.doc["implementation"][field] for field in P.SUPPORT_FIELDS})
        reader._db, reader._lock, reader._closed = InertDB(), None, False
        reader._verified_artifacts = set()
        if mode == "validators":
            evidence.append(validator_cases(reader, P, installation, directory))
            for method in ("reserve_basis", "reserve_extension", "_reserve", "_commit_checked",
                           "_activate_import", "_flush_import_tree", "_import_active", "abandon"):
                refuse(lambda method=method:getattr(reader,method)(), "ADVISORY_NO_ADMISSION_CAPABILITY")
            refuse(lambda:cls._create_importing(), "ADVISORY_NO_ADMISSION_CAPABILITY")
            refuse(lambda:cls._open(directory, implementation_raw, store_id,
                create=True, limits=limits, importing=None), "ADVISORY_EXISTING_ACTIVE_ONLY")
        def context(root):
            need(root == selected_root, "INERT_EXACT_ROOT")
            events.append("context")
            return dict(local_root=root, semantic_id=reader.semantic_id,
                foundation_id=reader.foundation_id, implementation_id=reader.implementation_id,
                bindings=mapping, modules=["MUST_NOT_ESCAPE"], basis_module=["MUST_NOT_ESCAPE"])
        reader.context = context
        reader._active = lambda:events.append("active")
        return reader
    directory.mkdir()
    with patch.object(P.PortableCatalog, "_open", classmethod(opener)):
        call = lambda:helper.project(installation, directory, store_id, selected_root, requested,
                                    limits=P.Limits(), check=check, catalog_module=P)
        if mode == "close-failure":
            refuse(call, "INERT_CLOSE_FAILURE")
            need(events[-1] == "db-close", "CLOSURE_FAILURE_REACHED")
            return {"mode":mode, "events":events}
        result = call()
    need(events == ["open","context","active","db-close"], "INERT_PROJECTION_LIFECYCLE")
    need(result["owner_closure"] == "CLOSED" and result["snapshot_integrity"] == "NOT_CHECKED" and
         result["context_readiness"] == "NOT_ASSERTED" and result["mathematical_acceptance"] is False,
         "ADVISORY_RESULT_BOUNDARY")
    raw, missing = entry.advisory_projection(Q, result, requested, installation, store_id, selected_root, check)
    if mode == "missing":
        need(raw is None and missing == requested[1:], "MISSING_NO_SUBSET_QUERY")
    else:
        need(missing == [] and json.loads(raw) == [[n,mapping[E.name_key(n)]] for n in requested],
             "EXACT_PROJECTED_ROWS")
        for update, code in (({"modules":[]},"QUERY_ADVISORY_FIELDS"),
                             ({"snapshot_integrity":"CHECKED"},"QUERY_ADVISORY_BOUNDARY"),
                             ({"owner_closure":"NOT_CONFIRMED"},"QUERY_ADVISORY_BOUNDARY"),
                             ({"missing_names":requested},"QUERY_ADVISORY_MISSING_DISAGREEMENT")):
            bad = dict(result, **update)
            refuse(lambda:entry.advisory_projection(Q,bad,requested,installation,store_id,selected_root,check),code)
        bad = dict(result, bindings={**result["bindings"],E.name_key(name("Extra")):"8"*64})
        refuse(lambda:entry.advisory_projection(Q,bad,requested,installation,store_id,selected_root,check),
               "QUERY_ADVISORY_UNREQUESTED_BINDING")
    return {"mode":mode, "events":events, "evidence":evidence}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for option in ("package","profile-sha256","helper","helper-sha256","query","query-sha256","output"):
        parser.add_argument("--"+option, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTROL_PROCESS")
    package, output = Path(args.package), Path(args.output)
    need(package.is_absolute() and output.is_absolute() and output.parent.is_dir() and
         not os.path.lexists(output) and output.resolve().is_relative_to(ROOT/"experiments/v5-local-checks"),
         "CONTROL_FRESH_OUTPUT")
    profile_raw = read(package/"PROFILE.json",args.profile_sha256)
    profile = json.loads(profile_raw)
    manifest_path = package/"installation/INSTALLATION.json"
    manifest_raw = read(manifest_path,profile["installation_manifest_sha256"])
    manifest = json.loads(manifest_raw)
    selected = {}
    for key in ("ordinary_evidence","ordinary_semantics","local_catalog","portable_evidence",
                "portable_catalog","ordinary_admission"):
        relative = "py/"+key+".py"; pin = manifest["files"][relative]
        path = package/"installation"/relative; raw = read(path,pin["sha256"])
        need(len(raw) == pin["bytes"],"CONTROL_CORE_SIZE"); selected[key]=(path,raw)
    for key in ("ordinary_preview","portable_preview","formal_query"):
        relative = "authoring/py/"+key+".py"; pin = profile["files"][relative]
        path = package/relative; raw = read(path,pin["sha256"])
        need(len(raw) == pin["bytes"],"CONTROL_HELPER_SIZE"); selected[key]=(path,raw)
    for key,path,pin in (("_advisory",Path(args.helper),args.helper_sha256),
                         ("_advisory_query",Path(args.query),args.query_sha256)):
        need(path.is_absolute(),"CONTROL_SOURCE_PATH"); selected[key]=(path,read(path,pin))
    need(not any(key in sys.modules for key in selected),"CONTROL_PRELOADED")
    output.mkdir()
    with ExitStack() as stack:
        for target in ("subprocess.Popen","socket.socket","socket.create_connection",
                       "sqlite3.connect","os.system","os.startfile"):
            stack.enter_context(patch(target,forbidden))
        for key,(path,raw) in selected.items():
            spec=importlib.util.spec_from_file_location(key,path); module=importlib.util.module_from_spec(spec)
            stack.enter_context(patch.dict(sys.modules,{key:module}))
            exec(compile(raw,str(path),"exec"),module.__dict__)
        A,Q,helper,entry=(sys.modules[key] for key in
                         ("ordinary_admission","formal_query","_advisory","_advisory_query"))
        installation=A.NativeInstallation.__new__(A.NativeInstallation)
        installation.root=package/"installation"; installation.runtime_roots={}
        installation.doc=manifest
        installation.implementation_raw=A.E.canonical_json(manifest["implementation"])
        installation.implementation_id=A.S.implementation_id(installation.implementation_raw)
        installation.semantic_id=A.S.semantic_id()
        cases=[projection_case(helper,entry,Q,A,installation,output/mode,mode=mode)
               for mode in ("validators","missing","close-failure")]
        for values,code in ((dict(custody="x",custody_limits="y"),"QUERY_CONTEXT_ARGUMENTS"),
                            (dict(native_type="x"),"QUERY_EXACTLY_ONE_INPUT_KIND")):
            args0=NS(bindings=None,context_root="1"*64,catalog="x",store_id="2"*64,
                     custody=None,custody_limits=None,symbol_names="names",native_type=None)
            vars(args0).update(values)
            refuse(lambda:entry.query_kind(args0),code)
        cases.append({"mode":"advisory-arguments-refuse-custody-and-mixed-input"})
    check()
    for path,raw in selected.values():
        need(read(path)==raw,"CONTROL_SOURCE_CHANGED")
    need(read(package/"PROFILE.json")==profile_raw and read(manifest_path)==manifest_raw,
         "CONTROL_PACKAGE_CHANGED")
    result=dict(status="PASS_ADVISORY_QUERY_INERT_CONTROLS",groups=len(cases),cases=cases,
        profile_sha256=args.profile_sha256,
        source_pins={key:dict(path=str(path),bytes=len(raw),sha256=sha(raw)) for key,(path,raw) in selected.items()},
        wall_seconds=time.monotonic()-START,cpu_seconds=time.process_time()-CPU,
        scope="REAL_RECORD_VALIDATORS_SYNTHETIC_METADATA_INERT_OPEN_SQL_ACTIVATION_NO_ACCEPTANCE")
    raw=json.dumps(result,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",",":")).encode()
    with (output/"RESULT.json").open("xb") as stream:
        stream.write(raw)
    print(raw.decode(),flush=True)


if __name__ == "__main__":
    main()

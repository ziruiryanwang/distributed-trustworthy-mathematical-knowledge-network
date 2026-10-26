"""Finite native-free controls; source only until root selects execution.

Synthetic custody has no accepted owner/catalog. False but structurally valid
claims deliberately distinguish inert export from mathematical acceptance.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
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
from types import SimpleNamespace
from unittest.mock import patch

START, CPU = time.monotonic(), time.process_time()
MIB = 1024**2
PROFILE = "b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7"
INSTALL = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
STORE_LIMITS = dict(objects=4096, exports=65536, logical_bytes=64*MIB, db_pages=32768)
LIMITS = dict(units=1024, bytes=64*MIB, nodes=2097152, names=65536,
              edges=262144, locator_reads=65536, locator_bytes=64*MIB, output_bytes=68*MIB)
MODULES = {
    "ordinary_evidence": "installation/py/ordinary_evidence.py",
    "ordinary_semantics": "installation/py/ordinary_semantics.py",
    "portable_evidence": "installation/py/portable_evidence.py",
    "portable_candidate": "authoring/py/portable_candidate.py",
    "baseline_bundle": "reference/baseline_bundle.py",
    "ordinary_preview": "authoring/py/ordinary_preview.py",
    "portable_preview": "authoring/py/portable_preview.py",
}


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 150 and time.process_time()-CPU < 70,
         "TEST_ORIGINAL_BUDGET")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def raw(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def load(label, path):
    need(label not in sys.modules, "TEST_MODULE_PRELOADED:"+label)
    spec = importlib.util.spec_from_file_location(label, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[label] = module
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def fixture_name(label):
    return [[0, {"$bytes": list(part.encode())}] for part in label.split(".")]


def codec_api(package):
    profile_raw = (package/"PROFILE.json").read_bytes()
    install_raw = (package/"installation/INSTALLATION.json").read_bytes()
    need(sha(profile_raw) == PROFILE and sha(install_raw) == INSTALL, "TEST_APPROVED_PACKAGE")
    profile, install = json.loads(profile_raw), json.loads(install_raw)
    loaded = {}
    for name, relative in MODULES.items():
        path = package/relative
        pin = (install["files"][relative[len("installation/"):]] if relative.startswith("installation/")
               else profile["files"][relative])
        data = path.read_bytes()
        need(dict(bytes=len(data), sha256=sha(data)) == pin, "TEST_CODEC_PIN:"+name)
        loaded[name] = load(name, path)
    api = SimpleNamespace(E=loaded["ordinary_evidence"], S=loaded["ordinary_semantics"],
        PE=loaded["portable_evidence"], B=loaded["baseline_bundle"], PP=loaded["portable_preview"])
    inventory = (package/"installation/foundation/inventory.json").read_bytes()
    need(sha(inventory) == api.S.INVENTORY, "TEST_INVENTORY_PIN")
    return api, inventory


def make_unit(api, label, dependency=None, *, theorem=False, value=0):
    E, S, PE = api.E, api.S, api.PE
    name = fixture_name(label)
    typ_name = fixture_name("False" if theorem else "Nat")
    typ = [E.EXPR_FORMAT, [], [[2, typ_name, []]], 0]
    imports = [[typ_name, S.basis_symbol_id(S.semantic_id(), S.foundation_id(), typ_name)]]
    if dependency is not None:
        body = [E.EXPR_FORMAT, [], [[2, dependency["name"], []]], 0]
        imports.append([dependency["name"], dependency["export_id"]])
    else:
        body = [E.EXPR_FORMAT, [], [[7, {"$bytes": [] if value == 0 else [value]}]], 0]
    # The theorem claims False with a Nat-valued body. Export is NOT admission.
    if theorem:
        unit = [E.UNIT_FORMAT, [1, name, [], typ, body, [name]],
                [[name, 2, [], typ, [body, [name]]]]]
    else:
        unit = [E.UNIT_FORMAT, [0, name, [], typ, body, [2, 1], [name]],
                [[name, 1, [], typ, [body, [2, 1], [name]]]]]
    data = E.canonical_json(dict(schema=PE.SCHEMA, semantic_id=S.semantic_id(),
        imports=sorted(imports, key=lambda row:E.name_key(row[0])), unit=unit))
    parsed = PE.read_evidence(data)
    return data, dict(name=name, unit_id=parsed.unit_id,
                     export_id=S.export_id(S.semantic_id(), parsed.unit_id, name))


def make_group(api):
    E, S = api.E, api.S
    names = [fixture_name("SyntheticGroup.First"), fixture_name("SyntheticGroup.Second")]
    typ = [E.EXPR_FORMAT, [[0]], [[1, 0]], 0]
    unit = [E.UNIT_FORMAT, [3, [], 0, [[n, typ, []] for n in names]],
            [[n, 4, [], typ, [0, 0, names, [], 0, 0, 0, 0]] for n in names]]
    data = E.canonical_json(dict(schema=api.PE.SCHEMA, semantic_id=S.semantic_id(), imports=[], unit=unit))
    parsed = api.PE.read_evidence(data)
    targets = [dict(name=n, unit_id=parsed.unit_id,
                    export_id=S.export_id(S.semantic_id(), parsed.unit_id, n)) for n in names]
    return data, targets


def create_custody(path, api, units):
    """Real SQLite format; explicitly synthetic, never an accepted owner."""
    path.mkdir()
    db = sqlite3.connect(path/"ordinary.sqlite")
    db.executescript("""
      CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), cfg BLOB NOT NULL,
        objects INTEGER NOT NULL, exports INTEGER NOT NULL, logical_bytes INTEGER NOT NULL);
      CREATE TABLE objects(kind TEXT NOT NULL, identity TEXT NOT NULL, raw_sha256 TEXT NOT NULL,
        raw BLOB NOT NULL, PRIMARY KEY(kind,identity)) WITHOUT ROWID;
      CREATE TABLE exports(export_id TEXT PRIMARY KEY, unit_id TEXT NOT NULL,
        locator BLOB NOT NULL) WITHOUT ROWID;
    """)
    count, byte_count = 0, 0
    for data in units:
        parsed = api.PE.read_evidence(data)
        db.execute("INSERT INTO objects VALUES(?,?,?,?)", ("evidence", parsed.unit_id, sha(data), data))
        byte_count += len(data)+len("evidence")+128
        for row in parsed.document["unit"][2]:
            locator = raw(dict(schema=api.PP.LOCATOR_SCHEMA, semantic_id=api.S.semantic_id(),
                               unit_id=parsed.unit_id, export_name=row[0]))
            symbol = api.S.export_id(api.S.semantic_id(), parsed.unit_id, row[0])
            db.execute("INSERT INTO exports VALUES(?,?,?)", (symbol, parsed.unit_id, locator))
            count += 1
            byte_count += 128+len(locator)
    cfg = raw(dict(schema="DMKN_ORDINARY_INERT_CUSTODY_V1", semantic_id=api.S.semantic_id(), limits=STORE_LIMITS))
    db.execute("INSERT INTO meta VALUES(1,?,?,?,?)", (cfg, len(units), count, byte_count))
    db.commit()
    db.close()


def validate_output(path, api, expected):
    manifest_raw = (path/"manifest.json").read_bytes()
    manifest = api.B.read_manifest(manifest_raw, sha(manifest_raw))
    got = []
    for entries in manifest.batches:
        data = tuple((path/entry.relative_path).read_bytes() for entry in entries)
        api.B.validate_batch(entries, data)
        got.extend(data)
    need(got == expected, "TEST_EXACT_TOPOLOGICAL_BUNDLE")
    result = json.loads((path/"RESULT.json").read_bytes())
    need(result["mathematical_acceptance"] is False, "TEST_INERT_ASSURANCE")
    need(manifest.unit_count == len(expected), "TEST_NO_UNRELATED_UNITS")
    return result


def refuses(action, fragment):
    try:
        action()
    except (ValueError, sqlite3.Error) as error:
        need(fragment in str(error), "TEST_WRONG_REFUSAL:"+str(error))
        return str(error)
    raise AssertionError("TEST_MISSING_REFUSAL:"+fragment)


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--package", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--python-runtime", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "TEST_RUNTIME_PROFILE")
    root = Path(args.output)
    need(root.is_absolute() and not root.exists() and root.parent.is_dir(), "TEST_FRESH_OUTPUT")
    root.mkdir()
    package = Path(args.package)
    api, inventory = codec_api(package)
    helper = load("_selected_export_test_helper", Path(__file__).with_name("selected_export.py"))
    first, a = make_unit(api, "Fixture.First")
    second, b = make_unit(api, "Fixture.Second", a)
    theorem, t = make_unit(api, "Fixture.UnprovedFalse", b, theorem=True)
    unrelated, _ = make_unit(api, "Fixture.Unrelated")
    group, group_targets = make_group(api)
    custody = root/"custody"
    create_custody(custody, api, [first, second, theorem, unrelated, group])
    before = (custody/"ordinary.sqlite").read_bytes()
    groups = []

    def export(targets, leaf, *, selected_custody=custody, limits=None, selected_inventory=inventory):
        return helper.export_selected(selected_custody, targets, root/leaf, api=api,
            inventory_raw=selected_inventory, custody_limits=STORE_LIMITS,
            limits=LIMITS if limits is None else limits, check_budget=check, protected_paths=(package,))

    def forbidden(*unused_args, **unused_kwargs):
        raise AssertionError("TEST_UNEXPECTED_NETWORK_OR_NATIVE_PROCESS")

    # Direct controls have no right to launch anything or connect to a peer.
    with ExitStack() as guard:
        for target in ("socket.create_connection", "socket.socket", "subprocess.Popen", "os.system"):
            guard.enter_context(patch(target, forbidden))
        export([t], "chain")
        validate_output(root/"chain", api, [first, second, theorem])
        groups.append("full_import_closure_including_proof_only_and_inert_false_claim")
        export([group_targets[0]], "group")
        validate_output(root/"group", api, [group])
        need(len(api.PE.read_evidence(group).document["unit"][2]) == 2, "TEST_GROUP_SIBLINGS")
        groups.append("complete_group_without_unrelated_custody")
        refuses(lambda: export([], "empty"), "TARGET")
        refuses(lambda: export([t,t], "duplicate"), "TARGET")
        wrong = deepcopy(t); wrong["export_id"] = "0"*64
        refuses(lambda: export([wrong], "wrong-target"), "TARGET")
        refuses(lambda: export([t], "unit-bound", limits={**LIMITS, "units":1}), "BOUND")
        refuses(lambda: export([t], "byte-bound", limits={**LIMITS, "bytes":1}), "BOUND")
        refuses(lambda: export([t], "node-bound", limits={**LIMITS, "nodes":1}), "CLOSURE_CENSUS")
        refuses(lambda: export([t], "name-bound", limits={**LIMITS, "names":1}), "BOUND")
        refuses(lambda: export([t], "edge-bound", limits={**LIMITS, "edges":1}), "CLOSURE_CENSUS")
        refuses(lambda: export([t], "locator-bound", limits={**LIMITS, "locator_reads":1}), "LOCATOR_READ_BOUND")
        refuses(lambda: export([t], "locator-byte-bound", limits={**LIMITS, "locator_bytes":1}), "LOCATOR_UNAVAILABLE_OR_BOUND")
        refuses(lambda: export([t], "output-bound", limits={**LIMITS, "output_bytes":1}), "OUTPUT_BYTE_BOUND")
        need((root/"output-bound").is_dir() and not (root/"output-bound/RESULT.json").exists(),
             "TEST_PARTIAL_OUTPUT_PRESERVED_WITHOUT_SUCCESS")
        refuses(lambda: export([t], "bad-inventory", selected_inventory=b"[]"), "INVENTORY")
        refuses(lambda: export([t], "chain"), "FRESH")
        groups.append("target_identity_capacity_inventory_and_overwrite_refusals")

        absent = root/"missing-custody"
        create_custody(absent, api, [theorem])
        refuses(lambda: export([t], "missing", selected_custody=absent), "LOCATOR_UNAVAILABLE_OR_BOUND")

        def damaged(label, sql, values, marker):
            selected = root/(label+"-custody")
            create_custody(selected, api, [first, second, theorem])
            db = sqlite3.connect(selected/"ordinary.sqlite")
            db.execute(sql, values); db.commit(); db.close()
            old = (selected/"ordinary.sqlite").read_bytes()
            refuses(lambda: export([t], label, selected_custody=selected), marker)
            need((selected/"ordinary.sqlite").read_bytes() == old, "TEST_DAMAGED_INPUT_CHANGED")
        damaged("digest", "UPDATE objects SET raw_sha256=? WHERE identity=?", ("f"*64,t["unit_id"]),
                "EVIDENCE_RAW_BINDING")
        damaged("content-id", "UPDATE objects SET raw=?,raw_sha256=? WHERE identity=?",
                (first,sha(first),t["unit_id"]), "EVIDENCE_IDENTITY")
        bad_locator = raw(dict(schema=api.PP.LOCATOR_SCHEMA, semantic_id=api.S.semantic_id(),
                              unit_id=t["unit_id"], export_name=a["name"]))
        damaged("locator", "UPDATE exports SET locator=? WHERE export_id=?", (bad_locator,t["export_id"]),
                "LOCATOR_BINDING")

        def from_document(document):
            data = api.E.canonical_json(document)
            parsed = api.PE.read_evidence(data)
            name = parsed.document["unit"][2][0][0]
            return data, dict(name=name, unit_id=parsed.unit_id,
                export_id=api.S.export_id(api.S.semantic_id(), parsed.unit_id, name))
        doc = json.loads(first); doc["semantic_id"] = "f"*64
        bad_raw, bad_target = from_document(doc)
        selected = root/"semantic-custody"; create_custody(selected, api, [bad_raw])
        refuses(lambda: export([bad_target], "semantic", selected_custody=selected), "EVIDENCE_IDENTITY")
        doc = json.loads(first); doc["imports"][0][1] = "f"*64
        bad_raw, bad_target = from_document(doc)
        selected = root/"basis-custody"; create_custody(selected, api, [bad_raw])
        refuses(lambda: export([bad_target], "basis", selected_custody=selected), "BASIS_IMPORT_MISMATCH")
        alternative, alternative_target = make_unit(api, "Fixture.First", value=1)
        other, other_target = make_unit(api, "Fixture.Other", alternative_target)
        selected = root/"conflict-custody"
        create_custody(selected, api, [first,second,theorem,other])
        refuses(lambda: export([t,other_target], "conflict", selected_custody=selected), "CONFLICT")
        groups.append("missing_corrupt_locator_identity_semantic_basis_and_name_conflict_refusals")

        for suffix in ("-journal", "-wal", "-shm"):
            selected = root/("sidecar"+suffix)
            create_custody(selected, api, [first])
            sidecar = selected/("ordinary.sqlite"+suffix)
            sidecar.write_bytes(b"TEST_REJECT_WITHOUT_RECOVERY")
            old = (selected/"ordinary.sqlite").read_bytes()
            refuses(lambda: export([a], "refused"+suffix, selected_custody=selected), "SOURCE_NEEDS_RECOVERY")
            need((selected/"ordinary.sqlite").read_bytes() == old and
                 sidecar.read_bytes() == b"TEST_REJECT_WITHOUT_RECOVERY", "TEST_SIDECAR_MUTATED")
        refuses(lambda: helper.export_selected(custody,[a],custody/"output",api=api,
            inventory_raw=inventory,custody_limits=STORE_LIMITS,limits=LIMITS,check_budget=check),
            "OUTPUT_OVERLAP")
        groups.append("journal_sidecar_and_overlap_fail_closed")

        counts = dict(units=0,evidence_bytes=0,nodes=0,names=0,edges=0,locator_reads=0,locator_bytes=0)
        reader = helper.ReadCustody(custody, api.S.semantic_id(), STORE_LIMITS, api,LIMITS,counts,check)
        try:
            refuses(lambda: reader.db.execute("UPDATE meta SET objects=objects"), "readonly")
            writer = sqlite3.connect(custody/"ordinary.sqlite", timeout=0)
            try:
                writer.execute("BEGIN IMMEDIATE")
                writer.execute("UPDATE meta SET objects=objects+1")
                refuses(writer.commit, "locked")
                need(reader.one("SELECT objects FROM meta WHERE id=1") == (5,), "TEST_STABLE_SNAPSHOT")
            finally:
                writer.rollback(); writer.close()
        finally:
            reader.close()
        need(reader.db is None, "TEST_READER_CLOSED")
        groups.append("actual_readonly_connection_and_snapshot_writer_contention")

    need((custody/"ordinary.sqlite").read_bytes() == before, "TEST_CUSTODY_CHANGED")
    need(sorted(p.name for p in custody.iterdir()) == ["ordinary.sqlite"], "TEST_CUSTODY_SIDECARS")
    groups.append("custody_bytes_unchanged")

    request = dict(schema="DMKN_SELECTED_INERT_EXPORT_REQUEST_V1", custody=str(custody),
        targets=[t], output=str(root/"cli-bundle"), custody_limits=STORE_LIMITS, limits=LIMITS)
    request_path = root/"request.json"
    request_path.write_bytes(raw(request))
    entry = Path(__file__).with_name("export.py")
    helper_path = Path(__file__).with_name("selected_export.py")
    argv = [sys.executable, "-I", "-S", "-B", str(entry), "--package", str(package),
        "--profile-sha256", PROFILE, "--python-runtime", args.python_runtime,
        "--entry-sha256", sha(entry.read_bytes()), "--helper-sha256", sha(helper_path.read_bytes()),
        "--request", str(request_path), "--request-sha256", sha(request_path.read_bytes()),
        "--diagnostics", str(root/"cli-diagnostics"), "--wall-seconds", "75", "--cpu-seconds", "45",
        "--memory-mib", "768", "--active-processes", "1", "--stdout-bytes", str(MIB),
        "--stderr-bytes", str(MIB)]
    with (root/"cli-stdout.txt").open("xb") as stdout, (root/"cli-stderr.txt").open("xb") as stderr:
        outcome = subprocess.run(argv, cwd=root, stdout=stdout, stderr=stderr, timeout=90, check=False)
    need(outcome.returncode == 0, "TEST_PUBLIC_CLI_FAILED")
    launch = json.loads((root/"cli-stdout.txt").read_bytes())
    need(launch["ok"] is True and launch["status"] == "INERT_EXPORT_COMPLETE" and
         launch["mathematical_acceptance"] is False, "TEST_PUBLIC_CLI_REPORT")
    supervision = json.loads((root/"cli-diagnostics/SUPERVISION.json").read_bytes())
    need(supervision["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and
         supervision["direct_child_reaped"] is True and supervision["job_closed"] is True and
         supervision["child_exit_code"] == 0 and supervision["termination_requested"] is False and
         supervision["cleanup_errors"] == [] and supervision["final_job"]["active_processes"] == 0 and
         supervision["final_job"]["terminated_processes"] == 0, "TEST_ACTUAL_CLI_CLEAN_CLOSURE")
    worker = json.loads((root/"cli-diagnostics/WORKER.json").read_bytes())
    need(worker["ok"] is True and worker["supervised_completion"] is False and
         worker["result"]["source_acceptance"] == "UNASSERTED", "TEST_WORKER_IS_NOT_SUPERVISION")
    validate_output(root/"cli-bundle", api, [first, second, theorem])
    need((custody/"ordinary.sqlite").read_bytes() == before, "TEST_CLI_CUSTODY_CHANGED")
    groups.append("actual_public_companion_and_unchanged_baseline_format")
    result = dict(status="PASS_SELECTED_EXPORT_DATA_CONTROLS", groups=groups,
        mathematical_acceptance=False, native_executions=0, network_operations=0,
        fixture="SYNTHETIC_INERT_CUSTODY_NO_CATALOG_NO_ACCEPTANCE",
        wall_seconds=time.monotonic()-START, controller_cpu_seconds=time.process_time()-CPU)
    (root/"TEST-RESULT.json").write_bytes(raw(result))
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()

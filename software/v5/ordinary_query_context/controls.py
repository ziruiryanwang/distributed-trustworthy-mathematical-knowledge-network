"""Focused context-query controls: pure bindings and explicitly inert lifecycle.

The preserved Q implementation performs syntax/binding/query operations. Owner,
custody, profile and path-validation doubles in lifecycle cases supply NO real
state or mathematical authority. Only fresh test-output files are written. This
is not a real owner integration, native check, admission or acceptance campaign.
Root selection and an enclosing supervisor are required before execution.
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
from types import SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
START, CPU = time.monotonic(), time.process_time()
MIB = 1024**2
PINS = {
    "ordinary_evidence": "fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6",
    "ordinary_semantics": "ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915",
    "ordinary_preview": "0fd9bb516fbb53d9d4264271853904e35810286fc92d5670d15d7a9d3c26b0d6",
    "portable_evidence": "f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8",
    "portable_preview": "b78dd54340b7b55e4359769d6784f7f225ba304457ce880ce2760717e865550d",
    "formal_query": "7901236768784a399f9ae5c56b374d040bce56536b0a47a6ee85093440cabcee",
    "_context_query_entry": "449b5fea77f4c19cfbde47346ea255ae1277a1cf53e3030a6baa9de3f8659af6",
}
FIXTURE_PINS = {
    "query-local/native-type.json": "226bb411b2a7255eabc522f482afd2c199877ad624737fddf7b27ec0f8658480",
    "fixtures/known-bindings.json": "0ebd5b6de9942a1f9359e23c4d7a36219d30bd71af69c73813de8cfd03d95f2f",
    "query-prepared/QUERY.json": "eb611ed660111779f3bf1a05c044c2a362735d08eb91f7a6151ea80d9108c16a",
}


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 35 and time.process_time()-CPU < 20,
         "CONTEXT_CONTROLS_ORIGINAL_ALLOWANCE")


def forbidden(*_, **__):
    raise AssertionError("CONTEXT_CONTROLS_FORBIDDEN_EXTERNAL_CALL")


def raw(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def pinned(path, digest):
    need(path.is_absolute() and ".." not in path.parts and
         path.resolve(strict=True).is_relative_to(ROOT), "CONTEXT_CONTROLS_LOCAL_PIN")
    with path.open("rb") as stream:
        value = stream.read(MIB+1)
    need(0 < len(value) <= MIB and hashlib.sha256(value).hexdigest() == digest,
         "CONTEXT_CONTROLS_BYTE_PIN:"+str(path))
    return value


def refuse(code, call):
    try:
        call()
    except ValueError as error:
        need(str(error) == code, "CONTEXT_CONTROLS_WRONG_REFUSAL:"+str(error))
    else:
        raise AssertionError("CONTEXT_CONTROLS_MISSING_REFUSAL:"+code)


def inert_lifecycle(entry, Q, native_raw, binding_map, expected_query, output, mode):
    """Test sequencing/output only. All owner/path/profile APIs below are doubles."""
    events = []
    destination = output/mode
    fake = output/"nonexistent-inert-state"
    native_path, limits_path = fake/"native.json", fake/"limits.json"
    catalog_path, custody_path = fake/"catalog", fake/"custody"
    semantic = Q.S.semantic_id()
    context_id, store_id, implementation = "1"*64, "2"*64, "3"*64
    context = {"local_root": context_id, "semantic_id": semantic,
        "foundation_id": Q.S.foundation_id(), "implementation_id": implementation,
        "bindings": {} if mode == "inert-missing" else binding_map}
    if mode == "inert-context-mismatch":
        context["local_root"] = "5"*64
    inputs = {native_path: native_raw, limits_path: raw({"cap": 1}),
        catalog_path/"ADOPTION.json": raw({"schema": "INERT_ADOPTION_NOT_REAL_STATE",
            "store_id": store_id, "implementation": implementation, "limits": {}})}

    def read(path, maximum):
        value = inputs[path]
        need(len(value) <= maximum, "INERT_INPUT_BOUND")
        return value

    def close(label):
        events.append(label+"-close")
        if mode == "inert-close-failure":
            raise OSError("INERT_"+label.upper()+"_CLOSE")

    def opened_store(*args, **kwargs):
        need(args == (custody_path, semantic, {"cap": 1}) and kwargs == {"create": False},
             "INERT_CUSTODY_REOPEN_ARGUMENTS")
        events.append("custody-open")
        return custody

    def opened_owner(*args, **kwargs):
        need(args == (installation, catalog_path, store_id, custody) and
             kwargs == {"create": False, "limits": {}}, "INERT_OWNER_REOPEN_ARGUMENTS")
        events.append("owner-open")
        return owner

    def selected_context(root):
        need(root == context_id, "INERT_SELECTED_CONTEXT_ROOT")
        events.append("context")
        return context

    def write(path, value):
        need(events.count("owner-close") == events.count("custody-close") == 1 and
             events.index("owner-close") < events.index("custody-close"), "WRITE_BEFORE_BOTH_CLOSE")
        need(path.parent == destination, "INERT_WRITE_OUTSIDE_FRESH_TEST_OUTPUT")
        events.append("write:"+path.name)
        with path.open("xb") as stream:
            stream.write(value)
            stream.flush()
            os.fsync(stream.fileno())

    installation = NS(semantic_id=semantic, implementation_id=implementation,
        runtime_roots={}, doc={"implementation": implementation})
    custody = NS(close=lambda: close("custody"))
    owner = NS(catalog=NS(context=selected_context), close=lambda: close("owner"))
    # These deliberately do not validate real paths, adoption policy or state.
    P = NS(SCHEMA="INERT_ADOPTION_NOT_REAL_STATE", fields=lambda *a: None,
        uint=lambda *a: None, Limits=lambda **kw: kw, PortableCatalog=NS(_write_fresh=write))
    C = NS(ordinary=lambda path, **kw: path, read_bounded=read, hexid=Q.E._hex)
    A = NS(E=Q.E, S=Q.S, P=P, C=C, _writer_json=lambda value, maximum: json.loads(value),
        OrdinaryAdmission=NS(open=opened_owner))
    O = NS(STORE_LIMITS={"cap": (1, 2)}, OrdinaryStore=opened_store)
    allocation = NS(deadline=START+35, check=check,
        report=lambda: {"scope": "INERT_ALLOCATION_NOT_REAL_OWNER_ACCOUNTING"})
    loaded = NS(A=A, O=O, formal_query=Q, installation=installation,
        profile=NS(verify=lambda check: (check(), events.append("profile-verify"))))
    base = NS(Allowance=lambda args: allocation, separated=lambda *a: None,
        bootstrap=lambda *a: NS(load=lambda *a, **kw: loaded))
    adapter = NS(Q=Q, namespace_for=lambda semantic: "INERT_NAMESPACE",
        compile_query=lambda namespace, specs: ["INERT_FEATURE_NOT_REAL_DISCOVERY"])
    args = NS(bindings=None, context_root=context_id, catalog=str(catalog_path),
        custody=str(custody_path), store_id=store_id, custody_limits=str(limits_path),
        native_type=str(native_path), output=str(destination), profile_sha256="4"*64,
        python_runtime="INERT", lean_runtime="INERT", wall_seconds=35, cpu_seconds=20,
        memory_mib=256)
    original_rename = Path.rename

    def rename_then_throw(path, target):
        need(path == destination/".RESULT.pending" and target == destination/"RESULT.json",
             "INERT_RENAME_TARGET")
        original_rename(path, target)
        raise OSError("INERT_RENAME_COMPLETED_THEN_UNKNOWN")

    with ExitStack() as stack:
        stack.enter_context(patch.object(entry, "bootstrap_owner", lambda *a: base))
        stack.enter_context(patch.dict(sys.modules, {"discovery.ordinary_export_adapter": adapter}))
        if mode == "inert-rename-unknown":
            stack.enter_context(patch.object(Path, "rename", rename_then_throw))
        result, returned_raw = entry.run_context(args)
    need(json.loads(returned_raw) == result and result["mathematical_acceptance"] is False,
         "INERT_RETURNED_REPORT")
    need(events.count("owner-close") == events.count("custody-close") == 1,
         "INERT_BOTH_CLOSE_ATTEMPTED")
    if mode == "inert-context-mismatch":
        need(result["ok"] is False and result["phase"] == "RESOLVE_CONTEXT" and
             result["error"] == "QUERY_CONTEXT_IDENTITY" and not destination.exists(),
             "INERT_CONTEXT_MISMATCH_CLOSED_NO_OUTPUT")
    elif mode == "inert-missing":
        need(result["ok"] is False and result["status"] == "UNMAPPED_REFERENCES" and
             result["missing_names"] == Q.reference_names(native_raw) and not destination.exists(),
             "INERT_MISSING_NO_OUTPUT")
    elif mode == "inert-close-failure":
        need(result["ok"] is False and result["status"] == "FAILED_OWNER_CLOSURE" and
             [item["component"] for item in result["close_errors"]] == ["owner", "custody"] and
             not destination.exists(), "INERT_CLOSE_ERRORS_NO_OUTPUT")
    else:
        need((destination/"QUERY.json").read_bytes() == expected_query,
             "INERT_OUTPUT_QUERY_AGREEMENT")
        need([event for event in events if event.startswith("write:")] ==
             ["write:BINDINGS.json", "write:QUERY.json", "write:SPECS.json", "write:.RESULT.pending"],
             "INERT_OUTPUT_ORDER")
        need(sorted(path.name for path in destination.iterdir()) ==
             ["BINDINGS.json", "QUERY.json", "RESULT.json", "SPECS.json"], "INERT_OUTPUT_CENSUS")
        saved = (destination/"RESULT.json").read_bytes()
        need(json.loads(saved)["ok"] is True, "INERT_FINAL_MARKER")
        if mode == "inert-rename-unknown":
            need(result["ok"] is False and result["result_publication"] == "UNKNOWN" and
                 result["attempted_result_sha256"] == hashlib.sha256(saved).hexdigest(),
                 "INERT_UNKNOWN_PRESERVES_ATTEMPTED_HASH")
        else:
            need(result["ok"] is True and saved == returned_raw, "INERT_SUCCESS_PUBLICATION")
    return {"events": events, "result": result,
            "authority": "EXPLICIT_INERT_DOUBLES_NO_REAL_STATE_OR_ACCEPTANCE"}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for option in ("helpers", "formal-query", "fixtures", "output"):
        parser.add_argument("--"+option, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTEXT_CONTROLS_PROCESS")
    output = Path(args.output)
    need(output.is_absolute() and ".." not in output.parts and output.parent.is_dir() and
         output.resolve().is_relative_to(ROOT/"experiments/v5-local-checks") and
         not os.path.lexists(output), "CONTEXT_CONTROLS_FRESH_OUTPUT")
    paths = {key: Path(args.helpers)/(key+".py") for key in list(PINS)[:5]}
    paths.update(formal_query=Path(args.formal_query),
                 _context_query_entry=Path(__file__).absolute().with_name("query.py"))
    selected = {key: pinned(paths[key], digest) for key, digest in PINS.items()}
    fixture_paths = {key: Path(args.fixtures)/key for key in FIXTURE_PINS}
    fixtures = {key: pinned(fixture_paths[key], digest) for key, digest in FIXTURE_PINS.items()}
    need(not any(key in sys.modules for key in PINS), "CONTEXT_CONTROLS_CLEAN_MODULES")
    output.mkdir()
    cases = []

    def case(label, call):
        check()
        cases.append({"case": label, "outcome": "PASS", "detail": call()})

    with ExitStack() as stack:
        for target in ("subprocess.Popen", "socket.socket", "socket.create_connection",
                       "sqlite3.connect", "os.system", "os.startfile"):
            stack.enter_context(patch(target, forbidden))
        modules = {}
        for key, value in selected.items():
            check()
            spec = importlib.util.spec_from_file_location(key, paths[key])
            module = importlib.util.module_from_spec(spec)
            stack.enter_context(patch.dict(sys.modules, {key: module}))
            modules[key] = module
            exec(compile(value, str(paths[key]), "exec"), module.__dict__)
        Q, entry = modules["formal_query"], modules["_context_query_entry"]
        native_raw = fixtures["query-local/native-type.json"]
        bindings_raw = fixtures["fixtures/known-bindings.json"]
        expected_query = fixtures["query-prepared/QUERY.json"]
        rows = json.loads(bindings_raw)
        names = [row[0] for row in rows]
        keys = [Q.E.name_key(name, Q.DEFAULT_LIMITS.codec) for name in names]
        need(len(rows) == 4 and Q.reference_names(native_raw) == names, "SAVED_REFERENCE_CENSUS")
        # Reverse insertion order and add malformed unrelated metadata. Resolution
        # must select only query references, in the saved actual-Q order.
        mapping = {key: row[1] for key, row in reversed(list(zip(keys, rows)))}
        mapping[b"unrelated-not-a-query-name"] = "NOT_A_SYMBOL_ID"

        def exact():
            bound, missing = entry.resolve_context_bindings(Q, native_raw, mapping, check)
            need(missing == [] and bound == bindings_raw, "EXACT_ORDERED_BINDING_BYTES")
            query = Q.bind_native_type(native_raw, bound, semantic_id=Q.S.semantic_id())
            need(query == expected_query, "SAVED_MANUAL_QUERY_BYTE_AGREEMENT")
            return {"references": len(rows), "query_sha256": hashlib.sha256(query).hexdigest()}
        case("ordered-exact-bindings-and-saved-query", exact)

        def missing():
            for subset, expected in (({}, names), ({keys[0]: rows[0][1]}, names[1:])):
                bound, absent = entry.resolve_context_bindings(Q, native_raw, subset, check)
                need(bound is None and absent == expected, "ALL_MISSING_NO_PARTIAL_BINDINGS")
            return {"all_missing": names, "partly_missing": names[1:]}
        case("all-and-partly-missing-without-partial-output", missing)

        def invalid():
            broken = dict(mapping)
            broken[keys[1]] = "malformed"
            refuse("HASH_ENCODING", lambda: entry.resolve_context_bindings(Q, native_raw, broken, check))
            refuse("QUERY_CONTEXT_BINDING_MAP", lambda: entry.resolve_context_bindings(Q, native_raw, [], check))
            refuse("QUERY_CONTEXT_BINDING_MAP", lambda: entry.resolve_context_bindings(Q, native_raw, {}, None))
            return {"refusals": ["HASH_ENCODING", "QUERY_CONTEXT_BINDING_MAP"]}
        case("malformed-present-id-and-invalid-map-callback", invalid)

        def zero():
            zero_raw = raw([Q.NATIVE_SCHEMA, [], [Q.E.EXPR_FORMAT, [], [[7, {"$bytes": [1]}]], 0]])
            bound, absent = entry.resolve_context_bindings(Q, zero_raw, mapping, check)
            need(bound == b"[]" and absent == [], "ZERO_REFERENCE_BINDINGS")
            Q.read_query(Q.bind_native_type(zero_raw, bound, semantic_id=Q.S.semantic_id()))
            return {"native_utf8": zero_raw.decode(), "authority": "INERT_SYNTAX_NOT_CHECKED_TYPE"}
        case("zero-reference-inert-query", zero)

        def allowance():
            calls = []
            def counted():
                calls.append(1)
                check()
            entry.resolve_context_bindings(Q, native_raw, mapping, counted)
            need(len(calls) == len(rows)+1, "PER_REFERENCE_AND_TERMINAL_ALLOWANCE_CHECK")
            calls.clear()
            def exhausted():
                calls.append(1)
                if len(calls) == 2:
                    raise ValueError("CONTROL_ALLOWANCE_EXHAUSTED")
            refuse("CONTROL_ALLOWANCE_EXHAUSTED",
                   lambda: entry.resolve_context_bindings(Q, native_raw, mapping, exhausted))
            need(len(calls) == 2, "ALLOWANCE_REFUSAL_STOPPED")
            return {"complete_callbacks": len(rows)+1, "refusal_at_callback": 2}
        case("allowance-callback-and-propagated-refusal", allowance)

        def modes():
            fields = ("catalog", "custody", "store_id", "custody_limits")
            rejected = 0
            with patch.object(entry, "run_manual", forbidden), patch.object(entry, "run_context", forbidden):
                for contextual in (False, True):
                    for mask in range(16):
                        values = {field: "present" if mask & (1 << i) else None
                                  for i, field in enumerate(fields)}
                        trial = NS(bindings=None if contextual else "bindings",
                            context_root="context" if contextual else None, **values)
                        valid = mask == (15 if contextual else 0)
                        if valid:
                            need(entry.binding_mode(trial) == ("context" if contextual else "manual"),
                                 "VALID_BINDING_MODE")
                        else:
                            refuse("QUERY_CONTEXT_ARGUMENTS", lambda: entry.binding_mode(trial))
                            result, saved = entry.run(trial)
                            need(result["ok"] is False and result["phase"] == "ARGUMENTS" and
                                 json.loads(saved) == result, "MODE_REFUSED_BEFORE_DISPATCH")
                            rejected += 1
                for manual, contextual in ((None, None), ("bindings", "context")):
                    trial = NS(bindings=manual, context_root=contextual)
                    refuse("QUERY_EXACTLY_ONE_BINDING_MODE", lambda: entry.binding_mode(trial))
                    need(entry.run(trial)[0]["phase"] == "ARGUMENTS", "EXCLUSIVE_MODE_BEFORE_DISPATCH")
                    rejected += 1
            need(rejected == 32, "MODE_REFUSAL_CENSUS")
            return {"valid_modes": 2, "rejected_option_combinations": rejected}
        case("exact-mode-and-owner-option-tuple-before-dispatch", modes)

        for mode in ("inert-success", "inert-missing", "inert-close-failure", "inert-rename-unknown",
                     "inert-context-mismatch"):
            case(mode, lambda mode=mode: inert_lifecycle(
                entry, Q, native_raw, mapping, expected_query, output, mode))
        need(len(cases) == 11, "CONTEXT_CONTROLS_EXACT_GROUP_COUNT")
        for key, digest in PINS.items():
            pinned(paths[key], digest)
        for key, digest in FIXTURE_PINS.items():
            pinned(fixture_paths[key], digest)
    check()
    result = {"status": "PASS_FOCUSED_CONTEXT_QUERY_CONTROLS", "cases": cases,
        "source_pins": {key: {"path": str(paths[key]), "sha256": digest} for key, digest in PINS.items()},
        "fixture_pins": {key: {"path": str(fixture_paths[key]), "sha256": digest}
                         for key, digest in FIXTURE_PINS.items()},
        "wall_seconds": time.monotonic()-START, "controller_cpu_seconds": time.process_time()-CPU,
        "scope": "REAL_PURE_QUERY_HELPERS_AND_INERT_LIFECYCLE_NOT_OWNER_OR_MATHEMATICAL_ACCEPTANCE",
        "mathematical_acceptance": False}
    with (output/"REPORT.json").open("xb") as stream:
        stream.write(raw(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

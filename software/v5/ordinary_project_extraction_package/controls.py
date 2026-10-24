"""New project-extraction boundary: real pure syntax, explicitly inert facade.

No owner, database, native executable, network, profile loader or project artifact
is opened. Selected controller helper AST and capacity expressions are executed
with real ordinary_evidence syntax and explicit path/state doubles. The facade
itself is loaded in full with inert bootstrap/extraction/accounting doubles.
This is not extraction, acceptance, filesystem-defense or cost evidence.
Root must separately review/select this finite control before execution.
"""
from __future__ import annotations

import argparse
import ast
from contextlib import ExitStack
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
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
    "evidence": ("software/v5/ordinary_lean/ordinary_evidence.py",
        "fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6"),
    "controller": ("software/v5/ordinary_project_extraction/library_extraction.py",
        "cd79d9050fbc80a94faef845ddf99fe7d1b8ba5e376048aa4a7698f06f396061"),
    "owner": ("software/v5/ordinary_project_extraction_package/owner.py",
        "2d4de791436d86810ef192e6a776cdbc0b45076f8c0bc75458e35e005cb6cbbe"),
}


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def demand(ok, code):
    if not ok:
        raise ValueError(code)


def check():
    need(time.monotonic()-START < 35 and time.process_time()-CPU < 20,
         "PROJECT_CONTROLS_ORIGINAL_ALLOWANCE")


def forbidden(*_, **__):
    raise AssertionError("PROJECT_CONTROLS_FORBIDDEN_EXTERNAL_CALL")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def pinned(path, digest):
    need(path.is_absolute() and ".." not in path.parts and
         path.resolve(strict=True).is_relative_to(ROOT), "PROJECT_CONTROLS_LOCAL_PATH")
    with path.open("rb") as stream:
        raw = stream.read(MIB+1)
    need(0 < len(raw) <= MIB and sha(raw) == digest, "PROJECT_CONTROLS_PIN:"+str(path))
    return raw


def refuse(code, action):
    try:
        action()
    except ValueError as error:
        need(str(error) == code, "PROJECT_CONTROLS_WRONG_REFUSAL:"+str(error))
    else:
        raise AssertionError("PROJECT_CONTROLS_NO_REFUSAL:"+code)


def lean_name(*parts):
    return [[0, {"$bytes": list(part.encode("utf-8"))}] for part in parts]


def inert_facade(entry, E, output, mode, changes=None):
    """All state/path/profile/extraction APIs are explicit non-authority doubles."""
    fake = output/"not-created"
    paths = {name: fake/name for name in ("catalog", "custody", "limits.json",
        "retained", "selection.json", "modules.json", "destination")}
    store_id, parent, implementation = "1"*64, "2"*64, "3"*64
    selection_raw = encoded({"schema": "DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1",
        "project_search_paths": [r"E:\approved-inert"], "modules": [lean_name("Local", "Module")]})
    request_raw, candidate_raw = b"inert retained request", b"inert candidate"
    modules = [lean_name("Std", "Data")]
    events, calls = [], []
    values = {
        paths["limits.json"]: encoded({"cap": 1}),
        paths["catalog"]/"ADOPTION.json": encoded({"schema": "INERT",
            "store_id": store_id, "implementation": implementation, "limits": {}}),
        paths["retained"]/"REQUEST.json": request_raw,
        paths["retained"]/"candidate.json": candidate_raw,
        paths["selection.json"]: selection_raw, paths["modules.json"]: encoded(modules),
    }

    def read(path, maximum):
        value = values[path]
        need(len(value) <= maximum, "INERT_INPUT_BOUND")
        events.append("read:"+path.name)
        return value

    def close(label):
        events.append(label+"-close")
        if mode == "failure-and-close":
            raise OSError("INERT_"+label.upper()+"_CLOSE")

    installation = NS(root=fake/"installation", runtime_roots={},
        semantic_id="4"*64, implementation_id=implementation, doc={"implementation": implementation})
    custody = NS(close=lambda: close("custody"))
    owner = NS(close=lambda: close("owner"))

    def open_custody(*args, **kwargs):
        need(args == (paths["custody"], installation.semantic_id, {"cap": 1}) and
             kwargs == {"create": False}, "INERT_CUSTODY_ARGUMENTS")
        events.append("custody-open")
        return custody

    def open_owner(*args, **kwargs):
        need(args == (installation, paths["catalog"], store_id, custody) and
             kwargs["create"] is False and vars(kwargs["limits"]) == {}, "INERT_OWNER_ARGUMENTS")
        events.append("owner-open")
        return owner

    def extract(*args, **kwargs):
        need(args == (owner, parent, paths["retained"]), "INERT_EXTRACTION_ARGUMENTS")
        need(kwargs["request_sha256"] == sha(request_raw) and
             kwargs["candidate_sha256"] == sha(candidate_raw) and
             kwargs["output_directory"] == paths["destination"] and
             kwargs["profile"] is profile and
             kwargs["exporter"] == Path(entry.__file__).parent/"authoring/bin/MissingImportExporter.exe" and
             kwargs["parent_deadline"] == allocation.deadline and
             all(callable(kwargs[key]) for key in ("make_budget", "account_worker_cpu", "check_parent")),
             "INERT_EXTRACTION_BOUND_INPUTS")
        if mode == "std":
            need(kwargs["modules"] == modules and "project_selection_raw" not in kwargs and
                 "project_selection_sha256" not in kwargs, "INERT_STD_ONLY_ROUTING")
        else:
            need(kwargs["project_selection_raw"] == selection_raw and
                 kwargs["project_selection_sha256"] == sha(selection_raw) and
                 "modules" not in kwargs, "INERT_PROJECT_ONLY_ROUTING")
        calls.append("extract")
        events.append("extract")
        if mode == "failure-and-close":
            raise ValueError("INERT_EXTRACTION_FAILURE")
        return {"status": "INERT_EXTRACTION_NOT_EXECUTED", "mathematical_acceptance": False}

    # None of these doubles validates real paths, adoption policy or ownership.
    C = NS(ordinary=lambda path, **kw: path, read_bounded=read, hexid=E._hex)
    P = NS(SCHEMA="INERT", fields=lambda *a: None, uint=lambda *a: None,
           Limits=lambda **kw: NS(**kw))
    A = NS(C=C, P=P, E=E, _writer_json=lambda value, maximum: json.loads(value),
           OrdinaryAdmission=NS(open=open_owner))
    profile = NS()
    extraction = NS(A=A, extract_retained=extract, selected_modules=lambda value: value)
    loaded = NS(A=A, G=NS(), O=NS(STORE_LIMITS={"cap": (1, 2)}, OrdinaryStore=open_custody),
                installation=installation, profile=profile, library_extraction=extraction)
    allocation = NS(deadline=START+35, check=check, account=forbidden, operation=forbidden,
        report=lambda: {"scope": "INERT_ACCOUNTING_NOT_MEASURED_EXTRACTION"})
    optional = ("catalog_limits", "source", "acquired_targets", "module_targets", "module_anchor",
        "output_names", "project_authoring", "project_authoring_sha256", "candidate", "candidate_sha256",
        "supplement", "supplement_sha256", "prepared_bindings", "prepared_bindings_sha256", "context_root")
    args = NS(**dict.fromkeys(optional), operation="extract-std" if mode == "std" else "extract-project",
        profile_sha256="5"*64, python_runtime="INERT", lean_runtime="INERT", catalog=str(paths["catalog"]),
        custody=str(paths["custody"]), store_id=store_id, custody_limits=str(paths["limits.json"]),
        parent_root=parent, output=str(paths["destination"]), retained_contribution=str(paths["retained"]),
        retained_request_sha256=sha(request_raw), retained_candidate_sha256=sha(candidate_raw),
        library_modules=str(paths["modules.json"]) if mode == "std" else None,
        project_extraction=None if mode == "std" else str(paths["selection.json"]),
        project_extraction_sha256=None if mode == "std" else sha(selection_raw),
        after_root="", limit=32, wall_seconds=35, cpu_seconds=20, memory_mib=256)
    for key, value in (changes or {}).items():
        setattr(args, key, value)
    with patch.object(entry, "bootstrap", lambda *a: NS(load=lambda *a, **kw: loaded)), \
            patch.object(entry, "Allowance", lambda args: allocation):
        result = entry.run(args)
    if changes:
        need(result["ok"] is False and result["phase"] == "SUPPORT" and
             not calls and not any(event.endswith("-open") for event in events),
             "INERT_REFUSED_BEFORE_OWNER_OPEN")
    else:
        need(calls == ["extract"] and events.count("owner-close") == events.count("custody-close") == 1 and
             events.index("owner-close") < events.index("custody-close"), "INERT_BOTH_CLOSED")
        if mode == "failure-and-close":
            need(result["ok"] is False and result["error"] == "INERT_EXTRACTION_FAILURE" and
                 result["phase"] == "EXTRACT_PROJECT" and result["accepted"] is None and
                 [row["component"] for row in result["close_errors"]] == ["owner", "custody"],
                 "INERT_FAILURE_AND_BOTH_CLOSURE_ERRORS_PRESERVED")
        else:
            need(result["ok"] is True and result["result"]["mathematical_acceptance"] is False,
                 "INERT_SUCCESS_NOT_ACCEPTANCE")
    return {"events": events, "result": result}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PROJECT_CONTROLS_PROCESS")
    output = Path(args.output)
    need(output.is_absolute() and ".." not in output.parts and output.parent.is_dir() and
         output.resolve().is_relative_to(ROOT/"experiments/v5-local-checks") and
         not os.path.lexists(output), "PROJECT_CONTROLS_FRESH_OUTPUT")
    paths = {key: ROOT/relative for key, (relative, _) in PINS.items()}
    selected = {key: pinned(paths[key], pin) for key, (_, pin) in PINS.items()}
    output.mkdir()
    cases = []

    def case(label, call):
        check()
        cases.append({"case": label, "outcome": "PASS", "detail": call()})

    with ExitStack() as stack:
        for target in ("subprocess.Popen", "socket.socket", "socket.create_connection", "sqlite3.connect",
                       "os.system", "os.startfile"):
            stack.enter_context(patch(target, forbidden))
        stack.enter_context(patch.object(Path, "open", forbidden))
        modules = {}
        for key in ("evidence", "owner"):
            name = "_project_controls_"+key
            need(name not in sys.modules, "PROJECT_CONTROLS_CLEAN_MODULE")
            spec = importlib.util.spec_from_file_location(name, paths[key])
            module = importlib.util.module_from_spec(spec)
            stack.enter_context(patch.dict(sys.modules, {name: module}))
            exec(compile(selected[key], str(paths[key]), "exec"), module.__dict__)
            modules[key] = module
        E, entry = modules["evidence"], modules["owner"]
        tree = ast.parse(selected["controller"], filename=str(paths["controller"]))
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and
                     node.name in ("selected_modules", "selected_project")]
        need({node.name for node in functions} == {"selected_modules", "selected_project"},
             "PROJECT_CONTROLS_EXACT_HELPERS")
        path_calls = []
        def ordinary(path, **kwargs):
            need(kwargs == {"directory": True}, "INERT_DIRECTORY_HELPER_CONTRACT")
            path_calls.append(path)
            return path
        env = {"A": NS(E=E, C=NS(hexid=E._hex, ordinary=ordinary), need=demand, sha=sha),
               "os": os, "re": re, "Path": Path, "MIB": MIB}
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(paths["controller"]), "exec"), env)
        select_modules, select_project = env["selected_modules"], env["selected_project"]

        def names():
            for size in (75, 96):
                name = lean_name("A"*size)
                need(select_modules([name], installed_std=False) == [name], "PROJECT_LONG_COMPONENT")
            need(select_modules([lean_name("Std", "A"*64)]) == [lean_name("Std", "A"*64)], "STD_64")
            for bad in ("A"*97, "CON", "com1", "LPT9", "a-b", "..", "a/b", "é"):
                refuse("EXTRACTION_MODULE_IDENTIFIER", lambda bad=bad:
                       select_modules([lean_name("Local", bad)], installed_std=False))
            for size in (65, 75):
                refuse("EXTRACTION_MODULE_IDENTIFIER", lambda size=size:
                       select_modules([lean_name("Std", "A"*size)]))
            refuse("EXTRACTION_UNIQUE_INSTALLED_STD_MODULE", lambda: select_modules([lean_name("Local")]))
            refuse("EXTRACTION_UNIQUE_PROJECT_MODULE", lambda:
                   select_modules([lean_name("Local"), lean_name("Local")], installed_std=False))
            refuse("EXTRACTION_MODULE_IDENTIFIER", lambda:
                   select_modules([lean_name("Local")+[[1, 1]]], installed_std=False))
            return {"project_max_component_bytes": 96, "std_max_component_bytes": 64}
        case("project-module-grammar-and-preserved-std-mode", names)

        good = {"schema": "DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1",
                "project_search_paths": [r"e:/Approved/First", r"E:\Approved\Second"],
                "modules": [lean_name("Local", "Module")]}
        def selected(value, digest=None):
            raw = encoded(value)
            return select_project(raw, sha(raw) if digest is None else digest, check)
        def positive():
            path_calls.clear()
            value, roots = selected(good)
            need(value == good and roots == tuple(Path(path) for path in good["project_search_paths"]) and
                 path_calls == list(roots), "EXACT_ORDERED_SELECTION_SPELLING")
            return {"raw_paths": value["project_search_paths"], "path_validation": "INERT_DIRECTORY_DOUBLE"}
        case("exact-local-selection-hash-order-and-spelling", positive)

        def bad_selections():
            refuse("EXTRACTION_PROJECT_SELECTION_PIN", lambda: selected(good, "0"*64))
            refuse("EXTRACTION_PROJECT_SELECTION_FIELDS", lambda: selected(dict(good, extra=1)))
            refuse("JSON_LEXICAL_TOKEN", lambda:
                   select_project(encoded(good)+b"\n", sha(encoded(good)+b"\n"), check))
            for path in ("relative", "E:relative", r"\\server\share", r"\\?\E:\root", "E:/a;b", "E:/a\n"):
                refuse("EXTRACTION_PROJECT_ROOT_GRAMMAR", lambda path=path:
                       selected(dict(good, project_search_paths=[path])))
            for path in ("E:/a/../b", "E:/./b", "E:/"+"a/"*128):
                refuse("EXTRACTION_PROJECT_ROOT_COMPONENTS", lambda path=path:
                       selected(dict(good, project_search_paths=[path])))
            refuse("EXTRACTION_DUPLICATE_PROJECT_ROOT", lambda:
                   selected(dict(good, project_search_paths=["E:/Root", "e:\\root\\"])))
            refuse("EXTRACTION_PROJECT_WINDOWS_ROOTS", lambda: selected(dict(good, project_search_paths=[])))
            def exhausted():
                raise ValueError("INERT_DEADLINE")
            refuse("INERT_DEADLINE", lambda: select_project(encoded(good), sha(encoded(good)), exhausted))
            return {"scope": "PURE_GRAMMAR_HASH_CALLBACK_NOT_REAL_FILESYSTEM_DEFENSES"}
        case("selection-refusals-before-native-or-state", bad_selections)

        def capacities():
            function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and
                            node.name == "extract_retained")
            body = next(node.body for node in function.body if isinstance(node, ast.Try))
            position = next(i for i, node in enumerate(body) if isinstance(node, ast.Assign) and
                            any(isinstance(target, ast.Name) and target.id == "capacity" for target in node.targets))
            code = compile(ast.Module(body=body[position:position+2], type_ignores=[]),
                           str(paths["controller"]), "exec")
            def compute(units, size, nodes):
                context = {"A": NS(need=demand), "original": {"units": [None]*units},
                    "candidate_raw": bytes(size), "initial": NS(total_nodes=nodes),
                    "LIMITS": NS(max_units=32, max_bundle_bytes=4*MIB, max_total_nodes=131072)}
                exec(code, context)
                return context["capacity"]
            need(compute(3, 100, 47) == {"units": 29, "bytes": 4*MIB-100, "encoded_nodes": 131025},
                 "EXACT_REMAINING_CAPACITY")
            need(compute(31, 4*MIB-1, 131071) == {"units": 1, "bytes": 1, "encoded_nodes": 1},
                 "ONE_REMAINING_CAPACITY")
            for args in ((32, 100, 47), (3, 4*MIB, 47), (3, 100, 131072)):
                refuse("EXTRACTION_NO_SUPPLEMENT_CAPACITY", lambda args=args: compute(*args))
            return {"scope": "EXACT_SOURCE_EXPRESSIONS_NOT_BINDER_OR_NATIVE_LIMIT_INTEGRATION"}
        case("source-derived-remaining-capacity-arithmetic", capacities)
        for mode in ("project", "std", "failure-and-close"):
            case("inert-facade-"+mode, lambda mode=mode: inert_facade(entry, E, output, mode))

        def argument_failures():
            mutations = [({"project_extraction_sha256": None}, "OWNER_EXTRACTION_PROJECT_ARGUMENTS"),
                ({"project_extraction": None}, "OWNER_EXTRACTION_PROJECT_ARGUMENTS"),
                ({"library_modules": "unexpected"}, "OWNER_EXTRACTION_STD_MODULES_ONLY"),
                ({"retained_candidate_sha256": None}, "OWNER_EXTRACTION_ARGUMENTS"),
                ({"source": "unexpected"}, "OWNER_CONTRIBUTION_ARGUMENTS"),
                ({"project_authoring": "unexpected"}, "OWNER_PROJECT_AUTHORING_ARGUMENTS"),
                ({"candidate": "unexpected"}, "OWNER_COMPLETION_ARGUMENTS"),
                ({"output_names": "unexpected"}, "OWNER_OUTPUT_NAME_ARGUMENT"),
                ({"project_extraction_sha256": "0"*64}, "OWNER_EXTRACTION_PROJECT_PIN")]
            for changes, code in mutations:
                detail = inert_facade(entry, E, output, "project", changes)
                need(detail["result"]["error"] == code, "EXACT_FACADE_REFUSAL:"+code)
            for changes, code in (({"project_extraction": "unexpected"}, "OWNER_EXTRACTION_PROJECT_ARGUMENTS"),
                                  ({"library_modules": None}, "OWNER_EXTRACTION_STD_MODULES_ONLY")):
                detail = inert_facade(entry, E, output, "std", changes)
                need(detail["result"]["error"] == code, "EXACT_STD_FACADE_REFUSAL")
            return {"preopen_refusals": len(mutations)+2}
        case("facade-mode-exclusivity-and-wrong-hash-before-open", argument_failures)
        need(len(cases) == 8, "PROJECT_CONTROLS_GROUP_COUNT")
    for key, (_, digest) in PINS.items():
        pinned(paths[key], digest)
    check()
    result = {"status": "PASS_FOCUSED_PROJECT_EXTRACTION_CONTROLS", "cases": cases,
        "source_pins": PINS, "wall_seconds": time.monotonic()-START,
        "controller_cpu_seconds": time.process_time()-CPU,
        "scope": "PURE_SYNTAX_AND_INERT_FACADE_NOT_EXTRACTION_OR_MATHEMATICAL_ACCEPTANCE",
        "mathematical_acceptance": False}
    with (output/"REPORT.json").open("xb") as stream:
        stream.write(encoded(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

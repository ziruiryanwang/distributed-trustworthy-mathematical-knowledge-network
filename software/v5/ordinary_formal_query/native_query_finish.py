"""Pure postcheck of preserved native02 outputs, never a native retry.

The original whole run remains FAILED. Compilation/extraction outputs are only
eligible for root adoption jointly with the independent saved-output review.
No compiler, owner, database or network call is allowed by this continuation.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack
import hashlib
import importlib.util
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import time
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
OLD = LOCAL/"ordinary-formal-query-native-02"
NATIVE = OLD/"native"
PACKAGE = LOCAL/"ordinary-current-relocated-smoke-01-payload"
SNAP = OLD/"sources/software/v5/ordinary_formal_query"
SUPPORT = ROOT/"software/v5/ordinary_module_matching/native_check02.py"
SUPPORT_SHA = "8d0238e312bca697b7d74d01785581bfc5954f45942cb134a369a108ca4f80a1"
PROFILE_SHA = "192dfee12ac186fbdac0634212b28c1c6324222da2b035f8f295ec764303a68d"
SELECTION_SHA = "56b4cd0613f3753040f903386469d78f6b1ef6d6a6169a496da46e30da6430cd"
COMMAND_SHA = "f71bb36f23edff62b8e48fde803e159a93e1ec5f62541d11d357c59e79971992"
QUERY_SHA = "7901236768784a399f9ae5c56b374d040bce56536b0a47a6ee85093440cabcee"
SUFFIXES = (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")
SAVED = {
    "RESULT.json": "d4d326d36146279fe9ecf254eb1b3f51c5f8ae95392696830e43c5eeb7fd3f70",
    "selection.json": SELECTION_SHA,
    "native/INPUTS.json": "14d4dec23487cff83178fdafed7b826b22b4a158ca7cbfc6470a42b9ed9a1f4b",
    "native/NATIVE-QUERY-RESULT.json": "cdbb4cbddd4b78cbc16df7fb115c974c0adbd887a9616f133e67f9ade3cf582f",
    "native/query.json": "fa1965b1c69bcbe479e66e65d19bbea710fde294ce2e00e603c0636207735ef5",
    "native/OwnerQueryCommand.lean": COMMAND_SHA,
    "native/QueryNativeFixture.lean": "5f49a13151c483a369a0768e06e5433c2c9899958e72b83aa8dee7a8850982c2",
    "native/OwnerQueryCommand.olean": "0dcf8f7ba86ef053001876d1dfe70245bc494cddc6b8c3d8e5ac5069c82da4e2",
    "native/OwnerQueryCommand.olean.private": "6264acaefd4796dacb162e1ad2448709a5bedcccc64c63fcaf0fcf1779cfccb5",
    "native/OwnerQueryCommand.olean.server": "f9aaec7c95b2f81462f0faab5ee53c1125f17c9a5d7367bea9c8576fc421fcfe",
    "native/OwnerQueryCommand.ir": "ad8627e47bf8bbcfc5401dac6316f2c91792214b184df1c3f825c5c32cb42866",
    "native/OwnerQueryCommand.ir.sig": "8777e7153d3ce8e581d31c625e4c515d886132f6e63ec95ea201045859bcf948",
    "native/QueryNativeFixture.olean": "d762e903fb5caa36d3ab9af6d4960cffe8ceedaad579f083431ce25e1c7405f8",
    "native/QueryNativeFixture.olean.private": "4f0192f4fd6ce6b1abe26e1607a87644d36ca6dd241605c16f7a5f0626dd4ab5",
    "native/QueryNativeFixture.olean.server": "7787728a0ba8fe15480f4792489baceefb7b562100becf75bb58ad97fd7b6bdd",
    "native/QueryNativeFixture.ir": "40067d77e33c2026cc732d88abe095c306548fcf8275c7d109ece98c6909daae",
    "native/QueryNativeFixture.ir.sig": "870d254a54ddd4b357200513e1e3f8a160aa3c045279765b6b3fd3424c460ecb",
}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def forbidden(*_, **__):
    raise AssertionError("QUERY_FINISH_FORBIDDEN_EXTERNAL_CALL")


def support():
    # This used support module has inert top-level declarations. Importing it
    # does not execute its main; only existing pin/JSON/clean/save helpers run.
    with SUPPORT.open("rb") as stream:
        raw = stream.read(1024**2+1)
    need(hashlib.sha256(raw).hexdigest() == SUPPORT_SHA, "QUERY_FINISH_SUPPORT_PIN")
    spec = importlib.util.spec_from_file_location("_query_finish_support", SUPPORT)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(SUPPORT), "exec"), module.__dict__)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "QUERY_FINISH_CONTEXT")
    started, cpu_started, held = time.monotonic(), time.process_time(), {}

    def check():
        need(time.monotonic()-started < 35 and time.process_time()-cpu_started < 20,
             "QUERY_FINISH_ORIGINAL_ALLOWANCE")

    with ExitStack() as stack:
        for target in ("subprocess.Popen", "subprocess.call", "subprocess.run", "socket.socket",
                       "socket.create_connection", "sqlite3.connect", "os.system", "os.startfile"):
            stack.enter_context(patch(target, forbidden))
        K = support()

        def hold(path, expected=None):
            actual = K.pin(path, check)
            need(expected is None or actual == expected or
                 (type(expected) is str and actual["sha256"] == expected), "QUERY_FINISH_PIN:"+str(path))
            need(held.setdefault(str(path), actual) == actual, "QUERY_FINISH_PIN_CHANGED")
            return actual

        def read(path, expected=None, maximum=2*1024**2):
            hold(path, expected)
            return K.read(path, maximum)

        output = K.ordinary(Path(args.output), directory=True, fresh=True)
        need(output.is_relative_to(LOCAL) and not output.is_relative_to(OLD) and
             not OLD.is_relative_to(output) and not output.is_relative_to(PACKAGE) and
             not PACKAGE.is_relative_to(output), "QUERY_FINISH_FRESH_DISJOINT")
        hold(SUPPORT, SUPPORT_SHA)
        hold(Path(__file__).resolve())
        for relative, expected in SAVED.items():
            hold(OLD/relative, expected)
        selection = K.diagnostic_json(read(OLD/"selection.json", SELECTION_SHA))
        need(selection["schema"] == "DMKN_V5_LOCAL_CHECK_V1" and
             selection["name"] == "ordinary-formal-query-native-02" and
             len(selection["sources"]) == 5 and len(selection["runtime_pins"]) == 156,
             "QUERY_FINISH_ORIGINAL_SELECTION")
        for relative, expected in selection["sources"].items():
            hold(ROOT/relative, expected)
            hold(OLD/"sources"/relative, expected)
        for path, expected in selection["runtime_pins"].items():
            hold(Path(path), expected)
        inputs = K.diagnostic_json(read(NATIVE/"INPUTS.json"))
        need(inputs["profile_sha256"] == PROFILE_SHA and len(inputs["pins"]) == 16,
             "QUERY_FINISH_SAVED_INPUTS")
        for path, expected in inputs["pins"].items():
            hold(Path(path), expected)
        outer = K.diagnostic_json(read(OLD/"RESULT.json"))
        native = K.diagnostic_json(read(NATIVE/"NATIVE-QUERY-RESULT.json"))
        need(outer["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1" and
             outer["selection_sha256"] == SELECTION_SHA and native["status"] == "FAILED" and
             native["error_type"] == "EvidenceError" and native["error"] == "JSON_LEXICAL_TOKEN" and
             native["acceptance"] is False and len(native["calls"]) == 2,
             "QUERY_FINISH_PRESERVED_FAILED_OUTCOME")
        K.clean(outer["result"], exit_code=1)
        need(read(OLD/"command/stdout.txt") == b'{"status": "FAILED"}\r\n' and
             read(OLD/"command/stderr.txt") == b"", "QUERY_FINISH_OUTER_LOGS")
        for filename, call in zip(("OwnerQueryCommand.lean", "QueryNativeFixture.lean"), native["calls"]):
            record = call["supervision"]
            cpu = K.clean(record)
            need(call["file"] == filename and call["cpu_complete"] is True and
                 call["charged_cpu_seconds"] == cpu and record["cwd"] == str(NATIVE),
                 "QUERY_FINISH_CLEAN_NATIVE_CALL")
            logdir = NATIVE/(Path(filename).stem+"-supervision")
            command = K.diagnostic_json(read(logdir/"command.json"))
            need(command == {key: record[key] for key in ("argv", "cwd", "limits")} and
                 read(logdir/"stdout.txt") == b"" and read(logdir/"stderr.txt") == b"",
                 "QUERY_FINISH_NATIVE_COMMAND_LOGS")
        need(not os.path.lexists(NATIVE/"bound-query.json") and not os.path.lexists(NATIVE/"bindings.json"),
             "QUERY_FINISH_ORIGINAL_DID_NOT_COMPLETE")
        template = read(SNAP/"QueryNativeFixture.lean")
        need(read(NATIVE/"QueryNativeFixture.lean") == template.replace(b"__QUERY_OUTPUT__",
             str(NATIVE/"query.json").replace("\\", "/").encode("ascii")) and
             read(NATIVE/"OwnerQueryCommand.lean") == read(SNAP/"OwnerQueryCommand02.lean", COMMAND_SHA),
             "QUERY_FINISH_ACTUAL_NATIVE_SOURCES")

        profile = K.diagnostic_json(read(PACKAGE/"PROFILE.json", PROFILE_SHA))
        manifest = K.diagnostic_json(read(PACKAGE/"installation/INSTALLATION.json",
                                          profile["installation_manifest_sha256"]))

        def installed(logical):
            path = PACKAGE/"installation"/logical
            hold(path, manifest["files"][logical])
            return path

        def author(logical):
            path = PACKAGE/logical
            hold(path, profile["files"][logical])
            return path

        Apath = installed("supervisor/commons.py")
        A = K.load_exact(Apath, "_query_finish_inventory_json", held[str(Apath)], check)
        modules = {}
        for name, path in (("ordinary_evidence", installed("py/ordinary_evidence.py")),
                          ("ordinary_semantics", installed("py/ordinary_semantics.py")),
                          ("ordinary_preview", author("authoring/py/ordinary_preview.py")),
                          ("portable_evidence", installed("py/portable_evidence.py")),
                          ("portable_preview", author("authoring/py/portable_preview.py"))):
            modules[name] = K.load_exact(path, name, held[str(path)], check)
        query_source = SNAP/"formal_query.py"
        hold(query_source, QUERY_SHA)
        Q = K.load_exact(query_source, "formal_query", held[str(query_source)], check)
        E, S = modules["ordinary_evidence"], modules["ordinary_semantics"]
        raw = read(NATIVE/"query.json")
        parsed = Q.read_native_type(raw)
        name = lambda text: [[0, {"$bytes": list(text.encode("ascii"))}]]
        need(parsed["universe_params"] == [name("u"), name("v")] and
             Q.reference_names(raw) == [name("Eq")], "QUERY_FINISH_EXACT_PARAMS_REFERENCES")
        exprs, current, binders = parsed["type"][2], parsed["type"][3], []
        while exprs[current][0] == 5:
            node = exprs[current]
            binders.append([node[1], node[2]])
            current = node[4]
        need(binders == [[name(label), flag] for label, flag in
                         (("A", 1), ("B", 0), ("f", 0), ("g", 0), ("a", 0))],
             "QUERY_FINISH_SECTION_CLOSURE")
        # This exact fixed basis inventory is an operational JSON asset ending
        # in LF, not an inert evidence/query envelope. Do not weaken E.strict_json.
        inventory_raw = read(installed("foundation/inventory.json"), S.INVENTORY, 1024**2)
        rows = A.strict(inventory_raw)
        need(type(rows) is list and len(rows) == 581 and
             sum(type(row) is list and len(row) == 5 and row[0] == name("Eq") for row in rows) == 1,
             "QUERY_FINISH_EQ_KNOWN_FIXED_BASIS")
        bindings = E.canonical_json([[name("Eq"), S.basis_symbol_id(S.semantic_id(), S.foundation_id(), name("Eq"))]])
        query = Q.bind_native_type(raw, bindings, semantic_id=S.semantic_id())
        spec = Q.query_spec(query)
        for path, expected in held.items():
            need(K.pin(Path(path), check) == expected, "QUERY_FINISH_FINAL_PIN")
        check()
        output.mkdir()
        K.save(output/"bound-query.json", query)
        K.save(output/"bindings.json", bindings)
        report = {"schema": "DMKN_ORDINARY_QUERY_SAVED_POSTCHECK_V1",
            "status": "PASS_SAVED_NATIVE_QUERY_POSTCHECK", "original_run_status": "FAILED",
            "original_failure": "JSON_LEXICAL_TOKEN_FIXED_INVENTORY_NOT_INERT_ENVELOPE",
            "original_selection_sha256": SELECTION_SHA,
            "original_result_pin": held[str(OLD/"RESULT.json")],
            "original_native_result_pin": held[str(NATIVE/"NATIVE-QUERY-RESULT.json")],
            "original_run": str(OLD), "profile_sha256": PROFILE_SHA,
            "source_command_pin": held[str(NATIVE/"OwnerQueryCommand.lean")],
            "compiled_command_artifacts": {suffix: held[str(NATIVE/("OwnerQueryCommand"+suffix))] for suffix in SUFFIXES},
            "successful_native_calls": [call["file"] for call in native["calls"]],
            "query_pin": held[str(NATIVE/"query.json")], "spec": spec,
            "bound_query_pin": K.pin(output/"bound-query.json", check),
            "bindings_pin": K.pin(output/"bindings.json", check), "section_binders": binders,
            "type_nodes": parsed["type_nodes"], "pins": held,
            "authority": "SAVED_COMPILATION_AND_QUERY_POSTCHECK_REQUIRES_INDEPENDENT_REVIEW_AND_ROOT_ADOPTION",
            "acceptance": False, "native_calls_performed": 0,
            "original_known_inclusive_cpu_seconds": outer["result"]["final_job"]["cpu_seconds"]+outer["wrapper_cpu_seconds"],
            "original_wall_seconds": outer["wall_seconds"],
            "wall_seconds": time.monotonic()-started, "cpu_seconds": time.process_time()-cpu_started}
        check()
        K.save(output/"REPORT.json", report)
    print(report["status"], flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Native-free retained-preparation/module-selector/public-CLI controls.

Use retained public B-contribution bytes as a compatibility fixture. Its explicit
map supplies a MOCK parent lookup, not an opened owner or a fresh warrant. Load
the selected successor once; prohibit databases, native children and networking.
No proof checking, extraction, admission or new mathematical validity is claimed.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
from contextlib import ExitStack
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import sqlite3
import stat
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import patch

MIB = 1024**2
PARENT = "287da91e1218e00b7bd6a12a550242a92279763e45601c41f200b6738ab3bcd6"
FIXTURE_PINS = {
    "REQUEST.json": "fe469911a76b0a76962462ae5ae3ac77db04b7151562b9f666e236ecce1973d3",
    "owner-request/header.json": "84839df3270083460a2c4733b382fadc7ddfb433913dc0da5bd4f44dcf400ffe",
    "owner-request/group-00000.json": "1506de8e3229b32aacc0f09ed2d1c7a546d46284efac87c5c44433f7484fee02",
    "owner-request/group-00001.json": "4f2d714f1e8e984c721f8ac02471285ef7f96f83e46ab4ccf699fe73c508722e",
    "targets.json": "eafe7371725fc7767b700cc6528e8dd2b9108d130c7ae06c3c678c6385030a68",
    "candidate.json": "59f551c47d48847673426023dbbb5442a03f0f896d5f3f5305f4bd81d736d322",
}


def need(condition, code):
    if not condition:
        raise AssertionError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class Allowance:
    deadline = START_WALL+50

    def check(self):
        need(time.monotonic() < self.deadline and time.process_time()-START_CPU < 30,
             "PREPARATION_CONTROL_ORIGINAL_ALLOWANCE")


def forbidden(*_, **__):
    raise AssertionError("PREPARATION_CONTROL_FORBIDDEN_EXTERNAL_OPERATION")


def read(path, maximum=2*MIB):
    need(path.is_absolute() and ".." not in path.parts, "PREPARATION_CONTROL_ABSOLUTE_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "PREPARATION_CONTROL_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PREPARATION_CONTROL_REGULAR")
    size = path.stat().st_size
    need(0 < size <= maximum, "PREPARATION_CONTROL_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "PREPARATION_CONTROL_FILE_CHANGED")
    return raw


def save(path, value):
    raw = value if type(value) is bytes else json.dumps(value, sort_keys=True,
        ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode("ascii")
    need(0 < len(raw) <= MIB, "PREPARATION_CONTROL_OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)
    return sha(raw)


def formal_name(text):
    return [[0, {"$bytes": list(part.encode("utf-8"))}] for part in text.split(".")]


def refuses(code, call, kind=ValueError):
    try:
        call()
    except kind as error:
        need(str(error) == code, "PREPARATION_CONTROL_WRONG_REFUSAL:"+str(error))
        return
    raise AssertionError("PREPARATION_CONTROL_MISSING_REFUSAL:"+code)


def selected_package(args, allowance):
    root = Path(args.package)
    raw = read(root/"PROFILE.json")
    need(sha(raw) == args.profile_sha256, "PREPARATION_CONTROL_PROFILE_PIN")
    descriptor = json.loads(raw)
    path, module_name = root/"owner.py", "_preparation_controls_owner"
    source, pin = read(path), descriptor["files"]["owner.py"]
    need(len(source) == pin["bytes"] and sha(source) == pin["sha256"] and
         module_name not in sys.modules, "PREPARATION_CONTROL_CODE_PIN")
    spec = importlib.util.spec_from_file_location(module_name, path)
    owner = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = owner
    exec(compile(source, str(path), "exec"), owner.__dict__)
    loader = owner.bootstrap(root, args.profile_sha256, allowance.check)
    loaded = loader.load(root, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        allowance.deadline, check_parent=allowance.check)
    need(loaded.library_extraction.A is loaded.A and loaded.library_extraction.G is loaded.G and
         loaded.library_extraction.X.A is loaded.A and loaded.G.A is loaded.A,
         "PREPARATION_CONTROL_SHARED_CORE")
    return owner, loaded


def controls(args, owner_cli, loaded, output, allowance):
    A, G, X = loaded.A, loaded.G, loaded.library_extraction
    R, E, S = X.R, A.E, A.S
    retained = Path(args.retained_directory)
    originals = {filename: read(retained/filename, MIB) for filename in FIXTURE_PINS}
    need({filename: sha(raw) for filename, raw in originals.items()} == FIXTURE_PINS,
         "PREPARATION_CONTROL_EXACT_RETAINED_FIXTURE")
    request_raw, header_raw, targets_raw = (originals[filename] for filename in
        ("REQUEST.json", "owner-request/header.json", "targets.json"))
    group_raws = tuple(originals[f"owner-request/group-{index:05d}.json"] for index in range(2))
    request, header = json.loads(request_raw), E.strict_json(header_raw, E.Limits(max_bytes=MIB))
    packets = [E.strict_json(raw) for raw in group_raws]
    semantic, foundation = loaded.installation.semantic_id, S.foundation_id()
    need(request["parent_root"] == header["context_root"] == PARENT and
         request["groups"] == header["group_count"] == 2, "PREPARATION_CONTROL_SELECTED_PARENT")
    # Explicit fixture-derived mock. This does NOT establish an owner warrant.
    parent_map = {E.name_key(row[1][0]): row[0] for row in header["basis_rows"]}
    for packet in packets:
        for name, mode, identity, body in packet[1]:
            key = E.name_key(name)
            need(key not in parent_map, "PREPARATION_CONTROL_FIXTURE_DUPLICATE")
            parent_map[key] = identity
    need(len(parent_map) == 583, "PREPARATION_CONTROL_FIXTURE_CENSUS")
    expected_name = E.name_key(formal_name("CommonsPeerExample.applyFour_eq"))
    fixture = output/"fixture"
    fixture.mkdir()

    def run(request_bytes=request_raw, header_bytes=header_raw, groups=group_raws,
            targets=targets_raw, *, mapping=None, **changes):
        chosen = parent_map if mapping is None else mapping
        options = dict(semantic_id=semantic, foundation_id=foundation, context_root=PARENT,
            warranted_symbol=lambda name: chosen.get(E.name_key(name)), check_budget=allowance.check)
        options.update(changes)
        return R.reconstruct_preparation(request_bytes, header_bytes, groups, targets, **options)

    def repin(*, changed_header=None, changed_packets=None, changed_targets=None, changed_request=None):
        doc = copy.deepcopy(request if changed_request is None else changed_request)
        hraw = header_raw if changed_header is None else E.canonical_json(changed_header)
        graw = group_raws if changed_packets is None else tuple(E.canonical_json(p) for p in changed_packets)
        traw = targets_raw if changed_targets is None else E.canonical_json(changed_targets)
        doc["groups"] = len(graw)
        doc["payload_bytes"] = len(hraw)+sum(map(len, graw))
        doc["request_files"] = {"header.json": {"bytes": len(hraw), "sha256": sha(hraw)}}
        for index, raw in enumerate(graw):
            doc["request_files"][f"group-{index:05d}.json"] = {"bytes": len(raw), "sha256": sha(raw)}
        doc["output_targets"] = {"bytes": len(traw), "sha256": sha(traw)}
        return (json.dumps(doc, sort_keys=True, allow_nan=False).encode("utf-8"), hraw, graw, traw)

    def retained_positive():
        calls = []
        def lookup(name):
            key = E.name_key(name); calls.append(key)
            return parent_map.get(key)
        result = run(warranted_symbol=lookup)
        need(result.status == "READY" and not result.mathematical_acceptance and
             dict(result.bindings) == parent_map and len(result.bindings) == 583 and
             result.output_names == (expected_name,), "PREPARATION_CONTROL_RECONSTRUCTED_MAP")
        need(result.request_sha256 == FIXTURE_PINS["REQUEST.json"] and
             result.header_sha256 == FIXTURE_PINS["owner-request/header.json"] and
             result.targets_sha256 == FIXTURE_PINS["targets.json"] and
             result.group_sha256s == tuple(FIXTURE_PINS[f"owner-request/group-{index:05d}.json"]
                                          for index in range(2)), "PREPARATION_CONTROL_RETAINED_HASHES")
        need(result.parent_lookups == len(calls) == len(set(calls)) == 584 and
             result.input_bytes == sum(map(len, (request_raw, header_raw, *group_raws, targets_raw))),
             "PREPARATION_CONTROL_COUNTS_AND_LOOKUP_CACHE")
        need(type(result.bindings) is tuple and all(type(row) is tuple and type(row[0]) is bytes
             for row in result.bindings) and type(result.output_names) is tuple,
             "PREPARATION_CONTROL_IMMUTABLE_ROWS")
        need({filename: sha(read(retained/filename, MIB)) for filename in FIXTURE_PINS} == FIXTURE_PINS,
             "PREPARATION_CONTROL_ORIGINAL_FILES_PRESERVED")

    def changed_pins_and_envelopes():
        refuses("RETAINED_REQUEST_DUPLICATE_KEY", lambda:
            R._metadata_json(b'{"groups":2,"groups":2}', allowance.check))
        refuses("RETAINED_REQUEST_DEPTH", lambda:
            R._metadata_json(b"["*65+b"0"+b"]"*65, allowance.check))
        for token in (b"-1", b"18446744073709551616"):
            refuses("RETAINED_REQUEST_INTEGER", lambda token=token:
                R._metadata_json(b'{"x":'+token+b"}", allowance.check))
        refuses("RETAINED_REQUEST_NONINTEGER", lambda:
            R._metadata_json(b'{"x":1.5}', allowance.check))
        bad = copy.deepcopy(request); bad["request_files"]["header.json"]["sha256"] = "0"*64
        refuses("RETAINED_FILE_CHANGED", lambda: run(request_bytes=json.dumps(bad).encode()))
        refuses("RETAINED_FILE_PIN", lambda: run(targets=targets_raw+b" "))
        for filename, remove in (("group-00001.json", True), ("unexpected.json", False)):
            bad = copy.deepcopy(request)
            if remove:
                del bad["request_files"][filename]
            else:
                bad["request_files"][filename] = {"bytes": 1, "sha256": "0"*64}
            refuses("RETAINED_EXACT_FILE_MAP", lambda bad=bad: run(request_bytes=json.dumps(bad).encode()))
        refuses("RETAINED_REQUEST_CENSUS", lambda: run(groups=group_raws[:1]))
        bad = copy.deepcopy(request); bad["parent_root"] = "0"*64
        refuses("RETAINED_REQUEST_PARENT", lambda: run(request_bytes=json.dumps(bad).encode()))
        for key, value in (("schema", "DMKN_OWNER_REQUEST_V1"), ("semantic_id", "0"*64),
                           ("foundation_id", "0"*64), ("context_root", "0"*64)):
            bad_header = copy.deepcopy(header); bad_header[key] = value
            inputs = repin(changed_header=bad_header)
            refuses("RETAINED_HEADER_CONTEXT", lambda inputs=inputs: run(*inputs))

    def protected_identity_and_targets():
        bad_packets = copy.deepcopy(packets); bad_packets[0][1][0][2] = "0"*64
        inputs = repin(changed_packets=bad_packets)
        refuses("RETAINED_UNWARRANTED_BINDING", lambda: run(*inputs))
        bad_packets = copy.deepcopy(packets); bad_packets[0][1].append(copy.deepcopy(bad_packets[0][1][0]))
        inputs = repin(changed_packets=bad_packets)
        refuses("RETAINED_DUPLICATE_OR_NAME_BOUND", lambda: run(*inputs))
        bad_header = copy.deepcopy(header); bad_header["targets"][0][1] = "0"*64
        inputs = repin(changed_header=bad_header)
        refuses("RETAINED_PREPARED_TARGET_BINDING", lambda: run(*inputs))
        inputs = repin(changed_targets=[formal_name("ChangedTarget")])
        refuses("RETAINED_OUTPUT_TARGETS", lambda: run(*inputs))
        duplicate = [E.strict_json(expected_name)]*2
        bad = copy.deepcopy(request); bad["output_names"] = duplicate
        inputs = repin(changed_targets=duplicate, changed_request=bad)
        refuses("RETAINED_OUTPUT_COLLISION", lambda: run(*inputs))
        refuses("RETAINED_OUTPUT_COLLISION", lambda:
            run(mapping={**parent_map, expected_name: "0"*64}))

    def capacity_and_cancellation():
        refuses("RETAINED_INPUT_BOUNDS", lambda: run(groups=(b"[]",)*33))
        refuses("RETAINED_INPUT_BOUNDS", lambda: run(header_bytes=b"x"*(MIB+1)))
        refuses("RETAINED_INPUT_BOUNDS", lambda: run(targets=b"x"*65537))
        refuses("RETAINED_REQUEST_BYTES", lambda: run(request_bytes=b"x"*(MIB+1)))
        refuses("RETAINED_PAYLOAD_BOUND", lambda: run(groups=(b"x"*MIB,)*4))
        # Deliberately inert synthetic rows test only the selected-name cap.
        extra_names = [formal_name("Cap"+str(index)) for index in range(4096-581+1)]
        rows = [[name, 0, "1"*64, [[], []]] for name in extra_names]
        bad_header = copy.deepcopy(header); bad_header["group_count"] = 1
        inputs = repin(changed_header=bad_header, changed_packets=[[R.R.GROUP_FORMAT, rows, []]])
        mapping = {**parent_map, **{E.name_key(name): "1"*64 for name in extra_names}}
        refuses("RETAINED_DUPLICATE_OR_NAME_BOUND", lambda: run(*inputs, mapping=mapping))
        class Cancelled(RuntimeError):
            pass
        def stop():
            raise Cancelled("CONTROL_CANCELLED")
        refuses("CONTROL_CANCELLED", lambda: run(check_budget=stop), Cancelled)
        def failed_lookup(_):
            raise Cancelled("CONTROL_LOOKUP_FAILED")
        refuses("CONTROL_LOOKUP_FAILED", lambda: run(warranted_symbol=failed_lookup), Cancelled)
        def wrong_lookup(_):
            return 1
        refuses("RETAINED_LOOKUP_TYPE", lambda: run(warranted_symbol=wrong_lookup))

    def module_path_boundary():
        good = [formal_name("Std"), formal_name("Std.Data.HashMap.Basic")]
        need(X.selected_modules(good) == good, "PREPARATION_CONTROL_STD_MODULES")
        refuses("EXTRACTION_MODULES_EMPTY", lambda: X.selected_modules([]))
        refuses("EXTRACTION_UNIQUE_INSTALLED_STD_MODULE", lambda:
            X.selected_modules([formal_name("Init")]))
        refuses("EXTRACTION_UNIQUE_INSTALLED_STD_MODULE", lambda:
            X.selected_modules([formal_name("Std"), formal_name("Std")]))
        for part in ("..", ".", "a/b", "a\\b", "/tmp", "C:\\Temp", "COM1", "nul", "con",
                     "bad\npart", "", "é", "a b"):
            selected = formal_name("Std")+[[0, {"$bytes": list(part.encode("utf-8"))}]]
            refuses("EXTRACTION_MODULE_IDENTIFIER", lambda selected=selected: X.selected_modules([selected]))
        refuses("EXTRACTION_MODULE_IDENTIFIER", lambda:
            X.selected_modules([formal_name("Std")+[[1, 2]]]))

    catalog, custody = fixture/"catalog", fixture/"custody"
    catalog.mkdir(); custody.mkdir()
    limits_path, modules_path, bad_modules_path = fixture/"limits.json", fixture/"modules.json", fixture/"bad-modules.json"
    save(limits_path, {key: bounds[0] for key, bounds in loaded.O.STORE_LIMITS.items()})
    modules = [formal_name("Std.Data.HashMap.Basic")]
    save(modules_path, modules)
    save(bad_modules_path, [formal_name("Std")+[[0, {"$bytes": [46, 46]}]]])
    store_id = "4"*64
    save(catalog/"ADOPTION.json", {"schema": A.P.SCHEMA, "store_id": store_id,
        "implementation": loaded.installation.doc["implementation"], "limits": vars(A.P.Limits())})

    def cli_args(**changes):
        selected = dict(operation="extract-std", profile_sha256=args.profile_sha256,
            python_runtime=args.python_runtime, lean_runtime=args.lean_runtime,
            catalog=str(catalog), custody=str(custody), store_id=store_id, custody_limits=str(limits_path),
            wall_seconds=50, cpu_seconds=30, memory_mib=256, catalog_limits=None, parent_root=PARENT,
            source=None, acquired_targets=None, output_names=None, output=str(fixture/"not-created-output"),
            context_root=None, after_root="", limit=32, project_authoring=None, project_authoring_sha256=None,
            candidate=None, candidate_sha256=None, supplement=None, supplement_sha256=None,
            prepared_bindings=None, prepared_bindings_sha256=None, retained_contribution=str(retained),
            retained_request_sha256=FIXTURE_PINS["REQUEST.json"],
            retained_candidate_sha256=FIXTURE_PINS["candidate.json"], library_modules=str(modules_path))
        return SimpleNamespace(**(selected | changes))

    fake_loader = SimpleNamespace(load=lambda *_, **__: loaded)

    def cli_preopen_boundary():
        cases = [({"retained_request_sha256": None}, "OWNER_EXTRACTION_ARGUMENTS"),
            ({"retained_request_sha256": "0"*64}, "OWNER_EXTRACTION_INPUT_PIN"),
            ({"retained_candidate_sha256": "0"*64}, "OWNER_EXTRACTION_INPUT_PIN"),
            ({"library_modules": str(bad_modules_path)}, "EXTRACTION_MODULE_IDENTIFIER"),
            ({"output_names": str(retained/"targets.json")}, "OWNER_OUTPUT_NAME_ARGUMENT"),
            ({"source": "not-selected"}, "OWNER_CONTRIBUTION_ARGUMENTS")]
        with patch.object(owner_cli, "bootstrap", lambda *_, **__: fake_loader), \
                patch.object(loaded.O, "OrdinaryStore", forbidden):
            for changes, code in cases:
                report = owner_cli.run(cli_args(**changes))
                need(not report["ok"] and report["phase"] == "SUPPORT" and report["error"] == code,
                     "PREPARATION_CONTROL_PREOPEN_REFUSAL:"+str(report))
        need(not (fixture/"not-created-output").exists(), "PREPARATION_CONTROL_NO_CLI_OUTPUT")

    def cli_mocked_forwarding():
        captured, closed = [], []
        mock_owner = SimpleNamespace(close=lambda: closed.append("owner"))
        mock_custody = SimpleNamespace(close=lambda: closed.append("custody"))
        def extract(*positional, **keywords):
            captured.append((positional, keywords))
            return {"status": "MOCK_READY", "mathematical_acceptance": False}
        def failed_extract(*positional, **keywords):
            extract(*positional, **keywords)
            keywords["account_worker_cpu"](0.25)  # Mock charge, not native CPU.
            raise G.ContributionError("EXTRACTION_NATIVE", RuntimeError("CONTROL_EXTRACTION_FAILURE"),
                                      native_cpu_seconds=0.25)
        with patch.object(owner_cli, "bootstrap", lambda *_, **__: fake_loader), \
                patch.object(loaded.O, "OrdinaryStore", lambda *_, **__: mock_custody), \
                patch.object(A.OrdinaryAdmission, "open", lambda *_, **__: mock_owner):
            with patch.object(X, "extract_retained", extract):
                report = owner_cli.run(cli_args())
            with patch.object(X, "extract_retained", failed_extract):
                failure = owner_cli.run(cli_args())
        need(report["ok"] and report["result"]["status"] == "MOCK_READY" and not failure["ok"] and
             failure["accepted"] is None and failure["detail"]["native_cpu_seconds"] == 0.25 and
             failure["cost"]["worker_cpu_seconds"] == 0.25 and
             failure["detail"]["error"] == "CONTROL_EXTRACTION_FAILURE",
             "PREPARATION_CONTROL_MOCK_RESULT_AND_FAILURE")
        need(len(captured) == 2 and closed == ["owner", "custody"]*2,
             "PREPARATION_CONTROL_MOCK_CLOSURE")
        for positional, keywords in captured:
            need(positional == (mock_owner, PARENT, retained) and
                 keywords["request_sha256"] == FIXTURE_PINS["REQUEST.json"] and
                 keywords["candidate_sha256"] == FIXTURE_PINS["candidate.json"] and
                 keywords["modules"] == modules and keywords["profile"] is loaded.profile and
                 keywords["exporter"] == loaded.root/"authoring/bin/MissingImportExporter.exe" and
                 keywords["output_directory"] == fixture/"not-created-output" and
                 all(callable(keywords[key]) for key in ("make_budget", "account_worker_cpu", "check_parent")),
                 "PREPARATION_CONTROL_CLI_FORWARDING")

    return [("retained-actual-byte-compatibility-mock-parent", retained_positive),
            ("pins-exact-files-and-context-refusals", changed_pins_and_envelopes),
            ("protected-identity-and-target-refusals", protected_identity_and_targets),
            ("capacity-cancellation-and-lookup-failure", capacity_and_cancellation),
            ("installed-std-module-path-boundary", module_path_boundary),
            ("cli-preopen-refusals", cli_preopen_boundary),
            ("cli-mocked-forwarding-and-failure-retention", cli_mocked_forwarding)]


def main(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PREPARATION_CONTROL_PYTHON")
    allowance, rows = Allowance(), []
    with ExitStack() as guards:
        guards.enter_context(patch.object(sqlite3, "connect", forbidden))
        guards.enter_context(patch.object(subprocess, "Popen", forbidden))
        guards.enter_context(patch.object(socket.socket, "connect", forbidden))
        guards.enter_context(patch.object(socket.socket, "connect_ex", forbidden))
        owner, loaded = selected_package(args, allowance)
        guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, "open", forbidden))
        guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, "preflight", forbidden))
        guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, "admit", forbidden))
        guards.enter_context(patch.object(loaded.library_extraction.X, "exchange", forbidden))
        guards.enter_context(patch.object(loaded.peer_api.H, "exchange", forbidden))
        guards.enter_context(patch.object(loaded.peer_api.H.Provider, "start", forbidden))
        output = loaded.A.C.ordinary(Path(args.output), directory=True)
        retained = loaded.A.C.ordinary(Path(args.retained_directory), directory=True)
        for protected in (loaded.root, retained, *loaded.installation.runtime_roots.values()):
            need(not output.is_relative_to(protected) and not protected.is_relative_to(output),
                 "PREPARATION_CONTROL_OUTPUT_OVERLAP")
        for group, control in controls(args, owner, loaded, output, allowance):
            allowance.check()
            try:
                control(); allowance.check()
                rows.append({"group": group, "ok": True})
            except BaseException as error:
                rows.append({"group": group, "ok": False, "error_type": type(error).__name__,
                             "error": str(error)[:1000]})
    report = {"ok": len(rows) == 7 and all(row["ok"] for row in rows), "groups": rows,
        "profile_sha256": args.profile_sha256, "implementation_id": loaded.installation.implementation_id,
        "retained_file_sha256s": FIXTURE_PINS, "native_operations": 0, "owner_opens": 0,
        "wall_seconds": time.monotonic()-START_WALL, "controller_cpu_seconds": time.process_time()-START_CPU,
        "claim": "RETAINED_BYTES_AND_EXPLICIT_MOCKS_NOT_NATIVE_EXTRACTION_OR_MATHEMATICAL_ACCEPTANCE"}
    save(output/"PREPARATION-CONTROLS.json", report)
    print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output", "retained-directory"):
        parser.add_argument("--"+argument, required=True)
    raise SystemExit(main(parser.parse_args()))

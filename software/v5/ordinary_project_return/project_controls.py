"""Pure controls for the import-only generated bridge-name compatibility fix.

The selected package is loaded once. Only configuration validation and source
assembly are exercised; no owner, custody, database, native process, actual
project module or network is opened. One original 50 wall / 30 CPU seconds
covers this entire control invocation. Root selects any execution separately.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
from contextlib import ExitStack
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
from unittest.mock import patch

MIB = 1024**2
EXPECTED_HELPER_SHA256 = "09394f523417406aefcad0b47d06fa2d7782940bec3bb5094975f08b68f94ca8"
BRIDGE = "DMKNBridge_450bf7c15f3af7aa703934147ce9cd2fa1fbb5a50ec2dca7f7e41bbf1714f458"
FORBIDDEN_ATTEMPTS = []


def need(condition, code):
    if not condition:
        raise AssertionError(code)


class Allowance:
    deadline = START_WALL+50

    def check(self):
        need(time.monotonic() < self.deadline and time.process_time()-START_CPU < 30,
             "RETURN_CONTROL_ORIGINAL_ALLOWANCE")


def forbidden(label):
    def refuse(*_, **__):
        FORBIDDEN_ATTEMPTS.append(label)
        raise AssertionError("RETURN_CONTROL_FORBIDDEN:"+label)
    return refuse


def read(path, maximum=2*MIB):
    need(path.is_absolute() and ".." not in path.parts, "RETURN_CONTROL_ABSOLUTE")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "RETURN_CONTROL_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "RETURN_CONTROL_REGULAR")
    size = path.stat().st_size
    need(0 < size <= maximum, "RETURN_CONTROL_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "RETURN_CONTROL_CHANGED")
    return raw


def selected_package(args, allowance):
    root = Path(args.package)
    raw = read(root/"PROFILE.json")
    need(hashlib.sha256(raw).hexdigest() == args.profile_sha256, "RETURN_CONTROL_PROFILE_PIN")
    descriptor = json.loads(raw)
    path, name = root/"owner.py", "_project_return_controls_owner"
    source, pin = read(path), descriptor["files"]["owner.py"]
    need(len(source) == pin["bytes"] and hashlib.sha256(source).hexdigest() == pin["sha256"] and
         name not in sys.modules, "RETURN_CONTROL_OWNER_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    owner = importlib.util.module_from_spec(spec)
    sys.modules[name] = owner
    exec(compile(source, str(path), "exec"), owner.__dict__)
    loader = owner.bootstrap(root, args.profile_sha256, allowance.check)
    loaded = loader.load(root, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        allowance.deadline, check_parent=allowance.check)
    need(loaded.G.A is loaded.A and
         loaded.descriptor["files"]["authoring/py/ordinary_contribution.py"]["sha256"] ==
         EXPECTED_HELPER_SHA256, "RETURN_CONTROL_SELECTED_HELPER")
    return loaded


def refuses(code, call):
    try:
        call()
    except ValueError as error:
        need(str(error) == code, "RETURN_CONTROL_WRONG_REFUSAL:"+str(error))
        return
    raise AssertionError("RETURN_CONTROL_MISSING_REFUSAL:"+code)


def controls(G, output):
    config = {"schema": G.PROJECT_SCHEMA, "module_name": "NewWork.Contribution",
        "project_cwd": str(output), "project_search_paths": [str(output)],
        "imports": [{"module": BRIDGE, "meta": False}]}

    def imported(value, **changes):
        return G.TrustedProjectAuthoring.from_document(dict(config,
            imports=[{"module": value, "meta": False}], **changes))

    def import_and_source():
        need(len(BRIDGE) == 75 and G._project_module(BRIDGE, allow_bridge_import=True) == BRIDGE,
             "RETURN_CONTROL_EXACT_75_CHARACTER_IMPORT")
        backend = G.TrustedProjectAuthoring.from_document(config)
        need(backend.to_document() == config and backend.module_path() == Path("NewWork/Contribution.lean") and
             backend.import_bytes() == ("public import "+BRIDGE+"\n").encode("ascii"),
             "RETURN_CONTROL_CLOSED_CONFIG_ROUNDTRIP")
        parameters = dict(source_body=b"-- unchanged new-declaration body\n",
            request_directory=output/"request", semantic_id="1"*64, context_root="2"*64,
            foundation_id="3"*64, targets_file=output/"targets.json",
            candidate_file=output/"candidate.json")
        ordinary = G.assemble_source(**parameters)
        generated = G.assemble_source(**parameters, authoring_backend=backend)
        inserted = ("public import "+BRIDGE+"\n").encode("ascii")
        need(generated == ordinary.replace(b"\n\npublic section", b"\n"+inserted+b"\npublic section", 1)
             and generated.index(inserted) < generated.index(b"#ordinary_construct_portable "),
             "RETURN_CONTROL_ONLY_EXACT_IMPORT_HEADER_DELTA")
        meta = G.TrustedProjectAuthoring.from_document(dict(config,
            imports=[{"module": BRIDGE, "meta": True}]))
        need(meta.import_bytes() == ("public meta import "+BRIDGE+"\n").encode("ascii"),
             "RETURN_CONTROL_EXISTING_EXPLICIT_META_FIELD")

    def exception_import_only():
        refuses("CONTRIBUTION_PROJECT_MODULE_NAME", lambda: G._project_module(BRIDGE))
        refuses("CONTRIBUTION_PROJECT_MODULE_NAME", lambda:
            G.TrustedProjectAuthoring.from_document(dict(config, module_name=BRIDGE)))
        direct = G.TrustedProjectAuthoring(BRIDGE, output, (output,), ((BRIDGE, False),))
        refuses("CONTRIBUTION_PROJECT_MODULE_NAME", direct.to_document)
        refuses("CONTRIBUTION_PROJECT_MODULE_NAME", direct.module_path)
        refuses("CONTRIBUTION_PROJECT_MODULE_NAME", lambda:
            G._project_module(BRIDGE, allow_bridge_import=1))
        refuses("CONTRIBUTION_PROJECT_FIELDS", lambda:
            G.TrustedProjectAuthoring.from_document(dict(config, allow_bridge_import=True)))

    def exact_grammar_and_old_bounds():
        bad = ["DMKNBridge_"+"a"*63, "DMKNBridge_"+"a"*65,
            "DMKNBridge_"+"A"*64, "DMKNBridge_"+"g"*64,
            "DMKNBridgE_"+"a"*64, "X."+BRIDGE, BRIDGE+".X", BRIDGE+"\n",
            BRIDGE+" ", BRIDGE+";", "../"+BRIDGE, "X/"+BRIDGE, "X\\"+BRIDGE,
            BRIDGE[:-1]+"\u00e9", "A"*65, "Project.CON", "Project..Bad"]
        for name in bad:
            refuses("CONTRIBUTION_PROJECT_MODULE_NAME", lambda name=name: imported(name))
        # These are ordinary identifiers, not rejected merely for resembling a bridge.
        total_256 = ".".join(("A"*63, "B"*63, "C"*63, "D"*64))
        ordinary = ("A"*64, "DMKNBridge_"+"a"*52, "DMKNBridge_"+"a"*53,
                    "Project.Support", ".".join(["A"]*16), total_256)
        need(len(total_256) == 256, "RETURN_CONTROL_TOTAL_BOUND_FIXTURE")
        for name in ordinary:
            need(G._project_module(name) == name and
                 G._project_module(name, allow_bridge_import=True) == name and
                 imported(name).imports == ((name, False),), "RETURN_CONTROL_OLD_GRAMMAR:"+name)
        for name in (total_256+"E", ".".join(["A"]*17)):
            refuses("CONTRIBUTION_PROJECT_MODULE_NAME", lambda name=name: imported(name))

    def closed_fields_paths_and_counts():
        many = [{"module": "Module"+str(index), "meta": False} for index in range(63)]
        many.append({"module": BRIDGE, "meta": False})
        need(len(G.TrustedProjectAuthoring.from_document(dict(config, imports=many)).imports) == 64,
             "RETURN_CONTROL_IMPORT_COUNT_EDGE")
        paths = [str(output/("Path"+str(index))) for index in range(16)]
        need(len(G.TrustedProjectAuthoring.from_document(dict(config,
            project_search_paths=paths)).project_search_paths) == 16,
             "RETURN_CONTROL_SEARCH_COUNT_EDGE")
        cases = [(dict(config, imports=many+[{"module": "Extra", "meta": False}]),
                    "CONTRIBUTION_PROJECT_IMPORTS"),
            (dict(config, imports=config["imports"]*2), "CONTRIBUTION_PROJECT_DUPLICATE_IMPORT"),
            (dict(config, imports=[{"module": BRIDGE, "meta": 1}]), "CONTRIBUTION_PROJECT_META"),
            (dict(config, imports=[{"module": BRIDGE, "meta": False, "allow_bridge_import": True}]),
                    "CONTRIBUTION_PROJECT_IMPORT_FIELDS"),
            (dict(config, project_cwd="relative"), "CONTRIBUTION_PROJECT_CWD"),
            (dict(config, project_search_paths=[str(output)+";other"]), "CONTRIBUTION_PROJECT_SEARCH_PATHS"),
            (dict(config, project_search_paths=[str(output), str(output)]), "CONTRIBUTION_PROJECT_SEARCH_PATHS"),
            (dict(config, project_search_paths=paths+[str(output/"Path16")]), "CONTRIBUTION_PROJECT_SEARCH_PATHS")]
        for document, code in cases:
            refuses(code, lambda document=document: G.TrustedProjectAuthoring.from_document(document))

    return [("exact-generated-import-roundtrip-and-source-header", import_and_source),
            ("exception-import-only-not-output-or-user-mode", exception_import_only),
            ("exact-bridge-grammar-and-preserved-ordinary-bounds", exact_grammar_and_old_bounds),
            ("closed-fields-paths-and-counts-with-bridge-import", closed_fields_paths_and_counts)]


def main(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "RETURN_CONTROL_PYTHON")
    allowance, rows = Allowance(), []
    with ExitStack() as guards:
        for obj, method, label in ((sqlite3, "connect", "database"),
                (subprocess, "Popen", "child-process"),
                (socket.socket, "connect", "socket-connect"),
                (socket.socket, "connect_ex", "socket-connect-ex"),
                (socket.socket, "bind", "socket-bind"),
                (socket.socket, "listen", "socket-listen"),
                (socket.socket, "sendto", "socket-sendto")):
            guards.enter_context(patch.object(obj, method, forbidden(label)))
        loaded = selected_package(args, allowance)
        for obj, method, label in ((loaded.O, "OrdinaryStore", "real-custody"),
                (loaded.A.OrdinaryAdmission, "open", "real-owner"),
                (loaded.A.OrdinaryAdmission, "initialize", "initialization"),
                (loaded.A.OrdinaryAdmission, "preflight", "preflight"),
                (loaded.A.OrdinaryAdmission, "admit", "admission"),
                (loaded.G, "contribute_source", "contribution"),
                (loaded.installation._supervisor, "supervise", "native-supervision"),
                (loaded.peer_api.H, "exchange", "peer-exchange"),
                (loaded.peer_api.H.Provider, "start", "peer-provider")):
            guards.enter_context(patch.object(obj, method, forbidden(label)))
        output = loaded.A.C.ordinary(Path(args.output), directory=True)
        for protected in (loaded.root, *loaded.installation.runtime_roots.values()):
            need(not output.is_relative_to(protected) and not protected.is_relative_to(output),
                 "RETURN_CONTROL_OUTPUT_OVERLAP")
        for name, control in controls(loaded.G, output):
            allowance.check()
            try:
                control(); allowance.check()
                rows.append({"group": name, "ok": True})
            except BaseException as error:
                rows.append({"group": name, "ok": False, "error_type": type(error).__name__,
                             "error": str(error)[:1000]})
        loaded.profile.verify(allowance.check)
    report = {"ok": len(rows) == 4 and all(row["ok"] for row in rows) and not FORBIDDEN_ATTEMPTS,
        "groups": rows, "profile_sha256": args.profile_sha256,
        "helper_sha256": EXPECTED_HELPER_SHA256, "implementation_id": loaded.installation.implementation_id,
        "native_operations": 0, "owner_opens": 0, "custody_opens": 0,
        "forbidden_attempts": FORBIDDEN_ATTEMPTS,
        "wall_seconds": time.monotonic()-START_WALL,
        "controller_cpu_seconds": time.process_time()-START_CPU,
        "claim": "PURE_CONFIGURATION_AND_SOURCE_ASSEMBLY_NOT_PROJECT_EXECUTION_OR_MATHEMATICAL_ACCEPTANCE"}
    allowance.check()
    raw = json.dumps(report, sort_keys=True, ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(raw) <= MIB, "RETURN_CONTROL_REPORT_BOUND")
    with (output/"PROJECT-RETURN-CONTROLS.json").open("xb") as stream:
        stream.write(raw)
    print(raw.decode("ascii"), flush=True)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    raise SystemExit(main(parser.parse_args()))

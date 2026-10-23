"""Five native-free controls for one selected trusted-project package.

The real profile loader is exercised once. Explicit mocks inspect author-worker
invocations and CLI forwarding; guards prohibit subprocesses, databases and peer
connections. No Lean execution, project compatibility or mathematics is claimed.
Root must select this source and an outer finite process envelope before use.
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
from types import SimpleNamespace
from unittest.mock import patch

MIB = 1024**2


def need(condition, code):
    if not condition:
        raise AssertionError(code)


class Allowance:
    deadline = START_WALL+50

    def check(self):
        need(time.monotonic() < self.deadline and time.process_time()-START_CPU < 30,
             "PROJECT_CONTROL_ORIGINAL_ALLOWANCE")


def forbidden(*_, **__):
    raise AssertionError("PROJECT_CONTROL_FORBIDDEN_EXTERNAL_OPERATION")


def read(path, maximum=2*MIB):
    need(path.is_absolute() and ".." not in path.parts, "PROJECT_CONTROL_ABSOLUTE_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "PROJECT_CONTROL_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PROJECT_CONTROL_REGULAR_FILE")
    size = path.stat().st_size
    need(0 < size <= maximum, "PROJECT_CONTROL_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "PROJECT_CONTROL_FILE_CHANGED")
    return raw


def save(path, value):
    raw = value if type(value) is bytes else json.dumps(value, sort_keys=True,
        ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode("ascii")
    need(0 < len(raw) <= MIB, "PROJECT_CONTROL_OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def module(path, name, pin):
    raw = read(path)
    need(len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"],
         "PROJECT_CONTROL_CODE_PIN")
    need(name not in sys.modules, "PROJECT_CONTROL_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    exec(compile(raw, str(path), "exec"), result.__dict__)
    return result


def selected_package(args, allowance):
    root = Path(args.package)
    raw = read(root/"PROFILE.json")
    need(hashlib.sha256(raw).hexdigest() == args.profile_sha256, "PROJECT_CONTROL_PROFILE_PIN")
    descriptor = json.loads(raw)
    owner = module(root/"owner.py", "_project_controls_owner", descriptor["files"]["owner.py"])
    loader = owner.bootstrap(root, args.profile_sha256, allowance.check)
    loaded = loader.load(root, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        allowance.deadline, check_parent=allowance.check)
    worker = module(root/"author_worker.py", "_project_controls_worker",
                    loaded.descriptor["files"]["author_worker.py"])
    need(loaded.G.A is loaded.A and loaded.peer_api.A is loaded.A,
         "PROJECT_CONTROL_SHARED_CORE")
    return owner, loader, loaded, worker


def refuses(code, call):
    try:
        call()
    except ValueError as error:
        need(str(error) == code, "PROJECT_CONTROL_WRONG_REFUSAL:"+str(error))
        return
    raise AssertionError("PROJECT_CONTROL_EXPECTED_REFUSAL:"+code)


def controls(args, owner, loaded, worker, output, allowance):
    G, A = loaded.G, loaded.A
    fixture = output/"fixture"
    fixture.mkdir()
    cwd, project, source_root, build, catalog, custody = (fixture/name for name in
        ("project-cwd", "project-compiled", "generated-source", "build", "catalog", "custody"))
    for path in (cwd, project, source_root, build, catalog, custody):
        path.mkdir()
    source_dir = source_root/"NewWork"
    source_dir.mkdir()
    source = source_dir/"Contribution.lean"
    save(source, b"-- INERT CONTROL FILE; NEVER COMPILED\n")
    candidate = fixture/"candidate.json"
    config = {"schema": G.PROJECT_SCHEMA, "module_name": "NewWork.Contribution",
        "project_cwd": str(cwd), "project_search_paths": [str(project)],
        "imports": [{"module": "Project.Support", "meta": False},
                    {"module": "Project.Tactics", "meta": True}]}
    backend = G.TrustedProjectAuthoring.from_document(config)
    backend.verify(allowance.check)

    def owner_json():
        need(owner.project_json(json.dumps(config).encode()) == config, "PROJECT_CONTROL_JSON_ROUNDTRIP")
        for raw, code in ((b'{"x":true,"x":false}', "OWNER_PROJECT_JSON_DUPLICATE"),
                          (b'{"x":1}', "OWNER_PROJECT_JSON_NUMBER"),
                          (b'{"x":NaN}', "OWNER_PROJECT_JSON_NUMBER"),
                          (b'['*9+b']'*9, "OWNER_PROJECT_JSON_DEPTH"),
                          (b'{"x":', "OWNER_PROJECT_JSON_UNTERMINATED"),
                          (b'{"x":]}', "OWNER_PROJECT_JSON_BRACKETS"),
                          (b'{"x":"\xff"}', "OWNER_PROJECT_JSON_SYNTAX")):
            refuses(code, lambda raw=raw: owner.project_json(raw))

    def backend_and_source():
        need(backend.to_document() == config and backend.module_path() == Path("NewWork/Contribution.lean"),
             "PROJECT_CONTROL_CLOSED_ROUNDTRIP")
        for bad in ("../Outside", "Project..Bad", "Project.Bad\nrun_cmd", "Project.CON", "X."*130):
            refuses("CONTRIBUTION_PROJECT_MODULE_NAME", lambda bad=bad:
                G.TrustedProjectAuthoring.from_document(dict(config, module_name=bad)))
        for field, bad, code in (("extra", True, "CONTRIBUTION_PROJECT_FIELDS"),
                ("schema", "other", "CONTRIBUTION_PROJECT_SCHEMA"),
                ("project_cwd", "relative", "CONTRIBUTION_PROJECT_CWD"),
                ("project_search_paths", [str(project)]*2, "CONTRIBUTION_PROJECT_SEARCH_PATHS"),
                ("project_search_paths", [str(project)+";other"], "CONTRIBUTION_PROJECT_SEARCH_PATHS"),
                ("imports", [], "CONTRIBUTION_PROJECT_IMPORTS"),
                ("imports", [{"module": "Project.Support\nrun_cmd", "meta": False}],
                    "CONTRIBUTION_PROJECT_MODULE_NAME"),
                ("imports", [{"module": "Project.Support", "meta": 1}], "CONTRIBUTION_PROJECT_META"),
                ("imports", [config["imports"][0]]*2, "CONTRIBUTION_PROJECT_DUPLICATE_IMPORT"),
                ("imports", [{"module": "Project.Support", "meta": False, "code": "x"}],
                    "CONTRIBUTION_PROJECT_IMPORT_FIELDS")):
            refuses(code, lambda field=field, bad=bad:
                G.TrustedProjectAuthoring.from_document(dict(config, **{field: bad})))
        parameters = dict(source_body=b"-- exact caller body\n", request_directory=fixture/"request",
            semantic_id="1"*64, context_root="2"*64, foundation_id="3"*64,
            targets_file=fixture/"targets.json", candidate_file=candidate)
        quote = lambda value: json.dumps(str(value)).encode("ascii")
        expected = (b"module\n\npublic import Init\npublic meta import PortableOwnerConstructCommand\n"
            b"public meta import PortableContributionExportCommand\n\npublic section\n\n"
            b"#ordinary_construct_portable " + b" ".join(quote(parameters[key]) for key in
                ("request_directory", "semantic_id", "context_root", "foundation_id")) + b"\n\n"
            + parameters["source_body"] + b"\n\n#ordinary_export_contribution "
            + quote(parameters["targets_file"]) + b" " + quote(candidate) + b"\n")
        need(G.assemble_source(**parameters) == expected, "PROJECT_CONTROL_DEFAULT_SOURCE_BYTES")
        generated = G.assemble_source(**parameters, authoring_backend=backend)
        insertion = b"public import Project.Support\npublic meta import Project.Tactics\n"
        need(generated == expected.replace(b"\n\npublic section", b"\n"+insertion+b"\npublic section", 1),
             "PROJECT_CONTROL_EXACT_PROJECT_HEADER_ONLY")
        refuses("CONTRIBUTION_AUTHORING_BACKEND", lambda:
            G.assemble_source(**parameters, authoring_backend=lambda: None))

    def worker_invocations():
        lean = loaded.installation.path("lean")
        helpers = loaded.profile.helper_paths
        worker_args = [str(lean), str(source), str(build), os.pathsep.join(map(str, helpers)), str(candidate)]
        captures = []
        def capture(argv, **kwargs):
            captures.append((argv, kwargs)); return 17
        with patch.dict(os.environ, {"LEAN_PATH": "unselected", "LEAN_SRC_PATH": "unselected",
                "PYTHONPATH": "unselected", "PATH": "unselected"}), patch.object(subprocess, "call", capture):
            need(worker.author_worker(worker_args) == 17, "PROJECT_CONTROL_DEFAULT_WORKER_RETURN")
            default_argv, default_kw = captures.pop()
            need(default_argv == [str(lean), "-DElab.async=false", "-R", str(source.parent),
                "-o", str(build/"OrdinaryProducer.olean"), str(source)] and default_kw["cwd"] == Path.cwd()
                and default_kw["env"]["LEAN_PATH"] == os.pathsep.join(map(str, helpers)),
                "PROJECT_CONTROL_DEFAULT_ARGV_COMPATIBILITY")
            project_args = [*worker_args, str(source_root), str(cwd), str(project)]
            need(worker.project_author_worker(project_args) == 17, "PROJECT_CONTROL_WORKER_RETURN")
            argv, options = captures.pop()
            need(argv == [str(lean), "-DElab.async=false", "-R", str(source_root),
                "-o", str(build/"OrdinaryProducer.olean"), str(source)] and options["cwd"] == cwd
                and cwd != source_root, "PROJECT_CONTROL_EXPLICIT_MODULE_ROOT_AND_CWD")
            need(options["env"]["LEAN_PATH"].split(os.pathsep) ==
                [*map(str, helpers), str(lean.parent.parent/"lib/lean"), str(project)],
                "PROJECT_CONTROL_HELPER_RUNTIME_PRECEDENCE")
            for options in (default_kw, options):
                need(not any(key.upper().startswith("PYTHON") or key.upper().startswith("LEAN")
                    and key != "LEAN_PATH" for key in options["env"]), "PROJECT_CONTROL_AMBIENT_SCRUB")
                need(options["env"]["PATH"] == os.pathsep.join((str(Path(sys.executable).parent), str(lean.parent)))
                    and options["stdin"] == subprocess.DEVNULL
                    and options["creationflags"] == subprocess.CREATE_NO_WINDOW,
                    "PROJECT_CONTROL_FINITE_WORKER_INVOCATION")
            wrong_root = [*project_args]; wrong_root[5] = str(cwd)
            refuses("OWNER_PROJECT_WORKER_INPUTS", lambda: worker.project_author_worker(wrong_root))
            duplicate = [*project_args]; duplicate[7] = os.pathsep.join([str(project)]*2)
            refuses("OWNER_PROJECT_WORKER_PATHS", lambda: worker.project_author_worker(duplicate))
            need(not captures, "PROJECT_CONTROL_REFUSAL_DISPATCHED")

    source_body, acquired, names, limits = (fixture/name for name in
        ("Body.lean", "acquired.json", "names.json", "custody-limits.json"))
    save(source_body, b"theorem freshTarget : True := True.intro\n")
    save(acquired, [])
    save(names, [[[0, {"$bytes": list(b"freshTarget")}]]])
    save(limits, {name: bounds[0] for name, bounds in loaded.O.STORE_LIMITS.items()})
    store_id = "4"*64
    save(catalog/"ADOPTION.json", {"schema": A.P.SCHEMA, "store_id": store_id,
        "implementation": loaded.installation.doc["implementation"], "limits": vars(A.P.Limits())})
    config_file = fixture/"project.json"
    config_pin = save(config_file, config)
    invalid_file = fixture/"invalid-project.json"
    invalid_pin = save(invalid_file, dict(config, schema="invalid"))

    def call_args(**changes):
        selected = dict(operation="contribute", profile_sha256=args.profile_sha256,
            python_runtime=args.python_runtime, lean_runtime=args.lean_runtime,
            catalog=str(catalog), custody=str(custody), store_id=store_id, custody_limits=str(limits),
            wall_seconds=50, cpu_seconds=30, memory_mib=256, catalog_limits=None,
            parent_root="5"*64, source=str(source_body), acquired_targets=str(acquired),
            output_names=str(names), output=str(fixture/"not-created"), context_root=None,
            after_root="", limit=32, project_authoring=None, project_authoring_sha256=None)
        return SimpleNamespace(**(selected | changes))

    def preopen_cli_refusals():
        cases = [({"project_authoring": str(config_file)}, "OWNER_PROJECT_AUTHORING_ARGUMENTS"),
            ({"project_authoring_sha256": config_pin}, "OWNER_PROJECT_AUTHORING_ARGUMENTS"),
            ({"project_authoring": str(config_file), "project_authoring_sha256": "0"*64},
                "OWNER_PROJECT_AUTHORING_PIN"),
            ({"project_authoring": str(invalid_file), "project_authoring_sha256": invalid_pin},
                "CONTRIBUTION_PROJECT_SCHEMA")]
        fake_loader = SimpleNamespace(load=lambda *_, **__: loaded)
        with patch.object(owner, "bootstrap", lambda *_, **__: fake_loader), \
                patch.object(loaded.O, "OrdinaryStore", forbidden), \
                patch.object(A.OrdinaryAdmission, "open", forbidden):
            for changes, code in cases:
                report = owner.run(call_args(**changes))
                need(report["ok"] is False and report["phase"] == "SUPPORT"
                    and report["error"] == code, "PROJECT_CONTROL_PREOPEN_REFUSAL:"+str(report))
            for operation in ("init", "status"):
                report = owner.run(call_args(operation=operation, parent_root=None, source=None,
                    acquired_targets=None, output_names=None, output=None,
                    project_authoring=str(config_file), project_authoring_sha256=config_pin))
                need(report["ok"] is False and report["phase"] == "SUPPORT" and
                    report["error"] == "OWNER_PROJECT_AUTHORING_ARGUMENTS",
                    "PROJECT_CONTROL_CONTRIBUTE_ONLY_SELECTION")
        need(not (fixture/"not-created").exists(), "PROJECT_CONTROL_NO_CONTRIBUTION_OUTPUT")

    def cli_forwarding():
        captured = []
        fake_loader = SimpleNamespace(load=lambda *_, **__: loaded)
        fake_state = SimpleNamespace(close=lambda: None)
        def contribute(*positional, **keywords):
            captured.append((positional, keywords))
            return {"admission": {"status": "CHECKED", "local_root": "6"*64}, "claim": "MOCK_ONLY"}
        with patch.object(owner, "bootstrap", lambda *_, **__: fake_loader), \
                patch.object(loaded.O, "OrdinaryStore", lambda *_, **__: fake_state), \
                patch.object(A.OrdinaryAdmission, "open", lambda *_, **__: fake_state), \
                patch.object(G, "contribute_source", contribute):
            default = owner.run(call_args())
            selected = owner.run(call_args(project_authoring=str(config_file), project_authoring_sha256=config_pin))
        need(default["ok"] and selected["ok"] and len(captured) == 2, "PROJECT_CONTROL_MOCKED_FORWARDING")
        need("authoring_backend" not in captured[0][1] and
            captured[1][1]["authoring_backend"] == backend, "PROJECT_CONTROL_EXPLICIT_BACKEND_ONLY")
        need("project_authoring_selection" not in default and selected["project_authoring_selection"] ==
            {"file": str(config_file), "sha256": config_pin}, "PROJECT_CONTROL_CONFIG_REPORT_SELECTION")

    return [("owner-json", owner_json), ("closed-backend-and-source", backend_and_source),
            ("mocked-worker-invocations", worker_invocations),
            ("preopen-cli-refusals", preopen_cli_refusals), ("mocked-cli-forwarding", cli_forwarding)]


def main(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PROJECT_CONTROL_PYTHON")
    allowance = Allowance()
    rows = []
    with ExitStack() as guards:
        guards.enter_context(patch.object(sqlite3, "connect", forbidden))
        guards.enter_context(patch.object(subprocess, "Popen", forbidden))
        guards.enter_context(patch.object(socket.socket, "connect", forbidden))
        guards.enter_context(patch.object(socket.socket, "connect_ex", forbidden))
        owner, loader, loaded, worker = selected_package(args, allowance)
        guards.enter_context(patch.object(loaded.peer_api.H, "exchange", forbidden))
        guards.enter_context(patch.object(loaded.peer_api.H.Provider, "start", forbidden))
        output = loaded.A.C.ordinary(Path(args.output), directory=True)
        for protected in (loaded.root, *loaded.installation.runtime_roots.values()):
            need(not output.is_relative_to(protected) and not protected.is_relative_to(output),
                 "PROJECT_CONTROL_OUTPUT_OVERLAP")
        for name, control in controls(args, owner, loaded, worker, output, allowance):
            allowance.check()
            try:
                control(); allowance.check()
                rows.append({"group": name, "ok": True})
            except BaseException as error:
                rows.append({"group": name, "ok": False, "error_type": type(error).__name__,
                             "error": str(error)[:1000]})
    report = {"ok": len(rows) == 5 and all(row["ok"] for row in rows), "groups": rows,
        "profile_sha256": args.profile_sha256, "implementation_id": loaded.installation.implementation_id,
        "wall_seconds": time.monotonic()-START_WALL, "controller_cpu_seconds": time.process_time()-START_CPU,
        "native_operations": 0, "owner_opens": 0,
        "claim": "EXPLICIT_MOCKS_NOT_PROJECT_COMPATIBILITY_OR_MATHEMATICAL_ACCEPTANCE"}
    save(output/"PROJECT-CONTROLS.json", report)
    print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    raise SystemExit(main(parser.parse_args()))

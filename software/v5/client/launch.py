"""Trusted local owner launcher; reuse the fixed release's bounded Windows Job.

This is not a remote executable API or a hostile-code sandbox. The small outer
bootstrap is separately measured; all client setup runs in the attached child.
"""
from __future__ import annotations
import time
STARTED_NS, STARTED_CPU = time.monotonic_ns(), time.process_time()
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

MIB = 1024**2
MANIFEST_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
HELPERS = {"_dmkn_client_supervisor": "operator/commons.py", "domains": "receiver/helpers/domains.py",
           "_dmkn_client_job": "receiver/helpers/run_stage.py"}
SOURCE_MAX, SOURCE_TOTAL, SOURCE_COUNT = 2*MIB, 64*MIB, 512
PORTABLE = frozenset(("__init__.py", "controller.py", "controller_services.py", "protocol.py",
    "workflow.py", "available_descriptor.py", "observed_route.py", "protocol.mjs", "framing.mjs",
    "intent.mjs", "runtime.mjs", "maintained.mjs", "transport.mjs", "composition.mjs", "ipc_wire.mjs",
    "node_entry.mjs", "maintained_roles.mjs", "role_composition.mjs", "node_entry_roles.mjs",
    "services_composition.mjs", "node_entry_services.mjs"))


def need(ok, code):
    if not ok: raise ValueError(code)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "CLIENT_DUPLICATE_KEY")
            result[key] = value
        return result
    def reject(value): raise ValueError("CLIENT_NONINTEGER_JSON_NUMBER")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=reject, parse_constant=reject)


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":"
         and path != Path(path.anchor) and str(path.resolve()) == str(path), "CLIENT_CANONICAL_LOCAL_PATH")
    for part in path.parts[1:]:
        need(part not in (".", "..") and not part.endswith((".", " ")) and not os.path.isreserved(part)
             and not any(ord(c) < 32 or c in ':*?"<>|' for c in part), "CLIENT_PATH_COMPONENT")
    for ancestor in path.parents:
        info = ancestor.lstat()
        need(stat.S_ISDIR(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "CLIENT_ORDINARY_ANCESTOR")
    if fresh:
        need(not path.exists() and not path.is_symlink() and not path.is_junction(), "CLIENT_FRESH_PATH")
    else:
        info = path.lstat()
        need(not getattr(info, "st_file_attributes", 0) & 0x400 and
             (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)), "CLIENT_ORDINARY_TARGET")
    return path


def read(path, maximum, *, allow_empty=False):
    path = ordinary(path)
    size = path.stat().st_size
    need((0 if allow_empty else 1) <= size <= maximum, "CLIENT_FILE_SIZE")
    with path.open("rb") as stream: raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "CLIENT_FILE_CHANGED")
    return raw


def relative(value):
    need(type(value) is str and 0 < len(value) <= 1024 and "\\" not in value, "CLIENT_RELATIVE_PATH")
    path = PurePosixPath(value)
    need(path.parts and not path.is_absolute() and path.as_posix() == value and
         all(part not in (".", "..") and not part.endswith((".", " ")) and not os.path.isreserved(part)
             and not any(ord(c) < 32 or c in ':*?"<>|' for c in part) for part in path.parts),
         "CLIENT_RELATIVE_COMPONENTS")
    return path.parts


def pin_row(row):
    need(type(row) is dict and set(row) == {"bytes", "sha256"}
         and type(row["bytes"]) is int and 0 <= row["bytes"] <= 128*MIB
         and type(row["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]), "CLIENT_PIN_ROW")
    return row


def pinned(path, row, maximum=128*MIB):
    pin_row(row)
    path = ordinary(path)
    need(path.stat().st_size == row["bytes"] <= maximum, "CLIENT_PIN_SIZE:"+str(path))
    with path.open("rb") as stream: digest = hashlib.file_digest(stream, "sha256").hexdigest()
    need(path.stat().st_size == row["bytes"] and digest == row["sha256"], "CLIENT_PIN:"+str(path))
    return path


def overlap(left, right): return left.is_relative_to(right) or right.is_relative_to(left)


def read_plan(path, expected):
    need(type(expected) is str and re.fullmatch(r"[0-9a-f]{64}", expected), "CLIENT_PLAN_SHA")
    raw = read(path, MIB); need(sha(raw) == expected, "CLIENT_PLAN_PIN")
    value = strict(raw)
    need(type(value) is dict and set(value) == {"schema", "name", "installation_root", "workspace_root",
         "source_roots", "sources", "owner_entry", "parameters", "limits", "output_limits"}
         and value["schema"] == "DMKN_V5_CLIENT_LAUNCH_V1", "CLIENT_PLAN_SCHEMA")
    need(type(value["name"]) is str and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", value["name"]), "CLIENT_RUN_NAME")
    installation = ordinary(value["installation_root"], directory=True)
    workspace = ordinary(value["workspace_root"], directory=True)
    need(type(value["source_roots"]) is dict and set(value["source_roots"]) == {"v5", "portable", "owner"},
         "CLIENT_SOURCE_ROOTS")
    roots = {key: ordinary(path, directory=True) for key, path in value["source_roots"].items()}
    run = workspace / value["name"]
    need(not any(overlap(run, root) for root in (installation, *roots.values())), "CLIENT_OUTPUT_IMMUTABLE_OVERLAP")
    sources = value["sources"]
    need(type(sources) is dict and 1 <= len(sources) <= SOURCE_COUNT, "CLIENT_SOURCE_COUNT")
    names, total = set(), 0
    for name, row in sources.items():
        parts = relative(name)
        need(2 <= len(parts) <= 32 and parts[0] in roots and name.casefold() not in names, "CLIENT_SOURCE_NAME")
        need(Path(parts[-1]).suffix.casefold() not in (".pyc", ".pyo", ".pyd"), "CLIENT_SOURCE_NOT_BYTECODE_OR_EXTENSION")
        names.add(name.casefold()); pin_row(row)
        need(row["bytes"] <= SOURCE_MAX, "CLIENT_SOURCE_FILE_BOUND"); total += row["bytes"]
    need(total <= SOURCE_TOTAL, "CLIENT_SOURCE_TOTAL_BOUND")
    need({"v5/client/launch.py", "v5/client/boot.py", "v5/client/workspace.py"} <= set(sources), "CLIENT_PUBLIC_SOURCE_REQUIRED")
    need({name for name in sources if name.startswith("portable/")} ==
         {"portable/location/"+name for name in PORTABLE}, "CLIENT_PORTABLE_CLOSURE")
    need(not any(name.startswith(("v5/location/", "v5/portable_runtime/")) for name in sources), "CLIENT_NO_SECOND_LOCATION")
    entry = "/".join(relative(value["owner_entry"]))
    need(entry.endswith(".py") and "owner/"+entry in sources, "CLIENT_OWNER_ENTRY")
    need(type(value["parameters"]) is dict and len(json.dumps(value["parameters"], ensure_ascii=True)) <= 65536,
         "CLIENT_OWNER_PARAMETERS")
    output = value["output_limits"]
    need(type(output) is dict and set(output) == {"bytes", "entries"}
         and type(output["bytes"]) is int and SOURCE_TOTAL <= output["bytes"] <= 2*1024**3
         and type(output["entries"]) is int and 1024 <= output["entries"] <= 32768, "CLIENT_OUTPUT_LIMITS")
    return value, raw, installation, workspace, roots, run


def load_manifest(installation):
    raw = read(installation / "RELEASE-MANIFEST.json", 8*MIB)
    need(sha(raw) == MANIFEST_SHA, "CLIENT_FIXED_RUNTIME_MANIFEST")
    files = strict(raw)["files"]
    need(type(files) is dict and 1 <= len(files) <= 20000, "CLIENT_FIXED_RUNTIME_MAP")
    return files, raw


def load_helper(name, path, row):
    need(name not in sys.modules, "CLIENT_BOOTSTRAP_MODULE_ALREADY_LOADED")
    pinned(path, row, 4*MIB); raw = read(path, 4*MIB)
    need(sha(raw) == row["sha256"], "CLIENT_BOOTSTRAP_SOURCE_CHANGED")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def boot_helpers(installation, files):
    modules = {name: load_helper(name, installation / path, files[path]) for name, path in HELPERS.items()}
    return modules["_dmkn_client_supervisor"], modules["_dmkn_client_job"]


def invocation(installation):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, "CLIENT_ISOLATED_WINDOWS_OWNER")
    executable = installation / "receiver/runtime/python/python.exe"
    need(str(Path(sys.executable).resolve()) == str(executable), "CLIENT_FIXED_PYTHON_EXECUTABLE")
    return executable


def output_census(run, limits):
    entries, total = 0, 0
    for parent, children, names in os.walk(run, followlinks=False):
        parent = ordinary(parent, directory=True)
        for child in children: ordinary(parent / child, directory=True)
        entries += len(children)+len(names)
        need(entries <= limits["entries"], "CLIENT_FINAL_OUTPUT_ENTRY_LIMIT")
        for name in names:
            total += ordinary(parent / name).stat().st_size
            need(total <= limits["bytes"], "CLIENT_FINAL_OUTPUT_BYTE_LIMIT")
    return {"entries": entries, "bytes": total}


def main():
    need(len(sys.argv) == 3, "CLIENT_USAGE_PLAN_AND_SHA")
    plan_path = ordinary(sys.argv[1])
    plan, raw, installation, workspace, roots, run = read_plan(plan_path, sys.argv[2])
    executable = invocation(installation)
    need(str(Path(__file__).resolve()) == str(roots["v5"] / "client/launch.py"), "CLIENT_LAUNCH_ORIGIN")
    files, manifest_raw = load_manifest(installation)
    for name in ("receiver/runtime/python/python.exe", "receiver/runtime/python/python314.dll"):
        pinned(installation / name, files[name])
    for name in ("launch.py", "boot.py"):
        pinned(roots["v5"] / "client" / name, plan["sources"]["v5/client/"+name], SOURCE_MAX)
    A, J = boot_helpers(installation, files)
    limits = A.limits_checked(plan["limits"])
    need(limits["wall_seconds"] <= 3600 and limits["cpu_seconds"] <= 86400
         and limits["memory_mib"] <= 4096, "CLIENT_FINITE_OPERATION_LIMITS")
    deadline_ns = STARTED_NS + limits["wall_seconds"]*1_000_000_000
    need(time.monotonic_ns() < deadline_ns and time.process_time()-STARTED_CPU <= 30, "CLIENT_BOOTSTRAP_LIMIT")
    ordinary(run, directory=True, fresh=True); run.mkdir()
    plan_copy = run / "plan.json"
    with plan_copy.open("xb") as stream: stream.write(raw)
    argv = [str(executable), "-I", "-S", "-B", str(roots["v5"] / "client/boot.py"),
            str(plan_copy), sys.argv[2], str(STARTED_NS), str(deadline_ns)]
    bootstrap_cpu = time.process_time()-STARTED_CPU
    need(time.monotonic_ns() < deadline_ns and bootstrap_cpu <= 30, "CLIENT_BOOTSTRAP_LIMIT")
    result = A.supervise(argv, installation, run / "command", limits, J.Job, started=STARTED_NS/1e9)
    status, final_error, observed_output = result["status"], None, None
    try:
        need(read(plan_path, MIB) == raw and read(plan_copy, MIB) == raw
             and read(installation / "RELEASE-MANIFEST.json", 8*MIB) == manifest_raw,
             "CLIENT_FINAL_BOOTSTRAP_CHANGED")
        for path in HELPERS.values(): pinned(installation / path, files[path], 4*MIB)
        for name in ("launch.py", "boot.py"):
            pinned(roots["v5"] / "client" / name, plan["sources"]["v5/client/"+name], SOURCE_MAX)
        if result["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED":
            need(not (run / "BOOT-FAILED.json").exists(), "CLIENT_BOOT_FAILURE_MARKER")
            boot = strict(read(run / "BOOT-RESULT.json", MIB))
            need(boot.get("schema") == "DMKN_V5_CLIENT_BOOT_RESULT_V1"
                 and boot.get("status") == "OWNER_EXITED_ZERO"
                 and boot.get("plan_sha256") == sys.argv[2], "CLIENT_BOOT_COMPLETION_REQUIRED")
        observed_output = output_census(run, plan["output_limits"])
        need(time.monotonic_ns() < deadline_ns and time.process_time()-STARTED_CPU <= 60,
             "CLIENT_FINAL_WRAPPER_LIMIT")
    except BaseException as error:
        status, final_error = "CLIENT_FINAL_BINDING_OR_LIMIT_FAILED", str(error)[:1000]
    report = {"schema": "DMKN_V5_CLIENT_LAUNCH_RESULT_V1", "status": status,
              "plan_sha256": sys.argv[2], "final_error": final_error, "observed_output": observed_output,
              "result": result, "bootstrap_cpu_seconds": bootstrap_cpu,
              "wrapper_cpu_seconds": time.process_time()-STARTED_CPU,
              "wall_seconds": (time.monotonic_ns()-STARTED_NS)/1e9,
              "pre_clock_interpreter_startup": "UNMEASURED_NOT_ZERO",
              "bootstrap_containment": "TRUSTED_FINITE_WRAPPER_NOT_INSIDE_CHILD_JOB",
              "authority": "OPERATIONAL_CLOSURE_NOT_MATHEMATICAL_ACCEPTANCE"}
    A.save_new(run / "RESULT.json", report)
    # Final report I/O is not permission to extend the operation.
    try:
        output_census(run, plan["output_limits"])
        need(time.monotonic_ns() < deadline_ns and time.process_time()-STARTED_CPU <= 60,
             "CLIENT_FINALIZATION_LIMIT")
    except BaseException as error:
        A.save_new(run / "FINALIZATION-FAILED.json", {"status": "CLIENT_FINALIZATION_LIMIT",
                                                     "error": str(error)[:1000]})
        return 1
    print(json.dumps(report, sort_keys=True), flush=True)
    return 0 if status == "COMMAND_EXITED_ZERO_AND_CLOSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())

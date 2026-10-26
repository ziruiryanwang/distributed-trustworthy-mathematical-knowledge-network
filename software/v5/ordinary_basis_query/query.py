"""Bounded approved-local Lean type extraction into fixed-basis search hints.

No owner, custody, network, proof admission or arbitrary project imports. Source
elaboration executes at account permissions; the Windows Job is not a sandbox.
Only the parent RESULT after clean closure authorizes using the candidate hints.
"""
from __future__ import annotations

import time
START, CPU_START = time.monotonic(), time.process_time()
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from types import SimpleNamespace

MIB = 1024**2
SCHEMA = "DMKN_ORDINARY_BASIS_QUERY_V1"
RUN_SHA = "47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39"
LIMITS = {"wall_seconds": 600, "cpu_seconds": 600, "memory_mib": 4096,
          "active_processes": 4, "stdout_bytes": MIB, "stderr_bytes": MIB}
ARTIFACTS = tuple("native/Query" + suffix for suffix in
                  (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig"))
OUTPUTS = {"native/Query.lean", "native/type.json", "BINDINGS.json", "QUERY.json", "SPECS.json", *ARTIFACTS}
REQUIRED_OUTPUTS = OUTPUTS - set(ARTIFACTS[1:])


def need(ok, code):
    if not ok:
        raise ValueError("BASIS_QUERY_" + code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def hexid(value):
    need(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value), "HASH")
    return value


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def strict_json(raw, *, reports=False):
    need(type(raw) is bytes and 0 < len(raw) <= MIB, "JSON_BOUND")
    depth, quoted, escaped = 0, False, False
    for byte in raw:
        if quoted:
            if escaped: escaped = False
            elif byte == 92: escaped = True
            elif byte == 34: quoted = False
        elif byte == 34: quoted = True
        elif byte in (91, 123):
            depth += 1; need(depth <= 24, "JSON_DEPTH")
        elif byte in (93, 125): depth -= 1
    def pairs(rows):
        result = {}
        for key, value in rows:
            need(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    def number(value):
        need(reports, "JSON_NUMBER")
        result = float(value); need(math.isfinite(result), "REPORT_NUMBER")
        return result
    def reject(_):
        raise ValueError("BASIS_QUERY_JSON_NUMBER")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=number, parse_constant=reject)


def validate_query(doc):
    need(type(doc) is dict and set(doc) == {"universes", "type"}, "QUERY_FIELDS")
    universes, term = doc["universes"], doc["type"]
    need(type(universes) is list and len(universes) <= 32 and
         all(type(u) is str and re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,63}", u)
             for u in universes) and len(set(universes)) == len(universes), "UNIVERSES")
    need(type(term) is str and term.strip() and "\0" not in term and
         len(term.encode("utf-8")) <= 65536, "TYPE_TEXT")
    return tuple(universes), term


def source_text(universes, type_text, native_output_path):
    universes, term = validate_query({"universes": list(universes), "type": type_text})
    path = str(native_output_path)
    need(0 < len(path) <= 32768 and all(ord(c) >= 32 for c in path), "LEAN_PATH_STRING")
    quoted = json.dumps(path.replace("\\", "/"), ensure_ascii=False)
    names = ["«" + name + "»" for name in universes]
    header = "module\n\npublic import Init\npublic meta import OwnerQueryCommand\n\npublic section\n"
    if names:
        header += "universe " + " ".join(names) + "\n"
    return (header + "\n#ordinary_type_query [" + ", ".join(names) + "] " + quoted +
            " : (\n" + term + "\n)\n").encode("utf-8")


def validate_config(doc):
    need(type(doc) is dict and set(doc) == {"schema", "package", "profile_sha256",
         "python_runtime", "lean_runtime", "query", "limits"} and doc["schema"] == SCHEMA,
         "CONFIG_FIELDS")
    for key in ("package", "python_runtime", "lean_runtime"):
        need(type(doc[key]) is str and 0 < len(doc[key]) <= 32767, "CONFIG_PATH")
    hexid(doc["profile_sha256"])
    query = doc["query"]
    need(type(query) is dict and set(query) == {"path", "sha256"} and
         type(query["path"]) is str and 0 < len(query["path"]) <= 32767, "QUERY_SELECTION")
    hexid(query["sha256"])
    limits = doc["limits"]
    need(type(limits) is dict and set(limits) == set(LIMITS) and
         all(type(v) is int and 1 <= v <= LIMITS[k] for k, v in limits.items()) and
         limits["wall_seconds"] >= 35 and limits["cpu_seconds"] >= 4 and
         limits["active_processes"] >= 2, "LIMITS")
    return strict_json(canonical(doc))


class UnknownVocabulary(ValueError):
    def __init__(self, names):
        self.names = names
        super().__init__("BASIS_QUERY_UNKNOWN_VOCABULARY")


def basis_bindings(Q, S, native_raw, inventory_raw, semantic_id, check):
    need(type(inventory_raw) is bytes and digest(inventory_raw) == S.INVENTORY, "INVENTORY_PIN")
    need(semantic_id == S.semantic_id() and Q.S is S, "SEMANTIC_PROFILE")
    inventory = strict_json(inventory_raw)
    need(type(inventory) is list and len(inventory) == 581, "INVENTORY_CENSUS")
    keys = set()
    for row in inventory:
        check(); need(type(row) is list and len(row) >= 1, "INVENTORY_ROW")
        key = Q.E.name_key(row[0]); need(key not in keys, "INVENTORY_DUPLICATE")
        keys.add(key)
    names = Q.reference_names(native_raw)
    missing = [name for name in names if Q.E.name_key(name) not in keys]
    if missing:
        raise UnknownVocabulary(missing)
    rows = []
    for name in names:
        check(); rows.append([name, S.basis_symbol_id(semantic_id, S.foundation_id(), name)])
    return Q.E.canonical_json(rows)


def make_hints(Q, S, native_raw, inventory_raw, semantic_id, check):
    bindings = basis_bindings(Q, S, native_raw, inventory_raw, semantic_id, check)
    query = Q.bind_native_type(native_raw, bindings, semantic_id=semantic_id)
    specs = Q.E.canonical_json([Q.query_spec(query)])
    check()
    return {"bindings_raw": bindings, "query_raw": query, "specs_raw": specs,
            "interpretation": {"semantic_id": semantic_id, "foundation_id": S.foundation_id(),
                "inventory_sha256": S.INVENTORY, "vocabulary": "EXACT_FIXED_BASIS_ONLY",
                "key_profile": Q.PROFILE_ID}}


def clean_supervision(report, limits=None):
    final = report.get("final_job") if type(report) is dict else None
    clean = (type(final) is dict and report.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED" and
            type(report.get("child_exit_code")) is int and report["child_exit_code"] == 0 and
            report.get("direct_child_reaped") is True and report.get("job_closed") is True and
            report.get("cleanup_errors") == [] and report.get("termination_requested") is False and
            all(type(final.get(k)) is int and final[k] == 0 for k in
                ("active_processes", "terminated_processes")) and
            type(final.get("cpu_seconds")) in (int, float) and
            math.isfinite(final["cpu_seconds"]) and final["cpu_seconds"] >= 0)
    if not clean or limits is None:
        return clean
    selected, logs = report.get("limits"), report.get("observed_logs")
    def finite(value):
        return type(value) in (int, float) and math.isfinite(value) and value >= 0
    return (type(selected) is dict and selected == limits and
            all(type(value) is int for value in selected.values()) and
            finite(report.get("wall_seconds_through_cleanup")) and
            report["wall_seconds_through_cleanup"] <= limits["wall_seconds"] and
            finite(report.get("wrapper_supervision_cpu_seconds")) and
            final["cpu_seconds"] <= limits["cpu_seconds"] and type(logs) is dict and
            set(logs) == {"stdout_bytes", "stderr_bytes"} and
            all(type(value) is int and 0 <= value <= limits[key] for key, value in logs.items()))


def initial_read(value, maximum):
    path = Path(value)
    need(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":" and
         path != Path(path.anchor) and len(path.parts) <= 128 and len(str(path)) <= 32767 and
         all(p not in (".", "..") and not p.endswith((".", " ")) and not os.path.isreserved(p)
             and not any(ord(c) < 32 or c in ':*?"<>|' for c in p) for p in path.parts[1:]),
         "BOOTSTRAP_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "BOOTSTRAP_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "BOOTSTRAP_KIND")
    need(path.resolve() == path and 0 < path.stat().st_size <= maximum, "BOOTSTRAP_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(0 < len(raw) <= maximum and path.stat().st_size == len(raw), "BOOTSTRAP_CHANGED")
    return raw


def load_source(name, path, raw):
    need(name not in sys.modules, "PRELOADED_SOURCE")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def setup(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON_PROFILE")
    need(args.approve_local_query is True, "LOCAL_EXECUTION_APPROVAL_REQUIRED")
    need(time.monotonic()-START < 35 and time.process_time()-CPU_START < 4, "INITIAL_ALLOWANCE")
    config_raw = initial_read(args.config, MIB)
    need(digest(config_raw) == hexid(args.config_sha256), "CONFIG_PIN")
    config = validate_config(strict_json(config_raw)); limits = config["limits"]
    origin = START
    if args.worker:
        need(type(args.origin) is float and math.isfinite(args.origin) and args.origin <= START and
             type(args.deadline) is float and math.isfinite(args.deadline) and
             args.deadline == args.origin + limits["wall_seconds"] - 5 and START < args.deadline,
             "WORKER_ORIGINAL_DEADLINE")
        origin = args.origin
    else:
        need(args.origin is None and args.deadline is None and args.entry_sha256 is None,
             "PRIVATE_WORKER_OPTIONS")
    deadline = origin + limits["wall_seconds"] - (5 if args.worker else 0)
    def check():
        need(time.monotonic() < deadline and
             time.process_time()-CPU_START < (limits["cpu_seconds"] if args.worker else min(30, limits["cpu_seconds"])),
             "ORIGINAL_ALLOWANCE_EXHAUSTED")
    check()
    entry = Path(__file__).absolute(); entry_raw = initial_read(entry, 2*MIB)
    if args.worker:
        need(digest(entry_raw) == hexid(args.entry_sha256), "WORKER_ENTRY_PIN")
    package = Path(config["package"]); launcher = package/"run.py"
    run_raw = initial_read(launcher, 2*MIB)
    need(digest(run_raw) == RUN_SHA, "SUPPORTED_LAUNCHER")
    R = load_source("_basis_query_launch_support", launcher, run_raw)
    package = R.ordinary(package, directory=True)
    python = R.ordinary(config["python_runtime"], directory=True)
    lean = R.ordinary(config["lean_runtime"], directory=True)
    output = R.ordinary(args.output, directory=True, fresh=not args.worker)
    config_path = R.ordinary(args.config); query_path = R.ordinary(config["query"]["path"])
    query_raw = R.read(query_path, MIB, check)
    need(digest(query_raw) == config["query"]["sha256"], "QUERY_PIN")
    universes, term = validate_query(strict_json(query_raw))
    R.separated([package, python, lean], "BASIS_QUERY_SUPPORT_OVERLAP")
    need(all(not R.overlap(output, p) for p in
             (package, python, lean, entry.parent, config_path, query_path)), "OUTPUT_INPUT_OVERLAP")
    bound = R.bind_support(package, config["profile_sha256"], python, check)
    check()
    return SimpleNamespace(R=R, config=config, config_raw=config_raw, config_path=config_path,
        query_raw=query_raw, query_path=query_path, package=package, python=python, lean=lean,
        entry=entry, entry_raw=entry_raw, limits=limits, output=output, bound=bound,
        origin=origin, deadline=deadline, check=check, universes=universes, term=term)


def save_bytes(path, raw, maximum=MIB):
    need(type(raw) is bytes and 0 < len(raw) <= maximum, "OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    need(initial_read(path, maximum) == raw, "OUTPUT_READBACK")


def recheck_inputs(s):
    for path, raw in ((s.config_path, s.config_raw), (s.query_path, s.query_raw), (s.entry, s.entry_raw)):
        need(s.R.read(path, 2*MIB, s.check) == raw, "INPUT_CHANGED")


def candidate_pins(s):
    with os.scandir(s.R.ordinary(s.output/"native", directory=True)) as rows:
        actual = set()
        for row in rows:
            s.check(); actual.add("native/" + row.name); need(len(actual) <= 7, "NATIVE_CENSUS_BOUND")
    allowed = {name for name in OUTPUTS if name.startswith("native/")}
    required = {name for name in REQUIRED_OUTPUTS if name.startswith("native/")}
    need(required <= actual <= allowed, "NATIVE_CENSUS")
    result, total = {}, 0
    for name in sorted(actual | {name for name in OUTPUTS if not name.startswith("native/")}):
        maximum = 16*MIB if name in ARTIFACTS else MIB
        raw = s.R.read(s.output/name, maximum, s.check); total += len(raw)
        need(total <= 64*MIB, "OUTPUT_TOTAL")
        result[name] = {"bytes": len(raw), "sha256": digest(raw)}
    return result


def worker(args):
    s = None
    report = {"schema": "DMKN_ORDINARY_BASIS_QUERY_WORKER_V1", "ok": False,
              "mathematical_acceptance": False, "supervised_completion": False}
    try:
        s = setup(args); R = s.R; s.check()
        profile = R.strict(R.read(s.package/"PROFILE.json", 2*MIB, s.check))
        owner_raw = R.bound_file(s.package/"owner.py", profile["files"]["owner.py"], s.check, source=True)
        owner = R.load_source("_basis_query_owner", s.package/"owner.py", owner_raw)
        loader = owner.bootstrap(s.package, s.config["profile_sha256"], s.check)
        loaded = loader.load(s.package, s.config["profile_sha256"],
            {"python_runtime": s.python, "lean_runtime": s.lean}, s.deadline, check_parent=s.check)
        Q, S = loaded.formal_query, loaded.A.S
        need(Q.S is S and Q.E is loaded.A.E, "LOADED_SHARED_SEMANTICS")
        native = s.output/"native"; R.ordinary(native, directory=True, fresh=True).mkdir()
        raw_source = source_text(s.universes, s.term, native/"type.json")
        save_bytes(native/"Query.lean", raw_source)
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith(
               ("LEAN", "PYTHON", "RUST", "CARGO", "RISC0", "NODE")) and k.upper() not in {"PATH", "VIRTUAL_ENV"}}
        env["PATH"] = os.pathsep.join(map(str, (s.python, s.python/"DLLs", s.lean/"bin")))
        env["LEAN_PATH"] = os.pathsep.join(map(str, (*loaded.profile.helper_paths, s.lean/"lib/lean")))
        argv = [str(loaded.installation.path("lean")), "-DElab.async=false", "-R", str(native),
                "-o", str(native/"Query.olean"), str(native/"Query.lean")]
        s.check()
        # Inherit the supervised worker streams: native output shares its log caps.
        code = subprocess.call(argv, cwd=native, env=env, stdin=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        s.check(); need(code == 0, "NATIVE_EXTRACTION_FAILED")
        native_raw = R.read(native/"type.json", MIB, s.check)
        hints = make_hints(Q, S, native_raw, loaded.installation.read("inventory", MIB),
                           loaded.installation.semantic_id, s.check)
        adapter = sys.modules["discovery.ordinary_export_adapter"]
        need(adapter.Q is Q, "LOADED_DISCOVERY_QUERY")
        namespace = adapter.namespace_for(loaded.installation.semantic_id)
        features = adapter.compile_query(namespace, strict_json(hints["specs_raw"]))
        for name, key in (("BINDINGS.json", "bindings_raw"), ("QUERY.json", "query_raw"), ("SPECS.json", "specs_raw")):
            save_bytes(s.output/name, hints[key])
        loaded.profile.verify(s.check)
        recheck_inputs(s)
        need(R.read(native/"Query.lean", MIB, s.check) == raw_source, "GENERATED_SOURCE_CHANGED")
        pins = candidate_pins(s); s.check()
        report.update(ok=True, status="CANDIDATE_HINTS_NOT_SUPERVISED_SUCCESS", files=pins,
            interpretation=hints["interpretation"], config_sha256=args.config_sha256,
            namespace=namespace, features=features,
            profile_sha256=s.config["profile_sha256"], entry_sha256=digest(s.entry_raw),
            query_sha256=s.config["query"]["sha256"], native_exit_code=code,
            installation_manifest_sha256=s.bound["installation_manifest_sha256"])
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:2000])
        if isinstance(error, UnknownVocabulary): report["missing_references"] = error.names
    report["worker_cpu_seconds_before_report"] = time.process_time()-CPU_START
    if s is not None:
        try: save_bytes(s.output/"WORKER.json", canonical(report))
        except BaseException as error: report.update(ok=False, report_error=type(error).__name__)
    print(canonical(report).decode("ascii"), flush=True)
    return 0 if report["ok"] else 1


def parent(args):
    s, created, supervision = None, False, None
    result = {"schema": "DMKN_ORDINARY_BASIS_QUERY_RESULT_V1", "ok": False,
              "status": "NO_WORKER_LAUNCHED", "mathematical_acceptance": False,
              "claim": "FIXED_BASIS_SEARCH_HINTS_NOT_ACCEPTANCE_OR_COVERAGE"}
    try:
        s = setup(args); R = s.R
        supervisor, job = R.load_supervision(s.bound)
        original_environment = supervisor.child_environment
        def environment(cwd):
            value = original_environment(cwd)
            value["PATH"] = os.pathsep.join(map(str, (s.python, s.python/"DLLs", s.lean/"bin")))
            return value
        argv = [str(s.python/"python.exe"), "-I", "-S", "-B", str(s.entry), "--worker",
            "--config", str(s.config_path), "--config-sha256", args.config_sha256,
            "--output", str(s.output), "--approve-local-query", "--origin", repr(s.origin),
            "--deadline", repr(s.deadline-5), "--entry-sha256", digest(s.entry_raw)]
        need(len(subprocess.list2cmdline(argv).encode("utf-16-le"))//2 < 32760, "COMMAND_LINE_BOUND")
        child_limits = dict(s.limits); child_limits["wall_seconds"] -= 5
        s.check(); s.output.mkdir(); created = True
        save_bytes(s.output/"LAUNCH.json", canonical({"argv": argv, "limits": child_limits,
            "original_limits": s.limits, "config_sha256": args.config_sha256,
            "query_sha256": s.config["query"]["sha256"], "entry_sha256": digest(s.entry_raw)}))
        result["status"] = "WORKER_OUTCOME_PENDING"
        supervisor.child_environment = environment
        try:
            supervision = supervisor.supervise(argv, s.output, s.output/"child", child_limits, job, started=s.origin)
        finally: supervisor.child_environment = original_environment
        save_bytes(s.output/"SUPERVISION.json", canonical(supervision))
        need(clean_supervision(supervision, child_limits), "WORKER_NOT_CLEANLY_COMPLETE")
        s.check()
        worker_raw = R.read(s.output/"WORKER.json", MIB, s.check)
        report = strict_json(worker_raw, reports=True)
        need(type(report) is dict and report.get("schema") == "DMKN_ORDINARY_BASIS_QUERY_WORKER_V1" and
             report.get("ok") is True and report.get("status") == "CANDIDATE_HINTS_NOT_SUPERVISED_SUCCESS" and
             report.get("supervised_completion") is False and report.get("mathematical_acceptance") is False and
             type(report.get("native_exit_code")) is int and report["native_exit_code"] == 0 and
             report.get("config_sha256") == args.config_sha256 and
             report.get("profile_sha256") == s.config["profile_sha256"] and
             report.get("entry_sha256") == digest(s.entry_raw) and
             report.get("query_sha256") == s.config["query"]["sha256"] and
             report.get("installation_manifest_sha256") == s.bound["installation_manifest_sha256"], "WORKER_BINDING")
        need(candidate_pins(s) == report["files"], "CANDIDATE_CHANGED")
        recheck_inputs(s)
        R.bind_support(s.package, s.config["profile_sha256"], s.python, s.check)
        s.check()
        result.update(ok=True, status="BASIS_QUERY_READY", config_sha256=args.config_sha256,
            query_sha256=s.config["query"]["sha256"], profile_sha256=s.config["profile_sha256"],
            interpretation=report["interpretation"], files=report["files"],
            namespace=report["namespace"], features=report["features"],
            worker_report_sha256=digest(worker_raw), specs_file=str(s.output/"SPECS.json"),
            next="Use SPECS.json with separately selected existing peer find contacts and budgets")
    except BaseException as error:
        result.update(ok=False, status="QUERY_NOT_READY", error_type=type(error).__name__,
            error=str(error)[:2000], retention="PARTIAL_OUTPUT_PRESERVED_NO_RETRY")
    result["wrapper_cpu_seconds_before_final_report"] = time.process_time()-CPU_START
    result["wall_seconds_before_final_report"] = time.monotonic()-START
    result["known_worker_job_cpu_seconds"] = (supervision.get("final_job") or {}).get("cpu_seconds") if supervision else None
    result["cost_scope"] = "WORKER_AND_LEAN_INCLUSIVE_JOB;TRUSTED_WRAPPER_CPU_SEPARATE;NO_DOUBLE_COUNT"
    if created:
        try:
            # A partial/fsync/readback failure must never leave a success marker.
            pending = s.output/"RESULT.pending.json"
            save_bytes(pending, canonical(result))
            if result["ok"]: s.check()
            # Windows rename refuses an existing target; never replace a result.
            pending.rename(s.output/"RESULT.json")
        except BaseException as error: result.update(ok=False, status="RESULT_WRITE_FAILED", report_error=type(error).__name__)
    print(canonical(result).decode("ascii"), flush=True)
    return 0 if result["ok"] else 1


def arguments():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("config", "config-sha256", "output"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--approve-local-query", action="store_true")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--origin", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--deadline", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--entry-sha256", help=argparse.SUPPRESS)
    return parser.parse_args()


if __name__ == "__main__":
    selected = arguments()
    raise SystemExit(worker(selected) if selected.worker else parent(selected))

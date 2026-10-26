"""Bounded questions over one registered owner-local module chain.

Approved local Lean syntax executes at account permissions, not in a sandbox.
Owner opening can reconcile reservations. No export, admission, fetch or network.
Only the parent RESULT after clean closure authorizes using candidate hints.
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
SCHEMA = "DMKN_ORDINARY_ANCHOR_QUERY_V1"
RUN_SHA = "47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39"
LIMITS = {"wall_seconds": 600, "cpu_seconds": 600, "memory_mib": 4096,
          "active_processes": 4, "stdout_bytes": MIB, "stderr_bytes": MIB}
OUTPUTS = {"native/Query.lean", "native/type.json", "BINDINGS.json", "QUERY.json", "SPECS.json", "ANCHOR.json"}


def need(ok, code):
    if not ok:
        raise ValueError("ANCHOR_QUERY_" + code)


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
        raise ValueError("ANCHOR_QUERY_JSON_NUMBER")
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


def source_text(universes, type_text, native_output_path, module_name):
    universes, term = validate_query({"universes": list(universes), "type": type_text})
    path = str(native_output_path)
    need(0 < len(path) <= 32768 and all(ord(c) >= 32 for c in path), "LEAN_PATH_STRING")
    quoted = json.dumps(path.replace("\\", "/"), ensure_ascii=False)
    names = ["«" + name + "»" for name in universes]
    need(type(module_name) is str and re.fullmatch(r"DMKNBridge_[0-9a-f]{64}", module_name), "MODULE_NAME")
    header = ("module\n\npublic import Init\npublic import " + module_name +
              "\npublic meta import OwnerQueryCommand\n\npublic section\n")
    if names:
        header += "universe " + " ".join(names) + "\n"
    return (header + "\n#ordinary_type_query [" + ", ".join(names) + "] " + quoted +
            " : (\n" + term + "\n)\n").encode("utf-8")


def validate_config(doc):
    need(type(doc) is dict and set(doc) == {"schema", "package", "profile_sha256",
         "python_runtime", "lean_runtime", "query", "owner", "limits"} and doc["schema"] == SCHEMA,
         "CONFIG_FIELDS")
    for key in ("package", "python_runtime", "lean_runtime"):
        need(type(doc[key]) is str and 0 < len(doc[key]) <= 32767, "CONFIG_PATH")
    hexid(doc["profile_sha256"])
    query = doc["query"]
    need(type(query) is dict and set(query) == {"path", "sha256"} and
         type(query["path"]) is str and 0 < len(query["path"]) <= 32767, "QUERY_SELECTION")
    hexid(query["sha256"])
    owner = doc["owner"]
    need(type(owner) is dict and set(owner) == {"catalog", "custody", "store_id",
         "context_root", "anchor_id", "custody_limits"}, "OWNER_FIELDS")
    for key in ("catalog", "custody"):
        need(type(owner[key]) is str and 0 < len(owner[key]) <= 32767, "OWNER_PATH")
    for key in ("store_id", "context_root", "anchor_id"):
        hexid(owner[key])
    custody_limits = owner["custody_limits"]
    need(type(custody_limits) is dict and set(custody_limits) == {"path", "sha256"} and
         type(custody_limits["path"]) is str and 0 < len(custody_limits["path"]) <= 32767,
         "CUSTODY_LIMITS_SELECTION")
    hexid(custody_limits["sha256"])
    limits = doc["limits"]
    need(type(limits) is dict and set(limits) == set(LIMITS) and
         all(type(v) is int and 1 <= v <= LIMITS[k] for k, v in limits.items()) and
         limits["wall_seconds"] >= 35 and limits["cpu_seconds"] >= 4 and
         limits["active_processes"] >= 2, "LIMITS")
    return strict_json(canonical(doc))


class UnknownVocabulary(ValueError):
    def __init__(self, names):
        self.names = names
        super().__init__("ANCHOR_QUERY_UNKNOWN_VOCABULARY")


def realized_bindings(Q, S, native_raw, inventory_raw, semantic_id,
                      plan_raw, context_bindings, check):
    """Pure projection of a Store.load-validated plan, not anchor authority itself."""
    need(type(inventory_raw) is bytes and digest(inventory_raw) == S.INVENTORY, "INVENTORY_PIN")
    need(semantic_id == S.semantic_id() and Q.S is S, "SEMANTIC_PROFILE")
    inventory = strict_json(inventory_raw)
    need(type(inventory) is list and len(inventory) == 581, "INVENTORY_CENSUS")
    keys = set()
    for row in inventory:
        check(); need(type(row) is list and len(row) >= 1, "INVENTORY_ROW")
        key = Q.E.name_key(row[0]); need(key not in keys, "INVENTORY_DUPLICATE")
        keys.add(key)
    plan = Q.E.strict_json(plan_raw, Q.E.Limits(max_bytes=4*MIB))
    need(type(plan) is dict and set(plan) == {"schema", "anchor_id", "support_id", "modules", "bindings"}
         and plan["schema"] == "DMKN_LOCAL_MODULE_ANCHOR_PLAN_V1", "PLAN_FIELDS")
    hexid(plan["anchor_id"]); hexid(plan["support_id"])
    need(type(context_bindings) is dict and type(plan["bindings"]) is list and
         1 <= len(plan["bindings"]) <= 1024, "PLAN_BINDINGS")
    realized = {}
    for unit in plan["bindings"]:
        check()
        need(type(unit) is dict and set(unit) == {"unit_id", "outputs", "realization"} and
             type(unit["outputs"]) is list and 1 <= len(unit["outputs"]) <= 4096, "PLAN_UNIT")
        identity = hexid(unit["unit_id"])
        for row in unit["outputs"]:
            check()
            need(type(row) is dict and set(row) ==
                 {"name", "export_id", "kind", "level_params", "inventory_sha256"}, "PLAN_OUTPUT")
            key = Q.E.name_key(row["name"])
            symbol = S.export_id(semantic_id, identity, row["name"])
            need(key not in keys and key not in realized and len(realized) < 16384 and
                 row["export_id"] == symbol and context_bindings.get(key) == symbol,
                 "REALIZED_EXPORT_BINDING")
            realized[key] = symbol
    names = Q.reference_names(native_raw)
    missing = [name for name in names if Q.E.name_key(name) not in keys and Q.E.name_key(name) not in realized]
    if missing:
        raise UnknownVocabulary(missing)
    rows = []
    for name in names:
        check(); key = Q.E.name_key(name)
        symbol = S.basis_symbol_id(semantic_id, S.foundation_id(), name) if key in keys else realized[key]
        need(context_bindings.get(key) == symbol, "REFERENCE_CONTEXT_BINDING")
        rows.append([name, symbol])
    return Q.E.canonical_json(rows)


def make_hints(Q, S, native_raw, inventory_raw, semantic_id, plan_raw, context_bindings, check):
    bindings = realized_bindings(Q, S, native_raw, inventory_raw, semantic_id,
                                plan_raw, context_bindings, check)
    query = Q.bind_native_type(native_raw, bindings, semantic_id=semantic_id)
    specs = Q.E.canonical_json([Q.query_spec(query)])
    check()
    return {"bindings_raw": bindings, "query_raw": query, "specs_raw": specs,
            "interpretation": {"semantic_id": semantic_id, "foundation_id": S.foundation_id(),
                "inventory_sha256": S.INVENTORY, "vocabulary": "FIXED_BASIS_AND_REGISTERED_CHAIN",
                "key_profile": Q.PROFILE_ID}}


def checked_context(owner, installation, context_root, foundation_id):
    context = owner.catalog.context(context_root)
    need(context["local_root"] == context_root and context["semantic_id"] == installation.semantic_id and
         context["foundation_id"] == foundation_id and
         context["implementation_id"] == installation.implementation_id, "CONTEXT_IDENTITY")
    return context


def registered_view(loaded, owner, catalog_path, context, anchor_id, check):
    M = loaded.module_export; K = M.K
    need(K.A is loaded.A and M.A is loaded.A, "ANCHOR_SHARED_HELPERS")
    # open_for_owner otherwise creates a missing sidecar; queries must refuse it.
    loaded.A.C.ordinary(catalog_path/"module-anchors-v1", directory=True)
    support = M.support_descriptor(loaded.installation, loaded.profile,
                                  loaded.root/"module/OrdinaryModule.lean", loaded.root/"module_worker.py")
    store = K.open_for_owner(owner, support, check)
    return store, store.load(anchor_id, context, check)


def unchanged_view(store, anchor_id, context, view, check):
    need(store.load(anchor_id, context, check) == view, "ANCHOR_CHANGED")


def close_handles(owner, custody):
    errors = []
    for label, value in (("owner", owner), ("custody", custody)):
        if value is not None:
            try:
                value.close()
            except BaseException as error:
                errors.append({"component": label, "error_type": type(error).__name__, "error": str(error)[:500]})
    return errors


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
    R = load_source("_anchor_query_launch_support", launcher, run_raw)
    package = R.ordinary(package, directory=True)
    python = R.ordinary(config["python_runtime"], directory=True)
    lean = R.ordinary(config["lean_runtime"], directory=True)
    output = R.ordinary(args.output, directory=True, fresh=not args.worker)
    config_path = R.ordinary(args.config); query_path = R.ordinary(config["query"]["path"])
    query_raw = R.read(query_path, MIB, check)
    need(digest(query_raw) == config["query"]["sha256"], "QUERY_PIN")
    universes, term = validate_query(strict_json(query_raw))
    owner_selection = config["owner"]
    catalog = R.ordinary(owner_selection["catalog"], directory=True)
    custody = R.ordinary(owner_selection["custody"], directory=True)
    need(all(os.pathsep not in str(path) for path in (package, python, lean, catalog)), "SEARCH_PATH_SEPARATOR")
    custody_limits_path = R.ordinary(owner_selection["custody_limits"]["path"])
    custody_limits_raw = R.read(custody_limits_path, 65536, check)
    need(digest(custody_limits_raw) == owner_selection["custody_limits"]["sha256"], "CUSTODY_LIMITS_PIN")
    R.separated([output, catalog, custody, package, python, lean, entry.parent], "ANCHOR_QUERY_PATH_OVERLAP")
    need(all(not R.overlap(output, p) for p in
             (config_path, query_path, custody_limits_path)), "OUTPUT_INPUT_OVERLAP")
    need(all(not R.overlap(state, p) for state in (catalog, custody)
             for p in (entry, config_path, query_path, custody_limits_path)), "STATE_INPUT_OVERLAP")
    bound = R.bind_support(package, config["profile_sha256"], python, check)
    check()
    return SimpleNamespace(R=R, config=config, config_raw=config_raw, config_path=config_path,
        query_raw=query_raw, query_path=query_path, package=package, python=python, lean=lean,
        catalog=catalog, custody=custody, custody_limits_path=custody_limits_path,
        custody_limits_raw=custody_limits_raw,
        entry=entry, entry_raw=entry_raw, limits=limits, output=output, bound=bound,
        origin=origin, deadline=deadline, check=check, universes=universes, term=term)


def save_bytes(path, raw, maximum=MIB):
    need(type(raw) is bytes and 0 < len(raw) <= maximum, "OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    need(initial_read(path, maximum) == raw, "OUTPUT_READBACK")


def recheck_inputs(s):
    for path, raw in ((s.config_path, s.config_raw), (s.query_path, s.query_raw), (s.entry, s.entry_raw),
                      (s.custody_limits_path, s.custody_limits_raw)):
        need(s.R.read(path, 2*MIB, s.check) == raw, "INPUT_CHANGED")


def candidate_pins(s):
    with os.scandir(s.R.ordinary(s.output/"native", directory=True)) as rows:
        actual = set()
        for row in rows:
            s.check(); actual.add("native/" + row.name); need(len(actual) <= 2, "NATIVE_CENSUS_BOUND")
    need(actual == {"native/Query.lean", "native/type.json"}, "NATIVE_CENSUS")
    result, total = {}, 0
    for name in sorted(OUTPUTS):
        maximum = 8*MIB if name == "ANCHOR.json" else MIB
        raw = s.R.read(s.output/name, maximum, s.check); total += len(raw)
        need(total <= 13*MIB, "OUTPUT_TOTAL")
        result[name] = {"bytes": len(raw), "sha256": digest(raw)}
    return result


def completed_output_census(s, supervision):
    expected = {"native", "child", "LAUNCH.json", "SUPERVISION.json", "WORKER.json"}
    expected.update(name for name in OUTPUTS if not name.startswith("native/"))
    actual = set()
    for path in s.output.iterdir():
        s.check(); need(len(actual) < len(expected), "OUTPUT_CENSUS_BOUND")
        s.R.ordinary(path, directory=path.name in {"native", "child"})
        actual.add(path.name)
    need(actual == expected, "OUTPUT_CENSUS")
    child = s.output/"child"
    child_names = set()
    for path in child.iterdir():
        s.check(); need(len(child_names) < 3, "CHILD_CENSUS_BOUND")
        child_names.add(path.name)
    need(child_names == {"command.json", "stdout.txt", "stderr.txt"}, "CHILD_CENSUS")
    for label in ("stdout", "stderr"):
        size = s.R.ordinary(child/(label + ".txt")).stat().st_size
        need(size == supervision["observed_logs"][label + "_bytes"], "CHILD_LOG_CHANGED")
    s.R.ordinary(child/"command.json")


def worker(args):
    s = owner = custody = candidate = None
    report = {"schema": "DMKN_ORDINARY_ANCHOR_QUERY_WORKER_V1", "ok": False,
              "mathematical_acceptance": False, "supervised_completion": False}
    phase = "SETUP"
    try:
        s = setup(args); R = s.R; s.check()
        profile = R.strict(R.read(s.package/"PROFILE.json", 2*MIB, s.check))
        owner_raw = R.bound_file(s.package/"owner.py", profile["files"]["owner.py"], s.check, source=True)
        entry = R.load_source("_anchor_query_owner", s.package/"owner.py", owner_raw)
        loader = entry.bootstrap(s.package, s.config["profile_sha256"], s.check)
        loaded = loader.load(s.package, s.config["profile_sha256"],
            {"python_runtime": s.python, "lean_runtime": s.lean}, s.deadline, check_parent=s.check)
        A, O, Q, installation = loaded.A, loaded.O, loaded.formal_query, loaded.installation
        S = A.S; selected = s.config["owner"]
        need(Q.S is S and Q.E is A.E, "LOADED_SHARED_SEMANTICS")
        phase = "OWNER_INPUTS"
        custody_limits = A._writer_json(s.custody_limits_raw, 65536)
        A.P.fields(custody_limits, O.STORE_LIMITS, "ANCHOR_QUERY_CUSTODY_LIMITS")
        for key, bounds in O.STORE_LIMITS.items():
            A.P.uint(custody_limits[key], *bounds, "ANCHOR_QUERY_CUSTODY_LIMIT:" + key)
        marker = A.E.strict_json(A.C.read_bounded(s.catalog/"ADOPTION.json", 65536),
                                 A.E.Limits(max_bytes=65536))
        A.P.fields(marker, ("schema", "store_id", "implementation", "limits"), "ANCHOR_QUERY_ADOPTION_FIELDS")
        need(marker["schema"] == A.P.SCHEMA and marker["store_id"] == selected["store_id"] and
             marker["implementation"] == installation.doc["implementation"], "ADOPTION_BINDING")
        limits = A.P.Limits(**marker["limits"])
        phase = "OPEN_OWNER"; s.check()
        custody = O.OrdinaryStore(s.custody, installation.semantic_id, custody_limits, create=False)
        owner = A.OrdinaryAdmission.open(installation, s.catalog, selected["store_id"],
                                        custody, create=False, limits=limits)
        s.check(); phase = "REGISTERED_ANCHOR"
        context = checked_context(owner, installation, selected["context_root"], S.foundation_id())
        store, view = registered_view(loaded, owner, s.catalog, context, selected["anchor_id"], s.check)
        plan = loaded.module_export.K.parse(view.plan_raw, 4*MIB)
        phase = "NATIVE_QUERY"
        native = s.output/"native"; R.ordinary(native, directory=True, fresh=True).mkdir()
        raw_source = source_text(s.universes, s.term, native/"type.json", view.module_name)
        save_bytes(native/"Query.lean", raw_source)
        paths = (*loaded.profile.helper_paths, s.lean/"lib/lean", *view.import_directories)
        need(len(paths) <= 41 and len(set(paths)) == len(paths) and
             all(os.pathsep not in str(path) for path in paths), "IMPORT_DIRECTORIES")
        for path in paths:
            R.ordinary(path, directory=True)
        # Match OrdinaryModule.nativePath's ordinary-drive extended spelling.
        # Stable plan/report paths remain ordinary; only Lean's filesystem spelling changes.
        lean_paths = ["\\\\?\\" + str(path) for path in paths]
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith(
               ("LEAN", "PYTHON", "RUST", "CARGO", "RISC0", "NODE")) and k.upper() not in {"PATH", "VIRTUAL_ENV"}}
        env["PATH"] = os.pathsep.join(map(str, (s.python, s.python/"DLLs", s.lean/"bin")))
        env["LEAN_PATH"] = os.pathsep.join(lean_paths)
        need(len(env["LEAN_PATH"]) < 30000, "IMPORT_PATH_BOUND")
        argv = [str(installation.path("lean")), "-j", "1", "-DElab.async=false",
                "-R", str(native), str(native/"Query.lean")]
        s.check()
        # The native child inherits the parent's one whole-tree Job and log caps.
        code = subprocess.call(argv, cwd=native, env=env, stdin=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        s.check(); need(code == 0, "NATIVE_EXTRACTION_FAILED")
        native_raw = R.read(native/"type.json", MIB, s.check)
        hints = make_hints(Q, S, native_raw, installation.read("inventory", MIB),
                          installation.semantic_id, view.plan_raw, context["bindings"], s.check)
        adapter = sys.modules["discovery.ordinary_export_adapter"]
        need(adapter.Q is Q, "LOADED_DISCOVERY_QUERY")
        namespace = adapter.namespace_for(installation.semantic_id)
        features = adapter.compile_query(namespace, Q.E.strict_json(hints["specs_raw"]))
        phase = "FINAL_VALIDATION"
        loaded.profile.verify(s.check); recheck_inputs(s)
        # Fetch/authenticate the selected context again while the same owner lock is live.
        current = checked_context(owner, installation, selected["context_root"], S.foundation_id())
        unchanged_view(store, selected["anchor_id"], current, view, s.check)
        need(realized_bindings(Q, S, native_raw, installation.read("inventory", MIB),
             installation.semantic_id, view.plan_raw, current["bindings"], s.check) == hints["bindings_raw"],
             "FINAL_BINDINGS_CHANGED")
        need(R.read(native/"Query.lean", MIB, s.check) == raw_source and
             R.read(native/"type.json", MIB, s.check) == native_raw, "GENERATED_INPUT_CHANGED")
        interpretation = {**hints["interpretation"], "implementation_id": installation.implementation_id,
            "store_id": selected["store_id"], "context_root": selected["context_root"],
            "anchor_id": view.anchor_id, "support_id": view.support_id,
            "plan_sha256": digest(view.plan_raw), "module_name": view.module_name,
            "reference_count": len(Q.reference_names(native_raw))}
        anchor = {"schema": "DMKN_ORDINARY_ANCHOR_QUERY_SELECTION_V1", **interpretation,
            "store_binding": view.store_binding, "record_sha256": [digest(raw) for raw in view.records],
            "artifact_bytes": view.artifact_bytes, "import_directories": list(map(str, view.import_directories)),
            "lean_path": lean_paths, "modules": plan["modules"]}
        candidate = {"hints": hints, "anchor": canonical(anchor), "source_raw": raw_source,
            "native_raw": native_raw, "interpretation": interpretation, "namespace": namespace,
            "features": features, "native_exit_code": code}
    except BaseException as error:
        report.update(phase=phase, error_type=type(error).__name__, error=str(error)[:2000])
        if isinstance(error, UnknownVocabulary):
            report["missing_references"] = error.names
    finally:
        errors = close_handles(owner, custody)
        report["owner_handles_closed"] = owner is not None and custody is not None and not errors
        if errors:
            candidate = None
            report.update(status="FAILED_OWNER_CLOSURE", close_errors=errors)

    # No candidate output/report success is written before both state handles close.
    try:
        if candidate is not None:
            s.check(); recheck_inputs(s)
            need(s.R.read(s.output/"native/Query.lean", MIB, s.check) == candidate["source_raw"] and
                 s.R.read(s.output/"native/type.json", MIB, s.check) == candidate["native_raw"],
                 "CLOSED_INPUT_CHANGED")
            for name, key in (("BINDINGS.json", "bindings_raw"), ("QUERY.json", "query_raw"), ("SPECS.json", "specs_raw")):
                s.check(); save_bytes(s.output/name, candidate["hints"][key])
            save_bytes(s.output/"ANCHOR.json", candidate["anchor"], 8*MIB)
            pins = candidate_pins(s); s.check()
            report.update(ok=True, status="CANDIDATE_HINTS_NOT_SUPERVISED_SUCCESS", files=pins,
                interpretation=candidate["interpretation"], config_sha256=args.config_sha256,
                namespace=candidate["namespace"], features=candidate["features"],
                profile_sha256=s.config["profile_sha256"], entry_sha256=digest(s.entry_raw),
                query_sha256=s.config["query"]["sha256"], native_exit_code=candidate["native_exit_code"],
                installation_manifest_sha256=s.bound["installation_manifest_sha256"])
    except BaseException as error:
        report.update(ok=False, phase="CLOSED_PUBLICATION", error_type=type(error).__name__, error=str(error)[:2000])
    report["worker_cpu_seconds_before_report"] = time.process_time()-CPU_START
    if s is not None:
        try:
            save_bytes(s.output/"WORKER.json", canonical(report))
        except BaseException as error:
            report.update(ok=False, report_error=type(error).__name__)
    print(canonical(report).decode("ascii"), flush=True)
    return 0 if report["ok"] else 1


def parent(args):
    s, created, supervision = None, False, None
    result = {"schema": "DMKN_ORDINARY_ANCHOR_QUERY_RESULT_V1", "ok": False,
              "status": "NO_WORKER_LAUNCHED", "mathematical_acceptance": False,
              "claim": "REGISTERED_VOCABULARY_SEARCH_HINTS_NOT_ACCEPTANCE_OR_COVERAGE"}
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
        need(type(report) is dict and report.get("schema") == "DMKN_ORDINARY_ANCHOR_QUERY_WORKER_V1" and
             report.get("ok") is True and report.get("status") == "CANDIDATE_HINTS_NOT_SUPERVISED_SUCCESS" and
             report.get("supervised_completion") is False and report.get("mathematical_acceptance") is False and
             report.get("owner_handles_closed") is True and "close_errors" not in report and
             type(report.get("native_exit_code")) is int and report["native_exit_code"] == 0 and
             report.get("config_sha256") == args.config_sha256 and
             report.get("profile_sha256") == s.config["profile_sha256"] and
             report.get("entry_sha256") == digest(s.entry_raw) and
             report.get("query_sha256") == s.config["query"]["sha256"] and
             report.get("installation_manifest_sha256") == s.bound["installation_manifest_sha256"], "WORKER_BINDING")
        interpretation = report.get("interpretation")
        need(type(interpretation) is dict and interpretation.get("vocabulary") == "FIXED_BASIS_AND_REGISTERED_CHAIN"
             and all(interpretation.get(key) == s.config["owner"][key]
                     for key in ("store_id", "context_root", "anchor_id")), "WORKER_OWNER_SELECTION")
        for key in ("semantic_id", "foundation_id", "implementation_id", "inventory_sha256",
                    "key_profile", "support_id", "plan_sha256"):
            hexid(interpretation[key])
        need(candidate_pins(s) == report["files"], "CANDIDATE_CHANGED")
        completed_output_census(s, supervision)
        recheck_inputs(s)
        R.bind_support(s.package, s.config["profile_sha256"], s.python, s.check)
        s.check()
        result.update(ok=True, status="ANCHOR_QUERY_READY", config_sha256=args.config_sha256,
            query_sha256=s.config["query"]["sha256"], profile_sha256=s.config["profile_sha256"],
            entry_sha256=digest(s.entry_raw), custody_limits_sha256=digest(s.custody_limits_raw),
            interpretation=report["interpretation"], files=report["files"],
            owner_handles_closed=True, installation_manifest_sha256=s.bound["installation_manifest_sha256"],
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

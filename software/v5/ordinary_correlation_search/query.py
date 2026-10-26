"""Compile inert local type metadata into the existing peer search spec.

Manual mode supplies known symbol bindings and opens no owner state. Context
mode resolves those bindings through one explicitly selected existing owner
context, using its real lock/lifecycle. Reopening can settle old reservations.
Neither mode runs Lean, fetches evidence, accepts mathematics or queries peers.
The meaning is the selected receiver interpretation, not project equivalence.
Optional conclusion correlation is only an inert candidate filter. The explicit
context-binder count differs from the owner context used to resolve symbols.
Process limits are cooperative; use an outer supervisor for hard containment.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys

MIB = 1024**2


def need(condition, code):
    if not condition:
        raise ValueError(code)


def bootstrap_owner(root, expected, check):
    """Check this entry and old owner bytes before importing reusable helpers.

    Entrypoint/Python/OS integrity and immutable local owner storage remain
    premises. The externally selected hash is byte selection, not authentication.
    The unchanged owner bootstrap next checks the new exact profile loader.
    """
    need(type(expected) is str and len(expected) == 64 and
         all(c in "0123456789abcdef" for c in expected), "QUERY_PROFILE_HASH")
    def read(path, maximum):
        need(path.is_absolute() and ".." not in path.parts, "QUERY_BOOTSTRAP_PATH")
        for part in (*reversed(path.parents), path):
            info = part.lstat()
            need(not stat.S_ISLNK(info.st_mode) and not
                 (getattr(info, "st_file_attributes", 0) & 0x400), "QUERY_BOOTSTRAP_REDIRECT")
            need(stat.S_ISDIR(info.st_mode) if part != path else
                 stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "QUERY_BOOTSTRAP_FILE")
        size = path.stat().st_size
        need(0 < size <= maximum, "QUERY_BOOTSTRAP_BOUND")
        check()
        with path.open("rb") as stream:
            raw = stream.read(maximum+1)
        need(len(raw) == size, "QUERY_BOOTSTRAP_CHANGED")
        return raw
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "QUERY_BOOTSTRAP_DUPLICATE")
            result[key] = value
        return result
    raw = read(root/"PROFILE.json", 2*MIB)
    need(hashlib.sha256(raw).hexdigest() == expected, "QUERY_PROFILE_PIN")
    doc = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    need(type(doc) is dict and type(doc.get("files")) is dict, "QUERY_BOOTSTRAP_DESCRIPTOR")
    selected = {}
    for filename in ("query.py", "owner.py"):
        pin = doc["files"].get(filename)
        need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
             type(pin["bytes"]) is int and 0 < pin["bytes"] <= 2*MIB, "QUERY_BOOTSTRAP_PIN")
        selected[filename] = read(root/filename, 2*MIB)
        need(len(selected[filename]) == pin["bytes"] and
             hashlib.sha256(selected[filename]).hexdigest() == pin["sha256"],
             "QUERY_BOOTSTRAP_SOURCE_CHANGED")
    name, path = "_dmkn_ordinary_owner_entry", root/"owner.py"
    need(name not in sys.modules, "QUERY_BOOTSTRAP_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(selected["owner.py"], str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    # Reuse the exact owner Allowance implementation, including all subsequent
    # worker CPU charges, while accounting from THIS entry's original start.
    module.START_WALL, module.START_CPU = START_WALL, START_CPU
    return module


def binding_mode(args):
    manual = getattr(args, "bindings", None) is not None
    contextual = getattr(args, "context_root", None) is not None
    need(manual != contextual, "QUERY_EXACTLY_ONE_BINDING_MODE")
    values = [getattr(args, field, None) for field in
              ("catalog", "custody", "store_id", "custody_limits")]
    need(all(value is not None for value in values) if contextual else
         all(value is None for value in values), "QUERY_CONTEXT_ARGUMENTS")
    return "context" if contextual else "manual"


def conclusion_context_binders(args):
    """None selects exact type; explicit zero selects the correlation profile."""
    count = getattr(args, "conclusion_context_binders", None)
    need(count is None or type(count) is int and 0 <= count <= 4096,
         "QUERY_CONCLUSION_CONTEXT_BINDERS")
    return count


def selected_query(args, Q, adapter, query_raw):
    """Return one ordinary spec and truthful profile labels; never acceptance."""
    count = conclusion_context_binders(args)
    if count is None:
        return Q.query_spec(query_raw), {
            "search_mode": "exact-whole-type", "search_profile": Q.PROFILE_ID,
            "conclusion_context_binders": None,
            "claim": "BOUNDED_EXACT_TYPE_SEARCH_INPUT_NOT_THEOREM_OR_GLOBAL_COVERAGE"}
    spec = adapter.correlation_query_spec(query_raw, context_binders=count)
    return spec, {
        "search_mode": "conclusion-correlation",
        "search_profile": adapter.CORRELATION_PROFILE_ID,
        "conclusion_context_binders": count,
        "claim": "BOUNDED_CONCLUSION_CORRELATION_CANDIDATE_FILTER_NOT_APPLICABILITY_OR_GLOBAL_COVERAGE"}


def arguments():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("profile-sha256", "python-runtime", "lean-runtime", "native-type", "output"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+name, required=True, type=int)
    parser.add_argument("--conclusion-context-binders", type=int,
        help="Optional fixed conclusion-correlation mode; strip exactly N leading query foralls (explicit 0 is valid)")
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--bindings", help="Existing exact canonical binding rows; no owner opening")
    modes.add_argument("--context-root", help="Exact existing owner context supplying query bindings")
    for name in ("catalog", "custody", "store-id", "custody-limits"):
        parser.add_argument("--"+name, help="Required only with --context-root")
    args = parser.parse_args()
    try:
        binding_mode(args)
        conclusion_context_binders(args)
    except ValueError as error:
        parser.error(str(error))
    return args


def run_manual(args):
    allocation, created, output, result = None, False, None, None
    phase = "BOOTSTRAP"
    try:
        conclusion_context_binders(args)
        need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
             sys.dont_write_bytecode and not sys.flags.optimize, "QUERY_PYTHON_PROFILE")
        need(type(args.wall_seconds) is int and 35 <= args.wall_seconds <= 3600 and
             type(args.cpu_seconds) is int and 4 <= args.cpu_seconds <= 600,
             "QUERY_FINITE_ALLOWANCE")
        deadline = START_WALL+args.wall_seconds
        def check():
            need(time.monotonic() < deadline and
                 time.process_time()-START_CPU < args.cpu_seconds, "QUERY_ALLOWANCE")
        root = Path(__file__).absolute().parent
        base = bootstrap_owner(root, args.profile_sha256, check)
        allocation = base.Allowance(args)
        loader = base.bootstrap(root, args.profile_sha256, allocation.check)
        loaded = loader.load(root, args.profile_sha256,
            {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
            allocation.deadline, check_parent=allocation.check)
        A, Q = loaded.A, loaded.formal_query
        adapter = sys.modules["discovery.ordinary_export_adapter"]
        need(Q.E is A.E and Q.S is A.S and adapter.Q is Q, "QUERY_SHARED_HELPERS")
        phase = "INPUTS"
        native_path, bindings_path = (A.C.ordinary(Path(value))
                                     for value in (args.native_type, args.bindings))
        native_raw = A.C.read_bounded(native_path, MIB)
        bindings_raw = A.C.read_bounded(bindings_path, MIB)
        output = A.C.ordinary(Path(args.output), directory=True, fresh=True)
        base.separated([output, root, *loaded.installation.runtime_roots.values()],
                       "QUERY_OUTPUT_SUPPORT_OVERLAP")
        need(not native_path.is_relative_to(output) and not bindings_path.is_relative_to(output),
             "QUERY_INPUT_OUTPUT_OVERLAP")
        allocation.check()
        phase = "QUERY"
        query_raw = Q.bind_native_type(native_raw, bindings_raw,
                                      semantic_id=loaded.installation.semantic_id)
        spec, search = selected_query(args, Q, adapter, query_raw)
        namespace = adapter.namespace_for(loaded.installation.semantic_id)
        features = adapter.compile_query(namespace, [spec])
        # Recheck captured inputs and selected package before any output commit.
        need(A.C.read_bounded(native_path, MIB) == native_raw and
             A.C.read_bounded(bindings_path, MIB) == bindings_raw, "QUERY_INPUT_CHANGED")
        loaded.profile.verify(allocation.check)
        allocation.check()
        output.mkdir()
        created = True
        A.P.PortableCatalog._write_fresh(output/"QUERY.json", query_raw)
        A.P.PortableCatalog._write_fresh(output/"SPECS.json", A.E.canonical_json([spec]))
        result = {"ok": True, "operation": "prepare-query", "namespace": namespace,
            "specs": [spec], "features": features, "key_profile": Q.PROFILE_ID,
            "query_sha256": hashlib.sha256(query_raw).hexdigest(),
            "native_type_sha256": hashlib.sha256(native_raw).hexdigest(),
            "bindings_sha256": hashlib.sha256(bindings_raw).hexdigest(),
            "profile_sha256": args.profile_sha256, "mathematical_acceptance": False,
            **search,
            "next": "Use specs in existing peer.py find with explicit contacts and budgets"}
        allocation.check()
    except BaseException as error:
        result = {"ok": False, "phase": phase, "error_type": type(error).__name__,
                  "error": str(error)[:2000], "mathematical_acceptance": False,
                  "retention": "PARTIAL_OUTPUT_RETAINED_NO_RETRY"}
    result["cost"] = allocation.report() if allocation is not None else {
        "wall_seconds": time.monotonic()-START_WALL,
        "controller_cpu_seconds": time.process_time()-START_CPU,
        "worker_cpu_seconds": 0, "controller_limits": "COOPERATIVE_REQUIRES_EXTERNAL_JOB"}
    raw = json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False,
                     separators=(",", ":")).encode("utf-8")
    if created:
        try:
            A.P.PortableCatalog._write_fresh(output/"RESULT.json", raw)
        except BaseException as error:
            result.update(ok=False, report_write_error=str(error)[:500])
            raw = json.dumps(result, sort_keys=True, allow_nan=False).encode("utf-8")
    return result, raw


def resolve_context_bindings(Q, native_raw, context_bindings, check):
    """Pure reference projection, not a source of owner or theorem authority."""
    need(type(context_bindings) is dict and callable(check), "QUERY_CONTEXT_BINDING_MAP")
    names = Q.reference_names(native_raw)
    rows, missing = [], []
    for name in names:
        check()
        key = Q.E.name_key(name, Q.DEFAULT_LIMITS.codec)
        if key not in context_bindings:
            missing.append(name)
        else:
            rows.append([name, Q.E._hex(context_bindings[key])])
    check()
    if missing:
        need(len(Q.E.canonical_json(missing)) <= MIB, "QUERY_CONTEXT_MISSING_BYTES")
        return None, missing
    raw = Q.E.canonical_json(rows)
    need(len(raw) <= MIB, "QUERY_CONTEXT_BINDINGS_BYTES")
    return raw, []


def run_context(args):
    allocation = owner = custody = output = None
    context_selection, result = None, None
    created = publication_attempted = published = False
    result_sha256 = None
    phase = "BOOTSTRAP"
    try:
        need(binding_mode(args) == "context", "QUERY_CONTEXT_MODE")
        conclusion_context_binders(args)
        need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
             sys.dont_write_bytecode and not sys.flags.optimize, "QUERY_PYTHON_PROFILE")
        need(type(args.wall_seconds) is int and 35 <= args.wall_seconds <= 3600 and
             type(args.cpu_seconds) is int and 4 <= args.cpu_seconds <= 600,
             "QUERY_FINITE_ALLOWANCE")
        deadline = START_WALL+args.wall_seconds
        def check():
            need(time.monotonic() < deadline and
                 time.process_time()-START_CPU < args.cpu_seconds, "QUERY_ALLOWANCE")
        root = Path(__file__).absolute().parent
        base = bootstrap_owner(root, args.profile_sha256, check)
        allocation = base.Allowance(args)
        loader = base.bootstrap(root, args.profile_sha256, allocation.check)
        loaded = loader.load(root, args.profile_sha256,
            {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
            allocation.deadline, check_parent=allocation.check)
        A, O, Q, installation = loaded.A, loaded.O, loaded.formal_query, loaded.installation
        adapter = sys.modules["discovery.ordinary_export_adapter"]
        need(Q.E is A.E and Q.S is A.S and adapter.Q is Q, "QUERY_SHARED_HELPERS")
        phase = "INPUTS"
        A.C.hexid(args.context_root); A.C.hexid(args.store_id)
        native_path = A.C.ordinary(Path(args.native_type))
        limits_path = A.C.ordinary(Path(args.custody_limits))
        native_raw = A.C.read_bounded(native_path, MIB)
        Q.read_native_type(native_raw)  # Reject malformed syntax before owner recovery/opening.
        limits_raw = A.C.read_bounded(limits_path, 65536)
        custody_limits = A._writer_json(limits_raw, 65536)
        A.P.fields(custody_limits, O.STORE_LIMITS, "QUERY_CUSTODY_LIMITS")
        for key, bounds in O.STORE_LIMITS.items():
            A.P.uint(custody_limits[key], *bounds, "QUERY_CUSTODY_LIMIT:"+key)
        catalog_path = A.C.ordinary(Path(args.catalog), directory=True)
        custody_path = A.C.ordinary(Path(args.custody), directory=True)
        output = A.C.ordinary(Path(args.output), directory=True, fresh=True)
        base.separated([output, catalog_path, custody_path, root,
                        *installation.runtime_roots.values()], "QUERY_CONTEXT_PATH_OVERLAP")
        for path in (native_path, limits_path):
            need(all(not path.is_relative_to(directory)
                     for directory in (output, catalog_path, custody_path)), "QUERY_CONTEXT_INPUT_OVERLAP")
        marker = A.E.strict_json(A.C.read_bounded(catalog_path/"ADOPTION.json", 65536),
                                A.E.Limits(max_bytes=65536))
        A.P.fields(marker, ("schema", "store_id", "implementation", "limits"), "QUERY_ADOPTION_FIELDS")
        need(marker["schema"] == A.P.SCHEMA and marker["store_id"] == args.store_id and
             marker["implementation"] == installation.doc["implementation"], "QUERY_ADOPTION_BINDING")
        limits = A.P.Limits(**marker["limits"])
        allocation.check()
        phase = "OPEN_OWNER"
        custody = O.OrdinaryStore(custody_path, installation.semantic_id, custody_limits, create=False)
        owner = A.OrdinaryAdmission.open(installation, catalog_path, args.store_id,
                                       custody, create=False, limits=limits)
        allocation.check()
        phase = "RESOLVE_CONTEXT"
        context = owner.catalog.context(args.context_root)
        need(context["local_root"] == args.context_root and
             context["semantic_id"] == installation.semantic_id and
             context["foundation_id"] == A.S.foundation_id() and
             context["implementation_id"] == installation.implementation_id, "QUERY_CONTEXT_IDENTITY")
        bindings_raw, missing = resolve_context_bindings(Q, native_raw, context["bindings"], allocation.check)
        context_selection = {key: context[key] for key in
                             ("semantic_id", "foundation_id", "implementation_id")}
        context_selection.update(store_id=args.store_id, context_root=args.context_root)
        if missing:
            result = {"ok": False, "operation": "prepare-query", "status": "UNMAPPED_REFERENCES",
                "phase": phase, "missing_names": missing, "mathematical_acceptance": False,
                "retention": "NO_QUERY_OUTPUT_NO_FETCH_OR_RETRY"}
        else:
            phase = "QUERY"
            query_raw = Q.bind_native_type(native_raw, bindings_raw, semantic_id=installation.semantic_id)
            spec, search = selected_query(args, Q, adapter, query_raw)
            namespace = adapter.namespace_for(installation.semantic_id)
            features = adapter.compile_query(namespace, [spec])
            context_selection["reference_count"] = len(Q.E.strict_json(bindings_raw))
            result = {"ok": True, "operation": "prepare-query", "namespace": namespace,
                "specs": [spec], "features": features, "key_profile": Q.PROFILE_ID,
                "query_sha256": hashlib.sha256(query_raw).hexdigest(),
                "native_type_sha256": hashlib.sha256(native_raw).hexdigest(),
                "bindings_sha256": hashlib.sha256(bindings_raw).hexdigest(),
                "profile_sha256": args.profile_sha256, "mathematical_acceptance": False,
                **search,
                "next": "Use specs in existing peer.py find with explicit contacts and budgets"}
        phase = "FINAL_VALIDATION"
        need(A.C.read_bounded(native_path, MIB) == native_raw and
             A.C.read_bounded(limits_path, 65536) == limits_raw, "QUERY_INPUT_CHANGED")
        loaded.profile.verify(allocation.check)
        allocation.check()
    except BaseException as error:
        result = {"ok": False, "operation": "prepare-query", "phase": phase,
            "error_type": type(error).__name__, "error": str(error)[:2000],
            "mathematical_acceptance": False, "retention": "NO_QUERY_OUTPUT_NO_RETRY"}
    finally:
        close_errors = []
        for label, value in (("owner", owner), ("custody", custody)):
            if value is not None:
                try:
                    value.close()
                except BaseException as error:
                    close_errors.append({"component": label, "error_type": type(error).__name__,
                                         "error": str(error)[:500]})
        if close_errors:
            result.update(ok=False, status="FAILED_OWNER_CLOSURE", close_errors=close_errors)
        result.update(binding_mode="selected-local-context",
            context_selection=context_selection,
            interpretation="SELECTED_RECEIVER_CONTEXT_NOT_PROJECT_EQUIVALENCE")

    # No success publication is attempted until both state handles are closed.
    try:
        if allocation is not None:
            allocation.check()
        if result["ok"]:
            phase = "OUTPUT"
            output.mkdir(); created = True
            for filename, raw in (("BINDINGS.json", bindings_raw), ("QUERY.json", query_raw),
                                   ("SPECS.json", A.E.canonical_json([spec]))):
                allocation.check()
                A.P.PortableCatalog._write_fresh(output/filename, raw)
        result["cost"] = allocation.report() if allocation is not None else {
            "wall_seconds": time.monotonic()-START_WALL,
            "controller_cpu_seconds": time.process_time()-START_CPU,
            "worker_cpu_seconds": 0, "controller_limits": "COOPERATIVE_REQUIRES_EXTERNAL_JOB"}
        raw = json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False,
                         separators=(",", ":")).encode("utf-8")
        if result["ok"]:
            # Reported costs precede this final marker write, as in manual mode;
            # an enclosing supervisor measures whole-operation finalization too.
            result_sha256 = hashlib.sha256(raw).hexdigest()
            pending, target = output/".RESULT.pending", output/"RESULT.json"
            A.P.PortableCatalog._write_fresh(pending, raw)
            A.C.ordinary(target, fresh=True)
            allocation.check()
            publication_attempted = True
            pending.rename(target)  # Windows same-volume fresh rename, no overwrite.
            published = True
        return result, raw
    except BaseException as error:
        failure = {"ok": False, "operation": "prepare-query", "phase": phase,
            "error_type": type(error).__name__, "error": str(error)[:2000],
            "binding_mode": "selected-local-context", "context_selection": context_selection,
            "interpretation": "SELECTED_RECEIVER_CONTEXT_NOT_PROJECT_EQUIVALENCE",
            "mathematical_acceptance": False, "retention": "PARTIAL_OUTPUT_RETAINED_NO_RETRY",
            "output": str(output) if created else None,
            "result_publication": "PUBLISHED" if published else "UNKNOWN" if publication_attempted else "NOT_ATTEMPTED",
            "attempted_result_sha256": result_sha256}
        if close_errors:
            failure["close_errors"] = close_errors
        failure["cost"] = allocation.report() if allocation is not None else {
            "wall_seconds": time.monotonic()-START_WALL,
            "controller_cpu_seconds": time.process_time()-START_CPU,
            "worker_cpu_seconds": 0, "controller_limits": "COOPERATIVE_REQUIRES_EXTERNAL_JOB"}
        return failure, json.dumps(failure, sort_keys=True, ensure_ascii=False, allow_nan=False,
                                   separators=(",", ":")).encode("utf-8")


def run(args):
    # This also validates programmatic callers before they can open any state.
    try:
        mode = binding_mode(args)
        conclusion_context_binders(args)
    except ValueError as error:
        result = {"ok": False, "phase": "ARGUMENTS", "error_type": "ValueError",
                  "error": str(error), "mathematical_acceptance": False}
        return result, json.dumps(result, sort_keys=True, allow_nan=False).encode("utf-8")
    return run_context(args) if mode == "context" else run_manual(args)


if __name__ == "__main__":
    result, raw = run(arguments())
    sys.stdout.buffer.write(raw+b"\n")
    sys.stdout.buffer.flush()
    raise SystemExit(0 if result["ok"] else 1)

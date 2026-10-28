"""Compile inert type or symbol-neighborhood inputs into existing search specs.

Manual mode supplies known symbol bindings and opens no owner state. Context
mode resolves those bindings through one explicitly selected existing owner
context, using its real lock/lifecycle. Reopening can settle old reservations.
Symbol-neighborhood mode projects one to eight exact structured names from
owner-recorded context metadata, without checking retained proof snapshots or
opening custody. It emits a conjunction of existing type-symbol features and
does not assert that this context is load-ready. Exact-type modes are unchanged.
Directory export captures all recorded bindings once for historical advisory
lookup, through the same metadata validation and close-before-publication rules.
Every requested name must resolve; missing names never weaken the conjunction.
No mode runs Lean, fetches evidence, accepts mathematics or queries peers.
The meaning is the selected receiver interpretation, not project equivalence.
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
    state = [getattr(args, field, None) for field in ("catalog", "store_id")]
    custody = [getattr(args, field, None) for field in ("custody", "custody_limits")]
    advisory = (getattr(args, "symbol_names", None) is not None or
                getattr(args, "directory_export", None) is not None)
    if contextual:
        need(all(value is not None for value in state) and
             (all(value is None for value in custody) if advisory else
              all(value is not None for value in custody)), "QUERY_CONTEXT_ARGUMENTS")
    else:
        need(all(value is None for value in state+custody), "QUERY_CONTEXT_ARGUMENTS")
    return "context" if contextual else "manual"


def query_kind(args):
    native = getattr(args, "native_type", None) is not None
    symbols = getattr(args, "symbol_names", None) is not None
    directory = getattr(args, "directory_export", None) is not None
    need(sum((native, symbols, directory)) == 1, "QUERY_EXACTLY_ONE_INPUT_KIND")
    if directory:
        need(args.directory_export == "v1" and binding_mode(args) == "context",
             "QUERY_DIRECTORY_REQUIRES_CONTEXT_V1")
        return "directory-export"
    if symbols:
        need(binding_mode(args) == "context", "QUERY_SYMBOLS_REQUIRE_CONTEXT")
    return "symbol-neighborhood" if symbols else "exact-type"


def arguments():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+name, required=True, type=int)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--native-type", help="Existing canonical native type AST JSON")
    inputs.add_argument("--symbol-names", help="Canonical list of one to eight exact structured Lean names")
    inputs.add_argument("--directory-export", choices=("v1",),
                        help="Export all historical advisory bindings at the selected root")
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--bindings", help="Existing exact canonical binding rows; no owner opening")
    modes.add_argument("--context-root", help="Exact existing owner context supplying query bindings")
    for name in ("catalog", "store-id"):
        parser.add_argument("--"+name, help="Required with --context-root")
    for name in ("custody", "custody-limits"):
        parser.add_argument("--"+name, help="Required for contextual exact-type mode; forbidden for symbol mode")
    args = parser.parse_args()
    try:
        binding_mode(args)
        query_kind(args)
    except ValueError as error:
        parser.error(str(error))
    return args


def run_manual(args):
    allocation, created, output, result = None, False, None, None
    phase = "BOOTSTRAP"
    try:
        need(query_kind(args) == "exact-type" and binding_mode(args) == "manual",
             "QUERY_MANUAL_EXACT_TYPE_ONLY")
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
        spec = Q.query_spec(query_raw)
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
            "claim": "BOUNDED_EXACT_TYPE_SEARCH_INPUT_NOT_THEOREM_OR_GLOBAL_COVERAGE",
            "next": "Use specs in existing peer.py find with explicit contacts and budgets"}
        allocation.check()
    except BaseException as error:
        result = {"ok": False, "phase": phase, "error_type": type(error).__name__,
                  "error": str(error)[:2000], "mathematical_acceptance": False,
                  "retention": "PARTIAL_OUTPUT_RETAINED_NO_RETRY"}
    result.update(operation="prepare-query", query_kind="exact-type")
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


def read_symbol_names(Q, names_raw):
    """Bounded exact original names, without Lean parsing or namespace lookup."""
    need(type(names_raw) is bytes and 0 < len(names_raw) <= 65536,
         "QUERY_SYMBOL_NAMES_BYTES")
    names = Q.E.strict_json(names_raw, Q.DEFAULT_LIMITS.codec)
    need(type(names) is list and 1 <= len(names) <= 8, "QUERY_SYMBOL_NAMES_COUNT")
    keys = [Q.E.name_key(name, Q.DEFAULT_LIMITS.codec) for name in names]
    need(len(set(keys)) == len(keys), "QUERY_SYMBOL_NAMES_DUPLICATE")
    return names


def resolve_names(Q, names, context_bindings, check):
    """Pure reference projection, not a source of owner or theorem authority."""
    need(type(context_bindings) is dict and callable(check), "QUERY_CONTEXT_BINDING_MAP")
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


def resolve_context_bindings(Q, native_raw, context_bindings, check):
    return resolve_names(Q, Q.reference_names(native_raw), context_bindings, check)


def load_advisory_context(loaded, check):
    """Execute only the explicitly profiled root auxiliary's captured bytes."""
    name, filename = "_dmkn_advisory_context", "advisory_context.py"
    need(name not in sys.modules, "QUERY_ADVISORY_PRELOADED")
    pin = loaded.descriptor["files"].get(filename)
    need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
         type(pin["bytes"]) is int and 0 < pin["bytes"] <= 2*MIB,
         "QUERY_ADVISORY_PIN")
    loaded.A.C.hexid(pin["sha256"])
    path = loaded.A.C.ordinary(loaded.root/filename)
    check()
    raw = loaded.A.C.read_bounded(path, 2*MIB)
    need(len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"],
         "QUERY_ADVISORY_CHANGED")
    check()
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec"), module.__dict__)
        need(callable(getattr(module, "project", None)), "QUERY_ADVISORY_API")
    except BaseException:
        del sys.modules[name]
        raise
    check()
    return module


def load_directory_index(loaded, check):
    """Load the exact profiled pure auxiliary; never import a cwd-relative file."""
    name, filename = "_dmkn_name_directory", "directory_index.py"
    need(name not in sys.modules, "QUERY_DIRECTORY_PRELOADED")
    pin = loaded.descriptor["files"].get(filename)
    need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
         type(pin["bytes"]) is int and 0 < pin["bytes"] <= 2*MIB,
         "QUERY_DIRECTORY_PIN")
    loaded.A.C.hexid(pin["sha256"])
    path = loaded.A.C.ordinary(loaded.root/filename)
    check()
    raw = loaded.A.C.read_bounded(path, 2*MIB)
    need(len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"],
         "QUERY_DIRECTORY_CHANGED")
    check()
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec"), module.__dict__)
        need(callable(getattr(module, "build", None)), "QUERY_DIRECTORY_API")
    except BaseException:
        del sys.modules[name]
        raise
    check()
    return module


def advisory_projection(Q, context, names, installation, store_id, local_root, check):
    """Reject extra authority/data and inconsistent selected-name projections."""
    need(type(context) is dict and set(context) == {
        "local_root", "semantic_id", "foundation_id", "implementation_id", "store_id",
        "bindings", "missing_names", "snapshot_integrity", "context_readiness",
        "mathematical_acceptance", "owner_closure"}, "QUERY_ADVISORY_FIELDS")
    need(context["local_root"] == local_root and context["store_id"] == store_id and
         context["semantic_id"] == installation.semantic_id and
         context["foundation_id"] == Q.S.foundation_id() and
         context["implementation_id"] == installation.implementation_id,
         "QUERY_CONTEXT_IDENTITY")
    need(context["snapshot_integrity"] == "NOT_CHECKED" and
         context["context_readiness"] == "NOT_ASSERTED" and
         context["mathematical_acceptance"] is False and
         context["owner_closure"] == "CLOSED", "QUERY_ADVISORY_BOUNDARY")
    bindings = context["bindings"]
    need(type(bindings) is dict, "QUERY_ADVISORY_BINDINGS")
    keys = {Q.E.name_key(name, Q.DEFAULT_LIMITS.codec) for name in names}
    need(set(bindings) <= keys, "QUERY_ADVISORY_UNREQUESTED_BINDING")
    for symbol in bindings.values():
        check(); Q.E._hex(symbol)
    raw, missing = resolve_names(Q, names, bindings, check)
    need(context["missing_names"] == missing, "QUERY_ADVISORY_MISSING_DISAGREEMENT")
    return raw, missing


def run_context(args):
    allocation = owner = custody = output = None
    context_selection, result = None, None
    kind, operation, input_pins = None, "prepare-query", {}
    created = publication_attempted = published = False
    result_sha256 = None
    advisory_closure = "NOT_OPENED"
    phase = "BOOTSTRAP"
    try:
        kind = query_kind(args)
        operation = "prepare-symbol-query" if kind == "symbol-neighborhood" else "prepare-query"
        need(binding_mode(args) == "context", "QUERY_CONTEXT_MODE")
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
        input_path = A.C.ordinary(Path(args.symbol_names if kind == "symbol-neighborhood" else args.native_type))
        limits_path = None
        input_maximum = 65536 if kind == "symbol-neighborhood" else MIB
        input_raw = A.C.read_bounded(input_path, input_maximum)
        # Reject malformed names/type syntax before owner recovery/opening.
        if kind == "symbol-neighborhood":
            names = read_symbol_names(Q, input_raw)
            input_pins["names_sha256"] = hashlib.sha256(input_raw).hexdigest()
        else:
            Q.read_native_type(input_raw)
            input_pins["native_type_sha256"] = hashlib.sha256(input_raw).hexdigest()
        if kind == "exact-type":
            limits_path = A.C.ordinary(Path(args.custody_limits))
            limits_raw = A.C.read_bounded(limits_path, 65536)
            input_pins["custody_limits_sha256"] = hashlib.sha256(limits_raw).hexdigest()
            custody_limits = A._writer_json(limits_raw, 65536)
            A.P.fields(custody_limits, O.STORE_LIMITS, "QUERY_CUSTODY_LIMITS")
            for key, bounds in O.STORE_LIMITS.items():
                A.P.uint(custody_limits[key], *bounds, "QUERY_CUSTODY_LIMIT:"+key)
        catalog_path = A.C.ordinary(Path(args.catalog), directory=True)
        state_paths = [catalog_path]
        if kind == "exact-type":
            custody_path = A.C.ordinary(Path(args.custody), directory=True)
            state_paths.append(custody_path)
        output = A.C.ordinary(Path(args.output), directory=True, fresh=True)
        base.separated([output, *state_paths, root,
                        *installation.runtime_roots.values()], "QUERY_CONTEXT_PATH_OVERLAP")
        for path in (input_path, *((limits_path,) if limits_path is not None else ())):
            need(all(not path.is_relative_to(directory)
                     for directory in (output, *state_paths)), "QUERY_CONTEXT_INPUT_OVERLAP")
        marker = A.E.strict_json(A.C.read_bounded(catalog_path/"ADOPTION.json", 65536),
                                A.E.Limits(max_bytes=65536))
        A.P.fields(marker, ("schema", "store_id", "implementation", "limits"), "QUERY_ADOPTION_FIELDS")
        need(marker["schema"] == A.P.SCHEMA and marker["store_id"] == args.store_id and
             marker["implementation"] == installation.doc["implementation"], "QUERY_ADOPTION_BINDING")
        limits = A.P.Limits(**marker["limits"])
        allocation.check()
        if kind == "symbol-neighborhood":
            phase = "LOAD_ADVISORY_HELPER"
            advisory = load_advisory_context(loaded, allocation.check)
            phase = "PROJECT_RECORDED_CONTEXT"
            advisory_closure = "NOT_CONFIRMED"
            context = advisory.project(installation, catalog_path, args.store_id,
                args.context_root, names, limits=limits, check=allocation.check, catalog_module=A.P)
            bindings_raw, missing = advisory_projection(Q, context, names, installation,
                args.store_id, args.context_root, allocation.check)
            advisory_closure = "CLOSED"
        else:
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
        context_selection = {key: context[key] for key in
                             ("semantic_id", "foundation_id", "implementation_id")}
        context_selection.update(store_id=args.store_id, context_root=args.context_root)
        if kind == "exact-type":
            bindings_raw, missing = resolve_context_bindings(Q, input_raw, context["bindings"], allocation.check)
        if missing:
            result = {"ok": False, "operation": operation, "status": "UNMAPPED_REFERENCES",
                "phase": phase, "missing_names": missing, "mathematical_acceptance": False,
                "retention": "NO_QUERY_OUTPUT_NO_FETCH_OR_RETRY"}
        else:
            phase = "QUERY"
            binding_rows = Q.E.strict_json(bindings_raw)
            if kind == "symbol-neighborhood":
                specs = [{"tag": "type-symbol", "symbol": {
                    "kind": "portable-symbol", "symbol_id": symbol}} for _, symbol in binding_rows]
                query_fields = {"names_sha256": input_pins["names_sha256"],
                    "claim": "BOUNDED_TYPE_SYMBOL_CONJUNCTION_NOT_THEOREM_OR_GLOBAL_COVERAGE"}
                query_files = (("SYMBOL-NAMES.json", input_raw),)
            else:
                query_raw = Q.bind_native_type(input_raw, bindings_raw, semantic_id=installation.semantic_id)
                specs = [Q.query_spec(query_raw)]
                query_fields = {"key_profile": Q.PROFILE_ID,
                    "query_sha256": hashlib.sha256(query_raw).hexdigest(),
                    "native_type_sha256": input_pins["native_type_sha256"],
                    "claim": "BOUNDED_EXACT_TYPE_SEARCH_INPUT_NOT_THEOREM_OR_GLOBAL_COVERAGE"}
                query_files = (("QUERY.json", query_raw),)
            namespace = adapter.namespace_for(installation.semantic_id)
            features = adapter.compile_query(namespace, specs)
            context_selection["reference_count"] = len(binding_rows)
            result = {"ok": True, "operation": operation, "namespace": namespace,
                "specs": specs, "features": features,
                "bindings_sha256": hashlib.sha256(bindings_raw).hexdigest(),
                "profile_sha256": args.profile_sha256, "mathematical_acceptance": False,
                **query_fields,
                "next": "Use specs in existing peer.py find with explicit contacts and budgets"}
        phase = "FINAL_VALIDATION"
        need(A.C.read_bounded(input_path, input_maximum) == input_raw, "QUERY_INPUT_CHANGED")
        if limits_path is not None:
            need(A.C.read_bounded(limits_path, 65536) == limits_raw, "QUERY_INPUT_CHANGED")
        loaded.profile.verify(allocation.check)
        allocation.check()
    except BaseException as error:
        result = {"ok": False, "operation": operation, "phase": phase,
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
            query_kind=kind, profile_sha256=args.profile_sha256, input_pins=input_pins,
            owner_closure="FAILED" if any(item["component"] == "owner" for item in close_errors)
                          else "CLOSED" if owner is not None else "NOT_OPENED",
            custody_closure="FAILED" if any(item["component"] == "custody" for item in close_errors)
                            else "CLOSED" if custody is not None else "NOT_OPENED",
            interpretation="SELECTED_RECEIVER_CONTEXT_NOT_PROJECT_EQUIVALENCE")
        if kind == "symbol-neighborhood":
            result.update(owner_closure=advisory_closure, custody_closure="NOT_OPENED",
                snapshot_integrity="NOT_CHECKED", context_readiness="NOT_ASSERTED",
                interpretation="RECORDED_ROOT_SEARCH_BINDINGS_NOT_LOAD_READY_OR_PROJECT_EQUIVALENCE")

    # No success publication is attempted until every opened state handle closes.
    # Symbol mode's helper owns the only handle and returns after its close.
    try:
        if allocation is not None:
            allocation.check()
        if result["ok"]:
            phase = "OUTPUT"
            output.mkdir(); created = True
            for filename, raw in (("BINDINGS.json", bindings_raw), *query_files,
                                   ("SPECS.json", A.E.canonical_json(specs))):
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
        failure = {"ok": False, "operation": operation, "phase": phase,
            "error_type": type(error).__name__, "error": str(error)[:2000],
            "binding_mode": "selected-local-context", "context_selection": context_selection,
            "query_kind": kind, "profile_sha256": args.profile_sha256, "input_pins": input_pins,
            "owner_closure": result["owner_closure"], "custody_closure": result["custody_closure"],
            "interpretation": result["interpretation"],
            "mathematical_acceptance": False, "retention": "PARTIAL_OUTPUT_RETAINED_NO_RETRY",
            "output": str(output) if created else None,
            "result_publication": "PUBLISHED" if published else "UNKNOWN" if publication_attempted else "NOT_ATTEMPTED",
            "attempted_result_sha256": result_sha256}
        if close_errors:
            failure["close_errors"] = close_errors
        if kind == "symbol-neighborhood":
            failure.update(snapshot_integrity="NOT_CHECKED", context_readiness="NOT_ASSERTED")
        failure["cost"] = allocation.report() if allocation is not None else {
            "wall_seconds": time.monotonic()-START_WALL,
            "controller_cpu_seconds": time.process_time()-START_CPU,
            "worker_cpu_seconds": 0, "controller_limits": "COOPERATIVE_REQUIRES_EXTERNAL_JOB"}
        return failure, json.dumps(failure, sort_keys=True, ensure_ascii=False, allow_nan=False,
                                   separators=(",", ":")).encode("utf-8")


def run_directory(args):
    """Export one complete historical map, with no current-state lookup promise."""
    allocation = output = context_selection = receipt = None
    created, build_started = False, False
    closure, phase = "NOT_OPENED", "BOOTSTRAP"
    try:
        need(query_kind(args) == "directory-export" and binding_mode(args) == "context",
             "QUERY_DIRECTORY_CONTEXT_MODE")
        need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
             sys.dont_write_bytecode and not sys.flags.optimize, "QUERY_PYTHON_PROFILE")
        need(type(args.wall_seconds) is int and 35 <= args.wall_seconds <= 3600 and
             type(args.cpu_seconds) is int and 4 <= args.cpu_seconds <= 600,
             "QUERY_FINITE_ALLOWANCE")
        deadline = START_WALL+args.wall_seconds
        def bootstrap_check():
            need(time.monotonic() < deadline and
                 time.process_time()-START_CPU < args.cpu_seconds, "QUERY_ALLOWANCE")
        root = Path(__file__).absolute().parent
        base = bootstrap_owner(root, args.profile_sha256, bootstrap_check)
        allocation = base.Allowance(args)
        loader = base.bootstrap(root, args.profile_sha256, allocation.check)
        loaded = loader.load(root, args.profile_sha256,
            {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
            allocation.deadline, check_parent=allocation.check)
        A, installation = loaded.A, loaded.installation
        auth = sys.modules.get("discovery.authenticated_index")
        features = sys.modules.get("discovery.formal_features")
        need(A.E is sys.modules.get("ordinary_evidence") and
             auth is not None and features is not None and
             auth.hexid is features.hexid and auth._digest is features.digest and
             Path(auth.__file__).absolute() == root/"support/discovery/authenticated_index.py" and
             Path(features.__file__).absolute() == root/"support/discovery/formal_features.py",
             "QUERY_DIRECTORY_SHARED_HELPERS")
        phase = "INPUTS"
        A.C.hexid(args.context_root); A.C.hexid(args.store_id)
        catalog_path = A.C.ordinary(Path(args.catalog), directory=True)
        output = A.C.ordinary(Path(args.output), directory=True, fresh=True)
        base.separated([output, catalog_path, root, *installation.runtime_roots.values()],
                       "QUERY_CONTEXT_PATH_OVERLAP")
        marker = A.E.strict_json(A.C.read_bounded(catalog_path/"ADOPTION.json", 65536),
                                A.E.Limits(max_bytes=65536))
        A.P.fields(marker, ("schema", "store_id", "implementation", "limits"), "QUERY_ADOPTION_FIELDS")
        need(marker["schema"] == A.P.SCHEMA and marker["store_id"] == args.store_id and
             marker["implementation"] == installation.doc["implementation"], "QUERY_ADOPTION_BINDING")
        limits = A.P.Limits(**marker["limits"])
        phase = "LOAD_DIRECTORY_HELPERS"
        advisory = load_advisory_context(loaded, allocation.check)
        need(callable(getattr(advisory, "snapshot", None)), "QUERY_DIRECTORY_SNAPSHOT_API")
        directory = load_directory_index(loaded, allocation.check)
        phase = "EXPORT_RECORDED_CONTEXT"
        closure = "NOT_CONFIRMED"
        context = advisory.snapshot(installation, catalog_path, args.store_id,
            args.context_root, limits=limits, check=allocation.check, catalog_module=A.P)
        need(type(context) is dict and set(context) == {
            "local_root", "semantic_id", "foundation_id", "implementation_id", "store_id",
            "bindings", "missing_names", "snapshot_integrity", "context_readiness",
            "mathematical_acceptance", "binding_count", "coverage", "owner_closure"},
            "QUERY_DIRECTORY_CONTEXT_FIELDS")
        need(context["local_root"] == args.context_root and context["store_id"] == args.store_id and
             context["semantic_id"] == installation.semantic_id and
             context["foundation_id"] == A.S.foundation_id() and
             context["implementation_id"] == installation.implementation_id,
             "QUERY_CONTEXT_IDENTITY")
        need(context["snapshot_integrity"] == "NOT_CHECKED" and
             context["context_readiness"] == "NOT_ASSERTED" and
             context["mathematical_acceptance"] is False and context["owner_closure"] == "CLOSED" and
             context["coverage"] == "COMPLETE_RECORDED_BINDINGS_AT_SELECTED_ROOT" and
             context["missing_names"] == [] and type(context["bindings"]) is dict and
             type(context["binding_count"]) is int and
             1 <= context["binding_count"] == len(context["bindings"]) <= 1048576,
             "QUERY_DIRECTORY_CONTEXT_BOUNDARY")
        closure = "CLOSED"
        context_selection = {key: context[key] for key in
                             ("semantic_id", "foundation_id", "implementation_id", "store_id")}
        context_selection.update(context_root=args.context_root)
        from datetime import datetime, timezone
        metadata = dict(context_selection,
            source_profile_sha256=args.profile_sha256,
            name_codec_sha256=installation.doc["files"][installation.doc["roles"]["evidence"]]["sha256"],
            exported_at_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        def final_check():
            loaded.profile.verify(allocation.check)
            allocation.check()
        phase = "FINAL_VALIDATION"
        final_check()
        phase = "DIRECTORY_BUILD"
        output.mkdir(); created = True
        build_started = True
        receipt = directory.build(context["bindings"], output, metadata, evidence=A.E,
            auth=auth, check=allocation.check, final_check=final_check)
        need(type(receipt) is dict and set(receipt) == {
            "directory_manifest_sha256", "directory_manifest", "entries", "records_bytes", "tree_bytes"}
             and receipt["entries"] == context["binding_count"], "QUERY_DIRECTORY_RECEIPT")
        allocation.check()
        result = {"ok": True, "status": "EXPORTED_HISTORICAL_NAME_DIRECTORY",
                  "directory_receipt": receipt, "directory_publication": "COMPLETE"}
    except BaseException as error:
        result = {"ok": False, "phase": phase, "error_type": type(error).__name__,
                  "error": str(error)[:2000], "retention": "PARTIAL_OUTPUT_RETAINED_NO_RETRY",
                  "directory_publication": "COMPLETE" if receipt is not None else
                                           "UNKNOWN" if build_started else "NOT_ATTEMPTED",
                  "directory_receipt": receipt}
    result.update(operation="export-name-directory", query_kind="directory-export",
        binding_mode="selected-local-context", context_selection=context_selection,
        profile_sha256=args.profile_sha256, owner_closure=closure, custody_closure="NOT_OPENED",
        snapshot_integrity="NOT_CHECKED", context_readiness="NOT_ASSERTED",
        current_owner_state="NOT_ASSERTED_BY_DIRECTORY", mathematical_acceptance=False,
        interpretation="HISTORICAL_RECORDED_BINDINGS_NOT_CURRENT_STATE_OR_ACCEPTANCE",
        output=str(output) if created else None)
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
            # The committed directory, if any, remains historical output even
            # when this auxiliary report cannot be written. Never erase it.
            result.update(ok=False, report_write_error=str(error)[:500])
            raw = json.dumps(result, sort_keys=True, allow_nan=False).encode("utf-8")
    return result, raw


def run(args):
    # This also validates programmatic callers before they can open any state.
    try:
        mode = binding_mode(args)
        kind = query_kind(args)
    except ValueError as error:
        result = {"ok": False, "phase": "ARGUMENTS", "error_type": "ValueError",
                  "error": str(error), "mathematical_acceptance": False}
        return result, json.dumps(result, sort_keys=True, allow_nan=False).encode("utf-8")
    if kind == "directory-export":
        return run_directory(args)
    return run_context(args) if mode == "context" else run_manual(args)


if __name__ == "__main__":
    result, raw = run(arguments())
    sys.stdout.buffer.write(raw+b"\n")
    sys.stdout.buffer.flush()
    raise SystemExit(0 if result["ok"] else 1)

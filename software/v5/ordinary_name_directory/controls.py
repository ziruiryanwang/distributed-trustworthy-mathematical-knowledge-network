"""Focused inert directory controls. Root selects execution separately.

Uses the real name codec and existing ordinal-vector verifier. All directories
are fresh synthetic files below the selected output; no owner or native state.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import time
from types import ModuleType, SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
START, CPU = time.monotonic(), time.process_time()


def need(ok, code):
    if not ok:
        raise AssertionError("DIRECTORY_CONTROL_" + code)


def check():
    need(time.monotonic() - START < 45 and time.process_time() - CPU < 25,
         "ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def forbidden(*args, **kwargs):
    raise AssertionError("DIRECTORY_CONTROL_FORBIDDEN_NATIVE_NETWORK_DATABASE")


def refuses(call, code=None):
    try:
        call()
    except ValueError as error:
        need(code is None or str(error) == code, "REFUSAL:" + str(error))
        return str(error)
    raise AssertionError("DIRECTORY_CONTROL_EXPECTED_REFUSAL:" + str(code))


def name(*parts):
    return [[1, part] if type(part) is int else
            [0, {"$bytes": list(part.encode("utf-8"))}] for part in parts]


class Reader:
    """Counts and bounds every actual requested slice; optional inert corruption."""
    def __init__(self, raw, unit, mutate=None):
        self.raw, self.unit, self.mutate = raw, unit, mutate
        self.calls, self.bytes = [], 0

    def __call__(self, offset, size):
        check()
        need(type(offset) is int and type(size) is int and size == self.unit and
             offset >= 0 and offset % self.unit == 0 and offset + size <= len(self.raw),
             "FIXED_BOUNDED_READ")
        self.calls.append((offset, size))
        self.bytes += size
        raw = self.raw[offset:offset + size]
        return self.mutate(offset, raw, len(self.calls)) if self.mutate else raw


def controls(D, E, A, F, output, codec_pin):
    groups = []
    metadata = dict(semantic_id="1" * 64, foundation_id="2" * 64,
                    implementation_id="3" * 64, store_id="4" * 64,
                    context_root="5" * 64, source_profile_sha256="6" * 64,
                    name_codec_sha256=codec_pin,
                    exported_at_utc="2026-10-28T00:00:00Z")

    def fixture(label, names, meta=None, bindings=None, final_check=check):
        directory = output / label
        directory.mkdir()
        if bindings is None:
            bindings = {E.name_key(n): sha(b"directory-control-symbol\0" + E.name_key(n))
                        for n in names}
        result = D.build(bindings, directory, metadata if meta is None else meta,
                         evidence=E, auth=A, check=check, final_check=final_check)
        raw = (directory / "DIRECTORY.json").read_bytes()
        entries = (directory / "ENTRIES.bin").read_bytes()
        tree = (directory / "TREE.bin").read_bytes()
        need(result["directory_manifest_sha256"] == sha(raw) and
             result["directory_manifest"] == json.loads(raw) and
             result["entries"] == len(bindings) and
             result["records_bytes"] == len(entries) and result["tree_bytes"] == len(tree),
             "BUILD_RESULT")
        return dict(directory=directory, result=result, raw=raw, entries=entries,
                    tree=tree, bindings=bindings)

    def lookup(fx, requested, entry_mutate=None, tree_mutate=None,
               manifest_raw=None, manifest_pin=None, tree_raw=None):
        er = Reader(fx["entries"], 64, entry_mutate)
        tr = Reader(fx["tree"] if tree_raw is None else tree_raw, 32, tree_mutate)
        raw = fx["raw"] if manifest_raw is None else manifest_raw
        pin = sha(fx["raw"]) if manifest_pin is None else manifest_pin
        result = D.lookup_open(raw, pin, er, tr, requested, evidence=E, auth=A, check=check)
        need(result["io"]["entry_reads"] == len(er.calls) and
             result["io"]["entry_bytes"] == er.bytes and
             result["io"]["tree_reads"] == len(tr.calls) and
             result["io"]["tree_bytes"] == tr.bytes and
             result["mathematical_acceptance"] is False and
             result["owner_opened"] is False and
             result["coverage"] == "SELECTED_HISTORICAL_DIRECTORY_ONLY",
             "RESULT_SCOPE_AND_REAL_IO")
        return result, er, tr

    def ready(fx, requested):
        result, er, tr = lookup(fx, requested)
        expected = [[n, fx["bindings"][E.name_key(n)]] for n in requested]
        specs = [{"tag": "type-symbol", "symbol": {
                  "kind": "portable-symbol", "symbol_id": symbol}}
                 for _, symbol in expected]
        need(result["status"] == "DIRECTORY_QUERY_READY" and
             result["bindings"] == expected and result["missing_names"] == [] and
             result["specs"] == specs, "EXACT_READY")
        return result, er, tr

    # Choose records and absent requests by exact hash order. No lucky preimage
    # search is required to ensure both boundaries and an interior interval.
    pool = [name("DirectoryControl", i) for i in range(32)]
    pool.sort(key=lambda n: D.name_digest(E.name_key(n), A))
    selected = [pool[i] for i in (4, 10, 16, 22, 28)]
    fx = fixture("five", selected)
    ready(fx, [selected[4], selected[0], selected[2]])
    need(len(fx["entries"]) == 5 * 64 and len(fx["tree"]) == 15 * 32,
         "NON_POWER_OF_TWO_LAYOUT")
    groups.append("real-codec-exact-hits-and-nonpower-layout")

    for label, absent, expected_auth in (("left", pool[0], 1),
                                        ("interior", pool[7], 2),
                                        ("right", pool[31], 1)):
        result, _, _ = lookup(fx, [absent])
        need(result["status"] == "DIRECTORY_NAMES_MISSING" and
             result["missing_names"] == [absent] and result["bindings"] == [] and
             "specs" not in result and result["io"]["authenticated_records"] == expected_auth,
             "AUTHENTICATED_ABSENCE:" + label)
    result, _, _ = lookup(fx, [selected[0], pool[7], selected[3]])
    need(result["missing_names"] == [pool[7]] and len(result["bindings"]) == 2 and
         "specs" not in result, "NO_WEAKER_CONJUNCTION")
    groups.append("authenticated-first-last-interior-absence-all-or-none")

    # This first unauthenticated midpoint lies about its key and skips a real
    # requested hit. All final endpoint bytes/proofs are honest. The interval
    # comparison, rather than trusting the corrupted search route, must refuse.
    midpoint = (len(selected) // 2) * 64
    altered = [0]
    def steer(offset, raw, ordinal):
        if offset == midpoint and altered[0] == 0:
            altered[0] += 1
            return bytes(32) + raw[32:]
        return raw
    refuses(lambda: lookup(fx, [selected[0]], entry_mutate=steer),
            "DIRECTORY_ABSENCE_INTERVAL")
    need(altered == [1], "CORRUPTED_MIDPOINT_REACHED")
    groups.append("untrusted-midpoint-steering-cannot-prove-false-absence")

    def alter_symbol(offset, raw, ordinal):
        return raw[:32] + bytes([raw[32] ^ 1]) + raw[33:] if offset == 0 else raw
    refuses(lambda: lookup(fx, [selected[0]], entry_mutate=alter_symbol),
            "VECTOR_PROOF_ROOT")
    def alter_sibling(offset, raw, ordinal):
        return bytes([raw[0] ^ 1]) + raw[1:] if ordinal == 1 else raw
    refuses(lambda: lookup(fx, [selected[0]], tree_mutate=alter_sibling),
            "VECTOR_PROOF_ROOT")
    refuses(lambda: lookup(fx, [selected[0]], entry_mutate=lambda o, r, i: r[:-1]),
            "DIRECTORY_ENTRY_READ")
    refuses(lambda: lookup(fx, [selected[0]], tree_mutate=lambda o, r, i: r[:-1]),
            "DIRECTORY_TREE_READ")
    groups.append("changed-entry-sibling-and-short-read-refuse")

    refuses(lambda: lookup(fx, [selected[0]], manifest_pin="0" * 64),
            "DIRECTORY_MANIFEST_PIN")
    bad = deepcopy(fx["result"]["directory_manifest"])
    bad["count"] = True
    raw = E.canonical_json(bad)
    refuses(lambda: lookup(fx, [selected[0]], manifest_raw=raw, manifest_pin=sha(raw)),
            "DIRECTORY_COUNT")
    bad = deepcopy(fx["result"]["directory_manifest"])
    bad["metadata"]["context_root"] = "a" * 64
    raw = E.canonical_json(bad)
    refuses(lambda: lookup(fx, [selected[0]], manifest_raw=raw, manifest_pin=sha(raw)),
            "DIRECTORY_CONTEXT")
    bad = deepcopy(fx["result"]["directory_manifest"])
    bad["entries_bytes"] += 64
    raw = E.canonical_json(bad)
    refuses(lambda: lookup(fx, [selected[0]], manifest_raw=raw, manifest_pin=sha(raw)),
            "DIRECTORY_FILE_SIZES")
    groups.append("descriptor-pin-context-count-and-layout-binding")

    for field in ("context_root", "source_profile_sha256", "semantic_id"):
        changed = dict(metadata, **{field: "b" * 64})
        other = fixture("changed-" + field, selected, meta=changed)
        need(other["entries"] == fx["entries"] and other["tree"] != fx["tree"],
             "METADATA_CONTEXT_ISOLATION")
        refuses(lambda: lookup(fx, [selected[0]], tree_raw=other["tree"]),
                "VECTOR_PROOF_ROOT")
        result, _, _ = ready(other, [selected[0]])
        need(result["metadata"] == changed, "HISTORICAL_METADATA_RETAINED")
    groups.append("same-records-cannot-cross-root-profile-or-semantic-context")

    special = [name("Names", 7), name("Names", "7"), name("Names", "a.b"),
               name("Names", "a", "b"), name("\u6570\u5b66", "\U00020bb7"),
               name("Names", 0), name("Names", "\u00e9"), name("Names", "e\u0301")]
    sx = fixture("exact-names", special)
    need(len(sx["bindings"]) == 8, "DISTINCT_EXACT_NAME_KEYS")
    ready(sx, list(reversed(special)))
    refuses(lambda: lookup(sx, []), "DIRECTORY_QUERY_COUNT")
    refuses(lambda: lookup(sx, special + [name("Extra")]), "DIRECTORY_QUERY_COUNT")
    refuses(lambda: lookup(sx, [special[0], deepcopy(special[0])]), "DIRECTORY_QUERY_DUPLICATE")
    refuses(lambda: lookup(sx, [name("_kernel_freshForbidden")]))
    groups.append("unicode-numeric-exact-name-codec-and-one-through-eight-bound")

    one = fixture("singleton", [selected[0]])
    result, _, tr = ready(one, [selected[0]])
    need(not tr.calls and result["io"]["authenticated_records"] == 1,
         "SINGLETON_EMPTY_PATH")
    for absent in (pool[0], pool[31]):
        result, _, tr = lookup(one, [absent])
        need(result["status"] == "DIRECTORY_NAMES_MISSING" and not tr.calls and
             result["io"]["authenticated_records"] == 1, "SINGLETON_BOUNDARY")
    empty = fixture("empty", [])
    result, er, tr = lookup(empty, [selected[0]])
    need(result["status"] == "DIRECTORY_NAMES_MISSING" and "specs" not in result and
         result["io"]["authenticated_records"] == 0 and not er.calls and not tr.calls,
         "EMPTY_COMMITTED_VECTOR")
    groups.append("singleton-zero-height-and-supported-empty-vector")

    collision_dir = output / "collision"
    collision_dir.mkdir()
    same_symbol = {E.name_key(n): "c" * 64 for n in selected[:2]}
    with patch.object(D, "name_digest", return_value=bytes(32)):
        refuses(lambda: D.build(same_symbol, collision_dir, metadata, evidence=E,
                                auth=A, check=check, final_check=check),
                "DIRECTORY_DUPLICATE_NAME_DIGEST")
    need(not list(collision_dir.iterdir()), "COLLISION_NO_PUBLICATION")
    groups.append("distinct-names-same-symbol-hash-collision-refuses-before-write")

    stopped = output / "stopped-before-manifest"
    stopped.mkdir()
    def stop():
        raise ValueError("CONTROL_FINAL_STOP")
    refuses(lambda: D.build(fx["bindings"], stopped, metadata, evidence=E, auth=A,
                            check=check, final_check=stop), "CONTROL_FINAL_STOP")
    need((stopped / "ENTRIES.bin").is_file() and (stopped / "TREE.bin").is_file() and
         not (stopped / "DIRECTORY.json").exists(), "NO_FINAL_MANIFEST_ON_FAILURE")
    refuses(lambda: D.build(fx["bindings"], fx["directory"], metadata, evidence=E,
                            auth=A, check=check, final_check=check),
            "DIRECTORY_EMPTY_OUTPUT_REQUIRED")
    groups.append("final-source-budget-failure-and-existing-output-no-publication")

    many_names = [name("CountBound", i) for i in range(257)]
    many = fixture("read-bound-257", many_names)
    requested = [many_names[i] for i in (0, 1, 31, 64, 128, 192, 255, 256)]
    result, er, tr = ready(many, requested)
    height = (len(many_names) - 1).bit_length()
    probe_bound = len(many_names).bit_length()
    need(len(er.calls) <= len(requested) * (probe_bound + 2) and
         len(tr.calls) <= len(requested) * 2 * height and
         er.bytes + tr.bytes < len(many["entries"]) + len(many["tree"]) and
         result["io"]["authenticated_records"] == len(requested),
         "LOGARITHMIC_SLICE_BOUND_NO_FULL_HASH")
    groups.append("actual-reader-count-and-byte-bound-for-eight-fresh-names")
    check()
    return groups


def caller_controls(D, E, A, F, Q, H, output, codec_pin):
    """Changed caller seams with explicit inert lifecycle/installation doubles."""
    cases = []
    def arguments(**changes):
        values = dict(native_type=None, symbol_names=None, directory_export=None,
                      bindings=None, context_root=None, catalog=None, store_id=None,
                      custody=None, custody_limits=None, profile_sha256="6" * 64,
                      python_runtime="unused-python", lean_runtime="unused-lean",
                      wall_seconds=35, cpu_seconds=25, memory_mib=256, output="unused")
        values.update(changes)
        return NS(**values)
    modes = [(arguments(native_type="type", bindings="bindings"), "manual", "exact-type"),
             (arguments(native_type="type", context_root="r", catalog="c", store_id="s",
                        custody="u", custody_limits="l"), "context", "exact-type"),
             (arguments(symbol_names="names", context_root="r", catalog="c", store_id="s"),
              "context", "symbol-neighborhood"),
             (arguments(directory_export="v1", context_root="r", catalog="c", store_id="s"),
              "context", "directory-export")]
    for args, mode, kind in modes:
        need(Q.binding_mode(args) == mode and Q.query_kind(args) == kind, "MODE_COMPATIBILITY")
    with patch.object(Q, "bootstrap_owner", forbidden):
        for args in (arguments(directory_export="v1", bindings="bindings"),
                     arguments(directory_export="v2", context_root="r", catalog="c", store_id="s"),
                     arguments(directory_export="v1", native_type="type", context_root="r",
                               catalog="c", store_id="s"),
                     arguments(directory_export="v1", context_root="r", catalog="c", store_id="s",
                               custody="forbidden", custody_limits="forbidden")):
            result, _ = Q.run(args)
            need(result["ok"] is False and result["phase"] == "ARGUMENTS",
                 "BAD_MODE_REFUSES_BEFORE_BOOTSTRAP")
    cases.append("old-query-mode-compatibility-and-directory-arguments-before-opening")

    names = [name("Caller", "one"), name("Caller", "two")]
    bindings = {E.name_key(n): sha(E.name_key(n)) for n in names}
    # Exercise the actual shared reader's new full-map branch. No real catalog
    # class, SQLite connection, owner lock, snapshot or installation is supplied.
    for mode in ("good", "empty", "close-failure"):
        events = []
        class Limits:
            pass
        class Installation:
            pass
        class Catalog:
            @classmethod
            def open(cls, directory, implementation_raw, store_id, *, create, limits):
                return cls._open(directory, implementation_raw, store_id,
                                 create=create, limits=limits, importing=None)
            @classmethod
            def _open(cls, directory, implementation_raw, store_id, *, create, limits, importing):
                need(create is False and importing is None, "SNAPSHOT_NO_CREATE")
                events.append("open")
                return cls()
            def context(self, root):
                events.append("full-context")
                return dict(local_root=root, semantic_id="1" * 64,
                            foundation_id="2" * 64, implementation_id="3" * 64,
                            bindings={} if mode == "empty" else bindings,
                            modules=["MUST_NOT_ESCAPE"])
            def _active(self):
                events.append("active")
            def close(self):
                events.append("close")
                self._closed = True
                self._db = object() if mode == "close-failure" else None
                self._lock = None
        C = NS(ordinary=lambda path, **kw: Path(path))
        S = NS(foundation_id=lambda: "2" * 64)
        P = NS(PortableCatalog=Catalog, Limits=Limits, L=C, E=E, S=S, hexid=D.hexid)
        adm = NS(P=P, C=C, E=E, S=S, NativeInstallation=Installation)
        installation = Installation()
        installation.root = output / "synthetic-support"
        installation.runtime_roots = {"python": output / "synthetic-runtime"}
        installation.implementation_raw = b"synthetic"
        installation.semantic_id, installation.implementation_id = "1" * 64, "3" * 64
        call = lambda: H.snapshot(installation, output / "synthetic-owner", "4" * 64,
                                  "5" * 64, limits=Limits(), check=check, catalog_module=P)
        with patch.dict(sys.modules, {"ordinary_admission": adm, "portable_catalog": P}):
            if mode == "good":
                result = call()
                need(result["bindings"] == bindings and result["bindings"] is not bindings and
                     result["binding_count"] == 2 and result["owner_closure"] == "CLOSED" and
                     "modules" not in result and events == ["open", "full-context", "active", "close"],
                     "DETACHED_FULL_MAP_AFTER_CLOSE")
                projection = H.project(installation, output / "synthetic-owner", "4" * 64,
                    "5" * 64, [names[1]], limits=Limits(), check=check, catalog_module=P)
                need(projection["bindings"] == {E.name_key(names[1]): bindings[E.name_key(names[1])]} and
                     "binding_count" not in projection, "OLD_PROJECTION_UNCHANGED")
            else:
                refuses(call, "ADVISORY_DIRECTORY_NAME_COUNT" if mode == "empty" else
                              "ADVISORY_OWNER_CLOSURE")
                need(events[-1] == "close", "FAILED_FULL_MAP_CLOSES")
    cases.append("shared-advisory-full-map-close-empty-refusal-and-old-projection")

    # Drive actual run_directory orchestration while replacing all installed
    # owner/loading authority with named doubles. The real builder writes only
    # a fresh synthetic export; this tests ordering, not mathematical grounding.
    for mode in ("good", "bad-closure", "bad-root", "final-profile-failure"):
        folder = output / ("caller-" + mode)
        folder.mkdir()
        catalog = folder / "synthetic-catalog"
        catalog.mkdir()
        destination = folder / "export"
        events = []
        implementation = {"synthetic": "implementation"}
        marker = dict(schema="SYNTHETIC_CATALOG", store_id="4" * 64,
                      implementation=implementation, limits={})
        (catalog / "ADOPTION.json").write_bytes(E.canonical_json(marker))
        def ordinary(path, *, directory=False, fresh=False):
            path = Path(path)
            if fresh:
                need(not path.exists(), "CALLER_FRESH_PATH")
            return path
        def bounded(path, maximum):
            need(Path(path) == catalog / "ADOPTION.json", "ONLY_SYNTHETIC_ADOPTION_READ")
            raw = Path(path).read_bytes()
            need(len(raw) <= maximum, "CALLER_INPUT_BOUND")
            return raw
        def fields(value, expected, code):
            need(type(value) is dict and set(value) == set(expected), code)
        def write_fresh(path, raw):
            with Path(path).open("xb") as stream:
                stream.write(raw)
        C = NS(ordinary=ordinary, read_bounded=bounded, hexid=D.hexid)
        P = NS(SCHEMA="SYNTHETIC_CATALOG", fields=fields, Limits=lambda **kw: NS(),
               PortableCatalog=NS(_write_fresh=write_fresh))
        S = NS(foundation_id=lambda: "2" * 64)
        adm = NS(C=C, P=P, E=E, S=S)
        source_root = Path(Q.__file__).absolute().parent
        installation = NS(semantic_id="1" * 64, implementation_id="3" * 64,
            runtime_roots={"python": folder / "runtime-python", "lean": folder / "runtime-lean"},
            doc={"implementation": implementation, "roles": {"evidence": "unusual-codec-role.py"},
                 "files": {"unusual-codec-role.py": {"sha256": codec_pin}}})
        class Allocation:
            def __init__(self, args):
                self.deadline = time.monotonic() + 30
            def check(self):
                check()
            def report(self):
                return {"scope": "SYNTHETIC_CONTROL_ALLOCATION"}
        def verify(callback):
            callback()
            events.append("profile")
            if mode == "final-profile-failure" and events.count("profile") == 2:
                raise ValueError("CONTROL_FINAL_PROFILE_CHANGED")
        loaded = NS(A=adm, installation=installation, profile=NS(verify=verify))
        loader = NS(load=lambda *a, **kw: loaded)
        base = NS(Allowance=Allocation, bootstrap=lambda *a, **kw: loader,
                  separated=lambda paths, code: events.append("separated"))
        def snapshot(*args, **kwargs):
            events.append("snapshot-closed")
            return dict(local_root="a" * 64 if mode == "bad-root" else "5" * 64,
                semantic_id="1" * 64, foundation_id="2" * 64, implementation_id="3" * 64,
                store_id="4" * 64, bindings=dict(bindings), missing_names=[],
                snapshot_integrity="NOT_CHECKED", context_readiness="NOT_ASSERTED",
                mathematical_acceptance=False, binding_count=2,
                coverage="COMPLETE_RECORDED_BINDINGS_AT_SELECTED_ROOT",
                owner_closure="FAILED" if mode == "bad-closure" else "CLOSED")
        def build(actual_bindings, target, actual_metadata, **kwargs):
            need(events[-1] == "profile" and "snapshot-closed" in events and
                 actual_bindings == bindings and actual_metadata["name_codec_sha256"] == codec_pin and
                 actual_metadata["source_profile_sha256"] == "6" * 64 and
                 actual_metadata["context_root"] == "5" * 64, "CLOSE_PIN_METADATA_BEFORE_BUILD")
            events.append("build")
            return D.build(actual_bindings, target, actual_metadata, **kwargs)
        args = arguments(directory_export="v1", context_root="5" * 64,
                         catalog=str(catalog), store_id="4" * 64, output=str(destination))
        with ExitStack() as stack:
            stack.enter_context(patch.object(Q, "bootstrap_owner", return_value=base))
            stack.enter_context(patch.object(Q, "load_advisory_context", return_value=NS(snapshot=snapshot)))
            stack.enter_context(patch.object(Q, "load_directory_index", return_value=NS(build=build)))
            stack.enter_context(patch.object(A, "__file__", str(source_root / "support/discovery/authenticated_index.py")))
            stack.enter_context(patch.object(F, "__file__", str(source_root / "support/discovery/formal_features.py")))
            stack.enter_context(patch.dict(sys.modules, {"ordinary_evidence": E,
                "discovery.authenticated_index": A, "discovery.formal_features": F}))
            result, raw = Q.run_directory(args)
        need(json.loads(raw)["ok"] == result["ok"] and result["mathematical_acceptance"] is False,
             "CALLER_REPORT")
        if mode == "good":
            need(result["ok"] is True and result["owner_closure"] == "CLOSED" and
                 result["directory_publication"] == "COMPLETE" and
                 events.count("profile") == 2 and (destination / "DIRECTORY.json").is_file(),
                 "CALLER_PUBLICATION_AFTER_REVALIDATION")
        else:
            need(result["ok"] is False and not (destination / "DIRECTORY.json").exists(),
                 "CALLER_FAILED_SEAM_NO_MANIFEST")
            expected = {"bad-closure": "QUERY_DIRECTORY_CONTEXT_BOUNDARY",
                        "bad-root": "QUERY_CONTEXT_IDENTITY",
                        "final-profile-failure": "CONTROL_FINAL_PROFILE_CHANGED"}[mode]
            need(result["error_type"] == "ValueError" and result["error"] == expected,
                 "CALLER_EXACT_CHANGED_SEAM_REFUSAL:" + str(result.get("error")))
            if mode != "final-profile-failure":
                need("build" not in events and not destination.exists() and
                     result["phase"] == "EXPORT_RECORDED_CONTEXT" and
                     result["directory_publication"] == "NOT_ATTEMPTED",
                     "CALLER_REFUSES_BEFORE_BUILD")
            else:
                need(events.count("profile") == 2 and events.count("build") == 1 and
                     result["phase"] == "DIRECTORY_BUILD" and
                     result["directory_publication"] == "UNKNOWN" and
                     result["owner_closure"] == "CLOSED" and
                     (destination / "ENTRIES.bin").is_file() and
                     (destination / "TREE.bin").is_file(), "CALLER_FINAL_GATE_RETAINED_PARTIAL")
    cases.append("actual-export-orchestration-codec-role-closed-context-and-final-profile-gate")
    return cases


def load_module(module_name, path, expected, pins):
    path = Path(path)
    need(path.is_absolute(), "ABSOLUTE_SOURCE")
    raw = path.read_bytes()
    need(0 < len(raw) <= 2 * 1024**2 and sha(raw) == expected,
         "SOURCE_PIN:" + str(path))
    need(module_name not in sys.modules, "MODULE_COLLISION")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    pins[str(path)] = expected
    return module


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for field in ("candidate", "evidence", "features", "auth", "query", "advisory"):
        parser.add_argument("--" + field, required=True)
        parser.add_argument("--" + field + "-sha256", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_PYTHON")
    output = Path(args.output)
    need(output.is_absolute() and output.parent.is_dir() and not output.exists() and
         output.resolve().is_relative_to(ROOT / "experiments/v5-local-checks"), "FRESH_OUTPUT")
    pins = {}
    with ExitStack() as stack:
        for target in ("subprocess.Popen", "socket.create_connection", "socket.socket",
                       "sqlite3.connect", "os.system", "os.startfile"):
            stack.enter_context(patch(target, forbidden))
        package_name = "_directory_control_discovery"
        need(package_name not in sys.modules, "PACKAGE_COLLISION")
        package = ModuleType(package_name)
        package.__path__ = []
        sys.modules[package_name] = package
        E = load_module("_directory_control_evidence", args.evidence, args.evidence_sha256, pins)
        F = load_module(package_name + ".formal_features", args.features, args.features_sha256, pins)
        A = load_module(package_name + ".authenticated_index", args.auth, args.auth_sha256, pins)
        D = load_module("_directory_control_candidate", args.candidate, args.candidate_sha256, pins)
        Q = load_module("_directory_control_query", args.query, args.query_sha256, pins)
        H = load_module("_directory_control_advisory", args.advisory, args.advisory_sha256, pins)
        output.mkdir()
        cases = controls(D, E, A, F, output, args.evidence_sha256)
        cases += caller_controls(D, E, A, F, Q, H, output, args.evidence_sha256)
    for path, expected in pins.items():
        need(sha(Path(path).read_bytes()) == expected, "SOURCE_CHANGED")
    check()
    result = dict(status="PASS_HISTORICAL_DIRECTORY_CONTROLS", groups=len(cases),
                  cases=cases, source_pins=pins, mathematical_acceptance=False,
                  scope="SYNTHETIC_FILES_REAL_CODEC_AND_VECTOR_NO_OWNER_NATIVE_NETWORK",
                  wall_seconds=time.monotonic() - START, cpu_seconds=time.process_time() - CPU)
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"),
                     allow_nan=False).encode("utf-8")
    with (output / "RESULT.json").open("xb") as stream:
        stream.write(raw)
    print(raw.decode("utf-8"), flush=True)


if __name__ == "__main__":
    main()

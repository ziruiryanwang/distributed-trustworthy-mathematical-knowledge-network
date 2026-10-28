"""Prepare advisory whole-type-pattern specs from a pinned raw type, offline.

Only selected inert codecs, index helpers and the fixed inventory are loaded.
No owner, native installation, proof, project, network or runtime is opened.
The approved entrypoint/package, Python and protected files are trust premises.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import time
import types

MIB = 1024 ** 2
MODE = "type-pattern-v1"
# Dependency order is explicit; no product path is put on sys.path.
SOURCES = (
    ("ordinary_evidence", "installation/py/ordinary_evidence.py", "evidence"),
    ("ordinary_semantics", "installation/py/ordinary_semantics.py", "semantics"),
    ("portable_evidence", "installation/py/portable_evidence.py", "portable_evidence"),
    ("ordinary_preview", "authoring/py/ordinary_preview.py", None),
    ("portable_preview", "authoring/py/portable_preview.py", None),
    ("formal_query", "authoring/py/formal_query.py", None),
    ("ordinary_type_pattern", "authoring/py/ordinary_type_pattern.py", None),
    ("discovery.formal_features", "support/discovery/formal_features.py", None),
    ("discovery.ordinary_export_adapter", "support/discovery/ordinary_export_adapter.py", None),
)


def need(ok, code):
    if not ok:
        raise ValueError("PATTERN_QUERY_" + code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and ".." not in path.parts, "ABSOLUTE_PATH")
    for part in (*reversed(path.parents), path):
        if fresh and part == path:
            need(not os.path.lexists(part), "FRESH_OUTPUT")
            continue
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and
             not getattr(info, "st_file_attributes", 0) & 0x400, "REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if part != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PATH_KIND")
    need(path.resolve(strict=not fresh) == path, "CANONICAL_PATH")
    return path


def read(path, maximum):
    path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    need(len(raw) == size, "READ_CHANGED")
    return raw


def pinned(path, pin, maximum=2*MIB):
    need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
         type(pin["bytes"]) is int, "PIN_FIELDS")
    raw = read(path, maximum)
    need(len(raw) == pin["bytes"] and digest(raw) == pin["sha256"], "SOURCE_PIN")
    return raw


@contextmanager
def modules(package, profile, manifest, check):
    captured = []
    for name, relative, core_role in SOURCES:
        check()
        if core_role is None:
            pin = profile["files"].get(relative)
        else:
            logical = relative.removeprefix("installation/")
            need(manifest["roles"].get(core_role) == logical, "CORE_ROLE")
            pin = manifest["files"].get(logical)
        captured.append((name, package/relative, pinned(package/relative, pin)))
    names = ["discovery", *[name for name, _, _ in captured]]
    need(not any(name == base or name.startswith(base + ".") for name in sys.modules
                 for base in names), "PRELOADED_MODULE")
    loaded = {}
    try:
        namespace = types.ModuleType("discovery")
        namespace.__path__ = []
        sys.modules["discovery"] = namespace
        for name, path, raw in captured:
            check()
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
            loaded[name] = module
        yield loaded
    finally:
        for name in reversed(names):
            sys.modules.pop(name, None)


def prepare(args):
    started, cpu = time.monotonic(), time.process_time()
    need(args.input_kind in ("native-type", "preview"), "INPUT_KIND")
    def check():
        need(time.monotonic()-started < 30 and time.process_time()-cpu < 20, "ALLOWANCE")
    package = ordinary(Path(__file__).absolute().parent, directory=True)
    source = ordinary(args.input)
    output = ordinary(args.output, directory=True, fresh=True)
    for path in (package, source):
        need(not output.is_relative_to(path) and not path.is_relative_to(output), "OUTPUT_OVERLAP")
    profile_raw = read(package/"PROFILE.json", 2*MIB)
    need(digest(profile_raw) == args.profile_sha256, "PROFILE_PIN")
    # JSON below comes only from explicitly approved hash-pinned local metadata.
    # Untrusted query bytes instead pass through the bounded original DAG codec.
    profile = json.loads(profile_raw)
    need(type(profile) is dict and profile.get("schema") == "DMKN_ORDINARY_OWNER_PROFILE_V1"
         and type(profile.get("files")) is dict, "PROFILE_SCHEMA")
    pinned(package/"pattern_query.py", profile["files"].get("pattern_query.py"))
    manifest_raw = read(package/"installation/INSTALLATION.json", 2*MIB)
    need(digest(manifest_raw) == profile.get("installation_manifest_sha256"), "INSTALLATION_PIN")
    manifest = json.loads(manifest_raw)
    need(type(manifest) is dict and type(manifest.get("files")) is dict and
         type(manifest.get("roles")) is dict, "INSTALLATION_SCHEMA")
    inventory = pinned(package/"installation/foundation/inventory.json",
                       manifest["files"].get("foundation/inventory.json"), MIB)
    source_raw = read(source, MIB)
    need(digest(source_raw) == args.input_sha256, "INPUT_PIN")
    with modules(package, profile, manifest, check) as loaded:
        E, S = loaded["ordinary_evidence"], loaded["ordinary_semantics"]
        P = loaded["ordinary_type_pattern"]
        D = loaded["discovery.ordinary_export_adapter"]
        check()
        derive = P.native_pattern if args.input_kind == "native-type" else P.preview_pattern
        result = derive(source_raw, inventory)
        namespace = D.namespace_for(S.semantic_id(), discovery_profile=MODE)
        specs = [result["spec"]]
        features = D.compile_query(namespace, specs, discovery_profile=MODE)
        report = dict(schema="DMKN_ORDINARY_PATTERN_QUERY_V1", operation="prepare-pattern-query",
            status="PATTERN_QUERY_READY", profile_sha256=args.profile_sha256,
            semantic_id=S.semantic_id(), foundation_id=S.foundation_id(),
            discovery_profile=MODE, namespace=namespace, pattern_profile_id=P.PROFILE_ID,
            input_kind=args.input_kind, input_sha256=digest(source_raw), input_bytes=len(source_raw),
            inventory_sha256=digest(inventory), specs=specs, features=features,
            extraction_counters=result["counters"], extraction_work=result["work"],
            mathematical_acceptance=False, owner_opened=False, native_opened=False,
            assurance="ADVISORY_WHOLE_TYPE_VARIANT_NOT_SEMANTIC_EQUIVALENCE_OR_PROOF",
            next="Find with explicit type-pattern-v1 and specs; inspect and check selected evidence",
            cost=dict(wall_seconds=time.monotonic()-started, cpu_seconds=time.process_time()-cpu,
                      scope="COOPERATIVE_30_WALL_20_CPU_SECONDS"))
        check()
        need(read(package/"PROFILE.json", 2*MIB) == profile_raw and
             read(source, MIB) == source_raw, "SELECTED_INPUT_CHANGED")
        report_raw, specs_raw = E.canonical_json(report), E.canonical_json(specs)
        need(len(report_raw) <= MIB and len(specs_raw) <= MIB, "OUTPUT_BOUND")
        output.mkdir()
        # RESULT is written last; a partial directory is not a completed query.
        with (output/"SPECS.json").open("xb") as stream:
            stream.write(specs_raw)
        with (output/"RESULT.json").open("xb") as stream:
            stream.write(report_raw)
    return report


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_PYTHON")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for option in ("profile-sha256", "input", "input-sha256", "output"):
        parser.add_argument("--" + option, required=True)
    parser.add_argument("--input-kind", required=True, choices=("native-type", "preview"))
    print(json.dumps(prepare(parser.parse_args()), sort_keys=True, ensure_ascii=True,
                     allow_nan=False))


if __name__ == "__main__":
    main()

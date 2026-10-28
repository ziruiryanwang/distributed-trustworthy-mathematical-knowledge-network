"""Resolve exact names from one approved historical directory, entirely offline.

No owner, Lean worker, service, proof, or corpus scan is opened. The manifest
selection must come from an approved complete exporter, not a foreign assertion.
Use returned specs as explicit advisory inputs to the existing find preparer.
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

MIB = 1024**2
CODECS = (
    ("ordinary_evidence", "installation/py/ordinary_evidence.py", "fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6"),
    ("ordinary_semantics", "installation/py/ordinary_semantics.py", "ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915"),
    ("discovery.formal_features", "support/discovery/formal_features.py", "f1f53ee40ce32126085f7f776c47d9d0ab2c5b7c679d40f018f6bff70f6430e5"),
    ("discovery.authenticated_index", "support/discovery/authenticated_index.py", "77a12cda9dd4a303153b59d00998de8aa6bf08bb572af10136e21dfa9c96cc95"),
)


def need(condition, code):
    if not condition:
        raise ValueError("DIRECTORY_LOOKUP_" + code)


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and ".." not in path.parts, "ABSOLUTE_PATH")
    for part in (*reversed(path.parents), path):
        if fresh and part == path:
            need(not part.exists() and not part.is_symlink(), "FRESH_OUTPUT")
            continue
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and
             not getattr(info, "st_file_attributes", 0) & 0x400, "REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if part != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PATH_KIND")
    need(path.resolve(strict=not fresh) == path, "CANONICAL_PATH")
    return path


def read(path, cap):
    path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= cap, "READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(cap+1)
    need(len(raw) == size, "READ_CHANGED")
    return raw


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "JSON_DUPLICATE")
            result[key] = value
        return result
    def reject(_):
        raise ValueError("DIRECTORY_LOOKUP_JSON_NUMBER")
    return json.loads(raw, object_pairs_hook=pairs, parse_float=reject, parse_constant=reject)


@contextmanager
def modules(package, profile, check):
    sources = []
    for name, relative, pin in CODECS:
        check(); raw = read(package/relative, 2*MIB)
        need(digest(raw) == pin, "CODEC_PIN:" + name)
        sources.append((name, package/relative, raw))
    pin = profile["files"].get("directory_index.py")
    need(type(pin) is dict and set(pin) == {"bytes", "sha256"}, "INDEX_ROLE")
    raw = read(package/"directory_index.py", MIB)
    need(type(pin["bytes"]) is int and len(raw) == pin["bytes"] and
         digest(raw) == pin["sha256"], "INDEX_PIN")
    sources.append(("_offline_name_directory", package/"directory_index.py", raw))
    sentinel = object()
    names = ["discovery", *[name for name, _, _ in sources]]
    previous = {name: sys.modules.get(name, sentinel) for name in names}
    loaded = {}
    try:
        namespace = types.ModuleType("discovery")
        namespace.__path__ = []
        sys.modules["discovery"] = namespace
        for name, path, raw in sources:
            check()
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
            loaded[name] = module
        yield loaded
    finally:
        for name, old in previous.items():
            if old is sentinel:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old


def lookup(args):
    started, cpu = time.monotonic(), time.process_time()
    def check():
        need(time.monotonic()-started < 30 and time.process_time()-cpu < 20, "ALLOWANCE")
    package = ordinary(Path(__file__).absolute().parent, directory=True)
    directory = ordinary(args.directory, directory=True)
    names_path = ordinary(args.symbol_names)
    output = ordinary(args.output, directory=True, fresh=True)
    for source in (package, directory, names_path):
        need(not output.is_relative_to(source) and not source.is_relative_to(output), "OUTPUT_OVERLAP")
    need(not directory.is_relative_to(package) and not package.is_relative_to(directory), "DIRECTORY_PACKAGE_OVERLAP")
    profile_raw = read(package/"PROFILE.json", 2*MIB)
    need(digest(profile_raw) == args.profile_sha256, "PROFILE_PIN")
    profile = strict(profile_raw)
    need(type(profile) is dict and profile.get("schema") == "DMKN_ORDINARY_OWNER_PROFILE_V1"
         and type(profile.get("files")) is dict, "PROFILE_SCHEMA")
    own = read(package/"lookup_directory.py", MIB)
    need(profile["files"].get("lookup_directory.py") == {"bytes": len(own), "sha256": digest(own)}, "ENTRY_PIN")
    manifest = read(directory/"DIRECTORY.json", 8192)
    names_raw = read(names_path, 65536)
    with modules(package, profile, check) as loaded:
        E, S = loaded["ordinary_evidence"], loaded["ordinary_semantics"]
        D, A = loaded["_offline_name_directory"], loaded["discovery.authenticated_index"]
        doc = D.descriptor_checked(manifest, args.directory_sha256, evidence=E, auth=A)
        need(doc["metadata"]["semantic_id"] == S.semantic_id() and
             doc["metadata"]["foundation_id"] == S.foundation_id() and
             doc["metadata"]["name_codec_sha256"] == CODECS[0][2], "DIRECTORY_SEMANTICS")
        names = E.strict_json(names_raw, E.Limits(max_bytes=65536))
        entry_path, tree_path = ordinary(directory/"ENTRIES.bin"), ordinary(directory/"TREE.bin")
        need(entry_path.stat().st_size == doc["entries_bytes"] and
             tree_path.stat().st_size == doc["tree_bytes"], "DIRECTORY_FILE_SIZES")
        with entry_path.open("rb") as entries, tree_path.open("rb") as tree:
            def selected_read(stream, maximum):
                def take(offset, count):
                    need(type(offset) is int and type(count) is int and
                         0 <= offset <= maximum and 0 <= count <= maximum-offset, "READ_RANGE")
                    stream.seek(offset)
                    return stream.read(count)
                return take
            result = D.lookup_open(manifest, args.directory_sha256,
                selected_read(entries, doc["entries_bytes"]), selected_read(tree, doc["tree_bytes"]),
                names, evidence=E, auth=A, check=check)
        check()
        need(read(directory/"DIRECTORY.json", 8192) == manifest and
             read(names_path, 65536) == names_raw and
             read(package/"PROFILE.json", 2*MIB) == profile_raw, "SELECTED_INPUT_CHANGED")
        result.update(operation="lookup-name-directory", profile_sha256=args.profile_sha256,
            symbol_names_sha256=digest(names_raw), mathematical_acceptance=False,
            acceptance_rule="ORDINARY_RECIPIENT_CHECKING_UNCHANGED",
            next="Use specs as explicit find inputs; not as a current-owner query report",
            cost={"wall_seconds": time.monotonic()-started,
                  "cpu_seconds": time.process_time()-cpu,
                  "limits": "COOPERATIVE_30_WALL_20_CPU_SECONDS"})
        raw = E.canonical_json(result)
        need(len(raw) <= MIB, "OUTPUT_BOUND")
        check(); output.mkdir()
        with (output/"RESULT.json").open("xb") as stream:
            stream.write(raw)
        if "specs" in result:
            with (output/"SPECS.json").open("xb") as stream:
                stream.write(E.canonical_json(result["specs"]))
    return result


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_PYTHON")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("profile-sha256", "directory", "directory-sha256", "symbol-names", "output"):
        parser.add_argument("--"+name, required=True)
    result = lookup(parser.parse_args())
    print(json.dumps(result, sort_keys=True, ensure_ascii=True, allow_nan=False))


if __name__ == "__main__":
    main()

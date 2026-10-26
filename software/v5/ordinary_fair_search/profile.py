"""Ordinary Lean-first package loader with optional inert baseline interchange.

Preserve the selected preview installation, native helpers and ordinary APIs.
Only baseline production/intake are added. The logical reference/ directory
contains two inert/baseline controllers, not original-library reference support;
no reference matcher, registration, authoring or separate helper profile loads.

The entrypoint/Python/OS and immutable owner-controlled storage are premises.
All auxiliary payloads and installed core Python are pinned before import;
the unchanged NativeInstallation.open verifies remaining installed support.
Runtime pins are selected support, not a hermetic toolchain attestation.
The changed owner/loader imply a new anchor-support identity, not migration.
"""
from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import math
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import time
from types import SimpleNamespace

MIB = 1024**2
SCHEMA = "DMKN_ORDINARY_OWNER_PROFILE_V1"
CORE = {"core": "ordinary_admission", "evidence": "ordinary_evidence",
        "semantics": "ordinary_semantics", "portable_evidence": "portable_evidence",
        "catalog": "portable_catalog", "legacy_catalog": "local_catalog"}
AUTHOR = ("ordinary_contribution", "portable_owner_request", "owner_request",
          "portable_candidate", "portable_preview", "ordinary_preview",
          "library_completion", "completion_api", "retained_preparation",
          "supervised_library_exchange", "library_extraction", "module_closure", "anchor_store", "module_export", "formal_query",
          "baseline_production")
SUPPORT = ("transport/ordinary_acquisition.py", "transport/http_provider.py",
           "transport/authoring_offers.py",
           "transport/clients.py", "transport/fair_exchange.py",
           "discovery/fair_search.py", "discovery/formal_features.py",
           "discovery/discovery_store.py", "discovery/authenticated_index.py",
           "discovery/summary_wire.py", "custody/module_store.py",
           "discovery/ordinary_export_adapter.py", "discovery/search_session.py",
           "discovery/discovery_query.py", "discovery/candidate_query.py")
NATIVE = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport",
          "OwnerRebind", "OwnerConstruction", "OwnerUseCommand", "OrdinaryExport",
          "SuccessorExport", "SuccessorExportCommand", "PortableOwnerConstructCommand",
          "PortableConstructExportCommand", "PortableContributionExportCommand", "OwnerQueryCommand")
SUFFIXES = (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")
BASELINE = ("baseline_bundle", "baseline_intake")


def need(condition, code):
    if not condition:
        raise ValueError(code)


def hexid(value):
    need(type(value) is str and len(value) == 64 and
         all(c in "0123456789abcdef" for c in value), "OWNER_PROFILE_HEX")
    return value


def ordinary(value, *, directory=False):
    path = Path(value)
    need(path.is_absolute() and ".." not in path.parts and len(path.parts) <= 128 and
         len(str(path)) <= 32768, "OWNER_PROFILE_ABSOLUTE_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             (getattr(info, "st_file_attributes", 0) & 0x400), "OWNER_PROFILE_REDIRECTED_PATH")
        if part != path or directory:
            need(stat.S_ISDIR(info.st_mode), "OWNER_PROFILE_DIRECTORY")
        else:
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "OWNER_PROFILE_SINGLE_FILE")
    return path


def relative(value):
    need(type(value) is str and 0 < len(value) <= 1024 and "\\" not in value,
         "OWNER_PROFILE_RELATIVE_PATH")
    path = PurePosixPath(value)
    need(path.parts and not path.is_absolute() and path.as_posix() == value and
         all(part not in (".", "..") and not part.endswith((".", " ")) and
             not any(ord(c) < 32 or c in ':*?"<>|' for c in part) and
             not os.path.isreserved(part) for part in path.parts), "OWNER_PROFILE_RELATIVE_PATH")
    return path


def bounded(path, maximum):
    path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "OWNER_PROFILE_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size, "OWNER_PROFILE_READ_CHANGED")
    return raw


def owner_json(raw, maximum=2*MIB):
    need(type(raw) is bytes and 0 < len(raw) <= maximum, "OWNER_PROFILE_JSON_BOUND")
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "OWNER_PROFILE_JSON_DUPLICATE")
            result[key] = value
        return result
    def reject(_):
        raise ValueError("OWNER_PROFILE_JSON_NUMBER")
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                          parse_float=reject, parse_constant=reject)
    except (RecursionError, UnicodeError) as error:
        raise ValueError("OWNER_PROFILE_JSON_SYNTAX") from error


def check_pin(path, pin, check):
    need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
         type(pin["bytes"]) is int and 0 < pin["bytes"] <= 128*MIB,
         "OWNER_PROFILE_FILE_PIN")
    hexid(pin["sha256"])
    path = ordinary(path)
    check()
    need(path.stat().st_size == pin["bytes"], "OWNER_PROFILE_FILE_SIZE")
    digest, size = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            check(); size += len(block)
            need(size <= pin["bytes"], "OWNER_PROFILE_FILE_GREW")
            digest.update(block)
    need(size == pin["bytes"] and path.stat().st_size == size and
         digest.hexdigest() == pin["sha256"], "OWNER_PROFILE_FILE_CHANGED")
    return (path, size, pin["sha256"])


def census(root, names, check):
    """No unselected code/bytecode on any package Python/Lean search path."""
    actual, pending, entries = set(), [(ordinary(root, directory=True), 0)], 0
    while pending:
        directory, depth = pending.pop()
        check()
        with os.scandir(directory) as listing:
            for entry in listing:
                check(); entries += 1
                need(entries <= 4096, "OWNER_PROFILE_CENSUS_BOUND")
                path = Path(entry.path)
                if entry.is_dir(follow_symlinks=False):
                    need(depth < 8, "OWNER_PROFILE_CENSUS_DEPTH")
                    pending.append((ordinary(path, directory=True), depth+1))
                else:
                    actual.add(ordinary(path).relative_to(root).as_posix())
    need(actual == set(names), "OWNER_PROFILE_EXACT_CENSUS")


def load(package_root, expected_profile_sha256, runtime_roots, deadline, *, check_parent):
    """Open selected installed support; never open/create mathematical state."""
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "OWNER_PROFILE_PYTHON")
    need(type(deadline) in (int, float) and math.isfinite(deadline) and
         callable(check_parent), "OWNER_PROFILE_DEADLINE")
    def check():
        check_parent()
        need(time.monotonic() < deadline, "OWNER_PROFILE_DEADLINE")
    check()
    root = ordinary(package_root, directory=True)
    raw = bounded(root/"PROFILE.json", 2*MIB)
    need(hashlib.sha256(raw).hexdigest() == hexid(expected_profile_sha256), "OWNER_PROFILE_PIN")
    doc = owner_json(raw)
    need(type(doc) is dict and set(doc) == {"schema", "installation_manifest_sha256",
         "helper_paths", "author_worker", "files"} and doc["schema"] == SCHEMA,
         "OWNER_PROFILE_FIELDS")
    need(doc["helper_paths"] == ["authoring/helpers"] and doc["author_worker"] == "author_worker.py",
         "OWNER_PROFILE_LAYOUT")
    files = doc["files"]
    need(type(files) is dict and 1 <= len(files) <= 512 and
         len({name.casefold() for name in files}) == len(files), "OWNER_PROFILE_FILE_CENSUS")
    required = {"owner.py", "profile.py", "author_worker.py", "peer.py", "peer_api.py", "query.py", "run.py"} | {
        "authoring/py/"+name+".py" for name in AUTHOR} | {"support/"+name for name in SUPPORT}
    required.update(("authoring/bin/MissingImportExporter.exe",
                     "module_worker.py", "module/OrdinaryModule.lean",
                     "authoring/py/baseline_worker.py", "authoring/bin/BaselineExporter.exe"))
    required.update("reference/"+name+".py" for name in BASELINE)
    native_allowed = {"authoring/helpers/"+name+suffix for name in NATIVE for suffix in SUFFIXES}
    native_required = {"authoring/helpers/"+name+".olean" for name in NATIVE}
    need(required | native_required <= set(files) <= required | native_allowed,
         "OWNER_PROFILE_PAYLOAD_SET")
    pins, total = [], 0
    for name, pin in files.items():
        check()
        path = root.joinpath(*relative(name).parts)
        selected = check_pin(path, pin, check)
        pins.append(selected); total += selected[1]
        need(total <= 512*MIB, "OWNER_PROFILE_TOTAL_BOUND")
    for directory in ("authoring/helpers", "authoring/py", "authoring/bin", "support", "module", "reference"):
        census(root/directory, (name[len(directory)+1:] for name in files
               if name.startswith(directory+"/")), check)
    need(Path(__file__).absolute() == root/"profile.py", "OWNER_PROFILE_RUNNING_LOADER")

    installed = ordinary(root/"installation", directory=True)
    manifest_raw = bounded(installed/"INSTALLATION.json", 2*MIB)
    manifest_sha = hexid(doc["installation_manifest_sha256"])
    need(hashlib.sha256(manifest_raw).hexdigest() == manifest_sha, "OWNER_PROFILE_INSTALLATION_PIN")
    manifest = owner_json(manifest_raw)
    need(type(manifest) is dict and type(manifest.get("roles")) is dict and
         type(manifest.get("files")) is dict, "OWNER_PROFILE_INSTALLATION_BOOTSTRAP")
    for role, name in CORE.items():
        logical = "py/"+name+".py"
        need(manifest["roles"].get(role) == logical and logical in manifest["files"],
             "OWNER_PROFILE_CORE_LAYOUT")
        check_pin(installed/logical, manifest["files"][logical], check)
    census(installed/"py", (name+".py" for name in CORE.values()), check)
    loaded_names = (*CORE.values(), *AUTHOR, *BASELINE, "transport", "discovery", "custody", "peer_api")
    need(not any(name == base or name.startswith(base+".") for name in sys.modules
                 for base in loaded_names), "OWNER_PROFILE_PRELOADED_MODULE")
    sys.path[:0] = [str(installed/"py"), str(root/"authoring/py"), str(root/"support"), str(root/"reference")]
    A = importlib.import_module("ordinary_admission")
    # The unchanged installation verifier checks every remaining payload, all
    # named runtime attachments, the actual running core and supervisor binding.
    installation = A.NativeInstallation.open(installed, manifest_raw, manifest_sha,
        runtime_roots={key: Path(value) for key, value in runtime_roots.items()})
    check()
    need(A.E.strict_json(raw, A.E.Limits(max_bytes=2*MIB)) == doc, "OWNER_PROFILE_CANONICAL_JSON")
    G = importlib.import_module("ordinary_contribution")
    O = importlib.import_module("transport.ordinary_acquisition")
    for name in AUTHOR:
        module = importlib.import_module(name)
        need(Path(module.__file__).absolute() == root/"authoring/py"/(name+".py"),
             "OWNER_PROFILE_LOADED_HELPER")
    for path in SUPPORT:
        name = path[:-3].replace("/", ".")
        module = importlib.import_module(name)
        need(Path(module.__file__).absolute() == root/"support"/path,
             "OWNER_PROFILE_LOADED_SUPPORT")
    for name in BASELINE:
        module = importlib.import_module(name)
        need(Path(module.__file__).absolute() == root/"reference"/(name+".py"),
             "OWNER_PROFILE_LOADED_BASELINE")
    profile = G.AuthoringProfile(installation_manifest_sha256=manifest_sha,
        helper_paths=(root/"authoring/helpers",), author_worker_script=root/"author_worker.py",
        file_pins=tuple(pins))
    profile.verify(check)
    # Root scripts are not on sys.path. Execute only the just-verified exact
    # coordinator bytes, then require its shared core identity at the caller.
    peer_path = root/"peer_api.py"
    peer_raw = bounded(peer_path, 2*MIB)
    need(hashlib.sha256(peer_raw).hexdigest() == files["peer_api.py"]["sha256"],
         "OWNER_PROFILE_PEER_API_CHANGED")
    spec = importlib.util.spec_from_file_location("peer_api", peer_path)
    peer = importlib.util.module_from_spec(spec)
    sys.modules["peer_api"] = peer
    try:
        exec(compile(peer_raw, str(peer_path), "exec"), peer.__dict__)
    except BaseException:
        del sys.modules["peer_api"]
        raise
    check()
    return SimpleNamespace(root=root, descriptor=doc, installation=installation,
                           profile=profile, A=A, G=G, O=O, peer_api=peer,
                           baseline_intake=sys.modules["baseline_intake"],
                           baseline_production=sys.modules["baseline_production"],
                           completion_api=sys.modules["completion_api"],
                           library_extraction=sys.modules["library_extraction"],
                           module_export=sys.modules["module_export"],
                           formal_query=sys.modules["formal_query"])

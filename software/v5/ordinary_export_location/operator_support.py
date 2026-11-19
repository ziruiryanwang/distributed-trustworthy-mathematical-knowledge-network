"""Captured support for the optional export-location operator; no mathematical warrant.

The operator selects SOURCES.json by an external SHA-256. The closed role set
contains no owner/admission loader, native installation, seed or executable basis.
Protected approved software, Python/stdlib and Windows remain trust premises.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import stat
import sys
from types import MappingProxyType, ModuleType

MIB = 1024**2
PROFILE_SCHEMA = "DMKN_ORDINARY_EXPORT_OPERATOR_SOURCES_V1"
ORDER = (
    "ordinary_evidence", "ordinary_semantics", "portable_evidence", "portable_candidate",
    "ordinary_preview", "portable_preview", "formal_query", "baseline_bundle",
    "discovery.formal_features", "discovery.authenticated_index", "discovery.pair_access",
    "discovery.discovery_store", "discovery.discovery_query", "discovery.candidate_query",
    "discovery.summary_wire", "discovery.ordinary_export_adapter", "custody.module_store",
    "transport.http_provider", "transport.clients", "transport.ordinary_acquisition",
    "transport.authoring_offers", "transport.contact_directory",
    "transport.fair_exchange", "transport.ordinary_location_controller",
    "transport.ordinary_location_gateway", "advertisement_delta")
PACKAGES = ("discovery", "transport", "custody")
PATHS = {name: "support/" + name.replace(".", "/") + ".py" for name in ORDER}
PATHS.update({"_entry": "run.py", "_support": "operator_support.py", "_core": "operator.py",
              "_supervisor": "supervisor/commons.py", "domains": "supervisor/domains.py",
              "_job": "supervisor/run_stage.py"})
ALIASES = {"E": "ordinary_evidence", "S": "ordinary_semantics", "PE": "portable_evidence",
    "B": "baseline_bundle", "PP": "portable_preview", "O": "transport.ordinary_acquisition",
    "DS": "discovery.discovery_store", "OA": "discovery.ordinary_export_adapter",
    "H": "transport.http_provider", "F": "discovery.formal_features",
    "C": "discovery.candidate_query", "Q": "discovery.discovery_query",
    "W": "discovery.summary_wire", "D": "discovery.discovery_store",
    "X": "transport.fair_exchange", "L": "transport.ordinary_location_controller",
    "G": "transport.ordinary_location_gateway", "Delta": "advertisement_delta"}
NODE_FILES = ("protocol.mjs", "intent.mjs", "maintained_roles.mjs", "ipc_wire.mjs",
    "node_entry.mjs", "runtime.mjs", "framing.mjs", "transport.mjs",
    "role_composition.mjs", "services_composition.mjs")
PATHS.update({"node/"+name: "node/"+name for name in NODE_FILES})
PYTHON_FILES = {"python.exe", "python314.dll", "python3.dll"}
_CONSTRUCTION = object()


def need(condition, code):
    if not condition:
        raise ValueError("EXPORT_OPERATOR_SUPPORT_" + code)


def hexid(value):
    need(type(value) is str and len(value) == 64 and
         all(c in "0123456789abcdef" for c in value), "SHA256")
    return value


def fields(value, keys, code):
    need(type(value) is dict and set(value) == set(keys), code)


def uint(value, low, high, code):
    need(type(value) is int and low <= value <= high, code)
    return value


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def strict(raw, *, reports=False):
    """Operational JSON permits booleans; evidence uses its unchanged codec."""
    def pairs(rows):
        value = {}
        for key, item in rows:
            need(key not in value, "DUPLICATE_JSON_KEY")
            value[key] = item
        return value
    def reject(_):
        raise ValueError("EXPORT_OPERATOR_SUPPORT_JSON_NUMBER")
    def decimal(value):
        result = float(value)
        need(math.isfinite(result), "REPORT_NUMBER")
        return result
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
        parse_float=decimal if reports else reject, parse_constant=reject)


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                      separators=(",", ":")).encode("ascii")


def ordinary(value, *, directory=False, fresh=False):
    """Current launcher's local nonredirected path policy, without owner imports."""
    path = Path(value)
    need(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":" and
         path != Path(path.anchor) and len(path.parts) <= 128 and len(str(path)) <= 32767,
         "ABSOLUTE_NONROOT_PATH")
    need(all(part not in (".", "..") and not part.endswith((".", " ")) and
         not os.path.isreserved(part) and not any(ord(c) < 32 or c in ':*?"<>|' for c in part)
         for part in path.parts[1:]), "PATH_COMPONENT")
    for ancestor in reversed(path.parents):
        info = ancestor.lstat()
        need(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode) and
             not getattr(info, "st_file_attributes", 0) & 0x400, "PATH_ANCESTRY")
    if fresh:
        need(not path.exists() and not path.is_symlink(), "FRESH_PATH")
    else:
        info = path.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PATH_KIND")
    need(path.resolve(strict=not fresh) == path, "CANONICAL_PATH")
    return path


def overlap(left, right):
    return left.is_relative_to(right) or right.is_relative_to(left)


def separated(paths, code):
    for position, left in enumerate(paths):
        for right in paths[position+1:]:
            need(not overlap(left, right), code)


def reject_dedicated(path):
    for parent in (path, *path.parents):
        try:
            (parent / "DMKN-DEDICATED-HOST.json").lstat()
        except FileNotFoundError:
            continue
        need(False, "DEDICATED_HOST_PATH")


def read(path, maximum, check):
    path = ordinary(path)
    uint(maximum, 1, 128*MIB, "READ_LIMIT")
    check()
    size = path.stat().st_size
    need(0 < size <= maximum, "FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    check()
    need(len(raw) == size and path.stat().st_size == size, "FILE_CHANGED")
    return raw


def write_fresh(path, raw, check):
    need(type(raw) is bytes and 0 < len(raw) <= 16*MIB, "WRITE_BOUND")
    path = ordinary(path, fresh=True)
    check()
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "SHORT_WRITE")
        stream.flush()
        os.fsync(stream.fileno())
    need(read(path, len(raw), check) == raw, "WRITE_READBACK")


def bound_file(path, size, expected, check, *, capture=False):
    uint(size, 1, (2 if capture else 128)*MIB, "PIN_SIZE")
    hexid(expected)
    path = ordinary(path)
    need(path.stat().st_size == size, "PIN_SIZE_CHANGED")
    hashed, actual, chunks = hashlib.sha256(), 0, []
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            check()
            actual += len(block)
            need(actual <= size, "PIN_GREW")
            hashed.update(block)
            if capture:
                chunks.append(block)
    check()
    need(actual == size and path.stat().st_size == actual and hashed.hexdigest() == expected,
         "PIN_CHANGED")
    return b"".join(chunks) if capture else None


def load_source(name, path, raw):
    need(name not in sys.modules, "PRELOADED_MODULE:" + name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    if "." in name:
        parent, child = name.rsplit(".", 1)
        setattr(sys.modules[parent], child, module)
    return module


@dataclass(frozen=True)
class BoundProfile:
    root: Path
    python_root: Path
    profile_sha256: str
    manifest_raw: bytes
    paths: object
    raws: object
    python_pins: tuple

    def verify(self, check):
        need(read(self.root / "SOURCES.json", 2*MIB, check) == self.manifest_raw,
             "PROFILE_CHANGED")
        for name, raw in self.raws.items():
            need(read(self.paths[name], 2*MIB, check) == raw, "SOURCE_CHANGED:" + name)
        for filename, size, sha256 in self.python_pins:
            bound_file(self.python_root / filename, size, sha256, check)
        check()


def bind(root, expected_profile, python_root, check):
    need(callable(check), "BUDGET_CALLBACK")
    check()
    root = ordinary(root, directory=True)
    python_root = ordinary(python_root, directory=True)
    need(not overlap(root, python_root), "RUNTIME_SOFTWARE_OVERLAP")
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and sys.maxsize > 2**32 and
         sys.byteorder == "little" and sys.version_info[:3] == (3, 14, 6), "PYTHON_PROFILE")
    need(ordinary(Path(sys.executable)) == python_root / "python.exe", "RUNNING_PYTHON")
    raw = read(root / "SOURCES.json", 2*MIB, check)
    need(digest(raw) == hexid(expected_profile), "PROFILE_PIN")
    manifest = strict(raw)
    fields(manifest, ("schema", "python", "files"), "PROFILE_FIELDS")
    need(manifest["schema"] == PROFILE_SCHEMA, "PROFILE_SCHEMA")
    fields(manifest["files"], PATHS, "SOURCE_ROLE_SET")
    paths, raws = {}, {}
    for name, relative in PATHS.items():
        pin = manifest["files"][name]
        fields(pin, ("path", "source", "bytes", "sha256"), "SOURCE_PIN_FIELDS")
        need(pin["path"] == relative and type(pin["source"]) is str and
             0 < len(pin["source"]) <= 512, "SOURCE_PATH")
        path = root / relative
        raws[name] = bound_file(path, pin["bytes"], pin["sha256"], check, capture=True)
        paths[name] = path
    python = manifest["python"]
    fields(python, ("version", "files"), "PYTHON_FIELDS")
    need(python["version"] == "3.14.6", "PYTHON_VERSION")
    fields(python["files"], PYTHON_FILES, "PYTHON_ROLE_SET")
    runtime = []
    for filename in sorted(PYTHON_FILES):
        pin = python["files"][filename]
        fields(pin, ("bytes", "sha256"), "PYTHON_PIN_FIELDS")
        bound_file(python_root / filename, pin["bytes"], pin["sha256"], check)
        runtime.append((filename, pin["bytes"], pin["sha256"]))
    return BoundProfile(root, python_root, expected_profile, raw,
                        MappingProxyType(paths), MappingProxyType(raws), tuple(runtime))


@dataclass(frozen=True)
class ExportLocationSupport:
    """Authenticated optional routing role; no admission or native-installation object."""
    root: Path
    python_runtime_root: Path
    profile_sha256: str
    semantic_id: str
    namespace: str
    modules: object
    api: object
    _bound: BoundProfile
    _check: object
    _token: object

    def __post_init__(self):
        need(self._token is _CONSTRUCTION, "LOADER_CONSTRUCTION")

    def __getattr__(self, key):
        if key in ALIASES:
            return self.api[key]
        raise AttributeError(key)

    def verify(self):
        self._bound.verify(self._check)
        need(set(self.modules) == set(ORDER) and
             all(sys.modules.get(name) is module for name, module in self.modules.items()),
             "LOADED_MODULE_IDENTITY")
        need(all(self.api[key] is self.modules[name] for key, name in ALIASES.items()),
             "LOADED_ALIAS_IDENTITY")
        need(self.semantic_id == self.S.semantic_id() and
             self.namespace == self.OA.namespace_for(self.semantic_id), "SEMANTIC_NAMESPACE")
        self._check()

    ordinary = staticmethod(ordinary)
    hexid = staticmethod(hexid)
    fields = staticmethod(fields)
    uint = staticmethod(uint)
    overlap = staticmethod(overlap)

    def read(self, path, maximum):
        return read(path, maximum, self._check)

    def write_fresh(self, path, raw):
        return write_fresh(path, raw, self._check)


def load_support(bound, check):
    need(type(bound) is BoundProfile and callable(check), "BOUND_PROFILE")
    need(not any(name in ORDER or any(name == base or name.startswith(base + ".")
             for base in PACKAGES) for name in sys.modules), "PRELOADED_SUPPORT")
    for name in PACKAGES:
        package = ModuleType(name)
        package.__package__, package.__path__ = name, []
        package.__spec__ = importlib.util.spec_from_loader(name, loader=None, is_package=True)
        package.__spec__.submodule_search_locations = []
        sys.modules[name] = package
    modules = {}
    for name in ORDER:
        check()
        modules[name] = load_source(name, bound.paths[name], bound.raws[name])
    api = {key: modules[name] for key, name in ALIASES.items()}
    semantic_id = api["S"].semantic_id()
    result = ExportLocationSupport(bound.root, bound.python_root, bound.profile_sha256,
        semantic_id, api["OA"].namespace_for(semantic_id), MappingProxyType(modules),
        MappingProxyType(api), bound, check, _CONSTRUCTION)
    result.verify()
    return result


def load_supervision(bound):
    need(type(bound) is BoundProfile, "BOUND_SUPERVISOR")
    supervisor = load_source("_export_operator_supervisor", bound.paths["_supervisor"],
                             bound.raws["_supervisor"])
    load_source("domains", bound.paths["domains"], bound.raws["domains"])
    job = load_source("_export_operator_job", bound.paths["_job"], bound.raws["_job"])
    return supervisor, job.Job


def operational_result(report):
    return (report.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED" and
            report.get("child_exit_code") == 0 and report.get("direct_child_reaped") is True and
            report.get("job_closed") is True and report.get("cleanup_errors") == [] and
            report.get("termination_requested") is False and
            type(report.get("final_job")) is dict and
            report["final_job"].get("active_processes") == 0 and
            report["final_job"].get("terminated_processes") == 0)

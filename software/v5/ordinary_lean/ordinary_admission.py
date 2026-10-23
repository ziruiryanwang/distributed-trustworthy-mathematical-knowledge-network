"""Installation-relative ordinary Lean admission, not a network trust service.

Owner-adopted named support + immutable owner storage + a clean live native
checking event authorize promotion. Hashes identify that support; they do not
prove its correctness. The installation is explicitly NOT a hermetic toolchain.
Peer input is inert V2 evidence, never Lean source, native modules or a command.

One finite call checks only new complete units above one protected local context.
Cold context loading is not constant cost. Custody is durable before promotion;
failed calls may leave inert bytes, charged snapshot staging and retained call
spool. Call spool is bounded per operation but is NOT charged by the catalog's
snapshot-byte quota; its disk capacity is a separate operator responsibility.
No retry or migration is
implicit. The selected Windows supervisor is containment, NOT a security sandbox.

Installation manifest (canonical JSON, externally pinned SHA256):
  schema, implementation, roles, compiled_dirs, support_groups, files
roles maps ROLE_FILES to logical relative files. A python_runtime/ or lean_runtime/
prefix selects a separately rooted, explicitly owner-supplied runtime attachment;
other paths remain installation-relative. Absolute attachment paths are not IDs.
compiled_dirs maps each
flat helper directory to its sorted .olean filenames. support_groups maps each
of P.SUPPORT_FIELDS to sorted paths in files. files maps paths to {bytes,sha256}.
Each implementation support digest is support_digest(field, manifest). Relative
paths make relocation neutral. This first stable I intentionally differs from
development test-controller I; existing stores cannot silently change I.

Source candidate: no execution/installation/adoption follows from importing it.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import heapq
import importlib.util
import json
import math
import os
from pathlib import Path, PurePosixPath
import secrets
import subprocess
import sys
import time

# The isolated internal shim imports only these owner-installed sibling modules.
_SOURCE = Path(__file__).resolve().parent
if str(_SOURCE) not in sys.path:
    sys.path.insert(0, str(_SOURCE))
import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as PE
import local_catalog as C
import portable_catalog as P

MIB = 1024 * 1024
INSTALL_SCHEMA = "DMKN_ORDINARY_NATIVE_INSTALLATION_V1"
SUPPORT_DOMAIN = "DMKN-ORDINARY-INSTALLED-SUPPORT-V1"
ROLE_FILES = ("python", "python_dll", "python_stable_dll", "lean", "worker",
              "seed", "inventory", "supervisor", "job", "domains", "core",
              "evidence", "semantics", "portable_evidence", "catalog", "legacy_catalog")
RUNTIME_ROOTS = ("python_runtime", "lean_runtime")
CORE_NAMES = {"core": "ordinary_admission.py", "evidence": "ordinary_evidence.py",
              "semantics": "ordinary_semantics.py", "portable_evidence": "portable_evidence.py",
              "catalog": "portable_catalog.py", "legacy_catalog": "local_catalog.py"}
NATIVE_MODULES = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "LocalSnapshot",
                  "BootstrapSupport", "OrdinaryExport", "BasisSnapshot", "OrdinaryWorkflowWorker")
KERNEL_FILES = ("lean.exe", "libInit_shared.dll", "libleanshared.dll",
                "libleanshared_1.dll", "libleanshared_2.dll", "libc++.dll")
REPORT_FIELDS = {"schema", "kind", "module_name", "parent_module", "names",
                 "units_checked", "artifact_bytes"}
need, sha = C.need, P.sha


def relative(value):
    need(type(value) is str and 0 < len(value) <= 1024 and "\\" not in value,
         "ADMISSION_RELATIVE_PATH")
    path = PurePosixPath(value)
    need(not path.is_absolute() and path.as_posix() == value and path.parts and
         all(part not in (".", "..") and not part.endswith((".", " ")) and
             not any(ord(c) < 32 or c in ':*?"<>|' for c in part) and
             not os.path.isreserved(part) for part in path.parts), "ADMISSION_RELATIVE_PATH")
    return path


def support_digest(field, manifest):
    """Public pure constructor for the stable implementation support claim.

    Call only after validating/installing the selected bytes. Including role and
    helper-search bindings in controller support prevents execution-role changes
    from retaining I just because the same unordered file set is present.
    """
    need(field in P.SUPPORT_FIELDS, "ADMISSION_SUPPORT_FIELD")
    selected = {path: manifest["files"][path] for path in manifest["support_groups"][field]}
    value = {"field": field, "files": selected}
    if field == "controller_support":
        value.update(roles=manifest["roles"], compiled_dirs=manifest["compiled_dirs"])
    return C.digest(SUPPORT_DOMAIN, value)


def _writer_json(raw, maximum):
    """Bounded native writer JSON (key order/whitespace need not be canonical).

    This is for pinned basis material and the actual selected worker report,
    never a more permissive replacement for V2 peer-evidence parsing.
    """
    need(type(raw) is bytes and 0 < len(raw) <= maximum, "ADMISSION_WRITER_BYTES")
    stack, quoted, escaped, i = [], False, False, 0
    while i < len(raw):
        byte = raw[i]
        if quoted:
            need(byte >= 32, "ADMISSION_WRITER_STRING")
            if escaped: escaped = False
            elif byte == 92: escaped = True
            elif byte == 34: quoted = False
            i += 1
            continue
        if byte == 34:
            quoted = True
        elif byte in (91, 123):
            stack.append(byte)
            need(len(stack) <= 64, "ADMISSION_WRITER_DEPTH")
        elif byte in (93, 125):
            need(stack and stack.pop() == (91 if byte == 93 else 123), "ADMISSION_WRITER_BRACKETS")
        elif 48 <= byte <= 57:
            start = i
            while i < len(raw) and 48 <= raw[i] <= 57:
                i += 1
                need(i-start <= 20, "ADMISSION_WRITER_INTEGER")
            token = raw[start:i]
            need((len(token) == 1 or token[0] != 48) and
                 (len(token) < 20 or token <= b"18446744073709551615"), "ADMISSION_WRITER_UINT64")
            continue
        else:
            need(byte in (9, 10, 13, 32, 44, 58), "ADMISSION_WRITER_TOKEN")
        i += 1
    need(not quoted and not escaped and not stack, "ADMISSION_WRITER_UNTERMINATED")
    def pairs(rows):
        result = {}
        for key, value in rows:
            need(key not in result, "ADMISSION_WRITER_DUPLICATE_KEY")
            result[key] = value
        return result
    def reject(_):
        raise C.CatalogError("ADMISSION_WRITER_NUMBER")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=reject, parse_constant=reject)


class NativeInstallation:
    """Once-per-owner-process verification of immutable explicit named support.

    The current process must use this installed core and the pinned Python.
    Owner adoption, OS/runtime integrity, no hostile in-process caller and no
    installation mutation after opening are premises, not facts from this hash.
    """

    @classmethod
    def open(cls, installation_root, manifest_raw, expected_manifest_sha256, *, runtime_roots):
        need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
             sys.dont_write_bytecode and not sys.flags.optimize, "ADMISSION_OWNER_PYTHON_PROFILE")
        C.hexid(expected_manifest_sha256)
        need(type(manifest_raw) is bytes and sha(manifest_raw) == expected_manifest_sha256,
             "ADMISSION_INSTALLATION_PIN")
        doc = E.strict_json(manifest_raw, E.Limits(max_bytes=2*MIB))
        P.fields(doc, ("schema", "implementation", "roles", "compiled_dirs", "support_groups", "files"),
                 "ADMISSION_INSTALLATION_FIELDS")
        need(doc["schema"] == INSTALL_SCHEMA, "ADMISSION_INSTALLATION_SCHEMA")
        root = C.ordinary(installation_root, directory=True)
        P.fields(runtime_roots, RUNTIME_ROOTS, "ADMISSION_RUNTIME_ROOTS")
        attachments = {key: C.ordinary(value, directory=True) for key, value in runtime_roots.items()}
        selected_roots = [root, *attachments.values()]
        for position, left in enumerate(selected_roots):
            for right in selected_roots[position+1:]:
                need(not left.is_relative_to(right) and not right.is_relative_to(left),
                     "ADMISSION_INSTALLATION_RUNTIME_OVERLAP")
        P.fields(doc["roles"], ROLE_FILES, "ADMISSION_INSTALLATION_ROLES")
        P.fields(doc["support_groups"], P.SUPPORT_FIELDS, "ADMISSION_SUPPORT_GROUPS")
        files, roles, compiled = doc["files"], doc["roles"], doc["compiled_dirs"]
        need(type(files) is dict and 1 <= len(files) <= 512 and type(compiled) is dict and
             1 <= len(compiled) <= 8, "ADMISSION_INSTALLATION_CENSUS_BOUND")
        total = 0
        for path, pin in files.items():
            relative(path)
            P.fields(pin, ("bytes", "sha256"), "ADMISSION_FILE_PIN")
            total += P.uint(pin["bytes"], 1, 512*MIB, "ADMISSION_FILE_BOUND")
            C.hexid(pin["sha256"])
        need(total <= 2*1024*MIB, "ADMISSION_INSTALLATION_BYTE_BOUND")
        need(len({path.casefold() for path in files}) == len(files), "ADMISSION_PATH_CASE_ALIAS")
        for role, path in roles.items():
            relative(path)
            need(path in files, "ADMISSION_UNPINNED_ROLE:"+role)
        need(len(set(roles.values())) == len(roles), "ADMISSION_ROLE_ALIAS")
        need(roles["python"] == "python_runtime/python.exe" and
             roles["python_dll"] == "python_runtime/python314.dll" and
             roles["python_stable_dll"] == "python_runtime/python3.dll" and
             roles["lean"] == "lean_runtime/bin/lean.exe", "ADMISSION_RUNTIME_ROLE_LAYOUT")
        for role in set(ROLE_FILES)-{"python", "python_dll", "python_stable_dll", "lean"}:
            need(relative(roles[role]).parts[0] not in RUNTIME_ROOTS, "ADMISSION_CORE_RUNTIME_ALIAS")
        core_dir = relative(roles["core"]).parent
        for role, name in CORE_NAMES.items():
            need(relative(roles[role]) == core_dir/name, "ADMISSION_CORE_LAYOUT")
        need(relative(roles["worker"]).name == "OrdinaryWorkflowWorker.lean", "ADMISSION_FIXED_WORKER")
        worker_dir = relative(roles["worker"]).parent
        native_sources = {(worker_dir/(name+".lean")).as_posix() for name in NATIVE_MODULES}
        native_objects = set()
        for directory, names in compiled.items():
            relative(directory)
            need(relative(directory).parts[0] not in RUNTIME_ROOTS, "ADMISSION_COMPILED_RUNTIME_ALIAS")
            need(type(names) is list and names == sorted(set(names)) and 1 <= len(names) <= 8,
                 "ADMISSION_COMPILED_CENSUS")
            for name in names:
                need(type(name) is str and name in {n+".olean" for n in NATIVE_MODULES},
                     "ADMISSION_COMPILED_NAME")
                path = (relative(directory)/name).as_posix()
                need(path in files and name not in {PurePosixPath(p).name for p in native_objects},
                     "ADMISSION_COMPILED_SHADOW")
                native_objects.add(path)
        need({PurePosixPath(p).name for p in native_objects} == {n+".olean" for n in NATIVE_MODULES},
             "ADMISSION_NATIVE_MODULE_CENSUS")
        native_by_name = {PurePosixPath(p).stem: p for p in native_objects}
        kernel_dir = relative(roles["lean"]).parent
        kernel = {(kernel_dir/name).as_posix() for name in KERNEL_FILES}
        need(relative(roles["lean"]).name == "lean.exe" and native_sources | kernel <= set(files),
             "ADMISSION_NATIVE_SUPPORT_REQUIRED")
        required = {
            "kernel_support": kernel,
            "adapter_support": native_sources | native_objects,
            "basis_receiver_support": {roles["seed"], roles["inventory"]} |
                {(worker_dir/(n+".lean")).as_posix() for n in ("BootstrapSupport", "BasisSnapshot")} |
                {native_by_name[n] for n in ("BootstrapSupport", "BasisSnapshot")},
            "snapshot_support": {(worker_dir/"LocalSnapshot.lean").as_posix(), native_by_name["LocalSnapshot"]},
            "controller_support": {roles[k] for k in (*CORE_NAMES, "python", "python_dll", "python_stable_dll",
                                                       "supervisor", "job", "domains")},
        }
        covered = set()
        for field, paths in doc["support_groups"].items():
            need(type(paths) is list and paths == sorted(set(paths)) and required[field] <= set(paths) <= set(files),
                 "ADMISSION_REQUIRED_SUPPORT:"+field)
            covered.update(paths)
        need(covered == set(files), "ADMISSION_UNCOMMITTED_SUPPORT")
        implementation_raw = E.canonical_json(doc["implementation"])
        implementation = S.read_implementation(implementation_raw)
        need(all(implementation[field] == support_digest(field, doc) for field in P.SUPPORT_FIELDS),
             "ADMISSION_IMPLEMENTATION_SUPPORT")
        need(files[roles["seed"]] == {"bytes": 724174, "sha256": S.SEED} and
             files[roles["inventory"]] == {"bytes": 823690, "sha256": S.INVENTORY},
             "ADMISSION_FIXED_BASIS_BYTES")
        self = cls.__new__(cls)
        self.root, self.manifest_raw, self.manifest_sha256 = root, manifest_raw, expected_manifest_sha256
        self.runtime_roots = attachments
        self.doc, self.implementation_raw = doc, implementation_raw
        self.implementation_id = S.implementation_id(implementation_raw)
        self.semantic_id = implementation["semantic_id"]
        for path in files:
            self._verify(path)
        for directory, names in compiled.items():
            folder = C.ordinary(self.resolve(directory), directory=True)
            with os.scandir(folder) as listing:
                actual = []
                for entry in listing:
                    need(len(actual) < 8 and entry.name in names, "ADMISSION_COMPILED_EXTRA")
                    C.ordinary(Path(entry.path))
                    actual.append(entry.name)
            need(sorted(actual) == names, "ADMISSION_COMPILED_CENSUS")
        need(self.path("python") == Path(sys.executable).resolve() and
             self.path("core") == Path(__file__).resolve(), "ADMISSION_RUNNING_SUPPORT")
        for role, module in (("evidence", E), ("semantics", S), ("portable_evidence", PE),
                             ("catalog", P), ("legacy_catalog", C)):
            need(self.path(role) == Path(module.__file__).resolve(), "ADMISSION_LOADED_SUPPORT")
        self._supervisor = self._load("_dmkn_ordinary_supervisor", "supervisor")
        self._load("domains", "domains")
        self._job_module = self._load("_dmkn_ordinary_job", "job")
        return self

    def path(self, role):
        return self.resolve(self.doc["roles"][role])

    def resolve(self, logical_path):
        parts = relative(logical_path).parts
        if parts[0] in RUNTIME_ROOTS:
            need(len(parts) >= 2, "ADMISSION_RUNTIME_FILE_PATH")
            return self.runtime_roots[parts[0]].joinpath(*parts[1:])
        return self.root.joinpath(*parts)

    def _verify(self, relative_path):
        pin = self.doc["files"][relative_path]
        path = C.ordinary(self.resolve(relative_path))
        need(path.stat().st_size == pin["bytes"], "ADMISSION_SUPPORT_SIZE")
        size, digest = 0, hashlib.sha256()
        with path.open("rb") as stream:
            while block := stream.read(MIB):
                size += len(block)
                need(size <= pin["bytes"], "ADMISSION_SUPPORT_GREW")
                digest.update(block)
        need(size == pin["bytes"] and path.stat().st_size == size and digest.hexdigest() == pin["sha256"],
             "ADMISSION_SUPPORT_CHANGED")

    def read(self, role, maximum):
        path, pin = self.path(role), self.doc["files"][self.doc["roles"][role]]
        raw = C.read_bounded(path, maximum)
        need(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"], "ADMISSION_ROLE_CHANGED")
        return raw

    def _load(self, name, role):
        path, raw = self.path(role), self.read(role, 2*MIB)
        if name in sys.modules:
            module = sys.modules[name]
            need(Path(module.__file__).resolve() == path, "ADMISSION_LOADED_SUPPORT_COLLISION")
            return module
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            exec(compile(raw, str(path), "exec"), module.__dict__)
        except BaseException:
            del sys.modules[name]
            raise
        return module


class OperationBudget:
    """One nonrenewing admission allocation; instantiate before preparation.

    Parent Python CPU/wall checks are cooperative. The native subprocess tree has
    actual selected Windows Job limits; filesystem/log caps are sampled. A caller
    needing hard limits for the Python controller must supervise that controller
    too. This object cannot be reused to launch another native operation.
    """
    def __init__(self, wall_seconds, cpu_seconds, memory_mib, *, active_processes=4,
                 output_bytes=64*MIB, log_bytes=MIB):
        P.uint(wall_seconds, 30, 3600, "ADMISSION_WALL_ALLOCATION")
        P.uint(cpu_seconds, 2, 200000, "ADMISSION_CPU_ALLOCATION")
        P.uint(memory_mib, 1, 8192, "ADMISSION_MEMORY_ALLOCATION")
        P.uint(active_processes, 2, 8, "ADMISSION_PROCESS_ALLOCATION")
        P.uint(output_bytes, 1, 1024*MIB, "ADMISSION_OUTPUT_ALLOCATION")
        P.uint(log_bytes, 1, 8*MIB, "ADMISSION_LOG_ALLOCATION")
        self.started, self.cpu_started = time.monotonic(), time.process_time()
        self.deadline, self.cpu_seconds = self.started+wall_seconds, cpu_seconds
        self.memory_mib, self.active_processes = memory_mib, active_processes
        self.output_bytes, self.log_bytes = output_bytes, log_bytes
        self.worker_cpu, self.claimed = 0.0, False

    def check(self):
        need(time.monotonic() < self.deadline and
             time.process_time()-self.cpu_started+self.worker_cpu < self.cpu_seconds,
             "ADMISSION_OPERATION_BUDGET")

    def claim(self):
        need(not self.claimed, "ADMISSION_BUDGET_ALREADY_USED")
        self.claimed = True
        self.check()

    def allowance(self, grant_deadline):
        self.check()
        # Existing supervisor may spend <=20s in failed-child wait/quiescence;
        # reserve that plus bookkeeping, never replenish its parent allocation.
        wall = math.floor(min(self.deadline, grant_deadline)-time.monotonic())-24
        cpu = math.floor(self.cpu_seconds-(time.process_time()-self.cpu_started)-self.worker_cpu)-1
        need(wall >= 1 and cpu >= 1, "ADMISSION_INSUFFICIENT_REMAINING_BUDGET")
        return {"cpu_seconds": cpu, "wall_seconds": wall, "memory_mib": self.memory_mib,
                "active_processes": self.active_processes,
                "stdout_bytes": self.log_bytes, "stderr_bytes": self.log_bytes}


@dataclass(frozen=True)
class PreflightLimits:
    max_units: int = 1024
    max_bytes: int = 64*MIB
    max_nodes: int = 2097152
    max_names: int = 65536
    max_edges: int = 1048576

    def __post_init__(self):
        for key, ceiling in (("max_units", 1024), ("max_bytes", 64*MIB), ("max_nodes", 2097152),
                             ("max_names", 65536), ("max_edges", 1048576)):
            P.uint(getattr(self, key), 1, ceiling, "ADMISSION_PREFLIGHT_LIMIT:"+key)


@dataclass(frozen=True)
class Preflight:
    """Immutable convenience plan, NEVER a warrant or resumable native grant."""
    status: str
    parent_root: str
    raw_units: tuple[bytes, ...]
    ordered_units: tuple[bytes, ...]
    missing: tuple[tuple[bytes, str], ...]
    reused_unit_ids: tuple[str, ...]


def _plan(context, raw_units, limits, check):
    need(type(limits) is PreflightLimits and type(raw_units) in (tuple, list) and
         1 <= len(raw_units) <= limits.max_units and all(type(raw) is bytes for raw in raw_units) and
         sum(map(len, raw_units)) <= limits.max_bytes, "ADMISSION_FINITE_BATCH")
    check()
    units, new, exports, reused, nodes, names = {}, {}, {}, [], 0, 0
    for raw in raw_units:
        check()
        item = PE.read_evidence(raw)
        need(item.document["semantic_id"] == context["semantic_id"], "ADMISSION_UNSUPPORTED_SEMANTICS")
        if item.unit_id in units:
            need(units[item.unit_id].raw == raw, "ADMISSION_UNIT_COLLISION")
            continue
        units[item.unit_id] = item
        nodes += item.census.total_nodes
        rows = item.document["unit"][2]
        names += len(rows)
        need(nodes <= limits.max_nodes and names <= limits.max_names, "ADMISSION_BATCH_CENSUS_BOUND")
        known = 0
        for row in rows:
            key = E.name_key(row[0])
            identity = S.export_id(context["semantic_id"], item.unit_id, row[0])
            previous = context["bindings"].get(key)
            if previous is not None:
                need(previous == identity, "ADMISSION_PARENT_NAME_CONFLICT")
                known += 1
            else:
                need(key not in exports, "ADMISSION_SELECTED_NAME_CONFLICT")
                exports[key] = (identity, item.unit_id)
        need(known in (0, len(rows)), "ADMISSION_PARTIAL_GROUP_ALREADY_PRESENT")
        if known:
            reused.append(item.unit_id)
        else:
            new[item.unit_id] = item
    dependencies, users, missing, edges = {}, {identity: [] for identity in new}, {}, 0
    for identity, item in units.items():
        check()
        deps = set()
        for name, symbol in item.document["imports"]:
            edges += 1
            need(edges <= limits.max_edges, "ADMISSION_IMPORT_EDGE_BOUND")
            key = E.name_key(name)
            current = context["bindings"].get(key)
            if current is not None:
                need(current == symbol, "ADMISSION_PARENT_IMPORT_CONFLICT")
            elif key in exports:
                expected, supplying_unit = exports[key]
                need(symbol == expected, "ADMISSION_SELECTED_IMPORT_CONFLICT")
                deps.add(supplying_unit)
            else:
                need(key not in missing or missing[key] == symbol, "ADMISSION_MISSING_NAME_CONFLICT")
                missing[key] = symbol
        # A reused exact output already has a warranted root in this context;
        # immutable evidence must still have its exact complete imports there.
        if identity not in new:
            need(not deps and all(context["bindings"].get(E.name_key(n)) == s
                                  for n, s in item.document["imports"]), "ADMISSION_REUSED_IMPORT_LINEAGE")
            continue
        dependencies[identity] = deps
        for dependency in deps:
            users[dependency].append(identity)
    ready = [identity for identity, deps in dependencies.items() if not deps]
    heapq.heapify(ready)
    ordered = []
    while ready:
        check()
        identity = heapq.heappop(ready)
        ordered.append(new[identity].raw)
        for user in users[identity]:
            dependencies[user].remove(identity)
            if not dependencies[user]: heapq.heappush(ready, user)
    need(len(ordered) == len(new), "ADMISSION_CYCLIC_SELECTED_UNITS")
    return Preflight("NEEDS" if missing else "READY", context["local_root"],
                     tuple(units[key].raw for key in sorted(units)), tuple(ordered),
                     tuple(sorted(missing.items())), tuple(sorted(reused)))


def _clean_worker(result):
    final = result.get("final_job")
    return (result.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED" and
            result.get("child_exit_code") == 0 and result.get("direct_child_reaped") is True and
            result.get("job_closed") is True and result.get("cleanup_errors") == [] and
            result.get("termination_requested") is False and type(final) is dict and
            final.get("active_processes") == 0 and final.get("terminated_processes") == 0)


class OrdinaryAdmission:
    """Serialized owner API; caller owns discovery, custody service and authoring.

    evidence_store is an owner-supplied durable-custody contract, normally the
    installed OrdinaryStore. It is NOT a peer-supplied callback or mathematical
    authority. Its actual durable implementation must be adopted by the owner;
    callable checks/readback cannot prove crash persistence. It is deliberately
    outside mathematical I because a false durability promise loses availability,
    not kernel checking. No hostile in-process caller is in this model.
    Closing this object closes its catalog, never caller-owned custody.
    """
    @classmethod
    def open(cls, installation, catalog_directory, store_id, evidence_store, *, create=False, limits=P.Limits()):
        need(type(installation) is NativeInstallation and type(limits) is P.Limits,
             "ADMISSION_CONFIGURATION")
        need(evidence_store.semantic_id == installation.semantic_id and
             callable(evidence_store.put_evidence) and callable(evidence_store.get_evidence),
             "ADMISSION_CUSTODY_CONFIGURATION")
        directory = C.ordinary(catalog_directory, directory=True, fresh=create)
        custody_root = C.ordinary(evidence_store.root, directory=True)
        for left, right in [(directory, custody_root)] + [
                (state, support) for state in (directory, custody_root)
                for support in (installation.root, *installation.runtime_roots.values())]:
            need(not left.is_relative_to(right) and not right.is_relative_to(left),
                 "ADMISSION_STORAGE_INSTALLATION_OVERLAP")
        self = cls.__new__(cls)
        self.installation, self.evidence_store = installation, evidence_store
        self.catalog = P.PortableCatalog.open(directory, installation.implementation_raw,
                                             store_id, create=create, limits=limits)
        self.directory, self.limits = directory, limits
        try:
            self.calls = directory/"admission-calls"
            if create: C.ordinary(self.calls, directory=True, fresh=True).mkdir()
            else: C.ordinary(self.calls, directory=True)
        except BaseException:
            self.catalog.close()
            raise
        return self

    def close(self):
        self.catalog.close()

    def preflight(self, parent_root, raw_units, *, limits=PreflightLimits(), budget=None):
        need(budget is None or type(budget) is OperationBudget, "ADMISSION_BUDGET_TYPE")
        check = (lambda: None) if budget is None else budget.check
        check()
        context = self.catalog.context(parent_root)
        check()
        return _plan(context, raw_units, limits, check)

    def _call_directory(self):
        path = self.calls/secrets.token_hex(32)
        C.ordinary(path, directory=True, fresh=True).mkdir()
        return path

    @staticmethod
    def _write(path, raw, maximum):
        need(type(raw) is bytes and 0 < len(raw) <= maximum, "ADMISSION_AUTHORED_FILE_BOUND")
        P.PortableCatalog._write_fresh(path, raw)

    def _stage(self, raw_units, budget):
        for raw in raw_units:
            budget.check()
            evidence = PE.read_evidence(raw)
            stored = self.evidence_store.put_evidence(raw, before_commit=budget.check)
            need(stored["semantic_id"] == self.installation.semantic_id and
                 stored["identity"] == evidence.unit_id and stored["raw_sha256"] == sha(raw) and
                 stored["raw_bytes"] == len(raw) and stored["mathematical_acceptance"] is False,
                 "ADMISSION_CUSTODY_BINDING")
            need(self.evidence_store.get_evidence(self.installation.semantic_id, evidence.unit_id,
                 len(raw), check_budget=budget.check) == raw, "ADMISSION_CUSTODY_READBACK")
            budget.check()

    def initialize(self, budget):
        """Fresh-store fixed basis only; never replay/migrate an existing library."""
        need(type(budget) is OperationBudget, "ADMISSION_BUDGET_TYPE")
        budget.claim()
        seed = _writer_json(self.installation.read("seed", MIB), MIB)
        inventory = _writer_json(self.installation.read("inventory", MIB), MIB)
        names = seed[2]
        need(type(names) is list and len(names) == 581 and [row[0] for row in inventory] == names,
             "ADMISSION_FIXED_BASIS_NAME_CENSUS")
        budget.check()
        seconds = math.floor(budget.deadline-time.monotonic())-1
        need(seconds >= 25, "ADMISSION_REMAINING_BUDGET")
        grant = self.catalog.reserve_basis(names, seconds=seconds, output_bytes=budget.output_bytes,
                                           parent_deadline=budget.deadline)
        return self._execute(grant, None, (), names, 456, budget)

    def admit(self, parent_root, plan, budget):
        need(type(plan) is Preflight and type(budget) is OperationBudget and plan.parent_root == parent_root,
             "ADMISSION_PLAN_TYPE_OR_PARENT")
        budget.claim()
        # Do not trust status, order, missing list or reused IDs in a caller plan.
        actual = self.preflight(parent_root, plan.raw_units, budget=budget)
        need(actual.status == "READY", "ADMISSION_MISSING_DEPENDENCIES")
        self._stage(actual.raw_units, budget)
        if not actual.ordered_units:
            budget.check()
            return {"status": "REUSED", "local_root": parent_root, "units_checked": 0,
                    "retained_unit_ids": list(actual.reused_unit_ids)}
        context = self.catalog.context(parent_root)
        names = [row[0] for raw in actual.ordered_units
                 for row in PE.read_evidence(raw).document["unit"][2]]
        budget.check()
        seconds = math.floor(budget.deadline-time.monotonic())-1
        need(seconds >= 25, "ADMISSION_REMAINING_BUDGET")
        grant = self.catalog.reserve_extension(parent_root, actual.ordered_units,
            seconds=seconds, output_bytes=budget.output_bytes, parent_deadline=budget.deadline)
        return self._execute(grant, context, actual.ordered_units, names, len(actual.ordered_units), budget)

    def _execute(self, grant, context, raw_units, names, unit_count, budget):
        call, supervisor_result, native_entered = None, None, False
        try:
            budget.check()
            need(grant.deadline <= budget.deadline, "ADMISSION_GRANT_PARENT_DEADLINE")
            call = self._call_directory()
            self._write(call/"installation.json", self.installation.manifest_raw, 2*MIB)
            if context is None:
                need(grant.kind == "basis" and not raw_units and grant.parent_plan_raw == b"[]" and
                     grant.input_unit_ids == () and grant.parent_module_raw == b"[]", "ADMISSION_BASIS_GRANT")
                command = ["basis", str(self.installation.path("seed")), str(self.installation.path("inventory"))]
            else:
                identities = tuple(PE.read_evidence(raw).unit_id for raw in raw_units)
                need(grant.kind == "extension" and grant.parent == context["local_root"] and
                     grant.input_unit_ids == identities and grant.request_hash == P.batch_id(list(identities)) and
                     grant.parent_plan_raw == E.canonical_json(context["modules"]) and
                     grant.parent_module_raw == E.canonical_json(context["root_module"]), "ADMISSION_EXTENSION_GRANT")
                plan = {"basis_module": context["basis_module"], "root_module": context["root_module"],
                        "modules": E.strict_json(grant.parent_plan_raw, E.Limits(max_bytes=16*MIB))}
                units = [PE.read_evidence(raw).document["unit"] for raw in raw_units]
                self._write(call/"plan.json", E.canonical_json(plan), 16*MIB)
                self._write(call/"units.json", E.canonical_json(units), 64*MIB)
                command = ["extend", str(call/"plan.json"), str(call/"units.json")]
            report_path, artifact_path = call/"worker-report.json", grant.directory/"chunk.olean"
            command.extend([grant.root, str(artifact_path), str(report_path)])
            argv = [str(self.installation.path("python")), "-I", "-S", "-B",
                    str(self.installation.path("core")), "--worker", str(self.installation.root),
                    str(self.installation.runtime_roots["python_runtime"]),
                    str(self.installation.runtime_roots["lean_runtime"]),
                    str(call/"installation.json"), self.installation.manifest_sha256, *command]
            A, J = self.installation._supervisor, self.installation._job_module
            allowance = A.limits_checked(budget.allowance(grant.deadline))
            native_entered = True
            supervisor_result = A.supervise(argv, call, call/"supervision", allowance, J.Job)
            # Save observation but do not read it back to manufacture authority.
            A.save_new(call/"supervision-result.json", supervisor_result)
            final = supervisor_result.get("final_job")
            if type(final) is dict and type(final.get("cpu_seconds")) in (int, float):
                budget.worker_cpu += final["cpu_seconds"]
            need(_clean_worker(supervisor_result), "ADMISSION_NATIVE_EVENT_NOT_CLEAN")
            need(C.ordinary(call/"supervision/stdout.txt").stat().st_size == 0 and
                 C.ordinary(call/"supervision/stderr.txt").stat().st_size == 0,
                 "ADMISSION_NATIVE_DIAGNOSTIC")
            budget.check()
            report = _writer_json(C.read_bounded(report_path, 16*MIB), 16*MIB)
            artifact = C.ordinary(artifact_path)
            need(type(report) is dict and set(report) == REPORT_FIELDS and
                 report["schema"] == "DMKN_ORDINARY_WORKER_OUTPUT_V1" and report["kind"] == grant.kind and
                 report["module_name"] == E.strict_json(grant.module_name_raw) and
                 report["parent_module"] == E.strict_json(grant.parent_module_raw) and report["names"] == names and
                 type(report["units_checked"]) is int and report["units_checked"] == unit_count and
                 type(report["artifact_bytes"]) is int and report["artifact_bytes"] == artifact.stat().st_size and
                 0 < report["artifact_bytes"] <= budget.output_bytes, "ADMISSION_ACTUAL_REPORT_BINDING")
            budget.check()
            accepted = self.catalog._commit_checked(grant)
            retained = list(grant.input_unit_ids)
            grant = None
            # Atomic catalog promotion is the linearization point. A later
            # transport/publication failure cannot undo it or grant a new budget.
            return {"status": "CHECKED", "local_root": accepted, "units_checked": unit_count,
                    "retained_unit_ids": retained, "operation_directory": str(call),
                    "worker_cpu_seconds": budget.worker_cpu,
                    "controller_cpu_seconds": time.process_time()-budget.cpu_started}
        finally:
            if grant is not None and not self.catalog._closed and self.catalog._grant is grant:
                # If cleanup is uncertain, quarantine the owner catalog rather
                # than permit further admission while a possible child exists.
                if native_entered and (supervisor_result is None or not (
                    supervisor_result.get("job_closed") is True and
                    supervisor_result.get("direct_child_reaped") is True and
                    supervisor_result.get("cleanup_errors") == [] and
                    type(supervisor_result.get("final_job")) is dict and
                    supervisor_result["final_job"].get("active_processes") == 0)):
                    try:
                        marker = self.directory/"WITHDRAWN"
                        if not os.path.lexists(marker):
                            self._write(marker, b"ADMISSION_NATIVE_CLEANUP_UNCERTAIN", 128)
                    finally:
                        self.catalog.close()
                else:
                    self.catalog.abandon(grant)


def _worker_main(args):
    """Only internal fixed-command launch, inherited enclosing Windows Job.

    No catalog opening or promotion. Parent has verified immutable installation
    support once; this child binds its exact manifest/roles without rehashing the
    whole native runtime for every theorem. Direct use supplies no authority.
    """
    need(os.name == "nt" and len(args) == 11 and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "ADMISSION_WORKER_ARGUMENTS")
    root = C.ordinary(args[0], directory=True)
    attachments = {key: C.ordinary(value, directory=True) for key, value in zip(RUNTIME_ROOTS, args[1:3])}
    manifest_path, expected = C.ordinary(args[3]), C.hexid(args[4])
    raw = C.read_bounded(manifest_path, 2*MIB)
    need(sha(raw) == expected, "ADMISSION_WORKER_MANIFEST")
    doc = E.strict_json(raw, E.Limits(max_bytes=2*MIB))
    need(doc["schema"] == INSTALL_SCHEMA, "ADMISSION_WORKER_SCHEMA")
    def path(role):
        parts = relative(doc["roles"][role]).parts
        return C.ordinary(attachments[parts[0]].joinpath(*parts[1:]) if parts[0] in attachments
                          else root.joinpath(*parts))
    need(path("core") == Path(__file__).resolve() and path("python") == Path(sys.executable).resolve(),
         "ADMISSION_WORKER_RUNNING_SUPPORT")
    command = args[5:]
    need(command[0] in ("basis", "extend") and len(command) == 6, "ADMISSION_FIXED_COMMAND")
    C.hexid(command[3])
    for value in command[1:3]: C.ordinary(value)
    for value in command[4:]: C.ordinary(value, fresh=True)
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
    env["LEAN_PATH"] = os.pathsep.join(str(C.ordinary(root.joinpath(*relative(d).parts), directory=True))
                                      for d in doc["compiled_dirs"])
    env["PATH"] = os.pathsep.join((str(path("python").parent), str(path("lean").parent)))
    worker = path("worker")
    argv = [str(path("lean")), "-R", str(worker.parent), "--run", str(worker), *command]
    return subprocess.call(argv, cwd=Path.cwd(), env=env, stdin=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)


if __name__ == "__main__":
    need(sys.argv[1:2] == ["--worker"], "ADMISSION_INTERNAL_WORKER_ONLY")
    raise SystemExit(_worker_main(sys.argv[2:]))

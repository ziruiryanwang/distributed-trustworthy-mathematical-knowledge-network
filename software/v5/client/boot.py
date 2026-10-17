"""Child side of the fixed bounded launcher; trusted owner strategy only."""
from __future__ import annotations
import time
import ctypes
from dataclasses import dataclass
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
from types import MappingProxyType, ModuleType


@dataclass(frozen=True)
class Context:
    installation: Path
    workspace_root: Path
    run: Path
    location_workspace: Path
    sources_v5: Path
    sources_portable: Path
    sources_owner: Path
    started: float
    deadline: float
    limits: object
    parameters: object
    source_sha256: object

    def remaining_seconds(self):
        remaining = int(self.deadline-time.monotonic())
        if remaining < 1: raise ValueError("CLIENT_ORIGINAL_DEADLINE_EXHAUSTED")
        return remaining


def bootstrap():
    # Only enough code to pin the reusable bootstrap helper; no v5 imports.
    if len(sys.argv) != 5: raise ValueError("CLIENT_BOOT_ARGUMENTS")
    plan_path = Path(sys.argv[1])
    if plan_path.stat().st_size > 1024**2: raise ValueError("CLIENT_BOOT_PLAN_SIZE")
    with plan_path.open("rb") as stream: raw = stream.read(1024**2+1)
    import hashlib
    if len(raw) > 1024**2 or hashlib.sha256(raw).hexdigest() != sys.argv[2]:
        raise ValueError("CLIENT_BOOT_PLAN_PIN")
    value = json.loads(raw)
    path = Path(__file__).resolve().parent / "launch.py"
    expected = value["sources"]["v5/client/launch.py"]
    if path.stat().st_size > 2*1024**2: raise ValueError("CLIENT_BOOT_HELPER_SIZE")
    with path.open("rb") as stream: source = stream.read(2*1024**2+1)
    if len(source) != expected["bytes"] or hashlib.sha256(source).hexdigest() != expected["sha256"]:
        raise ValueError("CLIENT_BOOT_HELPER_PIN")
    name = "_dmkn_client_launch"
    if name in sys.modules: raise ValueError("CLIENT_BOOT_HELPER_COLLISION")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(source, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def main():
    L = bootstrap()
    plan, raw, installation, workspace, roots, run = L.read_plan(sys.argv[1], sys.argv[2])
    L.invocation(installation)
    L.need(str(Path(sys.argv[1])) == str(run / "plan.json"), "CLIENT_COPIED_PLAN_ORIGIN")
    L.need(str(Path(__file__).resolve()) == str(roots["v5"] / "client/boot.py"), "CLIENT_BOOT_ORIGIN")
    L.need(all(value.isascii() and value.isdigit() and len(value) <= 20 for value in sys.argv[3:]),
           "CLIENT_BOOT_CLOCKS")
    started_ns, deadline_ns = (int(value) for value in sys.argv[3:])
    L.need(0 < started_ns < deadline_ns and deadline_ns-started_ns ==
           plan["limits"]["wall_seconds"]*1_000_000_000, "CLIENT_ORIGINAL_CLOCK_BINDING")

    def active(): L.need(time.monotonic_ns() < deadline_ns, "CLIENT_ORIGINAL_DEADLINE_EXHAUSTED")

    active()
    # OS membership is a diagnostic, not proof of a particular Job's limits.
    # The parent supervisor supplies exact limit and terminal-closure evidence.
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.IsProcessInJob.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
    kernel.IsProcessInJob.restype = ctypes.c_int
    member = ctypes.c_int()
    L.need(kernel.IsProcessInJob(kernel.GetCurrentProcess(), None, ctypes.byref(member)) and member.value,
           "CLIENT_BOOT_REQUIRES_ACTUAL_JOB")
    files, manifest_raw = L.load_manifest(installation)
    # The actual mathematical owners load their own `domains` module with an
    # exact compatibility tag. Do not occupy that name in the child bootstrap.
    A = L.load_helper("_dmkn_client_supervisor", installation / "operator/commons.py",
                      files["operator/commons.py"])
    limits = A.limits_checked(plan["limits"])
    L.need(limits["wall_seconds"] <= 3600 and limits["cpu_seconds"] <= 86400
           and limits["memory_mib"] <= 4096, "CLIENT_FINITE_OPERATION_LIMITS")
    L.ordinary(run, directory=True)
    python_root = installation / "receiver/runtime/python"
    runtime = {name: row for name, row in files.items() if name.startswith("receiver/runtime/python/")}
    L.need(1 <= len(runtime) <= 10000 and sum(row["bytes"] for row in runtime.values()) <= 256*L.MIB,
           "CLIENT_PYTHON_RUNTIME_BOUND")

    def verify_runtime():
        actual, directories = set(), 0
        for parent, children, names in os.walk(python_root, followlinks=False):
            active(); parent = L.ordinary(parent, directory=True); directories += 1
            L.need(directories <= 10000, "CLIENT_PYTHON_DIRECTORY_BOUND")
            for child in children: L.ordinary(parent / child, directory=True)
            for name in names:
                actual.add((parent / name).relative_to(installation).as_posix())
                L.need(len(actual) <= 10000, "CLIENT_PYTHON_FILE_BOUND")
        L.need(actual == set(runtime), "CLIENT_EXACT_PYTHON_CENSUS")
        for name, row in runtime.items():
            active(); L.pinned(installation / name, row)
        for name in L.HELPERS.values(): L.pinned(installation / name, files[name], 4*L.MIB)

    verify_runtime()
    runtime_search = []
    for item in sys.path:
        path = Path(item)
        L.need(item and path.is_absolute() and path.is_relative_to(python_root), "CLIENT_STDLIB_SEARCH_ORIGIN")
        runtime_search.append(str(path))
    snapshot, work = run / "sources", run / "work"
    for path in (snapshot, work):
        L.ordinary(path, directory=True, fresh=True); path.mkdir()
    held, original = {}, {}
    try:
        for name, row in plan["sources"].items():
            active(); parts = L.relative(name)
            source = roots[parts[0]].joinpath(*parts[1:])
            L.pinned(source, row, L.SOURCE_MAX)
            contents = L.read(source, L.SOURCE_MAX, allow_empty=True)
            L.need(L.sha(contents) == row["sha256"], "CLIENT_SOURCE_CHANGED_DURING_COPY")
            target = snapshot.joinpath(*parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream: stream.write(contents)
            held[target] = contents; original[source] = row
        # Exact source identities, not an inherited module cache or cwd lookup.
        portable, v5, owner = snapshot / "portable", snapshot / "v5", snapshot / "owner"
        prefixes = {L.relative(name)[1] for name in plan["sources"] if name.startswith(("v5/", "portable/"))}
        prefixes = {Path(name).stem for name in prefixes}
        L.need(not any(name.split(".")[0] in prefixes for name in sys.modules), "CLIENT_PRELOADED_PACKAGE_CONFLICT")
        L.need("location" in prefixes and (portable / "location/__init__.py") in held, "CLIENT_CLOSED_LOCATION_PACKAGE")
        sys.path[:] = [str(portable), str(v5), *runtime_search]

        class PinnedLoader(importlib.machinery.SourceFileLoader):
            def get_code(self, fullname):
                path = Path(self.path)
                L.need(path in held and path.suffix == ".py", "CLIENT_IMPORT_NOT_SELECTED_SOURCE")
                return compile(held[path], str(path), "exec", dont_inherit=True)

        class Origins:
            def find_spec(self, fullname, path=None, target=None):
                active()
                spec = importlib.machinery.PathFinder.find_spec(fullname, path, target)
                if spec is None: return None
                if spec.origin is None:
                    L.need(spec.submodule_search_locations is not None and all(
                        Path(value).is_relative_to(v5) or Path(value).is_relative_to(portable)
                        for value in spec.submodule_search_locations), "CLIENT_NAMESPACE_ORIGIN")
                    return spec
                origin = Path(spec.origin)
                if origin in held:
                    L.need(origin.suffix == ".py", "CLIENT_IMPORT_SOURCE_SUFFIX")
                    spec.loader = PinnedLoader(fullname, str(origin)); return spec
                L.need(origin.is_relative_to(python_root) and
                       origin.relative_to(installation).as_posix() in runtime, "CLIENT_UNSELECTED_IMPORT_ORIGIN")
                return spec

        guard = Origins()
        # Builtin/Frozen importers stay ahead; guard replaces filesystem fallback.
        L.need(sys.meta_path[-1] is importlib.machinery.PathFinder, "CLIENT_DEFAULT_FILESYSTEM_IMPORTER")
        sys.meta_path[-1] = guard
        context = Context(installation, workspace, run, work, v5, portable, owner,
                          started_ns/1e9, deadline_ns/1e9, MappingProxyType(dict(limits)),
                          MappingProxyType(dict(plan["parameters"])),
                          MappingProxyType({name: row["sha256"] for name, row in plan["sources"].items()}))
        entry = owner.joinpath(*L.relative(plan["owner_entry"]))
        L.need("__dmkn_owner_strategy__" not in sys.modules, "CLIENT_OWNER_MODULE_COLLISION")
        strategy = ModuleType("__dmkn_owner_strategy__")
        strategy.__file__, strategy.__package__ = str(entry), None
        sys.modules[strategy.__name__] = strategy
        namespace = strategy.__dict__
        active(); exec(compile(held[entry], str(entry), "exec", dont_inherit=True), namespace)
        L.need(callable(namespace.get("main")), "CLIENT_OWNER_MAIN_REQUIRED")
        code = namespace["main"](context)
        L.need(type(code) is int and code == 0, "CLIENT_OWNER_NONZERO_OR_INVALID_RESULT")
        active()

        origins = {}
        for name, module in tuple(sys.modules.items()):
            if name.split(".")[0] not in prefixes: continue
            value = getattr(module, "__file__", None)
            if value is None:
                paths = getattr(module, "__path__", ())
                L.need(paths and all(Path(item).is_relative_to(snapshot) for item in paths), "CLIENT_NAMESPACE_CHANGED")
                continue
            path = Path(value)
            L.need(path in held and path.suffix == ".py", "CLIENT_IMPORTED_FILE_ORIGIN")
            origins[name] = str(path.relative_to(snapshot))
        L.need(sys.meta_path[-1] is guard and sys.path == [str(portable), str(v5), *runtime_search],
               "CLIENT_IMPORT_SELECTION_CHANGED")
        L.need(L.read(sys.argv[1], L.MIB) == raw and
               L.read(installation / "RELEASE-MANIFEST.json", 8*L.MIB) == manifest_raw, "CLIENT_FINAL_PLAN_CHANGED")
        for source, row in original.items(): active(); L.pinned(source, row, L.SOURCE_MAX)
        for path, contents in held.items():
            active(); L.need(L.read(path, L.SOURCE_MAX, allow_empty=True) == contents, "CLIENT_SNAPSHOT_CHANGED")
        actual = set()
        total, entries = 0, 0
        for parent, children, names in os.walk(run, followlinks=False):
            active(); parent = L.ordinary(parent, directory=True)
            for name in children: L.ordinary(parent / name, directory=True)
            entries += len(children)+len(names)
            L.need(entries <= plan["output_limits"]["entries"], "CLIENT_OUTPUT_ENTRY_LIMIT")
            for name in names:
                path = L.ordinary(parent / name); total += path.stat().st_size
                if path.is_relative_to(snapshot): actual.add(path)
                L.need(total <= plan["output_limits"]["bytes"], "CLIENT_OUTPUT_BYTE_LIMIT")
        L.need(actual == set(held), "CLIENT_EXACT_SNAPSHOT_CENSUS")
        verify_runtime(); active()
        A.save_new(run / "BOOT-RESULT.json", {"schema": "DMKN_V5_CLIENT_BOOT_RESULT_V1", "status": "OWNER_EXITED_ZERO",
            "plan_sha256": sys.argv[2], "source_files": len(held), "source_bytes": sum(map(len, held.values())),
            "imported_origins": origins, "observed_output_entries": entries, "observed_output_bytes": total,
            "output_scope": "FINAL_PRE_REPORT_CENSUS_NOT_HARD_DISK_QUOTA",
            "job_membership": "OS_CONFIRMED_MEMBERSHIP_LIMITS_AND_CLOSURE_REPORTED_BY_PARENT",
            "authority": "SOURCE_AND_OPERATION_EVIDENCE_NOT_MATHEMATICAL_ACCEPTANCE"})
        active()
        return 0
    except BaseException as error:
        # Preserve failed output and let the unchanged parent reap all descendants.
        A.save_new(run / "BOOT-FAILED.json", {"status": "CLIENT_BOOT_OR_OWNER_FAILED",
                   "error": (type(error).__name__+": "+str(error))[:2000]})
        raise


if __name__ == "__main__":
    raise SystemExit(main())

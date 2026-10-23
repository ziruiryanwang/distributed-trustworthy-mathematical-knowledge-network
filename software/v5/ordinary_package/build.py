"""Build one owner-selected ordinary package from explicit source/runtime roots.

Windows, the exact named Lean 4.34.0/Python 3.14.6 support below, and immutable
owner-selected source/storage are premises. Runtime libraries remain externally
supplied; these pins are not a hermetic toolchain claim. One supervised Job
compiles two isolated lanes under one original allowance. No source adoption,
basis initialization, owner store, peer request, retry or cleanup is performed.
Failure preserves the fresh partial output; PROFILE.json is committed last.
Run with the selected Python using -I -S -B, preferably under an outer owner Job
for hard containment of this cooperative Python controller as well.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import stat
import subprocess
import sys
import time

MIB = 1024**2
ORDINARY = "software/v5/ordinary_lean/"
PACKAGE = "software/v5/ordinary_package/"
RECEIVER_MODULES = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "LocalSnapshot",
                    "BootstrapSupport", "OrdinaryExport", "BasisSnapshot", "OrdinaryWorkflowWorker")
PUBLIC_MODULES = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport")
AUTHORING_MODULES = (*PUBLIC_MODULES, "OwnerRebind", "OwnerConstruction", "OwnerUseCommand",
                    "OrdinaryExport", "SuccessorExport", "SuccessorExportCommand",
                    "PortableOwnerConstructCommand", "PortableConstructExportCommand",
                    "PortableContributionExportCommand")
CORE_PY = ("ordinary_admission.py", "ordinary_evidence.py", "ordinary_semantics.py",
           "portable_evidence.py", "portable_catalog.py", "local_catalog.py")
AUTHORING_PY = ("ordinary_contribution.py", "portable_owner_request.py", "owner_request.py",
                "portable_candidate.py", "portable_preview.py", "ordinary_preview.py")
SUPPORT_PY = ("transport/ordinary_acquisition.py", "transport/http_provider.py", "transport/clients.py",
              "discovery/formal_features.py", "discovery/discovery_store.py",
              "discovery/authenticated_index.py", "discovery/summary_wire.py", "custody/module_store.py")
ENTRY_POINTS = ("owner.py", "profile.py", "author_worker.py")
SUPERVISOR = ("commons.py", "run_stage.py", "domains.py")
FOUNDATION = {"seed": "software/assets/foundation/seed-verified.json",
              "inventory": "software/assets/foundation/seed-inventory-json.json"}
RECEIVER_SOURCES = {name: (PACKAGE+"receiver_source/OrdinaryExport.lean" if name == "OrdinaryExport"
                           else ORDINARY+name+".lean") for name in RECEIVER_MODULES}
SOURCE_FILES = tuple(sorted({PACKAGE+"build.py", ORDINARY+"ordinary_installation.py",
    *RECEIVER_SOURCES.values(), *(ORDINARY+name+".lean" for name in AUTHORING_MODULES),
    *(ORDINARY+name for name in (*CORE_PY, *AUTHORING_PY)), *FOUNDATION.values(),
    *("software/v5/"+name for name in SUPPORT_PY), *(PACKAGE+name for name in ENTRY_POINTS),
    *(PACKAGE+"supervisor/"+name for name in SUPERVISOR)}))
PRESERVED = {
    PACKAGE+"receiver_source/OrdinaryExport.lean": (8611, "ecab2be2b5ba3535547621e4d21d43ca5c8fbf23bd94cfe91d69a3916b9147bf"),
    PACKAGE+"supervisor/commons.py": (41984, "6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9"),
    PACKAGE+"supervisor/run_stage.py": (30037, "bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028"),
    PACKAGE+"supervisor/domains.py": (4934, "651db5f6bb707159c0d29dd6092174bfcebd1dc17b833fdfdacf7e2a66d8522a"),
}
PUBLIC_HASHES = {
    "OriginalExpr": "2064205249945563302b0ef4c0d3562ff1864730ee4644083a3b888433db2fb9",
    "OriginalDecl": "6a1adbab4496e351b3c66946c84a34eefc7270c214b684b44e77e10371dc89c8",
    "CheckedExtension": "60eba9cf947571f4336dd6e1f89a098b710a50f1e803a79d5691cc6292d2ae5a",
    "BootstrapSupport": "ccc6b864aba8e7239401a787930ea208e6d99653225e7565fd8a613b7db9e40c",
}
# Fixed supported named runtime profile, not a complete runtime-library census.
RUNTIME_PINS = {
    "python_runtime/python.exe": (106208, "03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38"),
    "python_runtime/python314.dll": (6778592, "fde89cdb5c2d08ae65de7ef4abca1876c93ba3796002f5ac0bf7e4d4f5a94da0"),
    "python_runtime/python3.dll": (73952, "22c6e46d8bd563cdb072650901461ef68be2ea6cb1e80af859559d9395a27e39"),
    "lean_runtime/bin/lean.exe": (83456, "a8040e2cab341c12116ab591fed9f761816f5f6b08554f6cc1680e86dfbba0a2"),
    "lean_runtime/bin/libInit_shared.dll": (28345856, "841b87dfdfb81be44d03720039d123cac50e9b3e2461ff50753f77ba2c7a0b8f"),
    "lean_runtime/bin/libc++.dll": (1659392, "8a9deaac6d2f4d2de468a544d1f35cd0dd4bcde03cda3cfb76fb9674749828d4"),
    "lean_runtime/bin/libleanshared.dll": (70414848, "002995f741bab9497ff7ecd18be469ddd5dd7d0833037d6f434084d36138f2cd"),
    "lean_runtime/bin/libleanshared_1.dll": (52662272, "15d171f935fc65a394049af4b027818891fa271821c3a5524a2fdc7688ecfa45"),
    "lean_runtime/bin/libleanshared_2.dll": (59422720, "bdbb5b6c62d4530c296a05828f1a9a0c9f52ad7da5d17efd2b1cba505468355b"),
}
COMPANIONS = (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")


def source_paths(source_root):
    """Exact source/archive selection; pure path construction, no imports or IO."""
    return tuple(Path(source_root).joinpath(*name.split("/")) for name in SOURCE_FILES)


def need(ok, code):
    if not ok:
        raise ValueError(code)


def ordinary(value, *, directory=False, fresh=False):
    """Bootstrap path check before the selected existing core can be loaded."""
    path = Path(value)
    need(path.is_absolute() and path != Path(path.anchor) and len(path.drive) == 2
         and path.drive[1] == ":" and len(str(path)) <= 32768, "PACKAGE_ABSOLUTE_LOCAL_PATH")
    need(all(part not in (".", "..") and not part.endswith((".", " "))
             and not os.path.isreserved(part) and not any(ord(c) < 32 or c in ':*?"<>|' for c in part)
             for part in path.parts[1:]), "PACKAGE_PATH_COMPONENT")
    for item in (*reversed(path.parents), path):
        try:
            info = item.lstat()
        except FileNotFoundError:
            need(item == path and fresh, "PACKAGE_MISSING_PATH")
            return path
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "PACKAGE_REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if item != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PACKAGE_PATH_KIND")
    need(not fresh, "PACKAGE_FRESH_REQUIRED")
    return path


def pin(path, check, maximum=512*MIB):
    check(); path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "PACKAGE_FILE_BOUND")
    digest, observed = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            check(); observed += len(block)
            need(observed <= size, "PACKAGE_FILE_GREW")
            digest.update(block)
    need(observed == size and path.stat().st_size == size, "PACKAGE_FILE_CHANGED_SIZE")
    return {"bytes": size, "sha256": digest.hexdigest()}


def fresh_bytes(path, raw):
    ordinary(path, fresh=True)
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def save_json(path, value):
    fresh_bytes(path, json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                                indent=2).encode("ascii"))


def public_source(raw):
    """Exact existing header transform; all post-import body bytes stay intact."""
    lines = raw.decode("utf-8").splitlines(keepends=True)
    end = 0
    while end < len(lines) and lines[end].startswith("import "):
        end += 1
    need(end > 0 and end < len(lines) and not lines[end].strip(), "EXACT_LEGACY_IMPORT_HEADER_REQUIRED")
    imports = "".join("public "+line for line in lines[:end])
    body = "".join(lines[end:]).encode("utf-8")
    generated = ("module\n\n"+imports+"\npublic section\n"+"".join(lines[end:])).encode("utf-8")
    need(generated.endswith(body), "UNCHANGED_SUPPORT_BODY_REQUIRED")
    return generated, body


def load_module(name, path):
    need(name not in sys.modules, "PACKAGE_LOADED_MODULE_COLLISION:"+name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def compile_worker(arguments):
    """Internal fixed worker; all its descendants share the parent's single Job."""
    need(len(arguments) == 6 and os.name == "nt" and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "PACKAGE_COMPILE_WORKER_PROFILE")
    lean, receiver_source, receiver_objects, authoring_source, authoring_objects = map(Path, arguments[:5])
    deadline = float(arguments[5])
    need(math.isfinite(deadline) and 0 < deadline-time.monotonic() <= 3600, "PACKAGE_COMPILE_DEADLINE")
    ordinary(lean)
    for path in (receiver_source, receiver_objects, authoring_source, authoring_objects):
        ordinary(path, directory=True)
    for source, objects, modules in ((receiver_source, receiver_objects, RECEIVER_MODULES),
                                     (authoring_source, authoring_objects, AUTHORING_MODULES)):
        need(not any(objects.iterdir()), "PACKAGE_COMPILE_FRESH_LANE")
        env = {key: value for key, value in os.environ.items()
               if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
        env["LEAN_PATH"] = str(objects)
        env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), str(lean.parent)))
        for module in modules:
            need(time.monotonic() < deadline, "PACKAGE_COMPILE_DEADLINE")
            argv = [str(lean), "-DElab.async=false", "-R", str(source), "-o",
                    str(objects/(module+".olean")), str(source/(module+".lean"))]
            result = subprocess.call(argv, cwd=source.parent, env=env, stdin=subprocess.DEVNULL,
                                     creationflags=subprocess.CREATE_NO_WINDOW)
            print(json.dumps({"lane": source.name, "module": module, "exit_code": result}), flush=True)
            need(result == 0, "PACKAGE_COMPILE_FAILED:"+module)
            need(time.monotonic() < deadline, "PACKAGE_COMPILE_DEADLINE")
    return 0


def build(source_root, python_runtime, lean_runtime, output, *, wall_seconds, cpu_seconds, memory_mib):
    started, cpu_started, worker_cpu = time.monotonic(), time.process_time(), 0.0
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, "PACKAGE_BUILDER_PYTHON_PROFILE")
    for value, low, high in ((wall_seconds, 60, 3600), (cpu_seconds, 10, 3600), (memory_mib, 256, 8192)):
        need(type(value) is int and low <= value <= high, "PACKAGE_FINITE_ALLOWANCE")
    deadline = started+wall_seconds

    def check():
        need(time.monotonic() < deadline and time.process_time()-cpu_started+worker_cpu < cpu_seconds,
             "PACKAGE_ORIGINAL_ALLOWANCE")

    root = ordinary(source_root, directory=True)
    runtimes = {"python_runtime": ordinary(python_runtime, directory=True),
                "lean_runtime": ordinary(lean_runtime, directory=True)}
    output = ordinary(output, directory=True, fresh=True)
    # A fresh build directory may be inside a repository. Only explicit selected
    # files are copied; never recurse through the source root or into this output.
    need(not root.is_relative_to(output) and all(not path.is_relative_to(output) for path in source_paths(root)),
         "PACKAGE_SOURCE_OUTPUT_OVERLAP")
    need(all(not output.is_relative_to(path) and not path.is_relative_to(output)
             for path in runtimes.values()), "PACKAGE_RUNTIME_OUTPUT_OVERLAP")
    need(not runtimes["python_runtime"].is_relative_to(runtimes["lean_runtime"])
         and not runtimes["lean_runtime"].is_relative_to(runtimes["python_runtime"]), "PACKAGE_RUNTIME_OVERLAP")
    need(Path(sys.executable).resolve() == runtimes["python_runtime"]/"python.exe", "PACKAGE_RUNNING_PYTHON")
    source_pins = {name: pin(path, check, 2*MIB) for name, path in zip(SOURCE_FILES, source_paths(root))}
    need(sum(value["bytes"] for value in source_pins.values()) <= 16*MIB, "PACKAGE_SOURCE_TOTAL")
    need(pin(Path(__file__).resolve(), check, 2*MIB) == source_pins[PACKAGE+"build.py"], "PACKAGE_RUNNING_BUILDER")
    for name, (size, digest) in PRESERVED.items():
        need(source_pins[name] == {"bytes": size, "sha256": digest}, "PACKAGE_PRESERVED_SOURCE:"+name)
    runtime_sources = {}
    for name, (size, digest) in RUNTIME_PINS.items():
        attachment, relative = name.split("/", 1)
        path = runtimes[attachment].joinpath(*relative.split("/"))
        need(pin(path, check) == {"bytes": size, "sha256": digest}, "PACKAGE_SUPPORTED_RUNTIME:"+name)
        runtime_sources[name] = path
    output.mkdir()
    work = output/"_build"
    work.mkdir()
    phase, supervision = "STAGING", None
    try:
        inputs = work/"inputs"
        inputs.mkdir()

        def mkdirs(path):
            missing = []
            while not path.exists():
                need(path.is_relative_to(output), "PACKAGE_OUTPUT_DIRECTORY")
                missing.append(path); path = path.parent
            ordinary(path, directory=True)
            for directory in reversed(missing):
                check(); ordinary(directory, directory=True, fresh=True).mkdir()

        def copy_exact(source, target, expected):
            check(); need(pin(source, check, 2*MIB) == expected, "PACKAGE_SOURCE_CHANGED")
            mkdirs(target.parent)
            with source.open("rb") as stream:
                raw = stream.read(expected["bytes"]+1)
            need(len(raw) == expected["bytes"] and hashlib.sha256(raw).hexdigest() == expected["sha256"],
                 "PACKAGE_COPY_CHANGED")
            fresh_bytes(target, raw)
            need(pin(target, check, 2*MIB) == expected, "PACKAGE_COPY_READBACK")

        for name in SOURCE_FILES:
            copy_exact(root/name, inputs/name, source_pins[name])
        save_json(work/"SOURCES.json", {"source_root": str(root), "files": source_pins,
                  "runtime_roots": {key: str(value) for key, value in runtimes.items()},
                  "runtime_files": {name: {"bytes": size, "sha256": digest}
                                    for name, (size, digest) in RUNTIME_PINS.items()}})
        # Only owner-selected staged source is imported, never a retained install.
        need(all(name[:-3] not in sys.modules for name in CORE_PY), "PACKAGE_CORE_IMPORT_COLLISION")
        installer = load_module("_dmkn_ordinary_package_assembler", inputs/ORDINARY/"ordinary_installation.py")
        A, E = installer.A, installer.E
        for filename in CORE_PY:
            need(Path(sys.modules[filename[:-3]].__file__).resolve() == inputs/ORDINARY/filename,
                 "PACKAGE_CORE_IMPORT_PATH")
        supervisor = load_module("_dmkn_ordinary_package_supervisor", inputs/PACKAGE/"supervisor/commons.py")
        load_module("domains", inputs/PACKAGE/"supervisor/domains.py")
        job = load_module("_dmkn_ordinary_package_job", inputs/PACKAGE/"supervisor/run_stage.py")
        lanes = {"receiver-source": work/"receiver-source", "receiver-objects": work/"receiver-objects",
                 "authoring-source": work/"authoring-source", "authoring-objects": output/"authoring/helpers"}
        for path in lanes.values():
            mkdirs(path)
        for name, relative in RECEIVER_SOURCES.items():
            copy_exact(inputs/relative, lanes["receiver-source"]/(name+".lean"), source_pins[relative])
        public_map = []
        for name in AUTHORING_MODULES:
            source = inputs/ORDINARY/(name+".lean")
            expected = source_pins[ORDINARY+name+".lean"]
            with source.open("rb") as stream:
                raw = stream.read(expected["bytes"]+1)
            need(len(raw) == expected["bytes"] and hashlib.sha256(raw).hexdigest() == expected["sha256"],
                 "PACKAGE_AUTHORING_SOURCE_CHANGED")
            generated, body = public_source(raw) if name in PUBLIC_MODULES else (raw, raw)
            generated_hash = hashlib.sha256(generated).hexdigest()
            if name in PUBLIC_MODULES:
                need(generated_hash == PUBLIC_HASHES[name], "PACKAGE_SELECTED_PUBLIC_SOURCE:"+name)
            fresh_bytes(lanes["authoring-source"]/(name+".lean"), generated)
            public_map.append({"module": name, "original_sha256": hashlib.sha256(raw).hexdigest(),
                               "generated_sha256": generated_hash, "body_sha256": hashlib.sha256(body).hexdigest()})
        save_json(work/"PUBLIC-SOURCE-MAP.json", public_map)
        phase = "COMPILING"
        check()
        child_wall = math.floor(deadline-time.monotonic())-25
        child_cpu = math.floor(cpu_seconds-(time.process_time()-cpu_started))-2
        need(child_wall >= 1 and child_cpu >= 1, "PACKAGE_COMPILE_REMAINING_ALLOWANCE")
        limits = supervisor.limits_checked({"wall_seconds": child_wall, "cpu_seconds": child_cpu,
            "memory_mib": memory_mib, "active_processes": 8, "stdout_bytes": 8*MIB, "stderr_bytes": 8*MIB})
        child_deadline = min(deadline-25, time.monotonic()+child_wall)
        argv = [str(runtimes["python_runtime"]/"python.exe"), "-I", "-S", "-B", str(inputs/PACKAGE/"build.py"),
                "--compile-worker", str(runtimes["lean_runtime"]/"bin/lean.exe"),
                *(str(lanes[key]) for key in ("receiver-source", "receiver-objects", "authoring-source", "authoring-objects")),
                str(child_deadline)]
        supervision = supervisor.supervise(argv, work, work/"compile", limits, job.Job)
        final_job = supervision.get("final_job")
        observed = final_job if type(final_job) is dict else supervision.get("last_observed_job")
        if type(observed) is dict and type(observed.get("cpu_seconds")) in (int, float):
            need(math.isfinite(observed["cpu_seconds"]) and observed["cpu_seconds"] >= 0, "PACKAGE_WORKER_CPU")
            worker_cpu = observed["cpu_seconds"]  # Once only; supervisor wrapper CPU is already process_time.
        save_json(work/"SUPERVISION.json", supervision)
        need(A._clean_worker(supervision) and type(final_job.get("cpu_seconds")) in (int, float),
             "PACKAGE_COMPILE_NOT_CLEAN")
        need((work/"compile/stderr.txt").stat().st_size == 0, "PACKAGE_COMPILE_DIAGNOSTICS")
        check()

        def census(directory, modules):
            allowed = {name+suffix for name in modules for suffix in COMPANIONS}
            found = {}
            with os.scandir(directory) as listing:
                for entry in listing:
                    check(); need(entry.name in allowed and entry.name not in found, "PACKAGE_COMPILED_EXTRA")
                    found[entry.name] = pin(Path(entry.path), check, 128*MIB)
            need({name+".olean" for name in modules} <= set(found), "PACKAGE_COMPILED_MISSING")
            need(sum(row["bytes"] for row in found.values()) <= 256*MIB, "PACKAGE_COMPILED_TOTAL")
            return found

        receiver_outputs = census(lanes["receiver-objects"], RECEIVER_MODULES)
        authoring_outputs = census(lanes["authoring-objects"], AUTHORING_MODULES)
        save_json(work/"COMPILED-FILES.json", {"receiver": receiver_outputs, "authoring": authoring_outputs})
        phase = "ASSEMBLING"
        files = {}

        def selected(logical, path, expected=None):
            actual = pin(path, check)
            need(expected is None or actual == expected, "PACKAGE_SELECTED_FILE_CHANGED")
            files[logical] = {"source": str(path), **actual}

        roles = {"python": "python_runtime/python.exe", "python_dll": "python_runtime/python314.dll",
                 "python_stable_dll": "python_runtime/python3.dll", "lean": "lean_runtime/bin/lean.exe",
                 "worker": "lean-src/OrdinaryWorkflowWorker.lean", "seed": "foundation/seed.json",
                 "inventory": "foundation/inventory.json", "supervisor": "supervisor/commons.py",
                 "job": "supervisor/run_stage.py", "domains": "supervisor/domains.py"}
        roles.update({role: "py/"+name for role, name in A.CORE_NAMES.items()})
        for name in CORE_PY:
            selected("py/"+name, inputs/ORDINARY/name, source_pins[ORDINARY+name])
        for name in SUPERVISOR:
            selected("supervisor/"+name, inputs/PACKAGE/"supervisor"/name, source_pins[PACKAGE+"supervisor/"+name])
        for role, relative in FOUNDATION.items():
            selected(roles[role], inputs/relative, source_pins[relative])
        for name in RECEIVER_MODULES:
            selected("lean-src/"+name+".lean", lanes["receiver-source"]/(name+".lean"), source_pins[RECEIVER_SOURCES[name]])
            selected("lean-lib/"+name+".olean", lanes["receiver-objects"]/(name+".olean"), receiver_outputs[name+".olean"])
        for name, path in runtime_sources.items():
            size, digest = RUNTIME_PINS[name]
            selected(name, path, {"bytes": size, "sha256": digest})
        groups = {
            "kernel_support": {name for name in files if name.startswith("lean_runtime/")},
            "adapter_support": {name for name in files if name.startswith(("lean-src/", "lean-lib/"))},
            "basis_receiver_support": {roles["seed"], roles["inventory"]} |
                {folder+name+suffix for folder, suffix in (("lean-src/", ".lean"), ("lean-lib/", ".olean"))
                 for name in ("BootstrapSupport", "BasisSnapshot")},
            "snapshot_support": {"lean-src/LocalSnapshot.lean", "lean-lib/LocalSnapshot.olean"},
            "controller_support": {roles[role] for role in (*A.CORE_NAMES, "python", "python_dll",
                                                           "python_stable_dll", "supervisor", "job", "domains")},
        }
        plan = {"schema": installer.PLAN_SCHEMA, "roles": roles,
                "compiled_dirs": {"lean-lib": sorted(name+".olean" for name in RECEIVER_MODULES)},
                "support_groups": {key: sorted(value) for key, value in groups.items()}, "files": files}
        plan_raw = E.canonical_json(plan)
        fresh_bytes(work/"INSTALLATION-PLAN.json", plan_raw)
        check()
        installation = installer.assemble(output/"installation", plan_raw, hashlib.sha256(plan_raw).hexdigest(),
                                          runtime_roots=runtimes, deadline=deadline)
        check()
        phase = "AUXILIARY_PAYLOAD"
        auxiliary = {"authoring/helpers/"+name: value for name, value in authoring_outputs.items()}
        copies = {"authoring/py/"+name: ORDINARY+name for name in AUTHORING_PY}
        copies.update({"support/"+name: "software/v5/"+name for name in SUPPORT_PY})
        copies.update({name: PACKAGE+name for name in ENTRY_POINTS})
        for logical, relative in copies.items():
            copy_exact(inputs/relative, output/logical, source_pins[relative])
            auxiliary[logical] = source_pins[relative]
        need(sum(row["bytes"] for row in auxiliary.values()) <= 512*MIB, "PACKAGE_AUXILIARY_TOTAL")
        phase = "FINAL_VERIFY"
        for name, expected in source_pins.items():
            need(pin(root/name, check, 2*MIB) == expected and pin(inputs/name, check, 2*MIB) == expected,
                 "PACKAGE_INPUT_CHANGED")
        for logical, expected in auxiliary.items():
            need(pin(output/logical, check, 128*MIB) == expected, "PACKAGE_AUXILIARY_CHANGED")
        need(census(lanes["authoring-objects"], AUTHORING_MODULES) == authoring_outputs,
             "PACKAGE_AUTHORING_CENSUS_CHANGED")
        # Verify every assembled file and named runtime once more before the final marker.
        for logical, row in files.items():
            path = runtime_sources[logical] if logical in runtime_sources else output/"installation"/logical
            need(pin(path, check) == {key: row[key] for key in ("bytes", "sha256")}, "PACKAGE_INSTALLED_CHANGED")
        need(pin(output/"installation/INSTALLATION.json", check, 2*MIB)["sha256"] == installation["manifest_sha256"],
             "PACKAGE_INSTALLATION_MANIFEST_CHANGED")
        descriptor = {"schema": "DMKN_ORDINARY_OWNER_PROFILE_V1",
                      "installation_manifest_sha256": installation["manifest_sha256"],
                      "helper_paths": ["authoring/helpers"], "author_worker": "author_worker.py", "files": auxiliary}
        descriptor_raw = E.canonical_json(descriptor)
        need(len(descriptor_raw) <= 2*MIB, "PACKAGE_PROFILE_BOUND")
        profile_sha = hashlib.sha256(descriptor_raw).hexdigest()
        result = {"status": "BUILT_NOT_ADOPTED", "profile_sha256": profile_sha, "installation": installation,
                  "receiver_modules": list(RECEIVER_MODULES), "authoring_modules": list(AUTHORING_MODULES),
                  "auxiliary_files": len(auxiliary), "worker_cpu_seconds": worker_cpu,
                  "controller_cpu_seconds": time.process_time()-cpu_started,
                  "wall_seconds_before_profile_commit": time.monotonic()-started,
                  "claim": "SOURCE_BUILD_AND_ASSEMBLY_NOT_BASIS_OR_OWNER_ACCEPTANCE"}
        save_json(work/"BUILD-RESULT.json", result)
        fresh_bytes(output/".PROFILE.pending", descriptor_raw)
        check(); ordinary(output/"PROFILE.json", fresh=True)
        (output/".PROFILE.pending").rename(output/"PROFILE.json")
        return result
    except BaseException as error:
        # Failure logging is best-effort, never a new allowance or cleanup/retry.
        try:
            save_json(work/"BUILD-FAILURE.json", {"phase": phase, "error_type": type(error).__name__,
                "error": str(error)[:2000], "worker_cpu_seconds": worker_cpu,
                "worker_cpu_complete": supervision is not None and type(supervision.get("final_job")) is dict
                    and type(supervision["final_job"].get("cpu_seconds")) in (int, float),
                "controller_cpu_seconds": time.process_time()-cpu_started, "wall_seconds": time.monotonic()-started,
                "retention": "PARTIAL_OUTPUT_PRESERVED_NO_RETRY_NO_MATHEMATICAL_ACCEPTANCE"})
        except BaseException:
            pass
        raise


def main():
    if sys.argv[1:2] == ["--compile-worker"]:
        return compile_worker(sys.argv[2:])
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("source-root", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+flag, required=True)
    for flag in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+flag, required=True, type=int)
    args = parser.parse_args()
    result = build(args.source_root, args.python_runtime, args.lean_runtime, args.output,
                   wall_seconds=args.wall_seconds, cpu_seconds=args.cpu_seconds, memory_mib=args.memory_mib)
    print(json.dumps(result, sort_keys=True, allow_nan=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

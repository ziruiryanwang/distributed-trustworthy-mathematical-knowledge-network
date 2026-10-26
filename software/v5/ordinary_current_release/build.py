"""Build the current ordinary package from its one exact release selection.

Narrow successor of ordinary_bounded_operations/build.py. Preserve its receiver,
authoring, query and missing-import/baseline-exporter compilation lanes exactly.
The release map directly selects current sources and the complete output-role
partition. No historical overlay, installation, experiment output, fixed native
binary hash or accepted owner state is an input. Fresh native output determines
the installation and owner-profile identities; prebuilt pins do not determine
fresh-build identities.

Windows/Python 3.14.6/Lean 4.34.0 and immutable owner-selected storage are
premises. Run with the selected Python -I -S -B. This controller cooperatively
accounts for staging, three supervised child Jobs and final copying under one
allowance. An enclosing owner Job can additionally contain the controller.
No state, download, source adoption, retry or mathematical acceptance occurs.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import time

MIB = 1024**2
PREFIX = "software/v5/ordinary_current_release/"
BUILDER = "software/v5/ordinary_package/build.py"
BUILDER_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
MAP_SHA = "821796aa5b4996edd3f34babdb3be186d8321e0b3b4208b1e3f18705400caf78"
NATIVE_SHARED = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport",
                 "OrdinaryExport")
NATIVE_PROGRAMS = ("MissingImportExporter", "BaselineExporter")
NATIVE = NATIVE_SHARED + NATIVE_PROGRAMS
QUERY = "OwnerQueryCommand"
DOCUMENTS = {"README.md", "PRODUCER.md", "LAUNCHER.md", "RECEIVE-POLICY.md",
             "BOUNDED-TRANSPORT.md", "EXECUTION-TRUST.md", "CONTACTS.md", "SPARSE-SEARCH.md"}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def bootstrap(path):
    """Only the fixed previously selected builder is executed at bootstrap."""
    need(path.is_absolute() and path.is_file() and path.stat().st_size <= 2*MIB,
         "DISTRIBUTION_BUILDER_PATH")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == BUILDER_SHA, "DISTRIBUTION_BASE_BUILDER_PIN")
    name = "_dmkn_distribution_preserved_builder"
    need(name not in sys.modules, "DISTRIBUTION_PRELOADED_BUILDER")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def relative(name):
    path = PurePosixPath(name)
    need(type(name) is str and path.as_posix() == name and not path.is_absolute()
         and path.parts and all(part not in ("", ".", "..") and
             not part.endswith((".", " ")) and not os.path.isreserved(part) and
             not any(ord(c) < 32 or c in ':*?"<>|\\' for c in part) for part in path.parts),
         "DISTRIBUTION_RELATIVE_PATH")
    return path


def legacy_view(raw):
    """Exact run_missing_import_build.py legacy_view, without its old paths."""
    lines = raw.splitlines(keepends=True)
    need(lines and lines[0].strip() == b"module", "EXPECTED_MODULE_HEADER")
    output, sections, imports = [], 0, 0
    for line in lines[1:]:
        if line.strip() == b"public section":
            sections += 1
        elif line.startswith(b"public import "):
            output.append(line[len(b"public "):]); imports += 1
        else:
            output.append(line)
    need(sections == 1 and imports == 3, "EXACT_PUBLIC_HEADER_TRANSFORM")
    return b"".join(output)


def extractor_worker(arguments):
    """Fixed sequential compiler lane; its parent Job owns all descendants."""
    need(len(arguments) == 4 and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "DISTRIBUTION_EXTRACTOR_WORKER_PROFILE")
    runtime, source, objects = map(Path, arguments[:3])
    deadline = float(arguments[3])
    need(math.isfinite(deadline) and 0 < deadline-time.monotonic() <= 3600 and
         all(path.is_absolute() and path.is_dir() for path in (runtime, source, objects))
         and not any(objects.iterdir()), "DISTRIBUTION_EXTRACTOR_FRESH_LANE")
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith(("LEAN", "PYTHON")) and k.upper() != "PATH"}
    env["LEAN_PATH"] = str(objects)
    env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), str(runtime/"bin")))

    def run(label, argv):
        need(time.monotonic() < deadline, "DISTRIBUTION_EXTRACTOR_DEADLINE")
        code = subprocess.call(argv, cwd=source.parent, env=env, stdin=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        print(json.dumps({"phase": label, "exit_code": code}), flush=True)
        need(code == 0, "DISTRIBUTION_EXTRACTOR_FAILED:"+label)
        need(time.monotonic() < deadline, "DISTRIBUTION_EXTRACTOR_DEADLINE")

    for name in NATIVE:
        run(name+"-codegen", [str(runtime/"bin/lean.exe"), "-R", str(source),
            "-o", str(objects/(name+".olean")), "-c", str(objects/(name+".c")),
            str(source/(name+".lean"))])
        run(name+"-object", [str(runtime/"bin/leanc.exe"), "-c", "-O0",
            str(objects/(name+".c")), "-o", str(objects/(name+".o"))])
    # Each program defines main. Share support objects, never link both mains.
    for program in NATIVE_PROGRAMS:
        run(program+"-link", [str(runtime/"bin/leanc.exe"), "-leanshared",
            *(str(objects/(name+".o")) for name in (*NATIVE_SHARED, program)),
            "-o", str(objects/(program+".exe"))])
    return 0


def query_worker(arguments):
    """One new local command compilation, using already built helper modules."""
    need(len(arguments) == 5 and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "DISTRIBUTION_QUERY_WORKER_PROFILE")
    runtime, source, helpers, objects = map(Path, arguments[:4])
    deadline = float(arguments[4])
    need(math.isfinite(deadline) and 0 < deadline-time.monotonic() <= 3600 and
         all(path.is_absolute() and path.is_dir() for path in (runtime, helpers, objects)) and
         source.is_absolute() and source.is_file() and source.name == QUERY+".lean" and
         not any(objects.iterdir()), "DISTRIBUTION_QUERY_FRESH_LANE")
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith(("LEAN", "PYTHON")) and k.upper() != "PATH"}
    env["LEAN_PATH"] = os.pathsep.join((str(runtime/"lib/lean"), str(helpers)))
    env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), str(runtime/"bin")))
    code = subprocess.call([str(runtime/"bin/lean.exe"), "-DElab.async=false",
        "-R", str(source.parent), "-o", str(objects/(QUERY+".olean")), str(source)],
        cwd=source.parent, env=env, stdin=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW)
    print(json.dumps({"phase": "query-command", "exit_code": code}), flush=True)
    need(code == 0, "DISTRIBUTION_QUERY_COMPILE_FAILED")
    need(time.monotonic() < deadline, "DISTRIBUTION_QUERY_DEADLINE")
    return 0


def build(args):
    started, cpu_started = time.monotonic(), time.process_time()
    worker_cpu, cpu_complete, stages = 0.0, True, []
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "DISTRIBUTION_PYTHON_PROFILE")
    for value, low, high in ((args.wall_seconds, 120, 3600),
                            (args.cpu_seconds, 100, 3600), (args.memory_mib, 256, 8192)):
        need(type(value) is int and low <= value <= high, "DISTRIBUTION_FINITE_ALLOWANCE")
    deadline = started+args.wall_seconds

    def check():
        need(time.monotonic() < deadline and
             time.process_time()-cpu_started+worker_cpu < args.cpu_seconds,
             "DISTRIBUTION_ORIGINAL_ALLOWANCE")

    B = bootstrap(Path(args.source_root)/BUILDER)
    root = B.ordinary(args.source_root, directory=True)
    runtimes = {"python_runtime": B.ordinary(args.python_runtime, directory=True),
                "lean_runtime": B.ordinary(args.lean_runtime, directory=True)}
    output = B.ordinary(args.output, directory=True, fresh=True)
    need(not root.is_relative_to(output), "DISTRIBUTION_SOURCE_OUTPUT_OVERLAP")
    need(all(not output.is_relative_to(path) and not path.is_relative_to(output)
             for path in runtimes.values()), "DISTRIBUTION_RUNTIME_OUTPUT_OVERLAP")
    need(not runtimes["python_runtime"].is_relative_to(runtimes["lean_runtime"]) and
         not runtimes["lean_runtime"].is_relative_to(runtimes["python_runtime"]),
         "DISTRIBUTION_RUNTIME_OVERLAP")
    need(Path(sys.executable).resolve() == runtimes["python_runtime"]/"python.exe",
         "DISTRIBUTION_RUNNING_PYTHON")
    map_pin = B.pin(root/PREFIX/"release.json", check, 2*MIB)
    need(map_pin["sha256"] == MAP_SHA, "DISTRIBUTION_SOURCE_MAP_PIN")
    with (root/PREFIX/"release.json").open("rb") as stream:
        map_raw = stream.read(2*MIB+1)
    need(hashlib.sha256(map_raw).hexdigest() == MAP_SHA, "DISTRIBUTION_SOURCE_MAP_CHANGED")
    release = json.loads(map_raw)
    need(release["schema"] == "DMKN_ORDINARY_CURRENT_RELEASE_SELECTION_V1",
         "DISTRIBUTION_SOURCE_MAP_SCHEMA")
    mapping, counts = release["build"], release["counts"]
    sources, copies, lanes = mapping["sources"], mapping["copies"], mapping["lanes"]
    source_union = set(B.SOURCE_FILES) | set(copies.values()) | {
        row["source"] for lane in lanes.values() for row in lane}
    need(set(sources) == source_union and
         len(sources) == counts["source_inputs"] and len(copies) == counts["direct_copies"] and
         mapping["base_inputs"] == list(B.SOURCE_FILES) and
         len(mapping["base_inputs"]) == counts["base_inputs"] and
         mapping["base_builder"] == {"source": BUILDER, **sources[BUILDER]} and
         sources[BUILDER]["sha256"] == BUILDER_SHA and
         len({name.casefold() for name in sources}) == len(sources) and
         len({name.casefold() for name in copies}) == len(copies), "DISTRIBUTION_SOURCE_CENSUS")
    for name in (*sources, *copies):
        relative(name)
    need(all(name.startswith(("software/v5/", "software/assets/foundation/")) and
             not (root/name).is_relative_to(output) for name in sources) and
         set(copies.values()) <= set(sources), "DISTRIBUTION_SOURCE_SCOPE")
    need(tuple(row["module"] for row in lanes["receiver"]) == B.RECEIVER_MODULES and
         tuple(row["module"] for row in lanes["authoring"]) == B.AUTHORING_MODULES and
         tuple(row["module"] for row in lanes["extractor"]) == NATIVE and
         tuple(mapping["authoring_suffixes"]) == B.COMPANIONS, "DISTRIBUTION_MODULE_MAP")
    need(lanes["query"] == [{"module": QUERY,
        "source": "software/v5/ordinary_formal_query/OwnerQueryCommand02.lean",
        "transform": "identity", "transformed_sha256":
            sources["software/v5/ordinary_formal_query/OwnerQueryCommand02.lean"]["sha256"]}],
        "DISTRIBUTION_QUERY_SOURCE_MAP")
    need(mapping["native_outputs"] == {
        "MissingImportExporter": "authoring/bin/MissingImportExporter.exe",
        "BaselineExporter": "authoring/bin/BaselineExporter.exe"} and
         set(mapping["documentation"]) == DOCUMENTS and
         all(copies[name] == mapping["documentation"][name] for name in DOCUMENTS),
         "DISTRIBUTION_NATIVE_AND_DOCUMENT_MAP")
    # Derive each disjoint output role from the unchanged compiler lanes.
    # Prebuilt identities are deliberately not used to accept fresh native bytes.
    receiver_roles = {"installation/lean-lib/"+row["module"]+".olean"
                      for row in lanes["receiver"]}
    authoring_roles = {"authoring/helpers/"+row["module"]+suffix
                      for row in lanes["authoring"] for suffix in B.COMPANIONS}
    query_roles = {"authoring/helpers/"+row["module"]+suffix
                  for row in lanes["query"] for suffix in B.COMPANIONS}
    extractor_roles = set(mapping["native_outputs"].values())
    role_groups = (set(copies), receiver_roles, authoring_roles, query_roles,
                   extractor_roles, {"installation/INSTALLATION.json"})
    payload_roles = set().union(*role_groups)
    payload_count = len(payload_roles)
    native_roles = authoring_roles | query_roles | extractor_roles
    auxiliary_roles = {name for name in payload_roles
                       if not name.startswith("installation/") and name not in DOCUMENTS}
    noncompiled_roles = auxiliary_roles - native_roles
    need(sum(len(group) for group in role_groups) == payload_count and
         len({name.casefold() for name in payload_roles}) == payload_count and
         set(release["prebuilt"]["files"]) == payload_roles | {"PROFILE.json"} and
         set(mapping["native_roles"]) == native_roles and
         len(mapping["native_roles"]) == len(native_roles) and
         set(mapping["noncompiled_roles"]) == noncompiled_roles and
         all(mapping["noncompiled_roles"][name] == sources[copies[name]]
             for name in noncompiled_roles), "DISTRIBUTION_RELEASE_ROLE_CLOSURE")
    actual_counts = {
        "installed_direct": sum(name.startswith("installation/") for name in copies),
        "auxiliary_direct": len(noncompiled_roles), "receiver_generated": len(receiver_roles),
        "authoring_generated": len(authoring_roles), "query_generated": len(query_roles),
        "extractor_generated": len(extractor_roles), "installation_manifest": 1,
        "profile_manifest": 1, "payloads_excluding_profile": payload_count,
        "package_files": payload_count+1, "auxiliary_payloads": len(auxiliary_roles),
        "documentation": len(DOCUMENTS)}
    need(all(counts[name] == value for name, value in actual_counts.items()) and
         set(copies) == ({name for name in copies if name.startswith("installation/")} |
                        noncompiled_roles | DOCUMENTS), "DISTRIBUTION_RELEASE_COUNTS")
    for name in payload_roles:
        relative(name)
    own_pin = B.pin(root/PREFIX/"build.py", check, 2*MIB)
    need(B.pin(Path(__file__).resolve(), check, 2*MIB) == own_pin,
         "DISTRIBUTION_RUNNING_SOURCE")
    source_pins = dict(sources, **{PREFIX+"build.py": own_pin, PREFIX+"release.json": map_pin})
    for name, expected in source_pins.items():
        need(B.pin(root/name, check, 2*MIB) == expected, "DISTRIBUTION_SELECTED_SOURCE:"+name)
    need(sum(row["bytes"] for row in source_pins.values()) <= 16*MIB,
         "DISTRIBUTION_SOURCE_TOTAL")
    runtime_pins = mapping["runtime_pins"]
    base_runtime_pins = {name: {"bytes": size, "sha256": digest}
                         for name, (size, digest) in B.RUNTIME_PINS.items()}
    need(len(runtime_pins) == counts["runtime_pins"] and
         set(base_runtime_pins) <= set(runtime_pins) and
         all(runtime_pins[name] == expected for name, expected in base_runtime_pins.items()),
         "DISTRIBUTION_RUNTIME_CLOSURE")
    runtime_paths = {}
    for name, expected in runtime_pins.items():
        attachment, suffix = name.split("/", 1)
        runtime_paths[name] = runtimes[attachment]/relative(suffix)
        need(B.pin(runtime_paths[name], check) == expected, "DISTRIBUTION_RUNTIME_PIN:"+name)
    output.mkdir()
    work, package = output/"_build", output/"package"
    work.mkdir()
    phase = "STAGING"

    def mkdirs(path):
        pending = []
        while not path.exists():
            need(path.is_relative_to(output), "DISTRIBUTION_OUTPUT_DIRECTORY")
            pending.append(path); path = path.parent
        B.ordinary(path, directory=True)
        for item in reversed(pending):
            check(); B.ordinary(item, directory=True, fresh=True).mkdir()

    def copy_exact(source, target, expected):
        need(B.pin(source, check, 128*MIB) == expected, "DISTRIBUTION_COPY_INPUT")
        mkdirs(target.parent); B.ordinary(target, fresh=True)
        digest, size = hashlib.sha256(), 0
        with source.open("rb") as incoming, target.open("xb") as outgoing:
            while block := incoming.read(MIB):
                check(); size += len(block)
                need(size <= expected["bytes"], "DISTRIBUTION_COPY_GREW")
                outgoing.write(block); digest.update(block)
            outgoing.flush(); os.fsync(outgoing.fileno())
        need(size == expected["bytes"] and digest.hexdigest() == expected["sha256"] and
             B.pin(target, check, 128*MIB) == expected, "DISTRIBUTION_COPY_CHANGED")

    def read_json(path):
        B.pin(path, check, 2*MIB)
        with path.open("rb") as stream:
            return json.loads(stream.read(2*MIB+1))

    try:
        inputs = work/"inputs"
        inputs.mkdir()
        for name, expected in source_pins.items():
            copy_exact(root/name, inputs/name, expected)
        B.save_json(work/"SOURCES.json", {"source_root": str(root), "files": source_pins,
            "runtime_roots": {name: str(path) for name, path in runtimes.items()},
            "runtime_files": runtime_pins, "original_allowance": {
                "wall_seconds": args.wall_seconds, "cpu_seconds": args.cpu_seconds,
                "memory_mib": args.memory_mib}})
        need(all(name[:-3] not in sys.modules for name in B.CORE_PY),
             "DISTRIBUTION_CORE_IMPORT_COLLISION")
        installer = B.load_module("_dmkn_distribution_installer", inputs/B.ORDINARY/"ordinary_installation.py")
        A, E, S = installer.A, installer.E, installer.S
        need(all(Path(sys.modules[name[:-3]].__file__).resolve() == inputs/B.ORDINARY/name
                 for name in B.CORE_PY), "DISTRIBUTION_CORE_IMPORT_PATH")
        supervisor = B.load_module("_dmkn_distribution_supervisor", inputs/B.PACKAGE/"supervisor/commons.py")
        B.load_module("domains", inputs/B.PACKAGE/"supervisor/domains.py")
        jobs = B.load_module("_dmkn_distribution_job", inputs/B.PACKAGE/"supervisor/run_stage.py")

        def child_grant():
            check()
            # Preserve the existing supervisor's maximum 60 controller CPU
            # seconds and 20 seconds cleanup, plus final-copy slack. Unused
            # reserve remains available, never becomes a renewed allowance.
            grant = {"wall_seconds": math.floor(deadline-time.monotonic())-25,
                     "cpu_seconds": math.floor(args.cpu_seconds-worker_cpu-
                         (time.process_time()-cpu_started))-62,
                     "memory_mib": args.memory_mib, "active_processes": 8,
                     "stdout_bytes": 8*MIB, "stderr_bytes": 8*MIB}
            return supervisor.limits_checked(grant)

        def run_child(name, argv, grant):
            nonlocal worker_cpu, cpu_complete
            check()
            # Reserve first: an exception before a final sample must never
            # make the unmeasured child appear free in the failure receipt.
            worker_cpu += grant["cpu_seconds"]; cpu_complete = False
            record = supervisor.supervise(argv, work, work/name, grant, jobs.Job)
            final = record.get("final_job")
            observed = final.get("cpu_seconds") if type(final) is dict else None
            known = type(observed) in (int, float) and math.isfinite(observed) and observed >= 0
            if known:
                worker_cpu += observed-grant["cpu_seconds"]; cpu_complete = True
            stage = {"name": name, "limits": grant,
                     "charged_cpu_seconds": observed if known else grant["cpu_seconds"],
                     "cpu_complete": known, "supervision": record}
            stages.append(stage)
            B.save_json(work/(name+"-SUPERVISION.json"), stage)
            need(known and A._clean_worker(record), "DISTRIBUTION_CHILD_NOT_CLEAN:"+name)
            need((work/name/"stderr.txt").stat().st_size == 0,
                 "DISTRIBUTION_CHILD_DIAGNOSTICS:"+name)
            check()

        phase = "BASE_BUILD"
        grant = child_grant()
        inner_wall, inner_cpu = grant["wall_seconds"]-25, grant["cpu_seconds"]-2
        need(inner_wall >= 60 and inner_cpu >= 10, "DISTRIBUTION_BASE_REMAINING_ALLOWANCE")
        base = work/"base"
        argv = [str(runtimes["python_runtime"]/"python.exe"), "-I", "-S", "-B", str(inputs/BUILDER),
                "--source-root", str(inputs), "--python-runtime", str(runtimes["python_runtime"]),
                "--lean-runtime", str(runtimes["lean_runtime"]), "--output", str(base),
                "--wall-seconds", str(inner_wall), "--cpu-seconds", str(inner_cpu),
                "--memory-mib", str(args.memory_mib)]
        run_child("base-job", argv, grant)
        base_result = read_json(base/"_build/BUILD-RESULT.json")
        need(base_result["status"] == "BUILT_NOT_ADOPTED", "DISTRIBUTION_BASE_RESULT")
        inner = read_json(base/"_build/SUPERVISION.json")
        need(A._clean_worker(inner) and
             type(inner["final_job"].get("cpu_seconds")) in (int, float) and
             math.isfinite(inner["final_job"]["cpu_seconds"]) and
             inner["final_job"]["cpu_seconds"] >= 0 and
             (base/"_build/compile/stderr.txt").stat().st_size == 0,
             "DISTRIBUTION_BASE_NESTED_JOB_NOT_CLEAN")
        # Charge the inclusive outer base Job once, never its nested worker again.
        public = read_json(base/"_build/PUBLIC-SOURCE-MAP.json")
        need(len(public) == 13 and all(observed["module"] == row["module"] and
             observed["original_sha256"] == sources[row["source"]]["sha256"] and
             observed["generated_sha256"] == row["transformed_sha256"]
             for observed, row in zip(public, lanes["authoring"])), "DISTRIBUTION_PUBLIC_TRANSFORMS")

        phase = "EXTRACTOR_BUILD"
        native_source, native_objects = work/"extractor-source", work/"extractor-objects"
        native_source.mkdir(); native_objects.mkdir()
        transformed = {}
        for row in lanes["extractor"]:
            check()
            with (inputs/row["source"]).open("rb") as stream:
                raw = stream.read(2*MIB+1)
            need(hashlib.sha256(raw).hexdigest() == sources[row["source"]]["sha256"],
                 "DISTRIBUTION_NATIVE_INPUT")
            view = legacy_view(raw) if row["transform"] == "legacy_view_v1" else raw
            need(hashlib.sha256(view).hexdigest() == row["transformed_sha256"],
                 "DISTRIBUTION_NATIVE_TRANSFORM")
            path = native_source/(row["module"]+".lean")
            B.fresh_bytes(path, view); transformed[path.name] = B.pin(path, check, 2*MIB)
        B.save_json(work/"EXTRACTOR-SOURCE-MAP.json", transformed)
        grant = child_grant()
        argv = [str(runtimes["python_runtime"]/"python.exe"), "-I", "-S", "-B",
                str(inputs/PREFIX/"build.py"), "--extractor-worker", str(runtimes["lean_runtime"]),
                str(native_source), str(native_objects),
                str(min(deadline-25, time.monotonic()+grant["wall_seconds"]))]
        run_child("extractor-job", argv, grant)
        native_outputs = {name+suffix: B.pin(native_objects/(name+suffix), check, 128*MIB)
                          for name in NATIVE for suffix in (".olean", ".c", ".o")}
        for program in NATIVE_PROGRAMS:
            native_outputs[program+".exe"] = B.pin(native_objects/(program+".exe"), check, 128*MIB)
        B.save_json(work/"EXTRACTOR-OUTPUTS.json", native_outputs)

        phase = "QUERY_COMMAND_BUILD"
        query_row = lanes["query"][0]
        query_source = work/"query-source"/(QUERY+".lean")
        copy_exact(inputs/query_row["source"], query_source, sources[query_row["source"]])
        query_objects = work/"query-objects"
        query_objects.mkdir()
        grant = child_grant()
        argv = [str(runtimes["python_runtime"]/"python.exe"), "-I", "-S", "-B",
                str(inputs/PREFIX/"build.py"), "--query-worker", str(runtimes["lean_runtime"]),
                str(query_source), str(base/"authoring/helpers"), str(query_objects),
                str(min(deadline-25, time.monotonic()+grant["wall_seconds"]))]
        run_child("query-job", argv, grant)
        query_outputs = {QUERY+suffix: B.pin(query_objects/(QUERY+suffix), check, 128*MIB)
                         for suffix in B.COMPANIONS}
        need({path.name for path in query_objects.iterdir()} == set(query_outputs) and
             all(pin["bytes"] > 0 for pin in query_outputs.values()),
             "DISTRIBUTION_QUERY_EXACT_COMPANIONS")
        B.save_json(work/"QUERY-OUTPUTS.json", query_outputs)

        phase = "ASSEMBLING"
        compiled = read_json(base/"_build/COMPILED-FILES.json")
        expected_authoring = {name+suffix for name in B.AUTHORING_MODULES for suffix in B.COMPANIONS}
        need(set(compiled["authoring"]) == expected_authoring, "DISTRIBUTION_ALL_65_AUTHORING_PARTS")
        manifest_path = base/"installation/INSTALLATION.json"
        manifest_pin = B.pin(manifest_path, check, 2*MIB)
        need(manifest_pin["sha256"] == base_result["installation"]["manifest_sha256"],
             "DISTRIBUTION_BASE_MANIFEST")
        manifest = read_json(manifest_path)
        installation_pins = {name[len("installation/"):]: sources[source]
                             for name, source in copies.items() if name.startswith("installation/")}
        need(len(installation_pins) == actual_counts["installed_direct"],
             "DISTRIBUTION_INSTALLED_DIRECT_CENSUS")
        installation_pins.update({"lean-lib/"+name+".olean": compiled["receiver"][name+".olean"]
                                  for name in B.RECEIVER_MODULES})
        installation_pins.update({name: runtime_pins[name] for name in B.RUNTIME_PINS})
        need(manifest["files"] == installation_pins, "DISTRIBUTION_INSTALLATION_EXACT_MAP")
        implementation_raw = E.canonical_json(manifest["implementation"])
        implementation = S.read_implementation(implementation_raw)
        need(all(implementation[field] == A.support_digest(field, manifest)
                 for field in installer.P.SUPPORT_FIELDS), "DISTRIBUTION_ACTUAL_SUPPORT_DIGESTS")
        implementation_id = S.implementation_id(implementation_raw)
        need(implementation_id == base_result["installation"]["implementation_id"],
             "DISTRIBUTION_ACTUAL_IMPLEMENTATION_ID")
        selected = {name: (inputs/source, sources[source]) for name, source in copies.items()}
        for name in B.RECEIVER_MODULES:
            logical = "installation/lean-lib/"+name+".olean"
            selected[logical] = (base/logical, compiled["receiver"][name+".olean"])
        for name in sorted(expected_authoring):
            logical = "authoring/helpers/"+name
            selected[logical] = (base/logical, compiled["authoring"][name])
        for name, expected in query_outputs.items():
            selected["authoring/helpers/"+name] = (query_objects/name, expected)
        for program, logical in mapping["native_outputs"].items():
            selected[logical] = (native_objects/(program+".exe"), native_outputs[program+".exe"])
        selected["installation/INSTALLATION.json"] = (manifest_path, manifest_pin)
        need(set(selected) == payload_roles and len(selected) == payload_count and
             len({name.casefold() for name in selected}) == payload_count and
             sum(pin["bytes"] for _, pin in selected.values()) <= 768*MIB,
             "DISTRIBUTION_FINAL_CENSUS")
        for name, (source, expected) in sorted(selected.items()):
            relative(name); copy_exact(source, package/name, expected)

        phase = "FINAL_VERIFY"
        for name, expected in source_pins.items():
            need(B.pin(root/name, check, 2*MIB) == expected and
                 B.pin(inputs/name, check, 2*MIB) == expected, "DISTRIBUTION_SOURCE_CHANGED")
        for name, expected in runtime_pins.items():
            need(B.pin(runtime_paths[name], check) == expected, "DISTRIBUTION_RUNTIME_CHANGED")
        for name, expected in transformed.items():
            need(B.pin(native_source/name, check, 2*MIB) == expected, "DISTRIBUTION_VIEW_CHANGED")
        need(B.pin(query_source, check, 2*MIB) == sources[query_row["source"]],
             "DISTRIBUTION_QUERY_SOURCE_CHANGED")
        for name, (source, expected) in selected.items():
            need(B.pin(source, check, 128*MIB) == expected and
                 B.pin(package/name, check, 128*MIB) == expected, "DISTRIBUTION_PAYLOAD_CHANGED")
        # Exact package census only; never traverse the checkout or old outputs.
        actual, pending = set(), [package]
        while pending:
            folder = B.ordinary(pending.pop(), directory=True)
            with os.scandir(folder) as listing:
                for entry in listing:
                    check(); path = Path(entry.path)
                    if entry.is_dir(follow_symlinks=False):
                        need(len(path.relative_to(package).parts) <= 4, "DISTRIBUTION_CENSUS_DEPTH")
                        pending.append(B.ordinary(path, directory=True))
                    else:
                        actual.add(B.ordinary(path).relative_to(package).as_posix())
                        need(len(actual) <= payload_count, "DISTRIBUTION_CENSUS_BOUND")
        need(actual == set(selected), "DISTRIBUTION_EXACT_PACKAGE_CENSUS")
        auxiliary = {name: pin for name, (_, pin) in selected.items()
                     if not name.startswith("installation/") and name not in DOCUMENTS}
        need(set(auxiliary) == auxiliary_roles and
             all(auxiliary[name] == mapping["noncompiled_roles"][name] for name in noncompiled_roles) and
             sum(pin["bytes"] for pin in auxiliary.values()) <= 512*MIB,
             "DISTRIBUTION_AUXILIARY_CENSUS")
        profile = {"schema": mapping["profile"]["owner_schema"],
                   "installation_manifest_sha256": manifest_pin["sha256"],
                   "helper_paths": mapping["profile"]["helper_paths"],
                   "author_worker": mapping["profile"]["author_worker"], "files": auxiliary}
        raw = E.canonical_json(profile)
        need(len(raw) <= 2*MIB, "DISTRIBUTION_PROFILE_BOUND")
        result = {"status": "BUILT_NOT_ADOPTED", "package": str(package),
            "profile_sha256": hashlib.sha256(raw).hexdigest(),
            "installation_manifest_sha256": manifest_pin["sha256"], "implementation_id": implementation_id,
            "files_excluding_profile": payload_count, "auxiliary_files": len(auxiliary),
            "documentation_files": {name: selected[name][1] for name in sorted(DOCUMENTS)},
            "source_map_sha256": MAP_SHA, "builder": own_pin,
            "inclusive_child_job_cpu_seconds": worker_cpu, "child_cpu_complete": cpu_complete,
            "controller_cpu_seconds_before_commit": time.process_time()-cpu_started,
            "wall_seconds_before_commit": time.monotonic()-started,
            "claim": "SOURCE_BUILD_AND_ASSEMBLY_NOT_OWNER_OR_MATHEMATICAL_ACCEPTANCE"}
        B.save_json(work/"BUILD-RESULT.json", result)
        B.fresh_bytes(package/".PROFILE.pending", raw)
        check(); B.ordinary(package/"PROFILE.json", fresh=True)
        (package/".PROFILE.pending").rename(package/"PROFILE.json")
        return result
    except BaseException as error:
        try:
            B.save_json(work/"BUILD-FAILURE.json", {"phase": phase,
                "error_type": type(error).__name__, "error": str(error)[:2000],
                "inclusive_child_cpu_charged": worker_cpu, "child_cpu_complete": cpu_complete,
                "controller_cpu_seconds": time.process_time()-cpu_started,
                "wall_seconds": time.monotonic()-started, "completed_stage_reports": len(stages),
                "unknown_cpu_policy": "FULL_CHILD_GRANT_CHARGED_THEN_STOP",
                "retention": "PARTIAL_OUTPUT_PRESERVED_NO_RETRY_NO_ACCEPTANCE"})
        except BaseException:
            pass
        raise


def main():
    if sys.argv[1:2] == ["--extractor-worker"]:
        return extractor_worker(sys.argv[2:])
    if sys.argv[1:2] == ["--query-worker"]:
        return query_worker(sys.argv[2:])
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("source-root", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+name, required=True, type=int)
    print(json.dumps(build(parser.parse_args()), sort_keys=True, allow_nan=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

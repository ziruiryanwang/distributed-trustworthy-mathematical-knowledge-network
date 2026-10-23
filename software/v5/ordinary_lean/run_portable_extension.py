"""One actual native alias check above a privately copied imported V2 parent.

Selected compatibility discriminator, not new mathematics or useful growth.
The accepted theorem's exact type/parameters are retained; its alias proof is
one constant at those parameters. No old declaration is rechecked, no basis is
rebuilt, and no compiler is launched. The unchanged adopted worker restores
the retained snapshots and checks exactly this one new complete unit.

Only this controller's actual clean supervised worker event can authorize the
private live-grant commit. Saved success files never supply that authority.
The fresh catalog copy preserves experiment evidence; ordinary contributions
do not require copying their complete store on each call.
"""
from pathlib import Path, PurePosixPath
import hashlib
import importlib.util
import json
import math
import os
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_evidence as E
import ordinary_semantics as S
import local_catalog as C
import portable_evidence as PE
import portable_catalog as P

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
ORIGIN = LOCAL / "ordinary-native-admission-01"
OLD_SOURCE = ORIGIN / "sources/software/v5/ordinary_lean"
OLD_SELECTION = "ab2f655448242587880129e62cca4bc5dc74638c1e8699e30b4a9f67e26fce5f"
PARENT_DIRECTORY = LOCAL / "ordinary-portable-import-01/portable-catalog"
MANIFEST_SCHEMA = "DMKN_ORDINARY_PORTABLE_EXTENSION_PARENT_V1"
TARGET = "DMKN.ReadFootprint.Consumer.snapshot_predicate_applyBatches"
ALIAS = "DMKN.ReadFootprint.Portable.snapshot_predicate_applyBatches_alias01"
CURRENT_SOURCES = ("ordinary_evidence.py", "ordinary_semantics.py", "local_catalog.py",
                   "portable_evidence.py", "portable_catalog.py", "run_portable_extension.py")
PREFIX = "software/v5/ordinary_lean/"
MIB = 1024 * 1024
need, sha = C.need, P.sha


def name(text):
    result = [[0, {"$bytes": list(part.encode("utf-8"))}] for part in text.split(".")]
    E.name_key(result)
    return result


def trusted(raw):
    """Only selected owner metadata/supervision, including finite timings."""
    def pairs(rows):
        result = {}
        for key, value in rows:
            need(key not in result, "PORTABLE_CONTROLLER_DUPLICATE_KEY")
            result[key] = value
        return result
    def reject(_):
        raise ValueError("PORTABLE_CONTROLLER_NONFINITE")
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=reject)


class Inputs:
    def __init__(self, selection, deadline):
        self.selection, self.deadline, self.pins, self.total = selection, deadline, {}, 0

    def live(self):
        need(time.monotonic() < self.deadline, "PORTABLE_EXTENSION_DEADLINE")

    def verify_pin(self, path, pin):
        self.live()
        path = C.ordinary(path)
        P.fields(pin, ("bytes", "sha256"), "PORTABLE_EXTENSION_FILE_PIN")
        P.uint(pin["bytes"], 0, 128 * MIB, "PORTABLE_EXTENSION_FILE_BOUND")
        C.hexid(pin["sha256"])
        need(path.stat().st_size == pin["bytes"], "PORTABLE_EXTENSION_FILE_SIZE")
        actual, size = hashlib.sha256(), 0
        with path.open("rb") as stream:
            while raw := stream.read(MIB):
                self.live()
                size += len(raw)
                need(size <= pin["bytes"], "PORTABLE_EXTENSION_FILE_GREW")
                actual.update(raw)
        need(size == pin["bytes"] and path.stat().st_size == size and
             actual.hexdigest() == pin["sha256"], "PORTABLE_EXTENSION_FILE_CHANGED")

    def pin(self, path, *, expected=None, maximum=128 * MIB):
        path = C.ordinary(path)
        if expected is None:
            expected = {"bytes": path.stat().st_size,
                        "sha256": self.selection["runtime_pins"].get(str(path), "")}
        need(expected["bytes"] <= maximum, "PORTABLE_EXTENSION_SELECTED_FILE_BOUND")
        self.verify_pin(path, expected)
        if path in self.pins:
            need(self.pins[path] == expected, "PORTABLE_EXTENSION_PIN_CONFLICT")
        else:
            self.pins[path] = dict(expected)
            self.total += expected["bytes"]
            need(len(self.pins) <= 16384 and self.total <= 1024 * MIB, "PORTABLE_EXTENSION_INPUT_BOUND")
        return dict(expected)

    def read(self, path, maximum, *, expected=None):
        pin = self.pin(path, expected=expected, maximum=maximum)
        raw = C.read_bounded(path, maximum)
        need(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"], "PORTABLE_EXTENSION_READ_CHANGED")
        self.live()
        return raw

    def named(self, pin, maximum=16 * MIB):
        P.fields(pin, ("path", "bytes", "sha256"), "PORTABLE_EXTENSION_NAMED_PIN")
        path = Path(pin["path"])
        need(self.selection["runtime_pins"].get(str(path)) == pin["sha256"],
             "PORTABLE_EXTENSION_ROOT_PIN_REQUIRED")
        return self.read(path, maximum, expected={key: pin[key] for key in ("bytes", "sha256")})

    def verify(self):
        for path, pin in self.pins.items():
            self.verify_pin(path, pin)


def load_exact(name, path, expected, inputs):
    raw = inputs.read(path, 2 * MIB)
    need(sha(raw) == expected, "PORTABLE_EXTENSION_NATIVE_SOURCE")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


class ParentCopy:
    """Exact adopted experiment parent, not import or peer-store authority."""
    def __init__(self, raw, inputs):
        doc = E.strict_json(raw, E.Limits(max_bytes=16 * MIB))
        P.fields(doc, ("schema", "source_directory", "store_id", "parent_root", "implementation",
            "source_manifest", "correspondence", "import_selection", "directories", "files", "target_evidence"),
            "PORTABLE_EXTENSION_MANIFEST_FIELDS")
        need(doc["schema"] == MANIFEST_SCHEMA and doc["source_directory"] == str(PARENT_DIRECTORY),
             "PORTABLE_EXTENSION_LOCAL_PARENT")
        C.hexid(doc["store_id"]); C.hexid(doc["parent_root"])
        self.doc, self.inputs, self.files, self.directories = doc, inputs, doc["files"], doc["directories"]
        need(type(self.files) is dict and 1 <= len(self.files) <= 8192 and
             type(self.directories) is list and 1 <= len(self.directories) <= 128 and
             len(set(self.directories)) == len(self.directories), "PORTABLE_EXTENSION_COPY_BOUND")
        for relative in [*self.files, *self.directories]:
            path = PurePosixPath(relative)
            need(type(relative) is str and relative and path.as_posix() == relative and not path.is_absolute()
                 and all(part not in (".", "..") for part in path.parts), "PORTABLE_EXTENSION_RELATIVE_PATH")
            parent = path.parent.as_posix()
            need(parent == "." or parent in self.directories, "PORTABLE_EXTENSION_MISSING_DIRECTORY")
        need({"ADOPTION.json", "catalog.sqlite", "owner.lock"} <= set(self.files) and
             {"operations", "imports"} <= set(self.directories) and
             doc["target_evidence"] in self.files, "PORTABLE_EXTENSION_COPY_CENSUS")
        total = 0
        for pin in self.files.values():
            P.fields(pin, ("bytes", "sha256"), "PORTABLE_EXTENSION_COPY_PIN")
            P.uint(pin["bytes"], 1, 128 * MIB, "PORTABLE_EXTENSION_COPY_FILE_BOUND")
            C.hexid(pin["sha256"])
            total += pin["bytes"]
        need(total <= 512 * MIB and self.files["owner.lock"] == {"bytes": 1, "sha256": sha(b"\0")},
             "PORTABLE_EXTENSION_COPY_TOTAL")

    def path(self, relative):
        return PARENT_DIRECTORY.joinpath(*PurePosixPath(relative).parts)

    def verify(self, *, locked=False):
        self.inputs.live()
        need(not os.path.lexists(PARENT_DIRECTORY / "WITHDRAWN"), "PORTABLE_EXTENSION_PARENT_WITHDRAWN")
        for suffix in ("-journal", "-wal", "-shm"):
            need(not os.path.lexists(str(PARENT_DIRECTORY / "catalog.sqlite") + suffix),
                 "PORTABLE_EXTENSION_PARENT_SIDECAR")
        for relative in ["", *self.directories]:
            directory = PARENT_DIRECTORY if not relative else self.path(relative)
            C.ordinary(directory, directory=True)
            expected = {PurePosixPath(item).name for item in [*self.files, *self.directories]
                if PurePosixPath(item).parent.as_posix() == (relative or ".")}
            actual = set()
            with os.scandir(directory) as listing:
                for entry in listing:
                    self.inputs.live()
                    need(entry.name in expected and entry.name not in actual, "PORTABLE_EXTENSION_EXACT_TREE")
                    actual.add(entry.name)
            need(actual == expected, "PORTABLE_EXTENSION_EXACT_TREE")
        for relative, pin in self.files.items():
            if not (locked and relative == "owner.lock"):
                self.inputs.verify_pin(self.path(relative), pin)

    def copy(self, destination):
        import msvcrt
        self.verify()
        with (PARENT_DIRECTORY / "owner.lock").open("r+b") as lock:
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            self.verify(locked=True)
            C.ordinary(destination, directory=True, fresh=True).mkdir()
            for relative in sorted(self.directories, key=lambda item: (item.count("/"), item)):
                destination.joinpath(*PurePosixPath(relative).parts).mkdir()
            for relative, pin in sorted(self.files.items()):
                self.inputs.live()
                target = destination.joinpath(*PurePosixPath(relative).parts)
                actual, size = hashlib.sha256(), 0
                with target.open("xb") as outgoing:
                    if relative == "owner.lock":
                        lock.seek(0)
                        raw = lock.read(2)
                        need(raw == b"\0", "PORTABLE_EXTENSION_LOCK_CHANGED")
                        outgoing.write(raw); actual.update(raw); size = len(raw)
                    else:
                        with self.path(relative).open("rb") as incoming:
                            while raw := incoming.read(MIB):
                                self.inputs.live()
                                size += len(raw)
                                need(size <= pin["bytes"], "PORTABLE_EXTENSION_COPY_GREW")
                                outgoing.write(raw); actual.update(raw)
                    outgoing.flush(); os.fsync(outgoing.fileno())
                need({"bytes": size, "sha256": actual.hexdigest()} == pin, "PORTABLE_EXTENSION_COPY_CHANGED")
                self.inputs.verify_pin(target, pin)
            self.verify(locked=True)
        self.verify()


def alias_evidence(raw, parent):
    """Pure complete V2 unit; the later actual kernel event must check it."""
    original = PE.read_evidence(raw)
    target, alias = name(TARGET), name(ALIAS)
    need(original.document["semantic_id"] == parent["semantic_id"] and
         parent["bindings"].get(E.name_key(target)) ==
         S.export_id(parent["semantic_id"], original.unit_id, target), "PORTABLE_EXTENSION_TARGET_IDENTITY")
    for imported, symbol in original.document["imports"]:
        need(parent["bindings"].get(E.name_key(imported)) == symbol, "PORTABLE_EXTENSION_TARGET_IMPORT")
    descriptor, inventory = original.document["unit"][1:]
    need(len(descriptor) == 6 and descriptor[0] == 1 and descriptor[1] == target and
         len(inventory) == 1 and inventory[0][0] == target and inventory[0][1] == 2 and
         inventory[0][2:4] == descriptor[2:4], "PORTABLE_EXTENSION_EXACT_THEOREM")
    parameters, target_type = descriptor[2:4]
    proof = [E.EXPR_FORMAT, [[4, index] for index in range(len(parameters))],
             [[2, target, list(range(len(parameters)))]], 0]
    unit = [E.UNIT_FORMAT, [1, alias, parameters, target_type, proof, [alias]],
            [[alias, 2, parameters, target_type, [proof, [alias]]]]]
    need(E.name_key(alias) not in parent["bindings"], "PORTABLE_EXTENSION_ALIAS_EXISTS")
    census = E.inspect_unit(unit)
    need(E.name_key(target) in census.external_names, "PORTABLE_EXTENSION_ALIAS_MUST_USE_TARGET")
    imports = []
    for key in census.external_names:
        need(key in parent["bindings"], "PORTABLE_EXTENSION_UNRESOLVED_IMPORT")
        imports.append([E.strict_json(key), parent["bindings"][key]])
    evidence = PE.read_evidence(E.canonical_json({"schema": PE.SCHEMA,
        "semantic_id": parent["semantic_id"], "imports": imports, "unit": unit}))
    return evidence, original.unit_id


def native_support(inputs, source_manifest, implementation):
    original_raw = inputs.read(ORIGIN / "selection.json", 2 * MIB)
    need(sha(original_raw) == OLD_SELECTION, "PORTABLE_EXTENSION_ORIGINAL_SELECTION")
    original = trusted(original_raw)
    for pin in source_manifest["check_support"]:
        P.fields(pin, ("path", "bytes", "sha256"), "PORTABLE_EXTENSION_SUPPORT_PIN")
        path = Path(pin["path"])
        need(inputs.selection["runtime_pins"].get(str(path)) == pin["sha256"],
             "PORTABLE_EXTENSION_ROOT_SUPPORT_PIN")
        inputs.pin(path, expected={key: pin[key] for key in ("bytes", "sha256")})
    profile_path = ORIGIN / "native-admission/PROFILE.json"
    profile = E.strict_json(inputs.read(profile_path, 2 * MIB))
    need(C.digest("ordinary-native-profile-v1", profile["profile"]) == source_manifest["profile_id"],
         "PORTABLE_EXTENSION_ORIGINAL_PROFILE")
    support = profile["support"]
    for key, section, domain in (("kernel_support", "kernel", "ordinary-kernel-support-v1"),
        ("adapter_support", "adapter", "ordinary-adapter-support-v1"),
        ("basis_receiver_support", "basis_receiver", "ordinary-basis-receiver-support-v1")):
        need(C.digest(domain, support[section]) == profile["profile"][key] == implementation[key],
             "PORTABLE_EXTENSION_RETAINED_NATIVE_SUPPORT")
    for filename, pin in support["adapter"]["source"].items():
        need(original["sources"].get(PREFIX + filename) == pin["sha256"], "PORTABLE_EXTENSION_OLD_SOURCE_MAP")
        inputs.pin(OLD_SOURCE / filename, expected=pin, maximum=2 * MIB)
    worker_path = OLD_SOURCE / "run_native_admission.py"
    G = load_exact("portable_extension_native", worker_path,
                   original["sources"][PREFIX + "run_native_admission.py"], inputs)
    G.E, G.C = E, C
    built, core, snapshots = map(Path, original["argv"][-4:-1])
    for directory, modules in ((core, G.GROUPS[0]), (snapshots, G.GROUPS[1]), (built, G.GROUPS[2])):
        C.ordinary(directory, directory=True)
        need(directory.is_relative_to(LOCAL), "PORTABLE_EXTENSION_NATIVE_DIRECTORY")
        expected = {module + ".olean" for module in modules}
        pending, found, entries = [directory], set(), 0
        while pending:
            with os.scandir(pending.pop()) as listing:
                for entry in listing:
                    inputs.live(); entries += 1
                    need(entries <= 128, "PORTABLE_EXTENSION_NATIVE_CENSUS_BOUND")
                    path = Path(entry.path)
                    if entry.is_dir(follow_symlinks=False):
                        pending.append(C.ordinary(path, directory=True))
                    else:
                        C.ordinary(path)
                        found.add(path.relative_to(directory).as_posix())
        need(found == expected, "PORTABLE_EXTENSION_NATIVE_CENSUS")
        for filename in expected:
            pin = support["adapter"]["compiled"][filename]
            path = directory / filename
            need(original["runtime_pins"].get(str(path)) == pin["sha256"], "PORTABLE_EXTENSION_OLD_BINARY_MAP")
            inputs.pin(path, expected=pin)
    need(set(support["kernel"]["files"]) == set(G.KERNEL_FILES), "PORTABLE_EXTENSION_KERNEL_CENSUS")
    for filename, pin in support["kernel"]["files"].items():
        inputs.pin(G.LEAN.parent / filename, expected=pin)
    for path in (Path(sys.executable), *(Path(sys.executable).parent / item
                                        for item in ("python314.dll", "python3.dll"))):
        pin = inputs.pin(path)
        need(original["runtime_pins"].get(str(path)) == pin["sha256"], "PORTABLE_EXTENSION_OLD_PYTHON")
    runner = ORIGIN / "sources/tools/Run-V5-Check.py"
    R = load_exact("portable_extension_runner", runner, original["sources"]["tools/Run-V5-Check.py"], inputs)
    release_raw = C.read_bounded(R.BASE / "RELEASE-MANIFEST.json", 8 * MIB)
    need(sha(release_raw) == R.MANIFEST_SHA, "PORTABLE_EXTENSION_SUPERVISOR_MANIFEST")
    supervisor_files = trusted(release_raw)["files"]
    A = R.load("portable_extension_supervisor", "operator/commons.py", supervisor_files)
    R.load("domains", "receiver/helpers/domains.py", supervisor_files)
    J = R.load("portable_extension_job", "receiver/helpers/run_stage.py", supervisor_files)
    return G, A, J, built, core, snapshots


def main():
    started, cpu_start = time.monotonic(), time.process_time()
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv) == 3,
         "PORTABLE_EXTENSION_SELECTED_INVOCATION")
    output, manifest_path = map(Path, sys.argv[1:])
    source = Path(__file__).resolve()
    need(output.is_absolute() and output.parent == LOCAL and source.parents[4] == output and
         manifest_path.is_absolute() and manifest_path.is_relative_to(LOCAL), "PORTABLE_EXTENSION_SELECTED_PATHS")
    outer = trusted(C.read_bounded(output / "selection.json", 2 * MIB))
    ceiling = outer["limits"]
    need(outer["schema"] == "DMKN_V5_LOCAL_CHECK_V1" and 30 <= ceiling["cpu_seconds"] <= 120 and
         60 <= ceiling["wall_seconds"] <= 180 and ceiling["memory_mib"] <= 1536 and
         ceiling["active_processes"] >= 3, "PORTABLE_EXTENSION_FINITE_ENVELOPE")
    deadline, cpu_cap = started + ceiling["wall_seconds"] - 20, ceiling["cpu_seconds"] - 10
    inputs = Inputs(outer, deadline)
    manifest_raw = inputs.read(manifest_path, 16 * MIB)
    manifest = ParentCopy(manifest_raw, inputs)
    doc = manifest.doc
    implementation_raw = inputs.named(doc["implementation"])
    implementation = S.read_implementation(implementation_raw)
    source_manifest_raw = inputs.named(doc["source_manifest"])
    source_manifest = E.strict_json(source_manifest_raw, E.Limits(max_bytes=16 * MIB))
    correspondence_raw = inputs.named(doc["correspondence"])
    correspondence = E.strict_json(correspondence_raw)
    import_selection_raw = inputs.named(doc["import_selection"])
    import_selection = trusted(import_selection_raw)
    need(implementation["controller_support"] == C.digest("ordinary-portable-controller-support-v1",
         import_selection["sources"]), "PORTABLE_EXTENSION_IMPLEMENTATION_CONTROLLER")
    for filename in CURRENT_SOURCES:
        relative = PREFIX + filename
        expected = import_selection["sources"].get(relative)
        need(type(expected) is str and outer["sources"].get(relative) == expected,
             "PORTABLE_EXTENSION_CONTROLLER_NOT_IN_IMPLEMENTATION")
        path = source.parent / filename
        inputs.pin(path, expected={"bytes": path.stat().st_size, "sha256": expected}, maximum=2 * MIB)
    need(correspondence["implementation_id"] == S.implementation_id(implementation_raw) and
         correspondence["source_profile_id"] == source_manifest["profile_id"] and
         correspondence["semantic_id"] == S.semantic_id() and correspondence["foundation_id"] == S.foundation_id(),
         "PORTABLE_EXTENSION_IMPORTED_CORRESPONDENCE")
    G, A, J, built, core, snapshots = native_support(inputs, source_manifest, implementation)
    root = output / "portable-extension"
    C.ordinary(root, directory=True, fresh=True).mkdir()
    (root / "call").mkdir()
    manifest.copy(root / "catalog")
    copied = root / "catalog"
    marker = E.strict_json(C.read_bounded(copied / "ADOPTION.json", 2 * MIB))
    need(marker["schema"] == P.SCHEMA and marker["store_id"] == doc["store_id"] and
         marker["implementation"] == implementation, "PORTABLE_EXTENSION_COPIED_IMPLEMENTATION")
    limits = C.Limits(**marker["limits"])
    for relative, pin in manifest.files.items():
        if relative not in ("catalog.sqlite", "owner.lock"):
            inputs.pin(copied.joinpath(*PurePosixPath(relative).parts), expected=pin)
    catalog = P.PortableCatalog.open(copied, implementation_raw, doc["store_id"], limits=limits)
    grant, child_cpu = None, 0.0
    def within():
        inputs.live()
        need(child_cpu + time.process_time() - cpu_start < cpu_cap, "PORTABLE_EXTENSION_CPU_ENVELOPE")
    try:
        parent = catalog.context(doc["parent_root"])
        need(len(parent["modules"]) == 5 and len(parent["bindings"]) == 3629, "PORTABLE_EXTENSION_ADOPTED_PARENT")
        activation = catalog._active()
        imported = catalog._import_record(activation)
        need(imported is not None and imported["source_manifest_sha256"] == sha(source_manifest_raw) and
             imported["correspondence_sha256"] == sha(correspondence_raw) and
             imported["source_selected_root"] == source_manifest["selected_root"] and
             imported["roots"][-1][0] == doc["parent_root"], "PORTABLE_EXTENSION_IMPORT_LINEAGE")
        audit_path = copied.joinpath(*PurePosixPath(imported["audit"]["relative_path"]).parts)
        audit = E.strict_json(inputs.read(audit_path, 16 * MIB, expected={
            "bytes": imported["audit"]["artifact_bytes"], "sha256": imported["audit"]["artifact_sha256"]}),
            E.Limits(max_bytes=16 * MIB))
        target_key = E.name_key(name(TARGET))
        selected = [entry for row in audit["roots"] for entry in row["translations"]
            if any(E.name_key(binding[0]) == target_key for binding in entry["portable_outputs"])]
        need(len(selected) == 1 and selected[0]["portable_evidence"]["relative_path"] == doc["target_evidence"],
             "PORTABLE_EXTENSION_AUDITED_TARGET_EVIDENCE")
        evidence_path = copied.joinpath(*PurePosixPath(doc["target_evidence"]).parts)
        target_raw = inputs.read(evidence_path, 8 * MIB, expected=manifest.files[doc["target_evidence"]])
        evidence, target_unit_id = alias_evidence(target_raw, parent)
        need(target_unit_id == selected[0]["portable_unit_id"] and
             sha(target_raw) == selected[0]["portable_evidence"]["artifact_sha256"],
             "PORTABLE_EXTENSION_AUDIT_TARGET_ID")
        files = G.AuthoredFiles()
        evidence_pin = files.write(root / "evidence.json", evidence.raw, 8 * MIB)
        units_raw = E.canonical_json([evidence.document["unit"]])
        units_pin = files.write(root / "call/units.json", units_raw, 8 * MIB)
        within()
        seconds = math.floor(deadline - time.monotonic()) - 1
        need(seconds >= 20, "PORTABLE_EXTENSION_REMAINING_BUDGET")
        grant = catalog.reserve_extension(doc["parent_root"], (evidence.raw,), seconds=seconds, output_bytes=8 * MIB)
        need(grant.input_unit_ids == (evidence.unit_id,) and grant.request_hash == P.batch_id([evidence.unit_id]) and
             grant.parent_plan_raw == E.canonical_json(parent["modules"]) and
             grant.parent_module_raw == E.canonical_json(parent["root_module"]) and grant.deadline <= deadline,
             "PORTABLE_EXTENSION_LIVE_GRANT_BINDING")
        plan = {"basis_module": parent["basis_module"], "root_module": parent["root_module"],
                "modules": E.strict_json(grant.parent_plan_raw, E.Limits(max_bytes=16 * MIB))}
        plan_pin = files.json(root / "call/plan.json", plan, 16 * MIB)
        for path, pin in ((root / "evidence.json", evidence_pin), (root / "call/units.json", units_pin),
                          (root / "call/plan.json", plan_pin)):
            inputs.pin(path, expected=pin, maximum=16 * MIB)
        alias = name(ALIAS)
        expected = dict(parent["bindings"])
        expected[E.name_key(alias)] = S.export_id(parent["semantic_id"], evidence.unit_id, alias)
        files.json(root / "NATIVE-PLAN.json", {"schema": "DMKN_ORDINARY_PORTABLE_NATIVE_PLAN_V1",
            "implementation_id": parent["implementation_id"], "semantic_id": parent["semantic_id"],
            "foundation_id": parent["foundation_id"], "parent_root": doc["parent_root"],
            "parent_module": parent["root_module"], "new_root": grant.root, "alias": alias,
            "target": name(TARGET), "target_unit_id": target_unit_id, "unit_id": evidence.unit_id,
            "request_hash": grant.request_hash, "units_checked": 1, "new_names": 1,
            "assurance": "INERT_PLAN_REQUIRES_ACTUAL_CLEAN_NATIVE_CHECK"}, 2 * MIB)
        report_path = root / "call/worker-report.json"
        argv = [sys.executable, "-I", "-S", "-B", str(OLD_SOURCE / "run_native_admission.py"), "--worker",
            str(built), str(core), str(snapshots), "extend", str(root / "call/plan.json"),
            str(root / "call/units.json"), grant.root, str(grant.directory / "chunk.olean"), str(report_path)]
        remaining_cpu = cpu_cap - (time.process_time() - cpu_start)
        remaining_wall = min(deadline, grant.deadline) - time.monotonic()
        need(remaining_cpu >= 5 and remaining_wall >= 20, "PORTABLE_EXTENSION_NATIVE_REMAINDER")
        allowance = A.limits_checked({"cpu_seconds": math.floor(remaining_cpu),
            "wall_seconds": math.floor(remaining_wall - 10), "memory_mib": ceiling["memory_mib"],
            "active_processes": 2, "stdout_bytes": MIB, "stderr_bytes": MIB})
        actual = A.supervise(argv, ROOT, root / "call/supervision", allowance, J.Job)
        A.save_new(root / "call/SUPERVISION.json", actual)
        final = actual.get("final_job")
        if type(final) is dict and type(final.get("cpu_seconds")) in (int, float):
            child_cpu = final["cpu_seconds"]
        need(G.clean_worker(actual), "PORTABLE_EXTENSION_ACTUAL_WORKER_NOT_CLEAN")
        for filename in ("stdout.txt", "stderr.txt"):
            log = C.ordinary(root / "call/supervision" / filename)
            need(log.stat().st_size <= MIB, "PORTABLE_EXTENSION_LOG_BOUND")
            with log.open("rb") as stream:
                need(b"PANIC" not in stream.read(MIB + 1).upper(), "PORTABLE_EXTENSION_NATIVE_DIAGNOSTIC")
        within(); inputs.verify(); manifest.verify()
        raw_report = C.read_bounded(report_path, 16 * MIB)
        report = G.writer_json(raw_report, 16 * MIB)
        artifact = C.ordinary(grant.directory / "chunk.olean")
        need(type(report) is dict and set(report) == G.REPORT_FIELDS and
             report["schema"] == "DMKN_ORDINARY_WORKER_OUTPUT_V1" and report["kind"] == "extension" and
             report["module_name"] == E.strict_json(grant.module_name_raw) and
             report["parent_module"] == E.strict_json(grant.parent_module_raw) and report["names"] == [alias] and
             type(report["units_checked"]) is int and report["units_checked"] == 1 and
             type(report["artifact_bytes"]) is int and report["artifact_bytes"] == artifact.stat().st_size and
             0 < report["artifact_bytes"] <= 8 * MIB, "PORTABLE_EXTENSION_ACTUAL_REPORT_BINDING")
        within()
        accepted = catalog._commit_checked(grant)
        request_hash, operation = grant.request_hash, grant.identifier
        grant = None
        before = catalog.context(accepted)
        need(before["bindings"] == expected and len(before["modules"]) == 6 and
             before["modules"][-1]["parent_module"] == parent["root_module"], "PORTABLE_EXTENSION_EXACT_CONTEXT")
        record_raw, record = catalog._root_row(accepted)
        need(record["origin"] == "native-check" and record["provenance"] == {
            "implementation_id": parent["implementation_id"], "operation_id": operation},
            "PORTABLE_EXTENSION_NATIVE_ORIGIN")
        catalog.close()
        catalog = P.PortableCatalog.open(copied, implementation_raw, doc["store_id"], limits=limits)
        need(catalog.context(accepted) == before, "PORTABLE_EXTENSION_REOPEN_CONTEXT")
        inputs.verify(); manifest.verify(); within()
        result = {"schema": "DMKN_ORDINARY_PORTABLE_EXTENSION_RESULT_V1",
            "status": "PASS_ONE_ACTUAL_NEW_NATIVE_UNIT_OVER_IMPORTED_PARENT",
            "implementation_id": parent["implementation_id"], "semantic_id": parent["semantic_id"],
            "foundation_id": parent["foundation_id"], "store_id": doc["store_id"],
            "parent_root": doc["parent_root"], "parent_module": parent["root_module"], "local_root": accepted,
            "target": name(TARGET), "target_unit_id": target_unit_id, "alias": alias,
            "alias_symbol_id": expected[E.name_key(alias)], "unit_id": evidence.unit_id,
            "request_hash": request_hash, "units_checked": 1, "new_names": 1,
            "total_names": len(expected), "artifact_bytes": report["artifact_bytes"],
            "artifact_sha256": record["snapshot"]["artifact_sha256"], "record_sha256": sha(record_raw),
            "worker_report_sha256": sha(raw_report), "parent_manifest_sha256": sha(manifest_raw),
            "worker_cpu_seconds": child_cpu, "controller_cpu_seconds": time.process_time() - cpu_start,
            "wall_seconds": time.monotonic() - started,
            "claims": "LOCAL_NATIVE_SNAPSHOT_COMPATIBILITY_NOT_NOVEL_MATHEMATICS_DISCOVERY_GROWTH_OR_RELEASE"}
        A.save_new(root / "EXTENSION-RESULT.json", result)
        print(json.dumps(result), flush=True)
        return 0
    finally:
        if grant is not None and not catalog._closed and catalog._grant is grant:
            catalog.abandon(grant)
        catalog.close()


if __name__ == "__main__":
    raise SystemExit(main())

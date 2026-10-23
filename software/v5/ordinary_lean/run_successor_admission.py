"""Root-selected one-batch admission over the adopted protected local library.

No original catalog writes, basis/proof-closure replay, new verifier, automatic
retry or certificate. A saved report is not acceptance: only this controller's
actual clean pinned worker invocation may reach the private catalog commit.
"""
from pathlib import Path, PurePosixPath
import gc
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
ORIGIN = LOCAL / "ordinary-native-admission-01"
OLD_SOURCE = ORIGIN / "sources/software/v5/ordinary_lean"
OLD_SELECTION = "ab2f655448242587880129e62cca4bc5dc74638c1e8699e30b4a9f67e26fce5f"
STORE_PATH = LOCAL / "ordinary-native-recovery-01/native-recovery/catalog"
PROFILE = "fd23ae289706e5a3277a3c4304de83d65498755dd014b234810e79539f5c8219"
BASIS = "cb8f9c2db2b5b53984be1ce8b5f540024264a1e2db41fc7226c594ee1f022299"
PARENT = "4d70ddd613bbbfe5e9312ea403e64a95a0a2239842a19d90bf0c044847929026"
STORE = "12185a972a6302a0a70899e968f4c249d1994afd252ecbb74c91e59961b81eb5"
DATABASE = "bcb94ff9695f4d360205eaf8f81151f1cf70437c0e6c434b48f6993d893980e9"
MIB = 1024 * 1024


def need(ok, code):
    if not ok:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def trusted_json(raw):
    """Only root-pinned local records; permit finite supervision timing floats."""
    def pairs(rows):
        out = {}
        for key, value in rows:
            need(key not in out, "TRUSTED_JSON_DUPLICATE_KEY")
            out[key] = value
        return out
    def reject(_):
        raise ValueError("TRUSTED_JSON_NONFINITE")
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=reject)


def bootstrap_read(path, maximum):
    need(path.is_absolute() and path.resolve() == path and path.is_file() and
         0 < path.stat().st_size <= maximum, "BOOTSTRAP_LOCAL_PATH_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    need(0 < len(raw) <= maximum, "BOOTSTRAP_READ_BOUND")
    return raw


def load_exact(name, path, expected):
    raw = bootstrap_read(path, 2 * MIB)
    need(sha(raw) == expected, "FROZEN_SOURCE_PIN:" + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


class Inputs:
    def __init__(self, selection):
        self.selection, self.pins = selection, {}

    def pin(self, path, maximum=512 * MIB, *, expected=None):
        C.ordinary(path)
        size = path.stat().st_size
        need(0 < size <= maximum, "INPUT_BYTE_BOUND:" + str(path))
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        actual = {"bytes": size, "sha256": digest}
        need(path.stat().st_size == size, "INPUT_CHANGED_DURING_HASH")
        if expected is None:
            need(self.selection["runtime_pins"].get(str(path)) == digest,
                 "ROOT_RUNTIME_PIN_REQUIRED:" + str(path))
        else:
            need(type(expected) is dict and set(expected) == {"bytes", "sha256"} and
                 actual == expected, "AUTHENTICATED_MANIFEST_PIN:" + str(path))
        self.pins[path] = actual
        return actual

    def read(self, path, maximum, *, expected=None):
        pin = self.pin(path, maximum, expected=expected)
        raw = C.read_bounded(path, maximum)
        need(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"], "PINNED_READ_CHANGED")
        return raw

    def verify(self):
        for path, expected in tuple(self.pins.items()):
            self.pin(path, expected["bytes"], expected=expected)


def native_support(inputs, original):
    """Reuse exact native support without reading the obsolete producer bundle."""
    document = trusted_json(inputs.read(ORIGIN / "native-admission/PROFILE.json", 2 * MIB))
    profile, support = document["profile"], document["support"]
    C.profile_bytes(profile)
    need(C.digest("ordinary-native-profile-v1", profile) == PROFILE, "ADOPTED_NATIVE_PROFILE")
    for field, component, domain in (
        ("kernel_support", "kernel", "ordinary-kernel-support-v1"),
        ("adapter_support", "adapter", "ordinary-adapter-support-v1"),
        ("basis_receiver_support", "basis_receiver", "ordinary-basis-receiver-support-v1")):
        need(C.digest(domain, support[component]) == profile[field], "PROFILE_SUPPORT_BINDING")
    for name, pin in support["adapter"]["source"].items():
        path = OLD_SOURCE / name
        need(original["sources"].get("software/v5/ordinary_lean/" + name) == pin["sha256"],
             "ORIGINAL_SELECTED_SOURCE_BINDING")
        inputs.pin(path, 2 * MIB)
        need(inputs.pins[path] == pin, "ORIGINAL_PROFILE_SOURCE")
    built, core, snapshots = map(Path, original["argv"][-4:-1])
    for directory, modules in ((core, G.GROUPS[0]), (snapshots, G.GROUPS[1]), (built, G.GROUPS[2])):
        C.ordinary(directory, directory=True)
        need(directory.is_relative_to(LOCAL), "FROZEN_BUILD_DIRECTORY")
        # Bounded, non-following census prevents selected-path module shadowing.
        pending, found, entries = [directory], set(), 0
        while pending:
            current = pending.pop()
            with os.scandir(current) as listing:
                for entry in listing:
                    entries += 1
                    need(entries <= 128, "COMPILED_PATH_CENSUS_BOUND")
                    path = Path(entry.path)
                    if entry.is_dir(follow_symlinks=False):
                        C.ordinary(path, directory=True)
                        pending.append(path)
                    else:
                        C.ordinary(path)
                        found.add(path.relative_to(directory).as_posix())
        need(found == {name + ".olean" for name in modules}, "COMPILED_DIRECTORY_CENSUS")
        for name in modules:
            path = directory / (name + ".olean")
            inputs.pin(path)
            need(inputs.pins[path] == support["adapter"]["compiled"][name + ".olean"] and
                 original["runtime_pins"].get(str(path)) == inputs.pins[path]["sha256"],
                 "FROZEN_PROFILE_ARTIFACT")
    need(set(support["kernel"]["files"]) == set(G.KERNEL_FILES), "KERNEL_FILE_CENSUS")
    for name, pin in support["kernel"]["files"].items():
        path = G.LEAN.parent / name
        inputs.pin(path)
        need(inputs.pins[path] == pin, "FROZEN_KERNEL_FILE")
    for path in (Path(sys.executable), *(Path(sys.executable).parent / x
                                       for x in ("python314.dll", "python3.dll"))):
        inputs.pin(path)
        need(original["runtime_pins"].get(str(path)) == inputs.pins[path]["sha256"],
             "ORIGINAL_PYTHON_RUNTIME")
    return profile, built, core, snapshots


class StoreManifest:
    """Exact adopted local-store copy authority, not a foreign-catalog importer."""
    def __init__(self, raw):
        doc = trusted_json(raw)
        need(type(doc) is dict and set(doc) == {"schema", "store_directory", "profile_id",
             "basis_id", "context_id", "store_id", "directories", "files"} and
             doc["schema"] == "DMKN_ORDINARY_SUCCESSOR_PARENT_COPY_V1" and
             doc["store_directory"] == str(STORE_PATH) and doc["profile_id"] == PROFILE and
             doc["basis_id"] == BASIS and doc["context_id"] == PARENT and doc["store_id"] == STORE,
             "ADOPTED_PARENT_COPY_MANIFEST")
        self.files, self.directories = doc["files"], doc["directories"]
        need(type(self.files) is dict and len(self.files) == 7 and
             type(self.directories) is list and len(self.directories) == 6 and
             len(set(self.directories)) == 6 and "operations" in self.directories,
             "ADOPTED_PARENT_FILE_CENSUS")
        total = 0
        for relative in [*self.directories, *self.files]:
            path = PurePosixPath(relative)
            need(type(relative) is str and path.as_posix() == relative and not path.is_absolute() and
                 all(x not in (".", "..") for x in path.parts), "MANIFEST_RELATIVE_PATH")
        for relative in self.directories:
            need(relative == "operations" or re.fullmatch(r"operations/[0-9a-f]{64}", relative),
                 "CATALOG_DIRECTORY_SHAPE")
        for relative, pin in self.files.items():
            need(relative in ("ADOPTION.json", "catalog.sqlite", "owner.lock") or
                 re.fullmatch(r"operations/[0-9a-f]{64}/chunk\.olean", relative), "CATALOG_FILE_SHAPE")
            need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
                 type(pin["bytes"]) is int and 0 < pin["bytes"] <= 64 * MIB, "CATALOG_FILE_PIN")
            C.hexid(pin["sha256"])
            total += pin["bytes"]
            parent = PurePosixPath(relative).parent.as_posix()
            need(parent == "." or parent in self.directories, "CATALOG_FILE_PARENT")
        need(total <= 128 * MIB and self.files["catalog.sqlite"]["sha256"] == DATABASE and
             self.files["owner.lock"] == {"bytes": 1, "sha256": sha(b"\0")}, "EXACT_ADOPTED_DATABASE")

    def path(self, relative):
        return STORE_PATH.joinpath(*PurePosixPath(relative).parts)

    def verify(self, *, locked=False):
        C.ordinary(STORE_PATH, directory=True)
        need(not os.path.lexists(STORE_PATH / "WITHDRAWN"), "ADOPTED_PARENT_WITHDRAWN")
        for relative in ["", *self.directories]:
            directory = STORE_PATH if not relative else self.path(relative)
            C.ordinary(directory, directory=True)
            expected = {PurePosixPath(x).name for x in [*self.directories, *self.files]
                        if PurePosixPath(x).parent.as_posix() == (relative or ".")}
            need({entry.name for entry in directory.iterdir()} == expected, "ADOPTED_PARENT_EXACT_TREE")
        for relative, expected in self.files.items():
            path = C.ordinary(self.path(relative))
            if locked and relative == "owner.lock":
                continue
            need(path.stat().st_size == expected["bytes"], "PARENT_FILE_SIZE")
            with path.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            need(digest == expected["sha256"] and path.stat().st_size == expected["bytes"],
                 "PARENT_FILE_CHANGED")

    def copy_to(self, destination):
        import msvcrt
        self.verify()
        with (STORE_PATH / "owner.lock").open("r+b") as lock:
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            self.verify(locked=True)
            C.ordinary(destination, directory=True, fresh=True).mkdir()
            for relative in sorted(self.directories, key=lambda x: (x.count("/"), x)):
                destination.joinpath(*PurePosixPath(relative).parts).mkdir()
            for relative, expected in sorted(self.files.items()):
                target = destination.joinpath(*PurePosixPath(relative).parts)
                digest, size = hashlib.sha256(), 0
                with target.open("xb") as outgoing:
                    if relative == "owner.lock":
                        lock.seek(0)
                        data = lock.read(2)
                        need(data == b"\0", "LOCK_CHANGED")
                        outgoing.write(data)
                        digest.update(data)
                        size = len(data)
                    else:
                        with self.path(relative).open("rb") as incoming:
                            while data := incoming.read(MIB):
                                size += len(data)
                                need(size <= expected["bytes"], "PARENT_COPY_GREW")
                                outgoing.write(data)
                                digest.update(data)
                    outgoing.flush()
                    os.fsync(outgoing.fileno())
                need({"bytes": size, "sha256": digest.hexdigest()} == expected, "PARENT_COPY_PIN")
                C.ordinary(target)
                with target.open("rb") as stream:
                    readback = hashlib.file_digest(stream, "sha256").hexdigest()
                need(target.stat().st_size == size and readback == expected["sha256"], "COPY_READBACK")
            self.verify(locked=True)
        self.verify()


def prepared_bindings(inputs, manifest_path, parent_bindings):
    manifest = trusted_json(inputs.read(manifest_path, 2 * MIB))
    need(manifest["profile_id"] == PROFILE and manifest["context_id"] == PARENT and
         type(manifest["request_files"]) is dict, "PREPARED_CONTEXT")
    files, directory = manifest["request_files"], manifest_path.parent / "owner-request"
    C.ordinary(directory, directory=True)
    need(1 <= len(files) <= 8193 and {p.name for p in directory.iterdir()} == set(files),
         "PREPARED_FILE_CENSUS")
    total, bindings = 0, {}

    def read(name):
        nonlocal total
        need(name in files, "PREPARED_FILENAME_REQUIRED")
        raw = inputs.read(directory / name, 8 * MIB, expected=files[name])
        total += len(raw)
        need(total <= 64 * MIB, "PREPARED_AGGREGATE_BYTES")
        return E.strict_json(raw, E.Limits(max_bytes=8 * MIB))

    def bind(name, symbol):
        key = E.name_key(name)
        E._hex(symbol)
        need(key not in bindings and parent_bindings.get(key) == symbol, "PREPARED_ACCEPTED_IDENTITY")
        need(len(bindings) < 65536, "PREPARED_BINDING_BOUND")
        bindings[key] = symbol

    header = read("header.json")
    need(type(header) is dict and set(header) == {"schema", "profile_id", "context_id", "basis_id",
         "basis_rows", "targets", "group_count"} and header["schema"] == "DMKN_OWNER_REQUEST_V1" and
         header["profile_id"] == PROFILE and header["context_id"] == PARENT and header["basis_id"] == BASIS,
         "PREPARED_HEADER")
    count = header["group_count"]
    need(type(count) is int and 0 <= count <= 8192 and
         set(files) == {"header.json", *(f"group-{i:05d}.json" for i in range(count))},
         "PREPARED_NUMBERED_GROUPS")
    need(type(header["basis_rows"]) is list and 1 <= len(header["basis_rows"]) <= 4096,
         "PREPARED_BASIS_BOUND")
    for entry in header["basis_rows"]:
        symbol, row = E._array(entry, 2)
        bind(E._array(row, 5)[0], symbol)
    for index in range(count):
        marker, rows, optional = E._array(read(f"group-{index:05d}.json"), 3)
        need(marker == "DMKN_OWNER_GROUP_V1" and type(rows) is list and bool(rows), "PREPARED_GROUP")
        E._array(optional, maximum=1)
        for row in rows:
            name, mode, symbol, _ = E._array(row, 4)
            need(type(mode) is int and mode in (0, 1), "PREPARED_MATCH_MODE")
            bind(name, symbol)
    return bindings


def prepare_bundle(inputs, bundle_path, prepared, parent_bindings, target, directory, files):
    bundle = G.writer_json(inputs.read(bundle_path, 64 * MIB), 64 * MIB)
    need(type(bundle) is dict and set(bundle) == {"schema", "assurance", "profile_id", "context_id",
         "basis_id", "targets", "boundary_imports", "units", "stats"} and
         bundle["schema"] == "DMKN_ORDINARY_SUCCESSOR_BUNDLE_V1" and
         bundle["assurance"] == "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE" and
         bundle["profile_id"] == PROFILE and bundle["context_id"] == PARENT and bundle["basis_id"] == BASIS and
         bundle["targets"] == [target], "EXACT_SUCCESSOR_BUNDLE")
    available = {}
    for row in E._array(bundle["boundary_imports"], maximum=65536):
        name, symbol = E._array(row, 2)
        key = E.name_key(name)
        E._hex(symbol)
        need(key not in available and prepared.get(key) == symbol and parent_bindings.get(key) == symbol,
             "SUCCESSOR_BOUNDARY_IDENTITY")
        available[key] = symbol
    units = E._array(bundle["units"], maximum=1024)
    need(bool(units), "SUCCESSOR_NEW_UNITS_REQUIRED")
    stats = bundle["stats"]
    need(type(stats) is dict and set(stats) == {"source_records_enumerated", "selected_units", "dependency_edges",
         "scan_nodes", "unit_json_bytes", "boundary_imports"} and
         all(type(x) is int and 0 <= x <= (1 << 64) - 1 for x in stats.values()) and
         stats["selected_units"] == len(units) and stats["boundary_imports"] == len(available),
         "SUCCESSOR_STATISTICS_CENSUS")
    evidence_paths, identities, names, added = [], [], [], {}
    nodes, evidence_bytes, unit_bytes, stream_bytes = 0, 0, 0, 2
    units_path = directory / "units.json"
    with units_path.open("xb") as output:
        output.write(b"[")
        for index, unit in enumerate(units):
            census = E.inspect_unit(unit)
            need(all(key in available for key in census.external_names), "UNBOUND_SUCCESSOR_REFERENCE")
            imports = [[E.strict_json(key), available[key]] for key in census.external_names]
            raw = E.canonical_json({"schema": E.SCHEMA, "profile_id": PROFILE, "imports": imports, "unit": unit})
            evidence = E.read_evidence(raw)
            encoded = E.canonical_json(unit)
            nodes += census.total_nodes
            evidence_bytes += len(raw)
            unit_bytes += len(encoded)
            stream_bytes += len(encoded) + (1 if index else 0)
            need(nodes <= 2097152 and evidence_bytes <= 64 * MIB and stream_bytes <= 64 * MIB,
                 "SINGLE_SUCCESSOR_BATCH_BOUND")
            for row in unit[2]:
                name, key = row[0], E.name_key(row[0])
                need(key not in parent_bindings and key not in added, "SUCCESSOR_EXISTING_OR_DUPLICATE_NAME")
                symbol = E.export_id(PROFILE, evidence.unit_id, name)
                added[key], available[key] = symbol, symbol
                names.append(name)
                need(len(names) <= 65536, "SUCCESSOR_NAME_BOUND")
            path = directory / "evidence" / f"{index:05d}.json"
            pin = files.write(path, raw, 8 * MIB)
            evidence_paths.append((path, pin))
            identities.append(evidence.unit_id)
            if index:
                output.write(b",")
            output.write(encoded)
        output.write(b"]")
        output.flush()
        os.fsync(output.fileno())
    need(E.name_key(target) in added and unit_bytes == stats["unit_json_bytes"], "SUCCESSOR_TARGET_OR_BYTES")
    with units_path.open("rb") as stream:
        unit_digest = hashlib.file_digest(stream, "sha256").hexdigest()
    need(units_path.stat().st_size == stream_bytes, "SUCCESSOR_UNITS_WRITE_SIZE")
    return {"evidence": evidence_paths, "names": names, "added": added, "units": len(units),
            "nodes": nodes, "evidence_bytes": evidence_bytes, "units_path": units_path,
            "units_pin": {"bytes": stream_bytes, "sha256": unit_digest},
            "request_hash": C.digest("ordinary-batch-v1", identities), "owner_statistics": stats}


def main():
    global E, C, G
    started, cpu_start = time.monotonic(), time.process_time()
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv) == 6, "SELECTED_OWNER_INVOCATION")
    output, bundle_path, prepare_path, manifest_path = map(Path, sys.argv[1:5])
    source = Path(__file__).resolve()
    need(output.is_absolute() and output.is_relative_to(LOCAL) and source.parents[3] == output / "sources" and
         all(p.is_absolute() and p.is_relative_to(LOCAL) for p in (bundle_path, prepare_path, manifest_path)),
         "SELECTED_SUCCESSOR_PATHS")
    outer = trusted_json(bootstrap_read(output / "selection.json", 2 * MIB))
    need(outer["schema"] == "DMKN_V5_LOCAL_CHECK_V1" and
         sha(bootstrap_read(source, 2 * MIB)) == outer["sources"][source.relative_to(output / "sources").as_posix()],
         "SELECTED_CONTROLLER_SOURCE")
    ceiling = outer["limits"]
    need(30 <= ceiling["cpu_seconds"] <= 120 and 60 <= ceiling["wall_seconds"] <= 180 and
         ceiling["memory_mib"] <= 1536 and ceiling["active_processes"] >= 3, "FINITE_SUCCESSOR_ENVELOPE")
    original_raw = bootstrap_read(ORIGIN / "selection.json", 2 * MIB)
    need(sha(original_raw) == OLD_SELECTION and
         outer["runtime_pins"].get(str(ORIGIN / "selection.json")) == OLD_SELECTION, "FROZEN_NATIVE_SELECTION")
    original = trusted_json(original_raw)
    def old(name, filename):
        digest = original["sources"]["software/v5/ordinary_lean/" + filename]
        need(outer["runtime_pins"].get(str(OLD_SOURCE / filename)) == digest, "FROZEN_CONTROLLER_SELECTION")
        return load_exact(name, OLD_SOURCE / filename, digest)
    E = old("ordinary_evidence", "ordinary_evidence.py")
    C = old("ordinary_successor_catalog", "local_catalog.py")
    G = old("ordinary_successor_native", "run_native_admission.py")
    G.E, G.C = E, C
    inputs = Inputs(outer)
    inputs.pin(ORIGIN / "selection.json", 2 * MIB)
    profile, built, core, snapshots = native_support(inputs, original)
    runner_path = ORIGIN / "sources/tools/Run-V5-Check.py"
    inputs.pin(runner_path, 2 * MIB)
    R = load_exact("ordinary_successor_runner", runner_path, original["sources"]["tools/Run-V5-Check.py"])
    release = C.read_bounded(R.BASE / "RELEASE-MANIFEST.json", 8 * MIB)
    need(sha(release) == R.MANIFEST_SHA, "FROZEN_SUPERVISOR_MANIFEST")
    supervisor_files = trusted_json(release)["files"]
    A = R.load("ordinary_successor_supervisor", "operator/commons.py", supervisor_files)
    R.load("domains", "receiver/helpers/domains.py", supervisor_files)
    J = R.load("ordinary_successor_job", "receiver/helpers/run_stage.py", supervisor_files)
    manifest = StoreManifest(inputs.read(manifest_path, 2 * MIB))
    parts = sys.argv[5].split(".")
    need(parts and all(parts) and len(sys.argv[5].encode()) <= 32768, "SELECTED_TARGET_NAME")
    target = [[0, {"$bytes": list(part.encode("utf-8"))}] for part in parts]
    E.name_key(target)
    root = output / "successor-admission"
    C.ordinary(root, directory=True, fresh=True).mkdir()
    (root / "evidence").mkdir()
    (root / "call").mkdir()
    manifest.copy_to(root / "catalog")
    adoption = trusted_json(C.read_bounded(root / "catalog/ADOPTION.json", 2 * MIB))
    need(adoption["profile"] == profile and adoption["store_id"] == STORE and adoption["schema"] == C.SCHEMA,
         "COPIED_ADOPTION_IDENTITY")
    limits = C.Limits(**adoption["limits"])
    # Copied parent artifacts stay immutable even while the copy's database is
    # extended. Do not hash the separate locked byte through another handle.
    for relative, pin in manifest.files.items():
        if relative not in ("catalog.sqlite", "owner.lock"):
            inputs.pin(root / "catalog" / relative, 64 * MIB, expected=pin)
    catalog = C.LocalCatalog.open(root / "catalog", profile, STORE, limits=limits)
    grant, child_cpu = None, 0.0
    cpu_cap, wall_cap = ceiling["cpu_seconds"] - 10, ceiling["wall_seconds"] - 20
    def within():
        need(child_cpu + time.process_time() - cpu_start <= cpu_cap and
             time.monotonic() - started <= wall_cap, "SUCCESSOR_MASTER_ENVELOPE")
    try:
        parent = catalog.context(PARENT)
        need(len(parent["modules"]) == 4 and len(parent["bindings"]) == 3622, "ACTUAL_ADOPTED_CONTEXT")
        prepared = prepared_bindings(inputs, prepare_path, parent["bindings"])
        files = G.AuthoredFiles()
        batch = prepare_bundle(inputs, bundle_path, prepared, parent["bindings"], target, root, files)
        expected = dict(parent["bindings"])
        expected.update(batch["added"])
        plan = {"basis_module": C.module_name(BASIS), "root_module": C.module_name(PARENT),
                "modules": parent["modules"]}
        plan_path = root / "call/plan.json"
        plan_pin = files.json(plan_path, plan, 16 * MIB)
        files.json(root / "ADMISSION-PLAN.json", {"profile_id": PROFILE, "parent": PARENT,
            "bundle_sha256": inputs.pins[bundle_path]["sha256"],
            "prepare_manifest_sha256": inputs.pins[prepare_path]["sha256"],
            "request_hash": batch["request_hash"], "target": target,
            "units": batch["units"], "new_names": len(batch["names"]),
            "encoded_nodes": batch["nodes"], "evidence_bytes": batch["evidence_bytes"],
            "units_file": batch["units_pin"], "owner_statistics": batch["owner_statistics"]}, 2 * MIB)
        remaining_cpu = cpu_cap - (time.process_time() - cpu_start)
        remaining_wall = wall_cap - (time.monotonic() - started)
        need(remaining_cpu >= 5 and remaining_wall >= 20, "INSUFFICIENT_SUCCESSOR_BUDGET")
        evidence = tuple(inputs.read(path, 8 * MIB, expected=pin) for path, pin in batch["evidence"])
        grant = catalog.reserve_extension(PARENT, evidence, seconds=math.floor(remaining_wall) + 30,
                                          output_bytes=64 * MIB)
        need(grant.request_hash == batch["request_hash"], "LIVE_RESERVATION_REQUEST_BINDING")
        del evidence, prepared, parent, plan
        gc.collect()
        report_path = root / "call/worker-report.json"
        argv = [sys.executable, "-I", "-S", "-B", str(OLD_SOURCE / "run_native_admission.py"), "--worker",
                str(built), str(core), str(snapshots), "extend", str(plan_path), str(batch["units_path"]),
                grant.root, str(grant.directory / "chunk.olean"), str(report_path)]
        inputs.pin(plan_path, 16 * MIB, expected=plan_pin)
        inputs.pin(batch["units_path"], 64 * MIB, expected=batch["units_pin"])
        within()
        remaining_cpu = cpu_cap - (time.process_time() - cpu_start)
        remaining_wall = wall_cap - (time.monotonic() - started)
        need(remaining_cpu >= 5 and remaining_wall >= 20, "INSUFFICIENT_NATIVE_REMAINDER")
        allowance = A.limits_checked({"cpu_seconds": math.floor(remaining_cpu),
            "wall_seconds": math.floor(remaining_wall - 10), "memory_mib": ceiling["memory_mib"],
            "active_processes": 2, "stdout_bytes": MIB, "stderr_bytes": MIB})
        actual = A.supervise(argv, ROOT, root / "call/supervision", allowance, J.Job)
        A.save_new(root / "call/SUPERVISION.json", actual)
        final_job = actual.get("final_job")
        if type(final_job) is dict and type(final_job.get("cpu_seconds")) in (int, float):
            child_cpu = final_job["cpu_seconds"]
        need(G.clean_worker(actual), "SUCCESSOR_WORKER_FAILED_OR_UNCLEAN")
        for name in ("stdout.txt", "stderr.txt"):
            log = root / "call/supervision" / name
            C.ordinary(log)
            need(log.stat().st_size <= MIB, "SUCCESSOR_LOG_BOUND")
            with log.open("rb") as stream:
                need(b"PANIC" not in stream.read(MIB + 1).upper(), "NEW_NATIVE_DIAGNOSTIC_REQUIRES_REVIEW")
        within()
        inputs.verify()
        manifest.verify()
        raw_report = C.read_bounded(report_path, 16 * MIB)
        report = G.writer_json(raw_report, 16 * MIB)
        artifact = C.ordinary(grant.directory / "chunk.olean")
        need(type(report) is dict and set(report) == G.REPORT_FIELDS and
             report["schema"] == "DMKN_ORDINARY_WORKER_OUTPUT_V1" and report["kind"] == "extension" and
             report["module_name"] == C.module_name(grant.root) and report["parent_module"] == C.module_name(PARENT) and
             report["names"] == batch["names"] and type(report["units_checked"]) is int and
             report["units_checked"] == batch["units"] and type(report["artifact_bytes"]) is int and
             report["artifact_bytes"] == artifact.stat().st_size and 0 < report["artifact_bytes"] <= 64 * MIB,
             "ACTUAL_SUCCESSOR_REPORT_BINDING")
        within()
        accepted = catalog._commit_checked(grant)
        request_hash = grant.request_hash
        grant = None
        before = catalog.context(accepted)
        need(before["bindings"] == expected, "SUCCESSOR_EXACT_FINAL_BINDINGS")
        artifact_sha = catalog._record(accepted)["artifact_sha256"]
        catalog.close()
        catalog = C.LocalCatalog.open(root / "catalog", profile, STORE, limits=limits)
        after = catalog.context(accepted)
        need(after == before, "SUCCESSOR_REOPEN_CONTEXT")
        inputs.verify()
        manifest.verify()
        within()
        result = {"schema": "DMKN_ORDINARY_SUCCESSOR_ADMISSION_RESULT_V1",
            "status": "PASS_ACTUAL_NEW_SUCCESSOR_CHECKED_OVER_ADOPTED_PARENT", "profile_id": PROFILE,
            "store_id": STORE, "basis_id": BASIS, "parent": PARENT, "root": accepted,
            "target": target, "target_symbol_id": expected[E.name_key(target)], "request_hash": request_hash,
            "units_checked": batch["units"], "new_names": len(batch["names"]),
            "encoded_nodes": batch["nodes"], "evidence_bytes": batch["evidence_bytes"],
            "artifact_bytes": report["artifact_bytes"], "worker_report_sha256": sha(raw_report),
            "artifact_sha256": artifact_sha,
            "parent_manifest_sha256": inputs.pins[manifest_path]["sha256"],
            "bundle_sha256": inputs.pins[bundle_path]["sha256"],
            "prepare_manifest_sha256": inputs.pins[prepare_path]["sha256"],
            "worker_cpu_seconds": child_cpu, "controller_cpu_seconds": time.process_time() - cpu_start,
            "wall_seconds": time.monotonic() - started,
            "claims": "LOCAL_RECIPROCAL_CHECKED_EXTENSION_NOT_DISCOVERY_NOVELTY_GROWTH_OR_PUBLIC_RELEASE"}
        A.save_new(root / "SUCCESSOR-RESULT.json", result)
        print(json.dumps(result), flush=True)
        return 0
    finally:
        # The supervisor settles its Job before returning; never replay on a
        # failed or uncertain commit. Failed bytes and reservation stay charged.
        if grant is not None and not catalog._closed and catalog._grant is grant:
            catalog.abandon(grant)
        catalog.close()


if __name__ == "__main__":
    raise SystemExit(main())

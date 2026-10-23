"""One bounded real ordinary-basis/selected-closure integration, not a peer API.

Run only a root-selected immutable Run-V5-Check snapshot. This controller owns
the actual worker event; a saved report, caller environment or foreign .olean
cannot authorize promotion. No compilation, export regeneration or retry loop.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import os
import secrets
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
LEAN = ROOT / "software/runtime/lean-4.34.0-windows/bin/lean.exe"
SEED = ROOT / "software/assets/foundation/seed-verified.json"
INVENTORY = ROOT / "software/assets/foundation/seed-inventory-json.json"
MIB = 1024 * 1024
MAX_BATCHES = 32
MAX_EVIDENCE_BYTES = 128 * MIB
MAX_AUTHORED_BYTES = 256 * MIB
MAX_SCAN_NODES = 2097152
KERNEL_FILES = ("lean.exe", "libInit_shared.dll", "libleanshared.dll",
                "libleanshared_1.dll", "libleanshared_2.dll", "libc++.dll")
GROUPS = (("OriginalExpr", "OriginalDecl", "CheckedExtension"),
          ("LocalSnapshot",),
          ("BootstrapSupport", "OrdinaryExport", "BasisSnapshot", "OrdinaryWorkflowWorker"))
REPORT_FIELDS = {"schema", "kind", "module_name", "parent_module", "names",
                 "units_checked", "artifact_bytes"}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def local_path(value, *, directory=False):
    path = Path(value)
    need(path.is_absolute() and path.is_relative_to(LOCAL), "IMMUTABLE_LOCAL_PATH_REQUIRED")
    return C.ordinary(path, directory=directory)


def writer_json(raw, maximum):
    """Bounded lexical preflight before parsing our selected Lean JSON writer.

    Unlike evidence, the writer need not sort object keys or use Python's JSON
    escaping. Unsigned integer syntax/depth and duplicate keys are still checked
    before any producer claim is converted into canonical evidence.
    """
    need(type(raw) is bytes and 0 < len(raw) <= maximum, "WRITER_JSON_BYTES")
    stack, quoted, escaped, i = [], False, False, 0
    while i < len(raw):
        byte = raw[i]
        if quoted:
            need(byte >= 32, "WRITER_STRING_CONTROL")
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
            i += 1
            continue
        if byte == 34:
            quoted = True
        elif byte in (91, 123):
            stack.append(byte)
            need(len(stack) <= 64, "WRITER_JSON_DEPTH")
        elif byte in (93, 125):
            need(stack and stack.pop() == (91 if byte == 93 else 123), "WRITER_JSON_BRACKETS")
        elif 48 <= byte <= 57:
            start = i
            while i < len(raw) and 48 <= raw[i] <= 57:
                i += 1
                need(i - start <= 20, "WRITER_INTEGER_DIGITS")
            token = raw[start:i]
            need((len(token) == 1 or token[0] != 48) and
                 (len(token) < 20 or token <= b"18446744073709551615"), "WRITER_UINT64")
            continue
        else:
            need(byte in (9, 10, 13, 32, 44, 58), "WRITER_JSON_TOKEN")
        i += 1
    need(not quoted and not escaped and not stack, "WRITER_JSON_UNTERMINATED")

    def pairs(rows):
        found = {}
        for key, value in rows:
            need(key not in found, "WRITER_DUPLICATE_KEY")
            found[key] = value
        return found

    def reject(_):
        raise ValueError("WRITER_NONINTEGER")

    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=reject, parse_constant=reject)


class AuthoredFiles:
    def __init__(self):
        self.bytes = 0

    def write(self, path, raw, maximum):
        need(type(raw) is bytes and 0 < len(raw) <= maximum, "AUTHORED_FILE_BOUND")
        need(self.bytes + len(raw) <= MAX_AUTHORED_BYTES, "AUTHORED_TOTAL_BOUND")
        C.ordinary(path, fresh=True)
        with path.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        self.bytes += len(raw)
        return {"bytes": len(raw), "sha256": sha(raw)}

    def json(self, path, value, maximum):
        return self.write(path, E.canonical_json(value), maximum)


class SelectedInputs:
    def __init__(self, source, output, built, core, snapshots, bundle, A):
        self.A, self.pins = A, {}
        selection_raw = C.read_bounded(output / "selection.json", MIB)
        self.selection = A.strict(selection_raw)
        need(self.selection["schema"] == "DMKN_V5_LOCAL_CHECK_V1", "OUTER_SELECTION_SCHEMA")
        need(source.parents[3] == output, "SOURCE_OUTPUT_SNAPSHOT_BINDING")
        self.source, self.built, self.core, self.snapshots = source, built, core, snapshots
        self.snapshot_root = source.parents[2]
        self.source_rows, self.compiled_rows = {}, {}
        for name in ("ordinary_evidence.py", "local_catalog.py", "run_native_admission.py"):
            self.source_rows[name] = self.source_pin(source / name)
        for directory, modules in ((core, GROUPS[0]), (snapshots, GROUPS[1]), (built, GROUPS[2])):
            # Do not permit an extra selected-path binary to shadow runtime or
            # another selected module. Empty build subdirectories are harmless.
            artifacts = set()
            for path in directory.rglob("*"):
                if path.is_file():
                    C.ordinary(path)
                    artifacts.add(path.relative_to(directory).as_posix())
            need(artifacts == {module + ".olean" for module in modules}, "COMPILED_DIRECTORY_CENSUS")
            old = directory.parent / "sources/software/v5/ordinary_lean"
            for module in modules:
                self.source_rows[module + ".lean"] = self.source_pin(source / (module + ".lean"))
                prior = self.runtime_pin(old / (module + ".lean"), 2 * MIB)
                need(prior == self.source_rows[module + ".lean"], "CHANGED_COMPILED_SOURCE:" + module)
                self.compiled_rows[module + ".olean"] = self.runtime_pin(directory / (module + ".olean"))
        self.kernel_rows = {name: self.runtime_pin(LEAN.parent / name) for name in KERNEL_FILES}
        self.runtime_pin(Path(sys.executable))
        for name in ("python314.dll", "python3.dll"):
            self.runtime_pin(Path(sys.executable).parent / name)
        self.seed_pin = self.runtime_pin(SEED, MIB)
        self.inventory_pin = self.runtime_pin(INVENTORY, MIB)
        need(self.seed_pin == {"bytes": 724174, "sha256": C.SEED}, "EXACT_FIXED_SEED")
        need(self.inventory_pin == {"bytes": 823690, "sha256": C.INVENTORY}, "EXACT_FIXED_INVENTORY")
        self.bundle_pin = self.runtime_pin(bundle, 64 * MIB)

    def file_pin(self, path, maximum):
        C.ordinary(path)
        size = path.stat().st_size
        need(0 < size <= maximum, "SELECTED_FILE_SIZE")
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        need(path.stat().st_size == size, "SELECTED_FILE_SIZE_CHANGED")
        return {"bytes": size, "sha256": digest}

    def source_pin(self, path):
        relative = path.relative_to(self.snapshot_root).as_posix()
        actual = self.file_pin(path, 2 * MIB)
        need(self.selection["sources"].get(relative) == actual["sha256"], "OUTER_SOURCE_PIN:" + relative)
        self.pins[path] = actual
        return actual

    def runtime_pin(self, path, maximum=512 * MIB):
        actual = self.file_pin(path, maximum)
        need(self.selection["runtime_pins"].get(str(path)) == actual["sha256"], "OUTER_RUNTIME_PIN:" + str(path))
        self.pins[path] = actual
        return actual

    def assert_unchanged(self):
        # Finite selected binaries/support only, not a whole installation hash.
        # Owner storage immutability during each check remains a trust premise.
        for path, expected in self.pins.items():
            need(self.file_pin(path, max(expected["bytes"], 1)) == expected, "SELECTED_INPUT_CHANGED:" + str(path))

    def profile(self):
        basis_names = ("BootstrapSupport", "BasisSnapshot")
        basis = {"source": {name + ".lean": self.source_rows[name + ".lean"] for name in basis_names},
                 "compiled": {name + ".olean": self.compiled_rows[name + ".olean"] for name in basis_names}}
        adapter = {"source": self.source_rows, "compiled": self.compiled_rows}
        kernel = {"version": "Lean 4.34.0", "files": self.kernel_rows,
                  "scope": "EXPLICIT_NAMED_BINARIES_NOT_HERMETIC_TOOLCHAIN"}
        profile = {"schema": C.PROFILE,
            "kernel_support": C.digest("ordinary-kernel-support-v1", kernel),
            "adapter_support": C.digest("ordinary-adapter-support-v1", adapter),
            "basis_receiver_support": C.digest("ordinary-basis-receiver-support-v1", basis),
            "basis_seed": C.SEED, "basis_inventory": C.INVENTORY,
            "expression_format": E.EXPR_FORMAT, "declaration_format": E.UNIT_FORMAT,
            "axiom_policy": "FIXED_BASIS_NO_NEW_AXIOM_UNSAFE_SORRY",
            "snapshot_format": "LEAN_4_34_MODULEDATA_NO_EXTENSIONS_NO_IR"}
        C.profile_bytes(profile)
        return profile, {"kernel": kernel, "adapter": adapter, "basis_receiver": basis}


@dataclass(frozen=True)
class Batch:
    evidence: tuple[bytes, ...]
    raw_units: bytes
    names: tuple
    nodes: int


def prepare_bundle(bundle, fixed_names, profile_id, basis_id, files, evidence_directory):
    need(type(bundle) is dict and set(bundle) == {"schema", "assurance", "targets", "basis_names", "units", "stats"},
         "OWNER_BUNDLE_FIELDS")
    need(bundle["schema"] == "DMKN_ORDINARY_EXPORT_BUNDLE_V1" and
         bundle["assurance"] == "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE", "OWNER_BUNDLE_SCHEMA")
    need(bundle["basis_names"] == fixed_names, "EXACT_FIXED_BASIS_NAMES")
    units = bundle["units"]
    need(type(units) is list and 1 <= len(units) <= 8192, "OWNER_BUNDLE_UNIT_COUNT")
    stats = bundle["stats"]
    need(type(stats) is dict and set(stats) == {"source_records", "selected_units", "dependency_edges", "scan_nodes", "unit_json_bytes"}
         and all(type(x) is int and 0 <= x <= (1 << 64) - 1 for x in stats.values())
         and stats["selected_units"] == len(units), "OWNER_STATS_CENSUS")
    expected_target = [[0, {"$bytes": list(part.encode("utf-8"))}]
                       for part in ("DMKN", "ReadFootprint", "readsOnly_insertMany")]
    need(bundle["targets"] == [expected_target], "SELECTED_METHOD_TARGET")
    bindings = {E.name_key(name): E.basis_symbol_id(profile_id, basis_id, name) for name in fixed_names}
    need(len(bindings) == 581, "BASIS_UNIQUE_CENSUS")
    total_bytes, batches, current, raw_rows, names, nodes, raw_size, ev_size = 0, [], [], [], [], 0, 2, 0

    def finish():
        nonlocal current, raw_rows, names, nodes, raw_size, ev_size
        if current:
            raw = b"[" + b",".join(raw_rows) + b"]"
            need(len(raw) == raw_size, "BATCH_BYTE_ACCOUNTING")
            batches.append(Batch(tuple(current), raw, tuple(names), nodes))
            need(len(batches) <= MAX_BATCHES, "BATCH_COUNT_BOUND")
            current, raw_rows, names, nodes, raw_size, ev_size = [], [], [], 0, 2, 0

    for index, unit in enumerate(units):
        census = E.inspect_unit(unit)
        need(all(key in bindings for key in census.external_names), "UNCLOSED_OWNER_EXPORT_DEPENDENCY")
        imports = [[E.strict_json(key), bindings[key]] for key in census.external_names]
        raw = E.canonical_json({"schema": E.SCHEMA, "profile_id": profile_id, "imports": imports, "unit": unit})
        evidence = E.read_evidence(raw)
        unit_raw = E.canonical_json(unit)
        unit_names = [row[0] for row in unit[2]]
        need(census.total_nodes <= MAX_SCAN_NODES and len(unit_names) <= 65536,
             "SINGLE_UNIT_EXCEEDS_ADMISSION_DEFAULTS")
        need(len(unit_raw) + 2 <= 64 * MIB, "SINGLE_UNIT_BYTES")
        fits = (len(current) < 1024 and len(names) + len(unit_names) <= 65536 and
                nodes + census.total_nodes <= MAX_SCAN_NODES and
                raw_size + len(unit_raw) + bool(current) <= 64 * MIB and ev_size + len(raw) <= 64 * MIB)
        if not fits:
            finish()
        current.append(raw)
        raw_size += len(unit_raw) + bool(raw_rows)
        raw_rows.append(unit_raw)
        ev_size += len(raw)
        nodes += census.total_nodes
        names.extend(unit_names)
        total_bytes += len(raw)
        need(total_bytes <= MAX_EVIDENCE_BYTES, "TOTAL_EVIDENCE_BOUND")
        for name in unit_names:
            key = E.name_key(name)
            need(key not in bindings, "OWNER_EXPORT_OVERWRITE")
            bindings[key] = E.export_id(profile_id, evidence.unit_id, name)
        need(len(bindings) <= 1048576, "TOTAL_NAME_BOUND")
        files.write(evidence_directory / (f"{index:05d}.json"), raw, E.DEFAULT_LIMITS.max_bytes)
    finish()
    target_key = E.name_key(expected_target)
    need(target_key in bindings and target_key not in {E.name_key(x) for x in fixed_names}, "TARGET_NOT_EXPORTED")
    return batches, bindings, expected_target, {"units": len(units), "batches": len(batches),
        "evidence_bytes": total_bytes, "total_names": len(bindings), "owner_stats": stats}


def clean_worker(result):
    final = result.get("final_job")
    return (result.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED" and
            result.get("child_exit_code") == 0 and result.get("direct_child_reaped") is True and
            result.get("job_closed") is True and result.get("cleanup_errors") == [] and
            result.get("termination_requested") is False and type(final) is dict and
            final.get("active_processes") == 0 and final.get("terminated_processes") == 0)


def worker_mode(args):
    """Only selected launch plumbing: no catalog import, report adoption or commit."""
    need(len(args) >= 4, "WORKER_ARGUMENTS")
    source = Path(__file__).resolve().parent
    built, core, snapshots = map(Path, args[:3])
    command = args[3:]
    need(command[0] in ("basis", "extend") and len(command) == 6, "WORKER_FIXED_COMMAND")
    need(source.is_relative_to(LOCAL) and all(path.is_absolute() and path.is_relative_to(LOCAL)
         for path in (built, core, snapshots)), "WORKER_SELECTED_LOCAL_PATHS")
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON"))}
    env["LEAN_PATH"] = os.pathsep.join(map(str, (built, core, snapshots)))
    argv = [str(LEAN), "-R", str(source), "--run", str(source / "OrdinaryWorkflowWorker.lean"), *command]
    # The parent owns and settles the enclosing Windows Job; this process must
    # reap its Lean child before returning. No independent unsupervised worker.
    return subprocess.call(argv, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)


def main():
    global E, C
    started, controller_cpu = time.monotonic(), time.process_time()
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_CANONICAL_OWNER")
    if sys.argv[1:2] == ["--worker"]:
        return worker_mode(sys.argv[2:])
    need(len(sys.argv) == 6, "OUTPUT_WORKFLOW_CORE_SNAPSHOT_EXPORT_REQUIRED")
    source = Path(__file__).resolve().parent
    need(source.is_absolute() and source.is_relative_to(LOCAL), "IMMUTABLE_SOURCE_REQUIRED")
    E = load_module("ordinary_evidence", source / "ordinary_evidence.py")
    C = load_module("ordinary_local_catalog", source / "local_catalog.py")
    output, built, core, snapshots = [local_path(x, directory=True) for x in sys.argv[1:5]]
    bundle_path = local_path(sys.argv[5])
    runner_path = source.parents[2] / "tools/Run-V5-Check.py"
    R = load_module("ordinary_selected_outer_runner", runner_path)
    manifest = C.read_bounded(R.BASE / "RELEASE-MANIFEST.json", 8 * MIB)
    need(sha(manifest) == R.MANIFEST_SHA, "FROZEN_SUPERVISOR_MANIFEST")
    supervisor_files = json.loads(manifest)["files"]
    A = R.load("_ordinary_admission_supervisor", "operator/commons.py", supervisor_files)
    R.load("domains", "receiver/helpers/domains.py", supervisor_files)
    J = R.load("_ordinary_admission_job", "receiver/helpers/run_stage.py", supervisor_files)
    selected = SelectedInputs(source, output, built, core, snapshots, bundle_path, A)
    selected.source_pin(runner_path)
    profile, support = selected.profile()
    # Exact byte identity is established above, before parsing either fixed file.
    seed_raw, inventory_raw = C.read_bounded(SEED, MIB), C.read_bounded(INVENTORY, MIB)
    need(sha(seed_raw) == C.SEED and sha(inventory_raw) == C.INVENTORY, "FIXED_INPUT_CHANGED_BEFORE_PARSE")
    seed, inventory = writer_json(seed_raw, MIB), writer_json(inventory_raw, MIB)
    need(type(seed) is list and len(seed) == 3 and type(seed[1]) is list and len(seed[1]) == 456 and
         type(seed[2]) is list and len(seed[2]) == 581 and type(inventory) is list and len(inventory) == 581,
         "PINNED_BASIS_STRUCTURE")
    fixed_names = seed[2]
    need([row[0] for row in inventory] == fixed_names, "PINNED_INVENTORY_NAME_ORDER")
    bundle_raw = C.read_bounded(bundle_path, 64 * MIB)
    need(sha(bundle_raw) == selected.bundle_pin["sha256"], "EXPORT_BYTES_CHANGED")
    bundle = writer_json(bundle_raw, 64 * MIB)
    root = output / "native-admission"
    C.ordinary(root, directory=True, fresh=True).mkdir()
    (root / "evidence").mkdir()
    (root / "calls").mkdir()
    files = AuthoredFiles()
    profile_id = C.digest("ordinary-native-profile-v1", profile)
    basis_id = C.digest("ordinary-basis-root-v1", [profile_id, C.SEED, C.INVENTORY])
    batches, expected_bindings, target_name, summary = prepare_bundle(
        bundle, fixed_names, profile_id, basis_id, files, root / "evidence")
    files.json(root / "PROFILE.json", {"profile": profile, "support": support,
        "scope": "EXPLICIT_NATIVE_PINS_NOT_HERMETIC_TOOLCHAIN_OR_SECURITY_SANDBOX"}, 2 * MIB)
    files.json(root / "PLAN.json", {"schema": "DMKN_ORDINARY_ADMISSION_PLAN_V1", **summary,
        "profile_id": profile_id, "basis_id": basis_id, "export_sha256": selected.bundle_pin["sha256"],
        "batches": [{"units": len(b.evidence), "names": len(b.names), "nodes_upper_bound": b.nodes,
                     "units_bytes": len(b.raw_units), "evidence_bytes": sum(map(len, b.evidence))}
                    for b in batches]}, 2 * MIB)
    outer = selected.selection["limits"]
    cpu_cap, wall_cap = min(480, outer["cpu_seconds"] - 30), min(540, outer["wall_seconds"] - 30)
    need(cpu_cap >= 30 and wall_cap >= 30 and outer["active_processes"] >= 3,
         "MASTER_ENVELOPE_TOO_SMALL")
    child_cpu = 0.0
    store_id = secrets.token_hex(32)
    limits = C.Limits(max_roots=MAX_BATCHES + 1, max_operations=MAX_BATCHES + 1,
        max_artifact_bytes=64 * MIB, max_total_artifact_bytes=512 * MIB, max_db_pages=4096)
    catalog = C.LocalCatalog.open(root / "catalog", profile, store_id, create=True, limits=limits)
    steps = []

    def budget():
        remaining_cpu = cpu_cap - child_cpu - (time.process_time() - controller_cpu)
        remaining_wall = wall_cap - (time.monotonic() - started)
        need(remaining_cpu >= 5 and remaining_wall >= 20, "MASTER_BUDGET_EXHAUSTED")
        return A.limits_checked({"cpu_seconds": max(1, min(180, math.floor(remaining_cpu))),
            "wall_seconds": max(1, min(180, math.floor(remaining_wall - 10))),
            "memory_mib": min(1536, outer["memory_mib"]), "active_processes": 2,
            "stdout_bytes": MIB, "stderr_bytes": MIB})

    def execute(index, kind, batch=None):
        nonlocal child_cpu
        allowance = budget()
        parent = steps[-1]["root"] if steps else ""
        if kind == "basis":
            grant = catalog.reserve_basis(fixed_names, seconds=allowance["wall_seconds"] + 30,
                                          output_bytes=32 * MIB)
            expected_names, unit_count = fixed_names, 456
        else:
            grant = catalog.reserve_extension(parent, batch.evidence,
                seconds=allowance["wall_seconds"] + 30, output_bytes=64 * MIB)
            expected_names, unit_count = list(batch.names), len(batch.evidence)
        call = root / "calls" / f"{index:03d}-{kind}"
        call.mkdir()
        report_path = call / "worker-report.json"
        input_pins = {}
        try:
            if kind == "basis":
                args = ["basis", str(SEED), str(INVENTORY)]
                input_pins = {SEED: selected.seed_pin, INVENTORY: selected.inventory_pin}
            else:
                context = catalog.context(parent)
                plan = {"basis_module": C.module_name(catalog.basis_id),
                        "root_module": C.module_name(parent), "modules": context["modules"]}
                plan_path, units_path = call / "plan.json", call / "units.json"
                input_pins[plan_path] = files.json(plan_path, plan, 16 * MIB)
                input_pins[units_path] = files.write(units_path, batch.raw_units, 64 * MIB)
                args = ["extend", str(plan_path), str(units_path)]
            args += [grant.root, str(grant.directory / "chunk.olean"), str(report_path)]
            argv = [sys.executable, "-I", "-S", "-B", str(Path(__file__).resolve()), "--worker",
                    str(built), str(core), str(snapshots), *args]
            result = A.supervise(argv, ROOT, call / "supervision", allowance, J.Job)
            A.save_new(call / "SUPERVISION.json", result)
            need(clean_worker(result), "ACTUAL_WORKER_FAILED_OR_UNCLEAN")
            child_cpu += result["final_job"]["cpu_seconds"]
            need(child_cpu + time.process_time() - controller_cpu <= cpu_cap and
                 time.monotonic() - started <= wall_cap, "MASTER_BUDGET_EXCEEDED")
            # No saved PASS authorizes this branch: it is reachable only after
            # the selected invocation returned with its actual Job fully closed.
            selected.assert_unchanged()
            for path, expected in input_pins.items():
                need(selected.file_pin(path, expected["bytes"]) == expected, "WORKER_INPUT_CHANGED")
            raw_report = C.read_bounded(report_path, 16 * MIB)
            actual = writer_json(raw_report, 16 * MIB)
            artifact = C.ordinary(grant.directory / "chunk.olean")
            size = artifact.stat().st_size
            need(type(actual) is dict and set(actual) == REPORT_FIELDS and
                 actual["schema"] == "DMKN_ORDINARY_WORKER_OUTPUT_V1" and actual["kind"] == kind and
                 actual["module_name"] == C.module_name(grant.root) and
                 actual["parent_module"] == (C.module_name(parent) if parent else []) and
                 actual["names"] == expected_names and type(actual["units_checked"]) is int and
                 actual["units_checked"] == unit_count and type(actual["artifact_bytes"]) is int and
                 actual["artifact_bytes"] == size and 0 < size <= (32 if kind == "basis" else 64) * MIB,
                 "ACTUAL_WORKER_REPORT_BINDING")
            need(child_cpu + time.process_time() - controller_cpu <= cpu_cap and
                 time.monotonic() - started <= wall_cap, "MASTER_BUDGET_EXCEEDED_BEFORE_COMMIT")
            # _commit_checked independently flushes/authenticates the sole output
            # and atomically promotes the exact still-live reservation.
            accepted = catalog._commit_checked(grant)
            row = {"index": index, "kind": kind, "root": accepted, "parent": parent,
                "units": unit_count, "names": len(expected_names), "artifact_bytes": size,
                "worker_cpu_seconds": result["final_job"]["cpu_seconds"],
                "worker_report_sha256": sha(raw_report), "request_hash": grant.request_hash}
            steps.append(row)
            print(json.dumps(row), flush=True)
        except BaseException:
            # supervise always settles its Job before returning. An uncertain
            # catalog transaction can have closed the owner; never retry it.
            if not catalog._closed and catalog._grant is grant:
                catalog.abandon(grant)
            raise

    try:
        execute(0, "basis")
        for index, batch in enumerate(batches, 1):
            execute(index, "extension", batch)
        final_root = steps[-1]["root"]
        context = catalog.context(final_root)
        need(context["bindings"] == expected_bindings, "FINAL_CONTEXT_BINDING")
        catalog.close()
        catalog = C.LocalCatalog.open(root / "catalog", profile, store_id, limits=limits)
        reopened = catalog.context(final_root)
        need(reopened["bindings"] == expected_bindings and reopened["modules"] == context["modules"],
             "REOPEN_CONTEXT_BINDING")
        selected.assert_unchanged()
        need(child_cpu + time.process_time() - controller_cpu <= cpu_cap and
             time.monotonic() - started <= wall_cap, "MASTER_BUDGET_EXCEEDED_AT_REOPEN")
        result = {"schema": "DMKN_ORDINARY_NATIVE_ADMISSION_RESULT_V1",
            "status": "PASS_ACTUAL_CHECKED_BASIS_AND_SELECTED_EXTENSION_REOPEN",
            "profile_id": profile_id, "basis_id": basis_id, "root": final_root,
            "target": target_name, "target_symbol_id": expected_bindings[E.name_key(target_name)],
            "store_id": store_id, "steps": steps, "summary": summary,
            "known_worker_cpu_seconds": child_cpu,
            "controller_cpu_seconds": time.process_time() - controller_cpu,
            "wall_seconds": time.monotonic() - started,
            "authored_bytes": files.bytes,
            "claims": "ACTUAL_LOCAL_CHECKED_ADMISSION_AND_CATALOG_REOPEN_NOT_OWNER_BRIDGE_DISCOVERY_GROWTH_OR_RELEASE",
            "scope": "SELECTED_NONHERMETIC_NATIVE_TOOLCHAIN_OWNER_IMMUTABILITY_NO_SECURITY_SANDBOX"}
        A.save_new(root / "ADMISSION-RESULT.json", result)
        print(json.dumps(result), flush=True)
        return 0
    finally:
        catalog.close()


if __name__ == "__main__":
    raise SystemExit(main())

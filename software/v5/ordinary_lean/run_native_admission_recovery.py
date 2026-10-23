"""Root-selected recovery of one actual local admission, never foreign adoption.

No basis/prefix replay, old-state mutation, bundle parse, rebuild, retry loop or
semantic-profile change. This code is a fresh trusted controller selection.
The original catalog and all original failed evidence remain immutable.
"""
from contextlib import nullcontext
from pathlib import Path, PurePosixPath
import gc
import hashlib
import importlib.util
import json
import math
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
ORIGIN = LOCAL / "ordinary-native-admission-01"
OLD = ORIGIN / "native-admission"
SOURCE = ORIGIN / "sources/software/v5/ordinary_lean"
SELECTION = "ab2f655448242587880129e62cca4bc5dc74638c1e8699e30b4a9f67e26fce5f"
PROFILE = "fd23ae289706e5a3277a3c4304de83d65498755dd014b234810e79539f5c8219"
BASIS = "cb8f9c2db2b5b53984be1ce8b5f540024264a1e2db41fc7226c594ee1f022299"
PREFIX = "e0053044c9c3974bc4912e2083ff5f2340e5fd9e2326594e62de9c7b0421d201"
FAILED_ROOT = "4be468bdaa615733e9509cc7fc76a33b2f4b4d0d175ae237b991bce0200ae95c"
STORE = "12185a972a6302a0a70899e968f4c249d1994afd252ecbb74c91e59961b81eb5"
OPERATIONS = (
    "271479fcbce08ebc01dc64502a83b82e578d7897548e3bc7e2a1304eff582a51",
    "5f300d0fa7e48fa4efc8bf9e359bd5f552e0c8572b95142afbca7b45fa913221",
    "7160c6db37d6548f76f6fa319131ca50c8428147f85f278697a9613eddf1abcb")
CALLS = ("000-basis", "001-extension", "002-extension")
MIB = 1024 * 1024


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def bounded(path, maximum):
    need(path.is_absolute() and path.resolve() == path and path.is_file(), "FIXED_ORDINARY_FILE")
    size = path.stat().st_size
    need(0 <= size <= maximum, "FIXED_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    need(len(raw) == size, "FIXED_FILE_CHANGED")
    return raw


def trusted_json(raw):
    """Only byte-authenticated owner records, including finite timing floats."""
    def pairs(rows):
        result = {}
        for key, value in rows:
            need(key not in result, "TRUSTED_JSON_DUPLICATE")
            result[key] = value
        return result

    def reject(_):
        raise ValueError("TRUSTED_JSON_NONFINITE")

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=reject)


def load(name, path, expected):
    raw = bounded(path, 2 * MIB)
    need(sha(raw) == expected, "SELECTED_SOURCE_CHANGED:" + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def required_files():
    names = {"selection.json", "RESULT.json", "command/stdout.txt", "command/stderr.txt",
        "native-admission/PLAN.json", "native-admission/PROFILE.json",
        "native-admission/catalog/ADOPTION.json", "native-admission/catalog/catalog.sqlite",
        "native-admission/catalog/owner.lock"}
    names.update(f"native-admission/evidence/{index:05d}.json" for index in range(2852))
    for index, call in enumerate(CALLS):
        prefix = "native-admission/calls/" + call + "/"
        names.update(prefix + suffix for suffix in ("SUPERVISION.json", "supervision/stderr.txt"))
        if index < 2:
            names.add(prefix + "worker-report.json")
            names.add("native-admission/catalog/operations/" + OPERATIONS[index] + "/chunk.olean")
        if index > 0:
            names.update(prefix + suffix for suffix in ("plan.json", "units.json"))
    return names


class OriginFiles:
    def __init__(self, manifest):
        self.entries = manifest["files"]
        need(type(self.entries) is dict and set(self.entries) == required_files(), "ORIGIN_EXACT_FILE_INVENTORY")
        total = 0
        for relative, row in self.entries.items():
            path = PurePosixPath(relative)
            need(not path.is_absolute() and path.as_posix() == relative and
                 all(part not in (".", "..") for part in path.parts), "ORIGIN_RELATIVE_PATH")
            need(type(row) is dict and set(row) == {"bytes", "sha256"} and
                 type(row["bytes"]) is int and 0 <= row["bytes"] <= 64 * MIB, "ORIGIN_FILE_ENTRY")
            C.hexid(row["sha256"])
            total += row["bytes"]
        need(total <= 128 * MIB, "ORIGIN_TOTAL_BYTE_BOUND")

    def path(self, relative):
        need(relative in self.entries, "UNSELECTED_ORIGIN_FILE")
        return C.ordinary(ORIGIN.joinpath(*PurePosixPath(relative).parts))

    def verify(self, relative):
        path, expected = self.path(relative), self.entries[relative]
        need(path.stat().st_size == expected["bytes"], "ORIGIN_FILE_SIZE_CHANGED")
        with path.open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        need(actual == expected["sha256"] and path.stat().st_size == expected["bytes"], "ORIGIN_FILE_PIN")

    def read(self, relative, maximum):
        expected = self.entries[relative]
        need(expected["bytes"] <= maximum, "ORIGIN_READ_BOUND")
        raw = bounded(self.path(relative), maximum)
        need(len(raw) == expected["bytes"] and sha(raw) == expected["sha256"], "ORIGIN_READ_PIN")
        return raw

    def document(self, relative, maximum=2 * MIB):
        return trusted_json(self.read(relative, maximum))

    def verify_all(self):
        for relative in self.entries:
            self.verify(relative)


def closed(result, code):
    final = result.get("final_job")
    return (result.get("child_exit_code") == code and result.get("direct_child_reaped") is True and
        result.get("job_closed") is True and result.get("cleanup_errors") == [] and
        result.get("termination_requested") is False and type(final) is dict and
        final.get("active_processes") == 0 and final.get("terminated_processes") == 0)


def copy_catalog(origin, destination):
    """Byte copy of this exact quiescent owner store; never open original DB."""
    import msvcrt
    source = OLD / "catalog"
    expected_dirs = {"operations", *("operations/" + op for op in OPERATIONS)}
    expected_files = {"ADOPTION.json", "catalog.sqlite", "owner.lock",
        *("operations/" + op + "/chunk.olean" for op in OPERATIONS[:2])}
    actual_dirs, actual_files = set(), set()
    for path in source.rglob("*"):
        relative = path.relative_to(source).as_posix()
        if path.is_dir():
            C.ordinary(path, directory=True)
            actual_dirs.add(relative)
        else:
            C.ordinary(path)
            actual_files.add(relative)
    need(actual_dirs == expected_dirs and actual_files == expected_files, "ORIGINAL_CATALOG_EXACT_CENSUS")
    need(origin.read("native-admission/catalog/owner.lock", 1) == b"\0", "ORIGINAL_OWNER_LOCK")
    with (source / "owner.lock").open("r+b") as lock:
        msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        C.ordinary(destination, directory=True, fresh=True).mkdir()
        for relative in sorted(expected_dirs, key=lambda x: (x.count("/"), x)):
            destination.joinpath(*PurePosixPath(relative).parts).mkdir()
        for relative in sorted(expected_files):
            key = "native-admission/catalog/" + relative
            expected = origin.entries[key]
            target = destination.joinpath(*PurePosixPath(relative).parts)
            digest, count = hashlib.sha256(), 0
            with target.open("xb") as outgoing:
                if relative == "owner.lock":
                    lock.seek(0)
                    raw = lock.read(2)
                    need(raw == b"\0", "LOCK_CHANGED")
                    outgoing.write(raw)
                    digest.update(raw)
                    count = len(raw)
                else:
                    with origin.path(key).open("rb") as incoming:
                        while raw := incoming.read(MIB):
                            count += len(raw)
                            need(count <= expected["bytes"], "COPY_INPUT_GREW")
                            digest.update(raw)
                            outgoing.write(raw)
                outgoing.flush()
                os.fsync(outgoing.fileno())
            need(count == expected["bytes"] and digest.hexdigest() == expected["sha256"], "CATALOG_COPY_PIN")
            C.ordinary(target)
            with target.open("rb") as check:
                copied = hashlib.file_digest(check, "sha256").hexdigest()
            need(target.stat().st_size == count and copied == expected["sha256"], "CATALOG_COPY_READBACK")
        # Reading locked first byte through a different handle is unnecessary.
        for relative in expected_files - {"owner.lock"}:
            origin.verify("native-admission/catalog/" + relative)
        # Closing releases this OS lock. No old DB/catalog method was called.


def expected_argv(selected, index):
    base = [sys.executable, "-I", "-S", "-B", str(SOURCE / "run_native_admission.py"), "--worker",
            str(selected.built), str(selected.core), str(selected.snapshots)]
    call = OLD / "calls" / CALLS[index]
    if index == 0:
        args = ["basis", str(G.SEED), str(G.INVENTORY)]
    else:
        args = ["extend", str(call / "plan.json"), str(call / "units.json")]
    return base + args + [(BASIS, PREFIX, FAILED_ROOT)[index],
        str(OLD / "catalog/operations" / OPERATIONS[index] / "chunk.olean"), str(call / "worker-report.json")]


def validate_events(origin, selected, catalog, fixed_names):
    outer = origin.document("RESULT.json")
    need(outer["selection_sha256"] == SELECTION and closed(outer["result"], 1) and
         outer["result"]["status"] == "COMMAND_FAILED", "ORIGINAL_OUTER_EVENT")
    spent = outer["result"]["final_job"]["cpu_seconds"] + outer["wrapper_cpu_seconds"]
    need(spent == 7483 / 64, "ORIGINAL_KNOWN_SPEND_CHANGED")
    rows = [trusted_json(line) for line in origin.read("command/stdout.txt", MIB).splitlines() if line]
    need(len(rows) == 2 and [r["root"] for r in rows] == [BASIS, PREFIX], "ORIGINAL_COMMIT_EVENTS")
    records = [catalog._record(root) for root in (BASIS, PREFIX)]
    for index, row in enumerate(rows):
        call = "native-admission/calls/" + CALLS[index] + "/"
        supervision = origin.document(call + "SUPERVISION.json")
        need(G.clean_worker(supervision) and supervision["argv"] == expected_argv(selected, index),
             "ORIGINAL_ACTUAL_ACCEPTED_WORKER")
        report_raw = origin.read(call + "worker-report.json", 16 * MIB)
        report = G.writer_json(report_raw, 16 * MIB)
        record = records[index]
        expected_parent = "" if index == 0 else BASIS
        need(set(report) == G.REPORT_FIELDS and report["schema"] == "DMKN_ORDINARY_WORKER_OUTPUT_V1" and
             report["kind"] == ("basis" if index == 0 else "extension") and
             report["module_name"] == C.module_name(row["root"]) and
             report["parent_module"] == (C.module_name(expected_parent) if expected_parent else []) and
             report["units_checked"] == (456 if index == 0 else 1024) and
             report["artifact_bytes"] == record["artifact_bytes"] == row["artifact_bytes"] and
             row["worker_report_sha256"] == sha(report_raw) and row["request_hash"] == record["request_hash"] and
             row["parent"] == expected_parent and record["parent"] == expected_parent and
             record["operation"] == OPERATIONS[index] and record["profile_id"] == PROFILE,
             "ORIGINAL_REPORT_COMMIT_BINDING")
        need(report["names"] == (fixed_names if index == 0 else [x[0] for x in record["bindings"]]),
             "ORIGINAL_ACTUAL_NAME_CENSUS")
        artifact_key = "native-admission/catalog/operations/" + OPERATIONS[index] + "/chunk.olean"
        need(origin.entries[artifact_key] == {"bytes": record["artifact_bytes"],
             "sha256": record["artifact_sha256"]}, "ORIGINAL_COMMITTED_ARTIFACT")
    failed = origin.document("native-admission/calls/002-extension/SUPERVISION.json")
    need(closed(failed, 1) and failed["status"] == "COMMAND_FAILED" and
         failed["argv"] == expected_argv(selected, 2), "ORIGINAL_FAILED_WORKER_CLOSURE")
    need(not os.path.lexists(OLD / "calls/002-extension/worker-report.json"), "FAILED_REPORT_MUST_REMAIN_ABSENT")
    operations = catalog._db.execute("SELECT id,root,state,reserved_bytes FROM operations ORDER BY id").fetchall()
    need(set(operations) == {(OPERATIONS[0], BASIS, "COMMITTED", records[0]["artifact_bytes"]),
        (OPERATIONS[1], PREFIX, "COMMITTED", records[1]["artifact_bytes"]),
        (OPERATIONS[2], FAILED_ROOT, "FAILED_RETAINED", 64 * MIB)}, "PRESERVED_OPERATION_STATES")
    need({r[0] for r in catalog._db.execute("SELECT id FROM roots")} == {BASIS, PREFIX}, "EXACT_ACCEPTED_PREFIX")
    return records


def prepare_streamed(origin, plan, destination, fixed_names, records):
    """One parsed evidence at a time; retain only identities/name summaries."""
    bindings = {E.name_key(name): E.basis_symbol_id(PROFILE, BASIS, name) for name in fixed_names}
    need(records[0]["bindings"] == [[E.strict_json(key), value] for key, value in sorted(bindings.items())],
         "BASIS_BINDING_IDENTITY")
    start, total_bytes, prepared = 0, 0, []
    for index, expected in enumerate(plan["batches"], 1):
        prior = ("native-admission/calls/" + CALLS[index] + "/units.json") if index <= 2 else None
        file_path = origin.path(prior) if prior else destination / f"batch-{index:03d}-units.json"
        identities, names, introduced, nodes, evidence_bytes = [], [], [], 0, 0
        digest, size = hashlib.sha256(), 0
        with (nullcontext(None) if prior else file_path.open("xb")) as output:
            def emit(raw):
                nonlocal size
                size += len(raw)
                need(size <= 64 * MIB, "STREAMED_UNIT_BYTE_BOUND")
                if output is not None:
                    output.write(raw)
                digest.update(raw)
            emit(b"[")
            for offset in range(expected["units"]):
                raw = origin.read(f"native-admission/evidence/{start + offset:05d}.json", 8 * MIB)
                item = E.read_evidence(raw)
                need(item.document["profile_id"] == PROFILE, "ORIGINAL_EVIDENCE_PROFILE")
                for name, symbol in item.document["imports"]:
                    need(bindings.get(E.name_key(name)) == symbol, "ORIGINAL_EVIDENCE_DEPENDENCY")
                if offset:
                    emit(b",")
                unit_raw = E.canonical_json(item.document["unit"])
                emit(unit_raw)
                identities.append(item.unit_id)
                nodes += item.census.total_nodes
                evidence_bytes += len(raw)
                for row in item.document["unit"][2]:
                    name, key = row[0], E.name_key(row[0])
                    need(key not in bindings, "ORIGINAL_EVIDENCE_OVERWRITE")
                    symbol = E.export_id(PROFILE, item.unit_id, name)
                    bindings[key] = symbol
                    names.append(name)
                    introduced.append([name, symbol])
                # Do not retain any parsed declaration document across units.
                del item, raw, unit_raw
            emit(b"]")
            if output is not None:
                output.flush()
                os.fsync(output.fileno())
        actual = {"units": len(identities), "names": len(names), "nodes_upper_bound": nodes,
                  "units_bytes": size, "evidence_bytes": evidence_bytes}
        need(actual == expected and len(identities) <= 1024 and len(names) <= 65536 and
             nodes <= 2097152 and evidence_bytes <= 64 * MIB, "ORIGINAL_BATCH_PLAN_BINDING")
        request = C.digest("ordinary-batch-v1", identities)
        if index == 1:
            need(request == records[1]["request_hash"] and introduced == records[1]["bindings"],
                 "ACCEPTED_PREFIX_EXACT_EVIDENCE")
        if index <= 2:
            need(origin.entries[prior] == {"bytes": size, "sha256": digest.hexdigest()}, "OLD_UNITS_EXACT_BINDING")
        prepared.append({"start": start, "count": len(identities), "names": names,
            "request_hash": request, "path": file_path, "bytes": size, "sha256": digest.hexdigest()})
        start += len(identities)
        total_bytes += evidence_bytes
        del introduced, identities
    need(start == 2852 and total_bytes == plan["evidence_bytes"] and len(bindings) == plan["total_names"],
         "FINAL_EVIDENCE_PLAN_CENSUS")
    return prepared, bindings


def main():
    global E, C, G
    started, cpu_start = time.monotonic(), time.process_time()
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv) == 3, "SELECTED_RECOVERY_INVOCATION")
    source, output, manifest_path = Path(__file__).resolve(), Path(sys.argv[1]), Path(sys.argv[2])
    need(output.is_absolute() and output.is_relative_to(LOCAL) and source.parents[3] == output / "sources" and
         manifest_path.is_absolute() and manifest_path.is_relative_to(LOCAL), "RECOVERY_SNAPSHOT_PATHS")
    outer = trusted_json(bounded(output / "selection.json", MIB))
    need(outer["schema"] == "DMKN_V5_LOCAL_CHECK_V1" and outer["limits"]["cpu_seconds"] <= 360 and
         outer["limits"]["wall_seconds"] <= 420 and outer["limits"]["memory_mib"] <= 1536 and
         outer["limits"]["active_processes"] >= 3, "FINITE_REMAINING_SELECTION")
    relative = source.relative_to(output / "sources").as_posix()
    need(sha(bounded(source, 2 * MIB)) == outer["sources"][relative], "RECOVERY_SOURCE_PIN")
    manifest_raw = bounded(manifest_path, 2 * MIB)
    need(outer["runtime_pins"].get(str(manifest_path)) == sha(manifest_raw), "RECOVERY_MANIFEST_PIN")
    manifest = trusted_json(manifest_raw)
    need(type(manifest) is dict and set(manifest) == {"schema", "origin", "original_selection_sha256", "profile_id",
        "basis_id", "accepted_root", "store_id", "known_spent_cpu_ticks64", "disposition", "files"} and
        manifest["schema"] == "DMKN_ORDINARY_ADMISSION_RECOVERY_V1" and manifest["origin"] == str(ORIGIN) and
        manifest["original_selection_sha256"] == SELECTION and manifest["profile_id"] == PROFILE and
        manifest["basis_id"] == BASIS and manifest["accepted_root"] == PREFIX and manifest["store_id"] == STORE and
        manifest["known_spent_cpu_ticks64"] == 7483 and
        manifest["disposition"] == "ADOPTED_FIXED_ORIGIN_AFTER_KERNEL_SNAPSHOT_REVIEW", "FIXED_ROOT_ADOPTED_RECOVERY")
    original_raw = bounded(ORIGIN / "selection.json", MIB)
    need(sha(original_raw) == SELECTION, "ORIGINAL_SELECTION_ANCHOR")
    original = trusted_json(original_raw)
    for path, pin in original["runtime_pins"].items():
        need(outer["runtime_pins"].get(path) == pin, "ORIGINAL_RUNTIME_PIN_NOT_RETAINED:" + path)
    def old_module(name, filename):
        key = "software/v5/ordinary_lean/" + filename
        return load(name, SOURCE / filename, original["sources"][key])
    E = old_module("ordinary_evidence", "ordinary_evidence.py")
    C = old_module("ordinary_recovery_catalog", "local_catalog.py")
    G = old_module("ordinary_original_admission", "run_native_admission.py")
    G.E, G.C = E, C
    runner_path = ORIGIN / "sources/tools/Run-V5-Check.py"
    R = load("ordinary_recovery_runner", runner_path, original["sources"]["tools/Run-V5-Check.py"])
    release = C.read_bounded(R.BASE / "RELEASE-MANIFEST.json", 8 * MIB)
    need(sha(release) == R.MANIFEST_SHA, "FROZEN_SUPERVISOR_MANIFEST")
    supervisor_files = trusted_json(release)["files"]
    A = R.load("ordinary_recovery_supervisor", "operator/commons.py", supervisor_files)
    R.load("domains", "receiver/helpers/domains.py", supervisor_files)
    J = R.load("ordinary_recovery_job", "receiver/helpers/run_stage.py", supervisor_files)
    built, core, snapshots, bundle = map(Path, original["argv"][-4:])
    selected = G.SelectedInputs(SOURCE, ORIGIN, built, core, snapshots, bundle, A)
    selected.source_pin(runner_path)
    profile, support = selected.profile()
    need(C.digest("ordinary-native-profile-v1", profile) == PROFILE, "UNCHANGED_ORIGINAL_PROFILE")
    origin = OriginFiles(manifest)
    origin.verify_all()
    retained_profile = origin.document("native-admission/PROFILE.json")
    need(retained_profile["profile"] == profile and retained_profile["support"] == support, "ORIGINAL_PROFILE_SUPPORT")
    plan = origin.document("native-admission/PLAN.json")
    need(plan["profile_id"] == PROFILE and plan["basis_id"] == BASIS and plan["units"] == 2852 and
         [row["units"] for row in plan["batches"]] == [1024, 1024, 804] and
         plan["export_sha256"] == selected.bundle_pin["sha256"], "ACTUAL_ORIGINAL_BATCH_PLAN")
    adoption = origin.document("native-admission/catalog/ADOPTION.json")
    need(adoption["profile"] == profile and adoption["store_id"] == STORE and adoption["schema"] == C.SCHEMA,
         "ORIGINAL_STORE_ADOPTION")
    limits = C.Limits(**adoption["limits"])
    root = output / "native-recovery"
    C.ordinary(root, directory=True, fresh=True).mkdir()
    (root / "prepared").mkdir()
    (root / "calls").mkdir()
    copy_catalog(origin, root / "catalog")
    catalog = C.LocalCatalog.open(root / "catalog", profile, STORE, limits=limits)
    known_children, steps = 0.0, []
    cpu_cap = min(350, outer["limits"]["cpu_seconds"] - 10)
    wall_cap = min(400, outer["limits"]["wall_seconds"] - 20)
    need(cpu_cap >= 30 and wall_cap >= 30, "REMAINING_ENVELOPE_TOO_SMALL")
    def within():
        need(known_children + time.process_time() - cpu_start <= cpu_cap and
             time.monotonic() - started <= wall_cap, "RECOVERY_MASTER_ENVELOPE")
    try:
        seed_raw = C.read_bounded(G.SEED, MIB)
        need(sha(seed_raw) == C.SEED, "FIXED_SEED_BEFORE_PARSE")
        seed = G.writer_json(seed_raw, MIB)
        fixed_names = seed[2]
        records = validate_events(origin, selected, catalog, fixed_names)
        accepted_context = catalog.context(PREFIX)
        prepared, final_bindings = prepare_streamed(origin, plan, root / "prepared", fixed_names, records)
        need(accepted_context["bindings"] == {E.name_key(name): symbol for record in records
             for name, symbol in record["bindings"]}, "RELOCATED_PREFIX_BINDINGS")
        original_parent_plan = origin.document("native-admission/calls/002-extension/plan.json", 16 * MIB)
        expected_old_modules = [{**row, "path": str(OLD / "catalog/operations" / OPERATIONS[index] / "chunk.olean")}
                                for index, row in enumerate(accepted_context["modules"])]
        need(original_parent_plan == {"basis_module": C.module_name(BASIS), "root_module": C.module_name(PREFIX),
             "modules": expected_old_modules}, "ORIGINAL_FAILED_PARENT_CONTEXT")
        del seed, seed_raw, records, accepted_context, original_parent_plan, expected_old_modules
        gc.collect()
        parent = PREFIX
        for index in (1, 2):
            batch = prepared[index]
            within()
            need(cpu_cap - known_children - (time.process_time() - cpu_start) >= 5 and
                 wall_cap - (time.monotonic() - started) >= 20, "RECOVERY_INSUFFICIENT_REMAINING_BUDGET")
            allowance = A.limits_checked({"cpu_seconds": max(1, min(180, math.floor(cpu_cap - known_children -
                (time.process_time() - cpu_start)))), "wall_seconds": max(1, min(180, math.floor(wall_cap -
                (time.monotonic() - started) - 10))), "memory_mib": outer["limits"]["memory_mib"],
                "active_processes": 2, "stdout_bytes": MIB, "stderr_bytes": MIB})
            # Only immutable raw bytes for this one reservation are retained.
            evidence = tuple(origin.read(f"native-admission/evidence/{number:05d}.json", 8 * MIB)
                             for number in range(batch["start"], batch["start"] + batch["count"]))
            grant = catalog.reserve_extension(parent, evidence, seconds=allowance["wall_seconds"] + 30,
                                               output_bytes=64 * MIB)
            del evidence
            need(grant.request_hash == batch["request_hash"], "FRESH_RESERVATION_EXACT_REQUEST")
            if index == 1:
                need(grant.root == FAILED_ROOT and grant.identifier != OPERATIONS[2], "FRESH_FAILED_BATCH_GRANT")
            call = root / "calls" / f"{index + 1:03d}-extension"
            call.mkdir()
            try:
                context = catalog.context(parent)
                input_plan = {"basis_module": C.module_name(BASIS), "root_module": C.module_name(parent),
                              "modules": context["modules"]}
                files = G.AuthoredFiles()
                plan_path = call / "plan.json"
                plan_pin = files.json(plan_path, input_plan, 16 * MIB)
                report_path = call / "worker-report.json"
                argv = [sys.executable, "-I", "-S", "-B", str(SOURCE / "run_native_admission.py"), "--worker",
                    str(built), str(core), str(snapshots), "extend", str(plan_path), str(batch["path"]), grant.root,
                    str(grant.directory / "chunk.olean"), str(report_path)]
                del context, input_plan, files
                gc.collect()
                within()
                actual = A.supervise(argv, ROOT, call / "supervision", allowance, J.Job)
                A.save_new(call / "SUPERVISION.json", actual)
                final_job = actual.get("final_job")
                if type(final_job) is dict and type(final_job.get("cpu_seconds")) in (int, float):
                    known_children += final_job["cpu_seconds"]
                need(G.clean_worker(actual), "RECOVERY_WORKER_FAILED_OR_UNCLEAN")
                selected.assert_unchanged()
                need(selected.file_pin(plan_path, plan_pin["bytes"]) == plan_pin and
                     selected.file_pin(batch["path"], batch["bytes"]) == {"bytes": batch["bytes"],
                     "sha256": batch["sha256"]}, "RECOVERY_WORKER_INPUT_BINDING")
                raw_report = C.read_bounded(report_path, 16 * MIB)
                report = G.writer_json(raw_report, 16 * MIB)
                artifact = C.ordinary(grant.directory / "chunk.olean")
                need(type(report) is dict and set(report) == G.REPORT_FIELDS and
                     report["schema"] == "DMKN_ORDINARY_WORKER_OUTPUT_V1" and report["kind"] == "extension" and
                     report["module_name"] == C.module_name(grant.root) and report["parent_module"] == C.module_name(parent) and
                     report["names"] == batch["names"] and report["units_checked"] == batch["count"] and
                     type(report["artifact_bytes"]) is int and report["artifact_bytes"] == artifact.stat().st_size and
                     0 < report["artifact_bytes"] <= 64 * MIB, "RECOVERY_ACTUAL_REPORT_BINDING")
                within()
                accepted = catalog._commit_checked(grant)
                step = {"index": index + 1, "root": accepted, "parent": parent, "units": batch["count"],
                    "names": len(batch["names"]), "artifact_bytes": report["artifact_bytes"],
                    "worker_report_sha256": sha(raw_report), "request_hash": grant.request_hash,
                    "worker_cpu_seconds": actual["final_job"]["cpu_seconds"]}
                steps.append(step)
                parent = accepted
                print(json.dumps(step), flush=True)
                del report, raw_report, actual
            except BaseException:
                if not catalog._closed and catalog._grant is grant:
                    catalog.abandon(grant)
                raise
        before = catalog.context(parent)
        need(before["bindings"] == final_bindings, "RECOVERY_FINAL_BINDINGS")
        catalog.close()
        catalog = C.LocalCatalog.open(root / "catalog", profile, STORE, limits=limits)
        after = catalog.context(parent)
        need(before == after, "RECOVERY_REOPEN_CONTEXT")
        origin.verify_all()
        selected.assert_unchanged()
        within()
        target = [[0, {"$bytes": list(part.encode())}] for part in ("DMKN", "ReadFootprint", "readsOnly_insertMany")]
        need(E.name_key(target) in after["bindings"], "RECOVERY_TARGET_ABSENT")
        result = {"schema": "DMKN_ORDINARY_NATIVE_RECOVERY_RESULT_V1",
            "status": "PASS_ACTUAL_REMAINING_ADMISSION_WITH_PROTECTED_PREFIX_REUSE",
            "origin": str(ORIGIN), "original_selection_sha256": SELECTION, "reused_roots": [BASIS, PREFIX],
            "profile_id": PROFILE, "store_id": STORE, "root": parent, "steps": steps,
            "target": target, "target_symbol_id": after["bindings"][E.name_key(target)],
            "original_known_cpu_seconds": 7483 / 64, "recovery_known_worker_cpu_seconds": known_children,
            "recovery_controller_cpu_seconds": time.process_time() - cpu_start,
            "recovery_wall_seconds": time.monotonic() - started,
            "claims": "REAL_LOCAL_CHECKED_CLOSURE_AND_REOPEN_NOT_FRONTEND_COMPATIBILITY_DISCOVERY_GROWTH_OR_RELEASE",
            "scope": "ROOT_ADOPTED_FIXED_ORIGIN_NOT_GENERIC_FOREIGN_CATALOG_OR_REPORT_TRUST"}
        A.save_new(root / "RECOVERY-RESULT.json", result)
        print(json.dumps(result), flush=True)
        return 0
    finally:
        catalog.close()


if __name__ == "__main__":
    raise SystemExit(main())

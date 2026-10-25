"""SOURCE-selected fixed-basis controls; never mathematical acceptance.

Real binding/path/hash/SQLite validators operate on visibly synthetic fixtures.
Activation authority and the runtime's installation/supervisor are disclosed
doubles. No Lean, existing protected state, network or child process is used.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import stat
import sys
import time
from types import SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()
CASES = []


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic() - START < 60 and time.process_time() - CPU < 30,
         "CONTROL_ORIGINAL_ALLOWANCE")


def refusal(code, action, exception=ValueError):
    try:
        action()
    except exception as error:
        need(code in str(error), "WRONG_REFUSAL:" + str(error))
        return
    raise AssertionError("MISSING_REFUSAL:" + code)


def case(label, action):
    check()
    action()
    CASES.append(label)


def module(identifier, path):
    need(identifier not in sys.modules and path.is_absolute() and
         ".." not in path.parts, "CONTROL_FIXED_SOURCE")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             (getattr(info, "st_file_attributes", 0) & 0x400), "CONTROL_SOURCE_REDIRECTION")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "CONTROL_SOURCE_KIND")
    with path.open("rb") as stream:
        raw = stream.read(2 * MIB + 1)
    need(0 < len(raw) <= 2 * MIB, "CONTROL_SOURCE_BOUND")
    spec = importlib.util.spec_from_file_location(identifier, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[identifier] = value
    exec(compile(raw, str(path), "exec", dont_inherit=True), value.__dict__)
    need(Path(value.__file__).absolute() == path, "CONTROL_SOURCE_IDENTITY")
    return value, {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def name(text):
    return [[0, {"$bytes": list(text.encode("ascii"))}]]


def fresh(path, raw):
    P.PortableCatalog._write_fresh(path, raw)


class Fixture:
    """Fresh nonmathematical catalog; only _active is an authority double.

    The real context, _root_row, _validate_record and artifact validators run.
    Fake basis names and fake artifact bytes explicitly lack Lean acceptance.
    The genuine Windows owner lock protects only these synthetic fixtures.
    """
    def __init__(self, root, *, payload=b"SYNTHETIC-NOT-A-LEAN-OBJECT\n"):
        import msvcrt
        root.mkdir()
        self.root, self.payload = root, payload
        self.native = native = object.__new__(P.PortableCatalog)
        native._root, native._store_id, native._limits = root, "1" * 64, P.Limits()
        native.semantic_id, native.foundation_id = S.semantic_id(), S.foundation_id()
        implementation = dict(schema=S.IMPLEMENTATION_SCHEMA, semantic_id=native.semantic_id,
            platform=dict(os="windows", architecture="x86_64", word_bits=64, byte_order="little"),
            snapshot_format="LEAN_4_34_MODULEDATA_NO_EXTENSIONS_NO_IR",
            support_scope="EXPLICIT_NAMED_SUPPORT_NOT_HERMETIC_TOOLCHAIN")
        implementation.update({key: str(i + 2) * 64 for i, key in enumerate(P.SUPPORT_FIELDS)})
        native._implementation_raw = E.canonical_json(implementation)
        native.implementation_id = S.implementation_id(native._implementation_raw)
        native._current_support = sorted({implementation[key] for key in P.SUPPORT_FIELDS})
        native._basis_request = P.basis_request_id(native.semantic_id, native.foundation_id)
        native._basis_root = S.local_root_id(native._implementation_raw, native._store_id,
                                             "basis", "", native._basis_request)
        self.activation = dict(schema=P.ACTIVATION_SCHEMA, semantic_id=native.semantic_id,
            foundation_id=native.foundation_id, implementation_id=native.implementation_id,
            store_id=native._store_id, state="ACTIVE", origin="native-bootstrap",
            basis_root=native._basis_root)
        native._activation_raw = E.canonical_json(self.activation)
        native._marker = E.canonical_json(dict(schema=P.SCHEMA, store_id=native._store_id,
                                               implementation=implementation, limits=vars(native._limits)))
        native._active = lambda: deepcopy(self.activation)  # Explicit authority seam.
        native._verified_artifacts = set()
        fresh(root / "ADOPTION.json", native._marker)
        fresh(root / "owner.lock", b"\0")
        native._lock = (root / "owner.lock").open("r+b")
        msvcrt.locking(native._lock.fileno(), msvcrt.LK_NBLCK, 1)
        native._db = sqlite3.connect(root / "catalog.sqlite", isolation_level=None)
        native._db.execute("PRAGMA journal_mode=DELETE")
        native._db.execute("CREATE TABLE meta(id INTEGER PRIMARY KEY, marker BLOB, activation BLOB)")
        native._db.execute("CREATE TABLE roots(id TEXT PRIMARY KEY, parent TEXT, record BLOB)")
        native._db.execute("CREATE TABLE operations(id TEXT PRIMARY KEY, root TEXT, state TEXT, reserved_bytes INTEGER)")
        native._db.execute("CREATE TABLE imports(id TEXT PRIMARY KEY)")
        native._db.execute("INSERT INTO meta VALUES(1,?,?)", (native._marker, native._activation_raw))
        (root / "operations").mkdir()
        basis_names = [name("synthetic_basis_" + str(i)) for i in range(581)]
        bindings = [[n, S.basis_symbol_id(native.semantic_id, native.foundation_id, n)] for n in basis_names]
        self.basis = self.record("basis", "", native._basis_request, [], bindings, "a" * 64, payload)
        unit_id = "b" * 64
        self.extension = self.record("extension", native._basis_root, P.batch_id([unit_id]),
            [unit_id], [[name("synthetic_extension"), "c" * 64]], "d" * 64, b"FAKE-EXTENSION\n")
        self.selected = self.extension["local_root"]
        self.context = native.context(self.selected)
        self.binding, actual_context = H.capture(native, self.selected, check=check)
        need(actual_context == self.context, "FIXTURE_CONTEXT")
        self.doc = E.strict_json(self.binding)
        self.artifact = Path(self.doc["basis"]["artifact_path"])

    def record(self, kind, parent, request, units, bindings, operation, payload):
        native = self.native
        root_id = S.local_root_id(native._implementation_raw, native._store_id, kind, parent, request)
        directory = self.root / "operations" / operation
        directory.mkdir()
        fresh(directory / "chunk.olean", payload)
        row = dict(schema=P.ROOT_SCHEMA, local_root=root_id, parent_root=parent, kind=kind,
            semantic_id=native.semantic_id, foundation_id=native.foundation_id,
            input_unit_ids=units, request_hash=request, bindings=bindings,
            snapshot=dict(module_name=P.L.module_name(root_id),
                parent_module=P.L.module_name(parent) if parent else [],
                relative_path="operations/" + operation + "/chunk.olean",
                artifact_bytes=len(payload), artifact_sha256=hashlib.sha256(payload).hexdigest(),
                writer_origin="native-check"), origin="native-check",
            provenance=dict(implementation_id=native.implementation_id, operation_id=operation))
        native._db.execute("INSERT INTO roots VALUES(?,?,?)", (root_id, parent, E.canonical_json(row)))
        native._db.execute("INSERT INTO operations VALUES(?,?,?,?)",
                           (operation, root_id, "COMMITTED", len(payload)))
        return row

    def close_native(self):
        if self.native._db is not None:
            self.native._db.close()
            self.native._db = None
        if self.native._lock is not None:
            self.native._lock.close()

    def anchor(self, callback=check):
        self.close_native()
        return H.SourceAnchor.open(self.binding, check=callback)


def binding_controls(fixture):
    doc = fixture.doc
    need(doc["basis"]["basis_root"] == fixture.basis["local_root"] and
         doc["selected_root"] == fixture.selected and
         doc["basis"]["artifact_path"] != fixture.context["modules"][-1]["path"] and
         doc["basis"]["record_sha256"] == hashlib.sha256(E.canonical_json(fixture.basis)).hexdigest(),
         "CAPTURE_MUST_SELECT_COMMITTED_BASIS_NOT_SELECTED_EXTENSION")
    case("capture-committed-basis-not-extension", lambda: None)
    changes = [
        ("old-v1-binding", "BINDING_FIELDS", lambda d: (d.pop("basis"), d.update(schema="DMKN_GROUNDED_CUT_NATIVE_SUPPORT_ANCHOR_V1"))),
        ("wrong-basis-root", "BASIS_ORIGIN_BINDING", lambda d: d["basis"].update(basis_root="f" * 64)),
        ("nonzero-parent", "BASIS_ORIGIN_BINDING", lambda d: d["basis"].update(parent_root="f" * 64)),
        ("nonempty-parent-module", "BASIS_ORIGIN_BINDING", lambda d: d["basis"].update(parent_module=name("wrong"))),
        ("wrong-basis-request", "BASIS_ORIGIN_BINDING", lambda d: d["basis"].update(request_hash="f" * 64)),
        ("wrong-basis-module", "BASIS_FIXED_PROFILE", lambda d: d["basis"].update(module_name=name("wrong"))),
        ("wrong-fixed-count", "BASIS_FIXED_PROFILE", lambda d: d["basis"].update(names_count=580)),
        ("wrong-seed", "BASIS_FIXED_PROFILE", lambda d: d["basis"].update(seed_sha256="f" * 64)),
        ("wrong-inventory", "BASIS_FIXED_PROFILE", lambda d: d["basis"].update(inventory_sha256="f" * 64)),
        ("relative-path-escape", "BASIS_ARTIFACT_PATH", lambda d: d["basis"].update(relative_path="../chunk.olean")),
        ("different-absolute-path", "BASIS_ARTIFACT_PATH", lambda d: d["basis"].update(artifact_path=str(fixture.root / "wrong.olean"))),
        ("zero-artifact-size", "BASIS_ARTIFACT_BOUND", lambda d: d["basis"].update(artifact_bytes=0)),
        ("artifact-cap", "BASIS_ARTIFACT_BOUND", lambda d: d["basis"].update(artifact_bytes=H.MAX_BASIS_BYTES + 1)),
    ]
    for label, code, mutate in changes:
        altered = deepcopy(doc)
        mutate(altered)
        case("binding-" + label, lambda value=altered, expected=code:
             refusal(expected, lambda: H.parse_binding(E.canonical_json(value))))


def capture_controls(fixture):
    native = fixture.native
    # A context double supplies an unchanged plausible context: capture must
    # separately validate its basis row and committed operation, not trust it.
    with patch.object(native, "context", lambda selected: deepcopy(fixture.context)):
        for field, value in (("origin", "legacy-translation"), ("parent_root", "f" * 64),
                             ("kind", "extension")):
            row = deepcopy(fixture.basis)
            row[field] = value
            with patch.object(native, "_root_row", lambda root, r=row: (E.canonical_json(r), r)):
                case("capture-refuses-basis-" + field, lambda: refusal("COMMITTED_NATIVE_BASIS_REQUIRED",
                     lambda: H.capture(native, fixture.selected, check=check)))
        for field, value in (("state", "RUNNING"), ("root", "f" * 64), ("reserved_bytes", 1)):
            original = ("COMMITTED" if field == "state" else fixture.basis["local_root"]
                        if field == "root" else len(fixture.payload))
            native._db.execute("UPDATE operations SET " + field + "=? WHERE id=?", (value, "a" * 64))
            try:
                case("capture-operation-" + field, lambda: refusal("PORTABLE_NATIVE_OPERATION_BINDING",
                     lambda: H.capture(native, fixture.selected, check=check)))
            finally:
                native._db.execute("UPDATE operations SET " + field + "=? WHERE id=?", (original, "a" * 64))
    with patch.object(native, "_lock", None):
        case("capture-requires-live-lock", lambda: refusal("LIVE_NATIVE_BOOTSTRAP_REQUIRED",
             lambda: H.capture(native, fixture.selected, check=check)))


def snapshot_controls(output):
    fixture = Fixture(output / "snapshot-success", payload=b"S" * (H.HASH_CHUNK + 7))
    calls = []
    def callback():
        check()
        calls.append(None)
    anchor = fixture.anchor(callback)
    try:
        traced = []
        anchor._db.set_trace_callback(traced.append)
        before = len(calls)
        snapshot = anchor.basis_snapshot()
        need(set(snapshot) == {"module_name", "path", "artifact_bytes"} and
             snapshot["path"] == str(fixture.artifact) and
             snapshot["artifact_bytes"] == len(fixture.payload) and len(calls) - before == 7,
             "EXACT_DESCRIPTOR_AND_PER_CHUNK_CALLBACKS")
        need(traced == ["SELECT length(marker),length(activation) FROM meta WHERE id=1",
                        "SELECT marker,activation FROM meta WHERE id=1"] * 2,
             "UNCHANGED_BEFORE_AFTER_METADATA_NO_HISTORY")
        snapshot["module_name"].append([1, 99])
        need(anchor.basis_snapshot()["module_name"] == fixture.doc["basis"]["module_name"],
             "SNAPSHOT_RETURN_MUTATES_ANCHOR")
        case("snapshot-detached-exact-three-fields-and-full-check-cadence", lambda: None)
        # Deliberate corruption is confined to this fresh synthetic artifact.
        with fixture.artifact.open("r+b") as stream:
            stream.write(b"T")
        refusal("BASIS_ARTIFACT_DIGEST", anchor.basis_snapshot)
        refusal("CLOSED_OR_WITHDRAWN", anchor.basis_snapshot)
        case("snapshot-rehash-each-event-and-sticky-digest-denial", lambda: None)
    finally:
        anchor.close()
    scenarios = ("size", "path", "missing", "withdrawn", "lock", "budget")
    for mode in scenarios:
        fixture = Fixture(output / ("snapshot-" + mode))
        anchor = fixture.anchor()
        try:
            if mode == "size":
                with fixture.artifact.open("ab") as stream:
                    stream.write(b"x")
                code = "BASIS_ARTIFACT_SIZE"
            elif mode == "path":
                anchor._doc["basis"]["artifact_path"] = str(fixture.root / "wrong.olean")
                code = "BASIS_ARTIFACT_PATH"
            elif mode == "missing":
                fixture.artifact.rename(fixture.artifact.with_suffix(".retained"))
                code = "CATALOG_MISSING_PATH"
            elif mode == "withdrawn":
                fresh(fixture.root / "WITHDRAWN", b"synthetic withdrawal\n")
                code = "GROUNDED_SOURCE_WITHDRAWN"
            elif mode == "lock":
                anchor._lock.close()
                code = "NATIVE_LOCK_LOST"
            else:
                calls = []
                def exhausted():
                    check()
                    calls.append(None)
                    if len(calls) == 3:  # First hashing callback, after both initial checks.
                        raise ValueError("SYNTHETIC_ORIGINAL_BUDGET_EXHAUSTED")
                anchor._check = exhausted
                code = "SYNTHETIC_ORIGINAL_BUDGET_EXHAUSTED"
            refusal(code, anchor.basis_snapshot)
            if mode == "withdrawn":
                (fixture.root / "WITHDRAWN").rename(fixture.root / "WITHDRAWN.retained")
            anchor._check = check
            refusal("CLOSED_OR_WITHDRAWN", anchor.basis_snapshot)
            case("snapshot-" + mode + "-sticky-denial", lambda: None)
        finally:
            anchor.close()


class Budget:
    """Original suite deadline; no native CPU or process authority."""
    def __init__(self):
        self.deadline = START + 60
        self.output_bytes, self.log_bytes, self.worker_cpu = 64 * MIB, 1024, 0
    def check(self):
        check()
    def allowance(self, deadline):
        need(deadline == self.deadline, "BUDGET_RENEWED")
        return {"synthetic": True}


def runtime_controls(output):
    fixture = Fixture(output / "runtime-anchor")
    anchor = fixture.anchor()
    runtime = object.__new__(R.CutRuntime)
    runtime.root = output / "unused-support"
    installation = NS(implementation_id=fixture.native.implementation_id,
        runtime_roots=dict(python_runtime=output / "unused-python", lean_runtime=output / "unused-lean"),
        path=lambda role: output / "never-executed.exe", _job_module=NS(Job=object))
    runtime.base = NS(root=output / "unused-base", installation=installation, A=A)
    runtime.manifest_sha = "a" * 64
    own, old = name("synthetic_new"), name("synthetic_old")
    inventory = [own, 2, [], ["synthetic-type"], ["synthetic-proof"]]
    packet = dict(schema="DMKN_GROUNDED_CUT_BASIS_REQUEST_V1", request_id="b" * 64,
        concrete_units=[["synthetic-concrete"]], signature_rows=[[old, [], "c" * 64]],
        new_unit=["synthetic-unit", [], [inventory]])
    workers, authentications = [], []
    mode = "good"
    actual_snapshot = anchor.basis_snapshot
    def snapshot():
        authentications.append(None)
        return actual_snapshot()
    def supervise(argv, call, spool, limits, job):
        check()
        workers.append(None)
        actual_raw = C.read_bounded(call / "request.json", MIB)
        actual = E.strict_json(actual_raw)
        need(actual["basis_snapshot"] == dict(module_name=fixture.doc["basis"]["module_name"],
            path=str(fixture.artifact), artifact_bytes=len(fixture.payload)), "RUNTIME_INTERNAL_SNAPSHOT")
        report = dict(schema="DMKN_GROUNDED_CUT_BASIS_CONDITIONAL_OUTPUT_V1",
            assurance="CONDITIONAL_KERNEL_JUDGMENT_NOT_LOCAL_WARRANT", request_id=packet["request_id"],
            theorem_name=own, theorem_inventory=inventory, signature_labels=[[old, "c" * 64]],
            counts=dict(concrete_units=1, concrete_names=1, signatures=1, scratch_names=1,
                input_bytes=len(actual_raw), basis_artifact_bytes=len(fixture.payload),
                encoded_nodes=1, scan_nodes=1, kernel_calls=5))
        if mode == "old-report":
            report["schema"] = "DMKN_GROUNDED_CUT_CONDITIONAL_OUTPUT_V1"
        elif mode == "request-id":
            report["request_id"] = "f" * 64
        elif mode == "inventory":
            report["theorem_inventory"] = ["wrong"]
        elif mode == "signature":
            report["signature_labels"] = []
        elif mode == "basis-bytes":
            report["counts"]["basis_artifact_bytes"] += 1
        elif mode == "kernel-calls":
            report["counts"]["kernel_calls"] += 456
        elif mode == "boolean-count":
            report["counts"]["encoded_nodes"] = True
        elif mode == "request-mutated":
            with (call / "request.json").open("ab") as stream:
                stream.write(b" ")
        fresh(call / "report.json", E.canonical_json(report))
        spool.mkdir()
        fresh(spool / "stderr.txt", b"")
        return dict(status="COMMAND_EXITED_ZERO_AND_CLOSED", child_exit_code=0,
            direct_child_reaped=True, job_closed=True, cleanup_errors=[], termination_requested=False,
            final_job=dict(active_processes=0, terminated_processes=0, cpu_seconds=0))
    installation._supervisor = NS(limits_checked=lambda value: value, supervise=supervise,
        save_new=lambda path, value: fresh(path, E.canonical_json(value)))
    try:
        with patch.object(A, "OperationBudget", Budget), \
             patch.object(R.CutRuntime, "verify", lambda self, callback: callback()), \
             patch.object(anchor, "basis_snapshot", snapshot):
            for mode, code in (("good", None), ("caller-snapshot", "REQUEST_FIELDS"),
                ("old-request", "REQUEST_FIELDS"), ("implementation", "BASIS_IMPLEMENTATION"),
                ("old-report", "REPORT_BINDING"), ("request-id", "REPORT_BINDING"),
                ("inventory", "ACTUAL_INVENTORY_BINDING"), ("signature", "ACTUAL_INVENTORY_BINDING"),
                ("basis-bytes", "ACTUAL_COST_BINDING"), ("kernel-calls", "ACTUAL_COST_BINDING"),
                ("boolean-count", "ADMISSION_WRITER_TOKEN"), ("request-mutated", "REQUEST_CHANGED")):
                requested = deepcopy(packet)
                if mode == "caller-snapshot":
                    requested["basis_snapshot"] = {"path": "CALLER-MUST-NOT-CONTROL"}
                if mode == "old-request":
                    requested["schema"] = "DMKN_GROUNDED_CUT_REQUEST_V1"
                installation.implementation_id = "f" * 64 if mode == "implementation" else fixture.native.implementation_id
                worker_before, auth_before = len(workers), len(authentications)
                call = output / ("runtime-" + mode)
                action = lambda: runtime.check_packet(E.canonical_json(requested), call, Budget(), anchor=anchor)
                if code is None:
                    report_raw, observation, actual_raw = action()
                    expected_snapshot = dict(module_name=fixture.doc["basis"]["module_name"],
                        path=str(fixture.artifact), artifact_bytes=len(fixture.payload))
                    need(E.strict_json(actual_raw) == {**packet, "basis_snapshot": expected_snapshot} and
                         C.read_bounded(call / "request.json", MIB) == actual_raw and
                         C.read_bounded(call / "report.json", MIB) == report_raw and
                         observation["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED", "RUNTIME_TRIPLE_BINDING")
                else:
                    refusal(code, action)
                before_launch = mode in ("caller-snapshot", "old-request", "implementation")
                need(len(workers) - worker_before == (0 if before_launch else 1) and
                     len(authentications) - auth_before == (0 if before_launch else 1),
                     "RUNTIME_SINGLE_AUTHENTICATION_OR_EARLY_REFUSAL")
                if before_launch:
                    need(not os.path.lexists(call), "EARLY_REFUSAL_CREATED_CALL")
                case("runtime-" + mode, lambda: None)
            case("runtime-anchor-type-required", lambda: refusal("BUDGET_AND_SOURCE_ANCHOR_TYPES",
                 lambda: runtime.check_packet(E.canonical_json(packet), output / "never-call", Budget(), anchor=NS())))
    finally:
        anchor.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source, output = Path(args.source_root), Path(args.output)
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTROL_PROCESS")
    need(source.is_absolute() and source.resolve().is_relative_to(ROOT) and
         output.is_absolute() and output.resolve().is_relative_to(ROOT / "experiments") and
         not output.is_relative_to(source) and not source.is_relative_to(output) and
         output.parent.is_dir() and not os.path.lexists(output), "CONTROL_PATHS")
    names = ("ordinary_evidence", "ordinary_semantics", "portable_evidence", "local_catalog",
             "portable_catalog", "ordinary_admission", "source_anchor", "cut_runtime")
    loaded, pins = {}, {}
    for i, identifier in enumerate(names):
        check()
        relative = ("ordinary_lean/" if i < 6 else "grounded_cut_basis/") + identifier + ".py"
        loaded[identifier], pins[relative] = module(identifier, source / relative)
    globals().update(E=loaded[names[0]], S=loaded[names[1]], PE=loaded[names[2]], C=loaded[names[3]],
                     P=loaded[names[4]], A=loaded[names[5]], H=loaded[names[6]], R=loaded[names[7]])
    C.ordinary(source, directory=True)
    C.ordinary(output, directory=True, fresh=True)
    output.mkdir()
    fixture = Fixture(output / "capture")
    try:
        binding_controls(fixture)
        capture_controls(fixture)
    finally:
        fixture.close_native()
    snapshot_controls(output)
    runtime_controls(output)
    check()
    need(len(CASES) == 42 and len(set(CASES)) == 42, "CONTROL_EXPECTED_CASE_CENSUS")
    report = dict(schema="DMKN_FIXED_BASIS_NATIVE_FREE_CONTROLS_V1", cases=CASES, count=len(CASES),
        source_pins=pins, native_runs=0, mathematical_acceptance=False, existing_protected_stores_opened=0,
        authority_doubles=["synthetic activation", "capture negative context/row seams",
                           "runtime installation and supervisor", "runtime support verification", "runtime budget"],
        wall_seconds=time.monotonic() - START, cpu_seconds=time.process_time() - CPU)
    fresh(output / "result.json", json.dumps(report, sort_keys=True).encode())
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()

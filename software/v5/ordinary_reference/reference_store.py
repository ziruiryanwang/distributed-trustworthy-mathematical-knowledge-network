"""Protected original references and all-new deltas under the existing owner.

Only the selected live controller may commit. No peer registration, saved-report
adoption, owner construction, proof checking, subprocess or network API exists.
The catalog lock, selected support, immutable files and no hostile administrator
or rollback are premises, exactly as for the predecessor local anchor sidecar.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import secrets
import time

import ordinary_admission as A
import reference_request as Q
import reference_report as R
import snapshot_reopen as V
import protected_metadata as P

MIB = 1024**2
STORE_SCHEMA = "DMKN_LOCAL_ORDINARY_REALIZATION_STORE_V1"
SUPPORT_SCHEMA = "DMKN_LOCAL_ORDINARY_REALIZATION_SUPPORT_V1"
RECORD_SCHEMA = "DMKN_LOCAL_ORDINARY_REALIZATION_V1"
RESERVATION_SCHEMA = "DMKN_LOCAL_ORDINARY_REALIZATION_RESERVATION_V1"
CLOSED_SCHEMA = "DMKN_LOCAL_ORDINARY_REALIZATION_CLOSED_V1"
INPUT_SCHEMA = "DMKN_LOCAL_ORDINARY_REFERENCE_MATCH_INPUTS_V1"
PLAN_SCHEMA = "DMKN_ORDINARY_REFERENCE_MODULE_PLAN_V1"
GENERATED_PLAN_SCHEMA = "DMKN_ORDINARY_REFERENCE_GENERATED_PLAN_V1"
RECORD_DOMAIN = b"DMKN-LOCAL-ORDINARY-REALIZATION-V1\0"
SUPPORT_DOMAIN = b"DMKN-LOCAL-ORDINARY-REALIZATION-SUPPORT-V1\0"
KEY_DOMAIN = b"DMKN-REFERENCE-DELTA-MATERIALIZATION-V1\0"
KINDS = ("original-reference", "generated-delta")
SUFFIXES = (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir")
LIMITS = {"max_store_bytes": 4096*MIB, "max_operations": 128, "max_record_bytes": 2*MIB,
    "max_reference_operation_bytes": 768*MIB, "max_reference_metadata_bytes": 256*MIB,
    "max_snapshot_artifact_bytes": 512*MIB, "max_snapshot_modules": 4096,
    "max_delta_operation_bytes": 128*MIB, "max_delta_metadata_bytes": 32*MIB,
    "max_delta_module_bytes": 64*MIB, "max_chain_artifact_bytes": 256*MIB,
    "max_chain_modules": 32, "max_chain_units": 1024, "max_chain_names": 16384,
    "max_chain_records_bytes": 4*MIB, "max_generated_plan_bytes": 4*MIB}
REFERENCE_EVENTS = {"request.json": 96*MIB, "inventory.json": MIB,
    "reference-report.json": 32*MIB, "warrants.json": 32*MIB, "SUPERVISION.json": MIB}
DELTA_EVENTS = {"request.json": 4*MIB, "inventory.json": MIB, "reference-plan.json": MIB,
    "generated-plan.json": 4*MIB, "native-report.json": 8*MIB,
    "native-report.json.pending": 8*MIB, "native-report.json.phases.jsonl": MIB,
    "SUPERVISION.json": MIB}
DELTA_REQUEST_SCHEMA = "DMKN_ORDINARY_REFERENCE_MODULE_REQUEST_V1"
DELTA_REQUEST_FIELDS = {"schema", "semantic_id", "context_root", "foundation_id", "module_name",
    "targets", "unit_ids", "units", "reference_id", "parent_delta_id", "reference_plan_sha256"}
DELTA_REPORT_FIELDS = {"schema", "assurance", "semantic_id", "context_root", "foundation_id",
    "module_name", "targets", "unit_ids", "reference_id", "parent_delta_id", "reference_plan_sha256",
    "direct_imports", "names", "inventories", "added_names", "added_inventories",
    "matched_unit_indices", "matched_names", "matched_inventories", "units_checked", "units_matched",
    "checking_passes", "basis_rows", "usable_basis_rows", "reference_public_units",
    "reference_public_names", "generated_names", "artifact_parts"}
REFERENCE_FIELDS = {"schema", "kind", "store_binding", "support_id", "operation_id",
    "source_context_root", "snapshot_id", "targets", "snapshot_manifest", "reference_report",
    "warrants", "event_files"}
DELTA_FIELDS = {"schema", "kind", "store_binding", "support_id", "operation_id",
    "source_context_root", "reference_id", "parent_delta_id", "module_name", "direct_imports",
    "targets", "materialization_key", "artifact_parts", "units", "added_names", "event_files"}


class ReferenceError(ValueError):
    """Local operational refusal, not a mathematical invalidity judgment."""


class ReferenceCommitUnknown(ReferenceError):
    def __init__(self, reference_id, *, kind="original-reference"):
        self.reference_id = reference_id
        self.realization_id, self.kind = reference_id, kind
        self.report = {"status": "COMMIT_UNKNOWN", "kind": kind,
            "reference_id" if kind == "original-reference" else "delta_id": reference_id,
            "new_catalog_acceptance": False,
            "retention": "EXACT_ID_LOOKUP_ONLY_NO_AUTOMATIC_RETRY_OR_RECONSTRUCTION"}
        super().__init__("REFERENCE_COMMIT_UNKNOWN:"+reference_id)


class ReferenceCommittedError(ReferenceError):
    def __init__(self, reference_id, *, kind="original-reference"):
        self.reference_id = reference_id
        self.realization_id, self.kind = reference_id, kind
        self.report = {"status": "COMMITTED_REFERENCE_REPORTING_FAILED", "kind": kind,
            "reference_id" if kind == "original-reference" else "delta_id": reference_id,
            "new_catalog_acceptance": False, "retention": "PRESERVE_COMMITTED_RECORD_EXACT_ID_LOOKUP"}
        super().__init__("REFERENCE_COMMITTED_REPORTING_FAILED:"+reference_id)


def need(condition, code):
    if not condition:
        raise ReferenceError(code)


def fields(value, expected, code):
    need(type(value) is dict and set(value) == set(expected), code)


def canonical(value):
    return A.E.canonical_json(value)


def parse(raw, maximum):
    return A.E.strict_json(raw, A.E.Limits(max_bytes=maximum))


def pin_shape(pin, maximum):
    fields(pin, ("bytes", "sha256"), "REFERENCE_PIN_FIELDS")
    need(type(pin["bytes"]) is int and 0 < pin["bytes"] <= maximum, "REFERENCE_PIN_BOUND")
    A.C.hexid(pin["sha256"])
    return pin


def file_pin(path, maximum, check):
    path = A.C.ordinary(Path(path)); check()
    initial = path.stat().st_size
    need(0 < initial <= maximum, "REFERENCE_FILE_BOUND")
    total, digest = 0, hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            check(); total += len(block)
            need(total <= initial, "REFERENCE_FILE_GREW")
            digest.update(block)
    need(total == initial == path.stat().st_size, "REFERENCE_FILE_CHANGED")
    return {"bytes": total, "sha256": digest.hexdigest()}


def verify(path, expected, maximum, check):
    pin_shape(expected, maximum)
    need(file_pin(path, maximum, check) == expected, "REFERENCE_FILE_PIN")
    return Path(path)


def _targets(value, *, with_units=False):
    need(type(value) is list and 1 <= len(value) <= 1024 and len(canonical(value)) <= MIB,
         "REFERENCE_TARGET_BOUND")
    seen = set()
    for row in value:
        fields(row, ("name", "export_id", "unit_id") if with_units else ("name", "export_id"),
               "REFERENCE_TARGET_FIELDS")
        key = A.E.name_key(row["name"])
        need(key not in seen, "REFERENCE_TARGET_DUPLICATE"); seen.add(key)
        A.C.hexid(row["export_id"])
        if with_units:
            A.C.hexid(row["unit_id"])
            need(A.S.export_id(A.S.semantic_id(), row["unit_id"], row["name"]) == row["export_id"],
                 "REFERENCE_TARGET_EXPORT")


def module_name(text):
    need(type(text) is str and text.startswith("DMKNBridge_") and len(text) == 75,
         "REFERENCE_MODULE_NAME")
    A.C.hexid(text[11:])
    return [[0, {"$bytes": list(text.encode("ascii"))}]]


def module_text(name):
    A.E.name_key(name)
    need(type(name) is list and len(name) == 1 and name[0][0] == 0, "REFERENCE_MODULE_NAME")
    text = bytes(name[0][1]["$bytes"]).decode("ascii")
    need(module_name(text) == name, "REFERENCE_MODULE_NAME")
    return text


def materialization_key(support_id, reference_id, parent_delta_id, targets):
    A.C.hexid(support_id); A.C.hexid(reference_id)
    if parent_delta_id:
        A.C.hexid(parent_delta_id)
    else:
        need(parent_delta_id == "", "REFERENCE_DELTA_PARENT")
    _targets(targets, with_units=True)
    keys = [A.E.name_key(row["name"]) for row in targets]
    need(len(targets) <= 32 and len(canonical(targets)) <= 65536 and keys == sorted(keys),
         "REFERENCE_DELTA_TARGET_BOUND_ORDER")
    return A.sha(KEY_DOMAIN+canonical({"support_id": support_id, "reference_id": reference_id,
        "parent_delta_id": parent_delta_id, "targets": targets}))


@dataclass(frozen=True)
class ReferenceView:
    reference_id: str
    store_binding: str
    support_id: str
    registration_context_root: str
    snapshot: V.SnapshotView
    report_path: Path
    report_raw: bytes
    report_sha256: str
    warrant_bindings: tuple[tuple[bytes, str], ...]
    public_frontier: tuple[tuple[str, tuple[tuple[bytes, str], ...]], ...]
    basis_bindings: tuple[tuple[bytes, int, tuple[bytes, ...], str, str], ...]
    usable_basis_keys: tuple[bytes, ...]
    private_module_keys: tuple[bytes, ...]
    public_module_keys: tuple[bytes, ...]
    record_raw: bytes
    event_pins: tuple[tuple[str, int, str], ...]


@dataclass(frozen=True)
class NativeMatchInputs:
    operation_id: str
    snapshot_directory: Path
    request_path: Path
    inventory_path: Path
    replay_path: Path
    report_path: Path
    supervision_path: Path
    request_sha256: str
    snapshot_id: str


@dataclass(frozen=True)
class DeltaView:
    reference: ReferenceView
    delta_id: str
    module_name: str
    materialization_key: str
    module_directory: Path
    # Generated directories only, for the explicit-map consumer. Original
    # snapshot hash directories are NOT module-search/LEAN_PATH roots.
    import_directories: tuple[Path, ...]
    frontier: tuple[tuple[str, tuple[tuple[bytes, str], ...]], ...]
    generated_plan_raw: bytes
    records: tuple[bytes, ...]
    artifact_bytes: int
    store_binding: str
    support_id: str


@dataclass(frozen=True)
class NativeDeltaPlan:
    operation_id: str
    module_name: str
    generated_plan_path: Path
    reference_plan_path: Path
    reference_plan_raw: bytes
    reference_plan_sha256: str
    output_path: Path
    report_path: Path
    supervision_path: Path


@dataclass(frozen=True)
class NativeDeltaInputs:
    plan: NativeDeltaPlan
    request_path: Path
    inventory_path: Path
    request_sha256: str


@dataclass(frozen=True)
class _DeltaInputs:
    paths: NativeDeltaInputs
    request_raw: bytes
    inventory_raw: bytes
    inputs_raw: bytes
    units_raw: bytes


@dataclass(frozen=True)
class _Grant:
    identifier: str
    directory: Path
    kind: str
    deadline: float
    selection_raw: bytes
    check: object


@dataclass(frozen=True)
class _BoundInputs:
    request: Q.ReferenceRequest
    snapshot: V.SnapshotView
    targets_raw: bytes
    warrants_raw: bytes
    inputs_raw: bytes
    paths: NativeMatchInputs


class Store:
    """A typed protected sidecar, never a second owner or acceptance catalog."""

    def _owner_live(self):
        owner = self.owner
        need(type(owner) is A.OrdinaryAdmission and type(owner.catalog) is A.P.PortableCatalog,
             "REFERENCE_OWNER_TYPE")
        catalog = owner.catalog; catalog._active()
        need(catalog._lock is not None and not catalog._lock.closed and catalog._root == self.catalog_root
             and catalog._marker == self.adoption_raw and catalog._activation_raw == self.activation_raw,
             "REFERENCE_OWNER_BINDING")
        need(A.C.read_bounded(catalog._root/"ADOPTION.json", 65536) == self.adoption_raw,
             "REFERENCE_ADOPTION_CHANGED")

    def _live(self, check):
        need(callable(check), "REFERENCE_CHECK_CALLBACK"); check(); self._owner_live()
        need(not self._denied and not os.path.lexists(self.root/"BLOCKED"), "REFERENCE_STORE_BLOCKED")
        need(A.C.read_bounded(self.root/"STORE.json", 65536) == self.marker_raw, "REFERENCE_STORE_CHANGED")

    def _context(self, context):
        need(type(context) is dict and type(context.get("bindings")) is dict and
             all(context.get(key) == getattr(self, key) for key in
                 ("semantic_id", "foundation_id", "implementation_id")), "REFERENCE_CONTEXT_POLICY")

    def _operation_census(self, operation, kind, check):
        """Finite kind-specific tree; count every byte, including staged/orphan data."""
        reference = kind == "original-reference"
        maximum = LIMITS["max_reference_operation_bytes" if reference else "max_delta_operation_bytes"]
        metadata_max = LIMITS["max_reference_metadata_bytes" if reference else "max_delta_metadata_bytes"]
        total = metadata = entries = module_dirs = 0
        stack = [operation]
        while stack:
            directory = A.C.ordinary(stack.pop(), directory=True)
            for path in directory.iterdir():
                check(); entries += 1
                need(entries <= (24640 if reference else 64), "REFERENCE_OPERATION_ENTRY_BOUND")
                rel = path.relative_to(operation).parts
                if path.is_dir():
                    A.C.ordinary(path, directory=True)
                    allowed = rel in (("events",), ("supervision",))
                    if reference:
                        allowed = allowed or rel in (("snapshot",), ("snapshot", "modules"))
                        if len(rel) == 3 and rel[:2] == ("snapshot", "modules"):
                            A.C.hexid(rel[2]); module_dirs += 1
                            need(module_dirs <= 4096, "REFERENCE_SNAPSHOT_MODULE_BOUND")
                            allowed = True
                    else:
                        allowed = allowed or rel == ("modules",)
                    need(allowed, "REFERENCE_OPERATION_DIRECTORY"); stack.append(path)
                    continue
                A.C.ordinary(path); size = path.stat().st_size
                artifact = False
                if len(rel) == 1:
                    bounds = {"RESERVATION.json": 2*MIB, "MATCH-INPUTS.json": 2*MIB,
                              "CLOSED.json": 4096, "record.staged.json": 2*MIB, "FAILURE.json": MIB}
                    bound = bounds.get(rel[0])
                elif rel[0] == "events" and len(rel) == 2:
                    bounds = REFERENCE_EVENTS if reference else DELTA_EVENTS
                    bound = bounds.get(rel[1])
                elif rel[0] == "supervision" and len(rel) == 2:
                    bound = MIB if rel[1] in ("stdout.txt", "stderr.txt") else None
                elif reference and rel[0] == "snapshot" and len(rel) == 2:
                    bound = {"prepared-manifest.json": 32*MIB, "replay-request.json": 16*MIB,
                             "source-report.json": 16*MIB}.get(rel[1])
                elif reference and len(rel) == 4 and rel[:2] == ("snapshot", "modules"):
                    bound = 64*MIB if rel[3] in tuple("module"+suffix for suffix in SUFFIXES) else None
                    artifact = True
                elif not reference and rel[0] == "modules" and len(rel) == 2:
                    bound = 64*MIB if any(rel[1].endswith(suffix) for suffix in SUFFIXES) else None
                    artifact = True
                else:
                    bound = None
                need(bound is not None and 0 <= size <= bound, "REFERENCE_OPERATION_FILE")
                total += size
                if not artifact:
                    metadata += size
                need(total <= maximum and metadata <= metadata_max, "REFERENCE_OPERATION_BYTE_BOUND")
        artifact_max = 512*MIB if reference else 64*MIB
        need(total-metadata <= artifact_max, "REFERENCE_OPERATION_ARTIFACT_BOUND")
        return total

    def _census(self, check, *, allow_pending=None):
        self._live(check)
        top = set()
        for path in self.root.iterdir():
            check(); top.add(path.name)
            need(len(top) <= 3, "REFERENCE_STORE_CENSUS")
        need(top == {"STORE.json", "operations", "records"}, "REFERENCE_STORE_CENSUS")
        total = (self.root/"STORE.json").stat().st_size
        count = 0
        for path in A.C.ordinary(self.root/"records", directory=True).iterdir():
            check(); A.C.ordinary(path)
            need(path.suffix == ".json", "REFERENCE_RECORD_FILENAME"); A.C.hexid(path.stem)
            size = path.stat().st_size
            need(0 < size <= LIMITS["max_record_bytes"], "REFERENCE_RECORD_BOUND")
            count += 1; total += size
            need(count <= 128, "REFERENCE_RECORD_COUNT")
        operations = 0
        for operation in A.C.ordinary(self.root/"operations", directory=True).iterdir():
            check(); A.C.ordinary(operation, directory=True); A.C.hexid(operation.name)
            operations += 1; need(operations <= 128, "REFERENCE_OPERATION_COUNT")
            reservation = parse(A.C.read_bounded(operation/"RESERVATION.json", 2*MIB), 2*MIB)
            fields(reservation, ("schema", "operation_id", "kind", "store_binding", "support_id", "selection"),
                   "REFERENCE_RESERVATION_FIELDS")
            need(reservation["schema"] == RESERVATION_SCHEMA and reservation["operation_id"] == operation.name
                 and reservation["kind"] in KINDS and reservation["store_binding"] == self.store_binding,
                 "REFERENCE_RESERVATION_BINDING")
            A.C.hexid(reservation["support_id"])
            total += self._operation_census(operation, reservation["kind"], check)
            need(total <= LIMITS["max_store_bytes"], "REFERENCE_STORE_BYTE_BOUND")
            if allow_pending is not None and operation == allow_pending.directory:
                continue
            closed = parse(A.C.read_bounded(operation/"CLOSED.json", 4096), 4096)
            fields(closed, ("schema", "operation_id", "store_binding", "reason"), "REFERENCE_CLOSED_FIELDS")
            need(closed["schema"] == CLOSED_SCHEMA and closed["operation_id"] == operation.name and
                 closed["store_binding"] == self.store_binding and type(closed["reason"]) is str
                 and 0 < len(closed["reason"]) <= 256, "REFERENCE_CLEANUP_UNKNOWN")
        need(total <= LIMITS["max_store_bytes"], "REFERENCE_STORE_BYTE_BOUND")
        return total, operations

    def reserve_reference(self, selection, check, *, deadline):
        self._live(check)
        need(self._grant is None and not self._commit_attempted, "REFERENCE_OPERATION_ACTIVE")
        need(type(deadline) in (int, float) and math.isfinite(deadline) and time.monotonic() < deadline,
             "REFERENCE_DEADLINE")
        raw = canonical(selection); need(len(raw) <= 2*MIB, "REFERENCE_SELECTION_BOUND")
        value = parse(raw, 2*MIB)
        fields(value, ("source_context_root", "targets", "project_selection", "bundle_manifest", "artifact_report"),
               "REFERENCE_SELECTION_FIELDS")
        A.C.hexid(value["source_context_root"]); _targets(value["targets"])
        for role, maximum in (("project_selection", MIB), ("bundle_manifest", 2*MIB), ("artifact_report", 16*MIB)):
            pin_shape(value[role], maximum)
        context = self.owner.catalog.context(value["source_context_root"]); self._context(context)
        total, count = self._census(check)
        need(count < 128 and total+768*MIB+2*MIB <= LIMITS["max_store_bytes"], "REFERENCE_RESERVATION_CAPACITY")
        identifier = secrets.token_hex(32)
        directory = A.C.ordinary(self.root/"operations"/identifier, directory=True, fresh=True)
        directory.mkdir()
        reservation = {"schema": RESERVATION_SCHEMA, "operation_id": identifier,
            "kind": "original-reference", "store_binding": self.store_binding,
            "support_id": self.support_id, "selection": value}
        A.P.PortableCatalog._write_fresh(directory/"RESERVATION.json", canonical(reservation))
        grant = _Grant(identifier, directory, "original-reference", float(deadline), raw, check)
        self._grant = grant
        return grant

    def _grant_live(self, grant, check):
        need(type(grant) is _Grant and self._grant is grant and grant.check is check,
             "REFERENCE_LIVE_GRANT_REQUIRED")
        self._live(check); need(time.monotonic() < grant.deadline, "REFERENCE_DEADLINE")
        expected = {"schema": RESERVATION_SCHEMA, "operation_id": grant.identifier,
            "kind": grant.kind, "store_binding": self.store_binding, "support_id": self.support_id,
            "selection": parse(grant.selection_raw, 2*MIB)}
        need(A.C.read_bounded(grant.directory/"RESERVATION.json", 2*MIB) == canonical(expected),
             "REFERENCE_LIVE_RESERVATION_CHANGED")

    def bind_reference_inputs(self, grant, request, snapshot, check):
        self._grant_live(grant, check)
        need(grant.kind == "original-reference" and self._bound is None and type(request) is Q.ReferenceRequest
             and type(snapshot) is V.SnapshotView, "REFERENCE_BIND_CONFIGURATION")
        need(snapshot.directory == grant.directory/"snapshot", "REFERENCE_FINAL_SNAPSHOT_LOCATION")
        selected = parse(grant.selection_raw, 2*MIB)
        manifest = parse(snapshot.manifest_raw, 32*MIB)
        need(manifest["project_selection_sha256"] == selected["project_selection"]["sha256"] and
             manifest["source_report_sha256"] == selected["artifact_report"]["sha256"] and
             len(snapshot.source_report_raw) == selected["artifact_report"]["bytes"], "REFERENCE_SNAPSHOT_SELECTION")
        need(type(request.raw) is bytes and 0 < len(request.raw) <= Q.MAX_REQUEST and
             A.sha(request.raw) == request.sha256, "REFERENCE_REQUEST_BYTES")
        document = parse(request.raw, Q.MAX_REQUEST)
        fields(document, ("schema", *R.IDENTITIES, "units", "targets"), "REFERENCE_REQUEST_FIELDS")
        need(document["schema"] == Q.SCHEMA and document["semantic_id"] == self.semantic_id
             and document["foundation_id"] == self.foundation_id and
             document["context_root"] == selected["source_context_root"] and
             document["snapshot_id"] == snapshot.manifest_sha256 and document["support_id"] == self.support_id
             and document["targets"] == selected["targets"], "REFERENCE_REQUEST_BINDING")
        context = self.owner.catalog.context(selected["source_context_root"]); self._context(context)
        warrants = {}
        for row in P.basis_inventory(request.inventory_raw):
            check(); key = A.E.name_key(row[0])
            warrants[key] = A.S.basis_symbol_id(self.semantic_id, self.foundation_id, row[0])
        identities, bindings = [], []
        for entry in A.E._array(document["units"], maximum=8192):
            check(); fields(entry, ("unit_id", "unit", "outputs"), "REFERENCE_PRIVATE_UNIT_FIELDS")
            identity = A.C.hexid(entry["unit_id"]); identities.append(identity)
            unit = A.E._array(entry["unit"], 3)
            rows = A.E._array(unit[2], maximum=262144)
            for row, output in zip(rows, A.E._array(entry["outputs"], len(rows))):
                check(); A.E._array(row, 5)
                fields(output, ("name", "export_id"), "REFERENCE_PRIVATE_OUTPUT_FIELDS")
                key = A.E.name_key(row[0]); symbol = A.S.export_id(self.semantic_id, identity, row[0])
                need(output == {"name": row[0], "export_id": symbol} and key not in warrants,
                     "REFERENCE_PRIVATE_BINDING")
                warrants[key] = symbol; bindings.append((key, symbol, identity))
                need(len(bindings) <= 262144, "REFERENCE_PRIVATE_NAME_BOUND")
        need(bool(identities) and len(set(identities)) == len(identities) and tuple(identities) == request.unit_ids
             and tuple(sorted(bindings)) == request.output_bindings, "REFERENCE_PRIVATE_CENSUS")
        for key, symbol in warrants.items():
            check(); need(context["bindings"].get(key) == symbol, "REFERENCE_CURRENT_PRIVATE_WARRANT")
        lookup = {key: (symbol, identity) for key, symbol, identity in bindings}
        targets = []
        for target in selected["targets"]:
            symbol, identity = lookup.get(A.E.name_key(target["name"]), (None, None))
            need(symbol == target["export_id"], "REFERENCE_TARGET_PRIVATE")
            targets.append({**target, "unit_id": identity})
        warrants_raw = canonical({"schema": P.WARRANT_SCHEMA, "semantic_id": self.semantic_id,
            "foundation_id": self.foundation_id, "bindings": [
                {"name": A.E.strict_json(key), "symbol_id": symbol} for key, symbol in sorted(warrants.items())]})
        need(len(warrants_raw) <= P.MAX_WARRANTS, "REFERENCE_WARRANT_BOUND")
        events = A.C.ordinary(grant.directory/"events", directory=True, fresh=True); events.mkdir()
        paths = NativeMatchInputs(grant.identifier, snapshot.directory, events/"request.json", events/"inventory.json",
            snapshot.directory/"replay-request.json", events/"reference-report.json", events/"SUPERVISION.json",
            request.sha256, snapshot.manifest_sha256)
        inputs = {"schema": INPUT_SCHEMA, "operation_id": grant.identifier, "store_binding": self.store_binding,
            "support_id": self.support_id, "selection_sha256": A.sha(grant.selection_raw),
            "snapshot_id": snapshot.manifest_sha256, "request": {"bytes": len(request.raw), "sha256": request.sha256},
            "inventory": {"bytes": len(request.inventory_raw), "sha256": A.sha(request.inventory_raw)},
            "replay_request": {"bytes": len(snapshot.replay_raw), "sha256": A.sha(snapshot.replay_raw)},
            "warrants": {"bytes": len(warrants_raw), "sha256": A.sha(warrants_raw)}}
        inputs_raw = canonical(inputs)
        # All maximum-size future report/control/staging writes fit the original
        # reservation. Large inputs are written once at final locations.
        present = self._operation_census(grant.directory, grant.kind, check)
        future = len(request.raw)+len(request.inventory_raw)+len(warrants_raw)+len(inputs_raw)+32*MIB+8*MIB
        need(present+future <= 768*MIB, "REFERENCE_INPUT_CAPACITY")
        for path, raw in ((paths.request_path, request.raw), (paths.inventory_path, request.inventory_raw),
                          (events/"warrants.json", warrants_raw), (grant.directory/"MATCH-INPUTS.json", inputs_raw)):
            self._grant_live(grant, check)
            A.P.PortableCatalog._write_fresh(path, raw)
            need(A.C.read_bounded(path, max(1, len(raw))) == raw, "REFERENCE_INPUT_READBACK")
        self._bound = _BoundInputs(request, snapshot, canonical(targets), warrants_raw, inputs_raw, paths)
        self._operation_census(grant.directory, grant.kind, check)
        return paths

    def _close_operation(self, grant, reason):
        self._owner_live()
        need(type(grant) is _Grant and self._grant is grant and type(reason) is str and 0 < len(reason) <= 256,
             "REFERENCE_CLOSE_GRANT")
        value = {"schema": CLOSED_SCHEMA, "operation_id": grant.identifier,
                 "store_binding": self.store_binding, "reason": reason}
        path = grant.directory/"CLOSED.json"
        if os.path.lexists(path):
            previous = parse(A.C.read_bounded(path, 4096), 4096)
            fields(previous, value, "REFERENCE_CLOSED_FIELDS")
            need(all(previous[key] == value[key] for key in ("schema", "operation_id", "store_binding"))
                 and type(previous["reason"]) is str and 0 < len(previous["reason"]) <= 256,
                 "REFERENCE_CLOSED_CHANGED")
        else:
            A.P.PortableCatalog._write_fresh(path, canonical(value))

    def abandon(self, grant, reason):
        """Controller only: no child started, or actual cleanup is complete."""
        if self._grant is not grant or self._commit_attempted:
            return
        self._close_operation(grant, reason); self._grant = self._bound = None
        self._delta_reference = self._delta_parent = self._delta_plan = self._delta_bound = self._delta_generated_raw = None

    def mark_blocked(self, grant, reason, check=None):
        self._owner_live()
        need(self._grant is grant and type(reason) is str and 0 < len(reason) <= 256, "REFERENCE_BLOCK_GRANT")
        self._denied = True
        if not os.path.lexists(self.root/"BLOCKED"):
            A.P.PortableCatalog._write_fresh(self.root/"BLOCKED", canonical({
                "schema": "DMKN_LOCAL_ORDINARY_REALIZATION_BLOCKED_V1", "operation_id": grant.identifier,
                "store_binding": self.store_binding, "reason": reason}))

    def _record(self, raw, identity, *, kind):
        need(kind in KINDS, "REFERENCE_RECORD_KIND")
        need(A.sha(RECORD_DOMAIN+raw) == identity, "REFERENCE_RECORD_ADDRESS")
        record = parse(raw, LIMITS["max_record_bytes"])
        fields(record, REFERENCE_FIELDS if kind == "original-reference" else DELTA_FIELDS, "REFERENCE_RECORD_FIELDS")
        need(record["schema"] == RECORD_SCHEMA and record["kind"] == kind and
             record["store_binding"] == self.store_binding and record["support_id"] == self.support_id,
             "REFERENCE_RECORD_BINDING")
        operation = A.C.hexid(record["operation_id"]); A.C.hexid(record["source_context_root"])
        _targets(record["targets"], with_units=True)
        if kind == "original-reference":
            A.C.hexid(record["snapshot_id"])
            for field, relative, maximum in (("snapshot_manifest", "snapshot/prepared-manifest.json", 32*MIB),
                    ("reference_report", "events/reference-report.json", 32*MIB),
                    ("warrants", "events/warrants.json", 32*MIB)):
                self._record_pin(record[field], operation, relative, maximum)
            need(record["snapshot_manifest"]["sha256"] == record["snapshot_id"], "REFERENCE_SNAPSHOT_ID")
            fields(record["event_files"], REFERENCE_EVENTS, "REFERENCE_EVENT_CENSUS")
            for name, maximum in REFERENCE_EVENTS.items():
                self._record_pin(record["event_files"][name], operation, "events/"+name, maximum)
            need(record["reference_report"] == record["event_files"]["reference-report.json"] and
                 record["warrants"] == record["event_files"]["warrants.json"], "REFERENCE_EVENT_BINDING")
        else:
            A.C.hexid(record["reference_id"])
            if record["parent_delta_id"]:
                A.C.hexid(record["parent_delta_id"])
            else:
                need(record["parent_delta_id"] == "", "REFERENCE_DELTA_PARENT")
            _, _, added = self._delta_units(record["units"])
            need(record["added_names"] == added and bool(added), "REFERENCE_DELTA_ALL_NEW")
            key = materialization_key(self.support_id, record["reference_id"], record["parent_delta_id"], record["targets"])
            text = module_text(record["module_name"])
            need(record["materialization_key"] == key and text == "DMKNBridge_"+key,
                 "REFERENCE_DELTA_KEY")
            direct = A.E._array(record["direct_imports"], maximum=16)
            need(bool(direct) and len({A.E.name_key(name) for name in direct}) == len(direct),
                 "REFERENCE_DELTA_IMPORTS")
            need(type(record["artifact_parts"]) is list and len(record["artifact_parts"]) == 5,
                 "REFERENCE_DELTA_PARTS")
            total = 0
            for part, suffix in zip(record["artifact_parts"], SUFFIXES):
                self._record_pin(part, operation, "modules/"+text+suffix, 64*MIB)
                total += part["bytes"]
            need(total <= 64*MIB, "REFERENCE_DELTA_MODULE_BOUND")
            fields(record["event_files"], DELTA_EVENTS, "REFERENCE_DELTA_EVENT_CENSUS")
            for name, maximum in DELTA_EVENTS.items():
                self._record_pin(record["event_files"][name], operation, "events/"+name, maximum)
        return record

    def _delta_units(self, units):
        rows = A.E._array(units, maximum=32)
        need(bool(rows), "REFERENCE_DELTA_UNITS_EMPTY")
        identities, names, added = set(), {}, []
        basis = {A.E.name_key(row[0]) for row in P.basis_inventory(self.owner.installation.read("inventory", MIB))}
        for unit in rows:
            fields(unit, ("unit_id", "outputs", "realization"), "REFERENCE_DELTA_UNIT_FIELDS")
            identity = A.C.hexid(unit["unit_id"])
            need(identity not in identities and unit["realization"] == "added", "REFERENCE_DELTA_ALL_NEW")
            identities.add(identity)
            outputs = A.E._array(unit["outputs"], maximum=4096)
            need(bool(outputs), "REFERENCE_DELTA_OUTPUT_EMPTY")
            for row in outputs:
                fields(row, ("name", "export_id", "kind", "level_params", "inventory_sha256"),
                       "REFERENCE_DELTA_OUTPUT_FIELDS")
                key = A.E.name_key(row["name"])
                symbol = A.C.hexid(row["export_id"]); A.C.hexid(row["inventory_sha256"])
                need(key not in basis and key not in names and len(names) < 4096 and
                     symbol == A.S.export_id(self.semantic_id, identity, row["name"]) and
                     type(row["kind"]) is int and 1 <= row["kind"] <= 6, "REFERENCE_DELTA_OUTPUT_IDENTITY")
                A.E._names(row["level_params"], A.E.DEFAULT_LIMITS.max_params, A.E.DEFAULT_LIMITS, params=True)
                names[key] = (symbol, identity); added.append(row["name"])
        return identities, names, added

    def _record_pin(self, pin, operation, relative, maximum):
        fields(pin, ("path", "bytes", "sha256"), "REFERENCE_RECORD_PIN")
        need(pin["path"] == "operations/"+operation+"/"+relative, "REFERENCE_RECORD_PATH")
        pin_shape({key: pin[key] for key in ("bytes", "sha256")}, maximum)

    def _pinned_raw(self, pin, maximum, check):
        path = self.root.joinpath(*pin["path"].split("/"))
        expected = {key: pin[key] for key in ("bytes", "sha256")}
        check(); raw = A.C.read_bounded(A.C.ordinary(path), maximum)
        need({"bytes": len(raw), "sha256": A.sha(raw)} == expected, "REFERENCE_RETAINED_METADATA_PIN")
        return path, raw

    def load_reference(self, reference_id, current_context, check):
        self._live(check); self._context(current_context); A.C.hexid(reference_id)
        raw = A.C.read_bounded(self.root/"records"/(reference_id+".json"), LIMITS["max_record_bytes"])
        record = self._record(raw, reference_id, kind="original-reference")
        operation = self.root/"operations"/record["operation_id"]
        # Only record publication establishes registration. Closed history is
        # consistency evidence, never a saved-PASS adoption route.
        closed = parse(A.C.read_bounded(operation/"CLOSED.json", 4096), 4096)
        fields(closed, ("schema", "operation_id", "store_binding", "reason"), "REFERENCE_CLOSED_FIELDS")
        need(closed.get("schema") == CLOSED_SCHEMA and closed.get("operation_id") == operation.name and
             closed.get("store_binding") == self.store_binding and type(closed["reason"]) is str
             and 0 < len(closed["reason"]) <= 256, "REFERENCE_REGISTERED_CLOSURE")
        _, warrant_raw = self._pinned_raw(record["warrants"], 32*MIB, check)
        warrants = P.read_warrants(warrant_raw, record["warrants"]["sha256"], semantic_id=self.semantic_id,
            foundation_id=self.foundation_id, current_context=current_context, check=check)
        self._pinned_raw(record["snapshot_manifest"], 32*MIB, check)
        snapshot = V.read_snapshot(operation/"snapshot", record["snapshot_id"],
            self.owner.installation.manifest_sha256, check_budget=check)
        report_path, report_raw = self._pinned_raw(record["reference_report"], 32*MIB, check)
        metadata = P.read_metadata(report_raw, record["reference_report"]["sha256"],
            identities={"semantic_id": self.semantic_id, "foundation_id": self.foundation_id,
                "context_root": record["source_context_root"], "snapshot_id": record["snapshot_id"],
                "support_id": self.support_id}, targets=record["targets"],
            inventory_raw=self.owner.installation.read("inventory", MIB), warrant_bindings=warrants,
            snapshot=snapshot, check=check)
        self._live(check)
        return ReferenceView(reference_id, self.store_binding, self.support_id, record["source_context_root"],
            snapshot, report_path, report_raw, record["reference_report"]["sha256"], warrants,
            metadata.public_frontier, metadata.basis_bindings, metadata.usable_basis_keys,
            metadata.private_module_keys, metadata.public_module_keys, raw,
            tuple((pin["path"], pin["bytes"], pin["sha256"]) for pin in record["event_files"].values()))

    def _commit_reference(self, grant, validated_live_match, check):
        """PRIVATE: selected controller passes its actual event, never saved adoption."""
        self._grant_live(grant, check)
        need(grant.kind == "original-reference" and type(self._bound) is _BoundInputs,
             "REFERENCE_BOUND_INPUTS_REQUIRED")
        fields(validated_live_match, ("bound_report", "snapshot", "supervision", "report_raw"),
               "REFERENCE_LIVE_EVENT_FIELDS")
        value, bound = validated_live_match, self._bound
        report = value["bound_report"]
        need(type(report) is R.BoundReferenceReport and type(value["snapshot"]) is V.SnapshotView
             and value["snapshot"] == bound.snapshot and type(value["report_raw"]) is bytes
             and report.raw == value["report_raw"] and A.sha(report.raw) == report.sha256,
             "REFERENCE_LIVE_EVENT_BINDING")
        need(type(value["supervision"]) is dict and A._clean_worker(value["supervision"]),
             "REFERENCE_LIVE_EVENT_NOT_CLEAN")
        selected = parse(grant.selection_raw, 2*MIB)
        context = self.owner.catalog.context(selected["source_context_root"]); self._context(context)
        # Rebind once here as a defensive typed-boundary check. This is a live
        # registration check, never the body-free later reopening path.
        need(R.bind_report(report.raw, report.sha256, request=bound.request,
             replay_request_raw=bound.snapshot.replay_raw, check_budget=check) == report,
             "REFERENCE_LIVE_REPORT_REBIND")
        need(A.C.read_bounded(bound.paths.report_path, 32*MIB) == report.raw and
             json.loads(A.C.read_bounded(bound.paths.supervision_path, MIB)) == value["supervision"],
             "REFERENCE_LIVE_EVENT_FILES")
        for path, raw in ((bound.paths.request_path, bound.request.raw),
                          (bound.paths.inventory_path, bound.request.inventory_raw),
                          (grant.directory/"events/warrants.json", bound.warrants_raw),
                          (grant.directory/"MATCH-INPUTS.json", bound.inputs_raw)):
            check(); need(A.C.read_bounded(path, len(raw)) == raw, "REFERENCE_LIVE_INPUT_CHANGED")
        warrants = P.read_warrants(bound.warrants_raw, A.sha(bound.warrants_raw),
            semantic_id=self.semantic_id, foundation_id=self.foundation_id, current_context=context, check=check)
        targets = parse(bound.targets_raw, MIB)
        P.read_metadata(report.raw, report.sha256, identities={"semantic_id": self.semantic_id,
            "foundation_id": self.foundation_id, "context_root": selected["source_context_root"],
            "snapshot_id": bound.snapshot.manifest_sha256, "support_id": self.support_id},
            targets=targets, inventory_raw=bound.request.inventory_raw, warrant_bindings=warrants,
            snapshot=bound.snapshot, check=check)

        def retained_pin(relative, maximum):
            path = grant.directory/relative
            return {"path": "operations/"+grant.identifier+"/"+relative, **file_pin(path, maximum, check)}

        events = {name: retained_pin("events/"+name, maximum) for name, maximum in REFERENCE_EVENTS.items()}
        record = {"schema": RECORD_SCHEMA, "kind": "original-reference", "store_binding": self.store_binding,
            "support_id": self.support_id, "operation_id": grant.identifier,
            "source_context_root": selected["source_context_root"], "snapshot_id": bound.snapshot.manifest_sha256,
            "targets": targets, "snapshot_manifest": retained_pin("snapshot/prepared-manifest.json", 32*MIB),
            "reference_report": events["reference-report.json"], "warrants": events["warrants.json"],
            "event_files": events}
        raw = canonical(record); need(len(raw) <= 2*MIB, "REFERENCE_RECORD_BOUND")
        identity = A.sha(RECORD_DOMAIN+raw); self._record(raw, identity, kind="original-reference")
        self._close_operation(grant, "LIVE_CORRESPONDENCE_CLEAN_BEFORE_COMMIT")
        total, _ = self._census(check, allow_pending=grant)
        operation_bytes = self._operation_census(grant.directory, grant.kind, check)
        need(total+2*len(raw) <= LIMITS["max_store_bytes"] and operation_bytes+len(raw) <= 768*MIB,
             "REFERENCE_COMMIT_CAPACITY")
        staging = grant.directory/"record.staged.json"
        A.P.PortableCatalog._write_fresh(staging, raw)
        self._grant_live(grant, check)
        destination = A.C.ordinary(self.root/"records"/(identity+".json"), fresh=True)
        need(os.name == "nt", "REFERENCE_NONOVERWRITING_WINDOWS_COMMIT")
        self._commit_attempted = True
        try:
            os.rename(staging, destination)
            need(A.C.read_bounded(destination, 2*MIB) == raw, "REFERENCE_COMMIT_READBACK")
        except BaseException as error:
            self._denied = True
            raise ReferenceCommitUnknown(identity) from error
        self._grant = self._bound = None
        try:
            return self.load_reference(identity, context, check)
        except BaseException as error:
            raise ReferenceCommittedError(identity) from error

    def plan(self, reference, generated_plan_pin, *, parent_delta_id=""):
        """Pure spelling helper; controller must first load the current protected view."""
        need(type(reference) is ReferenceView and reference.store_binding == self.store_binding
             and reference.support_id == self.support_id, "REFERENCE_VIEW_BINDING")
        if parent_delta_id:
            A.C.hexid(parent_delta_id)
        else:
            need(parent_delta_id == "", "REFERENCE_DELTA_PARENT")
        fields(generated_plan_pin, ("path", "bytes", "sha256"), "REFERENCE_GENERATED_PLAN_PIN")
        pin_shape({key: generated_plan_pin[key] for key in ("bytes", "sha256")}, 4*MIB)
        need(type(generated_plan_pin["path"]) is str and Path(generated_plan_pin["path"]).is_absolute(),
             "REFERENCE_GENERATED_PLAN_PATH")
        raw = canonical({"schema": PLAN_SCHEMA, "reference_id": reference.reference_id,
            "snapshot_id": reference.snapshot.manifest_sha256, "support_id": self.support_id,
            "semantic_id": self.semantic_id, "foundation_id": self.foundation_id,
            "implementation_id": self.implementation_id, "registration_context_root": reference.registration_context_root,
            "parent_delta_id": parent_delta_id, "original_roots": parse(reference.snapshot.root_imports_raw, MIB),
            "reference_report": {"path": str(reference.report_path), "bytes": len(reference.report_raw),
                                  "sha256": reference.report_sha256},
            "replay_request": {"path": str(reference.snapshot.directory/"replay-request.json"),
                "bytes": len(reference.snapshot.replay_raw), "sha256": A.sha(reference.snapshot.replay_raw)},
            "generated_plan": generated_plan_pin})
        need(len(raw) <= MIB, "REFERENCE_PLAN_BOUND")
        return raw

    def load_delta(self, delta_id, current_context, check):
        self._live(check); self._context(current_context); A.C.hexid(delta_id)
        reverse, seen, current, record_bytes = [], set(), delta_id, 0
        reference_id = None
        while current:
            self._live(check)
            need(current not in seen and len(seen) < 32, "REFERENCE_DELTA_CHAIN_BOUND")
            seen.add(current)
            raw = A.C.read_bounded(self.root/"records"/(current+".json"), 2*MIB)
            record_bytes += len(raw); need(record_bytes <= 4*MIB, "REFERENCE_DELTA_CHAIN_RECORD_BOUND")
            record = self._record(raw, current, kind="generated-delta")
            if reference_id is None:
                reference_id = record["reference_id"]
            need(record["reference_id"] == reference_id, "REFERENCE_DELTA_FOREIGN_BASE")
            reverse.append((current, raw, record)); current = record["parent_delta_id"]
        reference = self.load_reference(reference_id, current_context, check)
        modules, bindings, frontier, directories = [], [], [], []
        names = {key: (symbol, "") for key, symbol in reference.warrant_bindings}
        # Include original whole-unit IDs as well as names: a delta cannot
        # present an old unit under another output inventory.
        original = A._writer_json(reference.report_raw, 32*MIB)
        units = set(original["private_unit_ids"])
        previous_id, previous_imports, artifact_bytes = "", [row["module"] for row in
            parse(reference.snapshot.root_imports_raw, MIB)], 0
        generated_units = generated_names = 0
        module_keys = set(reference.snapshot.module_keys)
        for identity, raw, record in reversed(reverse):
            check()
            need(record["parent_delta_id"] == previous_id and record["direct_imports"] == previous_imports,
                 "REFERENCE_DELTA_EXACT_CHAIN")
            operation = self.root/"operations"/record["operation_id"]
            closed = parse(A.C.read_bounded(operation/"CLOSED.json", 4096), 4096)
            fields(closed, ("schema", "operation_id", "store_binding", "reason"), "REFERENCE_CLOSED_FIELDS")
            need(closed.get("schema") == CLOSED_SCHEMA and closed.get("operation_id") == operation.name
                 and closed.get("store_binding") == self.store_binding and type(closed["reason"]) is str
                 and 0 < len(closed["reason"]) <= 256, "REFERENCE_DELTA_REGISTERED_CLOSURE")
            record_units, record_names, _ = self._delta_units(record["units"])
            module_key = A.E.name_key(record["module_name"])
            need(not units.intersection(record_units) and not names.keys() & record_names.keys()
                 and module_key not in module_keys, "REFERENCE_DELTA_CHAIN_COLLISION")
            units.update(record_units); names.update(record_names); module_keys.add(module_key)
            generated_units += len(record_units); generated_names += len(record_names)
            need(generated_units <= 1024 and generated_names <= 16384, "REFERENCE_DELTA_CHAIN_CENSUS")
            for key, (symbol, _) in record_names.items():
                check(); need(current_context["bindings"].get(key) == symbol, "REFERENCE_DELTA_CURRENT_WARRANT")
            parts = []
            for part in record["artifact_parts"]:
                check(); artifact_bytes += part["bytes"]
                need(artifact_bytes <= 256*MIB, "REFERENCE_DELTA_CHAIN_ARTIFACT_BOUND")
                path = self.root.joinpath(*part["path"].split("/"))
                expected = {key: part[key] for key in ("bytes", "sha256")}
                verify(path, expected, 64*MIB, check); parts.append({"path": str(path), **expected})
            directory = Path(parts[0]["path"]).parent
            present = set()
            for path in directory.iterdir():
                check(); A.C.ordinary(path); present.add(path.name)
                need(len(present) <= 5, "REFERENCE_DELTA_ARTIFACT_CENSUS")
            need(present == {Path(part["path"]).name for part in parts}, "REFERENCE_DELTA_ARTIFACT_CENSUS")
            directories.append(directory)
            modules.append({"delta_id": identity, "module_name": record["module_name"],
                "direct_imports": record["direct_imports"], "added_names": record["added_names"], "artifact_parts": parts})
            bindings.extend(record["units"])
            frontier.extend((unit["unit_id"], tuple((A.E.name_key(row["name"]), row["export_id"])
                for row in unit["outputs"])) for unit in record["units"])
            public_names = {key: (symbol, unit) for unit, outputs in reference.public_frontier for key, symbol in outputs}
            public_names.update({key: (symbol, unit) for unit, outputs in frontier for key, symbol in outputs})
            for target in record["targets"]:
                need(public_names.get(A.E.name_key(target["name"])) == (target["export_id"], target["unit_id"]),
                     "REFERENCE_DELTA_TARGET_REALIZATION")
            previous_id, previous_imports = identity, [record["module_name"]]
        generated_raw = canonical({"schema": GENERATED_PLAN_SCHEMA, "reference_id": reference_id,
            "support_id": self.support_id, "delta_id": delta_id, "modules": modules, "bindings": bindings})
        need(len(generated_raw) <= 4*MIB, "REFERENCE_GENERATED_PLAN_BOUND")
        self._live(check)
        last = reverse[0][2]
        return DeltaView(reference, delta_id, module_text(last["module_name"]), last["materialization_key"],
            directories[-1], tuple(directories), tuple(frontier), generated_raw,
            tuple(raw for _, raw, _ in reversed(reverse)), artifact_bytes, self.store_binding, self.support_id)

    def reserve_delta(self, reference, parent, selection, check, *, deadline):
        self._live(check)
        need(self._grant is None and not self._commit_attempted, "REFERENCE_OPERATION_ACTIVE")
        need(type(reference) is ReferenceView and (parent is None or type(parent) is DeltaView),
             "REFERENCE_DELTA_VIEW_TYPE")
        need(type(deadline) in (int, float) and math.isfinite(deadline) and time.monotonic() < deadline,
             "REFERENCE_DEADLINE")
        selected_raw = canonical(selection); selected = parse(selected_raw, MIB)
        fields(selected, ("source_context_root", "targets"), "REFERENCE_DELTA_SELECTION_FIELDS")
        A.C.hexid(selected["source_context_root"])
        key = materialization_key(self.support_id, reference.reference_id, "" if parent is None else parent.delta_id,
                                  selected["targets"])
        context = self.owner.catalog.context(selected["source_context_root"]); self._context(context)
        if parent is None:
            need(self.load_reference(reference.reference_id, context, check) == reference, "REFERENCE_DELTA_BASE_CHANGED")
        else:
            need(parent.reference == reference and self.load_delta(parent.delta_id, context, check) == parent
                 and len(parent.records) < 32, "REFERENCE_DELTA_PARENT_CHANGED")
        for row in selected["targets"]:
            need(context["bindings"].get(A.E.name_key(row["name"])) == row["export_id"],
                 "REFERENCE_DELTA_TARGET_WARRANT")
        total, count = self._census(check)
        need(count < 128 and total+128*MIB+2*MIB <= LIMITS["max_store_bytes"], "REFERENCE_DELTA_RESERVATION_CAPACITY")
        identifier = secrets.token_hex(32)
        directory = A.C.ordinary(self.root/"operations"/identifier, directory=True, fresh=True); directory.mkdir()
        # Bind base/key in the protected reservation itself, not only mutable
        # convenience attributes of the caller-supplied view.
        selected.update(reference_id=reference.reference_id, parent_delta_id="" if parent is None else parent.delta_id,
                        materialization_key=key)
        selected_raw = canonical(selected)
        reservation = {"schema": RESERVATION_SCHEMA, "operation_id": identifier, "kind": "generated-delta",
            "store_binding": self.store_binding, "support_id": self.support_id, "selection": selected}
        A.P.PortableCatalog._write_fresh(directory/"RESERVATION.json", canonical(reservation))
        grant = _Grant(identifier, directory, "generated-delta", float(deadline), selected_raw, check)
        self._grant, self._delta_reference, self._delta_parent = grant, reference, parent
        return grant

    def materialization_key(self, reference_id, parent_delta_id, targets):
        return materialization_key(self.support_id, reference_id, parent_delta_id, targets)

    def prepare_delta_plan(self, grant, check):
        self._grant_live(grant, check)
        need(grant.kind == "generated-delta" and self._delta_plan is None, "REFERENCE_DELTA_PLAN_STATE")
        reference, parent = self._delta_reference, self._delta_parent
        selected = parse(grant.selection_raw, MIB)
        generated_raw = (parent.generated_plan_raw if parent is not None else canonical({
            "schema": GENERATED_PLAN_SCHEMA, "reference_id": reference.reference_id,
            "support_id": self.support_id, "delta_id": "", "modules": [], "bindings": []}))
        events = A.C.ordinary(grant.directory/"events", directory=True, fresh=True); events.mkdir()
        modules = A.C.ordinary(grant.directory/"modules", directory=True, fresh=True); modules.mkdir()
        generated_path, plan_path = events/"generated-plan.json", events/"reference-plan.json"
        generated_pin = {"path": str(generated_path), "bytes": len(generated_raw), "sha256": A.sha(generated_raw)}
        plan_raw = self.plan(reference, generated_pin, parent_delta_id=selected["parent_delta_id"])
        for path, raw in ((generated_path, generated_raw), (plan_path, plan_raw)):
            self._grant_live(grant, check); A.P.PortableCatalog._write_fresh(path, raw)
            need(A.C.read_bounded(path, len(raw)) == raw, "REFERENCE_DELTA_PLAN_READBACK")
        text = "DMKNBridge_"+selected["materialization_key"]
        plan = NativeDeltaPlan(grant.identifier, text, generated_path, plan_path, plan_raw, A.sha(plan_raw),
            modules/(text+".olean"), events/"native-report.json", events/"SUPERVISION.json")
        self._delta_plan, self._delta_generated_raw = plan, generated_raw
        return plan

    def bind_delta_inputs(self, grant, request_raw, inventory_raw, check):
        self._grant_live(grant, check)
        need(grant.kind == "generated-delta" and type(self._delta_plan) is NativeDeltaPlan
             and self._delta_bound is None, "REFERENCE_DELTA_INPUT_STATE")
        need(type(request_raw) is bytes and 0 < len(request_raw) <= 4*MIB and
             type(inventory_raw) is bytes and 0 < len(inventory_raw) <= MIB and A.sha(inventory_raw) == A.S.INVENTORY,
             "REFERENCE_DELTA_INPUT_BYTES")
        selected, plan = parse(grant.selection_raw, MIB), self._delta_plan
        request = parse(request_raw, 4*MIB); fields(request, DELTA_REQUEST_FIELDS, "REFERENCE_DELTA_REQUEST_FIELDS")
        need(request["schema"] == DELTA_REQUEST_SCHEMA and request["semantic_id"] == self.semantic_id
             and request["foundation_id"] == self.foundation_id and
             request["context_root"] == selected["source_context_root"] and
             request["reference_id"] == selected["reference_id"] and request["parent_delta_id"] == selected["parent_delta_id"]
             and request["reference_plan_sha256"] == plan.reference_plan_sha256
             and request["module_name"] == module_name(plan.module_name)
             and request["targets"] == [row["name"] for row in selected["targets"]], "REFERENCE_DELTA_REQUEST_BINDING")
        context = self.owner.catalog.context(selected["source_context_root"]); self._context(context)
        identities = A.E._array(request["unit_ids"], maximum=32)
        raw_units = A.E._array(request["units"], len(identities))
        need(bool(identities), "REFERENCE_DELTA_EMPTY")
        units = []
        for identity, unit in zip(identities, raw_units):
            check(); A.C.hexid(identity); A.E.inspect_unit(unit)
            outputs = [{"name": row[0], "export_id": A.S.export_id(self.semantic_id, identity, row[0]),
                "kind": row[1], "level_params": row[2], "inventory_sha256": A.sha(canonical(row))} for row in unit[2]]
            units.append({"unit_id": identity, "outputs": outputs, "realization": "added"})
        unit_ids, names, _ = self._delta_units(units)
        parent = self._delta_parent; reference = self._delta_reference
        old_names = dict(reference.warrant_bindings)
        old_units = set(A._writer_json(reference.report_raw, 32*MIB)["private_unit_ids"])
        if parent is not None:
            old_units.update(unit for unit, _ in parent.frontier)
            old_names.update((key, symbol) for _, outputs in parent.frontier for key, symbol in outputs)
        need(not old_names.keys() & names.keys() and not old_units & unit_ids, "REFERENCE_DELTA_NOT_NEW")
        for key, (symbol, _) in names.items():
            check(); need(context["bindings"].get(key) == symbol, "REFERENCE_DELTA_CURRENT_WARRANT")
        all_public = {key: (symbol, unit) for unit, outputs in reference.public_frontier for key, symbol in outputs}
        if parent is not None:
            all_public.update((key, (symbol, unit)) for unit, outputs in parent.frontier for key, symbol in outputs)
        all_public.update(names)
        for row in selected["targets"]:
            need(all_public.get(A.E.name_key(row["name"])) == (row["export_id"], row["unit_id"]),
                 "REFERENCE_DELTA_TARGET_REALIZATION")
        paths = NativeDeltaInputs(plan, grant.directory/"events/request.json", grant.directory/"events/inventory.json",
                                  A.sha(request_raw))
        inputs_raw = canonical({"schema": "DMKN_LOCAL_ORDINARY_REFERENCE_DELTA_INPUTS_V1",
            "operation_id": grant.identifier, "store_binding": self.store_binding, "support_id": self.support_id,
            "selection_sha256": A.sha(grant.selection_raw), "reference_plan_sha256": plan.reference_plan_sha256,
            "generated_plan_sha256": A.sha(self._delta_generated_raw),
            "request": {"bytes": len(request_raw), "sha256": A.sha(request_raw)},
            "inventory": {"bytes": len(inventory_raw), "sha256": A.sha(inventory_raw)}})
        present = self._operation_census(grant.directory, grant.kind, check)
        # Existing files are metadata only at this point. Reserve final+pending
        # reports, trace/supervision, both logs, failure, staging record and close.
        future_metadata = len(request_raw)+len(inventory_raw)+len(inputs_raw)+23*MIB+4096
        need(present+future_metadata <= 32*MIB and present+future_metadata+64*MIB <= 128*MIB,
             "REFERENCE_DELTA_INPUT_CAPACITY")
        for path, raw in ((paths.request_path, request_raw), (paths.inventory_path, inventory_raw),
                          (grant.directory/"MATCH-INPUTS.json", inputs_raw)):
            self._grant_live(grant, check); A.P.PortableCatalog._write_fresh(path, raw)
            need(A.C.read_bounded(path, len(raw)) == raw, "REFERENCE_DELTA_INPUT_READBACK")
        self._delta_bound = _DeltaInputs(paths, request_raw, inventory_raw, inputs_raw, canonical(units))
        return paths

    def _commit_delta(self, grant, validated_live_delta, check):
        """PRIVATE live three-phase event; saved final/pending reports never adopt."""
        self._grant_live(grant, check)
        need(grant.kind == "generated-delta" and type(self._delta_bound) is _DeltaInputs, "REFERENCE_DELTA_BOUND_REQUIRED")
        fields(validated_live_delta, ("report_raw", "report", "supervision"), "REFERENCE_DELTA_LIVE_FIELDS")
        value, bound, plan = validated_live_delta, self._delta_bound, self._delta_plan
        selected, request = parse(grant.selection_raw, MIB), parse(bound.request_raw, 4*MIB)
        report = value["report"]
        need(type(value["report_raw"]) is bytes and 0 < len(value["report_raw"]) <= 8*MIB and
             A._writer_json(value["report_raw"], 8*MIB) == report, "REFERENCE_DELTA_REPORT_BYTES")
        fields(report, DELTA_REPORT_FIELDS, "REFERENCE_DELTA_REPORT_FIELDS")
        need(report["schema"] == "DMKN_ORDINARY_REFERENCE_MODULE_OUTPUT_V1" and
             report["assurance"] == "LOCAL_CHECKED_REFERENCE_MODULE_CONTROLLER_BOUND_IDENTITIES" and
             all(report[key] == request[key] for key in DELTA_REQUEST_FIELDS-{"schema", "units"}),
             "REFERENCE_DELTA_REPORT_BINDING")
        need(type(value["supervision"]) is dict and A._clean_worker(value["supervision"]) and
             json.loads(A.C.read_bounded(plan.supervision_path, MIB)) == value["supervision"],
             "REFERENCE_DELTA_NOT_CLEAN")
        reference, parent = self._delta_reference, self._delta_parent
        direct = ([row["module"] for row in parse(reference.snapshot.root_imports_raw, MIB)] if parent is None
                  else [module_name(parent.module_name)])
        rows = [row for unit in request["units"] for row in unit[2]]
        names = [row[0] for row in rows]
        need(report["direct_imports"] == direct and report["inventories"] == report["added_inventories"] == rows
             and report["names"] == report["added_names"] == names and
             all(report[key] == [] for key in ("matched_unit_indices", "matched_names", "matched_inventories")),
             "REFERENCE_DELTA_EXACT_NEW_INVENTORIES")
        expected_counts = {"units_checked": len(request["units"]), "units_matched": 0, "checking_passes": 2,
            "basis_rows": 581, "usable_basis_rows": len(reference.usable_basis_keys),
            "reference_public_units": len(reference.public_frontier),
            "reference_public_names": sum(len(outputs) for _, outputs in reference.public_frontier),
            "generated_names": 0 if parent is None else sum(len(outputs) for _, outputs in parent.frontier)}
        need(all(type(report[key]) is int and report[key] == count for key, count in expected_counts.items()),
             "REFERENCE_DELTA_COUNTERS")
        for path, raw in ((bound.paths.request_path, bound.request_raw), (bound.paths.inventory_path, bound.inventory_raw),
                (plan.reference_plan_path, plan.reference_plan_raw), (plan.generated_plan_path, self._delta_generated_raw),
                (grant.directory/"MATCH-INPUTS.json", bound.inputs_raw), (plan.report_path, value["report_raw"])):
            check(); need(A.C.read_bounded(path, len(raw)) == raw, "REFERENCE_DELTA_INPUT_CHANGED")
        context = self.owner.catalog.context(selected["source_context_root"]); self._context(context)
        if parent is None:
            need(self.load_reference(reference.reference_id, context, check) == reference, "REFERENCE_DELTA_BASE_CHANGED")
        else:
            need(self.load_delta(parent.delta_id, context, check) == parent, "REFERENCE_DELTA_PARENT_CHANGED")
        units = parse(bound.units_raw, 4*MIB)
        _, unit_names, added = self._delta_units(units)
        for key, (symbol, _) in unit_names.items():
            check(); need(context["bindings"].get(key) == symbol, "REFERENCE_DELTA_CURRENT_WARRANT")
        need(len(units)+(0 if parent is None else len(parent.frontier)) <= 1024 and
             len(unit_names)+(0 if parent is None else sum(len(outputs) for _, outputs in parent.frontier)) <= 16384,
             "REFERENCE_DELTA_CHAIN_CENSUS")
        artifact_rows = A.E._array(report["artifact_parts"], 5)
        artifact_pins, artifact_bytes = [], 0
        for row, suffix in zip(artifact_rows, SUFFIXES):
            fields(row, ("path", "bytes"), "REFERENCE_DELTA_ARTIFACT_FIELDS")
            path = grant.directory/"modules"/(plan.module_name+suffix)
            need(row["path"] == str(path) and type(row["bytes"]) is int, "REFERENCE_DELTA_ARTIFACT_PATH")
            actual = file_pin(path, 64*MIB, check)
            need(actual["bytes"] == row["bytes"], "REFERENCE_DELTA_ARTIFACT_SIZE")
            artifact_bytes += actual["bytes"]
            artifact_pins.append({"path": "operations/"+grant.identifier+"/modules/"+path.name, **actual})
        need(artifact_bytes <= 64*MIB and artifact_bytes+(0 if parent is None else parent.artifact_bytes) <= 256*MIB,
             "REFERENCE_DELTA_ARTIFACT_BOUND")
        actual_names = set()
        for path in (grant.directory/"modules").iterdir():
            check(); A.C.ordinary(path); actual_names.add(path.name)
            need(len(actual_names) <= 5, "REFERENCE_DELTA_PART_CENSUS")
        need(actual_names == {plan.module_name+suffix for suffix in SUFFIXES}, "REFERENCE_DELTA_PART_CENSUS")
        events = {name: {"path": "operations/"+grant.identifier+"/events/"+name,
            **file_pin(grant.directory/"events"/name, maximum, check)} for name, maximum in DELTA_EVENTS.items()}
        record = {"schema": RECORD_SCHEMA, "kind": "generated-delta", "store_binding": self.store_binding,
            "support_id": self.support_id, "operation_id": grant.identifier,
            "source_context_root": selected["source_context_root"], "reference_id": reference.reference_id,
            "parent_delta_id": selected["parent_delta_id"], "module_name": module_name(plan.module_name),
            "direct_imports": direct, "targets": selected["targets"], "materialization_key": selected["materialization_key"],
            "artifact_parts": artifact_pins, "units": units, "added_names": added, "event_files": events}
        raw = canonical(record)
        need(len(raw) <= 2*MIB and len(raw)+(0 if parent is None else sum(map(len, parent.records))) <= 4*MIB,
             "REFERENCE_DELTA_RECORD_BOUND")
        identity = A.sha(RECORD_DOMAIN+raw); self._record(raw, identity, kind="generated-delta")
        # Check prospective chain-plan size BEFORE the irrevocable record commit.
        generated = parse(self._delta_generated_raw, 4*MIB); generated["delta_id"] = identity
        generated["modules"].append({"delta_id": identity, "module_name": record["module_name"],
            "direct_imports": direct, "added_names": added, "artifact_parts": [
                {**part, "path": str(self.root.joinpath(*part["path"].split("/")))} for part in artifact_pins]})
        generated["bindings"].extend(units)
        need(len(canonical(generated)) <= 4*MIB, "REFERENCE_GENERATED_PLAN_BOUND")
        self._close_operation(grant, "LIVE_DELTA_THREE_PHASES_CLEAN_BEFORE_COMMIT")
        total, _ = self._census(check, allow_pending=grant)
        operation_bytes = self._operation_census(grant.directory, grant.kind, check)
        need(total+2*len(raw) <= LIMITS["max_store_bytes"] and operation_bytes+len(raw) <= 128*MIB,
             "REFERENCE_DELTA_COMMIT_CAPACITY")
        staging = grant.directory/"record.staged.json"; A.P.PortableCatalog._write_fresh(staging, raw)
        self._grant_live(grant, check)
        destination = A.C.ordinary(self.root/"records"/(identity+".json"), fresh=True)
        need(os.name == "nt", "REFERENCE_NONOVERWRITING_WINDOWS_COMMIT"); self._commit_attempted = True
        try:
            os.rename(staging, destination)
            need(A.C.read_bounded(destination, 2*MIB) == raw, "REFERENCE_DELTA_COMMIT_READBACK")
        except BaseException as error:
            self._denied = True
            raise ReferenceCommitUnknown(identity, kind="generated-delta") from error
        self._grant = self._bound = None
        self._delta_reference = self._delta_parent = self._delta_plan = self._delta_bound = self._delta_generated_raw = None
        try:
            return self.load_delta(identity, context, check)
        except BaseException as error:
            raise ReferenceCommittedError(identity, kind="generated-delta") from error


def open_for_owner(owner, selected_support, check):
    """Create only a genuinely missing sidecar; never adopt another tree."""
    need(type(owner) is A.OrdinaryAdmission and type(owner.catalog) is A.P.PortableCatalog
         and callable(check) and Q.A is A and R.A is A and R.Q is Q and V.A is A and P.A is A,
         "REFERENCE_OWNER_CONFIGURATION")
    check(); owner.catalog._active()
    need(owner.catalog._lock is not None and not owner.catalog._lock.closed, "REFERENCE_OWNER_LOCK")
    support = parse(selected_support, MIB)
    fields(support, ("schema", "installation_manifest_sha256", "semantic_id", "foundation_id",
        "implementation_id", "policy", "sources", "native_helpers"), "REFERENCE_SUPPORT_FIELDS")
    installation = owner.installation
    need(support["schema"] == SUPPORT_SCHEMA and
         support["installation_manifest_sha256"] == installation.manifest_sha256 and
         support["semantic_id"] == installation.semantic_id == A.S.semantic_id() and
         support["foundation_id"] == A.S.foundation_id() and
         support["implementation_id"] == installation.implementation_id and
         type(support["policy"]) is str and 0 < len(support["policy"]) <= 256, "REFERENCE_SUPPORT_BINDING")
    need(type(support["sources"]) is dict and 1 <= len(support["sources"]) <= 64, "REFERENCE_SUPPORT_SOURCES")
    for role, pin in support["sources"].items():
        need(type(role) is str and 0 < len(role) <= 128, "REFERENCE_SUPPORT_ROLE"); pin_shape(pin, 2*MIB)
    need(type(support["native_helpers"]) is list and 1 <= len(support["native_helpers"]) <= 64,
         "REFERENCE_SUPPORT_HELPERS")
    names = []
    for row in support["native_helpers"]:
        need(type(row) is list and len(row) == 3, "REFERENCE_HELPER_PIN")
        name, size, digest = row
        need(type(name) is str and 0 < len(name) <= 256, "REFERENCE_HELPER_NAME")
        pin_shape({"bytes": size, "sha256": digest}, 128*MIB); names.append(name)
    need(names == sorted(set(names)), "REFERENCE_HELPER_ORDER")
    self = Store()
    self.owner, self.catalog_root = owner, owner.catalog._root
    self.adoption_raw, self.activation_raw = owner.catalog._marker, owner.catalog._activation_raw
    self.semantic_id, self.foundation_id = installation.semantic_id, A.S.foundation_id()
    self.implementation_id = installation.implementation_id
    self.support_id = A.sha(SUPPORT_DOMAIN+selected_support)
    self.root = self.catalog_root/"ordinary-realizations-v1"
    self._grant = self._bound = None
    self._delta_reference = self._delta_parent = self._delta_plan = self._delta_bound = self._delta_generated_raw = None
    self._commit_attempted = self._denied = False
    self.marker_raw = canonical({"schema": STORE_SCHEMA, "store_id": owner.catalog._store_id,
        "adoption_sha256": A.sha(self.adoption_raw), "activation_sha256": A.sha(self.activation_raw),
        "semantic_id": self.semantic_id, "foundation_id": self.foundation_id,
        "implementation_id": self.implementation_id, "limits": LIMITS})
    self.store_binding = A.sha(self.marker_raw)
    if not os.path.lexists(self.root):
        self._owner_live(); A.C.ordinary(self.root, directory=True, fresh=True).mkdir()
        (self.root/"operations").mkdir(); (self.root/"records").mkdir()
        A.P.PortableCatalog._write_fresh(self.root/"STORE.json", self.marker_raw)
    else:
        A.C.ordinary(self.root, directory=True)
        need(A.C.read_bounded(self.root/"STORE.json", 65536) == self.marker_raw, "REFERENCE_STORE_MARKER")
    self._census(check)
    return self

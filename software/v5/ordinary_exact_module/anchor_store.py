"""Protected owner-local realizations of already warranted ordinary mathematics.

No peer-facing registration, saved-report recovery, admission, native import or
generic artifact adoption exists here. The selected export controller is trusted
to call _commit_generated only after its actual clean three-phase event. Hashes
preserve that event's exact bytes; they do not prove that the event took place.
The catalog's owner lock, unchanged selected support, immutable local storage and
no hostile administrator/rollback are the same premises as ordinary admission.
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
import module_closure as M

MIB = 1024**2
STORE_SCHEMA = "DMKN_LOCAL_MODULE_ANCHOR_STORE_V1"
RECORD_SCHEMA = "DMKN_LOCAL_MODULE_ANCHOR_V1"
PLAN_SCHEMA = "DMKN_LOCAL_MODULE_ANCHOR_PLAN_V1"
SUPPORT_SCHEMA = "DMKN_LOCAL_MODULE_ANCHOR_SUPPORT_V1"
RECORD_DOMAIN = b"DMKN-LOCAL-MODULE-ANCHOR-V1\0"
SUPPORT_DOMAIN = b"DMKN-LOCAL-MODULE-ANCHOR-SUPPORT-V1\0"
KEY_DOMAIN = b"DMKN-ORDINARY-ANCHORED-MODULE-V1\0"
PART_SUFFIXES = (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir")
EVENT_NAMES = ("request.json", "inventory.json", "anchor-plan.json", "native-report.json",
               "native-report.json.pending", "native-report.json.phases.jsonl", "SUPERVISION.json")
LIMITS = {"max_chain": 32, "max_units": 1024, "max_names": 16384,
    "max_artifact_bytes": 256*MIB, "max_module_bytes": 64*MIB,
    "max_record_bytes": 2*MIB, "max_records_bytes": 4*MIB, "max_plan_bytes": 4*MIB,
    "max_operation_bytes": 128*MIB, "max_metadata_bytes": 32*MIB,
    "max_operations": 256, "max_store_bytes": 1024*MIB}
RECORD_FIELDS = {"schema", "store_binding", "support_id", "operation_id", "source_context_root",
    "parent_anchor_id", "module_name", "direct_imports", "targets", "materialization_key",
    "artifact_parts", "units", "added_names", "matched_names", "event_files"}


class AnchorError(ValueError):
    """Local operational refusal, never a judgment that mathematics is false."""


class AnchorCommitUnknown(AnchorError):
    def __init__(self, anchor_id):
        self.anchor_id = anchor_id
        self.report = {"status": "COMMIT_UNKNOWN", "anchor_id": anchor_id,
            "new_catalog_acceptance": False,
            "retention": "EXACT_ID_LOOKUP_ONLY_NO_AUTOMATIC_RETRY_OR_RECONSTRUCTION"}
        super().__init__("ANCHOR_COMMIT_UNKNOWN:"+anchor_id)


class AnchorCommittedError(AnchorError):
    def __init__(self, anchor_id):
        self.anchor_id = anchor_id
        self.report = {"status": "COMMITTED_LOCAL_ANCHOR_REPORTING_FAILED", "anchor_id": anchor_id,
            "new_catalog_acceptance": False,
            "retention": "COMMITTED_RECORD_PRESERVED_EXACT_ID_LOOKUP_AVAILABLE"}
        super().__init__("ANCHOR_COMMITTED_REPORTING_FAILED:"+anchor_id)


def need(condition, code):
    if not condition:
        raise AnchorError(code)


def fields(value, keys, code):
    need(type(value) is dict and set(value) == set(keys), code)


def canonical(value):
    return A.E.canonical_json(value)


def parse(raw, maximum):
    # The registry format has no booleans, nulls or floating-point values. Reuse
    # the strict bounded canonical codec; mathematical peer parsers are unchanged.
    return A.E.strict_json(raw, A.E.Limits(max_bytes=maximum))


def matched_realization(unit):
    """Classify a protected matched unit; this is not installed-record proof.

    The inert codec checks shapes, safety flags and bounded expression packets.
    These additional checks bind the descriptor to its claimed inventory. Only
    the live native event establishes exact kernel/frontend and public records,
    prefix-closed semantics, and the accepted complete generated-unit premise.
    In particular, a recursor count cannot be inferred from reduced metadata.
    """
    A.E.inspect_unit(unit)
    descriptor, rows = unit[1], unit[2]
    tag = descriptor[0]
    if tag < 3:
        name, params, type_dag, body = descriptor[1:5]
        need(descriptor[-1] == [name], "ANCHOR_MATCHED_SINGLETON_ALL")
        if tag == 0:
            expected = [name, 1, params, type_dag, [body, descriptor[5], [name]]]
        elif tag == 1:
            expected = [name, 2, params, type_dag, [body, [name]]]
        else:
            expected = [name, 3, params, type_dag, [body, 0, [name]]]
        need(rows == [expected], "ANCHOR_MATCHED_DESCRIPTOR_INVENTORY")
        return "installed-singleton-theorem" if tag == 1 else "installed-exact-nontheorem"

    # No whole-environment enumeration or name-based completeness inference.
    # The full ordered inventory remains bound to the warranted request unit.
    params, num_params, types = descriptor[1:]
    group = [entry[0] for entry in types]
    by_name = {A.E.name_key(row[0]): row for row in rows}
    declared = {A.E.name_key(name) for name in group}
    constructors = {}
    need(all(row[1] in (4, 5, 6) for row in rows), "ANCHOR_MATCHED_GROUP_KIND")
    for name, type_dag, ctors in types:
        row = by_name[A.E.name_key(name)]
        details = row[4]
        need(row[1] == 4 and row[2:4] == [params, type_dag] and
             details[0] == num_params and details[2] == group and
             details[3] == [ctor[0] for ctor in ctors], "ANCHOR_MATCHED_GROUP_TYPE")
        for index, (ctor_name, ctor_type) in enumerate(ctors):
            key = A.E.name_key(ctor_name)
            ctor = by_name[key]
            need(ctor[1] == 5 and ctor[2:4] == [params, ctor_type] and
                 ctor[4][:3] == [name, index, num_params], "ANCHOR_MATCHED_GROUP_CONSTRUCTOR")
            constructors[key] = ctor
    need({A.E.name_key(row[0]) for row in rows if row[1] == 4} == declared and
         {A.E.name_key(row[0]) for row in rows if row[1] == 5} == set(constructors),
         "ANCHOR_MATCHED_GROUP_CENSUS")
    for row in rows:
        if row[1] == 6:
            details = row[4]
            need(details[0] == group and details[1] == num_params,
                 "ANCHOR_MATCHED_GROUP_RECURSOR")
            seen = set()
            for ctor_name, num_fields, _ in details[5]:
                key = A.E.name_key(ctor_name)
                need(key in constructors and key not in seen and
                     constructors[key][4][3] == num_fields, "ANCHOR_MATCHED_GROUP_RULE")
                seen.add(key)
    return "installed-exact-nontheorem"


def module_name(text):
    need(type(text) is str and text.startswith("DMKNBridge_") and len(text) == 75,
         "ANCHOR_MODULE_NAME")
    A.C.hexid(text[11:])
    return [[0, {"$bytes": list(text.encode("ascii"))}]]


def module_text(name):
    A.E.name_key(name)
    need(type(name) is list and len(name) == 1 and name[0][0] == 0,
         "ANCHOR_MODULE_NAME")
    text = bytes(name[0][1]["$bytes"]).decode("ascii")
    need(module_name(text) == name, "ANCHOR_MODULE_NAME")
    return text


def materialization_key(support_id, parent_anchor_id, targets):
    A.C.hexid(support_id)
    if parent_anchor_id:
        A.C.hexid(parent_anchor_id)
    else:
        need(parent_anchor_id == "", "ANCHOR_PARENT_ID")
    return A.sha(KEY_DOMAIN+canonical({"support_id": support_id,
        "parent_anchor_id": parent_anchor_id, "targets": targets}))


def _pin(value, maximum):
    fields(value, ("bytes", "sha256"), "ANCHOR_PIN_FIELDS")
    need(type(value["bytes"]) is int and 0 < value["bytes"] <= maximum,
         "ANCHOR_PIN_BOUND")
    A.C.hexid(value["sha256"])
    return value


def _verify(path, pin, maximum, check):
    _pin(pin, maximum)
    path = A.C.ordinary(path)
    check()
    need(path.stat().st_size == pin["bytes"], "ANCHOR_FILE_SIZE")
    size, digest = 0, hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            check()
            size += len(block)
            need(size <= pin["bytes"], "ANCHOR_FILE_GREW")
            digest.update(block)
    need(size == pin["bytes"] and path.stat().st_size == size and
         digest.hexdigest() == pin["sha256"], "ANCHOR_FILE_CHANGED")
    return path


@dataclass(frozen=True)
class AnchorView:
    anchor_id: str
    module_name: str
    materialization_key: str
    module_directory: Path
    import_directories: tuple[Path, ...]
    frontier: M.AnchorFrontier
    plan_raw: bytes
    records: tuple[bytes, ...]
    artifact_bytes: int
    store_binding: str
    support_id: str


@dataclass(frozen=True)
class _Grant:
    identifier: str
    directory: Path
    deadline: float
    parent: AnchorView | None
    selection_raw: bytes
    check: object


class Store:
    """Serialized sidecar; it owns no independent owner lock or acceptance DB."""

    def _owner_live(self):
        owner = self.owner
        need(type(owner) is A.OrdinaryAdmission and type(owner.catalog) is A.P.PortableCatalog,
             "ANCHOR_OWNER_TYPE")
        catalog = owner.catalog
        catalog._active()
        need(catalog._lock is not None and not catalog._lock.closed and
             catalog._root == self.catalog_root and
             catalog._marker == self.adoption_raw and catalog._activation_raw == self.activation_raw,
             "ANCHOR_OWNER_BINDING")
        need(A.C.read_bounded(catalog._root/"ADOPTION.json", 65536) == self.adoption_raw,
             "ANCHOR_ADOPTION_CHANGED")

    def _live(self, check):
        need(callable(check), "ANCHOR_CHECK_CALLBACK")
        check()
        self._owner_live()
        need(not self._denied and not os.path.lexists(self.root/"BLOCKED"), "ANCHOR_BLOCKED")
        need(A.C.read_bounded(self.root/"STORE.json", 65536) == self.marker_raw,
             "ANCHOR_STORE_CHANGED")

    def _census(self, check, *, allow_pending=None):
        """Bound actual retained bytes, including orphans; no content discovery."""
        self._live(check)
        total, entries, operations = 0, 0, 0
        operation_bytes, metadata_bytes = {}, {}
        pending = [(self.root, 0)]
        operation_paths = []
        while pending:
            directory, depth = pending.pop()
            A.C.ordinary(directory, directory=True)
            with os.scandir(directory) as listing:
                for entry in listing:
                    check(); entries += 1
                    need(entries <= 8192, "ANCHOR_STORE_ENTRY_BOUND")
                    path = Path(entry.path)
                    if entry.is_dir(follow_symlinks=False):
                        need(depth < 4, "ANCHOR_STORE_DEPTH")
                        A.C.ordinary(path, directory=True)
                        if directory == self.root:
                            need(path.name in ("operations", "records"), "ANCHOR_STORE_DIRECTORY")
                        elif directory == self.root/"operations":
                            A.C.hexid(path.name)
                            operations += 1
                            need(operations <= LIMITS["max_operations"], "ANCHOR_OPERATION_COUNT")
                            operation_paths.append(path)
                        else:
                            need(directory.parent == self.root/"operations" and
                                 path.name in ("modules", "events"), "ANCHOR_OPERATION_DIRECTORY")
                        pending.append((path, depth+1))
                    else:
                        A.C.ordinary(path)
                        size = path.stat().st_size
                        need(0 <= size <= LIMITS["max_operation_bytes"], "ANCHOR_STORED_FILE_BOUND")
                        total += size
                        need(total <= LIMITS["max_store_bytes"], "ANCHOR_STORE_BYTE_BOUND")
                        relative = path.relative_to(self.root).parts
                        if len(relative) >= 3 and relative[0] == "operations":
                            identity = relative[1]
                            operation_bytes[identity] = operation_bytes.get(identity, 0)+size
                            need(operation_bytes[identity] <= LIMITS["max_operation_bytes"],
                                 "ANCHOR_OPERATION_BYTE_BOUND")
                            if relative[2] != "modules":
                                metadata_bytes[identity] = metadata_bytes.get(identity, 0)+size
                                need(metadata_bytes[identity] <= LIMITS["max_metadata_bytes"],
                                     "ANCHOR_OPERATION_METADATA_BOUND")
                        if directory == self.root:
                            need(path.name == "STORE.json", "ANCHOR_STORE_FILE")
        for operation in operation_paths:
            check()
            reservation = parse(A.C.read_bounded(operation/"RESERVATION.json", MIB), MIB)
            fields(reservation, ("schema", "operation_id", "store_binding", "support_id",
                "parent_anchor_id", "selection"), "ANCHOR_RESERVATION_FIELDS")
            need(reservation["schema"] == "DMKN_LOCAL_MODULE_RESERVATION_V1" and
                 reservation["operation_id"] == operation.name and
                 reservation["store_binding"] == self.store_binding,
                 "ANCHOR_RESERVATION_BINDING")
            if allow_pending is not None and operation == allow_pending.directory:
                continue
            closed = parse(A.C.read_bounded(operation/"CLOSED.json", 4096), 4096)
            fields(closed, ("schema", "operation_id", "store_binding", "reason"),
                   "ANCHOR_CLOSED_FIELDS")
            need(closed["schema"] == "DMKN_LOCAL_MODULE_OPERATION_CLOSED_V1" and
                 closed["operation_id"] == operation.name and closed["store_binding"] == self.store_binding and
                 type(closed["reason"]) is str and 0 < len(closed["reason"]) <= 256,
                 "ANCHOR_OPERATION_CLEANUP_UNKNOWN")
        return total, operations

    def _targets(self, value):
        need(type(value) is list and 1 <= len(value) <= 32 and len(canonical(value)) <= 65536,
             "ANCHOR_TARGET_BOUND")
        keys = []
        for row in value:
            fields(row, ("name", "export_id", "unit_id"), "ANCHOR_TARGET_FIELDS")
            key = A.E.name_key(row["name"])
            keys.append(key)
            A.C.hexid(row["export_id"]); A.C.hexid(row["unit_id"])
            need(A.S.export_id(self.semantic_id, row["unit_id"], row["name"]) == row["export_id"],
                 "ANCHOR_TARGET_EXPORT_BINDING")
        need(keys == sorted(set(keys)), "ANCHOR_TARGET_ORDER")

    def _units(self, value):
        need(type(value) is list and 1 <= len(value) <= 32, "ANCHOR_RECORD_UNIT_BOUND")
        units, names, added, matched = set(), {}, [], []
        for row in value:
            fields(row, ("unit_id", "outputs", "realization"), "ANCHOR_UNIT_FIELDS")
            identity = A.C.hexid(row["unit_id"])
            need(identity not in units, "ANCHOR_DUPLICATE_UNIT")
            units.add(identity)
            need(row["realization"] in ("added", "installed-singleton-theorem",
                 "installed-exact-nontheorem"), "ANCHOR_REALIZATION")
            outputs = row["outputs"]
            need(type(outputs) is list and 1 <= len(outputs) <= 4096,
                 "ANCHOR_UNIT_OUTPUT_BOUND")
            for output in outputs:
                fields(output, ("name", "export_id", "kind", "level_params", "inventory_sha256"),
                       "ANCHOR_OUTPUT_FIELDS")
                key = A.E.name_key(output["name"])
                need(key not in names and key not in self.basis_names and len(names) < 4096,
                     "ANCHOR_OUTPUT_NAME_CONFLICT")
                A.C.hexid(output["export_id"]); A.C.hexid(output["inventory_sha256"])
                need(A.S.export_id(self.semantic_id, identity, output["name"]) == output["export_id"],
                     "ANCHOR_OUTPUT_EXPORT_BINDING")
                need(type(output["kind"]) is int and 1 <= output["kind"] <= 6 and
                     type(output["level_params"]) is list and len(output["level_params"]) <= 1024,
                     "ANCHOR_OUTPUT_METADATA")
                levels = [A.E.name_key(name) for name in output["level_params"]]
                need(len(set(levels)) == len(levels), "ANCHOR_LEVEL_PARAMS")
                names[key] = (output["export_id"], identity)
                (added if row["realization"] == "added" else matched).append(output["name"])
            kinds = [output["kind"] for output in outputs]
            if row["realization"] == "installed-singleton-theorem":
                need(kinds == [2], "ANCHOR_MATCHED_SINGLETON")
            elif row["realization"] == "installed-exact-nontheorem":
                # Full coherence was checked at the protected live commit. This
                # compact record is not a freestanding complete-group warrant.
                need(kinds in ([1], [3]) or
                     (4 in kinds and all(kind in (4, 5, 6) for kind in kinds)),
                     "ANCHOR_MATCHED_EXACT_NONTHEOREM")
        return units, names, added, matched

    def _record(self, raw, expected_id):
        need(A.sha(RECORD_DOMAIN+raw) == expected_id, "ANCHOR_RECORD_ADDRESS")
        value = parse(raw, LIMITS["max_record_bytes"])
        fields(value, RECORD_FIELDS, "ANCHOR_RECORD_FIELDS")
        need(value["schema"] == RECORD_SCHEMA and value["store_binding"] == self.store_binding and
             value["support_id"] == self.support_id, "ANCHOR_RECORD_SUPPORT")
        operation = A.C.hexid(value["operation_id"])
        A.C.hexid(value["source_context_root"])
        parent = value["parent_anchor_id"]
        need(type(parent) is str, "ANCHOR_PARENT_ID")
        if parent:
            A.C.hexid(parent)
        self._targets(value["targets"])
        key = materialization_key(self.support_id, parent, value["targets"])
        text = module_text(value["module_name"])
        need(value["materialization_key"] == key and text == "DMKNBridge_"+key,
             "ANCHOR_MATERIALIZATION_BINDING")
        direct = value["direct_imports"]
        need(type(direct) is list and len(direct) == 1, "ANCHOR_DIRECT_IMPORTS")
        A.E.name_key(direct[0])
        _, _, added, matched = self._units(value["units"])
        need(bool(added) and value["added_names"] == added and value["matched_names"] == matched,
             "ANCHOR_UNIT_PARTITION")
        parts = value["artifact_parts"]
        need(type(parts) is list and len(parts) == 5, "ANCHOR_PART_CENSUS")
        total = 0
        for part, suffix in zip(parts, PART_SUFFIXES):
            fields(part, ("path", "bytes", "sha256"), "ANCHOR_PART_FIELDS")
            need(part["path"] == f"operations/{operation}/modules/{text}{suffix}", "ANCHOR_PART_PATH")
            _pin({key: part[key] for key in ("bytes", "sha256")}, LIMITS["max_module_bytes"])
            total += part["bytes"]
        need(total <= LIMITS["max_module_bytes"], "ANCHOR_MODULE_BYTE_BOUND")
        fields(value["event_files"], EVENT_NAMES, "ANCHOR_EVENT_CENSUS")
        total = 0
        for name, pin in value["event_files"].items():
            fields(pin, ("path", "bytes", "sha256"), "ANCHOR_EVENT_FIELDS")
            need(pin["path"] == f"operations/{operation}/events/{name}", "ANCHOR_EVENT_PATH")
            _pin({key: pin[key] for key in ("bytes", "sha256")}, 8*MIB)
            total += pin["bytes"]
        need(total <= LIMITS["max_metadata_bytes"], "ANCHOR_METADATA_BOUND")
        return value

    def plan(self, parent=None):
        if parent is None:
            return canonical({"schema": PLAN_SCHEMA, "anchor_id": "", "support_id": self.support_id,
                              "modules": [], "bindings": []})
        need(type(parent) is AnchorView and parent.store_binding == self.store_binding and
             parent.support_id == self.support_id, "ANCHOR_VIEW_BINDING")
        return parent.plan_raw

    def load(self, anchor_id, current_context, check):
        self._live(check)
        A.C.hexid(anchor_id)
        fields_subset = {"semantic_id": self.semantic_id, "foundation_id": self.foundation_id,
                         "implementation_id": self.implementation_id}
        need(type(current_context) is dict and type(current_context.get("bindings")) is dict and
             all(current_context.get(key) == value for key, value in fields_subset.items()),
             "ANCHOR_CONTEXT_POLICY")
        # The caller supplies the catalog's just-validated context; it is not peer input.
        reverse, seen, current, record_bytes = [], set(), anchor_id, 0
        while current:
            self._live(check)
            need(current not in seen and len(seen) < LIMITS["max_chain"], "ANCHOR_CHAIN_BOUND")
            seen.add(current)
            raw = A.C.read_bounded(self.root/"records"/(current+".json"), LIMITS["max_record_bytes"])
            record_bytes += len(raw)
            need(record_bytes <= LIMITS["max_records_bytes"], "ANCHOR_CHAIN_METADATA_BOUND")
            record = self._record(raw, current)
            reverse.append((current, raw, record))
            current = record["parent_anchor_id"]
        ordered = list(reversed(reverse))
        modules, bindings, unit_ids, names, frontier, directories = [], [], set(), {}, [], []
        artifact_bytes = 0
        previous_name = [[0, {"$bytes": list(b"Init")}]]
        previous_id = ""
        for identity, raw, record in ordered:
            check()
            need(record["parent_anchor_id"] == previous_id and record["direct_imports"] == [previous_name],
                 "ANCHOR_EXACT_PARENT_CHAIN")
            record_units, record_names, _, _ = self._units(record["units"])
            need(not unit_ids.intersection(record_units) and not names.keys() & record_names.keys(),
                 "ANCHOR_CHAIN_COLLISION")
            unit_ids.update(record_units); names.update(record_names)
            need(len(unit_ids) <= LIMITS["max_units"] and len(names) <= LIMITS["max_names"],
                 "ANCHOR_CHAIN_CENSUS")
            for key, (export_id, _) in record_names.items():
                check()
                need(current_context["bindings"].get(key) == export_id,
                     "ANCHOR_CURRENT_CONTEXT_MISMATCH")
            parts = []
            for part in record["artifact_parts"]:
                artifact_bytes += part["bytes"]
                need(artifact_bytes <= LIMITS["max_artifact_bytes"], "ANCHOR_CHAIN_ARTIFACT_BOUND")
                pin = {key: part[key] for key in ("bytes", "sha256")}
                path = self.root.joinpath(*part["path"].split("/"))
                _verify(path, pin, LIMITS["max_module_bytes"], check)
                parts.append(dict(pin, path=str(path)))
            directory = Path(parts[0]["path"]).parent
            need({p.name for p in directory.iterdir()} == {Path(p["path"]).name for p in parts},
                 "ANCHOR_MODULE_DIRECTORY_CENSUS")
            directories.append(directory)
            modules.append({"anchor_id": identity, "module_name": record["module_name"],
                "direct_imports": record["direct_imports"], "added_names": record["added_names"],
                "artifact_parts": parts})
            bindings.extend(record["units"])
            for unit in record["units"]:
                frontier.append((unit["unit_id"], tuple((A.E.name_key(row["name"]), row["export_id"])
                                for row in unit["outputs"])))
            for target in record["targets"]:
                need(names.get(A.E.name_key(target["name"])) == (target["export_id"], target["unit_id"]),
                     "ANCHOR_TARGET_REALIZATION")
            previous_name, previous_id = record["module_name"], identity
        plan_raw = canonical({"schema": PLAN_SCHEMA, "anchor_id": anchor_id,
            "support_id": self.support_id, "modules": modules, "bindings": bindings})
        need(len(plan_raw) <= LIMITS["max_plan_bytes"], "ANCHOR_PLAN_BOUND")
        self._live(check)
        last = ordered[-1][2]
        return AnchorView(anchor_id, module_text(last["module_name"]), last["materialization_key"],
            directories[-1], tuple(directories), M.AnchorFrontier(anchor_id, tuple(frontier)),
            plan_raw, tuple(raw for _, raw, _ in ordered), artifact_bytes,
            self.store_binding, self.support_id)

    def reserve(self, parent, selected_request_pins, check, *, deadline):
        self._live(check)
        need(self._grant is None and not self._commit_attempted, "ANCHOR_OPERATION_ACTIVE")
        need(type(deadline) in (int, float) and math.isfinite(deadline) and
             time.monotonic() < deadline, "ANCHOR_DEADLINE")
        value = parse(canonical(selected_request_pins), MIB)
        fields(value, ("source_context_root", "targets", "materialization_key", "request", "inventory",
                       "anchor_plan"), "ANCHOR_SELECTION_FIELDS")
        A.C.hexid(value["source_context_root"])
        self._targets(value["targets"])
        for role, maximum in (("request", 4*MIB), ("inventory", MIB), ("anchor_plan", 4*MIB)):
            _pin(value[role], maximum)
        parent_id = "" if parent is None else parent.anchor_id
        expected_plan = self.plan(parent)
        need(value["anchor_plan"] == {"bytes": len(expected_plan), "sha256": A.sha(expected_plan)} and
             value["materialization_key"] == materialization_key(self.support_id, parent_id, value["targets"]),
             "ANCHOR_SELECTION_BINDING")
        context = self.owner.catalog.context(value["source_context_root"])
        if parent is not None:
            current = self.load(parent_id, context, check)
            need(current == parent and len(parent.records) < LIMITS["max_chain"], "ANCHOR_PARENT_CHANGED")
        total, operations = self._census(check)
        need(operations < LIMITS["max_operations"] and
             total+LIMITS["max_operation_bytes"] <= LIMITS["max_store_bytes"], "ANCHOR_RESERVATION_CAPACITY")
        identifier = secrets.token_hex(32)
        directory = A.C.ordinary(self.root/"operations"/identifier, directory=True, fresh=True)
        directory.mkdir()
        reservation = {"schema": "DMKN_LOCAL_MODULE_RESERVATION_V1", "operation_id": identifier,
            "store_binding": self.store_binding, "support_id": self.support_id,
            "parent_anchor_id": parent_id, "selection": value}
        A.P.PortableCatalog._write_fresh(directory/"RESERVATION.json", canonical(reservation))
        grant = _Grant(identifier, directory, float(deadline), parent, canonical(value), check)
        self._grant = grant
        return grant

    def _grant_live(self, grant, check):
        need(type(grant) is _Grant and self._grant is grant and grant.check is check,
             "ANCHOR_LIVE_GRANT_REQUIRED")
        self._live(check)
        need(time.monotonic() < grant.deadline, "ANCHOR_DEADLINE")

    def _close_operation(self, grant, reason):
        # Cleanup recording must remain possible after the mathematical allowance
        # expires. No native work or acceptance is authorized by this bounded write.
        self._owner_live()
        need(type(grant) is _Grant and self._grant is grant and type(reason) is str and
             0 < len(reason) <= 256, "ANCHOR_CLOSE_GRANT")
        path = grant.directory/"CLOSED.json"
        value = {"schema": "DMKN_LOCAL_MODULE_OPERATION_CLOSED_V1", "operation_id": grant.identifier,
                 "store_binding": self.store_binding, "reason": reason}
        if os.path.lexists(path):
            previous = parse(A.C.read_bounded(path, 4096), 4096)
            need(set(previous) == set(value) and all(previous[key] == value[key]
                 for key in ("schema", "operation_id", "store_binding")) and
                 type(previous["reason"]) is str and 0 < len(previous["reason"]) <= 256,
                 "ANCHOR_CLOSED_CHANGED")
        else:
            A.P.PortableCatalog._write_fresh(path, canonical(value))

    def abandon(self, grant, reason):
        """Trusted controller: no child started, or cleanup is actually complete."""
        if self._grant is not grant or self._commit_attempted:
            return
        self._close_operation(grant, reason)
        self._grant = None

    def mark_blocked(self, grant, reason, check=None):
        """Uncertain child cleanup; budget expiry must not prevent this marker.

        An unclosed reservation also independently blocks a fresh open. Thus a
        marker-write failure cannot silently convert uncertain cleanup to success.
        """
        self._owner_live()
        need(self._grant is grant and type(reason) is str and 0 < len(reason) <= 256,
             "ANCHOR_BLOCK_GRANT")
        self._denied = True
        if not os.path.lexists(self.root/"BLOCKED"):
            A.P.PortableCatalog._write_fresh(self.root/"BLOCKED", canonical({
                "schema": "DMKN_LOCAL_MODULE_ANCHOR_BLOCKED_V1", "operation_id": grant.identifier,
                "store_binding": self.store_binding, "reason": reason}))

    def _commit_generated(self, grant, validated_live_export, check):
        """PRIVATE live-event commit, never a saved report's adoption API."""
        self._grant_live(grant, check)
        fields(validated_live_export, ("request", "report", "artifact_parts", "event_files"),
               "ANCHOR_LIVE_EXPORT_FIELDS")
        value = validated_live_export
        selected = parse(grant.selection_raw, MIB)
        request_raw = value["request"]
        need(type(request_raw) is bytes and selected["request"] == {
            "bytes": len(request_raw), "sha256": A.sha(request_raw)}, "ANCHOR_LIVE_REQUEST_PIN")
        request = parse(request_raw, 4*MIB)
        fields(request, ("schema", "semantic_id", "foundation_id", "context_root", "module_name",
            "targets", "unit_ids", "units", "anchor_id", "anchor_plan_sha256"), "ANCHOR_REQUEST_FIELDS")
        parent_id = "" if grant.parent is None else grant.parent.anchor_id
        need(request["schema"] == M.REQUEST_SCHEMA and request["semantic_id"] == self.semantic_id and
             request["foundation_id"] == self.foundation_id and
             request["context_root"] == selected["source_context_root"] and
             request["anchor_id"] == parent_id and request["anchor_plan_sha256"] == selected["anchor_plan"]["sha256"] and
             request["targets"] == [row["name"] for row in selected["targets"]] and
             request["module_name"] == module_name("DMKNBridge_"+selected["materialization_key"]),
             "ANCHOR_LIVE_REQUEST_BINDING")
        report = value["report"]
        need(type(report) is dict and report.get("checking_passes") == 2 and
             all(report.get(key) == request[key] for key in ("semantic_id", "foundation_id", "context_root",
                  "module_name", "targets", "unit_ids", "anchor_id", "anchor_plan_sha256")),
             "ANCHOR_LIVE_REPORT_BINDING")
        need(type(request["units"]) is list and 1 <= len(request["units"]) <= 32 and
             type(request["unit_ids"]) is list and len(request["unit_ids"]) == len(request["units"]),
             "ANCHOR_DELTA_BOUND")
        matched = report.get("matched_unit_indices")
        need(type(matched) is list and len(matched) < len(request["units"]) and
             all(type(index) is int and 0 <= index < len(request["units"]) for index in matched) and
             matched == sorted(set(matched)),
             "ANCHOR_MATCHED_INDICES")
        units = []
        for index, (identity, unit) in enumerate(zip(request["unit_ids"], request["units"])):
            A.C.hexid(identity)
            if index in matched:
                realization = matched_realization(unit)
            else:
                A.E.inspect_unit(unit)
                realization = "added"
            outputs = [{"name": row[0], "export_id": A.S.export_id(self.semantic_id, identity, row[0]),
                        "kind": row[1], "level_params": row[2], "inventory_sha256": A.sha(canonical(row))}
                       for row in unit[2]]
            units.append({"unit_id": identity, "outputs": outputs,
                "realization": realization})
        _, names, added, matched_names = self._units(units)
        need(bool(added) and report.get("added_names") == added and report.get("matched_names") == matched_names,
             "ANCHOR_LIVE_PARTITION")
        events = value["event_files"]
        fields(events, EVENT_NAMES, "ANCHOR_EVENT_CENSUS")
        need(type(value["artifact_parts"]) is list and len(value["artifact_parts"]) == 5,
             "ANCHOR_LIVE_PARTS")
        artifact_total = event_total = 0
        for pin in value["artifact_parts"]:
            fields(pin, ("path", "bytes", "sha256"), "ANCHOR_COPY_PIN")
            _pin({key: pin[key] for key in ("bytes", "sha256")}, LIMITS["max_module_bytes"])
            artifact_total += pin["bytes"]
        for pin in events.values():
            fields(pin, ("path", "bytes", "sha256"), "ANCHOR_COPY_PIN")
            _pin({key: pin[key] for key in ("bytes", "sha256")}, 8*MIB)
            event_total += pin["bytes"]
        reservation_bytes = A.C.ordinary(grant.directory/"RESERVATION.json").stat().st_size
        # Reserve metadata headroom BEFORE any copy. Even a failed partial copy
        # must remain below the same reopen/census ceilings; rejecting only after
        # the last write would poison an otherwise cleanly closed operation.
        metadata_envelope = event_total+reservation_bytes+4096+LIMITS["max_record_bytes"]
        need(artifact_total <= LIMITS["max_module_bytes"] and
             metadata_envelope <= LIMITS["max_metadata_bytes"] and
             artifact_total+metadata_envelope <= LIMITS["max_operation_bytes"],
             "ANCHOR_COPY_CAPACITY")
        for directory in (grant.directory/"modules", grant.directory/"events"):
            A.C.ordinary(directory, directory=True, fresh=True).mkdir()
        copied_bytes, metadata_bytes = 0, 0

        def copy_file(source_pin, relative, maximum):
            nonlocal copied_bytes
            self._grant_live(grant, check)
            fields(source_pin, ("path", "bytes", "sha256"), "ANCHOR_COPY_PIN")
            pin = {key: source_pin[key] for key in ("bytes", "sha256")}
            source = _verify(Path(source_pin["path"]), pin, maximum, check)
            need(not source.is_relative_to(self.root), "ANCHOR_EXTERNAL_GENERATION_REQUIRED")
            destination = self.root.joinpath(*relative.split("/"))
            A.C.ordinary(destination, fresh=True)
            actual, digest = 0, hashlib.sha256()
            with source.open("rb") as inp, destination.open("xb") as out:
                while block := inp.read(MIB):
                    self._grant_live(grant, check)
                    actual += len(block); copied_bytes += len(block)
                    need(actual <= pin["bytes"] and copied_bytes <= LIMITS["max_operation_bytes"],
                         "ANCHOR_COPY_BOUND")
                    out.write(block); digest.update(block)
                out.flush(); os.fsync(out.fileno())
            need(actual == pin["bytes"] and digest.hexdigest() == pin["sha256"], "ANCHOR_COPY_CHANGED")
            _verify(destination, pin, maximum, check)
            return dict(pin, path=relative)

        text = module_text(request["module_name"])
        parts = []
        for pin, suffix in zip(value["artifact_parts"], PART_SUFFIXES):
            need(Path(pin["path"]).name == text+suffix, "ANCHOR_GENERATED_PART_NAME")
            parts.append(copy_file(pin, f"operations/{grant.identifier}/modules/{text}{suffix}",
                                   LIMITS["max_module_bytes"]))
        need(sum(part["bytes"] for part in parts) <= LIMITS["max_module_bytes"], "ANCHOR_MODULE_BYTE_BOUND")
        event_pins = {}
        for name in EVENT_NAMES:
            pin = events[name]
            if name in ("request.json", "inventory.json", "anchor-plan.json"):
                role = {"request.json": "request", "inventory.json": "inventory", "anchor-plan.json": "anchor_plan"}[name]
                need({key: pin[key] for key in ("bytes", "sha256")} == selected[role], "ANCHOR_EVENT_INPUT_PIN")
            if name == "native-report.json":
                report_raw = A.C.read_bounded(Path(pin["path"]), 8*MIB)
                need(A._writer_json(report_raw, 8*MIB) == report, "ANCHOR_EVENT_REPORT_PIN")
            event_pins[name] = copy_file(pin, f"operations/{grant.identifier}/events/{name}", 8*MIB)
            metadata_bytes += pin["bytes"]
            need(metadata_bytes <= LIMITS["max_metadata_bytes"], "ANCHOR_METADATA_BOUND")
        context = self.owner.catalog.context(selected["source_context_root"])
        all_names = dict(names)
        parent_unit_count = parent_record_bytes = parent_artifact_bytes = 0
        if grant.parent is not None:
            need(self.load(parent_id, context, check) == grant.parent, "ANCHOR_PARENT_CHANGED")
            parent_names = {key for _, outputs in grant.parent.frontier.units for key, _ in outputs}
            parent_units = {identity for identity, _ in grant.parent.frontier.units}
            need(not parent_names.intersection(names) and not parent_units.intersection(
                 row["unit_id"] for row in units), "ANCHOR_DELTA_PARENT_COLLISION")
            parent_unit_count = len(parent_units)
            parent_record_bytes = sum(map(len, grant.parent.records))
            parent_artifact_bytes = grant.parent.artifact_bytes
            all_names.update({key: (identity, unit) for unit, outputs in grant.parent.frontier.units
                              for key, identity in outputs})
        need(parent_unit_count+len(units) <= LIMITS["max_units"] and
             len(all_names) <= LIMITS["max_names"] and
             parent_artifact_bytes+sum(part["bytes"] for part in parts) <= LIMITS["max_artifact_bytes"],
             "ANCHOR_COMMIT_CHAIN_BOUND")
        for name, (identity, _) in names.items():
            need(context["bindings"].get(name) == identity, "ANCHOR_CURRENT_CONTEXT_MISMATCH")
        for target in selected["targets"]:
            need(all_names.get(A.E.name_key(target["name"])) == (target["export_id"], target["unit_id"]),
                 "ANCHOR_TARGET_REALIZATION")
        record = {"schema": RECORD_SCHEMA, "store_binding": self.store_binding, "support_id": self.support_id,
            "operation_id": grant.identifier, "source_context_root": selected["source_context_root"],
            "parent_anchor_id": parent_id, "module_name": request["module_name"],
            "direct_imports": [module_name(grant.parent.module_name) if grant.parent is not None
                               else [[0, {"$bytes": list(b"Init")}]]],
            "targets": selected["targets"], "materialization_key": selected["materialization_key"],
            "artifact_parts": parts, "units": units, "added_names": added,
            "matched_names": matched_names, "event_files": event_pins}
        raw = canonical(record)
        need(len(raw) <= LIMITS["max_record_bytes"] and
             parent_record_bytes+len(raw) <= LIMITS["max_records_bytes"] and
             metadata_bytes+len(raw)+len(grant.selection_raw)+8192 <= LIMITS["max_metadata_bytes"],
             "ANCHOR_RECORD_BOUND")
        identity = A.sha(RECORD_DOMAIN+raw)
        self._record(raw, identity)
        prospective = parse(self.plan(grant.parent), LIMITS["max_plan_bytes"])
        prospective["anchor_id"] = identity
        prospective["modules"].append({"anchor_id": identity, "module_name": record["module_name"],
            "direct_imports": record["direct_imports"], "added_names": record["added_names"],
            "artifact_parts": [{**part, "path": str(self.root.joinpath(*part["path"].split("/")))}
                               for part in parts]})
        prospective["bindings"].extend(units)
        need(len(canonical(prospective)) <= LIMITS["max_plan_bytes"], "ANCHOR_PLAN_BOUND")
        # Record cleanup before commit. A crash before this marker leaves an
        # explicitly unresolved reservation; no saved PASS can recover authority.
        self._close_operation(grant, "LIVE_GENERATION_CLEAN_BEFORE_COMMIT")
        total, _ = self._census(check, allow_pending=grant)
        need(total+2*len(raw) <= LIMITS["max_store_bytes"], "ANCHOR_COMMIT_CAPACITY")
        staging = grant.directory/"record.staged.json"
        A.P.PortableCatalog._write_fresh(staging, raw)
        self._grant_live(grant, check)
        destination = A.C.ordinary(self.root/"records"/(identity+".json"), fresh=True)
        # Windows same-volume rename is non-overwriting; refuse other OS rather
        # than silently replacing a record under POSIX rename semantics.
        need(os.name == "nt", "ANCHOR_WINDOWS_COMMIT_REQUIRED")
        self._commit_attempted = True
        try:
            os.rename(staging, destination)
            need(A.C.read_bounded(destination, LIMITS["max_record_bytes"]) == raw, "ANCHOR_COMMIT_READBACK")
        except BaseException as error:
            self._denied = True
            raise AnchorCommitUnknown(identity) from error
        self._grant = None
        # Publication has already committed. Failure here must never delete or
        # revoke it; explicit later exact-ID lookup can validate retained state.
        try:
            return self.load(identity, context, check)
        except BaseException as error:
            raise AnchorCommittedError(identity) from error


def open_for_owner(owner, selected_support, check):
    """Create only a genuinely missing sidecar; never adopt a preexisting tree."""
    need(type(owner) is A.OrdinaryAdmission and type(owner.catalog) is A.P.PortableCatalog and
         callable(check), "ANCHOR_OWNER_CONFIGURATION")
    check()
    owner.catalog._active()
    need(owner.catalog._lock is not None and not owner.catalog._lock.closed, "ANCHOR_OWNER_LOCK")
    support = parse(selected_support, MIB)
    fields(support, ("schema", "installation_manifest_sha256", "semantic_id", "foundation_id",
        "implementation_id", "policy", "sources", "native_helpers"), "ANCHOR_SUPPORT_FIELDS")
    installation = owner.installation
    need(support["schema"] == SUPPORT_SCHEMA and
         support["installation_manifest_sha256"] == installation.manifest_sha256 and
         support["semantic_id"] == installation.semantic_id and support["foundation_id"] == A.S.foundation_id() and
         support["implementation_id"] == installation.implementation_id and
         type(support["policy"]) is str and 0 < len(support["policy"]) <= 256,
         "ANCHOR_SELECTED_SUPPORT")
    need(type(support["sources"]) is dict and 1 <= len(support["sources"]) <= 64,
         "ANCHOR_SUPPORT_SOURCES")
    for role, pin in support["sources"].items():
        need(type(role) is str and 0 < len(role) <= 128, "ANCHOR_SUPPORT_ROLE")
        _pin(pin, 2*MIB)
    helpers = support["native_helpers"]
    need(type(helpers) is list and 1 <= len(helpers) <= 64, "ANCHOR_HELPER_BOUND")
    helper_names = []
    for item in helpers:
        need(type(item) is list and len(item) == 3, "ANCHOR_HELPER_PIN")
        name, size, digest = item
        need(type(name) is str and 0 < len(name) <= 256, "ANCHOR_HELPER_NAME")
        _pin({"bytes": size, "sha256": digest}, 128*MIB)
        helper_names.append(name)
    need(helper_names == sorted(set(helper_names)), "ANCHOR_HELPER_ORDER")
    self = Store()
    self.owner, self.catalog_root = owner, owner.catalog._root
    self.adoption_raw, self.activation_raw = owner.catalog._marker, owner.catalog._activation_raw
    self.semantic_id, self.foundation_id = installation.semantic_id, A.S.foundation_id()
    self.implementation_id = installation.implementation_id
    self.support_id = A.sha(SUPPORT_DOMAIN+selected_support)
    self.root = self.catalog_root/"module-anchors-v1"
    self._grant, self._commit_attempted, self._denied = None, False, False
    inventory_raw = installation.read("inventory", MIB)
    need(A.sha(inventory_raw) == A.S.INVENTORY, "ANCHOR_FIXED_INVENTORY")
    self.basis_names = frozenset(A.E.name_key(row[0]) for row in json.loads(inventory_raw))
    self.marker_raw = canonical({"schema": STORE_SCHEMA, "store_id": owner.catalog._store_id,
        "adoption_sha256": A.sha(self.adoption_raw), "activation_sha256": A.sha(self.activation_raw),
        "semantic_id": self.semantic_id, "foundation_id": self.foundation_id,
        "implementation_id": self.implementation_id, "limits": LIMITS})
    self.store_binding = A.sha(self.marker_raw)
    if not os.path.lexists(self.root):
        self._owner_live()
        A.C.ordinary(self.root, directory=True, fresh=True).mkdir()
        (self.root/"operations").mkdir()
        (self.root/"records").mkdir()
        A.P.PortableCatalog._write_fresh(self.root/"STORE.json", self.marker_raw)
    else:
        A.C.ordinary(self.root, directory=True)
        need(A.C.read_bounded(self.root/"STORE.json", 65536) == self.marker_raw,
             "ANCHOR_STORE_MARKER")
    A.C.ordinary(self.root/"operations", directory=True)
    A.C.ordinary(self.root/"records", directory=True)
    self._census(check)
    return self


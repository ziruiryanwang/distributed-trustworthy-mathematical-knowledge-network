"""Body-free metadata of an already protected live reference.

This parser creates no authority. Its caller authenticates the protected record,
support and exact file hashes before calling, and holds the real owner lock.
It deliberately cannot replace reference_report.bind_report for a live match:
singleton witnesses, full signatures and dependency closure were checked there.
No synthetic ReferenceRequest and no old proof-body request is constructed.
"""
from __future__ import annotations

from dataclasses import dataclass
import ordinary_admission as A

MIB = 1024**2
MAX_REPORT = MAX_WARRANTS = 32*MIB
SCHEMA = "DMKN_ORDINARY_REFERENCE_BASE_REPORT_V2"
WARRANT_SCHEMA = "DMKN_LOCAL_REFERENCE_WARRANTS_V1"
IDENTITIES = ("semantic_id", "foundation_id", "context_root", "snapshot_id", "support_id")
COUNTERS = ("private_unit_count", "private_name_count", "public_unit_count", "public_name_count",
    "unit_array_bytes", "encoded_nodes", "private_scan_nodes", "public_scan_nodes",
    "private_edges", "public_edges", "basis_scan_nodes", "basis_edges", "basis_pruning_rounds")
FIELDS = {"schema", "assurance", *IDENTITIES, *COUNTERS, "targets", "private_unit_ids",
    "public_units", "private_module_names", "public_module_names", "checked_units", "added_names",
    "public_basis", "usable_basis_names"}
ABSTRACT = {1: "abstract_singleton_definition", 2: "erased_singleton_theorem",
            3: "abstract_singleton_opaque"}


def fields(value, expected, code):
    A.need(type(value) is dict and set(value) == set(expected), code)


def uint(value, maximum, code):
    A.need(type(value) is int and 0 <= value <= maximum, code)
    return value


def _raw(raw, expected, maximum, code):
    A.C.hexid(expected)
    A.need(type(raw) is bytes and 0 < len(raw) <= maximum and A.sha(raw) == expected, code)


def basis_inventory(raw):
    _raw(raw, A.S.INVENTORY, MIB, "PROTECTED_REFERENCE_INVENTORY")
    rows = A.E._array(A._writer_json(raw, MIB), 581)
    keys = []
    for row in rows:
        A.E._array(row, 5)
        keys.append(A.E.name_key(row[0]))
    A.need(len(set(keys)) == 581, "PROTECTED_REFERENCE_BASIS_CENSUS")
    return rows


def read_warrants(raw, expected_sha256, *, semantic_id, foundation_id, current_context, check):
    """Check exact protected bindings against a current owner-validated context."""
    check()
    _raw(raw, expected_sha256, MAX_WARRANTS, "PROTECTED_REFERENCE_WARRANT_BYTES")
    doc = A.E.strict_json(raw, A.E.Limits(max_bytes=MAX_WARRANTS))
    fields(doc, ("schema", "semantic_id", "foundation_id", "bindings"), "PROTECTED_REFERENCE_WARRANT_FIELDS")
    A.need(doc["schema"] == WARRANT_SCHEMA and doc["semantic_id"] == semantic_id == A.S.semantic_id()
           and doc["foundation_id"] == foundation_id == A.S.foundation_id(),
           "PROTECTED_REFERENCE_WARRANT_POLICY")
    A.need(type(current_context) is dict and current_context.get("semantic_id") == semantic_id
           and current_context.get("foundation_id") == foundation_id
           and type(current_context.get("bindings")) is dict, "PROTECTED_REFERENCE_CURRENT_CONTEXT")
    result, previous = [], None
    for row in A.E._array(doc["bindings"], maximum=262144+581):
        check()
        fields(row, ("name", "symbol_id"), "PROTECTED_REFERENCE_WARRANT_ROW")
        key, symbol = A.E.name_key(row["name"]), A.C.hexid(row["symbol_id"])
        A.need((previous is None or key > previous) and current_context["bindings"].get(key) == symbol,
               "PROTECTED_REFERENCE_CURRENT_WARRANT")
        result.append((key, symbol)); previous = key
    A.need(len(result) > 581, "PROTECTED_REFERENCE_WARRANT_CENSUS")
    check()
    return tuple(result)


@dataclass(frozen=True)
class ProtectedMetadata:
    public_frontier: tuple[tuple[str, tuple[tuple[bytes, str], ...]], ...]
    public_bindings: tuple[tuple[bytes, str, str, int, tuple[bytes, ...], str, str], ...]
    basis_bindings: tuple[tuple[bytes, int, tuple[bytes, ...], str, str], ...]
    usable_basis_keys: tuple[bytes, ...]
    private_module_keys: tuple[bytes, ...]
    public_module_keys: tuple[bytes, ...]
    private_unit_ids: tuple[str, ...]


def read_metadata(raw, expected_sha256, *, identities, targets, inventory_raw,
                  warrant_bindings, snapshot, check):
    """Reopen protected metadata, not a peer report or a correspondence proof."""
    check()
    _raw(raw, expected_sha256, MAX_REPORT, "PROTECTED_REFERENCE_REPORT_BYTES")
    fields(identities, IDENTITIES, "PROTECTED_REFERENCE_IDENTITIES")
    report = A._writer_json(raw, MAX_REPORT)
    fields(report, FIELDS, "PROTECTED_REFERENCE_REPORT_FIELDS")
    A.need(report["schema"] == SCHEMA and
           report["assurance"] == "CORRESPONDENCE_REQUIRES_CURRENT_PROTECTED_WARRANTS",
           "PROTECTED_REFERENCE_REPORT_SCHEMA")
    for key in IDENTITIES:
        A.C.hexid(identities[key])
        A.need(report[key] == identities[key], "PROTECTED_REFERENCE_IDENTITY:"+key)
    A.need(type(report["checked_units"]) is int and report["checked_units"] == 0
           and report["added_names"] == [], "PROTECTED_REFERENCE_NOT_NEW_ACCEPTANCE")
    warrants = dict(warrant_bindings)
    A.need(len(warrants) == len(warrant_bindings), "PROTECTED_REFERENCE_WARRANT_DUPLICATE")
    inventory = basis_inventory(inventory_raw)
    basis, common = [], set()
    for row, original in zip(A.E._array(report["public_basis"], 581), inventory):
        check()
        fields(row, ("name", "kind", "level_params", "projection", "kernel_projection"),
               "PROTECTED_REFERENCE_BASIS_FIELDS")
        key = A.E.name_key(row["name"])
        A.need(row["name"] == original[0] and type(row["kind"]) is int and row["kind"] == original[1]
               and warrants.get(key) == A.S.basis_symbol_id(identities["semantic_id"],
                   identities["foundation_id"], row["name"]), "PROTECTED_REFERENCE_BASIS_IDENTITY")
        params = A.E._names(row["level_params"], A.E.DEFAULT_LIMITS.max_params,
                            A.E.DEFAULT_LIMITS, params=True)
        A.need(len(params) == original[2], "PROTECTED_REFERENCE_BASIS_PARAMETERS")
        for field in ("projection", "kernel_projection"):
            A.need(row[field] in ("full", "absent", ABSTRACT.get(row["kind"])) and
                   type(row[field]) is str, "PROTECTED_REFERENCE_BASIS_PROJECTION")
        if "absent" not in (row["projection"], row["kernel_projection"]):
            common.add(key)
        basis.append((key, row["kind"], tuple(params), row["projection"], row["kernel_projection"]))
    order = {row[0]: index for index, row in enumerate(basis)}
    usable, previous = [], -1
    for name in A.E._array(report["usable_basis_names"], maximum=581):
        check()
        key = A.E.name_key(name)
        A.need(key in common and order[key] > previous, "PROTECTED_REFERENCE_USABLE_BASIS")
        usable.append(key); previous = order[key]
    removed = len(common)-len(usable)
    rounds = uint(report["basis_pruning_rounds"], 581, "PROTECTED_REFERENCE_PRUNING_ROUNDS")
    A.need((rounds == 0) == (removed == 0) and rounds <= removed, "PROTECTED_REFERENCE_PRUNING_ROUNDS")
    private = tuple(A.C.hexid(value) for value in A.E._array(report["private_unit_ids"], maximum=8192))
    A.need(bool(private) and len(set(private)) == len(private), "PROTECTED_REFERENCE_PRIVATE_CENSUS")
    private_order = {identity: index for index, identity in enumerate(private)}
    frontier, bindings, names, previous = [], [], set(), -1
    for unit in A.E._array(report["public_units"], maximum=len(private)):
        check()
        fields(unit, ("unit_id", "outputs"), "PROTECTED_REFERENCE_PUBLIC_UNIT")
        identity = A.C.hexid(unit["unit_id"])
        A.need(identity in private_order and private_order[identity] > previous,
               "PROTECTED_REFERENCE_PUBLIC_ORDER")
        previous = private_order[identity]
        outputs = []
        for row in A.E._array(unit["outputs"], maximum=262144):
            check()
            fields(row, ("name", "export_id", "kind", "level_params", "projection", "kernel_projection"),
                   "PROTECTED_REFERENCE_PUBLIC_FIELDS")
            key, symbol = A.E.name_key(row["name"]), A.C.hexid(row["export_id"])
            A.need(key not in order and key not in names and len(names) < 262144 and
                   symbol == A.S.export_id(identities["semantic_id"], identity, row["name"])
                   and warrants.get(key) == symbol, "PROTECTED_REFERENCE_PUBLIC_WARRANT")
            A.need(type(row["kind"]) is int and 1 <= row["kind"] <= 6, "PROTECTED_REFERENCE_PUBLIC_KIND")
            params = A.E._names(row["level_params"], A.E.DEFAULT_LIMITS.max_params,
                                A.E.DEFAULT_LIMITS, params=True)
            for field in ("projection", "kernel_projection"):
                A.need(type(row[field]) is str and row[field] in ("full", ABSTRACT.get(row["kind"])),
                       "PROTECTED_REFERENCE_PUBLIC_PROJECTION")
            names.add(key); outputs.append((key, symbol))
            bindings.append((key, symbol, identity, row["kind"], tuple(params),
                             row["projection"], row["kernel_projection"]))
        A.need(bool(outputs), "PROTECTED_REFERENCE_EMPTY_UNIT")
        frontier.append((identity, tuple(outputs)))
    A.need(bool(frontier), "PROTECTED_REFERENCE_PUBLIC_EMPTY")
    target_lookup = {key: (symbol, identity) for key, symbol, identity, *_ in bindings}
    expected_targets, target_keys = [], set()
    for target in A.E._array(targets, maximum=1024):
        check()
        fields(target, ("name", "export_id", "unit_id"), "PROTECTED_REFERENCE_TARGET_FIELDS")
        key = A.E.name_key(target["name"])
        A.need(key not in target_keys and target_lookup.get(key) == (target["export_id"], target["unit_id"]),
               "PROTECTED_REFERENCE_TARGET_NOT_PUBLIC")
        target_keys.add(key)
        expected_targets.append({"name": target["name"], "export_id": target["export_id"]})
    A.need(bool(expected_targets) and report["targets"] == expected_targets, "PROTECTED_REFERENCE_TARGETS")

    def modules(field):
        result = tuple(A.E.name_key(name) for name in A.E._array(report[field], maximum=4096))
        A.need(bool(result) and len(set(result)) == len(result), "PROTECTED_REFERENCE_MODULE_CENSUS")
        return result

    private_modules, public_modules = modules("private_module_names"), modules("public_module_names")
    roots = A.E.strict_json(snapshot.root_imports_raw)
    root_keys = {A.E.name_key(row["module"]) for row in roots}
    A.need(set(private_modules) == set(snapshot.module_keys) and
           root_keys <= set(public_modules) <= set(private_modules), "PROTECTED_REFERENCE_MODULE_MEMBERSHIP")
    for key in COUNTERS:
        uint(report[key], 2**64-1, "PROTECTED_REFERENCE_COUNTER:"+key)
    A.need(report["private_unit_count"] == len(private) and
           report["private_name_count"] == len(warrants)-581 and
           report["public_unit_count"] == len(frontier) and report["public_name_count"] == len(bindings)
           and report["encoded_nodes"] <= 20000000 and report["unit_array_bytes"] <= 64*MIB and
           report["private_scan_nodes"]+report["public_scan_nodes"]+report["basis_scan_nodes"] <= 20000000
           and report["private_edges"]+report["public_edges"]+report["basis_edges"] <= 262144,
           "PROTECTED_REFERENCE_COUNTER_CENSUS")
    check()
    return ProtectedMetadata(tuple(frontier), tuple(bindings), tuple(basis), tuple(usable),
                             private_modules, public_modules, private)

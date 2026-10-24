"""Bind V2 live correspondence metadata; never confer mathematical authority.

The matcher, not this shape parser, establishes signature equality, the original
singleton property, and the greatest dependency-closed public basis. The caller
must bind that actual clean native event to current protected warrants. Saved
reports and Python objects are not transferable certificates or registrations.
"""
from __future__ import annotations

from dataclasses import dataclass

import ordinary_admission as A
import reference_request as Q
import baseline_snapshot as S

MIB = 1024**2
MAX_REPORT = 32*MIB
SCHEMA = "DMKN_ORDINARY_REFERENCE_BASE_REPORT_V2"
IDENTITIES = ("semantic_id", "foundation_id", "context_root", "snapshot_id", "support_id")
COUNTERS = ("private_unit_count", "private_name_count", "public_unit_count", "public_name_count",
            "unit_array_bytes", "encoded_nodes", "private_scan_nodes", "public_scan_nodes",
            "private_edges", "public_edges", "basis_scan_nodes", "basis_edges", "basis_pruning_rounds")
FIELDS = {"schema", "assurance", *IDENTITIES, "targets", "private_unit_ids", "public_units",
          "private_module_names", "public_module_names", *COUNTERS, "checked_units", "added_names",
          "public_basis", "usable_basis_names"}
ABSTRACT = {1: "abstract_singleton_definition", 2: "erased_singleton_theorem",
            3: "abstract_singleton_opaque"}


@dataclass(frozen=True)
class BoundReferenceReport:
    """Request-bound metadata, not a certificate or a protected registration."""
    raw: bytes
    sha256: str
    public_unit_ids: tuple[str, ...]
    public_bindings: tuple[tuple[bytes, str, str, str, str], ...]
    private_module_keys: tuple[bytes, ...]
    public_module_keys: tuple[bytes, ...]
    basis_bindings: tuple[tuple[bytes, int, tuple[bytes, ...], str, str], ...]
    usable_basis_keys: tuple[bytes, ...]


def _fields(value, keys, code):
    A.need(type(value) is dict and set(value) == set(keys), code)


def _uint(value, low, high, code):
    A.need(type(value) is int and low <= value <= high, code)
    return value


def _singleton_kind(unit):
    """Require the full ordinary descriptor/inventory singleton relation."""
    descriptor, rows = unit[1], unit[2]
    if type(descriptor) is not list or not descriptor or len(rows) != 1:
        return None
    tag = descriptor[0]
    if type(tag) is not int or tag not in (0, 1, 2) or len(descriptor) != (7 if tag == 0 else 6):
        return None
    own, params, ty, body = descriptor[1:5]
    if descriptor[-1] != [own]:
        return None
    details = ([body, descriptor[5], [own]] if tag == 0 else
               [body, [own]] if tag == 1 else [body, 0, [own]])
    return tag+1 if rows[0] == [own, tag+1, params, ty, details] else None


def _projection(value, kind, *, abstract, absent=False, code="REFERENCE_REPORT_PROJECTION"):
    A.need(type(value) is str and (value == "full" or (absent and value == "absent") or
           (abstract and kind in ABSTRACT and value == ABSTRACT[kind])), code)


def _basis(report, request, check):
    raw = request.inventory_raw
    A.need(type(raw) is bytes and 0 < len(raw) <= MIB and A.sha(raw) == A.S.INVENTORY,
           "REFERENCE_REPORT_FIXED_INVENTORY")
    inventory = A.E._array(A._writer_json(raw, MIB), 581)
    rows = A.E._array(report["public_basis"], len(inventory))
    bindings, common = [], set()
    for row, original in zip(rows, inventory):
        check()
        A.E._array(original, 5)
        _fields(row, {"name", "kind", "level_params", "projection", "kernel_projection"},
                "REFERENCE_REPORT_BASIS_FIELDS")
        A.need(row["name"] == original[0] and type(row["kind"]) is int and row["kind"] == original[1],
               "REFERENCE_REPORT_BASIS_IDENTITY")
        key = A.E.name_key(row["name"])
        # The fixed legacy inventory stores a universe COUNT, not names. Ordered
        # name/signature equality is a live matcher obligation, not inferred here.
        params = A.E._names(row["level_params"], A.E.DEFAULT_LIMITS.max_params,
                            A.E.DEFAULT_LIMITS, params=True)
        A.need(len(params) == original[2], "REFERENCE_REPORT_BASIS_PARAMETERS")
        for field in ("projection", "kernel_projection"):
            _projection(row[field], row["kind"], abstract=True, absent=True,
                        code="REFERENCE_REPORT_BASIS_PROJECTION")
        if row["projection"] != "absent" and row["kernel_projection"] != "absent":
            common.add(key)
        bindings.append((key, row["kind"], tuple(params), row["projection"], row["kernel_projection"]))
    order = {binding[0]: index for index, binding in enumerate(bindings)}
    A.need(len(order) == len(inventory), "REFERENCE_REPORT_BASIS_CENSUS")
    usable, previous = [], -1
    for name in A.E._array(report["usable_basis_names"], maximum=len(inventory)):
        check()
        key = A.E.name_key(name)
        A.need(key in common and order[key] > previous, "REFERENCE_REPORT_USABLE_BASIS")
        previous = order[key]
        usable.append(key)
    # Deletion rounds are nonempty. Maximality and graph closure belong to the
    # live native computation; this parser intentionally does not replay it.
    rounds = _uint(report["basis_pruning_rounds"], 0, len(inventory), "REFERENCE_REPORT_BASIS_ROUNDS")
    removed = len(common)-len(usable)
    A.need((rounds == 0) == (removed == 0) and rounds <= removed,
           "REFERENCE_REPORT_BASIS_ROUNDS")
    return tuple(bindings), tuple(usable)


def bind_report(raw, expected_sha256, *, request, replay_request_raw, check_budget):
    """Check exact request membership without launching or authorizing native work."""
    A.need(Q.A is A and S.A is A and type(request) is Q.ReferenceRequest and
           callable(check_budget), "REFERENCE_REPORT_CONFIGURATION")
    check = check_budget
    check()
    A.C.hexid(expected_sha256)
    A.need(type(raw) is bytes and 0 < len(raw) <= MAX_REPORT and A.sha(raw) == expected_sha256,
           "REFERENCE_REPORT_EXACT_BYTES")
    A.need(type(request.raw) is bytes and 0 < len(request.raw) <= Q.MAX_REQUEST and
           A.sha(request.raw) == request.sha256, "REFERENCE_REPORT_REQUEST_PIN")
    selected = A.E.strict_json(request.raw, A.E.Limits(max_bytes=Q.MAX_REQUEST))
    _fields(selected, {"schema", *IDENTITIES, "units", "targets"}, "REFERENCE_REPORT_REQUEST_FIELDS")
    A.need(selected["schema"] == Q.SCHEMA, "REFERENCE_REPORT_REQUEST_SCHEMA")
    report = A._writer_json(raw, MAX_REPORT)
    _fields(report, FIELDS, "REFERENCE_REPORT_FIELDS")
    A.need(report["schema"] == SCHEMA and
           report["assurance"] == "CORRESPONDENCE_REQUIRES_CURRENT_PROTECTED_WARRANTS",
           "REFERENCE_REPORT_SCHEMA")
    for key in IDENTITIES:
        A.C.hexid(selected[key])
        A.need(report[key] == selected[key], "REFERENCE_REPORT_IDENTITY:"+key)
    A.need(type(report["checked_units"]) is int and report["checked_units"] == 0 and
           report["added_names"] == [], "REFERENCE_REPORT_NOT_NEW_ACCEPTANCE")
    A.need(report["targets"] == selected["targets"], "REFERENCE_REPORT_TARGETS")

    units = A.E._array(selected["units"], maximum=8192)
    A.need(bool(units), "REFERENCE_REPORT_EMPTY_PRIVATE")
    by_id, ordered, expected_bindings = {}, [], []
    name_count = 0
    for entry in units:
        check()
        _fields(entry, {"unit_id", "unit", "outputs"}, "REFERENCE_REPORT_PRIVATE_FIELDS")
        identity = entry["unit_id"]
        A.C.hexid(identity)
        A.need(identity not in by_id, "REFERENCE_REPORT_PRIVATE_DUPLICATE")
        unit = A.E._array(entry["unit"], 3)
        rows = A.E._array(unit[2], maximum=262144)
        outputs = A.E._array(entry["outputs"], len(rows))
        A.need(bool(rows), "REFERENCE_REPORT_PRIVATE_OUTPUTS_EMPTY")
        for row, output in zip(rows, outputs):
            check()
            A.E._array(row, 5)
            _fields(output, {"name", "export_id"}, "REFERENCE_REPORT_OUTPUT_FIELDS")
            key = A.E.name_key(row[0])
            A.C.hexid(output["export_id"])
            A.need(output["name"] == row[0], "REFERENCE_REPORT_PRIVATE_OUTPUT_NAME")
            expected_bindings.append((key, output["export_id"], identity))
        by_id[identity] = (len(ordered), entry)
        ordered.append(identity)
        name_count += len(rows)
        A.need(name_count <= 262144, "REFERENCE_REPORT_PRIVATE_NAME_BOUND")
    A.need(tuple(ordered) == request.unit_ids and report["private_unit_ids"] == ordered and
           tuple(sorted(expected_bindings)) == request.output_bindings and
           len({row[0] for row in expected_bindings}) == name_count,
           "REFERENCE_REPORT_PRIVATE_CENSUS")

    basis_bindings, usable_basis = _basis(report, request, check)
    public_rows = A.E._array(report["public_units"], maximum=len(units))
    A.need(bool(public_rows), "REFERENCE_REPORT_PUBLIC_EMPTY")
    previous = -1
    public_ids, public_bindings = [], []
    for public in public_rows:
        check()
        _fields(public, {"unit_id", "outputs"}, "REFERENCE_REPORT_PUBLIC_FIELDS")
        identity = public["unit_id"]
        A.C.hexid(identity)
        A.need(identity in by_id, "REFERENCE_REPORT_PUBLIC_UNKNOWN")
        index, entry = by_id[identity]
        A.need(index > previous, "REFERENCE_REPORT_PUBLIC_ORDER")
        previous = index
        outputs = A.E._array(public["outputs"], len(entry["outputs"]))
        singleton = _singleton_kind(entry["unit"])
        for output, binding, expected in zip(outputs, entry["outputs"], entry["unit"][2]):
            check()
            _fields(output, {"name", "export_id", "kind", "level_params", "projection",
                             "kernel_projection"}, "REFERENCE_REPORT_PUBLIC_OUTPUT_FIELDS")
            A.need(output["name"] == binding["name"] and output["export_id"] == binding["export_id"] and
                   type(output["kind"]) is int and output["kind"] == expected[1] and
                   output["level_params"] == expected[2], "REFERENCE_REPORT_PUBLIC_OUTPUT_IDENTITY")
            for field in ("projection", "kernel_projection"):
                _projection(output[field], expected[1], abstract=singleton == expected[1])
            public_bindings.append((A.E.name_key(binding["name"]), binding["export_id"], identity,
                                    output["projection"], output["kernel_projection"]))
        public_ids.append(identity)
    public_lookup = {key: symbol for key, symbol, *_ in public_bindings}
    for target in selected["targets"]:
        check()
        A.need(public_lookup.get(A.E.name_key(target["name"])) == target["export_id"],
               "REFERENCE_REPORT_TARGET_NOT_PUBLIC")

    A.need(type(replay_request_raw) is bytes and 0 < len(replay_request_raw) <= S.MAX_REQUEST,
           "REFERENCE_REPORT_REPLAY_BOUND")
    replay = A.E.strict_json(replay_request_raw, A.E.Limits(max_bytes=S.MAX_REQUEST))
    _fields(replay, {"schema", "mode", "modules", "artifacts"}, "REFERENCE_REPORT_REPLAY_FIELDS")
    A.need(replay["schema"] == S.REQUEST_SCHEMA and replay["mode"] == "replay",
           "REFERENCE_REPORT_REPLAY_SCHEMA")
    artifacts = A.E._array(replay["artifacts"], maximum=S.MAX_MODULES)
    selected_modules = [S._module(row["module"])[0] for row in artifacts]
    A.need(bool(selected_modules) and len(set(selected_modules)) == len(selected_modules),
           "REFERENCE_REPORT_REPLAY_MODULES")

    def module_keys(key):
        result = []
        for name in A.E._array(report[key], maximum=S.MAX_MODULES):
            check()
            result.append(S._module(name)[0])
        A.need(bool(result) and len(set(result)) == len(result), "REFERENCE_REPORT_MODULE_CENSUS")
        return tuple(result)

    private_modules, public_modules = module_keys("private_module_names"), module_keys("public_module_names")
    roots = {S._module(name)[0] for name in A.E._array(replay["modules"], maximum=16)}
    A.need(bool(roots) and set(private_modules) == set(selected_modules) and
           roots <= set(public_modules) <= set(private_modules), "REFERENCE_REPORT_MODULE_MEMBERSHIP")
    for key in COUNTERS:
        _uint(report[key], 0, 2**64-1, "REFERENCE_REPORT_COUNTER:"+key)
    A.need(report["private_unit_count"] == len(units) and report["private_name_count"] == name_count and
           report["public_unit_count"] == len(public_ids) and
           report["public_name_count"] == len(public_bindings) and
           report["encoded_nodes"] == request.nodes <= 20000000 and
           report["private_scan_nodes"] + report["basis_scan_nodes"] + report["public_scan_nodes"] <= 20000000 and
           report["private_edges"] + report["basis_edges"] + report["public_edges"] <= 262144,
           "REFERENCE_REPORT_COUNTER_CENSUS")
    unit_bytes = 2 + len(units)-1
    for entry in units:
        check()
        unit_bytes += len(A.E.canonical_json(entry["unit"]))
    A.need(report["unit_array_bytes"] == unit_bytes <= Q.MAX_UNIT_ARRAY, "REFERENCE_REPORT_UNIT_BYTES")
    check()
    return BoundReferenceReport(raw, expected_sha256, tuple(public_ids), tuple(public_bindings),
                                private_modules, public_modules, basis_bindings, usable_basis)

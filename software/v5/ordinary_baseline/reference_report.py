"""Bind live native correspondence metadata to its selected inputs.

This parser establishes response shape and exact request membership only. It
does not prove correspondence, authenticate artifacts or confer a local warrant.
The calling controller must retain current owner authority and the actual clean
native event. A saved response cannot be used to register a reference.
"""
from __future__ import annotations

from dataclasses import dataclass

import ordinary_admission as A
import reference_request as Q
import baseline_snapshot as S

MIB = 1024**2
MAX_REPORT = 32*MIB
SCHEMA = "DMKN_ORDINARY_REFERENCE_BASE_REPORT_V1"
IDENTITIES = ("semantic_id", "foundation_id", "context_root", "snapshot_id", "support_id")
COUNTERS = ("private_unit_count", "private_name_count", "public_unit_count", "public_name_count",
            "unit_array_bytes", "encoded_nodes", "private_scan_nodes", "public_scan_nodes",
            "private_edges", "public_edges")
FIELDS = {"schema", "assurance", *IDENTITIES, "targets", "private_unit_ids", "public_units",
          "private_module_names", "public_module_names", *COUNTERS, "checked_units", "added_names"}


@dataclass(frozen=True)
class BoundReferenceReport:
    """Request-bound metadata, not a transferable certificate or registration."""
    raw: bytes
    sha256: str
    public_unit_ids: tuple[str, ...]
    public_bindings: tuple[tuple[bytes, str, str, str, str], ...]
    private_module_keys: tuple[bytes, ...]
    public_module_keys: tuple[bytes, ...]


def _fields(value, keys, code):
    A.need(type(value) is dict and set(value) == set(keys), code)


def _uint(value, low, high, code):
    A.need(type(value) is int and low <= value <= high, code)
    return value


def _singleton_theorem(unit):
    descriptor, rows = unit[1], unit[2]
    return (type(descriptor) is list and len(descriptor) == 6 and descriptor[0] == 1 and
            len(rows) == 1 and descriptor[5] == [descriptor[1]] and
            rows[0] == [descriptor[1], 2, descriptor[2], descriptor[3],
                        [descriptor[4], descriptor[5]]])


def bind_report(raw, expected_sha256, *, request, replay_request_raw, check_budget):
    """Validate a response, without launching or authorizing its native event.

    `request` must be the result of the current-warrant planner. Its Python type
    is not a security capability. `replay_request_raw` must be authenticated by
    the outer snapshot controller; paths and bytes are not checked again here.
    """
    A.need(Q.A is A and S.A is A and type(request) is Q.ReferenceRequest and
           callable(check_budget), "REFERENCE_REPORT_CONFIGURATION")
    check = check_budget
    check()
    A.C.hexid(expected_sha256)
    A.need(type(raw) is bytes and 0 < len(raw) <= MAX_REPORT and
           A.sha(raw) == expected_sha256, "REFERENCE_REPORT_EXACT_BYTES")
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
        singleton = _singleton_theorem(entry["unit"])
        for output, binding, expected in zip(outputs, entry["outputs"], entry["unit"][2]):
            check()
            _fields(output, {"name", "export_id", "kind", "level_params", "projection",
                             "kernel_projection"}, "REFERENCE_REPORT_PUBLIC_OUTPUT_FIELDS")
            A.need(output["name"] == binding["name"] and output["export_id"] == binding["export_id"] and
                   type(output["kind"]) is int and output["kind"] == expected[1] and
                   output["level_params"] == expected[2], "REFERENCE_REPORT_PUBLIC_OUTPUT_IDENTITY")
            for key in ("projection", "kernel_projection"):
                value = output[key]
                A.need(value == "full" or (value == "erased_singleton_theorem" and singleton),
                       "REFERENCE_REPORT_PROJECTION")
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
        names = A.E._array(report[key], maximum=S.MAX_MODULES)
        result = []
        for name in names:
            check()
            result.append(S._module(name)[0])
        A.need(bool(result) and len(set(result)) == len(result), "REFERENCE_REPORT_MODULE_CENSUS")
        return tuple(result)

    private_modules = module_keys("private_module_names")
    public_modules = module_keys("public_module_names")
    roots = {S._module(name)[0] for name in A.E._array(replay["modules"], maximum=16)}
    A.need(bool(roots) and set(private_modules) == set(selected_modules) and
           roots <= set(public_modules) <= set(private_modules), "REFERENCE_REPORT_MODULE_MEMBERSHIP")
    for key in COUNTERS:
        _uint(report[key], 0, 2**64-1, "REFERENCE_REPORT_COUNTER:"+key)
    A.need(report["private_unit_count"] == len(units) and report["private_name_count"] == name_count and
           report["public_unit_count"] == len(public_ids) and
           report["public_name_count"] == len(public_bindings) and
           report["encoded_nodes"] == request.nodes <= 20000000 and
           report["private_scan_nodes"] + report["public_scan_nodes"] <= 20000000 and
           report["private_edges"] + report["public_edges"] <= 262144,
           "REFERENCE_REPORT_COUNTER_CENSUS")
    # Native compress and canonical encoding agree on this array-only ordinary
    # declaration grammar (byte objects have a single key). No full second array
    # is allocated just to count its brackets and commas.
    unit_bytes = 2 + len(units)-1
    for entry in units:
        check()
        unit_bytes += len(A.E.canonical_json(entry["unit"]))
    A.need(report["unit_array_bytes"] == unit_bytes <= Q.MAX_UNIT_ARRAY,
           "REFERENCE_REPORT_UNIT_BYTES")
    check()
    return BoundReferenceReport(raw, expected_sha256, tuple(public_ids), tuple(public_bindings),
                                private_modules, public_modules)

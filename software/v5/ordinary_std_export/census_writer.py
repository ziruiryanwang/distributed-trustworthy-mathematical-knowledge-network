"""Read-only, stdlib-only structural census of the one retained native writer.

This is not a portable binder, validation receipt, kernel check or output recovery.
Matches portable_owner_request.prepare's owner_absent=True frontier selection:
singleton theorem types only; all external unit references for other whole groups.
Root reviews/selects this file before one invocation. Only stdout is written.
"""
from collections import Counter, deque
from pathlib import Path
import argparse
import hashlib
import json
import stat
import sys
import time

MIB = 1024**2
WRITER_BYTES = 38154768
WRITER_SHA = "5a2f721127cfef3ae39613c1ec723b2f710cc410c872650fb2acfd7d04078b7a"
INVENTORY_SHA = "c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0"
EXPR = "DMKN_LEAN_ORIGINAL_EXPR_V1"
UNIT = "DMKN_LEAN_ORDINARY_UNIT_V1"
START, CPU_START = time.monotonic(), time.process_time()


def need(value, message):
    if not value:
        raise ValueError(message)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU_START < 30,
         "CENSUS_ORIGINAL_45_WALL_30_CPU_EXHAUSTED")


def encode(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def pairs(rows):
    result = {}
    for key, value in rows:
        need(key not in result, "DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def read(path, maximum, digest):
    check()
    need(path.is_absolute(), "ABSOLUTE_PATH")
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and
         not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT,
         "ORDINARY_INPUT_REQUIRED")
    need(0 < info.st_size <= maximum, "INPUT_BYTE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == info.st_size and hashlib.sha256(raw).hexdigest() == digest,
         "INPUT_PIN")
    check()
    return raw


def name_key(name):
    need(type(name) is list and 0 < len(name) <= 4096, "NAME_SHAPE")
    for part in name:
        need(type(part) is list and len(part) == 2 and type(part[0]) is int,
             "NAME_COMPONENT")
        if part[0] == 0:
            need(type(part[1]) is dict and set(part[1]) == {"$bytes"} and
                 type(part[1]["$bytes"]) is list and
                 all(type(x) is int and 0 <= x <= 255 for x in part[1]["$bytes"]),
                 "NAME_STRING_COMPONENT")
            bytes(part[1]["$bytes"]).decode("utf-8")
        else:
            need(part[0] == 1 and type(part[1]) is int and 0 <= part[1] < 2**32,
                 "NAME_NUMERIC_COMPONENT")
    return encode(name)


def display(key):
    # Display only; canonical structured bytes above determine all graph equality.
    return ".".join(bytes(v["$bytes"]).decode("utf-8") if tag == 0 else str(v)
                    for tag, v in json.loads(key))


def packet_refs(packet):
    need(type(packet) is list and len(packet) == 4 and packet[0] == EXPR,
         "EXPRESSION_PACKET")
    levels, nodes, root = packet[1:]
    need(type(levels) is list and type(nodes) is list and nodes and
         type(root) is int and root == len(nodes)-1, "EXPRESSION_CENSUS_SHAPE")
    refs = set()
    for index, node in enumerate(nodes):
        if index % 1024 == 0:
            check()
        need(type(node) is list and node and type(node[0]) is int and 0 <= node[0] <= 9,
             "EXPRESSION_NODE_SHAPE")
        if node[0] in (2, 8):
            need(len(node) == (3 if node[0] == 2 else 4), "REFERENCE_NODE_SHAPE")
            refs.add(name_key(node[1]))
    return refs, len(levels)+len(nodes)


def unit_packets(unit):
    """Count each serialized packet occurrence, as inspect_unit does, not DAG reachability."""
    stack, refs, total = [unit], set(), 0
    while stack:
        value = stack.pop()
        if type(value) is list:
            if value and value[0] == EXPR:
                found, count = packet_refs(value)
                refs.update(found)
                total += count
            else:
                stack.extend(value)
        elif type(value) is dict:
            # Only byte wrappers occur inside the unit format; bytes contain no refs.
            need(set(value) == {"$bytes"}, "UNEXPECTED_UNIT_OBJECT")
    return refs, total


def semantic_refs(row):
    """Mirror owner_request._semantic_refs; theorem proof details are omitted."""
    _, kind, _, packet, details = row
    refs, _ = packet_refs(packet)
    if kind in (1, 3):
        refs.update(packet_refs(details[0])[0])
    elif kind == 4:
        refs.update(name_key(n) for n in details[2]+details[3])
    elif kind == 5:
        refs.add(name_key(details[0]))
    elif kind == 6:
        refs.update(name_key(n) for n in details[0])
        for constructor, _, rhs in details[5]:
            refs.add(name_key(constructor))
            refs.update(packet_refs(rhs)[0])
    return refs


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--writer", required=True, type=Path)
    parser.add_argument("--inventory", required=True, type=Path)
    args = parser.parse_args()
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "ISOLATED_STDLIB_ONLY_INVOCATION_REQUIRED")
    raw = read(args.writer, WRITER_BYTES, WRITER_SHA)
    need(len(raw) == WRITER_BYTES, "EXACT_WRITER_LENGTH")
    inv_raw = read(args.inventory, MIB, INVENTORY_SHA)
    writer = json.loads(raw, object_pairs_hook=pairs)
    inventory = json.loads(inv_raw, object_pairs_hook=pairs)
    del raw
    need(type(writer) is dict and set(writer) == {
        "schema", "assurance", "targets", "basis_names", "units", "stats"}, "WRITER_FIELDS")
    need(writer["schema"] == "DMKN_ORDINARY_EXPORT_BUNDLE_V1" and
         writer["assurance"] == "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE", "WRITER_SCHEMA")
    need(type(inventory) is list and len(inventory) == 581 and
         writer["basis_names"] == [row[0] for row in inventory], "FIXED_BASIS_CENSUS")
    basis = {name_key(row[0]) for row in inventory}
    target = [[0, {"$bytes": list(part.encode("ascii"))}]
              for part in ("Std", "HashMap", "isEmpty_insert")]
    need(len(basis) == 581 and writer["targets"] == [target], "EXACT_BASIS_AND_TARGET")
    units = writer["units"]
    need(type(units) is list and 0 < len(units) <= 8192, "UNIT_COUNT")
    owners, data, total_bytes = {}, [], 0
    for index, unit in enumerate(units):
        check()
        need(type(unit) is list and len(unit) == 3 and unit[0] == UNIT and
             type(unit[1]) is list and unit[1] and unit[1][0] in (0, 1, 2, 3) and
             type(unit[2]) is list and unit[2], "UNIT_SHAPE")
        rows = unit[2]
        need(all(type(row) is list and len(row) == 5 and type(row[1]) is int and
                 1 <= row[1] <= 6 for row in rows), "ROW_SHAPE")
        own = {name_key(row[0]) for row in rows}
        need(len(own) == len(rows) and not own.intersection(basis) and
             not own.intersection(owners), "UNIT_NAME_COLLISION")
        complete, nodes = unit_packets(unit)
        complete.difference_update(own)
        # Native export is dependency-first. Refuse absent/forward refs, not guess.
        need(complete <= basis | owners.keys(), "FULL_UNIT_UNBOUND_OR_FORWARD_REFERENCE")
        selected = set().union(*(semantic_refs(row) for row in rows))-own
        singleton = len(rows) == 1 and rows[0][1] == 2
        if not singleton:
            selected.update(complete)
        need(selected <= complete, "SEMANTIC_REFERENCE_OUTSIDE_UNIT_IMPORTS")
        byte_count = len(encode(unit))  # One unit at a time; never rebuild the bundle.
        total_bytes += byte_count
        data.append(dict(own=own, full=complete, selected=selected, nodes=nodes,
                         bytes=byte_count, singleton=singleton,
                         kinds=Counter(row[1] for row in rows), descriptor=unit[1][0]))
        owners.update((key, index) for key in own)
    need(writer["stats"]["selected_units"] == len(units) and
         writer["stats"]["unit_json_bytes"] == total_bytes, "NATIVE_UNIT_BYTE_CENSUS")

    def closure(field):
        pending, found = deque([name_key(target)]), set()
        while pending:
            check()
            key = pending.popleft()
            if key in basis:
                continue
            need(key in owners, "UNRESOLVED_NONBASIS_REFERENCE")
            index = owners[key]
            if index not in found:
                found.add(index)
                pending.extend(data[index][field])
        return found

    full, frontier = closure("full"), closure("selected")
    names = set().union(*(data[i]["own"] for i in frontier))
    required = set().union(*(data[i]["selected"] for i in frontier))
    omitted = set().union(*(data[i]["full"] for i in frontier))-basis-names
    need(not (required-basis-names), "FRONTIER_NOT_CLOSED")

    def summary(indices):
        kinds, descriptors = Counter(), Counter()
        for i in indices:
            kinds.update(data[i]["kinds"])
            descriptors[data[i]["descriptor"]] += 1
        largest = sorted(indices, key=lambda i: (-data[i]["bytes"], i))[:12]
        return {"units": len(indices), "rows": sum(len(data[i]["own"]) for i in indices),
            "canonical_unit_bytes": sum(data[i]["bytes"] for i in indices),
            "serialized_nodes": sum(data[i]["nodes"] for i in indices),
            "selected_edges": sum(len(data[i]["selected"]) for i in indices),
            "full_import_edges": sum(len(data[i]["full"]) for i in indices),
            "singleton_theorem_groups": sum(data[i]["singleton"] for i in indices),
            "inventory_kind_counts": dict(sorted(kinds.items())),
            "descriptor_kind_counts": dict(sorted(descriptors.items())),
            "largest_units": [{"writer_index": i, "rows": len(data[i]["own"]),
                "canonical_unit_bytes": data[i]["bytes"], "nodes": data[i]["nodes"],
                "names": [display(k) for k in sorted(data[i]["own"])]} for i in largest]}

    report = {"schema": "DMKN_NATIVE_WRITER_FRONTIER_CENSUS_V1",
        "authority": "STRUCTURAL_DATA_ANALYSIS_NOT_PORTABLE_BINDING_OR_ACCEPTANCE",
        "writer_sha256": WRITER_SHA, "writer_bytes": WRITER_BYTES,
        "inventory_sha256": INVENTORY_SHA, "target": target, "native_stats": writer["stats"],
        "writer_unit_count": len(units), "whole_proof_closure": summary(full),
        "signature_materialization_frontier": summary(frontier),
        "frontier_writer_indices": sorted(frontier), "basis_rows": len(basis),
        "rows_including_basis": len(names)+len(basis), "induced_missing_references": [],
        "proof_only_external_boundary_count": len(omitted),
        "proof_only_external_boundary": [{"name": json.loads(k), "display": display(k)} for k in sorted(omitted)],
        "byte_scope": "EXACT_CANONICAL_NATIVE_UNIT_BYTES_ONLY;LOWER_BOUND_ON_PORTABLE_EVIDENCE;NO_MANIFEST_RECOVERY",
        "whole_writer_is_target_closure": full == set(range(len(units)))}
    # Recheck selected raw inputs, without product imports or writes.
    del writer, units, inventory
    read(args.writer, WRITER_BYTES, WRITER_SHA)
    read(args.inventory, MIB, INVENTORY_SHA)
    report.update(wall_seconds=time.monotonic()-START, cpu_seconds=time.process_time()-CPU_START)
    output = encode(report)
    need(len(output) <= 4*MIB, "OUTPUT_BOUND")
    check()
    sys.stdout.buffer.write(output+b"\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        sys.stderr.write("CENSUS_FAILED "+type(error).__name__+": "+str(error)[:2048]+"\n")
        raise SystemExit(1)

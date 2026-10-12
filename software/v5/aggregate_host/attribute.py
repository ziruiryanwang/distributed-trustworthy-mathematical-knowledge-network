"""Offline attribution of exact aggregate instruction samples, never proof cost.

Only a separately selected immutable source snapshot may run this helper. Its
pinned selection binds saved execution/assembly records; it invokes no tools,
SDK, guest, compiler or prover. Ordinary execution failures remain prefixes.
"""
from pathlib import Path
import argparse
import hashlib
import heapq
import json
import os
import re
import struct
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
MIB = 1024**2
U32, U64 = 2**32, 2**64
STRIDE, CELL_LIMIT, WINDOW = 256, 131072, 2**20
MAP_ROWS, MATCH_LIMIT, REPORT_LIMIT = 100000, 524288, 64 * MIB
MEASUREMENT = "DETERMINISTIC_INSTRUCTION_SAMPLES_NOT_PROOF_CYCLE_ATTRIBUTION"
MAP_HEADER = "     VMA      LMA     Size Align Out     In      Symbol"
MAP_ROW = re.compile(r"^\s*([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+([0-9]+)(\s+)(.*)$")
CATEGORIES = ("symbol", "ambiguous_symbol", "section_only", "ambiguous_section",
              "unknown_user_code", "outside_user_executable")


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def integer(value, maximum, reason, minimum=0):
    need(type(value) is int and minimum <= value <= maximum, reason)
    return value


def digest(value):
    need(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value), "LOWERCASE_SHA256")
    return value


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def parse(raw):
    def no_constant(_):
        raise ValueError("NONFINITE_JSON_NUMBER")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                      parse_constant=no_constant)


def coarse_class(name):
    # Match the owning namespace only, never a type appearing in a generic arg.
    prefixes = (
        ("dmkn_aggregate_relation::relation::", "aggregate_orchestration"),
        ("dmkn_aggregate_relation::census::", "aggregate_census"),
        ("dmkn_aggregate_relation::wire::", "aggregate_wire"),
        ("dmkn_aggregate_relation::membership::", "aggregate_membership"),
        ("dmkn_aggregate_relation::header::", "aggregate_header"),
        ("dmkn_module_relation::relation::", "module_orchestration"),
        ("dmkn_module_relation::canonical::", "module_canonical"),
        ("dmkn_module_relation::commitments::", "module_commitments"),
        ("dmkn_module_relation::journal::", "module_journal"),
        ("dmkn_module_relation::policy::", "module_policy"),
        ("nanoda_lib::parser::", "native_row_parser"),
        ("nanoda_lib::module_correspondence::", "canonical_native_correspondence"),
        ("nanoda_lib::tc::", "checker_typechecking"),
        ("nanoda_lib::inductive::", "checker_inductive"),
        ("nanoda_lib::quot::", "checker_quotient"),
        ("nanoda_lib::level::", "checker_levels"),
        ("nanoda_lib::expr::", "checker_expressions"),
        ("serde_json::", "serialization"), ("serde_core::", "serialization"),
        ("sha2::", "hashing"), ("risc0_zkvm::sha::", "hashing"),
        ("alloc::", "general_runtime"), ("core::", "general_runtime"),
        ("std::", "general_runtime"), ("risc0_zkvm::guest::", "guest_runtime"),
    )
    if name in ("memcpy", "memset", "memmove", "memcmp"):
        return "general_runtime"
    return next((label for prefix, label in prefixes if name.startswith(prefix)), "unclassified")


def elf_headers(raw):
    need(len(raw) >= 52 and raw[:7] == b"\x7fELF\x01\x01\x01", "ELF32_LE_VERSION1")
    fields = struct.unpack_from("<HHIIIIIHHHHHH", raw, 16)
    kind, machine, version, entry, phoff, _, _, ehsize, phsize, phcount, _, _, _ = fields
    need((kind, machine, version, ehsize, phsize) == (2, 243, 1, 52, 32)
         and 1 <= phcount <= 256 and phoff + phcount * phsize <= len(raw), "RV32_PROGRAM_HEADERS")
    segments, executable = [], []
    for index in range(phcount):
        kind, offset, address, _, filesz, memsz, flags, _ = struct.unpack_from("<IIIIIIII", raw, phoff + index * phsize)
        if kind == 1:
            need(filesz <= memsz and offset + filesz <= len(raw) and address + memsz <= U32,
                 "BOUNDED_LOAD_SEGMENT")
            segments.append({"address": address, "file_bytes": filesz, "memory_bytes": memsz, "flags": flags})
            if flags & 1 and memsz:
                executable.append((address, address + memsz))
    executable.sort()
    need(executable and all(a[1] <= b[0] for a, b in zip(executable, executable[1:]))
         and any(start <= entry < end for start, end in executable), "DISJOINT_EXECUTABLE_ENTRY_RANGES")
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "entry": entry, "segments": segments}, executable


def map_intervals(raw, executable):
    lines = raw.decode("utf-8").splitlines()
    need(lines and lines[0] == MAP_HEADER and len(lines) <= MAP_ROWS + 1, "EXACT_BOUNDED_LINKER_MAP_FORMAT")
    intervals, labels, out, inp = [], [], None, None
    counts = {"output": 0, "input": 0, "symbol": 0, "zero_size_rows": 0,
              "nonexecutable_rows": 0, "executable_intervals": 0}
    for line_number, line in enumerate(lines[1:], 2):
        need(line and len(line) <= 16384, "MAP_LINE_BOUND")
        match = MAP_ROW.fullmatch(line)
        need(match is not None and match.start(6) in (33, 41, 49), "UNSUPPORTED_MAP_RECORD_LAYOUT")
        start, lma, size = (int(match[i], 16) for i in (1, 2, 3))
        align, name, column = int(match[4]), match[6], match.start(6)
        need(0 <= start < U32 and 0 <= lma < U32 and 0 <= size <= U32
             and start + size <= U32 and 0 < align <= U32 and name, "MAP_ADDRESS_SIZE_OR_NAME")
        row = {"id": line_number, "start": start, "end": start + size, "name": name}
        kind = {33: "output", 41: "input", 49: "symbol"}[column]
        counts[kind] += 1
        counts["zero_size_rows"] += int(size == 0)
        if kind == "output":
            out, inp = row, None
        elif kind == "input":
            need(out is not None and out["start"] <= start <= row["end"] <= out["end"],
                 "INPUT_SECTION_OUTSIDE_OUTPUT")
            inp = row
        else:
            need(out is not None, "SYMBOL_WITHOUT_OUTPUT")
        in_exec = any(a <= start < b and row["end"] <= b for a, b in executable)
        if not in_exec:
            need(not size or not any(start < b and a < row["end"] for a, b in executable),
                 "MAP_RANGE_PARTIALLY_OVERLAPS_EXECUTABLE")
            counts["nonexecutable_rows"] += 1
            continue
        if kind == "symbol":
            need(inp is not None and inp["start"] <= start <= row["end"] <= inp["end"],
                 "EXECUTABLE_SYMBOL_OUTSIDE_INPUT_SECTION")
        row.update(kind=kind, output_section=out["id"],
                   input_section=inp["id"] if inp is not None else None)
        if not size:
            labels.append(row)
        elif kind != "output":
            row["class"] = coarse_class(name) if kind == "symbol" else "section_only"
            intervals.append(row)
    counts["executable_intervals"] = len(intervals)
    return intervals, labels, counts


def sample_cells(diag):
    need(diag["schema"] == "DMKN_AGGREGATE_EXECUTION_DIAGNOSTIC_V1"
         and diag["status"] in ("CAPSULE_RETAINED_NOT_CERTIFICATE", "FAILED_NO_ACCEPTED_CAPSULE")
         and type(diag["guest_execute_calls"]) is int and diag["guest_execute_calls"] == 1
         and type(diag["proof_calls"]) is int and diag["proof_calls"] == 0
         and diag["mathematical_admission"] is False, "EXACT_NONCERTIFICATE_DIAGNOSTIC")
    samples = diag["samples"]
    need(samples["enabled"] is True and samples["measurement"] == MEASUREMENT
         and type(samples["stride"]) is int and samples["stride"] == STRIDE
         and type(samples["cell_limit"]) is int and samples["cell_limit"] == CELL_LIMIT
         and type(samples["cycle_window"]) is int and samples["cycle_window"] == WINDOW
         and type(samples["saturated"]) is bool, "EXACT_SAMPLING_CONVENTION")
    counters = ("instructions_observed", "samples_stored", "samples_omitted",
                "maximum_reported_cycle", "backwards_cycle_events")
    for key in counters:
        integer(samples[key], U64 - 2, "NO_U64_SATURATION:" + key)
    cells = samples["samples"]
    need(type(cells) is list and len(cells) <= CELL_LIMIT, "SAMPLE_CELL_BOUND")
    prior, stored, per_pc = None, 0, {}
    for cell in cells:
        need(type(cell) is list and len(cell) == 3, "EXACT_SAMPLE_TRIPLE")
        window = integer(cell[0], samples["maximum_reported_cycle"] // WINDOW, "SAMPLE_WINDOW")
        pc = integer(cell[1], U32 - 1, "U32_BYTE_PC")
        count = integer(cell[2], U64 - 2, "POSITIVE_UNSATURATED_CELL", 1)
        key = (window, pc)
        need(prior is None or prior < key, "SORTED_UNIQUE_SAMPLE_KEYS")
        prior = key
        stored += count
        per_pc[pc] = per_pc.get(pc, 0) + count
    observed, omitted = samples["instructions_observed"], samples["samples_omitted"]
    need(stored == samples["samples_stored"] and stored + omitted == (observed + STRIDE - 1) // STRIDE,
         "EXACT_SAMPLE_COUNT_CONSERVATION")
    need(samples["saturated"] == (omitted > 0) and (not omitted or len(cells) == CELL_LIMIT)
         and samples["backwards_cycle_events"] <= max(0, observed - 1), "SATURATION_AND_BACKWARDS_CONSISTENCY")
    return samples, per_pc


def attribute(intervals, executable, per_pc):
    # Each interval enters/leaves once. Only active matches are enumerated.
    ordered = sorted(intervals, key=lambda row: (row["start"], row["end"], row["id"]))
    by_id = {row["id"]: row for row in intervals}
    active_symbols, active_sections, ends = set(), set(), []
    cursor = emitted = 0
    histogram = dict.fromkeys(CATEGORIES, 0)
    classes, ranges, pcs = {}, {}, []
    for pc, count in sorted(per_pc.items()):
        while cursor < len(ordered) and ordered[cursor]["start"] <= pc:
            row = ordered[cursor]
            active = active_symbols if row["kind"] == "symbol" else active_sections
            active.add(row["id"])
            heapq.heappush(ends, (row["end"], row["id"], row["kind"]))
            cursor += 1
        while ends and ends[0][0] <= pc:
            _, row_id, kind = heapq.heappop(ends)
            (active_symbols if kind == "symbol" else active_sections).remove(row_id)
        candidates = active_symbols or active_sections
        emitted += len(candidates)
        need(emitted <= MATCH_LIMIT, "BOUNDED_AMBIGUITY_OUTPUT_NO_TRUNCATION")
        ids = sorted(candidates)
        if active_symbols:
            category = "symbol" if len(ids) == 1 else "ambiguous_symbol"
        elif active_sections:
            category = "section_only" if len(ids) == 1 else "ambiguous_section"
        else:
            category = ("unknown_user_code" if any(a <= pc < b for a, b in executable)
                        else "outside_user_executable")
        label = by_id[ids[0]]["class"] if category == "symbol" else category
        histogram[category] += count
        classes[label] = classes.get(label, 0) + count
        if category in ("symbol", "section_only"):
            ranges[ids[0]] = ranges.get(ids[0], 0) + count
        pcs.append({"pc": pc, "samples": count, "category": category, "class": label, "range_ids": ids})
    total = sum(per_pc.values())
    need(sum(histogram.values()) == sum(classes.values()) == total, "ATTRIBUTION_COUNT_CONSERVATION")
    return {"pc_attribution": pcs, "category_counts": histogram, "class_counts": classes,
            "unique_range_counts": [{"range_id": key, "samples": value} for key, value in sorted(ranges.items())],
            "stored_samples": total, "candidate_references": emitted,
            "class_fractions": {key: value / total for key, value in classes.items()} if total else {},
            "fraction_meaning": "RETAINED_DETERMINISTIC_INSTRUCTION_SAMPLES_ONLY"}


def main():
    invoked = Path(__file__).resolve(strict=True)
    need(invoked.is_relative_to(HERE), "OWNER_SNAPSHOT_ROOT")
    parts = invoked.relative_to(HERE).parts
    need(len(parts) == 6 and parts[1:] == ("sources", "software", "v5", "aggregate_host", "attribute.py")
         and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", parts[0]) and os.name == "nt"
         and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "CANONICAL_ISOLATED_OWNER_SNAPSHOT")
    parser = argparse.ArgumentParser()
    parser.add_argument("selection")
    parser.add_argument("selection_sha256")
    args = parser.parse_args()
    bound, read_bytes = {}, 0

    def bind(pin, maximum):
        nonlocal read_bytes
        need(type(pin) is dict and set(pin) in ({"path", "sha256"}, {"path", "bytes", "sha256"}), "EXACT_FILE_PIN")
        path = Path(pin["path"])
        need(path.is_absolute() and path.is_relative_to(HERE) and path.resolve(strict=True) == path
             and path.is_file(), "EXACT_LOCAL_INPUT_PATH")
        digest(pin["sha256"])
        if "bytes" in pin:
            integer(pin["bytes"], maximum, "PIN_BYTE_BOUND", 1)
        size = path.stat().st_size
        need(0 < size <= maximum and ("bytes" not in pin or pin["bytes"] == size), "INPUT_SIZE_BOUND")
        read_bytes += size
        need(read_bytes <= 128 * MIB, "TOTAL_INPUT_BYTE_BOUND")
        with path.open("rb") as stream:
            raw = stream.read(maximum + 1)
        actual = {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        need(len(raw) == size == path.stat().st_size and actual["sha256"] == pin["sha256"], "INPUT_PIN_CHANGED")
        need(str(path) not in bound or bound[str(path)] == actual, "CONFLICTING_INPUT_PINS")
        bound[str(path)] = actual
        return raw

    config = parse(bind({"path": args.selection, "sha256": digest(args.selection_sha256)}, MIB))
    need(set(config) == {"schema", "diagnostic", "execution_result", "execution_command",
                         "assembly_result", "assembly_command", "output"}
         and config["schema"] == "DMKN_PC_ATTRIBUTION_SELECTION_V1", "EXACT_SELECTION_SCHEMA")
    output = Path(config["output"])
    operation = HERE / parts[0]
    need(output.is_absolute() and output.is_relative_to(operation) and output.resolve() == output
         and output.parent.is_dir() and not output.exists(), "FRESH_OPERATION_OUTPUT")
    output.mkdir()
    report = {"schema": "DMKN_PC_ATTRIBUTION_RESULT_V1", "status": "FAIL_PC_ATTRIBUTION",
              "measurement": MEASUREMENT, "tool_calls": 0, "guest_executions": 0,
              "proof_calls": 0, "mathematical_admission": False}
    code = 1
    try:
        records = {key: parse(bind(config[key], 8 * MIB if key == "diagnostic" else 2 * MIB))
                   for key in ("diagnostic", "execution_result", "execution_command", "assembly_result", "assembly_command")}
        diag, execution, execution_command, assembly, command = (records[key] for key in
            ("diagnostic", "execution_result", "execution_command", "assembly_result", "assembly_command"))
        assembly_dir = Path(config["assembly_result"]["path"]).parent
        execution_dir = Path(config["execution_result"]["path"]).parent
        need(Path(config["assembly_command"]["path"]) == assembly_dir / "COMMAND.json"
             and Path(config["execution_command"]["path"]) == execution_dir / "COMMAND.json"
             and Path(config["diagnostic"]["path"]) == execution_dir / "diagnostic.json",
             "EXACT_SIBLING_OPERATION_RECORDS")
        need(assembly["schema"] == "DMKN_V5_AGGREGATE_IMAGE_ASSEMBLY_RESULT_V1"
             and assembly["status"] == "PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY"
             and assembly["assembler_calls"] == 1 and assembly["guest_executions"] == assembly["proof_calls"] == 0
             and assembly["mathematical_admission"] is False and assembly["prior_resource_failure_preserved"] is True
             and not (assembly_dir / "FINALIZATION-FAILED.json").exists(), "ADOPTED_ASSEMBLY_NOT_ADMISSION")
        need(command["authority"] == "ASSEMBLY_ONLY_NOT_ADMISSION" and command["cwd"] == str(ROOT)
             and command["artifact_validation"]["sha256"] == assembly["artifact_validation_sha256"], "ASSEMBLY_COMMAND_BINDING")
        validation_path = Path(command["artifact_validation"]["path"])
        validation = parse(bind(command["artifact_validation"], 2 * MIB))
        need(validation["schema"] == "DMKN_V5_AGGREGATE_ARTIFACT_VALIDATION_V1"
             and validation["status"] == "PASS_REVALIDATED_AGGREGATE_GUEST_ARTIFACT_ONLY"
             and validation["old_failure_preserved"] is True and validation["prior_budget_met"] is False
             and validation["prior_effective_status"] == "FAIL_FINALIZATION"
             and validation["mathematical_admission"] is False
             and not (validation_path.parent / "FINALIZATION-FAILED.json").exists(), "ARTIFACT_REVALIDATION_NOT_BUDGET_PASS")
        build_pin, failure_pin = command["guest_build_result"], command["preserved_resource_failure"]
        need(validation["compile_result"] == {key: build_pin[key] for key in ("path", "sha256")}
             and validation["preserved_failure"] == {key: failure_pin[key] for key in ("path", "sha256")}
             and Path(failure_pin["path"]) == Path(build_pin["path"]).parent / "FINALIZATION-FAILED.json", "PRESERVED_COMPILE_LINEAGE")
        built, failure = parse(bind(build_pin, 2 * MIB)), parse(bind(failure_pin, 65536))
        need(failure == {"status": "FAIL_FINALIZATION", "overrides_result_and_attempt": True,
              "result_sha256": build_pin["sha256"], "error": "REMAINING_TOTAL_ENVELOPE"}
             and built["artifact"] == validation["artifact"]
             and command["user_elf"] == built["artifact"]["user_elf"], "ORIGINAL_RESOURCE_FAILURE_RETAINED")
        artifact = validation["artifact"]
        elf = bind(artifact["user_elf"], 64 * MIB)
        map_raw = bind(artifact["link_map"], 8 * MIB)
        headers, executable = elf_headers(elf)
        need(headers == artifact["elf_headers"], "ACTUAL_EXECUTABLE_HEADERS_MATCH_VALIDATION")
        need(command["argv"] == [command["assembler"]["path"], "assemble", artifact["user_elf"]["path"],
                                 command["kernel"]["path"], assembly["image"]["path"]], "EXACT_ASSEMBLY_ARGV")
        bind(assembly["image"], 64 * MIB)
        digest(assembly["image_id"])
        need(diag["aggregate_image"] == execution["aggregate_image"] == assembly["image_id"]
             and diag["elf_sha256"] == assembly["image"]["sha256"]
             and execution["schema"] == "DMKN_AGGREGATE_COST_SCREEN_RESULT_V1"
             and execution["status"] in ("PASS_ONE_AGGREGATE_EXECUTION_CAPSULE_ONLY", "FAIL", "FAIL_FINAL_BINDING")
             and execution["host_calls"] == 1 and execution["proof_calls"] == 0
             and execution["mathematical_admission"] is False
             and execution["diagnostic"] == bound[config["diagnostic"]["path"]], "ACTUAL_DIAGNOSTIC_IMAGE_BINDING")
        argv = execution_command["argv"]
        need(type(argv) is list and len(argv) == 13 and argv[1:4] == ["snapshot", assembly["image_id"], assembly["image"]["path"]]
             and argv[8] == "pc-samples" and argv[10] == config["diagnostic"]["path"] and argv[11] == "1"
             and execution_command["authority"] == "ONE_GUEST_COST_SCREEN_NO_PROOF_OR_ADMISSION", "EXACT_SNAPSHOT_COMMAND")
        cycles = integer(diag["cycles_cap"], 2**28, "DIAGNOSTIC_CYCLE_CAP", 1)
        po2 = integer(diag["segment_po2"], 20, "DIAGNOSTIC_SEGMENT_PO2", 12)
        need(argv[6:8] == [str(cycles), str(po2)] and execution["cycles"] == cycles
             and execution["segment_po2"] == po2, "CONSISTENT_EXECUTION_BOUNDS")
        bind({"path": argv[4], "bytes": diag["wire_bytes"], "sha256": digest(diag["wire_sha256"])}, 16 * MIB)
        need(type(diag["header"]) is list and len(diag["header"]) == 192
             and all(type(value) is int and 0 <= value <= 255 for value in diag["header"]), "EXACT_HEADER_BYTES")
        header = bytes(diag["header"])
        bind({"path": argv[5], "bytes": len(header), "sha256": hashlib.sha256(header).hexdigest()}, 192)
        if diag["status"] == "FAILED_NO_ACCEPTED_CAPSULE":
            need(diag["result"] is None and execution["status"] != "PASS_ONE_AGGREGATE_EXECUTION_CAPSULE_ONLY",
                 "FAILED_DIAGNOSTIC_CANNOT_CLAIM_CAPSULE_PASS")
            extent = ("FAILED_EXECUTION_PREFIX_ONLY" if diag["session_stats"] is None
                      else "FAILED_AFTER_EXECUTION_NO_ACCEPTED_CAPSULE")
        else:
            result = diag["result"]
            need(type(result) is dict and type(diag["session_stats"]) is dict
                 and result["schema"] == "DMKN_AGGREGATE_SNAPSHOT_RESULT_V1"
                 and result["status"] == "UNTRUSTED_AGGREGATE_EXECUTION_CAPSULE_RETAINED"
                 and result["aggregate_image"] == assembly["image_id"] and result["header"] == diag["header"]
                 and result["capsule_path"] == argv[9] and result["guest_execute_calls"] == 1
                 and result["proof_calls"] == 0 and result["mathematical_admission"] is False,
                 "CONSISTENT_HOST_REPORTED_COMPLETED_CAPSULE")
            if execution["status"] == "PASS_ONE_AGGREGATE_EXECUTION_CAPSULE_ONLY":
                need(execution["actual_result"] == result, "WRAPPER_COMPLETION_MATCHES_DIAGNOSTIC")
            extent = "HOST_REPORTED_GUEST_COMPLETED_CAPSULE_NOT_WRAPPER_ACCEPTANCE"
        # A wrapper failure stays a failure even if the guest wrote its capsule.
        execution_override = execution_dir / "FINALIZATION-FAILED.json"
        if execution_override.exists():
            need(execution_override.stat().st_size <= 65536, "EXECUTION_OVERRIDE_BOUND")
            with execution_override.open("rb") as stream:
                raw_override = stream.read(65537)
            need(0 < len(raw_override) <= 65536, "EXECUTION_OVERRIDE_BOUND")
            override_pin = {"path": str(execution_override), "bytes": len(raw_override),
                            "sha256": hashlib.sha256(raw_override).hexdigest()}
            bind(override_pin, 65536)
            report["execution_finalization_override"] = override_pin
        samples, per_pc = sample_cells(diag)
        intervals, labels, parse_counts = map_intervals(map_raw, executable)
        attribution = attribute(intervals, executable, per_pc)
        report.update(status="PASS_PC_SAMPLE_ATTRIBUTION_ONLY", execution_status=execution["status"],
            diagnostic_status=diag["status"],
            diagnostic_error=diag.get("error"), execution_error=execution.get("error"),
            execution_cycle_cap=diag["cycles_cap"],
            execution_extent=extent,
            prior_compile_effective_status="FAIL_FINALIZATION", prior_budget_met=False,
            executable_ranges=[{"start": start, "end": end} for start, end in executable],
            address_convention="RAW_VIRTUAL_BYTE_PC_NO_REBASE", map_parse_counts=parse_counts,
            intervals=intervals, zero_sized_labels=labels, samples=samples, attribution=attribution,
            window_order_is_chronological=samples["backwards_cycle_events"] == 0,
            window_measure="SDK_REPORTED_ROW_POINTS_NOT_EQUAL_WALL_TIME_OR_INSTRUCTION_WINDOWS",
            limitations=["Periodic deterministic sampling may alias loops.",
                         "After cell saturation unseen window/PC pairs are omitted while existing pairs grow; retained samples favor previously seen cells.",
                         "No confidence interval or attribution of omitted samples is asserted.",
                         "A symbol identifies machine code, not inline provenance or caller-inclusive cost.",
                         "No cycle, proof-time, wall-time or whole-workflow cost fraction is inferred.",
                         "Host and SDK provenance is reused from the outer selected operation, not requalified here."])
        # Small exact-file rebind only; never traverse a SDK/cache/target tree.
        for pin in list(bound.values()):
            bind(pin, pin["bytes"])
        need(not (assembly_dir / "FINALIZATION-FAILED.json").exists()
             and not (validation_path.parent / "FINALIZATION-FAILED.json").exists(), "INPUT_OPERATION_FINALIZATION_CHANGED")
        code = 0
    except Exception as error:
        report.update(status="FAIL_PC_ATTRIBUTION", error=type(error).__name__ + ": " + str(error)[:2000])
    report["bound_files"] = bound
    raw_report = (json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    need(len(raw_report) <= REPORT_LIMIT, "REPORT_BYTE_BOUND")
    with (output / "RESULT.json").open("xb") as stream:
        stream.write(raw_report)
    print(json.dumps({"status": report["status"], "output": str(output), "proof_calls": 0}))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

"""One offline exact-image failure view; no execution or speedup comparison.

Reuse the frozen attribution algorithms. Only current record binding and small
summaries are new; the prior adopted attribution report is read, never rerun.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
MIB = 1024**2
HELPER_SHA = "0fc2ca9b35892cf86b3f8fdbf124db8cdb31f6cd20658125e2d6c23967c3a786"
A = "173255698c2bc9030e7528297b627c59d6d35a605ec3a16542b2ba73e5107ac2"
LOCATIONS = {
    "build_result": "bounded-parse-direct-build-01/RESULT.json",
    "build_attempt": "bounded-parse-direct-build-01-attempt.json",
    "artifact": "bounded-parse-direct-build-01/ARTIFACT.json",
    "source_map": "bounded-parse-direct-build-01/SOURCE-MAP.json",
    "assembly_result": "bounded-parse-image-assembly-01/assembly/RESULT.json",
    "assembly_outer": "bounded-parse-image-assembly-01/RESULT.json",
    "assembly_command": "bounded-parse-image-assembly-01/assembly/COMMAND.json",
    "screen_result": "bounded-parse-aggregate-snapshot-01/evidence/RESULT.json",
    "screen_outer": "bounded-parse-aggregate-snapshot-01/RESULT.json",
    "screen_command": "bounded-parse-aggregate-snapshot-01/evidence/COMMAND.json",
    "diagnostic": "bounded-parse-aggregate-snapshot-01/evidence/diagnostic.json",
    "baseline_report": "aggregate-pc-attribution-01/attribution/RESULT.json",
}
ANCHORS = {
    "build_result": "694d205b63082ecd02536eb70b16ae08a271f06d66d5df95f296a51a607ce22b",
    "assembly_result": "696774f9616ffd0f8a058eccf5fbf13f9f6b6e2eb0cfdbb5f7ee6acde75e6b7a",
    "assembly_outer": "f92ac44d3b2b12c677e3dcbe819dd64703cfd9f1da00d01efd58bb68e49c47ab",
    "screen_result": "bc7fae70d1a7cde35a3db76a075ff289d8e082dea90b4ec2f726fb05ed99ba05",
    "screen_outer": "a4db15321bc9084ba5db4c7f4dbbb702a391909c8cafe7fd7d82f7ecec6237e9",
    "diagnostic": "dca409e07e44f7647c2b248167cadcba6f5ad0827af83a3aa3173e0aee0bda72",
    "baseline_report": "31b29b7a8888fbfa0337fbf3a72b3269d2facbf05513d0e27a23ac4ca91de84b",
}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def closed(outer, exit_code):
    need(outer["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1", "OUTER_SCHEMA")
    value = outer["result"]
    need(value["child_exit_code"] == exit_code and value["direct_child_reaped"] is True
         and value["job_closed"] is True and value["cleanup_errors"] == []
         and value["termination_requested"] is False
         and value["final_job"]["active_processes"] == 0
         and value["final_job"]["terminated_processes"] == 0
         and value["status"] == ("COMMAND_EXITED_ZERO_AND_CLOSED" if exit_code == 0 else "COMMAND_FAILED"),
         "EXACT_CLEAN_OUTER_COMPLETION")


def summarize(samples, attribution, intervals):
    """Count aggregation only; PC/range resolution belongs to the frozen helper."""
    stored, omitted = samples["samples_stored"], samples["samples_omitted"]
    total = stored + omitted
    need(total > 0 and attribution["stored_samples"] == stored, "SUMMARY_TOTAL")
    by_id = {row["id"]: row for row in intervals}
    windows = {}
    for window, _pc, count in samples["samples"]:
        windows[window] = windows.get(window, 0) + count
    need(sum(windows.values()) == stored, "WINDOW_COUNT_CONSERVATION")
    rows = []
    for count in attribution["unique_range_counts"]:
        symbol = by_id[count["range_id"]]
        if symbol["kind"] == "symbol":
            rows.append({"range_id": symbol["id"], "name": symbol["name"],
                "start": symbol["start"], "end": symbol["end"],
                "input_section": symbol["input_section"],
                "input_object": by_id[symbol["input_section"]]["name"], "class": symbol["class"],
                "stored_samples": count["samples"],
                "unique_attribution_sample_count_bounds": [count["samples"], count["samples"] + omitted]})
    rows.sort(key=lambda row: (-row["stored_samples"], row["range_id"]))
    classes = [{"class": label, "stored_samples": count,
                "all_sampled_event_count_bounds": [count, count + omitted]}
               for label, count in sorted(attribution["class_counts"].items(), key=lambda item: (-item[1], item[0]))]
    need(sum(row["stored_samples"] for row in classes) == stored, "CLASS_COUNT_CONSERVATION")
    return {"instructions_observed": samples["instructions_observed"],
        "stored_samples": stored, "omitted_samples": omitted, "all_sampled_events": total,
        "sample_cells": len(samples["samples"]), "saturated": samples["saturated"],
        "stride": samples["stride"], "sdk_row_window_size": samples["cycle_window"],
        "maximum_reported_cycle": samples["maximum_reported_cycle"],
        "backwards_cycle_events": samples["backwards_cycle_events"],
        "window_counts": [[window, count] for window, count in sorted(windows.items())],
        "window_count_meaning": "RETAINED_SAMPLES_ONLY_OMITTED_EVENTS_HAVE_NO_RECORDED_WINDOW",
        "unrepresented_window_count_is_not_zero": True,
        "category_counts": attribution["category_counts"], "classes": classes,
        "top_symbols": rows[:40], "total_unique_symbol_ranges_with_samples": len(rows),
        "top_list_truncated": len(rows) > 40,
        "bounds_meaning": "GLOBAL_MISSING_LABEL_ACCOUNTING_NOT_STATISTICAL_OR_CYCLE_BOUNDS",
        "symbol_meaning": "UNIQUE_ATTRIBUTION_LABEL_NOT_ALL_OVERLAPPING_RANGE_PCS_OR_INLINE_OR_CALLER_INCLUSIVE_COST"}


def main():
    invoked = Path(__file__).resolve(strict=True)
    need(invoked.is_relative_to(HERE) and os.name == "nt" and Path.cwd() == ROOT
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "SELECTED_ISOLATED_SNAPSHOT")
    parts = invoked.relative_to(HERE).parts
    need(parts == ("bounded-parse-pc-attribution-01", "sources", "software", "v5",
                   "bounded_parse_guest", "attribute.py"), "EXACT_ADAPTER_SNAPSHOT")
    helper = invoked.parents[1] / "aggregate_host/attribute.py"
    with helper.open("rb") as stream:
        helper_raw = stream.read(25116)
    need(len(helper_raw) == 25115 and hashlib.sha256(helper_raw).hexdigest() == HELPER_SHA,
         "FROZEN_PURE_ATTRIBUTION_HELPER")
    spec = importlib.util.spec_from_file_location("_bounded_parse_frozen_attribution", helper)
    h = importlib.util.module_from_spec(spec)
    exec(compile(helper_raw, str(helper), "exec"), h.__dict__)
    bound, read_bytes = {}, 0

    def bind(pin, maximum):
        nonlocal read_bytes
        need(type(pin) is dict and set(pin) == {"path", "bytes", "sha256"}, "EXACT_FILE_PIN")
        path = Path(pin["path"])
        need(path.is_absolute() and path.is_relative_to(HERE) and path.resolve(strict=True) == path
             and path.is_file(), "ORDINARY_LOCAL_INPUT")
        h.integer(pin["bytes"], maximum, "INPUT_BYTE_BOUND", 1); h.digest(pin["sha256"])
        need(path.stat().st_size == pin["bytes"], "INPUT_SIZE")
        read_bytes += pin["bytes"]; need(read_bytes <= 128*MIB, "TOTAL_READ_BOUND")
        with path.open("rb") as stream:
            raw = stream.read(maximum + 1)
        need(len(raw) == pin["bytes"] == path.stat().st_size
             and hashlib.sha256(raw).hexdigest() == pin["sha256"], "INPUT_PIN_CHANGED")
        need(str(path) not in bound or bound[str(path)] == pin, "CONFLICTING_PIN")
        bound[str(path)] = dict(pin)
        return raw

    config_path = Path(sys.argv[1]); h.digest(sys.argv[2])
    config = h.parse(bind({"path": str(config_path), "bytes": config_path.stat().st_size,
                          "sha256": sys.argv[2]}, MIB))
    need(set(config) == {"schema", "records", "output"}
         and config["schema"] == "DMKN_BOUNDED_PARSE_ATTRIBUTION_SELECTION_V1"
         and type(config["records"]) is dict and set(config["records"]) == set(LOCATIONS), "CONFIG_SCHEMA")
    pins = config["records"]
    for key, relative in LOCATIONS.items():
        need(pins[key]["path"] == str(HERE / relative), "EXACT_RECORD_LOCATION:" + key)
        if key in ANCHORS:
            need(pins[key]["sha256"] == ANCHORS[key], "EXACT_ADOPTED_RECORD:" + key)
    output = Path(config["output"])
    need(output == HERE / "bounded-parse-pc-attribution-01/attribution"
         and output.resolve() == output and output.parent.is_dir() and not output.exists(), "FRESH_OUTPUT")
    output.mkdir()
    report = {"schema": "DMKN_BOUNDED_PARSE_ATTRIBUTION_RESULT_V1", "status": "FAIL_OFFLINE_ATTRIBUTION",
        "guest_executions": 0, "proof_calls": 0, "compiler_calls": 0, "subprocess_calls": 0,
        "mathematical_admission": False, "measurement": h.MEASUREMENT}
    code = 1
    try:
        records = {key: h.parse(bind(pin, 8*MIB if key in ("diagnostic", "baseline_report") else 2*MIB))
                   for key, pin in pins.items()}
        build, attempt, artifact = (records[key] for key in ("build_result", "build_attempt", "artifact"))
        assembly, asm_command = records["assembly_result"], records["assembly_command"]
        execution, command, diag = (records[key] for key in ("screen_result", "screen_command", "diagnostic"))
        need(build["schema"] == "DMKN_V5_BOUNDED_PARSE_DIRECT_PROJECT_BUILD_RESULT_V1"
             and build["status"] == "PASS_BOUNDED_PARSE_THREE_PROJECT_COMPILES_ONLY"
             and build["compiler_calls"] == 3 and build["job"]["active_processes"] == 0
             and build["job"]["terminated_processes"] == 0
             and attempt == {"result_sha256": pins["build_result"]["sha256"], "status": build["status"]},
             "ADOPTED_DIRECT_BUILD_LINEAGE")
        need(assembly["schema"] == "DMKN_V5_BOUNDED_PARSE_IMAGE_ASSEMBLY_RESULT_V1"
             and assembly["status"] == "PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY"
             and assembly["guest_build_result"] == pins["build_result"]
             and assembly["artifact_record"] == pins["artifact"] and assembly["image_id"] == A
             and assembly["assembler_calls"] == 1 and assembly["guest_executions"] == assembly["proof_calls"] == 0
             and assembly["mathematical_admission"] is False, "CURRENT_ASSEMBLY_LINEAGE")
        closed(records["assembly_outer"], 0); closed(records["screen_outer"], 1)
        need(asm_command["authority"] == "ASSEMBLY_ONLY_NOT_ADMISSION" and asm_command["cwd"] == str(ROOT)
             and asm_command["guest_result_sha256"] == pins["build_result"]["sha256"]
             and pins["source_map"] in asm_command["selected_inputs"], "CURRENT_ASSEMBLY_SOURCE_MAP")
        need(build["outputs"]["dmkn-aggregate-claim-guest"] == artifact["user_elf"], "BUILD_EXACT_ELF")
        elf, link_map = bind(artifact["user_elf"], 64*MIB), bind(artifact["link_map"], 8*MIB)
        need(artifact["user_elf"]["sha256"] == "16b7f1a26bcabdf95bf6cd85da1c0f8e6cd6c8647c2b7b049c65c7332f0fc701"
             and artifact["link_map"]["sha256"] == "b200d6322acfad9ab454f5fddbfb90dc08d1e476f3282b53956ab9a34e9f4581",
             "EXACT_NEW_ELF_AND_MAP")
        headers, executable = h.elf_headers(elf)
        need(headers == artifact["elf_headers"] and asm_command["argv"][1:] == ["assemble",
             artifact["user_elf"]["path"], asm_command["argv"][3], assembly["image"]["path"]], "ELF_ASSEMBLY_BINDING")
        bind(assembly["image"], 64*MIB)
        need(assembly["image"]["sha256"] == "e3ec2dbb7742bf6de81ebd0d226bd08f88d63c91e1658fdf262510c296857822"
             and diag["aggregate_image"] == execution["aggregate_image"] == A
             and diag["elf_sha256"] == assembly["image"]["sha256"]
             and execution["schema"] == "DMKN_AGGREGATE_COST_SCREEN_RESULT_V1"
             and execution["status"] == "FAIL" and execution["host_calls"] == 1
             and execution["proof_calls"] == 0 and execution["mathematical_admission"] is False
             and execution["diagnostic"] == pins["diagnostic"], "FAILED_SCREEN_EXACT_IMAGE")
        argv = command["argv"]
        need(type(argv) is list and len(argv) == 13 and argv[1:4] == ["snapshot", A, assembly["image"]["path"]]
             and argv[6:9] == [str(2**25), "18", "pc-samples"] and argv[10] == pins["diagnostic"]["path"]
             and argv[11] == "1" and command["authority"] == "ONE_GUEST_COST_SCREEN_NO_PROOF_OR_ADMISSION"
             and diag["cycles_cap"] == execution["cycles"] == 2**25
             and diag["segment_po2"] == execution["segment_po2"] == 18
             and diag["status"] == "FAILED_NO_ACCEPTED_CAPSULE" and diag["result"] is None
             and diag["session_stats"] is None and not Path(argv[9]).exists(), "PREFIX_NOT_CAPSULE")
        wire = bind({"path": argv[4], "bytes": diag["wire_bytes"], "sha256": diag["wire_sha256"]}, 16*MIB)
        need(type(diag["header"]) is list and len(diag["header"]) == 192
             and all(type(b) is int and 0 <= b <= 255 for b in diag["header"]), "HEADER_BYTE_LIST")
        header = bytes(diag["header"])
        bind({"path": argv[5], "bytes": 192, "sha256": hashlib.sha256(header).hexdigest()}, 192)
        need(header[:12] == b"DMKNA002\x02\0\0\0" and wire[:12] == b"DMKNAI02\x02\0\0\0"
             and header[12:44] == wire[12:44] == bytes.fromhex(A), "CURRENT_V2_STATEMENT")
        need(len(diag["parents"]) == 1, "ONE_RETAINED_PARENT")
        parent = {key: diag["parents"][0][key] for key in ("path", "bytes", "sha256")}
        need(parent["path"] == argv[12] and parent["sha256"] ==
             "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47", "EXACT_RETAINED_I_RECEIPT")
        bind(parent, 64*MIB)
        samples, per_pc = h.sample_cells(diag)
        intervals, _labels, parse_counts = h.map_intervals(link_map, executable)
        attribution = h.attribute(intervals, executable, per_pc)
        baseline = records["baseline_report"]
        need(baseline["schema"] == "DMKN_PC_ATTRIBUTION_RESULT_V1"
             and baseline["status"] == "PASS_PC_SAMPLE_ATTRIBUTION_ONLY"
             and baseline["execution_extent"] == "FAILED_EXECUTION_PREFIX_ONLY"
             and baseline["measurement"] == h.MEASUREMENT, "ADOPTED_BASELINE_REPORT_ONLY")
        report.update(status="PASS_OFFLINE_PREFIX_ATTRIBUTION_ONLY", aggregate_image=A,
            diagnostic_error=diag["error"], current_execution_status=execution["status"],
            current_extent="FAILED_EXECUTION_PREFIX_ONLY_NO_COMPLETE_CAPSULE", phases=diag["phases"],
            retained_segment_count=len(diag["retained_segments"]), retained_segment_bytes=diag["retained_segment_bytes"],
            current=summarize(samples, attribution, intervals),
            previous=summarize(baseline["samples"], baseline["attribution"], baseline["intervals"]),
            source_manifest=pins["source_map"], map_parse_counts=parse_counts,
            helper={"path": str(helper), "bytes": len(helper_raw), "sha256": HELPER_SHA},
            limitations=["Both records describe failed prefixes, not matched completed workloads.",
                "Windows are SDK reported row-point bins, not session/proof cycles, instructions or equal wall-time intervals.",
                "The two runs' PCs/windows are not aligned semantic phases; no speedup ratio is computed.",
                "Periodic deterministic instruction sampling may alias loops.",
                "Saturation drops new window/PC pairs while old pairs can grow; omitted events have no stored category/window.",
                "For each global retained category H and omitted total O, all sampled-event count lies in [H,H+O]. Bounds share one missing pool.",
                "Symbol bounds count unique-attribution labels, not all PCs inside potentially overlapping ranges; ambiguous labels stay separate.",
                "Symbol ranges exclude caller-inclusive costs; trait names may remain unclassified by unchanged coarse_class.",
                "A missing named symbol is not evidence its operation or inlined work disappeared.",
                "Host phases are wall durations; no proof-time, cycle or full-cost fraction is inferred."])
        for key in ("build_result", "assembly_result", "assembly_outer", "screen_result", "screen_outer"):
            need(not (Path(pins[key]["path"]).parent / "FINALIZATION-FAILED.json").exists(), "FAILURE_OVERRIDE_PRESENT")
        for pin in list(bound.values()):
            bind(pin, pin["bytes"])
        with helper.open("rb") as stream:
            need(hashlib.sha256(stream.read(25116)).hexdigest() == HELPER_SHA, "HELPER_CHANGED")
        code = 0
    except Exception as error:
        report.update(status="FAIL_OFFLINE_ATTRIBUTION", error=type(error).__name__ + ": " + str(error)[:2000])
    report["bound_files"] = bound
    raw = (json.dumps(report, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()
    need(len(raw) <= 16*MIB, "OUTPUT_REPORT_BOUND")
    with (output / "RESULT.json").open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    print(json.dumps({"status": report["status"], "output": str(output), "guest_executions": 0, "proof_calls": 0}))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

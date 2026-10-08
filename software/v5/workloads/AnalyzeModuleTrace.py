"""Offline interpretation of retained capped trace01; never reruns the VM.

Pinned SDK emits weighted row points in TraceEvent.cycle (5040 points/row).
The original sampler's 2^20-unit windows can therefore be grouped in sets of
5040 to obtain windows of 2^20 row-equivalents. This does not recover unsampled
instructions, inclusive call stacks, complete execution cost or proof timings.
"""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from TraceModuleScreen import ROOT, need, read_pin, save, elf_symbols, attribute


def main():
    need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "CANONICAL_ISOLATED_INVOCATION")
    parser = argparse.ArgumentParser()
    for name in ("trace", "elf"):
        parser.add_argument("--"+name, required=True)
        parser.add_argument("--"+name+"-sha", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    raw_trace = read_pin(args.trace, args.trace_sha)
    elf = read_pin(args.elf, args.elf_sha)
    profile = json.loads(raw_trace)
    need(profile["schema"] == "DMKN_EXECUTION_PC_SAMPLE_V1"
         and profile["outcome"] == "EXECUTION_ERROR_PARTIAL_SAMPLES"
         and "diagnostic sample cell bound" in profile["execution_error"]
         and profile["sample_limit_hit"] is True
         and profile["mathematical_admission"] is False and profile["proof_calls"] == 0
         and profile["completed_execution"] is None, "EXACT_RETAINED_PARTIAL_ERROR")
    need(profile["image_id"] == "d9572ba4c2336c1544cae3fba652cc66f47b70144c4051d3a57dd2e25af161bb"
         and profile["cycle_ceiling"] == 2**25 and profile["segment_po2"] == 18
         and profile["sample_stride"] == 256 and profile["sample_window_cycles"] == 2**20
         and profile["sample_cell_limit"] == 131072 and len(profile["samples"]) == 131072
         and profile["backwards_cycle_events"] == 0, "EXACT_PARTIAL_SAMPLING_PROFILE")
    need(profile["samples_observed"] == (profile["instructions_observed"]+255)//256 - 1
         == sum(row[2] for row in profile["samples"]), "CENSUS_INCLUDES_ONE_REFUSED_SAMPLE_ATTEMPT")
    need(profile["input_sha256"] == "6953baee3af4cababe4e72b651dbe07631f22189e83ff3a7c708c9a7eebc562d"
         and profile["expected_journal_sha256"] == "18d6f4837b81681649f0b80046be2a9510d32019e8508190bb799d466c3344d5",
         "EXACT_OLD_INPUT_BINDING")
    out = Path(args.output)
    need(out.is_absolute() and out.resolve() == out and out.is_relative_to(ROOT / "experiments/v5-local-checks")
         and not out.exists(), "FRESH_ANALYSIS_OUTPUT")
    points_per_row = 5040
    grouped = Counter()
    for window, pc, count in profile["samples"]:
        need(type(window) is int and window >= 0 and type(pc) is int and 0 <= pc < 2**32
             and type(count) is int and count > 0, "SAMPLE_ROW_BOUNDS")
        grouped[window // points_per_row, pc] += count
    report = attribute({"samples": [[w,p,n] for (w,p),n in sorted(grouped.items())]}, elf_symbols(elf))
    for row in report["windows"]:
        row["row_equivalent_window"] = row.pop("reported_cycle_window")
    report.update(schema="DMKN_OFFLINE_PARTIAL_TRACE_ANALYSIS_V1", status="ANALYZED_RETAINED_PARTIAL_TRACE",
                  guest_executions=0, proof_calls=0, mathematical_admission=False,
                  input_trace_sha256=args.trace_sha, input_elf_sha256=args.elf_sha,
                  execution_stopped="DIAGNOSTIC_SAMPLE_CELL_LIMIT_NOT_SUCCESS_NOT_SESSION_LIMIT",
                  instructions_observed=profile["instructions_observed"],
                  trace_reported_units="SDK_WEIGHTED_ROW_POINTS_NOT_INSTRUCTION_CYCLES",
                  points_per_row=points_per_row, row_equivalent_window_size=2**20,
                  reported_row_points=profile["max_reported_cycle"],
                  limits="PARTIAL_PREFIX_ONLY;DETERMINISTIC_ALIASING;NO_INCLUSIVE_CALL_STACK_OR_PROOF_TIME")
    need(report["sample_total"] == profile["samples_observed"], "ATTRIBUTION_CENSUS")
    read_pin(args.trace, args.trace_sha); read_pin(args.elf, args.elf_sha)
    out.mkdir()
    save(out / "RESULT.json", report)
    print(json.dumps({"status":report["status"], "samples":report["sample_total"],
                      "top_functions":report["all_function_samples"][:12]}))


if __name__ == "__main__":
    main()

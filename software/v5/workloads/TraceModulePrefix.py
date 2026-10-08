"""One pinned new-image, bounded-prefix diagnostic; not acceptance or a proof.

Reuses the already linked host and prepared input. A sampler-cell stop is useful
diagnostic evidence, explicitly not completed checking. SDK cycle counters use
weighted row points, not instruction cycles or padded proof rows.
"""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from TraceModuleScreen import ROOT, MAX_BYTES, need, read_pin, save, elf_symbols, attribute


def interpret(profile, image_id, frame_sha, journal_sha, symbols):
    need(profile["schema"] == "DMKN_EXECUTION_PC_SAMPLE_V1"
         and profile["mathematical_admission"] is False and profile["proof_calls"] == 0
         and profile["image_id"] == image_id and profile["cycle_ceiling"] == 2**25
         and profile["segment_po2"] == 18 and profile["sample_stride"] == 256
         and profile["sample_window_cycles"] == 2**20 and profile["sample_cell_limit"] == 131072
         and profile["backwards_cycle_events"] == 0, "EXACT_DIAGNOSTIC_PROFILE")
    need(profile["input_sha256"] == frame_sha and profile["expected_journal_sha256"] == journal_sha,
         "EXACT_PREPARED_INPUTS")
    instructions = profile["instructions_observed"]
    rows = profile["samples"]
    need(type(instructions) is int and instructions > 0 and type(rows) is list
         and 0 < len(rows) <= 131072 and type(profile["max_reported_cycle"]) is int
         and profile["max_reported_cycle"] >= 0, "BOUNDED_SAMPLE_PROFILE")
    hit = profile["sample_limit_hit"]
    need(type(hit) is bool, "EXACT_STOP_FLAG")
    error = profile["execution_error"]
    if hit:
        need(profile["outcome"] == "EXECUTION_ERROR_PARTIAL_SAMPLES"
             and profile["completed_execution"] is None and len(rows) == 131072
             and type(error) is str and "diagnostic sample cell bound" in error
             and (instructions - 1) % 256 == 0, "EXACT_SAMPLE_CELL_STOP")
        stop = "SAMPLE_CELL_BOUND_PARTIAL_PREFIX"
    elif profile["outcome"] == "EXECUTION_ERROR_PARTIAL_SAMPLES":
        need(profile["completed_execution"] is None and type(error) is str
             and "Session limit exceeded" in error, "EXPECTED_SESSION_STOP_ONLY")
        stop = "SESSION_BOUND_PARTIAL_PREFIX"
    else:
        need(profile["outcome"] == "EXECUTION_COMPLETED_NO_CERTIFICATE"
             and error is None and type(profile["completed_execution"]) is dict,
             "HOST_CHECKED_COMPLETION")
        stop = "COMPLETED_EXECUTION_NO_CERTIFICATE"
    # The cell-limited callback increments instructions, then refuses exactly
    # one new sample. All other terminal paths use the ordinary sample census.
    expected_samples = (instructions + 255) // 256 - int(hit)
    grouped, seen = Counter(), set()
    for row in rows:
        need(type(row) is list and len(row) == 3, "SAMPLE_ROW_SHAPE")
        window, pc, count = row
        need(type(window) is int and 0 <= window <= profile["max_reported_cycle"] >> 20
             and type(pc) is int and 0 <= pc < 2**32 and type(count) is int and count > 0,
             "SAMPLE_ROW_BOUNDS")
        need((window, pc) not in seen, "DISTINCT_SAMPLE_CELLS")
        seen.add((window, pc))
        grouped[window // 5040, pc] += count
    need(profile["samples_observed"] == expected_samples == sum(grouped.values()), "SAMPLE_CENSUS")
    analysis = attribute({"samples": [[w, pc, n] for (w, pc), n in sorted(grouped.items())]}, symbols)
    need(analysis["sample_total"] == expected_samples, "ATTRIBUTION_CENSUS")
    for row in analysis["windows"]:
        row["row_equivalent_window"] = row.pop("reported_cycle_window")
    analysis.update(schema="DMKN_MODULE_PREFIX_ANALYSIS_V1", execution_stop=stop,
                    trace_reported_units="SDK_WEIGHTED_ROW_POINTS_NOT_INSTRUCTION_CYCLES",
                    points_per_row=5040, row_equivalent_window_size=2**20,
                    reported_row_points=profile["max_reported_cycle"],
                    instructions_observed=instructions,
                    limits="DETERMINISTIC_EXCLUSIVE_SAMPLES;NO_INCLUSIVE_STACK_OR_PROOF_TIMING;PREFIX_IF_STOPPED")
    return analysis


def main():
    need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "CANONICAL_ISOLATED_INVOCATION")
    parser = argparse.ArgumentParser()
    names = ("host", "image", "frame", "journal", "elf", "kernel")
    for name in names:
        parser.add_argument("--" + name, required=True)
        parser.add_argument("--" + name + "-sha", required=True)
    parser.add_argument("--image-id", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(len(args.image_id) == 64 and all(c in "0123456789abcdef" for c in args.image_id), "IMAGE_ID")
    out = Path(args.output)
    need(out.is_absolute() and out.resolve() == out
         and out.is_relative_to(ROOT / "experiments/v5-local-checks") and not out.exists(), "FRESH_OUTPUT")
    held = {name: read_pin(getattr(args, name), getattr(args, name + "_sha"),
                          96*1024**2 if name == "host" else MAX_BYTES) for name in names}
    user_symbols, kernel_symbols = elf_symbols(held["elf"]), elf_symbols(held["kernel"])
    need(user_symbols, "USER_ELF_SYMBOLS_REQUIRED")
    # Preserve overlapping intervals as unknown, including cross-image overlap.
    # Missing kernel function symbols stay unknown; do not infer function names.
    symbols = sorted([(lo, hi, "guest::" + label) for lo, hi, label in user_symbols]
                     + [(lo, hi, "kernel::" + label) for lo, hi, label in kernel_symbols])
    out.mkdir()
    report = {"status": "FAIL", "schema": "DMKN_MODULE_PREFIX_DIAGNOSTIC_V1",
              "mathematical_admission": False, "proof_calls": 0, "guest_executions": 0,
              "image_id": args.image_id, "cycle_ceiling": 2**25, "segment_po2": 18,
              "inputs": {name: getattr(args, name + "_sha") for name in names},
              "user_function_symbols": len(user_symbols), "kernel_function_symbols": len(kernel_symbols)}
    try:
        argv = [args.host, "trace", args.image, args.frame, args.journal,
                str(2**25), "18", str(out / "trace.json")]
        environment = {key: value for key, value in os.environ.items() if not key.upper().startswith("RISC0_")}
        report["guest_executions"] = 1
        with (out / "host.stdout").open("xb") as stdout, (out / "host.stderr").open("xb") as stderr:
            call = subprocess.run(argv, cwd=ROOT, env=environment, stdout=stdout, stderr=stderr,
                                  timeout=180, check=False)
        report["host_exit_code"] = call.returncode
        need(all((out / name).stat().st_size <= 2**20 for name in ("host.stdout", "host.stderr")), "LOG_BOUND")
        need(call.returncode == 0, "DIAGNOSTIC_HOST_COLLECTION_FAILURE")
        trace_path = out / "trace.json"
        need(trace_path.stat().st_size <= MAX_BYTES, "TRACE_BYTE_BOUND")
        trace = trace_path.read_bytes()
        profile = json.loads(trace)
        analysis = interpret(profile, args.image_id, args.frame_sha, args.journal_sha, symbols)
        save(out / "attribution.json", analysis)
        report.update(status="DIAGNOSTIC_COLLECTED_NOT_CERTIFIED", execution_stop=analysis["execution_stop"],
                      execution_error=profile["execution_error"], completed_execution=profile["completed_execution"],
                      sample_total=analysis["sample_total"], top_functions=analysis["all_function_samples"][:15],
                      trace_sha256=hashlib.sha256(trace).hexdigest())
    except BaseException as error:
        report.update(status="FAIL", error={"type": type(error).__name__, "message": str(error)[:2000]})
    for name in names:
        read_pin(getattr(args, name), getattr(args, name + "_sha"), 96*1024**2 if name == "host" else MAX_BYTES)
    save(out / "RESULT.json", report)
    print(json.dumps({key: report.get(key) for key in ("status", "execution_stop", "sample_total", "error")}))
    return int(report["status"] == "FAIL")


if __name__ == "__main__":
    raise SystemExit(main())

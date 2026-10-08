"""One bounded old-image execution with partial PC samples, never a proof.

Maps deterministic samples to exact retained ELF symbol intervals. Missing or
overlapping intervals remain unattributed. No source-line/inclusive-stack or
proof-cycle attribution is invented. Root selects exact paths, pins and limits.
"""
from bisect import bisect_right
from collections import Counter, defaultdict
from pathlib import Path
import argparse
import hashlib
import json
import os
import struct
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MAX_BYTES = 16 * 1024**2


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read_pin(path, digest, limit=MAX_BYTES):
    path = Path(path)
    need(path.is_absolute() and path.is_file() and path.stat().st_size <= limit, "BOUNDED_INPUT")
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    need(len(raw) <= limit and hashlib.sha256(raw).hexdigest() == digest, "EXACT_INPUT_PIN")
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    need(len(raw) <= MAX_BYTES, "DIAGNOSTIC_OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def elf_symbols(raw):
    need(len(raw) >= 52 and raw[:7] == b"\x7fELF\x01\x01\x01", "ELF32_LITTLE_ENDIAN")
    need(struct.unpack_from("<H", raw, 18)[0] == 243, "RISCV_ELF")
    section_offset = struct.unpack_from("<I", raw, 32)[0]
    entry_size, count = struct.unpack_from("<HH", raw, 46)
    need(entry_size == 40 and 0 < count <= 4096, "BOUNDED_ELF_SECTIONS")
    need(section_offset + entry_size * count <= len(raw), "ELF_SECTION_BOUNDS")
    sections = [struct.unpack_from("<10I", raw, section_offset + i * 40) for i in range(count)]

    def section_data(section):
        offset, size = section[4:6]
        need(offset + size <= len(raw), "ELF_SECTION_DATA_BOUNDS")
        return raw[offset:offset + size]

    symbols = set()
    for section in sections:
        if section[1] != 2:
            continue
        need(section[9] == 16 and section[5] % 16 == 0 and section[6] < count,
             "ELF_SYMBOL_TABLE_SHAPE")
        table, strings = section_data(section), section_data(sections[section[6]])
        need(len(table) // 16 <= 100000, "ELF_SYMBOL_COUNT")
        for offset in range(0, len(table), 16):
            name, value, size, info, _, target = struct.unpack_from("<IIIBBH", table, offset)
            if info & 15 != 2 or size == 0 or target == 0 or target >= count:
                continue
            need(name < len(strings) and value + size <= 2**32, "ELF_SYMBOL_BOUNDS")
            end = strings.find(b"\0", name)
            need(end >= name and end-name <= 4096, "ELF_SYMBOL_NAME_BOUND")
            symbols.add((value, value + size, strings[name:end].decode("utf-8", "strict")))
    return sorted(symbols)


def attribute(profile, symbols):
    # Sweep all function intervals once. Each sampled PC maps only when exactly
    # one symbol interval contains it; overlapping aliases are not double-counted.
    events = defaultdict(list)
    for index, (start, end, _) in enumerate(symbols):
        events[start].append((index, True)); events[end].append((index, False))
    positions, owners, active = [], [], set()
    for pc, changes in sorted(events.items()):
        for index, add in changes:
            (active.add if add else active.discard)(index)
        positions.append(pc)
        owners.append(next(iter(active)) if len(active) == 1 else -1)
    totals, windows = Counter(), defaultdict(Counter)
    for window, pc, count in profile["samples"]:
        slot = bisect_right(positions, pc) - 1
        symbol = owners[slot] if slot >= 0 else -1
        label = symbols[symbol][2] if symbol >= 0 else "UNATTRIBUTED_OR_OVERLAPPING"
        totals[label] += count; windows[window][label] += count
    return {"elf_function_symbols": len(symbols),
            "sample_total": sum(totals.values()),
            "all_function_samples": totals.most_common(),
            "windows": [{"reported_cycle_window": window, "sample_total": sum(values.values()),
                         "top_functions": values.most_common(12)} for window, values in sorted(windows.items())],
            "meaning": "EXCLUSIVE_DETERMINISTIC_INSTRUCTION_SAMPLES_NOT_CYCLE_TIME_OR_INCLUSIVE_CALL_COST"}


def main():
    need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "CANONICAL_ISOLATED_INVOCATION")
    parser = argparse.ArgumentParser()
    for name in ("host", "image", "frame", "journal", "elf"):
        parser.add_argument("--" + name, required=True)
        parser.add_argument("--" + name + "-sha", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output)
    need(out.is_absolute() and out.resolve() == out and out.is_relative_to(ROOT / "experiments/v5-local-checks")
         and not out.exists(), "FRESH_CANONICAL_OUTPUT")
    held = {}
    for name in ("host", "image", "frame", "journal", "elf"):
        held[name] = read_pin(getattr(args, name), getattr(args, name + "_sha"),
                              96*1024**2 if name == "host" else MAX_BYTES)
    symbols = elf_symbols(held["elf"])
    need(symbols, "NO_SYMBOLS_FOR_DISCRIMINATING_DIAGNOSTIC")
    out.mkdir()
    report = {"status": "FAIL", "schema": "DMKN_MODULE_TRACE_SCREEN_V1",
              "mathematical_admission": False, "proof_calls": 0, "guest_executions": 0,
              "cycle_ceiling": 2**25, "inputs": {name: getattr(args, name+"_sha") for name in held}}
    try:
        argv = [args.host, "trace", args.image, args.frame, args.journal, str(2**25), "18", str(out / "trace.json")]
        environment = os.environ.copy()
        for key in list(environment):
            if key.upper().startswith("RISC0_"):
                del environment[key]
        report["guest_executions"] = 1
        call = subprocess.run(argv, cwd=ROOT, env=environment, capture_output=True, timeout=180, check=False)
        need(len(call.stdout) <= 2**20 and len(call.stderr) <= 2**20, "HOST_LOG_BOUND")
        with (out / "host.stdout").open("xb") as stream:
            stream.write(call.stdout)
        with (out / "host.stderr").open("xb") as stream:
            stream.write(call.stderr)
        report["host_exit_code"] = call.returncode
        need(call.returncode == 0, "DIAGNOSTIC_HOST_COLLECTION_FAILURE")
        trace_path = out / "trace.json"
        need(trace_path.stat().st_size <= MAX_BYTES, "TRACE_BYTE_CAP")
        profile = json.loads(trace_path.read_bytes())
        need(profile["schema"] == "DMKN_EXECUTION_PC_SAMPLE_V1" and profile["mathematical_admission"] is False
             and profile["proof_calls"] == 0 and profile["cycle_ceiling"] == 2**25
             and profile["segment_po2"] == 18 and profile["sample_stride"] == 256
             and profile["sample_cell_limit"] == 131072, "EXACT_DIAGNOSTIC_PROFILE")
        need(profile["input_sha256"] == args.frame_sha and profile["expected_journal_sha256"] == args.journal_sha,
             "DIAGNOSTIC_INPUT_BINDING")
        need(profile["image_id"] == "d9572ba4c2336c1544cae3fba652cc66f47b70144c4051d3a57dd2e25af161bb",
             "EXACT_FAILED_GUEST_IMAGE")
        need(not profile["sample_limit_hit"] and len(profile["samples"]) <= 131072
             and profile["instructions_observed"] > 0 and profile["backwards_cycle_events"] == 0,
             "USABLE_BOUNDED_DIAGNOSTIC")
        need(profile["samples_observed"] == (profile["instructions_observed"] + 255)//256
             == sum(row[2] for row in profile["samples"]), "SAMPLE_CENSUS")
        attributed = attribute(profile, symbols)
        save(out / "attribution.json", attributed)
        report.update(status="PARTIAL_DIAGNOSTIC_COLLECTED_NOT_CERTIFIED", execution_outcome=profile["outcome"],
                      execution_error=profile["execution_error"], completed_execution=profile["completed_execution"],
                      sample_total=attributed["sample_total"], top_functions=attributed["all_function_samples"][:15],
                      trace_sha256=hashlib.sha256(trace_path.read_bytes()).hexdigest())
    except BaseException as error:
        report.update(status="FAIL", error={"type":type(error).__name__, "message":str(error)[:2000]})
    for name in held:
        read_pin(getattr(args, name), getattr(args, name + "_sha"), 96*1024**2 if name == "host" else MAX_BYTES)
    save(out / "RESULT.json", report)
    print(json.dumps({key: report.get(key) for key in ("status", "execution_outcome", "sample_total", "error")}))
    return 0 if report["status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())

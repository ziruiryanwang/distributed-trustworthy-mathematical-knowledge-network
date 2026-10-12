"""One retained-export row-order correction and cold complete-packet admission.

No authoring, snapshot, guest, prover or network is executed. Retained failed
packet remains immutable. This harness is not a mathematical checker.
"""
from pathlib import Path
import argparse
import math
import os
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from admission.bindings import journal
from admission.verifier import ReceiptVerifier
from delta.actual import ROOT, BASE, IMAGE, FOUNDATION, POLICY, read_pin, save, sha
from delta.author_actual import inspect_reuse
from delta.receiver import DeltaVerifier
from delta.reprepare import reprepare_retained_export
from modules import codec as C
from production.producer import parse, encoded, fields, require, uint, file_pin, pin_fields, MIB

SCHEMA = "DMKN_V5_RETAINED_EXPORT_DELTA_REPREPARE_V1"
INPUTS = ("preparation_profile", "packet", "request", "export", "foundation")
OLD_PACKET = "40aac3921a49b144c19cb7310679741abbd82bb7d796f05a5a0beb71ee60649d"
EXPORT = "268681e0e4193badaa073be369ac062b678ef65123d152780182c448c2f902b7"
TARGET = "52c564f87f31082468557df6eed0a04bc7adf9d28d9614fe6cf173f5633088bf"
FIRST = "4adbc049e4d1e29ec045d64c7dba9e27bdd506dfa6c7fb707f022be40439e742"


def run(config_path, expected_hash):
    started, cpu = time.monotonic(), time.process_time()
    require(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
            and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
            "REPREPARE_OWNER_INVOCATION")
    path = Path(config_path)
    require(path.is_absolute() and path.resolve() == path and path.stat().st_size <= MIB,
            "REPREPARE_CONFIG_PATH")
    raw = path.read_bytes(); require(sha(raw) == expected_hash, "REPREPARE_CONFIG_PIN")
    config = parse(raw)
    fields(config, ("schema", *INPUTS, "native_executable", "runtime_pins", "output_directory",
                    "wall_seconds", "call_limits"))
    require(config["schema"] == SCHEMA, "REPREPARE_CONFIG_SCHEMA")
    uint(config["wall_seconds"], 600, 1); deadline = started+config["wall_seconds"]
    def remaining():
        n = math.floor(deadline-time.monotonic())
        require(n >= 1, "REPREPARE_ORIGINAL_DEADLINE"); return n
    limits = config["call_limits"]
    fields(limits, ("native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds", "memory_mib"))
    for key in ("native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds"): uint(limits[key], 120, 1)
    uint(limits["memory_mib"], 2048, 64)
    inputs = {name: read_pin(config[name]) for name in INPUTS}
    require(sha(inputs["packet"]) == OLD_PACKET and sha(inputs["export"]) == EXPORT,
            "REPREPARE_ACTUAL_RETAINED_ARTIFACTS")
    profile = parse(inputs["preparation_profile"])["producer"]
    require((profile["image_id"], profile["foundation"], profile["policy"])
            == (IMAGE, FOUNDATION, POLICY), "REPREPARE_ADOPTED_PROFILE")
    rows = config["runtime_pins"]
    require(type(rows) is list and 1 <= len(rows) <= 128, "REPREPARE_RUNTIME_COUNT")
    runtime = {}
    for row in rows:
        p = pin_fields(row)
        require(p.resolve() == p and str(p) not in runtime and file_pin(p) == row, "REPREPARE_RUNTIME_PIN")
        runtime[str(p)] = {k: row[k] for k in ("bytes", "sha256")}
    source_root = Path(__file__).resolve().parents[1]
    require({str(Path(__file__).resolve()), str(source_root/"delta/reprepare.py"),
             str(source_root/"delta/actual.py"), str(source_root/"delta/author_actual.py"),
             str(source_root/"authoring/receipt_integration.py")} <= set(runtime)
            and config["native_executable"] in rows, "REPREPARE_HELPER_PINS")
    output = Path(config["output_directory"])
    require(output.is_absolute() and output.resolve() == output and not output.exists()
            and output.parent.is_dir() and output.is_relative_to(ROOT/"experiments/v5-local-checks"),
            "REPREPARE_FRESH_OUTPUT")
    protected = [path, source_root, Path(profile["supervisor_manifest"]["path"]).parent,
                 *(pin_fields(config[k]) for k in INPUTS), *map(Path, runtime)]
    require(all(not output.is_relative_to(p) and not p.is_relative_to(output) for p in protected),
            "REPREPARE_OUTPUT_OVERLAP")
    remaining(); output.mkdir(); save(output/"configuration.json", config)
    frontier = receiver = None
    result = {"schema": SCHEMA, "status": "FAIL", "configuration_sha256": expected_hash,
              "error": None, "author_calls": 0, "guest_calls": 0, "proof_calls": 0, "network_calls": 0,
              "authority": "LOCAL_OPERATION_EVIDENCE_NOT_PORTABLE_AUTHORITY"}
    try:
        prepared = reprepare_retained_export(inputs["foundation"], inputs["request"],
                                             inputs["export"], inputs["packet"])
        before, after = C.parse_json(inputs["packet"]), C.parse_json(prepared)
        old_rows, new_rows = before["deltas"][-1].pop("rows"), after["deltas"][-1].pop("rows")
        require(before == after and old_rows != new_rows, "REPREPARE_ONLY_ROWS_CHANGED")
        full = C.parse_json(prepared); summary = C.summarize(full["deltas"][-1]["local_spec"])
        require(C.summary_id(summary) == TARGET and len(full["frontiers"]) == 1
                and len(full["deltas"]) == 2, "REPREPARE_SAME_TWO_DELTA_TARGET")
        result["reuse"] = inspect_reuse(inputs["export"], inputs["request"],
                                        {"packet": prepared, "local_module": TARGET})
        with (output/"delta-packet.json").open("xb") as stream:
            stream.write(prepared); stream.flush(); os.fsync(stream.fileno())
        result["prepared"] = {"packet": file_pin(output/"delta-packet.json"), "module": TARGET,
                              "summary": summary, "mathematical_acceptance": False,
                              "only_rows_changed": True, "relation_rows": len(new_rows)}
        receipt_runtime = {row["path"]: {k: row[k] for k in ("bytes", "sha256")}
            for row in (profile["host"], profile["python"], profile["python_dll"], *profile["runtime_pins"])}
        receipt_size = len(bytes.fromhex(full["frontiers"][0]["receipt_hex"]))
        frontier = ReceiptVerifier(supervisor_manifest=profile["supervisor_manifest"]["path"],
            supervisor_manifest_sha256=profile["supervisor_manifest"]["sha256"],
            executable=profile["host"]["path"], runtime_pins=receipt_runtime, image_id=IMAGE,
            foundation=FOUNDATION, policy=POLICY, operations=1, submitted_bytes=receipt_size,
            reserved_cpu_seconds=limits["receipt_cpu_seconds"], wall_seconds=remaining())
        receiver = DeltaVerifier(frontier, native_executable=config["native_executable"]["path"],
            runtime_pins=runtime, output_directory=output/"cold-recipient", operations=1,
            submitted_bytes=len(prepared), reserved_cpu_seconds=limits["receipt_cpu_seconds"]+2*limits["native_cpu_seconds"],
            controller_cpu_seconds=120, wall_seconds=remaining(), output_bytes=64*MIB, output_entries=256)
        handle = receiver.receive(prepared, summary, **{**limits, "wall_seconds": min(limits["wall_seconds"], remaining())})
        live = receiver.describe(handle)
        require(live["module"] == TARGET and journal(live["journal"])["rank"] == 2
                and {item["module"] for item in receiver.members(handle)} == {BASE, FIRST, TARGET}
                and receiver.export_packet(handle) == prepared, "REPREPARE_COLD_COMPLETE_AUTHORITY")
        require(receiver.open_group(handle, C.group_opening(full["deltas"][-1]["local_spec"], 0))
                == full["deltas"][-1]["local_spec"]["groups"][0], "REPREPARE_TARGET_OPENING")
        result["cold_conclusion"] = {"module": TARGET, "journal": list(live["journal"]),
                                     "profile_id": live["profile_id"], "packet_sha256": sha(prepared),
                                     "persisted_handle": False}
        for name in INPUTS: require(read_pin(config[name]) == inputs[name], "REPREPARE_INPUT_CHANGED")
        for row in rows: require(file_pin(Path(row["path"])) == row, "REPREPARE_RUNTIME_CHANGED")
        require(path.read_bytes() == raw and read_pin(result["prepared"]["packet"]) == prepared,
                "REPREPARE_FINAL_BYTES")
        remaining(); result["status"] = "PASS_RETAINED_SOURCE_CANONICAL_ROWS_AND_COLD_TWO_DELTA_ADMISSION"
    except BaseException as error:
        result["error"] = {"type": type(error).__name__, "message": str(error)[:4000]}
    finally:
        errors = []
        for owner in (receiver, frontier):
            if owner is not None:
                try: owner.close()
                except BaseException as error: errors.append(str(error)[:1000])
        result["cleanup_errors"] = errors
        result["receiver"] = None if receiver is None else receiver.report()
        result["frontier"] = None if frontier is None else frontier.report()
        result["owner_process_cpu_seconds"] = time.process_time()-cpu
        result["wall_seconds_before_final_report"] = time.monotonic()-started
        result["accounting_scope"] = "ONE_CRYPTO_TWO_NATIVE_MAX;NESTED_CONTROLLER_TIMES_OVERLAP;DO_NOT_ADD_OUTER_JOB_AGAIN"
        if errors or time.monotonic() >= deadline: result["status"] = "FAIL"
        try:
            save(output/"RESULT.json", result); remaining()
        except BaseException as error:
            result.update(status="FAIL", finalization_error={"type": type(error).__name__,
                          "message": str(error)[:2000]})
            save(output/"FINALIZATION-FAILED.json", result)
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument("--config", required=True); p.add_argument("--config-sha256", required=True)
    args = p.parse_args()
    report = run(args.config, args.config_sha256)
    print(encoded({k: report[k] for k in ("status", "error")}).decode(), end="")
    raise SystemExit(0 if report["status"].startswith("PASS_") else 1)

"""One selected real-frontier/native-delta acceptance and changed-boundary check.

Reuses retained ordinary-source child material. No Lean compilation, preparation,
guest execution, proof production, networking or saved-report authority. Root
must separately select the exact runtime, input pins and finite enclosing job.
"""
from pathlib import Path
import argparse
import hashlib
import math
import os
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from admission.bindings import journal
from admission.verifier import ReceiptVerifier, VerifiedModule
from delta.packet import SCHEMA as PACKET_SCHEMA, Envelope, DeltaError
from delta.receiver import DeltaVerifier, VerifiedDelta
from modules import codec as C
from production.producer import (MIB, encoded, parse, fields, require, uint,
                                digest, pin_fields, file_pin)

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SCHEMA = "DMKN_V5_ACTUAL_NATIVE_DELTA_V1"
BASE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
TARGET = "4adbc049e4d1e29ec045d64c7dba9e27bdd506dfa6c7fb707f022be40439e742"
IMAGE = "9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e"
FOUNDATION = "d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481"
POLICY = "5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377"
FIXTURES = {
    "child_input": (113220, "88b71b8282afc99297bf6564d22616fce6211eed9a9e18afa1cb42a41d1206e1"),
    "expected_journal": (184, "07734789fd165d5c29667a2925c09b882d346db97a511c75644f2cb4b8ccd0da"),
    "receipt": (223594, "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"),
}
INPUTS = ("preparation_profile", "child_input", "expected_journal", "receipt", "bundle")
CONFIG = ("schema", *INPUTS, "native_executable", "runtime_pins", "output_directory",
          "wall_seconds", "call_limits")


def sha(raw): return hashlib.sha256(raw).hexdigest()


def read_pin(pin, maximum=16*MIB):
    path = pin_fields(pin, maximum)
    require(path.resolve() == path and path.is_file(), "ACTUAL_CANONICAL_PIN_PATH")
    require(file_pin(path) == pin, "ACTUAL_INPUT_PIN")
    with path.open("rb") as stream: raw = stream.read(maximum+1)
    require(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"], "ACTUAL_READ_PIN")
    return raw


def save(path, value):
    raw = encoded(value)
    require(len(raw) <= 4*MIB, "ACTUAL_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def expect_refusal(name, operation, error_type, message, status=None):
    try: operation()
    except error_type as error:
        require(str(error) == message and (status is None or error.status == status),
                "ACTUAL_WRONG_REFUSAL:"+name+":"+str(error))
        return {"name": name, "reason": str(error), "type": type(error).__name__,
                "status": getattr(error, "status", None)}
    raise ValueError("ACTUAL_UNEXPECTED_ACCEPTANCE:"+name)


def run(config_path, config_sha256):
    started, cpu_started = time.monotonic(), time.process_time()
    digest(config_sha256); config_path = Path(config_path)
    require(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
            and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
            "ACTUAL_OWNER_INVOCATION")
    require(config_path.is_absolute() and config_path.resolve() == config_path
            and config_path.is_file() and 0 < config_path.stat().st_size <= MIB,
            "ACTUAL_CONFIGURATION_PATH")
    with config_path.open("rb") as stream: config_raw = stream.read(MIB+1)
    require(len(config_raw) <= MIB and sha(config_raw) == config_sha256, "ACTUAL_CONFIGURATION_PIN")
    config = parse(config_raw); fields(config, CONFIG)
    require(config["schema"] == SCHEMA, "ACTUAL_CONFIGURATION_SCHEMA")
    uint(config["wall_seconds"], 1800, 1); deadline = started+config["wall_seconds"]
    limits = config["call_limits"]
    fields(limits, ("native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds", "memory_mib"))
    for key in ("native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds"):
        uint(limits[key], 600, 1)
    uint(limits["memory_mib"], 4096, 64)

    def remaining():
        value = math.floor(deadline-time.monotonic())
        require(value >= 1, "ACTUAL_ORIGINAL_WALL")
        return value

    inputs = {name: read_pin(config[name]) for name in INPUTS}
    for name, (size, expected_sha) in FIXTURES.items():
        require(len(inputs[name]) == size and sha(inputs[name]) == expected_sha,
                "ACTUAL_RETAINED_FIXTURE:"+name)
    require(sha(inputs["bundle"]) == "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926",
            "ACTUAL_CURRENT_BASE_BUNDLE")
    producer = parse(inputs["preparation_profile"])["producer"]
    require((producer["image_id"], producer["foundation"], producer["policy"])
            == (IMAGE, FOUNDATION, POLICY), "ACTUAL_ADOPTED_PROFILE")
    runtime_rows = config["runtime_pins"]
    require(type(runtime_rows) is list and 1 <= len(runtime_rows) <= 128, "ACTUAL_PIN_LIST")
    runtime = {}
    for row in runtime_rows:
        path = pin_fields(row)
        require(path.resolve() == path and str(path) not in runtime, "ACTUAL_DISTINCT_CANONICAL_PIN")
        require(file_pin(path) == row, "ACTUAL_RUNTIME_PIN")
        runtime[str(path)] = {key: row[key] for key in ("bytes", "sha256")}
    require(file_pin(Path(__file__).resolve()) in runtime_rows
            and config["native_executable"] in runtime_rows, "ACTUAL_LOADED_HARNESS_AND_NATIVE_PINS")
    native = pin_fields(config["native_executable"])
    bundle = C.parse_json(inputs["bundle"]); child = C.parse_json(inputs["child_input"])
    base_summary = C.summarize(bundle["spec"]); target_summary = C.summarize(child["local_spec"])
    expected = journal(inputs["expected_journal"])
    require(C.summary_id(base_summary) == BASE and C.summary_id(target_summary) == TARGET
            and expected["summary"] == target_summary and expected["rank"] == 1
            and len(child["parents"]) == 1 and len(child["rows"]) == 1355
            and len(child["local_spec"]["groups"]) == 1, "ACTUAL_SELECTED_CHILD")
    require(child["rows"][-1] == {"thm": {"all": [101], "levelParams": [79,86,97],
        "name": 101, "type": 770, "value": 1200}}, "ACTUAL_SELECTED_THEOREM_ROW")
    packet_value = {"schema": PACKET_SCHEMA,
        "frontiers": [{"receipt_hex": inputs["receipt"].hex(), "summary": base_summary}],
        "deltas": [child]}
    packet = C.canonical(packet_value)
    output = Path(config["output_directory"])
    require(output.is_absolute() and output.resolve() == output and output.parent.is_dir()
            and not output.exists() and output.is_relative_to(ROOT/"experiments/v5-local-checks"),
            "ACTUAL_FRESH_OUTPUT")
    protected = [config_path, Path(__file__).resolve().parents[1],
                 Path(producer["supervisor_manifest"]["path"]).parent]
    protected.extend(pin_fields(config[name]) for name in INPUTS)
    protected.extend(pin_fields(row) for row in runtime_rows)
    protected.extend(pin_fields(row) for row in (producer["host"], producer["python"],
                     producer["python_dll"], *producer["runtime_pins"]))
    require(all(not output.is_relative_to(path) and not path.is_relative_to(output)
                for path in protected), "ACTUAL_OUTPUT_OVERLAP")
    remaining(); output.mkdir(); save(output/"configuration.json", config)
    result = {"schema": SCHEMA, "status": "FAIL", "configuration_sha256": config_sha256,
        "child_admitted": False, "child_module": TARGET, "checks": [], "error": None,
        "input_pins": {name: config[name] for name in INPUTS},
        "proof_calls": 0, "guest_calls": 0, "author_calls": 0, "network_calls": 0,
        "authority": "LOCAL_RUN_EVIDENCE_NOT_TRANSFERABLE_MATHEMATICAL_AUTHORITY"}
    verifier, owners = None, []
    try:
        receipt_runtime = {row["path"]: {key: row[key] for key in ("bytes", "sha256")}
            for row in (producer["host"], producer["python"], producer["python_dll"],
                        *producer["runtime_pins"])}
        verifier = ReceiptVerifier(supervisor_manifest=producer["supervisor_manifest"]["path"],
            supervisor_manifest_sha256=producer["supervisor_manifest"]["sha256"],
            executable=producer["host"]["path"], runtime_pins=receipt_runtime,
            image_id=IMAGE, foundation=FOUNDATION, policy=POLICY, operations=1,
            submitted_bytes=len(inputs["receipt"]), reserved_cpu_seconds=limits["receipt_cpu_seconds"],
            wall_seconds=remaining())

        def owner(name, *, envelope=None, operations=1):
            value = DeltaVerifier(verifier, native_executable=str(native), runtime_pins=runtime,
                output_directory=output/name, envelope=envelope, operations=operations,
                submitted_bytes=operations*len(packet),
                reserved_cpu_seconds=operations*(limits["receipt_cpu_seconds"]+limits["native_cpu_seconds"]),
                controller_cpu_seconds=120, wall_seconds=remaining(), output_bytes=64*MIB,
                output_entries=256)
            owners.append((name,value)); return value

        def receive(value, raw):
            return value.receive(raw,target_summary,**{**limits,
                "wall_seconds": min(limits["wall_seconds"],remaining())})

        # New changed-boundary structural refusals; no crypto/native calls here.
        bounded = owner("bounded", envelope=Envelope(packet_bytes=len(packet)-1))
        result["checks"].append(expect_refusal("aggregate_packet_cap", lambda: receive(bounded,packet),
            DeltaError,"PACKET_BYTE_ENVELOPE","NEEDS_SEAL"))
        missing = owner("missing")
        missing_raw = C.canonical({**packet_value,"frontiers":[]})
        result["checks"].append(expect_refusal("missing_real_frontier",lambda: receive(missing,missing_raw),
            DeltaError,"MISSING_OR_FORWARD_PARENT","MISSING_MATERIAL"))
        require(verifier.report()["attempts"] == 0 and
                not any((output/name/"1/native-0").exists() for name in ("bounded","missing")),
                "ACTUAL_PREFLIGHT_ONLY_REFUSALS")

        accepted = owner("accepted", operations=2)
        handle = receive(accepted,packet)
        require(type(handle) is VerifiedDelta and not isinstance(handle,VerifiedModule),
                "ACTUAL_DISTINCT_NATIVE_DELTA_AUTHORITY")
        live = accepted.describe(handle)
        require(live["journal"] == inputs["expected_journal"] and live["module"] == TARGET
                and live["packet_sha256"] == sha(packet), "ACTUAL_COMPUTED_TARGET_JOURNAL")
        opening = C.group_opening(child["local_spec"],0)
        require(accepted.open_group(handle,opening) == child["local_spec"]["groups"][0],
                "ACTUAL_OPENED_TARGET_GROUP")
        members = accepted.members(handle)
        require({item["module"] for item in members} == {BASE,TARGET}
                and len(members) == 2, "ACTUAL_COMPLETE_MEMBER_CLOSURE")
        require(accepted.describe_member(handle,BASE)["proof_form"] == "receipt-frontier"
                and accepted.describe_member(handle,TARGET)["proof_form"] == "native-delta",
                "ACTUAL_DISTINCT_MEMBER_FORMS")
        require(accepted.open_member_group(handle,BASE,bundle["openings"][0])
                == bundle["spec"]["groups"][bundle["openings"][0]["index"]], "ACTUAL_BASE_MEMBER_OPENING")
        exported = accepted.export_packet(handle)
        require(exported == packet, "ACTUAL_COMPLETE_EXACT_ONWARD_PACKET")
        save(output/"accepted-observation.json", {"module":live["module"],"summary":live["summary"],
            "journal":list(live["journal"]),"profile_id":live["profile_id"],
            "packet_sha256":sha(exported),"packet_bytes":len(exported),
            "members":[{"module":item["module"],"proof_form":item["proof_form"]} for item in members],
            "authority":"OBSERVED_LIVE_HANDLE_NOT_SAVED_ACCEPTANCE"})
        result["child_admitted"] = True
        result["checks"].append({"name":"genuine_cold_frontier_native_child_open_members_export","status":"PASS"})
        result["checks"].append(expect_refusal("fabricated_handle",lambda: accepted.describe(VerifiedDelta()),
            DeltaError,"FOREIGN_OR_UNKNOWN_DELTA_HANDLE","INVALID_OR_UNBOUND"))

        # Change only the genuine local theorem proof reference to its type term.
        # The statement/parent remain unchanged. Native checking must reject it;
        # the already verified frontier is reused, never reverified or invented.
        forged = C.parse_json(packet)
        forged["deltas"][0]["rows"][-1]["thm"]["value"] = 770
        forged_packet = C.canonical(forged)
        result["checks"].append(expect_refusal("ill_typed_theorem_witness",lambda: receive(accepted,forged_packet),
            DeltaError,"NATIVE_OR_FRONTIER_REJECTED","INVALID_OR_UNBOUND"))
        require(verifier.report()["attempts"] == 1, "ACTUAL_NO_DUPLICATE_FRONTIER_VERIFICATION")
        negative_process = parse((output/"accepted/2/process-0.json").read_bytes())
        final = negative_process["final_job"]
        require(negative_process["child_exit_code"] not in (None,0)
                and negative_process["direct_child_reaped"] is True
                and negative_process["job_closed"] is True
                and negative_process["cleanup_errors"] == []
                and negative_process["termination_requested"] is False
                and final["active_processes"] == final["terminated_processes"] == 0
                and 0 <= final["cpu_seconds"] <= limits["native_cpu_seconds"],
                "ACTUAL_CLEAN_NATIVE_REFUSAL_NOT_TIMEOUT")
        result["checks"].append(expect_refusal("failed_owner_revokes_prior_handle",lambda: accepted.describe(handle),
            DeltaError,"DELTA_CLOSED_OR_CHANGED_FRONTIER_OWNER","INVALID_OR_UNBOUND"))
        require(accepted.report()["live_handles"] == 0 and accepted.report()["closed"] is True,
                "ACTUAL_FAILED_OWNER_EMPTY")
        result["observed_native_negative_cpu_seconds"] = final["cpu_seconds"]
        for name in INPUTS:
            require(read_pin(config[name]) == inputs[name], "ACTUAL_INPUT_CHANGED")
        for row in runtime_rows: require(file_pin(Path(row["path"])) == row, "ACTUAL_FINAL_RUNTIME_CHANGED")
        require(config_path.read_bytes() == config_raw, "ACTUAL_CONFIGURATION_CHANGED")
        remaining()
        result["status"] = "PASS_REAL_FRONTIER_NATIVE_DELTA_AND_CHANGED_BOUNDARY_REFUSALS"
    except BaseException as error:
        result["error"] = {"type":type(error).__name__,"message":str(error)[:4000]}
    finally:
        result["before_closure"] = {
            "owners": {name:value.report() for name,value in owners},
            "receipt_owner": None if verifier is None else verifier.report()}
        errors = []
        for name,value in [*owners,("frontier",verifier)]:
            if value is not None:
                try: value.close()
                except BaseException as error: errors.append({"owner":name,"error":str(error)[:1000]})
        result["cleanup_errors"] = errors
        result["owners"] = {name:value.report() for name,value in owners}
        result["receipt_owner"] = None if verifier is None else verifier.report()
        if errors: result["status"] = "FAIL"
        result["owner_process_cpu_seconds"] = time.process_time()-cpu_started
        result["wall_seconds_before_final_report"] = time.monotonic()-started
        result["accounting_scope"] = ("ONE_RECEIPT_AND_TWO_NATIVE_WORKERS_AT_MOST;"
            "OWNER_PROCESS_CPU_DISJOINT;DELTA_REPORT_OBSERVED_SUCCESS_WORKER_IS_PARTIAL;"
            "FAILED_NATIVE_JOB_RETAINED_SEPARATELY;DO_NOT_ADD_ENCLOSING_INCLUSIVE_JOB_AGAIN")
        if time.monotonic() >= deadline: result.update(status="FAIL",late_deadline=True)
        try:
            save(output/"RESULT.json",result); remaining()
        except BaseException as error:
            result.update(status="FAIL",finalization_error={"type":type(error).__name__,"message":str(error)[:2000]})
            save(output/"FINALIZATION-FAILED.json",result)
    return result


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--config",required=True); parser.add_argument("--config-sha256",required=True)
    args = parser.parse_args()
    try:
        result = run(args.config,args.config_sha256)
        print(encoded({key:result.get(key) for key in ("status","child_admitted","error")}).decode(),end="")
        return 0 if result["status"].startswith("PASS_") else 1
    except BaseException as error:
        print(encoded({"status":"FAIL_CONFIGURATION_OR_REPORT","type":type(error).__name__,
                       "message":str(error)[:4000]}).decode(),end="",file=sys.stderr)
        return 1


if __name__ == "__main__": raise SystemExit(main())

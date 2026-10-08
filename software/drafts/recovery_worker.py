"""DRAFT: owner-local recovery of one interrupted, native-free peer request.

Not integrated, executed, or qualified. This worker neither allocates a stage nor
imports the checker/peer modules. Use only through future reviewed supervision.
The original supervisor receipt is trusted owner-local evidence, not a peer
certificate. Current source pins must still equal the original source cut.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import sys
import time

INSTALL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(INSTALL / "py"))

from domains import Domains, PYTHON_FLAGS, require_python_profile
from node import SAFE_ID, load_config, request as parse_node_request
from storage import ControlStore, Refusal, decode, digest, encode, owner_lock, read, require

MIB = 1048576
PEER_OPERATIONS = {"peer_find", "peer_acquire", "expose"}
SOURCE_NAMES = ("node", "run_stage", "storage", "checking", "domains", "supervise",
                "peer_wire", "peer_service", "peer_node")
SHA256 = re.compile(r"[a-fA-F0-9]{64}\Z")
INTERRUPTED = encode({"status": "REFUSED", "code": "INTERRUPTED_PEER_OPERATION"})


def fields(value, required, optional=()):
    require(type(value) is dict and set(required) <= set(value)
            <= set(required) | set(optional), "RECOVERY_FIELDS")


def strict_receipt_json(raw):
    """Receipts contain timing floats; reject duplicates/nonfinite values."""
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "RECOVERY_JSON_DUPLICATE")
            result[key] = value
        return result

    def finite(value):
        number = float(value)
        require(math.isfinite(number), "RECOVERY_JSON_NONFINITE")
        return number

    def nonfinite(_value):
        raise Refusal("RECOVERY_JSON_NONFINITE")

    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                          parse_float=finite, parse_constant=nonfinite)
    except (UnicodeDecodeError, ValueError, RecursionError) as error:
        raise Refusal("RECOVERY_JSON_INVALID", type(error).__name__) from None


def absolute_file(value):
    require(type(value) is str and 0 < len(value) <= 32767, "RECOVERY_PATH")
    path = Path(value)
    require(path.is_absolute(), "RECOVERY_ABSOLUTE_PATH")
    path = path.resolve(strict=True)
    require(path.is_file(), "RECOVERY_FILE_REQUIRED")
    return path


def owner_request(raw, clients):
    value = decode(raw)
    fields(value, {"op", "client", "args"})
    require(value["op"] == "recover_peer" and value["client"] == "owner",
            "RECOVERY_OWNER_OPERATION")
    selected = value["args"]
    fields(selected, {"client", "request_id", "supervisor_receipt"})
    require(type(selected["client"]) is str and selected["client"] in clients,
            "RECOVERY_TARGET_CLIENT")
    require(type(selected["request_id"]) is str
            and SAFE_ID.fullmatch(selected["request_id"]), "RECOVERY_TARGET_REQUEST_ID")
    return selected


def recorded_file(directory, receipt, name, bound):
    """Authenticate only indispensable identity inputs, not partial outputs."""
    rows = receipt.get("files")
    require(type(rows) is dict and {"request.json", "command.json"} <= set(rows)
            <= {"request.json", "command.json", "stdout.txt", "stderr.txt", "event.json"},
            "RECOVERY_RECEIPT_FILES")
    row = rows[name]
    fields(row, {"present", "bytes", "sha256"})
    require(row["present"] is True and type(row["bytes"]) is int
            and 0 < row["bytes"] <= bound and type(row["sha256"]) is str
            and SHA256.fullmatch(row["sha256"]), "RECOVERY_FILE_PIN")
    path = absolute_file(str(directory / name))
    require(path.parent == directory, "RECOVERY_ADJACENT_INPUT")
    raw = read(path, bound)
    require(len(raw) == row["bytes"] and digest(raw) == row["sha256"].lower(),
            "RECOVERY_FILE_CHANGED")
    return raw


def authenticate_pins(receipt, config, config_path, domains, event):
    pins = receipt.get("pins")
    require(type(pins) is list and len(pins) == 11, "RECOVERY_PIN_COUNT")
    interpreter = Path(sys.executable).resolve(strict=True)
    expected = {interpreter, config_path,
                *(domains.install / "py" / (name + ".py") for name in SOURCE_NAMES)}
    require(len(expected) == 11, "RECOVERY_PIN_PATH_COLLISION")
    selected, total = {}, 0
    for pin in pins:
        fields(pin, {"path", "bytes", "sha256"})
        path = absolute_file(pin["path"])
        require(path in expected and path not in selected, "RECOVERY_PIN_PATH")
        require(type(pin["bytes"]) is int and 0 < pin["bytes"] <= 16 * MIB
                and type(pin["sha256"]) is str and SHA256.fullmatch(pin["sha256"]),
                "RECOVERY_PIN_SHAPE")
        total += pin["bytes"]
        require(total <= 64 * MIB, "RECOVERY_PIN_TOTAL_BYTES")
        raw = read(path, pin["bytes"])
        actual = {"path": str(path), "bytes": len(raw), "sha256": digest(raw)}
        require(actual["bytes"] == pin["bytes"] and actual["sha256"] == pin["sha256"].lower(),
                "RECOVERY_ORIGINAL_CUT_CHANGED")
        selected[path] = actual
    require(set(selected) == expected, "RECOVERY_MISSING_PIN")
    require(type(receipt.get("bound_pin_count")) is int
            and receipt["bound_pin_count"] == len(selected)
            and type(receipt.get("bound_pin_bytes")) is int
            and receipt["bound_pin_bytes"] == total, "RECOVERY_PIN_COUNTERS")
    require(selected[config_path]["sha256"] == config["config_id"], "RECOVERY_CONFIG_PIN")
    for name in ("checking", "domains", "peer_wire", "peer_service", "peer_node"):
        configured = config["files"][name]
        fields(configured, {"path", "bytes", "sha256"})
        path = absolute_file(configured["path"])
        require(path == domains.install / "py" / (name + ".py")
                and type(configured["bytes"]) is int and type(configured["sha256"]) is str
                and SHA256.fullmatch(configured["sha256"]), "RECOVERY_CONFIG_SOURCE_PIN")
        require(selected[path]["bytes"] == configured["bytes"]
                and selected[path]["sha256"] == configured["sha256"].lower(),
                "RECOVERY_CONFIG_SOURCE_CHANGED")
    event["authenticated_pin_count"] = len(selected)
    event["authenticated_pin_bytes"] = total
    return interpreter


def authenticate_evidence(selected, config, config_path, domains, event):
    path = absolute_file(selected["supervisor_receipt"])
    directory = path.parent
    require(path.name == "supervisor.json" and directory.parent == domains.scratch / "calls"
            and SAFE_ID.fullmatch(directory.name), "RECOVERY_ORIGINAL_CALL_DIRECTORY")
    raw = read(path, 65536)
    receipt = strict_receipt_json(raw)
    require(type(receipt) is dict and type(receipt.get("schema")) is int
            and receipt["schema"] == 1 and receipt.get("name") == directory.name
            and receipt.get("status") in {"TRANSPORT_COMPLETE", "TRANSPORT_NONZERO_EXIT", "TRANSPORT_FAILED"}
            and receipt.get("native_acceptance") is False, "RECOVERY_RECEIPT_PROFILE")
    event["original_receipt"] = {"path": str(path), "bytes": len(raw), "sha256": digest(raw)}
    original_raw = recorded_file(directory, receipt, "request.json", 131072)
    require(receipt.get("request_sha256") == digest(original_raw), "RECOVERY_REQUEST_RECEIPT_BINDING")
    original = parse_node_request(original_raw, config["clients"])
    require(original["client"] == selected["client"]
            and original["request_id"] == selected["request_id"], "RECOVERY_SELECTED_REQUEST_BINDING")
    require(original["op"] in PEER_OPERATIONS, "RECOVERY_NATIVE_OPERATION_FORBIDDEN")
    command = strict_receipt_json(recorded_file(directory, receipt, "command.json", 65536))
    interpreter = authenticate_pins(receipt, config, config_path, domains, event)
    expected_command = {
        "argv": [str(interpreter), *PYTHON_FLAGS, str(domains.install / "py" / "node.py"),
                 "--config", str(config_path), "--state", str(domains.state),
                 "--request", str(directory / "request.json"), "--event", str(directory / "event.json")],
        "cwd": str(domains.install / "py"), "shell": False, "creationflags": 134217732,
        "environment_override": {"PYTHONDONTWRITEBYTECODE": "1"},
    }
    # Re-encoding, unlike Python equality, distinguishes false/0 and int/float.
    require(encode(command) == encode(expected_command), "RECOVERY_ORIGINAL_COMMAND_BINDING")
    event["original_request_sha256"] = digest(original_raw)
    event["original_operation"] = original["op"]
    event["original_call_directory"] = str(directory)
    return receipt, directory, original_raw


def require_quiescence(receipt):
    for key in ("job_created_before_process", "attach_resume_returned", "direct_child_reaped",
                "final_active_zero", "job_closed"):
        require(receipt.get(key) is True, "RECOVERY_QUIESCENCE_INCOMPLETE", key)
    require(type(receipt.get("pid")) is int and receipt["pid"] > 0
            and type(receipt.get("returncode")) is int, "RECOVERY_CHILD_EVIDENCE")
    initial, final = receipt.get("initial_job"), receipt.get("final_job")
    require(type(initial) is dict and type(initial.get("active_processes")) is int
            and initial["active_processes"] == 0, "RECOVERY_INITIAL_JOB_EVIDENCE")
    require(type(final) is dict and type(final.get("active_processes")) is int
            and final["active_processes"] == 0 and type(final.get("total_processes")) is int
            and final["total_processes"] >= 1, "RECOVERY_FINAL_JOB_EVIDENCE")
    require(type(receipt.get("cleanup_errors", [])) is list
            and receipt.get("cleanup_errors", []) == [], "RECOVERY_CLEANUP_ERRORS")
    require("evidence_persistence_error" not in receipt and "output_record_error" not in receipt,
            "RECOVERY_EVIDENCE_UNCERTAIN")
    # Deliberate Job termination is permitted; zero terminations is not a
    # recovery premise. Resource success and mathematical success are unrelated.


def exact_request_row(store, selected, original_raw, key):
    rows = store.rows("recovery_request",
        "SELECT key,client,request_id,raw,phase,response FROM requests WHERE client=? AND request_id=?",
        (selected["client"], selected["request_id"]))
    require(rows, "RECOVERY_REQUEST_NOT_FOUND")
    row = rows[0]
    require(row["key"] == key and row["client"] == selected["client"]
            and row["request_id"] == selected["request_id"] and bytes(row["raw"]) == original_raw,
            "RECOVERY_LEDGER_REQUEST_BINDING")
    return row


def require_no_stage(store, key):
    rows = store.rows("recovery_stages", "SELECT id FROM stages WHERE request=? LIMIT 1", (key,))
    require(not rows, "RECOVERY_NATIVE_STAGE_PRESENT")


def require_attempt(store, key, directory):
    data = {"request": key, "call_directory": str(directory)}
    expected_raw = encode({"config": store.config_id, "kind": "attempt", "client": "owner", "data": data})
    handle = "attempt:" + digest(expected_raw)
    rows = store.rows("recovery_attempt", "SELECT kind,client,raw FROM records WHERE handle=?", (handle,))
    require(rows and rows[0]["kind"] == "attempt" and rows[0]["client"] == "owner"
            and bytes(rows[0]["raw"]) == expected_raw, "RECOVERY_ORIGINAL_ATTEMPT_NOT_BOUND")
    return handle


def recover(store, selected, original_raw, receipt, directory, event):
    key = digest(encode([selected["client"], selected["request_id"]]))
    event["target_request_key"] = key
    require(store.meta()["initialized"] == 1, "NOT_INITIALIZED")
    row = exact_request_row(store, selected, original_raw, key)
    require_no_stage(store, key)
    if row["phase"] == "terminal":
        require(row["response"] is not None, "RECOVERY_TERMINAL_RESPONSE_MISSING")
        reply = bytes(row["response"])
        require(0 < len(reply) <= MIB, "RECOVERY_TERMINAL_RESPONSE_BOUND")
        event["historical"] = True
        event["state_outcome"] = "ORIGINAL_TERMINAL_RESPONSE_REPLAYED"
        return reply
    require(row["phase"] == "pending" and row["response"] is None, "RECOVERY_REQUEST_PHASE")
    require_quiescence(receipt)
    event["quiescence_authenticated"] = True
    event["attempt_handle"] = require_attempt(store, key, directory)
    # The OS writer lock remains held from selection through commit/close. All
    # transition guards are nevertheless re-read in the visibility transaction.
    with store.transaction():
        row = exact_request_row(store, selected, original_raw, key)
        require(row["phase"] == "pending" and row["response"] is None, "RECOVERY_REQUEST_PHASE_CHANGED")
        meta = dict(store.meta())
        require(meta["config"] == store.config_id and meta["initialized"] == 1
                and meta["active"] == key, "RECOVERY_ACTIVE_REQUEST_BINDING")
        require_no_stage(store, key)
        require_attempt(store, key, directory)
        event["terminal_write_attempted"] = True
        store.terminal(key, INTERRUPTED)
        after = dict(store.meta())
        require(after == dict(meta, active=None), "RECOVERY_COUNTERS_CHANGED")
        row = exact_request_row(store, selected, original_raw, key)
        require(row["phase"] == "terminal" and bytes(row["response"]) == INTERRUPTED,
                "RECOVERY_TERMINAL_BINDING")
    event["transition_committed"] = True
    event["state_outcome"] = "INTERRUPTED_RESPONSE_COMMITTED"
    event["retained_counters"] = {name: meta[name] for name in ("requests", "stages", "charged")}
    return INTERRUPTED


def blocked(error, event):
    if event["terminal_write_attempted"] and not event["transition_committed"]:
        event["state_outcome"] = "UNKNOWN_REPLAY_REQUIRED"
        code = "RECOVERY_PERSISTENCE_UNCERTAIN"
    else:
        code = error.code if isinstance(error, Refusal) else "RECOVERY_FAILED"
    detail = error.detail if isinstance(error, Refusal) else type(error).__name__
    event["failure_code"] = code
    event["failure_detail"] = detail[:512]
    return encode({"status": "BLOCKED", "code": code, "detail": detail[:512],
                   "state_outcome": event["state_outcome"]})


def main():
    parser = argparse.ArgumentParser()
    for name in ("config", "state", "request", "event"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    event = {"recovery_profile": "draft-native-free-peer-v1", "checker_loaded": False,
             "native_stages": 0, "stages_allocated": 0, "sql_vm_steps": 0, "sql_rows": {},
             "sql_opened": False, "historical": False, "request_sha256": None,
             "original_outputs_used": False, "mathematical_acceptance_authority": False,
             "quiescence_authenticated": False, "terminal_write_attempted": False,
             "transition_committed": False, "state_outcome": "UNCHANGED_BY_RECOVERY"}
    event_path = None
    try:
        require_python_profile()
        require(os.name == "nt", "WINDOWS_OWNER_LOCK_PROFILE")
        config_path = absolute_file(str(args.config))
        config = load_config(config_path)
        domains = Domains.from_config(config)
        require(domains.install == INSTALL, "RECOVERY_INSTALL_BINDING")
        domains.require_state(args.state)
        require(args.event.is_absolute(), "RECOVERY_EVENT_ABSOLUTE")
        selected_event = args.event.resolve()
        require(selected_event != domains.scratch and selected_event.is_relative_to(domains.scratch)
                and selected_event.parent.is_dir() and not selected_event.exists(), "RECOVERY_NEW_EVENT_DOMAIN")
        raw = read(absolute_file(str(args.request)), 16384)
        event["request_sha256"] = digest(raw)
        selected = owner_request(raw, config["clients"])
        original_directory = absolute_file(selected["supervisor_receipt"]).parent
        require(not selected_event.is_relative_to(original_directory),
                "RECOVERY_EVENT_MUST_NOT_MODIFY_ORIGINAL_CALL")
        event_path = selected_event
        receipt, directory, original_raw = authenticate_evidence(selected, config, config_path, domains, event)
        require(domains.state.is_dir() and (domains.state / "control.sqlite3").is_file(), "NOT_INITIALIZED")
        with owner_lock(domains.state):
            store = ControlStore(domains.state, config["config_id"], config["limits"], event, create=False)
            try:
                reply = recover(store, selected, original_raw, receipt, directory, event)
            finally:
                store.close()
    except Exception as error:
        reply = blocked(error, event)
    require(0 < len(reply) <= MIB, "RECOVERY_RESPONSE_LIMIT")
    event["sql_vm_steps_upper"] = event["sql_vm_steps"]
    event["sql_progress_interval"] = 1
    event["response_sha256"] = digest(reply)
    event["elapsed_seconds"] = time.monotonic() - started
    # No stdout claims a supervised response if durable event output fails.
    # Such failure never undoes a transaction; a later recovery must re-read it.
    if event_path is None:
        sys.stderr.write("Recovery event domain could not be established.\n")
        return 2
    try:
        event_raw = encode(event)
        require(len(event_raw) <= 65536, "RECOVERY_EVENT_LIMIT")
        with event_path.open("xb") as stream:
            stream.write(event_raw)
            stream.flush()
            os.fsync(stream.fileno())
    except Exception:
        sys.stderr.write("Recovery event persistence failed; ledger outcome requires replay.\n")
        return 2
    sys.stdout.buffer.write(reply)
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

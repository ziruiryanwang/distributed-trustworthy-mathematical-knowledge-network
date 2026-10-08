"""DRAFT owner recovery supervision; not installed, executed, or qualified.

Future manage.py integration imports invoke_recovery after both recovery files
are placed together in py/ in a new source cut. This draft also supplies a
standalone `recover --config ... --request ...` entry for reviewed qualification.
It never opens the control store or imports the recovery worker in its caller.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import uuid

INSTALL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(INSTALL / "py"))

from domains import Domains, require_python_profile
from node import SAFE_ID, load_config
from storage import decode, digest, encode, read, require

MIB = 1048576
SOURCE_NAMES = ("node", "run_stage", "storage", "checking", "domains", "supervise",
                "peer_wire", "peer_service", "peer_node")
LIMITS = {"wall_seconds": 30, "cpu_seconds": 15, "memory_mib": 256,
          "active_processes": 8, "stdout_bytes": MIB, "stderr_bytes": 65536,
          "event_bytes": 65536, "request_bytes": 16384,
          "poll_seconds": 0.05, "settle_seconds": 5}


def pin(path, bound=16 * MIB):
    path = Path(path).resolve(strict=True)
    require(path.is_file(), "RECOVERY_PIN_FILE")
    raw = read(path, bound)
    require(raw, "RECOVERY_EMPTY_PIN")
    return {"path": str(path), "bytes": len(raw), "sha256": digest(raw)}


def selected_owner_request(raw, config, domains):
    value = decode(raw)
    require(type(value) is dict and set(value) == {"op", "client", "args"}
            and value["op"] == "recover_peer" and value["client"] == "owner", "RECOVERY_OWNER_REQUEST")
    selected = value["args"]
    require(type(selected) is dict and set(selected) == {"client", "request_id", "supervisor_receipt"},
            "RECOVERY_TARGET_FIELDS")
    require(type(selected["client"]) is str and selected["client"] in config["clients"]
            and type(selected["request_id"]) is str and SAFE_ID.fullmatch(selected["request_id"]),
            "RECOVERY_TARGET_IDENTITY")
    chosen = selected["supervisor_receipt"]
    require(type(chosen) is str and 0 < len(chosen) <= 32767 and Path(chosen).is_absolute(),
            "RECOVERY_ORIGINAL_RECEIPT_PATH")
    chosen = Path(chosen).resolve(strict=True)
    require(chosen.name == "supervisor.json" and chosen.parent.parent == domains.scratch / "calls"
            and SAFE_ID.fullmatch(chosen.parent.name), "RECOVERY_ORIGINAL_RECEIPT_DOMAIN")
    return selected, pin(chosen, 65536)


def save_grant(path, value):
    raw = encode(value)
    require(len(raw) <= 65536, "RECOVERY_GRANT_LIMIT")
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def transport_failure(directory, code):
    return {"status": "TRANSPORT_FAILED", "code": code, "evidence": str(directory),
            "accepted": None, "state_outcome": "UNKNOWN"}


def invoke_recovery(args, *, owner_entrypoint=None):
    """One explicit finite owner grant; return None only after exact forwarding.

    owner_entrypoint is trusted integration wiring, not a request field. A future
    manage caller must pass its exact __file__; standalone entry omits it because
    this module is already pinned. Every state decision belongs to the worker.
    """
    require_python_profile()
    require(os.name == "nt", "WINDOWS_RECOVERY_SUPERVISION_REQUIRED")
    require(args.config.is_absolute() and args.request.is_absolute(), "RECOVERY_ABSOLUTE_INPUTS")
    config_path = args.config.resolve(strict=True)
    config = load_config(config_path)
    domains = Domains.from_config(config)
    require(domains.install == INSTALL, "RECOVERY_CALLING_INSTALLATION_BINDING")
    caller = Path(__file__).resolve(strict=True)
    require(caller.parent in {INSTALL / "drafts", INSTALL / "py"}, "RECOVERY_WRAPPER_LOCATION")
    worker = (caller.parent / "recovery_worker.py").resolve(strict=True)
    require(worker.parent == caller.parent, "RECOVERY_WORKER_LOCATION")
    raw = read(args.request, 16384)
    selected, original_receipt = selected_owner_request(raw, config, domains)
    inputs = [pin(sys.executable), pin(config_path),
              *[pin(INSTALL / "py" / (name + ".py")) for name in SOURCE_NAMES],
              pin(worker), pin(caller), original_receipt]
    if owner_entrypoint is not None:
        owner_path = Path(owner_entrypoint).resolve(strict=True)
        require(owner_path == INSTALL / "manage.py", "RECOVERY_OWNER_ENTRYPOINT_BINDING")
        inputs.append(pin(owner_path))
    require(len(inputs) in {14, 15} and len({row["path"] for row in inputs}) == len(inputs)
            and sum(row["bytes"] for row in inputs) <= 64 * MIB - 65536, "RECOVERY_INPUT_PIN_BOUND")

    # No directory or state write precedes owner-envelope/input validation.
    recoveries = domains.scratch / "recoveries"
    require(recoveries.resolve() == recoveries, "RECOVERY_EVIDENCE_PARENT_DOMAIN")
    recoveries.mkdir(parents=True, exist_ok=True)
    directory = recoveries / ("recovery-" + uuid.uuid4().hex)
    directory.mkdir(exist_ok=False)
    cases = directory / "cases"
    cases.mkdir(exist_ok=False)
    grant_path = directory / "grant.json"
    grant = {"schema": 1, "profile": "draft-owner-recovery-supervision-v1",
             "request_sha256": digest(raw), "target_client": selected["client"],
             "target_request_id": selected["request_id"], "original_receipt": original_receipt,
             "worker": str(worker), "state": str(domains.state), "limits": LIMITS,
             "inputs": inputs, "policy": "one explicit invocation; no automatic retries, quota reset, refunds or repair",
             "close_evidence": "CURRENT_CUT_WRAPPER_RETURN_ONLY; final active-zero and child reap required independently"}
    save_grant(grant_path, grant)
    # Finalize once, then pin. The grant lists its inputs, never its own hash.
    pins = [*inputs, pin(grant_path, 65536)]
    require(len(pins) <= 16 and sum(row["bytes"] for row in pins) <= 64 * MIB,
            "RECOVERY_FINAL_PIN_BOUND")

    import run_stage
    import supervise
    require(Path(run_stage.__file__).resolve() == INSTALL / "py" / "run_stage.py"
            and Path(supervise.__file__).resolve() == INSTALL / "py" / "supervise.py", "RECOVERY_SUPERVISION_MODULE_PATH")
    transport = supervise.Transport(sys.executable, worker, config_path, domains.state,
                                     cases, run_stage, dict(LIMITS, pins=pins))
    try:
        response = transport("recover", raw)
    except supervise.SupervisorFailure:
        return transport_failure(directory, "RECOVERY_PUBLIC_TRANSPORT_FAILED")
    if response["returncode"] != 0:
        return transport_failure(directory, "RECOVERY_PUBLIC_WORKER_EXIT")
    observed = response["event"]
    try:
        require(observed.get("recovery_profile") == "draft-native-free-peer-v1"
                and observed.get("checker_loaded") is False
                and observed.get("mathematical_acceptance_authority") is False,
                "RECOVERY_WORKER_PROFILE")
        for name in ("native_stages", "stages_allocated"):
            require(type(observed.get(name)) is int and observed[name] == 0, "RECOVERY_NATIVE_WORK_OBSERVED")
        require(type(observed.get("transition_committed")) is bool
                and type(observed.get("historical")) is bool
                and not (observed["transition_committed"] and observed["historical"]), "RECOVERY_RESULT_BRANCH")
        if observed["transition_committed"] or observed["historical"]:
            require(encode(observed.get("original_receipt")) == encode(original_receipt),
                    "RECOVERY_SELECTED_RECEIPT_CHANGED")
    except Exception:
        return transport_failure(directory, "RECOVERY_WORKER_OBSERVATION_UNCERTAIN")
    # Transport already binds event request/response hashes and requires a reaped
    # child and zero final Job processes. Do not re-encode a successful replay.
    sys.stdout.buffer.write(response["stdout"])
    sys.stdout.buffer.flush()
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    command = commands.add_parser("recover")
    command.add_argument("--config", required=True, type=Path)
    command.add_argument("--request", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = invoke_recovery(args)
    except Exception as error:
        result = {"status": "OWNER_COMMAND_FAILED", "code": getattr(error, "code", type(error).__name__),
                  "detail": str(error)[:512], "accepted": None, "state_outcome": "UNKNOWN"}
    if result is not None:
        sys.stdout.buffer.write(encode(result))
        sys.stdout.buffer.flush()
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

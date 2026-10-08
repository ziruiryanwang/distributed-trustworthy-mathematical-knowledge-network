"""V3 owner CLI adapter; integrated development, not qualified."""
from pathlib import Path
import sys
import uuid

from storage import Refusal, encode, read, require


def invoke_admin(args, *, owner_entrypoint):
    from domains import Domains
    from node import load_config
    import run_stage
    import supervise
    install = Path(owner_entrypoint).resolve().parent
    require(args.command in {"status", "renew"}, "ADMIN_COMMAND")
    # An invalid config cannot authorize a worker/event path. The calling
    # manage.main converts this pre-spawn error into OWNER_COMMAND_FAILED/code.
    config = load_config(args.config)
    domains = Domains.from_config(config)
    require(domains.install == install, "CALLING_INSTALLATION_BINDING")
    if args.command == "status":
        raw = encode({"schema": 1, "op": "status", "config": config["config_id"]})
    else:
        try:
            raw = read(args.request, 16384)
            require(bool(raw), "GRANT_ENVELOPE_BOUND")
        except Refusal as error:
            return {"status": "REFUSED", "code": error.code, "detail": error.detail[:512],
                "grant_recorded": False, "state_outcome": "UNCHANGED_BY_RENEWAL",
                "mathematicalAcceptance": False, "supervised": False,
                "cost_scope": "owner input-size preflight; CPU not measured"}
    evidence = domains.scratch / "administration"
    evidence.mkdir(exist_ok=True)
    names = ("admin_worker.py", "node.py", "capacity.py", "storage.py", "domains.py",
             "run_stage.py", "supervise.py", "admin_manage.py")
    def pin(path):
        import hashlib
        path = Path(path).resolve(strict=True)
        data = read(path, 16 * 1048576)
        return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    pins = [pin(sys.executable), pin(args.config), pin(owner_entrypoint),
            *[pin(install / "py" / name) for name in names]]
    limits = {"pins": pins, "wall_seconds": 10, "cpu_seconds": 5, "memory_mib": 128,
              "active_processes": 8, "request_bytes": 16384,
              "stdout_bytes": 65536, "stderr_bytes": 65536, "event_bytes": 65536}
    transport = supervise.Transport(sys.executable, install / "py/admin_worker.py", args.config,
                                    domains.state, evidence, run_stage, limits)
    name = "admin-" + uuid.uuid4().hex
    response, receipt, failure = None, None, None
    try:
        response = transport(name, raw)
    except supervise.SupervisorFailure as error:
        receipt, failure = error.record, error.code
    observation = {"observed_job_cpu_seconds": None, "cleanup": None,
                   "endpoint_census": "UNAVAILABLE", "owner_prefix_cpu_measured": False}
    # Endpoint-only evidence limit. Exceeding it cannot undo a committed grant.
    try:
        if receipt is None:
            receipt = supervise.strict_json(read(evidence / name / "supervisor.json", 65536))
        observation["observed_job_cpu_seconds"] = (receipt.get("final_job") or {}).get("cpu_seconds")
        observation["cleanup"] = {key: receipt.get(key) for key in
            ("direct_child_reaped", "final_active_zero", "job_closed", "cleanup_errors")}
        require(receipt.get("direct_child_reaped") is True and receipt.get("final_active_zero") is True
                and receipt.get("job_closed") is True and not receipt.get("cleanup_errors")
                and (receipt.get("final_job") or {}).get("active_processes") == 0,
                "ADMIN_CENSUS_REQUIRES_QUIESCENCE")
        total, entries = 0, 0
        for path in (evidence / name).iterdir():
            entries += 1
            require(entries <= 16 and path.is_file() and not path.is_symlink()
                    and not getattr(path.lstat(), "st_file_attributes", 0) & 0x400, "ADMIN_EVIDENCE_ENTRY")
            total += path.stat().st_size
            require(total <= 1048576, "ADMIN_EVIDENCE_BYTES")
        observation["endpoint_census"] = {"files": entries, "bytes": total,
                                          "bound_bytes": 1048576, "hard_transient_quota": False}
        if response is not None:
            require(response["returncode"] == 0, "ADMIN_WORKER_EXIT")
    except Exception as error:
        failure = failure or getattr(error, "code", type(error).__name__)
    if failure is not None or response is None:
        return {"status": "ADMIN_TRANSPORT_FAILED", "code": "RENEWAL_OUTCOME_UNKNOWN"
            if args.command == "renew" else "STATUS_UNAVAILABLE", "evidence": str(evidence / name),
            "detail": failure, "state_outcome": "UNKNOWN", **observation,
            "grant_recorded": None, "mathematicalAcceptance": False}
    sys.stdout.buffer.write(response["stdout"])
    sys.stdout.buffer.flush()
    return None

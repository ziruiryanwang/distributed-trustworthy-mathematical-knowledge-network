"""Finite cumulative owner hosting; immutable grants and pre-launch charges.

Cooperative Windows/local-filesystem profile, not a scheduler or acceptance path.
The existing supervisor and service worker remain the only execution machinery.
"""
from __future__ import annotations

import os
from pathlib import Path
import re
import sys

from domains import Domains, require_python_profile
from node import load_config
from storage import decode, digest, encode, owner_lock, read, require
import supervise

MIB = 1048576
INSTALL = Path(__file__).resolve().parent.parent
PROFILE = "finite-loopback-host-v1"
MAX_SLOTS = 4096
MAX_GRANTS = 128
ID = re.compile(r"[a-z0-9_-]{1,32}\Z")
HEX = re.compile(r"[a-f0-9]{64}\Z")
SOURCES = ("service_worker", "inspect_context", "node", "storage", "capacity",
           "domains", "run_stage", "supervise", "peer_wire", "peer_service", "peer_node", "hosting")


def safe(path, *, missing=False):
    path = Path(path)
    require(path.is_absolute() and ".." not in path.parts, "HOST_ABSOLUTE_PATH")
    for current in (path, *path.parents):
        if missing and current == path and not os.path.lexists(current):
            continue
        info = current.lstat()
        require(not current.is_symlink() and not getattr(info, "st_file_attributes", 0) & 0x400,
                "HOST_REPARSE_PATH")
    require(path.resolve() == path, "HOST_NONCANONICAL_PATH")
    return path


def save_new(path, value):
    raw = encode(value)
    require(len(raw) <= 65536, "HOST_RECORD_LIMIT")
    safe(path, missing=True)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def pin(path):
    path = safe(Path(path).resolve(strict=True))
    raw = read(path, 16 * MIB)
    require(raw, "HOST_EMPTY_PIN")
    return {"path": str(path), "bytes": len(raw), "sha256": digest(raw)}


def charge(grant):
    return {"sessions": 1, "service_seconds": grant["seconds"],
            "supervised_wall_seconds": grant["seconds"] + 30, "cpu_seconds": 120,
            "connections": grant["max_requests"], "send_bytes": grant["max_bytes"],
            "retained_bytes": MIB}


def parse_grant(raw, config):
    value = decode(raw)
    require(type(value) is dict and set(value) == {
        "schema", "profile", "id", "config", "client", "view", "catalog_sha256", "port",
        "max_sessions", "seconds", "max_requests", "max_bytes"}, "HOST_GRANT_FIELDS")
    require(type(value["schema"]) is int and value["schema"] == 1
            and value["profile"] == PROFILE, "HOST_GRANT_PROFILE")
    require(type(value["id"]) is str and ID.fullmatch(value["id"])
            and value["id"].upper() not in supervise.RESERVED_NAMES, "HOST_GRANT_ID")
    require(value["config"] == config["config_id"] and value["client"] in config["clients"],
            "HOST_CONFIG_OR_CLIENT")
    require(type(value["view"]) is str and value["view"].startswith("view:")
            and len(value["view"]) <= 96 and type(value["catalog_sha256"]) is str
            and HEX.fullmatch(value["catalog_sha256"]), "HOST_VIEW_BINDING")
    for field, low, high in (("port", 1, 65535), ("max_sessions", 1, 128),
                             ("seconds", 1, 360), ("max_requests", 1, 128),
                             ("max_bytes", 1, 256 * MIB)):
        require(type(value[field]) is int and low <= value[field] <= high, "HOST_LIMIT:" + field)
    return value


def limits(grant, pins):
    return {"pins": pins, "wall_seconds": grant["seconds"] + 30, "cpu_seconds": 120,
            "memory_mib": 256, "active_processes": 8, "stdout_bytes": 65536,
            "stderr_bytes": 65536, "event_bytes": 65536, "request_bytes": 16384}


def validate_view(config, domains, grant):
    # Read-only, bounded keyed lookup before any hosting authorization/write.
    # The existing worker still performs full view/custody validation per session.
    from inspect_context import ReadOnlyControl
    event = {"sql_vm_steps": 0, "sql_rows": {}, "sql_opened": False}
    control = ReadOnlyControl(domains.state, config["config_id"], event)
    try:
        view = control.record(grant["view"], "view", grant["client"])
        require(type(view) is dict and view.get("kind") == "peer_view"
                and view.get("mathematicalAcceptance") is False
                and type(view.get("catalog")) is dict
                and view["catalog"].get("sha256") == grant["catalog_sha256"], "HOST_COMMITTED_VIEW_BINDING")
    finally:
        control.close()


def names(directory, pattern, maximum):
    result = []
    with os.scandir(safe(directory)) as entries:
        for entry in entries:
            require(len(result) < maximum and re.fullmatch(pattern, entry.name)
                    and entry.is_file(follow_symlinks=False), "HOST_JOURNAL_LAYOUT")
            safe(Path(entry.path))
            result.append(entry.name)
    return sorted(result)


def read_manifest(root, name, config):
    require(type(name) is str and ID.fullmatch(name), "HOST_GRANT_ID")
    path = safe(root / "grants" / (name + ".json"))
    manifest = decode(read(path, 65536))
    require(type(manifest) is dict and set(manifest) == {
        "schema", "grant", "inputs", "authorized"} and type(manifest["schema"]) is int
        and manifest["schema"] == 1, "HOST_MANIFEST")
    grant = parse_grant(encode(manifest["grant"]), config)
    require(grant["id"] == name and manifest["authorized"] == {
        key: value * grant["max_sessions"] for key, value in charge(grant).items()}, "HOST_AUTHORIZATION")
    require(type(manifest["inputs"]) is list and len(manifest["inputs"]) == 15, "HOST_INPUT_PINS")
    return manifest, pin(path)


def request_for(grant, ordinal):
    return {"op": "serve", "session": "host-" + grant["id"] + "-" + str(ordinal).zfill(4),
            "client": grant["client"], "view": grant["view"], "port": grant["port"],
            "seconds": grant["seconds"], "max_requests": grant["max_requests"],
            "max_bytes": grant["max_bytes"]}


def quiescence(receipt):
    # Same positive evidence as owner recovery; an absent lock is insufficient.
    for key in ("job_created_before_process", "attach_resume_returned", "direct_child_reaped",
                "final_active_zero", "job_closed"):
        require(receipt.get(key) is True, "HOST_PRIOR_QUIESCENCE_UNCERTAIN")
    require(type(receipt.get("pid")) is int and receipt["pid"] > 0
            and type(receipt.get("returncode")) is int, "HOST_PRIOR_CHILD_UNCERTAIN")
    initial, final = receipt.get("initial_job"), receipt.get("final_job")
    require(type(initial) is dict and type(initial.get("active_processes")) is int
            and initial["active_processes"] == 0 and type(final) is dict
            and type(final.get("active_processes")) is int and final["active_processes"] == 0
            and type(final.get("total_processes")) is int and final["total_processes"] >= 1,
            "HOST_PRIOR_JOB_UNCERTAIN")
    require(receipt.get("cleanup_errors", []) == [] and "evidence_persistence_error" not in receipt
            and "output_record_error" not in receipt, "HOST_PRIOR_EVIDENCE_UNCERTAIN")


def reconcile(domains, root, slot, manifest, grant_pin):
    """Persist a terminal marker only from matching existing supervisor evidence."""
    request = slot["request"]
    directory = domains.scratch / "services" / request["session"] / "cases" / "serve"
    receipt_path = directory / "supervisor.json"
    require(receipt_path.is_file(), "HOST_PRIOR_RECEIPT_MISSING")
    raw = read(safe(receipt_path), 65536)
    receipt = supervise.strict_json(raw)
    require(type(receipt) is dict, "HOST_PRIOR_RECEIPT")
    quiescence(receipt)
    request_raw = read(safe(directory / "request.json"), 16384)
    require(request_raw == encode(request) and receipt.get("request_sha256") == digest(request_raw)
            and receipt.get("name") == "serve" and receipt.get("native_acceptance") is False,
            "HOST_PRIOR_REQUEST_BINDING")
    selected_limits = limits(manifest["grant"], [*manifest["inputs"], grant_pin])
    require(receipt.get("pins") == selected_limits["pins"]
            and receipt.get("limits") == dict(supervise.DEFAULTS, **{
                key: value for key, value in selected_limits.items() if key != "pins"})
            and receipt.get("wall_limit_seconds") == selected_limits["wall_seconds"],
            "HOST_PRIOR_ENVELOPE_BINDING")
    successful = receipt.get("status") == "TRANSPORT_COMPLETE" and receipt["returncode"] == 0
    if successful:
        stdout = read(safe(directory / "stdout.txt"), 65536)
        event_raw = read(safe(directory / "event.json"), 65536)
        event = supervise.strict_json(event_raw)
        result = supervise.strict_json(stdout)
        require(event.get("request_sha256") == digest(request_raw)
                and event.get("response_sha256") == digest(stdout), "HOST_PRIOR_OUTPUT_BINDING")
        for name, data in (("request.json", request_raw), ("stdout.txt", stdout), ("event.json", event_raw)):
            require(receipt.get("files", {}).get(name) == {
                "present": True, "bytes": len(data), "sha256": digest(data)}, "HOST_PRIOR_FILE_BINDING")
        observations = result.get("observations", {})
        successful = (result.get("status") == "SERVICE_STOPPED"
            and result.get("session") == request["session"] and result.get("view") == request["view"]
            and result.get("catalog_sha256") == manifest["grant"]["catalog_sha256"]
            and result.get("mathematicalAcceptance") is False and result.get("native_stages") == 0
            and event.get("checker_loaded") is False and event.get("native_stages") == 0
            and observations.get("mathematicalAcceptance") is False
            and observations.get("checker_loaded") is False and observations.get("native_stages") == 0
            and observations.get("bind_host") == "127.0.0.1" and observations.get("port") == request["port"]
            and observations.get("stop_reason") == "SESSION_LIMIT"
            and "last_error" not in observations)
    terminal = {"schema": 1, "slot_sha256": digest(encode(slot)), "supervisor_sha256": digest(raw),
                "status": "HOST_SESSION_COMPLETE" if successful else "HOST_SESSION_FAILED"}
    save_new(root / "done" / (str(slot["sequence"]).zfill(6) + ".json"), terminal)
    return terminal


def journal(domains, root, config):
    """Bounded retained journal. Every missing terminal marker is reconciled."""
    files = names(root / "slots", r"[0-9]{6}\.json", MAX_SLOTS)
    require(files == [str(index).zfill(6) + ".json" for index in range(1, len(files) + 1)],
            "HOST_JOURNAL_GAP")
    done_names = names(root / "done", r"[0-9]{6}\.json", MAX_SLOTS)
    require(set(done_names) <= set(files), "HOST_ORPHAN_TERMINAL")
    counts, failed, manifests = {}, set(), {}
    for sequence, name in enumerate(files, 1):
        slot = decode(read(safe(root / "slots" / name), 16384))
        require(type(slot) is dict and set(slot) == {
            "schema", "sequence", "grant", "grant_sha256", "request", "charge"}
            and type(slot["schema"]) is int and slot["schema"] == 1
            and type(slot["sequence"]) is int and slot["sequence"] == sequence, "HOST_SLOT")
        selected = slot["grant"]
        require(type(selected) is str and ID.fullmatch(selected), "HOST_SLOT_GRANT")
        if selected not in manifests:
            manifests[selected] = read_manifest(root, selected, config)
        manifest, grant_pin = manifests[selected]
        counts[selected] = counts.get(selected, 0) + 1
        require(selected not in failed and counts[selected] <= manifest["grant"]["max_sessions"]
                and slot["grant_sha256"] == grant_pin["sha256"]
                and encode(slot["charge"]) == encode(charge(manifest["grant"]))
                and encode(slot["request"]) == encode(request_for(manifest["grant"], counts[selected])), "HOST_SLOT_BINDING")
        terminal_path = root / "done" / name
        if terminal_path.exists():
            terminal = decode(read(safe(terminal_path), 16384))
        else:
            terminal = reconcile(domains, root, slot, manifest, grant_pin)
        require(type(terminal) is dict and set(terminal) == {
            "schema", "slot_sha256", "supervisor_sha256", "status"}
            and type(terminal["schema"]) is int and terminal["schema"] == 1
            and terminal["slot_sha256"] == digest(encode(slot))
            and type(terminal["supervisor_sha256"]) is str and HEX.fullmatch(terminal["supervisor_sha256"])
            and terminal["status"] in {"HOST_SESSION_COMPLETE", "HOST_SESSION_FAILED"}, "HOST_TERMINAL")
        receipt_path = (domains.scratch / "services" / slot["request"]["session"]
                        / "cases" / "serve" / "supervisor.json")
        require(receipt_path.is_file(), "HOST_COMPLETED_RECEIPT_MISSING")
        require(digest(read(safe(receipt_path), 65536)) == terminal["supervisor_sha256"],
                "HOST_COMPLETED_RECEIPT_CHANGED")
        if terminal["status"] == "HOST_SESSION_FAILED":
            failed.add(selected)
    return len(files), counts, failed


def run_grant(config, domains, config_path, grant, inputs, runner):
    """Internal owner integration, with injectable existing transport for tests."""
    root = domains.require_write(domains.scratch / "hosting")
    safe(root, missing=True)
    root.mkdir(exist_ok=True)
    with owner_lock(root):
        for name in ("grants", "slots", "done"):
            safe(root / name, missing=True).mkdir(exist_ok=True)
        # Resolve every prior reservation before authorizing a new grant or slot.
        total, counts, failed = journal(domains, root, config)
        stored = root / "grants" / (grant["id"] + ".json")
        expected = {"schema": 1, "grant": grant, "inputs": inputs,
                    "authorized": {key: value * grant["max_sessions"] for key, value in charge(grant).items()}}
        if stored.exists():
            require(read(safe(stored), 65536) == encode(expected), "HOST_GRANT_CHANGED")
        else:
            require(len(names(root / "grants", r"[a-z0-9_-]{1,32}\.json", MAX_GRANTS)) < MAX_GRANTS,
                    "HOST_GRANT_COUNT_LIMIT")
            save_new(stored, expected)
        manifest, grant_pin = read_manifest(root, grant["id"], config)
        count = counts.get(grant["id"], 0)
        if grant["id"] in failed:
            return report("HOST_HALTED", root, grant, count)
        while count < grant["max_sessions"]:
            require(total < MAX_SLOTS, "HOST_GLOBAL_SESSION_LIMIT")
            request = request_for(grant, count + 1)
            session = domains.require_write(domains.scratch / "services" / request["session"])
            require(not os.path.lexists(session), "HOST_NEW_SESSION_REQUIRED")
            safe(session.parent, missing=True).mkdir(exist_ok=True)
            slot = {"schema": 1, "sequence": total + 1, "grant": grant["id"],
                    "grant_sha256": grant_pin["sha256"], "request": request, "charge": charge(grant)}
            # Durable, full maxima charged BEFORE directories/worker launch. No refund.
            save_new(root / "slots" / (str(total + 1).zfill(6) + ".json"), slot)
            total, count = total + 1, count + 1
            session.mkdir(exist_ok=False)
            (session / "cases").mkdir()
            selected_limits = limits(grant, [*inputs, grant_pin])
            save_new(session / "grant.json", {"schema": 1, "hosting_grant": grant_pin,
                "reservation": slot, "limits": selected_limits})
            transport = supervise.Transport(sys.executable, domains.install / "py" / "service_worker.py",
                config_path, domains.state, session / "cases", runner, selected_limits)
            try:
                transport("serve", encode(request))
            except supervise.SupervisorFailure:
                # A failure receipt can establish safe stop, never successful service.
                pass
            terminal = reconcile(domains, root, slot, manifest, grant_pin)
            if terminal["status"] != "HOST_SESSION_COMPLETE":
                return report("HOST_HALTED", root, grant, count)
        return report("HOST_GRANT_EXHAUSTED", root, grant, count)


def report(status, root, grant, count):
    return {"status": status, "grant": grant["id"], "evidence": str(root),
            "reserved": {key: value * count for key, value in charge(grant).items()},
            "authorized": {key: value * grant["max_sessions"] for key, value in charge(grant).items()},
            "mathematicalAcceptance": False, "native_stages": 0,
            "policy": "full pre-launch maxima retained; no refunds or implicit renewal"}


def invoke_host(args, *, owner_entrypoint):
    require_python_profile()
    require(os.name == "nt", "WINDOWS_HOSTING_PROFILE")
    config_path = safe(args.config)
    grant_path = safe(args.grant)
    config = load_config(config_path)
    domains = Domains.from_config(config)
    require(domains.install == INSTALL and Path(owner_entrypoint).resolve(strict=True) == INSTALL / "manage.py",
            "HOST_INSTALL_BINDING")
    grant = parse_grant(read(grant_path, 16384), config)
    validate_view(config, domains, grant)
    inputs = [pin(sys.executable), pin(config_path), *[pin(INSTALL / "py" / (name + ".py")) for name in SOURCES],
              pin(INSTALL / "manage.py")]
    require(len(inputs) == 15 and sum(row["bytes"] for row in inputs) <= 64 * MIB - 65536, "HOST_PIN_LIMIT")
    import run_stage
    require(Path(run_stage.__file__).resolve() == INSTALL / "py" / "run_stage.py"
            and Path(supervise.__file__).resolve() == INSTALL / "py" / "supervise.py", "HOST_SUPERVISOR_ORIGIN")
    return run_grant(config, domains, config_path, grant, inputs, run_stage)

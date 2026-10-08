"""Bounded status/renew worker; integrated development, not qualified.

No mathematics, ordinary reservation, source execution, or background polling.
Supervisory files are distinct from the node-state read-only status guarantee.
"""
import argparse
import os
from pathlib import Path
import sys
import time

from capacity import parse_grant, physical_supply
from domains import Domains, require_python_profile
from node import load_config
from storage import ControlStore, Refusal, decode, digest, encode, owner_lock, read, require


def status_request(raw, config_id):
    value = decode(raw)
    require(type(value) is dict and set(value) == {"schema", "op", "config"}
            and type(value["schema"]) is int and value["schema"] == 1
            and value["op"] == "status" and value["config"] == config_id, "STATUS_REQUEST")


def status(store, domains):
    observation = store.authorization_state()
    used, authorized = observation["used"], observation["authorized"]
    remaining = {key: authorized[key] - used[key] for key in used}
    cap = observation["metadata_pages"]
    pages = store.scalar("status_pages", "PRAGMA page_count")
    freelist = store.scalar("status_freelist", "PRAGMA freelist_count")
    pending = None
    if observation["active"] is not None:
        rows = store.rows("status_active", "SELECT key,client,request_id,phase FROM requests WHERE key=?",
                          (observation["active"],))
        require(len(rows) == 1 and rows[0]["phase"] == "pending", "PENDING_BINDING")
        pending = dict(rows[0])
    heads = [dict(row) for row in store.rows("status_heads", "SELECT client,context FROM heads ORDER BY client LIMIT 17",
                                           maximum=16)]
    provider = store.rows("status_provider", "SELECT cut,snapshot FROM providers WHERE provider='P1'")
    if observation["initialized"]:
        require(len(provider) == 1, "INITIALIZED_PROVIDER_MISSING")
    physical = None
    supply_error = None
    try:
        physical = physical_supply(domains.state, domains.scratch, remaining["reserved_bytes"], cap,
                                   enforce=False)
    except Refusal as error:
        supply_error = error.code
    return {"status": "STATUS", "config": store.config_id, "mathematicalAcceptance": False,
        "state_read_only": True, "live_context_status": "UNCHECKED", **observation,
        "remaining": remaining, "metadata": {"pages": pages, "freelist_pages": freelist,
            "total_cap_pages": cap, "ordinary_cap_pages": cap - 2048,
            "terminal_cap_pages": cap - 1024, "new_admission_max_pages": cap - 4096,
            "ordinary_headroom": pages <= cap - 4096, "within_total_cap": pages <= cap},
        "pending_request": pending, "heads": heads,
        "provider": dict(provider[0]) if provider else None,
        "physical_supply": physical, "physical_supply_error": supply_error}


def run(config, raw, event):
    domains = Domains.from_config(config)
    envelope = decode(raw)
    require(type(envelope) is dict and type(envelope.get("op")) is str
            and envelope["op"] in {"status", "renew"}, "ADMIN_OPERATION")
    op = envelope["op"]
    event["operation"] = op
    if op == "status":
        status_request(raw, config["config_id"])
    else:
        parsed = parse_grant(raw, config["config_id"])
    def absent():
        return encode({"status": "NOT_INITIALIZED", "config": config["config_id"],
                       "state_read_only": True, "mathematicalAcceptance": False})
    database = domains.state / "control.sqlite3"
    if op == "status" and not (domains.state / "owner.lock").exists():
        require(not database.exists(), "STATE_LOCK_MISSING")
        return absent()
    with owner_lock(domains.state, create=False):
        if op == "status" and not database.exists():
            return absent()
        store = ControlStore(domains.state, config["config_id"], config["limits"], event,
                             create=False, readonly=op == "status", scratch=domains.scratch)
        try:
            return encode(status(store, domains)) if op == "status" else store.renew(raw, parsed)
        finally:
            store.close()


def main():
    parser = argparse.ArgumentParser()
    for name in ("config", "state", "request", "event"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    event = {"sql_vm_steps": 0, "sql_opened": False, "sql_rows": {}, "stages_allocated": 0,
             "checker_loaded": False, "renewal_historical": False, "operation": None}
    require_python_profile()
    config = load_config(args.config)
    domains = Domains.from_config(config)
    domains.require_state(args.state)
    require(args.event.is_absolute() and args.event.parent.is_dir() and not args.event.exists()
            and args.event.resolve().is_relative_to(domains.scratch), "EVENT_SCRATCH_DOMAIN")
    try:
        raw = read(args.request, 16384)
        event["request_sha256"] = digest(raw)
        reply = run(config, raw, event)
    except Refusal as error:
        unknown = error.code == "RENEWAL_OUTCOME_UNKNOWN"
        result = {"status": "BLOCKED" if unknown else "REFUSED", "code": error.code,
                  "detail": error.detail[:512], "mathematicalAcceptance": False}
        # Even malformed envelopes can be classified before operation selection:
        # a non-unknown Refusal has not committed a renewal. Status never does.
        result.update(grant_recorded=None if unknown else False,
                      state_outcome="UNKNOWN" if unknown else "UNCHANGED_BY_RENEWAL")
        reply = encode(result)
    except Exception as error:
        reply = encode({"status": "BLOCKED", "code": "RENEWAL_OUTCOME_UNKNOWN"
            if event["operation"] == "renew" else "ADMIN_OUTCOME_UNKNOWN",
            "detail": type(error).__name__ + ":" + str(error)[:512],
            "grant_recorded": None, "state_outcome": "UNKNOWN", "mathematicalAcceptance": False})
    require(len(reply) <= 65536, "ADMIN_RESPONSE_BOUND")
    event["elapsed_seconds"] = time.monotonic() - started
    event["response_sha256"] = digest(reply)
    payload = encode(event)
    require(len(payload) <= 65536, "ADMIN_EVENT_BOUND")
    with args.event.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    sys.stdout.buffer.write(reply)
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

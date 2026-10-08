"""Finite operator-selected service of one committed local exposure view.

Started only through the owner's process supervisor. This worker never imports
the mathematical checker, runs Lean, or updates the node's control database.
"""
from __future__ import annotations

import argparse
import importlib
from pathlib import Path
import re
import sys

from domains import Domains, require_python_profile
from inspect_context import ReadOnlyControl
from node import load_config, SAFE_ID
from storage import Refusal, decode, digest, encode, owner_lock, read, require

MIB = 1048576


def selected_pin(pin, expected):
    require(type(pin) is dict and set(pin) == {"path", "bytes", "sha256"}, "SERVICE_PIN")
    require(type(pin["bytes"]) is int and 0 < pin["bytes"] <= MIB
            and type(pin["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]), "SERVICE_PIN")
    require(Path(pin["path"]).resolve(strict=True) == expected.resolve(strict=True), "SERVICE_PIN_PATH")
    raw = read(expected, MIB)
    require(len(raw) == pin["bytes"] and digest(raw) == pin["sha256"], "SERVICE_PIN_CHANGED")
    return raw


def validate_selection(control, config, client, view, parsed, peer):
    """Authenticate each exact authority shape without reopening source packages."""
    selected = view["selected"]
    require(type(selected) is list and 1 <= len(selected) <= 32
            and len(parsed["entries"]) == len(selected), "VIEW_SELECTION_COUNT")
    seen = set()
    for row, entry in zip(selected, parsed["entries"]):
        require(type(row) is dict and row.get("provider") == "P1"
                and type(row.get("sequence")) is int and 1 <= row["sequence"] <= 8192
                and row["sequence"] not in seen, "VIEW_SELECTED_ROW")
        seen.add(row["sequence"])
        require(encode(row.get("descriptor_id")) == encode(entry["descriptor_id"]),
                "VIEW_SELECTED_ENTRY")
        if set(row) == {"provider", "sequence", "descriptor_id", "publication"}:
            publication = control.require_published("P1", row["sequence"], row["descriptor_id"])
            require(row["publication"] == publication, "VIEW_PUBLICATION_BINDING")
            offer = control.entry("P1", row["sequence"])
            require(encode(offer["descriptor_id"]) == encode(entry["descriptor_id"])
                    and encode(offer["formal_metadata"]) == encode(entry["formal_metadata"])
                    and offer["package"]["manifest_sha256"].lower() == entry["manifest_sha256"],
                    "VIEW_PUBLICATION_ENTRY")
        elif set(row) == {"provider", "sequence", "descriptor_id", "basis", "acquisition"}:
            require(len(selected) == 1 and row["basis"] == "replica-custody",
                    "VIEW_REPLICA_SELECTION")
            acquisition, remote, _offer = peer.replica_custody(
                control, config, client, row["acquisition"])
            require(row["sequence"] == acquisition["sequence"]
                    and encode(row["descriptor_id"]) == encode(acquisition["descriptor_id"])
                    and encode(view["foundation"]) == encode(remote["foundation"])
                    and encode(entry) == encode(remote["entry"]), "VIEW_REPLICA_ENTRY")
        else:
            raise Refusal("VIEW_SELECTED_ROW")


def operation(config, state, value, event):
    domains = Domains.from_config(config)
    domains.require_state(state)
    require(type(value) is dict and set(value) == {
        "op", "session", "client", "view", "port", "seconds", "max_requests", "max_bytes"}, "SERVICE_FIELDS")
    require(value["op"] == "serve" and type(value["session"]) is str
            and SAFE_ID.fullmatch(value["session"]), "SERVICE_SESSION")
    require(type(value["client"]) is str and value["client"] in config["clients"], "UNKNOWN_CLIENT")
    for name, low, high in (("port", 1, 65535), ("seconds", 1, 360),
                          ("max_requests", 1, 128), ("max_bytes", 1, 256*MIB)):
        require(type(value[name]) is int and low <= value[name] <= high, "SERVICE_LIMIT:" + name)
    services = domains.scratch / "services"
    session = services / value["session"]
    require(session.is_dir() and not (session / "ready.json").exists(), "NEW_SERVICE_SESSION_REQUIRED")
    # One service per node scratch domain. This lock never substitutes for the
    # outer supervisor's process-tree quiescence evidence.
    with owner_lock(services):
        control = ReadOnlyControl(domains.state, config["config_id"], event)
        try:
            view = control.record(value["view"], "view", value["client"])
            require(type(view) is dict and set(view) == {
                "kind", "directory", "foundation", "catalog", "complete", "selected", "mathematicalAcceptance"}
                and view["kind"] == "peer_view" and view["mathematicalAcceptance"] is False, "VIEW_RECORD")
            directory = Path(view["directory"])
            require(directory.is_absolute() and directory.name == "peer-view"
                    and directory.resolve(strict=True).parent.parent == domains.state / "work", "VIEW_PATH")
            catalog = selected_pin(view["catalog"], directory / "catalog.json")
            complete = decode(selected_pin(view["complete"], directory / "complete.json"))
            require(encode(complete) == encode({"schema": 1, "foundation": view["foundation"],
                    "catalog_sha256": digest(catalog)}), "VIEW_COMPLETION_BINDING")
            # peer_node's shared helper is ledger-only; importing it imports
            # inert wire/transport, never checking.py or a native allocator.
            for name in ("peer_wire", "peer_service", "peer_node"):
                selected_pin(config["files"][name], domains.install / "py" / (name + ".py"))
            wire = importlib.import_module("peer_wire")
            service = importlib.import_module("peer_service")
            peer = importlib.import_module("peer_node")
            for name, module in (("peer_wire", wire), ("peer_service", service), ("peer_node", peer)):
                require(Path(module.__file__).resolve() == domains.install / "py" / (name + ".py"),
                        "SERVICE_MODULE_PATH")
            parsed = wire.parse_catalog(catalog, view["foundation"])
            validate_selection(control, config, value["client"], view, parsed, peer)
        finally:
            control.close()
        observations = service.serve(directory, value["port"], session / "ready.json",
            session_seconds=value["seconds"], max_requests=value["max_requests"], max_bytes=value["max_bytes"])
        return {"status": "SERVICE_STOPPED", "session": value["session"], "view": value["view"],
                "catalog_sha256": digest(catalog), "observations": observations,
                "mathematicalAcceptance": False, "native_stages": 0}


def main():
    parser = argparse.ArgumentParser()
    for name in ("config", "state", "request", "event"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    require_python_profile()
    config = load_config(args.config)
    domains = Domains.from_config(config)
    event_path = args.event.resolve()
    require(event_path.is_relative_to(domains.scratch / "services") and event_path.parent.is_dir()
            and not event_path.exists(), "SERVICE_EVENT_PATH")
    raw = read(args.request, 16384)
    event = {"sql_vm_steps": 0, "sql_rows": {}, "sql_opened": False,
             "checker_loaded": False, "native_stages": 0, "request_sha256": digest(raw)}
    try:
        result = operation(config, args.state, decode(raw), event)
    except Exception as error:
        result = {"status": "SERVICE_REFUSED", "code": getattr(error, "code", type(error).__name__),
                  "detail": str(error)[:1024], "mathematicalAcceptance": False, "native_stages": 0}
    reply = encode(result)
    event["response_sha256"] = digest(reply)
    with args.event.open("xb") as stream:
        stream.write(encode(event))
    sys.stdout.buffer.write(reply)
    return 0 if result["status"] == "SERVICE_STOPPED" else 1


if __name__ == "__main__":
    raise SystemExit(main())

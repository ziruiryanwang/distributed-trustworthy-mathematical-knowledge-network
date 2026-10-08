"""Owner-local product commands. Development cut; not a qualified release.

Run with Python -B -E -s -S. The explicit installed module directory replaces
ambient user/site-package discovery. Request source remains owner-authorized.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid

INSTALL = Path(__file__).resolve().parent
sys.path.insert(0, str(INSTALL / "py"))

from domains import Domains
from storage import decode, encode, read, require

MIB = 1048576


def pin(path):
    path = Path(path).resolve(strict=True)
    raw = read(path, 16 * MIB)
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def save_new(path, value):
    raw = encode(value)
    require(len(raw) <= MIB, "OWNER_RECORD_BOUND")
    with Path(path).open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def configure(args):
    """Create configuration, never an accepted context or preloaded theorem."""
    state, scratch, runtime = (value.resolve() for value in (args.state, args.scratch, args.lean_runtime))
    require(not state.exists() and not scratch.exists(), "FRESH_STATE_AND_SCRATCH_REQUIRED")
    clients = args.client or ["local"]
    from node import SAFE_ID, bounded_int, context_package_limit
    from capacity import initial_authorization, physical_supply
    initial_requests = bounded_int(getattr(args, "initial_requests", 128), 1, 4096, "INITIAL_REQUESTS")
    initial_stages = bounded_int(getattr(args, "initial_stages", 16), 1, 256, "INITIAL_STAGES")
    reserved_mib = bounded_int(getattr(args, "initial_reserved_mib", 4096), 136, 65536, "INITIAL_RESERVED_MIB")
    metadata_mib = getattr(args, "initial_metadata_mib", 32)
    require(type(metadata_mib) is int and metadata_mib in (32, 64, 128, 256), "INITIAL_METADATA_MIB")
    initial_limits = {"requests": initial_requests, "stages": initial_stages,
        "staging_bytes": reserved_mib * MIB, "metadata_pages": metadata_mib * MIB // 4096,
        "stage_bytes": 128 * MIB, "request_bytes": 8 * MIB}
    initial = initial_authorization(initial_limits)
    common_names = ("subtype", "val", "property", "injective", "ext")
    package_limit = context_package_limit(getattr(args, "context_packages", 16), len(common_names))
    require(1 <= len(clients) <= 16 and len(set(clients)) == len(clients)
            and all(type(client) is str and SAFE_ID.fullmatch(client) and client != "owner" for client in clients),
            "CONFIG_CLIENTS")
    peers = {}
    selections = getattr(args, "peer", None) or []
    require(len(selections) <= 2, "CONFIG_PEERS")
    for selection in selections:
        parts = selection.split("=")
        require(len(parts) == 2 and SAFE_ID.fullmatch(parts[0]) and parts[0] not in peers
                and parts[1].isascii() and parts[1].isdecimal(), "CONFIG_PEER")
        port = int(parts[1])
        require(1 <= port <= 65535, "CONFIG_PEER_PORT")
        peers[parts[0]] = {"host": "127.0.0.1", "port": port}
    files = {}
    for key, relative in {
        "seed": "assets/foundation/seed-verified.json",
        "inventory": "assets/foundation/seed-inventory-json.json",
        "source_codec": "py/source_codec.py", "codec": "py/codec.py",
        "symbol_index": "py/symbol_index.py", "agent_client": "native/AgentClient.lean",
        "core_olean": "build/lib/AgentReplayCore.olean",
        "bootstrap_olean": "build/lib/BootstrapSupport.olean",
        "checking": "py/checking.py", "runner": "py/run_stage.py", "domains": "py/domains.py",
        "peer_wire": "py/peer_wire.py", "peer_service": "py/peer_service.py", "peer_node": "py/peer_node.py",
    }.items():
        files[key] = pin(INSTALL / relative)
    files["lean"] = pin(runtime / "bin/lean.exe")
    from build import assets, read_record
    asset_pin = assets()
    build = read_record(INSTALL / "build/build-receipt.json")
    require(build["status"] == "LOCAL_SUPPORT_BUILD_COMPLETED_NOT_MATH_ACCEPTANCE", "SUPPORT_BUILD_REQUIRED")
    require(build["lean"] == files["lean"] and build["outputs"] == {
        "bootstrap_olean": files["bootstrap_olean"], "core_olean": files["core_olean"]}, "LOCAL_SUPPORT_BUILD_BINDING")
    require(build["assets_lock"] == asset_pin and build["sources"] == {
        name: pin(INSTALL / "native" / (name + ".lean"))
        for name in ("BootstrapSupport", "AgentReplayCore", "AgentClient")}, "BUILD_SOURCE_BINDING")
    config = {
        "schema": 3, "domains": {"install": str(INSTALL), "state": str(state),
            "scratch": str(scratch), "lean_runtime": str(runtime)},
        "files": files, "clients": clients, "peers": peers, "owner_source_execution": True,
        "common": {"packages": [{"path": str(INSTALL / "assets/common" / name),
            "manifest_sha256": pin(INSTALL / "assets/common" / name / "manifest.json")["sha256"]}
            for name in common_names]},
        "offers": [],
        "limits": {**initial_limits, "native_seconds": 300, "native_memory_mib": 4096,
            "entries": 8192, "request_bytes": 8*MIB, "source_bytes": 65536,
            "peer_request_bytes": 64*MIB, "expose_request_bytes": 80*MIB,
            "packages": package_limit, "canonical_bytes": 64*MIB, "inprocess_seconds": 120},
    }
    Domains.from_config(config)
    supply = physical_supply(state, scratch, initial["reserved_bytes"], initial["metadata_pages"])
    # These are explicitly selected new operator paths; failure is retained.
    state.mkdir(parents=True, exist_ok=False)
    scratch.mkdir(parents=True, exist_ok=False)
    path = state / "config.json"
    save_new(path, config)
    from node import load_config
    load_config(path)
    return {"status": "CONFIGURED_NOT_INITIALIZED", "config": pin(path),
            "acceptance": False, "capacity_policy": "finite cumulative authorization; explicit owner renewal",
            "initial_physical_supply": supply}


def invoke(args):
    """Public-process supervision; this command never promotes state itself."""
    import run_stage
    import supervise
    from node import load_config
    config = load_config(args.config)
    domains = Domains.from_config(config)
    require(domains.install == INSTALL, "CALLING_INSTALLATION_BINDING")
    raw = read(args.request, 16384 if args.command == "inspect" else 131072)
    selected_op = decode(raw).get("op") if args.command == "request" else None
    evidence = domains.scratch / "calls"
    evidence.mkdir(parents=True, exist_ok=True)
    module = "inspect_context.py" if args.command == "inspect" else "node.py"
    names = [module, "run_stage.py", "storage.py", "capacity.py", "checking.py", "domains.py", "supervise.py"]
    if module != "node.py":
        names.append("node.py")
    if module == "node.py":
        names.extend(["peer_wire.py", "peer_service.py", "peer_node.py"])
    pins = [pin(sys.executable), pin(args.config), *[pin(INSTALL / "py" / name) for name in names]]
    limits = {"pins": pins, "wall_seconds": 450, "cpu_seconds": 450,
        "memory_mib": 6144, "active_processes": 8, "stdout_bytes": MIB,
        "stderr_bytes": 65536, "event_bytes": 65536}
    if selected_op in {"peer_find", "peer_acquire", "expose", "replica_expose"}:
        limits.update(wall_seconds=120, cpu_seconds=120, memory_mib=1024)
    transport = supervise.Transport(sys.executable, INSTALL / "py" / module,
        args.config, domains.state, evidence, run_stage, limits)
    name = "call-" + uuid.uuid4().hex
    try:
        response = transport(name, raw)
    except supervise.SupervisorFailure:
        # Detailed receipt remains in scratch. Never infer mathematical refusal
        # or safe automatic retry from a transport/process-tree failure.
        return {"status": "TRANSPORT_FAILED", "evidence": str(evidence / name),
                "accepted": None, "state_outcome": "UNKNOWN"}
    if response["returncode"] != 0:
        return {"status": "TRANSPORT_FAILED", "evidence": str(evidence / name),
                "code": "PUBLIC_WORKER_EXIT", "accepted": None, "state_outcome": "UNKNOWN"}
    sys.stdout.buffer.write(response["stdout"])
    sys.stdout.buffer.flush()
    return None


def serve(args):
    """Issue one explicit finite service grant; never automatically restart it."""
    import run_stage
    import supervise
    from node import load_config, SAFE_ID
    config = load_config(args.config)
    domains = Domains.from_config(config)
    require(domains.install == INSTALL, "CALLING_INSTALLATION_BINDING")
    require(SAFE_ID.fullmatch(args.session) and args.session.upper() not in supervise.RESERVED_NAMES,
            "SERVICE_SESSION")
    require(args.client in config["clients"], "UNKNOWN_CLIENT")
    require(1 <= args.port <= 65535 and 1 <= args.seconds <= 360
            and 1 <= args.max_requests <= 128 and 1 <= args.max_bytes <= 256*MIB, "SERVICE_LIMIT")
    root = domains.scratch / "services" / args.session
    root.mkdir(parents=True, exist_ok=False)
    cases = root / "cases"
    cases.mkdir()
    names = ["service_worker.py", "inspect_context.py", "node.py", "storage.py", "capacity.py", "domains.py",
             "run_stage.py", "supervise.py", "peer_wire.py", "peer_service.py", "peer_node.py"]
    pins = [pin(sys.executable), pin(args.config), *[pin(INSTALL / "py" / name) for name in names]]
    limits = {"pins": pins, "wall_seconds": args.seconds + 30, "cpu_seconds": 120,
              "memory_mib": 256, "active_processes": 8, "stdout_bytes": 65536,
              "stderr_bytes": 65536, "event_bytes": 65536, "request_bytes": 16384}
    request = {"op": "serve", "session": args.session, "client": args.client, "view": args.view,
               "port": args.port, "seconds": args.seconds, "max_requests": args.max_requests,
               "max_bytes": args.max_bytes}
    save_new(root / "grant.json", {"schema": 1, "request": request, "limits": limits,
        "policy": "one explicitly issued local session; no automatic retries or counter reset"})
    transport = supervise.Transport(sys.executable, INSTALL / "py/service_worker.py", args.config,
                                     domains.state, cases, run_stage, limits)
    try:
        response = transport("serve", encode(request))
    except supervise.SupervisorFailure:
        return {"status": "SERVICE_TRANSPORT_FAILED", "evidence": str(root),
                "service_outcome": "UNKNOWN", "mathematicalAcceptance": False}
    result = decode(response["stdout"]) if response["returncode"] != 0 else None
    if result is not None:
        return {"status": "SERVICE_REFUSED", "worker": result, "evidence": str(root),
                "mathematicalAcceptance": False}
    # Service observations include finite timing floats, so forward exact bytes.
    sys.stdout.buffer.write(response["stdout"])
    sys.stdout.buffer.flush()
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    config = commands.add_parser("configure", help="new empty-offer node; requires locally rebuilt support")
    config.add_argument("--state", required=True, type=Path)
    config.add_argument("--scratch", required=True, type=Path)
    config.add_argument("--lean-runtime", required=True, type=Path)
    config.add_argument("--client", action="append")
    config.add_argument("--peer", action="append", help="explicit loopback peer alias=port; at most two")
    config.add_argument("--context-packages", type=int, default=16,
                        help="initial per-context package limit, 5..16; immutable after configuration")
    config.add_argument("--initial-requests", type=int, default=128)
    config.add_argument("--initial-stages", type=int, default=16)
    config.add_argument("--initial-reserved-mib", type=int, default=4096)
    config.add_argument("--initial-metadata-mib", type=int, default=32)
    status = commands.add_parser("status", help="bounded read-only node status; no ordinary reservation")
    status.add_argument("--config", required=True, type=Path)
    for name in ("request", "inspect", "recover", "renew"):
        command = commands.add_parser(name)
        command.add_argument("--config", required=True, type=Path)
        command.add_argument("--request", required=True, type=Path)
    service = commands.add_parser("serve", help="serve one committed view in an explicitly bounded loopback session")
    service.add_argument("--config", required=True, type=Path)
    service.add_argument("--client", required=True)
    service.add_argument("--view", required=True)
    service.add_argument("--session", required=True)
    service.add_argument("--port", required=True, type=int)
    service.add_argument("--seconds", type=int, default=60)
    service.add_argument("--max-requests", type=int, default=128)
    service.add_argument("--max-bytes", type=int, default=256*MIB)
    hosting = commands.add_parser("host", help="continue one finite cumulative owner loopback hosting grant")
    hosting.add_argument("--config", required=True, type=Path)
    hosting.add_argument("--grant", required=True, type=Path)
    args = parser.parse_args()
    require(sys.dont_write_bytecode and sys.flags.ignore_environment and sys.flags.no_site
            and sys.flags.no_user_site, "RUN_PYTHON_WITH_B_E_s_S")
    try:
        if args.command == "configure":
            result = configure(args)
        elif args.command == "serve":
            result = serve(args)
        elif args.command == "host":
            from hosting import invoke_host
            result = invoke_host(args, owner_entrypoint=Path(__file__))
        elif args.command == "recover":
            from recovery_manage import invoke_recovery
            result = invoke_recovery(args, owner_entrypoint=Path(__file__))
        elif args.command in {"status", "renew"}:
            from admin_manage import invoke_admin
            result = invoke_admin(args, owner_entrypoint=Path(__file__))
        else:
            result = invoke(args)
    except Exception as error:
        result = {"status": "OWNER_COMMAND_FAILED", "code": getattr(error, "code", type(error).__name__),
                  "detail": str(error)[:1024], "accepted": None, "state_outcome": "UNKNOWN"}
        sys.stdout.buffer.write(encode(result))
        return 1
    if result is not None:
        sys.stdout.buffer.write(encode(result))
    return 1 if result is not None and result.get("status") in {
        "TRANSPORT_FAILED", "SERVICE_TRANSPORT_FAILED", "SERVICE_REFUSED", "ADMIN_TRANSPORT_FAILED",
        "REFUSED", "BLOCKED", "HOST_HALTED"} else 0


if __name__ == "__main__":
    raise SystemExit(main())

"""One actual loopback bootstrap/Noise/descriptor -> same-budget HTTP discovery.

Retained old-policy index metadata only: no index rebuild, native/proof run or
mathematical admission. Root selects exact inputs/ports and supervises all
children in the single finite parent Job. No search endpoint is injected.
"""
from pathlib import Path
import argparse
import asyncio
import hashlib
import json
import os
import sqlite3
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C
from discovery import formal_features as F
from discovery.discovery_store import Store
from discovery.module_export_adapter import ModuleExportAdapter, compile_query
from transport.candidate_integration import (RecordingProvider, OFFER_BYTES, CANDIDATE_LIMITS,
    SESSION_LIMITS, EXPECTED_OBJECT, EXPECTED_LOCATOR)
from transport.summary_integration import read_pin, save
from location import protocol as P
from location.controller import AdoptedLocationRuntime, SOURCE_NAMES, ROOT
from location.controller_roles import RoleLocationProcess, RoleLocatedWorkflow, ROLE_NAMES


def config(role, state, namespace, port, policy, endpoint=None, bootstrap=()):
    return {"schema": "DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", "role": role,
        "state": str(state), "namespace": namespace, "egress": policy,
        "listen": [f"/ip4/127.0.0.1/tcp/{port}"], "announce": [], "bootstrap": list(bootstrap),
        "endpoints": [] if role == "reader" else [endpoint],
        "limits": {"service_ms": 120000, "operation_ms": 15000, "query_events": 256, "provider_limit": 4,
            "advertised_keys": 2, "provider_ttl_ms": 120000, "reprovide_interval_ms": 30000,
            "maintenance_ms": 60000, "commands": 12, "descriptor_requests": 4, "descriptor_reply_bytes": 16384,
            "metadata": {}, "transport": {"outbound_attempts": 64, "inbound_upgrades": 64,
                "receive_bytes": 2*1024**2, "send_bytes": 2*1024**2}}}


async def run(args, out, report):
    original = read_pin(args.database, args.database_sha, 64*1024**2)
    bundle = C.parse_json(read_pin(args.bundle, args.bundle_sha, 2**20))
    F.need(C.module_id(bundle["spec"]) == bundle["module"], "LOCATION_INPUT_MODULE_BINDING")
    adapter = ModuleExportAdapter(C, bundle["spec"]["foundation"], bundle["spec"]["policy"])
    features = compile_query(adapter.namespace, [
        {"tag": "declaration-kind", "value": "theorem"},
        {"tag": "result-head", "head": {"tag": "const", "symbol": {"kind": "foundation-name",
         "name_hash": C.hash_value("foundation-symbol", [["s", "Eq"]])}}}])
    for port in (args.provider_port, args.reader_port): F.uint(port, 1024, 65535, "LOCATION_SELECTED_TEST_PORT")
    F.need(args.provider_port != args.reader_port, "LOCATION_DISTINCT_TEST_PORTS")
    index_root = out / "retained-index"; index_root.mkdir()
    database = index_root / "discovery.sqlite"
    with database.open("xb") as stream: stream.write(original)
    del original
    db = sqlite3.connect(database.as_uri()+"?mode=ro&immutable=1", uri=True)
    try: cfg = F.strict(bytes(db.execute("SELECT cfg FROM meta WHERE id=1").fetchone()[0]), 16384)
    finally: db.close()
    index = Store(index_root, adapter, cfg["limits"])
    http = RecordingProvider(index, out)
    source = Path(__file__).resolve().parent
    base_pins = {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in SOURCE_NAMES}
    role_pins = {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in ROLE_NAMES}
    adoption = AdoptedLocationRuntime(source, base_pins)
    nodes = []; workflow = search = None
    try:
        endpoint = await http.start()
        F.need(endpoint.port not in (args.provider_port, args.reader_port), "LOCATION_HTTP_DHT_PORT_COLLISION")
        policy_config = {"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test", "public_ports": [],
            "test_endpoints": [{"host": "127.0.0.1", "port": port} for port in sorted((endpoint.port, args.provider_port, args.reader_port))]}
        policy = P.OwnerEgressPolicy(policy_config)
        ep = {"host": endpoint.host, "port": endpoint.port, "tls": endpoint.tls, "server_name": endpoint.server_name}
        reader_config = config("reader", out / "reader-state", adapter.namespace, args.reader_port, policy_config)
        # This real Node child exercises only new role guards; no runtime
        # packages or sockets. It does not rerun any prior protocol tests.
        role_input = out / "role-control-config.json"; raw = F.compact(reader_config)
        with role_input.open("xb") as stream: stream.write(raw)
        env = {key: value for key, value in os.environ.items() if not key.upper().startswith("NODE")}
        role_child = await asyncio.create_subprocess_exec(str(adoption.node), str(source / "role_controls.mjs"),
            str(role_input), hashlib.sha256(raw).hexdigest(), cwd=ROOT, env=env,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, limit=65536)
        try: stdout, stderr = await asyncio.wait_for(role_child.communicate(), 15)
        except BaseException: role_child.kill(); await role_child.wait(); raise
        F.need(role_child.returncode == 0 and len(stdout) <= 16384 and len(stderr) <= 16384, "LOCATION_ROLE_CONTROL_RESULT")
        report["role_controls"] = json.loads(stdout)
        F.need(report["role_controls"]["status"] == "PASS", "LOCATION_ROLE_CONTROL_PASS")

        deadline = time.monotonic()+150
        provider_config = config("index-provider", out / "provider-state", adapter.namespace,
                                 args.provider_port, policy_config, ep)
        provider = RoleLocationProcess(adoption, role_pins, provider_config, out / "provider-controller", deadline=deadline)
        nodes.append(provider); provider_ready = await provider.start()
        peer = P.peer_id(provider_ready["peer_id"])
        bootstrap = f"/ip4/127.0.0.1/tcp/{args.provider_port}/p2p/{peer}"
        reader_config["bootstrap"] = [bootstrap]
        reader = RoleLocationProcess(adoption, role_pins, reader_config, out / "reader-controller", deadline=deadline)
        nodes.append(reader); reader_ready = await reader.start()
        F.need(reader_ready["role"] == "reader" and reader_config["endpoints"] == []
               and len(reader_ready["joins"]) == 1 and reader_ready["joins"][0]["status"] == "CONNECTED", "LOCATION_ACTUAL_BOOTSTRAP_JOIN")
        save(out / "provider-ready.json", provider_ready); save(out / "reader-ready.json", reader_ready)
        published = await provider.command("publish", {"features": features, "stripe": 0})
        F.need(published["route_key"] == P.route_key(adapter.namespace, features, 0)
               and published["status"] == "ADVERTISED_HINT", "LOCATION_PROVIDER_HINT_PUBLISHED")
        location_limits = dict(wall_ms=45000, route_operations=1, routing_events=256, routing_peer_slots=4,
                               descriptor_requests=1, contacts=4, reply_bytes=SESSION_LIMITS["bytes"]+4096)
        workflow = RoleLocatedWorkflow(reader, adapter.namespace, features, location_limits, SESSION_LIMITS, policy)
        initial = workflow.report(); save(out / "consumer-initial.json", initial)
        F.need(initial["workflow"]["contacts"] == 0 and not initial["workflow"]["search_issued"], "LOCATION_NO_PRESEEDED_SEARCH_CONTACT")
        located = await workflow.route(features, event_cap=256, peer_cap=4)
        F.need(peer in located["peers"], "LOCATION_ACTUAL_DHT_PROVIDER")
        contact = await workflow.descriptor(peer, located["route_key"], max_bytes=4096, max_age_ms=30000)
        F.need(contact["status"] == "ADOPTED_ADVISORY_CONTACTS" and len(contact["contacts"]) == 1, "LOCATION_ACTUAL_NOISE_DESCRIPTOR")
        search = workflow.begin_search(); selected_contact = contact["contacts"][0]
        F.need(search.endpoints[selected_contact] == endpoint, "LOCATION_RETURNED_ENDPOINT_MATCHES_PROVIDER")
        offered = await search.offer(selected_contact, OFFER_BYTES, max_expanded_bytes=1048576, max_age_ms=60000)
        selected = next((row for row in offered["partitions"] if row["anchor_count"] > 0), None)
        F.need(selected is not None and offered["mathematical_acceptance"] is False, "LOCATION_ACTUAL_OFFER")
        page = await search.candidates(selected_contact, offered["snapshot_id"], selected["partition"], 0, CANDIDATE_LIMITS)
        F.need(page["status"] == "VERIFIED_CANDIDATES" and page["mathematical_acceptance"] is False
               and page["verified_scan_coverage"] is False and len(page["matches"]) == 1
               and page["matches"][0]["object_id"] == EXPECTED_OBJECT and page["matches"][0]["locator"] == EXPECTED_LOCATOR,
               "LOCATION_EXACT_RETAINED_METADATA_CANDIDATE")
        F.need(workflow.report()["workflow"]["pending_requests"] == 0
               and search.report()["session"]["pending_requests"] == 0
               and search.report()["session"]["used"]["requests"] == 2, "LOCATION_SAME_FINITE_WORKFLOW")
        save(out / "located.json", located); save(out / "contact.json", contact)
        save(out / "offered.json", offered); save(out / "candidate.json", page)
        report.update(initial_contacts=0, endpoint_origin="ACTUAL_NOISE_DESCRIPTOR_ADOPTED_BY_SAME_WORKFLOW",
            route_origin="OWNER_QUERY_FEATURES_AND_BOOTSTRAP_ONLY", candidate_count=1,
            candidate_record_id=F.record_id(page["matches"][0]), index_rebuilds=0,
            namespace=adapter.namespace, metadata_policy=bundle["spec"]["policy"], current_policy_receipt_acceptance=False)
        reader_final = await reader.command("status", {})
        F.need(reader_final["role"] == "reader" and reader_final["stats"]["descriptor_requests"] == 0
               and reader_final["stats"]["commands"] == 2, "LOCATION_READER_ONLY_LOCATE_AND_DESCRIPTOR")
        report["reader_before_stop"] = reader_final
        report["provider_before_stop"] = await provider.command("status", {})
        for node in reversed(nodes): await node.command("stop", {})
    finally:
        # One failed child close must not prevent attempting the other close.
        # Preserve every failure; the finite parent Job remains the hard stop.
        cleanup_errors = []
        for node in reversed(nodes):
            try: await node.close()
            except BaseException as error:
                cleanup_errors.append({"phase": "node-close", "role": node.config["role"],
                    "type": type(error).__name__, "message": str(error)[:1000]})
        try: await http.stop()
        except BaseException as error:
            cleanup_errors.append({"phase": "http-stop", "type": type(error).__name__, "message": str(error)[:1000]})
        try: index.close()
        except BaseException as error:
            cleanup_errors.append({"phase": "index-close", "type": type(error).__name__, "message": str(error)[:1000]})
        report["cleanup_errors"] = cleanup_errors
        report["node_reports"] = [node.report() for node in nodes]
        report["http_final"] = http.status(); report["http_calls"] = http.calls
        if workflow is not None: report["workflow_final"] = workflow.report()
        F.need(not cleanup_errors, "LOCATION_INTEGRATION_CLEANUP_FAILED")
    F.need(all(node.process is not None and node.process.returncode == 0 and not node.channel_failed
               and not node.forced_termination and node.pre is not None and node.post is not None
               and node.role_pre == node.role_post for node in nodes), "LOCATION_CLEAN_PINNED_NODE_EXIT")
    dbpath = out / "reader-state/metadata.sqlite"
    db = sqlite3.connect(dbpath.as_uri()+"?mode=ro&immutable=1", uri=True)
    try:
        # Reader role guards plus fresh state mean no owner publication intent.
        published = db.execute("SELECT count(*) FROM kv WHERE k LIKE '/application/published/%'").fetchone()[0]
        intents = db.execute("SELECT count(*) FROM kv WHERE k LIKE '/application/provider-intent/%'").fetchone()[0]
    finally: db.close()
    F.need(published == intents == 0, "LOCATION_READER_NO_PUBLICATION_INTENT")
    report["reader_publication_rows"] = published; report["reader_intent_rows"] = intents
    read_pin(args.database, args.database_sha, 64*1024**2); read_pin(args.bundle, args.bundle_sha, 2**20)
    F.need(http.server is None and not http.tasks and len(http.calls) == 2, "LOCATION_HTTP_CLEAN_CLOSE")
    report["status"] = "PASS"


def main():
    F.need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
           "LOCATION_INTEGRATION_INVOCATION")
    parser = argparse.ArgumentParser()
    for name in ("database", "database-sha", "bundle", "bundle-sha", "output"):
        parser.add_argument("--"+name, required=True)
    parser.add_argument("--provider-port", type=int, required=True); parser.add_argument("--reader-port", type=int, required=True)
    args = parser.parse_args(); out = Path(args.output)
    F.need(out.is_absolute() and out.resolve() == out and out.is_relative_to(ROOT / "experiments/v5-local-checks")
           and not out.exists(), "LOCATION_INTEGRATION_FRESH_OUTPUT")
    out.mkdir(); report = {"status": "FAIL", "schema": "DMKN_V5_ACTUAL_LOCATION_METADATA_INTEGRATION_V1",
        "mathematical_acceptance": False, "global_complete": False, "independent_host_evidence": False}
    try: asyncio.run(run(args, out, report))
    except BaseException as error:
        report["error"] = {"type": type(error).__name__, "message": str(error)[:2000]}; raise
    finally: save(out / "RESULT.json", report)
    print(json.dumps(report), flush=True)


if __name__ == "__main__": main()

"""One finite optional routing operator, separate from mathematical admission.

The launcher supplies pinned support, approved paths and original containment.
The custodian role checks new exact locator proposals before publishing. The
gateway role exposes only bounded asynchronous reads through its own Node child.
"""
from __future__ import annotations

import asyncio
import hashlib
import ipaddress
import ssl
import time
from pathlib import Path

SCHEMA = "DMKN_ORDINARY_EXPORT_OPERATOR_OPERATION_V1"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError("EXPORT_OPERATOR_"+code)


class OperationFailure(RuntimeError):
    def __init__(self, report, error):
        super().__init__("EXPORT_OPERATOR_FAILED:"+type(error).__name__+":"+str(error)[:500])
        self.report = report


def failure(error):
    return dict(type=type(error).__name__, message=str(error)[:1000])


def proposals(s, publication, semantic):
    """Read only the explicitly selected new bundle, using hash-derived paths."""
    s.fields(publication, ("bundle_directory", "manifest", "selected_export_ids",
                          "requests", "reply_bytes", "attempt_timeout_ms"), "PUBLICATION_FIELDS")
    s.fields(publication["manifest"], ("path", "sha256"), "MANIFEST_FIELDS")
    root = s.ordinary(publication["bundle_directory"], directory=True)
    path = s.ordinary(publication["manifest"]["path"])
    raw = s.read(path, 2*MIB)
    held = s.Delta.manifest(raw, s.hexid(publication["manifest"]["sha256"]), check_budget=s._check)
    need(held.semantic_id == semantic, "BUNDLE_SEMANTICS")
    inputs = [s.read(root/entry.relative_path, entry.raw_bytes)
              for batch in held.batches for entry in batch]
    result = s.Delta.prepare(raw, held.sha256, inputs,
        selected_export_ids=publication["selected_export_ids"], check_budget=s._check)
    need(s.read(path, 2*MIB) == raw, "MANIFEST_CHANGED")
    # This is an operational document with false flags, not mathematical syntax.
    return s.F.strict(result, s.Delta.MAX_PROPOSAL_BYTES), hashlib.sha256(result).hexdigest()


def tls_context(s, tls):
    if tls is None:
        return None
    s.fields(tls, ("cert_file", "key_file"), "TLS_FIELDS")
    certificate, key = s.ordinary(tls["cert_file"]), s.ordinary(tls["key_file"])
    need(0 < certificate.stat().st_size <= MIB and 0 < key.stat().st_size <= MIB, "TLS_FILE_BOUND")
    s._check()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(str(certificate), str(key))
    s._check()
    return context


async def operate(s, config, allowance, *, node_runtime_root, workspace, mode, output, ready):
    """Every call owns one child/service grant; partial publication is retained."""
    s.fields(config, ("schema", "node", "gateway", "publication", "withdraw_exports"), "CONFIG_FIELDS")
    need(config["schema"] == SCHEMA and mode in ("create", "reopen"), "CONFIG_SCHEMA_MODE")
    node = config["node"]
    need(type(node) is dict and node.get("semantic_id") == s.semantic_id and
         node.get("role") in ("gateway", "custodian"), "NODE_ROLE_SEMANTICS")
    is_gateway = node["role"] == "gateway"
    need((config["gateway"] is not None) == is_gateway and
         (not is_gateway or config["publication"] is None and config["withdraw_exports"] == []),
         "DISTINCT_OPERATOR_ROLES")
    withdrawn = config["withdraw_exports"]
    need(type(withdrawn) is list and len(withdrawn) <= 4096, "WITHDRAW_COUNT")
    for export in withdrawn:
        s.hexid(export)
    need(len(set(withdrawn)) == len(withdrawn), "WITHDRAW_DUPLICATE")
    need(callable(ready), "READY_CALLBACK")
    output = s.ordinary(output, directory=True)
    workspace = s.ordinary(workspace, directory=True)
    node_runtime_root = s.ordinary(node_runtime_root, directory=True)
    need(output.is_relative_to(workspace) and output != workspace, "OUTPUT_WORKSPACE")
    policy = s.modules["transport.contact_directory"].OwnerEgressPolicy(node["egress"])
    own_endpoint = None if is_gateway else policy.endpoint(node["endpoints"][0])
    bundle, bundle_sha = (None, None) if config["publication"] is None else \
        proposals(s, config["publication"], s.semantic_id)
    service_ms = s.uint(node["limits"]["service_ms"], 1000, 3600000, "SERVICE_MS")
    # This horizon begins before child setup. Runtime verification/startup and
    # publication consume it; the HTTP listener never receives a new lifetime.
    began = time.monotonic()
    horizon = began+service_ms/1000
    channel_deadline = allowance.deadline-10
    need(horizon <= channel_deadline and began < channel_deadline, "SERVICE_AND_CLEANUP_RESERVE")
    pins = {name: hashlib.sha256(s._bound.raws["node/"+name]).hexdigest()
            for name in s.L.SOURCE_NAMES}
    adoption = s.L.AdoptedLocationRuntime(s.root/"node", pins,
        installation_root=node_runtime_root, workspace_root=workspace)
    channel = s.L.OrdinaryLocationProcess(adoption, node, output/"node", mode=mode,
                                         deadline=channel_deadline, service_deadline=horizon)
    provider = gateway = ledger = None
    client = context = None
    checked_proposals = []
    # Reject deterministic operator configuration errors before Node startup,
    # withdrawals, publication or listener effects.
    if bundle is not None:
        grant = config["publication"]
        s.uint(grant["attempt_timeout_ms"], 1, 60000, "PUBLICATION_ATTEMPT_MS")
        ledger = s.O.OrdinaryBudget(deadline=horizon, requests=grant["requests"],
                                    reply_bytes=grant["reply_bytes"])
        client = s.O.OrdinaryAcquisition(s.OA.OrdinaryExportAdapter(s.semantic_id),
                                        {"own": own_endpoint}, ledger)
        locator_bytes = 0
        for row in bundle["proposals"]:
            allowance.check()
            locator = dict(schema=s.PP.LOCATOR_SCHEMA, semantic_id=s.semantic_id,
                           unit_id=row["unit_id"], export_name=row["name"])
            expected = s.F.compact(s.PP.read_locator(locator))
            need(0 < len(expected) <= s.O.LOCATOR_MAX, "PROPOSAL_LOCATOR_BOUND")
            locator_bytes += len(expected)
            need(locator_bytes <= 8*MIB, "PROPOSAL_LOCATOR_AGGREGATE")
            checked_proposals.append((row, locator, expected))
    if is_gateway:
        cfg = config["gateway"]
        s.fields(cfg, ("listener", "limits", "provider"), "GATEWAY_FIELDS")
        s.fields(cfg["listener"], ("host", "port", "tls"), "LISTENER_FIELDS")
        s.fields(cfg["provider"], ("max_connections", "max_requests", "max_reply_bytes", "operation_ms"),
                 "HTTP_PROVIDER_LIMITS")
        need(type(cfg["listener"]["host"]) is str, "LISTENER_HOST")
        address = ipaddress.ip_address(cfg["listener"]["host"])
        s.uint(cfg["listener"]["port"], 0, 65535, "LISTENER_PORT")
        context = tls_context(s, cfg["listener"]["tls"])
        need(not address.is_unspecified and not address.is_multicast and
             (address.is_loopback or context is not None), "LISTENER_POLICY")
        gateway = s.G.Gateway(channel, policy=policy, limits=cfg["limits"], deadline=horizon)
        provider = s.H.Provider(export_location=gateway, **cfg["provider"])
    report = dict(schema="DMKN_ORDINARY_EXPORT_OPERATOR_RESULT_V1", status="STARTED",
        role=node["role"], mode=mode, semantic_id=s.semantic_id,
        publication=[], withdrawals=[], cleanup_errors=[],
        mathematical_acceptance=False, custody_retention_guaranteed=False,
        service_horizon_scope="ORIGINAL_PYTHON_START_BEFORE_CHILD_SETUP_NO_RENEWAL")
    error = None
    try:
        report["node_ready"] = await channel.start()
        allowance.check()
        need(time.monotonic() < horizon, "STARTUP_CONSUMED_SERVICE")
        for export in withdrawn:
            report["withdrawals"].append(await channel.command("withdraw",
                dict(semantic_id=s.semantic_id, export_id=export), until=horizon))
        if bundle is not None:
            report["proposal"] = {key: value for key, value in bundle.items() if key != "proposals"}
            report["proposal"]["sha256"] = bundle_sha
            for row, locator, expected in checked_proposals:
                allowance.check()
                exact = await client.locator("own", s.semantic_id, row["export_id"],
                    len(expected), expected_name=row["name"], attempt_timeout_ms=grant["attempt_timeout_ms"])
                need(exact["raw"] == expected and exact["locator"] == locator, "OWN_CUSTODY_READBACK")
                published = await channel.command("publish",
                    dict(semantic_id=s.semantic_id, export_id=row["export_id"]), until=horizon)
                report["publication"].append(dict(export_id=row["export_id"],
                    unit_id=row["unit_id"], eligibility="EXACT_OWN_LOCATOR_READ_NOT_RETENTION_GUARANTEE",
                    locator_sha256=hashlib.sha256(expected).hexdigest(), publication=published))
            ledger.close()
            report["eligibility_acquisition"] = client.report()
        if is_gateway:
            endpoint = await provider.start(cfg["listener"]["host"], cfg["listener"]["port"],
                                             tls_context=context)
            report["http_endpoint"] = dict(host=endpoint.host, port=endpoint.port, tls=endpoint.tls)
        allowance.check()
        need(time.monotonic() < horizon, "READY_AFTER_SERVICE_HORIZON")
        ready(dict(schema="DMKN_ORDINARY_EXPORT_OPERATOR_READY_V1", role=node["role"],
            node=report["node_ready"], http_endpoint=report.get("http_endpoint"),
            remaining_ms=max(0, int((horizon-time.monotonic())*1000)), mathematical_acceptance=False))
        await asyncio.sleep(max(0, horizon-time.monotonic()))
        report["service_termination"] = "NATURAL_ORIGINAL_OPERATOR_HORIZON"
    except BaseException as caught:
        error = caught
        report["error"] = failure(caught)
    finally:
        # Close HTTP admission before asking the private channel to stop.
        if provider is not None:
            try:
                await provider.stop()
                need(provider.server is None and not provider.tasks and not provider._connections
                     and provider.reserved_reply_bytes == 0, "HTTP_CLOSURE")
            except BaseException as caught:
                report["cleanup_errors"].append(failure(caught))
            report["http"] = provider.status()
        if gateway is not None:
            report["gateway"] = gateway.report()
            if report["gateway"].get("terminal_failure") is True:
                report["cleanup_errors"].append(dict(type="GatewayTerminalFailure",
                    message="Backend failed; no successful service completion is inferred."))
        if not channel.closed and not channel.channel_failed and channel.process is not None \
                and channel.process.returncode is None:
            try:
                report["node_final_status"] = await channel.command("status", {}, until=channel_deadline)
                report["node_stop"] = await channel.command("stop", {}, until=channel_deadline)
            except BaseException as caught:
                report["cleanup_errors"].append(failure(caught))
        try:
            await channel.close()
        except BaseException as caught:
            report["cleanup_errors"].append(failure(caught))
        report["node"] = channel.report()
        if ledger is not None:
            try:
                ledger.close()
            except BaseException as caught:
                report["cleanup_errors"].append(failure(caught))
            report["eligibility_budget"] = ledger.report()
        if client is not None:
            report["eligibility_acquisition"] = client.report()
    clean = (not report["cleanup_errors"] and channel.closed and not channel.channel_failed
             and not channel.forced_termination and channel.process is not None
             and channel.process.returncode == 0)
    report["service_seconds_including_setup"] = time.monotonic()-began
    if error is not None or not clean:
        report["status"] = "FAILED_PARTIAL_EFFECTS_PRESERVED"
        raise OperationFailure(report, error or RuntimeError("UNCLEAN_OPERATOR_CLOSURE"))
    allowance.check()
    s.verify()
    report["status"] = "OPERATOR_SERVICE_CLOSED"
    return report

"""Finite direct-I discovery/use/contribution and onward structural circulation.

This is a trusted local owner using the installed public facade. The retained
receipt is untrusted provider data. No new prover, checker, protocol or grant
renewal is introduced. The second consumer stages only; it does not admit.
"""
import asyncio
from copy import deepcopy
import hashlib
from importlib import import_module
from pathlib import Path
import sys
import time

from admission.trust import TrustDomain
from aggregate_claims import bindings as B
from client import remote_reader
from client.runtime import RuntimeProfile, read_pin
from client.serve_workspace import _close_workspace
from client.workspace_validated import Workspace
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from evidence_network.custody import public_profile, profile_id
from evidence_network.packet import pack_terminal_i, parse_terminal_i
from evidence_network.transport import CompositeProvider
from mixed_claims.packet import parse_packet
from modules import codec as C

MIB = 1024**2
BASE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
BINARY = [["s", "CommonsV5"], ["s", "binary_congr"]]
TERNARY = [["s", "OwnerV5"], ["s", "ternary_congr"]]
PINS = {
    "receipt": (223594, "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"),
    "journal": (184, "22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682"),
    "bundle": (53769, "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926"),
    "foundation": (23313, "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"),
    "template": (551, "586f33a0623679a7fedef12b453d269e54c2206ded4bc48142b91568351824b3"),
}
HELPERS = {
    "formal_terms": "0ddbc8dac7e60180f3f9aad3216873158d8b2722a9d31c48112e20262298c642",
    "circulation": "43c3a2eeebcccdfa05c00855887068d98084755e6c5169168dab3787d3208978",
    "contribution": "ce82e170e1fad04beeb0be8722c89d748e381762b4957dfaf7b5850e2a57495c",
    "congruence_query": "07a323edd3b10f94f6fc7f9790191b1145666b547b4575c70c4a7261b3d8fadd",
}


def _helpers(context):
    original, result = list(sys.path), {}
    try:
        sys.path.insert(0, str(context.sources_owner))
        for name, digest in HELPERS.items():
            path = ordinary(context.sources_owner/(name+".py"), directory=False)
            F.need(context.source_sha256["owner/"+name+".py"] == digest
                   and hashlib.sha256(path.read_bytes()).hexdigest() == digest,
                   "TERMINAL_I_HELPER_PIN:"+name)
            module = import_module(name)
            F.need(Path(module.__file__).resolve() == path, "TERMINAL_I_HELPER_ORIGIN:"+name)
            result[name] = module
        return result
    finally:
        sys.path[:] = original


def _parameters(context, circulation):
    p = deepcopy(dict(context.parameters))
    F.fields(p, {"schema", "action", "runtime_adoption", "foundation", "receipt", "journal",
        "bundle", "template", "workspace_config", "provider_workspace_path", "first_workspace_path",
        "second_workspace_path", "first_domain_path", "first_domain_id", "second_domain_path",
        "second_domain_id", "operation_limits", "author_limits", "admission_limits"})
    F.need(p["schema"] == "DMKN_V5_TERMINAL_I_OWNER_V1"
           and p["action"] == "explicit-temporary-adoption-and-terminal-i-circulation",
           "TERMINAL_I_EXPLICIT_ACTION")
    F.need(p["operation_limits"] == circulation._operation_limits("first")
           and p["author_limits"] == circulation.AUTHOR
           and p["admission_limits"] == circulation.ADMISSION, "TERMINAL_I_FIXED_FINITE_CAPS")
    for name, (size, digest) in PINS.items():
        F.need(p[name]["bytes"] == size and p[name]["sha256"] == digest,
               "TERMINAL_I_RETAINED_PIN:"+name)
    image = p["workspace_config"]["wire_profile"]["aggregate_image"]
    F.need(profile_id(p["workspace_config"]["wire_profile"])
           == profile_id(public_profile(image, terminal_i=True)), "TERMINAL_I_EXPLICIT_V2")
    paths = {}
    for field in ("provider_workspace_path", "first_workspace_path", "second_workspace_path",
                  "first_domain_path", "second_domain_path"):
        path = ordinary(p[field], fresh=True)
        for base in (context.installation, context.run, context.sources_owner,
                     context.sources_v5, context.sources_portable, *paths.values()):
            base = Path(base)
            F.need(not path.is_relative_to(base) and not base.is_relative_to(path),
                   "TERMINAL_I_DISJOINT_STATE")
        paths[field] = path
    for phase in ("first", "second"): C.digest_string(p[phase+"_domain_id"])
    F.need(p["first_domain_id"] != p["second_domain_id"], "TERMINAL_I_SEPARATE_DOMAINS")
    work, run = ordinary(context.location_workspace), ordinary(context.run)
    F.need(work != run and work.is_relative_to(run), "TERMINAL_I_OUTPUT_SCOPE")
    F.need(context.limits["memory_mib"] == 1024 and context.limits["active_processes"] == 4
           and context.limits["cpu_seconds"] == 300 and context.limits["wall_seconds"] == 600,
           "TERMINAL_I_OUTER_ENVELOPE")
    return p, paths, work


def _seed(workspace, receipt, exact, bundle):
    """Public custody/index methods only; historical acceptance is ignored."""
    F.fields(bundle, {"schema", "module", "spec", "openings", "bodies",
                      "certificate_verification", "mathematical_admission"})
    F.need(bundle["schema"] == "DMKN_V5_OWNER_WORKLOAD_BUNDLE_V1"
           and bundle["module"] == C.module_id(bundle["spec"]) == BASE,
           "TERMINAL_I_BASE_FIXTURE")
    member = B.member_journal(exact)
    F.need(member["module"] == BASE and member["rank"] == 0
           and member["summary"] == C.summarize(bundle["spec"]), "TERMINAL_I_FIXTURE_J")
    opening = C.group_opening(bundle["spec"], 10)
    F.need(opening == bundle["openings"][10]
           and len(opening["group"]["declarations"]) == 1
           and opening["group"]["declarations"][0]["name"] == BINARY
           and opening["group"]["declarations"][0]["kind"] == "theorem",
           "TERMINAL_I_BINARY_OPENING")
    workspace.modules.put_group(BASE, opening)
    held, unused = workspace.modules.get_group(BASE, BINARY, 10)
    F.need(held == opening, "TERMINAL_I_SEED_GROUP_READBACK")
    raw = pack_terminal_i(exact, receipt, aggregate_image=workspace.config["wire_profile"]["aggregate_image"],
        envelope=workspace._envelope, terminal_receipt_bytes=workspace.config["terminal_receipt_bytes"],
        terminal_i=True)
    workspace.packets.put(BASE, raw)
    digest = hashlib.sha256(raw).hexdigest()
    F.need(workspace.packets.get(digest, len(raw)) == raw, "TERMINAL_I_SEED_PACKET_READBACK")
    workspace.index.admit(workspace.adapter.encode_opening(BASE, BINARY, opening),
                          expected_id=C.export_id(BASE, BINARY))
    return {"module": BASE, "packet_sha256": digest, "packet_bytes": len(raw),
            "groups": 1, "bodies": 0, "mathematical_acceptance": False}


def _check_output(workspace, result, contract, original_journal, receipt_sha):
    intent = result["publication"]["intent"]
    opening, descriptor = workspace.modules.get_group(intent["module"], TERNARY)
    F.need(descriptor["kind"] == "theorem" and descriptor["name"] == TERNARY
           and descriptor["universes"] == 4 and descriptor["type"] == contract,
           "TERMINAL_I_GENERIC_TERNARY_DESCRIPTOR")
    raw = workspace.packets.get(intent["packet_sha256"], intent["packet_bytes"])
    claims, frontiers, witnesses, census = parse_packet(raw, workspace._envelope,
        aggregate_image=workspace.config["wire_profile"]["aggregate_image"])
    F.need(len(claims) == len(frontiers) == len(witnesses) == 1
           and claims[0][0] == 0 and claims[0][1] == original_journal
           and hashlib.sha256(claims[0][2]).hexdigest() == receipt_sha
           and frontiers[0] == (0, original_journal, 0, ())
           and witnesses[0][1] == (original_journal,) and witnesses[0][3] == 1,
           "TERMINAL_I_ONWARD_EXACT_I_LINEAGE")
    witness = C.parse_json(witnesses[0][0])
    F.need(len(witness["parents"]) == 1
           and [item["index"] for item in witness["parents"][0]["openings"]] == [10],
           "TERMINAL_I_ONLY_SELECTED_PARENT_GROUP")
    return raw, {"module": intent["module"], "name": TERNARY, "universes": 4,
                 "type_sha256": hashlib.sha256(C.canonical(contract)).hexdigest(),
                 "packet_census": census, "mathematical_acceptance": False}


async def _phase(context, p, paths, work, phase, support, foundation, queries,
                 provider_workspace, template, helpers, detail):
    circulation = helpers["circulation"]
    workspace = client = provider = reader = domain = None
    detail.update(status="FAILED", stage="adopt", error=None, cleanup_errors=[],
        client_closed=False, workspace_closed=False, domain_withdrawn=False, service_closed=False)
    try:
        domain = TrustDomain.create(paths[phase+"_domain_path"], p[phase+"_domain_id"], support)
        detail["trust"] = domain.identity()
        runtime = RuntimeProfile.from_context(context, p["runtime_adoption"], trust_domain=domain)
        workspace = Workspace.open(paths[phase+"_workspace_path"], p["workspace_config"], create=True)
        grant = workspace.reserve(p["operation_limits"], outer_deadline=context.deadline-10)
        detail["operation_id"] = grant.identifier
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=phase == "first",
            foundation_bytes=foundation, foundation_sha256=p["foundation"]["sha256"])
        provider = CompositeProvider(index=provider_workspace.index, custody=provider_workspace.modules,
                                     packets=provider_workspace.packets, **circulation.HTTP)
        service_deadline = min(grant.deadline-5, context.deadline-10, time.monotonic()+90)
        detail["stage"] = "discover-and-stage"
        async with asyncio.timeout_at(service_deadline):
            endpoint = await provider.start(host="127.0.0.1", port=0)
            detail["endpoint"] = {key: getattr(endpoint, key) for key in ("host", "port", "tls", "server_name")}
            reader, description = await circulation._acquire(client, endpoint, queries, detail)
            await provider.stop()
        detail["service"] = provider.status()
        F.need(provider.server is None and not provider.tasks, "TERMINAL_I_PROVIDER_OFFLINE")
        detail["service_closed"] = True
        before = client.report(); detail["before_admission"] = before
        F.need(before["receipt"]["attempts"] == before["aggregate"]["attempts"]
               == before["aggregate"]["member_calls"] == before["mixed"]["attempts"]
               == before["counts"]["admission_submissions"] == 0,
               "TERMINAL_I_STAGING_HAS_NO_MATHEMATICAL_CALLS")
        if phase == "second":
            detail.update(status="STRUCTURALLY_AVAILABLE", stage="done",
                          mathematical_acceptance=False, after_staging=client.report())
            return
        detail["stage"] = "admit-and-import"
        module = description["locator"]["module_id"]
        ready = reader.finish({module: deepcopy(p["admission_limits"])})
        detail["import"] = {key: ready[key] for key in ("status", "demands", "cost", "mathematical_acceptance")}
        F.need(ready["status"] == "READY" and ready["context"] is not None and not ready["demands"]
               and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
               "TERMINAL_I_LIVE_INTERFACE_CONTEXT")
        after_i = client.report(); detail["after_i_import"] = after_i
        F.need(after_i["receipt"]["attempts"] == after_i["counts"]["admission_submissions"] == 1
               and after_i["aggregate"]["attempts"] == after_i["aggregate"]["member_calls"]
               == after_i["mixed"]["attempts"] == 0, "TERMINAL_I_ONLY_REAL_I_ADMISSION")
        selected = detail["staged"]["selection"]
        exact = bytes(selected["journal"])
        packet = workspace.packets.get(selected["packet_sha256"], selected["packet_bytes"])
        receipt, packet_j, unused = parse_terminal_i(packet, workspace._envelope,
            aggregate_image=p["workspace_config"]["wire_profile"]["aggregate_image"],
            terminal_receipt_bytes=p["workspace_config"]["terminal_receipt_bytes"], terminal_i=True)
        F.need(packet_j == exact, "TERMINAL_I_SELECTED_PACKET_J")
        F.need(template.count("__METHOD_REF__") == 2, "TERMINAL_I_TWO_METHOD_USES")
        reference = circulation._reference(module, description["locator"]["relative_name"])
        source = template.replace("__METHOD_REF__", reference)
        detail["source"] = circulation._write(work/"ternary-source.lean", source.encode("utf-8"))
        detail["method_reference"] = reference
        detail["stage"] = "author-admit-publish"
        result = helpers["contribution"].contribute_from_context(client, ready["context"],
            source=source, roots=[TERNARY], export_names=[TERNARY],
            author_limits=deepcopy(p["author_limits"]), admission_limits=deepcopy(p["admission_limits"]))
        detail["contribution"] = result
        F.need(result["status"] == "CONTRIBUTED", "TERMINAL_I_NEW_CONTRIBUTION")
        raw, shape = _check_output(workspace, result, helpers["congruence_query"].contract(3),
                                   exact, hashlib.sha256(receipt).hexdigest())
        detail["output_descriptor"] = shape
        detail["packet"] = circulation._write(work/"ternary-published-packet.json", raw)
        after = client.report(); detail["after_contribution"] = after
        F.need(after["counts"]["admission_submissions"] == 2
               and after["counts"]["author_calls"] == after["counts"]["new_import_sessions"]
               == after["counts"]["publication_attempts"] == after["preparation"]["calls"]
               == after["mixed"]["attempts"] == 1
               and after["aggregate"]["attempts"] == after["aggregate"]["member_calls"] == 0,
               "TERMINAL_I_ONE_NEW_CHECKED_EXTENSION")
        F.need(all(after["acquisition"]["used"][key] == before["acquisition"]["used"][key]
                   for key in ("requests", "reply_bytes")), "TERMINAL_I_NO_NETWORK_AFTER_OFFLINE")
        detail.update(status="COMPLETED", stage="done")
    except BaseException as error:
        detail["error"] = remote_reader._error(error)
        raise
    finally:
        if provider is not None and not detail["service_closed"]:
            try:
                async with asyncio.timeout_at(context.deadline-5): await provider.stop()
                detail["service"] = provider.status()
                detail["service_closed"] = provider.server is None and not provider.tasks
            except BaseException as error:
                detail["cleanup_errors"].append(dict(component="service", **remote_reader._error(error)))
        if reader is not None:
            try:
                detail["reader"] = reader.report(); reader.close()
            except BaseException as error:
                detail["cleanup_errors"].append(dict(component="reader", **remote_reader._error(error)))
        if client is not None:
            try:
                closed = await client.close(); detail["client"] = closed
                F.need(closed["closed"] and not closed["cleanup_uncertain"]
                       and all(closed[key] is not None and closed[key]["closed"]
                               for key in ("receipt", "aggregate", "mixed"))
                       and (closed["preparation"] is None or closed["preparation"]["closed"]),
                       "TERMINAL_I_CLIENT_CLEANUP")
                if detail["status"] in ("COMPLETED", "STRUCTURALLY_AVAILABLE"):
                    F.need(closed["status"] == "CLOSED" and not closed["failures"],
                           "TERMINAL_I_CLIENT_CLEAN_CLOSE")
                detail["client_closed"] = True
            except BaseException as error:
                detail["cleanup_errors"].append(dict(component="client", **remote_reader._error(error)))
        if workspace is not None:
            detail["workspace_closed"] = _close_workspace(workspace, detail["cleanup_errors"])
        if domain is not None:
            try:
                domain.withdraw("Explicit finite terminal-I circulation phase completed or failed")
                marker = ordinary(paths[phase+"_domain_path"]/"WITHDRAWN", directory=False)
                F.need(marker.stat().st_size <= 16384, "TERMINAL_I_WITHDRAWAL_BOUND")
                withdrawal = C.parse_json(marker.read_bytes(), C.Limits(max_bytes=16384))
                F.need(withdrawal["schema"] == "DMKN_LOCAL_TRUST_WITHDRAWN_V1"
                       and withdrawal["adoption"] == detail["trust"], "TERMINAL_I_EXACT_WITHDRAWAL")
                detail.update(domain_withdrawn=True, withdrawal=withdrawal)
            except BaseException as error:
                detail["cleanup_errors"].append(dict(component="trust", **remote_reader._error(error)))
        if detail["cleanup_errors"] or not all(detail[key] for key in
                ("client_closed", "workspace_closed", "domain_withdrawn", "service_closed")):
            detail["status"] = "FAILED"
        remote_reader._save(work/(phase+"-result.json"), detail)


async def run(context):
    helpers = _helpers(context); circulation = helpers["circulation"]
    p, paths, work = _parameters(context, circulation)
    report = dict(schema="DMKN_V5_TERMINAL_I_RESULT_V1", status="FAILED", stage="freeze-query",
        error=None, cleanup_errors=[], phases={}, proof_production_calls=0,
        global_complete=False, mathematical_acceptance=False, full_v5_release=False,
        authority="OPERATIONAL_COMPOSITION_REPORT_NOT_TRANSFERABLE_AUTHORITY")
    report["input_pins"] = {name: deepcopy(p[name]) for name in PINS}
    report["helper_sha256"] = deepcopy(HELPERS)
    provider_workspace = None
    primary = None
    try:
        # Frozen mathematical signature only: no fixture, ModuleID or candidate
        # feeds the first query, including through its declared-type hash.
        query = helpers["congruence_query"].query(C, 2)
        report["first_query"] = circulation._write(work/"first-query.json", C.canonical(query))
        template = read_pin(p["template"], 65536).decode("utf-8")
        support = RuntimeProfile.support_manifest(context, p["runtime_adoption"])
        foundation = read_pin(p["foundation"], MIB)
        provider_workspace = Workspace.open(paths["provider_workspace_path"], p["workspace_config"], create=True)
        report["seed"] = _seed(provider_workspace, read_pin(p["receipt"], MIB),
            read_pin(p["journal"], 184), C.parse_json(read_pin(p["bundle"], MIB)))
        report["stage"] = "first-agent"
        first = report["phases"]["first"] = {}
        await _phase(context, p, paths, work, "first", support, foundation, [query],
                     provider_workspace, template, helpers, first)
        F.need(first["status"] == "COMPLETED", "TERMINAL_I_FIRST_PHASE_FAILED")
        F.need(_close_workspace(provider_workspace, report["cleanup_errors"]), "TERMINAL_I_SEED_CLOSE")
        provider_workspace = None
        # Reopen public custody only after the contributor is closed/withdrawn.
        # No saved warrant, trust domain or authoring context is revived.
        onward = first["contribution"]["publication"]["intent"]["module"]
        next_query = {**helpers["congruence_query"].query(C, 3),
                      "expected_module": onward, "expected_name": TERNARY}
        report["second_query"] = circulation._write(work/"second-query.json", C.canonical(next_query))
        provider_workspace = Workspace.open(paths["first_workspace_path"], p["workspace_config"], create=False)
        report["stage"] = "onward-structural-consumer"
        second = report["phases"]["second"] = {}
        await _phase(context, p, paths, work, "second", support, foundation, [next_query],
                     provider_workspace, template, helpers, second)
        F.need(second["status"] == "STRUCTURALLY_AVAILABLE", "TERMINAL_I_SECOND_STAGE_FAILED")
        report.update(status="COMPLETED", stage="done")
    except BaseException as error:
        primary = error; report["error"] = remote_reader._error(error)
    finally:
        if provider_workspace is not None:
            report["final_provider_workspace_closed"] = _close_workspace(provider_workspace, report["cleanup_errors"])
            if not report["final_provider_workspace_closed"]: report["status"] = "FAILED"
        if report["cleanup_errors"] or time.monotonic() >= context.deadline: report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        report["phases"] = {phase: dict(status=detail.get("status", "FAILED"),
            stage=detail.get("stage"), error=detail.get("error"),
            report_path=str(work/(phase+"-result.json")), operation_id=detail.get("operation_id"),
            cleanup_errors=detail.get("cleanup_errors", [])) for phase, detail in report["phases"].items()}
        remote_reader._save(work/"terminal-i-result.json", report)
    if isinstance(primary, asyncio.CancelledError): raise primary
    return report


def main(context):
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1

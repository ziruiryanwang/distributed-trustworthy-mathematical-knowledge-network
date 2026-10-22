"""One installed exact stage, supplier shutdown, genuine I admission and import.

Trusted finite local owner, not a new SDK module or hostile-source sandbox.
No proof generation, source authoring, publication, retry or grant renewal.
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
from client import direct_contacts, remote_reader
from client.runtime import RuntimeProfile, read_pin
from client.semantic_reader import SemanticReader, READY
from client.serve_workspace import _close_workspace
from client.workspace_validated import Workspace
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from evidence_network.custody import profile_id, public_profile
from evidence_network.packet import parse_terminal_i
from evidence_network.transport import CompositeProvider
from location.protocol import OwnerEgressPolicy
from modules import codec as C

MIB = 1024**2
BASE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
BINARY = [["s", "CommonsV5"], ["s", "binary_congr"]]
PACKET = dict(packet_sha256="a737e8f650e9d3abb4781bb2c85c0e625ed4573b7170d71aff1799dbb54495e3",
              packet_bytes=447887)
FIXTURES = {
    "receipt": (223594, "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"),
    "journal": (184, "22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682"),
    "bundle": (53769, "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926"),
    "foundation": (23313, "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"),
}
HELPER_SHA = "885138decc4950b307f71d6f98ca3ffbae4ba0bf6a1ee19454746f8e1b638e21"
SOURCE_PINS = {
    "v5/evidence_network/transport.py": "b34032085bca3ddbd248afe57e655777a140d2c34b6f33ea61b80721a07b926c",
    "v5/placement/controller.py": "77820241984b9dc7ba5d2117a4b11bc89bf217b81697ed8d8ce90fff15e115f2",
    "v5/client/workspace_evidence.py": "3f39d9b594490f04e2737c0f0595c881785a9a6a168cf8fc679d25a5cdef700e",
    "v5/client/workspace_staged.py": "5d96c8cb891eabeb083b0bc501df1a7b268c21b73f4c17da7eb536d2428ad995",
    "v5/client/semantic_reader.py": "253b0ffb5825de15c239be785edcda7e15647038716679402cdf990b81f4128d",
    "v5/client/managed_owner.py": "9a459df2cf2c81b953044b4b5172aaefb9a3001cede6f3a1a23b29f8beb6dcb1",
}
OUTER = dict(cpu_seconds=180, wall_seconds=300, memory_mib=768, active_processes=4,
             stdout_bytes=MIB, stderr_bytes=MIB)
OPERATION = dict(wall_seconds=150, controller_cpu_seconds=90, calls=96, input_bytes=32*MIB,
    worker_cpu_seconds=20, output_bytes=128*MIB, output_entries=1024,
    acquisition=dict(requests=8, reply_bytes=4*MIB, verify_attempts=1,
        verification_input_bytes=2*MIB, worker_cpu_seconds=20),
    imports=dict(max_sources=1, max_members=8, max_receipts=1, max_calls=8192,
                 submitted_bytes=32*MIB, data_bytes=8*MIB))
ADMISSION = dict(native_cpu_seconds=10, receipt_cpu_seconds=10, wall_seconds=60, memory_mib=512)
SEARCH = dict(providers=1, snapshots=1, requests=3, pages=1, examined=4,
              candidates=2, bytes=256*1024, inflight=1, wall_ms=90000)
PAGE = dict(examined=4, matches=2, bytes=131072, timeout_ms=1000, node_reads=50000)
HTTP = dict(max_connections=2, max_requests=8, max_reply_bytes=32*MIB, operation_ms=5000)
READER = dict(modules=1, names=4, groups=4, bodies=1, steps=16, data_bytes=MIB)


def _helper(context):
    """Only the unchanged fixture helper is used; its run/phase are never called."""
    path = ordinary(context.sources_owner/"terminal_fixture.py", directory=False)
    F.need(context.source_sha256["owner/terminal_fixture.py"] == HELPER_SHA
           and path.stat().st_size == 21432
           and hashlib.sha256(path.read_bytes()).hexdigest() == HELPER_SHA,
           "EXACT_INSTALLED_FIXTURE_HELPER_PIN")
    F.need("terminal_fixture" not in sys.modules, "EXACT_INSTALLED_HELPER_COLLISION")
    previous = list(sys.path)
    try:
        sys.path.insert(0, str(context.sources_owner))
        helper = import_module("terminal_fixture")
        F.need(Path(helper.__file__).resolve() == path, "EXACT_INSTALLED_HELPER_ORIGIN")
        return helper
    finally:
        sys.path[:] = previous


def _parameters(context):
    p = deepcopy(dict(context.parameters))
    F.fields(p, {"schema", "action", "runtime_adoption", "foundation", "receipt", "journal",
        "bundle", "workspace_config", "provider_workspace_path", "workspace_path",
        "domain_path", "domain_id", "operation_limits", "admission_limits"})
    F.need(p["schema"] == "DMKN_V5_EXACT_PACKET_INSTALLED_OWNER_V1"
           and p["action"] == "explicit-temporary-adoption-exact-stage-and-i-import",
           "EXACT_INSTALLED_EXPLICIT_ACTION")
    F.need(dict(context.limits) == OUTER and p["operation_limits"] == OPERATION
           and p["admission_limits"] == ADMISSION, "EXACT_INSTALLED_FIXED_CAPS")
    F.need(Path(__file__).resolve() == context.sources_owner/"owner.py"
           and len(context.source_sha256) == 131
           and {name for name in context.source_sha256 if name.startswith("owner/")}
               == {"owner/owner.py", "owner/terminal_fixture.py"}
           and all(context.source_sha256.get(name) == digest for name, digest in SOURCE_PINS.items()),
           "EXACT_INSTALLED_SELECTED_SOURCES")
    for name, (size, digest) in FIXTURES.items():
        F.fields(p[name], {"path", "bytes", "sha256"})
        F.need(p[name]["bytes"] == size and p[name]["sha256"] == digest,
               "EXACT_INSTALLED_FIXTURE_PIN:"+name)
    image = p["workspace_config"]["wire_profile"]["aggregate_image"]
    F.need(profile_id(p["workspace_config"]["wire_profile"])
           == profile_id(public_profile(image, terminal_i=True)), "EXACT_INSTALLED_V2_PROFILE")
    C.digest_string(p["domain_id"])
    paths = {}
    for field in ("provider_workspace_path", "workspace_path", "domain_path"):
        path = ordinary(p[field], fresh=True)
        for other in (context.installation.parent, context.run, context.sources_owner,
                      context.sources_v5, context.sources_portable, *paths.values()):
            other = Path(other)
            F.need(not path.is_relative_to(other) and not other.is_relative_to(path),
                   "EXACT_INSTALLED_DISJOINT_STATE")
        paths[field] = path
    context.remaining_seconds()
    return p, paths


def _write_packet(path, raw):
    F.need(type(raw) is bytes and len(raw) == PACKET["packet_bytes"]
           and hashlib.sha256(raw).hexdigest() == PACKET["packet_sha256"],
           "EXACT_INSTALLED_PACKET_BYTES")
    path = ordinary(path, fresh=True, directory=False)
    with path.open("xb") as stream:
        F.need(stream.write(raw) == len(raw), "EXACT_INSTALLED_PACKET_WRITE")
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def _zero_admission(report):
    F.need(report["receipt"]["attempts"] == report["aggregate"]["attempts"]
           == report["aggregate"]["member_calls"] == report["mixed"]["attempts"]
           == report["counts"]["admission_submissions"] == 0,
           "EXACT_INSTALLED_STAGING_NOT_ADMISSION")
    F.need(report["preparation"] is None, "EXACT_INSTALLED_NO_PREPARATION_OWNER")


async def run(context):
    work = ordinary(context.location_workspace)
    report = dict(schema="DMKN_V5_EXACT_PACKET_INSTALLED_RESULT_V1", status="FAILED",
        stage="parameters", error=None, cleanup_errors=[], proof_production_calls=0,
        authoring=False, packet_offer_calls=0, full_v5_release=False, global_complete=False,
        mathematical_acceptance=False, authority="OPERATION_REPORT_NOT_TRANSFERABLE_AUTHORITY",
        source_pins=deepcopy(SOURCE_PINS), limits=dict(outer=OUTER, operation=OPERATION,
            admission=ADMISSION, search=SEARCH, provider=HTTP, reader=READER),
        provider_stopped=False, reader_closed=False, client_closed=False,
        consumer_workspace_closed=False, provider_workspace_closed=False, domain_withdrawn=False)
    provider_workspace = workspace = client = provider = reader = domain = None
    primary = None
    try:
        p, paths = _parameters(context); helper = _helper(context)
        report["input_pins"] = {name: deepcopy(p[name]) for name in FIXTURES}
        receipt = read_pin(p["receipt"], MIB); exact = read_pin(p["journal"], 184)
        bundle = C.parse_json(read_pin(p["bundle"], MIB))
        foundation = read_pin(p["foundation"], MIB)
        expected = B.member_journal(exact)
        F.need(expected["module"] == BASE and expected["rank"] == 0,
               "EXACT_INSTALLED_EXPECTED_JOURNAL")
        report["stage"] = "adopt"
        support = RuntimeProfile.support_manifest(context, p["runtime_adoption"])
        domain = TrustDomain.create(paths["domain_path"], p["domain_id"], support)
        report["trust"] = domain.identity()
        runtime = RuntimeProfile.from_context(context, p["runtime_adoption"], trust_domain=domain)
        workspace = Workspace.open(paths["workspace_path"], p["workspace_config"], create=True)
        grant = workspace.reserve(p["operation_limits"], outer_deadline=context.deadline-15)
        report["operation_id"] = grant.identifier
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=False,
            foundation_bytes=foundation, foundation_sha256=p["foundation"]["sha256"])
        report["stage"] = "seed-and-serve"
        provider_workspace = Workspace.open(paths["provider_workspace_path"], p["workspace_config"], create=True)
        seeded = helper._seed(provider_workspace, receipt, exact, bundle)
        F.need(all(seeded[key] == value for key, value in PACKET.items())
               and seeded["module"] == BASE and seeded["groups"] == 1 and seeded["bodies"] == 0
               and seeded["mathematical_acceptance"] is False, "EXACT_INSTALLED_SEED_BINDING")
        report["seed"] = seeded
        provider = CompositeProvider(index=provider_workspace.index, custody=provider_workspace.modules,
                                     packets=provider_workspace.packets, **HTTP)
        service_deadline = min(grant.deadline-10, context.deadline-15, time.monotonic()+90)
        report["stage"] = "candidate-and-exact-stage"
        async with asyncio.timeout_at(service_deadline):
            endpoint = await provider.start(host="127.0.0.1", port=0)
            contact = {key: getattr(endpoint, key) for key in ("host", "port", "tls", "server_name")}
            report["contact"] = contact
            policy = OwnerEgressPolicy(dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test",
                public_ports=[], test_endpoints=[dict(host=endpoint.host, port=endpoint.port)]))
            report["binding"] = direct_contacts.bind(client, {"selected": contact},
                [dict(tag="declaration-kind", value="theorem")], policy, deepcopy(SEARCH),
                contact_lifetime_ms=90000)
            offer = await client.search_offer("selected", max_bytes=131072,
                max_expanded_bytes=262144, max_age_ms=60000, attempt_timeout_ms=5000)
            F.need(offer["status"] == "OFFERED", "EXACT_INSTALLED_SEARCH_OFFER")
            report["offer"] = offer
            partitions = [row for row in offer["partitions"] if row["anchor_count"] > 0]
            F.need(len(partitions) == 1, "EXACT_INSTALLED_SINGLE_PARTITION")
            page = await client.search_page("selected", offer["snapshot_id"], partitions[0]["partition"],
                0, deepcopy(PAGE), candidates_only=False, attempt_timeout_ms=5000)
            F.need(page["status"] == "VERIFIED_PAGE" and len(page["matches"]) == 1,
                   "EXACT_INSTALLED_ONE_AUTHENTICATED_CANDIDATE")
            report["page"] = page
            candidate = await client.resolve("selected", page["matches"][0])
            description = client.describe_candidate(candidate); report["candidate"] = description
            F.need(description["locator"]["module_id"] == BASE
                   and description["locator"]["relative_name"] == BINARY
                   and description["opening"] == C.group_opening(bundle["spec"], 10)
                   and description["descriptor"] == bundle["openings"][10]["group"]["declarations"][0]
                   and description["descriptor"]["kind"] == "theorem"
                   and description["descriptor"]["universes"] == 3,
                   "EXACT_INSTALLED_SELECTED_INTERFACE")
            reader = SemanticReader(client, candidate, limits=deepcopy(READER), definition_mode="interface-only")
            staged = await reader.stage_exact(candidate, dict(PACKET))
            report["staged"] = staged
            F.need(staged["status"] == "STAGED" and staged["module"] == BASE
                   and all(staged["selection"][key] == value for key, value in PACKET.items())
                   and bytes(staged["selection"]["journal"]) == exact
                   and staged["selection"]["summary"] == expected["summary"]
                   and staged["members"] == [dict(module=BASE, journal=list(exact), summary=expected["summary"])],
                   "EXACT_INSTALLED_STAGED_TARGET")
            await provider.stop()
        report["provider"] = provider.status()
        F.need(provider.server is None and not provider.tasks, "EXACT_INSTALLED_PROVIDER_NOT_STOPPED")
        report["provider_stopped"] = True
        before = client.report(); report["before_admission"] = before
        _zero_admission(before)
        F.need(before["transport"]["delta_http"]["completed_requests"] == 1
               and before["transport"]["structural_http"]["requests"] == 1
               and before["acquisition"]["used"]["requests"] == 5
               and report["provider"]["requests"] == 4
               and report["provider"]["failures"] == report["provider"]["refused"] == 0,
               "EXACT_INSTALLED_NO_PACKET_OFFER_REQUEST")
        raw = workspace.packets.get(PACKET["packet_sha256"], PACKET["packet_bytes"])
        held_receipt, held_journal, unused = parse_terminal_i(raw, workspace._envelope,
            aggregate_image=p["workspace_config"]["wire_profile"]["aggregate_image"],
            terminal_receipt_bytes=p["workspace_config"]["terminal_receipt_bytes"], terminal_i=True)
        F.need(held_receipt == receipt and held_journal == exact, "EXACT_INSTALLED_HELD_RECEIPT_J")
        report["received_packet"] = _write_packet(work/"received-terminal-i.json", raw)
        report["stage"] = "offline-preview-and-finish"
        preview = reader.preview(); report["preview"] = preview
        F.need(preview["status"] == READY and not preview["demands"]
               and preview["mathematical_acceptance"] is False, "EXACT_INSTALLED_READY_PREVIEW")
        ready = reader.finish({BASE: deepcopy(ADMISSION)})
        report["import"] = {key: ready[key] for key in ("status", "demands", "cost", "mathematical_acceptance")}
        F.need(ready["status"] == "READY" and ready["context"] is not None and not ready["demands"]
               and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
               "EXACT_INSTALLED_INTERFACE_IMPORT")
        after = client.report(); report["after_import"] = after
        F.need(after["receipt"]["attempts"] == after["counts"]["admission_submissions"]
               == after["counts"]["new_import_sessions"] == 1
               and after["aggregate"]["attempts"] == after["aggregate"]["member_calls"]
               == after["mixed"]["attempts"] == after["counts"]["author_calls"]
               == after["counts"]["publication_attempts"] == 0 and after["preparation"] is None,
               "EXACT_INSTALLED_ONLY_ONE_REAL_I")
        F.need(all(after["acquisition"]["used"][key] == before["acquisition"]["used"][key]
                   for key in ("requests", "reply_bytes")), "EXACT_INSTALLED_OFFLINE_COUNTERS")
        report.update(status="COMPLETED", stage="done")
    except BaseException as error:
        primary = error; report["error"] = remote_reader._error(error)
    finally:
        if provider is not None and not report["provider_stopped"]:
            try:
                async with asyncio.timeout_at(context.deadline-5): await provider.stop()
                report["provider"] = provider.status()
                report["provider_stopped"] = provider.server is None and not provider.tasks
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="provider", **remote_reader._error(error)))
        if reader is not None:
            try:
                report["reader"] = reader.report(); reader.close(); report["reader_closed"] = True
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="reader", **remote_reader._error(error)))
        if client is not None:
            try:
                closed = await client.close(); report["client"] = closed
                F.need(closed["closed"] and not closed["cleanup_uncertain"]
                       and all(closed[key] is not None and closed[key]["closed"]
                               for key in ("receipt", "aggregate", "mixed"))
                       and closed["preparation"] is None, "EXACT_INSTALLED_CLIENT_CLEANUP")
                if report["status"] == "COMPLETED":
                    F.need(closed["status"] == "CLOSED" and not closed["failures"],
                           "EXACT_INSTALLED_CLEAN_CLOSE")
                report["client_closed"] = True
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="client", **remote_reader._error(error)))
        if workspace is not None:
            report["consumer_workspace_closed"] = _close_workspace(workspace, report["cleanup_errors"])
        if provider_workspace is not None:
            report["provider_workspace_closed"] = _close_workspace(provider_workspace, report["cleanup_errors"])
        if domain is not None:
            try:
                domain.withdraw("Explicit finite exact-packet installed operation completed or failed")
                marker = ordinary(paths["domain_path"]/"WITHDRAWN", directory=False)
                F.need(marker.stat().st_size <= 16384, "EXACT_INSTALLED_WITHDRAWAL_BOUND")
                withdrawal = C.parse_json(marker.read_bytes(), C.Limits(max_bytes=16384))
                F.need(withdrawal["schema"] == "DMKN_LOCAL_TRUST_WITHDRAWN_V1"
                       and withdrawal["adoption"] == report["trust"], "EXACT_INSTALLED_EXACT_WITHDRAWAL")
                report.update(domain_withdrawn=True, withdrawal=withdrawal)
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="trust", **remote_reader._error(error)))
        if report["cleanup_errors"] or not all(report[key] for key in
            ("provider_stopped", "reader_closed", "client_closed", "consumer_workspace_closed",
             "provider_workspace_closed", "domain_withdrawn")) or time.monotonic() >= context.deadline:
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        remote_reader._save(work/"exact-packet-installed-result.json", report)
    if isinstance(primary, asyncio.CancelledError): raise primary
    return report


def main(context):
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1

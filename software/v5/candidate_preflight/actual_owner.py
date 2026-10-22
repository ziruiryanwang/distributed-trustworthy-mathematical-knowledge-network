"""One malformed peer packet preserves a genuine warrant, context and stage.

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
from client.serve_workspace import _close_workspace
from client.workspace_validated import Workspace
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from evidence_network.custody import profile_id, public_profile
from evidence_network.packet import parse_terminal_i
from evidence_network.transport import CompositeProvider, PACKET_ROUTE
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
    "v5/evidence_network/transport.py": "1dbc083447569a70c62910fec904e49d7df154c09684b26f28b30e071efa14c7",
    "v5/placement/controller.py": "77820241984b9dc7ba5d2117a4b11bc89bf217b81697ed8d8ce90fff15e115f2",
    "v5/client/workspace_evidence.py": "62c4ea578cf92c85b398880e8cfba9e914ecf6668e3916bd1d87ce5ee02efcce",
    "v5/client/workspace_staged.py": "5d96c8cb891eabeb083b0bc501df1a7b268c21b73f4c17da7eb536d2428ad995",
    "v5/client/semantic_reader.py": "253b0ffb5825de15c239be785edcda7e15647038716679402cdf990b81f4128d",
    "v5/client/managed_owner.py": "860fbea914c0de2515d14d3ceacad7fcae8f7c14d79cbfea1632ead172f9cd83",
    "v5/admission/clean_refusal.py": "7c1386cce693185ac7d6e1dda149993c892ac5b2d417242fb7e02b873648e5a7",
    "v5/admission/verifier.py": "ec6474cdd0580df89f9c646a41c0d909ec20e83da0a42274e0510a6e01bbbaea",
    "v5/aggregate_claims/aggregate_admission.py": "ce2cfc95f08699c679128448d9d9f5131cf54acbefa91225db2689a2b1574f5c",
    "v5/delta/custody.py": "e1e35cecd8f40154a98e40cb1a5a2cca1d8c376966e57ef529c7c878bdd6c634",
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


class _AdversarialProvider(CompositeProvider):
    """Test-only exact malformed response; installed client/stores stay strict."""
    def __init__(self, *, malformed, entry, deadline, **roles):
        super().__init__(**roles)
        F.need(malformed == b"{" and entry == dict(packet_bytes=1,
            packet_sha256=hashlib.sha256(malformed).hexdigest()), "PREFLIGHT_ADVERSARIAL_FIXTURE")
        self._malformed, self._entry, self._fixture_deadline = malformed, dict(entry), deadline
        self._fixture_tasks = set()
        self._fixture_started = self._fixture_closed = self._malformed_dispatches = 0
        self._fixture_errors = []

    def dispatch(self, route, request, *, check_budget=None):
        if route == PACKET_ROUTE and request == self._entry:
            F.need(check_budget is not None and self._malformed_dispatches == 0,
                   "PREFLIGHT_ONE_EXACT_ADVERSARIAL_DISPATCH")
            check_budget(); self._malformed_dispatches += 1; check_budget()
            return self._malformed
        return super().dispatch(route, request, check_budget=check_budget)

    async def _serve(self, reader, writer):
        task = asyncio.current_task()
        self._fixture_tasks.add(task); self._fixture_started += 1
        try:
            await super()._serve(reader, writer)
        except BaseException as error:
            self._fixture_errors.append(dict(component="handler", **remote_reader._error(error)))
            raise
        finally:
            try:
                writer.close()
                async with asyncio.timeout_at(min(self._fixture_deadline, time.monotonic()+1)):
                    await writer.wait_closed()
                self._fixture_closed += 1
            except BaseException as error:
                self._fixture_errors.append(dict(component="writer", **remote_reader._error(error)))
                raise
            finally:
                self._fixture_tasks.discard(task)

    async def stop(self):
        # Stop accepting first, then settle our tracked wrappers before the
        # ordinary provider's fallback cancellation. Do not hide close errors.
        if self.server is not None:
            self.server.close(); await self.server.wait_closed(); self.server = None
        async with asyncio.timeout_at(self._fixture_deadline):
            await asyncio.sleep(0)
            pending = list(self._fixture_tasks)
            if pending: await asyncio.gather(*pending, return_exceptions=True)
        await super().stop()
        F.need(not self._fixture_tasks and not self._fixture_errors
               and self._fixture_started == self._fixture_closed,
               "PREFLIGHT_FIXTURE_CLOSURE")

    def fixture_status(self):
        return dict(role="EXPLICIT_ADVERSARIAL_PEER_NOT_CLIENT_AUTHORITY",
            malformed_dispatches=self._malformed_dispatches, handlers_started=self._fixture_started,
            handlers_closed=self._fixture_closed, active_handlers=len(self._fixture_tasks),
            errors=deepcopy(self._fixture_errors))


def _packet_snapshot(workspace):
    return dict(status=workspace.packets.status(), offer=workspace.packets.offer(dict(
        module_id=BASE, wire_profile_id=workspace.packets.profile_id, max_offers=4, max_bytes=4096)))


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
    F.need(p["schema"] == "DMKN_V5_CANDIDATE_PREFLIGHT_ACTUAL_OWNER_V1"
           and p["action"] == "explicit-temporary-adoption-peer-preflight-and-continuation",
           "EXACT_INSTALLED_EXPLICIT_ACTION")
    F.need(dict(context.limits) == OUTER and p["operation_limits"] == OPERATION
           and p["admission_limits"] == ADMISSION, "EXACT_INSTALLED_FIXED_CAPS")
    F.need(Path(__file__).resolve() == context.sources_owner/"owner.py"
           and len(context.source_sha256) == 132
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


def _write_packet(path, raw, entry):
    F.need(type(raw) is bytes and len(raw) == entry["packet_bytes"]
           and hashlib.sha256(raw).hexdigest() == entry["packet_sha256"],
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
    report = dict(schema="DMKN_V5_CANDIDATE_PREFLIGHT_ACTUAL_RESULT_V1", status="FAILED",
        stage="parameters", error=None, cleanup_errors=[], proof_production_calls=0,
        authoring=False, packet_offer_calls=0, full_v5_release=False, global_complete=False,
        mathematical_acceptance=False, authority="OPERATION_REPORT_NOT_TRANSFERABLE_AUTHORITY",
        source_pins=deepcopy(SOURCE_PINS), limits=dict(outer=OUTER, operation=OPERATION,
            admission=ADMISSION, search=SEARCH, provider=HTTP),
        provider_stopped=False, client_closed=False,
        consumer_workspace_closed=False, provider_workspace_closed=False, domain_withdrawn=False)
    provider_workspace = workspace = client = provider = domain = None
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
        bad_raw = b"{"
        bad_entry = dict(packet_sha256=hashlib.sha256(bad_raw).hexdigest(), packet_bytes=len(bad_raw))
        F.need(bad_entry != PACKET, "CANDIDATE_DISTINCT_BAD_VARIANT")
        report["malformed_peer_bytes"] = _write_packet(work/"malformed-peer-packet.bin", bad_raw, bad_entry)
        report["adversarial_fixture"] = "EXACT_DIGEST_ONE_OPEN_BRACE_NOT_INSERTED_IN_ANY_PACKET_STORE"
        provider = _AdversarialProvider(index=provider_workspace.index, custody=provider_workspace.modules,
            packets=provider_workspace.packets, malformed=bad_raw, entry=bad_entry,
            deadline=min(grant.deadline-5, context.deadline-10), **HTTP)
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
            staged_token = await client.stage_packet_exact(candidate, dict(PACKET))
            staged = client.describe_staged(staged_token)
            report["staged_before"] = staged
            F.need(staged["status"] == "STAGED_UNTRUSTED_EVIDENCE" and not staged["admission_consumed"]
                   and all(staged["selection"][key] == value for key, value in PACKET.items())
                   and staged["selection"]["module"] == BASE
                   and bytes(staged["selection"]["journal"]) == exact
                   and staged["selection"]["summary"] == expected["summary"]
                   and staged["members"] == [dict(module=BASE, journal=list(exact), summary=expected["summary"])],
                   "EXACT_INSTALLED_STAGED_TARGET")
            before = client.report(); report["before_admission"] = before
            _zero_admission(before)
            F.need(before["transport"]["delta_http"]["completed_requests"] == 1
                   and before["transport"]["structural_http"]["requests"] == 1
                   and before["acquisition"]["used"]["requests"] == 5,
                   "CANDIDATE_STAGE_REQUESTS")
            raw = workspace.packets.get(PACKET["packet_sha256"], PACKET["packet_bytes"])
            held_receipt, held_journal, unused = parse_terminal_i(raw, workspace._envelope,
                aggregate_image=p["workspace_config"]["wire_profile"]["aggregate_image"],
                terminal_receipt_bytes=p["workspace_config"]["terminal_receipt_bytes"], terminal_i=True)
            F.need(held_receipt == receipt and held_journal == exact, "EXACT_INSTALLED_HELD_RECEIPT_J")
            report["good_packet"] = _write_packet(work/"good-terminal-i.json", raw, PACKET)
            report["stage"] = "genuine-prior-admission-and-context"
            warrant = client.admit_local(BASE, **PACKET, expected_exact_journal=exact, **ADMISSION)
            live_before = client.describe(warrant)
            openings = [dict(module=BASE, opening=deepcopy(description["opening"]))]
            ready = client.import_context([dict(warrant=warrant, resolutions=None)], [exact],
                deepcopy(openings), [], definition_mode="interface-only")
            F.need(ready["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY"
                   and ready["context"] is not None and not ready["demands"]
                   and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
                   "CANDIDATE_PRIOR_READY_CONTEXT")
            report["prior_import"] = {key: ready[key] for key in
                ("status", "demands", "cost", "mathematical_acceptance")}
            old_context = ready["context"]
            old_context_slot, old_session, old_view = client._context, client._session, client._selection_view
            original_owners = tuple(client._origin_owners)
            original_deadlines = tuple(None if owner is None else owner._deadline for owner in original_owners)
            original_grant_deadline = grant.deadline
            F.need(client.describe_staged(staged_token) == staged, "CANDIDATE_STAGE_NOT_CONSUMED_BY_IMPORT")
            prior = client.report(); report["before_refusal"] = prior
            F.need(prior["receipt"]["attempts"] == prior["receipt"]["live_handles"]
                   == prior["counts"]["admission_submissions"] == prior["counts"]["new_import_sessions"] == 1,
                   "CANDIDATE_ONE_GENUINE_PRIOR_I")
            consumer_packets = _packet_snapshot(workspace)
            provider_packets = _packet_snapshot(provider_workspace)
            F.need(consumer_packets["offer"]["packets"] == provider_packets["offer"]["packets"] == [PACKET],
                   "PREFLIGHT_ONLY_GOOD_PACKET_IN_CUSTODY")
            report["packets_before"] = dict(consumer=consumer_packets, provider=provider_packets)
            report["stage"] = "real-malformed-peer-preflight"
            trial = await client.try_acquire_terminal_exact(candidate, bad_entry,
                expected_exact_journal=exact, receipt_cpu_seconds=10, wall_seconds=60, memory_mib=512)
            F.need(trial == dict(status="CANDIDATE_REJECTED_UNDER_SELECTED_POLICY",
                   reason="PACKET_STRUCTURE_OR_SELECTED_POLICY", module=BASE, selection=bad_entry,
                   received_sha256=bad_entry["packet_sha256"], received_bytes=1,
                   authority="LOCAL_CANDIDATE_PREFLIGHT_NOT_MATHEMATICAL_ACCEPTANCE",
                   mathematical_acceptance=False), "PREFLIGHT_REAL_POLICY_REJECTION_REQUIRED")
            report["trial"] = trial
            refused = client.report(); report["after_refusal"] = refused
            F.need(refused["receipt"]["attempts"] == refused["counts"]["admission_submissions"] == 1
                   and refused["receipt"]["live_handles"] == 1
                   and refused["receipt"]["submitted_bytes"] == len(receipt)
                   and refused["receipt"]["reserved_cpu_seconds"] == 10
                   and refused["submitted_input_bytes"] == prior["submitted_input_bytes"]+1
                   and refused["acquisition"]["used"]["requests"] == prior["acquisition"]["used"]["requests"]+1
                   and refused["acquisition"]["used"]["reply_bytes"] == prior["acquisition"]["used"]["reply_bytes"]+1
                   and refused["acquisition"]["used"]["verify_attempts"] == 1,
                   "PREFLIGHT_CHARGED_TRANSFER_NO_SECOND_VERIFIER")
            report["packets_after"] = dict(consumer=_packet_snapshot(workspace),
                                            provider=_packet_snapshot(provider_workspace))
            F.need(report["packets_before"] == report["packets_after"], "PREFLIGHT_NO_CUSTODY_CHANGE")
            F.need(client.grant is grant and grant.deadline == original_grant_deadline
                   and all(a is b for a, b in zip(client._origin_owners, original_owners))
                   and tuple(None if owner is None else owner._deadline for owner in original_owners)
                       == original_deadlines
                   and client._context is old_context_slot and client._session is old_session
                   and client._selection_view is old_view and client.describe(warrant) == live_before
                   and client.describe_staged(staged_token) == staged,
                   "CANDIDATE_PRIOR_LIVE_WORK_UNCHANGED")
            report["same_original_owners_grant_context_and_unconsumed_stage"] = True
            await provider.stop()
        report["provider"] = provider.status()
        report["fixture"] = provider.fixture_status()
        F.need(provider.server is None and not provider.tasks, "EXACT_INSTALLED_PROVIDER_NOT_STOPPED")
        F.need(report["fixture"]["malformed_dispatches"] == 1
               and report["fixture"]["handlers_started"] == report["fixture"]["handlers_closed"] == 5
               and report["fixture"]["active_handlers"] == 0 and not report["fixture"]["errors"],
               "PREFLIGHT_ACTUAL_FIXTURE_AND_CLOSURE")
        report["provider_stopped"] = True
        stopped = client.report(); report["supplier_stopped_before_continuation"] = stopped
        F.need(stopped["transport"]["delta_http"]["completed_requests"] == 2
               and stopped["transport"]["structural_http"]["requests"] == 1
               and stopped["acquisition"]["used"]["requests"] == 6
               and report["provider"]["requests"] == 5
               and report["provider"]["failures"] == report["provider"]["refused"] == 0,
               "EXACT_INSTALLED_NO_PACKET_OFFER_REQUEST")
        report["stage"] = "offline-existing-work-continuation"
        cached = client.try_admit_terminal_local(BASE, **PACKET, expected_exact_journal=exact,
            receipt_cpu_seconds=10, wall_seconds=60, memory_mib=512)
        F.need(cached["status"] == "ADMITTED" and cached["warrant"] is warrant,
               "CANDIDATE_PRIOR_LIVE_CACHE_REUSED")
        report["cached_admission"] = {key: value for key, value in cached.items() if key != "warrant"}
        admitted = client.admit_staged(staged_token, expected_exact_journal=exact, **ADMISSION)
        F.need(admitted is warrant and client.describe(admitted) == live_before,
               "CANDIDATE_ORIGINAL_STAGED_AUTHORITY_USABLE")
        consumed = client.describe_staged(staged_token)
        F.need(consumed == {**staged, "admission_consumed": True}, "CANDIDATE_ONLY_ORIGINAL_STAGE_CONSUMED")
        report["staged_after_continuation"] = consumed
        advanced = client.advance_context(old_context, warrants=[], selected=[exact],
            openings=deepcopy(openings), bodies=[])
        F.need(advanced["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY"
               and advanced["context"] is not old_context and not advanced["demands"]
               and client._session is old_session and client.describe(warrant) == live_before,
               "CANDIDATE_ORIGINAL_READY_CONTEXT_USABLE")
        report["advanced_import"] = {key: advanced[key] for key in
            ("status", "demands", "cost", "mathematical_acceptance")}
        after = client.report(); report["after_continuation"] = after
        F.need(after["receipt"]["attempts"] == after["counts"]["admission_submissions"] == 1
               and after["receipt"]["live_handles"] == after["counts"]["new_import_sessions"] == 1
               and after["aggregate"]["attempts"] == after["aggregate"]["member_calls"]
               == after["mixed"]["attempts"] == after["counts"]["author_calls"]
               == after["counts"]["publication_attempts"] == 0 and after["preparation"] is None,
               "PREFLIGHT_EXACTLY_ONE_REAL_I_NO_OTHER_VERIFICATION")
        F.need(all(after["acquisition"]["used"][key] == stopped["acquisition"]["used"][key]
                   for key in ("requests", "reply_bytes")), "EXACT_INSTALLED_OFFLINE_COUNTERS")
        report.update(status="COMPLETED", stage="done")
    except BaseException as error:
        primary = error; report["error"] = remote_reader._error(error)
    finally:
        if provider is not None and not report["provider_stopped"]:
            try:
                async with asyncio.timeout_at(context.deadline-5): await provider.stop()
                report["provider"] = provider.status()
                report["fixture"] = provider.fixture_status()
                report["provider_stopped"] = provider.server is None and not provider.tasks
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="provider", **remote_reader._error(error)))
                report["fixture"] = provider.fixture_status()
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
                domain.withdraw("Explicit finite peer-preflight operation completed or failed")
                marker = ordinary(paths["domain_path"]/"WITHDRAWN", directory=False)
                F.need(marker.stat().st_size <= 16384, "EXACT_INSTALLED_WITHDRAWAL_BOUND")
                withdrawal = C.parse_json(marker.read_bytes(), C.Limits(max_bytes=16384))
                F.need(withdrawal["schema"] == "DMKN_LOCAL_TRUST_WITHDRAWN_V1"
                       and withdrawal["adoption"] == report["trust"], "EXACT_INSTALLED_EXACT_WITHDRAWAL")
                report.update(domain_withdrawn=True, withdrawal=withdrawal)
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="trust", **remote_reader._error(error)))
        if report["cleanup_errors"] or not all(report[key] for key in
            ("provider_stopped", "client_closed", "consumer_workspace_closed",
             "provider_workspace_closed", "domain_withdrawn")) or time.monotonic() >= context.deadline:
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        remote_reader._save(work/"candidate-preflight-actual-result.json", report)
    if isinstance(primary, asyncio.CancelledError): raise primary
    return report


def main(context):
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1

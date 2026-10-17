"""One genuine A/H2 -> ordinary SECOND -> fresh C reciprocal-use adapter.

Trusted owner strategy for the unchanged launcher. A real selected receipt is
mandatory; this file never constructs a fake issuer or runs a prover. Discovery
choosers get formal queries and finite grants, not evaluator target identifiers.
Same-process phase separation is not a hostile-code security boundary.
"""
import asyncio
from copy import deepcopy
import hashlib
import json
import time

from aggregate_claims import bindings as B
from client.terminal_assets import Assets, BASE
from client.terminal_inspection import inspect_author
from client.workspace_staged import Workspace
from discovery.module_export_adapter import compile_query
from evidence_network.transport import CompositeProvider
from location.controller import AdoptedLocationRuntime, SOURCE_NAMES
from location.controller_services import ServiceLocationProcess, ROLE_NAMES
from location import protocol as P
from mixed_claims.packet import Envelope, parse_packet
from modules import codec as C

MIB = 1024**2
RETENTION = {"mode": "quota-bounded-local-custody"}
SEARCH = dict(providers=4, snapshots=8, requests=16, pages=8, examined=256,
              candidates=64, bytes=2*MIB, wall_ms=90000, inflight=1)
LOCATION = dict(wall_ms=180000, route_operations=1, routing_events=256,
                routing_peer_slots=4, descriptor_requests=4, contacts=4,
                reply_bytes=2*MIB+32768)
PAGE = dict(scanned=32, matches=8, bytes=131072, timeout_ms=1000,
            record_probes=256, node_reads=32768, hash_calls=200000, sql_vm_steps=1000000)
OFFER_BYTES, SEMANTIC_BYTES = 16384, 2*MIB
MAX_STEPS, MAX_NAMES, MAX_GROUPS, MAX_BODIES = 32, 64, 12, 11
READY = "UNTRUSTED_AUTHORING_CONTEXT_READY"
STAGED_READY, STAGED_NEED = "STRUCTURAL_CLOSURE_STAGED", "NEED_STRUCTURAL_CONTEXT_DATA"
REFUSED = "REFUSED_PROVIDER_ATTEMPT"


def need(condition, reason):
    if not condition: raise ValueError(reason)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def serial(value):
    """Reports are inert; byte arrays are not restored as warrants."""
    if type(value) is bytes: return list(value)
    if type(value) in (tuple, list): return [serial(item) for item in value]
    if type(value) is dict: return {key: serial(item) for key, item in value.items()}
    return value


def save(path, value):
    raw = json.dumps(serial(value), sort_keys=True, separators=(",", ":"),
                     allow_nan=False).encode("utf-8")
    need(len(raw) <= 4*MIB, "TERMINAL_REPORT_BOUND")
    with path.open("xb") as stream: stream.write(raw)


def query_specs():
    """Common public vocabulary only; no FIRST or SECOND identifier."""
    return [{"tag": "declaration-kind", "value": "theorem"},
        {"tag": "result-head", "head": {"tag": "const", "symbol": {
            "kind": "foundation-name", "name_hash": C.hash_value("foundation-symbol", [["s", "Eq"]])}}},
        {"tag": "type-symbol", "symbol": {"kind": "export",
            "export_id": C.export_id(BASE, [["s", "CommonsV5"], ["s", "fold"]])}}]


async def discover(client, reader, specs, features, policy, record):
    """Bounded unknown-ID chooser; no assets, expected target or author source.

    One first page per nonempty offered partition, at most eight pages overall.
    Incomplete discovery is a failure of this finite gate, never global absence.
    Only explicit settled search refusals/ordinary empty offers can continue.
    """
    found = await client.find(reader, specs, policy, LOCATION, SEARCH,
        routes=[dict(features=features, stripe=0, event_cap=256, peer_cap=4, descriptors=4)],
        descriptor_age_ms=60000)
    record.update(discovery=found, attempts=[], chooser="FORMAL_QUERY_RETURN_ORDER_NO_TARGET_ID")
    need(found["status"] == "QUERY_CONTACTS_READY" and 0 < len(found["contacts"]) <= 4,
         "TERMINAL_NO_QUERY_CONTACTS")
    pages = 0
    for contact in found["contacts"]:
        offered = await client.search_offer(contact, OFFER_BYTES, max_expanded_bytes=MIB,
                                            max_age_ms=60000, attempt_timeout_ms=5000)
        attempt = {"provider": contact, "offer": offered, "pages": []}; record["attempts"].append(attempt)
        if offered["status"] in (REFUSED, "NO_OFFER", "REFUSED"): continue
        need(offered["status"] == "OFFERED", "TERMINAL_SEARCH_OFFER_STATUS")
        for partition in offered["partitions"]:
            if partition["anchor_count"] == 0: continue
            need(pages < SEARCH["pages"], "TERMINAL_SELECTED_PAGE_BOUND")
            pages += 1
            page = await client.search_page(contact, offered["snapshot_id"], partition["partition"],
                                            0, PAGE, candidates_only=True, attempt_timeout_ms=5000)
            attempt["pages"].append(page)
            if page["status"] == REFUSED: break
            need(page["status"] == "VERIFIED_CANDIDATES", "TERMINAL_CANDIDATE_STATUS")
            if not page["matches"]: continue
            candidate = await client.resolve(contact, page["matches"][0])
            description = client.describe_candidate(candidate)
            offers = await client.packet_offers(candidate, max_offers=2, max_bytes=4096)
            need(offers["packets"], "TERMINAL_NO_EVIDENCE_OFFER")
            record.update(candidate=description, packet_offer=offers["packets"][0],
                          global_complete=False, mathematical_acceptance=False)
            return candidate, description, offers["packets"][0]
    raise ValueError("TERMINAL_NO_CANDIDATE_IN_FINITE_QUERY_NOT_GLOBAL_ABSENCE")


async def demand_context(client, origin, original, entry, record):
    """Acquire bounded structural closure before either mathematical admission.

    Only the returned candidate and common BASE vocabulary identify modules.
    No evaluator journals, assets, author source or live warrant enter here.
    Preview predicts data needs; it never supplies an authoring context.
    """
    first = original["locator"]["module_id"]
    need(first != BASE, "TERMINAL_DISTINCT_DISCOVERED_MODULE")
    allowed = {BASE, first}
    candidates = {(first, C.name_key(original["locator"]["relative_name"])): (origin, original)}
    groups, bodies, selected, tokens = {}, {}, {}, {}
    record.update(steps=[], groups=[], bodies=[], staged=[], exact_name_requests=0,
                  ancestor_theorem_proof_requests=0, mathematical_acceptance=False,
                  acquisition="ACTUAL_STRUCTURAL_DEMANDS_BEFORE_ADMISSION")

    async def stage(candidate, data, offered):
        module = data["locator"]["module_id"]
        need(module in allowed and module not in tokens, "TERMINAL_STAGED_MODULE_SELECTION")
        token = await client.stage_packet(candidate, offered)
        snapshot = client.describe_staged(token); choice = snapshot["selection"]
        need(snapshot["status"] == "STAGED_UNTRUSTED_EVIDENCE"
             and snapshot["mathematical_acceptance"] is False and snapshot["admission_consumed"] is False
             and snapshot["provider"] == data["provider"]
             and all(snapshot["candidate"][key] == data[key] for key in ("locator", "opening", "descriptor"))
             and choice["module"] == module == C.summary_id(choice["summary"])
             and choice["summary"] == data["opening"]["summary"]
             and choice["packet_sha256"] == offered["packet_sha256"]
             and choice["packet_bytes"] == offered["packet_bytes"], "TERMINAL_EXACT_STAGED_CANDIDATE")
        parsed = B.member_journal(bytes(choice["journal"]))
        need(parsed["module"] == module and parsed["summary"] == choice["summary"],
             "TERMINAL_STAGED_JOURNAL_BINDING")
        selected[module] = deepcopy(choice); tokens[module] = token
        record["staged"].append(deepcopy(choice))

    def group(data):
        module, opening = data["locator"]["module_id"], data["opening"]
        need(module in allowed and module in selected
             and opening["summary"] == selected[module]["summary"], "TERMINAL_UNSELECTED_SEMANTIC_MODULE")
        C.verify_group_opening(module, opening)
        key, encoded = (module, opening["index"]), C.canonical(opening)
        if key in groups:
            need(groups[key] == encoded, "TERMINAL_GROUP_CONFLICT"); return
        need(len(groups) < MAX_GROUPS
             and sum(owner == BASE for owner, unused in groups) < (11 if module == BASE else 12),
             "TERMINAL_GROUP_LIMIT")
        need(module == BASE or not any(owner == first for owner, unused in groups),
             "TERMINAL_FIRST_SINGLE_GROUP")
        groups[key] = encoded
        record["groups"].append({"module": module, "index": opening["index"], "sha256": sha(encoded)})

    async def candidate(module, name):
        key = module, C.name_key(name)
        if key not in candidates:
            need(len(candidates) < MAX_NAMES, "TERMINAL_EXACT_NAME_LIMIT")
            token = await client.resolve_declaration(origin, module, name, max_bytes=SEMANTIC_BYTES)
            data = client.describe_candidate(token)
            need(data["locator"]["module_id"] == module
                 and C.name_key(data["locator"]["relative_name"]) == key[1], "TERMINAL_EXACT_NAME_BINDING")
            candidates[key] = token, data; record["exact_name_requests"] += 1
        return candidates[key]

    def arrays():
        # The preview is stateless: every call receives the complete selected
        # closure accumulated so far, not only the previous round's delta.
        openings = [{"module": module, "opening": C.parse_json(raw)}
                    for (module, unused_index), raw in sorted(groups.items())]
        values = [{"module": module, "universes": arity, "expression": C.parse_json(raw)}
                  for (module, arity, unused_digest), raw in sorted(bodies.items())]
        return openings, values

    await stage(origin, original, entry); group(original)
    for step in range(MAX_STEPS+1):
        openings, values = arrays()
        ready = client.preview_context([tokens[module] for module in sorted(tokens)], openings, values)
        need(ready["mathematical_acceptance"] is False, "TERMINAL_PREVIEW_IS_NOT_ACCEPTANCE")
        record["steps"].append({"step": step, "status": ready["status"],
                                "demands": deepcopy(ready["demands"]), "cost": deepcopy(ready["cost"])})
        if ready["status"] == STAGED_READY:
            need(not ready["demands"] and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0
                 and set(selected) == allowed, "TERMINAL_DEMAND_CONTEXT_READY")
            record.update(status=STAGED_READY,
                selected_journals={module: deepcopy(row["journal"]) for module, row in selected.items()},
                cost=deepcopy(ready["cost"]))
            return {"first_module": first, "tokens": tokens, "selected": selected,
                    "openings": openings, "bodies": values}
        need(step < MAX_STEPS and ready["status"] == STAGED_NEED and 0 < len(ready["demands"]) <= 64,
             "TERMINAL_FINITE_CONTEXT_PROGRESS")
        before = len(groups)+len(bodies)+len(selected)
        prior_bodies, prior_groups, prior_modules = set(bodies), set(groups), set(selected)
        unique = set()
        for demand in ready["demands"]:
            encoded = C.canonical(demand)
            need(encoded not in unique, "TERMINAL_DUPLICATE_CONTEXT_DEMAND"); unique.add(encoded)
            kind, module, name = demand["kind"], demand["module"], demand["name"]
            need(module in allowed and kind in ("NeedModuleEvidence", "NeedDeclaration", "NeedBody"),
                 "TERMINAL_UNSELECTED_CONTEXT_DEMAND")
            if kind == "NeedModuleEvidence":
                need(module == BASE and module not in prior_modules,
                     "TERMINAL_ALREADY_STAGED_MODULE_DEMAND")
            else:
                need(module in prior_modules, "TERMINAL_DEMAND_WITHOUT_STAGED_MODULE")
            token, data = await candidate(module, name)
            if module not in selected:
                need(kind == "NeedModuleEvidence" and module == BASE, "TERMINAL_DEMAND_REQUIRES_BASE_EVIDENCE")
                offers = await client.packet_offers(token, max_offers=2, max_bytes=4096)
                need(offers["packets"], "TERMINAL_BASE_EVIDENCE_OFFER")
                await stage(token, data, offers["packets"][0])
                record["base_packet_offer"] = deepcopy(offers["packets"][0])
            if kind == "NeedDeclaration":
                need((module, data["opening"]["index"]) not in prior_groups,
                     "TERMINAL_ALREADY_SATISFIED_DECLARATION_DEMAND")
            group(data)
            if kind == "NeedBody":
                arity, digest = demand["universes"], demand["body_hash"]
                key = module, arity, digest
                if key in bodies:
                    # Two declarations may demand one committed semantic body
                    # in this same batch. Fetch once, but never mask a demand
                    # that was already satisfied in a prior materialization.
                    need(key not in prior_bodies, "TERMINAL_ALREADY_SATISFIED_BODY_DEMAND")
                    continue
                need(len(bodies) < MAX_BODIES, "TERMINAL_BODY_PROGRESS_BOUND")
                result = await client.acquire_body(token, digest, max_bytes=SEMANTIC_BYTES)
                body = result["body"]
                need(body["module_id"] == module and body["relative_name"] == name
                     and body["universes"] == arity and body["body_hash"] == digest
                     and C.body_id(body["expression"], arity) == digest, "TERMINAL_EXACT_DEMANDED_BODY")
                bodies[key] = C.canonical(body["expression"])
                record["bodies"].append({"module": module, "universes": arity, "digest": digest,
                                          "response_sha256": sha(C.canonical(body))})
        need(len(groups)+len(bodies)+len(selected) > before, "TERMINAL_CONTEXT_NO_NEW_DATA")
    raise AssertionError("TERMINAL_UNREACHABLE_PROGRESS_EXIT")


def traffic(client):
    """Stable I/O counters only, excluding live remaining-time observations."""
    report = client.report(); transport = report["transport"]
    return {"search_http": deepcopy(report["search"]["http"]), "delta_http": deepcopy(transport["delta_http"]),
            "structural_http": deepcopy(transport["structural_http"]),
            "acquisition_used": deepcopy(report["acquisition"]["used"])}


class Strategy:
    def __init__(self, context):
        self.context, self.assets = context, Assets(context)
        self.config = self.assets.configuration(); self.envelope = Envelope(**self.config["packet_envelope"])
        self.workspaces, self.clients, self.nodes, self.providers = [], [], [], []
        self.closed_clients = {}
        self.egress = {"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test", "public_ports": [],
            "test_endpoints": [{"host": "127.0.0.1", "port": port} for port in sorted(self.assets.ports.values())]}
        self.specs = query_specs()
        self.services = context.location_workspace/"services"; self.services.mkdir()
        self.report = {"schema": "DMKN_V5_GENUINE_TERMINAL_STRATEGY_V1", "status": "FAIL", "phases": {},
            "cleanup_errors": [], "proof_calls": 0, "guest_calls": 0,
            "authority": "ACTUAL_ORIGINAL_LIVE_A_AND_MIXED_OWNERS_NOT_THIS_REPORT",
            "cold_scope": "FRESH_C_WORKSPACE_AND_OWNERS_SAME_PYTHON_PROCESS_AND_HOST",
            "full_v5_release": False, "positive_full_cost_growth_claim": False,
            "global_search_complete": False, "upstream_certification_cost": "RETAINED_SEPARATE_NOT_ZERO"}

    def open(self, name):
        self.context.remaining_seconds()
        workspace = Workspace.open(self.context.location_workspace/name, self.config, create=True)
        self.workspaces.append(workspace); return workspace

    def client(self, workspace, phase):
        grant = workspace.reserve(self.assets.grant_limits(phase), outer_deadline=self.context.deadline)
        self.report["phases"][phase] = {"grant": grant.identifier}
        client = self.assets.owners(workspace, grant, phase)
        self.clients.append((phase, client)); return grant, client

    def node(self, name, role, workspace, output, deadline, *, bootstrap=(), endpoint=None):
        source = self.context.sources_portable/"location"; selected = self.context.source_sha256
        adoption = AdoptedLocationRuntime(source, {name: selected["portable/location/"+name] for name in SOURCE_NAMES},
            installation_root=self.context.installation, workspace_root=self.context.location_workspace)
        remaining_ms = int((deadline-time.monotonic())*1000)
        need(remaining_ms >= 1000, "TERMINAL_NODE_ORIGINAL_LIFETIME")
        limits = dict(service_ms=min(3600000, remaining_ms), operation_ms=min(15000, remaining_ms),
            query_events=512, provider_limit=4, advertised_keys=2, provider_ttl_ms=120000,
            reprovide_interval_ms=30000, maintenance_ms=60000, commands=32,
            descriptor_requests=16, descriptor_reply_bytes=65536, metadata={},
            transport=dict(outbound_attempts=128, inbound_upgrades=128, receive_bytes=8*MIB, send_bytes=8*MIB))
        cfg = {"schema": "DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", "role": role,
            "state": str(output/(name+"-state")), "namespace": workspace.adapter.namespace,
            "egress": self.egress, "listen": [f'/ip4/127.0.0.1/tcp/{self.assets.ports[name]}'],
            "announce": [], "bootstrap": list(bootstrap), "endpoints": [] if endpoint is None else [endpoint],
            "limits": limits}
        node = ServiceLocationProcess(adoption, {name: selected["portable/location/"+name] for name in ROLE_NAMES},
            cfg, output/(name+"-channel"), deadline=deadline)
        self.nodes.append((name, node)); return node

    async def stop_node(self, node):
        if not node.closed:
            await node.command("stop", {}); await node.close()
        report = node.report()
        need(report["closed"] and report["returncode"] == 0 and not report["channel_failed"]
             and not report["forced_termination"], "TERMINAL_NODE_CLEAN_CLOSE")

    async def provider(self, workspace, name, http_name):
        provider = CompositeProvider(index=workspace.index, custody=workspace.modules, packets=workspace.packets,
                                     max_connections=2, max_requests=128, max_reply_bytes=128*MIB, operation_ms=10000)
        self.providers.append((name, provider))
        endpoint = await provider.start("127.0.0.1", self.assets.ports[http_name])
        service = self.node(name, "index-provider", workspace, self.services, self.context.deadline,
            bootstrap=[self.bootstrap], endpoint={"host": endpoint.host, "port": endpoint.port,
                                                   "tls": endpoint.tls, "server_name": endpoint.server_name})
        ready = await service.start()
        need(len(ready["joins"]) == 1 and ready["joins"][0]["status"] == "CONNECTED", "TERMINAL_PROVIDER_BOOTSTRAP")
        hint = await service.command("publish", {"features": self.features, "stripe": 0})
        need(hint["status"] == "HINT_DISPATCHED_UNACKNOWLEDGED" and hint["error"] is None
             and hint["census"]["add_provider_write"] > 0, "TERMINAL_PROVIDER_HINT")
        return provider, service, hint

    async def stop_provider(self, provider, node):
        await provider.stop(); await self.stop_node(node)
        need(provider.server is None and not provider.tasks and provider.reserved_reply_bytes == 0,
             "TERMINAL_PROVIDER_CLEAN_CLOSE")

    async def close_client(self, phase, client, *, success):
        if phase not in self.closed_clients:
            result = await client.close(); self.closed_clients[phase] = deepcopy(result)
            self.report["phases"][phase]["closed_client"] = deepcopy(result)
        result = self.closed_clients[phase]
        need(result["closed"] and result["receipt"] is None and result["aggregate"]["closed"]
             and result["mixed"]["closed"] and (result["preparation"] is None or result["preparation"]["closed"])
             and result["status"] not in ("CLEANUP_INCOMPLETE", "CLOSED_REPORT_UNCERTAIN"), "TERMINAL_CLIENT_CLOSE")
        if success: need(result["status"] == "CLOSED", "TERMINAL_CLIENT_SUCCESS_CLOSE")

    async def origin(self):
        workspace = self.open("origin"); material = self.assets.origin_material()
        modules = {row["module"] for row in material["terminals"]}
        need(len(material["terminals"]) == 2 and BASE in modules and len(modules) == 2, "TERMINAL_TWO_ORIGIN_MEMBERS")
        first = next(module for module in modules if module != BASE)
        packet_pins = []
        for row in material["terminals"]:
            held = workspace.packets.put(row["module"], row["packet"], before_commit=self.context.remaining_seconds)
            need(held["mathematical_acceptance"] is False
                 and workspace.packets.get(sha(row["packet"]), len(row["packet"])) == row["packet"],
                 "TERMINAL_ORIGIN_PACKET_READBACK")
            packet_pins.append({"module": row["module"], "bytes": len(row["packet"]), "sha256": sha(row["packet"])})
        for row in material["groups"]:
            workspace.modules.put_group(row["module"], row["opening"], before_commit=self.context.remaining_seconds)
            for declaration in row["opening"]["group"]["declarations"]:
                need(workspace.modules.get_group(row["module"], declaration["name"], row["opening"]["index"])[0]
                     == row["opening"], "TERMINAL_ORIGIN_GROUP_READBACK")
        for body in material["bodies"]:
            workspace.modules.put_body(body["module_id"], body["relative_name"], body,
                                       before_commit=self.context.remaining_seconds)
            need(workspace.modules.get_body(body["module_id"], body["relative_name"], body["universes"],
                                            body["body_hash"]) == body, "TERMINAL_ORIGIN_BODY_READBACK")
        name = material["first_export_name"]
        opening, unused = workspace.modules.get_group(first, name)
        index_result = workspace.index.admit(workspace.adapter.encode_opening(first, name, opening),
                                            expected_id=C.export_id(first, name))
        self.features = compile_query(workspace.adapter.namespace, self.specs)
        router = self.node("bootstrap", "reader", workspace, self.services, self.context.deadline)
        ready = await router.start()
        self.bootstrap = f'/ip4/127.0.0.1/tcp/{self.assets.ports["bootstrap"]}/p2p/{P.peer_id(ready["peer_id"])}'
        provider, service, hint = await self.provider(workspace, "origin_location", "origin_http")
        self.report["origin"] = {"packets": packet_pins, "groups": len(material["groups"]),
            "bodies": len(material["bodies"]), "index": index_result, "hint": hint,
            "authority": "STRUCTURAL_DATA_ONLY_NO_ORIGIN_MATHEMATICAL_OWNER"}
        return workspace, first, name, provider, service, router

    async def receiver_b(self, first, first_name):
        workspace = self.open("B"); grant, client = self.client(workspace, "B"); phase = self.report["phases"]["B"]
        reader = self.node("readerB", "reader", workspace, grant.directory, grant.deadline, bootstrap=[self.bootstrap])
        candidate, data, entry = await discover(client, reader, self.specs, self.features, P.OwnerEgressPolicy(self.egress), phase)
        phase["demand_context"] = {}
        staged = await demand_context(client, candidate, data, entry, phase["demand_context"])
        structural = client.report()["structural_staging"]
        need(structural["packets_staged"] == structural["tokens"] == structural["unconsumed"] == 2
             and structural["admission_transitions"] == 0
             and structural["previews"] == len(phase["demand_context"]["steps"]),
             "TERMINAL_COMPLETE_UNCONSUMED_STRUCTURAL_CLOSURE")
        before = traffic(client)
        # No evaluator expected ID/J reached the chooser or structural resolver.
        # All semantic acquisition is complete before this first actual A check.
        warrant = client.admit_staged(staged["tokens"][staged["first_module"]], **self.assets.calls["admit"])
        description = client.describe(warrant); expected = self.assets.expected_journals()
        need(description["kind"] == "A-member" and description["live"]["module"] == first
             and description["live"]["journal"] == expected["FIRST"]
             and description["live"]["aggregate_header"] == self.assets.header
             and {"bytes": description["live"]["receipt_bytes"], "sha256": description["live"]["receipt_sha256"]}
                 == self.assets.receipt_identity
             and data["locator"]["relative_name"] == first_name, "TERMINAL_B_POST_ADMISSION_EXPECTATION")
        base_warrant = client.admit_staged(staged["tokens"][BASE], expected_exact_journal=expected["BASE"],
                                            **self.assets.calls["admit"])
        base = client.describe(base_warrant)
        need(base["kind"] == "A-member" and base["live"]["module"] == BASE
             and base["live"]["journal"] == expected["BASE"]
             and all(base["live"][key] == description["live"][key]
                     for key in ("aggregate_header", "receipt_sha256", "receipt_bytes")),
             "TERMINAL_BASE_ACTUAL_WARRANT")
        ready = client.import_context(
            [{"warrant": warrant, "resolutions": None}, {"warrant": base_warrant, "resolutions": None}],
            [description["live"]["journal"], base["live"]["journal"]], staged["openings"], staged["bodies"])
        after = traffic(client)
        need(ready["status"] == READY and not ready["demands"]
             and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0
             and all(before[key] == after[key] for key in ("search_http", "delta_http", "structural_http")),
             "TERMINAL_STAGED_CLOSURE_REAL_IMPORT_WITHOUT_LATER_DIAL")
        phase.update(structural_before_admission=deepcopy(structural), base_admitted=base,
            local_admission_http_before=before, local_admission_http_after=after,
            preview_authorized_authoring=False, actual_import_status=ready["status"])
        # Trusted evaluator releases the fixed ordinary-source task only now.
        source, roots = self.assets.author_input()
        prepared = client.author(ready["context"], source, roots, **self.assets.calls["author"])
        inspected = inspect_author(prepared, source, roots, grant, envelope=self.envelope,
            aggregate_image=self.assets.aggregate_image, expected_header=self.assets.header,
            expected_target_journal=expected["SECOND"], expected_frontier_journals=[expected["BASE"], expected["FIRST"]],
            required_proof_module=first, required_proof_name=first_name, foundation_bytes=self.assets.foundation)
        raw = prepared["child"]["packet"]
        claims, unused_frontiers, witnesses, census = parse_packet(raw, self.envelope,
                                                                 aggregate_image=self.assets.aggregate_image)
        need(len(witnesses) == 1 and len(claims) == 1 and inspected["root_universes"] == 4,
             "TERMINAL_ONE_NEW_FOUR_UNIVERSE_DELTA")
        need({"bytes": len(claims[0][2]), "sha256": sha(claims[0][2])} == self.assets.receipt_identity,
             "TERMINAL_EXACT_CARRIED_RECEIPT")
        local_spec = C.parse_json(witnesses[0][0], C.Limits(max_bytes=self.envelope.packet_bytes))["local_spec"]
        need(local_spec == self.assets.expected_second_spec(), "TERMINAL_EXACT_SECOND_LOCAL_SPEC")
        published = client.publish(raw, roots, retention_policy=RETENTION)
        need(published["phase"] == "LOCALLY_PUBLISHED" and published["indexed"] == len(roots) == 1,
             "TERMINAL_B_PUBLICATION")
        stored = workspace.read_record("publications", published["publication_id"])
        need(stored["intent"] == published["intent"] and stored["outcome"]["phase"] == "LOCALLY_PUBLISHED"
             and workspace.packets.get(sha(raw), len(raw)) == raw, "TERMINAL_B_PUBLICATION_READBACK")
        phase.update(admitted=description, export=inspected, packet_census=census, publication=published,
                     packet_sha256=sha(raw), packet_bytes=len(raw), context_cost=ready["cost"],
                     carried_receipt=deepcopy(self.assets.receipt_identity), aggregate_header_sha256=sha(self.assets.header))
        replica, service, hint = await self.provider(workspace, "replica_location", "replica_http")
        phase["hint"] = hint
        await self.stop_node(reader); await self.close_client("B", client, success=True)
        return workspace, raw, published, replica, service

    async def receiver_c(self, raw, published, replica, service):
        need(self.closed_clients["B"]["status"] == "CLOSED", "TERMINAL_B_AUTHORITY_CLOSED_BEFORE_C")
        workspace = self.open("C"); grant, client = self.client(workspace, "C"); phase = self.report["phases"]["C"]
        reader = self.node("readerC", "reader", workspace, grant.directory, grant.deadline, bootstrap=[self.bootstrap])
        candidate, data, entry = await discover(client, reader, self.specs, self.features, P.OwnerEgressPolicy(self.egress), phase)
        warrant = await client.acquire(candidate, entry, **self.assets.calls["admit"])
        description = client.describe(warrant); expected = self.assets.expected_journals()
        need(description["kind"] == "mixed" and description["live"]["journal"] == expected["SECOND"]
             and description["live"]["module"] == published["intent"]["module"]
             and entry == {"packet_sha256": sha(raw), "packet_bytes": len(raw)}
             and workspace.packets.get(entry["packet_sha256"], entry["packet_bytes"]) == raw,
             "TERMINAL_C_FRESH_ADMISSION_EXACT_B_PUBLICATION")
        members = {row["module"]: row["journal"] for row in description["members"]}
        need(len(description["members"]) == len(members) == 3
             and set(members.values()) == set(expected.values()), "TERMINAL_C_EXACT_CLOSURE")
        await self.stop_provider(replica, service)
        phase["replica_removed_before_semantics"] = True
        before = traffic(client)
        material = client.semantic_material(warrant)
        need(material["status"] == "AVAILABLE_PACKET_SEMANTICS", "TERMINAL_C_RETAINED_SEMANTICS")
        ready = client.import_context([{"warrant": warrant, "resolutions": None}],
            [members[module] for module in sorted(members)], material["openings"], material["bodies"])
        after = traffic(client)
        # Compare actual I/O and prepaid usage, never ticking report ages.
        need(before == after and ready["status"] == READY and not ready["demands"]
             and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
             "TERMINAL_C_OFFLINE_READY_WITHOUT_NETWORK")
        phase.update(admitted=description, material_census=material["census"],
            unavailable_committed_bodies=material["unavailable_committed_bodies"], context_cost=ready["cost"],
            offline_http_before=before, offline_http_after=after, offline_status=ready["status"],
            semantic_origin="FRESHLY_ADMITTED_ACQUIRED_MIXED_PACKET_ONLY",
            old_report_granted_authority=False, fresh_actual_admission=True)
        await self.stop_node(reader); await self.close_client("C", client, success=True)

    async def cleanup(self):
        errors = []
        for name, provider in reversed(self.providers):
            try:
                await provider.stop()
                need(provider.server is None and not provider.tasks and provider.reserved_reply_bytes == 0,
                     "TERMINAL_PROVIDER_FINAL_CLOSURE")
            except BaseException as error: errors.append(name+"-provider:"+str(error)[:300])
        for name, node in reversed(self.nodes):
            if not node.closed:
                try: await node.command("stop", {})
                except BaseException as error: errors.append(name+"-stop:"+str(error)[:300])
        for phase, client in reversed(self.clients):
            if phase in self.closed_clients: continue
            try: await self.close_client(phase, client, success=False)
            except BaseException as error: errors.append(phase+"-close:"+str(error)[:300])
        for name, node in reversed(self.nodes):
            try: await node.close()
            except BaseException as error: errors.append(name+"-node:"+str(error)[:300])
        for workspace in reversed(self.workspaces):
            try: workspace.close()
            except BaseException as error: errors.append("workspace:"+str(error)[:300])
        self.report.update(cleanup_errors=errors, clients=deepcopy(self.closed_clients),
            nodes={name: node.report() for name, node in self.nodes},
            providers={name: provider.status() for name, provider in self.providers})
        return not errors and len(self.clients) == len(self.closed_clients)

    async def run(self):
        try:
            origin, first, name, provider, service, router = await self.origin()
            unused_workspace, raw, published, replica, replica_service = await self.receiver_b(first, name)
            await self.stop_provider(provider, service); origin.close()
            self.report["origin"]["removed_before_fresh_C"] = True
            await self.receiver_c(raw, published, replica, replica_service)
            await self.stop_node(router)
            br, cr = (self.closed_clients[phase] for phase in ("B", "C"))
            need(br["aggregate"]["attempts"] == cr["aggregate"]["attempts"] == 1
                 and br["mixed"]["attempts"] == 0 and cr["mixed"]["attempts"] == 1
                 and br["counts"]["author_calls"] == 1 and cr["counts"]["author_calls"] == 0
                 and br["counts"]["admission_submissions"] == cr["counts"]["admission_submissions"] == 1
                 and br["acquisition"]["used"]["verify_attempts"] == cr["acquisition"]["used"]["verify_attempts"] == 1
                 and br["receipt"] is None and cr["receipt"] is None, "TERMINAL_EXACT_REAL_OPERATION_COUNTS")
            need(br["structural_staging"]["packets_staged"] == br["structural_staging"]["admission_transitions"] == 2
                 and 1 <= br["structural_staging"]["previews"] <= 24
                 and all(cr["structural_staging"][key] == 0
                         for key in ("packets_staged", "admission_transitions", "previews"))
                 and br["counts"]["new_import_sessions"] == cr["counts"]["new_import_sessions"] == 1,
                 "TERMINAL_EXACT_STAGING_AND_LIVE_IMPORT_COUNTS")
            self.context.remaining_seconds()
            self.report.update(status="PASS_GENUINE_A_DEMAND_IMPORT_AUTHOR_PUBLICATION_FRESH_C_OFFLINE_REUSE",
                actual_operations={"aggregate_checks": 2, "ordinary_author_calls": 1,
                    "mixed_native_checks": 1, "legacy_I_checks": 0, "FIRST_native_proof_replays": 0})
        except BaseException as error:
            self.report["error"] = type(error).__name__+":"+str(error)[:2000]
        finally:
            if not await self.cleanup(): self.report["status"] = "FAIL_CLEANUP"
            save(self.context.location_workspace/"terminal-result.json", self.report)
        return 0 if self.report["status"].startswith("PASS_") else 1


def main(context):
    return asyncio.run(Strategy(context).run())

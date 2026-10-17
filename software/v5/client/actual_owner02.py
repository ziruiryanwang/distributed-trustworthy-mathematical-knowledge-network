"""One ordinary launcher strategy: real I -> reusable method -> reciprocal use.

Trusted local code, three finite grants, zero receipt production. This is not a
benchmark or a claim of global deployment. Phase three is cold CLIENT authority
in the same Python process, not an independent host or a cold-process test.
"""
import asyncio
from pathlib import Path

from aggregate_claims import bindings as B
from authoring.source import NATIVE_NAME_LIMITS
from client.actual_assets02 import (Assets, BASE, MIB, configuration, grant_limits,
                                  need, ordinary, read_pin, save, sha)
from client.workspace import Workspace
from discovery.module_export_adapter import compile_query
from frontier_network.transport import CompositeProvider
from location.controller import AdoptedLocationRuntime, SOURCE_NAMES
from location.controller_services import ServiceLocationProcess, ROLE_NAMES
from location import protocol as P
from modules import codec as C
from modules.model import Address
from modules.source_rows import decode_source

FUSION = [["s", "ClientV5"], ["s", "fusion"]]
PROJECTION = [["s", "ClientV5"], ["s", "project_summary"]]
RETENTION = {"mode": "quota-bounded-local-custody"}
CALL = dict(native_cpu_seconds=30, receipt_cpu_seconds=30, wall_seconds=60, memory_mib=1024)
LOCATION = dict(wall_ms=180000, route_operations=1, routing_events=256,
                routing_peer_slots=4, descriptor_requests=4, contacts=4, reply_bytes=1081344)
SEARCH = dict(providers=4, snapshots=4, requests=8, pages=4, examined=128,
              candidates=16, bytes=MIB, wall_ms=90000, inflight=1)
PAGE = dict(scanned=32, matches=8, bytes=131072, timeout_ms=1000,
            record_probes=256, node_reads=32768, hash_calls=200000, sql_vm_steps=1000000)


def prefix():
    return ("set_option autoImplicit false\nnoncomputable section\nuniverse u v w\n"
            f"open DMKN.Mod.«{BASE}».CommonsV5\nnamespace ClientV5\n")


def seed_source():
    return prefix()+"""theorem fusion {A : Type u} {B : Type v} {C : Type w}
    (leafB : A -> B) (nodeB : B -> B -> B)
    (leafC : A -> C) (nodeC : C -> C -> C) (h : B -> C)
    (hleaf : forall x, h (leafB x) = leafC x)
    (hnode : forall x y, h (nodeB x y) = nodeC (h x) (h y))
    (e : Tree A) : h (fold leafB nodeB e) = fold leafC nodeC e := by
  induction e using Tree.rec with
  | leaf x => exact hleaf x
  | node l r ihl ihr =>
    exact Eq.trans (hnode (fold leafB nodeB l) (fold leafB nodeB r))
      (binary_congr nodeC ihl ihr)
end ClientV5
"""


def projection_source(discovered_module):
    C.digest_string(discovered_module)
    return prefix()+"""theorem project_summary {A : Type u} {B : Type v} {C : Type w}
    (leafB : A -> B) (nodeB : B -> B -> B)
    (leafC : A -> C) (nodeC : C -> C -> C) (e : Tree A) :
    (fold (fun x => (leafB x, leafC x))
      (fun x y => (nodeB x.1 y.1, nodeC x.2 y.2)) e).1 =
    fold leafB nodeB e :=
  DMKN.Mod.«"""+discovered_module+"""».ClientV5.fusion
    (fun x => (leafB x, leafC x))
    (fun x y => (nodeB x.1 y.1, nodeC x.2 y.2))
    leafB nodeB (fun pair : B × C => pair.1)
    (fun _ => rfl) (fun _ _ => rfl) e
end ClientV5
"""


def inspect_author(prepared, source, root, required_module, required_name, grant):
    """Inspect the actual exported proof closure; does not mint acceptance."""
    need(prepared["status"] == "UNTRUSTED_MIXED_DELTA_PACKET_PREPARED"
         and prepared["mathematical_acceptance"] is False, "ACTUAL_AUTHOR_STATUS")
    child = prepared["child"]
    need(child["mathematical_acceptance"] is False and child["roots"] == [root]
         and child["source_sha256"] == sha(source.encode("utf-8")), "ACTUAL_AUTHOR_SOURCE_BINDING")
    request_path = ordinary(Path(prepared["evidence"])/"source-request.json")
    need(request_path.is_relative_to(grant.directory) and request_path.stat().st_size <= 16*MIB,
         "ACTUAL_REQUEST_EVIDENCE_SCOPE")
    with request_path.open("rb") as stream: request_raw = stream.read(16*MIB+1)
    need(len(request_raw) <= 16*MIB, "ACTUAL_REQUEST_BOUND")
    request = C.parse_json(request_raw)
    exported = C.parse_json(read_pin(prepared["export"], 16*MIB))
    need(request["source"] == source and request["roots"] == exported["roots"] == [root]
         and exported["source_sha256"] == child["source_sha256"], "ACTUAL_EXPORT_SOURCE_MATCH")
    context = request["context"]
    external = [{"source_name": C.relocated_name(item["owner"], d["name"]),
                 "module": item["owner"], "relative_name": d["name"]}
                for item in context["imports"] for d in item["group"]["declarations"]]
    env = decode_source(exported["rows"], exported["local_names"], context["foundation_view"]["names"],
                        B.FOUNDATION, B.POLICY, external, NATIVE_NAME_LIMITS)
    raw = read_pin(prepared["packet"], 16*MIB)
    need(raw == child["packet"] and sha(raw) == child["packet_sha256"], "ACTUAL_PACKET_OUTPUT_MATCH")
    witness = C.parse_json(raw)["deltas"][-1]
    need(env.module == child["local_module"] and env.spec == witness["local_spec"],
         "ACTUAL_EXPORTED_SPEC_MATCH")
    declarations = {C.name_key(d["name"]): d for group in env.spec["groups"] for d in group["declarations"]}
    selected = declarations[C.name_key(root)]
    need(selected["kind"] == "theorem" and selected["universes"] == 3, "ACTUAL_GENERIC_ROOT_THEOREM")
    required = ("external", required_module, C.name_key(required_name))
    visits = 0

    def references(expression):
        nonlocal visits
        stack, found = [expression], set()
        edges = {"sort": (), "bvar": (), "const": (), "app": (1, 2),
                 "lam": (2, 3), "forall": (2, 3), "let": (1, 2, 3), "proj": (3,)}
        while stack:
            node = stack.pop(); visits += 1
            need(visits <= 500000, "ACTUAL_INSPECTION_VISIT_BOUND")
            if node[0] in ("const", "proj"):
                ref = node[1]
                found.add((ref[0], ref[1], C.name_key(ref[2])) if ref[0] == "external"
                          else (ref[0], "", C.name_key(ref[1])))
            stack.extend(node[i] for i in edges[node[0]])
        return found

    statement_refs = references(selected["type"])
    need({("external", BASE, C.name_key([["s", "CommonsV5"], ["s", name]]))
          for name in ("Tree", "fold")} <= statement_refs, "ACTUAL_BASE_STATEMENT_REUSE")
    pending, seen, proof_refs = [C.name_key(root)], set(), set()
    while pending:
        key = pending.pop()
        if key in seen: continue
        need(key in declarations and len(seen) < 4096, "ACTUAL_LOCAL_PROOF_CLOSURE")
        seen.add(key); declaration = declarations[key]
        if declaration["kind"] not in ("theorem", "definition", "opaque"): continue
        digest = (env.local_proofs[Address.of(env.module, declaration["name"])]
                  if declaration["kind"] == "theorem" else declaration["value_hash"])
        refs = references(C.parse_json(env.bodies[declaration["universes"], digest]))
        proof_refs.update(refs); pending.extend(ref[2] for ref in refs if ref[0] == "local")
    need(required in proof_refs, "ACTUAL_REQUIRED_EXPORTED_PROOF_EDGE")
    return {"module": env.module, "root": root, "local_groups": len(env.spec["groups"]),
            "export_rows": len(exported["rows"]), "inspected_nodes": visits,
            "required_proof_edge": {"module": required_module, "name": required_name},
            "root_type_sha256": sha(C.canonical(selected["type"])),
            "packet_sha256": sha(raw), "proof_closure_declarations": len(seen),
            "authority": "ACTUAL_EXPORT_REFERENCE_INSPECTION_NOT_MATHEMATICAL_ACCEPTANCE"}


class Strategy:
    def __init__(self, context):
        self.context, self.assets = context, Assets(context)
        self.config = configuration()
        self.origin_root, self.consumer_root = context.location_workspace/"origin", context.location_workspace/"consumer"
        self.workspaces, self.clients, self.nodes, self.providers = [], [], [], []
        self.report = {"schema": "DMKN_V5_CLIENT_ACTUAL_RESULT_V1", "status": "FAIL",
            "phases": {}, "cleanup_errors": [], "proof_calls": 0, "guest_calls": 0,
            "cold_scope": "FRESH_CLIENT_OWNERS_SAME_PYTHON_PROCESS_AND_HOST",
            "consumer_inputs": "FOUNDATION_BASE_VOCABULARY_NEUTRAL_BOOTSTRAP_NO_TARGET_ID_OR_BUNDLE",
            "full_v5_release": False, "mathematical_authority": "LIVE_OWNERS_ONLY_NOT_THIS_REPORT"}

    def open(self, root, create=False):
        self.context.remaining_seconds()
        workspace = Workspace.open(root, self.config, create=create)
        self.workspaces.append(workspace); return workspace

    def client(self, workspace, phase):
        grant = workspace.reserve(grant_limits(phase), outer_deadline=self.context.deadline)
        client = self.assets.owners(workspace, grant, phase)
        self.clients.append((phase, client)); return grant, client

    async def close_client(self, name, client):
        result = await client.close()
        need(result["status"] == "CLOSED" and result["receipt"]["closed"]
             and result["mixed"]["closed"], "ACTUAL_CLIENT_CLOSE:"+name)
        self.report["phases"].setdefault(name, {})["closed_client"] = result

    async def seed(self):
        workspace = self.open(self.origin_root, True); grant, client = self.client(workspace, "seed")
        warrant = client.admit_receipt(self.assets.receipt, self.assets.summary,
                                      cpu_seconds=30, wall_seconds=60, memory_mib=1024)
        description = client.describe(warrant)
        need(description["live"]["module"] == BASE, "ACTUAL_SEED_I_MODULE")
        ready = client.import_context([{ "warrant": warrant, "resolutions": None}],
            [description["live"]["journal"]],
            [{"module": BASE, "opening": row} for row in self.assets.bundle["openings"]],
            [{"module": BASE, "universes": row["universes"], "expression": row["expression"]}
             for row in self.assets.bundle["bodies"]])
        need(ready["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY"
             and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0, "ACTUAL_SEED_CONTEXT")
        source = seed_source()
        prepared = client.author(ready["context"], source, [FUSION], cpu_seconds=60, wall_seconds=120)
        inspected = inspect_author(prepared, source, FUSION, BASE,
                                   [["s", "CommonsV5"], ["s", "binary_congr"]], grant)
        published = client.publish(prepared["child"]["packet"], [FUSION], retention_policy=RETENTION)
        need(published["phase"] == "LOCALLY_PUBLISHED" and published["indexed"] == 1,
             "ACTUAL_SEED_PUBLICATION")
        self.report["phases"]["seed"] = {"context_cost": ready["cost"], "export": inspected,
                                             "publication": published, "grant": grant.identifier}
        await self.close_client("seed", client); workspace.close()
        return published["intent"]["module"]

    def node(self, name, role, grant, workspace, policy, bootstrap=(), endpoint=None):
        source = self.context.sources_portable/"location"
        selected = self.context.source_sha256
        source_pins = {name: selected["portable/location/"+name] for name in SOURCE_NAMES}
        role_pins = {name: selected["portable/location/"+name] for name in ROLE_NAMES}
        adoption = AdoptedLocationRuntime(source, source_pins,
            installation_root=self.context.installation, workspace_root=workspace.root)
        limits = dict(service_ms=min(480000, grant.remaining_seconds()*1000), operation_ms=15000,
            query_events=512, provider_limit=4, advertised_keys=2, provider_ttl_ms=120000,
            reprovide_interval_ms=30000, maintenance_ms=60000, commands=32, descriptor_requests=16,
            descriptor_reply_bytes=65536, metadata={},
            transport=dict(outbound_attempts=128, inbound_upgrades=128, receive_bytes=8*MIB, send_bytes=8*MIB))
        config = {"schema": "DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", "role": role,
            "state": str(grant.directory/(name+"-state")), "namespace": workspace.adapter.namespace,
            "egress": policy, "listen": [f'/ip4/127.0.0.1/tcp/{self.assets.ports[name]}'],
            "announce": [], "bootstrap": list(bootstrap),
            "endpoints": [] if endpoint is None else [endpoint], "limits": limits}
        node = ServiceLocationProcess(adoption, role_pins, config,
                                     grant.directory/(name+"-channel"), deadline=grant.deadline)
        self.nodes.append((name, node)); return node

    async def stop_node(self, node):
        if not node.closed:
            await node.command("stop", {})
            await node.close()
        status = node.report()
        need(status["closed"] and status["returncode"] == 0
             and not status["channel_failed"] and not status["forced_termination"], "ACTUAL_NODE_CLEAN_CLOSE")

    async def consumer(self):
        """No seed module, packet, semantic bundle or live seed authority argument."""
        origin = self.open(self.origin_root)
        workspace = self.open(self.consumer_root, True); grant, client = self.client(workspace, "consumer")
        policy = {"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test", "public_ports": [],
            "test_endpoints": [{"host": "127.0.0.1", "port": p} for p in sorted(self.assets.ports.values())]}
        specs = [{"tag": "declaration-kind", "value": "theorem"},
            {"tag": "result-head", "head": {"tag": "const", "symbol": {"kind": "foundation-name",
                "name_hash": C.hash_value("foundation-symbol", [["s", "Eq"]])}}},
            {"tag": "type-symbol", "symbol": {"kind": "export", "export_id": C.export_id(BASE,
                [["s", "CommonsV5"], ["s", "fold"]])}}]
        features = compile_query(workspace.adapter.namespace, specs)
        router = self.node("router", "reader", grant, workspace, policy)
        ready = await router.start()
        bootstrap = f'/ip4/127.0.0.1/tcp/{self.assets.ports["router"]}/p2p/{P.peer_id(ready["peer_id"])}'
        provider = CompositeProvider(index=origin.index, custody=origin.modules, packets=origin.packets,
                                     max_connections=2, max_requests=32, max_reply_bytes=64*MIB, operation_ms=10000)
        self.providers.append(provider)
        endpoint = await provider.start("127.0.0.1", self.assets.ports["http"])
        public_endpoint = {"host": endpoint.host, "port": endpoint.port, "tls": endpoint.tls,
                           "server_name": endpoint.server_name}
        service = self.node("provider", "index-provider", grant, workspace, policy, [bootstrap], public_endpoint)
        service_ready = await service.start()
        need(len(service_ready["joins"]) == 1 and service_ready["joins"][0]["status"] == "CONNECTED",
             "ACTUAL_PROVIDER_BOOTSTRAP")
        hint = await service.command("publish", {"features": features, "stripe": 0})
        need(hint["status"] == "HINT_DISPATCHED_UNACKNOWLEDGED" and hint["error"] is None
             and hint["census"]["add_provider_write"] > 0, "ACTUAL_PROVIDER_HINT")
        reader = self.node("reader", "reader", grant, workspace, policy, [bootstrap])
        found = await client.find(reader, specs, P.OwnerEgressPolicy(policy), LOCATION, SEARCH,
            routes=[dict(features=features, stripe=0, event_cap=256, peer_cap=4, descriptors=4)])
        need(found["status"] == "QUERY_CONTACTS_READY" and found["contacts"], "ACTUAL_NO_QUERY_CONTACT")
        # One bounded, explicitly selected route/offer/page; no hidden retry.
        contact = found["contacts"][0]
        offered = await client.search_offer(contact, 8192, max_expanded_bytes=MIB, max_age_ms=60000)
        partition = next((row for row in offered["partitions"] if row["anchor_count"] > 0), None)
        need(partition is not None, "ACTUAL_NO_QUERY_PARTITION")
        page = await client.search_page(contact, offered["snapshot_id"], partition["partition"], 0, PAGE)
        need(page["status"] == "VERIFIED_CANDIDATES" and page["matches"], "ACTUAL_NO_QUERY_MATCH")
        candidate = await client.resolve(contact, page["matches"][0])
        candidate_data = client.describe_candidate(candidate)
        discovered = candidate_data["locator"]["module_id"]
        need(candidate_data["locator"]["relative_name"] == FUSION, "ACTUAL_SELECTED_METHOD_INTERFACE")
        offers = await client.packet_offers(candidate, max_offers=2, max_bytes=4096)
        need(offers["packets"], "ACTUAL_NO_PACKET_OFFER")
        warrant = await client.acquire(candidate, offers["packets"][0], **CALL)
        description = client.describe(warrant)
        need(description["live"]["module"] == discovered, "ACTUAL_ACQUIRED_METHOD_BINDING")
        material = client.semantic_material(warrant)
        members = {row["module"]: row["journal"] for row in description["members"]}
        need(set(members) == {BASE, discovered} and material["status"] == "AVAILABLE_PACKET_SEMANTICS",
             "ACTUAL_PACKET_ONLY_IMPORT_MEMBERS")
        ready = client.import_context([{"warrant": warrant, "resolutions": None}],
            [members[module] for module in sorted(members)], material["openings"], material["bodies"])
        need(ready["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY"
             and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0, "ACTUAL_ACQUIRED_CONTEXT")
        source = projection_source(discovered)
        prepared = client.author(ready["context"], source, [PROJECTION], cpu_seconds=60, wall_seconds=120)
        inspected = inspect_author(prepared, source, PROJECTION, discovered, FUSION, grant)
        published = client.publish(prepared["child"]["packet"], [PROJECTION], retention_policy=RETENTION)
        need(published["phase"] == "LOCALLY_PUBLISHED" and published["indexed"] == 1,
             "ACTUAL_SUCCESSOR_PUBLICATION")
        self.report["phases"]["consumer"] = {"discovery": found, "candidate": candidate_data,
            "hint": hint, "publication": published, "export": inspected, "context_cost": ready["cost"],
            "material_census": material["census"], "grant": grant.identifier,
            "semantic_origin": "ACTUAL_ACQUIRED_PACKET_ONLY"}
        await self.stop_node(reader)
        await self.close_client("consumer", client)
        await provider.stop(); await self.stop_node(service); await self.stop_node(router)
        need(provider.server is None and not provider.tasks, "ACTUAL_PROVIDER_CLOSED")
        origin.close(); workspace.close()
        return discovered, published

    async def cold(self, published):
        need(all(node.closed for unused, node in self.nodes)
             and all(provider.server is None and not provider.tasks for provider in self.providers),
             "ACTUAL_ORIGIN_SERVICES_MUST_BE_CLOSED")
        workspace = self.open(self.consumer_root)
        prior = workspace.read_record("publications", published["publication_id"])
        need(prior["intent"] == published["intent"] and prior["outcome"]["phase"] == "LOCALLY_PUBLISHED",
             "ACTUAL_REOPEN_PUBLICATION_RECORD")
        grant, client = self.client(workspace, "cold")
        intent = prior["intent"]
        warrant = client.admit_local(intent["module"], intent["packet_sha256"], intent["packet_bytes"], **CALL)
        description = client.describe(warrant)
        need(description["live"]["module"] == intent["module"] and len(description["members"]) == 3,
             "ACTUAL_COLD_CLIENT_ADMISSION")
        self.report["phases"]["cold"] = {"module": intent["module"], "grant": grant.identifier,
            "publication_id": published["publication_id"], "packet_sha256": intent["packet_sha256"],
            "members": [row["module"] for row in description["members"]],
            "old_report_granted_authority": False, "fresh_actual_admission": True}
        await self.close_client("cold", client); workspace.close()

    async def cleanup(self):
        errors = []
        for unused, node in reversed(self.nodes):
            if not node.closed:
                try: await node.command("stop", {})
                except BaseException as error: errors.append("node-stop:"+str(error)[:300])
        for name, client in reversed(self.clients):
            try: await client.close()
            except BaseException as error: errors.append(name+"-close:"+str(error)[:300])
        for unused, node in reversed(self.nodes):
            try: await node.close()
            except BaseException as error: errors.append("node-close:"+str(error)[:300])
        for provider in reversed(self.providers):
            try: await provider.stop()
            except BaseException as error: errors.append("provider-stop:"+str(error)[:300])
        for workspace in reversed(self.workspaces):
            try: workspace.close()
            except BaseException as error: errors.append("workspace-close:"+str(error)[:300])
        self.report["cleanup_errors"] = errors
        self.report["nodes"] = {name: node.report() for name, node in self.nodes}
        self.report["providers"] = [provider.status() for provider in self.providers]
        self.report["clients"] = {name: client.report() for name, client in self.clients}
        return not errors

    async def run(self):
        try:
            seed_module = await self.seed()
            discovered, published = await self.consumer()
            # Post-hoc equality is outside the unknown-ID consumer algorithm.
            need(discovered == seed_module, "ACTUAL_DISCOVERED_PUBLISHED_SEED")
            await self.cold(published)
            clients = self.report["phases"]
            need(sum(clients[name]["closed_client"]["receipt"]["attempts"] for name in clients) == 3
                 and sum(clients[name]["closed_client"]["counts"]["author_calls"] for name in clients) == 2,
                 "ACTUAL_EXACT_RECEIPT_AUTHOR_CALLS")
            self.context.remaining_seconds()
            self.report["status"] = "PASS_ORDINARY_CLIENT_RECIPROCAL_USE_AND_COLD_CLIENT_READMISSION"
        except BaseException as error:
            self.report["error"] = type(error).__name__+":"+str(error)[:2000]
        finally:
            if not await self.cleanup(): self.report["status"] = "FAIL_CLEANUP"
            save(self.context.location_workspace/"actual-result.json", self.report)
        return 0 if self.report["status"].startswith("PASS_") else 1


def main(context):
    return asyncio.run(Strategy(context).run())

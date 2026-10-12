"""One selected genuine-A author/discover/retain/provider-loss operation.

Owner-controlled harness, not a public sandbox or new acceptance authority.
Root must supply an adopted actual A image/receipt and exact fresh profile pins.
No mock verifier, I receipt call, proof production, baseline rerun or retry.
"""
from pathlib import Path
import argparse
import asyncio
import hashlib
import math
import os
import sqlite3
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from admission.bindings import journal
from aggregate_claims import bindings as B
from aggregate_claims.aggregate_admission import AggregateReceiptVerifier
from custody.module_store import ModuleStore, permitted_hashes, BODY_SCHEMA
from discovery.discovery_store import Store
from discovery.module_export_adapter import ModuleExportAdapter, compile_query
from location import protocol as P
from location.available_descriptor import descriptor
from location.observed_route import route, CENSUS
from location.controller import AdoptedLocationRuntime, SOURCE_NAMES, ordinary
from location.controller_services import ServiceLocationProcess, ROLE_NAMES
from mixed_claims.authoring import MixedSourceOperation, MixedOwnerPreparation, prepare_mixed_context
from mixed_claims.imports import MixedImportSession
from mixed_claims.packet import Envelope, parse_packet
from mixed_claims.receiver import MixedDeltaVerifier
from mixed_network.custody import PacketStore, public_profile
from mixed_network.transport import CompositeProvider, MixedLocatedHandoff, MixedAcquisition
from modules import codec as C
from production.producer import encoded, parse, fields, require, uint, digest, pin_fields, file_pin, MIB
from transport.receipt_client import AcquisitionBudget

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
V5 = ROOT / "software/v5"
SOURCE_V5 = Path(__file__).resolve().parents[1]
SCHEMA = "DMKN_V5_REAL_A_RECIPROCAL_OPERATION_V1"
BASE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
FIRST = "4adbc049e4d1e29ec045d64c7dba9e27bdd506dfa6c7fb707f022be40439e742"
SECOND = "52c564f87f31082468557df6eed0a04bc7adf9d28d9614fe6cf173f5633088bf"
IMAGE, FOUNDATION, POLICY = B.RELATION_IMAGE, B.FOUNDATION, B.POLICY
PORTS = ("bootstrap", "origin_location", "replica_location", "reader1", "reader2", "origin_http", "replica_http")
INPUT_PINS = {
    "source": (1383, "a4e2d897f929e2e63c43c70f274a8f270d9bb783180a6677366ae50ad73df153"),
    "roots": (52, "7882f5358514ab6fbe98c212868e267cd9d0dc4a20561b2702d66530a868b2e9"),
    "base_bundle": (53769, "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926"),
    "foundation": (23313, "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"),
    "first_input": (113220, "88b71b8282afc99297bf6564d22616fce6211eed9a9e18afa1cb42a41d1206e1"),
    "first_journal": (184, "07734789fd165d5c29667a2925c09b882d346db97a511c75644f2cb4b8ccd0da"),
    "reference_packet": (662480, "54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1"),
}
CONFIG = ("schema", "inputs", "aggregate", "lineage", "preparation_profile", "owner_allowance",
          "native_executable", "runtime_pins", "location", "ports", "output_directory", "limits")
LIMITS = ("wall_seconds", "controller_cpu_seconds", "output_bytes", "output_entries", "call", "author",
          "node", "location", "search", "candidate", "acquisition", "module_store", "packet_store",
          "index_store", "provider", "offer_bytes")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_pin(row, maximum=16*MIB):
    path = pin_fields(row, maximum)
    ordinary(path)
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    require(len(raw) == row["bytes"] and sha(raw) == row["sha256"], "RECIPROCAL_INPUT_PIN")
    return raw


def exact_bytes(value, size):
    require(type(value) is list and len(value) == size
            and all(type(part) is int and 0 <= part <= 255 for part in value), "RECIPROCAL_EXACT_BYTES")
    return bytes(value)


def save(path, value):
    raw = encoded(value)
    require(len(raw) <= 4*MIB, "RECIPROCAL_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def source_closure(runtime):
    paths = {Path(__file__).resolve()}
    for module in tuple(sys.modules.values()):
        value = getattr(module, "__file__", None)
        if value is None:
            continue
        path = Path(value).resolve()
        parts = path.parts
        project_v5 = any(parts[i:i+2] == ("software", "v5") for i in range(len(parts)-1))
        if path.is_relative_to(ROOT) and path.suffix == ".py" and project_v5:
            require(path.is_relative_to(SOURCE_V5), "RECIPROCAL_FOREIGN_PROJECT_SOURCE")
            paths.add(path)
    require(paths <= {Path(path) for path in runtime}, "RECIPROCAL_LOADED_SOURCE_NOT_PINNED")
    return sorted(str(path) for path in paths)


def semantic_material(raw, aggregate_image, store, check):
    """Selected structural custody from acquired bytes; never mathematical authority."""
    unused_claims, unused_frontiers, witnesses, census = parse_packet(
        raw, Envelope(), aggregate_image=aggregate_image)
    groups, available = {}, {}

    def opening(owner, value):
        C.verify_group_opening(owner, value)
        key = owner, value["index"]
        require(key not in groups or C.canonical(groups[key]) == C.canonical(value),
                "RECIPROCAL_SEMANTIC_GROUP_CONFLICT")
        groups[key] = value

    for witness_raw, unused_parents, unused_summary, unused_rank in witnesses:
        witness = C.parse_json(witness_raw)
        spec = witness["local_spec"]
        owner = C.module_id(spec)
        for index in range(len(spec["groups"])):
            opening(owner, C.group_opening(spec, index))
        for parent in witness["parents"]:
            owner = journal(bytes(parent["journal"]))["module"]
            for value in parent["openings"]:
                opening(owner, value)
        for body in witness["bodies"]:
            key = body["universes"], body["digest"]
            require(C.body_id(body["expression"], body["universes"]) == body["digest"],
                    "RECIPROCAL_SEMANTIC_BODY_DIGEST")
            require(key not in available or C.canonical(available[key]) == C.canonical(body["expression"]),
                    "RECIPROCAL_SEMANTIC_BODY_CONFLICT")
            available[key] = body["expression"]
    bodies, missing = {}, []
    for (owner, index), value in sorted(groups.items()):
        check()
        store.put_group(owner, value, before_commit=check)
        for declaration in value["group"]["declarations"]:
            held, unused = store.get_group(owner, declaration["name"], index)
            require(held == value, "RECIPROCAL_SEMANTIC_GROUP_READBACK")
            for digest_value in sorted(permitted_hashes(declaration)):
                key = declaration["universes"], digest_value
                if key not in available:
                    missing.append({"module": owner, "name": declaration["name"],
                                    "universes": key[0], "digest": key[1]})
                    continue
                response = {"schema": BODY_SCHEMA, "module_id": owner, "relative_name": declaration["name"],
                            "universes": key[0], "body_hash": key[1], "expression": available[key]}
                store.put_body(owner, declaration["name"], response, before_commit=check)
                require(store.get_body(owner, declaration["name"], *key) == response,
                        "RECIPROCAL_SEMANTIC_BODY_READBACK")
                bodies.setdefault((owner, *key), response)
    check()
    return groups, bodies, {"packet_census": census, "groups": len(groups), "bodies": len(bodies),
        "unavailable_committed_values": missing, "origin": "ACQUIRED_MIXED_PACKET_ONLY",
        "all_future_bodies_covered": False, "mathematical_acceptance": False}


class Campaign:
    def __init__(self, config, output, deadline, cpu_started, report, runtime, preparation, adoption):
        self.cfg, self.out, self.deadline = config, output, deadline
        self.cpu_started, self.report, self.runtime = cpu_started, report, runtime
        self.preparation_profile, self.adoption = preparation, adoption
        self.limits = config["limits"]
        self.adapter = ModuleExportAdapter(C, FOUNDATION, POLICY)
        self.aggregate_image = config["aggregate"]["image"]
        self.profile = public_profile(self.aggregate_image)
        self.features = compile_query(self.adapter.namespace, [
            {"tag": "declaration-kind", "value": "theorem"},
            {"tag": "result-head", "head": {"tag": "const", "symbol": {"kind": "foundation-name",
             "name_hash": C.hash_value("foundation-symbol", [["s", "Eq"]])}}},
            {"tag": "type-symbol", "symbol": {"kind": "export", "export_id": C.export_id(BASE,
             [["s", "CommonsV5"], ["s", "fold"]])}}])
        self.egress = {"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test", "public_ports": [],
            "test_endpoints": [{"host": "127.0.0.1", "port": port} for port in sorted(config["ports"].values())]}
        self.policy = P.OwnerEgressPolicy(self.egress)
        self.nodes, self.providers, self.stores, self.owners = [], [], [], []
        self.frontiers, self.receivers, self.clients, self.phases = [], [], [], []
        self.preparation = None

    def remaining(self):
        require(time.process_time()-self.cpu_started <= self.limits["controller_cpu_seconds"],
                "RECIPROCAL_CONTROLLER_CPU")
        left = math.floor(self.deadline-time.monotonic())
        require(left >= 1, "RECIPROCAL_ORIGINAL_DEADLINE")
        return left

    def census(self):
        size = count = 0
        for directory, dirs, files in os.walk(self.out, followlinks=False):
            self.remaining()
            for name in dirs+files:
                path = Path(directory)/name
                ordinary(path, directory=name in dirs)
                count += 1
                if name in files:
                    size += path.stat().st_size
                require(size <= self.limits["output_bytes"] and count <= self.limits["output_entries"],
                        "RECIPROCAL_EVIDENCE_CENSUS")
        return {"bytes": size, "entries": count, "scope": "THIS_EVIDENCE_ROOT_ONLY_SAMPLED_NOT_HARD_DISK_LIMIT"}

    def register(self, name, owner):
        self.owners.append((name, owner))
        return owner

    def aggregate_owner(self, name):
        self.remaining()
        selected, call = self.cfg["aggregate"], self.limits["call"]
        manifest = selected["supervisor_manifest"]
        owner = AggregateReceiptVerifier(supervisor_manifest=manifest["path"],
            supervisor_manifest_sha256=manifest["sha256"], executable=selected["executable"]["path"],
            runtime_pins=self.runtime, aggregate_image=self.aggregate_image, operations=1,
            submitted_bytes=8*MIB, reserved_cpu_seconds=call["receipt_cpu_seconds"],
            wall_seconds=self.remaining(), member_calls=4096, member_storage=8, member_bytes=8*MIB,
            controller_cpu_seconds=self.limits["controller_cpu_seconds"], output_bytes=64*MIB, output_entries=256)
        self.register(name+"-aggregate", owner)
        self.frontiers.append((name, owner))
        return owner

    def cold(self, name):
        frontier = self.aggregate_owner(name)
        call = self.limits["call"]
        receiver = MixedDeltaVerifier(aggregate_verifier=frontier,
            native_executable=self.cfg["native_executable"]["path"], runtime_pins=self.runtime,
            output_directory=self.out/(name+"-admission"),
            envelope=Envelope(packet_bytes=self.limits["packet_store"]["packet_bytes"],
                              claims=1, frontiers=2, deltas=1, edges=2),
            operations=1, submitted_bytes=self.limits["packet_store"]["packet_bytes"],
            reserved_cpu_seconds=call["receipt_cpu_seconds"]+call["native_cpu_seconds"],
            controller_cpu_seconds=self.limits["controller_cpu_seconds"], wall_seconds=self.remaining(),
            output_bytes=64*MIB, output_entries=256)
        self.register(name+"-mixed", receiver)
        self.receivers.append((name, receiver))
        return frontier, receiver

    def author(self, material, receipt, header, members):
        """No FIRST proof or reference SECOND witness is passed into this function."""
        frontier = self.aggregate_owner("author")
        call = self.limits["call"]
        handle = frontier.receive(receipt, header, self.out/"author-aggregate-admission",
            cpu_seconds=call["receipt_cpu_seconds"], wall_seconds=min(call["wall_seconds"], self.remaining()),
            memory_mib=call["memory_mib"])
        session = self.register("author-session", MixedImportSession(aggregate_verifier=frontier,
            max_sources=2, max_members=2, max_receipts=1, max_calls=4096,
            submitted_bytes=32*MIB, data_bytes=16*MIB, wall_seconds=self.remaining()))
        for module in (BASE, FIRST):
            row = members[module]
            member = frontier.select_member(handle, row["journal"], row["index"], row["siblings"])
            require(session.use_aggregate_member(member, receipt) == row["journal"],
                    "RECIPROCAL_IMPORTED_EXACT_MEMBER")
            require(session.select_warrant(row["journal"]) == module, "RECIPROCAL_MEMBER_SELECTION")
            for opening in material[module]["openings"]:
                session.open_group(module, opening)
            for body in material[module]["bodies"]:
                require(session.supply_body(module, body["universes"], body["expression"]) == body["digest"],
                        "RECIPROCAL_IMPORTED_BODY")
        operation = self.register("author-source", MixedSourceOperation(session, material["foundation"],
            self.cfg["inputs"]["foundation"]["sha256"], material["source"], material["roots"],
            envelope=Envelope(packet_bytes=self.limits["packet_store"]["packet_bytes"],
                              claims=1, frontiers=2, deltas=1, edges=2)))
        prepared = operation.prepare()
        require(prepared["status"] == "OWNER_SOURCE_REQUIRES_SUPERVISED_LEAN_AND_FINAL_RELATION"
                and prepared["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
                "RECIPROCAL_ORDINARY_AUTHOR_CONTEXT")
        allowance = {**self.cfg["owner_allowance"],
                     "wall_seconds": min(self.cfg["owner_allowance"]["wall_seconds"], self.remaining())}
        self.preparation = self.register("preparation", MixedOwnerPreparation(
            self.preparation_profile, allowance, self.out/"preparation"))
        self.report["author_calls"] += 1
        result = self.preparation.author(operation, "second", **{**self.limits["author"],
            "wall_seconds": min(self.limits["author"]["wall_seconds"], self.remaining())})
        require(result["status"] == "UNTRUSTED_MIXED_DELTA_PACKET_PREPARED"
                and result["mathematical_acceptance"] is False
                and result["child"]["status"] == "UNTRUSTED_MIXED_DELTA_PACKET"
                and result["child"]["mathematical_acceptance"] is False,
                "RECIPROCAL_UNTRUSTED_AUTHOR_OUTPUT")
        raw = read_pin(result["packet"])
        require(raw == result["child"]["packet"], "RECIPROCAL_AUTHOR_SAVED_PACKET")
        self.report["author"] = {"packet": result["packet"], "export": result["export"],
            "context_cost": prepared["cost"], "parent_selection_binding": result["child"]["parent_selection_binding"],
            "source_sha256": result["child"]["source_sha256"], "census": result["child"]["census"],
            "imported_modules": [BASE, FIRST], "imported_first_proof_bytes": 0,
            "imported_second_authority": False, "result_is_untrusted": True}
        operation.close()
        session.close()
        self.preparation.close()
        frontier.close()
        self.remaining()
        return raw

    def stores_for(self, name):
        self.remaining()
        modules = ModuleStore(self.out/(name+"-modules"), C, FOUNDATION, POLICY,
                              self.limits["module_store"], create=True)
        self.stores.append((name+"-modules", modules))
        packets = PacketStore(self.out/(name+"-packets"), self.profile,
                              self.limits["packet_store"], create=True)
        self.stores.append((name+"-packets", packets))
        return modules, packets

    def index_for(self, name):
        index = Store(self.out/(name+"-index"), self.adapter, self.limits["index_store"], create=True)
        self.stores.append((name+"-index", index))
        return index

    def node(self, name, role, bootstrap=(), endpoint=None):
        self.remaining()
        config = {"schema": "DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", "role": role,
            "state": str(self.out/(name+"-state")), "namespace": self.adapter.namespace, "egress": self.egress,
            "listen": [f'/ip4/127.0.0.1/tcp/{self.cfg["ports"][name]}'], "announce": [],
            "bootstrap": list(bootstrap), "endpoints": [] if role == "reader" else [endpoint],
            "limits": dict(self.limits["node"])}
        node = ServiceLocationProcess(self.adoption, self.cfg["location"]["role_pins"], config,
                                      self.out/(name+"-controller"), deadline=self.deadline)
        self.nodes.append((name, node))
        return node

    async def start_node(self, name, node, joined=True):
        ready = await node.start()
        require(ready["role"] == node.config["role"]
                and ready["startup_assurance"] == "LISTENING_AND_DIAL_ATTEMPTED_NOT_ROUTING_READY"
                and ready["query_readiness"] == "EVENT_BASED_UNDER_ORIGINAL_OPERATION_SIGNAL",
                "RECIPROCAL_NODE_EVENT_READINESS")
        if joined:
            require(len(ready["joins"]) == 1 and ready["joins"][0]["status"] == "CONNECTED",
                    "RECIPROCAL_BOOTSTRAP_JOIN")
        save(self.out/(name+"-ready.json"), ready)
        self.remaining()
        return ready

    async def provider(self, name, index, modules, packets, bootstrap):
        http = CompositeProvider(index=index, custody=modules, packets=packets, **self.limits["provider"])
        self.providers.append((name, http))
        endpoint = await http.start(host="127.0.0.1", port=self.cfg["ports"][name+"_http"])
        ep = {"host": endpoint.host, "port": endpoint.port, "tls": endpoint.tls, "server_name": endpoint.server_name}
        channel = self.node(name+"_location", "index-provider", [bootstrap], ep)
        await self.start_node(name+"_location", channel)
        published = await channel.command("publish", {"features": self.features, "stripe": 0})
        save(self.out/(name+"-publication.json"), published)
        # Adopted continuation semantics: a partial hint is not a failed theorem
        # or a discovery success. Actual route/search below decides availability.
        fields(published, ("route_key", "status", "termination", "error", "census", "routing_peers_before",
                           "routing_peers_after", "remote_placement_confirmed", "assurance",
                           "global_complete", "mathematical_acceptance"))
        fields(published["census"], CENSUS)
        census = published["census"]
        for key in CENSUS[:-1]:
            uint(census[key], 8192)
        require(all(census[key] <= census["events"] for key in CENSUS[1:-1])
                and census["add_provider_write"] <= census["peer_response"], "RECIPROCAL_PUBLICATION_CENSUS")
        require(census["last_query_error"] is None or type(census["last_query_error"]) is str
                and len(census["last_query_error"]) <= 500, "RECIPROCAL_PUBLICATION_ERROR")
        for key in ("routing_peers_before", "routing_peers_after"):
            uint(published[key], 16384)
        partial = (published["status"] == "INCOMPLETE" and published["termination"] == "QUERY_ERRORS"
                   and census["query_error"] > 0 and published["error"] is None)
        complete = (published["status"] == "HINT_DISPATCHED_UNACKNOWLEDGED"
                    and published["termination"] == "ITERATOR_EXHAUSTED"
                    and census["query_error"] == 0 and census["add_provider_write"] > 0
                    and published["error"] is None)
        no_write = (published["status"] == "INCOMPLETE" and published["termination"] == "NO_PROVIDER_RECORD_WRITE"
                    and census["query_error"] == census["add_provider_write"] == 0 and published["error"] is None)
        bounded_abort = (published["status"] == "INCOMPLETE" and published["termination"] == "ABORTED_OR_FAILED"
                         and published["error"] in ("TimeoutError: The operation was aborted due to timeout",
                                                    "Error: LOCATION_QUERY_EVENT_CAP"))
        require((partial or complete or no_write or bounded_abort) and published["remote_placement_confirmed"] is False
                and published["assurance"] == P.ASSURANCE and published["global_complete"] is False
                and published["mathematical_acceptance"] is False
                and published["route_key"] == P.route_key(self.adapter.namespace, self.features, 0)
                and not channel.closed and not channel.channel_failed
                and channel.process is not None and channel.process.returncode is None
                and time.monotonic() < channel.deadline, "RECIPROCAL_BOUNDED_PUBLICATION")
        self.remaining()
        return http, channel

    async def stop_node(self, node):
        if node.closed:
            return
        await node.command("stop", {})
        await node.close()
        require(node.process is not None and node.process.returncode == 0
                and not node.channel_failed and not node.forced_termination, "RECIPROCAL_GRACEFUL_NODE_EXIT")

    async def reader(self, name, bootstrap, final_context=False):
        """Candidate choice gets no expected target ID, packet hash or provider endpoint."""
        phase = {"name": name, "routes": [], "descriptors": [], "searches": [], "admitted": False,
            "initial_contacts": 0, "known_target_ids": [], "known_http_endpoints": [],
            "query_specs_origin": "LOCAL_BASE_VOCABULARY_THEOREM_EQ_FOLD",
            "bootstrap_scope": "NEUTRAL_READER_ROUTER_WITH_NO_PUBLICATION_OR_CUSTODY"}
        self.phases.append(phase)
        modules, packets = self.stores_for(name)
        budget = AcquisitionBudget(self.deadline, self.limits["acquisition"])
        channel = self.node(name, "reader", [bootstrap])
        handoff = MixedLocatedHandoff(channel, self.adapter, self.features, self.policy, budget,
                                     self.limits["location"], self.limits["search"])
        phase["prestart_budget"] = budget.report()
        require(handoff.location.report()["workflow"]["contacts"] == 0, "RECIPROCAL_NO_PRELOADED_CONTACT")
        await self.start_node(name, channel)
        attempted, contacts = set(), []
        # Two bounded existing routes at most. No wait/retry or new grant.
        for route_number in range(2):
            located = await route(handoff.location, self.features,
                event_cap=self.limits["location"]["routing_events"]//2,
                peer_cap=min(self.limits["node"]["provider_limit"], self.limits["location"]["routing_peer_slots"]//2))
            phase["routes"].append(located)
            for peer in located["peers"]:
                if peer in attempted:
                    continue
                attempted.add(peer)
                reply = await descriptor(handoff.location, peer, located["route_key"], max_bytes=4096, max_age_ms=60000)
                phase["descriptors"].append({"route": route_number, "peer": peer, "reply": reply})
                if reply["status"] != "DESCRIPTOR_UNAVAILABLE":
                    require(reply["status"] == "ADOPTED_ADVISORY_CONTACTS", "RECIPROCAL_DESCRIPTOR_OUTCOME")
                    contacts.extend(item for item in reply["contacts"] if item not in contacts)
            if contacts:
                break
        require(contacts, "RECIPROCAL_NO_LOCATED_CONTACT")
        search = handoff.begin_search()
        frontier, receiver = self.cold(name)
        client = self.register(name+"-client", MixedAcquisition.from_search(
            handoff, self.profile, modules, packets, verifier=receiver))
        self.clients.append((name, client))
        selected = None
        for contact in contacts:
            try:
                offered = await search.offer(contact, self.limits["offer_bytes"], max_expanded_bytes=MIB, max_age_ms=60000)
                phase["searches"].append({"contact": contact, "offer": offered})
                partition = next((row for row in offered["partitions"] if row["anchor_count"] > 0), None)
                if partition is None:
                    continue
                page = await search.candidates(contact, offered["snapshot_id"], partition["partition"], 0,
                                               self.limits["candidate"])
                phase["searches"][-1]["page"] = page
                require(page["status"] == "VERIFIED_CANDIDATES" and page["mathematical_acceptance"] is False
                        and page["verified_scan_coverage"] is False, "RECIPROCAL_CANDIDATES_NOT_AUTHORITY")
            except Exception as error:
                phase["searches"].append({"contact": contact, "failure": type(error).__name__+":"+str(error)[:1000]})
                budget.active()
                continue
            if page["matches"]:
                selected = contact, page["matches"][0]
                break
        require(selected is not None, "RECIPROCAL_NO_RETURNED_CANDIDATE")
        contact, record = selected
        resolved = await client.export(contact, record)
        module = resolved["locator"]["module_id"]
        offered = await client.offers(contact, module, max_offers=2, max_bytes=4096)
        require(offered["packets"], "RECIPROCAL_NO_MIXED_PACKET_OFFER")
        entry = offered["packets"][0]
        acquired = await client.packet(contact, module, entry)
        held = client.custody_ready(resolved, entry)
        require((held["census"]["claims"], held["census"]["frontiers"], held["census"]["deltas"])
                == (1, 2, 1), "RECIPROCAL_ONE_A_TWO_FRONTIERS_ONE_DELTA")
        admitted = client.admit(resolved, entry, **{**self.limits["call"],
            "wall_seconds": min(self.limits["call"]["wall_seconds"], self.remaining())})
        live = receiver.describe(admitted["handle"])
        raw = packets.get(entry["packet_sha256"], entry["packet_bytes"])
        inventory = receiver.members(admitted["handle"])
        require(live["module"] == module and journal(live["journal"])["rank"] == 2
                and receiver.export_packet(admitted["handle"]) == raw and len(inventory) == 3
                and sum(item["proof_form"] == "a-member-frontier" for item in inventory) == 2
                and sum(item["proof_form"] == "native-delta" for item in inventory) == 1,
                "RECIPROCAL_COMPLETE_LIVE_ADMISSION")
        groups, bodies, semantics = semantic_material(raw, self.aggregate_image, modules, budget.active)
        phase["semantic_custody"] = semantics
        if final_context:
            session = self.register(name+"-session", MixedImportSession(delta_verifier=receiver,
                max_sources=1, max_members=3, max_receipts=1, max_calls=4096,
                submitted_bytes=32*MIB, data_bytes=16*MIB, wall_seconds=self.remaining()))
            session.use_delta_handle(admitted["handle"])
            for item in inventory:
                session.select_warrant(item["journal"])
            for (owner, index), opening in sorted(groups.items()):
                representative = opening["group"]["declarations"][0]["name"]
                readback, unused = modules.get_group(owner, representative, index)
                session.open_group(owner, readback)
            for (owner, arity, digest_value), value in sorted(bodies.items()):
                readback = modules.get_body(owner, value["relative_name"], arity, digest_value)
                require(session.supply_body(owner, arity, readback["expression"]) == digest_value,
                        "RECIPROCAL_FINAL_IMPORT_BODY")
            context = prepare_mixed_context(session, read_pin(self.cfg["inputs"]["foundation"]),
                                            self.cfg["inputs"]["foundation"]["sha256"])
            require(context["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY"
                    and context["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
                    "RECIPROCAL_FINAL_ORDINARY_IMPORT_CONTEXT")
            save(self.out/(name+"-context.json"), context)
            phase["ordinary_import"] = {"status": context["status"], "cost": context["cost"],
                "selection_binding": context["selection_binding"], "author_calls": 0}
            session.close()
        require(frontier.report()["attempts"] == receiver.report()["attempts"] == 1,
                "RECIPROCAL_READER_SINGLE_COLD_CALL")
        phase.update(admitted=True, module=module, journal=list(live["journal"]), record=record, packet=entry,
            acquired=acquired, custody=held, actual_A_verifications=1, actual_native_checks=1,
            selected_contact_origin="ACTUAL_NOISE_DESCRIPTOR_WORKFLOW",
            selected_candidate_origin="FIRST_ACTUAL_RETURNED_FORMAL_QUERY_MATCH",
            search_final=search.report(), location_final=handoff.location.report(), client_final=client.report())
        exported = self.adapter.encode_opening(module, resolved["locator"]["relative_name"], resolved["opening"])
        require(self.adapter.extract(exported) == record, "RECIPROCAL_REPLICA_EXPORT_BINDING")
        client.close()
        frontier.close()
        phase["closed_receiver"], phase["closed_frontier"] = receiver.report(), frontier.report()
        await self.stop_node(channel)
        save(self.out/(name+"-result.json"), phase)
        self.census()
        return modules, packets, exported, module, entry

    async def cleanup(self):
        errors = []
        for name, owner in reversed(self.owners):
            try:
                owner.close()
            except BaseException as error:
                errors.append({"owner": name, "phase": "owner-close", "error": str(error)[:1000]})
        for name, node in reversed(self.nodes):
            try:
                if not node.closed and not node.channel_failed and node.process is not None and node.process.returncode is None:
                    await node.command("stop", {})
            except BaseException as error:
                errors.append({"owner": name, "phase": "node-stop", "error": str(error)[:1000]})
            try:
                await node.close()
            except BaseException as error:
                errors.append({"owner": name, "phase": "node-close", "error": str(error)[:1000]})
            try:
                raw = bytes(node.stderr)
                require(len(raw) <= 69632, "RECIPROCAL_STDERR_BOUND")
                with (self.out/(name+"-stderr.bin")).open("xb") as stream:
                    stream.write(raw)
            except BaseException as error:
                errors.append({"owner": name, "phase": "stderr-save", "error": str(error)[:1000]})
        for name, http in reversed(self.providers):
            try:
                await http.stop()
            except BaseException as error:
                errors.append({"owner": name, "phase": "http-stop", "error": str(error)[:1000]})
        for name, store in reversed(self.stores):
            try:
                store.close()
            except BaseException as error:
                errors.append({"owner": name, "phase": "store-close", "error": str(error)[:1000]})
        self.report.update(cleanup_errors=errors, phases=self.phases,
            node_reports={name: node.report() for name, node in self.nodes},
            provider_reports={name: http.status() for name, http in self.providers},
            frontier_reports={name: owner.report() for name, owner in self.frontiers},
            receiver_reports={name: owner.report() for name, owner in self.receivers},
            client_reports={name: client.report() for name, client in self.clients},
            preparation_report=None if self.preparation is None else self.preparation.report())
        require(not errors, "RECIPROCAL_CLEANUP_FAILURE")


def author_material(config, header):
    """Trusted setup strips proof-bearing retained inputs before author use."""
    inputs = config["inputs"]
    foundation = read_pin(inputs["foundation"])
    base = C.parse_json(read_pin(inputs["base_bundle"]))
    first = C.parse_json(read_pin(inputs["first_input"]))
    first_journal = read_pin(inputs["first_journal"])
    require(C.module_id(base["spec"]) == BASE and C.module_id(first["local_spec"]) == FIRST
            and journal(first_journal)["summary"] == C.summarize(first["local_spec"]),
            "RECIPROCAL_BASE_FIRST_REFERENCE")
    members = {}
    for item in config["aggregate"]["members"]:
        fields(item, ("journal", "index", "siblings"))
        exact = exact_bytes(item["journal"], 184)
        require(type(item["siblings"]) is list and len(item["siblings"]) <= B.MAX_SIBLINGS,
                "RECIPROCAL_MEMBER_PATH")
        siblings = [exact_bytes(value, 32) for value in item["siblings"]]
        uint(item["index"], B.MAX_MEMBERS-1)
        B.bind_member(header, exact, item["index"], siblings, adopted_image=config["aggregate"]["image"])
        decoded = journal(exact)
        module = decoded["module"]
        require(module in (BASE, FIRST) and module not in members, "RECIPROCAL_SELECTED_MEMBER_SET")
        require(decoded["rank"] == (0 if module == BASE else 1)
                and decoded["summary"] == C.summarize(base["spec"] if module == BASE else first["local_spec"]),
                "RECIPROCAL_EXACT_MEMBER_MATHEMATICS")
        if module == FIRST:
            require(exact == first_journal, "RECIPROCAL_EXACT_FIRST_J")
        members[module] = {"journal": exact, "index": item["index"], "siblings": siblings}
    require(set(members) == {BASE, FIRST}, "RECIPROCAL_TWO_SELECTED_MEMBERS")
    roots = C.parse_json(read_pin(inputs["roots"]))
    require(roots == [[["s", "OwnerV5"], ["s", "fold_map_twice_received"]]], "RECIPROCAL_RETAINED_ROOT")
    require(len(first["local_spec"]["groups"]) == 1, "RECIPROCAL_FIRST_SINGLE_INTERFACE")
    material = {BASE: {"openings": base["openings"], "bodies": base["bodies"]},
                FIRST: {"openings": [C.group_opening(first["local_spec"], 0)], "bodies": []},
                "foundation": foundation, "source": read_pin(inputs["source"]).decode("utf-8"), "roots": roots}
    return material, members


async def operation(c):
    aggregate = c.cfg["aggregate"]
    header = read_pin(aggregate["header"], B.HEADER_BYTES)
    B.decode_header(header, adopted_image=c.aggregate_image)
    receipt = read_pin(aggregate["receipt"], 8*MIB)
    material, members = author_material(c.cfg, header)
    raw = c.author(material, receipt, header, members)
    # Reference SECOND is read only after the real author operation has closed.
    claims, frontiers, witnesses, census = parse_packet(raw, Envelope(), aggregate_image=c.aggregate_image)
    require(len(claims) == 1 and claims[0] == (1, header, receipt)
            and len(frontiers) == 2 and len(witnesses) == 1
            and {value[1] for value in frontiers} == {value["journal"] for value in members.values()},
            "RECIPROCAL_OUTGOING_A_ONLY_SHAPE")
    reference = C.parse_json(read_pin(c.cfg["inputs"]["reference_packet"]))
    witness = C.parse_json(witnesses[0][0])
    require(witness == reference["deltas"][-1] and len(witness["rows"]) == 1009
            and witness["rank"] == 2 and C.module_id(witness["local_spec"]) == SECOND
            and set(witnesses[0][1]) == {value["journal"] for value in members.values()},
            "RECIPROCAL_COMPLETE_SECOND_REFERENCE_COMPATIBILITY")
    c.report["reference_comparison"] = {"complete_witness_equal": True, "rows": 1009,
        "new_witness_sha256": sha(witnesses[0][0]), "packet_census": census,
        "reference_packet_sha256": c.cfg["inputs"]["reference_packet"]["sha256"],
        "reference_is_admission_authority": False, "reference_was_supplied_to_author": False,
        "new_theorem_discovery_claim": False}
    origin_modules, origin_packets = c.stores_for("origin")
    origin_index = c.index_for("origin")
    origin_packets.put(SECOND, raw)
    unused_groups, unused_bodies, semantics = semantic_material(raw, c.aggregate_image, origin_modules, c.remaining)
    c.report["origin_semantics"] = semantics
    target = witness["local_spec"]
    published = 0
    for index, group in enumerate(target["groups"]):
        opening = C.group_opening(target, index)
        for declaration in group["declarations"]:
            origin_index.admit(c.adapter.encode_opening(SECOND, declaration["name"], opening))
            published += 1
    require(published > 0, "RECIPROCAL_TARGET_EXPORTS")
    bootstrap_node = c.node("bootstrap", "reader")
    ready = await c.start_node("bootstrap", bootstrap_node, joined=False)
    bootstrap = f'/ip4/127.0.0.1/tcp/{c.cfg["ports"]["bootstrap"]}/p2p/{P.peer_id(ready["peer_id"])}'
    origin_http, origin_node = await c.provider("origin", origin_index, origin_modules, origin_packets, bootstrap)
    modules1, packets1, export1, module1, entry1 = await c.reader("reader1", bootstrap)
    require(module1 == SECOND and packets1.get(entry1["packet_sha256"], entry1["packet_bytes"]) == raw,
            "RECIPROCAL_FIRST_RETURNED_PACKET")
    replica_index = c.index_for("replica")
    replica_index.admit(export1)
    await c.provider("replica", replica_index, modules1, packets1, bootstrap)
    await origin_http.stop()
    await c.stop_node(origin_node)
    origin_index.close()
    origin_modules.close()
    origin_packets.close()
    require(origin_http.server is None and not origin_http.tasks and origin_node.closed
            and all(owner.report()["closed"] for unused, owner in c.frontiers)
            and all(owner.report()["closed"] for unused, owner in c.receivers),
            "RECIPROCAL_ORIGIN_AND_OLD_AUTHORITY_CLOSED")
    c.report["origin_offline_before_second_retrieval"] = True
    modules2, packets2, export2, module2, entry2 = await c.reader("reader2", bootstrap, final_context=True)
    require(module2 == module1 == SECOND and entry2 == entry1 and export2 == export1
            and packets2.get(entry2["packet_sha256"], entry2["packet_bytes"]) == raw,
            "RECIPROCAL_FRESH_SURVIVOR_REACQUISITION")
    require(len(c.frontiers) == 3 and sum(owner.report()["attempts"] for unused, owner in c.frontiers) == 3
            and len(c.receivers) == 2 and sum(owner.report()["attempts"] for unused, owner in c.receivers) == 2
            and c.report["author_calls"] == 1 and c.preparation.report()["calls"] == 1,
            "RECIPROCAL_WHOLE_OPERATION_CALL_COUNTS")
    c.report.update(actual_A_verifications=3, actual_native_checks=2, actual_I_verifications=0,
        guest_calls=0, proof_calls=0, target_module=SECOND, packet_sha256=sha(raw), packet_bytes=len(raw),
        published_origin_exports=published, replica_data_origin="READER1_ACQUIRED_PACKET_SEMANTICS_AND_EXPORT_ONLY",
        second_reader_timing="START_ROUTE_SEARCH_AND_ALL_ACQUISITION_AFTER_ORIGIN_LOSS",
        count_scope="WHOLE_OPERATION_DISTINCT_FROM_EACH_READER_ONE_A_ONE_NATIVE")
    c.census()


def main():
    started, cpu_started = time.monotonic(), time.process_time()
    require(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
            and sys.dont_write_bytecode and not sys.flags.optimize, "RECIPROCAL_OWNER_INVOCATION")
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--config-sha256", required=True)
    args = parser.parse_args()
    digest(args.config_sha256)
    path = ordinary(Path(args.config))
    raw = read_pin({"path": str(path), "bytes": path.stat().st_size, "sha256": args.config_sha256}, MIB)
    config = parse(raw)
    fields(config, CONFIG)
    require(config["schema"] == SCHEMA, "RECIPROCAL_CONFIG_SCHEMA")
    fields(config["inputs"], INPUT_PINS)
    for name, (size, expected) in INPUT_PINS.items():
        row = config["inputs"][name]
        pin_fields(row)
        require(row["bytes"] == size and row["sha256"] == expected, "RECIPROCAL_RETAINED_INPUT_SELECTION:"+name)
    fields(config["limits"], LIMITS)
    limits = config["limits"]
    # The existing outer launcher allows <=600 worker wall seconds. Root must
    # leave cleanup/finalization headroom there; this file invents no outer fields.
    uint(limits["wall_seconds"], 540, 60)
    uint(limits["controller_cpu_seconds"], 360, 1)
    uint(limits["output_bytes"], 512*MIB, 128*MIB)
    uint(limits["output_entries"], 8192, 256)
    deadline = started+limits["wall_seconds"]
    fields(limits["call"], ("native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds", "memory_mib"))
    for key in ("native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds"):
        uint(limits["call"][key], 600, 1)
    uint(limits["call"]["memory_mib"], 4096, 64)
    fields(limits["author"], ("cpu_seconds", "wall_seconds", "memory_mib"))
    uint(limits["author"]["cpu_seconds"], 1200, 1)
    uint(limits["author"]["wall_seconds"], 600, 1)
    uint(limits["author"]["memory_mib"], 4096, 64)
    reserved = limits["call"]["receipt_cpu_seconds"]+limits["call"]["native_cpu_seconds"]
    require(reserved <= 600 and limits["acquisition"]["verify_attempts"] == 1
            and limits["acquisition"]["worker_cpu_seconds"] == reserved, "RECIPROCAL_SINGLE_READER_RESERVATION")
    require(limits["location"]["route_operations"] == 2
            and limits["location"]["routing_events"] >= 2 and limits["location"]["routing_peer_slots"] >= 2
            and limits["location"]["descriptor_requests"] >= 2, "RECIPROCAL_BOUNDED_EXISTING_ROUTE_GRANT")
    uint(limits["offer_bytes"], MIB, 1024)
    require(limits["packet_store"]["packet_bytes"] <= 16*MIB
            and limits["acquisition"]["verification_input_bytes"] >= limits["packet_store"]["packet_bytes"],
            "RECIPROCAL_PACKET_CEILING")
    fields(config["ports"], PORTS)
    for port in config["ports"].values():
        uint(port, 65535, 1024)
    require(len(set(config["ports"].values())) == len(PORTS), "RECIPROCAL_DISTINCT_PORTS")
    fields(config["aggregate"], ("image", "receipt", "header", "members", "executable", "supervisor_manifest"))
    aggregate = config["aggregate"]
    B._adopted_image(aggregate["image"])
    require(type(aggregate["members"]) is list and len(aggregate["members"]) == 2,
            "RECIPROCAL_AGGREGATE_MEMBER_COUNT")
    require(type(config["lineage"]) is list and 1 <= len(config["lineage"]) <= 16, "RECIPROCAL_LINEAGE_BOUND")
    profile = parse(read_pin(config["preparation_profile"]))
    producer = profile["producer"]
    require((producer["image_id"], producer["foundation"], producer["policy"])
            == (IMAGE, FOUNDATION, POLICY), "RECIPROCAL_FIXED_I_PREPARATION_PROFILE")
    allowance = config["owner_allowance"]
    fields(allowance, ("allowance_id", "operations", "worker_cpu_seconds", "controller_cpu_seconds",
                      "wall_seconds", "output_bytes", "output_entries"))
    digest(allowance["allowance_id"])
    require(allowance["operations"] == 1 and type(allowance["operations"]) is int,
            "RECIPROCAL_ONE_AUTHOR_ALLOWANCE")
    require(allowance["worker_cpu_seconds"] == limits["author"]["cpu_seconds"], "RECIPROCAL_AUTHOR_RESERVATION")
    runtime_rows = config["runtime_pins"]
    require(type(runtime_rows) is list and 1 <= len(runtime_rows) <= 128, "RECIPROCAL_RUNTIME_PIN_COUNT")
    runtime = {}
    for row in runtime_rows:
        candidate = ordinary(pin_fields(row))
        require(str(candidate) not in runtime and file_pin(candidate) == row, "RECIPROCAL_RUNTIME_PIN")
        runtime[str(candidate)] = {key: row[key] for key in ("bytes", "sha256")}
    require(aggregate["executable"] in runtime_rows and config["native_executable"] in runtime_rows
            and file_pin(Path(__file__).resolve()) in profile["source_pins"], "RECIPROCAL_EXECUTABLE_SOURCE_PINS")
    source_closure(runtime)
    loc = config["location"]
    fields(loc, ("source_directory", "source_pins", "role_pins", "entry_source", "ready_source"))
    require(set(loc["source_pins"]) == SOURCE_NAMES and set(loc["role_pins"]) == ROLE_NAMES,
            "RECIPROCAL_LOCATION_SOURCE_MAP")
    require(pin_fields(loc["entry_source"]) == V5/"location/node_entry_services_available.mjs"
            and sha(read_pin(loc["entry_source"], 2*MIB)) == loc["role_pins"]["node_entry_services.mjs"],
            "RECIPROCAL_AVAILABLE_ENTRY_ALIAS")
    require(pin_fields(loc["ready_source"]) == V5/"location/maintained_roles_ready.mjs"
            and sha(read_pin(loc["ready_source"], 2*MIB)) == loc["role_pins"]["maintained_roles.mjs"],
            "RECIPROCAL_READY_ROLE_ALIAS")
    adoption = AdoptedLocationRuntime(Path(loc["source_directory"]), loc["source_pins"])
    output = Path(config["output_directory"])
    require(output.is_absolute() and output.resolve() == output and output.parent.is_dir()
            and not output.exists() and output.is_relative_to(ROOT/"experiments/v5-local-checks"),
            "RECIPROCAL_FRESH_OUTPUT")
    ordinary(output.parent, directory=True)
    input_rows = [*config["inputs"].values(), *config["lineage"], config["preparation_profile"],
        aggregate["receipt"], aggregate["header"], aggregate["supervisor_manifest"],
        loc["entry_source"], loc["ready_source"]]
    profile_rows = [profile["image"], profile["worker"], profile["native_executable"], *profile["source_pins"],
        *profile["lean_runtime_pins"], producer["host"], producer["python"], producer["python_dll"],
        producer["supervisor_manifest"], *producer["source_pins"], *producer["runtime_pins"]]
    protected = [path, V5, SOURCE_V5, Path(loc["source_directory"]), Path(profile["lean_root"]),
                 Path(producer["supervisor_manifest"]["path"]).parent,
                 Path(aggregate["supervisor_manifest"]["path"]).parent]
    protected.extend(pin_fields(row) for row in input_rows+profile_rows+runtime_rows)
    require(all(not output.is_relative_to(item) and not item.is_relative_to(output) for item in protected),
            "RECIPROCAL_OUTPUT_OVERLAP")
    require(time.monotonic() < deadline, "RECIPROCAL_PREFLIGHT_DEADLINE")
    output.mkdir()
    save(output/"configuration.json", config)
    report = {"schema": SCHEMA, "status": "FAIL", "configuration_sha256": args.config_sha256,
        "lineage": config["lineage"], "input_pins": config["inputs"], "author_calls": 0,
        "independent_host_evidence": False, "global_complete": False,
        "origin_offline_before_second_retrieval": False, "global_growth_claim": False,
        "authority": "LOCAL_OPERATION_EVIDENCE_NOT_TRANSFERABLE_MATHEMATICAL_AUTHORITY",
        "isolation_scope": "TRUSTED_SINGLE_PROCESS_CONSUMER_INPUT_SEPARATION_NOT_HOSTILE_SANDBOX",
        "cost_scope": "OWNER_LIFETIME_CPU_NESTED_RESERVATIONS_NONADDITIVE_OUTER_JOB_AND_WRAPPER_SEPARATE"}
    campaign = Campaign(config, output, deadline, cpu_started, report, runtime, profile, adoption)

    async def run():
        try:
            for row in config["lineage"]:
                read_pin(row)
                campaign.remaining()
            await operation(campaign)
        except BaseException as error:
            report["operation_error"] = {"type": type(error).__name__, "message": str(error)[:2000]}
            raise
        finally:
            await campaign.cleanup()

    try:
        asyncio.run(run())
        require(all(node.process is not None and node.process.returncode == 0 and node.closed
                    and not node.channel_failed and not node.forced_termination
                    and node.pre is not None and node.post is not None and node.role_pre == node.role_post
                    for unused, node in campaign.nodes), "RECIPROCAL_PINNED_NODE_EXITS")
        require(all(http.server is None and not http.tasks for unused, http in campaign.providers),
                "RECIPROCAL_HTTP_CLOSURE")
        for name in ("bootstrap", "reader1", "reader2"):
            dbpath = output/(name+"-state")/"metadata.sqlite"
            db = sqlite3.connect(dbpath.as_uri()+"?mode=ro&immutable=1", uri=True)
            try:
                counts = [db.execute("SELECT count(*) FROM kv WHERE k LIKE ?", (key,)).fetchone()[0]
                          for key in ("/application/published/%", "/application/provider-intent/%")]
            finally:
                db.close()
            require(counts == [0, 0], "RECIPROCAL_NEUTRAL_ROLE:"+name)
        # Required source/runtime integrity, not a second mathematical campaign.
        for row in runtime_rows+input_rows:
            require(file_pin(pin_fields(row)) == row, "RECIPROCAL_FINAL_SELECTED_PIN")
            campaign.remaining()
        report["loaded_source_paths"] = source_closure(runtime)
        require(path.read_bytes() == raw, "RECIPROCAL_CONFIG_CHANGED")
        report["output_census_before_result"] = campaign.census()
        report["status"] = "PASS_REAL_A_ORDINARY_EXTENSION_PUBLIC_TWO_COLD_READERS_AND_SURVIVING_REPLICA"
    except BaseException as error:
        report["error"] = {"type": type(error).__name__, "message": str(error)[:2000]}
        raise
    finally:
        report["controller_cpu_seconds"] = time.process_time()-cpu_started
        report["wall_seconds"] = time.monotonic()-started
        try:
            save(output/"RESULT.json", report)
            campaign.census()
        except BaseException as error:
            report.update(status="FAIL", finalization_error={"type": type(error).__name__, "message": str(error)[:2000]})
            save(output/"FINALIZATION-FAILED.json", report)
            raise


if __name__ == "__main__":
    main()

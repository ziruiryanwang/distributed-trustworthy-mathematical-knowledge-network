"""Two genuine cold receivers; actual feature location, custody and origin loss.

Root selects the complete retained packet and every finite input/runtime grant.
No reauthoring, new proof, mock verifier, private holder list or new DHT protocol.
The second reader starts before origin loss to capture a genuine stale result;
its alternative routing, acquisition and admission all happen after origin loss.
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
from admission.verifier import ReceiptVerifier
from custody.module_store import ModuleStore, permitted_hashes, BODY_SCHEMA
from delta.authoring import DeltaImportSession, prepare_delta_context
from delta.custody import PacketStore, public_profile
from delta.packet import Envelope, parse_packet
from delta.receiver import DeltaVerifier
from delta.transport import CompositeProvider, DeltaLocatedHandoff, DeltaAcquisition
from discovery import formal_features as F
from discovery.discovery_store import Store
from discovery.module_export_adapter import ModuleExportAdapter, compile_query
from location import protocol as P
from location.available_descriptor import descriptor
from location.controller import AdoptedLocationRuntime, SOURCE_NAMES
from location.controller_services import ServiceLocationProcess, ROLE_NAMES
from modules import codec as C
from production.producer import encoded, parse, fields, require, uint, digest, pin_fields, file_pin, MIB
from transport.receipt_client import AcquisitionBudget

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
V5 = ROOT/"software/v5"
SOURCE_V5 = Path(__file__).resolve().parents[1]
SCHEMA = "DMKN_V5_ACTUAL_DELTA_NETWORK_V1"
BASE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
IMAGE = "9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e"
FOUNDATION = "d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481"
POLICY = "5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377"
PORTS = ("bootstrap", "origin_location", "replica_location", "reader1", "reader2", "origin_http", "replica_http")
CONFIG = ("schema", "packet", "lineage", "preparation_profile", "foundation", "native_executable",
          "runtime_pins", "location", "ports", "output_directory", "limits")
LIMITS = ("wall_seconds", "call", "node", "location", "search", "candidate", "acquisition",
          "module_store", "packet_store", "index_store", "provider", "offer_bytes")


def sha(raw): return hashlib.sha256(raw).hexdigest()


def read_pin(row, maximum=16*MIB):
    path = pin_fields(row, maximum)
    require(path.resolve() == path and path.is_file() and file_pin(path) == row, "NETWORK_INPUT_PIN")
    with path.open("rb") as stream: raw = stream.read(maximum+1)
    require(len(raw) == row["bytes"] and sha(raw) == row["sha256"], "NETWORK_READ_PIN")
    return raw


def save(path, value):
    raw = encoded(value)
    require(len(raw) <= 4*MIB, "NETWORK_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def node_config(role, state, namespace, port, policy, limits, endpoint=None, bootstrap=()):
    return {"schema":"DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", "role":role,
        "state":str(state), "namespace":namespace, "egress":policy,
        "listen":[f"/ip4/127.0.0.1/tcp/{port}"], "announce":[], "bootstrap":list(bootstrap),
        "endpoints":[] if role == "reader" else [endpoint], "limits":dict(limits)}


def source_closure(runtime):
    """Only actual loaded project Python sources, never saved-report authority."""
    paths = {Path(__file__).resolve()}
    for module in tuple(sys.modules.values()):
        value = getattr(module, "__file__", None)
        if value is None: continue
        path = Path(value).resolve()
        parts = path.parts
        project_v5 = any(parts[i:i+2] == ("software","v5") for i in range(len(parts)-1))
        if path.is_relative_to(ROOT) and path.suffix == ".py" and project_v5:
            # A snapshot must not silently borrow canonical/other snapshot code.
            require(path.is_relative_to(SOURCE_V5), "NETWORK_FOREIGN_PROJECT_SOURCE_IMPORT")
            paths.add(path)
    require(paths <= {Path(path) for path in runtime}, "NETWORK_LOADED_SOURCE_NOT_PINNED")
    return sorted(str(path) for path in paths)


def semantic_material(raw, store, check):
    """Recover selected committed semantics from the acquired packet itself.

    This is structural custody only; member authority is checked separately by
    a live DeltaImportSession. Theorem proofs remain in the checking packet.
    """
    unused_frontiers,witnesses,census = parse_packet(raw,Envelope())
    groups, available = {}, {}
    def opening(owner,value):
        C.verify_group_opening(owner,value)
        key = owner,value["index"]
        require(key not in groups or C.canonical(groups[key]) == C.canonical(value),
                "NETWORK_SEMANTIC_GROUP_CONFLICT")
        groups[key] = value
    for encoded_witness,unused_parents,unused_summary,unused_rank in witnesses:
        witness = C.parse_json(encoded_witness); spec = witness["local_spec"]
        owner = C.module_id(spec)
        for index in range(len(spec["groups"])): opening(owner,C.group_opening(spec,index))
        for parent in witness["parents"]:
            owner = journal(bytes(parent["journal"]))["module"]
            for value in parent["openings"]: opening(owner,value)
        for body in witness["bodies"]:
            key = body["universes"],body["digest"]
            require(C.body_id(body["expression"],body["universes"]) == body["digest"],
                    "NETWORK_SEMANTIC_BODY_DIGEST")
            require(key not in available or C.canonical(available[key]) == C.canonical(body["expression"]),
                    "NETWORK_SEMANTIC_BODY_CONFLICT")
            available[key] = body["expression"]
    bodies,missing = {},[]
    for (owner,index),value in sorted(groups.items()):
        check(); store.put_group(owner,value,before_commit=check)
        for declaration in value["group"]["declarations"]:
            held,unused = store.get_group(owner,declaration["name"],index)
            require(held == value,"NETWORK_SEMANTIC_GROUP_READBACK")
            for digest_value in sorted(permitted_hashes(declaration)):
                key = declaration["universes"],digest_value
                if key not in available:
                    # Opaque values need not be unfolded. The context builder
                    # decides which missing bodies are actual semantic demands.
                    missing.append({"module":owner,"name":declaration["name"],
                                    "universes":key[0],"digest":key[1]})
                    continue
                response = {"schema":BODY_SCHEMA,"module_id":owner,"relative_name":declaration["name"],
                    "universes":key[0],"body_hash":key[1],"expression":available[key]}
                store.put_body(owner,declaration["name"],response,before_commit=check)
                require(store.get_body(owner,declaration["name"],*key) == response,
                        "NETWORK_SEMANTIC_BODY_READBACK")
                bodies.setdefault((owner,*key),response)
    check()
    return groups,bodies,{"packet_census":census,"groups":len(groups),"bodies":len(bodies),
        "unavailable_committed_values":missing,"origin":"ACQUIRED_PACKET_ONLY",
        "all_future_bodies_covered":False,"mathematical_acceptance":False}


class Campaign:
    def __init__(self, config, output, deadline, report, runtime, producer, adoption, role_pins):
        self.cfg = {key:config[key] for key in ("ports","native_executable","foundation")}
        self.out, self.deadline, self.report = output, deadline, report
        self.limits, self.runtime, self.producer = config["limits"], runtime, producer
        self.adoption, self.role_pins = adoption, role_pins
        self.adapter = ModuleExportAdapter(C, FOUNDATION, POLICY)
        self.profile = public_profile(IMAGE, FOUNDATION, POLICY)
        self.features = compile_query(self.adapter.namespace, [
            {"tag":"declaration-kind", "value":"theorem"},
            {"tag":"result-head", "head":{"tag":"const", "symbol":{"kind":"foundation-name",
                "name_hash":C.hash_value("foundation-symbol", [["s","Eq"]])}}},
            {"tag":"type-symbol", "symbol":{"kind":"export", "export_id":C.export_id(BASE,
                [["s","CommonsV5"],["s","fold"]])}}])
        self.policy_config = {"schema":"DMKN_V5_OWNER_EGRESS_V1", "mode":"loopback-test", "public_ports":[],
            "test_endpoints":[{"host":"127.0.0.1", "port":port} for port in sorted(config["ports"].values())]}
        self.policy = P.OwnerEgressPolicy(self.policy_config)
        self.nodes, self.providers, self.stores, self.clients, self.frontiers, self.receivers = [], [], [], [], [], []
        self.phases = []; self.sessions = []

    def remaining(self):
        left = math.floor(self.deadline-time.monotonic())
        require(left >= 1, "NETWORK_ORIGINAL_DEADLINE")
        return left

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
        value = Store(self.out/(name+"-index"), self.adapter, self.limits["index_store"], create=True)
        self.stores.append((name+"-index", value))
        return value

    def node(self, name, role, bootstrap=(), endpoint=None):
        self.remaining()
        cfg = node_config(role, self.out/(name+"-state"), self.adapter.namespace,
            self.cfg["ports"][name], self.policy_config, self.limits["node"], endpoint, bootstrap)
        value = ServiceLocationProcess(self.adoption, self.role_pins, cfg,
                                       self.out/(name+"-controller"), deadline=self.deadline)
        self.nodes.append((name,value))
        return value

    async def start_node(self, name, value, joined=True):
        ready = await value.start()
        require(ready["role"] == value.config["role"], "NETWORK_NODE_ROLE")
        if joined:
            require(len(ready["joins"]) == 1 and ready["joins"][0]["status"] == "CONNECTED",
                    "NETWORK_NEUTRAL_BOOTSTRAP_JOIN")
        save(self.out/(name+"-ready.json"), ready)
        return ready

    async def provider(self, name, index, modules, packets, bootstrap):
        self.remaining()
        http = CompositeProvider(index=index, custody=modules, packets=packets, **self.limits["provider"])
        self.providers.append((name,http))
        endpoint = await http.start(host="127.0.0.1", port=self.cfg["ports"][name+"_http"])
        ep = {"host":endpoint.host,"port":endpoint.port,"tls":endpoint.tls,"server_name":endpoint.server_name}
        channel = self.node(name+"_location", "index-provider", [bootstrap], ep)
        await self.start_node(name+"_location", channel)
        published = await channel.command("publish", {"features":self.features,"stripe":0})
        require(published["status"] == "ADVERTISED_HINT"
                and published["route_key"] == P.route_key(self.adapter.namespace,self.features,0),
                "NETWORK_ACTUAL_FEATURE_ADVERTISEMENT")
        save(self.out/(name+"-publication.json"),published)
        return http,channel

    async def stop_node(self, value):
        if value.closed: return
        await value.command("stop", {})
        await value.close()
        require(value.process is not None and value.process.returncode == 0
                and not value.channel_failed and not value.forced_termination,
                "NETWORK_GRACEFUL_NODE_EXIT")

    def cold(self, name):
        self.remaining(); limits, producer = self.limits["call"], self.producer
        receipt_runtime = {row["path"]:{key:row[key] for key in ("bytes","sha256")}
            for row in (producer["host"],producer["python"],producer["python_dll"],*producer["runtime_pins"])}
        frontier = ReceiptVerifier(supervisor_manifest=producer["supervisor_manifest"]["path"],
            supervisor_manifest_sha256=producer["supervisor_manifest"]["sha256"],
            executable=producer["host"]["path"],runtime_pins=receipt_runtime,
            image_id=IMAGE,foundation=FOUNDATION,policy=POLICY,operations=1,submitted_bytes=8*MIB,
            reserved_cpu_seconds=limits["receipt_cpu_seconds"],wall_seconds=self.remaining())
        self.frontiers.append((name,frontier))
        receiver = DeltaVerifier(frontier,native_executable=self.cfg["native_executable"]["path"],
            runtime_pins=self.runtime,output_directory=self.out/(name+"-admission"),
            operations=1,submitted_bytes=self.limits["packet_store"]["packet_bytes"],
            reserved_cpu_seconds=limits["receipt_cpu_seconds"]+2*limits["native_cpu_seconds"],
            controller_cpu_seconds=120,wall_seconds=self.remaining(),output_bytes=64*MIB,output_entries=256)
        self.receivers.append((name,receiver))
        return frontier,receiver

    async def reader(self, name, bootstrap, *, transition=None):
        """No packet/target/provider ID enters routing or candidate selection.

        The harness callback changes external service availability only. Its
        arguments and return value contain no target/contact/authority data.
        This trusted same-process composition is not adversarial process isolation.
        """
        phase = {"name":name,"routes":[],"descriptors":[],"searches":[],"admitted":False,
                 "initial_contacts":0,"known_target_ids":[],"known_http_endpoints":[],
                 "query_specs_origin":"LOCAL_BASE_VOCABULARY_THEOREM_EQ_FOLD",
                 "bootstrap_scope":"NEUTRAL_READER_ROUTER_WITH_NO_PUBLICATION_OR_CUSTODY"}
        self.phases.append(phase)
        modules,packets = self.stores_for(name)
        budget = AcquisitionBudget(self.deadline,self.limits["acquisition"])
        channel = self.node(name,"reader",[bootstrap])
        handoff = DeltaLocatedHandoff(channel,self.adapter,self.features,self.policy,budget,
                                      self.limits["location"],self.limits["search"])
        phase["prestart_budget"] = budget.report()
        require(handoff.location.report()["workflow"]["contacts"] == 0,
                "NETWORK_FRESH_READER_NO_CONTACTS")
        await self.start_node(name,channel)
        require(channel.config["endpoints"] == [],"NETWORK_READER_NO_PROVIDER_ROLE")
        attempted, contacts = set(), []
        route_count = 2 if transition is not None else 1
        unavailable = 0
        for route_number in range(route_count):
            located = await handoff.location.route(self.features,
                event_cap=self.limits["location"]["routing_events"]//route_count,
                peer_cap=min(self.limits["node"]["provider_limit"],
                             self.limits["location"]["routing_peer_slots"]//route_count))
            phase["routes"].append(located)
            if route_number == 0 and transition is not None:
                require(located["peers"],"NETWORK_REAL_STALE_ROUTE_REQUIRED")
                phase["transition_before"] = {"time":time.monotonic(),"acquisition_attempts":0,
                                               "receipt_attempts":0,"native_attempts":0}
                await transition()
                phase["transition_after"] = {"time":time.monotonic(),"origin_closed":True}
            for peer in located["peers"]:
                # Skip only THIS reader's already attempted public route result,
                # never an expected private origin/replica ID.
                if peer in attempted: continue
                attempted.add(peer)
                reply = await descriptor(handoff.location,peer,located["route_key"],
                                         max_bytes=4096,max_age_ms=60000)
                phase["descriptors"].append({"route":route_number,"peer":peer,"reply":reply})
                if reply["status"] == "DESCRIPTOR_UNAVAILABLE":
                    unavailable += 1
                else:
                    require(reply["status"] == "ADOPTED_ADVISORY_CONTACTS",
                            "NETWORK_DESCRIPTOR_OUTCOME")
                    contacts.extend(item for item in reply["contacts"] if item not in contacts)
            if route_number == 0 and transition is not None:
                require(unavailable > 0 and not contacts and not channel.channel_failed,
                        "NETWORK_REAL_STALE_FIRST_SAME_CHANNEL")
        require(contacts,"NETWORK_NO_LOCATED_INDEX_CONTACT")
        search = handoff.begin_search()
        frontier,receiver = self.cold(name)
        client = DeltaAcquisition.from_search(handoff,self.profile,modules,packets,verifier=receiver)
        self.clients.append((name,client))
        selected = None
        for contact in contacts:
            try:
                offered = await search.offer(contact,self.limits["offer_bytes"],
                                             max_expanded_bytes=MIB,max_age_ms=60000)
                phase["searches"].append({"contact":contact,"offer":offered})
                partition = next((row for row in offered["partitions"] if row["anchor_count"] > 0),None)
                if partition is None: continue
                page = await search.candidates(contact,offered["snapshot_id"],partition["partition"],0,
                                               self.limits["candidate"])
                phase["searches"][-1]["page"] = page
                require(page["status"] == "VERIFIED_CANDIDATES" and page["mathematical_acceptance"] is False
                        and page["verified_scan_coverage"] is False,"NETWORK_CANDIDATE_ONLY")
            except Exception as error:
                # Search failures consume the original SearchSession tickets.
                # No new session or finite grant is minted for another contact.
                phase["searches"].append({"contact":contact,"failure":type(error).__name__+":"+str(error)[:1000]})
                budget.active(); continue
            if page["matches"]:
                selected = contact,page["matches"][0]
                break
        require(selected is not None,"NETWORK_NO_RETURNED_CANDIDATE")
        contact,record = selected
        resolved = await client.export(contact,record)
        module = resolved["locator"]["module_id"]
        offered = await client.offers(contact,module,max_offers=2,max_bytes=4096)
        require(offered["packets"],"NETWORK_NO_PACKET_OFFER")
        entry = offered["packets"][0]
        acquired = await client.packet(contact,module,entry)
        custody_state = client.custody_ready(resolved,entry)
        require(custody_state["census"]["frontiers"] == 1 and custody_state["census"]["deltas"] == 2,
                "NETWORK_ONE_FRONTIER_TWO_DELTA_ENDPOINT")
        admitted = client.admit(resolved,entry,**{**self.limits["call"],
            "wall_seconds":min(self.limits["call"]["wall_seconds"],self.remaining())})
        live = receiver.describe(admitted["handle"])
        require(live["module"] == module and journal(live["journal"])["rank"] == 2
                and receiver.export_packet(admitted["handle"]) == packets.get(entry["packet_sha256"],entry["packet_bytes"])
                and len(receiver.members(admitted["handle"])) == 3,"NETWORK_GENUINE_COMPLETE_ADMISSION")
        groups,bodies,semantics = semantic_material(packets.get(entry["packet_sha256"],entry["packet_bytes"]),
                                                   modules,budget.active)
        phase["semantic_custody"] = semantics
        if transition is not None:
            # Final consumer reconstructs an ordinary authoring context using
            # only its received semantics plus its independently adopted foundation.
            session = DeltaImportSession(receiver,max_handles=1,max_members=3,max_calls=4096,
                packet_bytes=self.limits["packet_store"]["packet_bytes"],data_bytes=16*MIB,
                wall_seconds=self.remaining())
            self.sessions.append((name,session)); session.use_handle(admitted["handle"])
            for (owner,index),value in sorted(groups.items()):
                representative = value["group"]["declarations"][0]["name"]
                held,unused = modules.get_group(owner,representative,index)
                session.open_group(owner,held)
            for (owner,arity,digest_value),value in sorted(bodies.items()):
                held = modules.get_body(owner,value["relative_name"],arity,digest_value)
                require(session.supply_body(owner,arity,held["expression"]) == digest_value,
                        "NETWORK_RECEIVED_IMPORT_BODY")
            context = prepare_delta_context(session,read_pin(self.cfg["foundation"]),
                                             self.cfg["foundation"]["sha256"])
            require(context["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY"
                    and context["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
                    "NETWORK_RECEIVED_NORMAL_IMPORT_CONTEXT")
            save(self.out/(name+"-authoring-context.json"),context)
            phase["normal_import_context"] = {"status":context["status"],"cost":context["cost"],
                "selection_binding":context["selection_binding"],"native_or_author_calls":0}
            session.close(); budget.active()
        phase.update(admitted=True,module=module,record=record,packet=entry,
            custody=custody_state,acquired=acquired,unavailable_descriptors=unavailable,
            journal=list(live["journal"]),selected_contact_origin="SAME_ACTUAL_NOISE_DESCRIPTOR_WORKFLOW",
            selected_candidate_origin="FIRST_ACTUAL_RETURNED_FORMAL_QUERY_MATCH",
            search_final=search.report(),location_final=handoff.location.report(),client_final=client.report())
        exported = self.adapter.encode_opening(module,resolved["locator"]["relative_name"],resolved["opening"])
        require(self.adapter.extract(exported) == record,"NETWORK_REPLICA_EXPORT_EXACT_BINDING")
        # No live receipt/delta authority is transferred to a provider or reader2.
        client.close(); frontier.close()
        phase["closed_receiver"] = receiver.report()
        phase["closed_frontier"] = frontier.report()
        await self.stop_node(channel)
        save(self.out/(name+"-result.json"),phase)
        return modules,packets,exported,module,entry

    async def cleanup(self):
        errors = []
        for name,value in reversed(self.clients+self.receivers+self.frontiers+self.sessions):
            try: value.close()
            except BaseException as error: errors.append({"owner":name,"phase":"owner-close","error":str(error)[:1000]})
        for name,node in reversed(self.nodes):
            try:
                if not node.closed and not node.channel_failed and node.process is not None and node.process.returncode is None:
                    await node.command("stop",{})
            except BaseException as error: errors.append({"owner":name,"phase":"node-stop","error":str(error)[:1000]})
            try: await node.close()
            except BaseException as error: errors.append({"owner":name,"phase":"node-close","error":str(error)[:1000]})
            try:
                raw = bytes(node.stderr); require(len(raw) <= 69632,"NETWORK_STDERR_CAP")
                with (self.out/(name+"-stderr.bin")).open("xb") as stream: stream.write(raw)
            except BaseException as error: errors.append({"owner":name,"phase":"stderr-save","error":str(error)[:1000]})
        for name,http in reversed(self.providers):
            try: await http.stop()
            except BaseException as error: errors.append({"owner":name,"phase":"http-stop","error":str(error)[:1000]})
        for name,store in reversed(self.stores):
            try: store.close()
            except BaseException as error: errors.append({"owner":name,"phase":"store-close","error":str(error)[:1000]})
        self.report.update(cleanup_errors=errors,phases=self.phases,
            node_reports={name:node.report() for name,node in self.nodes},
            provider_reports={name:http.status() for name,http in self.providers},
            frontier_reports={name:owner.report() for name,owner in self.frontiers},
            receiver_reports={name:owner.report() for name,owner in self.receivers},
            client_reports={name:client.report() for name,client in self.clients})
        require(not errors,"NETWORK_CLEANUP_FAILURE")


async def operation(campaign, packet):
    c = campaign
    parse_packet(packet,Envelope())
    parsed = C.parse_json(packet)
    require(len(parsed["frontiers"]) == 1 and len(parsed["deltas"]) == 2,"NETWORK_SELECTED_COMPLETE_PACKET_SHAPE")
    target = parsed["deltas"][-1]["local_spec"]; module = C.module_id(target)
    origin_modules,origin_packets = c.stores_for("origin")
    origin_index = c.index_for("origin")
    origin_packets.put(module,packet)
    unused_groups,unused_bodies,origin_semantics = semantic_material(packet,origin_modules,c.remaining)
    c.report["origin_selected_semantics"] = origin_semantics
    # Publish every target descriptor; no target ID is passed to either reader.
    published = 0
    for i,group in enumerate(target["groups"]):
        opening = C.group_opening(target,i)
        origin_modules.put_group(module,opening)
        for declaration in group["declarations"]:
            origin_index.admit(c.adapter.encode_opening(module,declaration["name"],opening)); published += 1
    require(published > 0,"NETWORK_TARGET_EXPORTS")
    bootstrap_node = c.node("bootstrap","reader")
    ready = await c.start_node("bootstrap",bootstrap_node,joined=False)
    bootstrap = f'/ip4/127.0.0.1/tcp/{c.cfg["ports"]["bootstrap"]}/p2p/{P.peer_id(ready["peer_id"])}'
    origin_http,origin_node = await c.provider("origin",origin_index,origin_modules,origin_packets,bootstrap)
    modules1,packets1,export1,module1,entry1 = await c.reader("reader1",bootstrap)
    # Expected retained IDs are AFTER-the-fact assertions, outside consumer code.
    require(module1 == module and packets1.get(entry1["packet_sha256"],entry1["packet_bytes"]) == packet,
            "NETWORK_FIRST_RETURNED_EXACT_RETAINED_PACKET")
    replica_index = c.index_for("replica"); replica_index.admit(export1)

    async def transition():
        await origin_http.stop()
        await c.stop_node(origin_node)
        origin_index.close(); origin_modules.close(); origin_packets.close()
        require(origin_http.server is None and not origin_http.tasks and origin_node.closed,
                "NETWORK_ORIGIN_COMPOSITE_CLOSED")
        c.report["origin_offline_before_second_retrieval"] = True
        # Only reader1's retained exact packet/group and derived formal export.
        await c.provider("replica",replica_index,modules1,packets1,bootstrap)

    modules2,packets2,export2,module2,entry2 = await c.reader("reader2",bootstrap,transition=transition)
    require(module2 == module1 == module and entry2 == entry1 and export2 == export1
            and packets2.get(entry2["packet_sha256"],entry2["packet_bytes"]) == packet,
            "NETWORK_FRESH_SURVIVOR_EXACT_REACQUISITION")
    require(sum(owner.report()["attempts"] for name,owner in c.frontiers) == 2
            and sum(owner.report()["attempts"] for name,owner in c.receivers) == 2,
            "NETWORK_TWO_COLD_ADMISSIONS_ONLY")
    c.report.update(target_module=module,retained_packet_sha256=sha(packet),retained_packet_bytes=len(packet),
        actual_crypto_verifications=2,actual_native_checks=4,author_calls=0,guest_calls=0,proof_calls=0,
        published_origin_exports=published,replica_index_origin="RECEIVED_EXACT_EXPORT_GROUP",
        second_reader_timing="START_AND_FIRST_ROUTE_BEFORE_ORIGIN_LOSS;ALTERNATIVE_ROUTE_AND_ALL_ACQUISITION_AFTER")


def main():
    started,cpu_started = time.monotonic(),time.process_time()
    require(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
            and sys.dont_write_bytecode and not sys.flags.optimize,"NETWORK_OWNER_INVOCATION")
    parser = argparse.ArgumentParser()
    parser.add_argument("--config",required=True); parser.add_argument("--config-sha256",required=True)
    args = parser.parse_args(); digest(args.config_sha256)
    path = Path(args.config)
    require(path.is_absolute() and path.resolve() == path and path.is_file(),"NETWORK_CONFIG_PATH")
    raw = read_pin({"path":str(path),"bytes":path.stat().st_size,"sha256":args.config_sha256},MIB)
    config = parse(raw); fields(config,CONFIG); require(config["schema"] == SCHEMA,"NETWORK_CONFIG_SCHEMA")
    fields(config["limits"],LIMITS); limits = config["limits"]
    uint(limits["wall_seconds"],1800,60); deadline = started+limits["wall_seconds"]
    fields(limits["call"],("native_cpu_seconds","receipt_cpu_seconds","wall_seconds","memory_mib"))
    for key in ("native_cpu_seconds","receipt_cpu_seconds","wall_seconds"): uint(limits["call"][key],600,1)
    uint(limits["call"]["memory_mib"],4096,64)
    reserved = limits["call"]["receipt_cpu_seconds"]+2*limits["call"]["native_cpu_seconds"]
    require(reserved <= 600 and limits["acquisition"]["verify_attempts"] == 1
            and limits["acquisition"]["worker_cpu_seconds"] == reserved,"NETWORK_EXACT_SINGLE_ADMISSION_GRANT")
    require(limits["location"]["route_operations"] == 2
            and limits["location"]["routing_events"] >= 2
            and limits["location"]["routing_peer_slots"] >= 2
            and limits["location"]["descriptor_requests"] >= 2,"NETWORK_TWO_ROUTE_FALLBACK_GRANT")
    uint(limits["offer_bytes"],MIB,1024)
    require(limits["packet_store"]["packet_bytes"] <= 16*MIB
            and limits["acquisition"]["verification_input_bytes"] >= limits["packet_store"]["packet_bytes"],
            "NETWORK_PACKET_CEILING")
    fields(config["ports"],PORTS)
    for port in config["ports"].values(): uint(port,65535,1024)
    require(len(set(config["ports"].values())) == len(PORTS),"NETWORK_DISTINCT_SELECTED_PORTS")
    packet = read_pin(config["packet"])
    require(type(config["lineage"]) is list and 1 <= len(config["lineage"]) <= 16,"NETWORK_LINEAGE_PIN_COUNT")
    for row in config["lineage"]: read_pin(row)
    read_pin(config["foundation"])
    preparation = parse(read_pin(config["preparation_profile"])); producer = preparation["producer"]
    require((producer["image_id"],producer["foundation"],producer["policy"]) == (IMAGE,FOUNDATION,POLICY),
            "NETWORK_CURRENT_RECEIPT_PROFILE")
    runtime_rows = config["runtime_pins"]
    require(type(runtime_rows) is list and 1 <= len(runtime_rows) <= 256,"NETWORK_RUNTIME_PINS")
    runtime = {}
    for row in runtime_rows:
        candidate = pin_fields(row)
        require(candidate.resolve() == candidate and str(candidate) not in runtime and file_pin(candidate) == row,
                "NETWORK_DISTINCT_RUNTIME_PIN")
        runtime[str(candidate)] = {key:row[key] for key in ("bytes","sha256")}
    require(config["native_executable"] in runtime_rows,"NETWORK_NATIVE_SELECTED_PIN")
    source_closure(runtime)
    loc = config["location"]; fields(loc,("source_directory","source_pins","role_pins","entry_source"))
    require(set(loc["source_pins"]) == SOURCE_NAMES and set(loc["role_pins"]) == ROLE_NAMES,
            "NETWORK_EXACT_LOCATION_SOURCE_SETS")
    source = Path(loc["source_directory"])
    entry_raw = read_pin(loc["entry_source"],2*MIB)
    require(pin_fields(loc["entry_source"]) == V5/"location/node_entry_services_available.mjs"
            and sha(entry_raw) == loc["role_pins"]["node_entry_services.mjs"],
            "NETWORK_REVIEWED_EXPLICIT_ENTRY_ALIAS")
    adoption = AdoptedLocationRuntime(source,loc["source_pins"])
    output = Path(config["output_directory"])
    require(output.is_absolute() and output.resolve() == output and output.parent.is_dir()
            and not output.exists() and output.is_relative_to(ROOT/"experiments/v5-local-checks"),
            "NETWORK_FRESH_OUTPUT")
    protected = [path,V5,SOURCE_V5,source,Path(producer["supervisor_manifest"]["path"]).parent]
    protected.extend(pin_fields(row) for row in [config["packet"],config["preparation_profile"],
        config["foundation"],loc["entry_source"],*config["lineage"],*runtime_rows,producer["host"],producer["python"],
        producer["python_dll"],*producer["runtime_pins"]])
    require(all(not output.is_relative_to(item) and not item.is_relative_to(output) for item in protected),
            "NETWORK_OUTPUT_OVERLAP")
    output.mkdir(); save(output/"configuration.json",config)
    report = {"schema":SCHEMA,"status":"FAIL","configuration_sha256":args.config_sha256,
        "lineage":config["lineage"],"packet_pin":config["packet"],"independent_host_evidence":False,
        "global_complete":False,"origin_offline_before_second_retrieval":False,
        "authority":"LOCAL_OPERATION_EVIDENCE_NOT_TRANSFERABLE_MATHEMATICAL_AUTHORITY",
        "cost_scope":"ACQUISITION_APP_BYTES_PLUS_SEPARATE_LOCATION_HTTP_OWNER_TELEMETRY_AND_ENCLOSING_JOB"}
    campaign = Campaign(config,output,deadline,report,runtime,producer,adoption,loc["role_pins"])
    async def run():
        try: await operation(campaign,packet)
        except BaseException as error:
            report["operation_error"] = {"type":type(error).__name__,"message":str(error)[:2000]}
            raise
        finally: await campaign.cleanup()
    try:
        asyncio.run(run())
        require(all(node.process is not None and node.process.returncode == 0 and node.closed
                    and not node.channel_failed and not node.forced_termination
                    and node.pre is not None and node.post is not None and node.role_pre == node.role_post
                    for name,node in campaign.nodes),"NETWORK_ALL_PINNED_NODE_EXITS")
        require(all(http.server is None and not http.tasks for name,http in campaign.providers),
                "NETWORK_ALL_HTTP_CLOSED")
        for name in ("bootstrap","reader1","reader2"):
            dbpath = output/(name+"-state")/"metadata.sqlite"
            db = sqlite3.connect(dbpath.as_uri()+"?mode=ro&immutable=1",uri=True)
            try:
                rows = [db.execute("SELECT count(*) FROM kv WHERE k LIKE ?",(key,)).fetchone()[0]
                        for key in ("/application/published/%","/application/provider-intent/%")]
            finally: db.close()
            require(rows == [0,0],"NETWORK_NEUTRAL_READER_NO_PUBLICATION:"+name)
        for row in runtime_rows: require(file_pin(pin_fields(row)) == row,"NETWORK_FINAL_RUNTIME_PIN")
        read_pin(config["packet"]); read_pin(config["preparation_profile"]); read_pin(config["foundation"])
        read_pin(loc["entry_source"],2*MIB)
        for row in config["lineage"]: read_pin(row)
        report["loaded_source_paths"] = source_closure(runtime)
        require(path.read_bytes() == raw,"NETWORK_CONFIG_CHANGED")
        campaign.remaining()
        report["status"] = "PASS_ACTUAL_FEATURE_DISCOVERY_TWO_COLD_DELTA_ADMISSIONS_AND_STALE_ORIGIN_FALLBACK"
    except BaseException as error:
        report["error"] = {"type":type(error).__name__,"message":str(error)[:2000]}
        raise
    finally:
        report["controller_cpu_seconds"] = time.process_time()-cpu_started
        report["wall_seconds"] = time.monotonic()-started
        try:
            save(output/"RESULT.json",report)
            campaign.remaining()
        except BaseException as error:
            report.update(status="FAIL",finalization_error={"type":type(error).__name__,"message":str(error)[:2000]})
            save(output/"FINALIZATION-FAILED.json",report)
            raise


if __name__ == "__main__": main()

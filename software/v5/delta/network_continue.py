"""One fresh receiving continuation from actual02's preserved reader1 custody.

The previous failed full operation remains failed. No first-reader re-admission,
Lean authoring, proof production, provider-ID preload or preserved database write.
"""
from pathlib import Path
import argparse
import asyncio
import os
import sqlite3
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from delta import network_actual02 as N
from delta import retained_custody
from location.observed_route import CENSUS
from delta.network_actual02 import (
    ROOT, V5, SOURCE_V5, LIMITS, PORTS, IMAGE, FOUNDATION, POLICY, MIB,
    read_pin, save, parse, fields, require, uint, digest, pin_fields, file_pin,
    sha, source_closure, AdoptedLocationRuntime, SOURCE_NAMES, ROLE_NAMES)

SCHEMA = "DMKN_V5_DELTA_RETAINED_CONTINUATION_V1"
CONFIG = tuple("retained_custody" if key == "packet" else key for key in N.CONFIG)


class Campaign(N.Campaign):
    """Only publication eligibility differs; all receiving authority is unchanged."""

    async def provider(self, name, index, modules, packets, bootstrap):
        self.remaining()
        http = N.CompositeProvider(index=index,custody=modules,packets=packets,**self.limits["provider"])
        self.providers.append((name,http))
        endpoint = await http.start(host="127.0.0.1",port=self.cfg["ports"][name+"_http"])
        ep = {"host":endpoint.host,"port":endpoint.port,"tls":endpoint.tls,"server_name":endpoint.server_name}
        channel = self.node(name+"_location","index-provider",[bootstrap],ep)
        await self.start_node(name+"_location",channel)
        published = await channel.command("publish",{"features":self.features,"stripe":0})
        save(self.out/(name+"-publication.json"),published)
        fields(published,("route_key","status","termination","error","census","routing_peers_before",
                          "routing_peers_after","remote_placement_confirmed","assurance",
                          "global_complete","mathematical_acceptance"))
        fields(published["census"],CENSUS)
        census = published["census"]
        for key in CENSUS[:-1]: uint(census[key],8192)
        require(all(census[key] <= census["events"] for key in CENSUS[1:-1])
                and census["add_provider_write"] <= census["peer_response"],
                "CONTINUATION_PUBLICATION_CENSUS")
        require(census["last_query_error"] is None or type(census["last_query_error"]) is str
                and len(census["last_query_error"]) <= 500,"CONTINUATION_PUBLICATION_LAST_ERROR")
        for key in ("routing_peers_before","routing_peers_after"): uint(published[key],16384)
        partial = (published["status"] == "INCOMPLETE" and published["termination"] == "QUERY_ERRORS"
                   and census["query_error"] > 0 and published["error"] is None)
        complete = (published["status"] == "HINT_DISPATCHED_UNACKNOWLEDGED"
                    and published["termination"] == "ITERATOR_EXHAUSTED"
                    and census["query_error"] == 0 and census["add_provider_write"] > 0
                    and published["error"] is None)
        no_write = (published["status"] == "INCOMPLETE"
                    and published["termination"] == "NO_PROVIDER_RECORD_WRITE"
                    and census["query_error"] == census["add_provider_write"] == 0
                    and published["error"] is None)
        # The retained Node source reports only text for caught exceptions.
        # Admit these exact local per-operation bounds, not arbitrary aborts,
        # transport/service exhaustion, authentication or IPC/channel failures.
        bounded_abort = (published["status"] == "INCOMPLETE"
                         and published["termination"] == "ABORTED_OR_FAILED"
                         and published["error"] in (
                             "TimeoutError: The operation was aborted due to timeout",
                             "Error: LOCATION_QUERY_EVENT_CAP"))
        require((partial or complete or no_write or bounded_abort)
                and published["remote_placement_confirmed"] is False
                and published["assurance"] == N.P.ASSURANCE and published["global_complete"] is False
                and published["mathematical_acceptance"] is False
                and published["route_key"] == N.P.route_key(self.adapter.namespace,self.features,0)
                and not channel.closed and not channel.channel_failed
                and channel.process is not None and channel.process.returncode is None
                and time.monotonic() < channel.deadline,
                "CONTINUATION_BOUNDED_PARTIAL_HINT_DISPATCH")
        self.remaining()
        # A write count, including zero, proves neither placement nor absence.
        # Actual route/descriptor/search decides usability under the same grant.
        return http,channel


async def operation(c, retained):
    packet,module,entry = retained["packet"],retained["module"],retained["entry"]
    origin_modules,origin_packets = c.stores_for("origin")
    origin_index = c.index_for("origin")
    exported,origin_semantics = retained_custody.populate(
        retained,origin_modules,origin_packets,c.adapter,c.remaining)
    origin_index.admit(exported)
    # Independent fresh custody instances, both derived only from actual02's
    # immutable reader1 databases. The old original producer is never opened.
    replica_modules,replica_packets = c.stores_for("replica")
    replica_index = c.index_for("replica")
    replica_export,replica_semantics = retained_custody.populate(
        retained,replica_modules,replica_packets,c.adapter,c.remaining)
    require(replica_export == exported,"CONTINUATION_EXACT_RETAINED_EXPORT")
    replica_index.admit(replica_export)
    c.report.update(origin_selected_semantics=origin_semantics,
        replica_selected_semantics=replica_semantics,
        old_origin_state_opened=False,first_recipient_repeated=False,
        preserved_database_access="READ_ONLY_IMMUTABLE_NO_SQLITE_SIDECARS")
    bootstrap_node = c.node("bootstrap","reader")
    ready = await c.start_node("bootstrap",bootstrap_node,joined=False)
    bootstrap = f'/ip4/127.0.0.1/tcp/{c.cfg["ports"]["bootstrap"]}/p2p/{N.P.peer_id(ready["peer_id"])}'
    origin_http,origin_node = await c.provider("origin",origin_index,origin_modules,origin_packets,bootstrap)

    async def transition():
        await origin_http.stop()
        await c.stop_node(origin_node)
        origin_index.close(); origin_modules.close(); origin_packets.close()
        require(origin_http.server is None and not origin_http.tasks and origin_node.closed,
                "CONTINUATION_TRANSIENT_ORIGIN_CLOSED")
        c.report["origin_offline_before_second_retrieval"] = True
        await c.provider("replica",replica_index,replica_modules,replica_packets,bootstrap)

    # The inherited reader receives only a neutral bootstrap and local formal
    # features. Exact target/packet/export assertions happen only AFTER its own
    # actual returned-candidate choice, acquisition, cold check and context.
    modules,packets,returned,received,received_entry = await c.reader(
        "reader2",bootstrap,transition=transition)
    require(received == module and received_entry == entry and returned == exported
            and packets.get(entry["packet_sha256"],entry["packet_bytes"]) == packet,
            "CONTINUATION_FRESH_RETURNED_EXACT_PACKET")
    require(len(c.frontiers) == len(c.receivers) == 1
            and sum(owner.report()["attempts"] for name,owner in c.frontiers) == 1
            and sum(owner.report()["attempts"] for name,owner in c.receivers) == 1,
            "CONTINUATION_SINGLE_COLD_ADMISSION")
    require([name for name,node in c.nodes] == ["bootstrap","origin_location","reader2","replica_location"],
            "CONTINUATION_EXACT_FOUR_NODE_LIFETIMES")
    c.report.update(target_module=module,retained_packet_sha256=sha(packet),retained_packet_bytes=len(packet),
        actual_crypto_verifications=1,actual_native_checks=2,author_calls=0,guest_calls=0,proof_calls=0,
        published_origin_exports=1,replica_index_origin="PINNED_PREVIOUS_RECIPIENT_GROUP_AND_RECORD",
        second_reader_timing="START_AND_FIRST_ROUTE_BEFORE_TRANSIENT_ORIGIN_LOSS;ALTERNATIVE_ROUTE_AND_ALL_ACQUISITION_AFTER")


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
    def active():
        require(deadline-time.monotonic() >= 1, "NETWORK_ORIGINAL_DEADLINE")
    retained = retained_custody.load(config["retained_custody"],active)
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
    loc = config["location"]; fields(loc,("source_directory","source_pins","role_pins","entry_source","ready_source"))
    require(set(loc["source_pins"]) == SOURCE_NAMES and set(loc["role_pins"]) == ROLE_NAMES,
            "NETWORK_EXACT_LOCATION_SOURCE_SETS")
    source = Path(loc["source_directory"])
    entry_raw = read_pin(loc["entry_source"],2*MIB)
    require(pin_fields(loc["entry_source"]) == V5/"location/node_entry_services_available.mjs"
            and sha(entry_raw) == loc["role_pins"]["node_entry_services.mjs"],
            "NETWORK_REVIEWED_EXPLICIT_ENTRY_ALIAS")
    ready_raw = read_pin(loc["ready_source"],2*MIB)
    require(pin_fields(loc["ready_source"]) == V5/"location/maintained_roles_ready.mjs"
            and sha(ready_raw) == loc["role_pins"]["maintained_roles.mjs"],
            "NETWORK_REVIEWED_EXPLICIT_READINESS_ALIAS")
    adoption = AdoptedLocationRuntime(source,loc["source_pins"])
    output = Path(config["output_directory"])
    require(output.is_absolute() and output.resolve() == output and output.parent.is_dir()
            and not output.exists() and output.is_relative_to(ROOT/"experiments/v5-local-checks"),
            "NETWORK_FRESH_OUTPUT")
    protected = [path,V5,SOURCE_V5,source,Path(producer["supervisor_manifest"]["path"]).parent]
    protected.extend(pin_fields(row) for row in [*config["retained_custody"].values(),config["preparation_profile"],
        config["foundation"],loc["entry_source"],loc["ready_source"],*config["lineage"],*runtime_rows,producer["host"],producer["python"],
        producer["python_dll"],*producer["runtime_pins"]])
    require(all(not output.is_relative_to(item) and not item.is_relative_to(output) for item in protected),
            "NETWORK_OUTPUT_OVERLAP")
    output.mkdir(); save(output/"configuration.json",config)
    report = {"schema":SCHEMA,"status":"FAIL","configuration_sha256":args.config_sha256,
        "lineage":config["lineage"],"retained_custody":config["retained_custody"],"independent_host_evidence":False,
        "evidence_composition":"ACTUAL02_READER1_PREFIX_PLUS_FRESH_CONTINUATION_NOT_ONE_UNINTERRUPTED_RUN",
        "global_complete":False,"origin_offline_before_second_retrieval":False,
        "authority":"LOCAL_OPERATION_EVIDENCE_NOT_TRANSFERABLE_MATHEMATICAL_AUTHORITY",
        "cost_scope":"ACQUISITION_APP_BYTES_PLUS_SEPARATE_LOCATION_HTTP_OWNER_TELEMETRY_AND_ENCLOSING_JOB"}
    campaign = Campaign(config,output,deadline,report,runtime,producer,adoption,loc["role_pins"])
    async def run():
        try: await operation(campaign,retained)
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
        for name in ("bootstrap","reader2"):
            dbpath = output/(name+"-state")/"metadata.sqlite"
            db = sqlite3.connect(dbpath.as_uri()+"?mode=ro&immutable=1",uri=True)
            try:
                rows = [db.execute("SELECT count(*) FROM kv WHERE k LIKE ?",(key,)).fetchone()[0]
                        for key in ("/application/published/%","/application/provider-intent/%")]
            finally: db.close()
            require(rows == [0,0],"NETWORK_NEUTRAL_READER_NO_PUBLICATION:"+name)
        for row in runtime_rows: require(file_pin(pin_fields(row)) == row,"NETWORK_FINAL_RUNTIME_PIN")
        retained_custody.pins(config["retained_custody"]); read_pin(config["preparation_profile"]); read_pin(config["foundation"])
        read_pin(loc["entry_source"],2*MIB); read_pin(loc["ready_source"],2*MIB)
        for row in config["lineage"]: read_pin(row)
        report["loaded_source_paths"] = source_closure(runtime)
        require(path.read_bytes() == raw,"NETWORK_CONFIG_CHANGED")
        campaign.remaining()
        report["status"] = "PASS_RETAINED_RECIPIENT_CUSTODY_FRESH_COLD_ADMISSION_AND_ACTUAL_STALE_PROVIDER_FALLBACK"
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

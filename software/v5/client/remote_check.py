"""One proof-production-free integration of ordinary service and reader entries.

Retained genuine mathematical bytes are inputs, not acceptance evidence.
Fresh same-call receipt/native checking must establish the reader's authority.
"""
import asyncio
from copy import deepcopy
from dataclasses import replace
import json
import time
from types import MappingProxyType

from client import remote_reader, serve_workspace
from client.runtime import read_pin
from client.workspace_validated import Workspace
from discovery import formal_features as F
from mixed_claims.packet import Envelope, parse_packet
from modules import codec as C

MIB = 1024**2


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     allow_nan=False).encode("utf-8")
    F.need(len(raw) <= 2*MIB, "REMOTE_CHECK_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


async def run(context):
    params = deepcopy(dict(context.parameters))
    F.fields(params, {"schema", "packet", "reader", "service_limits", "export_name"})
    F.need(params["schema"] == "DMKN_V5_REMOTE_CHECK_V1", "REMOTE_CHECK_SCHEMA")
    config = params["reader"]["workspace_config"]
    image = config["wire_profile"]["aggregate_image"]
    packet = read_pin(params["packet"], 16*MIB)
    claims, frontiers, witnesses, census = parse_packet(packet,
        Envelope(**config["packet_envelope"]), aggregate_image=image)
    F.need(len(claims) == len(frontiers) == len(witnesses) == 1 and claims[0][0] == 0,
           "REMOTE_CHECK_RETAINED_ONE_I_DELTA")
    spec = C.parse_json(witnesses[-1][0])["local_spec"]
    module = C.module_id(spec)
    F.need(module == C.summary_id(witnesses[-1][2]), "REMOTE_CHECK_TARGET")
    name = params["export_name"]
    C.validate_name(name)
    matches = [index for index, group in enumerate(spec["groups"])
               if any(row["name"] == name for row in group["declarations"])]
    F.need(len(matches) == 1, "REMOTE_CHECK_EXPORTED_DECLARATION")
    opening = C.group_opening(spec, matches[0])
    provider_path = context.workspace_root/(context.run.name+"-custody")
    reader_path = context.workspace_root/(context.run.name+"-reader")
    service_output, reader_output = (context.location_workspace/name
                                     for name in ("service", "reader"))
    service_output.mkdir()
    reader_output.mkdir()
    workspace = task = None
    report = {"schema": "DMKN_V5_REMOTE_CHECK_RESULT_V1", "status": "FAILED",
              "error": None, "cleanup_errors": [], "reader": None, "service": None,
              "scope": "REAL_RETAINED_I_NATIVE_REMOTE_ADMISSION_AND_IMPORT_NO_NEW_PROOF",
              "authority": "OPERATION_EVIDENCE_NOT_TRANSFERABLE_AUTHORITY",
              "new_proof_calls": 0, "public_network_calls": 0}
    try:
        workspace = Workspace.open(provider_path, config, create=True)
        workspace.modules.put_group(module, opening)
        workspace.packets.put(module, packet)
        workspace.index.admit(workspace.adapter.encode_opening(module, name, opening),
                              expected_id=C.export_id(module, name))
        workspace.close()
        workspace = None
        service_params = {
            "schema": serve_workspace.SCHEMA, "mode": "validated",
            "workspace_path": str(provider_path), "workspace_config": config,
            "bind": {"host": "127.0.0.1", "port": 0}, "tls": None,
            "service_limits": params["service_limits"],
        }
        service_context = replace(context, location_workspace=service_output,
                                  parameters=MappingProxyType(service_params))
        task = asyncio.create_task(serve_workspace.serve(service_context))
        ready_path = service_output/"service-ready.json"
        # One bounded startup observation, not service discovery or a retry.
        while not ready_path.exists():
            context.remaining_seconds()
            F.need(not task.done(), "REMOTE_CHECK_SERVICE_FAILED_BEFORE_READY")
            await asyncio.sleep(0.02)
        raw = ready_path.read_bytes()
        F.need(len(raw) <= MIB, "REMOTE_CHECK_READY_BOUND")
        ready = json.loads(raw)
        endpoint = ready["endpoint"]
        F.need(endpoint["host"] == "127.0.0.1" and not endpoint["tls"],
               "REMOTE_CHECK_LOOPBACK_ONLY")
        reader_params = deepcopy(params["reader"])
        reader_params.update(workspace_path=str(reader_path), create_workspace=True)
        query = reader_params["query"]
        label = query["selection"]["provider"]
        query["contacts"] = {label: endpoint}
        query["egress_policy"] = {"schema": "DMKN_V5_OWNER_EGRESS_V1",
            "mode": "loopback-test", "public_ports": [],
            "test_endpoints": [{"host": endpoint["host"], "port": endpoint["port"]}]}
        reader_context = replace(context, location_workspace=reader_output,
                                 parameters=MappingProxyType(reader_params))
        result = await remote_reader.run(reader_context)
        report["reader"] = result
        F.need(result["status"] == "COMPLETED" and result["read"]["status"] == "READY",
               "REMOTE_CHECK_ACTUAL_READER_READY")
        client = result["client"]
        F.need(result["read"]["admitted"]["kind"] == "mixed"
               and result["read"]["admitted"]["module"] == module,
               "REMOTE_CHECK_EXACT_RECEIVED_TARGET")
        F.need(client["receipt"]["attempts"] == client["mixed"]["attempts"] == 1
               and client["aggregate"]["attempts"] == 0
               and client["counts"]["admission_submissions"] == 1
               and client["counts"]["new_import_sessions"] == 1
               and client["counts"]["author_calls"] == client["counts"]["publication_attempts"] == 0
               and client["preparation"] is None and client["location"] is None,
               "REMOTE_CHECK_REAL_I_NATIVE_ONLY")
        F.need(result["read"]["context_cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
               "REMOTE_CHECK_NO_ANCESTRAL_PROOF_FRONTEND")
        report["service"] = await task
        F.need(report["service"]["status"] == "PASS", "REMOTE_CHECK_SERVICE_CLOSURE")
        report.update(status="PASS", packet_pin=params["packet"], target_module=module,
                      packet_census=census)
    except BaseException as error:
        report["error"] = {"type": type(error).__name__, "message": str(error)[:1000]}
        raise
    finally:
        if task is not None and not task.done():
            task.cancel()
        if task is not None:
            try:
                terminal = await task
                report["service"] = terminal
            except asyncio.CancelledError:
                report["cleanup_errors"].append("service_cancelled_after_integration_failure")
            except BaseException as error:
                report["cleanup_errors"].append(type(error).__name__+":"+str(error)[:500])
        if workspace is not None:
            try:
                workspace.close()
            except BaseException as error:
                report["cleanup_errors"].append(type(error).__name__+":"+str(error)[:500])
        if report["cleanup_errors"]:
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        save(context.location_workspace/"remote-check-result.json", report)
    return 0 if report["status"] == "PASS" else 1


def main(context):
    return asyncio.run(run(context))

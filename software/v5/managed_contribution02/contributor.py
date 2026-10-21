"""Selected ordinary public owner: one independent structural contribution.

No prover/verifier/trust adoption. Retained genuine artifacts exercise the new
private handoff and existing network submission, not new mathematics.
"""
import asyncio
from copy import deepcopy
import hashlib
from pathlib import Path
import time

from client.workspace_evidence import Workspace
from client.private_credentials import read_client
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from evidence_network.packet import pack_terminal_i
from evidence_network.transport import CompositeProvider
from modules import codec as C
from aggregate_claims import bindings as B
from placement import codec as P

MIB = 1024**2
FIXTURES = {
    "receipt": (223594, "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"),
    "journal": (184, "22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682"),
    "bundle": (53769, "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926"),
}
OPENING = (1595, "0c74d294730fc2d005a082aba01350e5a9ab54a5aa797036f35d607ce17c900a")
PACKET = (447887, "a737e8f650e9d3abb4781bb2c85c0e625ed4573b7170d71aff1799dbb54495e3")


def sha(raw): return hashlib.sha256(raw).hexdigest()


def pinned(row, expected):
    F.fields(row, ("path", "bytes", "sha256"))
    F.need((row["bytes"], row["sha256"]) == expected, "CONTRIBUTOR_FIXTURE_IDENTITY")
    path = ordinary(row["path"], directory=False)
    F.need(path.stat().st_size == row["bytes"] <= MIB, "CONTRIBUTOR_FIXTURE_BOUND")
    with path.open("rb") as stream: raw = stream.read(MIB+1)
    F.need((len(raw), sha(raw)) == expected, "CONTRIBUTOR_FIXTURE_PIN")
    return raw


def seed(workspace, fixtures):
    F.fields(fixtures, FIXTURES)
    blobs = {key: pinned(fixtures[key], identity) for key, identity in FIXTURES.items()}
    bundle = C.parse_json(blobs["bundle"])
    module = C.module_id(bundle["spec"])
    member = B.member_journal(blobs["journal"])
    F.need(member["module"] == module and member["summary"] == C.summarize(bundle["spec"]),
           "CONTRIBUTOR_FIXTURE_JOURNAL")
    opening = C.group_opening(bundle["spec"], 10)
    name = [["s", "CommonsV5"], ["s", "binary_congr"]]
    F.need(opening == bundle["openings"][10] and opening["group"]["declarations"][0]["name"] == name,
           "CONTRIBUTOR_SELECTED_OPENING")
    packet = pack_terminal_i(blobs["journal"], blobs["receipt"],
        aggregate_image=workspace.config["wire_profile"]["aggregate_image"], envelope=workspace._envelope,
        terminal_receipt_bytes=workspace.config["terminal_receipt_bytes"], terminal_i=True)
    F.need((len(C.canonical(opening)), sha(C.canonical(opening))) == OPENING
           and (len(packet), sha(packet)) == PACKET, "CONTRIBUTOR_RETAINED_BYTES")
    workspace.modules.put_group(module, opening)
    workspace.packets.put(module, packet)
    return module, name, opening, packet


async def contribute(context, p, report):
    workspace = provider = client = None
    cleanup = []
    try:
        F.need(time.monotonic()+35 < context.deadline, "CONTRIBUTOR_ORIGINAL_RESERVATION")
        deadline = context.deadline-10
        workspace = Workspace.open(context.location_workspace/"source-workspace", p["workspace_config"], create=True)
        module, name, opening, packet = seed(workspace, p["fixtures"])
        source = p["source_endpoint"]
        F.need(source == p["expected"]["source"] and source["host"] == "127.0.0.1"
               and source["tls"] is False and source["server_name"] is None, "CONTRIBUTOR_LOOPBACK_SOURCE")
        # The existing group route reserves 16 MiB before dispatch; actual
        # fixture bytes are much smaller. Keep room for the later offer/packet.
        provider = CompositeProvider(index=workspace.index, custody=workspace.modules, packets=workspace.packets,
            max_connections=2, max_requests=8, max_reply_bytes=20*MIB, operation_ms=10000)
        endpoint = await provider.start(host=source["host"], port=source["port"])
        F.need((endpoint.host, endpoint.port, endpoint.tls) == (source["host"], source["port"], False),
               "CONTRIBUTOR_SOURCE_ENDPOINT")
        client, metadata = read_client(p["credential"], p["expected"], egress=p["egress"],
            contact=p["intake_endpoint"], deadline=deadline, requests=1,
            incoming_bytes=90112, outgoing_bytes=25600, operation_ms=30000)
        F.need(metadata == p["expected"], "CONTRIBUTOR_PUBLIC_METADATA")
        bindings = metadata["bindings"]
        F.need(bindings["namespace"] == workspace.adapter.namespace
               and bindings["wire_profile_id"] == workspace.packets.profile_id, "CONTRIBUTOR_WORKSPACE_DOMAIN")
        export = workspace.adapter.encode_opening(module, name, opening)
        fingerprint = [spec for spec in workspace.adapter.describe(export)["specs"]
                       if spec["tag"] == "conclusion-fingerprint"]
        F.need(len(fingerprint) == 1, "CONTRIBUTOR_SINGLE_FINGERPRINT")
        manifest = dict(schema=P.REQUEST_SCHEMA, generation=bindings["generation"],
            namespace=bindings["namespace"], wire_profile_id=bindings["wire_profile_id"],
            module_id=module, relative_name=name, export_id=C.export_id(module, name),
            fingerprint=fingerprint[0], cell=P.cell(workspace.adapter, fingerprint[0])[0],
            export_object_sha256=sha(export), export_object_bytes=len(export), opening_max_bytes=65536,
            packet_sha256=sha(packet), packet_bytes=len(packet), bodies=[], retention_end_ms=p["retention_end_ms"])
        quote = P.quote(manifest, new_cell=True,
                        index_logical_cap=p["workspace_config"]["index_limits"]["max_logical_bytes"])
        F.need(all(quote[key] <= metadata["limits"][key] for key in P.RESOURCES), "CONTRIBUTOR_FUNDED_QUOTE")
        raw = F.compact(manifest)
        report.update(stage="submit", manifest=manifest, manifest_sha256=sha(raw), quote=quote,
            source_opening={"bytes": OPENING[0], "sha256": OPENING[1]},
            source_packet={"bytes": PACKET[0], "sha256": PACKET[1]})
        observed = await client.submit(raw)
        report["observed"] = observed
        response = observed["response"]
        F.need(observed["acknowledgement"] == "LOOPBACK_RESPONSE_OBSERVED"
               and response["request_id"] == P.request_id(raw, metadata["grant_id"], bindings["generation"])
               and response["placement"]["phase"] == "RECEIPT_COMMITTED"
               and response["placement"]["reservation"] == quote
               and response["placement"]["outcome"]["status"] == "INDEXED_UNADVERTISED",
               "CONTRIBUTOR_COMMITTED_PLACEMENT")
        report["source_operations_empty"] = not any((workspace.root/"operations").iterdir())
        F.need(report["source_operations_empty"], "CONTRIBUTOR_NO_PROOF_OPERATION")
        report["stage"] = "submitted"
    finally:
        if client is not None:
            try: client.close(); report["client"] = client.report()
            except BaseException: cleanup.append("CLIENT_CLOSE")
        if provider is not None:
            try:
                await provider.stop()
                report["source_provider"] = provider.status()
                F.need(provider.server is None and not provider.tasks, "CONTRIBUTOR_PROVIDER_CLOSE")
            except BaseException: cleanup.append("PROVIDER_CLOSE")
        if workspace is not None:
            try: workspace.close(); report["source_closed"] = True
            except BaseException: cleanup.append("WORKSPACE_CLOSE")
        report["cleanup_errors"] = cleanup
        F.need(not cleanup, "CONTRIBUTOR_CLEANUP_FAILED")


def main(context):
    report = {"schema": "DMKN_MANAGED_CONTRIBUTION_ACTOR_RESULT_V1", "status": "FAIL", "stage": "input",
        "mathematical_acceptance": False, "proof_generation": False, "public_deployment_qualified": False}
    try:
        p = deepcopy(dict(context.parameters))
        F.fields(p, ("schema", "workspace_config", "fixtures", "credential", "expected", "egress",
                     "source_endpoint", "intake_endpoint", "retention_end_ms"))
        F.need(p["schema"] == "DMKN_MANAGED_CONTRIBUTION_ACTOR_V1", "CONTRIBUTOR_SCHEMA")
        asyncio.run(contribute(context, p, report))
        report.update(status="PASS", stage="complete")
    except BaseException:
        # Secret-bearing client objects/errors/traceback locals are never serialized.
        report["error_code"] = "CONTRIBUTOR_OPERATION_FAILED"
    raw = F.compact(report)
    F.need(len(raw) <= MIB, "CONTRIBUTOR_REPORT_BOUND")
    with (context.location_workspace/"contributor-result.json").open("xb") as stream:
        stream.write(raw)
    return 0 if report["status"] == "PASS" else 1

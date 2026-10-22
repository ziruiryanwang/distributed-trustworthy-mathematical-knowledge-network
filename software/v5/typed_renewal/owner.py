"""Finite current-client U-to-V owner; no snapshot, proving or publication.

Run only through the selected client boot/Job. Copy source.py as the pinned
owner/renewal_source.py helper, preserving the current130 SDK source map.
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
from delta_claims.claims import expected_journal
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from mixed_claims.packet import Envelope
from modules import codec as C

MIB = 1024**2
SCHEMA = "DMKN_TYPED_RENEWAL_OWNER_V1"
ACTION = "explicit-temporary-A-only-adoption-and-source-renewal"
FOUNDATION_SHA = "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"
SOURCE_PINS = {
    "v5/client/runtime.py": "70c52b5148c481ca840c6c55557c9bc5abf71f40d522365f0cb7b0398adbad39",
    "v5/client/workspace_evidence.py": "62c4ea578cf92c85b398880e8cfba9e914ecf6668e3916bd1d87ce5ee02efcce",
    "v5/client/workspace_atomic.py": "32e3b95ea2e6d3f8dc35d63000728e9e075a16de3e13fb1a0b718bce45e11773",
    "v5/mixed_claims/imports_atomic.py": "45b082863525fb08c1e8925e998113b55deff4b92482c8cf9b63cea2093725ad",
    "v5/mixed_claims/authoring_atomic.py": "081d9d18d16d1cd68b40a5f3cf52493bac7e2e2dbdfb9bd632b72d74de235dbc",
    "v5/mixed_claims/receiver.py": "5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b",
    "v5/admission/trust.py": "c997d2a83ae5246dec9ff30eeca72e405ec0f66c0a307e53e0521eef66fae6d0",
}


def _helper(context):
    key = "owner/renewal_source.py"
    path = ordinary(context.sources_owner/"renewal_source.py", directory=False)
    read_pin(dict(path=str(path), bytes=path.stat().st_size,
                  sha256=context.source_sha256[key]), MIB)
    F.need("renewal_source" not in sys.modules, "RENEWAL_HELPER_COLLISION")
    previous = list(sys.path)
    try:
        sys.path.insert(0, str(context.sources_owner))
        helper = import_module("renewal_source")
        F.need(Path(helper.__file__).resolve() == path, "RENEWAL_HELPER_ORIGIN")
        return helper
    finally:
        sys.path[:] = previous


def _parameters(context):
    p = deepcopy(dict(context.parameters))
    F.fields(p, {"schema", "action", "runtime_adoption", "foundation", "receipt", "header", "journal",
        "membership", "opening", "workspace_config", "workspace_path", "domain_path", "domain_id",
        "operation_limits", "receipt_limits", "author_limits", "admission_limits"})
    F.need(p["schema"] == SCHEMA and p["action"] == ACTION, "RENEWAL_EXPLICIT_ACTION")
    F.need(Path(__file__).resolve() == context.sources_owner/"owner.py"
           and len(context.source_sha256) == 132
           and {name for name in context.source_sha256 if name.startswith("owner/")}
               == {"owner/owner.py", "owner/renewal_source.py"}
           and all(context.source_sha256.get(name) == digest for name, digest in SOURCE_PINS.items()),
           "RENEWAL_CURRENT_SELECTED_SOURCES")
    F.need(p["runtime_adoption"]["receipt"] is None
           and p["runtime_adoption"]["aggregate"] is not None, "RENEWAL_A_ONLY_ADOPTION")
    F.need(p["foundation"]["bytes"] == 23313 and p["foundation"]["sha256"] == FOUNDATION_SHA,
           "RENEWAL_EXACT_FOUNDATION")
    for name in ("receipt_limits", "author_limits", "admission_limits"):
        fields = {"cpu_seconds", "wall_seconds", "memory_mib"} if name != "admission_limits" else {
            "native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds", "memory_mib"}
        F.fields(p[name], fields)
        for field, value in p[name].items():
            F.uint(value, 64 if field == "memory_mib" else 1, 4096 if field == "memory_mib" else 600)
        F.need(p[name]["memory_mib"] <= context.limits["memory_mib"], "RENEWAL_OUTER_MEMORY")
    C.digest_string(p["domain_id"])
    paths = {}
    for field in ("workspace_path", "domain_path"):
        path = ordinary(p[field], fresh=True)
        for other in (context.installation.parent, context.run, context.sources_owner,
                      context.sources_v5, context.sources_portable, *paths.values()):
            other = Path(other)
            F.need(not path.is_relative_to(other) and not other.is_relative_to(path), "RENEWAL_DISJOINT_STATE")
        paths[field] = path
    context.remaining_seconds()
    F.need(time.monotonic() < context.deadline-15, "RENEWAL_CLEANUP_MARGIN")
    return p, paths


def _raw(path, maximum=16*MIB):
    path = ordinary(path, directory=False)
    size = path.stat().st_size
    F.need(0 < size <= maximum, "RENEWAL_OUTPUT_READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    F.need(len(raw) == size, "RENEWAL_OUTPUT_READ_CHANGED")
    return raw


def _save_bytes(path, raw):
    path = ordinary(path, fresh=True, directory=False)
    with path.open("xb") as stream:
        F.need(stream.write(raw) == len(raw), "RENEWAL_OUTPUT_WRITE")
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


async def run(context):
    work = ordinary(context.location_workspace)
    output = ordinary(work/"typed-renewal-result.json", fresh=True, directory=False)
    report = dict(schema="DMKN_TYPED_RENEWAL_RESULT_V1", status="FAILED", stage="parameters",
        error=None, cleanup_errors=[], client_closed=False, workspace_closed=False, domain_withdrawn=False,
        domain_creation="NOT_ATTEMPTED",
        cryptographic_production_calls=0, snapshot_calls=0, network_calls=0, publication_calls=0,
        mathematical_acceptance=False, full_v5_release=False,
        authority="LOCAL_OPERATION_REPORT_NOT_TRANSFERABLE_AUTHORITY")
    workspace = client = domain = None
    primary = cancelled = None
    try:
        p, paths = _parameters(context); helper = _helper(context)
        F.need(p["runtime_adoption"]["aggregate"]["image"]
               == p["workspace_config"]["wire_profile"]["aggregate_image"] == helper.A_IMAGE,
               "RENEWAL_EXPLICIT_TYPED_IMAGE")
        foundation = read_pin(p["foundation"], MIB)
        member = C.parse_json(read_pin(p["membership"], 65536))
        F.fields(member, {"index", "siblings"})
        F.need(type(member["siblings"]) is list and len(member["siblings"]) <= B.MAX_SIBLINGS,
               "RENEWAL_MEMBER_BOUND")
        for digest in member["siblings"]: C.digest_string(digest)
        material = dict(schema=helper.MATERIAL_SCHEMA, receipt=read_pin(p["receipt"], 64*MIB),
            header=read_pin(p["header"], B.HEADER_BYTES), journal=read_pin(p["journal"], 184),
            member_index=member["index"], siblings=[bytes.fromhex(digest) for digest in member["siblings"]],
            opening=C.parse_json(read_pin(p["opening"], MIB)))
        helper.validate_material(material)
        report["input_pins"] = {name: deepcopy(p[name]) for name in
            ("foundation", "receipt", "header", "journal", "membership", "opening")}
        report["stage"] = "explicit-adoption"
        support = RuntimeProfile.support_manifest(context, p["runtime_adoption"])
        report["domain_creation"] = "ATTEMPTED_STATE_UNCONFIRMED"
        domain = TrustDomain.create(paths["domain_path"], p["domain_id"], support)
        report["domain_creation"] = "OPENED"
        report["trust"] = domain.identity()
        runtime = RuntimeProfile.from_context(context, p["runtime_adoption"], trust_domain=domain)
        workspace = Workspace.open(paths["workspace_path"], p["workspace_config"], create=True)
        grant = workspace.reserve(p["operation_limits"], outer_deadline=context.deadline-15)
        report["operation_id"] = grant.identifier
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=True,
            foundation_bytes=foundation, foundation_sha256=FOUNDATION_SHA)
        report["stage"] = "verify-genuine-A-member"
        warrant = client.admit_aggregate_member(material["receipt"], material["header"], material["journal"],
            material["member_index"], material["siblings"], **p["receipt_limits"])
        parent = client.describe(warrant)
        F.need(parent["kind"] == "A-member" and parent["live"]["journal"] == material["journal"]
               and parent["live"]["module"] == helper.U_MODULE, "RENEWAL_ACTUAL_U_WARRANT")
        report["parent"] = dict(module=helper.U_MODULE, journal=list(material["journal"]),
                                 receipt_sha256=hashlib.sha256(material["receipt"]).hexdigest())
        ready = client.import_context([dict(warrant=warrant, resolutions=None)], [material["journal"]],
            [dict(module=helper.U_MODULE, opening=material["opening"])], [], definition_mode="interface-only")
        report["context"] = {key: ready[key] for key in ("status", "cost", "demands")}
        F.need(ready["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY" and not ready["demands"]
               and ready["cost"]["groups"] == ready["cost"]["declarations"] == 1
               and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0, "RENEWAL_READY_INTERFACE")
        report["stage"] = "source-author-once"
        prepared = client.author(ready["context"], helper.v_source(), [helper.V_NAME], **p["author_limits"])
        F.need(prepared["status"] == "UNTRUSTED_MIXED_DELTA_PACKET_PREPARED"
               and prepared["mathematical_acceptance"] is False, "RENEWAL_AUTHOR_NOT_AUTHORITY")
        child = prepared["child"]; raw = child["packet"]
        predicted = expected_journal(child["summary"], 2, B.RELATION_IMAGE)
        envelope = Envelope(**p["workspace_config"]["packet_envelope"])
        shape = helper.validate_renewal_packet(raw, predicted, material, envelope=envelope)
        F.need(child["local_module"] == helper.V_MODULE and child["roots"] == [helper.V_NAME]
               and child["packet_sha256"] == hashlib.sha256(raw).hexdigest()
               and child["source_sha256"] == hashlib.sha256(helper.v_source().encode("utf-8")).hexdigest(),
               "RENEWAL_AUTHOR_PACKET_BINDING")
        directory = grant.directory/"preparation"/"author-1"
        F.need(_raw(directory/"mixed-packet.json") == raw, "RENEWAL_ACTUAL_AUTHOR_PACKET")
        request_raw = _raw(directory/"source-request.json")
        export_raw = _raw(directory/"frontend"/"EXPORT.json")
        worker = C.parse_json(_raw(directory/"worker-result.json", MIB))
        F.need(worker["status"] == "PASS_NATIVE_EXPORT_ONLY"
               and worker["request_sha256"] == hashlib.sha256(request_raw).hexdigest()
               and worker["export_sha256"] == hashlib.sha256(export_raw).hexdigest()
               and worker["export_bytes"] == len(export_raw) and worker["native_return_code"] == 0
               and worker["native_timed_out"] is False and worker["direct_child_reaped"] is True,
               "RENEWAL_ACTUAL_FRONTEND_BINDING")
        report["source_inspection"] = helper.inspect_source_export(C.parse_json(request_raw),
            C.parse_json(export_raw), shape["witness"], material)
        report["stage"] = "independent-native-V-admission"
        workspace.packets.put(helper.V_MODULE, raw, before_commit=grant.remaining_seconds)
        checked = client.admit_local(helper.V_MODULE, child["packet_sha256"], len(raw),
            expected_exact_journal=predicted, **p["admission_limits"])
        fact = client.describe(checked); live = fact["live"]
        F.need(fact["kind"] == "mixed" and live["journal"] == predicted
               and live["module"] == helper.V_MODULE and live["summary"] == shape["summary"]
               and live["packet_sha256"] == child["packet_sha256"], "RENEWAL_ACTUAL_V_ACCEPTANCE")
        report["packet"] = _save_bytes(work/"V.packet.json", raw)
        report["journal"] = _save_bytes(work/"V.journal", live["journal"])
        report["source"] = _save_bytes(work/"V.lean", helper.v_source().encode("utf-8"))
        report["census"] = shape["census"]
        report["before_close"] = client.report()
        report.update(status="COMPLETED", stage="done", local_U_and_V_admitted=True)
    except BaseException as error:
        primary = error; report["error"] = remote_reader._error(error)
        if isinstance(error, asyncio.CancelledError): cancelled = error
    finally:
        if client is not None:
            try:
                closed = await client.close(); report["client"] = closed
                F.need(closed["closed"] and not closed["cleanup_uncertain"] and closed["receipt"] is None
                       and all(closed[name] is not None and closed[name]["closed"]
                               for name in ("aggregate", "mixed", "preparation")), "RENEWAL_CLIENT_CLOSURE")
                if report["status"] == "COMPLETED":
                    F.need(closed["status"] == "CLOSED" and not closed["failures"], "RENEWAL_CLEAN_SUCCESS")
                report["client_closed"] = True
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="client", **remote_reader._error(error)))
                if isinstance(error, asyncio.CancelledError): cancelled = error
        if workspace is not None:
            try:
                report["workspace_closed"] = _close_workspace(workspace, report["cleanup_errors"])
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="workspace-helper", **remote_reader._error(error)))
                if isinstance(error, asyncio.CancelledError): cancelled = error
        if domain is not None:
            try:
                domain.withdraw("Explicit finite typed renewal operation completed or failed")
                withdrawal = C.parse_json(_raw(paths["domain_path"]/"WITHDRAWN", 16384))
                F.need(withdrawal["schema"] == "DMKN_LOCAL_TRUST_WITHDRAWN_V1"
                       and withdrawal["adoption"] == report["trust"], "RENEWAL_EXACT_WITHDRAWAL")
                report.update(domain_withdrawn=True, withdrawal=withdrawal)
            except BaseException as error:
                report["cleanup_errors"].append(dict(component="trust", **remote_reader._error(error)))
                if isinstance(error, asyncio.CancelledError): cancelled = error
        if report["cleanup_errors"] or not all(report[key] for key in
                ("client_closed", "workspace_closed", "domain_withdrawn")) or time.monotonic() >= context.deadline:
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        try: remote_reader._save(output, report)
        except BaseException as error:
            if primary is not None:
                raise BaseExceptionGroup("Renewal operation and report write failed", [primary, error])
            raise
    if cancelled is not None: raise cancelled
    return report


def main(context):
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1

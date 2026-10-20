"""Optional owner policy: continue a live selected context to a checked output.

Borrows the client's original operation; never opens, closes, imports or retries.
This is trusted local-agent composition, not a new mathematical authority.
"""
from copy import deepcopy
import hashlib

from discovery import formal_features as F
from modules import codec as C


def contribute_from_context(client, context, *, source, roots, export_names,
                            author_limits, admission_limits):
    """Author once, admit the NEW packet, then publish it locally.

    ``context`` is the exact live token issued to ``client``, not a READY report.
    Existing authoring enforces its ownership/liveness. Calls must be serialized;
    the caller still owns client/workspace cleanup, including on exceptions.
    """
    roots, export_names = deepcopy(roots), deepcopy(export_names)
    author_limits, admission_limits = deepcopy(author_limits), deepcopy(admission_limits)
    F.need(type(source) is str, "CONTEXT_CONTRIBUTION_SOURCE")
    for names in (roots, export_names):
        F.need(type(names) is list and 1 <= len(names) <= 64, "CONTEXT_CONTRIBUTION_NAMES")
        for name in names:
            C.validate_name(name)
        F.need(len({C.name_key(name) for name in names}) == len(names),
               "CONTEXT_CONTRIBUTION_DUPLICATE_NAMES")
    F.fields(author_limits, {"cpu_seconds", "wall_seconds", "memory_mib"})
    F.uint(author_limits["cpu_seconds"], 1, 1200, "CONTEXT_CONTRIBUTION_AUTHOR_CPU")
    F.uint(author_limits["wall_seconds"], 1, 600, "CONTEXT_CONTRIBUTION_AUTHOR_WALL")
    F.fields(admission_limits, {"native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds", "memory_mib"})
    for key in ("native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds"):
        F.uint(admission_limits[key], 1, 600, "CONTEXT_CONTRIBUTION_ADMISSION:" + key)
    for limits in (author_limits, admission_limits):
        F.uint(limits["memory_mib"], 64, 4096, "CONTEXT_CONTRIBUTION_MEMORY")

    workspace, grant = client.workspace, client.grant
    prepared = client.author(context, source, roots, **author_limits)
    F.need(type(prepared) is dict, "CONTEXT_CONTRIBUTION_PREPARATION")
    report = {"schema": "DMKN_V5_CONTEXT_CONTRIBUTION_RESULT_V1",
        "operation_id": grant.identifier, "status": None, "demands": [],
        "preparation": {"status": prepared.get("status")},
        "checked_output": None, "publication": None, "mathematical_acceptance": False,
        "authority": "OPERATIONAL_CONTRIBUTION_REPORT_NOT_TRANSFERABLE_AUTHORITY"}
    if prepared.get("status") == "NEED_AUTHORING_CONTEXT_DATA":
        report.update(status="NEED_AUTHORING_CONTEXT_DATA",
                      demands=deepcopy(prepared.get("demands", [])))
        return report
    F.need(prepared.get("status") == "UNTRUSTED_MIXED_DELTA_PACKET_PREPARED"
           and prepared.get("mathematical_acceptance") is False,
           "CONTEXT_CONTRIBUTION_UNTRUSTED_PREPARATION")
    child = prepared.get("child")
    F.need(type(child) is dict, "CONTEXT_CONTRIBUTION_CHILD")
    raw = child.get("packet")
    F.need(child.get("status") == "UNTRUSTED_MIXED_DELTA_PACKET"
           and child.get("mathematical_acceptance") is False and type(raw) is bytes,
           "CONTEXT_CONTRIBUTION_PREPARED_PACKET")
    packet_sha = hashlib.sha256(raw).hexdigest()
    F.need(packet_sha == child.get("packet_sha256")
           and child.get("source_sha256") == hashlib.sha256(source.encode("utf-8")).hexdigest()
           and child.get("roots") == roots, "CONTEXT_CONTRIBUTION_PREPARATION_BINDING")
    module = child["local_module"]
    report["preparation"].update(module=module, packet_sha256=packet_sha,
        packet_bytes=len(raw), source_sha256=child["source_sha256"], roots=roots)

    # Same lower-level quota-bounded custody as contribute.py. This is not
    # admission and is not a separately charged client action. The old grant
    # and enclosing Job remain in force; no new allowance is created here.
    grant.remaining_seconds()
    workspace.packets.put(module, raw, before_commit=grant.remaining_seconds)
    checked = client.admit_local(module, packet_sha, len(raw), **admission_limits)
    fact = client.describe(checked)
    live = fact["live"]
    F.need(live["module"] == module and live["packet_sha256"] == packet_sha
           and live["summary"] == child["summary"], "CONTEXT_CONTRIBUTION_OUTPUT_BINDING")
    report["checked_output"] = {"kind": fact["kind"], "module": module,
        "journal": list(live["journal"]), "packet_sha256": packet_sha}
    publication = client.publish(raw, export_names,
        retention_policy={"mode": "quota-bounded-local-custody"})
    F.need(publication["phase"] == "LOCALLY_PUBLISHED"
           and publication["intent"]["module"] == module
           and publication["intent"]["packet_sha256"] == packet_sha
           and publication["intent"]["packet_bytes"] == len(raw)
           and publication["intent"]["export_names"] == export_names,
           "CONTEXT_CONTRIBUTION_PUBLICATION_BINDING")
    report.update(status="CONTRIBUTED", publication=publication)
    return report

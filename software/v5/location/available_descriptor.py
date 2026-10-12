"""Typed descriptor unavailability on the SAME actual channel/workflow/grant.

Requires a root-adopted fresh Node entry with DESCRIPTOR_UNAVAILABLE replies.
No retry, new process, new grant, endpoint injection or mathematical authority.
"""
import base64
import time

from discovery import formal_features as F
from . import protocol as P
from .controller_services import ServiceLocatedWorkflow, ServiceLocationProcess


async def descriptor(workflow, peer, route_key, *, max_bytes=4096, max_age_ms=60000):
    F.need(type(workflow) is ServiceLocatedWorkflow
           and type(workflow.channel) is ServiceLocationProcess,
           "AVAILABLE_EXACT_EXISTING_WORKFLOW")
    channel, budget = workflow.channel, workflow._workflow
    ticket = budget.begin_descriptor(peer, route_key, max_bytes=max_bytes, max_age_ms=max_age_ms)
    settled = False
    try:
        until = min(workflow.deadline, ticket.pop("until"))
        ticket["remaining_wall_ms"] = max(0, int((until-time.monotonic())*1000))
        reply = await channel.command("descriptor", ticket, until=until)
        if reply.get("status") == "DESCRIPTOR_UNAVAILABLE":
            F.fields(reply, ("status", "ticket", "peer", "reason", "mathematical_acceptance"))
            F.need(reply["ticket"] == ticket["ticket"] and reply["peer"] == peer
                   and reply["reason"] == "TCP_CONNECT_UNAVAILABLE"
                   and reply["mathematical_acceptance"] is False
                   and not channel.closed and not channel.channel_failed
                   and time.monotonic() < until, "AVAILABLE_REPLY_BINDING_OR_DEADLINE")
            charged = budget.abandon_descriptor(ticket["ticket"]); settled = True
            return {**reply, "settlement": charged, "global_complete": False,
                    "authenticated_peer": None}
        F.fields(reply, ("ticket", "authenticated_peer", "raw_base64", "request_body_bytes",
                         "reply_body_bytes", "framed_reply_bytes", "assurance", "mathematical_acceptance"))
        F.need(reply["ticket"] == ticket["ticket"] and reply["authenticated_peer"] == peer
               and reply["assurance"] == P.ASSURANCE and reply["mathematical_acceptance"] is False,
               "AVAILABLE_AUTHENTICATED_REPLY_BINDING")
        F.need(type(reply["raw_base64"]) is str and len(reply["raw_base64"]) <= 4*((max_bytes+2)//3),
               "AVAILABLE_RAW_BOUND")
        raw = base64.b64decode(reply["raw_base64"], validate=True)
        F.uint(reply["request_body_bytes"], 1, 2048)
        F.uint(reply["reply_body_bytes"], 1, max_bytes)
        F.uint(reply["framed_reply_bytes"], len(raw), max_bytes+4)
        F.need(len(raw) == reply["reply_body_bytes"], "AVAILABLE_BODY_LENGTH")
        # accept_descriptor takes its ticket before validating remote bytes.
        settled = True
        return budget.accept_descriptor(ticket["ticket"], raw, reply["authenticated_peer"])
    except BaseException:
        # Any malformed/authentication/IPC/budget outcome remains fail-closed.
        # The only recoverable outcome returned above is a typed local dial miss.
        await channel.close()
        raise
    finally:
        if not settled: budget.abandon_descriptor(ticket["ticket"])

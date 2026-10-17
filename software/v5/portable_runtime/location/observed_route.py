"""Keep advisory query diagnostics on the existing actual workflow/ticket.

No extra request, subclass, private provider list, deadline or routing allowance.
Requires the root-adopted maintained_roles_ready source in the child snapshot.
"""
import time

from discovery import formal_features as F
from . import protocol as P
from .controller_services import ServiceLocatedWorkflow, ServiceLocationProcess


CENSUS = ("events", "send_query", "peer_response", "final_peer", "query_error",
          "provider", "add_provider_write", "last_query_error")
TERMINATIONS = ("ROUTING_EXHAUSTED_NOT_GLOBAL_COMPLETE", "PROVIDER_BUDGET",
                "INCOMPLETE_QUERY_ERRORS", "INCOMPLETE_ABORTED_OR_FAILED")


async def route(workflow, features, stripe=0, *, event_cap, peer_cap):
    F.need(type(workflow) is ServiceLocatedWorkflow
           and type(workflow.channel) is ServiceLocationProcess,
           "OBSERVED_ROUTE_EXACT_EXISTING_WORKFLOW")
    channel, budget = workflow.channel, workflow._workflow
    ticket = budget.begin_route(features, stripe, event_cap=event_cap, peer_cap=peer_cap)
    settled = False
    try:
        ticket["remaining_wall_ms"] = max(0, int((workflow.deadline-time.monotonic())*1000))
        reply = await channel.command("locate", ticket, until=workflow.deadline)
        F.fields(reply, ("ticket", "route_key", "peers", "termination", "error", "census",
                         "routing_peers_before", "routing_peers_after", "assurance",
                         "global_complete", "mathematical_acceptance"))
        F.need(reply["ticket"] == ticket["ticket"] and reply["route_key"] == ticket["route_key"]
               and reply["assurance"] == P.ASSURANCE and reply["global_complete"] is False
               and reply["mathematical_acceptance"] is False,
               "OBSERVED_ROUTE_CHANNEL_BINDING")
        F.need(reply["termination"] in TERMINATIONS, "OBSERVED_ROUTE_TERMINATION")
        F.need(reply["error"] is None or type(reply["error"]) is str and len(reply["error"]) <= 500,
               "OBSERVED_ROUTE_ERROR_BOUND")
        census = reply["census"]
        F.fields(census, CENSUS)
        for key in CENSUS[:-1]: F.uint(census[key], 0, 8192, "OBSERVED_ROUTE_CENSUS")
        F.need(census["last_query_error"] is None or type(census["last_query_error"]) is str
               and len(census["last_query_error"]) <= 500, "OBSERVED_ROUTE_LAST_ERROR_BOUND")
        F.need(all(census[key] <= census["events"] for key in CENSUS[1:-1])
               and census["add_provider_write"] == 0, "OBSERVED_ROUTE_CENSUS_BINDING")
        for key in ("routing_peers_before", "routing_peers_after"):
            F.uint(reply[key], 0, 16384, "OBSERVED_ROUTE_TABLE_BOUND")
        F.need(not channel.closed and not channel.channel_failed
               and time.monotonic() < workflow.deadline, "OBSERVED_ROUTE_LIVE_CHANNEL")
        # The unchanged budget consumes this exact ticket before peer validation.
        # An incomplete route may still expose authentic advisory hints; neither
        # an empty result nor any termination proves mathematical nonexistence.
        settled = True
        result = budget.accept_route(ticket["ticket"], reply["peers"])
        return {**result, "termination":reply["termination"], "error":reply["error"],
                "census":census, "routing_peers_before":reply["routing_peers_before"],
                "routing_peers_after":reply["routing_peers_after"]}
    except BaseException:
        await channel.close()
        raise
    finally:
        if not settled: budget.abandon_route(ticket["ticket"])

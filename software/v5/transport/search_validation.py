"""Reject invalid index metadata before the original session commits anything.

The pure preflight is deliberately repeated by unchanged SearchSession.accept
on success. It reads only the touched snapshot/page, never copies session
history, installs metadata, issues warrants, retries, or renews an allowance.
Only expected validation errors are recoverable; local and commit errors fail.
"""
from dataclasses import dataclass

from discovery import candidate_query as C
from discovery import discovery_query as Q
from discovery import formal_features as F
from discovery import summary_wire as W
from . import http_provider as H
from . import search_resilience as R

SCHEMA = "DMKN_SEARCH_VALIDATION_REFUSAL_V1"


@dataclass(frozen=True)
class _InvalidMetadata:
    code: str


class _LocalGuardFailure(RuntimeError):
    def __init__(self, error):
        self.error = error
        super().__init__("SEARCH_LOCAL_GUARD_FAILURE")


def _pending(session, ticket):
    F.need(set(session.pending) == {ticket["ticket"]}, "SEARCH_EXACT_PENDING_TICKET")
    held = session.pending[ticket["ticket"]]
    F.need({key: value for key, value in held.items() if key != "reservation"} == ticket,
           "SEARCH_TICKET_BINDING_CHANGED")
    F.need(session.reserved == held["reservation"], "SEARCH_EXACT_PENDING_RESERVATION")


def _preflight(session, ticket, raw):
    """Return None or a typed data refusal; never call a stateful accept method."""
    _pending(session, ticket)
    F.need(type(raw) is bytes and len(raw) <= ticket["max_reply_bytes"],
           "SEARCH_EXACT_BOUNDED_RESPONSE")
    F.need((ticket["namespace"], tuple(ticket["features"])) == session._query,
           "SESSION_TICKET_QUERY_BINDING")
    operation, selected = ticket["operation"], ticket["snapshot_id"]
    F.need(operation in ("offer", "page", "candidates"), "SEARCH_SELECTED_OPERATION")
    if operation != "offer":
        F.need(selected in session.summaries and selected in session.coverage,
               "SESSION_VERIFIED_SUMMARY_REQUIRED")
    if operation == "page":
        coverage = session.coverage[selected]
        # This is local owner-state integrity, not malformed remote metadata.
        F.need(coverage.summary == session.summaries[selected], "SEARCH_COVERAGE_SUMMARY_BINDING")

    def guard():
        # A local deadline/offer-expiry ValueError is NOT bad remote metadata.
        # Other exception classes already escape the data-validation catch.
        try:
            if operation == "offer": session._offer_live(ticket)
            else: session._live()
        except ValueError as error:
            raise _LocalGuardFailure(error) from error

    try:
        guard()
        response = F.strict(raw, ticket["max_reply_bytes"])
        if operation == "offer":
            F.fields(response, ("schema", "namespace", "features", "status", "reason", "summary",
                                "global_complete", "mathematical_acceptance"))
            F.need(response["schema"] == "DMKN_DISCOVERY_OFFER_V1"
                   and response["namespace"] == ticket["namespace"]
                   and response["features"] == ticket["features"], "SESSION_OFFER_QUERY_BINDING")
            F.need(response["global_complete"] is False and response["mathematical_acceptance"] is False,
                   "SESSION_OFFER_ASSURANCE")
            status, reason = response["status"], response["reason"]
            if status != "OFFERED":
                F.need((status == "NO_OFFER" and reason in ("ROLE_NOT_SERVED", "NAMESPACE_NOT_SERVED"))
                       or (status == "REFUSED" and reason == "SUMMARY_RESOURCE_BOUND"),
                       "SESSION_OFFER_STATUS")
                F.need(response["summary"] is None, "SESSION_OFFER_NO_SUMMARY")
            else:
                F.need(reason == "SNAPSHOT_SELECTED" and type(response["summary"]) is dict,
                       "SESSION_OFFER_SUMMARY")
                selected = F.hexid(response["summary"].get("snapshot_id"))
                expanded = W.decode_summary(F.compact(response["summary"]), selected,
                    ticket["namespace"], ticket["features"],
                    max_wire_bytes=ticket["max_reply_bytes"],
                    max_expanded_bytes=ticket["max_expanded_bytes"], check_budget=guard)
                verified = Q.verify_summary(selected, ticket["namespace"], ticket["features"], expanded)
                if selected in session.summaries:
                    F.need(session.summaries[selected] == verified, "SESSION_SNAPSHOT_CONFLICT")
        elif operation == "candidates":
            C.verify_page(session.summaries[selected], ticket["request"], response, check_budget=guard)
        else:
            verified = Q.verify_page(coverage.summary, ticket["request"], response)
            for row in response["examined"]:
                key = row["record"]["object_id"]
                binding = ((verified["partition"], row["ordinal"]), F.record_id(row["record"]))
                F.need(key not in coverage.observed or coverage.observed[key] == binding,
                       "CROSS_PAGE_OBJECT_CONSISTENCY")
        guard()
    except _LocalGuardFailure as failure:
        raise failure.error
    except ValueError as error:
        # This region contains only bounded pure parsing/verification and the
        # guarded liveness callback, not mutation, transport or issuer work.
        return _InvalidMetadata(type(error).__name__+":"+str(error)[:200])
    return None


async def _send(client, provider, bound, ticket, route, attempt_timeout_ms):
    session = bound["session"]
    try:
        R._unchanged(client, bound)
        if client._clock() >= client._expiries[provider]:
            answer = R._Refusal("CONTACT_EXPIRED")
        else:
            remaining = min(ticket["remaining_wall_ms"],
                            int((session.deadline-session.clock())*1000))
            F.need(remaining >= 1, "SEARCH_ORIGINAL_DEADLINE")
            answer = await R._exchange(bound["endpoint"], route, ticket["request"],
                ticket["max_reply_bytes"], min(attempt_timeout_ms, remaining))
        R._unchanged(client, bound)
    except BaseException:
        client.http["failed_requests"] += 1
        R._abandon(session, ticket)
        raise
    if type(answer) is R._Refusal:
        reason = answer.reason
        client.http["failed_requests"] += 1
    else:
        F.need(type(answer) is dict, "SEARCH_EXCHANGE_RESPONSE")
        client.http["completed_requests"] += 1
        client.http["header_bytes"] += answer["header_bytes"]
        client.http["actual_request_bytes"] += answer["request_bytes"]
        client.http["actual_reply_bytes"] += answer["reply_bytes"]
        if answer["status"] == 200:
            try:
                rejection = _preflight(session, ticket, answer["raw"])
                R._unchanged(client, bound)
            except BaseException:
                # Fatal preflight still settles costs, but never grants recovery.
                R._abandon(session, ticket)
                raise
            if rejection is None:
                # No catch around actual accounting/commit. An unexpected late
                # error must retain the original ordinary owner's fail-stop.
                return session.accept(ticket["ticket"], answer["raw"])
            F.need(type(rejection) is _InvalidMetadata, "SEARCH_PREFLIGHT_RESULT")
            settlement = R._abandon(session, ticket)
            R._unchanged(client, bound)
            return {"schema": SCHEMA, "status": "REFUSED_PROVIDER_ATTEMPT",
                    "provider": provider, "ticket": ticket["ticket"], "operation": ticket["operation"],
                    "reason": "INVALID_METADATA", "validation_error": rejection.code,
                    "settlement": settlement, "mathematical_acceptance": False, "global_complete": False}
        reason = "HTTP_"+str(answer["status"])
    F.need(reason in R.REASONS, "SEARCH_REFUSAL_CLASSIFICATION")
    settlement = R._abandon(session, ticket)
    R._unchanged(client, bound)
    return {"schema": R.SCHEMA, "status": "REFUSED_PROVIDER_ATTEMPT", "provider": provider,
            "ticket": ticket["ticket"], "operation": ticket["operation"], "reason": reason,
            "settlement": settlement, "mathematical_acceptance": False, "global_complete": False}


async def offer(client, provider, max_bytes=1048576, *, max_expanded_bytes=1048576,
                max_age_ms=60000, attempt_timeout_ms=5000):
    F.uint(attempt_timeout_ms, 1, 60000, "SEARCH_ATTEMPT_TIMEOUT")
    bound = R._binding(client, provider)
    ticket = bound["session"].begin_offer(bound["endpoint"].label, max_bytes,
        max_expanded_bytes=max_expanded_bytes, max_age_ms=max_age_ms)
    return await _send(client, provider, bound, ticket, H.OFFER_ROUTE, attempt_timeout_ms)


async def page(client, provider, snapshot_id, partition, start, limits, *,
               candidates_only=True, attempt_timeout_ms=5000):
    F.need(type(candidates_only) is bool, "SEARCH_CANDIDATES_BOOL")
    F.uint(attempt_timeout_ms, 1, 60000, "SEARCH_ATTEMPT_TIMEOUT")
    bound = R._binding(client, provider)
    method = bound["session"].begin_candidates if candidates_only else bound["session"].begin_page
    ticket = method(bound["endpoint"].label, snapshot_id, partition, start, limits)
    route = H.CANDIDATE_ROUTE if candidates_only else "/v5/discovery/page"
    return await _send(client, provider, bound, ticket, route, attempt_timeout_ms)

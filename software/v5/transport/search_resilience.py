"""Settled pre-accept peer refusals inside one existing located search session.

No retry, session replacement, metadata-error recovery or mathematical authority.
The ordinary owner serializes calls and keeps its original grant/source checks.
Unlike the frozen exchange, this path requires observed socket closure before a
peer refusal can return normally. Cleanup uncertainty and cancellation are fatal.
"""
from __future__ import annotations

import asyncio
from copy import deepcopy
from dataclasses import dataclass
import ssl
import time

from discovery import formal_features as F
from discovery.search_session import SearchSession
from location import protocol as P
from location import workflow as L
from . import http_provider as H

SCHEMA = "DMKN_SEARCH_SETTLED_REFUSAL_V1"
HTTP_FIELDS = ("completed_requests", "failed_requests", "header_bytes",
               "actual_request_bytes", "actual_reply_bytes")
HEADER_REFUSALS = frozenset(("HTTP_HEADER_BYTES", "HTTP_HEADER_LINES",
    "HTTP_HEADER_SHAPE", "HTTP_HEADER_NAME", "HTTP_HEADER_DUPLICATE_OR_CONTROL",
    "HTTP_UNSUPPORTED_HEADER", "HTTP_CONTENT_LENGTH", "HTTP_MESSAGE_PROFILE"))
REASONS = frozenset(("CONTACT_EXPIRED", "CONNECTION_REFUSED", "CONNECTION_RESET",
    "BROKEN_PIPE", "ATTEMPT_TIMEOUT", "PEER_EOF", "HTTP_PROTOCOL",
    "HTTP_400", "HTTP_404", "HTTP_503"))


class SearchCleanupError(RuntimeError):
    """No safe continuation: the transport's shutdown was not observed cleanly."""


class _PeerProtocolError(Exception):
    pass


@dataclass(frozen=True)
class _Refusal:
    reason: str


def _binding(client, provider):
    """Check the exact existing owner objects; preserve their query and budget."""
    F.need(type(client) is L._LocatedSearchClient
           and type(client.session) is SearchSession
           and type(client._policy) is P.OwnerEgressPolicy,
           "SEARCH_EXACT_LOCATED_OWNER")
    session = client.session
    session._live()
    F.need(client._clock is session.clock, "SEARCH_ORIGINAL_CLOCK")
    F.need(type(client.endpoints) is dict and type(client._adopted_endpoints) is dict
           and client.endpoints == client._adopted_endpoints,
           "LOCATION_CONTACT_BINDING_CHANGED")
    F.need(type(provider) is str and provider in client.endpoints,
           "ENDPOINT_NOT_CONFIGURED")
    F.need(type(client._expiries) is dict and provider in client._expiries,
           "SEARCH_ORIGINAL_CONTACT_EXPIRY")
    endpoint = client.endpoints[provider]
    F.need(type(endpoint) is H.Endpoint, "SEARCH_EXACT_ENDPOINT")
    checked = client._policy.endpoint({"host": endpoint.host, "port": endpoint.port,
        "tls": endpoint.tls, "server_name": endpoint.server_name})
    F.need(endpoint == checked, "LOCATION_CONTACT_POLICY_CHANGED")
    F.fields(client.http, HTTP_FIELDS)
    F.need(all(type(value) is int and value >= 0 for value in client.http.values()),
           "SEARCH_HTTP_ACCOUNTING")
    F.need(type(session.pending) is dict and not session.pending
           and all(value == 0 for value in session.reserved.values()),
           "SEARCH_SERIALIZED_SETTLED_SESSION_REQUIRED")
    return {"session": session, "clock": session.clock, "query": session._query,
            "deadline": session.deadline, "limits": deepcopy(session.limits),
            "endpoints": dict(client.endpoints), "adopted": dict(client._adopted_endpoints),
            "expiries": dict(client._expiries), "policy": client._policy,
            "policy_state": (client._policy._mode, client._policy._ports,
                             client._policy._tests, deepcopy(client._policy._config)),
            "http": client.http, "endpoint": endpoint}


def _unchanged(client, bound):
    session, policy = bound["session"], bound["policy"]
    F.need(type(client) is L._LocatedSearchClient and client.session is session
           and type(session) is SearchSession and client._clock is bound["clock"]
           and session.clock is bound["clock"] and session._query == bound["query"]
           and session.deadline == bound["deadline"] and session.limits == bound["limits"],
           "SEARCH_OWNER_OR_BUDGET_CHANGED")
    F.need(client.endpoints == bound["endpoints"]
           and client._adopted_endpoints == bound["adopted"]
           and client._expiries == bound["expiries"] and client._policy is policy
           and (policy._mode, policy._ports, policy._tests, policy._config) == bound["policy_state"],
           "SEARCH_CONTACT_OR_POLICY_CHANGED")
    F.need(client.http is bound["http"], "SEARCH_HTTP_OWNER_CHANGED")
    session._live()


def _abandon(session, ticket):
    """Settle exactly the original ticket, including every full reservation."""
    F.need(set(session.pending) == {ticket["ticket"]}, "SEARCH_EXACT_PENDING_TICKET")
    held = session.pending[ticket["ticket"]]
    F.need({key: value for key, value in held.items() if key != "reservation"} == ticket,
           "SEARCH_TICKET_BINDING_CHANGED")
    reservation = deepcopy(held["reservation"])
    F.need(session.reserved == reservation, "SEARCH_EXACT_PENDING_RESERVATION")
    expected = dict(session.used)
    expected["bytes"] += ticket["max_reply_bytes"]
    expected["examined"] += reservation["examined"]
    expected["candidates"] += reservation["candidates"]
    scan = session.candidate_scan_charges
    if ticket["operation"] == "candidates": scan += reservation["examined"]
    result = session.abandon(ticket["ticket"])
    F.need(result == {"status": "ABANDONED_CONSERVATIVELY_CHARGED",
                      "ticket": ticket["ticket"]}
           and session.pending == {} and all(value == 0 for value in session.reserved.values())
           and session.used == expected and session.candidate_scan_charges == scan,
           "SEARCH_SETTLEMENT_ACCOUNTING")
    return result["status"]


async def _response(reader, writer, head, raw, maximum):
    await H._write(writer, head)
    await H._write(writer, raw)
    try:
        first, headers, count, incoming = await H._headers(reader)
    except UnicodeDecodeError as error:
        raise _PeerProtocolError() from error
    except ValueError as error:
        if type(error) is ValueError and error.args in [(code,) for code in HEADER_REFUSALS]:
            raise _PeerProtocolError() from error
        raise
    parts = first.split(" ")
    if not (len(parts) >= 3 and parts[0] == "HTTP/1.1"
            and parts[1] in ("200", "400", "404", "503")
            and "host" not in headers and count <= maximum):
        raise _PeerProtocolError()
    body = await H._body(reader, count)
    if await reader.read(1) != b"": raise _PeerProtocolError()
    return {"status": int(parts[1]), "raw": body, "request_bytes": len(raw),
            "reply_bytes": len(body), "header_bytes": len(head)+incoming}


async def _exchange(endpoint, route, request, maximum, timeout_ms):
    """One bounded connection; return only after clean observed stream closure.

    A connect timeout/reset before a writer is returned remains fatal: there is
    no acquired stream here with which to demonstrate shutdown. Refused connect
    uses asyncio's failed-connect cleanup contract. Other recoverable I/O errors
    occur only after obtaining a writer, followed by successful wait_closed.
    """
    endpoint.validate()
    F.need(route in (H.OFFER_ROUTE, H.CANDIDATE_ROUTE, "/v5/discovery/page"),
           "SEARCH_READ_ONLY_ROUTE")
    F.uint(maximum, 1, H.ROUTES[route], "HTTP_REPLY_CAP")
    F.uint(timeout_ms, 1, 60000, "HTTP_TIMEOUT")
    raw = F.compact(request)
    F.need(0 < len(raw) <= H.REQUEST_MAX, "HTTP_REQUEST_BYTES")
    host = "["+endpoint.host+"]" if ":" in endpoint.host else endpoint.host
    head = H._header("POST "+route+" HTTP/1.1", len(raw), host+":"+str(endpoint.port))
    context = None
    if endpoint.tls:
        context = ssl.create_default_context(cafile=endpoint.ca_file)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
    writer, outcome = None, None
    started = time.monotonic()
    timer = asyncio.timeout(timeout_ms/1000)
    try:
        try:
            async with timer:
                kwargs = {"ssl": context, "limit": H.HEADER_MAX}
                if endpoint.tls:
                    kwargs.update(server_hostname=endpoint.server_name or endpoint.host,
                        ssl_handshake_timeout=timeout_ms/1000, ssl_shutdown_timeout=1)
                try:
                    reader, writer = await asyncio.open_connection(endpoint.host, endpoint.port, **kwargs)
                except ConnectionRefusedError:
                    outcome = _Refusal("CONNECTION_REFUSED")
                else:
                    try:
                        outcome = await _response(reader, writer, head, raw, maximum)
                    except ConnectionResetError:
                        outcome = _Refusal("CONNECTION_RESET")
                    except BrokenPipeError:
                        outcome = _Refusal("BROKEN_PIPE")
                    except asyncio.IncompleteReadError:
                        outcome = _Refusal("PEER_EOF")
                    except (asyncio.LimitOverrunError, _PeerProtocolError):
                        outcome = _Refusal("HTTP_PROTOCOL")
        except TimeoutError:
            # Do not reinterpret a random TimeoutError from local code, nor an
            # unreturned connect/handshake transport, as a settled read timeout.
            if not timer.expired() or writer is None: raise
            outcome = _Refusal("ATTEMPT_TIMEOUT")
    finally:
        if writer is not None:
            try:
                writer.close()
                async with asyncio.timeout(1):
                    await writer.wait_closed()
            except asyncio.CancelledError:
                raise
            except Exception as error:
                raise SearchCleanupError("SEARCH_SOCKET_CLOSURE_UNCERTAIN") from error
    if type(outcome) is dict:
        outcome["elapsed_ms"] = int((time.monotonic()-started)*1000)
    F.need(type(outcome) in (dict, _Refusal), "SEARCH_EXCHANGE_OUTCOME")
    return outcome


async def _send(client, provider, bound, ticket, route, attempt_timeout_ms):
    session = bound["session"]
    try:
        _unchanged(client, bound)
        if client._clock() >= client._expiries[provider]:
            answer = _Refusal("CONTACT_EXPIRED")
        else:
            remaining = min(ticket["remaining_wall_ms"],
                            int((session.deadline-session.clock())*1000))
            F.need(remaining >= 1, "SEARCH_ORIGINAL_DEADLINE")
            answer = await _exchange(bound["endpoint"], route, ticket["request"],
                                     ticket["max_reply_bytes"], min(attempt_timeout_ms, remaining))
        _unchanged(client, bound)
    except BaseException:
        # Settlement is cleanup, not recovery. Unexpected errors/cancellation
        # retain the full charge and still escape to the ordinary fail-stop owner.
        client.http["failed_requests"] += 1
        _abandon(session, ticket)
        raise
    if type(answer) is _Refusal:
        reason = answer.reason
        client.http["failed_requests"] += 1
    else:
        F.need(type(answer) is dict, "SEARCH_EXCHANGE_RESPONSE")
        client.http["completed_requests"] += 1
        client.http["header_bytes"] += answer["header_bytes"]
        client.http["actual_request_bytes"] += answer["request_bytes"]
        client.http["actual_reply_bytes"] += answer["reply_bytes"]
        if answer["status"] == 200:
            # No recovery catch surrounds accept: malformed metadata, invalid
            # proofs, conflicts and its accounting failures remain fatal.
            return session.accept(ticket["ticket"], answer["raw"])
        reason = "HTTP_"+str(answer["status"])
    F.need(reason in REASONS, "SEARCH_REFUSAL_CLASSIFICATION")
    settlement = _abandon(session, ticket)
    _unchanged(client, bound)
    return {"schema": SCHEMA, "status": "REFUSED_PROVIDER_ATTEMPT", "provider": provider,
            "ticket": ticket["ticket"], "operation": ticket["operation"], "reason": reason,
            "settlement": settlement, "mathematical_acceptance": False, "global_complete": False}


async def offer(client, provider, max_bytes=1048576, *, max_expanded_bytes=1048576,
                max_age_ms=60000, attempt_timeout_ms=5000):
    """One explicit offer attempt on an existing located session; never retry."""
    F.uint(attempt_timeout_ms, 1, 60000, "SEARCH_ATTEMPT_TIMEOUT")
    bound = _binding(client, provider)
    ticket = bound["session"].begin_offer(bound["endpoint"].label, max_bytes,
        max_expanded_bytes=max_expanded_bytes, max_age_ms=max_age_ms)
    return await _send(client, provider, bound, ticket, H.OFFER_ROUTE, attempt_timeout_ms)


async def page(client, provider, snapshot_id, partition, start, limits, *,
               candidates_only=True, attempt_timeout_ms=5000):
    """One existing candidate/interval request, with unchanged authentication."""
    F.need(type(candidates_only) is bool, "SEARCH_CANDIDATES_BOOL")
    F.uint(attempt_timeout_ms, 1, 60000, "SEARCH_ATTEMPT_TIMEOUT")
    bound = _binding(client, provider)
    method = bound["session"].begin_candidates if candidates_only else bound["session"].begin_page
    ticket = method(bound["endpoint"].label, snapshot_id, partition, start, limits)
    route = H.CANDIDATE_ROUTE if candidates_only else "/v5/discovery/page"
    return await _send(client, provider, bound, ticket, route, attempt_timeout_ms)

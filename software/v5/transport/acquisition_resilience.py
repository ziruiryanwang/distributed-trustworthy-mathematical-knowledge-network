"""One settled body read on an existing structural owner and original budget.

No retry, new contact, custody write, mathematical authority or error-string
recovery. Successful HTTP payload validation and every local error stay fatal.
"""
import asyncio
from copy import deepcopy
from dataclasses import dataclass
import ssl
import time

from custody.module_store import permitted_hashes, validate_body
from discovery import formal_features as F
from evidence_network.transport import EvidenceAcquisition
from location import protocol as P
from . import http_provider as H
from . import search_resilience as R
from .located_receipts import _ExpiringContact
from .receipt_client import AcquisitionBudget, _SharedAcquisition

SCHEMA = "DMKN_SEMANTIC_BODY_ATTEMPT_V1"
ROUTE = "/v5/modules/body"
REASONS = frozenset(("CONNECTION_REFUSED", "PEER_EOF", "HTTP_404", "HTTP_503",
                     "ATTEMPT_TIMEOUT", "CONNECTION_RESET", "BROKEN_PIPE"))
_response = R._response


class BodyCleanupError(RuntimeError):
    """The local transport did not establish clean shutdown; never recover."""


@dataclass(frozen=True)
class _Unavailable:
    reason: str


async def _exchange(endpoint, request, maximum, timeout_ms):
    """Return only after clean closure; malformed HTTP remains an exception."""
    F.need(_response is R._response, "BODY_ATTEMPT_RESPONSE_SYMBOL_CHANGED")
    endpoint.validate()
    F.uint(maximum, 1, H.MODULE_MAX, "BODY_ATTEMPT_BYTES")
    F.uint(timeout_ms, 1, 60000, "BODY_ATTEMPT_TIMEOUT")
    raw = F.compact(request)
    F.need(0 < len(raw) <= H.REQUEST_MAX, "BODY_ATTEMPT_REQUEST_BYTES")
    host = "["+endpoint.host+"]" if ":" in endpoint.host else endpoint.host
    head = H._header("POST "+ROUTE+" HTTP/1.1", len(raw), host+":"+str(endpoint.port))
    context = None
    if endpoint.tls:
        context = ssl.create_default_context(cafile=endpoint.ca_file)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
    writer = outcome = None
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
                    # asyncio's failed-connect contract owns the unreturned socket.
                    outcome = _Unavailable("CONNECTION_REFUSED")
                else:
                    try:
                        # This parser has no route/session dependency. Protocol
                        # errors intentionally escape; only interrupted I/O settles.
                        outcome = await _response(reader, writer, head, raw, maximum)
                    except ConnectionResetError:
                        outcome = _Unavailable("CONNECTION_RESET")
                    except BrokenPipeError:
                        outcome = _Unavailable("BROKEN_PIPE")
                    except asyncio.IncompleteReadError:
                        outcome = _Unavailable("PEER_EOF")
        except TimeoutError:
            if not timer.expired() or writer is None:
                raise
            outcome = _Unavailable("ATTEMPT_TIMEOUT")
    finally:
        if writer is not None:
            try:
                writer.close()
                async with asyncio.timeout(1):
                    await writer.wait_closed()
            except asyncio.CancelledError:
                raise
            except Exception as error:
                raise BodyCleanupError("BODY_SOCKET_CLOSURE_UNCERTAIN") from error
    F.need(type(outcome) in (dict, _Unavailable), "BODY_ATTEMPT_EXCHANGE_OUTCOME")
    return outcome


def _binding(acquisition, provider):
    # The ordinary direct-contact client adds an exact private issuance guard.
    # Local import avoids the workspace/direct-contact construction cycle.
    from client.direct_contacts import _Contact
    F.need(type(acquisition) is EvidenceAcquisition, "BODY_ATTEMPT_EXACT_ACQUISITION")
    acquisition._active()
    structural, budget = acquisition.structural, acquisition.budget
    F.need(type(structural) is _SharedAcquisition and type(budget) is AcquisitionBudget
           and structural.budget is budget and structural.adapter is acquisition.adapter
           and structural.local_custody is None and acquisition.verifier is None,
           "BODY_ATTEMPT_ORIGINAL_OWNERS")
    F.need(type(provider) is str and provider in acquisition.endpoints
           and provider in structural.endpoints, "BODY_ATTEMPT_CONFIGURED_SUPPLIER")
    contact = acquisition.endpoints[provider]
    F.need(type(contact) in (_ExpiringContact, _Contact) and contact is structural.endpoints[provider]
           and contact._budget is budget and type(contact._policy) is P.OwnerEgressPolicy,
           "BODY_ATTEMPT_EXACT_CONTACT")
    F.need(budget.pending is None and structural.inflight == 0 and structural.reserved_bytes == 0,
           "BODY_ATTEMPT_SERIALIZED_SETTLED_OWNER")
    F.need(structural.request_cap == budget.limits["requests"]
           and structural.byte_cap == budget.limits["reply_bytes"]
           and structural.deadline <= budget.deadline, "BODY_ATTEMPT_ORIGINAL_CAPS")
    structural._deadline()
    return {"acquisition": acquisition, "structural": structural, "budget": budget,
            "adapter": acquisition.adapter, "modules": acquisition.modules,
            "packets": acquisition.packets, "handoff": acquisition._handoff,
            "search": acquisition._search, "contact": contact,
            "contact_type": type(contact), "direct_binding": getattr(contact, "_binding", None),
            "endpoints": dict(acquisition.endpoints), "structural_endpoints": dict(structural.endpoints),
            "endpoint": contact._endpoint, "expires": contact._expires,
            "policy": contact._policy, "policy_state": deepcopy(contact._policy.__dict__),
            "deadline": budget.deadline, "structural_deadline": structural.deadline,
            "limits": dict(budget.limits), "request_cap": structural.request_cap,
            "byte_cap": structural.byte_cap}


def _unchanged(bound):
    F.need(_response is R._response, "BODY_ATTEMPT_RESPONSE_SYMBOL_CHANGED")
    a, s, b, c = (bound[key] for key in ("acquisition", "structural", "budget", "contact"))
    F.need(type(a) is EvidenceAcquisition and type(s) is _SharedAcquisition
           and type(b) is AcquisitionBudget and type(c) is bound["contact_type"]
           and a.structural is s and a.budget is b and s.budget is b
           and a.adapter is s.adapter is bound["adapter"]
           and a.modules is bound["modules"] and a.packets is bound["packets"]
           and a._handoff is bound["handoff"] and a._search is bound["search"]
           and s.local_custody is None and a.verifier is None,
           "BODY_ATTEMPT_OWNER_CHANGED")
    F.need(a.endpoints == bound["endpoints"] and s.endpoints == bound["structural_endpoints"]
           and getattr(c, "_binding", None) is bound["direct_binding"]
           and c._endpoint is bound["endpoint"] and c._budget is b
           and c._expires == bound["expires"] and c._policy is bound["policy"]
           and c._policy.__dict__ == bound["policy_state"], "BODY_ATTEMPT_CONTACT_CHANGED")
    F.need(b.deadline == bound["deadline"] and b.limits == bound["limits"]
           and s.deadline == bound["structural_deadline"]
           and s.request_cap == bound["request_cap"] and s.byte_cap == bound["byte_cap"],
           "BODY_ATTEMPT_ALLOWANCE_CHANGED")
    a._active(); s._deadline(); c.validate()


async def try_body(acquisition, provider, resolved, digest, max_bytes, *, attempt_timeout_ms=5000):
    """Validate one response or settle unavailability; never commit custody.

    The facade's serialized action owns this call. Both existing acquisition
    accounting layers advance; no replacement owner or shadow allowance exists.
    """
    F.uint(max_bytes, 1, H.MODULE_MAX, "BODY_ATTEMPT_BYTES")
    F.uint(attempt_timeout_ms, 1, 60000, "BODY_ATTEMPT_TIMEOUT")
    bound = _binding(acquisition, provider)
    s, b = bound["structural"], bound["budget"]
    selected = deepcopy(resolved)
    loc, descriptor = selected["locator"], selected["descriptor"]
    F.need(digest in permitted_hashes(descriptor), "ACQUISITION_BODY_NOT_COMMITTED")
    request = {"module_id": loc["module_id"], "relative_name": deepcopy(loc["relative_name"]),
               "universes": descriptor["universes"], "body_hash": F.hexid(digest)}
    before = {key: getattr(s, key) for key in ("used_requests", "used_bytes", "failures",
        "actual_reply_bytes", "header_bytes", "request_body_upper_bound", "header_upper_bound")}
    shared_used, sequence = dict(b.used), b.sequence
    ticket = b.begin(max_bytes)
    entered, failed, charged, result = False, True, max_bytes, None
    observed_bytes = observed_headers = 0
    try:
        F.need(s.used_requests < s.request_cap and s.used_bytes+max_bytes <= s.byte_cap,
               "ACQUISITION_BUDGET")
        s.used_requests += 1; s.reserved_bytes += max_bytes; s.inflight += 1; entered = True
        s.request_body_upper_bound += H.REQUEST_MAX
        s.header_upper_bound += 2*H.HEADER_MAX
        _unchanged(bound)
        remaining = min(attempt_timeout_ms, b.remaining_ms(),
                        int((s.deadline-time.monotonic())*1000))
        F.need(remaining >= 1, "BODY_ATTEMPT_ORIGINAL_DEADLINE")
        answer = await _exchange(bound["contact"], request, max_bytes, remaining)
        _unchanged(bound)
        if type(answer) is _Unavailable:
            reason = answer.reason
        else:
            F.need(type(answer) is dict, "BODY_ATTEMPT_EXCHANGE_OUTCOME")
            observed_bytes, observed_headers = len(answer["raw"]), answer["header_bytes"]
            s.actual_reply_bytes += observed_bytes; s.header_bytes += observed_headers
            if answer["status"] == 200:
                charged = len(answer["raw"])
                value = s.adapter.codec.parse_json(answer["raw"])
                F.need(s.adapter.codec.canonical(value) == answer["raw"], "ACQUISITION_CANONICAL")
                validate_body(s.adapter.codec, loc["module_id"], loc["relative_name"],
                              descriptor, value, digest)
                _unchanged(bound)
                result = {"status": "BODY_VALIDATED", "body": value,
                          "assurance": "EXACT_DESCRIPTOR_COMMITTED_BODY", "mathematical_acceptance": False}
                failed = False
                reason = None
            else:
                F.need(answer["status"] in (404, 503), "BODY_ATTEMPT_UNRECOVERABLE_HTTP_STATUS")
                reason = "HTTP_"+str(answer["status"])
        if result is None:
            F.need(reason in REASONS, "BODY_ATTEMPT_REFUSAL_KIND")
            result = {"schema": SCHEMA, "status": "UNAVAILABLE_AT_SELECTED_SUPPLIER",
                      "supplier": provider, "reason": reason,
                      "request": deepcopy(request),
                      "settlement": "FULL_REPLY_RESERVATION_CHARGED",
                      "global_complete": False, "mathematical_acceptance": False}
    finally:
        if entered:
            s.reserved_bytes -= max_bytes; s.inflight -= 1; s.used_bytes += charged
            if failed: s.failures += 1
        b.settle(ticket, charged if entered and charged > 0 else None)
    _unchanged(bound)
    expected = dict(shared_used)
    expected["requests"] += 1; expected["reply_bytes"] += charged if charged > 0 else max_bytes
    F.need(b.used == expected and b.sequence == sequence+1 and b.pending is None
           and s.inflight == s.reserved_bytes == 0
           and s.used_requests == before["used_requests"]+1 and s.used_bytes == before["used_bytes"]+charged
           and s.failures == before["failures"]+int(failed)
           and s.actual_reply_bytes == before["actual_reply_bytes"]+observed_bytes
           and s.header_bytes == before["header_bytes"]+observed_headers
           and s.request_body_upper_bound == before["request_body_upper_bound"]+H.REQUEST_MAX
           and s.header_upper_bound == before["header_upper_bound"]+2*H.HEADER_MAX,
           "BODY_ATTEMPT_SETTLEMENT_BINDING")
    return result

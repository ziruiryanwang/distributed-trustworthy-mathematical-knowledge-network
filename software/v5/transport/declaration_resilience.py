"""One settled exact-declaration read; original owners, contacts and budgets.

Reuses the selected body transport's binding and HTTP response machinery.
Only pre-validation availability failures settle normally. No retry, custody,
candidate, new contact or mathematical authority is created here.
"""
import asyncio
from copy import deepcopy
import ssl
import time

from discovery import formal_features as F
from . import acquisition_resilience as AR
from . import http_provider as H

SCHEMA = "DMKN_SEMANTIC_DECLARATION_ATTEMPT_V1"
ROUTE = "/v5/modules/group"
_binding, _unchanged, _response = AR._binding, AR._unchanged, AR._response
_Unavailable = AR._Unavailable


class DeclarationCleanupError(RuntimeError):
    """Socket shutdown is uncertain; no continuation is permitted."""


def _sources():
    F.need(_binding is AR._binding and _unchanged is AR._unchanged
           and _response is AR._response and _Unavailable is AR._Unavailable,
           "DECLARATION_ATTEMPT_SYMBOL_CHANGED")


async def _exchange(endpoint, request, maximum, timeout_ms):
    """The existing settled body exchange with the fixed declaration route.

    Its body route cannot be rebound or monkey-patched for this operation.
    The common parser still treats malformed HTTP as fatal, not unavailable.
    """
    _sources(); endpoint.validate()
    F.uint(maximum, 1, H.MODULE_MAX, "DECLARATION_ATTEMPT_BYTES")
    F.uint(timeout_ms, 1, 60000, "DECLARATION_ATTEMPT_TIMEOUT")
    raw = F.compact(request)
    F.need(0 < len(raw) <= H.REQUEST_MAX, "DECLARATION_ATTEMPT_REQUEST_BYTES")
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
                    outcome = _Unavailable("CONNECTION_REFUSED")
                else:
                    try:
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
                raise DeclarationCleanupError("DECLARATION_SOCKET_CLOSURE_UNCERTAIN") from error
    F.need(type(outcome) in (dict, _Unavailable), "DECLARATION_ATTEMPT_EXCHANGE_OUTCOME")
    return outcome


async def try_declaration(acquisition, provider, module, relative_name, max_bytes, *,
                          attempt_timeout_ms=5000):
    """Validate an exact committed opening or settle one supplier's absence.

    Returns only structural data. The facade owns ordinary custody/readback and
    candidate issuance, outside all recoverable transport classification.
    """
    _sources()
    F.uint(max_bytes, 1, H.MODULE_MAX, "DECLARATION_ATTEMPT_BYTES")
    F.uint(attempt_timeout_ms, 1, 60000, "DECLARATION_ATTEMPT_TIMEOUT")
    bound = _binding(acquisition, provider)
    s, b = bound["structural"], bound["budget"]
    F.hexid(module); s.adapter.codec.validate_name(relative_name)
    request = {"module_id": module, "relative_name": deepcopy(relative_name), "group_index": None}
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
        F.need(remaining >= 1, "DECLARATION_ATTEMPT_ORIGINAL_DEADLINE")
        answer = await _exchange(bound["contact"], request, max_bytes, remaining)
        _sources(); _unchanged(bound)
        if type(answer) is _Unavailable:
            reason = answer.reason
        else:
            F.need(type(answer) is dict, "DECLARATION_ATTEMPT_EXCHANGE_OUTCOME")
            observed_bytes, observed_headers = len(answer["raw"]), answer["header_bytes"]
            s.actual_reply_bytes += observed_bytes; s.header_bytes += observed_headers
            if answer["status"] == 200:
                charged = len(answer["raw"])
                opening = s.adapter.codec.parse_json(answer["raw"])
                F.need(s.adapter.codec.canonical(opening) == answer["raw"], "ACQUISITION_CANONICAL")
                raw = s.adapter.encode_opening(module, request["relative_name"], opening)
                described = s.adapter.describe(raw)
                resolved = {**s.adapter.resolve(described["record"], raw), "opening": opening}
                F.need(resolved["locator"]["module_id"] == module
                       and resolved["locator"]["relative_name"] == request["relative_name"],
                       "DECLARATION_ATTEMPT_EXACT_NAME_BINDING")
                _unchanged(bound)
                result = {"status": "DECLARATION_VALIDATED", "resolved": resolved,
                          "mathematical_acceptance": False}
                failed, reason = False, None
            else:
                F.need(answer["status"] in (404, 503), "DECLARATION_ATTEMPT_UNRECOVERABLE_HTTP_STATUS")
                reason = "HTTP_"+str(answer["status"])
        if result is None:
            F.need(reason in AR.REASONS, "DECLARATION_ATTEMPT_REFUSAL_KIND")
            result = {"schema": SCHEMA, "status": "UNAVAILABLE_AT_SELECTED_SUPPLIER",
                "supplier": provider, "reason": reason, "request": deepcopy(request),
                "settlement": "FULL_REPLY_RESERVATION_CHARGED", "global_complete": False,
                "mathematical_acceptance": False}
    finally:
        if entered:
            s.reserved_bytes -= max_bytes; s.inflight -= 1; s.used_bytes += charged
            if failed: s.failures += 1
        b.settle(ticket, charged if entered and charged > 0 else None)
    _sources(); _unchanged(bound)
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
           "DECLARATION_ATTEMPT_SETTLEMENT_BINDING")
    return result

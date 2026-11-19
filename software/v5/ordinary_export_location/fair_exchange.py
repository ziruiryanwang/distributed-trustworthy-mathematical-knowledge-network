"""One settled discovery or ordinary read using the existing HTTP wire codec.

No DNS, redirects, retries, source execution or mathematical acceptance. The
async attempt timer is not a preemptive bound on local TLS/CA or CPU work.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
import ipaddress
import math
import socket
import ssl
import time

from discovery import formal_features as F
from . import http_provider as H

CLOSE_SECONDS = 1
HEADER_REFUSALS = frozenset(("HTTP_HEADER_BYTES", "HTTP_HEADER_LINES",
    "HTTP_HEADER_SHAPE", "HTTP_HEADER_NAME", "HTTP_HEADER_DUPLICATE_OR_CONTROL",
    "HTTP_UNSUPPORTED_HEADER", "HTTP_CONTENT_LENGTH", "HTTP_MESSAGE_PROFILE"))


@dataclass(frozen=True)
class SettledRefusal:
    reason: str


class UnsettledTransportError(RuntimeError):
    """The caller must not recover or dial another provider after this error."""


class _PeerProtocolError(Exception):
    pass


def _numeric_address(endpoint):
    address = ipaddress.ip_address(endpoint.host)
    if address.version == 4:
        return socket.AF_INET, (str(address), endpoint.port)
    scope = address.scope_id
    scope_id = 0
    if scope is not None:
        # Resolve only a local interface name, never a host through DNS.
        scope_id = (int(scope) if scope.isascii() and scope.isdecimal()
                    else socket.if_nametoindex(scope))
        F.uint(scope_id, 0, 0xffffffff, "ENDPOINT_SCOPE")
    return socket.AF_INET6, (str(address).split("%", 1)[0], endpoint.port, 0, scope_id)


def _close_owned_socket(sock):
    try:
        sock.close()
        if sock.fileno() != -1:
            raise RuntimeError("FAIR_RAW_SOCKET_STILL_OPEN")
    except Exception as error:
        raise UnsettledTransportError("FAIR_RAW_SOCKET_CLOSURE_UNCERTAIN") from error


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
    if not (len(parts) >= 3 and parts[0] == "HTTP/1.1" and
            parts[1] in ("200", "400", "404", "503") and
            "host" not in headers and count <= maximum):
        raise _PeerProtocolError()
    body = await H._body(reader, count)
    if await reader.read(1) != b"":
        raise _PeerProtocolError()
    return dict(status=int(parts[1]), raw=body, request_bytes=len(raw),
                reply_bytes=len(body), header_bytes=len(head)+incoming)


async def exchange(endpoint, route, request, maximum, timeout_ms, *, absolute_deadline=None):
    """Return raw response or settled refusal; unconfirmed cleanup is fatal.

    Known TCP connect failures require successful close of the owned raw socket
    and an invalid descriptor. After stream handoff, no-writer failures remain
    fatal; other recoverable I/O failures require successful writer.wait_closed.
    External cancellation and unknown local failures are never downgraded.
    """
    F.need(type(endpoint) is H.Endpoint, "FAIR_EXACT_ENDPOINT")
    endpoint.validate()
    F.need(route in (H.OFFER_ROUTE, H.CANDIDATE_ROUTE, H.SPARSE_CANDIDATE_ROUTE,
                     H.CONTACT_DIRECTORY_ROUTE, H.ORDINARY_PREVIEW_ROUTE,
                     H.ORDINARY_LOCATOR_ROUTE, H.ORDINARY_EVIDENCE_ROUTE,
                     H.AUTHORING_OFFERS_ROUTE, H.EXPORT_LOCATION_ROUTE), "FAIR_READ_ONLY_ROUTE")
    F.uint(maximum, 1, H.ROUTES[route], "HTTP_REPLY_CAP")
    F.uint(timeout_ms, 1, 60000, "HTTP_TIMEOUT")
    started = time.monotonic()
    until = started+timeout_ms/1000
    if absolute_deadline is not None:
        F.need(type(absolute_deadline) in (int, float) and math.isfinite(absolute_deadline),
               "FAIR_ABSOLUTE_DEADLINE")
        # Entering this coroutine late cannot renew the caller's original horizon.
        until = min(until, absolute_deadline)
        F.need(started < until, "FAIR_ABSOLUTE_DEADLINE_EXHAUSTED")
    raw = F.compact(request)
    F.need(0 < len(raw) <= H.REQUEST_MAX, "HTTP_REQUEST_BYTES")
    host = "["+endpoint.host+"]" if ":" in endpoint.host else endpoint.host
    head = H._header("POST "+route+" HTTP/1.1", len(raw), host+":"+str(endpoint.port))
    context = None
    if endpoint.tls:
        context = ssl.create_default_context(cafile=endpoint.ca_file)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
    family, address = _numeric_address(endpoint)
    remaining = until-time.monotonic()
    F.need(remaining > 0, "FAIR_LOCAL_ATTEMPT_SETUP_EXHAUSTED")
    sock, writer, outcome, cancellation = None, None, None, None
    transferred = False
    timer = asyncio.timeout_at(until)
    try:
        try:
            async with timer:
                sock = socket.socket(family, socket.SOCK_STREAM, socket.IPPROTO_TCP)
                sock.setblocking(False)
                try:
                    await asyncio.get_running_loop().sock_connect(sock, address)
                except ConnectionRefusedError:
                    outcome = SettledRefusal("CONNECTION_REFUSED")
                except ConnectionResetError:
                    outcome = SettledRefusal("CONNECTION_RESET")
                except TimeoutError:
                    outcome = SettledRefusal("ATTEMPT_TIMEOUT")
                else:
                    remaining = until-time.monotonic()
                    if remaining <= 0:
                        outcome = SettledRefusal("ATTEMPT_TIMEOUT")
                    else:
                        kwargs = dict(ssl=context, limit=H.HEADER_MAX)
                        if endpoint.tls:
                            kwargs.update(server_hostname=endpoint.server_name or endpoint.host,
                                ssl_handshake_timeout=remaining, ssl_shutdown_timeout=CLOSE_SECONDS)
                        # Ownership may move before this await returns a writer.
                        transferred = True
                        try:
                            reader, writer = await asyncio.open_connection(sock=sock, **kwargs)
                        except asyncio.CancelledError:
                            raise
                        except Exception as error:
                            raise UnsettledTransportError("FAIR_STREAM_CLOSURE_UNOBSERVED") from error
                        try:
                            outcome = await _response(reader, writer, head, raw, maximum)
                        except ConnectionResetError:
                            outcome = SettledRefusal("CONNECTION_RESET")
                        except BrokenPipeError:
                            outcome = SettledRefusal("BROKEN_PIPE")
                        except asyncio.IncompleteReadError:
                            outcome = SettledRefusal("PEER_EOF")
                        except (asyncio.LimitOverrunError, _PeerProtocolError):
                            outcome = SettledRefusal("HTTP_PROTOCOL")
        except TimeoutError as error:
            if not timer.expired():
                raise
            if writer is None and transferred:
                raise UnsettledTransportError("FAIR_STREAM_CLOSURE_UNOBSERVED") from error
            outcome = SettledRefusal("ATTEMPT_TIMEOUT")
    except asyncio.CancelledError as error:
        cancellation = error
        raise
    finally:
        if sock is not None and not transferred:
            try:
                _close_owned_socket(sock)
            except Exception as error:
                if cancellation is not None:
                    raise cancellation from error
                raise
        if writer is not None:
            try:
                writer.close()
                async with asyncio.timeout(CLOSE_SECONDS):
                    await writer.wait_closed()
            except asyncio.CancelledError:
                raise
            except Exception as error:
                raise UnsettledTransportError("FAIR_SOCKET_CLOSURE_UNCERTAIN") from error
    if type(outcome) is dict:
        outcome["elapsed_ms"] = int((time.monotonic()-started)*1000)
    F.need(type(outcome) in (dict, SettledRefusal), "FAIR_EXCHANGE_OUTCOME")
    return outcome

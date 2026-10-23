"""Small bounded read-only HTTP subset for discovery and typed inert custody.

One request/connection; explicit endpoints; no redirects, compression, remote
writes, source execution or certificate authority. External hard containment is
still required. HTTPS uses verified peer certificates; loopback may use HTTP.
"""
from __future__ import annotations

import asyncio
from copy import deepcopy
from dataclasses import dataclass
import ipaddress
import ssl
import time

from discovery import formal_features as F
from discovery import authenticated_index as A
from discovery import summary_wire as W

HEADER_MAX, REQUEST_MAX, CHUNK = 8192, 16384, 65536
MODULE_MAX = 16 * 1024**2
COMPACT_SUMMARY_ROUTE = "/v5/discovery/summary-compact"
OFFER_ROUTE = "/v5/discovery/offer"
CANDIDATE_ROUTE = "/v5/discovery/candidates"
ORDINARY_PREVIEW_ROUTE = "/v5/ordinary/preview"
ORDINARY_EVIDENCE_ROUTE = "/v5/ordinary/evidence"
ORDINARY_LOCATOR_ROUTE = "/v5/ordinary/locator"
ORDINARY_ROUTES = (ORDINARY_PREVIEW_ROUTE, ORDINARY_EVIDENCE_ROUTE, ORDINARY_LOCATOR_ROUTE)
ROUTES = {"/v5/discovery/summary": 1048576, COMPACT_SUMMARY_ROUTE: 1048576, OFFER_ROUTE: 1048576,
          "/v5/discovery/page": 1048576, CANDIDATE_ROUTE: 1048576,
          "/v5/modules/group": MODULE_MAX, "/v5/modules/body": MODULE_MAX,
          ORDINARY_PREVIEW_ROUTE: 1048576, ORDINARY_EVIDENCE_ROUTE: 8*1024**2,
          ORDINARY_LOCATOR_ROUTE: 1048576}


def _offer_request(request):
    F.fields(request, ("namespace", "features", "max_bytes", "max_expanded_bytes"))
    F.hexid(request["namespace"]); F.validate_features(request["features"], 8)
    F.uint(request["max_bytes"], 1024, 1048576, "OFFER_WIRE_BYTES")
    F.uint(request["max_expanded_bytes"], 1024, 1048576, "OFFER_EXPANDED_BYTES")


@dataclass(frozen=True)
class Endpoint:
    host: str
    port: int
    tls: bool = False
    server_name: str | None = None
    ca_file: str | None = None

    def validate(self):
        F.need(type(self.host) is str and len(self.host) <= 64, "ENDPOINT_HOST")
        address = ipaddress.ip_address(self.host)
        F.need(not address.is_unspecified and not address.is_multicast, "ENDPOINT_ADDRESS")
        F.uint(self.port, 1, 65535, "ENDPOINT_PORT")
        F.need(type(self.tls) is bool and (address.is_loopback or self.tls), "REMOTE_TLS_REQUIRED")
        if self.server_name is not None:
            F.need(self.tls and type(self.server_name) is str and 0 < len(self.server_name) <= 253
                   and all(ord(c) >= 33 and ord(c) < 127 for c in self.server_name), "TLS_SERVER_NAME")
        F.need(self.tls or self.ca_file is None, "HTTP_HAS_NO_CA")
        return self

    @property
    def label(self):
        return ("https://" if self.tls else "http://") + self.host + ":" + str(self.port)


def server_tls(cert_file, key_file):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(cert_file, key_file)
    return context


async def _headers(reader):
    raw = await reader.readuntil(b"\r\n\r\n")
    F.need(len(raw) <= HEADER_MAX, "HTTP_HEADER_BYTES")
    lines = raw[:-4].decode("ascii").split("\r\n")
    F.need(1 <= len(lines) <= 33 and all(lines), "HTTP_HEADER_LINES")
    headers = {}
    for line in lines[1:]:
        F.need(":" in line and not line.startswith((" ", "\t")), "HTTP_HEADER_SHAPE")
        name, value = line.split(":", 1)
        F.need(name and all("a" <= ch.lower() <= "z" or ch == "-" for ch in name), "HTTP_HEADER_NAME")
        name, value = name.lower(), value.strip(" ")
        F.need(name not in headers and all(32 <= ord(ch) < 127 for ch in value), "HTTP_HEADER_DUPLICATE_OR_CONTROL")
        headers[name] = value
    F.need(set(headers) <= {"host", "content-length", "content-type", "connection"}, "HTTP_UNSUPPORTED_HEADER")
    length = headers.get("content-length", "")
    F.need(length.isascii() and length.isdecimal() and 1 <= len(length) <= 9
           and (length == "0" or not length.startswith("0")), "HTTP_CONTENT_LENGTH")
    F.need(headers.get("connection", "").lower() == "close"
           and headers.get("content-type") == "application/json", "HTTP_MESSAGE_PROFILE")
    return lines[0], headers, int(length), len(raw)


async def _body(reader, count):
    result = bytearray()
    while len(result) < count:
        result.extend(await reader.readexactly(min(CHUNK, count-len(result))))
    return bytes(result)


def _header(first, count, host=None):
    return (first + "\r\n" + ("Host: "+host+"\r\n" if host is not None else "")
            + "Content-Length: "+str(count)+"\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n").encode("ascii")


async def _write(writer, raw):
    for start in range(0, len(raw), CHUNK):
        writer.write(raw[start:start+CHUNK]); await writer.drain()


async def exchange(endpoint, route, request, max_reply_bytes, timeout_ms):
    """Return bounded raw body/status and actual payload/header counts; never parse JSON."""
    endpoint.validate(); F.need(route in ROUTES, "HTTP_ROUTE")
    F.uint(max_reply_bytes, 1, ROUTES[route], "HTTP_REPLY_CAP")
    F.uint(timeout_ms, 1, 60000, "HTTP_TIMEOUT")
    raw = F.compact(request); F.need(0 < len(raw) <= REQUEST_MAX, "HTTP_REQUEST_BYTES")
    host = "["+endpoint.host+"]" if ":" in endpoint.host else endpoint.host
    head = _header("POST "+route+" HTTP/1.1", len(raw), host+":"+str(endpoint.port))
    context = None
    if endpoint.tls:
        context = ssl.create_default_context(cafile=endpoint.ca_file)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
    writer = None
    started = time.monotonic()
    try:
        async with asyncio.timeout(timeout_ms/1000):
            kwargs = {"ssl": context, "limit": HEADER_MAX}
            if endpoint.tls:
                kwargs.update(server_hostname=endpoint.server_name or endpoint.host,
                              ssl_handshake_timeout=timeout_ms/1000, ssl_shutdown_timeout=1)
            reader, writer = await asyncio.open_connection(endpoint.host, endpoint.port, **kwargs)
            await _write(writer, head); await _write(writer, raw)
            first, headers, count, incoming_headers = await _headers(reader)
            parts = first.split(" ")
            F.need(len(parts) >= 3 and parts[0] == "HTTP/1.1" and parts[1] in ("200", "400", "404", "503"), "HTTP_STATUS")
            F.need("host" not in headers and count <= max_reply_bytes, "HTTP_RESPONSE_BOUND")
            body = await _body(reader, count)
            F.need(await reader.read(1) == b"", "HTTP_TRAILING_RESPONSE")
            return {"status": int(parts[1]), "raw": body, "request_bytes": len(raw),
                    "reply_bytes": len(body), "header_bytes": len(head)+incoming_headers,
                    "elapsed_ms": int((time.monotonic()-started)*1000)}
    finally:
        if writer is not None:
            writer.close()
            try:
                async with asyncio.timeout(1): await writer.wait_closed()
            except Exception: pass


class Provider:
    def __init__(self, *, index=None, custody=None, ordinary=None, max_connections=2, max_requests=1024,
                 max_reply_bytes=256*1024**2, operation_ms=5000):
        F.need(index is not None or custody is not None or ordinary is not None, "PROVIDER_EMPTY")
        F.uint(max_connections, 1, 8); F.uint(max_requests, 1, 1000000)
        F.uint(max_reply_bytes, 1024, 2**40); F.uint(operation_ms, 1, 60000)
        self.index, self.custody, self.ordinary = index, custody, ordinary
        self.max_connections, self.max_requests = max_connections, max_requests
        self.max_reply_bytes, self.operation_ms = max_reply_bytes, operation_ms
        self.server, self.tasks = None, set()
        self.requests = self.reserved_reply_bytes = self.reply_bytes = self.header_bytes = self.request_bytes = 0
        self.failures = self.refused = 0

    async def start(self, host="127.0.0.1", port=0, *, tls_context=None):
        address = ipaddress.ip_address(host)
        F.need(not address.is_unspecified and not address.is_multicast
               and (address.is_loopback or tls_context is not None), "PROVIDER_BIND_POLICY")
        F.uint(port, 0, 65535); F.need(self.server is None, "PROVIDER_ALREADY_STARTED")
        kwargs = {"ssl": tls_context, "limit": HEADER_MAX, "backlog": 16}
        if tls_context is not None: kwargs.update(ssl_handshake_timeout=5, ssl_shutdown_timeout=1)
        self.server = await asyncio.start_server(self._serve, host, port, **kwargs)
        actual = self.server.sockets[0].getsockname()[1]
        return Endpoint(host, actual, tls_context is not None)

    async def stop(self):
        if self.server is not None:
            self.server.close(); await self.server.wait_closed(); self.server = None
        tasks = list(self.tasks)
        for task in tasks: task.cancel()
        if tasks: await asyncio.gather(*tasks, return_exceptions=True)

    def dispatch(self, route, request, *, check_budget=None):
        """Offer/compact-summary/ordinary routes return bytes; old routes objects."""
        F.need(route in ROUTES, "HTTP_ROUTE")
        if route in ORDINARY_ROUTES:
            # Lazy role import preserves old discovery/module dependency surfaces.
            from . import ordinary_acquisition as O
            F.need(self.ordinary is not None, "ROLE_NOT_SERVED")
            return O.serve(self.ordinary, route, request, check_budget=check_budget)
        if route == CANDIDATE_ROUTE:
            from discovery import candidate_query as C
            F.need(self.index is not None, "ROLE_NOT_SERVED")
            C.validate_request(request, self.index.namespace)
            if check_budget is not None: check_budget()
            local_request = deepcopy(request)
            local_request["limits"]["timeout_ms"] = min(request["limits"]["timeout_ms"], self.operation_ms)
            result = C.page(self.index, local_request)
            if check_budget is not None: check_budget()
            return result
        if route == OFFER_ROUTE:
            _offer_request(request)
            if check_budget is not None: check_budget()
            envelope = {"schema": "DMKN_DISCOVERY_OFFER_V1", "namespace": request["namespace"],
                        "features": request["features"], "status": "NO_OFFER", "reason": "ROLE_NOT_SERVED",
                        "summary": None, "global_complete": False, "mathematical_acceptance": False}
            if self.index is not None:
                envelope["reason"] = "NAMESPACE_NOT_SERVED"
                if self.index.namespace == request["namespace"]:
                    envelope.update(status="OFFERED", reason="SNAPSHOT_SELECTED")
                    # The entire envelope, not just its inner compact summary,
                    # is bounded by the caller's one reserved wire allowance.
                    inner_cap = request["max_bytes"] - (len(F.compact(envelope))-4)
                    try:
                        F.need(inner_cap >= 1, "SUMMARY_WIRE_BYTES")
                        descriptor = self.index.snapshot()
                        sid = A.snapshot_id(descriptor)
                        if check_budget is not None: check_budget()
                        expanded = self.index.summary(sid, request["features"], request["max_expanded_bytes"])
                        raw = W.encode_summary(expanded, sid, request["namespace"], request["features"],
                            max_wire_bytes=inner_cap, max_expanded_bytes=request["max_expanded_bytes"],
                            check_budget=check_budget)
                        envelope["summary"] = F.strict(raw, inner_cap)
                    except ValueError as error:
                        if str(error) not in ("SUMMARY_BYTES_EXHAUSTED", "SUMMARY_EXPANSION_BYTES",
                                              "SUMMARY_WIRE_BYTES", "NODE_READ_CAP", "INDEX_HASH_CAP",
                                              "DISCOVERY_TIME_EXHAUSTED"):
                            raise
                        envelope.update(status="REFUSED", reason="SUMMARY_RESOURCE_BOUND", summary=None)
            if check_budget is not None: check_budget()
            raw = F.compact(envelope)
            F.need(len(raw) <= request["max_bytes"], "OFFER_WIRE_BYTES")
            return raw
        if route == COMPACT_SUMMARY_ROUTE:
            F.need(self.index is not None, "ROLE_NOT_SERVED")
            F.fields(request, ("snapshot_id", "features", "max_bytes", "max_expanded_bytes"))
            F.uint(request["max_bytes"], 1024, 1048576, "COMPACT_SUMMARY_WIRE_BYTES")
            F.uint(request["max_expanded_bytes"], 1024, 1048576, "COMPACT_SUMMARY_EXPANDED_BYTES")
            if check_budget is not None: check_budget()
            expanded = self.index.summary(request["snapshot_id"], request["features"], request["max_expanded_bytes"])
            return W.encode_summary(expanded, request["snapshot_id"], self.index.namespace, request["features"],
                                    max_wire_bytes=request["max_bytes"], max_expanded_bytes=request["max_expanded_bytes"],
                                    check_budget=check_budget)
        if route == "/v5/discovery/summary":
            F.need(self.index is not None, "ROLE_NOT_SERVED")
            F.fields(request, ("snapshot_id", "features", "max_bytes"))
            return self.index.summary(request["snapshot_id"], request["features"], request["max_bytes"])
        if route == "/v5/discovery/page":
            F.need(self.index is not None, "ROLE_NOT_SERVED")
            return self.index.page(request)
        F.need(self.custody is not None, "ROLE_NOT_SERVED")
        if route == "/v5/modules/group":
            F.fields(request, ("module_id", "relative_name", "group_index"))
            return self.custody.get_group(request["module_id"], request["relative_name"], request["group_index"])[0]
        F.fields(request, ("module_id", "relative_name", "universes", "body_hash"))
        return self.custody.get_body(request["module_id"], request["relative_name"], request["universes"], request["body_hash"])

    async def _serve(self, reader, writer):
        task = asyncio.current_task()
        if len(self.tasks) >= self.max_connections or self.requests >= self.max_requests:
            self.refused += 1; writer.close(); return
        self.tasks.add(task); self.requests += 1
        reservation = 0
        until = time.monotonic() + self.operation_ms/1000
        try:
            async with asyncio.timeout(self.operation_ms/1000):
                first, headers, count, header_count = await _headers(reader)
                self.header_bytes += header_count
                parts = first.split(" ")
                F.need(len(parts) == 3 and parts[0] == "POST" and parts[2] == "HTTP/1.1"
                       and parts[1] in ROUTES and "host" in headers, "HTTP_REQUEST_LINE")
                route = parts[1]; F.need(0 < count <= REQUEST_MAX, "HTTP_REQUEST_BOUND")
                raw = await _body(reader, count); self.request_bytes += len(raw)
                request = F.strict(raw, REQUEST_MAX)
                reservation = ROUTES[route]
                if route in ORDINARY_ROUTES:
                    from . import ordinary_acquisition as O
                    reservation = O.request_limit(route, request)
                if route == CANDIDATE_ROUTE:
                    from discovery import candidate_query as C
                    C.validate_request(request)
                    reservation = request["limits"]["bytes"]
                if route == OFFER_ROUTE:
                    _offer_request(request)
                    reservation = request["max_bytes"]
                if route == COMPACT_SUMMARY_ROUTE:
                    F.fields(request, ("snapshot_id", "features", "max_bytes", "max_expanded_bytes"))
                    reservation = F.uint(request["max_bytes"], 1024, ROUTES[route], "COMPACT_SUMMARY_WIRE_BYTES")
                    F.uint(request["max_expanded_bytes"], 1024, 1048576, "COMPACT_SUMMARY_EXPANDED_BYTES")
                F.need(self.reply_bytes+self.reserved_reply_bytes+reservation <= self.max_reply_bytes, "PROVIDER_REPLY_QUOTA")
                self.reserved_reply_bytes += reservation
                try:
                    def check_budget():
                        F.need(time.monotonic() < until, "PROVIDER_OPERATION_DEADLINE")
                    if route == CANDIDATE_ROUTE:
                        check_budget()
                        # Spend no more than the client's cap or the remaining
                        # owner operation time. Limits are maxima, not promises
                        # to spend the whole requested amount. No caller object
                        # is changed by public dispatch; this is a parsed copy.
                        request["limits"]["timeout_ms"] = min(request["limits"]["timeout_ms"],
                            max(1, int((until-time.monotonic())*1000)))
                    value = self.dispatch(route, request, check_budget=check_budget)
                    encoded = value if route in (COMPACT_SUMMARY_ROUTE, OFFER_ROUTE, *ORDINARY_ROUTES) else F.compact(value)
                    F.need(len(encoded) <= reservation, "PROVIDER_RESPONSE_BYTES")
                    F.need(time.monotonic() < until, "PROVIDER_OPERATION_DEADLINE")
                    head = _header("HTTP/1.1 200 OK", len(encoded))
                    # Charge before sending; interruption cannot erase allocation.
                    self.reply_bytes += len(encoded); self.header_bytes += len(head)
                    await _write(writer, head); await _write(writer, encoded)
                finally:
                    self.reserved_reply_bytes -= reservation; reservation = 0
        except Exception:
            self.failures += 1
            # Close on malformed/overbudget requests. No free error body or
            # provider-local not-found message is promoted to global absence.
        finally:
            writer.close()
            try:
                try:
                    async with asyncio.timeout(1): await writer.wait_closed()
                except Exception: pass
            finally:
                self.tasks.discard(task)

    def status(self):
        return {"requests": self.requests, "request_bytes": self.request_bytes,
                "reply_bytes": self.reply_bytes, "header_bytes": self.header_bytes,
                "reserved_reply_bytes": self.reserved_reply_bytes, "active": len(self.tasks),
                "failures": self.failures, "refused": self.refused, "mathematical_acceptance": False}

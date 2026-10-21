"""Finite owner-provisioned placement wire; no grant vending or mathematics.

Tokens live in owner memory and request bodies only. Public errors are closed
codes; local raw errors/Node diagnostics never become wire observations. Bounds
cover authorized application reads/writes, not arbitrary TCP/TLS/OS ingress.
"""
import asyncio
from copy import deepcopy
import ipaddress
import math
import ssl
import time

from discovery import authenticated_index as A
from discovery import formal_features as F
from location.protocol import OwnerEgressPolicy, route_key
from transport import http_provider_receipts as H
from . import codec as P
from .ledger import PHASES

SUBMIT, STATUS = "/v5/placement/submit", "/v5/placement/status"
SUBMIT_SCHEMA, STATUS_SCHEMA = "DMKN_PLACEMENT_SUBMIT_V1", "DMKN_PLACEMENT_STATUS_V1"
RESPONSE_SCHEMA, ERROR_SCHEMA = "DMKN_PLACEMENT_RESPONSE_V1", "DMKN_PLACEMENT_ERROR_V1"
SUBMIT_MAX, STATUS_MAX, REPLY_MAX, ROUTE_MAX = 17408, 1024, 81920, 4096
IN_RESERVE, OUT_RESERVE = SUBMIT_MAX+H.HEADER_MAX, REPLY_MAX+H.HEADER_MAX
BINDINGS = ("service_epoch", "generation", "namespace", "wire_profile_id")
ERRORS = frozenset(("INVALID_REQUEST", "BUSY", "REFUSED_OR_INCOMPLETE", "SERVICE_UNAVAILABLE"))
ROUTE_STATES = frozenset(("NOT_ATTEMPTED", "DISPATCH_ATTEMPTED", "HINT_DISPATCHED_UNACKNOWLEDGED",
                          "INCOMPLETE", "DISPATCH_UNCERTAIN"))
SUCCESS_FIELDS = ("status", "request_id", "service_epoch", "generation", "namespace", "wire_profile_id",
    "export_id", "record", "record_id", "snapshot_id", "snapshot", "route", "export_object_sha256",
    "export_object_bytes", "packet_sha256", "packet_bytes", "bodies", "retention_end_ms",
    "service_not_after_ms", "reservation", "recovery", "reservation_semantics", "observed", "assurance",
    *P.FLAGS)


class PlacementWireError(ValueError):
    """Closed public diagnostic; uncertain submit means status must be observed."""
    def __init__(self, code, *, uncertain=False):
        allowed = ERRORS | {"CLIENT_CLOSED_OR_EXPIRED", "CLIENT_BINDING_CHANGED", "CLIENT_BUDGET",
            "CLIENT_REQUEST_INVALID", "TRANSPORT_OR_RESPONSE_FAILURE", "CLEANUP_UNCERTAIN"}
        if code not in allowed: code = "TRANSPORT_OR_RESPONSE_FAILURE"
        super().__init__(code)
        self.code, self.uncertain = code, bool(uncertain)


def _bindings(value):
    F.fields(value, BINDINGS)
    for name in BINDINGS: F.hexid(value[name])
    return deepcopy(value)


def _token(value):
    F.need(type(value) is str and len(value) == 64
           and all(char in "0123456789abcdef" for char in value), "PLACEMENT_WIRE_TOKEN")
    return value


def _deadline(value):
    now = time.monotonic()
    F.need(type(value) in (int, float) and math.isfinite(value) and now < value <= now+3600,
           "PLACEMENT_WIRE_ORIGINAL_DEADLINE")
    return value


def request_bytes(route, token, payload):
    """Owner-side canonical envelope; never persist or print the returned bytes."""
    _token(token)
    if route == SUBMIT:
        F.need(type(payload) is bytes and 0 < len(payload) <= P.REQUEST_MAX, "PLACEMENT_INNER_BOUND")
        value = F.strict(payload, P.REQUEST_MAX)
        F.need(type(value) is dict and F.compact(value) == payload, "PLACEMENT_INNER_CANONICAL")
        envelope = {"schema": SUBMIT_SCHEMA, "token": token, "manifest": value}
    else:
        F.need(route == STATUS, "PLACEMENT_WIRE_ROUTE")
        envelope = {"schema": STATUS_SCHEMA, "token": token, "request_id": F.hexid(payload)}
    raw = F.compact(envelope)
    F.need(len(raw) <= (SUBMIT_MAX if route == SUBMIT else STATUS_MAX), "PLACEMENT_ENVELOPE_BOUND")
    return raw


def parse_request(route, raw):
    F.need(route in (SUBMIT, STATUS) and type(raw) is bytes, "PLACEMENT_WIRE_REQUEST")
    maximum = SUBMIT_MAX if route == SUBMIT else STATUS_MAX
    F.need(0 < len(raw) <= maximum, "PLACEMENT_ENVELOPE_BOUND")
    value = F.strict(raw, maximum)
    F.fields(value, ("schema", "token", "manifest") if route == SUBMIT else ("schema", "token", "request_id"))
    F.need(F.compact(value) == raw, "PLACEMENT_ENVELOPE_CANONICAL")
    token = _token(value["token"])
    F.need(value["schema"] == (SUBMIT_SCHEMA if route == SUBMIT else STATUS_SCHEMA), "PLACEMENT_ENVELOPE_SCHEMA")
    if route == SUBMIT:
        F.need(type(value["manifest"]) is dict, "PLACEMENT_INNER_OBJECT")
        payload = F.compact(value["manifest"])
        F.need(0 < len(payload) <= P.REQUEST_MAX, "PLACEMENT_INNER_BOUND")
    else: payload = F.hexid(value["request_id"])
    return token, payload


def _route(value):
    # Unknown fields, particularly raw error/census strings, cannot cross this seam.
    fields = ("status", "cell", "features", "stripe", "run_id", "request_id", "observed_at_ms",
              "add_provider_write", "error_code")
    F.fields(value, fields)
    F.need(value["status"] in ROUTE_STATES and value["stripe"] == 0
           and type(value["stripe"]) is int, "PLACEMENT_ROUTE_STATE")
    F.hexid(value["cell"])
    F.need(type(value["features"]) is list and len(value["features"]) == 1, "PLACEMENT_ROUTE_FEATURE")
    F.hexid(value["features"][0]); F.uint(value["add_provider_write"], 0, 2**53-1)
    if value["status"] == "NOT_ATTEMPTED":
        F.need(all(value[key] is None for key in ("run_id", "request_id", "observed_at_ms", "error_code"))
               and value["add_provider_write"] == 0, "PLACEMENT_ROUTE_UNATTEMPTED")
    else:
        F.hexid(value["run_id"]); F.hexid(value["request_id"])
        F.uint(value["observed_at_ms"], 1, 2**53-1)
        if value["status"] == "HINT_DISPATCHED_UNACKNOWLEDGED":
            F.need(value["add_provider_write"] > 0 and value["error_code"] is None, "PLACEMENT_ROUTE_HINT")
        else:
            expected = "ROUTE_INCOMPLETE" if value["status"] == "INCOMPLETE" else "ROUTE_UNCERTAIN"
            F.need(value["error_code"] == expected, "PLACEMENT_ROUTE_CLOSED_ERROR")
            if value["status"] == "DISPATCH_ATTEMPTED":
                F.need(value["add_provider_write"] == 0, "PLACEMENT_ROUTE_ATTEMPT_ONLY")
    F.need(len(F.compact(value)) <= ROUTE_MAX, "PLACEMENT_ROUTE_BOUND")
    return deepcopy(value)


def _success(value, bindings, rid, *, projected=False):
    F.fields(value, SUCCESS_FIELDS)
    F.need(value["status"] == "INDEXED_UNADVERTISED" and value["request_id"] == rid
           and all(value[name] == bindings[name] for name in BINDINGS), "PLACEMENT_RECEIPT_BINDING")
    for key in P.FLAGS: F.need(value[key] is False, "PLACEMENT_RECEIPT_ASSURANCE")
    for key in ("export_id", "record_id", "snapshot_id", "export_object_sha256", "packet_sha256"):
        F.hexid(value[key])
    for key, maximum in (("export_object_bytes",16*1024**2),("packet_bytes",32*1024**2),
                         ("retention_end_ms",2**53-1),("service_not_after_ms",2**53-1)):
        F.uint(value[key], 1, maximum)
    F.need(type(value["recovery"]) is bool, "PLACEMENT_RECEIPT_RECOVERY")
    P.limits(value["reservation"])
    record = F.validate_record(value["record"], bindings["namespace"])
    F.need(F.record_id(record) == value["record_id"] and record["object_id"] == value["export_id"]
           and record["object_sha256"] == value["export_object_sha256"]
           and record["object_bytes"] == value["export_object_bytes"], "PLACEMENT_RECEIPT_RECORD")
    A.validate_snapshot(value["snapshot"], bindings["namespace"])
    F.need(A.snapshot_id(value["snapshot"]) == value["snapshot_id"], "PLACEMENT_RECEIPT_SNAPSHOT")
    F.fields(value["route"], ("status", "cell", "features", "stripe"))
    F.need(value["route"]["status"] == "INTENT_ONLY" and type(value["route"]["stripe"]) is int
           and value["route"]["stripe"] == 0, "PLACEMENT_RECEIPT_ROUTE")
    F.hexid(value["route"]["cell"])
    F.need(type(value["route"]["features"]) is list and len(value["route"]["features"]) == 1,
           "PLACEMENT_RECEIPT_ROUTE_FEATURE")
    F.hexid(value["route"]["features"][0])
    F.need(value["route"]["features"][0] in record["features"]
           and route_key(bindings["namespace"],value["route"]["features"],0) == value["route"]["cell"],
           "PLACEMENT_RECEIPT_DERIVED_ROUTE")
    F.need(type(value["bodies"]) is list and len(value["bodies"]) <= 8, "PLACEMENT_RECEIPT_BODIES")
    for body in value["bodies"]:
        F.fields(body, ("body_hash", "response_sha256", "response_bytes"))
        F.hexid(body["body_hash"]); F.hexid(body["response_sha256"])
        F.uint(body["response_bytes"], 1, 16*1024**2)
    body_keys = [body["body_hash"] for body in value["bodies"]]
    F.need(body_keys == sorted(set(body_keys)), "PLACEMENT_RECEIPT_BODY_ORDER")
    F.need(value["assurance"] == "OWNER_LOCAL_STRUCTURAL_CUSTODY_AND_INDEX_READBACK_NOT_REMOTE_ACK"
           and value["reservation_semantics"] == "CUMULATIVE_NONREFUNDABLE_AUTHORIZATION_NOT_PHYSICAL_FREE_SPACE",
           "PLACEMENT_RECEIPT_SCOPE")
    # Do not expose nested acquisition/controller diagnostics. This closed
    # projection retains only audited resource totals, not arbitrary strings.
    observed = value["observed"]
    F.fields(observed, ("structural_input_bytes", "new_store_logical_bytes") if projected else
             ("structural_input_bytes", "store_counts_before", "store_counts_after",
              "new_store_logical_bytes", "index_work", "packet_census", "acquisition"))
    F.uint(observed["structural_input_bytes"], 0, 2**50)
    F.fields(observed["new_store_logical_bytes"], ("modules", "packets", "index"))
    for amount in observed["new_store_logical_bytes"].values(): F.uint(amount, 0, 2**50)
    result = deepcopy({key: item for key, item in value.items() if key != "observed"})
    result["observed"] = {"structural_input_bytes": observed["structural_input_bytes"],
                          "new_store_logical_bytes": deepcopy(observed["new_store_logical_bytes"])}
    F.need(len(F.compact(result)) <= P.OUTCOME_MAX, "PLACEMENT_RECEIPT_BOUND")
    return result


def public_response(joined, bindings, rid, *, projected=False):
    """Closed wire projection. Never modify the immutable local ledger receipt."""
    bindings = _bindings(bindings); F.hexid(rid)
    F.fields(joined, ("placement", "route"))
    held = joined["placement"]
    F.fields(held, ("request_id", "phase", "reservation", "recovery_used", "outcome", "observation_only", *P.FLAGS))
    F.need(held["request_id"] == rid and held["phase"] in PHASES and type(held["recovery_used"]) is bool
           and held["observation_only"] is True, "PLACEMENT_PUBLIC_ROW")
    for key in P.FLAGS: F.need(held[key] is False, "PLACEMENT_PUBLIC_ASSURANCE")
    reservation = P.limits(held["reservation"])
    if held["phase"] == "RECEIPT_COMMITTED":
        outcome = _success(held["outcome"], bindings, rid, projected=projected)
        F.need(outcome["reservation"] == reservation, "PLACEMENT_RESERVATION_BINDING")
    else:
        if projected:
            F.need(held["outcome"] in (None, {"status":"INCOMPLETE", "code":"PLACEMENT_INCOMPLETE"}),
                   "PLACEMENT_PUBLIC_INCOMPLETE")
        outcome = None if held["outcome"] is None else {"status":"INCOMPLETE", "code":"PLACEMENT_INCOMPLETE"}
    placement = {key:deepcopy(held[key]) for key in ("request_id", "phase", "recovery_used", "observation_only", *P.FLAGS)}
    placement.update(reservation=reservation, outcome=outcome)
    route = _route(joined["route"])
    if outcome is not None and held["phase"] == "RECEIPT_COMMITTED":
        F.need(all(route[key] == outcome["route"][key] for key in ("cell", "features", "stripe")),
               "PLACEMENT_JOINED_ROUTE_BINDING")
    result = dict(schema=RESPONSE_SCHEMA, status="OBSERVED", bindings=bindings, request_id=rid,
                  placement=placement, route=route, mathematical_acceptance=False)
    F.need(len(F.compact(result)) <= REPLY_MAX, "PLACEMENT_FULL_REPLY_BOUND")
    return result


def _error(code):
    F.need(code in ERRORS, "PLACEMENT_CLOSED_ERROR")
    return F.compact(dict(schema=ERROR_SCHEMA, status="REFUSED_OR_INCOMPLETE", code=code,
                          mathematical_acceptance=False))


class PlacementProvider:
    def __init__(self, handler, *, limits):
        # Delayed import avoids a cycle with the owner's start() composition.
        from client.serve_placement import PlacementService
        F.need(type(handler) is PlacementService, "PLACEMENT_EXACT_SERVICE")
        handler._active()
        F.fields(limits, ("max_connections", "max_requests", "incoming_bytes", "outgoing_bytes", "operation_ms"))
        F.uint(limits["max_connections"], 1, 8); F.uint(limits["max_requests"], 1, 4096)
        F.uint(limits["incoming_bytes"], IN_RESERVE, 2**40)
        F.uint(limits["outgoing_bytes"], OUT_RESERVE, 2**40); F.uint(limits["operation_ms"], 1, 60000)
        self._handler, self._bindings = handler, _bindings(dict(handler.bindings))
        self.deadline = _deadline(handler.deadline)
        self._cleanup_deadline = _deadline(handler.outer_deadline)
        F.need(self.deadline < self._cleanup_deadline, "PLACEMENT_ORIGINAL_CLEANUP_MARGIN")
        self._limits, self._limits_raw = deepcopy(limits), F.compact(limits)
        self.server, self.endpoint, self._busy, self._stopping = None, None, False, False
        self.tasks, self.writers = set(), set()
        self._used = dict(requests=0, incoming_reserved=0, outgoing_reserved=0,
                         observed_incoming=0, attempted_outgoing=0, busy=0, refused=0,
                         completed_actions=0, cancelled=0, cleanup_errors=0, handler_errors=0)

    def _active(self):
        F.need(not self._stopping and time.monotonic() < self.deadline
               and self._handler.deadline == self.deadline and self._handler.bindings == self._bindings
               and self._handler.outer_deadline == self._cleanup_deadline
               and F.compact(self._limits) == self._limits_raw, "PLACEMENT_PROVIDER_BINDING_OR_EXPIRED")
        self._handler._active()

    def _halt(self):
        if self.server is not None: self.server.close()

    async def start(self, host="127.0.0.1", port=0, *, tls_context=None):
        self._active(); F.need(self.server is None, "PLACEMENT_PROVIDER_ALREADY_STARTED")
        address = ipaddress.ip_address(host); F.uint(port, 0, 65535)
        F.need(not address.is_unspecified and not address.is_multicast
               and (address.is_loopback or tls_context is not None), "PLACEMENT_BIND_POLICY")
        if tls_context is not None:
            F.need(type(tls_context) is ssl.SSLContext and tls_context.protocol == ssl.PROTOCOL_TLS_SERVER
                   and tls_context.minimum_version >= ssl.TLSVersion.TLSv1_2, "PLACEMENT_SERVER_TLS")
        kwargs = dict(ssl=tls_context, limit=H.HEADER_MAX, backlog=self._limits["max_connections"])
        if tls_context is not None:
            kwargs.update(ssl_handshake_timeout=min(10,self._limits["operation_ms"]/1000), ssl_shutdown_timeout=1)
        try:
            self.server = await asyncio.start_server(self._accept, str(address), port, **kwargs)
            self.endpoint = H.Endpoint(str(address), self.server.sockets[0].getsockname()[1], tls_context is not None).validate()
            self._active(); return self.endpoint
        except BaseException:
            # Retain the server handle for owner cleanup, but never leave an
            # accepting listener after partial start/expired owner bindings.
            self._stopping = True; self._halt()
            raise

    def _accept(self, reader, writer):
        # Synchronous admission: no queue or await before original reservation.
        try:
            self._active(); used, cap = self._used, self._limits
            F.need(used["requests"] < cap["max_requests"]
                   and used["incoming_reserved"]+IN_RESERVE <= cap["incoming_bytes"]
                   and used["outgoing_reserved"]+OUT_RESERVE <= cap["outgoing_bytes"], "PLACEMENT_TRAFFIC_CAP")
            used["requests"] += 1; used["incoming_reserved"] += IN_RESERVE; used["outgoing_reserved"] += OUT_RESERVE
            self.writers.add(writer)
            if used["requests"] >= cap["max_requests"] or used["incoming_reserved"]+IN_RESERVE > cap["incoming_bytes"] \
                    or used["outgoing_reserved"]+OUT_RESERVE > cap["outgoing_bytes"]: self._halt()
            if len(self.tasks) >= cap["max_connections"]:
                used["refused"] += 1; writer.close(); return
            task = asyncio.create_task(self._serve(reader, writer))
            self.tasks.add(task); task.add_done_callback(self._done)
        except Exception:
            self._used["refused"] += 1; self._halt(); writer.close()

    def _done(self, task):
        self.tasks.discard(task)
        if not task.cancelled() and task.exception() is not None:
            self._used["handler_errors"] += 1; self._halt()

    async def _serve(self, reader, writer):
        until = min(self.deadline, time.monotonic()+self._limits["operation_ms"]/1000)
        sent, held = False, False
        async def reply(raw, status):
            nonlocal sent
            F.need(not sent and len(raw) <= REPLY_MAX, "PLACEMENT_RESPONSE_ONCE")
            header = H._header("HTTP/1.1 "+status, len(raw))
            F.need(len(header) <= H.HEADER_MAX, "PLACEMENT_RESPONSE_HEADER")
            sent = True; self._used["attempted_outgoing"] += len(header)+len(raw)
            await H._write(writer, header); await H._write(writer, raw)
        try:
            async with asyncio.timeout_at(until):
                first, headers, count, incoming = await H._headers(reader)
                self._used["observed_incoming"] += incoming
                parts = first.split(" ")
                F.need(len(parts) == 3 and parts[0] == "POST" and parts[2] == "HTTP/1.1"
                       and parts[1] in (SUBMIT, STATUS) and "host" in headers, "PLACEMENT_POST_ROUTE")
                route = parts[1]
                F.need(0 < count <= (SUBMIT_MAX if route == SUBMIT else STATUS_MAX), "PLACEMENT_CONTENT_LENGTH")
                raw = await H._body(reader, count); self._used["observed_incoming"] += len(raw)
                token, payload = parse_request(route, raw)
                if self._busy:
                    self._used["busy"] += 1; await reply(_error("BUSY"), "503 Service Unavailable"); return
                self._busy = held = True; self._active()
                rid = P.request_id(payload, P.digest(token.encode("ascii")), self._bindings["generation"]) \
                    if route == SUBMIT else payload
                try:
                    if route == SUBMIT: joined = await self._handler.submit(token, payload, until=until)
                    else: joined = self._handler.status(token, payload, until=until)
                    self._active(); F.need(time.monotonic() < until, "PLACEMENT_REQUEST_EXPIRED")
                    response = public_response(joined, self._bindings, rid)
                    self._used["completed_actions"] += 1
                except asyncio.CancelledError: raise
                except Exception:
                    self._used["handler_errors"] += 1
                    await reply(_error("REFUSED_OR_INCOMPLETE"), "503 Service Unavailable"); return
                await reply(F.compact(response), "200 OK")
        except asyncio.CancelledError:
            self._used["cancelled"] += 1
            raise
        except Exception:
            self._used["refused"] += 1
            if not sent and time.monotonic() < until:
                try:
                    async with asyncio.timeout_at(until): await reply(_error("INVALID_REQUEST"), "400 Bad Request")
                except Exception: pass
        finally:
            if held: self._busy = False
            writer.close()
            try:
                async with asyncio.timeout(1): await writer.wait_closed()
                self.writers.discard(writer)
            except asyncio.CancelledError:
                self._used["cleanup_errors"] += 1
                raise
            except Exception: self._used["cleanup_errors"] += 1

    async def stop(self, *, until):
        F.need(type(until) in (int,float) and math.isfinite(until) and until <= self._cleanup_deadline,
               "PLACEMENT_ORIGINAL_CLEANUP_BOUND")
        self._stopping = True; self._halt()
        for task in tuple(self.tasks): task.cancel()
        for writer in tuple(self.writers): writer.close()
        try:
            async with asyncio.timeout_at(until):
                if self.server is not None:
                    await self.server.wait_closed(); self.server = None
                if self.tasks: await asyncio.gather(*tuple(self.tasks), return_exceptions=True)
                self.tasks.difference_update(task for task in tuple(self.tasks) if task.done())
                for writer in tuple(self.writers):
                    try: await writer.wait_closed()
                    except Exception: self._used["cleanup_errors"] += 1
                    self.writers.discard(writer)
        except Exception:
            self._used["cleanup_errors"] += 1
            raise PlacementWireError("CLEANUP_UNCERTAIN") from None
        if self._used["cleanup_errors"] or self.tasks or self.writers:
            raise PlacementWireError("CLEANUP_UNCERTAIN")

    def report(self):
        return dict(bindings=deepcopy(self._bindings), limits=deepcopy(self._limits), used=dict(self._used),
            active_connections=len(self.tasks), retained_closing_connections=len(self.writers), active_intake=self._busy,
            accepting=self.server is not None and self.server.is_serving() and not self._stopping,
            stopped=self._stopping, transport="TLS" if self.endpoint is not None and self.endpoint.tls else "LOOPBACK_TEST",
            accounting="NONREFUNDABLE_APPLICATION_AUTHORIZATION_NOT_TCP_TLS_OS_INGRESS",
            pre_handshake_limit="EXTERNAL_OS_AND_SUPERVISOR_REQUIRED", mathematical_acceptance=False)

    status = report


class PlacementClient:
    """One fixed owner-adopted endpoint/token; no discovery-selected write target."""
    def __init__(self, egress, contact, expected, token, *, deadline, requests,
                 incoming_bytes, outgoing_bytes, operation_ms=60000):
        self._policy = OwnerEgressPolicy(egress); self._egress = F.compact(egress)
        self._contact = deepcopy(contact); self._endpoint = self._policy.endpoint(contact)
        F.need(self._endpoint.ca_file is None, "PLACEMENT_NO_REMOTE_CA_OVERRIDE")
        self._expected = _bindings(expected); self._token = _token(token)
        self._binding = (self._endpoint, F.compact(expected), P.digest(token.encode("ascii")))
        self.deadline = self._deadline = _deadline(deadline)
        F.uint(requests, 1, 4096); F.uint(incoming_bytes, OUT_RESERVE, 2**40)
        F.uint(outgoing_bytes, IN_RESERVE, 2**40); F.uint(operation_ms, 1, 60000)
        self._caps = requests,incoming_bytes,outgoing_bytes,operation_ms
        self._used = dict(requests=0, incoming_reserved=0, outgoing_reserved=0,
                          observed_incoming=0, attempted_outgoing=0, uncertain_submits=0, cleanup_errors=0)
        self._busy, self.closed = False, False

    def _active(self):
        if self.closed or time.monotonic() >= self._deadline: raise PlacementWireError("CLIENT_CLOSED_OR_EXPIRED")
        try:
            intact = self.deadline == self._deadline and F.compact(self._policy._config) == self._egress \
                and (self._policy.endpoint(self._contact), F.compact(self._expected), P.digest(self._token.encode("ascii"))) == self._binding
        except Exception: raise PlacementWireError("CLIENT_BINDING_CHANGED") from None
        if not intact: raise PlacementWireError("CLIENT_BINDING_CHANGED")

    async def submit(self, manifest):
        try:
            raw = request_bytes(SUBMIT, self._token, manifest)
            value = F.strict(manifest, P.REQUEST_MAX)
            F.need(all(value[name] == self._expected[name] for name in ("generation","namespace","wire_profile_id")),
                   "PLACEMENT_CLIENT_MANIFEST_BINDING")
            rid = P.request_id(manifest, P.digest(self._token.encode("ascii")), self._expected["generation"])
        except Exception: raise PlacementWireError("CLIENT_REQUEST_INVALID") from None
        return await self._send(SUBMIT, raw, rid, manifest=value)

    async def status(self, request_id):
        try: raw = request_bytes(STATUS, self._token, request_id)
        except Exception: raise PlacementWireError("CLIENT_REQUEST_INVALID") from None
        return await self._send(STATUS, raw, request_id)

    async def _send(self, route, raw, rid, *, manifest=None):
        self._active()
        if self._busy or self._used["requests"] >= self._caps[0] \
                or self._used["incoming_reserved"]+OUT_RESERVE > self._caps[1] \
                or self._used["outgoing_reserved"]+IN_RESERVE > self._caps[2]:
            raise PlacementWireError("CLIENT_BUDGET")
        self._used["requests"] += 1; self._used["incoming_reserved"] += OUT_RESERVE
        self._used["outgoing_reserved"] += IN_RESERVE; self._busy = True
        until = min(self._deadline, time.monotonic()+self._caps[3]/1000)
        writer, value, failure, cleanup_failed = None, None, None, False
        uncertainty_recorded = False
        def record_uncertainty():
            nonlocal uncertainty_recorded
            if route == SUBMIT and not uncertainty_recorded:
                self._used["uncertain_submits"] += 1; uncertainty_recorded = True
        try:
            self._active(); endpoint = self._endpoint
            context = None
            if endpoint.tls:
                context = ssl.create_default_context(); context.minimum_version = ssl.TLSVersion.TLSv1_2
            kwargs = dict(ssl=context, limit=H.HEADER_MAX)
            if context is not None:
                kwargs.update(server_hostname=endpoint.server_name or endpoint.host,
                              ssl_handshake_timeout=max(.001,until-time.monotonic()), ssl_shutdown_timeout=1)
            async with asyncio.timeout_at(until):
                reader, writer = await asyncio.open_connection(endpoint.host, endpoint.port, **kwargs)
                self._active()
                host = "["+endpoint.host+"]" if ":" in endpoint.host else endpoint.host
                header = H._header("POST "+route+" HTTP/1.1", len(raw), host+":"+str(endpoint.port))
                F.need(len(header) <= H.HEADER_MAX, "PLACEMENT_REQUEST_HEADER")
                self._used["attempted_outgoing"] += len(header)+len(raw)
                await H._write(writer, header); await H._write(writer, raw)
                first, headers, count, incoming = await H._headers(reader)
                self._used["observed_incoming"] += incoming
                parts = first.split(" ", 2)
                F.need(len(parts) == 3 and parts[0] == "HTTP/1.1" and parts[1] in ("200","400","503")
                       and "host" not in headers and 0 < count <= REPLY_MAX, "PLACEMENT_RESPONSE_FRAME")
                response = await H._body(reader, count); self._used["observed_incoming"] += len(response)
                F.need(await reader.read(1) == b"", "PLACEMENT_TRAILING_RESPONSE")
                value = F.strict(response, REPLY_MAX)
                F.need(F.compact(value) == response, "PLACEMENT_RESPONSE_CANONICAL")
                if parts[1] != "200":
                    F.fields(value, ("schema","status","code","mathematical_acceptance"))
                    F.need(value["schema"] == ERROR_SCHEMA and value["status"] == "REFUSED_OR_INCOMPLETE"
                           and value["code"] in ERRORS and value["mathematical_acceptance"] is False,
                           "PLACEMENT_RESPONSE_ERROR")
                    raise PlacementWireError(value["code"], uncertain=route == SUBMIT)
                F.fields(value, ("schema","status","bindings","request_id","placement","route","mathematical_acceptance"))
                F.need(value["schema"] == RESPONSE_SCHEMA and value["status"] == "OBSERVED"
                       and value["bindings"] == self._expected and value["request_id"] == rid
                       and value["mathematical_acceptance"] is False, "PLACEMENT_EXPECTED_RESPONSE")
                checked = public_response({"placement":value["placement"],"route":value["route"]}, self._expected, rid, projected=True)
                F.need(checked == value, "PLACEMENT_RESPONSE_PROJECTION")
                if manifest is not None and value["placement"]["phase"] == "RECEIPT_COMMITTED":
                    receipt = value["placement"]["outcome"]
                    for key in ("export_id","export_object_sha256","export_object_bytes","packet_sha256","packet_bytes","retention_end_ms"):
                        F.need(receipt[key] == manifest[key], "PLACEMENT_SUBMITTED_OBJECT_BINDING")
                    F.need(receipt["route"]["cell"] == manifest["cell"], "PLACEMENT_SUBMITTED_CELL")
                    F.need([body["body_hash"] for body in receipt["bodies"]]
                           == [body["body_hash"] for body in manifest["bodies"]]
                           and all(actual["response_bytes"] <= requested["max_bytes"]
                                   for actual,requested in zip(receipt["bodies"],manifest["bodies"])),
                           "PLACEMENT_SUBMITTED_BODIES")
                self._active(); F.need(time.monotonic() < until, "PLACEMENT_CLIENT_REPLY_EXPIRED")
        except asyncio.CancelledError:
            record_uncertainty()
            raise
        except Exception as error:
            failure = PlacementWireError(error.code,
                uncertain=route == SUBMIT or error.uncertain) if type(error) is PlacementWireError else PlacementWireError(
                "TRANSPORT_OR_RESPONSE_FAILURE", uncertain=route == SUBMIT)
        finally:
            try:
                if writer is not None:
                    try:
                        writer.close()
                        async with asyncio.timeout(1): await writer.wait_closed()
                    except asyncio.CancelledError:
                        record_uncertainty()
                        self.closed = True; self._used["cleanup_errors"] += 1; raise
                    except Exception: cleanup_failed = True; self.closed = True; self._used["cleanup_errors"] += 1
            finally:
                self._busy = False
        if cleanup_failed: failure = PlacementWireError("CLEANUP_UNCERTAIN", uncertain=route == SUBMIT)
        if failure is not None:
            record_uncertainty()
            raise failure from None
        return {"response":value, "acknowledgement":"PEER_ACKNOWLEDGED" if self._endpoint.tls else "LOOPBACK_RESPONSE_OBSERVED",
                "transport_assurance":"SYSTEM_CA_TLS_OWNER_SELECTED_PEER" if self._endpoint.tls else "EXPLICIT_PLAINTEXT_LOOPBACK_TEST",
                "mathematical_acceptance":False}

    def close(self):
        F.need(not self._busy, "PLACEMENT_CLIENT_ACTIVE")
        self.closed = True

    def report(self):
        return dict(expected=deepcopy(self._expected), endpoint=self._endpoint.label, used=dict(self._used),
                    closed=self.closed, active=self._busy, mathematical_acceptance=False,
                    scope="OWNER_SELECTED_CONTACT_NOT_DHT_AUTHORITY_NO_AUTOMATIC_RETRY")

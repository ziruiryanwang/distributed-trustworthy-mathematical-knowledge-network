"""Explicit native-delta offers/acquisition alongside unchanged formal indexes.

Composite providers may advertise existing formal-index roles because they
actually serve those indexes. No generic custody routing or receipt ABI change.
Owner hard containment and egress policy remain required; HTTP is read-only.
"""
import asyncio
from copy import deepcopy
import math
import ssl
import time

from custody.module_store import ModuleStore
from discovery import formal_features as F
from discovery import candidate_query as Q
from discovery.module_export_adapter import ModuleExportAdapter
from location import protocol as P
from location.workflow import _LocatedSearchClient
from location.controller_services import ServiceLocationProcess, ServiceLocatedWorkflow
from transport.clients import configured
from transport.located_receipts import _ExpiringContact
from transport.receipt_client import AcquisitionBudget, _SharedAcquisition
from transport import http_provider_receipts as H
from .custody import PacketStore, MAX_PACKET, profile_id, packet_digest, offer_request, blob_request, verify_offer
from .receiver import DeltaVerifier

OFFER_ROUTE = "/v5/modules/delta-offer"
PACKET_ROUTE = "/v5/modules/delta-packet"
ROUTES = {key: value for key, value in H.ROUTES.items()
          if key not in (H.RECEIPT_ROUTE, H.RECEIPT_OFFER_ROUTE)}
ROUTES.update({OFFER_ROUTE: 16384, PACKET_ROUTE: MAX_PACKET})


async def exchange(endpoint, route, request, max_reply_bytes, timeout_ms):
    """New delta routes only, sharing frozen HTTP framing and TLS policy."""
    endpoint.validate()
    F.need(route in (OFFER_ROUTE, PACKET_ROUTE), "DELTA_HTTP_ROUTE")
    F.uint(max_reply_bytes, 1, ROUTES[route]); F.uint(timeout_ms, 1, 60000)
    if route == OFFER_ROUTE: offer_request(request)
    else:
        blob_request(request)
        F.need(max_reply_bytes == request["packet_bytes"], "DELTA_HTTP_EXACT_REPLY_CAP")
    raw = F.compact(request); F.need(0 < len(raw) <= H.REQUEST_MAX, "DELTA_HTTP_REQUEST_BYTES")
    host = "["+endpoint.host+"]" if ":" in endpoint.host else endpoint.host
    head = H._header("POST "+route+" HTTP/1.1", len(raw), host+":"+str(endpoint.port))
    context = None
    if endpoint.tls:
        context = ssl.create_default_context(cafile=endpoint.ca_file)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
    writer = None; started = time.monotonic()
    try:
        async with asyncio.timeout(timeout_ms/1000):
            kwargs = {"ssl": context, "limit": H.HEADER_MAX}
            if endpoint.tls:
                kwargs.update(server_hostname=endpoint.server_name or endpoint.host,
                              ssl_handshake_timeout=timeout_ms/1000, ssl_shutdown_timeout=1)
            reader, writer = await asyncio.open_connection(endpoint.host, endpoint.port, **kwargs)
            await H._write(writer, head); await H._write(writer, raw)
            first, headers, count, incoming = await H._headers(reader,
                "application/octet-stream" if route == PACKET_ROUTE else "application/json")
            if route == PACKET_ROUTE:
                F.need(count == request["packet_bytes"], "DELTA_HTTP_EXACT_CONTENT_LENGTH")
            parts = first.split(" ")
            F.need(len(parts) >= 3 and parts[0] == "HTTP/1.1" and parts[1] in ("200", "400", "404", "503"),
                   "DELTA_HTTP_STATUS")
            F.need("host" not in headers and count <= max_reply_bytes, "DELTA_HTTP_RESPONSE_BOUND")
            body = await H._body(reader, count)
            F.need(await reader.read(1) == b"", "DELTA_HTTP_TRAILING_RESPONSE")
            return {"status": int(parts[1]), "raw": body, "request_bytes": len(raw),
                    "reply_bytes": len(body), "header_bytes": len(head)+incoming,
                    "elapsed_ms": int((time.monotonic()-started)*1000)}
    finally:
        if writer is not None:
            writer.close()
            try:
                async with asyncio.timeout(1): await writer.wait_closed()
            except Exception: pass


class CompositeProvider(H.Provider):
    """Same index/group/body service plus distinctly typed packet custody.

    Base start/stop, counters and existing dispatch are reused. Only the closed
    route/framing loop is a successor, because its frozen receipt-only constants
    cannot safely be monkeypatched. No receipt endpoint is served here.
    """
    def __init__(self, *, index, custody, packets, **limits):
        F.need(index is not None and type(custody) is ModuleStore and type(packets) is PacketStore,
               "DELTA_COMPOSITE_ACTUAL_ROLES")
        F.need(index.adapter.foundation == custody.foundation == packets.profile["foundation"]
               and index.adapter.policy == custody.policy == packets.profile["policy"],
               "DELTA_COMPOSITE_PROFILE")
        self.packets = packets
        super().__init__(index=index, custody=custody, **limits)

    def dispatch(self, route, request, *, check_budget=None):
        F.need(route in ROUTES, "DELTA_COMPOSITE_ROUTE")
        if route not in (OFFER_ROUTE, PACKET_ROUTE):
            return super().dispatch(route, request, check_budget=check_budget)
        if check_budget is not None: check_budget()
        if route == OFFER_ROUTE:
            offer_request(request); result = self.packets.offer(request)
        else:
            blob_request(request); result = self.packets.get(request["packet_sha256"], request["packet_bytes"])
        if check_budget is not None: check_budget()
        return result

    async def _serve(self, reader, writer):
        task = asyncio.current_task()
        if len(self.tasks) >= self.max_connections or self.requests >= self.max_requests:
            self.refused += 1; writer.close(); return
        self.tasks.add(task); self.requests += 1
        reservation = 0; until = time.monotonic()+self.operation_ms/1000
        try:
            async with asyncio.timeout(self.operation_ms/1000):
                first, headers, count, header_count = await H._headers(reader)
                self.header_bytes += header_count
                parts = first.split(" ")
                F.need(len(parts) == 3 and parts[0] == "POST" and parts[2] == "HTTP/1.1"
                       and parts[1] in ROUTES and "host" in headers, "DELTA_HTTP_REQUEST_LINE")
                route = parts[1]; F.need(0 < count <= H.REQUEST_MAX, "DELTA_HTTP_REQUEST_BOUND")
                raw = await H._body(reader, count); self.request_bytes += len(raw)
                request = F.strict(raw, H.REQUEST_MAX)
                if route in (OFFER_ROUTE, PACKET_ROUTE):
                    F.need(F.compact(request) == raw, "DELTA_HTTP_REQUEST_CANONICAL")
                reservation = ROUTES[route]
                if route == OFFER_ROUTE:
                    offer_request(request); reservation = request["max_bytes"]
                elif route == PACKET_ROUTE:
                    blob_request(request); reservation = request["packet_bytes"]
                elif route == H.CANDIDATE_ROUTE:
                    Q.validate_request(request); reservation = request["limits"]["bytes"]
                elif route == H.OFFER_ROUTE:
                    H._offer_request(request); reservation = request["max_bytes"]
                elif route == H.COMPACT_SUMMARY_ROUTE:
                    F.fields(request, ("snapshot_id", "features", "max_bytes", "max_expanded_bytes"))
                    reservation = F.uint(request["max_bytes"], 1024, ROUTES[route])
                    F.uint(request["max_expanded_bytes"], 1024, 1048576)
                F.need(self.reply_bytes+self.reserved_reply_bytes+reservation <= self.max_reply_bytes,
                       "DELTA_PROVIDER_REPLY_QUOTA")
                self.reserved_reply_bytes += reservation
                try:
                    def check_budget():
                        F.need(time.monotonic() < until, "DELTA_PROVIDER_DEADLINE")
                    if route == H.CANDIDATE_ROUTE:
                        check_budget()
                        request["limits"]["timeout_ms"] = min(request["limits"]["timeout_ms"],
                            max(1, int((until-time.monotonic())*1000)))
                    value = self.dispatch(route, request, check_budget=check_budget)
                    body = value if route in (H.COMPACT_SUMMARY_ROUTE, H.OFFER_ROUTE, PACKET_ROUTE) else F.compact(value)
                    F.need(len(body) <= reservation, "DELTA_PROVIDER_RESPONSE_BYTES"); check_budget()
                    head = H._header("HTTP/1.1 200 OK", len(body),
                        media="application/octet-stream" if route == PACKET_ROUTE else "application/json")
                    self.reply_bytes += len(body); self.header_bytes += len(head)
                    await H._write(writer, head); await H._write(writer, body)
                finally:
                    self.reserved_reply_bytes -= reservation; reservation = 0
        except Exception:
            self.failures += 1
        finally:
            writer.close()
            try:
                try:
                    async with asyncio.timeout(1): await writer.wait_closed()
                except Exception: pass
            finally: self.tasks.discard(task)


class DeltaLocatedHandoff:
    """Prepay exact existing location/search grants before its fresh child starts.

    The caller starts/closes the actual channel and uses this actual location
    object for route/descriptor calls. There is no second location protocol or
    search budget. One begin_search and one acquisition handoff may be issued.
    """
    def __init__(self, channel, adapter, features, policy, budget, location_limits, search_limits):
        F.need(type(budget) is AcquisitionBudget, "DELTA_HANDOFF_EXACT_BUDGET")
        budget.active()
        F.need(type(channel) is ServiceLocationProcess and channel.deadline == budget.deadline
               and channel.config["role"] == "reader" and channel.process is None
               and channel._start_task is None and channel._spawn_task is None and channel._close_task is None
               and channel.sequence == channel.sent == channel.received == channel.read_frames == 0
               and channel.stderr_task is None and not channel.stderr and not channel.channel_failed
               and not channel.closed, "DELTA_HANDOFF_FRESH_READER")
        F.need(type(adapter) is ModuleExportAdapter and type(policy) is P.OwnerEgressPolicy,
               "DELTA_HANDOFF_ADAPTER_POLICY")
        F.need(channel.config["namespace"] == adapter.namespace and channel.config["egress"] == policy._config,
               "DELTA_HANDOFF_CHANNEL_PROFILE")
        self.channel, self.adapter, self.policy, self.budget = channel, adapter, policy, budget
        self.location = ServiceLocatedWorkflow(channel, adapter.namespace, features, location_limits, search_limits, policy)
        self._origin = channel, self.location, self.location._workflow, budget, adapter, policy
        self._deadline = budget.deadline
        self._location_deadline = self.location._workflow._deadline
        self._config = F.compact(channel.config)
        self._grants = F.compact({"location": location_limits, "search": search_limits})
        self._query = adapter.namespace, tuple(F.validate_features(features, 8))
        attempts = location_limits["route_operations"]+location_limits["descriptor_requests"]+search_limits["requests"]
        # Existing workflow validates that reply_bytes includes the entire
        # search byte ceiling. Charge once before caller can dispatch anything.
        budget.charge_external("delta-location-and-search", attempts, location_limits["reply_bytes"])
        self._prepaid = F.compact(budget.external)
        self._search = None; self._search_deadline = None; self._issued = False
        self._check()

    def _check(self):
        channel, location, workflow, budget, adapter, policy = self._origin
        F.need(self.channel is channel and self.location is location and location._workflow is workflow
               and self.budget is budget and location.channel is channel
               and self.adapter is adapter and self.policy is policy, "DELTA_HANDOFF_ORIGIN_CHANGED")
        budget.active()
        F.need(channel.deadline == budget.deadline == self._deadline and not channel.closed and not channel.channel_failed
               and workflow._deadline == self._location_deadline
               and self._location_deadline <= self._deadline, "DELTA_HANDOFF_ORIGINAL_DEADLINE")
        F.need(F.compact(channel.config) == self._config and F.compact(budget.external) == self._prepaid
               and F.compact({"location": workflow._limits, "search": workflow._search_limits}) == self._grants,
               "DELTA_HANDOFF_CONFIG_OR_PREPAY_CHANGED")
        F.need(channel.config["namespace"] == self.adapter.namespace
               and channel.config["egress"] == self.policy._config
               and (workflow._namespace, workflow._features) == self._query, "DELTA_HANDOFF_POLICY_CHANGED")
        if self._search is not None:
            F.need(workflow._search_client is self._search
                   and self._search.session.deadline == self._search_deadline
                   and self._search_deadline <= self._deadline, "DELTA_HANDOFF_SEARCH_ORIGIN_OR_DEADLINE")

    def begin_search(self):
        self._check(); F.need(self._search is None and not self._issued, "DELTA_HANDOFF_SEARCH_ALREADY_ISSUED")
        search = self.location.begin_search()
        F.need(type(search) is _LocatedSearchClient and search.session.deadline <= self._deadline,
               "DELTA_HANDOFF_ACTUAL_SEARCH")
        self._search, self._search_deadline = search, search.session.deadline
        self._check()
        return search


class DeltaAcquisition:
    """One fixed workflow budget for exact bytes and actual native-delta admission.

    Caller precharges any prior location/search suballocation BEFORE starting it.
    No automatic provider selection, retry, download or verifier configuration.
    All stores are structural; only the exact live DeltaVerifier grants authority.
    """
    def __init__(self, adapter, endpoints, profile, budget, module_custody, packet_custody, *, verifier=None):
        F.need(type(budget) is AcquisitionBudget, "DELTA_ACQUISITION_EXACT_BUDGET")
        budget.active(); self.budget = budget
        self.profile = deepcopy(profile); self.profile_id = profile_id(profile)
        F.need(type(module_custody) is ModuleStore and type(packet_custody) is PacketStore,
               "DELTA_ACQUISITION_ACTUAL_CUSTODY")
        F.need(adapter.foundation == module_custody.foundation == profile["foundation"]
               and adapter.policy == module_custody.policy == profile["policy"]
               and packet_custody.profile_id == self.profile_id, "DELTA_ACQUISITION_PROFILE")
        if verifier is not None:
            F.need(type(verifier) is DeltaVerifier
                   and (verifier._image, verifier._foundation, verifier._policy)
                   == (profile["image"], profile["foundation"], profile["policy"]),
                   "DELTA_ACQUISITION_REAL_OWNER_VERIFIER")
            verifier._active()
        self.adapter, self.modules, self.packets = adapter, module_custody, packet_custody
        self.verifier = verifier; self.endpoints = configured(endpoints)
        self._origin_verifier = verifier
        self._origin_deadline = budget.deadline
        self._search = self._handoff = None; self._offers = set(); self.closed = False
        self.structural = _SharedAcquisition(adapter, self.endpoints, budget)
        self.http = {"completed_requests": 0, "failed_requests": 0, "request_bytes": 0,
                     "reply_bytes": 0, "header_bytes": 0, "unknown_header_upper_bound": 0,
                     "unknown_request_body_upper_bound": 0}

    @classmethod
    def from_search(cls, handoff, profile, module_custody, packet_custody, *, verifier=None):
        """Use actual existing location/search contacts; no uncharged holder referral.

        The exact prospective handoff charged the full actual configured grants
        before its fresh child could start. No arbitrary prepaid ledger suffices.
        """
        F.need(type(handoff) is DeltaLocatedHandoff, "DELTA_ACQUISITION_EXACT_PROSPECTIVE_HANDOFF")
        handoff._check()
        search, policy, budget, adapter = handoff._search, handoff.policy, handoff.budget, handoff.adapter
        F.need(type(search) is _LocatedSearchClient and not handoff._issued
               and search is handoff.location._workflow._search_client
               and not search.session.pending, "DELTA_ACQUISITION_SAME_UNCONSUMED_SEARCH")
        handoff._issued = True  # Even failed handoff attempts do not renew it.
        endpoints = {}
        for name, endpoint in search.endpoints.items():
            F.need(endpoint == search._adopted_endpoints[name], "DELTA_SEARCH_CONTACT_CHANGED")
            expires = min(budget.deadline, search._expiries[name])
            if time.monotonic() < expires:
                endpoints[name] = _ExpiringContact(endpoint, expires, policy, budget)
        F.need(endpoints, "DELTA_SEARCH_NO_LIVE_CONTACT")
        result = cls(adapter, endpoints, profile, budget, module_custody, packet_custody, verifier=verifier)
        result._search, result._handoff = search, handoff
        handoff._check()
        return result

    def _active(self):
        F.need(not self.closed and self.verifier is self._origin_verifier
               and self.budget.deadline == self._origin_deadline, "DELTA_ACQUISITION_ORIGIN_OR_CLOSED")
        self.budget.active()
        if self._handoff is not None:
            self._handoff._check()
            F.need(self._search is self._handoff._search, "DELTA_ACQUISITION_SEARCH_ORIGIN_CHANGED")

    async def _get(self, provider, route, request, maximum):
        self._active(); F.need(provider in self.endpoints, "DELTA_ENDPOINT_NOT_CONFIGURED")
        ticket = self.budget.begin(maximum); charged = None; measured = False
        try:
            response = await exchange(self.endpoints[provider], route, request, maximum, self.budget.remaining_ms())
            charged = len(response["raw"]); measured = True
            self.http["completed_requests"] += 1
            for key in ("request_bytes", "reply_bytes", "header_bytes"): self.http[key] += response[key]
            F.need(response["status"] == 200, "DELTA_HTTP_ERROR")
            self._active(); return response["raw"]
        except BaseException:
            self.http["failed_requests"] += 1
            if not measured:
                self.http["unknown_header_upper_bound"] += 2*H.HEADER_MAX
                self.http["unknown_request_body_upper_bound"] += H.REQUEST_MAX
            raise
        finally: self.budget.settle(ticket, charged)

    async def export(self, provider, record):
        self._active()
        if self._search is not None:
            F.need((record["object_id"], F.record_id(record)) in self._search.session.seen_candidates,
                   "DELTA_CANDIDATE_NOT_RETURNED_BY_ORIGINATING_SEARCH")
        resolved = await self.structural.export(provider, record)
        loc = resolved["locator"]
        self.modules.put_group(loc["module_id"], resolved["opening"], before_commit=self._active)
        held, unused = self.modules.get_group(loc["module_id"], loc["relative_name"], loc["group_index"])
        F.need(held == resolved["opening"], "DELTA_GROUP_COMMIT_READBACK")
        self._active()
        # The underlying descriptor adapter's historical receipt next-gate text
        # is not authority. State the correct distinct gate for this workflow.
        return {**resolved, "next_gate": "ACTUAL_COMPLETE_DELTA_RECEIVE_BEFORE_MATHEMATICAL_USE"}

    async def body(self, provider, resolved, digest, maximum):
        self._active()
        result = await self.structural.body(provider, resolved, digest, maximum)
        loc = resolved["locator"]; response = result["body"]
        self.modules.put_body(loc["module_id"], loc["relative_name"], response, before_commit=self._active)
        held = self.modules.get_body(loc["module_id"], loc["relative_name"], response["universes"], digest)
        F.need(held == response, "DELTA_BODY_COMMIT_READBACK")
        self._active(); return result

    async def offers(self, provider, module, *, max_offers=4, max_bytes=4096):
        request = {"module_id": F.hexid(module), "wire_profile_id": self.profile_id,
                   "max_offers": max_offers, "max_bytes": max_bytes}
        raw = await self._get(provider, OFFER_ROUTE, request, max_bytes)
        value = F.strict(raw, max_bytes); F.need(F.compact(value) == raw, "DELTA_OFFER_CANONICAL")
        result = verify_offer(value, request)
        for row in result["packets"]:
            self._offers.add((provider, module, row["packet_sha256"], row["packet_bytes"]))
        self._active(); return result

    async def packet(self, provider, module, entry):
        self._active(); F.hexid(module); blob_request(entry)
        F.need((provider, module, entry["packet_sha256"], entry["packet_bytes"]) in self._offers,
               "DELTA_PACKET_NOT_OFFERED_BY_SELECTED_PROVIDER")
        raw = await self._get(provider, PACKET_ROUTE, entry, entry["packet_bytes"])
        F.need(len(raw) == entry["packet_bytes"] and packet_digest(raw) == entry["packet_sha256"],
               "DELTA_PACKET_HASH_BINDING")
        self.packets.put(module, raw, before_commit=self._active)
        F.need(self.packets.get(entry["packet_sha256"], entry["packet_bytes"]) == raw,
               "DELTA_PACKET_COMMIT_READBACK")
        self._active()
        return {**deepcopy(entry), "module_id": module, "wire_profile_id": self.profile_id,
                "assurance": "EXACT_UNTRUSTED_DELTA_PACKET_CUSTODIED", "mathematical_acceptance": False}

    def custody_ready(self, resolved, entry, demanded_bodies=()):
        self._active(); blob_request(entry)
        loc = resolved["locator"]; module, name = loc["module_id"], loc["relative_name"]
        opening, descriptor = self.modules.get_group(module, name, loc["group_index"])
        F.need(opening == resolved["opening"] and descriptor == resolved["descriptor"], "DELTA_SELECTED_GROUP")
        F.need(type(demanded_bodies) in (list, tuple) and len(demanded_bodies) <= 16384,
               "DELTA_DEMANDED_BODY_SET")
        for digest in demanded_bodies: F.hexid(digest)
        F.need(len(set(demanded_bodies)) == len(demanded_bodies), "DELTA_DUPLICATE_BODY_DEMAND")
        for digest in demanded_bodies:
            self.modules.get_body(module, name, descriptor["universes"], digest)
        raw = self.packets.get(entry["packet_sha256"], entry["packet_bytes"])
        target, census = self.packets.inspect(module, raw)
        F.need(target == opening["summary"], "DELTA_PACKET_SEMANTIC_SUMMARY")
        self._active()
        return {"status": "SELECTED_PACKET_AND_SEMANTICS_DURABLY_READ_BACK", "module_id": module,
                "packet_sha256": entry["packet_sha256"], "census": census,
                "demanded_bodies": list(demanded_bodies), "cross_database_atomic": False,
                "all_future_bodies_covered": False, "mathematical_acceptance": False}

    def admit(self, resolved, entry, *, demanded_bodies=(), native_cpu_seconds=30,
              receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024):
        self._active(); F.need(type(self.verifier) is DeltaVerifier, "DELTA_REAL_OWNER_VERIFIER_REQUIRED")
        F.uint(native_cpu_seconds, 1, 600); F.uint(receipt_cpu_seconds, 1, 600)
        F.uint(wall_seconds, 1, 600); F.uint(memory_mib, 64, 4096)
        held = self.custody_ready(resolved, entry, demanded_bodies)
        raw = self.packets.get(entry["packet_sha256"], entry["packet_bytes"])
        census = held["census"]
        reserved = census["frontiers"]*receipt_cpu_seconds+census["deltas"]*native_cpu_seconds
        # This reuses the original conservative <=600 CPU per-verification
        # workflow envelope. It does not grant a fresh CPU allowance per delta.
        self.budget.verification(len(raw), reserved)
        remaining = min(wall_seconds, math.floor(self.budget.deadline-time.monotonic()))
        F.need(remaining >= 1, "DELTA_ACQUISITION_VERIFY_DEADLINE")
        handle = None
        try:
            handle = self.verifier.receive(raw, resolved["opening"]["summary"],
                native_cpu_seconds=native_cpu_seconds, receipt_cpu_seconds=receipt_cpu_seconds,
                wall_seconds=remaining, memory_mib=memory_mib)
            group = self.verifier.open_group(handle, resolved["opening"])
            retained = self.custody_ready(resolved, entry, demanded_bodies)
            self._active()
            return {"handle": handle, "group": group, "custody": retained,
                    "assurance": "LIVE_LOCALLY_CHECKED_DELTA_WITH_SELECTED_COMPONENT_CUSTODY"}
        except BaseException:
            if handle is not None: self.verifier.close()
            raise

    def report(self):
        return {"budget": self.budget.report(), "delta_http": dict(self.http),
                "structural_http": self.structural.report(), "wire_profile_id": self.profile_id,
                "proof_form": "bounded-native-delta-v1", "closed": self.closed,
                "worker_reservations_scope": "NESTED_WORKFLOW_AND_VERIFIER_CONSTRAINTS_NOT_ADDITIVE_ACTUAL_CPU",
                "mathematical_acceptance": False}

    def close(self):
        F.need(self.budget.pending is None and self.structural.inflight == 0, "DELTA_ACQUISITION_PENDING")
        if self.closed: return
        self.closed = True; self.budget.closed = True
        if self.verifier is not None: self.verifier.close()

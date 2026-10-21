"""Finite exact-demand custody hints on the original located client operation.

Trusted-owner composition, not a new acquisition/checking authority. The facade
owns serialization, source pins and fail-stop; the reader owns semantic staging.
No search contact map is changed, and no child or budget is created here.
"""
import base64
from copy import deepcopy
import secrets
import time

from custody.module_store import permitted_hashes
from discovery import formal_features as F
from evidence_network.transport import EvidenceAcquisition
from location import observed_route as OR, protocol as P
from location.controller_services import ServiceLocationProcess
from modules import codec as C
from transport.receipt_client import AcquisitionBudget, _SharedAcquisition

SCHEMA = "DMKN_V5_BODY_LOCATION_ALLOWANCE_V1"
LIMITS = {"route_operations": (1, 16), "routing_events": (1, 4096),
          "routing_peer_slots": (1, 128), "descriptor_requests": (1, 32),
          "capabilities": (1, 32)}
COUNTERS = ("route_operations_issued", "routing_events_reserved",
            "routing_peer_slots_reserved", "descriptor_requests_issued",
            "descriptor_reply_bytes_reserved", "descriptor_reply_bytes_observed",
            "capabilities_issued", "capabilities_consumed", "body_attempts",
            "body_successes", "settled_unavailable")


class BodySupplier:
    """Opaque local identity; construction alone grants no membership."""
    __slots__ = ()


def _domain(client):
    adapter, store = client.workspace.adapter, client.workspace.modules
    profile = client.workspace.config["wire_profile"]
    F.need(adapter.codec is store.codec is C and C.SPEC_SCHEMA == "DMKN_MODULE_SPEC_V1"
           and adapter.foundation == store.foundation == profile["foundation"]
           and adapter.policy == store.policy == profile["policy"],
           "BODY_LOCATION_SEMANTIC_OWNERS")
    return {"foundation": F.hexid(store.foundation), "policy": F.hexid(store.policy)}


def _milliseconds(until):
    remaining = int((until-time.monotonic())*1000)
    F.need(remaining >= 1, "BODY_LOCATION_ORIGINAL_DEADLINE")
    return min(3600000, remaining)


def _quiescent(client):
    a, s = client._acquisition, client._search
    F.need(a is not None and s is not None and a.budget.pending is None
           and a.structural.inflight == a.structural.reserved_bytes == 0
           and not s.session.pending and not any(s.session.reserved.values()),
           "BODY_LOCATION_SERIALIZED_SETTLED_OWNERS")


def _uncertain_channel(channel):
    if (channel.channel_failed or channel.forced_termination
        or channel.process is not None and channel.process.returncode not in (None, 0)):
        return True
    closing = channel._close_task
    # A zero process exit does not certify the parent's final source-pin checks.
    # Read only the already-owned task state; do not start/wait/retry cleanup.
    return closing is not None and (not closing.done() or closing.cancelled()
                                   or closing.exception() is not None)


class _Demand:
    """One shared immutable-byte selection for a finite located result set."""
    def __init__(self, pool, reader, demand):
        from .semantic_reader import SemanticReader
        c = pool.client
        F.need(type(reader) is SemanticReader and reader._client is c
               and reader._grant is pool.grant and reader._state == "COLLECTING"
               and reader._busy and c._busy, "BODY_LOCATION_ACTUAL_ACTIVE_READER")
        reader._active()
        chosen, address = reader._demand(demand)
        F.need(chosen["kind"] == "NeedBody" and address in reader._names
               and chosen["module"] in reader._members,
               "BODY_LOCATION_RESOLVED_SELECTED_DEMAND")
        candidate, held = reader._names[address]
        provider, resolved = c._candidate(candidate)
        description = C.canonical({"provider": provider, **resolved})
        F.need(description == held
               and reader._supplier_names.get((provider, *address)) == (candidate, held),
               "BODY_LOCATION_ORIGINAL_CANDIDATE")
        loc, descriptor = resolved["locator"], resolved["descriptor"]
        F.need(loc["module_id"] == chosen["module"]
               and C.name_key(loc["relative_name"]) == address[1]
               and descriptor["universes"] == chosen["universes"]
               and chosen["body_hash"] in permitted_hashes(descriptor),
               "BODY_LOCATION_DESCRIPTOR_COMMITMENT")
        member = reader._members[chosen["module"]]
        F.need(resolved["opening"]["summary"] == C.parse_json(member[1])["summary"],
               "BODY_LOCATION_SELECTED_MEMBER_SUMMARY")
        C.verify_group_opening(chosen["module"], resolved["opening"])
        key = chosen["module"], chosen["universes"], chosen["body_hash"]
        F.need(key not in reader._bodies, "BODY_LOCATION_ALREADY_STAGED")
        a = c._acquisition
        F.need(type(a) is EvidenceAcquisition and type(a.structural) is _SharedAcquisition
               and a.budget is a.structural.budget is pool.budget
               and a.adapter is a.structural.adapter is c.workspace.adapter
               and a.modules is c.workspace.modules and a.packets is c.workspace.packets
               and a.verifier is None and a.structural.local_custody is None
               and a._search is c._search and a._handoff is None and not a.closed,
               "BODY_LOCATION_ORIGINAL_ACQUISITION")
        self.pool, self.reader, self.candidate = pool, reader, candidate
        self.search, self.acquisition, self.structural = c._search, a, a.structural
        self.grant, self.budget = pool.grant, pool.budget
        self.address, self.key, self.member = address, key, member
        self.demand_raw, self.held = C.canonical(chosen), held
        self.provider, self.resolved = provider, resolved
        self.endpoints, self.structural_endpoints = dict(a.endpoints), dict(a.structural.endpoints)
        self.deadlines = (self.search.session.deadline, a.structural.deadline, pool.deadline)
        self.request = {"module_id": chosen["module"], "relative_name": deepcopy(chosen["name"]),
                        "universes": chosen["universes"], "body_hash": chosen["body_hash"]}
        self.ref = P.body_ref({"module_id": chosen["module"],
            "export_id": C.export_id(chosen["module"], chosen["name"]),
            "universes": chosen["universes"], "body_hash": chosen["body_hash"]})
        self.route_key = P.body_route_key(pool.namespace, self.ref)
        self._request_raw, self._ref_raw = C.canonical(self.request), C.canonical(self.ref)

    def check(self):
        p, c, r, a, s = self.pool, self.pool.client, self.reader, self.acquisition, self.structural
        p.check()
        F.need(r._client is c and r._grant is self.grant is p.grant
               and r._state == "COLLECTING" and r._busy and c._busy
               and r._search is c._search is self.search
               and r._acquisition is c._acquisition is a and not a.closed,
               "BODY_LOCATION_READER_GENERATION_CHANGED")
        F.need(a.structural is s and a.budget is s.budget is self.budget is p.budget
               and a.adapter is s.adapter is c.workspace.adapter
               and a.modules is c.workspace.modules and a.packets is c.workspace.packets
               and a.verifier is None and s.local_custody is None
               and a._search is self.search and a._handoff is None
               and a.endpoints == self.endpoints and s.endpoints == self.structural_endpoints,
               "BODY_LOCATION_ACQUISITION_CHANGED")
        F.need((self.search.session.deadline, s.deadline, p.deadline) == self.deadlines
               and s.request_cap == p.budget.limits["requests"]
               and s.byte_cap == p.budget.limits["reply_bytes"], "BODY_LOCATION_CAPS_CHANGED")
        F.need(self.demand_raw in r._pending and self.key not in r._bodies
               and r._members.get(self.key[0]) == self.member
               and r._names.get(self.address) == (self.candidate, self.held)
               and r._supplier_names.get((self.provider, *self.address)) == (self.candidate, self.held),
               "BODY_LOCATION_DEMAND_NO_LONGER_CURRENT")
        provider, resolved = c._candidate(self.candidate)
        F.need(provider == self.provider and resolved is self.resolved
               and C.canonical({"provider": provider, **resolved}) == self.held
               and C.canonical(self.request) == self._request_raw
               and C.canonical(self.ref) == self._ref_raw
               and P.body_route_key(p.namespace, self.ref) == self.route_key,
               "BODY_LOCATION_EXACT_DEMAND_CHANGED")
        a._active(); s._deadline()

    def invalidated(self):
        """No facade action or clock/egress check: safe even during report/close."""
        p, c, r = self.pool, self.pool.client, self.reader
        return (p.closed or getattr(c, "_closed", False) or getattr(c, "_state", None) != "OPEN"
            or _uncertain_channel(p.channel)
            or getattr(c, "_cleanup_uncertain", False)
            or r._state != "COLLECTING" or c._search is not self.search
            or c._acquisition is not self.acquisition or self.acquisition.closed
            or self.demand_raw not in r._pending or self.key in r._bodies
            or r._members.get(self.key[0]) != self.member
            or r._names.get(self.address) != (self.candidate, self.held))


class _BodyContact:
    """One exact attempt's endpoint-compatible guard, never a contact-map row."""
    def __init__(self, attempt, endpoint, expires, policy, budget):
        self._binding, self._endpoint, self._expires = attempt, endpoint, expires
        self._policy, self._budget = policy, budget

    @property
    def host(self): return self._endpoint.host
    @property
    def port(self): return self._endpoint.port
    @property
    def tls(self): return self._endpoint.tls
    @property
    def server_name(self): return self._endpoint.server_name
    @property
    def ca_file(self): return self._endpoint.ca_file
    @property
    def label(self): return self._endpoint.label

    def validate(self):
        self._binding.validate()
        return self


class _BodyAttempt:
    """Closed bridge to the one retained transport engine; pool issues it only."""
    def __init__(self, pool, token, entry):
        self.pool, self.token, self._entry = pool, token, entry
        context = entry["context"]
        self.context = context
        self.acquisition, self.structural, self.budget = context.acquisition, context.structural, pool.budget
        self.resolved, self.digest, self.request = context.resolved, context.key[2], deepcopy(context.request)
        self.route_key = context.route_key
        self.supplier = entry["supplier"]
        self.contact = _BodyContact(self, entry["endpoint"], entry["expires"], pool.policy, pool.budget)
        self._contact, self._ticket, self._settled, self._finished = self.contact, None, False, False

    def validate(self, *, check_expiry=True):
        F.need(type(check_expiry) is bool, "BODY_LOCATION_EXPIRY_MODE")
        p, row, context, contact = self.pool, self._entry, self.context, self.contact
        F.need(type(self) is _BodyAttempt and type(p) is _BodyPool
               and not self._finished and p._entries.get(self.token) is row
               and row["state"] == "ATTEMPTING" and row["attempt"] is self
               and row["context"] is context and type(contact) is _BodyContact
               and contact is self._contact and contact._binding is self,
               "BODY_LOCATION_PRIVATE_ATTEMPT")
        context.check()
        F.need(self.acquisition is context.acquisition and self.structural is context.structural
               and self.budget is p.budget and self.resolved is context.resolved
               and self.digest == context.key[2] and self.request == context.request
               and self.route_key == context.route_key
               and self.supplier == row["supplier"] and contact._endpoint is row["endpoint"]
               and contact._expires == row["expires"] and contact._policy is p.policy
               and contact._budget is p.budget, "BODY_LOCATION_ATTEMPT_BINDING_CHANGED")
        if check_expiry:
            F.need(time.monotonic() < row["expires"], "BODY_LOCATION_CAPABILITY_EXPIRED")
            endpoint = row["endpoint"]
            checked = p.policy.endpoint({"host": endpoint.host, "port": endpoint.port,
                "tls": endpoint.tls, "server_name": endpoint.server_name})
            F.need(checked == endpoint, "BODY_LOCATION_ORIGINAL_EGRESS")
            endpoint.validate()
        return self

    def reserved(self, ticket):
        self.validate(check_expiry=False)
        F.need(self._ticket is None and type(ticket) is int and self.budget.pending is not None
               and self.budget.pending[0] == ticket and self.budget.sequence == ticket,
               "BODY_LOCATION_ORIGINAL_TICKET")
        self._ticket = ticket
        self.pool.used["body_attempts"] += 1

    def settled(self, status):
        F.need(status in ("BODY_VALIDATED", "UNAVAILABLE_AT_SELECTED_SUPPLIER")
               and self._ticket is not None and not self._settled
               and self.budget.pending is None and self.structural.inflight == 0
               and self.structural.reserved_bytes == 0, "BODY_LOCATION_ATTEMPT_SETTLEMENT")
        self.validate()
        self._settled = True
        self.pool.used["body_successes" if status == "BODY_VALIDATED" else "settled_unavailable"] += 1

    def finish(self):
        if self._finished: return
        self._finished = True
        self._entry["state"] = "SPENT"
        self._entry["attempt"] = None
        if self.pool._entries.get(self.token) is self._entry:
            del self.pool._entries[self.token]


class _BodyPool:
    def __init__(self, client, envelope, limits):
        self.client, self.envelope = client, envelope
        self.grant, self.budget, self.channel, self.policy = (
            client.grant, client._budget, envelope.channel, envelope.policy)
        self.domain = _domain(client)
        self.namespace = P.body_namespace(self.domain)
        self.deadline = min(self.grant.deadline, envelope.deadline)
        self.limits, self._limits = deepcopy(limits), deepcopy(limits)
        self._domain = deepcopy(self.domain)
        self._deadline, self._grant_deadline = self.deadline, self.grant.deadline
        self._policy_state = deepcopy(self.policy.__dict__)
        self._budget_limits = deepcopy(self.budget.limits)
        self.used = {key: 0 for key in COUNTERS}
        self.closed, self._sequence, self._entries = False, 0, {}

    def check(self):
        """No client._active recursion; caller facade already owns that check."""
        c, e, ch = self.client, self.envelope, self.channel
        F.need(not self.closed and c._body_pool is c._origin_body_pool is self
               and c._query_envelope is c._origin_query_envelope is e
               and c.grant is self.grant and c._budget is self.budget and c._channel is ch
               and c._state == "OPEN" and not c._closed and c._busy
               and not _uncertain_channel(ch)
               and not getattr(c, "_cleanup_uncertain", False),
               "BODY_LOCATION_ORIGINAL_POOL_CLIENT")
        F.need(self.domain == self._domain == _domain(c)
               and self.namespace == P.body_namespace(self._domain)
               and ch.config["schema"] == "DMKN_V5_MAINTAINED_LOCATION_ROLES_V2"
               and ch.config["body_domain"] == self._domain and ch.config["role"] == "reader"
               and e.policy is self.policy and self.policy.__dict__ == self._policy_state,
               "BODY_LOCATION_DOMAIN_POLICY_CHANGED")
        F.need(self.limits == self._limits and self.budget.limits == self._budget_limits
               and self.grant.deadline == self.budget.deadline == ch.deadline == self._grant_deadline
               and self.deadline == self._deadline == min(self.grant.deadline, e.deadline),
               "BODY_LOCATION_ORIGINAL_ALLOWANCE")
        e.check(c); self.budget.active()

    def prune(self):
        # Expired ISSUED rows are inert tombstones, not usable endpoints. Keep
        # them until an explicit attempted consumption so the original body
        # reservation precedes its predial expiry refusal; cumulative issuance
        # bounds retained rows. Terminal/retired/fulfilled state drops them.
        for token, row in tuple(self._entries.items()):
            if row["state"] == "SPENT" or row["context"].invalidated():
                row["state"] = "SPENT"
                self._entries.pop(token, None)

    def invalidate_reader(self, reader):
        for token, row in tuple(self._entries.items()):
            if row["context"].reader is reader:
                row["state"] = "SPENT"
                self._entries.pop(token, None)

    def close(self):
        self.closed = True
        for row in self._entries.values(): row["state"] = "SPENT"
        self._entries.clear()

    def report(self):
        self.prune()
        return {"schema": "DMKN_V5_BODY_LOCATION_POOL_REPORT_V1",
            "status": "CLOSED" if self.closed else "RESERVED",
            "namespace": self.namespace, "limits": deepcopy(self.limits), "used": dict(self.used),
            "retained_capabilities": len(self._entries),
            "unexpired_issued_hints": sum(row["state"] == "ISSUED" and time.monotonic() < row["expires"]
                                          for row in self._entries.values()),
            "remaining_wall_ms": max(0, int((self.deadline-time.monotonic())*1000)),
            "body_success_scope": "TRANSPORT_BODY_VALIDATION_NOT_CUSTODY_OR_ADMISSION",
            "accounting": "PREPAID_LOCATION_NO_REFUNDS;BODY_GET_ORIGINAL_ACQUISITION_BUDGET",
            "dht_wire_bytes": None, "global_complete": False, "mathematical_acceptance": False}

    def _ticket(self):
        self._sequence += 1
        return self._sequence

    @staticmethod
    def _route_reply(reply, ticket):
        F.fields(reply, ("ticket", "route_key", "peers", "termination", "error", "census",
            "routing_peers_before", "routing_peers_after", "assurance", "global_complete",
            "mathematical_acceptance"))
        F.need(reply["ticket"] == ticket["ticket"] and reply["route_key"] == ticket["route_key"]
               and reply["assurance"] == P.ASSURANCE and reply["global_complete"] is False
               and reply["mathematical_acceptance"] is False, "BODY_LOCATION_ROUTE_BINDING")
        F.need(reply["termination"] in OR.TERMINATIONS, "BODY_LOCATION_ROUTE_TERMINATION")
        for error in (reply["error"], reply["census"].get("last_query_error")):
            F.need(error is None or type(error) is str and len(error) <= 500,
                   "BODY_LOCATION_ROUTE_ERROR_BOUND")
        census = reply["census"]
        F.fields(census, OR.CENSUS)
        # Same observed iterator-event census as observed_route. Reserved
        # event_cap counts adopted onProgress hooks, a different measure; no
        # unsupported census.events <= event_cap comparison is inferred.
        for name in OR.CENSUS[:-1]: F.uint(census[name], 0, 8192, "BODY_LOCATION_ROUTE_CENSUS")
        F.need(all(census[name] <= census["events"] for name in OR.CENSUS[1:-1])
               and census["add_provider_write"] == 0, "BODY_LOCATION_ROUTE_CENSUS_BINDING")
        for name in ("routing_peers_before", "routing_peers_after"):
            F.uint(reply[name], 0, 16384, "BODY_LOCATION_ROUTING_TABLE_BOUND")
        F.need(type(reply["peers"]) is list and len(reply["peers"]) <= ticket["peer_cap"],
               "BODY_LOCATION_ROUTE_PEER_CAP")
        peers = tuple(P.peer_id(value) for value in reply["peers"])
        F.need(len(set(peers)) == len(peers), "BODY_LOCATION_DUPLICATE_PEER")
        return peers

    async def locate(self, reader, demand, *, event_cap, peer_cap, descriptor_requests, max_age_ms=10000):
        self.check(); self.prune(); _quiescent(self.client)
        context = _Demand(self, reader, demand)
        F.need(not self.channel.lock.locked() and not self.channel.closed
               and not self.channel.channel_failed and self.envelope.started,
               "BODY_LOCATION_ORIGINAL_LIVE_CHILD")
        F.uint(event_cap, 1, self.channel.config["limits"]["query_events"], "BODY_LOCATION_EVENTS")
        F.uint(peer_cap, 1, self.channel.config["limits"]["provider_limit"], "BODY_LOCATION_PEERS")
        F.uint(descriptor_requests, 1, peer_cap, "BODY_LOCATION_DESCRIPTOR_COUNT")
        F.uint(max_age_ms, 1, 60000, "BODY_LOCATION_HINT_AGE")
        until = min(self.deadline, context.search.session.deadline, context.structural.deadline)
        _milliseconds(until)
        attempts = {"routes": 0, "descriptors": 0, "descriptor_unavailable": 0,
                    "route_termination": None, "route_census": None, "route_error": None}
        def result(status, capabilities=()):
            return {"status": status, "capabilities": list(capabilities),
                "route_key": context.route_key, "attempts": deepcopy(attempts),
                "global_complete": False, "mathematical_acceptance": False}
        u, l = self.used, self.limits
        if (u["route_operations_issued"] >= l["route_operations"]
            or u["routing_events_reserved"]+event_cap > l["routing_events"]
            or u["routing_peer_slots_reserved"]+peer_cap > l["routing_peer_slots"]
            or u["descriptor_requests_issued"]+descriptor_requests > l["descriptor_requests"]
            or u["capabilities_issued"] >= l["capabilities"]):
            return result("BODY_LOCATION_BUDGET_EXHAUSTED")
        u["route_operations_issued"] += 1
        u["routing_events_reserved"] += event_cap
        u["routing_peer_slots_reserved"] += peer_cap
        ticket = {"ticket": self._ticket(), "operation": "body-route",
            "route_key": context.route_key, "spec": P.body_route_spec(self.namespace, context.ref),
            "event_cap": event_cap, "peer_cap": peer_cap, "remaining_wall_ms": _milliseconds(until)}
        capabilities = []
        try:
            attempts["routes"] = 1
            reply = await self.channel.command("locate-body", ticket, until=until)
            context.check(); _milliseconds(until)
            F.need(not self.channel.closed and not self.channel.channel_failed,
                   "BODY_LOCATION_ROUTE_CHANNEL_FAILED")
            peers = self._route_reply(reply, ticket)
            attempts.update(route_termination=reply["termination"], route_census=reply["census"],
                            route_error=reply["error"])
            for peer in peers[:descriptor_requests]:
                if u["capabilities_issued"] >= l["capabilities"]: break
                context.check()
                expires = min(until, time.monotonic()+max_age_ms/1000)
                request = P.body_descriptor_request(self.namespace, context.ref, secrets.token_hex(32), 4096)
                F.need(len(F.compact(request)) <= 2048, "BODY_LOCATION_DESCRIPTOR_REQUEST_BYTES")
                u["descriptor_requests_issued"] += 1
                u["descriptor_reply_bytes_reserved"] += 4096
                attempts["descriptors"] += 1
                descriptor_ticket = {"ticket": self._ticket(), "operation": "body-descriptor",
                    "peer": peer, "request": request, "max_reply_bytes": 4096,
                    "remaining_wall_ms": _milliseconds(expires)}
                answer = await self.channel.command("descriptor-body", descriptor_ticket, until=expires)
                context.check(); _milliseconds(expires)
                F.need(not self.channel.closed and not self.channel.channel_failed,
                       "BODY_LOCATION_DESCRIPTOR_CHANNEL_FAILED")
                if answer.get("status") == "DESCRIPTOR_UNAVAILABLE":
                    F.fields(answer, ("status", "ticket", "peer", "reason", "mathematical_acceptance"))
                    F.need(answer["ticket"] == descriptor_ticket["ticket"] and answer["peer"] == peer
                           and answer["reason"] == "TCP_CONNECT_UNAVAILABLE"
                           and answer["mathematical_acceptance"] is False,
                           "BODY_LOCATION_DESCRIPTOR_UNAVAILABLE_BINDING")
                    attempts["descriptor_unavailable"] += 1
                    continue
                F.fields(answer, ("ticket", "authenticated_peer", "raw_base64", "request_body_bytes",
                    "reply_body_bytes", "framed_reply_bytes", "assurance", "mathematical_acceptance"))
                F.need(answer["ticket"] == descriptor_ticket["ticket"] and answer["authenticated_peer"] == peer
                       and answer["assurance"] == P.ASSURANCE and answer["mathematical_acceptance"] is False,
                       "BODY_LOCATION_DESCRIPTOR_CHANNEL_BINDING")
                F.need(type(answer["raw_base64"]) is str and len(answer["raw_base64"]) <= 4*((4096+2)//3),
                       "BODY_LOCATION_DESCRIPTOR_BASE64_BOUND")
                raw = base64.b64decode(answer["raw_base64"], validate=True)
                F.uint(answer["request_body_bytes"], 1, 2048)
                F.uint(answer["reply_body_bytes"], 1, 4096)
                F.uint(answer["framed_reply_bytes"], len(raw), 4100)
                F.need(len(raw) == answer["reply_body_bytes"], "BODY_LOCATION_DESCRIPTOR_LENGTH")
                u["descriptor_reply_bytes_observed"] += len(raw)
                endpoints = P.verify_body_descriptor(raw, request, peer, self.policy)
                F.need(len(endpoints) == 1, "BODY_LOCATION_ONE_DEMAND_ENDPOINT")
                context.check(); _milliseconds(expires)
                endpoint = endpoints[0]
                token = BodySupplier()
                u["capabilities_issued"] += 1
                supplier = F.digest("DMKN-V5-BODY-SUPPLIER-V1", {"peer": peer,
                    "route_key": context.route_key, "issuance": u["capabilities_issued"],
                    "endpoint": {"host": endpoint.host, "port": endpoint.port,
                        "tls": endpoint.tls, "server_name": endpoint.server_name}})
                self._entries[token] = {"context": context, "endpoint": endpoint, "expires": expires,
                    "peer": peer, "supplier": supplier, "state": "ISSUED", "attempt": None}
                capabilities.append(token)
            context.check()
            return result("BODY_CUSTODIANS_LOCATED" if capabilities else "NO_BODY_CUSTODIAN_WITHIN_ALLOWANCE",
                          capabilities)
        except BaseException:
            self.close()
            try: await self.channel.close()
            except BaseException as error:
                self.client._failures.append("body_location_cleanup:"+type(error).__name__)
                self.client._cleanup_uncertain = True
                self.client.workspace._poisoned = True
            raise

    def begin_attempt(self, reader, demand, capability):
        self.check(); _quiescent(self.client)
        F.need(type(capability) is BodySupplier and capability in self._entries,
               "BODY_LOCATION_UNKNOWN_CAPABILITY")
        row = self._entries[capability]
        F.need(row["state"] == "ISSUED" and row["attempt"] is None
               and row["context"].reader is reader
               and C.canonical(demand) == row["context"].demand_raw,
               "BODY_LOCATION_WRONG_OR_CONSUMED_CAPABILITY")
        row["context"].check()
        attempt = _BodyAttempt(self, capability, row)
        row["state"], row["attempt"] = "ATTEMPTING", attempt
        self.used["capabilities_consumed"] += 1
        return attempt


def reserve(client, limits):
    """Validate/prepay before first query; facade adopts the returned pool once."""
    from .located_queries import _LocatedEnvelope
    from .workspace_validated import CommonsClient
    F.need(type(client) is CommonsClient and client._busy
           and client._body_pool is client._origin_body_pool is None,
           "BODY_LOCATION_FRESH_CLIENT_POOL")
    F.fields(limits, ("schema", *LIMITS))
    F.need(limits["schema"] == SCHEMA, "BODY_LOCATION_ALLOWANCE_SCHEMA")
    for name, bounds in LIMITS.items(): F.uint(limits[name], *bounds, "BODY_LOCATION_LIMIT:"+name)
    F.need(limits["capabilities"] <= limits["descriptor_requests"], "BODY_LOCATION_CAPABILITY_ALLOWANCE")
    e = client._query_envelope
    F.need(type(e) is _LocatedEnvelope and client._origin_query_envelope is e
           and e.client is client and e.state == "RESERVED" and not e.generations
           and e.current is None and not e.started, "BODY_LOCATION_PREQUERY_RESERVATION")
    e.check(client)
    ch, b = e.channel, client._budget
    F.need(type(ch) is ServiceLocationProcess and ch.config["role"] == "reader"
           and ch.config["schema"] == "DMKN_V5_MAINTAINED_LOCATION_ROLES_V2"
           and ch.config["body_domain"] == _domain(client)
           and ch.process is None and ch._start_task is ch._spawn_task is ch._close_task is None
           and ch.sequence == ch.sent == ch.received == ch.read_frames == 0
           and ch.stderr_task is None and not ch.stderr and not ch.lock.locked()
           and not ch.closed and not ch.channel_failed, "BODY_LOCATION_PRISTINE_V2_READER")
    F.need(type(b) is AcquisitionBudget and b is e.budget
           and b.sequence == 0 and b.pending is None, "BODY_LOCATION_PREACQUISITION_RESERVATION")
    commands = (e.limits["location"]["route_operations"]+e.limits["location"]["descriptor_requests"]
                +limits["route_operations"]+limits["descriptor_requests"]+2)
    F.need(commands <= min(ch.config["limits"]["commands"], 60), "BODY_LOCATION_COMBINED_COMMAND_CAP")
    pool = _BodyPool(client, e, limits)
    _milliseconds(pool.deadline)
    b.charge_external("body-location", limits["route_operations"]+limits["descriptor_requests"],
                      4096*limits["descriptor_requests"])
    return pool

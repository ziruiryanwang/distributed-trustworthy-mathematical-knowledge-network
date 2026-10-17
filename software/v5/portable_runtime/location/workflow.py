"""Single-owner locate -> search envelope, with no budget renewal by referrals.

Pure source boundary. A future adopted location transport must enforce ticket
caps and supply authenticated channel IDs. DHT events are NOT wire bytes.
Search reply capacity is prepaid once at construction; only one SearchSession
can be issued. The caller remains responsible for hard process containment.
"""
from copy import deepcopy
import secrets
import time

from discovery import formal_features as F
from discovery.search_session import LIMITS as SEARCH_LIMITS, SearchSession
from transport.clients import SearchClient
from . import protocol as P

LIMITS = {"wall_ms": (1, 3600000), "route_operations": (1, 32),
          "routing_events": (1, 4096), "routing_peer_slots": (1, 256),
          "descriptor_requests": (1, 64), "contacts": (1, 64),
          "reply_bytes": (2048, 1024**3)}


class _LocatedSearchClient(SearchClient):
    """Recheck owner egress and local hint lifetime before every HTTP dial."""
    def __init__(self, session, endpoints, policy, expiries, clock):
        super().__init__(session, endpoints)
        self._policy, self._expiries, self._clock = policy, dict(expiries), clock
        self._adopted_endpoints = dict(endpoints)

    async def _send(self, provider, ticket, route):
        try:
            F.need(provider in self._expiries and self._clock() < self._expiries[provider],
                   "LOCATION_CONTACT_EXPIRED")
            endpoint = self.endpoints[provider]
            F.need(endpoint == self._adopted_endpoints[provider], "LOCATION_CONTACT_BINDING_CHANGED")
            checked = self._policy.endpoint({"host": endpoint.host, "port": endpoint.port,
                "tls": endpoint.tls, "server_name": endpoint.server_name})
            F.need(endpoint == checked, "LOCATION_CONTACT_POLICY_CHANGED")
        except BaseException:
            # The public method has already reserved its request. Refusal cannot
            # turn that attempt into a new allowance or leave a pending ticket.
            self.session.abandon(ticket["ticket"])
            raise
        return await super()._send(provider, ticket, route)


class WorkflowBudget:
    def __init__(self, namespace, features, limits, search_limits, policy, *, clock=None):
        F.fields(limits, LIMITS)
        for key, bounds in LIMITS.items():
            F.uint(limits[key], *bounds, "LOCATION_LIMIT:" + key)
        F.fields(search_limits, SEARCH_LIMITS)
        for key, bounds in SEARCH_LIMITS.items():
            F.uint(search_limits[key], *bounds, "LOCATION_SEARCH_LIMIT:" + key)
        F.need(type(policy) is P.OwnerEgressPolicy, "LOCATION_OWNER_POLICY_REQUIRED")
        F.need(search_limits["bytes"] + 1024 <= limits["reply_bytes"]
               and search_limits["wall_ms"] <= limits["wall_ms"]
               and search_limits["providers"] <= limits["contacts"], "LOCATION_SEARCH_PREALLOCATION")
        self._namespace, self._features = F.hexid(namespace), tuple(F.validate_features(features, 8))
        self._limits, self._search_limits = deepcopy(limits), deepcopy(search_limits)
        self._policy, self._clock = policy, clock or time.monotonic
        self._deadline = self._clock() + limits["wall_ms"] / 1000
        self._state, self._sequence, self._pending = "LOCATING", 0, None
        self._used = dict(route_operations=0, routing_events=0, routing_peer_slots=0,
                          descriptor_requests=0, descriptor_reply_bytes=0, descriptor_request_bytes=0)
        self._located, self._routes, self._contacts, self._expiries = set(), {}, {}, {}
        self._search_client = None

    def _live(self, phase="LOCATING"):
        if self._clock() >= self._deadline:
            self._state = "DEADLINE_EXHAUSTED"
        F.need(self._state == phase, "LOCATION_PHASE:" + self._state)

    def _issue(self, ticket):
        self._sequence += 1
        self._pending = {"ticket": self._sequence, **deepcopy(ticket)}
        return deepcopy(self._pending)

    def _take(self, ticket_id, operation):
        F.uint(ticket_id, 1, self._sequence, "LOCATION_TICKET")
        F.need(self._pending is not None and self._pending["ticket"] == ticket_id
               and self._pending["operation"] == operation, "LOCATION_PRIVATE_TICKET")
        ticket, self._pending = self._pending, None
        return ticket

    def begin_route(self, features, stripe=0, *, event_cap, peer_cap):
        self._live()
        F.need(self._pending is None, "LOCATION_INFLIGHT")
        chosen = F.validate_features(features, 8)
        F.need(set(chosen) <= set(self._features), "LOCATION_ROUTE_NOT_QUERY_SUBSET")
        F.uint(event_cap, 1, self._limits["routing_events"], "LOCATION_ROUTE_EVENTS")
        F.uint(peer_cap, 1, self._limits["routing_peer_slots"], "LOCATION_ROUTE_PEERS")
        F.need(self._used["route_operations"] < self._limits["route_operations"]
               and self._used["routing_events"] + event_cap <= self._limits["routing_events"]
               and self._used["routing_peer_slots"] + peer_cap <= self._limits["routing_peer_slots"],
               "LOCATION_ROUTE_BUDGET")
        spec = P.route_spec(self._namespace, chosen, stripe)
        key = P.route_key(self._namespace, chosen, stripe)
        # Full local allowances charge at issuance; transport failures or low
        # remote work claims cannot refund events/peer slots.
        self._used["route_operations"] += 1
        self._used["routing_events"] += event_cap
        self._used["routing_peer_slots"] += peer_cap
        return self._issue({"operation": "route", "route_key": key, "spec": spec,
            "event_cap": event_cap, "peer_cap": peer_cap,
            "remaining_wall_ms": max(0, int((self._deadline-self._clock())*1000))})

    def accept_route(self, ticket_id, peers):
        ticket = self._take(ticket_id, "route")
        self._live()
        F.need(type(peers) is list and len(peers) <= ticket["peer_cap"], "LOCATION_PEER_COUNT")
        selected = tuple(P.peer_id(value) for value in peers)
        F.need(len(set(selected)) == len(selected), "LOCATION_DUPLICATE_PEER")
        self._live()
        key = ticket["route_key"]
        self._routes[key] = deepcopy(ticket["spec"])
        self._located.update((peer, key) for peer in selected)
        return {"route_key": key, "peers": list(selected), "assurance": P.ASSURANCE,
                "global_complete": False, "mathematical_acceptance": False}

    def abandon_route(self, ticket_id):
        self._take(ticket_id, "route")
        return {"status": "ABANDONED_FULL_ROUTE_ALLOWANCE_CHARGED"}

    def begin_descriptor(self, peer, route_key, *, max_bytes=4096, max_age_ms=10000):
        self._live()
        F.need(self._pending is None, "LOCATION_INFLIGHT")
        peer, key = P.peer_id(peer), F.hexid(route_key)
        F.need((peer, key) in self._located, "LOCATION_PEER_NOT_LOCATED_FOR_KEY")
        F.uint(max_bytes, 1024, P.MAX_DESCRIPTOR, "LOCATION_DESCRIPTOR_BYTES")
        F.uint(max_age_ms, 1, 60000, "LOCATION_DESCRIPTOR_AGE")
        F.need(self._used["descriptor_requests"] < self._limits["descriptor_requests"]
               and self._search_limits["bytes"] + self._used["descriptor_reply_bytes"] + max_bytes
               <= self._limits["reply_bytes"], "LOCATION_DESCRIPTOR_BUDGET")
        spec = self._routes[key]
        request = P.descriptor_request(self._namespace, spec["predicate"]["all"],
            spec["stripe"], secrets.token_hex(32), max_bytes)
        request_bytes = len(F.compact(request))
        F.need(request_bytes <= 2048, "LOCATION_REQUEST_BYTES")
        self._used["descriptor_requests"] += 1
        self._used["descriptor_request_bytes"] += request_bytes
        until = min(self._deadline, self._clock()+max_age_ms/1000)
        return self._issue({"operation": "descriptor", "peer": peer, "request": request,
            "max_reply_bytes": max_bytes, "until": until,
            "remaining_wall_ms": max(0, int((until-self._clock())*1000))})

    def accept_descriptor(self, ticket_id, raw, authenticated_peer):
        F.need(type(raw) is bytes, "LOCATION_RAW_BYTES_REQUIRED")
        ticket = self._take(ticket_id, "descriptor")
        self._used["descriptor_reply_bytes"] += len(raw)
        if len(raw) > ticket["max_reply_bytes"]:
            self._state = "TRANSPORT_BYTE_VIOLATION"
            raise ValueError("LOCATION_TRANSPORT_BYTE_VIOLATION")
        self._live()
        F.need(self._clock() < ticket["until"], "LOCATION_DESCRIPTOR_EXPIRED")
        F.need(authenticated_peer == ticket["peer"], "LOCATION_WRONG_AUTHENTICATED_PEER")
        endpoints = P.verify_descriptor(raw, ticket["request"], authenticated_peer, self._policy)
        prepared = {}
        for endpoint in endpoints:
            spec = {"host": endpoint.host, "port": endpoint.port,
                    "tls": endpoint.tls, "server_name": endpoint.server_name}
            name = F.digest("DMKN-V5-LOCATED-ENDPOINT-V1", spec)
            # Revalidate at adoption; no peer gets to supply CA/path options.
            prepared[name] = self._policy.endpoint(spec)
        F.need(len(set(self._contacts) | set(prepared)) <= self._limits["contacts"], "LOCATION_CONTACT_CAP")
        self._live()
        F.need(self._clock() < ticket["until"], "LOCATION_DESCRIPTOR_EXPIRED")
        self._contacts.update(prepared)
        self._expiries.update({name: ticket["until"] for name in prepared})
        return {"status": "ADOPTED_ADVISORY_CONTACTS", "contacts": sorted(prepared),
                "assurance": P.ASSURANCE, "global_complete": False, "mathematical_acceptance": False}

    def abandon_descriptor(self, ticket_id):
        ticket = self._take(ticket_id, "descriptor")
        self._used["descriptor_reply_bytes"] += ticket["max_reply_bytes"]
        return {"status": "ABANDONED_FULL_DESCRIPTOR_BYTES_CHARGED"}

    def begin_search(self):
        self._live()
        F.need(self._pending is None and self._contacts, "LOCATION_READY_CONTACTS_REQUIRED")
        limits = deepcopy(self._search_limits)
        remaining = int((self._deadline-self._clock()) * 1000)
        F.need(remaining >= 1, "LOCATION_SEARCH_TIME_EXHAUSTED")
        limits["wall_ms"] = min(limits["wall_ms"], remaining)
        # Construct once; no fresh search budget on failed providers/referrals.
        session = SearchSession(self._namespace, list(self._features), limits, clock=self._clock)
        session.deadline = min(session.deadline, self._deadline)
        endpoints = {}
        for name, endpoint in self._contacts.items():
            if self._clock() >= self._expiries[name]:
                continue
            endpoints[name] = self._policy.endpoint({"host": endpoint.host, "port": endpoint.port,
                "tls": endpoint.tls, "server_name": endpoint.server_name})
        F.need(endpoints, "LOCATION_NO_UNEXPIRED_CONTACTS")
        self._search_client = _LocatedSearchClient(session, endpoints, self._policy, self._expiries, self._clock)
        self._state = "SEARCH"
        return self._search_client

    def report(self):
        if self._clock() >= self._deadline and self._state in ("LOCATING", "SEARCH"):
            self._state = "DEADLINE_EXHAUSTED"
        reserved = (self._pending["max_reply_bytes"]
                    if self._pending is not None and self._pending["operation"] == "descriptor" else 0)
        return {"status": self._state, "used": deepcopy(self._used),
            "search_reply_allocation": self._search_limits["bytes"],
            "pending_descriptor_reply_reservation": reserved,
            "committed_reply_capacity": self._used["descriptor_reply_bytes"] + reserved + self._search_limits["bytes"],
            "reply_capacity_limit": self._limits["reply_bytes"],
            "pending_requests": int(self._pending is not None), "located_peer_route_pairs": len(self._located),
            "contacts": len(self._contacts), "search_issued": self._search_client is not None,
            "remaining_wall_ms": max(0, int((self._deadline-self._clock()) * 1000)),
            "search": None if self._search_client is None else self._search_client.report(),
            "dht_wire_bytes": None, "dht_byte_assurance": "NOT_MEASURED_OR_BOUNDED_BY_QUERY_EVENTS",
            "global_complete": False, "mathematical_acceptance": False}

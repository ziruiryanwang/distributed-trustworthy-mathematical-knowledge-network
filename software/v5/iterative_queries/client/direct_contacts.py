"""One owner-configured search on an existing finite validated client.

Direct contacts replace location, not authentication or mathematical admission.
The guarded search client is reused without fabricating a location handoff.
All remote data remain untrusted; the original client owns actual verification.
"""
from copy import deepcopy
from pathlib import Path
import time

from discovery import formal_features as F
from discovery.search_session import SearchSession
from evidence_network.transport import EvidenceAcquisition
from location.protocol import OwnerEgressPolicy
from location.workflow import _LocatedSearchClient
from modules import codec as C
from transport.located_receipts import _ExpiringContact
from .workspace_atomic import _action
from .workspace_validated import CommonsClient


class _Binding:
    """Keep direct custody tied to the original query, not a replaceable search."""
    def __init__(self, client, search, policy):
        self.client, self.search, self.policy = client, search, policy
        self.grant, self.budget = client.grant, client._budget
        self.deadline = self.grant.deadline
        self.session, self.clock = search.session, search.session.clock
        self.query = self.session._query
        self.search_deadline, self.limits = self.session.deadline, deepcopy(self.session.limits)
        self.endpoints, self.expiries = dict(search.endpoints), dict(search._expiries)
        self.policy_state = policy._mode, policy._ports, policy._tests, deepcopy(policy._config)
        self.acquisition = None

    def check(self):
        c, s, p = self.client, self.search, self.policy
        F.need(c.grant is self.grant and c._budget is self.budget
               and self.grant.deadline == self.budget.deadline == self.deadline
               and c._search is s and c._handoff is None and c._channel is None,
               "DIRECT_ORIGINAL_OPERATION")
        F.need(s.session is self.session and self.session.clock is self.clock
               and s._clock is self.clock and self.session._query == self.query
               and self.session.deadline == self.search_deadline
               and self.session.limits == self.limits, "DIRECT_ORIGINAL_SEARCH")
        F.need(s.endpoints == s._adopted_endpoints == self.endpoints
               and s._expiries == self.expiries and s._policy is p
               and (p._mode, p._ports, p._tests, p._config) == self.policy_state,
               "DIRECT_ORIGINAL_CONTACTS")
        if self.acquisition is not None:
            a = self.acquisition
            F.need(c._acquisition is a and a._search is s and a._handoff is None
                   and a.budget is self.budget and not a.closed, "DIRECT_ORIGINAL_ACQUISITION")
        self.budget.active()


class _Contact(_ExpiringContact):
    def __init__(self, endpoint, expires, policy, budget, binding):
        super().__init__(endpoint, expires, policy, budget)
        self._binding = binding

    def validate(self):
        self._binding.check()
        return super().validate()


@_action
def bind(client, contacts, specs, policy, search_limits, *, contact_lifetime_ms=60000):
    """Configure once, without I/O; use normal search/resolve/acquire afterwards.

    ``contacts`` maps local labels to exact OwnerEgressPolicy endpoint records.
    Labels, endpoints, query and limits are trusted owner choices, not referrals.
    This uses the same one-query slot as find(), and cannot replenish a grant.
    """
    F.need(type(client) is CommonsClient, "DIRECT_EXACT_VALIDATED_CLIENT")
    F.need(not client._query_used and client._channel is None
           and client._handoff is None and client._search is None
           and client._acquisition is None, "DIRECT_ONE_FRESH_QUERY")
    F.need(type(policy) is OwnerEgressPolicy, "DIRECT_OWNER_POLICY")
    F.need(type(contacts) is dict and 1 <= len(contacts) <= 64, "DIRECT_CONTACT_COUNT")
    F.uint(contact_lifetime_ms, 1, 3600000, "DIRECT_CONTACT_LIFETIME")
    endpoints = {}
    for label, value in contacts.items():
        F.need(type(label) is str and 1 <= len(label.encode("utf-8")) <= 128
               and all(ord(char) >= 32 for char in label), "DIRECT_CONTACT_LABEL")
        endpoints[label] = policy.endpoint(value)
    F.need(len(set(endpoints.values())) == len(endpoints), "DIRECT_DUPLICATE_ENDPOINT")
    features = client.workspace.adapter.compile_query(specs)
    session = SearchSession(client.workspace.adapter.namespace, features, search_limits)
    F.need(len(endpoints) <= session.limits["providers"], "DIRECT_PROVIDER_SUBALLOCATION")
    session.deadline = min(session.deadline, client.grant.deadline)
    session._live()

    # The launcher/actual issuers selected this helper before the operation.
    # Hashing arbitrary local code here must not turn it into an adopted source.
    path = Path(__file__).resolve()
    pins = [owner._pins[path] for owner in (client.receipt, client.aggregate, client.delta)
            if owner is not None and path in owner._pins]
    F.need(bool(pins) and all(pin == pins[0] for pin in pins), "DIRECT_REQUIRED_SOURCE_PIN")
    client._required_origins[__name__] = path
    client._source_pins[path] = deepcopy(pins[0])
    client._active()
    client._charge(C.canonical(specs))

    # Charge the whole prospective search suballocation, before any dial. No
    # refund is issued for a short search. Acquisition uses this same ledger.
    client._budget.charge_external("direct-contact-search", session.limits["requests"],
                                   session.limits["bytes"])
    client._query_used = True
    expires = min(client.grant.deadline, time.monotonic()+contact_lifetime_ms/1000)
    search = _LocatedSearchClient(session, endpoints, policy,
                                  {label: expires for label in endpoints}, session.clock)
    client._search = search
    binding = _Binding(client, search, policy)
    custody = {label: _Contact(endpoint, expires, policy, client._budget, binding)
               for label, endpoint in endpoints.items()}
    acquisition = EvidenceAcquisition(client.workspace.adapter, custody,
        client.workspace.config["wire_profile"], client._budget,
        client.workspace.modules, client.workspace.packets, verifier=None)
    # Candidate membership must still come from this exact session. No opaque
    # location handoff is invented, and no index hit is mathematical authority.
    acquisition._search = search
    client._acquisition = binding.acquisition = acquisition
    binding.check()
    return {"status": "QUERY_CONTACTS_READY", "contact_origin": "OWNER_CONFIGURED_CONTACTS",
            "contacts": sorted(endpoints), "global_complete": False,
            "mathematical_acceptance": False, "location_performed": False,
            "search_prepaid": {"requests": session.limits["requests"],
                               "reply_bytes": session.limits["bytes"]}}


# Optional query generations are selected before any acquisition. The legacy
# bind() above is intentionally unchanged and still consumes its one-shot slot.
from hashlib import sha256
from discovery.search_session import LIMITS as _SEARCH_LIMITS

_ADDITIVE = ("providers", "snapshots", "requests", "pages", "examined", "candidates", "bytes")
_ENVELOPE_KEYS = (*_SEARCH_LIMITS, "generations")


def _policy_state(policy):
    return policy._mode, policy._ports, policy._tests, deepcopy(policy._config)


def _compact_generation(search, acquisition):
    """Fixed-width scalar accounting, never retain coverage/records/offer lists."""
    s = search.session
    return {
        "search": {**{key: s.used[key] for key in
                      ("requests", "request_bytes", "pages", "examined", "candidates", "bytes")},
                   "provider_slots_used": len(s.providers),
                   "snapshot_attempt_slots": s.snapshot_slots,
                   "pending_requests": len(s.pending),
                   "reserved": dict(s.reserved), "status": s.state},
        "search_http": dict(search.http),
        "acquisition_http": dict(acquisition.http),
        "structural_http": acquisition.structural.report(),
    }


class _QueryEnvelope:
    """One owner-selected, nonrenewable pool; only this client may advance it."""
    def __init__(self, client, limits, policy):
        F.fields(limits, _ENVELOPE_KEYS)
        for key, bounds in _SEARCH_LIMITS.items():
            F.uint(limits[key], *bounds, "QUERY_ENVELOPE_LIMIT:"+key)
        F.uint(limits["generations"], 1, 8, "QUERY_ENVELOPE_GENERATIONS")
        F.need(type(policy) is OwnerEgressPolicy, "QUERY_ENVELOPE_OWNER_POLICY")
        self.client, self.grant, self.budget = client, client.grant, client._budget
        self.namespace = client.workspace.adapter.namespace
        self.policy, self.policy_state = policy, _policy_state(policy)
        self.limits = deepcopy(limits)
        self._limits = deepcopy(limits)
        self.deadline = min(self.grant.deadline, time.monotonic()+limits["wall_ms"]/1000)
        self._deadline = self.deadline
        self._grant_deadline = self.grant.deadline
        self._budget_limits = deepcopy(self.budget.limits)
        self.allocated = {key: 0 for key in _ADDITIVE}
        self.generations, self.current = [], None
        self.state = "RESERVED"

    def check(self, client):
        F.need(client is self.client and client.grant is self.grant
               and client._budget is self.budget
               and self.grant.deadline == self.budget.deadline == self._grant_deadline
               and self.budget.limits == self._budget_limits
               and client.workspace.adapter.namespace == self.namespace,
               "QUERY_ENVELOPE_ORIGINAL_LIFETIME")
        F.need(self.limits == self._limits and self.deadline == self._deadline
               and _policy_state(self.policy) == self.policy_state
               and client._query_used and client._channel is None and client._handoff is None,
               "QUERY_ENVELOPE_FIXED_POLICY")
        F.need(self.state in ("RESERVED", "ACTIVE"), "QUERY_ENVELOPE_TERMINAL")
        if self.current is None:
            F.need(client._search is None and client._acquisition is None,
                   "QUERY_ENVELOPE_EMPTY_BINDING")
        else:
            row, search, acquisition, binding = self.current
            F.need(client._search is search and client._acquisition is acquisition
                   and row is self.generations[-1] and row["status"] == "ACTIVE"
                   and not acquisition.closed, "QUERY_ENVELOPE_CURRENT_BINDING")
            binding.check()

    def validate_next(self, limits):
        F.need(time.monotonic() < self.deadline, "QUERY_ENVELOPE_DEADLINE")
        F.fields(limits, _SEARCH_LIMITS)
        for key, bounds in _SEARCH_LIMITS.items():
            F.uint(limits[key], *bounds, "QUERY_GENERATION_LIMIT:"+key)
        F.need(len(self.generations) < self.limits["generations"],
               "QUERY_ENVELOPE_GENERATION_LIMIT")
        F.need(limits["wall_ms"] <= self.limits["wall_ms"]
               and limits["inflight"] <= self.limits["inflight"],
               "QUERY_ENVELOPE_NONADDITIVE_LIMIT")
        for key in _ADDITIVE:
            F.need(self.allocated[key]+limits[key] <= self.limits[key],
                   "QUERY_ENVELOPE_EXHAUSTED:"+key)
        F.need(self.budget.pending is None, "QUERY_GENERATION_ACQUISITION_PENDING")
        if self.current is not None:
            unused, search, acquisition, unused_binding = self.current
            F.need(not search.session.pending and not any(search.session.reserved.values())
                   and acquisition.structural.inflight == 0
                   and acquisition.structural.reserved_bytes == 0,
                   "QUERY_GENERATION_PENDING")

    def allocate(self, limits, features):
        row = {"generation": len(self.generations)+1, "status": "ALLOCATED",
               "query_sha256": sha256(C.canonical(
                   {"namespace": self.namespace, "features": features})).hexdigest(),
               "allocation": {key: limits[key] for key in _ADDITIVE},
               "outcome": None}
        for key in _ADDITIVE: self.allocated[key] += limits[key]
        self.generations.append(row)
        return row

    def retire_current(self):
        if self.current is None: return
        row, search, acquisition, unused_binding = self.current
        # Terminal state first: retained SearchClient references cannot dial if
        # structural retirement subsequently fails. The action then fail-stops.
        search.session.state = "RETIRED"
        row["outcome"] = _compact_generation(search, acquisition)
        acquisition.retire_generation()
        row["status"] = "RETIRED"
        self.client._candidates.clear()
        self.client._staged.clear()
        self.client._search = self.client._acquisition = None
        self.current = None

    def terminal(self, status):
        # Closing an already failed client is cleanup, not a successful outcome.
        if self.state == "FAILED" and status == "CLOSED": return
        self.state = status
        if self.generations and self.generations[-1]["status"] == "ALLOCATED":
            self.generations[-1]["status"] = status
        if self.client._search is not None:
            self.client._search.session.state = "CLIENT_"+status
        if self.current is not None:
            row, search, acquisition, unused_binding = self.current
            search.session.state = "CLIENT_"+status
            row["status"] = status
            row["outcome"] = _compact_generation(search, acquisition)

    def report(self):
        rows = deepcopy(self.generations)
        if self.current is not None:
            row, search, acquisition, unused_binding = self.current
            rows[row["generation"]-1]["outcome"] = _compact_generation(search, acquisition)
        return {"schema": "DMKN_DIRECT_QUERY_ENVELOPE_V1", "status": self.state,
                "namespace": self.namespace, "limits": deepcopy(self.limits),
                "allocated": dict(self.allocated), "generations": rows,
                "remaining_wall_ms": max(0, int((self.deadline-time.monotonic())*1000)),
                "accounting": "SEARCH_PREPAID_ONCE;GENERATION_ALLOCATIONS_NOT_REFUNDED;"
                              "ACQUISITION_CHARGES_REMAIN_IN_ORIGINAL_BUDGET",
                "global_complete": False, "mathematical_acceptance": False}


@_action
def reserve_queries(client, envelope, policy):
    """Reserve one finite adaptive direct-search pool before any acquisition.

    envelope has SearchSession limit fields plus generations (1..8). Additive
    fields are totals across generations; wall_ms fixes one absolute deadline.
    No search is dispatched and no existing grant or issuer is extended.
    """
    F.need(type(client) is CommonsClient, "DIRECT_EXACT_VALIDATED_CLIENT")
    F.need(client._query_envelope is None and not client._query_used
           and client._channel is None and client._handoff is None
           and client._search is None and client._acquisition is None,
           "QUERY_ENVELOPE_FRESH_OPERATION")
    selected = _QueryEnvelope(client, envelope, policy)
    path = Path(__file__).resolve()
    pins = [owner._pins[path] for owner in (client.receipt, client.aggregate, client.delta)
            if owner is not None and path in owner._pins]
    F.need(bool(pins) and all(pin == pins[0] for pin in pins), "DIRECT_REQUIRED_SOURCE_PIN")
    client._required_origins[__name__] = path
    client._source_pins[path] = deepcopy(pins[0])
    client._active()
    client._charge(C.canonical(envelope))
    # Existing preallocation guard (including sequence==0) remains authoritative.
    client._budget.charge_external("direct-query-envelope", envelope["requests"], envelope["bytes"])
    client._query_used = True
    client._query_envelope = client._origin_query_envelope = selected
    selected.check(client)
    return {"status": "QUERY_ENVELOPE_RESERVED", "generations": envelope["generations"],
            "search_prepaid": {"requests": envelope["requests"], "reply_bytes": envelope["bytes"]},
            "global_complete": False, "mathematical_acceptance": False}


@_action
def next_query(client, contacts, specs, search_limits, *, contact_lifetime_ms=60000):
    """Retire the prior direct query and bind a different owner-chosen query.

    Acquire needed mathematics before rotation. Old candidates, staging handles,
    search and semantic-reader objects do not survive as active capabilities.
    Original warrants, custody, owners and import context remain unchanged.
    """
    F.need(type(client) is CommonsClient and type(client._query_envelope) is _QueryEnvelope,
           "QUERY_ENVELOPE_REQUIRED")
    selected = client._query_envelope
    selected.check(client); selected.validate_next(search_limits)
    F.need(type(contacts) is dict and 1 <= len(contacts) <= 64, "DIRECT_CONTACT_COUNT")
    F.uint(contact_lifetime_ms, 1, 3600000, "DIRECT_CONTACT_LIFETIME")
    endpoints = {}
    for label, value in contacts.items():
        F.need(type(label) is str and 1 <= len(label.encode("utf-8")) <= 128
               and all(ord(char) >= 32 for char in label), "DIRECT_CONTACT_LABEL")
        endpoints[label] = selected.policy.endpoint(value)
    F.need(len(set(endpoints.values())) == len(endpoints), "DIRECT_DUPLICATE_ENDPOINT")
    F.need(len(endpoints) <= search_limits["providers"], "DIRECT_PROVIDER_SUBALLOCATION")
    client._charge(C.canonical(specs))
    features = client.workspace.adapter.compile_query(specs)
    # Failed construction/retirement consumes this complete reservation too.
    row = selected.allocate(search_limits, features)
    selected.retire_current()
    session = SearchSession(selected.namespace, features, search_limits)
    session.deadline = min(session.deadline, selected.deadline, client.grant.deadline)
    session._live()
    expires = min(selected.deadline, client.grant.deadline,
                  time.monotonic()+contact_lifetime_ms/1000)
    search = _LocatedSearchClient(session, endpoints, selected.policy,
                                  {label: expires for label in endpoints}, session.clock)
    client._search = search
    binding = _Binding(client, search, selected.policy)
    custody = {label: _Contact(endpoint, expires, selected.policy, client._budget, binding)
               for label, endpoint in endpoints.items()}
    acquisition = EvidenceAcquisition(client.workspace.adapter, custody,
        client.workspace.config["wire_profile"], client._budget,
        client.workspace.modules, client.workspace.packets, verifier=None)
    acquisition._search = search
    client._acquisition = binding.acquisition = acquisition
    selected.current = row, search, acquisition, binding
    selected.state = row["status"] = "ACTIVE"
    binding.check()
    return {"status": "QUERY_CONTACTS_READY", "generation": row["generation"],
            "contact_origin": "OWNER_CONFIGURED_CONTACTS", "contacts": sorted(endpoints),
            "global_complete": False, "mathematical_acceptance": False,
            "location_performed": False, "allocation": dict(row["allocation"]),
            "search_prepaid": "ORIGINAL_QUERY_ENVELOPE_NO_SECOND_CHARGE"}


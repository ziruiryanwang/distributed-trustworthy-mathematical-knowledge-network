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

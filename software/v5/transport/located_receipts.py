"""Owner-only composition of adopted location, candidate search and admission.

No planner, provider crawl, new proof relation or remote configuration. Caller
selects the query, route/page and candidate. Existing used implementations stay
unchanged. Root must supply one outer Job and the original absolute deadline.
"""
from copy import deepcopy
import time

from discovery import formal_features as F
from discovery.module_export_adapter import ModuleExportAdapter
from custody.module_store import ModuleStore
from custody.receipt_store import ReceiptStore, profile_id
from location import protocol as P
from location.controller_services import ServiceLocationProcess, ServiceLocatedWorkflow
from .receipt_client import AcquisitionBudget, ReceiptAcquisition, DeadlineReceiptVerifier, deadline_checked


class _ExpiringContact:
    """Endpoint-compatible owner guard; remote bytes cannot construct it.

    Both frozen HTTP implementations call endpoint.validate() immediately before
    dialing, after their caller has reserved the attempt. Thus expiry/policy
    refusals stay charged. The accepted descriptor is advisory, not authority.
    """
    def __init__(self, endpoint, expires, policy, budget):
        self._endpoint, self._expires, self._policy, self._budget = endpoint, expires, policy, budget

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
        self._budget.active()
        F.need(time.monotonic() < self._expires, "LOCATED_CUSTODY_CONTACT_EXPIRED")
        expected = self._policy.endpoint({"host": self.host, "port": self.port,
            "tls": self.tls, "server_name": self.server_name})
        F.need(expected == self._endpoint, "LOCATED_CUSTODY_EGRESS_BINDING")
        self._endpoint.validate(); return self


class LocatedReceiptWorkflow:
    """One fresh private reader, one search session, one acquisition ledger.

    Setup is owner-controlled. The channel and optional adopted verifier MUST
    already bind the identical original deadline; this constructor creates no
    new operation deadline. No I/O/child start occurs until start(). Caller owns
    durable store lifetimes. close() owns child teardown and handle revocation.
    """
    def __init__(self, *, deadline, channel, adapter, features, policy, location_limits,
                 search_limits, acquisition_limits, wire_profile, module_custody,
                 receipt_custody, verifier=None):
        self.deadline = deadline_checked(deadline)
        F.need(type(channel) is ServiceLocationProcess and channel.deadline == self.deadline
               and channel.config["role"] == "reader" and channel.process is None
               and channel._start_task is None and not channel.closed, "LOCATED_RECEIPT_FRESH_READER")
        F.need(type(adapter) is ModuleExportAdapter and type(policy) is P.OwnerEgressPolicy,
               "LOCATED_RECEIPT_OWNER_ADAPTER_POLICY")
        F.need(channel.config["namespace"] == adapter.namespace and channel.config["egress"] == policy._config,
               "LOCATED_RECEIPT_READER_NAMESPACE_POLICY")
        wire_id = profile_id(wire_profile)
        F.need(type(module_custody) is ModuleStore and type(receipt_custody) is ReceiptStore
               and adapter.foundation == module_custody.foundation == wire_profile["foundation"]
               and adapter.policy == module_custody.policy == wire_profile["policy"]
               and receipt_custody.profile_id == wire_id, "LOCATED_RECEIPT_INITIAL_NAMESPACE_PROFILE")
        if verifier is not None:
            F.need(type(verifier) is DeadlineReceiptVerifier and verifier.outer_deadline == self.deadline
                   and verifier.wire_profile_id == wire_id,
                   "LOCATED_RECEIPT_ORIGINAL_VERIFIER_DEADLINE")
        self.channel, self.adapter, self.policy = channel, adapter, policy
        self.features = list(F.validate_features(features, 8))
        self.budget = AcquisitionBudget(self.deadline, acquisition_limits)
        self.location = ServiceLocatedWorkflow(channel, adapter.namespace, self.features,
                                                location_limits, search_limits, policy)
        # The retained location wrapper already clamps to channel.deadline.
        F.need(self.location.deadline <= self.deadline, "LOCATED_RECEIPT_LOCATION_DEADLINE")
        # A route operation is one logical attempt, not one DHT packet. All
        # route events/raw Node traffic keep their own adopted service limits.
        self.prepaid_attempts = (location_limits["route_operations"]+location_limits["descriptor_requests"]
                                 +search_limits["requests"])
        self.budget.charge_external("location-and-search", self.prepaid_attempts, location_limits["reply_bytes"])
        self._location_limits, self._search_limits = deepcopy(location_limits), deepcopy(search_limits)
        self._profile = deepcopy(wire_profile)
        self._modules, self._receipts, self._verifier = module_custody, receipt_custody, verifier
        self._search = self._acquisition = None
        self.phase, self.closed = "CREATED", False

    def _active(self, phase):
        self.budget.active(); F.need(not self.closed and self.phase == phase, "LOCATED_RECEIPT_PHASE:"+self.phase)

    async def start(self):
        self._active("CREATED")
        self.phase = "STARTING"
        try:
            ready = await self.channel.start(); self.budget.active()
            F.need(ready["role"] == "reader", "LOCATED_RECEIPT_READY_ROLE")
            self.phase = "LOCATING"; return ready
        except BaseException:
            self.phase = "FAILED_START"; raise

    async def route(self, features, stripe=0, *, event_cap, peer_cap):
        self._active("LOCATING")
        result = await self.location.route(features, stripe, event_cap=event_cap, peer_cap=peer_cap)
        self.budget.active(); return result

    async def descriptor(self, peer, route_key, *, max_bytes=4096, max_age_ms=10000):
        self._active("LOCATING")
        result = await self.location.descriptor(peer, route_key, max_bytes=max_bytes, max_age_ms=max_age_ms)
        self.budget.active(); return result

    def begin_search(self):
        self._active("LOCATING"); self._search = self.location.begin_search()
        F.need(self._search.session.deadline <= self.deadline, "LOCATED_RECEIPT_SEARCH_DEADLINE")
        self.phase = "SEARCH"
        return {"contacts": sorted(self._search.endpoints), "mathematical_acceptance": False,
                "global_complete": False}

    async def offer(self, provider, max_bytes=1048576, *, max_expanded_bytes=1048576, max_age_ms=60000):
        self._active("SEARCH")
        result = await self._search.offer(provider, max_bytes, max_expanded_bytes=max_expanded_bytes, max_age_ms=max_age_ms)
        self.budget.active(); return result

    async def candidates(self, provider, snapshot_id, partition, start, limits):
        self._active("SEARCH")
        result = await self._search.candidates(provider, snapshot_id, partition, start, limits)
        self.budget.active(); return result

    def begin_acquisition(self):
        self._active("SEARCH")
        F.need(not self._search.session.pending, "LOCATED_RECEIPT_PENDING_SEARCH")
        endpoints = {}
        for name, endpoint in self._search.endpoints.items():
            F.need(endpoint == self._search._adopted_endpoints[name], "LOCATED_RECEIPT_CONTACT_CHANGED")
            expires = min(self.deadline, self._search._expiries[name])
            if time.monotonic() < expires:
                endpoints[name] = _ExpiringContact(endpoint, expires, self.policy, self.budget)
        F.need(endpoints, "LOCATED_RECEIPT_NO_UNEXPIRED_CUSTODY_CONTACT")
        self._acquisition = ReceiptAcquisition(self.adapter, endpoints, self._profile, self.budget,
            self._modules, self._receipts, verifier=self._verifier)
        self.phase = "ACQUIRING"
        return {"contacts": sorted(endpoints), "custody_roles": "UNPROVEN_TRY_AND_CHARGE",
                "mathematical_acceptance": False}

    async def export(self, provider, record):
        self._active("ACQUIRING"); F.validate_record(record, self.adapter.namespace)
        F.need((record["object_id"], F.record_id(record)) in self._search.session.seen_candidates,
               "LOCATED_RECEIPT_CANDIDATE_NOT_RETURNED_BY_THIS_SEARCH")
        return await self._acquisition.export(provider, record)

    async def body(self, provider, resolved, digest, maximum):
        self._active("ACQUIRING"); return await self._acquisition.body(provider, resolved, digest, maximum)

    async def receipt_offers(self, provider, module, *, max_offers=4, max_bytes=4096):
        self._active("ACQUIRING")
        return await self._acquisition.offers(provider, module, max_offers=max_offers, max_bytes=max_bytes)

    async def receipt(self, provider, module, entry):
        self._active("ACQUIRING"); return await self._acquisition.receipt(provider, module, entry)

    def custody_ready(self, resolved, entry, demanded_bodies=()):
        self._active("ACQUIRING"); return self._acquisition.custody_ready(resolved, entry, demanded_bodies)

    def admit(self, resolved, entry, operation_directory, **limits):
        self._active("ACQUIRING"); return self._acquisition.admit(resolved, entry, operation_directory, **limits)

    def report(self):
        return {"phase": self.phase, "closed": self.closed, "budget": self.budget.report(),
            "location": self.location.report(), "acquisition": None if self._acquisition is None else self._acquisition.report(),
            "prepaid_attempt_scope": "MAX_ROUTE_OPERATIONS_PLUS_DESCRIPTOR_REQUESTS_PLUS_SEARCH_HTTP_REQUESTS",
            "prepaid_bytes_scope": "LOCATION_DESCRIPTOR_REPLY_CAPACITY_INCLUDING_PREPAID_SEARCH_REPLY_CAPACITY",
            "location_grant": deepcopy(self._location_limits), "search_grant": deepcopy(self._search_limits),
            "dht_packet_bytes_in_reply_budget": False, "global_complete": False, "mathematical_acceptance": False}

    async def close(self):
        # The caller serializes methods and first cancels/awaits any active call.
        # Teardown uses the adopted child's bounded cleanup allowance, not a new
        # work deadline; no handle or work success is issued during teardown.
        F.need(self.budget.pending is None and self.location.report()["workflow"]["pending_requests"] == 0
               and (self._search is None or not self._search.session.pending), "LOCATED_RECEIPT_CLOSE_PENDING")
        if self.closed: return
        self.closed = True; self.phase = "CLOSED"
        try:
            if self._acquisition is not None: self._acquisition.close()
            else:
                self.budget.closed = True
                if self._verifier is not None: self._verifier.close()
        finally: await self.channel.close()

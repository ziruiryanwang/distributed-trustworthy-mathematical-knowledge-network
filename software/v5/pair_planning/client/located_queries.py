"""Adaptive located queries under one original child, grant and prepaid pool.

Trusted-owner composition only. Location hints never admit mathematics. Query
choice is local; no retry, new child, issuer, proof protocol or global scan.
"""
from copy import deepcopy
from pathlib import Path
import time

from discovery import formal_features as F
from discovery.search_session import LIMITS as SEARCH_LIMITS
from evidence_network.transport import EvidenceAcquisition
from location import available_descriptor as AD
from location import observed_route as OR
from location.controller_services import ServiceLocationProcess, ServiceLocatedWorkflow, ROLE_NAMES
from location.protocol import OwnerEgressPolicy
from location.workflow import LIMITS as LOCATION_LIMITS, _LocatedSearchClient
from modules import codec as C
from transport.located_receipts import _ExpiringContact
from .workspace_atomic import _action, _async_action, _under, _sha
from .workspace_validated import CommonsClient

SEARCH_ADDITIVE = ("providers", "snapshots", "requests", "pages", "examined", "candidates", "bytes")
LOCATION_ADDITIVE = ("route_operations", "routing_events", "routing_peer_slots",
                     "descriptor_requests", "contacts", "reply_bytes")


def _limits(value, bounds, label):
    F.fields(value, bounds)
    for key, pair in bounds.items(): F.uint(value[key], *pair, label+":"+key)


def _compatible(location, search):
    F.need(search["bytes"]+1024 <= location["reply_bytes"]
           and search["wall_ms"] <= location["wall_ms"]
           and search["providers"] <= location["contacts"], "LOCATED_SEARCH_SUBALLOCATION")


def _policy_state(policy):
    return policy._mode, policy._ports, policy._tests, deepcopy(policy._config)


def _snapshot(generation):
    """Scalar accounting only: no peer, route, coverage, candidate or offer map."""
    workflow, search, acquisition = (generation[key] for key in ("workflow", "search", "acquisition"))
    location = None
    if workflow is not None:
        budget = workflow._workflow
        location = {"status": budget._state, "used": dict(budget._used),
                    "pending_requests": int(budget._pending is not None),
                    "contacts": len(budget._contacts)}
    result = {"location": location, "search": None, "search_http": None,
              "acquisition_http": None, "structural_http": None}
    if search is not None:
        session = search.session
        result["search"] = {"status": session.state, "used": dict(session.used),
            "provider_slots_used": len(session.providers), "snapshot_attempt_slots": session.snapshot_slots,
            "pending_requests": len(session.pending), "reserved": dict(session.reserved)}
        result["search_http"] = dict(search.http)
    if acquisition is not None:
        result["acquisition_http"] = dict(acquisition.http)
        result["structural_http"] = acquisition.structural.report()
    return result


class _Binding:
    def __init__(self, envelope, generation, search):
        self.envelope, self.generation, self.search = envelope, generation, search
        self.session, self.clock = search.session, search.session.clock
        self.query, self.deadline = self.session._query, self.session.deadline
        self.limits = deepcopy(self.session.limits)
        self.endpoints, self.expiries = dict(search.endpoints), dict(search._expiries)
        self.acquisition = None

    def check(self):
        e, g, s = self.envelope, self.generation, self.search
        e.check_origin(); e.check_workflow(g)
        F.need(e.current is g and e.client._search is s and g["search"] is s
               and g["workflow"]._workflow._state == "SEARCH", "LOCATED_CURRENT_GENERATION")
        F.need(s.session is self.session and self.session.clock is s._clock is self.clock
               and self.session._query == self.query and self.session.deadline == self.deadline
               and self.session.limits == self.limits
               and s.endpoints == s._adopted_endpoints == self.endpoints
               and s._expiries == self.expiries and s._policy is e.policy,
               "LOCATED_ORIGINAL_SEARCH")
        if self.acquisition is not None:
            a = self.acquisition
            F.need(e.client._acquisition is a and g["acquisition"] is a
                   and a._search is s and a._handoff is None and a.budget is e.budget
                   and not a.closed, "LOCATED_ORIGINAL_ACQUISITION")


class _Contact(_ExpiringContact):
    def __init__(self, endpoint, expires, envelope, binding):
        super().__init__(endpoint, expires, envelope.policy, envelope.budget)
        self._binding = binding

    def validate(self):
        self._binding.check()
        return super().validate()


class _LocatedEnvelope:
    def __init__(self, client, channel, envelope, policy):
        F.fields(envelope, ("search", "location"))
        F.fields(envelope["search"], (*SEARCH_LIMITS, "generations"))
        search = {key: envelope["search"][key] for key in SEARCH_LIMITS}
        _limits(search, SEARCH_LIMITS, "LOCATED_SEARCH_ENVELOPE")
        _limits(envelope["location"], LOCATION_LIMITS, "LOCATED_LOCATION_ENVELOPE")
        F.uint(envelope["search"]["generations"], 1, 8, "LOCATED_GENERATION_CAP")
        _compatible(envelope["location"], search)
        F.need(type(policy) is OwnerEgressPolicy, "LOCATED_OWNER_POLICY")
        F.need(type(channel) is ServiceLocationProcess and channel.config["role"] == "reader"
               and channel.deadline == client.grant.deadline and channel.process is None
               and channel._start_task is channel._spawn_task is channel._close_task is None
               and channel.sequence == channel.sent == channel.received == channel.read_frames == 0
               and channel.stderr_task is None and not channel.stderr
               and not channel.closed and not channel.channel_failed and not channel.lock.locked(),
               "LOCATED_FRESH_ORIGINAL_READER")
        F.need(channel.adoption is channel._origin_adoption
               and channel.config["namespace"] == client.workspace.adapter.namespace
               and channel.config["egress"] == policy._config
               and set(channel.role_pins) == ROLE_NAMES,
               "LOCATED_ORIGINAL_NAMESPACE_POLICY_ADOPTION")
        F.need(client.workspace.root.is_relative_to(channel.adoption.workspace), "LOCATED_ADOPTED_WORKSPACE")
        _under(channel.evidence, client.grant.directory); _under(channel.state, client.grant.directory)
        self.client, self.grant, self.budget, self.channel = client, client.grant, client._budget, channel
        self.namespace, self.policy = client.workspace.adapter.namespace, policy
        self.policy_state = _policy_state(policy)
        self.limits = deepcopy(envelope); self._limits = deepcopy(envelope)
        self.deadline = min(client.grant.deadline, time.monotonic()+search["wall_ms"]/1000,
                            time.monotonic()+envelope["location"]["wall_ms"]/1000)
        self._deadline, self._grant_deadline = self.deadline, client.grant.deadline
        self._budget_limits = deepcopy(self.budget.limits)
        self._adoption, self._config = channel.adoption, deepcopy(channel.config)
        self._role_pins = dict(channel.role_pins)
        self._paths = channel.evidence, channel.state
        self.search_allocated = {key: 0 for key in SEARCH_ADDITIVE}
        self.location_allocated = {key: 0 for key in LOCATION_ADDITIVE}
        self.generations, self.current, self.started = [], None, False
        self.state = "RESERVED"

    def check_origin(self):
        c, ch = self.client, self.channel
        F.need(c.grant is self.grant and c._budget is self.budget and c._channel is ch
               and c._handoff is None and c._query_used
               and c._query_envelope is c._origin_query_envelope is self,
               "LOCATED_ORIGINAL_CLIENT_LIFETIME")
        F.need(ch.deadline == self.grant.deadline == self.budget.deadline == self._grant_deadline
               and self.deadline == self._deadline and self.limits == self._limits
               and self.budget.limits == self._budget_limits, "LOCATED_ORIGINAL_LIMITS")
        F.need(ch.adoption is ch._origin_adoption is self._adoption
               and ch.config == self._config and dict(ch.role_pins) == self._role_pins
               and (ch.evidence, ch.state) == self._paths
               and c.workspace.adapter.namespace == self.namespace
               and _policy_state(self.policy) == self.policy_state,
               "LOCATED_ORIGINAL_CHANNEL_POLICY")
        # Location transport is not mathematical authority. Its shorter service
        # lifetime cannot invalidate already-issued warrants or local work under
        # the original grant; new location work checks liveness separately.
        self.budget.active()

    def check_workflow(self, generation):
        workflow, budget = generation["workflow"], generation["workflow_budget"]
        F.need(type(workflow) is ServiceLocatedWorkflow and workflow.channel is self.channel
               and workflow._workflow is budget and workflow.deadline == budget._deadline == generation["deadline"]
               and budget._policy is self.policy and budget._clock is generation["clock"]
               and budget._namespace == self.namespace and budget._features == generation["features"]
               and budget._limits == generation["location_limits"]
               and budget._search_limits == generation["search_limits"], "LOCATED_ORIGINAL_WORKFLOW")

    def check(self, client):
        F.need(client is self.client and self.state in ("RESERVED", "LOCATING", "ACTIVE", "NO_CONTACTS"),
               "LOCATED_ENVELOPE_TERMINAL")
        self.check_origin()
        if self.current is None:
            F.need(client._search is None and client._acquisition is None, "LOCATED_EMPTY_SCOPE")
        else:
            g = self.current
            self.check_workflow(g)
            F.need(g["row"] is self.generations[-1], "LOCATED_CURRENT_ROW")
            if g["search"] is None:
                F.need(self.state == "LOCATING" and client._busy
                       and client._search is None and client._acquisition is None, "LOCATED_LOCATING_SCOPE")
            else:
                g["binding"].check()

    def validate_next(self, location, search, features, routes, descriptor_bytes, descriptor_age_ms):
        F.need(time.monotonic() < self.deadline, "LOCATED_ENVELOPE_EXPIRED")
        F.need(not self.channel.closed and not self.channel.channel_failed,
               "LOCATED_CHANNEL_CLOSED_OR_FAILED")
        _limits(location, LOCATION_LIMITS, "LOCATED_GENERATION_LOCATION")
        _limits(search, SEARCH_LIMITS, "LOCATED_GENERATION_SEARCH"); _compatible(location, search)
        F.need(len(self.generations) < self.limits["search"]["generations"], "LOCATED_GENERATION_LIMIT")
        for selected, allocated, caps, dimensions in (
            (location, self.location_allocated, self.limits["location"], LOCATION_ADDITIVE),
            (search, self.search_allocated, self.limits["search"], SEARCH_ADDITIVE)):
            F.need(selected["wall_ms"] <= caps["wall_ms"], "LOCATED_GENERATION_WALL_LIMIT")
            for key in dimensions:
                F.need(allocated[key]+selected[key] <= caps[key], "LOCATED_ENVELOPE_EXHAUSTED:"+key)
        F.need(search["inflight"] <= self.limits["search"]["inflight"], "LOCATED_GENERATION_INFLIGHT")
        F.uint(descriptor_bytes, 1024, 4096, "LOCATED_DESCRIPTOR_BYTES")
        F.uint(descriptor_age_ms, 1, 60000, "LOCATED_DESCRIPTOR_AGE")
        F.need(type(routes) is list and 1 <= len(routes) <= location["route_operations"], "LOCATED_ROUTE_PLAN")
        for item in routes:
            F.fields(item, ("features", "stripe", "event_cap", "peer_cap", "descriptors"))
            chosen = F.validate_features(item["features"], 8)
            F.need(set(chosen) <= set(features), "LOCATED_ROUTE_QUERY_SUBSET")
            F.uint(item["stripe"], 0, 255); F.uint(item["event_cap"], 1, location["routing_events"])
            F.uint(item["peer_cap"], 1, location["routing_peer_slots"])
            F.uint(item["descriptors"], 0, 64)
        F.need(sum(row["event_cap"] for row in routes) <= location["routing_events"]
               and sum(row["peer_cap"] for row in routes) <= location["routing_peer_slots"]
               and sum(row["descriptors"] for row in routes) <= location["descriptor_requests"],
               "LOCATED_ROUTE_SUBALLOCATION")
        F.need(self.budget.pending is None and not self.channel.lock.locked(), "LOCATED_OPERATION_PENDING")
        if self.current is not None:
            g = self.current
            F.need(g["workflow"]._workflow._pending is None, "LOCATED_WORKFLOW_PENDING")
            if g["search"] is not None:
                s, a = g["search"].session, g["acquisition"]
                F.need(not s.pending and not any(s.reserved.values())
                       and a.structural.inflight == a.structural.reserved_bytes == 0, "LOCATED_SEARCH_PENDING")

    def allocate(self, location, search, features):
        row = {"generation": len(self.generations)+1, "status": "ALLOCATED",
               "query_sha256": _sha(C.canonical({"namespace": self.namespace, "features": features})),
               "location_allocation": {key: location[key] for key in LOCATION_ADDITIVE},
               "search_allocation": {key: search[key] for key in SEARCH_ADDITIVE},
               "route_terminations": {key: 0 for key in OR.TERMINATIONS},
               "route_census": {key: 0 for key in OR.CENSUS[:-1]},
               "last_route_error": None, "descriptor_unavailable": 0, "outcome": None}
        for key in LOCATION_ADDITIVE: self.location_allocated[key] += location[key]
        for key in SEARCH_ADDITIVE: self.search_allocated[key] += search[key]
        self.generations.append(row)
        return {"row": row, "workflow": None, "workflow_budget": None,
                "search": None, "acquisition": None, "binding": None,
                "location_limits": deepcopy(location), "search_limits": deepcopy(search),
                "features": tuple(features), "deadline": None, "clock": None}

    def retire(self):
        if self.current is None: return
        g = self.current
        g["row"]["status"] = "RETIRED"
        g["workflow"]._workflow._state = "RETIRED"
        if g["search"] is not None: g["search"].session.state = "RETIRED"
        if g["acquisition"] is not None: g["acquisition"].retire_generation()
        g["row"]["outcome"] = _snapshot(g)
        self.client._candidates.clear(); self.client._staged.clear()
        self.client._search = self.client._acquisition = None
        self.current = None

    def terminal(self, status):
        if self.state == "FAILED" and status == "CLOSED": return
        self.state = status
        if self.generations and self.generations[-1]["status"] == "ALLOCATED":
            self.generations[-1]["status"] = status
        if self.client._search is not None: self.client._search.session.state = "CLIENT_"+status
        if self.current is not None:
            g = self.current; g["row"]["status"] = status
            if g["workflow"] is not None: g["workflow"]._workflow._state = "CLIENT_"+status
            if g["search"] is not None: g["search"].session.state = "CLIENT_"+status
            g["row"]["outcome"] = _snapshot(g)

    def report(self):
        rows = deepcopy(self.generations)
        if self.current is not None:
            rows[self.current["row"]["generation"]-1]["outcome"] = _snapshot(self.current)
        return {"schema": "DMKN_LOCATED_QUERY_ENVELOPE_V1", "status": self.state,
                "namespace": self.namespace, "limits": deepcopy(self.limits),
                "search_allocated": dict(self.search_allocated),
                "location_allocated": dict(self.location_allocated), "generations": rows,
                "remaining_wall_ms": max(0, int((self.deadline-time.monotonic())*1000)),
                "channel": self.channel.report(), "child_started": self.started,
                "accounting": "LOCATION_REPLY_CAP_INCLUDES_SEARCH;PREPAID_ONCE;NO_REFUNDS;"
                              "ROUTE_ATTEMPTS_AND_EVENTS_ARE_NOT_DHT_WIRE_BYTES",
                "global_complete": False, "mathematical_acceptance": False}


@_action
def reserve_located_queries(client, channel, envelope, policy):
    """Transfer one pristine reader and prepay a finite combined L/S envelope."""
    F.need(type(client) is CommonsClient and client._query_envelope is None
           and not client._query_used and client._channel is None and client._handoff is None
           and client._search is None and client._acquisition is None, "LOCATED_FRESH_CLIENT")
    selected = _LocatedEnvelope(client, channel, envelope, policy)
    path = Path(__file__).resolve()
    pins = [owner._pins[path] for owner in (client.receipt, client.aggregate, client.delta)
            if owner is not None and path in owner._pins]
    F.need(bool(pins) and all(pin == pins[0] for pin in pins), "LOCATED_REQUIRED_SOURCE_PIN")
    client._required_origins[__name__] = path; client._source_pins[path] = deepcopy(pins[0])
    client._active(); client._charge(C.canonical(envelope))
    location, search = envelope["location"], envelope["search"]
    requests = location["route_operations"]+location["descriptor_requests"]+search["requests"]
    client._budget.charge_external("located-query-envelope", requests, location["reply_bytes"])
    client._query_used = True; client._channel = channel
    client._query_envelope = client._origin_query_envelope = selected
    selected.check(client)
    return {"status": "LOCATED_QUERY_ENVELOPE_RESERVED", "generations": search["generations"],
            "prepaid": {"requests": requests, "reply_bytes": location["reply_bytes"]},
            "global_complete": False, "mathematical_acceptance": False}


@_async_action
async def next_located_query(client, specs, location_limits, search_limits, *, routes,
                             descriptor_bytes=4096, descriptor_age_ms=60000,
                             plan_pairs=False):
    """One adaptive query; optional pair anchors preserve legacy route subsets.

    Settled no-contact consumes its slice. Larger summaries use the same caps;
    no automatic fallback, extra generation or rebinding follows refusal.
    """
    F.need(type(client) is CommonsClient and type(client._query_envelope) is _LocatedEnvelope,
           "LOCATED_ENVELOPE_REQUIRED")
    selected = client._query_envelope
    try:
        selected.check(client)
        F.need(type(plan_pairs) is bool, "PAIR_QUERY_PLAN_OPTION")
        client._charge(C.canonical({"specs": specs, "routes": routes}))
        query_plan = client.workspace.adapter.plan_query(specs) if plan_pairs else None
        features = (query_plan["features"] if query_plan is not None else
                    client.workspace.adapter.compile_query(specs))
        selected.validate_next(location_limits, search_limits, features, routes,
                               descriptor_bytes, descriptor_age_ms)
        generation = selected.allocate(location_limits, search_limits, features)
        if query_plan is not None: generation["row"]["query_plan"] = deepcopy(query_plan)
        selected.retire()
        selected.current = generation; selected.state = generation["row"]["status"] = "LOCATING"
        workflow = ServiceLocatedWorkflow(selected.channel, selected.namespace, features,
                                          location_limits, search_limits, selected.policy)
        generation["workflow"], generation["workflow_budget"] = workflow, workflow._workflow
        workflow.deadline = workflow._workflow._deadline = min(workflow.deadline, selected.deadline)
        generation["deadline"], generation["clock"] = workflow.deadline, workflow._workflow._clock
        if not selected.started:
            selected.started = True
            ready = await selected.channel.start()
            F.need(ready["role"] == "reader", "LOCATED_READY_ROLE")
        selected.check(client)
        attempted = set()
        for plan in routes:
            located = await OR.route(workflow, plan["features"], plan["stripe"],
                                     event_cap=plan["event_cap"], peer_cap=plan["peer_cap"])
            row = generation["row"]
            row["route_terminations"][located["termination"]] += 1
            for key in OR.CENSUS[:-1]: row["route_census"][key] += located["census"][key]
            route_error = located["error"] or located["census"]["last_query_error"]
            if route_error is not None: row["last_route_error"] = route_error
            for peer in [peer for peer in located["peers"] if peer not in attempted][:plan["descriptors"]]:
                attempted.add(peer)
                answer = await AD.descriptor(workflow, peer, located["route_key"],
                                             max_bytes=descriptor_bytes, max_age_ms=descriptor_age_ms)
                if answer["status"] == "DESCRIPTOR_UNAVAILABLE": row["descriptor_unavailable"] += 1
            selected.check(client)
        budget = workflow._workflow
        budget._live(); selected.budget.active()
        F.need(time.monotonic() < selected.deadline, "LOCATED_ENVELOPE_EXPIRED")
        usable = [name for name in budget._contacts if budget._clock() < budget._expiries[name]]
        if not usable:
            generation["row"]["status"] = "NO_CONTACTS_IN_SELECTED_ROUTE_PLAN"
            budget._state = "RETIRED_NO_CONTACTS"
            generation["row"]["outcome"] = _snapshot(generation)
            selected.current = None; selected.state = "NO_CONTACTS"
            result = {"status": "NO_CONTACTS_IN_SELECTED_ROUTE_PLAN",
                      "generation": generation["row"]["generation"], "contacts": [],
                      "global_complete": False, "mathematical_acceptance": False}
            if query_plan is not None: result["query_plan"] = deepcopy(query_plan)
            return result
        search = workflow.begin_search()
        F.need(type(search) is _LocatedSearchClient, "LOCATED_ACTUAL_SEARCH_REQUIRED")
        generation["search"] = client._search = search
        binding = _Binding(selected, generation, search)
        generation["binding"] = binding
        custody = {name: _Contact(endpoint, search._expiries[name], selected, binding)
                   for name, endpoint in search.endpoints.items()}
        acquisition = EvidenceAcquisition(client.workspace.adapter, custody,
            client.workspace.config["wire_profile"], selected.budget,
            client.workspace.modules, client.workspace.packets, verifier=None)
        acquisition._search = search
        client._acquisition = generation["acquisition"] = binding.acquisition = acquisition
        selected.state = generation["row"]["status"] = "ACTIVE"
        binding.check()
        result = {"status": "QUERY_CONTACTS_READY", "generation": generation["row"]["generation"],
                  "contacts": sorted(search.endpoints), "contact_origin": "AUTHENTICATED_ADVISORY_DESCRIPTORS",
                  "global_complete": False, "mathematical_acceptance": False}
        if query_plan is not None: result["query_plan"] = deepcopy(query_plan)
        return result
    except BaseException:
        # Tombstone before diagnostics; cleanup failure must not bypass the
        # decorator's original owner/budget fail-stop or create a fresh child.
        try: selected.terminal("FAILED")
        except BaseException as error:
            client._failures.append("located_diagnostic:"+type(error).__name__)
        try: await selected.channel.close()
        except BaseException as error:
            client._failures.append("located_cleanup:"+type(error).__name__)
            client._cleanup_uncertain = True; client.workspace._poisoned = True
        raise

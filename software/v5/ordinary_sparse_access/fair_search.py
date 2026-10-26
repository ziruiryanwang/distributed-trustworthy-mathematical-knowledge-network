"""Finite serial discovery rounds within one existing prepaid search session.

Opportunity fairness is conditional on remaining resources and bounded local
work. No global coverage, relevance, acceptance, retry or new grant is promised.
"""
from __future__ import annotations

from copy import deepcopy
import math

from discovery import candidate_query as C
from discovery import formal_features as F
from discovery.search_session import SearchSession
from transport import fair_exchange as X
from transport import http_provider as H
from transport.clients import configured

HTTP_FIELDS = ("completed_requests", "failed_requests", "header_bytes",
               "actual_request_bytes", "actual_reply_bytes")
REFUSALS = frozenset(("CONNECTION_REFUSED", "CONNECTION_RESET", "BROKEN_PIPE",
                     "PEER_EOF", "HTTP_PROTOCOL", "ATTEMPT_TIMEOUT"))


class _NoSlice(Exception):
    pass


def _error(error):
    value = str(error)
    code = value if len(value) <= 160 and value and all(
        ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_:.+-" for ch in value) else "FAIR_METADATA_REJECTED"
    return dict(type=type(error).__name__, code=code)


class FairSearch:
    def __init__(self, session, endpoints, *, candidate_mode="atomic-v1"):
        F.need(type(session) is SearchSession, "FAIR_EXACT_SESSION")
        session._live()
        F.need(type(candidate_mode) is str and candidate_mode in ("atomic-v1", "sparse-v2"),
               "CANDIDATE_MODE")
        self.candidate_mode = candidate_mode
        self.session = session
        self.endpoints = configured(endpoints)
        F.need(all(type(endpoint) is H.Endpoint for endpoint in self.endpoints.values()), "FAIR_EXACT_ENDPOINT")
        F.need(session.limits["candidates"] <= 256 and session.limits["requests"] <= 512 and
               session.limits["bytes"] <= 32*1024**2, "FAIR_RESULT_PROFILE")
        self._bound = (session, session.clock, session._query, session.deadline,
                       deepcopy(session.limits), dict(self.endpoints), candidate_mode)
        self.http = {key: 0 for key in HTTP_FIELDS}
        self._started = False
        self._result = dict(status="STARTED", candidate_mode=candidate_mode,
                            matches=[], offers=[], provider_errors=[],
                            termination=None, global_complete=False, verified_scan_coverage=False,
                            mathematical_acceptance=False)
        self._settled()

    def _binding(self):
        session, clock, query, deadline, limits, endpoints, candidate_mode = self._bound
        F.need(self.session is session and session.clock is clock and session._query == query and
               session.deadline == deadline and session.limits == limits and self.endpoints == endpoints and
               self.candidate_mode == candidate_mode,
               "FAIR_OWNER_OR_GRANT_CHANGED")
        session._live()

    def _check(self, check_owner):
        self._binding()
        check_owner()
        self._binding()

    def _settled(self):
        F.need(not self.session.pending and all(value == 0 for value in self.session.reserved.values()),
               "FAIR_SERIAL_SETTLED_SESSION_REQUIRED")

    def _held(self, ticket):
        F.need(set(self.session.pending) == {ticket["ticket"]}, "FAIR_EXACT_PENDING_TICKET")
        held = self.session.pending[ticket["ticket"]]
        F.need({key: value for key, value in held.items() if key != "reservation"} == ticket and
               self.session.reserved == held["reservation"], "FAIR_TICKET_BINDING_CHANGED")
        return deepcopy(held["reservation"])

    def _abandon(self, ticket):
        reservation = self._held(ticket)
        expected = dict(self.session.used)
        expected["bytes"] += ticket["max_reply_bytes"]
        expected["examined"] += reservation["examined"]
        expected["candidates"] += reservation["candidates"]
        scans = self.session.candidate_scan_charges
        if ticket["operation"] == "candidates":
            scans += reservation["examined"]
        answer = self.session.abandon(ticket["ticket"])
        F.need(answer == dict(status="ABANDONED_CONSERVATIVELY_CHARGED", ticket=ticket["ticket"]) and
               self.session.used == expected and self.session.candidate_scan_charges == scans,
               "FAIR_SETTLEMENT_ACCOUNTING")
        self._settled()

    def _slice(self, active, ceiling):
        F.uint(active, 1, 64, "FAIR_ACTIVE_PROVIDERS")
        residual = math.floor((self.session.deadline-self.session.clock())*1000)
        # A closure reserve is included in EACH provider's share, not merely once
        # at the end of a round. Floor rounding cannot enlarge the original grant.
        timeout = min(ceiling, residual//active - X.CLOSE_SECONDS*1000)
        if timeout < 1:
            raise _NoSlice()
        return timeout

    def _refusal(self, provider, phase, reason):
        self._result["provider_errors"].append(dict(provider=provider, phase=phase,
            error=dict(type="SettledRefusal", code=reason)))

    async def _request(self, provider, phase, make_ticket, active, ceiling,
                       check_owner, recover_metadata_failure):
        self._check(check_owner)
        self._settled()
        timeout = self._slice(active, ceiling)
        until = self.session.clock()+timeout/1000
        ticket = make_ticket()
        route = H.OFFER_ROUTE if phase == "offer" else (
            H.SPARSE_CANDIDATE_ROUTE if self.candidate_mode == "sparse-v2" else H.CANDIDATE_ROUTE)
        try:
            self._check(check_owner)
            self._held(ticket)
            narrowed = min(timeout, ticket["remaining_wall_ms"],
                math.floor((until-self.session.clock())*1000),
                math.floor((self.session.deadline-self.session.clock())*1000)-X.CLOSE_SECONDS*1000)
            if narrowed < 1:
                raise _NoSlice()
            response = await X.exchange(self.endpoints[provider], route, ticket["request"],
                                        ticket["max_reply_bytes"], narrowed,
                                        absolute_deadline=self.session.deadline)
            self._check(check_owner)
            self._held(ticket)
        except BaseException:
            self.http["failed_requests"] += 1
            self._abandon(ticket)
            raise
        try:
            return self._consume(provider, phase, ticket, response, check_owner, recover_metadata_failure)
        except BaseException:
            # Response processing can fail before accept takes the ticket. Never
            # leave that reservation live; after accept it is already settled.
            if ticket["ticket"] in self.session.pending:
                self._abandon(ticket)
            raise

    def _consume(self, provider, phase, ticket, response, check_owner, recover_metadata_failure):
        if type(response) is X.SettledRefusal:
            F.need(response.reason in REFUSALS, "FAIR_REFUSAL_CLASSIFICATION")
            self.http["failed_requests"] += 1
            self._abandon(ticket)
            self._refusal(provider, phase, response.reason)
            return None
        F.need(type(response) is dict, "FAIR_EXCHANGE_RESPONSE")
        self.http["completed_requests"] += 1
        self.http["header_bytes"] += response["header_bytes"]
        self.http["actual_request_bytes"] += response["request_bytes"]
        self.http["actual_reply_bytes"] += response["reply_bytes"]
        if response["status"] != 200:
            F.need(response["status"] in (400, 404, 503), "FAIR_HTTP_STATUS")
            self._abandon(ticket)
            self._refusal(provider, phase, "HTTP_"+str(response["status"]))
            return None
        # Only this existing authenticated metadata boundary can invoke the
        # root's recovery predicate. Transport, cleanup and local checks above
        # never enter that catch or become permission to dial another provider.
        try:
            accepted = self.session.accept(ticket["ticket"], response["raw"])
        except Exception as error:
            self._check(check_owner)
            self._settled()
            allowed = recover_metadata_failure(error)
            F.need(type(allowed) is bool, "FAIR_RECOVERY_PREDICATE")
            self._check(check_owner)
            if not allowed:
                raise
            self._result["provider_errors"].append(dict(provider=provider, phase=phase, error=_error(error)))
            return None
        self._check(check_owner)
        self._settled()
        return accepted

    async def run(self, providers, offer, page, *, attempt_timeout_ms,
                  check_owner, recover_metadata_failure):
        F.need(not self._started, "FAIR_SINGLE_RUN")
        self._started = True
        try:
            F.need(callable(check_owner) and callable(recover_metadata_failure), "FAIR_CALLBACKS")
            F.uint(attempt_timeout_ms, 1, 60000, "FAIR_ATTEMPT_TIMEOUT")
            F.need(type(providers) is list and 1 <= len(providers) <= 64 and
                   all(type(name) is str and name in self.endpoints for name in providers) and
                   len(set(providers)) == len(providers), "FAIR_PROVIDER_LIST")
            F.fields(offer, ("max_bytes", "max_expanded_bytes", "max_age_ms"))
            for key, low, high in (("max_bytes", 1024, 1048576),
                                   ("max_expanded_bytes", 1024, 1048576), ("max_age_ms", 1, 3600000)):
                F.uint(offer[key], low, high, "FAIR_OFFER_LIMIT:"+key)
            F.fields(page, C.LIMITS)
            for key, (low, high) in C.LIMITS.items():
                F.uint(page[key], low, high, "FAIR_PAGE_LIMIT:"+key)
            providers, offer, page = tuple(providers), deepcopy(offer), deepcopy(page)
            ready = []
            for position, provider in enumerate(providers):
                offered = await self._request(provider, "offer",
                    lambda: self.session.begin_offer(self.endpoints[provider].label, **offer),
                    len(providers)-position, attempt_timeout_ms, check_owner, recover_metadata_failure)
                if offered is None:
                    continue
                self._result["offers"].append({key: offered[key] for key in
                    ("status", "snapshot_id", "reason") if key in offered} | {"provider": provider})
                if offered["status"] == "OFFERED":
                    parts = [deepcopy(part) for part in offered["partitions"] if part["anchor_count"] > 0]
                    if parts:
                        ready.append(dict(provider=provider, snapshot=offered["snapshot_id"],
                                          partitions=parts, position=0, start=0))
            while ready:
                following = []
                for position, state in enumerate(ready):
                    provider, sid = state["provider"], state["snapshot"]
                    partition = state["partitions"][state["position"]]
                    found = await self._request(provider, "candidates",
                        lambda: self.session.begin_candidates(self.endpoints[provider].label, sid,
                            partition["partition"], state["start"], page, mode=self.candidate_mode),
                        len(ready)-position+len(following), attempt_timeout_ms,
                        check_owner, recover_metadata_failure)
                    if found is None:
                        continue
                    self._result["matches"].extend(dict(provider=provider, snapshot_id=sid, record=row)
                                                   for row in found["new_matches"])
                    cursor = found["advisory_next"]
                    if cursor is None or cursor["next"] <= state["start"]:
                        state["position"] += 1
                        state["start"] = 0
                    else:
                        state["start"] = cursor["next"]
                    if state["position"] < len(state["partitions"]):
                        following.append(state)
                ready = following
            self._check(check_owner)
            self._result.update(status="INCOMPLETE_SEARCH", termination=(
                "SELECTED_CONTACTS_FINISHED_WITH_PROVIDER_ERRORS_NO_COMPLETENESS_CLAIM"
                if self._result["provider_errors"] else "SELECTED_CONTACTS_FINISHED_NO_COMPLETENESS_CLAIM"))
        except _NoSlice:
            self._result.update(status="INCOMPLETE_SEARCH", termination="FAIR_NO_LEGAL_ATTEMPT_SLICE")
        except BaseException as error:
            if type(error) is ValueError and str(error).startswith("SESSION_BUDGET:"):
                self._result.update(status="INCOMPLETE_SEARCH", termination=str(error))
            else:
                self._result.update(status="FAILED", termination="FATAL_SEARCH_FAILURE")
                raise
        self._check(check_owner)
        self._settled()
        return self.result()

    def result(self):
        return deepcopy(self._result)

    def report(self):
        return dict(session=self.session.report(), http=dict(self.http))

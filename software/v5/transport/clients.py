"""Explicit-endpoint search and typed acquisition clients, never mathematics.

Caller selects every operation. No discovery/proof ancestry crawl or automatic
retry. Use one owner/event-loop to serialize each session's public methods.
"""
from __future__ import annotations

from copy import deepcopy
import time

from discovery import formal_features as F
from custody.module_store import validate_body, permitted_hashes
from .http_provider import exchange, MODULE_MAX, OFFER_ROUTE, CANDIDATE_ROUTE


def configured(endpoints):
    F.need(type(endpoints) is dict and 1 <= len(endpoints) <= 64, "CONFIGURED_ENDPOINTS")
    result = {}
    for key, endpoint in endpoints.items():
        F.need(type(key) is str and 1 <= len(key) <= 128, "ENDPOINT_LABEL")
        endpoint.validate(); result[key] = endpoint
    return result


class SearchClient:
    def __init__(self, session, endpoints):
        self.session, self.endpoints = session, configured(endpoints)
        self.http = {"completed_requests": 0, "failed_requests": 0, "header_bytes": 0,
                     "actual_request_bytes": 0, "actual_reply_bytes": 0}

    async def _send(self, provider, ticket, route):
        try:
            timeout = max(1, min(60000, ticket["remaining_wall_ms"]))
            response = await exchange(self.endpoints[provider], route, ticket["request"], ticket["max_reply_bytes"], timeout)
        except BaseException:
            self.http["failed_requests"] += 1
            self.session.abandon(ticket["ticket"])
            raise
        self.http["completed_requests"] += 1
        self.http["header_bytes"] += response["header_bytes"]
        self.http["actual_request_bytes"] += response["request_bytes"]
        self.http["actual_reply_bytes"] += response["reply_bytes"]
        if response["status"] != 200:
            self.session.abandon(ticket["ticket"])
            raise ValueError("REMOTE_HTTP_ERROR_CONSERVATIVELY_CHARGED")
        return self.session.accept(ticket["ticket"], response["raw"])

    async def summary(self, provider, snapshot_id, max_bytes=1048576, *,
                      encoding="expanded-v1", max_expanded_bytes=1048576):
        F.need(provider in self.endpoints, "ENDPOINT_NOT_CONFIGURED")
        ticket = self.session.begin_summary(self.endpoints[provider].label, snapshot_id, max_bytes,
                                           encoding=encoding, max_expanded_bytes=max_expanded_bytes)
        route = "/v5/discovery/summary-compact" if ticket["summary_encoding"] == "compact-v1" else "/v5/discovery/summary"
        return await self._send(provider, ticket, route)

    async def offer(self, provider, max_bytes=1048576, *, max_expanded_bytes=1048576,
                    max_age_ms=60000):
        """Ask one owner-approved contact, without knowing a snapshot ID.

        No referral dialing or retries. OFFERED authenticates a selected index
        summary, not mathematics, availability, recency or global completeness.
        The existing session owns all offer/page requests and failure charges.
        """
        F.need(provider in self.endpoints, "ENDPOINT_NOT_CONFIGURED")
        ticket = self.session.begin_offer(self.endpoints[provider].label, max_bytes,
            max_expanded_bytes=max_expanded_bytes, max_age_ms=max_age_ms)
        return await self._send(provider, ticket, OFFER_ROUTE)

    async def page(self, provider, snapshot_id, partition, start, limits):
        F.need(provider in self.endpoints, "ENDPOINT_NOT_CONFIGURED")
        ticket = self.session.begin_page(self.endpoints[provider].label, snapshot_id, partition, start, limits)
        return await self._send(provider, ticket, "/v5/discovery/page")

    async def candidates(self, provider, snapshot_id, partition, start, limits):
        """Request proved positive records, never authenticated scan coverage."""
        F.need(provider in self.endpoints, "ENDPOINT_NOT_CONFIGURED")
        ticket = self.session.begin_candidates(self.endpoints[provider].label, snapshot_id, partition, start, limits)
        return await self._send(provider, ticket, CANDIDATE_ROUTE)

    def report(self): return {"session": self.session.report(), "http": dict(self.http)}


class AcquisitionClient:
    """One finite acquisition workflow; no certificates or silent budget renewal."""
    def __init__(self, adapter, endpoints, *, requests, bytes, wall_ms, local_custody=None):
        F.uint(requests, 1, 8192, "ACQUISITION_REQUESTS")
        F.uint(bytes, 1024, 1024**3, "ACQUISITION_BYTES")
        F.uint(wall_ms, 1, 3600000, "ACQUISITION_WALL")
        self.adapter, self.endpoints = adapter, configured(endpoints)
        self.local_custody = local_custody
        self.request_cap, self.byte_cap, self.deadline = requests, bytes, time.monotonic()+wall_ms/1000
        self.used_requests = self.used_bytes = self.reserved_bytes = self.inflight = 0
        self.actual_reply_bytes = self.header_bytes = self.failures = 0

    def _deadline(self):
        F.need(time.monotonic() < self.deadline, "ACQUISITION_DEADLINE")

    async def _get(self, provider, route, request, maximum):
        F.need(provider in self.endpoints, "ENDPOINT_NOT_CONFIGURED")
        F.uint(maximum, 1, MODULE_MAX, "ACQUISITION_OBJECT_BOUND")
        F.need(time.monotonic() < self.deadline, "ACQUISITION_DEADLINE")
        F.need(self.inflight < 8 and self.used_requests < self.request_cap
               and self.used_bytes+self.reserved_bytes+maximum <= self.byte_cap, "ACQUISITION_BUDGET")
        self.used_requests += 1; self.reserved_bytes += maximum; self.inflight += 1
        charged = maximum
        try:
            response = await exchange(self.endpoints[provider], route, request, maximum,
                                      max(1, min(60000, int((self.deadline-time.monotonic())*1000))))
            charged = len(response["raw"])
            self.actual_reply_bytes += charged; self.header_bytes += response["header_bytes"]
            F.need(response["status"] == 200, "ACQUISITION_HTTP_ERROR")
            F.need(time.monotonic() < self.deadline, "ACQUISITION_DEADLINE")
            value = self.adapter.codec.parse_json(response["raw"])
            F.need(self.adapter.codec.canonical(value) == response["raw"], "ACQUISITION_CANONICAL")
            return value
        except BaseException:
            self.failures += 1; raise
        finally:
            self.reserved_bytes -= maximum; self.used_bytes += charged; self.inflight -= 1

    async def export(self, provider, record):
        F.validate_record(record, self.adapter.namespace)
        F.need(record["schema"] == F.EXPORT_RECORD_SCHEMA, "ACQUISITION_EXPORT_RECORD")
        loc = record["locator"]
        request = {"module_id": loc["module_id"], "relative_name": deepcopy(loc["relative_name"]),
                   "group_index": loc["group_index"]}
        opening = await self._get(provider, "/v5/modules/group", request, min(MODULE_MAX, record["object_bytes"]))
        raw = self.adapter.encode_opening(loc["module_id"], loc["relative_name"], opening)
        result = self.adapter.resolve(record, raw)
        F.need(time.monotonic() < self.deadline, "ACQUISITION_DEADLINE")
        if self.local_custody is not None:
            self.local_custody.put_group(loc["module_id"], opening, before_commit=self._deadline)
        return {**result, "opening": opening}

    async def declaration(self, provider, module, relative_name, max_bytes):
        """NeedDeclaration without an index hint; structural binding only."""
        F.hexid(module); self.adapter.codec.validate_name(relative_name)
        opening = await self._get(provider, "/v5/modules/group", {"module_id": module,
                                 "relative_name": deepcopy(relative_name), "group_index": None}, max_bytes)
        raw = self.adapter.encode_opening(module, relative_name, opening)
        described = self.adapter.describe(raw)
        F.need(time.monotonic() < self.deadline, "ACQUISITION_DEADLINE")
        if self.local_custody is not None:
            self.local_custody.put_group(module, opening, before_commit=self._deadline)
        return {**self.adapter.resolve(described["record"], raw), "opening": opening}

    async def body(self, provider, resolved_export, body_hash, max_bytes):
        loc, descriptor = resolved_export["locator"], resolved_export["descriptor"]
        F.need(body_hash in permitted_hashes(descriptor), "ACQUISITION_BODY_NOT_COMMITTED")
        request = {"module_id": loc["module_id"], "relative_name": deepcopy(loc["relative_name"]),
                   "universes": descriptor["universes"], "body_hash": F.hexid(body_hash)}
        response = await self._get(provider, "/v5/modules/body", request, max_bytes)
        validate_body(self.adapter.codec, loc["module_id"], loc["relative_name"], descriptor, response, body_hash)
        F.need(time.monotonic() < self.deadline, "ACQUISITION_DEADLINE")
        if self.local_custody is not None:
            self.local_custody.put_body(loc["module_id"], loc["relative_name"], response, before_commit=self._deadline)
        return {"body": response, "assurance": "EXACT_DESCRIPTOR_COMMITTED_BODY", "mathematical_acceptance": False}

    def report(self):
        return {"requests": self.used_requests, "charged_reply_bytes": self.used_bytes,
                "reserved_reply_bytes": self.reserved_bytes, "actual_reply_bytes": self.actual_reply_bytes,
                "header_bytes": self.header_bytes, "failures": self.failures,
                "inflight": self.inflight, "mathematical_acceptance": False}

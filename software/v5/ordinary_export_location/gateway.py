"""Optional operator-only HTTP lookup adapter over one owned ordinary Node channel.

Loaded as transport.ordinary_location_gateway by the separate pinned operator role.
Readers do not import this module or the controller. The whole locate/descriptor
sequence has fail-fast ownership; there is no waiter queue or peer callback.
"""
from __future__ import annotations

import asyncio
import base64
import math
import secrets
import time

from discovery import formal_features as F
from . import contact_directory as CD
from . import ordinary_acquisition as O
from . import ordinary_location_controller as C

LIMITS = {"requests": (1, 4096), "reply_bytes": (1024, 64*1024**2), "descriptors": (1, 4096),
    "event_cap": (1, 4096), "max_providers": (1, 64), "max_descriptors": (1, 64),
    "max_bytes": (1024, 16384), "max_age_ms": (1, 3600000), "operation_ms": (1, 60000)}
SAFE_INTEGER = 2**53-1


class Gateway:
    def __init__(self, controller, *, policy, limits, deadline):
        F.need(type(controller) is C.OrdinaryLocationProcess and controller.config["role"] == "gateway" and
               type(policy) is CD.OwnerEgressPolicy, "EXPORT_GATEWAY_OWNER_ROLES")
        F.need(not controller.closed and not controller.channel_failed, "EXPORT_GATEWAY_TERMINAL_CONTROLLER")
        F.fields(limits, LIMITS)
        for name, bounds in LIMITS.items():
            F.uint(limits[name], *bounds, "EXPORT_GATEWAY_LIMIT:"+name)
        F.need(limits["reply_bytes"] >= limits["max_bytes"] and limits["descriptors"] >= 1,
               "EXPORT_GATEWAY_SLICE_MINIMUM")
        F.need(type(deadline) in (int, float) and math.isfinite(deadline) and
               time.monotonic() < deadline <= min(controller.deadline, controller.service_deadline),
               "EXPORT_GATEWAY_ORIGINAL_DEADLINE")
        self.controller, self.policy, self.limits, self.deadline = controller, policy, dict(limits), deadline
        self._controller_config = F.compact(controller.config)
        self._policy = F.compact(policy.report())
        self._busy = False
        self._ticket = 0
        self._data = {"admitted_requests": 0, "charged_reply_bytes": 0, "emitted_reply_bytes": 0,
            "descriptor_attempts": 0, "descriptor_unavailable": 0, "not_advertised_descriptors": 0,
            "expired_descriptors": 0,
            "lookup_commands": 0, "query_events": 0, "truncated_replies": 0,
            "busy_refusals": 0, "exhausted_refusals": 0, "expired_refusals": 0,
            "terminal_failure": False}

    def _owner(self):
        try:
            F.need(F.compact(self.controller.config) == self._controller_config and
                   F.compact(self.policy.report()) == self._policy, "EXPORT_GATEWAY_OWNER_BINDING_CHANGED")
            F.need(not self._data["terminal_failure"] and not self.controller.closed and
                   not self.controller.channel_failed, "EXPORT_GATEWAY_TERMINAL_CHANNEL")
            F.need(self.controller.process is not None and self.controller.process.returncode is None,
                   "EXPORT_GATEWAY_RUNNING_CONTROLLER")
        except BaseException:
            self._data["terminal_failure"] = True
            raise

    def request_limit(self, request):
        maximum = O.export_location_request_limit(request)
        F.need(request["semantic_id"] == self.controller.config["semantic_id"], "EXPORT_GATEWAY_SEMANTICS")
        return maximum

    def _refusal(self, request, reason, *, descriptors=0):
        F.need(reason in ("BUSY", "EXHAUSTED", "EXPIRED"), "EXPORT_GATEWAY_REFUSAL_REASON")
        self._data[reason.lower()+"_refusals"] += 1
        raw = F.compact(O.export_location_envelope(request, [], descriptors, False, reason=reason))
        F.need(len(raw) <= request["max_bytes"], "EXPORT_GATEWAY_REFUSAL_BYTES")
        # Pre-admission refusal framing is funded by H.Provider's independent HTTP grant.
        return raw

    def _remaining(self, until):
        remaining = math.floor(1000*(min(until, self.deadline, self.controller.deadline,
                                        self.controller.service_deadline)-time.monotonic()))
        if remaining < 1:
            raise C.LocationUnavailable("EXPIRED")
        return min(remaining, 60000)

    def _next_ticket(self):
        self._ticket += 1
        return F.uint(self._ticket, 1, 8192, "EXPORT_GATEWAY_TICKET_CAP")

    def _locate_reply(self, reply, payload):
        F.fields(reply, ("ticket", "route_key", "peers", "termination", "error", "census",
            "routing_peers_before", "routing_peers_after", "assurance", "global_complete", "mathematical_acceptance"))
        F.uint(reply["ticket"], 1, SAFE_INTEGER)
        F.need(reply["ticket"] == payload["ticket"] and reply["route_key"] == payload["route_key"] and
               reply["assurance"] == O.EXPORT_LOCATION_ASSURANCE and reply["global_complete"] is False and
               reply["mathematical_acceptance"] is False, "EXPORT_GATEWAY_LOCATE_BINDING")
        F.need(type(reply["peers"]) is list and len(reply["peers"]) <= payload["peer_cap"],
               "EXPORT_GATEWAY_LOCATE_PEERS")
        peers = [O.export_peer_id(peer) for peer in reply["peers"]]
        F.need(len(set(peers)) == len(peers), "EXPORT_GATEWAY_DUPLICATE_PEER")
        F.need(reply["termination"] in ("ROUTING_EXHAUSTED_NOT_GLOBAL_COMPLETE", "PROVIDER_BUDGET",
               "INCOMPLETE_QUERY_ERRORS", "INCOMPLETE_ABORTED_OR_FAILED"), "EXPORT_GATEWAY_LOCATE_TERMINATION")
        F.need(reply["error"] is None or (type(reply["error"]) is str and len(reply["error"]) <= 500),
               "EXPORT_GATEWAY_LOCATE_ERROR")
        F.uint(reply["routing_peers_before"], 0, SAFE_INTEGER); F.uint(reply["routing_peers_after"], 0, SAFE_INTEGER)
        census = reply["census"]
        F.fields(census, ("events", "send_query", "peer_response", "final_peer", "query_error",
                         "provider", "add_provider_write", "last_query_error"))
        for key in set(census)-{"last_query_error"}:
            F.uint(census[key], 0, SAFE_INTEGER)
        F.need(census["last_query_error"] is None or (type(census["last_query_error"]) is str and
               len(census["last_query_error"]) <= 500), "EXPORT_GATEWAY_QUERY_ERROR")
        self._data["query_events"] += census["events"]
        return peers

    def _descriptor_reply(self, reply, payload):
        if type(reply) is dict and reply.get("status") == "DESCRIPTOR_UNAVAILABLE":
            F.fields(reply, ("status", "ticket", "peer", "reason", "mathematical_acceptance"))
            F.uint(reply["ticket"], 1, SAFE_INTEGER)
            F.need(reply["ticket"] == payload["ticket"] and reply["peer"] == payload["peer"] and
                   reply["reason"] == "TCP_CONNECT_UNAVAILABLE" and reply["mathematical_acceptance"] is False,
                   "EXPORT_GATEWAY_DESCRIPTOR_UNAVAILABLE_BINDING")
            self._data["descriptor_unavailable"] += 1
            return None
        F.fields(reply, ("ticket", "authenticated_peer", "raw_base64", "request_body_bytes",
                         "reply_body_bytes", "framed_reply_bytes", "assurance", "mathematical_acceptance"))
        F.uint(reply["ticket"], 1, SAFE_INTEGER)
        F.need(reply["ticket"] == payload["ticket"] and reply["authenticated_peer"] == payload["peer"] and
               reply["assurance"] == O.EXPORT_LOCATION_ASSURANCE and reply["mathematical_acceptance"] is False,
               "EXPORT_GATEWAY_DESCRIPTOR_CHANNEL_BINDING")
        F.need(type(reply["raw_base64"]) is str and 0 < len(reply["raw_base64"]) <= 5464,
               "EXPORT_GATEWAY_DESCRIPTOR_BASE64_BOUND")
        raw = base64.b64decode(reply["raw_base64"], validate=True)
        F.need(base64.b64encode(raw).decode("ascii") == reply["raw_base64"] and 0 < len(raw) <= 4096,
               "EXPORT_GATEWAY_DESCRIPTOR_BASE64")
        for field, expected, maximum in (("request_body_bytes", len(F.compact(payload["request"])), 2048),
                ("reply_body_bytes", len(raw), 4096), ("framed_reply_bytes", len(raw)+4, 4100)):
            F.need(F.uint(reply[field], 1, maximum) == expected, "EXPORT_GATEWAY_DESCRIPTOR_BYTE_ACCOUNTING")
        descriptor = O.read_export_descriptor(raw, payload["request"], reply["authenticated_peer"])
        if descriptor["schema"] == O.EXPORT_DESCRIPTOR_UNAVAILABLE:
            self._data["not_advertised_descriptors"] += 1
            return None
        return descriptor

    def _encode(self, request, held, attempts, truncated):
        now = time.monotonic()
        candidates, byte_omitted = [], False
        for peer, endpoint, expiry in held.values():
            remaining = math.floor(1000*(expiry-now))
            if remaining < 1:
                truncated = True
                continue
            candidate = {"peer_id": peer, "endpoint": endpoint, "remaining_ms": min(3600000, remaining)}
            # Encode only one bounded prefix plus one candidate, never all 64 expanded rows.
            trial = F.compact(O.export_location_envelope(request, [*candidates, candidate], attempts, False))
            if len(candidates) >= request["max_providers"] or len(trial) > request["max_bytes"]:
                truncated = byte_omitted = True
                break
            candidates.append(candidate)
        raw = F.compact(O.export_location_envelope(request, candidates, attempts, truncated))
        F.need(len(raw) <= request["max_bytes"], "EXPORT_GATEWAY_REPLY_BOUND")
        O.read_export_location_reply(raw, request)
        return raw, byte_omitted, truncated

    async def lookup(self, request, *, until):
        self.request_limit(request)
        self._owner()
        F.need(type(until) in (int, float) and math.isfinite(until), "EXPORT_GATEWAY_HTTP_DEADLINE")
        began = time.monotonic()
        cutoff = min(until, self.deadline, self.controller.deadline, self.controller.service_deadline,
                     began+min(request["timeout_ms"], self.limits["operation_ms"])/1000)
        if cutoff <= began:
            return self._refusal(request, "EXPIRED")
        if self._busy:
            return self._refusal(request, "BUSY")
        maximum = min(request["max_bytes"], self.limits["max_bytes"])
        if self._data["admitted_requests"] >= self.limits["requests"] or (
                self._data["charged_reply_bytes"]+maximum > self.limits["reply_bytes"] or
                self._data["descriptor_attempts"] >= self.limits["descriptors"]):
            return self._refusal(request, "EXHAUSTED")
        # One owner for the complete locate->descriptor sequence; Node's known-peer
        # cache is query-local and must not be replaced by a competing HTTP lookup.
        self._busy = True
        self._data["admitted_requests"] += 1; self._data["charged_reply_bytes"] += maximum
        local = dict(request)
        local["max_bytes"] = maximum
        local["max_providers"] = min(request["max_providers"], self.limits["max_providers"],
                                     self.controller.config["limits"]["provider_limit"])
        local["max_descriptors"] = min(request["max_descriptors"], self.limits["max_descriptors"],
            self.limits["descriptors"]-self._data["descriptor_attempts"])
        held, attempts = {}, 0
        try:
            payload = {"ticket": self._next_ticket(), "operation": "ordinary-route",
                "route_key": request["route_key"], "spec": O.export_route_spec(request["semantic_id"], request["export_id"]),
                "event_cap": min(self.limits["event_cap"], self.controller.config["limits"]["query_events"]),
                "peer_cap": local["max_providers"], "remaining_wall_ms": self._remaining(cutoff)}
            self._data["lookup_commands"] += 1
            located = await self.controller.command("locate", payload, until=cutoff)
            self._owner()
            peers = self._locate_reply(located, payload)
            truncated = located["termination"] != "ROUTING_EXHAUSTED_NOT_GLOBAL_COMPLETE"
            for position, peer in enumerate(peers):
                if attempts >= local["max_descriptors"]:
                    truncated = True
                    break
                self._owner()
                descriptor_started = time.monotonic()
                descriptor_request = O.export_descriptor_request(request["semantic_id"], request["export_id"],
                                                                  secrets.token_hex(32))
                payload = {"ticket": self._next_ticket(), "operation": "ordinary-descriptor", "peer": peer,
                    "request": descriptor_request, "max_reply_bytes": 4096,
                    "remaining_wall_ms": self._remaining(cutoff)}
                attempts += 1; self._data["descriptor_attempts"] += 1
                result = await self.controller.command("descriptor", payload, until=cutoff)
                self._owner()
                descriptor = self._descriptor_reply(result, payload)
                if descriptor is None:
                    continue
                endpoint_spec = descriptor["endpoints"][0]
                endpoint = self.policy.endpoint(endpoint_spec)
                # The lookup execution cutoff is not the custodian-hint lease.
                # Original service/policy lifetimes still bound every hint.
                expiry = min(self.deadline, self.controller.deadline, self.controller.service_deadline,
                    descriptor_started+self.limits["max_age_ms"]/1000,
                    descriptor_started+descriptor["remaining_ms"]/1000)
                if expiry <= time.monotonic():
                    self._data["expired_descriptors"] += 1
                    continue
                identity = O.endpoint_identity(endpoint)
                if identity in held:
                    old_peer, old_endpoint, old_expiry = held[identity]
                    held[identity] = (old_peer, old_endpoint, min(old_expiry, expiry))
                else:
                    held[identity] = (peer, endpoint_spec, expiry)
                _, byte_omitted, _ = self._encode(local, held, attempts, truncated)
                if byte_omitted:
                    truncated = True
                    break
            self._remaining(cutoff); self._owner()
            raw, _, truncated = self._encode(local, held, attempts, truncated)
            self._data["truncated_replies"] += int(truncated)
            self._data["emitted_reply_bytes"] += len(raw)
            return raw
        except C.LocationUnavailable as error:
            # The concrete controller promises this only before a command was issued.
            return self._refusal(local, error.reason, descriptors=attempts)
        except BaseException:
            self._data["terminal_failure"] = True
            raise
        finally:
            self._busy = False

    def report(self):
        return {**self._data, "busy": self._busy, "limits": dict(self.limits),
            "remaining_ms": max(0, math.floor(1000*(min(self.deadline, self.controller.deadline,
                                                        self.controller.service_deadline)-time.monotonic()))),
            "pre_admission_refusals": "FUNDED_BY_HTTP_PROVIDER_GRANT_NOT_BACKEND_LOOKUP_GRANT",
            "global_complete": False, "mathematical_acceptance": False}

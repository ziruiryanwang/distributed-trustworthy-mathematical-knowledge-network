"""Bounded, caller-driven public search accounting and authenticated coverage.

No networking or research planner. The transport must enforce each ticket's
reply byte ceiling while receiving, and supply hard process/resource isolation.
Raw bytes are charged even when their decoding or authentication fails.
"""
from __future__ import annotations

from copy import deepcopy
import time

from . import discovery_query as Q
from . import formal_features as F
from . import summary_wire as W

LIMITS = {"providers": (1, 64), "snapshots": (1, 256), "requests": (1, 8192),
          "pages": (1, 4096), "examined": (1, 131072), "candidates": (1, 32768),
          "bytes": (1024, 1024**3), "wall_ms": (1, 3600000), "inflight": (1, 8)}


class SearchSession:
    def __init__(self, namespace, features, limits, *, clock=None):
        F.fields(limits, LIMITS)
        for key, (low, high) in LIMITS.items(): F.uint(limits[key], low, high, "SESSION_LIMIT:"+key)
        self.namespace, self.features = F.hexid(namespace), list(F.validate_features(features, 8))
        self._query = (self.namespace, tuple(self.features))
        self.limits, self.clock = dict(limits), clock or time.monotonic
        self.deadline = self.clock() + limits["wall_ms"] / 1000
        self.used = {k: 0 for k in ("requests", "request_bytes", "pages", "examined", "candidates", "bytes")}
        self.reserved = {k: 0 for k in ("examined", "candidates", "bytes")}
        self.providers, self.attempted_snapshots = set(), set()
        self.snapshot_slots, self.offer_hints = 0, {}
        self.summaries, self.coverage, self.pending = {}, {}, {}
        self.last_verified = {}
        self.last_advisory, self.seen_candidates, self.candidate_first = {}, {}, {}
        self.candidate_scan_charges, self.duplicate_candidates, self.metadata_conflicts = 0, 0, 0
        self.sequence, self.state, self.last_refusal = 0, "ACTIVE", None

    def _live(self):
        F.need(self.state == "ACTIVE", "SESSION_" + self.state)
        F.need((self.namespace, tuple(self.features)) == self._query, "SESSION_QUERY_CHANGED")
        if self.clock() >= self.deadline:
            self.state = "DEADLINE_EXHAUSTED"
            raise ValueError("SESSION_DEADLINE_EXHAUSTED")

    def _reserve(self, provider, snapshot, operation, request, byte_cap, examined=0, candidates=0,
                 *, summary_encoding=None, max_expanded_bytes=None, max_age_ms=None):
        self._live()
        F.need(type(provider) is str and 0 < len(provider.encode("utf-8")) <= 256
               and all(ord(ch) >= 32 for ch in provider), "SESSION_PROVIDER_LABEL")
        if operation == "offer": F.need(snapshot is None, "SESSION_OFFER_SNAPSHOT_UNKNOWN")
        else: F.hexid(snapshot)
        slot = int(operation == "offer" or snapshot not in self.attempted_snapshots)
        request_bytes = len(F.compact(request))
        F.need(request_bytes <= 16384, "SESSION_REQUEST_BYTE_CAP")
        additions = {"bytes": byte_cap, "examined": examined, "candidates": candidates}
        def within(ok, label):
            if not ok:
                self.last_refusal = "SESSION_BUDGET:" + label
                raise ValueError(self.last_refusal)
        within(len(self.pending) < self.limits["inflight"], "inflight")
        within(len(self.providers | {provider}) <= self.limits["providers"], "providers")
        within(self.snapshot_slots + slot <= self.limits["snapshots"], "snapshots")
        within(self.used["requests"] < self.limits["requests"], "requests")
        if operation in ("page", "candidates"): within(self.used["pages"] < self.limits["pages"], "pages")
        for key, value in additions.items():
            within(self.used[key] + self.reserved[key] + value <= self.limits[key], key)
        self.sequence += 1
        ticket = {"ticket": self.sequence, "provider": provider, "snapshot_id": snapshot,
                  "namespace": self.namespace, "features": list(self.features),
                  "operation": operation, "request": deepcopy(request), "max_reply_bytes": byte_cap,
                  "request_bytes": request_bytes,
                  "remaining_wall_ms": max(0, int((self.deadline-self.clock()) * 1000))}
        if operation in ("summary", "offer"):
            ticket["summary_encoding"] = summary_encoding
            ticket["max_expanded_bytes"] = max_expanded_bytes
        if operation == "offer":
            ticket["offer_until"] = min(self.deadline, self.clock() + max_age_ms/1000)
            ticket["remaining_wall_ms"] = min(ticket["remaining_wall_ms"], max_age_ms)
        self.pending[self.sequence] = {**deepcopy(ticket), "reservation": additions}
        self.providers.add(provider); self.snapshot_slots += slot
        if snapshot is not None: self.attempted_snapshots.add(snapshot)
        self.used["requests"] += 1
        self.used["request_bytes"] += request_bytes
        if operation in ("page", "candidates"): self.used["pages"] += 1
        for key, value in additions.items(): self.reserved[key] += value
        return ticket

    def begin_offer(self, provider, max_bytes=1048576, *, max_expanded_bytes=1048576,
                    max_age_ms=60000):
        """Select no SID in advance; each attempt consumes one snapshot slot.

        max_age_ms uses only the owner's request-start monotonic clock. It
        limits offer adoption/hint reuse, not an immutable snapshot's validity.
        All bytes, attempts and providers share the normal session allowance.
        """
        F.uint(max_bytes, 1024, 1048576, "SESSION_OFFER_BYTES")
        F.uint(max_expanded_bytes, 1024, 1048576, "SESSION_SUMMARY_EXPANDED_BYTES")
        F.uint(max_age_ms, 1, 3600000, "SESSION_OFFER_AGE")
        request = {"namespace": self.namespace, "features": list(self.features),
                   "max_bytes": max_bytes, "max_expanded_bytes": max_expanded_bytes}
        return self._reserve(provider, None, "offer", request, max_bytes,
                             summary_encoding="compact-v1", max_expanded_bytes=max_expanded_bytes,
                             max_age_ms=max_age_ms)

    def begin_summary(self, provider, snapshot_id, max_bytes=1048576, *,
                      encoding="expanded-v1", max_expanded_bytes=1048576):
        F.uint(max_bytes, 1024, 1048576, "SESSION_SUMMARY_BYTES")
        F.need(encoding in ("expanded-v1", "compact-v1"), "SESSION_SUMMARY_ENCODING")
        F.uint(max_expanded_bytes, 1024, 1048576, "SESSION_SUMMARY_EXPANDED_BYTES")
        request = {"snapshot_id": F.hexid(snapshot_id), "features": list(self.features), "max_bytes": max_bytes}
        if encoding == "compact-v1": request["max_expanded_bytes"] = max_expanded_bytes
        return self._reserve(provider, snapshot_id, "summary", request, max_bytes,
                             summary_encoding=encoding, max_expanded_bytes=max_expanded_bytes)

    def begin_page(self, provider, snapshot_id, partition, start, limits):
        self._live(); F.hexid(snapshot_id)
        F.need(snapshot_id in self.summaries, "SESSION_VERIFIED_SUMMARY_REQUIRED")
        F.uint(partition, 0, 255, "SESSION_PARTITION")
        plan = Q.plan_partitions(self.summaries[snapshot_id])[partition]
        F.uint(start, 0, plan["anchor_count"], "SESSION_START")
        request = {"schema": "DMKN_FORMAL_QUERY_REQUEST_V1", "namespace": self.namespace,
                   "snapshot_id": snapshot_id, "features": list(self.features), "partition": partition,
                   "anchor": plan["anchor"], "start": start, "limits": deepcopy(limits)}
        Q.validate_request(request, self.namespace)
        return self._reserve(provider, snapshot_id, "page", request, limits["bytes"],
                             limits["examined"], limits["matches"])

    def begin_candidates(self, provider, snapshot_id, partition, start, limits):
        """Positive-only query; full scan allowance shares the examined budget.

        Returned provider counters never refund the reserved scan allowance.
        This consumes the same request/page/provider/byte/inflight budgets as
        ordinary pages, and requires the same already-verified pinned summary.
        """
        from . import candidate_query as C
        self._live(); F.hexid(snapshot_id)
        F.need(snapshot_id in self.summaries, "SESSION_VERIFIED_SUMMARY_REQUIRED")
        F.uint(partition, 0, 255, "SESSION_PARTITION")
        plan = Q.plan_partitions(self.summaries[snapshot_id])[partition]
        F.uint(start, 0, plan["anchor_count"], "SESSION_START")
        request = {"schema": "DMKN_FORMAL_CANDIDATE_REQUEST_V1", "namespace": self.namespace,
                   "snapshot_id": snapshot_id, "features": list(self.features), "partition": partition,
                   "anchor": plan["anchor"], "start": start, "limits": deepcopy(limits)}
        C.validate_request(request, self.namespace)
        return self._reserve(provider, snapshot_id, "candidates", request, limits["bytes"],
                             limits["scanned"], limits["matches"])

    def _take(self, ticket_id, received_bytes):
        F.uint(ticket_id, 1, self.sequence, "SESSION_TICKET")
        F.need(ticket_id in self.pending, "SESSION_TICKET_NOT_PENDING")
        ticket = self.pending.pop(ticket_id)
        for key, value in ticket["reservation"].items(): self.reserved[key] -= value
        self.used["bytes"] += received_bytes
        if ticket["operation"] == "candidates":
            # This charge survives parsing, proof, deadline and transport failure.
            # A provider's claimed skipped work is not authenticated and cannot
            # be used to refund the owner's finite aggregate allowance.
            self.used["examined"] += ticket["reservation"]["examined"]
            self.candidate_scan_charges += ticket["reservation"]["examined"]
        return ticket

    def _conservative_rows(self, ticket):
        for key in ("examined", "candidates"):
            if key == "examined" and ticket["operation"] == "candidates": continue
            self.used[key] += ticket["reservation"][key]

    def _prepare_candidates(self, records):
        """Dedup exact committed claims, never give first metadata authority.

        Different RecordIDs for one object ID remain bounded alternatives until
        acquisition/recomputation. A malicious first provider must not suppress
        a later honest candidate merely by claiming the same object identity.
        """
        updates, first_updates, new, conflicts, duplicates = {}, {}, [], [], 0
        for record in records:
            self._live()
            key, rid = record["object_id"], F.record_id(record)
            pair = (key, rid)
            if pair in updates or pair in self.seen_candidates:
                duplicates += 1
            else:
                new.append(deepcopy(record))
                first = first_updates.get(key, self.candidate_first.get(key))
                if first is None: first_updates[key] = rid
                elif first != rid:
                    conflicts.append({"object_id": key, "record_id": rid, "earlier_record_id": first,
                                      "assurance": "ALTERNATIVE_METADATA_NOT_FIRST_SEEN_AUTHORITY"})
            updates[pair] = True
        self._live()
        return updates, first_updates, new, conflicts, duplicates

    def _commit_candidates(self, prepared):
        updates, first_updates, new, conflicts, duplicates = prepared
        self.seen_candidates.update(updates); self.candidate_first.update(first_updates)
        self.duplicate_candidates += duplicates; self.metadata_conflicts += len(conflicts)
        return {"new_matches": new, "duplicate_matches": duplicates, "metadata_conflicts": conflicts}

    def _store_summary(self, selected, verified):
        if selected in self.summaries:
            F.need(self.summaries[selected] == verified, "SESSION_SNAPSHOT_CONFLICT")
        else:
            self.summaries[selected] = verified
            self.coverage[selected] = Q.Coverage(verified)

    def _offer_live(self, ticket):
        self._live()
        F.need(self.clock() < ticket["offer_until"], "SESSION_OFFER_EXPIRED")

    def _accept_offer(self, ticket, raw):
        self._offer_live(ticket)
        response = F.strict(raw, ticket["max_reply_bytes"])
        F.fields(response, ("schema", "namespace", "features", "status", "reason", "summary",
                            "global_complete", "mathematical_acceptance"))
        F.need(response["schema"] == "DMKN_DISCOVERY_OFFER_V1"
               and response["namespace"] == ticket["namespace"]
               and response["features"] == ticket["features"], "SESSION_OFFER_QUERY_BINDING")
        F.need(response["global_complete"] is False and response["mathematical_acceptance"] is False,
               "SESSION_OFFER_ASSURANCE")
        status, reason = response["status"], response["reason"]
        if status != "OFFERED":
            F.need((status == "NO_OFFER" and reason in ("ROLE_NOT_SERVED", "NAMESPACE_NOT_SERVED"))
                   or (status == "REFUSED" and reason == "SUMMARY_RESOURCE_BOUND"), "SESSION_OFFER_STATUS")
            F.need(response["summary"] is None, "SESSION_OFFER_NO_SUMMARY")
            self._offer_live(ticket)
            return {"status": status, "reason": reason, "provider": ticket["provider"],
                    "global_complete": False, "mathematical_acceptance": False}
        F.need(reason == "SNAPSHOT_SELECTED" and type(response["summary"]) is dict, "SESSION_OFFER_SUMMARY")
        selected = F.hexid(response["summary"].get("snapshot_id"))
        expanded = W.decode_summary(F.compact(response["summary"]), selected,
            ticket["namespace"], ticket["features"], max_wire_bytes=ticket["max_reply_bytes"],
            max_expanded_bytes=ticket["max_expanded_bytes"], check_budget=lambda: self._offer_live(ticket))
        verified = Q.verify_summary(selected, ticket["namespace"], ticket["features"], expanded)
        self._offer_live(ticket)
        self._store_summary(selected, verified)
        self.attempted_snapshots.add(selected)  # Its attempt slot was already reserved before I/O.
        self.offer_hints[(ticket["provider"], selected)] = ticket["offer_until"]
        return {"status": "OFFERED", "provider": ticket["provider"], "snapshot_id": selected,
                "partitions": Q.plan_partitions(verified),
                "remaining_hint_ms": max(0, int((ticket["offer_until"]-self.clock())*1000)),
                "assurance": "AUTHENTICATED_PROVIDER_SELECTED_METADATA_ONLY",
                "global_complete": False, "mathematical_acceptance": False}

    def accept(self, ticket_id, raw):
        """Consume one response. Invalid replies raise, with costs preserved."""
        F.need(type(raw) is bytes, "SESSION_RAW_BYTES_REQUIRED")
        ticket = self._take(ticket_id, len(raw))
        try:
            if len(raw) > ticket["max_reply_bytes"]:
                self.state = "TRANSPORT_BYTE_VIOLATION"
                raise ValueError("SESSION_TRANSPORT_BYTE_VIOLATION")
            self._live()
            F.need((ticket["namespace"], tuple(ticket["features"])) == self._query,
                   "SESSION_TICKET_QUERY_BINDING")
            selected = ticket["snapshot_id"]
            if ticket["operation"] == "offer": return self._accept_offer(ticket, raw)
            if ticket["operation"] == "summary":
                if ticket["summary_encoding"] == "compact-v1":
                    response = W.decode_summary(raw, selected, self.namespace, self.features,
                        max_wire_bytes=ticket["max_reply_bytes"], max_expanded_bytes=ticket["max_expanded_bytes"],
                        check_budget=self._live)
                else:
                    response = F.strict(raw, min(ticket["max_reply_bytes"], ticket["max_expanded_bytes"]))
                verified = Q.verify_summary(selected, self.namespace, self.features, response)
                self._live()
                self._store_summary(selected, verified)
                return {"status": "VERIFIED_SUMMARY", "snapshot_id": selected,
                        "partitions": Q.plan_partitions(verified), "mathematical_acceptance": False}
            response = F.strict(raw, ticket["max_reply_bytes"])
            if ticket["operation"] == "candidates":
                from . import candidate_query as C
                verified = C.verify_page(self.summaries[selected], ticket["request"], response,
                                         check_budget=self._live)
                prepared = self._prepare_candidates(verified["matches"])
                self._live()
                self.used["candidates"] += len(verified["matches"])
                dedup = self._commit_candidates(prepared)
                self.last_advisory.setdefault(selected, {})[ticket["request"]["partition"]] = {
                    "provider": ticket["provider"], "next_cursor": deepcopy(verified["advisory_next"]),
                    "provider_termination": verified["provider_termination"], "verified_scan_coverage": False}
                return {"status": "VERIFIED_CANDIDATES", **verified, **dedup}
            prepared = None
            def before_page_commit():
                nonlocal prepared
                self._live()
                # Coverage invokes this only AFTER its existing full verification,
                # but BEFORE committing an interval. Do not mutate dedup early.
                wanted = set(ticket["features"])
                records = [row["record"] for row in response["examined"]
                           if wanted <= set(row["record"]["features"])]
                prepared = self._prepare_candidates(records)
            verified = self.coverage[selected].accept(ticket["request"], response, before_commit=before_page_commit)
            self.used["examined"] += len(response["examined"])
            self.used["candidates"] += len(verified["matches"])
            dedup = self._commit_candidates(prepared)
            self.last_verified.setdefault(selected, {})[verified["partition"]] = {
                "start": verified["start"], "next": verified["next"],
                "next_cursor": deepcopy(response["next_cursor"])}
            return {"status": "VERIFIED_PAGE", **verified, **dedup,
                    "next_cursor": deepcopy(response["next_cursor"])}
        except Exception:
            self._conservative_rows(ticket)
            raise

    def abandon(self, ticket_id):
        """Unknown/partial transport outcome: consume full reserved allowances."""
        F.uint(ticket_id, 1, self.sequence, "SESSION_TICKET")
        F.need(ticket_id in self.pending, "SESSION_TICKET_NOT_PENDING")
        maximum = self.pending[ticket_id]["max_reply_bytes"]
        ticket = self._take(ticket_id, maximum)
        self._conservative_rows(ticket)
        return {"status": "ABANDONED_CONSERVATIVELY_CHARGED", "ticket": ticket_id}

    def report(self):
        if self.state == "ACTIVE" and self.clock() >= self.deadline: self.state = "DEADLINE_EXHAUSTED"
        return {"status": self.state, "last_refusal": self.last_refusal,
                "namespace": self.namespace, "features": list(self.features),
                "used": {**self.used, "providers": len(self.providers), "snapshots": len(self.attempted_snapshots)},
                "snapshot_budget": {"charged_attempt_slots": self.snapshot_slots,
                                    "known_snapshot_ids": len(self.attempted_snapshots),
                                    "limit": self.limits["snapshots"]},
                "reserved": dict(self.reserved), "pending_requests": len(self.pending),
                "remaining_wall_ms": max(0, int((self.deadline-self.clock()) * 1000)),
                "coverage": {key: value.report() for key, value in self.coverage.items()},
                "last_verified": deepcopy(self.last_verified),
                "last_advisory": deepcopy(self.last_advisory),
                "candidate_search": {"charged_scan_allowances": self.candidate_scan_charges,
                                     "unique_verified_records": len(self.seen_candidates),
                                     "duplicate_verified_hits": self.duplicate_candidates,
                                     "alternative_metadata_claims": self.metadata_conflicts,
                                     "duplicates_still_charged": True},
                "offer_hints": [{"provider": provider, "snapshot_id": sid,
                                 "remaining_ms": max(0, int((until-self.clock())*1000)),
                                 "fresh": self.clock() < until}
                                for (provider, sid), until in self.offer_hints.items()],
                "global_complete": False, "mathematical_acceptance": False}

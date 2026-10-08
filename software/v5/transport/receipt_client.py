"""One original acquisition/verification budget, no index or custody authority.

The owner creates the deadline and budget before work, preallocating earlier
location/search costs with charge_external. No remote configuration or automatic
retry exists. Same-process trusted owner assumptions match ReceiptVerifier.
"""
from copy import deepcopy
import math
import time

from discovery import formal_features as F
from admission.verifier import ReceiptVerifier
from custody.module_store import ModuleStore
from custody.receipt_store import ReceiptStore, MAX_RECEIPT, profile_id, receipt_digest, verify_offer, blob_request
from .clients import AcquisitionClient, configured
from .http_provider_receipts import exchange, RECEIPT_OFFER_ROUTE, RECEIPT_ROUTE, HEADER_MAX, REQUEST_MAX

LIMITS = {"requests": (1, 8192), "reply_bytes": (1024, 1024**3), "verify_attempts": (1, 4096),
          "verification_input_bytes": (1, 1024**3), "worker_cpu_seconds": (1, 86400)}


def deadline_checked(deadline):
    F.need(type(deadline) in (int, float) and math.isfinite(deadline)
           and time.monotonic() < deadline <= time.monotonic()+3600, "RECEIPT_ORIGINAL_DEADLINE")
    return deadline


class AcquisitionBudget:
    def __init__(self, deadline, limits):
        F.fields(limits, LIMITS)
        for key, bounds in LIMITS.items(): F.uint(limits[key], *bounds, "RECEIPT_WORKFLOW_LIMIT:"+key)
        self.deadline = deadline_checked(deadline); self.limits = dict(limits)
        self.used = {key: 0 for key in limits}; self.pending = None; self.sequence = 0
        self.external = []; self.closed = False

    def active(self):
        F.need(not self.closed and time.monotonic() < self.deadline, "RECEIPT_WORKFLOW_CLOSED_OR_EXPIRED")

    def charge_external(self, label, requests, reply_bytes):
        """Prepay a finite search/location suballocation BEFORE dispatching it.

        This does not invent evidence for earlier work; only trusted owner code
        can compose the matching external phase. No unused allowance is refunded.
        """
        self.active(); F.need(self.pending is None and self.sequence == 0, "RECEIPT_PREALLOCATION_PHASE")
        F.need(type(label) is str and 0 < len(label) <= 64 and len(self.external) < 8, "RECEIPT_EXTERNAL_LABEL")
        F.need(label not in [row["label"] for row in self.external], "RECEIPT_EXTERNAL_DUPLICATE")
        F.uint(requests, 0, self.limits["requests"]); F.uint(reply_bytes, 0, self.limits["reply_bytes"])
        F.need(self.used["requests"]+requests <= self.limits["requests"]
               and self.used["reply_bytes"]+reply_bytes <= self.limits["reply_bytes"], "RECEIPT_AGGREGATE_BUDGET")
        self.used["requests"] += requests; self.used["reply_bytes"] += reply_bytes
        self.external.append({"label": label, "requests": requests, "reply_bytes": reply_bytes})

    def begin(self, maximum):
        self.active(); F.uint(maximum, 1, MAX_RECEIPT)
        F.need(self.pending is None and self.used["requests"] < self.limits["requests"]
               and self.used["reply_bytes"]+maximum <= self.limits["reply_bytes"], "RECEIPT_AGGREGATE_BUDGET")
        self.used["requests"] += 1; self.sequence += 1
        self.pending = (self.sequence, maximum); return self.sequence

    def settle(self, ticket, count=None):
        F.need(self.pending is not None and self.pending[0] == ticket, "RECEIPT_PRIVATE_TICKET")
        maximum = self.pending[1]
        if count is None: count = maximum
        F.uint(count, 0, maximum, "RECEIPT_SETTLEMENT_BYTES")
        self.used["reply_bytes"] += count; self.pending = None

    def verification(self, count, cpu):
        self.active(); F.need(self.pending is None, "RECEIPT_NETWORK_PENDING")
        F.uint(count, 1, MAX_RECEIPT); F.uint(cpu, 1, 600)
        changes = {"verify_attempts": 1, "verification_input_bytes": count, "worker_cpu_seconds": cpu}
        F.need(all(self.used[key]+value <= self.limits[key] for key, value in changes.items()), "RECEIPT_VERIFY_BUDGET")
        for key, value in changes.items(): self.used[key] += value

    def remaining_ms(self):
        self.active(); value = int((self.deadline-time.monotonic())*1000)
        F.need(value > 0, "RECEIPT_WORKFLOW_CLOSED_OR_EXPIRED"); return min(60000, value)

    def report(self):
        return {"limits": dict(self.limits), "used": dict(self.used),
                "reserved_reply_bytes": 0 if self.pending is None else self.pending[1],
                "pending_requests": int(self.pending is not None), "external_prepaid": deepcopy(self.external),
                "remaining_ms": max(0, int((self.deadline-time.monotonic())*1000)),
                "closed": self.closed, "mathematical_acceptance": False}


class DeadlineReceiptVerifier(ReceiptVerifier):
    """Owner-created adopted verifier with the exact original outer deadline.

    The inherited minting/check/evidence rules are unchanged. Constructor ABI
    compatibility is an owner's adoption assertion, not downloaded authority.
    """
    def __init__(self, *, deadline, wire_profile, **adoption):
        selected = deadline_checked(deadline); wire_id = profile_id(wire_profile)
        F.need(adoption.get("image_id") == wire_profile["image"]
               and adoption.get("foundation") == wire_profile["foundation"]
               and adoption.get("policy") == wire_profile["policy"], "RECEIPT_LOCAL_ADOPTION_PROFILE")
        self.outer_deadline = selected
        super().__init__(**adoption)
        self._deadline = min(self._deadline, selected)
        self.wire_profile_id = wire_id
        self._active()

    def _active(self):
        # The base constructor calls this during adoption hashing too. Set the
        # outer deadline BEFORE super(), not only after that work has finished.
        F.need(time.monotonic() < self.outer_deadline, "RECEIPT_ORIGINAL_DEADLINE")
        super()._active()


class _SharedAcquisition(AcquisitionClient):
    def __init__(self, adapter, endpoints, budget):
        self.budget = budget; self.request_body_upper_bound = 0; self.header_upper_bound = 0
        super().__init__(adapter, endpoints, requests=budget.limits["requests"], bytes=budget.limits["reply_bytes"],
                         wall_ms=max(1, int((budget.deadline-time.monotonic())*1000)))
        # A public deadline on the unchanged acquisition client; never later
        # than the ORIGINAL owner deadline even after constructing the client.
        self.deadline = min(self.deadline, budget.deadline)

    async def _get(self, provider, route, request, maximum):
        ticket = self.budget.begin(maximum); before = self.used_bytes
        # The frozen client does not expose request-body outcomes. Bound them
        # conservatively for every attempt; do not call this actual wire cost.
        self.request_body_upper_bound += REQUEST_MAX
        self.header_upper_bound += 2*HEADER_MAX
        try: return await super()._get(provider, route, request, maximum)
        finally:
            # Even predial refusal is a consumed outer attempt. Unknown lower
            # outcomes conservatively charge the complete selected allowance.
            difference = self.used_bytes-before
            self.budget.settle(ticket, difference if difference > 0 else None)

    def report(self):
        return {**super().report(), "request_body_upper_bound": self.request_body_upper_bound,
                "header_upper_bound": self.header_upper_bound}


class ReceiptAcquisition:
    """Read-only remote acquisition into separate local structural stores.

    Supply owner-approved endpoints; a missing custody role consumes/refuses its
    attempt. No dynamic referrals, source execution or verifier configuration.
    """
    def __init__(self, adapter, endpoints, profile, budget, module_custody, receipt_custody, *, verifier=None):
        F.need(type(budget) is AcquisitionBudget, "RECEIPT_OWNER_BUDGET")
        budget.active(); self.budget = budget
        self.profile = deepcopy(profile); self.profile_id = profile_id(profile)
        F.need(type(module_custody) is ModuleStore and type(receipt_custody) is ReceiptStore,
               "RECEIPT_OWNER_CUSTODY")
        F.need(module_custody.foundation == profile["foundation"] and module_custody.policy == profile["policy"]
               and receipt_custody.profile_id == self.profile_id, "RECEIPT_CUSTODY_PROFILE")
        F.need(adapter.foundation == profile["foundation"] and adapter.policy == profile["policy"], "RECEIPT_ADAPTER_PROFILE")
        if verifier is not None:
            F.need(type(verifier) is DeadlineReceiptVerifier and verifier.wire_profile_id == self.profile_id
                   and verifier.outer_deadline == budget.deadline, "RECEIPT_EXACT_OWNER_VERIFIER")
        self.verifier = verifier; self.modules = module_custody; self.receipts = receipt_custody
        self.endpoints = configured(endpoints)
        self.structural = _SharedAcquisition(adapter, self.endpoints, budget)
        self.adapter = adapter
        self.http = {"completed_requests": 0, "failed_requests": 0, "request_bytes": 0,
                     "reply_bytes": 0, "header_bytes": 0, "unknown_header_upper_bound": 0,
                     "unknown_request_body_upper_bound": 0}

    async def _get(self, provider, route, request, maximum):
        F.need(provider in self.endpoints, "ENDPOINT_NOT_CONFIGURED")
        ticket = self.budget.begin(maximum); charged = None; measured = False
        try:
            response = await exchange(self.endpoints[provider], route, request, maximum, self.budget.remaining_ms())
            charged = len(response["raw"]); measured = True
            self.http["completed_requests"] += 1
            for key in ("request_bytes", "reply_bytes", "header_bytes"): self.http[key] += response[key]
            F.need(response["status"] == 200, "RECEIPT_HTTP_ERROR")
            self.budget.active(); return response["raw"]
        except BaseException:
            self.http["failed_requests"] += 1
            if not measured:
                self.http["unknown_header_upper_bound"] += 2*HEADER_MAX
                self.http["unknown_request_body_upper_bound"] += REQUEST_MAX
            raise
        finally: self.budget.settle(ticket, charged)

    async def export(self, provider, record):
        resolved = await self.structural.export(provider, record)
        loc = resolved["locator"]; self.budget.active()
        self.modules.put_group(loc["module_id"], resolved["opening"], before_commit=self.budget.active)
        held, unused = self.modules.get_group(loc["module_id"], loc["relative_name"], loc["group_index"])
        F.need(held == resolved["opening"], "RECEIPT_GROUP_COMMIT_READBACK")
        self.budget.active(); return resolved

    async def body(self, provider, resolved, digest, maximum):
        result = await self.structural.body(provider, resolved, digest, maximum)
        loc = resolved["locator"]; response = result["body"]
        self.modules.put_body(loc["module_id"], loc["relative_name"], response, before_commit=self.budget.active)
        held = self.modules.get_body(loc["module_id"], loc["relative_name"], response["universes"], digest)
        F.need(held == response, "RECEIPT_BODY_COMMIT_READBACK")
        self.budget.active(); return result

    async def offers(self, provider, module, *, max_offers=4, max_bytes=4096):
        request = {"module_id": F.hexid(module), "wire_profile_id": self.profile_id,
                   "max_offers": max_offers, "max_bytes": max_bytes}
        raw = await self._get(provider, RECEIPT_OFFER_ROUTE, request, max_bytes)
        value = F.strict(raw, max_bytes); F.need(F.compact(value) == raw, "RECEIPT_OFFER_CANONICAL")
        value = verify_offer(value, request); self.budget.active(); return value

    async def receipt(self, provider, module, entry):
        F.hexid(module); blob_request(entry)
        raw = await self._get(provider, RECEIPT_ROUTE, entry, entry["receipt_bytes"])
        F.need(len(raw) == entry["receipt_bytes"] and receipt_digest(raw) == entry["receipt_sha256"], "RECEIPT_BLOB_BINDING")
        self.receipts.put(module, raw, before_commit=self.budget.active)
        F.need(self.receipts.get(entry["receipt_sha256"], entry["receipt_bytes"]) == raw, "RECEIPT_COMMIT_READBACK")
        self.budget.active()
        return {**deepcopy(entry), "module_id": module, "wire_profile_id": self.profile_id,
                "assurance": "EXACT_OPAQUE_RECEIPT_BYTES_CUSTODIED", "mathematical_acceptance": False}

    def custody_ready(self, resolved, entry, demanded_bodies=()):
        """Selected components only. Separate DB commits are NOT atomic together."""
        self.budget.active(); blob_request(entry)
        loc = resolved["locator"]; module, name = loc["module_id"], loc["relative_name"]
        opening, descriptor = self.modules.get_group(module, name, loc["group_index"])
        F.need(opening == resolved["opening"] and descriptor == resolved["descriptor"], "RECEIPT_SELECTED_GROUP_BINDING")
        F.need(type(demanded_bodies) in (tuple, list) and len(demanded_bodies) <= 16384, "RECEIPT_DEMANDED_BODY_SET")
        for digest in demanded_bodies: F.hexid(digest)
        F.need(len(set(demanded_bodies)) == len(demanded_bodies), "RECEIPT_DEMANDED_BODY_SET")
        for digest in demanded_bodies:
            self.modules.get_body(module, name, descriptor["universes"], F.hexid(digest))
        self.receipts.get(entry["receipt_sha256"], entry["receipt_bytes"])
        self.budget.active()
        return {"status": "SELECTED_COMPONENTS_DURABLY_READ_BACK", "module_id": module,
                "receipt_sha256": entry["receipt_sha256"], "demanded_bodies": list(demanded_bodies),
                "cross_database_atomic": False, "all_future_bodies_covered": False, "mathematical_acceptance": False}

    def admit(self, resolved, entry, operation_directory, *, demanded_bodies=(), cpu_seconds=30,
              wall_seconds=60, memory_mib=1024):
        F.need(type(self.verifier) is DeadlineReceiptVerifier, "RECEIPT_REAL_OWNER_VERIFIER_REQUIRED")
        self.custody_ready(resolved, entry, demanded_bodies)
        raw = self.receipts.get(entry["receipt_sha256"], entry["receipt_bytes"])
        self.budget.verification(len(raw), cpu_seconds)
        handle = None
        try:
            handle = self.verifier.receive(raw, resolved["opening"]["summary"], operation_directory,
                cpu_seconds=cpu_seconds, wall_seconds=wall_seconds, memory_mib=memory_mib)
            group = self.verifier.open_group(handle, resolved["opening"])
            retained = self.custody_ready(resolved, entry, demanded_bodies)
            self.budget.active()
            return {"handle": handle, "group": group, "custody": retained,
                    "assurance": "LIVE_LOCALLY_VERIFIED_MODULE_WITH_SELECTED_COMPONENT_CUSTODY"}
        except BaseException:
            # Do not let a minted handle survive a failed final custody/deadline
            # check. Conservatively revoke this owner's verifier instance.
            if handle is not None: self.verifier.close()
            raise

    def report(self):
        return {"budget": self.budget.report(), "receipt_http": dict(self.http),
                "structural_http": self.structural.report(), "wire_profile_id": self.profile_id,
                "mathematical_acceptance": False}

    def close(self):
        F.need(self.budget.pending is None, "RECEIPT_CLOSE_DURING_REQUEST")
        self.budget.closed = True
        if self.verifier is not None: self.verifier.close()

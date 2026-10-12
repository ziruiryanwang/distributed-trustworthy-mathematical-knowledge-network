"""Mixed proof form over the unchanged profile-addressed packet HTTP protocol.

No new routing/search protocol, budget, retry or mathematical checker. Reused
methods operate on opaque bytes or structural semantic openings. See the seam
decision for the explicit inherited-method audit and separate real A gate.
"""
from copy import deepcopy
import math
import time

from custody.module_store import ModuleStore
from delta import transport as D
from discovery import formal_features as F
from mixed_claims.receiver import MixedDeltaVerifier
from transport.clients import configured
from transport.receipt_client import AcquisitionBudget, _SharedAcquisition
from .custody import PacketStore, PROOF_FORM, profile_id, verify_offer

OFFER_ROUTE, PACKET_ROUTE, ROUTES = D.OFFER_ROUTE, D.PACKET_ROUTE, D.ROUTES
MixedLocatedHandoff = D.DeltaLocatedHandoff


class CompositeProvider(D.CompositeProvider):
    def __init__(self, *, index, custody, packets, **limits):
        F.need(index is not None and type(custody) is ModuleStore and type(packets) is PacketStore,
               "MIXED_COMPOSITE_ACTUAL_ROLES")
        F.need(index.adapter.foundation == custody.foundation == packets.profile["foundation"]
               and index.adapter.policy == custody.policy == packets.profile["policy"],
               "MIXED_COMPOSITE_PROFILE")
        self.packets = packets
        D.H.Provider.__init__(self, index=index, custody=custody, **limits)


class MixedAcquisition(D.DeltaAcquisition):
    """Same original grants; only a locally adopted mixed verifier grants authority.

    Inherit from_search/_active/_get/export/body/packet/custody_ready/close. All
    type/profile-specific construction, offer and admission gates are overridden.
    The one-shot handoff is deliberately the exact existing handoff, not a copy.
    """
    def __init__(self, adapter, endpoints, profile, budget, module_custody, packet_custody, *, verifier=None):
        F.need(type(budget) is AcquisitionBudget, "MIXED_ACQUISITION_EXACT_BUDGET")
        budget.active(); self.budget = budget
        self.profile = deepcopy(profile); self.profile_id = profile_id(profile)
        F.need(type(module_custody) is ModuleStore and type(packet_custody) is PacketStore,
               "MIXED_ACQUISITION_ACTUAL_CUSTODY")
        F.need(adapter.foundation == module_custody.foundation == profile["foundation"]
               and adapter.policy == module_custody.policy == profile["policy"]
               and packet_custody.profile_id == self.profile_id, "MIXED_ACQUISITION_PROFILE")
        if verifier is not None:
            F.need(type(verifier) is MixedDeltaVerifier
                   and (verifier._image, verifier._aggregate_image, verifier._foundation, verifier._policy)
                   == (profile["relation_image"], profile["aggregate_image"], profile["foundation"], profile["policy"]),
                   "MIXED_ACQUISITION_REAL_OWNER_VERIFIER")
            verifier._active()
        self.adapter, self.modules, self.packets = adapter, module_custody, packet_custody
        self.verifier = verifier; self.endpoints = configured(endpoints)
        self._origin_verifier = verifier
        self._origin_deadline = budget.deadline
        self._search = self._handoff = None; self._offers = set(); self.closed = False
        self.structural = _SharedAcquisition(adapter, self.endpoints, budget)
        self.http = {"completed_requests": 0, "failed_requests": 0, "request_bytes": 0,
                     "reply_bytes": 0, "header_bytes": 0, "unknown_header_upper_bound": 0,
                     "unknown_request_body_upper_bound": 0}

    async def export(self, provider, record):
        result = await super().export(provider, record)
        return {**result, "next_gate": "ACTUAL_COMPLETE_MIXED_RECEIVE_BEFORE_MATHEMATICAL_USE"}

    async def offers(self, provider, module, *, max_offers=4, max_bytes=4096):
        request = {"module_id": F.hexid(module), "wire_profile_id": self.profile_id,
                   "max_offers": max_offers, "max_bytes": max_bytes}
        raw = await self._get(provider, OFFER_ROUTE, request, max_bytes)
        value = F.strict(raw, max_bytes); F.need(F.compact(value) == raw, "MIXED_OFFER_CANONICAL")
        result = verify_offer(value, request)
        for row in result["packets"]:
            self._offers.add((provider, module, row["packet_sha256"], row["packet_bytes"]))
        self._active(); return result

    async def packet(self, provider, module, entry):
        result = await super().packet(provider, module, entry)
        return {**result, "assurance": "EXACT_UNTRUSTED_MIXED_PACKET_CUSTODIED"}

    def admit(self, resolved, entry, *, demanded_bodies=(), native_cpu_seconds=30,
              receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024):
        self._active()
        F.need(type(self.verifier) is MixedDeltaVerifier, "MIXED_REAL_OWNER_VERIFIER_REQUIRED")
        F.uint(native_cpu_seconds, 1, 600); F.uint(receipt_cpu_seconds, 1, 600)
        F.uint(wall_seconds, 1, 600); F.uint(memory_mib, 64, 4096)
        held = self.custody_ready(resolved, entry, demanded_bodies)
        raw = self.packets.get(entry["packet_sha256"], entry["packet_bytes"])
        census = held["census"]
        reserved = census["claims"]*receipt_cpu_seconds+census["deltas"]*native_cpu_seconds
        # Keep the existing <=600 CPU per admission suballocation. This matches
        # the receiver's per-claim (not per selected member) reservation.
        self.budget.verification(len(raw), reserved)
        remaining = min(wall_seconds, math.floor(self.budget.deadline-time.monotonic()))
        F.need(remaining >= 1, "MIXED_ACQUISITION_VERIFY_DEADLINE")
        handle = None
        try:
            handle = self.verifier.receive(raw, resolved["opening"]["summary"],
                native_cpu_seconds=native_cpu_seconds, receipt_cpu_seconds=receipt_cpu_seconds,
                wall_seconds=remaining, memory_mib=memory_mib)
            group = self.verifier.open_group(handle, resolved["opening"])
            retained = self.custody_ready(resolved, entry, demanded_bodies)
            self._active()
            # Structural readback can outlive the mathematical owner's lifetime.
            # Revalidate the exact handle's live warrant closure at promotion.
            self.verifier.describe(handle)
            self._active()
            return {"handle": handle, "group": group, "custody": retained,
                    "assurance": "LIVE_LOCALLY_CHECKED_MIXED_DELTA_WITH_SELECTED_COMPONENT_CUSTODY"}
        except BaseException:
            if handle is not None: self.verifier.close()
            raise

    def report(self):
        return {**super().report(), "proof_form": PROOF_FORM}

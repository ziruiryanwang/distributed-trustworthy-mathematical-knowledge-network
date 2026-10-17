"""Explicit I-only custody/acquisition over unchanged mixed packet transport.

No new proof protocol or checker. The exact live mixed verifier is configured
with a genuine I owner and no A owner. Inherited methods conserve the original
query/acquisition grant and retain fail-stop authority lifetimes.
"""
from copy import deepcopy

from admission.verifier import ReceiptVerifier
from custody.module_store import ModuleStore
from delta import transport as D
from discovery import formal_features as F
from mixed_claims.receiver import MixedDeltaVerifier
from mixed_network import transport as M
from transport.clients import configured
from transport.receipt_client import AcquisitionBudget, _SharedAcquisition
from .custody import PacketStore, PROOF_FORM, profile_id, verify_offer

OFFER_ROUTE, PACKET_ROUTE, ROUTES = D.OFFER_ROUTE, D.PACKET_ROUTE, D.ROUTES
FrontierLocatedHandoff = D.DeltaLocatedHandoff


class CompositeProvider(D.CompositeProvider):
    """Only construction is profile-specific; inherited dispatch calls this store."""
    def __init__(self, *, index, custody, packets, **limits):
        F.need(index is not None and type(custody) is ModuleStore and type(packets) is PacketStore,
               "I_FRONTIER_COMPOSITE_ACTUAL_ROLES")
        F.need(profile_id(packets.profile) == packets.profile_id
               and index.adapter.foundation == custody.foundation == packets.profile["foundation"]
               and index.adapter.policy == custody.policy == packets.profile["policy"],
               "I_FRONTIER_COMPOSITE_PROFILE")
        self.packets = packets
        D.H.Provider.__init__(self, index=index, custody=custody, **limits)


class FrontierAcquisition(M.MixedAcquisition):
    """One exact I-only wire profile; underlying mathematics stays mixed-native.

    Inherit mixed admit/export/packet and legacy opaque from_search, _active,
    _get, body, custody_ready, close. Override every lexical profile/offer/report
    boundary. The handoff remains the same concrete one-shot class, not a copy.
    """
    def __init__(self, adapter, endpoints, profile, budget, module_custody, packet_custody, *, verifier=None):
        F.need(type(budget) is AcquisitionBudget, "I_FRONTIER_ACQUISITION_EXACT_BUDGET")
        budget.active(); self.budget = budget
        self.profile = deepcopy(profile); self.profile_id = profile_id(profile)
        F.need(type(module_custody) is ModuleStore and type(packet_custody) is PacketStore,
               "I_FRONTIER_ACQUISITION_ACTUAL_CUSTODY")
        F.need(adapter.foundation == module_custody.foundation == profile["foundation"]
               and adapter.policy == module_custody.policy == profile["policy"]
               and profile_id(packet_custody.profile) == packet_custody.profile_id == self.profile_id,
               "I_FRONTIER_ACQUISITION_PROFILE")
        if verifier is not None:
            F.need(type(verifier) is MixedDeltaVerifier
                   and (verifier._image, verifier._aggregate_image, verifier._foundation, verifier._policy)
                   == (profile["relation_image"], None, profile["foundation"], profile["policy"])
                   and type(verifier._owners[0]) is ReceiptVerifier and verifier._owners[1] is None,
                   "I_FRONTIER_ACQUISITION_REAL_OWNER_VERIFIER")
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

    async def offers(self, provider, module, *, max_offers=4, max_bytes=4096):
        request = {"module_id": F.hexid(module), "wire_profile_id": self.profile_id,
                   "max_offers": max_offers, "max_bytes": max_bytes}
        raw = await self._get(provider, OFFER_ROUTE, request, max_bytes)
        value = F.strict(raw, max_bytes)
        F.need(F.compact(value) == raw, "I_FRONTIER_OFFER_CANONICAL")
        result = verify_offer(value, request)
        for row in result["packets"]:
            self._offers.add((provider, module, row["packet_sha256"], row["packet_bytes"]))
        self._active(); return result

    def report(self):
        return {**super().report(), "proof_form": PROOF_FORM,
                "supported_claim_tags": [0], "aggregate_image": None}

"""Closed profile-selected transport under one existing search/acquisition grant.

No issuer, callback, native call or verification reservation is accepted here.
The ordinary client owns every mathematical admission and exact live warrant.
"""
from copy import deepcopy

from custody.module_store import ModuleStore
from delta import transport as D
from discovery import formal_features as F
from transport.clients import configured
from transport.receipt_client import AcquisitionBudget, _SharedAcquisition
from .custody import PacketStore, profile_id, verify_offer

OFFER_ROUTE, PACKET_ROUTE, ROUTES = D.OFFER_ROUTE, D.PACKET_ROUTE, D.ROUTES
EvidenceLocatedHandoff = D.DeltaLocatedHandoff


class CompositeProvider(D.CompositeProvider):
    def __init__(self, *, index, custody, packets, **limits):
        F.need(index is not None and type(custody) is ModuleStore and type(packets) is PacketStore,
               "EVIDENCE_COMPOSITE_ACTUAL_ROLES")
        F.need(profile_id(packets.profile) == packets.profile_id
               and index.adapter.foundation == custody.foundation == packets.profile["foundation"]
               and index.adapter.policy == custody.policy == packets.profile["policy"],
               "EVIDENCE_COMPOSITE_PROFILE")
        self.packets = packets
        D.H.Provider.__init__(self, index=index, custody=custody, **limits)


class EvidenceAcquisition(D.DeltaAcquisition):
    """Structural custody only; one generation of an original shared budget."""
    def __init__(self, adapter, endpoints, profile, budget, module_custody, packet_custody, *, verifier=None):
        F.need(verifier is None, "EVIDENCE_ACQUISITION_HAS_NO_VERIFIER")
        F.need(type(budget) is AcquisitionBudget, "EVIDENCE_ACQUISITION_EXACT_BUDGET")
        budget.active(); self.budget = budget
        self.profile = deepcopy(profile); self.profile_id = profile_id(profile)
        F.need(type(module_custody) is ModuleStore and type(packet_custody) is PacketStore,
               "EVIDENCE_ACQUISITION_ACTUAL_CUSTODY")
        F.need(adapter.foundation == module_custody.foundation == profile["foundation"]
               and adapter.policy == module_custody.policy == profile["policy"]
               and packet_custody.profile_id == self.profile_id
               and profile_id(packet_custody.profile) == self.profile_id, "EVIDENCE_ACQUISITION_PROFILE")
        self.adapter, self.modules, self.packets = adapter, module_custody, packet_custody
        self.verifier = self._origin_verifier = None
        self.endpoints = configured(endpoints); self._origin_deadline = budget.deadline
        self._search = self._handoff = None; self._offers = set(); self.closed = False
        self.structural = _SharedAcquisition(adapter, self.endpoints, budget)
        self.http = {"completed_requests": 0, "failed_requests": 0, "request_bytes": 0,
                     "reply_bytes": 0, "header_bytes": 0, "unknown_header_upper_bound": 0,
                     "unknown_request_body_upper_bound": 0}

    async def export(self, provider, record):
        result = await super().export(provider, record)
        return {**result, "next_gate": "ACTUAL_PUBLIC_CLIENT_EVIDENCE_ADMISSION_BEFORE_MATHEMATICAL_USE"}

    async def declaration(self, provider, module, relative_name, max_bytes):
        """Real same-contact demand resolution, not an invented index candidate."""
        self._active()
        result = await self.structural.declaration(provider, module, relative_name, max_bytes)
        loc = result["locator"]
        self.modules.put_group(loc["module_id"], result["opening"], before_commit=self._active)
        opening, descriptor = self.modules.get_group(loc["module_id"], loc["relative_name"], loc["group_index"])
        F.need(opening == result["opening"] and descriptor == result["descriptor"],
               "EVIDENCE_DECLARATION_COMMIT_READBACK")
        self._active()
        return {**result, "candidate_origin": "EXPLICIT_SAME_CONTACT_DECLARATION_DEMAND_NOT_INDEX_SEARCH",
                "next_gate": "ACTUAL_PUBLIC_CLIENT_EVIDENCE_ADMISSION_BEFORE_MATHEMATICAL_USE"}

    async def offers(self, provider, module, *, max_offers=4, max_bytes=4096):
        request = {"module_id": F.hexid(module), "wire_profile_id": self.profile_id,
                   "max_offers": max_offers, "max_bytes": max_bytes}
        raw = await self._get(provider, OFFER_ROUTE, request, max_bytes)
        value = F.strict(raw, max_bytes); F.need(F.compact(value) == raw, "EVIDENCE_OFFER_CANONICAL")
        result = verify_offer(value, request, profile=self.profile)
        for row in result["packets"]:
            self._offers.add((provider, module, row["packet_sha256"], row["packet_bytes"]))
        self._active(); return result

    async def packet(self, provider, module, entry):
        """Acquire an actual offer; this API retains the offer prerequisite."""
        return await self._packet(provider, module, entry, offered=True)

    async def packet_exact(self, provider, module, entry):
        """Acquire a known digest AND size without inventing an offer."""
        return await self._packet(provider, module, entry, offered=False)

    async def _packet(self, provider, module, entry, *, offered):
        self._active(); F.hexid(module); D.blob_request(entry)
        # Strict scalar fields are copied before the first await. Caller mutation
        # cannot change the charged identity, readback or returned description.
        entry = dict(entry)
        F.need(type(self.modules) is ModuleStore and type(self.packets) is PacketStore,
               "EVIDENCE_ACQUISITION_ACTUAL_CUSTODY")
        F.need(profile_id(self.profile) == self.profile_id == self.packets.profile_id
               and profile_id(self.packets.profile) == self.profile_id
               and self.adapter.foundation == self.modules.foundation == self.profile["foundation"]
               and self.adapter.policy == self.modules.policy == self.profile["policy"],
               "EVIDENCE_ACQUISITION_PROFILE")
        F.need(entry["packet_bytes"] <= self.packets.limits["packet_bytes"]
               and entry["packet_bytes"] <= self.packets.envelope.packet_bytes,
               "EVIDENCE_ACQUISITION_PACKET_CAP")
        if offered:
            F.need((provider, module, entry["packet_sha256"], entry["packet_bytes"]) in self._offers,
                   "DELTA_PACKET_NOT_OFFERED_BY_SELECTED_PROVIDER")
        raw = await self._get(provider, PACKET_ROUTE, entry, entry["packet_bytes"])
        F.need(len(raw) == entry["packet_bytes"] and D.packet_digest(raw) == entry["packet_sha256"],
               "DELTA_PACKET_HASH_BINDING")
        self.packets.put(module, raw, before_commit=self._active)
        F.need(self.packets.get(entry["packet_sha256"], entry["packet_bytes"]) == raw,
               "DELTA_PACKET_COMMIT_READBACK")
        self._active()
        return {**entry, "module_id": module, "wire_profile_id": self.profile_id,
                "assurance": "EXACT_UNTRUSTED_TYPED_EVIDENCE_CUSTODIED", "mathematical_acceptance": False}

    def admit(self, *args, **kwargs):
        raise ValueError("PUBLIC_CLIENT_ADMISSION_REQUIRED")

    def retire_generation(self):
        """Tombstone a quiescent structural scope without closing shared authority.

        The serialized caller retires the matching search session and candidate
        scope. Custodied bytes, issuer owners and the original budget survive.
        Captured endpoint objects still reject through their original binding.
        """
        if self.closed: return
        F.need(self.budget.pending is None and self.structural.inflight == 0
               and self.structural.reserved_bytes == 0, "EVIDENCE_ACQUISITION_PENDING")
        self.closed = True
        self._offers.clear()
        self.structural.deadline = 0
        self.structural.endpoints.clear()
        self.endpoints.clear()

    def close(self):
        # A retired generation must never close a successor's shared budget,
        # including while that successor has a pending request.
        if self.closed: return
        # This structural object never owns an issuer, including an object
        # assigned later to its verifier attribute. Do not invoke one on close.
        F.need(self.budget.pending is None and self.structural.inflight == 0, "EVIDENCE_ACQUISITION_PENDING")
        self.closed = True; self.budget.closed = True

    def report(self):
        return {**super().report(), "proof_form": self.profile["proof_form"],
                "admission": "STRUCTURAL_ONLY_NO_VERIFIER_OR_VERIFICATION_RESERVATION"}

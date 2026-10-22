"""Closed profile-selected transport under one existing search/acquisition grant.

No issuer, callback, native call or verification reservation is accepted here.
The ordinary client owns every mathematical admission and exact live warrant.
"""
import asyncio
from copy import deepcopy
from dataclasses import asdict
import json
import math
import ssl
import time

from aggregate_claims import bindings as B
from custody.module_store import ModuleStore
from delta import transport as D
from delta.packet import DeltaError
from discovery import formal_features as F
from modules import codec as C
from transport.clients import configured
from transport.receipt_client import AcquisitionBudget, _SharedAcquisition
from .custody import PacketStore, profile_id, verify_offer
from . import packet as P
from .packet import inspect_evidence

OFFER_ROUTE, PACKET_ROUTE, ROUTES = D.OFFER_ROUTE, D.PACKET_ROUTE, D.ROUTES
EvidenceLocatedHandoff = D.DeltaLocatedHandoff


class PacketCleanupError(RuntimeError):
    """The new trial transfer did not establish socket closure; never recover."""


def _parser_policy_failure(error):
    """Only reviewed parser failures, including their exact decode causes.

    The frozen codec wraps RecursionError. Do not mistake that runtime limit
    for a declared grammar bound, or suppress an unexpected exception chain.
    """
    if type(error) not in (C.StructureError, DeltaError):
        raise error
    allowed = (C.StructureError, DeltaError, json.JSONDecodeError,
               UnicodeDecodeError, UnicodeEncodeError, ValueError)
    current, seen = error, set()
    while current is not None:
        if id(current) in seen or len(seen) >= 16 or type(current) not in allowed:
            raise error
        seen.add(id(current))
        cause, context = current.__cause__, current.__context__
        if cause is not None and context is not None and cause is not context:
            raise error
        current = cause if cause is not None else context


def preflight_packet(raw, entry, summary, *, envelope, aggregate_image,
                     terminal_receipt_bytes, terminal_i):
    """Pure peer-byte triage; caller charges before entry. Never grants authority.

    Trusted argument/configuration checks lie outside the only recoverable
    catch. Unknown schemas/profile incompatibility are policy-relative refusal,
    not a claim that the packet is well-formed or its mathematics is false.
    """
    F.need(inspect_evidence is P.inspect_evidence, "PACKET_PREFLIGHT_PARSER_SYMBOL")
    D.blob_request(entry); entry = dict(entry)
    C.validate_summary(summary); module = C.summary_id(summary)
    P.validate_limits(envelope, terminal_receipt_bytes); B._adopted_image(aggregate_image)
    F.need(type(terminal_i) is bool and entry["packet_bytes"] <= envelope.packet_bytes,
           "PACKET_PREFLIGHT_TRUSTED_POLICY")
    F.need(type(raw) is bytes and len(raw) <= envelope.packet_bytes,
           "PACKET_PREFLIGHT_BOUNDED_IMMUTABLE_INPUT")
    received = D.packet_digest(raw) if raw else None
    def rejected(reason):
        return {"status": "CANDIDATE_REJECTED_UNDER_SELECTED_POLICY", "reason": reason,
                "module": module, "selection": dict(entry),
                "received_sha256": received, "received_bytes": len(raw),
                "authority": "LOCAL_CANDIDATE_PREFLIGHT_NOT_MATHEMATICAL_ACCEPTANCE",
                "mathematical_acceptance": False}
    if len(raw) != entry["packet_bytes"] or received != entry["packet_sha256"]:
        return rejected("PACKET_IDENTITY_MISMATCH")
    try:
        kind, target, exact, census = inspect_evidence(raw, envelope,
            aggregate_image=aggregate_image, terminal_receipt_bytes=terminal_receipt_bytes,
            terminal_i=terminal_i)
    except (C.StructureError, DeltaError) as error:
        _parser_policy_failure(error)
        return rejected("PACKET_STRUCTURE_OR_SELECTED_POLICY")
    if target != summary or C.summary_id(target) != module:
        return rejected("SELECTED_TARGET_MISMATCH")
    return {"status": "CANDIDATE_PREFLIGHT_PASSED", "evidence_kind": kind,
            "summary": target, "journal": exact, "census": census,
            "mathematical_acceptance": False}


async def _exchange_packet_settled(endpoint, entry, *, timeout_ms, deadline):
    """Existing packet framing, but return only after successful bounded close."""
    endpoint.validate(); D.blob_request(entry)
    F.uint(timeout_ms, 1, 60000)
    F.need(type(deadline) in (int, float) and math.isfinite(deadline)
           and time.monotonic() < deadline, "PACKET_TRIAL_ORIGINAL_DEADLINE")
    raw = F.compact(entry)
    F.need(0 < len(raw) <= D.H.REQUEST_MAX, "DELTA_HTTP_REQUEST_BYTES")
    host = "["+endpoint.host+"]" if ":" in endpoint.host else endpoint.host
    head = D.H._header("POST "+PACKET_ROUTE+" HTTP/1.1", len(raw), host+":"+str(endpoint.port))
    context = None
    if endpoint.tls:
        context = ssl.create_default_context(cafile=endpoint.ca_file)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
    writer = response = None; started = time.monotonic()
    try:
        async with asyncio.timeout_at(min(deadline, started+timeout_ms/1000)):
            kwargs = {"ssl": context, "limit": D.H.HEADER_MAX}
            if endpoint.tls:
                kwargs.update(server_hostname=endpoint.server_name or endpoint.host,
                              ssl_handshake_timeout=timeout_ms/1000, ssl_shutdown_timeout=1)
            reader, writer = await asyncio.open_connection(endpoint.host, endpoint.port, **kwargs)
            await D.H._write(writer, head); await D.H._write(writer, raw)
            first, headers, count, incoming = await D.H._headers(reader, "application/octet-stream")
            F.need(count == entry["packet_bytes"], "DELTA_HTTP_EXACT_CONTENT_LENGTH")
            parts = first.split(" ")
            F.need(len(parts) >= 3 and parts[0] == "HTTP/1.1"
                   and parts[1] in ("200", "400", "404", "503"), "DELTA_HTTP_STATUS")
            F.need("host" not in headers and count <= entry["packet_bytes"], "DELTA_HTTP_RESPONSE_BOUND")
            body = await D.H._body(reader, count)
            F.need(await reader.read(1) == b"", "DELTA_HTTP_TRAILING_RESPONSE")
            response = {"status": int(parts[1]), "raw": body, "request_bytes": len(raw),
                        "reply_bytes": len(body), "header_bytes": len(head)+incoming}
    finally:
        if writer is not None:
            try:
                writer.close()
                async with asyncio.timeout_at(min(deadline, time.monotonic()+1)):
                    await writer.wait_closed()
            except asyncio.CancelledError:
                raise
            except Exception as error:
                raise PacketCleanupError("PACKET_SOCKET_CLOSURE_UNCERTAIN") from error
    F.need(time.monotonic() < deadline, "PACKET_TRIAL_ORIGINAL_DEADLINE")
    F.need(type(response) is dict, "PACKET_TRIAL_EXCHANGE_OUTCOME")
    response["elapsed_ms"] = int((time.monotonic()-started)*1000)
    return response


def _packet_trial_unchanged(bound):
    # Local import avoids AR's EvidenceAcquisition construction-time cycle.
    from transport import acquisition_resilience as R
    R._unchanged(bound)
    a, b, s = bound["acquisition"], bound["budget"], bound["structural"]
    F.need(a.profile == bound["packet_profile"] and profile_id(a.profile) == a.profile_id
           == bound["packet_profile_id"] == a.packets.profile_id
           and a.packets.profile == bound["packet_profile"]
           and a.packets.envelope is bound["packet_envelope"]
           and asdict(a.packets.envelope) == bound["packet_envelope_state"]
           and a.packets.limits == bound["packet_limits"]
           and a.packets.terminal_receipt_bytes == bound["terminal_receipt_bytes"]
           and a.adapter.foundation == a.modules.foundation == a.profile["foundation"]
           and a.adapter.policy == a.modules.policy == a.profile["policy"],
           "PACKET_TRIAL_PROFILE_OR_LIMITS_CHANGED")
    F.need(type(a.packets) is PacketStore and type(a.modules) is ModuleStore
           and a.http is bound["packet_http"]
           and b.pending is None and s.inflight == 0 and s.reserved_bytes == 0,
           "PACKET_TRIAL_SETTLED_ORIGINAL_OWNER")


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

    async def _trial_packet_bytes(self, provider, module, entry, *, offered):
        """One settled raw-byte transfer, no custody/parser/admission mutation."""
        from transport import acquisition_resilience as R
        self._active(); F.hexid(module); D.blob_request(entry)
        F.need(type(offered) is bool, "PACKET_TRIAL_OFFER_MODE")
        entry = dict(entry)
        bound = R._binding(self, provider)
        bound.update(packet_profile=deepcopy(self.profile), packet_profile_id=self.profile_id,
            packet_envelope=self.packets.envelope, packet_limits=dict(self.packets.limits),
            packet_envelope_state=asdict(self.packets.envelope), packet_http=self.http,
            terminal_receipt_bytes=self.packets.terminal_receipt_bytes)
        _packet_trial_unchanged(bound)
        P.validate_limits(bound["packet_envelope"], bound["terminal_receipt_bytes"])
        F.need(entry["packet_bytes"] <= bound["packet_limits"]["packet_bytes"]
               and entry["packet_bytes"] <= bound["packet_envelope"].packet_bytes,
               "EVIDENCE_ACQUISITION_PACKET_CAP")
        if offered:
            F.need((provider, module, entry["packet_sha256"], entry["packet_bytes"]) in self._offers,
                   "DELTA_PACKET_NOT_OFFERED_BY_SELECTED_PROVIDER")
        budget = bound["budget"]
        ticket = budget.begin(entry["packet_bytes"]); charged = None; measured = False
        try:
            response = await _exchange_packet_settled(bound["contact"], entry,
                timeout_ms=budget.remaining_ms(), deadline=bound["deadline"])
            charged = len(response["raw"]); measured = True
            self.http["completed_requests"] += 1
            for key in ("request_bytes", "reply_bytes", "header_bytes"): self.http[key] += response[key]
            F.need(response["status"] == 200, "DELTA_HTTP_ERROR")
            self._active()
        except BaseException:
            self.http["failed_requests"] += 1
            if not measured:
                self.http["unknown_header_upper_bound"] += 2*D.H.HEADER_MAX
                self.http["unknown_request_body_upper_bound"] += D.H.REQUEST_MAX
            raise
        finally:
            budget.settle(ticket, charged)
        _packet_trial_unchanged(bound)
        return response["raw"], bound

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

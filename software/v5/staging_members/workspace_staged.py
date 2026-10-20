"""Bounded structural acquisition before unchanged mathematical admission.

Staged tokens name held data, never mathematical warrants. Provider freshness
still gates every dial. Local admission needs the original grant, reader and
owners, but does not dial or renew a provider contact. Used predecessors stay
unchanged; select this successor in the actual owners' source maps.
"""
from copy import deepcopy
from pathlib import Path

from aggregate_claims import bindings as B
from custody.module_store import permitted_hashes
from delta_claims.claims import expected_journal
from discovery import formal_features as F
from mixed_claims import packet as MP
from modules import codec as C
from transport import semantic_staging as S
from . import workspace_resilient as R
from .workspace_atomic import OperationGrant, _action, _async_action, _sha


class StagedEvidence:
    """Opaque same-client data locator; no receipt/import/authoring authority."""
    __slots__ = ()


def _member_inventory(raw, kind, exact, *, envelope, aggregate_image, max_members):
    """Parsed data only; kind/exact come from the existing evidence inspection."""
    if kind == "terminal":
        journals = [exact]
    else:
        F.need(kind == "mixed", "CLIENT_STAGING_MEMBER_EVIDENCE_KIND")
        unused, frontiers, witnesses, unused_census = MP.parse_packet(
            raw, envelope, aggregate_image=aggregate_image)
        journals = [item[1] for item in frontiers]
        journals.extend(expected_journal(summary, rank, B.RELATION_IMAGE)
                        for unused_raw, unused_parents, summary, rank in witnesses)
    F.need(0 < len(journals) <= max_members and len(set(journals)) == len(journals)
           and exact in journals, "CLIENT_STAGING_MEMBER_INVENTORY_LIMIT")
    return [{"module": parsed["module"], "journal": list(value), "summary": parsed["summary"]}
            for value in sorted(journals) for parsed in [B.member_journal(value)]]


def _select_member_rows(snapshots, selected_members, max_members):
    """Explicit token-bound subset for structural preview, never live warrants."""
    F.need(type(selected_members) is list and 0 < len(selected_members)
           <= min(S.MAX_STAGED, max_members), "CLIENT_STAGING_SELECTED_MEMBER_LIST")
    selected, seen = [], set()
    for row in selected_members:
        F.fields(row, ("token", "module", "journal"))
        F.need(type(row["token"]) is StagedEvidence and row["token"] in snapshots
               and type(row["journal"]) is bytes and len(row["journal"]) == 184,
               "CLIENT_STAGING_SELECTED_MEMBER_TOKEN")
        C.digest_string(row["module"])
        snapshot = snapshots[row["token"]]
        member = next((value for value in snapshot["members"]
                       if value["module"] == row["module"]
                       and bytes(value["journal"]) == row["journal"]), None)
        F.need(member is not None and row["module"] not in seen,
               "CLIENT_STAGING_SELECTED_MEMBER_SUBSET_OR_VARIANT")
        seen.add(row["module"])
        selected.append({**member, **{key: snapshot["selection"][key]
            for key in ("packet_sha256", "packet_bytes")}})
    return selected


class Workspace(R.Workspace):
    def operation(self, grant, *, aggregate_owner, delta_owner, receipt_owner=None,
                  preparation_owner=None, foundation_bytes, foundation_sha256):
        self._active(); self._grant_active(grant)
        F.need(not self._poisoned and self._client is None,
               "CLIENT_OPERATION_ACTIVE_OR_UNCERTAIN")
        F.need(type(grant) is OperationGrant and grant in self._grants
               and grant._workspace is self and not grant._used,
               "CLIENT_EXACT_UNUSED_GRANT")
        client = CommonsClient(self, grant, receipt_owner, aggregate_owner, delta_owner,
                               preparation_owner, foundation_bytes, foundation_sha256)
        self._record(grant.identifier, "OPEN")
        grant._used = True; self._client = client
        return client


class CommonsClient(R.CommonsClient):
    def __init__(self, workspace, grant, receipt, aggregate, delta, preparation,
                 foundation, foundation_sha):
        # Base construction calls the census/report methods. No authority is
        # installed in these maps, including during failed construction.
        self._staged = {}
        self._staging_counts = {key: 0 for key in
                               ("packets_staged", "admission_transitions", "previews")}
        super().__init__(workspace, grant, receipt, aggregate, delta, preparation,
                         foundation, foundation_sha)
        root = Path(__file__).resolve().parents[1]
        extra = {"client.workspace_staged": root/"client/workspace_staged.py",
                 "transport.semantic_staging": root/"transport/semantic_staging.py"}
        pins = {path: pin for owner in (receipt, aggregate, delta) if owner is not None
                for path, pin in owner._pins.items()}
        F.need(set(extra.values()) <= set(pins), "CLIENT_STAGING_REQUIRED_SOURCE_PINS")
        self._required_origins.update(extra)
        self._source_pins.update({path: deepcopy(pins[path]) for path in extra.values()})
        self._active(); self._census()

    def _staging_census(self):
        return {"tokens": len(self._staged),
                "retained_metadata_bytes": sum(len(row[0]) for row in self._staged.values()),
                "unconsumed": sum(not row[1] for row in self._staged.values())}

    def _census(self):
        disk = super()._census(); staged = self._staging_census()
        caps = self.grant._limits["imports"]
        F.need(staged["tokens"] <= caps["max_sources"]
               and staged["retained_metadata_bytes"] <= caps["data_bytes"],
               "CLIENT_STAGING_RETAINED_LIMIT")
        return {**disk, "structural_staging": staged}

    def _stage(self, token, *, unused=False):
        F.need(type(token) is StagedEvidence and token in self._staged,
               "CLIENT_FOREIGN_STAGED_EVIDENCE")
        raw, consumed = self._staged[token]
        F.need(not unused or not consumed, "CLIENT_STAGED_ALREADY_CONSUMED")
        return C.parse_json(raw), consumed

    def _read_stage(self, token):
        snapshot, consumed = self._stage(token)
        selected, resolved = snapshot["selection"], snapshot["candidate"]
        loc = resolved["locator"]
        raw = self._store(self.workspace.packets.get,
                          selected["packet_sha256"], selected["packet_bytes"])
        self._charge(raw)
        kind, summary, exact, unused = self._inspect(raw)
        F.need(kind in ("terminal", "mixed") and _sha(raw) == selected["packet_sha256"]
               and len(raw) == selected["packet_bytes"] and list(exact) == selected["journal"]
               and summary == selected["summary"] == resolved["opening"]["summary"]
               and C.summary_id(summary) == selected["module"] == loc["module_id"],
               "CLIENT_STAGED_EXACT_PACKET_CHANGED")
        opening, descriptor = self._store(self.workspace.modules.get_group,
            loc["module_id"], loc["relative_name"], loc["group_index"])
        F.need(opening == resolved["opening"] and descriptor == resolved["descriptor"],
               "CLIENT_STAGED_GROUP_CHANGED")
        F.need(snapshot["members"] == self._structural_members(raw, kind, exact),
               "CLIENT_STAGED_MEMBER_INVENTORY_CHANGED")
        return snapshot, raw, consumed

    def _structural_members(self, raw, kind, exact):
        """Bounded parsed claim inventory, never admission or portable authority."""
        return _member_inventory(raw, kind, exact, envelope=self.workspace._envelope,
            aggregate_image=self._aggregate_image,
            max_members=self.grant._limits["imports"]["max_members"])

    @_async_action
    async def stage_packet(self, candidate, entry):
        """One offered transfer/readback, no verifier or verification reservation."""
        provider, resolved = self._candidate(candidate); loc = resolved["locator"]
        F.fields(entry, ("packet_sha256", "packet_bytes"))
        self._charge(C.canonical(entry))
        caps = self.grant._limits["imports"]
        F.need(len(self._staged) < caps["max_sources"], "CLIENT_STAGING_SOURCE_LIMIT")
        # Exact variant selection is explicit at the caller; no last-write-wins
        # choice between same-ModuleID journals or proof representations.
        F.need(all(C.parse_json(row[0])["selection"]["module"] != loc["module_id"]
                   for row in self._staged.values()), "CLIENT_STAGING_MODULE_ALREADY_SELECTED")
        F.need((provider, loc["module_id"], entry["packet_sha256"], entry["packet_bytes"])
               in self._acquisition._offers, "CLIENT_UNOFFERED_PACKET")
        await self._acquisition.packet(provider, loc["module_id"], entry)
        self._acquisition.custody_ready(resolved, entry, ())
        raw = self._store(self.workspace.packets.get, entry["packet_sha256"], entry["packet_bytes"])
        self._charge(raw)
        kind, summary, exact, unused = self._inspect(raw)
        F.need(kind in ("terminal", "mixed") and summary == resolved["opening"]["summary"]
               and C.summary_id(summary) == loc["module_id"], "CLIENT_STAGING_TARGET")
        selected = {"module": loc["module_id"], "journal": list(exact), "summary": summary,
                    "packet_sha256": entry["packet_sha256"], "packet_bytes": entry["packet_bytes"]}
        members = self._structural_members(raw, kind, exact)
        snapshot = C.canonical({"provider": provider, "candidate": resolved, "selection": selected,
                                "members": members})
        self._charge(snapshot)
        F.need(self._staging_census()["retained_metadata_bytes"]+len(snapshot) <= caps["data_bytes"],
               "CLIENT_STAGING_RETAINED_LIMIT")
        self._active()
        token = StagedEvidence(); self._staged[token] = snapshot, False
        self._staging_counts["packets_staged"] += 1
        return token

    @_action
    def describe_staged(self, token):
        snapshot, unused_raw, consumed = self._read_stage(token)
        return {"status": "STAGED_UNTRUSTED_EVIDENCE", **snapshot,
                "admission_consumed": consumed, "mathematical_acceptance": False}

    @_action
    def preview_context(self, staged_tokens, openings, bodies, *, limits=None, selected_members=None):
        """Data-only prediction. Real live import must repeat all trust checks."""
        F.need(type(staged_tokens) is list and 0 < len(staged_tokens)
               <= self.grant._limits["imports"]["max_sources"], "CLIENT_STAGING_TOKEN_LIST")
        F.need(len({id(token) for token in staged_tokens}) == len(staged_tokens),
               "CLIENT_STAGING_DUPLICATE_TOKEN")
        F.need(type(openings) is list and type(bodies) is list
               and len(openings) <= C.DEFAULT_LIMITS.max_groups
               and len(bodies) <= C.DEFAULT_LIMITS.max_declarations,
               "CLIENT_STAGING_DATA_LISTS")
        submitted = {"openings": openings, "bodies": bodies, "limits": limits}
        S._bounded_json(submitted, min(C.DEFAULT_LIMITS.max_bytes,
                                      self.grant._limits["imports"]["data_bytes"]))
        self._charge(C.canonical(submitted))
        selected, snapshots = [], {}
        for token in staged_tokens:
            # Preview predicts semantic closure, not present certificate validity
            # or availability. The immutable same-client data identity suffices;
            # full packet readback remains mandatory before/after admission.
            snapshot, unused_consumed = self._stage(token, unused=True)
            snapshots[token] = snapshot
            if selected_members is None:
                selected.append(snapshot["selection"])
        if selected_members is not None:
            selected = _select_member_rows(snapshots, selected_members,
                                          self.grant._limits["imports"]["max_members"])
        self._charge(C.canonical(selected))
        self._staging_counts["previews"] += 1
        # Reject structurally impossible/over-limit inputs before store loops.
        # This remains a private inert result until every held-data check passes.
        result = S.preview(selected, openings, bodies, self._foundation, self._foundation_sha, limits=limits)
        # Preview uses actual held structural bytes, not caller-asserted custody.
        body_names = {}
        for row in openings:
            F.fields(row, ("module", "opening"))
            group = C.verify_group_opening(row["module"], row["opening"])
            held, unused = self._store(self.workspace.modules.get_group,
                row["module"], group["declarations"][0]["name"], row["opening"]["index"])
            F.need(held == row["opening"], "CLIENT_STAGING_OPENING_NOT_HELD")
            for descriptor in group["declarations"]:
                for digest in permitted_hashes(descriptor):
                    body_names.setdefault((row["module"], descriptor["universes"], digest), descriptor["name"])
        for row in bodies:
            F.fields(row, ("module", "universes", "expression"))
            digest = C.body_id(row["expression"], row["universes"])
            key = row["module"], row["universes"], digest
            F.need(key in body_names, "CLIENT_STAGING_BODY_NOT_COMMITTED")
            held = self._store(self.workspace.modules.get_body, row["module"],
                              body_names[key], row["universes"], digest)
            F.need(held["expression"] == row["expression"], "CLIENT_STAGING_BODY_NOT_HELD")
        return result

    @_action
    def admit_staged(self, token, *, expected_exact_journal=None, native_cpu_seconds=30,
                     receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024):
        """Consume one local transition; exact unchanged owners establish trust."""
        for value in (native_cpu_seconds, receipt_cpu_seconds, wall_seconds): F.uint(value, 1, 600)
        F.uint(memory_mib, 64, 4096)
        self._stage(token, unused=True)
        frozen, unused = self._staged[token]
        self._staged[token] = frozen, True
        self._staging_counts["admission_transitions"] += 1
        snapshot, raw, unused = self._read_stage(token)
        selected, resolved = snapshot["selection"], snapshot["candidate"]
        exact = bytes(selected["journal"])
        self._expected(exact, expected_exact_journal)
        warrant = self._admit_evidence(raw, selected["summary"], exact, native_cpu_seconds,
            receipt_cpu_seconds, min(wall_seconds, self.grant.remaining_seconds()), memory_mib)
        kind, handle, unused_raw, live = self._warrant(warrant)
        F.need(kind in ("A-member", "mixed"), "CLIENT_EVIDENCE_WARRANT_KIND")
        owner = self.aggregate if kind == "A-member" else self.delta
        owner.open_group(handle, resolved["opening"])
        # Rebind local bytes after the real check, without calling any endpoint.
        final_snapshot, final_raw, unused = self._read_stage(token)
        unused_kind, unused_handle, unused_raw, final = self._warrant(warrant)
        F.need(final_snapshot == snapshot and final_raw == raw and final["journal"] == live["journal"] == exact
               and final["summary"] == selected["summary"] and final["module"] == selected["module"],
               "CLIENT_STAGED_FINAL_TARGET")
        return warrant

    def _fail(self, error):
        self._staged.clear()
        super()._fail(error)

    def report(self):
        return {**super().report(), "structural_staging": {
            **self._staging_census(), **self._staging_counts,
            "mathematical_acceptance": False, "no_contact_renewal": True}}

    async def close(self):
        # Do not revoke a running call's tokens merely because an invalid
        # concurrent close was attempted. Preserve the inherited refusal.
        F.need(not self._busy, "CLIENT_CANCEL_AND_AWAIT_ACTIVE_CALL_BEFORE_CLOSE")
        self._staged.clear()
        return await super().close()

"""Exact-address semantic dependencies under one existing owner workflow.

These calls are not discovery results and cannot add search candidates. A
selected module already has a live verified import; this adapter acquires only
additional committed group data. It mints no handle and fetches no proof body.
"""
from copy import deepcopy

from discovery import formal_features as F
from modules import codec as C
from transport.located_receipts import LocatedReceiptWorkflow
from transport.receipt_client import DeadlineReceiptVerifier, ReceiptAcquisition
from .imports import ImportSession


class DependencyAcquisition:
    """Single-owner companion; no new client, grant, deadline or close ownership.

    The caller serializes workflow/session/store access. A late refusal may
    leave structurally committed custody or a live selected group; these are
    separate local operations, not a cross-component atomic transaction.
    Copied output never transfers mathematical acceptance.
    """
    def __init__(self, workflow, session):
        F.need(type(workflow) is LocatedReceiptWorkflow
               and type(session) is ImportSession, "DEPENDENCY_EXACT_OWNER_TYPES")
        workflow._active("ACQUIRING"); session._active()
        F.need(type(workflow._acquisition) is ReceiptAcquisition
               and type(workflow._verifier) is DeadlineReceiptVerifier
               and workflow._verifier is session._verifier
               and workflow._acquisition.verifier is workflow._verifier,
               "DEPENDENCY_SAME_LIVE_VERIFIER")
        self._workflow, self._session = workflow, session
        self._acquisition = workflow._acquisition
        self._structural = self._acquisition.structural
        self._budget, self._store = workflow.budget, workflow._modules
        self._verifier = workflow._verifier
        self._active()

    def _active(self):
        w, s, a = self._workflow, self._session, self._acquisition
        w._active("ACQUIRING"); s._active()
        F.need(w._acquisition is a and a.structural is self._structural
               and w.budget is self._budget and a.budget is self._budget
               and self._structural.budget is self._budget
               and w._modules is self._store and a.modules is self._store
               and w._verifier is self._verifier and a.verifier is self._verifier
               and s._verifier is self._verifier,
               "DEPENDENCY_OWNER_BINDING_CHANGED")
        F.need(w.deadline == self._budget.deadline == self._verifier.outer_deadline
               and self._structural.deadline <= w.deadline
               and s._deadline <= w.deadline, "DEPENDENCY_ORIGINAL_DEADLINE")

    def _selected(self, module):
        self._active()
        # This re-describes the actual registered handle, including the exact
        # retained receipt/journal/summary; a stored flag is never consulted.
        return self._session._describe(module)

    async def declaration(self, provider, module, relative_name, max_bytes):
        """Acquire one needed group of an already selected verified module.

        No index hint or RecordID is required: this is an exact-address semantic
        dependency, not a promotion into the original search's candidate set.
        The retained structural client charges the shared ledger before dialing
        and checks the original deadline/contact TTL/owner egress at preflight.
        """
        C.digest_string(module); C.validate_name(relative_name)
        name = deepcopy(relative_name)  # Freeze the exact request address across await.
        F.uint(max_bytes, 1, 16*1024**2, "DEPENDENCY_GROUP_REPLY_LIMIT")
        selected = self._selected(module)
        # The retained public declaration helper computes discovery features.
        # Exact dependencies need no feature budget or candidate record. Keep
        # its actual canonical HTTP reader/guards/ledger, then check the group.
        opening = await self._structural._get(provider, "/v5/modules/group",
            {"module_id": module, "relative_name": name, "group_index": None}, max_bytes)
        self._selected(module)
        group = C.verify_group_opening(module, opening)
        F.need(opening["summary"] == selected["summary"], "DEPENDENCY_EXACT_SELECTED_SUMMARY")
        choices = [d for d in group["declarations"] if C.name_key(d["name"]) == C.name_key(name)]
        F.need(len(choices) == 1, "DEPENDENCY_EXACT_SELECTED_ADDRESS")
        descriptor = choices[0]
        loc = {"schema": "DMKN_MODULE_EXPORT_LOCATOR_V1", "module_id": module,
               "group_index": opening["index"], "relative_name": name,
               "descriptor_id": C.hash_value("declaration-descriptor", descriptor)}
        self._store.put_group(module, opening, before_commit=lambda: self._selected(module))
        held, actual = self._store.get_group(module, name, loc["group_index"])
        F.need(held == opening and actual == descriptor, "DEPENDENCY_GROUP_COMMIT_READBACK")
        self._selected(module)
        group = self._session.open_group(module, held)
        F.need(group == held["group"], "DEPENDENCY_LIVE_OPENING_BINDING")
        result = {"export_id": C.export_id(module, name), "locator": deepcopy(loc),
                "descriptor": deepcopy(descriptor), "opening": deepcopy(held),
                "assurance": "EXACT_GROUP_DURABLY_HELD_AND_OPENED_IN_LIVE_OWNER_SESSION",
                "discovery_candidate_promotion": False,
                "cross_component_atomic": False,
                "mathematical_acceptance": False}
        self._selected(module)
        return result

"""Acquire an unselected semantic owner without inventing a search candidate.

Only the existing real receipt-admission method may create trust. This companion
adds no transport, provider crawl, executable configuration or budget renewal.
The owner serializes access to all participating workflow/session/store objects.
"""
from copy import deepcopy

from discovery import formal_features as F
from modules import codec as C
from custody.receipt_store import blob_request
from .acquisition import DependencyAcquisition


class ModuleDependencyAcquisition:
    """One finite exact-address selection companion, owned by the live workflow.

    Structural custody is not atomic with admission/session selection. A late
    selection failure revokes ALL handles of the originating verifier, including
    earlier imports. Copies returned here are never portable acceptance tokens.
    There is no implicit retry; unavailable providers remain explicit failures.
    """
    def __init__(self, workflow, session, *, selections=8, data_bytes=16*1024**2):
        F.uint(selections, 1, 8, "MODULE_DEPENDENCY_SELECTION_LIMIT")
        F.uint(data_bytes, 1, 16*1024**2, "MODULE_DEPENDENCY_DATA_LIMIT")
        self._bridge = DependencyAcquisition(workflow, session)
        a = self._bridge._acquisition
        self._receipts, self._adapter = a.receipts, a.adapter
        self._profile = C.canonical(a.profile)
        self._profile_id = a.profile_id
        self._contacts = dict(a.endpoints)
        self._selection_cap, self._data_cap = selections, data_bytes
        self._selected, self._data_bytes = {}, 0
        self._active()

    def _active(self):
        b = self._bridge
        b._active()
        a, w = b._acquisition, b._workflow
        F.need(a.receipts is self._receipts and w._receipts is self._receipts
               and a.adapter is self._adapter and w.adapter is self._adapter
               and b._structural.adapter is self._adapter
               and a.profile_id == self._profile_id == self._receipts.profile_id
               == b._verifier.wire_profile_id
               and C.canonical(a.profile) == self._profile
               and C.canonical(w._profile) == self._profile,
               "MODULE_DEPENDENCY_OWNER_BINDING_CHANGED")
        for contacts in (a.endpoints, b._structural.endpoints):
            F.need(set(contacts) == set(self._contacts)
                   and all(contacts[k] is v for k, v in self._contacts.items()),
                   "MODULE_DEPENDENCY_CONTACTS_CHANGED")

    def _new(self, module):
        self._active()
        C.digest_string(module)
        F.need(module not in self._bridge._session._records,
               "MODULE_DEPENDENCY_ALREADY_SELECTED_USE_DECLARATION")

    async def prepare(self, provider, module, relative_name, max_bytes):
        """Hold one exact opening as UNTRUSTED custody, not a verified import.

        The caller may then use the existing workflow's receipt_offers/receipt
        calls. Nothing in this operation adds a discovery record or handle.
        """
        self._new(module)
        C.validate_name(relative_name)
        name = deepcopy(relative_name)
        key = module, C.name_key(name)
        F.uint(max_bytes, 1, 16*1024**2, "MODULE_DEPENDENCY_GROUP_REPLY_LIMIT")
        F.need(key in self._selected or len(self._selected) < self._selection_cap,
               "MODULE_DEPENDENCY_SELECTION_CAP")
        opening = await self._bridge._structural._get(provider, "/v5/modules/group",
            {"module_id": module, "relative_name": name, "group_index": None}, max_bytes)
        self._new(module)
        group = C.verify_group_opening(module, opening)
        summary = opening["summary"]
        F.need(summary["foundation"] == self._adapter.foundation
               and summary["policy"] == self._adapter.policy,
               "MODULE_DEPENDENCY_NAMESPACE")
        matches = [d for d in group["declarations"] if C.name_key(d["name"]) == key[1]]
        F.need(len(matches) == 1, "MODULE_DEPENDENCY_EXACT_ADDRESS")
        descriptor = matches[0]
        locator = {"schema": "DMKN_MODULE_EXPORT_LOCATOR_V1", "module_id": module,
                   "group_index": opening["index"], "relative_name": name,
                   "descriptor_id": C.hash_value("declaration-descriptor", descriptor)}
        resolved = {"export_id": C.export_id(module, name), "locator": locator,
                    "descriptor": descriptor, "opening": opening,
                    "assurance": "UNTRUSTED_EXACT_ADDRESS_GROUP_CUSTODY",
                    "discovery_candidate_promotion": False, "cross_component_atomic": False,
                    "mathematical_acceptance": False}
        raw = C.canonical(resolved)
        previous = self._selected.get(key)
        F.need(previous is None or previous == raw, "MODULE_DEPENDENCY_SELECTION_CONFLICT")
        F.need(self._data_bytes+(len(raw) if previous is None else 0) <= self._data_cap,
               "MODULE_DEPENDENCY_DATA_CAP")
        store = self._bridge._store
        store.put_group(module, opening, before_commit=lambda: self._new(module))
        held, actual = store.get_group(module, name, locator["group_index"])
        F.need(held == opening and actual == descriptor, "MODULE_DEPENDENCY_COMMIT_READBACK")
        self._new(module)
        if previous is None:
            self._selected[key] = raw
            self._data_bytes += len(raw)
        result = C.parse_json(raw)
        self._new(module)
        return result

    def admit(self, module, relative_name, entry, operation_directory, **limits):
        """Real same-budget admission, then selection in the same live session.

        The opening comes from this companion's immutable retained selection,
        not from a caller-returned mutable object. Exact receipt bytes are read
        back from the same custody store. Receipt offers never grant authority.
        """
        self._new(module)
        key = module, C.name_key(relative_name)
        F.need(key in self._selected, "MODULE_DEPENDENCY_NOT_PREPARED")
        selected = C.parse_json(self._selected[key])
        entry = deepcopy(entry)
        blob_request(entry)
        s = self._bridge._session
        opening_raw = C.canonical(selected["opening"])
        # Avoid predictable expensive admission followed by wholesale revocation.
        F.need(len(s._records) < s._max_modules
               and s._receipt_bytes+entry["receipt_bytes"] <= s._receipt_cap
               and s._calls+2 <= s._max_calls
               and len(s._groups) < C.DEFAULT_LIMITS.max_groups
               and s._data_bytes+len(opening_raw) <= s._data_cap,
               "MODULE_DEPENDENCY_IMPORT_CAPACITY")
        admitted = None
        try:
            admitted = self._bridge._acquisition.admit(selected, entry, operation_directory, **limits)
            self._new(module)
            raw = self._receipts.get(entry["receipt_sha256"], entry["receipt_bytes"])
            F.need(s.use_handle(admitted["handle"], raw) == module, "MODULE_DEPENDENCY_ADMITTED_MODULE")
            self._active()
            group = s.open_group(module, selected["opening"])
            F.need(group == selected["opening"]["group"], "MODULE_DEPENDENCY_LIVE_GROUP_BINDING")
            s._describe(module)
            result = {"module_id": module, "relative_name": deepcopy(relative_name),
                      "receipt_sha256": entry["receipt_sha256"],
                      "status": "SELECTED_IN_ORIGINATING_LIVE_IMPORT_SESSION",
                      "discovery_candidate_promotion": False, "cross_component_atomic": False,
                      "mathematical_acceptance": False}
            self._active()
            return result
        except BaseException:
            if admitted is not None:
                self._bridge._verifier.close()
            raise

    def report(self):
        self._active()
        return {"retained_selections": len(self._selected), "retained_data_bytes": self._data_bytes,
                "limits": {"selections": self._selection_cap, "data_bytes": self._data_cap},
                "new_budget_or_deadline": False, "mathematical_acceptance": False}

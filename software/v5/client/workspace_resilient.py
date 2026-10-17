"""Evidence client with bounded, explicitly settled index-provider refusals.

Storage, grants, issuers, admission and publication are inherited unchanged.
Only pre-accept search transport failures can return normally; no automatic
retry or fresh allowance is issued. Existing callers choose the next contact.
This successor must be selected in the same real owners' source pins.
"""
from copy import deepcopy
from pathlib import Path

from discovery import formal_features as F
from transport import search_resilience as R
from . import workspace_evidence as E
from .workspace_atomic import OperationGrant, _async_action


class Workspace(E.Workspace):
    """Same persisted evidence schema; explicit new operation implementation."""

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


class CommonsClient(E.CommonsClient):
    """Original owned lifetime; failed peer reads need not revoke live warrants."""

    def __init__(self, workspace, grant, receipt, aggregate, delta, preparation,
                 foundation, foundation_sha):
        super().__init__(workspace, grant, receipt, aggregate, delta, preparation,
                         foundation, foundation_sha)
        # Base construction has already established exact owners and its source
        # closure. Extend that closure before Workspace transfers ownership;
        # inherited _active checks every extra origin and owner pin thereafter.
        root = Path(__file__).resolve().parents[1]
        extra = {
            "client.workspace_resilient": root/"client/workspace_resilient.py",
            "transport.search_resilience": root/"transport/search_resilience.py",
        }
        pins = {path: pin for owner in (receipt, aggregate, delta) if owner is not None
                for path, pin in owner._pins.items()}
        F.need(set(extra.values()) <= set(pins), "CLIENT_RESILIENCE_REQUIRED_SOURCE_PINS")
        self._required_origins.update(extra)
        self._source_pins.update({path: deepcopy(pins[path]) for path in extra.values()})
        self._active(); self._census()

    @_async_action
    async def search_offer(self, provider, max_bytes=1048576, *,
                           max_expanded_bytes=1048576, max_age_ms=60000,
                           attempt_timeout_ms=5000):
        """One attempt, same grant. A settled refusal is not global absence."""
        F.need(self._search is not None, "CLIENT_SEARCH_NOT_READY")
        return await R.offer(self._search, provider, max_bytes,
                             max_expanded_bytes=max_expanded_bytes,
                             max_age_ms=max_age_ms, attempt_timeout_ms=attempt_timeout_ms)

    @_async_action
    async def search_page(self, provider, snapshot_id, partition, start, limits, *,
                          candidates_only=True, attempt_timeout_ms=5000):
        """No retry or coverage promotion when a peer attempt is refused."""
        F.need(self._search is not None and type(candidates_only) is bool,
               "CLIENT_SEARCH_NOT_READY")
        return await R.page(self._search, provider, snapshot_id, partition, start, limits,
                            candidates_only=candidates_only,
                            attempt_timeout_ms=attempt_timeout_ms)

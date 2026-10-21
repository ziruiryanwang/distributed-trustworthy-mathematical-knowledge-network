"""Staged client whose invalid index replies do not revoke mathematical state.

Only pure, pre-commit discovery validation can yield a metadata refusal. All
mathematical admission, storage, source checks, grant limits, and fail-stop
handling of unexpected or commit-time errors remain inherited and unchanged.
The caller chooses any next provider within the same finite original grant.
"""
from copy import deepcopy
from pathlib import Path

from discovery import formal_features as F
from transport import search_validation as V
from . import workspace_staged as S
from .workspace_atomic import OperationGrant, _async_action


class Workspace(S.Workspace):
    def operation(self, grant, *, aggregate_owner, delta_owner, receipt_owner=None,
                  preparation_owner=None, foundation_bytes, foundation_sha256):
        self._active(); self._grant_active(grant)
        F.need(not self._poisoned and self._client is None,
               "CLIENT_OPERATION_ACTIVE_OR_UNCERTAIN")
        F.need(type(grant) is OperationGrant and grant in self._grants
               and grant._workspace is self and not grant._used,
               "CLIENT_EXACT_UNUSED_GRANT")
        client = CommonsClient(self, grant, receipt_owner, aggregate_owner,
                               delta_owner, preparation_owner, foundation_bytes,
                               foundation_sha256)
        self._record(grant.identifier, "OPEN")
        grant._used = True; self._client = client
        return client


class CommonsClient(S.CommonsClient):
    def __init__(self, workspace, grant, receipt, aggregate, delta, preparation,
                 foundation, foundation_sha):
        # Parent construction dynamically calls _active/report. Initialize the
        # optional state first; legacy callers retain their old report shape.
        self._query_envelope = self._origin_query_envelope = None
        super().__init__(workspace, grant, receipt, aggregate, delta, preparation,
                         foundation, foundation_sha)
        root = Path(__file__).resolve().parents[1]
        extra = {
            "client.workspace_validated": root/"client/workspace_validated.py",
            "transport.search_validation": root/"transport/search_validation.py",
        }
        pins = {path: pin for owner in (receipt, aggregate, delta) if owner is not None
                for path, pin in owner._pins.items()}
        F.need(set(extra.values()) <= set(pins),
               "CLIENT_VALIDATION_REQUIRED_SOURCE_PINS")
        self._required_origins.update(extra)
        self._source_pins.update({path: deepcopy(pins[path]) for path in extra.values()})
        self._active(); self._census()

    def _active(self):
        super()._active()
        F.need(self._query_envelope is self._origin_query_envelope,
               "QUERY_ENVELOPE_ORIGIN_CHANGED")
        if self._origin_query_envelope is not None:
            self._origin_query_envelope.check(self)

    def _fail(self, error):
        # Tombstone direct search references even if next-query construction
        # failed before installing its acquisition. Original owner cleanup is
        # still mandatory if diagnostic capture itself unexpectedly fails.
        selected = self._origin_query_envelope
        try:
            if selected is not None: selected.terminal("FAILED")
        except BaseException as cleanup:
            self._failures.append("query_cleanup:"+type(cleanup).__name__)
        super()._fail(error)

    def report(self):
        result = super().report()
        if self._origin_query_envelope is not None:
            result["iterative_queries"] = self._origin_query_envelope.report()
        return result

    async def close(self):
        F.need(not self._busy, "CLIENT_CANCEL_AND_AWAIT_ACTIVE_CALL_BEFORE_CLOSE")
        if not self._closed and self._origin_query_envelope is not None:
            try:
                self._origin_query_envelope.terminal("CLOSED")
            except BaseException as cleanup:
                # Diagnostic capture must never strand transferred owners or
                # skip the original shared-budget close. Keep failure visible.
                self._failures.append("query_cleanup:"+type(cleanup).__name__)
                self._cleanup_uncertain = True
                self.workspace._poisoned = True
        return await super().close()

    @_async_action
    async def search_offer(self, provider, max_bytes=1048576, *,
                           max_expanded_bytes=1048576, max_age_ms=60000,
                           attempt_timeout_ms=5000):
        """Return a settled refusal for invalid metadata, never global absence."""
        F.need(self._search is not None, "CLIENT_SEARCH_NOT_READY")
        return await V.offer(self._search, provider, max_bytes,
                             max_expanded_bytes=max_expanded_bytes,
                             max_age_ms=max_age_ms,
                             attempt_timeout_ms=attempt_timeout_ms)

    @_async_action
    async def search_page(self, provider, snapshot_id, partition, start, limits, *,
                          candidates_only=True, attempt_timeout_ms=5000):
        """Reject before commit; success still uses unchanged authentication."""
        F.need(self._search is not None and type(candidates_only) is bool,
               "CLIENT_SEARCH_NOT_READY")
        return await V.page(self._search, provider, snapshot_id, partition, start,
                            limits, candidates_only=candidates_only,
                            attempt_timeout_ms=attempt_timeout_ms)


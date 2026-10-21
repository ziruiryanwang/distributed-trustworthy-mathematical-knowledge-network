# Continued context: source checkpoint

2026-10-21, core_release. Implements root's CONTINUING-CONTEXT-SELECTION;
source-only, no imports, compilation, controls or mathematical runtime run.

## Narrow change

Two fresh files under `software/v5/continuing_context` preserve the selected
predecessors and add exactly one method each:

- `client/workspace_atomic.py` adds decorated `advance_context(context, *,
  warrants, selected, openings, bodies)` immediately before `author`.
- `mixed_claims/imports_atomic.py` adds `begin_extension(view)` immediately before
  `view_context`.

The baseline atomic client is `conjunction_index/client/workspace_atomic.py`
(`eea95a6bb12349e5fc7b1e80bc610710ccafc7cbbfd2b40d705d80cdc67c8022`). The baseline
imports implementation is `standalone_validation/mixed_claims/imports_atomic.py`
(`8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595`). No old file
is modified, and no source rule/checker or receiver method is changed.

## Transition and authority argument

The existing `_action` wrapper charges and serializes the client call. The new
facade first calls `_live_context` and requires a READY view. It invokes the
same session's `begin_extension`, invalidates the old context wrapper, and
dispatches the pre-existing dynamic `_context_data` implementation. Validated
clients therefore retain their selected evidence/aggregate behavior.

`begin_extension` invokes existing `require_view`, which charges via `_begin`
and checks the original live owners, exact view identity and complete frozen
state. It refuses active batching. Only then does it clear the four sealed-view
fields. It changes no semantic/evidence map, counter, original deadline, owner,
limit, profile or definition policy. Exceptions close the session and re-raise;
the facade's existing fail-stop wrapper closes the enclosing client.

Existing `extend_context` is byte-for-byte unchanged and still refuses READY.
Existing materialization still checks immutable direct selection, conflicting
representations, exact committed groups/bodies and all finite capacities. It
issues a fresh view only on READY; NEED remains incomplete and extendable.

Every captured sealed `MixedSourceOperation` rechecks its exact view through
`_active` before prepare/finish and at final publication. The revoked identity
cannot match the replacement view. The new facade also removes the old
`AuthorContext` before any further context construction. Failure does not roll
back to old authority. This is a serialized local capability transition, not
concurrent snapshots or a new trust mode.

The API note is `software/v5/continuing_context/API.md`. Core growth independently
owns new transition controls; adaptive audit owns exact source/control review.
Root retains launch, adoption, installation and Git ownership. The matched
sharing pair remains unimplemented pending adoption of this necessary endpoint.

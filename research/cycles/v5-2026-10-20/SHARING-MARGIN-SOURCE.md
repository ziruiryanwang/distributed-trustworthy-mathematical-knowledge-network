# Sharing-margin source obstruction and central correction

2026-10-21, core_release. Source-only; no adapter, selector, product change,
runtime, mathematical admission, timing, installation copy or Git operation.

## Outcome

Do not run the proposed matched pair yet. The selected current client cannot
reach the local arm's stipulated endpoint within the same operation. This is
deterministic from source, not an uncertainty requiring an experiment.

The `232b0930` SHARING-MARGIN-NEXT decision correctly requires equal canonical
READY semantics and says to stop on an API obstruction. Its proposed
`READY(I) -> author(M) -> extend_context(I+M)` route is not implementable with
the current selected superclass. Preserve that note and the independent
`d9de7cd2` decision review as prior evidence, with this correction attached.

This finding concerns continued local mathematical work, not only a benchmark:
after making one accepted contribution, a local agent should be able to use it
alongside its prior imported mathematics without recreating its whole operation.
Fix that actual capability before measuring a sharing margin.

## Exact source resolution and proof of obstruction

The authoritative installed basis is
`experiments/v5-local-checks/distribution-terminal-i-01-input.json`, SHA-256
`d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0`.
Apply the already selected efficient imports and receiver overlays equally to
both arms. Relevant logical-to-physical resolutions are:

| Logical file | Physical source under `software/v5/` | SHA-256 |
|---|---|---|
| `client/workspace_atomic.py` | `conjunction_index/client/workspace_atomic.py` | `eea95a6bb12349e5fc7b1e80bc610710ccafc7cbbfd2b40d705d80cdc67c8022` |
| `client/workspace_evidence.py` | `terminal_i/client/workspace_evidence.py` | `8531ee14e24d60617491b9f00e14ea1f7c410a279d116322489fe763a421ea68` |
| `mixed_claims/imports_atomic.py` | `standalone_validation/mixed_claims/imports_atomic.py` | `8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595` |

The validated client inherits its actual `extend_context` from the selected
atomic superclass, not the older `software/v5/client/workspace.py` implementation.

1. `terminal_i/client/workspace_evidence.py:380` calls the session's
   `materialize`, saves its returned sealed view in `_selection_view`, and returns
   the local opaque context. `import_context` permits only one initial session.
2. `standalone_validation/mixed_claims/imports_atomic.py:477` documents its
   contract explicitly: READY seals; NEED remains extendable. On READY it creates
   a `SealedSelection`, sets `_sealed=True` and retains the exact sealed state
   and context payload (lines 548-572).
3. `conjunction_index/client/workspace_atomic.py:658` first validates the context,
   then requires `_selection_view is None` with `CLIENT_READY_CONTEXT_SEALED`.
   A READY context therefore cannot enter `_context_data` through extension.
4. Removing that client check alone is invalid: session `use_delta_handle`
   invokes `_mutable` (line 281), whose line 435 guard rejects a sealed session.
   The immutability checks protect the cached semantic context and must remain.
5. No selected public client operation reopens or replaces this session while
   retaining its original import counters and grant. `author` consumes the
   existing READY view; it does not unseal or replace it.

Hence the local endpoint is unreachable by the proposed calls, independently
of timing, RAM or proof validity. The sharing arm's one-shot initial import is
not subject to this obstruction. Charging L a second complete client startup
merely to manufacture comparability would handicap the baseline unnecessarily.

Adaptive audit independently confirms this exact selected-source chain and
acknowledges that its earlier favorable reading used the stale superclass.

## Recommended minimal product correction (not selected by this note)

Add an explicit same-operation `advance_context` operation for a READY context.
Keep `extend_context`'s current demand-completion behavior and sealed refusal.
Do not weaken acceptance, mutate a retained sealed token, or silently create a
fresh grant/session. Proposed fresh physical scope, subject to root selection:

- `software/v5/continuing_context/client/workspace_atomic.py`: exact selected
  atomic source plus one explicit facade operation.
- `software/v5/continuing_context/mixed_claims/imports_atomic.py`: exact selected
  efficient imports source plus one checked selection-generation transition.
- Narrow public documentation/control helpers in separately assigned paths.

The internal transition takes the exact current sealed view, validates its live
owners and frozen state, charges its call, revokes that view, and returns the
same session to mutable selection-building state. It retains all prior selected
mathematics, openings, bodies and evidence. Ordinary existing `_context_data`
then merges supplied live warrants and materializes the next selection; READY
creates a new opaque view and context. An incomplete next selection may return
NEED and use the existing `extend_context` route. No automatic demand search,
new proof, or external callback belongs in the transition.

All calls are synchronous under the existing client action serialization.
An in-flight public `author` cannot interleave with advancement. Any saved old
`MixedSourceOperation` remains bound to its old view and must fail subsequent
view checks, rather than seeing changed semantics under the same capability.

### Required invariants

Let a session state be `(O,D,L,U,K,Q,V)`: original owners, deadline, limits,
used counters, evidence/semantic maps, fixed definition policy, and current
view. Advancing a READY view must satisfy:

\[
O'=O,\qquad D'=D,\qquad L'=L,\qquad U'\ge U,\qquad Q'=Q.
\]

No verifier receives a new allocation, no receipt/native cache is reset, and no
existing source is dropped merely to reclaim capacity. Existing import rules
continue to enforce immutable direct selection, committed-body equality,
group-summary correspondence and explicit whole-journal representation choices.
`max_sources` must already accommodate both direct I and M in the original
caller grant; it is not enlarged during advancement.

- The old view is irrevocably invalid after transition. A new view is valid only
  after a complete fresh materialization over the now-selected semantics.
- Old context wrappers cannot authorize subsequent use, even if the new context
  happens to have equal serialized mathematics. Opaque identity is not restored.
- Wrong, stale, foreign, closed, expired, withdrawn or state-tampered views are
  refused before publication of new context authority.
- Any transition/import/materialization failure uses existing fail-stop cleanup;
  do not revive the prior view or refund consumed calls/bytes.
- Existing frontend theorem-ancestor-proof-byte and native acceptance boundaries
  remain unchanged. This is continued use of already live warrants, not a new
  transferable mathematical certificate.

### Minimum changed-boundary evidence

Source review should resolve the transition's live-check/charge/revocation order,
old capability invalidation and lifetime/resource preservation before controls.
One small focused native-free suite can test exact transition mechanics, stale
and wrong views, withdrawal/expiry, unchanged limits/counters, and failure closure.
No repeated old pin/import/native campaign is justified.

Then one actual same-client I-to-M advancement can be embedded in the originally
planned matched pair, after independent source/control adoption. L constructs M,
admits it, advances to I0/I10/M0; S acquires M and imports the same selected
semantic set. Both use the same successor implementation. This avoids a separate
costly circulation solely to prove the endpoint and avoids forcing S to perform
unused author construction. Compare canonical mathematics and READY/no-demands,
not source-owner IDs or opaque token identities.

## Preserved matched-measurement design

Once the endpoint exists, stage the current 114-file logical SDK with reviewed
overlays once; do not copy the 842 MB installation. Run serial L and S children
with the existing frozen supervisor `supervise` and Windows descendant Jobs.
Each arm includes its startup, all Lean/native/receipt descendants and cleanup;
S includes its real provider/index construction, local service and shutdown.
The driver/setup/tail remains charged by the outer Job and is disclosed
separately. Nested Job CPU must not be added again to the inclusive outer total.
Fixed per-arm allowances are sublimits of one original finite overall deadline;
neither failure nor an unused budget allows renewal.

Use existing author limits 45 CPU seconds / 90 wall seconds / 768 MiB and
admission 10 native + 10 receipt CPU seconds / 60 wall seconds / 512 MiB,
subject to root's complete enclosing allocation. No positive margin, discovery
benefit, scalable demand or certificate payback is presumed. No experiment is
currently selected by this checkpoint.

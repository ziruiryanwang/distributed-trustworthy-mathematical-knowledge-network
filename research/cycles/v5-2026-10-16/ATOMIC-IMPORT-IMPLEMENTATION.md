# Atomic import implementation checkpoint

2026-10-16, `memo_independent_review`. Implements root's
[ATOMIC-IMPORT-SELECTION](ATOMIC-IMPORT-SELECTION.md), not release acceptance.
Canonical guard PASS. Only the two new assigned source files and this note were
edited; no product/test execution, import, compilation, benchmark or Git change.

## Source identity and extraction

Both new files were first copied exactly from their frozen predecessors and
matched their full SHA-256 hashes before `apply_patch` changes. The predecessors
were rechecked unchanged afterward.

| File under `software/v5/mixed_claims/` | Bytes | SHA-256 |
|---|---:|---|
| `imports_atomic.py` | 41903 | `8d5e77ea1a239c10bd745a2860080d4ea6c91e52f4da32c7f18562ca755c0ba8` |
| `authoring_atomic.py` | 17988 | `22c2e758ce487f77e22f465ed5191f64928a423af4ea63efefed7a8888b086fe` |
| Preserved `imports.py` | — | `50b09b084b7cb54db2b1196e3570f1b15066e85e9ce55002b8d27bb4460cb1df` |
| Preserved `authoring.py` | — | `8b09cb1b8f0466a5049ed53f7b28098b6022234e3681786b2f4a9f542cd83e1b` |

The new imports module contains the single `_build_context` algorithm used by
both paths. A read-only whole-text comparison confirmed its body equals the
retained authoring context body after only replacing session basis/census with
data parameters and moving authority calls to wrappers. No mathematical closure,
body demand, reference traversal, ordering or canonical output logic was altered.
The eager pure foundation decoder remains named `_decode_foundation` for root's
explicit synthetic controls; `_decode_context_foundation` supplies a data-only
foundation view. There is no runtime import in the batch.

## Public integration signatures

```python
ready, view = session.materialize(
    batch_bytes, foundation_bytes, foundation_sha256, limits=None)
# batch fields: selected, openings, bodies; journals encoded as byte lists.

session.require_view(view)
ready_copy = session.view_context(view)
items, selection_binding = session.view_selection(view)

operation = MixedSourceOperation(
    session, foundation_bytes, foundation_sha256, source, roots,
    envelope=envelope, view=view)
```

`limits` is keyword-only and accepts only an exact dict of exact string keys and
integer values (or None). `view` is an identity-only `SealedSelection` token, with
no public authority fields. Context/items are stored as canonical immutable bytes
and decoded into detached returned values. The view belongs to one exact live
session, whose exact semantic state is retained as tuples of immutable entries.
Copied/foreign tokens fail identity checks; close clears token/payload/state.

## State and charging invariants

- Existing `use_*` imports establish live source authority before materializing.
  No receipt, source report or packet flag becomes a new admission credential.
- The batch is exact bounded canonical bytes. Its **full submitted byte count is
  charged once before parsing**, including malformed/canonical refusal. This is
  an explicit additional batch-submission charge versus the old incremental
  session's semantic-data-only accounting. Client submission and session quotas
  are nested constraints, not additive physical network-byte measurements.
- Selection/opening/body calls retain a charge per logical record. Two logical
  selection calls remain around context preparation. Semantic data quotas count
  new canonical openings/bodies as before; duplicate records still cost calls.
- Full `_live` runs at batch entry and exit. Between them only loaded controller
  code, immutable bytes, staged maps, pure semantic checks and cheap `_active`
  calls run. No process, await, filesystem access or external callback occurs.
- READY publishes complete state and a one-way seal only after all fallible
  exit/state/resource checks. NEED publishes validated incremental data but no
  view and stays extendable. Exceptions close the session/discard pending state;
  submitted/call counters are not rolled back.
- `_direct`, `use_delta_handle`, `_merge`, `select_warrant`, `open_group`,
  `supply_body` and another batch refuse sealed state. Internal commit points
  are guarded too. Read operations, liveness and resource counters still work.
- Full-state equality protects the view, not `representation_revision` alone.
  Sources, receipts, nodes, summaries, direct selections, groups, bodies and
  semantic byte count are captured; calls/submitted bytes are intentionally
  excluded because reads consume resources without changing mathematics.

## Later authoring does not restore the multiplier

On sealed sessions, `selected_data`, `selection`, `require_selection` and the
existing `onward_packet` use the view path, not per-group owner reopening.
`MixedSourceOperation(view=...)` reuses the exact cached context, checks exact
foundation bytes/pin, and refuses an alternative context-limits override. Its
`_active` performs one `require_view` plus immutable binding comparison; it does
not redundantly call `require_selection`. Preparation's native pre/post and final
authority/installation checks are unchanged. New child packets remain untrusted
until actual receiver admission.

The source-derived materialization count is two full session `_live` calls,
independent of opening/body count. View checks also have a fixed number of full
boundaries. Selected semantic traversal/copying still depends on selected bytes.
This is not an executed performance result or a predicted wall-time percentage.

## Source binding and review changes

The atomic import class requires its own new loaded/pinned origin (not the unused
old mixed imports module), plus the eagerly used foundation-decoder dependencies.
The preparation source allowlist includes both new atomic modules. Root controls
and launch selection must pin these exact new paths; the unchanged receiver's
original required source graph remains intact.

Initial independent review found and corrected the unused old loaded-origin
requirement, custom limits-iterator possibility, and absent submitted-batch charge.
Root also identified and removed a redundant constant-factor sealed-source check.
These were repaired before any execution; full independent review is pending.

There is deliberately no claim of equivalent detection of transient filesystem
mutate-and-restore events between old sampling points. The trusted serialized
controller/data boundary and fresh native/boundary checks are as specified in
[CLIENT-CONTROLLER-COST](CLIENT-CONTROLLER-COST.md).

Root owns workspace integration, focused structural controls, exact launch
selection and the later continuation using actual03's retained seed packet.
No seed reauthoring, repeated discovery, proof production or budget increase is
selected by this implementation checkpoint.

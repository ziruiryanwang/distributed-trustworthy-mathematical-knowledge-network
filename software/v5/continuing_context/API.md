# Continue a local mathematical investigation

This source successor adds one public operation: `client.advance_context`.
It does not change mathematical admission, introduce a new proof form, or make
serialized context data into authoring authority. It is not installed until a
release explicitly selects both continuing-context source files.

## Why it exists

Once an import context is READY, its view is sealed so an authoring operation
cannot silently see different mathematics. The existing `extend_context`
only supplies data while an import is incomplete; it deliberately rejects a
READY view. After authoring and genuinely admitting a new contribution, use
`advance_context` to make a new selection in the same finite operation.

```python
# `ready` belongs to this live client; `new_warrant` was genuinely admitted
# by it, not reconstructed from a saved result or supplied by another owner.
material = client.semantic_material(new_warrant)
description = client.describe(new_warrant)

next_ready = client.advance_context(
    ready["context"],
    warrants=[{"warrant": new_warrant, "resolutions": None}],
    selected=[bytes(description["live"]["journal"])],
    openings=chosen_new_openings,
    bodies=chosen_new_bodies,
)
```

Choose openings and bodies from the actual admitted material or exact committed
data already held locally. The row shapes are unchanged: openings have `module`
and `opening`; bodies have `module`, `universes` and `expression`. Do not blindly
import an entire packet or library when only a small part is useful.

`next_ready` has the existing `status`, `context`, `demands`, `cost` and
`mathematical_acceptance=False` fields. READY permits ordinary authoring with
its new context. NEED requires the exact missing data and the existing
`extend_context(next_ready["context"], ...)` route. Mathematical acceptance still
belongs to the live admitted warrants, not to a context-preparation status.

## Lifetime and resource contract

Advancement revokes the old context and its sealed view. Do not use `ready`
again, including after a failed advancement; misuse is fail-stop. Saved or
in-flight lower-level author operations bound to that old view cannot resume.
Public client calls are serialized, so public authoring and advancement do not
run concurrently.

The same session, verifier owners, mathematical caches, prior selected journals,
semantic data, used counters, limits, original deadline and definition mode are
retained. Nothing is reset or refunded. The original import allowance must have
space for the added evidence. This operation is additive: it is not a way to
remove old sources, reclaim capacity, replace an immutable direct journal choice,
or change `eager`/`interface-only` policy.

Where supplied evidence has a different representation of an existing exact
journal, the existing explicit `resolutions` contract still applies. No new
acceptance is inferred from a matching name, hash, prior publication or view.
Any guard, merge or materialization failure closes the operation under its
existing fail-stop rules; the prior view is not restored.

The internal `MixedImportSession.begin_extension(view)` is a local trusted-owner
transition, not a network or persistence API. It validates and charges the exact
live sealed view, revokes that view, and retains the original session state for
ordinary further materialization. It must never be used to revive closed or
withdrawn authority.

To compare two independently prepared contexts, compare their chosen exact
mathematical journals, openings, required bodies and definition mode. Opaque
token identity and the owner/source-bound `selection_binding` hash are not
mathematics-only equality tests.

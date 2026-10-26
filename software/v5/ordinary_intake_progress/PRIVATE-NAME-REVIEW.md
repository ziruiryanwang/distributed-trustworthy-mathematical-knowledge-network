# Independent review of the kernel-only compatibility proposal

Disposition: **PASS_IN_PRINCIPLE_FOR_SOURCE_IMPLEMENTATION** of the restricted
typed lane. This does not approve unreviewed code or select execution. Reviewer
performed source/data reads only: no implementation, native/owner/status call,
database API, test or Git mutation.

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Checkpoint: `research/cycles/v5-2026-10-26-local-discovery/CHECKPOINT.md`.
Reviewed proposal: PRIVATE-NAME-COMPATIBILITY.md, 12,922 bytes, SHA-256
`fe270247b1e417cd988262d24e430e8605e845feb54e5dfe02baf53a61dd4dbf`.

## Independent source finding

The inspected Lean 4.34 Environment.lean is SHA-256
`ee364e4788ce0560c87f621eeb3c4c3dfec62e8db4e15e099fd80e6adc533b86`.
Its checked Kernel.Environment.addDeclCore API (lines 293-298) is distinct from
addDeclWithoutChecking. The frontend Environment.addDeclCore (701-731) performs
checked insertion and then adds declarations to private/public AsyncConsts.
AsyncConsts.add (459-469) rejects collisions after privateToUserName removes
module-private prefixes. PrivateName.lean confirms that normalization. Exact
different declarations can therefore collide in this additional frontend index.

The observed native diagnostic is consistent with that source path. It does
not establish exact-name identity collision or mathematical invalidity. The
existing refusal on nonempty stderr remains correct and must stay in force.
The failed report/chunk cannot be adopted retrospectively.

The proposed dedicated lane uses a supported checked kernel API and retains
exact names. LocalSnapshot's existing serialization consumes actual generated
ConstantInfo records; OrdinaryWorkflowWorker.extend subsequently consumes only
the resulting chunk description. It does not need to reconstruct an elaborator
environment after checking. On later authenticated restoration, finalizeImport
(2334 onward) keys imported declarations by their complete names. The current
restore uses explicit protected artifacts, no plugins, loadExts=false and trust
level zero. Thus the normalized local-elaboration index is not part of the
mathematical persistence relation used by this native lane.

## Required invariant and argument

Let K0 be the caller's warranted exact-profile kernel environment. At every
iteration, Ki is the actual result of previous checked additions. The shared
loop must retain all current declaration-policy, reference-closure, exact-name
nonoverwrite, finite-resource, generated-row equality and generated-name census
checks. Its fixed native adapter must invoke checked Kernel.Environment.addDeclCore
and accept only its successful actual result.

Under the existing trusted-kernel contract, induction on units then preserves
the mathematical extension relation from K0 to the final kernel state. Expected
inventories remain claims compared with actual generated records; they never
install declarations. Final census and exact rows retain the same exclusions
of missing, extra, altered, unsafe, partial or axiomatic generated content.
Serialization must receive only those actual successful records through its
private caller path. Subsequent protected byte/lineage authentication and import
preserve their exact identities. No normalization, renaming, new axiom, skipped
check or authority-from-file is introduced.

This is an architectural argument conditional on the existing kernel/runtime
and protected-parent premises, not a new proof of the native kernel. quotInit
alone still cannot establish those premises. Private helpers organize trusted
code; they do not secure an otherwise hostile in-process caller.

## Boundaries that make the proposal acceptable

- Use one private policy loop and two fixed checked adapters. No peer input or
  public callback may select a checker or bypass policy. All existing checks
  stay shared and retain their order.
- Preserve the existing frontend checkBatch parameters, result type and actual
  Environment state for ordinary authoring/rebinding callers. The new lane
  returns Kernel.Environment and cannot accidentally satisfy a frontend API.
- Do not use Environment.ofKernelEnv to return the new state to elaboration.
  Lean's comment at 642-646 explicitly restricts that helper to temporary
  interpreter/exception contexts. Its equal public/private bases and discarded
  realization/asynchronous metadata make a blanket replacement inappropriate.
- Share private exact-record snapshot serialization, with a separately typed
  native entrypoint. Keep metadata/import/fresh-path/size policy unchanged.
  Only the protected worker's native extend route selects the kernel lane.
- Changed native/support bytes require a new implementation identity and exact
  integration adoption. Existing owners are not silently compatible with it.
  The separate integration assignment owns that concrete footprint.

Preserving the frontend API does not prove every future rich-library authoring
workflow is compatible. In particular, a caller that itself replays multi-origin
private declarations through the old frontend lane could still encounter the
same frontend restriction. The proposed change resolves native admission's
inappropriate dependency; broader warm authoring remains an explicit later gate.

## Small decision-changing qualification

The proposal's focused controls are appropriate: distinct exact private names
with the same normalized suffix, dependent declarations using both exact names,
exact duplicate-name refusal, wrong expected rows, an actually invalid proof,
and snapshot/restoration followed by another checked extension. Include a
public/private normalized pair if cheap. Inspect both fixed adapters and ensure
frontend callers continue using the original one. No need to repeat the large
failed intake or generate another deliberate panic to establish this boundary.

No unresolved conceptual blocker remains within these restrictions. The next
review must inspect the actual refactor and focused controls before any build
or runtime selection. No success, performance improvement or complete v5
readiness is inferred from this principle-level pass.

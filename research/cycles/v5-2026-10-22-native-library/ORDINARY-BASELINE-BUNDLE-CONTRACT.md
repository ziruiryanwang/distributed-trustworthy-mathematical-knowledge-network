# Strict baseline bundles: a minimal intake contract

2026-10-24. Source/theory-only proposal by `cold_intake_strategy`, incorporating
root's simplification and independent challenges from `module_anchor_audit`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
This note changes no source, installed package, owner state, assurance policy,
runtime allowance or Git selection. It is not implementation or v5 acceptance.

## Decision and actual workflow

Expose one bounded operation that independently checks an existing **inert
baseline bundle before authoring**. Its input is a finite exact manifest,
individually bounded evidence files, an explicitly selected already-warranted
local root and one finite invocation allowance. Its output is a new warranted
local root, or an honest partial/failed/uncertain outcome.

Use the existing 1,024-unit / 64-MiB admission core. Do not enlarge the small
retained-contribution completion command, rewrite retained requests, invent a
progress database, replay saved success reports, or require a new certificate.
The starting root may be **any eligible compatible protected context**. It need
not be the bundle's producer root, an earlier receiver root or a descendant of
an originally selected intake root. Exact portable imports already specify
their interpretations. Ordinary source candidates whose unclaimed names still
need binding are a different object and are outside this operation.

The practical workflow is:

1. Obtain or locally produce the exact inert bundle under a separate finite
   extraction/acquisition allowance.
2. Select the existing local owner and a protected context explicitly.
3. Preflight the entire bundle's syntax, identities, dependency feasibility and
   known resource requirements before the first native checking call.
4. Check only missing whole units in bounded dependency-complete batches,
   retaining each actually committed extension.
5. Separately connect the checked baseline to ordinary Lean, then author against
   that real baseline and use the existing small incremental workflow. This need
   not regenerate the entire baseline: candidate route A2 establishes exact
   correspondence to an approved existing local project and preserves its normal
   notation, instance/simp registries and tools. It would emit only unfamiliar
   deltas, while the mathematical receipt remains strict seed-derived acceptance.

Step 5 and the producer in step 1 are essential. A2 is under separate native and
independent review; artifact approval alone supplies no mathematical warrant or
correspondence. This intake contract alone is not a usable-library solution. See
[the next release decision](ORDINARY-NEXT-RELEASE-BOTTLENECK.md) and the separate
[strategy update](ORDINARY-BASELINE-STRATEGY-UPDATE.md); detailed correspondence
belongs to `ORDINARY-BASELINE-REALIZATION-CONTRACT.md`, not this intake note.

## What is reused, rather than redesigned

`ordinary_lean/ordinary_admission.py::_plan` already validates exact portable
evidence, complete group reuse, name/import identity conflicts, missing imports,
within-batch acyclicity, and node/name/edge limits. `admit` independently repeats
preflight against its **actual** protected parent; a `Preflight` object is never
authority. The actual checked worker and `PortableCatalog._commit_checked`
establish each new local warrant. `context` authenticates the protected lineage
and artifacts without re-proving every accepted theorem.

Existing ordinary owner `status` provides paginated root identifiers and an
optional exact `context_root` validation. Inventory identifiers are locators,
not warrants. Opening the owner can mark abandoned reservations interrupted;
this must not be advertised as a zero-write database operation.

The prior [cold-intake strategy](ORDINARY-COLD-INTAKE-STRATEGY.md) establishes the
conditional prefix argument and records actual 1,024 / 1,024 / 804-unit
admission of a 2,852-unit, 49,499,157-byte historical closure. Its combined
admission/recovery cost was 271.15625 known CPU seconds, including a failed
attempt. That evidence is sufficient to avoid another large batching experiment.
It does not establish this new public operation, ordinary realization, Mathlib
support or economic benefit.

## Portable input and local authorization

The proposed minimal manifest has exactly this conceptual shape; an
implementation selection must pin its canonical encoding and version before
use:

```text
schema
semantic_id
batches: [
  [ { unit_id, raw_sha256, raw_bytes }, ... ],
  ...
]
```

The caller supplies the exact manifest hash separately. Each unit is read only
from a derived `units/<unit_id>.json` filename below the explicitly selected
bundle directory. No arbitrary relative path, parent traversal, URL, archive
extraction, imported `.olean`, executable source or build script is an intake
input. Apply the existing ordinary-file/reparse/single-link checks and bounded
reads. Hashes identify bytes; they do not certify mathematics.

Unit IDs must be unique in this manifest. Every batch is nonempty. Each entry's
declared length, raw hash and domain-separated UnitID must equal the actual
canonical evidence. Imports, exports and declaration kinds come only from
parsing that evidence, not from a second manifest declaration inventory. The
manifest's semantics must equal the selected owner's supported semantics.

Targets are not required for mathematical intake: all listed units constitute
the requested finite baseline. A separate producer/realizer may identify selected
entrypoints and exact export IDs. Adding an entrypoint list must not permit
unchecked units or incomplete declaration groups to be accepted.

Local, nonportable arguments supply the owner/custody selection, starting root,
fresh operation-output/spool path and finite limits. Their envelope bounds at
least manifest bytes/depth/entries; total units, evidence bytes, encoded nodes,
names and import edges; batch and native-launch counts; spool/output/log storage;
controller/native CPU, wall time, memory and active processes. The caller cannot
use its own larger values to bypass installed ceilings. Select exact aggregate
profile ceilings from the producer/realizer census before implementation; this
note does not silently choose a larger existing installation profile.

Each batch stays within the **unchanged** core maxima:

| Quantity | Existing maximum per admission batch |
|---|---:|
| Whole units | 1,024 |
| Raw evidence bytes | 64 MiB |
| Encoded nodes | 2,097,152 |
| Exported names | 65,536 |
| Import edges | 1,048,576 |

Custody also has its existing 8-MiB individual evidence limit. A single
oversized or unsupported unit is refused, not split or replaced by axioms.
The 1,024-unit cap is not a promise that any 1,024 units fit the other bounds.

## Whole-bundle preflight without whole-proof residency

Let `K` be the context obtained by actually validating the selected protected
root. Set a **planning-only** binding projection `P0 = bindings(K)`. Read one
batch at a time, retaining only bounded planning metadata between batches.

For batch `j`:

1. Bound the entry count and claimed bytes before reading evidence; then parse
   the bounded bytes and recompute every identity and census.
2. Invoke the existing pure `_plan` rules against the projection consisting of
   `P(j-1)`, the selected semantics and a nonauthoritative parent label. Require
   `READY`. Reuse the existing within-batch topological order.
3. Add only the planned exact new outputs to `Pj`. Reject a conflicting output,
   partial existing group or any imported identity mismatch. Reused whole units
   must have their exact complete imports in the prior projection.
4. Accumulate all global census/storage/launch bounds. Retain the exact ordered
   unit IDs and batch metadata, not every proof byte in memory.

This imposes a deliberately simple producer contract: cross-batch dependencies
must point into the selected starting context or earlier manifest batches.
Forward dependencies across batches refuse even if a global scheduler could
reorder them. Dependency cycles within a batch refuse through the existing
planner. There is no new package solver or arbitrary repartitioning algorithm.

The projection is a **feasibility hypothesis**, not an accepted mathematical
environment. Never register it, pass it to native checking as an owner context,
return it as a successful root, or feed its preflight object directly to `admit`.
Later actual admission independently rederives every batch against a genuine
committed parent.

An implementation may copy exact validated files into a finite fresh local
spool or use an already owner-selected immutable spool. Later reads still check
the pinned length and hashes. If files change after preflight, refuse before
checking the affected batch; no earlier committed root is revoked or rewritten.
This is not an all-bundle transaction or a claim of immunity to a hostile local
owner. Spool creation/read/hash cost counts; no source execution is involved.

Known infeasibility should be rejected before native work: missing dependencies,
conflicting names, unsupported semantics, excessive structural counts, exhausted
root/operation slots, known custody quota exhaustion, and insufficient aggregate
artifact reservations. Future kernel success and actual artifact size cannot
be proved by metadata; the runtime still enforces their finite caps.

Custody byte accounting must not count only evidence length. Current
`ordinary_acquisition.OrdinaryStore._put` charges a new evidence object

```text
len(raw) + len("evidence") + 128
  + sum_over_exports(128 + len(canonical_locator))
```

as well as object/export row quotas. Use the same exact computation or a sound
conservative upper bound. Exact duplicate objects may need no new quota, but
validating that fact and their bytes/locators is not free. Database page/disk
limits and temporary storage remain independently enforced. A conservative
capacity refusal is permitted; pretending raw bytes bound all storage is not.

## Checking and the mathematical argument

After all metadata preflight succeeds, retain `last_confirmed_root = K.root`.
For each manifest batch, reread its exact evidence and call real owner
`preflight(last_confirmed_root, batch)` followed by real `admit` under a fresh
single-use **suballocation of the original invocation allowance**. Advance
`last_confirmed_root` only from the actual successful result. Do not select a
different branch because a status file says it is newer.

Current `admit` stages **all** supplied evidence to custody with exact readback,
including units already warranted. An all-reused batch returns `REUSED` with
the unchanged root and zero native checks, but still pays parsing, metadata,
custody validation/readback and bookkeeping. Keeping this existing behavior
avoids promising availability that a shortcut did not establish. No obligatory
native replay of already-warranted complete units is introduced.

Write `Valid(K)` for the existing policy-relative protected-context judgment.
For each successful batch the unchanged admission contract supplies

```text
Valid(Kj-1) and Admit(Kj-1, Bj) = Kj
  imply Valid(Kj) and bindings(Kj-1) is a subset of bindings(Kj).
```

This follows because all new imports resolve to exact already-warranted or
earlier checked declarations, every whole new unit is checked, and promotion
requires the live bound clean event. Reused units contribute no new assumptions.
Induction establishes validity of every confirmed prefix. Metadata preflight
is not a premise asserting `Valid(Pj)`.

The theorem is conditional on the existing checker, foundation, implementation
and protected-owner assumptions. It establishes **prefix safety**, not semantic
equivalence of arbitrary source projects, all-or-nothing bundle acceptance,
continued evidence availability or constant-cost context loading.

## Continuation and uncertain commits: no new progress protocol

Stop on the first failure, budget exhaustion or unknown native/commit outcome.
Do not retry, renew an allowance or rebuild a missing artifact automatically.
Previously confirmed roots, custody writes, failed reservations and their costs
remain retained. Report the manifest identity, original selected root, last
confirmed root, completed batch observations and the failed/unknown position as
diagnostics; none is a transferable mathematical warrant.

The catalog commit is the linearization point. A later exception or missing
response does not prove that no root was accepted. In particular,
`CATALOG_TRANSACTION_UNCERTAIN_REOPEN_REQUIRED` closes the catalog and requires
protected recovery. Do not replace that outcome with `ROLLED_BACK`, assume the
last confirmed root is the newest durable root, or replay a saved worker report.

After clean process closure, a later explicitly authorized invocation may use
the existing protected status/context path to identify and validate a root.
Listing a root ID is not enough: `catalog.context(selected_root)` must succeed
under current support/policy and snapshot checks. Sticky `WITHDRAWN`, corruption
or unresolved cleanup remains a refusal, not a request to reset the marker.

The caller then selects that validated root and the same or another exact
bundle, with a **new explicit finite allowance**. The ordinary whole-unit rules
skip all exact evidence already warranted there. A saved cursor is unnecessary.
No ancestry relation to the earlier starting root is needed for safety, because
portable evidence imports contain exact symbol identities. However, two roots
are not thereby merged: missing units are actually checked above the one selected
context, and a conflicting binding still refuses.

This permits safe continuation from a compatible independently warranted context
without asserting identical source interpretation or identical operation
history. A changed manifest is a new selected input, never silently called the
same attempt. Historical resource costs remain historical costs; a new allowance
is not zero-cost continuation and must not be reported as one uninterrupted run.

## Aggregate budgets and full costs

One invocation has one original wall deadline and cumulative controller/native
CPU allowance. Count metadata preflight, spool work, all repeated parses,
custody operations, context validation/loading, failed work and cleanup. Bound
the number of batches and actual launches; per-batch limits alone are insufficient.

Before each launch reserve its complete permitted native CPU/output grant from
the remaining envelope. The simplest safe implementation prepartitions finite
per-batch caps and does **not** refund unused reserved CPU. This is conservative
admission accounting, not a claim that the CPU was actually consumed. A more
permissive implementation may release unused reservation only from an explicit
finite trustworthy final accounting observation, never from missing data.

This matters concretely: `OperationBudget.worker_cpu` starts at zero, and
`_execute` updates it only when a final native CPU value is available. Zero in
that field after an exception is not evidence of zero native cost. Missing or
invalid final accounting retains the full authorized reservation. In the selected
nonrefundable-grant mode, a clean actual successful admission may continue without
complete measured CPU: the full cap already accounts for it. Report the core's
CPU observation as partial, never as zero actual expense. An unknown actual
checking/commit/cleanup outcome still stops the invocation. The existing
clean-worker/cleanup rules are unchanged. Do not
reinterpret a saved report as either accounting authority for a new launch or
mathematical authority.

Controller CPU checks are cooperative unless the whole public operation also
has an outer supervisor. Native Windows Job limits do not automatically bound
an unsupervised Python controller. A claim of hard whole-operation containment
requires an actual outer envelope; otherwise state the cooperative boundary.

Catalog root/operation/artifact reservations, custody quotas and spool limits
must all fit. Failed catalog reservations are retained and charged. A finite
upper bound on each expected artifact is authorization to attempt its production,
not a prediction of successful output or a bound on whole-system storage growth.

For `m` batches a useful cost decomposition is

```text
C_intake = C_metadata + C_spool + C_custody
         + sum_j(C_context(Kj-1) + C_check(new_units_j))
         + C_controller + C_failed + C_cleanup.
```

No ancestral theorem-proof replay occurs for the accepted prefix, but catalog
context construction traverses the selected chain and native workers load its
modules. Many tiny batches can magnify those costs. A proof-residency bound is
roughly one bounded batch plus bounded cumulative identifier metadata and the
real context, not memory independent of all selected mathematics. This operation
does not solve enormous cold closure checking; it makes a finite one-time
expense operable and reusable without hiding that expense.

## Separate boundaries that must not disappear in the handoff

**Evidence production.** A producer must supply complete supported ordinary
evidence with exact import identities. Current approved project extraction is
still coupled to a retained small candidate. Importing private Lean artifacts
can load a substantial transitive environment. Admission batching does not
provide streaming source extraction, missing private proofs, lower extraction
RAM, foreign toolchain compatibility or a license to execute remote projects.
Produce the closure once; do not re-extract the same source closure per batch.

**Ordinary realization.** Existing anchor total-unit cap is 1,024, chain cap 32,
and the ordinary new-delta request is 32 units / 4 MiB. Thus internal acceptance
of 2,852 units alone cannot make that closure available in an ordinary project;
32-unit slices would need at least 90 modules. The separate realization contract
must select a coherent finite baseline profile and resolve installed definition/
group collisions. Internal checked snapshots are not directly interchangeable
with normal Init-based project modules. These are limits of the regenerated
module route A1, not a requirement that A2 regenerate that background. A2 instead
needs the separate exact private/public dependency-closed correspondence and
artifact-bound caching obligations in the strategy update. It cannot adopt the
local project's unchecked mathematics merely to preserve its frontend features.

**Benefit.** A pinned ordinary Lake library with the same indexes, tactics,
caches, representation and warm reuse is the proper baseline. The commons
route must earn its additional independent checking/production/realization cost
through actual selective reuse, discovery, assurance or integration advantages.
This intake contract alone proves no useful-growth or speedup claim.

**Huge-network architecture.** A receiver chooses relevant finite baselines;
it is not required to import all network knowledge. Strict cold missing-closure
cost remains. Certificates or an explicitly different approved-base trust mode
may later serve a justified workload, but neither is silently enabled here.

## Smallest consequential implementation and discriminator

If root selects implementation after source review, the minimal consequences
are a bounded manifest/spool parser and projected planner; a thin finite owner
facade over unchanged actual preflight/admit; cumulative authorization and
precise partial/unknown reporting; and a source-complete package/API recipe.
No new mathematical checker, catalog authority, retry journal, global scheduler,
consumer rebase, network protocol or certificate relation is needed.

Metadata tests should cover a dependency into an earlier batch, a forbidden
forward dependency, conflicting IDs/partial groups, oversized input, last-batch
metadata failure before any native launch, exact reused groups, cumulative
capacity refusal and changed evidence bytes. Native-free doubles may test call
ordering and accounting, but cannot prove mathematical acceptance or durable
commit recovery.

Reuse the historical large admission evidence for batching feasibility. The
small new public discriminator need only exercise at least two dependency-linked
batches through the real facade, then an explicitly selected existing root that
skips the already accepted exact units while checking one new dependent unit.
Reuse existing catalog uncertainty evidence for unchanged commit semantics;
test the new facade's uncertain-result reporting without a new large failure
campaign. A separate ordinary-module consumer is required before describing
baseline onboarding as usable. No runtime is authorized by this note.

## Concrete producer seam: selected full closure over the exact fixed seed

The source already contains most of a practical producer. A user should select
a finite local library and exact target names, then receive the manifest and
files automatically; hand-authoring thousands of evidence files is not an
acceptable workflow. The smallest candidate is a **thin parameterized successor
of `ordinary_lean/NativeOwnerExporter.lean` plus an inert V2 binding/splitting
controller**. Keep the existing shared closure exporter unchanged.

### Existing source mechanisms and exact limitations

`NativeOwnerExporter.run` already imports one private source environment with
runtime-first explicit paths, no inherited `LEAN_PATH`, no plugins and
`loadExts := false`; compiled helpers are not a second imported mathematical
environment. It invokes `Export.indexSource` and `Export.selected` and emits
the bounded `DMKN_ORDINARY_EXPORT_BUNDLE_V1` **writer format**. This writer schema
is not the old portable evidence identity scheme. Its current entrypoint is
hardcoded to `examples.ReadFootprint` and
`DMKN.ReadFootprint.readsOnly_insertMany`; it is not already a general public
library producer.

`OrdinaryExport.selected` compares the source's exact normalized fixed-basis
inventory before using that basis as its stopping boundary. The source limits
are 8,192 units, 64 MiB total encoded-unit bytes, 8 MiB per unit, 1,024 targets,
262,144 selected dependency edges and 20,000,000 traversed source nodes, with
separate source/group census and codec limits. It collects complete declaration
groups, rejects new axioms/unsafe/partial declarations, checks the selected
closure, and emits dependency-ordered units. The final native writer additionally
bounds the entire wrapper to 64 MiB. No new giant-corpus algorithm is needed for
this finite producer.

The approved-project extraction adapter already supplies the explicit roots/
module grammar and local-selection validation. Reuse that selection mechanism,
not its retained-consumer coupling or 32-unit completion capacity. A fresh
producer request selects its exact target list directly; there is no need to
invent a failed consumer first or modify an earlier retained request.

The native successor should replace the fixed module/target selection with
bounded explicit request fields and reuse the missing-import extractor's safe
complete-record target check instead of the example's theorem-only target gate.
The shared closure exporter still decides which full declaration kinds/groups
are supported. Preserve the current private import, exact seed-inventory
comparison, complete closure selection and output bounds, as well as the existing
Windows path-spelling rule from the reviewed project extractor. No source build,
tactic execution, dynamic owner lookup
protocol, callback-based arbitrary boundary or certificate is necessary.

### Inert V2 binding and automatic manifest production

The controller authenticates the selected runtime/executable and the fixed
inventory bytes whose hash is `ordinary_semantics.INVENTORY`; its exact 581
names and selected `S = semantic_id()` / `F = foundation_id()` are locally fixed,
not supplied by the writer as mathematical authority. After the bounded native
export closes cleanly:

1. Reuse the bounded Lean-writer JSON reader, exact wrapper/target/statistics
   checks and `ordinary_evidence.inspect_unit`. Require the writer's basis list
   to equal the exact fixed inventory list. Require a nonempty selected closure
   and targets outside that fixed basis; a request naming an already-fixed-basis
   target receives an explicit already-in-basis refusal, not a fabricated
   wrapper theorem. This keeps the minimal producer's target/output rule exact.
2. Initialize a temporary identity map only with
   `basis_symbol_id(S, F, name)` for those 581 names. This is an identity
   computation, **not** a claim that this producer has checked a basis. An
   actual strict receiver still needs its independently warranted fixed basis.
3. For each already dependency-ordered complete unit, compute its exact external
   reference census and require every reference to be in that map. Construct
   canonical V2 evidence using precisely those imports, parse it with
   `portable_evidence.read_evidence`, and reject any output collision with the
   fixed basis or an earlier unit. Extend the temporary map using the actual
   `ordinary_semantics.export_id(S, unit_id, name)` functions.
4. Greedily place consecutive whole units into the manifest's batches, closing
   a batch before any existing unit/byte/node/name/edge cap would be exceeded.
   Check that a unit can fit by itself. Since the entire prior order was checked,
   this batching introduces no forward dependency. Also bound the native
   unit-array serialization needed by admission, not only envelope lengths.
5. Write the exact fresh `units/<unit_id>.json` files and manifest, verify
   readback/hash/length and that all selected target names occur among the
   emitted outputs. Emit target export IDs and producer provenance only as
   separate inert convenience metadata. Publish the completed manifest only
   after all required local outputs exist; preserve partial/failing outputs
   under their original attempt instead of presenting a complete bundle.

This loop reuses the identity/envelope logic in `portable_candidate.bind_candidate`
and the finite splitting pattern in historical
`run_native_admission.prepare_bundle`. It must call the **current V2** identity
and evidence functions directly; the historical function itself uses old profile-
bound V1 identities and a hardcoded target and is not a drop-in implementation.
The ordinary candidate binder expects a genuine selected protected context and
authenticated prepared request. Do not feed it a fake root or arbitrary lookup
map merely to reuse a helper. A small pure seed-bound loop avoids that false
premise and avoids opening an owner/catalog just to manufacture portable claims.

Require finite aggregate encoded-node/name/edge/output caps and the installed
parser limits in addition to the native bounds. The producer can initially
retain the same 64-MiB maximum for the complete portable evidence set; envelope
overhead means a near-limit writer bundle may then refuse. It must not silently
increase that maximum. The exact full-request/spool/CPU/memory profile remains a
separate source selection. The writer constructs one bounded JSON bundle, so
this is **not streaming extraction**: Lean structures, JSON serialization and
Python parsing can multiply peak memory beyond the 64-MiB byte cap. Use an
actual finite outer process envelope and fail honestly when a closure does not
fit. Do not rerun extraction separately for every admission batch.

### What the operator has approved, and what remains unproved

Targets are explicit structured local names chosen by the operator, not global
research tasks or human-intention acceptance conditions. Import roots/modules
must come from an explicit owner-selected approved-project descriptor, using
the existing supported-runtime and path rules. The approved local artifacts
may be deserialized to extract inert records. A peer bundle cannot select that
environment or cause this producer to load a peer binary or project source.

The existing project-selection hash authenticates the **selection document**
(ordered roots/modules), not their complete transitive artifact contents.
Likewise, `loadExts := false` and empty plugins are not a hostile-artifact sandbox.
This seam therefore inherits an approved-local-input safety premise; it does
not claim hermetic source provenance or that a root pathname cryptographically
identifies a library. No actual user project has been supplied or approved here.
The historical ReadFootprint selection is old evidence, not a new runtime grant.

These limits do not make emitted proofs mathematically trusted: each receiver
still parses, binds and independently checks the full missing inert units.
They do matter for A2. A completed extraction receipt alone cannot authorize
future reuse of the local project as a correspondence cache; A2 must separately
bind its exact selected artifact graph and prove the relevant private/public
interpretation relation. Changed artifacts invalidate that separate relation.

This producer is a selected finite-closure exporter, not a way to import all
Mathlib or all network knowledge cheaply. If actual project private imports or
supported closure bounds are the blocker, record that outcome before designing
a streaming exporter or approved-base trust mode. The next implementation
decision must join producer, strict intake and the chosen ordinary-project
correspondence route; completing any one in isolation does not close v5.

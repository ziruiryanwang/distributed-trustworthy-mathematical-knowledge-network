# Same-base reuse: repair only the checked delta materializer

2026-10-24. `thin_reuse_route`; bounded source/theory decision. No implementation,
native process, build, download, protected-state operation or Git mutation.

## Decision

**Prefer a versioned, module-only successor of `ReferenceModule.lean`.** Retain
the existing original-base correspondence/registration and exact delta collector;
correct its private-versus-exported enclosing-header expectation. Do not revive
`contribute-reference`, `ReferenceSource02` or general frontend reconstruction.
Do not build a proof-to-Lean-source emitter for this case.

This is the smallest supported route to the newly selected growth target:
an independently warranted new result becomes usable inside a recipient's
existing approved, exactly matched ordinary base without importing producer
code or a second copy of that base. Root must select implementation and any
changed-boundary execution separately; this note is not runtime authority.

## The exact useful case, not all theorem-only extensions

Let K be an eligible independently checked local mathematical context, P the
recipient's approved original compiled base, and e a new supported declaration.
Require a protected correspondence between P's actual private/public records
and the selected warranted interpretation in K. Approval to execute P is not
that mathematical warrant. The recipient must keep using those exact artifacts.

The existing materializer additionally requires e's complete proof to check
against the registered **public** base frontier, not just its private data.
Therefore "theorem-only" is not itself a compatibility guarantee. A proof using
private-only helpers or computation hidden by P's public abstraction may refuse.
The mode correction does not weaken that gate, erase proofs or promise all Lean
libraries. Different versions, new producer metadata and arbitrary environment
merging remain outside this selected case.

Subject to these premises, new checked module D imports P rather than redefining
it. The recipient imports D into its ordinary project and retains P's notation,
classes and tactics from its already approved artifacts. D need supply only the
new warranted declarations, not the producer's frontend extensions.

## Why the current ordinary route alone does not suffice

`OrdinaryModule04.run` imports Init or existing generated anchors. Its exact
installed-singleton-theorem matching does not establish a generic original-base
frontier, and installed definition/group collisions refuse. OwnerConstruction
and OwnerRebind construct/rebind scratch authoring environments; they do not
materialize a proof-complete thin module over arbitrary original P. Their
scratch assumptions remain subject to independent final admission.

`produce-baseline` and `intake-baseline` already handle selected complete inert
evidence and independent acceptance. They do not by themselves make the admitted
result importable inside P. Conversely, approving the producer's package solves
a different problem and gives up this case's no-new-producer-code condition.
A checked bridge cannot resolve duplicate import names before it can be used.

## Why local explicit-proof source is not the smaller implementation

In principle a fixed approved structural adapter can decode the complete new
proof, check exact constant interpretations, and create a theorem in P. No
producer tactics need execute. But the present source supplies no qualified
general Expr-to-source output route for that purpose. A surface emitter would
need exact names/universes, binder hygiene, dependent expressions, projection
and literal treatment, bounded output and actual rechecking. Pretty-printing a
proof or evaluating downloaded tactic text is not that contract.

If instead the adapter inserts decoded declarations directly and writes a
module, it has recreated the essential existing ReferenceModule operation:
exact artifact imports, base interpretation, checked new declarations, output
binding and fresh rereads. Avoiding text does not avoid those responsibilities.

A weaker reconstruction may reinterpret foreign names in the recipient's local
environment and prove a new local statement. That can be useful advice, but it
does not establish the original portable identity. Its result must be presented
as newly checked local mathematics and it still depends on warranted local
premises. Do not silently substitute that different contract for same-base reuse.

Thus route B is feasible as a future narrowly motivated adapter, not currently
cheaper than repairing the existing structurally decoded materializer. No new
proof syntax, interpreter or source-emission campaign is justified here.

## Source-proven defect and bounded correction

The retained audit already diagnoses the defect; this is not a new discovery.
Pinned Lean `Environment.importModules` forwards the chosen OLean level to
`finalizeImport`, whose default `isModule` is `level != .private`. Consequently
private inspection has a false enclosing header even when every imported module
is individually modern. ReferenceModule's `checkBaseHeaders` currently rejects
that valid inspection mode unconditionally.

Unlike the parked source extractor, ReferenceModule already performs **separate**
private and exported imports in `run`, and separate private/exported `reread`
phases. Its private inspection never needs to masquerade as the public view.
The minimal correction is therefore:

- Require `env.header.isModule == publicView` for these supported call sites,
  where `publicView` is false for `.private` and true for `.exported`.
- Keep every imported record's `data.isModule` requirement and exact import
  order, root/artifact map, generated header and declaration census checks.
- Keep independent checks against registered private versus public/kernel
  projection metadata. Do not flip a header or synthesize a public map.
- Keep both actual `CheckedExtension.checkBatch` passes, full new inventories,
  output binding, artifact hashing and both fresh rereads before promotion.
- Keep the final output writer based on the actual exported environment;
  `setExporting true` on private data is not an alternative public import.

`OwnerRebind.exposeAdded` exposes actual newly checked recursors/registers local
prefixes; it does not require or synthesize an exported base. The unchanged
checker inserts genuinely checked declarations via `addDeclCore`. No new
calculus, assumption policy or peer warrant is needed for this correction.

This source argument identifies the intended delta. It does not establish
compilation, runtime success or absence of later compatibility failures.

## Support identity and minimal end-to-end consequence

The existing `reference_registration.support_descriptor` pins the delta native
source as well as its worker/controller and the exact matcher/support artifacts.
A changed materializer therefore changes support identity. Existing registration
cannot silently authorize it, and no saved success report may be imported as a
new live warrant. Preserve the old registered state and failures unchanged.

An eventual integration must use either a freshly authorized registration under
the new support or a separately justified migration. The latter is more scope;
**prefer fresh registration, not a migration mechanism**, while retaining the
already checked mathematical base where the existing owner APIs permit it.
Charge snapshot/match/setup costs; no implication of cheap fresh cold onboarding.

The intended finite route needs no special reference source-authoring command:
ordinary approved authoring/owner-free production -> existing independent
intake -> registered same-base delta materialization -> ordinary recipient use.
Materialization follows genuine ordinary admission; it does not supply new
peer acceptance, incremental producer export, useful discovery or general P
onboarding. Those are distinct obligations, not implied by this repair.
Returned complete proofs use the existing ordinary contribution/completion path
when its limits and bindings are satisfied. Do not call that whole path tested
by composing separate predecessor passes on paper.

The smallest future discriminator must check the changed boundary: private and
exported base/header modes, an actual delta importing unchanged P, fresh rereads
and ordinary application alongside P, with an incompatible interpretation or
private-only dependency refusing. It need not repeat proof search, certifier,
index or broad growth campaigns. Exact fixtures/allocation remain root's choice.

Initial matching/snapshotting, full selected-context imports, proof/conversion,
new evidence, materialization, retention and failed attempts remain real costs.
The architectural gain is avoiding a duplicate base and new producer execution
in this compatible warm workflow, not a measured research speedup or general
ancestry-free verification. This source-only choice does not close final v5.

Sources read: GROWTH-VALUE-CHALLENGE; RETAINED-WORKFLOW-AUDIT's final diagnosis;
ReferenceModule checkBaseHeaders/importBase/run/reread; registration support pins
and delta-controller protected-reference load; OrdinaryModule04.run; OwnerRebind
exposeAdded and OwnerConstruction; pinned Lean Environment import/finalization.

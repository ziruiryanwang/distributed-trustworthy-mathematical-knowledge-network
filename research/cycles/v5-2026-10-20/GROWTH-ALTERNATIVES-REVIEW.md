# Independent review: direct I versus aggregate A

2026-10-20, core_search. Source and saved-evidence inspection only. Canonical
guard passed; no runtime, code change, proof, benchmark, RAM investigation or
Git mutation. Reviewed `GROWTH-NEXT-DECISION.md`, including its typed-row follow-up.
Economics derivations are not repeated here.

**Disposition: the central distinction is sound, with the integration scope
clarification below.** It neither establishes a successful new frontier seal nor
justifies claiming full Lean soundness or positive current implementation profit.

## Direct-I induction: what was checked

`modules/receipt/src/relation.rs::check_bound` checks exact foundation values,
same-image/foundation/policy parent journals, distinct module ownership, group
openings, canonical committed bodies and conditional row correspondence. It
checks every local descriptor with the existing conditional native checker and
requires rank zero for no parents, otherwise exactly `1 + max(parent ranks)`
with checked overflow and every parent rank strictly smaller. `src/main.rs`
then invokes actual `env::verify` for **every** returned exact parent J before
committing the child J. Rank alone is not authority; those premises are essential.

`src/bin/module_host.rs::checked_receipt` rejects Fake and Composite receipts,
requires succinct Poseidon2, uses `with_dev_mode(false)` and full application
verification, and binds the actual adopted image to the journal's image,
foundation and policy. Python `admission/bindings.py` additionally binds current
stdout, exact receipt bytes/hash and exact journal/summary; it explicitly says
that fabricated stdout is not verification. A saved receipt report is not a
substitute for executing the adopted verifier.

The induction is therefore valid **conditional on** the recursive multi-premise
cryptographic soundness claim and the checking/correspondence interpretation.
In a concrete cryptographic theorem, use the stated adversarial/security model
and forgery-error bound, not an unconditional logical implication over arbitrary
bytes. This source inspection proves neither that security theorem nor the
checker-to-unrestricted-Lean refinement. The note already discloses both
conditions; it does not improperly promote VM execution into all-of-Lean truth.

For the certified child proposition, a cold receiver need not obtain parent
receipts or ancestral theorem witnesses merely to discharge that proposition:
the final succinct child receipt has discharged its own assumptions. A usable
mathematical context may nevertheless require imported types, transparent
bodies, recursor metadata and compatible warrants for separately selected
semantic objects. The note correctly preserves that distinction. It does not
claim constant total import cost or eliminate required semantic dependencies.

## A and exact identity

Same-I recursive branching already exists. A is not required merely because a
module contains many local declarations. Its distinct benefit is a bounded
retrospective DAG seal that preserves the exact journals of native intermediate
nodes without producing a separate I receipt for every one of them.

Repackaging those declarations into a new module can change owner-qualified
references, ModuleID and J; it is not sealing the old exact graph. An A-member
also is not an I receipt accepted by the same-I guest. A changed I executable
cannot silently inherit the old same-I premises. Those distinctions are
accurately represented in the note and must remain in any eligibility report.

## Existing pure-I capability is broader than the missing unified-facade seam

The current atomic client already exposes `admit_receipt` and passes a live I
warrant to `MixedImportSession.use_legacy_handle` from `import_context`.
`semantic_material(I)` explicitly asks for caller/provider semantics; it does
not refuse I use or pretend that the succinct receipt supplies its bodies.
The existing `LocatedReceiptWorkflow` composes formal discovery, receipt offers,
exact receipt custody and real receipt admission. `ReceiptStore` and the HTTP
receipt provider already implement the lower-level pure-I wire route.

The missing convenience/integration is narrower: current ordinary packet
publication/acquisition uses a nonempty native-delta grammar or terminal A-member
evidence. `workspace_evidence.export_evidence` refuses an I warrant, and its
terminal parser requires A membership. Therefore neither a zero-delta mixed
packet nor a dummy A owner is a legitimate shortcut.

The two proposed seams are necessary for the **chosen frozen-native-packet to
unified ordinary-facade route**, not prerequisites for every direct-I production
or reuse route. `SourceOperation`, `ImportSession.make_request` and
`OwnerPreparation.snapshot` already support source-derived I preparation;
lower-level pure-I circulation already exists. Root should select a specific
missing workflow, not rebuild those facilities to make a second product lane.
This clarification was sent directly to core_growth.

## Actual previous child failure is decisive negative evidence

I read the saved
`experiments/v5-local-checks/receipt-source-integration-01/evidence/RESULT.json`
and its selection/outcome checkpoint. Base I admission, source authoring and
host preparation succeeded; selected child `4adbc049...` had one local theorem,
526 export rows and 1,355 relation rows. Its actual source closure references
the imported `binary_congr` while imported theorem-proof bytes are zero.

The guest snapshot then refused
`Session limit exceeded: 33557665 >= 33554432`; no child capsule or child
receipt was produced. The recorded whole operation failed, with clean enclosing
closure, 13.515625 CPU seconds and about 44.0269 wall seconds. These facts support
the preparation/reuse prefix, not successful frontier supply or a production
upper bound. They neither prove direct I is intrinsically slower than A nor
justify repeating it under a larger cap. The later complete A capsule is
strictly more execution evidence for its selected input, not an A receipt.

## Typed-row coordination and next decision

core_growth owns the constructor/field acceptance table. No overlapping table
or implementation is introduced here. I communicated these separate authority
categories for its surrounding decision: live I warrant; live A-member warrant;
native witness; unresolved proof checkpoint/capsule; unverified raw receipt
bytes. None may be promoted by a representation optimization.

The table's refinement target is the intersection of strict input parsing,
conditional correspondence and ordered native application. Preserve exact J,
all exact parent premises, unused-row handling and foundation comparisons;
equating only successful final JSON is insufficient. The identified `all`
field loss and reachable-versus-unused payload distinction warrant a finite
source audit before implementation. I have not independently certified the
27-constructor table's every field or Serde corner case; that is core_growth's
separately owned unfinished task.

No additional economics helper or pure-I transport implementation follows from
this review. The high-payoff choice remains supported frontier production and
an exact representation refinement that could reduce its actual cost without
changing mathematical acceptance.

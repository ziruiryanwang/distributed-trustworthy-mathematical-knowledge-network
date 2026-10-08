# Minimal verified import and ordinary Lean authoring seam

Source-backed proposal, not implementation authority or a passed public workflow.
Mechanism lane. Root selects ownership/runtime; existing receipt/build sources
and tests remain frozen. The immediate execution/segment decision takes priority.

## Two boundaries, not a new authority-bearing JSON format

`admission.verifier.ReceiptVerifier` already owns live registered handles and
same-call exact receipt verification. `modules.model.ConditionalEnvironment`
and `modules.receipt.witness.make_input` deliberately do not establish trust.
A thin owner-process adapter should join these boundaries without changing them.

Proposed source ownership, only if selected: `software/v5/authoring/imports.py`
for operation-local verified imports; `AuthorLean.lean` and `source.py` in that
same directory for the bounded local authoring path. Root retains admission,
proving-stage integration and deployment configuration. No discovery change,
global registry, source trust flag or new certificate profile is needed.

An `ImportSession` holds exactly one live owner-created verifier, a finite byte/
group/body budget, immutable receipt copies and a local map of opened groups.
Its public acquisition input is `(receipt_bytes, expected_summary, openings)`;
or an existing handle plus its exact receipt bytes. It calls `receive` once
per exact `(profile_id, canonical_summary_bytes, receipt_sha256)` in this session,
then `describe` and `open_group`. Every cache hit rechecks handle liveness and
exact byte equality, not just ModuleID. The cache cannot deserialize acceptance.
Close/expiry revokes all authority. Different receipts for the same module need
explicit deterministic first-selected-parent handling; do not merge their ranks
or journals. A module has one exact parent journal in a child request.

### Selected D19 deadline/lifetime bridge

Root temporarily assigns the previously unused `authoring/imports.py` seam to
the scale lane for this narrow source-only bridge and focused refusal controls.
No Lean frontend, proof relation, used admission/transport source or existing
evidence is changed. Actual runtime requires independent source/selection review.

The session accepts exactly owner-created `ReceiptVerifier` or
`DeadlineReceiptVerifier`, not arbitrary subclasses, `isinstance` widening,
duck-typed verifiers or saved-success dictionaries. Construction requires the
actual verifier to be live. The session's deadline is the minimum of the caller's
requested lifetime, the verifier's actual deadline and (for the deadline-bound
variant) its original outer D. Every session liveness check also checks that
same verifier. Closing the verifier therefore refuses even empty-session data
or request operations, not only operations that happen to describe a handle.
All original registry/receipt/summary/journal bindings remain unchanged.

`LocatedReceiptWorkflow.close()` owns closing its verifier and revoking its
handles. Consequently use the same live verifier to select acquired handles,
open groups, supply demanded committed bodies and build the request **before**
closing that workflow. There is no ownership transfer through a serialized token.
The resulting untrusted prover request may outlive a local session only because
the host/guest independently reverify its genuine parent receipts, exact selected
journals and all child obligations; persisted local success is never authority.

Internal construction derives `ImportClaim` ONLY from the live handle's decoded
184-byte journal and exact retained receipt hash. It uses `open_group` on every
selected opening, then adds the derived claim/openings to a private conditional
environment. It exposes copied data for authoring, not its mutable environment
as a reusable trust object. `make_input` receives the exact journal/opening set;
the output is still an UNTRUSTED PROVER REQUEST. Actual host parent verification,
guest `env::verify`, local checking and final empty-assumption admission remain
mandatory. Local source cannot make the adapter accept caller-authored claims.

Hash-bound definition/recursor bodies can arrive separately. Every body uses its
owner namespace, universe arity and committed digest; bounded demand expansion
must fail closed on missing content. No proof-ancestry fetching is introduced.
Copies, parsing, hashes, demands and failed requests count against session cost.
Verification dedup here only removes duplicate owner admission within an
operation; it does not yet remove host verification across proof-stage commands.

## Existing Lean seam and the genuine missing piece

`workloads/ExportWorkload.lean` already elaborates ordinary owner-selected Lean
source under pinned Lean4.34, exports native rows and whole inductive groups,
and labels output untrusted. Its current roots are hardcoded to two workload
theorems. It starts from Init, so it is NOT an arbitrary imported-module authoring
interface. `source_rows.decode_source` already converts such rows into local
spec/proofs with explicit local/foundation/external structured-name inventories;
external declaration rows are omitted, and local axioms refuse.

The old frozen `native/AgentClient.lean` demonstrates a useful pattern: import
Init only for frontend syntax, reconstruct selected dependency-ordered bindings,
check their canonical identities, elaborate owner code, preserve all old bindings,
and export only reachable new dependencies for independent checking. Reuse this
pattern, not the old all-proof replay or its old content format. Do not edit it.

A fresh adapter must therefore:

1. Accept selected structured source roots and the session's exact imported
   declaration registry. No dot-splitting of semantic names and no fixed workload
   theorem names. Derive new reachable local names from the elaborated environment,
   including kernel-generated auxiliaries and complete atomic inductive groups.
2. Assemble a frontend environment from exact bound foundation and selected
   imports under `DMKN.Mod.<ModuleID>`. Shared Init constants must match adopted
   canonical bindings; unrelated frontend library constants used by new work are
   captured as new local dependencies, never silently added to the foundation.
3. Install imported Prop theorem interfaces as explicit AUTHORING-ONLY assumptions
   with exact external mappings; their proof bodies are not downloaded. Opaque
   imported values may similarly use non-reducing authoring-only assumptions,
   provided the final relation retains their original Opaque descriptors. This
   is a proposed frontend representation, not public axiom admission, and needs
   separate soundness/compatibility review before implementation. No fresh local
   axiom or undeclared assumed interface may escape as a checked contribution.
4. For transparent imported definitions, install actual authenticated bodies with
   their original definition hints. Stock Lean does not provide this project's
   `NeedBody` kernel semantics. Therefore the first adapter must fetch the selected
   frontend definition/body dependency closure BEFORE elaboration or refuse with
   a bounded explicit demand. It must not replace absent definitions by opacity
   or dummy values. This may fetch more semantic bodies than the final guest
   demands; charge it honestly. It still need not fetch ancestor proof histories.
5. Reconstruct complete imported inductives/constructors/recursors with native
   Lean's group constructor, and compare all regenerated committed metadata/rules
   after canonical relocation. Do not install arbitrary claimed reduction rules.
   If selected metadata cannot be reproduced, refuse rather than approximate.
6. Run only owner-authorized local source: Lean source/macros/initializers are
   executable code, not a hostile-data sandbox. Check old bindings unchanged;
   export the selected new closure; call `decode_source` with inventories derived
   from the session and frontend, not manually written canonical JSON. Then add
   the session's authenticated group/body openings and construct the prover input.

Independent final relation checking remains the soundness firewall if frontend
elaboration uses additional syntax, unsafe owner tactics, or authoring assumptions.
It cannot compensate for an unusable adapter that routinely generates false
conversion obligations, so exact relocation/kind/metadata controls matter too.

## Smallest consequential validation if selected

Use one actual verified base module, ordinary Lean source defining a genuinely
new child over its imported Tree/map interfaces, and the same retained base
receipt. The author supplies source and roots, not a canonical spec or claims.
Check one duplicate-use handle path, one foreign/expired-handle refusal, one
changed-body refusal, one unknown assumed-constant refusal and one hidden new
axiom refusal at their changed boundaries. Reuse existing codec/kernel negatives.
Final real child receipt and a cold receiver remain a separate required endpoint.

The historical `PrepareReceiptWorkload.py` remains frozen profile1-only and
asserts an obsolete witness field. Do not advertise/invoke it as this workflow.

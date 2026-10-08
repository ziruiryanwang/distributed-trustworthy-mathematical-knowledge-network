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

### Selected D20 exact-address dependency-group companion

Root selects fresh `authoring/acquisition.py` without modifying the now-used
D18/D19 transport or import-session files. `DependencyAcquisition` requires the
exact adopted `LocatedReceiptWorkflow` and `ImportSession` with the **same live
DeadlineReceiptVerifier** and an already selected module. It captures and
rechecks their exact acquisition/client/store/budget/verifier object identities.
The session may expire earlier than the workflow; both are checked before and
after work, during precommit, and after output copying.

`declaration(provider,module,structured_name,max_bytes)` copies the validated
name before awaiting the retained structural client's `_get` on the existing
exact-address group route. There is no new client, grant, deadline, provider referral, receipt
verification or proof download. This is explicit semantic-dependency acquisition;
it has **no RecordID and is not a discovery candidate**. It does not change the
original search's `seen_candidates` or waive that set's export gate. A new module
must first acquire a real receipt and be selected by the existing live session.

The retained transport bounds the reply and checks canonical bytes. The companion
checks the ModuleID group opening, exact live selected summary and unique
structured name, then derives the usual typed locator/ExportID directly. It
does **not** call the retained `declaration` helper: that helper constructs
optional discovery features twice, which could refuse a valid complex dependency
at the feature-profile cap. Dependency acquisition requires no such feature work.
It durably commits and reads back the exact group/descriptor through the
same ModuleStore, then calls the actual `ImportSession.open_group`. All HTTP
attempts and unknown outcomes retain the existing shared accounting, original-D,
contact-TTL and egress checks. This adds no automatic retry or network traversal.

Store commit, session selection and returned data are not one atomic operation.
A later failure may leave structural custody or a verified session opening;
neither mints a new handle or a transferable acceptance record. The companion
returns copied data and marks nonpromotion/non-atomicity explicitly. Closing
the existing workflow still revokes every originating handle; the companion
owns no new closer. This is source-only pending independent review and focused
changed-boundary controls; no positive receipt/import qualification is inferred.

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

## D20 selected source implementation and exact native reconstruction proposal

Root selects **fresh source-only** `authoring/context.py`, `AuthorLean.lean` and
`source.py`. Existing used imports/acquisition/exporters remain frozen. This
section fixes the proposed complete-group algorithm before implementation;
independent native-boundary challenge precedes coding that seam. No runtime,
build or positive admission is selected by this source assignment.

### Existing Lean4.34 APIs actually inspected

The retained runtime is `software/runtime/lean-4.34.0-windows`. Its
`src/lean/Lean/Declaration.lean` defines `Constructor {name,type}`,
`InductiveType {name,type,ctors}` and
`Declaration.inductDecl (lparams : List Name) (nparams : Nat)
(types : List InductiveType) (isUnsafe : Bool)` (lines173–196).
`Environment.lean:701` provides
`env.addDeclCore maxHeartbeats maxRecDepth decl none (doCheck := true)` and
documents that it checks the declaration. This also populates elaborator
constant visibility. `Lean.Elab.Frontend.lean:134` provides
`Lean.Elab.process source environment options fileName`.
These are retained source/API observations, not a successful new build.

`InductiveVal`, `ConstructorVal`, `RecursorVal` and `RecursorRule` expose all
committed metadata: mutual members/constructors/parameter-index-field counts,
nested/recursive/reflexive/unsafe flags, motives/minors/K flag and each rule's
constructor/field count/RHS. `Declaration.getNames` explicitly warns that it
omits nested auxiliary recursors. Therefore that function alone cannot establish
the generated census; compare the actual environment difference after insertion.

### Three files, one coherent authoring operation

`context.py` freezes data from the actual live ImportSession and expands only
the selected semantic context. Its address map is `(ModuleID, structured Name)`;
the whole group is the indivisible installation unit. It traverses declaration
types, transparent-definition bodies and recursor rule bodies, recording work,
unique groups, body bytes and outstanding typed demands under finite limits.
Theorem proof bodies and opaque values are not traversed. Missing groups/bodies
return explicit bounded demands without starting a process or dialing; the
owner satisfies them through the existing same-budget acquisition/session APIs.
No foundation or newly encountered module is silently accepted. Each imported
module must already have the same verifier's live session selection. Foundation
rows have an owner-adopted exact byte pin; unrelated Init is not that foundation.

The assembler builds a dependency graph over selected groups, using every
semantic reference in the required types/bodies. It topologically orders them;
self references are allowed only within a complete inductive group being
constructed. Unexpected cycles or absent definitions refuse, not become axioms.
The resulting packet is private untrusted frontend input, not a new receipt or
portable trust token. Before/after frontend work the owner rechecks the live
session and immutable selected data; late expiry cannot yield a child request.

`AuthorLean.lean` reconstructs a frontend over pinned Init for syntax only.
The exact adopted foundation subset is compared against its supplied canonical
view before use; a conflict refuses. The decoder uses structured names and
ordered universe parameters, de Bruijn indices, exact binder info and the
existing canonical expression tags. It rejects metavariables, free locals,
unsupported constructors and undeclared references rather than guessing.
Each imported absolute name is the exact `codec.relocated_name` spelling,
not display-string parsing. Imported theorem/opaque interfaces are explicitly
authoring-only assumptions; their types/registration are exact, and they can
never become new accepted axioms. Transparent definitions install actual bound
bodies with their committed hints. No `sorry`, dummy theorem proof, arbitrary
recursor insertion or `doCheck := false` is permitted.

For **each complete inductive group**:

1. Obtain the ordered type list from the common committed `meta.all`; require
   consistent type-universe parameters and `num_params`. Obtain each type's
   ordered constructors from its own committed constructor list. Decode their
   exact types with this group's type names in the allowed mutual scope.
2. Require every declared group name to be absent. Call checked
   `Declaration.inductDecl` with those types/constructors and `isUnsafe=false`.
   Do not submit claimed recursor rules as kernel declarations.
3. Enumerate **all newly created constants**, not only getNames. The new-name
   set must equal the authenticated group's exact declaration-name set; every
   new constant must have the expected kind. An extra nested helper, missing
   recursor or differently generated name refuses unless it is already part of
   that exact complete group. No synthetic name repair or extra trusted group.
4. Compare types after replacing universe parameters by their positional names,
   dropping expression metadata and ignoring only binder display names (not
   binder info, levels, de Bruijn positions, projection owner/index or references).
   Compare all metadata fields and ordered lists exactly. For every generated
   recursor rule, compare actual constructor, field count and normalized RHS
   with the actual supplied expression previously hash-bound by the session.
   The Python adapter already checked the RHS digest; Lean need not invent a
   second cryptographic hash implementation. Any difference refuses before source.

This permits nested groups only when the complete committed/generated census
and metadata really agree; a successful simple Tree group is not broad nested
compatibility evidence. Scope is determined by explicit refusal, not by accepting
approximate native metadata. The checked constructor plus comparison supplies
frontend compatibility; only the later certified relation grants mathematics.

After assembly, preserve all old bindings across owner-source elaboration.
Roots are caller-supplied structured names and may select a theorem, definition,
opaque value or inductive group. The exporter stops traversal at exactly adopted
foundation/registered external bindings, captures new reachable auxiliaries and
complete groups, and refuses fresh axioms/unsafe/partial declarations. Imported
authoring assumptions are omitted only through that explicit external registry.
Unknown library constants used by the child must be captured as local dependencies
or refused, including hidden `sorryAx`; Init syntax grants no semantic exemption.

`source.py` binds the owner source, roots, context and fresh export files under
the original finite operation. It verifies the returned census and old bindings,
derives local/foundation/external inventories rather than asking the caller for
canonical groups, and calls existing `source_rows.decode_source`. Only this new
local-only ConditionalEnvironment is passed to ImportSession.make_request.
The result remains an untrusted request with exact genuine parent receipt bytes;
the unchanged host/guest/final receiver must recheck them and the child. Process
launch integration is root-owned and separately selected; these source files
must not autonomously start an unbounded Lean/prover/network workflow.

## D22 new external-owner acquisition

`authoring/module_dependency.py` closes the unselected-owner structural seam
without changing frozen transport or admission. `ModuleDependencyAcquisition`
retains the same workflow/session/verifier, stores, adapter, profile, expiring
contact objects and aggregate budget. Its `prepare(provider,module,name,cap)`
copies the exact address before await, validates opening/address/namespace,
commits and reads back custody, and keeps a bounded immutable local selection.
This is untrusted data, with no feature extraction or discovery-candidate entry.

The owner explicitly acquires an offered receipt using existing workflow calls.
`admit(module,name,entry,operation_directory,**limits)` uses only the retained
opening and the existing real same-budget ReceiptAcquisition.admit, then reads
back the exact receipt bytes and calls ImportSession.use_handle/open_group.
It checks predictable module/receipt/call/data capacity before expensive work.
A late session-selection failure revokes the entire originating verifier,
including earlier imports; structural custody and paid costs can remain. No
new close owner, provider traversal, retry, source execution or renewed budget.
Already-selected modules use DependencyAcquisition instead. Returned JSON is
not transferable acceptance; only the live verifier/session retain authority.

Six changed-boundary controls actually pass and are independently audited at
module-dependency-controls01, selection927f60ee189aa95a769982d18f5bee8e318eeb596cde160681eb3477e318958c.
No old passing suite was repeated. No positive receipt/handle or cryptographic
success was fabricated; these are structural/refusal controls, not the required
genuine admitted external-owner and source-derived-child endpoint. Used source
and test bytes stay frozen. See DECISIONS/ASSURANCE for exact results and costs.

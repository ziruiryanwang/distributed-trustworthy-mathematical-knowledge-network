# CP-001E: independent V2 client, advisory and custody-integration audit

Date: 2026-09-20  
Status: Completed bounded independent review; reported R1–R5 concept findings resolved at the recorded final revision  
Method: Complete V2 read, cross-document schema/interface checks, and paper counterexamples; no code, executable model, native proof execution or benchmark

## Reviewed boundary and independence

This reviewer read the complete [integrated V2 specification](../../spec/OPERATIONAL-CORPUS-V2.md), concentrating on Advisory2, REUSE1, FIND_WINDOW, Native2/NET2 reference boundaries, and custody integration. V2 is authored by the root agent, so this is an independent review of that integration. The reviewer compared it with relevant frozen mathematics/network/organization definitions and the [agent reuse/discovery proposal](../analyses/CP-001E-agent-reuse-and-discovery.md).

The reviewer authored the reuse proposal and [custody contract](../analyses/CP-001E-custody-contract.md); this audit is not an independent endorsement of those authored designs. The network author separately reviewed custody's partial-release/ownership repair. Frozen CP-001D was not edited.

| Recorded input | SHA-256 |
|---|---|
| V2 integrated contract, initial read | `a7fd9eb3bf55d46caf1edf10f986099bf7ba7f7f0d1867bd4c441139bc893a09` |
| V2 client/advisory re-read after first grammar repairs | `4a55f9bfb5698e1e0116ad127999cbb424ee672a62144cd8e3b64f91118862e4` |
| V2 client/advisory re-read after final requested repairs | `1572ccfa3a4309e41c2db2c3d7267326ec7512c67ed2e5f4e2cf082d1e4a689c` |
| Reuse/discovery proposal | `0525e8dd334b0ea6f0b6ddf099d9a42a2a6a06afefab370f9d403502318796b0` |
| Custody contract, independently cross-reviewed repair | `914e2c9ab6fb41f4927aaa7ca03646d38876d2708e7feb1956caf23af99893b2` |

These hashes identify inspected revisions, not a blanket approval of future bytes at the same path.

## Main disposition

The integration preserves the essential truth boundary: advisory labels, matches, routes, scores and receipts cannot establish a native theorem. Exact checked application remains separate from incomplete argument matching, and durable local custody remains separate from remote service promises. No new human-intention record, mandatory goal, or research scheduler appears in the reviewed design.

Several selected wire/client semantics were underspecified in the initial V2 revision. The independently re-read revisions resolve the explicit continuation, structure-field, binder/rewrite, foundation/contact and aggregate-validation findings. No further concept blocker was found in these bounded client/advisory/custody-integration boundaries. This is not source-to-code correspondence, kernel soundness certification or a deployment approval.

## Concrete findings

### R1: FIND_WINDOW lacks an encoded continuation entry point

Severity: material wire-operability gap. Status: resolved in the first re-read revision.

The selected request is `[predicate,snapshotSelector,startPosition,pageCeilings]`. Its snapshot variants are current view or a live snapshot token; its start variants are BEGIN or a caller-chosen descriptor boundary. The text then specifies a holder-bound authenticated continuation, but does not say where that continuation appears on a later call or whether an existing variant means it.

A snapshot token and a scan continuation are not interchangeable by inference. The continuation additionally binds original window start, next unprocessed position, exact predicate, extractor/planner/base list, and holder/deadline. A client that merely sends the next public key as a new seek has not submitted that authenticated continuation. It might still obtain useful data, but cannot call this the stipulated exact continuation operation without the missing contract.

Required repair: choose one precise tagged resume variant or explicit optional cursor field, fix permitted combinations with initial-seek fields, and retain the original finite snapshot deadline. Do not let the resumed request alter its predicate, planner, original start or next position. Each continuation remains a fresh paid call. Wrong-holder/stale/tampered/mismatched cases must give explicit noncontinuation, not restart at a convenient current snapshot.

Verified disposition: `startPosition=[2,continuationToken]` is the selected resume variant and requires `[1,liveSnapshotToken]`. Holder, query, extractor/planner, original boundary, next position, retained snapshot and expiry must agree. The spec names explicit stale/mismatch outcomes and disallows using the current-view selector to reinterpret a continuation. This resolves the missing wire entry point without widening authority.

### R2: Advisory2 field hints need a single exact native field convention

Severity: material client interpretation gap. Status: resolved in the first re-read revision.

Tag 2 names `[GroupID,typeIndex,classHint,fieldLabels]`; each field entry names only `fieldIndex`. A general inductive type can have several constructors with different field telescopes. In that case one integer does not select a unique field. The statement that it must refer to an existing native field does not select which constructor or how parameters are treated.

Minimal repair: require tag 2's field-bearing target to be an exact checked one-constructor structure/type accepted by the native projection route, with fieldIndex interpreted exactly as that route's `Expr.proj` index after its parameter convention. Alternatively a different grammar could name a constructor explicitly, but this would be an additional feature. Fix field-label ordering and duplicate-field semantics; a sorted list with unique field indexes is a simple initial choice. Duplicate full entry prohibition alone does not resolve two labels for the same field inside one entry.

Class membership remains local search metadata. Passing this check must not install a new native declaration or alter the checked constructor telescope.

Verified disposition: tag 2 now restricts to exact checked one-constructor non-indexed native structures, adopts native projection field numbering after uniform parameters, and requires strictly increasing unique field indexes checked against the generated constructor. Actual projections still check at their concrete context/universe instantiation. The restriction is a deliberate initial convenience limit, not a rejection of more general native mathematics.

### R3: Binder hints and rewrite orientation need exact interpretation

Severity: client interoperability/refinement gap. Status: resolved after the final requested repairs.

The binderInfoCodes array is bounded but not explicitly mapped to binder positions. For a checked constant with a dependent Pi type, select whether a list of length m annotates the first m outermost Pi binders of its reconstructed constant type, including any abstracted Judgment context. State what missing suffix positions mean. Select a bounded syntactic or explicitly fuel-bounded unfolding rule; a metadata-length check must not invoke unbounded conversion.

The rewrite tag gives orientation 0/1 but not which value means left-to-right. A checked theorem can also have a Pi telescope before its equation, and an English relation label is not the kernel's Eq constant. Select forward/reverse meanings and require the exact foundation's checked equality head after the permitted bounded telescope exposure. Any actual instantiated dependent transport still passes native checking. Missing assumptions or instantiations remain residuals, never new implicit axioms.

Verified first-revision disposition: rewrite direction 0 is left-to-right and 1 right-to-left; the post-telescope/Pi conclusion must have the exact admitted seed Eq head after bounded conversion. Failed or budget-limited normalization does not activate a rewrite. Binder hints now address consecutive outer Pi binders from position zero with an explicit/default suffix. Requested final wording retains rejection/nonactivation when more codes are supplied than available syntactic binders and states that a Judgment's abstracted local context belongs to the reconstructed constant type.

Verified final disposition: the prefix count is explicitly bounded by available syntactic consecutive outer Pi binders of the reconstructed constant type, including a Judgment's abstracted telescope. Excessive lists cannot activate; no unbounded normalization is needed to discover additional Pi positions for this hint.

### R4: Advisory foundation and contact grammar should be explicit

Severity: exact-binding/interoperability refinement. Status: resolved after the final requested repairs.

LibraryViewPage and CollectionGuidePage each contain a FoundationID, while targetRefs can refer to seed indexes or content-addressed declarations. Explicitly require every activated target/interface to resolve under that page's exact qualified foundation; seed indexes must use only its frozen seed table. A page headed by foundation A with an object from foundation B is not a checked alias in A merely because B is also locally available. The native mixed-closure prohibition is not itself a complete advisory-page reference rule.

The frozen network has both simple bootstrap contact items `[nodeKey,endpoints]` and richer route records `[nodeID,endpoints,nativeProfileIDs,indexKeys]`. Calling a guide contact the NET2 bounded public-contact grammar should select the exact one and inherited field limits, not leave two array shapes plausible. Contact validation remains inert; every connection or route query needs separately authorized local work and no recursive following.

Verified first-revision disposition: every resolved target/interface/replay hint must use the page's exact FoundationID; seed refs use only that foundation's qualified export inventory. A mismatch keeps the entry inactive. The contact-array choice remains the independent small wire-grammar refinement.

Verified final disposition: guide contacts use exactly the richer GET_ROUTES four-element record, with inherited endpoint/profile/key bounds, disclosure and separately authorized connection rules. The simple offline-bootstrap shape is explicitly not this field's grammar.

### R5: Aggregate bundle validation must be distinguished from lazy page receipt

Severity: bounded-admission clarification. Status: resolved after the final requested repairs.

Manifest length totals can be checked before member fetch from its declared payloadLength entries, using overflow-checked addition. The 4096 aggregate advisory-entry limit cannot be verified from that manifest alone: entry counts are inside member pages. A manifest may individually satisfy 1024 members/8 MiB while its member pages collectively exceed 4096 entries.

The limits are explicitly stated, which is good. Select the lifecycle: for example, hash/schema-checked individual pages can be staged/displayed as tentative, while full-bundle conformance is asserted only after actual lengths and all entry counts are checked. A lazy client must not label the unseen remainder conforming. Alternatively partial per-entry activation may have a separately bounded, explicitly partial admission status, but it cannot imply global bundle validation. Provider public-bundle activation should already validate the complete declared bundle and authorize every listed member. None of these checks requires importing all referenced mathematical proofs.

Verified final disposition: the provider validates every member before public disclosure activation. A receiver stages partial data as tentative, then checks every actual member length/hash/type/page schema plus aggregate byte/allocation and entry counts before declaring the bundle conforming or activating entries through it. This requires bounded advisory metadata acquisition only, not all referenced theorem closures. Failed/abandoned bundles create neither semantic activation nor free persistent retention. An independent bounded cache can retain already checked data without upgrading its status.

## Positive checks and their limits

### A1: The advisory grammar fits the canonical CBOR subset

Arrays, numeric tags/counts and byte strings suffice for all proposed record shapes. classHint is the numeric 0/1 enum, not CBOR false/true; orientation is numeric. Optional replays use explicit empty/singleton arrays, not null or omitted fields. Labels use byte strings rather than CBOR text. Typed IDs retain their usual exact encoding. Unknown member kinds, nested manifests and native records are excluded from the manifest membership grammar.

Codec/display qualification should include strict UTF-8/Unicode-scalar conformance vectors and a fixed forbidden bidirectional-formatting/control set implementing the stated exclusion. Invalid UTF-8, surrogate encodings, overlong encodings and markup are not a new instruction language. The core rendering rule already requires escaping and exact-ID fallback on ambiguity. This is a presentation/data-validation qualification, not a claim that sanitizing text proves mathematical truth.

The new organizational type numbers are distinct from the native and network ranges. No inspected frozen registry allocation conflicts with 0x8120..0x8122. Future registries must preserve that separation.

### A2: Per-entry activation is a useful and safe separation

Schema/hash-checked receipt can support visibly untrusted display/routing without importing every mathematical object in a guide. Semantic activation requires that entry's exact checked target and current policy; one entry does not activate its neighbors. A replay hint is not an accepted witness selection. Class or rewrite search is bounded and cannot install peer executable code.

The explicit application condition is appropriate: actual arguments check against sequentially instantiated dependent types, and the resulting application/transport checks against the claimed local result. A proposed substitution with open metavariables is not CHECKED_LOCAL_APPLICATION. An unfamiliar structure representation needs a checked adapter; independently generated identical canonical group descriptors can deduplicate.

### A3: Data traversal does not silently become generic content-addressed access

The negotiated manifest hints are at most four. Scope `[2,manifestCID]` includes that exact manifest plus only its explicitly listed typed member pages, not target theorems, checker materials, other bundles or private operational records. BUNDLE1's separate 256-item/16-KiB request and 4-MiB payload ceilings apply even though the full advisory bundle may be 8 MiB. Large pages/bundles therefore need separately admitted bounded range calls; aggregate cache/traffic/work ceilings remain in force.

The count/byte ceilings are conjunctive, not guarantees that 1024 maximal pages fit. For example, the 8-MiB bundle bound precludes 1024 one-MiB members. The manifest remains at most 64 KiB and cannot list itself recursively. Native target reads need their own explicit public-root or export scope. Paid receipt, signatures, or membership never imply native acceptance or remote permanence.

### A4: Window discovery does not claim completeness or uniform sampling

The provider-public ordering avoids exposing private assessment-ID order. An exact arbitrary lower boundary can avoid repeatedly obtaining one prefix, but END applies only to the named suffix and snapshot. A matching row that cannot fit stays unprocessed. A time-truncated scan is not an empty complete answer. New windows and cursors do not extend the original finite snapshot lifetime.

The reuse proposal correctly says rotating hash-space starts are not uniform sampling of stored records. The integrated specification does not overturn that qualification. Exact-ID queries and ordinary STRUCT1 remain usable baselines. The final revision explicitly leaves STRUCT2/learned lanes optional research/client extensions: it does not instantiate an interoperable ExtractorID from a suggested feature budget. Public negotiation requires the exact versioned token/extraction/normalization/truncation contract first. This preserves the baseline without inventing an implicit common STRUCT2 schema.

### A5: Custody integration preserves the local-only boundary

V2 does not create a new wire promise of permanent preservation. The linked contract distinguishes exact original replay retention from same-JudgmentID recovery via another independently checked complete proof. A changed foundation usually changes the exact target identity; an old affected acceptance is not inherited.

The selected allocation is owner-release-required, with separately finite work budgets. Work-budget expiry can stop maintenance without silently making owned roots garbage. Handoff is only a finite independent acquisition/check/activation process plus limited observations, not proof that the destination will store forever.

The first custody draft had a concrete partial-release defect. The network author found it; the repaired contract adds per-target ownership and localCustodyID bindings. That author then independently re-read ownership, replacement/release, maintenance and status at the recorded custody hash and reported no further blocker in those boundaries. This reviewer records that disposition without calling its own authored custody note independently approved by itself. Crash/durability behavior remains unimplemented and unqualified.

## Required adversarial paper/conformance cases

- Initial FIND_WINDOW seeks into a gap; its next paid call submits the selected explicit continuation variant and cannot change the predicate or original start.
- A matching descriptor exceeds the remaining page space; resumption returns or reconsiders it rather than skipping it.
- A guide tries to reference a second advisory manifest or a private custody record; the first advisory scope cannot serve it.
- A valid manifest declares pages whose checked counts exceed 4096; the receiver never asserts full-bundle conformance and stops within its aggregate allowance.
- A label contains invalid/overlong UTF-8, a bidirectional override, or markup; it is rejected or safely displayed according to the exact label grammar, never executed.
- Foundation A's page names a seed index meaningful only in B, or an object genuinely bound to B; activation in A fails rather than reinterpreting it.
- A field hint names a multi-constructor type or an out-of-range native field; it remains unactivated/rejected and cannot create a projection.
- Binder metadata hides a required law premise; the final explicit application still exposes the unsatisfied premise.
- A rewrite candidate is conditional or reversed; each actual instantiation/transport is checked and finite, with no missing condition silently accepted.
- A release races with custody maintenance/replacement; exact ownership version checks prevent reacquisition by a stale job and preserve independently owned shared roots.

## Qualification boundary

This is a paper-level integration audit. It does not reproduce the new kernel fixes, execute the selected bootstrap, verify codecs, test client extraction, or measure discovery utility. The new v4.34 candidate and its ABI/bootstrap/checker route still need the separate stated qualification. Actual reciprocal usefulness and affordable preservation require demonstrated end-to-end checked applications and sustained funded service; no grammar or index alone proves exponential useful growth.

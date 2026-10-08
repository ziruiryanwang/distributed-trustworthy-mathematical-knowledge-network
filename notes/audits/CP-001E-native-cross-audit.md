# CP-001E: native-scaling and adjacent mathematical cross-audit

Date: 2026-09-19. Status: bounded independent paper review; no code, exploit execution, native replay, build, or performance/reliability experiment. Frozen CP-001D artifacts were not edited.

Disposition update: 2026-09-20, after P1/P3 reread and the separate foundation-source cross-audit.

Reviewer scope: native identities/evidence and incremental verification, followed by targeted review of the root preservation argument, the exchange inventory, and the agent-reuse mathematical interface. This is not a complete audit of every operational field in those notes.

## Reviewed materials

- [Native scaling amendment](../analyses/CP-001E-native-scaling.md), authored by this reviewer and subjected to the local checks recorded below.
- [Preservation over unbounded time](../analyses/CP-001E-preservation-over-unbounded-time.md), probability/CTMC/capacity sections read in full.
- [Exchange scaling](../analyses/CP-001E-exchange-scaling.md), targeted EXPORT_HEAD2 inventory/closure/authority review.
- [Agent reuse and discovery](../analyses/CP-001E-agent-reuse-and-discovery.md), targeted identity, contextual application, and optional LibraryView review.

## Preservation mathematics

### Finite repaired-copy chain: checked argument

The finite-state chain has loss rate kλ from k copies and repair rate μ from positive k below r, with zero absorbing. λ and μ are finite positive rates. From any positive k, the event that the next at most r actual jumps are sufficient losses without repair to reach zero has positive probability. A finite minimum over positive starting states is therefore some δ > 0. The probability of avoiding absorption through m such jump blocks is at most (1−δ)^m. Every holding time before absorption is almost surely finite; bounded finite rates prevent explosion. Hence absorption occurs almost surely over an unbounded time horizon under this stationary finite-redundancy model.

This is a valid conditional countermodel to unconditional permanent survival, not a measured hazard estimate and not a statement that every conceivable repair process has this stationary law.

### Expected hitting time: checked equations

For 1 ≤ k < r, first-step conditioning gives

\[
-1=k\lambda(T_{k-1}-T_k)+\mu(T_{k+1}-T_k).
\]

Writing Δk = Tk−Tk−1 gives kλΔk−μΔk+1=1; at r, Δr=1/(rλ). This reproduces the note's recurrence. For r=3,

\[
\Delta_3=\frac1{3\lambda},\qquad
\Delta_2=\frac1{2\lambda}+\frac\mu{6\lambda^2},\qquad
\Delta_1=\frac1\lambda+\frac\mu{2\lambda^2}+\frac{\mu^2}{6\lambda^3}.
\]

Summing gives the stated 11/(6λ)+2μ/(3λ²)+μ²/(6λ³). Units are time. In the μ→0 limit it is H₃/λ, the correct mean time until all three independent exponential lifetimes have failed without repair. No error was found in this recurrence or simplification.

### Conditional loss budgets: checked bound and one wording finding

If the conditional first-loss hazard in interval t is bounded by εt on every surviving history, then P(first loss in interval t) ≤ εt. Summing first-loss events proves the stated upper bound without independence across intervals. The 6ε/(π²t²) allocation sums to ε. Under the additional bound q raised to rt, the sign and ceiling in the logarithmic replica target are correct for 0<q<1 and a nontrivial target 0<ε<1.

Finding P1: the reviewed sentence that per-root allocations “must also be summable” is too strong if read as a universal necessity over all possible joint failure models. Counterexample: every root's loss is the same common event A with P(A)=ε. Each root has risk ε, their sum diverges, but the probability of any-root loss is ε, not one. This does not justify actual common-mode reliability; it refutes the universal logical necessity claim.

Requested repair: summable per-root budgets suffice, and are the selected way to obtain a useful all-roots bound from individual risk budgets using the union-bound method. Non-summability alone supplies neither that bound nor a theorem that loss occurs. Stronger joint models can support different statements. The reviewer reread the complete revised preservation note at the final hash below. P1 is repaired: it now explicitly confines the summability method to a sufficient marginal-budget union-bound construction and gives the common-event counterexample.

Finding P3, raised in the parallel review, is also repaired and independently reread: zero is absorbing only in the model with no outside archive, alternative proof, reconstruction shards, or rederivation source. Loss of one exact ReplayID's evidence is not identified with irreversible loss of its judgment. The selected custody target remains exact selected replay evidence; an alternative proof needs its own newly admitted replay and does not silently fulfill an exact-byte promise. The risk schedule now explicitly states the nontrivial range 0 < ε < 1. No error was found in these repaired statements.

The custodianship/capacity distinction is otherwise appropriate: native truth, locally protected reuse, observed replicas, and active preservation authority are not equated. Finite storage with an unbounded stream of retained independent bytes requires continuing capacity or release/representation changes.

## Export inventory: exactness sound, incremental layout defect

The reviewed EXPORT_HEAD2 correctly distinguishes a full native-object inventory from the native witness map. It includes actual terms, declarations, profiles, replay metadata, and native trie pages. Its inventory nodes are outside their own leaf set, preventing a self-commitment cycle. Its export capability authorizes exact reachable inventory pages plus the exact listed native objects, not arbitrary CAS content. Independent native reachability/equality checks remain necessary; counts alone are not completeness evidence. These interface choices agree with the native amendment.

Finding N1: the initial deterministic packing into full consecutive 2,048-entry leaves, grouped into full 128-child branches, is not incrementally persistent under ordered insertion. Adding one CID near the front shifts leaf boundaries throughout the suffix. Almost every suffix leaf gets new contents/hash even when all old native objects are unchanged. A root with N inventory entries can therefore require Θ(N) rewritten inventory bytes for a single small addition. Repeated growing exports can recreate Θ(N²) metadata; a random insertion-position model gives the same suffix effect in expectation. This is not repaired by merely content-addressing the packed pages.

Requested selected repair: use a canonical persistent key-prefix map from exact native CID to payload length under separate operational node types, or explicitly account for the linear per-export rebuild instead of claiming incremental cost close to new bytes. The exchange author selected the persistent key-prefix repair. The reviewer reread the final EXPORT_HEAD2 section at the hash below and confirms N1 is repaired: it uses operational type 0x8020/schema 1 with the fixed 37-byte exact key, canonical binary Patricia partitions, and bounded node grammar. Its O(kL) update bound is conditional on independently established exact deltas and locally verified old subtrees. Counts and payload totals are verified local summaries, not publisher authority.

The replacement openly charges 2N−1 inventory nodes for N native objects and counts native plus inventory objects in cold transfer, rather than retaining the withdrawn 517-page packing example. It also acknowledges O(L²) downstream inventory work for O(L) changed native map nodes and complete cold derivation when needed. The exact native/inventory read-scope separation remains intact. The native witness map is still not treated as a full inventory.

## Agent reuse: distinctions checked and one wording repair confirmed

The note correctly distinguishes aliases from changed native definitions, definitional conversion from content identity, and actual dependent application from approximate relevance. Its optional LibraryView contains inert local conveniences, not macros or executable peer authority. Instance/rewrite activation is locally bounded; actual instance values, rewrite proofs, argument substitutions, and residual-premise witnesses remain subject to native checking. Remote view distribution requires a separate reviewed capability rather than an invented native CAS permission. The no-intention/no-public-unsolved-task boundary is preserved.

Finding O1 was initially a wording issue: independently generating isomorphic source records does not by itself imply distinct GroupIDs. Name-neutral identical canonical group descriptors can deduplicate. The author changed the table to different native descriptors representing isomorphic interfaces, and qualified the MonoidLike example with genuinely distinct GroupIDs due to fields/order/helper references. The reviewer reread and confirmed this repair. No open finding remains in this targeted interface portion.

## Exact witness and warm-cache requirements

The native amendment explicitly does not reuse an arbitrary existing Lean environment merely because it contains a theorem constant with the same JudgmentID-derived name. If an old environment installed proof A but the selected replay chooses proof B, a literal-environment-B receipt would be false without additional work. The selected baseline branches/reconstructs a compatible environment under exact selected witness maps. It does not silently invoke proof irrelevance to reuse A's footprint, environment, or cost as B's.

Receiver-owned native certificates bind exact typed root, selected witness-map root, FoundationID, checker image, adapter/decoder, interpretation-view mapping, and semantic options. Current permission and availability are separate guards. Root-proof map equality includes the root's own selected proof; compatible child-map unions reject equal-judgment conflicting proofs. A missing or foreign acceptance flag is never a local certificate.

SemanticContext2 contains only exact statement-direct refs; proof-only dependencies are selected through replay and cannot be smuggled into the statement context. No flat declaration manifest is required: exact declaration closure is derived from native references plus the selected witness map, with no-missing/extra witness equality and grounding checks. Existing CP-001D IDs are not rewritten or silently reinterpreted.

The relevant-guard current-use amendment keeps a final local linearization boundary. It does not reuse an old positive state as current merely because its native proof still checks. Missing incident-journal coverage requires complete re-establishment or UNKNOWN; broad unresolved incidents trip a conservative breaker before descendant repair. Unrelated positive imports need not invalidate every mathematical certificate or force a global-epoch retry.

The exchange reviewer requested an explicit support-summary coverage clarification, now applied in the native note: incident clearance includes every binding-relevant native closure identity, including Replay/root records, proof/term/foundation objects and native map/set pages, not only declaration IDs. A collision or decoder incident on a trie node cannot be incorrectly cleared by a declaration-only summary. Locally derived summary corruption is guarded separately and never justified by a self-referential content set.

The source-security review also led to a Native2 fixed-width/ABI table. Projection indexes must fit u32 and the actual qualified structure field bound; every native index/count/length conversion is checked for exact representability and semantic bounds. Arbitrary-precision mathematical values remain distinct from machine indexes. Raising a resource allowance cannot authorize host-dependent truncation. A computed dangerous arithmetic operation can still fail; isolated failure is mathematical nondecision with diagnostics, never an invented ACCEPT or a theorem of falsity.

## Foundation-security qualification

The root's parallel source audit reported post-v4.22.0 kernel fixes relevant to native universe/projection and nested-inductive paths. A subsequent [independent foundation-source cross-audit](CP-001E-foundation-cross-audit.md) by this reviewer verified selected old/new source differences, release backport ancestry, corrected issue scope, and the pinned Lean4Lean proof-coverage limitations. No exploit was executed. That separate audit binds its reviewed root security-note hash and its bounded source scope; the [foundation security audit](../analyses/CP-001E-foundation-security-audit.md) owns the corrected source selection and requalification decision.

The native-scaling note now explicitly treats v4.22.0 as historical, not deployable merely because it was pinned. FoundationID is abstract over an explicitly selected qualified native foundation. Efficient exact hashing, persistent maps, source-independent checking, or warm caches cannot compensate for an unsound native kernel. Relevant checker/foundation changes must invalidate their corresponding native certificates and current reliance guards.

## Hash-bound reviewed revisions

These identify reviewed drafts, not a claim that later sibling edits have already been reviewed. The parent checkpoint must record final revisions. P1, P3, N1, and O1 have been reread after repair.

| Target | Reviewed SHA-256 |
|---|---|
| Preservation note, including P1 wording | `56BF53D9C924165FA79234267AF21F9D36D58782DC8EBAAFDEEAF8DD295EFDBF` |
| Preservation note, after P1/P3 repair and full reread | `0E90487F0654D1CF10E4175F0031EB376706CD5BBF5EE7E34779BAC02A0ACC25` |
| Agent-reuse note, after O1 repair | `295F383DAF99C03FEBB8FBB7F3123C3BEBD1902A9737AF285081AC589B942B03` |
| Exchange note, after N1 persistent-inventory repair | `55CF17DB72FE9EE735D27E390C78D2EBBC66251DA62BF8EA8F0D51E75764DDE2` |

## Disposition

The finite-state reliability calculation and conditional per-interval bound pass this paper review. P1's universal-necessity wording and P3's exact-replay/judgment-loss distinction are repaired and reread. The native/data-plane scope relation passes its targeted exactness review, and N1's incremental inventory layout is repaired and reread. O1 is repaired and reread. Native cache/environment binding, exact incident-support coverage, fixed native-width interpretation, and the foundation-security gate are explicit obligations, not empirical performance or release qualification claims. No frozen CP-001D artifact was changed.

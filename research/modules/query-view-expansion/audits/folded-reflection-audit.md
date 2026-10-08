# Independent folded-reflection policy audit

Date: 2026-09-20. Reviewer: `folded_reflection_audit`. Status: exact-cut concept review; no blocking contradiction found in the assigned feature, application and joint-budget scope. This is not policy selection, implementation qualification, native execution or empirical usefulness evidence.

## Reviewed cut and scope

The reviewer read the complete [folded-reflection policy](../folded-reflection-policy.md) after the integration owner supplied its held hash, and independently recomputed that hash. The author held the source unchanged during review. This audit owns only this new file; it does not edit the source, frozen J or prior audits.

| Artifact | SHA-256 read |
|---|---|
| Folded-reflection policy | `7C156479F372B7AAE53CC266DCC0CDC382F8E042BD190D041AD515A4AC3E2E45` |
| [J / VIEWS1 proposal](../proposal.md) | `2AC5045E20F9B44198BEFBB1048987132A3E7AB2F3DEF08B6AD0695DBBF467A2` |
| [STRUCT2](../../../../notes/analyses/CP-001G-structural-retrieval.md) | `1F295806C580224811C10A0A8273A53D35C0FDDC7D8085EBC5F9F224F47CDDCA` |
| [PI1](../../../../notes/analyses/CP-001G-proof-instance-composition.md) | `0E1D443FBF13727A0011BD101135BAADD79F48074137B90E5CC2FCAF63A34E3E` |
| [BRIDGE1](../../../../notes/analyses/CP-001G-interface-bridges-and-applications.md) | `99804AE611C9B84E5B69806714B1218A993F837A5D33A7346AEE0024AA83AC3B` |

The combined review covers literal feature exposure and query lifting, actual proof-instance application, context/universe restrictions, candidate ordering, shared counters and the claimed finite successful/defeating paths. Relevant inherited sections and J's existing feature/application audits were read; this is not a fresh audit of every earlier network, storage or kernel contract.

Only document/source inspection, hash calculation and paper arithmetic were performed. No implementation, extractor, executable model, Lean elaboration, native import/replay or benchmark was run.

## Literal feature route, without a name oracle

The semantic map reference is exactly `[1,DefinitionID]` or `[4,OpaqueID]`. Thus the requested feature payload is `[6,0,f_ref]`, not `[6,0,[0,f_ref]]`, not a JudgmentID and not a proof-instance reference. STRUCT2's tag 6 takes a constant reference, whereas its HeadAtom grammar belongs to different payload positions. The selected native query has mode 0 / APPLY_RESULT and no pattern. The direct-broker query's absent target filter is correctly distinguished from a native pattern field.

The closed query `Pi x:B, Eq A (f x) (f x)` requires no inhabitant of B. Its only fresh variable is explicitly bound. This policy first checks f/h and their actual types, so its formation uses a checked map, unlike an unqualified header being treated as a declaration. Query construction still costs local resources and needs disclosure admission.

After the single Pi is peeled, the terminal equality contains the rigid role-0 references A and f, with repeated f occurrences coalesced. Eq itself is excluded by the tag-6 emission rule. Under completed extraction, these at-most-two terminal-reference tokens precede any role-1/role-2 copies from the Eq operands because terminal focus precedes operand foci. Therefore the four-reference lane includes the role-0 f token. It does not need to borrow unused slots from the conclusion, input/output or domain lanes. Beta/zeta companions of this short syntax add no new constant identities.

For the favorable stored type, `I.{v_I} B A f` is already terminal: the judgment has no stored context and the conclusion has no leading Pi. Its at-most-four distinct rigid terminal references are I, B, A and f. The fixed four-reference lane includes their tag-6 tokens when relevant inspection, feature generation and descriptor construction complete. Repeated raw/normalized occurrences coalesce. Fixed universe vectors are not tag-6 constant-reference tokens. No B-domain token is manufactured from I's uninspected body.

This is a real addition to the narrow J route: a folded r can be absent from the B-domain lane while present in the existing f-reference lane, and the client learns f before computing that lane. Neither I nor r is an initial answer identifier. The result is conditional on the literal retained type, successful extraction, public index coverage and consulted-prefix position. It does not apply to arbitrary equivalent wrappers, generic carrier/dictionary parameters, truncated feature output or unavailable providers.

An absent pattern is essential to the specified use. The query proposes a reference-based candidate search; the returned r is not asserted to prove the reflexive query equality. Requiring whole-query pattern agreement would introduce an unsupported extra restriction on folded r. Token membership itself establishes neither injectivity nor even applicability.

## Source observation and what it cannot establish

The reviewer independently fetched the exact pinned [Lean `src/Init/Data/Function.lean`](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/Data/Function.lean#L51-L54), receiving HTTP 200. Namespace Function begins at line 13; lines 51–54 contain the displayed `Injective` definition and equality-reflection body. This corroborates the source-level motivating example.

It does not establish an exported content ID, the native universe-parameter ordering of I, the actual retained form of a particular theorem or successful source-to-content reconstruction. The policy correctly puts those facts in the favorable representation premise. In particular, a closed zero-universe theorem may refer to a polymorphic I at an explicit fixed universe vector. Zero universe arity of r is not permission to erase I's vector.

The source's implicit-looking a₁/a₂ binders are actual native function arguments. No remote binder annotation, source spelling, reducibility registration or class extension becomes authority. Complete qualified native conversion, not the source read, decides the trial.

## Exact reflection application

The recovery gate permits only a theorem whose stored judgment context is empty, declaration universe arity is zero and conclusion is closed. It does not require that the conclusion syntactically looks like injectivity. A closed conclusion can itself contain leading Pis; the valid-but-irrelevant second defeating candidate uses this fact.

For a qualified chosen instance p_r, PI1 reconstructs its checked witness constant at the closed target type. Consequently `[2,[7,ProofInstanceID(p_r)],[]]` is the appropriate WitnessTermDAG constant node. A semantic `[2,JudgmentID]` reference is not allowed in that witness subgrammar. Empty r context means no hidden preliminary telescope arguments, and zero r universe arity justifies the empty level vector on this witness occurrence.

In the body of `lambda x:B, lambda y:B, lambda e:Eq A (f x) (f y), w(p_r) x y e`, the bound variables x, y, e have indices 2, 1, 0. In e's domain, before e is bound, x/y have indices 1/0. Three ordinary application nodes supply those exact arguments. These indices agree with the proposal; no residual term, unspecified universe or inferred class argument is smuggled into the construction.

The trial must check at the entire reflection type. A successful proof of r's own proposition is insufficient. For example, a checked r at `Eq (B -> A) f f` is legitimate mathematics, but its proof constant has an equality type, not the function type needed for three applications. Rejecting that *trial* does not reject the true theorem or its usefulness elsewhere.

For the stipulated transparent I with the checked injectivity body, ordinary conversion can expose the x/y/e function type. The resulting checked R_r supplies exactly the missing reflection used by BRIDGE1. Its evidence, actual footprint, realization and current-use guards must agree with f/h and the eventual image application. Same statement identity alone cannot establish PI1 compatibility. Extra rebuild/recheck work is explicitly charged; no different witness environment inherits a usable flag automatically.

The forward lifts are deliberately only candidate terms until the final original-type check. No standalone lift check is selected. The final expression combines the checked image equality with lifts and R_r, and only its successful native check in the original Gamma yields `CHECKED_LOCAL_APPLICATION`. No public wrapper, theorem publication or protected custody follows automatically.

## Joint schedule and resource arithmetic

The replacement policy is not silently called conformance to unchanged J. It selects one pair and one view, initial h-only nomination and a separate recovery lane. It cannot gain additional r trials from initial helper rows or fallback to a second pair after the chosen one fails.

The numeric envelopes compose as follows:

| Counter | Independent arithmetic/check |
|---|---|
| Candidate pages and decoded rows | `2 + 2 + 2 = 6` pages; at most `6 * 64 = 384` rows before lower byte/work limits |
| Retained lane slots | `16 + 8 + 8 + 16 = 48`; repeated cross-lane descriptors remain conservatively charged |
| Type probes | `4 + 4 + 2 + 2 = 12`; each retains the inherited 256-KiB/eight-attempt/512-node/depth-32 bounds |
| Direct full qualification path | f, h, r₁, r₂ and one image root give five starts, leaving at most three of the eight for additional actual qualification/reconstruction starts |
| Constructed proof checks | r₁ trial, r₂ trial, image application, final original-type proof give exactly four starts |

The direct five-start count is not an upper bound on every native operation needed in practice. A constructed check that also requires a new qualification/reconstruction start debits both counters. Closure, foundation and compatibility costs remain actual byte/CPU/memory work. None is made cheap merely by being grouped under one root.

Within the recovery lane, repeated delivery of the same descriptor cannot produce another selected trial. A descriptor already present in another lane may be considered in recovery, but consumes recovery's slot and selected probe/trial opportunity. Reused exact bytes may avoid actual transfer, not create uncharged extra search. An ineligible or incomplete first probe consumes its opportunity instead of licensing a third one.

The first matching image candidate is the only selected complete image-root attempt. A later failure cannot silently spend residual aggregate headroom on a replacement, generic fallback or second view. Lower grants, refused disclosure, missing source authority or uncertain recovery can stop sooner. All source negotiations, failures, retries, parsing and checking consume the same 256-attempt, byte, CPU, memory and time parent allocation. Existing exact invocation reconciliation is not a free restart.

This proves only consistency of the selected counter arithmetic under faithful inherited accounting. It does not prove that a cold foundation, the five native roots or all four checks fit the numerical resource supplies.

## Independently reconstructed successful and defeating paths

Take the stipulated distinct-record example and its checked mathematical evidence. Suppose the initial admitted prefix contains f/h, the f-reference prefix orders a true `f=f` theorem before a folded injectivity theorem, and the image prefix contains the A-associativity theorem. These are explicit finite corpus/order premises, not answer IDs handed to the client.

The client first discovers and qualifies f/h through B. It computes f's reference query and qualifies the first returned theorem. That theorem's exact reference feature is genuine, but its constructed reflection application rejects. The second theorem qualifies and its constructed reflection application succeeds through the checked I body. The client then discovers A-associativity using the already selected operation-pair token, assigns all three ordered A arguments to the corresponding f-images, checks that image application and checks the final lifted/reflected B-associativity proof.

Thus the false-positive trial, successful reflection trial, image check and final check use all four constructed starts. Five direct qualifications suffice only under the stated compatible-environment and resource premises. The failed trial is not erased from the cost denominator. No standalone lift check, explicit-wrapper publication or hidden third recovery probe was needed. This reconstructs a conditional nonempty successful path, not a claim of an implemented result or speed advantage over proving B-associativity directly.

For a separate ordinary defeat, put two true closed zero-universe judgments first in the recovery queue: `Eq (B -> A) f f` and `forall z:B, Eq A (f z) (f z)`. The first supplies no function argument; the second supplies only one B argument before reaching an equality proposition. Neither supports x, y, e in the required reflection application. Both can genuinely emit the requested f-reference token. The second type is closed despite its leading Pi and therefore is not filtered out by the empty-recorded-context restriction.

If both trials reject and a valid folded injectivity theorem occurs later, the procedure exhausts its two opportunities and stops before image work. The source, index and two earlier theorems can all be honest. The permitted result is a scoped missing-reflection observation with actual expenditure, not noninjectivity or mathematical nonexistence. This countercase refutes a general recall claim without contradicting the narrow success or native acceptance safety.

### Deliberate loss relative to J, even without crowding

The integration owner also requested an explicit check of the replacement policy's reverse comparison. The extractor argument confirms that this policy is not a recall superset of J.

Consider an ordinary explicit specialized reflection theorem with effective type `forall x y:B, Eq A (f x) (f y) -> Eq B x y`, represented with its binders in the legitimate judgment telescope and/or leading Pis. STRUCT2 reaches terminal `Eq B x y`; the terminal and Eq-operand foci contain B and variables, not f. The last-domain focus contains `Eq A (f x) (f y)`, but the tag-6 emission rule covers terminal and relation-operand foci, not binder-domain role 5. It therefore supplies no promised `[6,0,f_ref]` token even when extraction completes. Ordinary beta/zeta normalization does not change this example.

The same explicit r has inspected B domains and can carry J's B-domain token. Frozen J may discover and nominate it together with f/h. The replacement policy instead reserves initial helper nomination for h only; an initial r remains inert and is not given an extra trial. If the consulted corpus has only that explicit r and no suitable f-reference-lane reflection candidate, J can succeed while this replacement stops, even in an uncrowded honest corpus with enough resources.

This is an intentional heuristic tradeoff permitted by the proposal's explicit replacement boundary, not a safety finding or a request for an unbudgeted fallback. Conversely, the stipulated folded-only case is a route this policy can reach and J's selected explicit template need not. Neither policy has established recall dominance over the other. Selection or later empirical comparison must retain this distinction rather than describe folded recovery as uniformly improved J.

## Disposition and reopening boundary

No blocking contradiction was identified at `7C156479…` within this combined scope, under the inherited decoder/checker, accounting and qualified-reconstruction assumptions. No source repair was requested by this review. Selection remains the integration owner's decision.

Any change to the token role/reference grammar, query pattern, r context/universe gate, witness construction, lane reuse, pair/image choice or shared counters reopens the affected review. Mere replacement of the motivating source name cannot justify stronger mathematical authority or coverage.

The result is a source-grounded, finite local-policy hypothesis with a conditional successful path and a normal failure path. Actual retained folded artifacts, native interoperability, resource fit, independent runtime isolation/recovery, fixed-budget useful reuse and sustained growth remain unperformed qualifications. Nothing in this audit changes the project's active goal or authorizes execution.

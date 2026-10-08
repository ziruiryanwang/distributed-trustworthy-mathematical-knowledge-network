# Folded-reflection recovery: a bounded optional local policy

Date: 2026-09-20. Status: concept proposal for independent review, not an implemented, qualified or selected release profile. No Lean execution, native export/replay, executable model or measurement has been performed for this proposal.

## Scope and precedence

This policy asks whether one already discovered exact map can expose a reflection theorem whose stored type hides its quantifiers behind a definition. It changes a **client selection policy**, not mathematical acceptance, STRUCT2 extraction or the candidate-service wire contracts. There is no new index kind, opcode, remote search capability, mandatory publisher wrapper, common research goal or central service.

Inherit the input fragment, effective-type interpretation, paid type-probe mechanism, image matching, lift construction, native/PI1 acceptance, source scopes, current-use guards and uncertainty accounting of [J's VIEWS1 proposal](proposal.md). Explicitly replace its helper nomination and page/probe/check schedule by the schedule below: **one f/h pair, one image view, one map depth**, with a recovery stage before the image query. This is a separately reviewed optional policy; it is not conformance to unchanged VIEWS1. Frozen [J](../../../notes/checkpoints/CP-001J-unfamiliar-interface-entry.md) and its audits remain untouched. Unchanged native/network authority comes from the existing integration, not this local supplement.

The opportunity is narrow. J can find an explicit `f : B -> A` and preservation theorem h through B-domain features, but its selected helper matcher need not reach or recognize a closed theorem `r : Function.Injective f`. General [STRUCT2](../../../notes/analyses/CP-001G-structural-retrieval.md) already has an exact-reference lane; the missing choice is how a client uses that lane within finite resources. This is neither a soundness defect nor proof that other existing client policies cannot succeed.

## Primary-source observation and representation premise

At Lean commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`, [src/Init/Data/Function.lean, lines 51–54](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/Data/Function.lean#L51-L54), within `namespace Function` begun at line 13, defines:

`@[expose] def Injective (f : α → β) : Prop := ∀ ⦃a₁ a₂⦄, f a₁ = f a₂ → a₁ = a₂`.

The inspected preceding source has no explicit declaration of the inferred α/β universe parameters. This source read establishes the definition's spelling and body, not its exported native universe-parameter order, exact content identities, retained syntax or compatibility with a qualified foundation. None of those exports was performed. The ordinary mathematical application motivating this case is also documented in the [pinned bridge-source audit](../../../notes/audits/CP-001G-bridge-cross-audit.md).

For the favorable paper family, assume an independently checked native representation with these exact properties:

- B and A are J's closed rigid monomorphic `Type 0` carriers; f and h satisfy its explicit templates and actual qualified types.
- The reflection judgment has **empty recorded context and zero declared universe parameters**. Its closed stored conclusion is literally the short application `I B A f`, retaining the folded definition rather than a prepublished explicit reflection wrapper.
- I is a native transparent definition representing the displayed injectivity body. Write its full occurrence as `I.{v_I} B A f`: v_I is the actual fixed, closed universe vector in I's declared parameter order, with the required length. All referenced universe vectors are exact data of the checked representation; none is inferred from a source name. Zero universe arity of r does not require I itself to be monomorphic.
- Complete acquisition/checking includes the actual definition and all needed support. The local checker can validate conversion and the application below within the actual admitted resources.

The recovery *search* does not receive I's or r's identity. It does not delta-normalize untrusted headers, use a `Function.Injective` name oracle, infer dictionaries or synthesize universe instantiations. That source definition motivates the example; ordinary native checking decides whether any particular recovered candidate works.

## Exact deterministic episode

All queues use J's supplied contact order, then paid page order, then the service's canonical descriptor-ID order. Each stage uses the same at-most-two supplied contacts. No automatic crawl or new contact is selected.

### Discover and qualify one forward pair

Issue J's exact BINDER_DOMAIN token query, without a pattern, at most once per contact. Keep the first 16 eligible definition/opaque descriptors and first eight eligible theorem descriptors. Probe at most the first four of each lane, with J's per-probe limits. Match maps and h against J's existing exact templates; this replacement schedule uses initial helper probes to nominate **h only**. Other initial helpers remain inert hints, not extra reflection trials.

Choose the lexicographically first matching `(d_f,d_h)` pair. No second pair is admitted if that pair fails. Fully acquire and actually check f/h, their exact B/A/op_B/op_A types and compatible PI1 interpretation before proceeding. Header agreement alone is insufficient. The relevant environment and current-use guards must remain coherent through all later checks.

### Query using the discovered map reference

Write `f_ref` for f's actual semantic constant reference, either `[1,DefinitionID]` or `[4,OpaqueID]`. It is neither a HeadAtom nor a ProofInstanceID. Form the complete closed query type

`Q_f := forall x : B, Eq A (f x) (f x)`.

The fresh x is explicitly bound, not a guessed inhabitant or unsolved metavariable. Checked `B : Type 0`, `A : Type 0` and `f : B -> A` establish this query's well-formedness. No supplied potentially large atom needs to be traversed to obtain f's token. Peeling Q_f's Pi leaves a terminal equality with an actual occurrence of f. Lift only its existing role-0 reference payload:

`P_f = [6,0,f_ref]`,

`T_f = SHA256(ASCII("DTMKN-STRUCT2-TOKEN") || encode([E,P_f]))`.

The existing native `FindPredicate 0x8102/3` is exactly

`[6,F,E,0,[T_f],[0]]`.

Here query mode 0 is APPLY_RESULT; the final `[0]` is absent pattern. At a separately negotiated [direct broker](../../../notes/analyses/CP-001I-direct-broker-bindings.md), the exact `BrokerPredicate 0x8126/1` is

`[F,E,[T_f],[0]]`.

Its final `[0]` is absent target filter, not a pattern field. Neither query supplies r, I or a desired theorem ID. These are symbol-based candidate queries: a returned theorem is not asserted to prove Q_f or to express injectivity. Query construction/type-view work remains paid local work; no proof of Q_f is requested or installed.

For the stipulated short stored terminal `I B A f`, the unique role-0 rigid constant references are at most I, B, A and f. STRUCT2 reserves four terminal/relation reference tokens, so `[6,0,f_ref]` is selected **if the relevant traversal, emission and descriptor construction complete without relevant truncation**. Fixed universe vectors do not add reference tokens. The small Q_f similarly exposes its f reference. This is a conditional syntax argument, not coverage of extra dictionaries, wrappers, larger terms or a generic bundled homomorphism. Index visibility and consulted-prefix placement remain additional premises.

Obtain at most one paid recovery page per contact. Retain the first eight eligible theorem descriptors in that lane and probe at most its first two distinct descriptors. A repeated d in that lane consumes received/decoded traffic but gives no extra slot or attempt. A d previously seen in another lane can enter this recovery queue; it consumes this lane's slot and selected probe/trial opportunity even if exact retained bytes can be reused. Global retained-slot accounting is conservative across lanes. No duplicate gives a free new attempt.

### Check at most two exact reflection candidates

For each of the two selected recovery descriptors, in queue order, its paid probe must expose the actual proposed target context, universe arity and complete type within the probe limits. Accept for full qualification only a theorem with empty recorded judgment context, zero universe arity and a closed conclusion. Those are admission restrictions, not an inference that its type is reflection. An ineligible, incomplete or rejected first probe consumes its opportunity; it does not authorize a third probe.

Fully acquire and independently qualify an admitted r candidate with its actual anchor replay and complete support. Then construct this closed native proof candidate:

`R_r := lambda x : B, lambda y : B, lambda e : Eq A (f x) (f y), w(p_r) x y e`.

Check it at exactly

`forall x y : B, Eq A (f x) (f y) -> Eq B x y`.

The [PI1 WitnessTermDAG](../../../notes/analyses/CP-001G-proof-instance-composition.md) reference is the constant node `[2,[7,ProofInstanceID(p_r)],[]]`: the empty level vector follows from this r's zero declaration universe arity. `[2,JudgmentID]` is not an allowed witness constant reference. At the innermost body, the explicit application arguments are bound-variable nodes `[0,2]`, `[0,1]`, `[0,0]`, for x, y, e respectively, supplied through three ordinary application nodes. Each lambda/domain is well scoped; in e's domain x/y have indices 1/0. There is no extra closure over a hidden recorded telescope. Source implicit binder annotations do not omit native arguments.

Ordinary native type conversion may unfold the *qualified* I definition when checking this term. It does not authorize arbitrary header normalization or add a trusted reflection rule. A valid theorem mentioning f can fail this exact application. Exact checking rejection is distinct from timeout, unavailable support, incompatible realization or another resource nondecision. Stop recovery after the first successful trial. A successful R_r remains a local checked term; this policy does not publish a new wrapper.

### Discover one image result and return to B

After reflection succeeds, construct J's one image equality using the checked f/h and issue its exact op_A operand-pair token query: at most one page per contact, 16 retained image descriptors, and two type probes. Apply J's existing narrow image-theorem matcher, including the requirement that every effective binder receive a checked ordered argument. Choose the first matching candidate; no second complete image-root attempt is selected if it later fails.

Acquire/qualify that one selected image root, check its actual application, then construct J's lift–image–reflection proof and check it at the original exact B equality under Gamma. Use R_r for the reflection step. Lift terms remain candidates until included in the final checked term, not checked-forward facts inferred from a symbolic recursion. This schedule selects no standalone lift check; any such check would consume a constructed-check slot and could prevent completion. Only the final original-goal check yields `CHECKED_LOCAL_APPLICATION`. No reflection success means this schedule stops before the image stage; inert image syntax is not checked partial success.

## Joint ceilings and non-free work

This reallocates, without increasing, J's aggregate ceilings. Smaller grants or inherited per-call limits can stop earlier. Every dimension binds simultaneously.

| Episode dimension | Selected ceiling |
|---|---|
| Candidate contacts / native source identities actually contacted | 2 / 8 total |
| Chosen f/h pairs / image views / map depth | 1 / 1 / 1, including failed choices |
| Candidate pages | 6: 2 initial + 2 recovery + 2 image |
| Rows decoded | 384 total, additionally subject to bytes/CPU |
| Retained descriptor slots | 48: 16 maps + 8 initial helpers + 8 recovery + 16 image |
| Type-probe starts | 12: 4 maps + 4 initial helpers + 2 recovery + 2 image |
| Each probe | 256 KiB; 8 remote attempts; 512 type/view nodes; depth 32 |
| Complete evidence acquisition/qualification starts | 8, including failures, interruptions and additional actual realization/recheck starts |
| Constructed proof-check starts | 4: at most 2 reflection trials + 1 image application + 1 final original-goal check |
| Matching/template node-pair inspections | 8192 aggregate |
| Remote invocation attempts | 256 across all stages, setup, control, acquisition and retries |
| All network payload/setup/control | 256 MiB; discovery at most 8 MiB within it |
| Metadata / total resident working set | 64 MiB within 2 GiB, including actual native/staging/control allocations |
| CPU / horizon / concurrent work stages | 120 CPU-seconds / 600 qualified receiver-local seconds / 1 |

The direct maximal path starts qualification of f, h, two r candidates and one image root: five starts, **not a promise that only five suffice**. Additional incompatible-environment realizations or rechecks debit the remaining three; they are not hidden under “one root.” A constructed check that also requires a new native qualification/reconstruction start debits both applicable counters. Closure dependencies and foundation work consume their full actual resources. Shared protected state is accounted under inherited physical sharing rules, never presumed free. Cold support might prevent even the first completion. Source service remains separately funded.

Query/check work, candidate parsing, failed leads, rejected conversions, discarded terms and uncertain executions debit the same parent allocation. Unused capacity does not authorize a second pair/view, third recovery candidate, second image-root selection, generic fallback or automatic restart. Source changes, leases and snapshots do not reset counters. Exact once-only invocation reconciliation, cancellation and uncertainty fences remain inherited; no unqualified replay of a partially completed episode is selected.

Every initial, map-reference and image query requires its own applicable disclosure authorization. Source reads require actual public scope or authorized holder-bound export, never merely a broker row. No extra type endpoint, arbitrary private lookup, signature-based theorem trust or inherited broker pattern test is introduced.

## Outcomes and conditional safety

Return the principal stage/outcome, bounded partial records and actual expenditures. Preserve J's distinctions: unsupported fragment; admission/disclosure blocked; no supported candidate in the scanned scope; type-probe/matching nondecision; exact malformed-input/native rejection; incompatible checked interface; native import nondecision; and budget exhaustion. Record failed reflection trials separately from missing candidates.

If reflection is not established, report the exact missing reflection type and scoped observations, not nonexistence or noninjectivity. If an image application succeeds but final transport fails or becomes noncurrent, retain only that exact checked partial application under its surviving guards. A completed checked reflection alone does not solve the B goal. Historical checked objects are not automatically current-use authority after an incident, policy or environment change.

Conditional safety is unchanged: assuming the adopted native checker/foundation and exact reconstruction contracts, a returned `CHECKED_LOCAL_APPLICATION` is supported by the final accepted term at the requested type/context. Recovery-token correctness, broker honesty, ranking quality and a source label are not additional mathematical trust axioms. This does not establish semantic consistency of an arbitrary foundation or completeness of search.

## Paper traces

### Favorable trace with one genuine false positive

Reuse J's distinct-record fixture: B has one Nat value field; A has Nat value and Unit marker fields; the operations add values; f copies the value and supplies the Unit marker. Preserve explicit h and the A-associativity theorem. Change only the required reflection theorem's stored type to the folded `I B A f`; no explicit reflection wrapper is prepublished. Complete checked evidence remains a premise, not an artifact asserted to exist.

Assume initial finite consulted prefixes put f/h within the selected positions. After their successful qualification, Q_f supplies T_f. Suppose the first two selected recovery rows are a closed, zero-universe proof of `Eq (B -> A) f f`, followed by the folded injectivity proof. The first is a true theorem and can emit T_f, but its proof constant cannot be applied to x, y, e at the reflection type. Its qualification and rejected trial are paid. The second qualifies and its trial succeeds by ordinary conversion/application through the checked I body.

Assume A-associativity occupies an admitted image-probe position. Its ordered application to the three f-images checks; the final lifted and reflected term checks at B-associativity. This direct trace uses five qualification starts and all four constructed-check starts. It additionally assumes actual compatible realization, successful feature extraction, current scopes and sufficient actual resources; further reconstruction work can exhaust the joint envelope. No content ID, exported artifact or observed timing is invented. Directly proving B-associativity using Nat may be cheaper.

### Crowded-prefix defeating trace

Keep the valid folded r and its genuine T_f membership. Put two earlier eligible theorem descriptors in the selected recovery prefix: the same `f=f` fact and a closed theorem `forall z : B, Eq A (f z) (f z)`. Both can mention f and carry fully valid native proofs. Neither supports the required three-argument reflection application: the first is not a function at all; after its B argument the second supplies an equality, not the remaining function expected by the trial.

Assume both are probed, qualified and rejected within resources. The true r lies later in the queue or beyond the retained prefix. Two trials are exhausted; report a bounded missing-reflection result and the actual cost. No image stage is attempted and no theorem is declared absent or false. No token dishonesty is needed for this defeat. J's independent constant-map/nonreflecting example remains another obstacle, even with favorable discovery.

## What this proposal does not establish

The first trace identifies a concrete syntax-sensitive recovery opportunity; the second shows ordinary crowding defeats it. Neither establishes performance improvement, broad-library coverage, native export feasibility under the current adapter, or sustained knowledge growth. A later separately authorized qualification would need actual retained folded native artifacts, independent checks and fixed-budget comparisons with unchanged J and direct local proof. Until then this is an auditable local-policy hypothesis, not execution evidence.

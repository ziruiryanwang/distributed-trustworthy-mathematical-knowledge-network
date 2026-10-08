# Next experiment contract: source-derived shared-Subtype composition

Date: 2026-09-20. Status: reviewed specification with clarification closure; **NOT IMPLEMENTED / NOT RUN**. This is the exact-case follow-up to the [concept/experiment decision](2026-09-20-concept-experiment-decision.md), not a new network profile or a claim of an operable finished product. Root owns this document. The current authorization is to select the case and specify the investigation, not to extend or execute the prototype.

## Decision and the uncertainty it resolves

Select Lean's existing `Subtype` and `Function.Injective` as the first shared source-library interface. Two isolated producers contribute a projection-injectivity theorem and a predicate-preserving map with its projection theorem. A fresh consumer combines both contributions to prove the existence of an injective lift, exports its actual checked result, and obtains fresh replay.

This tests a central unanswered question: can independently authored ordinary Lean mathematics cross our exchange boundary and compose over one faithfully reconstructed, proof-bearing, universe-polymorphic interface? The completed [15-to-19-object example](../../experiments/lean-feasibility/RESULTS.md) demonstrated real native dependency use but hand-constructed its ordinary payloads. It did not establish this source-export/interface capability.

The two gates remain separate:

- **Gate A is the selected next implementation target:** known-ID, source-derived shared-interface composition, with exact correspondence and actual-use controls. This note supplies its mathematical and acceptance contract. It still requires implementation and a pre-run artifact binding.
- **Gate B is a preregistered follow-on, not yet executable:** matched local-only, known-ID and discovery trials on the same mathematics. We fix the target, corpus formulas, fairness rules, outcomes and proposed ceilings here. A concrete local synthesis/search policy is still a real design dependency, not a hash waiting to be filled in. Gate B must not run until the separate launch conditions below are met.

Do not implement a broad new theorem prover merely to make this example pass. First establish Gate A; then choose the smallest credible local-agent policy and ask whether this very easy case has any discriminatory power for costed reuse. A decision not to use it as a utility benchmark is allowed and must be reported, not disguised by making the local baseline weaker.

## Why this interface

`Subtype {α : Sort u} (p : α → Prop)` has a value field and a proof field whose type depends on that value. Unlike the previous monomorphic definition/theorem example, this requires an external nominal inductive group, generated-member reconciliation, projections and explicit universes. The general consumer proof uses equality reasoning; it is not just reflexivity of an unfolded whole target.

The preliminary `Setoid` candidate remains legitimate, but its inspected formulation required both `Setoid` and `Equivalence`, while the proposed characterization mostly reduced definitionally. `ULift` exercises universes but lacks the dependent proof-bearing field. No mathlib download is needed for the selected case.

This is not new mathematics. Pinned `Init/Core.lean` already contains `Subtype.ext`, equivalent to the essential content of producer A's theorem. B's map is also easy to construct locally. Their role here is to expose representation, identity and composition failures. Neither a new content ID nor successful use establishes novelty, usefulness or saved work.

## Pinned read-only evidence

Use the existing portable Lean v4.34.0 candidate, commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`, and the previously saved full selected foundation. The following files were inspected and their SHA-256 bindings checked without starting Lean:

| Local source relative to `experiments/lean-feasibility/` | Bytes | SHA-256 |
|---|---:|---|
| `runtime/lean-4.34.0-windows/src/lean/Init/Prelude.lean` | 238777 | `2A3163BDD830CD31F1F1BC9BC79EA6BDAD6A3B2C6F334166792BBC73631F3B10` |
| `runtime/lean-4.34.0-windows/src/lean/Init/Core.lean` | 100653 | `6218A9825A0CE51A6BBE3949EC7A86C4406F4F216BD3CD1262736CFC1C997C54` |
| `runtime/lean-4.34.0-windows/src/lean/Init/Data/Function.lean` | 5902 | `88217ED8EC91DA1EC655C8A10F737B659A4570B4C05DBD6B084162A3157CF030` |
| `artifacts/20260920-seed-candidate-02/seed-verified.json` | 724174 | `A0ACDC706F5E42DCA21950C14DB2307A18955C63FF953019AAFF413D0A976001` |

Source anchors: `Subtype` at `Init/Prelude.lean:655`; `Function.Injective` at `Init/Data/Function.lean:53`; `Subtype.ext` at `Init/Core.lean:1380`. The source scout's structural scan of the saved 581-name seed found no `Subtype`, `Function.Injective`, `Setoid`, `Equivalence` or `ULift` exports. Required equality operations, `congrArg`, `Exists` and `And` are already present. This is a source/seed observation, not an executed extraction of the new interface.

The canonical seed remains the saved 262,520-byte `seed.cbor`, SHA-256 `C4EE214AB2E070DD6948DE1D4B8FA84C78CD182FBFE7CDC27D4317DD4E923147`. Reuse its actual candidate FoundationID and associated rules/reserved-name objects from the saved manifest. Do not invent a new FoundationID, add the external interface to the seed, or call this candidate a production-qualified foundation.

## Mathematical contract

The following is mathematical notation and a source-authoring blueprint, **not compiled Lean**. Local names explain the experiment; content identities will come from actual captured declarations. All declarations are closed over the displayed parameters when exported, with an empty explicit judgment telescope and the full source forall type as conclusion, following EXTRACT1's ordinary-source convention.

Let

\[
\begin{aligned}
&\alpha : \mathrm{Type}\ u,\quad \beta : \mathrm{Type}\ v,\\
&p:\alpha\to\mathrm{Prop},\quad q:\beta\to\mathrm{Prop},\quad f:\alpha\to\beta,\\
&h:\forall a:\alpha,\ p(a)\to q(f(a)),\quad h_f:\operatorname{Injective}(f).
\end{aligned}
\]

Write \(S_p=\operatorname{Subtype}(p)\), \(S_q=\operatorname{Subtype}(q)\), and \(\pi_p:S_p\to\alpha\), \(\pi_q:S_q\to\beta\) for their value projections. These abbreviations do not introduce an alternative datatype. The shared original `Subtype` supports `Sort`; the branch theorems in this first case intentionally quantify over `Type u` and `Type v`. Do not replace these by `Nat`, fix `u=v=0`, reorder actual native universe parameters, or claim the more general `Sort` theorem was tested.

### Producer A: projection injectivity

Source root `SharedSubtypeA.val_injective` has type

\[
\forall\{\alpha:\mathrm{Type}\ u\}(p:\alpha\to\mathrm{Prop}),\quad
\operatorname{Injective}(\pi_p).
\]

Author a proof by destructing both subtype values, eliminating their value equality, and using reflexivity/proof irrelevance. The selected A proof does not call `Subtype.ext` and has no dependency on producer B. This restriction fixes a conformance witness; it is not a rule imposed on baseline agents or a claim of mathematical independence from standard theory.

The actual proof record, including any elaborator-generated cases helper, must be captured. A direct cases proof that exports unsupported machinery is a diagnosed failure of this source path, not permission to replace the body by a hand-written canonical term after the fact.

### Producer B: a proof-preserving map and its law

Source definition `SharedSubtypeB.map` has the explicitly quantified type

\[
\forall\{\alpha:\mathrm{Type}\ u\}\{\beta:\mathrm{Type}\ v\}
\{p:\alpha\to\mathrm{Prop}\}\{q:\beta\to\mathrm{Prop}\},\quad
(f:\alpha\to\beta)\to(\forall a,\ p(a)\to q(f(a)))\to S_p\to S_q.
\]

Its value is

\[
M_{f,h}(x)=\langle f(x.\mathrm{val}),\ h(x.\mathrm{val})(x.\mathrm{property})\rangle.
\]

Source theorem `SharedSubtypeB.map_val`, under the same parameters, proves

\[
\forall x:S_p,\quad \pi_q(M_{f,h}(x))=f(\pi_p(x)).
\]

Its source proof may be reflexivity. B does not depend on A or on its statement/instance. The preservation proof `h` is a bound local parameter inside the definition; it is not an imported proof-instance reference inserted into a semantic definition body.

### Consumer: a joint application and a base-only target

Source root `SharedSubtypeConsumer.exists_injective_lift` proves, with all the parameters above,

\[
\exists L:S_p\to S_q,\quad
\bigl(\forall x:S_p,\ \pi_q(L(x))=f(\pi_p(x))\bigr)
\land\operatorname{Injective}(L).
\]

The target contains only the common interface and local parameters/hypotheses. It does not require the consumer to know B's map name, a producer ID, a theorem spelling, or a human's intended answer.

Gate A deliberately fixes this witness construction: select \(L=M_{f,h}\), discharge its projection conjunct using B's theorem, and prove its injectivity using A's theorem. For arbitrary \(x,y:S_p\) and \(e:M_{f,h}(x)=M_{f,h}(y)\), let \(b_x,b_y\) denote B's projection laws. Then

\[
b_x^{-1}\ \cdot\ \operatorname{congrArg}(\pi_q,e)\ \cdot\ b_y
  : f(\pi_p(x))=f(\pi_p(y)).
\]

Apply \(h_f\), obtaining \(\pi_p(x)=\pi_p(y)\); apply A, obtaining \(x=y\). The equalities compose in that order: \(b_x^{-1}\) starts at \(f(\pi_p(x))\), and \(b_y\) ends at \(f(\pi_p(y))\). This verifies the paper derivation without asserting Lean elaboration or export has run.

The output's **type** need not mention B. Its actual witness does mention B's map and B's law, and applies A to the derived value equality. An unused let, an irrelevant annotation, or an additional unused premise referring to a contribution does not meet this specified Gate A construction. Conversely, another valid proof of the same target is a legitimate mathematical result; it simply does not witness this particular joint-composition test.

The test does not assume either subtype is inhabited. Predicate preservation plus injectivity suffices even for an empty domain. There is no additional nonemptiness, chosen representative, classical choice, global task list or human-intention premise.

## Common interface, authoring tools and evidence authority

Distinguish three things that otherwise produce an unfair or unsound experiment.

**Core interface I0.** Select the actual external `Subtype` atomic group, required generated interface, separately captured `Subtype.val` / `Subtype.property` projection declarations where referenced, and `Function.Injective`. Include their complete actual support beyond the unchanged seed. Use EXTRACT1's **completed-record recovery route** for this group; retain its source `all`/constructors/recursor inventory and compare it to receiving reconstruction. Kernel group generation does not magically regenerate separate elaborator projection definitions.

**Common standard support Istd.** Capture and independently admit the pinned `Subtype.ext` and its actual closure as explicit available standard support. Both producers and all three eventual Gate B arms receive the same common support. A's selected proof does not use ext, but ext must not be hidden to make acquisition of A appear valuable. If other standard-library declarations are used, their closures must also be captured and checked; inspect and report them, do not silently add assumptions.

**Local authoring capabilities.** Allow the same pinned `Init` source/catalogue, local elaborator and standard tactics in every Gate B arm. The exact module/artifact search paths and enabled local frontend facilities must be frozen before trials. Their presence helps construction but grants no receiving authority. No peer can install a plugin, tactic, simp registration or executable extension. Standard-source visibility does not mean all `Init` declarations are pre-admitted in the receiving kernel.

The selected capture route may import completed full-private producer artifacts with `plugins := #[]` and `loadExts := false` to inspect constant records, as in the [source-capture notes](../../experiments/lean-feasibility/source-capture-notes.md). This capture-only environment is not the receiving proof environment. Ordinary source compilation uses the owner's pinned trusted frontend; complete records are captured afterward. Record actual resolved paths and clear inherited module-path shadowing in child processes. Missing bodies, async placeholders, mismatched private artifacts, `sorryAx`, disallowed axioms, unsafe/partial definitions and unsupported declaration kinds cannot become accepted evidence.

Actual closure traversal, not a theorem-name whitelist or an entire `Init` import, determines the extra native declarations reconstructed. The **pre-admitted** common I0/Istd closure is fully inventoried and frozen before trials. The larger pinned standard-library source catalogue is an equally visible, read-only authoring input, not an inventory of already accepted declarations. A trial may reach another declaration from that exact catalogue through a previously frozen supported source-capture route, recording its actual closure and capture/checking/storage cost during that trial. This is on-demand standard support, not free growth of the prepared base. An unsupported closure gives unsupported/noncompletion; it never silently broadens the trusted basis, installs unchecked imported records, or changes the permitted source catalogue. Distinguish these origins from locally authored declarations and acquired corpus evidence in the export trace.

## Isolation, identity and reconstruction

Producer A and B use separate fresh processes, source directories and mutable artifact caches. Their read-only inputs are the same pinned runtime, complete selected foundation and frozen common interface/support. Neither has the other's source/module/package/output, and neither imports a combined hidden producer module. Record accessible inputs and the actual dependency graph. Shared standard tools are allowed and disclosed.

This is isolated branch construction, not independent mathematical invention: we supply both assignments. Nor is it an independently implemented kernel, different trust domain, statistical replication or malicious-process sandbox qualification.

Each producer separately resolves the shared source declarations to the exact frozen I0 identities. Require their common-interface descriptors and mappings to match. Familiar spelling is insufficient. A distinct group stays distinct; no automatic coercion, name alias or source annotation certifies its interchangeability. Identical captured syntax under the selected canonicalization may share identity; mere file/name duplication is not a valid negative-control construction.

For all exports retain both EXTRACT1 maps: source name to semantic reference, and source theorem implementation to ProofInstanceID. Semantic definitions/types use semantic references; theorem witness terms use actual proof-instance references. Compute exact PI1 representative obligations from the reachable graph. Do not assume an empty representative map because the previous fixture used one, and do not force a nonempty map simply to enlarge the test. No cross-branch representative substitution variation is selected here.

The consumer receives supplied replay/root IDs and inert packages, not producer source or an imported prechecked native environment. Reconstruct from the selected foundation through the checked native path, installing the shared group only once at its canonical identity. A local source presentation may expose checked aliases and explicit application syntax under CLIENT1; it may not insert unchecked axioms or substitute a source-native nominal copy for the canonical group. Capture the consumer's actual completed checked declaration. Inverse-export those native records, not the expected proof template.

A final fresh receiver starts empty and reconstructs the successor's whole exact evidence closure using only saved bytes and the selected local foundation decision. Compare actual types, bodies, universe order, generated inventory and canonical re-export. Reusing a producer import, prior ACCEPT cache, elaborator success flag or sender certificate does not satisfy fresh replay.

## Gate A stages and observable verdicts

| Stage | Required output | Stop/failure meaning |
|---|---|---|
| A0: bind inputs and implementation | Source/runtime/adapter hashes, resource settings, search paths, exact old foundation artifacts, permitted inputs | Missing bindings or unsupported authority path: not ready; no experiment pass |
| A1: capture and replay I0/Istd | Complete source records; group recovery descriptor; actual checked generated inventory; exact maps and support; matching independent producer resolutions | Unsupported capture, source-correspondence mismatch, native rejection or resource nondecision, distinguished |
| A2: source-author A and B separately | Completed ordinary source, source artifact hashes, branch exports, separate fresh branch replays; no cross-branch dependency | Compilation/capture/export/replay failure reported at its actual boundary |
| A3: known-ID consumer | Fresh joined checked environment; source-authored target above; actual witness application of A and B; no unchecked interface substitution | A valid alternative proof is not A3 conformance; source or identity ambiguity returns to concept work |
| A4: actual successor export and replay | Exact saved root/closure, actual inverse-native export, fresh third-party-style replay and comparison | A merely planned payload or unresolved dependency is not success |
| A5: controls and evidence audit | Outcomes of all controls below, complete retained attempts and costs, two separately scoped reviews | Control failure or incomplete evidence limits the claim even if A4 succeeded |

`A-PASS` requires A0–A5 for the declared cut. Also report the intermediate EXTRACT1 facts separately: complete candidate export, native acceptance, and source correspondence. Do not collapse them into one sender boolean. The word “independent” in final replay means fresh state on the same host/implementation unless stronger evidence actually exists.

Required controls, each in a fresh state with no auto-repair:

1. **Remove A's selected evidence.** Keep the successor target/root and remaining bytes fixed; withhold its A proof instance from available acquisition. The recorded construction must not accept without complete required evidence. This tests closure enforcement, not impossibility of an alternative local proof.
2. **Remove B's selected evidence.** Similarly withhold B's projection-law instance, retaining its map. Expected outcome is unavailable required evidence, not a mathematical refutation. If canonicalization has actually coalesced an object with available evidence, report that identity rather than pretending it was removed; redesign the control before claiming it ran.
3. **Change actual interface identity.** In a separately recorded control source, construct a valid `MarkedSubtype` with fields `val : α`, `property : p val`, `mark : Bool`, and its own map. Capture/check it. Attempt the *unchanged original-Subtype application* using the marked map, with no transport supplied and the original carrier, predicate and universe arguments fixed. The exact type mismatch must not be repaired by a spelling-based substitution or by inferring a different intended application. This control is separately bounded; it does not change the positive test's shared interface.
4. **Corrupt claimed generated correspondence.** Change one claimed generated-member field/count while preserving the actual selected group descriptor. Require mismatch detection against the receiver-derived inventory. An early malformed-byte rejection is not this specific control's success.
5. **Wrong but well-formed proof.** Submit a canonically valid, closed, correctly bound witness of the wrong type for a selected judgment, with its new identities recomputed. Require actual native type rejection rather than acceptance of the package's asserted verdict. Preserve the exact mutated object and failing stage.

Previously preserved seed/ell negative runs are precedents, not executions of these new controls. If an attempted control fails earlier than intended, retain it and label the intended boundary untested.

## Finite Gate A envelope

These are engineering stopping ceilings, not measurements or a production adversarial-input guarantee. Use them for the future first execution cut unless amended explicitly **before** that cut. Stage timing includes process startup and required work; record frontend, capture, codec, native check and export components where measurable.

| Resource | Ceiling for one stage/attempt |
|---|---|
| Active experimental Lean processes | One; wait for exit before the next |
| Wall / total child-process CPU | 300 seconds wall / 300 aggregate CPU-seconds, whichever stops first |
| Aggregate experimental child private committed memory | 4 GiB; include worker descendants, not just the launcher |
| Selected extension beyond the unchanged seed | 256 atomic source units, 1024 native exports; generated auxiliaries count |
| Serialized input/candidate closure | 64 MiB, including foundation objects; charge shared bytes once per stored closure and every actual transfer separately |
| New staging/output per numbered pipeline attempt | 256 MiB across all its stages together, including logs and copied inputs; stop before silently truncating evidence |
| Native check settings | Initially inherit the pinned prototype's 20,000,000 heartbeats and 10,000 recursion-depth ceiling per checked declaration; record exact runtime meaning/settings |
| Number of preserved attempts | At most 12 experimental pipeline attempts, including controls and retries, before a renewed scope decision; a serial pipeline can contain several bounded stage processes |

Preinstalled runtime/source/artifacts are read-only setup inputs, not part of the 64 MiB mathematical closure; report their footprint and setup cost separately. New source modules and build outputs do count toward staging. Enforce admission/count/byte bounds before traversals where possible; process caps provide a second stop. If reliable resource enforcement/measurement is unavailable, report that limit and do not claim to have met an enforced envelope. Do not reinterpret an OOM, timeout or unavailable dependency as a rejected mathematical theorem.

Every attempt gets immutable inputs, code/settings bindings, start/end/exit information and stdout/stderr. Retain failed attempts. Implementation debugging can revise code under a new recorded cut, but cannot overwrite evidence, silently change the mathematical target, specialize universes or relax budgets while reporting the original contract passed.

For finite accounting, each numbered pipeline attempt may invoke each of A0–A5 at most once. All sequential child processes within one stage, including its controls, share that stage's time/CPU/memory allocation; all stages also share the pipeline attempt's single 256 MiB staging/output cap. Repeating a stage consumes a new attempt number. Thus the twelve-attempt ceiling admits at most 72 stage invocations and 21,600 charged wall/CPU seconds each in aggregate; these are conservative maxima, not a reservation, expected runtime, or permission to bypass an earlier cap. Authoring/review time is reported separately from experimental execution. Do not replenish an allowance for every subprocess, control or retry.

## Required adapter work, not presumed existing support

The old ordinary fixture explicitly accepts zero-universe, empty-explicit-telescope statements, a limited direct-reference set, definitions/proof instances, and an empty representative map. See `reciprocal_fixture.py`'s `native_plan`, `visit`, `term` and inverse-export restrictions. Its source code reports these limitations. The existing bootstrap's seed-group reconstruction does not automatically qualify ordinary external groups.

The selected new path therefore needs source-driven ordinary collection, parameterized level expressions, multi-reference context sets, external group/member/projection handling, exact semantic/witness mapping and corresponding actual-native inverse export. It may need representative-map support if the actual closure requires it. Preserve all prior fixture cuts/results. Do not bypass those restrictions with trusted pre-imports and call the result the same verified path.

This list is a bounded implementation delta for a later authorized turn, not code added now. A discovered unsupported feature is classified and returned to the contract; it does not justify importing arbitrary libraries or dropping source correspondence.

## Gate B preregistration: target, corpus and access arms

Gate B has the same base-only existential target and hypotheses as above. The local-only arm may prove it directly; standard `Subtype.ext` is available. Use three fresh consumers with the same common formal/authoring inputs and policy:

| Arm | Additional contribution access | What it can establish |
|---|---|---|
| Local-only | No public contribution corpus or A/B IDs | Local completion/cost reference |
| Known-ID | The three relevant A theorem / B map / B law root bindings, without a proof sketch or producer aliases | Oracle-assisted access diagnostic, not discovery or guaranteed optimal performance |
| Discovery | Only two fixed provider-snapshot contacts and the declared search/acquisition interface | Discovery among the frozen finite candidates, not unfamiliar-provider reachability |

Do not give the discovery consumer this document, source-scout messages, Gate A source/proofs/plans, useful names/IDs, evaluator annotations, other arm transcripts, or cached evidence. A fresh model session, if later selected, must not inherit this conversation. The evaluator and consumer need separately controlled accessible-input sets; a prompt saying “ignore the answer” is not isolation. Root's current session can supervise but cannot stand in for a blind discovery consumer.

### Exact nominal candidate corpus

Preregister ten source-authored public target declarations, with the following formulas. Labels are evaluator-only; expose only protocol descriptors and inert fetched records to the discovery client. In these rows, shared parameters are universally quantified, `x,y : S_p`, and `g : S_p → S_q` where shown. “Control” does not mean mathematically useless: any legitimate use counts.

| Label | Target formula or definition | Provider | Experimental role |
|---|---|---|---|
| C1 | A's `Injective π_p` theorem | P1 | Supplied contribution |
| C2 | B's `M_(f,h) : S_p → S_q` definition | P2 | Supplied definition |
| C3 | B's `∀ x, π_q(M_(f,h)(x)) = f(π_p(x))` theorem | P2 | Supplied contribution |
| C4 | `∀ x, π_p(x) = π_p(x)` | P1 | Generic equality control |
| C5 | `∀ x y, x = y → π_p(x) = π_p(y)` | P2 | Potentially helpful congruence alternative |
| C6 | `∀ x : S_p, p(π_p(x))` | P1 | Dependent-property control/helper |
| C7 | `S_p → ∃ a : α, p(a)` | P2 | Related existential with different conclusion |
| C8 | `∀ g : S_p → S_q, (∀ x y : S_p, x = y) → Injective g` | P1 | Injectivity with an extra unsupplied premise |
| C9 | `∀ x y, (π_p(x) = π_p(y)) ↔ (π_p(y) = π_p(x))` | P2 | Iff/direction control/helper |
| C10 | `∀ x : S_p, True` | P1 | Broad logical control |

All control proofs use only the shared base/standard support, not C1–C3. Prove them in ordinary source and independently replay before publication; no knowingly false distractors. Index exactly the listed selected roots, not every closure object as an unannounced extra target. Complete support still accompanies acquisition and may itself be used after checking. If distinct source declarations collapse to the same exact semantic target, coalesce them according to the profile and report the resulting unique-target count; do not inject meaningless syntactic wrappers to restore ten IDs.

Within each provider, use the existing canonical descriptor-ID ordering, never a favorable manually sorted useful-first list. Retain both provider snapshots and the evaluator's separate answer/role map before consumer trials. This is a small engineered corpus, not representative mathematical retrieval, a large-library benchmark, a mandatory network task registry or a universal usefulness test.

### What STRUCT2 supplies, and what it does not

Use the selected [STRUCT2/1](../../notes/analyses/CP-001G-structural-retrieval.md) descriptor/extractor and existing `FIND_WINDOW` operation 10 with `FindPredicate 0x8102/3`, mode 6. A local snapshot service can exercise these query semantics; it does not qualify network framing, routing, custody, signatures, service fairness or remote latency. Do not add an experiment-specific opcode or a centralized theorem authority.

With `H_S` the exact informative head of the shared Subtype type former, a local request for a function `S_p → S_q` can lift the FUNCTION_OUTPUT pair `[4,H_S,H_S]`. This pair erases the difference between the predicates and carriers at retrieval time; actual instantiation must check those differences. It arises only after the local policy has selected an existential witness-type subproblem. Merely extracting features from the whole outer `Exists` does not perform that decomposition.

Similarly, an APPLY_RESULT query on the folded `Function.Injective` head can retrieve a differently shaped set than a query on its unfolded forall/equality form. STRUCT2 does beta/zeta normalization, not arbitrary delta unfolding. Projection constants and native projection nodes have different exact HeadAtom forms. Do not invent a token from a printed expression and assume the source exporter emits it. C3's unknown map identity cannot be included in an initial query; it can become a legitimate local expression only after discovery/acquisition/checked instantiation of that map.

Before any B trial, save actual descriptors, feature payloads/tokens/flags and lane selection traces. Check query derivation from permitted local formal state. A missing feature is a measured coverage issue, not permission to hard-code “find B.map, then B.map_val, then A.” Any stronger local unfolding/view policy must be explicitly chosen, costed and applied equally; it is not part of STRUCT2 by default.

### Genuine unresolved local-policy decision

The actual shared solver/controller is **not selected by this note**. Existing pinned library-search routines are useful candidate tools, not evidence that the required synthesis works. Before launch, select and freeze one policy specifying:

- How it opens the formal target, selects existential/function subproblems, and chooses direct construction versus acquisition; all three arms retain direct proving capability.
- How it instantiates universe/telescope parameters, constructs actual checked dependent applications and handles residual proof obligations.
- Which local unfoldings, constructor/cases/congruence/rewrite/apply actions are available and their scheduling/finite fuel; how failed applications backtrack without losing their accounting.
- How query modes/lanes arise from the current state, how candidates are ordered/acquired, and when search stops. No answer-specific names, IDs or encoded derivation.
- If using a model, its fixed model/version/configuration, exact initial prompt/tool schemas/context access, token/call limits and recorded nondeterminism. No new model/API execution is authorized here.

A policy may be heuristic. It need not be proved optimal or complete. It must be specified sufficiently that an unsuccessful attempt is a meaningful observation and a second implementer can identify what ran. A small separate policy-conformance check can establish faithful execution, not test-set independence. Do not quietly tune on the three measured arms; any pilot tuning must be disclosed and followed by a fresh frozen evaluation cut.

### Proposed B ceilings and accounting

Preregister a 300-second total end-to-end wall/CPU envelope per arm, the same 4 GiB aggregate private-memory limit and one active Lean child at a time. Start from an equally prepared, checked common base; report that preparation separately and also report a cold onboarding total. End at actual checked successor export plus fresh replay, not at model text, tactic success or a search hit.

For discovery use at most one STRUCT2 interactive attempt: 10 wall-seconds, 2 local CPU-seconds, 24 pages, 8 MiB aggregate discovery traffic and 64 MiB temporary discovery memory, all within the outer limits. Up to eight candidate-root acquisition/application attempts; retries and evidence alternatives consume these slots. Retain the existing at-most-eight-lane portfolio and per-page limits, but do not confuse those with a selected synthesis controller. Across modes/providers the controller must obey the one-attempt totals, not receive a fresh allowance for every subgoal.

The cumulative contribution-acquisition cap is frozen after A from the independently checked corpus closures: eight times the largest non-common single-target complete closure size, with an absolute 64 MiB ceiling. Common prepared bytes are counted separately; retransfers and failed bytes count against acquisition. If this cap cannot serve the intended finite case, report that before B rather than adjusting after observing a trial. Kernel/checking/staging limits inherit A unless a new preregistered cut changes them for all arms. An LLM, if chosen, also needs a finite token/call limit before launch; 300 seconds is not a substitute for that choice.

Run one trial per arm as an initial diagnostic, serially in the preregistered order local-only, known-ID, discovery. Disclose OS/runtime cache state; fresh logical state is not guaranteed cold physical storage. No statistical timing or general superiority claim follows from this order or sample size. Stronger comparisons require repetition/counterbalanced order and held-out cases.

Record: endpoint completion; actual acquired artifact use in the checked term; discovery-origin use; stage/total wall and CPU; peak measured memory; model tokens/calls if applicable; lanes/pages/bytes; candidates attempted; failure reasons; capture/check/adaptation/proving/export costs; and retained evidence/index bytes. Record producer, interface preparation and publication/index costs separately and include them in any whole-system amortization claim. No unseen future reusers are credited in advance.

Compare actual referenced identities with the initial checked common closure and with on-demand standard/local evidence. A fetched object already held under the same identity is reacquisition, not new-to-consumer evidence. A locally derived object whose ID matches a corpus object is not discovery merely because those bytes could have been fetched. Report acquired-reference use, acquisition origin and new-to-consumer evidence separately. Source aliases, additional downloads and exact-ID multiplicity cannot inflate the usefulness measure; even genuinely new-to-consumer evidence is not automatically new mathematics or saved work.

Mathematical completion is independent of contribution use. A direct local proof counts, including in the assisted arms. A correct alternative contribution route counts. Two-branch use is required by Gate A, not by Gate B. A timeout is censored noncompletion, not an exact infinite cost or a manufactured numerical speedup. “Discoverable checked reuse” and “observed benefit” are separate fields; neither implies sustained useful accumulation.

## Launch checklist: bindings versus open decisions

| Item | Type of remaining work | Gate |
|---|---|---|
| Actual I0/Istd source closure, universes/member inventories, content IDs, exact PI1 maps | Deterministic capture/reconstruction outputs under this contract; must be bound, not guessed | A artifact freeze |
| Ordinary source/receiver/export adapter implementation and reviewed code hashes | Engineering work not yet authorized or done; prior prototype does not support the whole case | A launch |
| Resource enforcement, immutable attempt layout and negative-control inputs | Engineering/pre-run bindings; fail readiness if not supplied | A launch |
| Actual public corpus/descriptors/snapshot order and sizes | Capture-derived fields with fixed formulas/provider allocation | B freeze after A |
| Concrete local synthesis/query/application policy and, if applicable, model budget | **Genuine design choice still open**; not fillable by inventing a hash | B launch |
| Consumer accessible-input enforcement and arm-specific exposure | Implementation/control verification before measured trials | B launch |
| Whether this easy case merits a utility trial at all | Decision after A costs and policy feasibility; no predicted win | B launch |

No missing item is silently satisfied by an agent saying “use an LLM” or by a provider supplying a relevant ID. A known-ID composition success can justify proceeding to a tightly specified B pilot; it cannot justify reporting B already ready or passed.

## Decision rules and retained checkpoint

If source-derived identity or joint reconstruction is ambiguous, repair that core contract before retrieval work. If the contract is determinate but implementation fails, record and repair the implementation under an explicit new cut. If the known-ID consumer works but no credible generic policy derives useful queries, the obstacle is local reasoning/retrieval coupling—not a need for blockchain consensus or a larger theorem dump.

If assisted completion is no cheaper than direct construction, report it. This case can still qualify a necessary interoperability mechanism; it does not qualify the value proposition. Move later utility experiments toward work with real reusable content rather than withholding `Subtype.ext`, forcing imports, multiplying easy theorem hashes, or treating independent agents' use counts as a correctness oracle.

Retain this contract, source bindings, actual later artifacts/attempts, reviewer findings/dispositions, and the result-dependent next decision. Do not rewrite frozen prior evidence. The deliverable of this turn is the reviewed bounded specification and truthful readiness distinction. The whole decentralized-mathematics objective remains unfinished.

## Review record

The source scout selected and source-bound the Subtype case. Separate native and evaluation preflights identified the standard-ext baseline hazard, the old adapter's restricted scope, and the missing local synthesis/query policy. Root incorporated these before the complete held-cut reviews below.

All three reviewers read the same entire 37,618-byte cut, SHA-256 `2C0F61B4F4CE170AA0971F1B83FCBF5B887EB572D88A29449BB5F0B38012DC0B`, with no file-write or execution authority:

| Reviewer and scope | Finding and disposition |
|---|---|
| `bounded_domains_author`: mathematics, native/source path | No blocker in scope; checked the equality chain, absence of inhabitance/choice premise, corpus formulas, controls and explicit adapter delta. This reviewer originated the mathematical suggestion; not a blind independent invention audit |
| `bounded_domains_resource`: evaluation, corpus and resources | No blocker in scope; fair standard support and direct/alternative solutions preserved; Gate B honestly unready. Root made the finite aggregate stage/retry accounting explicit |
| `feasibility_checkpoint_audit`: independent integration/authority review | No blocker in scope; requested clarification between frozen pre-admitted support and later charged on-demand standard capture. Root made these origins explicit and separately distinguished reacquisition from new-to-consumer evidence |

Root also fixed the nominal-mismatch control's carrier/predicate/universe arguments to prevent an elaborator from changing the application being tested. Both the integration and evaluation reviewers verified and scoped-reread the resulting 40,876-byte cut, SHA-256 `C36EF9ABC245A556F39750A37CA63E882DF7CB563BCB1D3F9906EB9A465462A6`, and found no new blocker. The integration reviewer closed the origin/control/accounting clarifications. The evaluation reviewer additionally requested an explicit whole-pipeline interpretation of the existing 256 MiB staging cap; root applied that stricter wording above, without enlarging any allowance. Only this cap clarification and review/status reporting changed after that rereview. Mathematical targets and experimental priority did not change.

These are document-level judgments, not code audits, source-capture execution, native conformance or empirical usefulness evidence. All reviewer handoffs are complete; none retains write or execution authority from this investigation.

## References

- [Strategy decision](2026-09-20-concept-experiment-decision.md) and [executed local checkpoint](2026-09-20-executed-reciprocal-feasibility.md).
- [EXTRACT1: complete source cuts and group recovery](../../notes/analyses/CP-001H-complete-export-and-group-recovery.md).
- [PI1: exact evidence references and grounded composition](../../notes/analyses/CP-001G-proof-instance-composition.md).
- [CLIENT1: local presentation and library correspondence](../../notes/analyses/CP-001G-library-interoperability.md).
- [STRUCT2: bounded formal candidate retrieval](../../notes/analyses/CP-001G-structural-retrieval.md).
- [Pinned source-capture APIs and receiving boundary](../../experiments/lean-feasibility/source-capture-notes.md).

Bibliography entries are intentionally unnumbered.

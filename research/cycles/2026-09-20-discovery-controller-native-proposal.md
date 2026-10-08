# Native controller proposal for full existential Gate B

Date: 2026-09-20. Status: proposed bounded client policy; **not implemented, qualified or run**. Scope is the original [Gate B target, three arms and ten-target corpus](2026-09-20-subtype-composition-contract.md#gate-b-preregistration-target-corpus-and-access-arms). This is an interchangeable local-agent policy, not a mandatory commons prover, network goal registry or mathematical acceptance rule. Root owns integration; this note changes no held contract or completed evidence.

## Decision and target

Retain the full target: given arbitrary `α : Type u`, `β : Type v`, predicates `P,Q`, `f : α → β`, preservation `h`, and injectivity `hf`, construct

\[
\exists L:\operatorname{Subtype}(P)\to\operatorname{Subtype}(Q),\quad
(\forall x,\operatorname{val}(Lx)=f(\operatorname{val}(x)))\land\operatorname{Injective}(L).
\]

Do not substitute projection injectivity for this target. Discovering a function-valued definition, specializing it and solving its residual obligations are important untested capabilities. A direct local construction counts in every arm. Standard `Subtype.ext`, the common interface, pinned `Init` source/catalogue and standard local authoring facilities remain equally available; none is withheld to force corpus use. No model API, new prover, broad mathlib import or advanced unfolding-view search is selected.

Use the existing generic `Lean.Meta.SolveByElim` search with explicitly specified orchestration. Its `intro` and `constructor` options are enabled; its constructor fallback uses `newGoals := .all`. Unlike the `LibrarySearch.solveByElim` convenience wrapper, this exposes an existential's data-witness obligation rather than disabling constructor search. Successful completion is not predicted.

## Owner-side interfaces and persistent state

The controller receives the exact common checked environment, closed formal target, frozen local catalogue/capture policy, arm-specific access capability, provider snapshot bindings and one cumulative budget account. It receives no evaluator role map, producer aliases, Gate A proof, intended witness or answer-bearing conversation. Known-ID access alone includes the three preregistered root hints; discovery does not.

| Interface | Input and output; authority boundary |
|---|---|
| `Solve(E,target,localPool,account)` | Fresh metavariables in immutable checked environment `E`; returns complete candidate, suspended frontier, bounded failure or budget stop. Only native checking and subsequent export/replay establish accepted evidence. |
| `QueryIntent(snapshot,telescope,type,mode)` | A captured actual local obligation and its transitive local-variable context, not an invented desired intermediate result. Metadata adapter returns the selected STRUCT2 token-only predicates and inert descriptor/replay hints. |
| `Admit(snapshot,descriptor,anchorReplay)` | Independently acquire and check the exact complete closure, preserving foundation, interface and representative bindings; return compatible `E'` and its checked handles, or a classified failure. No header/pattern installs declarations. |
| `Commit(E,closedTerm)` | Check exact target correspondence, complete term, actual support, capture/export and fresh replay. Unrelated admitted candidates are excluded from the final least closure. |

Outside **all** Lean saved states keep: immutable environment version, admitted evidence handles, finite candidate/cursor cache, exposed-query keys, pending query intent, stop reason, and spent counters. Proof-state restoration never restores these counters or unread traffic. A result/callback names its environment version; mismatches fail. Candidate caches contain hints or checked handles with distinct states, not foreign acceptance certificates.

## Finite state machine

`READY → SOLVE → {EXPOSE, CANDIDATE_COMPLETE, NONCOMPLETION}`; `EXPOSE → ADMIT_OR_SKIP → READY`; `CANDIDATE_COMPLETE → EXPORT_AND_FRESH_REPLAY → COMPLETE_OR_FAILURE`.

At `READY`, instantiate the original target in a fresh `MetaM` context over `E`; do not migrate old metavariables or universe constraints. The local and checked-candidate pools are rebuilt from the same exact declarations. Within one invocation use ordinary Lean backtracking. Keep `commitIndependentGoals := false`, `exfalso := true`, introductions and constructors enabled, default application transparency, and `maxDepth := 32`. The independent cumulative limits below are necessary: depth can reset for independent goals and does not bound total search.

For the leading syntactic logical skeleton, introduce proposition-valued Pi goals and expose the intrinsic seed `Exists`/`And` constructors with **all** dependent subgoals retained. This is a fixed general logical policy, not a script selecting B's map. Do not lambda-introduce a non-`Prop` function-witness goal before its first eligible exposure. Do not delta-unfold a folded proposition merely to manufacture a preferred query; later local `apply`/introduction may use their ordinary checked conversion.

### Safe suspension, not an exception convention

Lean's backtracker catches exceptions around alternatives and can continue through `discharge`. Therefore **never use an exception as the acquisition handshake**. On the first eligible concrete frontier, write one intent into the bounded outer accumulator and set an exposure barrier. `cfg.suspend` returns true for that goal and every subsequent goal while the barrier is set; `cfg.proc` performs no further construction once the barrier is set. Return residual goals normally. The outer orchestrator reads the accumulator even if another part of search reports failure, discards the entire tentative proof state, and services at most one candidate-admission attempt at that boundary.

A tentative complete proof obtained in an invocation with a pending exposure is not committed first: the declared query-first exposure is serviced, and the proof is recomputed from the original target. This may waste work; its actual cost is reported. Budget exhaustion similarly sets an outer stop flag and suspends further search; it is not a catchable success or an exception that refills fuel. The implementation must demonstrate that barriers and counters survive failed branches before trials.

After a compatible admission, clean-restart over `E'`. After empty results, duplicate/already-held evidence or an admission failure, mark the completed exposure, retain its cost/failure record, and clean-restart over unchanged `E`. No alias overwrite or certificate transfer is permitted. Incompatible acquisition is refused in this first cut rather than invoking another proof-context solver. Every restart, including an unsuccessful exposure, consumes the same allowance. Reserve a restart slot before raising a barrier; when no restart/admission allowance remains, disable further exposures and continue the current local search. Never create a barrier whose required fresh invocation is unfunded.

## Generic candidate selection and query-first exposure

The local pool comprises local hypotheses and all declarations actually admitted in the common/candidate closure, not a hand-selected list of useful theorem names. Local standard-source suggestions may use the equally exposed pinned catalogue through the frozen on-demand capture/check route; those operations share the acquisition and time limits. The entire `Init` environment is not silently pre-admitted. Source aliases and publisher metadata cannot select proof authority.

For each actual goal, generate candidates by their actual types: exact informative result/function-shape buckets first, followed by generic parameter-headed candidates. Retain function-valued **definitions**, not only theorems. Within a bucket use local declaration order for hypotheses and exact typed content-ID order for declarations. Deduplicate exact handles. At most 64 local candidate probes are admitted per search event, subject to the cumulative probe allowance. Ordinary Lean application instantiates parameters and universes and produces every residual obligation; matching a head is not typing. Constructor/lambda construction and standard local support remain fallback alternatives. No requirement demands that a particular contribution occur in the final term.

The metadata bridge accepts only a well-scoped finite semantic expression: instantiate assigned metavariables, close actual free variables over their transitive telescope, retain binder types and exact checked semantic references, and reject any remaining expression/level metavariable or missing correspondence as `QUERY_NOT_REPRESENTABLE`. No metavariable constant ID, proof-instance reference in a semantic type, or source-name-derived identity is invented. This skips that query, not the local proof attempt. Required query-capture bounds are at most 64 telescope binders and the existing native DAG limits; exceeding either is explicit omission. If the separately selected extractor implementation does not support the captured syntax, record `NOT_EXTRACTED`; do not manufacture a completed descriptor or an exhaustion flag. Even supported redex-free inputs retain STRUCT2's prescribed normalization scans and companion-view accounting.

Use mode 2 (`FUNCTION_OUTPUT`) for a non-`Prop` function obligation `B → A`, deriving the informative input/output pair from this actual obligation; mode 0 (`APPLY_RESULT`) for proposition obligations. No mode-1 rewrite or mode-3 binder-domain expansion is selected initially. Use the existing predicate `[6,F,E,mode,sortedRequiredTokens,[0]]`: pattern-free is a selected cheap lane, not stronger matching. STRUCT2 performs its specified raw/beta-zeta extraction only. Request the ordered existing portfolio, but service **one** not-yet-issued lane on the first exposure of a query key; save omissions. For the function case prefer its allowed informative input/output-pair lane before output-head fallback. For proposition queries retain the portfolio's existing ordering. Query keys commit to foundation, extractor, mode and the closed formal view, independent of arbitrary fresh metavariable names.

At most eight distinct lanes/first-exposure keys are issued across the entire arm. For each issued lane, request at most one page from each of the two frozen providers, in preregistered alternating-provider order; use the existing exact page/cursor semantics and canonical descriptor-ID order. This deliberately selects at most 16 pages of the 24-page ceiling, not complete coverage. Deduplicate target/replay hints and allow at most two evidence alternatives per exact target. Select the next unread candidate by lane issuance order, provider turn, then descriptor ID—not evaluator relevance. At most 32 candidate-type inspections share the existing diversity reservations; they confer no acceptance. A missing native type-probe path cannot be replaced by trusting a header.

Each query-first boundary admits at most one fresh candidate. A query key is exposed only once; a later failed local search may consume its next cached candidate under the remaining acquisition/restart budget, selecting the earliest exposed key with unread candidates. This is a fixed heuristic, not complete search. Already-held evidence is recorded as reacquisition and does not create a new mathematical object.

The local-only arm has no external exposure barrier; it runs the same local search with an empty external candidate source. Known-ID obtains its permitted candidates through the same charged admission interface, without a proof sketch. Discovery obtains candidates only from its declared pages. Search stops on a completed checked result after scheduled exposures; it does not reject a direct proof for lacking corpus dependencies. Query-first is an explicitly costed **exposure/conformance policy**. It may be worse than solving immediately; a search hit, fetched theorem or extra dependency is not a benefit claim.

## Bounded generic projection-congruence saturation

At a proposition-search event, before its local application alternatives, permit at most **two rounds** of a single generic operation: from an actual local homogeneous equality `e : a = b`, derive `congrArg π e` for checked nondependent data projections of the equality's carrier. Process at most the first 16 equality hypotheses in local-context order and the first four field indices of each eligible exact one-constructor, nonindexed carrier; perform at most 32 `(e,field)` probes and add at most 16 distinct facts per event. Across the whole arm permit at most 64 successfully constructed facts, including subsequently discarded ones. All probes also debit the cumulative probe account.

Derive field names/indices from actual checked native declarations, not remote structure metadata. For a fresh local `z` of the carrier type, form the candidate native projection and infer/check its type; use it only when abstraction gives a nondependent function. Dependent proof fields are not coerced into ordinary `congrArg`. Use existing `Lean.Meta.mkCongrArg`; verify its returned term/type in the current environment. Unsupported projection generation is a recorded failed probe. The second round sees only earlier-round facts; no unbounded transitive/congruence closure, rewriting catalogue or specialized injective-map lemma is introduced.

Use explicit native projection expressions if needed: reconstructed kernel groups do not automatically carry frontend structure/field metadata. `mkProjection` cannot simply be assumed to work because a group has the familiar source spelling. This implementation boundary must be qualified. Generated facts are local proof terms; their true dependencies, including seed `congrArg`, survive actual export if used.

## One arm, one account

| Resource | Proposed first-cut ceiling; never reset by rollback/restart |
|---|---|
| Whole arm | Existing 300 seconds wall **and aggregate CPU**, 4 GiB private commit, one active child; includes discovery, acquisition, proving, export and fresh replay |
| Solver invocations | At most 9: initial invocation plus at most 8 orchestration restarts, regardless of success/failure |
| Search | Depth 32 per backtrack invocation; at most 2,048 search-event visits across all `proc`, fallback/constructor/introduction and independent-goal entries; at most 16,384 reserved type/application/projection probes total |
| Candidate admission | At most 8 root attempts including standard on-demand support, retries and alternatives; duplicate/failed attempts debit slots; original closure-byte cap unchanged |
| Discovery | One aggregate attempt: at most 8 lanes, 24 pages (this policy schedules at most 16), 10 wall seconds, 2 local CPU seconds, 8 MiB traffic, 64 MiB temporary state; at most 1,536 retained descriptors |
| Congruence | Two rounds/event; 16 equalities, four fields, 32 probes, 16 facts/event; 64 constructed facts/arm |

Charge a search-event visit before executing its action, including failed actions. Where an upstream iterator cannot expose each attempted application, conservatively reserve its entire bounded candidate batch **before** calling it; unused reservations are not refunded. Count wrapper `proc`/discharge work and independent-goal entries, not only successful tactic applications. The discovery deadline is fixed at the first query-planning/exposure operation plus 10 wall seconds; proving, admission or restart does not pause or renew it. Later local solving may continue within the arm's 300 seconds after discovery closes, but emits no new provider requests. All syntax, package and export limits remain inherited. An exhausted allowance stops its funded operation and is recorded; exhausting the whole-arm or search allowance without complete export/replay gives noncompletion. These are policy ceilings, not predicted sufficient resources or a claim that native checking is bounded by the node count.

## Genuine launch blockers and stopping rules

Before any measured arm: freeze and review (1) the wrapper's barrier/counter semantics and complete metavariable closure check; (2) candidate pool/type probing, faithful local catalogue exposure and on-demand admission; (3) formal query capture and the selected STRUCT2/FIND_WINDOW adapter with actual descriptors; (4) native projection/congruence generation over reconstructed groups; (5) isolated consumer accessible inputs and common preparation; (6) aggregate runner/accounting and actual export/fresh replay. No producer body, expected derivation or useful-ID allowlist may leak into the controller's decision policy.

Use a separately labeled, at-most-one-attempt controller-conformance pilot before the three frozen arms; disclose all pilot adjustments, then freeze a new evaluation cut. A narrower projection smoke check is optional within that pilot, never replacement of the full target. Failure to obtain a representable query, useful candidate, closed proof, admissible closure or export ends at its actual boundary; no automatic resource increase, new view theory, answer-specific tactic, hidden source import or additional pilot catalogue follows. Return to the smallest demonstrated blocker. Report completion, acquired-reference use, new-to-consumer evidence and measured cost separately; no novelty, benefit or sustained-growth result follows from conformance alone.

## Inspected pinned sources

All anchors use Lean commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`, inspected read-only in the existing v4.34.0 source tree. No compilation, tests, experiments or model/API execution were performed for this proposal.

- [SolveByElim configuration, constructor fallback and search](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/Tactic/SolveByElim.lean#L95): lines 95–110, 163–164, 203–208, 251–273.
- [LibrarySearch wrapper disables constructors](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/Tactic/LibrarySearch.lean#L104): lines 104–110.
- [Native constructor application](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/Tactic/Constructor.lean#L19): lines 19–30.
- [Application and restoration during matching](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/Tactic/Apply.lean#L169): lines 169–231.
- [Backtrack hooks, caught exceptions and independent-goal scheduling](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/Tactic/Backtrack.lean#L40): lines 40–77, 107–157, 164–199.
- [Meta saved-state restoration](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/Basic.lean#L620): lines 620–626.
- [Congruence builder and projection metadata requirement](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/AppBuilder.lean#L212): lines 212–230 and 516–531.
- [Selected STRUCT2 query contract and portfolio](../../notes/analyses/CP-001G-structural-retrieval.md#selected-local-query-portfolio-and-application-path).

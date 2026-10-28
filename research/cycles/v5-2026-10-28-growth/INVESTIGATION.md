# One source-only discovery diagnostic: destructive observation updates

Date: 2026-10-28. Investigator: fresh_discovery_diagnostic. Status: **one proposed substantive extension, entirely unchecked**. The stopping condition is reached. No further source search, index call, or native action is requested by this investigator.

## Decision and recommendation

The ordinary source route was adequate to identify the existing result, avoid presenting it again as a discovery, and formulate a concrete extension. No index was requested or consulted. This diagnostic supplies no evidence that a new search mechanism is needed, or that the index improves discovery.

The proposed extension admits destructive updates to an observed Boolean property. For finite plans built from total atomic updates, sequence, and unrestricted binary choice, three observation-transfer modes suffice for an exact contextual-refinement criterion. The current write-only map theorem uses only two of these modes; a reset requires the third. The attached `Proposed.lean` is a complete proof attempt for the general statement, with explicit attainable-outcome and observation-realizability arguments. It has not been compiled, imported, or checked.

Recommend that root, if selecting a next mathematical action, consider **one bounded ordinary Lean check of this exact source body using the approved compiled contextual-refinement library**. Its sole retained-theory dependency is `FiniteMapRefinement.Context`. There is no need established here for a new search/index mechanism, cold grounding, a reciprocal exchange, or product mutation. This recommendation is not execution authority. Native failure, if any, must remain a failure of this unchecked candidate rather than being reported as a discovery-tool failure.

## What the corpus already establishes

- `TheoryA.lean` gives directed preservation of idempotent repairs, safe scheduling, and examples showing that mutual preservation does not by itself determine equal outputs. It already distinguishes joint contextual preservation from pairwise preservation.
- `TheoryB02.lean` adds closure-operator hypotheses and proves canonical least fixed results, including equal results from equivalent joint constraints. These are existing results, not contributions of this investigation.
- `ordinary_finite_map_effects/Body.lean` defines finite write-only plans and proves exact nonemptiness guarantees: an initially nonempty input or `mustWrite = true` is necessary and sufficient. The source expressly excludes erase, failure, loops, and guard correlation.
- `ordinary_finite_map_refinement/BodyParametric.lean` proves that implication between `mustWrite` summaries is exactly contextual refinement, with an empty-input witness for completeness. It also supplies the polymorphic one-hole `Context` type reused by the proposal.
- `fresh_recipient/Body.lean` already proves a sequence/choice distribution law for contextual nonemptiness. Repeating this law or another Boolean identity would not be a substantive extension.

All five file hashes matched `CORPUS.json`. Their publication/index coverage was not investigated.

## The single extension

Let `S` be a state type, `A` an action type, `observe : S -> Bool`, and `step : A -> S -> S`. Each action is total and comes with an independently supplied exact observation contract:

`observe (step a s) = eval (effect a) (observe s)`.

The three modes have these meanings:

| Mode | Evaluation on false | Evaluation on true | Meaning for a compound plan |
| --- | --- | --- | --- |
| zero | false | false | A false observation is attainable from every input. |
| keep | false | true | True is guaranteed exactly when the input observation is true. |
| one | true | true | Every outcome has a true observation. |

For an atomic deterministic action the contract is equality, so a zero-mode action actually returns a false observation. For a compound plan, zero is a least-outcome summary; it does **not** assert that all outcomes are false. For example, choosing between reset and write has mode zero but may return either observation.

Plans have `skip`, `atom`, left-to-right `seq`, and `choose`. Both choice branches are possible and the branch selection imposes no shared-history restriction. There is no failure, divergence, guard, or exceptional outcome.

Define the summary `sigma` by:

- `sigma(skip) = keep`;
- `sigma(atom a) = effect a`;
- `eval(sigma(seq p q), b) = eval(sigma(q), eval(sigma(p), b))`;
- `eval(sigma(choose p q), b) = eval(sigma(p), b) AND eval(sigma(q), b)`.

The three modes are closed under both operations. They are ordered pointwise by implication: `zero <= keep <= one`. This gives a constant-size summary per plan, but no runtime cost, performance improvement, or deployment claim is made.

The main proposed law is:

> If both observation values have witnesses `s0` and `s1`, then replacing `p` by `q` preserves the guarantee that every result has observation true, in every finite one-hole sequence/choice context and on every initial state, exactly when `sigma(p) <= sigma(q)`.

The program need not have a finite state space for this law; the syntax is finite and the atoms are total. It applies in particular to finite-state updates. The included Boolean-state instance is finite and supplies an exact counterexample to replacing skip by reset.

### Why the statement is exact

The source proves two complementary assertions rather than relying only on a sound lower bound:

1. **Lower bound.** Whenever the summary evaluates to true on the initial observation, every execution ends with observation true. The sequential case uses monotonicity of the suffix summary in its Boolean input.
2. **Attained minimum.** For every plan and every input state, there exists an actual execution whose final observation equals the summary. For sequence, first select an actual prefix outcome attaining its minimum, then an actual suffix outcome from that very intermediate state. For choice, the minimum of two Boolean observations is one of them, so select the attaining branch.

The second assertion establishes seriality as well as exactness. Universal guarantees are therefore not obtained from empty execution sets. Together the assertions give `Guarantee(p,s) iff eval(sigma(p),observe(s)) = true`.

Summary order is preserved by sequence and choice in either argument, so induction through the existing context constructors gives substitution soundness. For the converse, the hole context at `s0` and `s1` tests both entries of the transfer function. Soundness itself needs neither witness. Completeness needs the two witnesses for this uniform three-mode criterion: if all states have observation true, modes keep and one can be indistinguishable on every actual input even though the abstract order distinguishes them at false.

The proposal contains the full proof attempt for these steps: `execution_lower_bound`, `minimum_outcome`, `guarantee_iff`, `summary_fill_mono`, `contextual_of_summary`, and `contextual_iff`. These names denote unchecked source, not accepted theorems.

### Concrete motivation and nontrivial difference from the corpus

Use map nonemptiness as `observe`. A put has mode one, skip has mode keep, and resetting the entire map to a designated empty map has mode zero. With an explicit empty map and an explicit nonempty map, the proposed law yields a three-class contextual criterion for plans containing whole-map reset.

The current one-bit write summary cannot express this extension exactly:

- Skip and reset both fail to guarantee nonemptiness from an empty input, but a nonempty input distinguishes them.
- Put and skip are distinguished by an empty input.
- A plan that writes and then resets has a write on its path but finishes empty. The attached source includes this exact Boolean observation trace.

Thus all three classes are observationally distinct when the corresponding actions and inputs are present. A summary with only two values cannot completely classify this extended contextual observation. This is a changed capability and hypothesis boundary, not a new name for the existing `mustWrite` theorem.

The HashMap-specific instantiation is explained here but is not supplied as checked Lean. The complete source candidate proves the generic action-contract theorem and the concrete two-state counterexample. It reuses the existing generic context type and does not edit the existing plan language or product files.

### Scope limits

An arbitrary single-key erase does not satisfy one of the three exact observation contracts: deleting the same key can empty a singleton map while leaving a larger map nonempty, although both inputs had observation true. State-dependent guards, partial actions, loops, and branch correlations are also outside the model. An observation-negating atom is excluded by the monotonicity needed to compose minimum observations. No claim of equal maps, equal traces, arbitrary-state semantic refinement, literature novelty, or completeness for these excluded languages is made.

## Actual access and assistance log

The canonical root was explicitly supplied to every shell call:

`E:\Distributed Trustworthy Mathematical Knowledge Network`.

The prescribed guard first failed because direct PowerShell scripts were disabled. After reading the documented remedy in `AGENTS.md`, the process-local command `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <canonical-root>\tools\Enter-Project.ps1` returned PASS. No persistent policy was changed. Guard/instruction reads are excluded from the research-read limit. Root explicitly confirmed that it had read GOAL/NOW and owned global scope; this investigator did not read those research narratives.

The research content reads, in order, were:

| Action | File | Source bytes | What happened |
| --- | --- | ---: | --- |
| 1 | `research/cycles/v5-2026-10-28-growth/SELECTION.md` | 2517 | Full selection read. |
| 2 | `research/cycles/v5-2026-10-28-growth/CORPUS.json` | 1280 | Full manifest read. |
| 3 | `software/v5/concept_episode/TheoryA.lean` | 5724 | Whole file; default PowerShell decoding garbled non-ASCII symbols. |
| 4 | `software/v5/concept_episode/TheoryB02.lean` | 7401 | Same decoding problem. |
| 5 | `software/v5/ordinary_finite_map_effects/Body.lean` | 5482 | Same decoding problem. |
| 6 | `software/v5/ordinary_finite_map_refinement/BodyParametric.lean` | 6902 | Same decoding problem. |
| 7 | `software/v5/ordinary_finite_map_refinement/fresh_recipient/Body.lean` | 1077 | Same decoding problem. |
| 8 | `software/v5/concept_episode/TheoryA.lean` | 5724 | Whole-file UTF-8 reread. |
| 9 | `software/v5/concept_episode/TheoryB02.lean` | 7401 | Whole-file UTF-8 reread. |
| 10 | `software/v5/ordinary_finite_map_effects/Body.lean` | 5482 | Whole-file UTF-8 reread. |
| 11 | `software/v5/ordinary_finite_map_refinement/BodyParametric.lean` | 6902 | Whole-file UTF-8 reread. |
| 12 | `software/v5/ordinary_finite_map_refinement/fresh_recipient/Body.lean` | 1077 | Whole-file UTF-8 reread. |

Actions 3-7 and 8-12 were each submitted as independent parallel file reads. Their order within each batch is a reporting order, not an asserted completion order. Every returned result was inspected. Total displayed source/document content: **12 reads, 56,969 source bytes** (about 55.64 KiB), conservatively counting the garbled attempts in full. Five additional SHA-256 scans read the five source files for identity only, totaling 26,586 bytes. Even charging those separately gives **17 file-read actions and 83,555 bytes** (about 81.60 KiB), within the 20-action/512-KiB allowance. File metadata and tool output framing are not mathematical source content.

No optional operator/index documentation was opened. No search result IDs, prior proof outcomes, NEXT-CENTRAL-DECISION, owner database, network resource, Git state, or other mathematical source was consulted. Vocabulary from the brief was finite-state update, combination, substitution, and observable property. Corpus reading added the specific repair/closure/plan/context/summary names. Because no index request occurred, there is no supported formal query or index-origin result to report.

Root received progress messages and provided mathematical assistance: it explicitly cautioned that universal guarantees over empty execution sets are vacuous and that sequence needs attainable intermediate states; it requested explicit seriality and realizability premises. The candidate's attained-minimum proof and its two observation witnesses address those concerns. Root also asked for a complete unchecked source and honest reporting of ordinary-source adequacy. This result is **assisted**, not an unassisted-autonomy demonstration. No additional investigator or agent was delegated by this investigator.

Only this report and `Proposed.lean` were written, using absolute canonical paths. No source was executed, imported, or compiled. No Lean/native check, service/owner operation, package or product mutation, network access, or Git operation took place. The explicitly required workspace guard was the sole project-script execution.

The corpus/access limits were instructions on a shared filesystem, not technical isolation. Model compute was not reliably metered. There was no comparator or causal efficacy experiment. The diagnostic conclusion is limited to one ordinary-source-assisted proposal that is ready for root review; the broader v5 goal is not evaluated here.

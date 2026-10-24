# Next leverage: ordinary Lean applicability, optional trustworthy interchange

2026-10-24. `growth_payoff`; source/theory-only decision. No experiment, download,
build, product edit or Git operation. This does not repeat the factorization,
recipe, budget or demand-staging arguments. Its new evidence is the actual
applicability machinery already shipped in the pinned Lean runtime.

## Decision

**Consolidate an ordinary-Lean-first use workflow; do not build another
applicability engine or index profile now.** The highest-payoff remaining product
boundary is getting a selected external result into a consumer's ordinary approved
Lean environment with the required assurance, then letting existing Lean tools
find/apply it. The owner-free `produce-baseline` facade under implementation is a
useful part of that boundary; a compulsory new mathematical library ecosystem is not.

This is not a claim that all deployment problems are solved or that no future
retrieval research is worthwhile. It follows from a concrete duplication check:
the basic proposed retrieval/application mechanism exists locally, the custom
retrieval seams already exist, and another index does not supply missing semantic
bridges, incompatible toolchains, absent evidence or untransferred automation.
Generic engineering need not wait for an external user; its supported workflow,
trust boundary and limitations must be explicit rather than advertised as novel
mathematical discovery.

## Actual available mechanism

The retained source under
`software/runtime/lean-4.34.0-windows/src/lean/Lean/` supplies:

| Source | Actual capability | Important limit |
|---|---|---|
| `Meta/Tactic/LibrarySearch.lean` | `libSearchFindDecls` uses a lazy discrimination tree over imported declaration signatures; `librarySearch` attempts applications, invokes a discharger, and returns partial applications with remaining goals/metavariable contexts. | Searches the imported environment, not unknown remote declarations; heuristic, resource-limited, incomplete. |
| `Meta/Tactic/Apply.lean` | `MVarId.apply` infers the actual candidate type, creates dependent argument metavariables, tries definitional matching, processes instance synthesis and returns unsolved goals. | Requires the actual local environment and can be expensive; a type-shaped match is not discharged applicability. |
| `Elab/Tactic/LibrarySearch.lean` | `exact?` and `apply?` expose complete/partial suggestions, including subgoal messages for `apply?`. | Some diagnostic paths introduce sorry; successful diagnostic compilation is not finished-proof evidence. |

Precisely, default `exact?` requires closure and throws when it only finds partial
suggestions. `apply?` and the `collectAll`/`config.all` suggestion branch can reach
`admitGoal`, even when that branch also reports complete suggestions. The term
form `exact?%` uses `mkLabeledSorry` on unsuccessful search. Check the actual final
proof and dependencies, not a tactic-name blacklist: successfully closed default
`exact?` can legitimately construct a finished proof. Advisory suggestions must
be replayed/completed before adoption; a compile exit code alone is insufficient.

The core API already accounts for parameter instantiation, local hypotheses and
remaining obligations. It saves/restores speculative metavariable state. It is
not necessary to implement a second dependent-type unifier to expose these facts.
Use ordinary `apply`/`refine` or the accepted explicit suggested term for the final
proof, discharge every obligation, and retain the existing no-sorry/axiom policy.

Loogle, LeanSearch and Aesop can be useful optional tools when already approved
in a consumer's environment. This audit did not install, inspect or establish
their compatibility. The recommendation needs none of them: the pinned runtime's
built-in `exact?`/`apply?` already gives a concrete existing starting point.

## What information actually blocks reuse?

The obstacles must be separated because different remedies apply:

| Observed obstacle | Missing information or capability | Smallest appropriate route |
|---|---|---|
| A relevant imported theorem is not known by name | Candidate ranking plus local parameter instantiation | Existing `exact?`/`apply?`, local source search and explicit `apply`; do not first convert the local library into another index. |
| A theorem has been found but side conditions are unclear | Actual local residual goals, including instance and conversion constraints | Lean application in that environment; a preview's binder list cannot decide them. |
| A useful vocabulary is unfamiliar | A relation between the local property and an external definition | Existing ordinary body-discovery route is optional advice; actual definition/application still needs checking. No new normalizer is selected. |
| The method needs a relation not yet proved | Mathematical bridge, not another keyword | Explicit existing bridge or genuine mathematical work. The Lean-MLIR refinement/equality mismatch cannot be repaired by a search adapter. |
| A result is outside the imported environment | Obtainable compatible source/package or exact checking evidence, plus adoption permission | Approved ordinary package first; otherwise selected inert export, independent admission and checked local module export. |
| The result relies on foreign tactics/attributes/version conventions | Authoring metadata, approved executable tooling or a supported explicit mathematical application | Keep ordinary package integration where appropriate; portable theorem data alone does not reproduce every tactic database. |

The last two rows are the software's concrete incremental opportunity. An exact
preview already exposes the formal type and identities; another preview object
does not fix their adoption boundary. Once the result is admitted and supplied
through a locally generated checked module, ordinary Lean can reason about it in
the normal context. Raw remote names cannot be inserted into the local candidate
finder before those declarations exist; cached provider success is not an import.

Existing cycle evidence prevents overclaiming: exact-type querying is implemented
but deliberately misses specialization/reduction; the body-discovery discriminator
reduced examined postings while almost doubling search-response bytes, not total
cost. CvxLean already has a substantive ordinary package interface with a different
toolchain, and the inspected Lean-MLIR adapter has an unpermitted axiom. None of
these facts selects another custom retrieval engine as the present bottleneck.

## Falsifiable usefulness region, with a fair comparator

Compare the same supported local goal/context and actual permitted tools. A local
first route is useful when its retrieval/application and approval work is less
than mandatory custom export/index/acquisition for already imported facts, or when
it avoids those operations entirely. This is a concrete elimination of work, not
a lower bound on all other proof strategies. It is falsified if native search is
too expensive, misses the needed method while the existing specialized route finds
it cheaply, or a consumer already has a cheaper explicit application. Therefore
native-first is an optional, bounded strategy, not an unconditional speed theorem.

For an external result, a sharper benefit region is: the consumer requires an
independently checked supported result; executing the new publisher's source or
compiled artifacts is not approved; a willing operator can provide the inert
bundle within the available cost/latency envelope; and the existing admission plus
local module/application route completes within that envelope. This supplies a
**new supported workflow capability**: use that external result without approving
its publisher's executable environment. Current hostile-input assurance and broad
module compatibility still have to meet the release bar; process limits alone
do not establish that assurance.

Two possible claims must remain separate:

- If an ordinary approved/sandboxed package route already finishes the same use,
  this is only a potential cost/integration improvement, requiring a positive
  comparison after accounting for extraction, checks, failed candidates and upkeep.
- If the declared portfolio currently lacks any permitted artifact-adoption route
  and this one fits, it enables the specified reuse procedure under that policy.
  This does not prove the mathematical endpoint was impossible by another local
  proof or that new original mathematics has been created.

Give ordinary Lean/Git all its real source sharing, caches, search, package and
safe-validation options. Do **not** give it a hypothetical completed interchange
tool at zero engineering cost and then conclude that building such a tool cannot
be valuable. Conversely, if both routes actually use this adapter, there is no
intrinsic network advantage: the adapter's shared usefulness is the deliverable.
The comparison is between actual alternatives, while simulation only limits
claims of unique architectural superiority. A real external customer is useful
later evidence of prevalence, not a logical prerequisite to this generic tool.

## One next action

**Select a single coherent native-first public workflow using the existing
producer/admission/module APIs, not a new search mechanism.** Its contract is:

1. Work in the user's approved ordinary Lean project; use local explicit terms
   and built-in lookup/application before optional remote search.
2. For a selected missing result, prefer an approved normal package when suitable.
   Otherwise produce/obtain an inert bundle through the minimal selected facade;
   run the unchanged real receiver admission.
3. Use `owner.py export-module` and its returned module/import directories to
   expose the accepted mathematics to ordinary Lean; use a protected module anchor
   only when its exact existing requirements hold. The module interface is already
   implemented and has scoped retained evidence.
4. Resume the original local goal with normal Lean application and explicit
   remaining obligations. Only a complete checked proof can be contributed back;
   an `apply?` suggestion, successful diagnostic compile or provider report cannot.

The immediate missing glue is a coherent supported invocation/compatibility path,
not a proof-search algorithm. Root can consolidate public commands and guide an
agent through them without introducing another protocol or runtime. Preserve the
current original-reference continuation failure: general original-library metadata
reuse is not passed merely because the simpler checked-module route has prior
evidence. Where that narrower route cannot supply the desired normal project
semantics, report the incompatibility instead of silently switching meanings.

Do not repeat old native/search campaigns to market this as growth. A later finite
changed-boundary check can establish that the consolidated invocation preserves
the existing semantics; useful uptake remains conditional, and public security,
portability, packaging and deployment work remain real release obligations.

**Stop/renavigate trigger:** if this consolidation exposes a concrete missing
local-to-external goal or applicability-data interface that existing Lean cannot
provide, name that exact failure and add only its narrow adapter. Until then,
deployment/workflow consolidation has higher justified payoff than a new matcher,
recipe interpreter, global index or proof-calculus extension.

Root independently confirmed the pinned native source boundaries above. Adopt
this as a **source-only workflow-consolidation contract**: preserve each existing
mathematical/approval boundary, expose the ordinary invocation path, and add no
new diagnostics schema or protocol. Implementation/runtime selection remains
separate. No source claim here upgrades the failed original-reference workflow,
establishes a full security sandbox or completes final v5.

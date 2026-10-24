# Shared search guidance: useful optional advice, not another core protocol

2026-10-24. `growth_hint_route`; source/theory only. No code, build,
experiment, download, protected-state opening or Git mutation.

## Decision

**Reject a new network proof-plan language or hint-replay service as the next
implementation.** Preserve the broader design rule: agents may share fallible
problem-solving guidance as advice, while only locally checked finished proofs
enter warranted mathematics. This can avoid a producer's library closure for
some uses, but the principle and the necessary local application machinery
already exist. No concrete missing product seam currently justifies new code.

The gain is possible when the recipient already possesses the necessary
mathematical premises but lacks a cheap way to select/combine them. Advice can
transfer *where to search* without transferring *what to assume*. It does not
replace the existing inert-import route when a genuinely missing premise is
needed. The product should accommodate both, not force every beneficial
interaction through expensive theorem adoption.

## Precise acceptance and dependency argument

Fix a locally warranted environment K, actual local target G and policy P.
An approved local procedure R consumes bounded advice h and either fails or
constructs a closed proof term p. Require the following:

1. h cannot install declarations, change K/P, run arbitrary commands or choose
   new executable interpreters. Any suggested constant resolves to an actual
   eligible local binding; a printed foreign name is not that binding.
2. R can search, instantiate parameters and discharge obligations, but success
   means an actual p, not a diagnostic, remaining-goal list or success flag.
3. The existing protected checker establishes `K |- p : G`, with the existing
   foundation/axiom policy and no unresolved metavariables or sorry dependencies.
4. Input, decoding, search and checking consume the selected local allowance;
   hostile-input containment remains a separate operational obligation.

Then the conclusion is warranted independently of h's author and correctness.
Indeed h is absent from the final derivation judgment; only K, p and G enter
it. If p uses only K's already warranted constants, no producer-library import
is logically required. This is an instance of the existing consumer-native
evidence argument, not a new theorem or a proof of this implementation's security.

This does **not** erase K's own restoration/dependency costs, make an arbitrary
proof short, or preserve the success of a proof that uses missing foreign
definitions. If advice says "apply L" and L is not warranted locally, R must
fail, reconstruct a valid local proof of L, or use the ordinary adoption route.
Name similarity, a same-looking type and a provider's past success supply none
of those warrants. The historical theorem-erasure issue is not implicated: no
accepted theorem body is replaced or removed by this argument.

## What guidance could transfer, and what it would cost

- A small list of locally available lemma bindings can prune candidate search.
- An instantiation or witness can bypass search for suitable arguments while
  preserving all type/condition checks.
- A decomposition can reveal useful intermediate propositions; the recipient
  must still prove them. An invented premise cannot be smuggled into acceptance.
- A learned ranker can suggest the same choices, without becoming authority.

For a fixed ordinary search policy, a valid early suggestion can skip its prior
failed candidate trials. The avoided work is precisely those trials; charge
advice production, discovery, binding, replay, failures and retention against
it. No universal proof-search lower bound is needed to compare those two fixed
policies. Conversely, no saving follows when local search already finds the
same choice cheaply, the suggested subgoals are harder, or binding/retrieval
costs exceed skipped work. This is a conditional mechanism, not observed speedup.

Allow ordinary Lean/Git the identical advice and approved local tools. There is
then no intrinsic commons-only mathematical advantage. Reliable circulation and
application of useful advice could be an integration contribution; hypothetical
popularity or arbitrarily many recipients cannot establish its net benefit.

## Existing machinery and duplicate-work check

The earlier GROWTH-FIRST-ARCHITECTURE-DECISION already explicitly permits
proof-producing application suggestions as untrusted advice. Its method/bridge
and ordinary-sharing arguments remain applicable. GROWTH-CONSTRUCTIVE-MODEL
already separates untrusted problem-solving knowledge from warranted output.
GROWTH-NEXT-LEVERAGE already recommends ordinary Lean application over another
matcher/recipe interpreter. This investigation does not supersede those results.

Directly inspected pinned Lean 4.34 sources confirm the relevant local seam:

| Source | Relevant existing behavior |
|---|---|
| `Lean/Meta/Tactic/LibrarySearch.lean`, `mkLibrarySearchLemma` and `librarySearchLemma` | Construct a local constant, apply it to the actual goal and attempt residual goals. |
| Same file, `tryOnEach` | Tries candidates, preserves/restores speculative state and distinguishes complete from partial results. |
| Same file, `librarySearch` | Exposes complete or partial applications using actual local context; no remote-import authority. |
| `Lean/Elab/Tactic/LibrarySearch.lean` | Exposes `exact?`/`apply?`; some diagnostic paths use `admitGoal` or `mkLabeledSorry`. |
| `ordinary_lean/CheckedExtension.lean` | Rejects `sorryAx` references and calls `addDeclCore` with checking enabled. |

Thus advice can influence an agent's existing approved search/application
choices. A successful diagnostic compilation is not a finished contribution.
The final ordinary proof and its actual dependencies still undergo acceptance.
These sources do not constitute an implemented remote-hint API, nor establish
that every external suggestion is compatible with this pinned environment.

Arbitrary Lean source or tactic text is **not inert advice**. Elaboration can
invoke executable macros, tactics, extensions and commands. Kernel rejection
afterwards does not undo their side effects. A future automatic replay boundary
would need a small decoded data vocabulary with fixed approved operations,
precise local binding, quotas and failure handling. It must not simply feed
network strings to an elaborator or label all proof-producing code harmless.

## Why not build that boundary now?

A generic proof skeleton format would need binding, universe/metavariable,
subgoal-state, version and replay semantics. A sufficiently complete format
approaches another proof representation; a tiny one may add nothing over a
named lemma and ordinary application. Neither useful coverage nor better
discovery follows from serializing these operations.

The retained SAT proof-search construction is still NO-GO. Advice does not
repair its unsupported cost/representation/query premises or justify rerunning
that experiment. The optional local witness adapter also remains distinct:
its family-specific evidence relation does not establish a general plan engine.

There is presently no supplied supported history where useful advice exists,
the recipient's approved local tools can exploit it, and an absent transport/
replay feature prevents that use at lower cost. Root should therefore **close
this alternative without new implementation**. Keep advice at the optional
agent/tool layer and the existing checked-output return path in the core.
Reopen only for that concrete missing seam, not to increase protocol breadth.

This leaves the final-v5 and useful-growth obligations open. It rules out one
unjustified engineering detour while preserving a real avenue of collaborative
learning that does not require importing every producer's mathematical world.

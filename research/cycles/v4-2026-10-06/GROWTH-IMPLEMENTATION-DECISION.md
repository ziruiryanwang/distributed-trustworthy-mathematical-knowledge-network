# Next growth feature: anyone holding a fragment can seal that exact result

2026-10-06 UTC. `/root/growth_mechanism_v4`. Source/design only, no runtime and
no edits to the selected frontier source. Root agrees this is the next fresh-cut
feature after the current fragment runtime boundary, not an expensive proof
campaign. Read current contributor/fragment/stage code and the existing growth
philosophy; canonical workspace guard passed.

## Decision and the actual missing operation

Add **`prepare-seal --fragment DIR`**, a fresh finite preparation of the exact
received proof for subsequent optional cryptographic certification. It must not
require the original author's Lean source, tactics or help, and must not rename
the theorem. It checks the same pinned relation and uses the existing staged
certificate machinery. The command itself produces READY, never a certificate.

The current successor has these real source boundaries:

- `prepare` requires `--source` and performs conditional native authoring before
  fragment execution or certificate snapshot capture.
- `check-fragment` already loads and snapshots inert input/journal/capsule,
  verifies the selected certified frontier and runs the pinned guest. But its
  CLI fixes `output_mode=fragment`, exports another fragment and terminates.
- `FRAGMENT_CHECKED` cannot be advanced; this is correct and must not change.
- The API says to seal by starting a new certificate preparation. Without the
  new command, a receiver possessing only the fragment lacks the source needed
  by that route. Producing a renamed alias is not sealing the same exact object.

This missing source-free operation prevents a truly independent receiver from
funding a seal when continued inlining becomes too costly. It is more central
than adding a use-frequency score: an investment policy cannot choose an
operation the software does not expose.

## Why this feature wins the next-step comparison

| Candidate | Central payoff | Current obstacle/cost | Decision |
|---|---|---|---|
| Source-free exact sealing | Any receiver can turn an existing bounded delta into a portable certified frontier; enables independent rollover | Existing load/group/capture/advance primitives already fit; small workflow/API seam | Next |
| Bounded search fallback | Limits interference from irrelevant search | Search and contributor already have separate budgets; aggregate autonomous-agent scheduling is not presently controlled by one API | Preserve explicit budgets and document caller composition; do not build a new agent controller now |
| Rent/buy recommendation | Could avoid premature expensive seals | Future savings and true certification price are not generally known; existing observed CPU is not the missing counterfactual | Optional local heuristic later, not a fake 2-competitive product claim |
| Retention/utility ranking | Allocates scarce cache/serving resources | Existing CACHESEL1 concept already covers bounded use signals/bundles; adaptation does not remove the source-free rollover gap | Defer duplicate subsystem |
| Acyclic semantic Definition DAG | Removes the F-closed vocabulary ceiling | New relation/image, dependency semantics and integration required | Next major semantic extension after fragment/rollover usability, not tonight's small patch |

This ordering does not claim source-free sealing reduces cryptographic proving
cost. It removes an unnecessary source/author dependency and permits independent
timing/funding of a real, still-expensive frontier investment.

## Exact deterministic algorithm

Inputs available to a local agent:

```text
adopted installed profile + digest
ordinary inert fragment directory + expected manifest digest
expected output interface ID
fresh operation directory
explicit finite CPU allowance and absolute deadline
```

The fragment already contains the framed proof packet, exact expected journal,
output capsule and genuine-parent **candidates**. A sender's local success flag
is neither input evidence nor a prerequisite. No demand history, natural-language
intention or publisher identity is needed.

1. Bind the chosen manifest bytes to the caller's expected digest; use existing
   strict `fragments.load` to enforce the exact tree, lengths/hashes, profile,
   image, framing, capsule, rank and selected-parent bindings. Require its output
   interface to equal the caller's expected ID. Binding is not proof acceptance.
2. Create a **fresh** certificate-mode operation. Snapshot the exact inert files
   once under `inputs/fragment-0`; record the same immutable fragment binding in
   `state.local_fragments`. Do not open/modify the sender's or a previous local
   operation. Keep its failure/deadline/state unchanged.
3. Use existing `group_parents` to snapshot and actually verify the exact full
   certified-parent journals/receipts, deduplicating only under its existing
   exact-member rules. Bind `state.child` to the copied input, journal, capsule
   and rederived info. Preserve the fragment's packet bytes and target index;
   no re-elaboration, recomposition, renaming or rank increment is necessary.
4. Call existing `op.capture()` **once**. This runs the actual pinned guest as
   snapshot execution with the same expected journal and certified parents.
   Do not first call fragment `execute`, and do not export a new fragment:
   execute-then-capture would duplicate the same local proof checking.
5. Close READY only on genuine capture success and clean worker/resource closure.
   `state.snapshot` and `state.shape` are populated; `state.local_execution`,
   `state.fragment` and `state.bundle` remain null. The command has not certified
   anything. Failure closes under the unchanged fail-not-resumable policy.
6. Any later proof work uses ordinary explicit `advance` on this **new** READY
   operation, with its original immutable budget/deadline. Final bundle creation
   still requires all stages, discharged assumptions and genuine final cold
   verification. The exact original output interface/packet journal is retained.

No automatic advance, budget renewal, proof campaign, remote-source execution
or conversion of a local-status flag into a cryptographic receipt occurs.

The expected manifest digest/interface inputs bind user selection, not political
attribution. The exact received fragment is enough to prepare its seal even if
its original producer disappears. This removes an indispensable-author service
without inventing an indispensable replacement server.

## Concrete patch seams for the next fresh cut

Current inspected source paths are below `experiments/certified-frontier-01/project/companion/`.
They are source evidence, **not permission to edit that selected cut**.

- `cert_workflow.py:check_fragment`: extract/reuse its load/snapshot/group/child
  setup for a new `prepare_seal` function. The last action is `op.capture()`,
  not `fragments.execute` followed by `fragments.export`.
- CLI action construction: add `prepare-seal` with fragment/expected-manifest/
  expected-interface/profile/run/CPU/deadline arguments; default `kind=proposition`
  and `output_mode=certificate`. It is a fresh action, not an `advance` variant.
- Initial state can use the existing V4 shape. `local_fragments` is already
  permitted with certificate mode; `Session.capture` uses only child, parents,
  pinned profile and limits. It does not require a native source file/result.
  Recheck these invariants in the final successor rather than blindly widening
  schemas. A diagnostic root name may be derived from the exact capsule, but
  mathematical identity remains its rederived interface and journal.
- Keep `validate_collection_state`, `begin_attempt`, `advance`,
  `finalize_bundle` and current `FRAGMENT_CHECKED` terminal rules intact unless
  a precise incompatibility is found. Install/profile code pins must name the
  fresh successor; never overlay a used installation.
- Update `CONTRIBUTOR-API.md`: READY from source-free preparation is neither
  local native admission nor a portable certificate. Explain optional later
  sealing and its expense. Existing certified-only consumers need the actual
  final BundleV3, not the fragment or READY report.

No guest, host, checker, foundation, image, crypto system or network protocol
change is needed by this operation's design. Whether the existing implementation
actually composes as described is a focused conformance question.

## Minimal contracts, no new full certificate required for this seam

| Contract | Required oracle |
|---|---|
| Source independence | Input contains no Lean source; prepare-seal never enters native authoring or calls a source compiler |
| Exact identity | Child input/journal/capsule bytes, target, interface, rank and full parent selections match the loaded fragment |
| Genuine checking | Parent verification and actual snapshot relation are required; local sender flags are ignored |
| No double execution | Exactly one snapshot execution; no standalone execute before it and no fragment export |
| Fresh state | New certificate-mode operation; old FRAGMENT_CHECKED/failed state cannot be resumed, changed or budget-extended |
| Correct READY boundary | Snapshot/shape present after success; no local_execution/fragment/bundle; no completed proof stage credited |
| Refusal controls | Expected manifest/interface mismatch, packet/journal change, invalid/missing parent, unknown/expired allocation refuse at their actual boundaries |
| Ordinary later continuation | Existing stage argument generation consumes the exact saved child/parents/snapshot; no need to launch cryptographic stages just to inspect this plumbing |

Native-free mocks may establish routing/state-machine contracts but not actual
guest acceptance. One bounded real snapshot preparation on an already available
fragment can qualify the new end-to-end seam, with changed-source/cost accounting.
The inherited final-certificate path remains separately qualified or limited by
its actual prior evidence. Do not launch another full proof merely to prove this
new source-free input adapter calls the existing mechanism.

## Local decision policy: useful now without pretending costs are known

The immediately deployable policy is a deterministic **eligibility/reason**
decision, not an oracle usefulness score:

- If the local/receiving assurance policy permits bounded fragments and the
  actual selected composition fits its bounds, keep the fragment route available.
- If an explicitly selected consumer requires a genuine certificate, expose
  `prepare-seal` with an explicit new allocation or return DEFERRED_NO_ALLOCATION.
- If a composed delta hits its bound, return NEEDS_SHORTER_DELTA_OR_SEAL with
  the actual bound and exact candidate interfaces. Do not promise a seal will
  make every later proof fit, or choose one using an invented savings estimate.
- If an agent requests sealing for anticipated frequent reuse, accept that
  paid local choice. Any `B`/future-savings estimate is tagged HEURISTIC unless
  the exact two-route rent-or-buy premises in GROWTH-MECHANISM actually hold.

This is enough to make promotion operable. A richer advisory policy can later
consume actual invocations' observed CPU, charged CPU, source/profile bindings,
fragment sizes and exact use events. Charged allowance and measured CPU must
not be mixed, and neither supplies the unobserved certified-reader counterfactual.
Foreign usage reports never authenticate validity or authorize spending.

## Philosophical/claim recheck

The underlying resource-bounded capability interpretation survives this review.
There are two updates to the October 2 wording, not changes to frozen evidence:

1. Its illustrative `Explicit_B` definition required a genuine final receipt.
   With the new declared local-execution assurance mode, accepted evidence may
   instead be a genuine local check of the bounded delta and certified frontier.
   These modes have different trusted components; one must not call local
   execution a transferable receipt. Validity remains independent of intention.
2. Its final call for an actual workload comparison describes the then-unproved
   experimental growth claim, not a rule that theoretical justification is
   impossible. A supplied correct algorithm may have a proved cost advantage
   for a formal family relative to a specified algorithm; exact checked
   transformations and online bounds can justify conditional improvements.

Algorithms and general laws can improve the attainable resource frontier across
many independently chosen inputs. Complementary components may be useful only
together, so raw theorem count and isolated popularity remain unsuitable growth
definitions. The seal operation itself establishes **accessible independent
rollover**, not new mathematical content or exponential growth. Its conditional
payoff is that already obtained reusable capability can remain an affordable
proof frontier for future agents without requiring its author's continued help.

Actual cost savings, demand frequency, broad recall and successful sustained
growth remain distinct claims. Theoretical guarantees should use their explicit
algorithm/assurance/resource assumptions; tests should target the implementation
seams those deductions cannot establish by themselves.

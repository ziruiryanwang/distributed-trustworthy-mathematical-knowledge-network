# Consumer adaptations as reusable capital: preserve the bridge, do not invent a protocol

2026-10-24. Bounded source/theory investigation by growth_architecture_payoff.
No implementation, build, experiment, installation, migration or Git operation.
This note recommends a software decision; it does not establish measured growth.

## Decision

Use **ordinary consumer-owned Lean adapter modules/packages** as the first way to
return useful adaptations. When a consumer has already proved the compatibility
bridge needed for its own work, let it offer that named declaration alongside its
terminal theorem. Do not require either upstream library to merge it first. Keep
the producer's ordinary package interface and optional selected-target export.

The distinction is between publishing a reusable intermediate and publishing
only its consequences. It is not a new mathematical object, a network research
agenda, an automatic generalizer, or a claim that any bridge deserves retention.
The existing implementation already accepts multiple selected target names.
No new contribution schema or proof-search engine is justified by this finding.

## Duplication check: two tempting mechanisms are already covered

The project's v4 `GROWTH-MECHANISM.md`, mechanism C, already proves the exact
stationary rent-or-buy result and identifies shared-cost/expiry failures. Applying
it to adapters would not be a new growth theory. In particular, repeated past
adaptation cost is not enough to promise that a new adapter will work or repay.

`v4-2026-10-06-resumed/PARAMETRIC-COMPILER-DESIGN.md` already separates safe local
abstraction from unjustified generalization of transparent constants. Existing
Lean `Meta/Basic.lean` supplies `mkLambdaFVars` and `mkForallFVars`. Implementing
another lambda lifter would duplicate both the reasoning and available tools.

The method-times-bridge argument, finite budget protection, closure-overlap cost
model and fair ordinary-package comparison remain in the prior native-library
notes. This investigation does not rename them as new results.

## What retaining an intermediate adds

Suppose a consumer checks a bridge `b : B` and uses a method `m : B -> Q` to obtain
`m b : Q`. A declaration exposing only the endpoint interface `Q` generally does
not expose the bridge contract `B` or an independently named way to use it.

**Non-recoverability from the interface.** There is no uniform logical rule
recovering `B` from `Q` for arbitrary `m : B -> Q`. Set `Q = True`; every `B`
admits such an m, whereas `True -> B` is not valid for arbitrary B (take False).
Thus endpoint interfaces alone are not a sufficient interchange abstraction for
all useful intermediate knowledge. This is an elementary counterexample, not a
growth benchmark or an assertion that useful endpoints are normally trivial.

An exact retained proof body or its dependency graph may contain b. We do not
claim those bytes have vanished. The missing capability is **direct, named,
selectable access to the reusable contract** without requiring every later agent
to excavate every encountered endpoint's proof dependencies. Existing package
source browsing may already provide that access; if so, use it rather than claim
an additional network advantage.

Conversely, a named bridge does not imply a useful consumer. Its formal contract
can be too specialized, its dependencies costly, or its imported representation
incompatible. Making it visible is a small option to reuse, not proof of value.

## A constructive promotion rule

For a local agent's successful adaptation, in this order:

1. Identify an **already checked named declaration** that supplies the actual
   missing map, structure laws, representation relation, or applicability proof.
   If it is merely another copy of an already cheaply available bridge, retain
   the original locator or a local alias; do not count another capability.
2. Offer its ordinary package/revision and declaration locator, together with
   its actual imports and toolchain requirements. A small ordinary application
   declaration can show how a method consumes it. The example is reusable advice,
   not an additional truth criterion or a compulsory contribution.
3. Keep the jointly compatible environment explicit. A bridge package may depend
   on both independently maintained libraries; it need not be accepted into
   either parent repository. This removes an organizational bottleneck without
   assuming that direct Git publication is slow or unavailable.
4. Use native package adoption when locally approved and suitable. Only if a
   receiver needs selected inert evidence, select the bridge itself as an export
   target through the existing bounded producer. Existing exact evidence can be
   reused; no fresh owner, universal export, or certificate is required to offer.
5. If the desired reusable bridge does **not** already exist, stop treating
   promotion as free extraction. Generalization or bridge discovery is a new
   local mathematical investment. Its bounded optional selection belongs to the
   agent, not an automatic network obligation.

This rule is constructive because it operates on an actual named, checked
declaration and existing ordinary publication/export operations. It does not
need a classifier deciding whether arbitrary mathematics is important.

The source seam is concrete: `software/v5/ordinary_producer_package/owner.py`
`run_producer` reads the explicit `--output-names` list and passes it unchanged
as `targets` to `produce_bundle`. The installed direct export has retained scoped
evidence; this note does not invoke or rerun it. The default native workflow can
simply include the bridge among named declarations in its ordinary Lean module.

## The coherence condition is not optional

Independent bridge advertisements do not form a freely composable graph of
library names. A usable chain needs **one actual compatible mathematical
environment**, supported universe instantiations, the required endpoint
transports and all residual premises. Toolchain equality alone is insufficient;
different pinned versions can assign different meanings to the same names.

For a sufficient narrow condition, let E be a checked environment containing
all methods, bridges and definitions needed by a selected application, and let
E' be a supported conservative extension that preserves those declarations and
their meanings. The same kernel proof term remains typed in E' by weakening.
This does not imply that rerunning a tactic or type-class search will behave the
same: new registrations can change elaboration. Check the resulting term, not a
replayed success message. Nor does weakening identify incompatible package
versions or show that arbitrary binary artifacts can safely be loaded.

Counterexample to name-only graph composition: one bridge's target is a carrier
with operation `op1`, while the next bridge's source has the same advertised
label but operation `op2`. Their preservation laws need not compose. A checked
coercion/transport between the actual structures is required. No global ontology
or semantic-equivalence oracle fixes this merely by clustering the labels.

Hence preserve adapters as normal jointly pinned modules; do not build a global
bridge-path executor before this ordinary compatibility boundary is usable.

## Cost, useful evidence and the stop rule

For an already created bridge, its mathematical discovery cost is common to
both histories in which the consumer completes the same original task. It is
not erased: it cancels in this particular incremental publication comparison.
Extra naming, source extraction, documentation, offering/indexing, review,
version maintenance, materialization, custody and later independent adoption
remain chargeable. If sharing caused the agent to produce a more general bridge,
that extra work does not cancel. Failed downstream use and irrelevant offers
also count. Use the existing full-cost model rather than invent a new ledger.

The highest-information next observation is a genuine independent consumer that
needs a previously produced adaptation, or a deterministic existing API obstacle
preventing it from being named, selected and used. A terminal theorem count,
proof mentioning the bridge, or second copy of the same example is not that
observation. Source inspection already shows named multi-target selection; no
experiment is needed merely to establish that it accepts a list of targets.

**Software decision:** preserve the ability to publish consumer-owned ordinary
adapter packages and select their reusable intermediate declarations. Do not
commission an adapter miner, generalization service, special bridge registry or
new online investment controller now. If ordinary repository/package sharing
already supplies the same route, expose that route as part of the product.
The commons' remaining value must come from usable discovery, permitted adoption
and availability at acceptable cost, not claiming ordinary abstraction as a new
network invention. This bounded investigation found no additional mechanism whose
expected payoff currently justifies new implementation.

## Sources reused

- `v5-2026-10-22-native-library/GROWTH-FIRST-ARCHITECTURE-DECISION.md`,
  `PRACTICAL-NEXT-DECISION.md` and `DEMAND-DRIVEN-GROWTH.md`: growth/comparator,
  compatibility and receiver-selected materialization premises.
- `v4-2026-10-06/GROWTH-MECHANISM.md`, mechanism C: existing rent-or-buy theorem.
- `v4-2026-10-06-resumed/PARAMETRIC-COMPILER-DESIGN.md`: existing abstraction
  contract and transparent-constant counterexample.
- Retained Lean 4.34 `src/lean/Lean/Meta/Basic.lean`: existing binder-construction
  functions. No runtime or source modification was performed.

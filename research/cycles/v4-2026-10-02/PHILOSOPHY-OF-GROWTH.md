# What growth can mean for a mathematical commons

2026-10-02 UTC. `/root/typed_review`; source/theory checkpoint, no runtime.
Companion to GROWTH-ENDPOINT-SELECTION.md and CORE-MODEL.md. The purpose is
to make the project's philosophical commitments operational and criticizable,
not to declare a single doctrine of mathematics correct.

## The apparent paradox is real but harmless

Fix a formal foundation F and a sound inference relation. Let Th(F) be its
deductive closure. If F proves p, then Th(F union {p}) = Th(F): any derivation
using p can substitute its original derivation. Likewise a safe fresh explicit
definition is eliminable and conservative over the original language. These
are statements about unrestricted consequence, not the cost of finding,
communicating or checking a proof.

Our software cannot honestly call each verified lemma an enlargement of Th(F).
Yet knowing a hard theorem, having a usable named definition, finding a lemma
within a budget, or possessing an independently checkable certificate changes
what finite agents can actually do. Unrestricted logical closure deliberately
forgets those differences. Explicit accessible knowledge does not.

Thus the project is best understood as growth of **resource-bounded,
independently checkable mathematical capability**. It maintains valid reusable
representations and a decentralized route to them. It need not settle whether
mathematical objects exist independently of us to make that precise.

This is closely related to the established **logical-omniscience problem**,
not a new discovery that finite agents have finite resources. Independently read
the complete section5 of the Stanford Encyclopedia's Epistemic Logic overview
on2026-10-02. It describes the implausible closure of an agent's knowledge under
every logical consequence, discusses Hintikka's implicit-knowledge interpretation,
and presents awareness logic's separation of explicit from implicit knowledge.
The overview attributes the early observation to Hintikka1962pp30-31; this
checkpoint did not inspect that book or the original awareness-logic papers.
We reuse the distinction, not their entire modal semantics: awareness by itself
does not provide a certificate, a retrieval route or an accountable cost bound.

An operational distinction for this software is:

```text
Implicit_F(p): p belongs to Th(F).
Explicit_B(a,p;K,pi,run): in the actual bounded run, agent a obtains an object,
  authenticates its exact profile/p-interface and genuine final certificate,
  materializes the selected semantic data and can perform the declared local
  use, all within resource budget B under policy pi and advertised assumptions.
```

The second is a realized execution/capability event, not a claim that p is false
when no peer can currently supply it. Failed retrieval can make Explicit false
while Implicit remains true. A hypothetical existence of some easy algorithm
is not evidence the actual policy found it. Different resource metrics/policies/
network snapshots can give different explicit frontiers. A receipt-check event
without a usable local interface does not automatically satisfy the full event.

## A pluralistic contract, not hidden metaphysics

Several positions are compatible with the architecture:

- A formalist can interpret acceptance as derivability in a specified calculus;
  the exact foundation and checker matter, not an intention to describe an
  externally privileged object.
- A structuralist can regard definitions and theorems as reusable descriptions
  of structures/relations. Exact dependencies preserve what structure is being
  discussed; a changed operation body is not merely another attribution.
- A realist may regard proofs as access to pre-existing truths; publication is
  improved access, not creation of those truths.
- A constructive or computational interpretation emphasizes witnesses and
  algorithms. Prop-only proof erasure is useful for statements, but must not
  erase a data-valued definition needed for computation or make all foundations
  appear equivalent.
- A fallibilist treats the code, formalization and foundational choice as
  corrigible. Mechanically checked results are much stronger evidence than
  unverified claims, not immunity from kernel bugs or an inconsistent F.

The shared operational requirement is conditional, transparent assurance:
accepted statements have the advertised formal derivation under their pinned
foundation/checker/cryptographic assumptions. Different profiles can coexist;
no network popularity vote establishes a foundation's consistency. This is
pluralism about interpretation, not relativism that accepts a failed proof.

## Truth, explicitness, access and usefulness are different predicates

A contribution can be formally valid and still be a duplicate, a tautological
wrapper, unavailable from current peers, unfindable under a bounded query, or
irrelevant to a particular agent. Conversely a definition can be eliminable
and still be a major practical abstraction. Keep separate observations:

| Question | Operational evidence |
|---|---|
| Is it certified in the advertised theory? | Actual receipt and exact profile/interface binding; conditional checker soundness |
| Is it a new byte-level/interface object? | Content/structural identity comparison, not an importance judgment |
| Does it create accessible reusable vocabulary? | Exact definition import and later theorem/type references without unsafe premises |
| Is it currently discoverable/available? | Bounded query/holder outcome under stated coverage/lease assumptions |
| Does it improve subsequent work? | Fair counterfactual endpoint/cost comparison, including investment and failures |
| Is it semantically novel in mathematics? | No general kernel-decidable criterion is claimed |

Acceptance must not require human intention. An unintended theorem that passes
the actual formal boundary is still a theorem of that theory. Intention may
influence a local agent's chosen investigation, just as hardware or interests
do; it is not an input to core proof validity. Evaluation workloads chosen by
an investigator are external scientific instruments, not an intention oracle
inside the product.

## Definitions are compressed shared reasoning, with limits

Writing a named operation lets an agent state general laws once and use the
same exact meaning repeatedly. Inlining its body every time can increase term
size, destroy recognizability and make search compare huge expressions. Shared
names/content IDs preserve abstraction and may reduce representation/search
cost even when elimination shows no new logical strength.

That advantage is not universal. A bad definition can obscure a simpler
formulation; excessive layers can create heavy definitional reduction; changing
a transparent body alters later conversion judgments; and a content ID alone
does not make another peer store the body. The semantic data required by local
computation remains payable. Succinct certificates compress proof of checked
typing, not arbitrary execution or the description of an enormous function.

The proposed initial F-closed safe definitions therefore have a concrete role:
allow local agents to create vocabulary others can use in theorem types, without
assuming new axioms or demanding theorem proof ancestry. Type/body/universes/
hint/dependencies bind that role. This addresses a genuine present limitation,
not a philosophical excuse to call wrappers growth.

## A noncircular measure of useful growth

For a declared reasoner policy pi, external endpoint distribution mu and finite
resource opportunity B, compare independently validated completion events and
capped effort to equal exact endpoints with knowledge K versus K plus objects.
The objects are not useful merely because the experiment counts their own
publication. They must alter a later task outcome or cost at equal quality.

The distribution need not be globally agreed or part of the network. Agents
can disagree about which capabilities matter. A theorem useful to one problem
family may harm search on another; no universal task-independent scalar ranking
follows. Nodes may expose local demand-weighted scores and use-frequency
heuristics while maintaining exact validity separately.

Avoid circularity by freezing target statements, opportunities, baseline access,
retrieval policy and cost accounting before comparing; separate seed production
from held-out downstream tasks; disclose intervention and prior-exposure limits;
and permit the local control any shorter proof, native cache or ordinary tactic
available under the same foundation. Do not define usefulness as being cited
in a proof that was forced to cite it. A dependency occurrence witnesses use,
not necessity or causal benefit.

The marginal savings for subsequent endpoints must exceed incremental
production/setup and actual maintenance/failure costs over the declared horizon.
CPU, elapsed latency, agent tokens, bytes and memory are distinct resources.
When only a subset is measured, the claim must name that subset. Unknown model
compute is not zero. A claimed better success rate at the same finite budget
can matter even when no elapsed-speed advantage is established; lower CPU from
an early failed run is not superiority.

## Important impossibilities and adversarial pitfalls

General semantic redundancy is not a simple hash comparison. Deciding arbitrary
theorem equivalence or whether an arbitrary proposed statement is already
derivable runs into undecidability in sufficiently expressive theories. Bounded
normalization, exact structural fingerprints and learned similarity are useful
filters, not complete novelty or correctness oracles. A failure to find an
equivalent theorem is not proof of novelty; a similar theorem is not an
authenticated substitution.

Automation can defeat an apparently difficult benchmark: a direct recursor
proof, decision procedure or library tactic may solve the endpoint more cheaply
than acquiring its planned lemma. That is valuable negative evidence. It is
not permission to ban the shortcut after observation, add artificial padding,
or force ancestral replay on a warm native control. The existing A/B/E1 map
examples illustrate exactly this danger.

Popularity is observationally ambiguous: usage can indicate utility, easy
discovery, duplicated wrappers, coordinated manipulation or a feedback loop
that suppresses rare valuable work. A local score can combine witnessed
downstream use, saved effort, failure/resource cost and diversity, but should
retain uncertainty/exploration and be replaceable. No score promotes invalid
or unverified interfaces, and no mandatory global usefulness ledger is needed.

There is no sound inference from a growing receipt count to exponential useful
knowledge. Fixed hardware, nonzero per-artifact cost, duplicates, diminishing
marginal benefit and evolving task distributions all matter. A branching
dependency graph can have exponentially many syntactic paths while yielding
few independently useful capabilities. A finite benchmark's improvements
telescope and saturate; sustained claims need new independent workloads and
resource-accounted horizons, not repeated credit for one solved task.

## Direct consequences for v4

First, preserve exact proof/certificate safety while improving locality and
production cost; heuristics must never become acceptance authority. Second,
implement the smallest safe contributed-definition seam so that independently
chosen mathematics can acquire reusable vocabulary instead of staying trapped
in one fixed map/Fin language. Third, assess symbolic iterative-system laws
or later the already known list/fold vocabulary with honest local/exact-reuse/
non-oracle-search controls and paid investment. Fourth, accept a negative
leverage result and use it to choose the next capability, rather than redefine
the success criterion around a happy-path artifact.

This position intentionally leaves foundation interpretation, broad novelty
and universal utility open. Its testable commitment is narrower and stronger:
the same finite agents should demonstrably accomplish more reliable reusable
mathematics, or equal mathematics at lower accountable cost, because of actual
accessible prior work—not because an evaluator declared every new filename
valuable. Until that comparison succeeds, efficient-growth support remains
an architectural objective and empirical hypothesis, not a completed fact.

## Literature inspected

- [Epistemic Logic, section5: Logical Omniscience](https://plato.stanford.edu/entries/logic-epistemic/#LogiOmni),
  Stanford Encyclopedia of Philosophy; complete relevant section inspected
  by bounded read-only HTTPS on2026-10-02. Supports the explicit/implicit
  distinction and warns against logically omniscient agents. Does not establish
  this network's soundness, economics, recall or conservative-definition code.
- Existing project growth-model critique, GROWTH-DESIGN.md under the
  v3-2026-09-27 cycle: finite-resource utility, saturation and reproduction
  caveats inspected. Existing known mathematical workloads and native evidence
  remain distinct from future certified-definition qualification.

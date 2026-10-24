# Growth-first architecture decision: circulate usable methods, preserve ordinary Lean

2026-10-24. Root synthesis following the user's priority correction. This is a
design decision and conditional theoretical argument, not a growth measurement
or completed v5 release. The at-hand public-reference attempt has closed failed;
its successful library intake and native correspondence remain preserved. There
is no live experiment and no new runtime is selected by this note.

## Decision

Develop the commons as an **interoperability layer for independently produced
Lean mathematics**, not a replacement for all Lean packages, a global research
scheduler, or a compulsory certificate factory. Keep repositories and existing
custody/search implementations where they work. A contribution should be cheap
to offer; a receiver should be able to inspect it, acquire the missing warranted
mathematics, and use it in its normal local development.

The most promising growth mechanism is not storing more statements. It is
circulating **general methods together with the mathematical bridges that make
them applicable in other contexts**. A bridge is itself checked mathematics:
an instance of a structure, a homomorphism, a refinement relation, or a theorem
discharging another method's assumptions. No human intention or mandatory task
list enters mathematical acceptance. Local agents still choose their own work.

This does not require a new wire object or identity migration today. Existing
theorems and definitions can express the methods and bridges; exact evidence IDs
can continue to identify witnesses. Discovery may suggest a related bundle, but
that suggestion has no mathematical authority. We first need to know whether
the remaining obstacle is finding the bundle, using it, or checking its evidence.

Package integration does not waive decentralization. A supported publication
must be identifiable independently of a mutable hosting account, obtainable
through replaceable custodians, and checkable without trusting a host's verdict.
A Git host or search service may be one provider, never an indispensable global
authority. An optional local strategy must not be mistaken for a mandatory
network-wide research policy.

## What is established, and what is not

The philosophy and cost accounting already exist; do not spend another cycle
renaming them. Under a fixed foundation, a proved lemma generally does not enlarge
unrestricted deductive closure. It can enlarge **resource-bounded, warranted
capability** by supplying a derivation, abstraction, algorithm or usable interface.
Validity, accessibility, actual use and comparative benefit are different claims.

Use three comparisons:

| Route | What it is allowed to use | What its comparison answers |
|---|---|---|
| Local | Good local Lean libraries, tactics, caches and local generalization | Whether sharing contributes anything beyond independent work |
| Ordinary sharing | The local route plus searchable repositories/packages, mirrors and timely branch publication | Whether our integration removes a real friction |
| Commons | The supported selective discovery, evidence and adoption route | Whether this implementation delivers those capabilities affordably |

Both sharing routes can use the same public mathematical discoveries and good
retrieval algorithms. We cannot reserve an easy tactic or reusable abstraction
for our arm. Common producer work belongs in both totals and cancels in a cost
difference; extra work induced by sharing remains incremental. Same task count,
source-call count, or number of agent turns does not imply equal compute.

The comparator-simulation argument in GROWTH-COMPARATOR-CHALLENGE is decisive:
if ordinary sharing can simulate every relevant commons action with equal
assurance and no greater cost, there is no strict implementation advantage.
That is not product failure. Packaging useful checking/discovery capabilities
on top of ordinary sharing can itself be the useful software. The architectural
goal is public usefulness, not proving that every existing mechanism is inferior.

## A constructive growth mechanism: factor methods from realizations

Fix a common supported formal environment K. Let S be a formal type of structures,
L(s) its explicit law predicate, and, for i=1,...,m, let an accepted method have type

    M_i : forall s : S, L(s) -> P_i(s).

Independently, contributor j supplies a supported structure s_j and accepted
bridge b_j : L(s_j), for j=1,...,n. Provided the actual declarations inhabit one
compatible environment, ordinary application constructs

    M_i(s_j)(b_j) : P_i(s_j).

This conclusion follows from dependent function application, not an unverified
analogy or a theorem about arbitrary semantic equivalence. Required universe,
definition and conversion checks still apply. Distinct owners must independently
warrant their selected premises; another owner's acceptance flag is insufficient.

**Capability theorem.** For any selected finite set E of pairs (i,j), if acquisition
and all required checks finish within their stated bounds, the above construction
gives warranted endpoints for every pair in E. Prove this by checking M_i and b_j
in the common environment and applying the ordinary inference rule. For a chain
of such contributions, induct over the finite dependency DAG. Temporal exchange
can be cyclic; mathematical justification cannot depend on its own future output.

The mechanism factors two independently supplied kinds of knowledge. Its cost
has the form

    shared method/bridge creation and publication, charged once where shared
    + sum over receivers of missing discovery/admission/context costs
    + sum over (i,j) actually used of application, checking and endpoint costs
    + failed searches, service, retention, adaptation and retirement.

The scheme can describe m*n applications using m+n ingredients. This is **not**
m*n new mathematical insights, a lower bound on another solver, or free output:
materializing |E| endpoints incurs their costs. Equivalent instances and wrappers
must not inflate measured capability. A normal parametric Lean library can have
exactly the same factorization. Our potential contribution is getting independent
methods and bridges to their consumers sooner and with less adoption work.

The substantive new object may be a bridge, not another universal theorem. This
avoids repeatedly rediscovering generic facts already in Lean. For example, the
pinned Init sources already contain Function.LeftInverse.injective and
List.foldl_hom/List.foldr_hom. The present flip/involution example and a generic
fold-transport example are useful interoperability checks, not persuasive
comparative growth workloads. No experiment is needed to reject that inference.

## Complementary bundles, not a universal usefulness score

A method and its applicability bridge may each have zero value for an endpoint
when offered alone, but positive joint value. This refutes a general diminishing-
returns assumption; it does not imply that all mathematics is supermodular.
Other methods are substitutes, and larger search spaces can waste budget.

Consequences for architecture:

- Preserve exact premise/type inspection and allow discovery of small coherent
  bundles. Do not admit everything merely to decide whether it might apply.
- Permit explicit proof-producing application suggestions as untrusted advice.
  An actual checked application decides truth; metadata cannot grant a warrant.
- Keep parametric methods and useful bridges as ordinary mathematics. Do not
  invent compulsory global popularity, value, novelty or coordination machinery.
- Local usage is a sensible heuristic for caching, not a proof of causal value.
  Never-used work may be a missing complement; highly used work may be trivial.
- Generalization, distillation and speculative bridge creation are optional
  investments by local agents. They need a plausible demand/cost case; the network
  should not automatically launch them for every theorem.

Explicit arguments are preferable for the first application contract. Portable
mathematical declarations do not currently transfer arbitrary new simp attributes,
instance registrations, notation or executable tactics. These are distinct
authoring facilities, not evidence that a theorem is false. Where they dominate
real usefulness, integration with normal locally approved packages can be better
than enlarging the remote-code trust boundary.

## Why quicker circulation can matter, without inventing proof-search hardness

PRACTICAL-NEXT-DECISION gives the finite adoption-window model. If the same useful
method reaches consumers earlier through this route, the improvement depends on
the number of otherwise uncached opportunities in that window, their successful
uptake, and their actual net saving. Additional service/publication cost must be
subtracted. Direct Git sharing may erase that window entirely; do not assign it
an artificial central-release delay.

A second possible margin is reduced **application discovery**: an exact method
plus bridge or suggested instantiation avoids a specified sequence of failed
candidate trials. This can be analyzed for a fixed local procedure without
claiming to bound all possible mathematical ingenuity. Already available tactics,
cheap type-class search, warm local caches and expensive residual obligations
can erase this margin. Advice must be optional so that an unhelpful suggestion
does not become a compulsory computational tax.

Neither margin requires the service to understand human intention. A local agent
can query formal expressions and decide what to try. Nor does it require online
training of every agent. Training and learned ranking remain replaceable local or
provider choices whose total costs and errors belong in the comparison.

The most concrete adoption-friction hypothesis is **automatic use without
approving a new contributor's executable code**. An exact supported proof-data
object can in principle be interpreted by an already adopted checker, whereas
ordinary Lean source can contain macros, tactics and initializers. This does not
make our current parser/checker a proven security sandbox; hostile-input assurance
remains release work. Nor should the comparison ban a package tool from extracting
the same proof data or using a suitable sandbox. The useful software may be that
reusable extraction/inspection/admission adapter itself. A stronger ordinary tool
that already supplies it is a dependency or competitor to examine, not something
to exclude by definition. Compiler success alone also does not establish that a
result uses only the receiver's permitted axioms.

## External evidence changes the burden of justification

These are inspected primary sources, not independently reproduced results:

- [Is This LLM Library Learning? Evaluation Must Account For Compute and Behaviour](https://aclanthology.org/2026.eacl-long.163/)
  (EACL 2026), sections 3-4 and 7: the authors challenge reuse and compute-adjusted
  gains in three systems, including a detailed LEGO-Prover analysis. Their cost
  matching uses token-based proxies and some model evaluations use subsets. This
  is a warning against our evaluation shortcuts, not proof that libraries cannot
  help. We should separately verify actual reuse and its whole-cost benefit.
- [LeanSearch v2](https://arxiv.org/html/2605.13137v2), sections 4.2-5: the paper
  evaluates related sets of premises, not just individual matching declarations,
  and reports a downstream proof experiment. Its natural-language-assisted query
  route and Lean/Mathlib evaluation are not evidence for our formal-only distributed
  interface, worldwide coverage, or cost advantage. The relevant design lesson
  is to evaluate a usable proof route, including complements, rather than only
  top-ranked theorem relevance. This does not mandate natural language in our core.
- [DreamCoder](https://people.csail.mit.edu/asolar/papers/EllisWNSMHCST21.pdf)
  (PLDI 2021): learned symbolic abstractions and a search policy are developed
  together for program synthesis. It is a precedent for treating abstractions as
  search tools, not evidence that a growing theorem repository automatically
  improves agents or that we should train a model now.

A useful diagnostic would compare the same tools and compute with and without
cross-problem reuse, preserving within-problem refinement. A method mentioned
in a final proof may still be unnecessary; a library-aware process may simply
have spent more effort. Such testing is selected only when theory/source analysis
leaves a decision-changing empirical question. No paid API, model training,
benchmark reproduction or broad test campaign is commissioned here.

## Consequential architecture choices and stopping rules

| Choice now | Reason | What would change the choice |
|---|---|---|
| Ordinary Lean plus checked interchange | Removes the need to abandon useful local libraries | A supported method still cannot be used without new executable metadata or excessive adaptation |
| Native-first, receiver-relative acceptance | Ordinary evidence is much cheaper to supply than compulsory cryptographic certification | A stated cold-access demand repays a supported certificate's full production cost |
| Exact witness identities stay | Prevent unsafe operational substitutions; changing IDs is not needed to study growth | A concrete useful composition is blocked solely by witness fragmentation and has a sound cheaper bridge |
| Existing providers/transports stay replaceable | Reuse working machinery; no mandatory central server | A demonstrated service/availability constraint requires a new transport or index primitive |
| Growth work before further network campaigns | A second exchange demo cannot establish productivity | The causal account selects one precise interoperability or cost premise needing execution |

The next experiment is not yet selected. First choose a substantive independently
useful method/bridge pair, inspect the strongest existing Lean/package route,
and state the surviving friction. If none survives, use the ordinary route and
stop building a bespoke mechanism. If the uncertainty is a deterministic API
boundary, resolve only that boundary. If it is real research uptake, a contrived
small local test cannot settle it; seek later independent usage rather than
inventing a benchmark that makes the answer inevitable.

A candidate is worth working on when its expected effect on this decision exceeds
the time, compute, integration risk and maintenance it creates. That estimate is
a judgment to revisit, not a fabricated numeric ranking. Existing investment is
not a reason to continue a mechanism. Passing a component test is not v5.

### First real-case screen: stopped two low-payoff campaigns before execution

GROWTH-CASE-SELECTION inspects pinned CvxLean covariance reduction and Lean-MLIR
compiler-rewrite sources. The former is substantive parameterized mathematics,
but already package-shared and on a different Lean version; we have not identified
an independent consumer whose adoption our route improves. The latter's exact
refinement-to-equality wrapper explicitly uses an unrestricted axiom, so it is
not eligible under our policy. This says nothing against unrelated checked parts
of that library. Root independently read the pinned wrapper, CvxLean reduction
interface and both toolchain files and adopts these narrow source conclusions.

Neither is selected for porting, proof generation or a growth benchmark. Filling
an unrelated compiler-verification gap solely to manufacture a showcase would
be a poor investment. The source screen reinforces two needs for the product:
explicit supported-version/axiom boundaries, and ordinary package integration.
It does not justify a new network mechanism or a measured growth claim.

## At-hand engineering result retained

Public workflow01 checked the basis and six library units and matched the original
library, then refused protected registration because its file census omitted the
supervisor's 2,012-byte command.json. The records directory is empty. No author A,
author B, generated delta or negative call ran. The failed attempt cost
120.1050634 wall / 77.703125 known CPU seconds with clean process closure.
See ORDINARY-REFERENCE-DELTA-CONTRACT's independent actual audit for exact pins.

A future source repair should narrowly allow the supervisor's bounded diagnostic
file and correct misleading workflow error classification. It must not accept
arbitrary files, promote a saved match into a fresh live event, mutate the frozen
installation, or repeat the successful snapshot copy merely to make a test green.
This deterministic issue does not invalidate the growth mechanism; it does keep
the integrated ordinary-reference endpoint unfinished. Its low-cost repair can
follow this decision without triggering another whole-workflow campaign.

## Prior work reused and audit trail

Read with PRACTICAL-NEXT-DECISION, GROWTH-COMPARATOR-CHALLENGE and the independent
GROWTH-ARCHITECTURE-CHALLENGE in this cycle. Earlier arguments retained unchanged:
CP-001C-growth-analysis (capability, optional-access and branching limits),
v4-2026-10-02/PHILOSOPHY-OF-GROWTH, v5-2026-10-20/GROWTH-OPERATING-REGION,
and v5-2026-10-22-architecture-reaudit/ARCHITECTURE-REAUDIT. Witness-sensitive
computation and proof-identity arguments in CP-001F/G/H remain binding cautions,
not issues to rediscover through another experiment.

The parameterized bridge mechanism also reuses
CP-001G-interface-bridges-and-applications and its independent audit: a map into
another structure yields the actual mapped proposition, not an arbitrary desired
one. Needed laws, residual assumptions and an endpoint transport must be proved.
This is not a newly invented bridge calculus or a reason to recreate those files.

## Demand-selected materialization: next implementation selection

The later source reviews in CANDIDATE-OFFER-CONTRACT/CHALLENGE and
PRODUCER-FACADE-PLAN expose two avoidable prerequisites: producer mathematical
adoption before offering, and exact proof-data export before current exact-index
publication. Exact previews are cheap to read but require proof-derived identities
to construct. They are not a pre-export discovery format.

Select a staged product workflow: ordinary repository/package/source discovery
(untrusted advice), explicit local selection of useful targets, reuse of an
existing bundle or approved-local export, then unchanged exact inspection and
receiver admission. Do not make every declaration enter our representation.
Ordinary package use remains valid when it is cheaper. No automated remote export,
new hint namespace, search protocol or natural-language intent field is selected.
Demand-driven materialization can save unused closure work, but repeated environment
loads, overlapping requests and producer disappearance can erase that saving;
DEMAND-DRIVEN-GROWTH supplies the separately reviewed conditional model.

The immediate useful change is common to both eager and demand-selected use:
expose existing `baseline_production.produce_bundle` as a public owner-free
command. It removes an actual integration gap without committing to a new network.
The target user has a compiled approved local Lean project and selected declarations;
the receiver independently checks exported data. Existing exact bundles need no
new export at all. No claim of measured demand or strict superiority over equally
equipped ordinary sharing follows; this adapter may itself be that ordinary tool.

Root selects **source only** under `software/v5/ordinary_producer_package/`:
fresh owner/profile/controller successors and short usage documentation. Derive
owner from reference owner02, profile from its current loader, controller from
the existing baseline producer. Add `produce-baseline` dispatch before any owner
or custody opening; preserve all existing operations and receiver rules. Reuse
the byte-exact worker and retained native exporter, not a build. Change only the
obsolete controller colocation checks to the exact consolidated layout. Require
explicit project approval/targets/output and one original resource envelope;
report inert candidates, never admission. No dummy owner/context/warrants.

Use one ordinary consolidated package revision when later selected, not a second
product line. Its changed owner/profile source implies a new reference-support
identity; preserve old installations and records, never relabel or silently migrate
them. No compatibility framework is commissioned to keep a fixture warm. This
does not repair the separately diagnosed original-reference import-mode defect.
Candidate ingestion remains optional and unselected. Root retains launch, package,
actual-evidence and Git ownership. Independent source/contract review precedes
any finite changed-boundary test; no experiment is selected by this paragraph.

Root also owns `ordinary_producer_package/cli_controls.py`: focused native-free
argument/dispatch/original-budget checks using explicit support/native doubles.
It must not open a catalog or execute Lean. Source review remains separate from
any test launch; these controls cannot establish installed or mathematical success.

## Subsequent root decision: reuse native applicability, close conversion work

The owner-free producer's installed direct invocation completed with clean closure
in 7.3928916 wall / 4.859375 known aggregate CPU seconds. It returned the retained
six-unit manifest exactly, with mathematical acceptance false. Independent actual
audit is separate; this result justifies the joined public boundary, not growth.
No further exporter expansion, remote conversion service or certificate campaign
is selected by success.

Root read GROWTH-NEXT-LEVERAGE and independently inspected the pinned Lean
LibrarySearch meta/elaborator source. Its lazy local signature search, actual
dependent application and remaining-obligation reporting already implement the
basic applicability machinery. Adopt an ordinary-Lean-first optional local policy;
retain existing specialized remote discovery for missing external candidates.
Do not implement another matcher, recipe interpreter or diagnostics protocol.
Partial suggestion branches can introduce sorry, including all-suggestions mode;
the complete proof and allowed dependencies, not compilation alone, decide admission.

The next selected task is source-only consolidation of one supported reciprocal
workflow through the existing producer, intake, checked-module and ordinary-project
return APIs. It must identify exact compatibility/cost boundaries and preserve the
parked original-reference failure. A new runtime or package requires a separately
justified changed boundary. If the ordinary route is sufficient, use it. This
software can be valuable as the reusable interchange tool itself; it need not
outperform a comparator hypothetically furnished with a free copy of that tool.
No measured uptake, universal proof-search improvement, or final-v5 claim follows.

# CP-001E: preservation over an unbounded operating lifetime

Date: 2026-09-19  
Status: Concept analysis and proposed amendment; no implementation or reliability measurement

This note tests the user's long-term objective against the preservation rules in frozen [CP-001D](../checkpoints/CP-001D-operable-Lean-commons.md). It does not redefine the objective as a short-lived exchange service. The question is how an indefinitely operating mathematical commons can keep accumulating recoverable knowledge, and what assumptions that claim necessarily needs.

## The gap between verification and accumulation

Independent native checking protects a receiver from accepting unsupported derivations. It does not ensure that the proof survives.

Consider a completely honest network in which every new result receives only a seven-day warm-cache allocation. Each agent generates correct results, announces them, and then investigates something else. Suppose no result is reused within its cache term. Every stored closure can eventually expire, even though no proof was false and every service operation conformed.

This is a counterexample to “successful verification and bounded caching imply long-term accumulation.” It does not contradict CP-001D's explicitly conditional availability guarantees. It identifies a gap between those guarantees and the desired product outcome if the deployment supplies no durable preservation.

Likewise, three signed storage observations do not imply three independent or persistent copies. A root must have actual complete retrievable evidence, active local retention authority, and a compatible checking route. A historical promise alone supplies none of those facts.

## Four different positive statements

The interface must distinguish:

| Statement | Sufficient local evidence | What it does not promise |
|---|---|---|
| Checked derivation | Exact successful native replay assessment | Bytes are still retained |
| Locally reusable | Complete protected local replay closure and current admissibility | A different node can acquire it |
| Currently replicated | Complete local copy plus scoped independent-provider observations and appropriate retrieval checks | Independent failure domains or indefinite survival |
| Preserved under policy P | An explicit active preservation allocation and its scoped maintenance/coverage observations | Unconditional eternity, global consensus, or mathematical importance |

The last statement is a scoped operational commitment, not a new truth label or a fifth mathematical foundation. It must name the issuer, selected roots, active terms, observed coverage, resource policy, and failure assumptions.

The corpus need not force every correct result into the last category. It must not report an ephemeral verification count as durable knowledge growth.

## Fixed finite replication does not imply survival forever

### Repeated-interval countermodel

Assume a fixed retained root has r independent copies. During each interval there is probability \(p>0\) that all copies are lost before repair, and assume these all-loss events are independent across intervals. After T intervals the survival probability is

\[
\Pr[\text{survive through }T]=(1-p)^T.
\]

It tends to zero as \(T\to\infty\). Even if \(p=q^r\) is extremely small under a per-copy independence model, no fixed positive p gives an unconditional infinite-lifetime guarantee.

This is a conditional countermodel, not an empirical assertion that actual failure probabilities are known or independent. It is enough to disprove the implication from “r finite replicas with repair” to “guaranteed forever.”

### A repaired-copy continuous-time model

For a less coarse model, let k be the number of complete surviving copies of one selected exact evidence representation, with states \(0,\ldots,r\). State 0 is absorbing **within this model**: no external archive, alternate proof, reconstructive code/shards, or independent rederivation source is included. A hash or empty manifest cannot restore lost bytes. Losing this exact ReplayID's evidence is not automatically irreversible loss of its mathematical judgment; that judgment might have another complete proof. Each live copy fails independently at rate \(\lambda>0\), so the loss rate at k is \(k\lambda\). While \(1\le k<r\), one serial repair facility creates another complete copy at rate \(\mu>0\). At r, repair stops. All repair work and capacity are assumed actually supplied.

This finite-state process still reaches zero with probability one. From every positive state there is a positive probability that the next r transitions contain enough losses and no successful repair to reach zero. The minimum of these finitely many positive probabilities is positive. Conditional survival after successive r-transition blocks therefore has an exponentially decreasing upper bound. Finite positive transition rates exclude infinitely many transitions in finite time; absorption is almost sure over an unbounded time horizon.

This statement is stronger than merely saying that a disaster is possible. Under this explicit stationary model, eventual loss is almost certain, despite finite expected repair time and redundancy.

Let \(T_k\) be expected time to loss from k copies. With \(T_0=0\), define \(\Delta_k=T_k-T_{k-1}\). The hitting-time equations give

\[
\Delta_r=\frac1{r\lambda},\qquad
\Delta_k=\frac{1+\mu\Delta_{k+1}}{k\lambda}
\quad(1\le k<r),
\qquad T_r=\sum_{k=1}^{r}\Delta_k.
\]

For r=3 this simplifies to

\[
T_3=\frac{11}{6\lambda}
  +\frac{2\mu}{3\lambda^2}
  +\frac{\mu^2}{6\lambda^3}.
\]

The expression is finite for every finite positive \(\lambda,\mu\). It can be very large; that still is not eternity. Real correlated failure and variable repair capacity can invalidate the model and sharply reduce actual survival.

No numerical reliability claim is made from this formula. It is an analytic demonstration that fixed replication and fast repair are not, by themselves, a proof of permanent survival.

## Conditional unbounded-lifetime risk control

An infinite-horizon probability bound is possible only with stronger assumptions and appropriate allocation.

Suppose that, conditional on all prior history in which the root survives, the probability of unrecoverable loss in interval t is at most \(\varepsilon_t\). This bound must include the actual retention/repair/observation policy and correlated hazards. Then the union bound gives

\[
\Pr[\text{ever lose the root}]
\le \sum_{t=1}^{\infty}\varepsilon_t.
\]

Thus a summable schedule such as

\[
\varepsilon_t=\frac{6\varepsilon}{\pi^2t^2}
\]

supports an upper bound \(\varepsilon\), with \(0<\varepsilon<1\), if the conditional loss bounds are justified and the policy is actually sustained. Independence across intervals is not needed for this union bound.

Under the much stronger model that interval loss is at most \(q^{r_t}\), with known \(0<q<1\), a sufficient replica target is

\[
r_t\ge
\left\lceil
\frac{\log(\pi^2t^2/(6\varepsilon))}{-\log q}
\right\rceil.
\]

This requires redundancy to grow logarithmically with the chosen interval index, as well as continued repair, supply, and genuinely applicable independence/failure bounds. It is not a production policy justified merely by observing several public keys.

For an unbounded sequence of newly preserved roots, summable per-root risk allocations are sufficient for a nontrivial all-roots guarantee **by this marginal-budget union-bound method**. They are not necessary for every possible joint model: perfectly correlated failures of every root can have collection risk \(\varepsilon\) while every per-root marginal is \(\varepsilon\). Marginal fixed budgets alone do not establish a collection bound; if root-loss events are independent with fixed positive probability, eventual loss of some root is almost sure. One sufficient allocation gives root n a budget proportional to \(1/n^2\), then divides that budget across its maintenance intervals. Actual cost can be prohibitive; this is a statement of the mathematical tradeoff, not a claim of free reliability.

The baseline must therefore present replication counts and observed health as operational facts, not as certified infinite-horizon probabilities.

## Selected preservation amendment: explicit local collection custodianship

An operable deployment should support an explicit durable-preservation role, rather than relying entirely on automatic warm caches.

The selected role is **local collection custodianship**:

1. A node's owner adopts a bounded preservation policy and supplies capacity. No global election, registry, unique-person identity, or universal curator is required.
2. The policy names a finite selected set of exact ReplayIDs or an immutable finite collection inventory. It contains existing mathematics, not unsolved tasks or human intentions.
3. Admission checks the exact union of required bytes, metadata, native profiles/checker materials, pins, and the maintenance allocation. A root is not called preserved before the allocation is active.
4. The custodian keeps one complete local pinned closure and independently seeks additional willing replicas under separate providers' own authority. Remote observations are explicitly weaker than local possession.
5. A bounded local maintenance cursor records integrity-check coverage, observation age, unmet replica targets, and repair progress. Time passing cannot silently upgrade coverage.
6. Automatic cache replacement cannot release this collection's exact promised roots. Any release must obey its actual term/owner policy and active-use/export protections. If custody can end at the owner's discretion, the public description says so.
7. Before a planned release, the node may request a funded handoff to another willing custodian. It does not claim transfer complete from a request, signature alone, or shared storage URL. The successor independently acquires, checks, and funds the closure. Handoff remains conditional on that supplied capacity.
8. If capacity or maintenance falls short, report DEGRADED or UNKNOWN scoped preservation state; stop admitting additional promises before consuming the recovery reserve. Do not invent a global “all mathematics safe” flag.

This is an operational role and schema amendment to be integrated with exact local authority. It does not give its operator mathematical authority or the power to force other nodes to store content.

The selected first profile makes custody policy, status, and handoff intent **local-only operational records**. It does not add a remotely authoritative preservation certificate. Existing exact exports and finite retention observations supply only their already stated guarantees. The [custody contract](CP-001E-custody-contract.md) specifies bounded records and transitions. The first preservation target is complete exact selected replay evidence; preservation of a judgment through substitute proofs requires a newly admitted complete replay and does not silently satisfy an exact-byte promise.

### No concealed permanent obligation

A durable pin survives ordinary process restart, but its permanence is limited by its actual owner-authorized policy and physical failure assumptions. A future contractual storage commitment may require payment, legal enforcement, or cryptoeconomic machinery; none is silently provided by this concept.

The base product can include an operator-configured preservation allocation and make it a clearly distinguished mode during setup. It cannot make a network-level permanence claim if every participant declines that role.

### How automatic selection remains useful

Local usage frequency, downstream checked references, cold replay cost, structural coverage, proof diversity, and resource burden can nominate roots for the custodian's finite selection budget. Nomination does not directly create a pin.

A bounded exploration allocation protects some opportunity for low-demand new material; explicit chosen collection roots protect material the operator elects to preserve. Neither produces a universal notion of valuable mathematics.

Operators need not provide names or credit. They do need to supply actual storage and service if they make preservation claims. Authentication matters only to bind scoped operational statements and authority.

## Capacity accounting for a growing collection

Let \(S(t)\) be the exact union size of selected unique recoverable payload at time t, \(M(t)\) its necessary metadata/checker support, and \(\rho(t)\) the effective replica overhead under an explicitly stated placement model. Required supplied capacity satisfies at least

\[
B(t)\ge \rho(t)S(t)+M(t).
\]

Deduplication can reduce S for repeated exact bytes. It does not guarantee compression of arbitrary future native evidence. A safe representation transformation must preserve its stated exact-byte or judgment-recovery contract and pay construction/checking/recovery costs.

If net newly selected unique bytes arrive at rate g and neither release nor representation saving occurs, even constant g requires unbounded capacity as time tends to infinity. An exponentially growing selected corpus requires comparably growing resources or per-result savings/selection strong enough to change that growth law. A finite rate cap prevents overload, not this long-term capacity requirement.

Different collection custodians can select overlapping or complementary roots. That supports plural decentralized preservation, but overlap does not equal independent redundancy and complementary shards need reachable complete per-root closure. A node's index must not count unavailable shards as current local evidence.

## Required diagnostics

For each named preservation scope, report:

- active retained-root count and exact unique-byte union;
- native checking-material/profile coverage;
- local corruption/missing-byte facts and unresolved incident scopes;
- integrity-scan coverage and oldest unchecked interval;
- actual replica observations, their ages, and the assumptions behind any claimed diversity;
- missing replica targets, repair backlog within its finite admission bound, and repair service received;
- explicitly released roots versus roots whose remote recoverability is unknown;
- total preservation, repair, metadata, transfer, and checking cost.

These are scoped measurements. They do not require logging every research intention or every event in the world. A node can forget detailed histories while retaining sufficient current obligations, exact objects, and bounded aggregated observations.

## Consequence for the project bar

CP-001D's trustworthy contribution/reuse path is necessary but insufficient for the indefinite-accumulation objective without actual durable-preservation participation. The project needs both efficient repeated use and sustained recoverable storage supplied by decentralized custodians.

This note selects that operational role and derives why finite replication alone cannot justify “forever.” It leaves no hidden inference that a signed promise or blockchain history regenerates lost mathematics. Whether a deployment has adequate capacity, failure diversity, maintenance, and adoption incentives remains a real condition to test and sustain.

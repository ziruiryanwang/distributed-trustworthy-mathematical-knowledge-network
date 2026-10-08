# Tentative v3: assurance and large-scale limits

Tentative release argument, 2026-09-30. This covers the actually
adopted certified-collection, local-index/shape, and routed-advertisement
boundaries. The [support report](RESULTS.md) identifies the exact shipped source,
executed gates and remaining qualification gaps. The
[layered guide](LAYERED-GUIDE.md) gives the informal overview.

## The safety claim, stated precisely

Let F be the independently adopted fixed foundation/support policy, I the
adopted checker image, and C the selected body-free formal capsule. A received
bundle contains C, a complete finite collection journal J, a final receipt R
and an exact file manifest. Receiving a filename, hash, advertisement, TLS
response or `verified` field is not mathematical acceptance.

The experimental receiver accepts only after checking the selected policy,
file lengths/hashes, capsule/journal member binding and the actual full receipt
verification for I and J. In the current collection relation, J commits one
or two distinct output interfaces. A receiver of member0 still checks the
**whole** journal and receipt, not a truncated member0 statement. Its receipt
must be final with discharged assumptions; a proof checkpoint is not enough.

The intended conditional implication is:

```text
correct bytes/bindings + sound execution certificate + faithful checker
    => the selected judgement is derivable in the adopted foundation F.
```

This is a conditional composition argument, **not a proved end-to-end theorem
about this implementation**. Truth in an intended mathematical interpretation
additionally requires soundness of F in that interpretation. Derivability in
F and truth are different statements; cryptography does not establish either
the appropriateness or consistency of a chosen foundation.

The outstanding assumptions are substantive:

- The fixed restricted checker relation must faithfully implement the intended
  Lean judgement, and the exported/canonical interface must denote the same
  judgement that local Lean uses. General checker-to-Lean correspondence has
  **not been formally proved** here. Selected native/canonical experiments
  support finite cases, not all Lean or mathlib.
- Hashes must bind the intended bytes; receipt verification must be sound for
  the exact adopted image/journal and its recursive composition. The pinned
  proof system, SDK, host/guest boundary, implementation and compilation/runtime
  are trusted within their declared scope. Construction-specific adaptive
  recursive **production security is not established** by our tests.
- The verifier's own executable, policy and environment must be correctly
  adopted and executed. An attacker controlling the receiving machine can
  change its outputs. Local file/process checks are not administrator-resistant
  isolation or an arbitrary hostile-source sandbox.

A sender's identity, popularity or reputation is not an alternative assumption
for theorem correctness. Pinned TLS supplies endpoint authentication for
transport; it does not certify mathematics. Human intention and political
attribution do not enter the formal acceptance predicate.

## Why a parent interface may replace its proof history

The current relation admits only fixed-support Prop interfaces and same-image
recursion. Output types refer to fixed support, not parent proof constants.
Each selected parent member must match exactly one safe body-free axiom with
the same declaration name, ordered universes and formal type. Extra axioms,
unmatched selected members, colliding names, new nonbaseline definitions and
self/cross-output references are refused. General new definitions/inductives
are outside this profile, not silently treated as opaque certified lemmas.

There are at most eight distinct immediate parent journals and eight selected
members. Rank is0 with no parents; otherwise it is exactly1 plus the maximum
parent rank, with overflow checked. Parents must use the same image/foundation.
One complete receipt is required per distinct parent journal; selecting two
members of the same collection does not create two independent certificates.

Under the assumptions above, an induction on this strictly descending rank
explains composition. A rank0 accepted certificate establishes checked outputs
over F. For a higher rank, every substituted parent proposition follows from
F by the induction hypothesis, while the checker establishes the child from
F plus exactly those propositions. Proof substitution/cut then gives the child
over F. The host must actually resolve every cryptographic assumption and
verify the final result. Merely listing lower-ranked parents does not perform
that discharge.

Rank is a local well-foundedness/binding condition, not a network consensus
height. This argument needs neither a globally agreed ledger nor an ordered
history of all discoveries. Different nodes can hold different subsets without
making certificate validity depend on their catalogues agreeing.

What has actually been observed includes the AB collection's final receipt
and cold check, selected-member A/B receiver positives, a swapped-member
refusal and a genuinely corrupted receipt refusal. The composite TLS02 handoff
preserves its failed transport allocation and adds a separate successful cold
check of the identical acquired copy. That is not a fabricated single-run
transport pass. These results support specific enforcement seams; they do not
discharge the general correspondence/cryptographic assumptions above.

## The locality property—and what it does not say

For an accepted instance, the receiving operation's mathematical inputs are
the adopted policy/runtime, selected capsule, full finite journal and final
receipt. **Transitive parent proof packets are not receiver inputs.** In the
current profile the journal is152 or184 bytes; the adopted AB receipt is223,594
bytes. A selected A receiver does not need B's capsule or either output's proof
ancestors. The completed rank-1 child now has a 152-byte full journal and a
223,530-byte final receipt, with actual same-invocation origin cold verification.
Unresolved intermediate proof checkpoints do not have this acceptance status.

If H denotes the transitive proof-history size, there is no mandatory receiver
step of downloading or replaying all H. That is the architectural advance over
requiring fresh ancestral replay. It is not a theorem that every mathematical
interface, certificate or computation has constant size/time, or that every
valid contribution will fit the current finite verifier limits. Work still
depends on selected interface bytes, receipt bytes, adopted cryptographic
parameters and actual verification. Startup/runtime adoption is also real work.

Producer cost is different. A producer checks immediate parents, elaborates its
own source, saves its own execution snapshot and generates/discharges a new
receipt. Its local stage history, pinned output set and storage can grow during
that operation. The current public controller repeatedly rechecks saved local
state; certificate locality for receivers does not excuse expensive production.
Clean READY continuations preserve one original budget/deadline and charge each
new invocation; they do not make already spent work disappear.

Nor does an opaque theorem certificate replace definition evaluation. If a
future supported proof needs a definition body, reduction, computation or a
new inductive type, those semantic inputs and their checking/evaluation costs
must be supplied or justified by an explicitly extended relation. No such
extension may inherit this profile's claims without new correspondence and
compatibility work. The older native v2 lane remains a different trust/replay
model, not an undocumented fallback that proves this certified lane complete.

## Discovery composes with safety, not with completeness

The core separation is:

```text
bounded untrusted hint -> acquired exact bytes -> independent receipt check
                                              -> usable formal interface
```

Local discovery derives typed bundle/interface/type/symbol keys and a bounded
syntactic conclusion-shape feature. Indexed postings avoid mandatory reads of
unrelated theorem blobs. Shape matching is neither mathematical equivalence nor
a novelty/usefulness decision procedure. An advertiser can publish a wrong key;
acquisition must independently bind the actual bytes to the requested key, and
receipt verification must independently establish the selected judgement.

The routed layer adds small metadata advertisements of holders. A publisher
announces selected derived keys, a consumer follows explicitly admitted
referrals to candidate rendezvous indexes, and a returned ad identifies a holder.
One operation ledger covers the selected lookups/confirmation/acquisition;
failed attempts remain charged. The client enforces finite candidate/RPC/byte/
scan/deadline limits, strict referral progress and endpoint admission. Local
tables and their processing have finite configured bounds, not zero cost.

These controls constrain exposure and prevent a hint from becoming proof
authority. They do **not** imply useful discoverability. At least one reachable
advertisement path must intersect a selected rendezvous view, and some advertised
holder must still possess and serve the bytes within the caller's resources.
Churn, partitions, expired leases, missing placement, popular-key saturation,
spam, stale holders or an eclipsed entry set can break that premise while every
mathematical receipt remains sound. No global all-peer fallback repairs it.

The current unsplit-key, bounded-table profile has no proved logarithmic lookup,
automatic scalable rebalancing or production churn-repair guarantee. Strictly
closer hops alone prove neither reachability nor good global routing complexity.
Replica count alone proves neither intersection nor retention. A response
marked incomplete or exhausted means only what its local cut/lease/operation
scope says; it never establishes that no matching theorem exists globally.

There is a simple impossibility behind that last restriction. Fix a consumer
whose reachable peers are a set U during a partition. Compare two worlds that
have identical bytes and messages in U, but in only one world an unreachable
peer holds a matching theorem. The consumer has the same observations in both
worlds (couple any random choices). Therefore its same answer cannot certify
global absence correctly in both. Global complete/fresh status needs additional
reachability, synchronization or coverage assumptions; decentralization and
valid receipts alone cannot supply them. V3 returns scoped hints and explicit
exhaustion instead of an unsupported global-absence conclusion.

The actual evidence makes these distinctions visible:

| Boundary | Evidence | Not established |
|---|---|---|
| Local unrelated metadata | Selected lookup used62 SQLite VM opcodes at1,000 and100,000 unrelated synthetic rows; no instrumented Python theorem-blob opens. | Constant physical I/O, semantic recall or huge-network routing. |
| Syntactic selectivity | A33-entry differing-shape case finds the target in1,279 reply bytes; the matched same-shape case exhausts16 candidates/16,619 bytes without it. | Universal rubbish elimination, deduplication or usefulness. |
| Routed publication | Fourteen inert groups, plus actual H/E/M/D/C TLS announce/acquire prefix and independently adopted same-copy packaged cold completion. Original allocation FAIL remains preserved. | Natural overlay convergence, huge-network reachability or mathematical growth. |
| Exact transfer/check | Retained TLS02 and routed C-owned copies each have a separately audited fresh full receipt check; these are explicitly composite outcomes. | These composites alone do not establish a completed public contribution/return loop or independent-host deployment. |
| Actual public child cycle | All 122 public production stages, real final discharge/origin cold verification, then ten public peer envelopes and two fresh received-copy cold checks after services stop. | Huge-network search, affordable broad production, net useful-growth speedup, independent hosts or production security. |

Fake transport and synthetic descriptors in the routing tests remain clearly
labeled. Their evaluator's router inventory is not a global roster distributed
to product nodes. The separate genuine-routing gate, package runtime and public
producer continuation retain their own qualification status; this document does
not promote a source plan into an executed result.

## Growth is an economic and empirical claim

In a fixed foundation, valid theorems are already in its deductive closure.
Useful accumulation means making relevant consequences practically accessible
and enabling later independent work at a justified cost—not merely increasing
file, proof, advertisement or certificate counts. Definitions and broader
mathematical support will need their own supported semantic boundary.

A reuse advantage for a matched workload requires total saved search/transfer/
checking/downstream effort to exceed extra certification, setup, failed work,
replication and maintenance costs. Local warm native caches are a legitimate
baseline; they must not be charged fictitious full replay on every reuse. The
AB certificate campaign's 69,638.921875 known CPU seconds is a real producer cost;
small cold-verifier inner milliseconds alone cannot establish net benefit.

Usage-frequency ranking and other heuristic policies may guide local choices,
provided their cost, biases and incompleteness are disclosed. They never weaken
the acceptance predicate. No measured useful-growth speedup or exponential
growth law is established by the evidence listed here. The two central remaining
questions are affordable end-to-end public production/reciprocal reuse and an honest
matched demonstration that selective sharing helps independent agents do more
useful mathematics for their resources.

## Evidence references

- [Collection relation contract](../../experiments/certified-collection-01/CONTRACT.md).
- [Actual final collection receipt audit](../../experiments/certified-collection-01/SUFFIX02-OUTCOME-AUDIT.md).
- [Actual collection receiver controls](../../experiments/certified-collection-01/RECEIVER-RECEIPT-OUTCOME-AUDIT.md).
- [Local indexed-peer contract outcome](../../experiments/certified-indexed-peer-01/OUTCOME-AUDIT.md).
- [Shape selectivity and honest miss](../../experiments/certified-shape-index-01/OUTCOME-AUDIT.md).
- [Actual inert routing outcome](../../experiments/certified-routed-peer-01/OUTCOME-AUDIT.md).
- [Failed TLS02 prefix preserved](../../experiments/certified-indexed-peer-01/TLS02-OUTCOME-AUDIT.md).
- [Separate actual acquired-copy verification](../../experiments/certified-indexed-peer-01/COMPLETION-OUTCOME-AUDIT.md).
- [Public controller continuation limits](../../experiments/certified-collection-contributor-04/CONTINUATION-DECISION.md).
- [Actual final public child](../../experiments/certified-collection-contributor-04/ADVANCE-PREFIX-012-OUTCOME-AUDIT.md).
- [Actual enveloped child return](../../experiments/certified-indexed-return-01/RETURN-ENVELOPED-OUTCOME-AUDIT.md).

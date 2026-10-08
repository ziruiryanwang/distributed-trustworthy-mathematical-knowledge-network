# After the genuine child: next affordable-certification decision

2026-09-28. Research proposal only: **no implementation, build or benchmark is
selected**. Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Reuse the [actual child audit](../../../experiments/certified-importer-probe-02/CHILD-CERTIFICATE-OUTCOME.md),
[prior prover diagnosis](../../../experiments/general-checker-guest-04/PROVING-PERFORMANCE-DIAGNOSIS.md)
and [cost-accounting boundary](CERTIFICATE-COST-DECISION.md).

## Recommendation

Prioritize a small **execution/row-count discriminator for co-checking two new
interfaces in one certified collection**, before another full expensive proof
campaign. Do not prioritize more launcher/hash micro-optimization or a speculative
backend rebuild. If batching does not materially reduce proved work, stop it
and investigate a specifically measured segment-prover bottleneck.

Distinguish co-checking new proofs from aggregating existing certificates.
Aggregation leaves the original theorem-certification cost intact and adds
aggregation work; it may help distribution, but is not the next answer to
expensive initial production. Co-checking could amortize checker/support setup
and trace work; no saving is established.

## Evidence and repeated work

The completed child used 34,315.109375 worker CPU seconds:

- Segment stages: 27,830.625 (81.10%).
- Lift/join stages: 6,378.046875 (18.59%).
- Resolve/finish/cold verify: 106.4375.

These are **whole-stage**, not isolated cryptographic-kernel timings. Outer
controller CPU was 70.1875, about 0.204% of total new known CPU. Eliminating that
entire measured term alone cannot provide a large improvement.

Driver07 repeats parent verification, guest execution and session/snapshot
binding in each of 94 stage commands, followed by one cold verify. Their separate
share inside worker totals is unmeasured; not every repeated check is safely
cacheable. Guest04 `relation.rs:212-335` repeatedly constructs/authenticates
schema/support/DAG data, builds the checker environment and checks the selected
theorem and parent types. Some of this could be shared within one batch; each
new proof and additional trace page still costs work. Neither source size nor
the L/child segment difference identifies a measured fixed startup cost.
The installed prepare timings are not an installed full-proof benchmark.

## Batching changes the theorem being certified

The current guest enforces one selected output theorem. Replacing its interface
field with a Merkle root is insufficient. A new certificate must establish:

```text
Every distinct member committed by (profile, foundation, root, count, rank)
was actually checked under the adopted foundation and authenticated premises,
and every external-premise assumption was discharged.
```

A receiver needs that final certificate **and** membership of its exact capsule.
Membership in an arbitrary root proves no mathematical validity. Required changes:

- Bind domain-separated leaf/root formats to exact member names, ordered
  universes, type commitments, count/index and adopted policy. Reject duplicate,
  reordered, omitted or unchecked members and ambiguous encodings.
- Check every output with exact axiom/support and declaration/reference census.
  Retain the fixed 43-record/66-name, Prop-only restriction. For the smallest
  probe forbid references between new batch members, avoiding cycles or treating
  unchecked neighbours as axioms. Batching does not solve new definitions.
- Fully verify compatible external certificates and discharge assumptions;
  ranks must decrease across certificate dependencies. A member cannot
  authenticate itself through its own collection.
- Adopt a new image/journal/profile deliberately. Current same-image rules do
  **not** automatically admit old-image L receipts into a batch profile.
  Cross-profile compatibility and downstream member reuse are separate gates.
- Bind receipt, membership, exact local import and successor premise to the same
  member. Consumers need only their selected capsule/path/claim/receipt and
  required support, never all batch proofs or ancestral archives. A root cannot
  supply unavailable member or definition data.

## Small prospective discriminator and go/no-go

**A: execution only.** Freeze one new pair of independent ordinary Prop theorems
and exact proofs/interfaces; do not reuse completed L/child certification as
fresh work. Initially use no external parents, avoiding an unqualified image
bridge. Compare two singleton executions with one pair execution; one singleton
under the batch format measures that format's fixed overhead. Hold checker
policy, support, hardware/backend and segment exponent 18 fixed. Record exact
output correspondence, padded rows/segments, full preparation/command CPU/wall,
bytes and memory. Charge new image/build/setup separately.

Proposed go bar, fixed before any run: pair padded rows at most 75% of the summed
singleton rows, fewer segments, unchanged mathematical checks and no exceeded
finite resource envelope. This 25% bar is an engineering selection criterion,
not predicted gain. Otherwise stop: no full batch proof, enlarged budget or
post-hoc addition of easy members.

**B, only after A passes and separate root selection:** certify the same new pair
once as two singletons and once as a batch under matched total resources. This
explicit matched comparison is not rerunning completed project proofs. Include
every attempt, preparation, proving/compression, verification, failure and setup;
report full-pair cost and per-result waiting latency, not only cost divided by two.

Suggested local adoption bars: at least 20% lower steady-profile full-pair CPU;
no worse full-pair wall completion; unchanged 4-GiB worker ceiling; successful
cold member verification/import without other proof bodies; no more than 10%
cold-intake **full-wrapper CPU** regression on this sample, with cold-intake
wall time reported separately. Compare each selected member at the same
verification/import boundary. Report setup separately and include it in any
amortization claim. One pair is scoped evidence, not statistical or corpus-wide
proof of speedup.

Negatives must cover one invalid member invalidating the batch, unchecked/
duplicate/dropped leaves, altered capsule/path and uncertified/wrong-profile
roots. Genuine unresolved-assumption and recursive-member reuse gates require
a later explicitly compatible parent-bearing case; zero-parent success cannot
qualify them, demonstrate reciprocal collection reuse, or establish that a
strictly sequential new-parent chain can usefully be batched.

Batching couples availability and latency: one bad member or waiting producer
can delay another. Keep singleton contribution available; batching is optional
local policy, not a global task queue. No result here establishes useful growth,
exponential accumulation or an economic break-even reuse count.

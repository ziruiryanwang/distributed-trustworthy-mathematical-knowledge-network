# Complete retained aggregate path: independent non-memory feasibility review

Disposition: **a finite, unchanged-graph non-memory profile exists, conditional
on its artifact/cost caps; no proof production or memory-sufficiency claim**.
The retained `s=113,m=1,po19` capsule does not require a geometry redesign merely
to fit command-line, serialized-composite, read, history or retention bounds.
The earlier illustrative 1 MiB artifact cap did not establish the 64 MiB
internal-composite constraint. A 512 KiB cap repairs that arithmetic condition.
Whether genuine artifacts and execution costs fit is a separate obligation.

This is source/data inspection only. No product import, test, build, SDK edit,
proof operation, allowance or Git mutation occurred. Root owns adoption and
launches. The genuine no-host constructor/request preflight is a disjoint
assignment; this note does not substitute hypothetical records for actual
adoption evidence. See `REAL-PRODUCER-PREFLIGHT-DESIGN.md` when finalized.

## Exact scope and sources

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
The guard passed on resumption. Current reviewed bytes:

| Source | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/aggregate_resources/producer.py` | 44720 | `1d191bdc2079760ce89a57a08924254f01487d24726e10b386c7eca1ef9eec09` |
| `software/v5/aggregate_production/stage_host.rs` | 22515 | `5865e6afb30bd81adb79d6fe04e09ac8bb7238b40956284fa3bcd2d4da4fe102` |
| `software/v5/aggregate/receipt.rs` | 3631 | `41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254` |

SDK source prefix `S` below means the retained
`experiments/general-checker-host-05/build-01/source/risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8/risc0`.
This review reuses `AGGREGATE-BUILD-OUTCOME.md` for the actual linked host and
`PROVER-MEMORY-REVIEW.md` for the memory obstruction; it does not repeat either
campaign. `SMALL-SEGMENT-DESIGN.md` concerns an alternative geometry, not the
113-segment object reviewed here.

The actual retained capsule is 37,187,089 bytes, SHA-256
`7996306944a51e0eec597266819871115f4bdea1f799c944442e472869465ffd`, under
`experiments/v5-local-checks/frontier-capability-execution-01/evidence`.
Its fixed per-host inputs total **39,372,335 bytes**:
1,745,920 image + 215,540 wire + 192 header + 37,187,089 capsule + 223,594 I receipt.
The graph has 340 host calls: 113 segment, 113 lift, 112 join, one resolve,
one finish; 339 produce checkpoints. No ancestry of earlier mathematical proofs
is included in this new aggregate's segment count.

## Finite least-change profile

Keep the adopted image, capsule, host, graph, verifier and SDK unchanged. Choose
512 KiB artifact limits and 64 KiB for each stdout/stderr stream, for every kind.
These are proposed local resource caps, not measured output sizes or funding.
Use the previously quoted CPU caps 1700/250/250/600/300 and wall caps
420/150/150/600/120 for segment/lift/join/resolve/finish respectively. The sums
remain 249250 worker CPU seconds and 81930 worker wall seconds. The whole
allowance ceilings remain 250000 worker CPU, 3600 controller CPU, 86400 wall,
2 GiB retained output and 8192 entries. There is only 750 CPU seconds of
worst-case reservation slack; failures cannot receive an automatic fresh budget.

Memory must be selected explicitly under `PROFILE_V2`. Neither the 8192 MiB
policy maximum nor these non-memory inequalities establishes sufficiency or
current physical/commit headroom. The proven unchanged-po19 lower bound exceeds
5.33 GiB; the separate memory review remains controlling.

### Internal composite serialization: the previously missing condition

`stage_host.rs:307-326` encodes the entire tuple
`(Vec<SegmentReceipt>, Vec<InnerAssumptionReceipt>, Digest)` under a **64 MiB**
serializer bound. Final receipt size and 512 MiB total reads do not imply this
intermediate fits.

For fixed-integer bincode, each vector prefix occupies eight bytes and Digest
occupies 32, so the tuple adds 48 bytes beyond its elements. The segment
checkpoint envelope occupies `64 + len("segment") = 71` bytes. Consequently a
successfully admitted 512 KiB segment checkpoint contains at most `524288-71`
bytes of the same serialized SegmentReceipt used in the composite.

The one erased-claim assumption is no larger than its 223,594-byte original I
Receipt. Source justification: `S/zkvm/src/receipt.rs` defines Receipt as inner,
journal and metadata; its journal vector contributes at least eight bytes and
metadata Digest contributes 32. Both the original InnerReceipt::Succinct and
new InnerAssumptionReceipt::Succinct use a four-byte enum tag. The succinct
fields otherwise stay identical (`receipt/succinct.rs:258`), with the claim
replaced by MaybePruned::Pruned(Digest), 36 bytes. Even bounding the old claim's
serialized length below by zero, removing at least 40 outer bytes pays for
those 36 bytes. The actual nonempty journal only tightens the inequality.
This uses the inspected pinned serde layout, not a universal SDK-version rule.

Thus the actual finish tuple has the conditional upper bound

`113 * (524288 - 71) + 223594 + 48 = 59,460,163 < 67,108,864 bytes`.

The looser bound omitting checkpoint overhead is 59,468,186 bytes and also
fits. This proves serialized length under selected successful artifact caps,
not peak resident memory: decoded segments, cache copies and tuple bytes can
coexist. If an actual segment exceeds its cap, production stops; this note
does not assert that arbitrary valid segment receipts fit 512 KiB.

### Native reads versus complete controller input inventory

Finish reads all 113 segments plus the resolved prefix. Its host-read upper
bound is `39,372,335 + 114*524288 = 99,141,167 < 512 MiB`.

The controller's `_request` is stricter in a different way: it retains every
successful checkpoint, not just dependencies consumed by the next host. The
five exact snapshot records have lengths 9281, 2125, 2542, 562 and 1230 bytes,
total **15,740**. Snapshot executable `aggregate-host-build-01/aggregate_host.exe`
is **6,626,304** bytes, SHA-256
`b1605995c957e06b7c4529d28dfc2a49e496cefae7629b3fdddfc4a1bfb6f6d1`.
`_snapshot` adds that executable, not only its name, to session pins.
The fixed request inventory therefore totals **46,014,379** bytes.

Even immediately before finish, with 339 maximum-sized checkpoints and the
maximum admitted eight MiB of prior reports, the request inventory is at most

`46,014,379 + 339*524288 + 8*1048576 = 232,136,619 < 536,870,912 bytes`.

Installation/profile pins are separately checked against their own 512 MiB
envelope in the constructor. They are not accidentally charged as per-host
inputs by this calculation. Within `run`, newly saved controls, reservations
and stage results also become rebind inputs; the source does not reapply the
512 MiB request-sum assertion after every insertion. Their bounds belong in
retention and controller-work accounting, not an invented cumulative host-read
guarantee. Actual constructor adoption remains the no-host preflight's job.

### Retention, reports and bounded continuation

Each stage's conservative reserve is
`0.5 + 0.0625 + 0.0625 + 2 = 2.625 MiB`, with eight entries.
A single successful full-path quote is **896.5 MiB / 2724 entries**.
Allowing a separate four MiB / four entry administrative envelope per attempt,
even 17 attempts quote **960.5 MiB / 2788 entries**, below 2 GiB / 8192.
These envelopes assume the selected per-stage limits and small records fit;
sampled filesystem census/log limits are not hard disk quotas. Failed partial
outputs remain charged. They cannot be erased from the continuation history.

The current protocol allows at most 16 prior attempts. It need not make one
attempt per stage: a five-stage pilot followed, if separately selected, by one
335-stage remainder fits in two requests. If shorter batches are desired,
`5 + 15*21 + 20 = 340` fits exactly 17 requests. That latter schedule leaves
no spare attempt slot; a failed attempt may exhaust its continuation plan.
All choices preserve one exact profile/session/allowance/budget/carry lineage.

For the ordinary ASCII attempt paths below, a pin or retained-checkpoint row
is below 512 encoded JSON bytes. A generous successful-report bound is
`(339 retained rows + 340 stage pins + 16 prior pins + 2 control pins)*512`
`+ 16 KiB = 373,248 bytes`, below both one MiB/report and 512 KiB/report.
The 16 KiB remainder covers the fixed report schema, bounded budget/carry,
numeric observations and envelope. Hence at most 16 such prior reports occupy
less than eight MiB. The request is smaller: it does not inline stage reports
or ancestor JSON contents. This proves a finite naming/batching profile can fit;
arbitrarily long owner-supplied paths are not covered. Exact future requests
still undergo the actual encoded-size checks, and failure diagnostics/oversized
records must not be silently treated as a successful-path bound.

### Windows finish argv: actual normal-path arithmetic

Use the uncreated prospective base
`experiments/v5-local-checks/aggregate-production-planned-01/attempt-XX`
under the canonical root, with `XX=01..17`. Generate the unchanged graph and
place its stages in the `5 + 15*21 + 20` schedule. The 113 segment paths and
one resolve path are 155..157 UTF-16 code units each. Use the actual retained
image/wire/header/capsule/I paths and actual stage-host executable path.

The full finish argv has **128 arguments and 19,227 UTF-16 code units including
spaces, required quotes and terminating NUL**. Windows' 32767-unit boundary
therefore leaves **13,540 units**. The paths are ASCII without embedded quotes
or trailing backslashes, so ordinary quote-if-whitespace accounting is exact.
This was computed as data in PowerShell, without launching the command or
creating the prospective directories. Two-attempt naming has the same lengths.

This is a real solution for s113, not a general escape from Windows argv limits.
Adding path nesting or raising the segment count changes the inequality.
The smaller-geometry review already demonstrates a different profile that
does not fit; it must not inherit this result.

## Controller cost remains quadratic in stage count

Every `rebind` rehashes all installation pins and every accumulated input pin.
There are two such calls per successful stage, plus initial/final calls per
attempt. New checkpoint pins are appended after the successful stage rebind.
Thus the repeated-artifact component is proportional to
`sum(j*a_j)`; it is O(H^2) for similarly sized artifacts, not O(H).
The output census likewise repeatedly visits retained entries.

For the illustrated 17-batch schedule, cumulative end counts sum to 2940.
Bounding each rebind's retained artifact bytes by 512 KiB per completed call,
the `rebind` subset alone is at most
`[340*339 + 4*2940]*524288 = 66,595,061,760 bytes` (62.021484375 GiB).
There are at most `2*340+4*17=748` such fixed-input/installation rebind passes.
Constructor, `_request`, individual checkpoint checks and source/adoption checks
add further reads. This is a conservative successful-path byte-work quote,
not a timing upper bound or an actual measurement.

The 3600-second controller cap cannot be justified from bytes alone; storage
throughput, antivirus/interference and Python/hash overhead matter. Do not turn
these small metadata limits into a claim that control overhead is negligible.
Conversely, this finite quadratic cost is not a source-level proof of failure.
No expensive proof run is needed to identify the structural cost. Any future
optimization must preserve mutation/conflict checks or replace them with an
explicitly justified immutable-input/owner model, not merely remove checking.

## Appendix: is complete-composite finish necessary for sound acceptance?

**No, not for the current receiver predicate under the already explicit
recursive-soundness assumptions. Yes, it is part of the currently selected
producer workflow contract and therefore cannot be silently removed.**

Let `A` be the independently adopted image, `H` the independently selected exact
aggregate header, and `V` the adopted non-dev verification context. Define

`Accept(A,H,R) := genuine succinct Poseidon2 R; R.journal = H;`
`R.verify_with_context(V,A) = success; H parses and binds A/foundation/policy.`

This is precisely the substantive final application predicate in
`software/v5/aggregate/receipt.rs:32-79`. The current receiver already accepts
this receipt without any segment/composite input.

The source argument is:

1. `S/zkvm/src/receipt.rs:156-194` checks inner/metadata parameter consistency,
   verifies the inner receipt, and compares its complete claim digest with
   `ReceiptClaim::ok(A, journal_digest)`.
2. `S/zkvm/src/claim/receipt.rs:79-99` fixes success exit, starting image,
   expected output journal and **zero unresolved-assumption digest** in `ok`.
   Therefore integrity of an arbitrary conditional claim is not sufficient.
3. `S/zkvm/src/receipt/succinct.rs:105-213` checks trusted verifier-parameter
   digest, proof/circuit version, hash suite, control inclusion, recursive seal,
   inner control root and authenticated claim digest. No ancestor proof vector
   is an input to this verifier.
4. `S/zkvm/src/host/recursion/prove/mod.rs:219-250,737-778` shows resolve proves
   a recursive predicate supplied with both seals, the exact head assumption,
   its compatible control root and the remaining tail. The host-side claim
   rewrite alone is NOT the assurance argument; the recursive predicate and
   its verifier are essential. The source's final claim comparison enforces
   that all remaining assumptions have actually disappeared.
5. Under the adopted adaptive, branching, multi-claim recursive soundness,
   collision binding and exact image/checker correctness assumptions, this
   accepted claim establishes the grounded aggregate relation. The relation's
   seal-height and mathematical-rank induction then gives the selected member
   validity, as stated in `v5-2026-10-12/DELTA-SEALING-POLICY.md:208-227`.
   A source trace is not a new cryptographic security theorem; the open theorem/
   parameter/audit mapping in `v5-2026-10-07/ASSURANCE.md` remains open.

Current `stage_host.rs:307-326` additionally reconstructs the full composite,
checks every segment and chaining, verifies assumptions through that route,
and compares its claim to the capsule and expected claim. This is a separate
producer consistency check and defense in depth against construction/recursion
implementation mistakes. It checks the same target by a less compressed route.
It does not make the remote receiver independent of recursive soundness: the
receiver is not given that composite, and the producer's report is untrusted.

A future explicitly selected **frontier-only finish** may therefore take just
the final resolved succinct checkpoint (or final joined/lifted one for m=0),
verify it under V, require the exact `ok(A,H)` claim, construct R, and rerun
the unchanged full `verify_aggregate`. Keep non-dev, exact adopted A/header,
parameter/hash-suite and unresolved-assumption refusals. Never replace the
cryptographic verification with a saved success flag, capsule hash or host report.
It is mathematically sufficient for the stated receiver predicate even if the
certificate was produced through another valid execution yielding the same H;
it does not attest the owner's chosen production history or its resource costs.

Such a successor would remove the final all-segment argv and composite
serialization coupling. **It would not alone remove** the controller's retained
checkpoint inventory/O(H^2) rehash, the complete capsule, s<=128 graph restriction,
prover memory requirements, or all required SDK correspondence work. It must
be a new producer contract/source/build with explicit loss of the independent
composite cross-check, not a retroactive claim about the current linked host.
Retain old evidence; keep complete composites as an optional separately funded
diagnostic/audit if desired. A real fresh succinct final artifact is still not
available from this aggregate path, and this appendix does not manufacture one.

## Root decision supported

For the retained s113 path, proceed with the small genuine no-host preflight
before selecting any proof expenditure; there is no demonstrated non-memory
static obstruction under the finite caps above. Do not infer cap sufficiency,
memory availability, successful production, positive growth benefit or v5
completion. Independently, a frontier-only producer successor is a defensible
architectural simplification if root chooses to remove final whole-session
reverification; it should be assessed against its lost diagnostic value and
other remaining whole-session dependencies, not sold as a complete scaling fix.

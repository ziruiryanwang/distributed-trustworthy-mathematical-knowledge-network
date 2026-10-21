# Next growth decision: incremental native admission

Status: source/theory decision, 2026-10-21. Author: core_growth. Root owns
selection, integration and execution. No new run or certificate is selected here.

## Concrete choice

Implement a bounded, same-live-owner memo of exact native conditional-check
results. A newly extended packet must still establish its entire current graph,
but need not rerun the native checker for an unchanged witness already checked
successfully by that owner. This is one receiver successor, not a new checker,
proof guest, packet format, trust mode or certification campaign.

The currently installed receiver is selected through
`experiments/v5-local-checks/distribution-terminal-i-01-input.json`, SHA-256
`d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0`:
`software/v5/runtime_efficient/mixed_claims/receiver.py`.
The later independently qualified standalone-validation receiver,
`software/v5/standalone_validation/mixed_claims/receiver.py`, SHA-256
`835d59809045c3e49f9d7e5483108f4034c591a3a82224e4155f4f7d0f6dcced`,
is the proposed successor basis. Its phase/import changes can be batched with
this substantive feature instead of recopying the installation separately.

## Existing mechanism versus actual gap

Whole-packet facade caching already exists. Mixed reception also caches genuine
I/A receipt handles. General exact-J sealing preparation and typed-row checking
already exist; do not implement them again.

However, the native witness loop invokes the native subprocess for every witness
in every newly admitted packet. Extending M to M+V misses the whole-packet cache
and rechecks M. Mirror03 exercised precisely this pattern: owner one admitted M
then M+V; fresh owner two admitted M+V then M+V+W. A fresh owner must initially
check its own native material; its later extension need not repeat that work.

This removes repeated mathematical checking rather than another filesystem guard
sweep. The native costs in the retained small workloads were small; controller
costs dominated. Consequently there is no warranted numerical whole-workflow
speedup claim and no reason to rerun mirror03 to advertise one.

## Exact contract

1. A memo record denotes a successfully checked **conditional relation**:
   exact immutable canonical witness bytes, exact returned J, exact ordered parent
   journals, rank, image, foundation, policy and owner profile. It does not assert
   that its parents remain mathematical premises forever. A digest may locate a
   record, but exact byte equality must establish witness equality.
2. On every admission, parse and validate the submitted packet normally; rebuild
   its current graph, receipt/member frontiers, ranks and target closure normally.
   Before inserting either a reused or freshly checked J, establish all its exact
   parents in that current graph. Current valid premises need not have the same
   historical receipt representation as the earlier successful admission.
3. Retain the original owner/source/pin/adoption/deadline checks and the pre/post
   native-loop frontier checks. Only an actual miss writes a native input and
   launches/checks a subprocess. A hit is reported explicitly as reused native
   validation; never fabricate stdout or a fresh process-success report. Native
   input readback is required for actual executions, not for an uncreated hit
   input. Packet readback, final closure and final live checks still apply.
4. Pending records become reusable only after the complete packet passes all
   final validation and live-handle promotion conditions. A failed native prefix
   never seeds later reuse. Owner revocation/failure clears retained and pending
   records. No serialized report, disk cache, foreign owner or caller-supplied
   hit count grants reuse authority.
5. Retain records only for the most recently completely admitted packet, with
   explicit limits of at most the envelope's delta count and at most the
   envelope's witness-byte allowance, never above 16 records and 16 MiB total
   canonical witness bytes. Count actual retained byte lengths; do not assume
   canonicalization is length-decreasing. Skip retention when a bound would be
   exceeded. Atomic replacement after success drops old entries; dropping or
   evicting an entry can only cause an ordinary future miss.
6. Preserve attempts, submitted bytes, per-call resource checks and the original
   full-graph native/receipt CPU reservations, including hits. No refunds, larger
   caps or miss-only funding are introduced. The existing output-census reserve
   can remain conservative. Observed worker CPU includes actual processes only.

The record is private live implementation state. As with current live handles,
this assumes execution integrity of the owning verifier, rather than security
against arbitrary mutation of that Python process. Existing exact journal and
content-identity cryptographic assumptions remain; witness memo equality itself
does not add a hash-collision assumption if exact bytes are compared.

## Why this preserves the mathematical acceptance argument

Assume the unchanged native checker soundly establishes its exact bound relation
for a witness under its exact ordered parent journals. A completed successful
admission therefore supplies a genuine observation of that relation, not an
unverified claimed J. Equality of all relation inputs makes a reused observation
the same conditional result as reexecuting that deterministic checker.

For the new packet, induct over its checked topological witness order. Frontiers
are established by the current live receipt/member obligations. Each native miss
is checked normally; each hit supplies the identical previously established
conditional relation. In either case, every exact parent is already established
in the current graph, and the existing rank and actual-graph checks apply.
Therefore each inserted node and the final closed target have the same warranted
status as before. Old frontier authority is neither retained nor substituted.
Eviction affects cost only; failed admissions contribute no reusable records.

This is a refinement argument conditional on the existing checker and binding
correctness, not a new proof that the checker implements all of Lean correctly.

## Warranted cost consequence and limits

Consider one live owner receiving prefixes of n distinct native witnesses. If
each prior prefix fits the retained record/byte bounds, the old path executes
1+2+...+n = n(n+1)/2 native checks; the proposed path executes n. This counts
checker invocations, not uniform-cost steps. More generally its eliminated worker
work is the sum of the costs of the exact repeated native checks it avoids,
against added bounded lookup/equality/record bookkeeping costs.

Parsing, canonicalization, witness transfer, current premise validation, closure,
needed semantics and packet storage remain cumulative. The current packet limit
is 16 deltas; this is not unbounded ancestry elimination or cold-owner scalability.
Full-graph reservations remain unchanged, so this first slice does not admit more
contributions under a fixed reservation grant. A future miss-only grant would
need an immutable owner-generated plan and atomic check-to-use across acquisition,
facade and receiver; caller hit counts and informal refunds are not safe substitutes.

An equally optimized local/shared-library comparator must receive the same memo
optimization. This is an operational prerequisite for economical incremental
reuse, not proof that network sharing beats such a comparator. The conditional
growth/operating-region results already recorded in GROWTH-OPERATING-REGION and
BENEFIT-CASE remain conditional: no supported positive full-cost margin is yet
demonstrated for the current small workloads. Do not convert author timing into
a universal lower bound on rediscovery cost.

## Smallest changed-boundary evidence

Independent focused controls should cover exact repeat versus changed witness,
J/parents/rank/profile binding, current missing or invalid premises, failed-prefix
nonpromotion, closed/foreign owner exclusion, final-check failure, byte/entry
overflow as a safe miss, and honest hit/process accounting. Reuse must still
fail when the current packet lacks a required exact parent.

Root may later select one short genuine prefix extension to connect the focused
controls to real native checking. No old successful circulation, broad suite,
new prover, new guest or expensive certificate is required for this decision.

## Central unresolved work remains explicit

Ordinary native sharing is a project capability, not an adversary every succinct
mechanism must beat. Renewable economical certified frontiers and a supported
full-cost benefit case remain unresolved. This bounded refinement does not solve
them or justify a v5 release. It is selected because the exact duplicate work is
present in the real reciprocal path, the acceptance argument is local, and the
implementation boundary is one receiver file. Reassess after this slice instead
of building another general advisor, synthetic profit workload or speculative
certification campaign.

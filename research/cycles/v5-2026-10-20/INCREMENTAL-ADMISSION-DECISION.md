# Same-live conditional-witness memoization: defer on measured payoff

2026-10-20. Source and saved-data inspection only. No implementation, imports,
tests, native calls, proof runs, memory investigation or Git changes.

## Decision

**The narrow optimization is coherent and not already implemented, but do not
implement it now.** In the actual continuation, the two repeated native calls
account for only 0.0625 recorded CPU seconds, including their supervisors, and
0.1692674 wall seconds. Removing every recorded second of those blocks would
represent approximately 0.148% of the run's known CPU and 0.213% of wall time,
before introducing memo lookup/accounting costs. This is not the highest-payoff
next step and does not resolve first-time recipients' proof ancestry.

The initially conspicuous five calls versus three distinct witnesses is a real
redundancy, not evidence of a large cost. The saved timing changes the priority
decision. Preserve the design below for a workload where repeated native work
is demonstrably material; do not launch a benchmark just to justify this cache.

## Current selected implementation, not a stale predecessor

The installed logical `sdk/v5/mixed_claims/receiver.py` is exactly
`software/v5/runtime_efficient/mixed_claims/receiver.py`: 24,253 bytes, SHA-256
`aa591a1829deff82576ba30af484ab560ee04900200fd79ac93c19a9c2c7bf7f`.
The installed manifest and both files were read and matched. The synchronous
pin-phase optimization described in `INSTALLED-COST-DECISION.md` is already
present. Do not propose it again or calculate savings against the older source.

The selected receiver still launches every parsed native witness at lines
280–301. Its existing `_cache` stores same-live I/A receipt handles, not native
conditional results. The facade's `workspace_mixed._admit_packet` instead keys
the entire packet by hash, length and requested summary. The changed child
packet correctly misses that cache even when two contained witnesses recur.
The selected pin-phase optimization changes neither fact.

`LOCAL-CACHE-DECISION.md` concerns a different, deferred facility: persistent
trusted acceptance across restarts. The proposal here would stay private to one
already-live mixed owner; no disk trust store, new issuer or restored handle is
needed. Existing producer checkpoint caching and guest proof memoization also
do not implement this receiving-side optimization.

## Actual cost that could be targeted

Evidence comes from the already-audited operation
`product-local/v5-distribution-connected-01/context-commons/operations/` followed
by `f3bf4210934ebc0da8d26c220522fd9916b78106f0961c33e3bbedc6fa3ba41f`.
All values below are the saved `delta/{admission}/process-{index}.json` values,
not new measurements. Supervisor CPU is separate from that subprocess's Job CPU
but already included in the whole run; never add it to the whole run again.

| Admission / delta | Job CPU seconds | Supervising CPU seconds | Wall through cleanup |
|---|---:|---:|---:|
| Input / 0 | 0.015625 | 0 | 0.9814232 |
| Input / 1 | 0.015625 | 0 | 0.0601282 |
| Output / 0, repeated | 0.015625 | 0.015625 | 0.1097512 |
| Output / 1, repeated | 0.03125 | 0 | 0.0595162 |
| Output / 2, new | 0.015625 | 0 | 0.0600199 |

The repeated witnesses are exactly 105,541 and 104,388 bytes, with hashes
`2cdef224538a722c…` and `4ded495098397d44…`. The output contains a third new
96,190-byte witness. Whole known CPU is 42.28125 seconds and wall is 79.3818659
seconds; all five native blocks total only 0.109375 recorded Job-plus-supervisor
CPU seconds. The first native call's larger wall time is not charged to either
later repeated call in the proposed saving.

These recorded blocks give a gross attributable ceiling for eliminating just
those launches in this run, not a counterfactual end-to-end speedup bound.
Controller hashing, parsing, process setup outside recorded spans, receipt
verification and authoring have different accounting boundaries. Their split
is not established here. In particular, neither "the rest is all hashing" nor
"memoization saves 40% because two of five calls disappear" follows. Skipping
existing pin checks would be a separate intervention, not free memo benefit.

Repeated report SHA-256 values:

- Output / 0: `ad3a20593176ac1975e050affafc355653b5a35000baf1d040b2bc8b539d53e9`.
- Output / 1: `0fd98923fe40a7a1571158c6cd2b156d69929921d1bff5f93e04b8b5bf37cfd1`.

## Why a future same-live memo can be sound

Under the existing adopted-checker/runtime assumptions, a successful checked
witness establishes a conditional relation, not unconditional acceptance:

```text
Check_P(w) = (J, [J1, ..., Jk])
    means: Valid_P(J1) and ... and Valid_P(Jk) imply Valid_P(J).
```

A private memo may remember that exact conditional result. On another receive,
the current graph must still establish every exact ordered parent before adding
J. Induction through the unchanged topological graph then establishes the same
target validity as re-executing `Check_P(w)`. The memo does not discharge a
parent, create a certificate or replace a current live I/A frontier.

The minimum boundaries would be:

1. Entries originate only after an actual supervised native success, clean
   closure, input readback, adopted-source checks and exact `bind_native` result.
   A caller report, saved stdout, ModuleID or summary cannot populate an entry.
2. Use the same owner and exact adopted profile. Index by witness hash and length
   if useful, but compare the complete immutable canonical witness bytes before
   reuse. Retain exact J and ordered parents. Different proofs, parent orders,
   ranks or same-ModuleID/different-J variants are not interchangeable hits.
3. Retain fresh parsing, input/resource bounds, source/runtime/profile checks,
   current live frontier checks, parent establishment, rank checks, closure,
   expected target binding and final promotion checks on each call. A remembered
   conditional result is usable with different valid evidence for the same
   exact premises, never with merely similar premises.
4. Any owner failure, pin/profile/origin change, expiry or close revokes and
   clears the memo together with existing handles. No persistence, cross-owner
   borrowing, restart import or ordinary API for restoring entries.
5. Retain all original packet/proof bytes for export and cold recipients. Memo
   hits skip local execution only; they do not remove required transmitted
   evidence or silently turn an unsealed native contribution into a receipt.
6. Explicitly bound retained unique witness bytes and entry count within the
   original owner envelope. A full memo may decline new entries; it must not
   extend its budget. Preserve existing conservative CPU reservations initially,
   including hit reservations. Distinguish actual executions from memo hits in
   evidence; never manufacture another process-success record on a hit.

Existing input/operation caps already make the submitted history finite, but a
new retained memo still needs a deliberately chosen storage cap. Different
future CPU-reservation treatment would require an additional accounting review;
no allowance saving should be claimed merely from avoiding a launch.

## Relative priority

For a repeatedly extended unchanged chain, native check invocations could in
principle fall from the sum of all submitted prefix lengths to the number of
distinct witness bytes. Packet parsing, transport, graph checks and retained
evidence may still grow with all submitted prefixes. This is not an overall
linear-cost theorem, and independent cold owners receive no such warm benefit.

Affordable certified frontier creation and renewal remain the central scalable
receiving obligation: unlike this memo, a real compact certificate can help a
fresh independent receiver avoid ancestral proof replay. The current evidence
does not justify diverting implementation effort from that issue to save two
very short native calls. Reopen this memo only when a supported use case and
saved evidence or a convincing resource model show substantial repeated native
cost. This note selects neither a proof campaign nor another cost investigation.

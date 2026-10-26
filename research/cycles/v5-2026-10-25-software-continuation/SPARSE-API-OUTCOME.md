# Sparse-access API controls: saved-outcome audit

2026-10-25. Reviewer: `ordinary_routing_gap`.

**PASS for the selected native-free Store/query/SearchSession boundary.** The
saved result records all 13 grouped controls passing, with clean process closure.
The selective access path returns the identical original proved candidate while
reducing scanned entries from 3 to 1 and record probes from 7 to 4 in the fixed
fixture. **It does not establish end-to-end speedup:** charged SQL work is 3900
in both paths and hash calls are 1592 in both paths.

This audit reads retained inputs, source, results and accounting. It reruns no
test, imports no product module, opens no retained SQLite database and changes
no experiment state. The reviewer did not author the test harness, but authored
the candidate-query/provider changes; their separate independent source reviews
are required and are not replaced by this outcome review. Full v5 remains open.

## Identity and execution binding

Run: `experiments/v5-local-checks/sparse-access-api01`.
Package: `experiments/v5-local-checks/sparse-access-assembly01/assembled/package`.
All relative paths in this note are beneath the canonical project root.

| Item | SHA-256 |
|---|---|
| Selected package PROFILE | `97f93cc66f77ebcecd7a3a341baaaf4725236a8dec5fb9cee3c3e67d478f2834` |
| Original and saved selection | `650639f5c3a14a9cb488c0e950b495675ad8b08a31682d4087e6f371e56c4ed9` |
| Test, original and frozen source | `54a5c9b9b3f660f98e93cb3ea8b13ed37bda9c0626c38ce7b763122319447f3f` |
| Runner, original and frozen source | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |
| Suite RESULT.json | `56c7cb351503afffbefd695c23097c3d9b23bd2b8326b78d0605a0f2e124247c` |
| Outer RESULT.json | `1f173cea85a2c41fc958aab4e426637d6283713b2ba5e0b250df15ae49ebf8fe` |
| Command stdout | `1b7ac56d415eb99e7c5eb61a6dc89913b2d079d2db8c0e202e3e3dd90883a93f` |

Independent read-only hashing found zero mismatches among all 161 external pins
(152 package files and 9 runtime inputs), both source pins at original and
snapshot locations, and all 17 fixture texts. Fixture hashes were recomputed
from their retained UTF-8 text, not inferred from a PASS label.

The command receipt and outer report agree with the selected isolated Python
invocation (`-I -S -B`), canonical cwd, explicit package/profile/runtime paths,
fresh suite output and original resource envelope. The stdout and suite-result
text are identical after trimming terminal whitespace: stdout is 2813 characters
and suite RESULT.json is 2812. Their unequal byte hashes do not conceal a JSON
content difference. Stderr is empty. No evidence bytes were normalized.

## What the controls actually establish

The independent [source review](SPARSE-TEST-SOURCE-REVIEW.md) inspected the full
test and its genuine Boolean/integer-alias controls before execution. The saved
result satisfies those assertions, including the following distinct boundaries:

- Same common-prefix records, snapshots, summaries and original vector proofs
  with/without optional pair access; duplicate admission is a no-op. Reopening
  retains exact configuration, and persisted `max_rows: true` cannot alias 1.
- The fixed late AB hit has original anchor ordinal 2. The sparse seek returns
  that same hit/proof; opposite-anchor and old-cut checks do not substitute a
  new vector, admit a later companion or ignore an additional query conjunct.
- Disabled, ineligible and third-anchor requests retain atomic fallback, while
  enabled-but-corrupt access refuses instead of silently falling back. Recorded
  refusals include missing access table, `CANDIDATE_PAIR_COMPANION_CUT`,
  `CANDIDATE_PAIR_ADMISSION_CUT` and `ACCESS_NOT_READY`.
- Twenty-two positive-reply mutations, mode/shape/proof binding and strict
  cursor controls reject malformed replies. V1 retains its original
  ordinal-distance condition; V2 does not pretend sparse distance is a count.
- Meter exhaustion preserves continuation without skipping the pending hit;
  whole-envelope byte refusal likewise does not advance it. Connection progress
  callbacks and busy-timeout settings are cleaned up.
- An actual SQLite trigger aborts the second orientation after the first insert.
  The test checks all expected logical tables roll back, then closes/reopens and
  performs a subsequent valid admission. This is transaction-abort evidence,
  not a process-kill or hardware-failure durability test.
- Independent row/byte quotas produce `ACCESS_ROW_CAP` and
  `ACCESS_LOGICAL_BYTE_CAP`; duplicate-at-cap remains a no-op. The multi-pair
  fixture charges 2 access checks, 4 inserts and 840 logical bytes.
- The ordinary-preview path uses the real adapter and derived identities, but
  the fixture remains **unproved metadata**. Its export is
  `1ea7020561852034e244bceba8f2ecd31a4b246596f3feb69d7f93c245c810ed`,
  namespace `d966de54aa32c6cd059ab9553a0968a320594a63561cadf742cca6265858079c`,
  record `ef4bf07f65677aac4a71d744e5547482bd9c1765a3ecc38ca48ae8ab1ca5644a`
  and partition 30. This is not Lean acceptance.
- Real SearchSession success, failure, wrong-version, malformed-proof and
  abandonment paths retain held-schema/default-V1 behavior and consume the
  selected reservations without duplicate settlement, refunds or new coverage.

The old and new snapshots are respectively
`6a7084a768213b2d714304d45717d17acd37b30af0a1a7b6b859bb68641fa854`
and `0f07b14339f3cc5ab75fe096c62b2f57f234ecdaf8a145c3ef17829ece358008`.

## Locality discriminator, not a speedup result

| Recorded counter | Atomic | Sparse |
|---|---:|---:|
| Scanned | 3 | 1 |
| Record probes | 7 | 4 |
| Record loads | 1 | 1 |
| Proofs | 1 | 1 |
| Node reads | 34 | 34 |
| Hash calls | 1592 | 1592 |
| Charged SQL VM steps | 3900 | 3900 |

SQLite reports an indexed primary-key search over
`(anchor, companion, partition, anchor_ordinal)` with lower/upper ordinal bounds.
The test also checks the actual range access, not merely the readiness probe.
This supports the claimed replacement of irrelevant anchor enumeration by a
pair-selective seek in this fixture. It does not establish large-network recall,
predict a runtime crossover, pay for index maintenance, or justify materializing
arbitrary pairs. Static bounded opt-in pairs remain a workload-dependent choice.

## Complete recorded resource accounting

| Scope | Recorded amount |
|---|---:|
| Outer total wall | 3.0868176999501884 seconds |
| Command through-cleanup wall | 2.842050800099969 seconds |
| Suite wall | 2.3930677003227174 seconds |
| Job user CPU | 1.65625 seconds |
| Job kernel CPU | 0.640625 seconds |
| Job combined CPU | 2.296875 seconds |
| Outer runner/wrapper CPU, separate | 0.515625 seconds |
| Harness CPU, nested within Job accounting | 2.234375 seconds |
| Peak Job private commit | 34,955,264 bytes |
| Stdout / stderr | 2813 / 0 bytes |

Do not add the nested harness CPU to Job CPU or sum overlapping wall scopes.
The original outer limits were 120 wall / 90 CPU seconds, 768 MiB, 3 processes,
and 1 MiB per log. Internal limits were 90 wall / 60 process-CPU seconds. No
allowance renewal is recorded. The harness reports zero native and socket calls
and forbids child/shell/socket launch entrypoints.

The outer result is `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit 0, direct child
reaped, Job closed, zero active processes and zero cleanup errors. It records
2 total processes, zero terminated processes and no termination request.

## Adoption boundary and next decision

The finite API/DB/protocol gate passes for these exact frozen bytes. Public
HTTP/CLI forwarding, live directory integration, native mathematics, crash-kill
durability, global semantic recall, end-to-end benefit and useful concept/theory
growth are not established by this run. No further run is selected by this
audit. A separately reviewed small public forwarding check can cover the
remaining changed interface without repeating native/contact campaigns.

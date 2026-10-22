# Exact-packet controls02: independent actual outcome

2026-10-22. Reviewer: `storage_outcome_audit`.
**PASS_TWO_CORRECTED_FIXTURE_CONTROLS; NOT_MATHEMATICAL_ACCEPTANCE.**

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Evidence: `experiments/v5-local-checks/exact-packet-controls-02`.
This review only reads saved files and hashes source bindings. No tests, imports,
database connections, new runtime, secret reads or Git mutation were performed.

## What actually passed

The saved test result and complete stderr independently agree on exactly two
selected tests, both passing, zero failures/errors/skips. They are the inherited
04/05 bodies from frozen controls01, using the reviewed fixture-only adapter
`b3e0411e...`. There are no forbidden calls or recorded event-loop errors.
The six successful predecessor groups were not rerun. Controls01 remains a
failed eight-group operation; this separate success does not rewrite it.

| Test | Actual exercised boundary |
|---|---|
| 04 budget/contact/commit expiry | Exhausted request allowance refuses before another server request; an expired canonical contact consumes the failed attempt's reserved request/byte budget without contacting the provider; an unknown endpoint does not charge; injected expiry at real SQLite commit rolls back packet insertion while retaining charges; direct admission and closed/retired acquisition are refused. |
| 05 placement and duplicate accounting | Real HTTP group opening plus exact packet retrieval, with offers explicitly forbidden; real custody/index/placement ledger records the quoted reservation; replaying the same request adds no reservation; a new authorized request reuses local bytes without more HTTP but incurs its new quoted reservation. |

Group04 recorded only `/v5/modules/delta-offer` and `/v5/modules/delta-packet`.
Group05 recorded only `/v5/modules/group` and `/v5/modules/delta-packet`.
The latter therefore reaches the formerly blocked group route and the exact
packet path, rather than treating the old EOF as a success.

The commit-expiry fault is deliberately injected through the real store's
`before_commit` callback. It is not evidence of spontaneous natural expiry.
The provider ceiling is 32 MiB, accommodating the real 16 MiB group-route
reservation; this is an allowance, not measured transferred bytes or memory.
No mathematical admission takes place: all receipt bytes are inert fixtures,
all placement authority flags remain false, and proof/native/Node calls are zero.

## Source and selection identity

I independently hashed all 138 saved source-snapshot files: **1,901,521 bytes**,
each matching its selected hash, with no extra snapshot file. The reviewed
controls02, frozen controls01 and runner are the selected entry/dependencies.

I independently hashed all 129 staged logical SDK files: **1,694,560 bytes**.
Every length/hash matches the result manifest and selected physical source.
Comparison with the authoritative storage map `a629df82...` finds exactly the
six reviewed exact-packet replacements and 123 unchanged logical modules:
`managed_owner`, `semantic_reader`, `workspace_evidence`, `workspace_staged`,
`evidence_network/transport`, and `placement/controller`. No extra staged file.

Selection contains 29 runtime/map pins and the original finite envelope
(30 CPU seconds, 90 wall seconds, 256 MiB, one active process, 1 MiB per log).
The saved command uses the pinned interpreter, `-I -S -B`, canonical cwd and this
operation's snapshot entry/output. Runtime payload trees were not redundantly
rehash-swept by this audit; the executed supervisor enforces the selected pins.

## Termination and resources

The actual supervisor reports `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit 0,
direct child reaped, Job closed, final active processes 0, no cleanup error and
no requested termination. Test teardown stops providers and closes acquisition,
controller, packet/module store and workspace resources; both tests completed
without teardown errors. The Job reports two total processes with a maximum of
one active process allowed; this is cumulative accounting, not two simultaneously
active processes. No process/runtime session remains in the returned operation.

| Measurement | Saved value |
|---|---:|
| Aggregate Job CPU (user + kernel) | 1.265625 s |
| Outer wrapper CPU | 0.484375 s |
| Known combined measured CPU | **1.75 s** |
| Outer wall time | 6.026886899955571 s |
| Command wall through cleanup | 5.872561300173402 s |
| Peak Job private commit | 30,478,336 B |
| stdout / stderr | 0 / 385 B |

The complete stderr contains only the two unittest pass lines and `Ran 2 tests`
/ `OK`. These CPU and memory values describe this narrow synthetic-receipt test,
not proof verification, a throughput benchmark or full workflow cost.

## Evidence pins

| Saved file | Bytes | SHA-256 |
|---|---:|---|
| `selection.json` | 27158 | `95b18eecf8ff046e355b1aeb1ec6963504fd33fb6d863ad6703810e4758d414e` |
| `RESULT.json` | 2013 | `3435feaedfa6cff39f9e923ea0eb91a421d092538e49795d0b80820ea042c114` |
| `exact-packet-controls-result.json` | 24690 | `d55a57a41b25529a756f18deb6d1fd43600d646bc54c35ae8307ab0866624726` |
| `command/stderr.txt` | 385 | `5a465bea61098ee746b530761eb3cf7a721f24aa23e55636dff04480f4cc5eb7` |
| `command/command.json` | 670 | `9002ca9ca0cfab2053b9d91456605e60ff517d363ebfdb25de5804cc0b1c84ff` |

## Adoption boundary

The narrow actual controls pass, complementing the six separately preserved
controls01 passes. No installed-client integration, genuine receipt admission,
independent-host operation, full-v5 readiness or new mathematical growth claim
follows. The next distinct integration gate may proceed under root's separate
reviewed selection; no successful control needs repetition.

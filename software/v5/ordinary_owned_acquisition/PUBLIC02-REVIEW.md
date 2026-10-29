# Narrow second-run source review

2026-10-28, query_scaling. **GO for a fresh root-selected finite operation** of
the exact successor below. This is source/data inspection only; no import,
execution, network, database open, native operation or Git change occurred.
Passing controls, assembly and kit work were not repeated.

| Reviewed file | SHA-256 |
|---|---|
| `public_workflow02.py` (19,366 bytes) | `0d036a7556cc217e99f54c166f2bed2f1c1f92d8369eb122b1c0241fe1ba3336` |
| `PUBLIC02-PLAN.md` (3,373 bytes) | `b5ba46ba63c435faaad3149a45b6081723dd985c2837dd16eecc0098366b5f75` |
| Preserved `public_workflow.py` | `b1df3ea586f1a7d0a030ca08a326a433cf7ab3895fce5853ed29a69594b7fb46` |
| Preserved `PUBLIC-PLAN.md` | `efe91173f6bbc832730a013d7e3ffab779dee9c4074e0904f5426af778c5fa96` |

Read the saved public01 inner result, hash
`78836c2158528216d7260f0c6d04127202fcaf5ca9e5e0b0fa1d60366012f754`.
It remains FAIL at `OWNED_PUBLIC_EXPECTED_SETTLED_REFUSAL`, caused by the genuine
typed `ATTEMPT_TIMEOUT`. The one request charged the full 1,351-byte cap, left
zero pending ticket and 6,485 ms in the original ledger. There was no live-provider
request. The natural ten-second lease, quiescence, custody/reserved-socket closure
and empty cleanup-errors list were saved. The outer result records nonzero child
exit with the child reaped, Job closed, zero active processes and no cleanup error.
This evidence supports correcting the OS-specific test expectation; it does not
turn public01 into a pass or establish a product failure.

Compared the complete old/new source texts. The only substantive changes are:

- The first call's expected reason is the closed tuple
  `("CONNECTION_REFUSED", "ATTEMPT_TIMEOUT")`.
- The handler requires a non-None expectation and membership in that tuple,
  while still requiring provider `unavailable` and the exact preview route.

The remaining changes are the opening description and two explanatory comments.
No product source, package pin, loader closure, fixture, address, timer, quota,
success comparison or cleanup branch changes. Unexpected success still raises
`UNAVAILABLE_SUCCEEDED`; other reasons fail membership; live calls still pass no
expected unavailable reason. Unknown exceptions, malformed responses, TLS errors
and uncertain cleanup still terminate without fallback. Both newly allowed first
outcomes already require the unchanged owned transport's settled-close path.

All original assertions remain: four requests under one exact budget object and
deadline, 8,076 reply bytes including the failed preview, 1,500 ms attempt cap,
full failure charge/no pending ticket before fallback, three exact raw responses,
three completed responses/one failed attempt, natural ten-second service and
complete successful cleanup. The internal 35-wall/20-CPU envelope and original
reader deadline at most eight seconds after readiness are unchanged. The fresh
operation does not resume or replenish public01's consumed ledger.

`PUBLIC02-PLAN` is a narrow addendum to the preserved plan and uses fresh
`owned-acquisition-public02/workflow` output. Its stdout proposal repeats the
original prospective 2 MiB figure; actual public01's controlling EXECUTION entry
selected 1 MiB per stream. This review retains that smaller **1 MiB per stream**
outer bound, alongside 45 wall seconds, 30 Job CPU seconds, 512 MiB and one active
process. The code needs no larger logs; root's fresh supervisor selection is
authoritative. No other grant discrepancy was found.

No blocking source finding. Root still selects and audits the new operation.
The earlier review's scope remains: packaged typed API plus explicit harness
fallback, not full public receive, learned-location coverage or mathematical
admission. The first failure and all used bytes remain preserved.

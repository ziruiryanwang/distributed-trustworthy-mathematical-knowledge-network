# Placement-network controls01: retained-outcome audit

2026-10-21, core_release. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

Disposition: **PASS_EXACT_TEN_FOCUSED_PLACEMENT_NETWORK_CONTROLS**.
The selected run completed once with ten passes, zero failures/errors/skips,
exact retained sources and clean process closure. This audit read existing
outputs and hashed retained/live input bytes; it did not rerun controls,
import product code, create a new workload or edit used bytes. Root owns
adoption and the subsequent actual network integration decision.

Authorship: core_growth authored controls, root selected/executed the run,
and this reviewer authored the wire and reviewed the control source.
The separate independent product-source review is
`PLACEMENT-NETWORK-SOURCE-REVIEW.md` (`37d24d4e`). This is an independent audit
of root's saved execution evidence, not an independent reimplementation or a
replacement for that product review.

## Exact retained evidence

Run directory: `experiments/v5-local-checks/placement-network-controls-01`.
Both original and saved `selection.json` hash to
`0cf577d19f36257e7aa0b0b77c8f3f08e12baa652e3e4cb7221107def16ebbb7`.

| Evidence within run | Bytes | SHA-256 |
|---|---:|---|
| `RESULT.json` | 2033 | `fce2d9198ebaf460155867ddfb5127102487e6f2d20b4416fdd45a5a6e5a2f5a` |
| `placement-network-controls-result.json` | 40655 | `1a40b840dbfe24fddac20704fcc2ad38a2874c6e8d36804f635d3a150f0f1c2f` |
| `command/command.json` | 684 | `af1688dc133210d077ebd48de7d1bfef0506ed124bb85bc7c3cc1e0c7bf67ca8` |
| `command/stderr.txt` | 6872 | `d9658013e73dea48c4d713753ad4a86840bbf14125580b31769927cf68a148fe` |
| `command/stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The outer record reports `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit 0,
direct child reaped, Job closed, no cleanup errors, no requested termination,
zero final active processes and zero terminated processes. The two recorded
Job processes fit the selected two-process allowance. The report is not a
security-sandbox or hermetic-runtime claim.

The final allocation remains exactly **60 CPU seconds, 120 wall seconds,
384 MiB, two processes**, and one MiB per log. Job CPU was 2.46875 seconds;
outer wrapper CPU was 0.484375 seconds: **2.953125 known measured CPU seconds**.
The nested 0.015625 supervision CPU is already within wrapper CPU and is not
added again. Total reported wall time was **8.235715900082141 seconds**, including
the outer wrapper. Command wall through cleanup was 8.069969399832189 seconds.
Peak reported Job private commit was 32,534,528 bytes (31.02734375 MiB), which
is neither whole-PC memory nor a product deployment-sizing measurement.

## Exact source and runtime identity

Read-only rehashing found **zero mismatches** across:

- All **127 physical source bindings**, checked against both original current
  files and the retained `sources` snapshot. Snapshot file census is exactly127.
- All **121 logical source rows**, checked against both the reported physical
  snapshot path and retained `selected-code` bytes/sizes. Staged file census
  is exactly121, with no additional file counted as product source.
- All **19 runtime pins**, including the exact installed114 SDK map `d3519be1`
  and the retained eighteen-file Python closure.

The actual harness is `29a34996d384ccfb49861f51bf11421b6b509d9cd80e39bb01d4604d18a06bd7`;
wire is `1ec5c452ec129ae033f0577ebac6223e2cf3192d4724a3d31fe2e5c27a06cd4b`;
advertisement is `b5523f82f6d5eba4ba9e72639888f1c9da014f298aa9c1081c76aa3f920f35a6`;
service is `07c60c4f33401d41694228d0f6bde35d9148e769947b75211e9ed4098ec68674`.
These match the final reviewed cancellation-corrected source, not the earlier
client source. The unchanged runner also verifies runtime pins before and
after execution, unchanged selection and unchanged snapshot bytes before
writing its successful outer result.

## Actual ten-method outcome

Read the complete inner JSON, command record and stderr. The ten selected
method names match the source review exactly; stderr reports all ten `ok`
and `Ran 10 tests in 2.727s`, followed by `OK`. Several asyncio debug slow-task
notices report approximately0.10-0.13 seconds of synchronous fixture work.
They are not failed assertions or unhandled task errors. Inner forbidden-call
and loop-error lists are empty. No skip or error is hidden by an aggregate pass.

| Method boundary | Retained outcome |
|---|---|
| Closed envelope bounds | Exact16384-byte inner object produced a16508-byte envelope; overflows/extra-field refusals passed. |
| Projection and saved incomplete diagnostics | Two wire observations of an actually saved incomplete request were sanitized; the successful receipt and both saved rows remained unchanged. |
| Exact duplicate/status | Two later observations caused zero duplicate effects and only one simulated publication. |
| One active intake | Concurrent second intake was charged BUSY, without a queued second placement. |
| Dispatch failure | Attempt stayed charged, core receipt stayed committed, status/replay did not retry. |
| Post-dispatch journal failure | Prior durable attempt remained uncertain rather than unattempted. |
| Intake cancellation | Original receipt persisted, route remained uncertain, and busy/writer cleanup assertions passed. |
| Automatic lifetime | Original monitor closed intake/location/read/stores; the reserved command formula and original finite authority held. |
| Client binding/cleanup/cancellation | Two preallocation refusals and four postallocation memory-transport failure cases passed; all four counted uncertainty, both cancellation cases counted exactly once, and no actual client dial occurred. |
| Unauthorized/unknown/exhausted intake | Two refusals were charged without core/route mutations; the third connection closed without dispatch or further allowance. |

The ninth method's four cases specifically exercised final-read binding change,
token-bearing immediate-close exception, cleanup-only cancellation, and
send-plus-cleanup cancellation. The selected source asserts closed ordinary
error codes, propagated cancellation, original reservations, cleared busy,
closed client on cleanup failure and exact once-only uncertainty accounting.
The retained observation records four uncertain outcomes, two cleanup
cancellations and zero double counting, consistent with all those assertions
having passed; it is not merely the earlier preallocation-only control.

For the privacy boundary, an additional read-only inspection of retained c02's
SQLite bytes found exactly one `LOCAL_ONLY:` token-bearing injected diagnostic.
The extracted token was compared only in memory and was never printed. Neither
that token, its diagnostic prefix, nor `PRIVATE_CLOSE_DIAGNOSTIC:` occurs in
stdout, stderr or the inner public result JSON. This supplements the executed
wire assertions; it does not claim the local diagnostic ledger is secret-free.
The fixture deliberately tests that a raw local error must not be returned.

## Interpretation and next decision

Actual SQLite stores, controller, route journal, service lifetime and Python
wire/client logic ran. HTTP framing used memory streams and Node commands were
simulated. Receipt bytes were inert and never admitted. No actual network call,
Node child, native check, proof production or old-suite import is reported; the
selected guards and exact reviewed source support those scope statements.
All service teardown assertions passed and the outer Job has no remaining actor.

This closes the focused changed-boundary controls for the exact selected bytes.
It does **not** qualify real DHT routing, public TLS, independently hosted
operation, mathematical reception, global availability, full-cost useful growth
or final v5. Do not rerun this passing campaign. The appropriate next new
boundary remains root's separately reviewed real placement, exact replay,
source withdrawal and goal-only discovery/acquisition/admission composition.
All used source, selection, logs, fixture state and results remain frozen.

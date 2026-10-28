# Discovery service 01: closed without requests

2026-10-28. Read-only saved-output audit of
`experiments/v5-local-checks/finite-map-discovery-serve01`.

**Outcome:** the finite service hosted its selected index and ended cleanly after
its 300-second lease. It received zero requests. This is clean idle-hosting
evidence; there is no discovery, preview, mathematical acceptance or growth
result. Root records that prepared find01 never executed. The expired endpoint
`127.0.0.1:65091` must not be reused as a fresh service endpoint.

## Actual operation and closure

- Public `serve` result: `ok=true`, `LEASE_FINISHED`, `quiescent=true`, empty
  cleanup errors; provider `accepting=false`, active/cleanup-pending/reserved
  reply bytes all zero.
- Provider requests, accepted attempts, request/header/reply bytes, refusals and
  failures are all zero. No searched corpus or returned interface is established.
- READY selected `finite-map-index01`, shared `std-kernel-custody01`, loopback,
  TLS disabled and a 300-second lease. READY equals the public result's saved
  READY object.
- Outer result: `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit zero, direct child
  reaped, Job closed, final active and terminated processes zero, no termination
  requested, empty cleanup errors and empty stderr.
- Public limits were 330 wall seconds / 30 CPU seconds / 768 MiB. Outer limits
  were 360 wall seconds / 45 CPU seconds / 1024 MiB / four processes / 1 MiB per
  output stream. These are the recorded scopes, not a new security claim.

## Retained cost and evidence bindings

Outer elapsed time was 301.609174000012 seconds. Job CPU was 6.703125 seconds and
outer-wrapper CPU was 2.5 seconds: **9.203125 known measured CPU seconds**.
Nested public-controller CPU (6.625 seconds) and inner-supervision CPU overlap
these scopes and must not be added again. Public wall time was 300.9779161
seconds; worker CPU was zero. Peak Job private commitment was 31,240,192 bytes.
The spent idle-service time and cost remain part of the record.

All four selected source snapshot hashes match. Selection SHA matches the outer
result; saved stdout parses identically to public `peer/RESULT.json`; READY is
identical to its result field. The selection lists 164 runtime pins; this audit
did not independently rehash those runtime files.

| File within run directory | SHA-256 |
|---|---|
| `selection.json` | `1f4da7c0027636e393be4c721033f32ea84bca85b35359e8da6b7781fed86e29` |
| `RESULT.json` | `ebc8ab11d40f66d76479a9c4ee31627e677c1728654c294e7ae5a39f9855a628` |
| `peer/READY.json` | `fcb0f5387509d540acd2552718383d3aa03ee4dc8202548ebc1cc38ad7538d4f` |
| `peer/RESULT.json` | `a762863c48d7385474fd1252217887927163ad363feeac4fbd55f9bebf63ea54` |

## Consequential next step

The shortest bridge is the separately root-selected fresh serve02, immediately
followed by find02 and previews derived from actual returned records. Prepare
exact dynamic selection machinery before the live lease. Select the needed
nonemptiness equivalence and zero-summary execution witness by their returned
formal types, derive acquired triples from those records/previews, and only then
compare with prospective targets. No new harness, index or compatibility
mechanism is needed. Same-owner contribution must await terminal clean closure.

This note does not authorize a rerun or qualify independent-recipient use,
novelty, complete search, scalable discovery or useful-growth acceleration.

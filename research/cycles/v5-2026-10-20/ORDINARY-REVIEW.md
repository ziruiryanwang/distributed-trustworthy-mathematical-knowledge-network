# Ordinary real-owner integration review

2026-10-20; independent source/selection review by `core_release`.

Disposition: no blocking issue found; clear the single exact plan below for
root's bounded execution decision. No execution or mathematical acceptance
occurred in this review.

## Exact selection

| File | SHA-256 |
|---|---|
| `software/v5/client/runtime_check.py` (8,777 bytes) | `1cda7434722090566c3392bde89042fb49f63364f50dc3b1e98ba6cb1c185eb6` |
| `software/v5/client/runtime.py` | `7759b74f87b6eee8c4ea57a3c8791d22d4879b8acc0458474b64c38836dd5b11` |
| `research/cycles/v5-2026-10-20/select_runtime_check.py` | `6934b9ae0533355e23ee9e84616afcfada5da841cceb2d6a2d1296e75b94f156` |
| `experiments/v5-local-checks/client-runtime-check-01-plan.json` (19,420 bytes) | `8eea1d8ff69ee381517643db3fdbcec41149ffceaaf66326d88fd11bd25dc8b6` |

The plan contains 88 sources: the previously exercised genuine 90-source
closure minus four fixture-owner/helper entries plus the ordinary factory
and this owner. The two added entries match the exact source hashes above;
no `actual_*` source remains selected. The fresh run directory was absent
at review. The selector checks all retained source and asset pins before
writing, and neither builds nor invokes a verifier.

## Decision-changing checks

- The owner derives the expected module and summary from the exact pinned
  bundle, disregards historical acceptance fields, and obtains current
  authority through one real `admit_receipt`. It checks the returned I warrant's
  exact module, summary and receipt identity before semantic import.
- The import consumes the current warrant journal plus the retained openings
  and bodies. READY is an authoring-context result, explicitly not a new
  mathematical acceptance. No proof is generated; native delta, authoring,
  discovery and network paths are not invoked.
- The corrected envelope retains `claims=1, frontiers=1, deltas=2, edges=3`,
  avoiding accidental default owner-allowance multiplication. The aggregate
  issuer is absent, not silently substituted.
- Budgets are nested and finite: outer 60 CPU/180 wall seconds/256 MiB;
  original grant 45 controller CPU/5 worker CPU/120 wall; one receipt
  attempt bounded by 5 CPU/30 wall/128 MiB. These comfortably exceed the
  retained tiny receipt verification observation without authorizing a
  proof campaign. No RAM polling or capacity experiment is warranted.
- Client and workspace cleanup are attempted in `finally`. The final source
  distinguishes failed-but-physically-clean closure from cleanup failure:
  success requires CLOSED; after an action failure, CLOSED or FAILED is
  accepted only with client and both actual owners closed. Original failure
  remains failure. Cleanup errors force failure and cannot produce PASS.
- Same-call request, binding, process and verifier-stdout identities are saved
  for actual-result review. This review does not predict their contents.

## Scope

A passing run would establish the new ordinary factory → real I verifier →
retained receipt → semantic-import path under this exact selection. It would
not establish genuine A production, new theorem proving, global networking,
deployment readiness, or completion of v5. Preserve any failure; no automatic
retry or expanded budget is cleared by this review.

## Actual saved-outcome audit

Disposition: **PASS within the stated ordinary I admission/import scope**.
Reviewed the single completed run
`product-local/v5-client-owner-runs/client-runtime-check-01`; no rerun.

Independently rehashed all 88 original/snapshot source pairs and checked that
all 67 recorded imported origins belong to that exact selected map. The copied
plan retains hash `8eea1d8ff69ee381517643db3fdbcec41149ffceaaf66326d88fd11bd25dc8b6`.
The ten direct evidence/asset pins (request, binding, process, stdout; three
input pins; three runtime-adoption pins) and the actual receipt copy match
their saved identities.

The real pinned host executed `receive` with the expected image, receipt and
module. Its same-call stdout reports `REAL_MODULE_RECEIPT_VERIFIED`,
`fully_resolved=true`, `mathematical_admission=true`, and exact expected
module/summary/receipt identity. The current binding reports
`SAME_CALL_BINDINGS_VALIDATED_BEFORE_HANDLE`. This is genuine receipt
verification, not the earlier inert-owner test.

The owner subsequently imported 11 groups / 14 declarations into a fresh
authoring context with 60,281 frontend packet bytes and zero frontend
theorem-ancestor proof bytes. Fixed foundation proof bodies remain included.
One receipt admission and one import occurred; native-delta, authoring,
publication and network counters remain zero. The READY authoring context is
not itself a new accepted theorem, and zero frontend ancestor bytes is not a
claim of zero semantic work.

Client status is CLOSED, workspace is closed, cleanup errors are empty. The
pre-close receipt/mixed counters intentionally retain `closed=false`; final
closure assertions separately established both owners closed. Both actual
Jobs reaped their children and closed with zero active/terminated processes.

Known CPU is **5.140625 seconds** (4.75 outer Job + 0.390625 wrapper); outer
wall is **15.64936 seconds**, peak Job private commit **106,299,392 bytes**.
The nested verifier's 0.03125 Job CPU seconds are already included, not added
again. Pre-clock interpreter startup remains unmeasured.

| Saved evidence | SHA-256 |
|---|---|
| Outer `RESULT.json` | `05a6f7941717b5ed6decdc00b24f9a9a54c9d225846a1f5f4999c4b1c4f5a9bc` |
| `BOOT-RESULT.json` | `9cd8c3131b9c68cc3ea6591a522dfb0a7ff4a4a0470889a46b352e8bd1d08378` |
| `work/runtime-result.json` | `5b30b2d5be77037dd7b75af6b62fd1fa4e33f25c008d0a7732fc15dce29126c8` |

Used source and outcome bytes remain frozen. This closes the new factory's
retained real-I integration gap, not A production, broad growth evidence,
public deployment readiness or the full v5 goal.

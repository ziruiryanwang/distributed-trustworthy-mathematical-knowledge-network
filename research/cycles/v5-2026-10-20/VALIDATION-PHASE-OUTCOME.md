# Validation-phase controls: independent actual-outcome audit

2026-10-20, `core_release`. **PASS for the selected native-free changed boundary.**
No rerun, product import, build, proof/native execution or Git operation was
performed by this audit. Root selects any later integration separately. This
does not establish mirror completion, end-to-end speedup or final-v5 readiness.

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Evidence: `experiments/v5-local-checks/validation-phase-controls-01/`.
The governing source review is `VALIDATION-PHASE-REVIEW.md`,
`b24084dc0e1ec1fe08098b33a95d5b090ca0cd257b40ec326c8e9006b104145d`;
the exact launch is recorded in `VALIDATION-PHASE-LAUNCH.md`.

## Exact evidence and source closure

| Evidence | SHA-256 |
|---|---|
| Selected and saved `selection.json` | `54b80af9e6a201197414ab152c4ba63b0922df79149ff5b922e966bcacd4d82c` |
| `controls-result.json` | `efaecef34a836ad5b8b790d55226b28dd04beb53ed5e996db06b48b2de1100ce` |
| Outer `RESULT.json` | `e891f144566d3eea1cd898d53409cadeff82c1966f8b5c89260a4791ae02d0fe` |
| Full `command/stderr.txt` | `89e6c4be378a0020f864ca3eb49f8648d3b3e75a0cfe8ed7a5bbf1411853a234` |

I rehashed all 195 source selections both at their canonical originals and in
the actual saved snapshot, all 22 runtime pins, and all 114 staged logical source
copies plus the report's source paths. All hashes/sizes agree; actual file counts
are 195 and 114, with no extra copied payloads. The original selection and saved
selection have the same digest. The executed command uses `-I -S -B`, the exact
saved control source and canonical working directory, with the selected limits.

The staged map differs from current114 exactly at these two logical paths:

- `v5/admission/trust.py`, 13,774 bytes,
  `c997d2a83ae5246dec9ff30eeca72e405ec0f66c0a307e53e0521eef66fae6d0`.
- `v5/admission/pin_phase.py`, 3,719 bytes,
  `76b54eb04fa2a66ec598b8c6d668e675d8bd483809f8fa66448fa7319b82a9ce`.

The executed control source remains
`775a68abca3c5ac3c094a1ee921c1b2bc367a5a55a753e34783b0c3a76da4b0a`.
Historical controls and the pair planner are present only in the outer source
snapshot; no old suite is executed and the planner is not substituted into this
114-entry staged map. The fixed source hashes establish that distinction.

## Actual observations

The full stderr lists all 14 selected methods `ok`, then `Ran 14 tests in 0.804s`
and `OK`. The saved report agrees: 14 tests, zero failures/errors/skips, all 14
observation groups, no forbidden calls, and explicit false mathematical acceptance.
Stdout is empty. No additional warning or traceback appears in the full logs.

- Seventeen ordinary same-domain checks require 17 real persisted reads; the
  same phase needs exactly two, with identical returned identities and isolated
  identity copies. In the composed pin/active case, **40 original active calls
  still execute**, while trust and pin content each require only two real reads.
- Three exact domain objects over two persisted paths produce six reads; equal
  support or persisted path does not alias distinct objects. Four malformed,
  foreign or unregistered binding cases refuse without invalidating an otherwise
  still-valid binding. Two fresh phases plus one ordinary check give five reads.
- Nested success gives four reads; an inner body failure restores the outer
  scope. Outer/body exceptions leave no surviving cache. A captured context
  used after scope exit refuses as closed. Observed inner tampering remains denied
  even after restoring disk bytes.
- Real adoption-byte and record-identity replacement each refuse at the second
  read and remain denied after restoration. Changes to all five in-memory
  generation fields refuse. Actual `withdraw` immediately denies and writes its
  exact adoption identity. Missing first-read data never becomes cached success.
- The saved event trace places the injected persisted marker during final pin
  checking, before the final trust read that refuses it. This directly exercises
  the consequential pin-before-trust finalization order.
- Original synthetic deadline guards refuse on a cached hit, phase exit and a
  clock crossing injected only after the real final trust read. Their deadline
  remains 10; no renewal occurs. Reported read counts include the separate fresh
  outside-scope checks after refusal, not an extra successful-exit read.
- A previously unseen finalization domain is refused before any disk read for
  it. Expected-pin/checker conflicts, changed final pins, failed-pin noncaching
  and the unchanged synchronous caller structure all meet their assertions.

These are genuine filesystem/read/cache tests of inert local-policy records,
not verification of a mathematical receipt. The deadline guard is intentionally
synthetic; source review, not that mock alone, establishes that production owner
guards remain at their existing call sites. No subprocess/network/proof operation
was attempted by the guarded test path.

## Cost and closure

The child exits zero. The outer report is `COMMAND_EXITED_ZERO_AND_CLOSED`, with
direct child reaped, zero active processes, Job closed, no cleanup errors, no
termination request and zero terminated processes. The same closure values occur
in the last observed and final Job records.

- Selected envelope: 45 CPU seconds, 90 wall seconds, 384 MiB, two processes.
- Job CPU: 1.03125 seconds = 0.65625 user + 0.375 kernel seconds.
- Outer wrapper CPU: 0.75 seconds; known disjoint total **1.78125 seconds**.
- Overall measured wall: **7.292886500246823 seconds**; nested cleanup wall is
  5.430273100268096 seconds and is not added to that total.
- Peak Job private commitment: 31,014,912 bytes. Two total Job processes recorded.
- Logs: 1,624 stderr bytes and zero stdout bytes, both within the selected cap.

The inner 0.015625-second wrapper-supervision figure lies inside the outer wrapper
measurement and is not added again. The test runner's 0.804 seconds is likewise
not an additional cost or a measured speedup. Root reported an earlier shell
policy refusal before staging; no test evidence or allocation is attributed to
that nonexecution. This saved selection has one terminal execution.

The deterministic reduction and refusal controls support adopting the two-file
repair for a fresh integrated build. They do not predict that the complete
mirror workload fits its original grant. No installed release is changed by this
audit; all used sources, selection, fixtures and outcomes remain preserved.

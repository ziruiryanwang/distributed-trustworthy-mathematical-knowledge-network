# Independent actual std-kernel-intake01 audit

Disposition: **CLOSED_CPU_REFUSAL_WITH_ONE_CONFIRMED_BATCH; FULL INTAKE FAILED**.

Saved run: `experiments/v5-local-checks/std-kernel-intake01`. The reviewer used
file reads, hashes and standalone standard-library JSON comparison only. No
product imports, owner/status/recovery call, database API, native execution,
artifact import or Git operation was performed. All four current/source-snapshot
pairs and 218 external pins match the reviewed selection
`289e01974d27bf9af17affad9a02e1151a761cc1c486363adb2b6d138c95590b`.

## Confirmed first batch

The owner reports BASELINE_INTAKE_STOPPED with one CHECKED batch: index 0,
1,024 units, last confirmed root
`c3d0f6209f42abdc98a6975a358545b0d61701e849b6ed0a3e69bdc1b7f400f6`.
Its native call is
`std-kernel-catalog01/admission-calls/689b1b1c066dc59068dadc0ca1a9c0c6294da5d40aa1b609b1f2e171631701c2`.
The plan names the actual fresh basis root
`4d7cc70e515293b3037a8fa34f60fa97fe082196e005aa7cd894204464ca5f2b`.

All 1,024 selected first-batch inert files match their manifest bytes/hashes.
Their unit payload multiset equals the native projected units exactly; order is
the controller's dependency order, not manifest order. The actual successful
worker report binds all 1,162 expected names in projected order, 1,024 units,
the correct parent/new module and a 2,150,184-byte artifact. Native stdout and
stderr are empty, and the event exits zero and closes cleanly. Thus the previous
private-name diagnostic obstruction does not recur for this selected first batch.

The artifact under
`operations/f1b41c5c66464e8f181b21061a3c4a2d70638953c43a1069a6471b089053113c/chunk.olean`
has SHA-256
`1959cf9a4dbc022d9dd1d9b93d5e178d507d0d1b592da03a7b87ce03ceef96b1`.
The controller's CHECKED result and BATCH_CONFIRMED observation agree. This
does not independently establish the owner's current recovery eligibility after
the subsequent failure.

## Failed second native event

Call:
`std-kernel-catalog01/admission-calls/22c8515b1ecd70bb3fa48d0aa50ce9b8ade0d4051c29f7a66d894cb5428f721d`.
Its plan contains the basis and confirmed first artifact, with correct sizes/
name counts and the confirmed first root as parent. All 1,024 second-batch inert
files match their manifest hashes/lengths, and their payload multiset equals the
second native projection. Their raw total is 17,147,916 bytes; the first batch
raw total is 9,997,243 bytes. This audit does not recheck the unattempted third batch.

The second native report records **RESOURCE_LIMIT**, error
`RuntimeError: OWNER_COMMAND_RESOURCE_LIMIT`, CPU allowance 24 seconds and
measured CPU **24.015625 seconds**. Its wall allowance was 196 seconds and actual
wall 24.3546537. Termination was requested; the direct child was reaped, Job
closed, cleanup errors empty, and final active/terminated counts were both zero.
The recorded termination request and zero terminated count are retained as
reported; no unobserved leaf-process sequence is inferred.

Both native logs are empty. No worker report or selected second `chunk.olean`
exists. The outer owner reports failed batch 1 / ADMIT /
`ADMISSION_NATIVE_EVENT_NOT_CLEAN`, with `accepted=null`, while retaining the
one-batch prefix in its detail. **possible_unreported_commit remains true**.
These file observations do not authorize clearing that conservative flag or
calling status/recovery. No mathematical rejection or memory-limit event is
established by this run. The observed CPU exhaustion is distinct from the old
frontend diagnostic failure.

## Diagnostics and whole cost

`intake-diagnostics/8f8bbda4ecc02ffccf9b67d7e50ca8b2` contains 20 records,
14,217 bytes: sequence 0 through 19, one BATCH_CONFIRMED, then second ADMIT_INTENT
and FAILED; no COMPLETE. Metadata ended at 36.262121 wall / 35.78125 controller
CPU. First confirmation was 88.686303 wall / 61.5 controller CPU. Second intent
was 102.7325735 wall / 75.375 controller CPU, and failure 156.9336543 wall /
103.40625 controller CPU. The known delayed worker accounting at BATCH_CONFIRMED
is followed by 24.46875 in the next record; no cost disappears.

Reservations total 120 CPU seconds across two attempted batches. Actual first
native allowance was 37 CPU seconds and observed CPU 24.46875; the second's
allowance was 24 and observed CPU 24.015625. Reserved batch budget is therefore
not a promise of 60 native CPU seconds. The source-level allowance cause is a
separate investigation; this audit establishes the recorded operational boundary.

Public and outer layers exit one with COMMAND_FAILED but are cleanly reaped/
closed, no termination request, active processes or cleanup errors. Their stderr
is empty. Outer wall is **159.3159979 seconds**; inclusive Job CPU 153.375 plus
wrapper 1.59375 is **154.96875 known CPU seconds**. Peak aggregate private commit
is 1,019,195,392 bytes. Nested worker 48.484375 and controller 104.234375 must not
be added again. Fresh init plus this intake costs 165.609375 known CPU seconds;
earlier failed-route costs remain separate retained history.

| Evidence | SHA-256 |
|---|---|
| outer RESULT.json | `8800b81ea98ae4a61b79d26dcbfe49972baf4979a61fdcd2f5bc03b914184095` |
| owner stdout | `dbb7d1f1e0f0361b9f263ed1ecbed1a3734b2502ad05889131fbf39ba0e2d07b` |
| first worker report | `6feadef736891be3284cb56dd6bd92a8590b0e8b9863619718566fa0389459de` |
| first supervision | `89f1b1af017f3f73a718f3be300ddf49ac51367aeac042a43aa631e229f4636e` |
| second supervision | `060390bedef5b71ba3267c9c43afa297ac512ccde447158a6db61e9a01b182e2` |
| FAILED diagnostic | `7fae68e4d5af68c164e7912234d7e0a45febbbb7bffc23d6f504166ee27d70c7` |

No third native call occurred in this intake; the third existing call directory
belongs to initialization. No ordinary library registration or full-closure
acceptance is reported. The absence of WITHDRAWN does not establish eligibility.
Preserve state, prefix, used sources and all failed work. No retry, status,
recovery, cap increase or artifact promotion is selected by this audit.

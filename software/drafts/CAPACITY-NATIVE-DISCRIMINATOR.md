# Native capacity-renewal discriminator

Prospective test specification, 2026-09-21. Source review only: no harness,
launch, import, build, database query or execution is authorized or reported.
This refines [OPERATING-ENVELOPE](OPERATING-ENVELOPE.md); the native-free
[capacity suite](CAPACITY-V3-TESTS.md) is a prerequisite, not native evidence.

## One narrow claim

A genuinely initialized node can exhaust its initial request/stage/byte
authorization, preserve an actual refused request, accept an explicit owner
grant, and complete one further genuinely checked source submission. A second
grant enables one ordinary metadata request. Historical responses remain
exactly replayable without charging again or rerunning native work.

This is bounded continuing operation, not indefinite operation, autonomous
research, useful growth, distributed replication or mathematical novelty.
The source result is a private checked artifact; publication, admission and
downstream reuse are deliberately outside this two-stage experiment.

## Fresh installation and fixed source

Use one fresh source-pinned **version-3** installation, one ordinary client
`local`, no peers, the five configured common packages and no initial offers.
Build support locally; do not copy old compiled support or accepted state.
Configure with `--initial-requests 2 --initial-stages 1
--initial-reserved-mib 144 --initial-metadata-mib 32`. Keep other product limits
unchanged, including 128-MiB stages, 8-MiB ordinary request grants and the
default context-package cap. Bind actual resulting configuration and runtime.

Store this exact UTF-8/LF source, with a final LF, once before submissions:

```lean
universe u
noncomputable def RenewalCompose (A B C : Sort u)
    (g : B -> C) (f : A -> B) (a : A) : C :=
  g (f a)
```

The selected root is `RenewalCompose`. Use the same source/root and the actual
bootstrap context C0 for both submissions; only the ordinary request ID changes.
This follows the reviewed [noncomputable source profile](CONTEXT-NONCOMPUTABLE-REVIEW.md):
safe mathematical definition, optional executable code generation disabled,
no added axioms, `sorry`, tactics, imports or kernel-check bypass. It is a
review input, not an already verified result. Do not repair source mid-run.

The exact current public code for the stage-quota refusal is
`SELECTED_CHECK_FAILED:Refusal:STAGE_QUOTA`: the checking boundary wraps the
store's typed `STAGE_QUOTA` refusal. The shorthand below names its cause.
Independent pre-execution review found and corrected the harness's original
bare-code expectation; neither the product nor the required state transition
changed. No native allocation had executed when this correction was made.

## Exact seventeen installed CLI calls

Let U be consumed `(requests, stages, reserved MiB)` and A the authorized
vector. A row's vector is the expected state **after** that call. All new
ordinary IDs are distinct, except explicitly labelled byte-exact replays.
`init` uses owner; every other ordinary request uses `local`. Readonly SQL
snapshots are observations, not extra CLIs or authority to mutate state.

| # | Installed CLI / operation | Required observation | U | A |
| ---: | --- | --- | --- | --- |
| 1 | `build.py` | Fresh support stage, two compilations; not mathematical acceptance | absent | absent |
| 2 | `manage.py configure` | Fresh immutable schema-3 configuration; no control DB yet | absent | configured (2,1,144) |
| 3 | ordinary `init {}` | Real checked C0, P1 snapshot S0/cut zero; receiver stage 0 | (1,1,136) | (2,1,144) |
| 4 | ordinary `submit`, ID `submit-exhausted` | Request reserves; exact `STAGE_QUOTA` refusal; no second stage | (2,1,144) | (2,1,144) |
| 5 | owner `status` | Remaining vector zero, active null, no state-byte mutation | (2,1,144) | (2,1,144) |
| 6 | ordinary `info {}`, ID `info-no-credit` | `REQUEST_QUOTA` before reservation; no request/attempt row | (2,1,144) | (2,1,144) |
| 7 | owner `renew`, G1 | Add (1,1,136), no refund/acceptance or old-table changes | (2,1,144) | (3,2,280) |
| 8 | ordinary `submit`, ID `submit-renewed` | Actual checked artifact R against C0; receiver stage 1 | (3,2,280) | (3,2,280) |
| 9 | owner `status` | Exhausted again, actual two stages, active null; readonly | (3,2,280) | (3,2,280) |
| 10 | exact G1 replay | Original #7 response, historical event, no second increment | (3,2,280) | (3,2,280) |
| 11 | owner `renew`, G2 | Add (1,0,8), no native work | (3,2,280) | (4,2,288) |
| 12 | ordinary `info {}`, ID `info-renewed` | Success, still C0/S0; historical description, no checking | (4,2,288) | (4,2,288) |
| 13 | exact #3 ordinary replay | Original init response, not a new bootstrap | (4,2,288) | (4,2,288) |
| 14 | exact #4 ordinary replay | Original `STAGE_QUOTA`, even after later renewal | (4,2,288) | (4,2,288) |
| 15 | exact #8 ordinary replay | Original R response, not a new source check | (4,2,288) | (4,2,288) |
| 16 | exact G2 replay | Original #11 response, historical event, unchanged tables | (4,2,288) | (4,2,288) |
| 17 | owner `status` | Final U=A, two grants, active null, readonly | (4,2,288) | (4,2,288) |

Every ordinary call uses `manage.py request --config ABS --request ABS`.
Status uses `manage.py status --config ABS`; renewal uses
`manage.py renew --config ABS --request ABS`. The two strict schema-1 renewal
envelopes bind the actual config digest, `op:"renew"`, distinct fixed safe IDs
G1/G2, and respectively `add:{requests:1,stages:1,reserved_bytes:142606336}`
and `add:{requests:1,stages:0,reserved_bytes:8388608}`. Omit metadata expansion.
Retain each original raw envelope and reuse those bytes, not reconstructed JSON.
For every ordinary/admin call, bind actual commands, distinct expected source
pins, request/output digests, worker events and complete supervisor receipts;
do not reuse the ordinary-event schema for administrative calls.

Totals: two preparation CLIs; eight ordinary CLIs (four reserved requests,
one pre-reservation refusal, three exact replays); seven administrative CLIs
(three status, two fresh grants, two exact grant replays). No optional inspect,
publish, final info, recovery or extra status calls are included.

## State, replay and native evidence obligations

After each relevant CLI's complete descendant quiescence, retain bounded
readonly snapshots of all ten tables in fixed indexed order, at most 128 rows
per table and a 32-MiB database. Bind BLOB bytes exactly or by length/digest.
Record page/freelist counts and immutable config identity. No nonempty SQLite
sidecar may be erased or recovered by the observer. Acquire the existing owner
lock for observations; no synthetic row, head, context or acceptance is allowed.

At #4 only ordinary reservation/attempt/terminal bookkeeping is added, with
the 8-MiB request charge retained. Checker preparation may read/copy packages
and retain files; zero stage allocations/pipeline commands, not zero work, is
required. At #6 compare full table snapshots and retained state-file bytes:
no ordinary reservation or charge was committed. Keep its failed-call costs.

For G1/G2, compare the complete ten-table projection: only `authorization`
and `owner_grants` may change. Used counters, requests, stages, records, heads,
providers, entries and snapshots remain logically identical. Each grant stores
one exact success response with `mathematicalAcceptance:false`, `refund:false`
and historical before/after values. G1 replay after #8 must still return #7's
old `used_at_commit`, not a newly generated current-capacity response.

All five exact replays require identical original response bytes, identical
before/after ten-table projections, zero new stage allocation and no native
pipeline commands. Ordinary events must mark `historical:true`; grant events
must mark `renewal_historical:true`. Status is not historical replay: bind each
fresh status observation to its corresponding snapshot. Compare state-file
hashes/lengths before/after all three status calls; administrative scratch
diagnostics are separate retained costs and are not claimed read-only.

Bind C0 to the actual bootstrap replay, stage-0 receipt, package closure and
native output. Bind R to the exact submitted bytes/root, actual C0 context,
candidate capture/replay and inverse capture/replay, canonical type/body,
allowed dependencies and stage-1 receipts. Require one safe ordinary-definition
root with the stated polymorphic composition body; no assumption that the
readable template alone proves this. Keep source/refusal evidence from #4.
Checking R does not move the head or publish it: C0 and P1 cut zero remain.

Exactly two receiver stages are expected: bootstrap one pipeline command and
successful submit five commands, six total. Their IDs are 0 and 1. Support
build is separate: one stage, two compilation commands. These counts are not
OS-process counts (auxiliary processes may exist). Final committed charges
are `4*8 MiB + 2*128 MiB = 288 MiB = 301989888 bytes`; no refund occurs.

## Containment, retention and reuse of existing machinery

Use the reviewed native-context coordinator/worker shape as a reuse candidate,
with unchanged `supervise.Transport` containment. Do not import/run a previous
driver or proliferate independent generic harnesses. Root must first select a
minimal adaptation and review its source/launch; frozen context allocations
and drivers stay unchanged. In particular, native03's preserved **version-2**
product root, eight-table snapshots, fourteen-call count and 98-file inventory
are not valid renewal inputs. Pin the actual selected version-3 manifest,
including capacity/admin modules and their distinct administrative receipts.

Proposed outer envelope: 450 seconds wall, 450 Job CPU seconds, 6144 MiB
private commit, sixteen requested active processes, 64 KiB each worker
stdout/stderr/event. Preserve existing product ordinary/native limits and
administrative 10-second wall/5-second CPU/128-MiB limits. Exact launch review
must confirm feasible nested containment; this note is not an allowance grant.
Use two new named roots for installation/state/driver data and qualification
evidence, selected and pinned by root; both absent initially, no sockets.

Proposed combined retained endpoint ceiling: 1 GiB, 16384 files, 32768 entries,
including copied sources, fresh support outputs, work, all call evidence and
final reports. The externally pinned Lean runtime is excluded and identified.
The 288-MiB node charge is neither this endpoint total nor a disk reservation.
Real supply checks remain enabled for configure, store creation, new ordinary
admission and fresh grants;
do not mock them or claim uninterrupted physical availability.

Count outer Job CPU once; it includes worker, CLI wrappers and nested Jobs.
Record coordinator/launcher CPU outside it separately and mark unmeasured
endpoints. Retain actual CPU/cleanup facts before interpreting outcome. Census
only after genuine worker-tree quiescence, including failed prefixes; uncertain
cleanup forbids live-tree census. Bounds are not hard transient disk quotas.

## Stop and review conditions

Expected #4/#6 refusals are assertions in this allocation, not reasons to repair
anything. Any unexpected refusal, quota delta, output/persistence ambiguity,
source rejection, missing evidence or containment failure stops the sequence.
Preserve original requests, replies, files, counters and unknown outcomes;
never alter configuration, reset usage, add an extra grant/stage, or retry a
failed call to force the intended path. Planned exact-response replays
are the five calls already listed, not general recovery authority.

Strongest immediate label: `PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT`. Independently
audit actual native binding, seventeen call identities, all counter/table
deltas, replay bytes, physical-supply samples, retained costs and cleanup.
A pass establishes this finite continuation only, not the usable-v1 goal.

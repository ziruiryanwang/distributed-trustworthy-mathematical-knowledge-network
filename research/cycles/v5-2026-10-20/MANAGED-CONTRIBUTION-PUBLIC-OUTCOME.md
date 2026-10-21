# Actual managed public contribution: failure audit

2026-10-21, support_screen. **FAIL: no committed contribution, host custody or
orderly managed close was achieved.** The exact attempted run remains failed.
Independent saved-evidence audit confirms a genuine private-handoff grant,
separate contributor/client attempt, retained full reservation and clean process
containment. It does not promote these subevents into a passing integration.

The first failure has a concrete actor-budget defect. The host's separate
`GENERATIONS_CLOSE_UNPROVEN` cause is not recoverable from the retained reports;
its actual state is `QUIESCED_UNCLEAN`, not `CLOSED`. No retry or product repair
is selected by this audit.

## Exact used inputs and evidence

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Run-local paths below are under
`experiments/v5-local-checks/managed-contribution-01`.

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| Outer `managed-contribution-01-eight-processes-selection.json` and retained `selection.json` | 45744 each | `2b74035786a198d430a9c9a0646e68b13827ced9e7841e1c077c37f1137ff3fb` |
| Outer `managed-contribution-01-input.json` | 3470 | `d8f40d9c05b4edf5242b319f4dcba204ab5da09e11b8467091f5d5e7be7b1c6f` |
| `RESULT.json` | 2286 | `81b74b7a281d0b13e14c7adec41e2c5d632d6841e00a6acf0a306ffda4995006` |
| `managed-contribution-result.json` | 16320 | `c9fdf33a5599d44dcb4fd0612861a484fc5be562fb38db722e9fbeaa66cdb7ba` |
| `operations/serve/work/managed-result.json` | 24482 | `6bbdc213fb518c3ff799f38f05e9f436bdc8498dacdf3b75c1169be2971d063a` |
| `operations/serve/work/managed-worker/work/managed-ready.json` | 3362 | `c0adccc655e61dfbdd1ce2108632f85315a00709cb7304f5bb93ad297e0dbd47` |
| `operations/serve/work/managed-worker/work/managed-result.json` | 21836 | `29499a4043226866b207ef08f8395deab53b724ec8d90bd02d852cf5287c51dc` |
| `operations/contribute/work/contributor-result.json` | 2708 | `ebd6b7165ebc63f721c568e880eaac9d99f8da4da23768b6cab761fa8d277a34` |

The used release is
`2cb30fae38d4054a2662f7652ac7ad4d5eef5b1e5f7ba8549b8fd288a90792f1`.
Driver `f2aa0cac44cd578bbf8e7fa9bc6fbbae6d5aef9c5e76d9d208e4a5e8c76f471f`
and contributor
`367e875a28e9ec21f9a4a9b9afbcf81e33bf87d02416bc913397c8d891e90e15`
remain unchanged. The preparation failures and narrowly changed outer cap are
preserved in `MANAGED-CONTRIBUTION-PUBLIC-LAUNCH.md` and its two repair records:
DirectoryInfo preparation refusal, then unsupported12-process runner refusal
before product output/child. The actual single service allocation uses8 active
processes, the same input and original horizons; those preliminary refusals are
not prior completed contribution tests or renewed service attempts.

## Identity and authority bindings

Read-only checks independently verified all four outer source snapshots and
all127 installed SDK byte/hash rows. Each of the public host, nested worker and
contributor plans contains128 entries; all384 plan-source rows were checked
against their actual source roots and all nonowner rows against the release map.
The two public run snapshots'256 byte/hash rows also match. No mismatch was found.
The selected runtime map contains160 pins; no new full installation payload
sweep or duplicate source review was performed.

Public host plan
`372bb04be8c65bc425fc5ef4af0907fc5d0412f6f0d34f59e18711c9e24470a6`,
nested plan
`4bc865ceb8183161111cd8e71ab8093fd30182b7a09f24adb7cafd68e7fa47d6`
and contributor plan
`ecc6e1604b4a90f298b3bcc9b26a291102f1ce1c15b2e65f7ebaea5724cfa50c`
remain the actual selected plans, not reconstructed successor runs. The public
ready metadata's parent-plan digest, profile, original service cutoff and service
bindings agree with the saved host/worker records. Its exact number/nonce/worker
session agrees with the worker join; the extra mathematical-acceptance flag is
false. The original service cutoff is2247016074172500 monotonic nanoseconds.

## Actual sequence and first failure

The managed worker started and published nonsecret `READY` handoff metadata;
the contributor reached `stage:submit`, with an actual closed PlacementClient
report showing one request,1333 attempted outgoing bytes,240 observed incoming
bytes and one uncertain submit. A complete observed response/receipt was never
recorded. Its source provider accepted one request with156 request bytes,
130 header bytes,zero reply bytes and one failure; active/refused/reserved reply
counts are0. Client, source provider and source workspace cleanup completed
without contributor cleanup errors. This is an actual attempted cross-process
source pull, not the required three successful opening/offer/packet pulls.

The source explanation is decisive for this actor configuration:

- `contributor.py` sets the source provider's `max_reply_bytes` to4 MiB.
- The selected `transport/http_provider_receipts.py` sets
  `/v5/modules/group` to `MODULE_MAX = 16 MiB`.
- Inherited `delta/transport.py` initially reserves `ROUTES[route]` and only
  specializes other listed routes. It therefore requires16 MiB of remaining
  source reply authority before dispatching a group request, even for the
  selected1595-byte opening.
- Consequently the actor's valid first group pull cannot satisfy
  `DELTA_PROVIDER_REPLY_QUOTA`. The provider increments its failure counter and
  closes without a reply. The saved one-request/zero-reply result and durable
  `IncompleteReadError` agree with this path. The swallowed provider exception
  itself was not logged, so no nonexistent captured traceback is claimed.

This is an **integration actor budget defect**, not evidence that the new private
handoff parser/publisher failed. A source-only review missed the route-reservation
requirement, including this reviewer's contributor pass699f23dd. Those earlier
immutable reviews stay preserved as historical judgments; they do not override
the actual failure. Any fresh actor would need sufficient existing-route budget,
not weaker product validation or edited used bytes.

## Durable grant, reservation and failed request

The auditor opened only four selected nonsecret SQLite databases, using stdlib
`sqlite3`, `mode=ro&immutable=1`, after checking absence of WAL/journal sidecars.
Integrity checks returned `ok`; bounded queries returned at most four rows.
Before/after hashes were identical. No product APIs or imports were used.

| Database beneath the run root | Bytes | SHA-256 |
|---|---:|---|
| `managed/generations.sqlite` | 20480 | `77d864389b4ef59e0056f062825722fce31a85d8b14f8cdd2501fa5d8f2efaf8` |
| `managed/slot-0/g00000000000000000001/workspace/placement.sqlite` | 28672 | `170cb5ab0fb541c1a59339b051bc6d4361c5179abd2a946fad3aba6f81aae613` |
| same workspace, `modules/modules.sqlite` | 24576 | `ba46360c8daa00fec40afb239052f17f81f5fd5c3e15043964b99803676883ba` |
| same workspace, `packets/evidence-packets.sqlite` | 16384 | `3fa46276c596316bdc136b71df7a7bcfedf1a99453894b8e11e563bbda9c9ef1` |

Exactly one grant exists. Its identifier, issuing runtime, source endpoint,
write/retention horizons and complete limits match public ready metadata.
This supports actual issued authority reaching the receiving service, without
opening the private credential or asserting its raw contents independently.

Exactly one request exists:
`2057ce599ae5e403bb43f0c48e3797f03a6682ba6964228af380a660aaa6254d`.
Its exact canonical manifest equals the contributor report and hashes to
`3e5f15fcbfab51046b11bb2d2a40abd644d6368b42db88c916986368a2a0aa95`.
Phase is **INCOMPLETE**, recovery_used is0, outcome status isINCOMPLETE with
`IncompleteReadError` and reason `0 bytes read on a total of undefined expected
bytes`. It is not `RECEIPT_COMMITTED`. The selected cell remains `RESERVED`.

Meta-used, grant-used and request-reservation all equal the original complete
quote:placements1,requests3,reply_bytes517519,wire_overhead_bytes98304,
structural_bytes17010880,storage_bytes34138740,index_calls2,recovery_passes1,
new_cells1. No refund/reset is observed despite the failure. These are charged
authorization reservations, not measured physical consumption.

Host module/group/declaration/body/logical-byte counters are all0. Host groups,
packets and offers contain zero rows. No host opening or packet custody was
achieved. Both host and contributor workspace `operations` directories are
independently empty. That emptiness does not turn absent custody into a pass.

## Separate close failure and durable quiescence

The host worker reached `SEALED_SERVING` before closing. Its closure list then
contains `GENERATIONS_CLOSE_UNPROVEN`; manager close additionally refuses with
`GENERATIONS_ACTORS_REQUIRE_CLOSE_OR_OUTER_RECOVERY`. Public parent and nested
worker fail, and all three boot-failure files report
`CLIENT_OWNER_NONZERO_OR_INVALID_RESULT` rather than successful boot outcomes.
The driver records `stage:wait-original-host-close` because it waits on the
original host even after the contributor attempt; that final stage is not the
time or cause of the first contribution failure.

Source tracing explains the **diagnostic loss**, not the underlying close cause:
`GenerationServices._close_handle` awaits `service.close()`, then calls
`manager._closed_run`. That method checks the service result'sCLOSED status,
empty cleanup errors and every required flag before returning the result.
Failure throws `GENERATIONS_CLOSE_UNPROVEN`; the owner serializes that exception
from the gather, losing the existing service final report's failure code,
component flags and observed intake/location diagnostics. No such report or
Node command/result transcript is retained in this run's location channel.

The Node state directory has a `metadata.sqlite-journal`. Its metadata database,
journal and identity key were not opened, recovered, modified or deleted. This
sidecar alone does not identify the close cause, Node return code or forced
termination. Neither the contributor refusal, health interval, Node command
allowance nor maintenance interval is established as the cause. No budget
increase or speculative successful-close claim is justified by missing evidence.

The surviving supervisor instead records clean process quiescence. Independent
registry inspection corroborates session `QUIESCED`, slot0 phaseSEALED_SERVING,
run_state **QUIESCED_UNCLEAN**, one run and exact nonce/worker quiescence identity.
There is no closure digest. Slot1 is stillnull; allocated sequence1,retired
floor0 and original horizon1792592590257 persist. No retirement/reclamation,
FREE state or physical-capacity reuse occurred. The worker's earlier in-memory
CLOSING/BOUND snapshot is not mistaken for the final durable registry.

## Containment, costs and uncompleted gates

Outer session84975 exits1 with `COMMAND_FAILED`. Direct child reaped istrue,
final active processes0,Job closedtrue,cleanup errors empty,termination requested
false and terminated processes0. Public host and contributor wrapper records
and the nested supervisor also have reaped/active0/closed/empty-error containment.
These are process-cleanup facts, not proof of orderly application close.

Measured outer Job CPU is30.859375 seconds (17.96875 user+12.890625 kernel),
plus1.03125 outer wrapper CPU: **31.890625 known CPU seconds**. Outer wall is
89.26250510010868 seconds; command-through-cleanup wall88.97542330017313.
Peak Job private commit389488640 bytes (371.4453125 MiB). Outer logs are54
stdout/0 stderr bytes. The nested CPU totals and0.453125 supervisor CPU are
not added again to the inclusive outer Job/wrapper accounting. Total Job
processes13 is cumulative, not13 concurrent processes or an8-process cap failure.

The failure prevented the driver's later full success assertions and bounded
authentic-token leak scan. Neither root nor this auditor opened the authentic
credential for this audit, so no completed raw-token scan is claimed. Private
credential output is preserved; public ready's file pin alone is not an
independent private-file inspection. No actual credential contents were printed,
staged or copied by this reviewer.

The outcome therefore remains **FAIL**, with the precise subevents above:
actual grant/attempt/reservation preservation and exact-job quiescence, but no
committed receipt, host custody, successful source traffic, orderlyCLOSED or
end-to-end contribution qualification. Mathematical acceptance, independent hosts,
public deployment, global availability and full-v5 completion remain unclaimed.
All used code, inputs, logs, failed state, private output and charges stay frozen.
The only write by this audit is this new checkpoint; no rerun, source repair,
Git mutation, deletion, credential access or prior-evidence rewrite occurred.

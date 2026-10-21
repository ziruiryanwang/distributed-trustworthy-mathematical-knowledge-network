# Placement network: independent three-module source review

2026-10-21, adaptive_audit. Complete source read of the three selected new
modules and their author checkpoints. **GO for separately selected focused
controls/integration of the exact corrected source below. The narrow wire
objections are resolved; no remaining concrete source blocker found.** No imports, tests, source edits,
network launch, old-control replay or Git mutation by this reviewer.

## Exact reviewed inputs

Paths below are under `software/v5/placement_network/`.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `placement/network.py` (corrected) | 31301 | `1ec5c452ec129ae033f0577ebac6223e2cf3192d4724a3d31fe2e5c27a06cd4b` |
| `placement/advertisement.py` | 14569 | `b5523f82f6d5eba4ba9e72639888f1c9da014f298aa9c1081c76aa3f920f35a6` |
| `client/serve_placement.py` | 19750 | `07c60c4f33401d41694228d0f6bde35d9148e769947b75211e9ed4098ec68674` |

Used core/Store/read/Node sources remain unchanged. The earlier design review
is `592b6240`; this review concerns the implementation, not another architecture
checklist or a claim that the new composition has executed.

## Concrete wire issues reported and resolved

The initially reviewed `d3d29f50` source preserved an existing PlacementWireError
unchanged. Its final `_active()` can raise a closed expiry/binding error with
`uncertain=False` after a submit was transmitted, for example when synchronous
response parsing crosses the original deadline. The raised exception then
mislabels a potentially committed placement as definite failure, although the
counter already increments uncertain submits. Once an in-flight submit has
reserved its call, conservatively reconstruct any caught closed error with
`uncertain=True`; pre-reservation refusal can remain definite. Do not reuse or
mutate an arbitrary existing exception object.

The client's `writer.close()` was also outside its cleanup exception guard.
A synchronous close exception can bypass closed error conversion. Put close
and wait_closed in the same cleanup handling so no raw transport exception or
pending success escapes. Cancellation must still propagate and clear busy.

Correction `3d773761` implements exactly those two changes. Caught closed errors
are reconstructed using their closed code and
`uncertain=(route == SUBMIT or error.uncertain)`; generic errors retain closed
transport failure handling. Close and wait_closed now share cleanup guards,
which latch closed/cleanup-error state and clear busy even on cancellation.
Read-only reverse-delta reconstruction reproduced the exact prior30981-byte
`d3d29f50` source hash, confirming no other changes.

Root then identified one accounting edge: cancellation first arriving during
cleanup bypassed the outer cancellation handler, leaving uncertain_submits at0.
Final `1ec5c452` adds a per-call at-most-once helper used by outer cancellation,
cleanup cancellation and final failure. It counts an allocated submit once,
never twice when both cancellation sites run, and never counts status as a
submit. Read-only reverse reconstruction reproduced exact31072-byte `3d773761`.
The actual final block and hash were inspected; updated author note is
`507bce659a1ea459bc513fb8160826a12a73900bce01b0f3f7142bb779121ebe`.

## Confirmed source properties

The earlier raw-diagnostic issue is resolved in the reviewed new code. Both
coordinator and wire sanitize incomplete ledger outcomes to the closed generic
code. `_route` admits only nine exact fields and closed error codes; raw Node
error/census strings remain in the local bounded journal, never the wire facet.
Success observation projection keeps only structural input and new logical
storage counts. Exact record/snapshot IDs, export commitments, body sequence,
route feature membership/key derivation and original service bindings are
validated before transmission and again by the client.

Intake uses closed submit/status envelopes and route-specific byte ceilings.
Before task creation its synchronous accept callback nonrefundably charges full
input/output allowances, including busy/malformed cases, and bounds handlers.
One synchronously claimed action slot prevents a queued placement stream.
Capacity exhaustion stops acceptance; retained closing writers remain bounded
by the finite request allowance and tracked for cleanup. The owner-selected
client binds endpoint, token digest and expected four identities; it uses system
CA/hostname validation or explicitly permitted loopback, never a DHT-selected
credential destination. No token enters ledger/report/configuration output.

Advertisement binds exact controller/grant/Workspace/read provider/locator and
immutable journal config. A finite original run allocation precedes startup.
The explicit H+2L+1 command bound, cell cap, run cap and journal page cap are
enforced. Request existence uses a primary-key lookup rather than exception
fallback. Exact duplicates still call the core's observation-only path, but
cannot call publish or mutate the route journal; status likewise only observes.
Ephemeral controller/network call accounting still applies to observations.

For a new committed receipt, the derived route is compared exactly. A durable
DISPATCH_ATTEMPTED row commits before the existing locator command. The original
write/admission/retention/service guards run before dispatch and journal COMMIT.
One opportunity exists per cell/run, including uncertain calls. Missing returned
observations become DISPATCH_UNCERTAIN; saved incomplete observations remain
distinct from positive ADD_PROVIDER-write evidence. No exception or cleanup
failure is promoted into clean placement success or a fabricated remote ACK.
Historical facets retain their original run/request/time identifiers.

The service opens one locked Workspace and owns the single exact fresh locator
plus two bounded listeners. Original active/stop/drain/outer margins are computed
before startup; the controller wall interval rounds down. Its tracked monitor
has finite health calls and starts the same close task on expiry/failure.
Early close cancels/settles startup/monitor, drains intake, invalidates the write
grant, closes locator/read service, and closes SQLite only after actor drain.
Cleanup errors remain latched, with failed final status and outer containment
required when a live actor cannot be drained. No hidden fresh service allowance,
automatic dispatch retry, second Workspace or recursive proof work is introduced.

## Important semantic limits retained

The HTTP per-request cutoff bounds wrapper waits and before/after checks;
unchanged core synchronous pre-COMMIT guards use original service/token windows,
not that shorter HTTP cutoff. Synchronous work can cross HTTP timeout and commit
before the wrapper rejects its response. Such an outcome is uncertain, not
rollback or a strict no-commit-after-request-deadline guarantee. The author has
made this precise in service source note `14a94e39`, without modifying used
core bytes. Hard whole-process containment is separate.

App handler limits do not bound pre-handler TLS handshakes or arbitrary OS
ingress. The implementation reports that distinction, uses finite handshake/
shutdown deadlines and retains external exposure/containment requirements.
Core receipts remain INDEXED_UNADVERTISED; separate dispatch observations are
not remote DHT acknowledgements, availability guarantees or mathematics.
No HTTP-loopback outcome can establish authenticated public TLS or independent
hosting. No full-cost growth or complete-v5 conclusion follows from source GO.

## Disposition

The narrow wire corrections above are source-resolved against the exact final
hash. Root owns adoption and runtime selection. Focused controls and integration
launch/outcome reviews remain separately owned; this checkpoint does not repeat
or execute them. Source GO is not an actual pass, public deployment qualification,
full-cost benefit demonstration or final-v5 acceptance.

# Minimal installed public V request continuation

2026-10-22, storage_integration_adapter. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**Actual hold:** root subsequently reported snapshot01 exit1 before any
OWNER-RESULT or capsule, with clean Job closure and retained pending/failure
evidence. There is no successful snapshot for request construction. The01
paths below preserve the originally proposed contract, not usable evidence;
any successor must use a separately selected fresh snapshot/capsule path and
actual adopted result. No request selector has been authored or run. Root and
the outcome auditor own causal investigation; this lane stops at the contract.

**Source-only, conditional on an independently adopted actual snapshot.** No
snapshot success, segment count, request budget, proof funding or final-v5
completion is assumed. Root owns adoption, exact selection and dispatch. This
continues the installed profile/snapshot path in
`INSTALLED-PRODUCER-V-CONTINUATION-PLAN.md`; it does not replace product code.

## Smallest implementation

Use the already shipped public action=request:

```text
INSTALLED_PYTHON -I -S -B INSTALLED_DISTRIBUTION producer RELEASE_SHA REQUEST_SELECTION SELECTION_SHA
```

One file-only PowerShell selector is sufficient because no existing command
constructs the external action=request input/public launch selection. It will
write those two JSON documents and its PREPARED record, not instantiate a
producer or call Python. It must take actual snapshot result/outer/outcome
digests, a root-selected budget document pin and a fresh root-selected allowance
ID. It must not synthesize a successful snapshot or choose a budget automatically.
The real public entry calls `production_request` exactly once; that method
already invokes the complete preflight. **No additional preflight invocation.**

## Actual evidence, not predicted layout

Let W be `product-local/v5-distribution-installed-producer-01/v-continuation01`.
Read the actual completed public outer at W/snapshot-01/RESULT.json. Its selected
plan must be the actual copied W/snapshot-01/selection.json, not the original
external plan. Follow exact reported pins to the actual worker and snapshot
result, and require their bindings and clean completion. Root independently
adopts the snapshot before the selector is used. Pending/failure sentinels
override otherwise successful reports.

The five snapshot evidence roles are:

| Role | Required actual file |
|---|---|
| result | W/capsule-01/RESULT.json |
| outer | W/snapshot-01/RESULT.json |
| selection | W/snapshot-01/selection.json |
| configuration | Actual copied selection's input, W/inputs/snapshot.json |
| command | Actual result's command, W/capsule-01/COMMAND.json |

Actual session.segment count s and assumption count a come only from the saved
snapshot result. Check supported 1<=s<=256 and 0<=a<=8; bind parent pins to actual
session/staging, not a guessed graph. The selected V route is expected to have
one typed parent, but a shape discrepancy is a root decision, not permission
to silently construct a different route. It is legitimate to stop without a
request if the snapshot fails or actual layout changes the economic decision.

## Request data and explicit budget boundary

The exact10-field input is:

```text
schema = DMKN_RELEASE_LIFECYCLE_REQUEST_ENTRY_V1
snapshot_evidence = the five actual pins
allowance_id = fresh explicit64-hex V ID
budget = exact root-selected budget document contents
checkpoints = []
prior_attempts = []
output_directory = ABSOLUTE_W/attempt-01
stage_limit = finite root-selected prefix, initially1 unless separately selected
carried_external_costs = measured snapshot cost with exact stated scope
request_output = ABSOLUTE_W/request-01/request.json
```

The budget has exactly worker_cpu_seconds, controller_cpu_seconds, wall_seconds,
output_bytes, output_entries, stages. The stage table has exactly segment, lift,
join, resolve, finish, each with CPU, wall, memory, active_processes, stdout,
stderr and artifact-output bounds. Preserve the existing implementation's
validation and ceilings; do not duplicate its entire validator in the selector.
The selector only checks shape, positive integral fields and the supplied pin.
The public producer owns full validation and actual fixed-input/read/output
envelopes. New source fields or raised caps are not needed.

Creating a request is **not** granting funds, dispatching a proof or claiming
the complete graph fits. Existing `_envelope` calculates its full-path bound;
the preflight may report a non-fitting full path while accepting a finite valid
request. Do not translate request success into a funded/completable-path claim.
Root should choose limits after actual s/a and useful marginal payoff are known.
No previous U allowance, checkpoint, failure history or research profile is
migrated. The request selects no prior attempts or prior public launches.

## Reuse the completed finite pin map

Avoid reimplementing profile adoption or scanning the entire installation.
The actual completed snapshot selection already has the reviewed operative60
plus profile, configuration and V packet:63 distinct pins. Rebind those exact
rows and keep them as the base. Add the new request input and the actual five
evidence roles (configuration is already present), then actual staging,
diagnostic, snapshot stdout, saved native invocation, session wire/header/capsule
and parents, snapshot worker report and executed copied entry. Session image
already belongs to operative60. Deduplicate by exact absolute path with
size/digest conflict rejection.

For the expected sole-parent route this is78 distinct pins. More generally
the predicted count is77+a; actual distinct-set derivation is authoritative.
Keep the256-entry/512MiB public runtime bounds and original20MiB fixed-session
bound. The two64KiB copied-entry/worker-report maxima remain within the existing
14MiB reservation. The real constructor and request preflight independently
rebind all inputs; the selector is not a substitute acceptance implementation.

The new exact13-field public plan uses action=request, name=request-01, the same
release/profile/installed entry, fresh W/request-01, the actual derived runtime,
prior_launches=[], input_launch=null. Snapshot outer is evidence, not a prior
proof attempt or a generated-request origin. Proposed request outer bound:
60 CPU seconds,120 wall seconds,512MiB, one process,1MiB logs,8MiB/256 output
entries. Root separately selects that bound. No native host is invoked.

## Cost and final handoff

Carry snapshot public outer.final_job CPU as the worker-inclusive charge and
outer.wrapper_cpu_seconds separately as controller cost; do not add nested
snapshot/native CPU again. Carry outer.wall_seconds for that same snapshot
scope. Constructor/profile creation, ordinary V production, historical U
certification and request-construction/finalization costs remain separately
recorded setup/service costs, not zero and not silently included in that scope.
Unmeasured tails remain unknown. No report is a tamper-proof economic ledger.

On actual success require completed request outer, exact worker request pin,
PASS_REQUEST_CONSTRUCTION_ONLY, one production_request call, zero separately
requested preflight/run/proof calls, closed owner, final bindings and absent
failure/pending sentinels. W/attempt-01 must remain absent. Save actual s/a,
request pin and theoretical complete graph size3s+a without running another
program solely to calculate that arithmetic.

The next proof launch remains a separate root decision. It would require the
generated request and the completed request outer as input_launch. This plan
selects no such launch, automatic continuation, budget renewal or retry.

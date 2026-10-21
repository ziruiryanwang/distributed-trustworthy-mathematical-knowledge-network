# Mirror01 controller refusal: exact cause and minimum correction

2026-10-20. Source/evidence-only diagnosis by `core_growth`; root owns selection,
implementation, execution and adoption. No rerun, changed cap, product import,
build, proof production, RAM investigation or used-file edit was performed.

## Decision

Select a fresh **two-file synchronous validation-phase successor** of
`admission/trust.py` and `admission/pin_phase.py`, with independent focused
controls. Preserve the existing pin phase and every owner liveness/binding check.
Coalesce only its repeated persisted trust-domain reads, with first-touch and
fresh successful-exit validation. Do not raise the CPU limit or cache the entire
author operation. This is a source-supported removal of duplicated work, not a
prediction that the complete mirror workload will now fit its grant.

The refusal was **controller CPU exhaustion before Lean authoring began**.
The selected grant and aggregate owner's cap are both 120 CPU seconds. There is
no source-supported hidden lower subordinate cap to correct.

## Exact basis

The authoritative current114 source map is
`experiments/v5-local-checks/distribution-body-custody-01-input.json`, SHA-256
`995525c5cbf2746718cbf583a3e3e401bc56c2f88d1cef8664ffeb1b644454be`.
Installed release:
`8e93486cadb5806d6470d7a8920803a9a4bad39260dd72f3be3498f699eeeb1e`.
Logical paths below resolve through that map, not through historical names.

| Logical source | Selected source beneath `software/v5/` | SHA-256 |
|---|---|---|
| `admission/trust.py` | `trust_withdrawal/admission/trust.py` | `a60fd123845c7cd732967f995363b3132ebab1522cd90870ab728e6a54dd83ee` |
| `admission/pin_phase.py` | `runtime_efficient/admission/pin_phase.py` | `4b302fc472ced49a7681deb019c20a92674353d9adf109949cba7d3034b0deca` |
| `admission/verifier.py` | `trust_withdrawal/admission/verifier.py` | `01fb93b5d0063110fe82978dcc8a593557b34eaa8b6497f596715ca65064e38c` |
| `aggregate_claims/aggregate_admission.py` | `trust_withdrawal/aggregate_claims/aggregate_admission.py` | `2ef830f849ff214b4e4b3c314332d8d3d23844c1a763828e1be5a5f37732aa` |
| `client/runtime.py` | `trust_withdrawal/client/runtime.py` | `70c52b5148c481ca840c6c55557c9bc5abf71f40d522365f0cb7b0398adbad39` |
| `client/workspace_atomic.py` | `conjunction_index/client/workspace_atomic.py` | `eea95a6bb12349e5fc7b1e80bc610710ccafc7cbbfd2b40d705d80cdc67c8022` |
| `mixed_claims/imports_atomic.py` | `interface_views/imports_atomic.py` | `e38ac52a888f354e8e878984397a5c93c82ac38284b9e6fc89051063537aa459` |
| `mixed_claims/authoring_atomic.py` | `interface_views/authoring_atomic.py` | `081d9d18d16d1cd68b40a5f3cf52493bac7e2e2dbdfb9bd632b72d74de235dbc` |
| `mixed_claims/receiver.py` | `runtime_efficient/mixed_claims/receiver.py` | `aa591a1829deff82576ba30af484ab560ee04900200fd79ac93c19a9c2c7bf7f` |

Evidence directory:
`product-local/v5-distribution-body-custody-01/mirror-method01-operations/installed-mirror-method-01/`.

- `work/first-result.json`: SHA-256
  `e8c7769d27b733fdb945b5396db51fef8a596f6f8bb1aa01c6dcc808cd39369c`.
- Outer `RESULT.json`: SHA-256
  `fe42beffbfd55cd9b23c20df63177024f64913a4658be211f67e0828b68542f8`.
- First operation ID:
  `22546d972c80824b5e9d8a979129dc0d649f001c0b2c985e3175bc741e5bde31`.
- Native/receipt evidence is below
  `product-local/v5-distribution-body-custody-01/mirror-method01-first/operations/<operation-ID>/delta/1/`.

## What actually happened

| Observation | Before contribution | Final first-owner report |
|---|---:|---:|
| Controller CPU since grant | 89.15625 s | 120.765625 s |
| Wall time since grant | 96.5012864000164 s | 130.51080239983276 s |
| Client calls | 34 | 35 |
| Admission submissions | 1 | 1 |
| Author calls | 0 | 0 |
| Publication attempts | 0 | 0 |
| Preparation calls / worker charge | 0 / 0 | 0 / 0 |
| Aggregate receipt attempts / member calls | 0 / 0 | 0 / 0 |
| Preparation lifetime controller CPU | 84.75 s | 116.359375 s |

The recorded stage is `author-admit-publish`; the exception is
`StructureError: AGGREGATE_CONTROLLER_CPU`. No contribution exists. The earlier
M import reached READY with no outstanding semantic demand: five declarations,
two groups, 34,414-byte context, 33,499-byte selected input and zero frontend
proof-ancestor bytes. The retained I receipt and M native delta checks succeeded:
their child reports each record 0.015625 CPU seconds. Preparation contains no
`author-1` worker evidence. Therefore this is not a failed Lean proof or a failed
new proof-production attempt. The second owner never starts.

Outer supervision reports 122.859375 total Job CPU seconds, including 73.234375
kernel CPU seconds, and 120,549,376 peak private-commit bytes. It records no
termination request, no remaining active process, closed Job and empty cleanup
errors. The first client, workspace and service closed; its trust domain was
withdrawn. The CPU measurements are inclusive at different scopes; do not add
the preparation or nested owner lifetime figures to the Job total.

`client/runtime.py:388` passes
`controller_cpu_seconds=caps["controller_cpu_seconds"]` into the aggregate owner.
`aggregate_admission.py:56,62,103-108` starts a `time.process_time()` timer at owner
construction and checks elapsed same-process CPU against that cap on every
`_active()`. It is not an aggregate-receipt-work counter. That owner can therefore
be the first component to report refusal even with zero aggregate attempts. An
inner synchronous validation can cross the cap before the next outer grant
check. No separate lower cap or allocation mismatch is established.

## Why the existing optimization is insufficient

The selected `PP.phase` already caches successful exact immutable file pins per
synchronous phase and checks each afresh at successful exit. Adding that cache
again would duplicate completed work. Its deliberately preserved `active()`
callbacks run before/after pin comparisons, including cache hits and final sweep.

The current call path is:

```text
CommonsClient.author
  -> _live_context -> session.require_view -> _check_view -> _live
  -> MixedSourceOperation constructor
       -> require_view
       -> view_context -> _check_view twice
       -> operation._active -> require_view

each session._live
  -> PP.phase(session._active)
     -> receipt._check_install / aggregate._check_live / mixed._check
     -> source snapshots and existing liveness checks

each applicable active callback
  -> issuer._active -> check_binding -> TrustDomain.check -> _current -> _read
```

The author-call counter increments only after constructing `MixedSourceOperation`.
The zero author/preparation counters localize the failure before that increment;
the saved report has no traceback that distinguishes one exact nested check.

`TrustDomain._read` performs two complete ancestor-directory `lstat` walks,
withdrawal-marker probes before/after, and adoption-file metadata/open/fstat/read/
metadata checks. The actual adoption record is 20,233 bytes. Receipt and aggregate
owners have bindings to the same persisted domain, while mixed-owner checks can
call those issuers again. Pin-hash reuse does not reuse these trust reads.

This proves redundant persisted validation exists and scales with nested guard
count. The large kernel-time fraction is consistent with filesystem work, but
is not profiler attribution: neither an exact fraction of wasted CPU nor a
specific end-to-end speedup has been measured. Other hashing, snapshot encoding,
path resolution and repeated sealed-view phases remain after this correction.

## Minimum safe successor contract

The existing trust model explicitly assumes a trusted owner/controller/filesystem,
owner-serialized operation and checks linearizing at their final read. It does
not protect against arbitrary concurrent hostile mutation or whole-directory
rollback. The existing pin phase likewise permits only trusted synchronous
validation. Within those stated assumptions:

1. **Scope:** integrate an internal trust-validation context into `PP.phase` only.
   Its body, existing final pin sweep and final trust sweep must all complete
   before the phase returns. No await, native subprocess, network call, user
   callback, new public action or externally usable authority may cross this
   scope. Do not cache an entire public author/admit/publish operation.
2. **Exact identity:** key by exact `TrustDomain` object, not path, support hash,
   binding identity or equal adoption bytes. Retain a snapshot of the immutable
   path/raw/directory-key/record-key/identity generation used for the first read.
   Distinct domains, even ones opening the same path, have independent entries.
3. **First touch:** run the unchanged full persisted `_read` and exact adoption/
   directory/record comparison. Record only a successful check. Do not cache a
   failed read or allow a failure to create a usable generation.
4. **Every hit:** still check exact domain class, unchanged generation and sticky
   `_denied`; preserve `check_binding`'s original-domain registration checks.
   Every original `_active` owner/profile/deadline/resource check still executes.
   Cache persisted evidence only, never authority or whole liveness results.
5. **Finalization:** after final pin validation, unconditionally perform the
   complete fresh persisted check for every touched domain. This path must bypass
   its cache. Run the original active callback after each full final read while
   the scoped cache remains installed, catching CPU/deadline expiry caused by
   that work without recursively causing repeated filesystem reads. The fixed
   owner graph must not introduce an unseen domain during finalization: fail
   closed if it does, rather than mutate the iteration or silently omit it.
6. **Denial monotonicity:** an observed withdrawal, changed/missing adoption,
   redirected/replaced path or failed fresh check permanently latches that live
   domain denied, as today. In-process `withdraw()` immediately sets `_denied`;
   the next cached touch must fail even before finalization. Removing/restoring
   files never clears an already observed denial. No reset API is added.
7. **Nested/exception boundaries:** nested phases have independent fresh caches.
   They may not inherit the outer successful read. After a nested phase exits,
   the outer still requires its own final read and sees any sticky denial. Body
   exceptions cannot return a successful phase; discard scoped data and restore
   the previous context in all cases. A final-read exception propagates and
   retains denial. Closed scope state must not be usable as a later cache.
8. **Outside scope:** `_current` retains fresh disk validation on every call.
   The change cannot create a TTL cache, long-lived adoption cache, file-stat-only
   acceptance path or fallback that silently treats missing state as trusted.

### Race argument and its exact limit

For a successful phase, each touched domain has a full successful first and
final read. Every intermediate use checks the same in-memory generation and
observed-denial latch. Under the owner-stable, non-yielding phase assumption,
repeated full reads between those boundaries establish no additional fact.
Any persisted marker or mutation still present at finalization is rejected before
phase success; every already observed denial is sticky across nested phases.

This **changes disk-observation granularity** from every nested micro-guard to
first/final phase reads. It is not observationally identical under arbitrary
concurrent writes. A marker created and removed entirely between those reads
may go unobserved; hostile rollback/transient tampering is outside the existing
trusted-owner model. An owner who needs immediate asynchronous revocation must
use a different synchronization contract, not infer it from this optimization.
Even fresh reads cannot promise recall after return or eliminate the last-read/
return interval. Sequential checks of distinct domains are not one atomic global
policy snapshot. These limits must remain explicit in the successor docstring.

### Work reduction justified without a large experiment

Let `q_j` be the old number of persisted `_current` reads inside successful phase
`j`, and `d_j` its number of distinct touched domain objects. Retaining ordinary
checks outside phases, the change replaces the phase contribution
`sum(q_j)` by `2 * sum(d_j)` full persisted reads, provided finalization's active
callbacks touch only that fixed set. Nested scopes count separately. It does not
reduce the number of original liveness callbacks or waive final file pin checks.
This yields a deterministic operation-count benefit when `q_j > 2*d_j`, without
requiring a timing benchmark or raising the existing controller grant.

## Focused evidence before adoption

The independent control owner should implement deterministic real-domain controls
rather than replay the expensive mirror workload merely to diagnose the cause:

- Repeated same-domain/two-binding calls give exactly first+final persisted reads;
  ordinary calls outside a phase remain fresh. Distinct exact domains never alias.
- Changed generation, unregistered/foreign binding and immediate in-process
  withdrawal reject on a cache hit; original deadlines/resource checks still run.
- Final adoption tamper, replacement, missing file and persisted withdrawal
  reject and latch denial; restoring bytes or deleting a marker does not revive
  a domain whose denial was observed.
- Nested phases perform independent first/final checks; inner denial remains
  visible outside; body/final exceptions restore scope and leave no reusable cache.
- A final fresh read crossing a synthetic deadline is rejected by the preserved
  active callback. A new domain during finalization fails closed.
- Existing pin-final-sweep behavior, expected-pin conflicts and refusal paths are
  unchanged. The selected synchronous call graph contains no prohibited yield or
  authority escape. No deadline/counter/cap is increased.

These controls establish the changed boundary and operation-count reduction,
not complete mirror success or final-v5 deployability. After source review and
one bounded control run, root can decide whether the one consequential fresh
integration is worth its expected payoff. Preserve mirror01 and current114.

Independent challenge and detailed control planning are recorded separately in
`VALIDATION-PHASE-REVIEW.md` and `VALIDATION-PHASE-CONTROL-PLAN.md` when finalized.

# Two-slot custody lifecycle: concrete source cut

2026-10-21, core_release, under
[BOUNDED-GENERATIONS-IMPLEMENTATION](BOUNDED-GENERATIONS-IMPLEMENTATION.md).

**Source implemented and author-inspected; independent review and execution
remain pending.** No product imports/tests, runtime, deletion, installation,
Git changes, resource survey or old campaign were performed. These additions
are not in the consolidated 121-file installation. Its actual build audit was
finished first in `CONSOLIDATED-BUILD-OUTCOME.md` (`8d732943...`).

## Exact files

Paths are relative to the canonical project root.

| Fresh source | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/bounded_generations/placement/lifecycle.py` | 31764 | `6852b5a20d4b188d328c5554f40e0bdfb2b20f84943ac689350459a5e8b2f90d` |
| `software/v5/bounded_generations/client/serve_generations.py` | 8896 | `404365849dd0e41860ba8ccda01a5b064d028241a2d8b0063d76936fcd306687` |

They add logical `v5/placement/lifecycle.py` and
`v5/client/serve_generations.py` to the existing package namespaces. They reuse
the exact selected `PlacementService` (`7e735337...`), advertisement
(`5aa23ee7...`), placement ledger/controller and portable location classes.
No existing file, source map, fixture or used installation is changed.

## Owner-facing interface

The existing trusted-owner Windows/whole-process containment model remains.
Neither this manager nor arbitrary owner Python is a hostile-source sandbox.

```python
manager = ManagedGenerations.open(
    root, config, create=True, deadline=owner_monotonic_deadline,
    calls=128, cpu_seconds=30)
record = manager.allocate(slot, generation_config)
services = GenerationServices(manager, runtime)
await services.start_slot(record["generation"],
    outer_deadline=fresh_finite_deadline,
    location_deadline=fresh_location_deadline)
service = services.service(record["generation"])
# Use the unchanged owner token / placement / retained-advertisement APIs.
manager.seal(record["generation"])
await services.close_slot(record["generation"])
# Later, with a valid explicitly adopted time model and expired promises:
clock = manager.adopt_clock(lower_utc_ms=lower, valid_for_ms=validity,
    rate_error_ppm=rho_ppm, model_id=config["clock_model_id"])
await services.retire_slot(record["generation"], clock)
plan = manager.plan_reclamation(record["generation"])
```

`config` has exactly `schema`, `epoch`, `clock_model_id`, `registry_pages`,
`owner_reserved_bytes`, `registry_reserved_bytes`, `cleanup_reserved_bytes`,
`protected_roots`, and a two-element `slots` list. Each slot fixes
`reserved_bytes`, `max_cells`, `max_runs`, `read_endpoint`, `intake_endpoint`,
and one explicit IPv4/IPv6 TCP `listen` address. The six role ports must be
distinct. Manager root must be ordinary, exact and disjoint from the named
protected source/installation/user-data roots. Creation requires a fresh root.

`generation_config` has exactly `workspace`, `placement`, `service_limits`,
`egress`, and `location`. Placement is the current exact config with only its
`generation` field omitted; the manager derives that identity. Location is
the existing V1 index-provider config with only `state` omitted; the manager
binds that fresh state path per run. Its namespace, egress, read endpoint and
listen address must agree with the slot/generation. Other mathematical,
placement and network limits are interpreted by the unchanged concrete APIs.

`runtime` binds `source_root`, `installation_root`, the existing exact
`source_pins` and exact `role_pins`. The existing adopted locator runtime still
checks its pinned assets. No arbitrary callback supplies a locator or close
result. TLS contexts are optional explicit arguments to `start_slot`, with the
unchanged service's exact endpoint/TLS checks.

## Implemented state and safety arguments

The owner lock and capped SQLite registry contain one meta row and exactly two
slot rows, not an ever-growing event log. Each occupied record carries one
bounded exact configuration, immutable original horizons, cumulative runs,
current phase, current run state and at most one closure digest. The registry
checks slot membership, bounded monotone sequence, retired floor, derived
generation identity and run/phase census on reads. Database commit uncertainty
poisons the current manager instead of pretending a failed reservation is free.
Root's source reread identified partial-open cleanup ordering: the corrected
release path now attempts both database and owner-lock closure even if either
throws, preserving the original opening failure and retaining cleanup uncertainty.
It does not mark any managed actor CLOSED or free a slot.
The independent review also identified construction-before-attachment cleanup:
`PlacementService.open` can succeed before the manager rejects attachment.
The root-selected correction retains that exact local service, attempts both
service and locator close independently, preserves the primary exception with
bounded cleanup notes, and leaves the run UNKNOWN/charged. Successful cleanup
of an unattached object is never converted into a durable CLOSED warrant.
The second reviewer correction preserves the existing automatic finite shutdown:
retirement closes the grant and sets the service wake event, but does not set
`_closing` itself. The monitor's `finally` therefore still schedules its exact
tracked close task. The existing grant guard immediately forbids new work;
the composer still awaits the ordinary service close before durable retirement.

**Allocation before creation.** `allocate` durably consumes the sequence and
slot before creating the exact deterministic `slot-s/g<sequence>` directory
and marker. Partial failure remains charged. The original admission/retention
horizons are not rewritten on reopen, and successive allocated retention
horizons cannot decrease. There is no absent-generation recreation path.

**Run charge before output.** `reserve_run` requires a current exact generation,
matching marker/config, a closed/no prior actor, and remaining original run
allowance. It durably consumes that run before `start_slot` creates any
`run-NNNN` directory. A reopened generation uses the existing workspace but
fresh Node state/evidence paths and explicit current finite owner deadlines.
Core ledger run count must equal manager run count before exposure. The same
owner budgets are not reset by a failed startup.

**Exact service ownership.** Attachment requires the real selected
`PlacementService` and `ServiceLocationProcess` classes, a fresh unstarted
locator/service, the exact workspace path/config and current run census.
The manager retains their current object identities. It does not accept a
caller-supplied dictionary, boolean, PID, released lock or free port as closure.

**Seal before re-exposure after intent.** `seal` first checks current live
authority and idle intake/controller/advertisement, writes `SEALING`, calls the
existing synchronous core seal, then writes `SEALED_SERVING`. There is no await
between these steps. A safely closed generation with retained seal intent is
sealed before a later service starts listeners. Unknown prior actors are held
instead of reopened to finish the operation speculatively.

**Retirement is not deletion.** `begin_retire` requires the conservative lower
bound to reach the original retention horizon, persists `RETIRING`, then
immediately revokes any current service grant and wakes its shutdown path.
This also allows an expired OPEN generation to close and retire without
inventing a seal under an expired grant; this matters if its final finite run
ended before an explicit seal. `commit_retired` requires fresh time evidence
and current run `NONE` or proven `CLOSED`, with no current owned actor. Only
then does it write `RETIRED` and advance the floor over a prefix without an
unretired generation. No retired generation can reopen.

Independent review identified a late-start race: retirement could run after
the underlying asynchronous service start completed but before its shielded
caller resumed. `_started` now requires both RESERVED and an original phase
in PROVISIONING/OPEN/SEALING/SEALED_SERVING before any positive state update,
so it cannot overwrite RETIRING. It also reruns the exact service's current
authority/configuration/role checks before writing LIVE. This closes the
separate expired/revoked-grant boundary without changing shutdown ordering.

**Actual same-run close.** Closing attempts the unchanged service shutdown,
then verifies its CLOSED report, exact original roles, every cleanup facet,
real listener/task sets, closed stores/grant, and reaped/completed locator
process/tasks. Only that current handle can commit `CLOSED`. Failed or missing
construction/closure remains UNKNOWN/INCOMPLETE with its slot/run charged.
On manager reopen, persisted RESERVED/LIVE/CLOSING becomes UNKNOWN; a saved
deadline or close-looking report cannot recreate execution authority. Cleanup
of exact current objects can still be attempted after manager write authority
expires, but no expired guard can assert a durable positive close.

## Conservative clock premise

`ConservativeClock` is a fresh same-manager in-memory adoption, not persisted
authority and not a new clock-synchronization protocol. The owner explicitly
adopts a model digest and asserts an initial UTC lower bound L and maximum
monotonic rate error rho for a finite validity interval. Using integer arithmetic,
the lower bound is `L + floor(elapsed_monotonic_ms * (1-rho))`. A backward
monotonic value, expired interval or foreign manager refuses. System wall-clock
jumps and previously observed maxima are not inputs.

The retirement implication remains conditional on that adopted model:
lower bound >= original T implies every promised horizon <= T has elapsed.
The API does not manufacture a trustworthy UTC source. Registry rollback or
cloning by the trusted owner is likewise not prevented by a local counter;
restoration needs a new explicitly adopted epoch and its own treatment.

## Exact remaining implementation prerequisites

1. **Reclaimer, not another retention theory.** `plan_reclamation` checks the
   retired identity/marker and returns a read-only boundary plan. It never
   unlinks, changes phase or marks FREE. Both retired slots therefore remain
   occupied in this cut. Root must separately select an exact ordinary managed
   file inventory, finite reclaim authority, failure recovery and verified
   absence before a FREE transition. No current project directory is eligible.
2. **Crash-owner recovery.** The same-process CLOSED path is concrete. Recovery
   of UNKNOWN prior actors needs exact supervisor run-bound positive closure
   evidence or an actual finite recovery operation for those actors. This cut
   deliberately has no permissive imported-report/boolean override.
3. **Physical-envelope adoption.** The registry checks 4096-byte pages,
   DELETE/FULL, requested MEMORY temporary storage and a finite page cap. The
   already written `PLACEMENT-LIFECYCLE-SPACE-BOUND.md` still requires exact
   selected Python/Node SQLite/VFS correspondence, the Node temporary-storage
   guard and capped persisted outputs before claiming its physical envelope.
   Owner byte allocations here are charges, not verified physical quotas.
   `physical_envelope_adopted` remains false. No saturation experiment, RAM
   upgrade or fresh resource study is justified by this dependency.

Thus this is the concrete bounded lifecycle/composition implementation leading
to sustained custody, not a completed claim that generations already recycle.
Independent source review should now target these exact state/actor boundaries;
the prospective focused-control owner has been told not to invent a parallel
API. Runtime and tests remain root-selected after the higher-priority installed
smoke issue is resolved. No mathematical admission or useful-growth claim
follows from this source checkpoint.

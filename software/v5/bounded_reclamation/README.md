# Bounded custody generations

This SDK component lets a custody operator replace expired generations without
accumulating an ever-growing local history. It is an owner-local resource
mechanism, not a blockchain, mathematical verifier or global retention policy.
It does not decide which mathematics is worth keeping.

Logical modules: `placement.lifecycle`, `placement.reclaim`, and the unchanged
`client.serve_generations` composer from `../bounded_generations/`.
This source cut is not yet part of the consolidated installed distribution.
Current evidence and exact adoption decisions are in
`research/cycles/v5-2026-10-20/BOUNDED-RECLAMATION-*.md`.

## What an operator gets

A manager has two fixed slots. A slot holds one immutable generation identity,
original configuration, retention horizon and run allowance. A second slot
allows overlap while an older generation finishes its promises. Allocation and
each service run are charged before their files or processes are created.

An operator can start a current generation, seal it against new placement,
continue serving retained objects, and retire it after its original retention
horizon. Reclamation then removes only a known closed layout and frees the slot.
The next allocation gets a greater sequence and a different identity. Old
identifiers never acquire authority over the replacement generation.

This does **not** guarantee that another custodian still holds expiring data.
Replication and renewal must happen before expiry through the existing placement
interfaces. If no usable copy remains, a certificate cannot recover the data.

## Owner API sequence

Use a new private ordinary directory, exact manager configuration, selected
runtime pins and a finite enclosing process-tree supervisor. No remote request
may choose the manager path, clock authority or reclamation profile.

```python
manager = ManagedGenerations.open(
    root, manager_config, create=True,
    deadline=outer_deadline, calls=128, cpu_seconds=60,
)
generation = manager.allocate(0, generation_config)
services = GenerationServices(manager, adopted_location_runtime)
await services.start_slot(
    generation["generation"],
    outer_deadline=outer_deadline,
    location_deadline=locator_deadline,
)
service = services.service(generation["generation"])
# Use the existing PlacementService owner API and its original finite limits.
# manager.seal(generation["generation"]) stops new placement, not retained service.
```

At retirement, the owner must have a justified **lower** bound on actual UTC.
The manager conservatively advances that bound under the selected monotonic
clock error model. Reading an unauthenticated network timestamp or blindly
trusting a persisted wall-clock value is not such a justification.

```python
clock = manager.adopt_clock(
    lower_utc_ms=justified_lower_bound,
    valid_for_ms=finite_validity,
    rate_error_ppm=adopted_clock_error,
    model_id=manager_config["clock_model_id"],
)
await services.retire_slot(generation["generation"], clock)
manager.begin_reclamation(generation["generation"], {
    "layout": "DMKN_V5_CLOSED_GENERATION_LAYOUT_V1",
    "ownership": "PRIVATE_ENROLLED_NO_OTHER_WRITERS_OR_RESTORES_V1",
    "max_calls": selected_total_cleanup_calls,
    "max_entries_per_call": selected_window_size,
    "max_apparent_bytes": selected_slot_byte_ceiling,
})
outcome = manager.reclaim_step(
    generation["generation"],
    max_entries=selected_window_size,
    deadline=current_finite_action_deadline,
)
```

These fragments describe API order, not a complete runnable configuration or
automatic clock adoption. Close every owned service with `await services.close()`
and check all returned errors before `manager.close()`, also on failure. Original
deadlines remain in force during teardown. Never infer closure from an absent PID,
free port, released lock or a caller-supplied close-looking JSON report.

## Failure and recovery contract

- `NONE` means no service run was ever reserved. `CLOSED` requires genuine exact
  owned-role closure. A persisted `RESERVED`, `LIVE` or `CLOSING` run becomes
  `UNKNOWN` on reopen and remains held. Failed provisioning that was genuinely
  closed remains `INCOMPLETE`/`CLOSED`; there is no crash-owner closure shortcut.
- Cleanup intent, call charges and a deletion window are committed before
  effects. After interruption, reopen the same manager with its exact config
  and fresh finite owner authority. The original cleanup cap is not renewed;
  even an admitted census that refuses consumes one of its calls.
- A cleanup step returns `RECLAIMING` or `FREE`. Only `FREE` permits slot reuse.
  It can conservatively hold forever if its finite allowance is exhausted or
  foreign data appears. Do not bypass that refusal with a recursive cleaner.
- Unknown files, extra generations/runs, links, changed root identities and
  unproven closure refuse. Preserve the remaining tree and failure evidence.
  `workspace/operations` must be empty: even owner-created mathematical
  operation files are outside this deletion grammar and prevent reclamation.
- The new schema enrolls only new roots. There is no automatic migration of
  old managers, no restoration of deleted data, and no root recreation during
  cleanup recovery. Deletion of an expired enrolled generation is irreversible.

## Bounds and assumptions

The fixed layout has `N = 20 + 9R` roles for `R` charged runs, at most 36,884.
Each successful cleanup step performs pre/post full bounded metadata censuses;
invalid or exhausted admission can refuse before census. `W` admitted calls cost
`O(NW)`, not amortized constant time. A sufficiently funded single-window pass
costs `O(N)`. It never reads proof ancestry or hashes database payloads.

Private enrollment requires no other writers, restorers or namespace renamers.
Per-file historical identities are not stored; this is not protection against
a hostile same-user filesystem writer. SQLite page caps, apparent-byte limits
and logical reservations are not physical disk quotas or guaranteed free space.
`physical_envelope_adopted` remains false. Process resource limits likewise do
not constitute a hostile-code security sandbox.

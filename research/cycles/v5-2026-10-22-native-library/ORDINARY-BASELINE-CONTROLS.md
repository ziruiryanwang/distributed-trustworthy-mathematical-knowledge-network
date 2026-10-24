# Baseline changed-boundary controls: source checkpoint

2026-10-24. Author: `baseline_controls`. Source only; no selector, test, build,
owner, catalog, custody, native import or network operation has run.

## Scope

Fresh sources are `software/v5/ordinary_baseline/controls.py` and
`select_controls.py`. The intended single run is
`experiments/v5-local-checks/ordinary-baseline-controls-01`, with the unchanged
current preview package supplying parsers/planner. The runner snapshots the new
bundle/intake/control sources, pins the existing package/runtime bytes and three
small retained evidence fixtures, and uses 60 wall seconds, 35 CPU seconds,
768 MiB and two active processes. Root selects execution only after review.

The selector is file-only. It reuses only immutable package/runtime pins from
the prior preview selection, never its allowance, owner state or success report.
It creates fresh selection/output locations and refuses an existing attempt.

## Evidence supplied by the tests

Twenty-four focused cases use real ordinary syntax, V2 identities, the fixed
581-name inventory, three small retained dependency-linked units, the actual
new bundle parser and the existing pure admission planner. They test:

- Exact fixed-seed binding, target identities and whole-unit partitioning;
  incorrect inventory, basis target, forward order, byte census, target selection
  and aggregate count refuse.
- Manifest pin, global uniqueness, forbidden path fields and UnitID binding.
- Complete two-batch metadata feasibility before the first admission callback;
  later conflict or cross-batch forward dependency refuses without callbacks.
- Exact all-reuse, including a selected per-artifact cap smaller than an unused
  new-output allowance, and new work above a compatible independently selected root.
- Known catalog-root, custody-locator, CPU and retained-spool capacity refusals
  before checking. Native plan-wrapper bounds have a separate source derivation;
  no giant context fixture or lowered-scale experiment is required here.
- Input mutation between planning and intake retains only the confirmed prefix.
- A simulated durable second commit with a lost response reports uncertainty,
  does not assert rollback, and does not retry. Full child CPU reservations remain
  charged despite missing measured worker CPU, which is explicitly labeled a
  partial observation without a completeness claim. An invocation budget cannot renew.
- Aggregate binding-byte count includes one canonical array's brackets/commas,
  rather than incorrectly summing independent per-batch wrapper bytes.

## Deliberate nonclaims

The owner, custody rows, SQL responses, input filesystem and admission/commit
events are explicit inert test doubles. Their `CHECKED` strings are simulated
control-flow results, not mathematical warrants. Real owner/database/native/network
entry points are forbidden during the tests. The output states no mathematical
acceptance and no ordinary-library registration.

These controls do not establish durable recovery, binary correspondence,
filesystem defenses, native checking, large-library performance or deployable v5.
The future actual producer/intake/reference/delta workflow remains necessary.

## Review state

Root and `module_anchor_audit` received the sources for independent review.
The final source hashes must be read after any review corrections and supplied
explicitly to the selector. No current test result or PASS exists.

# Managed contribution: simultaneous process envelope

2026-10-21, core_release. **PASS: the selected path requires at most seven
simultaneous descendant processes, so the existing supported outer cap of eight
suffices.** Do not enlarge the frozen supervisor ceiling, alter product limits,
combine the actors, rebuild, or renew the original horizons.

This is a source-derived launch-envelope argument, not a completed test result.
All checks below were read-only; no selector or product code was executed.

## Why the original invocation refused

`Run-V5-Check.py` calls the frozen `A.limits_checked` before runtime pin sweeps,
output creation, snapshots and `A.supervise`. Frozen `operator/commons.py`
sets `CEILINGS.active_processes = 8`; the original selection requested12.
The installed `run_stage.Job` independently requires a bound in1..8. Thus
reducing the test selection to8 satisfies both existing checks. The reported
prelaunch refusal is consistent with source order and the independently
observed absence of `experiments/v5-local-checks/managed-contribution-01/`.

Original immutable input:
`d8f40d9c05b4edf5242b319f4dcba204ab5da09e11b8467091f5d5e7be7b1c6f`.
Original immutable selection:
`cbd5e7cb510dbb6818e50dd6ed31aaa24f4378d17c13448478b613187f51c67b`.

## Actual process tree

The enclosing Run-V5-Check Python process owns the outer Job but is not itself
assigned to that Job. Its one child is the driver, which is counted below:

```text
outer Job: proposed active_processes = 8
└─ 1. installed_contribution.py driver
   ├─ 2. host distribution.py + client.launch.py (same process)
   │  └─ 3. host boot.py + managed_owner parent (same process)
   │     └─ 4. worker boot.py + managed_owner worker (same process)
   │        └─ 5. node.exe / node_entry_services.mjs
   └─ 6. contributor distribution.py + client.launch.py (same process)
      └─ 7. contributor boot.py + contributor.py (same process)
```

Key boundaries read from the actual installed source:

- `distribution.py:1012-1018` creates a Python ModuleType, executes the pinned
  launcher in it and calls `module.main()` **in the same process**. There is
  no separate distribution-to-launch subprocess.
- `client/launch.py:212-216` creates one boot argv and calls `A.supervise` once.
- `client/boot.py:180-182` executes the pinned owner and calls its main function
  **in the boot process**. There is no separate owner interpreter.
- `managed_owner.py:311-318` invokes the supervised worker boot directly;
  it does not insert another distribution or launcher process.
- `placement/sessions.py:348-399` adds a BoundJob wrapper and calls the same
  `A.supervise` once. Identity binding and recovery are local function calls,
  not supervisor helper processes.
- The selected location controller starts exactly one Node process using
  `asyncio.create_subprocess_exec`; this generation starts one locator.
- Driver `ThreadPoolExecutor(max_workers=1)` runs the host supervisor in a
  **thread**, allowing the main driver thread to run the contributor supervisor.
  The driver creates no process pool.
- The contributor's CompositeProvider inherits the HTTP provider whose
  `start` uses `asyncio.start_server`. Provider, client, SQLite and fixture
  packaging stay in the contributor process. This path calls no prover,
  verifier, Lean tool or Node reader.
- Frozen `A.supervise:195-198` constructs a Job object and one suspended
  `subprocess.Popen(argv, ..., CREATE_NO_WINDOW)` child, then assigns/resumes
  it. It does not start a shell, launcher helper or recovery process.

Before contributor start the subtree is at most five processes. During the
actual contribution, all seven may coexist: host wrappers wait for worker/Node,
while the independent contributor boot and its wrapper remain alive. Closure
only removes these processes; it starts no successor or restart. Under the
adopted runtime behavior, seven is therefore the maximum distinct active OS
process count of this chosen path, not merely a sum of requested caps.

Do not infer this result from `total_processes` accounting or require that
counter to equal seven. Cumulative Job accounting, nested assignments and the
instantaneous active population are different concepts. The selected source
has not changed the underlying Windows nested-Job assumptions.

## Existing nested limits stay unchanged

| Job scope | Actual maximum descendants | Existing selected cap |
|---|---:|---:|
| Managed worker boot and Node |2|3|
| Public host boot, worker and Node |3|6|
| Host distribution branch |4|7|
| Public contributor boot |1|3|
| Contributor distribution branch |2|4|
| Entire driver tree |7|proposed8|

Nested cap sums need not fit the outer cap: unused allowances are not running
processes. The outer Job still bounds their actual simultaneous aggregate.
Nothing weakens mathematical, resource, closure, provenance or credential
checks. Host and contributor remain distinct public invocations with separate
processes, workspaces, limits and the actual network transfer. They remain
same-machine actors, not independently hosted replicas.

## Narrow successor selector review

Read in full:

- `Select-ManagedContribution01-EightProcesses.ps1`,2118bytes, SHA-256
  `209c840c88d0cb6ffa3fcd6cee6c06fc4682b44a532ca1da7c6e960c0dc51392`.
- `MANAGED-CONTRIBUTION-PRELAUNCH-LIMIT-REPAIR.md`,1381bytes, SHA-256
  `45906c46fd6d1a21a6cb16108d3ea2d0ccc3b5ff73d6c8f636f5cb67d6adb80e`.

The script authenticates both immutable files above before parsing. Its only
mutation to the parsed selection is `limits.active_processes = 8`. It checks
the expected test name and original12, then writes a **different fresh** path:
`experiments/v5-local-checks/managed-contribution-01-eight-processes-selection.json`.
The old selection/input are never opened for writing. Sources, argv, other
limits, original input pointer/hash and UTC horizons are preserved. Serialization
can change whitespace but not their values; the source selection had no JSON
integer outside exact signed64-bit representation on this path.

It refuses if the new selection or product output already exists, checks that
the original write horizon still has more than300seconds remaining, uses a
bounded serialization and `CreateNew`/flush, and does not execute anything.
Both intended fresh targets were absent at review. This point-in-time check
does not replace the script's recheck or the existing product horizon guards.
The private preparation is neither rerun nor inspected; there is no credential,
ACL or new input operation in this successor.

**Recommendation:** adopt exactly selector209c840c for one preparation, inspect
its new selection, and use only the same still-valid original input/horizons.
If any original horizon guard refuses, preserve that refusal; this review
authorizes no renewal. No product rebuild or repeated control campaign is needed.

## Installed anchors

| Source | SHA-256 |
|---|---|
| `distribution.py` |`eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813`|
| `sdk/v5/client/launch.py` |`523a3031da86457037af3c41f87425cd406e5fe3fcf6a2edb2d87eff9b59ef78`|
| `sdk/v5/client/boot.py` |`76cdcd42379d61c5fe37dc86a23363687c084c56887302dcdd922aa9b089ce2b`|
| `base/operator/commons.py` |`6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9`|
| `base/receiver/helpers/run_stage.py` |`bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028`|

Driver `f2aa0cac`, owner `75c0e8a9`, contributor `367e875a`, supervised sessions
`b4cfab61` and location controller `eeb82d5d` retain their previously reviewed
selections. This investigation does not reopen unrelated source review.

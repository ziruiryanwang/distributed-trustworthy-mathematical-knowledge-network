# Independent receiver-build source review

Disposition: **PASS_SOURCE_PLAN_AND_EXACT_BUILD01_SELECTION**.

Read-only review of `build.py` (12,375 bytes,
`391575e16709589acfaf38b5d6e76e380fcfe7ff0c4d10ae0e3067a1fac41852`)
and `BUILD-PLAN.md` (5,124 bytes,
`0254f817363896976e987e9b76a547fa11dc9770e271c159a2eedc2b78196de9`).
The reviewer also read the reused helper's path, pinning, JSON, census and fresh
write functions, the installed manifest and receiver import declarations. No
compiler, imported helper/product code, native command, owner/database or Git
operation ran. This review supplements `REVIEW.md`; it selects no runtime.

No source blocker found. The adapter's dependency order agrees with the actual
eight-module receiver imports: reuse OriginalExpr, OriginalDecl and
BootstrapSupport, then compile CheckedExtension, LocalSnapshot, OrdinaryExport,
BasisSnapshot and OrdinaryWorkflowWorker. The latter two unchanged sources are
recompiled because their imports changed. No authoring helper or fixture is run.

The source/output scope checks constrain work to the existing local-check
snapshot layout and its fresh sibling `native` directory. Reused sources,
objects, supervisor and nine named runtime files are checked against the pinned
installed manifest. The helper is pinned before loading and defines ordinary
local paths with no redirections, single-link files, fresh exclusive writes,
bounded hashing and exact census. The three changed sources and builder are
selected by the outer runner; their absence of hard-coded expected hashes in
the adapter is therefore intentional, not permission for an unpinned launch.

Copied inputs are read back, recorded and rechecked after clean compiler closure.
The worker checks its own source identity and initial source/object census,
scrubs inherited Lean/Python/PATH settings, and uses only the fresh helper path
plus the trusted Lean sysroot. Five sequential commands run under one supervised
Job with remaining original wall/CPU allowance and a cleanup reserve; the outer
runner provides the aggregate bound. A clean exit, reaped child, closed Job,
zero active/terminated processes, empty cleanup errors, known CPU and empty
native stderr are all required before success. A failed call stops the sequence;
partial outputs remain as evidence.

The final object census requires all eight `.olean` files, permits only named
compiler companions for the five compiled modules, and enforces per-file and
aggregate validation bounds. Those checks are not a hard disk quota. The result
explicitly says `COMPILED_NOT_TESTED_OR_ADOPTED` and discloses that the nine
named runtime pins are not a hermetic compiler/runtime closure. Protected local
storage and trusted toolchain assumptions remain unchanged.

For root's later launch review, the stated six source snapshots and 22 external
pins are consistent: two manifests, five reused sources, three reused objects,
three supervisor files and nine runtime files. Verify their actual values and
the fresh output before selection. The proposed inner 180 wall/120 CPU/1024 MiB
and outer 240 wall/150 CPU/1280 MiB are finite, with four processes sufficient
for runner, adapter, compile worker and Lean. This is not a measured cost or a
reason to renew a failed allowance. Focused controls, a new installation identity
and any fresh owner/intake remain separate decisions.

## Exact build01 selection

The subsequent reviewed selection is
`experiments/v5-local-checks/kernel-admission-build01.selection.json`, SHA-256
`6b9ca2c90ca8b9796b23f3761a5f339f63cdf1c9d896c71c6d316e875eb66635`.
All eight source pins (the six core inputs plus CONTRACT and BUILD-PLAN) and
22 external pins were independently compared with actual file bytes: no
mismatches. The output `kernel-admission-build01` was absent at review time.
The actual argv, fixed source/output layout, inner 180/120/1024 and outer
240/150/1280/four-process limits match the reviewed plan. The unchanged
`Run-V5-Check.py` was read in full: it validates the exact selection, snapshots
sources, supervises the fixed command and rechecks snapshot/external bindings.

**GO for this one compilation selection if root chooses it.** This clears no
fixture execution, owner state, intake, package adoption or automatic retry.

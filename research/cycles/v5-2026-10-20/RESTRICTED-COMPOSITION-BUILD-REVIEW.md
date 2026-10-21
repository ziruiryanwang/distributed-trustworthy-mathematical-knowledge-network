# RC native builder and selector: independent source review

2026-10-21, core_release. Source-only review requested by root. No selector,
compiler, checker, control, guest, receipt or network operation was executed.

## Disposition

**PASS for the adapter/selector source boundary and source reachability.** All
fifteen selected source files now exist, and their module/include/direct-crate
closure agrees with the recipe. Final launch selection still requires their
separate semantic/control review and exact finalized source pins. This is not
a claim that the code compiles or passes controls.

Reviewed exact sources:

| File | SHA-256 |
|---|---|
| `software/v5/restricted_composition/build.py` | `ae40fd0bf9209b8dac6e1edc297d1ae34f4000b1a92d5f9d39f046c740a9d121` |
| `research/cycles/v5-2026-10-20/Select-RestrictedCompositionBuild01.ps1` | `b66c248be5f9f4ed3af718e7c38fbfef801bc4ea5bc9ad69a53d29a8fb951ad8` |

No adapter correction was required by this review. Do not turn this source PASS
into actual build evidence or into a new-image/cryptographic trust adoption.

## Exactly what can execute

The selector hashes thirteen new files and two unchanged files into one15-entry
selection; it does not import Python, invoke rustc or launch a test. Its builder
hash must match the caller's explicit expected digest. Canonical cwd and fixed
canonical paths are enforced. Existing selection/run/attempt paths refuse;
selection writing uses CreateNew, exclusive access, UTF-8 without BOM and a
durable flush. It creates no second workspace or alternate source hierarchy.

The builder requires the canonical script path/cwd, pinned Python and DLL,
isolated/no-site/no-bytecode/nonoptimized interpreter mode and exactly two
arguments. The selected JSON must have the exact compile-only schema/name and
exact15source set. Unknown source names cannot extend compiler reachability.
It copies those sources into a fresh source snapshot and checks size/SHA;
final source-map comparison rejects added/changed/missing snapshot files.

Only three rustc commands are derived from the retained, hash-pinned
`proof-validation-integration-build-01/compile-commands.json` aggregate recipe:

| Label | Crate / type | Root | Added project externs |
|---|---|---|---|
| rc-core | dmkn_rc_relation / rlib | lib.rs | none beyond retained module relation |
| rc-aggregate | dmkn_aggregate_relation / rlib | aggregate_lib.rs | new RC core |
| rc-controls | dmkn_rc_controls / bin | controls_root.rs | new RC core and new aggregate |

All three retain explicit `dmkn_module_relation=<retained original rlib>` and
the same selected `serde_json` rlib, target x86_64-pc-windows-msvc, edition2021,
overflow checks, unwind panic, opt-level2, embedded bitcode, selected MSVC linker
and prior dependency/native-library search paths. Only exact one-occurrence
source/output replacements are accepted. New artifacts have distinct metadata
suffixes and an explicit new-run dependency search directory. Controls add fat
LTO but no `--test`. The binary is compiled, **never invoked** by this builder.
The original checker/module relation are retained binary dependencies, not
fresh compiler roots; no Cargo/dependency/checker rebuild occurs.

The old command/source-map/result records and two original rlibs have hardcoded
SHA pins. Original build PASS plus exact finalized attempt binding and absence
of `FINALIZATION-FAILED.json` are prerequisites. The two reused source records
must equal their original source-map entries. The174-entry retained runtime map
includes the actual rustc executable; the recipe explicitly supplies the old
module and serde_json externs. The compile-result and recipe selection records
are not interpreted as mathematical authority.

## Source reachability

The intended closure is explicit, not a directory-wide copy:

- Core `lib.rs` reaches `relation.rs`, `syntax.rs`, `foundation.rs`, `typing.rs`.
  Growth confirmed the tiny compiled signature is inside foundation.rs, with no
  generated side file, full-F include or additional include path.
- Aggregate root reaches aggregate_relation/census/wire plus unchanged
  aggregate_claims/header and membership via their relative paths.
- Controls root reaches controls.rs plus the selected census/wire source for
  private counter tests; real positive/graph checks use the compiled aggregate.
- build.py and fixtures.py are pinned preparation sources, not rustc roots.
  Fixture generation is not invoked by this compile-only builder.
- Original canonical/commitment/journal/policy/general-checker implementation
  is reached through the pinned retained module library, not mutable Rust source.

The completed source declarations/imports have now been inspected: no additional
`mod`/`include`/direct dependency escapes this15-file list. The direct crates are
std, serde_json, retained dmkn_module_relation and, where applicable, the new
dmkn_rc_relation/dmkn_aggregate_relation. Both reused files exactly match their
retained source-map hashes. `run_controls.py` is outside the compile map and
is not reached by any rustc root. This closure check is not a duplicate broad
semantic audit. Later implementation changes need another closure check only
if their imports/module paths or compiler roots change.

## Resource, evidence and cleanup boundaries

The three commands share **one** Job and phase; allowances do not reset per
compiler. The exact wrapper changes the inherited phase call to180CPU seconds,
1024MiB Job memory and six active processes, with240seconds phase wall time.
The controller has30CPU/360wall checkpoint checks. These are separate resource
coordinates; controller CPU is not hidden inside the worker Job total.

The inherited runtime monitor starts children suspended and without a visible
window, attaches them to the owned Job before resuming, redirects stdin, and
tracks per-command logs and before/after Job counters. Failed assignment kills
and reaps that child. Failure kills the owned Job; cleanup refuses remaining
members, Job limit terminations or uncertain closure. Only the retained exact
VCTIP executable in the owned Job can receive the selected postbuild telemetry
cleanup; arbitrary user applications are not killed by name.

The child environment is explicitly constructed, not inherited credentials.
Compiler/temp/profile outputs remain under the fresh run. The output allowance
is512MiB/2048entries, sampled at refresh points, and logs have the inherited
one-MiB sampled limit. **These are not filesystem quotas or a proof of a hard
physical-disk high-water bound.** Controller time checks are also boundary checks,
not an OS hard limit on a single hashing call. An eventual outer invocation
must preserve the separate bounded controller envelope.

Every command is recorded with exact argv, exit/status, logs, timing and cleanup.
The successful report pins all three outputs; zero checker/module/dependency
rebuild, test/native-mathematics/guest/proof/network call fields match the command
set. A compile success is overridden by cleanup/final input or snapshot failure.
The result and finalized attempt are written once; a last output-census failure
writes an overriding finalization-failed marker and exits nonzero. Partial
directories survive failure and prohibit implicit retry under the same name.
Final report/exit tail is explicitly outside the reported sampled accounting.

No runtime-capacity experiment, hardware inspection, old build campaign or
cryptographic proof was repeated during this review. The next necessary action
is completion of the separate core/control review and root's bounded decision.

## Controls invocation source review

The following later root-owned preparation sources also receive a scoped
**PASS**, conditional on the actual completed build and finalized control set:

| File | SHA-256 |
|---|---|
| `software/v5/restricted_composition/run_controls.py` | `ff9a23e03d8356adb5eddaeabfe8adfc1cbb6bfac791d4e3a3203e91ebfba589` |
| `research/cycles/v5-2026-10-20/Select-RestrictedCompositionControls01.ps1` | `da159306a5d8638076cab5b6a6a5a42dc1bf72be046316815b5c81c89ba397cc` |

This is not permission to execute the still-preparatory control source. The
observed draft controls.rs deliberately reports PREPARATION_NOT_COMPLETE while
its private-core cases are unfinished. The runner will reject that report;
root must not select this draft merely because the adapter is correct.

The selector requires the caller's expected build-result/binary/adapter hashes,
successful three-compile status, no finalization-failed marker and exact attempt
binding. It checks binary digest/size against the build output and binds the
build selection, including that build's fixture source digest. Its19retained
runtime pins plus build result/binary/attempt/selection and3fixtures give26pins.
Nine source files comprise Run-V5-Check, the adapter, fixture builder and exactly
six module package/codec/model/native-row/witness sources. Their import closure
was inspected; there is no additional package or subprocess dependency. Source
creation is exclusive and no selector operation launches Python/native checks.

The actual proposed invocation uses the pinned isolated Python and existing
snapshotting Run-V5-Check, with a45CPU/90wall/512MiB/3process shared Job and
one-MiB outer stdout/stderr limits. The new adapter is required to execute from
the selected sources/software/v5/restricted_composition snapshot and verifies
every imported module's exact origin. It reads only the three pinned retained
fixtures, constructs one canonical four-field fixture of at most4MiB, then runs
the one pinned control executable with60seconds timeout. It does not restart a
timeout or gain another enclosing allocation. The outer Job contains/reaps the
native child and its possible descendants.

The base journal is retained genuine evidence, but this harness does not
re-verify its receipt. It reports conditional refinement evidence, not new
certificate authority. Fixture and binary digests are rechecked afterward;
stdout/stderr are bounded before reading; all retained fixture digests are
rechecked. A native report passes only on exit0, exact expected unique test
count, all per-test PASS, empty errors, valid refusal names and explicit false
crypto/global-growth flags plus the expected conditional authority label.
Report-count expectations must be selected from the finalized reviewed control
source. No command invokes a guest, produces a receipt or accesses the network.

Inner native log sizes are checked after execution, not continuously; the
outer supervisor limits resources and its own redirected logs, not arbitrary
child output files. Do not call these checks a hard whole-output disk quota.
Errors before the adapter report remain failures captured by the outer owner;
they never become an empty passing suite. The source review cannot predict a
passing actual build/control outcome.

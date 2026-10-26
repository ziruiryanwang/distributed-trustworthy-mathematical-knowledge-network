# Narrow native exact-name admission controls

Source preparation only under CONTRACT. Root owns compilation, exact selection,
execution and adoption. No control, compiler, Lean, owner, database or Git
operation was run by the control author. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`; checkpoint is
`research/cycles/v5-2026-10-26-local-discovery/CHECKPOINT.md`.

## One fixture and the changed boundary

`KernelAdmissionChecks.lean` imports the selected successor LocalSnapshot and
CheckedExtension. It reuses the existing AdmissionChecks/LocalSnapshotChecks
patterns, without copying or rerunning their broad campaigns. The three new
product files and the eight-module receiver build have separate owners.

Its parent is explicitly **conditional owner-selected Init**, not a protected
mathematical warrant: import the selected local Init, serialize only eleven
records (Eq/refl/rec, the four Quot records, Bool/false/true/rec) with the existing
`saveModuleData`, then restore through unchanged `restoreLocal`. There is no
456-unit seed replay, Std closure, owner/catalog or test-only product hook.

The central three definitions have genuine full-name collisions under Lean's
`privateToUserName`, but distinct exact names:

| Full name | Type/value |
|---|---|
| `_private.KernelAdmissionAlpha.0.KernelCollision.token` | Bool / false |
| `_private.KernelAdmissionBeta.0.KernelCollision.token` | Bool / true |
| `KernelCollision.token` | Bool → Bool / identity |

Private names are constructed with actual `mkPrivateNameCore`. Before checking,
the fixture asserts both private flags, all exact inequalities and both
projections to the public name. Opposite private values and the public function
type make loss of exact-name identity consequential, rather than testing three
interchangeable proofs.

The agreed product APIs are `CheckedExtension.checkKernelBatch`, returning
`KernelCheckedBatch.environment : Kernel.Environment`, and
`LocalSnapshot.checkAndWriteKernelChunk`, returning `WrittenKernelExtension`.
The old `checkBatch`/CheckedBatch/checkAndWriteChunk and restoreLocal remain
Environment-based. No conversion through Environment.ofKernelEnv is used.

## Positive path and focused refusals

Expected claims are produced with actual checked Kernel.Environment.addDeclCore,
encoded by the existing codec and decoded again. This is fixture construction,
not authority granted to input rows: the tested admission repeats genuine kernel
checking and compares its output. Tiny invalid claims are constructed explicitly.

The first native snapshot admits all three definitions. Without restore or any
frontend update, the second admits three equality theorems that refer to their
exact names: alpha=false, beta=true, and public(true)=true. The second snapshot
must contain only its three new theorems although six constants inhabit stage
two. Both snapshot row arrays are checked exactly.

Restore the complete three-module chain through unchanged restoreLocal; verify
all six rows and exact module name arrays, and require zero stage-two names.
Check one new theorem using the restored beta theorem and its private constant.
No ancestor proof unit is resubmitted after restoration.

Then exercise the changed shared checking boundary:

- An actual same-name duplicate within a batch and an overwrite of an existing
  parent name must refuse, unlike the accepted projected-name collisions.
- The false=true proof must produce an actual declTypeMismatch/exprTypeMismatch
  in a direct kernel call. The new snapshot route must reject it and create no
  artifact, ruling out an unrelated resource refusal as the negative's basis.
- An ordinary expected row claiming alpha=true for the actual alpha=false
  declaration must refuse. A missing exact reference must also refuse.
- A tiny nonnested singleton inductive must pass with its complete generated
  group; changing its constructor's expected field count must refuse.
- A stage-two cap of two must reject the three-definition batch at the census;
  an uninitialized kernel parent must refuse. Failed calls must leave the
  immutable original parent empty of every fixture declaration.
- Finally, use unchanged Environment-backed checkAndWriteChunk on one
  noncolliding identity definition and verify its exact returned row/delta.

The known old frontend collision is deliberately not replayed: it can panic
and would add no evidence beyond the preserved actual Std failure. No exception
suppression, unchecked admission, declaration renaming or limit escalation is
part of the positive path.

## Finite shape and expected output

Checking limits are at most four units, sixteen new names, thirty-two stage-two
names, ten thousand scanned nodes, one million kernel heartbeats and depth one
thousand per tiny call. Snapshot limits are four modules, sixty-four names,
one MiB per artifact and four MiB total. Only four selected artifacts are written:
`basis.olean`, `first.olean`, `second.olean`, `frontend.olean`; the refused
`bad-refused.olean` must not exist. All are beneath one fresh fixture directory.

Main argv is exactly `PINNED_SYSROOT FRESH_OUTPUT_DIRECTORY`. Success requires
the conditional-fixture line, these sixteen PASS markers in order, and one exact
completion line, with zero exit and no stderr:

```text
genuine-name-projection-collision-fixture
exact-private-private-and-public-names-checked
later-exact-references-and-delta-only-snapshot
restore-full-names-and-check-only-new-consumer
true-exact-duplicate-in-batch
true-exact-parent-overwrite
bad-proof-is-genuine-kernel-type-mismatch
invalid-proof-refuses-before-snapshot
ordinary-expected-row-mismatch
unbound-reference-refused
complete-generated-group-checked
generated-constructor-row-mismatch
aggregate-stage-two-bound-retained
uninitialized-kernel-parent-refused
failed-batches-preserve-immutable-parent
unchanged-environment-backed-snapshot-api
```

Each is prefixed `KERNEL_ADMISSION_CHECK_PASS `. Completion is:

```text
KERNEL_ADMISSION_CHECKS_COMPLETE fixtureRecords=11 chainCheckedUnits=7 generatedGroupUnits=1 frontendUnits=1 conditionalFixtureOnly=true protectedCatalog=false basisAdoption=false
```

Those counts identify successful control paths, not total kernel invocations or
production acceptance. Fixture production, isolated refusals and the direct
negative kernel call also consume the selected whole-process budget.

## Prospective direct execution, not a selection

First require the independently adopted exact receiver build and its complete
source/object map. Build01 has returned raw success at
`experiments/v5-local-checks/kernel-admission-build01/native/lean-lib`; its actual
independent audit/adoption is still required. The fixture is
not a ninth receiver module and does not modify that build or installation.

The existing Run-V5-Check schema has no environment field. A minimal root-owned
direct selection can use a short inline Python bootstrap in its hashed argv:

```python
import os, subprocess, sys
env = {key: value for key, value in os.environ.items()
       if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
env["PATH"] = os.pathsep.join((r"D:\Python314",
    r"E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows\bin"))
env["LEAN_PATH"] = sys.argv[1]
code = subprocess.call(sys.argv[2:],
    cwd=r"E:\Distributed Trustworthy Mathematical Knowledge Network",
    env=env, stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
sys.exit(code)
```

After `python.exe -I -S -B -c <exact-code>`, supply the adopted lean-lib path,
pinned `lean.exe`, `-R`, immutable fixture snapshot directory, `--run`, immutable
fixture source, pinned sysroot, and fresh `{output}/fixture`. This sets the
selected import path before Lean elaborates the fixture, after removing every
inherited environment name beginning with LEAN or PYTHON (case-insensitively)
and PATH, then installing the same explicit Python/Lean PATH as build.py.
The child has closed standard input and no visible console window. The selected Python
parent waits for and reaps its Lean child, propagating its exit code. The bootstrap is an
explicit selected argv value, not a new selector or framework. Root may choose
another reviewed existing launcher. Do not use the old run_snapshot_checks
unchanged: it recompiles an old module and hardcodes the old fixture path.

Proposed outer allowance: 120 wall / 90 inclusive Job CPU seconds, 1,280 MiB,
four active processes, one MiB per stream. These are prospective test limits,
not an increase to product intake limits. The outer supervisor owns whole-tree
containment and cleanup. Do not run additional native work concurrently with
this selected control merely because the fixture is small.

Required snapshots: existing runner, this Lean fixture, TEST-PLAN and CONTRACT.
Required external pins: the adopted build's complete object/source map and
BUILD/result/selection evidence, the exact runtime map used for that build,
and relevant independent adoption evidence. Root must derive the final count
and concrete hashes from the actual build, within the existing runner limits.
Do not invent build hashes or silently import old CheckedExtension/LocalSnapshot
objects. Runtime pins are the existing cooperative trust boundary, not a claim
of a fully hermetic Lean toolchain.

Require immutable input rechecks, all sixteen markers and exact artifacts/row
census, normal outer zero-exit/reaping/Job closure, zero active/terminated
processes, no cleanup error and empty stderr. Preserve the first outcome and
partial files without retry. Root's independent outcome audit decides adoption.
No protected basis, Std compatibility replay, new implementation installation,
contribution, growth benefit or final-v5 qualification follows automatically.

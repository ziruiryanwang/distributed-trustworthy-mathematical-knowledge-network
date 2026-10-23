# Ordinary Lean core: combined actual outcome

2026-10-22. Independent reviewer: `lean_workflow_trace`. Read-only saved-evidence
review of controls02–07, exact source diffs and selected compiled prerequisites.
No rerun, new build, source repair or Git operation by this review.

**PASS for the selected metadata-preserving codec and conditional checked-batch
controls.** Exact core modules compiled in05, CodecChecks passed in05, and the
repaired admission test passed all15 named checks in07 using those exact05
modules. Failed02–06 remain failures; this does not relabel any complete run.

## What actually ran

| Run | Actual outcome | Known CPU seconds |
|---|---|---:|
| 02 | OriginalExpr parser errors: reserved `prefix` binder and record layout. | 2.296875 |
| 03 | OriginalExpr compiles; OriginalDecl constructor-record layout fails. | 3.609375 |
| 04 | OriginalExpr compiles; later OriginalDecl record layout fails. | 3.6875 |
| 05 | All three core modules compile; CodecChecks passes; AdmissionChecks parser errors on reserved identifiers. | 6.1875 |
| 06 | Admission-only elaboration fails because `decoded[i]!` requires an unavailable `Inhabited DecodedUnit`; core not rebuilt. | 1.75 |
| 07 | Admission-only execution passes all15 markers; core not rebuilt. | 2.671875 |

Known CPU is Job CPU plus the outer wrapper's own CPU; its supervision subinterval
is already included. Total02–07 is20.203125 CPU seconds, including failures. For07:
2.21875 Job CPU +0.453125 outer CPU;2.8281140998005867 outer wall seconds;
979,763,200-byte peak Job private commit. All six retained operations have reaped
direct children, zero final active processes, closed Jobs and no cleanup errors.
All retain90 CPU /180 wall /1,536 MiB /4-active-process limits. These small
fixture costs are not broad-library admission or useful-growth benchmarks.

## Repairs did not weaken the checks

Inspected immutable02→03 OriginalExpr,03→05 OriginalDecl and05→07 AdmissionChecks
diffs. Core repairs rename a reserved local binder and correct Lean record
layout. Test repairs rename `opaque`/`axiom` locals and replace partial fixture
indexing with explicit optional lookup that fails if either selected unit is
absent. All original test conditions, expected rejection markers, kernel
checking calls and parent-immutability assertions remain. No default inhabitant,
skip, trusted peer declaration or relaxed rejection criterion was introduced.

07's output contains exactly the following15 `ADMISSION_CHECK_PASS` markers:

- `actual-kernel-metadata-fidelity`
- `decode-and-check-actual-six-unit-batch`
- `invalid-proof-is-actual-type-mismatch`
- `invalid-proof-admission`
- `axiom-encoding`
- `axiom-admission`
- `unsafe-encoding`
- `unsafe-admission`
- `overwrite-admission`
- `overwrite-decoder`
- `missing-reference-decoder`
- `missing-reference-admission`
- `generated-constructor-inventory`
- `failed-batch-no-success-prefix`
- `immutable-parent-preserved`

The actual invalid-proof type-mismatch check matters: the subsequent broad
kernel/resource marker alone is not being used as evidence of mathematical
rejection. The six positive units and their scope are described in
`ADMISSION-SOURCE-REVIEW.md`. CodecChecks05 explicitly reports syntax-only
coverage rather than mathematical acceptance.

## Exact attribution and limits

Every retained02–07 source snapshot independently matches its own selection;
each result's selection hash matches the saved selection.07 selects05's three
`.olean` files and three corresponding source files as runtime pins. All six
hashes independently match. The07 driver additionally requires exact equality
between its selected core sources and05's compiled-source snapshots, sets
`LEAN_PATH` to05's build directory and runs only AdmissionChecks.05's command
log records successful compilation of OriginalExpr, OriginalDecl and
CheckedExtension plus successful CodecChecks before its separate test failure.
Thus07 is not misattributed to uncompiled new core source or an earlier build.

07 prints both `owner-selected-Init conditional=true networkParentWarrant=false`
and `ADMISSION_CHECKS_COMPLETE conditionalFixtureOnly=true publicDeployment=false`.
The fixture imports selected Init; it does not independently warrant the parent,
validate a peer binary, demonstrate durable persistence or exercise an ordinary
project return loop. Executable/DLL and selected compiled-module pins are not a
hermetic full Lean runtime-library proof. No security sandbox, private-syscall
trust bypass, succinct certificate or global-scale guarantee follows.

| Retained evidence | SHA-256 |
|---|---|
| controls05 `RESULT.json` | `b566005fd1523b32b27aa43222df37a7834eaee75f6627ab7473dae5de1fa11b` |
| controls05 `codec-controls.stdout.txt` | `2712ac3762a982c59aa0f760a19f240c0eedab259debfbf74c8970be5667ecc5` |
| controls07 `selection.json` | `fa6e5417e2e0555a07b77ea67da7c096f132b054a79100d6c202a7a835350754` |
| controls07 `RESULT.json` | `1ba5bc4a9106574109b2075b913e966e4e3822cdaaada9fafb76c36cb7e05cb6` |
| controls07 `admission-controls.stdout.txt` | `d4e2a9888a85ec91a9dd36653b55566d457e919012c7ccb4304973e095d8aaea` |
| controls07 `CHECKS.json` | `00430b184d95df52a2d6b73eff81d8f3cfc3b1b9d39af87e5a1af71d89eb447a` |

This closes the selected core control gate. It supports moving to warranted
parent selection, protected persistence and normal-project rebinding; it does
not justify another unchanged core campaign or a completed-v5 claim.

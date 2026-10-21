# Standalone validation: actual focused-control outcome

2026-10-21, independent core_release audit. **PASS_SELECTED_TEN_CONTROLS.**
The new standalone boundary and exact-owner import borrowing behave as selected
in the saved focused run. No product code was executed/imported, no tests rerun
and no source/evidence/Git state altered by this audit.

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Operation: `experiments/v5-local-checks/standalone-validation-controls-01`,
selected by root in `STANDALONE-VALIDATION-LAUNCH.md`. Source review3524a601 and
independent harness/selector reviewf73d4011 remain separate predecessor reviews;
this note audits actual evidence, not a duplicate source review.

## Exact source and evidence bindings

| Artifact | SHA-256 |
|---|---|
| Original/saved selection | `490b73d6f20140b950ba30e0f2b7e07c54d179d4b305cd916594963fa3471ff2` |
| RESULT.json | `295dbc8a87b98733a2ed7b2da45533fdc85b76939375b349c307feee410549fd` |
| controls-result.json | `15a937332a124ae5fcc381af45b3571b439b471e471149d162a9362386c1e7e1` |
| command/stderr.txt | `5e7155e9870e9bdddbfe7a4025325f5931e2bf966a51716b5a770e5c88499a8a` |
| Selected harness | `e944888dbd137298163eaba666024bf620eb9aa0f11678d9edea6be3e9f74667` |
| pin_phase successor | `ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881` |
| mixed receiver successor | `835d59809045c3e49f9d7e5483108f4034c591a3a82224e4155f4f7d0f6dcced` |
| imports_atomic successor | `8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595` |

Independently rehashed **119 source originals and119 snapshots**, all **114
logical selected-code copies** against their source/size/hash records, and all
**19 runtime pins**: no mismatch. Actual selected-code census is exactly114 files.
Relative to terminal-I114 inputd3519be1, the logical map has exactly the three
successors above,111 unchanged rows and no missing/extra keys. The two AST-only
reference files also match their recorded size/hash bindings; neither is an old
executed suite. Exact expanded argv, canonical cwd and all limit values match
the saved selection.

## Actual results, not exit-code inference

Read complete stderr and controls result: exactly ten named methods,10 executed,
zero failures/errors/skips, PASS, no forbidden calls. Stdout is empty; stderr
contains the ten individual `ok` lines and `Ran 10 tests ... OK` (1454 bytes).
Native, network and proof call counts are all0; mathematical_acceptance is false.

| Selected boundary | Actual observations |
|---|---|
| Original bodies/order | Both mixed old-check/new-check-phase and import live-phase AST bodies/order equal; reference files only parsed. |
| Standalone real observations |29-pin case:trust62 ->4, pin reads58 ->58;35-pin case:trust74 ->4, pin reads70 ->70. Both have2 real trust-origin resolutions. |
| Existing import borrowing |31 distinct pins,62 real reads,6 trust reads,2 trust-origin resolutions; one mixed check shares one root/final sweep. |
| Supplied deadlines |First-pin, final-pin and borrowed-pin expiry all refuse at the tighter supplied deadline; final case completed original body first. Simulated clocks, no sleep. |
| Live guards |Registered binding, local withdrawal, mixed profile, controller CPU and owner identity changes each refuse and revoke mixed ownership. |
| Independent nesting |Wrong owner, unregistered and default-nested cases each retain independent phases:4 actual repeated-pin reads,6 trust reads. |
| Copied-context lifetime |Borrowed copy refuses after borrow ends while root remains live; root/borrow copies refuse after root closure, even with permissive callbacks. |
| Conflicts/registration |Checker and expected-pin conflicts refuse; good record remains; tuple registration shape required. |
| Deferred finalization |Eight cases:pin, withdrawal marker, adoption bytes and post-real-resolution exception, each standalone/enclosed. Original mixed body completed; mixed revoked; enclosing import closes; independent I issuer is not newly closed. |
| Body failure/restoration |Body-only import failure preserves prior mixed ownership; substituted owner not borrowed/revoked; all three outer contexts restored and a fresh independent check succeeds. |

Original live guard calls are retained, and added guards are visible:29-pin
standalone baseline I/mixed calls62/31 become242/211;35-pin baseline74/37 becomes
290/253. Thus this is not blanket removal of checks. **Pin reads in those two
standalone cases do not decrease.** The demonstrated saving is repeated
persisted trust observation; no numeric CPU-speedup claim follows from counts.

## Scope and limits

The fixtures invoke real selected `_active`, `_check_install`, `_check`,
`_check_phase` and `_live` code with genuine freshly provisioned local trust
records/bindings, file origins and real pin reads. They are explicitly exact-class
structural shells, not ordinary constructed runtime adoptions. I has no executable,
mixed has no native executable, import source inventory is empty, and there are
no mathematical handles. Nonempty source-handle binding and mathematical admission
remain outside this test's dynamic coverage; unchanged body/order evidence and
previous real workflows are distinct evidence, not retroactive coverage here.

The origin failure is injected after an actual final filesystem resolution. It
tests exception propagation/revocation, not hostile path rollback. Trap counters
detect accidental external calls in a trusted harness; they are not a sandbox.
The assumed owner-serialized stable local code/filesystem model is unchanged.
No whole-operation trust cache, new checker or certificate authority is established.

## Resources and closure

Job CPU2.15625 =1.1875 user+0.96875 kernel; separate wrapper0.453125 yields
**2.609375 known CPU seconds**. Total wall **5.766483800020069 seconds**, child
cleanup through5.712915200274438. Supervision0.015625 is already within wrapper
CPU; test-runner elapsed1.937 is already within the operation wall, not additive.
Peak Job private commit31,989,760 bytes. Bounds remain45CPU/90wall/384MiB/two
active processes/1MiB per log; no renewal.

`COMMAND_EXITED_ZERO_AND_CLOSED`: child0, direct child reaped, Job closed, two
lifetime processes, zero active/terminated, no cleanup errors or termination
request. No runtime remains. Root reported an initial selector call blocked by
PowerShell policy before staging, then one process-local-bypass staging; this is
not a failed test attempt and does not change the single actual run audited here.

No focused-control blocker remains for these exact three sources. Root may
separately select their reviewed file-only installation. No passing mirror or
terminal-I workload should be repeated merely to restate this control outcome;
integrated performance and broader v5 readiness remain separate open claims.

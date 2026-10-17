# Local allocation build: exact selection and cap-delta review

2026-10-17, `v5_growth_decision`. Read-only independent prelaunch review;
canonical workdir/guard used. No compiler, test, host, proof or Git operation.
This checkpoint was separately assigned by root after LOCAL-NEXT-CENTRAL.

**PASS for this exact finite compile-only selection, conditional on root's
immediate headroom/no-overlap checks and completion of the separately selected
adoption controls. NOT RUN; no fit, host-adoption or proof claim.**

Selection:
`experiments/v5-local-checks/prover-allocation-build-01-selection.json`, SHA-256
`7a548b3f74c0c5bbe8bc2ba68e408a3dfdf22addefb9410b1a25f5d8be5d13ff`.
Its output directory and external attempt record were absent when reviewed.

## Exact changes checked

- Complete selector read. It requires canonical cwd, three fresh target paths,
  exact retained selection `049129da...71fa38`, a1,071-entry runtime map,
  four exact source pins and unchanged descriptor/patch identities. It prepares
  a fresh selection only; no process launch or retained-file write.
- All four current source byte lengths and SHA-256 values match the saved plan.
  Runtime key/value comparison against the retained stage-build selection gives
  exactly1,071 versus1,071 entries and zero changed/missing mappings.
- `build.py` now has SHA-256
  `cb557ac2bf8aa462710e234bc188b3b0709020b3927959c8431e52b7de46ecfd`.
  Replacing its two `2048` literals by `3072` **in memory only** reconstructs
  exactly the previously reviewed SHA-256
  `8ca39b2dc68fdab7ebe96eef2bf53ce212c3a5196acb626f7bc7b99263c91781`.
- `adoption.py` now has SHA-256
  `b41fd140a13782be3258452ecee7c7389bf2b8621f24fdb4d21f64962b334176`.
  Restoring its single cap literal in memory reconstructs exactly the reviewed
  `56b633aa0a528cb383f47cf5b1e73bd9a8b18387382c23d4c8114348b2cc6459`.
- The lowered2,048MiB value agrees in selector, saved plan, builder LIMITS,
  actual `InclusiveJob(240,2048,active_processes=6)` constructor and adopter
  LIMITS. The retained phase constructor's `(300,4096,8)` request is deliberately
  checked and replaced by this exact narrower Job, not accidentally honored.
- Recipe3f2d878d states the new cap and historical observations correctly.
  Descriptorc93a45a6 and patcha53940b6 remain unchanged. Two backend Rust
  rebuilds, two relation rebuilds, one stage-host link; no C++/checker/guest
  rebuild or produced-host/proof/network call is introduced.

The full original builder/adopter review remains in
SELECTIVE-FRONTIER-REVIEW.md. Exact old-byte reconstruction means this review
need not repeat the complete compiler-argv/dependency/environment audit.
The runtime-map comparison checks saved identities, not a fresh rehash of all
2.32GB of retained runtime bytes; the builder's unchanged before/after runtime
rebinding remains mandatory at execution.

## Finite envelope and selection rationale

Five serial disjoint Jobs: each240CPU/300wall seconds,2,048MiB private commit,
six active processes. Whole allowance1,200workerCPU/180final-controllerCPU/
1,800wall seconds, with ordinary-controller120CPU,1GiB fresh output,
8,192entries and1MiB logs per command. Failure stops the chain; no cap increase,
feature expansion, retry or automatic proof follows.

LOCAL-MEMORY-DECISION documents retained actual full SDK peak1,406.875MiB
(including `fresh:false` relevant libraries) and recent matching host-link
peak1,176.046875MiB. These justify one bounded compilation attempt, not a formal
upper bound for the changed direct-rustc recipe. Root must observe at least
3GiB available physical **and** system-commit headroom immediately before
launch, and exclude overlap with another large project Job. This margin is not
a reservation against unrelated user activity. Do not close user applications
or change system settings to manufacture it.

The4GiB proof-worker envelope is unchanged and not cleared by this review.
Actual result/closure/output/source-map review and the adoption boundary remain
necessary. A successful compiler operation establishes neither observed proof
memory fit, a genuine A receipt, useful-growth advantage nor final v5 readiness.

## Actual saved outcome audit — 2026-10-17

Reviewer: `memo_independent_review`. **PASS for the exact five-step compile-only
outcome.** The NOT RUN statement above is retained as the prelaunch assessment;
this section records the subsequent actual result, not a changed gate. Root
reports that its immediate physical/commit observations were 3,155,916 /
3,484,216 KiB with zero matching heavy processes before its one session51290
launch. This reviewer audited saved records and current bytes only, without
rerunning the builder, invoking the adopter, importing Python, executing the
produced host, or starting any native/proof operation.

Exact evidence:

- Selection remains `7a548b3f74c0c5bbe8bc2ba68e408a3dfdf22addefb9410b1a25f5d8be5d13ff`;
  the external selection and saved copy both rehash to that identity.
- `prover-allocation-build-01/RESULT.json`: 57,441 bytes, SHA-256
  `ac259e9db55275a0a8404e9cf881fd3779f2e7259ccfe134c8e93e3b180b4102`.
- External `prover-allocation-build-01-attempt.json`: SHA-256
  `2c61fd2ca46d86fe2d179f8728483bb5c1c207f248ab83f4bc4db4f273afb1e6`;
  binds that result hash and `PASS_PROVER_ALLOCATION_FIVE_STEP_COMPILE_ONLY`.
- No finalization-failure, cleanup-failure or override file was present.

### Exact inputs, transformation and dependency closure

Independently rehashed all four selected original sources, 180 snapshot/source
files, 172 original source inputs, 15 helper pins, all 1,071 runtime pins,
five result outputs and ten command logs, plus seven record/selection pins.
These checks covered 1,459 unique paths; all selected sizes/digests matched.
The runtime pins total exactly 2,320,491,997 bytes and agree with both INPUT-MAP
and the retained predecessor runtime map. No runtime dependency was silently
replaced by an unselected toolchain identity.

Independently reconstructed the expected 180-file source map from the selected
four adapters, descriptor SDK inventories, retained evidence records,
integration/stage source maps and generated preflight file. It exactly matches
the saved map. Actual source/generated trees have exactly those 180 files and
no reparse entries. The only SDK transformation is the descriptor-selected
preflight file: original 5,582 bytes / `bf427f0e...228bde`, patched 6,003 bytes /
`88fbf84e...b67396`, with exact patch `a53940b6...7fdc6c` and unchanged
descriptor `c93a45a6...ace710`. The patch is the reviewed byte-to-u32 allocation
correction with checked multiplication/alignment, not a relation/checker change.

Reconstructed all five argv arrays from descriptor templates and verified exact
equality to compile-commands.json, RESULT commands and separate command.json
records. Every declared new-library dependency edge occurs exactly once at its
selected fresh path. Reconstructed the base environment from the retained
environment with the new root and the two selected offline/telemetry settings;
all five step overlays also match. No inherited environment is enabled. There
is no Cargo, build-script, produced-host, checker or guest invocation in these
five actual commands.

### Five serial, closed Jobs

| Command | Worker CPU seconds | Command wall seconds | Peak Job private commit bytes |
|---|---:|---:|---:|
| `risc0_circuit_rv32im` | 50.156250 | 23.817590 | 617,472,000 |
| `risc0_zkvm` | 101.484375 | 32.097021 | 969,547,776 |
| `dmkn_module_relation` | 14.406250 | 3.276187 | 607,383,552 |
| `dmkn_aggregate_relation` | 2.890625 | 1.655404 | 510,058,496 |
| `small_aggregate_stage_host` | 158.343750 | 169.134295 | 1,240,559,616 |

Each command completed with exit0, zero starting Job CPU, no cleanup errors,
and a separately saved closed Job record. Each final active-process count is0;
Job-termination count is0. Five command intervals are disjoint and ordered;
each stays below 240 CPU / 300 wall seconds / 2,048 MiB. Job files, command
after-stats and RESULT phase-stats agree exactly. Four Jobs report two total
processes each; the final link reports four, giving12 across the serial Jobs.

The final link includes one explicitly selected owned VCTIP telemetry cleanup
with observed exit and the pinned executable identity. This is recorded, not
misrepresented as absence of cleanup. It is not a new broad user-application
termination or a hidden Job failure. Relation and host stderr contain only
three and four dead-code warnings respectively; the other logs are empty.

The actual rebuild counts are two backend Rust crates, two relation Rust
crates and one host link. Native C++ circuits, the independent checker and
guest images were not rebuilt. Host calls, guest calls, proof calls and network
calls are all0 in the reviewed compile path.

### Outputs and measured costs

The new stage host is 68,039,168 bytes, SHA-256
`263841ae256af217de2c00452c7f0688a2e9e58e6aa6d95457d5118aef04ff3c`.
All four fresh rlibs and the final executable rehash to their saved output
identities. A matching PDB is retained as an auxiliary build output, not an
extra execution or adopted runtime requirement.

Worker Job CPU sums exactly to **327.28125 seconds**. Disjoint measured
controller CPU is21.59375 seconds, so known total is **348.875 seconds**.
Overall reported wall is277.4021032000892 seconds. The serial maximum Job
peak is1,240,559,616 bytes (**1,183.08984375 MiB**), not the sum of the peaks.
The recorded final pre-report output census is122,688,176 working bytes /
309 entries, under the1GiB/8,192 caps. Its single disclosed INetCache alias
targets the same fresh run tree and was pruned by the census, not traversed.
Final report/exit tail is explicitly excluded from the measured CPU/wall
accounting; it is not asserted zero. No failure override was found after it.

### Scope of the pass

This establishes that the reviewed allocation-refined producer host and its
four selected Rust dependencies compiled within the selected local envelope.
It does **not** demonstrate reduced proof-time memory, executable semantic
correctness, a genuine A/H2 receipt, final integration, useful growth or v5
release readiness. The new executable has not been invoked or adopted as an
alias by this review. The existing4GiB proof-worker hold remains unchanged;
no cap ladder, automatic proof, retry or new budget follows from this pass.

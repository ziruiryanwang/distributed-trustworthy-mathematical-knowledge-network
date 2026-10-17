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

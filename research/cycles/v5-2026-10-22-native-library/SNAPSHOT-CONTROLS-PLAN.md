# Focused local snapshot controls: source and proposed finite run

2026-10-22. Root assigned implementation; execution remains root-only and has
**not** been selected or performed by this agent.

## Source changes

- `LocalSnapshot.lean` now returns `WrittenExtension { chunk : SavedChunk,
  environment : Environment }`. The returned environment is precisely the
  successful `checkBatch` environment. The private writer still receives only
  that same function's actual result; no new arbitrary-checked-result API.
  SHA-256 `488a76f4b8599a95bdc748c5e89187bc55e23f63d34cf52952702d93ff68795c`.
- New `LocalSnapshotChecks.lean` is a focused owner-authored source test, SHA-256
  `d2da1cb87e774404313e5985daea2663c0b24097f556edac04463a0e4c0d1c36`.

The reviewer `lean_workflow_trace` has been informed of this narrow API change.
No code outside the two assigned Lean files changed in this continuation.

## Checks and what each discriminates

| Expected marker | Concrete discriminator |
|---|---|
| `two-chained-deltas-without-intermediate-restore` | A polymorphic identity theorem is checked/written; B genuinely applies A. B uses A's returned in-memory environment without import between calls. The environment retains two stage2 names while each file descriptor contains exactly its own one-name delta. |
| `exact-map-restore-without-ancestor-checking` | A fresh restore consumes only the complete three-module local plan. It preserves exact A/B inventory rows, each stored chunk's one-name census, and moves their constants into stage1. No A/B inert proof packets are supplied to the checker again. |
| `restored-theorem-supports-new-consumer-proof` | Only a new C theorem using restored B is kernel-checked; one new checked unit, no old theorem re-admission. |
| `incomplete-import-plan` | Removing A while B still names A fails the chain validator before deserialization. |
| `wrong-parent-plan` | Replacing B's recorded parent by the basis fails the chain validator. |
| `existing-output-refused` | A new call cannot overwrite A's file; bytes are compared unchanged afterwards. |
| `uninitialized-parent-refused` | A genuinely empty `mkEmptyEnvironment 0` cannot produce a snapshot; no output is written. |

There are exactly seven named PASS markers followed by
`SNAPSHOT_CHECKS_COMPLETE conditionalFixtureOnly=true protectedCatalog=false
basisAdoption=false publicDeployment=false`. A missing marker, exception or
nonzero exit is failure, not partial acceptance.

The test fixture copies ten explicitly selected Eq/Quot/True kernel records from
the owner-selected pinned Init into a tiny local test module. It is prominently
**conditional test trust**, not the production fixed basis, not a network warrant,
and not evidence that arbitrary compiled files are acceptable. It keeps the
snapshot implementation discriminator cheap without rerunning the separate
456-unit basis campaign. Production basis construction remains tied to the real
selected `BootstrapProbe.receiveSeed` result under the protected profile.

## Reuse exact compiled core05, no passed-suite repetition

Read-only hash checks confirm current `OriginalExpr`, `OriginalDecl` and
`CheckedExtension` sources exactly match the source copies that compiled in
`experiments/v5-local-checks/ordinary-library-controls-05`. Reuse those exact
locally generated `.olean` prerequisites:

- OriginalExpr: `435d330a5c3bac37aa7b9bfcdd0a548fc3af0593bf53b6a10645e7cc5001eafd`.
- OriginalDecl: `565821e2a3bbbdd9fd8f912ec69985e3906806cee7c358d9420f6c553f3b82da`.
- CheckedExtension: `9b34b26e6ab1560390b0f8a8ddc32fd5c21107df4e84b6be828cfcbe87372298`.

Root's runner should pin those files and source copies, verify current equality,
compile only LocalSnapshot into a fresh build directory, then run only
LocalSnapshotChecks with the pinned sysroot and a fresh output directory.
Use the new build and exact05 build in the compile/run import path; the tested
restore itself empties its fallback path and consumes explicit artifacts only.
Do not edit the existing run_checks driver or old experiment snapshots merely
to add this lane. A small root-selected adapter is sufficient.

Proposed outer envelope: retain the existing ordinary controls'90 CPU seconds,
180 wall seconds,1536MiB,4 processes and bounded logs; there is no theoretical
reason for a larger grant for these seven small controls. This is a proposal,
not execution permission, a memory benchmark, or an empirical timing claim.
The fixture stores at most three small modules under max4-module/64-name/4MiB
selected import caps. Native output bounds are post-write, so outer controller
output reservation remains required even here.

No cryptographic proof, paid service, network experiment, installed release or
provenance framework is involved. Passing these controls would establish only
the selected snapshot/continuation boundary, not protected catalog integrity,
fresh-process independent basis adoption, useful growth or final v5.

## Runner source review and actual follow-up

The snapshot author independently read root's short runner before execution.
It compiles only LocalSnapshot and runs only the seven new controls, preserving
exact05 source equality and clearing inherited Lean search variables. Two small
recommendations were made: retain timeout partial logs and match exact ordered
marker labels plus the complete suffix instead of merely counting markers.
Root applied both before launch; the actual saved runner SHA-256 is
`a7edb547c855462969fb4b39016a9ef5ea8a989a15b17d34da5eb52ff3a7436f`.
Its path/byte pin trust remains with the selected outer local runner, not an
arbitrary user-supplied path. The actual terminal result is reviewed in
`SNAPSHOT-OUTCOME.md`; no rerun was performed.

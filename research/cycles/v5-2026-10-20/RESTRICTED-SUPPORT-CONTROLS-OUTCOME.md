# Derived-support controls: actual outcome audit

2026-10-21, core_release. **PASS for the selected native changed-boundary
controls and two exact-fixture differentials.** This audit reads retained
evidence only; it launches no runtime and does not redo the adopted build or
source-refinement audit. It does not qualify guest cost, proof production,
useful growth or v5 release.

## Identity and execution binding

Run: `experiments/v5-local-checks/restricted-support-controls-01`.

Independently recomputed SHA-256 pins:

| Artifact | SHA-256 |
|---|---|
| Sibling selection and run-local saved selection | `6f855719615335d5bb88221e90c170a5892d5ded441be0e28e2178a3d687ab35` |
| `RESULT.json` | `b1ebc2538329c08fe67509f5d50ea0ead4ac8a174973506f493d160840a27da0` |
| `command/stdout.txt` | `b9ac046a12a5131d67343596dbee9c48ad0c418fda51c2c20146af1610e6f081` |

All ten selected source files and their ten retained snapshot copies match;
all 24 runtime pins match (18 Python-runtime files and six retained
build/executable/fixture inputs). The eight entries in the adopted build's
source map equal their selected control-source pins. Its actual build authority
is reused from `RESTRICTED-SUPPORT-BUILD-OUTCOME.md`, not reconstructed here.
The selected executable is `restricted-support-build-01/restricted_support_controls.exe`
(`50b8952c5cfef085980075edb9e852150136abbcd2142934ac749216f62b774c`);
the retained fixture hash is
`019219ca4548dafbdaa814c209a4ec087229091750db3f3cf48fcc155269f40a`.

The command record, outer result and selection have the same canonical cwd,
pinned Python invocation with `-I -S -B`, exact selected runner snapshot and
limits. The runner invokes only that native executable on the retained fixture.
The unchanged outer runner checks selected runtime pins before and after use.
No compiler/SDK dependency-tree campaign was repeated.

## Actual contract outcome

The raw native JSON has schema `DMKN_RC_SUPPORT_CONTROLS_V1`, status `PASS`,
30 executed entries and no errors. I mechanically compared its complete ordered
case-name sequence with all `suite.check`/`suite.negative` call names in the
pinned snapshot: exact equality, not merely a matching count. All entries are
`PASS`. The complete ordered expected-refusal sequence also equals the 12
`suite.negative` names, and each corresponding actual entry contains its refusal.

The cases cover derived support and charging, malformed IDs, capture-sensitive
open/close, closed-subtree identity, local-node identity rather than serial
number, atomic local types, depth-128 acceptance/depth-129 refusal, work
exhaustion/no partial metadata, nonlocal close refusal and preserved rejection
of an unauthenticated constant. Actual selected observations include open work
2 and close work 3 on height-32 closed trees; interval false positives still
traverse (work 8). These are charged native mechanism counts.

The last two cases call both retained baseline and fresh support checkers on
the same frame. Their successful assertions compare exact encoded journal
bytes, ordered pending-parent journal bytes, expected adopted journal digest,
and expression/level/address census. They do not compare only module names.

| Retained fixture | Journal SHA-256 | Rank / parents | Expression / level / address census | Baseline work | Support work | Removed |
|---|---|---|---|---:|---:|---:|
| First | `0ba261cd27c816223aa56bc6cbe217e67f48264b8d1c707326095492620a1657` | 1 / 1 | 283 / 30 / 4 | 10972 | 9707 | 1265 |
| Second | `dce99babfd2e4e579c2981e6461e4b80c2f794da53b0959eb7494ee1f7c82d86` | 2 / 1 | 349 / 30 / 4 | 13055 | 10927 | 2128 |

The corresponding ModuleIDs are
`ad0cc7c499ec6ca71cd211733c3f566f417b4d86a6064292510b927c4eb122c3`
and `38fbe7771b5ec333bde219631bfb9d6c0a75193f51695723abd41f8b5cfe6dc8`.
Both work differences independently recompute correctly. Metadata overhead is
included in the support counters; counters are not VM rows or CPU predictions.

## Closure, cost and conclusion

Outer status is `COMMAND_EXITED_ZERO_AND_CLOSED`: child exit 0, direct child
reaped, Job closed, no cleanup errors or termination request, final active 0,
terminated 0, cumulative processes 3. Logs are stdout 4073 bytes / stderr 0.
Worker Job CPU is 0.1875 s; separately reported wrapper CPU is 0.234375 s;
known total is **0.421875 s**, without nested double counting. Total wall is
1.4570977999828756 s, and peak Job private commit is 17747968 bytes. Selected
limits remain 30 CPU s / 60 wall s / 512 MiB / 3 processes / 1 MiB per log.

Actual flags are `crypto_produced=false`, `proof_calls=0`, `guest_calls=0` and
`global_growth_claim=false`. The native refinement discriminator passes. The
original failed guest economic screen remains unchanged; these results alone
neither meet its fixed row/CPU criteria nor authorize a proof investment.

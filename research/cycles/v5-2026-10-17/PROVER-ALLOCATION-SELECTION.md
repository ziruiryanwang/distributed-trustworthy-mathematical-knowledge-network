# Source selection: prover allocation-unit refinement

2026-10-17. Root read SMALL-LAYOUT-FEASIBILITY appendix and the retained
PROVER-MEMORY-REVIEW. Full v5 stays active; no proof/build runtime selected.

## Decision and expected marginal payoff

Select the narrow host-side Rust byte-to-word allocation correction for source
implementation and an exact build recipe. Every po18 segment requests 459 MiB
less auxiliary vector payload. This is a structural resource saving, not a
measured working-set reduction, peak upper bound or growth claim. Preserve the
guest A, checker I, circuit, policy, verifier, completed capsule and all receipts.
No po19 attempt is justified under4GiB; the C++-only obstruction remains.

Do not edit the retained SDK or any used artifact. The new output is an explicit
patch/preparation artifact under `software/v5/prover_memory`, with exact original
source pin, typed word-size conversion, divisibility and checked multiplication.
The accessible zeroed prefix, all trace writes, final length and synchronous FFI
input must remain identical; capacity is not part of the mathematical witness.
Independent safety review is mandatory before applying/building this successor.

## Ownership and bounded source scope

- `memo_independent_review`: fresh `software/v5/prover_memory/preflight.patch`,
  `SOURCE.json` and `BUILD-RECIPE.md`. Derive the minimal exact offline compiler
  graph from retained commands/artifacts: circuit, zkvm, module relation,
  aggregate relation, stage host. Identify actual metadata/dependency/link
  adjustments and all retained inputs; do not promise a five-command Cargo build.
  No new compiler runner or execution until root reviews the recipe.
- `v5_growth_decision`: independent access/FFI/memory/build-identity challenge;
  concise audit in this checkpoint. No duplicate test campaign.
- Root: source adoption, eventual finite build/proof selection and Git.

All paths use `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Save source status here or in the three assigned artifacts, not new repeated
theory documents. No network/download, SDK mutation, process termination,
memory-cap increase, previous-layout replay or automatic proof funding.

The old stage-build adoption grammar asserts no backend/relation rebuilds;
therefore a new backend cannot be smuggled into that record. The recipe must
identify an explicit successor adoption seam, preferably compatible with the
generic lifecycle owner now being implemented, before any build investment.
Hardware capacity remains a separate operational prerequisite. A user has been
asked optionally to free memory; useful source work continues meanwhile.

# Restricted guest03: actual four-crate build audit

Disposition: **PASS for the exact selected four-crate build**, not guest
execution, image assembly, proof, mathematical admission or release. Root ran
the operation once (session70321). The reviewer checked saved evidence and
current selected bytes; no runtime or campaign was repeated.

Run: `experiments/v5-local-checks/restricted-guest-build-03`.

| Record | SHA-256 |
|---|---|
| Original and saved selection | `d110cb21351b2f07461986d971533a895011ab0da695e07c6b62175e7de85bf3` |
| `RESULT.json` | `44f808cdd24c2707d114675bf77a4126a805865eaae825666db0c9403e354273` |
| Guest ELF,623,848 bytes | `58250728be048d3badcb4db80cc162ea17b16044b927835e0d59ddf25a260840` |
| Link map,617,778 bytes | `524598f41a8b8353768b2315a308990f835b59d730d563472a232967b9b27f77` |

## Actual changed-boundary checks

- Rehashed all21 original selected production files and all21 fresh snapshot
  files. Snapshot file count and both source-map projections agree exactly with
  selection. Rehashed both used adapters and checked their source/input-map
  bindings. Their reviewed bytes remain build03`847589a3…` and
  recipes03`e51b7b02…`.
- Rehashed the two copied Nanoda artifacts and their distinct adopted-direct-
  build source copies. The fresh retained-project directory contains exactly
  those two files, not an old module binary. Actual module argv uses this
  retained Nanoda; restricted core, aggregate and guest use the newly compiled
  module. The aggregate additionally names the new restricted core.
- Rehashed all three selected native-adoption records and checked agreement
  between selection and RESULT. Original failed-operation status remains
  `FAIL_FINALIZATION`; the distinct retained Nanoda adoption is recorded.
- Checked all four actual command records against saved recipes and each
  phase's `command.json`. Order is module, restricted core, aggregate, guest.
  Every command completed with exit0, no cleanup errors and no active or
  limit-terminated processes. Actual argv preserves the reviewed fresh source,
  output and dependency edges. Four compiler launches include exactly one
  module compile.
- Rehashed all seven outputs (three rlib/rmeta pairs and guest ELF), with exact
  output paths. Rehashed link map; `ARTIFACT.json` equals RESULT's artifact and
  binds the same ELF output. Rehashed all eight logs. All stdout logs and the
  last three stderr logs are empty; module stderr is1,171 bytes, SHA-256
  `a27839b9525d7e0ab8174a7148eb4f601dc8d7934c58ad3ec4791c4ba946693e`.
- Original/saved selection raw hashes agree. Attempt binds the exact RESULT
  and `PASS_RC_GUEST_FOUR_CRATE_COMPILES_ONLY`. The phase Job report is closed,
  has no cleanup errors and agrees with RESULT's cumulative statistics.
  No finalization-failure override exists for this new run.

The selected builder rehashed the236-library view and26 compiler inputs before
and after use. This audit did not duplicate those unchanged bulk reads. Source
closure remains the declared static closure, not a new dep-info qualification.
The source/predecessor rationale is already in
`RESTRICTED-GUEST-BUILD03-REVIEW.md` (`81d8dd27…`) and is not reopened here.

## Cost and closure

| Command | Inclusive worker CPU seconds |
|---|---:|
| Original module |4.359375|
| Restricted core |1.796875|
| Restricted aggregate |0.90625|
| Guest |7.453125|
| Total worker Job |14.515625|

Disjoint controller CPU is4.296875 seconds: **18.8125 known CPU-seconds** total.
Wrapper wall is16.515248300042003 seconds. The final report/exit tail is excluded
as declared by the builder. Command costs are components of the worker total,
not amounts to add again. Final Job: nine total processes, zero active, zero
limit-terminated; peak private commit326,934,528 bytes. Sampled/final fresh
output census is15,465,336 bytes and77 entries, within selected limits.

No checker/dependency/Cargo rebuild, graph command, guest execution, image
assembly, proof or network call occurred. The one extra small module compile
resolved the unsupported intermediate-artifact dependency at measured modest
cost; this is preparation evidence, not a cryptographic-runtime speedup or a
growth-benefit result. Root may separately select assembly of these exact
outputs after adopting this audit. All used bytes and evidence stay frozen.

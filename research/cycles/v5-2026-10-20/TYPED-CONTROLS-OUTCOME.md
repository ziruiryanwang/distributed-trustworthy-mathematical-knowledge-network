# Typed-row controls: saved-outcome audit

`core_search`, 2026-10-20. **Recommend ADOPT the finite changed-boundary PASS.**
No discrepancy found between the selected invocation, actual logs, compiled
assertions and saved bindings. This audit executed no tests and changed no
used source/evidence. It does not adopt a speedup, certificate or final v5.

## Exact evidence and containment

Run: `experiments/v5-local-checks/typed-rows-controls-01`.

| Evidence | SHA-256 |
|---|---|
| Original and saved selection | `4c648a97e777e0c2bcdf547f80107fb9bcdcea8e7a265c07874fe7c6ce361700` |
| Outer `RESULT.json` | `bbdceb54b828f79c017481da542d4a2834763932b3c07da4fab544c34dd41b72` |
| `evidence/result.json` | `daeb9f2f242ef1a027d54c1b16a330b1a4e0e63e6dce0d797eeb88bc8084c71e` |
| `evidence/stdout.txt` | `81e239c87a1da367e963be9fe77a6994b57ce21ed0331c6d090dd30affde3221` |
| `evidence/stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Outer status is `COMMAND_EXITED_ZERO_AND_CLOSED`, direct child exit 0/reaped,
zero remaining active processes, no forced termination and no cleanup errors.
The exact command runs the selected wrapper and binary with eight expected
tests, canonical cwd and the selected 40 CPU / 90 wall / 512 MiB / three-process
envelope. Final Job CPU is 0.375 seconds; separate wrapper CPU is 0.328125,
giving **0.703125 known CPU seconds**. Recorded total wall is **1.6626333
seconds**. These are this control run's costs, not comparative speedup data.

Read-only rehashing found no mismatch in all 24 runtime/input pins, both
selected current/snapshot sources, or all 39 source-snapshot length/digest
entries from the adopted build. The original and saved selection are identical.
The actual binary is `83c27079...` from build02/result `add627e4...`; its binding
was already reviewed in `TYPED-CONTROLS-SELECTION-REVIEW.md` and the independent
build audit. All three mandatory fixture digests remain exact. They are required
environment reads inside assertions, not optional skipped paths.

## What actually passed

Raw Rust output has eight distinct `ok` lines and exactly `8 passed; 0 failed;
0 ignored; 0 measured; 0 filtered out`. The wrapper report and outer stdout
agree. I read the actual compiled `controls.rs` and `controls_root.rs` snapshots.

| Control | Consequential assertion exercised |
|---|---|
| Fourteen constructors | All selected tags map to exactly equal private native syntax; logical node/depth counts match; all binder styles, target `usize` maximum and `nondep=true` syntax are included. |
| Generic metadata/unreached semantics | Declaration metadata remains a generic Value; a 257-universe syntax list is not prematurely rejected; unrelated malformed semantic fields remain unextracted syntax. |
| Strict/raw/width boundaries | Decoded duplicates, signed/noninteger numbers, invalid Unicode/UTF-8, truncation and trailing data refuse; unsupported widths/shapes select literal legacy parsing without coercion. |
| Recursion/duplicate parity | Selected near-limit nested depths have the same parser outcome and successful counts; escaped-equivalent keys refuse. |
| Aggregate charge ordering | Five resource axes exercise exact-bound, over-bound and overflow starts; old/new success/error and partially updated census agree, including malformed record cases. |
| Dispatch/semantic refusals | Unsupported positional/extra/unknown forms select a legacy token; typed schema/foundation failures retain the actual old first error. |
| Real retained module pair | Both selected witnesses use the typed path (930 and 583 typed rows); actual legacy and new conditional checkers both succeed with identical encoded journals and ordered parent journals. Combined census is `[2364,22,23,3,29858,28]`. |
| Real retained aggregate | Actual new aggregate checking matches the pinned previously saved header, ordered assumption claims, member journals, census, edge count and wire count; admission remains false. |

## Claim boundary and recommendation

This supplies finite executable evidence for the representation refinement and
its integration with real conditional checking. The actual legacy module path
is called for the two module positives; the aggregate comparison deliberately
uses the pinned prior oracle rather than recompiling/repeating the old graph.

The semantic-refusal test compares outcomes, not an instrumented retry count.
The no-semantic-fallback claim also relies on the reviewed `Prepared` dispatch
source, whose legacy branch is selected before checking. The controls are not
an exhaustive equivalence proof, a malicious-mathematics campaign or validation
on the zkVM's different target width. In particular they do not measure guest
cycles, producer cost, receipt soundness or useful knowledge growth. No genuine
receipt was produced or accepted, and no product/guest image was changed by
these tests.

Adopt this exact scoped PASS and preserve its inputs/results. No test repetition
is warranted by this audit. Any further work should address the next actual
decision, not expand this passing control into a release claim.

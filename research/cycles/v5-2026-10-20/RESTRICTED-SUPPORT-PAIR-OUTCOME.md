# Support guest: actual fixed investment-screen outcome

2026-10-21, core_release. **Valid execution; investment screen FAILS.** Both
exact-target arms succeed, but support uses 85.106383% of general padded rows,
exceeding the fixed 75% ceiling. The other two gates pass. This audit confirms
the failure; it does not weaken the gate or authorize another RC optimization,
timing retry, proof investment or release claim.

Run: `experiments/v5-local-checks/restricted-support-matched-execution-01`.

## Exact evidence and endpoints

Independently checked SHA-256 identities:

| Record | SHA-256 |
|---|---|
| Selection, including saved copy | `83c64d369149cdc1e2fc840925b215a54ee094ea778810b29e96fb1b543b9235` |
| Configuration, including saved copy | `6afff33289b12bc8d11cd172c50cdc823d1612ee0eac8602d2617ef233687bf4` |
| Inner pair RESULT | `07e8840f423f322dda398deb7c83bd9b1eb975935f7547be26ec0c2708144451` |
| Outer RESULT | `a05b2a58bbb3d88eeffa43858e4ad02749b35e904c37e0b4ee5081d460ee6209` |

All selected canonical/snapshot source and runtime hashes match. The actual
fixture and retained receipt match the selected pins. The target journal hashes
to `0ba261cd27c816223aa56bc6cbe217e67f48264b8d1c707326095492620a1657`,
with ModuleID `ad0cc7c499ec6ca71cd211733c3f566f417b4d86a6064292510b927c4eb122c3`.
The exact parent journal hashes to
`22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682`.
Both actual diagnostics bind the same genuine 223594-byte retained base receipt
`850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`.

Actual general image ID is
`9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865`;
support image ID is
`ae765f5bb55fdf2b2d95aa28aa70c741b77142d3b1af4f90c89cc648f5a260bf`.
The latter binds the separately adopted 685992-byte combined image,
SHA-256 `cb32fe6a93c6127b5bc7bd7c86187ec085db8040cbf0e6ecd615bbee1daed66c`.
Actual command arguments, headers, diagnostics and image bytes agree.

Both headers are byte-identical except their image field. Both wire graph
regions are identical; their payloads match the selected original witness
and restricted frame hashes. Header/wire digests, capsule/diagnostic pins and
actual host stdout agree. No fixture, target, parent or mathematical policy was
changed to obtain this comparison. Each arm made one successful guest execution
and zero proof calls. The old native restricted host is used only within this
previously reviewed exact-fixture differential boundary.

## All retained segments and fixed gates

I independently hashed and checked all **66 retained segment files**, their
ordered indexes, exact directory counts, lengths, po2 bounds and reported
instruction/row/padding/byte totals. SDK row counts already include padding.

| Measure | General | Support |
|---|---:|---:|
| Padded rows | 9240576 | 7864320 |
| Nonpadding rows | 8367627 | 7103043 |
| Padding rows | 872949 | 761277 |
| Segments | 36: 35 at po18, 1 at po16 | 30 at po18 |
| Retained segment bytes | 6803397 | 5075892 |
| Host Job CPU seconds | 0.828125 | 0.640625 |
| Arm-controller CPU seconds | 0.5625 | 0.71875 |
| Standalone known CPU, full shared preparation included | 2.078125 | 2.046875 |

The exact row inequality is `4 * 7864320 > 3 * 9240576`: **FAIL**.
Measured row saving is 14.893617%, not the required 25%.
Thirty segments at po18 satisfy the 64-segment bound. The measured full-CPU
nonregression gate passes; its small difference is one paired observation,
not statistical timing evidence.

## Accounting and closure

Shared preparation/setup/final binding/bookkeeping is 0.6875 CPU seconds,
charged fully to each standalone arm and once to the pair. Controller total is
1.96875 s; nested host Jobs total 1.46875 s; inner known pair CPU is 3.4375 s.
The independently enclosing Job is 3.515625 s and separate outer wrapper is
0.34375 s: **3.859375 s known total**. Nested totals and supervision are not
added again. Final serialization/startup/exit tails are captured by the outer
scope, subject to the existing disclosed measurement boundary. Build/assembly
costs remain separate, not silently claimed amortized.

Both host commands exit 0, with empty stderr, reaped children, closed Jobs,
zero active/terminated processes and no cleanup errors. Outer exit 1 is the
intended investment-screen failure: its child is reaped, Job closed, active and
terminated counts zero, cleanup errors empty, no forced termination. Total
outer wall is 4.129904100205749 seconds. Pair errors are empty; proof/admission,
full-cost-growth and full-release flags remain false.

**Disposition:** retain the successful bounded refinement evidence and this
failed fixed investment screen unchanged. End the selected RC shortcut
investment. Continue higher-payoff existing-product integration; do not infer
an absent cache from an older installed source map.

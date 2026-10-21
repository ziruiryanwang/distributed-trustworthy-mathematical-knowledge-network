# Restricted/general matched execution: failed investment screen

Disposition: **both exact-target executions pass; the prospective restricted-
checker investment screen fails.** This is a valid negative result, not a
successful optimization. Root executed one fixed-order pair (general then
restricted). No timing retry, threshold relaxation, proof or runtime rerun was
performed by this audit.

Run: `experiments/v5-local-checks/restricted-matched-execution-01`.

| Record | SHA-256 |
|---|---|
| Inner `pair/RESULT.json` | `c1c895edb4536b86050643a215a08d3c4ec6184cde16f2a379433850b4ee134f` |
| Outer `RESULT.json` | `edd6113225c2eb99188d2c9fb00b1047f8892b38c536ef79c0be452dae6c4095` |
| Outer saved selection | `28d0513700e9de8fb093ce221c081cda84c42ff99ca14cf18e3f3c3de98b5172` |
| Pair configuration | `abe099bcaf0f17a81636da8876648aab7efe1b2b3a2ae9d7df7b0b2f0bf27fa3` |

These exact retained hashes were independently checked. The previously adopted
source/preparer reviews and launch decision supply the acceptance rules;
historical build and assembly audits were not repeated.

## Same mathematical target and boundary

The fixed fixture is84,727 bytes, SHA-256`019219ca…`. Independently rehashed it
and the single223,594-byte genuine parent receipt
`850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`.
Both actual argv lists use that same receipt path and one boundary assumption.

Recomputed the184-byte target journal's digest:
`0ba261cd27c816223aa56bc6cbe217e67f48264b8d1c707326095492620a1657`.
Its module field is exactly the first adopted native-control target
`ad0cc7c499ec6ca71cd211733c3f566f417b4d86a6064292510b927c4eb122c3`.
The parent journal digest is
`22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682`.
The two derived members are exactly parent and target. This is the matched
original witness/RC frame specified before execution, not a historical timing
substitute or a different target.

Independently rehashed both actual host executables and assembled image files
against their adopted records. General image ID is
`9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865`;
restricted image ID is
`b6b09430b3a9c20a523c00d7cefe3e2312a2ad323ed089f70fe1d0188236a393`.
Image IDs are not file hashes. Actual argv, diagnostics, successful stdout and
derivation agree on these identities and their exact image-file hashes.

Both192-byte output headers agree with the expected header and saved
`header.bin`; the two arms' headers differ only at bytes12..43 containing the
aggregate image ID. Both wire hashes match their derived representation and
actual diagnostic. The diagnostics bind the same parent receipt and journal,
record genuine boundary verification, and report one successful guest execution,
one resolved boundary assumption and zero proof calls. No new receipt or
mathematical admission was produced. The auditor verified the retained bindings,
not the receipt again through another runtime call.

## Complete actual segment accounting

Rehashed **every one of the76 actual serialized segment files**, checked exact
directory counts and consecutive indices, and recomputed diagnostic totals.
Every segment satisfies `rows = 2^po2` with `po2 <= 18`. No prefix or omitted
segment is counted as a successful full execution. Capsule and diagnostic
bytes/hashes also match the inner result.

| Quantity | General | Restricted |
|---|---:|---:|
| Segments |36|40|
| Segment histogram |35 at po18;1 at po16|39 at po18;1 at po17|
| Padded rows |9,240,576|10,354,688|
| Padding subset |872,949|1,024,998|
| Nonpadding rows |8,367,627|9,329,690|
| Instructions |10,202,450|13,661,107|
| Serialized segment bytes |6,803,397|6,331,462|
| Capsule bytes |6,803,834|6,331,899|
| Wire bytes |35,720|7,037|

Padded rows already include padding; padding is not added twice. Per-file sums
match SDK session totals, retained-byte totals and the recorded arm summaries.
This is audited execution-cost evidence from the reviewed host, not a
cryptographic certification of those segments.

## Fixed screen and cost accounting

The launch fixed all three conditions before the run:

| Required condition | Actual outcome |
|---|---|
| Restricted padded rows <=75% of general |**FAIL:**10,354,688 >6,930,432|
| Restricted <=64 segments, each at most po18 |PASS|
| No standalone known-CPU regression |**FAIL:**2.5 >2.171875 seconds|

Restricted padded rows are12.0567% **higher**, not25% lower. Its measured
standalone known CPU is15.1079% higher. This one fixed-order pair is not a
statistically significant CPU comparison; the reported CPU failure remains
the actual prospective gate result. A smaller wire/capsule does not override
the failed execution-cost conditions.

| CPU component, seconds | General | Restricted |
|---|---:|---:|
| Inclusive host Job |0.859375|0.796875|
| Disjoint arm controller interval |0.65625|1.046875|
| Incremental known sum |1.515625|1.84375|
| Full shared preparation charged to standalone arm |0.65625|0.65625|
| Standalone known sum |2.171875|2.5|

The pair's measured adapter CPU is2.359375 seconds, including both arm controller
intervals and shared preparation once. Adding its two disjoint host Jobs gives
4.015625 inner known CPU-seconds before final reporting. Inner supervisor CPU
is already inside the controller intervals and must not be added again.

For the **whole operation**, use the outer inclusive Job4.09375 plus separate
wrapper0.34375: **4.4375 known CPU-seconds**. Do not add the inner pair or nested
host Jobs to that inclusive outer Job. The outer supervisor's0.015625 seconds
is likewise a subset of its wrapper, not an additional charge. Outer wall is
6.640465199947357 seconds. One-time builds, assembly and failed preflights stay
preserved and are outside this execution screen; none is erased by these small
execution numbers.

## Closure and consequence

Both arm Jobs exited0, were closed and directly reaped, with zero active or
limit-terminated processes, no cleanup errors and empty stderr. Saved host Job
records equal those in the inner result. Inner errors are empty. The outer
operation exited1 intentionally for `FAIL_RC_INVESTMENT_SCREEN`, so its
`COMMAND_FAILED` status is correct; it too closed/reaped cleanly with zero
active/terminated processes and no cleanup errors or requested termination.

The candidate is **not cleared as the advantageous certification route** by
this experiment. The result supports changing the mechanism or its theory,
not repeating timing until it passes or starting an expensive proof under a
failed investment gate. It does not prove every possible restricted-checker
design fails, and it does not change the broader v5 goal. All used source,
inputs, outputs, segments, failures and thresholds remain frozen.

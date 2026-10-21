# Typed FIRST execution: actual audit and failed investment screen

2026-10-21, adaptive_audit. **Execution/capsule boundary PASS; fixed128-segment
economic screen FAIL.** Root reported terminal exit0 before this audit. Actual
execution used148 segments. No proof, retry, threshold increase or later stage
is selected. No workload was rerun by this reviewer.

## Exact terminal evidence

Run: `experiments/v5-local-checks/typed-frontier-execution-01`.

| Record | SHA-256 |
|---|---|
| Selection | `a1ba369a538638ce7fb08abcbe1d65c1353f2af0b9138acb27463b42c209e9e0` |
| Configuration | `68f797f51dd5d7563119e251ccf0c1ea091e0a4a27117094a363f464e9f3bca2` |
| Outer `RESULT.json` | `d1db0238bb2de9d927b6fdc922786f87eb6e2252bb28f1ef39ae953b381cb430` |
| Inner `evidence/RESULT.json` | `6cdc0e5addb00dcd021e44784f4e087f8f5e460981a3d2aaa5127e060425aac4` |
| Diagnostic | `54e2a4f6c38e66e95c700dc17d69a2f98b4f6d8ab2f336127ab3ddf58ef9731a` |
|113849-byte wire| `0f9a621cd20d1fca790d0f9c053cf51a4e2eb734f54afce625f9874efe9c0740` |
|192-byte header| `d36dae30d4a343b1601b1133e542aa37f33eb2879c054926d7b32d0d614e9e60` |
| Selection derivation | `bf46d54926d0c7ba54ce919d20fa68293b7ab3f421fcde7f85cd0a37a686ca47` |

All10 current/snapshot source pairs and40 runtime pins independently rehash
exactly. Actual outer argv equals selection after snapshot/output substitution;
limits are unchanged. Saved/outer stdout agrees with the inner result, whose
actual result equals host stdout and diagnostic result. No error is hidden in
the diagnostic. The reviewed selector was used once; no product source changed.

## Same mathematical target, genuinely new image

New wire/header equal the prior selected-frontier wire/header **byte for byte
except bytes12..43**, the explicit aggregate-image field. That field equals the
adopted A′ `9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865`
and differs from the old image. This is exact matched-target evidence, not a
smaller replacement problem or relabeling an old capsule.

The FIRST witness remains113220B/`88b71b8282afc99297bf6564d22616fce6211eed9a9e18afa1cb42a41d1206e1`;
its exact journal is `07734789fd165d5c29667a2925c09b882d346db97a511c75644f2cb4b8ccd0da`.
BASE's journal is `22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682`.
The one genuine boundary receipt remains223594B/
`850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`.
Its actual bytes match the selected parent. The new header, exact target,
parent and member records agree across derivation, wire, host and diagnostic.
SECOND remains omitted downstream work, not claimed completed here.

The command uses the retained generic snapshot host and the actual assembled
image file `0bb44c54`,67108864-cycle cap, po2=18, stats mode, one receipt and120s
timeout. The retained host's checked path computes the image ID, preflights the
exact conditional header, genuinely verifies the boundary receipt, executes the
guest once, requires Halted(0)/exact journal/fully resolved session claim and
materializes all segments. These are execution checks, not a produced SNARK or
mathematical admission credential. No instruction-profile samples were enabled.

## Segment custody and cost

All148 consecutive `0.segment` through `147.segment` files were independently
hashed against the diagnostic; directory membership is exact. Every segment is
po2=18 with262144 rows. Their total27359090B and summed statistics match the
diagnostic. Capsule27359527B independently matches
`8d2bc03ed5b726d05a974542daf36c32b5b4e58ead669c9278291dfbee091cf4`.
Session/capsule binding strings agree across the host result and diagnostic;
this audit did not independently decode the capsule's Rust serialization.

| Cost/statistic | Prior exact FIRST | New typed FIRST |
|---|---:|---:|
| Segments |167|148|
| Padded rows |43778048|38797312|
| Padding rows |4205234|3686730|
| Guest instructions |47430434|44359406|

Thus this exact workload saves19 segments and4980736 padded rows,11.3772455%.
This is neither a measured proof-time reduction nor a general mathematics-growth
claim; it does not establish the complete128-segment proof investment region.

The enclosing Job consumed3.28125 inclusive CPU seconds; wrapper consumed0.3125,
giving known disjoint3.59375s. The0.015625 supervision CPU is already included in
wrapper CPU. Outer recorded wall3.465522500220686s; command wall through cleanup
3.394166700076312s. Peak Job private commit86921216B. All fit180CPU/240wall/
3072MiB/three-active-process limits. Phase milliseconds are wall durations, not
CPU. Outer final report/exit tail is not included in pre-report timing.

Outer completion exits0, reaps its child, closes its Job, has zero active or
terminated processes, no cleanup errors and no termination request. One guest
execution, zero proof calls and zero mathematical admissions. The capsule and
all segments are retained inert evidence, not resumed proof authority.

## Decision

148 exceeds the prospectively fixed128 threshold by20 segments. Preserve the raw
execution PASS and record the **investment-screen failure** separately; neither
rewrite the raw outcome nor call the intended renewal gate passed. The148-run
capsule is not an authorization to increase proof budgets or run a proof prefix.

The implementation produced a real, bounded11.38% padded-row improvement on the
unchanged target but not enough to fund the selected renewal route. Next action
must be a fresh source/theory marginal-payoff decision, with all used inputs and
evidence frozen. No broad RAM campaign, repeated successful execution or altered
target is justified by this outcome. The genuine renewable-certificate and
full-cost useful-growth gates remain open.

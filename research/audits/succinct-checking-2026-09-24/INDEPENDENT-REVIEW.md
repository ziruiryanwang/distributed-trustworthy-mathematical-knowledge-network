# Independent review of current checking cost and succinct-proof inference

2026-09-24. Disposition: **PASS_SELECTED_READ_ONLY_INFERENCE_NO_MATERIAL_CORRECTION**.

This bounded review checked the two existing notes against their selected
retained observations, native-stage receipts, dispatcher events and frozen
source13 source paths. It did not repeat the completed experiments, run Lean,
import product code, query node databases, change source/state, or evaluate a
new proof system. The canonical workspace guard passed.

Reviewed notes:

| File | SHA-256 |
|---|---|
| `COST-EVIDENCE.md` | `d7489c0bc52f41a5cf81447f06b8d1c3d5e451507f872992b6bb2bc51dbfd97c` |
| `TRUST-DESIGN.md` | `353a4a88e0055ce521f456ba89983ffb70c3eb58e53457f314600894e14a6290` |

## Quantitative checks

- All six continuation ordinary-operation CPU/wall rows match their
  `continuation-01/steps/<label>/observation.json` records. Return admission is
  32.96875 inclusive Job CPU / 33.3866865 wall seconds; author submission is
  156.03125 inclusive CPU / 127.2798794 wall seconds. Earlier Rose admission is
  38.078125 CPU / 37.0190451 wall, with 11.109375 nested native CPU seconds.
- Both selected stage receipts match the audited hashes quoted in the cost
  note. Admission's nested Job is 7.609375 CPU seconds; complete stage wall is
  8.3368168 seconds. Peak Job private commit is 2,283,884,544 bytes, or
  2.127033 GiB. It is not proof size or resident working set.
- Submission's five CPU increments are differences of cumulative counters:
  23.609375, 16.875, 14.578125, 4.390625 and 14.0625 seconds. Their sum is
  73.515625; the three Lean steps sum to 52.25. Their recorded start/end
  durations match the note. Summing cumulative counter readings instead would
  double count, but the note does not do so.
- Admission/submission dispatcher events bind the actual request hashes
  `c91b9718...a1c2a7` / `37ba8d02...8aeeaa4` and corresponding public-response
  hashes. Their read counts, canonical-byte totals, cache hits and accumulated
  reader wall times match the note. Source13 `py/checking.py:197` measures
  these reader calls inside the ordinary operation; those measurements must
  not be added to outer totals or treated as unique traffic.
- The unchanged-pipeline CPU thought experiment is correct:
  `32.96875 - 7.609375 = 25.359375`, a 23.0805687% reduction and
  `32.96875 / 25.359375 = 1.3000616` speedup. It is specifically the hypothetical
  removal of the entire nested native Job for free, with all other CPU work
  unchanged. It is not a measured SNARK gain, elapsed-time estimate, bound on
  a redesigned acceptance relation, or bound on safe improvements outside
  that Job. The note states these qualifications.
- Source13 `py/run_stage.py:250` reads Windows Job accounting through
  `QueryInformationJobObject`; line 257 maps `TotalKernelTime / 1e7` to
  `kernel_cpu_seconds`. This is Windows operating-system kernel-mode CPU,
  **not** Lean mathematical-kernel CPU. The note correctly distinguishes them.

The roughly 628 CPU seconds for the larger release workload must not become
“one theorem's verification cost.” The 7.61-second native number also includes
reconstruction, parsing/import/startup, checks and description output; it does
not isolate proof-kernel work. No kernel-versus-overhead attribution beyond
the existing process boundaries is supported.

## Challenge to the active-reuse claim

The trust note's current-source13 claim holds. `AgentClient.lean:213` implements
`checkSource`; line 216 calls `receive` before authoring, and `sourceEnvironment`
installs missing declarations through `checkedAdd` at line 187. In
`AgentReplayCore.lean:373`, `checkedAdd` uses `addDeclCore` with `doCheck := true`.
The Python submission path also performs its candidate and inverse native
replays. Replacing only today's `admit` result with a verified succinct receipt
would leave those later reconstruction/checking operations unchanged and
would not manufacture the context data required by `submit`.

This is a property of the unchanged implementation, not an impossibility
theorem about succinctly certified Lean reuse. A certificate-bound importer,
verified cached environment or suitable native proof-producing certificate
could change the cost and trust boundary. Such a path need not mean modifying
Lean's logical kernel, but it must specify and justify the import/acceptance
authority and exact data bindings. The note already permits a future
certificate-aware import path and does not claim all original proof checking
is intrinsically unavoidable.

An ordinary succinct receipt is not, by itself, a Lean proof term of the
original arbitrary proposition. Encoding a verifier in Lean is likewise
insufficient without the relevant soundness and statement connection.
Definitions, types and reduction interfaces needed for active authoring still
need an available representation, whereas receipt-only readers may have a
different data requirement. The note keeps these consumer cases separate.

No material correction to either reviewed note is required. Their conclusions
remain conditional and unmeasured for an actual succinct implementation; no
new product qualification or architecture selection follows from this review.

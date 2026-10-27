# Native-free frontier controls: independent actual audit

2026-10-26. **PASS for all six selected native-free control groups and clean
closure.** Read saved evidence once; no rerun, product import, native call, state
operation or package mutation by the reviewer.

Run: `experiments/v5-local-checks/demand-frontier-controls01`.

| Evidence | SHA-256 |
|---|---|
| selection.json | `d2829fdc27dcb95b8622d566e0117918c71b51d7903e6932ad069fcb7385af46` |
| RESULT.json | `6bed61e6e09ee475c7051b560a12e5042750ef9094f8fc0b3acd7ef7d73e294f` |
| command/FRONTIER-CONTROLS.json | `ada3e27d95dd832143f537f8df60a2866a36c36ca9cb71964c11638a5cfcaed3` |

All seven actual source snapshot hashes match the independently reviewed
selection. The report's four successor pins and frozen PROFILE identity match
CONTROL-REVIEW.md. Saved stdout equals the saved report apart from its terminal
line ending. All six groups are present exactly once and pass:

- Frozen V2 complete-output and retained-preparation differential.
- Reached V3 cuts and exact acquired target bindings.
- Exact authenticated-context prefix predicate.
- Actual CLI selector scope before state/native work.
- V3 order/shape and fixed or lowered limits.
- Retained V3 binding and tamper refusals.

There are no forbidden attempts, native operations, owner opens or custody opens.
The outer child exits zero; direct child is reaped, Job closed, active processes
zero, cleanup errors empty and no termination requested. stderr is zero bytes;
stdout is 1,170 bytes. Total processes are two under the selected two-active-process
limit. The original selection's 75-wall/45-CPU/768-MiB limits are unchanged.

Measured outer wall time is 12.6325168 seconds, Job CPU 11.640625 seconds, and
separately reported outer-wrapper CPU 0.53125 seconds. The inner 11.9087017 wall
and 11.578125 controller-CPU values are contained observations, not additional
cost. Peak Job private commitment is 55,283,712 bytes.

This supports only the reviewed pure changed-boundary contracts. Synthetic
context dictionaries do not authenticate catalogs, and synthetic declarations
are not checked mathematics. Native demanded-name refusal, rejection of a locally
valid but false-under-real-parent successor, actual package behavior and useful
finite-map refinement still require their own selected evidence. No prior campaign
is renewed and no growth or full-release claim follows.

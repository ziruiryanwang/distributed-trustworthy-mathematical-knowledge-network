# Controls01: preserved harness failure, verified completed prefix

**Overall result remains FAILED.** The helper correctly refused an unwrapped
receive report; the test expected the wrong refusal code. This is not a product
acceptance failure or a complete controls pass. Source and all failed-run bytes
remain frozen. Audit used saved files, standard-library JSON/hashing and source
inspection only; no helper/product/state/runtime replay.

Run: `experiments/v5-local-checks/current-operator-controls01`.

| Evidence | SHA-256 |
|---|---|
| Exact selection | `6f5dac42a20347583d49e36c89058399d3c6cde11003b170f32e1d8e6522439b` |
| Outer RESULT.json | `718a6a58af718cd24a595b4d83f23791e2200333c8859ce5971383fb8840ba56` |
| Used test | `91b40f6273d27a842d2ed4d7496a2dca3de39373b84dea58a3d9a664b55644ab` |
| Stderr | `0cf1703769a3ce5f6499ea6729bbe08f4aa7b1d144b6319d0aa2741ce248e7c3` |

The preserved traceback ends at test line 390: expected `KIT_PARENT_OPERATION`,
actual `KIT_PARENT_SUCCESS`. Saved negative-fixture-057.json is the unwrapped
receive result. It still contains `operation="receive"`, so the operation gate
passes; absent wrapper `ok`/PROFILE fields fail the next gate. The helper's
behavior is correct. No prepared-058 directory was created. The earlier source
review missed this assertion-order mistake; its predicted complete outcome was
not runtime evidence.

Eight actual prepared directories were independently audited:

| Directory suffix | Completed preparation |
|---|---|
| 002 | Current-profile query arguments and exact native-type copy |
| 004 | Receive to contribution, exact source/project/targets/frontier |
| 006 | Contribution parent, empty acquired list, no project |
| 008 / 010 | Receive / contribution publication and access pairs |
| 012 | Historical query to sparse find, original query PROFILE |
| 018 | Historical find/intake to multi-source receive, original PROFILE |
| 026 | Explicit nondefault manifest intake without producer metadata |

All eight receipt input/file hashes and directory censuses match actual bytes.
Their roots, target triples, source/native/project copies, manifest paths/pins
and config fields match the exact selected requests/public reports. No advertised
operation-output or index directory was created. All 65 external pins (62 data
inputs plus three Python runtime files), both source snapshots and their original
source files still match the selection. The failure tree has 29 request files,
ten negative fixtures and eight preparation directories; no controls RESULT exists.

The frozen sequential source plus saved failure point establishes completion of
the first seven groups and 20 counted negative preparations before the failing
assertion. Two layout-refusal checks and overwrite preservation also preceded it.
Group eight's terminal marker was not reached; the final ten approval/target/source
negatives and the suite's final integrity group were not executed. The independent
rehash above does not manufacture their missing suite outcome.

Outer status COMMAND_FAILED, child exit 1, direct child reaped and Job closed;
no cleanup error, termination request or final active/terminated process. Two
total processes; peak private commit 41,938,944 bytes; stdout zero, stderr 3,585
bytes. Wall **1.6278547 seconds**; known CPU **0.65625 seconds** = 0.46875 Job +
0.1875 wrapper, within the selected 90-wall/60-CPU/768-MiB/four-process bounds.

The minimal correction is a fresh remaining-only test: assert the observed
unwrapped-report refusal, run the ten never-executed negative cases and finish
selected-input integrity. Do not replay the eight positives or edit controls01.
Root must select that successor separately after source review. No native/exporter
or mathematical qualification follows from these inert preparations.

## Remaining-only successor source review

**PASS_SOURCE_FOR_SEPARATE_ROOT_SELECTION**, not executed by this reviewer:

| File | Bytes | SHA-256 |
|---|---:|---|
| control_remaining.py | 6,818 | `bd1b4e89799b50ac6dab42e4e3e945c2138267387d9bc6dd2ba76b4143cce78c` |
| REMAINING-PLAN.md | 3,824 | `7b6dacd7e7c7f1617ed0ab02217485f1afc2fe5af110b85ae6f53da7974f1cdf` |

The successor loads the exact frozen test's definitions under a private module
name; it never invokes its main or Controls.execute. It asserts the observed
unwrapped-result shape and correct refusal, then runs only the unexecuted ten
negative variants. Their AST is identical to the frozen tail after replacing
the helper-instance variable `self` with `controls`. No positive preparation or
earlier completed negative is replayed.

Expected successor census: **three groups, zero positives, eleven refusals,
63 selected inputs** (the earlier 62 plus frozen test; 1,115,142 bytes). Frozen
test/helper/adapter/map hashes remain unchanged. The inherited inert boundary,
fresh-output absence checks, selected-input rehash and cooperative limits remain.
Root must bind these 63 inputs and runtime files, snapshot the successor/runner,
and choose a distinct fresh output. Exact launch JSON and actual successor
outcome remain separate gates. Controls01 remains FAILED regardless of them.

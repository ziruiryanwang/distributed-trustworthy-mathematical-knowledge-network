# Existing cost evidence: does context reconstruction justify optimization?

2026-10-28, growth_design_audit. Saved JSON/log inspection only, starting from
[HANDOFF-FIXTURES](../ordinary_incremental_host/HANDOFF-FIXTURES.md). No product
imports, owner/database opens, source tracing, benchmarking or native runs.

**Decision:** controller work is material, but these records do not identify
repeated context metadata reconstruction as its dominant component. They support
considering a small, structurally justified operation-local reuse; they do not
justify a persistent cache, long-lived owner or new profiling campaign by themselves.

## Exact evidence and measured scopes

Let A be `experiments/v5-local-checks/finite-map-refinement-contribution02` and
C be `experiments/v5-local-checks/ordinary-project-extraction-public-01/project`.
Paths are relative to the canonical root. All times below are seconds.

| Existing saved record | Relevant fields |
|---|---|
| A/launcher/child/stdout.txt | `cost.controller_cpu_seconds=4.84375`, `worker_cpu_seconds=5.390625`, `wall_seconds=10.392600999999559` |
| A/contribution/RESULT.json | helper `wall_seconds=9.606735500012292`; `admission.controller_cpu_seconds=2.5`, `worker_cpu_seconds=2.125`; 21 units |
| A/contribution/AUTHORING-SUPERVISION.json | `final_job.cpu_seconds=3.265625`, `wall_seconds_through_cleanup=3.4362808000005316`; four processes |
| C/calls/03-complete/stdout.txt | `cost.controller_cpu_seconds=1.109375`, `worker_cpu_seconds=1.40625`, `wall_seconds=2.3953099003992975` |
| C/completion/RESULT.json | helper `wall_seconds=1.6121895001269877`; `admission.controller_cpu_seconds=0.3125`, `worker_cpu_seconds=1.40625`; three units |
| C/PROJECT-CHECK-RESULT.json | `calls[label=03-complete].supervision.final_job.cpu_seconds=2.578125`, `wall_seconds_through_cleanup=2.4848329997621477` |

The four fixture result/wrapper hashes are in HANDOFF-FIXTURES. Additional pins:
AUTHORING-SUPERVISION `2b7b404326597380c7b1e48642c84865befecad08e90e937ad08aeb9db5a8c88`;
C/PROJECT-CHECK-RESULT `98d23d1397f432f260152a854c5373e8dd049792787ce5e1c30e40966b23a8ef`.

The result files explicitly link the saved native admission directories:

- Contribution: `experiments/v5-local-checks/std-kernel-catalog01/admission-calls/95746899a32b13c1f7667db9c68a61a276a523754cbddc44376c520ea1d407d6`.
  Its `supervision-result.json` records CPU 2.125 and wall 2.039151500008302;
  SHA-256 `2e4b909e2518683574975d5111b7f265a4c7f43d1c27847f24beae7e0c98fbd6`.
- Completion: `experiments/v5-local-checks/ordinary-current-relocated-smoke-01/smoke/catalog/admission-calls/d064cc5737b6761e427609c9a5ac5c9dbe2cfea5fdda68868ae6a9530b403ebb`.
  Its `supervision-result.json` records CPU 1.40625 and wall 1.2747017000801861;
  SHA-256 `9523a7b196c697790c30601c7a493eab482a98c32e05abd29b1874b4e550fdbf`.

The contribution worker total is exactly 3.265625 + 2.125 = 5.390625.
These are inclusive worker Jobs, not isolated Lean kernel CPU. Authoring includes
source/extraction/context construction; admission includes worker startup/imports
and checking. Admission controller CPU is nested within public controller CPU,
not an additional cost. Outer Job CPU likewise already includes nested Jobs.
The existing [operational audit](../ordinary_finite_map_refinement/CONTRIBUTION02-OUTCOME.md)
records whole contribution known CPU 11.015625, including outer overhead.

## What can be bounded, and what cannot be inferred

For a change confined to the measured controller, let M be CPU spent on the
specific repeated metadata work and S its removed CPU on the same input.
Assuming unchanged other work and no added cost, `0 <= S <= M <= controller CPU`.

| Public operation | Controller + worker CPU | Absolute ceiling on removed controller CPU | Optimistic CPU speedup ceiling |
|---|---:|---:|---:|
| Contribution | 10.234375 | 4.84375 (47.33%) | 1.899x |
| Completion | 2.515625 | 1.109375 (44.10%) | 1.789x |

These ceilings assume eliminating **all** controller work and retaining worker
costs, so they are deliberately loose, not predicted improvements. Real metadata
reuse saves only a subset and incurs its own lookup/validation costs. Nested
admission-controller ceilings are 2.5 and 0.3125; remaining controller CPU is
2.34375 and 0.796875. Neither partition identifies context-specific cost.

A/contribution/authoring-supervision/stdout.txt, SHA-256
`36a313e9e5b1652bc64672423ecd0f646c5460eae73f9b922af079e5ef6c5d17`,
records phase names but **no timestamps or CPU deltas**: 11 groups, 581 basis
rows, two targets, 971,618 read bytes, 609 labels, 22 introduced names, nine
checked units, 2,386 scanned nodes and 38,088 encoded nodes. These prove bounded
construction work occurred, not how much time it consumed or how much repeated.
Native worker reports contain artifact sizes/unit counts, without phase timing.

Do not subtract CPU from wall time to infer metadata latency. The saved intervals
include filesystem waits, supervision and worker concurrency. The two examples
also differ in mathematics, version, initial state and workflow: neither is a
matched scaling comparison or evidence for cost as the library tends to infinity.
Completion reuses an already extracted candidate; source extraction is outside
its 2.3953-second public call, not free in the complete creative workflow.

## Consequential next choice

The separate source investigation may establish repeated identical traversal
within one operation. If so, pass an already validated immutable context between
those phases while preserving parent/policy/data binding; this may be justified
by eliminated work without a benchmark campaign. Select it only if its scope and
correctness argument are small relative to the plausible few-second ceiling.
Do not infer that cross-call persistent caching or daemonization pays for its
invalidation/trust complexity. These records supply no reuse frequency or
amortization evidence. If source analysis does not expose a simple duplication,
defer this optimization and address a more direct user-workflow obstacle.

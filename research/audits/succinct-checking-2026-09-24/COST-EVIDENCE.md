# Current local-checking cost: source13 evidence

2026-09-24. Read-only diagnostic by `succinct_cost_evidence`; canonical guard
passed. No Lean execution, build, benchmark, product import, network request,
or change to a frozen source/run. This note interprets existing observations;
it is not a new performance experiment.

## Bottom line

The delivered v2's local admission is currently expensive for the small
tree-counting example: about **33.4 wall seconds**, versus about **127.3 wall
seconds** for the separate author-side source submission. But the evidence
does **not** show that mathematical proof checking dominates admission cost.
Only 7.61 of admission's 32.97 inclusive CPU seconds occur in its nested Lean
job, and that job includes far more than the mathematical kernel.

It would be incorrect to call the roughly 628 CPU seconds across preparation,
the failed first exchange and the continuation “the theorem verification cost.”

## Current measurements, not historical source09 numbers

All paths below are relative to the canonical project root. JSON observations
are single-line files, so their source line is 1. The outer observations are
under `experiments/auxiliary-frontend-01/continuation-01/steps/`.

| Ordinary operation | Observation directory | Inclusive Job CPU seconds | Wall seconds |
|---|---|---:|---:|
| Author B submits revised source | `receiver-count-publishable-submit/observation.json` | 156.031250 | 127.279879 |
| B publishes checked artifact | `receiver-count-publishable-publish/observation.json` | 10.687500 | 11.387001 |
| B exposes immutable view | `receiver-count-publishable-expose/observation.json` | 2.812500 | 3.311450 |
| Receiver A discovers advertisement | `producer-count-publishable-find/observation.json` | 0.546875 | 0.728232 |
| A acquires candidate bytes | `producer-count-publishable-acquire/observation.json` | 6.140625 | 6.664703 |
| A freshly admits candidate | `producer-count-publishable-admit/observation.json` | 32.968750 | 33.386686 |

`producer` is the original A node; it is the receiver of B's return theorem.
CPU includes the ordinary process tree, not only Lean. Wall and CPU are
different dimensions and cannot be added. Above numbers exclude distinct
request-helper calls and the separately supervised service.

The earlier Rose admission in the same source13 exercise measured 38.078125
inclusive CPU / 37.019045 wall seconds. Its nested native job measured
11.109375 CPU seconds. This is a second small-workload observation, not a
repeatability study or a size-scaling curve.

## Admission: what was inside the 33.4 seconds?

The return admission's nested stage receipt is:

`product-local/auxiliary-frontend-integration-13/producer-state/work/31196529e2e7253f3ad2a77a2cc5a5192152174a6fbc1cc249661f116dc67b40/stage-0002/stage.json`

Its SHA-256 was checked during this diagnostic and equals the audited pin:
`7ad40aa78c35de01260a722b504d3e1108a90c419f1da626de5bd00f8673ab18`.

- One `AgentClient.lean --describe` invocation: 7.609375 nested Job CPU
  seconds; 7.938100 elapsed seconds from its recorded start/end timestamps.
  There is one selected-native step, but its Job reports two total processes;
  this is native-step/process-tree timing, not isolated single-process timing.
- Complete stage wall time: 8.336817 seconds, including stage machinery.
- Peak nested Job private commit: 2,283,884,544 bytes, approximately 2.13 GiB.
  This is process-tree private commit, not proof-object size or measured
  resident working set, and not a proven irreducible memory requirement.
- Inclusive ordinary CPU minus nested Job CPU is 25.359375 seconds. This
  remainder is not all known avoidable overhead or all canonical encoding.

The dispatcher event, mapped to the public request through its SHA-256, is:

`product-local/auxiliary-frontend-integration-13/producer-scratch/calls/call-f2ac89059b954c1cb98c2d5914db562b/event.json`

It reports 6 canonical package reads, 1,686,704 aggregate decoded canonical
bytes, 6 package-cache hits, 13.678026 accumulated package-reader wall seconds,
one evidence read and one pipeline child. Package-read time is already inside
the enclosing call; it must not be added to the total. The byte total counts
repeated reads and is not unique network traffic or total retained storage.

Native `--describe` is not a stopwatch around `Lean.Kernel.check`. Source13
`native/AgentClient.lean:68` invokes `receive` at line 71, then performs exact
reference checks, exports type DAGs, optional pretty-printing and JSON output.
`native/AgentReplayCore.lean:373` defines `checkedAdd`, which invokes
`env.addDeclCore ... (doCheck := true)` at line 375. Startup/import/parsing,
environment reconstruction and these output operations are part of the same
native process. There is no source13 profile isolating their proportions.
In the Windows receipts, **`kernel_cpu_seconds` means operating-system kernel
CPU**, not Lean's mathematical kernel CPU.

Under the deliberately restricted hypothetical “remove this entire native
job for free while all other costs remain unchanged,” ordinary CPU would fall
only from 32.968750 to 25.359375 seconds: about 23.1% saved, or 1.30× speedup.
This is an Amdahl-style illustrative ceiling for that unchanged pipeline,
**not** a ceiling for a redesigned succinct-admission architecture and not a
prediction for any actual SNARK implementation.

## Submission: a different, deliberately longer pipeline

The revised source submission's stage receipt is:

`product-local/auxiliary-frontend-integration-13/receiver-state/work/85be6a29be4b1b98614d519ddfa75f39048cf8f9fc8d5a833b550413996866ae/stage-0003/stage.json`

Its SHA-256 was checked and matches:
`b0238593b230ba7f2164b9e5cca92e9be2d9dc6de2b453e8f50fa2379e52063c`.

| Child operation | CPU seconds, difference of cumulative Job counters | Recorded start/end wall seconds |
|---|---:|---:|
| Lean source checking/elaboration/capture | 23.609375 | 24.646576 |
| Python capture → canonical candidate | 16.875000 | 17.614991 |
| Lean freshly describes/replays candidate | 14.578125 | 15.269956 |
| Python inverse reconstruction | 4.390625 | 4.826139 |
| Lean freshly describes/replays inverse | 14.062500 | 14.534136 |
| Nested children total | 73.515625 | 76.891798 |

Complete stage wall is 78.211385 seconds. The three Lean invocations together
use 52.25 CPU seconds; the two Python workers use 21.265625 CPU seconds. The
outer ordinary call additionally includes 82.515625 CPU seconds outside this
nested Job. No component here is cleanly isolated mathematical-kernel time.

The corresponding event is:

`product-local/auxiliary-frontend-integration-13/receiver-scratch/calls/call-019c3dfaf44b41f8b770ee874febf6bd/event.json`

It reports 10 canonical reads, 2,811,641 aggregate canonical bytes, 6 cache
hits, and 25.634884 accumulated package-reader wall seconds. These dispatcher
metrics are not a complete profiler of the child Python workers.

Source13 `py/checking.py:540` defines the five operations; `:552` implements
submission and `:588` onward reauthenticates source capture, canonical plans,
candidate/inverse equality and import before returning a private artifact.
This is not simply “run the theorem proof once.”

## What the present implementation redoes

Source13 `py/checking.py:197` measures `read_package`; `:209` implements a
bounded request-local package cache; `:244` constructs a union and its plan.
`admit` at `:513` revalidates the prior context, selected metadata and union,
then invokes a fresh native description/checking stage at `:530`.
`describe` at `:486` binds the returned result to canonical references.

The observed engineering questions therefore include repeated canonical
processing, fresh environment construction, output/receipt validation and
subprocess startup. These deserve attribution before choosing cryptography
as the primary optimization. Simply removing identity, closure or replay
checks is not a safe optimization; any reuse cache needs exact immutable
inputs, foundation/checker/policy binding and an invalidation rule.

## Limits and recommendation to the parent analysis

- Current evidence is one same-host Windows source13 engineering exercise
  plus its continuation, with small contexts. It does not measure sustained
  throughput, large libraries, concurrent readers, or a mobile/light node.
- The return admission genuinely runs after the serving node's service is
  closed; that validates independence of acceptance from the online peer,
  not cheapness. See `experiments/auxiliary-frontend-01/CONTINUATION-OUTCOME.md:40`.
- Historical source09 package profiles are useful mechanism evidence only.
  Source10 subsequently changed the codec; do not quote source09 timings as
  current source13 throughput. The existing profiler was intentionally not
  rerun; this diagnostic did not duplicate it.
- Succinct verification may remove repeated remote acceptance work if it
  proves the correctly bound relation. These measurements provide no current
  prover cost, verifier cost, break-even reader count, or measured speedup.
- A useful next design comparison is optimized native admission versus a
  succinct full-acceptance relation, retaining enough canonical mathematical
  data for local reuse. Compare complete workflows, not just Lean time against
  a standalone cryptographic verifier microbenchmark.

## Source references

- [Audited continuation outcome](../../../experiments/auxiliary-frontend-01/CONTINUATION-OUTCOME.md)
- [Admission ordinary observation](../../../experiments/auxiliary-frontend-01/continuation-01/steps/producer-count-publishable-admit/observation.json)
- [Submission ordinary observation](../../../experiments/auxiliary-frontend-01/continuation-01/steps/receiver-count-publishable-submit/observation.json)
- [Frozen checking adapter](../../../product-local/auxiliary-frontend-source-13/py/checking.py)
- [Frozen Lean client](../../../product-local/auxiliary-frontend-source-13/native/AgentClient.lean)
- [Frozen Lean replay core](../../../product-local/auxiliary-frontend-source-13/native/AgentReplayCore.lean)
- [Historical baseline and explicit deduplication decision](../../../experiments/package-cost-01/BASELINE.md)

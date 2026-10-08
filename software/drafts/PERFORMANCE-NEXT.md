# Performance diagnosis: vocabulary-01

The 207-byte submission took 100.988 seconds externally. Its measured Lean
children account for 24.547 CPU seconds; the receipts do not justify calling
the whole delay kernel checking. This is one completed run, not a benchmark
distribution. This diagnosis involved only file inspection, with no product
execution, imports, tests, or code changes.

## Measured accounting

Sources: `software/qualification/usefulness-vocabulary-01/submit/OBSERVATION.json`;
under `product-local/usefulness-vocabulary-01`, public call
`scratch/calls/call-2ce91222b4794f30a034a9ffed78846e/{supervisor,event}.json`
and receipt
`state/work/916d97f0c277a333ec62c6d8686d447b5a750561331931aab3cc591b84fa78d6/stage-0001/stage.json`.

| Submission step | Child CPU seconds | Step wall seconds |
| --- | ---: | ---: |
| 0: source check/capture, Lean | 8.609 | 8.949 |
| 1: canonical capture compilation, Python | 19.938 | 21.062 |
| 2: candidate replay/description, Lean | 8.172 | 8.443 |
| 3: inverse export, Python | 3.813 | 4.070 |
| 4: inverse replay/description, Lean | 7.766 | 8.114 |
| Entire stage | 48.297 | 51.279 |

CPU rows are differences between successive cumulative Job counters, not sums
of those counters. Step wall values use recorded start/end timestamps. Stage
wall includes additional preparation/accounting; it is not the sum of step
durations.

The public process tree measured 109.516 CPU seconds and 100.670 wall seconds;
the dispatcher measured 100.472 wall seconds. The 61.219 CPU-second difference
between public-tree and stage-child totals is not attributed to functions or
individual processes. It includes work outside the stage child Job, not merely
the outer wrapper. CPU for that outer wrapper remains unmeasured.

Dispatcher metrics record nine package reads, 2,523,908 canonical bytes, five
package-cache hits, and 25.368 seconds inside `Checker.read_package`. This timer
includes decoding, commitments, closure validation, and planning; it is not an
I/O-only measure. Subtracting stage wall and this parent-side timer from
dispatcher elapsed time leaves 23.825 seconds without phase attribution.
Neither this residual nor the CPU difference is demonstrated avoidable work.

For context, initialization's stage 0 used 8.844 child CPU seconds and 9.452
wall seconds; its public tree used 40.969 CPU seconds. Publication allocated no
stage and used 7.953 public-tree CPU seconds. Their public-call IDs are
`call-8b5f6c45a5a9441c978d8764acb49211` and
`call-8450a205dc68417ba35aa42ee80c5732`.

## Source-grounded candidates, not measured causes

The inspected `checking.py` and `source_codec.py` hashes match this installation's
pinned copies. `Checker.submit` validates/joins the inherited context, then
joins it again after the stage. It reads candidate and inverse packages,
constructs their plans, verifies native exports, and imports/rereads the final
package. The capture worker independently merges inherited packages and builds
its own source compiler.

`source_codec.read_package`, `export_package`, `merge_packages`, and
`reexport_actual` invoke `make_plan`; `reexport_actual` also reconstructs a
store. Each `Store` constructs the foundation; `Store.get` recomputes object
commitments. These are concrete repeated operations worth profiling. Existing
metrics do not show their individual costs, so they do not establish a cache
design, an optimization target, or a likely speedup. Likewise, each Lean step
runs `AgentClient.lean`, but its startup/elaboration/kernel split is unmeasured.

## One smallest decision-changing profile

Run one fresh, bounded diagnostic submission of the same source/context on a
separate diagnostic installation. Collect a dispatcher-only `cProfile` using
process CPU time, retaining the ordinary public/stage receipts and exclusive
and cumulative function totals. This targets the presently unattributed
parent-side work without profiling every process. Label instrumentation
overhead unmeasured; do not compare its wall time as an optimization result.

The decision is whether foundation/commitment/planning computation or another
identified function dominates dispatcher CPU. Optimize only the measured
dominant path next. Preserve source checking, both fresh canonical kernel
replays, inverse binding, and evidence authentication. No new public option,
persistent cache, or weakened check is proposed.

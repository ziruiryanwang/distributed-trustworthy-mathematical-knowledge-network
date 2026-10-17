# Allocation-refined build adoption controls

2026-10-17; author memo_tests_review. Source-only checkpoint under
`LOCAL-RESUMPTION.md`. The full v5 goal remains unchanged.

## Scope and status

Added only `software/v5/prover_memory/test_adoption.py` and this checkpoint.
No test, compiler, native process, proof, cloud operation or Git mutation was
performed. Root owns review, exact source selection and any one bounded run.
The completed generic lifecycle suite is neither imported nor repeated.

The test uses the actual `adoption.adopt_build` and refined producer stage hook,
with inherited record reading, source pin collection, exact source-map/command
derivation, environment matching and serial accounting validation active.
Its support object performs ordinary file/path/byte/hash checks but never
dispatches a process. `subprocess.Popen` is additionally denied during the suite.

Small synthetic fixtures supply fake compiler outputs and accounting. The
descriptor hash constant is temporarily substituted to bind each synthetic
descriptor; all validation logic is unchanged. A separate assertion checks the
real reviewed `SOURCE.json` against the real production anchor and five step
names. Synthetic runtime maps contain 1,071 nonexistent inert paths; their
reported byte count is fictional test data, not downloaded or scanned binaries.
No synthetic result is authority for an actual build or mathematics.

## Exact seven controls

| Control | Changed boundary tested |
|---|---|
| Exact build and both refined stage hooks | Real descriptor anchor/name order; complete synthetic adoption through both `RefinedAggregateProducer` and `RefinedLifecycleProducer`; all required source pins retained. |
| Scope, limits and commands | Reject an unselected memory limit, changed rebuild count, four rather than five command outcomes, or substituted old-library command argument. |
| Sources and empty evidence | Reject omitted derived source, traversal spelling and empty executable source; recheck preserved empty nonexecutable evidence after adoption. |
| Environment and runtime identity | Reject inherited compiler environment or changed retained runtime manifest. |
| Serial accounting | Reject live child state, phase wall-limit overshoot, incorrect CPU sum or summed rather than serial-maximum memory peak. |
| Support-source closure | Reject omitted inherited lifecycle source, duplicate runtime pin, wrong source digest or foreign adoption module origin. No real source file is modified. |
| Delegation and failure cleanup | Snapshot role remains inherited; initialization refusal closes support for both refined owner classes. |

Successful stage-hook controls bypass full producer constructors intentionally;
they do not repeat lifecycle/profile tests. Constructor testing here is limited
to the newly introduced wrapper's cleanup on an injected inherited refusal.

All expected resource limits derive from `adoption.LIMITS`. The prospective
3,072-to-2,048 MiB build limit selection therefore needs no duplicate fixture or
hard-coded update. The mismatch control uses selected memory plus one MiB.

## Exact source dependencies for root selection

The ordinary-source closure is the 24 paths in
`aggregate_lifecycle.producer.SOURCE_MODULES`, plus these five paths:

- `software/v5/prover_memory/__init__.py`
- `software/v5/prover_memory/adoption.py`
- `software/v5/prover_memory/producer.py`
- `software/v5/prover_memory/test_adoption.py`
- `software/v5/prover_memory/SOURCE.json`

The closure's 24 modules are: `aggregate_lifecycle`,
`aggregate_lifecycle.producer`, `aggregate_lifecycle.snapshot`, `aggregate_small`,
`aggregate_small.producer`, `production`, `production.producer`,
`aggregate_claims`, `aggregate_claims.bindings`, `aggregate_claims.input`,
`aggregate_claims.prepare_mixed`, `mixed_claims`, `mixed_claims.packet`, `delta`,
`delta.packet`, `delta.receiver`, `delta_claims`, `delta_claims.claims`,
`delta_claims.receiver`, `admission`, `admission.bindings`, `admission.verifier`,
`modules`, `modules.codec`. A package maps to its `__init__.py`; a dotted module
maps to its corresponding `.py` below `software/v5`.

No import or execution of `build.py`, no SDK source scan, no retained binary
scan, no old test import and no integration fixture are needed. Python/stdlib,
outer supervisor and selected runner remain root-owned runtime dependencies.
Pin the current adapter bytes after root's prospective limit change; do not
reuse pre-change adoption or build identities.

Proposed invocation, for root to instantiate with a fresh selected output:

```text
<selected-python> -I -S -B <canonical-root>/software/v5/prover_memory/test_adoption.py --output <fresh-absolute-experiments-output>
```

The suite requires the canonical cwd, isolated/no-site/no-bytecode/nonoptimized
Python, a fresh output beneath canonical `experiments`, and an existing output
parent. It retains all synthetic fixtures and one machine-readable RESULT with
test/failure/error/skip counts, loaded source pins and the real descriptor pin.
No cleanup deletes evidence. A root-selected run must pass seven tests with zero
failures/errors/skips, under its outer finite envelope, before adoption.

This checkpoint records authored controls, not a passing outcome. The full
five-compile build, corrected proof memory and genuine receipt remain separate
unresolved runtime gates.

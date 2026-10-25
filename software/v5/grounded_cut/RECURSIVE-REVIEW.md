# Independent review: actual recursive grounded-cut workflow

2026-10-24. Reviewer: `current_scale_obstruction`, independent of this workflow's
author. **SOURCE GO for one separately root-selected finite run.** No blocking
source defect was identified. This review does not select execution, assert a
successful native event, establish speedup, or complete deployable v5.

## Exact reviewed inputs

| File | SHA-256 |
|---|---|
| `recursive_workflow.py` | `d8c143bfd345abde7302097977a5e9655071257b66ac9f3cc40b0e4bf1288b1a` |
| `RECURSIVE-GATE-PLAN.md` including source appendix | `266ba4631b68f7833b688348dc35e84d08f0f3b32f521e6c5be869dbe0792e31` |

The entire workflow and plan were read. Relevant actual APIs were traced through
the current `ordinary_admission`, `portable_catalog`, `baseline_bundle`,
`cut_bootstrap`, `cut_controller`, `cut_catalog`, `cut_summary`, `cut_runtime`,
`source_anchor`, `cut_worker`, `GroundedCutDriver.lean` and the conditional Lean
primitive. The pinned ordinary supervisor's final CPU/cleanup report production
was also inspected. This is not a new complete proof of every unchanged component;
their existing adopted source review remains a premise.

No workflow, Lean process, test, owner/custody catalog or package build was run or
opened during this review. No product source, retained evidence or Git state was
changed. Only this Markdown review was created.

## Source findings

### Input identity and independent grounding

The runner pins the base PROFILE, the selected additional support manifest and its
bootstrap before loading them. It requires the exact selected isolated Python,
canonical cwd, fresh output and disjoint input/support/runtime/output roots.
The outer selection must additionally pin the runner snapshot and explicitly
adopt the built support; accepting a hash argument is not initial support trust.

The retained ordinary manifest is pinned to
`680cd98f8d1d31ef251b1e78b1cdae7a60bbe2b733e95193b0fe52cb9855c302`.
Every listed unit is checked for exact byte count/hash, V2 identity and semantics.
The script builds one exact name/export map, validates all imports against that
map or the pinned basis, derives the two targets' complete dependency closure and
performs iterative topological ordering. Duplicate names, missing imports,
self-dependencies and cycles refuse. The fixed expected 36-unit/274177-byte
closure and 34-unit/244463-byte prerequisite counts are assertions on this
derived graph, not fabricated accepted inputs.

Both exact named target units are excluded from fresh native admission. The
script checks that no remaining prerequisite needs either target and asserts
both names absent from the actually admitted native context. This prevents the
recursive test from succeeding by having silently admitted the target laws in
the prerequisite batch.

Provisional summary projection and preparation occur before mathematical state
creation. They establish only supported shape and expected diagnostics. Their
bytes never enter a protected catalog. Real `initialize`, `preflight`/`admit`
and locked `cut_controller.bootstrap` calls establish the actual starting state.
API signatures, `CHECKED`/`READY` statuses, retained-unit fields and their use in
the runner match the selected implementations.

### Real recursive use and persistence

The execution sequence contains exactly six prospective controller invocations:
native basis, native prerequisite admission, native-to-cut derivation, first cut,
second cut and durable intent resolution. Four of these invoke mathematical
workers: two ordinary workers and two cut workers. Derivation and resolution do
not introduce extra mathematical worker events.

The native owner remains genuinely locked during derivation, then native and
custody handles close. Each cut uses the actual protected controller, a fresh call
directory and an independently reopened custody/anchor/cut catalog. There is no
replacement acceptance function, catalog double, saved-report replay or native
fallback. Protected catalog and anchor handles are closed by the called APIs and
the runner's diagnostic reopen; no scratch environment is returned across cuts.

The second event names the first event's newly committed root as parent. Its
committed frontier must contain the first law's exact name, ExportID and summary
identity. The actual saved packet must contain the corresponding signature; the
signature layout's export slot is correctly checked at index 2. Packet concrete
units, signatures and new full theorem are compared with the independently
computed expected byte hashes. These comparisons occur **after** the real
supervised checking/promotion and do not manufacture authority.

The actual `resolve` path reads the saved pre-COMMIT intent, authenticates its
exact proposed record and performs an indexed root lookup. It neither calls a
worker nor commits again. The runner requires the exact committed root and
`reexecuted == False`. This tests normal durable resolution, not simulated reply
loss or arbitrary database crash recovery; those are not claimed here.

### No ancestral theorem-proof input to the cut checks

After successful derivation the prerequisite raw tuple is dropped. After the
first cut its full target input and saved packet objects are dropped. The
retained graph observation contains hashes/counts/frontier identities, not the
old full theorem bodies or provisional summary objects. The next event receives
the second full target and resolves earlier mathematics through protected cut
summaries.

During initial cut reopen, each cut/check/diagnostic reopen, and resolution, the
parent profile hook rejects the ordinary native owner/execution/context/artifact
paths, every custody locator call and any evidence getter for an old unit. The
only permitted evidence getter is the current new theorem's exact custody
readback, and final assertions require exactly one such read per cut. The audit
hook rejects original-bundle opens and native-state opens outside the fixed
anchor identity files/database. The source anchor itself performs fixed metadata
queries, not context recovery or history traversal.

These hooks are **not** complete OS tracing, SQL tracing or a hostile-code
sandbox. They do not establish absence of ancestry by themselves. The approved
controller source separately shows that dependencies are obtained through
`Q.prepare` and protected summary lookups. The approved child invocation passes
only selected support/runtime roots and the new request/report paths; the fixed
Lean driver receives seed, inventory and that packet, not native ancestry
snapshots or the original bundle. That source restriction plus the actual clean
supervised outcome is necessary evidence.

The resulting claim is therefore narrowly: the two **cut-check paths** do not
restore old theorem proof histories. Fixed basis reconstruction and selected
concrete semantic checking remain real work in each cut worker. Native-to-cut
derivation intentionally reads original proofs once. The final 36-unit custody
audit intentionally reads them again outside the cut guard, as separately charged
availability/handoff evidence. Neither read is concealed as ancestry-free
checking or a speedup measurement.

### Finite resource account and failure handling

The proposed inner allowance of 360 wall seconds, 240 CPU seconds and 1280 MiB,
inside an outer 420-wall/300-CPU/1536-MiB Job, is consistent with the runner's
validation and the selected APIs. It is a finite prospective attempt, not a
prediction that the workload will fit. Root must bind those exact values and
the outer process/output/cleanup limits in its separate launch selection.

Each allocated `OperationBudget` derives wall/CPU allowance from the original
deadline and original parent process CPU plus previously observed worker CPU.
Sequential worker trees close before subsequent allocations. The existing
per-worker 24-second wall/one-CPU cleanup reserve remains in `allowance`; a new
operation object does not renew the enclosing budget. Under the actual pinned
supervisor, successful final Job reports include finite CPU observations from
the Job accounting implementation. Unclean or uncertain operations abort rather
than fund another attempt. Missing/unknown failure usage remains the outer Job's
accounting responsibility and is not asserted to be zero.

The enclosing Job must provide hard aggregate containment. Inner Python guards
are cooperative; per-child memory ceilings do not independently cap total
controller-plus-child memory. Likewise sampled spool and acceptance/storage caps
are not a hard filesystem quota. The selected durable databases, summaries,
artifacts, reports and fixed number of calls have explicit finite bounds.

Per-invocation event records retain worker CPU, parent CPU, elapsed time and the
passed logical map-I/O allowance. The three small diagnostic `open_cut` reopens
have their own finite read allowances and are included in original wall/CPU and
outer accounting, but their counters are not in the invocation-event `logical_io`
fields. Accordingly those fields must not be presented as an exhaustive total of
all workflow storage reads. This is a reporting-scope note, not a launch blocker.

Failures preserve partial state and durable intents, record the current phase
and known costs where possible, and rethrow. A failure before output creation may
have only outer-runner evidence. A post-commit reporting failure is explicitly a
possibly committed result, not permission to retry. No branch renews the budget,
changes the theorem, retries checking, erases failure state or substitutes native
success. Final inner success still requires independent outer cleanup/accounting
adoption before interpreting it as an actual completed workflow.

## Disposition

SOURCE GO applies only to this exact prospective two-law workflow and plan, with
adopted immutable support and the separately reviewed finite outer launch. There
is no identified API, graph, authority, recursion or nonrenewing-account defect
requiring a source change before that selection.

A successful run could establish genuine recursive local theorem reuse through
the new cut implementation and durable retained ordinary claims. It would not
establish comparative speedup, cheap cold trust, general mixed-definition cut
support, novel mathematics, sustained useful growth, public-network operation or
final-v5 readiness. No separate custody-return action is authorized by this
review or invoked by the workflow.

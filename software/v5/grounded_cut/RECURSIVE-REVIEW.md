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

## Saved actual outcome audit: recursive01

2026-10-24. **PASS_SELECTED_TWO_RECURSIVE_LOCAL_CUTS_AND_CLEAN_CLOSURE.**
The separately selected single run completed. Its saved result supports actual
recursive local theorem checking without ancestral theorem-proof input on the
two cut-check paths, under the approved local-owner/controller premises. It does
not establish that this implementation is faster or economically preferable.

This audit read saved files and approved source only. It did not open any SQLite
database, call a product API, rerun a worker, renew an allocation, or modify used
source/evidence. The source review above remains the authority-boundary argument;
saved reports by themselves are not proof of protected mathematical acceptance.

### Exact evidence and identity

Run directory: `experiments/v5-local-checks/grounded-cut-recursive01/`.
Selection: `experiments/v5-local-checks/grounded-cut-recursive01-selection.json`,
SHA-256 `697a2346fcd6dd476571bde7dd5365702751fe59b9d32cf5b8d78d4656936a17`.
Both source snapshots match the reviewed hashes above and the selected runner
hash `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.
All twenty selected runtime/support/manifest pins were independently rehashed
with no mismatch. This is explicit-file identity, not toolchain hermeticity.

| Saved evidence | SHA-256 |
|---|---|
| `RESULT.json` | `b688295b7dcd1ac10fed2a9bc78e52abb191337bbbb7ce7d756d0499a9ac3cbc` |
| `workflow/WORKFLOW.json` | `6faceceb2b5e358983d32e692d7364e9e445169892969f4c1c726ee03d9823ac` |
| `workflow/INPUT-GRAPH.json` | `c53d3046a3c4190389dd6c0c1e6f063302c4c955c635392b84fe78b51b83e9ce` |
| `workflow/STATE-IDENTITIES.json` | `fde03ecba0d1948af835fb01d7e81b1579a62db7cf0092e47918a93e6587ee19` |

The exact input manifest accounts for 106 units / 822414 bytes. The selected
closure has 36 units / 274177 bytes; all 36 saved source-unit byte lengths and
hashes independently match the graph pins and manifest. The native admission's
34 retained UnitIDs are exactly that closure minus the two targets. No admitted
prerequisite depends on either excluded target; the second target directly
depends on the first. The native reports identify 456 basis units / 581 names,
then 34 prerequisite units / 45 names. Both target names are absent from both
reports. Their root-derived native module names and parent module agree with
the saved event roots.

### Actual cut packets and durable chain

Both actual packet component-hash lists independently match their prospective
projections. Each `new_unit` is exactly the corresponding original full target
unit, not a substituted statement, and has one theorem descriptor. Every
`concrete_units` entry is non-theorem. Worker report theorem names, full theorem
inventory, signature labels and request IDs agree with those actual packets.

| Cut | New theorem | Concrete units / names | Signatures | Encoded nodes | Kernel calls |
|---|---|---:|---:|---:|---:|
| 1 | `RepairTheory.ClosureBridge.run_extensive` | 13 / 24 | 5 | 2403 | 481 |
| 2 | `RepairTheory.ClosureBridge.same_constraints_same_run` | 20 / 31 | 6 | 3360 | 490 |

Cut 2 includes the exact first ExportID
`f2fa586cebc1ea3a305b51af3ab81ce5ac6eb89775e880bf45c9dd4109bd40c1`
as a signature. The first intent's result summary is
`11983e834ad4f328da8e7ca7c9d853e471f6cfc0488c144782de5564fb4ef809`,
matching the first projection and the second expected frontier. This is actual
reuse of the newly admitted first interface, not a prerequisite-batch admission
of both targets.

All three COMMIT-INTENT root identifiers independently recompute from the exact
canonical record using the implemented root domain. Their parent, request,
UnitID, support, store and epoch bindings agree with the actual event records:

```text
native prerequisites: 981170133ce1cffc1a100c181a56293c725834922f85cb436426822923eb4be6
cut bootstrap:        14a87f12e9bb91d4dd22e09d369faa581a3c2ba64797c93f69578920c660f630
first cut:            46fab40192de561eb2ac93bd830d6a13f01f456e50834e5c176180cd476580a1
second/final cut:     eb68e5b157392f9aa4660e993c5a65db95a2c7386077f6c38ef07bb62bed4525
```

The bootstrap record has no cut parent; each theorem-cut record names the
preceding cut root. The final resolution returns COMMITTED at the exact second
root/request, with `reexecuted: false`. Final stdout agrees. No
`WORKFLOW-FAILURE.json` exists. An intent alone would not prove commit: this
audit additionally relies on the approved runner's successful post-commit
catalog reopens, exact frontier checks and real resolver call. It does not claim
an independent present-time database reread or simulated crash recovery.

The parent path audit reports no violation and exactly one permitted new-unit
custody readback per cut. It also records the restricted anchor identity opens.
Together with the approved child arguments and source, this supports the
ancestral-theorem-proof exclusion described above. It remains Python-level
instrumentation plus source review, not an OS trace or hostile-input sandbox.

### Complete selected-run costs and closure

All six controller events returned. The two native and two cut supervision
records each report zero exit, direct child reaped, Job closed, no termination
request, no cleanup error, zero final active/terminated processes and empty
stderr. Worker CPU observations agree with the workflow event records. Cut
workers receive only approved support/runtime paths and their new request/report
paths, not native ancestry snapshots or the source bundle.

| Event | Wall seconds | Parent CPU seconds | Worker CPU seconds |
|---|---:|---:|---:|
| Native basis | 17.419110 | 0.640625 | 16.203125 |
| Native prerequisites | 3.941605 | 1.703125 | 1.828125 |
| Native-to-cut derivation | 4.291896 | 3.953125 | 0 |
| Cut 1 | 46.204375 | 24.109375 | 20.500000 |
| Cut 2 | 48.732489 | 26.656250 | 20.218750 |
| Resolve second | 1.220976 | 1.171875 | 0 |

The outer RESULT is `COMMAND_EXITED_ZERO_AND_CLOSED`: 129.133710 seconds total
wall, 122.734375 inclusive Job CPU plus 1.312500 wrapper CPU, and 701468672 bytes
peak Job private commit. Eighteen total processes finished with zero active and
zero terminated; cleanup errors are empty. The original outer limits remained
420 wall / 300 CPU / 1536 MiB / eight active processes; inner limits remained
360 wall / 240 CPU / 1280 MiB. Do not add the table's worker CPU to inclusive Job
CPU. Diagnostic reopen work is included in enclosing CPU/wall but omitted from
event logical-I/O counters; those counters are not total physical or logical I/O.

Fixed basis reconstruction remains substantial work in every cut. The large
parent instrumentation cost also prevents these events from serving as a clean
performance comparison. This run gives no speedup, break-even or useful-growth
result. Its soundness-path success is not evidence for further optimization
investment without a separate full-cost decision.

### Custody and claim boundary

After the guarded cut checks, the approved runner separately reread all 36
custody units / 274177 bytes and checked their pins/identities and the exact
object census. This charged availability check intentionally reads old proofs;
it is not cut-check input. The audit did not independently reopen that custody
database. Both saved handoff files independently match their recorded length
and SHA-256, and RETURN-TARGETS contains the exact two graph ExportIDs:

- `CUSTODY-LIMITS.json`: 70 bytes,
  `de8f7b7436d2eacc72c2f095ab5b9255c3457eb78dd7ff49eda84f5c7e88e4d8`.
- `RETURN-TARGETS.json`: 135 bytes,
  `954a7d41f993ba3b6afe14eb9a8f2e4008050d313248b26368f61c0e16022ed6`.

The return adapter was not invoked; these bytes are inert custody handoff, not
transferable warrant. No certificate was produced. Both theorems were retained
existing inputs, not newly invented mathematics. This result does not establish
mixed-definition cut admission, cold recipient trust, unknown-ID discovery,
new concept creation, useful net growth, network operability or final-v5 release.

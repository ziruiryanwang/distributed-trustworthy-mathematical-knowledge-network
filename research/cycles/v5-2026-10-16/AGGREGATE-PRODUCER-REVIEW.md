# Independent aggregate producer source review

**Current disposition: SOURCE REVIEW PASS after the exact placeholder repair.**
Revised producer.py is44253 bytes/SHA
`796eb24619370a30192db6d0f63b914516919e7cae90aee32a1750736331b86b`;
`__init__.py` is unchanged. The final supplement below closes the one original
source blocker. This does not select controls, a build or proof funding.

2026-10-16, `/root/memo_independent_review`. **HOLD: one concrete operability
blocker** in the unexecuted candidate. No product edits, imports, compilation,
tests, proof/build invocation or Git mutation occurred. Canonical guard passes.

## Reviewed scope and identities

| File under `software/v5/aggregate_production/` | Bytes | SHA-256 |
|---|---:|---|
| `producer.py` | 44010 | `f1a7e70e5049e0b71b1e21a490c92208d0c5d42f85babbd339be0521c0091d6b` |
| `__init__.py` | 152 | `0ca27c691b5afe5ad93086251afb3259491f2ebcaf6e2a9b7ff7b209d4489bb2` |

Read the complete selected `../v5-2026-10-12/AGGREGATE-PRODUCER-PLAN.md`,
candidate producer, aggregate API/native stage host, retained loader/graph/
closure helpers, actual supervisor, build-output writer, and actual memo guest
build, image-assembly and capability-screen records. The plan resides in the
October12 cycle, not this cycle. This review checks software contract/operability,
not SDK cryptographic soundness, compiler correspondence or full v5 readiness.

## P1: actual adopted image records cannot pass `_local_outer`

At producer.py lines188–191, `_local_outer` expands only `{snapshot}` before
requiring equality with the actual outer command. The retained image-assembly
selection has this exact argv suffix:

```text
--output {output}\assembly
```

`experiments/v5-local-checks/proof-memo-image-assembly-01/RESULT.json` records
the actual absolute run directory followed by `\assembly`, not the literal
placeholder. The selected runner `tools/Run-V5-Check.py`, line104, expands both:

```python
x.replace("{snapshot}", str(snapshot)).replace("{output}", str(output))
```

Thus constructing the producer with the genuine adopted memo records reaches
`_adopt_image -> _local_outer -> OUTER_EXACT_SELECTED_ARGV` and refuses before
any session can be used. This conclusion follows from comparing retained JSON
values and source; it is **not** a reported executed constructor result.

Required narrow repair: mirror the selected runner's two substitutions in their
actual order, with `output = Path(outer_pin["path"]).parent` and
`snapshot = output / "sources"`. Preserve exact argv equality; do not accept
arbitrary suffixes, remove output checking, or rerun image assembly. No `{root}`
substitution exists in this selected runner. Add a data/pure control using the
retained selection shape so fake all-absolute argv fixtures cannot hide this.

Root and source author were notified during review. Source edits belong to the
author under root selection, not this reviewer. The source above remains held
until the changed boundary is independently checked.

## Other substantive findings: coherent at source level

No additional concrete source blocker was identified in the following paths:

| Boundary | Independent source assessment |
|---|---|
| Legacy reuse | Composition uses the original loader, pin/JSON helpers and graph; it never invokes the incompatible module `_request`, `_checkpoint`, `_run` or `run`. |
| Mathematical profile | H uses `DMKNA002`/2/192 bytes, distinct A/I, exact F/P, member-count and positive-height bounds. WIRE and capsule prefixes match their independent versions. Native host retains complete authoritative relation/receipt checks. |
| Checkpoint framing | Reads up to71 bytes, checks magic/version, binding, bounded kind, index and exact nonempty payload extent. Schema5/module framing refuses. Envelope is explicitly unauthenticated. |
| Native invocation | `stage_argv` matches host indices, receipt order, capsule position and dependency paths exactly; no snapshot, build or implicit next command exists. |
| Stage graph | Unchanged graph has3s+m calls, including finish; finish retains all segment checkpoints plus final prefix/resolve. Missing-plan stops at existing dependencies without deleting required segments. |
| Output contract | Exact field sets and type/equality comparisons distinguish booleans from integers, finish from proof stages, and bind A/H/s/m/capsule/session/output hashes. Nonzero/unclean exits never promote an output. |
| Actual evidence shapes | Apart from the placeholder defect, actual memo guest-build/source-map/artifact and capability inner/outer/configuration/native-command fields match the parser's schemas and relationships. |
| Future host build | `_adopt_build` matches the existing build writer's success shape, command/source snapshot and attempt/result linkage. No stage-host build has been adopted yet; a fabricated PASS cannot replace it. |
| Reservations | Selected per-kind limits, artifact/log/control/tail capacity and worker CPU are checked before launch. Durable reservation precedes `supervise`; native read-set ceiling is checked for the actual dependencies. |
| Failure accounting | Known closure charges measured Job CPU, including failed calls. Unknown closure retains reservation, flags uncertainty, stops the stage loop and closes the owner. Attempted host/prover stages are not confused with reported successful prover calls. |
| Continuation | Complete ordered same-profile/session/allowance/budget/carry history and all prior-success checkpoint pins are mandatory. Charges accumulate. Unknown closure, failed binding or override marker refuses normal continuation. |
| Finalization | Final rebinding/census precedes returned disposition; post-result failure writes an overriding marker and closes the owner. Enclosing caller must still record constructor/preflight/exit/uncertain-finalization outcomes. |

Data-only actual checks used the retained capability outer/inner/COMMAND/
configuration, memo assembly outer/inner/selection, and memo guest-build
RESULT/selection/source-map/ARTIFACT. No old mutable database was opened and no
successful screen, image assembly or proof was repeated.

## Operational conditions for the next root decision

These are explicit limits, not additional mandatory mechanisms:

- **Controls before actual work.** Pure/fake-supervisor controls must cover the
  changed placeholder path plus graph extremes, framing/argv/JSON negatives,
  failed reservations/calls, unknown accounting, finalization overrides and
  complete continuation. They do not certify a real receipt.
- **Bounded history affects scheduling.** Requests allow at most16 prior
  attempts: at most17 ordinary same-allowance attempts. For the retained fresh
  s113/m1 graph there are340 commands; a fixed successful chunk size needs at
  least20 commands to finish in17 attempts. A small pilot prefix can be followed
  by larger explicit chunks because stage_limit is not fixed in the lineage;
  failures also consume attempts. Do not plan hundreds of one-stage resumptions
  or infer end-to-end feasibility from the CPU/output envelope alone.
- **Full funding remains unestablished.** The conservative envelope reports
  worker CPU/output/entries/per-host reads, not a timing prediction or a guarantee
  that controller/wall budgets suffice. Per-stage pin rehashing and preflight are
  real costs. Root must select actual feasible budgets after source/controls.
- **Outer finalization remains necessary.** Saved attempt JSON is not a sealed
  process-completion certificate. Crash, failed marker write, constructor/refusal
  and post-observation tails need the already-required enclosing owner record
  and explicit adoption; never resume merely because a JSON status says PASS.
- API.md still says there is no Python producer. It remains a historical native
  host API document; future public documentation should point to the accepted
  controller profile/request contract. This is not a reason to launch work now.

## Disposition

**Source HOLD pending the narrow placeholder repair and independent recheck.**
The rest of this review supplies focused control requirements, not a proof
allowance or cryptographic/runtime pass. After the repair, root still owns exact
source selection, controlled tests, real stage-host build/adoption and a finite
full-path decision. No automatic retry or cap increase follows this review.

## Independent repair verification

Root separately selected the unused source repair; the original author applied
it. A complete text comparison against the exact original44010-byte source
found only the `_local_outer` delta: output is the outer record's parent,
snapshot is its sources child, and selected argv expands `{snapshot}` followed
by `{output}` before the unchanged exact-list comparison. The adjacent comment
accurately excludes nonexistent `{root}` behavior. No other producer logic
changed; the revised SHA above was read independently.

Read-only PowerShell JSON inspection expanded both actual retained selections
using those exact substitutions, then compared every string case-sensitively:

| Actual retained selection | Arg count | Exact actual outer argv match |
|---|---:|---|
| proof-memo-image-assembly-01 | 11 | Yes |
| frontier-capability-execution-01 | 7 | Yes |

This is **data/source comparison, not executing or importing the producer**.
It establishes that the specific real-record mismatch is repaired without
weakening equality. No new substantive finding arose in the changed boundary.
The original HOLD is retained as history and superseded by **SOURCE REVIEW PASS**.
All controls, actual build/adoption, enclosing-accounting and finite funding
conditions above remain. Full v5 and real aggregate receipt production remain
unestablished by this review.

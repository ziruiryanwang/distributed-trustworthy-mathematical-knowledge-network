# Strict intake parsing cost screen

2026-10-26. `rich_intake_acceptance`. Source-only decision screen for the actual
source-built package at
`experiments/v5-local-checks/current-release-build01/distribution/package`,
PROFILE `7c41db618e17dd9b296df6aa566d2673b72edd859023bcfb7369e11925685541`.
No benchmark, product import, native invocation, state opening, implementation,
cap change or package/security reaudit was performed. Root owns any next source
selection or launch. The canonical workspace guard passed.

## Decision

**Hold the proposed native init/intake until the parsing decision is resolved.**
There is no proved deterministic time refusal: source counts cannot establish
machine throughput. Nevertheless, the unchanged 60-CPU-per-batch/300-CPU-whole
plan is materially underjustified for this instance. Its success path performs
13 complete portable-evidence reads per unit, with approximately 584 MB of
Python lexical scanning and 13 DAG censuses of the 44.9-MB closure. This is much
more work than a single native check of three prepared batches.

The smallest useful next decision is operation-local reuse of parsed exact
bytes inside the existing trusted controller, starting with metadata planning
and admission's own repeated reads. It need not change native semantics,
acceptance, input partition, custody durability or the lexical parser. This
note selects no implementation. Completing inert reconstruction alone does not
clear this independent cost concern.

## Exact successful-path count

Assumptions: fresh independently initialized basis, all 2,651 supplied units
are new, and all three admissions finish. A failed prefix performs less work;
this table does not describe a measured run. File references below are relative
to the selected package.

| Phase and source | Full `portable_evidence.read_evidence` passes per supplied unit | Charged budget |
|---|---:|---|
| `reference/baseline_intake.py:187` -> `_read_batch` -> `baseline_bundle.validate_batch` -> `_measure` | 1 | Whole intake/controller |
| `baseline_intake.py:196` -> `ordinary_admission._plan` | 1 | Whole intake/controller |
| `baseline_intake.py:201`, output-binding projection from `plan.ordered_units` | 1 | Whole intake/controller |
| `baseline_intake.py:231`, `_custody_increment` argument | 1 | Whole intake/controller |
| `baseline_intake.py:292`, second `_read_batch` before creating the operation | 1 | Whole intake/controller |
| `baseline_intake.py:295` -> `owner.preflight` -> `_plan` | 1 | The batch's 60 CPU seconds, also whole controller |
| `ordinary_admission.py:570`, `admit`'s fresh `self.preflight` -> `_plan` | 1 | Same batch and whole controller |
| `ordinary_admission.py:539`, `_stage`'s identity parse | 1 | Same batch and whole controller |
| `_stage` -> `OrdinaryStore.put_evidence` -> `_put` -> `_validate` (`support/transport/ordinary_acquisition.py:167`) | 1 | Same batch and whole controller |
| `ordinary_admission.py:579`, names for native report comparison | 1 | Same batch and whole controller |
| `installation/py/portable_catalog.py:612`, `reserve_extension` | 1 | Same batch and whole controller |
| `ordinary_admission.py:599`, `_execute`'s input identities | 1 | Same batch and whole controller |
| `ordinary_admission.py:606`, `_execute`'s native unit serialization | 1 | Same batch and whole controller |
| **Total** | **13 = 4 planning + 1 reread + 8 admission** | |

`portable_evidence.read_evidence` calls `ordinary_evidence.strict_json`, then
`inspect_unit`, complete import/name census and content hashing. `strict_json`
contains a Python `while i < len(raw)` lexical scanner (including a nested
numeric-token loop), followed by UTF-8 decode, `json.loads`, and a complete
canonical JSON re-encoding/equality check. Thus these are real repeated byte,
tree and DAG traversals, not 13 cheap hash comparisons. The scanner input-byte
figures below count each raw byte once per call; they are not exact Python
instruction counts or memory traffic.

| Batch | Units | Raw bytes per pass | 4 planning scans | 8 scans inside 60 CPU | All 13 scans |
|---|---:|---:|---:|---:|---:|
| 0 | 1024 | 9,997,243 | 39,988,972 | 79,977,944 | 129,964,159 |
| 1 | 1024 | 17,147,916 | 68,591,664 | 137,183,328 | 222,922,908 |
| 2 | 603 | 17,767,684 | 71,070,736 | 142,141,472 | 230,979,892 |
| **Total** | **2651** | **44,912,843** | **179,651,372** | **359,302,744** | **583,866,959** |

That is 34,463 full reader calls and 14,866,670 total-node census visits using
the retained aggregate of 1,143,590 nodes. It excludes additional traversal
inside each census, name-key and symbol hashing, dependency ordering, locator
construction, canonical serialization, metadata/catalog parsing, SQLite
transactions, runtime binding and Lean work. Batch-level node counts were not
retained in the binder summary; none are invented here.

Before the first native extension can start, all three batches undergo planning,
then batch 0 undergoes its reread and eight admission parses: 269,626,559 bytes
of evidence enter strict scanning before that first native event. Native worker
startup reads only its small installation metadata in Python; Lean separately
decodes/checks the generated unit array. It does not add another Python portable
evidence pass. Custody readback uses two exact hashes and byte equality, not a
portable parse. File input is read twice overall (planning and actual batches),
and custody adds its actual write/readback; no claim of only two storage passes
for the entire workflow follows.

## Budget consequence and what the saved timing does establish

The 60-second `OperationBudget` begins after the second `_read_batch` and before
the caller's first `owner.preflight`. All eight admission parses, storage work,
native allowance, native CPU and final controller work consume it. Native CPU
is only the remaining grant after controller preparation, with one CPU second
and 24 wall seconds reserved by the existing allowance calculation. Batch 2's
smaller unit count does not make it cheap: it has the largest byte payload.

The whole intake accounting is stricter than just 300 measured CPU seconds.
The owner first subtracts its startup/controller cost; `IntakeBudget` then
checks live controller CPU **plus** the nonrefundable 60-second grant for each
attempted batch. Three completed attempts leave strictly less than 120 CPU
seconds for all controller work under the proposed public 300 seconds. This
includes the eight admission parses already inside each 60-second grant: the
reservation is conservative and is not refunded when controller work consumes
part of a batch allowance. A full success therefore needs less than roughly
9.23 CPU seconds per full-closure reader-equivalent pass on average, even
before other controller costs. This is a break-even condition, not an observed
throughput estimate. Giving the outer runner 330 seconds does not relax either
inner condition.

Preserved `binding-saved-writer01/binding/summary.json` records one successful
binder at 28.125 CPU seconds, 31.015625 CPU for its entire diagnostic. Its
source performs one bounded writer scan of 38,154,768 bytes, one strict scan
of each freshly constructed portable unit, one unit census, serialization,
names/imports and manifest work. It is not a measurement of one isolated strict
reader pass. The later unchanged-binder materialization failed in `BIND_ONCE`
at its cumulative 70.015625 CPU seconds. No per-phase completed cost was saved
there. These observations demonstrate variation and make a comfortable-fit
claim unwarranted; neither yields a valid linear prediction for the 13-pass
receiver, a rigorous runtime lower bound, or proof of deterministic failure.

Do not spend an initialized owner/native attempt merely to rediscover this
known structural multiplication. The actual native reconstruction and snapshot
costs remain unresolved after any parsing improvement.

## Existing reuse and the smallest safe candidates

Already present, without new code:

- `_plan` stores parsed evidence in its private `units`/`new` maps and reuses it
  for dependency ordering. It then discards those parsed objects and returns
  only immutable raw units and planning metadata.
- `baseline_bundle._measure_parsed` can measure an already parsed value; the
  strict external `validate_batch` route currently invokes `_measure` and does
  not expose a trusted parsed result to its caller.
- `OrdinaryStore._get` validates exact retained content/identity hashes without
  repeating syntax/DAG census. This optimization already covers readback.
- The adopted binder reuses its own just-inspected census during closed local
  construction. That optimization is unavailable to arbitrary received bytes
  and does not justify importing caller-supplied `Evidence` objects as authority.

The narrowest consequential source candidate is a private current-call parsed
map returned by an internal planning helper, while the public `preflight` API
continues to return its present nonauthoritative `Preflight`. Root's proposed
staging is preferable to also changing custody staging's identity parse: it
preserves every existing component boundary initially. Two isolated uses can
remove five of the 13 passes without touching `_stage`, custody/catalog
validation or the lexical parser:

1. In `admit`, build the private parsed map during its mandatory fresh preflight,
   independently recomputed from `plan.raw_units`, then reuse it only for
   collected native names, `_execute`'s identities and serialized units. Keep
   the caller's prior preflight, `admit`'s fresh one, `_stage`'s identity parse,
   custody's own `_validate`, and catalog's own `reserve_extension` parse.
   Admission falls from eight to five parses. Scope: admission internals only;
   public `Preflight` and generic custody/catalog interfaces stay unchanged.
2. Later, in `_plan_all`, reuse the exact parsed map from its own `_plan` call for the
   output-binding and quota projections. Keep `_read_batch`'s initial strict
   validation and `_plan`'s own strict read. Planning falls from four to two
   parses. Scope: the private admission planning helper and the baseline
   controller; no whole-call retention of all raw evidence is required.

Stage 1 alone removes 37.5% of admission's full parse/census calls and 23.1% of
the full path, reducing it from 13 to ten parses (449,128,430 scan-input bytes).
It leaves five passes inside each admission: 49,986,215 / 85,739,580 / 88,838,420
scan-input bytes for the three batches. Both stages together reduce the full
path from 13 to eight parses (359,302,744 bytes), a 38.5% work-count reduction.
These are worthwhile expected savings for a small internal lifetime change,
especially inside the fixed 60-second grants. They do not guarantee runtime
improvement by those percentages or establish that the unchanged limits suffice:
the remaining whole-controller break-even is below approximately 12 seconds
per full-closure reader-equivalent pass after stage 1, or 15 after both, before
other work. Root can select each seam separately with changed-boundary
proof/controls; no broad rewrite or immediate scanner change is needed.

The three eliminated admission reads have no intervening raw-byte or parent
change: they obtain names, identities and unit syntax from the same immutable
`actual.ordered_units` that `admit` just independently parsed. A private map
indexed by the exact raw bytes, with ordered lookup checked against those bytes,
preserves the current grant/report/native comparisons. Returned public plans
must still carry no trusted parsed map. `admit` must never reuse a caller's
earlier parse or skip the current parent/import/conflict checks. Keeping `_stage`
strict initially is a conservative, useful boundary; eliding its own parse is
a separable later decision, not required for this candidate's payoff.

The assurance seam is exact immutable `bytes` plus a private parse produced
during this call under the selected semantic/limit profile. `Evidence` currently
contains a mutable document. A caller-provided cache, mutable public plan field,
identity-only cache, or prior-call parse is insufficient. Internal consumers must
be shown not to mutate or externally expose the reused parsed document; equality
must bind every reused fact to the current raw bytes. Fresh parent/context,
import/conflict checks, custody persistence/readback, live grant binding and
native checking still occur. No metadata projection becomes a warrant.

More aggressive sharing across `_read_batch`, public preflight, catalog and
custody would require wider interfaces and stronger ownership/lifetime arguments;
it is unnecessary for the first candidate. Replacing the Python lexical scanner
has a larger assurance surface (depth, unsigned numeric limits before general
JSON conversion, exact strings/escapes, duplicate keys and canonical bytes).
Prefer eliminating identical work locally first. An optimized scanner would
need a separately justified strict-equivalence argument and focused hostile-input
checks, and would still leave redundant DAG/serialization work if used alone.

This screen supports a source decision before native work. It does not claim
the library has been accepted, that warm authoring works, or that a faster
receiver establishes useful mathematical growth.

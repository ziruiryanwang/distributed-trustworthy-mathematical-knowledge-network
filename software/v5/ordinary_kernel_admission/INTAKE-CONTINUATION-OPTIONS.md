# Strict intake continuation through the existing interface

2026-10-26. Independent source/data analysis by `kernel_package_audit`.

**Recommendation in principle:** retain the current checker and public owner
interface. Select an exact suffix of the original immutable manifest, divide
each of its two remaining original batches into two contiguous, approximately
byte-balanced subbatches, and consider two separately authorized two-batch
invocations. The second invocation must use the actually confirmed root returned
by the first. This note selects no manifest production, status operation, intake,
retry, budget renewal or product change.

The first prerequisite is independent confirmation that the protected owner and
the recorded prefix remain eligible after the failed native event. Diagnostics
and this analysis are not that confirmation. Root owns subsequent selection,
runtime execution and adoption.

## Current boundary

The independently audited `std-kernel-intake01` checked 1,024 units and reported
prefix root
`c3d0f6209f42abdc98a6975a358545b0d61701e849b6ed0a3e69bdc1b7f400f6`.
Its second native event exhausted its 24-second CPU allowance; the whole intake
failed. The prefix is not a completed rich parent. The conservative
`possible_unreported_commit` flag remains true in the saved failure; this review
does not clear it or infer recovery eligibility from the absence of WITHDRAWN.

The original immutable input directory is
`experiments/v5-local-checks/std-reconstruct01/materialized`. Its 468,097-byte
manifest has SHA-256
`1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c`.
Its exact row sequence has the following census:

| Original zero-based interval | Units | Raw portable bytes |
|---|---:|---:|
| `[0,1024)` | 1,024 | 9,997,243 |
| `[1024,2048)` | 1,024 | 17,147,916 |
| `[2048,2651)` | 603 | 17,767,684 |
| Remaining suffix `[1024,2651)` | **1,627** | **34,915,600** |

The largest suffix unit is 970,481 bytes, UnitID
`6b003717c84e9f75d6f94b31818f933abcc07ee3a38a6edd3924913de4e7ea20`,
raw SHA-256
`5a7447d599a7d95f906344ba291d0e3816444a2412db44e9b92bada714994986`.
These figures were computed from the retained manifest only. No raw theorem
trees were reparsed for this analysis. Decimal MB and binary MiB must not be
interchanged: 34,915,600 bytes is about 34.92 MB or 33.30 MiB.

## Why an exact contiguous suffix is legal

The installed public `owner.py` independently accepts `--bundle-directory`,
`--bundle-manifest` and `--bundle-manifest-sha256` (lines 440-446). It requires
the manifest to be an ordinary bounded file with the selected exact hash, but
does not require that file to reside inside the bundle directory. Thus a fresh
derived manifest can point to the unchanged original directory. No theorem
file needs copying or reconstruction.

The installed `reference/baseline_bundle.py` requires precisely the schema,
semantic ID and batches of `{unit_id, raw_sha256, raw_bytes}` entries. The path
of each unit is derived as `units/<unit_id>.json`. A derived manifest must use
the same schema and semantic ID, copy each selected entry exactly, preserve its
order and introduce no duplicate. Whole units, including recursive declaration
groups, remain indivisible. The ordinary strict parser, exact-byte checks,
dependency preflight and native checking still run at their existing boundaries.

`reference/baseline_intake.py:intake` expressly allows any eligible protected
parent root. It obtains the actual context with `owner.catalog.context`, plans
the selected manifest against that context, and checks each actual batch against
the latest returned root. No lineage cursor, saved receipt or invented context
is accepted in place of that owner state.

### Row order has a stronger justification than old batch admissibility

The fact that an entire old batch was admissible would not by itself justify
splitting its rows: a dependency could have appeared later inside that batch.
Here the executed reconstruction gives an independent row-level argument.

The used `ordinary_std_intake/reconstruct.py` and its saved source snapshot both
hash to
`244f1e17b80101961099cddf1bd557a655b3e76adb34894aa32ff14e31151868`.
Its relevant operations are:

1. Line 81 flattens the original manifest batches in their existing row order.
2. Lines 108-109 initialize `available` with exactly the selected 581 fixed-basis
   name bindings.
3. Line 126 pairs the retained writer units with those manifest entries using
   `zip(..., strict=True)`; no UnitID sort or other reordering intervenes.
4. Lines 130-135 inspect the unit's complete external-name census, require every
   external name already in `available`, and construct its exact import bindings
   from that map.
5. Lines 138-146 require the resulting raw length, raw SHA-256 and domain-separated
   UnitID to match the corresponding original manifest entry, then write/read back
   those exact bytes.
6. Only then do lines 150-154 add this unit's output bindings, rejecting any
   duplicate or preexisting output name.

Formally, let `U_i` be the exact unit at original manifest index `i`, `B` the
fixed basis binding map and `Out(U_i)` its exact export bindings. Induction on
the successful reconstruction loop establishes

`Available_i = B union Out(U_0) union ... union Out(U_(i-1))`

with pairwise nonconflicting output names. Every external binding in `U_i` is
looked up in `Available_i` before any binding from `U_i` is inserted. Therefore
every external dependency comes from the fixed basis or a strictly earlier
manifest unit. Internal references within an atomic unit are not separated by
a new batch boundary.

For any contiguous interval `[l,r)`, a parent containing those exact earlier
bindings supplies its external prefix dependencies; the remaining dependencies
are supplied by earlier rows in the same interval. Any sequence of contiguous
intervals therefore preserves this ordering property. This is not an assertion
about arbitrary external manifests. It relies on the inspected used source,
the reviewed reconstruction's successful completion, and exact retained hashes.
The public receiver still checks the current raw inputs and actual context.

`RECONSTRUCT-REVIEW.md` explicitly reviews this one-pass ordering invariant;
`RECONSTRUCT-OUTCOME.md` independently confirms the source/input pins, complete
2,651-unit terminal result and all exact restored bytes. The later intake's
native dependency ordering differing from manifest ordering does not contradict
the argument: multiple valid topological orders can exist. No extra raw
dependency census is necessary to justify this particular repartition.

## Partition comparison

For the global balanced candidates below, each cut was chosen at a whole-unit
boundary nearest the respective cumulative fraction of the suffix byte total.
All intervals are zero-based and half-open in the **original** manifest.

| Candidate | Original intervals | Unit counts | Raw bytes per batch |
|---|---|---|---|
| Three globally balanced batches | `[1024,1806)`, `[1806,2394)`, `[2394,2651)` | 782 / 588 / 257 | 11,538,984 / 11,735,583 / 11,641,033 |
| Four globally balanced batches | `[1024,1650)`, `[1650,2059)`, `[2059,2484)`, `[2484,2651)` | 626 / 409 / 425 / 167 | 8,735,779 / 8,768,648 / 8,678,416 / 8,732,757 |
| **Two halves of each original remaining batch** | `[1024,1644)`, `[1644,2048)`, `[2048,2477)`, `[2477,2651)` | **620 / 404 / 429 / 174** | **8,552,756 / 8,595,160 / 8,899,687 / 8,867,997** |

The last candidate is preferred. Its largest batch is only about 1.5% larger
than the largest globally balanced four-way batch, remains below the successful
first batch's 9,997,243 bytes, and is wholly contained inside one old batch.
The preceding intake completed metadata validation of every original batch.
Each new subbatch therefore inherits the old batch's additive structural bounds
on units, bytes, nodes, names, edges and encoded native-array size. This avoids
relying on byte size alone to bound a cross-boundary combination's structure.
Exact current validation remains mandatory; inheritance does not replace it.

The global three- and four-way candidates are also topologically justified,
but include a batch spanning the old boundary. Their structural ceilings cannot
be inferred solely from their raw byte counts. There is no need to take that
extra reasoning burden to save approximately 131 KB in maximum batch size.

The preferred first invocation would select rows `[1024,2048)` in two batches,
17,147,916 bytes total. Only after its actual outcome is adopted would a second
separately selected invocation choose `[2048,2651)` in two batches,
17,767,684 bytes total, against the first invocation's actual confirmed root.
No second parent root can be invented or populated prospectively.

## Resource reasoning

The installed `CallLimits` default is 60 CPU seconds per whole admission
operation, not 60 seconds exclusively for Lean. `IntakeBudget.operation` creates
that budget before public preflight and `admit` repeats planning/staging before
launching the worker. The worker receives only the remaining allowance. The
public CLI passes the defaults and exposes no per-batch CPU override. Increasing
only an aggregate owner limit would not enlarge the 60-second operation budget.

The actual successful first operation consumed 21.640625 controller CPU seconds
and 24.46875 worker CPU seconds. The failed second operation reached about
34-35 controller CPU seconds before receiving its 24-second native allowance.
The phase/cost analysis is separately owned by `kernel_path_integration`; these
observations support smaller batches but do not establish a universal linear
relationship between byte count and Lean checking work.

Aggregate accounting is intentionally conservative. Every manifest batch,
including a fully reused batch, reserves 60 nonrefundable CPU seconds. The live
check additionally charges controller CPU. If `H` is the aggregate CPU remaining
when `IntakeBudget` starts, the condition is strictly

`controller_CPU + 60 * attempted_batches < H`.

Owner startup occurs before that budget and reduces `H` below the public owner
allocation. The following ceilings consequently overstate the available
controller headroom slightly when the owner allocation is 300 seconds:

| One invocation | Reservations | Controller headroom before startup deduction |
|---|---:|---:|
| Three batches | 180 | Less than 120 CPU seconds |
| Four batches | 240 | Less than 60 CPU seconds |
| Five batches | 300 | None; cannot fit |
| Two batches | 120 | Less than 180 CPU seconds |

The phase analysis estimates roughly 113 controller CPU seconds for all four
suffix batches under the present repeated-read/replanning path. This is a
heuristic cost screen, not a runtime guarantee, but makes one four-batch
300-second invocation a poor candidate. Three larger batches reduce reservation
pressure while moving the individual 60-second operations closer to the observed
failure region. Two two-batch invocations preserve the existing per-operation
limit while giving each sufficient aggregate headroom in the current model.

These are two genuinely new selections with their own allocations, not a reset
or refund of the failed intake's charge. Total authorization and total actual
cost must include both and all preceding failed work. Extra process startup,
context restoration, two additional native snapshots/roots, custody scans and
plan overhead are real costs; no speedup or guaranteed completion is claimed.
The second invocation is conditional on the first's outcome, not automatically
launched. A refusal triggers a fresh decision rather than automatic rebatching.

## State and safety conditions for any later selection

- Determine protected recovery eligibility through the existing separately
  selected owner operation. `status` can mark abandoned RESERVED operations
  INTERRUPTED during owner open; it is not advertised as a read-only shell query.
  A saved diagnostic is not a substitute for that live validation.
- Preserve the failed operation, its reservations, accepted first snapshot,
  partially staged inert custody and all original source/input/evidence bytes.
  No catalog repair, manual DB edit, state migration or deletion is needed.
- Require the actual parent to contain the exact original prefix bindings.
  Existing mathematical acceptance follows protected context validation and
  checked ancestry, never theorem names alone or reconstruction hashes.
- Construct fresh canonical manifests with unchanged schema/semantic ID and exact
  original row entries. Reference the original materialized directory; do not
  rewrite its manifest, units or reconstruction report.
- Keep the existing bundle, native, custody and catalog bounds. The actual intake
  checks current root/operation counts, retained snapshot reservations, name and
  manifest capacities, native plan size, custody additions and spool reservation.
  Extra subbatch roots do not inherit these state-dependent limits automatically.
- Count existing failed-batch custody as stored inert evidence only. It may reduce
  additional logical storage, but never supplies mathematical acceptance. The
  current `admit` implementation still strictly stages and reads back supplied
  bytes even when complete identities are reusable; submitting the full original
  bundle would needlessly repeat prefix work and reserve a reused batch's cap.
- Retain the outer hard supervisor and existing clean-closure rules. This note
  introduces no source-execution privilege, certificate trust mode or exemption
  from fresh native checking for the previously unaccepted suffix.

## Scope and source anchors

The installed files read for this review are under
`experiments/v5-local-checks/kernel-admission-package01/distribution/package`:
`owner.py`, `reference/baseline_bundle.py`, `reference/baseline_intake.py`, and
`installation/py/ordinary_admission.py`.

Supporting fixed records:

| Record | SHA-256 |
|---|---|
| `ordinary_std_intake/RECONSTRUCT-REVIEW.md` | `03e34edfcad985483420acb30eb96a96187a5b6c23dabecb39a435e59496a5b9` |
| `ordinary_std_intake/RECONSTRUCT-OUTCOME.md` | `8a5b0e489ccae568cc9e3de0ab4850918f1ba7b7b5e21c2fb2a305160b947931` |
| `ordinary_kernel_admission/INTAKE-OUTCOME.md` | `dd296ef4753fb42d4d851232695a10a68906e44054cf5a368ceeafcaa05a08ea` |

This review used source reads, retained JSON metadata arithmetic and hashes only.
It imported no product module, opened no database, invoked no owner/status/native
command and created no executable payload, manifest, experiment or deployment.
The only new artifact is this analysis. It supports an economical continuation
decision; it is not acceptance of that continuation or of full deployable v5.

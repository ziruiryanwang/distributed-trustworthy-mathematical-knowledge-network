# Reuse the helper's existing context only for advisory preflight

2026-10-28, operable_scale_decision. Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Source feasibility only; no code edit, product import, owner/database access, native execution, runtime or Git.

## Decision

**GO in principle for the two helper call-site replacements, conditional on
accepting the explicit package/anchor compatibility cost below.** Use existing
`A._plan(context, raw_units, same_limits, budget.check)` for advisory preflight.
Keep `owner.admit` and every admission/catalog/native source byte unchanged.
No context cache, token, immutable-view framework, persistent index or new public
API is necessary. This removes known duplicated work without a profiling campaign;
it does not establish that context work dominates the creative workflow.

## Exact seam and argument

The selected core is `ordinary_parse_reuse/ordinary_admission.py`, not `ordinary_lean/ordinary_admission.py`.
Its public `preflight:530-536` performs
budget/type checks, obtains `catalog.context(parent_root)`, then calls `_plan`.
`_plan:390-392` is already the raw-only convenience wrapper over `_plan_with_parsed`.

- `ordinary_demand_frontier/ordinary_contribution.py:432` obtains `context` for
  request construction and binding; the `warranted` closure keeps it live. At
  `594-596`, replace only the `owner.preflight` call using `bound.raw_units`.
- `ordinary_library_package/completion_api.py:87` obtains the same local context
  for `complete_candidate`; it remains live at the `117-119` preflight call.
  Use `plan.raw_units` and the same current `budget.check`.

Preserve `PreflightLimits(max_units=32,max_bytes=4*MiB,max_nodes=131072,
max_names=4096,max_edges=32768)`, READY/missing diagnostics, parent argument,
current operation budget and every subsequent statement. Each helper already
requires the exact OrdinaryAdmission/OperationBudget types and original deadline.
The existing planner checks its budget before parsing and during bounded work.
An optional `context["local_root"] == parent_root` assertion catches programmer mismatch; introduce no token.

On stable owner-controlled state, the two context dictionaries have identical
semantic/root/binding content. `_plan_with_parsed` only reads that content, parses
the same raw units and returns the same raw-only Preflight fields. It does not
mutate the original map or hand parsed trees to callers. The helper has not
committed another extension between initial context acquisition and preflight.
The held owner lock and immutable-owner-path premise remain unchanged.

The initial dict is not thereby promoted to acceptance authority. At
`ordinary_admission.py:577-610`, `admit` checks the plan type/parent, claims the
same budget, freshly reads the real parent and independently replans **only
plan.raw_units** under current default limits. It ignores advisory status/order/
missing/reused assertions. This happens before custody staging; a new extension
then gets another fresh execution context and fresh reservation context, followed
by the unchanged actual native event and protected commit. All three stay intact.

If state changes despite the supported storage premise, an old view can produce
a stale refusal or proposal; it cannot authorize admission. A stale READY reaches
fresh validation, where withdrawal, invalid state, conflicting imports/names or
missing dependencies refuse. Failure may move from PREFLIGHT to ADMISSION and
claim the operation budget earlier; original CPU/time/failure accounting remains.
Do not promise identical failure phase or identical behavior under local tampering.

## Source-proven cost and compatibility

One full selected-chain metadata reconstruction disappears on each reached helper
preflight. The existing initial map was already retained; no new map, serialized
snapshot or lifetime extension is required. Raw evidence parsing/planning is
unchanged. In the ordinary new-admission path this changes five context calls to
four, not five to one. Artifact hashes were already cached within the process;
no saved native replay or repeated snapshot-hashing benefit follows. A context's
lineage/name/plan work is removed with no replacement traversal. Numerical end-to-end
speedup remains unknown; no-change retains that cost but avoids deployment work.

Changing only these `authoring/py` helpers changes PROFILE payload pins. It does
not change INSTALLATION.json or its core implementation I: `profile.py:202-239`
opens the separate installation, and core support identities come from its files.
Existing native catalog roots therefore need no re-admission merely for this edit.
The package source map, PROFILE and operator compatibility map/selector pins must
be updated honestly; preserve all used packages and unchanged native artifacts.

**Module-anchor caveat:** `ordinary_exact_module/module_export.py:29-62` includes
the exact contribution helper as support role `contribution`; it excludes completion.
A changed contribution file changes anchor `support_id`. Existing anchor records
then fail `_record`'s support equality (`anchor_store.py:366-372`) under that new
package. Their ordinary owner roots remain valid. Keep using the preserved old
package for those anchors, or separately price a new checked module realization;
do not weaken the support check, relabel anchors or rebuild them automatically.
Completion-only reuse does not incur this particular anchor-support change.

Host descriptors also pin PROFILE. Existing hosts should retain their approved
package; a helper refresh does not authorize rewriting their descriptor or migrating
state. Prefer folding this small optimization into a needed package refresh.
If preserving same-package old-anchor use is required, choose completion-only or
no change rather than expand this work into compatibility/migration machinery.

## Small validation and stop condition

Source review plus focused native-free caller controls should establish same plan
fields on stable inputs, exactly one fewer context acquisition, same limits/budget,
and no caller-plan authority after the helper returns. Reuse existing unchanged
admission forged-plan/refusal evidence; a targeted stale-view case may confirm the
failure-phase distinction without launching a worker. Verify installation/native
identity equality and the intentional PROFILE/anchor-support differences as files.
No new mathematics, native rebuild, timing or acceptance-core campaign; stop after these seams and packaging.

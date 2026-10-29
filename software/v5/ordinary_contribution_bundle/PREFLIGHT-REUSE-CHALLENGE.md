# Challenge: helper-local advisory preflight reuse

2026-10-28, query_scaling. Source-only; no implementation, imports, owner/DB
opening, native work, runtime or Git. **Technically sound in the stated advisory
scope; not identity-free, and no measured whole-workflow speedup is established.**

## Actual seam

The adopted map selects `ordinary_demand_frontier/ordinary_contribution.py`
(`67962af4`), `ordinary_library_package/completion_api.py` (`76767855`) and
`ordinary_parse_reuse/ordinary_admission.py` (`98c88eb0`), not the older admission
file in ordinary_lean. Exact selected package remains PROFILE `e8d33500`.

Contribution obtains `context` at line432, uses its bindings for preparation and
candidate binding, then calls `owner.preflight` at593. Completion obtains context
at87, uses it for completion binding, then calls `owner.preflight` at116.
Current admission `preflight`530-536 checks the budget, calls catalog.context
again, checks the budget and calls `_plan`. Replacing only that final helper call
with existing `A._plan(context, actual_raw_units, same_limits, check)` therefore
removes one real selected-parent reconstruction from either successful workflow.
Use the full parent `context`, never contribution's optional ancestor frontier.

Catalog.context530-549 rereads the selected chain and rebuilds/validates its
bindings and module plan. `_context_rows`492-528 allocates those dictionaries and
lists afresh. Snapshot artifact hashes are already memoized per catalog process
(`_artifact`320-332), so the saving is repeated metadata/lineage work, not another
full native artifact hash or eliminated Lean import. `_plan` still reparses and
checks the supplied new units. The initial read and every admission read remain.

## Authority and freshness

`_plan`390-476 returns the existing raw-only immutable Preflight convenience
object. It neither accepts mathematics nor reserves a grant. It reads context
semantic_id/local_root/bindings without mutating them; parsed evidence does not
escape. These helpers retain a locally constructed context, expose only lookup
callbacks, and do not mutate its bindings. Contribution's equal-frontier alias
is read-only too. No whole-context copy, global cache or new context input is
needed. This relies on the existing trusted, serialized owner/callback contract,
not protection against a hostile in-process caller.

Current `admit`577-611 ignores caller status/order/missing/reuse claims, claims
the same budget, freshly calls catalog.context, and replans actual raw units
before custody staging. It then gets another execution context and calls
reserve_extension, which itself obtains a fresh parent context (catalog607).
Grant, exact parent-plan, native-event and commit checks stay unchanged. Reusing
an advisory context must not replace any of these reads or `_plan_with_parsed`.

Error timing is not identical. The removed context call currently rechecks
closed/withdrawn/activation/lineage state before advisory planning. Under reuse,
such a change can be discovered at admission instead; a stale NEEDS/conflict
result could refuse before that fresh read. There is no acceptance bypass, but
failure phase, first diagnostic and budget.claim timing may differ. The enclosing
failure retention/accounting stays unchanged. Do not promise freshly validated
catalog state at the advisory point or exact error precedence. Parent roots are
immutable under the intended exclusive lifecycle; this is not a cross-call
freshness policy. Keep existing limits, the current post-authoring budget, and
the helper's parent/budget checks before/during/after planning; grant no allowance.

## Identity and deployment cost

Leaving admission/catalog/native and INSTALLATION bytes untouched preserves core
implementation identity and existing mathematical catalog compatibility. Changing
either helper still changes its PROFILE pin, source map and selected package/kit.
Existing host descriptors remain tied to their original PROFILE; retain the old
package for those hosts rather than silently rebind them.

More consequentially, `module_export.support_descriptor`27-65 explicitly includes
ordinary_contribution as the `contribution` source role. A contribution-helper
change therefore changes module-anchor support_id even with unchanged core I.
`anchor_store._record` requires the current support_id: old anchors remain valid
under their old support, but cannot be treated as compatible warm anchors by the
new helper package. Do not remove that pin or relabel anchors to hide this cost.
Completion_api is absent from that support-role set; a completion-only helper
change would not by itself change anchor support if owner/loader/module support
bytes stay fixed. This is a real distinction in the cost of the two-file proposal.

## Recommendation

Accept the authority argument for narrowly scoped advisory reuse. The one-read
saving is proven from the call graph; its CPU magnitude is not. Do not justify
both helper changes solely by preserving I: contribution-side anchor turnover
can outweigh the unmeasured metadata saving. A completion-only change is the
smaller identity-cost option if its workflow frequency warrants it. Otherwise
retain this finding until evidence makes the marginal benefit compelling.

If root selects implementation, focused file/source controls should establish
same-context plan equivalence, no context mutation, unchanged limits/budget use,
one fewer helper context call, and fresh admission refusal after stale advisory
READY. Explicitly record changed failure timing and the selected identity delta.
No persistent cache/index, admission-core repair, broad profiling campaign or
repeat native/host lifecycle is justified by this challenge alone.

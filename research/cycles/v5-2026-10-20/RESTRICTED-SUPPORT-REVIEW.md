# Derived support: independent source review and control contract

2026-10-21, adaptive_audit. **PASS for the selected source refinement; no
runtime result is claimed.** Root owns the next compile/run decision. This
review independently inspected the complete predecessor/successor syntax and
typing diffs, unchanged production callers, new module root and all controls.
It does not reopen the failed RC investment screen or qualify v5.

## Refinement verdict

The summary is derived only from immutable, already interned children. The
selected production closure mutates expression storage only in `Arena::node`;
metadata construction must succeed before node/summary publication. The
per-node extra storage is O(N), with the existing 32,768-node bound unchanged.
No metadata supplied by a peer is accepted.

`loose <= offset` is sufficient for open's identity shortcut: it excludes both
the replaced variable and larger loose variables that the predecessor refuses.
The binder recurrence decreases only the body's loose bound. Local-node-ID
intervals prove close's target absent only outside their hull or when empty;
false positives merely cause the unchanged traversal. Local stored types stay
atomic, and exact node identity, not a local's serial number, is authoritative.
Close's added Local-kind precondition holds at its unchanged production call.

The height guard prevents a skipped region from silently evading the existing
128-depth limit. It can conservatively refuse a predecessor success whose
cache shortened traversal. Metadata and target-kind checks are charged; reduced
traversal or extra metadata work can change work-limit outcomes. Accordingly,
the claim is unchanged mathematical output on successful valid operations,
not identical resource-refusal sets. No type/reference/inference rule changes.
Exact interning preserves binder origins/styles and unchanged subtree IDs.
The detailed inductive argument is in `RESTRICTED-SUPPORT-SOURCE.md`; review
found no missing premise requiring a new mechanism or broader campaign.

## Frozen source contract

Paths below are under `software/v5/`; hashes were independently read from disk.

| Source | SHA-256 |
|---|---|
| `restricted_support/lib.rs` | `59ac0cdf921ae2891b3406a4a2178691ccf0eac70d72463439793dae4d8c4d9e` |
| `restricted_support/syntax.rs` | `30376f68bf44099620cfe4a593f2227adb12880b09918cbb2b0c7d79f09d77ec` |
| `restricted_support/typing.rs` | `ec81356278582f8da01d9992a8ea0f5d8531e4aa8c795846eb836cc67d7845d5` |
| `restricted_support/controls.rs` | `340ca8530a9cea7d54e87930f7489af0f487bdbec9d4d4d89ce692cb585166b8` |
| `restricted_support/controls_root.rs` | `d4df5796cffaf35319d1fce5d548a681fc9fbc4a9b5a80d00db56d5f85cf2a48` |
| frozen `restricted_composition/relation.rs` | `540af158f61654f50aa50335dec7811b43448f3520050edf953db7e75060670b` |
| frozen `restricted_composition/foundation02.rs` | `e8d0e32b3c480eb05b6813b6afd8eae8413930e26a436955783b2bf3e2452dce` |

Controls are independently authored here; growth/root review their source.
They link the retained old RC rlib as `dmkn_rc_baseline` and the fresh core as
`dmkn_rc_relation`. Private controls include the exact production syntax/typing
units, not another checking implementation. No aggregate or guest is linked
by the control root. Builder/selector review remains separately owned.

The root accepts only the retained four-field fixture, exactly 84,727 bytes,
SHA-256 `019219ca4548dafbdaa814c209a4ec087229091750db3f3cf48fcc155269f40a`.
Both differential cases execute old and new conditional checkers and compare
the full encoded J, ordered pending parents and source-derived expression,
level and address census. The two expected J hashes are from the independent
read-only commitment reconstruction in
`RESTRICTED-COMPOSITION-CONTROLS-OUTCOME.md`, not claimed to have been printed
by the original controls: first `0ba261cd27c816223aa56bc6cbe217e67f48264b8d1c707326095492620a1657`,
successor `dce99babfd2e4e579c2981e6461e4b80c2f794da53b0959eb7494ee1f7c82d86`.

Inference work is reported as old, new and signed removed work. There is no
arbitrary work-percentage gate and no inference-work-equality requirement.
Native work is not guest rows, certification cost or full-cost growth. Intended
refusals require their specific diagnostic after successful setup; panics and
setup errors fail the suite. Synthetic internal expressions are unit controls,
not mathematical contributions.

## Exact machine-readable result contract

Schema: `DMKN_RC_SUPPORT_CONTROLS_V1`. Success requires `status=PASS`, all 30
ordered `executed` entries passing, `executed_count=30`, exactly the 12 ordered
`expected_refusals` below and empty `errors`. Every report has
`crypto_produced=false`, `proof_calls=0`, `guest_calls=0`,
`global_growth_claim=false`, and authority
`NATIVE_CONDITIONAL_CONTROLS_NOT_RECEIPT_AUTHORITY`.

Ordered executed names:

```text
support_leaf_and_local_atomic
support_app_union
support_binder_domain_body
support_identity_interning_charge
reject_unknown_support_id
reject_unknown_child_id
open_closed_tree_constant_work
open_direct_bvar
open_nested_capture_sensitive
reject_open_larger_bvar
reject_open_nested_larger_bvar
open_closed_nested_binder_identity
close_direct_local
close_nested_capture_sensitive
close_outside_local_interval
close_inside_interval_absent
close_distinct_local_node_same_serial
local_type_is_atomic_for_both
depth128_closed_tree
reject_depth129_open
reject_depth129_close
reject_open_deep_closed_child
reject_exhausted_open_budget
open_exact_two_work_units
reject_one_unit_open_budget
reject_partial_metadata_construction
reject_nonlocal_close_target
references_still_reject_unknown_constant
first_exact_baseline_j_parents_census
second_exact_baseline_j_parents_census
```

Ordered expected refusal names:

```text
reject_unknown_support_id
reject_unknown_child_id
reject_open_larger_bvar
reject_open_nested_larger_bvar
reject_depth129_open
reject_depth129_close
reject_open_deep_closed_child
reject_exhausted_open_budget
reject_one_unit_open_budget
reject_partial_metadata_construction
reject_nonlocal_close_target
references_still_reject_unknown_constant
```

No compiler, product import, checker execution, proof, guest or old campaign
was run for this review. The next evidence is the separately selected two-
compile native discriminator, followed by an independent actual-outcome audit.
The failed guest screen's 75%-of-general row, 64-segment and CPU-nonregression
thresholds remain unchanged; no guest speedup or release pass follows here.

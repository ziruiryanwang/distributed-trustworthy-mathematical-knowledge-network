# RC support summaries: source implementation and refinement

2026-10-21, core_growth, under `RESTRICTED-SUPPORT-SELECTION.md`.
Source implementation/self-review complete; independent adaptive review and any
root-selected execution remain separate. No source import, syntax execution,
compiler, test, guest, proof or network call occurred. Used predecessors stay
unchanged. This is not an efficiency pass or a v5 release.

## Exact source closure

| Path under `software/v5/` | SHA-256 |
|---|---|
| `restricted_support/lib.rs` | `59ac0cdf921ae2891b3406a4a2178691ccf0eac70d72463439793dae4d8c4d9e` |
| `restricted_support/syntax.rs` | `30376f68bf44099620cfe4a593f2227adb12880b09918cbb2b0c7d79f09d77ec` |
| `restricted_support/typing.rs` | `ec81356278582f8da01d9992a8ea0f5d8531e4aa8c795846eb836cc67d7845d5` |
| frozen `restricted_composition/relation.rs` | `540af158f61654f50aa50335dec7811b43448f3520050edf953db7e75060670b` |
| frozen `restricted_composition/foundation02.rs` | `e8d0e32b3c480eb05b6813b6afd8eae8413930e26a436955783b2bf3e2452dce` |

The new lib selects the frozen relation/foundation through explicit relative
`#[path]` attributes, and the local fresh syntax/typing modules. The mathematical
module dependency remains the original adopted `dmkn_module_relation`. No
aggregate, census, wire, guest or foundation implementation is copied/revised.
Full old/new syntax and typing diffs were inspected; they contain only the
changes below and explanatory comments.

## Implementation

The immutable expression arena keeps one private `Support` entry per expression
node. `Support` is crate-private and Copy, with three fields:

- `loose: usize`: maximum loose de Bruijn index plus one, or zero.
- `locals: Option<(Id,Id)>`: min/max interval of syntactically occurring Local
  **node IDs**, or None. It is not a list or a serial-number authority.
- `height: usize`: maximum traversed App/Pi/Lam edge count to an atomic leaf.

Metadata never appears in input syntax or a journal and is never read from a
peer. Derivation uses the candidate node and immutable existing child entries.
New App/Pi/Lam children must have existing support entries; failed derivation
does not publish a partial node. Successful new nodes append their constructor
and summary together before entering the unchanged exact interning map. Reusing
an interned node reuses its existing summary. The original selected production
source has no arena-node mutation outside `Arena::node`.

Support construction is bounded O(1) work per new node, aside from existing
interning: zero or two child lookups, scalar unions/maxima and checked height
addition. Metadata is O(number of arena nodes), bounded by the unchanged32768
node cap. No source-size, arena-size, binders, universes or work cap is enlarged.

Only `open` and `close` use shortcuts. They retain the original depth check at
each visited node, then charge a support lookup before considering identity.
Open returns the same expression ID only if `loose<=offset`; close returns it
only if the target Local node ID is outside the conservative interval or the
interval is absent. Both require `height<=128-current_depth` before skipping.
All other paths continue through the original traversal/cache/interner logic.

For focused internal tests `close` becomes crate-private, like `open`. It now
explicitly checks that the requested abstraction target is a Local node,
charging that check. Every original production caller already supplies the
fresh Local created by the unchanged inference logic. Invalid arbitrary-node
abstraction is not a public/production capability being removed.

## Refinement argument

Let children mean only those actually traversed by old open/close: App's two
children or Pi/Lam's domain/body. In particular a Local's stored type is atomic,
as it was in the predecessor. Neither support construction nor height traverses
that type.

Induction over node creation establishes these invariants:

1. `loose(Bvar i)=i+1`; Sort/Const/Local give0. App takes maximum. A binder
   takes `max(domain.loose, body.loose.saturating_sub(1))`.
2. Every syntactic Local occurrence lies inside the stored interval. A Local
   contributes precisely its own immutable node ID; branches take the interval
   hull. False positives inside an interval are possible; false negatives are
   not. Empty support means no such syntactic Local occurrence.
3. Height is0 for atomic leaves and1 plus the maximum child height otherwise.
   It bounds every old recursive call below this node independently of caches.

For open at offset k, invariant1 implies that `loose(e)<=k` means every Bvar
at traversal depth d below intervening binders has index strictly less than
k plus that binder count. Thus no visited Bvar is replaced, and no Bvar has an
index larger than the current offset that the old algorithm would reject.
Induction over constructors shows the old transformation reconstructs exactly
the original node. Exact structural interning would return the same ID. The
shortcut returns that ID directly and cannot capture or alter a variable.

For close targeting Local ID q, invariant2 and the explicit Local-kind
precondition prove that an outside/empty interval contains no node equal to q.
Old close therefore performs no replacement in any traversed child. Again
structural induction and unchanged interning establish the same output ID.
If q is inside the interval but absent, the unchanged traversal handles that
false positive. No support test grants a type-equality or proof conclusion.

Invariant3 plus the guard prevents a shortcut from suppressing an old depth
overflow. It can conservatively refuse an old success whose cache would have
avoided some deeper visits; it cannot silently widen the128-depth profile.
The guard uses subtraction only after the original `depth<=128` check and
uses saturating subtraction, so arithmetic cannot wrap. Offset increments,
binder style/origin, raw IMax shape and universe substitution remain unchanged.

Consequently, apart from explicit resource refusal behavior, each shortcut is
the identity of the old operation. Substitution, abstraction, reference checking,
constant resolution, inference and conversion rules are otherwise unchanged.
The original conditional-relation/refinement argument therefore continues to
apply to every successfully completed check. Unavailable signatures, unsupported
syntax, unresolved receipts and mathematical failures do not gain shortcuts:
reference/inference and aggregate obligations remain in their original places.

## Honest work accounting

Original `inference_work` remains the only work counter and retains200000.
The successor adds one charge for each new-node summary construction, one for
each summary query (including child queries during construction), and one for
close's explicit Local-kind boundary. Existing node/interner and depth charges
remain. There is no skipped-work refund, fabricated timing counter or bypass
around charging a metadata query. Failure can consume allowance; no conclusion
is returned after a work refusal.

Reduced traversals may bring an input below its former work refusal, while
metadata overhead or conservative height checks may refuse another. That is
not identical resource-refusal behavior and is not claimed. Actual completed
conclusions must agree; the unchanged source-derived virtual-witness bounds
continue to establish inclusion in the original mathematical relation.

For an unaffected region containing n visited node/offset states, the old
transform traverses/reinterns that region on each call; the successor uses one
depth charge, one support query and constant-time identity/depth checks. The
summary's once-per-new-node cost is shared by subsequent calls. Repeated large
unaffected regions therefore provide a nonempty asymptotic saving region.
Fully affected small terms can instead incur overhead. No33.07% row saving,
actual-work reduction on the retained fixtures or CPU improvement is predicted.

## Review/control interface and next decision

Adaptive received exact source pins and the natural crate-private API:
`Arena::support(&mut self, Id)->R<Support>`, readable `loose/locals/height`,
existing `Typing::open`, and crate-private `Typing::close`. The intended controls
cover independent derivation, nested binders, larger out-of-scope Bvars,
Local.ty atomicity, local-interval false positives, present/absent locals,
height128/129 and work boundaries. External new/retained-baseline relations
compare exact J, parent journals and derived work on both existing fixtures.
Those controls are separately authored; this source note does not report them
as passed.

Release owns the minimal two-compile adapter using the retained old RC rlib as
an explicit baseline alias. Root owns all selections and runs. Native work
counts, if later obtained, are mechanism evidence only, not guest-row or
full-cost growth measurements. No guest/host rebuild or proof is selected here.
The failed RC screen and its75%/64segment/CPU thresholds remain unchanged.

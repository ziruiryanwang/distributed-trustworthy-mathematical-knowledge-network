# Selected fixed-basis correspondence, not a smaller foundation

2026-10-23. Source-only assignment by `preview_boundary_review`; root owns
integration, any finite operation and adoption. Original preparation, failed
consumer01 and all helper/build snapshots remain unchanged.

## Decision and practical consequence

Consumer01 refused while matching unrelated full-basis `Nat.gcd`, before any
group or acquired method was installed. The accepted receiver basis remains a
complete pinned foundation; the authoring correspondence need not match every
root of that foundation. Match only the transitive semantic closure needed by
the selected request. If `Nat.gcd` is actually reachable, retain it and report
the missing owner semantics; never special-case it away.

The new pure `owner_basis_projection.project(header_raw, groups, *,
inventory_raw)` validates the exact original 581-row basis projection against
the fixed inventory digest, then returns a new header and an exact selected/
omitted name census. `groups` is the existing tuple of bytes; none is changed.
The small inventory file is required, not the 49 MB evidence-preparation scan.
Profile, context, full basis ID, targets and group count stay identical. The
returned names are exact canonical encoded-name bytes, not dotted strings.
`materialized_units` counts ordinary non-generated optional construction units;
`generated_units` separately counts generated packets without claiming whether
they are already present in the real owner. Real membership is still checked
by Lean. No runtime result or selected-row count is claimed by this source note.

## Closure rule and argument

Let B be the exact complete fixed-basis rows and G the immutable selected
ordinary groups. Roots are references in every selected group interface/exact
semantic row, all construction references in missing ordinary units (including
their proofs), implicit literal support, and directly requested basis targets.
The selected basis S is the least fixed point inside B of these roots and the
following semantic-reference relation:

- Every row contributes references in its type, including projection heads.
- Definitions and non-theorem opaques also contribute their full body.
- Theorems contribute their type, not their opaque proof value.
- Inductives contribute mutual-family and constructor names; constructors
  contribute their parent; recursors contribute group names, rule constructors
  and complete rule right-hand sides.
- Permitted fixed axioms and quotient primitives retain exact type/metadata
  matching; neither adds a proof-body traversal.

Legacy DAG const/projection references are tags 2/8 with `[6, name]` wrappers;
ordinary DAG references carry names directly. Both representations retain
literal tags 7/9. Required references outside the fixed basis plus selected
groups refuse; basis rows whose closure leaves the fixed basis refuse. Rows are
emitted in original inventory order. Cyclic generated metadata is handled by a
visited worklist, not an assumption of acyclic individual names.

By construction every retained semantic reference resolves inside S or the
selected ordinary groups. Thus removing B minus S removes no explicit or
accounted implicit dependency of this selected authoring correspondence. All
needed exact comparison obligations stay intact in `OwnerRebind`; no body is
replaced by its type and no unchecked declaration is inserted. Existing
generated packets retain their types and computation rules; they do not cause
the proof ancestry of existing ordinary theorem interfaces to be traversed.
The three ordinary missing-unit packets still contribute their full proof and
definition dependencies through `inspect_unit`.

This is a selected-correspondence argument, not an independent claim that the
ordinary owner environment is globally sound. The separately warranted receiver
still has the whole original basis and checks the final contributed successor.
Only actually bound selected names may stop successor export; merely retaining
the full basis ID does not grant boundary status to omitted names. A later proof
using an unbound hidden definition must obtain its semantics or fail export;
this projection does not silently whitelist it.

## Implicit literal semantics

The pinned installed `Lean/Expr.lean` defines `Literal.type` as `Nat` or
`String`. Pinned upstream commit
`293d5d0c0c3f3dded4688b3ccd6a33939ac5102b` was inspected directly:

- `src/kernel/type_checker.cpp`, `infer_lit`: invokes the literal type;
  `reduce_nat`: native arithmetic is selected only by the explicit application
  head constant (`Nat.gcd`, etc.), not by the existence of a Nat literal.
- `src/kernel/inductive.cpp`, `nat_lit_to_constructor`: introduces `Nat.zero`
  or `Nat.succ` and another Nat literal.
- The same file's `string_lit_to_constructor`: introduces `String.ofList`,
  `List.nil`, `List.cons`, `Char`, `Char.ofNat`, and Nat literals.

Therefore every Nat literal adds `Nat`, `Nat.zero`, `Nat.succ`; every string
literal additionally adds the listed string/character/list support. Their full
semantic closure is then taken, potentially introducing further needed bodies.
An occurrence of a native operation is independently retained through its
ordinary const reference. A Nat literal alone does **not** force every native
arithmetic operation, in particular not an otherwise unreachable `Nat.gcd`.
This does not weaken the complete builtin-support requirement for receiver
foundation acceptance: that is already established separately and unchanged.

## Bounds and remaining evidence

One request-wide cap covers 64 MiB input, 8,192 groups, 65,536 rows,
20,000,000 counted DAG/literal node visits and 262,144 reference-set entries.
The existing strict JSON reader bounds raw syntax before parsing. Fixed legacy
inventory syntax is used only after its exact SHA-256 check. No filesystem IO,
source execution, hashing of a new mathematical identity or external action is
performed by the helper. An empty basis closure currently refuses because the
unchanged Lean command requires a nonempty basis, rather than adding an
irrelevant row to manufacture success.

Independent source review and a root-selected actual projected-header/use/export
operation remain necessary. Successful source use would still not be receiver
acceptance, unknown-ID discovery, measured useful growth or completion of v5.

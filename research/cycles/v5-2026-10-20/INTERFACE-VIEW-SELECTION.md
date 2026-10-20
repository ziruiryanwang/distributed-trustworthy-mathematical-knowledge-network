# Explicit interface-only authoring for imported definitions

Root source selection, 2026-10-20. This advances the unchanged final v5 goal
on this PC. No proof campaign, RAM investigation or guest image change.

## Why this change

Source inspection finds eager body traversal in the installed
`runtime_efficient/mixed_claims/imports_atomic.py::_build_context`. Every opened
transparent definition's body is required even when subsequent reasoning needs
only its authenticated name and type. A body-only chain can therefore force
arbitrarily many acquisitions without any use of those reductions.

The unchanged `modules/native_rows.py::NativeRows.group` already emits an exact
`moduleImportDef` with committed body hash and reduction hints when an imported
definition body is absent. The final native checker retains missing-body demand;
it never reinterprets that definition as an accepted axiom or opaque declaration.

## Selected semantics

Add an explicit opt-in interface view. Default eager behavior is unchanged.
Only ordinary imported definitions may omit bodies. Types and their references
remain required. Inductive groups and recursor rules remain eager and complete.
Present bodies retain their original semantics; no automatic removal or retry.

The Lean frontend is an untrusted proposal generator. It may represent an
explicitly deferred imported definition by a rigid constant of the exact type.
Original authenticated descriptors, hashes, hints and identities remain stored
separately and are the sole inputs to final native witness emission. A frontend
projection is never an authenticated module opening or mathematical warrant.
New local axioms remain forbidden. Exported foreign names still resolve only to
the exact authenticated imports. A final missing-body failure yields no warrant
or publication; no fallback to opacity, fresh grant or automatic restart.

This view can be incomplete: hidden type aliases may prevent elaboration or
positivity checks. It is not an equivalent frontend, lazy conversion protocol,
general omission of semantic data or constant-cost import guarantee. For
body-independent proofs it can avoid work that the current eager path mandates.

## Implementation scope and owners

Fresh successors only under `software/v5/interface_views/`; all used predecessors
and the installed distribution remain unchanged. Before editing, pin the actual
logical predecessors from the installed map plus tested supplier_complete overlays.

- core_growth: context algorithm/session overlay and a small pure frontend
  projection helper; explicit mode binding and original descriptor preservation.
- core_search: ordinary client/SemanticReader and source-operation plumbing,
  reusing the original Lean executable if a clearly separated untrusted frontend
  projection suffices. No copied checker or new arbitrary source authority.
- core_release: independent review and disjoint focused controls, especially
  final descriptor preservation, forbidden local axioms and missing-body failure.
- Root: integration contracts, exact source mapping, selection and Git.

Agents must agree on shared interfaces before edits. No runtime/build is selected
yet. Prefer a small coherent vertical change over a helper that no client uses.
Controls must distinguish type/body demand reduction from full-cost growth and
real mathematical admission. Any actual Lean/native call requires separate
bounded root selection after source review, not a repeated existing campaign.

## Actual changed-boundary adapter: source preparation only

After source feasibility inspection, root selects preparation (not execution)
of one genuine public-owner contribution through a fresh pinned SDK source map
and existing installed binary assets. core_search owns a new actual adapter
under `software/v5/interface_views/actual.py` and a fresh current-cycle selector;
core_growth independently reviews them after reviewing the focused controls.

Reuse the retained mathematical input and summary-independence construction,
but select BASE groups 0 and 7 plus TARGET group 0, with only the two required
Tree recursor bodies. The expected frontend context is three groups/six
declarations/two bodies, compared with nine groups/twelve declarations/nine
bodies previously needed. The fold definition body is intentionally omitted;
final native witness emission must still preserve its definition kind/hash.
The call must actually check its new output and durably publish it.

The existing public `client.launch` may bind a fresh source map while reusing
the unchanged installed Lean/native/receipt assets. Do not alter the installed
distribution or claim its frozen `run` command loads these new sources. No new
guest, prover, copied runtime, or whole-distribution rebuild is required.

The retained input packet still includes native-tail witnesses and their
semantics. Therefore this changed-boundary test demonstrates smaller selected
authoring semantics, not reduced total initial proof traffic, a new succinct
frontier, positive full-cost growth, or final v5 completion. Source review and
the pure controls must pass before any finite actual-operation selection.

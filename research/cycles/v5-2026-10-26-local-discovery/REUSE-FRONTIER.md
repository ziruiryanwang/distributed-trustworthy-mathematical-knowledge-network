# Rich-concept reuse: proof closure is not the authoring frontier

2026-10-26. Source/data-only audit; no product imports, Lean/native execution,
owner state, tests, network or Git operations. No new cap, cache or module is
selected. The retained TheoryB bytes are not a newly accepted contribution.

## Decision

**The existing ordinary contribution route is the decisive first alternative.**
A module's 66 or 106 exported units do not establish that a selected reuse request
exceeds its 32-group bound. The bound counts the request's selected semantic and
materialization frontier, not the whole module or every theorem-proof ancestor.
For the concrete retained `same_constraints_same_run` target, that frontier is
21 units, although its complete import/proof closure contains 36 units and its
bundle contains 106. A cap/module redesign is not justified by those larger counts.

## Exact source argument

The selected source path is `software/v5/ordinary_project_return/ordinary_contribution.py`:

- `request_targets` selects exact already-warranted acquired targets; an empty
  selection uses warranted fixed-basis `Eq`, not a fabricated new premise.
- `contribute_source` obtains the selected protected parent context and retrieves
  exact local locators/evidence. It calls `ordinary_lean/portable_owner_request.py`
  with `owner_absent=lambda name: True`. Thus this case does not rely on having
  the foreign project's compiled Lean module in the authoring environment.
- `assemble_source` imports `Init` and the pinned construction/export helpers;
  optional trusted-project imports are absent when `authoring_backend is None`.

Let B be the fixed basis and T the selected targets. Define the least group-closed
set F containing the nonbasis groups of T. For each selected group U:

1. If U has exactly one kind-2 theorem row, follow references in its **type only**.
2. Otherwise, follow all its external unit imports: this route assumes the group
   absent, so actual definition/inductive construction data must be available.
3. Stop at B; include complete atomic groups, not arbitrary individual records.

This is exactly the relevant traversal in `portable_owner_request.prepare`
(lines 124–153), using `owner_request._semantic_refs` (lines 66–82). It still
reads/parses complete retained evidence for each selected U, and verifies the
protected warrant for **every import of U**, including proof-only imports that
it does not traverse. It does not fetch those omitted imports' evidence merely
because they appear in a selected theorem proof. F must be acyclic and identities
and group names must agree exactly; neither a remote claim nor an arbitrary map
is an eligible protected context.

`OwnerConstruction.lean:192` constructs missing singleton theorem signatures as
scratch axioms after checking their exact types. This supplies authoring premises,
not new mathematical acceptance. Definitions and generated groups use the separate
checked construction path; theorem proofs are expressly excluded from it.
`PortableContributionExportCommand` and `SuccessorExport.selectedDeferred` stop
new-output serialization at the prepared interpretation boundary.
`portable_candidate.bind_candidate` resolves exact imports again; complete **new**
units must then pass `owner.preflight` and `owner.admit` in the real receiver
context. A scratch axiom never independently becomes an accepted theorem.

## Conditions for no-foreign-project reuse

The route supports a rich concept when all of the following hold:

- The selected mathematics and its exact import warrants already belong to the
  protected parent. Local evidence/locators for F are retained and available.
- F is within 32 groups, 4096 rows including the 581 basis rows, 32768 semantic
  edges, 131072 acquired nodes, 4 MiB acquired evidence and 4 MiB prepared payload;
  each fetched evidence/group is at most 1 MiB. At most 32 acquired targets.
- Native construction can reproduce the required types/definitions/groups under
  the pinned Lean semantics, with no conflicting existing names and within its
  own decoding/checking/scan/resource limits. No notation, instance attribute,
  tactic plugin or source elaboration metadata is promised by inert export.
  The caller may use explicit qualified Lean terms instead of such conveniences.
- Owner-authored source makes new outputs using those reconstructed interfaces.
  Its newly exported closure, **not its selected ancestors**, must meet the
  separate 32-new-unit/4 MiB candidate and admission bounds and pass actual checking.

These are structural preconditions plus actual checking obligations, not a static
theorem that every in-budget request succeeds. Proof history can be arbitrarily
larger than F, but an individual selected theorem's complete evidence is still
read and bounded: the current API is not a proof-free interface store.

## Retained example: independent JSON graph census

Input: `experiments/v5-local-checks/concept-theory-b-export-01/bundle`.
Target unit: `0be846200d7809eaa68cf06cf23ef362052d4d3f4a5db4892c7f369691393e83`.
Target raw SHA256: `f47ae493eb89d7c052f62b039d9f929195b9e02f72aa38acaa597e4195774556`.
Manifest SHA256: `680cd98f8d1d31ef251b1e78b1cdae7a60bbe2b733e95193b0fe52cb9855c302`.
Fixed inventory SHA256: `c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0`.

Read-only Python standard-library analysis verified all 106 manifest length/SHA
pins, indexed complete groups by exported name, and followed the two rules above.
Type references were constant/projection nodes (tags 2/8); missing nonbasis names
were refused. No product code was imported and no output/state was written.

| Data census | Complete target import closure | Selected signature frontier F |
|---|---:|---:|
| Units | 36 | 21 |
| Export rows | 47 | 32 |
| Retained raw bytes | 274177 | 155125 |

F has one theorem signature and 20 definition/generated groups: the abstract
repair, order, closure structures, `AllClosure`, `run`, `Safe`, `Settled`, their
required auxiliaries and membership machinery. Its serialized unit nodes total
3202; request semantic edges total 93; rows plus basis total 613. Projected group
payload is 209914 bytes before the header (largest group 21419 bytes); this is a
byte-length calculation with fixed-length identity placeholders, not preparation.

The six proof-only imports excluded from F remain required protected warrants:
`Iff.mp`, `Iff.mpr`, `RepairTheory.run_settles`, and ClosureBridge's
`run_extensive`, `run_below_settled`, `OrderData.antisymm`.

## Closure of this audit

No new capability obstruction is established by the module-size argument.
Use the existing signature-based path before proposing another mechanism. The
counts do not prove native success, successful source authoring, useful growth,
proof-free first acquisition or a completed deployable v5. A genuinely oversized
definition frontier or selected evidence blob would be a real current limit;
neither follows from the whole-module count in this example.

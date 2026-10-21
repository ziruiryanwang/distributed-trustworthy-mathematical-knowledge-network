# Selected bounded numeral importer

Root, 2026-10-20. Implement the small source seam, not a new checker or experiment
framework. Read/adopt SEMANTICS `5a4d9a19`, SOURCE-SEAM `f01196de`, and the
independent review `1f79655f` (GO). Root read the complete saved review.

## Scope and invariant

Fresh successor `software/v5/nat_literals/source_rows.py` replaces only logical
`modules/source_rows.py` (`60c7255d`) when explicitly selected. No used predecessor,
installation, policy, foundation, frontend or checker/image bytes change.
Normalize only raw `natVal` decimal strings to the exact captured local Nat
zero/successor constructors. Preserve OfNat applications and all other syntax.
Require the original complete, unambiguous local Nat group with exact type and
constructor shapes; preserve all recursors for unchanged independent checking.
No foundation, external, relocated-lookalike or arbitrary-name Nat inference.

Normalization preserves meaning before relocation by native literal definitional
equality and congruence. Relocated validity is a separate mandatory fresh check;
failed or expensive conversions refuse under unchanged limits. This does not
solve subsequent builtin-Nat/relocated-Nat interoperability or provide source
execution attestation. No general arithmetic or growth advantage is claimed.

Preflight decimal spelling/value, per-expanded-occurrence work, depth and generated
bytes before unary allocation. Preserve existing whole-expression/group/spec
limits and source census. Reject strings and oversized/unsupported literals.
Do not turn a bounded importer into an automatic representation optimizer.

## Ownership and verification

- core_search: fresh successor and short `nat_literals/README.md`; checkpoint
  exact changed boundaries there. No test/runtime/Git ownership.
- core_release: independent source review and disjoint `nat_literals/controls.py`.
  Positive zero/small numeral and original-constructor equality, exact Nat group
  and name-role refusals, malformed/huge values, depth/work/byte limits, repeated
  DAG occurrences, unchanged nonliteral and OfNat structure. Synthetic fixtures
  establish importer contracts only, not mathematical acceptance.
- core_growth: minimal existing-route native smoke plan; then source fixture/
  adapter only on separate selection. No new benchmark or crypto production.
- root: finite existing-supervisor selector, launch after source/control review,
  actual adoption, ledgers and explicit reviewed Git checkpoint.

One focused small contract run is the intended next runtime; it is not selected
until exact source hashes are reviewed. A genuine frontend-plus-fresh-checker
case then decides real arithmetic compatibility. No full installation rebuild,
passing-campaign rerun, new receipt production, RAM investigation or cloud work.
The full v5 goal stays active; this removes a concrete ordinary-source obstacle.

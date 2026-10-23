# Original-expression codec implementation checkpoint

2026-10-22. `lean_acceptance_boundary`. Source-only selection fulfilled; root
and independent reviewer still need to inspect before any compilation/execution.

Created only the selected `software/v5/ordinary_lean/OriginalExpr.lean` and
`EXPRESSION-FORMAT.md`, plus this checkpoint. No frozen predecessor changed.
No build, runtime, test, proof or Git action was run.

The new codec preserves exact binder names/annotations, original caller-bound
ordered universe names, let nondep and native literals. It strips only mdata;
uses ExprStructEq/Expr.equal memo identity; validates bounded backward DAGs,
closed roots, exact arities/UTF-8/numeric bounds and canonical re-encoding.
Role-neutral name decoding permits anonymous binders; semantic references use
the reserved-name barrier and the caller's grounded-name set.

The wire envelope has an explicit `DMKN_LEAN_ORIGINAL_EXPR_V1` marker. This is
a fresh format, not an ambiguous reinterpretation of the old normalized DAG.
Bounds precede native node/name/literal construction, but outer serialized-byte,
JSON parser depth and process-resource limits are explicitly caller obligations.
The codec is inert syntax only, not declaration acceptance or persistence.

Ready for source review against the independent named-argument and metadata
findings. Next execution, if root selects it, should be one focused compilation
and metadata/hostile-data discriminator; do not rerun the old basis campaign.

Initial authored hashes (not execution pins): OriginalExpr.lean
`f9b281dfcd2864ec29f92b849a256dc79053262e3cbdc4aa98e38ead3617fc05`;
EXPRESSION-FORMAT.md
`950fc2c9cadc1f3c3af69cf9ebbece497eebc876c8bd266650645cc0f69b22ce`.

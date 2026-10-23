# Original-declaration source checkpoint

2026-10-22. `lean_acceptance_boundary`. Implemented only selected fresh
`OriginalDecl.lean`, `DECLARATION-FORMAT.md` and this checkpoint. No build,
test, runtime, proof, package or Git action.

Public namespace/API agreed with root: `OrdinaryLean.DeclCodec`,
`DecodedUnit {decl, expected}`, `decodeUnit`, `encodeUnit`, `inventoryRow`,
`expectedNames`, finite nested `Limits`. All helpers operate on inert data;
none imports or changes an environment. Original params/hints/all metadata
and the entire generated recursor inventory are preserved. Unsafe/partial,
axiom and quotient-initialization inputs refuse. Group-local reference
permission includes only group type names during descriptor construction.

Preflight bounds total descriptor and inventory expression/level nodes before
descriptor decoding. Expected inventory is claims-only and is never converted
to peer ConstantInfo. Root's checked-extension adapter must perform actual
kernel insertion, complete fresh-name census and exact actual-row comparison.

The independent codec reviewer found no concrete metadata/scope/canonical-DAG
logic defect at the initial source hash, but identified an outer JSON numeric
token hazard: exponents must be screened before the general parser. It is
recorded in the format contract and sent to root; this is a future outer reader
obligation, not a hidden assumption that parsed Json is a secure network input.

Both modules remain uncompiled source candidates. Independent review and a
root-selected focused compilation/control run are still required before use.

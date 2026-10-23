# Ordinary Lean integration boundary

This is a source candidate, not an installed service or an accepted v5 release.
It makes ordinary checked-library reuse the default development path. Generic
cryptographic certification remains optional and is not invoked here.

## Practical endpoint

An ordinary Lean participant discovers a previously unknown peer method over
`Std.ExtHashMap`, receives inert declaration data, checks only missing knowledge
above its accepted dependencies, uses it in its normal project, and shares a
downstream result. Checked local knowledge survives closing and reopening the
checker. A provider's signatures or binary `.olean` files are never proof evidence.

The test method is read-footprint preservation under `insertMany`; the downstream
use is preservation of an arbitrary predicate on a finite read snapshot across
multiple write batches. Std already provides single-key no-touch lemmas. Reusing
those lemmas earns no novelty credit. This endpoint tests interoperability and
composition; benefit over ordinary package sharing requires separate full-cost
accounting, including initial dependency checking and unsuccessful discovery.

## Component contract

1. `ExprCodec`: bounded inert syntax, exact ordinary binders/universes/native
   literals, erase only expression metadata. It grants no mathematical authority.
2. `DeclCodec`: safe ordinary declaration units and advertised output records.
   Constructor/recursor records are claims, never unchecked insertions.
3. `CheckedExtension.checkBatch`: direct finite `Environment.addDeclCore` with
   `doCheck := true`, known-parent references, no new axiom/quotient primitive,
   no overwrites, actual generated-record comparison, atomic batch output.
4. Pending controller: exact selected basis/profile, bounded serialized reader,
   persistent catalog and protected local snapshot writer/restorer, fresh grants.
5. Pending ordinary-project command: match accepted dependency meanings against
   actual private/kernel owner records; check-add only missing declarations;
   expose actual checked auxiliary recursors; `setEnv` only after success.
   Keep normal imports/notation/instances. Do not import checker snapshots beside
   Init. Export the successor for a final independent receiver check.
6. Pending discovery adapter: translate ordinary-profile types and symbol locks
   into the existing bounded index engine. Its resolver requests applicable local
   checked evidence, not unconditionally a succinct certificate.

`checkBatch` is INTERNAL CONDITIONAL PLUMBING. Its `Environment` argument is not
a warrant. A future peer API must obtain the parent only through the protected
controller, not from a peer binary, frontend, or a caller-set verified flag.
Even `quotInit = true` proves neither the exact builtin basis nor axiom policy.

The preservation argument is: a valid exact-profile parent plus an allowed unit
plus actual successful kernel insertion yields a valid extension, conditional on
the kernel and adapters. Output comparison binds what was checked to what was
advertised. Protected local persistence preserves this judgment; ordinary binary
loading does not create it. No certificate, global ledger or consensus is needed
for that local induction.

## Cost and compatibility boundaries

Reference scans and output comparisons concern the new data. Generated census
checks traverse only bounded stage-two state once per batch, not every imported
proof or the full environment for each declaration. Restore places saved ancestors
in stage one. Startup still hashes/loads the selected local snapshots. Initial
acquisition may need the missing proof closure; strict no-history onboarding
requires separate applicable evidence or an explicit unavailable result.

The frontend can use arbitrary owner tools; it remains a construction aid, not
authority. `Lean.addDecl` is deliberately avoided at the receiver boundary because
its elaborator wrapper supports skip-check options, asynchronous checks and recovery
axioms. Ordinary source authoring is checked again as inert data on publication.

All new development files may evolve through reviewed successors. Executed
immutable experiment snapshots, inputs and outputs remain preserved byte-for-byte;
no failed outcome will be rewritten to fit a repair. This avoids making every
small development edit a second product installation. Frozen predecessors are
unchanged. Builds and changed-boundary checks still require a finite root selection.

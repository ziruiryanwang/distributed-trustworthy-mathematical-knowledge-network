# Metadata-preserving ordinary Lean boundary: first source selection

2026-10-22. Root has fully read ACCEPTANCE-BOUNDARY, PERSISTENCE-BOUNDARY,
WORKFLOW-TRACE and REVIEW-BOUNDARY, and independently inspected the relevant
Lean/Bootstrap/exporter sources. This selects fresh source only, not execution,
adoption of a new foundation, or a release claim.

## Decisive findings and design choice

The ordinary kernel checking and local serialization APIs exist. The retained
456-unit basis has genuine empty-environment reconstruction machinery and native
Nat/String/Quot support. But its codec normalizes binder names, universe names,
definition hints and mutual-block metadata. It is a mathematical bootstrap reuse
candidate, NOT a drop-in ordinary Init module.

The independent review also found that Lean rejects duplicate imported definitions
even when equal. Therefore checker snapshots remain internal to the isolated
mathematical environment. Normal authoring needs checked rebinding of NEW
declarations against exact-compatible ordinary imports, without importing the
checker basis a second time. Authoring success never becomes admission authority.

These findings rule out simply persisting the old descriptor format and calling
it full ordinary Lean interoperability. They justify one concrete necessary
source change before any costly compatibility run: a metadata-preserving inert
expression/declaration representation and checked extension adapter.

## Selected first source ownership

`lean_acceptance_boundary` may create only:

- `software/v5/ordinary_lean/OriginalExpr.lean`
- `software/v5/ordinary_lean/EXPRESSION-FORMAT.md`

This is the first component of the actual ordinary-library path, not a standalone
release target. Reuse the established bounded DAG/name/literal encoding patterns
and exact structural memo comparison. Do not alter old BootstrapSupport,
AuthorLean, installed products, receipts or used experiment code. Do not implement
a new checker, new crypto backend or new network. Root owns later integration.

### Concrete codec contract

Use a distinct format, not ambiguous reinterpretation of old tags. Preserve
original declaration level-parameter names at the caller boundary; level nodes
refer to their ordered positions. Preserve native Nat/String literals. Retain
old semantic tags for bvar/sort/constant/application/literal/projection; add
binder-name fields to lambda/forall and binder-name/nondep fields to lets.
Use explicit binder-info codes and exact original-name components. Anonymous
binder names are permitted; anonymous or forbidden semantic declaration/reference
names are not. Remove only expression mdata, explicitly documented as outside
mathematical and ordinary binder metadata. Free/metavariables remain forbidden.

Hash-map memoization must distinguish binder names/annotations: Lean's BEq Expr
does not, but Expr.equal does. DAG indices point backward; node/depth/name/byte
bounds are checked before constructing the untrusted expression. Roundtrip must
preserve this format's relevant structure, not silently normalize it to the old
lossy format. Avoid recursive expansion of shared DAGs during checking.

The codec grants no authority. The later extension adapter must preserve exact
hint kinds and all/group information, check against grounded imports via actual
kernel constructors, and compare generated records. Those are separate selected
steps after this necessary syntax component is reviewed. In particular, no
withHeight rewrite may silently change an ordinary extension's hint metadata.

## Review and execution rule

The author supplies the source and a short implementation checkpoint here.
Root and a distinct reviewer inspect new behavior against the format contract.
Only then select bounded compilation and metadata/hostile-input checks, including
named binders, native literals, forward references, bad scopes and metadata-sensitive
sharing. No current build or runtime is authorized by this source selection.

Parallel root work fixes the checked-extension/owner-rebind API and persistence
integration contract from the three source notes. Do not build a generic storage
or scheduling framework while the actual mathematical use boundary is unfinished.
The final v5 goal remains unchanged; this selection removes a demonstrated blocker
to that workflow rather than substituting an easier success condition.

## Integrated source continuation (same cycle, after codec delivery)

The fresh payoff audit found that Std already supplies `insertMany`, its append
law and single-key no-touch lookup. Do not clone these and count that as growth.
The concrete workflow endpoint is now a peer-only read-footprint abstraction:
`ReadsOnly R F` and `Avoids R log` imply that `F` is unchanged by `insertMany`.
A downstream participant applies that method to a finite read snapshot and an
arbitrary predicate across a sequence of write batches. This is a composition
and usability discriminator, not a claim of novel mathematics or measured growth.

Source-only ownership is extended as follows; no execution is selected here:

- `lean_acceptance_boundary`: `software/v5/ordinary_lean/OriginalDecl.lean`,
  implementing safe def/theorem/opaque/group records and actual-record projection
  on the delivered codec API. Preserve exact ordinary metadata, reject new
  axioms/quotient initialization. No new checker or binary importer.
- Root: `software/v5/ordinary_lean/CheckedExtension.lean` and
  `INTEGRATION.md`; finite direct checked insertion, no frontend bypass and no
  assumption that an arbitrary environment is warranted. Keep this as internal
  plumbing until profile/controller/persistence binding exists.
- `ordinary_payoff_audit`: optional source-only `ReadFootprint.lean` and
  `ReadFootprintConsumer.lean` under `software/v5/ordinary_lean/examples/`,
  using Std's real existing statements. Preserve the strong package-sharing
  comparator in the payoff note. These are owner-authored mathematical inputs,
  never peer code the receiver should execute.
- `lean_workflow_trace`: independent codec review, then changed admission and
  owner bridge source review. Do not duplicate the payoff/comparator audit.

The source continuation is justified by actual API and compatibility findings;
it is not permission for a full backend build or certificate. Root later chooses
only compile and changed-boundary controls that can change the integration decision.

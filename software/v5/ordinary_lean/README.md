# Ordinary Lean candidate

The default-direction implementation for inexpensive native library reuse,
without mandatory cryptographic certificate production. Not a completed v5
release or an externally deployable service yet.

`OriginalExpr` preserves ordinary Lean names, binders, universes and native
literals in bounded inert DAGs. `OriginalDecl` preserves safe declaration and
generated-group records. `CheckedExtension` directly calls the Lean kernel and
compares actual output; its parent environment is an explicit warrant precondition,
not something a caller can assert through a public endpoint.

## Working path

The installed owner APIs now perform fresh checked onboarding, exact dependency
binding, durable portable evidence retention and incremental native admission.
The [independently audited reciprocal workflow](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-API-RECIPROCAL-OUTCOME.md)
used real formal-index discovery: B found A's method, checked its missing evidence,
used it twice in an ordinary Lean proof after A stopped, and published a checked
successor that C rediscovered and acquired from cold B custody. C was an inert
acquisition client, not a third independently accepting owner. All roles ran on
one machine. This is operability evidence, not a worldwide-release/growth claim.

| Boundary | Interface | Meaning |
|---|---|---|
| Select local implementation | `NativeInstallation.open` in `ordinary_admission.py` | Owner-pinned manifest and runtime attachments; not remote mathematics. |
| Open persistent checked project | `OrdinaryAdmission.open` | Exact local catalog and separately owned inert custody. |
| Learn fixed foundation once | `owner.initialize(OperationBudget(...))` | Actual checked initialization for a fresh store, not a per-use operation. |
| Plan a bounded missing delta | `owner.preflight(parent_root, raw_units, budget=...)` | Reports exact missing imports; a plan is never an acceptance token. |
| Check and retain the delta | `owner.admit(parent_root, plan, budget)` | Revalidates, retains evidence, runs the controlled native checker and promotes only after a clean exact event. |
| Reuse locally warranted knowledge | `portable_owner_request.py`, `portable_candidate.py` | Exact theorem signatures and necessary definition semantics for owner authoring; new exported proofs still require admission. |
| Contribute caller-selected source | `ordinary_contribution.contribute_source` | An open owner, zero to 32 acquired exports, UTF-8 source body, and one to 32 new definition/theorem names; bounded authoring followed by the same independent admission. |
| Locate/acquire/serve inert objects | `../transport/ordinary_acquisition.py` | Typed preview, export locator and complete unit evidence; custody does not transfer acceptance. |

The generic contribution API removes the earlier fixed theorem/template
restriction. Its [contract](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-GENERIC-AUTHORING-IMPLEMENTATION.md)
documents exact encoded names, pinned authoring support and shared parent-budget
callbacks. Caller source is executable owner-approved code, never automatically
downloaded peer source. `ContributionError.report` preserves accepted-root
information if later publication fails; it also reports exact missing meanings.
Preparing an acquired method does not require using it, and definitions need no
theorem wrapper. The [explicit-source example](examples/GenericContributionExplicitBody.lean)
shows two acquired methods producing a bare definition and a checked theorem.

The earlier installed examples are `run_ordinary_api_producer.py` and
`run_ordinary_api_receiver.py`; `ordinary_successor_authoring.py` is the older
single-fixture helper. These are selected development callers, not a universal
installer or permission to execute peer-supplied source. One finite caller budget
must encompass its stages; do not renew grants inside missing-dependency loops.
The owner closes its catalog; the caller separately closes custody and services.

For normal local use, prefer the [ordinary package commands](../ordinary_package/README.md)
over those experiment callers. The source-built package has an audited relocated
initialization and a corrected caller contribution followed by persistent status.
Its exact runtime attachments remain explicit. It does not yet provide peer CLI
commands or arbitrary Lake-project integration; a separate file-only peer
successor is under development without changing the acceptance core.

## Scale and remaining work

No client enumerates the whole network. Cold ordinary learning nevertheless
acquires and checks its selected missing dependency closure. Warm use avoids
rechecking locally warranted old proofs, but currently rebuilds/loads selected
context metadata. Use bounded project contexts and batches; this is not a
constant-cost guarantee for unbounded local libraries.

An optional unfamiliar-vocabulary discovery adapter now uses bounded
definition-body fingerprints followed by existing exact-symbol method search.
Its metadata-only check reduced examined postings from eight to three but
increased search reply bytes from 103,356 to 202,790, including the false
candidate branch. It is not a default planner or a demonstrated total-cost win.
Search hints remain separate from evidence and acceptance. Selectivity at both
stages, full-cost benefit, context scaling, public packaging and deployment
security remain release obligations. Windows Job limits are containment, not a
hostile-source sandbox. License and public distribution are still undecided.

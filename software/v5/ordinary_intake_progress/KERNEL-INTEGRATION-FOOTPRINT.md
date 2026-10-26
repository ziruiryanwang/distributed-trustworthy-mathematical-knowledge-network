# Receiver-only kernel path: minimum integration footprint

Source-only investigation by kernel_path_integration, 2026-10-26. Canonical root
is `E:\Distributed Trustworthy Mathematical Knowledge Network`; checkpoint is
`research/cycles/v5-2026-10-26-local-discovery/CHECKPOINT.md`. No compiler, product
import, owner/status, database, test, Git or state operation was performed.
PRIVATE-NAME-COMPATIBILITY owns the mathematical/API repair argument. This note
describes integration consequences, conditional on root selecting that repair.

## Recommendation

Keep the first repair inside the existing **receiver lane**. Its native objects
live in `installation/lean-lib`; the ordinary project/authoring helpers live in
the separate `authoring/helpers` lane. A kernel-only path for inert admission
does not justify changing the elaborator-facing helpers or recompiling extractor
executables, query helpers, ordinary project support, transport or search.

Keep the existing eight receiver module names if the safe implementation permits.
The installation loader has an exact module census, not an arbitrary plugin list.
A ninth KernelCheckedExtension module would require unrelated Python/layout
changes. Adding a function inside an existing receiver source avoids that work.
This is a footprint recommendation, not permission to duplicate or weaken the
checking relation; the source/API design still needs its independent justification.

## Exact native dependency closure

The selected receiver sources use these imports:

| Module | Relevant project imports | Required treatment if CheckedExtension changes |
|---|---|---|
| OriginalExpr | none in this closure | Reuse exact current receiver object/source. |
| OriginalDecl | OriginalExpr | Reuse exact current receiver object/source. |
| BootstrapSupport | Lean/Std support, no CheckedExtension | Reuse exact current receiver object/source. |
| CheckedExtension | OriginalDecl | Compile the selected receiver successor. |
| LocalSnapshot | CheckedExtension | Recompile; use selected successor if its call/result boundary changes. |
| OrdinaryExport | BootstrapSupport, OriginalDecl, CheckedExtension | Recompile the **receiver** source, even if text stays unchanged. |
| BasisSnapshot | BootstrapSupport, LocalSnapshot | Recompile, even if text stays unchanged. |
| OrdinaryWorkflowWorker | OrdinaryExport, BasisSnapshot | Recompile; use selected successor if dispatch changes. |

Thus the five-module compilation order can be CheckedExtension, LocalSnapshot,
OrdinaryExport, BasisSnapshot, OrdinaryWorkflowWorker, with the three unchanged
prerequisites pinned. The receiver OrdinaryExport is the selected
`ordinary_package/receiver_source/OrdinaryExport.lean`, not the public authoring
source of that basename. Use the actual package installation/source map to select
these bytes, rather than a directory-wide latest-source scan.

Do not mix changed receiver modules into `authoring/helpers`. Its public-header
transform and generated companions are a distinct established lane. Reusing that
lane is justified only while its mathematical/front-end API and dependencies
remain unchanged. This preserves current frontend metadata behavior but does not
claim that the old frontend path can ingest every normalized-name collision.

## Reusable machinery and smallest new orchestration

The existing `ordinary_installation.py:assemble` is already a suitable file-only
installer. Its pinned plan selects exact source/object files, verifies external
runtimes, preserves exact roles/support groups, computes their support digests
and implementation ID, and writes INSTALLATION last. Its current source SHA is
`637142362b667e639d5895300dae9d9d575323ea30687dda1dafeebc00812467`.
The adopted parse-reuse assembler demonstrates this mechanism against a selected
base package; its retained source is an example to reuse, not an operation to rerun.
Existing ordinary-file helpers and the Run-V5-Check Job supervisor also suffice.

There is **no unchanged drop-in receiver-only build CLI** among the inspected
current entries:

- `ordinary_package/build.py:compile_worker` always compiles eight receiver and
  thirteen authoring modules. Its build controller pins the public transform of
  CheckedExtension in PUBLIC_HASHES. Feeding a globally changed source into this
  frozen entry would fail or require an unnecessary authoring-lane change.
- `ordinary_current_release/build.py` additionally builds extractors/query and
  pins release.json by MAP_SHA. Its fixed source map is not an override mechanism.
- `ordinary_lean/run_workflow_build.py` assumes unchanged historical
  CheckedExtension/LocalSnapshot prerequisites; it cannot serve this repair.

If selected, a small bounded compile adapter can reuse the exact existing compiler
invocation/environment/supervision pattern while selecting only the five modules
above. Use a fresh source/object subtree, scrub LEAN/PYTHON inherited settings,
keep the pinned supported runtime, and record all commands/outputs and actual
object pins. Supply complete prerequisites without inheriting a mutable search
path. This is finite build orchestration, not another selector or protocol.
Whether to copy the three prerequisite objects into that fresh tree or use an
explicit immutable prerequisite search root is an implementation choice that
must be bound and reviewed before execution.

After a passing focused native boundary, form a fresh package from the adopted
154-file progress package. Replace only the selected receiver source files and
five rebuilt objects, regenerate INSTALLATION through the existing installer,
and update PROFILE's installation hash. Its 117 auxiliary file rows can remain
byte-identical. For S changed receiver source files, at most S+7 package files
need differ (S sources, five objects, two manifests); recompilation does not
promise that every object actually differs. Require the exact observed delta.

This focused development route does not finish source-distribution integration.
Before distributing a final source release, the flat release map/build must
explicitly select receiver successors separately from unchanged authoring
sources. Never claim a source archive reproduces this package while it still
selects the old receiver. That consolidation should follow the decisive native
boundary, rather than rebuilding all unrelated lanes first.

## Identity and owner state

The mathematical semantic identity and inert Std evidence need not change if
the repair preserves the exact checking relation and codec. The implementation
identity **does change**: receiver source/object hashes participate in
adapter_support; LocalSnapshot participates in snapshot_support; a changed
BasisSnapshot object can also change basis_receiver_support. Kernel/controller
support can remain unchanged. Derive actual identities, never predict them.

PortableCatalog binds the complete implementation in ADOPTION.json and its
database marker before ordinary use (`portable_catalog.py:145-190`). An old
owner cannot be reopened under the new implementation merely because its
semantic ID is equal. Existing UPDATE-AND-RECOVERY policy calls for fresh state
and independently checked selected inert mathematics. Do not edit markers,
copy a successful old basis snapshot into a newly trusted owner, or promote the
failed run's retained artifact. The failed owner can remain preserved; no
additional recovery operation is necessary merely to investigate a fresh lane.

## Minimum changed-boundary evidence

Prefer a tiny native fixture before another 2,651-unit intake:

1. Two distinct exact private names with the same normalized user name, including
   a private/public pair, retain distinct values/types and check without stderr.
   A later declaration must use the intended exact names; acceptance of one
   constant while silently losing the other is a failure.
2. The kernel-only path still rejects an ill-typed proof, exact duplicate/overwrite,
   ungrounded reference, disallowed axiom/unsafe declaration, and a tampered expected
   generated record. Select only cases whose shared-core refactor changes the
   boundary; do not repeat the entire old parser/transport suite.
3. If persistence plumbing changes, write one small collision-bearing checked
   chunk, restore it through the existing snapshot route, and check one dependent
   continuation. Require exact names/records, fresh artifact bindings and clean
   diagnostics; compilation or a saved worker report alone is insufficient.
4. Audit the fresh installation's exact changed-file map and implementation
   identity. Only then select fresh basis initialization and, if still useful,
   one observable intake using the already retained manifest/bundle and original
   finite budgets. This note selects none of those operations.

Keep the elaborator-facing API source-equivalent, or explicitly review/test any
change to it; a generic core refactor may warrant one small compatibility control.
Root owns that decision after the actual source diff. No budget enlargement,
stderr filtering, global renaming, new certificate path or migration is justified
by the current native diagnostic.

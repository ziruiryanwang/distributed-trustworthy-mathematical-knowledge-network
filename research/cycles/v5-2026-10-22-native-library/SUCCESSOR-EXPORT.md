# Successor export above an accepted correspondence

2026-10-23. Source implementation by `successor_export`, under root's explicit
selection. No compilation, consumer run, mathematical admission or Git mutation
was performed by this assignment. Existing used producer/checker source snapshots,
artifacts and the accepted recovery context remain unchanged.

## Workflow and decision

A consumer has used `OwnerRebind` to obtain the actual accepted method under
ordinary Lean names, then written a new theorem in the same source module.
Publishing that theorem must not require the original proof bodies of already
warranted dependencies. Otherwise the efficient authoring interface would merely
move the old private-import/ancestry problem to the contribution step.

This implements the narrow cut already specified in `OWNER-REBIND-PLAN.md`:

```text
selectedAbove(owner, authenticatedBoundNamesAndSymbolIDs, targets)
  -> dependency-first new ordinary units + selected exact boundary labels
```

There is no new certificate system, package manager, global census or warrant
from a theorem type. Existing declaration encoding, atomic-group reconstruction,
dependency scheduling and receiver checking are reused.

## Selected sources and interfaces

- `software/v5/ordinary_lean/OrdinaryExport.lean`: module-enabled mutable source
  successor; factors the former selected-closure loop into
  `Export.selectedFromBoundary`. Existing `Export.selected` still requires its
  exact fixed-basis source comparison before entering that loop. Existing caller
  fields remain available. The extra `boundaryReferences` field is not inserted
  into historical producer-bundle schemas.
- `software/v5/ordinary_lean/SuccessorExport.lean`: `selectedAbove` and
  `bundleBytes`. Inputs use `OwnerRebind.BoundName`. The bundle schema is
  `DMKN_ORDINARY_SUCCESSOR_BUNDLE_V1`, with exact `profile_id`, `context_id`,
  `basis_id`, selected boundary labels, new units, targets and finite counters.
- `software/v5/ordinary_lean/SuccessorExportCommand.lean`: public command
  `#ordinary_export_above fully.qualified.theorem "fresh-absolute-output"`.
  It uses actual `getEnv` and `OwnerUse.getBoundContext?`, requires the same
  current module, a nonimported new theorem target outside the bound names,
  and at least one new exported unit. It never calls `modifyEnv`, `importModules`
  or any receiver/catalog adoption operation.

The command depends on the contemporaneous `OwnerUseCommand.lean` authoring seam.
The agreed `BoundContext` fields are `profileId`, `contextId`, `basisId`,
`mainModule` and `bindings`; its environment extension is local/nonpersistent.
Source/API compilation remains a root-owned next gate, not assumed here.

Source hashes at this checkpoint:

```text
OrdinaryExport.lean
3f2c8a4d95cb7c5d39f614f80f4c739aa28cd8d37705b036e7f83764399de040
SuccessorExport.lean
28f455679669e56245ada61f61345849b20faab1da6a043d0dc0e5657ef85028
SuccessorExportCommand.lean
a091f8879869b7484fc560c723642bc2835411390c19a7035c5a181007f79623
```

Root subsequently ran `ordinary-successor-core-build-01`, selection
`233f414cbd217884668ecf39f9371f65838f169ab8a06e81e7181077de91a7bb`.
This author read its saved `COMPILE-RESULT.json` and `RESULT.json`: the two core
modules compiled with exit zero, clean closure, 2.03125 Job CPU seconds and
0.4375 wrapper CPU seconds. This is source/API compilation only, not an
independent review or a successor operation. The command module remains a
separate build gate. Retain/reuse the successful core artifacts; do not rebuild
them merely to compile the command.

### Command staging successor

The first command build failed in `OwnerUseCommand` before reaching the
successor command: its generated elaborator was `meta` but called a local
non-`meta` `run`. Lean 4.34's module system distinguishes compile-time helpers
from run-time executable functions. `Lean/Parser/Command.lean` documents that
ordinary imported functions can be made available for public metaprograms using
`public meta import`; local executable helpers must be `meta` as well.
`Lean/Compiler/LCNF/Visibility.lean::checkMeta` enforces that distinction.

The unexecuted successor command is updated correspondingly: its three imports
are `public meta import` and its declaration section is `public meta section`.
This changes staging only; no kernel checking option is disabled and none of the
ordinary codec/export/checker helpers are converted to `meta` or rebuilt.
Current command SHA256:
`1b5a381476d84b832d5200456aa6087c3c9e5e25d322c61076e86d9bf538a741`.
The earlier command source hash above records the preserved first build snapshot.

## Boundary invariant and assurance argument

Let `K` be the actual accepted receiver context and `B` the exact correspondence
returned by successful owner rebinding. The controller, not the exporter, must
establish that every `(name, symbolID)` in `B` denotes its warranted declaration
in `K` and matches the applicable authoring semantics. The owner environment may
subsequently add ordinary declarations but must not replace that correspondence.

The shared closure scheduler enforces:

1. A selected reference in `B` stops traversal. Neither `makeUnit` nor theorem
   proof serialization runs for that stopped name. Exact symbol labels survive
   in the successor bundle.
2. A name outside `B` is grouped using the existing actual-kernel owner function.
   Its complete new declaration unit is serialized. Existing
   `CheckedExtension.allowedDeclaration` still excludes new axioms, quotient
   primitives and unsafe/unsupported declaration forms.
3. No emitted group may overlap `B`. A referenced generated member outside `B`
   whose owner is inside `B` is refused as `BOUNDARY_GROUP_STRADDLE`. Complete
   generated-group correspondence is inherited from the actual rebinding event,
   not inferred from a matching group owner's type.
4. The finite selected dependency graph is Kahn-scheduled. A nonclosed or cyclic
   new graph refuses. New units retain the existing exact original-expression
   and declaration inventory encoding.
5. Before a new axiom-shaped unit could be serialized, the exporter returns
   `MISSING_WARRANT_OR_FULL_DECLARATION original_name=<encoded-name JSON> name=...`.
   This includes preexisting public theorem handles absent from `B`. It is a
   request for a real accepted correspondence or full inert proof evidence,
   never permission to insert a fallback axiom or import every private proof.

Conditional conclusion: if the controller authenticates the boundary and the
receiver resolves its exact IDs in `K`, then receiver checking of every new unit
extends `K` by checked declarations without requiring the owner to reconstruct
the boundary's proof history. This is a composition argument for the intended
pipeline, not a claim that the source helper itself proves the premise or that
compilation constitutes mathematical acceptance. Calling the public helper with
a fabricated boundary can at most produce untrusted claims; it cannot create a
catalog warrant.

## Exact imports versus the bundle lookup map

`boundary_imports` contains reached original names and their unchanged accepted
symbol IDs. It can additionally contain implicit literal-stage support from the
existing `BootstrapProbe.makeUnit` machinery. It is therefore a selected lookup
map, **not** a per-unit evidence envelope's direct-import census.

The trusted controller must use the existing
`ordinary_evidence.inspect_unit(unit).external_names` to derive exact imports,
resolve each against this authenticated map or earlier new units, canonicalize
them, construct the existing evidence envelope, and run `read_evidence` plus
actual receiver checking. It must not put incidental literal-only names into
that envelope's import list. It must not accept names/IDs merely because they
appear in the bundle. Profile/context labels also require exact controller checks.

## Cost and remaining census boundary

The new entry starts with direct kernel lookups and an empty group index.
Ordinary new definitions and theorems never enumerate the owner environment.
Thus their export traversal depends on the selected new proof/declaration data,
its distinct references and bounded boundary map, rather than all imported
compiler/library declarations or ancestral theorem proofs.

If the selected new closure genuinely introduces an inductive group, complete
actual generated records—including nested recursors—are still needed. The helper
then invokes the existing bounded `indexSource` once and reuses that group index.
It does not guess recursor names from surface syntax. This local fallback has a
cost proportional to the imported owner constant census; it is not hidden or
claimed to be globally size-independent. `source_records_enumerated` reports zero
when no census occurs, otherwise the actual bounded count.

Finite bounds remain explicit: at most 65,536 supplied boundary names, existing
8,192 selected units / 262,144 selected dependency edges / 20,000,000 scanned
nodes, 8 MiB per ordinary unit, 64 MiB unit payload and 64 MiB final bundle.
Host CPU/wall/RAM supervision remains the controller's responsibility. These
limits do not create a hostile-code sandbox.

## Immediate integration obligations

Compile only the new public authoring helpers, reusing the successful lower
support artifacts. Then use the existing consumer proof body and export the
substantive successor in the same source session. Independently admit its inert
new units over actual accepted context `4d70ddd6...`; that also exercises loading
the final recovery snapshot.

The current 1,098-name prepared semantic map is smaller than the 3,622-name
accepted context. Consumer proofs may invoke other ordinary Std theorem handles.
A precise missing-warrant refusal is expected evidence for selectively extending
the real correspondence, not a reason to broaden trust, load all private data or
claim complete reciprocal use prematurely. Unknown-ID discovery, full-cost
growth advantage, portable catalog integration and deployment remain separate.

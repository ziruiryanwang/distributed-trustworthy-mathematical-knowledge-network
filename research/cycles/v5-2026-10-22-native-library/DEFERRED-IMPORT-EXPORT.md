# Reached imported names as deferred receiver-resolution requests

2026-10-23. `successor_export`; root-selected source successor after consumer04
constructed its selected handles and elaborated the substantive new theorem,
but could not export imported `Iff.rfl` outside the finite prepared map.
Independent review found that name already accepted in the actual parent.
No runtime, Git, catalog mutation or experiment edit was performed here.

## General correction

The prepared construction closure is not necessarily the complete set of local
library lemmas a later proof will use. Requiring that closure to predict every
future proof dependency is unnecessary. Neither a one-name exception nor an
all-parent authoring map is the appropriate fix.

The new explicit candidate path stops at safe imported owner names and carries
unclaimed names to the receiver for exact pointwise resolution. They are not
assertions that the receiver contains those names. If any are missing, report
the complete bounded missing set before native work. This change neither
acquires missing proofs automatically nor turns imported local axioms into
receiver warrants.

## Exact source cut

| File under `software/v5/ordinary_lean` | SHA-256 |
|---|---|
| `OrdinaryExport.lean` | `1d4df6817098f5ad9cd0106d98f39a6905a55be8b23484294b5c3d22653a7d4f` |
| `SuccessorExport.lean` | `c68286f46711d0f2c2e13db972ffbc207feb6a4bfea157a53a251bfb5cb1d8c8` |
| `ConstructExportCommand.lean` | `b7f9cd638a2178068b485adb6695bb476517eda1a10b3b6b584d74707d257a94` |

The source-only V2 catalog contract was also completed separately at
`PORTABLE-CATALOG-CONTRACT.md`, hash
`26553e975ca5dbb788fe6a217e4ecf1e07144a74ac553fd4eae3604fa6ab993b`.
It does not change this immediate V1 consumer/receiver integration.

## API and bundle

New API:

```text
Export.DynamicBoundary {stop : Name -> IO Bool, maxLookups, maxNames}
Export.selectedFromBoundary(..., dynamic : Option DynamicBoundary := none)
SuccessorExport.CandidateExported {exported : Exported, unresolvedImports}
SuccessorExport.selectedDeferred(owner,preparedLabels,introducedNames,targets,limits)
SuccessorExport.candidateBundleBytes(profile,context,basis,candidate,limits)
```

`#ordinary_export_constructed` now invokes the new deferred entry and emits
`DMKN_ORDINARY_CANDIDATE_BUNDLE_V1`. It retains the existing assurance and fields
but adds `unresolved_imports`, an array of original encoded names, and the
matching `stats.unresolved_imports` count. `boundary_imports` still contains
only names with explicit prepared accepted-ID claims.

The earlier `selectedAbove`, `selectedInterpreted`, `bundleBytes` and exact
commands remain explicit unchanged routes. The shared scheduler's default
`dynamic = none` preserves its previous static-boundary behavior. No old packet
schema silently gains optional authority-bearing fields.

## Traversal invariants

The shared scheduler has one bounded memo of both positive and negative dynamic
answers. Each distinct nonstatic name consumes one lookup, at most 262,144 by
default. The total static plus dynamically stopped names is at most 65,536.
No owner-library enumeration or external catalog call occurs. The dynamic
predicate only checks `isImportedConst`, point lookup and the existing safe
record filter. Existing limits still bound new units, scan work, edges, group
records, unit bytes and total bytes.

It is essential to consider **both** raw references and normalized group owners:

- `unit.refs` retains actual referenced names, including a constructor or
  recursor member. Stopped raw names enter `boundaryReferences`.
- `unit.edges` normalizes such references to atomic group owners. Its stopping
  test prevents the scheduler from exporting an imported whole group after
  already stopping at its member.
- If a raw member does not stop but its owner does, the existing straddle
  refusal remains. New generated groups remain atomic and cannot emit names
  that already stopped at the boundary.
- Merely consulting an owner to cut traversal does not fabricate an extra
  per-unit import. The packet is formed from actual reached raw names. Existing
  literal-stage support can remain in this lookup map; the receiver derives
  exact per-unit imports from inert evidence as before.

Reached prepared names still require a safe owner record which is imported or
recorded as construction-introduced. A current-module new declaration sharing
a prepared name refuses. Other new local declarations are exported completely;
an unsupported local axiom still refuses. New targets cannot be imported or
already in the prepared boundary. Unresolved entries are imported names only,
never arbitrary locally authored claims.

## Receiver obligation, owned separately by root

Before constructing any checking envelopes or launching native work:

1. Strictly parse the new schema and bounded known/unknown arrays, refusing
   duplicate names, overlap, malformed names and inconsistent statistics.
2. Check each claimed boundary ID against both the authenticated prepared map
   and actual accepted parent, as before.
3. Resolve **every** unresolved name against that same eligible protected parent.
   Collect/report missing names within the operation's aggregate budget; do not
   promote a partial map, invent IDs, or start a worker on incomplete resolution.
4. Recompute each new unit's complete external-reference census and use these
   exact resolved IDs or earlier checked-unit outputs for its envelope. Reject
   unsupported references and overwrites. Run the unchanged native all-new-unit
   checker and retain actual input/report/artifact/grant-before-commit binding.

The acceptance argument is unchanged: the receiver checks complete new units
under its own exact meanings. An imported local name may denote something
different; the candidate then either checks under the receiver interpretation
or is rejected. A safe local imported record is a serialization stopping hint,
not a mathematical trust premise. No peer native artifact or source is imported.

## Remaining evidence

Root owns source adoption and bounded compilation/consumer/controller runs;
`admission_event_audit` owns the independent changed-boundary review. No passing
runtime result is claimed here. The useful discriminator is the same ordinary
consumer reaching real receiver checking with the general resolution rule,
not another broad proof/correspondence campaign or a patch specific to `Iff.rfl`.

# Direct inductive interfaces: use the existing publication path first

Disposition: **no new product mechanism is needed to make accepted Plan and Exec
independently searchable**. The seven-target contribution route remains suitable.
Its result does not itself include Plan/Exec previews, but the existing public
`peer.py publish` operation can construct and index them afterward. A narrower
contributor-target convenience change is feasible; select it only if returning
all nine targets directly is worth a helper rebuild and focused controls.

This is a source-only decision review against the adopted
`experiments/v5-local-checks/kernel-admission-package01/distribution/package`.
No compilation, product import, database, owner call, test, publication or Git
operation was performed. No rich-parent or contribution success is inferred.

## The existing route already supports direct concept publication

The current contributor checks only the requested names when producing previews,
but exports and admits the complete reachable new declaration groups. Therefore,
if the selected seven-target contribution passes, Plan and Exec occur as genuine
accepted outputs of their complete inductive units, not as unverified aliases.
The receipt exposes each retained unit's bytes/path and the resulting local root.

For each desired concept name `n`, find its exact inventory row in those returned
public evidence bytes. Let `U` be that unit's verified portable ID and compute
`e = export_id(S, U, n)` with the existing identity function. Supply `(n, U, e)` to
public `peer.py publish`, using the accepted result root and existing custody.
This requires no private database inspection, wrapper theorem or replacement
concept definition.

Use the contribution's `RESULT.units` rows (`file`, `unit_id`, `bytes`, `sha256`)
to select and verify those evidence files. The inventory is `document.unit[2]`;
require the exact structured Plan/Exec names and kind 4. The existing pure
`ordinary_contribution.publication_targets` can derive their triples from these
raw units with `[Plan, Exec]` as output names. This is identity calculation, not
another contribution or owner-state operation.

The existing CLI shape is below; placeholders become exact selected values only
after contribution success. The configuration has exactly `index`,
`context_root`, `targets`, `max_unit_bytes`, `max_total_bytes`. Its `targets` array
contains the two derived triples and `context_root` is `RESULT.local_root`.
`index` uses the existing path/limits/create configuration; select its own storage
directory, disjoint from the catalog and custody. Preserve the same owner store ID
and configured custody limits. There is no native allowance or source body here.

```text
D:\Python314\python.exe -I -S -B <package>/peer.py publish
  --profile-sha256 60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b
  --python-runtime D:\Python314 --lean-runtime <pinned Lean runtime>
  --catalog <existing catalog> --custody <existing custody>
  --store-id <existing store ID> --custody-limits <existing limits JSON>
  --config <selected publication JSON> --config-sha256 <its SHA-256>
  --output <fresh publication evidence directory>
  --wall-seconds <finite bound> --cpu-seconds <finite bound> --memory-mib <finite bound>
```

This is a prospective invocation template, not a run selection. `publish` writes
only the owner's local index/custody; it does not start service or contact others.

Current `peer_api.publish` (lines 827-890) establishes all of the following before
index admission:

1. The selected local context has the exact name-to-export binding `n -> e`.
2. The provided unit/name reproduce `e` under the current semantic identity.
3. Custody supplies the selected bounded evidence; the requested inventory row
   yields a preview which resolves against those exact evidence bytes.
4. The existing index receives that preview under its exact export ID.

There is no definition/theorem-only restriction in this path. Its typed adapter
maps inventory kind 4 to `inductive`; portable preview validation already permits
kinds 1 through 6. The resulting records support the existing declaration-kind,
type-symbol, result-head and declared-type-key features. An inductive's broad
type can have many matches; this is ordinary bounded discovery, not guaranteed
unique or globally complete search. In particular, Exec's type references the
exact Plan and map interfaces, whereas Plan's sort-valued type is less selective.

Indexing remains distinct from mathematical acceptance. Publication neither
rechecks an accepted proof ancestry nor grants recipients authority to trust the
publisher. A recipient still acquires exact evidence and follows its ordinary
local checking policy. Multiple publication targets commit separately; preserve
successful rows if a later row fails.

The relevant exact current package files are:

| File | SHA-256 |
|---|---|
| peer_api.py | `dcaea5226f58e4254dd4cff0d6c621cf593aabe9b4d511d127194816c8ddc0ef` |
| authoring/py/ordinary_contribution.py | `09394f523417406aefcad0b47d06fa2d7782940bec3bb5094975f08b68f94ca8` |
| authoring/py/portable_preview.py | `b78dd54340b7b55e4359769d6784f7f225ba304457ce880ce2760717e865550d` |
| authoring/py/ordinary_preview.py | `0fd9bb516fbb53d9d4264271853904e35810286fc92d5670d15d7a9d3c26b0d6` |
| support/discovery/ordinary_export_adapter.py | `3ddbed2156a393b08543a5da88c89b5c5b9c2b4f65689c46fbd7623cec38db0a` |

## Optional direct contribution target change

The current authoring source
`software/v5/ordinary_lean/PortableContributionExportCommand.lean`, SHA-256
`dc6988a6a237f482fed6f9055d8a248e430c8c99cb17c70a4a110774717e0182`,
is selected unchanged by the existing release source map. Its explicit kind
guard admits `.thmInfo` and `.defnInfo` only. The exact prospective change is to
allow `.inductInfo` too, with an accurate diagnostic/comment. Keep all prior
theorem/definition behavior and checks. Constructors, recursors, opaque values,
axioms and quotient initialization need not become new selectable target kinds.

The required safety invariant is not merely "kind 4 is serializable." Preserve:

- Top-level construction context and same owner module; exact nonduplicate names
  and target bounds; no imported target or prepared-boundary target.
- `OwnerRebind.requireSafe`: exact record key, no unsafe or partial declaration.
- Existing group-owner resolution. Selecting any inductive member must export
  its complete mutual group, constructors and recursors, deduplicated by owner.
- No partial imported/local group boundary; no forbidden/unwarranted dependency;
  current unit/node/byte/census limits and expected-target equality.
- Actual ordinary receiver checking and exact generated inventory comparison
  before producing checked contribution/publication bytes.

`SuccessorExport.selectedDeferred` already excludes imported target names and
retains unresolved imported names as requests, not invented identities.
`OrdinaryExport.selectedFromBoundary` already groups inductives, refuses group
straddles, checks allowed declarations and emits a closed topological unit list.
`portable_candidate.bind_candidate` checks every requested name occurs among
new complete-unit outputs; `publication_targets` maps any inventory kind to its
exact unit. None of these modules requires a change for `.inductInfo` targets.
For the existing finite-map body, adding the two type targets should add preview
rows while using the same already reachable group set; exact ordering/bytes are
to be observed, not assumed identical across different target orders.

## Exact rebuild and identity footprint if selected later

The changed module imports only `PortableConstructExportCommand`, which already
imports its required unchanged authoring chain. No other shipped Lean helper
imports `PortableContributionExportCommand`; generated authoring files import it
at their next ordinary compilation. Thus the minimum is **one helper compile**,
using the current package's `authoring/helpers` prerequisites and a fresh output
directory. Receiver `installation/lean-lib` must not shadow authoring modules with
the same names. The old full-package builder is unnecessary.

The source is already a `module` with `public meta` import/section; do not run
the separate public-header transformation on it. Preserve the established
`lean.exe -DElab.async=false -R <source> -o <fresh object> <source file>` invocation,
scrub inherited Lean/Python configuration and retain an exact input/output map.

The current module has exactly five installed artifacts: `.olean`,
`.olean.private`, `.olean.server`, `.ir`, `.ir.sig`. Collect its actual new outputs
and update those five existing PROFILE rows; record which bytes actually change.
The prospective package delta is at most these five artifacts plus PROFILE.
There is no ninth receiver module, new profile field or new entry point.
All 112 other auxiliary rows, all receiver installation bytes and all eight
additional package guides remain unchanged. The package census remains 154.
Retain the successor source separately and explicitly include it in any future
source distribution; old frozen source archives do not reproduce a new helper.

INSTALLATION remains exactly
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`;
implementation identity remains
`86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea`.
The local catalog marker binds implementation/store/limits, not the auxiliary
PROFILE hash. A separately adopted helper/profile can therefore use the same
unchanged checked rich parent through the normal public open path, with the new
PROFILE hash supplied explicitly. No marker rewrite, basis recheck or migration
is justified solely by this authoring-helper change. Preserve normal exclusive
owner locking, corruption checks and failed-operation handling.

## Smallest decision-changing controls

For the recommended unchanged-software route, use the already planned successful
seven-target contribution rather than making another mathematical episode:

1. Read its returned Plan/Exec unit rows and exact accepted root. Publish those
   two direct inductive targets through the existing public command.
2. Retrieve their previews through an existing bounded index query; require
   kind 4, the exact types/bindings and equality to the acquired evidence rows.
   Do not infer this from seven neighboring previews or a bare result count.
3. Submit one mismatched name/unit/export triple through the same publication
   boundary. Require exact binding refusal before index admission; retain its
   outcome without repeating unrelated receiver controls.

If root instead selects the helper change, first use one tiny export-level
fixture with a safe new inductive plus an existing eligible definition/theorem.
Require complete group inventory and exact direct target mapping. In that same
bounded fixture, test an imported inductive target and a current-module axiom
target: both must refuse without producing candidate output. A constructor-only
selection should remain refused if the narrowed policy is retained. Feed the
positive candidate through ordinary syntax/binding/preview checks and use the
single planned actual finite-map admission as the integrated receiver test; do
not repeat rich-library intake. Independently audit actual helper/package deltas
and unchanged INSTALLATION before using the current protected parent.

Recommendation to root: keep the seven-target source/plan unchanged and add the
existing two-target publication step after success. This closes the useful
searchable-concept outcome with lower cost. The convenience of selecting
inductives directly can remain a small later API improvement rather than a
prerequisite for the current mathematical contribution.

# Typed lifecycle entry: source checkpoint

2026-10-22. Implements the root's
`TYPED-RENEWAL-PRODUCTION-SELECTION.md` as two new files only:

| File | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/typed_production/lifecycle_operator.py` |19,820|`a23c24c35b81110c8a3b0ea5e503811c3baa35ee042b1fed9c526684909a31aa`|
| `software/v5/typed_production/LIFECYCLE-CLI.md` |6,318|`1bb8acbf9a43b72bfaa28f88a06e34e2f205c410e29150ab31bf735a91355060`|

Status: **source authored; independent review and controls pending**. No source
import, syntax check, control, request preparation, snapshot, proof, installation
or Git mutation was performed by this author. All old producer/profile/source and
used operation files remain unchanged. The entry is not yet a release claim.

## Contract agreed before implementation

Author and independent reviewer agreed separate `snapshot` and `request` actions,
common explicit source-root/self-hash/profile/input/report arguments and a bounded
stdlib bootstrap before product imports. The reviewer identified a prospective
digest cycle in the first proposed input wrapper before code was written. The
implemented snapshot input is therefore the existing generic configuration
directly; `--outer-selection {output}/selection.json` binds the actual copied
wrapper selection at runtime, without placing its hash into a document whose
hash that selection already contains.

The copied selection's run name, source location/hash, configuration/profile pins
and literal-substituted argv must match the real invocation. The request action
forbids `--outer-selection` and accepts the completed five-role snapshot evidence
through `DMKN_TYPED_LIFECYCLE_REQUEST_ENTRY_V1`. No new producer schema is created.

## Deliberately narrow implementation

- Before importing product modules, bootstrap verifies isolated Windows mode,
  self hash, the29 producer files, their matching support-runtime rows and the
  existing `aggregate_small/operator.py` file. It rejects preloaded product
  packages, checks all loaded module origins, then rebinds those source bytes.
- It imports the unchanged producer29 from its explicit stable root; the new
  entry stays an outer-selected source. There is no new profile factory, plugin
  callback, consumer SDK import or source-tree copy inside the profile.
- Snapshot calls existing `prepare` once and `snapshot` once. It verifies the
  saved result against the returned object, applies the existing result-shape
  gate and retains/rebinds cited generated evidence. A raised snapshot call has
  unknown host-dispatch extent, not a fabricated zero-host result.
- Request calls existing `production_request` once. Its internal preflight is
  not duplicated. Only after owner closure and rebindings does the entry write
  the returned request into a fresh file; the future proof directory must remain
  absent. No `run` method is referenced or called.
- Existing pinned-document, declared-pin, separation, rebinding and durable-save
  helpers are reused after bootstrap. All outputs are fresh and mutually
  nonoverlapping with source/install/input boundaries. Owner constructor failure,
  action failure, close failure and finalization failure cannot pass.
- Late rebind/report or partially written request failure produces a separate
  overriding finalization sentinel when possible. Unsafe bootstrap paths are
  never written; the failure is printed and exits nonzero. The enclosing wrapper
  must still bound startup/imports/refusal/closure/exit and provide actual closure.

## Independent control seam

`main(argv)` and `_bootstrap(args)` are explicit. Bootstrap returns the ordinary
helpers/producer/snapshot/envelope modules, exact source/profile pins and the real
`sys.orig_argv`; tests may replace it with expressly inert objects. The separate
`_snapshot_selection` helper retains real copied-selection/source/argv checks.
The reviewer owns new controls and their exact test contract. Such doubles cannot
qualify actual host execution, cryptographic verification or mathematical truth.

The new entry enables the already implemented lifecycle; it does not invent
future U/V receipts, fund a campaign, change producer caps or assert that useful
growth is profitable. Actual U acceptance, source-derived V admission, one actual
new V layout and its separate cost-based production decision remain prerequisites.

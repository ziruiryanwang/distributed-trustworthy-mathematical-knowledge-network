# One current release selection

2026-10-26. Source-only map; root adoption and independent review precede any
driver execution. Local and unpublished; license remains undecided. This is a
distribution repair, not completed v5 or evidence of growth acceleration.

## What is selected

`release.json` names the current package directly. An operator does not apply
historical overlays or need historical experiment receipts to build, prepare or
use the selected software. Repository-relative source names are preserved so
existing Lean module/import identities remain unchanged.

There are two distributions of this same selection:

- **Source:** 93 exact build inputs, eight operator companions and five current
  release-support files, totaling 106 payload files before the outer manifest.
- **Prebuilt:** 154 exact package files, the same eight companions and four
  release-support files, totaling 166 payload files before the outer manifest.

Both place the new guide at `README.md`. Other companion destinations retain
their repository-relative layout. Source distribution has the new build driver;
prebuilt distribution has `package/` instead. Neither embeds Python or Lean
runtime distributions. The outer `CURRENT-RELEASE-MANIFEST.json` adds one file
to each census; both remain within the existing 256-file helper bound.

## Package-role closure

| Kind | Files | Selection |
|---|---:|---|
| Exact direct copies | 72 | `build.copies` plus `build.sources` pins |
| Receiver objects | 8 | `build.lanes.receiver`, `.olean` only |
| Authoring helper parts | 65 | 13 modules times five `authoring_suffixes` |
| Formal-query helper parts | 5 | One query module times five suffixes |
| Native extractor executables | 2 | `build.native_outputs` |
| Installation manifest | 1 | Actual generated installation identity |
| Owner profile | 1 | Actual generated auxiliary identity |
| **Total** | **154** | Exact current prebuilt path/pin set |

The direct copies split into 19 installation files, 45 auxiliary files and
eight documents. Auxiliary files split into 45 fixed noncompiled roles and
72 generated native roles (65 + 5 + 2). `build.noncompiled_roles` gives the
45 fixed role pins and `build.native_roles` the 72 role names. Together they
cover the exact 117 entries of the selected owner profile. Receiver objects
belong to the installation identity, not this auxiliary partition.

The eight documents are README, PRODUCER, LAUNCHER, RECEIVE-POLICY,
BOUNDED-TRANSPORT, EXECUTION-TRUST, CONTACTS and SPARSE-SEARCH. Source paths
for the last four are selected explicitly, not inferred from their destination
names. In particular BOUNDED-TRANSPORT comes from the transport-release README;
EXECUTION-TRUST comes from ordinary_bounded_transport.

## Source and compiler boundary

The 93 build inputs are the exact union of the unchanged lower builder's 47
fixed inputs, the 72 direct-copy sources and all compiler-lane sources. This
union is 3,020,951 bytes. It intentionally retains lower-builder inputs even
where a later direct copy supersedes their staged output. Removing those inputs
would change that builder's contract, outside this selection.

The selected lower builder is `software/v5/ordinary_package/build.py`,
SHA-256 `49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5`.
Receiver, authoring, extractor and query lanes retain their existing ordered
8 / 13 / 7 / 1 module lists, exact source transforms and transformed hashes.
The extractor lane links two separate programs, never both main functions.
The existing public-source header transform and legacy-view transform are
unchanged. This selection does not modify mathematical algorithms, seed,
source interpretation, importer identity rules or compiler flags.

`build.runtime_pins` combines nine unchanged installation/runtime pins with
14 unchanged compiler/linker pins. These 23 pins identify named support in
complete external Windows x86-64 Python 3.14.6 and Lean 4.34.0 distributions;
they are not a hermetic toolchain census. Resource limits and execution trust
remain unchanged. Owner-approved local source is executable code; inert peer
artifacts and process limits do not turn it into a hostile-source sandbox.

## Exact prebuilt versus fresh build

The selected prebuilt contains 39,150,659 bytes. Its exact pins were read from
the current binding-package01 assembly and independently matched against all
154 actual files, including a fresh file census. The 72 selected direct-copy
sources match their corresponding package destinations exactly. Every source
also present in the prior bounded source selection retains its existing pin.

- PROFILE SHA-256:
  `dc0c19b7cf116742caa0751665da93400f6bc5b4663cfe313c3e81aa0d9c58e0`.
- INSTALLATION SHA-256:
  `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.

These are **prebuilt** identities. A fresh source build must derive its own
installation/profile identities from actual output bytes and check the role
closure. Equal selected source does not imply bit-identical native artifacts,
the same implementation identity, or compatibility with an existing owner
state. The new driver must not copy the prebuilt manifests over fresh output.
Historical experiment paths and receipts are audit evidence only, not inputs
required by the distributed build or preparer.

## Minimal operator closure

Eight companion destinations are pinned individually:

- Frozen low-level release-bundle filesystem/JSON/archive helpers. The new
  packer may use these helpers, not historical `known_pins`, `pack` or `verify`.
- Frozen ordinary_multi_source_package preparer, loaded from the extracted
  root by explicit path. Its dependency closure is the standard library.
- Existing basis-query and anchor-query companions, using the selected package.
- Selected offline export at its established `ordinary_selected_export/export.py`
  destination and its unchanged adjacent `selected_export.py` helper.
- Operator and network example JSON documents at their established paths.

The export destination maps to the fresh `export_selected.py` repository input.
Its only intended change is the adopted binder pin, from `d5a9c133...` to
`e4b52c2f...`. The fresh repository input itself is not another supported runtime
entrypoint. Independent review must establish the exact one-pin difference.

Historical high-level packers, selectors, overlay recipes, broad guide trees,
mirror machinery and automated service leases are not part of this closure.
The lease helper hard-pins superseded transport sources; service remains
available through the selected package's existing public `run.py peer serve`
workflow. No new service implementation is selected by omitting that helper.

## Pinning without a circular manifest

The manifest pins frozen build/prebuilt/companion inputs. `release_support`
is an explicit destination-to-source map for the new build, pack, prepare and
guide files plus `release.json` itself. These fresh support files are pinned
by the generated outer archive manifest after source review, not recursively
inside `release.json`. The externally selected outer-manifest digest is the
archive integrity anchor; a self-reported archive digest is not authority.

Source-map closure establishes exact selection, not runtime success. Subsequent
changed-boundary checks remain root-owned: manifest/refusal controls, relocated
offline preparation/public loading and, if selected, one direct source build.
No product import, compiler execution or experiment was performed for this map.

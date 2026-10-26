# Flat current operator and distribution plan

2026-10-26. `practical_library_route`. Source design only; root adopts the map
before bundle/preparer implementation or any runtime. No old source is edited.

## One selection, two independently usable archives

`release.json` selects the exact 154-file prebuilt package, the complete direct
build-input union, unchanged compiler lanes, runtime pins and current companions.
The map owner's current census is 93 build inputs / 3,020,951 bytes; the selected
prebuilt is 39,150,659 bytes. The final exact map, not these prose counts, governs.
No historical overlay, prior archive, experiment directory or old source-manifest
is a runtime input to the new distribution route.

Source extraction contains the selected build sources, common companions,
source support and the release selection. Prebuilt extraction contains
`package/<154 exact paths>`, the same common companions, prebuilt support and
the same release selection. Both have one root README. Existing repository-relative
companion paths are preserved, so `--source-root` always means the extracted root.
The prebuilt extraction need not carry the build source tree. Its README directs
source rebuilding to the separate source archive, not an absent local builder.

`release_support.source` and `.prebuilt` map destinations to repository inputs.
Source support adds current build.py/bundle.py/prepare_selected.py and root README;
prebuilt support excludes build.py. New support bytes are pinned by the generated
outer archive manifest, not recursively by release.json. The release selection
is itself a payload in each archive, not a self-hashed row in its own selection.

## Complete common companion closure

| Release destination | Repository input / dependency |
|---|---|
| `software/v5/ordinary_release_bundle/bundle.py` | Exact frozen file-only primitives, SHA `5a8742bec0c13f3c7e8104111ba883887d5569cbb1a5498d79567e998dcd4d32`; standard library only. Never call its historical pack/verify/known_pins. |
| `software/v5/ordinary_multi_source_package/prepare.py` | Exact inert helper, SHA `77f0bc5c6d02e1a87c29e44d71cbb77de4f1655998b980c9b71eb14085afb2b0`; standard library only, explicitly selected from extracted root. |
| `software/v5/ordinary_basis_query/query.py` | Exact current companion; selected package launcher/full loader and external approved runtimes supply its execution dependencies. |
| `software/v5/ordinary_anchor_query/query.py` | Exact current companion; selected package plus explicit local owner/registered anchor and external runtimes. No historical source tree. |
| `software/v5/ordinary_selected_export/export.py` | Fresh input `ordinary_current_release/export_selected.py`; precisely one old-binder pin replaced by `e4b52c2f...fa19b6`, 19039 bytes / SHA `b0095dd2d6fc64a31334ec106802b444a9bb997ecd5aa09855e00ec83aa98c91`. |
| `software/v5/ordinary_selected_export/selected_export.py` | Exact frozen helper; required **adjacent** to export.py. The fresh repository input alone is not a runnable companion. Package codecs/runtime/custody are explicit external inputs. |
| `software/v5/ordinary_operator_kit/examples.json` | Exact request examples, not executable requests or current package selection. |
| `software/v5/ordinary_network_kit/examples.json` | Exact network examples, same distinction. |

The existing service_plan.py pins old peer_api/http_provider bytes. Root excludes
that optional multi-lease wrapper; use current public `run.py peer serve` for an
explicit finite lease. The inert mirror and old guides are not part of this
selection. Their preserved source/evidence is neither deleted nor promoted.

## Stable small APIs

```text
pack(source_root, output, *, kind="source", package=None, check=None)
verify(source_root, manifest_sha256, *, check=None)
prepare_selected(source_root, package, profile_sha256, request, output)

bundle.py pack --source-root ROOT --kind source|prebuilt [--package PACKAGE] --output FRESH
bundle.py verify --source-root EXTRACTED --manifest-sha256 APPROVED_HASH
prepare_selected.py --source-root EXTRACTED --package PACKAGE --profile-sha256 HASH --request JSON --output FRESH
```

Packing writes `source.zip` or `package.zip`, a fresh `relocated/` exact extraction
and terminal external `RECEIPT.json`. Both extractions contain
`CURRENT-RELEASE-MANIFEST.json`. Results include `kind`, `files`, `relocated`,
`archive`/`manifest` byte-length+SHA pins, and `archive_file`/`manifest_file` names.
The outer manifest records kind, selected release pin, exact payload map,
kind-specific entrypoints, supported runtime profile and undecided license status.
It excludes its own row. Receiver approval of utility/manifest remains external.

The bundle reuses ordinary paths, strict JSON, canonical encoding, bounded reads,
exclusive writes and complete 256-entry census from the one fixed helper. Its
ZIP path uses sorted ZIP_STORED file-only members, fixed metadata, no ZIP64,
exact readback and post-copy source checks. Exact directory census includes empty
extra directories and aliases. No repository glob, overwrite, deletion or retry.
The helper's source-only 2-MiB pin/16-MiB archive policies are not silently applied
to compiled payloads: the largest selected prebuilt file is 5,588,544 bytes.
Use explicit packaging-only bounds (source 2-MiB files/8-MiB total/16-MiB archive;
prebuilt 8-MiB files/64-MiB total/72-MiB archive) without changing product limits.
Confirm both complete entry counts fit 256 before implementation; otherwise
return to root rather than widening the helper. Limits remain cooperative.

## Selector acceptance and authority

Use release `build.noncompiled_roles` (45 fixed pin rows) and `build.native_roles`
(72 fixed names), plus unchanged profile schema/helper-path/author-worker layout.
An explicitly approved actual PROFILE may differ after recompilation. Validate
its complete 45/72 partition, fixed noncompiled pins and actual 45 file bytes;
validate native pin shapes, not native mathematics or binaries. No third
compatibility JSON and no automatic acceptance of merely matching filenames.

Load the selected frozen prepare.py once in a private module, set only its local
PROFILE to the caller's selected digest, and call its unchanged `prepare`.
Do not import product code, open state, execute requests, guess contacts, rewrite
old reports or approve native artifacts. Preserve original report-profile binding,
multi-source receive policy validation, fresh outputs and finite cooperative
allowance. Revalidate selected metadata/helper inputs before successful return.

## Evidence and stop boundary

Root's TEST-PLAN selects exact tree/ZIP/refusal controls, relocated real offline
preparation and a narrow current-export codec load. The existing public loader
and binder tests are reused, not rerun. The direct source build, if needed, is a
separate finite selection with output-derived identities. No source equivalence
claim implies bit-identical compiled outputs or authority over old owner state.
This work closes a distribution gap; it does not prove growth speedup, worldwide
operation or final-v5 completion. All work remains local and unpublished.

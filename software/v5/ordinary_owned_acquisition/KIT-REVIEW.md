# Investigator kit integration review

2026-10-28, query_scaling. **PASS for the selected source-only kit delta.**
This independently reviews root's kit integration and exact file selection,
not this reviewer's transport helper implementations. No product/helper import,
preparer, packer, native operation, owner/database open, network or Git operation
was run. Reading and hashing retained assembly files is not a repeated assembly.

## Exact selection and actual package

`SELECTED-FILES.json` SHA-256:
`8850811b7e1d4108252f79bf36b5d8092433c2b698985c4fbf194cefeffc1746`.

Compared against the adopted
`software/v5/ordinary_contribution_bundle/SELECTED-FILES.json` and the actual
package at
`experiments/v5-local-checks/owned-acquisition-assembly01/distribution/package`.
Both selections have 268 payloads. Independently checked every selected source
or actual package file's length/hash: **zero mismatches**, 42,987,097 total bytes,
below the unchanged kit utility's 64 MiB aggregate bound.

The actual package has exactly 160 files, including ignored/hidden files. All
160 are selected and pinned. Its actual PROFILE is
`85d45c928523c2b96f127ec8c15b2e2664f8428f0c1ef2415470a5b30737d3c8`;
the actual unchanged installation manifest is
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.
All PROFILE payload entries agree with the selection. The 93 current source-map
records all have exact corresponding selected source rows, and all 78 direct-copy
roles match the actual selected package payload pins.

Only PROFILE and the two transport payloads differ from the prior 160-file
package selection. The other 157 package payload pins remain exact. This includes
the entire installation, owner/profile loader, module support and native lanes.
This file identity check does not compute a fresh owner or anchor state.

## Source and helper deltas

Exactly four source snapshot keys are replaced: the two transport helper paths,
source-map path and builder path move to `ordinary_owned_acquisition`. Their
pins agree with the already reviewed map/builder and the selected helper pins.
There are no extra source snapshots or missing map dependencies.

Among keys common to the old/new selections, content changes only in GUIDE,
REFRESH-REQUESTS, REFRESH-USAGE, kit.py, compatibility.json, prepare_selected.py,
PROFILE and the two transport payloads. Exact source comparisons establish:

| Item | Reviewed change |
|---|---|
| `kit/kit.py` | Only PROFILE, SOURCE_MAP path/hash and BUILDER path/hash constants. Same helpers, counts, bounds, manifest rules, copy/verify/archive behavior and external runtime/license claims. |
| `kit/file_helpers.py` | Byte-identical to the selected predecessor; SHA `b5d211a83644b61c6a6fe673785ccd1e1960816a2d58f20787b9d4dfdb3c9da9`. |
| `kit/operator/compatibility.json` | Same 50 direct-source roles and every other logical field; only ordinary_acquisition/fair_exchange pins change. JSON formatting changes do not add a compatibility rule. |
| `kit/operator/prepare_selected.py` | Only MAP_SHA changes to the actual compatibility digest `493e8b76697b23454874887b4449cde8138687b81bf5ba9e2a9b3a5a317ae942`. |
| `kit/REFRESH-REQUESTS.json`, `kit/REFRESH-USAGE.md` | Exactly the old PROFILE literal is replaced by the current PROFILE. |
| `kit/GUIDE.md` | Current PROFILE in its two active positions, current source-build path, and one new ordinary-download boundary paragraph. |

The reusable prepare.py, REQUESTS.json, contribution projector/contract and both
preview helpers retain their previous selection and exact bytes. No preparer
implementation, request schema, source-contribution workflow or preview behavior
changes. Existing math/runtime prerequisites remain required.

The GUIDE's new paragraph accurately states observed closure before configured
fallback, original grants, terminal malformed/TLS/uncertain cleanup, default
no-retry behavior and the default refusal exception-shape change. It explicitly
excludes dynamic dependency-location gateways. The preceding contribution
handoff and compatibility instructions remain intact.

Searched current GUIDE/refresh instructions and actual package Markdown/JSON for
the replaced PROFILE/hash and obsolete active builder/transport-source paths;
no stale active reference was found. Current source-map/build constants in the
kit utility agree with actual reviewed bytes. The unchanged generic file helper
is invoked by kit.py for its bounded file primitives, not as a replacement kit
entrypoint or historical build selection.

## Scope of approval

The exact selection is coherent for root's subsequent finite file-only packaging
step, conditional on the separate helper/source and actual-operation reviews.
This review does not claim an archive has been created or a public workflow has
passed, and does not adopt a new package. No preparer/runtime replay or native
rebuild is justified by these constant and documentation changes alone. The
frozen standalone inert-host distribution remains unchanged.

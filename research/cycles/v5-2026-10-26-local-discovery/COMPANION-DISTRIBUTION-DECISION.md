# Distribute a coherent source workflow, not scattered repository companions

2026-10-26. Source-only decision; no package/import/test/extraction/native/network
operation. Root subsequently reported the service-plan run exited zero; its
independent outcome audit/adoption remains pending and is not assumed successful.
No old archive, default PROFILE, owner state or used source is changed.

## Recommendation

Prefer **one new self-contained source-distribution successor** containing the
unchanged base payloads and the selected companions, rather than a supplemental
ZIP as the main operator handoff. The base is only 3,789,448 source payload bytes;
the eight current additional files total 108,535 bytes. Avoiding that small
duplication is not worth making every new operator manage two roots and resolve
missing guide links. A supplement remains useful later as an optional transfer
optimization, not the first usability improvement.

This is source delivery, not a new mathematical package or native build. Preserve
the old archive and all 143 base payload bytes, create a fresh artifact with a
distinct manifest/receipt, and keep the existing default package/state selection.
Use a new narrowly scoped packaging successor; do not modify frozen `bundle.py`
or invent a generic installer, updater or version-resolution framework.

## What is actually available

The current source utility is
`software/v5/ordinary_release_bundle/bundle.py`, SHA-256
`5a8742bec0c13f3c7e8104111ba883887d5569cbb1a5498d79567e998dcd4d32`.
Its `known_pins` requires 140 selected known payloads; three self/guide/license
files produce exactly 143. `validate_manifest` fixes that count, manifest profile
and entrypoints; `verify` checks the exact selection and full extraction census
(`:205-290`). `pack` has no supplied-file-list or supplement option (`:299-361`).

Therefore simply extracting a companion ZIP into the verified base source root
makes the existing verifier refuse extra files. Keeping a supplement in a second
root preserves verification but breaks existing cross-directory documentation
links. The old utility cannot truthfully be claimed to verify a combined delivery.
Its bounded path/hash/manifest/census/ZIP primitives can be reused in a separately
reviewed successor; its fixed full `pack`/`verify` contract cannot be silently
monkey-patched to change meaning.

The exact baseline association remains:

- ZIP SHA-256 `897a6eb57056b911b200551413c65ce7788ba3d448ff8b6b8c143d883180ebd0`.
- Base SOURCE-MANIFEST SHA-256
  `f1beab01d43e4b5fc6d7b9999ff2795598e3f2ee77c0dc85f1d99e82a15b31f1`.
- Current runtime PROFILE
  `b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7`
  is an existing selected installation, not a required hash for all future builds.

Observed additional inputs below are under `software/v5/`. The first six were
confirmed tracked by `git ls-files`; the two service files are currently untracked
reviewed-source candidates pending the selected execution/adoption. This census
does not authorize packaging them as tested software.

| Relative path | Bytes | SHA-256 |
|---|---:|---|
| `ordinary_selected_export/export.py` | 19039 | `79f61b6d1d52b1bb15130c866909ddbc61e3b1f643a91d3943a631e0fb4f6a05` |
| `ordinary_selected_export/selected_export.py` | 14944 | `49ee6de8c6daa5fb7fd1a445ae7d4c9a1a0312b816697ae4ce6634b504a65eb2` |
| `ordinary_selected_export/README.md` | 7419 | `b0ce7f735af04e29834447a823c6023063d860dd0e4be883ef31aff402bd5126` |
| `ordinary_selected_export/INTAKE.md` | 7479 | `b0d8e19e74fef6167afc7bf432535ea10caf21f8d134b77a4e90229d7ce8bb5e` |
| `ordinary_reuse_workflow/README.md` | 13371 | `0558657ff9cfb32fd5c0ec4f76617a6b43e5a6ee7ad4d61953dfefd50879876a` |
| `UPDATE-AND-RECOVERY.md` | 6003 | `16ac51432c6d05f00e21dc0a228980748cb4938398462425302790d3ff075e32` |
| `ordinary_service_plan/service_plan.py` | 30967 | `3245a5f50d694ef5ca9714c6408e9cfc93b1378606398c433cdda4a4e113ee01` |
| `ordinary_service_plan/README.md` | 9313 | `1c2ff344b62dec784eed7958e6a37c87c4856008a0b5e63af120b9e3a8780668` |

Runtime closure is small: the exporter needs its two adjacent code files and
explicit selected package/runtime paths; the service runner needs its one file
and explicit selected package/runtime paths. Neither needs research directories,
experiment runners, private state, a compiler rebuild or historical generated
package paths. Existing source archive supplies the actual package build chain.

## First true packaging gap: document closure

Do not pack immediately. Existing companion instructions refer to documentation
outside the 143-payload base: export README points to release ADOPTION, update
policy links both release/export ADOPTION and a research decision. Those ADOPTION
files themselves reference experiments/audits. Blindly copying their recursive
link closure would pull research evidence into the operator product and recreate
the repository-navigation problem.

The minimum correction is **distribution-specific navigation**, not another
mechanism: one new top-level start guide identifies the base build recipe, exact
companion source pins, direct intake/reuse/service/update workflows, honest adopted
evidence status, trust assumptions and unresolved license. Provide deliberately
selected local release-status/rationale summaries for essential out-of-archive
links, or fresh distribution copies of the affected guides with corrected links.
Do not edit the frozen originals or pretend broken links are full documentation.
Stop source selection here until root chooses that finite document closure and
the service-plan outcome is actually adopted. No broad bibliography/evidence
tree is required to execute the software.

## Minimum later packaging gate

The fresh manifest should bind the exact original 143-file projection, exact
additional allowlist, top-level navigation and packaging successor, plus the
base ZIP/manifest association. Keep original relative source paths so existing
builders and guide links work. A new full-root verifier must cover the complete
union and reject extras/aliases/changed bytes; the old base-only verifier is not
the entrypoint for this enlarged root. Preserve its original manifest as base
evidence rather than overwriting it with the enlarged manifest.

Count before packing: 143 original payloads + 8 current companions = 151,
before adding the new verifier/entry guide and explicitly selected document
closure. Do not announce a final count while that closure is unresolved.
No native outputs, runtimes, private catalogs, TLS keys or experiment directories
belong in the source ZIP. Keep deterministic stored ZIP entries, fresh outputs,
complete readback, exact extraction census and an externally selected receipt.

One file-only pack/relocation/verify gate is sufficient for this changed boundary,
plus a source-level command/link closure check. Reuse the completed native archive
installation evidence; neither moving a three-file companion nor adding guides
justifies another native build or mathematical campaign. Each companion uses
the operator's actual generated PROFILE; do not freeze the historical PROFILE
into future build instructions or add source acceptance to a report adapter.

A supplemental ZIP would still need its own exact manifest/verifier, base
association and explicit instructions to keep the old verified source root
untouched. It can be a secondary convenience once the full distribution is
coherent. For the present new-operator workflow it saves approximately 3.8 MB
but adds a second integrity/navigation/extraction workflow, so is not simpler.

## Root's selected follow-up and helper-reuse feasibility

Root read this decision and selected the self-contained successor direction.
No packer implementation or execution is selected by this note. A forthcoming
contract will own the final map and evidence gate.

A small successor can load the exact approved old utility source bytes and reuse
only its pure `guard`, `read`, `relative`, `ordinary`, `canonical`, `pin`,
`pin_shape`, `known_pins`, `census` and `validate_manifest`. Do not change its
globals or invoke its whole-root `pack`/`verify` on the enlarged root. The new
utility separately binds the original SOURCE-MANIFEST by its known external hash,
validates the original 143-payload projection (140 known + 3 exact selected
utility/guide/license bytes), and declares a distinct union manifest/receipt.
The stored-ZIP creation/readback loop is small; a second copied 400-line utility
is unnecessary. Existing 256-entry census capacity comfortably covers the
proposed approximately 156 members plus fewer than 45 directories.

Proposed exact minimal payload roles are the 143 original manifest keys, three
unchanged companion code paths from the table, five companion guide destinations
from that table, and three new root-level files: `distribution.py`,
`START-HERE.md`, `DISTRIBUTION-STATUS.md`. Preserve original `SOURCE-MANIFEST.json`
as base evidence; add a differently named complete-union manifest. That map would
contain 154 payloads and two manifests (156 archive members), before any deliberate
contract change. These new filenames/counts are proposals, not created artifacts.

Only guide copies requiring changed navigation/status need fresh source versions,
mapped explicitly to their expected destinations inside the new archive. Their
old sources remain unchanged. Root's top-level START-HERE is authoritative;
historical evidence links may be labelled historical/nonoperational rather than
recursively included. Operator build/runtime selections still use actual fresh
identities, not the historical runtime PROFILE. No old verifier's exact-census
claim or historical successful test is reinterpreted by this projection check.

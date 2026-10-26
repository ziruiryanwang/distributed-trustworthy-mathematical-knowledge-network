# Independent current-release map review

2026-10-26. `current_acceptance_challenge`. Source/data inspection only.

**PASS_MAP_SELECTION_FOR_IMPLEMENTATION.** The proposed flat selection accounts
for the current package, its unchanged compiler inputs and its operator companion
closure. No blocker was found for root to select implementation of the narrow
build/pack/preparer successors. This is one map gate, not approval of future code,
archive output, compilation, mathematical acceptance, deployment or completed v5.

## Exact reviewed inputs

| Input | Bytes | SHA-256 |
|---|---:|---|
| `release.json` | 82,011 | `821796aa5b4996edd3f34babdb3be186d8321e0b3b4208b1e3f18705400caf78` |
| `MAP.md` | 7,530 | `f23c2f04bb4263e58478bf6bc1aa404fb73d1d7400fe8d0e586c9fca61603993` |
| selected lower `ordinary_package/build.py` | 27,225 | `49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5` |
| `export_selected.py` | 19,039 | `b0095dd2d6fc64a31334ec106802b444a9bb997ecd5aa09855e00ec83aa98c91` |

The reviewed prebuilt is
`experiments/v5-local-checks/binding-package01/assembled/package`, with PROFILE
`dc0c19b7cf116742caa0751665da93400f6bc5b4663cfe313c3e81aa0d9c58e0`
and INSTALLATION
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
The updated CONTRACT, TEST-PLAN and OPERATOR-PLAN were read for scope and intended
entrypoint layout. Their plans do not themselves authorize execution.

## Complete package and source accounting

An independent fresh file census and length/SHA-256 reads match all **154 files /
39,150,659 bytes** to `prebuilt.files`. All **93 source inputs / 3,020,951 bytes**
match their declared pins. All **72 direct-copy destinations** match the selected
source bytes and the corresponding prebuilt bytes. All eight companion inputs
also match their declared lengths and hashes.

The reconstructed destination partition is complete and disjoint, including
case-insensitive uniqueness:

| Role | Files |
|---|---:|
| Installation direct inputs | 19 |
| Auxiliary direct inputs | 45 |
| Documents | 8 |
| Receiver `.olean` outputs | 8 |
| Authoring helper outputs | 65 |
| Query helper outputs | 5 |
| Extractor executables | 2 |
| INSTALLATION and PROFILE | 2 |
| **Total** | **154** |

The actual PROFILE's 117 auxiliary entries are exactly the selected **45 fixed
noncompiled roles + 72 native roles**; every fixed role pin matches the actual
payload. The native role names are exactly 13 authoring modules times five
suffixes, one query module times five suffixes, and two extractor executables.
Receiver outputs belong to INSTALLATION, not this auxiliary partition.

The 93 sources are exactly the union of the lower builder's 47 fixed inputs,
all direct-copy sources, and all compiler-lane sources. The fixed list was
checked against the selected lower builder's source declarations; it is also
unchanged from the preserved upper build map. Lower-stage Python/entrypoint
inputs remain present even when a selected final copy replaces their staged
output. Removing them would require changing the lower builder and is outside
this gate. No historical overlay driver or experiment output is needed in this
source-input union.

## Unchanged native meaning; fresh output identities

The ordered **8 receiver / 13 authoring / 7 extractor / 1 query** module lanes,
their sources, five authoring/query output suffixes and two extractor output
names match the preserved upper build selection. The receiver's OrdinaryExport
is the package-specific receiver source, not the authoring source. Extractor
programs have separate main functions and must continue to link separately.

All **29 lane-source transformed hashes** were independently recomputed without
loading project code: identity, the four public-source header transformations,
and the extractor's exact legacy-view header transformation. They match the map.
The post-header source bodies remain unchanged. The nine installation runtime
pins and fourteen extra compiler/linker pins preserve the named-support boundary;
the latter match the preserved upper map. These are not a complete runtime or
compiler-library census. Complete externally supplied runtimes remain a premise.

The map correctly separates exact prebuilt identities from fresh compilation.
A future build must derive INSTALLATION, implementation and PROFILE identities
from its actual outputs. It must not enforce historical binary hashes on newly
compiled objects, overwrite fresh manifests with prebuilt ones, or infer existing
owner-state compatibility from source equality.

## Minimal companion and support closure

The eight common companions include the actual frozen filesystem helper, inert
preparer, basis/anchor queries, export entrypoint and adjacent export helper,
and two example documents. Source inspection of the existing query/export
entrypoints locates their non-stdlib dependencies in the explicitly supplied
package/runtime roots, except the adjacent selected-export helper, which is
included. The map preserves that sibling layout.

Raw-byte comparison confirms the fresh exporter changes **exactly one** binder
hash occurrence from `d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce`
to `e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6`.
All remaining bytes are equal. The repository input `export_selected.py` is
installed as `software/v5/ordinary_selected_export/export.py`, beside unchanged
`selected_export.py`; running the repository input in place is not the supported
release entrypoint. No binder semantics or external-reader audit is repeated.

The stale optional service-plan wrapper is explicitly excluded, not accidentally
shipped with superseded transport pins. The existing public `run.py peer serve`
remains the service entrypoint. Historical packers, selectors, overlay chains and
guide trees are not required by the selected distribution.

The source/prebuilt destination unions contain **106 / 166 payload files** with
no case-insensitive collisions. Including all parent directories and the outer
manifest gives **148 / 194 filesystem entries**, both below the existing helper's
256-entry bound. The source distribution contains its future build entrypoint;
the prebuilt distribution instead contains `package/`. Their common entrypoints
are mapped into both layouts.

Fresh build/pack/preparer/README support is intentionally a destination-to-source
selection, **not yet a claim that implemented support has been hash-reviewed**.
The outer archive manifest will pin the actual reviewed support bytes and
`release.json`; its externally approved digest is the integrity anchor. This is
acyclic. Self-reported manifest/hash values do not establish approval.

## Remaining changed-boundary gates

Root may now select the narrow implementations. Their actual code still needs
review for flat selection, strict paths/census, input rechecks, unchanged native
lanes and output-derived identities. Then select only the relevant archive and
relocated-preparation/export-loading evidence, and a separate direct build if
needed. Reuse the prior mathematical/binder evidence; do not rerun those campaigns.

This review used only source/data reads, hashes and set/byte comparisons. No
product module was imported, no compiler/native program or test campaign ran,
and no state, network, Git index or historical file was modified.

## Adopted-map implementation review

After root adopted the map and selected source-only implementation, the reviewer
read the new pack/preparer files completely, the guide, the changed builder path
and the complete builder diff against its frozen bounded-operations predecessor.
The following source boundary is **CLEAR_FOR_ROOT_TEST_SELECTION**, subject to
the separately reviewed final test/selection inputs. No runtime is selected by
this review, and no successful build or archive is being reported.

| Implemented input | Bytes | SHA-256 |
|---|---:|---|
| `build.py` | 32,799 | `86612e8c76cf7281e942ea9e55705ba53de85d2c6efb45950561532997055d03` |
| `bundle.py` | 14,420 | `437cc3c083d62b2e792ace0d3243552d8c15d02fea6b827ec256dda83829f1bd` |
| `prepare_selected.py` | 6,217 | `8d36fef4c8b50baff5146325ceea83c103c1540b3cbb90b6a8d3c10a71e3bf8b` |
| `README.md` | 13,665 | `d1603614fa5d50dc8414a7721c8e0e99ebd2a62e6fe033aedf97195614839833` |

### Direct builder

The builder consumes the exact pinned release selection and fixed lower builder,
snapshots the 93 inputs plus itself and the release, and checks the fixed-source
union and complete disjoint output-role partition. It uses prebuilt **names** to
check output closure, not prebuilt compiled hashes to qualify fresh artifacts.
The 23 runtime pins retain the exact nine lower-builder pins as a subset.

The extractor/query workers, source transforms, compiler arguments, environment
construction and lower-builder invocation are unchanged. The complete diff shows
unchanged nested allowance, copy and supervision procedures: the inclusive child
Job charge is not double-counted; unknown child CPU charges the original grant
and stops; partial failures remain retained. The author's parse-only AST account
in BUILD-NOTES corroborates the unchanged-function delta, but is not an execution
result and was not used in place of reviewing the changed path.

Assembly validates the actual lower INSTALLATION file map and support digests,
derives its actual implementation ID, and constructs PROFILE from the actual
117 auxiliary hashes. The final file-role census and input/output rechecks precede
PROFILE publication. The resource ceilings, failure policy and PROFILE-last order
are unchanged. The map does not silently change compiler semantics or introduce
a dependency on an old overlay, package or experiment directory.

### Archive and relocated distribution

The packer executes only the hash-pinned frozen file/JSON helper, not its old
high-level selection/pack/verify methods. Every selected fixed source/prebuilt/
companion pin is checked; fresh support bytes and the release are recorded in
the externally approved outer manifest. Relative-path validation, single-link
regular files, no redirected ancestry, exclusive writes, complete case-safe
file/directory census, aggregate byte bounds and input rechecks are retained.

One review defect was corrected before execution: the release selector originally
required compact canonical JSON equality for the approved pretty-printed release.
The corrected path uses strict parsing plus its exact SHA-256; the newly generated
outer manifest still must be canonical. The release bytes and pin did not change.

Root identified a second evidence-boundary issue: the initial relocation was a
matching in-memory copy, not an extraction from the ZIP. The final reviewed source
first writes and inspects the actual sorted ZIP_STORED file-only members, then
creates its **sole relocated tree from that ZIP**. Each bounded member is hashed
before exclusive writing. Exact metadata/content checks, complete relocated
census, original-input rechecks and a final ZIP hash recheck precede the terminal
external receipt. No additional full copy or trial is needed for this change.

The source/prebuilt packaging ceilings differ explicitly so the 5,588,544-byte
receiver object is not rejected by a source-only 2-MiB policy. These are packaging
limits, not widened mathematical/proof/agent resource limits. The verifier binds
the outer manifest to the fixed release and validates every actual payload and
directory; it grants no authorship, native-code, mathematical or license approval.

### Inert selection and operator guidance

The preparer loads the exact frozen multi-source helper from the explicit source
root into one private module. It uses the release's known 45 noncompiled pins and
72 native role names, accepts an explicitly approved actual PROFILE identity,
reads all fixed interface bytes and rechecks release/PROFILE/helper inputs around
the unchanged inert preparation call. It sets only the private helper's PROFILE;
it does not rewrite old reports, change state, run product code or approve native
binaries. Output must be fresh and separated from source/package paths.

The guide uses the materialized sibling export layout, distinguishes source and
prebuilt entrypoints, gives the current direct builder invocation and does not
tell operators to run a historical overlay chain. It distinguishes the preparer's
supported report schemas from direct contribution/publication, warns that example
historical profile hashes are not current selections, and requires actual returned
identities and clean completion evidence. It explicitly preserves owner-approved
local execution, platform/runtime, publication/license and incomplete-v5 boundaries.

Test-source/allocation clearance and observed outcomes remain separate. In
particular, dynamically packed support files must be compared to the reviewed
test snapshots before any relocated companion is loaded; merely generating an
outer manifest does not prove those bytes were the reviewed selection.

## Final file-gate source clearance

**CLEAR_SELECTED_FILE_GATE_SOURCE_AND_ALLOCATION.** The implementation pins above
were reread unchanged. The independent test/selector reviewer
`inert_rehost_relation` completed the distinct harness review; this reviewer
verified its final file pins and incorporated its conclusion without duplicating
the complete harness audit.

| Gate input | Bytes | SHA-256 |
|---|---:|---|
| `test_release.py` | 15,235 | `fc65a4da6149200f16652fe61cfba3cda82efab1f8aa542a744f44f3218f0beb` |
| `select_release.py` | 5,661 | `3a80153e6ad91cde74a5277276e7b0eaa2b285f32d2d7f0a1aa026b23d061781` |

That review found and resolved a source-binding issue before execution: packing
from the canonical tree must not silently substitute changed fresh support for
the reviewed snapshots. The final test compares every release-support payload
against its reviewed snapshot **before** importing a relocated utility, and
rechecks originals and snapshots afterward. It actually imports the verifier
from each relocated distribution, checking helper resolution outside the test
snapshot tree, and performs post-use full-tree verification.

The finite gate covers both exact archives and their sole actual ZIP extractions,
eleven intended refusal codes, the actual inert init preparation's argument/config
bytes and receipt pins, and the selected pure exporter-codec load. It does not
initialize future catalog/custody paths, invoke native code, spawn a subprocess
or accept mathematics. The selector pins source/external inputs before the gate
and requires fresh retained outputs. Its 150-wall/75-CPU-second inner allowance
fits the 180-wall/90-CPU-second, 768-MiB, one-process outer selection. These are
one finite file/inert operation's bounds, not a renewed native/growth campaign.

No source/allocation blocker remains for root's explicit selection of this exact
gate. The direct native build still requires its own separate finite selection;
neither this clearance nor a file-gate pass would constitute that build's outcome.

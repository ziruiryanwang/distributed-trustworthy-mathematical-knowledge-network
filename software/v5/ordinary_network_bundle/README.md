# Build and use the coherent ordinary network source handoff

This source handoff includes the ordinary Lean-first investigator, fair provider
scheduling, one-hop contact discovery, optional sparse pair access, and the
matching offline operator kit. It preserves the original source paths so the
existing bounded build and three file-only overlays can be used without a new
installer or compiler.

This is source-delivery infrastructure, **not the completed worldwide v5 release**.
Source-only implementation is not evidence that an archive, relocation or new
native build succeeded. Later review/outcome records identify any selected actual
checks separately. License remains undecided; see [LICENSE-STATUS.md](LICENSE-STATUS.md).
No external publication is performed or authorized by the bundle utility.

## Exact contents and new entrypoint

There are **136 payload files and one SOURCE-MANIFEST.json**:

| Inputs | Count |
|---|---:|
| Unchanged bounded build, fair overlay and predecessor references | 102 |
| Contact overlay: ten payload sources/documents, assembler and exact map | 12 |
| Sparse overlay: twelve payload sources/documents, assembler and exact map | 14 |
| New operator helper, selector, compatibility map, guide and examples | 5 |
| This bundle utility, guide and license-status document | 3 |

The operator entry is
**`software/v5/ordinary_network_kit/prepare_selected.py`**, explained in its
[START-HERE guide](../ordinary_network_kit/START-HERE.md). Old operator-kit files
are retained only for unchanged authoring/setup instructions and historical
bindings. Their old profile selectors and adoption records do not select this
new interface. Do not follow the old operator entrypoint for the final package.

The fixed allowlist excludes runtimes, native/generated binaries, project owner
state, credentials, experiments, research history and test campaigns. It does
not recursively copy the workspace. Historical evidence paths in retained
documents are identifiers, not promises that their experiment trees are included.
This compact checkout is not the full project/audit archive. Implementation,
review and outcome checkpoint links (including the new kit's IMPLEMENTATION.md)
refer to retained full-project records; they are not required build inputs and
are not shipped in this fixed five-file kit selection.

Supply independently approved Windows x86-64 **Python 3.14.6** and **Lean 4.34.0**
distributions. The existing builders check selected runtime-file hashes; this
is not a hermetic or bit-reproducible compiler guarantee. Other runtime versions
and operating systems are not covered by this handoff.

## Check an extracted handoff before building

Independently approve the archive, utility and external receipt. Verify the
archive hash before extracting into a fresh owner-controlled directory such as
`C:\commons-source`. Select the manifest hash from that approved receipt:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_network_bundle\bundle.py' verify `
  --source-root 'C:\commons-source' `
  --manifest-sha256 'REPLACE_WITH_APPROVED_MANIFEST_SHA256'
```

This checks the new exact file census, fixed inputs, manifest and file hashes.
It imports no product and runs no compiler. A hash shipped with a download does
not authenticate that download, grant a license or establish source safety.
Immutable owner-controlled files are a premise, not a hostile-filesystem sandbox.
The predecessor bundle's manifest format is deliberately not accepted as this
new format. Preserve failed or partial output; do not edit pins to force success.

## Build once, then apply the three existing overlays

Use the same approved source checkout at every stage. All output leaves must
be fresh and their parents must already exist; keep outputs outside the extracted
source. Inspect each terminal report before selecting the next operation.

| Stage | Existing recipe | Input receipt |
|---|---|---|
| Bounded native build | [Build guide](../ordinary_bounded_operations/README.md) | Approved source/runtime selection |
| Fair overlay | [Fair assembly guide](../ordinary_fair_search/README.md) | Actual `_build/BUILD-RESULT.json` from that build |
| Contact overlay | `ordinary_contact_federation/assemble.py` with its OVERLAY.json | Actual fair `ASSEMBLY.json` |
| Sparse overlay | `ordinary_sparse_access/assemble.py` with its OVERLAY.json | Actual contact `ASSEMBLY.json` |

The fair stage uses its documented `--base-build-receipt` flags. The contact and
sparse stages instead both use `--base-receipt`. For example, contact assembly's
manual command shape is:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_contact_federation\assemble.py' `
  --source-root 'C:\commons-source' `
  --base-package 'C:\commons-builds\fair-01\package' `
  --base-profile-sha256 'REPLACE_WITH_APPROVED_FAIR_PROFILE_SHA256' `
  --base-receipt 'C:\commons-builds\fair-01\ASSEMBLY.json' `
  --base-receipt-sha256 'REPLACE_WITH_APPROVED_FAIR_RECEIPT_SHA256' `
  --overlay 'C:\commons-source\software\v5\ordinary_contact_federation\OVERLAY.json' `
  --overlay-sha256 'REPLACE_WITH_APPROVED_CONTACT_OVERLAY_SHA256' `
  --output 'C:\commons-builds\contact-01' --wall-seconds 120 --cpu-seconds 90
```

For the final sparse stage, deliberately select
`ordinary_sparse_access/assemble.py` and its own OVERLAY.json; pass the actual
contact package/profile/ASSEMBLY receipt and another fresh output. Do not pass
the original build receipt or fair profile to that final stage. Finite ceilings
are examples, not success promises. The overlays reuse the exact native bytes
without rebuilding them. PROFILE is committed last, but its presence alone does
not establish successful assembly. Read the actual terminal `ASSEMBLED_NOT_ADOPTED`
receipt and preserve failures. No retry or automatic chaining is installed.

Fresh native builds can have different binary hashes. Use their actual approved
receipts and final PROFILE; never rewrite old evidence or silently substitute a
historical binary identity. File-only source/overlay checks do not establish that
a new native build from this extraction has been executed successfully.

## Use only the final package and matching kit

Follow the [new operator guide](../ordinary_network_kit/START-HERE.md), replacing
its historical local example paths with your own source/runtime/final-package
paths and your final PROFILE hash. Keep the kit outside the package. Its selected
wrapper recognizes the exact contact-and-sparse auxiliary interface, not arbitrary
profiles or native binaries. It prepares request files but does not execute them.
Use the bounded final package's `run.py` for each independently selected operation.

Direct find defaults to atomic V1; sparse V2 is optional. Directory-find can
suggest unknown providers under an explicit short-lived egress policy. Read the
actual operation's RESULT.json, then explicitly approve contacts again for a
later preview or receive. Directory hints, source offers and saved report hashes
never grant permanent connection or source-execution authority. Pair-index creation
is an optional provider cost; an existing enabled index requires its exact original
configuration on reopening, not silent migration or query-triggered rebuilding.

The ordinary research loop remains independent Lean investigation: reuse formal
interfaces, define concepts, study consequences and connections, export selected
work, check it independently, then publish accepted targets. No mandatory global
task list, human-intention predicate or model API is imposed. Search metadata and
source compilation are not mathematical acceptance. Cold checking can require
bounded dependency acquisition; storage, availability and useful growth are not
guaranteed by this handoff. See the included
[launcher](../ordinary_bounded_operations/LAUNCHER.md),
[producer](../ordinary_producer_package/README.md),
[contact](../ordinary_contact_federation/CONTACTS.md) and
[sparse](../ordinary_sparse_access/SPARSE-SEARCH.md) boundaries.

## Recreate this exact source handoff

From a separately approved checkout containing the exact allowlisted inputs:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_network_bundle\bundle.py' pack `
  --source-root 'C:\commons-source' `
  --output 'C:\commons-handoffs\ordinary-network-source-01'
```

Choose an absent output directory whose parent exists. Packing writes only
source.zip and an external terminal RECEIPT.json, using stored ZIP members and
the explicit fixed census. Existing files and partial failures are neither
overwritten nor removed. No archive is created merely by reading this guide.
The utility has cooperative 60-wall/30-CPU-second checks; an enclosing owner Job
is needed for hard process limits. Resource containment is not hostile-source
security isolation. Publication, licensing, release authentication and maintenance
remain separate decisions.

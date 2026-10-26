# Build and operate the ordinary transport-release source handoff

This is the coherent source route to the ordinary Lean-first candidate with fair
provider scheduling, contact discovery, optional sparse search and the repaired
pre-TLS connection/shutdown boundary. It includes a fresh-build-compatible final
assembler and the matching frozen offline operator selector.

**This guide overrides the included historical recipes that stop at sparse
assembly or select `ordinary_network_kit/prepare_selected.py`.** Build once, apply
all four overlays in order, then use
`software/v5/ordinary_bounded_transport/prepare_selected.py` for the final package.
The historical `ordinary_bounded_transport/assemble.py` is deliberately not
included: it binds one old local build instead of a fresh supported build.

This is source-delivery infrastructure, not a completed worldwide v5 release.
No pack, relocation, native build, deployment or mathematical result follows
merely from this guide. Actual selected outcomes are recorded separately in the
full project. [License remains undecided](LICENSE-STATUS.md); nothing here grants
public redistribution or authorizes external publication.

## What the handoff contains

The fixed selection has **143 payload files and one SOURCE-MANIFEST.json**:

| Inputs | Count |
|---|---:|
| Original bounded-build/fair sources and predecessor references | 102 |
| Contact overlay sources, assembler and map | 12 |
| Sparse overlay sources, assembler and map | 14 |
| Network-kit helper, historical selector, map, guide and examples | 5 |
| Fresh transport-release assembler, guide and overlay map | 3 |
| Frozen repaired provider, execution-trust note, final selector and map | 4 |
| This bundle utility, guide and license-status document | 3 |

All earlier 133 fixed inputs remain byte-pinned; seven required files extend the
closure. The earlier bundle's three self/document files are replaced in this new
selection, not modified on disk. No recursive workspace scan chooses inputs.
Runtimes, generated/native binaries, credentials, owner state, research history,
experiments and test campaigns are not distributed. Links in retained documents
to old checkpoints identify full-project evidence, not missing build inputs.
This IMPLEMENTATION/review/outcome history is likewise not part of the compact
payload. The included source paths are preserved for the existing builders.

Supply independently approved Windows x86-64 **Python 3.14.6** and **Lean 4.34.0**
distributions. Selected runtime-file hashes remain checked by the builders and
launcher; this is not a hermetic runtime or bit-reproducible-build guarantee.
Other operating systems and runtime versions are outside this supported profile.

## Verify a fresh extraction

Independently approve the source utility, archive and external receipt. Check the
archive digest before extracting to a fresh owner-controlled directory. Then use
the manifest digest from the approved receipt, for example:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_release_bundle\bundle.py' verify `
  --source-root 'C:\commons-source' `
  --manifest-sha256 'REPLACE_WITH_APPROVED_MANIFEST_SHA256'
```

Verification checks the exact new-format manifest, expected census, fixed input
pins and actual bytes. It does not import product code, run the archive or invoke
a compiler. A hash received with an untrusted download is not authentication,
approval to execute its code, a license or a mathematical warrant. Owner-controlled
immutable inputs remain a premise. Preserve failures; do not edit pins to force
acceptance. This successor does not accept the old network-bundle manifest as its
new format.

## Build once and apply four overlays

Use one approved extracted source checkout and independently approved runtimes.
Keep all operation outputs outside that checkout. Each output leaf must be absent,
with an existing parent. Inspect actual terminal reports before selecting each
next operation; no command below automatically renews a failed allowance.

| Stage | Selected entry/guide | Immediate input |
|---|---|---|
| Native bounded build | [Bounded build guide](../ordinary_bounded_operations/README.md) | Approved source/runtime inputs |
| Overlay 1: fair | [Fair guide](../ordinary_fair_search/README.md) | Actual `_build/BUILD-RESULT.json` and package from that build |
| Overlay 2: contact | `ordinary_contact_federation/assemble.py` and its OVERLAY.json | Actual fair package, PROFILE and ASSEMBLY.json |
| Overlay 3: sparse | `ordinary_sparse_access/assemble.py` and its OVERLAY.json | Actual contact package, PROFILE and ASSEMBLY.json |
| Overlay 4: transport | [Fresh-build transport guide](../ordinary_transport_release/README.md) | Actual sparse package, PROFILE and ASSEMBLY.json |

Fair uses its documented `--base-build-receipt` arguments. Contact, sparse and
transport use `--base-receipt` and the **immediately preceding** ASSEMBLY receipt.
For contact and sparse, follow their included recipes with the actual preceding
package and fresh output; their claims that sparse is the final stage are
historical for this handoff. The final stage is explicitly:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_transport_release\assemble.py' `
  --source-root 'C:\commons-source' `
  --base-package 'C:\commons-builds\sparse-01\package' `
  --base-profile-sha256 'REPLACE_WITH_APPROVED_SPARSE_PROFILE_SHA256' `
  --base-receipt 'C:\commons-builds\sparse-01\ASSEMBLY.json' `
  --base-receipt-sha256 'REPLACE_WITH_APPROVED_SPARSE_RECEIPT_SHA256' `
  --overlay 'C:\commons-source\software\v5\ordinary_transport_release\OVERLAY.json' `
  --overlay-sha256 'REPLACE_WITH_APPROVED_TRANSPORT_OVERLAY_SHA256' `
  --output 'C:\commons-builds\transport-01' --wall-seconds 120 --cpu-seconds 90
```

These finite ceilings are example selections, not success promises. The final
assembler accepts newly selected generated identities only inside the known
supported source/interface/role layout. It checks selected actual bytes and the
immediate receipt chain; it does not validate an arbitrary binary or certify a
compiler run. Fresh supported builds may yield different compiled hashes and
receipts. Use their actual approved identities; never rewrite old evidence or
substitute historical generated pins. Unchanged external-runtime pin policy
still applies.

All four overlays copy existing native bytes without rebuilding them. PROFILE
is committed last, but its presence alone is not success: inspect the actual
terminal `ASSEMBLED_NOT_ADOPTED` receipt and preserve partial failures. A successful
file-only assembly does not establish that a new native build is sound or that
the whole v5 objective is complete.

## Prepare operations with the matching final selector

Use the final transport package and final PROFILE hash. Keep the source-side kit
outside the package. Existing operation-request forms and lifecycle instructions
are in [the network-kit guide](../ordinary_network_kit/START-HERE.md), but replace
every final selector command with the frozen bounded-transport selector below:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_bounded_transport\prepare_selected.py' `
  --package 'C:\commons-builds\transport-01\package' `
  --profile-sha256 'REPLACE_WITH_APPROVED_FINAL_PROFILE_SHA256' `
  --request 'C:\commons-requests\request.json' `
  --output 'C:\commons-requests\prepared-01'
```

This selector uses the included network `prepare.py` helper but recognizes the
bounded-transport auxiliary interface. The retained old network selector is
historical and is expected to refuse the final provider identity. Do not weaken
its compatibility map or swap pins to make it accept. The final selector checks
known noncompiled sources and configuration compatibility; it does not establish
native artifact safety or mathematical acceptance.

Preparation writes inert arguments/configuration and a receipt, without starting
the operation. Select and execute the resulting arguments through the **final
package's bounded `run.py`**, following its [launcher guide](../ordinary_bounded_operations/LAUNCHER.md).
Review actual operation RESULT and supervisor closure, not just a preparation
receipt or printed success phrase. Every service has its own explicit finite
lease and resource allowance; no background daemon is installed by the kit.

## Data, code and ordinary investigation

Read the included [execution-trust boundary](../ordinary_bounded_transport/EXECUTION-TRUST.md)
before authoring or importing projects. Ordinary peer preview/receive exchanges
inert mathematics; Lean/Lake source and compiled-project execution require trust
at the actual account permissions. A Windows Job is resource containment, not
filesystem/network isolation. A project-selection hash does not pin every
transitive artifact or make hostile code safe. Keep checker, runtime, catalog
and checked snapshots protected; arbitrary peer native `.olean` import is not
supported.

Local agents still decide independently what to investigate: acquire warranted
formal interfaces, define concepts, derive consequences and connections, export
selected work, check it independently and publish accepted targets. No global
task list, human-intention acceptance predicate or model API is mandatory.
Source compilation, discovery metadata and popularity never grant mathematical
authority. Direct atomic search remains available; sparse pair access is optional.
Directory hints are short-lived suggestions, not automatic authorization for
later retrieval or source execution. Explicitly approve contacts for each later
operation. Cold acceptance may require bounded dependency acquisition; this
handoff does not guarantee global completeness, useful growth or availability.

The repair bounds owned connections before TLS and charges accepted attempts
against the finite allowance. Shutdown cancels/settles owned work before reporting
quiescence. It does not prevent network saturation, prove parser/runtime safety,
grant per-actor fairness or isolate executable projects. The supported-runtime
and operator-resource assumptions remain visible.

## Recreate the source handoff locally

From a separately approved checkout containing this exact closure:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_release_bundle\bundle.py' pack `
  --source-root 'C:\commons-source' `
  --output 'C:\commons-handoffs\ordinary-transport-release-source-01'
```

Choose a fresh output leaf with an existing parent. Packing writes only
`source.zip` and external terminal `RECEIPT.json`, using the explicit fixed census
and stored ZIP members. It does not execute/extract the archive, publish anything,
remove partial failures or overwrite outputs. Cooperative limits remain
60 wall/30 CPU seconds; hard process containment requires an enclosing owner Job.
Licensing, distribution authentication, independent assurance and maintenance
remain separate release decisions, not consequences of file-integrity checks.

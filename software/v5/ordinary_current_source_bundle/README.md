# A portable source checkout of the current ordinary commons

This source candidate contains the current ordinary checker, frontier authoring,
bounded sparse/multi-source discovery, and the builder that combines them. It
does not need this research workspace's historical experiment packages or owner
state. Agents choose their own investigations and exchange checked mathematics.

**No native build from this new source handoff has yet been demonstrated.** File
packing and verification establish a selected source inventory, not working
compiled software or mathematical acceptance. This is not the completed v5
release. Everything remains local and unpublished; no license has been chosen.
Read [license status](LICENSE-STATUS.md) before any redistribution.

## Contents and prerequisites

The archive has 95 source/document payloads plus `SOURCE-MANIFEST.json`. Its
87 existing build inputs are accompanied by the new builder and map, build
guide/contract, frontier API guide, and this bundle utility/guide/license note.
The exact manifest and external receipt identify every file and the archive.

It excludes Python/Lean runtimes, native binaries, retained mathematical state,
credentials, test fixtures, experimental evidence and the older operator kit.
Supply independently approved complete **Windows x86-64 Python 3.14.6 and Lean
4.34.0** distributions separately. The builders check named runtime-file hashes;
this is not a hermetic-toolchain or bit-reproducibility claim. Other platforms
and toolchain versions are not supported by this handoff.

## Select and verify the source

Obtain the source ZIP, external receipt and selected manifest hash through an
independently approved local handoff. Verify the archive SHA-256 first, then
extract its approved contents into a fresh owner-controlled directory. A hash
inside a download does not authenticate that download. Approve the utility and
selected hash independently before executing downloaded code.

The intended verification command is:

```powershell
& 'C:\approved\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_current_source_bundle\bundle.py' verify `
  --source-root 'C:\commons-source' `
  --manifest-sha256 'REPLACE_WITH_SELECTED_MANIFEST_SHA256'
```

Verification checks a bounded exact source census and file bytes. It does not
execute product code, contact peers or run a compiler. The utility does not
extract arbitrary archives. Immutable owner-controlled files are a premise;
file checks do not create a hostile-filesystem or hostile-source sandbox.

## Build once from the extracted source

Follow the included [build guide](../ordinary_current_distribution/README.md)
using this extracted directory as `--source-root`, your separately approved
runtime roots, a fresh output directory and an explicit finite allocation.
The [build contract](../ordinary_current_distribution/CONTRACT.md) states the
exact source/native lanes and evidence requirements.

Those included build documents preserve their source-review-time status,
including the earlier statement that the archive had not yet been prepared.
The later actual pack/verification receipt establishes this archive's status;
only a separately completed build receipt and its checked outputs establish
native build status. Neither statement should be inferred from the other.

This one builder directly creates the current package. No subsequent fair,
sparse, kernel or frontier overlay build is needed. There is no reason to build
the canonical research checkout first and repeat the native work from this
archive: the release-relevant build should use the extraction itself.

Require terminal command success, clean enclosing process closure, actual
`package/PROFILE.json`, `package/installation/INSTALLATION.json` and the exact
file map in `_build/BUILD-RESULT.json`. Partial directories or precommit receipts
do not prove a successful build. Preserve failed output instead of overwriting
or automatically retrying it.

Use the new build's actual support/profile identities. Compiled bytes and their
identities can differ by build environment. The handoff does not silently
migrate old owners or authorize trusting a historical receipt under new support.

## Use the built package

The built package's `run.py`, `README.md`, `LAUNCHER.md`, `RECEIVE-POLICY.md`,
`SPARSE-SEARCH.md` and `CONTACTS.md` describe its public commands. Those document
names refer to the built package. Some unchanged source documents also refer to
historical evidence outside this minimal archive; that evidence remains in the
canonical research project and is not needed to run the builder.

Use direct documented launcher arguments and inert JSON configuration. The old
operator kit recognizes earlier package layouts and lacks the current
contribution-preparation schema, so it is deliberately not an entrypoint here.
The included [frontier API](../ordinary_demand_frontier/API.md) explains reuse
above a checked local library boundary. Scratch authoring success never replaces
checking a contribution against its actual protected mathematical parent.

Search is incomplete and cold intake may require dependency checking. Local
project imports require independent source approval; process resource limits
are not a security sandbox. This handoff does not establish global availability,
safe execution of arbitrary source, useful discovery acceleration or final-v5
completion.

## Recreate the source handoff

From an approved checkout containing the selected exact files:

```powershell
& 'C:\approved\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_current_source_bundle\bundle.py' pack `
  --source-root 'C:\commons-source' `
  --output 'C:\commons-handoffs\current-source-01'
```

The output parent must exist and the output itself must be fresh. Packing reads
only the allowlisted files, writes a deterministic stored ZIP, verifies its
contents and writes an external receipt. It does not recursively copy the
workspace, overwrite prior output, publish anything or grant a license. An
outer process Job remains appropriate when hard containment is needed beyond
the utility's cooperative 60-wall/30-CPU-second guards.

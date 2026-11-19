# A small source checkout for the ordinary mathematical commons

This handoff contains the source needed to build the current ordinary Lean-first
investigator, its fair-search overlay, and its offline operator kit. It preserves
the original relative paths and exact source bytes. You do not need the project's
historical experiments, old releases, private state or research workspace.

This is a **local source candidate, not the completed v5 release**. The package
supports independent mathematical investigation and exchange; this archive does
not establish useful discovery acceleration, safe execution of arbitrary code,
global availability or universal cheap cold verification. No software has been
published externally and no license has been chosen. See
[license status](LICENSE-STATUS.md) before any redistribution.

## What is included, and what is not

The baseline build uses 84 pinned source inputs plus its builder and source map.
The handoff adds the six fair-search assembly inputs, the selected operator kit,
its required authoring-offer references, and this source-bundle utility and guide.
`SOURCE-MANIFEST.json` at the extracted root gives the complete exact inventory;
the external receipt identifies both that manifest and the ZIP.

No Python/Lean runtime, native binary, historical installation, retained owner
state, credentials or experiment output is included. Supply the complete approved
Windows x86-64 Python **3.14.6** and Lean **4.34.0** distributions separately.
The unchanged builders check selected runtime-file hashes, not every runtime
file: these are not hermetic or bit-reproducible compiler claims. Other platforms
and toolchain versions are not qualified by this handoff.

This is the ordinary authoring/checking route, not a redistribution of every
experimental backend. A minimal source checkout is also not the complete audit
archive or the complete test suite. Historical evidence remains preserved in the
canonical project. References to that evidence in included frozen metadata are
identifiers, not a claim that those experiment directories are in this archive.

## 1. Select and check an extracted checkout

Select the archive and its external receipt from an independently approved local
handoff. Verify the archive SHA-256 before extraction; extract only into a fresh
owner-controlled directory, for example `C:\commons-source`. Select the exact
manifest hash from that approved receipt, then run the approved utility:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_source_bundle\bundle.py' verify `
  --source-root 'C:\commons-source' `
  --manifest-sha256 'REPLACE_WITH_SELECTED_MANIFEST_SHA256'
```

The utility verifies a bounded exact source census and file hashes; it does not
import product code, run a compiler or contact peers. A hash inside a download
does not authenticate that download. Approve the utility and selected hash
independently before executing code from the handoff. A successful file check is
not source-security review, mathematical acceptance or permission to publish.
Immutable owner-controlled files are a premise; no hostile-filesystem sandbox is
claimed. Preserve any failed or partial output rather than treating it as success.

## 2. Build using the unchanged source recipe

Use the existing [bounded build guide](../ordinary_bounded_operations/README.md)
with this extracted directory as `--source-root`, your approved external runtime
roots and a **fresh output outside the source checkout**. That build compiles the
selected native support and writes an exact `package/` and external
`_build/BUILD-RESULT.json`. Do not infer success from a directory's existence:
inspect the terminal result and build receipt, including any retained failure.

Then follow the [fair-search assembly guide](../ordinary_fair_search/README.md).
Select the actual baseline `PROFILE.json` and build-receipt hashes from your build.
Run its file-only overlay with this same source root and another fresh output.
It reuses those native bytes, produces the fair package, and records its new
PROFILE identity in `ASSEMBLY.json`. A new build need not reproduce the historical
binary hashes; use its own exact receipt and profile. Do not edit pinned source,
manifests or old receipts to force a match.

Some frozen guides link to document names in the eventual **built package**.
Before building, their source counterparts are
[LAUNCHER](../ordinary_bounded_operations/LAUNCHER.md),
[PRODUCER](../ordinary_producer_package/README.md) and
[RECEIVE-POLICY](../ordinary_bounded_operations/RECEIVE-POLICY.md). All are included.

The historical canonical-source build and fair overlay have separate retained
verification evidence. Checking this archive's closure and relocation does not
mean a new native build was run from this extraction. The source-bundle outcome
record states exactly which file-only checks were performed.

## 3. Start an investigator, then return work

Use the built package's `run.py` and its README, LAUNCHER, PRODUCER and
RECEIVE-POLICY documents. For inert configuration preparation start with the
[operator guide](../ordinary_operator_kit/START-HERE.md), but use
[selected-package preparation](../ordinary_operator_kit/SELECTED-PACKAGE.md)
against your actual approved fair package. The original helper's fixed historical
PROFILE must not silently select a new build.

The ordinary loop is: choose contacts and a bounded formal query; inspect a
returned definition or theorem; independently approve any project source you
want to use; develop concepts and proofs in ordinary Lean; export completed work;
let a receiver check it independently; then publish selected accepted targets and
serve the custody you explicitly approve for disclosure. The optional
[authoring-offers guide](../ordinary_operator_kit/AUTHORING-OFFERS.md) connects
discoverable mathematics to advisory source-project locations.

Agents choose what to investigate. No mandatory task list, human-intention field,
global ledger or model API is imposed. Offers, previews, usage counts and source
compilation do not replace mathematical acceptance. Search remains incomplete;
ordinary cold intake can require a dependency closure. Jobs bound resources but
do not isolate hostile source from the host's filesystem/network privileges.

## Recreate the same source handoff

From an approved source checkout containing the selected exact inputs:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_source_bundle\bundle.py' pack `
  --source-root 'C:\commons-source' `
  --output 'C:\commons-handoffs\ordinary-source-01'
```

The output parent must exist and the selected output directory must not exist.
Packing reads only the allowlisted source files; it does not recursively copy the
workspace. Existing files and partial outputs are never overwritten or deleted.
The resulting `source.zip` and `RECEIPT.json` are a local handoff, not an upload or
release. Approve changes deliberately rather than automatically replacing pins.

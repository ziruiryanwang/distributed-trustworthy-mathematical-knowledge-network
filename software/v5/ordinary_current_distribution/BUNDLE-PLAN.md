# Smallest source archive successor

2026-10-28. Source-only plan for root selection; no archive or build exists from
the new controller. The candidate builder remains `d14f2910...` and its map is
`65fde356...`. Controls and independent review are separate prerequisites.

Use one fresh `software/v5/ordinary_current_source_bundle/` successor of the
existing file-only `ordinary_source_bundle` utility. This is a fixed selection
update, not a new packaging design. The utility's path, JSON, ZIP, exact census,
readback, retention and resource-guard algorithms need no changes.

## Exact payload

**95 payload files plus SOURCE-MANIFEST.json = 96 archive members.**

- The 87 existing source-map inputs (2,933,782 bytes).
- Five fixed additions: current distribution builder, source map, README and
  CONTRACT, plus `ordinary_demand_frontier/API.md`.
- Three new bundle files: bundle.py, README.md and LICENSE-STATUS.md. The license
  note can be byte-identical to its existing predecessor; it remains a status
  statement, not a license grant.

The build takes 89 of these files (87 plus builder/map). The extra documents
close the build guide's local links without shipping tests, experiment history,
native artifacts, runtime distributions, state or the incompatible old operator
kit. The source archive should be approximately 3 MiB. Its exact size/hash must
come from a later actual pack receipt.

## Utility delta

Change only fixed selection constants/checks and corresponding guide text:

1. MAP and PREFIX select the new map and bundle directory.
2. ENTRYPOINTS contains the new flattened builder only. Remove old overlay and
   operator entries; there is no fair-overlay step after this build.
3. FIXED becomes the five explicit additions, with exact lengths/hashes after
   builder/control review. NEW remains the three bundle-owned files.
4. Require `DMKN_ORDINARY_CURRENT_SOURCE_MAP_V1`, 87 map inputs, 92 fixed known
   files, 95 payload files and 96 ZIP members. Update receipt counts likewise.
5. Preserve the existing 2 MiB individual, 8 MiB payload, 16 MiB archive and
   256-entry extracted-census limits; the smaller payload fits. Verify the actual
   directory closure before selecting the final map rather than increasing caps.

The README describes selection/hash verification, one flattened build from the
extraction, and direct current package launcher/API use. It must not imply the
new controller has already run or the old operator kit recognizes this package.
Keep the known Windows/toolchain profile, local unpublished state and undecided
license. Pin the new utility/guide bytes in root's operation selection as before.

## One release-relevant evidence path

After source review, one file-only pack/controlled extraction/relocated verify
with the new closure and selected-map/missing-file/extra-file refusal controls
is enough for this narrow mapping successor. Do not repeat unchanged ZIP/path
campaigns. The independent test oracle should derive the expected 95 paths from
the reviewed 87-source build map plus the eight explicit additions.

The **next actual build should use that extracted archive**, with its separately
approved external runtimes. Do not first build the canonical source and then
rebuild merely to demonstrate source relocation. This saves a native build while
checking the actual new-operator workflow. Reuse focused native-free controller
evidence and existing source mathematics; inspect the new build's actual support
identities and one appropriate fresh public operation rather than replaying rich
Std grounding or prior network/proof campaigns.

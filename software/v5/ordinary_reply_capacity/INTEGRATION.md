# Reply-capacity package integration

2026-10-28. Source implementation under root's explicit delegation. **No assembly,
build, test, product import, mathematical state access or Git operation was run.**
The provider's source review and control results are separate from this integration;
this document makes no execution or adoption claim.

## Exact candidate files

| File | SHA-256 |
|---|---|
| `http_provider.py` | `929fbf453bb23d353f89384db3dbb8cd4e11e6fd5383a09a36d93fc92631b93b` |
| `assemble.py` | `f27efc29532e9377af01750eec7cc8c0c2f3d7d4a92cdfc1ea08ad0d857b46db` |
| `build.py` | `80c9615f8742d14a7fa2e0b94914268bc1f0735da637f8d666bfb60c5e5f0f2e` |
| `source-map.json` | `05d96f671ecb755b20bcb55d0a93a33a8e70abdaa559017c750635deaba1eef5` |
| `PAYLOADS.json` | `6e249ba771899ec9a9afa4f8cf24f2964d3d08b8329132e7134cf86ce03115c6` |

These are fresh successors of the dedicated-host integration. The selected
provider is 31,972 bytes and is copied to `support/transport/http_provider.py`.
The nine earlier payload origins and pins are unchanged. The provider's eight-line
behavioral addition is documented in [CONTRACT.md](CONTRACT.md) and
[REVIEW.md](REVIEW.md); integration does not change that source.

## File-only assembly

The base remains the **original** `current-distribution-build01` package and build
receipt, not a previous overlay:

- Package: `experiments/v5-local-checks/current-distribution-build01/distribution/package`.
- Receipt: `experiments/v5-local-checks/current-distribution-build01/distribution/_build/BUILD-RESULT.json`.
- Receipt SHA-256: `08ef24292afc45b7cfae7075c0ea2231f45ea88e02cc05bca2dd263f95612863`.
- Base PROFILE: `d5e56dd3bb2d1a531abeaabf06aea1864a7037c88a2035749230574455d7d4b0`.

The assembler continues to require that exact selected receipt/profile shape,
154 base files, original compatibility map, every base file pin and exact census.
It applies the nine retained payloads plus the selected provider and creates a new
PROFILE with the provider role updated. Its required delta from that base is:

- Seven replacements: `LAUNCHER.md`, `PROFILE.json`, `owner.py`, `profile.py`,
  `query.py`, `run.py`, `support/transport/http_provider.py`.
- Four additions: `HOSTING.md`, `advisory_context.py`, `custodian.py`, `host.py`.
- 147 unchanged base files, 158 total output files.

Native binaries, installation manifest and mathematical implementation identity
remain inherited exactly. The assembler preserves fresh-path requirements,
source/base readback checks, output census and failure preservation. It neither
opens owner state nor runs a compiler, product command or service. A generated
PROFILE and `ASSEMBLY.json` would identify assembled bytes only.

The assembler's textual changes from the dedicated-host predecessor are its
description, selection-directory prefix, payload-map pin, additional provider
origin, PROFILE role update and exact changed-file list. The pinned file helper,
original compatibility selection and all checking/copy logic are retained.

## Portable source build

`source-map.json` differs from the dedicated-host map only in the provider's
copy origin and its source key, byte count and SHA-256. It replaces
`ordinary_multi_source/http_provider.py` with this directory's successor. The
91-source closure and 76 direct copies remain unchanged in size. There are no
changes to compiler lanes, transforms, native runtime pins, native outputs,
profile configuration, documentation, build tools or authoring suffixes.

The builder changes only its map prefix and map pin. All derived counts remain:

| Quantity | Count |
|---|---:|
| Installed direct files | 19 |
| Auxiliary direct files | 48 |
| Documentation files | 9 |
| Receiver generated files | 8 |
| Authoring generated files | 65 |
| Query generated files | 5 |
| Extractor generated files | 2 |
| Installation manifest | 1 |
| Payload files excluding PROFILE | 157 |
| Auxiliary PROFILE roles | 120 |

The existing full-build route would select the new provider without rebuilding
an obsolete package first. A full build is **not selected** by this source task;
the file-only assembly is sufficient to integrate this pure Python change into
the retained original build.

## Scope and next evidence

Static source comparison confirmed the stated delta, equal native metadata,
91/76 map counts and all nine retained payload pins. No predecessor was modified.
The separate report-selection companion remains unchanged and outside these
payloads. Root will select a matching compatibility successor against the final
package PROFILE if needed; this integration does not silently loosen its pins.

Independent source review and root's exact finite assembly selection are the next
boundary. A successful assembly would still require inspection of its actual
receipt/delta. Existing provider controls establish their own limited dispatch
claims; they do not imply new mathematical, internet-deployment or whole-v5
acceptance. No native mathematics or reciprocal experiment needs repeating for
this integration.

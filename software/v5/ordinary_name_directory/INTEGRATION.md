# Historical name-directory package integration

2026-10-28, source-only candidate. No assembly, build, import, control execution,
owner access, or product adoption has been selected by this checkpoint.

The package successor replaces `query.py`, `advisory_context.py`, `run.py`, and
`profile.py`; adds `directory_index.py` and `lookup_directory.py`; and regenerates
`PROFILE.json` last. The expected result is 160 files: five changed existing
files including PROFILE, two additions, and 153 byte-identical existing files.
All installation, core, native, compiled-support, and existing documentation
bytes remain those of the adopted 158-file package. The new profile contains
122 auxiliary files. Existing accepted owner roots and installation identity do
not change.

The launcher accepts `query --directory-export v1`. Its value is a literal,
not a path. The existing query allowance and context/catalog/store selections
remain required; directory export forbids custody and uses no name file.
The exporter reads the complete validated historical binding map, closes the
owner, then writes its directory. The profile loader requires both new roles.

The offline entrypoint is `lookup_directory.py`, run with isolated Python
`-I -S -B`. It takes `--profile-sha256`, `--directory`, `--directory-sha256`,
`--symbol-names`, and a fresh `--output`. It uses the approved complete export's
manifest hash and the successor package profile. One to eight exact structured
names form one conjunction. Returned `SPECS.json`, when present, is an explicit
advisory find input; the result is not an old current-owner query report and
must not be passed off under the old report profile. Receiving/admission rules
remain unchanged.

## Assembly input and scope

`assemble.py` accepts `--source-root`, `--base-kit`, `--kit-receipt`, and a fresh
`--output`. It writes `package/` and `ASSEMBLY.json` under that output. The selected
baseline is the existing adopted extraction:

`experiments/v5-local-checks/usable-kit-pack01/packed/commons`

The external receipt is its sibling `packed/RECEIPT.json`. The assembler pins:

- `KIT-MANIFEST.json`: `0b027eedfc768a3dbde08c1b389b19fd316e17cf1cbe6c5b421e5cc735b86ec8`
- Pack receipt: `7443cec2b4159c7c2a66c110cf88c3b1656ce8c9e858e983d646dd7091d9457d`
- Base PROFILE: `c8c8b5971e43361b7b09847b35b0e44c2645b284e59c59b90ab993136ccdb146`
- Installation manifest: `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`
- Bundled base source map: `05d96f671ecb755b20bcb55d0a93a33a8e70abdaa559017c750635deaba1eef5`

It verifies the exact 158-file package census and bytes, binds the external kit
receipt to the manifest, and verifies the bundled old map. It requires the new
map to differ only in the six selected Python roles and five derived counts.
It then copies into a fresh output and rechecks the base, fresh inputs, and output
before writing PROFILE. No historical assembly adapter is executed. Only the
pinned fair-search module's file/path helpers are loaded; its assembly main is
never invoked. The report explicitly claims package-subtree verification, not a
fresh verification of all 260 kit payloads or its archive. Partial outputs remain
on failure. The cooperative allowance is 60 wall seconds and 30 CPU seconds;
an outer finite launcher remains a separate root selection.

## Direct source recipe

`build.py` and `source-map.json` preserve the current reply-capacity direct build
recipe, changing the same six Python roles. The source closure contains 93 inputs
and 78 direct copies; the final payload has 159 files before PROFILE and 122
auxiliary payloads. All compiler lanes, transforms, native runtime/output pins,
fixed compile worker, installation assembler, and nine documentation selections
are unchanged. This route directly builds selected sources; it does not build an
obsolete package or replay historical overlay chains. No native build is selected.

The source map and both `MAP_SHA` constants must be refreshed together after
reviewers close the six payload sources. Root owns that final pin refresh and any
later finite execution/adoption. This checkpoint used only text/JSON inspection,
file authoring, and SHA-256 pinning; it does not report runtime qualification.

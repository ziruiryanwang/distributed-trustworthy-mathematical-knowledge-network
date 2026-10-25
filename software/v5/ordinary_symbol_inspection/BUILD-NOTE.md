# File-only inspection successor

Source-only preparation, 2026-10-24; execution is root-selected separately. This
assembler adapts the preserved ordinary_preview_package/assemble.py file-copy
pattern. It does not compile Lean, run native code, open mathematical state,
serve peers, migrate a catalog or make a mathematical acceptance claim.

## Exact boundary

The only accepted predecessor profile is native-src01:
`fc45893cef624978f0ab5212d0e1e172ff7c71f821124daa8751727bf7123ef6`.
Its fixed owner/loader pins are checked before loading the existing profile.
The same existing loader verifies the package and supplied runtime pins. No new
loader or trust semantics are introduced. The builder utility is pinned to
`49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5`.

The predecessor has no ASSEMBLY.json. Authority is its exact selected profile,
its selected installation manifest, and these separate document pins:

| Payload | Bytes | SHA-256 |
|---|---:|---|
| README.md | 8523 | f425e20490191f3609b72e87ed877e791277568c9a6e094b13feca548d457a86 |
| PRODUCER.md | 5051 | 8904e3e83c0d93880f488c4df0a003b0e499389cdf4bc4915d10b466ca8d4b45 |

Copy 111 auxiliary/profile-selected files, 28 installation files (including its
manifest, excluding externally supplied runtime files), and the two documents:
141 payloads. Only peer.py and peer_api.py change; 139 remain byte-identical.
The new profile replaces precisely those two file pins and is committed last.
The new ASSEMBLY.json records the full output payload map, original profile,
reviewed source pins, installation identity, and exact changed/unchanged census.
Neither record is evidence of successful public use or mathematical acceptance.

The old documents are deliberately unchanged. They do not document inspection;
the new API.md is an adjacent source note, not an extra installed role.

## Invocation contract

Required arguments: `--source-root` (runner source snapshot), `--base-package`,
`--base-profile-sha256`, `--peer-sha256`, `--peer-api-sha256`, `--python-runtime`,
`--lean-runtime`, `--output`, `--wall-seconds`, `--cpu-seconds`.
Run using the selected Python with `-I -S -B` and an external bounded process
envelope; root owns the direct JSON selection. No selector script is introduced.
The source snapshot must include this assembler, the two reviewed peer files,
and software/v5/ordinary_package/build.py at its fixed hash.

The script checks all predecessor and selected bytes before copying, checks each
copy, rechecks predecessor/selected maps, and requires exact bounded directory
censuses of both predecessor and fresh output. Redirected/hardlinked payloads,
case collisions, source/output overlap and preexisting output are refused using
the existing path helpers. Runtime files are validated, never copied or modified.
Sources and selected OS/storage remain immutable-owner premises.

Failures preserve any partial output and add an ASSEMBLY-FAILURE.json if possible;
there is no automatic cleanup, retry or reuse of that output. The first launch
freezes these selected source bytes. A later independent saved-result audit must
check the exact full map and new profile before any public-operation selection.

## Unfinished release integration

This is a file-only successor of a known installed package. The frozen native
source-distribution map does **not** yet include these inspection sources or this
assembly step. A reproducible deployable source release therefore still requires
a separately selected build/source-map integration and corresponding review.
Do not describe this copy operation as a completed source release or final v5.

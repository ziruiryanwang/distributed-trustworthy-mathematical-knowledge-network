# Independent one-pass source package review

Date: 2026-09-22. Read-only PowerShell/.NET byte audit of the newly packaged development source, its fresh installation, and the preserved paged predecessor. This reviewer did not run Python, product code, Lean, a service, or any test, and did not edit the archive, installation, source, or native evidence.

## Decision

**PACKAGE PASS for this exact source archive and installation, not software qualification.** The 112 manifest payloads match the fresh development source, the pristine installation, and the ZIP member bytes and lengths. The ZIP has exactly 113 regular members, including `SOURCE-MANIFEST.json`, with no duplicate, missing, or extra names under ordinal comparison. The install has exactly the same 113 files and no extras. The package result's counts, byte totals, and hashes agree with the observed files. This establishes a coherent source cut for the separately gated native attempt; it does not accept the one-pass service behavior or mathematics.

| Reviewed file | Bytes | SHA-256 |
| --- | ---: | --- |
| `math-commons-source.zip` | 3,666,368 | `6d406e1bd0f9d2e2c5757d99b448ae02e105236a5965a9de7a307f43fe6663c3` |
| `SOURCE-MANIFEST.json` | 20,052 | `1f3c345569bcb511fea67d62d42d457824d10567b08e926af0aa3b9f5779f9a6` |
| `PACKAGE-RESULT.json` | 455 | `7ffffba2a81e20365cd7519c130a3d6a74ee4047880cd8fbdf1fb071fc0ff69` |
| `START-HERE.md` | 2,446 | `aeb18814aba8f1f02224d2b6ffd2b784a1af9d22ff823ecafc508d4f56e40d07` |
| Paged predecessor `SOURCE-MANIFEST.json` | — | `fff9c122f04eae35cc16c0b0754074d07f307c1504838147097fc7f65a3ad6d0` |

The installed manifest is byte-identical to the delivered manifest. The source manifest declares 112 payloads totaling 3,621,056 bytes; those totals and the ZIP length match `PACKAGE-RESULT.json`. The development source contains 115 files: the 112 selected payloads plus `DOC-DELTA.md`, `IMPLEMENTATION.md`, and `PREDECESSOR-SOURCE-MANIFEST.json`, which are intentionally outside the source ZIP. The copied predecessor manifest has the paged manifest hash above. Every selected source file, installed file, and decompressed ZIP member was independently hashed against its manifest row; zero byte-length or SHA-256 mismatches were found.

## Exact predecessor delta

The old and new manifests have the same 112 payload paths. Exactly ten rows changed: `py/peer_service.py`, `py/service_worker.py`, and the eight packaged operator documents `README.md`, `PEER.md`, `QUICKSTART.md`, `AGENT-QUICKSTART.md`, `API.md`, `HOSTING.md`, `RECOVERY.md`, and `CORE.md`. The two changed Python hashes are respectively `c6f11671e16cbe50b2fdc50950e71dbcdb9dc8d049b0d29b1a05f21c2a9b420e` and `629ebe6557128b45e0b37b4d69ece7402b5df3550da34e91ba5c77c947820773`, matching the source review and native plan.

The other 102 payload rows are byte-identical to the paged predecessor. In particular, `py/checking.py` (`13afa1fa31f58f273c0364b9679fd56400587f2977ea24bddd85aad9471f840b`), `py/codec.py` (`d7c61363b82e037d6d7045188e25e22ac02db8605e3efe065821a7d7e6d00c0f`), all three Lean `native/` sources, all 75 `assets/` rows, `py/peer_wire.py`, and the remaining release/build/runtime-interface files have unchanged manifest hashes. This is byte identity, not a new checker or codec correctness judgment.

## Documentation and claim boundary

All eight packaged operator documents were checked for local Markdown links: 13 links resolve to files in the installed package, with none broken. The five local links in `START-HERE.md` resolve to the ZIP, manifest, paged-candidate note, and two experiment documents in this workspace. The changed documents consistently distinguish the preceding paged candidate's scoped same-host qualification from this unqualified one-pass cut. `README.md`, `QUICKSTART.md`, `API.md`, `PEER.md`, `HOSTING.md`, `RECOVERY.md`, `CORE.md`, and `AGENT-QUICKSTART.md` each make that boundary explicit or describe preserved historical claims as provenance. `START-HERE.md` retains the paged candidate as selected and describes the one-pass native-free comparison as preliminary while its independent outcome review, hosting receipts, and Lean follow-through remain pending.

`PACKAGE-RESULT.json` says `DEVELOPMENT_SOURCE_PACKAGED_UNQUALIFIED`, `mathematical_acceptance:false`, `external_publication:false`, and `runtime_included:false`; no signature or license decision is supplied. The archive remains a development candidate. Native launch, if elected, still requires the separately reviewed native-free result, exact source/review pins, and fresh single-attempt preparation and outcome audits.

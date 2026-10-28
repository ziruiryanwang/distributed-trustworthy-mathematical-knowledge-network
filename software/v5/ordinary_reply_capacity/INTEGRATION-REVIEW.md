# Reply-capacity integration: source review PASS

2026-10-28. Independent source/map review. No assembler, builder, test, product
module, native worker, protected state or Git operation was executed. This review
supports a finite file-only assembly selection; it is not an assembly outcome.

## Reviewed candidate

| File | SHA-256 |
|---|---|
| `assemble.py` | `f27efc29532e9377af01750eec7cc8c0c2f3d7d4a92cdfc1ea08ad0d857b46db` |
| `build.py` | `80c9615f8742d14a7fa2e0b94914268bc1f0735da637f8d666bfb60c5e5f0f2e` |
| `source-map.json` | `05d96f671ecb755b20bcb55d0a93a33a8e70abdaa559017c750635deaba1eef5` |
| `PAYLOADS.json` | `6e249ba771899ec9a9afa4f8cf24f2964d3d08b8329132e7134cf86ce03115c6` |

The selected provider is the same 31,972-byte source tested in controls01, SHA
`929fbf453bb23d353f89384db3dbb8cd4e11e6fd5383a09a36d93fc92631b93b`.
Its accounting argument and saved controls are separate reviewed evidence.

## File-only assembly delta

The assembler uses the original current-distribution build, not an overlay chain.
Its actual retained receipt hashes to
`08ef24292afc45b7cfae7075c0ea2231f45ea88e02cc05bca2dd263f95612863`,
lists 154 files and PROFILE
`d5e56dd3bb2d1a531abeaabf06aea1864a7037c88a2035749230574455d7d4b0`.
Its installation manifest is `9112bc5d...` and implementation is `86b6fcce...`.
The code retains exact base receipt/interface/census checks, all base-byte checks,
fresh destination separation, exclusive writes, copy readback, source/base rechecks
and final census/PROFILE creation. A new PROFILE is not yet asserted by this audit.

Compared with the dedicated-host assembler, the only textual changes are its
description and source-directory/map pins, the provider origin, the provider role
in PROFILE generation and the expected changed-file list. All nine prior payload
pins are identical; the tenth is the reviewed provider. The exact required result is:

- Seven replacements: `LAUNCHER.md`, `PROFILE.json`, `owner.py`, `profile.py`,
  `query.py`, `run.py`, `support/transport/http_provider.py`.
- Four additions: `HOSTING.md`, `advisory_context.py`, `custodian.py`, `host.py`.
- 147 unchanged original files and 158 total files.

No selected native file or installation manifest is replaced. Their expected pins
and implementation identity remain inherited from the selected base receipt.
Actual copying and output identity still need the subsequent saved assembly check.

## Portable build map

Independent parsed-map comparison finds exactly one copy-origin change:
`support/transport/http_provider.py` now selects
`software/v5/ordinary_reply_capacity/http_provider.py`. The sources table removes
the old provider's 31,361-byte `d9c342d1...` entry and adds the new provider/pin.
All other source pins are unchanged; counts remain 91 sources and 76 copies.

Every other top-level map field is equal, including counts, documentation, lanes,
native outputs, native runtime pins, profile, schema, tools and authoring suffixes.
The builder differs textually only in `PREFIX` and `MAP_SHA`. Thus the portable
build route selects the same change without changing compilation or mathematical
support rules. A full rebuild is unnecessary and is not selected by this review.

## Matching operator companion

The fresh `operator/prepare.py` is byte-identical to the separately reviewed
report-selection preparer, SHA `203f6249...0892`. This comparison is only a delta
review, not a new independent review of that helper's original implementation.
The adapter differs from `ordinary_report_selection/prepare_selected.py` only in
its exact compatibility-map pin; its own SHA is
`1fa8d9a68cf12aad37a29b542f37f0a064d79d1015a47a007209ca871323f195`.

The companion map SHA is
`86756f2f34c2d73f66985db57bf26f1227eb07c43cf559c31bda6d42ee0506c6`.
Independent comparison confirms 48 direct roles, unchanged 72 generated roles
and exactly one changed direct pin: the reviewed provider at its existing path.
Schema and all other entries remain equal. The helper pin remains exact.

README `aba5dac2...` accurately separates prior-report field extraction from
package/native approval. It also preserves existing host generations' original
PROFILE-bound seals; neither this companion nor the provider change migrates them.
The contribution template retains its earlier bytes (`c934d649...`). The companion
is separate from the 158 package files; no actual new-package adapter call is
claimed. This is the required map update, not a silent weakening of compatibility.

## Disposition

No source or mapping blocker was found for the selected integration. Root may
select one bounded file-only assembly from the exact original build and inspect
its actual delta, followed by a single adapter preparation if still needed.
No new grounding, native build, mathematical replay or service experiment follows
from this source review alone. Full v5 and broad deployment claims remain separate.

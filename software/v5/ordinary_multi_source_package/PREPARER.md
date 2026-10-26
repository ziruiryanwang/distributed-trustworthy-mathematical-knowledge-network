# Public preparer source checkpoint

2026-10-26. Source only; no module import, product execution, state opening,
test or assembly performed by this author. Root owns review/finite execution.

| Fresh file | Bytes | SHA-256 |
|---|---:|---|
| prepare.py | 34599 | `77f0bc5c6d02e1a87c29e44d71cbb77de4f1655998b980c9b71eb14085afb2b0` |
| prepare_selected.py | 5913 | `f0acfe0e718f14ce902c8b97db1508c952931ef3c54edaca5732f3e8309ae00c` |

`prepare.py` is derived from the exact frozen network-kit helper
`bca0979abaf9bb7e8a233b1432b9307bab53a3dd2532654536be5cb4fe5ef811`.
Only the existing preview/receive branch changes:

- For receive alone, presence of any of `acquisition_sources`,
  `attempt_timeout_ms`, `finalization_reserve_ms` requires all three through
  the existing exact-field check. Unknown fields still refuse.
- The selected sources must be a list of 1..8 distinct string labels already
  present in validated contacts. Their exact order and values are preserved.
- Both time fields use the existing strict integer validator with 1..60000
  bounds, excluding booleans. No timeout or source list is inferred.
- The three validated fields are copied into config. With no optional field,
  the old configuration and behavior remain unchanged. Preview and every other
  operation retain their original request schema.

All report predicates, parent-root resolution, exact export identity checks,
state path rules, custody limits, output checks and encodings remain unchanged.
The private helper retains its predecessor PROFILE constant; it is not a
standalone selector for the new package. The supported public entry is the
new `prepare_selected.py`, which sets its fresh private helper's PROFILE from
the explicitly supplied, validated actual package PROFILE before preparation.
No old report becomes new-profile evidence through this operation.

The selector differs from the investigator predecessor only in its descriptive
header, helper location (same folder), helper/map pins, and returned interface
label `multi-source-investigator-v1`. Its CLI, exact 45/72 role partition,
source checking, fresh-output constraints and report/config schema remain.
The selected map is root's
`e3357c5f51819b3086149226d16c887e708324bbfa6774d7b744246d920b0bc1`.

Fresh output texts were read back and matched the intended exact deltas. This
is a source identity check, not syntax execution or behavioral qualification.
Focused public-boundary controls should cover old requests, all optional fields,
partial groups, non-list/empty/oversized/duplicate/unknown/nonstring sources,
boolean/out-of-range times, optional fields on preview, source-map mismatch and
old-PROFILE reports. Do not rerun mathematical or native campaigns for this seam.

# Suffix manifests: independent exact-selection and input-format review

2026-10-26. `kernel_package_audit`. Source and saved-file analysis only.

**PASS_SOURCE_FORMAT_AND_EXACT_SELECTION for the fresh `*-canonical.json`
files below. HOLD for the preserved original `part-a.json` and `part-b.json`:**
each original has one trailing LF that the installed strict manifest parser
rejects. This defect was found before any intake launch; no native allowance
was consumed. The original row selections are correct. The fresh successors
remove exactly that final byte, leaving every other byte unchanged.

This review authorizes no execution. Protected prefix eligibility, runtime
selection and adoption of each actual next root remain separate obligations.

## Exact files and preserved correction

All four files are under
`experiments/v5-local-checks/std-kernel-suffix-inputs01`.

| File | Bytes | SHA-256 | Disposition |
|---|---:|---|---|
| `part-a.json` | 180,918 | `9666347ff646b9bd5a72ea928e479c2a47b5b638a75fc3208a3819200794e810` | Preserved; trailing LF refuses |
| `part-b.json` | 106,732 | `f206b740c95167f166be05fac5416f9e8c117e3ef4bff4d83138f9d26414f310` | Preserved; trailing LF refuses |
| **`part-a-canonical.json`** | **180,917** | **`9eee85273f5fcbc0b91f9f0975c10bfad557b6cb555d334e580499fdf0fedb9c`** | **Exact canonical successor** |
| **`part-b-canonical.json`** | **106,731** | **`a0036d02cc15f0fb5a11d3b02a097870b12b81e963f10db26a9949d6b42b5c5c`** | **Exact canonical successor** |

The reviewer independently hashed all four actual files and compared the fresh
bytes against the complete corresponding original byte array minus its final
`0x0A`. Both comparisons pass. Fresh files end in `0x7D` (`}`); originals retain
their original hashes. Their directory contains exactly these four ordinary
files and no unit directory or copied theorem files.

The original materialized manifest remains
`experiments/v5-local-checks/std-reconstruct01/materialized/manifest.json`,
SHA-256
`1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c`,
independently rehashed unchanged. The units remain referenced at their original
directory. This review did not repeat the previous full unit-byte census or
reparse theorem trees; its preservation claim is the unchanged manifest,
absence of copied units and unchanged selected row identities, together with
the prior exact reconstruction audit. The reviewer wrote no input or unit file.

## Complete row comparison

Both manifests have exactly the fields `batches`, `schema`, `semantic_id`, with
schema `DMKN_ORDINARY_BASELINE_BUNDLE_V1` and semantic ID
`9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7`.
Both values equal the original manifest's values. This is the same selected
semantic identity already validated by the preceding intake's completed
metadata pass; it is not a newly invented mathematical environment.

Every entry has precisely `raw_bytes`, `raw_sha256`, `unit_id`. The reviewer
compared every field of every entry, at its exact array position, with the
following original zero-based, half-open intervals:

| File/batch | Original interval | Units | Raw portable bytes |
|---|---|---:|---:|
| Part A, batch 0 | `[1024,1644)` | 620 | 8,552,756 |
| Part A, batch 1 | `[1644,2048)` | 404 | 8,595,160 |
| Part B, batch 0 | `[2048,2477)` | 429 | 8,899,687 |
| Part B, batch 1 | `[2477,2651)` | 174 | 8,867,997 |
| Total | `[1024,2651)` | **1,627** | **34,915,600** |

The original unique row sequence and these consecutive disjoint intervals
establish uniqueness both within each part and across the pair. No unit is
omitted, duplicated, reordered, split, renamed or assigned a different raw
hash/length. Part A totals 1,024 units / 17,147,916 bytes; part B totals 603 units
/ 17,767,684 bytes. Each subbatch lies wholly within its original batch.

`INTAKE-CONTINUATION-OPTIONS.md` supplies the executed reconstruction's
row-level topological-order induction and the structural-bound inheritance
argument. The current review verifies that these actual files implement those
exact cuts, rather than relying on a merely matching aggregate count.

## The actual raw-input boundary

The installed sources are under
`experiments/v5-local-checks/kernel-admission-package01/distribution/package`.

`owner.py` reads the selected manifest as bounded raw bytes and checks its
explicit hash. It does not trim or normalize that input. The unchanged bytes
reach `reference/baseline_bundle.py:read_manifest`, which calls
`installation/py/ordinary_evidence.py:strict_json` before validating the schema,
semantic identity, entries and limits.

`ordinary_evidence.py:canonical_json` (lines 66-72) uses recursively sorted keys,
UTF-8, separators `,` and `:`, and **no final newline**. `strict_json` rejects
whitespace outside strings at lines 113-116 with `JSON_LEXICAL_TOKEN`, before
also requiring exact canonical byte equality at line 137. The semantic contract
explicitly describes whitespace as `none-including-no-final-newline`.

Therefore the two LF originals would deterministically refuse. General JSON
validity, correct row data and a matching supplied file hash do not repair this
raw-format violation.

For each file, the reviewer independently rebuilt the compact recursively
key-ordered encoding from the validated row data and confirmed that the
original equals exactly that encoding plus one LF. The fresh actual file then
equals that independently rebuilt encoding byte-for-byte. This simultaneously
rules out a BOM, duplicate keys, additional whitespace, missing/extra fields,
changed key order and hidden appended content in the selected new bytes.

The documents contain only the allowed arrays, objects, ASCII strings and
unsigned integers. Depth, token lengths, entry sizes, batch lengths, total
units, total raw bytes and manifest byte lengths are below the installed
default limits; every identity is the original validated 64-hex value. On this
source argument the fresh files satisfy the manifest reader's raw syntax and
metadata conditions. No product parser was imported or executed for the review.
Live budget callbacks, current source/input pins, dependency/context validation
and raw-unit/native admission remain runtime obligations.

## Follow-up check: contribution JSON has a different reader

Root asked whether the prepared contribution's pretty JSON and final LF require
the same correction. **They do not.** Applying the manifest rule indiscriminately
would create unnecessary successor files.

The actual `contribute` branch in installed `owner.py`, lines 495-504, reads:

- `acquired-targets.json` and `output-names.json` through `A._writer_json`.
  That reader explicitly permits noncanonical key order and whitespace; its
  lexical branch allows TAB, LF, CR and SPACE. These actual files contain the
  permitted strings/arrays/objects/unsigned integers. Acquired targets are `[]`;
  the seven output names are ordinary structured names.
- `project-authoring.json` through `owner.project_json` after checking its exact
  SHA-256. This separate local configuration reader allows standard JSON
  whitespace and booleans, bounds depth, rejects duplicate keys and numeric
  values, and delegates exact field/type checks to
  `TrustedProjectAuthoring.from_document`. The actual `meta: false` is the
  intended Boolean, and the document contains no numeric values.

The later `G._outputs` and `G._acquired` calls to `E.strict_json` operate on newly
canonicalized structured-name keys, not on the original pretty input files.
They do not reintroduce a final-LF requirement for those raw CLI inputs.

| Existing contribution input | Bytes | SHA-256 |
|---|---:|---|
| `ordinary_finite_map_effects/acquired-targets.json` | 3 | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |
| `ordinary_finite_map_effects/output-names.json` | 4,558 | `3d23d0a69da5e49ee3fe9de4762e2696cc2df3a91a8493d391138208454739af` |
| `ordinary_finite_map_effects/project-authoring.json` | 467 | `769dbc28ad5a4333168bc5e7df2aa6cb832a9c0d316484e1aa0f96f56a6a2d53` |

These exact input bytes were read and hashed. This is a format-boundary review,
not a new whole-contribution qualification or permission to execute trusted
project source. The existing contribution plan/reviews and future actual parent
requirements remain in force.

## Review activity and conclusion

One initial in-memory comparison incorrectly expected PowerShell's parsed JSON
integers always to be Int64; the parser used Int32 for small values. The review
corrected its own type assertion to accept the two exact integral types and
completed the complete-row comparison. No product defect or input modification
resulted from that local analysis interruption.

All review actions were source reads, ordinary-file enumeration, metadata
comparisons and hashes. No product import, owner/status call, database access,
native process, experiment, Git mutation or input rewrite occurred.

Select only the two exact canonical successors if continuation is later approved.
Keep the original LF files as the preserved prelaunch correction record. Keep
the contribution inputs unchanged: their actual readers accept the present
format. Neither this file-level pass nor the completed original first batch
establishes full rich intake, contribution success or deployable v5 completion.

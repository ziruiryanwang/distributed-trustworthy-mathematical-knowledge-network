# Managed storage distribution selector review

2026-10-21. Independent source-only review by support_screen.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Disposition

**PASS_SELECTOR_SOURCE_ONLY.** The reviewed preparation script constructs the
intended exact 129-entry SDK successor from observed127, preserves the other
distribution-input fields, retains the selected builder/runtime envelope, and
addresses only fresh output names. No concrete selector defect was found.
This is not an executed preparation, build, installed adoption, storage control
result or final-v5 qualification. Root owns whether and when to select those
separate actions.

Reviewed script:
`research/cycles/v5-2026-10-20/Select-ManagedStorageDistribution01.ps1`,
6704 bytes, SHA-256
`2a1839587f786ab1ea941cec3dcebe62c1e38b766de706388564961b1be82480`.

Its single mandatory `ReviewSha256` argument addresses the existing combined
`MANAGED-STORAGE-OWNER-PATHS-REVIEW.md`, 15102 bytes, SHA-256
`19820ac508dbfecddcb80d2919c1c48c28b5473b6987051912f4a33d1d16f2c9`.
That is the expected adopted argument for this source. There is no reference
to a nonexistent separate pin-closure review. This preparation-review note
does not replace that product-source review or cause either script to execute.

## Exact map consequence

The basis input is
`experiments/v5-local-checks/distribution-managed-observed-01-input.json`,
2812285 bytes, SHA-256
`e0f0dc5d63dee0d088b8edd9e61d9a1d1bebbe31d3dde76b53887d1c901f7201`.
Read-only inspection confirmed its 127 SDK rows and their current exact
source lengths/hashes. The selector checks that pinned input, schema/base
role and count before copying every logical row into its ordered map. It
also rechecks every predecessor row's file kind, hash and length before
making any output.

The fixed changes table contains exactly these entries, all beneath
`software/v5/managed_storage/`. The reviewer independently checked each
current source hash against the script's complete hard-coded SHA-256.

| Logical SDK entry | Action | Source SHA-256 prefix |
|---|---|---|
| `v5/client/managed_owner.py` | replace | `6991ac58` |
| `v5/client/serve_generations.py` | replace | `e12f3899` |
| `v5/client/workspace_evidence.py` | replace | `d94e3825` |
| `v5/custody/module_store.py` | replace | `580515e4` |
| `v5/evidence_network/custody.py` | replace | `4264841e` |
| `v5/discovery/discovery_store.py` | replace | `7f3c884b` |
| `v5/placement/ledger.py` | replace | `59f87b93` |
| `v5/placement/advertisement.py` | replace | `13b0ef1a` |
| `v5/placement/lifecycle.py` | replace | `0fa3dcc4` |
| `v5/placement/sessions.py` | replace | `6e07010c` |
| `v5/placement/storage_profile.py` | add | `3b535a33` |
| `v5/placement/storage_paths.py` | add | `e1bcba27` |
| `portable/location/intent.mjs` | replace | `6c30e879` |
| `portable/location/maintained_roles.mjs` | replace | `d69d0b12` |

Nonportable changes receive exactly one `v5/` prefix; the two Node paths keep
their `portable/` names. No `storage_binding.py` or second portable namespace
is added. Logical membership gives 12 replacements and exactly two additions:
127 - 12 = 115 predecessor rows remain unchanged; 127 + 2 = 129 final rows.
Each changed row contains the selected absolute source path, actual current
length and the checked hard-coded digest. The script asserts these counts.

The basis has 106 `v5/` entries, all ending in `.py`. Both additions are Python
helpers, and the replacements preserve that classification. Thus the final
108 `v5/` entries are exactly the 108 preparation sources produced by the
unchanged builder's `v5/`-and-`.py` rule, not merely a count of unrelated
prefix matches. The remaining 21 portable entries are inherited except the
two explicit Node replacements. The generic builder permits up to 141 SDK
rows, so the selected 129 does not cross its source-count boundary.

## Preserved input, builder and runtime

The only assignment to an existing distribution-input field is
`$basis.sdk_sources=$sources`. The other ten fields remain the same parsed
values from the pinned basis: `aggregate_image`, `assets`, `base_manifest`,
`base_role`, `base_root`, `distribution_source`, `lean_runtime`,
`lean_support`, `preparation_template` and `schema`. Serialization creates
new input bytes and a new input hash; it does not claim byte identity with
the old JSON. No foundation/image, native asset, template, Lean support map,
base role, compiler or verifier change is introduced.

The selector separately requires the unchanged builder's exact source path
and digest in the retained input, and hashes the builder itself:

- `software/v5/body_location/distribution.py`, 54824 bytes,
  `eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813`.
- `tools/Run-V5-Check.py`, 5735 bytes,
  `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.

The predecessor build selection is
`experiments/v5-local-checks/distribution-managed-observed-build-01-selection.json`,
8542 bytes, SHA-256
`c3257f270ca3b45bfa5a5c7f88798112dac49d9aaea378913ec1df9f98e3b3f6`.
Its 29 runtime-pin rows contain the old observed input once. The selector
omits only that exact input path, retains and checks the other 28 rows, then
adds the freshly written storage input/hash, restoring 29 runtime pins.
Read-only hashing confirmed all 28 inherited rows. Its interpreter is the
same pinned `argv[0]`, which must remain present in that runtime map.

The generated build command retains `-I -S -B`, the exact builder snapshot
path and `build` mode. Only the new input path/hash and fresh destination
replace their predecessor counterparts. The generated source snapshot map
contains precisely the unchanged runner and builder. CPU 120 seconds, wall
600 seconds, memory 128 MiB, two active processes, and 1 MiB each for stdout
and stderr are exactly the predecessor finite envelope, not enlarged limits.

The unchanged builder still checks the input hash/shape, exact base manifest,
template/foundation/assets, source pin rows and ordinary fresh output, and
performs pinned file copying and release verification. This is identity and
source inspection of the selected build path, not another audit of all
previously qualified builder behavior or a prediction of successful execution.

## Fresh writes and stop behavior

The script requires the canonical current directory and constructs all paths
from the fixed canonical root. Its output boundary consists of:

- `experiments/v5-local-checks/distribution-managed-storage-01-input.json`;
- `experiments/v5-local-checks/distribution-managed-storage-build-01-selection.json`;
- `product-local/v5-distribution-managed-storage-01`;
- the reserved future runner directory
  `experiments/v5-local-checks/distribution-managed-storage-build-01`.

All four names were absent at review time. Before writing, the script refuses
any preexisting output name. The two JSON files use exclusive `CreateNew`,
bounded UTF-8 serialization, flush and close; the parent directory is created
only after both files are written. The actual installation destination is
the fresh child `Mathematical Commons v5`, not an existing candidate.

The preparation script does not invoke Python, the check runner, builder,
service, prover or a shell command. It writes the two instruction files and
creates the empty installation parent, then reports `build_executed=false`.
No predecessor input, source, installation, evidence or credential is written,
deleted or migrated. A partial preparation failure can leave its newly
created files; the script stops rather than overwriting or cleaning them on
a retry. Ordinary private-workspace/no-concurrent-substitution premises
remain; this is not an adversarial filesystem transaction mechanism.

## Evidence scope

Canonical guard passed. Work consisted of reading the selector and relevant
unchanged builder sections, parsing existing JSON/source as data, checking
logical membership, lengths/hashes and output absence, and writing this
assigned checkpoint. The selector itself was not invoked. No generated
storage input/selection, build, import, product control, database read,
credential access, deletion or Git operation occurred.

The prior combined source review remains adopted and sealed; no repeated
whole-source review or passed campaign was performed. Root's separate tiny
Python and Node controls, if selected and run, need actual saved-output
review after terminal notice. Their success is not inferred here and the
reviewer must not rerun them to obtain evidence.

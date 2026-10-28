# Incremental-host kit: saved pack outcome

2026-10-28, query_scaling. **PASS for the completed file-only pack, exact archive
and extracted-byte census.** This independent audit read saved evidence and file
bytes only. No pack rerun, product import, preparer execution, database/owner
access, native work or Git action occurred. The separate public host workflow
and its live state were not inspected.

## Exact completed artifacts

Run root: `experiments/v5-local-checks/incremental-kit-pack01`.

| Artifact beneath run root | Bytes | SHA-256 |
| --- | ---: | --- |
| `packed/commons-local.zip` | 43,088,921 | `933a5f7d797be2184cf89958c0a05cac8ff4baa536a59f11ce280167e598a07f` |
| `packed/commons/KIT-MANIFEST.json` | 38,498 | `efeb28150e429f6bcb0e41db2070183b21fd1395c426aca317dd62b31593eecd` |
| `packed/RECEIPT.json` | — | `2e30bfa10af4b47770d2d190aa2b2564d2cd9dd56b0d0474836efa2e17d24301` |
| `RESULT.json` | — | `4786f58515d5f83a53ab74dd12c404ac20e9e162c9c28475c99e41b122528abe` |
| `selection.json` | — | `b9fcfcab8119ae9c448761e920b19be71c72416bde0e75adb3f89788692b59c2` |
| `command/command.json` | — | `43d6d96a14fbafb9684813b86867c3e9459566b843775fb56fc1af55aba3c3ff` |
| `command/stdout.txt` | 774 | `30d7f5b900b99289e6ca6be4e6efc21f3ed01e8e5e41a7e7890d625c0bddb83f` |

The payload selection is
`software/v5/ordinary_incremental_host/SELECTED-FILES.json`, SHA256
`a1c7402e71d9f399a374215454cd31a51d5790c4fae0b578449be9116ab1ee1e`.
Its prior independent source review is `KIT-REVIEW.md`, SHA256
`af6fc9e32ab4d5129aa4bb36beaac65dd232d96abe9e94a349dcb30df5ef8216`.

## Independent byte and evidence checks

The receipt reports `PACKED_AND_RELOCATED_LOCAL_KIT` and its nested verification
reports `VERIFIED_LOCAL_KIT_BYTES`. Parsed stdout equals the saved receipt. The
actual archive and manifest lengths/hashes match both. All 266 manifest rows
match the exact selected sizes and digests: 160 actual package payloads, 93 mapped
sources, two map/build recipes and eleven companions.

I independently hashed every extracted payload and every archive entry stream.
Both have exactly those 266 payloads plus KIT-MANIFEST.json, with no missing or
extra paths. All 267 archive names are distinct even under case folding, and
all entry lengths/digests match the manifest or its exact external pin. Entries
have equal stored/uncompressed lengths, totaling 43,042,873 uncompressed bytes.
The extracted tree also has the exact implied directory census and no reparse
entries. No extraction was performed by this audit.

The embedded package PROFILE remains
`e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13`,
and installation remains
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.
The manifest retains the local/unpublished, no-new-mathematical-acceptance claim,
undecided local-only license status and explicit Windows/Python/Lean external
profile. Native payloads are the unchanged selected files, not a new native build.

The saved run's four source snapshots and their canonical originals all match
the selected utility, helper, payload-selection and supervisor pins. Its three
explicit Python runtime files also match their saved pins when read for this
audit; that does not establish a hermetic toolchain. The saved command arguments
and limits match RESULT's command report, and RESULT binds the exact selection
hash above. The command is the single selected `kit.py pack` invocation.

## Closure and cost

Saved status is `COMMAND_EXITED_ZERO_AND_CLOSED`: child exit 0, direct child
reaped, final active processes 0, Job closed, no cleanup errors, no requested
termination and no terminated process. Actual log lengths match the supervisor:
774 stdout bytes and zero stderr bytes.

Known cost is **2.0 CPU seconds**: 1.859375 Job CPU plus 0.140625 wrapper CPU.
The separately reported 0.046875 supervision subtotal is already within wrapper
accounting and is not added again. Total saved wall time is 6.1748854 seconds;
the command-through-cleanup subtotal is 6.1671892 seconds. Peak Job private commit
was 147,279,872 bytes. These are this pack's saved measurements only; they exclude
the independent byte audit and other workflows.

## Scope of the pass

The receipt's relocation label means archive extraction and byte verification.
**No new relocated find-preparer execution was performed or is claimed.** Its
unchanged behavior evidence is reused as justified in KIT-REVIEW; the exact new
operator/profile pins are covered by the static review and actual payload hashes.

This pass does not establish the public init/append/serve workflow, mathematical
acceptance, producer efficiency, public deployment, a new source/native build or
full-v5 completion. Those retain separate outcomes and decisions. Root owns
adoption; no further pack or relocation run is needed for this completed boundary.

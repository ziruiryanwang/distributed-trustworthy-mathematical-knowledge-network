# Consolidated candidate: actual file-only installation outcome

2026-10-21, independent outcome reviewer core_release.

**PASS_EXACT_CONSOLIDATED_DIRECTORY_BUILD_AND_CLEAN_CLOSURE.** The selected
121-source union is installed at
`product-local/v5-distribution-consolidated-01/Mathematical Commons v5`.
This is exact installation evidence, not the pending installed restart smoke,
new mathematical acceptance, physical-storage qualification or final v5 release.
Root owns adoption and any subsequent finite launch.

## Exact actual evidence

Paths below beginning `distribution-` are under `experiments/v5-local-checks/`.

| Artifact | SHA-256 |
|---|---|
| `distribution-consolidated-build-01-selection.json` and run's identical saved `selection.json` | `75b26bd551f993dece152682024b7de5ead55effdc53a1d1c00045f09cc1ff3e` |
| `distribution-consolidated-01-input.json` | `8ba3707236c1a6e01ab7f87886814f801034b2fe9144ad9603585adcc73feb33` |
| `distribution-consolidated-build-01/RESULT.json` | `7fd26c953d5755744c2333c37e0228d904c95f8ced82ae8d0fd5626ecaf66dbc` |
| `distribution-consolidated-build-01/command/stdout.txt` | `f80130e610ddc916823b776f9339722a495d8031f84a2752f0980405e48f2664` |
| Installed `V5-RELEASE.json` | `1fd0ae63faa84cc1f3ef82f17d2056657f8d6a3e5dea3686ace433987bd1e5be` |

The selected and actual argv agree: retained isolated Python executes the
unchanged snapshotted builder with `build`, exact input/digest and fresh selected
destination. Actual command cwd is the canonical project root. Both selected
source snapshots match their reviewed pins: outer runner `44a7bf1b...` and builder
`eb1348f6...`. No source overlay, proof build, native invocation or existing
installation migration appears in this command.

## Installed map and payload identity

The actual stdout is `DIRECTORY_CREATED_AND_EXACTLY_VERIFIED`, with
`mathematical_acceptance: false`, the selected destination and the manifest
digest above. Its **9,866 payload files / 842,568,302 payload bytes** agree with
the actual manifest census and sum; the release manifest itself is separate.

Independent metadata checks verified:

- All 121 input SDK keys map to exactly `sdk/<logical-key>` in the installed
  release, with identical source lengths and SHA-256 values.
- The input differs from the fixed 114-row basis by precisely the five
  replacements and seven additions in `CONSOLIDATED-SOURCE-MAP.md`
  (`b6ec6126...`), leaving 109 basis SDK rows unchanged. Every non-SDK input
  field remains identical to that basis.
- The 121 rows comprise exactly 100 v5 Python and 21 portable files. Installed
  preparation contains exactly those 100 Python source pins, without duplicates
  or omissions; every preparation length/digest equals its installed file row.
- The installed manifest's `build_input_sha256` matches the actual input, its
  actual hash equals stdout, and the actual result binds the exact selection.

Per `CONSOLIDATED-LAUNCH.md`, this audit **reuses the builder's completed whole
payload validation** rather than rehashing another 842 MB. The reviewed unchanged
builder checks the input and selected source pins, copies with exact pinned
length/digest verification, writes its manifest, then calls
`verify_release(..., full=True)` before returning success. That routine validates
the manifest, performs the exact directory census, checks every payload pin and
checks the exact inherited base-role projection. The source snapshot executing
that path is hash-bound above. This audit independently checked small evidence/
manifest/source identities and all SDK/preparation metadata; it did not run a
second installation, verification command or prior test campaign.

## Resource and closure outcome

The outer result is `COMMAND_EXITED_ZERO_AND_CLOSED` with child exit 0. Its
original selected limits remain 120 CPU / 600 wall seconds, 128 MiB, two
processes and 1 MiB each stdout/stderr.

| Observation | Actual |
|---|---:|
| Worker Job CPU, user plus kernel | 62.46875 s |
| Outer wrapper CPU | 1.578125 s |
| Combined known CPU, without nested double count | 64.046875 s |
| Outer wall time | 308.51123770000413 s |
| Command wall through cleanup | 308.3984648999758 s |
| Peak Job private commit | 56,537,088 bytes |
| Stdout / stderr | 353 / 0 bytes |
| Final active / terminated processes | 0 / 0 |

The 1.296875-second inner supervision figure is included in the outer wrapper
scope, not added again. Direct child reaped and Job closed are true; cleanup
errors are empty; no termination was requested. These are operation observations,
not a universal runtime or RAM claim.

## Remaining scope

The combined installed restart/discovery smoke remains separately selected and
unrun by this audit. Existing sharing, native reuse, continuing context and
placement evidence is reused, not relabeled as a new test of this installation.
No trust policy, owner warrant or retained experiment state was adopted. The
new bounded-generation source work is excluded from this installed release.
Full deployable v5 remains unfinished.

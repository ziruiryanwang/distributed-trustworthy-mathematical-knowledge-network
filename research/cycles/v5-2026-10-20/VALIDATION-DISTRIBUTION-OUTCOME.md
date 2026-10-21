# Combined validation/discovery distribution: independent actual outcome

Date: 2026-10-21. Reviewer: adaptive_audit. Disposition:
**PASS_SELECTED_FIVE_REPLACEMENT_DIRECTORY_BUILD**.

The selected operation produced the expected exact successor installation and
closed normally. This is a distribution-integrity result, not mathematical
acceptance, a full-workflow speedup, useful-growth evidence or final v5 release
acceptance. Root owns adoption and any separately selected installed workload.
No additional import, build, proof or mirror operation was run by this audit.

## Scope and exact identities

The root-selected build was session `44813`, operation
`experiments/v5-local-checks/distribution-validation-build-01`, governed by
[VALIDATION-DISTRIBUTION-LAUNCH.md](VALIDATION-DISTRIBUTION-LAUNCH.md).
Its terminal notice preceded examination of actual results.

New installation:
`product-local/v5-distribution-validation-01/Mathematical Commons v5`.
Predecessor:
`product-local/v5-distribution-body-custody-01/Mathematical Commons v5`.
Neither the predecessor installation nor its used states was modified.

| Object | SHA-256 |
|---|---|
| New installed `V5-RELEASE.json` | `728d12fca7152b2043936b6e9939fd4e0a935f2f006750c9ea639fcdcc2fb216` |
| New `distribution-validation-01-input.json` | `d11abac9a9c5a5ac7d7b22efbf26bb04fcad1e886f19a2195d42060dd44ab565` |
| Retained build `selection.json` | `823098b1b46087d3ce737623c06ae839c820718973ac82447dcd381157d9bbac` |
| Predecessor installed release | `8e93486cadb5806d6470d7a8920803a9a4bad39260dd72f3be3498f699eeeb1e` |
| Predecessor build input | `995525c5cbf2746718cbf583a3e3e401bc56c2f88d1cef8664ffeb1b644454be` |
| Unchanged installed `distribution.py` builder | `eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813` |
| Unchanged `tools/Run-V5-Check.py` runner | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |

The complete selector source had already been reviewed without a blocker:
`Select-ValidationDistribution01.ps1`, 6,136 bytes,
`94702a0a71cdbfb90525b6e19f550070da6a927c283cd5c0c3f2e9ea03204b0d`.
Its five-source map is `VALIDATION-DISTRIBUTION-SOURCES.json`, 512 bytes,
`1c7b7f60fb81ab35eb012eb5ece5103424a12381fb0b35141f828c194748d02a`.

## Complete map comparison

There are exactly 114 SDK entries, as in the predecessor: five replacements,
109 unchanged entries, no additions and no removals. All 114 installed SDK
files and their selected original source files were independently size-checked
and rehashed against the input and release map, with zero mismatches. Their
combined size is 1,403,974 bytes.

| Installed relative path | Old bytes | New bytes | New SHA-256 |
|---|---:|---:|---|
| `sdk/v5/admission/trust.py` | 10,480 | 13,774 | `c997d2a83ae5246dec9ff30eeca72e405ec0f66c0a307e53e0521eef66fae6d0` |
| `sdk/v5/admission/pin_phase.py` | 3,187 | 3,719 | `76b54eb04fa2a66ec598b8c6d668e675d8bd483809f8fa66448fa7319b82a9ce` |
| `sdk/v5/client/located_queries.py` | 23,155 | 23,902 | `4ffb84789deefb524f7f290b2a8879e3b9a1eadc0febf53ad2f5e1a3e168c66a` |
| `sdk/v5/discovery/module_export_adapter.py` | 14,770 | 16,182 | `c7fde37659753a9238506d399e0be5c44ebb5e3a012b5a681dfa1a1551884fd1` |
| `sdk/v5/client/direct_contacts.py` | 19,214 | 19,788 | `1f4224808ceb65feff3fd80353a3dbea3923e2ad091e7c435193fd82f4dc54c8` |

Both complete release payload maps contain 9,859 files. Exactly these five
entries change; 9,854 are unchanged. No payload path was added or removed.
Payload size increases from 842,430,650 to 842,437,209 bytes: the 6,559-byte
difference exactly equals the five source changes above.

Independent actual installation census found 9,860 files including
`V5-RELEASE.json`, payload sizes totaling 842,437,209 bytes, and zero extra
files, missing files, size mismatches or reparse points.

Only `sdk_sources` differs between the build inputs, in those same five rows.
Among release top-level fields other than `files` and `preparation`, only
`build_input_sha256` changes. The 93 preparation source pins contain no
duplicates, missing entries or binding mismatches; only the same five rows
change. All other preparation fields are unchanged. The source snapshots of
the builder and runner were independently rehashed against their origins,
without mismatch.

Unchanged release metadata includes:

- Schema `DMKN_V5_DIRECTORY_RELEASE_V3`.
- Base role `mathematical-client-location-v1` and base manifest
  `a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`.
- Aggregate image
  `99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60`.
- Aggregate, foundation, frontend, image, native and receipt role mappings;
  SDK destinations and Lean support metadata.

### Assurance boundary

This audit compared the entire payload map and actual file census/sizes, but
did **not** redundantly stream and hash all 842 MB of unchanged asset payload.
It independently rehashed the SDK sources/installations and installed builder.
The exact unchanged builder's successful full verification is the actual
whole-payload hash evidence. The runner checked its 29 runtime pins before
and after execution; this audit does not claim a separate rehash of every
runtime binary. These distinct evidence sources are not interchangeable.

## Actual result, resources and closure

The complete stdout, stderr and terminal result were read. Stdout is one
351-byte JSON result reporting `DIRECTORY_CREATED_AND_EXACTLY_VERIFIED`,
`mathematical_acceptance=false`, 9,859 payload files, 842,437,209 bytes and the
new installation/release identity above. Stderr is empty.

The terminal result is `COMMAND_EXITED_ZERO_AND_CLOSED`: child exit zero,
Job closed, direct child reaped, no active or terminated processes remaining,
two lifetime processes, no cleanup errors and no termination request.

| Measurement | Actual |
|---|---:|
| Job user CPU | 31.875 s |
| Job kernel CPU | 28.375 s |
| Job total CPU | 60.25 s |
| Outer wrapper CPU | 1.546875 s |
| Known total CPU | 61.796875 s |
| Overall wall time | 294.9408837999217 s |
| Supervision through cleanup | 294.8437173999846 s |
| Peak Job private commit | 57,348,096 bytes |

The 1.25-second supervisor CPU measurement is a subinterval of wrapper CPU,
not an additional charge. Original limits were 120 CPU seconds, 300 wall
seconds, 128 MiB, two active processes and 1 MiB for each log. No limit was
renewed. Completion was close to the original wall cap; it does not demonstrate
a robust timing margin or justify repeating this build.

Retained evidence inside the operation:

| File | Bytes | SHA-256 |
|---|---:|---|
| `selection.json` | 8,518 | `823098b1b46087d3ce737623c06ae839c820718973ac82447dcd381157d9bbac` |
| `RESULT.json` | 2,224 | `6d279ac48c3dcd70c2563b1cdb398a0458aa56ae024a4b0383dea844b572a2e3` |
| `command/stdout.txt` | 351 | `51ba50b4d243096ca4770f44e23e9fc7a4bf03829b79cfaed5db90195b65fdf7` |
| `command/stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Consequential decision and preserved limits

The installation contains exactly the two validation-phase successors covered
by [VALIDATION-PHASE-OUTCOME.md](VALIDATION-PHASE-OUTCOME.md), SHA-256
`74c541489862cd39521602c5d644cf96a0f616b72ba6c42dcbdf24813e10e94a`,
and the three planner successors covered by
[PAIR-PLANNING-OUTCOME.md](PAIR-PLANNING-OUTCOME.md), SHA-256
`0392fd309d3eb454358160c4e054a988804d7ba30dee78fe71914e51030eefd9`.
This build verifies their distribution binding, not their combined installed
mathematical workflow.

The validation change retains its synchronous phase and trusted stable local
filesystem assumptions; it is not concurrent-rollback protection. The planner
result retains the larger-summary tradeoff and finite committed-corpus scope.
Neither result establishes whole-workflow efficiency or full-cost growth.

The original mirror01 failure remains failed and charged, as recorded in
[MIRROR-METHOD-OUTCOME.md](MIRROR-METHOD-OUTCOME.md), SHA-256
`c37d3d9141224d338b6d16900b1ab5b1296b9416e3f86b641dbed6b5209d41c8`.
No new certificate, trust adoption, mathematical authority or automatic retry
arises from this build. No decision-changing distribution blocker remains;
root may decide the next separately bounded installed workflow without
another import-only test or repeated component campaign.

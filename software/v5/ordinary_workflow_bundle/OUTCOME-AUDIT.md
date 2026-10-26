# Independent outcome audit: workflow-source-controls03

2026-10-26. Disposition: **FAILED; HOLD for the full workflow controls.**
The one actual pack completed and its exact source projection is independently
confirmed below. The test then failed in its extraction census before the public
relocated verifier. This is not a passing suite, a release, a native build, or
mathematical/network qualification. Preserve the failed reports and all used
bytes. No rerun, repack, product/test import, or Git mutation was performed by
this audit.

## Evidence and binding

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Evidence root: `experiments/v5-local-checks/workflow-source-controls03`.
The original and retained selection agree at SHA-256
`8e0a666ee576dafb8ec8727366d7931906f89825f4c677c3f6ac8da6462a4ed0`.
Independent read-only checks found all 154 selected canonical source originals
and their 154 snapshots match the selection, and all 157 external pins match.
Those external pins cover 153 actual canonical pack inputs, the original base
archive, and three Python runtime files. The test ran from its snapshot but used
the explicit canonical utility/source root. Do not describe the pack as having
read every input from the snapshot. Immutable owner-controlled canonical inputs
and the runner's before/after binding checks remain assumptions.

Important used source hashes:

| File | SHA-256 |
|---|---|
| `bundle.py` | `ceae62463c13dccd3a58faea0b8548d1454e09de3877b8058303dd51619b10c7` |
| `test_bundle.py` | `91c5226002e5b02eb42e21e14ae6bc16881929ffff67894258c03263f99f588f` |
| `TEST-PLAN.md` | `de1cdd762f36ab056f0171934e4db68af60cbbcedeb6373eda240849b99d8213` |
| `tools/Run-V5-Check.py` | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |

Important retained evidence hashes:

| File, relative to evidence root | SHA-256 |
|---|---|
| `RESULT.json` | `0ef6ab1e2755d4b4a76d2bd3eb42f302a6094d8dbd4a7e7f74047a5a03910510` |
| `suite/RESULT.json` | `768ddbf4ea01a4f77d862950838d8b0eec3fb241244ac8c0c7b5ede1e863dad3` |
| `suite/packed/RECEIPT.json` | `a807b5d365439457c3b2194838f6e5887ac5d71f19c3be6ee4308c6d2f0250a3` |
| `suite/packed/source.zip` | `46913cfd1c957720a673ec4a41f770bbcd10a489a04c176ca7bdbcbae5e39c49` |

## What actually completed

The test has exactly one completed group,
`actual_pack_complete_union_and_base_projection`. The actual public pack
command has `attempts: 1`, and emitted
`PACKED_WORKFLOW_SOURCE_NOT_BUILT`. Its parsed stdout equals its saved receipt.

An independent read-only ZIP examination, without running either bundle helper,
confirmed:

- 155 archive members: 154 payloads and the union manifest. Archive length is
  3,953,637 bytes; payload total is 3,903,806 bytes.
- All 143 base payloads match the original approved base archive by length and
  SHA-256. The original archive's SHA-256 is
  `897a6eb57056b911b200551413c65ce7788ba3d448ff8b6b8c143d883180ebd0`.
- All ten companion destinations match their explicitly selected canonical
  sources, including the four guide remappings and root `START-HERE.md`.
  The exact mappings are retained in the completed group and source reviews.
- The embedded `BASE-SOURCE-MANIFEST.json` is the exact original manifest,
  SHA-256 `f1beab01d43e4b5fc6d7b9999ff2795598e3f2ee77c0dc85f1d99e82a15b31f1`.
- The union manifest is 22,999 bytes, SHA-256
  `1c9a8b381b614a05ddf2c5b96e12c8adc07bf0eb473ab238af6ef9ba71f76417`.
  Its full payload names, lengths and hashes match the archive. Archive and
  manifest receipt bindings agree. No competing root `SOURCE-MANIFEST.json`
  is present.
- Independent ZIP inspection checked fixed timestamps, regular-file external
  attributes and stored lengths. The reached test group additionally checked its
  complete fixed ZIP metadata predicate; no claim depends on a later group.
- The already extracted tree contains exactly 155 expected files and 38
  expected directories, no reparse points, and all file lengths/hashes match
  the archive. The independent census found no extra or missing file.

These are exact-byte/source-packaging findings, not proof of software behavior.

## Failure and checks not reached

The suite records `FAILED`, `AssertionError`,
`WORKFLOW_TEST_EXTRA_FILE`. In `census`, that label combines three conjuncts:
regular-file metadata, `st_nlink == 1`, and expected membership. It therefore
does not itself establish that an extra file exists. The original report does
not identify the failing filename or separately report the failing conjunct.

Root's retained read-only diagnosis in `CONTINUATION.md` reports that all 155
files are expected, but Windows `DirEntry.stat(follow_symlinks=False).st_nlink`
was zero while direct `Path.stat(...).st_nlink` was one. Together with the
independently confirmed exact extraction, this supports a test-only cached
metadata false refusal under the unchanged-retained-state premise. It is not
a recovered original per-file trace. The production helper already uses direct
metadata and is unchanged.

The failure occurred in the first `extract()` -> `census()` before the
`relocated-verify` call. No such command or log exists. Consequently:

- Relocated public verification and its no-write comparison: **NOT RUN**.
- Operational guide file/link closure: **NOT RUN**.
- Nine manifest refusal controls: **NOT RUN**.
- Two unapproved-helper bootstrap controls: **NOT RUN**.
- Extra-member refusal fixture: **NOT RUN**.

A fresh test-only continuation may reuse this retained archive after separate
source/selection review. It cannot retroactively turn controls03 into a pass.
Controls01 remains the preserved source-scope preflight failure with no test
output; controls02 was never executed.

## Closure and cost

Outer status is `COMMAND_FAILED`, child exit code 1. Direct child reaped and Job
closed are true; cleanup errors are empty; termination was not requested. Final
active processes and terminated processes are zero, with four lifetime Job
processes. No final-binding failure is recorded.

| Recorded measure | Value |
|---|---:|
| Whole wrapper wall time | 4.884598799981177 s |
| Supervision through cleanup wall time | 1.791381100192666 s |
| Inclusive Job CPU | 0.96875 s |
| Outer wrapper CPU | 0.75 s |
| Known combined CPU | 1.71875 s |
| Peak Job private commitment | 56,758,272 bytes |
| Outer stdout / stderr | 3,248 / 0 bytes |

The suite's 0.25 controller CPU seconds and inner supervision CPU are already
inside the outer accounting; do not add them again. Selected limits were 120
wall seconds, 60 inclusive Job CPU seconds, 384 MiB, four concurrent processes,
2 MiB stdout and 1 MiB stderr. Scope remains local source distribution only;
there was no Lean invocation, new support build, mathematics, service, network,
or external publication.

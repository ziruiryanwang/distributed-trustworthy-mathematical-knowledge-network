# Independent outcome audit: retained-archive continuation04

2026-10-26. Disposition: **PASS for the selected source-distribution continuation
and newly reached relocation/refusal checks.** The retained controls03 source ZIP
was reused, not recreated. Controls03 remains FAILED as recorded in
`OUTCOME-AUDIT.md`; controls01 remains its preflight failure and controls02 was
never run. This pass is not native-build, mathematical, independent-host,
whole-workflow usability, or complete-v5 qualification.

## Exact operation and evidence

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Evidence: `experiments/v5-local-checks/workflow-source-continuation04`.
Root selected this single operation in `EXECUTION04.md` after `REVIEW04.md`.
The retained selection and original both have SHA-256
`0e7c7e2ff68711c8682f76ee1344626d0c99458ae9b5cd6db7cc6f7dad5fadaf`.

This audit read saved reports/streams/argv and reviewed source only. It did not
run/import product or test code, repack, extract, launch native work, alter Git,
or edit prior evidence. Independent read-only checks confirmed all 154 selected
source originals and all 154 snapshots match their selection, as do all 159
external pins. These include the exact retained archive and receipt. The runner
reports no final-binding failure. Immutable owner-controlled input and runtime
premises remain; this is not hermetic execution or protection from an adversarial
same-account writer changing/restoring files between observations.

| Evidence relative to continuation root | SHA-256 |
|---|---|
| `RESULT.json` | `9176ea717c36fc67d445394636e7d01a861302b665ccce6b1592021a911a6a02` |
| `suite/RESULT.json` | `1342c6c15faf5749afa6636c9d783579352d2062a747101bcf3cde1c8f9f9934` |
| `suite/relocated-verify-COMMAND.json` | `1b0556b4278cbc9cd041066fd41d643aef1bc4191fb25883244e071e8b2ed3a9` |
| `suite/relocated-verify.stdout` | `9a86585d8bae1a81d343c4f7f2efaa71e7b0a21c1ac57c2843372afa862a31aa` |

## Six completed groups

1. **Retained exact source projection.** The first group binds the existing
   controls03 pack receipt, all 143 base payloads and ten mapped additions. The
   union has 154 payloads / 155 ZIP members. Archive SHA-256 remains
   `46913cfd1c957720a673ec4a41f770bbcd10a489a04c176ca7bdbcbae5e39c49`,
   length 3,953,637 bytes. Its receipt SHA-256 remains
   `a807b5d365439457c3b2194838f6e5887ac5d71f19c3be6ee4308c6d2f0250a3`.
   The earlier independent exact ZIP/source audit is reusable because these
   inputs and every selected source are unchanged. No new pack command, pack
   output, or base-manifest copy exists in continuation04.
2. **Actual relocated public verification.** The saved command has one attempt,
   isolated `-I -S -B` Python, and the utility inside the new relocated tree.
   Both its `--source-root` and supplied union-manifest hash bind that tree.
   It returned `VERIFIED_EXACT_WORKFLOW_SOURCE_NOT_BUILT`; parsed stdout exactly
   agrees with the suite's verification record. Stderr is empty. The selected
   manifest SHA-256 is
   `1c9a8b381b614a05ddf2c5b96e12c8adc07bf0eb473ab238af6ef9ba71f76417`.
   Before, after, and final successful-tree census records agree: 155 files,
   38 directories, 3,926,805 bytes, map hash
   `b51383cbc8b0586186c9494ab16a6b21d6e1cef1d10c22e046458bd02e6e39c1`.
   Independent saved-tree inspection confirmed every expected file/hash/length,
   exact directories, no extra file and no reparse point. The recorded map hash
   itself is not a separate timestamped filesystem history; it accompanies the
   reviewed before/after test checks and independent final inspection.
3. **Operational documentation file closure.** Six selected guides produce
   27 local inline links, 15 explicit source-script occurrences and 16 declared
   entrypoint roles. Independent inspection confirms each reported target
   resolves inside the delivered tree and is an included payload. The source
   scripts/entrypoints are present. This is the reviewed bounded inline-link
   check, not a general CommonMark parser, executable command exercise, complete
   prose/anchor validation, or recursive preservation of archival evidence links.
4. **Nine manifest refusals.** All selected changed-boundary cases refuse with
   the recorded errors listed below. These are reviewed in-process synthetic
   document mutations, not nine extra subprocesses or repacks.
5. **Two unapproved-helper bootstrap refusals.** Fresh tiny fixtures retain
   the exact utility and respectively 51-byte and 22,041-byte unapproved helpers.
   Independent inspection confirmed two files per fixture, exact utility bytes,
   and the harmless `UNAPPROVED_HELPER_EXECUTED` assertion sentinel. The saved
   errors are the length/pin checks before `exec`; sentinel execution would have
   raised a different uncaught assertion and failed the test.
6. **Extra-member refusal.** The separate preserved extraction contains exactly
   the original 155 files plus `UNSELECTED.txt`, with the expected 42-byte inert
   text; its 38 directories and original file hashes are intact. Actual verify
   refused `SOURCE_BUNDLE_EXTRA_OR_ALIASED_FILE`. The successful relocated tree
   was not mutated and retained its original census.

The suite reports PASS with exactly six groups. Its JSON stdout and saved
`suite/RESULT.json` independently agree after parsing.

| Selected manifest mutation | Actual error |
|---|---|
| Wrong base association | `WORKFLOW_BUNDLE_MANIFEST_PROFILE` |
| Changed base projection | `WORKFLOW_BUNDLE_BASE_PROJECTION` |
| Changed approved companion | `WORKFLOW_BUNDLE_COMPANION_PIN` |
| Missing adjacent export code | `WORKFLOW_BUNDLE_EXACT_SELECTION` |
| Competing old root manifest | `WORKFLOW_BUNDLE_EXACT_SELECTION` |
| Extra file replaces required guide | `WORKFLOW_BUNDLE_EXACT_SELECTION` |
| Wrong full-root verifier | `WORKFLOW_BUNDLE_MANIFEST_PROFILE` |
| Wrong exact base-manifest bytes | `WORKFLOW_BUNDLE_BASE_MANIFEST_PIN` |
| Base hash supplied as union selection | `WORKFLOW_BUNDLE_MANIFEST_PIN` |

Bootstrap errors were `WORKFLOW_BUNDLE_BOOTSTRAP_LENGTH` and
`WORKFLOW_BUNDLE_BOOTSTRAP_PIN`. Thus there are twelve actual refusal cases
across groups four through six, with no unexpected acceptance recorded.

## Clean closure and cost

Outer status is `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit 0. Direct child
reaped and Job closed are true. Cleanup errors are empty; termination was not
requested; final active/terminated process counts are both zero. Lifetime Job
process count is four. The suite's own PASS does not substitute for this outer
closure and final-binding record.

| Recorded measure | Value |
|---|---:|
| Whole wrapper wall time | 10.911098799668252 s |
| Supervision through cleanup wall time | 7.892382399644703 s |
| Inclusive Job CPU | 1.171875 s |
| Outer wrapper CPU | 0.453125 s |
| Known combined CPU | 1.625 s |
| Peak Job private commitment | 51,814,400 bytes |
| Outer stdout / stderr | 13,021 / 0 bytes |

Suite wall time is 7.368938899599016 s and its controller CPU is 0.796875 s;
the latter is already in inclusive Job CPU and must not be added again. Selected
limits remain 120 wall seconds / 60 inclusive Job CPU seconds / 384 MiB / four
concurrent processes / 2 MiB stdout / 1 MiB stderr.

Together, failed controls03 and continuation04 used 3.34375 known combined CPU
seconds and 15.79569759964943 summed wrapper-wall seconds. This does not include
the older preflight01's incompletely recorded CPU or read-only review work, and
must not be advertised as all-in development cost.

## Adoption boundary

The new evidence closes the exact retained archive's selected distribution
verification, selected documentation-file closure and refusal checks. It leaves
the base payloads, native trust policy and prior tests unchanged. There was no
new support build, Lean proof, agent discovery/growth experiment, service lease,
network access, external trial or publication. Source identity is not source
authenticity or permission to execute it; the license remains undecided and the
user's local/unpublished boundary still applies. Full usable/deployable v5 remains
open; do not replace that goal with this source-packaging pass.

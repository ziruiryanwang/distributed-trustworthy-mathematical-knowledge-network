# Dedicated inert host: independent saved-outcome audit

2026-10-28. **PASS for the completed dedicated-host integration described below.**
Two unsuccessful inspections remain failures; the missing inspection subsequently
succeeded under a fresh, smaller, explicitly selected service. This is not full
v5 completion, mathematical acceptance or an independently hosted deployment.

The reviewer read saved reports, sources, selections, inert input files and file
metadata/hashes. No product imports, commands, tests, services, Lean workers,
database connections, owner-state access or Git operations were performed.
All operation paths below are under `experiments/v5-local-checks/` and start with
`dedicated-host-`. [EXECUTION.md](EXECUTION.md) records root's finite selections.

## Package and controls

The file-only assembly and its outer supervision completed successfully. All
**158 actual package files**, their lengths/hashes and the exact directory census
match `assembly01/distribution/ASSEMBLY.json`. Comparison with the original current
build receipt independently confirms six changed paths, four additions and
**148 unchanged files**, exactly as [INTEGRATION-REVIEW.md](INTEGRATION-REVIEW.md)
specified. The native payloads and installation remain unchanged.

| Selected artifact | SHA-256 |
|---|---|
| Package PROFILE | `21bcb169cced5d85c3d2272265ef1f24f6848fbe2da0d2ab3f3acfe27697bba7` |
| Assembly receipt | `b8d75e6973e19de199ed5f0b160837465ae10dba415defac2bd7d78cbf8c6103` |
| Installation manifest | `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27` |
| Controls result | `fa3255d772b7ff3ec2fb2cfaa19f2f47c4b432cab3d886e710dd9e0bc3a52750` |

All 120 PROFILE auxiliary pins agree with the assembly receipt and actual files.
The implementation ID stays
`86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea`.
Assembly selection `902f6074...` and controls selection `434dac69...` remain
bound to their saved results. All 32 selected current/snapshot source instances
(14 assembly sources and two control sources, each checked twice) match their
recorded hashes. All eight public-operation config files match their actual
supervised command pins. Every saved child stdout agrees with its corresponding
result JSON after terminal line endings are removed, including the failures.

Controls01 passed the five prospectively selected groups: ordinary/launcher path
exclusion, producer output exclusion before production, real two-handle Windows
locking and close failures, inert seal refusals, and pending asynchronous task
drain while the host lock remains held. These are the declared real-lock/inert-SDK
controls, not new validation of mathematical codecs, remote-host exclusion or an
OS security sandbox. The source review's narrower trust model remains applicable.

## Actual preparation and recipient inspection

Prepare01 completed once without opening a mathematical owner or invoking native
checking. Its retained manifest is
`d31ee8536962cff8c60c856f107594610d7b82f851c518ec37a838885f3bb4b6`.
The reviewer rechecked all 47 selected unit files against that manifest: **695,269
bytes**, no mismatches. Preparation reports 47 units, 68 names, 17,114 nodes and
437 edges. Both selected target identities match the preserved bundle/config.

The final HOST.json has SHA-256
`f38a1ec2e7168cd0b34daaa0bc1349513a2f501fadda591579deb8a109d80eb5`.
It records 49 custody objects (47 evidence units and two previews), 68 export
locators, 742,244 logical charged bytes and two indexed objects. Its exact snapshot
is `86b3b8ad8c747104dbf733b3a9aa65625222165be255a54d0c4db58fd8d54611`.
Preparation closed index, custody and host lock before reporting success. Directory
metadata shows only the fixed marker, one-zero-byte lock, seal and two stores;
there is no mathematical owner catalog/ADOPTION or native artifact under H.
No store database was opened by this audit.

Serve01 used that seal/PROFILE and its own actual READY endpoint, loopback port
54708, for the selected 120-second lease. Find01 returned one candidate for the
theorem-kind query: `ResetEffects.contextual_iff`, export
`b093eb970b89de31662abccdb05552270225e26b93e4f0dc47a6463b1590f8be`.
The result correctly remains `INCOMPLETE_SEARCH`, with no global completeness or
verified scan-coverage claim. Actual search used two requests, one candidate page
and 4,551 reply bytes. Its outer prepaid ledger conservatively charged the selected
16 requests / 4 MiB; those are distinct accounting views, not conflicting counts.

Preview01 used the actual returned provider/record/snapshot. It obtained the
4,798-byte preview with SHA-256
`f3fd920019c877c33483c8b82bfa1692e300aad7307008cb70edd97d7c32a435`,
matching the prepared target and candidate record. Its disposition remains
`PREVIEW_BOUND_NOT_ACCEPTED`; `evidence_bound` and
`snapshot_membership_reverified` are false. This operation binds selected preview
bytes, not mathematical truth or a fresh proof of index membership.

After the two failures below, Serve02 reopened the **same** generation and PROFILE
under a fresh 30-second lease. Inspection03 used its actual READY port 63684 and
the prior bound target selection. It returned the complete 26,650-byte unit
`c59ee7bd4eed61193dc06729ca76e28887ad83171f11173353e93bb46305c2c4`,
SHA-256 `bf13287aed53c34ccf58798d3e77ab0df1b60f74ed780641de88a9dc7fd813bd`.
The saved evidence JSON reserializes byte-for-byte to the retained original unit;
its independently rehashed source file agrees with the reported length/digest.
The 355-byte locator also matches inspection01's earlier locator, SHA-256
`ab449eac1509ba0326a801cabe50923e77eb4169ab4e58c60a3d8d0a8e768968`.

Inspection03 completed two requests / **27,005 actual reply bytes**, with no failed
attempts. Its result is `INSPECTION_BOUND_NOT_ACCEPTED`: dependencies unchecked,
native usability false, mathematical acceptance false. No successful preparation,
find, preview or mathematical operation was repeated for the continuation.

## Preserved failures and their implications

**Inspect01 failed.** Its actual config selected a 1-MiB locator cap and an 8-MiB
unit cap, departing from ACTUAL-PLAN's smaller caps. The client obtained the valid
355-byte locator, then reported `IncompleteReadError`, with no evidence returned.
The selected provider reserves each request's advertised maximum before dispatch:

\[
\text{sent bytes}+\text{outstanding reservations}+\text{new reservation}
\leq \text{service total reply cap}.
\]

An 8-MiB unit reservation cannot fit an 8-MiB service cap after earlier replies.
The saved service has one failed response and 9,704 sent bytes; this fits the
source-derived quota explanation. The server report does not separately name a
per-response exception, so the observed client error and the source-derived
reason remain distinguished. This is an operation-config failure, not a failed
proof or evidence that the selected theorem is unavailable in custody.

Inspect01's closed ledger retains two requests and **8,388,963 charged reply
bytes** (the actual locator plus the unsuccessful reserved unit maximum), while
HTTP telemetry records only 355 actual reply bytes and one failed attempt.

**Inspect02 also failed.** Root selected smaller caps (4,096 locator, 65,536 unit,
69,632 total bytes) against the original endpoint; that finite service had ended.
The client reported `ConnectionRefusedError` before any response, charged one
request / 4,096 bytes and recorded zero actual reply bytes. Neither failure was
erased, relabeled, renewed or counted as successful inspection.

Root then explicitly selected Serve02 and Inspection03 with new output/diagnostic
paths, the unchanged seal/PROFILE and smaller limits. This was a new finite
remaining-only selection, not an extension of Serve01. Actual success does not
retroactively make the first ACTUAL-PLAN execution a complete pass.

## Closure and costs

All ten supervised operations are terminal. Assembly, controls and the six
successful public calls exited zero; the two failed inspections exited one.
Every outer report has its direct child reaped, Job closed, zero active processes,
zero terminated processes, empty cleanup errors and empty stderr. Both failed
client ledgers are closed with zero pending/reserved requests. The saved reports
therefore show no runtime left active by these selections.

Both services report `LEASE_FINISHED`, provider quiescence, zero active requests,
zero reserved reply bytes, and closed index/custody/host lock. Serve01 completed
five provider requests / 9,704 bytes with one failure; Serve02 completed two /
27,005 bytes with no failures. Neither lease was silently extended. The latest
seal still has the same exact hash; the two successful reopen paths also checked
its saved status counters under the lock.

Known CPU below is final whole-child-Job CPU **plus** the separately reported
launcher/check-runner CPU. Inner controller/native CPU is not added again.

| Operation | Disposition | Known CPU seconds | Reported outer wall seconds |
|---|---|---:|---:|
| Assembly01 | Pass | 1.859375 | 4.523761 |
| Controls01 | Five groups pass | 0.265625 | 0.525313 |
| Prepare01 | Prepared inert host | 1.953125 | 2.202556 |
| Find01 | Candidate returned; incomplete search | 1.000000 | 1.183093 |
| Preview01 | Bound preview | 0.968750 | 1.073814 |
| Inspect01 | Failed | 1.000000 | 1.123948 |
| Inspect02 | Failed | 1.031250 | 3.111512 |
| Serve01 | Original 120-second lease closed | 4.125000 | 121.400480 |
| Inspect03 | Exact inert evidence returned | 0.968750 | 1.133047 |
| Serve02 | Fresh 30-second lease closed | 2.109375 | 31.482032 |
| **Total** | Includes both failures | **15.281250** | Not additive elapsed time |

Clients overlap service wall intervals. Source review, manual/inert configuration
preparation, saved-file audit and operator idle time are not included in these
CPU measurements. Prior theory production, grounding and native build costs were
not rerun or charged anew. No measured speedup follows from this table.

## Retained result pins and supported conclusion

| Result JSON | SHA-256 |
|---|---|
| Prepare01 | `494511df9c0ba206f101bc0ebd5b8dc50d2872bab3fc2b352cbcd33924e287b7` |
| Find01 | `f467a06169b3da4925db0af858d6aefc0514c86474a7abdc8c33916e2e0826ca` |
| Preview01 | `77065fe33292368d3d4a177c4b836cf0bcf98128b0984a6178168734226c5113` |
| Inspect01 failure | `68dad27db16501562e744fda17e5914b5244e4c80cd78b4c1c5f27ce98eac8d8` |
| Inspect02 failure | `c62b7a2deb860c570f44beaf7367d2de35a60a3eda3e913fff8ebbbeab3edfb2` |
| Serve01 | `1f5def70dc3410f806f34e94823cf0e9bc348b16d658128a415d2e322aabc06d` |
| Inspect03 | `88b4d30408048585c5745c605ab474f5e94db3f5e4bb84988e0e5ba5be938b28` |
| Serve02 | `2721f092f4f6502c5439e26e02ae3d525b43aac5cdbd3bc241423cc019b7d212` |

The implemented public role can prepare, search and serve existing exact inert
mathematics without setting up a mathematical owner or running Lean; recipients
retain their original acceptance obligations. Hosting and contributor state are
separate under the reviewed cooperative marker/lock premise. This removes an
unnecessary owner-grounding requirement from the hosting workflow.

The outcome does not establish whole dependency availability, sustained custody,
independent machine/operator failures, hostile-local-user isolation, internet
deployment, broad retrieval quality, net useful-growth advantage or final v5
completion. The package still requires its selected runtime attachments for
verification, even though this host role runs no native mathematical worker.
Those limits are unchanged by a successful byte-service integration.

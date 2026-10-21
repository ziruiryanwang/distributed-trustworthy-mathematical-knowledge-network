# Terminal-I controls: combined actual-outcome audit

2026-10-21, adaptive_audit. **PASS for the combined scoped native-free contract
evidence: nine original passing methods plus one corrected lifecycle method.**
The original ten-method run remains **FAIL**. No product source changed, no
passing method was repeated, and neither run establishes genuine cryptographic
or mathematical acceptance.

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
This independent audit read saved source/selection/result/log files and checked
their lengths, hashes and censuses. It did not import or execute product/test
code, repeat tests, start a worker, build/install software, or mutate Git. Used
sources and both original operation directories remain unchanged.

## Exact saved evidence

All run paths below are under `experiments/v5-local-checks/`.

| Evidence | Original `terminal-i-controls-01` | Follow-up `terminal-i-close-control-01` |
|---|---|---|
| Selection SHA-256 | `b43f3eb450219760ae80a91e29b316743b9a517b34c99d688129c067877037ec` | `725173159658670acfbd066d6b6ef11b7ba8aab905977ba8607cf11a38a70bec` |
| `controls-result.json` SHA-256 | `539b0f9daac8dceebe38521267a7ae42ad2eb7a7099ec7b702ebad1181bceadd` | `70e5d5d96ef3020ddc6e84a5d9c72e381f356c7b2b8261b9369020cd4affc3e7` |
| `RESULT.json` SHA-256 | `56580006ee422e6d764d00a5f1e4ca53f3c1b5d9baf7925dd9efe2136c495987` | `a682688b3aae790d403e305a81cdf487dfd9335a221329c46426c99dcc7309b5` |
| `command/stderr.txt` SHA-256 | `c6e394a2d53ac1b22e7a8b8cabee5791f8affddb94b66b80062e3a88842c6cb0` | `aa3a9be011aa071578759ddb3404b64965e4c39b3ad84ce8162a72b09a416899` |
| Actual stdout/stderr bytes | 0 / 6,169 | 0 / 236 |
| Test outcome | 10 run, 9 pass, 1 failure, 0 errors/skips | 1 run, 1 pass, 0 failures/errors/skips |
| Child exit/status | 1 / `COMMAND_FAILED` | 0 / `COMMAND_EXITED_ZERO_AND_CLOSED` |

The two operation-local selection copies match their respective external
`*-selection.json` exactly. The original runner is
`tools/Run-V5-Check.py`, SHA-256
`44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.
Both use the selected isolated installed Python with `-I -S -B`, canonical cwd,
fresh source snapshots and the frozen local-check supervisor. No new native
mathematical executable is selected by either command.

## Source and runtime identity

Every selected physical source snapshot was independently hash checked: exactly
122 files in original `sources/`, 123 in follow-up `sources/`. The follow-up
preserves all original 122 mappings and adds only
`software/v5/terminal_i/controls_close.py`, SHA-256
`52041fd0b60c4a7165a15e07ceb42a78c62d53459e5e985f8ee9ff8cbd462389`.
All 20 runtime pins are unchanged and independently hash matched in each
selection: 18 Python/runtime files, the origin map and the retained foundation.

Both actual `selected-code/` trees contain exactly 115 files. Each file's length
and hash matches its result-recorded mapping and the named source input; the two
logical maps are identical. They are the origin-repaired 114-file product map
`2ea8322879b2e45afb2a2f5e8d99500bfcfdbe0982cdf14687b1e8bdd0950556`, with exactly
the five reviewed Terminal-I replacements, plus the frozen factory module:

| Logical product path | SHA-256 |
|---|---|
| `v5/evidence_network/packet.py` | `cf8aaa6190d46c4b41792cb54da7da5983d19450cafb65920af2a188afbbcefd` |
| `v5/evidence_network/custody.py` | `c039af086cf73d57191187e9d5b02292c5c9b8a3fb455d67dc719ad8f7d183a0` |
| `v5/evidence_network/transport.py` | `7ac7204b6e97b48eb1764c92b98437ad87e45f0fc62aa78973f5985816d63827` |
| `v5/client/workspace_evidence.py` | `8531ee14e24d60617491b9f00e14ea1f7c410a279d116322489fe763a421ea68` |
| `v5/client/workspace_staged.py` | `ae3dc1a743a0cf4bd2da7f388ed46d6f75f73330802b9263a03a54a230fafd2b` |

The extra logical file is `v5/client/test_workspace_mixed.py`, SHA-256
`478de57908ebffc98093f0139f83e0a06a9609383f237cec4466086736eb0c3e`.
Its factory helpers, not its previous suite, are used. Thus 115 test-staged files
must not be described as a 115-file product successor.

The original harness remains exactly
`42749d5968bd4dea19ac0cc59fd6bd86e0dead7fe4fd9f6e23b65bf2ab6ee372`.
The follow-up's `original-controls.py` is an exact independently checked copy
of those bytes. Both staged foundation copies match 23,313-byte input
`736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c`.
No installation or mathematical acceptance follows from these identity checks.

## Original failure and narrow correction

Original stderr contains exactly one failure:
`test_live_I_dispatch_cache_export_and_close` expected
`CLIENT_CLOSED_FAILED_OR_EXPIRED`, but received
`CLIENT_GRANT_CHANGED_OR_EXPIRED` at the final post-close `describe(token)`.
All preceding checks in that method had completed, including I routing,
receipt-cache reuse, one reservation, byte-exact reexport, client closure,
empty warrant map and retained packet data. It failed on error ordering, not
on acceptance after closure. Its trailing observation was not written, so it
is not counted as an original pass.

The unchanged inherited ordering explains the precise result. Client
`_active` first calls `workspace._grant_active`; orderly close has already
removed that grant from `workspace._grants`. The grant check therefore refuses
before the later closed-client predicate. The follow-up changes only the
expected final refusal to the anchored
`^CLIENT_GRANT_CHANGED_OR_EXPIRED$`, retaining all earlier assertions, original
factory/staging/traps/cleanup, and actual product methods. It imports the exact
saved original harness, overrides that one method and sets explicit singleton
`SELECTED`. The other nine inherited methods are not selected or run.

Root's `TERMINAL-I-CLOSE-LAUNCH.md` independently selected this narrow correction
before execution. The saved follow-up reports exactly that one method and its
completed observation. The original failed run, exit code, costs and logs are
preserved; this audit does not turn it into a 10/10 passing run.

## Contract evidence actually established

The nine original passing methods establish their asserted native-free scope:

- Closed canonical I grammar/profile/rank constraints; old A and mixed forms
  remain distinct; V1 rejects new I wire data.
- Exact V1/V2 profile-bound offers and persisted readback/reopen separation.
- Both fresh and cached same-ModuleID/different-rank journal disagreement refuse
  without caller-supplied expected J, revoke tokens/owners and retain charges.
- Missing I does not fall back to A or native; V1's existing local I capability
  does not imply terminal-I export. Actual A dispatch remains A.
- Real in-process acquisition reaches the I group-opening path; same-live reuse
  avoids a second packet transfer/admission and retains the original budget.
- Actual singleton staging and semantic `NeedBody` demand reach structural
  closure with no issuer call; after endpoint expiry, unchanged sealed import
  completes under the inert I fixture with no extra dispatch, A or mixed call.
- Changed staged packet bytes refuse before admission, with no network fallback.
- Profile, parser-symbol, closed-fixture-owner and foreign-token changes refuse
  through normal failure cleanup.

The corrected one-method pass additionally completes local live-I caching,
one shared reservation, byte-exact reexport and post-close denial/data-retention
evidence. Both JSON reports have empty forbidden-call and event-loop-error
arrays, zero skips, and explicitly false mathematical/cryptographic acceptance
and actual unknown-ID discovery. Asyncio slow-task diagnostic lines in original
stderr are not extra failures or exception-handler events.

These are real facade, custody, structural transport, reader and import-session
paths under **inert issuer receive/liveness/install fixtures**. The provider
exchange is in-process, not a network or discovery run. Event-loop internal
socketpair construction precedes the socket trap. No result here qualifies
genuine receipt verification, live trust withdrawal, TLS, remote availability,
native Lean checking or a hostile-code sandbox.

## Closure and full charged cost

Both runs independently record: direct child reaped, job closed, zero active
and terminated processes, no termination request, and empty cleanup-error list.
The original nonzero exit is the completed test assertion failure, not killed
or incomplete cleanup. The actual stderr/test counts and supervisor results
agree. The fixed per-run caps are unchanged: 45 CPU seconds, 90 wall seconds,
384 MiB, two active processes, and 1 MiB each for stdout/stderr.

| Measured quantity | Original | Follow-up |
|---|---:|---:|
| Final Job user+kernel CPU seconds | 3.140625 | 0.9375 |
| Outer wrapper CPU seconds | 0.546875 | 0.5 |
| Known inclusive CPU seconds | 3.6875 | 1.4375 |
| Recorded total wall seconds | 7.8577239001 | 4.6004757001 |
| Peak Job private commit MiB | 35.8359375 | 29.5234375 |

Combined known charged CPU is **5.125 seconds** and the sum of recorded run wall
durations is **12.4581996002 seconds**. That wall sum excludes human/source-review
time between runs. The supervisor's smaller internal wrapper CPU counters are
subsets of the outer wrapper totals and are not added again. Peak commit is not
summed across sequential jobs. Supervisor caps/measurements remain their stated
scope, not a hermetic accounting of all machine activity or unreported tails.

## Disposition

**PASS_COMBINED_NINE_PLUS_ONE_NATIVE_FREE_TERMINAL_I_CONTRACTS.** The unchanged
five product successors have the selected native-free changed-boundary evidence
needed for root's next distribution decision. There is no remaining product
blocker in these two saved outcomes. Genuine installed I admission/import and
new checked contribution remain separate workload gates; no proof-production,
growth-efficiency or full-v5 claim is made. No further test or retry is selected.

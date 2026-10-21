# One corrected close-refusal control, not a repeated suite

2026-10-21, core_growth. Root-assigned source-only follow-up. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
No runtime, test import, compilation, build, product edit or Git mutation was
performed. Frozen `controls.py`, product sources and failed01 evidence remain
unchanged; the future terminal-I workload is also unchanged.

## Actual failure and source-established cause

`terminal-i-controls-01` records ten methods, nine passes, one assertion failure,
zero errors/skips, no forbidden native/network calls and no event-loop errors.
Its `command/stderr.txt` identifies the sole mismatch: the last assertion in
`test_live_I_dispatch_cache_export_and_close` expected
`CLIENT_CLOSED_FAILED_OR_EXPIRED`, but actual refusal was
`CLIENT_GRANT_CHANGED_OR_EXPIRED`.

This is the intended earlier guard, not a successful post-close operation:

1. `client.workspace_mixed.CommonsClient.close` clears warrants/caches, closes
   its owners, sets closed state, saves its report, then in `finally` removes
   its grant from `workspace._grants`.
2. Decorated `describe` calls the inherited `_enter` before its body.
3. `_enter` calls `_active`; mixed `_active` first calls workspace liveness and
   `workspace._grant_active(self.grant)`.
4. `_grant_active` requires membership in the original grant registry, so it
   refuses immediately after close. The later explicit client-closed predicate
   is not reached. The decorated `describe` body cannot return authority.

The observed exception therefore follows directly from unchanged guard order.
Changing the product to force a later diagnostic would have no safety benefit.
The original control already reached its byte-exact export, same-live hit,
single reservation, cleared-warrant and retained-custody assertions before the
last diagnostic mismatch. That historical failure nevertheless remains FAIL.

## Fresh minimal harness

`software/v5/terminal_i/controls_close.py`, 3444 bytes, SHA-256
`52041fd0b60c4a7165a15e07ceb42a78c62d53459e5e985f8ee9ff8cbd462389`.

It hashes and snapshots the exact frozen original harness, imports that
snapshot without running its main, and subclasses its existing `Controls`.
Only the failed method is overridden. Its original assertions remain intact;
only the post-close regex changes to the exact anchored
`^CLIENT_GRANT_CHANGED_OR_EXPIRED$`.

The original suite variable is replaced **in memory only** with the singleton
method name, and the original main is called. That main explicitly constructs
its suite from `SELECTED`: the other nine methods are not executed. All original
source-map staging, inert factories, real selected facade/custody code,
forbidden-call traps, lifecycle cleanup, counters and result generation remain
unchanged. There is no interception/relaxation of product exceptions or broad
accept-either-error assertion.

Future CLI, only if root selects a fresh bounded operation:

```text
controls_close.py --output <fresh existing ordinary output directory>
```

In addition to the original runner's new selected-source copies and result, the
fresh output receives `original-controls.py`, byte-equal to the frozen source.
No old experiment directory is reused or amended.

## Exact dependencies and retained evidence

| Role | Canonical-root-relative path | SHA-256 |
|---|---|---|
| Frozen original harness | `software/v5/terminal_i/controls.py` | `42749d5968bd4dea19ac0cc59fd6bd86e0dead7fe4fd9f6e23b65bf2ab6ee372` |
| Selected-map basis | `experiments/v5-local-checks/distribution-origin-01-input.json` | `2ea8322879b2e45afb2a2f5e8d99500bfcfdbe0982cdf14687b1e8bdd0950556` |
| Existing inert factory | `software/v5/client/test_workspace_mixed.py` | `478de57908ebffc98093f0139f83e0a06a9609383f237cec4466086736eb0c3e` |
| Selected mixed client | `software/v5/client/workspace_mixed.py` | `eb4e9374707b3e3f03b7e60ad91fd0fd30a3872d3e9fb59fe3f93c039338acbd` |
| Selected atomic client | `software/v5/conjunction_index/client/workspace_atomic.py` | `eea95a6bb12349e5fc7b1e80bc610710ccafc7cbbfd2b40d705d80cdc67c8022` |
| Failed01 controls result | `experiments/v5-local-checks/terminal-i-controls-01/controls-result.json` | `539b0f9daac8dceebe38521267a7ae42ad2eb7a7099ec7b702ebad1181bceadd` |
| Failed01 outer result | `experiments/v5-local-checks/terminal-i-controls-01/RESULT.json` | `56580006ee422e6d764d00a5f1e4ca53f3c1b5d9baf7925dd9efe2136c495987` |

The original harness pins its five terminal-I replacements (cf8aaa61, c039af08,
7ac7204b, 8531ee14, ae3dc1a7), exact foundation and 114-source map. Those pins are
reused without modification; [TERMINAL-I-SOURCE.md](TERMINAL-I-SOURCE.md) records
the complete product hashes. The original factories remain explicitly inert;
their acceptance is never claimed as cryptographic or mathematical evidence.

## Required later result

Require exactly one selected method executed, zero failures/errors/skips,
empty forbidden-call and event-loop-error lists, original cleanup checks passed
and clean outer process closure. The observation must still establish one
inert I call, zero A/mixed calls, one shared verification reservation, byte-exact
reexport, same-live caching, closed live authority, persistent public bytes and
the precise grant-refusal diagnostic. Any failure is preserved; no automatic
retry or weakening follows.

A later one-method pass supplements the original nine passed methods; it does
not rewrite failed01 into a ten-method pass, qualify real cryptography, replace
the pending genuine workload or complete v5. Root owns selection and adoption.

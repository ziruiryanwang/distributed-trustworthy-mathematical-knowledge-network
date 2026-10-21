# Consolidated smoke02: independent narrow source review

2026-10-21, `support_guest`.

Disposition: **PASS_SELECTED_SMOKE02_REPAIR_AND_SELECTOR_NOT_EXECUTION**.
No remaining blocker was found in the selected narrow repair. Root still owns
one fresh finite input/launch and subsequent actual evidence adoption; this is
not a predicted success, an old-allocation renewal or a restart qualification.

## Exact reviewed bytes

- Fresh `software/v5/consolidated_candidate/restart_smoke02.py`, 39791 B:
  `a6e4dd616b614cb01181fa482f9340bd817098ea17453e0cd394bc403345912f`.
- Fresh adjacent `Select-ConsolidatedSmoke02.ps1`, 6962 B:
  `52e4db2bb2888deb5fecb1b8ad6e3005a43d2e26c101d23650913340c7af9d60`.
- Author checkpoint `CONSOLIDATED-SMOKE02-SOURCE.md`:
  `0548f1358b9fc698bd6d0ac32a098d5ffa6c6b3c70a6cb61bb9164e0868cfcbe`.
- Preserved smoke01 failure audit `CONSOLIDATED-SMOKE-OUTCOME.md`:
  `983d7ca81a6b3dac22e59f8f83dba8ae3d12262ad916822c9707285dedc68eba`.
- Used predecessor `restart_smoke.py` remains 38004 B:
  `e8b3a0257785e82242d20eb98a24fa4b3fad3b5884e77dc6e7a791598a6cccc2`.

The reviewer read the selection, author checkpoint and every changed source
region. An independent ordered-text reconstruction restored the exact old
adapter by removing the new helper and reverting only the import, committed
comparison/report block and pending-census block. Outside these selected regions
the sources are identical after newline/trailing-blank normalization. This is
stronger than merely comparing unordered sets of changed lines. No product
implementation, installed bytes, previous source or state is changed.

## Receipt comparison

The new expected response is the existing installed `public_response` applied
to `first.ledger.public(committed)` and the actual returned route, with the
original expected bindings/request ID. Full response equality is required,
alongside exact `committed["manifest"] == raw`. This follows the intentional
local-diagnostics-to-public-receipt projection, rather than deleting arbitrary
keys from persisted expectations.

The complete unprojected `committed` object remains the restart baseline.
Every later request/receipt/grant/cell/funding/custody/index preservation check
is unchanged. The returned response and original manifest plus the committed
manifest/outcome and projected-response hashes are saved before the equality
assertion, so a repeated comparison failure would retain more direct evidence.

## Pending task evidence and finite settlement

`pending_observation()` counts every unfinished noncurrent asyncio task, with
no type exemption. At most 32 code identities are serialized, each consisting
of bounded installed-relative/owner/fixed-unknown source label, code-qualified
name and first line number. It does not expose task names, repr, arguments,
locals, stack values or token-bearing coroutine state. Identity truncation
does not truncate the total count used by the failure test.

After all owned closes, the adapter records the first census, yields exactly
once using `await asyncio.sleep(0)`, and records the second. Any remaining task
still adds `pending-async-actors`; the original OUTER deadline is checked
immediately afterward. No arbitrary task is cancelled, no task kind is ignored,
and there is no retry loop, extra budget or extension. This is bounded settling
of already-scheduled shutdown work, not retrospective identification or waiver
of smoke01's unsaved task. All concrete owned-actor and Node closure assertions
remain unchanged.

## Selector and unchanged boundary

Independent ordered comparison shows selector02 differs from selector01 only
by its explanatory first comment, fresh `consolidated-restart-smoke-02` names,
fresh `restart_smoke02.py` source/argv path and trailing blank. PowerShell parse
passes. Input, selection and output paths were absent at review time. It selects
the same adopted installation, 121 SDK rows, 148 runtime pins, four outer
sources, retained fixture and original-duration one-time horizons. Its
150 CPU / 300 wall seconds, 512 MiB and six-process limits are unchanged.

Installed-origin and runtime pre/post validation, sole submit, source withdrawal,
B1 complete close before B2, sealed original two-run generation, fresh locator,
original deadlines, two-descriptor unknown-ID discovery, exact retained bytes,
zero mathematical execution and all final-state assertions are inherited
unchanged. No installation rebuild or separate diagnostic network run is needed
for this adapter change.

This reviewer performed source/data/hash and PowerShell-parser checks only,
without executing/importing the adapter or product, generating a smoke input,
running a test/network/proof, or touching Git. Smoke01 remains FAIL and its
27.9375 known CPU seconds remain charged. Actual smoke02, if root launches it,
must receive a separate outcome audit and must not borrow an unexecuted restart
pass from this source review. Full v5 and later lifecycle work remain separate.
